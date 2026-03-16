from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from aas1.common import load_yaml, utc_now
from aas1.spec_path_resolver import resolve_spec_ref
from aas1.task_claim_coordinator import TaskClaimCoordinator


def build_bootstrap_runtime_audit(
    repo_root: Path,
    *,
    agent_name: str | None = None,
    parent_model: str | None = None,
    reasoning_effort: str | None = None,
    child_agent_capable: bool | None = None,
) -> dict[str, Any]:
    active_claims = _active_claims(repo_root)
    rg_path = shutil.which("rg")

    parent_model_known = bool((parent_model or "").strip())
    if child_agent_capable is True:
        child_capability_status = "verified_available"
        child_capability_notes = [
            "Bootstrap explicitly confirmed that the runtime can form real child sessions.",
        ]
    elif child_agent_capable is False:
        child_capability_status = "verified_unavailable"
        child_capability_notes = [
            "Bootstrap explicitly confirmed that real child sessions are unavailable in this runtime.",
        ]
    else:
        child_capability_status = "unverified_runtime_capability"
        child_capability_notes = [
            "Bootstrap could not directly verify child-agent capability in-band; do not claim swarm readiness as proven.",
        ]

    return {
        "type": "BOOTSTRAP_RUNTIME_AUDIT",
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "agent_name": agent_name,
        "active_claims": active_claims,
        "active_claim_count": len(active_claims),
        "required_bootstrap_refs": {
            "master_redesign_spec": "docs/specifications/STRATEGY/MASTER_REDESIGN_SPEC.md",
            "c14": resolve_spec_ref(repo_root, "C14"),
            "c48": resolve_spec_ref(repo_root, "C48"),
        },
        "tooling": {
            "rg_available": bool(rg_path),
            "rg_path": rg_path,
            "search_mode": "rg" if rg_path else "powershell_fallback",
        },
        "parent_model_audit": {
            "policy_target": "gpt-5.4",
            "actual_runtime_model": parent_model.strip() if parent_model_known else None,
            "reasoning_effort": (reasoning_effort or "").strip() or None,
            "auditability": "runtime_exposed" if parent_model_known else "degraded_unknown_runtime_model",
            "routing_basis": "Codex MODEL_ROUTING primary director policy",
        },
        "child_agent_capability": {
            "status": child_capability_status,
            "verified": child_agent_capable is not None,
            "notes": child_capability_notes,
        },
        "bootstrap_readiness": {
            "active_claim_contents_available": True,
            "rg_verified": bool(rg_path),
            "parent_model_exposed": parent_model_known,
            "child_agent_capability_verified": child_agent_capable is not None,
            "auditability_degraded": not parent_model_known or child_agent_capable is None,
        },
        "notes": [
            "Bootstrap must still read the listed surfaces directly; this audit only records runtime/tooling readiness and resolved refs.",
            "If parent model or child-agent capability is not exposed, report degraded auditability rather than claiming full bootstrap proof.",
        ],
    }


def _active_claims(repo_root: Path) -> list[dict[str, Any]]:
    claims_root = repo_root / "docs" / "task_claims"
    active_claims: list[dict[str, Any]] = []
    if not claims_root.exists():
        return active_claims

    for path in sorted(claims_root.glob("*.yaml")):
        if path.name == "CLAIM_TEMPLATE.yaml":
            continue
        try:
            payload = load_yaml(path)
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        if str(payload.get("status") or "").strip().upper() not in TaskClaimCoordinator.ACTIVE_STATUSES:
            continue
        active_claims.append(
            {
                "task_id": str(payload.get("task_id") or path.stem),
                "status": str(payload.get("status") or ""),
                "agent_name": str(payload.get("agent_name") or ""),
                "path": str(path.relative_to(repo_root)).replace("\\", "/"),
            }
        )
    return active_claims
