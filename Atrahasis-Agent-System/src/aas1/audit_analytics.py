from __future__ import annotations

from pathlib import Path
from typing import Any

from aas1.audit_timeline_store import AuditTimelineStore
from aas1.controller_run_registry import ControllerRunRegistry, TERMINAL_STATUSES
from aas1.hitl_queue_store import HitlQueueStore
from aas1.workflow_policy_engine import WorkflowPolicyEngine


class AuditAnalytics:
    """Aggregates repo-wide controller activity into operator-facing analytics."""

    def __init__(self, repo_root: Path) -> None:
        self.timeline = AuditTimelineStore(repo_root)
        self.runs = ControllerRunRegistry(repo_root)
        self.hitl = HitlQueueStore(repo_root)
        self.workflow_policy = WorkflowPolicyEngine(repo_root)

    def summary(self, *, limit_tasks: int = 25) -> dict[str, Any]:
        task_ids = set(self.workflow_policy.list_task_ids())
        for run in self.runs.list_runs(limit=500):
            task_id = str(run.get("task_id", "")).upper()
            if task_id:
                task_ids.add(task_id)
        task_cards = []
        event_type_counts: dict[str, int] = {}
        level_counts: dict[str, int] = {}
        pending_hitl = self.hitl.list_entries(include_resolved=False, limit=500)
        for task_id in sorted(task_ids):
            events = self.timeline.list_events(task_id=task_id, limit=200)
            latest = events[-1] if events else None
            run = self.runs.load_latest(task_id)
            policy = self.workflow_policy.load(task_id)
            for item in events:
                event_type = str(item.get("event_type", "unknown"))
                level = str(item.get("level", "INFO"))
                event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
                level_counts[level] = level_counts.get(level, 0) + 1
            task_cards.append(
                {
                    "task_id": task_id,
                    "last_event_id": latest.get("id") if latest else None,
                    "last_event_type": latest.get("event_type") if latest else None,
                    "last_event_at": latest.get("timestamp") if latest else None,
                    "lifecycle_status": (policy or {}).get("lifecycle_status"),
                    "current_stage": (policy or {}).get("current_stage"),
                    "run_status": (run or {}).get("status"),
                    "pending_hitl_count": len([item for item in pending_hitl if item.get("task_id") == task_id]),
                }
            )
        active_runs = 0
        terminal_runs = 0
        for card in task_cards:
            run_status = str(card.get("run_status") or "")
            if not run_status:
                continue
            if run_status in TERMINAL_STATUSES:
                terminal_runs += 1
            else:
                active_runs += 1
        task_cards.sort(key=lambda item: (item.get("last_event_at") or "", item["task_id"]), reverse=True)
        return {
            "task_count": len(task_cards),
            "active_run_count": active_runs,
            "terminal_run_count": terminal_runs,
            "pending_hitl_count": len(pending_hitl),
            "event_type_counts": event_type_counts,
            "level_counts": level_counts,
            "task_cards": task_cards[:limit_tasks],
        }
