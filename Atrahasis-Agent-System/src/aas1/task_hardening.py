from __future__ import annotations

import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from aas1.aas5_ideation import (
    ADVERSARIAL_INTEGRITY_REVIEW,
    AUTHORITY_COVERAGE_AUDIT,
    AAS5_DOCTRINE_VERSION,
    AAS5_IDEATION_AGENT_COUNT,
    AAS5_IDEATION_TEAM_MODE,
    AAS5_NON_PARENT_NODE_COUNT,
    AAS5_TOPOLOGY_MODE,
    EXECUTION_PARALLELISM_RECORD,
    LANE_IDS,
    RUNTIME_AUDIT_RECORD,
    SWARM_COMPLIANCE_AUDIT,
    SWARM_TOPOLOGY_GRAPH,
    audit_artifact_path,
    auditor_nodes,
    build_aas5_batches,
    build_aas5_ideation_nodes,
    build_audit_payload,
    build_execution_parallelism_payload,
    build_lane_plan_payload,
    build_lane_report_payload,
    build_model_audit,
    build_artifact_provenance,
    build_topology_graph_payload,
    lane_manager,
    lane_plan_path,
    lane_report_path,
    lane_reporter,
    lane_worker_node_ids,
    make_run_key,
)
from aas1.artifact_registry import ArtifactRegistry
from aas1.common import ensure_dir, load_json, load_yaml, utc_now, write_text
from aas1.command_modifier_router import CommandModifierRouter
from aas1.task_claim_coordinator import TaskClaimCoordinator
from aas1.task_id_policy import TaskIdPolicy
from aas1.workflow_policy_engine import (
    future_exploration_for,
    improvement_trigger_policy_for,
    radical_redesign_policy_for,
)


TASK_ID_RE = re.compile(r"T-\d+")
NAMED_AUTHORITY_SURFACE_RE = re.compile(r"\b(?:C\d+|T-[A-Z0-9-]+)\b", re.IGNORECASE)
TODO_TASK_ROW_RE = re.compile(r"^\|\s*`?(T-[A-Z0-9-]+)`?\s*\|", re.IGNORECASE)
NEXT_DISPATCHABLE_RE = re.compile(
    r"Next dispatchable canonical (?P<kind>task|tranche):\s*(?P<body>.+)",
    re.IGNORECASE,
)
UDO_SECTION_RE = re.compile(
    r"## User Dispatch Order \(Simple\)\n(?P<body>.*?)(?:\n---|\Z)",
    re.DOTALL,
)
UDO_LINE_RE = re.compile(r"^\s*(?P<index>\d+)\.\s+(?P<body>.+)$")

TASK_START_CHECKLIST = "TASK_START_CHECKLIST.json"
DIRECT_SPEC_AUDIT_RECORD = "DIRECT_SPEC_AUDIT_RECORD.json"
DIRECT_SPEC_VERIFICATION_REPORT = "DIRECT_SPEC_VERIFICATION_REPORT.json"
CLOSEOUT_CONSISTENCY_REPORT = "CLOSEOUT_CONSISTENCY_REPORT.json"
AUTHORITY_COVERAGE_MATRIX = "AUTHORITY_COVERAGE_MATRIX.json"
COMMAND_REQUEST = "COMMAND_REQUEST.yaml"
HUMAN_DECISION_RECORD = "HUMAN_DECISION_RECORD.json"
WORKFLOW_RUN_RECORD = "WORKFLOW_RUN_RECORD.json"
TEAM_PLAN = "TEAM_PLAN.yaml"
FUTURE_BRANCH_REPORT = "FUTURE_BRANCH_REPORT.json"
CHILD_RESULT_MERGE_PACKAGE = "CHILD_RESULT_MERGE_PACKAGE.json"
SWARM_EXECUTION_RECORD = "SWARM_EXECUTION_RECORD.json"
DEFAULT_LIVE_CHILD_CAP = 6

BASELINE_WORKSPACE_FILES = ["README.md", "TASK_BRIEF.md", TASK_START_CHECKLIST]
TASK_CLASS_REQUIRED_ARTIFACTS = {
    "FULL_PIPELINE": BASELINE_WORKSPACE_FILES + ["TEAM_PLAN.yaml", SWARM_EXECUTION_RECORD],
    "DIRECT_SPEC": BASELINE_WORKSPACE_FILES
    + [DIRECT_SPEC_AUDIT_RECORD, DIRECT_SPEC_VERIFICATION_REPORT, CLOSEOUT_CONSISTENCY_REPORT],
    "GOVERNANCE": BASELINE_WORKSPACE_FILES + [CLOSEOUT_CONSISTENCY_REPORT],
    "ANALYSIS": BASELINE_WORKSPACE_FILES,
    "PACKAGING": BASELINE_WORKSPACE_FILES + [CLOSEOUT_CONSISTENCY_REPORT],
    "VALIDATION": BASELINE_WORKSPACE_FILES,
    "DEMO": BASELINE_WORKSPACE_FILES,
}
TASK_CLASS_VALIDATORS = {
    "FULL_PIPELINE": ["workspace", "swarm_execution"],
    "DIRECT_SPEC": ["workspace", "direct_spec_verification", "closeout_consistency"],
    "GOVERNANCE": ["workspace", "closeout_consistency"],
    "ANALYSIS": ["workspace"],
    "PACKAGING": ["workspace", "closeout_consistency"],
    "VALIDATION": ["workspace"],
    "DEMO": ["workspace"],
}
TASK_CLASS_STOP_RULES = {
    "FULL_PIPELINE": [
        "Stop after IDEATION and wait for explicit concept approval before promotion.",
        "Do not mint any C-xxx invention id before HITL approval is recorded.",
        "Stop again if convergence or adversarial review is required by policy.",
        "When ideation is architecture-heavy or operator-requested as a swarm, form a real child swarm; do not substitute internal roleplay.",
        "Ordinary FULL PIPELINE / IDEATION defaults to a real Alpha/Beta/Gamma/Radical future-branch swarm rather than a smaller viewpoint-only readout.",
        f"Do not treat ideation as complete until {FUTURE_BRANCH_REPORT} and {SWARM_EXECUTION_RECORD} both record a satisfied real future-branch swarm.",
        "Do not present an ideation recommendation or swarm readout until validate_swarm_execution_record.py passes.",
        "Operator instructions such as 'do not edit shared state yet' do not prohibit a noncanonical analysis-band T-900x workspace; they prohibit canonical shared-state progression.",
    ],
    "DIRECT_SPEC": [
        "Do not stop at progress checkpoints; continue until blocked, HITL-gated, or ready for assessment/closeout.",
        "Do not claim a scoped purge or terminology sweep is clean until DIRECT_SPEC_VERIFICATION_REPORT.json records clean=true.",
        "Do not mark the task DONE until CLOSEOUT_CONSISTENCY_REPORT.json records valid=true.",
    ],
    "GOVERNANCE": [
        "Do not change parser-consumed shared-doc formats without preserving compatibility or updating the consuming code in the same task.",
        "Do not mark the task DONE until CLOSEOUT_CONSISTENCY_REPORT.json records valid=true.",
    ],
    "ANALYSIS": [
        "Stop when the analysis verdict is ready or when a HITL gate requires operator choice.",
    ],
    "PACKAGING": [
        "Do not mark the task DONE until CLOSEOUT_CONSISTENCY_REPORT.json records valid=true.",
    ],
    "VALIDATION": [
        "Stop when validation evidence and findings are complete.",
    ],
    "DEMO": [
        "Stop when the demo artifact or walkthrough is complete.",
    ],
}
DIRECT_SPEC_PATTERN_HINTS = {
    "bridge": "bridge",
    "a2a": "A2A",
    "mcp": "MCP",
    "asv": "ASV",
}
DEFAULT_AUTHORITY_INPUTS = [
    "docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v5.md",
    "docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v4.md",
    "docs/SESSION_BRIEF.md",
    "docs/AGENT_STATE.md",
    "docs/TODO.md",
    "docs/DECISIONS.md",
    "docs/platform_overlays/SHARED_OPERATING_MODEL.md",
    "docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md",
    "docs/platform_overlays/codex/RUNTIME.md",
]


def normalize_task_id(task_id: str) -> str:
    token = task_id.strip().upper()
    if not TASK_ID_RE.fullmatch(token):
        raise ValueError(f"Invalid task id: {task_id}")
    return token


def _require_ideation_future_policy() -> dict[str, Any]:
    policy = future_exploration_for("FULL_PIPELINE", "IDEATION")
    if policy is None:
        raise ValueError("FULL_PIPELINE / IDEATION future-branch policy is not configured.")
    return policy


