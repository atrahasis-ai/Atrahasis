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

from aas5.common import write_json, write_text
from aas5.provider_runtime import ProviderRuntimeRegistry
from aas5.task_id_policy import TaskIdPolicy
from aas5.workflow_retirement_manager import WorkflowRetirementManager


class WorkflowRetirementManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "workflow_retirement_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_workflow_retirement_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        (self.repo_root / "docs" / "task_workspaces").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "task_claims").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "runtime" / "state").mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_retire_tasks_deletes_active_state_and_records_registry_entry(self) -> None:
        workspace = self.repo_root / "docs" / "task_workspaces" / "T-9000"
        write_text(workspace / "README.md", "# test workspace")
        claim = self.repo_root / "docs" / "task_claims" / "T-9000.yaml"
        write_text(claim, "task_id: T-9000")

        workflow_state = self.repo_root / "runtime" / "state" / "workflows" / "T-9000"
        write_json(workflow_state / "latest.json", {"task_id": "T-9000"})
        governance_state = self.repo_root / "runtime" / "state" / "governance" / "T-9000"
        write_json(governance_state / "latest.json", {"task_id": "T-9000"})

        provider_runtime = ProviderRuntimeRegistry(self.repo_root)
        provider_runtime.register_backend(
            provider="codex",
            agent_name="Nergal",
            session_id="codex-live-001",
            current_task="T-9000",
        )

        manager = WorkflowRetirementManager(self.repo_root)
        summary = manager.retire_tasks(["T-9000"], reason="test retirement")

        self.assertFalse(workspace.exists())
        self.assertFalse(claim.exists())
        self.assertFalse(workflow_state.exists())
        self.assertFalse(governance_state.exists())
        self.assertTrue((self.repo_root / "runtime" / "state" / "registries" / "retired_task_registry.json").exists())
        self.assertEqual(summary["tasks"][0]["task_id"], "T-9000")
        self.assertTrue(summary["tasks"][0]["workspace_removed"])
        self.assertTrue(summary["tasks"][0]["claim_removed"])
        self.assertEqual(
            {item["bucket"] for item in summary["tasks"][0]["state_removals"]},
            {"workflows", "governance"},
        )
        self.assertEqual(summary["provider_sessions_cleared"][0]["session_id"], "codex-live-001")

        payload = json.loads((self.repo_root / "runtime" / "state" / "registries" / "retired_task_registry.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["retired_tasks"][0]["task_id"], "T-9000")
        self.assertEqual(payload["retired_tasks"][0]["task_class"], "analysis")
        self.assertTrue(payload["retired_tasks"][0]["workspace_removed"])
        self.assertEqual(payload["retired_tasks"][0]["state_buckets_removed"], ["workflows", "governance"])
        self.assertFalse((self.repo_root / "archive" / "retired_workflows").exists())
        self.assertFalse((self.repo_root / "runtime" / "archive" / "retired_workflows").exists())

    def test_task_id_policy_skips_and_rejects_retired_ids_from_registry(self) -> None:
        registry_path = self.repo_root / "runtime" / "state" / "registries" / "retired_task_registry.json"
        write_json(
            registry_path,
            {
                "type": "RETIRED_TASK_REGISTRY",
                "updated_at": "2026-03-16T00:00:00Z",
                "batches": [],
                "retired_tasks": [
                    {
                        "task_id": "T-9000",
                        "task_class": "analysis",
                        "retired_at": "2026-03-16T00:00:00Z",
                        "reason": "test",
                        "source": "unit_test",
                        "workspace_removed": True,
                        "workspace_path": str(self.repo_root / "docs" / "task_workspaces" / "T-9000"),
                        "claim_removed": False,
                        "claim_path": None,
                        "state_buckets_removed": [],
                    }
                ],
            },
        )

        policy = TaskIdPolicy(self.repo_root)
        task_id, task_class, auto_minted = policy.resolve(modifier="AASA", requested_task_id=None)
        self.assertEqual(task_id, "T-9001")
        self.assertEqual(task_class, "analysis")
        self.assertTrue(auto_minted)

        with self.assertRaisesRegex(ValueError, "retired and cannot be reused"):
            policy.resolve(modifier="AASA", requested_task_id="T-9000")


if __name__ == "__main__":
    unittest.main()
