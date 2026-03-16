from __future__ import annotations

import unittest

from tests.controller_testkit import http_json, running_fake_operator_http_server


class OperatorHttpEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self._server_context = running_fake_operator_http_server()
        self.handle = self._server_context.__enter__()

    def tearDown(self) -> None:
        self._server_context.__exit__(None, None, None)

    def test_health_and_policy_reads(self) -> None:
        status, payload = http_json(self.handle.base_url, "/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertIn("runtime_bridge", payload)

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/workflow-policy?task_id=t-9002&refresh=false",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["task_id"], "T-9002")
        self.assertEqual(payload["settings"]["dispatch_mode"], "hook_only")
        self.assertEqual(self.handle.server.controller.calls[-1]["refresh"], False)

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/audit-timeline?task_id=T-9002&limit=5",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["task_id"], "T-9002")
        self.assertEqual(payload["event_count"], 1)

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/dashboard-summary?limit_tasks=5",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["dashboard"]["task_count"], 1)
        self.assertIn("daemon", payload)

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/notifications?limit=5",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["notification_count"], 1)

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/improvement-advisories?limit=5&refresh=true&high_confidence_only=true",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["advisory_count"], 1)
        self.assertEqual(self.handle.server.controller.calls[-1]["refresh"], True)
        self.assertEqual(self.handle.server.controller.calls[-1]["high_confidence_only"], True)

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/daemon-status",
        )
        self.assertEqual(status, 200)
        self.assertFalse(payload["running"])

    def test_policy_configuration_posts(self) -> None:
        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/configure-workflow-policy",
            method="POST",
            payload={"task_id": "T-9002", "dispatch_mode": "manual", "auto_closeout": True, "monitor_enabled": False},
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["workflow_policy"]["settings"]["dispatch_mode"], "manual")
        self.assertTrue(payload["workflow_policy"]["settings"]["auto_closeout"])
        self.assertFalse(payload["workflow_policy"]["settings"]["monitor_enabled"])

    def test_retired_runtime_endpoints_return_gone(self) -> None:
        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/start-task-turn",
            method="POST",
            payload={"task_id": "T-9002", "prompt": "Summarize."},
        )
        self.assertEqual(status, 410)
        self.assertEqual(payload["error"], "RetiredControllerRuntime")
        self.assertIn("runtime_bridge", payload)

    def test_hitl_and_closeout_posts(self) -> None:
        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/start-convergence-decision",
            method="POST",
            payload={"task_id": "T-9002", "notes": ["Need explicit parent decision."]},
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["convergence_gate_record"]["convergence_status"], "READY_FOR_DECISION")
        self.assertEqual(self.handle.server.controller.calls[-1]["method"], "start_convergence_decision")

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/respond-hitl",
            method="POST",
            payload={"entry_id": "hitl-1", "response_payload": {"approved": True}},
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "RESOLVED")

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/finalize-review",
            method="POST",
            payload={
                "task_id": "T-9002",
                "verdict": "REVIEW_APPROVED",
                "summary": "Looks good.",
                "findings": [],
                "notes": ["test note"],
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["review_gate_record"]["review_status"], "REVIEW_APPROVED")

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/finalize-adversarial-review",
            method="POST",
            payload={
                "task_id": "T-9002",
                "verdict": "REVIEW_APPROVED",
                "summary": "Adversarial concerns addressed.",
                "findings": [],
                "notes": ["risk checked"],
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["adversarial_review_record"]["review_status"], "REVIEW_APPROVED")

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/finalize-convergence-decision",
            method="POST",
            payload={
                "task_id": "T-9002",
                "selected_disposition": "hybridize",
                "rationale": "Blend the strongest branches.",
                "notes": ["parent-selected"],
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["convergence_gate_record"]["selected_disposition"], "hybridize")

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/record-human-decision",
            method="POST",
            payload={"task_id": "T-9002", "operator_decision": "APPROVED", "workflow_status": "READY_FOR_CLOSEOUT"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["human_decision_record"]["operator_decision"], "APPROVED")

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/execute-closeout",
            method="POST",
            payload={"task_id": "T-9002", "validate_workspace": True},
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "CLOSEOUT_COMPLETE")
        self.assertTrue(payload["validation"]["valid"])

    def test_notification_and_daemon_posts(self) -> None:
        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/acknowledge-notification",
            method="POST",
            payload={"notification_id": "note-t-9002-pending_hitl"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["notifications"][0]["status"], "ACKNOWLEDGED")

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/acknowledge-improvement-advisory",
            method="POST",
            payload={"advisory_id": "aas5-update-controller-reliability"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["advisories"][0]["status"], "ACKNOWLEDGED")

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/daemon-start",
            method="POST",
            payload={"host": "127.0.0.1", "port": 4190},
        )
        self.assertEqual(status, 200)
        self.assertTrue(payload["running"])
        self.assertEqual(payload["port"], 4190)

        status, payload = http_json(
            self.handle.base_url,
            "/api/controller/daemon-stop",
            method="POST",
            payload={},
        )
        self.assertEqual(status, 200)
        self.assertFalse(payload["running"])


if __name__ == "__main__":
    unittest.main()