def _slugify_branch_token(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-").lower()


def _branch_artifact_path(*, branch: dict[str, Any]) -> str:
    lane_id = str(branch.get("lane_id") or "lane")
    parent_role = str(branch.get("parent_role") or "child")
    branch_kind = str(branch.get("branch_kind") or "branch")
    return f"children/{lane_id}__{parent_role}__{branch_kind}.json"


def _branch_child_id(*, dispatch_id: str, branch: dict[str, Any]) -> str:
    return f"{dispatch_id}-{_slugify_branch_token(str(branch.get('branch_id') or 'branch'))}"


def _branch_objective(*, branch: dict[str, Any], title: str) -> str:
    return f"{str(branch.get('objective') or '').strip()} Apply that branch specifically to '{title}'."


def _build_ideation_branch_specs(
    *,
    task_id: str,
    dispatch_id: str,
    future_policy: dict[str, Any],
) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for branch in future_policy.get("branches", []):
        branch_payload = dict(branch)
        artifact_path = _branch_artifact_path(branch=branch_payload)
        specs.append(
            {
                "branch_id": str(branch_payload.get("branch_id") or ""),
                "parent_role": str(branch_payload.get("parent_role") or ""),
                "branch_kind": str(branch_payload.get("branch_kind") or ""),
                "branch_label": str(branch_payload.get("branch_label") or ""),
                "lane_id": str(branch_payload.get("lane_id") or ""),
                "lane_label": str(branch_payload.get("lane_label") or ""),
                "lane_strategy": str(branch_payload.get("lane_strategy") or ""),
                "objective": str(branch_payload.get("objective") or ""),
                "radical_candidate": bool(branch_payload.get("radical_candidate")),
                "artifact_path": artifact_path,
                "artifact_ref": f"docs/task_workspaces/{task_id}/{artifact_path}",
                "child_id": _branch_child_id(dispatch_id=dispatch_id, branch=branch_payload),
            }
        )
    return specs


def _build_lane_manager_specs(*, task_id: str, branch_specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in branch_specs:
        lane_id = str(item.get("lane_id") or "")
        if not lane_id:
            continue
        grouped.setdefault(lane_id, []).append(item)
    managers: list[dict[str, Any]] = []
    for lane_id, children in grouped.items():
        lane_label = str(children[0].get("lane_label") or lane_id.title())
        lane_strategy = str(children[0].get("lane_strategy") or "")
        manager_id = f"manager:{lane_id}"
        managers.append(
            {
                "manager_id": manager_id,
                "agent_name": f"pending-{lane_id}-manager",
                "role": "lane_manager",
                "tier": "future_lane_manager",
                "lane_id": lane_id,
                "lane_label": lane_label,
                "lane_strategy": lane_strategy,
                "model": "gpt-5.4",
                "reasoning_effort": "high",
                "objective": (
                    f"Own the {lane_label} branch lane for task {task_id}, keep its three leaf agents independent, "
                    "and manage lane-local convergence without taking over final parent authority."
                ),
                "permission": "read_only",
                "safe_zone_paths": [f"docs/task_workspaces/{task_id}/"],
                "managed_branch_ids": [str(child.get('branch_id') or '') for child in children],
                "managed_child_ids": [str(child.get('child_id') or '') for child in children],
                "managed_child_count": len(children),
                "status": "PLANNED",
            }
        )
    managers.sort(key=lambda item: str(item.get("lane_id") or ""))
    return managers


def parse_todo_dispatch_state(todo_text: str) -> dict[str, Any]:
    task_rows = _parse_task_rows(todo_text)
    next_dispatchable = _parse_next_dispatchable(todo_text)
    user_dispatch_entries = _parse_user_dispatch_entries(todo_text)
    ordered_ids: list[str] = []
    for entry in user_dispatch_entries:
        for task_id in entry["task_ids"]:
            if task_id not in ordered_ids:
                ordered_ids.append(task_id)
    return {
        "task_rows": task_rows,
        "next_dispatchable": next_dispatchable,
        "user_dispatch_entries": user_dispatch_entries,
        "user_dispatch_order": ordered_ids,
    }


def load_todo_dispatch_state(repo_root: Path) -> dict[str, Any]:
    todo_path = repo_root / "docs" / "TODO.md"
    return parse_todo_dispatch_state(todo_path.read_text(encoding="utf-8"))


def infer_task_class(*, todo_type: str, claim: dict[str, Any] | None = None) -> str:
    normalized_type = (todo_type or "").strip().upper().replace(" ", "_")
    if normalized_type in {"FULL_PIPELINE", "FULL_SYSTEM_DESIGN"}:
        return "FULL_PIPELINE"
    if normalized_type in {"DIRECT_SPEC", "DIRECT_SPEC_EDIT"}:
        return "DIRECT_SPEC"
    if normalized_type == "GOVERNANCE":
        return "GOVERNANCE"
    if normalized_type == "PACKAGING":
        return "PACKAGING"
    pipeline_type = str(((claim or {}).get("scope") or {}).get("pipeline_type") or "").strip().upper()
    if pipeline_type in {"DIRECT_EDIT", "DIRECT_SPEC"}:
        return "DIRECT_SPEC"
    if pipeline_type == "GOVERNANCE":
        return "GOVERNANCE"
    if pipeline_type == "PACKAGING":
        return "PACKAGING"
    return "ANALYSIS"


def prepare_task(
    repo_root: Path,
    *,
    task_id: str,
    agent_name: str | None = None,
    override_patterns: list[str] | None = None,
) -> dict[str, Any]:
    task_id = normalize_task_id(task_id)
    dispatch_state = load_todo_dispatch_state(repo_root)
    task_row = dispatch_state["task_rows"].get(task_id) or {}
    claim = load_claim(repo_root, task_id)
    task_class = infer_task_class(todo_type=str(task_row.get("type") or ""), claim=claim)
    workspace_root = ensure_dir(repo_root / "docs" / "task_workspaces" / task_id)
    created: list[str] = []

    readme_path = workspace_root / "README.md"
    if not readme_path.exists():
        write_text(readme_path, build_workspace_readme(task_id=task_id, task_class=task_class))
        created.append(_rel(repo_root, readme_path))

    task_brief_path = workspace_root / "TASK_BRIEF.md"
    if not task_brief_path.exists():
        write_text(
            task_brief_path,
            build_task_brief(
                repo_root=repo_root,
                task_id=task_id,
                task_class=task_class,
                task_row=task_row,
                claim=claim,
                dispatch_state=dispatch_state,
            ),
        )
        created.append(_rel(repo_root, task_brief_path))

    checklist = build_task_start_checklist(
        repo_root=repo_root,
        task_id=task_id,
        task_class=task_class,
        task_row=task_row,
        claim=claim,
        agent_name=agent_name,
        dispatch_state=dispatch_state,
    )
    registry = ArtifactRegistry(repo_root)
    checklist_path = registry.write_json_artifact(
        task_id,
        TASK_START_CHECKLIST,
        checklist,
        schema_name="task_start_checklist",
    )
    created.append(_rel(repo_root, checklist_path))

    if task_class == "DIRECT_SPEC":
        audit_record = build_direct_spec_audit_record(
            repo_root=repo_root,
            task_id=task_id,
            task_row=task_row,
            claim=claim,
            override_patterns=override_patterns,
        )
        audit_path = registry.write_json_artifact(
            task_id,
            DIRECT_SPEC_AUDIT_RECORD,
            audit_record,
            schema_name="direct_spec_audit_record",
        )
        created.append(_rel(repo_root, audit_path))

    return {
        "task_id": task_id,
        "task_class": task_class,
        "workspace_path": f"docs/task_workspaces/{task_id}",
        "artifacts_written": created,
        "checklist_ref": f"docs/task_workspaces/{task_id}/{TASK_START_CHECKLIST}",
        "task_brief_ref": f"docs/task_workspaces/{task_id}/TASK_BRIEF.md",
        "dispatchable": checklist["readiness_checks"]["dispatchable_now"],
        "claim_status": (claim or {}).get("status"),
        "write_surface": checklist["write_surface"],
    }


def prepare_idea_task(
    repo_root: Path,
    *,
    title: str,
    prompt: str,
    agent_name: str | None = None,
    authority_surfaces: list[str] | None = None,
    requested_task_id: str | None = None,
    operator_constraints: list[str] | None = None,
) -> dict[str, Any]:
    clean_title = title.strip()
    clean_prompt = prompt.strip()
    if not clean_title:
        raise ValueError("Idea title is required.")
    if not clean_prompt:
        raise ValueError("Idea prompt is required.")
    command_request = asdict(
        CommandModifierRouter().parse(
            modifier="AASNI",
            prompt=clean_prompt,
            task_id=requested_task_id or "T-9000",
            operator_constraints=list(operator_constraints or []),
        )
    )
    effective_prompt = str(command_request.get("prompt") or clean_prompt).strip()
    effective_constraints = list(command_request.get("operator_constraints") or [])
    normalized_surfaces = _normalize_named_surfaces(
        list(authority_surfaces or []) + _extract_named_surfaces_from_prompt(effective_prompt)
    )
    effective_agent_name = _infer_parent_agent_name(repo_root=repo_root, agent_name=agent_name)

    task_id_policy = TaskIdPolicy(repo_root)
    task_id, _task_band, auto_minted = task_id_policy.resolve(
        modifier="AASNI",
        requested_task_id=requested_task_id,
        task_class="analysis",
    )
    dispatch_state = load_todo_dispatch_state(repo_root)
    workspace_root = ensure_dir(repo_root / "docs" / "task_workspaces" / task_id)
    registry = ArtifactRegistry(repo_root)
    created: list[str] = []
    now = utc_now()
    workflow_id = _workflow_token(task_id=task_id, modifier="AASNI", timestamp=now)
    dispatch_id = f"{task_id}-IDEATION-{now.replace(':', '').replace('-', '')}"
    active_claims = _active_claims(repo_root)
    parallel_mode_active = any(True for _item in active_claims)
    future_policy = _require_ideation_future_policy()
    branch_specs = _build_ideation_branch_specs(
        task_id=task_id,
        dispatch_id=dispatch_id,
        future_policy=future_policy,
    )
    run_key = make_run_key(task_id, workflow_id)
    aas5_nodes = build_aas5_ideation_nodes(
        task_id=task_id,
        branch_specs=branch_specs,
        title=clean_title,
    )
    lane_ids = [lane_id for lane_id in (future_policy.get("lane_order") or []) if lane_manager(aas5_nodes, lane_id)]
    lane_plan_artifacts = [lane_plan_path(lane_id) for lane_id in lane_ids]
    lane_report_artifacts = [lane_report_path(lane_id) for lane_id in lane_ids]
    audit_artifacts = [audit_artifact_path(item.audit_domain or "") for item in auditor_nodes(aas5_nodes)]
    participant_artifacts = [node.expected_artifact for node in aas5_nodes]
    command_request["task_id"] = task_id

    readme_path = workspace_root / "README.md"
    if not readme_path.exists():
        write_text(
            readme_path,
            build_idea_workspace_readme(task_id=task_id, title=clean_title, authority_surfaces=normalized_surfaces),
        )
        created.append(_rel(repo_root, readme_path))

    task_brief_path = workspace_root / "TASK_BRIEF.md"
    if not task_brief_path.exists():
        write_text(
            task_brief_path,
            build_idea_task_brief(
                task_id=task_id,
                title=clean_title,
                prompt=effective_prompt,
                authority_surfaces=normalized_surfaces,
                dispatch_state=dispatch_state,
                branch_specs=branch_specs,
            ),
        )
        created.append(_rel(repo_root, task_brief_path))

    checklist = {
        "type": "TASK_START_CHECKLIST",
        "task_id": task_id,
        "task_class": "FULL_PIPELINE",
        "title": clean_title,
        "generated_at": now,
        "agent_name": effective_agent_name,
        "next_dispatchable_summary": (dispatch_state.get("next_dispatchable") or {}).get("raw"),
        "readiness_checks": {
            "task_listed": False,
            "dependencies_resolved": True,
            "claim_conflict": False,
            "dispatchable_now": True,
            "parallel_mode_active": parallel_mode_active,
        },
        "write_surface": {
            "mode": "exploratory_task_workspace",
            "paths": [f"docs/task_workspaces/{task_id}/"],
            "source": "AASNI_auto_mint",
        },
        "required_artifacts": [
            "README.md",
            "TASK_BRIEF.md",
            TASK_START_CHECKLIST,
            COMMAND_REQUEST,
            HUMAN_DECISION_RECORD,
            WORKFLOW_RUN_RECORD,
            AUTHORITY_COVERAGE_MATRIX,
            TEAM_PLAN,
            FUTURE_BRANCH_REPORT,
            SWARM_EXECUTION_RECORD,
            CHILD_RESULT_MERGE_PACKAGE,
            SWARM_TOPOLOGY_GRAPH,
            EXECUTION_PARALLELISM_RECORD,
            *lane_plan_artifacts,
            *lane_report_artifacts,
            *audit_artifacts,
            *participant_artifacts,
        ],
        "validators": ["workspace", "swarm_execution"],
        "stop_rules": list(TASK_CLASS_STOP_RULES["FULL_PIPELINE"]),
        "dependency_ids": [],
        "unresolved_dependencies": [],
        "claim_conflicts": [],
        "source_refs": {
            "todo": "docs/TODO.md",
            "claim": "",
            "workspace": f"docs/task_workspaces/{task_id}/",
        },
        "notes": [
            "This exploratory ideation run is still a real AAS5 task workspace and may not remain session-only.",
            "Read the contents of current claim YAML files before ideation so the swarm has parallel-context awareness.",
            "Run the full AAS5 25-agent ordinary ideation topology and persist one participant artifact per non-parent node before presenting a recommendation.",
            "A noncanonical T-900x workspace is allowed here and does not count as canonical shared-state progression.",
            "If validate_swarm_execution_record.py does not pass, do not present a recommendation; report noncompliance instead.",
            "Update the placeholder ideation artifacts before presenting a final recommendation.",
            f"Plan the AAS5 swarm in deliberate waves of at most {DEFAULT_LIVE_CHILD_CAP} live children so runtime caps are handled deliberately rather than by spawn failure.",
        ],
    }
    if "STRICT_FULL_PIPELINE_TASK" in effective_constraints:
        checklist["notes"].append(
            "Prompt modifier `Full Pipeline Task:` detected. Judgment-call downgrade to parent-only advisory mode is forbidden."
        )
    checklist_path = registry.write_json_artifact(
        task_id,
        TASK_START_CHECKLIST,
        checklist,
        schema_name="task_start_checklist",
    )
    created.append(_rel(repo_root, checklist_path))

    command_request_path = registry.write_yaml_artifact(
        task_id,
        COMMAND_REQUEST,
        command_request,
        schema_name="command_request",
    )
    created.append(_rel(repo_root, command_request_path))

    human_decision = build_placeholder_human_decision_record(
        task_id=task_id,
        prompt=effective_prompt,
        authority_surfaces=normalized_surfaces,
        operator_constraints=effective_constraints,
    )
    human_decision_path = registry.write_json_artifact(
        task_id,
        HUMAN_DECISION_RECORD,
        human_decision,
        schema_name="human_decision_record",
    )
    created.append(_rel(repo_root, human_decision_path))

    authority_matrix = build_placeholder_authority_coverage_matrix(
        task_id=task_id,
        authority_surfaces=normalized_surfaces,
        generated_at=now,
    )
    authority_matrix["doctrine_version"] = AAS5_DOCTRINE_VERSION
    authority_matrix["workflow_id"] = workflow_id
    authority_matrix["run_key"] = run_key
    authority_matrix_path = registry.write_json_artifact(
        task_id,
        AUTHORITY_COVERAGE_MATRIX,
        authority_matrix,
        schema_name="authority_coverage_matrix",
    )
    created.append(_rel(repo_root, authority_matrix_path))

    team_plan = build_placeholder_team_plan(
        task_id=task_id,
        title=clean_title,
        agent_name=effective_agent_name,
        workflow_id=workflow_id,
        dispatch_id=dispatch_id,
        run_key=run_key,
        authority_surfaces=normalized_surfaces,
        generated_at=now,
        future_policy=future_policy,
        branch_specs=branch_specs,
        aas5_nodes=aas5_nodes,
    )
    team_plan_path = registry.write_yaml_artifact(
        task_id,
        TEAM_PLAN,
        team_plan,
        schema_name="team_plan",
    )
    created.append(_rel(repo_root, team_plan_path))

    future_branch_report = build_placeholder_future_branch_report(
        task_id=task_id,
        workflow_id=workflow_id,
        dispatch_id=dispatch_id,
        run_key=run_key,
        generated_at=now,
        future_policy=future_policy,
        branch_specs=branch_specs,
        aas5_nodes=aas5_nodes,
    )
    future_branch_report_path = registry.write_json_artifact(
        task_id,
        FUTURE_BRANCH_REPORT,
        future_branch_report,
        schema_name="future_branch_report",
    )
    created.append(_rel(repo_root, future_branch_report_path))

    child_artifact_paths: list[str] = []
    for node in aas5_nodes:
        child_result = build_placeholder_child_result(
            task_id=task_id,
            workflow_id=workflow_id,
            run_key=run_key,
            node=node,
            title=clean_title,
            parent_agent_name=effective_agent_name,
        )
        child_path = registry.write_json_artifact(
            task_id,
            node.expected_artifact,
            child_result,
            schema_name="child_agent_result",
        )
        child_artifact_paths.append(_rel(repo_root, child_path))
        created.append(_rel(repo_root, child_path))

    for lane_id in lane_ids:
        manager = lane_manager(aas5_nodes, lane_id)
        reporter = lane_reporter(aas5_nodes, lane_id)
        if manager is None or reporter is None:
            continue
        worker_ids = lane_worker_node_ids(aas5_nodes, lane_id)
        lane_label = str(manager.lane_label or lane_id.title())
        lane_strategy = str(manager.lane_strategy or "")
        lane_plan_payload = build_lane_plan_payload(
            task_id=task_id,
            workflow_id=workflow_id,
            run_key=run_key,
            lane_id=lane_id,
            lane_label=lane_label,
            lane_strategy=lane_strategy,
            manager_id=manager.node_id,
            worker_node_ids=worker_ids,
            reporter_node_id=reporter.node_id,
            generated_at=now,
        )
        lane_plan_path_ref = registry.write_yaml_artifact(
            task_id,
            lane_plan_path(lane_id),
            lane_plan_payload,
            schema_name="lane_plan",
        )
        created.append(_rel(repo_root, lane_plan_path_ref))
        lane_report_payload = build_lane_report_payload(
            task_id=task_id,
            workflow_id=workflow_id,
            run_key=run_key,
            lane_id=lane_id,
            lane_label=lane_label,
            reporter_node_id=reporter.node_id,
            worker_node_ids=worker_ids,
            generated_at=now,
        )
        lane_report_path_ref = registry.write_json_artifact(
            task_id,
            lane_report_path(lane_id),
            lane_report_payload,
            schema_name="lane_convergence_report",
        )
        created.append(_rel(repo_root, lane_report_path_ref))

    audit_type_map = {
        "compliance": "SWARM_COMPLIANCE_AUDIT",
        "runtime": "RUNTIME_AUDIT_RECORD",
        "authority": "AUTHORITY_COVERAGE_AUDIT",
        "adversarial": "ADVERSARIAL_INTEGRITY_REVIEW",
    }
    audit_gate_map = {
        "compliance": ["All 25 AAS5 topology nodes must be real and independently represented before recommendation."],
        "runtime": ["Runtime accounting and requested-vs-observed model routing must be recorded before recommendation."],
        "authority": ["Every named authority surface must be covered before recommendation."],
        "adversarial": ["Adversarial sufficiency must be explicitly reviewed before recommendation."],
    }
    for auditor in auditor_nodes(aas5_nodes):
        domain = str(auditor.audit_domain or "")
        audit_payload = build_audit_payload(
            artifact_type=audit_type_map.get(domain, "AAS5_AUDIT_RECORD"),
            task_id=task_id,
            workflow_id=workflow_id,
            run_key=run_key,
            owner_node_id=auditor.node_id,
            generated_at=now,
            summary=f"Pending {domain or 'audit'} review.",
            blocking_gates=audit_gate_map.get(domain, ["Audit must complete before recommendation."]),
        )
        audit_path_ref = registry.write_json_artifact(
            task_id,
            audit_artifact_path(domain),
            audit_payload,
            schema_name="aas5_audit_record",
        )
        created.append(_rel(repo_root, audit_path_ref))

    topology_graph = build_topology_graph_payload(
        task_id=task_id,
        workflow_id=workflow_id,
        run_key=run_key,
        generated_at=now,
        nodes=aas5_nodes,
    )
    topology_graph_path = registry.write_json_artifact(
        task_id,
        SWARM_TOPOLOGY_GRAPH,
        topology_graph,
        schema_name="swarm_topology_graph",
    )
    created.append(_rel(repo_root, topology_graph_path))

    parallelism_record = build_execution_parallelism_payload(
        task_id=task_id,
        workflow_id=workflow_id,
        run_key=run_key,
        generated_at=now,
        nodes=aas5_nodes,
        max_live_children=DEFAULT_LIVE_CHILD_CAP,
    )
    parallelism_path = registry.write_json_artifact(
        task_id,
        EXECUTION_PARALLELISM_RECORD,
        parallelism_record,
        schema_name="execution_parallelism_record",
    )
    created.append(_rel(repo_root, parallelism_path))

    merge_package = build_placeholder_child_result_merge_package(
        task_id=task_id,
        workflow_id=workflow_id,
        dispatch_id=dispatch_id,
        run_key=run_key,
        aas5_nodes=aas5_nodes,
        lane_ids=lane_ids,
    )
    merge_package_path = registry.write_json_artifact(
        task_id,
        CHILD_RESULT_MERGE_PACKAGE,
        merge_package,
        schema_name="child_result_merge_package",
    )
    created.append(_rel(repo_root, merge_package_path))

    swarm_execution = build_placeholder_swarm_execution_record(
        task_id=task_id,
        generated_at=now,
        agent_name=effective_agent_name,
        future_policy=future_policy,
        workflow_id=workflow_id,
        run_key=run_key,
        branch_specs=branch_specs,
        aas5_nodes=aas5_nodes,
        team_plan_ref=f"docs/task_workspaces/{task_id}/{TEAM_PLAN}",
        merge_package_ref=f"docs/task_workspaces/{task_id}/{CHILD_RESULT_MERGE_PACKAGE}",
        topology_graph_ref=f"docs/task_workspaces/{task_id}/{SWARM_TOPOLOGY_GRAPH}",
        parallelism_record_ref=f"docs/task_workspaces/{task_id}/{EXECUTION_PARALLELISM_RECORD}",
    )
    swarm_execution_path = registry.write_json_artifact(
        task_id,
        SWARM_EXECUTION_RECORD,
        swarm_execution,
        schema_name="swarm_execution_record",
    )
    created.append(_rel(repo_root, swarm_execution_path))

    workflow_record = build_placeholder_workflow_run_record(
        task_id=task_id,
        workflow_id=workflow_id,
        command_request=command_request,
        generated_at=now,
        future_policy=future_policy,
        branch_specs=branch_specs,
        run_key=run_key,
        aas5_nodes=aas5_nodes,
        lane_ids=lane_ids,
    )
    workflow_record_path = registry.write_json_artifact(
        task_id,
        WORKFLOW_RUN_RECORD,
        workflow_record,
        schema_name="workflow_run_record",
    )
    created.append(_rel(repo_root, workflow_record_path))

    return {
        "task_id": task_id,
        "task_class": "FULL_PIPELINE",
        "modifier": "AASNI",
        "workspace_path": f"docs/task_workspaces/{task_id}",
        "auto_minted": auto_minted,
        "expected_team_mode": future_policy.get("team_mode"),
        "expected_branch_count": len(branch_specs),
        "expected_node_count": len(aas5_nodes) + 1,
        "expected_branch_ids": [item["branch_id"] for item in branch_specs],
        "artifacts_written": created,
        "authority_surfaces": normalized_surfaces,
        "notes": [
            "Exploratory FULL PIPELINE ideation now has a real T-900x workspace anchor.",
            "Replace the placeholder AAS5 ideation artifacts before treating the ideation stage as complete.",
            "A compliant ideation recommendation is blocked until validate_swarm_execution_record.py passes.",
        ],
    }


def verify_direct_spec_task(
    repo_root: Path,
    *,
    task_id: str,
    override_patterns: list[str] | None = None,
    allow_patterns: list[str] | None = None,
) -> dict[str, Any]:
    task_id = normalize_task_id(task_id)
    claim = load_claim(repo_root, task_id)
    workspace_root = repo_root / "docs" / "task_workspaces" / task_id
    audit_path = workspace_root / DIRECT_SPEC_AUDIT_RECORD
    audit_record = load_json(audit_path) if audit_path.exists() else {}
    scope_paths = _resolve_scope_paths(repo_root, claim=claim, task_id=task_id)
    forbidden_patterns = (
        list(override_patterns or [])
        or list(audit_record.get("forbidden_patterns") or [])
        or infer_direct_spec_patterns(task_row={}, claim=claim)
    )
    compiled_allow = [re.compile(item, re.IGNORECASE) for item in (allow_patterns or [])]
    matches: list[dict[str, Any]] = []
    checked_files: list[dict[str, Any]] = []
    for relative_path in scope_paths:
        absolute_path = repo_root / relative_path
        if not absolute_path.exists() or absolute_path.is_dir():
            continue
        checked_files.append(
            {
                "path": relative_path,
                "size_bytes": absolute_path.stat().st_size,
            }
        )
        text = absolute_path.read_text(encoding="utf-8", errors="replace")
        for pattern in forbidden_patterns:
            for line_number, line in enumerate(text.splitlines(), start=1):
                if re.search(pattern, line, re.IGNORECASE):
                    if any(allow.search(line) for allow in compiled_allow):
                        continue
                    matches.append(
                        {
                            "path": relative_path,
                            "pattern": pattern,
                            "line_number": line_number,
                            "line_text": line.strip()[:240],
                        }
                    )

    report = {
        "type": "DIRECT_SPEC_VERIFICATION_REPORT",
        "task_id": task_id,
        "generated_at": utc_now(),
        "scope_paths": scope_paths,
        "forbidden_patterns": forbidden_patterns,
        "checked_files": checked_files,
        "match_count": len(matches),
        "matches": matches,
        "clean": len(matches) == 0,
        "notes": _direct_spec_verification_notes(
            scope_paths=scope_paths,
            checked_files=checked_files,
            forbidden_patterns=forbidden_patterns,
            matches=matches,
        ),
    }
    ArtifactRegistry(repo_root).write_json_artifact(
        task_id,
        DIRECT_SPEC_VERIFICATION_REPORT,
        report,
        schema_name="direct_spec_verification_report",
    )
    return report


def validate_closeout_consistency(repo_root: Path, *, task_id: str) -> dict[str, Any]:
    task_id = normalize_task_id(task_id)
    dispatch_state = load_todo_dispatch_state(repo_root)
    task_row = dispatch_state["task_rows"].get(task_id) or {}
    claim = load_claim(repo_root, task_id)
    task_class = infer_task_class(todo_type=str(task_row.get("type") or ""), claim=claim)
    workspace_root = repo_root / "docs" / "task_workspaces" / task_id
    verification_path = workspace_root / DIRECT_SPEC_VERIFICATION_REPORT
    verification = load_json(verification_path) if verification_path.exists() else None
    live_handoffs = sorted((repo_root / "docs" / "handoffs").glob(f"{task_id}_*_HANDOFF.md"))
    applied_handoffs = sorted((repo_root / "docs" / "handoffs" / "applied").glob(f"{task_id}_*_HANDOFF.md"))
    checklist_path = workspace_root / TASK_START_CHECKLIST

    checks = [
        _check_result(
            "workspace_present",
            workspace_root.exists(),
            f"Task workspace {'exists' if workspace_root.exists() else 'is missing'}.",
        ),
        _check_result(
            "task_brief_present",
            (workspace_root / "TASK_BRIEF.md").exists(),
            f"TASK_BRIEF.md {'exists' if (workspace_root / 'TASK_BRIEF.md').exists() else 'is missing'}.",
        ),
        _check_result(
            "task_start_checklist_present",
            checklist_path.exists(),
            f"{TASK_START_CHECKLIST} {'exists' if checklist_path.exists() else 'is missing'}.",
        ),
        _check_result(
            "claim_present",
            claim is not None,
            "Claim file loaded." if claim is not None else "Claim file is missing.",
        ),
    ]

    if task_class == "DIRECT_SPEC":
        checks.append(
            _check_result(
                "direct_spec_audit_present",
                (workspace_root / DIRECT_SPEC_AUDIT_RECORD).exists(),
                f"{DIRECT_SPEC_AUDIT_RECORD} {'exists' if (workspace_root / DIRECT_SPEC_AUDIT_RECORD).exists() else 'is missing'}.",
            )
        )
        checks.append(
            _check_result(
                "direct_spec_verification_clean",
                bool(verification) and bool(verification.get("clean")),
                "Direct-spec verification is clean."
                if verification and verification.get("clean")
                else "Direct-spec verification is missing or not clean.",
            )
        )

    task_in_dispatch_order = any(task_id in entry["task_ids"] for entry in dispatch_state["user_dispatch_entries"])
    claim_status = str((claim or {}).get("status") or "")
    checks.append(
        _check_result(
            "done_claim_removed_from_dispatch_order",
            claim_status != "DONE" or not task_in_dispatch_order,
            "DONE task no longer appears in User Dispatch Order."
            if claim_status == "DONE" and not task_in_dispatch_order
            else "DONE task still appears in User Dispatch Order." if claim_status == "DONE" else "Claim is not DONE yet.",
        )
    )
    checks.append(
        _check_result(
            "no_live_handoff_when_done",
            claim_status != "DONE" or not live_handoffs,
            "No live handoff remains for a DONE task."
            if claim_status == "DONE" and not live_handoffs
            else "Live handoff remains and closeout is not yet fully applied." if claim_status == "DONE" else "Claim is not DONE yet.",
        )
    )
    checks.append(
        _check_result(
            "applied_handoff_consistent",
            claim_status != "DONE" or bool(applied_handoffs) or not live_handoffs,
            "Applied handoff found or no handoff was required."
            if claim_status == "DONE" and (applied_handoffs or not live_handoffs)
            else "DONE task has a live handoff but no applied handoff yet.",
        )
    )

    valid = all(item["passed"] for item in checks)
    report = {
        "type": "CLOSEOUT_CONSISTENCY_REPORT",
        "task_id": task_id,
        "task_class": task_class,
        "generated_at": utc_now(),
        "claim_status": claim_status or None,
        "workspace_present": workspace_root.exists(),
        "handoff_status": {
            "live_exists": bool(live_handoffs),
            "live_paths": [_rel(repo_root, path) for path in live_handoffs],
            "applied_exists": bool(applied_handoffs),
            "applied_paths": [_rel(repo_root, path) for path in applied_handoffs],
        },
        "checks": checks,
        "valid": valid,
        "notes": [
            "Closeout consistency requires claim, workspace, dispatch-order, and handoff state to agree.",
            "This report is machine-oriented and should be regenerated immediately before declaring DONE.",
        ],
    }
    ArtifactRegistry(repo_root).write_json_artifact(
        task_id,
        CLOSEOUT_CONSISTENCY_REPORT,
        report,
        schema_name="closeout_consistency_report",
    )
    return report


def load_claim(repo_root: Path, task_id: str) -> dict[str, Any] | None:
    claim_path = repo_root / "docs" / "task_claims" / f"{task_id}.yaml"
    if not claim_path.exists():
        return None
    payload = load_yaml(claim_path)
    return payload if isinstance(payload, dict) else None


def build_task_start_checklist(
    *,
    repo_root: Path,
    task_id: str,
    task_class: str,
    task_row: dict[str, Any],
    claim: dict[str, Any] | None,
    agent_name: str | None,
    dispatch_state: dict[str, Any],
) -> dict[str, Any]:
    active_claims = _active_claims(repo_root)
    scope_paths = _resolve_scope_paths(repo_root, claim=claim, task_id=task_id)
    dependency_ids = _extract_task_ids(str(task_row.get("dependencies") or ""))
    unresolved_dependencies = [dep for dep in dependency_ids if dep in dispatch_state["task_rows"]]
    first_dispatch_entry = dispatch_state["user_dispatch_entries"][0] if dispatch_state["user_dispatch_entries"] else None
    dispatchable_now = bool(task_row) and not unresolved_dependencies
    if first_dispatch_entry and task_id not in first_dispatch_entry["task_ids"]:
        dispatchable_now = False
    if claim and claim.get("status") == "DONE":
        dispatchable_now = False
    conflicts = _claim_conflicts(
        task_id=task_id,
        scope_paths=scope_paths,
        active_claims=active_claims,
        agent_name=agent_name,
    )
    if conflicts:
        dispatchable_now = False

    return {
        "type": "TASK_START_CHECKLIST",
        "task_id": task_id,
        "task_class": task_class,
        "title": task_row.get("title") or (claim or {}).get("title"),
        "generated_at": utc_now(),
        "agent_name": agent_name,
        "next_dispatchable_summary": (dispatch_state["next_dispatchable"] or {}).get("raw"),
        "readiness_checks": {
            "task_listed": bool(task_row),
            "dependencies_resolved": not unresolved_dependencies,
            "claim_conflict": bool(conflicts),
            "dispatchable_now": dispatchable_now,
            "parallel_mode_active": any(item.get("task_id") != task_id for item in active_claims),
        },
        "write_surface": {
            "mode": "claim_safe_zone" if claim else "task_workspace_only",
            "paths": scope_paths or [f"docs/task_workspaces/{task_id}/"],
            "source": "claim" if claim else "workspace_fallback",
        },
        "required_artifacts": list(TASK_CLASS_REQUIRED_ARTIFACTS.get(task_class, BASELINE_WORKSPACE_FILES)),
        "validators": list(TASK_CLASS_VALIDATORS.get(task_class, ["workspace"])),
        "stop_rules": list(TASK_CLASS_STOP_RULES.get(task_class, [])),
        "dependency_ids": dependency_ids,
        "unresolved_dependencies": unresolved_dependencies,
        "claim_conflicts": conflicts,
        "source_refs": {
            "todo": "docs/TODO.md",
            "claim": f"docs/task_claims/{task_id}.yaml" if claim else "",
            "workspace": f"docs/task_workspaces/{task_id}/",
        },
        "notes": _checklist_notes(task_class=task_class, dispatchable_now=dispatchable_now, conflicts=conflicts),
    }


def build_direct_spec_audit_record(
    *,
    repo_root: Path,
    task_id: str,
    task_row: dict[str, Any],
    claim: dict[str, Any] | None,
    override_patterns: list[str] | None = None,
) -> dict[str, Any]:
    scope_paths = _resolve_scope_paths(repo_root, claim=claim, task_id=task_id)
    forbidden_patterns = list(override_patterns or []) or infer_direct_spec_patterns(task_row=task_row, claim=claim)
    return {
        "type": "DIRECT_SPEC_AUDIT_RECORD",
        "task_id": task_id,
        "task_class": "DIRECT_SPEC",
        "generated_at": utc_now(),
        "target_specs": list((claim or {}).get("target_specs") or _infer_target_specs(scope_paths)),
        "scope_paths": scope_paths,
        "authority_inputs": list(DEFAULT_AUTHORITY_INPUTS),
        "forbidden_patterns": forbidden_patterns,
        "verification_rule": "All forbidden patterns must be absent from the exact claimed scope before the task may be marked clean or DONE.",
        "notes": [
            "This record exists to make direct-spec verification reproducible and scope-bound.",
            "Override forbidden patterns explicitly if the task requires a narrower or broader lexical sweep.",
        ],
    }


def build_workspace_readme(*, task_id: str, task_class: str) -> str:
    return "\n".join(
        [
            f"# Task Workspace: {task_id}",
            "",
            f"This workspace is the canonical task-local audit surface for `{task_id}`.",
            f"Current hardening profile: `{task_class}`.",
            "",
            "Use this folder to record task-start readiness, scoped verification, and closeout consistency.",
        ]
    )


def build_idea_workspace_readme(*, task_id: str, title: str, authority_surfaces: list[str]) -> str:
    lines = [
        f"# Task Workspace: {task_id}",
        "",
        f"Purpose: exploratory `AASNI` ideation for `{title}`.",
        "",
        "Execution notes:",
        f"- `{task_id}` is an analysis-band exploratory task in the `T-9000` range.",
        "- This run is not a canonical backlog claim and must not modify `docs/TODO.md` unless explicitly promoted later.",
        "- Even as an exploratory run, ideation must persist its workspace, swarm, and authority-coverage artifacts here.",
    ]
    if authority_surfaces:
        lines.extend(["", "Named authority surfaces:"])
        for surface in authority_surfaces:
            lines.append(f"- `{surface}`")
    return "\n".join(lines)


def build_task_brief(
    *,
    repo_root: Path,
    task_id: str,
    task_class: str,
    task_row: dict[str, Any],
    claim: dict[str, Any] | None,
    dispatch_state: dict[str, Any],
) -> str:
    scope_paths = _resolve_scope_paths(repo_root, claim=claim, task_id=task_id)
    stop_rules = TASK_CLASS_STOP_RULES.get(task_class, [])
    lines = [
        f"# TASK_BRIEF: {task_id}",
        "",
        f"## Title",
        task_row.get("title") or (claim or {}).get("title") or task_id,
        "",
        "## Classification",
        f"- Task class: `{task_class}`",
        f"- TODO type: `{task_row.get('type') or 'UNKNOWN'}`",
        f"- Priority: `{task_row.get('priority') or 'UNKNOWN'}`",
        f"- Dependencies: `{task_row.get('dependencies') or 'none'}`",
        "",
        "## Canonical Write Surface",
    ]
    for path in scope_paths or [f"docs/task_workspaces/{task_id}/"]:
        lines.append(f"- `{path}`")
    lines.extend(
        [
            "",
            "## Dispatch Context",
            f"- Next dispatchable summary: {(dispatch_state['next_dispatchable'] or {}).get('raw') or 'n/a'}",
            "",
            "## Required Local Artifacts",
        ]
    )
    for filename in TASK_CLASS_REQUIRED_ARTIFACTS.get(task_class, BASELINE_WORKSPACE_FILES):
        lines.append(f"- `{filename}`")
    lines.extend(["", "## Stop Rules"])
    for rule in stop_rules:
        lines.append(f"- {rule}")
    return "\n".join(lines)


def build_idea_task_brief(
    *,
    task_id: str,
    title: str,
    prompt: str,
    authority_surfaces: list[str],
    dispatch_state: dict[str, Any],
    branch_specs: list[dict[str, Any]],
) -> str:
    lines = [
        f"# TASK_BRIEF: {task_id}",
        "",
        "## Title",
        title,
        "",
        "## Classification",
        "- Task class: `FULL_PIPELINE`",
        "- Modifier: `AASNI`",
        "- Mode: `exploratory candidate ideation`",
        "- Canonical backlog task: `no`",
        "",
        "## Operator Prompt",
        prompt,
        "",
        "## Workspace Rule",
        "This idea may not remain session-only. Use this workspace as the canonical audit surface for ideation, real child swarm evidence, and operator choice.",
        "This noncanonical T-900x workspace is task-local audit state, not canonical shared-state progression in TODO/claims/handoffs.",
        "",
        "## Required Ideation Artifacts",
        f"- `{COMMAND_REQUEST}`",
        f"- `{HUMAN_DECISION_RECORD}`",
        f"- `{WORKFLOW_RUN_RECORD}`",
        f"- `{AUTHORITY_COVERAGE_MATRIX}`",
        f"- `{TEAM_PLAN}`",
        f"- `{FUTURE_BRANCH_REPORT}`",
        f"- `{SWARM_EXECUTION_RECORD}`",
        f"- `{CHILD_RESULT_MERGE_PACKAGE}`",
        *[f"- `{item['artifact_path']}`" for item in branch_specs],
        "",
        "## Read-First Constraints",
        "- Resolve named spec ids to their real titled paths before reading them.",
        "- Read the contents of current claim YAML files before ideation so the swarm sees parallel work already underway.",
        "- Stop after ideation and wait for operator choice before promotion.",
        "- Use the default Alpha/Beta/Gamma/Radical future-branch swarm for this ideation task; do not silently fall back to a smaller 3-role team.",
        "- If the workspace, coverage matrix, or swarm validator is incomplete, do not present an ideation recommendation; report the missing compliance gate instead.",
        "",
        "## Dispatch Context",
        f"- Current canonical next dispatchable summary: {(dispatch_state.get('next_dispatchable') or {}).get('raw') or 'n/a'}",
    ]
    if authority_surfaces:
        lines.extend(["", "## Named Authority Surfaces"])
        for surface in authority_surfaces:
            lines.append(f"- `{surface}`")
    return "\n".join(lines)


def infer_direct_spec_patterns(*, task_row: dict[str, Any], claim: dict[str, Any] | None) -> list[str]:
    text = " ".join(
        [
            str(task_row.get("title") or ""),
            str(task_row.get("notes") or ""),
            str((claim or {}).get("notes") or ""),
        ]
    ).lower()
    patterns = [regex for marker, regex in DIRECT_SPEC_PATTERN_HINTS.items() if marker in text]
    return patterns


def _parse_task_rows(todo_text: str) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for line in todo_text.splitlines():
        if not TODO_TASK_ROW_RE.match(line.strip()):
            continue
        parts = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
        if len(parts) < 2:
            continue
        rows[parts[0]] = {
            "task_id": parts[0],
            "title": parts[1] if len(parts) > 1 else "",
            "type": parts[2] if len(parts) > 2 else "",
            "priority": parts[3] if len(parts) > 3 else "",
            "dependencies": parts[4] if len(parts) > 4 else "",
            "notes": parts[5] if len(parts) > 5 else "",
        }
    return rows


def _parse_next_dispatchable(todo_text: str) -> dict[str, Any] | None:
    for line in todo_text.splitlines():
        match = NEXT_DISPATCHABLE_RE.search(line)
        if not match:
            continue
        body = match.group("body").strip().rstrip(".")
        return {
            "kind": match.group("kind").lower(),
            "raw": body,
            "label": _dispatch_label(body),
            "task_ids": _extract_task_ids(body),
        }
    return None


def _parse_user_dispatch_entries(todo_text: str) -> list[dict[str, Any]]:
    match = UDO_SECTION_RE.search(todo_text)
    if not match:
        return []
    entries: list[dict[str, Any]] = []
    for line in match.group("body").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        line_match = UDO_LINE_RE.match(stripped)
        if not line_match:
            continue
        body = line_match.group("body").strip()
        entries.append(
            {
                "index": int(line_match.group("index")),
                "raw": body,
                "label": _dispatch_label(body),
                "task_ids": _extract_task_ids(body),
            }
        )
    return entries


def _dispatch_label(body: str) -> str | None:
    if " - " in body:
        return body.split(" - ", 1)[0].strip().strip("`")
    return None


def _extract_task_ids(text: str) -> list[str]:
    ordered: list[str] = []
    for match in TASK_ID_RE.findall(text.upper()):
        if match not in ordered:
            ordered.append(match)
    return ordered


def _active_claims(repo_root: Path) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    claims_root = repo_root / "docs" / "task_claims"
    if not claims_root.exists():
        return claims
    for path in sorted(claims_root.glob("*.yaml")):
        if path.name == "CLAIM_TEMPLATE.yaml":
            continue
        try:
            payload = load_yaml(path)
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        if payload.get("status") in TaskClaimCoordinator.ACTIVE_STATUSES:
            claims.append(payload)
    return claims


def _resolve_scope_paths(repo_root: Path, *, claim: dict[str, Any] | None, task_id: str) -> list[str]:
    if claim:
        safe_zone_paths = list((((claim or {}).get("scope") or {}).get("safe_zone_paths") or []))
        if safe_zone_paths:
            return [_normalize_repo_path(item) for item in safe_zone_paths]
        target_specs = list((claim or {}).get("target_specs") or [])
        if target_specs:
            return _spec_paths_for_ids(repo_root, target_specs)
    return [f"docs/task_workspaces/{task_id}/"]


def _spec_paths_for_ids(repo_root: Path, spec_ids: list[str]) -> list[str]:
    resolved: list[str] = []
    specs_root = repo_root / "docs" / "specifications"
    for spec_id in spec_ids:
        pattern = f"{spec_id}*"
        for spec_dir in sorted(specs_root.glob(pattern)):
            if not spec_dir.is_dir():
                continue
            for candidate in sorted(spec_dir.glob("*MASTER*SPEC*.md")):
                relative = _rel(repo_root, candidate)
                if relative not in resolved:
                    resolved.append(relative)
    return resolved


def _claim_conflicts(
    *,
    task_id: str,
    scope_paths: list[str],
    active_claims: list[dict[str, Any]],
    agent_name: str | None,
) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    normalized_scope = [_normalize_repo_path(item) for item in scope_paths]
    for payload in active_claims:
        other_task_id = str(payload.get("task_id") or "")
        if other_task_id == task_id:
            other_agent = str(payload.get("agent_name") or "")
            if (
                str(payload.get("status") or "").upper() in TaskClaimCoordinator.ACTIVE_STATUSES
                and agent_name
                and other_agent
                and other_agent != agent_name
            ):
                conflicts.append(
                    {
                        "task_id": other_task_id,
                        "agent_name": other_agent,
                        "reason": "task is already actively claimed by another agent",
                    }
                )
            continue
        for other_path in list(((payload.get("scope") or {}).get("safe_zone_paths") or [])):
            normalized_other = _normalize_repo_path(other_path)
            if any(_paths_overlap(item, normalized_other) for item in normalized_scope):
                conflicts.append(
                    {
                        "task_id": other_task_id,
                        "agent_name": payload.get("agent_name"),
                        "reason": f"overlapping safe zone: {normalized_other}",
                    }
                )
                break
    return conflicts


def _paths_overlap(left: str, right: str) -> bool:
    if left == right:
        return True
    return left.startswith(right.rstrip("/") + "/") or right.startswith(left.rstrip("/") + "/")


def _normalize_repo_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def _checklist_notes(*, task_class: str, dispatchable_now: bool, conflicts: list[dict[str, Any]]) -> list[str]:
    notes = []
    if not dispatchable_now:
        notes.append("Task is not dispatchable yet; resolve the listed blockers before claiming or editing.")
    if conflicts:
        notes.append("Active claim conflicts were detected on the write surface.")
    if task_class == "FULL_PIPELINE":
        notes.append("Architecture-heavy ideation must use a real child swarm with TEAM_PLAN.yaml, SWARM_EXECUTION_RECORD.json, and CHILD_RESULT_MERGE_PACKAGE.json.")
        notes.append("Run validate_swarm_execution_record.py before treating a swarm ideation stage as complete.")
    if task_class == "DIRECT_SPEC":
        notes.append("Run verify_direct_spec_task.py before declaring the claimed surface clean.")
        notes.append("Run validate_task_closeout_consistency.py before marking the claim DONE.")
    return notes


def _direct_spec_verification_notes(
    *,
    scope_paths: list[str],
    checked_files: list[dict[str, Any]],
    forbidden_patterns: list[str],
    matches: list[dict[str, Any]],
) -> list[str]:
    notes = [
        f"Checked {len(checked_files)} file(s) across the exact claimed scope.",
        f"Forbidden patterns: {', '.join(forbidden_patterns) if forbidden_patterns else 'none declared'}.",
    ]
    if not scope_paths:
        notes.append("No scope paths were available; verification coverage is incomplete.")
    if matches:
        notes.append("Clean=false because forbidden-pattern matches remain in the claimed scope.")
    else:
        notes.append("Clean=true for the declared forbidden patterns across the claimed scope.")
    return notes


def _infer_target_specs(scope_paths: list[str]) -> list[str]:
    specs = []
    for path in scope_paths:
        for spec_id in re.findall(r"/(C\d+)[^/]*?/", path.replace("\\", "/")):
            if spec_id not in specs:
                specs.append(spec_id)
    return specs


def _check_result(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": passed,
        "detail": detail,
    }


def _rel(repo_root: Path, path: Path) -> str:
    return str(path.relative_to(repo_root)).replace("\\", "/")


def _normalize_named_surfaces(authority_surfaces: list[str]) -> list[str]:
    normalized: list[str] = []
    for item in authority_surfaces:
        token = item.strip().upper()
        if token and token not in normalized:
            normalized.append(token)
    return normalized


def _extract_named_surfaces_from_prompt(prompt: str) -> list[str]:
    return _normalize_named_surfaces([match.group(0) for match in NAMED_AUTHORITY_SURFACE_RE.finditer(prompt or "")])


def _infer_parent_agent_name(*, repo_root: Path, agent_name: str | None) -> str | None:
    explicit_name = str(agent_name or "").strip()
    if explicit_name:
        return explicit_name
    agent_state_path = repo_root / "docs" / "AGENT_STATE.md"
    if not agent_state_path.exists():
        return None
    try:
        agent_state = load_yaml(agent_state_path) or {}
    except Exception:
        return None
    active_sessions = agent_state.get("active_sessions") or []
    for item in reversed(active_sessions):
        if not isinstance(item, dict):
            continue
        session_name = str(item.get("agent_name") or "").strip()
        status = str(item.get("status") or "").strip().upper()
        if session_name and status == "ACTIVE":
            return session_name
    return None


def _planned_swarm_batches(total_children: int, *, live_child_cap: int = DEFAULT_LIVE_CHILD_CAP) -> dict[str, int | str]:
    planned_cap = max(1, min(live_child_cap, max(total_children, 1)))
    planned_wave_count = max(1, (max(total_children, 1) + planned_cap - 1) // planned_cap)
    return {
        "scheduling_mode": "batched_by_runtime_cap",
        "max_live_children": planned_cap,
        "spawn_batch_size": planned_cap,
        "planned_wave_count": planned_wave_count,
    }


def _workflow_token(*, task_id: str, modifier: str, timestamp: str) -> str:
    compact = timestamp.replace(":", "").replace("-", "")
    return f"{task_id}-{modifier}-{compact}"


def _model_audit(
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


def build_placeholder_human_decision_record(
    *,
    task_id: str,
    prompt: str,
    authority_surfaces: list[str],
    operator_constraints: list[str],
) -> dict[str, Any]:
    priority_zones = authority_surfaces or ["architecture"]
    constraints = list(operator_constraints)
    if not constraints:
        constraints.append("Do not promote this exploratory idea into canonical shared work without explicit operator direction.")
    blocking_gates = [
        f"{AUTHORITY_COVERAGE_MATRIX} must address every named authority surface.",
        f"{FUTURE_BRANCH_REPORT} must record the full AAS5 ordinary ideation topology and lane convergence state.",
        f"{SWARM_EXECUTION_RECORD} must be satisfied and validate_swarm_execution_record.py must pass before any recommendation is presented.",
        f"{SWARM_TOPOLOGY_GRAPH} and {EXECUTION_PARALLELISM_RECORD} must record the realized topology and runtime/accounting state before recommendation.",
    ]
    if "STRICT_FULL_PIPELINE_TASK" in constraints:
        blocking_gates.append(
            "The operator used the strict `Full Pipeline Task:` modifier. Parent-only advisory analysis is forbidden; either run the real ABGR swarm or report noncompliance."
        )
    return {
        "decision_type": "OPERATOR_GUIDANCE",
        "task_id": task_id,
        "workflow_status": "BLOCKED_PENDING_SWARM_VALIDATION",
        "prompt": prompt,
        "research_strategy_summary": "Exploratory AASNI ideation. Do not request operator path selection until real swarm evidence and authority coverage are complete.",
        "evidence_summary": {
            "modifier": "AASNI",
            "priority_zones": priority_zones,
            "contradiction_count": 0,
            "strategy_summary": "Use the AAS5 25-agent ideation topology, record authority coverage and runtime truth, validate swarm execution, and stop after ideation for operator choice.",
        },
        "options": [],
        "operator_actions": [
            {
                "label": "choose_path",
                "instruction": "Select one ideation path or reject the candidate entirely.",
            }
        ],
        "operator_decision": "PENDING",
        "recommendation_authorized": False,
        "blocking_gates": blocking_gates,
        "constraints": constraints,
    }


def build_placeholder_authority_coverage_matrix(
    *,
    task_id: str,
    authority_surfaces: list[str],
    generated_at: str,
) -> dict[str, Any]:
    return {
        "type": "AUTHORITY_COVERAGE_MATRIX",
        "task_id": task_id,
        "stage": "IDEATION",
        "generated_at": generated_at,
        "coverage_required": bool(authority_surfaces),
        "recommendation_blocked_until_complete": True,
        "named_authority_surfaces": authority_surfaces,
        "surface_rows": [
            {
                "surface": surface,
                "current_authority": "Pending ideation coverage.",
                "coverage_status": "MISSING",
                "disposition": "not_applicable",
                "new_authority_needed": False,
                "notes": [
                    "Replace this placeholder row after reading the resolved authority surface.",
                ],
            }
            for surface in authority_surfaces
        ],
        "new_semantic_authority_test": {
            "verdict": "pending",
            "rationale": "Pending ideation analysis.",
            "affected_modules": [],
            "follow_on_task_shapes": [],
        },
        "notes": [
            "This placeholder exists so exploratory ideation cannot remain session-only.",
            "Do not finalize the recommendation until every named surface is addressed.",
        ],
    }


def build_placeholder_team_plan(
    *,
    task_id: str,
    title: str,
    agent_name: str | None,
    workflow_id: str,
    dispatch_id: str,
    run_key: str,
    authority_surfaces: list[str],
    generated_at: str,
    future_policy: dict[str, Any],
    branch_specs: list[dict[str, Any]],
    aas5_nodes: list[Any],
) -> dict[str, Any]:
    batches = build_aas5_batches(aas5_nodes, max_live_children=DEFAULT_LIVE_CHILD_CAP)
    context_refs = [
        "docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v5.md",
        "docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v4.md",
        "docs/SESSION_BRIEF.md",
        "docs/DECISIONS.md",
        "docs/TODO.md",
        f"docs/task_workspaces/{task_id}/TASK_BRIEF.md",
    ]
    for surface in authority_surfaces:
        if surface not in context_refs:
            context_refs.append(surface)
    improvement_policy = improvement_trigger_policy_for("FULL_PIPELINE", "IDEATION") or {
        "enabled": True,
        "trigger_reasons": ["task_class_has_design_surface"],
        "decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"],
        "lane_ids": list(future_policy.get("lane_ids") or []),
        "lane_order": list(future_policy.get("lane_order") or []),
    }
    radical_policy = radical_redesign_policy_for("FULL_PIPELINE", "IDEATION") or {
        "enabled": True,
        "trigger_reasons": ["stage_supports_core_assumption_rewrite"],
        "decision_options": ["reject", "hybridize", "promote"],
        "radical_branch_ids": [
            item["branch_id"] for item in branch_specs if item.get("lane_id") == "radical" or item.get("radical_candidate")
        ],
    }
    managers = [item for item in aas5_nodes if item.tier == "lane_manager"]
    workers = [item for item in aas5_nodes if item.tier == "lane_worker"]
    reporters = [item for item in aas5_nodes if item.tier == "lane_reporter"]
    auditors = [item for item in aas5_nodes if item.tier == "auditor"]
    ordered_children = [*managers, *workers, *reporters, *auditors]

    def _participant(node: Any, *, routing_basis: str) -> dict[str, Any]:
        return {
            "node_id": node.node_id,
            "parent_node_id": node.parent_node_id,
            "agent_name": f"pending-{node.node_id.replace('.', '-')}",
            "role": node.role,
            "role_label": node.role_label,
            "tier": node.tier,
            "lane_id": node.lane_id,
            "lane_label": node.lane_label,
            "lane_strategy": node.lane_strategy,
            "audit_domain": node.audit_domain,
            "batch_label": node.batch_label,
            "model": node.requested_model,
            "reasoning_effort": node.requested_reasoning_effort,
            "model_audit": _model_audit(
                policy_target=node.requested_model,
                actual_runtime_model=None,
                reasoning_effort=node.requested_reasoning_effort,
                auditability="runtime_not_exposed",
                routing_basis=routing_basis,
            ),
            "objective": node.objective,
            "permission": "read_only",
            "safe_zone_paths": [f"docs/task_workspaces/{task_id}/"],
            "expected_artifact": node.expected_artifact,
            "expected_artifact_ref": f"docs/task_workspaces/{task_id}/{node.expected_artifact}",
            "branch_id": node.branch_id,
            "branch_label": node.branch_label,
            "branch_kind": node.branch_kind,
            "status": "PLANNED",
        }

    return {
        "version": "2.0",
        "doctrine_version": AAS5_DOCTRINE_VERSION,
        "topology_mode": AAS5_TOPOLOGY_MODE,
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "dispatch_id": dispatch_id,
        "status": "PLANNED",
        "created_at": generated_at,
        "updated_at": generated_at,
        "selection": {
            "action_label": "explore_futures",
            "instruction": "future_swarm:ideation",
            "spawn_id": dispatch_id,
            "program_title": title,
            "target_domain": "architecture",
            "program_goal": str(future_policy.get("program_goal") or ""),
            "priority_score": 1,
        },
        "parent": {
            "node_id": "mst",
            "provider": "codex",
            "agent_name": agent_name or "pending-parent-agent",
            "session_id": "pending-parent-session",
            "role": "master_orchestrator",
            "role_label": "Master Orchestrator",
            "merge_owner": agent_name or "pending-parent-agent",
            "model": "gpt-5.4",
            "reasoning_effort": "xhigh",
            "model_audit": _model_audit(
                policy_target="gpt-5.4",
                actual_runtime_model=None,
                reasoning_effort="xhigh",
                auditability="runtime_not_exposed",
                routing_basis="Codex MODEL_ROUTING primary director policy target for AAS5 ideation orchestration.",
            ),
        },
        "spawn_policy": {
            "team_mode": AAS5_IDEATION_TEAM_MODE,
            "orchestration_topology": "master_lane_managers_reporters_auditors",
            "manager_count": len(managers),
            "reporter_count": len(reporters),
            "auditor_count": len(auditors),
            "worker_count": len(workers),
            "total_non_parent_participants": len(aas5_nodes),
            "total_agents": AAS5_IDEATION_AGENT_COUNT,
            "simultaneous_target_agent_count": AAS5_IDEATION_AGENT_COUNT,
            "max_children": len(aas5_nodes),
            "max_live_children": DEFAULT_LIVE_CHILD_CAP,
            "spawn_batch_size": DEFAULT_LIVE_CHILD_CAP,
            "planned_wave_count": len(batches),
            "batch_count": len(batches),
            "scheduling_mode": "batched_by_runtime_cap",
            "default_child_permission": "read_only",
            "hitl_gate_owner": "parent",
            "shared_state_owner": "parent",
            "execution_parallelism_mode": "degraded_batched",
        },
        "manager_orchestrators": [
            {
                **_participant(
                    item,
                    routing_basis="AAS5 lane-manager routing target for ordinary FULL_PIPELINE / IDEATION.",
                ),
                "manager_id": item.node_id,
                "managed_child_ids": [node.node_id for node in workers if node.parent_node_id == item.node_id],
                "managed_branch_ids": [str(node.branch_id or "") for node in workers if node.parent_node_id == item.node_id],
                "managed_child_count": sum(1 for node in workers if node.parent_node_id == item.node_id),
            }
            for item in managers
        ],
        "lane_convergence_reporters": [
            _participant(
                item,
                routing_basis="AAS5 lane convergence reporter routing target for ordinary FULL_PIPELINE / IDEATION.",
            )
            for item in reporters
        ],
        "audit_orchestrators": [
            _participant(
                item,
                routing_basis="AAS5 audit-role routing target for ordinary FULL_PIPELINE / IDEATION.",
            )
            for item in auditors
        ],
        "workers": [
            _participant(
                item,
                routing_basis="AAS5 branch-worker routing target for ordinary FULL_PIPELINE / IDEATION.",
            )
            for item in workers
        ],
        "context_refs": context_refs,
        "children": [
            _participant(
                item,
                routing_basis="AAS5 non-parent participant routing target for ordinary FULL_PIPELINE / IDEATION.",
            )
            for item in ordered_children
        ],
        "future_exploration": {
            "enabled": True,
            "current_stage": "IDEATION",
            "max_depth": int(future_policy.get("max_depth") or 2),
            "convergence_owner": "mst",
            "convergence_artifact": f"docs/task_workspaces/{task_id}/{FUTURE_BRANCH_REPORT}",
            "branch_report_ref": f"docs/task_workspaces/{task_id}/{FUTURE_BRANCH_REPORT}",
            "topology_graph_ref": f"docs/task_workspaces/{task_id}/{SWARM_TOPOLOGY_GRAPH}",
            "parallelism_record_ref": f"docs/task_workspaces/{task_id}/{EXECUTION_PARALLELISM_RECORD}",
            "lane_plan_refs": {lane_id: f"docs/task_workspaces/{task_id}/{lane_plan_path(lane_id)}" for lane_id in LANE_IDS},
            "lane_report_refs": {lane_id: f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}" for lane_id in LANE_IDS},
            "audit_refs": {
                "compliance": f"docs/task_workspaces/{task_id}/{SWARM_COMPLIANCE_AUDIT}",
                "runtime": f"docs/task_workspaces/{task_id}/{RUNTIME_AUDIT_RECORD}",
                "authority": f"docs/task_workspaces/{task_id}/{AUTHORITY_COVERAGE_AUDIT}",
                "adversarial": f"docs/task_workspaces/{task_id}/{ADVERSARIAL_INTEGRITY_REVIEW}",
            },
            "improvement_trigger_policy": improvement_policy,
            "radical_trigger_policy": radical_policy,
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
                    "expected_artifact": item["artifact_ref"],
                    "worker_node_id": next(
                        (node.node_id for node in workers if node.branch_id == item["branch_id"]),
                        None,
                    ),
                    "radical_candidate": bool(item["radical_candidate"]),
                    "status": "PLANNED",
                }
                for item in branch_specs
            ],
        },
        "notes": [
            "Read current claim YAML contents before spawning children so the swarm has parallel-context awareness.",
            "Replace planned participant metadata with actual session identifiers after spawn and keep node ids stable.",
            "AAS5 ordinary ideation uses one master, four lane managers, twelve workers, four lane reporters, and four independent auditors.",
            f"Plan participant spawning in {len(batches)} wave(s) of up to {DEFAULT_LIVE_CHILD_CAP} live children to respect the live runtime cap.",
        ],
    }


def build_placeholder_future_branch_report(
    *,
    task_id: str,
    workflow_id: str,
    dispatch_id: str,
    run_key: str,
    generated_at: str,
    future_policy: dict[str, Any],
    branch_specs: list[dict[str, Any]],
    aas5_nodes: list[Any],
) -> dict[str, Any]:
    workers = [item for item in aas5_nodes if item.tier == "lane_worker"]
    return {
        "type": "FUTURE_BRANCH_REPORT",
        "doctrine_version": AAS5_DOCTRINE_VERSION,
        "topology_mode": AAS5_TOPOLOGY_MODE,
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "dispatch_id": dispatch_id,
        "team_mode": AAS5_IDEATION_TEAM_MODE,
        "current_stage": "IDEATION",
        "convergence_owner": "mst",
        "convergence_artifact": f"docs/task_workspaces/{task_id}/{CHILD_RESULT_MERGE_PACKAGE}",
        "recommendation_authorized": False,
        "blocking_gates": [
            "The full AAS5 25-agent ordinary ideation topology must complete with real session results.",
            f"Run validate_swarm_execution_record.py {task_id} before presenting a recommendation.",
        ],
        "improvement_trigger_policy": improvement_trigger_policy_for("FULL_PIPELINE", "IDEATION"),
        "radical_trigger_policy": radical_redesign_policy_for("FULL_PIPELINE", "IDEATION"),
        "lane_report_refs": {lane_id: f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}" for lane_id in LANE_IDS},
        "audit_refs": {
            "compliance": f"docs/task_workspaces/{task_id}/{SWARM_COMPLIANCE_AUDIT}",
            "runtime": f"docs/task_workspaces/{task_id}/{RUNTIME_AUDIT_RECORD}",
            "authority": f"docs/task_workspaces/{task_id}/{AUTHORITY_COVERAGE_AUDIT}",
            "adversarial": f"docs/task_workspaces/{task_id}/{ADVERSARIAL_INTEGRITY_REVIEW}",
        },
        "lane_summaries": [
            {
                "lane_id": lane_id,
                "lane_label": next((item.lane_label for item in workers if item.lane_id == lane_id), lane_id.title()),
                "status": "PLANNED",
                "worker_node_ids": [item.node_id for item in workers if item.lane_id == lane_id],
                "reporter_node_id": next(
                    (item.node_id for item in aas5_nodes if item.tier == "lane_reporter" and item.lane_id == lane_id),
                    None,
                ),
                "lane_report_ref": f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}",
            }
            for lane_id in LANE_IDS
        ],
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
                "expected_artifact": item["artifact_ref"],
                "worker_node_id": next(
                    (node.node_id for node in workers if node.branch_id == item["branch_id"]),
                    None,
                ),
                "radical_candidate": bool(item["radical_candidate"]),
                "status": "PLANNED",
            }
            for item in branch_specs
        ],
        "created_at": generated_at,
        "updated_at": generated_at,
    }


