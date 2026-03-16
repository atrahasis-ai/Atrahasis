# Parallel Execution Protocol
**Scope:** Dual-agent (Claude + Codex) concurrent operation on AAS tasks
**Effective:** 2026-03-12
**Authority:** Supplements `SHARED_OPERATING_MODEL.md`

---

## Overview

Two platforms can work on different AAS tasks simultaneously. This protocol prevents file conflicts through three mechanisms:

1. **Claim files** — per-task lock in `docs/task_claims/`
2. **Safe zones** — each task's files are exclusively owned by the claiming platform
3. **Handoff files** — shared-state updates are queued, not applied directly

Task IDs and invention IDs are not the same thing:
- `T-xxx` identifies the task / problem space being worked
- `C-xxx` identifies an invention only after ideation has produced a concept that is approved to advance
- a task claim may therefore begin with **no invention IDs** and later expand to **one or more**

---

## 1. Task Claiming

### Mechanism
Each claimed task gets a YAML file in `docs/task_claims/`:

```
docs/task_claims/T-060.yaml
docs/task_claims/T-061.yaml
```

### Claim file format
```yaml
task_id: "T-060"
invention_ids: []
target_specs: []
title: "Sentinel Graph"
platform: "CODEX"
agent_name: "Marduk"
claimed_at: "2026-03-11T14:00:00Z"
updated_at: "2026-03-11T14:30:00Z"
status: "IN_PROGRESS"
scope:
  safe_zone_paths:
    - "docs/task_workspaces/T-060/"
  pipeline_type: "AAS"
notes: ""
```

The `agent_name` field must match the agent's registered name in `docs/platform_overlays/AGENT_REGISTRY.md`.

### Rules
- Before claiming, read all existing claim files to check for conflicts
- A task may only be claimed by one platform at a time
- Claim files are the authoritative lock — not TODO.md
- Create the claim file BEFORE starting any task work
- A task may start with `invention_ids: []` and later gain one or more `C` IDs after concept promotion
- For `FULL PIPELINE` tasks, `invention_ids` MUST remain `[]` until `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` exists and records the user's explicit concept-selection approval
- When invention IDs are minted, update both `invention_ids` and `scope.safe_zone_paths`
- `recommended_concepts`, `CONCEPT_MAPPING.md`, or claim-file notes are not substitutes for approval evidence
- If one task spawns multiple inventions that need independent concurrent execution, split them into follow-on task claims or wait for explicit user direction before overlapping safe zones
- Update `status` field as work progresses: `CLAIMED` → `IN_PROGRESS` → `DONE`
- Update `updated_at` whenever `status` changes
- **TODO.md live sync (mandatory):** When claiming a task, the platform MUST also add a row to the `Active / In Progress` table in `docs/TODO.md`. When a task reaches `DONE`, the platform MUST remove that row. If the task also appears in `TODO.md`'s `User Dispatch Order (Simple)` section, the completion path MUST also remove that task ID from the UDO during closeout (or immediately in solo execution). See Section 7 for details.

### Direct spec edit claims
For non-AAS tasks that edit existing specs, the claim scope lists the target spec files:

```yaml
task_id: "T-070"
invention_ids: []
target_specs: ["C3"]
title: "Specify Capsule Epoch Protocol"
platform: "CLAUDE"
claimed_at: "2026-03-11T14:00:00Z"
updated_at: "2026-03-11T14:00:00Z"
status: "IN_PROGRESS"
scope:
  safe_zone_paths:
    - "docs/specifications/C3/MASTER_TECH_SPEC.md"
  pipeline_type: "DIRECT_EDIT"
notes: "Adding section to C3"
```

Two direct-edit tasks targeting the SAME spec file must NOT run in parallel.

---

## 2. Safe Zones (parallel-safe, no coordination needed)

During execution, a platform may freely create/edit only files within its claimed task's safe zone:

