from __future__ import annotations

from typing import Any


class TechnologyOpportunityScanner:
    def run(self, *, discovery_map: dict[str, Any], frontier_model: dict[str, Any]) -> dict[str, Any]:
        high_value_targets = [signal["domain"] for signal in frontier_model["frontier_signals"][:5]]
        emerging_clusters = [cluster["name"] for cluster in discovery_map["problem_clusters"][:5]]
        hypothesis_zones = [
            {
                "zone": signal["domain"],
                "priority_rank": index,
                "basis": "frontier_signal",
            }
            for index, signal in enumerate(frontier_model["frontier_signals"][:5], start=1)
        ]
        return {
            "type": "OPPORTUNITY_REPORT",
            "high_value_invention_targets": high_value_targets,
            "emerging_research_clusters": emerging_clusters,
            "high_impact_hypothesis_zones": hypothesis_zones,
            "priority_rank": 1,
        }
