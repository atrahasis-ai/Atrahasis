# AAS3 Task ID Policy
**Scope:** Runtime-enforced task ID allocation for the Atrahasis Agent System
**Effective:** 2026-03-13

---

## Purpose

Task IDs are semantic bands, not arbitrary labels.

The AAS3 runtime now uses task-ID classes to separate:

- canonical shared backlog work
- ad hoc analysis and idea workflows
- runtime and provider validation
- demos and operator walkthroughs

This prevents exploratory runs from polluting canonical backlog numbering.

---

## Task Bands

### Canonical shared backlog

- `T-001` to `T-7999`
- Use for real shared work tied to:
  - `docs/TODO.md`
  - `docs/task_claims/`
  - handoffs
  - serialized closeout
- Default class for `AASBT`

### Ad hoc analysis / questions / idea integration

- `T-9000` to `T-9499`
- Use for:
  - `AASA`
  - `AASAQ`
  - `AASNI`
- These runs are exploratory unless explicitly promoted later

### Runtime / provider / system validation

- `T-9500` to `T-9799`
- Use for:
  - provider-runtime checks
  - orchestration validation
  - workflow sanity checks
  - system verification tasks

### Demo / operator walkthroughs

- `T-9800` to `T-9999`
- Use for:
  - demonstrations
  - operator-interface walkthroughs
  - prompt or UX test scenarios

---

## Runtime Rules

- `AASBT` requires an explicit task ID and that ID must be canonical unless it refers to an existing legacy workspace.
- `AASA`, `AASAQ`, and `AASNI` may omit the task ID.
- If no task ID is supplied for `AASA`, `AASAQ`, or `AASNI`, the runtime auto-mints the next free task ID in the correct band.
- The runtime checks both `docs/task_workspaces/` and `docs/task_claims/` before minting or accepting a new task ID.
- Existing historical task IDs remain valid if they already exist in the repo, even if they do not follow the new preferred ranges.

---

## Operator Guidance

- Do not add ad hoc runs to `docs/TODO.md` unless explicitly promoted into canonical shared work.
- If an ad hoc run becomes a real shared task, promote it into canonical backlog space rather than treating the exploratory task ID as backlog authority.
- If a band ever nears exhaustion, widen the range upward without renumbering historical tasks.