def build_placeholder_child_result(
    *,
    task_id: str,
    workflow_id: str,
    run_key: str,
    node: Any,
    title: str,
    parent_agent_name: str | None,
) -> dict[str, Any]:
    payload = {
        "type": "CHILD_AGENT_RESULT",
        "doctrine_version": AAS5_DOCTRINE_VERSION,
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "node_id": node.node_id,
        "parent_node_id": node.parent_node_id,
        "role": node.role,
        "role_label": node.role_label,
        "objective": f"{node.objective} Apply that role specifically to '{title}'.",
        "status": "PLANNED",
        "session_identity": {
            "agent_name": f"pending-{node.node_id.replace('.', '-')}",
            "session_id": None,
            "provider": "codex",
            "role": node.role,
        },
        "model_audit": _model_audit(
            policy_target=node.requested_model,
            actual_runtime_model=None,
            reasoning_effort=node.requested_reasoning_effort,
            auditability="runtime_not_exposed",
            routing_basis="AAS5 ordinary FULL_PIPELINE / IDEATION placeholder routing target.",
        ),
        "artifact_provenance": build_artifact_provenance(
            writer_mode="bootstrap_placeholder",
            writer_agent_name=parent_agent_name or "pending-parent-agent",
            writer_session_id=None,
            writer_node_id="mst",
            owner_node_id=node.node_id,
            notes=[
                "Placeholder written during prepare_idea_task.",
                "Replace this artifact with a real participant result or an explicitly parent-recorded proxy write before merge.",
            ],
        ),
        "verdict": "PENDING",
        "evidence": [],
        "recommended_next_action": "Replace this placeholder with the real participant result before convergence.",
    }
    if node.lane_id:
        payload["lane_id"] = node.lane_id
        payload["lane_label"] = node.lane_label
        payload["lane_strategy"] = node.lane_strategy
    if node.audit_domain:
        payload["audit_domain"] = node.audit_domain
    if node.branch_id:
        payload["branch_id"] = node.branch_id
        payload["branch_label"] = node.branch_label
        payload["parent_role"] = node.role
        payload["branch_kind"] = node.branch_kind
    return payload


