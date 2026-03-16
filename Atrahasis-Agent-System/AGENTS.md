# Atrahasis Repo Instructions

## Required Repo Skills

Use these repo-local skills when their trigger conditions are met:

- `aas5-bootstrap`
  Path: `.agents/skills/aas5-bootstrap/SKILL.md`
  Use for session initialization and reinitialization.

- `aas5-task-routing`
  Path: `.agents/skills/aas5-task-routing/SKILL.md`
  Use before any substantive post-bootstrap task answer, task start, ideation, analysis, or edit.

- `aas5-task-start`
  Path: `.agents/skills/aas5-task-start/SKILL.md`
  Use for canonical `Start T-xxx` or `AASBT` task dispatch.

- `aas5-ideation`
  Path: `.agents/skills/aas5-ideation/SKILL.md`
  Use for `FULL PIPELINE / IDEATION`, especially exploratory subsystem or authority-boundary work.

## Trigger Rules

- After bootstrap, every substantive operator prompt must route through `aas5-task-routing` first.
- Do not answer a substantive post-bootstrap prompt directly from the parent session without task classification.
- If the operator prompt begins with `Full Pipeline Task:` or `FULL PIPELINE TASK:`, treat that prefix as a hard operator modifier.

## `Full Pipeline Task:` Meaning

This prefix is a strict instruction, not a stylistic label.

When it appears:

- do not make a judgment call to stay lightweight
- do not downgrade into parent-only advisory analysis
- do not present options or a recommendation unless the required AAS5 path actually ran
- route the prompt through `aas5-task-routing` immediately

If the prompt is exploratory or noncanonical:

- treat it as strict exploratory `FULL PIPELINE / IDEATION`
- create the noncanonical `T-900x` workspace
- run the real `Alpha/Beta/Gamma/Radical` swarm
- require `TEAM_PLAN.yaml`, `FUTURE_BRANCH_REPORT.json`, `SWARM_EXECUTION_RECORD.json`, `CHILD_RESULT_MERGE_PACKAGE.json`, and per-child artifacts under `children/`
- if that path is not being executed, stop and report noncompliance instead of answering informally

If the prompt is a canonical backlog task with an explicit task id:

- route it as a strict `FULL PIPELINE` task start
- use the canonical task workspace path, not a session-only analysis

## Guardrails

- `do not add it to TODO`, `do not claim a canonical task`, or `do not edit shared state yet` do not prohibit the noncanonical `T-900x` workspace for exploratory ideation
- if `validate_swarm_execution_record.py` has not passed, recommendation is not authorized
- if the required workspace or swarm artifacts do not exist, stop and report noncompliance
- never label parent-only analysis as swarm output
