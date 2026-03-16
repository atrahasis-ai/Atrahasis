from __future__ import annotations

from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


class OperatorSessionManager:
    """Durable operator-facing review session state."""

    def __init__(self, repo_root: Path) -> None:
        self.root = ensure_dir(runtime_state_dir(repo_root) / "operator_sessions")

    def persist_pending_session(
        self,
        *,
        task_id: str,
        workflow_id: str,
        human_record: dict[str, Any],
        exploration_record: dict[str, Any],
        rendered_prompt: str,
        artifact_paths: dict[str, str],
    ) -> str:
        payload = {
            "type": "OPERATOR_SESSION",
            "task_id": task_id,
            "workflow_id": workflow_id,
            "status": human_record.get("workflow_status", "PENDING_HUMAN_REVIEW"),
            "updated_at": utc_now(),
            "rendered_prompt": rendered_prompt,
            "decision_options": human_record.get("options", []),
            "operator_actions": human_record.get("operator_actions", []),
            "priority_order": exploration_record.get("priority_order", []),
            "recommended_branch_budget": exploration_record.get("recommended_branch_budget"),
            "artifact_refs": dict(artifact_paths),
        }
        task_root = ensure_dir(self.root / task_id)
        path = task_root / f"{workflow_id}.json"
        write_json(path, payload)
        write_json(task_root / "latest.json", payload)
        return str(path)

    def load_latest_prompt(self, task_id: str) -> str | None:
        path = self.root / task_id / "latest.json"
        if not path.exists():
            return None
        payload = load_json(path)
        return payload.get("rendered_prompt")

    def load_latest_session(self, task_id: str) -> dict[str, Any] | None:
        path = self.root / task_id / "latest.json"
        if not path.exists():
            return None
        return load_json(path)

    def update_latest_session(
        self,
        *,
        task_id: str,
        status: str,
        artifact_refs: dict[str, str | None] | None = None,
        rendered_prompt: str | None = None,
    ) -> dict[str, Any] | None:
        payload = self.load_latest_session(task_id)
        if payload is None:
            return None
        payload["status"] = status
        payload["updated_at"] = utc_now()
        if rendered_prompt is not None:
            payload["rendered_prompt"] = rendered_prompt
        if artifact_refs:
            merged = dict(payload.get("artifact_refs", {}))
            merged.update({key: value for key, value in artifact_refs.items() if value})
            payload["artifact_refs"] = merged
        task_root = ensure_dir(self.root / task_id)
        latest_path = task_root / "latest.json"
        workflow_id = payload.get("workflow_id")
        if workflow_id:
            write_json(task_root / f"{workflow_id}.json", payload)
        write_json(latest_path, payload)
        return payload
