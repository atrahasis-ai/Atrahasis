from __future__ import annotations

import re
from typing import Any


class ResearchDirectorModel:
    DEFAULT_ALIGNMENT_SCORE = 0.65

    def plan_directives(
        self,
        *,
        frontier_model: dict[str, Any],
        discovery_map: dict[str, Any],
        telemetry_metrics: dict[str, Any],
        value_alignment_signal: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        alignment_score, alignment_mode = self._alignment_signal(value_alignment_signal)
        discovery_terms = self._discovery_terms(discovery_map)
        telemetry_pressure = self._telemetry_pressure(telemetry_metrics)
        spawn_candidates = []
        for signal in frontier_model.get("frontier_signals", [])[:4]:
            domain = signal["domain"]
            signal_support = self._signal_support(domain, discovery_terms)
            priority_score = round(
                (signal["momentum"] * 0.6)
                + (alignment_score * 0.25)
                + (signal_support * 0.1)
                + (telemetry_pressure * 0.05),
                3,
            )
            spawn_candidates.append(
                {
                    "spawn_id": f"spawn:{self._slug(domain)}",
                    "program_title": f"{domain.title()} Research Program",
                    "target_domain": domain,
                    "program_goal": f"Explore {domain} in a coordinated research program.",
                    "priority_score": priority_score,
                    "recommended_action": "spawn_program" if priority_score >= 0.72 else "continue_program",
                }
            )
        return {
            "type": "RESEARCH_DIRECTOR_DIRECTIVES",
            "alignment_mode": alignment_mode,
            "alignment_score": alignment_score,
            "telemetry_pressure": telemetry_pressure,
            "spawn_candidates": spawn_candidates,
            "priority_domains": [item["target_domain"] for item in spawn_candidates[:3]],
        }

    def run(
        self,
        *,
        research_program_report: dict[str, Any],
        frontier_model: dict[str, Any],
        discovery_map: dict[str, Any],
        telemetry_metrics: dict[str, Any],
        value_alignment_signal: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        directives = self.plan_directives(
            frontier_model=frontier_model,
            discovery_map=discovery_map,
            telemetry_metrics=telemetry_metrics,
            value_alignment_signal=value_alignment_signal,
        )
        active_programs = [
            program
            for program in research_program_report.get("active_programs", [])
            if program.get("execution_state") == "active"
        ]
        active_programs.sort(key=lambda item: item.get("opportunity_score", 0.0), reverse=True)
        total_weight = sum(max(program.get("opportunity_score", 0.0), 0.05) for program in active_programs) or 1.0

        resource_allocations = []
        recommended_actions = []
        for program in active_programs:
            allocation_ratio = round(max(program.get("opportunity_score", 0.0), 0.05) / total_weight, 3)
            branch_budget = max(1, min(3, round(allocation_ratio * 6)))
            action = self._recommend_action(
                program=program,
                allocation_ratio=allocation_ratio,
                telemetry_pressure=directives["telemetry_pressure"],
                alignment_score=directives["alignment_score"],
            )
            rationale = self._action_rationale(
                program=program,
                action=action,
                allocation_ratio=allocation_ratio,
            )
            resource_allocations.append(
                {
                    "program_id": program["program_id"],
                    "program_title": program["program_title"],
                    "scope_level": program.get("scope_level"),
                    "execution_state": program.get("execution_state"),
                    "allocation_ratio": allocation_ratio,
                    "branch_budget": branch_budget,
                    "recommended_action": action,
                    "rationale": rationale,
                }
            )
            recommended_actions.append(
                {
                    "action": action,
                    "program_id": program["program_id"],
                    "program_title": program["program_title"],
                    "target_domain": program["target_domain"],
                    "scope_level": program.get("scope_level"),
                    "execution_state": program.get("execution_state"),
                    "allocation_ratio": allocation_ratio,
                    "branch_budget": branch_budget,
                    "opportunity_score": program.get("opportunity_score", 0.0),
                    "rationale": rationale,
                }
            )

        spawn_candidates = self._spawn_candidates(
            active_programs=active_programs,
            directives=directives,
            frontier_model=frontier_model,
        )
        priority_order = [item["program_id"] for item in resource_allocations]
        priority_order.extend(item["spawn_id"] for item in spawn_candidates[:2])

        summary = self._strategy_summary(
            active_programs=active_programs,
            resource_allocations=resource_allocations,
            spawn_candidates=spawn_candidates,
        )
        telemetry_events = [
            {
                "event": "research_strategy_generated",
                "active_program_count": len(active_programs),
                "spawn_candidate_count": len(spawn_candidates),
            }
        ]
        telemetry_events.extend(
            {
                "event": "research_strategy_action_recommended",
                "program_id": item["program_id"],
                "action": item["recommended_action"],
                "allocation_ratio": item["allocation_ratio"],
            }
            for item in resource_allocations
        )

        return {
            "type": "RESEARCH_STRATEGY_REPORT",
            "strategy_summary": summary,
            "alignment_mode": directives["alignment_mode"],
            "alignment_score": directives["alignment_score"],
            "telemetry_pressure": directives["telemetry_pressure"],
            "telemetry_metrics": telemetry_metrics,
            "priority_order": priority_order,
            "recommended_branch_budget": resource_allocations[0]["branch_budget"] if resource_allocations else 1,
            "resource_allocations": resource_allocations,
            "recommended_actions": recommended_actions,
            "spawn_candidates": spawn_candidates,
            "telemetry_events": telemetry_events,
        }

    def _recommend_action(
        self,
        *,
        program: dict[str, Any],
        allocation_ratio: float,
        telemetry_pressure: float,
        alignment_score: float,
    ) -> str:
        opportunity = program.get("opportunity_score", 0.0)
        status = program.get("program_status")
        execution_state = program.get("execution_state", "active")
        if execution_state.startswith("paused"):
            return "pause_program"
        if status in {"completed", "archived"} or execution_state in {"completed", "archived"}:
            return "terminate_program"
        if program.get("scope_level") == "L0" and opportunity >= 0.65:
            return "expand_program"
        if opportunity >= 0.7 and allocation_ratio >= 0.32 and alignment_score >= 0.55:
            return "expand_program"
        if opportunity < 0.42 and telemetry_pressure >= 0.55:
            return "pause_program"
        if opportunity < 0.25:
            return "terminate_program"
        return "continue_program"

    def _spawn_candidates(
        self,
        *,
        active_programs: list[dict[str, Any]],
        directives: dict[str, Any],
        frontier_model: dict[str, Any],
    ) -> list[dict[str, Any]]:
        existing_domains = {program["target_domain"] for program in active_programs}
        active_domain_tokens = {
            token
            for program in active_programs
            for token in self._tokens(program["target_domain"] + " " + program["program_title"])
        }
        candidates = []
        for item in directives.get("spawn_candidates", []):
            if item["target_domain"] in existing_domains:
                continue
            candidate_tokens = self._tokens(item["target_domain"] + " " + item["program_title"])
            if active_domain_tokens and not (active_domain_tokens & candidate_tokens):
                continue
            if item["priority_score"] < 0.72:
                continue
            candidates.append(item)
        if candidates:
            return candidates[:2]
        for signal in frontier_model.get("frontier_signals", [])[:2]:
            if signal["domain"] in existing_domains or signal["momentum"] < 0.8:
                continue
            signal_tokens = self._tokens(signal["domain"])
            if active_domain_tokens and not (active_domain_tokens & signal_tokens):
                continue
            candidates.append(
                {
                    "spawn_id": f"spawn:{self._slug(signal['domain'])}",
                    "program_title": f"{signal['domain'].title()} Research Program",
                    "target_domain": signal["domain"],
                    "program_goal": f"Explore {signal['domain']} in a coordinated research program.",
                    "priority_score": round(signal["momentum"], 3),
                    "recommended_action": "spawn_program",
                }
            )
        return candidates[:2]

    def _alignment_signal(self, value_alignment_signal: dict[str, Any] | None) -> tuple[float, str]:
        if value_alignment_signal is None:
            return self.DEFAULT_ALIGNMENT_SCORE, "fallback_neutral"
        score = value_alignment_signal.get("alignment_score")
        if score is None:
            return self.DEFAULT_ALIGNMENT_SCORE, "fallback_neutral"
        return round(float(score), 3), "external"

    def _telemetry_pressure(self, telemetry_metrics: dict[str, Any]) -> float:
        contradiction_pressure = min(telemetry_metrics.get("contradiction_count", 0) / 10, 1.0)
        graph_pressure = min(telemetry_metrics.get("discovery_node_count", 0) / 120, 1.0)
        active_program_pressure = min(telemetry_metrics.get("active_program_count", 0) / 5, 1.0)
        return round(
            (contradiction_pressure * 0.45)
            + (graph_pressure * 0.3)
            + (active_program_pressure * 0.25),
            3,
        )

    def _signal_support(self, domain: str, discovery_terms: set[str]) -> float:
        domain_tokens = self._tokens(domain)
        if not domain_tokens:
            return 0.35
        overlap = len(domain_tokens & discovery_terms) / len(domain_tokens)
        return round(max(overlap, 0.35), 3)

    def _discovery_terms(self, discovery_map: dict[str, Any]) -> set[str]:
        labels = []
        for node in discovery_map.get("nodes", discovery_map.get("entities", [])):
            labels.append(str(node.get("label", "")))
        return self._tokens(" ".join(labels))

    def _strategy_summary(
        self,
        *,
        active_programs: list[dict[str, Any]],
        resource_allocations: list[dict[str, Any]],
        spawn_candidates: list[dict[str, Any]],
    ) -> str:
        if not active_programs:
            return "No active research programs. Spawn a new program from frontier signals."
        lead = resource_allocations[0]
        summary = (
            f"Focus on {lead['program_title']} with {lead['recommended_action']} "
            f"and branch budget {lead['branch_budget']}."
        )
        if spawn_candidates:
            summary += f" Hold {len(spawn_candidates)} spawn candidate(s) for operator approval."
        return summary

    def _action_rationale(
        self,
        *,
        program: dict[str, Any],
        action: str,
        allocation_ratio: float,
    ) -> str:
        return (
            f"{program['program_title']} has opportunity score {program.get('opportunity_score', 0.0)} "
            f"and allocation ratio {allocation_ratio}, so the recommended action is {action}."
        )

    def _slug(self, value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

    def _tokens(self, text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z][a-z0-9_-]{3,}", text.lower())
        }
