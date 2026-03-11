#!/usr/bin/env python3
"""
Validate docs/contribution_requests/*.yaml against docs/schemas/contribution_request.schema.json.

Usage:
  python scripts/validate_contribution_requests.py docs/contribution_requests
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def load_schema(repo_root: Path) -> dict:
    schema_path = repo_root / "docs" / "schemas" / "contribution_request.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    return json.loads(schema_path.read_text())


def iter_yaml_files(dir_path: Path):
    for p in sorted(dir_path.glob("*.y*ml")):
        if p.is_file():
            yield p


def main() -> int:
    if len(sys.argv) != 2:
        eprint("Usage: python scripts/validate_contribution_requests.py <contribution_requests_dir>")
        return 2

    dir_path = Path(sys.argv[1]).resolve()
    if not dir_path.exists() or not dir_path.is_dir():
        eprint(f"Directory not found: {dir_path}")
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    schema = load_schema(repo_root)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    yaml_files = list(iter_yaml_files(dir_path))
    if not yaml_files:
        print("No contribution request YAML files found (OK).")
        return 0

    all_request_ids: set[str] = set()
    failed = False

    for path in yaml_files:
        try:
            data: Any = yaml.safe_load(path.read_text())
        except Exception as exc:
            eprint(f"[FAIL] YAML parse error in {path.name}: {exc}")
            failed = True
            continue

        if not isinstance(data, dict):
            eprint(f"[FAIL] {path.name} must parse to a YAML mapping/object.")
            failed = True
            continue

        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            eprint(f"[FAIL] {path.name}: schema validation failed ({len(errors)} error(s))")
            for err in errors:
                p = ".".join([str(x) for x in err.path]) or "<root>"
                eprint(f"  - {p}: {err.message}")
            failed = True
            continue

        # Additional lightweight sanity checks:
        filename_invention_id = path.stem
        if data.get("invention_id") != filename_invention_id:
            eprint(f"[FAIL] {path.name}: invention_id '{data.get('invention_id')}' must match filename '{filename_invention_id}'")
            failed = True

        reqs = data.get("requests", [])
        local_ids: set[str] = set()
        for r in reqs:
            rid = r.get("id")
            if rid in local_ids:
                eprint(f"[FAIL] {path.name}: duplicate request id in file: {rid}")
                failed = True
            local_ids.add(rid)
            if rid in all_request_ids:
                eprint(f"[FAIL] {path.name}: duplicate request id across files: {rid}")
                failed = True
            all_request_ids.add(rid)

        if not failed:
            print(f"[OK] {path.name}")

    if failed:
        return 1

    print("All contribution requests validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
