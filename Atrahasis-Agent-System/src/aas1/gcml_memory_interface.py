from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aas1.common import category_for_path, detect_ids, load_yaml, summarize_text


class GCMLMemoryInterface:
    CORE_FILES = (
        "docs/AGENT_STATE.md",
        "docs/SESSION_BRIEF.md",
        "docs/INVENTION_DASHBOARD.md",
        "docs/DECISIONS.md",
        "docs/PATTERN_REGISTER.md",
        "docs/TODO.md",
        "docs/HITL_POLICY.md",
    )
    MANIFEST_EXCLUDED_PREFIXES = (
        "docs/handoffs/",
        "docs/task_claims/",
        "docs/task_workspaces/",
        "docs/templates/",
    )

    def __init__(self, repo_root: Path, knowledge_index: Any | None = None) -> None:
        self.repo_root = repo_root
        self.knowledge_index = knowledge_index

    def load_core_memory(self) -> dict[str, Any]:
        if self.knowledge_index is not None:
            return self.knowledge_index.load_core_memory()
        result: dict[str, Any] = {"agent_state": {}, "documents": []}
        state_path = self.repo_root / "docs" / "AGENT_STATE.md"
        if state_path.exists():
            try:
                result["agent_state"] = load_yaml(state_path) or {}
            except Exception:
                result["agent_state"] = {}
        for rel_path in self.CORE_FILES:
            path = self.repo_root / rel_path
            if path.exists():
                text = path.read_text(encoding="utf-8")
                result["documents"].append(
                    {"path": rel_path, "summary": summarize_text(text), "text": text[:8000]}
                )
        return result

    def collect_repo_manifest(self) -> list[dict[str, Any]]:
        if self.knowledge_index is not None:
            return self.knowledge_index.collect_repo_manifest()
        manifest: list[dict[str, Any]] = []
        for path in sorted((self.repo_root / "docs").rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml"}:
                continue
            if self._exclude_from_manifest(path):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            ids = detect_ids(path.relative_to(self.repo_root))
            manifest.append(
                {
                    "path": str(path.relative_to(self.repo_root)).replace("\\", "/"),
                    "category": category_for_path(path),
                    "summary": summarize_text(text),
                    "word_count": len(text.split()),
                    "invention_ids": ids["inventions"],
                    "task_ids": ids["tasks"],
                    "text": text[:12000],
                }
            )
        return manifest

    def load_task_workspace(self, task_id: str) -> list[dict[str, Any]]:
        if self.knowledge_index is not None:
            return self.knowledge_index.load_task_workspace(task_id)
        task_dir = self.repo_root / "docs" / "task_workspaces" / task_id
        if not task_dir.exists():
            return []
        workspace_docs: list[dict[str, Any]] = []
        for path in sorted(task_dir.rglob("*")):
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                workspace_docs.append(
                    {
                        "path": str(path.relative_to(self.repo_root)).replace("\\", "/"),
                        "summary": summarize_text(text),
                        "word_count": len(text.split()),
                        "text": text[:12000],
                    }
                )
        return workspace_docs

    def count_workflow_runs(self) -> int:
        if self.knowledge_index is not None:
            return self.knowledge_index.count_workflow_runs()
        task_root = self.repo_root / "docs" / "task_workspaces"
        if not task_root.exists():
            return 0
        return sum(1 for _path in task_root.rglob("WORKFLOW_RUN_RECORD.json"))

    def load_hypothesis_archive(self) -> list[dict[str, Any]]:
        if self.knowledge_index is not None:
            return self.knowledge_index.load_hypothesis_archive()
        task_root = self.repo_root / "docs" / "task_workspaces"
        if not task_root.exists():
            return []

        archive: list[dict[str, Any]] = []
        for path in sorted(task_root.rglob("HYPOTHESIS_PACKET.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            task_id = path.parent.name
            for hypothesis in payload.get("hypotheses", []):
                archive.append(
                    {
                        "task_id": task_id,
                        "artifact_path": str(path.relative_to(self.repo_root)).replace("\\", "/"),
                        "hypothesis": hypothesis,
                    }
                )
        return archive

    def _exclude_from_manifest(self, path: Path) -> bool:
        rel_path = str(path.relative_to(self.repo_root)).replace("\\", "/").lower()
        return rel_path.startswith(self.MANIFEST_EXCLUDED_PREFIXES)
