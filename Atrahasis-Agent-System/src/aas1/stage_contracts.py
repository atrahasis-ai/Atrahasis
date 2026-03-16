from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from aas1.common import utc_now


CONTROL_ARTIFACTS = {
    "README.md",
    "TASK_BRIEF.md",
    "TASK_START_CHECKLIST.json",
    "AUTHORITY_COVERAGE_MATRIX.json",
    "COMMAND_REQUEST.yaml",
    "DISCOVERY_MAP.json",
    "TECHNOLOGY_FRONTIER_MODEL.json",
    "OPPORTUNITY_REPORT.json",
    "HYPOTHESIS_PACKET.json",
    "CONTRADICTION_MAP.json",
    "SOLUTION_PATH_SET.json",
    "NOVELTY_REPORT.json",
    "FEASIBILITY_REPORT.json",
    "EXPERIMENT_SIMULATION_REPORT.json",
    "HUMAN_DECISION_RECORD.json",
    "EXPLORATION_CONTROL_RECORD.json",
    "WORKFLOW_RUN_RECORD.json",
    "WORKFLOW_SUMMARY.md",
    "REVIEW_GATE_RECORD.json",
    "ADVERSARIAL_REVIEW_RECORD.json",
    "CONVERGENCE_GATE_RECORD.json",
    "CLOSEOUT_EXECUTION_RECORD.json",
    "TEAM_DISPATCH_RECOMMENDATIONS.json",
    "TEAM_PLAN.yaml",
    "TEAM_DISPATCH_RECORD.json",
    "FUTURE_BRANCH_REPORT.json",
    "LANE_PLAN_alpha.yaml",
    "LANE_PLAN_beta.yaml",
    "LANE_PLAN_gamma.yaml",
    "LANE_PLAN_radical.yaml",
    "LANE_CONVERGENCE_REPORT_alpha.json",
    "LANE_CONVERGENCE_REPORT_beta.json",
    "LANE_CONVERGENCE_REPORT_gamma.json",
    "LANE_CONVERGENCE_REPORT_radical.json",
    "SWARM_COMPLIANCE_AUDIT.json",
    "RUNTIME_AUDIT_RECORD.json",
    "AUTHORITY_COVERAGE_AUDIT.json",
    "ADVERSARIAL_INTEGRITY_REVIEW.json",
    "SWARM_TOPOLOGY_GRAPH.json",
    "EXECUTION_PARALLELISM_RECORD.json",
    "STAGE_CONTRACT_REPORT.json",
    "CHILD_RESULT_MERGE_PACKAGE.json",
    "FUTURE_CONVERGENCE_REPORT.json",
    "TASK_IMPROVEMENT_REPORT.json",
    "RADICAL_REDESIGN_REPORT.json",
    "SHARED_STATE_CLOSEOUT_RECORD.json",
    "DIRECT_SPEC_AUDIT_RECORD.json",
    "DIRECT_SPEC_VERIFICATION_REPORT.json",
    "CLOSEOUT_CONSISTENCY_REPORT.json",
    "SWARM_EXECUTION_RECORD.json",
}

