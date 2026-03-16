# T-250 Prior Art Report

## Scope

Evaluate prior art relevant to `C43` `Custody-Bounded Semantic Bridge (CBSB)`:
- universal protocol bridges from one tool ecosystem into another,
- translation of tool inventory and invocation semantics,
- semantic enrichment at the boundary,
- trust-preserving source-versus-adapter provenance separation,
- and bounded warm-state or continuation behavior inside a migration bridge.

This report uses repo-canonical and user-supplied primary sources only:
- Alternative B strategy packet,
- `T-089` communication comparison analysis,
- `C39` LCML,
- `C40` DAAF,
- `C41` LSCM,
- `C42` LPEM,
- and `T-301` retrofit/dependency audit.

No external web research was performed in this run.

## Primary comparison set

### 1. MCP list/call baseline

Source:
- Alternative B packet
- `docs/task_workspaces/T-089/COMPARISON_ANALYSIS.md`

Contribution:
- practical baseline for tool discovery and tool invocation through one
  interoperable ecosystem
- direct migration surface that `T-250` must wrap

Limitation:
- no native Atrahasis semantic accountability contract
- no signed bridge-scoped inventory snapshot concept
- no explicit source-versus-bridge provenance floor
- no lawful non-native continuation model tied to `C40` / `C42`

Relevance:
- direct system being wrapped

### 2. Generic protocol translation gateways

Source:
- broad known gateway pattern
- bounded by Alternative B bridge requirements

Contribution:
- method/field translation across protocol boundaries
- compatibility without re-implementing the source ecosystem

Limitation:
- translation alone is not a semantic trust model
- most gateways overstate equivalence between source and translated surfaces
- generic gateways do not define signed translated inventory state or
  accountability envelopes as first-class artifacts

Relevance:
- baseline non-novel pattern that `C43` must exceed

### 3. Schema-normalizing adapters

Source:
- broad known schema-adapter pattern
- `T-301` inventory of old-stack dependency surfaces

Contribution:
- one normalized interface can absorb many heterogeneous backends
- useful precedent for zero per-server configuration goals

Limitation:
- schema normalization does not define confidence, evidence, provenance, or
  trust ceilings
- a normalizer can easily hide where semantics were inferred rather than
  observed

Relevance:
- `C43` needs generic translation, but must go beyond syntax normalization

### 4. Metadata and observability shims

Source:
- broad known envelope-enrichment pattern
- Alternative B requirement for semantic enrichment

Contribution:
- add metadata, tracing, correlation identifiers, or audit tags around source
  operations

Limitation:
- most enrichment layers add operations metadata, not semantic accountability
- they rarely distinguish source-observed truth from adapter-inferred structure

Relevance:
- closest non-novel baseline for bridge-side enrichment behavior

### 5. Existing Atrahasis native substrate

Canonical repo sources:
- `C39` defines the bridge-visible message families and `provenance_mode`
- `C40` defines `SP-BRIDGE-LIMITED`, provenance floors, and anti-spoofing
  admission
- `C41` defines native-versus-bridge manifest disclosure
- `C42` defines signed native tool inventory snapshots, accountable results,
  and explicit native-versus-bridge posture for tool flows

Limitation:
- these authorities define the native target and trust boundaries, but not the
  universal migration bridge itself

Relevance:
- direct architectural lineage for `C43`

## What is not novel in C43

- protocol translation by itself
- inventory caching by itself
- schema normalization by itself
- result wrapping by itself
- adapter-side warm-state reuse by itself

## What is novel enough to justify C43

`C43` is justified only if it delivers an Atrahasis-specific composition that
mainstream bridge layers do not currently provide:

1. signed bridge-scoped inventory snapshots rather than ad hoc cache state,
2. invocation pinned to translated snapshot/tool identity and translation
   policy,
3. explicit separation between source-observed MCP facts, bridge-normalized
   structure, and bridge-inferred semantic assertions,
4. accountable result wrapping with explicit `BRIDGE_ENRICHED` or
   `BRIDGE_DEGRADED` posture,
5. and bounded non-native warm-state or continuation handles that never claim
   native `C42` priming or `C23` authority.

## Prior-art destruction attempts

### Claim: "This is just an MCP proxy"
- Rebuttal: a proxy does not define signed translated inventory state, explicit
  provenance-floor disclosure, or source-versus-bridge semantic separation.

### Claim: "This is just schema mapping plus wrappers"
- Rebuttal: schema mapping plus wrappers does not define custody-bound
  translation identity, bridge trust ceilings, or derated continuation posture.

### Claim: "This is just C42 for non-native tools"
- Rebuttal: `C42` is native tool authority. `C43` is specifically about how a
  non-native source can be admitted into the system without falsely inheriting
  native guarantees.

## Prior-art conclusion

`C43` has a real novelty claim if it stays focused on one architectural move:
make a migration bridge into a visible custody boundary with signed translated
state and explicit non-native semantic accountability, rather than a thin
compatibility facade or a fake native tool host.