def build_placeholder_child_result_merge_package(
    *,
    task_id: str,
    workflow_id: str,
    dispatch_id: str,
    run_key: str,
    aas5_nodes: list[Any],
    lane_ids: list[str],
) -> dict[str, Any]:
    child_results = []
    child_artifact_paths = [f"docs/task_workspaces/{task_id}/{item.expected_artifact}" for item in aas5_nodes]
    for item in aas5_nodes:
        child_results.append(
            {
                "node_id": item.node_id,
                "parent_node_id": item.parent_node_id,
                "role": item.role,
                "role_label": item.role_label,
                "status": "PLANNED",
                "branch_id": item.branch_id,
                "branch_label": item.branch_label,
                "parent_role": item.role if item.branch_id else None,
                "branch_kind": item.branch_kind,
                "lane_id": item.lane_id,
                "lane_label": item.lane_label,
                "lane_strategy": item.lane_strategy,
                "audit_domain": item.audit_domain,
                "verdict": "PENDING",
                "recommended_next_action": "Run the real AAS5 participant analysis and replace the placeholder artifact.",
                "evidence": [],
                "artifact_path": f"docs/task_workspaces/{task_id}/{item.expected_artifact}",
                "model_audit": _model_audit(
                    policy_target=item.requested_model,
                    actual_runtime_model=None,
                    reasoning_effort=item.requested_reasoning_effort,
                    auditability="runtime_not_exposed",
                    routing_basis="AAS5 ordinary FULL_PIPELINE / IDEATION placeholder routing target.",
                ),
                "artifact_provenance": build_artifact_provenance(
                    writer_mode="bootstrap_placeholder",
                    writer_agent_name=None,
                    writer_session_id=None,
                    writer_node_id="mst",
                    owner_node_id=item.node_id,
                    notes=[
                        "Placeholder merge entry written during prepare_idea_task.",
                    ],
                ),
            }
        )
    return {
        "type": "CHILD_RESULT_MERGE_PACKAGE",
        "doctrine_version": AAS5_DOCTRINE_VERSION,
        "topology_mode": AAS5_TOPOLOGY_MODE,
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "dispatch_id": dispatch_id,
        "dispatch_status": "PLANNED",
        "generated_at": utc_now(),
        "merge_ready": False,
        "child_results": child_results,
        "lane_report_refs": {lane_id: f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}" for lane_id in lane_ids},
        "audit_refs": {
            "compliance": f"docs/task_workspaces/{task_id}/{SWARM_COMPLIANCE_AUDIT}",
            "runtime": f"docs/task_workspaces/{task_id}/{RUNTIME_AUDIT_RECORD}",
            "authority": f"docs/task_workspaces/{task_id}/{AUTHORITY_COVERAGE_AUDIT}",
            "adversarial": f"docs/task_workspaces/{task_id}/{ADVERSARIAL_INTEGRITY_REVIEW}",
        },
        "disagreement_signals": [],
        "recommended_parent_actions": [
            "Spawn the real AAS5 ordinary ideation swarm and update every participant artifact before merging the ideation result.",
        ],
        "synthesis_outline": [
            "Replace each placeholder participant artifact with the real verdict and evidence.",
            "Update lane reports, audit artifacts, TEAM_PLAN.yaml, FUTURE_BRANCH_REPORT.json, and SWARM_EXECUTION_RECORD.json after the real AAS5 swarm completes.",
            "Converge the lane outputs and audits explicitly before presenting the ideation option set.",
        ],
        "source_refs": {
            "children": child_artifact_paths,
            "future_branch_report": f"docs/task_workspaces/{task_id}/{FUTURE_BRANCH_REPORT}",
            "swarm_topology_graph": f"docs/task_workspaces/{task_id}/{SWARM_TOPOLOGY_GRAPH}",
            "execution_parallelism_record": f"docs/task_workspaces/{task_id}/{EXECUTION_PARALLELISM_RECORD}",
        },
    }


