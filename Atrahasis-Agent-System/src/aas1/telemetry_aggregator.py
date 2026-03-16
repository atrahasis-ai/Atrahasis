from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, runtime_logs_dir, runtime_state_dir, utc_now, write_json


class TelemetryAggregator:
    """Produces queryable workflow health summaries from append-only telemetry."""

    def __init__(self, repo_root: Path) -> None:
        self.logs_dir = ensure_dir(runtime_logs_dir(repo_root))
        self.root = ensure_dir(runtime_state_dir(repo_root) / "telemetry")

    def record_workflow(
        self,
        *,
        task_id: str,
        workflow_id: str,
        status: str,
        stage_records: list[dict[str, Any]],
        artifact_paths: dict[str, str],
    ) -> str:
        system_events = self._recent_events("system.log", task_id=task_id, workflow_id=workflow_id)
        payload = {
            "type": "TELEMETRY_SUMMARY",
            "task_id": task_id,
            "workflow_id": workflow_id,
            "status": status,
            "updated_at": utc_now(),
            "stage_count": len(stage_records),
            "artifact_count": len(artifact_paths),
            "event_counts": self._event_counts(system_events),
            "recent_events": system_events[-12:],
        }
        task_root = ensure_dir(self.root / task_id)
        path = task_root / f"{workflow_id}.json"
        write_json(path, payload)
        write_json(task_root / "latest.json", payload)
        return str(path)

    def _recent_events(
        self,
        filename: str,
        *,
        task_id: str,
        workflow_id: str,
    ) -> list[dict[str, Any]]:
        path = self.logs_dir / filename
        if not path.exists():
            return []
        rows: list[dict[str, Any]] = []
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if payload.get("task_id") == task_id or payload.get("workflow_id") == workflow_id:
                    rows.append(payload)
        return rows

    def _event_counts(self, events: list[dict[str, Any]]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for event in events:
            name = event.get("event", "unknown")
            counts[name] = counts.get(name, 0) + 1
        return counts
