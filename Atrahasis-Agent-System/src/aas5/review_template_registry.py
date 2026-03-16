from __future__ import annotations

from pathlib import Path
from typing import Any


DEFAULT_STAGE_REVIEW_ROLES = {
    "IDEATION": "systems_thinker",
    "RESEARCH": "prior_art_researcher",
    "FEASIBILITY": "critic",
    "DESIGN": "systems_thinker",
    "SPECIFICATION": "specification_writer",
    "ASSESSMENT": "assessment_council",
}

DEFAULT_ROLE = "critic"


class ReviewTemplateRegistry:
    """Resolve stable, repo-local review templates by stage or explicit role."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.template_root = repo_root / "docs" / "platform_overlays" / "codex" / "review_templates"

    def resolve(
        self,
        *,
        task_id: str,
        workflow_policy: dict[str, Any] | None,
        explicit_role: str | None = None,
    ) -> dict[str, Any]:
        stage = self._normalize_stage((workflow_policy or {}).get("current_stage"))
        role = self._normalize_role(explicit_role) or DEFAULT_STAGE_REVIEW_ROLES.get(stage, DEFAULT_ROLE)
        path = self.template_root / f"{role}.md"
        if not path.exists():
            role = DEFAULT_ROLE
            path = self.template_root / f"{role}.md"
        text = path.read_text(encoding="utf-8")
        return {
            "task_id": task_id,
            "stage": stage,
            "role": role,
            "path": path.relative_to(self.repo_root).as_posix(),
            "text": text,
        }

    def compose(
        self,
        *,
        task_id: str,
        template: dict[str, Any],
        instructions: str | None,
    ) -> str:
        parts = [
            f"Apply the Atrahasis review template `{template['role']}` for task `{task_id}`.",
            f"Current workflow stage: `{template.get('stage') or 'UNKNOWN'}`.",
            "Return findings first. Cite concrete artifact paths when possible. Respect HITL gates and do not assume canonical closeout authority.",
            "",
            "## Template",
            template["text"].strip(),
        ]
        if instructions:
            parts[0:0] = [
                "## Additional Operator Instructions",
                instructions.strip(),
                "",
            ]
        return "\n".join(parts).strip() + "\n"

    def _normalize_role(self, value: str | None) -> str | None:
        if not value:
            return None
        return str(value).strip().lower().replace(" ", "_")

    def _normalize_stage(self, value: Any) -> str:
        if value is None:
            return "UNKNOWN"
        return str(value).strip().upper().replace(" ", "_")
