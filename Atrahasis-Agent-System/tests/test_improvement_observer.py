from __future__ import annotations

import shutil
import sys
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from aas1.audit_timeline_store import AuditTimelineStore
from aas1.controller_run_registry import ControllerRunRegistry
from aas1.hitl_queue_store import HitlQueueStore
from aas1.improvement_observer import ImprovementObserver
from aas1.workflow_policy_engine import WorkflowPolicyEngine


class ImprovementObserverTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "improvement_observer_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_improvement_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        (self.repo_root / "runtime" / "state").mkdir(parents=True, exist_ok=True)
        self.timeline = AuditTimelineStore(self.repo_root)
        self.runs = ControllerRunRegistry(self.repo_root)
        self.hitl = HitlQueueStore(self.repo_root)
        self.workflow_policy = WorkflowPolicyEngine(self.repo_root)
        self.observer = ImprovementObserver(self.repo_root)

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_observer_surfaces_major_system_update_advisories_after_two_cycles(self) -> None:
        self._seed_policy(
            task_id="T-9001",
            pending_hitl_count=3,
            review_status="REVIEW_CHANGES_REQUESTED",
            convergence_required=True,
            convergence_satisfied=False,
            convergence_status="CONTINUE_EXPLORATION",
            missing_requirements=["validator:workspace", "REVIEW_GATE_RECORD.json", "HUMAN_DECISION_RECORD.json"],
        )
        self._seed_policy(
            task_id="T-9002",
            pending_hitl_count=3,
            review_status="REVIEW_BLOCKED",
            adversarial_review_status="REVIEW_BLOCKED",
            convergence_required=True,
            convergence_satisfied=False,
            convergence_status="PENDING_DECISION",
            missing_requirements=["WORKFLOW_RUN_RECORD.json", "COMMAND_REQUEST.yaml", "evidence_artifacts>=2"],
        )
        self._seed_policy(
            task_id="T-9003",
            pending_hitl_count=3,
            review_status="REVIEW_CHANGES_REQUESTED",
            convergence_required=True,
            convergence_satisfied=False,
            convergence_status="PENDING_DECISION",
            missing_requirements=["REVIEW_GATE_RECORD.json", "HUMAN_DECISION_RECORD.json", "validator:workspace"],
        )
        self._seed_run("T-9001", "TURN_RUNNING")
        self._seed_run("T-9002", "FAILED")
        self._seed_run("T-9003", "FAILED")
        self._seed_hitl("T-9001", 3)
        self._seed_hitl("T-9002", 3)
        self._seed_hitl("T-9003", 3)
        self.timeline.append_event(task_id="T-9001", event_type="controller_warning", summary="Synthetic warning 1", level="WARNING")
        self.timeline.append_event(task_id="T-9001", event_type="controller_warning", summary="Synthetic warning 2", level="WARNING")
        self.timeline.append_event(task_id="T-9002", event_type="controller_warning", summary="Synthetic warning 3", level="WARNING")
        self.timeline.append_event(task_id="T-9002", event_type="controller_warning", summary="Synthetic warning 4", level="WARNING")
        self.timeline.append_event(task_id="T-9003", event_type="controller_warning", summary="Synthetic warning 5", level="WARNING")
        self.timeline.append_event(task_id="T-9003", event_type="controller_warning", summary="Synthetic warning 6", level="WARNING")

        first = self.observer.evaluate()
        self.assertEqual(first["open_count"], 0)
        payload = self.observer.evaluate()
        categories = {item["category"] for item in payload["advisories"] if item.get("status") != "RESOLVED"}
        self.assertIn("controller_reliability_hardening", categories)
        self.assertIn("hitl_queue_compaction", categories)
        self.assertIn("review_policy_tightening", categories)
        self.assertIn("convergence_policy_tuning", categories)
        self.assertIn("stage_contract_hardening", categories)

    def test_acknowledged_advisory_resolves_when_pressure_clears(self) -> None:
        self._seed_policy(task_id="T-9002", pending_hitl_count=3)
        self._seed_policy(task_id="T-9003", pending_hitl_count=3)
        self._seed_run("T-9002", "TURN_RUNNING")
        self._seed_run("T-9003", "TURN_RUNNING")
        self._seed_hitl("T-9003", 3)
        self._seed_hitl("T-9002", 4)

        self.observer.evaluate()
        initial = self.observer.evaluate()
        open_advisory = next(item for item in initial["advisories"] if item["category"] == "hitl_queue_compaction")
        acknowledged = self.observer.acknowledge(advisory_id=open_advisory["advisory_id"])
        acknowledged_item = next(item for item in acknowledged["advisories"] if item["advisory_id"] == open_advisory["advisory_id"])
        self.assertEqual(acknowledged_item["status"], "ACKNOWLEDGED")

        for entry in self.hitl.list_entries(task_id="T-9002", include_resolved=False, limit=20):
            self.hitl.resolve_entry(entry_id=entry["entry_id"], response_payload={"approved": True})
        self._seed_policy(task_id="T-9002", pending_hitl_count=0)

        resolved = self.observer.evaluate()
        resolved_item = next(item for item in resolved["advisories"] if item["advisory_id"] == open_advisory["advisory_id"])
        self.assertEqual(resolved_item["status"], "RESOLVED")

    def _seed_policy(
        self,
        *,
        task_id: str,
        pending_hitl_count: int,
        review_status: str = "READY",
        adversarial_review_status: str | None = None,
        convergence_required: bool = False,
        convergence_satisfied: bool = True,
        convergence_status: str = "NOT_REQUIRED",
        missing_requirements: list[str] | None = None,
    ) -> None:
        self.workflow_policy._write(  # noqa: SLF001
            task_id=task_id,
            payload={
                "task_id": task_id,
                "current_stage": "DESIGN",
                "lifecycle_status": "READY",
                "pending_hitl_count": pending_hitl_count,
                "review_status": review_status,
                "adversarial_review": {
                    "enabled": bool(adversarial_review_status),
                    "status": adversarial_review_status,
                },
                "convergence": {
                    "required_before_stage_close": convergence_required,
                    "satisfied": convergence_satisfied,
                    "status": convergence_status,
                },
                "stage_contract": {
                    "missing_requirements": list(missing_requirements or []),
                },
                "next_actions": [],
            },
        )

    def _seed_run(self, task_id: str, status: str) -> None:
        run = self.runs.ensure_run(task_id=task_id, run_id=f"{task_id}-run", status="IDLE")
        self.runs.update_status(task_id=task_id, run_id=run["run_id"], status=status)

    def _seed_hitl(self, task_id: str, count: int) -> None:
        for index in range(count):
            self.hitl.create_entry(
                task_id=task_id,
                run_id=f"{task_id}-run",
                source="controller",
                category="pending_hitl",
                summary=f"Synthetic HITL item {index + 1}",
            )


if __name__ == "__main__":
    unittest.main()
