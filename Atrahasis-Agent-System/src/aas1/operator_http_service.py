from __future__ import annotations

import json
import threading
import webbrowser
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from aas1.common import utc_now
from aas1.control_plane import AtrahasisControlPlane
from aas1.invention_pipeline_manager import InventionPipelineManager
from aas1.operator_controller_service import OperatorControllerService
from aas1.task_id_policy import TASK_ID_RE, TaskIdPolicy


DEFAULT_OPERATOR_HOST = "127.0.0.1"
DEFAULT_OPERATOR_PORT = 4180
RETIRED_RUNTIME_MESSAGE = (
    "Controller-owned App Server runtime has been retired from AAS5. "
    "Use direct provider sessions and task-local artifacts instead."
)


def _bool_arg(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _now_display() -> str:
    return datetime.now().astimezone().isoformat()


class ControllerEventBroker:
    def __init__(self, *, max_events: int = 400) -> None:
        self._events: deque[dict[str, Any]] = deque(maxlen=max_events)
        self._condition = threading.Condition()
        self._counter = 0

    def publish(self, event: dict[str, Any]) -> dict[str, Any]:
        with self._condition:
            self._counter += 1
            payload = {
                "id": self._counter,
                "timestamp": event.get("timestamp", utc_now()),
                "event_type": event.get("event_type", "controller_event"),
                "payload": event.get("payload", {}),
            }
            self._events.append(payload)
            self._condition.notify_all()
            return payload

    def wait_for_events(
        self,
        *,
        after_id: int,
        timeout_seconds: float,
        task_id: str | None = None,
    ) -> list[dict[str, Any]]:
        def _matches(event: dict[str, Any]) -> bool:
            if event["id"] <= after_id:
                return False
            if not task_id:
                return True
            payload = event.get("payload", {})
            payload_task = payload.get("task_id") or payload.get("run", {}).get("task_id")
            return payload_task is None or payload_task == task_id

        with self._condition:
            if not any(_matches(event) for event in self._events):
                self._condition.wait(timeout_seconds)
            return [event for event in self._events if _matches(event)]


@dataclass
class RetiredRuntimeLaunchConfig:
    listen_url: str | None = None
    codex_executable: str | None = None


class RetiredRuntimeManager:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.launch_config = RetiredRuntimeLaunchConfig()

    def start(self, *, listen_url: str | None = None, codex_executable: str | None = None) -> dict[str, Any]:
        return self.status()

    def stop(self) -> dict[str, Any]:
        return self.status()

    def status(self) -> dict[str, Any]:
        return {
            "enabled": False,
            "running": False,
            "mode": "retired",
            "reason": RETIRED_RUNTIME_MESSAGE,
            "listen_url": None,
            "codex_executable": None,
        }

    def client_config(self) -> dict[str, Any]:
        return {
            "enabled": False,
            "mode": "retired",
            "reason": RETIRED_RUNTIME_MESSAGE,
            "repo_root": str(self.repo_root),
        }


class OperatorHttpServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        server_address: tuple[str, int],
        handler_class: type[BaseHTTPRequestHandler],
        *,
        repo_root: Path,
        ui_path: Path,
    ) -> None:
        super().__init__(server_address, handler_class)
        self.repo_root = repo_root
        self.ui_path = ui_path
        self.control = AtrahasisControlPlane(repo_root)
        self.controller_lock = threading.Lock()
        self.runtime_bridge = RetiredRuntimeManager(repo_root)
        self.event_broker = ControllerEventBroker()
        self.controller = OperatorControllerService(
            repo_root,
            control=self.control,
            runtime_bridge=self.runtime_bridge,
            event_callback=self.event_broker.publish,
            start_monitor=True,
        )


