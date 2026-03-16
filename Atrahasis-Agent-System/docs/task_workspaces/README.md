# Task Workspaces

Task workspaces are the canonical task-local execution and audit surface for AAS4 runs.

Path pattern:

- `docs/task_workspaces/<TASK_ID>/`

## Baseline Files For Every Real Task

- `README.md`
- `TASK_BRIEF.md`
- `TASK_START_CHECKLIST.json`

## Direct Spec Minimum Additions

- `DIRECT_SPEC_AUDIT_RECORD.json`
- `DIRECT_SPEC_VERIFICATION_REPORT.json`
- `CLOSEOUT_CONSISTENCY_REPORT.json`

Reference templates:
- `docs/templates/AUTHORITY_COVERAGE_MATRIX_TEMPLATE.json`
- `docs/templates/TASK_START_CHECKLIST_TEMPLATE.json`
- `docs/templates/DIRECT_SPEC_AUDIT_RECORD_TEMPLATE.json`
- `docs/templates/DIRECT_SPEC_VERIFICATION_REPORT_TEMPLATE.json`
- `docs/templates/CLOSEOUT_CONSISTENCY_REPORT_TEMPLATE.json`
- `docs/templates/FUTURE_BRANCH_REPORT_TEMPLATE.json`
- `docs/templates/SWARM_EXECUTION_RECORD_TEMPLATE.json`

Exploratory idea prep:
- `python scripts/prepare_aas4_idea_task.py --title "<IDEA TITLE>" --prompt-file <prompt.txt>`
- Use this for noncanonical `AASNI` or architecture-heavy exploratory `FULL PIPELINE` ideation so the run receives a real `T-900x` workspace anchor.

## Full Pipeline Artifact Families

`FULL PIPELINE` work still uses the richer AAS artifact set such as:

- `AUTHORITY_COVERAGE_MATRIX.json`
- `TEAM_PLAN.yaml`
- `FUTURE_BRANCH_REPORT.json`
- `SWARM_EXECUTION_RECORD.json`
- `CHILD_RESULT_MERGE_PACKAGE.json`
- `children/<lane>__<role>__<branch_kind>.json`
- `COMMAND_REQUEST.yaml`
- `DISCOVERY_MAP.json`
- `TECHNOLOGY_FRONTIER_MODEL.json`
- `OPPORTUNITY_REPORT.json`
- `HYPOTHESIS_PACKET.json`
- `CONTRADICTION_MAP.json`
- `SOLUTION_PATH_SET.json`
- `NOVELTY_REPORT.json`
- `FEASIBILITY_REPORT.json`
- `EXPERIMENT_SIMULATION_REPORT.json`
- `HUMAN_DECISION_RECORD.json`
- `EXPLORATION_CONTROL_RECORD.json`
- `WORKFLOW_RUN_RECORD.json`
- `WORKFLOW_SUMMARY.md`

## Rules

- `T-xxx` remains the task anchor even if invention candidates branch later
- exploratory `AASNI` ideation still needs a real `T-900x` workspace and may not remain session-only
- a noncanonical `T-900x` workspace is task-local audit state, not forbidden shared-state progression
- historical files remain valid inputs to new runs
- subsystem outputs must be mediated by the orchestration layer
- no subsystem may write operator-facing control decisions outside the pipeline manager
- a task may not be marked `DONE` until its closeout semantics are machine-checkable for its task class
- a real-swarm ideation result is not valid unless the task workspace contains actual swarm execution evidence rather than a solo role-play summary
- a real-swarm ideation result is also incomplete unless the child-result artifacts exist on disk and the swarm record points to them
- child-result artifacts should record session identity, model auditability, and whether the artifact was written directly by the child session or by a parent proxy

## Optional Controller Files

- `REVIEW_GATE_RECORD.json`
  First-class controller-owned review status, findings, and verdicts.
- `CONTROLLER_RUN_RESULT.json`
  Controller-owned run snapshot for retained runtime metadata and sync posture.
- `CLOSEOUT_EXECUTION_RECORD.json`
  Controller-owned closeout execution record covering review finalization, human decision capture, claim/handoff updates, and validator results.
- `CLOSEOUT_CONSISTENCY_REPORT.json`
  Machine-checked report that claim state, task workspace, handoff state, and dispatch order agree before `DONE`.
