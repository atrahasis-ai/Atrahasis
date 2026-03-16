from __future__ import annotations

import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Callable

from aas1.audit_analytics import AuditAnalytics
from aas1.audit_timeline_store import AuditTimelineStore
from aas1.artifact_registry import ArtifactRegistry
from aas1.common import load_json, utc_now
from aas1.control_plane import AtrahasisControlPlane
from aas1.controller_daemon import ControllerDaemonManager
from aas1.controller_run_registry import ControllerRunRegistry, TERMINAL_STATUSES
from aas1.dispatch_merge_engine import DispatchMergeEngine
from aas1.hitl_queue_store import HitlQueueStore
from aas1.human_decision_interface import HumanDecisionInterface
from aas1.improvement_observer import ImprovementObserver
from aas1.invention_pipeline_manager import InventionPipelineManager
from aas1.notification_center import NotificationCenter
from aas1.operator_session_manager import OperatorSessionManager
from aas1.redesign_memory_store import RedesignMemoryStore
from aas1.review_template_registry import ReviewTemplateRegistry
from aas1.shared_state_closeout import SharedStateCloseoutManager
from aas1.workflow_policy_engine import WorkflowPolicyEngine
from aas1.workflow_context_store import WorkflowContextStore

RETIRED_RUNTIME_MESSAGE = (
    "Controller-owned App Server runtime has been retired from AAS5. "
    "Use direct provider sessions and task-local artifacts instead."
)


