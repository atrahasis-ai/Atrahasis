#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run schema-constrained Codex execution for machine-consumed AAS5 artifacts."
    )
    parser.add_argument("prompt", nargs="?", help="Inline prompt text. Optional when --prompt-file is supplied.")
    parser.add_argument("--prompt-file", help="Path to a UTF-8 prompt file.")
    parser.add_argument("--schema", required=True, help="Path to the JSON schema for the final output.")
    parser.add_argument("--output", required=True, help="Path to the schema-constrained output artifact.")
    parser.add_argument("--events", help="Optional path for the Codex JSONL event stream.")
    parser.add_argument("--stderr-log", help="Optional path for stderr output.")
    parser.add_argument("--model", help="Optional model override.")
    parser.add_argument(
        "--sandbox",
        default="workspace-write",
        choices=["read-only", "workspace-write", "danger-full-access"],
        help="Codex sandbox mode for the exec run.",
    )
    parser.add_argument("--search", action="store_true", help="Enable live web search for this run.")
    parser.add_argument("--ephemeral", action="store_true", help="Run Codex in ephemeral mode.")
    parser.add_argument(
        "--skip-git-repo-check",
        action="store_true",
        help="Pass through Codex's --skip-git-repo-check flag.",
    )
    parser.add_argument(
        "--runner",
        choices=["codex", "codex-alpha"],
        default="codex",
        help="Executable to use for the run.",
    )
    parser.add_argument(
        "--enable",
        action="append",
        default=[],
        help="Codex feature flag to enable. Repeatable.",
    )
    parser.add_argument(
        "--disable",
        action="append",
        default=[],
        help="Codex feature flag to disable. Repeatable.",
    )
    parser.add_argument(
        "--config",
        action="append",
        default=[],
        help="Codex config override of the form key=value. Repeatable.",
    )
    return parser


def _read_prompt(args: argparse.Namespace) -> str:
    prompt_parts: list[str] = []
    if args.prompt_file:
        prompt_parts.append(Path(args.prompt_file).read_text(encoding="utf-8").strip())
    if args.prompt:
        prompt_parts.append(args.prompt.strip())
    prompt = "\n\n".join(part for part in prompt_parts if part)
    if not prompt:
        raise ValueError("An inline prompt or --prompt-file is required.")
    return prompt


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    prompt = _read_prompt(args)
    schema_path = (repo_root / args.schema).resolve() if not Path(args.schema).is_absolute() else Path(args.schema)
    output_path = (repo_root / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
    events_path = (
        Path(args.events)
        if args.events and Path(args.events).is_absolute()
        else (repo_root / args.events).resolve()
        if args.events
        else output_path.with_suffix(".events.jsonl")
    )
    stderr_path = (
        Path(args.stderr_log)
        if args.stderr_log and Path(args.stderr_log).is_absolute()
        else (repo_root / args.stderr_log).resolve()
        if args.stderr_log
        else output_path.with_suffix(".stderr.log")
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    events_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)

    command = [args.runner]
    for feature in args.enable:
        command.extend(["--enable", feature])
    for feature in args.disable:
        command.extend(["--disable", feature])
    for item in args.config:
        command.extend(["-c", item])
    if args.search:
        command.append("--search")
    command.extend(
        [
            "exec",
            "-C",
            str(repo_root),
            "-s",
            args.sandbox,
            "--color",
            "never",
            "--json",
            "--output-schema",
            str(schema_path),
            "-o",
            str(output_path),
        ]
    )
    if args.model:
        command.extend(["-m", args.model])
    if args.ephemeral:
        command.append("--ephemeral")
    if args.skip_git_repo_check:
        command.append("--skip-git-repo-check")
    command.append(prompt)

    completed = subprocess.run(
        command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    events_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")

    summary = {
        "runner": args.runner,
        "repo_root": str(repo_root),
        "schema": str(schema_path),
        "output": str(output_path),
        "events": str(events_path),
        "stderr_log": str(stderr_path),
        "return_code": completed.returncode,
        "search_enabled": args.search,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return completed.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
