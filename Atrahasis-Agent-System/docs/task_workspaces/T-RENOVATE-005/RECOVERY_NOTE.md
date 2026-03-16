# T-RENOVATE-005 Recovery Note

## Recovery Status

Recovered by `Ninkasi` on `2026-03-14` after user-confirmed terminal failure on the prior `Enki` session.

## Canonical Scope Correction

The stale live claim incorrectly targeted `C22`.

The canonical task definition in `docs/specifications/STRATEGY/RENOVATION_TASKS.md` defines `T-RENOVATE-005` as:

- target: `C3 Noosphere`
- purpose: sever public connections and define the unidirectional osmosis boundary with a mandatory `Data Quarantine Filter`

The claim has been corrected to that canonical scope.

## Salvage Review

No partial workspace, handoff, or committed spec diff was found for the stale `C22`-scoped claim.

So this task is resumed from:

- the canonical renovation task definition,
- the recovered redesign synthesis in `docs/task_workspaces/T-9004/RECOVERY_CONSOLIDATED_SYNTHESIS.md`,
- and the existing `C3` master spec.

## Immediate Next Editing Goals

1. Identify where `C3` currently assumes public or porous connectivity.
2. Define a one-way osmosis boundary compatible with the sovereign closed-core redesign.
3. Add quarantine, provenance screening, and toxic-pattern filtering as mandatory ingress constraints.
4. Preserve compatibility with the rest of the closed-core doctrine rather than inventing a parallel communication architecture.
