#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def main() -> int:
    if len(sys.argv) != 2:
        eprint("Usage: python scripts/validate_swarm_execution_record.py <TASK_ID>")
        return 2

    task_id = sys.argv[1].strip().upper()
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas1.swarm_validation import validate_swarm_execution_task

    failures = validate_swarm_execution_task(repo_root=repo_root, task_id=task_id)
    if failures:
        eprint("[FAIL] SWARM_EXECUTION_RECORD.json")
        for item in failures:
            eprint(f"  - {item}")
        return 1

    print("[OK] SWARM_EXECUTION_RECORD.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
