from __future__ import annotations

from pathlib import Path
from typing import Any

from aas5.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


class ProgramStateStore:
    """Durable research-program state snapshots and latest views."""

    def __init__(self, repo_root: Path) -> None:
        self.root = ensure_dir(runtime_state_dir(repo_root) / "programs")

    def load_latest(self, task_id: str) -> dict[str, Any] | None:
        path = self.root / task_id / "latest.json"
        if not path.exists():
            return None
        return load_json(path)

    def persist(
        self,
        *,
        task_id: str,
        workflow_id: str,
        program_report: dict[str, Any],
    ) -> str:
        payload = {
            "type": "PROGRAM_STATE_SNAPSHOT",
            "task_id": task_id,
            "workflow_id": workflow_id,
            "updated_at": utc_now(),
            "active_programs": program_report.get("active_programs", []),
            "master_program_tree": program_report.get("master_program_tree", []),
            "governance_summary": program_report.get("governance_summary", {}),
        }
        task_root = ensure_dir(self.root / task_id)
        path = task_root / f"{workflow_id}.json"
        write_json(path, payload)
        write_json(task_root / "latest.json", payload)
        return str(path)
