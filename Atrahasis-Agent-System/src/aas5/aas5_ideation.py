from __future__ import annotations

from dataclasses import dataclass
from typing import Any


AAS5_DOCTRINE_VERSION = "AAS5"
AAS5_TOPOLOGY_MODE = "AAS5_25_AGENT_HIERARCHY"
AAS5_IDEATION_TEAM_MODE = "FUTURE_BRANCH_SWARM"
AAS5_IDEATION_AGENT_COUNT = 25
AAS5_NON_PARENT_NODE_COUNT = 24
SWARM_TOPOLOGY_GRAPH = "SWARM_TOPOLOGY_GRAPH.json"
EXECUTION_PARALLELISM_RECORD = "EXECUTION_PARALLELISM_RECORD.json"
SWARM_COMPLIANCE_AUDIT = "SWARM_COMPLIANCE_AUDIT.json"
RUNTIME_AUDIT_RECORD = "RUNTIME_AUDIT_RECORD.json"
AUTHORITY_COVERAGE_AUDIT = "AUTHORITY_COVERAGE_AUDIT.json"
ADVERSARIAL_INTEGRITY_REVIEW = "ADVERSARIAL_INTEGRITY_REVIEW.json"

LANE_IDS = ("alpha", "beta", "gamma", "radical")
WORKER_ROLE_ORDER = ("visionary", "systems_thinker", "critic")

AUDITOR_DOMAIN_SPECS = (
    ("compliance", "Swarm Compliance Auditor"),
    ("runtime", "Runtime Audit Recorder"),
    ("authority", "Authority Coverage Auditor"),
    ("adversarial", "Adversarial Integrity Reviewer"),
)

MODEL_AUDITABILITY_STATES = (
    "verified_exact",
    "verified_alias",
    "self_reported_alias",
    "runtime_not_exposed",
    "unknown_unresolved",
)

NON_BLOCKING_MODEL_AUDITABILITY_STATES = {
    "verified_exact",
    "verified_alias",
    "self_reported_alias",
    "runtime_not_exposed",
}

DEFAULT_REQUESTED_MODELS = {
    "master": ("gpt-5.4", "xhigh"),
    "manager": ("gpt-5.4", "xhigh"),
    "worker": ("gpt-5.4", "high"),
    "reporter": ("gpt-5.4", "xhigh"),
    "auditor": ("gpt-5.4", "xhigh"),
}

DEGRADED_FALLBACK_MODELS = {
    "master": ("gpt-5.2", "xhigh"),
    "manager": ("gpt-5.2", "xhigh"),
    "worker": ("gpt-5.2", "high"),
    "reporter": ("gpt-5.2", "xhigh"),
    "auditor": ("gpt-5.2", "xhigh"),
}

DEFAULT_MANAGER_BATCH = "managers"
DEFAULT_WORKER_BATCH_PREFIX = "workers"
DEFAULT_REPORTER_BATCH = "reporters"
DEFAULT_AUDITOR_BATCH = "auditors"


@dataclass(frozen=True)
class AAS5Node:
    node_id: str
    parent_node_id: str
    tier: str
    role: str
    role_label: str
    lane_id: str | None
    lane_label: str | None
    audit_domain: str | None
    batch_label: str
    requested_model: str
    requested_reasoning_effort: str
    expected_artifact: str
    objective: str
    branch_id: str | None = None
    branch_label: str | None = None
    branch_kind: str | None = None
    lane_strategy: str | None = None


def make_run_key(task_id: str, workflow_id: str) -> str:
    return f"{task_id}::{workflow_id}"


def manager_node_id(lane_id: str) -> str:
    return f"mgr.{lane_id}"


def worker_node_id(lane_id: str, role: str) -> str:
    return f"wrk.{lane_id}.{role}"


def reporter_node_id(lane_id: str) -> str:
    return f"rep.{lane_id}"


def auditor_node_id(domain: str) -> str:
    return f"aud.{domain}"


def lane_plan_path(lane_id: str) -> str:
    return f"LANE_PLAN_{lane_id}.yaml"


def lane_report_path(lane_id: str) -> str:
    return f"LANE_CONVERGENCE_REPORT_{lane_id}.json"


def lane_manager_artifact_path(lane_id: str) -> str:
    return f"children/managers/{manager_node_id(lane_id)}.json"


def lane_worker_artifact_path(lane_id: str, role: str) -> str:
    return f"children/workers/{worker_node_id(lane_id, role)}.json"


def lane_reporter_artifact_path(lane_id: str) -> str:
    return f"children/reporters/{reporter_node_id(lane_id)}.json"


def auditor_artifact_path(domain: str) -> str:
    return f"children/auditors/{auditor_node_id(domain)}.json"