class OperatorControllerService:
    """Controller-owned orchestration across AAS runtime state and task-local artifacts."""

    def __init__(
        self,
        repo_root: Path,
        *,
        control: AtrahasisControlPlane,
        runtime_bridge: Any,
        event_callback: Callable[[dict[str, Any]], None] | None = None,
        start_monitor: bool = False,
        monitor_interval_seconds: float = 5.0,
    ) -> None:
        self.repo_root = repo_root
        self.control = control
        self.runtime_bridge = runtime_bridge
        self.registry = ArtifactRegistry(repo_root)
        self.run_registry = ControllerRunRegistry(repo_root)
        self.hitl_queue = HitlQueueStore(repo_root)
        self.operator_sessions = OperatorSessionManager(repo_root)
        self.workflow_context = WorkflowContextStore(repo_root)
        self.audit_timeline = AuditTimelineStore(repo_root)
        self.workflow_policy = WorkflowPolicyEngine(repo_root)
        self.merge_engine = DispatchMergeEngine(repo_root, artifact_registry=self.registry)
        self.shared_closeout = SharedStateCloseoutManager(repo_root)
        self.analytics = AuditAnalytics(repo_root)
        self.notifications = NotificationCenter(repo_root)
        self.improvement_observer = ImprovementObserver(repo_root)
        self.daemon = ControllerDaemonManager(repo_root)
        self.review_templates = ReviewTemplateRegistry(repo_root)
        self.human_decision = HumanDecisionInterface()
        self.redesign_memory = RedesignMemoryStore(repo_root)
        self._event_callback = event_callback
        self._monitor_interval_seconds = max(1.0, monitor_interval_seconds)
        self._monitor_stop = threading.Event()
        self._monitor_thread: threading.Thread | None = None
        if start_monitor:
            self.start_monitor()

    def stop(self) -> None:
        self.stop_monitor()

    def start_monitor(self) -> None:
        if self._monitor_thread is not None and self._monitor_thread.is_alive():
            return
        self._monitor_stop.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True, name="atrahasis-controller-monitor")
        self._monitor_thread.start()

    def stop_monitor(self) -> None:
        self._monitor_stop.set()
        thread = self._monitor_thread
        if thread is not None and thread.is_alive():
            thread.join(timeout=1.0)
        self._monitor_thread = None

    def get_run_state(self, *, task_id: str) -> dict[str, Any]:
        task_root = self.registry.task_root(task_id)
        workflow_policy = self.evaluate_workflow_policy(task_id=task_id, emit_events=False)
        workflow_context = self.control.get_latest_workflow_context(task_id=task_id)
        task_improvement_report = self._load_optional_json(task_root / "TASK_IMPROVEMENT_REPORT.json")
        radical_redesign_report = self._load_optional_json(task_root / "RADICAL_REDESIGN_REPORT.json")
        convergence_gate_record = self._load_optional_json(task_root / "CONVERGENCE_GATE_RECORD.json")
        human_decision_record = self._load_optional_json(task_root / "HUMAN_DECISION_RECORD.json")
        return {
            "task_id": task_id,
            "run": self.run_registry.load_latest(task_id),
            "workflow_context": workflow_context,
            "controller_run_result": self._load_optional_json(task_root / "CONTROLLER_RUN_RESULT.json"),
            "review_gate_record": self._load_optional_json(task_root / "REVIEW_GATE_RECORD.json"),
            "adversarial_review_record": self._load_optional_json(task_root / "ADVERSARIAL_REVIEW_RECORD.json"),
            "convergence_gate_record": convergence_gate_record,
            "closeout_execution_record": self._load_optional_json(task_root / "CLOSEOUT_EXECUTION_RECORD.json"),
            "stage_contract_report": self._load_optional_json(task_root / "STAGE_CONTRACT_REPORT.json"),
            "child_result_merge_package": self._load_optional_json(task_root / "CHILD_RESULT_MERGE_PACKAGE.json"),
            "future_branch_report": self._load_optional_json(task_root / "FUTURE_BRANCH_REPORT.json"),
            "future_convergence_report": self._load_optional_json(task_root / "FUTURE_CONVERGENCE_REPORT.json"),
            "task_improvement_report": task_improvement_report,
            "radical_redesign_report": radical_redesign_report,
            "operator_option_set": self.human_decision.synthesize_operator_options(
                human_record=human_decision_record or {},
                task_improvement_report=task_improvement_report,
                radical_redesign_report=radical_redesign_report,
                convergence_gate_record=convergence_gate_record,
            ),
            "redesign_memory": self.workflow_policy.redesign_memory_state(
                self.redesign_memory.snapshot_for_task(
                    task_id=task_id,
                    workflow_context=workflow_context,
                    workflow_policy=workflow_policy,
                    human_decision_record=human_decision_record,
                )
            ),
            "shared_state_closeout_record": self._load_optional_json(task_root / "SHARED_STATE_CLOSEOUT_RECORD.json"),
            "claim": self.control.task_claims.load_claim(task_id),
            "pending_hitl_count": len(self.hitl_queue.list_entries(task_id=task_id, include_resolved=False, limit=500)),
            "workflow_policy": workflow_policy,
            "audit_timeline_tail": self.audit_timeline.list_events(task_id=task_id, limit=50),
            "notifications": [item for item in self.notifications.list_notifications(limit=200) if item.get("task_id") == task_id],
        }

    def get_hitl_queue(
        self,
        *,
        task_id: str | None = None,
        include_resolved: bool = False,
        limit: int = 100,
    ) -> dict[str, Any]:
        entries = self.hitl_queue.list_entries(task_id=task_id, include_resolved=include_resolved, limit=limit)
        return {"task_id": task_id, "entry_count": len(entries), "entries": entries}

    def get_workflow_policy(self, *, task_id: str, refresh: bool = True) -> dict[str, Any]:
        return self.evaluate_workflow_policy(task_id=task_id, emit_events=refresh)

    def configure_workflow_policy(
        self,
        *,
        task_id: str,
        dispatch_mode: str | None = None,
        auto_closeout: bool | None = None,
        monitor_enabled: bool | None = None,
    ) -> dict[str, Any]:
        state = self.workflow_policy.update_settings(
            task_id=task_id,
            dispatch_mode=dispatch_mode,
            auto_closeout=auto_closeout,
            monitor_enabled=monitor_enabled,
        )
        self._record_timeline(
            task_id=task_id,
            event_type="workflow_policy_configured",
            summary="Workflow policy settings updated.",
            payload={"dispatch_mode": dispatch_mode, "auto_closeout": auto_closeout, "monitor_enabled": monitor_enabled},
        )
        payload = {"task_id": task_id, "workflow_policy": state}
        self._emit_event("workflow_policy_changed", payload)
        return payload

    def get_audit_timeline(self, *, task_id: str, after_id: int = 0, limit: int = 200) -> dict[str, Any]:
        events = self.audit_timeline.list_events(task_id=task_id, after_id=after_id, limit=limit)
        return {"task_id": task_id, "event_count": len(events), "events": events}

    def get_dashboard_summary(self, *, limit_tasks: int = 25) -> dict[str, Any]:
        advisories = self.improvement_observer.load()
        return {
            "dashboard": self.analytics.summary(limit_tasks=limit_tasks),
            "notifications": self.notifications.list_notifications(limit=100),
            "improvement_advisories": advisories,
            "runtime_bridge": self.runtime_bridge.status(),
            "daemon": self.daemon.status(),
            "provider_sessions": self.control.get_active_provider_sessions(),
        }

    def get_notifications(self, *, open_only: bool = True, limit: int = 100) -> dict[str, Any]:
        items = self.notifications.list_notifications(open_only=open_only, limit=limit)
        return {"notification_count": len(items), "notifications": items}

    def acknowledge_notification(self, *, notification_id: str) -> dict[str, Any]:
        payload = self.notifications.acknowledge(notification_id=notification_id)
        self._emit_event("notifications_changed", {"notifications": self.notifications.list_notifications(limit=100)})
        return payload

    def get_improvement_advisories(
        self,
        *,
        open_only: bool = False,
        limit: int = 50,
        refresh: bool = False,
        high_confidence_only: bool = False,
    ) -> dict[str, Any]:
        payload = self._sync_improvement_advisories(emit_events=False) if refresh else self.improvement_observer.load()
        advisories = self.improvement_observer.list_advisories(
            open_only=open_only,
            limit=limit,
            high_confidence_only=high_confidence_only,
        )
        return {
            "updated_at": payload.get("updated_at"),
            "open_count": payload.get("open_count", 0),
            "acknowledged_count": payload.get("acknowledged_count", 0),
            "resolved_count": payload.get("resolved_count", 0),
            "advisory_count": len(advisories),
            "advisories": advisories,
        }

    def acknowledge_improvement_advisory(self, *, advisory_id: str) -> dict[str, Any]:
        payload = self.improvement_observer.acknowledge(advisory_id=advisory_id)
        self._emit_event(
            "improvement_advisories_changed",
            {
                "updated_at": payload.get("updated_at"),
                "open_count": len([item for item in payload.get("advisories", []) if item.get("status") == "OPEN"]),
                "advisories": payload.get("advisories", []),
            },
        )
        return payload

    def daemon_status(self) -> dict[str, Any]:
        return self.daemon.status()

    def start_daemon(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 4180,
    ) -> dict[str, Any]:
        return self.daemon.start(
            host=host,
            port=port,
        )

    def stop_daemon(self) -> dict[str, Any]:
        return self.daemon.stop()

    def start_task_thread(
        self,
        *,
        task_id: str,
        model: str | None = None,
        base_instructions: str | None = None,
    ) -> dict[str, Any]:
        raise RuntimeError(RETIRED_RUNTIME_MESSAGE)

    def start_task_turn(
        self,
        *,
        task_id: str,
        prompt: str,
        effort: str | None = None,
        output_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raise RuntimeError(RETIRED_RUNTIME_MESSAGE)

    def resume_task(self, *, task_id: str) -> dict[str, Any]:
        raise RuntimeError(RETIRED_RUNTIME_MESSAGE)

    def start_review(
        self,
        *,
        task_id: str,
        instructions: str | None = None,
        delivery: str = "detached",
        review_role: str | None = None,
    ) -> dict[str, Any]:
        raise RuntimeError(RETIRED_RUNTIME_MESSAGE)

    def start_adversarial_review(
        self,
        *,
        task_id: str,
        instructions: str | None = None,
        delivery: str = "detached",
    ) -> dict[str, Any]:
        raise RuntimeError(RETIRED_RUNTIME_MESSAGE)

    def start_convergence_decision(
        self,
        *,
        task_id: str,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        run = self._require_or_create_run(task_id=task_id, auto_thread=False)
        policy_state = self.evaluate_workflow_policy(task_id=task_id, emit_events=False)
        convergence = dict(policy_state.get("convergence") or {})
        if not convergence.get("required_before_stage_close"):
            raise ValueError(f"No convergence gate is currently required for {task_id}.")
        record = self._write_convergence_gate_record(
            task_id=task_id,
            run=run,
            selected_disposition=None,
            rationale=None,
            completed_at=None,
            notes=notes,
        )
        queue_entry = self._ensure_controller_hitl_entry(
            task_id=task_id,
            run_id=run.get("run_id"),
            category="convergence_gate",
            summary="Convergence decision is required before the current stage can close.",
            artifact_refs={
                "workflow_policy": f"runtime/state/workflow_policy/{task_id}/latest.json",
                "convergence_gate_record": record["path"],
                "future_convergence_report": f"docs/task_workspaces/{task_id}/FUTURE_CONVERGENCE_REPORT.json",
                "task_improvement_report": f"docs/task_workspaces/{task_id}/TASK_IMPROVEMENT_REPORT.json",
                "radical_redesign_report": f"docs/task_workspaces/{task_id}/RADICAL_REDESIGN_REPORT.json",
            },
            metadata={
                "current_stage": convergence.get("current_stage"),
                "recommended_parent_action": convergence.get("recommended_parent_action"),
                "decision_options": list(convergence.get("decision_options", [])),
            },
        )
        updated_run = self.run_registry.update_status(
            task_id=task_id,
            run_id=run["run_id"],
            status=str(run.get("status") or "CONVERGENCE_PENDING"),
            artifact_updates={"convergence_gate_record": record["path"]},
        )
        self.run_registry.append_event(
            task_id=task_id,
            run_id=run["run_id"],
            event_type="convergence_decision_started",
            payload={"record_ref": record["path"]},
        )
        payload = {
            "task_id": task_id,
            "run": updated_run,
            "convergence_gate_record": record["payload"],
            "queue_entry": queue_entry,
        }
        self._record_timeline(
            task_id=task_id,
            event_type="convergence_decision_started",
            summary="Controller opened a convergence decision gate.",
            payload={"run_id": run["run_id"], "record_ref": record["path"]},
        )
        self.evaluate_workflow_policy(task_id=task_id, emit_events=True)
        self._emit_event("convergence_gate_changed", payload)
        self._emit_event("hitl_queue_changed", self.get_hitl_queue(task_id=task_id, include_resolved=False))
        return payload

    def finalize_review(
        self,
        *,
        task_id: str,
        verdict: str,
        summary: str,
        findings: list[dict[str, Any]] | None = None,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        return self._finalize_review_flow(
            task_id=task_id,
            verdict=verdict,
            summary=summary,
            findings=findings,
            notes=notes,
            record_kind="review_gate",
        )

    def finalize_adversarial_review(
        self,
        *,
        task_id: str,
        verdict: str,
        summary: str,
        findings: list[dict[str, Any]] | None = None,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        return self._finalize_review_flow(
            task_id=task_id,
            verdict=verdict,
            summary=summary,
            findings=findings,
            notes=notes,
            record_kind="adversarial_review",
        )

    def finalize_convergence_decision(
        self,
        *,
        task_id: str,
        selected_disposition: str,
        rationale: str,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        run = self._require_or_create_run(task_id=task_id, auto_thread=False)
        record = self._write_convergence_gate_record(
            task_id=task_id,
            run=run,
            selected_disposition=selected_disposition,
            rationale=rationale,
            completed_at=utc_now(),
            notes=notes,
        )
        updated_run = self.run_registry.update_status(
            task_id=task_id,
            run_id=run["run_id"],
            status=str(run.get("status") or "IDLE"),
            artifact_updates={"convergence_gate_record": record["path"]},
        )
        self.run_registry.append_event(
            task_id=task_id,
            run_id=run["run_id"],
            event_type="convergence_decision_finalized",
            payload={"selected_disposition": selected_disposition},
        )
        for entry in self.hitl_queue.list_entries(task_id=task_id, include_resolved=False, limit=100):
            if entry.get("source") == "controller" and entry.get("category") == "convergence_gate":
                self.hitl_queue.resolve_entry(
                    entry_id=entry["entry_id"],
                    response_payload={
                        "selected_disposition": selected_disposition,
                        "rationale": rationale,
                    },
                )
        payload = {
            "task_id": task_id,
            "run": updated_run,
            "convergence_gate_record": record["payload"],
        }
        self._record_timeline(
            task_id=task_id,
            event_type="convergence_decision_finalized",
            summary=f"Convergence decision finalized as {selected_disposition}.",
            payload={"run_id": run["run_id"], "selected_disposition": selected_disposition},
        )
        self.evaluate_workflow_policy(task_id=task_id, emit_events=True)
        self._emit_event("convergence_gate_changed", payload)
        self._emit_event("hitl_queue_changed", self.get_hitl_queue(task_id=task_id, include_resolved=False))
        self._emit_event("run_state_changed", payload)
        return payload

    def _finalize_review_flow(
        self,
        *,
        task_id: str,
        verdict: str,
        summary: str,
        findings: list[dict[str, Any]] | None,
        notes: list[str] | None,
        record_kind: str,
    ) -> dict[str, Any]:
        run = self._require_or_create_run(task_id=task_id, auto_thread=False)
        status = self._review_status_from_verdict(verdict)
        spec = self._review_record_spec(record_kind)
        policy_state = self.workflow_policy.load(task_id) or self.get_workflow_policy(task_id=task_id, refresh=False)
        adversarial_policy = dict((policy_state.get("adversarial_review") or {})) if record_kind == "adversarial_review" else None
        review_payload = self._write_review_record(
            task_id=task_id,
            run=run,
            record_kind=record_kind,
            review_status=status,
            review_thread_id=run.get("review_thread_id"),
            review_target=None,
            review_delivery=None,
            custom_instructions=None,
            review_response=None,
            findings=findings or [],
            verdict=verdict,
            summary=summary,
            completed_at=utc_now(),
            notes=notes,
            adversarial_policy=adversarial_policy,
        )
        updated_run = self.run_registry.update_status(
            task_id=task_id,
            run_id=run["run_id"],
            status=status,
            artifact_updates={spec["artifact_key"]: review_payload["path"]},
            metadata_updates={"active_review_kind": record_kind},
        )
        self.run_registry.append_event(task_id=task_id, run_id=run["run_id"], event_type=spec["timeline_finalized_event"], payload={"verdict": verdict, "status": status})
        for entry in self.hitl_queue.list_entries(task_id=task_id, include_resolved=False, limit=100):
            if entry.get("category") == spec["queue_category"] and entry.get("run_id") == run["run_id"]:
                self.hitl_queue.resolve_entry(entry_id=entry["entry_id"], response_payload={"verdict": verdict, "summary": summary})
        self._propagate_status(
            task_id=task_id,
            workflow_status=self._review_workflow_status(record_kind=record_kind, review_status=status),
            artifact_updates={spec["artifact_key"]: review_payload["path"]},
        )
        payload = {"task_id": task_id, "run": updated_run, spec["artifact_key"]: review_payload["payload"]}
        self._record_timeline(
            task_id=task_id,
            event_type=spec["timeline_finalized_event"],
            summary=spec["timeline_finalized_summary"].format(verdict=verdict),
            payload={"run_id": run["run_id"], "verdict": verdict, "status": status},
        )
        self.evaluate_workflow_policy(task_id=task_id, emit_events=True)
        self._emit_event(spec["event_name"], payload)
        self._emit_event("hitl_queue_changed", self.get_hitl_queue(task_id=task_id, include_resolved=False))
        return payload

    def respond_hitl(self, *, entry_id: str, response_payload: dict[str, Any]) -> dict[str, Any]:
        entry = self.hitl_queue.load_entry(entry_id)
        request_id = entry.get("request_id")
        if request_id is not None:
            response_payload = dict(response_payload)
            response_payload.setdefault("runtime_bridge_retired", True)
            response_payload.setdefault("note", RETIRED_RUNTIME_MESSAGE)
        resolved = self.hitl_queue.resolve_entry(entry_id=entry_id, response_payload=response_payload)
        task_id = resolved.get("task_id")
        run_id = resolved.get("run_id")
        if task_id and run_id:
            self.run_registry.append_event(task_id=task_id, run_id=run_id, event_type="hitl_resolved", payload={"entry_id": entry_id, "category": resolved.get("category")})
            self._record_timeline(task_id=task_id, event_type="hitl_resolved", summary=f"HITL entry {entry_id} resolved.", payload={"entry_id": entry_id, "category": resolved.get("category")})
            self.evaluate_workflow_policy(task_id=task_id, emit_events=True)
            self._emit_event("run_state_changed", {"task_id": task_id, "run": self.run_registry.load_latest(task_id)})
            self._emit_event("hitl_queue_changed", self.get_hitl_queue(task_id=task_id, include_resolved=False))
        return resolved

    def record_human_decision(
        self,
        *,
        task_id: str,
        operator_decision: str,
        workflow_status: str | None = None,
        constraints: list[str] | None = None,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        payload = self.control.record_human_decision(
            task_id=task_id,
            operator_decision=operator_decision,
            workflow_status=workflow_status,
            constraints=constraints,
            notes=notes,
        )
        latest = self.run_registry.load_latest(task_id)
        if latest is not None:
            self.run_registry.update_status(task_id=task_id, run_id=latest["run_id"], status=workflow_status or latest.get("status", "PENDING_HUMAN_REVIEW"))
            self.run_registry.append_event(task_id=task_id, run_id=latest["run_id"], event_type="human_decision_recorded", payload={"operator_decision": operator_decision, "workflow_status": workflow_status})
        self._record_timeline(task_id=task_id, event_type="human_decision_recorded", summary=f"Operator decision recorded: {operator_decision}.", payload={"workflow_status": workflow_status, "constraints": constraints, "notes": notes})
        self.evaluate_workflow_policy(task_id=task_id, emit_events=True)
        self._emit_event("run_state_changed", {"task_id": task_id, "run": self.run_registry.load_latest(task_id)})
        return payload

    def create_claim(self, **kwargs: Any) -> dict[str, Any]:
        payload = self.control.create_claim(**kwargs)
        self._record_timeline(task_id=kwargs.get("task_id"), event_type="claim_created", summary="Controller created a task claim.", payload={"claim_path": payload.get("claim_path")})
        if kwargs.get("task_id"):
            self.evaluate_workflow_policy(task_id=str(kwargs["task_id"]), emit_events=True)
        self._emit_event("run_state_changed", {"task_id": kwargs.get("task_id"), "claim": payload.get("claim")})
        return payload

    def write_handoff(self, **kwargs: Any) -> dict[str, Any]:
        payload = self.control.write_handoff(**kwargs)
        self._record_timeline(task_id=kwargs.get("task_id"), event_type="handoff_written", summary="Controller wrote a handoff artifact.", payload={"handoff_path": payload.get("handoff_path")})
        if kwargs.get("task_id"):
            self.evaluate_workflow_policy(task_id=str(kwargs["task_id"]), emit_events=True)
        self._emit_event("run_state_changed", {"task_id": kwargs.get("task_id"), "handoff_path": payload.get("handoff_path")})
        return payload

    def ensure_pipeline_run_record(self, *, task_id: str, workflow_record: dict[str, Any]) -> dict[str, Any]:
        run = self.run_registry.ensure_run(
            task_id=task_id,
            workflow_id=workflow_record.get("workflow_id"),
            status=workflow_record.get("status", "PENDING_HUMAN_REVIEW"),
            legacy_runtime_url=None,
        )
        run = self.run_registry.update_status(
            task_id=task_id,
            run_id=run["run_id"],
            status=workflow_record.get("status", "PENDING_HUMAN_REVIEW"),
            artifact_updates={"workflow_run_record": workflow_record.get("artifacts", {}).get("workflow_run_record")},
            metadata_updates={"pipeline_run": workflow_record},
        )
        self.run_registry.append_event(task_id=task_id, run_id=run["run_id"], event_type="pipeline_run_recorded", payload={"workflow_id": workflow_record.get("workflow_id"), "status": workflow_record.get("status")})
        self._record_timeline(task_id=task_id, event_type="pipeline_run_recorded", summary="Pipeline run record captured in the controller.", payload={"workflow_id": workflow_record.get("workflow_id"), "status": workflow_record.get("status")})
        self.evaluate_workflow_policy(task_id=task_id, emit_events=True)
        self._emit_event("run_state_changed", {"task_id": task_id, "run": run})
        return run

    def sync_task_run(self, *, task_id: str) -> dict[str, Any]:
        run = self._require_or_create_run(task_id=task_id, auto_thread=False)
        if not run.get("thread_id") and not run.get("review_thread_id"):
            return {"task_id": task_id, "run": run, "synced": False, "reason": "No bound thread or review thread."}
        updated_run = self.run_registry.update_status(
            task_id=task_id,
            run_id=run["run_id"],
            status=str(run.get("status") or "IDLE"),
            metadata_updates={"last_sync": {"synced_at": utc_now(), "synced": False, "reason": RETIRED_RUNTIME_MESSAGE}},
        )
        self.run_registry.append_event(
            task_id=task_id,
            run_id=run["run_id"],
            event_type="runtime_sync_skipped",
            payload={"reason": RETIRED_RUNTIME_MESSAGE},
        )
        payload = {
            "task_id": task_id,
            "run": updated_run,
            "synced": False,
            "reason": RETIRED_RUNTIME_MESSAGE,
        }
        self._record_timeline(
            task_id=task_id,
            event_type="runtime_sync_skipped",
            summary="Controller skipped legacy runtime sync because the App Server bridge is retired.",
            payload={"run_status": updated_run.get("status")},
        )
        self._emit_event("run_state_changed", payload)
        return payload

    def recover_state(self) -> dict[str, Any]:
        stale_hitl_entry_ids = []
        for entry in self.hitl_queue.list_entries(include_resolved=False, limit=500):
            if entry.get("source") in {"app_server", "runtime_bridge"} and entry.get("request_id"):
                stale_hitl_entry_ids.append(entry["entry_id"])
                self.hitl_queue.update_entry(
                    entry_id=entry["entry_id"],
                    summary=f"{entry.get('summary', 'Pending legacy runtime request')} (runtime retired)",
                    metadata={"recovered_at": utc_now(), "recovery_state": "RUNTIME_BRIDGE_RETIRED"},
                )
        payload = {
            "recovered_run_count": 0,
            "recovered_runs": [],
            "stale_hitl_entry_ids": stale_hitl_entry_ids,
            "error_count": 0,
            "errors": [],
            "runtime_bridge_retired": True,
            "reason": RETIRED_RUNTIME_MESSAGE,
            "notifications": self.notifications.list_notifications(limit=100),
        }
        self._emit_event("recovery_completed", payload)
        return payload

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
        run = self._require_or_create_run(task_id=task_id, auto_thread=False)
        task_root = self.registry.task_root(task_id)
        existing_review = self._load_optional_json(task_root / "REVIEW_GATE_RECORD.json") or {}
        existing_decision = self._load_optional_json(task_root / "HUMAN_DECISION_RECORD.json") or {}
        existing_claim = self.control.task_claims.load_claim(task_id)
        artifacts: dict[str, str] = {}
        review_result = None
        if review and review.get("verdict") and review.get("summary"):
            review_result = self.finalize_review(
                task_id=task_id,
                verdict=str(review["verdict"]),
                summary=str(review["summary"]),
                findings=list(review.get("findings", [])),
                notes=[str(item) for item in review.get("notes", [])] or None,
            )
            artifacts["review_gate_record"] = f"docs/task_workspaces/{task_id}/REVIEW_GATE_RECORD.json"
        decision_result = None
        if human_decision and human_decision.get("operator_decision"):
            decision_result = self.record_human_decision(
                task_id=task_id,
                operator_decision=str(human_decision["operator_decision"]),
                workflow_status=str(human_decision["workflow_status"]) if human_decision.get("workflow_status") else None,
                constraints=[str(item) for item in human_decision.get("constraints", [])] or None,
                notes=[str(item) for item in human_decision.get("notes", [])] or None,
            )
            artifacts["human_decision_record"] = f"docs/task_workspaces/{task_id}/HUMAN_DECISION_RECORD.json"
        claim_result = None
        if claim_update and claim_update.get("status"):
            claim_payload = self.control.task_claims.update_status(
                task_id=task_id,
                status=str(claim_update["status"]),
                notes=str(claim_update.get("notes")) if claim_update.get("notes") is not None else None,
            )
            claim_result = {"task_id": task_id, "claim_path": f"docs/task_claims/{task_id}.yaml", "claim": claim_payload}
        handoff_result = None
        if handoff and handoff.get("title") and handoff.get("platform") and handoff.get("pipeline_verdict"):
            handoff_result = self.write_handoff(
                task_id=task_id,
                title=str(handoff["title"]),
                platform=str(handoff["platform"]),
                pipeline_verdict=str(handoff["pipeline_verdict"]),
                notes=str(handoff.get("notes", "")),
                artifacts=list(handoff.get("artifacts", [])) or self._default_handoff_artifacts(task_id=task_id),
                applied=bool(handoff.get("applied", False)),
            )
            artifacts["handoff"] = handoff_result["handoff_path"]
        validation = self._validate_workspace(task_id=task_id) if validate_workspace else {"valid": True, "exit_code": 0, "output": ""}
        resolved_review = review or {
            "verdict": existing_review.get("verdict"),
            "summary": existing_review.get("summary"),
            "notes": existing_review.get("notes", []),
        }
        resolved_decision = human_decision or {
            "operator_decision": existing_decision.get("operator_decision"),
            "workflow_status": existing_decision.get("workflow_status"),
            "notes": existing_decision.get("controller_notes", []),
        }
        resolved_workflow_status = str((resolved_decision or {}).get("workflow_status") or run.get("status") or "COMPLETED")
        closeout_workflow_status = "COMPLETED" if validation.get("valid") else resolved_workflow_status
        shared_state_closeout = None
        if validation.get("valid"):
            if claim_result is None and existing_claim and existing_claim.get("status") in {"CLAIMED", "IN_PROGRESS"}:
                claim_payload = self.control.task_claims.update_status(
                    task_id=task_id,
                    status="DONE",
                    notes=str((claim_update or {}).get("notes") or "Closed automatically by controller closeout."),
                )
                claim_result = {"task_id": task_id, "claim_path": f"docs/task_claims/{task_id}.yaml", "claim": claim_payload}
            shared_state_closeout = self.shared_closeout.apply(
                task_id=task_id,
                task_title=self._resolve_task_title(task_id=task_id),
                workflow_status=closeout_workflow_status,
                operator_decision=str((resolved_decision or {}).get("operator_decision")) if (resolved_decision or {}).get("operator_decision") else None,
                invention_ids=list((claim_result or {}).get("claim", {}).get("invention_ids", []) or (existing_claim or {}).get("invention_ids", []) or []),
                notes=[str(item) for item in (resolved_decision or {}).get("notes", [])],
                actor="Controller",
            )
            shared_state_closeout["agent_state_validation"] = self._validate_agent_state()
            self.registry.write_json_artifact(
                task_id,
                "SHARED_STATE_CLOSEOUT_RECORD.json",
                shared_state_closeout,
                schema_name="shared_state_closeout_record",
            )
            artifacts["shared_state_closeout_record"] = f"docs/task_workspaces/{task_id}/SHARED_STATE_CLOSEOUT_RECORD.json"
        record_payload = {
            "type": "CLOSEOUT_EXECUTION_RECORD",
            "task_id": task_id,
            "workflow_id": run.get("workflow_id"),
            "run_id": run["run_id"],
            "executed_at": utc_now(),
            "review_verdict": (resolved_review or {}).get("verdict"),
            "review_summary": (resolved_review or {}).get("summary"),
            "human_decision": (resolved_decision or {}).get("operator_decision"),
            "workflow_status": closeout_workflow_status,
            "claim_status": (claim_update or {}).get("status"),
            "handoff_path": (handoff_result or {}).get("handoff_path"),
            "validation": validation,
            "artifact_refs": dict(artifacts),
            "source": "operator_controller_service",
            "notes": [str(item) for item in (resolved_review or {}).get("notes", [])] + [str(item) for item in (resolved_decision or {}).get("notes", [])],
        }
        self.registry.write_json_artifact(task_id, "CLOSEOUT_EXECUTION_RECORD.json", record_payload, schema_name="closeout_execution_record")
        artifacts["closeout_execution_record"] = f"docs/task_workspaces/{task_id}/CLOSEOUT_EXECUTION_RECORD.json"
        final_status = "CLOSEOUT_COMPLETE"
        if not validation.get("valid"):
            final_status = "CLOSEOUT_VALIDATION_FAILED"
        updated_run = self.run_registry.update_status(
            task_id=task_id,
            run_id=run["run_id"],
            status=final_status,
            artifact_updates=artifacts,
            metadata_updates={"shared_state_closeout": shared_state_closeout},
        )
        self.run_registry.append_event(task_id=task_id, run_id=run["run_id"], event_type="closeout_executed", payload={"validation_valid": validation.get("valid", False), "status": final_status})
        payload = {
            "task_id": task_id,
            "status": final_status,
            "run": updated_run,
            "review_result": review_result,
            "human_decision_result": decision_result,
            "claim_result": claim_result,
            "handoff_result": handoff_result,
            "validation": validation,
            "closeout_execution_record": record_payload,
            "shared_state_closeout_record": shared_state_closeout,
        }
        self._record_timeline(task_id=task_id, event_type="closeout_executed", summary=f"Controller executed closeout with status {final_status}.", payload={"validation": validation, "artifacts": artifacts})
        policy_state = self.evaluate_workflow_policy(task_id=task_id, emit_events=True)
        self._sync_notifications(task_id=task_id, workflow_policy=policy_state, run_status=final_status)
        self._emit_event("closeout_completed", payload)
        self._emit_event("run_state_changed", payload)
        return payload

    def evaluate_workflow_policy(self, *, task_id: str, emit_events: bool = True) -> dict[str, Any]:
        task_root = self.registry.task_root(task_id)
        previous = self.workflow_policy.load(task_id)
        workflow_context = self.control.get_latest_workflow_context(task_id=task_id)
        review_gate_record = self._load_optional_json(task_root / "REVIEW_GATE_RECORD.json")
        adversarial_review_record = self._load_optional_json(task_root / "ADVERSARIAL_REVIEW_RECORD.json")
        future_convergence_report = self._load_optional_json(task_root / "FUTURE_CONVERGENCE_REPORT.json")
        task_improvement_report = self._load_optional_json(task_root / "TASK_IMPROVEMENT_REPORT.json")
        radical_redesign_report = self._load_optional_json(task_root / "RADICAL_REDESIGN_REPORT.json")
        convergence_gate_record = self._load_optional_json(task_root / "CONVERGENCE_GATE_RECORD.json")
        human_decision_record = self._load_optional_json(task_root / "HUMAN_DECISION_RECORD.json")
        closeout_execution_record = self._load_optional_json(task_root / "CLOSEOUT_EXECUTION_RECORD.json")
        controller_run_result = self._load_optional_json(task_root / "CONTROLLER_RUN_RESULT.json")
        state = self.workflow_policy.evaluate(
            task_id=task_id,
            workflow_context=workflow_context,
            run=self.run_registry.load_latest(task_id),
            review_gate_record=review_gate_record,
            adversarial_review_record=adversarial_review_record,
            future_convergence_report=future_convergence_report,
            task_improvement_report=task_improvement_report,
            radical_redesign_report=radical_redesign_report,
            convergence_gate_record=convergence_gate_record,
            human_decision_record=human_decision_record,
            closeout_execution_record=closeout_execution_record,
            controller_run_result=controller_run_result,
            claim=self.control.task_claims.load_claim(task_id),
            pending_hitl_count=len(self.hitl_queue.list_entries(task_id=task_id, include_resolved=False, limit=500)),
        )
        redesign_update = self.redesign_memory.ingest_task(
            task_id=task_id,
            workflow_context=workflow_context,
            workflow_policy=state,
            human_decision_record=human_decision_record,
            future_convergence_report=future_convergence_report,
            task_improvement_report=task_improvement_report,
            radical_redesign_report=radical_redesign_report,
            convergence_gate_record=convergence_gate_record,
            adversarial_review_record=adversarial_review_record,
            closeout_execution_record=closeout_execution_record,
        )
        redesign_snapshot = self.redesign_memory.snapshot_for_task(
            task_id=task_id,
            workflow_context=workflow_context,
            workflow_policy=state,
            human_decision_record=human_decision_record,
        )
        state["redesign_memory"] = self.workflow_policy.redesign_memory_state(redesign_snapshot)
        self.workflow_policy._write(task_id=task_id, payload=state)
        self._ensure_policy_queue_entries(task_id=task_id, policy_state=state)
        refreshed_pending = len(self.hitl_queue.list_entries(task_id=task_id, include_resolved=False, limit=500))
        if refreshed_pending != state.get("pending_hitl_count"):
            state["pending_hitl_count"] = refreshed_pending
            if refreshed_pending > 0:
                state["gate_state"] = "HITL_PENDING"
                if not any(item.get("action") == "resolve_hitl" for item in state.get("next_actions", [])):
                    state.setdefault("next_actions", []).insert(
                        0,
                        {
                            "action": "resolve_hitl",
                            "reason": "Pending controller-owned HITL queue entries remain unresolved.",
                            "priority": "high",
                        },
                    )
            self.workflow_policy._write(task_id=task_id, payload=state)
        if emit_events and redesign_update and redesign_update.get("changed"):
            redesign_entry = redesign_update.get("entry") or {}
            self._record_timeline(
                task_id=task_id,
                event_type="redesign_memory_updated",
                summary="Redesign memory was refreshed from the latest improvement and convergence artifacts.",
                payload={
                    "memory_id": redesign_entry.get("memory_id"),
                    "recommended_parent_action": redesign_entry.get("recommended_parent_action"),
                    "selected_disposition": redesign_entry.get("selected_disposition"),
                },
            )
        self.registry.write_json_artifact(
            task_id,
            "STAGE_CONTRACT_REPORT.json",
            state.get("stage_contract") or {},
            schema_name="stage_contract_report",
        )
        self._sync_notifications(
            task_id=task_id,
            workflow_policy=state,
            run_status=str((self.run_registry.load_latest(task_id) or {}).get("status") or ""),
        )
        self._sync_improvement_advisories(emit_events=emit_events)
        if emit_events:
            self._record_policy_transitions(task_id=task_id, previous=previous, current=state)
            self._emit_event("workflow_policy_changed", {"task_id": task_id, "workflow_policy": state})
            self._emit_event("hitl_queue_changed", self.get_hitl_queue(task_id=task_id, include_resolved=False))
        return state

    def run_monitor_cycle(self, *, task_id: str | None = None) -> dict[str, Any]:
        tasks: set[str] = set()
        if task_id:
            tasks.add(task_id)
        else:
            for run in self.run_registry.list_runs(limit=200):
                task_ref = str(run.get("task_id", "")).upper()
                if task_ref:
                    tasks.add(task_ref)
            tasks.update(self.workflow_policy.list_task_ids())
            for entry in self.hitl_queue.list_entries(include_resolved=False, limit=500):
                task_ref = str(entry.get("task_id", "")).upper()
                if task_ref:
                    tasks.add(task_ref)
        synced_tasks: list[str] = []
        policy_updates: list[dict[str, Any]] = []
        dispatch_results: list[dict[str, Any]] = []
        merge_results: list[dict[str, Any]] = []
        auto_closeouts: list[dict[str, Any]] = []
        legacy_runtime_tasks: list[str] = []
        errors: list[dict[str, str]] = []
        for current_task in sorted(tasks):
            try:
                existing_policy = self.workflow_policy.load(current_task)
                if task_id is None and existing_policy and not existing_policy.get("settings", {}).get("monitor_enabled", True):
                    continue
                run = self.run_registry.load_latest(current_task)
                if run and run.get("status") not in TERMINAL_STATUSES and (run.get("thread_id") or run.get("review_thread_id")):
                    sync_result = self.sync_task_run(task_id=current_task)
                    if sync_result.get("synced"):
                        synced_tasks.append(current_task)
                    else:
                        legacy_runtime_tasks.append(current_task)
                policy_state = self.evaluate_workflow_policy(task_id=current_task, emit_events=True)
                policy_updates.append(
                    {
                        "task_id": current_task,
                        "current_stage": policy_state.get("current_stage"),
                        "lifecycle_status": policy_state.get("lifecycle_status"),
                    }
                )
                merge_result = self._build_merge_package(task_id=current_task)
                if merge_result is not None:
                    merge_results.append({"task_id": current_task, **merge_result})
                dispatch_result = self._maybe_execute_auto_dispatch(task_id=current_task, policy_state=policy_state)
                if dispatch_result is not None:
                    dispatch_results.append(dispatch_result)
                if (
                    policy_state.get("lifecycle_status") == "READY_FOR_CLOSEOUT"
                    and policy_state.get("settings", {}).get("auto_closeout")
                    and not (self.registry.task_root(current_task) / "CLOSEOUT_EXECUTION_RECORD.json").exists()
                ):
                    auto_closeout_result = self.execute_closeout(task_id=current_task, validate_workspace=True)
                    auto_closeouts.append({"task_id": current_task, "status": auto_closeout_result.get("status")})
            except Exception as exc:
                errors.append({"task_id": current_task, "message": str(exc)})
                self._emit_event("controller_warning", {"task_id": current_task, "stage": "monitor_cycle", "message": str(exc)})
        payload = {
            "task_id": task_id,
            "task_count": len(tasks),
            "synced_tasks": synced_tasks,
            "policy_updates": policy_updates,
            "dispatch_results": dispatch_results,
            "merge_results": merge_results,
            "auto_closeouts": auto_closeouts,
            "legacy_runtime_tasks": legacy_runtime_tasks,
            "error_count": len(errors),
            "errors": errors,
        }
        self._emit_event("monitor_cycle_completed", payload)
        return payload

    def _require_or_create_run(self, *, task_id: str, auto_thread: bool) -> dict[str, Any]:
        latest = self.run_registry.load_latest(task_id)
        if latest is not None:
            if auto_thread and not latest.get("thread_id"):
                raise RuntimeError(RETIRED_RUNTIME_MESSAGE)
            return latest
        latest_context = self.control.get_latest_workflow_context(task_id=task_id)
        workflow_id = (latest_context.get("workflow") or {}).get("workflow_id")
        run = self.run_registry.ensure_run(task_id=task_id, workflow_id=workflow_id, status="IDLE", legacy_runtime_url=None)
        if auto_thread:
            raise RuntimeError(RETIRED_RUNTIME_MESSAGE)
        return run

    def _propagate_status(
        self,
        *,
        task_id: str,
        workflow_status: str,
        artifact_updates: dict[str, str | None] | None = None,
    ) -> None:
        latest_context = self.control.get_latest_workflow_context(task_id=task_id)
        workflow = latest_context.get("workflow") or {}
        workflow_id = workflow.get("workflow_id")
        if workflow_id:
            self.workflow_context.update_status(task_id=task_id, workflow_id=workflow_id, status=workflow_status, artifact_updates=artifact_updates)
        self.operator_sessions.update_latest_session(task_id=task_id, status=workflow_status, artifact_refs=artifact_updates)
        latest = self.run_registry.load_latest(task_id)
        if latest is not None:
            self.run_registry.update_status(task_id=task_id, run_id=latest["run_id"], status=workflow_status, artifact_updates=artifact_updates)

    def _review_record_spec(self, record_kind: str) -> dict[str, str]:
        if record_kind == "adversarial_review":
            return {
                "filename": "ADVERSARIAL_REVIEW_RECORD.json",
                "schema_name": "adversarial_review_record",
                "type": "ADVERSARIAL_REVIEW_RECORD",
                "artifact_key": "adversarial_review_record",
                "queue_category": "adversarial_review",
                "event_name": "adversarial_review_changed",
                "timeline_started_event": "adversarial_review_started",
                "timeline_started_summary": "Controller started an adversarial review gate.",
                "timeline_finalized_event": "adversarial_review_finalized",
                "timeline_finalized_summary": "Adversarial review finalized with verdict {verdict}.",
                "queue_summary_started": "Adversarial review started and awaits findings or operator disposition.",
                "queue_summary_ready": "Adversarial review output captured and awaits operator verdict.",
                "queue_summary_pending": "Adversarial review is pending or needs operator attention.",
            }
        return {
            "filename": "REVIEW_GATE_RECORD.json",
            "schema_name": "review_gate_record",
            "type": "REVIEW_GATE_RECORD",
            "artifact_key": "review_gate_record",
            "queue_category": "review_gate",
            "event_name": "review_gate_changed",
            "timeline_started_event": "review_started",
            "timeline_started_summary": "Controller started a review gate.",
            "timeline_finalized_event": "review_finalized",
            "timeline_finalized_summary": "Review finalized with verdict {verdict}.",
            "queue_summary_started": "Review started and awaits findings or operator disposition.",
            "queue_summary_ready": "Review output captured and awaits operator verdict.",
            "queue_summary_pending": "Review is pending or needs operator attention.",
        }

    def _review_workflow_status(self, *, record_kind: str, review_status: str) -> str:
        if record_kind == "adversarial_review":
            return f"ADVERSARIAL_{review_status}"
        return review_status

    def _write_review_record(
        self,
        *,
        task_id: str,
        run: dict[str, Any],
        record_kind: str,
        review_status: str,
        review_thread_id: str | None,
        review_target: dict[str, Any] | None,
        review_delivery: str | None,
        custom_instructions: str | None,
        review_response: dict[str, Any] | None,
        findings: list[dict[str, Any]] | None,
        verdict: str | None,
        summary: str | None,
        completed_at: str | None,
        notes: list[str] | None = None,
        adversarial_policy: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        spec = self._review_record_spec(record_kind)
        path = self.registry.task_root(task_id) / spec["filename"]
        existing = load_json(path) if path.exists() else {}
        payload = {
            "type": spec["type"],
            "task_id": task_id,
            "workflow_id": run.get("workflow_id"),
            "run_id": run["run_id"],
            "thread_id": run.get("thread_id"),
            "review_thread_id": review_thread_id or existing.get("review_thread_id"),
            "review_turn_id": run.get("review_turn_id"),
            "review_status": review_status,
            "review_target": review_target if review_target is not None else existing.get("review_target"),
            "review_delivery": review_delivery if review_delivery is not None else existing.get("review_delivery"),
            "custom_instructions": custom_instructions if custom_instructions is not None else existing.get("custom_instructions"),
            "started_at": existing.get("started_at", utc_now()),
            "completed_at": completed_at if completed_at is not None else existing.get("completed_at"),
            "verdict": verdict if verdict is not None else existing.get("verdict"),
            "summary": summary if summary is not None else existing.get("summary"),
            "findings": findings if findings is not None else existing.get("findings", []),
            "source": "operator_controller_service",
            "review_response": review_response if review_response is not None else existing.get("review_response"),
            "artifact_refs": {
                "workflow_run_record": f"docs/task_workspaces/{task_id}/WORKFLOW_RUN_RECORD.json",
                "human_decision_record": f"docs/task_workspaces/{task_id}/HUMAN_DECISION_RECORD.json",
                "controller_run_result": f"docs/task_workspaces/{task_id}/CONTROLLER_RUN_RESULT.json",
            },
            "notes": notes if notes is not None else existing.get("notes", []),
            "updated_at": utc_now(),
        }
        if record_kind == "adversarial_review":
            payload.update(
                {
                    "review_role": "adversarial_analyst",
                    "required_before_stage_close": bool((adversarial_policy or {}).get("required_before_stage_close", False)),
                    "triggering_stage": str((self.workflow_policy.load(task_id) or {}).get("current_stage") or "UNKNOWN"),
                    "trigger_reasons": list((adversarial_policy or {}).get("trigger_reasons", [])),
                }
            )
        self.registry.write_json_artifact(task_id, spec["filename"], payload, schema_name=spec["schema_name"])
        workflow_path = self.registry.task_root(task_id) / "WORKFLOW_RUN_RECORD.json"
        if workflow_path.exists():
            workflow_record = load_json(workflow_path)
            workflow_record["status"] = self._review_workflow_status(record_kind=record_kind, review_status=review_status)
            workflow_record.setdefault("artifacts", {})[spec["artifact_key"]] = f"docs/task_workspaces/{task_id}/{spec['filename']}"
            self.registry.write_json_artifact(task_id, "WORKFLOW_RUN_RECORD.json", workflow_record, schema_name="workflow_run_record")
        return {"path": f"docs/task_workspaces/{task_id}/{spec['filename']}", "payload": payload}

    def _write_review_gate_record(
        self,
        *,
        task_id: str,
        run: dict[str, Any],
        review_status: str,
        review_thread_id: str | None,
        review_target: dict[str, Any] | None,
        review_delivery: str | None,
        custom_instructions: str | None,
        review_response: dict[str, Any] | None,
        findings: list[dict[str, Any]] | None,
        verdict: str | None,
        summary: str | None,
        completed_at: str | None,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        return self._write_review_record(
            task_id=task_id,
            run=run,
            record_kind="review_gate",
            review_status=review_status,
            review_thread_id=review_thread_id,
            review_target=review_target,
            review_delivery=review_delivery,
            custom_instructions=custom_instructions,
            review_response=review_response,
            findings=findings,
            verdict=verdict,
            summary=summary,
            completed_at=completed_at,
            notes=notes,
        )

    def _write_convergence_gate_record(
        self,
        *,
        task_id: str,
        run: dict[str, Any],
        selected_disposition: str | None,
        rationale: str | None,
        completed_at: str | None,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        path = self.registry.task_root(task_id) / "CONVERGENCE_GATE_RECORD.json"
        existing = load_json(path) if path.exists() else {}
        workflow_policy = self.workflow_policy.load(task_id) or self.get_workflow_policy(task_id=task_id, refresh=False)
        convergence = dict(workflow_policy.get("convergence") or {})
        normalized_disposition = (
            str(selected_disposition).strip().upper().replace(" ", "_")
            if selected_disposition is not None
            else None
        )
        if normalized_disposition is None:
            convergence_status = str(convergence.get("status") or existing.get("convergence_status") or "READY_FOR_DECISION")
        elif normalized_disposition == "CONTINUE_EXPLORATION":
            convergence_status = "CONTINUE_EXPLORATION"
        else:
            convergence_status = "DECIDED"
        payload = {
            "type": "CONVERGENCE_GATE_RECORD",
            "task_id": task_id,
            "workflow_id": run.get("workflow_id"),
            "run_id": run.get("run_id"),
            "current_stage": workflow_policy.get("current_stage"),
            "required_before_stage_close": bool(convergence.get("required_before_stage_close", False)),
            "convergence_status": convergence_status,
            "ready_for_decision": bool(convergence.get("ready_for_decision", False)),
            "satisfied": bool(
                convergence.get("satisfied", False)
                if selected_disposition is None
                else normalized_disposition in {"REJECT", "ADOPT", "HYBRIDIZE", "ESCALATE_TO_HITL", "PROMOTE"}
            ),
            "branch_count": int(convergence.get("branch_count", 0)),
            "minimum_completed_branches": int(convergence.get("minimum_completed_branches", 0)),
            "completed_branch_count": int(convergence.get("completed_branch_count", 0)),
            "disagreement_signals": list(convergence.get("disagreement_signals", [])),
            "recommended_parent_action": convergence.get("recommended_parent_action"),
            "decision_options": list(convergence.get("decision_options", [])),
            "gamma_present": bool(convergence.get("gamma_present", False)),
            "requires_gamma_disposition": bool(convergence.get("requires_gamma_disposition", False)),
            "selected_disposition": (
                str(selected_disposition).strip().lower().replace(" ", "_")
                if selected_disposition is not None
                else existing.get("selected_disposition")
            ),
            "rationale": rationale if rationale is not None else existing.get("rationale"),
            "started_at": existing.get("started_at", utc_now()),
            "completed_at": completed_at if completed_at is not None else existing.get("completed_at"),
            "source_refs": {
                "future_convergence_report": f"docs/task_workspaces/{task_id}/FUTURE_CONVERGENCE_REPORT.json"
                if (self.registry.task_root(task_id) / "FUTURE_CONVERGENCE_REPORT.json").exists()
                else None,
                "task_improvement_report": f"docs/task_workspaces/{task_id}/TASK_IMPROVEMENT_REPORT.json"
                if (self.registry.task_root(task_id) / "TASK_IMPROVEMENT_REPORT.json").exists()
                else None,
                "radical_redesign_report": f"docs/task_workspaces/{task_id}/RADICAL_REDESIGN_REPORT.json"
                if (self.registry.task_root(task_id) / "RADICAL_REDESIGN_REPORT.json").exists()
                else None,
            },
            "source": "operator_controller_service",
            "notes": notes if notes is not None else existing.get("notes", []),
            "updated_at": utc_now(),
        }
        self.registry.write_json_artifact(
            task_id,
            "CONVERGENCE_GATE_RECORD.json",
            payload,
            schema_name="convergence_gate_record",
        )
        workflow_path = self.registry.task_root(task_id) / "WORKFLOW_RUN_RECORD.json"
        if workflow_path.exists():
            workflow_record = load_json(workflow_path)
            workflow_record.setdefault("artifacts", {})["convergence_gate_record"] = (
                f"docs/task_workspaces/{task_id}/CONVERGENCE_GATE_RECORD.json"
            )
            self.registry.write_json_artifact(
                task_id,
                "WORKFLOW_RUN_RECORD.json",
                workflow_record,
                schema_name="workflow_run_record",
            )
        return {"path": f"docs/task_workspaces/{task_id}/CONVERGENCE_GATE_RECORD.json", "payload": payload}

    def _review_status_from_verdict(self, verdict: str) -> str:
        normalized = verdict.strip().upper().replace(" ", "_")
        if normalized in {"APPROVE", "APPROVED", "PASS"}:
            return "REVIEW_APPROVED"
        if normalized in {"CHANGES_REQUESTED", "REQUEST_CHANGES", "ADVANCE_WITH_CONDITIONS"}:
            return "REVIEW_CHANGES_REQUESTED"
        if normalized in {"BLOCK", "BLOCKED", "FAIL", "REJECT"}:
            return "REVIEW_BLOCKED"
        return f"REVIEW_{normalized}"

    def _ensure_review_queue_entry(
        self,
        *,
        task_id: str,
        run: dict[str, Any],
        summary: str,
        artifact_refs: dict[str, str],
        category: str = "review_gate",
    ) -> dict[str, Any]:
        for entry in self.hitl_queue.list_entries(task_id=task_id, include_resolved=False, limit=100):
            if entry.get("category") == category and entry.get("run_id") == run["run_id"]:
                return self.hitl_queue.update_entry(
                    entry_id=entry["entry_id"],
                    summary=summary,
                    artifact_refs=artifact_refs,
                    metadata={"review_thread_id": run.get("review_thread_id"), "record_kind": category},
                )
        return self.hitl_queue.create_entry(
            task_id=task_id,
            run_id=run["run_id"],
            source="controller",
            category=category,
            summary=summary,
            thread_id=run.get("thread_id"),
            review_thread_id=run.get("review_thread_id"),
            artifact_refs=artifact_refs,
            metadata={"review_thread_id": run.get("review_thread_id"), "record_kind": category},
        )

    def _default_handoff_artifacts(self, *, task_id: str) -> list[dict[str, str]]:
        task_root = self.registry.task_root(task_id)
        candidates = [
            ("WORKFLOW_RUN_RECORD.json", "Workflow run record"),
            ("HUMAN_DECISION_RECORD.json", "Human decision record"),
            ("REVIEW_GATE_RECORD.json", "Review gate record"),
            ("ADVERSARIAL_REVIEW_RECORD.json", "Adversarial review record"),
            ("CONVERGENCE_GATE_RECORD.json", "Convergence gate record"),
            ("CONTROLLER_RUN_RESULT.json", "Controller run result"),
            ("CLOSEOUT_EXECUTION_RECORD.json", "Closeout execution record"),
            ("STAGE_CONTRACT_REPORT.json", "Stage contract report"),
            ("CHILD_RESULT_MERGE_PACKAGE.json", "Child-result merge package"),
            ("FUTURE_BRANCH_REPORT.json", "Future-branch plan"),
            ("FUTURE_CONVERGENCE_REPORT.json", "Future-convergence report"),
            ("TASK_IMPROVEMENT_REPORT.json", "Task-improvement report"),
            ("RADICAL_REDESIGN_REPORT.json", "Radical redesign report"),
            ("SHARED_STATE_CLOSEOUT_RECORD.json", "Shared-state closeout record"),
        ]
        artifacts = []
        for filename, description in candidates:
            if (task_root / filename).exists():
                artifacts.append({"path": f"docs/task_workspaces/{task_id}/{filename}", "description": description})
        return artifacts

    def _validate_workspace(self, *, task_id: str) -> dict[str, Any]:
        validator = self.repo_root / "scripts" / "validate_aas1_task_workspace.py"
        workspace = self.registry.task_root(task_id)
        completed = subprocess.run(
            [sys.executable, str(validator), str(workspace)],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        output = completed.stdout
        if completed.stderr:
            output = (output + "\n" + completed.stderr).strip()
        return {"valid": completed.returncode == 0, "exit_code": completed.returncode, "output": output.strip()}

    def _monitor_loop(self) -> None:
        while not self._monitor_stop.wait(self._monitor_interval_seconds):
            try:
                self.run_monitor_cycle()
            except Exception as exc:
                self._emit_event("controller_warning", {"stage": "monitor_loop", "message": str(exc)})

    def _record_timeline(
        self,
        *,
        task_id: str | None,
        event_type: str,
        summary: str,
        payload: dict[str, Any] | None = None,
        level: str = "INFO",
    ) -> None:
        if not task_id:
            return
        self.audit_timeline.append_event(
            task_id=task_id,
            event_type=event_type,
            summary=summary,
            payload=payload,
            level=level,
        )
        self._emit_event("audit_timeline_changed", self.get_audit_timeline(task_id=task_id, limit=50))
        self._emit_event("dashboard_summary_changed", self.get_dashboard_summary(limit_tasks=20))

    def _record_policy_transitions(
        self,
        *,
        task_id: str,
        previous: dict[str, Any] | None,
        current: dict[str, Any],
    ) -> None:
        if previous is None:
            self._record_timeline(
                task_id=task_id,
                event_type="workflow_policy_seeded",
                summary=f"Workflow policy initialized at stage {current.get('current_stage')}.",
                payload={"workflow_policy": current},
            )
            return
        if previous.get("current_stage") != current.get("current_stage"):
            self._record_timeline(
                task_id=task_id,
                event_type="stage_transition",
                summary=f"Workflow advanced from {previous.get('current_stage')} to {current.get('current_stage')}.",
                payload={
                    "previous_stage": previous.get("current_stage"),
                    "current_stage": current.get("current_stage"),
                    "lifecycle_status": current.get("lifecycle_status"),
                },
            )
        elif previous.get("lifecycle_status") != current.get("lifecycle_status"):
            self._record_timeline(
                task_id=task_id,
                event_type="workflow_state_changed",
                summary=f"Workflow state changed from {previous.get('lifecycle_status')} to {current.get('lifecycle_status')}.",
                payload={
                    "previous_lifecycle_status": previous.get("lifecycle_status"),
                    "current_lifecycle_status": current.get("lifecycle_status"),
                    "current_stage": current.get("current_stage"),
                },
            )

    def _ensure_policy_queue_entries(self, *, task_id: str, policy_state: dict[str, Any]) -> None:
        run = self.run_registry.load_latest(task_id)
        run_id = run.get("run_id") if run else None
        artifact_refs = {
            "workflow_policy": f"runtime/state/workflow_policy/{task_id}/latest.json",
            "workflow_run_record": f"docs/task_workspaces/{task_id}/WORKFLOW_RUN_RECORD.json",
        }
        lifecycle_status = policy_state.get("lifecycle_status")
        convergence = dict(policy_state.get("convergence") or {})
        if convergence.get("required_before_stage_close") and not convergence.get("satisfied"):
            convergence_artifacts = dict(artifact_refs)
            if convergence.get("record_ref"):
                convergence_artifacts["convergence_gate_record"] = str(convergence["record_ref"])
            if (policy_state.get("artifacts") or {}).get("future_convergence_report"):
                convergence_artifacts["future_convergence_report"] = str((policy_state.get("artifacts") or {}).get("future_convergence_report"))
            if (policy_state.get("artifacts") or {}).get("task_improvement_report"):
                convergence_artifacts["task_improvement_report"] = str((policy_state.get("artifacts") or {}).get("task_improvement_report"))
            if (policy_state.get("artifacts") or {}).get("radical_redesign_report"):
                convergence_artifacts["radical_redesign_report"] = str((policy_state.get("artifacts") or {}).get("radical_redesign_report"))
            self._ensure_controller_hitl_entry(
                task_id=task_id,
                run_id=run_id,
                category="convergence_gate",
                summary="Convergence decision is required before the current stage can close.",
                artifact_refs=convergence_artifacts,
                metadata={
                    "current_stage": policy_state.get("current_stage"),
                    "convergence_status": convergence.get("status"),
                    "recommended_parent_action": convergence.get("recommended_parent_action"),
                    "decision_options": list(convergence.get("decision_options", [])),
                },
            )
        if lifecycle_status == "NEXT_STAGE_READY":
            self._ensure_controller_hitl_entry(
                task_id=task_id,
                run_id=run_id,
                category="stage_transition",
                summary=f"{policy_state.get('current_stage')} is ready to begin.",
                artifact_refs=artifact_refs,
                metadata={"current_stage": policy_state.get("current_stage"), "next_actions": policy_state.get("next_actions")},
            )
        if lifecycle_status == "READY_FOR_CLOSEOUT":
            self._ensure_controller_hitl_entry(
                task_id=task_id,
                run_id=run_id,
                category="closeout_gate",
                summary="Task is ready for closeout execution.",
                artifact_refs=artifact_refs,
                metadata={"current_stage": policy_state.get("current_stage")},
            )
        primary = (policy_state.get("dispatch") or {}).get("primary")
        if primary:
            self._ensure_controller_hitl_entry(
                task_id=task_id,
                run_id=run_id,
                category="dispatch_recommendation",
                summary=f"Dispatch candidate ready: {primary.get('instruction')}.",
                artifact_refs=artifact_refs,
                metadata={"dispatch": primary, "dispatch_mode": (policy_state.get("dispatch") or {}).get("dispatch_mode")},
            )

    def _ensure_controller_hitl_entry(
        self,
        *,
        task_id: str,
        run_id: str | None,
        category: str,
        summary: str,
        artifact_refs: dict[str, str],
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        for entry in self.hitl_queue.list_entries(task_id=task_id, include_resolved=False, limit=200):
            if entry.get("source") == "controller" and entry.get("category") == category:
                return self.hitl_queue.update_entry(
                    entry_id=entry["entry_id"],
                    summary=summary,
                    artifact_refs=artifact_refs,
                    metadata=metadata,
                )
        return self.hitl_queue.create_entry(
            task_id=task_id,
            run_id=run_id,
            source="controller",
            category=category,
            summary=summary,
            artifact_refs=artifact_refs,
            metadata=metadata,
        )

    def _maybe_execute_auto_dispatch(self, *, task_id: str, policy_state: dict[str, Any]) -> dict[str, Any] | None:
        dispatch = policy_state.get("dispatch") or {}
        if not dispatch.get("auto_execute_ready"):
            return None
        primary = dispatch.get("primary") or {}
        if not primary.get("instruction") or not primary.get("action_label"):
            return None
        manager = InventionPipelineManager(self.repo_root)
        result = manager.prepare_team_dispatch(
            task_id=task_id,
            action_label=str(primary["action_label"]),
            instruction=str(primary["instruction"]),
            provider="codex",
            execute=True,
            dry_run=False,
        )
        updated_policy = self.workflow_policy.update_settings(task_id=task_id)
        updated_policy_dispatch = dict(policy_state.get("dispatch") or {})
        updated_policy_dispatch["last_executed"] = {
            "instruction": primary.get("instruction"),
            "action_label": primary.get("action_label"),
            "executed_at": utc_now(),
        }
        updated_policy["dispatch"] = updated_policy_dispatch
        updated_policy["updated_at"] = utc_now()
        self.workflow_policy._write(task_id=task_id, payload=updated_policy)
        self._record_timeline(
            task_id=task_id,
            event_type="auto_dispatch_executed",
            summary=f"Auto-dispatch executed for {primary.get('instruction')}.",
            payload={"dispatch": primary, "result": result},
        )
        self._emit_event("workflow_policy_changed", {"task_id": task_id, "workflow_policy": updated_policy})
        return {"task_id": task_id, "dispatch": primary, "result": result}

    def _sync_notifications(
        self,
        *,
        task_id: str,
        workflow_policy: dict[str, Any],
        run_status: str,
    ) -> dict[str, Any]:
        payload = self.notifications.sync_task_state(
            task_id=task_id,
            workflow_policy=workflow_policy,
            pending_hitl_count=len(self.hitl_queue.list_entries(task_id=task_id, include_resolved=False, limit=500)),
            run_status=run_status,
        )
        self._emit_event("notifications_changed", {"notifications": payload.get("notifications", [])})
        return payload

    def _sync_improvement_advisories(self, *, emit_events: bool) -> dict[str, Any]:
        payload = self.improvement_observer.evaluate()
        if emit_events and payload.get("changed"):
            self._emit_event(
                "improvement_advisories_changed",
                {
                    "updated_at": payload.get("updated_at"),
                    "open_count": payload.get("open_count", 0),
                    "advisories": payload.get("advisories", []),
                },
            )
        return payload

    def _build_merge_package(self, *, task_id: str) -> dict[str, Any] | None:
        result = self.merge_engine.build_for_task(task_id=task_id)
        if result is None:
            return None
        latest = self.run_registry.load_latest(task_id)
        if latest is not None:
            self.run_registry.update_status(
                task_id=task_id,
                run_id=latest["run_id"],
                status=str(latest.get("status") or "IDLE"),
                artifact_updates={"child_result_merge_package": result["merge_package_ref"]},
            )
        self._record_timeline(
            task_id=task_id,
            event_type="child_results_merged",
            summary="Controller generated a parent child-result merge package.",
            payload={"merge_package_ref": result["merge_package_ref"], "draft_ref": result["draft_ref"]},
        )
        return result

    def _resolve_task_title(self, *, task_id: str) -> str:
        title = None
        try:
            title = self.control._title_for_task(task_id)  # type: ignore[attr-defined]
        except Exception:
            title = None
        return title or f"{task_id} controller-managed task"

    def _validate_agent_state(self) -> dict[str, Any]:
        validator = self.repo_root / "scripts" / "validate_agent_state.py"
        target = self.repo_root / "docs" / "AGENT_STATE.md"
        completed = subprocess.run(
            [sys.executable, str(validator), str(target.relative_to(self.repo_root))],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        output = completed.stdout
        if completed.stderr:
            output = (output + "\n" + completed.stderr).strip()
        return {"valid": completed.returncode == 0, "exit_code": completed.returncode, "output": output.strip()}

    def _emit_event(self, event_type: str, payload: dict[str, Any]) -> None:
        if self._event_callback is None:
            return
        try:
            self._event_callback({"event_type": event_type, "timestamp": utc_now(), "payload": payload})
        except Exception:
            return

    def _load_optional_json(self, path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        return load_json(path)
