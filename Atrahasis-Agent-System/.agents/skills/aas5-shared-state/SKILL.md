---
name: aas5-shared-state
description: Handle AAS5 claim files, safe zones, handoffs, shared-state edits, and closeout rules. Use when work touches shared canonical docs, when parallel execution is active, or when a task may require a handoff instead of a direct edit.
---

# AAS5 Shared State

## Overview

Use this skill to keep canonical repo state coherent when claims, handoffs, or closeout rules apply.

## Workflow

1. Read all current `docs/task_claims/*.yaml` files before editing.
2. Treat claims as the authoritative lock, not `TODO.md`.
3. Write only inside the claimed safe zone.
4. Queue shared-state updates through `docs/handoffs/` when the parallel protocol requires it.
5. Keep Synthesis-owned shared artifacts read-only unless the current mode is explicitly synthesis.
6. Close out cleanly:
   - release or complete claim state
   - update shared docs only where allowed
   - remove completed tasks from `TODO.md` or queue the exact removal in the handoff
   - run required validators

## Guardrails

- Do not improvise around overlapping safe zones.
- Do not edit Synthesis-owned surfaces directly from a specialist mode.
- Do not modify `docs/TODO.md` live during parallel execution when the protocol says to queue the change.
