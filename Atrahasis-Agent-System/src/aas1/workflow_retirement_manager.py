from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from aas1.common import runtime_root_dir, runtime_state_dir, utc_now
from aas1.knowledge_index import KnowledgeIndex
from aas1.provider_runtime import ProviderRuntimeRegistry
from aas1.retired_task_registry import RetiredTaskRegistry
from aas1.task_id_policy import TaskIdPolicy


class WorkflowRetirementManager:
    """Retires workflow runs from active AAS5 state into a compact registry."""

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
        self.knowledge_index = KnowledgeIndex(repo_root)
        self.provider_runtime = ProviderRuntimeRegistry(repo_root)
        self.retired_task_registry = RetiredTaskRegistry(repo_root)

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

        self.retired_task_registry.record_batch(
            retired_at=retired_at,
            reason=reason,
            task_summaries=summary["tasks"],
            provider_sessions_cleared=cleared_sessions,
            knowledge_index_entries_pruned=len(pruned_entries),
        )
        summary["registry_path"] = str(self.retired_task_registry.path)
        return summary

    def _retire_task(self, *, task_id: str, retired_at: str) -> dict[str, Any]:
        task_summary = {
            "task_id": task_id,
            "task_class": self._task_class(task_id),
            "retired_at": retired_at,
            "workspace_removed": False,
            "workspace_path": None,
            "claim_removed": False,
            "claim_path": None,
            "state_removals": [],
        }

        workspace_path = self.repo_root / "docs" / "task_workspaces" / task_id
        if workspace_path.exists():
            self._delete_path(workspace_path)
            task_summary["workspace_removed"] = True
            task_summary["workspace_path"] = str(workspace_path)

        claim_path = self.repo_root / "docs" / "task_claims" / f"{task_id}.yaml"
        if claim_path.exists():
            self._delete_path(claim_path)
            task_summary["claim_removed"] = True
            task_summary["claim_path"] = str(claim_path)

        for bucket in self.STATE_BUCKETS:
            source = self.runtime_state_root / bucket / task_id
            if not source.exists():
                continue
            self._delete_path(source)
            task_summary["state_removals"].append(
                {
                    "bucket": bucket,
                    "path": str(source),
                }
            )
        return task_summary

    def _delete_path(self, path: Path) -> None:
        if path.is_dir():
            shutil.rmtree(path)
            return
        path.unlink(missing_ok=True)

    def _task_class(self, task_id: str) -> str:
        number = int(task_id.split("-", 1)[1])
        for label, band in TaskIdPolicy.BANDS.items():
            if band.contains(number):
                return label
        return "unknown"
