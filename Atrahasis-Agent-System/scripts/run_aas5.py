#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Atrahasis AAS5 invention pipeline.")
    parser.add_argument("modifier", help="AASBT | AASAQ | AASNI | AASA")
    parser.add_argument(
        "task_id",
        nargs="?",
        help="Task workspace identifier, e.g. T-230. Optional for non-AASBT modifiers.",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Operator prompt for the run. If task_id is omitted, this becomes the first trailing argument.",
    )
    parser.add_argument(
        "--constraint",
        action="append",
        default=[],
        help="Operator constraint to preserve during orchestration. Repeatable.",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Suppress the human-readable operator prompt and emit JSON only.",
    )
    parser.add_argument("--provider", help="Optional backend provider registration: codex | gemini")
    parser.add_argument("--agent-name", help="Agent name for backend registration")
    parser.add_argument("--session-id", help="Session identifier for backend registration")
    parser.add_argument(
        "--agent-type",
        action="append",
        default=[],
        help="Agent type or routing tier for backend registration. Repeatable.",
    )
    parser.add_argument(
        "--task-class",
        default="auto",
        choices=["auto", "canonical", "analysis", "validation", "demo"],
        help="Task-ID band to use when validating or auto-minting task IDs.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas5.invention_pipeline_manager import InventionPipelineManager
    from aas5.task_id_policy import TASK_ID_RE, TaskIdPolicy

    manager = InventionPipelineManager(repo_root)
    raw_task_id = args.task_id
    prompt = args.prompt
    if prompt is None and raw_task_id and not TASK_ID_RE.match(raw_task_id.strip().upper()):
        prompt = raw_task_id
        raw_task_id = None
    if prompt is None:
        parser.error("A prompt is required.")

    task_policy = TaskIdPolicy(repo_root)
    try:
        task_id, task_class, auto_minted = task_policy.resolve(
            modifier=args.modifier,
            requested_task_id=raw_task_id,
            task_class=args.task_class,
        )
    except ValueError as exc:
        parser.error(str(exc))

    if args.provider or args.agent_name or args.session_id:
        if not (args.provider and args.agent_name and args.session_id):
            parser.error("--provider, --agent-name, and --session-id must be supplied together")
        manager.register_backend(
            provider=args.provider,
            agent_name=args.agent_name,
            session_id=args.session_id,
            agent_types=args.agent_type,
            current_task=task_id,
        )
    result = manager.run_command(
        modifier=args.modifier,
        task_id=task_id,
        prompt=prompt,
        operator_constraints=args.constraint,
    )
    result["task_id"] = task_id
    result["task_class"] = task_class
    result["task_id_auto_minted"] = auto_minted
    if result.get("status") == "PENDING_HUMAN_REVIEW" and not args.json_only:
        prompt = manager.render_operator_prompt(task_id=task_id)
        if sys.stdout.isatty() and sys.stdin.isatty():
            print(prompt)
            return 0
        result["human_review_prompt"] = prompt
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
