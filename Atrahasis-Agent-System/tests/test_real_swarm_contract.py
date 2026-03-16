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

from aas1.stage_contracts import StageContractRegistry
from tests.aas5_fixture_support import AAS5IdeationFixture, copy_aas5_validator_runtime


class RealSwarmContractTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "real_swarm_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_swarm_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        self.task_root = self.repo_root / "docs" / "task_workspaces" / "T-9002"
        self.task_root.mkdir(parents=True, exist_ok=True)
        copy_aas5_validator_runtime(source_repo=REPO_ROOT, destination_repo=self.repo_root)
        self.fixture = AAS5IdeationFixture()

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_full_pipeline_ideation_fails_when_swarm_is_internal_only(self) -> None:
        self.fixture.write_supporting_artifacts(
            self.task_root,
            execution_mode="BLOCKED",
            satisfied=False,
            recommendation_authorized=False,
            multi_agent_enabled=False,
            real_child_sessions_available=False,
            internal_viewpoint_roles=["visionary", "systems_thinker", "critic"],
        )

        report = StageContractRegistry(self.repo_root).evaluate(
            task_id="T-9002",
            task_class="FULL_PIPELINE",
            current_stage="IDEATION",
        )
        self.assertFalse(report["satisfied"])
        self.assertIn("validator:swarm_execution", report["missing_requirements"])

    def test_full_pipeline_ideation_fails_when_child_artifact_refs_are_missing(self) -> None:
        self.fixture.write_supporting_artifacts(self.task_root, include_child_results=False)

        report = StageContractRegistry(self.repo_root).evaluate(
            task_id="T-9002",
            task_class="FULL_PIPELINE",
            current_stage="IDEATION",
        )
        self.assertFalse(report["satisfied"])
        self.assertIn("validator:swarm_execution", report["missing_requirements"])

    def test_full_pipeline_ideation_fails_when_required_branch_ids_are_missing(self) -> None:
        partial = self.fixture.non_parent_node_ids()[:-2]
        self.fixture.write_supporting_artifacts(self.task_root, spawned_node_ids=partial)

        report = StageContractRegistry(self.repo_root).evaluate(
            task_id="T-9002",
            task_class="FULL_PIPELINE",
            current_stage="IDEATION",
        )
        self.assertFalse(report["satisfied"])
        self.assertIn("validator:swarm_execution", report["missing_requirements"])


if __name__ == "__main__":
    unittest.main()
