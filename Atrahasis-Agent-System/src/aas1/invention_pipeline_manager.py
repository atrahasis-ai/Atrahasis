from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from aas1.artifact_projection_layer import ArtifactProjectionLayer
from aas1.artifact_registry import ArtifactRegistry
from aas1.command_modifier_router import CommandModifierRouter
from aas1.common import CommandRequest, load_json, utc_now
from aas1.codex_team_dispatcher import CodexTeamDispatcher
from aas1.cross_industry_discovery_engine import CrossIndustryDiscoveryEngine
from aas1.decision_ranking_engine import DecisionRankingEngine
from aas1.discovery_graph_store import DiscoveryGraphStore
from aas1.discovery.discovery_map import DiscoveryMap
from aas1.discovery.research_ingestion import ResearchIngestionEngine
from aas1.discovery.research_quality_filter import ResearchQualityFilter
from aas1.discovery.research_synthesis import ResearchSynthesisEngine
from aas1.discovery.technology_frontier_model import TechnologyFrontierModel
from aas1.exploration_control_engine import ExplorationControlEngine
from aas1.gcml_memory_interface import GCMLMemoryInterface
from aas1.governance_kernel import GovernanceKernel
from aas1.human_decision_interface import HumanDecisionInterface
from aas1.knowledge_index import KnowledgeIndex
from aas1.knowledge_distillation_engine import KnowledgeDistillationEngine
from aas1.pipeline_stage_registry import PipelineStageRegistry
from aas1.platform_alignment_engine import PlatformAlignmentEngine
from aas1.provider_runtime import ProviderRuntimeRegistry
from aas1.program_state_store import ProgramStateStore
from aas1.reasoning.contradiction_engine import ContradictionEngine
from aas1.reasoning.cross_domain_analogy import CrossDomainAnalogyEngine
from aas1.reasoning.discovery_gap_detector import DiscoveryGapDetector
from aas1.reasoning.hypothesis_engine import HypothesisEngine
from aas1.reasoning.idea_clustering import IdeaClusteringEngine
from aas1.research_director_model import ResearchDirectorModel
from aas1.research_program_engine import ResearchProgramEngine
from aas1.reasoning.solution_path_generator import SolutionPathGenerator
from aas1.telemetry import Telemetry
from aas1.telemetry_aggregator import TelemetryAggregator
from aas1.task_claim_coordinator import TaskClaimCoordinator
from aas1.validation.experiment_simulation import ExperimentSimulationEngine
from aas1.validation.feasibility_analysis import FeasibilityAnalysisEngine
from aas1.validation.novelty_detection import NoveltyDetectionEngine
from aas1.validation.technology_opportunity_scanner import TechnologyOpportunityScanner
from aas1.value_alignment_engine import ValueAlignmentEngine
from aas1.workflow_context_store import WorkflowContextStore