| Task Type | Safe Zone |
|-----------|-----------|
| AAS task before invention promotion | `docs/task_workspaces/<TASK_ID>/` |
| AAS task after invention promotion | `docs/task_workspaces/<TASK_ID>/`, plus `docs/specifications/<ID>/*`, `docs/invention_logs/<ID>*`, `docs/prior_art/<ID>/*`, `docs/contribution_requests/<ID>.yaml` for each claimed invention |
| Direct spec edit | The specific target spec file(s) listed in the claim |
| Governance / docs maintenance | The exact shared docs listed in the claim |

A platform must NEVER write to another platform's safe zone.

### Promotion precondition for FULL PIPELINE tasks

Before any promoted invention safe zone is created, the claiming platform MUST:
- stop after `IDEATION`,
- present the concept options to the user,
- wait for explicit concept approval,
- write `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md`.

Until that artifact exists:
- `invention_ids` stays empty,
- no `docs/specifications/C*` path may be created,
- no `docs/invention_logs/C*` path may be created,
- no `docs/prior_art/C*` path may be created.

---

## 3. Danger Zone (shared state — read only during parallel execution)

These files are read-only during parallel task execution:

- `docs/AGENT_STATE.md`
- `docs/SESSION_BRIEF.md`
- `docs/TODO.md` — **exception:** the `Active / In Progress` table may be updated per Section 7
- `docs/COMPLETED.md`
- `docs/INVENTION_DASHBOARD.md`
- `docs/DECISIONS.md`
- `docs/TRIBUNAL_LOG.md`
- `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md`
- `docs/platform_overlays/SHARED_OPERATING_MODEL.md`

Both platforms may READ these files at any time. Neither platform may WRITE to them while any other platform has an active (non-DONE) claim, except for the TODO.md exception noted above.

---

## 4. Handoff Files (completion packets)

When a task is complete, the platform creates a handoff file instead of updating shared state directly:

```
docs/handoffs/<TASK_ID>_<PLATFORM>_HANDOFF.md
```

Example: `docs/handoffs/T-060_CODEX_HANDOFF.md`

The handoff file contains exact text/deltas for every shared file that needs updating. See `docs/handoffs/HANDOFF_TEMPLATE.md` for the required format.

### What goes in a handoff file
1. Task ID and completion status
2. For `FULL PIPELINE` tasks, the path to `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` and the approved concept ID(s)
3. Pipeline verdict and scores
4. Exact YAML to append to `AGENT_STATE.md`
5. Exact markdown row to append to `COMPLETED.md`
6. Exact ADR text to append to `DECISIONS.md`
7. Exact row to append to `INVENTION_DASHBOARD.md`
8. Exact transcript to append to `TRIBUNAL_LOG.md`
9. `SESSION_BRIEF.md` update text
10. `TODO.md` changes (task removal/status change, plus `User Dispatch Order (Simple)` removal/update if the task appears there)

---

## 5. Serialized Closeout

After both platforms finish their tasks, shared state is updated in a single sequential pass. **Codex is the default closeout platform.**

### Closeout procedure (Codex)
1. User confirms both platforms are done (or Codex checks that no active non-DONE claims remain)
2. Codex reads ALL handoff files in `docs/handoffs/`
3. For any handoff that mints a new `C-xxx`, Codex verifies that the referenced `HITL_APPROVAL.md` exists and records explicit concept approval
4. Codex applies all deltas to shared state files in one pass
5. Codex updates `TODO.md` to reflect new status (human-readable board), including removing completed task IDs from `User Dispatch Order (Simple)`
6. Codex sets all claim file statuses to `DONE`
7. Codex moves processed handoff files to `docs/handoffs/applied/`

### Claude's role at closeout
Claude does NOT update shared state after parallel execution. Claude writes a handoff file and waits. If Codex is unavailable for closeout, the user may explicitly direct Claude to perform closeout instead.

### Why always Codex
One designated platform eliminates ambiguity about who integrates. Codex is chosen because it operates against the repo directly and can do sequential file updates reliably.

---

## 6. Stale Claim Recovery

### When is a claim stale?
A claim is considered potentially stale if:
- `status` is `CLAIMED` or `IN_PROGRESS`
- AND more than **24 hours** have passed since `updated_at` (or `claimed_at` if `updated_at` is missing)
- AND the claiming platform has not updated the claim file or produced any safe-zone artifacts

