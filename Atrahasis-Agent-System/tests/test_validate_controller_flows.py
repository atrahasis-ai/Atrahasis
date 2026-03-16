from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path

from tests.controller_testkit import running_fake_operator_http_server


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_controller_flows.py"


def _load_harness_module():
    spec = importlib.util.spec_from_file_location("validate_controller_flows_test_module", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidateControllerFlowsTests(unittest.TestCase):
    def test_run_offline_validation_against_fake_service(self) -> None:
        module = _load_harness_module()
        with running_fake_operator_http_server() as handle:
            report = module.run_offline_validation(
                service_url=handle.base_url,
                task_id="T-9002",
                request_timeout=5.0,
                spawned_service=False,
            )
        self.assertTrue(report["ok"])
        self.assertGreaterEqual(report["check_count"], 8)
        self.assertEqual(report["task_id"], "T-9002")

    def test_main_offline_uses_existing_service_and_writes_report(self) -> None:
        module = _load_harness_module()
        report_path = REPO_ROOT / "tests" / "controller-report.json"
        if report_path.exists():
            report_path.unlink()
        with running_fake_operator_http_server() as handle:
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                rc = module.main(
                    [
                        "offline",
                        "--service-url",
                        handle.base_url,
                        "--task-id",
                        "T-9002",
                        "--report-path",
                        str(report_path),
                    ]
                )
            raw_output = stdout.getvalue()
            payload = json.loads(raw_output[raw_output.find("{"):])
            written = json.loads(report_path.read_text(encoding="utf-8"))
            report_exists = report_path.exists()
        report_path.unlink(missing_ok=True)
        self.assertEqual(rc, 0)
        self.assertTrue(payload["ok"])
        self.assertTrue(report_exists)
        self.assertEqual(written["task_id"], "T-9002")


if __name__ == "__main__":
    unittest.main()
