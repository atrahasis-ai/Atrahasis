from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from aas1.common import load_yaml, utc_now, write_yaml


class TaskClaimCoordinator:
    ACTIVE_STATUSES = {"CLAIMED", "IN_PROGRESS"}

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.claim_root = repo_root / "docs" / "task_claims"

    def claim_task(
        self,
        *,
        task_id: str,
        title: str,
        platform: str,
        agent_name: str,
        safe_zone_paths: list[str],
        pipeline_type: str = "AAS",
        invention_ids: list[str] | None = None,
        target_specs: list[str] | None = None,
        notes: str = "",
        status: str = "CLAIMED",
    ) -> dict[str, Any]:
        existing = self.load_claim(task_id)
        if existing and existing.get("status") != "ABANDONED":
            raise ValueError(
                f"Task {task_id} already has a claim record owned by {existing.get('agent_name', 'unknown')} ({existing.get('platform', 'unknown')}) with status {existing.get('status', 'UNKNOWN')}."
            )
        now = utc_now()
        payload = {
            "task_id": task_id,
            "invention_ids": invention_ids or [],
            "target_specs": target_specs or [],
            "title": title,
            "platform": platform.strip().upper(),
            "agent_name": agent_name,
            "claimed_at": now if not existing else existing.get("claimed_at", now),
            "updated_at": now,
            "status": status,
            "scope": {
                "safe_zone_paths": safe_zone_paths,
                "pipeline_type": pipeline_type,
            },
            "notes": notes,
        }
        write_yaml(self.claim_root / f"{task_id}.yaml", payload)
        return payload

    def update_status(
        self,
        *,
        task_id: str,
        status: str,
        notes: str | None = None,
    ) -> dict[str, Any]:
        payload = self.load_claim(task_id)
        if payload is None:
            raise ValueError(f"Task claim not found: {task_id}")
        payload["status"] = status
        payload["updated_at"] = utc_now()
        if notes is not None:
            payload["notes"] = notes
        write_yaml(self.claim_root / f"{task_id}.yaml", payload)
        return payload

    def load_claim(self, task_id: str) -> dict[str, Any] | None:
        path = self.claim_root / f"{task_id}.yaml"
        if not path.exists():
            return None
        payload = load_yaml(path)
        if payload is None:
            return None
        if isinstance(payload, str):
            return yaml.safe_load(payload)
        return payload
