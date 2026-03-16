# C43 Feasibility Report: Custody-Bounded Semantic Bridge (CBSB)

**Invention:** C43 - Custody-Bounded Semantic Bridge (CBSB)
**Stage:** FEASIBILITY
**Date:** 2026-03-13
**Status:** COMPLETE
**Input Documents:** `docs/task_workspaces/T-250/IDEATION_COUNCIL_OUTPUT.yaml`, `docs/task_workspaces/T-250/IDEATION_COUNCIL_HYBRID_FOLLOWUP.yaml`, `docs/task_workspaces/T-250/PRIOR_ART_REPORT.md`, `docs/task_workspaces/T-250/LANDSCAPE_REPORT.md`, `docs/task_workspaces/T-250/SCIENCE_ASSESSMENT.md`

---

## 1. Refined Concept

CBSB refines `T-250` into six bounded but useful components:

1. **Signed Bridge Inventory Snapshots**
   - the bridge translates MCP tool inventories into signed bridge-scoped
     snapshots with explicit expiry, invalidation, and translation-policy
     identity

2. **Pinned Translation Context**
   - every translated invocation binds to one bridge snapshot, one translated
     tool identity, and one translation-policy hash rather than relying on
     ambient adapter behavior

3. **Source / Bridge Semantic Separation**
   - the bridge explicitly separates:
     - source-observed MCP facts,
     - bridge-normalized structure,
     - and bridge-inferred accountability semantics

4. **Accountable Bridged Results**
   - every bridge result becomes a distinct `tool_result` artifact with bounded
     `CLM + CNF + EVD + PRV` wrapping and explicit `BRIDGE_ENRICHED` or
     `BRIDGE_DEGRADED` posture

5. **Bounded Bridge State**
   - the bridge may keep reusable state for inventory caching and translation
     policy reuse, but that state remains visibly non-native and revocable

6. **Derated Continuation Handles**
   - the bridge may issue explicitly derated continuation handles for repeated
     or staged work, but those handles must not claim native `C42` execution
     priming or `C23` runtime authority

## 2. Why this is feasible

### 2.1 The upstream contracts already exist

- `C39` defines the tool-family message surfaces and bridge-visible
  `provenance_mode`
- `C40` defines bridge-limited trust, provenance floors, and anti-spoofing
  admission
- `C41` defines bridge posture disclosure in manifests
- `C42` defines the native target and makes native-versus-bridge distinction
  explicit

CBSB does not need to invent those primitives. It needs to compose them into a
generic bridge architecture.

### 2.2 The invention uses known building blocks

Research confirms the feasibility of:
- translation gateways,
- schema normalization,
- signed transformed state,
- bounded cache reuse,
- metadata enrichment,
- and explicit trust-ceiling disclosure.

### 2.3 The novelty is architectural, not speculative

The hard problem is not whether a bridge can translate tool calls. It is whether
that bridge can:
- remain universal,
- stay trust-honest,
- preserve semantic accountability,
- and still be useful enough for real migration.

That is difficult, but not scientifically doubtful.

### 2.4 The resulting design directly unblocks the backlog

- `T-260` gains a clear non-native counterpart to the native server framework
- `T-281` gains a concrete bridge conformance target
- `T-307` gains a credible migration and retirement policy anchor
- `T-303` and `T-290` gain explicit native-versus-bridge provenance inputs

## 3. Adversarial analysis summary

### Attack A - The bridge lies about native trust
- Risk: the translated endpoint appears equivalent to a native `C42` host
- Resolution: bridge posture remains explicit at manifest, invocation, result,
  and continuation surfaces; native equivalence is forbidden by default

### Attack B - The bridge invents semantics from raw MCP output
- Risk: confidence, evidence, or provenance are overstated relative to the
  source system
- Resolution: explicit source-observed vs bridge-inferred separation; degraded
  posture when the source lacks strong metadata

### Attack C - Zero per-server configuration fails in practice
- Risk: highly variable MCP servers require bespoke adapters, undermining the
  universal-bridge claim
- Resolution: specification must define a bounded generic translation profile
  plus explicit degraded/fail-closed behavior when a source server falls outside
  that profile

### Attack D - Bridge state becomes a shadow framework
- Risk: cached inventories, continuation handles, and warm state expand into a
  quasi-native runtime
- Resolution: bound bridge state to caching, translation reuse, and derated
  continuation only; no native priming or runtime lease semantics

### Attack E - Snapshot staleness causes invalid translated execution
- Risk: the bridge keeps serving outdated translated tool state
- Resolution: signed snapshot expiry, invalidation rules, and explicit failure
  semantics on stale or revoked source inventory

## 4. Assessment council

### Advocate

This is the strongest bridge direction because it preserves the migration value
of the MCP ecosystem without sacrificing the Alternative B integrity argument.
It turns the bridge into a visible custody boundary rather than a convenience
proxy.

### Skeptic

The design fails if:
- source-observed and bridge-inferred semantics are not clearly separated,
- the zero-config claim is oversold,
- or derated continuation handles drift into shadow native behavior.

### Arbiter verdict

**Decision: ADVANCE**

| Dimension | Score | Notes |
|---|---|---|
| Novelty | 4.0 / 5 | Strong bridge-specific composition, but built from known adapter primitives |
| Feasibility | 4.0 / 5 | Technically credible, with high integration and boundary-discipline cost |
| Impact | 5.0 / 5 | Foundational for migration, coexistence, conformance, and retrofit work |
| Risk | 6 / 10 | HIGH |

### Required actions for SPECIFICATION

1. Define the signed bridge snapshot structure and invalidation rules.
2. Define translation-policy identity and invocation pinning.
3. Define the source-observed / bridge-normalized / bridge-inferred separation
   model explicitly.
4. Define accountable bridged result wrapping and provenance-floor behavior.
5. Define the exact ceiling on bounded bridge state and derated continuation
   handles.
6. Define zero-config conformance boundaries and fail-closed behavior for
   non-conforming MCP servers.

---

**Stage Verdict:** ADVANCE to DESIGN