def audit_artifact_path(domain: str) -> str:
    if domain == "compliance":
        return SWARM_COMPLIANCE_AUDIT
    if domain == "runtime":
        return RUNTIME_AUDIT_RECORD
    if domain == "authority":
        return AUTHORITY_COVERAGE_AUDIT
    return ADVERSARIAL_INTEGRITY_REVIEW


def normalize_model_auditability(value: str | None) -> str:
    token = str(value or "").strip()
    if token in MODEL_AUDITABILITY_STATES:
        return token
    return "unknown_unresolved"


def build_model_audit(
    *,
    requested_model: str | None,
    requested_reasoning_effort: str | None,
    observed_runtime_model: str | None,
    observed_model_auditability: str,
    routing_basis: str,
) -> dict[str, Any]:
    auditability = normalize_model_auditability(observed_model_auditability)
    return {
        "requested_model": requested_model,
        "requested_reasoning_effort": requested_reasoning_effort,
        "observed_runtime_model": observed_runtime_model,
        "observed_model_auditability": auditability,
        "routing_basis": routing_basis,
        # Legacy aliases kept for transitional readers.
        "policy_target": requested_model,
        "reasoning_effort": requested_reasoning_effort,
        "actual_runtime_model": observed_runtime_model,
        "auditability": auditability,
    }


def build_artifact_provenance(
    *,
    writer_mode: str,
    writer_agent_name: str | None,
    writer_session_id: str | None,
    writer_node_id: str | None,
    owner_node_id: str | None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "writer_mode": writer_mode,
        "writer_agent_name": writer_agent_name,
        "writer_session_id": writer_session_id,
        "writer_node_id": writer_node_id,
        "owner_node_id": owner_node_id,
        "notes": list(notes or []),
    }


