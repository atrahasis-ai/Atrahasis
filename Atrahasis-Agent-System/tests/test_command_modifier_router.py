from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from aas5.command_modifier_router import CommandModifierRouter


class CommandModifierRouterTests(unittest.TestCase):
    def test_full_pipeline_task_prompt_modifier_adds_strict_constraints(self) -> None:
        router = CommandModifierRouter()
        request = router.parse(
            modifier="AASNI",
            prompt="Full Pipeline Task:\nEvaluate whether this idea should become a subsystem.",
            task_id="T-9000",
            operator_constraints=["do not edit shared state yet"],
        )
        self.assertEqual(request.command_modifier, "AASNI")
        self.assertEqual(request.prompt, "Evaluate whether this idea should become a subsystem.")
        self.assertIn("do not edit shared state yet", request.operator_constraints)
        self.assertIn("STRICT_FULL_PIPELINE_TASK", request.operator_constraints)
        self.assertIn("ABGR_SWARM_REQUIRED", request.operator_constraints)
        self.assertIn("NO_PARENT_ONLY_ADVISORY_FALLBACK", request.operator_constraints)
        self.assertIn("TASK_ROUTING_REQUIRED", request.operator_constraints)


if __name__ == "__main__":
    unittest.main()
