from __future__ import annotations

import hashlib
import re
from typing import Any


class ResearchProgramEngine:
    NON_SIGNAL_TOKENS = {"research", "program", "systems"}
    SCOPE_LEVELS = ("L0", "L1", "L2", "L3", "L4")
    MAX_ACTIVE_HYPOTHESES = 10

    def plan_programs(
        self,
        *,
        command_prompt: str,
        discovery_map: dict[str, Any],
        frontier_model: dict[str, Any],
        cross_industry_report: dict[str, Any],
        hypothesis_archive: list[dict[str, Any]],
        cycle_count: int,
        research_director_directives: dict[str, Any] | None = None,
        prior_program_report: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        program_specs = self._seed_program_specs(
            command_prompt=command_prompt,
            frontier_model=frontier_model,
            cross_industry_report=cross_industry_report,
            research_director_directives=research_director_directives,
        )
        programs = []
        telemetry_events: list[dict[str, Any]] = []
        if prior_program_report is not None:
            for previous in prior_program_report.get("active_programs", []):
                restored = self._restore_program(previous)
                programs.append(restored)
                telemetry_events.append(
                    {
                        "event": "program_restored",
                        "program_id": restored["program_id"],
                        "scope_level": restored["scope_level"],
                    }
                )
        for spec in program_specs:
            program = self._build_program(
                title=spec["program_title"],
                target_domain=spec["target_domain"],
                goal=spec["program_goal"],
                program_kind=spec.get("program_kind"),
                scope_level=spec.get("scope_level"),
                cycle_count=cycle_count,
                frontier_score=spec["frontier_score"],
                hypothesis_archive=hypothesis_archive,
            )
            programs.append(program)
            telemetry_events.append(
                {
                    "event": "program_created",
                    "program_id": program["program_id"],
                    "program_title": program["program_title"],
                    "scope_level": program["scope_level"],
                }
            )

        programs, governance_summary, governance_events = self._govern_programs(
            programs=programs,
            cycle_count=cycle_count,
        )
        telemetry_events.extend(governance_events)
        updated_map = self._attach_program_nodes(
            discovery_map=discovery_map,
            active_programs=programs,
        )
        return {
            "type": "RESEARCH_PROGRAM_REPORT",
            "cycle_count": cycle_count,
            "active_programs": programs,
            "master_program_tree": self._build_master_program_tree(programs),
            "governance_summary": governance_summary,
            "updated_discovery_map": updated_map,
            "telemetry_events": telemetry_events,
        }

    def _restore_program(self, program: dict[str, Any]) -> dict[str, Any]:
        restored = dict(program)
        for key in (
            "hypothesis_list",
            "contradiction_list",
            "solution_path_list",
            "research_artifacts",
            "archived_hypotheses",
            "governance_notes",
            "master_tree_path",
        ):
            restored[key] = list(program.get(key, []))
        restored["program_status"] = program.get("program_status", "active")
        restored["execution_state"] = program.get("execution_state", "active")
        restored["dependency_state"] = program.get("dependency_state", "clear")
        restored["active_hypothesis_count"] = len(restored.get("hypothesis_list", []))
        restored["archived_hypothesis_count"] = len(restored.get("archived_hypotheses", []))
        return restored

    def update_programs(
        self,
        *,
        program_report: dict[str, Any],
        hypothesis_packet: dict[str, Any],
        contradiction_map: dict[str, Any],
        solution_paths: dict[str, Any],
        decision_ranking_report: dict[str, Any],
        frontier_model: dict[str, Any],
        cycle_count: int,
    ) -> dict[str, Any]:
        programs = [dict(program) for program in program_report["active_programs"]]
        contradictions_by_hypothesis: dict[str, list[str]] = {}
        for contradiction in contradiction_map["contradictions"]:
            contradictions_by_hypothesis.setdefault(contradiction["hypothesis_id"], []).append(contradiction["id"])
        paths_by_hypothesis: dict[str, list[str]] = {}
        for path in solution_paths["candidate_paths"]:
            paths_by_hypothesis.setdefault(path["hypothesis_id"], []).append(path["id"])
        ranking_by_hypothesis = {
            item["hypothesis_id"]: item
            for item in decision_ranking_report.get("ranked_hypotheses", [])
        }
        telemetry_events: list[dict[str, Any]] = []

        for hypothesis in hypothesis_packet["hypotheses"]:
            program = self._find_program(programs, hypothesis)
            if program is None:
                target_domain = hypothesis.get("domain") or hypothesis.get("opportunity_zone") or hypothesis["title"]
                program = self._build_program(
                    title=hypothesis.get("opportunity_zone", hypothesis["title"]).title(),
                    target_domain=target_domain,
                    goal=f"Systematically explore {hypothesis['title']}.",
                    cycle_count=cycle_count,
                    scope_level=hypothesis.get("scope_level"),
                    frontier_score=self._frontier_score(
                        target_domain=target_domain,
                        frontier_model=frontier_model,
                    ),
                    hypothesis_archive=[],
                )
                programs.append(program)
                telemetry_events.append(
                    {
                        "event": "program_created",
                        "program_id": program["program_id"],
                        "program_title": program["program_title"],
                        "scope_level": program["scope_level"],
                    }
                )

            program["hypothesis_list"] = self._stable_unique(program["hypothesis_list"] + [hypothesis["id"]])
            program["contradiction_list"] = self._stable_unique(
                program["contradiction_list"] + contradictions_by_hypothesis.get(hypothesis["id"], [])
            )
            program["solution_path_list"] = self._stable_unique(
                program["solution_path_list"] + paths_by_hypothesis.get(hypothesis["id"], [])
            )
            program["research_artifacts"] = self._stable_unique(
                program["research_artifacts"]
                + [item["evidence_ref"] for item in hypothesis.get("supporting_research", [])]
            )[:12]
            ranking = ranking_by_hypothesis.get(hypothesis["id"], {})
            program.setdefault("_scores", []).append(ranking.get("opportunity_score", 0.0))
            program.setdefault("_novelty", []).append(hypothesis.get("novelty_score", 0))
            program.setdefault("_feasibility", []).append(hypothesis.get("feasibility_score", 0))

        for program in programs:
            scores = program.pop("_scores", [])
            novelty_scores = program.pop("_novelty", [])
            feasibility_scores = program.pop("_feasibility", [])
            program["number_of_hypotheses"] = len(program["hypothesis_list"])
            program["number_of_resolved_contradictions"] = min(
                len(program["contradiction_list"]),
                len(program["solution_path_list"]),
            )
            program["novelty_trend"] = round(
                sum(novelty_scores) / max(len(novelty_scores), 1),
                2,
            ) if novelty_scores else program.get("novelty_trend", 0.0)
            program["feasibility_trend"] = round(
                sum(feasibility_scores) / max(len(feasibility_scores), 1),
                2,
            ) if feasibility_scores else program.get("feasibility_trend", 0.0)
            if scores:
                program["opportunity_score"] = round(
                    (sum(scores) / len(scores) * 0.75) + (program["frontier_score"] * 0.25),
                    3,
                )
            elif program["number_of_hypotheses"] == 0:
                program["opportunity_score"] = round(program["frontier_score"] * 0.5, 3)
            program["program_status"] = self._program_status(program, cycle_count=cycle_count)
            program["last_exploration_cycle"] = cycle_count
            telemetry_events.append(
                {
                    "event": "program_updated",
                    "program_id": program["program_id"],
                    "program_status": program["program_status"],
                    "scope_level": program["scope_level"],
                }
            )

        programs, governance_summary, governance_events = self._govern_programs(
            programs=programs,
            cycle_count=cycle_count,
        )
        telemetry_events.extend(governance_events)
        for program in programs[:3]:
            telemetry_events.append(
                {
                    "event": "program_prioritized",
                    "program_id": program["program_id"],
                    "opportunity_score": program["opportunity_score"],
                    "scope_level": program["scope_level"],
                    "execution_state": program["execution_state"],
                }
            )

        updated_map = self._attach_program_nodes(
            discovery_map=program_report["updated_discovery_map"],
            active_programs=programs,
        )
        updated_map = self._attach_program_relationships(
            discovery_map=updated_map,
            active_programs=programs,
        )
        return {
            "type": "RESEARCH_PROGRAM_REPORT",
            "cycle_count": cycle_count,
            "active_programs": programs,
            "master_program_tree": self._build_master_program_tree(programs),
            "governance_summary": governance_summary,
            "updated_discovery_map": updated_map,
            "telemetry_events": telemetry_events,
        }

    def annotate_hypotheses(
        self,
        *,
        hypothesis_packet: dict[str, Any],
        program_report: dict[str, Any],
    ) -> dict[str, Any]:
        annotated = dict(hypothesis_packet)
        programs = program_report.get("active_programs", [])
        program_by_hypothesis = {
            hypothesis_id: program
            for program in programs
            for hypothesis_id in (program.get("hypothesis_list", []) + program.get("archived_hypotheses", []))
        }
        hypotheses = []
        for hypothesis in hypothesis_packet.get("hypotheses", []):
            enriched = dict(hypothesis)
            program = program_by_hypothesis.get(hypothesis["id"])
            if program is not None:
                enriched["program_id"] = program["program_id"]
                enriched["scope_level"] = program["scope_level"]
                enriched["domain"] = program["target_domain"]
            hypotheses.append(enriched)
        annotated["hypotheses"] = hypotheses
        return annotated

    def _seed_program_specs(
        self,
        *,
        command_prompt: str,
        frontier_model: dict[str, Any],
        cross_industry_report: dict[str, Any],
        research_director_directives: dict[str, Any] | None,
    ) -> list[dict[str, Any]]:
        lower_prompt = command_prompt.lower()
        prompt_tokens = self._signal_tokens(command_prompt)
        specs = []
        if research_director_directives:
            for candidate in research_director_directives.get("spawn_candidates", []):
                candidate_tokens = self._signal_tokens(candidate["target_domain"] + " " + candidate["program_title"])
                if prompt_tokens and not (prompt_tokens & candidate_tokens):
                    continue
                specs.append(
                    {
                        "program_title": candidate["program_title"],
                        "target_domain": candidate["target_domain"],
                        "program_goal": candidate["program_goal"],
                        "program_kind": "domain",
                        "scope_level": self._infer_scope_level(
                            target_domain=candidate["target_domain"],
                            title=candidate["program_title"],
                            goal=candidate["program_goal"],
                        ),
                        "frontier_score": candidate["priority_score"],
                    }
                )
        if any(token in lower_prompt for token in ("cool", "thermal", "heat", "data center")):
            specs.append(
                {
                    "program_title": "Data Center Thermal Systems",
                    "target_domain": "data center cooling",
                    "program_goal": "Develop low-energy thermal architectures for high-density compute environments.",
                    "program_kind": "domain",
                    "scope_level": "L2",
                    "frontier_score": 0.84,
                }
            )
        if cross_industry_report.get("analogies"):
            specs.append(
                {
                    "program_title": "Cross-Domain Thermal Analogies",
                    "target_domain": "cross-domain cooling analogies",
                    "program_goal": "Transfer high-efficiency thermal patterns from adjacent industries into data center cooling.",
                    "program_kind": "cross_domain",
                    "scope_level": "L3",
                    "frontier_score": 0.79,
                }
            )
        if len(specs) < 2:
            for signal in frontier_model.get("frontier_signals", [])[:3]:
                domain = signal["domain"]
                if any(domain == item["target_domain"] for item in specs):
                    continue
                specs.append(
                    {
                        "program_title": f"{domain.title()} Research Program",
                        "target_domain": domain,
                        "program_goal": f"Systematically explore opportunity space around {domain}.",
                        "program_kind": "domain",
                        "scope_level": self._infer_scope_level(
                            target_domain=domain,
                            title=f"{domain.title()} Research Program",
                            goal=f"Systematically explore opportunity space around {domain}.",
                        ),
                        "frontier_score": round(signal["momentum"], 3),
                    }
                )
        return specs[:5]

    def _build_program(
        self,
        *,
        title: str,
        target_domain: str,
        goal: str,
        program_kind: str | None = None,
        scope_level: str | None = None,
        cycle_count: int,
        frontier_score: float,
        hypothesis_archive: list[dict[str, Any]],
    ) -> dict[str, Any]:
        program_kind = program_kind or self._program_kind(target_domain=target_domain, title=title)
        resolved_scope = scope_level or self._infer_scope_level(
            target_domain=target_domain,
            title=title,
            goal=goal,
        )
        program_id = self._program_id(f"{resolved_scope}:{target_domain}")
        archive_matches = [
            item
            for item in hypothesis_archive
            if self._matches_program(
                item["hypothesis"],
                target_domain,
                title,
                program_kind=program_kind,
                frontier_score=frontier_score,
            )
        ]
        archive_refs = [item["artifact_path"] for item in archive_matches][:8]
        archived_hypotheses = [item["hypothesis"]["id"] for item in archive_matches]
        return {
            "program_id": program_id,
            "program_title": title,
            "scope_level": resolved_scope,
            "target_domain": target_domain,
            "program_goal": goal,
            "program_kind": program_kind,
            "created_cycle": cycle_count,
            "hypothesis_list": [],
            "contradiction_list": [],
            "solution_path_list": [],
            "research_artifacts": archive_refs,
            "opportunity_score": round(frontier_score, 3),
            "program_status": "proposed",
            "execution_state": "proposed",
            "last_exploration_cycle": cycle_count,
            "number_of_hypotheses": 0,
            "number_of_resolved_contradictions": 0,
            "novelty_trend": 0.0,
            "feasibility_trend": 0.0,
            "frontier_score": round(frontier_score, 3),
            "active_hypothesis_count": 0,
            "archived_hypothesis_count": len(archived_hypotheses[:12]),
            "archived_hypotheses": archived_hypotheses[:12],
            "master_tree_path": ["Atrahasis Master Program Tree", resolved_scope, target_domain],
            "dependency_state": "clear",
            "governance_notes": [],
        }

    def _find_program(self, programs: list[dict[str, Any]], hypothesis: dict[str, Any]) -> dict[str, Any] | None:
        best_program = None
        best_score = 0.0
        for program in programs:
            score = self._program_match_score(hypothesis, program)
            if score > best_score:
                best_program = program
                best_score = score
        return best_program

    def _matches_program(
        self,
        hypothesis: dict[str, Any],
        target_domain: str,
        title: str,
        *,
        program_kind: str | None = None,
        frontier_score: float = 0.0,
    ) -> bool:
        score = self._program_match_score(
            hypothesis,
            {
                "target_domain": target_domain,
                "program_title": title,
                "program_kind": program_kind or self._program_kind(target_domain=target_domain, title=title),
                "frontier_score": frontier_score,
            },
        )
        resolved_kind = program_kind or self._program_kind(target_domain=target_domain, title=title)
        threshold = 0.55 if resolved_kind == "cross_domain" else 0.3
        return score >= threshold

    def _program_status(self, program: dict[str, Any], *, cycle_count: int) -> str:
        if program["number_of_hypotheses"] == 0:
            return "archived" if program.get("archived_hypotheses") else "proposed"
        if program.get("program_status") == "completed":
            return "completed"
        resolved_ready = (
            program["number_of_resolved_contradictions"] >= min(program["number_of_hypotheses"], 3)
            and bool(program["solution_path_list"])
        )
        mature_signal = (
            program["opportunity_score"] >= 0.78
            and program["novelty_trend"] >= 3.5
            and program["feasibility_trend"] >= 4.0
        )
        if program.get("program_status") == "stabilizing" and mature_signal:
            return "completed"
        if resolved_ready:
            return "stabilizing"
        if cycle_count - program.get("created_cycle", cycle_count) > 3 and program["opportunity_score"] < 0.28:
            return "archived"
        return "active"

    def _program_id(self, target_domain: str) -> str:
        digest = hashlib.md5(target_domain.encode("utf-8")).hexdigest()
        return f"RP-{int(digest, 16) % 1000:03d}"

    def _frontier_score(self, *, target_domain: str, frontier_model: dict[str, Any]) -> float:
        target_tokens = self._tokens(target_domain)
        best = 0.45
        for signal in frontier_model.get("frontier_signals", []):
            signal_tokens = self._tokens(signal["domain"])
            overlap = len(target_tokens & signal_tokens) / len(target_tokens | signal_tokens) if target_tokens and signal_tokens else 0.0
            if overlap > 0:
                best = max(best, signal["momentum"])
        return round(best, 3)

    def _program_match_score(self, hypothesis: dict[str, Any], program: dict[str, Any]) -> float:
        origin = hypothesis.get("origin", "domain")
        candidate_label = hypothesis.get("candidate_label")
        program_kind = program.get("program_kind") or self._program_kind(
            target_domain=program["target_domain"],
            title=program["program_title"],
        )
        haystack = " ".join(
            filter(
                None,
                [
                    hypothesis.get("title"),
                    hypothesis.get("statement"),
                    hypothesis.get("opportunity_zone"),
                    hypothesis.get("cross_domain_source"),
                    hypothesis.get("domain"),
                ],
            )
        ).lower()
        target_tokens = self._signal_tokens(program["target_domain"] + " " + program["program_title"])
        haystack_tokens = self._signal_tokens(haystack)
        if program_kind == "cross_domain":
            if origin != "cross_domain" and candidate_label != "Cross-Domain Opportunity":
                return 0.0
            overlap = len(haystack_tokens & target_tokens) / max(len(target_tokens), 1)
            strength_bonus = min(float(hypothesis.get("cross_domain_strength") or 0.5) * 0.2, 0.2)
            return round(min(0.55 + (overlap * 0.25) + strength_bonus, 1.0), 3)
        if origin == "cross_domain" or candidate_label == "Cross-Domain Opportunity":
            return 0.0
        if not target_tokens or not haystack_tokens:
            return 0.0
        overlap_count = len(haystack_tokens & target_tokens)
        if overlap_count == 0 and program["target_domain"] not in haystack:
            return 0.0
        overlap_ratio = overlap_count / max(len(target_tokens), 1)
        phrase_bonus = 0.2 if program["target_domain"] in haystack else 0.0
        frontier_bonus = min(float(program.get("frontier_score", 0.0)) * 0.1, 0.1)
        return round(min((overlap_ratio * 0.7) + phrase_bonus + frontier_bonus, 1.0), 3)

    def _program_kind(self, *, target_domain: str, title: str) -> str:
        descriptor = f"{target_domain} {title}".lower()
        if "cross-domain" in descriptor:
            return "cross_domain"
        return "domain"

    def _infer_scope_level(self, *, target_domain: str, title: str, goal: str) -> str:
        descriptor = f"{target_domain} {title} {goal}".lower()
        if any(token in descriptor for token in ("system architecture", "platform architecture", "runtime architecture")):
            return "L0"
        if any(token in descriptor for token in ("layer", "orchestr", "control plane", "memory layer")):
            return "L1"
        if any(token in descriptor for token in ("mechanism", "algorithm", "heuristic", "analogy", "microfluidic")):
            return "L3"
        if any(token in descriptor for token in ("optimiz", "tuning", "performance", "implementation")):
            return "L4"
        return "L2"

    def _govern_programs(
        self,
        *,
        programs: list[dict[str, Any]],
        cycle_count: int,
    ) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
        merged_programs: dict[tuple[str, str], dict[str, Any]] = {}
        telemetry_events: list[dict[str, Any]] = []
        for program in programs:
            key = (program["scope_level"], program["target_domain"])
            if key not in merged_programs:
                merged_programs[key] = dict(program)
                continue
            merged_programs[key] = self._merge_programs(merged_programs[key], program)
            telemetry_events.append(
                {
                    "event": "program_governance_merged",
                    "program_id": merged_programs[key]["program_id"],
                    "scope_level": merged_programs[key]["scope_level"],
                    "target_domain": merged_programs[key]["target_domain"],
                }
            )

        governed = list(merged_programs.values())
        for program in governed:
            active_hypotheses = list(program.get("hypothesis_list", []))
            archived_hypotheses = list(program.get("archived_hypotheses", []))
            if len(active_hypotheses) > self.MAX_ACTIVE_HYPOTHESES:
                overflow = active_hypotheses[self.MAX_ACTIVE_HYPOTHESES :]
                program["hypothesis_list"] = active_hypotheses[: self.MAX_ACTIVE_HYPOTHESES]
                archived_hypotheses.extend(overflow)
                program["archived_hypotheses"] = [
                    item for item in self._stable_unique(archived_hypotheses)
                    if item not in program["hypothesis_list"]
                ]
                telemetry_events.append(
                    {
                        "event": "program_hypotheses_archived",
                        "program_id": program["program_id"],
                        "archived_count": len(overflow),
                    }
                )
                program.setdefault("governance_notes", []).append(
                    f"Hypothesis capacity reached; archived {len(overflow)} overflow hypotheses."
                )
            else:
                program["archived_hypotheses"] = [
                    item for item in self._stable_unique(archived_hypotheses)
                    if item not in program["hypothesis_list"]
                ]

            program["active_hypothesis_count"] = len(program["hypothesis_list"])
            program["archived_hypothesis_count"] = len(program["archived_hypotheses"])
            program["number_of_hypotheses"] = len(program["hypothesis_list"])
            if program["program_status"] == "archived":
                program["execution_state"] = "archived"
            elif program["program_status"] == "completed":
                program["execution_state"] = "completed"
            elif program["program_status"] == "proposed":
                program["execution_state"] = "proposed"
            else:
                program["execution_state"] = "active"
            program["last_exploration_cycle"] = cycle_count
            program["master_tree_path"] = ["Atrahasis Master Program Tree", program["scope_level"], program["target_domain"]]
            program.setdefault("dependency_state", "clear")

        l0_active = [
            program
            for program in governed
            if program["scope_level"] == "L0" and program["execution_state"] == "active"
        ]
        if l0_active:
            for program in governed:
                if program["scope_level"] == "L0":
                    continue
                if self._depends_on_l0(program=program, l0_programs=l0_active):
                    program["execution_state"] = "paused_by_l0_governance"
                    program["dependency_state"] = f"paused_for_{l0_active[0]['program_id']}"
                    program.setdefault("governance_notes", []).append(
                        f"Paused because {l0_active[0]['program_id']} is exploring system-architecture decisions."
                    )
                    telemetry_events.append(
                        {
                            "event": "program_paused_for_l0",
                            "program_id": program["program_id"],
                            "blocking_program_id": l0_active[0]["program_id"],
                        }
                    )

        governed.sort(
            key=lambda item: (
                item.get("execution_state") == "active",
                item.get("opportunity_score", 0.0),
                -self.SCOPE_LEVELS.index(item["scope_level"]),
            ),
            reverse=True,
        )
        summary = {
            "active_program_count": len([item for item in governed if item["execution_state"] == "active"]),
            "paused_program_count": len([item for item in governed if item["execution_state"].startswith("paused")]),
            "completed_program_count": len([item for item in governed if item["execution_state"] == "completed"]),
            "archived_program_count": len([item for item in governed if item["execution_state"] == "archived"]),
            "enforced_hypothesis_capacity": self.MAX_ACTIVE_HYPOTHESES,
            "l0_blockers": [item["program_id"] for item in l0_active],
        }
        return governed, summary, telemetry_events

    def _depends_on_l0(self, *, program: dict[str, Any], l0_programs: list[dict[str, Any]]) -> bool:
        program_tokens = self._signal_tokens(program["target_domain"] + " " + program["program_title"])
        for blocker in l0_programs:
            blocker_tokens = self._signal_tokens(blocker["target_domain"] + " " + blocker["program_title"])
            if not blocker_tokens:
                continue
            if {"system", "architecture", "platform"} & blocker_tokens:
                return True
            if program_tokens & blocker_tokens:
                return True
        return False

    def _merge_programs(self, primary: dict[str, Any], secondary: dict[str, Any]) -> dict[str, Any]:
        merged = dict(primary)
        for key in (
            "hypothesis_list",
            "contradiction_list",
            "solution_path_list",
            "research_artifacts",
            "archived_hypotheses",
            "governance_notes",
        ):
            merged[key] = self._stable_unique(primary.get(key, []) + secondary.get(key, []))
        merged["opportunity_score"] = round(
            max(primary.get("opportunity_score", 0.0), secondary.get("opportunity_score", 0.0)),
            3,
        )
        merged["frontier_score"] = round(
            max(primary.get("frontier_score", 0.0), secondary.get("frontier_score", 0.0)),
            3,
        )
        merged["novelty_trend"] = round(
            max(primary.get("novelty_trend", 0.0), secondary.get("novelty_trend", 0.0)),
            2,
        )
        merged["feasibility_trend"] = round(
            max(primary.get("feasibility_trend", 0.0), secondary.get("feasibility_trend", 0.0)),
            2,
        )
        merged["created_cycle"] = min(primary.get("created_cycle", 0), secondary.get("created_cycle", 0))
        merged["last_exploration_cycle"] = max(
            primary.get("last_exploration_cycle", 0),
            secondary.get("last_exploration_cycle", 0),
        )
        return merged

    def _build_master_program_tree(self, programs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "program_id": program["program_id"],
                "scope_level": program["scope_level"],
                "target_domain": program["target_domain"],
                "path": program["master_tree_path"],
                "execution_state": program["execution_state"],
            }
            for program in programs
        ]

    def _attach_program_nodes(
        self,
        *,
        discovery_map: dict[str, Any],
        active_programs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        nodes = [dict(node) for node in discovery_map.get("nodes", discovery_map.get("entities", []))]
        edges = [dict(edge) for edge in discovery_map.get("edges", discovery_map.get("relationships", []))]
        node_ids = {node["id"] for node in nodes}
        edge_keys = {(edge["from"], edge["to"], edge["type"]) for edge in edges}
        for program in active_programs:
            node_id = f"program:{program['program_id']}"
            self._append_node(
                nodes,
                node_ids,
                {
                    "id": node_id,
                    "type": "research_program",
                    "label": program["program_title"],
                    "opportunity_score": program["opportunity_score"],
                    "program_status": program["program_status"],
                    "execution_state": program["execution_state"],
                    "scope_level": program["scope_level"],
                },
            )
            concept_id = f"concept:{program['target_domain']}"
            self._append_node(
                nodes,
                node_ids,
                {
                    "id": concept_id,
                    "type": "concept",
                    "label": program["target_domain"],
                },
            )
            self._append_edge(edges, edge_keys, node_id, concept_id, "targets_domain")
        enriched = dict(discovery_map)
        enriched["nodes"] = nodes
        enriched["edges"] = edges
        enriched["entities"] = nodes
        enriched["relationships"] = edges
        return enriched

    def _attach_program_relationships(
        self,
        *,
        discovery_map: dict[str, Any],
        active_programs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        nodes = [dict(node) for node in discovery_map.get("nodes", discovery_map.get("entities", []))]
        edges = [dict(edge) for edge in discovery_map.get("edges", discovery_map.get("relationships", []))]
        node_ids = {node["id"] for node in nodes}
        edge_keys = {(edge["from"], edge["to"], edge["type"]) for edge in edges}
        for program in active_programs:
            program_node = f"program:{program['program_id']}"
            for hypothesis_id in program["hypothesis_list"]:
                self._append_edge(edges, edge_keys, program_node, hypothesis_id, "contains_hypothesis")
            for contradiction_id in program["contradiction_list"]:
                self._append_edge(edges, edge_keys, program_node, contradiction_id, "tracks_contradiction")
            for path_id in program["solution_path_list"]:
                self._append_edge(edges, edge_keys, program_node, path_id, "tracks_solution_path")
        enriched = dict(discovery_map)
        enriched["nodes"] = nodes
        enriched["edges"] = edges
        enriched["entities"] = nodes
        enriched["relationships"] = edges
        return enriched

    def _append_node(self, nodes: list[dict[str, Any]], node_ids: set[str], node: dict[str, Any]) -> None:
        if node["id"] in node_ids:
            return
        nodes.append(node)
        node_ids.add(node["id"])

    def _append_edge(
        self,
        edges: list[dict[str, Any]],
        edge_keys: set[tuple[str, str, str]],
        source: str,
        target: str,
        edge_type: str,
    ) -> None:
        key = (source, target, edge_type)
        if key in edge_keys:
            return
        edges.append({"from": source, "to": target, "type": edge_type})
        edge_keys.add(key)

    def _stable_unique(self, values: list[str]) -> list[str]:
        ordered = []
        seen = set()
        for value in values:
            if value in seen:
                continue
            ordered.append(value)
            seen.add(value)
        return ordered

    def _tokens(self, text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z][a-z0-9_-]{3,}", text.lower())
        }

    def _signal_tokens(self, text: str) -> set[str]:
        return {
            token
            for token in self._tokens(text)
            if token not in self.NON_SIGNAL_TOKENS
        }
