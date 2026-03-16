# Task Handoff: <TASK_ID> — <Title>
**Platform:** CLAUDE | CODEX
**Completed:** <ISO-8601 timestamp>
**Pipeline verdict:** APPROVE | ADVANCE | CONDITIONAL_ADVANCE | REJECT

---

## Invention Artifacts Created

| Path | Description |
|------|-------------|
| `docs/task_workspaces/<TASK_ID>/HITL_APPROVAL.md` | Explicit user concept-selection record required before any new `C-xxx` is minted |
| `docs/specifications/<ID>/MASTER_TECH_SPEC.md` | Final deliverable |
| `docs/specifications/<ID>/architecture.md` | System architecture |
| `docs/invention_logs/<ID>_IDEATION.md` | Ideation stage output |
| ... | ... |

---

## Approval Evidence (FULL PIPELINE only)

- Approval artifact: `docs/task_workspaces/<TASK_ID>/HITL_APPROVAL.md`
- Approved concept ID(s): `<IC-x>`
- Closeout rule: if this artifact is missing, no new `C-xxx` invention may be added to shared state

---

## Shared State Updates Required

### TODO.md
- Move T-<ID> from Active to completed (or remove from AAS Pipeline Required section)
- Remove `T-<ID>` from `User Dispatch Order (Simple)` if it appears there

### COMPLETED.md
Append:
```
| T-<ID> | <Title> | <date> | <summary> |
```

### AGENT_STATE.md
Add invention entry under `inventions:`:
```yaml
  C<ID>:
    title: "<Title>"
    stage: "ASSESSMENT"
    status: "COMPLETE"
    master_tech_spec: "docs/specifications/C<ID>/MASTER_TECH_SPEC.md"
    ...
```

### DECISIONS.md
Append ADR:
```
## ADR-<NNN> — <Title>
**Date:** <date>
**Status:** ACCEPTED
**Context:** ...
**Decision:** ...
**Consequences:** ...
**References:** docs/specifications/C<ID>/MASTER_TECH_SPEC.md
**Invention:** C<ID>
```

### INVENTION_DASHBOARD.md
Add row:
```
| C<ID> | <Title> | COMPLETE | docs/specifications/C<ID>/MASTER_TECH_SPEC.md |
```

### SESSION_BRIEF.md
Update "Latest Closed Invention" section.

### TRIBUNAL_LOG.md
Append council transcript summary.

---

## Assessment Scores
- Novelty: <1-5>
- Feasibility: <1-5>
- Impact: <1-5>
- Risk: <1-10> (<level>)

---

## Notes
<Any cross-invention dependencies, monitoring flags, or items for the other platform to be aware of>
