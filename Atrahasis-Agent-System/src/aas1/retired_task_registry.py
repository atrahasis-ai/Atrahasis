from __future__ import annotations

from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


class RetiredTaskRegistry:
    """Compact registry of retired task IDs and retirement batches."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.path = ensure_dir(runtime_state_dir(repo_root) / "registries") / "retired_task_registry.json"

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return self._default_payload()
        payload = load_json(self.path)
        payload.setdefault("type", "RETIRED_TASK_REGISTRY")
        payload.setdefault("updated_at", "")
        payload.setdefault("batches", [])
        payload.setdefault("retired_tasks", [])
        return payload

    def contains(self, task_id: str) -> bool:
        return any(entry.get("task_id") == task_id for entry in self.load()["retired_tasks"])

    def record_batch(
        self,
        *,
        retired_at: str,
        reason: str,
        task_summaries: list[dict[str, Any]],
        provider_sessions_cleared: list[dict[str, str]],
        knowledge_index_entries_pruned: int,
        source: str = "workflow_retirement_manager",
    ) -> dict[str, Any]:
        payload = self.load()
        task_index = {
            entry["task_id"]: entry
            for entry in payload["retired_tasks"]
            if isinstance(entry, dict) and entry.get("task_id")
        }

        batch_task_ids: list[str] = []
        for summary in task_summaries:
            task_id = summary["task_id"]
            batch_task_ids.append(task_id)
            task_index[task_id] = {
                "task_id": task_id,
                "task_class": summary["task_class"],
                "retired_at": retired_at,
                "reason": reason,
                "source": source,
                "workspace_removed": summary["workspace_removed"],
                "workspace_path": summary["workspace_path"],
                "claim_removed": summary["claim_removed"],
                "claim_path": summary["claim_path"],
                "state_buckets_removed": [item["bucket"] for item in summary["state_removals"]],
            }

        payload["retired_tasks"] = sorted(task_index.values(), key=self._sort_key)
        payload["batches"].append(
            {
                "retired_at": retired_at,
                "reason": reason,
                "source": source,
                "task_ids": batch_task_ids,
                "provider_sessions_cleared": provider_sessions_cleared,
                "knowledge_index_entries_pruned": knowledge_index_entries_pruned,
            }
        )
        payload["updated_at"] = utc_now()
        write_json(self.path, payload)
        return payload

    def _default_payload(self) -> dict[str, Any]:
        return {
            "type": "RETIRED_TASK_REGISTRY",
            "updated_at": "",
            "batches": [],
            "retired_tasks": [],
        }

    def _sort_key(self, entry: dict[str, Any]) -> tuple[int, str]:
        token = str(entry.get("task_id", ""))
        if token.startswith("T-"):
            try:
                return (int(token.split("-", 1)[1]), token)
            except ValueError:
                pass
        return (10**9, token)
