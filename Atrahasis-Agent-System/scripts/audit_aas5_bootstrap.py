#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit AAS5 bootstrap runtime readiness without mutating repo state."
    )
    parser.add_argument("--agent-name", help="Optional current session agent name.")
    parser.add_argument("--parent-model", help="Optional actual parent runtime model if exposed.")
    parser.add_argument("--reasoning-effort", help="Optional parent reasoning effort if exposed.")
    parser.add_argument(
        "--child-agent-capable",
        choices=["true", "false"],
        help="Explicitly mark whether the runtime exposes real child-agent capability.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas5.bootstrap_audit import build_bootstrap_runtime_audit

    child_agent_capable = None
    if args.child_agent_capable == "true":
        child_agent_capable = True
    elif args.child_agent_capable == "false":
        child_agent_capable = False

    payload = build_bootstrap_runtime_audit(
        repo_root,
        agent_name=args.agent_name,
        parent_model=args.parent_model,
        reasoning_effort=args.reasoning_effort,
        child_agent_capable=child_agent_capable,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
