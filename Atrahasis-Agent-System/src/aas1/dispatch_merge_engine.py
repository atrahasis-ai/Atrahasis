from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from aas1.aas5_ideation import (
    ADVERSARIAL_INTEGRITY_REVIEW,
    AUTHORITY_COVERAGE_AUDIT,
    AAS5_DOCTRINE_VERSION,
    EXECUTION_PARALLELISM_RECORD,
    RUNTIME_AUDIT_RECORD,
    SWARM_COMPLIANCE_AUDIT,
    SWARM_TOPOLOGY_GRAPH,
    lane_report_path,
)
from aas1.artifact_registry import ArtifactRegistry
from aas1.common import load_json, load_yaml, utc_now
from aas1.swarm_validation import validate_swarm_execution_task


class DispatchMergeEngine:
    """Builds durable parent merge packages from completed child dispatch runs."""

    def __init__(self, repo_root: Path, *, artifact_registry: ArtifactRegistry) -> None:
        self.repo_root = repo_root
        self.registry = artifact_registry

    def build_for_task(self, *, task_id: str) -> dict[str, Any] | None:
        task_root = self.registry.task_root(task_id)
        dispatch_path = task_root / "TEAM_DISPATCH_RECORD.json"
        if not dispatch_path.exists():
            return None
        dispatch_record = load_json(dispatch_path)
        if dispatch_record.get("status") not in {
            "TEAM_EXECUTION_COMPLETED",
            "TEAM_EXECUTION_PARTIAL_FAILURE",
            "TEAM_EXECUTION_FAILED",
        }:
            return None
        team_plan = load_yaml(task_root / "TEAM_PLAN.yaml") if (task_root / "TEAM_PLAN.yaml").exists() else {}
        if str((team_plan or {}).get("doctrine_version") or "") == AAS5_DOCTRINE_VERSION:
            return self._build_aas5_for_task(
                task_id=task_id,
                task_root=task_root,
                dispatch_record=dispatch_record,
                team_plan=team_plan,
            )
        future_branch_report = load_json(task_root / "FUTURE_BRANCH_REPORT.json") if (task_root / "FUTURE_BRANCH_REPORT.json").exists() else {}
        swarm_execution_record = load_json(task_root / "SWARM_EXECUTION_RECORD.json") if (task_root / "SWARM_EXECUTION_RECORD.json").exists() else {}
        future_exploration = (team_plan or {}).get("future_exploration") or {}
        stage = str(future_exploration.get("current_stage") or (future_branch_report or {}).get("current_stage") or "IDEATION")
        children = []
        verdicts = Counter()
        actions = Counter()
        statuses = Counter()
        for item in dispatch_record.get("children", []):
            artifact_path = self.repo_root / str(item.get("output_artifact", ""))
            child_payload = load_json(artifact_path) if artifact_path.exists() else {}
            verdict = str(child_payload.get("verdict", "")).strip()
            next_action = str(child_payload.get("recommended_next_action", "")).strip()
            status = str(item.get("status", child_payload.get("status", ""))).strip()
            session_identity = child_payload.get("session_identity") or {}
            if verdict:
                verdicts[verdict] += 1
            if next_action:
                actions[next_action] += 1
            if status:
                statuses[status] += 1
            children.append(
                {
                    "child_id": item.get("child_id"),
                    "role": item.get("role"),
                    "status": status,
                    "branch_id": child_payload.get("branch_id") or item.get("branch_id"),
                    "branch_label": child_payload.get("branch_label") or item.get("branch_label"),
                    "parent_role": child_payload.get("parent_role") or item.get("parent_role"),
                    "branch_kind": child_payload.get("branch_kind") or item.get("branch_kind"),
                    "lane_id": child_payload.get("lane_id") or item.get("lane_id"),
                    "lane_label": child_payload.get("lane_label") or item.get("lane_label"),
                    "lane_strategy": child_payload.get("lane_strategy") or item.get("lane_strategy"),
                    "verdict": verdict,
                    "recommended_next_action": next_action,
                    "evidence": list(child_payload.get("evidence", []))[:8],
                    "artifact_path": item.get("output_artifact"),
                    "agent_name": session_identity.get("agent_name") or item.get("role"),
                    "session_id": item.get("session_id") or session_identity.get("session_id"),
                    "model_audit": child_payload.get("model_audit") or {},
                    "artifact_provenance": child_payload.get("artifact_provenance") or {},
                }
            )
        branch_completion = self._branch_completion(
            branch_specs=list(future_exploration.get("branches") or []),
            children=children,
        )
        disagreements = []
        if len(verdicts) > 1:
            disagreements.append("Child verdicts diverge and require explicit parent reconciliation.")
        if len(actions) > 1:
            disagreements.append("Child next-action recommendations diverge and require an explicit parent decision.")
        if statuses.get("FAILED"):
            disagreements.append("At least one child run failed and its logs should be inspected before closeout.")
        advisory_considerations = self._advisory_considerations(children)
        merge_package_ref = f"docs/task_workspaces/{task_id}/CHILD_RESULT_MERGE_PACKAGE.json"
        package = {
            "type": "CHILD_RESULT_MERGE_PACKAGE",
            "task_id": task_id,
            "workflow_id": dispatch_record.get("workflow_id"),
            "dispatch_id": dispatch_record.get("dispatch_id"),
            "dispatch_status": dispatch_record.get("status"),
            "generated_at": utc_now(),
            "merge_ready": False,
            "child_results": children,
            "disagreement_signals": disagreements,
            "recommended_parent_actions": self._recommended_actions(actions=actions, statuses=statuses),
            "synthesis_outline": [
                "Summarize the strongest convergent evidence across child roles.",
                "Name the highest-risk disagreements or missing evidence explicitly.",
                "Choose the next parent action and justify it against the child record.",
                "Do not claim HITL completion unless the operator has explicitly approved it.",
            ],
            "source_refs": {
                "team_dispatch_record": f"docs/task_workspaces/{task_id}/TEAM_DISPATCH_RECORD.json",
                "team_plan": f"docs/task_workspaces/{task_id}/TEAM_PLAN.yaml" if team_plan else None,
                "future_branch_report": f"docs/task_workspaces/{task_id}/FUTURE_BRANCH_REPORT.json" if future_branch_report else None,
                "swarm_execution_record": f"docs/task_workspaces/{task_id}/SWARM_EXECUTION_RECORD.json" if swarm_execution_record else None,
            },
            "required_child_ids": branch_completion["required_branch_ids"],
            "completed_child_ids": branch_completion["completed_branch_ids"],
            "missing_child_ids": branch_completion["missing_branch_ids"],
            "validation_status": "PENDING",
        }
        if advisory_considerations:
            package["advisory_considerations"] = advisory_considerations
        self.registry.write_json_artifact(
            task_id,
            "CHILD_RESULT_MERGE_PACKAGE.json",
            package,
            schema_name="child_result_merge_package",
        )
        validation_failures: list[str] = []
        recommendation_authorized = False
        if stage == "IDEATION" and future_exploration.get("enabled"):
            candidate_blockers = self._branch_blocking_reasons(branch_completion=branch_completion)
            candidate_future_branch_report = self._sync_future_branch_report(
                task_id=task_id,
                dispatch_record=dispatch_record,
                future_branch_report=future_branch_report,
                team_plan=team_plan,
                branch_completion=branch_completion,
                recommendation_authorized=not candidate_blockers,
                blocking_gates=[] if not candidate_blockers else candidate_blockers,
            )
            self.registry.write_json_artifact(
                task_id,
                "FUTURE_BRANCH_REPORT.json",
                candidate_future_branch_report,
                schema_name="future_branch_report",
            )
            candidate_swarm_record = self._sync_swarm_execution_record(
                task_id=task_id,
                stage=stage,
                dispatch_record=dispatch_record,
                team_plan=team_plan,
                existing_record=swarm_execution_record,
                children=children,
                merge_package_ref=merge_package_ref,
                recommendation_authorized=not candidate_blockers,
                blocking_reasons=candidate_blockers,
            )
            self.registry.write_json_artifact(
                task_id,
                "SWARM_EXECUTION_RECORD.json",
                candidate_swarm_record,
                schema_name="swarm_execution_record",
            )
            if candidate_blockers:
                validation_failures = list(candidate_blockers)
                future_branch_report = candidate_future_branch_report
                swarm_execution_record = candidate_swarm_record
            else:
                validation_failures = validate_swarm_execution_task(repo_root=self.repo_root, task_id=task_id)
                if validation_failures:
                    future_branch_report = self._sync_future_branch_report(
                        task_id=task_id,
                        dispatch_record=dispatch_record,
                        future_branch_report=candidate_future_branch_report,
                        team_plan=team_plan,
                        branch_completion=branch_completion,
                        recommendation_authorized=False,
                        blocking_gates=validation_failures,
                    )
                    self.registry.write_json_artifact(
                        task_id,
                        "FUTURE_BRANCH_REPORT.json",
                        future_branch_report,
                        schema_name="future_branch_report",
                    )
                    swarm_execution_record = self._sync_swarm_execution_record(
                        task_id=task_id,
                        stage=stage,
                        dispatch_record=dispatch_record,
                        team_plan=team_plan,
                        existing_record=candidate_swarm_record,
                        children=children,
                        merge_package_ref=merge_package_ref,
                        recommendation_authorized=False,
                        blocking_reasons=validation_failures,
                    )
                    self.registry.write_json_artifact(
                        task_id,
                        "SWARM_EXECUTION_RECORD.json",
                        swarm_execution_record,
                        schema_name="swarm_execution_record",
                    )
                else:
                    recommendation_authorized = True
                    future_branch_report = candidate_future_branch_report
                    swarm_execution_record = candidate_swarm_record

        package["merge_ready"] = recommendation_authorized if stage == "IDEATION" else bool(children)
        package["validation_status"] = (
            "PASSED" if recommendation_authorized else ("FAILED" if validation_failures else "NOT_REQUIRED")
        )
        package["validation_failures"] = list(validation_failures)
        self.registry.write_json_artifact(
            task_id,
            "CHILD_RESULT_MERGE_PACKAGE.json",
            package,
            schema_name="child_result_merge_package",
        )

        result = {
            "merge_package": package,
            "merge_package_ref": merge_package_ref,
        }
        future_convergence = self._build_future_convergence_report(
            task_id=task_id,
            dispatch_record=dispatch_record,
            team_plan=team_plan,
            future_branch_report=future_branch_report,
            children=children,
            disagreements=disagreements,
            actions=actions,
        )
        if future_convergence is not None:
            result["future_convergence_report"] = future_convergence
            result["future_convergence_report_ref"] = f"docs/task_workspaces/{task_id}/FUTURE_CONVERGENCE_REPORT.json"
        task_improvement = self._build_task_improvement_report(
            task_id=task_id,
            dispatch_record=dispatch_record,
            team_plan=team_plan,
            future_convergence=future_convergence,
            children=children,
        )
        if task_improvement is not None:
            result["task_improvement_report"] = task_improvement
            result["task_improvement_report_ref"] = f"docs/task_workspaces/{task_id}/TASK_IMPROVEMENT_REPORT.json"
        radical_report = self._build_radical_redesign_report(
            task_id=task_id,
            dispatch_record=dispatch_record,
            team_plan=team_plan,
            future_convergence=future_convergence,
            children=children,
        )
        if radical_report is not None:
            result["radical_redesign_report"] = radical_report
            result["radical_redesign_report_ref"] = f"docs/task_workspaces/{task_id}/RADICAL_REDESIGN_REPORT.json"
        self.registry.write_markdown_artifact(
            task_id,
            "PARENT_SYNTHESIS_DRAFT.md",
            self._render_parent_draft(task_id=task_id, team_plan=team_plan, package=package),
        )
        result["draft_ref"] = f"docs/task_workspaces/{task_id}/PARENT_SYNTHESIS_DRAFT.md"
        if stage == "IDEATION" and future_exploration.get("enabled"):
            result["swarm_execution_record_ref"] = f"docs/task_workspaces/{task_id}/SWARM_EXECUTION_RECORD.json"
            result["future_branch_report_ref"] = f"docs/task_workspaces/{task_id}/FUTURE_BRANCH_REPORT.json"
            result["swarm_validation_passed"] = recommendation_authorized
            result["swarm_validation_failures"] = list(validation_failures)
        return result

    def _build_aas5_for_task(
        self,
        *,
        task_id: str,
        task_root: Path,
        dispatch_record: dict[str, Any],
        team_plan: dict[str, Any],
    ) -> dict[str, Any]:
        participants: list[dict[str, Any]] = []
        verdicts = Counter()
        actions = Counter()
        statuses = Counter()
        for item in dispatch_record.get("children", []):
            artifact_path = self.repo_root / str(item.get("output_artifact", ""))
            child_payload = load_json(artifact_path) if artifact_path.exists() else {}
            verdict = str(child_payload.get("verdict", "")).strip()
            next_action = str(child_payload.get("recommended_next_action", "")).strip()
            status = str(item.get("status", child_payload.get("status", ""))).strip()
            session_identity = child_payload.get("session_identity") or {}
            if verdict:
                verdicts[verdict] += 1
            if next_action:
                actions[next_action] += 1
            if status:
                statuses[status] += 1
            participants.append(
                {
                    "node_id": child_payload.get("node_id") or item.get("node_id"),
                    "parent_node_id": child_payload.get("parent_node_id") or item.get("parent_node_id"),
                    "role": child_payload.get("role") or item.get("role"),
                    "role_label": child_payload.get("role_label") or item.get("role_label"),
                    "status": status,
                    "branch_id": child_payload.get("branch_id") or item.get("branch_id"),
                    "branch_label": child_payload.get("branch_label") or item.get("branch_label"),
                    "parent_role": child_payload.get("parent_role") or item.get("parent_role"),
                    "branch_kind": child_payload.get("branch_kind") or item.get("branch_kind"),
                    "lane_id": child_payload.get("lane_id") or item.get("lane_id"),
                    "lane_label": child_payload.get("lane_label") or item.get("lane_label"),
                    "lane_strategy": child_payload.get("lane_strategy") or item.get("lane_strategy"),
                    "audit_domain": child_payload.get("audit_domain") or item.get("audit_domain"),
                    "verdict": verdict,
                    "recommended_next_action": next_action,
                    "evidence": list(child_payload.get("evidence", []))[:8],
                    "artifact_path": item.get("output_artifact"),
                    "agent_name": session_identity.get("agent_name") or item.get("role"),
                    "session_id": item.get("session_id") or session_identity.get("session_id"),
                    "model_audit": child_payload.get("model_audit") or {},
                    "artifact_provenance": child_payload.get("artifact_provenance") or {},
                }
            )

        participant_index = {
            str(item.get("node_id") or ""): item for item in participants if str(item.get("node_id") or "")
        }
        lane_status_map = self._sync_aas5_lane_reports(task_id=task_id, participant_index=participant_index)
        self._sync_aas5_audits(task_id=task_id, participant_index=participant_index)

        topology_graph = load_json(task_root / SWARM_TOPOLOGY_GRAPH) if (task_root / SWARM_TOPOLOGY_GRAPH).exists() else {}
        if topology_graph:
            topology_graph["realized_node_count"] = 1 + len(participants)
            topology_graph["updated_at"] = utc_now()
            self.registry.write_json_artifact(task_id, SWARM_TOPOLOGY_GRAPH, topology_graph, schema_name="swarm_topology_graph")

        parallelism = load_json(task_root / EXECUTION_PARALLELISM_RECORD) if (task_root / EXECUTION_PARALLELISM_RECORD).exists() else {}
        parallelism.update(
            {
                "updated_at": utc_now(),
                "total_agents_spawned": 1 + len(participants),
                "total_children_spawned": len(participants),
                "total_grandchildren_spawned": sum(
                    1 for item in participants if str(item.get("parent_node_id") or "").startswith("mgr.")
                ),
                "actual_parallel_agent_count": min(
                    int(((team_plan.get("spawn_policy") or {}).get("max_live_children") or 0)) + 1,
                    1 + len(participants),
                ),
                "execution_parallelism_mode": "degraded_batched",
            }
        )
        self.registry.write_json_artifact(
            task_id,
            EXECUTION_PARALLELISM_RECORD,
            parallelism,
            schema_name="execution_parallelism_record",
        )

        disagreement_signals = []
        if len(verdicts) > 1:
            disagreement_signals.append("AAS5 participant verdicts diverge and require explicit master reconciliation.")
        if len(actions) > 1:
            disagreement_signals.append("AAS5 participant next-action recommendations diverge and require an explicit master decision.")
        if statuses.get("FAILED"):
            disagreement_signals.append("At least one AAS5 participant run failed and its logs should be inspected before closeout.")

        merge_package = {
            "type": "CHILD_RESULT_MERGE_PACKAGE",
            "doctrine_version": team_plan.get("doctrine_version"),
            "topology_mode": team_plan.get("topology_mode"),
            "task_id": task_id,
            "workflow_id": dispatch_record.get("workflow_id"),
            "run_key": team_plan.get("run_key"),
            "dispatch_id": dispatch_record.get("dispatch_id"),
            "dispatch_status": dispatch_record.get("status"),
            "generated_at": utc_now(),
            "merge_ready": False,
            "child_results": participants,
            "lane_report_refs": {lane_id: f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}" for lane_id in lane_status_map},
            "audit_refs": {
                "compliance": f"docs/task_workspaces/{task_id}/{SWARM_COMPLIANCE_AUDIT}",
                "runtime": f"docs/task_workspaces/{task_id}/{RUNTIME_AUDIT_RECORD}",
                "authority": f"docs/task_workspaces/{task_id}/{AUTHORITY_COVERAGE_AUDIT}",
                "adversarial": f"docs/task_workspaces/{task_id}/{ADVERSARIAL_INTEGRITY_REVIEW}",
            },
            "disagreement_signals": disagreement_signals,
            "recommended_parent_actions": self._recommended_actions(actions=actions, statuses=statuses),
            "synthesis_outline": [
                "Summarize the strongest convergent evidence across AAS5 managers, workers, reporters, and auditors.",
                "Name the highest-risk disagreements or missing evidence explicitly.",
                "Do not authorize recommendation while AAS5 validator failures remain.",
            ],
            "source_refs": {
                "team_dispatch_record": f"docs/task_workspaces/{task_id}/TEAM_DISPATCH_RECORD.json",
                "team_plan": f"docs/task_workspaces/{task_id}/TEAM_PLAN.yaml",
                "future_branch_report": f"docs/task_workspaces/{task_id}/FUTURE_BRANCH_REPORT.json",
                "swarm_execution_record": f"docs/task_workspaces/{task_id}/SWARM_EXECUTION_RECORD.json",
                "swarm_topology_graph": f"docs/task_workspaces/{task_id}/{SWARM_TOPOLOGY_GRAPH}",
                "execution_parallelism_record": f"docs/task_workspaces/{task_id}/{EXECUTION_PARALLELISM_RECORD}",
            },
            "validation_status": "PENDING",
        }
        self.registry.write_json_artifact(
            task_id,
            "CHILD_RESULT_MERGE_PACKAGE.json",
            merge_package,
            schema_name="child_result_merge_package",
        )

        future_branch_report = load_json(task_root / "FUTURE_BRANCH_REPORT.json") if (task_root / "FUTURE_BRANCH_REPORT.json").exists() else {}
        branch_status_map = {
            str(item.get("branch_id") or ""): str(item.get("status") or "")
            for item in participants
            if str(item.get("branch_id") or "")
        }
        future_branch_report.update(
            {
                "updated_at": utc_now(),
                "recommendation_authorized": False,
                "blocking_gates": ["AAS5 validation must pass before recommendation can be authorized."],
                "lane_summaries": [
                    {
                        "lane_id": lane_id,
                        "status": lane_status,
                        "lane_report_ref": f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}",
                    }
                    for lane_id, lane_status in lane_status_map.items()
                ],
                "branches": [
                    {
                        **item,
                        "status": branch_status_map.get(str(item.get("branch_id") or ""), str(item.get("status") or "PLANNED")),
                    }
                    for item in list(future_branch_report.get("branches") or [])
                ],
            }
        )
        self.registry.write_json_artifact(
            task_id,
            "FUTURE_BRANCH_REPORT.json",
            future_branch_report,
            schema_name="future_branch_report",
        )

        swarm_execution = load_json(task_root / "SWARM_EXECUTION_RECORD.json") if (task_root / "SWARM_EXECUTION_RECORD.json").exists() else {}
        completed = len(participants) == 24 and not statuses.get("FAILED") and not statuses.get("PLANNED")
        swarm_execution.update(
            {
                "runtime_capabilities": {
                    "multi_agent_enabled": True,
                    "real_child_sessions_available": True,
                    "child_result_tracking_available": True,
                },
                "execution_mode": "REAL_SWARM" if completed else "BLOCKED",
                "execution_parallelism_mode": "degraded_batched",
                "spawned_children": [
                    {
                        "node_id": item.get("node_id"),
                        "parent_node_id": item.get("parent_node_id"),
                        "role": item.get("role"),
                        "role_label": item.get("role_label"),
                        "branch_id": item.get("branch_id"),
                        "lane_id": item.get("lane_id"),
                        "audit_domain": item.get("audit_domain"),
                        "agent_name": item.get("agent_name"),
                        "execution_type": "REAL_CHILD",
                        "status": item.get("status"),
                        "session_id": item.get("session_id"),
                        "artifact_ref": item.get("artifact_path"),
                        "model_audit": item.get("model_audit"),
                        "artifact_provenance": item.get("artifact_provenance"),
                    }
                    for item in participants
                ],
                "blocking_reason": None if completed else "One or more AAS5 participants are incomplete or failed.",
                "recommendation_authorized": False,
                "satisfied": completed,
            }
        )
        self.registry.write_json_artifact(
            task_id,
            "SWARM_EXECUTION_RECORD.json",
            swarm_execution,
            schema_name="swarm_execution_record",
        )

        validation_failures = validate_swarm_execution_task(repo_root=self.repo_root, task_id=task_id)
        if not validation_failures:
            swarm_execution["recommendation_authorized"] = True
            future_branch_report["recommendation_authorized"] = True
            future_branch_report["blocking_gates"] = []
            self.registry.write_json_artifact(
                task_id,
                "FUTURE_BRANCH_REPORT.json",
                future_branch_report,
                schema_name="future_branch_report",
            )
            self.registry.write_json_artifact(
                task_id,
                "SWARM_EXECUTION_RECORD.json",
                swarm_execution,
                schema_name="swarm_execution_record",
            )
            authorization_failures = validate_swarm_execution_task(repo_root=self.repo_root, task_id=task_id)
            if authorization_failures:
                validation_failures = authorization_failures
                swarm_execution["recommendation_authorized"] = False
                future_branch_report["recommendation_authorized"] = False
                future_branch_report["blocking_gates"] = list(authorization_failures)
                self.registry.write_json_artifact(
                    task_id,
                    "FUTURE_BRANCH_REPORT.json",
                    future_branch_report,
                    schema_name="future_branch_report",
                )
                self.registry.write_json_artifact(
                    task_id,
                    "SWARM_EXECUTION_RECORD.json",
                    swarm_execution,
                    schema_name="swarm_execution_record",
                )
        else:
            future_branch_report["blocking_gates"] = list(validation_failures)
            self.registry.write_json_artifact(
                task_id,
                "FUTURE_BRANCH_REPORT.json",
                future_branch_report,
                schema_name="future_branch_report",
            )

        merge_package["merge_ready"] = not validation_failures
        merge_package["validation_status"] = "PASSED" if not validation_failures else "FAILED"
        merge_package["validation_failures"] = list(validation_failures)
        self.registry.write_json_artifact(
            task_id,
            "CHILD_RESULT_MERGE_PACKAGE.json",
            merge_package,
            schema_name="child_result_merge_package",
        )

        self.registry.write_markdown_artifact(
            task_id,
            "PARENT_SYNTHESIS_DRAFT.md",
            self._render_parent_draft(task_id=task_id, team_plan=team_plan, package=merge_package),
        )
        return {
            "merge_package": merge_package,
            "merge_package_ref": f"docs/task_workspaces/{task_id}/CHILD_RESULT_MERGE_PACKAGE.json",
            "swarm_execution_record_ref": f"docs/task_workspaces/{task_id}/SWARM_EXECUTION_RECORD.json",
            "future_branch_report_ref": f"docs/task_workspaces/{task_id}/FUTURE_BRANCH_REPORT.json",
            "draft_ref": f"docs/task_workspaces/{task_id}/PARENT_SYNTHESIS_DRAFT.md",
        }

    def _sync_aas5_lane_reports(
        self,
        *,
        task_id: str,
        participant_index: dict[str, dict[str, Any]],
    ) -> dict[str, str]:
        lane_status_map: dict[str, str] = {}
        for lane_id in ("alpha", "beta", "gamma", "radical"):
            worker_ids = [f"wrk.{lane_id}.visionary", f"wrk.{lane_id}.systems_thinker", f"wrk.{lane_id}.critic"]
            reporter_id = f"rep.{lane_id}"
            reporter = participant_index.get(reporter_id) or {}
            workers = [participant_index.get(worker_id) or {} for worker_id in worker_ids]
            completed = reporter.get("status") == "COMPLETED" and all(item.get("status") == "COMPLETED" for item in workers)
            status = "COMPLETED" if completed else "PLANNED"
            lane_status_map[lane_id] = status
            report_payload = load_json(self.registry.task_root(task_id) / lane_report_path(lane_id))
            report_payload.update(
                {
                    "updated_at": utc_now(),
                    "status": status,
                    "summary": reporter.get("verdict") or "Pending lane convergence.",
                    "disagreement_signals": [] if completed else ["Lane convergence is incomplete."],
                    "candidate_options": [],
                    "recommendation_authorized": False,
                }
            )
            self.registry.write_json_artifact(
                task_id,
                lane_report_path(lane_id),
                report_payload,
                schema_name="lane_convergence_report",
            )
        return lane_status_map

    def _sync_aas5_audits(
        self,
        *,
        task_id: str,
        participant_index: dict[str, dict[str, Any]],
    ) -> dict[str, str]:
        audit_map = {
            "aud.compliance": SWARM_COMPLIANCE_AUDIT,
            "aud.runtime": RUNTIME_AUDIT_RECORD,
            "aud.authority": AUTHORITY_COVERAGE_AUDIT,
            "aud.adversarial": ADVERSARIAL_INTEGRITY_REVIEW,
        }
        statuses: dict[str, str] = {}
        for node_id, artifact_name in audit_map.items():
            participant = participant_index.get(node_id) or {}
            status = "COMPLETED" if participant.get("status") == "COMPLETED" else "PLANNED"
            statuses[node_id] = status
            payload = load_json(self.registry.task_root(task_id) / artifact_name)
            payload.update(
                {
                    "updated_at": utc_now(),
                    "status": status,
                    "summary": participant.get("verdict") or payload.get("summary") or "Pending audit review.",
                    "recommendation_authorized": False,
                }
            )
            self.registry.write_json_artifact(
                task_id,
                artifact_name,
                payload,
                schema_name="aas5_audit_record",
            )
        return statuses

    def _branch_completion(
        self,
        *,
        branch_specs: list[dict[str, Any]],
        children: list[dict[str, Any]],
    ) -> dict[str, Any]:
        branch_statuses: dict[str, str] = {}
        completed_branch_ids: list[str] = []
        missing_branch_ids: list[str] = []
        incomplete_branch_ids: list[str] = []
        failed_branch_ids: list[str] = []
        required_branch_ids = [str(item.get("branch_id") or "") for item in branch_specs if str(item.get("branch_id") or "")]
        for branch in branch_specs:
            branch_id = str(branch.get("branch_id") or "")
            if not branch_id:
                continue
            branch_children = [item for item in children if item.get("branch_id") == branch_id]
            status = self._branch_status(branch_children)
            branch_statuses[branch_id] = status
            if status == "COMPLETED":
                completed_branch_ids.append(branch_id)
            elif status == "FAILED":
                failed_branch_ids.append(branch_id)
            elif status == "NOT_STARTED":
                missing_branch_ids.append(branch_id)
            else:
                incomplete_branch_ids.append(branch_id)
        return {
            "required_branch_ids": required_branch_ids,
            "branch_statuses": branch_statuses,
            "completed_branch_ids": completed_branch_ids,
            "missing_branch_ids": missing_branch_ids,
            "incomplete_branch_ids": incomplete_branch_ids,
            "failed_branch_ids": failed_branch_ids,
            "all_required_completed": bool(required_branch_ids)
            and not missing_branch_ids
            and not incomplete_branch_ids
            and not failed_branch_ids,
        }

    def _branch_blocking_reasons(self, *, branch_completion: dict[str, Any]) -> list[str]:
        blockers: list[str] = []
        if branch_completion["missing_branch_ids"]:
            blockers.append(
                "Missing future-branch child results: " + ", ".join(branch_completion["missing_branch_ids"])
            )
        if branch_completion["incomplete_branch_ids"]:
            blockers.append(
                "Incomplete future-branch child results: " + ", ".join(branch_completion["incomplete_branch_ids"])
            )
        if branch_completion["failed_branch_ids"]:
            blockers.append(
                "Failed future-branch child results: " + ", ".join(branch_completion["failed_branch_ids"])
            )
        if blockers:
            blockers.append("Run validate_swarm_execution_record.py before presenting a recommendation.")
        return blockers

    def _sync_future_branch_report(
        self,
        *,
        task_id: str,
        dispatch_record: dict[str, Any],
        future_branch_report: dict[str, Any],
        team_plan: dict[str, Any],
        branch_completion: dict[str, Any],
        recommendation_authorized: bool,
        blocking_gates: list[str],
    ) -> dict[str, Any]:
        future_exploration = (team_plan or {}).get("future_exploration") or {}
        branches = []
        for item in future_exploration.get("branches", []):
            branch_id = str(item.get("branch_id") or "")
            branches.append(
                {
                    "branch_id": branch_id,
                    "parent_role": item.get("parent_role"),
                    "branch_kind": item.get("branch_kind"),
                    "branch_label": item.get("branch_label"),
                    "lane_id": item.get("lane_id"),
                    "lane_label": item.get("lane_label"),
                    "lane_strategy": item.get("lane_strategy"),
                    "objective": item.get("objective"),
                    "expected_artifact": item.get("expected_artifact"),
                    "radical_candidate": bool(item.get("radical_candidate")),
                    "status": branch_completion["branch_statuses"].get(branch_id, "NOT_STARTED"),
                }
            )
        return {
            "type": "FUTURE_BRANCH_REPORT",
            "task_id": task_id,
            "workflow_id": dispatch_record.get("workflow_id") or future_branch_report.get("workflow_id"),
            "dispatch_id": dispatch_record.get("dispatch_id") or future_branch_report.get("dispatch_id"),
            "team_mode": str(((team_plan or {}).get("spawn_policy") or {}).get("team_mode") or "FUTURE_BRANCH_SWARM"),
            "current_stage": str(future_exploration.get("current_stage") or future_branch_report.get("current_stage") or "IDEATION"),
            "convergence_owner": str(future_exploration.get("convergence_owner") or future_branch_report.get("convergence_owner") or "parent"),
            "convergence_artifact": str(
                future_exploration.get("convergence_artifact")
                or future_branch_report.get("convergence_artifact")
                or f"docs/task_workspaces/{task_id}/FUTURE_CONVERGENCE_REPORT.json"
            ),
            "recommendation_authorized": recommendation_authorized,
            "blocking_gates": list(blocking_gates),
            "improvement_trigger_policy": future_exploration.get("improvement_trigger_policy"),
            "radical_trigger_policy": future_exploration.get("radical_trigger_policy"),
            "branches": branches,
            "created_at": future_branch_report.get("created_at") or dispatch_record.get("created_at") or utc_now(),
            "updated_at": utc_now(),
        }

    def _sync_swarm_execution_record(
        self,
        *,
        task_id: str,
        stage: str,
        dispatch_record: dict[str, Any],
        team_plan: dict[str, Any],
        existing_record: dict[str, Any],
        children: list[dict[str, Any]],
        merge_package_ref: str,
        recommendation_authorized: bool,
        blocking_reasons: list[str],
    ) -> dict[str, Any]:
        spawn_policy = (team_plan or {}).get("spawn_policy") or {}
        parent = (team_plan or {}).get("parent") or {}
        required_roles = sorted(
            {
                str(item.get("parent_role") or item.get("role") or "")
                for item in ((team_plan or {}).get("children") or [])
                if str(item.get("parent_role") or item.get("role") or "")
            }
        )
        required_child_ids = [
            str(item.get("branch_id") or "")
            for item in (((team_plan or {}).get("future_exploration") or {}).get("branches") or [])
            if str(item.get("branch_id") or "")
        ]
        runtime_notes = [
            f"Planned batching: {int(spawn_policy.get('planned_wave_count') or 1)} wave(s) of up to {int(spawn_policy.get('spawn_batch_size') or max(len(children), 1))} live children."
        ]
        if blocking_reasons:
            runtime_notes.append("Recommendation remains blocked until swarm validation passes.")
        return {
            "type": "SWARM_EXECUTION_RECORD",
            "task_id": task_id,
            "stage": stage,
            "generated_at": utc_now(),
            "swarm_requirement": {
                "required": True,
                "reason": "Exploratory architecture-heavy FULL PIPELINE ideation requires a real child swarm.",
                "solo_mode_authorized": False,
                "blocking_behavior_if_unavailable": "stop_and_report",
            },
            "runtime_capabilities": {
                "multi_agent_enabled": bool(children),
                "real_child_sessions_available": bool(children),
                "child_result_tracking_available": True,
                "notes": runtime_notes,
            },
            "execution_mode": "REAL_SWARM" if recommendation_authorized else "BLOCKED",
            "parent_session": {
                "agent_name": str(parent.get("agent_name") or existing_record.get("parent_session", {}).get("agent_name") or "pending-parent-agent"),
                "session_id": parent.get("session_id") or existing_record.get("parent_session", {}).get("session_id"),
                "provider": str(parent.get("provider") or existing_record.get("parent_session", {}).get("provider") or "codex"),
                "role": str(parent.get("role") or existing_record.get("parent_session", {}).get("role") or "Swarm Director"),
                "model_audit": parent.get("model_audit") or existing_record.get("parent_session", {}).get("model_audit") or {},
            },
            "required_child_roles": required_roles,
            "required_child_ids": required_child_ids,
            "spawned_children": [
                {
                    "role": str(item.get("role") or ""),
                    "agent_name": str(item.get("agent_name") or ""),
                    "branch_id": item.get("branch_id"),
                    "execution_type": "REAL_CHILD",
                    "status": str(item.get("status") or ""),
                    "session_id": item.get("session_id"),
                    "artifact_ref": item.get("artifact_path"),
                    "model_audit": item.get("model_audit") or {},
                    "artifact_provenance": item.get("artifact_provenance") or {},
                }
                for item in children
            ],
            "internal_viewpoint_roles": [],
            "merge_evidence": {
                "team_plan_ref": f"docs/task_workspaces/{task_id}/TEAM_PLAN.yaml",
                "child_result_merge_package_ref": merge_package_ref,
            },
            "blocking_reason": None if recommendation_authorized else " ; ".join(blocking_reasons),
            "recommendation_authorized": recommendation_authorized,
            "notes": list(existing_record.get("notes") or [])
            + ["Do not treat the ideation run as complete until validator-backed swarm evidence exists."],
            "satisfied": recommendation_authorized,
        }

    def _recommended_actions(self, *, actions: Counter[str], statuses: Counter[str]) -> list[str]:
        results = []
        if statuses.get("FAILED"):
            results.append("Inspect failed child run logs before treating the dispatch as authoritative.")
        if actions:
            top_action, _count = actions.most_common(1)[0]
            results.append(f"Use `{top_action}` as the default parent recommendation unless contradictory evidence overrides it.")
        results.append("Generate a parent synthesis artifact before any shared-state closeout.")
        return results

    def _advisory_considerations(self, children: list[dict[str, Any]]) -> list[dict[str, Any]]:
        considerations = []
        for item in children:
            if str(item.get("role")) != "memory_reuse_analyst":
                continue
            summary = str(item.get("verdict") or "").strip()
            recommended_use = str(item.get("recommended_next_action") or "").strip()
            if not summary and not recommended_use:
                continue
            considerations.append(
                {
                    "source_role": "memory_reuse_analyst",
                    "summary": summary or "Advisory memory-reuse considerations are available.",
                    "recommended_use": recommended_use or "Treat as optional considerations during parent synthesis.",
                    "artifact_path": item.get("artifact_path"),
                }
            )
        return considerations

    def _render_parent_draft(self, *, task_id: str, team_plan: dict[str, Any], package: dict[str, Any]) -> str:
        lines = [
            f"# Parent Synthesis Draft - {task_id}",
            "",
            "## Dispatch Context",
            f"- Dispatch status: `{package.get('dispatch_status')}`",
            f"- Program: `{((team_plan or {}).get('selection') or {}).get('program_title', 'unknown')}`",
            "",
            "## Child Results",
        ]
        for item in package.get("child_results", []):
            lines.extend(
                [
                    f"### {item.get('role')}",
                    f"- Status: `{item.get('status')}`",
                    f"- Verdict: {item.get('verdict') or 'n/a'}",
                    f"- Recommended next action: {item.get('recommended_next_action') or 'n/a'}",
                    f"- Artifact: `{item.get('artifact_path')}`",
                ]
            )
        future_mode = ((team_plan or {}).get("future_exploration") or {}).get("enabled")
        if future_mode:
            lines.extend(["", "## Future Branches"])
            for item in package.get("child_results", []):
                if not item.get("branch_id"):
                    continue
                lines.append(
                    f"- `{item.get('branch_label') or item.get('branch_id')}` via `{item.get('parent_role') or item.get('role')}` [{item.get('lane_label') or item.get('lane_id') or 'untyped'}]: {item.get('verdict') or 'n/a'}"
                )
            improvement_policy = ((team_plan or {}).get("future_exploration") or {}).get("improvement_trigger_policy") or {}
            if improvement_policy.get("enabled"):
                lines.extend(
                    [
                        "",
                        "## Task Improvement Lanes",
                        f"- Trigger reasons: {', '.join(improvement_policy.get('trigger_reasons', [])) or 'none'}",
                        "- Parent must decide whether to `reject`, `adopt`, `hybridize`, or `escalate_to_hitl` a discovered improvement.",
                    ]
                )
            radical_policy = ((team_plan or {}).get("future_exploration") or {}).get("radical_trigger_policy") or {}
            if radical_policy.get("enabled"):
                lines.extend(
                    [
                        "",
                        "## Radical Redesign Lane",
                        f"- Trigger reasons: {', '.join(radical_policy.get('trigger_reasons', [])) or 'none'}",
                        "- Parent must choose one of: `reject`, `hybridize`, `promote`",
                    ]
                )
        if package.get("advisory_considerations"):
            lines.extend(["", "## Advisory Memory-Reuse Considerations"])
            for item in package.get("advisory_considerations", []):
                lines.extend(
                    [
                        f"- Summary: {item.get('summary') or 'n/a'}",
                        f"  Suggested use: {item.get('recommended_use') or 'n/a'}",
                    ]
                )
        if package.get("disagreement_signals"):
            lines.extend(["", "## Disagreement Signals"])
            for item in package.get("disagreement_signals", []):
                lines.append(f"- {item}")
        lines.extend(
            [
                "",
                "## Parent Decision",
                "- Convergent evidence:",
                "- Divergent evidence:",
                "- Chosen next action:",
                "- Residual risks:",
            ]
        )
        return "\n".join(lines)

    def _build_future_convergence_report(
        self,
        *,
        task_id: str,
        dispatch_record: dict[str, Any],
        team_plan: dict[str, Any],
        future_branch_report: dict[str, Any] | None,
        children: list[dict[str, Any]],
        disagreements: list[str],
        actions: Counter[str],
    ) -> dict[str, Any] | None:
        future_exploration = (team_plan or {}).get("future_exploration") or {}
        if not future_exploration.get("enabled"):
            return None
        branch_summaries = []
        branch_index = {
            str(item.get("branch_id")): item
            for item in future_exploration.get("branches", [])
            if item.get("branch_id")
        }
        for branch_id, branch in branch_index.items():
            branch_children = [item for item in children if item.get("branch_id") == branch_id]
            branch_summaries.append(
                {
                    "branch_id": branch_id,
                    "branch_label": branch.get("branch_label"),
                    "parent_role": branch.get("parent_role"),
                    "branch_kind": branch.get("branch_kind"),
                    "lane_id": branch.get("lane_id"),
                    "lane_label": branch.get("lane_label"),
                    "lane_strategy": branch.get("lane_strategy"),
                    "objective": branch.get("objective"),
                    "status": self._branch_status(branch_children),
                    "verdicts": [item.get("verdict") for item in branch_children if item.get("verdict")],
                    "recommended_next_actions": [
                        item.get("recommended_next_action")
                        for item in branch_children
                        if item.get("recommended_next_action")
                    ],
                    "child_artifacts": [item.get("artifact_path") for item in branch_children if item.get("artifact_path")],
                }
            )
        recommended_parent_action = None
        if actions:
            recommended_parent_action = actions.most_common(1)[0][0]
        report = {
            "type": "FUTURE_CONVERGENCE_REPORT",
            "task_id": task_id,
            "workflow_id": dispatch_record.get("workflow_id"),
            "dispatch_id": dispatch_record.get("dispatch_id"),
            "team_mode": dispatch_record.get("future_exploration", {}).get("enabled") and "FUTURE_BRANCH_SWARM" or dispatch_record.get("selection", {}).get("action_label"),
            "current_stage": future_exploration.get("current_stage"),
            "generated_at": utc_now(),
            "branch_count": len(branch_summaries),
            "branch_summaries": branch_summaries,
            "disagreement_signals": disagreements,
            "convergence_summary": self._convergence_summary(branch_summaries=branch_summaries, disagreements=disagreements),
            "recommended_parent_action": recommended_parent_action,
            "source_refs": {
                "team_dispatch_record": f"docs/task_workspaces/{task_id}/TEAM_DISPATCH_RECORD.json",
                "team_plan": f"docs/task_workspaces/{task_id}/TEAM_PLAN.yaml",
                "future_branch_report": f"docs/task_workspaces/{task_id}/FUTURE_BRANCH_REPORT.json" if future_branch_report else None,
            },
        }
        self.registry.write_json_artifact(
            task_id,
            "FUTURE_CONVERGENCE_REPORT.json",
            report,
            schema_name="future_convergence_report",
        )
        return report

    def _build_task_improvement_report(
        self,
        *,
        task_id: str,
        dispatch_record: dict[str, Any],
        team_plan: dict[str, Any],
        future_convergence: dict[str, Any] | None,
        children: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        future_exploration = (team_plan or {}).get("future_exploration") or {}
        improvement_policy = future_exploration.get("improvement_trigger_policy") or {}
        if not improvement_policy.get("enabled"):
            return None
        branch_summaries = list((future_convergence or {}).get("branch_summaries", []))
        lane_order = list(improvement_policy.get("lane_order", [])) or ["alpha", "beta", "gamma", "radical"]
        lane_groups = {lane_id: [] for lane_id in lane_order}
        for branch in branch_summaries:
            lane_id = str(branch.get("lane_id") or "")
            if lane_id:
                lane_groups.setdefault(lane_id, []).append(branch)
        lane_summaries = []
        for lane_id in lane_order:
            lane_branches = lane_groups.get(lane_id, [])
            lane_label = next((item.get("lane_label") for item in lane_branches if item.get("lane_label")), lane_id.title())
            lane_strategy = next((item.get("lane_strategy") for item in lane_branches if item.get("lane_strategy")), "")
            lane_summaries.append(
                {
                    "lane_id": lane_id,
                    "lane_label": lane_label,
                    "lane_strategy": lane_strategy,
                    "branch_count": len(lane_branches),
                    "completed_branch_count": sum(1 for item in lane_branches if item.get("status") == "COMPLETED"),
                    "status": self._lane_status(lane_branches),
                    "branch_ids": [item.get("branch_id") for item in lane_branches if item.get("branch_id")],
                    "verdicts": [verdict for item in lane_branches for verdict in item.get("verdicts", []) if verdict],
                    "recommended_next_actions": [
                        action
                        for item in lane_branches
                        for action in item.get("recommended_next_actions", [])
                        if action
                    ],
                }
            )
        recommended_parent_action = self._recommended_improvement_action(
            lane_summaries=lane_summaries,
            future_convergence=future_convergence or {},
        )
        advisory_considerations = self._advisory_considerations(children)
        report = {
            "type": "TASK_IMPROVEMENT_REPORT",
            "task_id": task_id,
            "workflow_id": dispatch_record.get("workflow_id"),
            "dispatch_id": dispatch_record.get("dispatch_id"),
            "current_stage": future_exploration.get("current_stage"),
            "generated_at": utc_now(),
            "trigger_policy": improvement_policy,
            "lane_summaries": lane_summaries,
            "parent_decision_options": improvement_policy.get(
                "decision_options",
                ["reject", "adopt", "hybridize", "escalate_to_hitl"],
            ),
            "recommended_parent_action": recommended_parent_action,
            "summary": self._improvement_summary(
                lane_summaries=lane_summaries,
                trigger_policy=improvement_policy,
                recommended_parent_action=recommended_parent_action,
                advisory_consideration_count=len(advisory_considerations),
            ),
            "source_refs": {
                "future_convergence_report": f"docs/task_workspaces/{task_id}/FUTURE_CONVERGENCE_REPORT.json" if future_convergence else None,
                "team_dispatch_record": f"docs/task_workspaces/{task_id}/TEAM_DISPATCH_RECORD.json",
                "team_plan": f"docs/task_workspaces/{task_id}/TEAM_PLAN.yaml",
            },
        }
        if advisory_considerations:
            report["advisory_considerations"] = advisory_considerations
        self.registry.write_json_artifact(
            task_id,
            "TASK_IMPROVEMENT_REPORT.json",
            report,
            schema_name="task_improvement_report",
        )
        return report

    def _build_radical_redesign_report(
        self,
        *,
        task_id: str,
        dispatch_record: dict[str, Any],
        team_plan: dict[str, Any],
        future_convergence: dict[str, Any] | None,
        children: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        future_exploration = (team_plan or {}).get("future_exploration") or {}
        radical_policy = future_exploration.get("radical_trigger_policy") or {}
        if not radical_policy.get("enabled"):
            return None
        radical_branch_ids = set(radical_policy.get("radical_branch_ids", []))
        radical_children = [item for item in children if item.get("branch_id") in radical_branch_ids]
        radical_branch_summaries = []
        convergence_index = {
            item.get("branch_id"): item
            for item in (future_convergence or {}).get("branch_summaries", [])
            if item.get("branch_id")
        }
        for branch_id in radical_branch_ids:
            branch_summary = convergence_index.get(branch_id)
            if branch_summary is None:
                matching = [item for item in radical_children if item.get("branch_id") == branch_id]
                branch_summary = {
                    "branch_id": branch_id,
                    "branch_label": next((item.get("branch_label") for item in matching if item.get("branch_label")), branch_id),
                    "parent_role": next((item.get("parent_role") for item in matching if item.get("parent_role")), None),
                    "branch_kind": next((item.get("branch_kind") for item in matching if item.get("branch_kind")), None),
                    "lane_id": next((item.get("lane_id") for item in matching if item.get("lane_id")), None),
                    "lane_label": next((item.get("lane_label") for item in matching if item.get("lane_label")), None),
                    "lane_strategy": next((item.get("lane_strategy") for item in matching if item.get("lane_strategy")), None),
                    "objective": "",
                    "status": self._branch_status(matching),
                    "verdicts": [item.get("verdict") for item in matching if item.get("verdict")],
                    "recommended_next_actions": [item.get("recommended_next_action") for item in matching if item.get("recommended_next_action")],
                    "child_artifacts": [item.get("artifact_path") for item in matching if item.get("artifact_path")],
                }
            radical_branch_summaries.append(branch_summary)
        report = {
            "type": "RADICAL_REDESIGN_REPORT",
            "task_id": task_id,
            "workflow_id": dispatch_record.get("workflow_id"),
            "dispatch_id": dispatch_record.get("dispatch_id"),
            "current_stage": future_exploration.get("current_stage"),
            "generated_at": utc_now(),
            "trigger_policy": radical_policy,
            "radical_branch_summaries": radical_branch_summaries,
            "parent_decision_options": radical_policy.get("decision_options", ["reject", "hybridize", "promote"]),
            "summary": self._radical_summary(radical_branch_summaries=radical_branch_summaries, trigger_policy=radical_policy),
            "source_refs": {
                "future_convergence_report": f"docs/task_workspaces/{task_id}/FUTURE_CONVERGENCE_REPORT.json" if future_convergence else None,
                "team_dispatch_record": f"docs/task_workspaces/{task_id}/TEAM_DISPATCH_RECORD.json",
                "team_plan": f"docs/task_workspaces/{task_id}/TEAM_PLAN.yaml",
            },
        }
        self.registry.write_json_artifact(
            task_id,
            "RADICAL_REDESIGN_REPORT.json",
            report,
            schema_name="radical_redesign_report",
        )
        return report

    def _branch_status(self, branch_children: list[dict[str, Any]]) -> str:
        statuses = {str(item.get("status") or "") for item in branch_children}
        if not branch_children:
            return "NOT_STARTED"
        if statuses == {"COMPLETED"}:
            return "COMPLETED"
        if "FAILED" in statuses and len(statuses) == 1:
            return "FAILED"
        if "FAILED" in statuses:
            return "PARTIAL_FAILURE"
        return "IN_PROGRESS"

    def _lane_status(self, lane_branches: list[dict[str, Any]]) -> str:
        statuses = {str(item.get("status") or "") for item in lane_branches}
        if not lane_branches:
            return "NOT_STARTED"
        if statuses == {"COMPLETED"}:
            return "COMPLETED"
        if "FAILED" in statuses and len(statuses) == 1:
            return "FAILED"
        if "FAILED" in statuses:
            return "PARTIAL_FAILURE"
        return "IN_PROGRESS"

    def _convergence_summary(
        self,
        *,
        branch_summaries: list[dict[str, Any]],
        disagreements: list[str],
    ) -> str:
        if disagreements:
            return "Branch futures diverge in ways that require explicit parent reconciliation."
        if not branch_summaries:
            return "No future branches were recorded."
        completed = sum(1 for item in branch_summaries if item.get("status") == "COMPLETED")
        return f"{completed} future branch(es) completed without a merge-blocking disagreement signal."

    def _recommended_improvement_action(
        self,
        *,
        lane_summaries: list[dict[str, Any]],
        future_convergence: dict[str, Any],
    ) -> str:
        if any(item.get("status") == "FAILED" for item in lane_summaries):
            return "hybridize"
        if any(
            item.get("lane_id") in {"gamma", "radical"} and item.get("completed_branch_count", 0) > 0
            for item in lane_summaries
        ):
            return "escalate_to_hitl"
        if future_convergence.get("disagreement_signals"):
            return "hybridize"
        if any(item.get("completed_branch_count", 0) > 0 for item in lane_summaries):
            return "adopt"
        return "reject"

    def _improvement_summary(
        self,
        *,
        lane_summaries: list[dict[str, Any]],
        trigger_policy: dict[str, Any],
        recommended_parent_action: str,
        advisory_consideration_count: int = 0,
    ) -> str:
        completed = sum(item.get("completed_branch_count", 0) for item in lane_summaries)
        trigger_text = ", ".join(trigger_policy.get("trigger_reasons", [])) or "task-improvement pressure"
        lane_order = list(trigger_policy.get("lane_order", [])) or [item.get("lane_id") for item in lane_summaries]
        lane_labels = "/".join(str(lane_id).title() for lane_id in lane_order if lane_id)
        summary = (
            f"Task-improvement lanes were activated by {trigger_text}; {completed} branch result(s) completed "
            f"across {lane_labels or 'typed future-branch'} lanes and the parent should {recommended_parent_action} the strongest improvement path."
        )
        if advisory_consideration_count:
            summary += f" {advisory_consideration_count} advisory memory-reuse consideration(s) are available for optional reuse or hybridization."
        return summary

    def _radical_summary(
        self,
        *,
        radical_branch_summaries: list[dict[str, Any]],
        trigger_policy: dict[str, Any],
    ) -> str:
        if not radical_branch_summaries:
            return "The radical redesign lane was triggered, but no radical branch outputs were recorded."
        completed = sum(1 for item in radical_branch_summaries if item.get("status") == "COMPLETED")
        trigger_text = ", ".join(trigger_policy.get("trigger_reasons", [])) or "manual architecture pressure"
        return f"The radical redesign lane was triggered by {trigger_text}; {completed} radical branch(es) completed and now require a parent decision to reject, hybridize, or promote."
