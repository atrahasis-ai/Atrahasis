#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from aas1.spec_path_resolver import resolve_spec_path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/resolve_spec_path.py <SPEC_ID> [<SPEC_ID> ...]", file=sys.stderr)
        return 2

    payload = []
    for raw_spec_id in sys.argv[1:]:
        spec_id = raw_spec_id.strip().upper()
        try:
            resolved = resolve_spec_path(REPO_ROOT, spec_id)
        except Exception as exc:
            payload.append({"spec_id": spec_id, "resolved": False, "error": str(exc)})
            continue
        payload.append(
            {
                "spec_id": spec_id,
                "resolved": True,
                "path": str(resolved.relative_to(REPO_ROOT)).replace("\\", "/"),
            }
        )

    print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2))
    return 0 if all(item.get("resolved") for item in payload) else 1


if __name__ == "__main__":
    raise SystemExit(main())
