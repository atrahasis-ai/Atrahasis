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

from aas1.human_decision_interface import HumanDecisionInterface
from aas1.invention_pipeline_manager import InventionPipelineManager


class HumanReviewOptionSynthesisTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path.home() / ".codex" / "memories" / "option_synthesis_tests"
        root.mkdir(parents=True, exist_ok=True)
        self.tempdir = root / f"localtmp_option_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir
        self.task_root = self.repo_root / "docs" / "task_workspaces" / "T-9002"
        self.task_root.mkdir(parents=True, exist_ok=True)
        self.interface = HumanDecisionInterface()

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_render_prompt_surfaces_improved_and_radical_paths(self) -> None:
        self._write_json(
            "HUMAN_DECISION_RECORD.json",
            {
                "decision_type": "OPERATOR_GUIDANCE",
                "task_id": "T-9002",
                "workflow_status": "PENDING_HUMAN_REVIEW",
                "prompt": "Design a stronger architecture.",
                "research_strategy_summary": "Baseline architecture path is viable.",
                "evidence_summary": {
                    "modifier": "AASA",
                    "priority_zones": ["architecture"],
                    "contradiction_count": 2,
                    "strategy_summary": "Baseline architecture path is viable.",
                },
                "options": [],
                "operator_decision": "PENDING",
                "constraints": [],
            },
        )
        self._write_json(
            "EXPLORATION_CONTROL_RECORD.json",
            {
                "escalate_to_human": True,
                "recommended_branch_budget": 2,
                "priority_order": ["alpha", "beta", "gamma"],
            },
        )
        self._write_json(
            "TASK_IMPROVEMENT_REPORT.json",
            {
                "type": "TASK_IMPROVEMENT_REPORT",
                "task_id": "T-9002",
                "workflow_id": "wf-1",
                "dispatch_id": "dispatch-1",
                "current_stage": "DESIGN",
                "generated_at": "2026-03-15T12:00:00Z",
                "trigger_policy": {
                    "enabled": True,
                    "trigger_reasons": ["task_class_has_design_surface"],
                    "decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"],
                    "lane_ids": ["alpha", "beta", "gamma"],
                    "lane_order": ["alpha", "beta", "gamma"],
                },
                "lane_summaries": [],
                "parent_decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"],
                "recommended_parent_action": "hybridize",
                "summary": "Blend the strongest Alpha and Beta branches into a stronger design path.",
                "source_refs": {},
            },
        )
        self._write_json(
            "RADICAL_REDESIGN_REPORT.json",
            {
                "type": "RADICAL_REDESIGN_REPORT",
                "task_id": "T-9002",
                "workflow_id": "wf-1",
                "dispatch_id": "dispatch-1",
                "current_stage": "DESIGN",
                "generated_at": "2026-03-15T12:01:00Z",
                "trigger_policy": {
                    "enabled": True,
                    "trigger_reasons": ["gamma_lane_present"],
                    "decision_options": ["reject", "hybridize", "promote"],
                    "radical_branch_ids": ["critic:governance_break"],
                },
                "radical_branch_summaries": [],
                "parent_decision_options": ["reject", "hybridize", "promote"],
                "summary": "A radical topology rewrite could unlock a higher-ceiling architecture.",
                "source_refs": {},
            },
        )
        self._write_json(
            "CONVERGENCE_GATE_RECORD.json",
            {
                "type": "CONVERGENCE_GATE_RECORD",
                "task_id": "T-9002",
                "current_stage": "DESIGN",
                "required_before_stage_close": True,
                "convergence_status": "READY_FOR_DECISION",
                "ready_for_decision": True,
                "satisfied": False,
                "branch_count": 3,
                "minimum_completed_branches": 2,
                "completed_branch_count": 2,
                "disagreement_signals": ["alpha_vs_beta_tradeoff"],
                "recommended_parent_action": "hybridize",
                "decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl", "promote"],
                "gamma_present": True,
                "requires_gamma_disposition": True,
                "selected_disposition": None,
                "rationale": None,
                "started_at": "2026-03-15T12:02:00Z",
                "completed_at": None,
                "source_refs": {},
                "source": "test",
                "notes": [],
                "updated_at": "2026-03-15T12:02:00Z",
            },
        )

        prompt = self.interface.render_prompt_for_task(task_workspace=self.task_root)
        self.assertIn("Operator Path Options:", prompt)
        self.assertIn("Current Path [current_path]", prompt)
        self.assertIn("Hybrid Path [hybrid_path]", prompt)
        self.assertIn("Radical Path [radical_path]", prompt)
        self.assertIn("Respond with one of:", prompt)
        self.assertIn("- hybrid_path: Hybrid Path", prompt)

    def test_manager_regenerates_prompt_from_task_local_artifacts(self) -> None:
        self._write_json(
            "HUMAN_DECISION_RECORD.json",
            {
                "decision_type": "OPERATOR_GUIDANCE",
                "task_id": "T-9002",
                "workflow_status": "PENDING_HUMAN_REVIEW",
                "prompt": "Original task prompt.",
                "research_strategy_summary": "Baseline path.",
                "evidence_summary": {
                    "modifier": "AASA",
                    "priority_zones": ["architecture"],
                    "contradiction_count": 1,
                    "strategy_summary": "Baseline path.",
                },
                "options": [],
                "operator_decision": "PENDING",
                "constraints": [],
            },
        )
        self._write_json(
            "EXPLORATION_CONTROL_RECORD.json",
            {
                "escalate_to_human": False,
                "recommended_branch_budget": 1,
                "priority_order": ["alpha"],
            },
        )
        self._write_json(
            "TASK_IMPROVEMENT_REPORT.json",
            {
                "type": "TASK_IMPROVEMENT_REPORT",
                "task_id": "T-9002",
                "workflow_id": "wf-1",
                "dispatch_id": "dispatch-1",
                "current_stage": "RESEARCH",
                "generated_at": "2026-03-15T12:05:00Z",
                "trigger_policy": {
                    "enabled": True,
                    "trigger_reasons": ["task_class_has_design_surface"],
                    "decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"],
                    "lane_ids": ["alpha", "beta", "gamma"],
                    "lane_order": ["alpha", "beta", "gamma"],
                },
                "lane_summaries": [],
                "parent_decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"],
                "recommended_parent_action": "adopt",
                "summary": "A better path was found.",
                "source_refs": {},
            },
        )

        manager = object.__new__(InventionPipelineManager)
        manager.repo_root = self.repo_root
        manager.human_decision = HumanDecisionInterface()

        prompt = InventionPipelineManager.render_operator_prompt(manager, task_id="T-9002")
        self.assertIn("Improved Path", prompt)
        self.assertIn("Respond with one of:", prompt)

    def _write_json(self, filename: str, payload: dict[str, object]) -> None:
        (self.task_root / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
