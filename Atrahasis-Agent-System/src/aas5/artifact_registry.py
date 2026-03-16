from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from aas5.common import ensure_dir, load_json, write_json, write_text, write_yaml


class ArtifactRegistry:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.docs_root = repo_root / "docs"
        self.schema_root = self.docs_root / "schemas"

    def task_root(self, task_id: str) -> Path:
        return ensure_dir(self.docs_root / "task_workspaces" / task_id)

    def schema(self, schema_name: str) -> dict[str, Any]:
        return load_json(self.schema_root / f"{schema_name}.schema.json")

    def validate(self, schema_name: str, payload: dict[str, Any]) -> None:
        validator = Draft202012Validator(self.schema(schema_name))
        errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
        if errors:
            rendered = "; ".join(
                f"{'.'.join(str(part) for part in err.path) or '<root>'}: {err.message}" for err in errors
            )
            raise ValueError(f"{schema_name} validation failed: {rendered}")

    def write_json_artifact(
        self,
        task_id: str,
        relative_path: str,
        payload: dict[str, Any],
        schema_name: str | None = None,
    ) -> Path:
        if schema_name is not None:
            self.validate(schema_name, payload)
        path = self.task_root(task_id) / relative_path
        write_json(path, payload)
        return path

    def write_yaml_artifact(
        self,
        task_id: str,
        relative_path: str,
        payload: dict[str, Any],
        schema_name: str | None = None,
    ) -> Path:
        if schema_name is not None:
            self.validate(schema_name, payload)
        path = self.task_root(task_id) / relative_path
        write_yaml(path, payload)
        return path

    def write_markdown_artifact(self, task_id: str, relative_path: str, text: str) -> Path:
        path = self.task_root(task_id) / relative_path
        write_text(path, text)
        return path

    def dump_json_template(self, path: Path, payload: dict[str, Any]) -> None:
        ensure_dir(path.parent)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def dump_yaml_template(self, path: Path, payload: dict[str, Any]) -> None:
        ensure_dir(path.parent)
        path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
