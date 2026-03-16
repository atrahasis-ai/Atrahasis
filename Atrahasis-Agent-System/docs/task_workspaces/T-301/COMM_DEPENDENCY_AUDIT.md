# T-301 Repo-Wide Communication Dependency Audit

## Executive Summary

This audit identifies where the repo still assumes the old communication model
`C4 ASV + A2A/MCP`, and converts that footprint into a dependency-safe retrofit
order for the Alternative B program.

Main finding:
- The old-stack dependency is concentrated in four places:
  1. the `C4` baseline itself
  2. cross-layer contracts that treat `ASV` as the canonical inter-layer message
     surface
  3. roadmap and implementation artifacts built around `asv-schema`,
     `MCP/A2A` adapters, and protocol-selection gates
  4. packaging and narrative artifacts that still describe Layer 1 as `ASV`

Practical consequence:
- `T-300` must define the supersession boundary before broad rewriting starts,
  once its own prerequisite chain exists.
- `T-302` is the first large retrofit pass across the stack.
- `T-304` and `T-305` cannot be done credibly until protocol and integration
  artifacts exist.
- `T-308` should be treated as cleanup after the real architectural rewrites,
  not as an early language-only sweep.

Non-finding:
- `C24` and `C33` do not currently show substantive `ASV + A2A/MCP` dependency in
  their live text. They still appear in later integration tasks because the new
  stack will add contracts, not because those specs currently need old-stack
  cleanup.

## Verified Constraints

- `T-200` is complete, so this audit is unblocked.
- `T-210` is not complete at audit time.
- Under the Dependency Safety Rules in `TODO.md`, this audit must not fabricate
  missing upstream protocol architecture.
- For `T-300+` work, `C4/ASV` remains required source material because it is the
  baseline being superseded.

## Method

1. Scanned canonical repo docs for `ASV`, `A2A`, `MCP`, and `Agent Card`.
2. Read the highest-hit canonical artifacts directly.
3. Separated:
   - normative dependency surfaces
   - roadmap/funding/package assumptions
   - reference-only or historical mentions
4. Derived retrofit ownership from the existing `TODO.md` dependency graph rather
   than inventing new task structure.

Excluded from patch-order inventory:
- prior-art research
- handoff files
- claim files
- completed-task archive rows
- historical invention logs unless they change current canonical wording

## Findings By Retrofit Tranche

### 1. T-300: C4 Supersession Boundary and Compatibility Policy

This is the first required rewrite boundary, not optional governance cleanup.

Why:
- The `C4` suite explicitly defines `ASV` as a JSON Schema vocabulary embedded in
  `Google A2A` and `Anthropic MCP`, and explicitly narrows scope away from a
  sovereign AACP direction.
- `UNIFIED_ARCHITECTURE.md` still presents Layer 1 as `ASV` and describes the
  stack in that frame.
- Several downstream specs still reference `C4` as the canonical vocabulary
  source, but not all of that surface should be retired. Some parts may remain as
  compatibility-only semantics or historical mapping guidance.

Artifacts that make `T-300` unavoidable:
- `docs/specifications/C4/MASTER_TECH_SPEC.md`
- `docs/specifications/C4/architecture.md`
- `docs/specifications/C4/technical_spec.md`
- `docs/specifications/UNIFIED_ARCHITECTURE.md`
- `docs/specifications/C9/MASTER_TECH_SPEC.md`
- `docs/specifications/C14/MASTER_TECH_SPEC.md`
- `docs/specifications/C17/MASTER_TECH_SPEC.md`

Output expectation:
- Define what survives from `C4` as compatibility semantics
- Define what is historical lineage only
- Define what must be replaced by `AACP v2 + extended AASL`

### 2. T-302: Cross-Layer Communication Retrofit Addendum

This is the first major technical rewrite pass.

Why:
- Current cross-layer specs still treat `ASV` as the canonical inter-layer message
  surface and, in several cases, assume the old A2A/MCP positioning implicitly.
