#!/usr/bin/env python3
"""
Validate docs/AGENT_STATE.md (YAML) against docs/schemas/agent_state.schema.json.

Usage:
  python scripts/validate_agent_state.py docs/AGENT_STATE.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def load_schema(repo_root: Path) -> dict:
    schema_path = repo_root / "docs" / "schemas" / "agent_state.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    return json.loads(schema_path.read_text())


def main() -> int:
    if len(sys.argv) != 2:
        eprint("Usage: python scripts/validate_agent_state.py <path-to-AGENT_STATE.md>")
        return 2

    state_path = Path(sys.argv[1]).resolve()
    if not state_path.exists():
        eprint(f"File not found: {state_path}")
        return 2

    repo_root = Path(__file__).resolve().parents[1]

    try:
        data = yaml.safe_load(state_path.read_text())
    except Exception as exc:
        eprint(f"YAML parse error in {state_path}: {exc}")
        return 1

    if not isinstance(data, dict):
        eprint(f"AGENT_STATE must parse to a YAML mapping/object, got: {type(data)}")
        return 1

    schema = load_schema(repo_root)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))

    if errors:
        eprint(f"AGENT_STATE schema validation FAILED ({len(errors)} error(s)):")
        for err in errors:
            path = ".".join([str(p) for p in err.path]) or "<root>"
            eprint(f"  - {path}: {err.message}")
        return 1

    print("AGENT_STATE schema validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
