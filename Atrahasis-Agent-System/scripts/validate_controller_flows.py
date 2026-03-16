#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass
class ValidationCheck:
    name: str
    ok: bool
    detail: str
    elapsed_ms: int
    payload_preview: str | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate local Atrahasis controller flows either offline or with live App Server/model traffic."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    offline = subparsers.add_parser(
        "offline",
        help="Validate controller HTTP surfaces without external model traffic.",
    )
    _add_common_args(offline)

    live = subparsers.add_parser(
        "live",
        help="Validate the controller end-to-end with the local App Server and real model traffic.",
    )
    _add_common_args(live)
    live.add_argument("--listen-url", default="ws://127.0.0.1:8765")
    live.add_argument("--codex-executable")
    live.add_argument("--turn-prompt", required=True)
    live.add_argument("--effort", default="high")
    live.add_argument("--sync-polls", type=int, default=2)
    live.add_argument("--sync-interval", type=float, default=2.0)
    live.add_argument("--review-instructions")
    live.add_argument("--review-role")
    live.add_argument("--skip-review", action="store_true")
    live.add_argument("--review-verdict")
    live.add_argument("--review-summary")
    live.add_argument("--review-findings-file")
    live.add_argument("--operator-decision")
    live.add_argument("--workflow-status")
    live.add_argument("--operator-note", action="append", default=[])
    live.add_argument("--dispatch-spawn-id")
    live.add_argument("--action-label", default="spawn_program")
    live.add_argument("--provider", default="codex")
    live.add_argument("--execute-closeout", action="store_true")
    live.add_argument("--skip-validate-workspace", action="store_true")

    return parser


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task-id", default="T-9002")
    parser.add_argument("--service-url")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int)
    parser.add_argument("--python-executable", default=sys.executable)
    parser.add_argument("--startup-timeout", type=float, default=20.0)
    parser.add_argument("--request-timeout", type=float, default=15.0)
    parser.add_argument("--report-path")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.mode == "live" and args.review_verdict and not args.review_summary:
        parser.error("--review-summary is required when --review-verdict is supplied.")

    repo_root = Path(__file__).resolve().parents[1]
    process: subprocess.Popen[str] | None = None
    service_url = args.service_url
    spawned_service = False
    report: dict[str, Any]

    try:
        if not service_url:
            port = args.port or _find_open_port(args.host)
            service_url = f"http://{args.host}:{port}"
            process = _spawn_service(
                repo_root=repo_root,
                python_executable=args.python_executable,
                host=args.host,
                port=port,
            )
            spawned_service = True
            _wait_for_health(service_url, timeout_seconds=args.startup_timeout, request_timeout=args.request_timeout)

        if args.mode == "offline":
            report = run_offline_validation(
                service_url=service_url,
                task_id=args.task_id.upper(),
                request_timeout=args.request_timeout,
                spawned_service=spawned_service,
            )
        else:
            report = run_live_validation(
                service_url=service_url,
                task_id=args.task_id.upper(),
                request_timeout=args.request_timeout,
                listen_url=args.listen_url,
                codex_executable=args.codex_executable,
                turn_prompt=args.turn_prompt,
                effort=args.effort,
                sync_polls=args.sync_polls,
                sync_interval=args.sync_interval,
                review_instructions=args.review_instructions,
                review_role=args.review_role,
                skip_review=args.skip_review,
                review_verdict=args.review_verdict,
                review_summary=args.review_summary,
                review_findings_file=args.review_findings_file,
                operator_decision=args.operator_decision,
                workflow_status=args.workflow_status,
                operator_notes=args.operator_note,
                dispatch_spawn_id=args.dispatch_spawn_id,
                action_label=args.action_label,
                provider=args.provider,
                execute_closeout=args.execute_closeout,
                validate_workspace=not args.skip_validate_workspace,
                spawned_service=spawned_service,
            )
    finally:
        if process is not None:
            _stop_service(process)

    if args.report_path:
        report_path = Path(args.report_path)
        if not report_path.is_absolute():
            report_path = (repo_root / report_path).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        report["report_path"] = str(report_path)

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("ok", False) else 1


