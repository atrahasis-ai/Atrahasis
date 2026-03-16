#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run scope-bound direct-spec verification and persist the report.")
    parser.add_argument("task_id", help="Task identifier, e.g. T-302")
    parser.add_argument(
        "--pattern",
        action="append",
        default=[],
        help="Override forbidden pattern. Repeatable.",
    )
    parser.add_argument(
        "--allow-pattern",
        action="append",
        default=[],
        help="Pattern to suppress known-safe matches. Repeatable.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas5.task_hardening import verify_direct_spec_task

    payload = verify_direct_spec_task(
        repo_root,
        task_id=args.task_id,
        override_patterns=args.pattern,
        allow_patterns=args.allow_pattern,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("clean") else 1


if __name__ == "__main__":
    raise SystemExit(main())
