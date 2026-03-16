# Task Handoff: T-085 - Add Heuristic Family Store to C6
**Platform:** CODEX
**Agent:** Inanna
**Completed:** 2026-03-12T08:53:56Z
**Pipeline verdict:** DIRECT_EDIT_COMPLETE

---

## Artifacts Updated

| Path | Description |
|------|-------------|
| `docs/specifications/C6/MASTER_TECH_SPEC.md` | Added Section 7.2.5 `Heuristic Family Store`, linked heuristic-family retirement into catabolism/archive/bundle compaction, extended retrieval and semantic-index filtering with `heuristic_family_id`, added parameters/conformance/test vector/glossary entries, and updated C6 version metadata/changelog to v2.0.4 |

---

## Shared State Updates Required

### TODO.md

Live-sync note:
- The temporary Active / In Progress row for `T-085` was added and then removed per the parallel execution protocol when the task reached `DONE`.

Backlog section changes still required at serialized closeout:
- Remove this row from `Direct Spec Edits (No AAS Pipeline) -> LOW Priority`:
```markdown
| T-085 | Add Heuristic Family Store to C6 | Missing section | C6 | H-class claims exist in the C5 taxonomy but heuristics are not grouped into "families" for tracking, versioning, or retirement. |
```
- Increase the completed-task count in:
```markdown
Completed tasks are archived in [COMPLETED.md](COMPLETED.md) (84 tasks).
```
by `+1` relative to the then-current live value when this handoff is applied.
- Update the footer line to reflect `T-085` closeout if this handoff is the latest applied closeout at integration time.

### COMPLETED.md

Append:
```markdown
| T-085 | Add Heuristic Family Store to C6 | 2026-03-12 | Direct spec edit completed by Inanna (Codex). Added C6 Section 7.2.5 `Heuristic Family Store`, defined H-class family membership/frontier/deprecation/retirement rules, extended retrieval and semantic indexing with `heuristic_family_id` and retired-family opt-in behavior, linked retired heuristic families into catabolism/archive/bundle compaction, and added D.10, E.8, TV-11, glossary entries, and v2.0.4 changelog metadata. |
```

### No Other Shared-State Updates Required

This task is a direct spec edit only. No updates are required for:
- `docs/AGENT_STATE.md`
- `docs/SESSION_BRIEF.md`
- `docs/INVENTION_DASHBOARD.md`
- `docs/DECISIONS.md`
- `docs/TRIBUNAL_LOG.md`

---

## Notes

- Verification was by targeted readback of the edited `C6` graph, retrieval, appendix, and changelog sections; no automated validator exists for this markdown spec edit.
- The heuristic family store is specified as an H-class-only overlay separate from the claim family graph, so proposition lineage and pragmatic recommendation versioning remain distinct.