DEFAULT_STAGE_CONTRACTS: dict[str, dict[str, dict[str, Any]]] = {
    "FULL_PIPELINE": {
        "IDEATION": {
            "required_files": [
                "COMMAND_REQUEST.yaml",
                "HUMAN_DECISION_RECORD.json",
                "AUTHORITY_COVERAGE_MATRIX.json",
                "TEAM_PLAN.yaml",
                "FUTURE_BRANCH_REPORT.json",
                "LANE_PLAN_alpha.yaml",
                "LANE_PLAN_beta.yaml",
                "LANE_PLAN_gamma.yaml",
                "LANE_PLAN_radical.yaml",
                "LANE_CONVERGENCE_REPORT_alpha.json",
                "LANE_CONVERGENCE_REPORT_beta.json",
                "LANE_CONVERGENCE_REPORT_gamma.json",
                "LANE_CONVERGENCE_REPORT_radical.json",
                "SWARM_COMPLIANCE_AUDIT.json",
                "RUNTIME_AUDIT_RECORD.json",
                "AUTHORITY_COVERAGE_AUDIT.json",
                "ADVERSARIAL_INTEGRITY_REVIEW.json",
                "SWARM_TOPOLOGY_GRAPH.json",
                "EXECUTION_PARALLELISM_RECORD.json",
                "SWARM_EXECUTION_RECORD.json",
                "CHILD_RESULT_MERGE_PACKAGE.json",
            ],
            "any_of_files": ["WORKFLOW_RUN_RECORD.json", "EXPLORATION_CONTROL_RECORD.json"],
            "minimum_evidence_artifacts": 2,
            "validators": ["swarm_execution"],
        },
        "RESEARCH": {
            "required_files": [
                "DISCOVERY_MAP.json",
                "TECHNOLOGY_FRONTIER_MODEL.json",
                "OPPORTUNITY_REPORT.json",
                "WORKFLOW_RUN_RECORD.json",
            ],
            "minimum_evidence_artifacts": 3,
        },
        "FEASIBILITY": {
            "required_files": [
                "HYPOTHESIS_PACKET.json",
                "CONTRADICTION_MAP.json",
                "FEASIBILITY_REPORT.json",
                "EXPERIMENT_SIMULATION_REPORT.json",
            ],
            "minimum_evidence_artifacts": 4,
        },
        "DESIGN": {
            "required_files": ["SOLUTION_PATH_SET.json", "WORKFLOW_SUMMARY.md"],
            "minimum_evidence_artifacts": 3,
            "required_globs": ["design/**/*", "architecture/**/*", "specifications/**/*"],
        },
        "SPECIFICATION": {
            "required_files": ["WORKFLOW_RUN_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "minimum_evidence_artifacts": 4,
            "required_globs": ["specifications/**/*", "*MASTER_TECH_SPEC.md", "*SPEC*.md", "*SPEC*.json"],
        },
        "ASSESSMENT": {
            "required_files": ["REVIEW_GATE_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "any_of_files": ["WORKFLOW_SUMMARY.md"],
            "minimum_evidence_artifacts": 4,
            "validators": ["workspace"],
        },
    },
    "DIRECT_SPEC": {
        "RESEARCH": {
            "required_files": [
                "README.md",
                "TASK_BRIEF.md",
                "TASK_START_CHECKLIST.json",
                "DIRECT_SPEC_AUDIT_RECORD.json",
            ],
            "minimum_evidence_artifacts": 0,
        },
        "SPECIFICATION": {
            "required_files": [
                "README.md",
                "TASK_BRIEF.md",
                "TASK_START_CHECKLIST.json",
                "DIRECT_SPEC_AUDIT_RECORD.json",
                "DIRECT_SPEC_VERIFICATION_REPORT.json",
            ],
            "minimum_evidence_artifacts": 0,
            "validators": ["direct_spec_verification"],
        },
        "ASSESSMENT": {
            "required_files": [
                "README.md",
                "TASK_BRIEF.md",
                "TASK_START_CHECKLIST.json",
                "DIRECT_SPEC_AUDIT_RECORD.json",
                "DIRECT_SPEC_VERIFICATION_REPORT.json",
                "CLOSEOUT_CONSISTENCY_REPORT.json",
            ],
            "minimum_evidence_artifacts": 0,
            "validators": ["workspace", "direct_spec_verification", "closeout_consistency"],
        },
    },
    "GOVERNANCE": {
        "RESEARCH": {
            "required_files": ["COMMAND_REQUEST.yaml", "DISCOVERY_MAP.json", "WORKFLOW_RUN_RECORD.json"],
            "minimum_evidence_artifacts": 2,
        },
        "DESIGN": {
            "required_files": ["WORKFLOW_RUN_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "minimum_evidence_artifacts": 3,
            "required_globs": ["*POLICY*.md", "*ADR*.md", "*DECISION*.md", "*PLAN*.md"],
        },
        "ASSESSMENT": {
            "required_files": ["REVIEW_GATE_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "minimum_evidence_artifacts": 3,
            "validators": ["workspace"],
        },
    },
    "ANALYSIS": {
        "RESEARCH": {
            "required_files": ["COMMAND_REQUEST.yaml", "DISCOVERY_MAP.json", "WORKFLOW_RUN_RECORD.json"],
            "minimum_evidence_artifacts": 2,
        },
        "ASSESSMENT": {
            "required_files": ["REVIEW_GATE_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "any_of_files": ["WORKFLOW_SUMMARY.md"],
            "minimum_evidence_artifacts": 2,
            "validators": ["workspace"],
        },
    },
    "PACKAGING": {
        "DESIGN": {
            "required_files": ["WORKFLOW_RUN_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "minimum_evidence_artifacts": 2,
            "required_globs": ["*PACKAGE*.md", "*PACKAGE*.json", "*REVIEW*.md"],
        },
        "SPECIFICATION": {
            "required_files": ["WORKFLOW_RUN_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "minimum_evidence_artifacts": 3,
            "required_globs": ["*PACKAGE*.md", "*SUMMARY*.md", "specifications/**/*"],
        },
        "ASSESSMENT": {
            "required_files": ["REVIEW_GATE_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "minimum_evidence_artifacts": 2,
            "validators": ["workspace"],
        },
    },
    "VALIDATION": {
        "ASSESSMENT": {
            "required_files": ["REVIEW_GATE_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "minimum_evidence_artifacts": 1,
            "validators": ["workspace"],
        },
    },
    "DEMO": {
        "DESIGN": {
            "required_files": ["WORKFLOW_RUN_RECORD.json"],
            "minimum_evidence_artifacts": 2,
        },
        "ASSESSMENT": {
            "required_files": ["REVIEW_GATE_RECORD.json", "HUMAN_DECISION_RECORD.json"],
            "minimum_evidence_artifacts": 2,
            "validators": ["workspace"],
        },
    },
}


class StageContractRegistry:
    """Evaluates exact artifact and validator contracts before stage closure."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.workspace_root = repo_root / "docs" / "task_workspaces"

    def evaluate(
        self,
        *,
        task_id: str,
        task_class: str,
        current_stage: str,
    ) -> dict[str, Any]:
        task_root = self.workspace_root / task_id
        contract = self._resolve_contract(task_id=task_id, task_class=task_class, current_stage=current_stage)
        required_files = list(contract.get("required_files", []))
        any_of_files = list(contract.get("any_of_files", []))
        required_globs = list(contract.get("required_globs", []))
        minimum_evidence_artifacts = int(contract.get("minimum_evidence_artifacts", 0))
        validator_names = list(contract.get("validators", []))

        required_results = [self._file_result(task_root=task_root, relative_path=item) for item in required_files]
        any_of_results = [self._file_result(task_root=task_root, relative_path=item) for item in any_of_files]
        glob_results = [self._glob_result(task_root=task_root, pattern=item) for item in required_globs]
        evidence = self._evidence_artifacts(task_root)
        artifacts_ready = self._artifacts_ready(
            required_results=required_results,
            any_of_results=any_of_results,
            glob_results=glob_results,
            minimum_evidence_artifacts=minimum_evidence_artifacts,
            evidence=evidence,
        )
        validator_results = self._run_validators(
            task_root=task_root,
            validator_names=validator_names,
            can_run=artifacts_ready,
        )

        satisfied = artifacts_ready and all(item.get("valid", False) for item in validator_results)
        missing = []
        for item in required_results:
            if not item["exists"]:
                missing.append(item["path"])
        if any_of_results and not any(item["exists"] for item in any_of_results):
            missing.append("one_of:" + ",".join(item["path"] for item in any_of_results))
        for item in glob_results:
            if not item["matched"]:
                missing.append("glob:" + item["pattern"])
        if len(evidence) < minimum_evidence_artifacts:
            missing.append(f"evidence_artifacts>={minimum_evidence_artifacts}")
        for item in validator_results:
            if not item.get("valid", False):
                missing.append(f"validator:{item['name']}")

        return {
            "type": "STAGE_CONTRACT_REPORT",
            "task_id": task_id,
            "task_class": task_class,
            "stage": current_stage,
            "evaluated_at": utc_now(),
            "contract": {
                "required_files": required_files,
                "any_of_files": any_of_files,
                "required_globs": required_globs,
                "minimum_evidence_artifacts": minimum_evidence_artifacts,
                "validators": validator_names,
            },
            "artifact_checks": {
                "required_files": required_results,
                "any_of_files": any_of_results,
                "required_globs": glob_results,
                "evidence_artifacts": evidence,
                "evidence_count": len(evidence),
            },
            "validator_results": validator_results,
            "satisfied": satisfied,
            "missing_requirements": missing,
        }

    def _resolve_contract(self, *, task_id: str, task_class: str, current_stage: str) -> dict[str, Any]:
        base = copy.deepcopy(DEFAULT_STAGE_CONTRACTS.get(task_class, {}).get(current_stage, {}))
        override_path = self.workspace_root / task_id / "STAGE_CONTRACT.yaml"
        if not override_path.exists():
            return base
        payload = yaml.safe_load(override_path.read_text(encoding="utf-8")) or {}
        override = (
            payload.get("task_classes", {}).get(task_class, {}).get(current_stage)
            or payload.get("stages", {}).get(current_stage)
            or {}
        )
        for key, value in override.items():
            base[key] = value
        return base

    def _artifacts_ready(
        self,
        *,
        required_results: list[dict[str, Any]],
        any_of_results: list[dict[str, Any]],
        glob_results: list[dict[str, Any]],
        minimum_evidence_artifacts: int,
        evidence: list[dict[str, Any]],
    ) -> bool:
        if any(not item["exists"] for item in required_results):
            return False
        if any_of_results and not any(item["exists"] for item in any_of_results):
            return False
        if any(not item["matched"] for item in glob_results):
            return False
        if len(evidence) < minimum_evidence_artifacts:
            return False
        return True

    def _file_result(self, *, task_root: Path, relative_path: str) -> dict[str, Any]:
        path = task_root / relative_path
        return {"path": relative_path, "exists": path.exists()}

    def _glob_result(self, *, task_root: Path, pattern: str) -> dict[str, Any]:
        matches = []
        for item in task_root.rglob("*"):
            if item.is_dir():
                continue
            relative = item.relative_to(task_root).as_posix()
            if item.match(pattern) or Path(relative).match(pattern):
                matches.append(relative)
        return {"pattern": pattern, "matched": bool(matches), "matches": matches[:20]}

    def _evidence_artifacts(self, task_root: Path) -> list[dict[str, Any]]:
        evidence = []
        if not task_root.exists():
            return evidence
        for item in sorted(task_root.rglob("*")):
            if item.is_dir():
                continue
            if item.name in CONTROL_ARTIFACTS:
                continue
            relative = item.relative_to(task_root).as_posix()
            evidence.append({"path": relative, "size_bytes": item.stat().st_size})
        return evidence[:200]

    def _run_validators(
        self,
        *,
        task_root: Path,
        validator_names: list[str],
        can_run: bool,
    ) -> list[dict[str, Any]]:
        results = []
        if not can_run:
            return results
        for name in validator_names:
            if name == "workspace":
                script = self.repo_root / "scripts" / "validate_aas1_task_workspace.py"
                argv = [sys.executable, str(script), str(task_root)]
            elif name == "direct_spec_verification":
                script = self.repo_root / "scripts" / "verify_direct_spec_task.py"
                argv = [sys.executable, str(script), task_root.name]
            elif name == "closeout_consistency":
                script = self.repo_root / "scripts" / "validate_task_closeout_consistency.py"
                argv = [sys.executable, str(script), task_root.name]
            elif name == "swarm_execution":
                script = self.repo_root / "scripts" / "validate_swarm_execution_record.py"
                argv = [sys.executable, str(script), task_root.name]
            else:
                continue
            completed = subprocess.run(
                argv,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            output = completed.stdout.strip()
            if completed.stderr.strip():
                output = (output + "\n" + completed.stderr.strip()).strip()
            results.append(
                {
                    "name": name,
                    "valid": completed.returncode == 0,
                    "exit_code": completed.returncode,
                    "output": output,
                }
            )
        return results
