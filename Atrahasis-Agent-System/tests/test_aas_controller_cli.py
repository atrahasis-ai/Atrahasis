from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import sys
import types
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "aas_controller.py"


class CliRecorder:
    def __init__(self) -> None:
        self.serve_calls: list[dict[str, object]] = []
        self.control_calls: list[dict[str, object]] = []
        self.controller_calls: list[dict[str, object]] = []


def _load_cli_module():
    spec = importlib.util.spec_from_file_location("aas_controller_test_module", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@contextlib.contextmanager
def _stubbed_aas1_modules(recorder: CliRecorder):
    original_modules = {name: sys.modules.get(name) for name in list(sys.modules) if name == "aas1" or name.startswith("aas1.")}

    aas1_pkg = types.ModuleType("aas1")
    aas1_pkg.__path__ = []  # type: ignore[attr-defined]

    class FakeControlPlane:
        def __init__(self, repo_root: Path) -> None:
            self.repo_root = repo_root

        def get_dispatchable_tasks(self, *, limit: int = 5) -> dict[str, object]:
            recorder.control_calls.append({"method": "get_dispatchable_tasks", "limit": limit})
            return {"tasks": [{"task_id": "T-9002"}], "next_dispatchable_canonical_task": "T-9002"}

    class FakeRetiredRuntimeManager:
        def __init__(self, repo_root: Path) -> None:
            self.repo_root = repo_root

    class FakeControllerService:
        def __init__(self, repo_root: Path, control: object, runtime_bridge: object) -> None:
            self.repo_root = repo_root
            self.control = control
            self.runtime_bridge = runtime_bridge

        def stop(self) -> None:
            recorder.controller_calls.append({"method": "stop"})

        def get_workflow_policy(self, *, task_id: str, refresh: bool = True) -> dict[str, object]:
            recorder.controller_calls.append({"method": "get_workflow_policy", "task_id": task_id, "refresh": refresh})
            return {"task_id": task_id, "current_stage": "RESEARCH", "settings": {"dispatch_mode": "hook_only"}}

        def get_dashboard_summary(self, *, limit_tasks: int = 25) -> dict[str, object]:
            recorder.controller_calls.append({"method": "get_dashboard_summary", "limit_tasks": limit_tasks})
            return {"dashboard": {"task_count": 1}, "notifications": [], "daemon": {"running": False}}

        def get_notifications(self, *, open_only: bool = True, limit: int = 100) -> dict[str, object]:
            recorder.controller_calls.append({"method": "get_notifications", "open_only": open_only, "limit": limit})
            return {"notification_count": 1, "notifications": [{"notification_id": "note-1", "status": "OPEN"}]}

        def acknowledge_notification(self, *, notification_id: str) -> dict[str, object]:
            recorder.controller_calls.append({"method": "acknowledge_notification", "notification_id": notification_id})
            return {"notification_count": 1, "notifications": [{"notification_id": notification_id, "status": "ACKNOWLEDGED"}]}

        def get_improvement_advisories(
            self,
            *,
            open_only: bool = False,
            high_confidence_only: bool = False,
            limit: int = 50,
            refresh: bool = False,
        ) -> dict[str, object]:
            recorder.controller_calls.append(
                {
                    "method": "get_improvement_advisories",
                    "open_only": open_only,
                    "high_confidence_only": high_confidence_only,
                    "limit": limit,
                    "refresh": refresh,
                }
            )
            advisories = [
                {
                    "advisory_id": "aas5-update-controller-reliability",
                    "headline": "Controller reliability hardening is warranted.",
                    "status": "OPEN",
                }
            ]
            return {"advisory_count": len(advisories), "advisories": advisories}

        def acknowledge_improvement_advisory(self, *, advisory_id: str) -> dict[str, object]:
            recorder.controller_calls.append({"method": "acknowledge_improvement_advisory", "advisory_id": advisory_id})
            return {"advisories": [{"advisory_id": advisory_id, "status": "ACKNOWLEDGED"}]}

        def daemon_status(self) -> dict[str, object]:
            recorder.controller_calls.append({"method": "daemon_status"})
            return {"running": False, "pid": None}

        def start_daemon(
            self,
            *,
            host: str = "127.0.0.1",
            port: int = 4180,
        ) -> dict[str, object]:
            recorder.controller_calls.append(
                {
                    "method": "start_daemon",
                    "host": host,
                    "port": port,
                }
            )
            return {"running": True, "pid": 5150, "port": port}

        def stop_daemon(self) -> dict[str, object]:
            recorder.controller_calls.append({"method": "stop_daemon"})
            return {"running": False, "pid": None}

        def run_monitor_cycle(self, *, task_id: str | None = None) -> dict[str, object]:
            recorder.controller_calls.append({"method": "run_monitor_cycle", "task_id": task_id})
            return {"task_ids": [task_id] if task_id else ["T-9002"]}

        def start_convergence_decision(
            self,
            *,
            task_id: str,
            notes: list[str] | None = None,
        ) -> dict[str, object]:
            recorder.controller_calls.append(
                {
                    "method": "start_convergence_decision",
                    "task_id": task_id,
                    "notes": notes,
                }
            )
            return {"task_id": task_id, "convergence_gate_record": {"convergence_status": "READY_FOR_DECISION", "notes": notes or []}}

        def finalize_adversarial_review(
            self,
            *,
            task_id: str,
            verdict: str,
            summary: str,
            findings: list[object],
            notes: list[str] | None = None,
        ) -> dict[str, object]:
            recorder.controller_calls.append(
                {
                    "method": "finalize_adversarial_review",
                    "task_id": task_id,
                    "verdict": verdict,
                    "summary": summary,
                    "findings": findings,
                    "notes": notes,
                }
            )
            return {"task_id": task_id, "adversarial_review_record": {"review_status": verdict, "summary": summary}}

        def finalize_convergence_decision(
            self,
            *,
            task_id: str,
            selected_disposition: str,
            rationale: str,
            notes: list[str] | None = None,
        ) -> dict[str, object]:
            recorder.controller_calls.append(
                {
                    "method": "finalize_convergence_decision",
                    "task_id": task_id,
                    "selected_disposition": selected_disposition,
                    "rationale": rationale,
                    "notes": notes,
                }
            )
            return {
                "task_id": task_id,
                "convergence_gate_record": {
                    "selected_disposition": selected_disposition,
                    "rationale": rationale,
                },
            }

    class FakePipelineManager:
        def __init__(self, repo_root: Path) -> None:
            self.repo_root = repo_root

    class FakeTaskIdPolicy:
        def __init__(self, repo_root: Path) -> None:
            self.repo_root = repo_root

        def resolve(self, *, modifier: str, requested_task_id: str | None, task_class: str):
            return requested_task_id or "T-9002", task_class, False

    def fake_serve_operator_http(**kwargs):
        recorder.serve_calls.append(kwargs)
        return 0

    control_plane_module = types.ModuleType("aas1.control_plane")
    control_plane_module.AtrahasisControlPlane = FakeControlPlane

    controller_module = types.ModuleType("aas1.operator_controller_service")
    controller_module.OperatorControllerService = FakeControllerService

    http_module = types.ModuleType("aas1.operator_http_service")
    http_module.serve_operator_http = fake_serve_operator_http
    http_module.RetiredRuntimeManager = FakeRetiredRuntimeManager

    pipeline_module = types.ModuleType("aas1.invention_pipeline_manager")
    pipeline_module.InventionPipelineManager = FakePipelineManager

    task_policy_module = types.ModuleType("aas1.task_id_policy")
    task_policy_module.TaskIdPolicy = FakeTaskIdPolicy
    task_policy_module.TASK_ID_RE = re.compile(r"^T-[A-Z0-9-]+$", re.IGNORECASE)

    sys.modules["aas1"] = aas1_pkg
    sys.modules["aas1.control_plane"] = control_plane_module
    sys.modules["aas1.operator_controller_service"] = controller_module
    sys.modules["aas1.operator_http_service"] = http_module
    sys.modules["aas1.invention_pipeline_manager"] = pipeline_module
    sys.modules["aas1.task_id_policy"] = task_policy_module
    try:
        yield
    finally:
        for name in ["aas1", "aas1.control_plane", "aas1.operator_controller_service", "aas1.operator_http_service", "aas1.invention_pipeline_manager", "aas1.task_id_policy"]:
            if name in original_modules and original_modules[name] is not None:
                sys.modules[name] = original_modules[name]
            else:
                sys.modules.pop(name, None)


def _run_main(argv: list[str], recorder: CliRecorder) -> tuple[int, str]:
    module = _load_cli_module()
    stdout = io.StringIO()
    with _stubbed_aas1_modules(recorder), contextlib.redirect_stdout(stdout):
        original_argv = sys.argv
        try:
            sys.argv = ["aas_controller.py", *argv]
            result = module.main()
        finally:
            sys.argv = original_argv
    return int(result), stdout.getvalue()


class AasControllerCliTests(unittest.TestCase):
    def test_parser_includes_new_controller_commands(self) -> None:
        module = _load_cli_module()
        parser = module.build_parser()
        args = parser.parse_args(["workflow-policy", "T-9002", "--no-refresh"])
        self.assertEqual(args.command, "workflow-policy")
        self.assertTrue(args.no_refresh)

        args = parser.parse_args(["monitor-cycle", "--task-id", "T-9002"])
        self.assertEqual(args.command, "monitor-cycle")
        self.assertEqual(args.task_id, "T-9002")

    def test_serve_delegates_to_http_service(self) -> None:
        recorder = CliRecorder()
        rc, _stdout = _run_main(["serve", "--host", "127.0.0.1", "--port", "4191"], recorder)
        self.assertEqual(rc, 0)
        self.assertEqual(len(recorder.serve_calls), 1)
        self.assertEqual(recorder.serve_calls[0]["host"], "127.0.0.1")
        self.assertEqual(recorder.serve_calls[0]["port"], 4191)

    def test_dispatchable_command_prints_json(self) -> None:
        recorder = CliRecorder()
        rc, stdout = _run_main(["dispatchable", "--limit", "3"], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["next_dispatchable_canonical_task"], "T-9002")
        self.assertEqual(recorder.control_calls[-1]["limit"], 3)

    def test_workflow_policy_command(self) -> None:
        recorder = CliRecorder()
        rc, stdout = _run_main(["workflow-policy", "T-9002", "--no-refresh"], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["task_id"], "T-9002")
        self.assertFalse(recorder.controller_calls[-1]["refresh"])

    def test_dashboard_notification_and_controller_commands(self) -> None:
        recorder = CliRecorder()

        rc, stdout = _run_main(["dashboard-summary", "--limit-tasks", "5"], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["dashboard"]["task_count"], 1)
        self.assertEqual(recorder.controller_calls[-1]["limit_tasks"], 5)

        rc, stdout = _run_main(["notifications", "--all", "--limit", "5"], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["notification_count"], 1)
        self.assertFalse(recorder.controller_calls[-1]["open_only"])

        rc, stdout = _run_main(["improvement-advisories", "--open-only", "--high-confidence-only", "--limit", "5", "--refresh"], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["advisory_count"], 1)
        self.assertTrue(recorder.controller_calls[-1]["refresh"])
        self.assertTrue(recorder.controller_calls[-1]["high_confidence_only"])

        rc, stdout = _run_main(["acknowledge-improvement-advisory", "aas5-update-controller-reliability"], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["advisories"][0]["status"], "ACKNOWLEDGED")

        rc, stdout = _run_main(["finalize-adversarial-review", "T-9002", "REVIEW_APPROVED", "Risk checked."], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["adversarial_review_record"]["review_status"], "REVIEW_APPROVED")

        rc, stdout = _run_main(["start-convergence-decision", "T-9002", "--note", "Need explicit disposition."], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["convergence_gate_record"]["convergence_status"], "READY_FOR_DECISION")
        self.assertEqual(recorder.controller_calls[-1]["method"], "start_convergence_decision")

        rc, stdout = _run_main(["finalize-convergence-decision", "T-9002", "hybridize", "Blend Alpha and Beta."], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertEqual(payload["convergence_gate_record"]["selected_disposition"], "hybridize")

        rc, stdout = _run_main(["daemon-start", "--port", "4190"], recorder)
        self.assertEqual(rc, 0)
        payload = json.loads(stdout)
        self.assertTrue(payload["running"])
        self.assertEqual(payload["port"], 4190)


if __name__ == "__main__":
    unittest.main()
