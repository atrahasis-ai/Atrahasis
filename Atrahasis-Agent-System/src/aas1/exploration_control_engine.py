from __future__ import annotations

from typing import Any


class ExplorationControlEngine:
    def run(
        self,
        *,
        research_program_report: dict[str, Any],
        research_strategy_report: dict[str, Any],
        decision_ranking_report: dict[str, Any],
        contradiction_map: dict[str, Any],
    ) -> dict[str, Any]:
        priority_order = research_strategy_report.get("priority_order", []) or [
            program["program_id"]
            for program in research_program_report.get("active_programs", [])[:5]
        ] or [
            item["hypothesis_id"]
            for item in decision_ranking_report.get("display_candidates", [])[:5]
        ]
        recommended_actions = research_strategy_report.get("recommended_actions", [])
        active_programs = [
            program
            for program in research_program_report.get("active_programs", [])
            if program.get("execution_state") == "active"
        ]
        return {
            "type": "EXPLORATION_CONTROL_RECOMMENDATION",
            "recommended_branch_budget": max(
                1,
                min(
                    5,
                    int(research_strategy_report.get("recommended_branch_budget") or max(2, min(5, len(priority_order)))),
                ),
            ),
            "priority_order": priority_order,
            "recommended_actions": recommended_actions,
            "strategy_summary": research_strategy_report.get("strategy_summary"),
            "escalate_to_human": len(contradiction_map["contradictions"]) > 0 or bool(active_programs),
        }