def build_placeholder_swarm_execution_record(
    *,
    task_id: str,
    generated_at: str,
    agent_name: str | None,
    future_policy: dict[str, Any],
    workflow_id: str,
    run_key: str,
    branch_specs: list[dict[str, Any]],
    aas5_nodes: list[Any],
    team_plan_ref: str,
    merge_package_ref: str,
    topology_graph_ref: str,
    parallelism_record_ref: str,
) -> dict[str, Any]:
    required_roles = sorted({item["parent_role"] for item in branch_specs})
    return {
        "type": "SWARM_EXECUTION_RECORD",
        "doctrine_version": AAS5_DOCTRINE_VERSION,
        "topology_mode": AAS5_TOPOLOGY_MODE,
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "stage": "IDEATION",
        "generated_at": generated_at,
        "swarm_requirement": {
            "required": True,
            "reason": "Exploratory architecture-heavy FULL PIPELINE ideation requires the real AAS5 25-agent topology.",
            "solo_mode_authorized": False,
            "blocking_behavior_if_unavailable": "stop_and_report",
        },
        "runtime_capabilities": {
            "multi_agent_enabled": False,
            "real_child_sessions_available": False,
            "child_result_tracking_available": True,
            "notes": [
                "Placeholder created by prepare_idea_task. Replace with actual runtime capabilities before stage close.",
                "If parent model identity or swarm capability are not exposed by the runtime, record degraded auditability explicitly rather than assuming success.",
            ],
        },
        "execution_mode": "BLOCKED",
        "execution_parallelism_mode": "blocked_pending_runtime_evidence",
        "parent_session": {
            "node_id": "mst",
            "agent_name": agent_name or "pending-parent-agent",
            "session_id": None,
            "provider": "codex",
            "role": "master_orchestrator",
            "model_audit": _model_audit(
                policy_target="gpt-5.4",
                actual_runtime_model=None,
                reasoning_effort="xhigh",
                auditability="runtime_not_exposed",
                routing_basis="Codex MODEL_ROUTING primary director policy target; prep-time placeholder has no runtime-exposed parent model.",
            ),
        },
        "required_child_roles": required_roles,
        "required_child_ids": [item["branch_id"] for item in branch_specs],
        "required_node_ids": ["mst", *[item.node_id for item in aas5_nodes]],
        "required_manager_ids": [item.node_id for item in aas5_nodes if item.tier == "lane_manager"],
        "required_reporter_ids": [item.node_id for item in aas5_nodes if item.tier == "lane_reporter"],
        "required_auditor_ids": [item.node_id for item in aas5_nodes if item.tier == "auditor"],
        "required_worker_node_ids": [item.node_id for item in aas5_nodes if item.tier == "lane_worker"],
        "spawned_children": [],
        "internal_viewpoint_roles": [],
        "merge_evidence": {
            "team_plan_ref": team_plan_ref,
            "child_result_merge_package_ref": merge_package_ref,
            "topology_graph_ref": topology_graph_ref,
            "execution_parallelism_record_ref": parallelism_record_ref,
            "future_branch_report_ref": f"docs/task_workspaces/{task_id}/{FUTURE_BRANCH_REPORT}",
            "lane_report_refs": {lane_id: f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}" for lane_id in LANE_IDS},
            "audit_refs": {
                "compliance": f"docs/task_workspaces/{task_id}/{SWARM_COMPLIANCE_AUDIT}",
                "runtime": f"docs/task_workspaces/{task_id}/{RUNTIME_AUDIT_RECORD}",
                "authority": f"docs/task_workspaces/{task_id}/{AUTHORITY_COVERAGE_AUDIT}",
                "adversarial": f"docs/task_workspaces/{task_id}/{ADVERSARIAL_INTEGRITY_REVIEW}",
            },
        },
        "blocking_reason": "Placeholder until the real AAS5 25-agent ideation swarm runs and persists per-node result artifacts plus lane and audit artifacts.",
        "recommendation_authorized": False,
        "notes": [
            "A blocked placeholder record is expected at prep time and must be replaced before ideation is treated as complete.",
            f"Expected team mode: {str(future_policy.get('team_mode') or AAS5_IDEATION_TEAM_MODE)}.",
            "If this record remains BLOCKED or recommendation_authorized=false, do not present an ideation recommendation.",
        ],
        "satisfied": False,
    }


