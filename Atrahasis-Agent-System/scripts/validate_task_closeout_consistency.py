#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate that claim, workspace, handoff, and dispatch state agree before DONE.")
    parser.add_argument("task_id", help="Task identifier, e.g. T-302")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas1.task_hardening import validate_closeout_consistency

    payload = validate_closeout_consistency(repo_root, task_id=args.task_id)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