class InventionPipelineManager:
    """Single orchestration authority for the AAS3 invention workflow."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.router = CommandModifierRouter()
        self.stage_registry = PipelineStageRegistry()
        self.knowledge_index = KnowledgeIndex(repo_root)
        self.memory = GCMLMemoryInterface(repo_root, knowledge_index=self.knowledge_index)
        self.registry = ArtifactRegistry(repo_root)
        self.projection_layer = ArtifactProjectionLayer(self.registry)
        self.telemetry = Telemetry(repo_root)
        self.telemetry_aggregator = TelemetryAggregator(repo_root)
        self.context_store = WorkflowContextStore(repo_root)
        self.governance_kernel = GovernanceKernel(repo_root)
        self.program_state_store = ProgramStateStore(repo_root)
        self.discovery_graph_store = DiscoveryGraphStore(repo_root)
        self.provider_runtime = ProviderRuntimeRegistry(repo_root)
        self.task_claims = TaskClaimCoordinator(repo_root)
        self.team_dispatcher = CodexTeamDispatcher(
            repo_root,
            artifact_registry=self.registry,
            provider_runtime=self.provider_runtime,
            context_store=self.context_store,
        )

        self.research_ingestion = ResearchIngestionEngine()
        self.research_quality = ResearchQualityFilter()
        self.research_synthesis = ResearchSynthesisEngine()
        self.discovery_map = DiscoveryMap()
        self.cross_industry = CrossIndustryDiscoveryEngine()
        self.knowledge_distillation = KnowledgeDistillationEngine()
        self.frontier_model = TechnologyFrontierModel()
        self.research_director = ResearchDirectorModel()
        self.research_programs = ResearchProgramEngine()
        self.discovery_gaps = DiscoveryGapDetector()

        self.opportunity_scanner = TechnologyOpportunityScanner()
        self.cross_domain_analogy = CrossDomainAnalogyEngine()
        self.hypothesis_engine = HypothesisEngine()
        self.idea_clustering = IdeaClusteringEngine()
        self.contradiction_engine = ContradictionEngine()
        self.solution_paths = SolutionPathGenerator()

        self.novelty_engine = NoveltyDetectionEngine()
        self.feasibility_engine = FeasibilityAnalysisEngine()
        self.value_alignment = ValueAlignmentEngine()
        self.platform_alignment = PlatformAlignmentEngine()
        self.decision_ranking = DecisionRankingEngine()
        self.experiment_simulation = ExperimentSimulationEngine()
        self.human_decision = HumanDecisionInterface()
        self.exploration_control = ExplorationControlEngine()

    def run_command(
        self,
        *,
        modifier: str,
        prompt: str,
        task_id: str,
        operator_constraints: list[str] | None = None,
    ) -> dict[str, Any]:
        request = self.router.parse(
            modifier=modifier,
            prompt=prompt,
            task_id=task_id,
            operator_constraints=operator_constraints,
        )
        return self.run(request)

    def run(self, request: CommandRequest) -> dict[str, Any]:
        request_payload = asdict(request)
        workflow_id = self._workflow_id(request)
        execution_profile = self.stage_registry.execution_profile(request.command_modifier)
        self.context_store.start_workflow(
            request=request,
            workflow_id=workflow_id,
            execution_profile=execution_profile,
        )
        self.telemetry.emit(
            "system",
            "pipeline_run_started",
            workflow_id=workflow_id,
            task_id=request.task_id,
            modifier=request.command_modifier,
            execution_profile=execution_profile["profile_id"],
        )

        task_readme = self._render_task_readme(request, workflow_id)
        task_brief = self._render_task_brief(request, workflow_id)
        self.projection_layer.project_markdown(task_id=request.task_id, relative_path="README.md", text=task_readme)
        self.projection_layer.project_markdown(task_id=request.task_id, relative_path="TASK_BRIEF.md", text=task_brief)
        self._write_artifact(
            request.task_id,
            "COMMAND_REQUEST.yaml",
            request_payload,
            schema_name="command_request",
            log_name="system",
        )

        core_memory = self.memory.load_core_memory()
        manifest = self.memory.collect_repo_manifest()
        task_workspace = self.memory.load_task_workspace(request.task_id)
        hypothesis_archive = self.memory.load_hypothesis_archive()
        cycle_count = self.memory.count_workflow_runs() + 1
        prior_program_report = self.program_state_store.load_latest(request.task_id)
        prior_discovery_map = self.discovery_graph_store.load_latest(request.task_id)

        stage_records: list[dict[str, Any]] = []
        artifact_paths: dict[str, str] = {}
        stage_artifacts: dict[str, Any] = {}
        reasoning_artifacts: dict[str, Any] = {}
        guidance_artifacts: dict[str, Any] = {}
        for stage in self.stage_registry.stages_for_modifier(request.command_modifier):
            if stage.name == "knowledge_infrastructure":
                stage_artifacts = self._run_stage_knowledge(
                    request=request,
                    workflow_id=workflow_id,
                    manifest=manifest,
                    task_workspace=task_workspace,
                    hypothesis_archive=hypothesis_archive,
                    cycle_count=cycle_count,
                    prior_program_report=prior_program_report,
                    prior_discovery_map=prior_discovery_map,
                    artifact_paths=artifact_paths,
                    stage_records=stage_records,
                )
                stage_result = stage_artifacts
            elif stage.name == "reasoning_and_evaluation":
                reasoning_artifacts = self._run_stage_reasoning_and_evaluation(
                    request=request,
                    workflow_id=workflow_id,
                    core_memory=core_memory,
                    quality_report=stage_artifacts["quality_report"],
                    synthesis_report=stage_artifacts["synthesis_report"],
                    discovery_map=stage_artifacts["discovery_map"],
                    frontier_model=stage_artifacts["frontier_model"],
                    cross_industry_report=stage_artifacts["cross_industry_report"],
                    research_program_report=stage_artifacts["research_program_report"],
                    research_director_directives=stage_artifacts["research_director_directives"],
                    cycle_count=cycle_count,
                    task_workspace=task_workspace,
                    artifact_paths=artifact_paths,
                    stage_records=stage_records,
                )
                stage_result = reasoning_artifacts
            else:
                guidance_artifacts = self._run_stage_human_guidance(
                    request=request,
                    workflow_id=workflow_id,
                    research_program_report=reasoning_artifacts["research_program_report"],
                    research_strategy_report=reasoning_artifacts["research_strategy_report"],
                    decision_ranking_report=reasoning_artifacts["decision_ranking_report"],
                    contradiction_map=reasoning_artifacts["contradiction_map"],
                    artifact_paths=artifact_paths,
                    stage_records=stage_records,
                )
                stage_result = guidance_artifacts

            latest_stage = stage_records[-1]
            self.context_store.record_stage(
                task_id=request.task_id,
                workflow_id=workflow_id,
                stage_name=latest_stage["stage"],
                status=latest_stage["status"],
                produced_artifacts=list(latest_stage["produced_artifacts"]),
                notes=latest_stage.get("notes"),
                stage_result=stage_result,
                artifact_paths=artifact_paths,
            )

        workflow_record = {
            "type": "WORKFLOW_RUN_RECORD",
            "workflow_id": workflow_id,
            "task_id": request.task_id,
            "modifier": request.command_modifier,
            "status": "PENDING_HUMAN_REVIEW",
            "started_at": request.created_at,
            "completed_at": utc_now(),
            "orchestrator": "InventionPipelineManager",
            "gcml_documents_loaded": len(core_memory["documents"]),
            "manifest_document_count": len(manifest),
            "artifacts": artifact_paths,
            "stage_records": stage_records,
            "hitl_requirements": request.hitl_requirements,
            "operator_constraints": request.operator_constraints,
            "recommended_next_actions": [
                "Respond to the surfaced human review prompt",
                "Approve, pause, terminate, or redirect the active research program",
                "Use the exploration guidance to choose the next invention branch",
            ],
        }
        artifact_paths["workflow_run_record"] = self._write_artifact(
            request.task_id,
            "WORKFLOW_RUN_RECORD.json",
            workflow_record,
            schema_name="workflow_run_record",
            log_name="system",
        )
        self.projection_layer.project_markdown(
            task_id=request.task_id,
            relative_path="WORKFLOW_SUMMARY.md",
            text=self._render_workflow_summary(workflow_record, reasoning_artifacts, guidance_artifacts),
        )
        self.context_store.complete_workflow(
            task_id=request.task_id,
            workflow_id=workflow_id,
            status=workflow_record["status"],
            workflow_record_path=artifact_paths["workflow_run_record"],
        )
        self.telemetry_aggregator.record_workflow(
            task_id=request.task_id,
            workflow_id=workflow_id,
            status=workflow_record["status"],
            stage_records=stage_records,
            artifact_paths=artifact_paths,
        )

        self.telemetry.emit(
            "system",
            "pipeline_run_completed",
            workflow_id=workflow_id,
            task_id=request.task_id,
            modifier=request.command_modifier,
            status=workflow_record["status"],
        )
        return workflow_record

    def _run_stage_knowledge(
        self,
        *,
        request: CommandRequest,
        workflow_id: str,
        manifest: list[dict[str, Any]],
        task_workspace: list[dict[str, Any]],
        hypothesis_archive: list[dict[str, Any]],
        cycle_count: int,
        prior_program_report: dict[str, Any] | None,
        prior_discovery_map: dict[str, Any] | None,
        artifact_paths: dict[str, str],
        stage_records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        ingestion_report = self.research_ingestion.run(manifest=manifest, task_workspace=task_workspace)
        artifact_paths["research_ingestion_report"] = self._write_artifact(
            request.task_id,
            "RESEARCH_INGESTION_REPORT.json",
            ingestion_report,
            schema_name="research_ingestion_report",
            log_name="system",
        )
        quality_report = self.research_quality.run(ingestion_report=ingestion_report)
        artifact_paths["research_quality_report"] = self._write_artifact(
            request.task_id,
            "RESEARCH_QUALITY_REPORT.json",
            quality_report,
            schema_name="research_quality_report",
            log_name="system",
        )
        synthesis_report = self.research_synthesis.run(quality_report=quality_report)
        artifact_paths["research_synthesis_report"] = self._write_artifact(
            request.task_id,
            "RESEARCH_SYNTHESIS_REPORT.json",
            synthesis_report,
            schema_name="research_synthesis_report",
            log_name="system",
        )
        discovery_map = self.discovery_map.run(
            synthesis_report=synthesis_report,
            quality_report=quality_report,
        )
        cross_industry_report = self.cross_industry.run(
            command_prompt=request.prompt,
            discovery_map=discovery_map,
            task_workspace=task_workspace,
        )
        self._emit_report_events(cross_industry_report)
        artifact_paths["cross_industry_discovery_report"] = self._write_artifact(
            request.task_id,
            "CROSS_INDUSTRY_DISCOVERY_REPORT.json",
            cross_industry_report,
            schema_name="cross_industry_discovery_report",
            log_name="system",
        )
        discovery_map = cross_industry_report["updated_discovery_map"]
        distillation_report = self.knowledge_distillation.run(
            discovery_map=discovery_map,
            hypothesis_archive=hypothesis_archive,
            cycle_count=cycle_count,
        )
        self._emit_report_events(distillation_report)
        artifact_paths["knowledge_distillation_report"] = self._write_artifact(
            request.task_id,
            "KNOWLEDGE_DISTILLATION_REPORT.json",
            distillation_report,
            schema_name="knowledge_distillation_report",
            log_name="system",
        )
        discovery_map = distillation_report["updated_discovery_map"]
        if prior_discovery_map is not None:
            discovery_map = self.discovery_graph_store.merge_graphs(
                prior_graph=prior_discovery_map,
                current_graph=discovery_map,
            )
        discovery_map, _graph_state_path = self.discovery_graph_store.persist(
            task_id=request.task_id,
            workflow_id=workflow_id,
            stage_name="knowledge_infrastructure",
            discovery_map=discovery_map,
        )
        artifact_paths["discovery_map"] = self._write_artifact(
            request.task_id,
            "DISCOVERY_MAP.json",
            discovery_map,
            schema_name="discovery_map",
            log_name="system",
        )
        frontier_model = self.frontier_model.run(
            synthesis_report=synthesis_report,
            discovery_map=discovery_map,
        )
        artifact_paths["technology_frontier_model"] = self._write_artifact(
            request.task_id,
            "TECHNOLOGY_FRONTIER_MODEL.json",
            frontier_model,
            schema_name="technology_frontier_model",
            log_name="system",
        )
        research_director_directives = self.research_director.plan_directives(
            frontier_model=frontier_model,
            discovery_map=discovery_map,
            telemetry_metrics=self._telemetry_metrics(
                discovery_map=discovery_map,
                hypothesis_archive=hypothesis_archive,
                research_program_report=None,
                contradiction_map=None,
            ),
        )
        research_program_report = self.research_programs.plan_programs(
            command_prompt=request.prompt,
            discovery_map=discovery_map,
            frontier_model=frontier_model,
            cross_industry_report=cross_industry_report,
            hypothesis_archive=hypothesis_archive,
            cycle_count=cycle_count,
            research_director_directives=research_director_directives,
            prior_program_report=prior_program_report,
        )
        research_program_report = self.governance_kernel.apply(
            task_id=request.task_id,
            workflow_id=workflow_id,
            program_report=research_program_report,
        )
        self._emit_report_events(research_program_report)
        self.program_state_store.persist(
            task_id=request.task_id,
            workflow_id=workflow_id,
            program_report=research_program_report,
        )
        stage_records.append(
            {
                "stage": "knowledge_infrastructure",
                "status": "COMPLETED",
                "produced_artifacts": [
                    "research_ingestion_report",
                    "research_quality_report",
                    "research_synthesis_report",
                    "discovery_map",
                    "cross_industry_discovery_report",
                    "knowledge_distillation_report",
                    "technology_frontier_model",
                ],
                "notes": [
                    "Knowledge retrieval is routed through the AAS3 knowledge index.",
                    "Discovery graph and planned program state were persisted to runtime state stores.",
                ],
            }
        )
        self.telemetry.emit(
            "system",
            "pipeline_stage_completed",
            task_id=request.task_id,
            stage="knowledge_infrastructure",
        )
        return {
            "quality_report": quality_report,
            "synthesis_report": synthesis_report,
            "discovery_map": discovery_map,
            "cross_industry_report": cross_industry_report,
            "research_director_directives": research_director_directives,
            "research_program_report": research_program_report,
            "frontier_model": frontier_model,
        }

    def _run_stage_reasoning_and_evaluation(
        self,
        *,
        request: CommandRequest,
        workflow_id: str,
        core_memory: dict[str, Any],
        quality_report: dict[str, Any],
        synthesis_report: dict[str, Any],
        discovery_map: dict[str, Any],
        frontier_model: dict[str, Any],
        cross_industry_report: dict[str, Any],
        research_program_report: dict[str, Any],
        research_director_directives: dict[str, Any],
        cycle_count: int,
        task_workspace: list[dict[str, Any]],
        artifact_paths: dict[str, str],
        stage_records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        gap_report = self.discovery_gaps.run(quality_report=quality_report)
        artifact_paths["discovery_gap_report"] = self._write_artifact(
            request.task_id,
            "DISCOVERY_GAP_REPORT.json",
            gap_report,
            schema_name="discovery_gap_report",
            log_name="system",
        )
        opportunity_report = self.opportunity_scanner.run(
            discovery_map=discovery_map,
            frontier_model=frontier_model,
        )
        artifact_paths["opportunity_report"] = self._write_artifact(
            request.task_id,
            "OPPORTUNITY_REPORT.json",
            opportunity_report,
            schema_name="opportunity_report",
            log_name="system",
        )
        analogy_report = self.cross_domain_analogy.run(opportunity_report=opportunity_report)
        artifact_paths["analogy_report"] = self._write_artifact(
            request.task_id,
            "ANALOGY_REPORT.json",
            analogy_report,
            schema_name="analogy_report",
            log_name="system",
        )
        hypothesis_packet = self.hypothesis_engine.run(
            command_prompt=request.prompt,
            opportunity_report=opportunity_report,
            analogy_report=analogy_report,
            cross_industry_report=cross_industry_report,
            synthesis_report=synthesis_report,
            discovery_map=discovery_map,
            task_workspace=task_workspace,
        )
        cluster_report = self.idea_clustering.run(hypothesis_packet=hypothesis_packet)
        artifact_paths["idea_cluster_report"] = self._write_artifact(
            request.task_id,
            "IDEA_CLUSTER_REPORT.json",
            cluster_report,
            schema_name="idea_cluster_report",
            log_name="system",
        )
        contradiction_map = self.contradiction_engine.run(
            hypothesis_packet=hypothesis_packet,
            gap_report=gap_report,
        )
        artifact_paths["contradiction_map"] = self._write_artifact(
            request.task_id,
            "CONTRADICTION_MAP.json",
            contradiction_map,
            schema_name="contradiction_map",
            log_name="system",
        )
        solution_paths = self.solution_paths.run(
            hypothesis_packet=hypothesis_packet,
            contradiction_map=contradiction_map,
            cluster_report=cluster_report,
        )
        artifact_paths["solution_path_set"] = self._write_artifact(
            request.task_id,
            "SOLUTION_PATH_SET.json",
            solution_paths,
            schema_name="solution_path_set",
            log_name="system",
        )
        novelty_report = self.novelty_engine.run(
            hypothesis_packet=hypothesis_packet,
            quality_report=quality_report,
        )
        artifact_paths["novelty_report"] = self._write_artifact(
            request.task_id,
            "NOVELTY_REPORT.json",
            novelty_report,
            schema_name="novelty_report",
            log_name="system",
        )
        feasibility_report = self.feasibility_engine.run(
            solution_paths=solution_paths,
            gap_report=gap_report,
            hypothesis_packet=hypothesis_packet,
        )
        artifact_paths["feasibility_report"] = self._write_artifact(
            request.task_id,
            "FEASIBILITY_REPORT.json",
            feasibility_report,
            schema_name="feasibility_report",
            log_name="system",
        )
        value_alignment_report = self.value_alignment.run(
            hypothesis_packet=hypothesis_packet,
            research_program_report=research_program_report,
            operator_constraints=request.operator_constraints,
            hitl_requirements=request.hitl_requirements,
            architecture_model=core_memory,
        )
        artifact_paths["value_alignment_report"] = self._write_artifact(
            request.task_id,
            "VALUE_ALIGNMENT_REPORT.json",
            value_alignment_report,
            schema_name="value_alignment_report",
            log_name="system",
        )
        platform_alignment_report = self.platform_alignment.run(
            hypothesis_packet=hypothesis_packet,
            research_program_report=research_program_report,
            value_alignment_report=value_alignment_report,
            architecture_model=core_memory,
        )
        self._emit_report_events(platform_alignment_report)
        artifact_paths["platform_alignment_report"] = self._write_artifact(
            request.task_id,
            "PLATFORM_ALIGNMENT_REPORT.json",
            platform_alignment_report,
            schema_name="platform_alignment_report",
            log_name="system",
        )
        hypothesis_packet = self.hypothesis_engine.link_artifacts(
            hypothesis_packet=hypothesis_packet,
            contradiction_map=contradiction_map,
            solution_paths=solution_paths,
            novelty_report=novelty_report,
            feasibility_report=feasibility_report,
        )
        artifact_paths["hypothesis_packet"] = self._write_artifact(
            request.task_id,
            "HYPOTHESIS_PACKET.json",
            hypothesis_packet,
            schema_name="hypothesis_packet",
            log_name="system",
        )
        discovery_map = self.discovery_map.link_invention_graph(
            discovery_map=discovery_map,
            hypothesis_packet=hypothesis_packet,
            contradiction_map=contradiction_map,
            solution_paths=solution_paths,
        )
        decision_ranking_report = self.decision_ranking.run(
            hypothesis_packet=hypothesis_packet,
            contradiction_map=contradiction_map,
            novelty_report=novelty_report,
            feasibility_report=feasibility_report,
            frontier_model=frontier_model,
            quality_report=quality_report,
            analogy_report=analogy_report,
            gap_report=gap_report,
            opportunity_report=opportunity_report,
            solution_paths=solution_paths,
            platform_alignment_report=platform_alignment_report,
        )
        artifact_paths["decision_ranking_report"] = self._write_artifact(
            request.task_id,
            "DECISION_RANKING_REPORT.json",
            decision_ranking_report,
            schema_name="decision_ranking_report",
            log_name="system",
        )
        research_program_report = self.research_programs.update_programs(
            program_report=research_program_report,
            hypothesis_packet=hypothesis_packet,
            contradiction_map=contradiction_map,
            solution_paths=solution_paths,
            decision_ranking_report=decision_ranking_report,
            frontier_model=frontier_model,
            cycle_count=cycle_count,
        )
        research_program_report = self.governance_kernel.apply(
            task_id=request.task_id,
            workflow_id=workflow_id,
            program_report=research_program_report,
        )
        self._emit_report_events(research_program_report)
        hypothesis_packet = self.research_programs.annotate_hypotheses(
            hypothesis_packet=hypothesis_packet,
            program_report=research_program_report,
        )
        artifact_paths["hypothesis_packet"] = self._write_artifact(
            request.task_id,
            "HYPOTHESIS_PACKET.json",
            hypothesis_packet,
            schema_name="hypothesis_packet",
            log_name="system",
        )
        discovery_map = research_program_report["updated_discovery_map"]
        discovery_map, _graph_state_path = self.discovery_graph_store.persist(
            task_id=request.task_id,
            workflow_id=workflow_id,
            stage_name="reasoning_and_evaluation",
            discovery_map=discovery_map,
        )
        research_program_report["updated_discovery_map"] = discovery_map
        self.program_state_store.persist(
            task_id=request.task_id,
            workflow_id=workflow_id,
            program_report=research_program_report,
        )
        artifact_paths["research_program_report"] = self._write_artifact(
            request.task_id,
            "RESEARCH_PROGRAM_REPORT.json",
            research_program_report,
            schema_name="research_program_report",
            log_name="system",
        )
        artifact_paths["discovery_map"] = self._write_artifact(
            request.task_id,
            "DISCOVERY_MAP.json",
            discovery_map,
            schema_name="discovery_map",
            log_name="system",
        )
        experiment_report = self.experiment_simulation.run(
            solution_paths=solution_paths,
            feasibility_report=feasibility_report,
        )
        artifact_paths["experiment_simulation_report"] = self._write_artifact(
            request.task_id,
            "EXPERIMENT_SIMULATION_REPORT.json",
            experiment_report,
            schema_name="experiment_simulation_report",
            log_name="system",
        )
        research_strategy_report = self.research_director.run(
            research_program_report=research_program_report,
            frontier_model=frontier_model,
            discovery_map=discovery_map,
            telemetry_metrics=self._telemetry_metrics(
                discovery_map=discovery_map,
                hypothesis_archive=[],
                research_program_report=research_program_report,
                contradiction_map=contradiction_map,
            ),
            value_alignment_signal=value_alignment_report,
        )
        self._emit_report_events(research_strategy_report)
        artifact_paths["research_strategy_report"] = self._write_artifact(
            request.task_id,
            "RESEARCH_STRATEGY_REPORT.json",
            research_strategy_report,
            schema_name="research_strategy_report",
            log_name="system",
        )
        stage_records.append(
            {
                "stage": "reasoning_and_evaluation",
                "status": "COMPLETED",
                "produced_artifacts": [
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
                ],
                "notes": [
                    "Cross-industry discovery and research-program planning run before hypothesis generation to keep exploration structured.",
                    "Research director strategy now allocates branch budget after governed program updates.",
                    "The governance kernel and durable graph/program stores are active in this stage.",
                ],
            }
        )
        self.telemetry.emit(
            "system",
            "pipeline_stage_completed",
            task_id=request.task_id,
            stage="reasoning_and_evaluation",
        )
        return {
            "opportunity_report": opportunity_report,
            "hypothesis_packet": hypothesis_packet,
            "contradiction_map": contradiction_map,
            "solution_paths": solution_paths,
            "novelty_report": novelty_report,
            "feasibility_report": feasibility_report,
            "value_alignment_report": value_alignment_report,
            "platform_alignment_report": platform_alignment_report,
            "decision_ranking_report": decision_ranking_report,
            "research_program_report": research_program_report,
            "research_strategy_report": research_strategy_report,
            "experiment_report": experiment_report,
        }

    def _run_stage_human_guidance(
        self,
        *,
        request: CommandRequest,
        workflow_id: str,
        research_program_report: dict[str, Any],
        research_strategy_report: dict[str, Any],
        decision_ranking_report: dict[str, Any],
        contradiction_map: dict[str, Any],
        artifact_paths: dict[str, str],
        stage_records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        request_payload = asdict(request)
        human_record = self.human_decision.run(
            command_request=request_payload,
            research_program_report=research_program_report,
            research_strategy_report=research_strategy_report,
            decision_ranking_report=decision_ranking_report,
            contradiction_map=contradiction_map,
        )
        artifact_paths["human_decision_record"] = self._write_artifact(
            request.task_id,
            "HUMAN_DECISION_RECORD.json",
            human_record,
            schema_name="human_decision_record",
            log_name="system",
        )
        exploration_record = self.exploration_control.run(
            research_program_report=research_program_report,
            research_strategy_report=research_strategy_report,
            decision_ranking_report=decision_ranking_report,
            contradiction_map=contradiction_map,
        )
        artifact_paths["exploration_control_record"] = self._write_artifact(
            request.task_id,
            "EXPLORATION_CONTROL_RECORD.json",
            exploration_record,
            schema_name="exploration_control_record",
            log_name="system",
        )
        dispatch_recommendations = self.team_dispatcher.build_recommendations(
            task_id=request.task_id,
            workflow_id=workflow_id,
            request_payload=request_payload,
            human_record=human_record,
            exploration_record=exploration_record,
        )
        human_record["dispatch_recommendations"] = self.team_dispatcher.dispatch_recommendation_summary(
            dispatch_recommendations
        )
        artifact_paths["human_decision_record"] = self._write_artifact(
            request.task_id,
            "HUMAN_DECISION_RECORD.json",
            human_record,
            schema_name="human_decision_record",
            log_name="system",
        )
        artifact_paths["team_dispatch_recommendations"] = self._write_artifact(
            request.task_id,
            "TEAM_DISPATCH_RECOMMENDATIONS.json",
            dispatch_recommendations,
            schema_name="team_dispatch_recommendations",
            log_name="system",
        )
        rendered_prompt = self.human_decision.render_prompt_from_records(
            human_record=human_record,
            exploration_record=exploration_record,
        )
        stage_records.append(
            {
                "stage": "human_guidance",
                "status": "PENDING_HUMAN_REVIEW",
                "produced_artifacts": [
                    "human_decision_record",
                    "exploration_control_record",
                    "team_dispatch_recommendations",
                ],
                "notes": [
                    "Human-review state is derived from task-local artifacts rather than a separate operator runtime surface.",
                    "Spawn-program actions now carry explicit Codex team recommendations.",
                ],
            }
        )
        self.telemetry.emit(
            "system",
            "pipeline_stage_completed",
            task_id=request.task_id,
            stage="human_guidance",
        )
        return {
            "human_decision_record": human_record,
            "exploration_control_record": exploration_record,
            "rendered_prompt": rendered_prompt,
        }

    def _telemetry_metrics(
        self,
        *,
        discovery_map: dict[str, Any],
        hypothesis_archive: list[dict[str, Any]],
        research_program_report: dict[str, Any] | None,
        contradiction_map: dict[str, Any] | None,
    ) -> dict[str, Any]:
        return {
            "discovery_node_count": len(discovery_map.get("nodes", discovery_map.get("entities", []))),
            "hypothesis_archive_count": len(hypothesis_archive),
            "active_program_count": len(research_program_report.get("active_programs", [])) if research_program_report else 0,
            "contradiction_count": len(contradiction_map.get("contradictions", [])) if contradiction_map else 0,
        }

    def _emit_report_events(self, report: dict[str, Any]) -> None:
        for item in report.get("telemetry_events", []):
            payload = dict(item)
            event = payload.pop("event", None)
            if event is None:
                continue
            self.telemetry.emit("system", event, **payload)

    def _write_artifact(
        self,
        task_id: str,
        relative_path: str,
        payload: dict[str, Any],
        *,
        schema_name: str,
        log_name: str,
    ) -> str:
        if relative_path.endswith(".json"):
            path = self.projection_layer.project_json(
                task_id=task_id,
                relative_path=relative_path,
                payload=payload,
                schema_name=schema_name,
            )
        else:
            path = self.projection_layer.project_yaml(
                task_id=task_id,
                relative_path=relative_path,
                payload=payload,
                schema_name=schema_name,
            )
        self.telemetry.emit(
            log_name,
            "artifact_written",
            task_id=task_id,
            artifact=str(path.relative_to(self.repo_root)).replace("\\", "/"),
            schema=schema_name,
        )
        return str(path.relative_to(self.repo_root)).replace("\\", "/")

    def _workflow_id(self, request: CommandRequest) -> str:
        return f"{request.task_id}-{request.command_modifier}-{request.created_at.replace(':', '').replace('-', '')}"

    def _render_task_readme(self, request: CommandRequest, workflow_id: str) -> str:
        constraints = "\n".join(f"- {item}" for item in request.operator_constraints) or "- none"
        return f"""# {request.task_id} AAS3 Workspace

