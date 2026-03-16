from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class HumanDecisionInterface:
    IMPROVEMENT_ARTIFACTS = (
        "TASK_IMPROVEMENT_REPORT.json",
        "RADICAL_REDESIGN_REPORT.json",
        "CONVERGENCE_GATE_RECORD.json",
    )

    def run(
        self,
        *,
        command_request: dict[str, Any],
        research_program_report: dict[str, Any],
        research_strategy_report: dict[str, Any],
        decision_ranking_report: dict[str, Any],
        contradiction_map: dict[str, Any],
    ) -> dict[str, Any]:
        display_candidates = decision_ranking_report.get("display_candidates", [])
        strategy_by_program = {
            item["program_id"]: item
            for item in research_strategy_report.get("resource_allocations", [])
        }
        top_hypotheses = [
            {
                "hypothesis_id": hypothesis["hypothesis_id"],
                "title": hypothesis["title"],
                "opportunity_zone": hypothesis.get("opportunity_zone"),
                "opportunity_score": hypothesis.get("opportunity_score"),
                "candidate_label": hypothesis.get("candidate_label"),
            }
            for hypothesis in display_candidates
        ]
        active_programs = []
        visible_programs = [
            program
            for program in research_program_report.get("active_programs", [])
            if program.get("execution_state") == "active"
        ]
        for program in visible_programs[:5]:
            ranked_program_hypotheses = [
                candidate for candidate in display_candidates if candidate["hypothesis_id"] in program["hypothesis_list"]
            ]
            strategy = strategy_by_program.get(program["program_id"], {})
            active_programs.append(
                {
                    "program_id": program["program_id"],
                    "program_title": program["program_title"],
                    "scope_level": program.get("scope_level"),
                    "target_domain": program["target_domain"],
                    "program_goal": program["program_goal"],
                    "hypothesis_list": program["hypothesis_list"][:5],
                    "contradiction_list": program["contradiction_list"][:5],
                    "solution_path_list": program["solution_path_list"][:5],
                    "opportunity_score": program["opportunity_score"],
                    "program_status": program["program_status"],
                    "execution_state": program.get("execution_state"),
                    "dependency_state": program.get("dependency_state"),
                    "last_exploration_cycle": program["last_exploration_cycle"],
                    "recommended_action": strategy.get("recommended_action"),
                    "allocation_ratio": strategy.get("allocation_ratio"),
                    "branch_budget": strategy.get("branch_budget"),
                    "governance_notes": program.get("governance_notes", [])[:3],
                    "cross_domain_candidates": [
                        candidate
                        for candidate in ranked_program_hypotheses
                        if candidate.get("candidate_label") == "Cross-Domain Opportunity"
                    ],
                }
            )
        priority_zones = [program["target_domain"] for program in active_programs] or [
            item["opportunity_zone"] for item in top_hypotheses if item.get("opportunity_zone")
        ]
        active_program_hypotheses = {
            hypothesis_id
            for program in active_programs
            for hypothesis_id in program["hypothesis_list"]
        }
        spawn_candidates = research_strategy_report.get("spawn_candidates", [])
        recommended_actions = research_strategy_report.get("recommended_actions", [])
        options = []
        for program in active_programs:
            options.extend(
                [
                    {
                        "label": "continue_program",
                        "program_id": program["program_id"],
                        "program_title": program["program_title"],
                    },
                    {
                        "label": "explore_new_hypothesis",
                        "program_id": program["program_id"],
                        "program_title": program["program_title"],
                    },
                    {
                        "label": "pause_program",
                        "program_id": program["program_id"],
                        "program_title": program["program_title"],
                    },
                    {
                        "label": "terminate_program",
                        "program_id": program["program_id"],
                        "program_title": program["program_title"],
                    },
                ]
            )
            if program.get("recommended_action") == "expand_program":
                options.append(
                    {
                        "label": "expand_program",
                        "program_id": program["program_id"],
                        "program_title": program["program_title"],
                    }
                )
        return {
            "decision_type": "OPERATOR_GUIDANCE",
            "task_id": command_request["task_id"],
            "workflow_status": "PENDING_HUMAN_REVIEW",
            "prompt": command_request["prompt"],
            "evidence_summary": {
                "modifier": command_request["command_modifier"],
                "priority_zones": priority_zones,
                "contradiction_count": len(contradiction_map["contradictions"]),
                "strategy_summary": research_strategy_report.get("strategy_summary"),
            },
            "active_research_programs": active_programs,
            "top_hypotheses": top_hypotheses,
            "research_strategy_summary": research_strategy_report.get("strategy_summary"),
            "recommended_actions": recommended_actions,
            "spawn_candidates": spawn_candidates,
            "core_contradictions": [
                {
                    "contradiction_id": item["id"],
                    "hypothesis_id": item["hypothesis_id"],
                    "statement": item["contradiction"],
                    "severity": item["severity"],
                }
                for item in contradiction_map["contradictions"]
                if item["hypothesis_id"] in active_program_hypotheses
            ][:5],
            "cross_domain_candidates": [
                item for item in display_candidates if item.get("candidate_label") == "Cross-Domain Opportunity"
            ],
            "options": options,
            "operator_actions": (
                [
                    {
                        "label": "spawn_program",
                        "instruction": candidate["spawn_id"],
                    }
                    for candidate in spawn_candidates[:2]
                ]
                + [
                    {
                        "label": "redirect",
                        "instruction": "<new exploration instruction>",
                    }
                ]
            ),
            "operator_decision": "PENDING",
            "constraints": command_request["operator_constraints"],
        }

    def render_prompt_for_task(self, *, task_workspace: Path) -> str:
        human_record = self._load_json(task_workspace / "HUMAN_DECISION_RECORD.json")
        exploration_record = self._load_json(task_workspace / "EXPLORATION_CONTROL_RECORD.json")
        task_improvement_report = self._load_optional_json(task_workspace / "TASK_IMPROVEMENT_REPORT.json")
        radical_redesign_report = self._load_optional_json(task_workspace / "RADICAL_REDESIGN_REPORT.json")
        convergence_gate_record = self._load_optional_json(task_workspace / "CONVERGENCE_GATE_RECORD.json")
        return self.render_prompt_from_records(
            human_record=human_record,
            exploration_record=exploration_record,
            task_improvement_report=task_improvement_report,
            radical_redesign_report=radical_redesign_report,
            convergence_gate_record=convergence_gate_record,
        )

    def render_prompt_from_records(
        self,
        *,
        human_record: dict[str, Any],
        exploration_record: dict[str, Any],
        task_improvement_report: dict[str, Any] | None = None,
        radical_redesign_report: dict[str, Any] | None = None,
        convergence_gate_record: dict[str, Any] | None = None,
    ) -> str:
        synthesized_options = self.synthesize_operator_options(
            human_record=human_record,
            task_improvement_report=task_improvement_report,
            radical_redesign_report=radical_redesign_report,
            convergence_gate_record=convergence_gate_record,
        )
        lines = [
            "Human Review Required",
            "",
            f"Task: {human_record.get('task_id', 'unknown')}",
            f"Status: {human_record.get('workflow_status', 'PENDING_HUMAN_REVIEW')}",
            f"Command: {human_record['evidence_summary']['modifier']}",
        ]
        prompt = human_record.get("prompt")
        if prompt:
            lines.extend(["", "Prompt:", prompt])
        strategy_summary = human_record.get("research_strategy_summary")
        if strategy_summary:
            lines.extend(["", "Research Strategy:", strategy_summary])

        programs = human_record.get("active_research_programs", [])
        if programs:
            lines.extend(["", "Active Research Programs:"])
            for item in programs:
                lines.append(
                    f"- Program {item['program_id']}: {item['program_title']} "
                    f"({item.get('scope_level', 'n/a')}, score {self._render_score(item.get('opportunity_score'))}, "
                    f"status {item['program_status']}, execution {item.get('execution_state', 'unknown')})"
                )
                lines.append(f"  Hypotheses: {', '.join(item['hypothesis_list']) or 'none'}")
                lines.append(f"  Contradictions: {', '.join(item['contradiction_list']) or 'none'}")
                if item.get("recommended_action"):
                    lines.append(
                        "  Recommended action: "
                        f"{item['recommended_action']} "
                        f"(branch budget {item.get('branch_budget', 'n/a')}, allocation {item.get('allocation_ratio', 'n/a')})"
                    )
                if item.get("governance_notes"):
                    for note in item["governance_notes"]:
                        lines.append(f"  Governance: {note}")
                if item.get("cross_domain_candidates"):
                    for candidate in item["cross_domain_candidates"]:
                        lines.append(
                            "  Cross-Domain Opportunity: "
                            f"{candidate['hypothesis_id']} {candidate['title']} "
                            f"(Opportunity score {self._render_score(candidate.get('opportunity_score'))})"
                        )
        else:
            hypotheses = human_record.get("top_hypotheses", [])
            if hypotheses:
                lines.extend(["", "Top Exploration Candidates:"])
                for item in hypotheses:
                    lines.append(
                        f"- {item['hypothesis_id']}: {item['title']} "
                        f"(Opportunity score {self._render_score(item.get('opportunity_score'))})"
                    )

        contradictions = human_record.get("core_contradictions", [])
        if contradictions:
            lines.extend(["", "Core Contradictions:"])
            for item in contradictions:
                lines.append(
                    f"- {item['contradiction_id']} [{item['severity']}]: {item['statement']}"
                )

        if synthesized_options:
            lines.extend(["", "Operator Path Options:"])
            for item in synthesized_options:
                title = item.get("title") or item["label"]
                lines.append(f"- {title} [{item['label']}]")
                lines.append(f"  Summary: {item['summary']}")
                if item.get("main_upside"):
                    lines.append(f"  Upside: {item['main_upside']}")
                if item.get("main_risk"):
                    lines.append(f"  Risk: {item['main_risk']}")
                if item.get("recommended"):
                    lines.append("  Recommended: yes")
        options = human_record.get("options", [])
        if options:
            lines.extend(["", "Operator Action Controls:"])
            for item in options:
                lines.append(
                    f"- {item['label']}: {item.get('program_id', item.get('path_id', 'unknown'))}"
                )
        for item in human_record.get("operator_actions", []):
            lines.append(f"- {item['label']}: {item.get('instruction', '')}".rstrip())

        spawn_candidates = human_record.get("spawn_candidates", [])
        if spawn_candidates:
            lines.extend(["", "Program Spawn Candidates:"])
            for item in spawn_candidates:
                lines.append(
                    f"- {item['spawn_id']}: {item['program_title']} "
                    f"(priority {self._render_score(item.get('priority_score'))})"
                )
        dispatch_recommendations = human_record.get("dispatch_recommendations", [])
        if dispatch_recommendations:
            lines.extend(["", "Recommended Codex Teams:"])
            for item in dispatch_recommendations:
                lines.append(
                    f"- {item['spawn_id']}: {item['team_mode']} "
                    f"using {', '.join(item.get('child_roles', [])) or 'no child roles'}"
                )
                lines.append(
                    f"  Approval: {item.get('approval_status', 'unknown')}; "
                    f"Dispatch: {item.get('dispatch_readiness', 'unknown')}"
                )
            lines.extend(
                [
                    "",
                    "Dispatch command after approval:",
                    f"- python scripts/dispatch_aas_team.py {human_record.get('task_id', 'T-000')} --spawn-id <spawn_id> --execute",
                ]
            )

        lines.extend(
            [
                "",
                "Exploration Guidance:",
                f"- Escalate to human: {str(exploration_record.get('escalate_to_human', False)).lower()}",
                f"- Recommended branch budget: {exploration_record.get('recommended_branch_budget', 'n/a')}",
            ]
        )
        priority_order = exploration_record.get("priority_order", [])
        if priority_order:
            lines.append(f"- Priority order: {', '.join(priority_order[:5])}")

        constraints = human_record.get("constraints", [])
        if constraints:
            lines.extend(["", "Operator Constraints:"])
            for item in constraints:
                lines.append(f"- {item}")

        lines.extend(
            [
                "",
                "Respond with one of:",
            ]
        )
        if synthesized_options:
            for item in synthesized_options:
                lines.append(f"- {item['label']}: {item['title']}")
        if options:
            for item in options:
                lines.append(f"- {item['label']}: {item.get('program_id', item.get('path_id', 'unknown'))}")
        for item in human_record.get("operator_actions", []):
            lines.append(f"- {item['label']}: {item.get('instruction', '')}".rstrip())
        return "\n".join(lines)

    def synthesize_operator_options(
        self,
        *,
        human_record: dict[str, Any],
        task_improvement_report: dict[str, Any] | None = None,
        radical_redesign_report: dict[str, Any] | None = None,
        convergence_gate_record: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        options: list[dict[str, Any]] = []
        baseline_summary = (
            human_record.get("research_strategy_summary")
            or human_record.get("evidence_summary", {}).get("strategy_summary")
            or "Continue along the current task path."
        )
        if task_improvement_report or radical_redesign_report:
            options.append(
                {
                    "label": "current_path",
                    "title": "Current Path",
                    "summary": baseline_summary,
                    "main_upside": "Keeps momentum on the current task path.",
                    "main_risk": None,
                    "recommended": False,
                    "source": "human_decision_record",
                }
            )
        if task_improvement_report:
            recommended_action = str(task_improvement_report.get("recommended_parent_action") or "").strip().lower()
            disagreement_signals = list((convergence_gate_record or {}).get("disagreement_signals", []))
            if not disagreement_signals:
                disagreement_signals = list((task_improvement_report.get("source_refs") or {}).keys())[:1]
            title = "Improved Path"
            label = "improved_path"
            if recommended_action == "hybridize":
                title = "Hybrid Path"
                label = "hybrid_path"
            elif recommended_action == "escalate_to_hitl":
                title = "Escalated Improvement Path"
                label = "improved_path"
            options.append(
                {
                    "label": label,
                    "title": title,
                    "summary": str(task_improvement_report.get("summary") or "A better task path was synthesized from the explored branches."),
                    "main_upside": f"Recommended action: {recommended_action or 'review improvement synthesis'}.",
                    "main_risk": disagreement_signals[0] if disagreement_signals else "Needs parent selection before the stage closes.",
                    "recommended": recommended_action in {"adopt", "hybridize"},
                    "source": "task_improvement_report",
                }
            )
        if radical_redesign_report:
            selected_disposition = str((convergence_gate_record or {}).get("selected_disposition") or "").strip().lower()
            options.append(
                {
                    "label": "radical_path",
                    "title": "Radical Path",
                    "summary": str(radical_redesign_report.get("summary") or "A high-novelty alternative path was discovered."),
                    "main_upside": "Highest novelty and strongest assumption-breaking upside.",
                    "main_risk": "May require broader change and explicit operator approval.",
                    "recommended": selected_disposition == "promote",
                    "source": "radical_redesign_report",
                }
            )
        return options

    def has_synthesized_option_inputs(self, *, task_workspace: Path) -> bool:
        return any((task_workspace / item).exists() for item in self.IMPROVEMENT_ARTIFACTS)

    def _load_json(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def _load_optional_json(self, path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        return self._load_json(path)

    def _render_score(self, value: Any) -> str:
        if value is None:
            return "n/a"
        return str(value)
