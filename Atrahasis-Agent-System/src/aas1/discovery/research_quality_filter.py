from __future__ import annotations

from typing import Any


class ResearchQualityFilter:
    CATEGORY_BONUS = {
        "core_doc": 0.2,
        "task_workspace": 0.25,
        "prior_art": 0.3,
        "specification": 0.25,
        "invention_log": 0.2,
    }

    def run(self, *, ingestion_report: dict[str, Any]) -> dict[str, Any]:
        ranked = []
        for item in ingestion_report["evidence"]:
            score = 0.35
            score += self.CATEGORY_BONUS.get(item["category"], 0.0)
            score += min(item["word_count"] / 3000, 0.2)
            ranked.append({**item, "quality_score": round(min(score, 1.0), 3)})
        ranked.sort(key=lambda item: item["quality_score"], reverse=True)
        return {
            "type": "RESEARCH_QUALITY_REPORT",
            "ranked_evidence": ranked,
            "high_quality_count": sum(1 for item in ranked if item["quality_score"] >= 0.7),
        }
