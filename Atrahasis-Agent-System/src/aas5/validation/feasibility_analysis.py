from __future__ import annotations

from typing import Any


class FeasibilityAnalysisEngine:
    def run(
        self,
        *,
        solution_paths: dict[str, Any],
        gap_report: dict[str, Any],
        hypothesis_packet: dict[str, Any],
    ) -> dict[str, Any]:
        blocker_count = gap_report["gap_count"]
        technical_feasibility = max(1, 5 - blocker_count)
        operational_feasibility = max(1, 4 - min(blocker_count, 3))
        hypothesis_assessments = []
        path_counts = {}
        for path in solution_paths["candidate_paths"]:
            path_counts[path["hypothesis_id"]] = path_counts.get(path["hypothesis_id"], 0) + 1

        for hypothesis in hypothesis_packet["hypotheses"]:
            path_bonus = 1 if path_counts.get(hypothesis["id"], 0) > 0 else 0
            feasibility_score = max(1, min(5, technical_feasibility + path_bonus - (0 if blocker_count == 0 else 1)))
            hypothesis_assessments.append(
                {
                    "hypothesis_id": hypothesis["id"],
                    "feasibility_score": feasibility_score,
                    "technical_feasibility": technical_feasibility,
                    "operational_feasibility": operational_feasibility,
                    "adoption_feasibility": 3,
                    "blocking_unknowns": [gap["gap"] for gap in gap_report["gaps"]],
                    "artifact_ref": f"FEASIBILITY_REPORT.json#{hypothesis['id']}",
                }
            )
        return {
            "type": "FEASIBILITY_REPORT",
            "technical_feasibility": technical_feasibility,
            "operational_feasibility": operational_feasibility,
            "adoption_feasibility": 3,
            "blocking_unknowns": [gap["gap"] for gap in gap_report["gaps"]],
            "hypothesis_assessments": hypothesis_assessments,
        }
