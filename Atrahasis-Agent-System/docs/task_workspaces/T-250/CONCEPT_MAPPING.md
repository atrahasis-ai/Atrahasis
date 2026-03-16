# T-250 Concept Mapping
**Agent:** Nergal (Codex)
**Date:** 2026-03-13

## Promoted Concepts

| Concept ID | Invention ID | Title | Decision |
|------------|-------------|-------|----------|
| IC-4 | C43 | Custody-Bounded Semantic Bridge (CBSB) | ADVANCE |
| IC-3 | - | Bridge-Resident Semantic Cell | NOT SELECTED |
| IC-2 | - | Snapshot-Bound Provenance Bridge | NOT SELECTED |
| IC-1 | - | Thin Passthrough Adapter | NOT SELECTED |

## Rationale

The user asked for a second council pass to determine whether the strengths of
`IC-2` and `IC-3` could be combined into a better solution, or whether `IC-3`
alone should win. The council rejected `IC-3` as the default bridge concept
because it overreaches into quasi-native framework/runtime behavior and weakens
bridge honesty.

`IC-4` is stronger because it:
- keeps `IC-2` as the architectural base,
- imports only the useful bridge-side state from `IC-3`,
- preserves signed bridge-scoped inventory snapshots,
- keeps source-observed versus bridge-inferred semantics explicitly separated,
- and allows bounded warm-state or derated continuation behavior without
  claiming native `C42` equivalence.

## C43 Safe Zone
- `docs/task_workspaces/T-250/`
- `docs/prior_art/C43/`
- `docs/specifications/C43/`
- `docs/invention_logs/C43_IDEATION.md`
- `docs/invention_logs/C43_REFINED_INVENTION_CONCEPT.yaml`
- `docs/invention_logs/C43_FEASIBILITY.md`
- `docs/invention_logs/C43_ASSESSMENT.md`