def run_offline_validation(
    *,
    service_url: str,
    task_id: str,
    request_timeout: float = 15.0,
    spawned_service: bool = False,
) -> dict[str, Any]:
    checks: list[ValidationCheck] = []
    checks.append(_expect_json(service_url, "GET", "/api/health", timeout=request_timeout, validator=lambda payload: ("status" in payload and "app_server" in payload, "Health payload returned service and app server status.")))
    checks.append(_expect_json(service_url, "GET", "/api/controller/session-brief", timeout=request_timeout, validator=lambda payload: ("summary" in payload and "next_dispatchable_canonical_task" in payload, "Session brief returned summary and next dispatchable task.")))
    checks.append(_expect_json(service_url, "GET", f"/api/controller/dispatchable?{urlencode({'limit': 3})}", timeout=request_timeout, validator=lambda payload: ("tasks" in payload and "next_dispatchable_canonical_task" in payload, "Dispatchable tasks returned tasks and canonical next task.")))
    checks.append(_expect_json(service_url, "GET", f"/api/controller/status?{urlencode({'task_id': task_id})}", timeout=request_timeout, validator=lambda payload: (payload.get("task_id") == task_id, f"Status payload returned task_id={task_id}.")))
    checks.append(_expect_json(service_url, "GET", f"/api/controller/run-state?{urlencode({'task_id': task_id})}", timeout=request_timeout, validator=lambda payload: (payload.get("task_id") == task_id and "run" in payload, "Run state returned task_id and run payload.")))
    checks.append(_expect_json(service_url, "GET", f"/api/controller/workflow-policy?{urlencode({'task_id': task_id, 'refresh': 'false'})}", timeout=request_timeout, validator=lambda payload: (payload.get("task_id") == task_id and "current_stage" in payload, "Workflow policy returned task_id and current_stage.")))
    checks.append(_expect_json(service_url, "GET", f"/api/controller/dashboard-summary?{urlencode({'limit_tasks': 5})}", timeout=request_timeout, validator=lambda payload: ("dashboard" in payload and "notifications" in payload and "daemon" in payload, "Dashboard summary returned dashboard, notifications, and daemon state.")))
    checks.append(_expect_json(service_url, "GET", f"/api/controller/notifications?{urlencode({'limit': 10})}", timeout=request_timeout, validator=lambda payload: ("notifications" in payload and "notification_count" in payload, "Notification feed returned notifications and counts.")))
    checks.append(_expect_json(service_url, "GET", "/api/controller/daemon-status", timeout=request_timeout, validator=lambda payload: ("running" in payload, "Daemon status returned a running flag.")))
    checks.append(_expect_json(service_url, "GET", f"/api/controller/audit-timeline?{urlencode({'task_id': task_id, 'limit': 5})}", timeout=request_timeout, validator=lambda payload: (payload.get("task_id") == task_id and "events" in payload, "Audit timeline returned task_id and events.")))
    checks.append(_expect_json(service_url, "GET", f"/api/controller/hitl-queue?{urlencode({'task_id': task_id, 'limit': 5})}", timeout=request_timeout, validator=lambda payload: (payload.get("task_id") == task_id and "entries" in payload, "HITL queue returned task_id and entries.")))
    checks.append(_expect_json(service_url, "POST", "/api/controller/evaluate-workflow-policy", payload={"task_id": task_id}, timeout=request_timeout, validator=lambda payload: (payload.get("task_id") == task_id and "workflow_policy" in payload, "Policy evaluation returned workflow policy state.")))
    checks.append(_expect_json(service_url, "POST", "/api/controller/monitor-cycle", payload={"task_id": task_id}, timeout=request_timeout, validator=lambda payload: ("task_ids" in payload or "processed_tasks" in payload or "task_id" in payload, "Monitor cycle endpoint returned a monitor summary.")))
    return _build_report(
        mode="offline",
        service_url=service_url,
        task_id=task_id,
        checks=checks,
        spawned_service=spawned_service,
    )


