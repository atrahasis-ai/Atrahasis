#!/usr/bin/env python3
"""
Validate an invention concept JSON/YAML file against docs/schemas/invention_concept.schema.json.

Usage:
  python scripts/validate_invention_concept.py <path-to-concept-file>
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
    schema_path = repo_root / "docs" / "schemas" / "invention_concept.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    return json.loads(schema_path.read_text())


def main() -> int:
    if len(sys.argv) != 2:
        eprint("Usage: python scripts/validate_invention_concept.py <path-to-concept-file>")
        return 2

    concept_path = Path(sys.argv[1]).resolve()
    if not concept_path.exists():
        eprint(f"File not found: {concept_path}")
        return 2

    repo_root = Path(__file__).resolve().parents[1]

    text = concept_path.read_text()
    try:
        if concept_path.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(text)
        else:
            data = json.loads(text)
    except Exception as exc:
        eprint(f"Parse error in {concept_path}: {exc}")
        return 1

    if not isinstance(data, dict):
        eprint(f"Concept file must parse to a mapping/object, got: {type(data)}")
        return 1

    schema = load_schema(repo_root)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))

    if errors:
        eprint(f"Invention concept validation FAILED ({len(errors)} error(s)):")
        for err in errors:
            path = ".".join([str(p) for p in err.path]) or "<root>"
            eprint(f"  - {path}: {err.message}")
        return 1

    print("Invention concept validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
