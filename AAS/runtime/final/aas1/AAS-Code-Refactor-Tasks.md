# AAS Code Refactor Tasks

## Stage 1 - Core Orchestration Layer

- add `src/aas1/invention_pipeline_manager.py`
- add `src/aas1/command_modifier_router.py`
- add `src/aas1/gcml_memory_interface.py`
- add `src/aas1/artifact_registry.py`
- add `src/aas1/telemetry.py`

## Stage 2 - Knowledge Infrastructure

- add `src/aas1/discovery/research_ingestion.py`
- add `src/aas1/discovery/research_synthesis.py`
- add `src/aas1/discovery/research_quality_filter.py`
- add `src/aas1/discovery/discovery_map.py`
- add `src/aas1/discovery/technology_frontier_model.py`

## Stage 3 - Invention Intelligence Modules

- add `src/aas1/reasoning/hypothesis_engine.py`
- add `src/aas1/reasoning/contradiction_engine.py`
- add `src/aas1/reasoning/solution_path_generator.py`
- add `src/aas1/reasoning/discovery_gap_detector.py`
- add `src/aas1/reasoning/cross_domain_analogy.py`
- add `src/aas1/reasoning/idea_clustering.py`

## Stage 4 - Evaluation Systems

- add `src/aas1/validation/novelty_detection.py`
- add `src/aas1/validation/feasibility_analysis.py`
- add `src/aas1/validation/experiment_simulation.py`
- add `src/aas1/validation/technology_opportunity_scanner.py`

## Stage 5 - Human Interaction Layer

- add `src/aas1/human_decision_interface.py`
- add `src/aas1/exploration_control_engine.py`

## Stage 6 - Final Integration

- wire all subsystems only through `Invention Pipeline Manager`
- add validators for the new schema-backed artifacts
- extend `docs/templates/` with templates for command requests, opportunity reports, hypothesis packets, contradiction maps, and workflow run records
- extend `docs/task_workspaces/README.md` to describe the new machine-readable artifact layout
- normalize lifecycle terminology across README, overview, prompt, and schema files
- update the state model so each task tracks command modifier, active opportunity zones, open contradictions, and selected solution paths

## Exclusions

- no core module from the redesign is excluded
- no subsystem is allowed to become a second execution controller
- AAS-RE itself is not refactored during AAS1 implementation except for minimal compatibility fixes if the target repo requires new analysis support
