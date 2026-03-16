from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from aas5.aas5_ideation import (
    ADVERSARIAL_INTEGRITY_REVIEW,
    AUTHORITY_COVERAGE_AUDIT,
    AAS5_DOCTRINE_VERSION,
    AAS5_IDEATION_AGENT_COUNT,
    AAS5_NON_PARENT_NODE_COUNT,
    AAS5_TOPOLOGY_MODE,
    EXECUTION_PARALLELISM_RECORD,
    LANE_IDS,
    MODEL_AUDITABILITY_STATES,
    RUNTIME_AUDIT_RECORD,
    SWARM_COMPLIANCE_AUDIT,
    SWARM_TOPOLOGY_GRAPH,
    lane_plan_path,
    lane_report_path,
)


def validate_swarm_execution_task(*, repo_root: Path, task_id: str) -> list[str]:
    task_token = task_id.strip().upper()
    record_path = repo_root / "docs" / "task_workspaces" / task_token / "SWARM_EXECUTION_RECORD.json"
    if not record_path.exists():
        return [f"SWARM_EXECUTION_RECORD.json not found for {task_token}"]
    try:
        payload = json.loads(record_path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive
        return [f"Failed to parse {record_path}: {exc}"]
    return validate_swarm_execution_payload(repo_root=repo_root, task_id=task_token, payload=payload)


def validate_swarm_execution_payload(*, repo_root: Path, task_id: str, payload: dict[str, Any]) -> list[str]:
    merge_evidence = payload.get("merge_evidence") or {}
    team_plan_ref = str(merge_evidence.get("team_plan_ref") or "")
    team_plan = _load_yaml_artifact(repo_root=repo_root, ref=team_plan_ref) if team_plan_ref else {}
    doctrine_version = str(payload.get("doctrine_version") or team_plan.get("doctrine_version") or "LEGACY")
    if doctrine_version == AAS5_DOCTRINE_VERSION:
        return _validate_aas5_payload(repo_root=repo_root, task_id=task_id, payload=payload, team_plan=team_plan)
    return _validate_legacy_payload(repo_root=repo_root, task_id=task_id, payload=payload, team_plan=team_plan)


def _validate_legacy_payload(
    *,
    repo_root: Path,
    task_id: str,
    payload: dict[str, Any],
    team_plan: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    merge_evidence = payload.get("merge_evidence") or {}
    if not (payload.get("swarm_requirement") or {}).get("required"):
        failures.append("swarm_requirement.required must be true for legacy real-swarm validation")
    if payload.get("execution_mode") != "REAL_SWARM":
        failures.append("execution_mode must be REAL_SWARM for legacy ideation validation")
    if not payload.get("satisfied"):
        failures.append("satisfied must be true for legacy ideation validation")
    if payload.get("recommendation_authorized") is not True:
        failures.append("recommendation_authorized must be true for legacy ideation validation")
    spawned_children = list(payload.get("spawned_children") or [])
    if not spawned_children:
        failures.append("spawned_children must contain at least one real child")
    team_plan_ref = str(merge_evidence.get("team_plan_ref") or "")
    if not team_plan_ref:
        failures.append("merge_evidence.team_plan_ref is required")
    elif not _artifact_ref_exists(repo_root=repo_root, ref=team_plan_ref):
        failures.append("merge_evidence.team_plan_ref must point to an existing artifact")
    if team_plan and not list(team_plan.get("children") or []):
        failures.append("TEAM_PLAN.yaml must declare legacy children")
    for child in spawned_children:
        artifact_ref = str(child.get("artifact_ref") or "")
        if not artifact_ref:
            failures.append("legacy spawned child is missing artifact_ref")
            continue
        child_payload = _load_json_artifact(repo_root=repo_root, ref=artifact_ref)
        if child_payload is None:
            failures.append(f"legacy child artifact missing or invalid: {artifact_ref}")
            continue
        if str(child_payload.get("status") or "").upper() == "PLANNED":
            failures.append(f"legacy child artifact remained PLANNED: {artifact_ref}")
    future_branch_report = repo_root / "docs" / "task_workspaces" / task_id / "FUTURE_BRANCH_REPORT.json"
    if not future_branch_report.exists():
        failures.append("legacy ideation requires FUTURE_BRANCH_REPORT.json")
    return failures


def _validate_aas5_payload(
    *,
    repo_root: Path,
    task_id: str,
    payload: dict[str, Any],
    team_plan: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    merge_evidence = payload.get("merge_evidence") or {}
    runtime = payload.get("runtime_capabilities") or {}
    spawned_children = list(payload.get("spawned_children") or [])
    if payload.get("doctrine_version") != AAS5_DOCTRINE_VERSION:
        failures.append("SWARM_EXECUTION_RECORD.json must declare doctrine_version=AAS5")
    if str(payload.get("topology_mode") or "") != AAS5_TOPOLOGY_MODE:
        failures.append(f"SWARM_EXECUTION_RECORD.json must declare topology_mode={AAS5_TOPOLOGY_MODE}")
    if not team_plan:
        failures.append("AAS5 validation requires TEAM_PLAN.yaml")
        return failures
    if str(team_plan.get("doctrine_version") or "") != AAS5_DOCTRINE_VERSION:
        failures.append("TEAM_PLAN.yaml must declare doctrine_version=AAS5")
    if str(team_plan.get("topology_mode") or "") != AAS5_TOPOLOGY_MODE:
        failures.append(f"TEAM_PLAN.yaml must declare topology_mode={AAS5_TOPOLOGY_MODE}")

    spawn_policy = team_plan.get("spawn_policy") or {}
    if str(spawn_policy.get("team_mode") or "") != "FUTURE_BRANCH_SWARM":
        failures.append("TEAM_PLAN.yaml must keep team_mode FUTURE_BRANCH_SWARM for AAS5 ideation")
    expected_counts = {
        "manager_count": 4,
        "reporter_count": 4,
        "auditor_count": 4,
        "worker_count": 12,
        "total_non_parent_participants": AAS5_NON_PARENT_NODE_COUNT,
        "total_agents": AAS5_IDEATION_AGENT_COUNT,
        "simultaneous_target_agent_count": AAS5_IDEATION_AGENT_COUNT,
    }
    for key, expected in expected_counts.items():
        if int(spawn_policy.get(key) or 0) != expected:
            failures.append(f"TEAM_PLAN.yaml spawn_policy.{key} must equal {expected}")
    children = list(team_plan.get("children") or [])
    if len(children) != AAS5_NON_PARENT_NODE_COUNT:
        failures.append("TEAM_PLAN.yaml must declare exactly 24 non-parent participants")
    manager_ids = {str(item.get("node_id") or item.get("manager_id") or "") for item in team_plan.get("manager_orchestrators", [])}
    reporter_ids = {str(item.get("node_id") or "") for item in team_plan.get("lane_convergence_reporters", [])}
    auditor_ids = {str(item.get("node_id") or "") for item in team_plan.get("audit_orchestrators", [])}
    worker_ids = {str(item.get("node_id") or "") for item in team_plan.get("workers", [])}
    if manager_ids != {f"mgr.{lane_id}" for lane_id in LANE_IDS}:
        failures.append("TEAM_PLAN.yaml must declare exactly the four AAS5 manager node ids")
    if reporter_ids != {f"rep.{lane_id}" for lane_id in LANE_IDS}:
        failures.append("TEAM_PLAN.yaml must declare exactly the four AAS5 reporter node ids")
    if auditor_ids != {"aud.compliance", "aud.runtime", "aud.authority", "aud.adversarial"}:
        failures.append("TEAM_PLAN.yaml must declare exactly the four AAS5 auditor node ids")
    if len(worker_ids) != 12:
        failures.append("TEAM_PLAN.yaml must declare exactly twelve AAS5 worker node ids")

    required_node_ids = ["mst", *[str(item) for item in (payload.get("required_node_ids") or []) if str(item)]]
    if len(set(required_node_ids)) != AAS5_IDEATION_AGENT_COUNT:
        failures.append("SWARM_EXECUTION_RECORD.json required_node_ids must enumerate the full 25-node AAS5 topology")

    topology_graph = _load_required_json(
        repo_root=repo_root,
        ref=str(merge_evidence.get("topology_graph_ref") or f"docs/task_workspaces/{task_id}/{SWARM_TOPOLOGY_GRAPH}"),
        failures=failures,
        label=SWARM_TOPOLOGY_GRAPH,
    )
    if topology_graph:
        graph_nodes = {str(item.get("node_id") or "") for item in topology_graph.get("nodes", []) if str(item.get("node_id") or "")}
        if len(graph_nodes) != AAS5_IDEATION_AGENT_COUNT:
            failures.append(f"{SWARM_TOPOLOGY_GRAPH} must contain exactly 25 nodes")
        expected_graph_nodes = {"mst", *manager_ids, *reporter_ids, *auditor_ids, *worker_ids}
        if graph_nodes != expected_graph_nodes:
            failures.append(f"{SWARM_TOPOLOGY_GRAPH} node ids must match TEAM_PLAN.yaml")

    parallelism = _load_required_json(
        repo_root=repo_root,
        ref=str(
            merge_evidence.get("execution_parallelism_record_ref")
            or f"docs/task_workspaces/{task_id}/{EXECUTION_PARALLELISM_RECORD}"
        ),
        failures=failures,
        label=EXECUTION_PARALLELISM_RECORD,
    )
    if parallelism:
        if int(parallelism.get("simultaneous_target_agent_count") or 0) != AAS5_IDEATION_AGENT_COUNT:
            failures.append(f"{EXECUTION_PARALLELISM_RECORD} must declare simultaneous_target_agent_count=25")
        if int(parallelism.get("total_agents_spawned") or 0) != AAS5_IDEATION_AGENT_COUNT:
            failures.append(f"{EXECUTION_PARALLELISM_RECORD} must declare total_agents_spawned=25")

    future_branch_report = _load_required_json(
        repo_root=repo_root,
        ref=str(merge_evidence.get("future_branch_report_ref") or f"docs/task_workspaces/{task_id}/FUTURE_BRANCH_REPORT.json"),
        failures=failures,
        label="FUTURE_BRANCH_REPORT.json",
    )
    if future_branch_report:
        if str(future_branch_report.get("doctrine_version") or "") != AAS5_DOCTRINE_VERSION:
            failures.append("FUTURE_BRANCH_REPORT.json must declare doctrine_version=AAS5")
        if len(list(future_branch_report.get("lane_summaries") or [])) != 4:
            failures.append("FUTURE_BRANCH_REPORT.json must record four lane_summaries for AAS5 ideation")

    for lane_id in LANE_IDS:
        lane_plan = _load_required_json_or_yaml(
            repo_root=repo_root,
            ref=f"docs/task_workspaces/{task_id}/{lane_plan_path(lane_id)}",
            failures=failures,
            label=lane_plan_path(lane_id),
        )
        if lane_plan and len(list(lane_plan.get("worker_node_ids") or [])) != 3:
            failures.append(f"{lane_plan_path(lane_id)} must enumerate exactly three worker_node_ids")
        lane_report = _load_required_json(
            repo_root=repo_root,
            ref=f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}",
            failures=failures,
            label=lane_report_path(lane_id),
        )
        if lane_report and str(lane_report.get("reporter_node_id") or "") != f"rep.{lane_id}":
            failures.append(f"{lane_report_path(lane_id)} must belong to reporter node rep.{lane_id}")

    for ref, label in [
        (f"docs/task_workspaces/{task_id}/{SWARM_COMPLIANCE_AUDIT}", SWARM_COMPLIANCE_AUDIT),
        (f"docs/task_workspaces/{task_id}/{RUNTIME_AUDIT_RECORD}", RUNTIME_AUDIT_RECORD),
        (f"docs/task_workspaces/{task_id}/{AUTHORITY_COVERAGE_AUDIT}", AUTHORITY_COVERAGE_AUDIT),
        (f"docs/task_workspaces/{task_id}/{ADVERSARIAL_INTEGRITY_REVIEW}", ADVERSARIAL_INTEGRITY_REVIEW),
    ]:
        audit_payload = _load_required_json(repo_root=repo_root, ref=ref, failures=failures, label=label)
        if audit_payload and str(audit_payload.get("status") or "").upper() == "PLANNED" and payload.get("execution_mode") == "REAL_SWARM":
            failures.append(f"{label} must not remain PLANNED once execution_mode=REAL_SWARM")

    parent_session = payload.get("parent_session") or {}
    _validate_model_audit(parent_session.get("model_audit") or {}, failures, "parent_session.model_audit")
    if str(parent_session.get("node_id") or "") not in {"", "mst"}:
        failures.append("parent_session.node_id must be mst when recorded")

    if payload.get("execution_mode") != "REAL_SWARM":
        failures.append("AAS5 ideation requires execution_mode=REAL_SWARM before stage close")
    if not payload.get("satisfied"):
        failures.append("AAS5 ideation requires satisfied=true before stage close")
    if not runtime.get("multi_agent_enabled"):
        failures.append("runtime_capabilities.multi_agent_enabled must be true for AAS5 validation")
    if not runtime.get("real_child_sessions_available"):
        failures.append("runtime_capabilities.real_child_sessions_available must be true for AAS5 validation")
    if len(spawned_children) != AAS5_NON_PARENT_NODE_COUNT:
        failures.append("spawned_children must contain exactly 24 non-parent participant sessions for AAS5")

    seen_node_ids: set[str] = set()
    for child in spawned_children:
        node_id = str(child.get("node_id") or "")
        if not node_id:
            failures.append("spawned AAS5 participant is missing node_id")
            continue
        seen_node_ids.add(node_id)
        artifact_ref = str(child.get("artifact_ref") or "")
        if not artifact_ref:
            failures.append(f"{node_id} must record artifact_ref")
            continue
        child_payload = _load_json_artifact(repo_root=repo_root, ref=artifact_ref)
        if child_payload is None:
            failures.append(f"{node_id} artifact_ref must point to parseable JSON")
            continue
        if str(child_payload.get("status") or "").upper() == "PLANNED":
            failures.append(f"{node_id} child artifact must not remain PLANNED")
        provenance = child_payload.get("artifact_provenance") or {}
        if str(provenance.get("writer_mode") or "") == "bootstrap_placeholder":
            failures.append(f"{node_id} child artifact must not remain bootstrap_placeholder provenance")
        if str(provenance.get("owner_node_id") or "") not in {"", node_id}:
            failures.append(f"{node_id} child artifact owner_node_id must match node_id")
        _validate_model_audit(child_payload.get("model_audit") or {}, failures, f"{node_id}.model_audit")

    expected_non_parent = {*manager_ids, *reporter_ids, *auditor_ids, *worker_ids}
    if seen_node_ids != expected_non_parent:
        failures.append("spawned_children node ids must match the 24 non-parent TEAM_PLAN participants exactly")

    recommendation_authorized = payload.get("recommendation_authorized") is True
    degraded_acknowledged = _degraded_mode_acknowledged(repo_root=repo_root, task_id=task_id)
    if parallelism:
        batch_count = int(parallelism.get("batch_count") or 0)
        runtime_limit_evidence = list(parallelism.get("runtime_limit_evidence") or [])
        if batch_count > 1 and recommendation_authorized and not (runtime_limit_evidence or degraded_acknowledged):
            failures.append("AAS5 batched ideation may not authorize recommendation without runtime evidence or degraded acknowledgement")
    if recommendation_authorized and future_branch_report and future_branch_report.get("recommendation_authorized") is not True:
        failures.append("FUTURE_BRANCH_REPORT.json must agree when SWARM_EXECUTION_RECORD.json authorizes recommendation")
    if recommendation_authorized and failures:
        failures.append("AAS5 recommendation_authorized must remain false while validation failures remain")
    return failures


def _validate_model_audit(model_audit: dict[str, Any], failures: list[str], label: str) -> None:
    auditability = str(
        model_audit.get("observed_model_auditability")
        or model_audit.get("auditability")
        or ""
    ).strip()
    if auditability not in MODEL_AUDITABILITY_STATES:
        failures.append(f"{label} must use an allowed observed_model_auditability")
    if auditability == "unknown_unresolved":
        failures.append(f"{label} may not remain unknown_unresolved")


def _degraded_mode_acknowledged(*, repo_root: Path, task_id: str) -> bool:
    record_path = repo_root / "docs" / "task_workspaces" / task_id / "HUMAN_DECISION_RECORD.json"
    if not record_path.exists():
        return False
    try:
        payload = json.loads(record_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if payload.get("degraded_mode_acknowledged") is True or payload.get("degraded_aas5_acknowledged") is True:
        return True
    decision = str(payload.get("operator_decision") or "").upper()
    return "ACK_DEGRADED_AAS5" in decision


def _artifact_ref_exists(*, repo_root: Path, ref: str) -> bool:
    return _artifact_path(repo_root=repo_root, ref=ref).exists()


def _artifact_path(*, repo_root: Path, ref: str) -> Path:
    normalized = ref.replace("\\", "/").strip().lstrip("/")
    if not normalized:
        return repo_root / "__missing__"
    return repo_root / Path(normalized)


def _load_json_artifact(*, repo_root: Path, ref: str) -> dict[str, Any] | None:
    path = _artifact_path(repo_root=repo_root, ref=ref)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_yaml_artifact(*, repo_root: Path, ref: str) -> dict[str, Any] | None:
    path = _artifact_path(repo_root=repo_root, ref=ref)
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return None


def _load_required_json(*, repo_root: Path, ref: str, failures: list[str], label: str) -> dict[str, Any] | None:
    if not _artifact_ref_exists(repo_root=repo_root, ref=ref):
        failures.append(f"{label} must exist")
        return None
    payload = _load_json_artifact(repo_root=repo_root, ref=ref)
    if payload is None:
        failures.append(f"{label} must contain parseable JSON")
        return None
    return payload


def _load_required_json_or_yaml(*, repo_root: Path, ref: str, failures: list[str], label: str) -> dict[str, Any] | None:
    if not _artifact_ref_exists(repo_root=repo_root, ref=ref):
        failures.append(f"{label} must exist")
        return None
    payload = _load_json_artifact(repo_root=repo_root, ref=ref)
    if payload is not None:
        return payload
    payload = _load_yaml_artifact(repo_root=repo_root, ref=ref)
    if payload is None:
        failures.append(f"{label} must contain parseable YAML or JSON")
    return payload
