#!/usr/bin/env python3
from __future__ import annotations

import argparse
import atexit
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Small local Atrahasis controller app for operator-facing orchestration.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve = subparsers.add_parser("serve", help="Run the local HTTP operator service and browser UI.")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=4180)
    serve.add_argument("--open", action="store_true")

    status = subparsers.add_parser("status", help="Show the latest workflow/operator/dispatch status for a task.")
    status.add_argument("task_id")

    prompt = subparsers.add_parser("prompt", help="Render the latest human review prompt for a task.")
    prompt.add_argument("task_id")

    dispatchable = subparsers.add_parser("dispatchable", help="Show next dispatchable tasks from TODO.")
    dispatchable.add_argument("--limit", type=int, default=5)

    claims = subparsers.add_parser("claims", help="Show current task claims.")
    claims.add_argument("--all", action="store_true", help="Include non-active claims.")

    workspace = subparsers.add_parser("workspace", help="Show a task workspace manifest.")
    workspace.add_argument("task_id")
    workspace.add_argument("--include-text", action="store_true")
    workspace.add_argument("--limit", type=int, default=100)

    decisions = subparsers.add_parser("decisions", help="Search or list ADR entries.")
    decisions.add_argument("--keyword")
    decisions.add_argument("--limit", type=int, default=5)
    decisions.add_argument("--include-text", action="store_true")

    search = subparsers.add_parser("search", help="Search canonical Atrahasis artifacts.")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--category")

    validate = subparsers.add_parser("validate", help="Validate one artifact against a local schema.")
    validate.add_argument("schema_name")
    validate.add_argument("artifact_path")

    run_state = subparsers.add_parser("run-state", help="Show the latest controller-owned run state for a task.")
    run_state.add_argument("task_id")

    workflow_policy = subparsers.add_parser("workflow-policy", help="Show the latest controller-enforced workflow policy state for a task.")
    workflow_policy.add_argument("task_id")
    workflow_policy.add_argument("--no-refresh", action="store_true")

    dashboard_summary = subparsers.add_parser("dashboard-summary", help="Show the repo-wide controller dashboard summary.")
    dashboard_summary.add_argument("--limit-tasks", type=int, default=25)

    notifications = subparsers.add_parser("notifications", help="Show controller-authored notifications.")
    notifications.add_argument("--all", action="store_true", help="Include resolved/acknowledged notifications.")
    notifications.add_argument("--limit", type=int, default=100)

    acknowledge_notification = subparsers.add_parser("acknowledge-notification", help="Acknowledge one controller notification.")
    acknowledge_notification.add_argument("notification_id")

    improvement_advisories = subparsers.add_parser("improvement-advisories", help="Show major AAS5 improvement advisories from the controller observer.")
    improvement_advisories.add_argument("--open-only", action="store_true")
    improvement_advisories.add_argument("--high-confidence-only", action="store_true")
    improvement_advisories.add_argument("--limit", type=int, default=50)
    improvement_advisories.add_argument("--refresh", action="store_true")

    acknowledge_improvement = subparsers.add_parser("acknowledge-improvement-advisory", help="Acknowledge one AAS5 improvement advisory.")
    acknowledge_improvement.add_argument("advisory_id")

    audit_timeline = subparsers.add_parser("audit-timeline", help="Show the controller audit timeline for a task.")
    audit_timeline.add_argument("task_id")
    audit_timeline.add_argument("--after-id", type=int, default=0)
    audit_timeline.add_argument("--limit", type=int, default=100)

    hitl_queue = subparsers.add_parser("hitl-queue", help="Show controller-owned HITL queue entries.")
    hitl_queue.add_argument("--task-id")
    hitl_queue.add_argument("--include-resolved", action="store_true")
    hitl_queue.add_argument("--limit", type=int, default=100)

    eval_policy = subparsers.add_parser("evaluate-workflow-policy", help="Recompute workflow policy, stage state, and next actions for a task.")
    eval_policy.add_argument("task_id")

    configure_policy = subparsers.add_parser("configure-workflow-policy", help="Update workflow policy settings for a task.")
    configure_policy.add_argument("task_id")
    configure_policy.add_argument("--dispatch-mode", choices=["manual", "hook_only", "auto_execute"])
    configure_policy.add_argument("--auto-closeout", choices=["true", "false"])
    configure_policy.add_argument("--monitor-enabled", choices=["true", "false"])

    recover = subparsers.add_parser("recover-state", help="Recover non-terminal controller runs and stale HITL entries.")

    monitor_cycle = subparsers.add_parser("monitor-cycle", help="Run one background monitor cycle across controller-known tasks.")
    monitor_cycle.add_argument("--task-id")

    daemon_status = subparsers.add_parser("daemon-status", help="Show detached controller daemon state.")

    daemon_start = subparsers.add_parser("daemon-start", help="Start the detached controller daemon.")
    daemon_start.add_argument("--host", default="127.0.0.1")
    daemon_start.add_argument("--port", type=int, default=4180)

    daemon_stop = subparsers.add_parser("daemon-stop", help="Stop the detached controller daemon.")

    start_convergence = subparsers.add_parser("start-convergence-decision", help="Start a convergence gate for a branch-heavy stage.")
    start_convergence.add_argument("task_id")
    start_convergence.add_argument("--note", action="append", default=[])

    respond_hitl = subparsers.add_parser("respond-hitl", help="Respond to a controller-owned HITL queue entry.")
    respond_hitl.add_argument("entry_id")
    respond_hitl.add_argument("response_json")

    record_decision = subparsers.add_parser("record-human-decision", help="Record an operator decision into workspace/runtime state.")
    record_decision.add_argument("task_id")
    record_decision.add_argument("operator_decision")
    record_decision.add_argument("--workflow-status")
    record_decision.add_argument("--constraint", action="append", default=[])
    record_decision.add_argument("--note", action="append", default=[])

    finalize_review = subparsers.add_parser("finalize-review", help="Finalize a review gate with a verdict and summary.")
    finalize_review.add_argument("task_id")
    finalize_review.add_argument("verdict")
    finalize_review.add_argument("summary")
    finalize_review.add_argument("--findings-json")
    finalize_review.add_argument("--note", action="append", default=[])

    finalize_adversarial_review = subparsers.add_parser("finalize-adversarial-review", help="Finalize an adversarial review gate with a verdict and summary.")
    finalize_adversarial_review.add_argument("task_id")
    finalize_adversarial_review.add_argument("verdict")
    finalize_adversarial_review.add_argument("summary")
    finalize_adversarial_review.add_argument("--findings-json")
    finalize_adversarial_review.add_argument("--note", action="append", default=[])

    finalize_convergence = subparsers.add_parser("finalize-convergence-decision", help="Finalize a convergence gate with a parent disposition and rationale.")
    finalize_convergence.add_argument("task_id")
    finalize_convergence.add_argument("selected_disposition")
    finalize_convergence.add_argument("rationale")
    finalize_convergence.add_argument("--note", action="append", default=[])

    create_claim = subparsers.add_parser("create-claim", help="Create a task claim using current Atrahasis conventions.")
    create_claim.add_argument("task_id")
    create_claim.add_argument("agent_name")
    create_claim.add_argument("--title")
    create_claim.add_argument("--platform", default="CODEX")
    create_claim.add_argument("--safe-zone", action="append", default=[])
    create_claim.add_argument("--pipeline-type", default="AAS")
    create_claim.add_argument("--invention-id", action="append", default=[])
    create_claim.add_argument("--target-spec", action="append", default=[])
    create_claim.add_argument("--status", default="CLAIMED")
    create_claim.add_argument("--notes", default="")

    write_handoff = subparsers.add_parser("write-handoff", help="Write a task handoff markdown file.")
    write_handoff.add_argument("task_id")
    write_handoff.add_argument("title")
    write_handoff.add_argument("platform")
    write_handoff.add_argument("pipeline_verdict")
    write_handoff.add_argument("--artifacts-json")
    write_handoff.add_argument("--notes", default="")
    write_handoff.add_argument("--applied", action="store_true")

    execute_closeout = subparsers.add_parser("execute-closeout", help="Run the controller closeout sequence for a task.")
    execute_closeout.add_argument("task_id")
    execute_closeout.add_argument("--review-json")
    execute_closeout.add_argument("--human-decision-json")
    execute_closeout.add_argument("--claim-update-json")
    execute_closeout.add_argument("--handoff-json")
    execute_closeout.add_argument("--skip-validate", action="store_true")

    run = subparsers.add_parser("run", help="Run the existing AAS pipeline manager.")
    run.add_argument("modifier")
    run.add_argument("task_id", nargs="?")
    run.add_argument("prompt", nargs="?")
    run.add_argument("--constraint", action="append", default=[])
    run.add_argument("--json-only", action="store_true")
    run.add_argument("--provider")
    run.add_argument("--agent-name")
    run.add_argument("--session-id")
    run.add_argument("--agent-type", action="append", default=[])
    run.add_argument(
        "--task-class",
        default="auto",
        choices=["auto", "canonical", "analysis", "validation", "demo"],
    )

    dispatch = subparsers.add_parser("dispatch", help="Prepare or execute a Codex child-session team.")
    dispatch.add_argument("task_id")
    dispatch.add_argument("--spawn-id", required=True)
    dispatch.add_argument("--action-label", default="spawn_program")
    dispatch.add_argument("--provider", default="codex")
    dispatch.add_argument("--agent-name")
    dispatch.add_argument("--session-id")
    dispatch.add_argument("--execute", action="store_true")
    dispatch.add_argument("--dry-run", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))

    from aas1.control_plane import AtrahasisControlPlane
    from aas1.invention_pipeline_manager import InventionPipelineManager
    from aas1.operator_controller_service import OperatorControllerService
    from aas1.operator_http_service import RetiredRuntimeManager, serve_operator_http
    from aas1.task_id_policy import TASK_ID_RE, TaskIdPolicy

    if args.command == "serve":
        return serve_operator_http(
            repo_root=repo_root,
            host=args.host,
            port=args.port,
            open_browser=args.open,
        )

    control = AtrahasisControlPlane(repo_root)
    runtime_bridge = RetiredRuntimeManager(repo_root)
    controller = OperatorControllerService(repo_root, control=control, runtime_bridge=runtime_bridge)
    atexit.register(controller.stop)

    if args.command == "status":
        print(json.dumps(control.get_task_status(task_id=args.task_id.upper()), indent=2, sort_keys=True))
        return 0
    if args.command == "prompt":
        manager = InventionPipelineManager(repo_root)
        print(manager.render_operator_prompt(task_id=args.task_id.upper()))
        return 0
    if args.command == "dispatchable":
        print(json.dumps(control.get_dispatchable_tasks(limit=args.limit), indent=2, sort_keys=True))
        return 0
    if args.command == "claims":
        print(json.dumps(control.get_task_claims(active_only=not args.all), indent=2, sort_keys=True))
        return 0
    if args.command == "workspace":
        print(
            json.dumps(
                control.get_task_workspace_manifest(
                    task_id=args.task_id.upper(),
                    include_text=args.include_text,
                    limit=args.limit,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "decisions":
        print(
            json.dumps(
                control.get_decisions(
                    keyword=args.keyword,
                    limit=args.limit,
                    include_text=args.include_text,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "search":
        print(
            json.dumps(
                control.search_canonical_artifacts(
                    query=args.query,
                    limit=args.limit,
                    category=args.category,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "validate":
        print(
            json.dumps(
                control.validate_artifact(
                    schema_name=args.schema_name,
                    artifact_path=args.artifact_path,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "run-state":
        print(json.dumps(controller.get_run_state(task_id=args.task_id.upper()), indent=2, sort_keys=True))
        return 0
    if args.command == "workflow-policy":
        print(
            json.dumps(
                controller.get_workflow_policy(task_id=args.task_id.upper(), refresh=not args.no_refresh),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "dashboard-summary":
        print(json.dumps(controller.get_dashboard_summary(limit_tasks=args.limit_tasks), indent=2, sort_keys=True))
        return 0
    if args.command == "notifications":
        print(
            json.dumps(
                controller.get_notifications(open_only=not args.all, limit=args.limit),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "acknowledge-notification":
        print(json.dumps(controller.acknowledge_notification(notification_id=args.notification_id), indent=2, sort_keys=True))
        return 0
    if args.command == "improvement-advisories":
        print(
            json.dumps(
                controller.get_improvement_advisories(
                    open_only=args.open_only,
                    high_confidence_only=args.high_confidence_only,
                    limit=args.limit,
                    refresh=args.refresh,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "acknowledge-improvement-advisory":
        print(json.dumps(controller.acknowledge_improvement_advisory(advisory_id=args.advisory_id), indent=2, sort_keys=True))
        return 0
    if args.command == "audit-timeline":
        print(
            json.dumps(
                controller.get_audit_timeline(task_id=args.task_id.upper(), after_id=args.after_id, limit=args.limit),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "hitl-queue":
        print(
            json.dumps(
                controller.get_hitl_queue(
                    task_id=args.task_id.upper() if args.task_id else None,
                    include_resolved=args.include_resolved,
                    limit=args.limit,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "evaluate-workflow-policy":
        print(
            json.dumps(
                {"task_id": args.task_id.upper(), "workflow_policy": controller.evaluate_workflow_policy(task_id=args.task_id.upper(), emit_events=True)},
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "configure-workflow-policy":
        auto_closeout = None if args.auto_closeout is None else args.auto_closeout == "true"
        monitor_enabled = None if args.monitor_enabled is None else args.monitor_enabled == "true"
        print(
            json.dumps(
                controller.configure_workflow_policy(
                    task_id=args.task_id.upper(),
                    dispatch_mode=args.dispatch_mode,
                    auto_closeout=auto_closeout,
                    monitor_enabled=monitor_enabled,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "recover-state":
        print(json.dumps(controller.recover_state(), indent=2, sort_keys=True))
        return 0
    if args.command == "monitor-cycle":
        print(
            json.dumps(
                controller.run_monitor_cycle(task_id=args.task_id.upper() if args.task_id else None),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "daemon-status":
        print(json.dumps(controller.daemon_status(), indent=2, sort_keys=True))
        return 0
    if args.command == "daemon-start":
        print(
            json.dumps(
                controller.start_daemon(
                    host=args.host,
                    port=args.port,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "daemon-stop":
        print(json.dumps(controller.stop_daemon(), indent=2, sort_keys=True))
        return 0
    if args.command == "start-convergence-decision":
        print(
            json.dumps(
                controller.start_convergence_decision(
                    task_id=args.task_id.upper(),
                    notes=args.note or None,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "respond-hitl":
        print(
            json.dumps(
                controller.respond_hitl(
                    entry_id=args.entry_id,
                    response_payload=json.loads(args.response_json),
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "record-human-decision":
        print(
            json.dumps(
                controller.record_human_decision(
                    task_id=args.task_id.upper(),
                    operator_decision=args.operator_decision,
                    workflow_status=args.workflow_status,
                    constraints=args.constraint or None,
                    notes=args.note or None,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "finalize-review":
        findings = json.loads(args.findings_json) if args.findings_json else []
        print(
            json.dumps(
                controller.finalize_review(
                    task_id=args.task_id.upper(),
                    verdict=args.verdict,
                    summary=args.summary,
                    findings=findings,
                    notes=args.note or None,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "finalize-adversarial-review":
        findings = json.loads(args.findings_json) if args.findings_json else []
        print(
            json.dumps(
                controller.finalize_adversarial_review(
                    task_id=args.task_id.upper(),
                    verdict=args.verdict,
                    summary=args.summary,
                    findings=findings,
                    notes=args.note or None,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "finalize-convergence-decision":
        print(
            json.dumps(
                controller.finalize_convergence_decision(
                    task_id=args.task_id.upper(),
                    selected_disposition=args.selected_disposition,
                    rationale=args.rationale,
                    notes=args.note or None,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "create-claim":
        print(
            json.dumps(
                controller.create_claim(
                    task_id=args.task_id.upper(),
                    title=args.title,
                    platform=args.platform,
                    agent_name=args.agent_name,
                    safe_zone_paths=args.safe_zone or None,
                    pipeline_type=args.pipeline_type,
                    invention_ids=args.invention_id or None,
                    target_specs=args.target_spec or None,
                    notes=args.notes,
                    status=args.status,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "write-handoff":
        artifacts = json.loads(args.artifacts_json) if args.artifacts_json else []
        print(
            json.dumps(
                controller.write_handoff(
                    task_id=args.task_id.upper(),
                    title=args.title,
                    platform=args.platform,
                    pipeline_verdict=args.pipeline_verdict,
                    notes=args.notes,
                    artifacts=artifacts,
                    applied=args.applied,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "execute-closeout":
        print(
            json.dumps(
                controller.execute_closeout(
                    task_id=args.task_id.upper(),
                    review=json.loads(args.review_json) if args.review_json else None,
                    human_decision=json.loads(args.human_decision_json) if args.human_decision_json else None,
                    claim_update=json.loads(args.claim_update_json) if args.claim_update_json else None,
                    handoff=json.loads(args.handoff_json) if args.handoff_json else None,
                    validate_workspace=not args.skip_validate,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "dispatch":
        manager = InventionPipelineManager(repo_root)
        payload = manager.prepare_team_dispatch(
            task_id=args.task_id.upper(),
            action_label=args.action_label,
            instruction=args.spawn_id,
            provider=args.provider,
            agent_name=args.agent_name,
            session_id=args.session_id,
            execute=args.execute,
            dry_run=args.dry_run,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        if args.execute and payload.get("status") in {"TEAM_EXECUTION_FAILED", "TEAM_EXECUTION_PARTIAL_FAILURE"}:
            return 1
        return 0

    manager = InventionPipelineManager(repo_root)
    task_policy = TaskIdPolicy(repo_root)
    raw_task_id = args.task_id
    prompt = args.prompt
    if prompt is None and raw_task_id and not TASK_ID_RE.match(raw_task_id.strip().upper()):
        prompt = raw_task_id
        raw_task_id = None
    if prompt is None:
        parser.error("A prompt is required.")

    task_id, task_class, auto_minted = task_policy.resolve(
        modifier=args.modifier,
        requested_task_id=raw_task_id,
        task_class=args.task_class,
    )
    if args.provider or args.agent_name or args.session_id:
        if not (args.provider and args.agent_name and args.session_id):
            parser.error("--provider, --agent-name, and --session-id must be supplied together")
        manager.register_backend(
            provider=args.provider,
            agent_name=args.agent_name,
            session_id=args.session_id,
            agent_types=args.agent_type,
            current_task=task_id,
        )
    result = manager.run_command(
        modifier=args.modifier,
        task_id=task_id,
        prompt=prompt,
        operator_constraints=args.constraint,
    )
    result["task_id"] = task_id
    result["task_class"] = task_class
    result["task_id_auto_minted"] = auto_minted
    if result.get("status") == "PENDING_HUMAN_REVIEW" and not args.json_only:
        rendered_prompt = manager.render_operator_prompt(task_id=task_id)
        if sys.stdout.isatty() and sys.stdin.isatty():
            print(rendered_prompt)
            return 0
        result["human_review_prompt"] = rendered_prompt
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
