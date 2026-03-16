# Synthesis Playbook

## Purpose

The AAS1 synthesis layer keeps artifacts consistent without becoming a second orchestrator. Synthesis exists to preserve durable outputs after `InventionPipelineManager` decides what to run.

## Artifact Families

### Intake
- `COMMAND_REQUEST.yaml`
- `TASK_BRIEF.md`

### Knowledge
- `RESEARCH_INGESTION_REPORT.json`
- `RESEARCH_QUALITY_REPORT.json`
- `RESEARCH_SYNTHESIS_REPORT.json`
- `DISCOVERY_MAP.json`
- `TECHNOLOGY_FRONTIER_MODEL.json`

### Reasoning and Evaluation
- `DISCOVERY_GAP_REPORT.json`
- `OPPORTUNITY_REPORT.json`
- `ANALOGY_REPORT.json`
- `HYPOTHESIS_PACKET.json`
- `IDEA_CLUSTER_REPORT.json`
- `CONTRADICTION_MAP.json`
- `SOLUTION_PATH_SET.json`
- `NOVELTY_REPORT.json`
- `FEASIBILITY_REPORT.json`
- `EXPERIMENT_SIMULATION_REPORT.json`

### Human Guidance
- `HUMAN_DECISION_RECORD.json`
- `EXPLORATION_CONTROL_RECORD.json`
- `WORKFLOW_RUN_RECORD.json`
- `WORKFLOW_SUMMARY.md`

## Rules

- preserve historical artifacts
- prefer structured JSON or YAML for machine-readable outputs
- use markdown for operator-facing summaries
- keep filenames stable across runs
