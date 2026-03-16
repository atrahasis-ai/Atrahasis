from __future__ import annotations

from typing import Any


class ContradictionEngine:
    def run(self, *, hypothesis_packet: dict[str, Any], gap_report: dict[str, Any]) -> dict[str, Any]:
        contradictions = []
        for index, hypothesis in enumerate(hypothesis_packet["hypotheses"], start=1):
            contradictions.append(
                {
                    "id": f"X-{index:03d}",
                    "hypothesis_id": hypothesis["id"],
                    "contradiction": self._derive_contradiction(hypothesis, gap_report),
                    "severity": self._severity(hypothesis, gap_report),
                }
            )
        return {
            "type": "CONTRADICTION_MAP",
            "contradictions": contradictions,
            "affected_subsystems": ["research", "reasoning", "validation"],
            "blocking_assumptions": [gap["gap"] for gap in gap_report["gaps"]],
            "severity": "high" if gap_report["gap_count"] else "medium",
        }

    def _derive_contradiction(self, hypothesis: dict[str, Any], gap_report: dict[str, Any]) -> str:
        statement = hypothesis["statement"].lower()
        zone = hypothesis["opportunity_zone"].lower()
        if "cool" in statement or "thermal" in statement or "heat" in statement:
            if "density" in statement or "comput" in statement:
                return (
                    "Increasing computational density raises thermal load, while reducing cooling energy "
                    "requires minimizing active heat-removal overhead."
                )
            if "energy" in statement:
                return (
                    "Reducing cooling energy demands less active cooling effort, while maintaining thermal "
                    "stability requires higher heat-transfer performance."
                )
        if "immersion" in zone:
            return (
                "Immersion cooling can cut fan energy and support dense compute, but it increases fluid "
                "management complexity and retrofit burden."
            )
        if "microfluidic" in zone:
            return (
                "Microfluidic cooling improves localized heat extraction for dense compute, but embedded "
                "channels increase manufacturing complexity and failure risk."
            )
        if "phase" in zone:
            return (
                "Phase-change cooling reduces active energy demand, but passive thermal transport may "
                "struggle to match peak heat flux at very high compute density."
            )
        if gap_report["gap_count"]:
            return "High-opportunity zone with unresolved evidence gaps."
        return "Novelty must be validated against concentrated prior art."

    def _severity(self, hypothesis: dict[str, Any], gap_report: dict[str, Any]) -> str:
        statement = hypothesis["statement"].lower()
        if "cool" in statement or "thermal" in statement or gap_report["gap_count"]:
            return "high"
        return "medium"