def run_live_validation(
    *,
    service_url: str,
    task_id: str,
    request_timeout: float,
    listen_url: str,
    codex_executable: str | None,
    turn_prompt: str,
    effort: str,
    sync_polls: int,
    sync_interval: float,
    review_instructions: str | None,
    review_role: str | None,
    skip_review: bool,
    review_verdict: str | None,
    review_summary: str | None,
    review_findings_file: str | None,
    operator_decision: str | None,
    workflow_status: str | None,
    operator_notes: list[str],
    dispatch_spawn_id: str | None,
    action_label: str,
    provider: str,
    execute_closeout: bool,
    validate_workspace: bool,
    spawned_service: bool,
) -> dict[str, Any]:
    checks = run_offline_validation(
        service_url=service_url,
        task_id=task_id,
        request_timeout=request_timeout,
        spawned_service=spawned_service,
    )["checks"]

    checks.append(
        _expect_json(
            service_url,
            "POST",
            "/api/app-server/start",
            payload={key: value for key, value in {"listen_url": listen_url, "codex_executable": codex_executable}.items() if value},
            timeout=request_timeout,
            validator=lambda payload: ("app_server" in payload and bool(payload["app_server"].get("running")), "App Server start returned a running status."),
        )
    )
    checks.append(
        _expect_json(
            service_url,
            "POST",
            "/api/controller/start-task-thread",
            payload={"task_id": task_id},
            timeout=request_timeout,
            validator=lambda payload: (payload.get("task_id") == task_id and payload.get("run", {}).get("thread_id"), "Controller bound a thread to the task."),
        )
    )
    checks.append(
        _expect_json(
            service_url,
            "POST",
            "/api/controller/start-task-turn",
            payload={"task_id": task_id, "prompt": turn_prompt, "effort": effort},
            timeout=request_timeout,
            validator=lambda payload: (payload.get("task_id") == task_id and payload.get("run", {}).get("status"), "Controller started a turn."),
        )
    )

    for poll_index in range(max(sync_polls, 0)):
        if poll_index:
            time.sleep(max(0.0, sync_interval))
        checks.append(
            _expect_json(
                service_url,
                "POST",
                "/api/controller/sync-task-run",
                payload={"task_id": task_id},
                timeout=request_timeout,
                validator=lambda payload: (payload.get("task_id") == task_id and "run" in payload, "Controller sync returned task run state."),
            )
        )

    review_payload: dict[str, Any] | None = None
    if not skip_review:
        checks.append(
            _expect_json(
                service_url,
                "POST",
                "/api/controller/start-review",
                payload={
                    "task_id": task_id,
                    "instructions": review_instructions,
                    "delivery": "detached",
                    "review_role": review_role,
                },
                timeout=request_timeout,
                validator=lambda payload: (payload.get("task_id") == task_id and payload.get("run", {}).get("review_thread_id"), "Controller started a review gate."),
            )
        )
        if review_verdict and review_summary:
            review_payload = {
                "task_id": task_id,
                "verdict": review_verdict,
                "summary": review_summary,
                "findings": _load_json_file(review_findings_file) if review_findings_file else [],
                "notes": ["Generated by validate_controller_flows.py"],
            }
            checks.append(
                _expect_json(
                    service_url,
                    "POST",
                    "/api/controller/finalize-review",
                    payload=review_payload,
                    timeout=request_timeout,
                    validator=lambda payload: (payload.get("task_id") == task_id and payload.get("review_gate_record", {}).get("review_status"), "Review finalization returned a review gate record."),
                )
            )

    decision_payload: dict[str, Any] | None = None
    if operator_decision:
        decision_payload = {
            "task_id": task_id,
            "operator_decision": operator_decision,
            "workflow_status": workflow_status,
            "constraints": [],
            "notes": operator_notes or ["Generated by validate_controller_flows.py"],
        }
        checks.append(
            _expect_json(
                service_url,
                "POST",
                "/api/controller/record-human-decision",
                payload=decision_payload,
                timeout=request_timeout,
                validator=lambda payload: (payload.get("task_id") == task_id and payload.get("human_decision_record", {}).get("operator_decision"), "Human decision record was written."),
            )
        )

    if dispatch_spawn_id:
        checks.append(
            _expect_json(
                service_url,
                "POST",
                "/api/controller/dispatch",
                payload={
                    "task_id": task_id,
                    "spawn_id": dispatch_spawn_id,
                    "action_label": action_label,
                    "provider": provider,
                    "dry_run": True,
                },
                timeout=request_timeout,
                validator=lambda payload: ("status" in payload or "team_plan" in payload or "dispatch_record" in payload, "Dispatch endpoint returned a team dispatch payload."),
            )
        )

    if execute_closeout:
        checks.append(
            _expect_json(
                service_url,
                "POST",
                "/api/controller/execute-closeout",
                payload={
                    "task_id": task_id,
                    "review": _closeout_review_payload(review_payload),
                    "human_decision": _closeout_human_decision_payload(decision_payload),
                    "validate_workspace": validate_workspace,
                },
                timeout=request_timeout,
                validator=lambda payload: (payload.get("task_id") == task_id and "validation" in payload, "Closeout execution returned a validation summary."),
            )
        )

    return _build_report(
        mode="live",
        service_url=service_url,
        task_id=task_id,
        checks=checks,
        spawned_service=spawned_service,
    )


