# Task Handoff: T-290 - AACP v2 Cross-Layer Integration with Atrahasis Stack
**Platform:** CODEX
**Agent:** Anu
**Completed:** 2026-03-13T22:19:28Z
**Pipeline verdict:** COMPLETE - DIRECT SPEC

---

## Artifacts Created

| Path | Description |
|------|-------------|
| `docs/task_workspaces/T-290/README.md` | Workspace summary and scope note |
| `docs/task_workspaces/T-290/TASK_BRIEF.md` | Task scope, prerequisites, governing authorities, and non-goals |
| `docs/task_workspaces/T-290/WORKFLOW_SUMMARY.md` | Summary of the completed integration design |
| `docs/task_workspaces/T-290/CROSS_LAYER_INTEGRATION_SPEC.md` | Canonical `T-290` deliverable defining `AXIP-v1` |

---

## Shared State Updates Required

Apply these changes only during serialized shared-state closeout, after
re-reading the live files.

### TODO.md

Live-sync note:
- The temporary `Active / In Progress` row for `T-290` has already been removed.

Backlog section changes still required at serialized closeout:
- Remove the `Cross-layer integration lane` bullet under `Wave 6 - Ecosystem and Cross-Layer Integration (After Wave 5)`:

```markdown
- `Cross-layer integration lane`: `T-290`. Treat as a broad existing-stack integration surface and do not overlap it with any retrofit task that touches the same layers.
```

- Remove the `T-290` row from the Wave 6 table:

```markdown
| T-290 | AACP v2 Cross-Layer Integration with Atrahasis Stack | DIRECT SPEC | HIGH | T-210, T-230, T-240, T-214 | Specify integration with C3, C5, C7, C8, C23, C24, C36, and the rest of the current stack. |
```

- Remove `+ T-290` from `User Dispatch Order (Simple)` step 1 so it becomes:

```markdown
1. `PARALLEL` - one of `T-261 / T-262 / T-280` + `T-281`
```

- Increment the completed-task count in the final `Completed tasks are archived...`
  line by `+1` relative to the live value at the time of closeout.
- Update the trailing `Last updated` note if that line is touched during the
  same serialized pass.

### COMPLETED.md

Append one completed-task row using the live file's existing sort/order
conventions:

```markdown
| T-290 | AACP v2 Cross-Layer Integration with Atrahasis Stack | 2026-03-13 | Direct-spec integration update. Defined `AXIP-v1`, the canonical native AACP/AASL cross-layer integration profile for the Atrahasis stack: `C39` class allocation for C3/C5/C6/C7/C8/C23/C24/C36, minimum `C40` profile floors, internal-vs-public semantic posture rules, runtime evidence split (`task_result` vs `attestation_submit`), habitat gateway no-rewrite rules, and the additive-to-retrofit boundary for `T-302+`. Agent: Anu (Codex). |
```

### SESSION_BRIEF.md

Optional but useful:
- add a current-state bullet noting that `T-290` is complete and `AXIP-v1` now
  gives `T-300`, `T-302`, `T-303`, `T-304`, `T-305`, `T-306`, and `T-281` a
  single native integration target.

### AGENT_STATE.md

No append required.
- `T-290` does not mint a new invention entry.

### DECISIONS.md

No append required.
- `T-290` is a direct-spec integration contract, not a new ADR.

### INVENTION_DASHBOARD.md

No append required.
- No new invention ID was created.

### TRIBUNAL_LOG.md

No append required.
- This task does not mint a tribunal-scored invention closeout.

---

## Notes

- This task is intentionally additive. It does not directly rewrite the live
  `C3`, `C5`, `C7`, `C8`, or `C36` texts; it defines the target profile those
  later retrofit tasks must consume.
- The main substantive design choice is the split between:
  - public native `AASL` surfaces,
  - internal native surfaces,
  - and temporary internal layer-local payload carriage during retrofit.
- `T-261` was already actively claimed during this closeout, so the backlog and
  completed-file updates were intentionally deferred to serialized shared-state
  cleanup.
