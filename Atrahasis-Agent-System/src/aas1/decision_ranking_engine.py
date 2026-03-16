from __future__ import annotations

import re
from typing import Any


class DecisionRankingEngine:
    DISPLAY_LIMIT = 5
    WEIGHTS = {
        "novelty_score": 0.24,
        "feasibility_score": 0.18,
        "contradiction_importance": 0.22,
        "technology_frontier_proximity": 0.14,
        "research_support_strength": 0.10,
        "cross_domain_analogy_strength": 0.07,
        "discovery_gap_priority": 0.05,
    }
    SEVERITY_SCORES = {"critical": 1.0, "high": 0.9, "medium": 0.6, "low": 0.35}

    def run(
        self,
        *,
        hypothesis_packet: dict[str, Any],
        contradiction_map: dict[str, Any],
        novelty_report: dict[str, Any],
        feasibility_report: dict[str, Any],
        frontier_model: dict[str, Any],
        quality_report: dict[str, Any],
        analogy_report: dict[str, Any],
        gap_report: dict[str, Any],
        opportunity_report: dict[str, Any],
        solution_paths: dict[str, Any],
        platform_alignment_report: dict[str, Any],
    ) -> dict[str, Any]:
        evidence_quality = {
            item["path"]: item["quality_score"]
            for item in quality_report["ranked_evidence"]
        }
        contradictions = {
            item["hypothesis_id"]: item
            for item in contradiction_map["contradictions"]
        }
        novelty = {
            item["hypothesis_id"]: item
            for item in novelty_report.get("hypothesis_assessments", [])
        }
        feasibility = {
            item["hypothesis_id"]: item
            for item in feasibility_report.get("hypothesis_assessments", [])
        }
        frontier_domains = [item["domain"] for item in frontier_model.get("frontier_signals", [])]
        breakthrough_candidates = frontier_model.get("breakthrough_candidates", [])
        opportunity_zones = [item["zone"] for item in opportunity_report.get("high_impact_hypothesis_zones", [])]
        path_lookup = {
            path["hypothesis_id"]: path
            for path in solution_paths.get("candidate_paths", [])
        }
        platform_alignment = {
            item["hypothesis_id"]: item
            for item in platform_alignment_report.get("hypothesis_assessments", [])
        }

        ranked_hypotheses = []
        total_hypotheses = max(len(hypothesis_packet["hypotheses"]), 1)
        max_support_count = max(
            (len(item.get("supporting_research", [])) for item in hypothesis_packet["hypotheses"]),
            default=1,
        )
        for index, hypothesis in enumerate(hypothesis_packet["hypotheses"], start=1):
            support_refs = [item["evidence_ref"] for item in hypothesis.get("supporting_research", [])]
            research_support = self._research_support_strength(
                support_refs=support_refs,
                evidence_quality=evidence_quality,
                max_support_count=max_support_count,
            )
            contradiction_importance = self._contradiction_importance(
                contradictions.get(hypothesis["id"]),
            )
            frontier_proximity = self._frontier_proximity(
                hypothesis=hypothesis,
                frontier_domains=frontier_domains,
                breakthrough_candidates=breakthrough_candidates,
                opportunity_zones=opportunity_zones,
            )
            analogy_strength = self._analogy_strength(
                hypothesis=hypothesis,
                analogy_report=analogy_report,
                hypothesis_index=index - 1,
                total_hypotheses=total_hypotheses,
            )
            gap_priority = self._discovery_gap_priority(
                support_strength=research_support,
                gap_report=gap_report,
            )
            normalized_signals = {
                "novelty_score": self._normalize_five_point(novelty.get(hypothesis["id"], {}).get("novelty_score", 0)),
                "feasibility_score": self._normalize_five_point(
                    feasibility.get(hypothesis["id"], {}).get("feasibility_score", 0)
                ),
                "contradiction_importance": contradiction_importance,
                "technology_frontier_proximity": frontier_proximity,
                "research_support_strength": research_support,
                "cross_domain_analogy_strength": analogy_strength,
                "discovery_gap_priority": gap_priority,
            }
            opportunity_score = round(
                sum(self.WEIGHTS[key] * value for key, value in normalized_signals.items()),
                3,
            )
            alignment_entry = platform_alignment.get(hypothesis["id"], {})
            priority_adjustment = round(float(alignment_entry.get("priority_adjustment", 0.0)), 3)
            platform_alignment_score = round(float(alignment_entry.get("platform_alignment_score", 0.65)), 3)
            adjusted_opportunity_score = round(
                min(max(opportunity_score + priority_adjustment, 0.0), 1.0),
                3,
            )
            recommended_path = path_lookup.get(hypothesis["id"])
            ranked_hypotheses.append(
                {
                    "hypothesis_id": hypothesis["id"],
                    "title": hypothesis["title"],
                    "opportunity_zone": hypothesis.get("opportunity_zone"),
                    "candidate_label": hypothesis.get("candidate_label", "Top Exploration Candidate"),
                    "origin": hypothesis.get("origin", "domain"),
                    "opportunity_score": adjusted_opportunity_score,
                    "base_opportunity_score": opportunity_score,
                    "platform_alignment_score": platform_alignment_score,
                    "priority_adjustment": priority_adjustment,
                    "recommended_path_id": recommended_path["id"] if recommended_path else None,
                    "recommended_path_title": recommended_path["title"] if recommended_path else None,
                    "normalized_signals": normalized_signals,
                }
            )

        ranked_hypotheses.sort(
            key=lambda item: (
                item["opportunity_score"],
                item["normalized_signals"]["novelty_score"],
                item["normalized_signals"]["contradiction_importance"],
            ),
            reverse=True,
        )
        presentation_limit = self.DISPLAY_LIMIT if len(ranked_hypotheses) > self.DISPLAY_LIMIT else len(ranked_hypotheses)
        for rank, item in enumerate(ranked_hypotheses, start=1):
            item["rank"] = rank
            item["display_to_operator"] = rank <= presentation_limit

        return {
            "type": "DECISION_RANKING_REPORT",
            "candidate_count": len(ranked_hypotheses),
            "presentation_limit": presentation_limit,
            "ranked_hypotheses": ranked_hypotheses,
            "display_candidates": [item for item in ranked_hypotheses if item["display_to_operator"]],
        }

    def _normalize_five_point(self, value: int) -> float:
        if value <= 0:
            return 0.0
        return round((value - 1) / 4, 3)

    def _research_support_strength(
        self,
        *,
        support_refs: list[str],
        evidence_quality: dict[str, float],
        max_support_count: int,
    ) -> float:
        if not support_refs:
            return 0.0
        avg_quality = sum(evidence_quality.get(ref, 0.55) for ref in support_refs) / len(support_refs)
        coverage = len(set(support_refs)) / max(max_support_count, 1)
        return round(min((avg_quality * 0.65) + (coverage * 0.35), 1.0), 3)

    def _contradiction_importance(self, contradiction: dict[str, Any] | None) -> float:
        if contradiction is None:
            return 0.25
        return self.SEVERITY_SCORES.get(contradiction.get("severity", "medium").lower(), 0.6)

    def _frontier_proximity(
        self,
        *,
        hypothesis: dict[str, Any],
        frontier_domains: list[str],
        breakthrough_candidates: list[str],
        opportunity_zones: list[str],
    ) -> float:
        tokens = self._tokens(" ".join(filter(None, [hypothesis.get("opportunity_zone"), hypothesis["title"]])))
        comparisons = frontier_domains + breakthrough_candidates + opportunity_zones
        if not comparisons:
            return 0.5
        best = 0.0
        for candidate in comparisons:
            candidate_tokens = self._tokens(candidate)
            if not candidate_tokens:
                continue
            overlap = len(tokens & candidate_tokens) / len(tokens | candidate_tokens)
            best = max(best, overlap)
        return round(max(best, 0.35), 3)

    def _analogy_strength(
        self,
        *,
        hypothesis: dict[str, Any],
        analogy_report: dict[str, Any],
        hypothesis_index: int,
        total_hypotheses: int,
    ) -> float:
        if hypothesis.get("cross_domain_strength") is not None:
            return round(float(hypothesis["cross_domain_strength"]), 3)
        analogies = analogy_report.get("analogies", [])
        if not analogies:
            return 0.4
        analogy = analogies[hypothesis_index % len(analogies)]
        tokens = self._tokens(" ".join(filter(None, [hypothesis.get("opportunity_zone"), hypothesis["title"]])))
        target_tokens = self._tokens(analogy.get("target_zone", ""))
        overlap = len(tokens & target_tokens) / len(tokens | target_tokens) if tokens and target_tokens else 0.0
        sequence_bonus = max(0.3, 1 - (hypothesis_index / max(total_hypotheses, 1)))
        return round(min(max(overlap, sequence_bonus), 1.0), 3)

    def _discovery_gap_priority(self, *, support_strength: float, gap_report: dict[str, Any]) -> float:
        if not gap_report.get("gaps"):
            return round(min(0.65 + (support_strength * 0.2), 1.0), 3)
        severity_bonus = 0.0
        for gap in gap_report["gaps"]:
            severity_bonus += 0.2 if gap.get("severity") == "high" else 0.1
        normalized_gap_pressure = min(severity_bonus, 1.0)
        return round(min((support_strength * 0.6) + (normalized_gap_pressure * 0.4), 1.0), 3)

    def _tokens(self, text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z][a-z0-9_-]{3,}", text.lower())
        }
