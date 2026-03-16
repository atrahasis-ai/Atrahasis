# Codex-Claude Coexistence Protocol
**Platform:** OpenAI Codex
**Purpose:** Rules for operating alongside Claude without corrupting shared AAS state
**Shared boundary:** See `docs/platform_overlays/SHARED_OPERATING_MODEL.md` and `docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md`

---

## Shared Canon

These files are shared and must remain vendor-neutral:

- `docs/AGENT_STATE.md`
- `docs/SESSION_BRIEF.md`
- `docs/DECISIONS.md`
- `docs/TODO.md`
- `docs/COMPLETED.md`
- `docs/INVENTION_DASHBOARD.md`
- `docs/TRIBUNAL_LOG.md`
- `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md`
- `docs/task_workspaces/*`
- invention specs, invention logs, and prior-art artifacts

Rules:
- do not inject Codex-specific runtime instructions into shared canon
- do not remove Claude-specific history from ADRs or archives
- preserve neutral invention content regardless of authoring platform

---

## Codex-Only Files

Safe to modify freely:

- `docs/platform_overlays/codex/MODEL_ROUTING.md`
- `docs/platform_overlays/codex/RUNTIME.md`
- `docs/platform_overlays/codex/COEXISTENCE.md`
- `docs/platform_overlays/codex/TEAM_FORMATION.md`
- `docs/platform_overlays/codex/templates/*`

---

## Parallel Execution

When both platforms are active at the same time, follow the shared protocol:

- claim tasks through `docs/task_claims/<TASK_ID>.yaml`
- write only inside the claimed task safe zone during execution
- treat shared state as read-only during parallel execution
- emit shared-state updates through `docs/handoffs/<TASK_ID>_CODEX_HANDOFF.md`
- wait for designated sequential closeout before shared files are updated
- for `FULL PIPELINE` tasks, do not promote any ideation concept or create per-invention artifacts until `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` records explicit user approval
- if the completed task appears in `docs/TODO.md`'s `User Dispatch Order (Simple)`, queue the exact UDO removal in the handoff rather than editing that section live
- spawned Codex child sessions inherit the parent's claim and safe-zone limits unless the parent explicitly narrows them further
- a child session is not a separate platform for lock purposes; the parent session remains responsible for protocol compliance

`TODO.md` is visibility-only during parallel execution. It is not the lock mechanism.

---

## Conflict Prevention

### Rule 1: Read before overwrite
Before editing shared state, read the current repo version and preserve any unrelated changes.

### Rule 2: Keep shared files vendor-neutral
If platform-specific guidance is needed, put it in the Codex overlay and reference it indirectly.

### Rule 3: ADRs are historical memory
ADR-030 remains as accepted historical record even though active routing now lives in overlays.

### Rule 4: Repo is canonical
Use the repo as the only live working state. Do not treat desktop output folders as active context.

### Rule 5: Flag, do not erase
If Codex finds platform-specific leakage in shared files, flag it and propose relocation rather than silently deleting it.

---

## Recovery Behavior

If Claude completed substantive work but failed to update shared memory:

1. recover the invention artifact from the repo if present
2. reconstruct missing state updates neutrally
3. record the recovery in shared logs
4. avoid rewriting the invention itself unless required