- Workflow ID: `{workflow_id}`
- Command Modifier: `{request.command_modifier}`
- Orchestrator: `InventionPipelineManager`
- Status: `PENDING_HUMAN_REVIEW`

## Prompt

{request.prompt}

## Operator Constraints

{constraints}
"""

    def _render_task_brief(self, request: CommandRequest, workflow_id: str) -> str:
        hitl = "\n".join(f"- {item}" for item in request.hitl_requirements) or "- none"
        return f"""# Task Brief

- Task ID: `{request.task_id}`
- Workflow ID: `{workflow_id}`
- Modifier: `{request.command_modifier}`
- Scope: `{request.scope}`
- Runtime Shape: `AAS3`

## Prompt

{request.prompt}

## Human Review Gates

{hitl}
"""

    def _render_workflow_summary(
        self,
        workflow_record: dict[str, Any],
        reasoning_artifacts: dict[str, Any],
        guidance_artifacts: dict[str, Any],
    ) -> str:
        programs = "\n".join(
            (
                f"- {program['program_id']}: {program['program_title']} "
                f"(score {program['opportunity_score']}, hypotheses {', '.join(program['hypothesis_list'][:3]) or 'none'})"
            )
            for program in reasoning_artifacts["research_program_report"]["active_programs"][:3]
        ) or "- none"
        options = "\n".join(
            (
                f"- {item['label']}: {item.get('program_id', item.get('path_id', 'unknown'))}"
            )
            for item in guidance_artifacts["human_decision_record"]["options"]
        ) or "- none"
        strategy_summary = guidance_artifacts["human_decision_record"].get("research_strategy_summary", "none")
        return f"""# Workflow Summary

