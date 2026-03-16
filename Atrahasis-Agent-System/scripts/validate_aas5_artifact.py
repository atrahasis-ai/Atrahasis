#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def load_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml", ".md"}:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise TypeError(f"{path} must parse to a mapping/object, got {type(data)}")
    return data


def load_schema(repo_root: Path, schema_name: str) -> dict[str, Any]:
    schema_path = repo_root / "docs" / "schemas" / f"{schema_name}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    return json.loads(schema_path.read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 3:
        eprint("Usage: python scripts/validate_aas5_artifact.py <schema-name> <artifact-path>")
        return 2

    schema_name = sys.argv[1]
    artifact_path = Path(sys.argv[2]).resolve()
    if not artifact_path.exists():
        eprint(f"Artifact not found: {artifact_path}")
        return 2

    repo_root = Path(__file__).resolve().parents[1]

    try:
        payload = load_payload(artifact_path)
        schema = load_schema(repo_root, schema_name)
    except Exception as exc:
        eprint(exc)
        return 1

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
    if errors:
        eprint(f"{artifact_path.name} validation FAILED ({len(errors)} error(s))")
        for err in errors:
            path = ".".join(str(part) for part in err.path) or "<root>"
            eprint(f"  - {path}: {err.message}")
        return 1

    print(f"{artifact_path.name} validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
