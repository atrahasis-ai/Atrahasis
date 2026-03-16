---
name: aas5-specification
description: Build or edit canonical AAS5 specification artifacts. Use when Codex needs to write or update master specs, task workspace artifacts, design deliverables, or schema-constrained machine artifacts on the repo’s canonical write surfaces.
---

# AAS5 Specification

## Overview

Use this skill to produce canonical specification outputs without drifting into noncanonical folders or ad hoc formats.

## Workflow

1. Read the target artifact fully before editing it.
2. Confirm the task class:
   - `DIRECT SPEC` modifies existing canonical specs
   - `FULL PIPELINE` writes the next approved stage artifact
3. Write only to canonical destinations such as:
   - the resolved canonical master tech spec path for `<ID>` under `docs/specifications/`
   - `docs/task_workspaces/T-<ID>/`
   - `docs/contribution_requests/<ID>.yaml`
4. Preserve the established section structure unless the task explicitly requires restructuring.
5. When the output is machine-consumed, use:
   - `python scripts/run_aas5_schema_exec.py --schema <schema> --output <artifact> --prompt-file <prompt>`
6. Run the relevant validators after the edit.

## Output Rules

- Preserve IDs, filenames, and terminology exactly.
- Keep additions mechanically consistent with nearby sections.
- Use contribution requests when specialist mode blocks direct shared-artifact edits.
- Resolve titled spec directories before reading or editing them. Do not assume a literal `docs/specifications/<ID>/MASTER_TECH_SPEC.md` path exists.

## Guardrails

- Do not invent a fresh subsystem when the task is a direct edit.
- Do not write final deliverables to desktop export folders unless explicitly requested.
- Do not claim schema or validator success unless you actually ran the check.
