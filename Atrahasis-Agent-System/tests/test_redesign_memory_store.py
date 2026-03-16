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
from aas1.redesign_memory_store import RedesignMemoryStore
from aas1.workflow_policy_engine import WorkflowPolicyEngine


class RedesignMemoryStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "redesign_memory_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_redesign_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        (self.repo_root / "docs" / "task_workspaces" / "T-9001").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "task_workspaces" / "T-9002").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "task_workspaces" / "T-9003").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "runtime" / "state").mkdir(parents=True, exist_ok=True)
        self._write_text(
            self.repo_root / "docs" / "TODO.md",
            "\n".join(
                [
                    "# TODO",
                    "",
                    "| ID | Task | Type | Priority | Dependencies | Notes |",
                    "|----|------|------|----------|--------------|-------|",
                    "| T-9001 | Authority boundary redesign | Analysis | HIGH | none | Synthetic redesign memory seed |",
                    "| T-9002 | Runtime topology redesign | Analysis | HIGH | none | Synthetic redesign memory target |",
                    "| T-9003 | Runtime topology retrofit | DIRECT_SPEC | HIGH | none | Synthetic direct-spec redesign target |",
                ]
            ),
        )
        self.store = RedesignMemoryStore(self.repo_root)

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_ingest_and_snapshot_include_current_entry(self) -> None:
        update = self.store.ingest_task(
            task_id="T-9001",
            workflow_context=self._workflow_context(
                task_id="T-9001",
                prompt="Redesign the authority boundary and runtime topology for the sovereign protocol stack.",
            ),
            workflow_policy=self._workflow_policy(task_id="T-9001", title="Authority boundary redesign"),
            future_convergence_report=self._future_convergence("T-9001"),
            task_improvement_report=self._task_improvement(
                "T-9001",
                summary="A hybrid authority boundary reduces governance friction while keeping strong isolation.",
            ),
            radical_redesign_report=self._radical_redesign(
                "T-9001",
                summary="A radical sovereignty split could unlock a cleaner runtime boundary.",
            ),
            convergence_gate_record=self._convergence_gate("hybridize"),
            adversarial_review_record=self._adversarial_review(),
            closeout_execution_record={"workflow_status": "COMPLETED"},
        )
        self.assertIsNotNone(update)
        self.assertTrue(update["changed"])

        snapshot = self.store.snapshot_for_task(
            task_id="T-9001",
            workflow_context=self._workflow_context(
                task_id="T-9001",
                prompt="Redesign the authority boundary and runtime topology for the sovereign protocol stack.",
            ),
            workflow_policy=self._workflow_policy(task_id="T-9001", title="Authority boundary redesign"),
        )
        self.assertEqual(snapshot["current_entry"]["task_id"], "T-9001")
        self.assertEqual(snapshot["current_entry"]["selected_disposition"], "HYBRIDIZE")
        self.assertIn("authority", " ".join(snapshot["query_terms"]).lower())

    def test_control_plane_surfaces_related_redesign_memory(self) -> None:
        self.store.ingest_task(
            task_id="T-9001",
            workflow_context=self._workflow_context(
                task_id="T-9001",
                prompt="Redesign the runtime authority boundary and topology for the sovereign stack.",
            ),
            workflow_policy=self._workflow_policy(task_id="T-9001", title="Authority boundary redesign"),
            future_convergence_report=self._future_convergence("T-9001"),
            task_improvement_report=self._task_improvement(
                "T-9001",
                summary="A hybrid authority boundary reduces governance friction while keeping strong isolation.",
            ),
            radical_redesign_report=self._radical_redesign(
                "T-9001",
                summary="A radical runtime split could unlock cleaner sovereignty boundaries.",
            ),
            convergence_gate_record=self._convergence_gate("hybridize"),
            adversarial_review_record=self._adversarial_review(),
            closeout_execution_record={"workflow_status": "COMPLETED"},
        )
        self.store.ingest_task(
            task_id="T-9002",
            workflow_context=self._workflow_context(
                task_id="T-9002",
                prompt="Evaluate runtime topology and authority-boundary improvements for the sovereign execution mesh.",
            ),
            workflow_policy=self._workflow_policy(task_id="T-9002", title="Runtime topology redesign"),
            future_convergence_report=self._future_convergence("T-9002"),
            task_improvement_report=self._task_improvement(
                "T-9002",
                summary="A better runtime topology was found by hybridizing the strongest Alpha and Beta lanes.",
            ),
            convergence_gate_record=self._convergence_gate("adopt"),
            closeout_execution_record={"workflow_status": "READY_FOR_CLOSEOUT"},
        )
        self._write_json(
            self.repo_root / "runtime" / "state" / "workflows" / "T-9002" / "latest.json",
            self._workflow_context(
                task_id="T-9002",
                prompt="Evaluate runtime topology and authority-boundary improvements for the sovereign execution mesh.",
            )["workflow"],
        )
        control = AtrahasisControlPlane(self.repo_root)
        redesign_memory = control.get_redesign_memory(task_id="T-9002", limit_related=3)
        self.assertGreaterEqual(redesign_memory["redesign_memory"]["related_entry_count"], 1)
        self.assertEqual(redesign_memory["redesign_memory"]["related_entries"][0]["task_id"], "T-9001")

        search = control.search_redesign_memory(
            query="authority boundary runtime topology sovereign",
            task_class="ANALYSIS",
            current_stage="DESIGN",
            limit=5,
        )
        self.assertGreaterEqual(search["match_count"], 1)
        self.assertEqual(search["matches"][0]["entry"]["task_id"], "T-9001")

    def test_workflow_policy_uses_redesign_memory_for_adversarial_review(self) -> None:
        self.store.ingest_task(
            task_id="T-9001",
            workflow_context=self._workflow_context(
                task_id="T-9001",
                prompt="Redesign the runtime authority boundary and topology for the sovereign stack.",
            ),
            workflow_policy=self._workflow_policy(task_id="T-9001", title="Authority boundary redesign"),
            future_convergence_report=self._future_convergence("T-9001"),
            task_improvement_report=self._task_improvement(
                "T-9001",
                summary="A previous redesign attempt found a better topology but failed under adversarial review.",
            ),
            convergence_gate_record=self._convergence_gate("reject"),
            adversarial_review_record={
                "review_status": "REVIEW_BLOCKED",
                "adversarial_policy": {
                    "trigger_reasons": ["architecture_improvement_pressure_detected"],
                },
            },
            closeout_execution_record={"workflow_status": "COMPLETED"},
        )
        engine = WorkflowPolicyEngine(self.repo_root)
        seed = engine.evaluate(
            task_id="T-9003",
            workflow_context=self._workflow_context(
                task_id="T-9003",
                prompt="Retrofit the runtime topology and authority boundary for the sovereign execution mesh.",
                command_modifier="AASBT",
                scope="buildout_task",
            ),
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        seed["current_stage"] = "SPECIFICATION"
        seed["next_stage"] = "ASSESSMENT"
        seed["stage_history"] = [
            {
                "stage": "SPECIFICATION",
                "status": "READY",
                "opened_at": "2026-03-15T00:00:00Z",
                "updated_at": "2026-03-15T00:00:00Z",
                "closed_at": None,
                "transition_reason": "test_seed",
            }
        ]
        engine._write(task_id="T-9003", payload=seed)
        state = engine.evaluate(
            task_id="T-9003",
            workflow_context=self._workflow_context(
                task_id="T-9003",
                prompt="Retrofit the runtime topology and authority boundary for the sovereign execution mesh.",
                command_modifier="AASBT",
                scope="buildout_task",
            ),
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        self.assertTrue(state["adversarial_review"]["enabled"])
        self.assertTrue(state["adversarial_review"]["recommended_only"])
        self.assertIn("historical_adversarial_findings_detected", state["adversarial_review"]["trigger_reasons"])
        self.assertEqual(state["redesign_memory"]["policy_signals"]["adversarial_issue_count"], 1)

    def test_redesign_memory_strengthens_convergence_branch_coverage(self) -> None:
        self.store.ingest_task(
            task_id="T-9001",
            workflow_context=self._workflow_context(
                task_id="T-9001",
                prompt="Redesign the runtime authority boundary and topology for the sovereign stack.",
            ),
            workflow_policy=self._workflow_policy(task_id="T-9001", title="Authority boundary redesign"),
            future_convergence_report=self._future_convergence("T-9001"),
            task_improvement_report=self._task_improvement(
                "T-9001",
                summary="Repeated redesign pressure suggests the current runtime topology is plateauing.",
            ),
            radical_redesign_report=self._radical_redesign(
                "T-9001",
                summary="A gamma-lane sovereignty split remained unresolved but promising.",
            ),
            convergence_gate_record={
                "selected_disposition": "continue_exploration",
                "convergence_status": "DECIDED",
            },
            adversarial_review_record={
                "review_status": "REVIEW_CHANGES_REQUESTED",
                "adversarial_policy": {
                    "trigger_reasons": ["architecture_improvement_pressure_detected"],
                },
            },
            closeout_execution_record={"workflow_status": "COMPLETED"},
        )
        engine = WorkflowPolicyEngine(self.repo_root)
        seed = engine.evaluate(
            task_id="T-9002",
            workflow_context=self._workflow_context(
                task_id="T-9002",
                prompt="Evaluate runtime topology and authority-boundary improvements for the sovereign execution mesh.",
            ),
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        seed["current_stage"] = "RESEARCH"
        seed["next_stage"] = "ASSESSMENT"
        seed["stage_history"] = [
            {
                "stage": "RESEARCH",
                "status": "READY",
                "opened_at": "2026-03-15T00:00:00Z",
                "updated_at": "2026-03-15T00:00:00Z",
                "closed_at": None,
                "transition_reason": "test_seed",
            }
        ]
        engine._write(task_id="T-9002", payload=seed)
        future_convergence = {
            "type": "FUTURE_CONVERGENCE_REPORT",
            "task_id": "T-9002",
            "workflow_id": "t-9002-wf-1",
            "dispatch_id": "dispatch-1",
            "current_stage": "RESEARCH",
            "generated_at": "2026-03-15T00:09:00Z",
            "branch_count": 3,
            "branch_summaries": [
                {"branch_id": "visionary:conservative", "branch_label": "A", "parent_role": "visionary", "branch_kind": "conservative", "lane_id": "alpha", "lane_label": "Alpha", "lane_strategy": "improve", "objective": "A", "status": "COMPLETED", "verdicts": ["good"], "recommended_next_actions": ["compare"], "child_artifacts": []},
                {"branch_id": "visionary:aggressive", "branch_label": "B", "parent_role": "visionary", "branch_kind": "aggressive", "lane_id": "beta", "lane_label": "Beta", "lane_strategy": "reframe", "objective": "B", "status": "COMPLETED", "verdicts": ["better"], "recommended_next_actions": ["compare"], "child_artifacts": []},
                {"branch_id": "visionary:radical", "branch_label": "C", "parent_role": "visionary", "branch_kind": "radical", "lane_id": "gamma", "lane_label": "Gamma", "lane_strategy": "break", "objective": "C", "status": "DRAFT", "verdicts": [], "recommended_next_actions": [], "child_artifacts": []},
            ],
            "disagreement_signals": ["authority_boundary_tradeoff"],
            "convergence_summary": "Synthetic convergence summary.",
            "recommended_parent_action": "hybridize",
            "source_refs": {},
        }
        task_improvement = {
            "type": "TASK_IMPROVEMENT_REPORT",
            "task_id": "T-9002",
            "workflow_id": "t-9002-wf-1",
            "dispatch_id": "dispatch-1",
            "current_stage": "RESEARCH",
            "generated_at": "2026-03-15T00:10:00Z",
            "trigger_policy": {"enabled": True, "trigger_reasons": ["task_class_has_design_surface"], "decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"], "lane_ids": ["alpha", "beta", "gamma"], "lane_order": ["alpha", "beta", "gamma"]},
            "lane_summaries": [],
            "parent_decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"],
            "recommended_parent_action": "hybridize",
            "summary": "Synthetic task improvement summary.",
            "source_refs": {},
        }
        radical_redesign = {
            "type": "RADICAL_REDESIGN_REPORT",
            "task_id": "T-9002",
            "workflow_id": "t-9002-wf-1",
            "dispatch_id": "dispatch-1",
            "current_stage": "RESEARCH",
            "generated_at": "2026-03-15T00:11:00Z",
            "trigger_policy": {"enabled": True, "trigger_reasons": ["gamma_lane_present"], "decision_options": ["reject", "hybridize", "promote"], "radical_branch_ids": ["visionary:radical"]},
            "radical_branch_summaries": [],
            "parent_decision_options": ["reject", "hybridize", "promote"],
            "summary": "Synthetic radical summary.",
            "source_refs": {},
        }
        state = engine.evaluate(
            task_id="T-9002",
            workflow_context=self._workflow_context(
                task_id="T-9002",
                prompt="Evaluate runtime topology and authority-boundary improvements for the sovereign execution mesh.",
            ),
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            future_convergence_report=future_convergence,
            task_improvement_report=task_improvement,
            radical_redesign_report=radical_redesign,
            convergence_gate_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        self.assertEqual(state["convergence"]["minimum_completed_branches"], 3)
        self.assertEqual(state["convergence"]["status"], "PENDING_BRANCH_COMPLETION")
        self.assertIn("historical_pressure_requires_fuller_branch_coverage", state["convergence"]["trigger_reasons"])

    def _workflow_context(
        self,
        *,
        task_id: str,
        prompt: str,
        command_modifier: str = "AASA",
        scope: str = "architecture_question",
    ) -> dict[str, object]:
        return {
            "workflow": {
                "workflow_id": f"{task_id.lower()}-wf-1",
                "request": {
                    "task_id": task_id,
                    "command_modifier": command_modifier,
                    "scope": scope,
                    "prompt": prompt,
                },
            },
            "workflow_record": {"modifier": command_modifier},
        }

    def _workflow_policy(self, *, task_id: str, title: str) -> dict[str, object]:
        return {
            "task_profile": {
                "task_id": task_id,
                "title": title,
                "task_class": "ANALYSIS",
                "modifier": "AASA",
                "scope": "architecture_question",
            },
            "current_stage": "DESIGN",
        }

    def _future_convergence(self, task_id: str) -> dict[str, object]:
        return {
            "task_id": task_id,
            "workflow_id": f"{task_id.lower()}-wf-1",
            "dispatch_id": f"{task_id.lower()}-dispatch",
            "current_stage": "DESIGN",
            "branch_count": 3,
            "branch_summaries": [
                {"branch_id": "visionary:conservative", "lane_id": "alpha", "status": "COMPLETED"},
                {"branch_id": "visionary:aggressive", "lane_id": "beta", "status": "COMPLETED"},
                {"branch_id": "visionary:radical", "lane_id": "gamma", "status": "COMPLETED"},
            ],
            "disagreement_signals": ["authority_boundary_tradeoff"],
            "convergence_summary": "Alpha and Beta agree on a stronger runtime authority boundary with one material tradeoff.",
            "recommended_parent_action": "hybridize",
        }

    def _task_improvement(self, task_id: str, *, summary: str) -> dict[str, object]:
        return {
            "task_id": task_id,
            "workflow_id": f"{task_id.lower()}-wf-1",
            "dispatch_id": f"{task_id.lower()}-dispatch",
            "current_stage": "DESIGN",
            "summary": summary,
            "recommended_parent_action": "hybridize",
            "trigger_policy": {
                "trigger_reasons": ["task_class_has_design_surface", "novelty_pressure_low"],
            },
            "lane_summaries": [
                {"lane_id": "alpha"},
                {"lane_id": "beta"},
                {"lane_id": "gamma"},
            ],
        }

    def _radical_redesign(self, task_id: str, *, summary: str) -> dict[str, object]:
        return {
            "task_id": task_id,
            "workflow_id": f"{task_id.lower()}-wf-1",
            "dispatch_id": f"{task_id.lower()}-dispatch",
            "current_stage": "DESIGN",
            "summary": summary,
            "trigger_policy": {
                "trigger_reasons": ["gamma_lane_present", "task_class_requires_architecture_pressure"],
            },
            "radical_branch_summaries": [
                {"lane_id": "gamma"},
            ],
        }

    def _convergence_gate(self, selected_disposition: str) -> dict[str, object]:
        return {
            "selected_disposition": selected_disposition,
            "convergence_status": "DECIDED",
        }

    def _adversarial_review(self) -> dict[str, object]:
        return {
            "review_status": "REVIEW_APPROVED",
            "adversarial_policy": {
                "trigger_reasons": ["architecture_improvement_pressure_detected"],
            },
        }

    def _write_json(self, path: Path, payload: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _write_text(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