- Workflow ID: `{workflow_record['workflow_id']}`
- Status: `{workflow_record['status']}`
- Orchestrator: `{workflow_record['orchestrator']}`

## Active Research Programs

{programs}

## Research Strategy

{strategy_summary}

## Operator Options

{options}
"""

    def render_operator_prompt(self, *, task_id: str) -> str:
        task_workspace = self.repo_root / "docs" / "task_workspaces" / task_id
        return self.human_decision.render_prompt_for_task(
            task_workspace=task_workspace,
        )

    def register_backend(
        self,
        *,
        provider: str,
        agent_name: str,
        session_id: str,
        agent_types: list[str] | None = None,
        current_task: str | None = None,
        status: str = "ACTIVE",
        notes: str = "",
    ) -> dict[str, Any]:
        return self.provider_runtime.register_backend(
            provider=provider,
            agent_name=agent_name,
            session_id=session_id,
            agent_types=agent_types,
            current_task=current_task,
            status=status,
            notes=notes,
        )

    def prepare_team_dispatch(
        self,
        *,
        task_id: str,
        action_label: str,
        instruction: str,
        provider: str = "codex",
        agent_name: str | None = None,
        session_id: str | None = None,
        execute: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        context = self.team_dispatcher.load_dispatch_context(task_id=task_id)
        human_record = context["human_record"]
        recommendations = context["recommendations"]
        workflow_id = context["workflow_id"]
        if recommendations is None:
            request = (
                context["latest_workflow"] or {}
            ).get("request", {})
            exploration_record = load_json(
                self.repo_root / "docs" / "task_workspaces" / task_id / "EXPLORATION_CONTROL_RECORD.json"
            )
            recommendations = self.team_dispatcher.build_recommendations(
                task_id=task_id,
                workflow_id=workflow_id,
                request_payload=request,
                human_record=human_record,
                exploration_record=exploration_record,
            )
        team_plan = self.team_dispatcher.prepare_dispatch(
            task_id=task_id,
            workflow_id=workflow_id,
            human_record=human_record,
            recommendations=recommendations,
            action_label=action_label,
            instruction=instruction,
            parent_provider=provider,
            parent_agent_name=agent_name,
            parent_session_id=session_id,
            dry_run=dry_run,
        )
        if execute:
            return self.team_dispatcher.execute_dispatch(team_plan=team_plan, dry_run=dry_run)
        return {"team_plan": team_plan}
