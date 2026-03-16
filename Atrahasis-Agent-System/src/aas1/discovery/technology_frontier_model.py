from __future__ import annotations

from typing import Any


class TechnologyFrontierModel:
    def run(self, *, synthesis_report: dict[str, Any], discovery_map: dict[str, Any]) -> dict[str, Any]:
        frontier_signals = []
        for index, keyword in enumerate(synthesis_report["top_keywords"][:8], start=1):
            frontier_signals.append(
                {
                    "domain": keyword,
                    "momentum": round(max(0.9 - index * 0.08, 0.2), 3),
                    "evidence_signal": min(index + 2, 10),
                }
            )
        return {
            "type": "TECHNOLOGY_FRONTIER_MODEL",
            "domain": "atrahasis_invention_intelligence",
            "frontier_signals": frontier_signals,
            "maturity_estimates": [
                {"cluster": cluster["name"], "maturity": "emerging" if cluster["signal"] < 6 else "active"}
                for cluster in discovery_map["problem_clusters"][:6]
            ],
            "breakthrough_candidates": [signal["domain"] for signal in frontier_signals[:4]],
        }
