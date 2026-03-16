from __future__ import annotations

import re
from typing import Any

from aas5.common import keyword_profile


class ValueAlignmentEngine:
    BASE_ALIGNMENT = 0.65
    MISSION_TOKENS = {
        "human",
        "guided",
        "invention",
        "research",
        "architecture",
        "platform",
        "operator",
        "analysis",
    }

    def run(
        self,
        *,
        hypothesis_packet: dict[str, Any],
        research_program_report: dict[str, Any],
        operator_constraints: list[str],
        hitl_requirements: list[str],
        architecture_model: dict[str, Any],
    ) -> dict[str, Any]:
        profile_tokens = self._profile_tokens(architecture_model)
        alignment_signals = []
        for hypothesis in hypothesis_packet["hypotheses"]:
            text = " ".join(
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
            tokens = self._tokens(text)
            mission_overlap = len(tokens & profile_tokens) / max(len(tokens), 1)
            human_guidance_bonus = 0.08 if operator_constraints or hitl_requirements else 0.0
            cross_domain_bonus = 0.04 if hypothesis.get("origin") == "cross_domain" else 0.0
            value_alignment_score = round(
                min(
                    self.BASE_ALIGNMENT
                    + (mission_overlap * 0.18)
                    + human_guidance_bonus
                    + cross_domain_bonus,
                    0.95,
                ),
                3,
            )
            alignment_signals.append(
                {
                    "hypothesis_id": hypothesis["id"],
                    "value_alignment_score": value_alignment_score,
                }
            )

        program_signals = []
        by_program = self._program_lookup(research_program_report)
        for program in research_program_report.get("active_programs", []):
            hypothesis_scores = [
                item["value_alignment_score"]
                for item in alignment_signals
                if item["hypothesis_id"] in by_program.get(program["program_id"], set())
            ]
            program_signals.append(
                {
                    "program_id": program["program_id"],
                    "value_alignment_score": round(
                        sum(hypothesis_scores) / max(len(hypothesis_scores), 1),
                        3,
                    ) if hypothesis_scores else self.BASE_ALIGNMENT,
                }
            )

        return {
            "type": "VALUE_ALIGNMENT_REPORT",
            "alignment_mode": "baseline_human_guided",
            "mission_profile": sorted(profile_tokens)[:20],
            "hypothesis_alignment": alignment_signals,
            "program_alignment": program_signals,
        }

    def _profile_tokens(self, architecture_model: dict[str, Any]) -> set[str]:
        texts = [item.get("summary", "") for item in architecture_model.get("documents", [])]
        texts.extend(item.get("text", "") for item in architecture_model.get("documents", []))
        return set(keyword_profile(texts, limit=16)) | self.MISSION_TOKENS

    def _program_lookup(self, research_program_report: dict[str, Any]) -> dict[str, set[str]]:
        return {
            item["program_id"]: set(item.get("hypothesis_list", []))
            for item in research_program_report.get("active_programs", [])
        }

    def _tokens(self, text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z][a-z0-9_-]{3,}", text.lower())
        }
