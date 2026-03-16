from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aas1.common import (
    category_for_path,
    detect_ids,
    ensure_dir,
    load_json,
    load_yaml,
    runtime_state_dir,
    summarize_text,
    write_json,
)


class KnowledgeIndex:
    CORE_FILES = (
        "docs/AGENT_STATE.md",
        "docs/SESSION_BRIEF.md",
        "docs/INVENTION_DASHBOARD.md",
        "docs/DECISIONS.md",
        "docs/PATTERN_REGISTER.md",
        "docs/TODO.md",
        "docs/HITL_POLICY.md",
    )
    SUPPORTED_SUFFIXES = {".md", ".json", ".yaml", ".yml"}
    MANIFEST_EXCLUDED_PREFIXES = (
        "docs/handoffs/",
        "docs/task_claims/",
        "docs/task_workspaces/",
        "docs/templates/",
    )

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.index_root = ensure_dir(runtime_state_dir(repo_root) / "knowledge_index")
        self.cache_path = self.index_root / "document_cache.json"
        self.cache = self._load_cache()

    def load_core_memory(self) -> dict[str, Any]:
        result: dict[str, Any] = {"agent_state": {}, "documents": []}
        state_path = self.repo_root / "docs" / "AGENT_STATE.md"
        if state_path.exists():
            try:
                result["agent_state"] = load_yaml(state_path) or {}
            except Exception:
                result["agent_state"] = {}
        for rel_path in self.CORE_FILES:
            path = self.repo_root / rel_path
            if not path.exists():
                continue
            entry = dict(self._document_entry(path))
            entry["text"] = entry["text"][:8000]
            result["documents"].append(entry)
        self._flush_cache()
        return result

    def collect_repo_manifest(self) -> list[dict[str, Any]]:
        manifest: list[dict[str, Any]] = []
        docs_root = self.repo_root / "docs"
        if not docs_root.exists():
            return manifest
        for path in sorted(docs_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in self.SUPPORTED_SUFFIXES:
                continue
            if self._exclude_from_manifest(path):
                continue
            manifest.append(self._document_entry(path))
        self._flush_cache()
        return manifest

    def load_task_workspace(self, task_id: str) -> list[dict[str, Any]]:
        task_dir = self.repo_root / "docs" / "task_workspaces" / task_id
        if not task_dir.exists():
            return []
        workspace_docs = []
        for path in sorted(task_dir.rglob("*")):
            if path.is_file() and path.suffix.lower() in self.SUPPORTED_SUFFIXES:
                workspace_docs.append(self._document_entry(path))
        self._flush_cache()
        return workspace_docs

    def load_hypothesis_archive(self) -> list[dict[str, Any]]:
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

    def count_workflow_runs(self) -> int:
        task_root = self.repo_root / "docs" / "task_workspaces"
        if not task_root.exists():
            return 0
        return sum(1 for _path in task_root.rglob("WORKFLOW_RUN_RECORD.json"))

    def prune_task_workspaces(self, task_ids: list[str]) -> list[str]:
        prefixes = [f"docs/task_workspaces/{task_id}/" for task_id in task_ids]
        removed = []
        for rel_path in list(self.cache):
            if any(rel_path.startswith(prefix) for prefix in prefixes):
                removed.append(rel_path)
                del self.cache[rel_path]
        if removed:
            self._flush_cache()
        return removed

    def _document_entry(self, path: Path) -> dict[str, Any]:
        rel_path = str(path.relative_to(self.repo_root)).replace("\\", "/")
        signature = self._signature(path)
        cached = self.cache.get(rel_path)
        if cached and cached.get("signature") == signature:
            return dict(cached["entry"])
        text = path.read_text(encoding="utf-8", errors="ignore")
        ids = detect_ids(path.relative_to(self.repo_root))
        entry = {
            "path": rel_path,
            "category": category_for_path(path),
            "summary": summarize_text(text),
            "word_count": len(text.split()),
            "invention_ids": ids["inventions"],
            "task_ids": ids["tasks"],
            "text": text[:12000],
        }
        self.cache[rel_path] = {"signature": signature, "entry": entry}
        return dict(entry)

    def _load_cache(self) -> dict[str, dict[str, Any]]:
        if not self.cache_path.exists():
            return {}
        payload = load_json(self.cache_path)
        return payload.get("documents", {})

    def _flush_cache(self) -> None:
        write_json(
            self.cache_path,
            {
                "type": "KNOWLEDGE_INDEX_CACHE",
                "documents": self.cache,
            },
        )

    def _signature(self, path: Path) -> dict[str, int]:
        stat = path.stat()
        return {
            "mtime_ns": stat.st_mtime_ns,
            "size": stat.st_size,
        }

    def _exclude_from_manifest(self, path: Path) -> bool:
        rel_path = str(path.relative_to(self.repo_root)).replace("\\", "/").lower()
        return rel_path.startswith(self.MANIFEST_EXCLUDED_PREFIXES)