def _closeout_review_payload(review_payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if not review_payload:
        return None
    return {
        "verdict": review_payload["verdict"],
        "summary": review_payload["summary"],
        "findings": review_payload.get("findings", []),
        "notes": review_payload.get("notes", []),
    }


def _closeout_human_decision_payload(decision_payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if not decision_payload:
        return None
    return {
        "operator_decision": decision_payload["operator_decision"],
        "workflow_status": decision_payload.get("workflow_status"),
        "constraints": decision_payload.get("constraints", []),
        "notes": decision_payload.get("notes", []),
    }


def _expect_json(
    service_url: str,
    method: str,
    path: str,
    *,
    payload: dict[str, Any] | None = None,
    timeout: float,
    validator: Any,
) -> ValidationCheck:
    started = time.perf_counter()
    try:
        response = _request_json(service_url, method, path, payload=payload, timeout=timeout)
        ok, detail = validator(response)
        return ValidationCheck(
            name=f"{method} {path}",
            ok=bool(ok),
            detail=str(detail),
            elapsed_ms=int((time.perf_counter() - started) * 1000),
            payload_preview=_preview(response),
        )
    except Exception as exc:
        return ValidationCheck(
            name=f"{method} {path}",
            ok=False,
            detail=str(exc),
            elapsed_ms=int((time.perf_counter() - started) * 1000),
        )


def _request_json(
    service_url: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    timeout: float = 15.0,
) -> dict[str, Any]:
    url = service_url.rstrip("/") + path
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, method=method, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed with HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"{method} {path} failed: {exc.reason}") from exc


def _spawn_service(*, repo_root: Path, python_executable: str, host: str, port: int) -> subprocess.Popen[str]:
    command = [
        python_executable,
        str(repo_root / "scripts" / "aas_controller.py"),
        "serve",
        "--host",
        host,
        "--port",
        str(port),
        "--no-app-server",
    ]
    return subprocess.Popen(
        command,
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _stop_service(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5.0)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5.0)


def _wait_for_health(service_url: str, *, timeout_seconds: float, request_timeout: float) -> None:
    deadline = time.time() + timeout_seconds
    last_error: str | None = None
    while time.time() < deadline:
        try:
            payload = _request_json(service_url, "GET", "/api/health", timeout=request_timeout)
            if payload.get("status") == "ok":
                return
        except Exception as exc:
            last_error = str(exc)
        time.sleep(0.25)
    raise RuntimeError(f"Controller HTTP service did not become healthy in time. Last error: {last_error}")


def _find_open_port(host: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def _build_report(
    *,
    mode: str,
    service_url: str,
    task_id: str,
    checks: list[ValidationCheck] | list[dict[str, Any]],
    spawned_service: bool,
) -> dict[str, Any]:
    normalized_checks = [
        check if isinstance(check, dict) else {
            "name": check.name,
            "ok": check.ok,
            "detail": check.detail,
            "elapsed_ms": check.elapsed_ms,
            "payload_preview": check.payload_preview,
        }
        for check in checks
    ]
    return {
        "type": "CONTROLLER_FLOW_VALIDATION_REPORT",
        "mode": mode,
        "task_id": task_id,
        "service_url": service_url,
        "spawned_service": spawned_service,
        "ok": all(bool(check["ok"]) for check in normalized_checks),
        "check_count": len(normalized_checks),
        "checks": normalized_checks,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def _preview(payload: dict[str, Any]) -> str:
    text = json.dumps(payload, sort_keys=True)
    if len(text) > 320:
        return text[:320] + "..."
    return text


def _load_json_file(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
