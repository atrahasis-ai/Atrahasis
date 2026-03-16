from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, runtime_root_dir, runtime_state_dir, utc_now, write_json
from aas1.knowledge_index import KnowledgeIndex
from aas1.provider_runtime import ProviderRuntimeRegistry


class WorkflowRetirementManager:
    """Archives ad hoc workflow runs out of the active AAS3 runtime."""

    STATE_BUCKETS = (
        "workflows",
        "operator_sessions",
        "programs",
        "discovery_graphs",
        "governance",
        "telemetry",
    )

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.runtime_root = runtime_root_dir(repo_root)
        self.runtime_state_root = runtime_state_dir(repo_root)
        self.repo_archive_root = ensure_dir(repo_root / "archive" / "retired_workflows")
        self.runtime_archive_root = ensure_dir(self.runtime_root / "archive" / "retired_workflows")
        self.knowledge_index = KnowledgeIndex(repo_root)
        self.provider_runtime = ProviderRuntimeRegistry(repo_root)

    def retire_tasks(self, task_ids: list[str], *, reason: str) -> dict[str, Any]:
        retired_at = utc_now()
        summary = {
            "type": "WORKFLOW_RETIREMENT_BATCH",
            "retired_at": retired_at,
            "reason": reason,
            "tasks": [],
        }

        for task_id in task_ids:
            summary["tasks"].append(self._retire_task(task_id=task_id, retired_at=retired_at))

        cleared_sessions = self.provider_runtime.clear_current_task_references(
            task_ids,
            note=f"retired workflow batch at {retired_at}",
        )
        pruned_entries = self.knowledge_index.prune_task_workspaces(task_ids)

        summary["provider_sessions_cleared"] = cleared_sessions
        summary["knowledge_index_entries_pruned"] = len(pruned_entries)

        manifest_path = self.runtime_archive_root / f"retirement-{retired_at.replace(':', '').replace('-', '')}.json"
        write_json(manifest_path, summary)
        summary["manifest_path"] = str(manifest_path)
        return summary

    def _retire_task(self, *, task_id: str, retired_at: str) -> dict[str, Any]:
        task_summary = {
            "task_id": task_id,
            "retired_at": retired_at,
            "workspace_archived": None,
            "state_archives": [],
        }

        workspace_path = self.repo_root / "docs" / "task_workspaces" / task_id
        if workspace_path.exists():
            archive_path = self._archive_move(
                source=workspace_path,
                destination=self.repo_archive_root / "task_workspaces" / task_id,
            )
            task_summary["workspace_archived"] = str(archive_path)

        for bucket in self.STATE_BUCKETS:
            source = self.runtime_state_root / bucket / task_id
            if not source.exists():
                continue
            archive_path = self._archive_move(
                source=source,
                destination=self.runtime_archive_root / "state" / bucket / task_id,
            )
            task_summary["state_archives"].append(
                {
                    "bucket": bucket,
                    "path": str(archive_path),
                }
            )
        return task_summary

    def _archive_move(self, *, source: Path, destination: Path) -> Path:
        ensure_dir(destination.parent)
        final_destination = destination
        suffix = 1
        while final_destination.exists():
            final_destination = destination.with_name(f"{destination.name}-{suffix}")
            suffix += 1
        shutil.move(str(source), str(final_destination))
        return final_destination
