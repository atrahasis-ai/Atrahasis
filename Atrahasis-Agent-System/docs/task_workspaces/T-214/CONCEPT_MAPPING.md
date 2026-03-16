# T-214 Concept Mapping
**Agent:** Inanna (Codex)
**Date:** 2026-03-12

## Promoted Concepts

| Concept ID | Invention ID | Title | Decision |
|------------|-------------|-------|----------|
| IC-2 | C41 | Layered Semantic Capability Manifest (LSCM) | ADVANCE |
| IC-1 | - | Signed Endpoint Capability Card | NOT SELECTED |
| IC-3 | - | Dynamic Operational Manifest Ledger | NOT SELECTED |

## Rationale

IC-2 is the only concept that satisfies all of `T-214`'s hard constraints at
once:
- it gives Alternative B a richer discovery contract than legacy agent cards,
- it keeps durable capability truth separate from live operational state,
- it carries `C40` trust posture and signature-chain rules without turning the
  manifest into a security-only sidecar,
- it gives `T-251`, `T-261`, `T-262`, `T-281`, and `T-290` a concrete manifest
  surface without pre-designing their downstream internals.

IC-1 is easier to ship but too shallow for semantic-capability discovery.
IC-3 is ambitious, but it collapses discovery, registry, and observability into
one unstable surface.

## C41 Safe Zone
- `docs/task_workspaces/T-214/`
- `docs/prior_art/C41/`
- `docs/specifications/C41/`
- `docs/invention_logs/C41_IDEATION.md`
- `docs/invention_logs/C41_REFINED_INVENTION_CONCEPT.yaml`
- `docs/invention_logs/C41_FEASIBILITY.md`
- `docs/invention_logs/C41_ASSESSMENT.md`
