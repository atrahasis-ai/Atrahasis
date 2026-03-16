# T-230 Concept Mapping
**Agent:** Marduk (Codex)
**Date:** 2026-03-12

## Promoted Concepts

| Concept ID | Invention ID | Title | Decision |
|------------|-------------|-------|----------|
| IC-2 | C40 | Dual-Anchor Authority Fabric (DAAF) | ADVANCE |
| IC-1 | - | Federated Security Gateway | NOT SELECTED |
| IC-3 | - | Capability-Lease Security Mesh | NOT SELECTED |

## Rationale

IC-2 is the only concept that satisfies all four `T-230` constraints at once:
- preserves a sovereign native-agent trust anchor,
- admits standard federation and workload identity for non-agent actors,
- binds security to canonical protocol meaning rather than transport bytes alone,
- keeps least-authority explicit without dragging the whole runtime and tool
  lifecycle into L3.

IC-1 is easier to roll out but recenters trust in a conventional gateway layer.
IC-3 has the strongest least-authority posture, but it pre-designs too much of
`T-240` and `C23` before those downstream surfaces are allowed to speak for
themselves.

## C40 Safe Zone
- `docs/task_workspaces/T-230/`
- `docs/prior_art/C40/`
- `docs/specifications/C40/`
- `docs/invention_logs/C40_IDEATION.md`
- `docs/invention_logs/C40_REFINED_INVENTION_CONCEPT.yaml`
- `docs/invention_logs/C40_FEASIBILITY.md`
- `docs/invention_logs/C40_ASSESSMENT.md`
