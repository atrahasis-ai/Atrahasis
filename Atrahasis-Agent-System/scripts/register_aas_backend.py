#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Register a Codex or Gemini backend session for AAS3.")
    parser.add_argument("provider", help="codex | gemini")
    parser.add_argument("agent_name", help="Registered Mesopotamian agent name")
    parser.add_argument("session_id", help="Conversation/session identifier")
    parser.add_argument("--agent-type", action="append", default=[], help="Agent type or tier. Repeatable.")
    parser.add_argument("--task-id", help="Current task assignment, if any.")
    parser.add_argument("--status", default="ACTIVE", help="Session status. Default: ACTIVE")
    parser.add_argument("--note", default="", help="Optional session note.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas1.provider_runtime import ProviderRuntimeRegistry

    registry = ProviderRuntimeRegistry(repo_root)
    payload = registry.register_backend(
        provider=args.provider,
        agent_name=args.agent_name,
        session_id=args.session_id,
        agent_types=args.agent_type,
        current_task=args.task_id,
        status=args.status,
        notes=args.note,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
