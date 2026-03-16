from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from aas1.aas5_ideation import (
    AAS5_DOCTRINE_VERSION,
    AAS5_TOPOLOGY_MODE,
    EXECUTION_PARALLELISM_RECORD,
    SWARM_TOPOLOGY_GRAPH,
    audit_artifact_path,
    auditor_nodes,
    build_aas5_ideation_nodes,
    build_artifact_provenance,
    build_audit_payload,
    build_execution_parallelism_payload,
    build_lane_plan_payload,
    build_lane_report_payload,
    build_model_audit,
    build_topology_graph_payload,
    lane_manager,
    lane_plan_path,
    lane_report_path,
    lane_reporter,
    lane_worker_node_ids,
    make_run_key,
)
from aas1.artifact_registry import ArtifactRegistry
from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now
from aas1.provider_runtime import ProviderRuntimeRegistry
from aas1.task_hardening import (
    build_placeholder_child_result_merge_package,
    build_placeholder_future_branch_report,
    build_placeholder_swarm_execution_record,
    build_placeholder_team_plan,
)
from aas1.workflow_policy_engine import future_exploration_for, improvement_trigger_policy_for, stage_team_roles_for
from aas1.workflow_context_store import WorkflowContextStore


class CodexTeamDispatcher:
    """Plan and optionally execute explicit Codex child-session teams."""

    LIVE_CHILD_CAP = 6

    def __init__(
        self,
        repo_root: Path,
        *,
        artifact_registry: ArtifactRegistry,
        provider_runtime: ProviderRuntimeRegistry,
        context_store: WorkflowContextStore | None = None,
    ) -> None:
        self.repo_root = repo_root
        self.registry = artifact_registry
        self.provider_runtime = provider_runtime
        self.context_store = context_store
        self.dispatch_root = ensure_dir(runtime_state_dir(repo_root) / "codex_dispatch")
        self.session_root = Path.home() / ".codex" / "sessions"
        self.child_schema_path = repo_root / "docs" / "schemas" / "child_agent_result.schema.json"
        self.workflow_policy_root = runtime_state_dir(repo_root) / "workflow_policy"

    def build_recommendations(
        self,
        *,
        task_id: str,
        workflow_id: str,
        request_payload: dict[str, Any],
        human_record: dict[str, Any],
        exploration_record: dict[str, Any],
    ) -> dict[str, Any]:
        context_refs = [
            "docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v5.md",
            "docs/platform_overlays/codex/TEAM_FORMATION.md",
            f"docs/task_workspaces/{task_id}/HUMAN_DECISION_RECORD.json",
            f"docs/task_workspaces/{task_id}/EXPLORATION_CONTROL_RECORD.json",
            f"docs/task_workspaces/{task_id}/RESEARCH_PROGRAM_REPORT.json",
            f"docs/task_workspaces/{task_id}/RESEARCH_STRATEGY_REPORT.json",
        ]
        parent_route = self.provider_runtime.resolve_model_route("codex", "research_director")
        dispatch_candidates = []
        contradiction_count = int(human_record.get("evidence_summary", {}).get("contradiction_count", 0))
        for candidate in human_record.get("spawn_candidates", [])[:3]:
            child_roles = self._child_roles_for_spawn(
                task_id=task_id,
                spawn_candidate=candidate,
                contradiction_count=contradiction_count,
            )
            dispatch_candidates.append(
                {
                    "action_label": "spawn_program",
                    "instruction": candidate["spawn_id"],
                    "spawn_id": candidate["spawn_id"],
                    "program_title": candidate["program_title"],
                    "target_domain": candidate["target_domain"],
                    "program_goal": candidate.get("program_goal", ""),
                    "priority_score": candidate.get("priority_score"),
                    "approval_status": "AWAITING_OPERATOR_APPROVAL",
                    "dispatch_readiness": "READY",
                    "team_mode": "STAGE_TEAM",
                    "parent_role": "research_director",
                    "parent_model": parent_route["model"],
                    "merge_owner": "parent",
                    "context_refs": context_refs,
                    "child_roles": child_roles,
                    "notes": [
                        "Children are read-only by default.",
                        "Parent session retains HITL, merge, and shared-state authority.",
                    ],
                }
            )
        return {
            "type": "TEAM_DISPATCH_RECOMMENDATIONS",
            "task_id": task_id,
            "workflow_id": workflow_id,
            "command_modifier": request_payload.get("command_modifier"),
            "priority_order": list(exploration_record.get("priority_order", [])),
            "dispatch_candidates": dispatch_candidates,
            "created_at": utc_now(),
        }

    def dispatch_recommendation_summary(
        self,
        recommendations: dict[str, Any],
    ) -> list[dict[str, Any]]:
        summary = []
        for candidate in recommendations.get("dispatch_candidates", []):
            summary.append(
                {
                    "action_label": candidate["action_label"],
                    "instruction": candidate["instruction"],
                    "spawn_id": candidate["spawn_id"],
                    "program_title": candidate["program_title"],
                    "target_domain": candidate["target_domain"],
                    "team_mode": candidate["team_mode"],
                    "dispatch_readiness": candidate["dispatch_readiness"],
                    "approval_status": candidate["approval_status"],
                    "child_roles": [item["role"] for item in candidate.get("child_roles", [])],
                }
            )
        return summary

    def prepare_dispatch(
        self,
        *,
        task_id: str,
        workflow_id: str,
        human_record: dict[str, Any],
        recommendations: dict[str, Any],
        action_label: str,
        instruction: str,
        parent_provider: str = "codex",
        parent_agent_name: str | None = None,
        parent_session_id: str | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        candidate = self._select_candidate(
            task_id=task_id,
            recommendations=recommendations,
            action_label=action_label,
            instruction=instruction,
        )
        now = utc_now()
        parent_session = self._resolve_parent_session(
            provider=parent_provider,
            task_id=task_id,
            agent_name=parent_agent_name,
            session_id=parent_session_id,
        )
        dispatch_id = f"{self._slug(candidate['spawn_id'])}-{now.replace(':', '').replace('-', '')}"
        if self._is_aas5_ideation_candidate(candidate):
            return self._prepare_aas5_ideation_dispatch(
                task_id=task_id,
                workflow_id=workflow_id,
                candidate=candidate,
                parent_session=parent_session,
                dispatch_id=dispatch_id,
                generated_at=now,
                action_label=action_label,
                instruction=instruction,
                dry_run=dry_run,
            )
        max_children = len(candidate.get("child_roles", []))
        max_live_children = max(1, min(self.LIVE_CHILD_CAP, max(max_children, 1)))
        planned_wave_count = max(1, (max(max_children, 1) + max_live_children - 1) // max_live_children)
        orchestration_topology = "parent_lane_managers" if candidate.get("future_exploration") else "flat_stage_team"
        payload = {
            "version": "1.0",
            "task_id": task_id,
            "workflow_id": workflow_id,
            "dispatch_id": dispatch_id,
            "status": "PLANNED",
            "created_at": now,
            "updated_at": now,
            "selection": {
                "action_label": candidate["action_label"],
                "instruction": candidate["instruction"],
                "spawn_id": candidate["spawn_id"],
                "program_title": candidate["program_title"],
                "target_domain": candidate["target_domain"],
                "program_goal": candidate.get("program_goal", ""),
                "priority_score": candidate.get("priority_score"),
            },
            "parent": {
                "provider": parent_session["provider"],
                "agent_name": parent_session["agent_name"],
                "session_id": parent_session["session_id"],
                "role": candidate["parent_role"],
                "merge_owner": candidate["merge_owner"],
                "model": candidate["parent_model"],
                "reasoning_effort": "xhigh",
                "model_audit": self._model_audit(
                    policy_target=candidate["parent_model"],
                    actual_runtime_model=None,
                    reasoning_effort="xhigh",
                    auditability="planned_not_verified",
                    routing_basis="Dispatcher-planned parent routing for Codex team execution.",
                ),
            },
            "spawn_policy": {
                "team_mode": candidate["team_mode"],
                "orchestration_topology": orchestration_topology,
                "manager_count": 0,
                "max_children": max_children,
                "max_live_children": max_live_children,
                "spawn_batch_size": max_live_children,
                "planned_wave_count": planned_wave_count,
                "scheduling_mode": "batched_by_runtime_cap",
                "default_child_permission": "read_only",
                "hitl_gate_owner": "parent",
                "shared_state_owner": "parent",
            },
            "manager_orchestrators": [],
            "context_refs": list(candidate.get("context_refs", [])),
            "children": [
                {
                    "child_id": f"{dispatch_id}-{index + 1}",
                    "agent_name": role["role"],
                    "role": role["role"],
                    "tier": role["tier"],
                    "model": role["model"],
                    "reasoning_effort": role["reasoning_effort"],
                    "model_audit": self._model_audit(
                        policy_target=role["model"],
                        actual_runtime_model=None,
                        reasoning_effort=role["reasoning_effort"],
                        auditability="planned_not_verified",
                        routing_basis="Dispatcher-planned child routing for Codex team execution.",
                    ),
                    "objective": role["objective"],
                    "permission": role["permission"],
                    "safe_zone_paths": list(role.get("safe_zone_paths", [])),
                    "expected_artifact": role["expected_artifact"],
                    "branch_id": role.get("branch_id"),
                    "branch_label": role.get("branch_label"),
                    "parent_role": role.get("parent_role"),
                    "branch_kind": role.get("branch_kind"),
                    "lane_id": role.get("lane_id"),
                    "lane_label": role.get("lane_label"),
                    "lane_strategy": role.get("lane_strategy"),
                    "manager_id": None,
                    "manager_lane_id": role.get("lane_id"),
                    "status": "PLANNED",
                }
                for index, role in enumerate(candidate.get("child_roles", []))
            ],
            "notes": list(candidate.get("notes", []))
            + [
                f"Plan child spawning in {planned_wave_count} wave(s) of up to {max_live_children} live children to respect runtime thread caps."
            ],
        }
        if candidate.get("future_exploration"):
            manager_specs = self._build_lane_manager_specs(children=payload["children"])
            payload["spawn_policy"]["manager_count"] = len(manager_specs)
            payload["manager_orchestrators"] = manager_specs
            child_to_manager = {
                child_id: manager["manager_id"]
                for manager in manager_specs
                for child_id in manager["managed_child_ids"]
            }
            for child in payload["children"]:
                child["manager_id"] = child_to_manager.get(child["child_id"])
                child["manager_lane_id"] = child.get("lane_id")
            payload["future_exploration"] = {
                "enabled": True,
                "current_stage": candidate["future_exploration"].get("current_stage"),
                "max_depth": int(candidate["future_exploration"].get("max_depth", 2)),
                "convergence_owner": candidate["future_exploration"].get("convergence_owner", "parent"),
                "convergence_artifact": f"docs/task_workspaces/{task_id}/FUTURE_CONVERGENCE_REPORT.json",
                "improvement_trigger_policy": candidate["future_exploration"].get("improvement_trigger_policy"),
                "radical_trigger_policy": candidate["future_exploration"].get("radical_trigger_policy"),
                "branches": [
                    {
                        "branch_id": item["branch_id"],
                        "parent_role": item["parent_role"],
                        "branch_kind": item["branch_kind"],
                        "branch_label": item["branch_label"],
                        "lane_id": item["lane_id"],
                        "lane_label": item["lane_label"],
                        "lane_strategy": item["lane_strategy"],
                        "objective": item["objective"],
                        "expected_artifact": item["expected_artifact"],
                        "radical_candidate": bool(item.get("radical_candidate")),
                        "status": "PLANNED",
                    }
                    for item in candidate["future_exploration"].get("branches", [])
                ],
            }
        if dry_run:
            return payload
        self.registry.write_yaml_artifact(task_id, "TEAM_PLAN.yaml", payload, schema_name="team_plan")
        future_branch_report_ref = None
        if payload.get("future_exploration"):
            future_branch_report = {
                "type": "FUTURE_BRANCH_REPORT",
                "task_id": task_id,
                "workflow_id": workflow_id,
                "dispatch_id": dispatch_id,
                "team_mode": payload["spawn_policy"]["team_mode"],
                "current_stage": payload["future_exploration"].get("current_stage"),
                "convergence_owner": payload["future_exploration"].get("convergence_owner"),
                "convergence_artifact": payload["future_exploration"].get("convergence_artifact"),
                "recommendation_authorized": False,
                "blocking_gates": [
                    "Team dispatch has not completed yet.",
                    "Run validate_swarm_execution_record.py before presenting a recommendation.",
                ],
                "improvement_trigger_policy": payload["future_exploration"].get("improvement_trigger_policy"),
                "radical_trigger_policy": payload["future_exploration"].get("radical_trigger_policy"),
                "branches": list(payload["future_exploration"].get("branches", [])),
                "created_at": payload["created_at"],
                "updated_at": payload["updated_at"],
            }
            branch_path = self.registry.write_json_artifact(
                task_id,
                "FUTURE_BRANCH_REPORT.json",
                future_branch_report,
                schema_name="future_branch_report",
            )
            future_branch_report_ref = str(branch_path.relative_to(self.repo_root)).replace("\\", "/")
            payload["future_exploration"]["branch_report_ref"] = future_branch_report_ref
            self.registry.write_yaml_artifact(task_id, "TEAM_PLAN.yaml", payload, schema_name="team_plan")
        self._update_dispatch_state(
            task_id=task_id,
            workflow_id=workflow_id,
            action_label=action_label,
            instruction=instruction,
            team_plan_ref="docs/task_workspaces/{}/TEAM_PLAN.yaml".format(task_id),
            workflow_status="APPROVED_FOR_TEAM_DISPATCH",
            future_branch_report_ref=future_branch_report_ref,
        )
        return payload

    def _is_aas5_ideation_candidate(self, candidate: dict[str, Any]) -> bool:
        future_exploration = dict(candidate.get("future_exploration") or {})
        if str(future_exploration.get("current_stage") or "").upper() != "IDEATION":
            return False
        branches = list(future_exploration.get("branches") or [])
        lane_ids = {str(item.get("lane_id") or "") for item in branches}
        return len(branches) == 12 and lane_ids == {"alpha", "beta", "gamma", "radical"}

    def _prepare_aas5_ideation_dispatch(
        self,
        *,
        task_id: str,
        workflow_id: str,
        candidate: dict[str, Any],
        parent_session: dict[str, str],
        dispatch_id: str,
        generated_at: str,
        action_label: str,
        instruction: str,
        dry_run: bool,
    ) -> dict[str, Any]:
        future_policy = dict(candidate.get("future_exploration") or {})
        run_key = make_run_key(task_id, workflow_id)
        title = str(candidate.get("program_title") or "AAS5 Ideation Dispatch")
        worker_nodes = build_aas5_ideation_nodes(
            task_id=task_id,
            branch_specs=list(future_policy.get("branches") or []),
            title=title,
        )
        branch_specs = []
        for branch in future_policy.get("branches", []):
            lane_id = str(branch.get("lane_id") or "")
            parent_role = str(branch.get("parent_role") or "")
            node = next(
                (item for item in worker_nodes if item.tier == "lane_worker" and item.lane_id == lane_id and item.role == parent_role),
                None,
            )
            if node is None:
                continue
            branch_specs.append(
                {
                    "branch_id": str(branch.get("branch_id") or ""),
                    "parent_role": parent_role,
                    "branch_kind": str(branch.get("branch_kind") or ""),
                    "branch_label": str(branch.get("branch_label") or ""),
                    "lane_id": lane_id,
                    "lane_label": str(branch.get("lane_label") or lane_id.title()),
                    "lane_strategy": str(branch.get("lane_strategy") or ""),
                    "objective": str(branch.get("objective") or ""),
                    "radical_candidate": bool(branch.get("radical_candidate")),
                    "artifact_ref": f"docs/task_workspaces/{task_id}/{node.expected_artifact}",
                }
            )
        lane_ids = [
            lane_id
            for lane_id in (future_policy.get("lane_order") or [])
            if lane_manager(worker_nodes, lane_id) is not None
        ]
        payload = build_placeholder_team_plan(
            task_id=task_id,
            workflow_id=workflow_id,
            dispatch_id=dispatch_id,
            run_key=run_key,
            generated_at=generated_at,
            title=title,
            agent_name=parent_session.get("agent_name"),
            authority_surfaces=[],
            future_policy=future_policy,
            branch_specs=branch_specs,
            aas5_nodes=worker_nodes,
        )
        payload["selection"] = {
            "action_label": candidate["action_label"],
            "instruction": candidate["instruction"],
            "spawn_id": candidate["spawn_id"],
            "program_title": title,
            "target_domain": candidate["target_domain"],
            "program_goal": candidate.get("program_goal", ""),
            "priority_score": candidate.get("priority_score"),
        }
        payload["parent"]["provider"] = parent_session["provider"]
        payload["parent"]["agent_name"] = parent_session["agent_name"]
        payload["parent"]["session_id"] = parent_session["session_id"]
        payload["parent"]["merge_owner"] = candidate["merge_owner"]
        payload["parent"]["model"] = candidate["parent_model"]
        payload["parent"]["model_audit"] = self._model_audit(
            policy_target=candidate["parent_model"],
            actual_runtime_model=None,
            reasoning_effort="xhigh",
            auditability="runtime_not_exposed",
            routing_basis="Dispatcher-planned AAS5 ordinary ideation parent routing for Codex team execution.",
        )
        payload["context_refs"] = list(candidate.get("context_refs", []))
        payload["notes"] = list(candidate.get("notes", [])) + list(payload.get("notes", []))
        for child in payload.get("children", []):
            if str(child.get("tier") or "") == "lane_worker":
                child["manager_id"] = child.get("parent_node_id")
                child["manager_lane_id"] = child.get("lane_id")
        if dry_run:
            return payload
        self.registry.write_yaml_artifact(task_id, "TEAM_PLAN.yaml", payload, schema_name="team_plan")
        future_branch_report = build_placeholder_future_branch_report(
            task_id=task_id,
            workflow_id=workflow_id,
            dispatch_id=dispatch_id,
            run_key=run_key,
            generated_at=generated_at,
            future_policy=future_policy,
            branch_specs=branch_specs,
            aas5_nodes=worker_nodes,
        )
        branch_path = self.registry.write_json_artifact(
            task_id,
            "FUTURE_BRANCH_REPORT.json",
            future_branch_report,
            schema_name="future_branch_report",
        )
        for lane_id in lane_ids:
            manager = lane_manager(worker_nodes, lane_id)
            reporter = lane_reporter(worker_nodes, lane_id)
            if manager is None or reporter is None:
                continue
            self.registry.write_json_artifact(
                task_id,
                lane_plan_path(lane_id),
                build_lane_plan_payload(
                    task_id=task_id,
                    workflow_id=workflow_id,
                    run_key=run_key,
                    lane_id=lane_id,
                    lane_label=manager.lane_label or lane_id.title(),
                    lane_strategy=manager.lane_strategy or "",
                    manager_id=manager.node_id,
                    worker_node_ids=lane_worker_node_ids(worker_nodes, lane_id),
                    reporter_node_id=reporter.node_id,
                    generated_at=generated_at,
                ),
                schema_name="lane_plan",
            )
            self.registry.write_json_artifact(
                task_id,
                lane_report_path(lane_id),
                build_lane_report_payload(
                    task_id=task_id,
                    workflow_id=workflow_id,
                    run_key=run_key,
                    lane_id=lane_id,
                    lane_label=reporter.lane_label or lane_id.title(),
                    reporter_node_id=reporter.node_id,
                    worker_node_ids=lane_worker_node_ids(worker_nodes, lane_id),
                    generated_at=generated_at,
                ),
                schema_name="lane_convergence_report",
            )
        for node in auditor_nodes(worker_nodes):
            self.registry.write_json_artifact(
                task_id,
                audit_artifact_path(node.audit_domain or ""),
                build_audit_payload(
                    artifact_type={
                        "compliance": "SWARM_COMPLIANCE_AUDIT",
                        "runtime": "RUNTIME_AUDIT_RECORD",
                        "authority": "AUTHORITY_COVERAGE_AUDIT",
                        "adversarial": "ADVERSARIAL_INTEGRITY_REVIEW",
                    }[node.audit_domain or "adversarial"],
                    task_id=task_id,
                    workflow_id=workflow_id,
                    run_key=run_key,
                    owner_node_id=node.node_id,
                    generated_at=generated_at,
                    summary=f"Placeholder audit artifact for {node.role_label}.",
                    blocking_gates=["Pending real AAS5 participant execution."],
                ),
                schema_name="aas5_audit_record",
            )
        self.registry.write_json_artifact(
            task_id,
            SWARM_TOPOLOGY_GRAPH,
            build_topology_graph_payload(
                task_id=task_id,
                workflow_id=workflow_id,
                run_key=run_key,
                generated_at=generated_at,
                nodes=worker_nodes,
            ),
            schema_name="swarm_topology_graph",
        )
        self.registry.write_json_artifact(
            task_id,
            EXECUTION_PARALLELISM_RECORD,
            build_execution_parallelism_payload(
                task_id=task_id,
                workflow_id=workflow_id,
                run_key=run_key,
                generated_at=generated_at,
                nodes=worker_nodes,
                max_live_children=self.LIVE_CHILD_CAP,
            ),
            schema_name="execution_parallelism_record",
        )
        self.registry.write_json_artifact(
            task_id,
            "CHILD_RESULT_MERGE_PACKAGE.json",
            build_placeholder_child_result_merge_package(
                task_id=task_id,
                workflow_id=workflow_id,
                dispatch_id=dispatch_id,
                run_key=run_key,
                aas5_nodes=worker_nodes,
                lane_ids=lane_ids,
            ),
            schema_name="child_result_merge_package",
        )
        self.registry.write_json_artifact(
            task_id,
            "SWARM_EXECUTION_RECORD.json",
            build_placeholder_swarm_execution_record(
                task_id=task_id,
                generated_at=generated_at,
                agent_name=parent_session.get("agent_name"),
                future_policy=future_policy,
                workflow_id=workflow_id,
                run_key=run_key,
                branch_specs=branch_specs,
                aas5_nodes=worker_nodes,
                team_plan_ref=f"docs/task_workspaces/{task_id}/TEAM_PLAN.yaml",
                merge_package_ref=f"docs/task_workspaces/{task_id}/CHILD_RESULT_MERGE_PACKAGE.json",
                topology_graph_ref=f"docs/task_workspaces/{task_id}/{SWARM_TOPOLOGY_GRAPH}",
                parallelism_record_ref=f"docs/task_workspaces/{task_id}/{EXECUTION_PARALLELISM_RECORD}",
            ),
            schema_name="swarm_execution_record",
        )
        payload["future_exploration"]["branch_report_ref"] = str(branch_path.relative_to(self.repo_root)).replace("\\", "/")
        self.registry.write_yaml_artifact(task_id, "TEAM_PLAN.yaml", payload, schema_name="team_plan")
        self._update_dispatch_state(
            task_id=task_id,
            workflow_id=workflow_id,
            action_label=action_label,
            instruction=instruction,
            team_plan_ref=f"docs/task_workspaces/{task_id}/TEAM_PLAN.yaml",
            workflow_status="APPROVED_FOR_TEAM_DISPATCH",
            future_branch_report_ref=payload["future_exploration"]["branch_report_ref"],
        )
        return payload

    def _build_lane_manager_specs(self, *, children: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for child in children:
            lane_id = str(child.get("lane_id") or "")
            if not lane_id:
                continue
            grouped.setdefault(lane_id, []).append(child)
        managers: list[dict[str, Any]] = []
        for lane_id, lane_children in sorted(grouped.items()):
            lane_label = str(lane_children[0].get("lane_label") or lane_id.title())
            lane_strategy = str(lane_children[0].get("lane_strategy") or "")
            manager_id = f"manager:{lane_id}"
            managers.append(
                {
                    "manager_id": manager_id,
                    "agent_name": f"{lane_id}_manager",
                    "role": "lane_manager",
                    "tier": "future_lane_manager",
                    "lane_id": lane_id,
                    "lane_label": lane_label,
                    "lane_strategy": lane_strategy,
                    "model": "gpt-5.4",
                    "reasoning_effort": "high",
                    "model_audit": self._model_audit(
                        policy_target="gpt-5.4",
                        actual_runtime_model=None,
                        reasoning_effort="high",
                        auditability="planned_not_verified",
                        routing_basis="Dispatcher-planned lane-manager routing for Codex team execution.",
                    ),
                    "objective": (
                        f"Manage the {lane_label} lane, preserve independence across its three leaf branch agents, "
                        "and return a lane-local convergence signal without overriding the parent orchestrator."
                    ),
                    "permission": "read_only",
                    "safe_zone_paths": list(lane_children[0].get("safe_zone_paths") or []),
                    "managed_branch_ids": [str(child.get("branch_id") or "") for child in lane_children],
                    "managed_child_ids": [str(child.get("child_id") or "") for child in lane_children],
                    "managed_child_count": len(lane_children),
                    "status": "PLANNED",
                }
            )
        return managers

    def execute_dispatch(self, *, team_plan: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            payload = {
                "type": "TEAM_DISPATCH_RECORD",
                "doctrine_version": team_plan.get("doctrine_version"),
                "topology_mode": team_plan.get("topology_mode"),
                "task_id": team_plan["task_id"],
                "workflow_id": team_plan["workflow_id"],
                "run_key": team_plan.get("run_key"),
                "dispatch_id": team_plan["dispatch_id"],
                "status": "DRY_RUN",
                "execution_mode": "codex_exec_sequential",
                "selection": dict(team_plan["selection"]),
                "team_plan_ref": f"docs/task_workspaces/{team_plan['task_id']}/TEAM_PLAN.yaml",
                "children": [],
                "created_at": utc_now(),
                "updated_at": utc_now(),
            }
            if team_plan.get("future_exploration"):
                payload["future_exploration"] = {
                    "enabled": True,
                    "current_stage": team_plan["future_exploration"].get("current_stage"),
                    "branch_count": len(team_plan["future_exploration"].get("branches", [])),
                    "convergence_artifact": team_plan["future_exploration"].get("convergence_artifact"),
                    "improvement_trigger_policy": team_plan["future_exploration"].get("improvement_trigger_policy"),
                    "radical_trigger_policy": team_plan["future_exploration"].get("radical_trigger_policy"),
                }
            return payload
        child_runs = []
        for child in team_plan.get("children", []):
            run_result = self._run_child(
                team_plan=team_plan,
                child=child,
                parent_agent_name=team_plan["parent"]["agent_name"],
                parent_session_id=team_plan["parent"]["session_id"],
            )
            child_runs.append(run_result)
            child["status"] = run_result["status"]
            if child.get("role") == "memory_reuse_analyst" and run_result["status"] == "COMPLETED":
                context_ref = str(run_result.get("output_artifact") or "")
                if context_ref and context_ref not in team_plan.get("context_refs", []):
                    team_plan.setdefault("context_refs", []).append(context_ref)
                note = "Memory-reuse considerations are advisory context for later child sessions and the parent merge."
                if note not in team_plan.get("notes", []):
                    team_plan.setdefault("notes", []).append(note)
        completed = sum(1 for item in child_runs if item["status"] == "COMPLETED")
        failed = len(child_runs) - completed
        status = "TEAM_EXECUTION_COMPLETED"
        if child_runs and completed == 0:
            status = "TEAM_EXECUTION_FAILED"
        elif failed:
            status = "TEAM_EXECUTION_PARTIAL_FAILURE"
        team_plan["status"] = status
        team_plan["updated_at"] = utc_now()
        self.registry.write_yaml_artifact(team_plan["task_id"], "TEAM_PLAN.yaml", team_plan, schema_name="team_plan")
        record = {
            "type": "TEAM_DISPATCH_RECORD",
            "doctrine_version": team_plan.get("doctrine_version"),
            "topology_mode": team_plan.get("topology_mode"),
            "task_id": team_plan["task_id"],
            "workflow_id": team_plan["workflow_id"],
            "run_key": team_plan.get("run_key"),
            "dispatch_id": team_plan["dispatch_id"],
            "status": status,
            "execution_mode": "codex_exec_sequential",
            "selection": dict(team_plan["selection"]),
            "team_plan_ref": f"docs/task_workspaces/{team_plan['task_id']}/TEAM_PLAN.yaml",
            "children": child_runs,
            "created_at": team_plan["created_at"],
            "updated_at": utc_now(),
        }
        if team_plan.get("future_exploration"):
            record["future_exploration"] = {
                "enabled": True,
                "current_stage": team_plan["future_exploration"].get("current_stage"),
                "branch_count": len(team_plan["future_exploration"].get("branches", [])),
                "convergence_artifact": team_plan["future_exploration"].get("convergence_artifact"),
                "improvement_trigger_policy": team_plan["future_exploration"].get("improvement_trigger_policy"),
                "radical_trigger_policy": team_plan["future_exploration"].get("radical_trigger_policy"),
            }
        self.registry.write_json_artifact(
            team_plan["task_id"],
            "TEAM_DISPATCH_RECORD.json",
            record,
            schema_name="team_dispatch_record",
        )
        merge_prompt_path = self.registry.write_markdown_artifact(
            team_plan["task_id"],
            "PARENT_MERGE_PROMPT.md",
            self._render_merge_prompt(team_plan=team_plan, child_runs=child_runs),
        )
        self._update_dispatch_state(
            task_id=team_plan["task_id"],
            workflow_id=team_plan["workflow_id"],
            action_label=team_plan["selection"]["action_label"],
            instruction=team_plan["selection"]["instruction"],
            team_plan_ref=f"docs/task_workspaces/{team_plan['task_id']}/TEAM_PLAN.yaml",
            dispatch_record_ref=f"docs/task_workspaces/{team_plan['task_id']}/TEAM_DISPATCH_RECORD.json",
            merge_prompt_ref=str(merge_prompt_path.relative_to(self.repo_root)),
            workflow_status=status,
            future_branch_report_ref=(team_plan.get("future_exploration") or {}).get("branch_report_ref"),
        )
        return record

    def load_dispatch_context(self, *, task_id: str) -> dict[str, Any]:
        task_root = self.registry.task_root(task_id)
        human_record = load_json(task_root / "HUMAN_DECISION_RECORD.json")
        recommendations_path = task_root / "TEAM_DISPATCH_RECOMMENDATIONS.json"
        recommendations = load_json(recommendations_path) if recommendations_path.exists() else None
        latest_workflow = self.context_store.load_latest(task_id) if self.context_store else None
        workflow_id = (latest_workflow or {}).get("workflow_id") or "unknown"
        return {
            "human_record": human_record,
            "recommendations": recommendations,
            "workflow_id": workflow_id,
            "latest_workflow": latest_workflow,
        }

    def _child_roles_for_spawn(
        self,
        *,
        task_id: str,
        spawn_candidate: dict[str, Any],
        contradiction_count: int,
    ) -> list[dict[str, Any]]:
        domain = spawn_candidate["target_domain"]
        roles = [
            ("prior_art_researcher", f"Identify the closest prior art and novelty deltas for {domain}."),
            ("landscape_analyst", f"Map the current technical and commercial landscape for {domain}."),
            ("science_advisor", f"Assess soundness, feasibility, and empirical risk for {domain}."),
        ]
        lowered = domain.lower()
        if "cross-domain" in lowered or "analogy" in lowered:
            roles.append(("domain_translator", f"Translate adjacent-domain patterns into the {domain} problem space."))
        if contradiction_count >= 4:
            roles.append(("adversarial_analyst", f"Stress-test the strongest failure modes for {domain} before promotion."))
        children = []
        dispatch_slug = self._slug(spawn_candidate["spawn_id"])
        for role, objective in roles[:4]:
            route = self.provider_runtime.resolve_model_route("codex", role)
            children.append(
                {
                    "role": role,
                    "tier": route["tier"],
                    "model": route["model"],
                    "reasoning_effort": route["reasoning_effort"],
                    "objective": objective,
                    "permission": "read_only",
                    "safe_zone_paths": [],
                    "expected_artifact": f"child_results/{dispatch_slug}_{role}.json",
                }
            )
        return children

    def _child_roles_for_stage_team(self, *, task_id: str, stage: str, task_class: str) -> list[dict[str, Any]]:
        children = []
        for role in stage_team_roles_for(task_class, stage):
            route = self.provider_runtime.resolve_model_route("codex", role)
            children.append(
                {
                    "role": role,
                    "tier": route["tier"],
                    "model": route["model"],
                    "reasoning_effort": route["reasoning_effort"],
                    "objective": f"Execute the bounded {stage.lower()} stage viewpoint as the Atrahasis {role}.",
                    "permission": "read_only",
                    "safe_zone_paths": [],
                    "expected_artifact": f"child_results/{self._slug(stage)}_{role}.json",
                }
            )
        return children

    def _memory_reuse_available(self, *, redesign_memory: dict[str, Any], task_class: str, stage: str) -> bool:
        if task_class not in {"ANALYSIS", "GOVERNANCE", "FULL_PIPELINE", "DIRECT_SPEC"}:
            return False
        if stage not in {"IDEATION", "RESEARCH", "FEASIBILITY", "DESIGN", "SPECIFICATION"}:
            return False
        signals = dict(redesign_memory.get("policy_signals") or {})
        if signals.get("history_available"):
            return True
        if redesign_memory.get("current_entry") or redesign_memory.get("related_entry_count", 0):
            return True
        return False

    def _memory_reuse_advisory_child(
        self,
        *,
        stage: str,
        redesign_memory: dict[str, Any],
        mode: str,
    ) -> dict[str, Any]:
        route = self.provider_runtime.resolve_model_route("codex", "memory_reuse_analyst")
        current_entry = dict(redesign_memory.get("current_entry") or {})
        related_entries = list(redesign_memory.get("related_entries", []))
        example_refs = [str(item.get("task_id")) for item in related_entries[:3] if item.get("task_id")]
        reference_text = ", ".join(example_refs) if example_refs else "available redesign history"
        current_text = str(current_entry.get("task_id") or "the current task")
        objective = (
            f"Review persisted redesign memory for {current_text} and related tasks ({reference_text}). "
            f"Return 2-5 advisory considerations for the {stage.lower()} stage: reusable mechanisms worth testing, "
            "prior failure conditions to avoid, and partially successful ideas that may be worth hybridizing. "
            "Offer considerations only; do not force or prescribe the final decision."
        )
        if mode == "future_branch_swarm":
            objective = (
                f"Review persisted redesign memory before the parent reconciles the {stage.lower()} improvement lanes. "
                f"Use {reference_text} to surface 2-5 advisory considerations: reusable fragments, prior failure conditions, "
                "and hybrid opportunities. Offer considerations only; do not force a winner."
            )
        return {
            "role": "memory_reuse_analyst",
            "tier": route["tier"],
            "model": route["model"],
            "reasoning_effort": route["reasoning_effort"],
            "objective": objective,
            "permission": "read_only",
            "safe_zone_paths": [],
            "expected_artifact": f"child_results/{self._slug(stage)}_memory_reuse_analyst.json",
        }

    def _prepend_memory_reuse_advisor(
        self,
        *,
        child_roles: list[dict[str, Any]],
        task_class: str,
        stage: str,
        redesign_memory: dict[str, Any],
        mode: str,
    ) -> list[dict[str, Any]]:
        if any(str(item.get("role")) == "memory_reuse_analyst" for item in child_roles):
            return child_roles
        if not self._memory_reuse_available(redesign_memory=redesign_memory, task_class=task_class, stage=stage):
            return child_roles
        advisor = self._memory_reuse_advisory_child(
            stage=stage,
            redesign_memory=redesign_memory,
            mode=mode,
        )
        return [advisor, *child_roles]

    def _child_roles_for_future_branches(
        self,
        *,
        task_id: str,
        branches: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        children = []
        for branch in branches:
            role = str(branch["parent_role"])
            route = self.provider_runtime.resolve_model_route("codex", role)
            branch_slug = self._slug(branch["branch_id"])
            children.append(
                {
                    "role": role,
                    "tier": route["tier"],
                    "model": route["model"],
                    "reasoning_effort": route["reasoning_effort"],
                    "objective": branch["objective"],
                    "permission": "read_only",
                    "safe_zone_paths": [],
                    "expected_artifact": f"future_branches/{branch_slug}.json",
                    "branch_id": branch["branch_id"],
                    "branch_label": branch["branch_label"],
                    "parent_role": branch["parent_role"],
                    "branch_kind": branch["branch_kind"],
                    "lane_id": branch.get("lane_id"),
                    "lane_label": branch.get("lane_label"),
                    "lane_strategy": branch.get("lane_strategy"),
                }
            )
        return children

    def _select_candidate(
        self,
        *,
        task_id: str,
        recommendations: dict[str, Any],
        action_label: str,
        instruction: str,
    ) -> dict[str, Any]:
        for item in recommendations.get("dispatch_candidates", []):
            if item["action_label"] == action_label and item["instruction"] == instruction:
                return item
        candidate = self._build_policy_candidate(task_id=task_id, action_label=action_label, instruction=instruction)
        if candidate is not None:
            return candidate
        raise ValueError(f"No dispatch candidate found for {action_label}:{instruction}")

    def _build_policy_candidate(
        self,
        *,
        task_id: str,
        action_label: str,
        instruction: str,
    ) -> dict[str, Any] | None:
        policy_path = self.workflow_policy_root / task_id / "latest.json"
        if not policy_path.exists():
            return None
        policy_state = load_json(policy_path)
        task_profile = policy_state.get("task_profile") or {}
        task_class = str(task_profile.get("task_class") or "ANALYSIS")
        redesign_memory = dict(policy_state.get("redesign_memory") or {})
        policy_dispatch = (policy_state.get("dispatch") or {}).get("primary") or {}
        parent_route = self.provider_runtime.resolve_model_route("codex", "director")
        if action_label == "stage_team" and instruction.startswith("stage:"):
            stage = instruction.split(":", 1)[1].strip().upper()
            child_roles = self._prepend_memory_reuse_advisor(
                child_roles=self._child_roles_for_stage_team(task_id=task_id, stage=stage, task_class=task_class),
                task_class=task_class,
                stage=stage,
                redesign_memory=redesign_memory,
                mode="stage_team",
            )
            return {
                "action_label": action_label,
                "instruction": instruction,
                "spawn_id": instruction,
                "program_title": f"{stage.title()} Stage Team",
                "target_domain": stage.lower(),
                "program_goal": f"Run the bounded {stage.lower()} stage team and merge in the parent session.",
                "priority_score": None,
                "approval_status": "POLICY_READY",
                "dispatch_readiness": "READY",
                "team_mode": "STAGE_TEAM",
                "parent_role": "director",
                "parent_model": parent_route["model"],
                "merge_owner": "parent",
                "context_refs": self._policy_context_refs(task_id=task_id),
                "child_roles": child_roles,
                "notes": [
                    "Policy-driven stage team generated from the workflow policy engine.",
                    "Children are read-only by default and the parent owns merge and HITL.",
                ],
            }
        if action_label == "explore_futures" and instruction.startswith("future_swarm:"):
            stage = instruction.split(":", 1)[1].strip().upper()
            future_policy = dict(policy_dispatch.get("future_exploration") or {})
            if not future_policy:
                generated = future_exploration_for(task_class, stage)
                future_policy = dict(generated or {})
            if not future_policy:
                return None
            future_policy["current_stage"] = stage
            future_policy.setdefault(
                "improvement_trigger_policy",
                improvement_trigger_policy_for(task_class, stage, human_decision_record=None),
            )
            branches = []
            for item in future_policy.get("branches", []):
                branch = dict(item)
                branch["expected_artifact"] = f"docs/task_workspaces/{task_id}/future_branches/{self._slug(branch['branch_id'])}.json"
                branches.append(branch)
            future_policy["branches"] = branches
            child_roles = self._prepend_memory_reuse_advisor(
                child_roles=self._child_roles_for_future_branches(task_id=task_id, branches=branches),
                task_class=task_class,
                stage=stage,
                redesign_memory=redesign_memory,
                mode="future_branch_swarm",
            )
            return {
                "action_label": action_label,
                "instruction": instruction,
                "spawn_id": instruction,
                "program_title": future_policy.get("program_title", f"{stage.title()} Future Exploration"),
                "target_domain": stage.lower(),
                "program_goal": future_policy.get("program_goal", f"Explore multiple competing {stage.lower()} futures before parent convergence."),
                "priority_score": None,
                "approval_status": "POLICY_READY",
                "dispatch_readiness": "READY",
                "team_mode": future_policy.get("team_mode", "FUTURE_BRANCH_SWARM"),
                "parent_role": "director",
                "parent_model": parent_route["model"],
                "merge_owner": "parent",
                "context_refs": self._policy_context_refs(task_id=task_id),
                "future_exploration": future_policy,
                "child_roles": child_roles,
                "notes": [
                    "Policy-driven task-improvement lanes generated from the workflow policy engine.",
                    "Future branches are typed future-improvement lanes that the parent reconciles back into the live task.",
                ],
            }
        return None

    def _policy_context_refs(self, *, task_id: str) -> list[str]:
        refs = [
            "docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v5.md",
            "docs/platform_overlays/codex/RUNTIME.md",
            "docs/platform_overlays/codex/TEAM_FORMATION.md",
            f"docs/task_workspaces/{task_id}/WORKFLOW_RUN_RECORD.json",
            f"docs/task_workspaces/{task_id}/HUMAN_DECISION_RECORD.json",
            f"runtime/state/workflow_policy/{task_id}/latest.json",
        ]
        redesign_path = self.repo_root / "runtime" / "state" / "redesign_memory" / "tasks" / task_id / "latest.json"
        if redesign_path.exists():
            refs.append(f"runtime/state/redesign_memory/tasks/{task_id}/latest.json")
        return refs

    def _resolve_parent_session(
        self,
        *,
        provider: str,
        task_id: str,
        agent_name: str | None,
        session_id: str | None,
    ) -> dict[str, str]:
        provider_key = provider.strip().lower()
        if session_id:
            return {
                "provider": provider_key,
                "agent_name": agent_name or "parent",
                "session_id": session_id,
            }
        sessions = self.provider_runtime.list_active_sessions()
        for item in sessions:
            if item.get("provider") != provider_key:
                continue
            if agent_name and item.get("agent_name") != agent_name:
                continue
            if item.get("current_task") == task_id:
                return {
                    "provider": provider_key,
                    "agent_name": item.get("agent_name", agent_name or "parent"),
                    "session_id": item.get("session_id", "not_exposed"),
                }
        return {
            "provider": provider_key,
            "agent_name": agent_name or "not_exposed",
            "session_id": session_id or "not_exposed",
        }

    def _run_child(
        self,
        *,
        team_plan: dict[str, Any],
        child: dict[str, Any],
        parent_agent_name: str,
        parent_session_id: str | None,
    ) -> dict[str, Any]:
        dispatch_dir = ensure_dir(self.dispatch_root / team_plan["task_id"] / team_plan["dispatch_id"])
        output_stem = str(child.get("node_id") or child["role"]).replace(".", "_")
        output_path = dispatch_dir / f"{output_stem}_last_message.json"
        stdout_path = dispatch_dir / f"{output_stem}.stdout.jsonl"
        stderr_path = dispatch_dir / f"{output_stem}.stderr.log"
        before_files = set(self._session_files())
        prompt = self._render_child_prompt(team_plan=team_plan, child=child)
        command = [
            "codex",
            "exec",
            "-C",
            str(self.repo_root),
            "-m",
            child["model"],
            "-s",
            "read-only",
            "--color",
            "never",
            "--json",
            "--output-schema",
            str(self.child_schema_path),
            "-o",
            str(output_path),
            prompt,
        ]
        completed = subprocess.run(
            command,
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        session_meta = self._detect_new_session(before_files=before_files)
        result_payload = self._coerce_child_result(
            task_id=team_plan["task_id"],
            child=child,
            output_path=output_path,
            return_code=completed.returncode,
            stderr_text=completed.stderr,
            session_meta=session_meta,
            parent_agent_name=parent_agent_name,
            parent_session_id=parent_session_id,
        )
        artifact_path = self.registry.write_json_artifact(
            team_plan["task_id"],
            child["expected_artifact"],
            result_payload,
            schema_name="child_agent_result",
        )
        return {
            "node_id": child.get("node_id"),
            "parent_node_id": child.get("parent_node_id"),
            "child_id": child["child_id"],
            "role": child["role"],
            "role_label": child.get("role_label"),
            "status": "COMPLETED" if completed.returncode == 0 else "FAILED",
            "model": child["model"],
            "reasoning_effort": child.get("reasoning_effort"),
            "permission": child["permission"],
            "branch_id": child.get("branch_id"),
            "branch_label": child.get("branch_label"),
            "parent_role": child.get("parent_role"),
            "branch_kind": child.get("branch_kind"),
            "lane_id": child.get("lane_id"),
            "lane_label": child.get("lane_label"),
            "lane_strategy": child.get("lane_strategy"),
            "audit_domain": child.get("audit_domain"),
            "output_artifact": str(artifact_path.relative_to(self.repo_root)),
            "session_id": session_meta.get("session_id"),
            "session_log": session_meta.get("session_log"),
            "return_code": completed.returncode,
            "stdout_log": str(stdout_path),
            "stderr_log": str(stderr_path),
        }

    def _coerce_child_result(
        self,
        *,
        task_id: str,
        child: dict[str, Any],
        output_path: Path,
        return_code: int,
        stderr_text: str,
        session_meta: dict[str, str | None],
        parent_agent_name: str,
        parent_session_id: str | None,
    ) -> dict[str, Any]:
        payload: dict[str, Any]
        try:
            payload = json.loads(output_path.read_text(encoding="utf-8")) if output_path.exists() else {}
        except json.JSONDecodeError:
            payload = {}
        evidence = payload.get("evidence")
        if not isinstance(evidence, list):
            evidence = []
        normalized = {
            "type": "CHILD_AGENT_RESULT",
            "node_id": child.get("node_id"),
            "parent_node_id": child.get("parent_node_id"),
            "task_id": task_id,
            "role": child["role"],
            "role_label": child.get("role_label"),
            "objective": child["objective"],
            "status": "COMPLETED" if return_code == 0 else "FAILED",
            "session_identity": {
                "agent_name": child["agent_name"],
                "session_id": session_meta.get("session_id"),
                "provider": "codex",
                "role": child["role"],
                "node_id": child.get("node_id"),
            },
            "model_audit": build_model_audit(
                requested_model=child["model"],
                requested_reasoning_effort=child.get("reasoning_effort"),
                observed_runtime_model=None,
                observed_model_auditability="runtime_not_exposed",
                routing_basis="Dispatcher child execution result recorded without direct runtime model exposure.",
            ),
            "artifact_provenance": build_artifact_provenance(
                writer_mode="parent_proxy",
                writer_agent_name=parent_agent_name,
                writer_session_id=parent_session_id,
                writer_node_id="mst",
                owner_node_id=child.get("node_id"),
                notes=[
                    "Parent dispatcher persisted this artifact after receiving the child output.",
                ],
            ),
            "verdict": payload.get("verdict")
            or ("Child Codex session completed." if return_code == 0 else "Child Codex session failed."),
            "evidence": evidence[:8],
            "recommended_next_action": payload.get("recommended_next_action")
            or ("Merge the child evidence into the parent synthesis." if return_code == 0 else "Inspect stderr and rerun or adjust the objective."),
        }
        if child.get("branch_id"):
            normalized["branch_id"] = child.get("branch_id")
            normalized["branch_label"] = child.get("branch_label")
            normalized["parent_role"] = child.get("parent_role")
            normalized["branch_kind"] = child.get("branch_kind")
            normalized["lane_id"] = child.get("lane_id")
            normalized["lane_label"] = child.get("lane_label")
            normalized["lane_strategy"] = child.get("lane_strategy")
        elif child.get("lane_id"):
            normalized["lane_id"] = child.get("lane_id")
            normalized["lane_label"] = child.get("lane_label")
            normalized["lane_strategy"] = child.get("lane_strategy")
        if child.get("audit_domain"):
            normalized["audit_domain"] = child.get("audit_domain")
        if return_code != 0 and stderr_text.strip():
            normalized["evidence"].append(
                {
                    "path": "runtime://codex_dispatch/stderr",
                    "note": stderr_text.strip()[:400],
                }
            )
        return normalized

    def _model_audit(
        self,
        *,
        policy_target: str | None,
        actual_runtime_model: str | None,
        reasoning_effort: str | None,
        auditability: str,
        routing_basis: str,
    ) -> dict[str, Any]:
        return build_model_audit(
            requested_model=policy_target,
            requested_reasoning_effort=reasoning_effort,
            observed_runtime_model=actual_runtime_model,
            observed_model_auditability=auditability,
            routing_basis=routing_basis,
        )

    def _artifact_provenance(
        self,
        *,
        writer_mode: str,
        writer_agent_name: str | None,
        writer_session_id: str | None,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        return build_artifact_provenance(
            writer_mode=writer_mode,
            writer_agent_name=writer_agent_name,
            writer_session_id=writer_session_id,
            writer_node_id=None,
            owner_node_id=None,
            notes=notes,
        )

    def _render_child_prompt(self, *, team_plan: dict[str, Any], child: dict[str, Any]) -> str:
        context_lines = "\n".join(f"- {path}" for path in team_plan.get("context_refs", []))
        future_branch_line = ""
        if child.get("branch_id"):
            future_branch_line = (
                f"Future branch: {child.get('branch_label')} "
                f"({child.get('parent_role')} / {child.get('branch_kind')}).\n"
            )
        advisory_line = ""
        if child.get("role") == "memory_reuse_analyst":
            advisory_line = (
                "Your output is advisory only. Surface considerations and cautions; do not claim that the parent must adopt any prior idea.\n"
            )
        elif any("memory_reuse_analyst" in str(path) for path in team_plan.get("context_refs", [])):
            advisory_line = (
                "If memory-reuse considerations are present in the context files, treat them as advisory inputs rather than binding instructions.\n"
            )
        return (
            f"You are acting as the Atrahasis `{child.get('role_label') or child['role']}` child session for task {team_plan['task_id']}.\n\n"
            "Operate in read-only mode.\n"
            "Do not edit files.\n"
            "Do not register yourself.\n"
            "Do not claim tasks.\n"
            "Do not modify AGENT_STATE, TODO, DECISIONS, dashboards, logs, or handoffs.\n"
            "Do not cross HITL gates.\n"
            "Stay tightly scoped to the assigned objective.\n\n"
            f"Node id: {child.get('node_id') or 'unknown'}.\n"
            f"Parent dispatch target: {team_plan['selection']['program_title']} ({team_plan['selection']['target_domain']}).\n"
            f"{future_branch_line}"
            f"{advisory_line}"
            f"Objective: {child['objective']}\n\n"
            "Read these local files first:\n"
            f"{context_lines}\n\n"
            "Return a JSON object only. Keep evidence concise and cite repo-relative paths in the evidence notes."
        )

    def _render_merge_prompt(self, *, team_plan: dict[str, Any], child_runs: list[dict[str, Any]]) -> str:
        lines = [
            f"# Parent Merge Prompt - {team_plan['task_id']}",
            "",
            "Use this in the parent Codex session after child dispatch completes.",
            "",
            "Read and merge these child result artifacts:",
        ]
        for item in child_runs:
            lines.append(f"- `{item['output_artifact']}`")
        lines.extend(
            [
                "",
                "Then produce a parent synthesis that:",
                "- reconciles disagreements explicitly",
                "- identifies the strongest evidence and unresolved risks",
                "- recommends whether the spawned program should continue, pause, or escalate",
                "- does not claim a HITL gate has been satisfied unless the user explicitly approved it",
            ]
        )
        if team_plan.get("future_exploration"):
            lines.extend(
                [
                    "",
                    "Task-improvement lane requirement:",
                    "- generate `FUTURE_CONVERGENCE_REPORT.json` by comparing the typed future-branch lanes before choosing one parent direction",
                    "- generate `TASK_IMPROVEMENT_REPORT.json` if the improvement trigger policy is enabled, and decide whether to reject, adopt, hybridize, or escalate the improvement",
                ]
            )
        return "\n".join(lines)

    def _update_dispatch_state(
        self,
        *,
        task_id: str,
        workflow_id: str,
        action_label: str,
        instruction: str,
        team_plan_ref: str,
        workflow_status: str,
        dispatch_record_ref: str | None = None,
        merge_prompt_ref: str | None = None,
        future_branch_report_ref: str | None = None,
    ) -> None:
        task_root = self.registry.task_root(task_id)
        human_record_path = task_root / "HUMAN_DECISION_RECORD.json"
        if human_record_path.exists():
            human_record = load_json(human_record_path)
            human_record["operator_decision"] = f"{action_label}:{instruction}"
            human_record["workflow_status"] = workflow_status
            human_record["team_plan_ref"] = team_plan_ref
            if dispatch_record_ref:
                human_record["dispatch_record_ref"] = dispatch_record_ref
            if merge_prompt_ref:
                human_record["merge_prompt_ref"] = merge_prompt_ref
            if future_branch_report_ref:
                human_record["future_branch_report_ref"] = future_branch_report_ref
            self.registry.write_json_artifact(task_id, "HUMAN_DECISION_RECORD.json", human_record, schema_name="human_decision_record")
        workflow_record_path = task_root / "WORKFLOW_RUN_RECORD.json"
        if workflow_record_path.exists():
            workflow_record = load_json(workflow_record_path)
            workflow_record["status"] = workflow_status
            workflow_record["recommended_next_actions"] = [
                "Review TEAM_PLAN.yaml and child result artifacts",
                "Merge the child findings in the parent Codex session",
                "Update shared state only after the parent synthesis is complete",
            ]
            workflow_record["artifacts"]["team_plan"] = team_plan_ref
            if dispatch_record_ref:
                workflow_record["artifacts"]["team_dispatch_record"] = dispatch_record_ref
            if merge_prompt_ref:
                workflow_record["artifacts"]["parent_merge_prompt"] = merge_prompt_ref
            if future_branch_report_ref:
                workflow_record["artifacts"]["future_branch_report"] = future_branch_report_ref
            self.registry.write_json_artifact(task_id, "WORKFLOW_RUN_RECORD.json", workflow_record, schema_name="workflow_run_record")
        if self.context_store is not None and workflow_id != "unknown":
            self.context_store.update_status(
                task_id=task_id,
                workflow_id=workflow_id,
                status=workflow_status,
                artifact_updates={
                    "team_plan": team_plan_ref,
                    "team_dispatch_record": dispatch_record_ref,
                    "parent_merge_prompt": merge_prompt_ref,
                    "future_branch_report": future_branch_report_ref,
                },
            )

    def _detect_new_session(self, *, before_files: set[Path]) -> dict[str, str | None]:
        after_files = self._session_files()
        candidates = [path for path in after_files if path not in before_files]
        if not candidates:
            return {"session_id": None, "session_log": None}
        latest = max(candidates, key=lambda path: path.stat().st_mtime)
        session_id = None
        try:
            first_line = latest.read_text(encoding="utf-8").splitlines()[0]
            payload = json.loads(first_line)
            session_id = payload.get("payload", {}).get("id")
        except Exception:
            session_id = None
        return {
            "session_id": session_id,
            "session_log": str(latest),
        }

    def _session_files(self) -> set[Path]:
        if not self.session_root.exists():
            return set()
        return {path for path in self.session_root.rglob("*.jsonl")}

    def _slug(self, value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")
