# Task Brief

- Task ID: `T-270`
- Title: `LLM Generation and Constrained Decoding for AASL-T`
- Modifier: `AASBT`
- Scope: `FULL PIPELINE rerun against existing approved concept C44`
- Runtime shape: `AAS4 manual rerun`

## Prompt

Design the system for LLM generation of well-formed `AASL-T`, including:
- few-shot prompt packs,
- EBNF/PEG-style constrained decoding,
- dataset requirements for tuning/alignment,
- and a benchmark suite covering structural validity, semantic correctness, and
  deployment gates.

## Governing Inputs

- `docs/task_workspaces/T-270/HITL_APPROVAL.md`
- `docs/task_workspaces/T-212/TYPE_EXTENSION_SPEC.md`
- `docs/specifications/C38/MASTER_TECH_SPEC.md`
- `../AACP-AASL/AACP_AASL_Full_Replace_AAS_Tasks.md`
- `../AACP-AASL/AACP_AASL_Full_Replacement_Strategy.md`

## Deliverable

- `docs/specifications/C44/MASTER_TECH_SPEC.md`

## Human Review Gates

- Existing concept approval already recorded for `C44`
- Parallel closeout required before shared-state updates are reconciled
