from __future__ import annotations

from typing import Any


class ExperimentSimulationEngine:
    def run(self, *, solution_paths: dict[str, Any], feasibility_report: dict[str, Any]) -> dict[str, Any]:
        experiments = []
        for path in solution_paths["candidate_paths"][:5]:
            experiments.append(
                {
                    "path_id": path["id"],
                    "experiment": f"Validate {path['title']}",
                    "simulated_outcome": "promising" if feasibility_report["technical_feasibility"] >= 3 else "risky",
                    "failure_modes": feasibility_report["blocking_unknowns"],
                    "go_no_go_signals": ["operator_review_required", "prior_art_check_required"],
                }
            )
        return {"type": "EXPERIMENT_SIMULATION_REPORT", "experiments": experiments}
