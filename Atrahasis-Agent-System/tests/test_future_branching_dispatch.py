from __future__ import annotations

import json
import shutil
import sys
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from aas1.artifact_registry import ArtifactRegistry
from aas1.codex_team_dispatcher import CodexTeamDispatcher
from aas1.dispatch_merge_engine import DispatchMergeEngine
from aas1.redesign_memory_store import RedesignMemoryStore
from aas1.swarm_validation import validate_swarm_execution_task
from aas1.workflow_policy_engine import WorkflowPolicyEngine


SCHEMA_NAMES = [
    "adversarial_review_record",
    "team_plan",
    "future_branch_report",
    "team_dispatch_record",
    "child_agent_result",
    "child_result_merge_package",
    "swarm_execution_record",
    "human_decision_record",
    "lane_plan",
    "lane_convergence_report",
    "aas5_audit_record",
    "swarm_topology_graph",
    "execution_parallelism_record",
    "future_convergence_report",
    "task_improvement_report",
    "radical_redesign_report",
    "convergence_gate_record",
]


class FakeProviderRuntime:
    def resolve_model_route(self, provider: str, agent_type: str) -> dict[str, str]:
        return {
            "tier": "primary",
            "model": "gpt-5.4",
            "reasoning_effort": "high",
        }

    def list_active_sessions(self) -> list[dict[str, str]]:
        return []


