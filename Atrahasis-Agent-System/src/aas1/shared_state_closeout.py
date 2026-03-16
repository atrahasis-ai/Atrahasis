from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from aas1.common import utc_now, write_text


class SharedStateCloseoutManager:
    """Applies narrow canonical shared-state closeout updates after task completion."""

    TASK_ROW_RE = re.compile(r"^\|\s*`?(?P<task_id>T-[A-Z0-9-]+)`?\s*\|", re.IGNORECASE)
    VALID_AGENT_STATE_ACTORS = {"Director", "Chronicler"}

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.docs_root = repo_root / "docs"

    def apply(
        self,
        *,
        task_id: str,
        task_title: str,
        workflow_status: str,
        operator_decision: str | None,
        invention_ids: list[str] | None = None,
        notes: list[str] | None = None,
        actor: str = "Controller",
    ) -> dict[str, Any]:
        completed_on = utc_now()[:10]
        changed_files = []
        todo_changes = self._update_todo(task_id=task_id, completed_on=completed_on)
        if todo_changes["changed"]:
            changed_files.append(todo_changes["path"])
        completed_changes = self._update_completed(
            task_id=task_id,
            task_title=task_title,
            completed_on=completed_on,
            operator_decision=operator_decision,
        )
        if completed_changes["changed"]:
            changed_files.append(completed_changes["path"])
        agent_state_changes = self._update_agent_state(
            task_id=task_id,
            task_title=task_title,
            workflow_status=workflow_status,
            completed_on=completed_on,
            actor=actor,
        )
        if agent_state_changes["changed"]:
            changed_files.append(agent_state_changes["path"])
        dashboard_changes = self._update_dashboard(
            task_id=task_id,
            task_title=task_title,
            invention_ids=invention_ids or [],
        )
        if dashboard_changes["changed"]:
            changed_files.append(dashboard_changes["path"])
        tribunal_changes = self._update_tribunal_log(
            task_id=task_id,
            task_title=task_title,
            workflow_status=workflow_status,
            operator_decision=operator_decision,
            notes=notes or [],
            completed_on=completed_on,
        )
        if tribunal_changes["changed"]:
            changed_files.append(tribunal_changes["path"])
        return {
            "type": "SHARED_STATE_CLOSEOUT_RECORD",
            "task_id": task_id,
            "task_title": task_title,
            "completed_on": completed_on,
            "workflow_status": workflow_status,
            "operator_decision": operator_decision,
            "invention_ids": invention_ids or [],
            "notes": notes or [],
            "changed_files": changed_files,
            "changed_components": {
                "todo": todo_changes,
                "completed": completed_changes,
                "agent_state": agent_state_changes,
                "dashboard": dashboard_changes,
                "tribunal_log": tribunal_changes,
            },
        }

    def _update_todo(self, *, task_id: str, completed_on: str) -> dict[str, Any]:
        path = self.docs_root / "TODO.md"
        text = path.read_text(encoding="utf-8")
        original = text
        lines = []
        for line in text.splitlines():
            match = self.TASK_ROW_RE.match(line.strip())
            if match and match.group("task_id").upper() == task_id.upper():
                continue
            lines.append(line)
        text = "\n".join(lines)
        section_match = re.search(r"## User Dispatch Order \(Simple\)\n(?P<body>.*?)(?:\nCompleted tasks|\n---|\Z)", text, re.DOTALL)
        if section_match:
            body_lines = []
            for raw in section_match.group("body").splitlines():
                if task_id not in raw:
                    body_lines.append(raw)
                    continue
                remaining = [item for item in re.findall(r"`(T-[A-Z0-9-]+)`", raw) if item.upper() != task_id.upper()]
                if not remaining:
                    continue
                prefix_match = re.match(r"^\s*\d+\.\s*", raw)
                prefix = prefix_match.group(0) if prefix_match else ""
                rest = re.sub(r"^\s*\d+\.\s*", "", raw)
                rest = re.sub(r"`T-[A-Z0-9-]+`", "{}", rest)
                body_lines.append(prefix + rest.format(*[f"`{item}`" for item in remaining]))
            renumbered = []
            counter = 1
            for raw in body_lines:
                if re.match(r"^\s*\d+\.\s*", raw):
                    renumbered.append(re.sub(r"^\s*\d+\.\s*", f"{counter}. ", raw))
                    counter += 1
                else:
                    renumbered.append(raw)
            body = "\n".join(renumbered).rstrip()
            text = text[: section_match.start("body")] + body + text[section_match.end("body") :]
        text = re.sub(
            r"\*Last updated: [^\n]+\*",
            f"*Last updated: {completed_on} ({task_id} task closeout)*",
            text,
            count=1,
        )
        if text != original:
            write_text(path, text)
        return {"path": str(path.relative_to(self.repo_root)), "changed": text != original}

    def _update_completed(
        self,
        *,
        task_id: str,
        task_title: str,
        completed_on: str,
        operator_decision: str | None,
    ) -> dict[str, Any]:
        path = self.docs_root / "COMPLETED.md"
        text = path.read_text(encoding="utf-8")
        if re.search(rf"^\|\s*{re.escape(task_id)}\s*\|", text, re.MULTILINE):
            return {"path": str(path.relative_to(self.repo_root)), "changed": False}
        line = f"| {task_id} | {task_title} | {completed_on} | Task closeout. Decision: {operator_decision or 'n/a'}. |"
        updated = text.rstrip() + "\n" + line + "\n"
        write_text(path, updated)
        return {"path": str(path.relative_to(self.repo_root)), "changed": True}

    def _update_agent_state(
        self,
        *,
        task_id: str,
        task_title: str,
        workflow_status: str,
        completed_on: str,
        actor: str,
    ) -> dict[str, Any]:
        path = self.docs_root / "AGENT_STATE.md"
        text = path.read_text(encoding="utf-8")
        original = text
        timestamp = utc_now()
        actor_name = actor if actor in self.VALID_AGENT_STATE_ACTORS else "Chronicler"
        text = re.sub(r'^last_updated: ".*"$', f'last_updated: "{timestamp}"', text, count=1, flags=re.MULTILINE)
        text = re.sub(r'^last_updated_by: ".*"$', f'last_updated_by: "{actor_name}"', text, count=1, flags=re.MULTILINE)
        summary = f'{task_id}: task closeout complete - {task_title} ({workflow_status}) on {completed_on}.'
        if summary not in text:
            text = text.rstrip() + f'\n  - "{summary}"\n'
        if text != original:
            write_text(path, text)
        return {"path": str(path.relative_to(self.repo_root)), "changed": text != original}

    def _update_dashboard(
        self,
        *,
        task_id: str,
        task_title: str,
        invention_ids: list[str],
    ) -> dict[str, Any]:
        path = self.docs_root / "INVENTION_DASHBOARD.md"
        text = path.read_text(encoding="utf-8")
        original = text
        closeout_label = invention_ids[0] if invention_ids else task_id
        closeout_title = invention_ids[0] if invention_ids else task_title
        text = re.sub(
            r"- Most recent canonical closeout: \*\*.+\*\*.*",
            f"- Most recent canonical closeout: **{closeout_label}** ({closeout_title})",
            text,
            count=1,
        )
        if text != original:
            write_text(path, text)
        return {"path": str(path.relative_to(self.repo_root)), "changed": text != original}

    def _update_tribunal_log(
        self,
        *,
        task_id: str,
        task_title: str,
        workflow_status: str,
        operator_decision: str | None,
        notes: list[str],
        completed_on: str,
    ) -> dict[str, Any]:
        path = self.docs_root / "TRIBUNAL_LOG.md"
        text = path.read_text(encoding="utf-8")
        marker = f"## Task Closeout: {task_id}"
        if marker in text:
            return {"path": str(path.relative_to(self.repo_root)), "changed": False}
        entry = [
            "",
            "---",
            marker,
            f"- Date: {completed_on}",
            f"- Task: {task_id}",
            f"- Title: {task_title}",
            f"- Workflow status: {workflow_status}",
            f"- Operator decision: {operator_decision or 'n/a'}",
        ]
        if notes:
            entry.append("- Notes:")
            entry.extend([f"  - {item}" for item in notes])
        updated = text.rstrip() + "\n" + "\n".join(entry) + "\n"
        write_text(path, updated)
        return {"path": str(path.relative_to(self.repo_root)), "changed": True}