- `T-302` is where those contracts are rewritten against the new `T-210/T-211/
  T-214/T-290` architecture rather than against the C4 baseline.

Primary `T-302` targets:
- `docs/specifications/C3/MASTER_TECH_SPEC.md`
- `docs/specifications/C5/MASTER_TECH_SPEC.md`
- `docs/specifications/C7/MASTER_TECH_SPEC.md`
- `docs/specifications/C8/MASTER_TECH_SPEC.md`
- `docs/specifications/C9/MASTER_TECH_SPEC.md`
- `docs/specifications/C23/MASTER_TECH_SPEC.md`
- `docs/specifications/C36/MASTER_TECH_SPEC.md`
- `docs/task_workspaces/T-067/specifications/MASTER_TECH_SPEC.md`

Secondary `T-302` adjacency:
- `docs/specifications/C14/MASTER_TECH_SPEC.md`
- `docs/specifications/C17/MASTER_TECH_SPEC.md`

Important nuance:
- `C24` is listed in later integration tasks, but this audit did not find live
  old-stack wording there. Its future patching is additive integration work, not
  old-stack cleanup.

### 3. T-303: Verification, Memory, and Provenance Retrofit

This tranche is narrower than `T-302` and should not be collapsed into it.

Why:
- Several specs depend on `ASV` not just as a message label, but as the
  provenance/trust surface used for verification, recovery, anomaly monitoring,
  and knowledge reconstruction.
- Alternative B adds native-vs-bridge provenance and new transport/security
  boundaries, so these contracts need a distinct trust-focused retrofit.

Primary `T-303` targets:
- `docs/specifications/C5/MASTER_TECH_SPEC.md`
- `docs/specifications/C6/MASTER_TECH_SPEC.md`
- `docs/specifications/C6/PATCH_ADDENDUM_v1.1.md`
- `docs/specifications/C34/MASTER_TECH_SPEC.md`
- `docs/specifications/C35/MASTER_TECH_SPEC.md`

### 4. T-304: Economics, Funding, and Cost Model Rewrite

This tranche is blocked until protocol and integration artifacts exist.

Why:
- `C22` still assumes `asv-schema` packages, `MCP/A2A` adapter prototypes, and a
  Wave 1 protocol-selection gate.
- `C8` still treats economic messages as `ASV` schemas.
- `C18` is lighter, but its external funding narrative still names the old
  six-layer stack with `ASV` at Layer 1.

Primary `T-304` targets:
- `docs/specifications/C8/MASTER_TECH_SPEC.md`
- `docs/specifications/C18/MASTER_TECH_SPEC.md`
- `docs/specifications/C22/MASTER_TECH_SPEC.md`

### 5. T-305: Implementation Plan and Wave Sequencing Rewrite

This is mostly a `C22` and packaging-plan rewrite, not a broad spec sweep.

Why:
- `C22` still builds the program around Wave 1 `ASV` infrastructure, `MCP/A2A`
  evaluation, `MCP` and `A2A` adapters, and JSON-Schema-first contract gates.
- `UNIFIED_ARCHITECTURE.md` still carries implementation and staffing language
  oriented around the old communication layer.

Primary `T-305` targets:
- `docs/specifications/C22/MASTER_TECH_SPEC.md`
- `docs/specifications/UNIFIED_ARCHITECTURE.md`

### 6. T-306: Interface and Developer Experience Retrofit

This tranche is centered on `EMA-I`.

Why:
- `C36` explicitly lists `REST`, `GraphQL`, `gRPC`, `WebSocket`, `MCP`, and `A2A`
  as transport bindings and treats agent-facing interaction as `C4 ASV` object
  flow.
- Once `T-260` and `T-280` exist, the interface layer needs to be re-described in
  native `AACP/AASL` terms rather than generic transport or bridge-era language.

Primary `T-306` target:
- `docs/specifications/C36/MASTER_TECH_SPEC.md`

