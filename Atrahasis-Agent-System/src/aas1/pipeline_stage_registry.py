from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StageDefinition:
    name: str
    handler_name: str
    description: str
    produced_artifacts: tuple[str, ...]
    supported_modifiers: tuple[str, ...] = ("AASBT", "AASAQ", "AASNI", "AASA")


COMMAND_EXECUTION_PROFILES = {
    "AASBT": {
        "profile_id": "buildout",
        "focus": "implementation_and_invention_delivery",
        "stage_order": ("knowledge_infrastructure", "reasoning_and_evaluation", "human_guidance"),
    },
    "AASAQ": {
        "profile_id": "architecture_question",
        "focus": "analysis_and_explanation",
        "stage_order": ("knowledge_infrastructure", "reasoning_and_evaluation", "human_guidance"),
    },
    "AASNI": {
        "profile_id": "new_idea_integration",
        "focus": "integration_and_impact_analysis",
        "stage_order": ("knowledge_infrastructure", "reasoning_and_evaluation", "human_guidance"),
    },
    "AASA": {
        "profile_id": "full_system_analysis",
        "focus": "broad_repository_analysis",
        "stage_order": ("knowledge_infrastructure", "reasoning_and_evaluation", "human_guidance"),
    },
}


class PipelineStageRegistry:
    """Registry-driven declaration of the AAS3 pipeline stages."""

    def __init__(self) -> None:
        self._stages = {
            "knowledge_infrastructure": StageDefinition(
                name="knowledge_infrastructure",
                handler_name="_run_stage_knowledge",
                description="Ingest repo knowledge, build discovery state, and seed governed programs.",
                produced_artifacts=(
                    "research_ingestion_report",
                    "research_quality_report",
                    "research_synthesis_report",
                    "cross_industry_discovery_report",
                    "knowledge_distillation_report",
                    "discovery_map",
                    "technology_frontier_model",
                ),
            ),
            "reasoning_and_evaluation": StageDefinition(
                name="reasoning_and_evaluation",
                handler_name="_run_stage_reasoning_and_evaluation",
                description="Generate and evaluate invention hypotheses within governed research programs.",
                produced_artifacts=(
                    "discovery_gap_report",
                    "opportunity_report",
                    "analogy_report",
                    "hypothesis_packet",
                    "idea_cluster_report",
                    "contradiction_map",
                    "solution_path_set",
                    "novelty_report",
                    "feasibility_report",
                    "value_alignment_report",
                    "platform_alignment_report",
                    "decision_ranking_report",
                    "research_program_report",
                    "research_strategy_report",
                    "experiment_simulation_report",
                ),
            ),
            "human_guidance": StageDefinition(
                name="human_guidance",
                handler_name="_run_stage_human_guidance",
                description="Project operator-facing decisions, exploration control, and resumable session state.",
                produced_artifacts=(
                    "human_decision_record",
                    "exploration_control_record",
                ),
            ),
        }

    def execution_profile(self, modifier: str) -> dict[str, object]:
        normalized = modifier.upper()
        profile = COMMAND_EXECUTION_PROFILES.get(normalized)
        if profile is None:
            raise ValueError(f"Unsupported command modifier for stage registry: {modifier}")
        return dict(profile)

    def stages_for_modifier(self, modifier: str) -> list[StageDefinition]:
        profile = self.execution_profile(modifier)
        return [self._stages[name] for name in profile["stage_order"]]

    def stage(self, name: str) -> StageDefinition:
        return self._stages[name]
