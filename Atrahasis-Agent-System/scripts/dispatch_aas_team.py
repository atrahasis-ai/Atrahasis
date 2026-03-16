#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan or execute an explicit Codex child-session team for an AAS task.")
    parser.add_argument("task_id", help="Task workspace identifier, e.g. T-9002")
    parser.add_argument(
        "--spawn-id",
        required=True,
        help="Approved spawn candidate id, e.g. spawn:model",
    )
    parser.add_argument(
        "--action-label",
        default="spawn_program",
        help="Operator action label. Default: spawn_program",
    )
    parser.add_argument(
        "--provider",
        default="codex",
        help="Backend provider to use for dispatch. Default: codex",
    )
    parser.add_argument("--agent-name", help="Optional parent agent name override.")
    parser.add_argument("--session-id", help="Optional parent session id override.")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Launch real child Codex sessions after writing the team plan.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build and print the plan/dispatch record without writing artifacts or running Codex.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas5.invention_pipeline_manager import InventionPipelineManager

    manager = InventionPipelineManager(repo_root)
    payload = manager.prepare_team_dispatch(
        task_id=args.task_id,
        action_label=args.action_label,
        instruction=args.spawn_id,
        provider=args.provider,
        agent_name=args.agent_name,
        session_id=args.session_id,
        execute=args.execute,
        dry_run=args.dry_run,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    if args.execute and payload.get("status") in {"TEAM_EXECUTION_FAILED", "TEAM_EXECUTION_PARTIAL_FAILURE"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