class FutureBranchingDispatchTests(unittest.TestCase):
    def setUp(self) -> None:
        temp_parent = Path.home() / ".codex" / "memories" / "future_branching_tests"
        temp_parent.mkdir(parents=True, exist_ok=True)
        self.tempdir = temp_parent / f"localtmp_future_{uuid.uuid4().hex}"
        self.repo_root = self.tempdir / "Atrahasis-Agent-System"
        (self.repo_root / "docs" / "schemas").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "docs" / "task_workspaces" / "T-9002").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "runtime" / "state").mkdir(parents=True, exist_ok=True)
        self._copy_schemas()
        self._write_todo()

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_workflow_policy_prefers_future_swarm_for_analysis_research(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        state = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASA", "scope": "architecture_question"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        primary = state["dispatch"]["primary"]
        self.assertEqual(primary["action_label"], "explore_futures")
        self.assertEqual(primary["team_mode"], "FUTURE_BRANCH_SWARM")
        self.assertEqual(len(primary["future_exploration"]["branches"]), 9)
        improvement_policy = primary["future_exploration"]["improvement_trigger_policy"]
        self.assertTrue(improvement_policy["enabled"])
        self.assertIn("task_class_has_design_surface", improvement_policy["trigger_reasons"])
        self.assertEqual(set(improvement_policy["decision_options"]), {"reject", "adopt", "hybridize", "escalate_to_hitl"})
        self.assertEqual(improvement_policy["lane_order"], ["alpha", "beta", "gamma"])
        self.assertEqual(set(improvement_policy["lane_ids"]), {"alpha", "beta", "gamma"})
        radical_policy = primary["future_exploration"]["radical_trigger_policy"]
        self.assertTrue(radical_policy["enabled"])
        self.assertIn("task_class_requires_architecture_pressure", radical_policy["trigger_reasons"])
        self.assertEqual(set(radical_policy["decision_options"]), {"reject", "hybridize", "promote"})
        self.assertEqual(len(radical_policy["radical_branch_ids"]), 3)

    def test_workflow_policy_defaults_full_pipeline_ideation_to_four_lane_future_swarm(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        state = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASNI", "scope": "new_idea_integration"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        primary = state["dispatch"]["primary"]
        self.assertEqual(primary["action_label"], "explore_futures")
        self.assertEqual(primary["team_mode"], "FUTURE_BRANCH_SWARM")
        self.assertEqual(primary["future_exploration"]["current_stage"], "IDEATION")
        self.assertEqual(len(primary["future_exploration"]["branches"]), 12)
        improvement_policy = primary["future_exploration"]["improvement_trigger_policy"]
        self.assertEqual(improvement_policy["lane_order"], ["alpha", "beta", "gamma", "radical"])
        self.assertEqual(set(improvement_policy["lane_ids"]), {"alpha", "beta", "gamma", "radical"})
        radical_policy = primary["future_exploration"]["radical_trigger_policy"]
        self.assertIn("visionary:frame_replacement", set(radical_policy["radical_branch_ids"]))
        self.assertIn("systems_thinker:authority_reset", set(radical_policy["radical_branch_ids"]))
        self.assertIn("critic:foundational_invalidity", set(radical_policy["radical_branch_ids"]))

    def test_prepare_dispatch_materializes_future_branch_team_plan(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASA", "scope": "architecture_question"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        registry = ArtifactRegistry(self.repo_root)
        dispatcher = CodexTeamDispatcher(
            self.repo_root,
            artifact_registry=registry,
            provider_runtime=FakeProviderRuntime(),
            operator_sessions=None,
            context_store=None,
        )
        payload = dispatcher.prepare_dispatch(
            task_id="T-9002",
            workflow_id="wf-1",
            human_record={},
            recommendations={"dispatch_candidates": []},
            action_label="explore_futures",
            instruction="future_swarm:research",
            dry_run=False,
        )
        branch_report_path = self.repo_root / "docs" / "task_workspaces" / "T-9002" / "FUTURE_BRANCH_REPORT.json"
        branch_report = json.loads(branch_report_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["spawn_policy"]["team_mode"], "FUTURE_BRANCH_SWARM")
        self.assertTrue(payload["future_exploration"]["enabled"])
        self.assertTrue(payload["future_exploration"]["improvement_trigger_policy"]["enabled"])
        self.assertTrue(payload["future_exploration"]["radical_trigger_policy"]["enabled"])
        self.assertEqual(len(payload["children"]), 9)
        self.assertEqual(len(branch_report["branches"]), 9)
        self.assertEqual(branch_report["current_stage"], "RESEARCH")
        self.assertTrue(branch_report["improvement_trigger_policy"]["enabled"])
        self.assertTrue(branch_report["radical_trigger_policy"]["enabled"])
        self.assertEqual(
            {item["lane_id"] for item in branch_report["branches"]},
            {"alpha", "beta", "gamma"},
        )
        self.assertEqual(
            len([item for item in branch_report["branches"] if item["radical_candidate"]]),
            3,
        )

    def test_prepare_dispatch_materializes_four_lane_ideation_swarm(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        state = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASNI", "scope": "new_idea_integration"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        primary = state["dispatch"]["primary"]
        registry = ArtifactRegistry(self.repo_root)
        dispatcher = CodexTeamDispatcher(
            self.repo_root,
            artifact_registry=registry,
            provider_runtime=FakeProviderRuntime(),
            operator_sessions=None,
            context_store=None,
        )
        payload = dispatcher.prepare_dispatch(
            task_id="T-9002",
            workflow_id="wf-ideation",
            human_record={},
            recommendations={"dispatch_candidates": []},
            action_label=primary["action_label"],
            instruction=primary["instruction"],
            dry_run=False,
        )
        branch_report_path = self.repo_root / "docs" / "task_workspaces" / "T-9002" / "FUTURE_BRANCH_REPORT.json"
        branch_report = json.loads(branch_report_path.read_text(encoding="utf-8"))
        worker_children = [item for item in payload["children"] if item["tier"] == "lane_worker"]
        self.assertEqual(primary["instruction"], "future_swarm:ideation")
        self.assertEqual(payload["doctrine_version"], "AAS5")
        self.assertEqual(payload["topology_mode"], "AAS5_25_AGENT_HIERARCHY")
        self.assertEqual(len(payload["children"]), 24)
        self.assertEqual(payload["spawn_policy"]["orchestration_topology"], "master_lane_managers_reporters_auditors")
        self.assertEqual(payload["spawn_policy"]["manager_count"], 4)
        self.assertEqual(payload["spawn_policy"]["reporter_count"], 4)
        self.assertEqual(payload["spawn_policy"]["auditor_count"], 4)
        self.assertEqual(payload["spawn_policy"]["worker_count"], 12)
        self.assertEqual(payload["spawn_policy"]["max_live_children"], 6)
        self.assertEqual(payload["spawn_policy"]["spawn_batch_size"], 6)
        self.assertEqual(payload["spawn_policy"]["planned_wave_count"], 5)
        self.assertEqual(payload["spawn_policy"]["scheduling_mode"], "batched_by_runtime_cap")
        self.assertEqual(len(payload["manager_orchestrators"]), 4)
        self.assertEqual(len(payload["lane_convergence_reporters"]), 4)
        self.assertEqual(len(payload["audit_orchestrators"]), 4)
        self.assertEqual(len(payload["workers"]), 12)
        self.assertTrue(all(item["managed_child_count"] == 3 for item in payload["manager_orchestrators"]))
        self.assertEqual(branch_report["doctrine_version"], "AAS5")
        self.assertEqual(len(branch_report["lane_summaries"]), 4)
        self.assertEqual(len(branch_report["branches"]), 12)
        self.assertEqual({item["lane_id"] for item in branch_report["branches"]}, {"alpha", "beta", "gamma", "radical"})
        self.assertEqual(len(worker_children), 12)
        self.assertTrue(all(item["manager_id"] for item in worker_children))
        self.assertTrue(any(item["branch_id"] == "visionary:frame_replacement" for item in worker_children))
        self.assertTrue(any(item["branch_id"] == "systems_thinker:authority_reset" for item in worker_children))
        self.assertTrue(any(item["branch_id"] == "critic:foundational_invalidity" for item in worker_children))

    def test_merge_engine_authorizes_ideation_after_complete_validated_swarm(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        state = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASNI", "scope": "new_idea_integration"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        primary = state["dispatch"]["primary"]
        registry = ArtifactRegistry(self.repo_root)
        dispatcher = CodexTeamDispatcher(
            self.repo_root,
            artifact_registry=registry,
            provider_runtime=FakeProviderRuntime(),
            operator_sessions=None,
            context_store=None,
        )
        team_plan = dispatcher.prepare_dispatch(
            task_id="T-9002",
            workflow_id="wf-ideation",
            human_record={},
            recommendations={"dispatch_candidates": []},
            action_label=primary["action_label"],
            instruction=primary["instruction"],
            parent_agent_name="Sin",
            parent_session_id="parent-session-1",
            dry_run=False,
        )
        (self.repo_root / "docs" / "task_workspaces" / "T-9002" / "HUMAN_DECISION_RECORD.json").write_text(
            json.dumps(
                {
                    "operator_decision": "ACK_DEGRADED_AAS5",
                    "degraded_mode_acknowledged": True,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        dispatch_children = []
        for index, child in enumerate(team_plan["children"], start=1):
            payload = {
                "type": "CHILD_AGENT_RESULT",
                "doctrine_version": "AAS5",
                "task_id": "T-9002",
                "workflow_id": "wf-ideation",
                "run_key": team_plan["run_key"],
                "node_id": child["node_id"],
                "parent_node_id": child.get("parent_node_id"),
                "role": child["role"],
                "role_label": child.get("role_label"),
                "objective": child["objective"],
                "status": "COMPLETED",
                "session_identity": {
                    "agent_name": child["agent_name"],
                    "session_id": f"child-session-{index}",
                    "provider": "codex",
                    "role": child["role"],
                    "node_id": child["node_id"],
                },
                "model_audit": {
                    "requested_model": child["model"],
                    "requested_reasoning_effort": child["reasoning_effort"],
                    "observed_runtime_model": child["model"],
                    "observed_model_auditability": "verified_exact",
                    "routing_basis": "Synthetic ideation child result for validator-backed merge testing.",
                    "policy_target": child["model"],
                    "actual_runtime_model": child["model"],
                    "reasoning_effort": child["reasoning_effort"],
                    "auditability": "verified_exact",
                },
                "artifact_provenance": {
                    "writer_mode": "parent_proxy",
                    "writer_agent_name": "Sin",
                    "writer_session_id": "parent-session-1",
                    "writer_node_id": "mst",
                    "owner_node_id": child["node_id"],
                    "notes": ["Synthetic ideation child artifact."],
                },
                "verdict": f"{child.get('role_label') or child['role']} is coherent under current authority.",
                "evidence": [{"path": "docs/TODO.md", "note": "Synthetic ideation evidence."}],
                "recommended_next_action": "Merge into the parent ideation synthesis.",
            }
            for field in ("branch_id", "branch_label", "parent_role", "branch_kind", "lane_id", "lane_label", "lane_strategy", "audit_domain"):
                if child.get(field) is not None:
                    payload[field] = child.get(field)
            registry.write_json_artifact("T-9002", child["expected_artifact"], payload, schema_name="child_agent_result")
            dispatch_child = {
                "node_id": child["node_id"],
                "parent_node_id": child.get("parent_node_id"),
                "child_id": child.get("child_id"),
                "role": child["role"],
                "role_label": child.get("role_label"),
                "status": "COMPLETED",
                "model": child["model"],
                "reasoning_effort": child["reasoning_effort"],
                "permission": child["permission"],
                "output_artifact": f"docs/task_workspaces/T-9002/{child['expected_artifact']}",
                "session_id": f"child-session-{index}",
                "session_log": None,
                "return_code": 0,
                "stdout_log": "stdout.log",
                "stderr_log": "stderr.log",
            }
            for field in ("branch_id", "branch_label", "parent_role", "branch_kind", "lane_id", "lane_label", "lane_strategy", "audit_domain"):
                if child.get(field) is not None:
                    dispatch_child[field] = child.get(field)
            dispatch_children.append(dispatch_child)

        registry.write_json_artifact(
            "T-9002",
            "TEAM_DISPATCH_RECORD.json",
            {
                "type": "TEAM_DISPATCH_RECORD",
                "doctrine_version": team_plan["doctrine_version"],
                "topology_mode": team_plan["topology_mode"],
                "task_id": "T-9002",
                "workflow_id": "wf-ideation",
                "run_key": team_plan["run_key"],
                "dispatch_id": team_plan["dispatch_id"],
                "status": "TEAM_EXECUTION_COMPLETED",
                "execution_mode": "codex_exec_sequential",
                "selection": dict(team_plan["selection"]),
                "team_plan_ref": "docs/task_workspaces/T-9002/TEAM_PLAN.yaml",
                "future_exploration": {
                    "enabled": True,
                    "current_stage": "IDEATION",
                    "branch_count": len(team_plan["future_exploration"]["branches"]),
                    "convergence_artifact": "docs/task_workspaces/T-9002/FUTURE_CONVERGENCE_REPORT.json",
                    "improvement_trigger_policy": team_plan["future_exploration"]["improvement_trigger_policy"],
                    "radical_trigger_policy": team_plan["future_exploration"]["radical_trigger_policy"],
                },
                "children": dispatch_children,
                "created_at": team_plan["created_at"],
                "updated_at": team_plan["updated_at"],
            },
            schema_name="team_dispatch_record",
        )

        merge_engine = DispatchMergeEngine(self.repo_root, artifact_registry=registry)
        result = merge_engine.build_for_task(task_id="T-9002")
        merge_package = json.loads(
            (self.repo_root / "docs" / "task_workspaces" / "T-9002" / "CHILD_RESULT_MERGE_PACKAGE.json").read_text(
                encoding="utf-8"
            )
        )
        future_branch_report = json.loads(
            (self.repo_root / "docs" / "task_workspaces" / "T-9002" / "FUTURE_BRANCH_REPORT.json").read_text(
                encoding="utf-8"
            )
        )
        swarm_record = json.loads(
            (self.repo_root / "docs" / "task_workspaces" / "T-9002" / "SWARM_EXECUTION_RECORD.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(result["merge_package"]["validation_status"], "PASSED")
        self.assertTrue(merge_package["merge_ready"])
        self.assertEqual(merge_package["validation_status"], "PASSED")
        self.assertTrue(future_branch_report["recommendation_authorized"])
        self.assertTrue(all(item["status"] == "COMPLETED" for item in future_branch_report["branches"]))
        self.assertEqual(swarm_record["execution_mode"], "REAL_SWARM")
        self.assertTrue(swarm_record["recommendation_authorized"])
        self.assertEqual(validate_swarm_execution_task(repo_root=self.repo_root, task_id="T-9002"), [])

    def test_merge_engine_builds_future_convergence_report(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASA", "scope": "architecture_question"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        registry = ArtifactRegistry(self.repo_root)
        dispatcher = CodexTeamDispatcher(
            self.repo_root,
            artifact_registry=registry,
            provider_runtime=FakeProviderRuntime(),
            operator_sessions=None,
            context_store=None,
        )
        team_plan = dispatcher.prepare_dispatch(
            task_id="T-9002",
            workflow_id="wf-1",
            human_record={},
            recommendations={"dispatch_candidates": []},
            action_label="explore_futures",
            instruction="future_swarm:research",
            dry_run=False,
        )
        first_child = next(child for child in team_plan["children"] if child["branch_kind"] == "conservative")
        second_child = next(child for child in team_plan["children"] if child["branch_kind"] == "radical")
        registry.write_json_artifact(
            "T-9002",
            first_child["expected_artifact"],
            {
                "type": "CHILD_AGENT_RESULT",
                "task_id": "T-9002",
                "role": first_child["role"],
                "objective": first_child["objective"],
                "status": "COMPLETED",
                "session_identity": {
                    "agent_name": first_child["agent_name"],
                    "session_id": "child-session-1",
                    "provider": "codex",
                    "role": first_child["role"],
                },
                "model_audit": {
                    "policy_target": first_child["model"],
                    "actual_runtime_model": first_child["model"],
                    "reasoning_effort": first_child["reasoning_effort"],
                    "auditability": "runtime_exposed",
                    "routing_basis": "Synthetic test child result.",
                },
                "artifact_provenance": {
                    "writer_mode": "parent_proxy",
                    "writer_agent_name": "test-parent",
                    "writer_session_id": "parent-session-1",
                    "notes": ["Synthetic test child artifact."],
                },
                "branch_id": first_child["branch_id"],
                "branch_label": first_child["branch_label"],
                "parent_role": first_child["parent_role"],
                "branch_kind": first_child["branch_kind"],
                "lane_id": first_child["lane_id"],
                "lane_label": first_child["lane_label"],
                "lane_strategy": first_child["lane_strategy"],
                "verdict": "Conservative future is viable.",
                "evidence": [{"path": "docs/TODO.md", "note": "Used as synthetic evidence."}],
                "recommended_next_action": "Compare against the other futures before converging.",
            },
            schema_name="child_agent_result",
        )
        registry.write_json_artifact(
            "T-9002",
            second_child["expected_artifact"],
            {
                "type": "CHILD_AGENT_RESULT",
                "task_id": "T-9002",
                "role": second_child["role"],
                "objective": second_child["objective"],
                "status": "COMPLETED",
                "session_identity": {
                    "agent_name": second_child["agent_name"],
                    "session_id": "child-session-2",
                    "provider": "codex",
                    "role": second_child["role"],
                },
                "model_audit": {
                    "policy_target": second_child["model"],
                    "actual_runtime_model": second_child["model"],
                    "reasoning_effort": second_child["reasoning_effort"],
                    "auditability": "runtime_exposed",
                    "routing_basis": "Synthetic test child result.",
                },
                "artifact_provenance": {
                    "writer_mode": "parent_proxy",
                    "writer_agent_name": "test-parent",
                    "writer_session_id": "parent-session-1",
                    "notes": ["Synthetic test child artifact."],
                },
                "branch_id": second_child["branch_id"],
                "branch_label": second_child["branch_label"],
                "parent_role": second_child["parent_role"],
                "branch_kind": second_child["branch_kind"],
                "lane_id": second_child["lane_id"],
                "lane_label": second_child["lane_label"],
                "lane_strategy": second_child["lane_strategy"],
                "verdict": "Aggressive future increases upside with higher risk.",
                "evidence": [{"path": "docs/TODO.md", "note": "Used as synthetic evidence."}],
                "recommended_next_action": "Compare against the other futures before converging.",
            },
            schema_name="child_agent_result",
        )
        registry.write_json_artifact(
            "T-9002",
            "TEAM_DISPATCH_RECORD.json",
            {
                "type": "TEAM_DISPATCH_RECORD",
                "task_id": "T-9002",
                "workflow_id": "wf-1",
                "dispatch_id": team_plan["dispatch_id"],
                "status": "TEAM_EXECUTION_COMPLETED",
                "execution_mode": "codex_exec_sequential",
                "selection": dict(team_plan["selection"]),
                "team_plan_ref": "docs/task_workspaces/T-9002/TEAM_PLAN.yaml",
                "future_exploration": {
                    "enabled": True,
                    "current_stage": "RESEARCH",
                    "branch_count": len(team_plan["future_exploration"]["branches"]),
                    "convergence_artifact": "docs/task_workspaces/T-9002/FUTURE_CONVERGENCE_REPORT.json",
                    "improvement_trigger_policy": team_plan["future_exploration"]["improvement_trigger_policy"],
                    "radical_trigger_policy": team_plan["future_exploration"]["radical_trigger_policy"],
                },
                "children": [
                    {
                        "child_id": first_child["child_id"],
                        "role": first_child["role"],
                        "status": "COMPLETED",
                        "model": first_child["model"],
                        "reasoning_effort": first_child["reasoning_effort"],
                        "permission": first_child["permission"],
                        "branch_id": first_child["branch_id"],
                        "branch_label": first_child["branch_label"],
                        "parent_role": first_child["parent_role"],
                        "branch_kind": first_child["branch_kind"],
                        "lane_id": first_child["lane_id"],
                        "lane_label": first_child["lane_label"],
                        "lane_strategy": first_child["lane_strategy"],
                        "output_artifact": f"docs/task_workspaces/T-9002/{first_child['expected_artifact']}",
                        "session_id": None,
                        "session_log": None,
                        "return_code": 0,
                        "stdout_log": "stdout.log",
                        "stderr_log": "stderr.log",
                    },
                    {
                        "child_id": second_child["child_id"],
                        "role": second_child["role"],
                        "status": "COMPLETED",
                        "model": second_child["model"],
                        "reasoning_effort": second_child["reasoning_effort"],
                        "permission": second_child["permission"],
                        "branch_id": second_child["branch_id"],
                        "branch_label": second_child["branch_label"],
                        "parent_role": second_child["parent_role"],
                        "branch_kind": second_child["branch_kind"],
                        "lane_id": second_child["lane_id"],
                        "lane_label": second_child["lane_label"],
                        "lane_strategy": second_child["lane_strategy"],
                        "output_artifact": f"docs/task_workspaces/T-9002/{second_child['expected_artifact']}",
                        "session_id": None,
                        "session_log": None,
                        "return_code": 0,
                        "stdout_log": "stdout.log",
                        "stderr_log": "stderr.log",
                    },
                ],
                "created_at": team_plan["created_at"],
                "updated_at": team_plan["updated_at"],
            },
            schema_name="team_dispatch_record",
        )
        engine = DispatchMergeEngine(self.repo_root, artifact_registry=registry)
        result = engine.build_for_task(task_id="T-9002")
        convergence_path = self.repo_root / "docs" / "task_workspaces" / "T-9002" / "FUTURE_CONVERGENCE_REPORT.json"
        improvement_path = self.repo_root / "docs" / "task_workspaces" / "T-9002" / "TASK_IMPROVEMENT_REPORT.json"
        radical_path = self.repo_root / "docs" / "task_workspaces" / "T-9002" / "RADICAL_REDESIGN_REPORT.json"
        convergence = json.loads(convergence_path.read_text(encoding="utf-8"))
        improvement = json.loads(improvement_path.read_text(encoding="utf-8"))
        radical = json.loads(radical_path.read_text(encoding="utf-8"))
        self.assertIsNotNone(result)
        self.assertEqual(convergence["branch_count"], 9)
        self.assertTrue(any(item["status"] == "COMPLETED" for item in convergence["branch_summaries"]))
        self.assertEqual({item["lane_id"] for item in convergence["branch_summaries"]}, {"alpha", "beta", "gamma"})
        self.assertEqual(result["future_convergence_report_ref"], "docs/task_workspaces/T-9002/FUTURE_CONVERGENCE_REPORT.json")
        self.assertEqual(result["task_improvement_report_ref"], "docs/task_workspaces/T-9002/TASK_IMPROVEMENT_REPORT.json")
        self.assertEqual(result["radical_redesign_report_ref"], "docs/task_workspaces/T-9002/RADICAL_REDESIGN_REPORT.json")
        self.assertEqual(set(improvement["parent_decision_options"]), {"reject", "adopt", "hybridize", "escalate_to_hitl"})
        self.assertEqual(improvement["recommended_parent_action"], "escalate_to_hitl")
        self.assertEqual(len(improvement["lane_summaries"]), 3)
        self.assertIn("Alpha/Beta/Gamma", improvement["summary"])
        self.assertEqual(set(radical["parent_decision_options"]), {"reject", "hybridize", "promote"})
        self.assertEqual(len(radical["radical_branch_summaries"]), 3)
        self.assertIn("reject, hybridize, or promote", radical["summary"])

    def test_future_dispatch_adds_memory_reuse_advisor_when_history_exists(self) -> None:
        store = RedesignMemoryStore(self.repo_root)
        store.ingest_task(
            task_id="T-9001",
            workflow_context={
                "workflow": {
                    "workflow_id": "t-9001-wf-1",
                    "request": {
                        "task_id": "T-9001",
                        "command_modifier": "AASA",
                        "scope": "architecture_question",
                        "prompt": "Prior runtime topology redesign for sovereign execution.",
                    },
                },
                "workflow_record": {"modifier": "AASA"},
            },
            workflow_policy={
                "task_profile": {
                    "task_id": "T-9001",
                    "title": "Earlier runtime topology redesign",
                    "task_class": "ANALYSIS",
                    "modifier": "AASA",
                    "scope": "architecture_question",
                },
                "current_stage": "DESIGN",
            },
            future_convergence_report={
                "task_id": "T-9001",
                "workflow_id": "t-9001-wf-1",
                "dispatch_id": "dispatch-1",
                "current_stage": "DESIGN",
                "branch_count": 3,
                "branch_summaries": [
                    {"branch_id": "visionary:conservative", "lane_id": "alpha", "status": "COMPLETED"},
                    {"branch_id": "visionary:aggressive", "lane_id": "beta", "status": "COMPLETED"},
                    {"branch_id": "visionary:radical", "lane_id": "gamma", "status": "COMPLETED"},
                ],
                "disagreement_signals": ["runtime_boundary_tradeoff"],
                "convergence_summary": "Earlier redesign hit a useful hybrid boundary.",
                "recommended_parent_action": "hybridize",
            },
            task_improvement_report={
                "task_id": "T-9001",
                "workflow_id": "t-9001-wf-1",
                "dispatch_id": "dispatch-1",
                "current_stage": "DESIGN",
                "summary": "A partially successful hybrid runtime topology existed.",
                "recommended_parent_action": "hybridize",
                "trigger_policy": {
                    "trigger_reasons": ["task_class_has_design_surface", "historical_runtime_boundary_pressure"],
                },
                "lane_summaries": [{"lane_id": "alpha"}, {"lane_id": "beta"}, {"lane_id": "gamma"}],
            },
            convergence_gate_record={"selected_disposition": "hybridize", "convergence_status": "DECIDED"},
            adversarial_review_record={
                "review_status": "REVIEW_APPROVED",
                "adversarial_policy": {"trigger_reasons": ["architecture_improvement_pressure_detected"]},
            },
            closeout_execution_record={"workflow_status": "COMPLETED"},
        )
        engine = WorkflowPolicyEngine(self.repo_root)
        engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASA", "scope": "architecture_question"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        registry = ArtifactRegistry(self.repo_root)
        dispatcher = CodexTeamDispatcher(
            self.repo_root,
            artifact_registry=registry,
            provider_runtime=FakeProviderRuntime(),
            operator_sessions=None,
            context_store=None,
        )
        payload = dispatcher.prepare_dispatch(
            task_id="T-9002",
            workflow_id="wf-1",
            human_record={},
            recommendations={"dispatch_candidates": []},
            action_label="explore_futures",
            instruction="future_swarm:research",
            dry_run=True,
        )
        self.assertEqual(payload["children"][0]["role"], "memory_reuse_analyst")
        self.assertIn("Offer considerations only", payload["children"][0]["objective"])
        self.assertIn("runtime/state/workflow_policy/T-9002/latest.json", payload["context_refs"])

    def test_full_pipeline_feasibility_requires_adversarial_review(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        seed = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASNI", "scope": "new_idea_integration"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        seed["current_stage"] = "FEASIBILITY"
        seed["next_stage"] = "DESIGN"
        seed["stage_history"] = [
            {
                "stage": "FEASIBILITY",
                "status": "READY",
                "opened_at": "2026-03-15T00:00:00Z",
                "updated_at": "2026-03-15T00:00:00Z",
                "closed_at": None,
                "transition_reason": "test_seed",
            }
        ]
        engine._write(task_id="T-9002", payload=seed)
        self._write_json_artifact("HYPOTHESIS_PACKET.json", {"type": "HYPOTHESIS_PACKET"})
        self._write_json_artifact("CONTRADICTION_MAP.json", {"type": "CONTRADICTION_MAP"})
        self._write_json_artifact("FEASIBILITY_REPORT.json", {"type": "FEASIBILITY_REPORT"})
        self._write_json_artifact("EXPERIMENT_SIMULATION_REPORT.json", {"type": "EXPERIMENT_SIMULATION_REPORT"})
        evidence_root = self.repo_root / "docs" / "task_workspaces" / "T-9002" / "evidence"
        evidence_root.mkdir(parents=True, exist_ok=True)
        for idx in range(4):
            (evidence_root / f"note-{idx}.md").write_text("evidence", encoding="utf-8")
        approved_review = {
            "review_status": "REVIEW_APPROVED",
            "completed_at": "2026-03-15T00:10:00Z",
            "updated_at": "2026-03-15T00:10:00Z",
        }
        approved_decision = {
            "operator_decision": "APPROVED",
            "controller_recorded_at": "2026-03-15T00:11:00Z",
            "updated_at": "2026-03-15T00:11:00Z",
        }
        blocked = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASNI", "scope": "new_idea_integration"}}},
            run=None,
            review_gate_record=approved_review,
            adversarial_review_record=None,
            human_decision_record=approved_decision,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        self.assertEqual(blocked["current_stage"], "FEASIBILITY")
        self.assertTrue(blocked["adversarial_review"]["required_before_stage_close"])
        self.assertIn("start_adversarial_review", {item["action"] for item in blocked["next_actions"]})
        advanced = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASNI", "scope": "new_idea_integration"}}},
            run=None,
            review_gate_record=approved_review,
            adversarial_review_record={
                "review_status": "REVIEW_APPROVED",
                "completed_at": "2026-03-15T00:12:00Z",
                "updated_at": "2026-03-15T00:12:00Z",
            },
            human_decision_record=approved_decision,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        self.assertEqual(advanced["current_stage"], "DESIGN")
        self.assertEqual(advanced["lifecycle_status"], "NEXT_STAGE_READY")

    def test_analysis_research_does_not_require_adversarial_review(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        state = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASA", "scope": "architecture_question"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        self.assertFalse(state["adversarial_review"]["required_before_stage_close"])
        self.assertNotIn("start_adversarial_review", {item["action"] for item in state["next_actions"]})
        self.assertFalse(state["convergence"]["required_before_stage_close"])
        self.assertEqual(state["convergence"]["status"], "NOT_REQUIRED")

    def test_branch_heavy_stage_requires_convergence_gate_before_advancing(self) -> None:
        engine = WorkflowPolicyEngine(self.repo_root)
        seed = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASA", "scope": "architecture_question"}}},
            run=None,
            review_gate_record=None,
            adversarial_review_record=None,
            human_decision_record=None,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        seed["current_stage"] = "RESEARCH"
        seed["next_stage"] = "ASSESSMENT"
        seed["stage_history"] = [
            {
                "stage": "RESEARCH",
                "status": "READY",
                "opened_at": "2026-03-15T00:00:00Z",
                "updated_at": "2026-03-15T00:00:00Z",
                "closed_at": None,
                "transition_reason": "test_seed",
            }
        ]
        engine._write(task_id="T-9002", payload=seed)
        self._write_json_artifact("COMMAND_REQUEST.yaml", {"task_id": "T-9002"})
        self._write_json_artifact("DISCOVERY_MAP.json", {"type": "DISCOVERY_MAP"})
        self._write_json_artifact("WORKFLOW_RUN_RECORD.json", {"type": "WORKFLOW_RUN_RECORD", "status": "REVIEW_APPROVED"})
        evidence_root = self.repo_root / "docs" / "task_workspaces" / "T-9002" / "evidence"
        evidence_root.mkdir(parents=True, exist_ok=True)
        for idx in range(2):
            (evidence_root / f"evidence-{idx}.md").write_text("evidence", encoding="utf-8")
        future_convergence = {
            "type": "FUTURE_CONVERGENCE_REPORT",
            "task_id": "T-9002",
            "workflow_id": "wf-1",
            "dispatch_id": "dispatch-1",
            "current_stage": "RESEARCH",
            "generated_at": "2026-03-15T00:09:00Z",
            "branch_count": 3,
            "branch_summaries": [
                {"branch_id": "visionary:conservative", "branch_label": "A", "parent_role": "visionary", "branch_kind": "conservative", "lane_id": "alpha", "lane_label": "Alpha", "lane_strategy": "improve", "objective": "A", "status": "COMPLETED", "verdicts": ["good"], "recommended_next_actions": ["compare"], "child_artifacts": []},
                {"branch_id": "visionary:aggressive", "branch_label": "B", "parent_role": "visionary", "branch_kind": "aggressive", "lane_id": "beta", "lane_label": "Beta", "lane_strategy": "reframe", "objective": "B", "status": "COMPLETED", "verdicts": ["better"], "recommended_next_actions": ["compare"], "child_artifacts": []},
                {"branch_id": "visionary:radical", "branch_label": "C", "parent_role": "visionary", "branch_kind": "radical", "lane_id": "gamma", "lane_label": "Gamma", "lane_strategy": "break", "objective": "C", "status": "DRAFT", "verdicts": [], "recommended_next_actions": [], "child_artifacts": []},
            ],
            "disagreement_signals": ["alpha_vs_beta_tradeoff"],
            "convergence_summary": "Synthetic convergence summary.",
            "recommended_parent_action": "hybridize",
            "source_refs": {},
        }
        task_improvement = {
            "type": "TASK_IMPROVEMENT_REPORT",
            "task_id": "T-9002",
            "workflow_id": "wf-1",
            "dispatch_id": "dispatch-1",
            "current_stage": "RESEARCH",
            "generated_at": "2026-03-15T00:10:00Z",
            "trigger_policy": {"enabled": True, "trigger_reasons": ["task_class_has_design_surface"], "decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"], "lane_ids": ["alpha", "beta", "gamma"], "lane_order": ["alpha", "beta", "gamma"]},
            "lane_summaries": [],
            "parent_decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"],
            "recommended_parent_action": "hybridize",
            "summary": "Synthetic task improvement summary.",
            "source_refs": {},
        }
        radical_redesign = {
            "type": "RADICAL_REDESIGN_REPORT",
            "task_id": "T-9002",
            "workflow_id": "wf-1",
            "dispatch_id": "dispatch-1",
            "current_stage": "RESEARCH",
            "generated_at": "2026-03-15T00:11:00Z",
            "trigger_policy": {"enabled": True, "trigger_reasons": ["gamma_lane_present"], "decision_options": ["reject", "hybridize", "promote"], "radical_branch_ids": ["visionary:radical"]},
            "radical_branch_summaries": [],
            "parent_decision_options": ["reject", "hybridize", "promote"],
            "summary": "Synthetic radical summary.",
            "source_refs": {},
        }
        approved_review = {
            "review_status": "REVIEW_APPROVED",
            "completed_at": "2026-03-15T00:12:00Z",
            "updated_at": "2026-03-15T00:12:00Z",
        }
        approved_decision = {
            "operator_decision": "APPROVED",
            "controller_recorded_at": "2026-03-15T00:13:00Z",
            "updated_at": "2026-03-15T00:13:00Z",
        }
        blocked = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASA", "scope": "architecture_question"}}},
            run=None,
            review_gate_record=approved_review,
            adversarial_review_record=None,
            future_convergence_report=future_convergence,
            task_improvement_report=task_improvement,
            radical_redesign_report=radical_redesign,
            convergence_gate_record=None,
            human_decision_record=approved_decision,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        self.assertEqual(blocked["current_stage"], "RESEARCH")
        self.assertEqual(blocked["lifecycle_status"], "CONVERGENCE_PENDING")
        self.assertTrue(blocked["convergence"]["required_before_stage_close"])
        self.assertIn("start_convergence_decision", {item["action"] for item in blocked["next_actions"]})
        advanced = engine.evaluate(
            task_id="T-9002",
            workflow_context={"workflow": {"request": {"command_modifier": "AASA", "scope": "architecture_question"}}},
            run=None,
            review_gate_record=approved_review,
            adversarial_review_record=None,
            future_convergence_report=future_convergence,
            task_improvement_report=task_improvement,
            radical_redesign_report=radical_redesign,
            convergence_gate_record={
                "type": "CONVERGENCE_GATE_RECORD",
                "task_id": "T-9002",
                "workflow_id": "wf-1",
                "run_id": "run-1",
                "current_stage": "RESEARCH",
                "required_before_stage_close": True,
                "convergence_status": "DECIDED",
                "ready_for_decision": True,
                "satisfied": True,
                "branch_count": 3,
                "minimum_completed_branches": 2,
                "completed_branch_count": 2,
                "disagreement_signals": ["alpha_vs_beta_tradeoff"],
                "recommended_parent_action": "hybridize",
                "decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl", "promote", "continue_exploration"],
                "gamma_present": True,
                "requires_gamma_disposition": True,
                "selected_disposition": "hybridize",
                "rationale": "Blend the strongest Alpha and Beta branches.",
                "started_at": "2026-03-15T00:14:00Z",
                "completed_at": "2026-03-15T00:15:00Z",
                "source_refs": {},
                "source": "test",
                "notes": [],
                "updated_at": "2026-03-15T00:15:00Z",
            },
            human_decision_record=approved_decision,
            closeout_execution_record=None,
            controller_run_result=None,
            claim=None,
            pending_hitl_count=0,
        )
        self.assertEqual(advanced["current_stage"], "ASSESSMENT")
        self.assertEqual(advanced["lifecycle_status"], "NEXT_STAGE_READY")

    def _copy_schemas(self) -> None:
        for name in SCHEMA_NAMES:
            source = REPO_ROOT / "docs" / "schemas" / f"{name}.schema.json"
            destination = self.repo_root / "docs" / "schemas" / f"{name}.schema.json"
            shutil.copy2(source, destination)

    def _write_json_artifact(self, filename: str, payload: dict[str, object]) -> None:
        path = self.repo_root / "docs" / "task_workspaces" / "T-9002" / filename
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def _write_todo(self) -> None:
        todo_path = self.repo_root / "docs" / "TODO.md"
        todo_path.write_text(
            "\n".join(
                [
                    "# TODO",
                    "",
                    "| ID | Task | Type | Priority | Dependencies | Notes |",
                    "|----|------|------|----------|--------------|-------|",
                    "| T-9001 | Earlier runtime redesign | Analysis | HIGH | none | Synthetic redesign memory seed |",
                    "| T-9002 | Architecture comparison | Analysis | HIGH | none | Synthetic test task |",
                    "",
                ]
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
