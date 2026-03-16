---
name: aas5-hitl-gates
description: Enforce Atrahasis human-approval boundaries, including degraded-mode acknowledgement requirements for AAS5 ordinary ideation.
---

# AAS5 HITL Gates

## Overview

Use this skill to decide whether work must stop for the operator and to produce the exact approval artifact or decision packet needed.

## Workflow

1. Identify whether the next action crosses a HITL gate.
2. For `FULL PIPELINE`, stop after `IDEATION` and require `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` before minting any `C-xxx` invention.
3. If ordinary AAS5 ideation is degraded rather than fully simultaneous, require explicit degraded-mode acknowledgement separately from concept-promotion approval.
4. If approval is required, prepare the narrowest possible decision packet:
   - concepts or options
   - strongest pros and objections
   - explicit recommendation
   - exact operator choice required
5. Record approval only in the canonical artifact path for the task.
6. Resume only after explicit approval evidence exists.

## Gates To Watch

- concept selection or promotion
- doctrinal pivots
- external research where approval is required
- patent strategy
- public disclosure
- abandonment
- resource-intensive prototyping

## Guardrails

- Do not treat `recommended_concepts` as approval evidence.
- Do not treat degraded-mode acknowledgement as concept-promotion approval, or concept-promotion approval as degraded-mode acknowledgement.
- Do not let a child session satisfy a HITL gate.
- Do not mint invention IDs before explicit approval is recorded.