### 7. T-307: Migration, Bridge, and Fallback Strategy

This tranche depends on the actual bridge artifacts, so it must stay late.

Why:
- The old stack is still the compatibility baseline.
- Migration policy cannot be written honestly until `T-250`, `T-251`, and
  `T-291` exist.
- The bridge/fallback narrative will need inputs from:
  - the `C4` baseline
  - `T-089` comparison findings
  - `C36` transport-binding tables
  - `C22` adapter/protocol-selection assumptions

### 8. T-308: Repo-Wide Terminology and Reference Sweep

This is a cleanup tranche, not an architectural one.

Why:
- Many low-severity artifacts still mention `ASV` in diagrams, glossaries,
  architecture summaries, or problem statements.
- Rewriting those early would only cause churn and risk conflicting with the real
  boundary decisions from `T-300` and `T-302`.

Likely `T-308` targets:
- `docs/SESSION_BRIEF.md`
- `docs/specifications/C3/MASTER_TECH_SPEC.md`
- `docs/specifications/C12/MASTER_TECH_SPEC.md`
- `docs/specifications/C14/MASTER_TECH_SPEC.md`
- `docs/specifications/C17/MASTER_TECH_SPEC.md`
- `docs/task_workspaces/T-063/specifications/MASTER_TECH_SPEC.md`
- `docs/task_workspaces/T-067/specifications/MASTER_TECH_SPEC.md`
- remaining intro/glossary references after substantive retrofits land

### 9. T-309: External Review Package Refresh

This is last by construction.

Why:
- External packaging must wait for the cost model, implementation plan, and
  terminology sweep to settle.
- The current public-facing architecture story still leans on old-stack wording in
  `UNIFIED_ARCHITECTURE`, `C22`, and portions of `C18`.

Likely `T-309` inputs:
- `docs/specifications/C18/MASTER_TECH_SPEC.md`
- `docs/specifications/C22/MASTER_TECH_SPEC.md`
- `docs/specifications/UNIFIED_ARCHITECTURE.md`
- the legacy external-review packaging scope formerly tracked as `T-011` (now folded into `T-309`)

## Dependency-Safe Patch Order

1. `T-300` first among retrofit tranches
   - reason: after `T-210` and this audit exist, define what `C4` still means
     before editing downstream references

2. `T-302` next
   - reason: after `T-300` and its listed protocol prerequisites exist, rewrite
     the actual cross-layer communication contracts

3. `T-303`
   - reason: after its own listed prerequisites and the `T-302` shape exist,
     trust/provenance boundaries can be rewritten without being diluted inside a
     broad stack addendum

4. `T-304` and `T-305`
   - reason: economics, funding, implementation waves, and staffing should be
     recomputed against real protocol/integration outputs, not speculative ones

5. `T-306`
   - reason: interface and developer experience wording depends on the new server,
     SDK, and tooling surfaces

6. `T-307`
   - reason: bridge retirement and fallback policy must wait for actual bridge
     specs and justification tests

7. `T-308`
   - reason: terminology cleanup should come after the architectural rewrites

8. `T-309`
   - reason: external packaging is the final synthesis layer

## Already Rebased / Not Immediate Retrofit Targets

These files are currently aligned enough that they do not belong in the early
patch order:
- `docs/TODO.md`
- `docs/SESSION_BRIEF.md`
- `docs/AGENT_STATE.md`
- `docs/DECISIONS.md`

They still contain deliberate historical-baseline language, but that language is
currently serving the authority boundary established by `ADR-041/ADR-042`, not
misstating the active program.

## Supporting Inputs (Not Patch Targets)

- `docs/task_workspaces/T-089/COMPARISON_ANALYSIS.md`
- `docs/task_workspaces/T-201/POLICY_DRAFT.md`

These are useful source inputs for migration and governance, but they are not
themselves retrofit targets in the canonical publication path.
