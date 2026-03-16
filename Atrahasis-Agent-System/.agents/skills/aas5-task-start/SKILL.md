---
name: aas5-task-start
description: Prepare and harden the start of a real AAS5 task. Use when the operator says `Start T-xxx`, `AASBT T-xxx`, `begin T-xxx`, or otherwise dispatches a canonical backlog task for real execution.
---

# AAS5 Task Start

## Overview

Use this skill to turn a direct task-start command into a machine-checked start contract instead of freehand execution.

## Workflow

1. Read the current claim files and the relevant `TODO.md` row.
2. Route the task class correctly before editing.
3. Run:
   - `python scripts/prepare_aas5_task.py T-<ID>`
4. Read the generated:
   - `docs/task_workspaces/T-<ID>/TASK_START_CHECKLIST.json`
   - `docs/task_workspaces/T-<ID>/TASK_BRIEF.md`
5. Follow the checklist's write surface, validators, and stop rules.
6. If the task class is `DIRECT SPEC`:
   - maintain `DIRECT_SPEC_AUDIT_RECORD.json`
   - run `python scripts/verify_direct_spec_task.py T-<ID>` before claiming the scope is clean
   - run `python scripts/validate_task_closeout_consistency.py T-<ID>` before marking the task `DONE`

## Guardrails

- Do not treat `Start T-xxx` as permission to improvise around claims, dependencies, or shared-state protocol.
- Do not stop at a narrative progress checkpoint for `DIRECT SPEC` work unless you are actually blocked, HITL-gated, or ready for assessment/closeout.
- If you change parser-consumed shared-doc structure, update the consuming parser/tests in the same task.