def build_aas5_batches(nodes: list[AAS5Node], *, max_live_children: int) -> list[dict[str, Any]]:
    managers = [node.node_id for node in nodes if node.tier == "lane_manager"]
    workers = [node.node_id for node in nodes if node.tier == "lane_worker"]
    reporters = [node.node_id for node in nodes if node.tier == "lane_reporter"]
    auditors = [node.node_id for node in nodes if node.tier == "auditor"]

    worker_batches: list[dict[str, Any]] = []
    for index in range(0, len(workers), max_live_children):
        batch_number = (index // max_live_children) + 1
        worker_batches.append(
            {
                "batch_label": f"{DEFAULT_WORKER_BATCH_PREFIX}.{batch_number}",
                "node_ids": workers[index : index + max_live_children],
            }
        )

    batches = [
        {"batch_label": DEFAULT_MANAGER_BATCH, "node_ids": managers},
        *worker_batches,
        {"batch_label": DEFAULT_REPORTER_BATCH, "node_ids": reporters},
        {"batch_label": DEFAULT_AUDITOR_BATCH, "node_ids": auditors},
    ]
    return [item for item in batches if item["node_ids"]]


def lane_worker_node_ids(nodes: list[AAS5Node], lane_id: str) -> list[str]:
    return [node.node_id for node in nodes if node.tier == "lane_worker" and node.lane_id == lane_id]


def lane_reporter(nodes: list[AAS5Node], lane_id: str) -> AAS5Node | None:
    for node in nodes:
        if node.tier == "lane_reporter" and node.lane_id == lane_id:
            return node
    return None


def lane_manager(nodes: list[AAS5Node], lane_id: str) -> AAS5Node | None:
    for node in nodes:
        if node.tier == "lane_manager" and node.lane_id == lane_id:
            return node
    return None


def auditor_nodes(nodes: list[AAS5Node]) -> list[AAS5Node]:
    return [node for node in nodes if node.tier == "auditor"]


def build_aas5_ideation_nodes(
    *,
    task_id: str,
    branch_specs: list[dict[str, Any]],
    title: str,
) -> list[AAS5Node]:
    lane_branches: dict[str, dict[str, dict[str, Any]]] = {lane_id: {} for lane_id in LANE_IDS}
    lane_labels: dict[str, str] = {}
    lane_strategies: dict[str, str] = {}
    for item in branch_specs:
        lane_id = str(item.get("lane_id") or "")
        role = str(item.get("parent_role") or "")
        if lane_id not in lane_branches or role not in WORKER_ROLE_ORDER:
            continue
        lane_branches[lane_id][role] = item
        lane_labels[lane_id] = str(item.get("lane_label") or lane_id.title())
        lane_strategies[lane_id] = str(item.get("lane_strategy") or "")

    nodes: list[AAS5Node] = []
    for lane_id in LANE_IDS:
        lane_label = lane_labels.get(lane_id, lane_id.title())
        lane_strategy = lane_strategies.get(lane_id, "")
        nodes.append(
            AAS5Node(
                node_id=manager_node_id(lane_id),
                parent_node_id="mst",
                tier="lane_manager",
                role="lane_manager",
                role_label=f"{lane_label} Manager",
                lane_id=lane_id,
                lane_label=lane_label,
                audit_domain=None,
                batch_label=DEFAULT_MANAGER_BATCH,
                requested_model=DEFAULT_REQUESTED_MODELS["manager"][0],
                requested_reasoning_effort=DEFAULT_REQUESTED_MODELS["manager"][1],
                expected_artifact=lane_manager_artifact_path(lane_id),
                objective=(
                    f"Manage the {lane_label} lane for '{title}', preserve independence across its three leaf workers, "
                    "and own lane-local execution state without issuing the final recommendation."
                ),
                lane_strategy=lane_strategy,
            )
        )
        nodes.append(
            AAS5Node(
                node_id=reporter_node_id(lane_id),
                parent_node_id="mst",
                tier="lane_reporter",
                role="lane_convergence_reporter",
                role_label=f"{lane_label} Lane Convergence Reporter",
                lane_id=lane_id,
                lane_label=lane_label,
                audit_domain=None,
                batch_label=DEFAULT_REPORTER_BATCH,
                requested_model=DEFAULT_REQUESTED_MODELS["reporter"][0],
                requested_reasoning_effort=DEFAULT_REQUESTED_MODELS["reporter"][1],
                expected_artifact=lane_reporter_artifact_path(lane_id),
                objective=(
                    f"Synthesize the completed {lane_label} worker results for '{title}' without acting as manager, auditor, or final recommender."
                ),
                lane_strategy=lane_strategy,
            )
        )
        for role in WORKER_ROLE_ORDER:
            branch = lane_branches.get(lane_id, {}).get(role)
            if branch is None:
                continue
            nodes.append(
                AAS5Node(
                    node_id=worker_node_id(lane_id, role),
                    parent_node_id=manager_node_id(lane_id),
                    tier="lane_worker",
                    role=role,
                    role_label=f"{lane_label} {role}",
                    lane_id=lane_id,
                    lane_label=lane_label,
                    audit_domain=None,
                    batch_label=DEFAULT_WORKER_BATCH_PREFIX,
                    requested_model=DEFAULT_REQUESTED_MODELS["worker"][0],
                    requested_reasoning_effort=DEFAULT_REQUESTED_MODELS["worker"][1],
                    expected_artifact=lane_worker_artifact_path(lane_id, role),
                    objective=str(branch.get("objective") or ""),
                    branch_id=str(branch.get("branch_id") or ""),
                    branch_label=str(branch.get("branch_label") or ""),
                    branch_kind=str(branch.get("branch_kind") or ""),
                    lane_strategy=lane_strategy,
                )
            )

    for domain, role_label in AUDITOR_DOMAIN_SPECS:
        nodes.append(
            AAS5Node(
                node_id=auditor_node_id(domain),
                parent_node_id="mst",
                tier="auditor",
                role="auditor",
                role_label=role_label,
                lane_id=None,
                lane_label=None,
                audit_domain=domain,
                batch_label=DEFAULT_AUDITOR_BATCH,
                requested_model=DEFAULT_REQUESTED_MODELS["auditor"][0],
                requested_reasoning_effort=DEFAULT_REQUESTED_MODELS["auditor"][1],
                expected_artifact=auditor_artifact_path(domain),
                objective=_auditor_objective(domain, title=title),
            )
        )

    return nodes


def _auditor_objective(domain: str, *, title: str) -> str:
    if domain == "compliance":
        return f"Audit whether the '{title}' ideation swarm satisfied the declared topology and anti-fake-realism rules."
    if domain == "runtime":
        return f"Audit runtime/accounting truth, batching, concurrency, and requested-vs-observed model routing for '{title}'."
    if domain == "authority":
        return f"Audit whether every named authority surface for '{title}' was explicitly covered before recommendation."
    return f"Audit adversarial sufficiency and self-certification failures for the '{title}' ideation swarm."


def build_lane_plan_payload(
    *,
    task_id: str,
    workflow_id: str,
    run_key: str,
    lane_id: str,
    lane_label: str,
    lane_strategy: str,
    manager_id: str,
    worker_node_ids: list[str],
    reporter_node_id: str,
    generated_at: str,
) -> dict[str, Any]:
    return {
        "type": "LANE_PLAN",
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "lane_id": lane_id,
        "lane_label": lane_label,
        "lane_strategy": lane_strategy,
        "manager_node_id": manager_id,
        "worker_node_ids": worker_node_ids,
        "reporter_node_id": reporter_node_id,
        "status": "PLANNED",
        "generated_at": generated_at,
        "notes": [
            "Placeholder lane plan created during AAS5 ideation prep.",
            "Replace this with runtime-backed lane execution state before recommendation.",
        ],
    }


def build_lane_report_payload(
    *,
    task_id: str,
    workflow_id: str,
    run_key: str,
    lane_id: str,
    lane_label: str,
    reporter_node_id: str,
    worker_node_ids: list[str],
    generated_at: str,
) -> dict[str, Any]:
    return {
        "type": "LANE_CONVERGENCE_REPORT",
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "lane_id": lane_id,
        "lane_label": lane_label,
        "reporter_node_id": reporter_node_id,
        "worker_node_ids": worker_node_ids,
        "status": "PLANNED",
        "recommendation_authorized": False,
        "blocking_gates": [
            "All three lane worker artifacts must be completed before lane convergence is valid.",
        ],
        "generated_at": generated_at,
        "updated_at": generated_at,
        "summary": "Pending lane convergence.",
        "disagreement_signals": [],
        "candidate_options": [],
        "notes": [
            "Placeholder lane convergence report created during AAS5 ideation prep.",
        ],
    }


def build_audit_payload(
    *,
    artifact_type: str,
    task_id: str,
    workflow_id: str,
    run_key: str,
    owner_node_id: str,
    generated_at: str,
    summary: str,
    blocking_gates: list[str],
) -> dict[str, Any]:
    return {
        "type": artifact_type,
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "owner_node_id": owner_node_id,
        "generated_at": generated_at,
        "updated_at": generated_at,
        "status": "PLANNED",
        "recommendation_authorized": False,
        "blocking_gates": list(blocking_gates),
        "summary": summary,
        "notes": [
            "Placeholder audit artifact created during AAS5 ideation prep.",
        ],
    }


def build_topology_graph_payload(
    *,
    task_id: str,
    workflow_id: str,
    run_key: str,
    generated_at: str,
    nodes: list[AAS5Node],
) -> dict[str, Any]:
    payload_nodes = [
        {
            "node_id": "mst",
            "parent_node_id": None,
            "tier": "master",
            "role": "master_orchestrator",
            "role_label": "Master Orchestrator",
            "lane_id": None,
            "audit_domain": None,
            "artifact_ref": None,
        }
    ]
    payload_edges = []
    for item in nodes:
        payload_nodes.append(
            {
                "node_id": item.node_id,
                "parent_node_id": item.parent_node_id,
                "tier": item.tier,
                "role": item.role,
                "role_label": item.role_label,
                "lane_id": item.lane_id,
                "audit_domain": item.audit_domain,
                "artifact_ref": f"docs/task_workspaces/{task_id}/{item.expected_artifact}",
            }
        )
        payload_edges.append({"parent_node_id": item.parent_node_id, "child_node_id": item.node_id})
    return {
        "type": "SWARM_TOPOLOGY_GRAPH",
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "generated_at": generated_at,
        "topology_mode": AAS5_TOPOLOGY_MODE,
        "ideal_agent_count": AAS5_IDEATION_AGENT_COUNT,
        "realized_node_count": len(payload_nodes),
        "nodes": payload_nodes,
        "edges": payload_edges,
        "notes": [
            "Placeholder topology graph created during AAS5 ideation prep.",
        ],
    }


def build_execution_parallelism_payload(
    *,
    task_id: str,
    workflow_id: str,
    run_key: str,
    generated_at: str,
    nodes: list[AAS5Node],
    max_live_children: int,
) -> dict[str, Any]:
    batches = build_aas5_batches(nodes, max_live_children=max_live_children)
    return {
        "type": "EXECUTION_PARALLELISM_RECORD",
        "task_id": task_id,
        "workflow_id": workflow_id,
        "run_key": run_key,
        "generated_at": generated_at,
        "updated_at": generated_at,
        "simultaneous_target_agent_count": AAS5_IDEATION_AGENT_COUNT,
        "execution_parallelism_mode": "degraded_batched",
        "total_agents_spawned": AAS5_IDEATION_AGENT_COUNT,
        "total_children_spawned": len(nodes),
        "total_grandchildren_spawned": sum(1 for node in nodes if node.parent_node_id.startswith("mgr.")),
        "max_live_concurrent_agents": min(AAS5_IDEATION_AGENT_COUNT, 1 + max_live_children),
        "max_live_concurrent_children": max_live_children,
        "max_live_concurrent_grandchildren": min(12, max_live_children),
        "actual_parallel_agent_count": min(AAS5_IDEATION_AGENT_COUNT, 1 + max_live_children),
        "batch_count": len(batches),
        "batch_structure": batches,
        "runtime_limit_evidence": [],
        "notes": [
            "Placeholder AAS5 execution parallelism record created during ideation prep.",
            "Batching is the default prep-time posture until runtime evidence proves ideal simultaneous execution.",
        ],
    }
