from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "through",
    "when",
    "where",
    "then",
    "than",
    "them",
    "they",
    "must",
    "will",
    "have",
    "has",
    "into",
    "your",
    "their",
    "about",
    "does",
    "used",
    "use",
    "using",
    "only",
    "each",
    "what",
    "which",
    "same",
    "more",
    "also",
    "just",
    "over",
    "under",
    "been",
    "being",
    "most",
    "such",
}


@dataclass
class CommandRequest:
    command_modifier: str
    task_id: str
    prompt: str
    scope: str
    operator_constraints: list[str] = field(default_factory=list)
    hitl_requirements: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: utc_now())


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def repo_root_from(anchor: Path) -> Path:
    return anchor.resolve().parents[2]


def workspace_root_from_repo(repo_root: Path) -> Path:
    return repo_root.parent


def legacy_runtime_root_dir(repo_root: Path) -> Path:
    return workspace_root_from_repo(repo_root) / "AAS" / "runtime"


def runtime_root_dir(repo_root: Path) -> Path:
    return repo_root / "runtime"


def runtime_state_dir(repo_root: Path) -> Path:
    return runtime_root_dir(repo_root) / "state"


def runtime_logs_dir(repo_root: Path) -> Path:
    return runtime_root_dir(repo_root) / "logs"


def summarize_text(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
        if stripped:
            return stripped[:180]
    return ""


def keyword_profile(texts: list[str], limit: int = 12) -> list[str]:
    counter: Counter[str] = Counter()
    for text in texts:
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text.lower()):
            if token not in STOPWORDS:
                counter[token] += 1
    return [word for word, _count in counter.most_common(limit)]


def detect_ids(path: Path) -> dict[str, list[str]]:
    text = str(path)
    return {
        "inventions": sorted(set(re.findall(r"C\d+", text))),
        "tasks": sorted(set(re.findall(r"T-\d+", text))),
    }


def category_for_path(path: Path) -> str:
    parts = {part.lower() for part in path.parts}
    if "task_workspaces" in parts:
        return "task_workspace"
    if "prior_art" in parts:
        return "prior_art"
    if "specifications" in parts:
        return "specification"
    if "invention_logs" in parts:
        return "invention_log"
    if "schemas" in parts:
        return "schema"
    if "scripts" in parts:
        return "script"
    return "core_doc"
