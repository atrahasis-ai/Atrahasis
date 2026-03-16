from __future__ import annotations

from collections import Counter
from typing import Any

from aas5.common import keyword_profile


class ResearchSynthesisEngine:
    def run(self, *, quality_report: dict[str, Any]) -> dict[str, Any]:
        evidence = quality_report["ranked_evidence"][:40]
        focused_evidence = [
            item for item in quality_report["ranked_evidence"]
            if item["category"] == "task_workspace"
        ][:12]
        category_counts = Counter(item["category"] for item in evidence)
        keyword_texts = [item["text"] for item in evidence]
        keyword_texts.extend(item["text"] for item in focused_evidence)
        keyword_texts.extend(item["summary"] for item in focused_evidence)
        keywords = keyword_profile(keyword_texts, limit=15)
        clusters = [
            {"cluster": category, "evidence_count": count}
            for category, count in category_counts.most_common()
        ]
        return {
            "type": "RESEARCH_SYNTHESIS_REPORT",
            "research_clusters": clusters,
            "top_keywords": keywords,
            "synthesis_summary": [
                f"{cluster['cluster']}:{cluster['evidence_count']}" for cluster in clusters[:6]
            ],
        }
