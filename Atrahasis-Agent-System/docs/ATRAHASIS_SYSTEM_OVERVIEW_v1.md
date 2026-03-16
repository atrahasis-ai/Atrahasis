# Atrahasis Agent System Overview
## Version 2.0

## Purpose

AAS1 is a human-guided invention intelligence system for the Atrahasis repository. It maps the repository as a living research corpus, identifies invention opportunities, generates candidate invention paths, and packages the results for human direction.

## Single Orchestration Rule

`InventionPipelineManager` is the only execution controller.

It is responsible for:

- command routing activation
- subsystem execution order
- artifact persistence
- telemetry emission
- operator pause points

The following modules are explicitly not controllers:

- `HypothesisEngine`
- `ExplorationControlEngine`
- `CommandModifierRouter`
- `TechnologyOpportunityScanner`
- `DiscoveryMap`

## Runtime Flow

1. Normalize the operator request.
2. Load GCML memory and repository evidence.
3. Run knowledge infrastructure modules.
4. Evaluate discovery gaps and opportunity zones.
5. Generate hypotheses, contradictions, and solution paths.
6. Run novelty, feasibility, and simulation analysis.
7. Produce human decision and exploration guidance packets.
8. Stop for operator review.

## Module Stack

### Orchestration
- `InventionPipelineManager`
- `CommandModifierRouter`
- `GCMLMemoryInterface`
- `ArtifactRegistry`
- `Telemetry`

### Knowledge Infrastructure
- `ResearchIngestionEngine`
- `ResearchQualityFilter`
- `ResearchSynthesisEngine`
- `DiscoveryMap`
- `TechnologyFrontierModel`

### Invention Intelligence
- `DiscoveryGapDetector`
- `CrossDomainAnalogyEngine`
- `HypothesisEngine`
- `IdeaClusteringEngine`
- `ContradictionEngine`
- `SolutionPathGenerator`

### Evaluation
- `TechnologyOpportunityScanner`
- `NoveltyDetectionEngine`
- `FeasibilityAnalysisEngine`
- `ExperimentSimulationEngine`

### Human Guidance
- `HumanDecisionInterface`
- `ExplorationControlEngine`

## Canonical Data Surfaces

- `docs/AGENT_STATE.md`
- `docs/SESSION_BRIEF.md`
- `docs/INVENTION_DASHBOARD.md`
- `docs/DECISIONS.md`
- `docs/PATTERN_REGISTER.md`
- `docs/task_workspaces/<TASK_ID>/`
- `docs/prior_art/`
- `docs/specifications/`

Historical artifacts remain inputs to future runs. The old multi-controller operating model does not.
