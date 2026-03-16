from __future__ import annotations

from typing import Any


class SolutionPathGenerator:
    def run(
        self,
        *,
        hypothesis_packet: dict[str, Any],
        contradiction_map: dict[str, Any],
        cluster_report: dict[str, Any],
    ) -> dict[str, Any]:
        candidate_paths = []
        for index, hypothesis in enumerate(hypothesis_packet["hypotheses"], start=1):
            candidate_paths.append(
                {
                    "id": f"P-{index:03d}",
                    "hypothesis_id": hypothesis["id"],
                    "title": self._path_title(hypothesis, index),
                    "required_subsystems": ["discovery", "reasoning", "validation", "governance"],
                    "tradeoffs": ["novelty_vs_feasibility", "breadth_vs_depth"],
                    "dependency_order": ["discovery", "opportunity", "hypothesis", "validation", "human_review"],
                }
            )
        return {
            "type": "SOLUTION_PATH_SET",
            "candidate_paths": candidate_paths,
            "required_subsystems": ["discovery", "reasoning", "validation", "governance"],
            "tradeoffs": ["evidence_depth", "operator_time", "portfolio_complexity"],
            "dependency_order": ["intake", "discovery", "reasoning", "validation", "governance"],
        }

    def _path_title(self, hypothesis: dict[str, Any], index: int) -> str:
        text = f"{hypothesis['opportunity_zone']} {hypothesis['statement']}".lower()
        if "microfluidic" in text:
            return "Localized microfluidic cooling channels"
        if "immersion" in text or "dielectric" in text:
            return "Immersion cooling with dielectric fluids"
        if "phase" in text:
            return "Passive phase-change cooling plates"
        if "liquid" in text and "immersion" in text:
            return "Hybrid liquid and immersion cooling architecture"
        if "cool" in text or "thermal" in text:
            defaults = (
                "Hybrid liquid and immersion cooling architecture",
                "Passive phase-change cooling plates",
                "Localized microfluidic cooling channels",
            )
            return defaults[(index - 1) % len(defaults)]
        return f"Path for {hypothesis['title']}"
