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

from aas5.bootstrap_audit import build_bootstrap_runtime_audit


class BootstrapAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "bootstrap_audit_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_bootstrap_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        (self.repo_root / "docs" / "task_claims").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "specifications" / "STRATEGY").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "specifications" / "C14 - AiBC Governance").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "specifications" / "C48 - Cryptographic Transparency Ledger").mkdir(
            parents=True, exist_ok=True
        )
        (self.repo_root / "docs" / "specifications" / "STRATEGY" / "MASTER_REDESIGN_SPEC.md").write_text(
            "# strategy\n", encoding="utf-8"
        )
        (
            self.repo_root
            / "docs"
            / "specifications"
            / "C14 - AiBC Governance"
            / "C14_AiBC_Governance_Master_Tech_Spec.md"
        ).write_text("# c14\n", encoding="utf-8")
        (
            self.repo_root
            / "docs"
            / "specifications"
            / "C48 - Cryptographic Transparency Ledger"
            / "C48_Cryptographic_Transparency_Ledger_Master_Tech_Spec.md"
        ).write_text("# c48\n", encoding="utf-8")
        (
            self.repo_root / "docs" / "task_claims" / "T-100.yaml"
        ).write_text(
            "\n".join(
                [
                    "task_id: T-100",
                    "status: CLAIMED",
                    "agent_name: Utu",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (
            self.repo_root / "docs" / "task_claims" / "T-101.yaml"
        ).write_text(
            "\n".join(
                [
                    "task_id: T-101",
                    "status: DONE",
                    "agent_name: Sin",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_bootstrap_audit_marks_unknown_runtime_as_degraded(self) -> None:
        payload = build_bootstrap_runtime_audit(self.repo_root, agent_name="Utu")
        self.assertEqual(payload["active_claim_count"], 1)
        self.assertEqual(payload["active_claims"][0]["task_id"], "T-100")
        self.assertEqual(payload["required_bootstrap_refs"]["c14"].split("/")[-1], "C14_AiBC_Governance_Master_Tech_Spec.md")
        self.assertEqual(
            payload["parent_model_audit"]["auditability"],
            "degraded_unknown_runtime_model",
        )
        self.assertEqual(
            payload["child_agent_capability"]["status"],
            "unverified_runtime_capability",
        )

    def test_bootstrap_audit_records_explicit_runtime_capability_when_provided(self) -> None:
        payload = build_bootstrap_runtime_audit(
            self.repo_root,
            agent_name="Utu",
            parent_model="gpt-5.4",
            reasoning_effort="xhigh",
            child_agent_capable=True,
        )
        self.assertEqual(payload["parent_model_audit"]["actual_runtime_model"], "gpt-5.4")
        self.assertEqual(payload["parent_model_audit"]["auditability"], "runtime_exposed")
        self.assertEqual(payload["child_agent_capability"]["status"], "verified_available")
        self.assertFalse(payload["bootstrap_readiness"]["auditability_degraded"])


if __name__ == "__main__":
    unittest.main()
