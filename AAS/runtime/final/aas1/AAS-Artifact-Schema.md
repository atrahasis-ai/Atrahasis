# AAS Artifact Schema

## Schema Strategy

AAS1 keeps the current human-readable canon and adds machine-readable invention-intelligence artifacts beside it. Existing files are preserved; new schema-backed artifacts are introduced under task workspaces and invention directories.

## Orchestration Rule

All schema-backed artifacts are produced or persisted by the `Invention Pipeline Manager`.

- subsystem modules return structured results
- the orchestration layer decides when those results become canonical artifacts
- no subsystem writes directly into another subsystem's artifact space

## Core Existing Artifacts Retained

- `docs/AGENT_STATE.md`
- `docs/SESSION_BRIEF.md`
- `docs/INVENTION_DASHBOARD.md`
- `docs/DECISIONS.md`
- `docs/PATTERN_REGISTER.md`
- `docs/TRIBUNAL_LOG.md`
- `docs/task_workspaces/<TASK_ID>/`
- `docs/prior_art/<INVENTION_ID>/`
- `docs/specifications/<INVENTION_ID>/`
- `docs/contribution_requests/<INVENTION_ID>.yaml`

## New Machine-Readable Artifacts

### COMMAND_REQUEST

- path: `docs/task_workspaces/<TASK_ID>/intake/command_request.yaml`
- producer: `Invention Pipeline Manager` via Command Modifier Router

### DISCOVERY_MAP

- path: `docs/task_workspaces/<TASK_ID>/discovery/discovery_map.json`
- producer: `Invention Pipeline Manager` using Discovery Map subsystem outputs

### TECHNOLOGY_FRONTIER_MODEL

- path: `docs/task_workspaces/<TASK_ID>/discovery/technology_frontier_model.json`
- producer: `Invention Pipeline Manager`

### OPPORTUNITY_REPORT

- path: `docs/task_workspaces/<TASK_ID>/discovery/opportunity_report.json`
- producer: `Invention Pipeline Manager` using Technology Opportunity Scanner outputs

### HYPOTHESIS_PACKET

- path: `docs/task_workspaces/<TASK_ID>/reasoning/hypothesis_packet.json`
- producer: `Invention Pipeline Manager`

### CONTRADICTION_MAP

- path: `docs/task_workspaces/<TASK_ID>/reasoning/contradiction_map.json`
- producer: `Invention Pipeline Manager`

### SOLUTION_PATH_SET

- path: `docs/task_workspaces/<TASK_ID>/reasoning/solution_paths.json`
- producer: `Invention Pipeline Manager`

### NOVELTY_REPORT

- path: `docs/task_workspaces/<TASK_ID>/validation/novelty_report.json`
- producer: `Invention Pipeline Manager`

### FEASIBILITY_REPORT

- path: `docs/task_workspaces/<TASK_ID>/validation/feasibility_report.json`
- producer: `Invention Pipeline Manager`

### EXPERIMENT_SIMULATION_REPORT

- path: `docs/task_workspaces/<TASK_ID>/validation/experiment_simulation_report.json`
- producer: `Invention Pipeline Manager`

### HUMAN_DECISION_RECORD

- path: `docs/task_workspaces/<TASK_ID>/governance/human_decision_record.yaml`
- producer: `Invention Pipeline Manager` after operator interaction

### WORKFLOW_RUN_RECORD

- path: `docs/task_workspaces/<TASK_ID>/runs/<RUN_ID>.json`
- producer: `Invention Pipeline Manager`

## Invention Folder Additions

When a concept becomes a `C-xxx` invention, add:

- `docs/invention_logs/<INVENTION_ID>_DISCOVERY_SUMMARY.md`
- `docs/prior_art/<INVENTION_ID>/opportunity_report.json`
- `docs/specifications/<INVENTION_ID>/solution_path_trace.json`

## Schema Files to Add

- `docs/schemas/command_request.schema.json`
- `docs/schemas/discovery_map.schema.json`
- `docs/schemas/opportunity_report.schema.json`
- `docs/schemas/hypothesis_packet.schema.json`
- `docs/schemas/contradiction_map.schema.json`
- `docs/schemas/solution_path_set.schema.json`
- `docs/schemas/workflow_run_record.schema.json`

## Design Rule

No current artifact is deleted by this redesign. AAS1 extends the repository with structured invention-intelligence artifacts instead of replacing the existing human-readable canon.
