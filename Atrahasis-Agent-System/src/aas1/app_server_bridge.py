from __future__ import annotations

import json
import shutil
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass
class _PendingResponse:
    event: threading.Event
    result: dict[str, Any] | None = None
    error: str | None = None


class AppServerBridge:
    """Persistent JSONL bridge between the controller and Codex App Server."""

    def __init__(
        self,
        *,
        repo_root: Path,
        ws_url: str,
        initialize_params: dict[str, Any],
        event_handler: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        self.repo_root = repo_root
        self.ws_url = ws_url
        self.initialize_params = initialize_params
        self.event_handler = event_handler
        self.script_path = repo_root / "scripts" / "app_server_bridge.mjs"
        self.node_executable = shutil.which("node") or "node"
        self._process: subprocess.Popen[str] | None = None
        self._stdout_thread: threading.Thread | None = None
        self._stderr_thread: threading.Thread | None = None
        self._pending: dict[str, _PendingResponse] = {}
        self._sequence = 0
        self._lock = threading.Lock()
        self._pending_lock = threading.Lock()
        self._send_lock = threading.Lock()
        self._connected = threading.Event()

    def start(self, *, timeout_seconds: float = 8.0) -> None:
        with self._lock:
            if self.is_running:
                return
            self._connected.clear()
            self._process = subprocess.Popen(
                [self.node_executable, str(self.script_path), self.ws_url],
                cwd=self.repo_root,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
            self._stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
            self._stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
            self._stdout_thread.start()
            self._stderr_thread.start()
        if not self._connected.wait(timeout_seconds):
            raise RuntimeError("Timed out connecting controller bridge to Codex App Server.")
        self.request("initialize", self.initialize_params, timeout_seconds=timeout_seconds)

    def stop(self) -> None:
        with self._lock:
            process = self._process
            if process is None:
                return
            self._send({"type": "close"})
            try:
                process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=2.0)
            self._process = None
            self._connected.clear()
            self._flush_pending("Bridge stopped before response.")

    @property
    def is_running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def request(self, method: str, params: dict[str, Any], *, timeout_seconds: float = 30.0) -> dict[str, Any]:
        if not self.is_running:
            raise RuntimeError("Bridge is not running.")
        request_id = self._next_request_id()
        pending = _PendingResponse(event=threading.Event())
        with self._pending_lock:
            self._pending[request_id] = pending
        self._send({"type": "request", "id": request_id, "method": method, "params": params})
        if not pending.event.wait(timeout_seconds):
            with self._pending_lock:
                self._pending.pop(request_id, None)
            raise TimeoutError(f"Timed out waiting for App Server response to {method}.")
        if pending.error:
            raise RuntimeError(pending.error)
        return pending.result or {}

    def respond(self, request_id: str | int, result: dict[str, Any]) -> None:
        if not self.is_running:
            raise RuntimeError("Bridge is not running.")
        self._send({"type": "respond", "id": request_id, "result": result})

    def _next_request_id(self) -> str:
        with self._lock:
            self._sequence += 1
            return f"bridge-{self._sequence:05d}"

    def _send(self, payload: dict[str, Any]) -> None:
        with self._send_lock:
            process = self._process
            if process is None or process.stdin is None:
                raise RuntimeError("Bridge stdin is unavailable.")
            process.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
            process.stdin.flush()

    def _read_stdout(self) -> None:
        assert self._process is not None and self._process.stdout is not None
        for raw_line in self._process.stdout:
            line = raw_line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                self._emit({"type": "bridge_error", "message": f"Invalid bridge JSON: {line}"})
                continue
            event_type = event.get("type")
            if event_type == "connected":
                self._connected.set()
            elif event_type == "rpc_response":
                with self._pending_lock:
                    pending = self._pending.pop(str(event.get("id")), None)
                if pending is not None:
                    pending.result = event.get("result", {})
                    pending.event.set()
                continue
            elif event_type == "rpc_error":
                with self._pending_lock:
                    pending = self._pending.pop(str(event.get("id")), None)
                if pending is not None:
                    pending.error = event.get("message", "App Server request failed.")
                    pending.event.set()
                continue
            elif event_type == "closed":
                self._connected.clear()
                self._flush_pending("App Server bridge closed before response.")
            self._emit(event)

    def _read_stderr(self) -> None:
        assert self._process is not None and self._process.stderr is not None
        for raw_line in self._process.stderr:
            line = raw_line.rstrip()
            if not line:
                continue
            self._emit({"type": "bridge_stderr", "message": line})

    def _emit(self, event: dict[str, Any]) -> None:
        if self.event_handler is None:
            return
        try:
            self.event_handler(event)
        except Exception:
            # Avoid crashing the bridge reader because of controller-side logging errors.
            return

    def _flush_pending(self, message: str) -> None:
        with self._pending_lock:
            for pending in self._pending.values():
                pending.error = message
                pending.event.set()
            self._pending.clear()
