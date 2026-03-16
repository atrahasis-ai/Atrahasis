#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a task workspace and machine-checked start checklist for AAS5.")
    parser.add_argument("task_id", help="Task identifier, e.g. T-302")
    parser.add_argument("--agent-name", help="Optional agent/session name for same-task claim checks.")
    parser.add_argument(
        "--pattern",
        action="append",
        default=[],
        help="Override direct-spec forbidden pattern. Repeatable.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas1.task_hardening import prepare_task

    payload = prepare_task(
        repo_root,
        task_id=args.task_id,
        agent_name=args.agent_name,
        override_patterns=args.pattern,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
