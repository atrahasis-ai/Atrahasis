from __future__ import annotations

import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from aas1.control_plane import AtrahasisControlPlane
from aas1.stage_contracts import StageContractRegistry
from aas1.common import load_yaml
from aas1.task_hardening import (
    AUTHORITY_COVERAGE_MATRIX,
    CHILD_RESULT_MERGE_PACKAGE,
    COMMAND_REQUEST,
    CLOSEOUT_CONSISTENCY_REPORT,
    DIRECT_SPEC_AUDIT_RECORD,
    DIRECT_SPEC_VERIFICATION_REPORT,
    FUTURE_BRANCH_REPORT,
    HUMAN_DECISION_RECORD,
    TASK_START_CHECKLIST,
    TEAM_PLAN,
    WORKFLOW_RUN_RECORD,
    parse_todo_dispatch_state,
    prepare_idea_task,
    prepare_task,
    validate_closeout_consistency,
    verify_direct_spec_task,
)


SCHEMA_NAMES = [
    "task_start_checklist",
    "command_request",
    "human_decision_record",
    "workflow_run_record",
    "authority_coverage_matrix",
    "team_plan",
    "future_branch_report",
    "child_agent_result",
    "child_result_merge_package",
    "swarm_execution_record",
    "lane_plan",
    "lane_convergence_report",
    "aas5_audit_record",
    "swarm_topology_graph",
    "execution_parallelism_record",
    "direct_spec_audit_record",
    "direct_spec_verification_report",
    "closeout_consistency_report",
]


class TaskHardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "task_hardening_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_task_hardening_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        (self.repo_root / "docs" / "schemas").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "task_claims").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "handoffs" / "applied").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "specifications").mkdir(parents=True, exist_ok=True)
        self._copy_schemas()
        self._write_todo()

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_parse_todo_dispatch_state_handles_tranche_and_parallel_entries(self) -> None:
        text = (self.repo_root / "docs" / "TODO.md").read_text(encoding="utf-8")
        parsed = parse_todo_dispatch_state(text)
        self.assertEqual(parsed["next_dispatchable"]["kind"], "tranche")
        self.assertEqual(parsed["next_dispatchable"]["task_ids"], ["T-303", "T-306", "T-305", "T-307"])
        self.assertEqual(len(parsed["user_dispatch_entries"]), 3)
        self.assertEqual(parsed["user_dispatch_entries"][0]["label"], "PARALLEL")
        self.assertEqual(parsed["user_dispatch_order"][:4], ["T-303", "T-306", "T-305", "T-307"])

    def test_control_plane_dispatchable_uses_tranche_first_tasks(self) -> None:
        plane = object.__new__(AtrahasisControlPlane)
        plane.docs_root = self.repo_root / "docs"
        payload = AtrahasisControlPlane.get_dispatchable_tasks(plane, limit=4)
        self.assertEqual(payload["next_dispatchable_canonical_task"], "T-303")
        self.assertEqual(payload["tasks"][0]["task_id"], "T-303")
        self.assertEqual(payload["user_dispatch_entries"][0]["task_ids"], ["T-303", "T-306", "T-305", "T-307"])

    def test_prepare_task_bootstraps_direct_spec_workspace(self) -> None:
        self._write_claim(
            "T-303",
            status="CLAIMED",
            agent_name="Zababa",
            safe_zone_paths=[
                "docs/specifications/C5 - Proof-Carrying Verification Membrane/C5_Proof-Carrying_Verification_Membrane_Master_Tech_Spec.md"
            ],
            target_specs=["C5"],
            notes="Remove bridged provenance caveats and MCP-era assumptions.",
        )
        result = prepare_task(self.repo_root, task_id="T-303", agent_name="Zababa")
        workspace = self.repo_root / "docs" / "task_workspaces" / "T-303"
        self.assertTrue((workspace / "README.md").exists())
        self.assertTrue((workspace / "TASK_BRIEF.md").exists())
        checklist = json.loads((workspace / TASK_START_CHECKLIST).read_text(encoding="utf-8"))
        audit = json.loads((workspace / DIRECT_SPEC_AUDIT_RECORD).read_text(encoding="utf-8"))
        self.assertEqual(result["task_class"], "DIRECT_SPEC")
        self.assertTrue(checklist["readiness_checks"]["dispatchable_now"])
        self.assertIn("verify_direct_spec_task.py", " ".join(checklist["notes"]))
        self.assertEqual(audit["target_specs"], ["C5"])
        self.assertIn("bridge", audit["forbidden_patterns"])

    def test_verify_direct_spec_task_detects_and_clears_forbidden_patterns(self) -> None:
        target = self._write_claimed_spec(
            task_id="T-303",
            spec_id="C5",
            spec_dir="C5 - Proof-Carrying Verification Membrane",
            filename="C5_Proof-Carrying_Verification_Membrane_Master_Tech_Spec.md",
            body="Legacy bridged provenance remains here.\n",
        )
        self._write_claim(
            "T-303",
            status="IN_PROGRESS",
            agent_name="Zababa",
            safe_zone_paths=[self._rel(target)],
            target_specs=["C5"],
            notes="Remove bridged provenance caveats.",
        )
        prepare_task(self.repo_root, task_id="T-303", agent_name="Zababa")
        report = verify_direct_spec_task(self.repo_root, task_id="T-303")
        self.assertFalse(report["clean"])
        self.assertEqual(report["matches"][0]["path"], self._rel(target))

        target.write_text("Native provenance only.\n", encoding="utf-8")
        clean_report = verify_direct_spec_task(self.repo_root, task_id="T-303")
        self.assertTrue(clean_report["clean"])
        self.assertEqual(clean_report["match_count"], 0)

    def test_validate_closeout_consistency_flags_live_handoff_and_dispatch_residue(self) -> None:
        target = self._write_claimed_spec(
            task_id="T-303",
            spec_id="C5",
            spec_dir="C5 - Proof-Carrying Verification Membrane",
            filename="C5_Proof-Carrying_Verification_Membrane_Master_Tech_Spec.md",
            body="Native provenance only.\n",
        )
        self._write_claim(
            "T-303",
            status="DONE",
            agent_name="Zababa",
            safe_zone_paths=[self._rel(target)],
            target_specs=["C5"],
            notes="Retrofit complete.",
        )
        prepare_task(self.repo_root, task_id="T-303", agent_name="Zababa")
        verify_direct_spec_task(self.repo_root, task_id="T-303")
        live_handoff = self.repo_root / "docs" / "handoffs" / "T-303_CODEX_HANDOFF.md"
        live_handoff.write_text("# handoff\n", encoding="utf-8")

        report = validate_closeout_consistency(self.repo_root, task_id="T-303")
        self.assertFalse(report["valid"])
        check_map = {item["name"]: item for item in report["checks"]}
        self.assertFalse(check_map["done_claim_removed_from_dispatch_order"]["passed"])
        self.assertFalse(check_map["no_live_handoff_when_done"]["passed"])
        self.assertTrue((self.repo_root / "docs" / "task_workspaces" / "T-303" / CLOSEOUT_CONSISTENCY_REPORT).exists())

    def test_prepare_idea_task_auto_mints_analysis_workspace_with_ideation_artifacts(self) -> None:
        payload = prepare_idea_task(
            self.repo_root,
            title="Independent Model Inference Microservice Layer",
            prompt="Evaluate whether this candidate belongs back in the architecture.",
            agent_name="Ningirsu",
            authority_surfaces=["C45", "C42", "C47", "T-300"],
        )
        self.assertTrue(payload["auto_minted"])
        self.assertEqual(payload["task_id"], "T-9000")

        workspace = self.repo_root / "docs" / "task_workspaces" / "T-9000"
        self.assertTrue((workspace / "README.md").exists())
        self.assertTrue((workspace / "TASK_BRIEF.md").exists())
        self.assertTrue((workspace / COMMAND_REQUEST).exists())
        self.assertTrue((workspace / HUMAN_DECISION_RECORD).exists())
        self.assertTrue((workspace / WORKFLOW_RUN_RECORD).exists())
        self.assertTrue((workspace / AUTHORITY_COVERAGE_MATRIX).exists())
        self.assertTrue((workspace / TEAM_PLAN).exists())
        self.assertTrue((workspace / FUTURE_BRANCH_REPORT).exists())
        self.assertTrue((workspace / CHILD_RESULT_MERGE_PACKAGE).exists())
        self.assertTrue((workspace / "SWARM_TOPOLOGY_GRAPH.json").exists())
        self.assertTrue((workspace / "EXECUTION_PARALLELISM_RECORD.json").exists())
        self.assertTrue((workspace / "LANE_PLAN_alpha.yaml").exists())
        self.assertTrue((workspace / "LANE_CONVERGENCE_REPORT_alpha.json").exists())
        self.assertTrue((workspace / "SWARM_COMPLIANCE_AUDIT.json").exists())
        self.assertTrue((workspace / "children" / "managers" / "mgr.alpha.json").exists())
        self.assertTrue((workspace / "children" / "workers" / "wrk.alpha.visionary.json").exists())
        self.assertTrue((workspace / "children" / "reporters" / "rep.alpha.json").exists())
        self.assertTrue((workspace / "children" / "auditors" / "aud.compliance.json").exists())

        checklist = json.loads((workspace / TASK_START_CHECKLIST).read_text(encoding="utf-8"))
        self.assertEqual(checklist["task_class"], "FULL_PIPELINE")
        self.assertEqual(checklist["write_surface"]["source"], "AASNI_auto_mint")
        self.assertIn("Read the contents of current claim YAML files", " ".join(checklist["notes"]))
        self.assertIn("does not count as canonical shared-state progression", " ".join(checklist["notes"]))
        self.assertIn(FUTURE_BRANCH_REPORT, checklist["required_artifacts"])
        self.assertEqual(len([item for item in checklist["required_artifacts"] if item.startswith("children/")]), 24)

        human_decision = json.loads((workspace / HUMAN_DECISION_RECORD).read_text(encoding="utf-8"))
        self.assertEqual(human_decision["workflow_status"], "BLOCKED_PENDING_SWARM_VALIDATION")
        self.assertFalse(human_decision["recommendation_authorized"])

        authority_matrix = json.loads((workspace / AUTHORITY_COVERAGE_MATRIX).read_text(encoding="utf-8"))
        self.assertEqual(authority_matrix["doctrine_version"], "AAS5")
        self.assertEqual(authority_matrix["new_semantic_authority_test"]["verdict"], "pending")
        self.assertEqual(authority_matrix["surface_rows"][0]["coverage_status"], "MISSING")

        team_plan = load_yaml(workspace / TEAM_PLAN)
        self.assertEqual(team_plan["doctrine_version"], "AAS5")
        self.assertEqual(team_plan["topology_mode"], "AAS5_25_AGENT_HIERARCHY")
        self.assertEqual(team_plan["spawn_policy"]["team_mode"], "FUTURE_BRANCH_SWARM")
        self.assertEqual(team_plan["spawn_policy"]["orchestration_topology"], "master_lane_managers_reporters_auditors")
        self.assertEqual(team_plan["spawn_policy"]["manager_count"], 4)
        self.assertEqual(team_plan["spawn_policy"]["reporter_count"], 4)
        self.assertEqual(team_plan["spawn_policy"]["auditor_count"], 4)
        self.assertEqual(team_plan["spawn_policy"]["worker_count"], 12)
        self.assertEqual(team_plan["spawn_policy"]["total_non_parent_participants"], 24)
        self.assertEqual(team_plan["spawn_policy"]["total_agents"], 25)
        self.assertEqual(team_plan["spawn_policy"]["max_live_children"], 6)
        self.assertEqual(team_plan["spawn_policy"]["spawn_batch_size"], 6)
        self.assertEqual(team_plan["spawn_policy"]["planned_wave_count"], 5)
        self.assertEqual(team_plan["spawn_policy"]["scheduling_mode"], "batched_by_runtime_cap")
        self.assertEqual(len(team_plan["manager_orchestrators"]), 4)
        self.assertTrue(all(item["managed_child_count"] == 3 for item in team_plan["manager_orchestrators"]))
        self.assertEqual({item["lane_id"] for item in team_plan["manager_orchestrators"]}, {"alpha", "beta", "gamma", "radical"})
        self.assertEqual(len(team_plan["lane_convergence_reporters"]), 4)
        self.assertEqual(len(team_plan["audit_orchestrators"]), 4)
        self.assertEqual(len(team_plan["workers"]), 12)
        self.assertEqual(len(team_plan["children"]), 24)
        self.assertEqual(team_plan["parent"]["node_id"], "mst")
        self.assertEqual(team_plan["future_exploration"]["current_stage"], "IDEATION")
        self.assertEqual(team_plan["parent"]["model_audit"]["observed_model_auditability"], "runtime_not_exposed")
        self.assertEqual(team_plan["children"][0]["model_audit"]["observed_model_auditability"], "runtime_not_exposed")
        self.assertEqual(
            set(team_plan["future_exploration"]["improvement_trigger_policy"]["lane_order"]),
            {"alpha", "beta", "gamma", "radical"},
        )
        branch_report = json.loads((workspace / FUTURE_BRANCH_REPORT).read_text(encoding="utf-8"))
        self.assertEqual(branch_report["doctrine_version"], "AAS5")
        self.assertEqual(branch_report["team_mode"], "FUTURE_BRANCH_SWARM")
        self.assertFalse(branch_report["recommendation_authorized"])
        self.assertEqual(len(branch_report["lane_summaries"]), 4)
        self.assertEqual(len(branch_report["branches"]), 12)
        self.assertIn("visionary:frame_replacement", {item["branch_id"] for item in branch_report["branches"]})

        child_result = json.loads(
            (workspace / "children" / "workers" / "wrk.alpha.visionary.json").read_text(encoding="utf-8")
        )
        self.assertEqual(child_result["node_id"], "wrk.alpha.visionary")
        self.assertEqual(child_result["artifact_provenance"]["writer_mode"], "bootstrap_placeholder")
        self.assertEqual(child_result["artifact_provenance"]["owner_node_id"], "wrk.alpha.visionary")
        self.assertEqual(child_result["model_audit"]["observed_model_auditability"], "runtime_not_exposed")

        swarm_record = json.loads((workspace / "SWARM_EXECUTION_RECORD.json").read_text(encoding="utf-8"))
        self.assertEqual(swarm_record["doctrine_version"], "AAS5")
        self.assertEqual(len(swarm_record["required_node_ids"]), 25)
        self.assertEqual(swarm_record["parent_session"]["model_audit"]["observed_model_auditability"], "runtime_not_exposed")
        self.assertFalse(swarm_record["recommendation_authorized"])

        registry = StageContractRegistry(self.repo_root)
        report = registry.evaluate(task_id="T-9000", task_class="FULL_PIPELINE", current_stage="IDEATION")
        self.assertFalse(report["satisfied"])
        self.assertIn("validator:swarm_execution", report["missing_requirements"])

    def test_prepare_idea_task_still_scaffolds_noncanonical_workspace_under_no_shared_state_constraints(self) -> None:
        payload = prepare_idea_task(
            self.repo_root,
            title="Exploratory Capacity Plane",
            prompt="Evaluate whether this candidate belongs back in the architecture.",
            agent_name="Ningirsu",
            authority_surfaces=["C45"],
            operator_constraints=[
                "do not add it to docs/TODO.md",
                "do not claim a canonical task",
                "do not edit shared state yet",
            ],
        )
        workspace = self.repo_root / "docs" / "task_workspaces" / payload["task_id"]
        self.assertTrue((workspace / TASK_START_CHECKLIST).exists())
        self.assertTrue((workspace / TEAM_PLAN).exists())
        checklist = json.loads((workspace / TASK_START_CHECKLIST).read_text(encoding="utf-8"))
        self.assertEqual(checklist["write_surface"]["mode"], "exploratory_task_workspace")
        self.assertIn("does not count as canonical shared-state progression", " ".join(checklist["notes"]))

    def test_prepare_idea_task_honors_full_pipeline_task_prompt_modifier(self) -> None:
        prompt = "\n".join(
            [
                "Full Pipeline Task:",
                "Treat the following as a candidate new FULL PIPELINE task, but do not add it to docs/TODO.md, do not claim a canonical task, and do not edit shared state yet.",
                "",
                "Run AAS5 in IDEATION mode only.",
            ]
        )
        payload = prepare_idea_task(
            self.repo_root,
            title="Independent Model Inference Microservice Layer",
            prompt=prompt,
            agent_name="Ningirsu",
            authority_surfaces=["C45", "C42", "C47", "T-300"],
        )
        workspace = self.repo_root / "docs" / "task_workspaces" / payload["task_id"]
        command_request = load_yaml(workspace / COMMAND_REQUEST)
        human_decision = json.loads((workspace / HUMAN_DECISION_RECORD).read_text(encoding="utf-8"))
        checklist = json.loads((workspace / TASK_START_CHECKLIST).read_text(encoding="utf-8"))

        self.assertEqual(command_request["command_modifier"], "AASNI")
        self.assertFalse(str(command_request["prompt"]).startswith("Full Pipeline Task:"))
        self.assertIn("STRICT_FULL_PIPELINE_TASK", command_request["operator_constraints"])
        self.assertIn("ABGR_SWARM_REQUIRED", command_request["operator_constraints"])
        self.assertIn("NO_PARENT_ONLY_ADVISORY_FALLBACK", command_request["operator_constraints"])
        self.assertIn("TASK_ROUTING_REQUIRED", command_request["operator_constraints"])
        self.assertIn("STRICT_FULL_PIPELINE_TASK", human_decision["constraints"])
        self.assertTrue(
            any("Parent-only advisory analysis is forbidden" in item for item in human_decision["blocking_gates"])
        )
        self.assertTrue(
            any("Judgment-call downgrade to parent-only advisory mode is forbidden" in item for item in checklist["notes"])
        )
        self.assertTrue((workspace / TEAM_PLAN).exists())
        self.assertTrue((workspace / FUTURE_BRANCH_REPORT).exists())

    def test_prepare_idea_task_extracts_authority_surfaces_from_prompt_and_infers_agent_name(self) -> None:
        self._write_agent_state(["Ningirsu"])
        prompt = "\n".join(
            [
                "Full Pipeline Task:",
                "Evaluate this candidate against C45, C42, C47, C36, C18, C22, C39, and T-300.",
                "Run AAS5 in IDEATION mode only.",
            ]
        )
        payload = prepare_idea_task(
            self.repo_root,
            title="Prompt Extracted Authority Coverage",
            prompt=prompt,
            agent_name=None,
            authority_surfaces=[],
        )
        workspace = self.repo_root / "docs" / "task_workspaces" / payload["task_id"]
        checklist = json.loads((workspace / TASK_START_CHECKLIST).read_text(encoding="utf-8"))
        authority_matrix = json.loads((workspace / AUTHORITY_COVERAGE_MATRIX).read_text(encoding="utf-8"))
        team_plan = load_yaml(workspace / TEAM_PLAN)

        self.assertEqual(checklist["agent_name"], "Ningirsu")
        self.assertTrue(authority_matrix["coverage_required"])
        self.assertEqual(
            authority_matrix["named_authority_surfaces"],
            ["C45", "C42", "C47", "C36", "C18", "C22", "C39", "T-300"],
        )
        self.assertEqual(team_plan["parent"]["agent_name"], "Ningirsu")
        self.assertEqual(payload["authority_surfaces"], ["C45", "C42", "C47", "C36", "C18", "C22", "C39", "T-300"])

    def _copy_schemas(self) -> None:
        for name in SCHEMA_NAMES:
            source = REPO_ROOT / "docs" / "schemas" / f"{name}.schema.json"
            destination = self.repo_root / "docs" / "schemas" / f"{name}.schema.json"
            shutil.copy2(source, destination)

    def _write_todo(self) -> None:
        text = "\n".join(
            [
                "# AAS TODO List",
                "",
                "Next dispatchable canonical tranche: `PARALLEL` - `T-303` + `T-306` + one of `T-305 / T-307`.",
                "",
                "| ID | Task | Type | Priority | Dependencies | Notes |",
                "|----|------|------|----------|--------------|-------|",
                "| T-303 | Verification, Memory, and Provenance Retrofit | DIRECT SPEC | HIGH | T-301, T-240, T-252, T-290 | Remove bridged provenance caveats. |",
                "| T-305 | Implementation Plan and Wave Sequencing Rewrite | Governance | HIGH | T-301 | Shared governance rewrite. |",
                "| T-306 | Interface and Developer Experience Retrofit | DIRECT SPEC | MEDIUM | T-302, T-260, T-280 | Native AACP/AASL workflows. |",
                "| T-307 | Sub-Agent Loci Conversion Strategy | Governance | HIGH | T-300, T-252, T-291 | Governance/shared-doc lane. |",
                "",
                "## User Dispatch Order (Simple)",
                "",
                "1. `PARALLEL` - `T-303` + `T-306` + one of `T-305 / T-307`",
                "2. `SOLO after T-307` - `T-308`",
                "3. `SOLO after T-308` - `T-309`",
                "",
                "---",
            ]
        )
        (self.repo_root / "docs" / "TODO.md").write_text(text, encoding="utf-8")

    def _write_agent_state(self, names: list[str]) -> None:
        entries = []
        for index, name in enumerate(names):
            entries.extend(
                [
                    f'  - agent_name: "{name}"',
                    '    cli_platform: "OpenAI Codex"',
                    '    provider: "codex"',
                    f'    session_id: "codex-{name.lower()}-{index}"',
                    "    current_task: null",
                    '    registered_at: "2026-03-16T00:00:00Z"',
                    '    status: "ACTIVE"',
                    "    supported_agent_types:",
                    '      - "director"',
                ]
            )
        content = "\n".join(
            [
                'version: "1.0"',
                'stage: "ARCHITECTURE_REWRITE"',
                'status: "ALTERNATIVE_C_ZERO_BRIDGE_PIVOT"',
                'last_updated: "2026-03-16T00:00:00Z"',
                'last_updated_by: "Director"',
                "active_sessions:",
                *entries,
                "",
            ]
        )
        (self.repo_root / "docs" / "AGENT_STATE.md").write_text(content, encoding="utf-8")

    def _write_claim(
        self,
        task_id: str,
        *,
        status: str,
        agent_name: str,
        safe_zone_paths: list[str],
        target_specs: list[str],
        notes: str,
    ) -> None:
        claim = {
            "task_id": task_id,
            "invention_ids": [],
            "target_specs": target_specs,
            "title": "Synthetic claim",
            "platform": "CODEX",
            "agent_name": agent_name,
            "claimed_at": "2026-03-15T00:00:00Z",
            "updated_at": "2026-03-15T00:00:00Z",
            "status": status,
            "scope": {
                "safe_zone_paths": safe_zone_paths,
                "pipeline_type": "DIRECT_EDIT",
            },
            "notes": notes,
        }
        path = self.repo_root / "docs" / "task_claims" / f"{task_id}.yaml"
        path.write_text(
            "\n".join(
                [
                    f"task_id: {claim['task_id']}",
                    "invention_ids: []",
                    "target_specs:",
                    *[f"- {item}" for item in target_specs],
                    f"title: {claim['title']}",
                    "platform: CODEX",
                    f"agent_name: {agent_name}",
                    "claimed_at: '2026-03-15T00:00:00Z'",
                    "updated_at: '2026-03-15T00:00:00Z'",
                    f"status: {status}",
                    "scope:",
                    "  safe_zone_paths:",
                    *[f"  - {item}" for item in safe_zone_paths],
                    "  pipeline_type: DIRECT_EDIT",
                    f"notes: {notes}",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def _write_claimed_spec(self, *, task_id: str, spec_id: str, spec_dir: str, filename: str, body: str) -> Path:
        path = self.repo_root / "docs" / "specifications" / spec_dir
        path.mkdir(parents=True, exist_ok=True)
        target = path / filename
        target.write_text(body, encoding="utf-8")
        return target

    def _rel(self, path: Path) -> str:
        return str(path.relative_to(self.repo_root)).replace("\\", "/")


if __name__ == "__main__":
    unittest.main()
