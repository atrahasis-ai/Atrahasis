#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create or update an AAS task claim.")
    parser.add_argument("task_id", help="Task identifier, e.g. T-910")
    parser.add_argument("title", help="Task title")
    parser.add_argument("platform", help="CODEX | GEMINI | CLAUDE")
    parser.add_argument("agent_name", help="Registered agent name")
    parser.add_argument("--safe-zone", action="append", default=[], help="Safe-zone path. Repeatable.")
    parser.add_argument("--pipeline-type", default="AAS", help="AAS | DIRECT_EDIT | GOVERNANCE")
    parser.add_argument("--invention-id", action="append", default=[], help="Claimed invention ID. Repeatable.")
    parser.add_argument("--target-spec", action="append", default=[], help="Target spec ID. Repeatable.")
    parser.add_argument("--status", default="CLAIMED", help="CLAIMED | IN_PROGRESS | DONE | ABANDONED")
    parser.add_argument("--note", default="", help="Optional claim note.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas5.task_claim_coordinator import TaskClaimCoordinator

    coordinator = TaskClaimCoordinator(repo_root)
    safe_zones = args.safe_zone or [f"docs/task_workspaces/{args.task_id}/"]
    payload = coordinator.claim_task(
        task_id=args.task_id,
        title=args.title,
        platform=args.platform,
        agent_name=args.agent_name,
        safe_zone_paths=safe_zones,
        pipeline_type=args.pipeline_type,
        invention_ids=args.invention_id,
        target_specs=args.target_spec,
        notes=args.note,
        status=args.status,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