class OperatorHttpHandler(BaseHTTPRequestHandler):
    server_version = "AtrahasisOperatorHTTP/0.1"

    @property
    def operator_server(self) -> OperatorHttpServer:
        return self.server  # type: ignore[return-value]

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Allow", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path in {"/", "/operator", "/operator/", "/ui/operator_console.html"}:
                return self._serve_ui()
            if path == "/api/health":
                return self._send_json(
                    {
                        "service": "aas-operator-http",
                        "status": "ok",
                        "timestamp": _now_display(),
                        "repo_root": str(self.operator_server.repo_root),
                        "runtime_bridge": self.operator_server.runtime_bridge.status(),
                    }
                )
            if path == "/api/controller/session-brief":
                return self._send_json(self.operator_server.control.get_session_brief())
            if path == "/api/controller/dispatchable":
                limit = int(query.get("limit", ["5"])[0])
                return self._send_json(self.operator_server.control.get_dispatchable_tasks(limit=limit))
            if path == "/api/controller/status":
                task_id = self._required_query(query, "task_id").upper()
                return self._send_json(self.operator_server.control.get_task_status(task_id=task_id))
            if path == "/api/controller/prompt":
                task_id = self._required_query(query, "task_id").upper()
                manager = InventionPipelineManager(self.operator_server.repo_root)
                return self._send_json({"task_id": task_id, "prompt": manager.render_operator_prompt(task_id=task_id)})
            if path == "/api/controller/claims":
                active_only = not _bool_arg(query.get("all", [None])[0], default=False)
                return self._send_json(self.operator_server.control.get_task_claims(active_only=active_only))
            if path == "/api/controller/workspace":
                task_id = self._required_query(query, "task_id").upper()
                include_text = _bool_arg(query.get("include_text", [None])[0], default=False)
                limit = int(query.get("limit", ["100"])[0])
                return self._send_json(
                    self.operator_server.control.get_task_workspace_manifest(
                        task_id=task_id,
                        include_text=include_text,
                        limit=limit,
                    )
                )
            if path == "/api/controller/decisions":
                keyword = query.get("keyword", [None])[0]
                include_text = _bool_arg(query.get("include_text", [None])[0], default=False)
                limit = int(query.get("limit", ["5"])[0])
                return self._send_json(
                    self.operator_server.control.get_decisions(
                        keyword=keyword,
                        limit=limit,
                        include_text=include_text,
                    )
                )
            if path == "/api/controller/search":
                query_text = self._required_query(query, "query")
                category = query.get("category", [None])[0]
                limit = int(query.get("limit", ["10"])[0])
                return self._send_json(
                    self.operator_server.control.search_canonical_artifacts(
                        query=query_text,
                        limit=limit,
                        category=category,
                    )
                )
            if path == "/api/controller/provider-sessions":
                return self._send_json(self.operator_server.control.get_active_provider_sessions())
            if path == "/api/controller/run-state":
                task_id = self._required_query(query, "task_id").upper()
                return self._send_json(self.operator_server.controller.get_run_state(task_id=task_id))
            if path == "/api/controller/workflow-policy":
                task_id = self._required_query(query, "task_id").upper()
                refresh = _bool_arg(query.get("refresh", [None])[0], default=False)
                return self._send_json(self.operator_server.controller.get_workflow_policy(task_id=task_id, refresh=refresh))
            if path == "/api/controller/dashboard-summary":
                limit_tasks = int(query.get("limit_tasks", ["25"])[0])
                return self._send_json(self.operator_server.controller.get_dashboard_summary(limit_tasks=limit_tasks))
            if path == "/api/controller/notifications":
                open_only = _bool_arg(query.get("open_only", [None])[0], default=True)
                limit = int(query.get("limit", ["100"])[0])
                return self._send_json(self.operator_server.controller.get_notifications(open_only=open_only, limit=limit))
            if path == "/api/controller/improvement-advisories":
                open_only = _bool_arg(query.get("open_only", [None])[0], default=False)
                refresh = _bool_arg(query.get("refresh", [None])[0], default=False)
                high_confidence_only = _bool_arg(query.get("high_confidence_only", [None])[0], default=False)
                limit = int(query.get("limit", ["50"])[0])
                return self._send_json(
                    self.operator_server.controller.get_improvement_advisories(
                        open_only=open_only,
                        limit=limit,
                        refresh=refresh,
                        high_confidence_only=high_confidence_only,
                    )
                )
            if path == "/api/controller/daemon-status":
                return self._send_json(self.operator_server.controller.daemon_status())
            if path == "/api/controller/audit-timeline":
                task_id = self._required_query(query, "task_id").upper()
                after_id = int(query.get("after_id", ["0"])[0])
                limit = int(query.get("limit", ["200"])[0])
                return self._send_json(self.operator_server.controller.get_audit_timeline(task_id=task_id, after_id=after_id, limit=limit))
            if path == "/api/controller/hitl-queue":
                task_id = query.get("task_id", [None])[0]
                include_resolved = _bool_arg(query.get("include_resolved", [None])[0], default=False)
                limit = int(query.get("limit", ["100"])[0])
                return self._send_json(
                    self.operator_server.controller.get_hitl_queue(
                        task_id=task_id.upper() if task_id else None,
                        include_resolved=include_resolved,
                        limit=limit,
                    )
                )
            if path == "/api/controller/events":
                task_id = query.get("task_id", [None])[0]
                after_id = int(query.get("after_id", ["0"])[0])
                return self._serve_event_stream(task_id=task_id.upper() if task_id else None, after_id=after_id)
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except Exception as exc:
            self._send_error(exc)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            payload = self._read_json_body()
            if path == "/api/controller/validate":
                return self._send_json(
                    self.operator_server.control.validate_artifact(
                        schema_name=str(payload["schema_name"]),
                        artifact_path=str(payload["artifact_path"]),
                    )
                )
            if path == "/api/controller/run":
                with self.operator_server.controller_lock:
                    return self._send_json(self._run_pipeline_request(payload))
            if path == "/api/controller/dispatch":
                with self.operator_server.controller_lock:
                    return self._send_json(self._dispatch_team(payload))
            if path == "/api/controller/start-task-thread":
                return self._runtime_retired_response()
            if path == "/api/controller/start-task-turn":
                return self._runtime_retired_response()
            if path == "/api/controller/sync-task-run":
                return self._runtime_retired_response()
            if path == "/api/controller/evaluate-workflow-policy":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        {
                            "task_id": str(payload["task_id"]).upper(),
                            "workflow_policy": self.operator_server.controller.evaluate_workflow_policy(
                                task_id=str(payload["task_id"]).upper(),
                                emit_events=True,
                            ),
                        }
                    )
            if path == "/api/controller/configure-workflow-policy":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.configure_workflow_policy(
                            task_id=str(payload["task_id"]).upper(),
                            dispatch_mode=str(payload["dispatch_mode"]) if payload.get("dispatch_mode") else None,
                            auto_closeout=bool(payload["auto_closeout"]) if "auto_closeout" in payload else None,
                            monitor_enabled=bool(payload["monitor_enabled"]) if "monitor_enabled" in payload else None,
                        )
                    )
            if path == "/api/controller/recover-state":
                with self.operator_server.controller_lock:
                    return self._send_json(self.operator_server.controller.recover_state())
            if path == "/api/controller/monitor-cycle":
                with self.operator_server.controller_lock:
                    task_id = str(payload["task_id"]).upper() if payload.get("task_id") else None
                    return self._send_json(self.operator_server.controller.run_monitor_cycle(task_id=task_id))
            if path == "/api/controller/resume-task":
                return self._runtime_retired_response()
            if path == "/api/controller/start-review":
                return self._runtime_retired_response()
            if path == "/api/controller/start-adversarial-review":
                return self._runtime_retired_response()
            if path == "/api/controller/start-convergence-decision":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.start_convergence_decision(
                            task_id=str(payload["task_id"]).upper(),
                            notes=[str(item) for item in payload.get("notes", [])] or None,
                        )
                    )
            if path == "/api/controller/acknowledge-notification":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.acknowledge_notification(
                            notification_id=str(payload["notification_id"]),
                        )
                    )
            if path == "/api/controller/acknowledge-improvement-advisory":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.acknowledge_improvement_advisory(
                            advisory_id=str(payload["advisory_id"]),
                        )
                    )
            if path == "/api/controller/respond-hitl":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.respond_hitl(
                            entry_id=str(payload["entry_id"]),
                            response_payload=dict(payload.get("response_payload", {})),
                        )
                    )
            if path == "/api/controller/record-human-decision":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.record_human_decision(
                            task_id=str(payload["task_id"]).upper(),
                            operator_decision=str(payload["operator_decision"]),
                            workflow_status=str(payload["workflow_status"]) if payload.get("workflow_status") else None,
                            constraints=[str(item) for item in payload.get("constraints", [])] or None,
                            notes=[str(item) for item in payload.get("notes", [])] or None,
                        )
                    )
            if path == "/api/controller/finalize-review":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.finalize_review(
                            task_id=str(payload["task_id"]).upper(),
                            verdict=str(payload["verdict"]),
                            summary=str(payload["summary"]),
                            findings=list(payload.get("findings", [])),
                            notes=[str(item) for item in payload.get("notes", [])] or None,
                        )
                    )
            if path == "/api/controller/finalize-adversarial-review":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.finalize_adversarial_review(
                            task_id=str(payload["task_id"]).upper(),
                            verdict=str(payload["verdict"]),
                            summary=str(payload["summary"]),
                            findings=list(payload.get("findings", [])),
                            notes=[str(item) for item in payload.get("notes", [])] or None,
                        )
                    )
            if path == "/api/controller/finalize-convergence-decision":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.finalize_convergence_decision(
                            task_id=str(payload["task_id"]).upper(),
                            selected_disposition=str(payload["selected_disposition"]),
                            rationale=str(payload["rationale"]),
                            notes=[str(item) for item in payload.get("notes", [])] or None,
                        )
                    )
            if path == "/api/controller/create-claim":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.create_claim(
                            task_id=str(payload["task_id"]).upper(),
                            title=str(payload["title"]) if payload.get("title") else None,
                            platform=str(payload.get("platform", "CODEX")),
                            agent_name=str(payload["agent_name"]),
                            safe_zone_paths=[str(item) for item in payload.get("safe_zone_paths", [])] or None,
                            pipeline_type=str(payload.get("pipeline_type", "AAS")),
                            invention_ids=[str(item) for item in payload.get("invention_ids", [])] or None,
                            target_specs=[str(item) for item in payload.get("target_specs", [])] or None,
                            notes=str(payload.get("notes", "")),
                            status=str(payload.get("status", "CLAIMED")),
                        )
                    )
            if path == "/api/controller/write-handoff":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.write_handoff(
                            task_id=str(payload["task_id"]).upper(),
                            title=str(payload["title"]),
                            platform=str(payload["platform"]),
                            pipeline_verdict=str(payload["pipeline_verdict"]),
                            notes=str(payload.get("notes", "")),
                            artifacts=list(payload.get("artifacts", [])),
                            applied=bool(payload.get("applied", False)),
                        )
                    )
            if path == "/api/controller/execute-closeout":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.execute_closeout(
                            task_id=str(payload["task_id"]).upper(),
                            review=dict(payload.get("review", {})) or None,
                            human_decision=dict(payload.get("human_decision", {})) or None,
                            claim_update=dict(payload.get("claim_update", {})) or None,
                            handoff=dict(payload.get("handoff", {})) or None,
                            validate_workspace=bool(payload.get("validate_workspace", True)),
                        )
                    )
            if path == "/api/controller/daemon-start":
                with self.operator_server.controller_lock:
                    return self._send_json(
                        self.operator_server.controller.start_daemon(
                            host=str(payload.get("host", DEFAULT_OPERATOR_HOST)),
                            port=int(payload.get("port", DEFAULT_OPERATOR_PORT)),
                        )
                    )
            if path == "/api/controller/daemon-stop":
                with self.operator_server.controller_lock:
                    return self._send_json(self.operator_server.controller.stop_daemon())
            if path in {"/api/app-server/start", "/api/app-server/stop"}:
                return self._runtime_retired_response()
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except Exception as exc:
            self._send_error(exc)

    def log_message(self, format: str, *args: object) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} {format % args}")

    def _serve_ui(self) -> None:
        body = self.operator_server.ui_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_event_stream(self, *, task_id: str | None, after_id: int) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        last_id = after_id
        try:
            while True:
                events = self.operator_server.event_broker.wait_for_events(
                    after_id=last_id,
                    timeout_seconds=15.0,
                    task_id=task_id,
                )
                if not events:
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
                    continue
                for event in events:
                    last_id = max(last_id, int(event["id"]))
                    body = json.dumps(event["payload"], sort_keys=True)
                    self.wfile.write(f"id: {event['id']}\n".encode("utf-8"))
                    self.wfile.write(f"event: {event['event_type']}\n".encode("utf-8"))
                    self.wfile.write(f"data: {body}\n\n".encode("utf-8"))
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            return

    def _send_error(self, exc: Exception, status: HTTPStatus = HTTPStatus.BAD_REQUEST) -> None:
        payload = {
            "error": type(exc).__name__,
            "message": str(exc),
        }
        self._send_json(payload, status=status)

    def _runtime_retired_response(self) -> None:
        self._send_json(
            {
                "error": "RetiredControllerRuntime",
                "message": RETIRED_RUNTIME_MESSAGE,
                "runtime_bridge": self.operator_server.runtime_bridge.status(),
            },
            status=HTTPStatus.GONE,
        )

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        payload = json.loads(raw.decode("utf-8") or "{}")
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object.")
        return payload

    def _required_query(self, query: dict[str, list[str]], key: str) -> str:
        value = query.get(key, [None])[0]
        if not value:
            raise ValueError(f"Missing query parameter: {key}")
        return value

    def _run_pipeline_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        manager = InventionPipelineManager(self.operator_server.repo_root)
        task_policy = TaskIdPolicy(self.operator_server.repo_root)
        modifier = str(payload["modifier"]).strip()
        raw_task_id = payload.get("task_id")
        prompt = payload.get("prompt")
        if prompt is None and raw_task_id and not TASK_ID_RE.match(str(raw_task_id).strip().upper()):
            prompt = raw_task_id
            raw_task_id = None
        if prompt is None:
            raise ValueError("A prompt is required.")

        resolved_task_id, task_class, auto_minted = task_policy.resolve(
            modifier=modifier,
            requested_task_id=str(raw_task_id).upper() if raw_task_id else None,
            task_class=str(payload.get("task_class", "auto")),
        )
        provider = payload.get("provider")
        agent_name = payload.get("agent_name")
        session_id = payload.get("session_id")
        if provider or agent_name or session_id:
            if not (provider and agent_name and session_id):
                raise ValueError("--provider, --agent-name, and --session-id must be supplied together")
            manager.register_backend(
                provider=str(provider),
                agent_name=str(agent_name),
                session_id=str(session_id),
                agent_types=[str(item) for item in payload.get("agent_type", [])],
                current_task=resolved_task_id,
            )

        result = manager.run_command(
            modifier=modifier,
            task_id=resolved_task_id,
            prompt=str(prompt),
            operator_constraints=[str(item) for item in payload.get("constraint", [])],
        )
        self.operator_server.controller.ensure_pipeline_run_record(task_id=resolved_task_id, workflow_record=result)
        result["task_id"] = resolved_task_id
        result["task_class"] = task_class
        result["task_id_auto_minted"] = auto_minted
        if result.get("status") == "PENDING_HUMAN_REVIEW" and not bool(payload.get("json_only", False)):
            result["human_review_prompt"] = manager.render_operator_prompt(task_id=resolved_task_id)
        return result

    def _dispatch_team(self, payload: dict[str, Any]) -> dict[str, Any]:
        manager = InventionPipelineManager(self.operator_server.repo_root)
        task_id = str(payload["task_id"]).upper()
        spawn_id = str(payload["spawn_id"])
        result = manager.prepare_team_dispatch(
            task_id=task_id,
            action_label=str(payload.get("action_label", "spawn_program")),
            instruction=spawn_id,
            provider=str(payload.get("provider", "codex")),
            agent_name=payload.get("agent_name"),
            session_id=payload.get("session_id"),
            execute=bool(payload.get("execute", False)),
            dry_run=bool(payload.get("dry_run", False)),
        )
        return result


def serve_operator_http(
    *,
    repo_root: Path,
    host: str = DEFAULT_OPERATOR_HOST,
    port: int = DEFAULT_OPERATOR_PORT,
    open_browser: bool = False,
) -> int:
    ui_path = repo_root / "ui" / "operator_console.html"
    server = OperatorHttpServer(
        (host, port),
        OperatorHttpHandler,
        repo_root=repo_root,
        ui_path=ui_path,
    )
    url = f"http://{host}:{port}/"
    server.controller.run_monitor_cycle()
    print(f"Atrahasis operator service listening at {url}")
    print("Controller runtime bridge: retired")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Atrahasis operator service.")
    finally:
        server.server_close()
        server.controller.stop()
    return 0