### Recovery procedure
1. The user (not a platform) decides whether to release a stale claim
2. To release: change the claim file `status` to `ABANDONED` and add a note
3. The task can then be re-claimed by either platform with a new claim file
4. Any partial artifacts in the safe zone should be reviewed before re-use

### Platform crash recovery
If a platform crashes mid-task:
- Its claim file remains in `docs/task_claims/` with status `IN_PROGRESS`
- The other platform must NOT auto-claim it — wait for user direction
- The user inspects the safe zone for partial work and decides whether to:
  - Resume on the same platform
  - Abandon and re-assign to the other platform
  - Salvage partial artifacts and continue

---

## 7. TODO.md Live Sync

`TODO.md` is a **human-readable status board** that must reflect reality in real time. It is NOT a lock mechanism — the authoritative claim/lock state lives in `docs/task_claims/` — but it MUST stay in sync with actual work.

### Mandatory updates (even during parallel execution)

**When claiming a task**, the platform MUST add a row to the `Active / In Progress` table:

```markdown
| T-060 | Sentinel Graph | IN_PROGRESS | CRITICAL | AAS | Claimed by Marduk (CODEX), 2026-03-12 |
```

The row must include: task ID, title, status, priority, pipeline type, and the agent's registered name + platform with the date.

**When a task reaches DONE**, the platform MUST remove its row from the `Active / In Progress` table.

### User Dispatch Order maintenance

`TODO.md` also contains a `User Dispatch Order (Simple)` section that the user relies on for delegation order.

Rules:
- If a completed task ID appears in `User Dispatch Order (Simple)`, that task ID MUST be removed from the UDO.
- During **parallel execution**, UDO edits are **not** part of the narrow live-sync exception. The completing platform MUST put the exact UDO removal/update into its handoff so the designated closeout platform can apply it safely.
- During **solo execution**, the active platform may remove the completed task ID from the UDO directly as part of the normal TODO update.
- If a UDO step references a completed prerequisite indirectly, remove only the completed task ID(s) unless the user explicitly asks for a broader rewrite.

### Conflict avoidance
- Each platform only adds/removes its own row — never another platform's
- This is a narrow, well-defined write (one table row) that does not conflict with other platforms' rows
- All other sections of TODO.md, including `User Dispatch Order (Simple)`, remain read-only during parallel execution except through serialized closeout
- The authoritative lock is still the claim file, not TODO.md

---

## 8. Solo Execution (no parallel run)

When only one platform is active (user confirms the other is not running):
- Claim files are optional but recommended for consistency
- The active platform may update shared state directly (no handoff file needed)
- The handoff protocol is only mandatory during confirmed parallel execution

---

## Quick Reference

```
BEFORE STARTING:
  1. Read docs/task_claims/*.yaml — check for active claims
  2. Create docs/task_claims/T-<ID>.yaml with status: CLAIMED
     - use invention_ids: [] if no invention has been promoted yet
  3. Update status to IN_PROGRESS when work begins
  4. Add a row to docs/TODO.md "Active / In Progress" table (MANDATORY)

DURING EXECUTION:
  5. Write ONLY to your safe zone paths
  6. For `FULL PIPELINE` tasks, stop after IDEATION, obtain user concept approval, and write `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md`
  7. Only after approval exists may the task mint one or more inventions, update invention_ids, and expand safe_zone_paths
  8. READ shared state as needed, but do NOT WRITE (except your TODO.md row)
  9. If you detect overlap with another claim, STOP and flag to user

WHEN DONE:
  10. Remove your row from docs/TODO.md "Active / In Progress" table (MANDATORY)
  11. If T-<ID> appears in "User Dispatch Order (Simple)", include the exact UDO removal/update in your handoff
  12. Create docs/handoffs/T-<ID>_<PLATFORM>_HANDOFF.md
  13. Update your claim file status to DONE
  14. Wait for closeout (user designates who applies handoffs)

CLOSEOUT (one platform, sequential):
  15. Read all handoff files
  16. Verify approval evidence for any new `C-xxx`
  17. Apply all deltas to shared state, including User Dispatch Order removals
  18. Move applied handoffs to docs/handoffs/applied/ (optional)
```
