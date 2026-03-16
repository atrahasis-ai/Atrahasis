# Shared AAS Operating Model
**Scope:** Vendor-neutral operating boundary for all platforms running the Atrahasis Agent System
**Effective:** 2026-03-11

---

## Purpose

This document defines the shared operating model for running AAS across multiple agent platforms without corrupting the canonical Atrahasis state.

It separates:
- shared AAS process and constitutional rules
- platform-specific runtime behavior
- export/archive behavior outside the repo

---

## Canonical Working State

All active AAS work is repo-canonical.

- **Canonical repo root:** `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\`
- **Canonical docs root:** `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\docs\`

All platforms must:
- read shared state from the repo
- write active AAS artifacts to the repo
- treat the repo as the only source of truth during active execution

---

## Desktop Export Policy

The desktop Atrahasis folder is not canonical working state.

- **Optional export/archive root:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\`

Rules:
- do not treat the desktop folder as live state during pipeline execution
- do not read from the desktop folder unless performing historical recovery requested by the user
- export to the desktop folder only when the user explicitly requests archive/publish/export behavior

Historical desktop paths that appear in older artifacts remain valid as provenance, not as active routing instructions.

---

## Shared Canon

These files are shared, vendor-neutral, and authoritative:

- `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md`
- `docs/AGENT_STATE.md`
- `docs/SESSION_BRIEF.md`
- `docs/INVENTION_DASHBOARD.md`
- `docs/DECISIONS.md`
- `docs/PATTERN_REGISTER.md`
- `docs/TRIBUNAL_LOG.md`
- `docs/TODO.md`
- `docs/COMPLETED.md`
- all `docs/task_workspaces/*`
- all `docs/specifications/*`
- all `docs/invention_logs/*`
- all `docs/prior_art/*`

Rules:
- no vendor-specific model names in shared state except as historical ADR content
- no platform-specific runtime instructions in shared canon
- no deletion of historical decisions solely because they came from another platform

---

## Platform Overlays

Platform overlays contain execution details that are specific to a given agent environment.

- `docs/platform_overlays/claude/`
- `docs/platform_overlays/codex/`
- `docs/platform_overlays/gemini/`
- `docs/platform_overlays/PROVIDER_RUNTIME_ABSTRACTION.md`

Allowed overlay content:
- model routing
- runtime/tooling assumptions
- session persistence mechanics
- coexistence guidance

Overlay files must not replace or contradict the shared constitutional workflow. They only map platform behavior onto the shared process.

---

## HITL Gate Responsibility

Shared constitutional HITL gates remain mandatory even when the user is talking
directly to a task-executing platform agent.

Rules:
- If there is no separate persistent Director session, the assigned platform agent
  acts as the Director proxy for HITL gates.
- For any `FULL PIPELINE` task, execution MUST stop after `IDEATION` until the user
  explicitly selects which concept(s), if any, should advance.
- That approval must be recorded in
  `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` before any `C-xxx` invention ID is
  minted or any per-invention artifact path is created.
- `recommended_concepts` are advisory only. They are not approval evidence.

---

## Collaboration Rules

1. One source of truth
Shared state is updated in the repo only.

2. Preserve unrelated changes
If another platform has modified a shared file, preserve those changes unless the user explicitly asks for reversion.

3. Platform-neutral invention content
Specifications, research, feasibility outputs, and assessment artifacts are platform-independent by default.

4. Historical ADRs stay
ADR entries remain append-only historical memory, even when they describe platform-specific decisions that have since moved into overlays.

5. Export is deliberate
Desktop export is a post-processing step, not part of the active execution path.

---

## Legacy Path Semantics

Older files may still contain:
- `output_folder` paths under `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\...`
- source document paths under `C:\Users\jever\OneDrive\Desktop\Atrahasis\...`
- inline `Output location:` references inside older invention artifacts

Interpretation:
- these are historical provenance or archive references
- they do not override repo-canonical working behavior
- when touched during maintenance, prefer clarifying them rather than deleting them

---

## Recommended Multi-Platform Workflow

1. Read shared state from `docs/`
2. Read the current platform overlay
3. Execute the AAS stage workflow
   - for `FULL PIPELINE` tasks, pause after `IDEATION`, obtain user concept
     approval, and persist `HITL_APPROVAL.md` before promotion
4. Write new/updated artifacts to the repo
5. Update shared state neutrally
6. Export/archive to desktop only if the user asks

---

## Parallel Execution

When multiple platforms run simultaneously, see `docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md` for:
- Task claiming via `docs/task_claims/`
- Safe zone / danger zone boundaries
- Handoff-based shared-state updates via `docs/handoffs/`
- Serialized closeout procedure
- Stale claim recovery

For backend registration and model-tier routing, see `docs/platform_overlays/PROVIDER_RUNTIME_ABSTRACTION.md`.

---

## Authority Boundary

If there is a conflict:
- shared constitutional process wins over platform overlay
- explicit user instruction wins over both
