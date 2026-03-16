from __future__ import annotations

from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


METHOD_TO_CATEGORY = {
    "item/commandExecution/requestApproval": "command_approval",
    "item/fileChange/requestApproval": "file_change_approval",
    "item/permissions/requestApproval": "permissions_approval",
    "item/tool/requestUserInput": "request_user_input",
}


class HitlQueueStore:
    """Durable controller-owned HITL queue."""

    def __init__(self, repo_root: Path) -> None:
        self.root = ensure_dir(runtime_state_dir(repo_root) / "hitl_queue")
        self.entries_root = ensure_dir(self.root / "entries")
        self.index_path = self.root / "index.json"

    def create_entry(
        self,
        *,
        task_id: str | None,
        run_id: str | None,
        source: str,
        category: str,
        summary: str,
        request_id: str | int | None = None,
        method: str | None = None,
        thread_id: str | None = None,
        review_thread_id: str | None = None,
        request_payload: dict[str, Any] | None = None,
        artifact_refs: dict[str, str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        entry_id = self._next_entry_id()
        payload = {
            "type": "HITL_QUEUE_ENTRY",
            "entry_id": entry_id,
            "task_id": task_id,
            "run_id": run_id,
            "source": source,
            "category": category,
            "summary": summary,
            "request_id": str(request_id) if request_id is not None else None,
            "method": method,
            "thread_id": thread_id,
            "review_thread_id": review_thread_id,
            "status": "PENDING",
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "resolved_at": None,
            "request_payload": request_payload or {},
            "response_payload": None,
            "artifact_refs": artifact_refs or {},
            "metadata": metadata or {},
        }
        self._write(payload)
        return payload

    def record_app_server_request(
        self,
        *,
        request_id: str | int,
        method: str,
        params: dict[str, Any],
        task_id: str | None,
        run_id: str | None,
        thread_id: str | None = None,
        review_thread_id: str | None = None,
    ) -> dict[str, Any]:
        existing = self.find_by_request_id(request_id)
        if existing and existing.get("status") == "PENDING":
            return existing
        return self.create_entry(
            task_id=task_id,
            run_id=run_id,
            source="app_server",
            category=METHOD_TO_CATEGORY.get(method, "server_request"),
            summary=f"{method} requires operator action",
            request_id=request_id,
            method=method,
            thread_id=thread_id,
            review_thread_id=review_thread_id,
            request_payload=params,
        )

    def list_entries(
        self,
        *,
        task_id: str | None = None,
        include_resolved: bool = False,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        paths = sorted(self.entries_root.glob("*.json"), reverse=True)
        results: list[dict[str, Any]] = []
        for path in paths:
            payload = load_json(path)
            if task_id and payload.get("task_id") != task_id:
                continue
            if not include_resolved and payload.get("status") != "PENDING":
                continue
            results.append(payload)
            if len(results) >= limit:
                break
        return results

    def load_entry(self, entry_id: str) -> dict[str, Any]:
        return load_json(self.entries_root / f"{entry_id}.json")

    def resolve_entry(
        self,
        *,
        entry_id: str,
        response_payload: dict[str, Any],
        status: str = "RESOLVED",
    ) -> dict[str, Any]:
        payload = self.load_entry(entry_id)
        payload["status"] = status
        payload["response_payload"] = response_payload
        payload["resolved_at"] = utc_now()
        payload["updated_at"] = utc_now()
        self._write(payload)
        return payload

    def update_entry(
        self,
        *,
        entry_id: str,
        status: str | None = None,
        summary: str | None = None,
        artifact_refs: dict[str, str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = self.load_entry(entry_id)
        if status:
            payload["status"] = status
        if summary:
            payload["summary"] = summary
        if artifact_refs:
            refs = dict(payload.get("artifact_refs", {}))
            refs.update(artifact_refs)
            payload["artifact_refs"] = refs
        if metadata:
            current = dict(payload.get("metadata", {}))
            current.update(metadata)
            payload["metadata"] = current
        payload["updated_at"] = utc_now()
        self._write(payload)
        return payload

    def find_by_request_id(self, request_id: str | int) -> dict[str, Any] | None:
        index = self._load_index()
        entry_id = index.get("by_request_id", {}).get(str(request_id))
        if not entry_id:
            return None
        path = self.entries_root / f"{entry_id}.json"
        if not path.exists():
            return None
        return load_json(path)

    def _next_entry_id(self) -> str:
        index = self._load_index()
        counter = int(index.get("counter", 0)) + 1
        index["counter"] = counter
        self._write_index(index)
        return f"HITL-{counter:05d}"

    def _write(self, payload: dict[str, Any]) -> None:
        write_json(self.entries_root / f"{payload['entry_id']}.json", payload)
        index = self._load_index()
        entries = index.setdefault("entries", {})
        entries[payload["entry_id"]] = {
            "task_id": payload.get("task_id"),
            "run_id": payload.get("run_id"),
            "status": payload.get("status"),
        }
        task_entries = index.setdefault("by_task", {})
        task_key = payload.get("task_id") or "__unbound__"
        existing = [item for item in task_entries.get(task_key, []) if item != payload["entry_id"]]
        existing.append(payload["entry_id"])
        task_entries[task_key] = existing[-200:]
        if payload.get("request_id"):
            index.setdefault("by_request_id", {})[str(payload["request_id"])] = payload["entry_id"]
        self._write_index(index)

    def _load_index(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return {"counter": 0, "entries": {}, "by_task": {}, "by_request_id": {}}
        return load_json(self.index_path)

    def _write_index(self, index: dict[str, Any]) -> None:
        write_json(self.index_path, index)
