from __future__ import annotations

from pathlib import Path
from typing import Any

from aas5.artifact_registry import ArtifactRegistry


class ArtifactProjectionLayer:
    """Projects runtime state into the canonical task-workspace artifact surface."""

    def __init__(self, registry: ArtifactRegistry) -> None:
        self.registry = registry

    def project_json(
        self,
        *,
        task_id: str,
        relative_path: str,
        payload: dict[str, Any],
        schema_name: str | None = None,
    ) -> Path:
        return self.registry.write_json_artifact(task_id, relative_path, payload, schema_name=schema_name)

    def project_yaml(
        self,
        *,
        task_id: str,
        relative_path: str,
        payload: dict[str, Any],
        schema_name: str | None = None,
    ) -> Path:
        return self.registry.write_yaml_artifact(task_id, relative_path, payload, schema_name=schema_name)

    def project_markdown(self, *, task_id: str, relative_path: str, text: str) -> Path:
        return self.registry.write_markdown_artifact(task_id, relative_path, text)
