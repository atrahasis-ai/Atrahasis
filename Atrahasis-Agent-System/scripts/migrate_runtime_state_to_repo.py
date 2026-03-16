#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


RUNTIME_BUCKETS = ("state", "logs", "archive")


def merge_move(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        return
    if not source.is_dir() or not destination.is_dir():
        raise FileExistsError(f"Cannot merge non-directory paths: {source} -> {destination}")
    for child in sorted(source.iterdir(), key=lambda path: path.name):
        target = destination / child.name
        if target.exists():
            if child.is_dir() and target.is_dir():
                merge_move(child, target)
                continue
            raise FileExistsError(f"Destination already exists: {target}")
        shutil.move(str(child), str(target))
    if source.exists() and not any(source.iterdir()):
        source.rmdir()


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    legacy_root = repo_root.parent / "AAS" / "runtime"
    target_root = repo_root / "runtime"

    summary: dict[str, Any] = {
        "repo_root": str(repo_root),
        "legacy_runtime_root": str(legacy_root),
        "target_runtime_root": str(target_root),
        "migrations": [],
    }

    target_root.mkdir(parents=True, exist_ok=True)

    for bucket in RUNTIME_BUCKETS:
        source = legacy_root / bucket
        destination = target_root / bucket
        if not source.exists():
            summary["migrations"].append(
                {
                    "bucket": bucket,
                    "status": "missing",
                    "source": str(source),
                    "destination": str(destination),
                }
            )
            continue
        merge_move(source, destination)
        summary["migrations"].append(
            {
                "bucket": bucket,
                "status": "migrated",
                "source": str(source),
                "destination": str(destination),
            }
        )

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