def build_placeholder_workflow_run_record(
    *,
    task_id: str,
    workflow_id: str,
    command_request: dict[str, Any],
    generated_at: str,
    future_policy: dict[str, Any],
    branch_specs: list[dict[str, Any]],
    run_key: str,
    aas5_nodes: list[Any],
    lane_ids: list[str],
) -> dict[str, Any]:
    return {
        "type": "WORKFLOW_RUN_RECORD",
        "doctrine_version": AAS5_DOCTRINE_VERSION,
        "topology_mode": AAS5_TOPOLOGY_MODE,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "task_id": task_id,
        "modifier": "AASNI",
        "status": "IDEATION_BLOCKED_PENDING_AAS5_SWARM",
        "started_at": generated_at,
        "completed_at": generated_at,
        "orchestrator": "InventionPipelineManager",
        "gcml_documents_loaded": 0,
        "manifest_document_count": 0,
        "artifacts": {
            "command_request": f"docs/task_workspaces/{task_id}/{COMMAND_REQUEST}",
            "authority_coverage_matrix": f"docs/task_workspaces/{task_id}/{AUTHORITY_COVERAGE_MATRIX}",
            "team_plan": f"docs/task_workspaces/{task_id}/{TEAM_PLAN}",
            "future_branch_report": f"docs/task_workspaces/{task_id}/{FUTURE_BRANCH_REPORT}",
            "swarm_execution_record": f"docs/task_workspaces/{task_id}/{SWARM_EXECUTION_RECORD}",
            "child_result_merge_package": f"docs/task_workspaces/{task_id}/{CHILD_RESULT_MERGE_PACKAGE}",
            "swarm_topology_graph": f"docs/task_workspaces/{task_id}/{SWARM_TOPOLOGY_GRAPH}",
            "execution_parallelism_record": f"docs/task_workspaces/{task_id}/{EXECUTION_PARALLELISM_RECORD}",
            "swarm_compliance_audit": f"docs/task_workspaces/{task_id}/{SWARM_COMPLIANCE_AUDIT}",
            "runtime_audit_record": f"docs/task_workspaces/{task_id}/{RUNTIME_AUDIT_RECORD}",
            "authority_coverage_audit": f"docs/task_workspaces/{task_id}/{AUTHORITY_COVERAGE_AUDIT}",
            "adversarial_integrity_review": f"docs/task_workspaces/{task_id}/{ADVERSARIAL_INTEGRITY_REVIEW}",
            **{f"lane_plan_{lane_id}": f"docs/task_workspaces/{task_id}/{lane_plan_path(lane_id)}" for lane_id in lane_ids},
            **{f"lane_report_{lane_id}": f"docs/task_workspaces/{task_id}/{lane_report_path(lane_id)}" for lane_id in lane_ids},
        },
        "stage_records": [
            {
                "stage": "IDEATION",
                "status": "BLOCKED_PENDING_AAS5_SWARM",
                "produced_artifacts": [
                    COMMAND_REQUEST,
                    HUMAN_DECISION_RECORD,
                    AUTHORITY_COVERAGE_MATRIX,
                    TEAM_PLAN,
                    FUTURE_BRANCH_REPORT,
                    SWARM_EXECUTION_RECORD,
                    CHILD_RESULT_MERGE_PACKAGE,
                    SWARM_TOPOLOGY_GRAPH,
                    EXECUTION_PARALLELISM_RECORD,
                    SWARM_COMPLIANCE_AUDIT,
                    RUNTIME_AUDIT_RECORD,
                    AUTHORITY_COVERAGE_AUDIT,
                    ADVERSARIAL_INTEGRITY_REVIEW,
                    *[lane_plan_path(lane_id) for lane_id in lane_ids],
                    *[lane_report_path(lane_id) for lane_id in lane_ids],
                    *[item.expected_artifact for item in aas5_nodes],
                ],
                "notes": [
                    "Exploratory FULL PIPELINE ideation scaffold created with the default AAS5 25-agent ordinary ideation topology.",
                    "Replace placeholder swarm and authority-coverage artifacts before stage close.",
                    "Do not present an ideation recommendation until validate_swarm_execution_record.py passes and recommendation_authorized=true is recorded.",
                ],
            }
        ],
        "hitl_requirements": list(command_request.get("hitl_requirements") or []),
        "operator_constraints": list(command_request.get("operator_constraints") or []),
        "recommended_next_actions": [
            "Read current claim YAML contents and the resolved authority surfaces.",
            f"Run the real {str(future_policy.get('team_mode') or AAS5_IDEATION_TEAM_MODE)} and persist one participant result artifact per non-parent node.",
            f"Batch participant spawning in waves of at most {DEFAULT_LIVE_CHILD_CAP} live children when runtime evidence requires it.",
            f"Run python scripts/validate_swarm_execution_record.py {task_id} before presenting a recommendation.",
            "Stop after ideation and wait for operator choice.",
        ],
    }
