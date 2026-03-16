# C42 Feasibility Report: Lease-Primed Execution Mesh (LPEM)

**Invention:** C42 - Lease-Primed Execution Mesh (LPEM)
**Stage:** FEASIBILITY
**Date:** 2026-03-13
**Status:** COMPLETE
**Input Documents:** `docs/task_workspaces/T-240/IDEATION_COUNCIL_OUTPUT.yaml`, `docs/task_workspaces/T-240/IDEATION_COUNCIL_HYBRID_FOLLOWUP.yaml`, `docs/task_workspaces/T-240/IDEATION_COUNCIL_PERFORMANCE_PRIORITIZED_FOLLOWUP.yaml`, `docs/task_workspaces/T-240/PRIOR_ART_REPORT.md`, `docs/task_workspaces/T-240/LANDSCAPE_REPORT.md`, `docs/task_workspaces/T-240/SCIENCE_ASSESSMENT.md`

---

## 1. Refined Concept

LPEM refines `T-240` into six bounded but powerful components:

1. **Signed Tool Inventory Snapshots**
   - discovery produces signed, reusable inventory state with explicit expiry,
     invalidation, and version binding,
   - invocations pin to snapshot identity rather than rediscovering tool state
     every time.

2. **Authority-Bound Invocation Context**
   - every invocation carries explicit authority posture from `C40`,
   - no warm channel, continuation, or primed execution context may become
     ambient authority.

3. **Lease-Primed Invocation**
   - a tool invocation may request more than an immediate result:
     - immediate bounded execution,
     - continuation-ready context,
     - or execution-ready priming for downstream `C23` handoff.

4. **Continuation Contexts**
   - tool results may return explicit continuation contexts bound to:
     - tool identity,
     - snapshot identity,
     - authority context,
     - policy hash,
     - provenance floor,
     - expiry,
     - and optional stream readiness.

5. **Runtime Handoff Contract**
   - a primed context does not itself execute runtime work,
   - it provides the lawful handoff material that a downstream `C23`
     `ExecutionLease` may consume without re-negotiating tool identity and trust
     from scratch.

6. **Deterministic Result Accountability**
   - every `tool_result` remains a distinct accountable artifact wrapped as
     `CLM + CNF + EVD + PRV`,
   - priming or continuation never replaces the accountable result boundary.

## 2. Why this is feasible

### 2.1 The upstream contracts already exist

- `C38` defines the layer boundary and canonical message identity.
- `C39` already defines the tool message classes.
- `T-212` already defines `TL{}`.
- `C40` already defines capability grants and no-ambient-authority expectations.
- `C41` already defines manifest disclosure of tool capability surfaces.
- `C23` already defines lease-bound execution and tool capability tokens.

LPEM does not need to invent these primitives from scratch. It needs to compose
them coherently.

### 2.2 The invention uses known building blocks

Research confirms the feasibility of:
- signed cacheable discovery state,
- long-lived multiplexed channels,
- progressive or partial-result protocol relationships,
- short-lived rotated workload identity,
- and lease-bound execution enforcement.

### 2.3 The novelty is integrative, not speculative

The hard problem is not whether the primitives work. It is whether they can be
combined without:
- creating ambient authority,
- losing provenance,
- or collapsing runtime ownership into the protocol layer.

That is a difficult architecture problem, but not a scientifically doubtful one.

### 2.4 The resulting design directly unblocks the backlog

- `T-243` gains a concrete continuation/stream handoff surface.
- `T-250` gains a target for native-vs-bridge execution posture.
- `T-260` gains a concrete native server/runtime interface target.
- `T-262` gains a clearer SDK surface for warm contexts and continuation-aware
  invocation.
- `T-290` gains a sharper integration seam into `C23`.

## 3. Adversarial analysis summary

### Attack A - Primed contexts become ambient authority
- Risk: once a context is minted, clients treat it like a standing permission
  rather than a bounded execution reference.
- Resolution: contexts remain explicitly bound to authority context, expiry,
  provenance floor, and policy hash; runtime work still requires a downstream
  `C23` lease.

### Attack B - Stale discovery or tool-version drift causes invalid execution
- Risk: invocations or continuations outlive the tool inventory state that
  originally justified them.
- Resolution: signed snapshots require expiry and invalidation; primed contexts
  bind to snapshot identity and fail closed when superseded or revoked.

### Attack C - T-240 silently steals C23 runtime ownership
- Risk: execution-ready contexts become de facto runtime leases.
- Resolution: `C42` defines handoff material only; actual execution remains
  impossible without `C23` lease issuance and tokenization.

### Attack D - Bridge traffic pretends to be native
- Risk: MCP-wrapped or translated tools reuse the same primed context semantics
  without visible degradation.
- Resolution: bridge posture remains explicit, provenance floors differ, and
  bridge/native capability ceilings are separable by policy.

### Attack E - The design over-optimizes advanced workflows and harms simple tools
- Risk: simple tools pay the price for high-consequence workflow machinery.
- Resolution: immediate bounded invocation remains the default path; continuation
  and execution-priming are requested explicitly rather than imposed universally.

## 4. Assessment council

### Advocate

This is the strongest tool invention direction because it upgrades AACP tool use
from "semantic RPC" to "governed execution fabric." It can materially reduce
repeated setup cost for serious tool workflows while preserving explicit trust
and provenance.

### Skeptic

The design fails if:
- continuation contexts become vague tokens with no hard validity model,
- the protocol takes over `C23`,
- or the common case becomes needlessly expensive compared with a simpler
  invocation/result path.

### Arbiter verdict

**Decision: ADVANCE**

| Dimension | Score | Notes |
|---|---|---|
| Novelty | 5.0 / 5 | Strongest Alternative B tool concept because it composes invocation and governed execution continuity |
| Feasibility | 4.0 / 5 | Known primitives, but high integration and boundary-management cost |
| Impact | 5.0 / 5 | Foundational for tools, bridges, runtime, SDKs, and first-party tool-suite planning |
| Risk | 7 / 10 | HIGH |

### Required actions for SPECIFICATION

1. Define signed inventory snapshot structure, expiry, and invalidation rules.
2. Define the invocation modes and priming levels explicitly.
3. Define continuation-context structure and validity semantics.
4. Define the `C23` runtime handoff contract without collapsing into runtime
   ownership.
5. Define native-versus-bridge provenance and capability ceilings clearly.
6. Define the minimum cheap path for simple tool invocations.

---

**Stage Verdict:** ADVANCE to DESIGN
