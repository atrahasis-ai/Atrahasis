# T-261 Swarm Proposal

- Task: `T-261`
- Title: `AACP Server Registry`
- Agent: `Nanshe (Codex)`
- Status: `CLAIMED`
- Date: `2026-03-13`

## Governing Inputs

- `C39` LCML discovery-family classes and manifest/query message contracts
- `C40` DAAF registry-vs-manifest trust rules and fail-closed admission
- `C41` LSCM manifest model and downstream `T-261` contract
- `C42` LPEM signed tool inventory snapshots and tool-surface reuse semantics
- `C45` ASCF native server framework as the primary producer surface
- `C47` Semantic Forge / Alternative C zero-bridge pivot

## State Note

The repo is not fully synchronized:
- `docs/TODO.md` and `docs/SESSION_BRIEF.md` still describe the Alternative B backlog.
- `docs/AGENT_STATE.md` and `docs/specifications/C47/MASTER_TECH_SPEC.md` introduce an Alternative C zero-bridge pivot.

This proposal resolves the mismatch by making `T-261` native-first:
- native AACP/C45 servers are first-class registry subjects,
- C47-forged probation/quarantine outputs are first-class but explicitly lifecycle-bounded,
- bridge-limited subjects, if retained at all, are compatibility-only and cannot satisfy native-only discovery or trust filters.

## Lead Architect

Define the registry as the canonical discovery and lookup surface for native AACP servers.

Baseline responsibilities:
- ingest signed `C41` manifests,
- validate them against `C40` registry truth,
- preserve immutable manifest snapshots and supersession lineage,
- materialize searchable capability projections from `C41`,
- ingest or dereference `C42` tool inventory snapshots for tool-level indexing,
- expose programmatic discovery APIs for subject lookup, capability search, and detail fetch.

Trust scoring should not be a single opaque reputation number. It should be a factorized registry trust vector derived from:
- native identity validity,
- manifest freshness and admission status,
- conformance/certification posture,
- provenance floor and verification posture,
- lifecycle state such as `PROBATION`, `ACTIVE`, `QUARANTINED`, or `REVOKED`.

## Visionary

Do not design a passive directory. Design a capability authority plane.

The registry should support discovery across:
- transport and encoding support,
- `C40` security profiles,
- `C39` message-family capability,
- `AASL` semantic surfaces,
- `C42` tool inventory traits,
- `C45` execution/sovereign-host traits,
- cost, provenance, and verification floors where policy-visible.

That turns `T-261` into the search-and-admission substrate for a sovereign native ecosystem rather than a static server list.

## Systems Thinker

Specify four tightly-bounded surfaces:

1. `NativeTrustRegistry`
   Stores native root anchors, rotation lineage, revocation, and lifecycle posture.

2. `ManifestRegistry`
   Stores immutable admitted `C41` manifests plus supersession edges and admission verdicts.

3. `CapabilityIndex`
   Search projection over messaging, semantics, bindings, security profiles, ontology snapshots, and discoverability tags.

4. `ToolIndex`
   Search projection over `C42` signed tool inventory snapshots, pinned to manifest and subject identity.

Programmatic discovery should expose:
- publish/update admission endpoints,
- manifest and subject query endpoints,
- capability/tool search endpoints,
- detail fetch endpoints,
- change-feed or snapshot export endpoints for caches and mirrors.

No new prerequisite task is required. `T-261` can consume `C41`, `C42`, `C45`, and `C47` directly.

## Critic

Non-negotiable constraints:
- ranking must never override fail-closed trust gates,
- manifest truth must never silently override `C40` registry truth,
- live telemetry and health cannot become canonical registry truth,
- bridge-derived or translated entries must remain visibly non-native,
- search tags must be projections from signed admitted artifacts, not free-form mutable metadata,
- stale manifests, revoked keys, or superseded identities must degrade or remove discoverability automatically.

## Final Proposal

Write `T-261` as a direct spec for a native-first AACP Server Registry with:
- immutable signed artifact ingestion,
- explicit registry-versus-manifest trust reconciliation,
- factorized trust vectors instead of opaque reputation,
- searchable manifest and tool capability indexes,
- programmatic discovery/query/update surfaces,
- explicit lifecycle handling for native, probationary, quarantined, and revoked subjects,
- compatibility-only handling for any surviving bridge-limited records under the Alternative C pivot.
