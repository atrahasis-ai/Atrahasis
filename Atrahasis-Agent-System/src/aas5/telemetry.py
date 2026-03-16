from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aas5.common import ensure_dir, runtime_logs_dir, utc_now


class Telemetry:
    def __init__(self, repo_root: Path) -> None:
        self.logs_dir = ensure_dir(runtime_logs_dir(repo_root))

    def emit(self, log_name: str, event: str, **payload: Any) -> None:
        record = {"timestamp": utc_now(), "event": event, **payload}
        path = self.logs_dir / f"{log_name}.log"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
