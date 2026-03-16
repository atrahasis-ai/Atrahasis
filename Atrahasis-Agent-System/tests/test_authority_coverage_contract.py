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

from aas5.stage_contracts import StageContractRegistry
from tests.aas5_fixture_support import AAS5IdeationFixture, copy_aas5_validator_runtime


class AuthorityCoverageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "authority_coverage_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_authority_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        self.task_root = self.repo_root / "docs" / "task_workspaces" / "T-9002"
        self.task_root.mkdir(parents=True, exist_ok=True)
        copy_aas5_validator_runtime(source_repo=REPO_ROOT, destination_repo=self.repo_root)
        self.fixture = AAS5IdeationFixture()

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_full_pipeline_ideation_requires_authority_coverage_matrix(self) -> None:
        self.fixture.write_supporting_artifacts(self.task_root, include_authority_matrix=False)

        registry = StageContractRegistry(self.repo_root)
        blocked = registry.evaluate(task_id="T-9002", task_class="FULL_PIPELINE", current_stage="IDEATION")
        self.assertFalse(blocked["satisfied"])
        self.assertIn("AUTHORITY_COVERAGE_MATRIX.json", blocked["missing_requirements"])

        self.fixture.write_json(
            self.task_root / "AUTHORITY_COVERAGE_MATRIX.json",
            self.fixture.authority_coverage_matrix_payload(),
        )
        satisfied = registry.evaluate(task_id="T-9002", task_class="FULL_PIPELINE", current_stage="IDEATION")
        self.assertTrue(satisfied["satisfied"])


if __name__ == "__main__":
    unittest.main()
