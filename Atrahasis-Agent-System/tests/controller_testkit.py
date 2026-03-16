from __future__ import annotations

import json
import sys
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from aas1.operator_http_service import ControllerEventBroker, OperatorHttpHandler


class FakeControlPlane:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def get_session_brief(self) -> dict[str, Any]:
        self.calls.append({"method": "get_session_brief"})
        return {
            "path": "docs/SESSION_BRIEF.md",
            "summary": "Brief summary",
            "next_dispatchable_canonical_task": "T-9002",
            "text": "brief",
        }

    def get_dispatchable_tasks(self, *, limit: int = 5) -> dict[str, Any]:
        self.calls.append({"method": "get_dispatchable_tasks", "limit": limit})
        return {
            "path": "docs/TODO.md",
            "next_dispatchable_canonical_task": "T-9002",
            "user_dispatch_order": ["T-9002"][:limit],
            "tasks": [{"task_id": "T-9002", "title": "Controller validation"}][:limit],
        }

    def get_task_status(self, *, task_id: str) -> dict[str, Any]:
        self.calls.append({"method": "get_task_status", "task_id": task_id})
        return {"task_id": task_id, "status": "PENDING_HUMAN_REVIEW"}

    def get_task_claims(self, *, active_only: bool = True) -> dict[str, Any]:
        self.calls.append({"method": "get_task_claims", "active_only": active_only})
        return {"active_only": active_only, "claim_count": 0, "claims": []}

    def get_task_workspace_manifest(
        self,
        *,
        task_id: str,
        include_text: bool = False,
        limit: int = 100,
    ) -> dict[str, Any]:
        self.calls.append(
            {
                "method": "get_task_workspace_manifest",
                "task_id": task_id,
                "include_text": include_text,
                "limit": limit,
            }
        )
        return {
            "task_id": task_id,
            "workspace_exists": True,
            "document_count": 1,
            "documents": [{"path": f"docs/task_workspaces/{task_id}/WORKFLOW_RUN_RECORD.json"}],
        }

    def get_decisions(
        self,
        *,
        keyword: str | None = None,
        limit: int = 5,
        include_text: bool = False,
    ) -> dict[str, Any]:
        self.calls.append({"method": "get_decisions", "keyword": keyword, "limit": limit, "include_text": include_text})
        return {"path": "docs/DECISIONS.md", "keyword": keyword, "decision_count": 1, "matches": []}

    def search_canonical_artifacts(
        self,
        *,
        query: str,
        limit: int = 10,
        category: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append({"method": "search_canonical_artifacts", "query": query, "limit": limit, "category": category})
        return {"query": query, "match_count": 1, "matches": [{"path": "docs/TODO.md", "category": "workflow"}]}

    def get_active_provider_sessions(self) -> dict[str, Any]:
        self.calls.append({"method": "get_active_provider_sessions"})
        return {"session_count": 1, "sessions": [{"provider": "codex", "session_id": "session-1"}]}

    def validate_artifact(self, *, schema_name: str, artifact_path: str) -> dict[str, Any]:
        self.calls.append({"method": "validate_artifact", "schema_name": schema_name, "artifact_path": artifact_path})
        return {"schema_name": schema_name, "artifact_path": artifact_path, "valid": True, "errors": []}


class FakeControllerService:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.policy_settings = {
            "dispatch_mode": "hook_only",
            "auto_closeout": False,
            "monitor_enabled": True,
        }
        self.run = {
            "run_id": "run-1",
            "thread_id": None,
            "turn_id": None,
            "review_thread_id": None,
            "status": "IDLE",
        }
        self.notifications = [
            {
                "notification_id": "note-t-9002-pending_hitl",
                "task_id": "T-9002",
                "category": "pending_hitl",
                "severity": "high",
                "summary": "T-9002 has pending HITL entries.",
                "status": "OPEN",
            }
        ]
        self.improvement_advisories = [
            {
                "advisory_id": "aas5-update-controller-reliability",
                "category": "controller_reliability_hardening",
                "severity": "major",
                "confidence": "high",
                "headline": "Controller reliability hardening is warranted.",
                "summary": "Synthetic advisory for the operator update window.",
                "status": "OPEN",
            }
        ]
        self.daemon = {
            "running": False,
            "pid": None,
            "host": "127.0.0.1",
            "port": 4180,
            "ui_url": "http://127.0.0.1:4180/operator/",
        }

    def _record(self, method: str, **payload: Any) -> None:
        self.calls.append({"method": method, **payload})

    def get_run_state(self, *, task_id: str) -> dict[str, Any]:
        self._record("get_run_state", task_id=task_id)
        return {
            "task_id": task_id,
            "run": dict(self.run),
            "workflow_policy": self.get_workflow_policy(task_id=task_id, refresh=False),
            "adversarial_review_record": None,
            "convergence_gate_record": None,
            "audit_timeline_tail": self.get_audit_timeline(task_id=task_id, limit=5)["events"],
        }

    def get_dashboard_summary(self, *, limit_tasks: int = 25) -> dict[str, Any]:
        self._record("get_dashboard_summary", limit_tasks=limit_tasks)
        return {
            "dashboard": {
                "task_count": 1,
                "active_run_count": 1,
                "terminal_run_count": 0,
                "pending_hitl_count": 1,
                "task_cards": [
                    {
                        "task_id": "T-9002",
                        "current_stage": "RESEARCH",
                        "lifecycle_status": "READY",
                        "run_status": self.run["status"],
                        "pending_hitl_count": 1,
                    }
                ][:limit_tasks],
            },
            "notifications": list(self.notifications),
            "improvement_advisories": {
                "updated_at": "2026-03-15T00:00:00Z",
                "open_count": 1,
                "acknowledged_count": 0,
                "resolved_count": 0,
                "advisories": list(self.improvement_advisories),
            },
            "runtime_bridge": {"enabled": False, "running": False, "mode": "retired", "reason": "Controller-owned App Server runtime has been retired from AAS5."},
            "daemon": dict(self.daemon),
            "provider_sessions": {"session_count": 1, "sessions": [{"provider": "codex", "session_id": "session-1"}]},
        }

    def get_notifications(self, *, open_only: bool = True, limit: int = 100) -> dict[str, Any]:
        self._record("get_notifications", open_only=open_only, limit=limit)
        notifications = list(self.notifications)
        if open_only:
            notifications = [item for item in notifications if item.get("status") == "OPEN"]
        notifications = notifications[:limit]
        return {"notification_count": len(notifications), "notifications": notifications}

    def acknowledge_notification(self, *, notification_id: str) -> dict[str, Any]:
        self._record("acknowledge_notification", notification_id=notification_id)
        for item in self.notifications:
            if item["notification_id"] == notification_id:
                item["status"] = "ACKNOWLEDGED"
        return {"notification_count": len(self.notifications), "notifications": list(self.notifications)}

    def get_improvement_advisories(
        self,
        *,
        open_only: bool = False,
        limit: int = 50,
        refresh: bool = False,
        high_confidence_only: bool = False,
    ) -> dict[str, Any]:
        self._record(
            "get_improvement_advisories",
            open_only=open_only,
            limit=limit,
            refresh=refresh,
            high_confidence_only=high_confidence_only,
        )
        advisories = list(self.improvement_advisories)
        if open_only:
            advisories = [item for item in advisories if item.get("status") == "OPEN"]
        if high_confidence_only:
            advisories = [item for item in advisories if item.get("confidence") == "high"]
        advisories = advisories[:limit]
        return {
            "updated_at": "2026-03-15T00:00:00Z",
            "open_count": len([item for item in advisories if item.get("status") == "OPEN"]),
            "acknowledged_count": len([item for item in advisories if item.get("status") == "ACKNOWLEDGED"]),
            "resolved_count": len([item for item in advisories if item.get("status") == "RESOLVED"]),
            "advisory_count": len(advisories),
            "advisories": advisories,
        }

    def acknowledge_improvement_advisory(self, *, advisory_id: str) -> dict[str, Any]:
        self._record("acknowledge_improvement_advisory", advisory_id=advisory_id)
        for item in self.improvement_advisories:
            if item["advisory_id"] == advisory_id:
                item["status"] = "ACKNOWLEDGED"
        return {
            "updated_at": "2026-03-15T00:00:00Z",
            "advisories": list(self.improvement_advisories),
        }

    def daemon_status(self) -> dict[str, Any]:
        self._record("daemon_status")
        return dict(self.daemon)

    def start_daemon(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 4180,
    ) -> dict[str, Any]:
        self._record(
            "start_daemon",
            host=host,
            port=port,
        )
        self.daemon.update(
            {
                "running": True,
                "pid": 5150,
                "host": host,
                "port": port,
                "ui_url": f"http://{host}:{port}/operator/",
            }
        )
        return dict(self.daemon)

    def stop_daemon(self) -> dict[str, Any]:
        self._record("stop_daemon")
        self.daemon["running"] = False
        self.daemon["pid"] = None
        return dict(self.daemon)

    def get_workflow_policy(self, *, task_id: str, refresh: bool = True) -> dict[str, Any]:
        self._record("get_workflow_policy", task_id=task_id, refresh=refresh)
        return {
            "task_id": task_id,
            "current_stage": "RESEARCH",
            "next_stage": "FEASIBILITY",
            "lifecycle_status": "READY",
            "settings": dict(self.policy_settings),
            "adversarial_review": {"enabled": False, "required_before_stage_close": False, "review_role": "adversarial_analyst"},
            "convergence": {"enabled": False, "required_before_stage_close": False, "status": "NOT_REQUIRED", "satisfied": True},
            "dispatch": {"dispatch_mode": self.policy_settings["dispatch_mode"], "ready": False},
            "next_actions": [{"action": "monitor_cycle"}],
            "pending_hitl_count": 1,
        }

    def get_audit_timeline(self, *, task_id: str, after_id: int = 0, limit: int = 200) -> dict[str, Any]:
        self._record("get_audit_timeline", task_id=task_id, after_id=after_id, limit=limit)
        return {
            "task_id": task_id,
            "event_count": 1,
            "events": [{"id": 1, "event_type": "thread_started", "summary": "Thread started"}][:limit],
        }

    def get_hitl_queue(
        self,
        *,
        task_id: str | None = None,
        include_resolved: bool = False,
        limit: int = 100,
    ) -> dict[str, Any]:
        self._record("get_hitl_queue", task_id=task_id, include_resolved=include_resolved, limit=limit)
        return {
            "task_id": task_id,
            "entry_count": 1,
            "entries": [{"entry_id": "hitl-1", "task_id": task_id or "T-9002", "status": "PENDING"}][:limit],
        }

    def start_task_thread(
        self,
        *,
        task_id: str,
        model: str | None = None,
        base_instructions: str | None = None,
    ) -> dict[str, Any]:
        self._record("start_task_thread", task_id=task_id, model=model, base_instructions=base_instructions)
        self.run.update({"thread_id": "thread-1", "status": "THREAD_READY"})
        return {"task_id": task_id, "run": dict(self.run), "response": {"thread": {"id": "thread-1"}}}

    def start_task_turn(
        self,
        *,
        task_id: str,
        prompt: str,
        effort: str | None = None,
        output_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._record("start_task_turn", task_id=task_id, prompt=prompt, effort=effort, output_schema=output_schema)
        self.run.update({"turn_id": "turn-1", "status": "TURN_RUNNING"})
        return {"task_id": task_id, "run": dict(self.run), "response": {"turn": {"id": "turn-1"}}}

    def sync_task_run(self, *, task_id: str) -> dict[str, Any]:
        self._record("sync_task_run", task_id=task_id)
        self.run["status"] = "TURN_COMPLETED"
        return {
            "task_id": task_id,
            "run": dict(self.run),
            "controller_run_result": {"type": "CONTROLLER_RUN_RESULT", "status": "SYNCED"},
        }

    def evaluate_workflow_policy(self, *, task_id: str, emit_events: bool = True) -> dict[str, Any]:
        self._record("evaluate_workflow_policy", task_id=task_id, emit_events=emit_events)
        policy = self.get_workflow_policy(task_id=task_id, refresh=False)
        policy["evaluated"] = True
        return policy

    def configure_workflow_policy(
        self,
        *,
        task_id: str,
        dispatch_mode: str | None = None,
        auto_closeout: bool | None = None,
        monitor_enabled: bool | None = None,
    ) -> dict[str, Any]:
        self._record(
            "configure_workflow_policy",
            task_id=task_id,
            dispatch_mode=dispatch_mode,
            auto_closeout=auto_closeout,
            monitor_enabled=monitor_enabled,
        )
        if dispatch_mode is not None:
            self.policy_settings["dispatch_mode"] = dispatch_mode
        if auto_closeout is not None:
            self.policy_settings["auto_closeout"] = auto_closeout
        if monitor_enabled is not None:
            self.policy_settings["monitor_enabled"] = monitor_enabled
        return {"task_id": task_id, "workflow_policy": self.get_workflow_policy(task_id=task_id, refresh=False)}

    def recover_state(self) -> dict[str, Any]:
        self._record("recover_state")
        return {"recovered_runs": 1, "recovered_hitl_entries": 1}

    def run_monitor_cycle(self, *, task_id: str | None = None) -> dict[str, Any]:
        self._record("run_monitor_cycle", task_id=task_id)
        return {"processed_tasks": [task_id] if task_id else ["T-9002"], "task_ids": [task_id] if task_id else ["T-9002"]}

    def resume_task(self, *, task_id: str) -> dict[str, Any]:
        self._record("resume_task", task_id=task_id)
        self.run["status"] = "THREAD_READY"
        return {"task_id": task_id, "run": dict(self.run), "response": {"thread": {"id": self.run["thread_id"] or "thread-1"}}}

    def start_review(
        self,
        *,
        task_id: str,
        instructions: str | None = None,
        delivery: str = "detached",
        review_role: str | None = None,
    ) -> dict[str, Any]:
        self._record("start_review", task_id=task_id, instructions=instructions, delivery=delivery, review_role=review_role)
        self.run.update({"review_thread_id": "review-1", "status": "REVIEW_PENDING"})
        return {"task_id": task_id, "run": dict(self.run), "response": {"reviewThreadId": "review-1"}}

    def start_adversarial_review(
        self,
        *,
        task_id: str,
        instructions: str | None = None,
        delivery: str = "detached",
    ) -> dict[str, Any]:
        self._record("start_adversarial_review", task_id=task_id, instructions=instructions, delivery=delivery)
        self.run.update({"review_thread_id": "review-adv-1", "status": "ADVERSARIAL_REVIEW_PENDING"})
        return {"task_id": task_id, "run": dict(self.run), "response": {"reviewThreadId": "review-adv-1"}}

    def start_convergence_decision(
        self,
        *,
        task_id: str,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        self._record("start_convergence_decision", task_id=task_id, notes=notes)
        return {
            "task_id": task_id,
            "run": dict(self.run),
            "convergence_gate_record": {
                "convergence_status": "READY_FOR_DECISION",
                "decision_options": ["reject", "adopt", "hybridize"],
                "notes": notes or [],
            },
        }

    def respond_hitl(self, *, entry_id: str, response_payload: dict[str, Any]) -> dict[str, Any]:
        self._record("respond_hitl", entry_id=entry_id, response_payload=response_payload)
        return {"entry_id": entry_id, "status": "RESOLVED", "response_payload": response_payload}

    def record_human_decision(
        self,
        *,
        task_id: str,
        operator_decision: str,
        workflow_status: str | None = None,
        constraints: list[str] | None = None,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        self._record("record_human_decision", task_id=task_id, operator_decision=operator_decision)
        return {
            "task_id": task_id,
            "human_decision_record": {
                "operator_decision": operator_decision,
                "workflow_status": workflow_status,
                "constraints": constraints or [],
                "notes": notes or [],
            },
        }

    def finalize_review(
        self,
        *,
        task_id: str,
        verdict: str,
        summary: str,
        findings: list[Any],
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        self._record("finalize_review", task_id=task_id, verdict=verdict, summary=summary)
        self.run["status"] = verdict
        return {
            "task_id": task_id,
            "review_gate_record": {
                "review_status": verdict,
                "summary": summary,
                "findings": findings,
                "notes": notes or [],
            },
        }

    def finalize_adversarial_review(
        self,
        *,
        task_id: str,
        verdict: str,
        summary: str,
        findings: list[Any],
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        self._record("finalize_adversarial_review", task_id=task_id, verdict=verdict, summary=summary)
        self.run["status"] = verdict
        return {
            "task_id": task_id,
            "adversarial_review_record": {
                "review_status": verdict,
                "summary": summary,
                "findings": findings,
                "notes": notes or [],
            },
        }

    def finalize_convergence_decision(
        self,
        *,
        task_id: str,
        selected_disposition: str,
        rationale: str,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        self._record(
            "finalize_convergence_decision",
            task_id=task_id,
            selected_disposition=selected_disposition,
            rationale=rationale,
            notes=notes,
        )
        return {
            "task_id": task_id,
            "convergence_gate_record": {
                "selected_disposition": selected_disposition,
                "rationale": rationale,
                "notes": notes or [],
            },
        }

    def create_claim(self, **payload: Any) -> dict[str, Any]:
        self._record("create_claim", **payload)
        return {"task_id": payload["task_id"], "claim": payload}

    def write_handoff(self, **payload: Any) -> dict[str, Any]:
        self._record("write_handoff", **payload)
        return {"task_id": payload["task_id"], "handoff": payload}

    def execute_closeout(
        self,
        *,
        task_id: str,
        review: dict[str, Any] | None = None,
        human_decision: dict[str, Any] | None = None,
        claim_update: dict[str, Any] | None = None,
        handoff: dict[str, Any] | None = None,
        validate_workspace: bool = True,
    ) -> dict[str, Any]:
        self._record("execute_closeout", task_id=task_id, validate_workspace=validate_workspace)
        self.run["status"] = "COMPLETED"
        return {
            "task_id": task_id,
            "status": "CLOSEOUT_COMPLETE",
            "validation": {"valid": validate_workspace, "errors": []},
            "review": review,
            "human_decision": human_decision,
            "claim_update": claim_update,
            "handoff": handoff,
        }

    def stop(self) -> None:
        self._record("stop")


class FakeRuntimeBridgeManager:
    def __init__(self) -> None:
        self.running = False

    def start(self, *, listen_url: str | None = None, codex_executable: str | None = None) -> dict[str, Any]:
        return self.status()

    def stop(self) -> dict[str, Any]:
        return self.status()

    def status(self) -> dict[str, Any]:
        return {
            "enabled": False,
            "running": False,
            "mode": "retired",
            "reason": "Controller-owned App Server runtime has been retired from AAS5.",
            "listen_url": None,
            "codex_executable": None,
        }

    def client_config(self) -> dict[str, Any]:
        return {
            "enabled": False,
            "mode": "retired",
            "reason": "Controller-owned App Server runtime has been retired from AAS5.",
        }


class FakeOperatorHttpServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        server_address: tuple[str, int],
        *,
        ui_path: Path,
    ) -> None:
        super().__init__(server_address, OperatorHttpHandler)
        self.repo_root = REPO_ROOT
        self.ui_path = ui_path
        self.control = FakeControlPlane()
        self.controller_lock = threading.Lock()
        self.runtime_bridge = FakeRuntimeBridgeManager()
        self.event_broker = ControllerEventBroker()
        self.controller = FakeControllerService()


@dataclass
class FakeServerHandle:
    base_url: str
    server: FakeOperatorHttpServer
    thread: threading.Thread


@contextmanager
def running_fake_operator_http_server() -> Any:
    ui_path = REPO_ROOT / "ui" / "operator_console.html"
    server = FakeOperatorHttpServer(("127.0.0.1", 0), ui_path=ui_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    handle = FakeServerHandle(
        base_url=f"http://127.0.0.1:{server.server_address[1]}",
        server=server,
        thread=thread,
    )
    try:
        yield handle
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2.0)


def http_json(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    timeout: float = 5.0,
) -> tuple[int, dict[str, Any]]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(base_url.rstrip("/") + path, data=data, method=method, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            return int(response.status), json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        try:
            return int(exc.code), json.loads(exc.read().decode("utf-8"))
        finally:
            exc.close()
