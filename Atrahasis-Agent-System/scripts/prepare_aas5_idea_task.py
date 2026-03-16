#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare a noncanonical exploratory AASNI ideation workspace with real-swarm artifact scaffolding."
    )
    parser.add_argument("--title", required=True, help="Idea title or candidate subsystem name.")
    parser.add_argument("--prompt", help="Full operator prompt for the exploratory idea task.")
    parser.add_argument("--prompt-file", help="Path to a text file containing the full operator prompt.")
    parser.add_argument("--task-id", help="Optional existing or requested analysis-band task id, e.g. T-9005.")
    parser.add_argument("--agent-name", help="Optional current agent/session name.")
    parser.add_argument(
        "--authority-surface",
        action="append",
        default=[],
        help="Named authority surface that must appear in the ideation coverage matrix. Repeatable.",
    )
    parser.add_argument(
        "--constraint",
        action="append",
        default=[],
        help="Optional operator constraint to persist in the command request and decision record. Repeatable.",
    )
    return parser


def _load_prompt(args: argparse.Namespace) -> str:
    if args.prompt and args.prompt_file:
        raise ValueError("Use either --prompt or --prompt-file, not both.")
    if args.prompt:
        return str(args.prompt).strip()
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8").strip()
    raise ValueError("One of --prompt or --prompt-file is required.")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        prompt = _load_prompt(args)
    except Exception as exc:
        parser.error(str(exc))

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas5.task_hardening import prepare_idea_task

    payload = prepare_idea_task(
        repo_root,
        title=args.title,
        prompt=prompt,
        agent_name=args.agent_name,
        authority_surfaces=args.authority_surface,
        requested_task_id=args.task_id,
        operator_constraints=args.constraint,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
