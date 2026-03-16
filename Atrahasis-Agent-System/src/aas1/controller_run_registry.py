from __future__ import annotations

from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


TERMINAL_STATUSES = {
    "REVIEW_APPROVED",
    "REVIEW_BLOCKED",
    "REVIEW_CHANGES_REQUESTED",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
}


class ControllerRunRegistry:
    """Persists controller-owned App Server run bindings per task."""

    def __init__(self, repo_root: Path) -> None:
        self.root = ensure_dir(runtime_state_dir(repo_root) / "controller_runs")
        self.index_path = self.root / "index.json"

    def ensure_run(
        self,
        *,
        task_id: str,
        workflow_id: str | None = None,
        run_id: str | None = None,
        status: str = "IDLE",
        app_server_url: str | None = None,
    ) -> dict[str, Any]:
        if run_id:
            path = self._run_path(task_id, run_id)
            if path.exists():
                return load_json(path)
        latest = self.load_latest(task_id)
        if latest and not run_id:
            if workflow_id is None or latest.get("workflow_id") == workflow_id:
                return latest
        resolved_run_id = run_id or workflow_id or f"{task_id}-controller-{utc_now().replace(':', '').replace('-', '')}"
        payload = {
            "type": "CONTROLLER_RUN",
            "task_id": task_id,
            "run_id": resolved_run_id,
            "workflow_id": workflow_id,
            "thread_id": None,
            "turn_id": None,
            "review_thread_id": None,
            "review_turn_id": None,
            "status": status,
            "app_server_url": app_server_url,
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "artifacts": {},
            "hitl_entry_ids": [],
            "event_log": [],
            "metadata": {},
        }
        self._write(payload)
        return payload

    def load(self, *, task_id: str, run_id: str) -> dict[str, Any]:
        return load_json(self._run_path(task_id, run_id))

    def load_latest(self, task_id: str) -> dict[str, Any] | None:
        path = self.root / task_id / "latest.json"
        if not path.exists():
            return None
        return load_json(path)

    def list_runs(self, *, task_id: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        if task_id:
            paths = sorted((self.root / task_id).glob("*.json"), reverse=True)
        else:
            paths = sorted(self.root.glob("*/*.json"), reverse=True)
        results: list[dict[str, Any]] = []
        for path in paths:
            if path.name == "latest.json":
                continue
            results.append(load_json(path))
            if len(results) >= limit:
                break
        return results

    def bind_thread(
        self,
        *,
        task_id: str,
        run_id: str,
        thread_id: str,
        status: str = "THREAD_READY",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = self.load(task_id=task_id, run_id=run_id)
        payload["thread_id"] = thread_id
        payload["status"] = status
        payload["updated_at"] = utc_now()
        if metadata:
            payload.setdefault("metadata", {})["thread"] = metadata
        self._write(payload)
        index = self._load_index()
        index.setdefault("threads", {})[thread_id] = {"task_id": task_id, "run_id": run_id}
        self._write_index(index)
        return payload

    def bind_turn(
        self,
        *,
        task_id: str,
        run_id: str,
        turn_id: str | None,
        status: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = self.load(task_id=task_id, run_id=run_id)
        payload["turn_id"] = turn_id
        payload["status"] = status
        payload["updated_at"] = utc_now()
        if metadata:
            payload.setdefault("metadata", {})["turn"] = metadata
        self._write(payload)
        return payload

    def bind_review(
        self,
        *,
        task_id: str,
        run_id: str,
        review_thread_id: str | None,
        review_turn_id: str | None = None,
        status: str = "REVIEW_PENDING",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = self.load(task_id=task_id, run_id=run_id)
        payload["review_thread_id"] = review_thread_id
        payload["review_turn_id"] = review_turn_id
        payload["status"] = status
        payload["updated_at"] = utc_now()
        if metadata:
            payload.setdefault("metadata", {})["review"] = metadata
        self._write(payload)
        if review_thread_id:
            index = self._load_index()
            index.setdefault("review_threads", {})[review_thread_id] = {"task_id": task_id, "run_id": run_id}
            self._write_index(index)
        return payload

    def update_status(
        self,
        *,
        task_id: str,
        run_id: str,
        status: str,
        artifact_updates: dict[str, str | None] | None = None,
        metadata_updates: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = self.load(task_id=task_id, run_id=run_id)
        payload["status"] = status
        payload["updated_at"] = utc_now()
        if artifact_updates:
            artifacts = dict(payload.get("artifacts", {}))
            artifacts.update({key: value for key, value in artifact_updates.items() if value})
            payload["artifacts"] = artifacts
        if metadata_updates:
            metadata = dict(payload.get("metadata", {}))
            metadata.update(metadata_updates)
            payload["metadata"] = metadata
        self._write(payload)
        return payload

    def append_event(
        self,
        *,
        task_id: str,
        run_id: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        record = self.load(task_id=task_id, run_id=run_id)
        record.setdefault("event_log", []).append(
            {
                "timestamp": utc_now(),
                "event_type": event_type,
                "payload": payload or {},
            }
        )
        record["event_log"] = record["event_log"][-120:]
        record["updated_at"] = utc_now()
        self._write(record)
        return record

    def note_hitl_entry(self, *, task_id: str, run_id: str, entry_id: str) -> dict[str, Any]:
        payload = self.load(task_id=task_id, run_id=run_id)
        existing = [item for item in payload.get("hitl_entry_ids", []) if item != entry_id]
        existing.append(entry_id)
        payload["hitl_entry_ids"] = existing[-120:]
        payload["updated_at"] = utc_now()
        self._write(payload)
        return payload

    def resolve_task_for_thread(self, thread_id: str) -> dict[str, str] | None:
        index = self._load_index()
        return index.get("threads", {}).get(thread_id)

    def resolve_task_for_review_thread(self, review_thread_id: str) -> dict[str, str] | None:
        index = self._load_index()
        return index.get("review_threads", {}).get(review_thread_id)

    def latest_active_task(self) -> str | None:
        index = self._load_index()
        latest_runs = index.get("latest_runs", {})
        for task_id, run_id in reversed(list(latest_runs.items())):
            payload = self.load(task_id=task_id, run_id=run_id)
            if payload.get("status") not in TERMINAL_STATUSES:
                return task_id
        return None

    def _write(self, payload: dict[str, Any]) -> None:
        task_id = payload["task_id"]
        run_id = payload["run_id"]
        task_root = ensure_dir(self.root / task_id)
        write_json(task_root / f"{run_id}.json", payload)
        write_json(task_root / "latest.json", payload)
        index = self._load_index()
        index.setdefault("latest_runs", {})[task_id] = run_id
        self._write_index(index)

    def _run_path(self, task_id: str, run_id: str) -> Path:
        return ensure_dir(self.root / task_id) / f"{run_id}.json"

    def _load_index(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return {"latest_runs": {}, "threads": {}, "review_threads": {}}
        return load_json(self.index_path)

    def _write_index(self, index: dict[str, Any]) -> None:
        write_json(self.index_path, index)
