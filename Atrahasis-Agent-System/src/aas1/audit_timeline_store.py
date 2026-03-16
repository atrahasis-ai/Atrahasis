from __future__ import annotations

from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


class AuditTimelineStore:
    """Durable per-task audit timeline for orchestration events."""

    def __init__(self, repo_root: Path) -> None:
        self.root = ensure_dir(runtime_state_dir(repo_root) / "audit_timelines")

    def append_event(
        self,
        *,
        task_id: str,
        event_type: str,
        summary: str,
        payload: dict[str, Any] | None = None,
        source: str = "system",
        level: str = "INFO",
    ) -> dict[str, Any]:
        state = self.load(task_id) or self._new_state(task_id)
        event_id = int(state.get("counter", 0)) + 1
        event = {
            "event_id": event_id,
            "timestamp": utc_now(),
            "event_type": event_type,
            "summary": summary,
            "source": source,
            "level": level,
            "payload": payload or {},
        }
        state["counter"] = event_id
        state["updated_at"] = event["timestamp"]
        state.setdefault("events", []).append(event)
        state["events"] = state["events"][-1000:]
        self._write(task_id=task_id, payload=state)
        return event

    def list_events(
        self,
        *,
        task_id: str,
        after_id: int = 0,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        state = self.load(task_id)
        if not state:
            return []
        events = [item for item in state.get("events", []) if int(item.get("event_id", 0)) > after_id]
        if limit <= 0:
            return events
        return events[-limit:]

    def load(self, task_id: str) -> dict[str, Any] | None:
        path = self.root / task_id / "latest.json"
        if not path.exists():
            return None
        return load_json(path)

    def _new_state(self, task_id: str) -> dict[str, Any]:
        return {
            "type": "AUDIT_TIMELINE",
            "task_id": task_id,
            "counter": 0,
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "events": [],
        }

    def _write(self, *, task_id: str, payload: dict[str, Any]) -> None:
        task_root = ensure_dir(self.root / task_id)
        write_json(task_root / "latest.json", payload)
