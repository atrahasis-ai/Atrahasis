from __future__ import annotations

from typing import Any


class DiscoveryGapDetector:
    REQUIRED_CATEGORIES = ("core_doc", "task_workspace", "prior_art", "specification", "invention_log")

    def run(self, *, quality_report: dict[str, Any]) -> dict[str, Any]:
        present = {item["category"] for item in quality_report["ranked_evidence"]}
        gaps = []
        for category in self.REQUIRED_CATEGORIES:
            if category not in present:
                gaps.append(
                    {
                        "gap": f"missing_{category}",
                        "severity": "high" if category in {"prior_art", "specification"} else "medium",
                    }
                )
        return {
            "type": "DISCOVERY_GAP_REPORT",
            "gaps": gaps,
            "gap_count": len(gaps),
        }
