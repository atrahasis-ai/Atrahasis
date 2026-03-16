from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, runtime_logs_dir, runtime_state_dir, utc_now, write_json


class ControllerDaemonManager:
    """Starts and manages the operator stack as a detached local process."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.state_root = ensure_dir(runtime_state_dir(repo_root) / "controller_daemon")
        self.log_root = ensure_dir(runtime_logs_dir(repo_root) / "controller_daemon")
        self.state_path = self.state_root / "latest.json"

    def status(self) -> dict[str, Any]:
        payload = self._load()
        pid = payload.get("pid")
        payload["running"] = bool(pid) and self._pid_exists(int(pid))
        return payload

    def start(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 4180,
        app_server_url: str = "ws://127.0.0.1:8765",
        codex_executable: str | None = None,
    ) -> dict[str, Any]:
        current = self.status()
        if current.get("running"):
            return current
        script = self.repo_root / "scripts" / "aas_controller.py"
        stdout_path = self.log_root / "stdout.log"
        stderr_path = self.log_root / "stderr.log"
        stdout_handle = stdout_path.open("a", encoding="utf-8")
        stderr_handle = stderr_path.open("a", encoding="utf-8")
        cmd = [
            sys.executable,
            str(script),
            "serve",
            "--host",
            host,
            "--port",
            str(port),
            "--app-server-url",
            app_server_url,
        ]
        if codex_executable:
            cmd.extend(["--codex-executable", codex_executable])
        kwargs: dict[str, Any] = {}
        creationflags = 0
        if os.name == "nt":
            creationflags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        else:
            kwargs["start_new_session"] = True
        process = subprocess.Popen(
            cmd,
            cwd=self.repo_root,
            stdout=stdout_handle,
            stderr=stderr_handle,
            stdin=subprocess.DEVNULL,
            creationflags=creationflags,
            **kwargs,
        )
        payload = {
            "pid": process.pid,
            "host": host,
            "port": port,
            "ui_url": f"http://{host}:{port}/operator/",
            "app_server_url": app_server_url,
            "codex_executable": codex_executable or shutil.which("codex-alpha") or shutil.which("codex"),
            "started_at": utc_now(),
            "stdout_log": str(stdout_path.relative_to(self.repo_root)),
            "stderr_log": str(stderr_path.relative_to(self.repo_root)),
        }
        self._write(payload)
        return self.status()

    def stop(self) -> dict[str, Any]:
        payload = self._load()
        pid = int(payload.get("pid") or 0)
        if pid and self._pid_exists(pid):
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False, capture_output=True, text=True, encoding="utf-8")
            else:
                os.kill(pid, signal.SIGTERM)
        payload["stopped_at"] = utc_now()
        self._write(payload)
        return self.status()

    def _load(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return {"running": False}
        from aas1.common import load_json

        return load_json(self.state_path)

    def _write(self, payload: dict[str, Any]) -> None:
        write_json(self.state_path, payload)

    def _pid_exists(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True
