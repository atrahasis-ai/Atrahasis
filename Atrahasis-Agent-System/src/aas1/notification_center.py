from __future__ import annotations

from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


class NotificationCenter:
    """Durable operator notifications derived from controller state."""

    def __init__(self, repo_root: Path) -> None:
        self.index_path = ensure_dir(runtime_state_dir(repo_root) / "notifications") / "latest.json"

    def list_notifications(self, *, open_only: bool = True, limit: int = 100) -> list[dict[str, Any]]:
        payload = self._load()
        items = payload.get("notifications", [])
        if open_only:
            items = [item for item in items if item.get("status") == "OPEN"]
        return items[:limit]

    def acknowledge(self, *, notification_id: str) -> dict[str, Any]:
        payload = self._load()
        for item in payload.get("notifications", []):
            if item.get("notification_id") == notification_id:
                item["status"] = "ACKNOWLEDGED"
                item["acknowledged_at"] = utc_now()
        self._write(payload)
        return payload

    def sync_task_state(
        self,
        *,
        task_id: str,
        workflow_policy: dict[str, Any] | None,
        pending_hitl_count: int,
        run_status: str | None,
    ) -> dict[str, Any]:
        payload = self._load()
        now = utc_now()
        lifecycle_status = str((workflow_policy or {}).get("lifecycle_status") or "")
        review_status = str((workflow_policy or {}).get("review_status") or "")
        desired = []
        if pending_hitl_count:
            desired.append(
                {
                    "task_id": task_id,
                    "category": "pending_hitl",
                    "severity": "high",
                    "summary": f"{task_id} has pending HITL entries.",
                    "action": "resolve_hitl",
                }
            )
        if lifecycle_status == "READY_FOR_CLOSEOUT":
            desired.append(
                {
                    "task_id": task_id,
                    "category": "closeout_ready",
                    "severity": "medium",
                    "summary": f"{task_id} is ready for closeout.",
                    "action": "execute_closeout",
                }
            )
        if review_status in {"REVIEW_BLOCKED", "REVIEW_CHANGES_REQUESTED"}:
            desired.append(
                {
                    "task_id": task_id,
                    "category": "review_attention",
                    "severity": "high",
                    "summary": f"{task_id} review requires attention: {review_status}.",
                    "action": "finalize_review",
                }
            )
        if run_status in {"FAILED", "TEAM_EXECUTION_FAILED", "CLOSEOUT_VALIDATION_FAILED"}:
            desired.append(
                {
                    "task_id": task_id,
                    "category": "run_failure",
                    "severity": "high",
                    "summary": f"{task_id} has a controller or execution failure: {run_status}.",
                    "action": "inspect_run",
                }
            )
        notifications = []
        existing = {(item.get("task_id"), item.get("category")): item for item in payload.get("notifications", [])}
        desired_keys = {(item["task_id"], item["category"]) for item in desired}
        for item in desired:
            current = existing.get((item["task_id"], item["category"]))
            if current:
                current.update(item)
                current["updated_at"] = now
                current["status"] = "OPEN"
                notifications.append(current)
            else:
                notifications.append(
                    {
                        "notification_id": f"note-{task_id.lower()}-{item['category']}",
                        "created_at": now,
                        "updated_at": now,
                        "status": "OPEN",
                        **item,
                    }
                )
        for key, item in existing.items():
            if key in desired_keys:
                continue
            if item.get("status") == "OPEN":
                item["status"] = "RESOLVED"
                item["updated_at"] = now
            notifications.append(item)
        notifications.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        self._write({"updated_at": now, "notifications": notifications[:500]})
        return self._load()

    def _load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return {"updated_at": utc_now(), "notifications": []}
        return load_json(self.index_path)

    def _write(self, payload: dict[str, Any]) -> None:
        write_json(self.index_path, payload)
