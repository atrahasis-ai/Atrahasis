from __future__ import annotations

import json
import shutil
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
    build_audit_payload,
    build_execution_parallelism_payload,
    build_lane_plan_payload,
    build_lane_report_payload,
    build_topology_graph_payload,
    lane_manager,
    lane_plan_path,
    lane_report_path,
    lane_reporter,
    lane_worker_node_ids,
    make_run_key,
)
from aas1.workflow_policy_engine import future_exploration_for


def copy_aas5_validator_runtime(*, source_repo: Path, destination_repo: Path) -> None:
    (destination_repo / "scripts").mkdir(parents=True, exist_ok=True)
    (destination_repo / "src" / "aas1").mkdir(parents=True, exist_ok=True)
    (destination_repo / "src" / "aas1" / "__init__.py").write_text("", encoding="utf-8")
    for relative in [
        ("scripts", "validate_swarm_execution_record.py"),
        ("src/aas1", "swarm_validation.py"),
        ("src/aas1", "aas5_ideation.py"),
    ]:
        root, name = relative
        shutil.copy2(source_repo / root / name, destination_repo / root / name)


class AAS5IdeationFixture:
    def __init__(self, *, task_id: str = "T-9002", workflow_id: str = "wf-1", dispatch_id: str = "disp-1") -> None:
        self.task_id = task_id
        self.workflow_id = workflow_id
        self.dispatch_id = dispatch_id
        self.generated_at = "2026-03-15T00:00:00Z"
        self.run_key = make_run_key(task_id, workflow_id)
        policy = future_exploration_for("FULL_PIPELINE", "IDEATION")
        assert policy is not None
        self.policy = dict(policy)
        self.branch_specs = [dict(item) for item in self.policy.get("branches", [])]
        self.nodes = build_aas5_ideation_nodes(task_id=task_id, branch_specs=self.branch_specs, title="Fixture")
        self.node_map = {node.node_id: node for node in self.nodes}
        self.manager_nodes = [node for node in self.nodes if node.tier == "lane_manager"]
        self.worker_nodes = [node for node in self.nodes if node.tier == "lane_worker"]
        self.reporter_nodes = [node for node in self.nodes if node.tier == "lane_reporter"]
        self.auditor_nodes = auditor_nodes(self.nodes)
        self.lane_ids = [lane_id for lane_id in (self.policy.get("lane_order") or []) if lane_manager(self.nodes, lane_id)]

    def non_parent_node_ids(self) -> list[str]:
        return [node.node_id for node in self.nodes]

    def _ref(self, relative_path: str) -> str:
        return f"docs/task_workspaces/{self.task_id}/{relative_path}"

    def _write(self, path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def _model_audit(self, *, model: str, effort: str, exposed: bool) -> dict[str, Any]:
        return {
            "requested_model": model,
            "requested_reasoning_effort": effort,
            "observed_runtime_model": model if exposed else None,
            "observed_model_auditability": "verified_exact" if exposed else "runtime_not_exposed",
            "routing_basis": "test fixture",
            "policy_target": model,
            "actual_runtime_model": model if exposed else None,
            "reasoning_effort": effort,
            "auditability": "verified_exact" if exposed else "runtime_not_exposed",
        }

    def write_workspace(
        self,
        task_root: Path,
        *,
        include_authority_matrix: bool = True,
        include_child_results: bool = True,
        spawned_node_ids: list[str] | None = None,
        execution_mode: str = "REAL_SWARM",
        satisfied: bool = True,
        recommendation_authorized: bool = True,
        multi_agent_enabled: bool = True,
        real_child_sessions_available: bool = True,
        internal_viewpoint_roles: list[str] | None = None,
    ) -> None:
        spawned = spawned_node_ids or self.non_parent_node_ids()
        self._write(task_root / "COMMAND_REQUEST.yaml", {"task_id": self.task_id, "command_modifier": "AASNI"})
        self._write(task_root / "HUMAN_DECISION_RECORD.json", {"operator_decision": "PENDING"})
        self._write(
            task_root / "WORKFLOW_RUN_RECORD.json",
            {
                "type": "WORKFLOW_RUN_RECORD",
                "doctrine_version": AAS5_DOCTRINE_VERSION,
                "topology_mode": AAS5_TOPOLOGY_MODE,
                "workflow_id": self.workflow_id,
                "run_key": self.run_key,
                "task_id": self.task_id,
                "modifier": "AASNI",
                "status": "IDEATION_IN_PROGRESS",
                "started_at": self.generated_at,
                "completed_at": self.generated_at,
                "orchestrator": "InventionPipelineManager",
                "gcml_documents_loaded": 0,
                "manifest_document_count": 0,
                "artifacts": {},
                "stage_records": [],
                "hitl_requirements": [],
                "operator_constraints": [],
                "recommended_next_actions": [],
            },
        )
        self._write(
            task_root / "TEAM_PLAN.yaml",
            {
                "version": "1.0",
                "doctrine_version": AAS5_DOCTRINE_VERSION,
                "topology_mode": AAS5_TOPOLOGY_MODE,
                "task_id": self.task_id,
                "workflow_id": self.workflow_id,
                "run_key": self.run_key,
                "dispatch_id": self.dispatch_id,
                "status": "PLANNED",
                "created_at": self.generated_at,
                "updated_at": self.generated_at,
                "parent": {
                    "node_id": "mst",
                    "provider": "codex",
                    "agent_name": "Utu",
                    "session_id": "parent-1",
                    "role": "master_orchestrator",
                    "merge_owner": "Utu",
                    "model": "gpt-5.4",
                    "reasoning_effort": "xhigh",
                    "model_audit": self._model_audit(model="gpt-5.4", effort="xhigh", exposed=True),
                },
                "spawn_policy": {
                    "team_mode": "FUTURE_BRANCH_SWARM",
                    "orchestration_topology": "master_lane_managers_reporters_auditors",
                    "manager_count": 4,
                    "reporter_count": 4,
                    "auditor_count": 4,
                    "worker_count": 12,
                    "total_non_parent_participants": 24,
                    "total_agents": 25,
                    "simultaneous_target_agent_count": 25,
                },
                "manager_orchestrators": [{"node_id": node.node_id, "manager_id": node.node_id} for node in self.manager_nodes],
                "lane_convergence_reporters": [{"node_id": node.node_id} for node in self.reporter_nodes],
                "audit_orchestrators": [{"node_id": node.node_id} for node in self.auditor_nodes],
                "workers": [{"node_id": node.node_id} for node in self.worker_nodes],
                "children": [{"node_id": node.node_id} for node in self.nodes],
            },
        )
        self._write(
            task_root / "FUTURE_BRANCH_REPORT.json",
            {
                "type": "FUTURE_BRANCH_REPORT",
                "doctrine_version": AAS5_DOCTRINE_VERSION,
                "topology_mode": AAS5_TOPOLOGY_MODE,
                "task_id": self.task_id,
                "workflow_id": self.workflow_id,
                "run_key": self.run_key,
                "dispatch_id": self.dispatch_id,
                "team_mode": "FUTURE_BRANCH_SWARM",
                "current_stage": "IDEATION",
                "recommendation_authorized": recommendation_authorized,
                "lane_summaries": [
                    {
                        "lane_id": lane_id,
                        "worker_node_ids": lane_worker_node_ids(self.nodes, lane_id),
                        "reporter_node_id": f"rep.{lane_id}",
                    }
                    for lane_id in self.lane_ids
                ],
                "branches": [{"branch_id": item["branch_id"], "lane_id": item["lane_id"], "status": "COMPLETED"} for item in self.branch_specs],
            },
        )
        self._write(
            task_root / "CHILD_RESULT_MERGE_PACKAGE.json",
            {
                "type": "CHILD_RESULT_MERGE_PACKAGE",
                "doctrine_version": AAS5_DOCTRINE_VERSION,
                "topology_mode": AAS5_TOPOLOGY_MODE,
                "task_id": self.task_id,
                "workflow_id": self.workflow_id,
                "run_key": self.run_key,
                "dispatch_id": self.dispatch_id,
                "dispatch_status": "COMPLETED",
                "generated_at": self.generated_at,
                "merge_ready": True,
                "child_results": [{"node_id": node_id, "artifact_path": self._ref(self.node_map[node_id].expected_artifact)} for node_id in spawned],
            },
        )
        for lane_id in self.lane_ids:
            manager = lane_manager(self.nodes, lane_id)
            reporter = lane_reporter(self.nodes, lane_id)
            assert manager is not None and reporter is not None
            self._write(
                task_root / lane_plan_path(lane_id),
                build_lane_plan_payload(
                    task_id=self.task_id,
                    workflow_id=self.workflow_id,
                    run_key=self.run_key,
                    lane_id=lane_id,
                    lane_label=manager.lane_label or lane_id.title(),
                    lane_strategy=manager.lane_strategy or "",
                    manager_id=manager.node_id,
                    worker_node_ids=lane_worker_node_ids(self.nodes, lane_id),
                    reporter_node_id=reporter.node_id,
                    generated_at=self.generated_at,
                ),
            )
            self._write(
                task_root / lane_report_path(lane_id),
                {
                    **build_lane_report_payload(
                        task_id=self.task_id,
                        workflow_id=self.workflow_id,
                        run_key=self.run_key,
                        lane_id=lane_id,
                        lane_label=reporter.lane_label or lane_id.title(),
                        reporter_node_id=reporter.node_id,
                        worker_node_ids=lane_worker_node_ids(self.nodes, lane_id),
                        generated_at=self.generated_at,
                    ),
                    "status": "COMPLETED",
                },
            )
        for node in self.auditor_nodes:
            self._write(
                task_root / audit_artifact_path(node.audit_domain or ""),
                {
                    **build_audit_payload(
                        artifact_type=node.role_label.upper().replace(" ", "_"),
                        task_id=self.task_id,
                        workflow_id=self.workflow_id,
                        run_key=self.run_key,
                        owner_node_id=node.node_id,
                        generated_at=self.generated_at,
                        summary="complete",
                        blocking_gates=[],
                    ),
                    "status": "COMPLETED",
                },
            )
        self._write(task_root / SWARM_TOPOLOGY_GRAPH, build_topology_graph_payload(task_id=self.task_id, workflow_id=self.workflow_id, run_key=self.run_key, generated_at=self.generated_at, nodes=self.nodes))
        self._write(task_root / EXECUTION_PARALLELISM_RECORD, {**build_execution_parallelism_payload(task_id=self.task_id, workflow_id=self.workflow_id, run_key=self.run_key, generated_at=self.generated_at, nodes=self.nodes, max_live_children=24), "batch_count": 1, "actual_parallel_agent_count": 25, "max_live_concurrent_agents": 25, "max_live_concurrent_children": 24, "runtime_limit_evidence": [{"source": "fixture"}]})
        if include_authority_matrix:
            self._write(
                task_root / "AUTHORITY_COVERAGE_MATRIX.json",
                {
                    "type": "AUTHORITY_COVERAGE_MATRIX",
                    "doctrine_version": AAS5_DOCTRINE_VERSION,
                    "task_id": self.task_id,
                    "workflow_id": self.workflow_id,
                    "run_key": self.run_key,
                    "stage": "IDEATION",
                    "generated_at": self.generated_at,
                    "coverage_required": True,
                    "recommendation_blocked_until_complete": True,
                    "named_authority_surfaces": ["C45", "C42"],
                    "surface_rows": [
                        {"surface": "C45", "coverage_status": "ADDRESSED", "disposition": "requires_direct_spec_addendum", "new_authority_needed": False, "notes": ["covered"]},
                        {"surface": "C42", "coverage_status": "ADDRESSED", "disposition": "requires_direct_spec_addendum", "new_authority_needed": False, "notes": ["covered"]},
                    ],
                    "new_semantic_authority_test": {"verdict": "execution_profile_addendum", "affected_modules": ["C45", "C42"]},
                },
            )
        if include_child_results:
            for node_id in spawned:
                node = self.node_map[node_id]
                self._write(
                    task_root / node.expected_artifact,
                    {
                        "type": "CHILD_AGENT_RESULT",
                        "doctrine_version": AAS5_DOCTRINE_VERSION,
                        "task_id": self.task_id,
                        "workflow_id": self.workflow_id,
                        "run_key": self.run_key,
                        "node_id": node.node_id,
                        "parent_node_id": node.parent_node_id,
                        "role": node.role,
                        "role_label": node.role_label,
                        "status": "COMPLETED",
                        "session_identity": {"agent_name": node.node_id, "session_id": f"session-{node.node_id}", "provider": "codex", "role": node.role, "node_id": node.node_id},
                        "model_audit": self._model_audit(model=node.requested_model, effort=node.requested_reasoning_effort, exposed=True),
                        "artifact_provenance": {"writer_mode": "child_session", "owner_node_id": node.node_id},
                        "audit_domain": node.audit_domain,
                        "lane_id": node.lane_id,
                        "branch_id": node.branch_id,
                        "verdict": "covered",
                        "recommended_next_action": "merge",
                    },
                )
        self._write(
            task_root / "SWARM_EXECUTION_RECORD.json",
            {
                "type": "SWARM_EXECUTION_RECORD",
                "doctrine_version": AAS5_DOCTRINE_VERSION,
                "topology_mode": AAS5_TOPOLOGY_MODE,
                "task_id": self.task_id,
                "workflow_id": self.workflow_id,
                "run_key": self.run_key,
                "stage": "IDEATION",
                "generated_at": self.generated_at,
                "swarm_requirement": {"required": True, "solo_mode_authorized": False},
                "runtime_capabilities": {"multi_agent_enabled": multi_agent_enabled, "real_child_sessions_available": real_child_sessions_available, "child_result_tracking_available": True},
                "execution_mode": execution_mode,
                "parent_session": {"node_id": "mst", "agent_name": "Utu", "session_id": "parent-1", "provider": "codex", "role": "master_orchestrator", "model_audit": self._model_audit(model="gpt-5.4", effort="xhigh", exposed=True)},
                "required_child_roles": ["visionary", "systems_thinker", "critic"],
                "required_child_ids": [item["branch_id"] for item in self.branch_specs],
                "required_node_ids": ["mst", *self.non_parent_node_ids()],
                "required_manager_ids": [node.node_id for node in self.manager_nodes],
                "required_reporter_ids": [node.node_id for node in self.reporter_nodes],
                "required_auditor_ids": [node.node_id for node in self.auditor_nodes],
                "required_worker_node_ids": [node.node_id for node in self.worker_nodes],
                "spawned_children": [
                    {
                        "node_id": node_id,
                        "artifact_ref": self._ref(self.node_map[node_id].expected_artifact),
                        "model_audit": self._model_audit(model=self.node_map[node_id].requested_model, effort=self.node_map[node_id].requested_reasoning_effort, exposed=True),
                    }
                    for node_id in spawned
                ],
                "internal_viewpoint_roles": list(internal_viewpoint_roles or []),
                "merge_evidence": {
                    "team_plan_ref": self._ref("TEAM_PLAN.yaml"),
                    "child_result_merge_package_ref": self._ref("CHILD_RESULT_MERGE_PACKAGE.json"),
                    "topology_graph_ref": self._ref(SWARM_TOPOLOGY_GRAPH),
                    "execution_parallelism_record_ref": self._ref(EXECUTION_PARALLELISM_RECORD),
                    "future_branch_report_ref": self._ref("FUTURE_BRANCH_REPORT.json"),
                },
                "recommendation_authorized": recommendation_authorized,
                "satisfied": satisfied,
            },
        )
        (task_root / "evidence").mkdir(parents=True, exist_ok=True)
        (task_root / "evidence" / "note.md").write_text("evidence", encoding="utf-8")
        (task_root / "analysis.md").write_text("analysis", encoding="utf-8")

    def authority_coverage_matrix_payload(self) -> dict[str, Any]:
        return {
            "type": "AUTHORITY_COVERAGE_MATRIX",
            "doctrine_version": AAS5_DOCTRINE_VERSION,
            "task_id": self.task_id,
            "workflow_id": self.workflow_id,
            "run_key": self.run_key,
            "stage": "IDEATION",
            "generated_at": self.generated_at,
            "coverage_required": True,
            "recommendation_blocked_until_complete": True,
            "named_authority_surfaces": ["C45", "C42"],
            "surface_rows": [
                {"surface": "C45", "coverage_status": "ADDRESSED", "disposition": "requires_direct_spec_addendum", "new_authority_needed": False, "notes": ["covered"]},
                {"surface": "C42", "coverage_status": "ADDRESSED", "disposition": "requires_direct_spec_addendum", "new_authority_needed": False, "notes": ["covered"]},
            ],
            "new_semantic_authority_test": {"verdict": "execution_profile_addendum", "affected_modules": ["C45", "C42"]},
        }

    def write_supporting_artifacts(self, task_root: Path, **kwargs: Any) -> None:
        self.write_workspace(task_root, **kwargs)

    def write_json(self, path: Path, payload: dict[str, Any]) -> None:
        self._write(path, payload)
