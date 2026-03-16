from __future__ import annotations

import re
from typing import Any

from aas1.common import keyword_profile


class PlatformAlignmentEngine:
    PLATFORM_TOKENS = {
        "atrahasis",
        "platform",
        "architecture",
        "invention",
        "research",
        "human",
        "operator",
        "guidance",
    }

    def run(
        self,
        *,
        hypothesis_packet: dict[str, Any],
        research_program_report: dict[str, Any],
        value_alignment_report: dict[str, Any],
        architecture_model: dict[str, Any],
    ) -> dict[str, Any]:
        platform_objectives = self._platform_objectives(architecture_model)
        program_scores = {
            item["program_id"]: item["value_alignment_score"]
            for item in value_alignment_report.get("program_alignment", [])
        }
        value_scores = {
            item["hypothesis_id"]: item["value_alignment_score"]
            for item in value_alignment_report.get("hypothesis_alignment", [])
        }

        hypothesis_assessments = []
        filtered_hypotheses = []
        program_rollups: dict[str, list[float]] = {}
        for hypothesis in hypothesis_packet["hypotheses"]:
            program = self._match_program(hypothesis=hypothesis, research_program_report=research_program_report)
            mission_overlap = self._mission_overlap(hypothesis=hypothesis, platform_objectives=platform_objectives)
            value_score = value_scores.get(hypothesis["id"], 0.65)
            program_score = program_scores.get(program["program_id"], 0.65) if program else 0.65
            platform_alignment_score = round(
                (mission_overlap * 0.45) + (value_score * 0.35) + (program_score * 0.20),
                3,
            )
            priority_adjustment = self._priority_adjustment(platform_alignment_score)
            if platform_alignment_score < 0.35:
                filtered_hypotheses.append(hypothesis["id"])
            if program is not None:
                program_rollups.setdefault(program["program_id"], []).append(platform_alignment_score)
            hypothesis_assessments.append(
                {
                    "hypothesis_id": hypothesis["id"],
                    "program_id": program["program_id"] if program else None,
                    "platform_alignment_score": platform_alignment_score,
                    "priority_adjustment": priority_adjustment,
                    "alignment_status": self._alignment_status(platform_alignment_score),
                }
            )

        program_recommendations = []
        for program in research_program_report.get("active_programs", []):
            avg_alignment = round(
                sum(program_rollups.get(program["program_id"], [])) / max(len(program_rollups.get(program["program_id"], [])), 1),
                3,
            ) if program_rollups.get(program["program_id"]) else 0.65
            action = self._program_action(avg_alignment=avg_alignment, opportunity_score=program.get("opportunity_score", 0.0))
            program_recommendations.append(
                {
                    "program_id": program["program_id"],
                    "program_title": program["program_title"],
                    "platform_alignment_score": avg_alignment,
                    "recommended_action": action,
                }
            )

        telemetry_events = [
            {
                "event": "platform_alignment_generated",
                "filtered_hypothesis_count": len(filtered_hypotheses),
                "average_alignment_score": round(
                    sum(item["platform_alignment_score"] for item in hypothesis_assessments)
                    / max(len(hypothesis_assessments), 1),
                    3,
                ),
            }
        ]

        return {
            "type": "PLATFORM_ALIGNMENT_REPORT",
            "platform_objectives": sorted(platform_objectives)[:24],
            "hypothesis_assessments": hypothesis_assessments,
            "filtered_hypotheses": filtered_hypotheses,
            "program_recommendations": program_recommendations,
            "telemetry_events": telemetry_events,
        }

    def _platform_objectives(self, architecture_model: dict[str, Any]) -> set[str]:
        texts = [item.get("summary", "") for item in architecture_model.get("documents", [])]
        texts.extend(item.get("text", "") for item in architecture_model.get("documents", []))
        return set(keyword_profile(texts, limit=16)) | self.PLATFORM_TOKENS

    def _match_program(
        self,
        *,
        hypothesis: dict[str, Any],
        research_program_report: dict[str, Any],
    ) -> dict[str, Any] | None:
        if hypothesis.get("origin") == "cross_domain" or hypothesis.get("candidate_label") == "Cross-Domain Opportunity":
            for program in research_program_report.get("active_programs", []):
                descriptor = f"{program['program_title']} {program['target_domain']}".lower()
                if "cross-domain" in descriptor:
                    return program
        haystack = self._tokens(
            " ".join(
                filter(
                    None,
                    [
                        hypothesis.get("title"),
                        hypothesis.get("statement"),
                        hypothesis.get("opportunity_zone"),
                    ],
                )
            )
        )
        best_program = None
        best_score = 0.0
        for program in research_program_report.get("active_programs", []):
            target_tokens = self._tokens(f"{program['target_domain']} {program['program_title']}")
            if not target_tokens:
                continue
            overlap = len(haystack & target_tokens) / max(len(target_tokens), 1)
            if overlap > best_score:
                best_score = overlap
                best_program = program
        return best_program

    def _mission_overlap(self, *, hypothesis: dict[str, Any], platform_objectives: set[str]) -> float:
        tokens = self._tokens(
            " ".join(
                filter(
                    None,
                    [
                        hypothesis.get("title"),
                        hypothesis.get("statement"),
                        hypothesis.get("summary"),
                        hypothesis.get("opportunity_zone"),
                    ],
                )
            )
        )
        if not tokens:
            return 0.35
        overlap = len(tokens & platform_objectives) / max(len(tokens), 1)
        return round(max(overlap, 0.35), 3)

    def _priority_adjustment(self, alignment_score: float) -> float:
        if alignment_score < 0.35:
            return -0.18
        if alignment_score >= 0.8:
            return max(round((alignment_score - 0.5) * 0.2, 3), 0.08)
        if alignment_score >= 0.65:
            return max(round((alignment_score - 0.5) * 0.2, 3), 0.03)
        return round((alignment_score - 0.5) * 0.2, 3)

    def _alignment_status(self, alignment_score: float) -> str:
        if alignment_score >= 0.65:
            return "aligned"
        if alignment_score < 0.35:
            return "deprioritized"
        return "neutral"

    def _program_action(self, *, avg_alignment: float, opportunity_score: float) -> str:
        if avg_alignment < 0.35:
            return "pause_program"
        if avg_alignment >= 0.7 and opportunity_score >= 0.6:
            return "continue_program"
        return "continue_program"

    def _tokens(self, text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z][a-z0-9_-]{3,}", text.lower())
        }
