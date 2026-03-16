from __future__ import annotations

from typing import Any


class NoveltyDetectionEngine:
    def run(self, *, hypothesis_packet: dict[str, Any], quality_report: dict[str, Any]) -> dict[str, Any]:
        prior_art_hits = sum(1 for item in quality_report["ranked_evidence"] if item["category"] == "prior_art")
        baseline_score = max(1, min(5, 5 - min(prior_art_hits // 8, 4)))
        hypothesis_assessments = []
        for index, hypothesis in enumerate(hypothesis_packet["hypotheses"], start=1):
            novelty_score = max(1, min(5, baseline_score + (1 if hypothesis["confidence"] >= 0.7 else 0) - ((index - 1) // 2)))
            hypothesis_assessments.append(
                {
                    "hypothesis_id": hypothesis["id"],
                    "novelty_score": novelty_score,
                    "collision_risk": "medium" if novelty_score >= 3 else "high",
                    "closest_prior_art": quality_report["ranked_evidence"][0]["path"] if quality_report["ranked_evidence"] else None,
                    "differentiators": [
                        hypothesis["title"],
                        hypothesis["statement"],
                    ],
                    "artifact_ref": f"NOVELTY_REPORT.json#{hypothesis['id']}",
                }
            )
        return {
            "type": "NOVELTY_REPORT",
            "closest_prior_art": quality_report["ranked_evidence"][0]["path"] if quality_report["ranked_evidence"] else None,
            "differentiators": [
                hypothesis["title"] for hypothesis in hypothesis_packet["hypotheses"][:3]
            ],
            "novelty_score": round(
                sum(item["novelty_score"] for item in hypothesis_assessments) / max(len(hypothesis_assessments), 1)
            ),
            "collision_risk": "medium" if baseline_score >= 3 else "high",
            "hypothesis_assessments": hypothesis_assessments,
        }
