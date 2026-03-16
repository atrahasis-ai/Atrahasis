from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


TASK_ID_RE = re.compile(r"^T-(\d+)$")


@dataclass(frozen=True)
class TaskBand:
    label: str
    start: int
    end: int
    description: str

    def contains(self, number: int) -> bool:
        return self.start <= number <= self.end


class TaskIdPolicy:
    """Central task-ID allocation and validation policy for AAS3."""

    BANDS = {
        "canonical": TaskBand(
            label="canonical",
            start=1,
            end=7999,
            description="Canonical shared backlog work tied to TODO/claims/closeout.",
        ),
        "analysis": TaskBand(
            label="analysis",
            start=9000,
            end=9499,
            description="Ad hoc analysis, architecture questions, and idea integration.",
        ),
        "validation": TaskBand(
            label="validation",
            start=9500,
            end=9799,
            description="Runtime, provider, and system validation tasks.",
        ),
        "demo": TaskBand(
            label="demo",
            start=9800,
            end=9999,
            description="Demo, operator-interface, and walkthrough scenarios.",
        ),
    }

    DEFAULT_CLASS_FOR_MODIFIER = {
        "AASBT": "canonical",
        "AASA": "analysis",
        "AASAQ": "analysis",
        "AASNI": "analysis",
    }

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.workspaces_root = repo_root / "docs" / "task_workspaces"
        self.claims_root = repo_root / "docs" / "task_claims"
        self.archived_workspaces_root = repo_root / "archive" / "retired_workflows" / "task_workspaces"
        self.runtime_archived_workflows_root = (
            repo_root.parent / "AAS" / "runtime" / "archive" / "retired_workflows" / "state" / "workflows"
        )

    def resolve(
        self,
        *,
        modifier: str,
        requested_task_id: str | None,
        task_class: str = "auto",
    ) -> tuple[str, str, bool]:
        normalized_modifier = modifier.strip().upper()
        resolved_class = self._resolve_task_class(normalized_modifier, task_class)

        if requested_task_id:
            task_id = self._normalize_task_id(requested_task_id)
            self._validate_requested_task_id(
                task_id=task_id,
                modifier=normalized_modifier,
                task_class=resolved_class,
            )
            return task_id, resolved_class, False

        if normalized_modifier == "AASBT":
            raise ValueError(
                "AASBT requires an explicit canonical task ID. It will not auto-mint one."
            )

        task_id = self._allocate_new_id(resolved_class)
        return task_id, resolved_class, True

    def _validate_requested_task_id(
        self,
        *,
        task_id: str,
        modifier: str,
        task_class: str,
    ) -> None:
        number = self._task_number(task_id)
        if self._task_exists(task_id):
            return

        if modifier == "AASBT":
            band = self.BANDS["canonical"]
            if not band.contains(number):
                raise ValueError(
                    f"AASBT task IDs must be in the canonical band T-{band.start:03d} to T-{band.end}. "
                    f"Received {task_id}."
                )
            return

        band = self.BANDS[task_class]
        if not band.contains(number):
            raise ValueError(
                f"New {modifier} task IDs must be in the {task_class} band "
                f"T-{band.start} to T-{band.end}. Received {task_id}."
            )

    def _allocate_new_id(self, task_class: str) -> str:
        band = self.BANDS[task_class]
        for number in range(band.start, band.end + 1):
            candidate = f"T-{number}"
            if not self._task_exists(candidate):
                return candidate
        raise ValueError(
            f"No free task IDs remain in the {task_class} band "
            f"T-{band.start} to T-{band.end}."
        )

    def _resolve_task_class(self, modifier: str, task_class: str) -> str:
        normalized = task_class.strip().lower()
        if normalized == "auto":
            return self.DEFAULT_CLASS_FOR_MODIFIER[modifier]
        if normalized not in self.BANDS:
            raise ValueError(f"Unsupported task class: {task_class}")
        if modifier == "AASBT" and normalized != "canonical":
            raise ValueError("AASBT may only use the canonical task class.")
        return normalized

    def _task_exists(self, task_id: str) -> bool:
        return (
            (self.workspaces_root / task_id).exists()
            or (self.claims_root / f"{task_id}.yaml").exists()
            or (self.archived_workspaces_root / task_id).exists()
            or (self.runtime_archived_workflows_root / task_id).exists()
        )

    def _normalize_task_id(self, value: str) -> str:
        token = value.strip().upper()
        if not TASK_ID_RE.match(token):
            raise ValueError(f"Invalid task ID format: {value}. Expected T-<number>.")
        return token

    def _task_number(self, task_id: str) -> int:
        match = TASK_ID_RE.match(task_id)
        if not match:
            raise ValueError(f"Invalid task ID format: {task_id}")
        return int(match.group(1))
