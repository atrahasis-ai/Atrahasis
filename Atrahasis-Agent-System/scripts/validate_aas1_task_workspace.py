#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


TEXT_ARTIFACTS = {
    "README.md": True,
    "TASK_BRIEF.md": True,
    "WORKFLOW_SUMMARY.md": False,
    "HITL_APPROVAL.md": False,
}

SCHEMA_ARTIFACTS = {
    "AUTHORITY_COVERAGE_MATRIX.json": "authority_coverage_matrix",
    "SWARM_EXECUTION_RECORD.json": "swarm_execution_record",
    "TASK_START_CHECKLIST.json": "task_start_checklist",
    "COMMAND_REQUEST.yaml": "command_request",
    "DISCOVERY_MAP.json": "discovery_map",
    "TECHNOLOGY_FRONTIER_MODEL.json": "technology_frontier_model",
    "OPPORTUNITY_REPORT.json": "opportunity_report",
    "HYPOTHESIS_PACKET.json": "hypothesis_packet",
    "CONTRADICTION_MAP.json": "contradiction_map",
    "SOLUTION_PATH_SET.json": "solution_path_set",
    "NOVELTY_REPORT.json": "novelty_report",
    "FEASIBILITY_REPORT.json": "feasibility_report",
    "EXPERIMENT_SIMULATION_REPORT.json": "experiment_simulation_report",
    "HUMAN_DECISION_RECORD.json": "human_decision_record",
    "EXPLORATION_CONTROL_RECORD.json": "exploration_control_record",
    "WORKFLOW_RUN_RECORD.json": "workflow_run_record",
    "REVIEW_GATE_RECORD.json": "review_gate_record",
    "ADVERSARIAL_REVIEW_RECORD.json": "adversarial_review_record",
    "CONVERGENCE_GATE_RECORD.json": "convergence_gate_record",
    "CONTROLLER_RUN_RESULT.json": "controller_run_result",
    "CLOSEOUT_EXECUTION_RECORD.json": "closeout_execution_record",
    "CLOSEOUT_CONSISTENCY_REPORT.json": "closeout_consistency_report",
    "DIRECT_SPEC_AUDIT_RECORD.json": "direct_spec_audit_record",
    "DIRECT_SPEC_VERIFICATION_REPORT.json": "direct_spec_verification_report",
    "STAGE_CONTRACT_REPORT.json": "stage_contract_report",
    "TEAM_DISPATCH_RECOMMENDATIONS.json": "team_dispatch_recommendations",
    "TEAM_PLAN.yaml": "team_plan",
    "TEAM_DISPATCH_RECORD.json": "team_dispatch_record",
    "FUTURE_BRANCH_REPORT.json": "future_branch_report",
    "CHILD_RESULT_MERGE_PACKAGE.json": "child_result_merge_package",
    "FUTURE_CONVERGENCE_REPORT.json": "future_convergence_report",
    "TASK_IMPROVEMENT_REPORT.json": "task_improvement_report",
    "RADICAL_REDESIGN_REPORT.json": "radical_redesign_report",
    "SHARED_STATE_CLOSEOUT_RECORD.json": "shared_state_closeout_record",
}


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def main() -> int:
    if len(sys.argv) != 2:
        eprint("Usage: python scripts/validate_aas1_task_workspace.py <task-workspace-dir>")
        return 2

    workspace = Path(sys.argv[1]).resolve()
    if not workspace.exists() or not workspace.is_dir():
        eprint(f"Task workspace not found: {workspace}")
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    schema_root = repo_root / "docs" / "schemas"
    failed = False

    for filename, required in TEXT_ARTIFACTS.items():
        artifact = workspace / filename
        if not artifact.exists():
            if required:
                eprint(f"[FAIL] missing required text artifact: {filename}")
                failed = True
            continue
        if not artifact.read_text(encoding="utf-8").strip():
            eprint(f"[FAIL] {filename}: text artifact is empty")
            failed = True
            continue
        print(f"[OK] {filename}")

    for filename, schema_name in SCHEMA_ARTIFACTS.items():
        artifact = workspace / filename
        if not artifact.exists():
            continue
        if not _validate_artifact(artifact=artifact, filename=filename, schema_name=schema_name, schema_root=schema_root):
            failed = True

    child_root = workspace / "children"
    child_results = sorted(child_root.glob("*.json")) if child_root.exists() else []
    if (workspace / "FUTURE_BRANCH_REPORT.json").exists() and not child_results:
        eprint("[FAIL] FUTURE_BRANCH_REPORT.json exists but children/ contains no child result artifacts")
        failed = True
    for artifact in child_results:
        if not _validate_artifact(
            artifact=artifact,
            filename=f"children/{artifact.name}",
            schema_name="child_agent_result",
            schema_root=schema_root,
        ):
            failed = True

    return 1 if failed else 0


def _validate_artifact(*, artifact: Path, filename: str, schema_name: str, schema_root: Path) -> bool:
    try:
        if artifact.suffix.lower() in {".yaml", ".yml"}:
            import yaml

            payload = yaml.safe_load(artifact.read_text(encoding="utf-8"))
        else:
            payload = json.loads(artifact.read_text(encoding="utf-8"))
        schema = json.loads((schema_root / f"{schema_name}.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
    except Exception as exc:
        eprint(f"[FAIL] {filename}: {exc}")
        return False

    if errors:
        eprint(f"[FAIL] {filename}: schema validation failed")
        for err in errors:
            path = ".".join(str(part) for part in err.path) or "<root>"
            eprint(f"  - {path}: {err.message}")
        return False

    print(f"[OK] {filename}")
    return True


if __name__ == "__main__":
    raise SystemExit(main())
