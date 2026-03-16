#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Retire workflow tasks by removing active workspace/state and recording them in the retired-task registry."
    )
    parser.add_argument("task_ids", nargs="+", help="Task IDs to retire, e.g. T-901 T-903 T-9500")
    parser.add_argument("--reason", default="Operator-requested retirement of workflow tasks.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas1.workflow_retirement_manager import WorkflowRetirementManager

    manager = WorkflowRetirementManager(repo_root)
    payload = manager.retire_tasks(task_ids=args.task_ids, reason=args.reason)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
