# C42 - Lease-Primed Execution Mesh (LPEM)

## Master Technical Specification

| Field | Value |
|---|---|
| Title | Lease-Primed Execution Mesh (LPEM) |
| Version | 1.0.0 |
| Date | 2026-03-13 |
| Invention ID | C42 |
| Task ID | T-240 |
| System | Atrahasis Agent System v2.4 |
| Stage | SPECIFICATION |
| Normative References | ADR-041, ADR-042, C23 SCR, C38 FSPA, C39 LCML, C40 DAAF, C41 LSCM, T-212 Type Extension Spec, T-213 Handshake/Session refinement, Alternative B source packet |

---

## Table of Contents

1. System role and architectural position
2. Scope and non-goals
3. Governing inputs
4. Core innovation
5. Design principles
6. Object model
7. Protocol flows
8. Warm-state reuse and execution priming
9. Cross-layer integration and downstream boundaries
10. Conformance profiles
11. Parameters
12. Formal requirements
13. Patent-style claims
14. Risks and open questions

---

## 1. System role and architectural position

### 1.1 Purpose

LPEM defines the canonical Alternative B tool-connectivity invention for native
`AACP`:
- discover tools through signed reusable inventory state,
- invoke tools against pinned semantic and authority context,
- return accountable results,
- optionally issue bounded continuation or execution-ready context,
- and hand runtime work to `C23` without ambient authority.

### 1.2 The problem it solves

Before `C42`, the repo had:
- `C39` defining tool message classes,
- `T-212` defining `TL{}` tool descriptors,
- `C40` defining capability grants and no ambient authority,
- `C41` defining manifest disclosure,
- `C23` defining lease-bound runtime execution,
- but no canonical invention saying how native tool invocation can become a
  high-performance, trust-preserving, execution-aware fabric.

Without `C42`, downstream tasks would be forced to guess:
- how discovery state is reused,
- how long-running or continuation-heavy tool work remains policy-visible,
- how execution priming differs from runtime authorization,
- how native and bridged tool flows stay distinguishable,
- and how high-speed tool use avoids cold-start overhead without sacrificing
  accountability.

### 1.3 Architectural position

Under `C38`, LPEM primarily lives in L4/L5 semantics while consuming `C40`
security and handing runtime work to `C23`.

LPEM defines:
- signed tool inventory snapshots,
- invocation priming levels,
- continuation-context structure,
- runtime handoff contract,
- accountable tool-result semantics,
- native-versus-bridge posture for those surfaces.

LPEM does **not** define:
- new transport bindings,
- new message classes beyond `C39`,
- new `TL{}` field meanings,
- `C23` runtime internals,
- manifest object structure,
- registry search/ranking behavior,
- the actual first-party tool library.

---

## 2. Scope and non-goals

### 2.1 In scope

- tool discovery snapshot structure and reuse semantics,
- invocation modes for immediate, continuation-ready, and execution-primed work,
- continuation-context validity semantics,
- runtime handoff payload needed by `C23`,
- mandatory accountable result wrapping,
- native-versus-bridge posture and trust ceilings,
- conformance targets for these behaviors.

### 2.2 Out of scope

- `T-243` stream carriage details,
- `C23` lease issuance internals,
- `T-260` framework ergonomics,
- `T-262` SDK API shape,
- `T-250` bridge translation mechanics,
- actual implementation of first-party tools,
- registry governance or marketplace behavior.

---

## 3. Governing inputs

LPEM is downstream of:
- `C38` for layer boundaries and canonical message identity,
- `C39` for `tool_discovery`, `tool_invocation`, `tool_result`, and
  `tool_change_notification`,
- `T-212` for `TL{}` descriptor fields,
- `C40` for authority contexts, capability grants, provenance floors, and no
  ambient authority,
- `C41` for manifest disclosure of tool capability surfaces,
- `C23` for lease-bound runtime execution and tool capability tokens.

LPEM must not contradict any of those authorities.

---

## 4. Core innovation

The invention is not merely "faster tool calls." The invention is a bounded
protocol composition that turns trusted tool invocation into the lawful start of
a governed execution fabric.

It does this through five linked moves:

1. **Signed discovery state**  
   Discovery returns reusable, signed tool inventory snapshots rather than
   forcing full rediscovery for every call.

2. **Pinned invocation context**  
   Invocation binds to snapshot identity, tool identity, canonicalized inputs,
   and explicit authority posture.

3. **Explicit priming levels**  
   Invocation can stay immediate, become continuation-ready, or become
   execution-primed for downstream runtime handoff.

4. **Bounded continuation contexts**  
   Follow-on work uses explicit expiring contexts rather than implicit session
   state or ambient authority.

5. **Lawful runtime handoff**  
   A primed context can carry the material a `C23` lease needs without becoming
   a lease by itself.

---

## 5. Design principles

### 5.1 Fast path first

Repeated tool use should avoid repeated cold discovery and cold trust setup when
the underlying authority state is still valid.

### 5.2 Priming is not execution

Execution-ready context may reduce future coordination, but it must never bypass
explicit `C23` lease issuance.

### 5.3 Trust survives speed

Snapshot reuse, warm state, and continuation are valid only under explicit
freshness, expiry, invalidation, and authority-matching rules.

### 5.4 Accountable results are mandatory

`tool_result` remains the accountable semantic artifact even when continuation
or execution priming is involved.

### 5.5 Cheap path preserved

Simple tools must still be able to use a bounded immediate path without
mandatory continuation or runtime-priming complexity.

### 5.6 Bridge honesty

Bridged and translated tool flows remain visible and policy-distinguishable from
native flows at every stage.

---

## 6. Object model

### 6.1 `ToolInventorySnapshot`

`ToolInventorySnapshot` is the reusable signed discovery artifact produced by
`tool_discovery`.

```text
ToolInventorySnapshot := {
  snapshot_id,
  subject_ref,
  inventory_hash,
  produced_at,
  expires_at,
  supersedes_snapshot_id?,
  trust_posture_ref,
  authority_floor,
  tool_entries[],
  signature_ref,
  invalidation_nonce
}
```

Semantics:
- `tool_entries[]` may inline `TL{}` objects or reference them.
- `inventory_hash` commits to the disclosed tool set.
- `expires_at` bounds safe reuse.
- `invalidation_nonce` lets later change notifications revoke the snapshot.

### 6.2 `PrimingLevel`

Every `tool_invocation_bundle` declares one of three priming levels:

- `IMMEDIATE_ONLY`
  - return only the bounded tool result
- `CONTINUATION_READY`
  - return a bounded continuation context for follow-on work
- `EXECUTION_PRIMED`
  - return continuation plus runtime-handoff material suitable for downstream
    `C23` lease derivation

### 6.3 `LeasePrimedInvocation`

The semantic payload of `tool_invocation_bundle` is refined as:

```text
LeasePrimedInvocation := {
  invocation_id,
  snapshot_id,
  tool_ref,
  input_schema_ref,
  canonical_input_hash,
  authority_context_ref,
  capability_grant_refs[],
  priming_level,
  continuation_ref?,
  session_ref?,
  desired_runtime_profile?,
  desired_operation_class?,
  stream_readiness_hint?
}
```

Semantics:
- `snapshot_id` pins the invocation to signed inventory state.
- `capability_grant_refs[]` are required when local policy or `C40` requires
  explicit grant handling.
- `continuation_ref?` is used when the invocation continues an earlier context.

### 6.4 `ContinuationContext`

`ContinuationContext` is the bounded follow-on context issued in a `tool_result`
when continuation or execution priming is granted.

```text
ContinuationContext := {
  context_id,
  parent_invocation_id,
  snapshot_id,
  tool_ref,
  authority_context_ref,
  capability_grant_refs[],
  policy_hash,
  provenance_floor,
  priming_level,
  allowed_follow_on_ops[],
  expires_at,
  session_binding?,
  stream_binding_hint?,
  bridge_posture,
  runtime_handoff_ref?
}
```

Semantics:
- a continuation context is explicit, expiring, and policy-bound,
- it is not a lease,
- it may be session-bound,
- it may be invalidated by snapshot supersession, grant expiry, or policy
  change.

### 6.5 `RuntimeHandoffContract`

`RuntimeHandoffContract` is the execution-facing payload that a primed context
may carry for `C23`.

```text
RuntimeHandoffContract := {
  handoff_id,
  context_id,
  tool_ref,
  operation_class_hint,
  runtime_profile_hint,
  required_cell_profile_floor,
  tool_token_template[],
  inference_policy_ref?,
  evidence_level,
  settlement_metering_class?,
  lease_binding_hash
}
```

Semantics:
- it is necessary input for runtime derivation,
- it is insufficient to authorize runtime work on its own,
- `lease_binding_hash` commits the handoff contract to the originating context.

### 6.6 `AccountableToolResult`

`tool_result_bundle` is refined to require accountable semantic wrapping:

```text
AccountableToolResult := {
  result_id,
  invocation_id,
  outcome,
  claim_ref,
  confidence_ref,
  evidence_ref,
  provenance_ref,
  continuation_context?,
  runtime_handoff?,
  native_posture,
  bridge_posture?
}
```

Semantics:
- `claim_ref`, `confidence_ref`, `evidence_ref`, and `provenance_ref` correspond
  to mandatory `CLM + CNF + EVD + PRV` surfaces,
- continuation and runtime handoff are adjuncts to the result, not replacements
  for it.

---

## 7. Protocol flows

### 7.1 Discovery and snapshot reuse

1. Client sends `tool_discovery`.
2. Server returns one signed `ToolInventorySnapshot`.
3. Client may cache the snapshot until:
   - `expires_at`,
   - an invalidating `tool_change_notification`,
   - authority-context mismatch,
   - or local policy revocation.

### 7.2 Immediate invocation

1. Client sends `tool_invocation` with `priming_level = IMMEDIATE_ONLY`.
2. Invocation references `snapshot_id`, `tool_ref`, and canonicalized input.
3. Server executes bounded tool work.
4. Server returns `tool_result` with accountable result only.

### 7.3 Continuation-ready invocation

1. Client sends `tool_invocation` with `priming_level = CONTINUATION_READY`.
2. Server returns accountable result plus `ContinuationContext`.
3. Later `tool_invocation` messages may reference `continuation_ref`.
4. If the context expires or is invalidated, follow-on work must fail closed.

### 7.4 Execution-primed invocation

1. Client sends `tool_invocation` with `priming_level = EXECUTION_PRIMED`.
2. Server evaluates whether policy allows priming.
3. Server returns accountable result plus:
   - `ContinuationContext`
   - and optional `RuntimeHandoffContract`
4. A downstream `C23` component may consume the handoff contract and issue an
   `ExecutionLease`.
5. No actual runtime execution may begin until that lease exists.

### 7.5 Change notification and invalidation

`tool_change_notification` may:
- add tools,
- update tools,
- revoke tools,
- or invalidate one or more snapshots.

If a snapshot or tool version is invalidated:
- future invocations using it must fail closed,
- continuation contexts bound to it must be rejected unless a policy-defined
  migration rule exists.

---

## 8. Warm-state reuse and execution priming

### 8.1 Warm-state reuse

LPEM allows warm-state optimization when:
- the session remains valid,
- the authority context still matches,
- referenced grants remain valid,
- the tool snapshot is still current,
- and local policy permits reuse.

Warm-state reuse may include:
- cached snapshot use,
- cached authority-context validation,
- reduced repeated negotiation for repeated invocations.

### 8.2 What warm-state reuse may not do

Warm-state reuse must not:
- silently survive authority-context change,
- survive grant expiry,
- survive snapshot invalidation,
- or imply runtime execution rights.

### 8.3 Execution priming

Execution priming is stronger than warm-state reuse:
- it lets a tool exchange return structured downstream execution context,
- but it still does not bypass `C23`.

Execution priming exists to reduce repeated coordination for complex tool
workflows, not to create a second runtime system.

---

## 9. Cross-layer integration and downstream boundaries

### 9.1 With `C39`

LPEM consumes the existing message classes and refines their semantic payloads.
It does not add a fifth tool message class.

### 9.2 With `C40`

LPEM consumes:
- authority contexts,
- capability grants,
- provenance floors,
- no-ambient-authority discipline.

Any primed or continuation context must remain subordinate to `C40`.

### 9.3 With `C41`

`C41` may advertise:
- supported priming levels,
- continuation support,
- native-versus-bridge posture,
- and relevant tool capability references.

`C41` does not absorb continuation or runtime handoff details.

### 9.4 With `T-243`

If a continuation needs streaming or push delivery:
- `C42` defines the need and references,
- `T-243` defines the actual carriage, ordering, and progress transport.

### 9.5 With `C23`

`C42` may prime runtime work, but:
- only `C23` can issue `ExecutionLease`,
- only `C23` can materialize tool tokens and active cells,
- `C42` handoff data must therefore remain necessary but insufficient.

### 9.6 With `T-250`

Bridge-derived contexts must remain visibly lower-trust or differently trusted
than native contexts unless downstream policy explicitly allows equivalence.

### 9.7 With `T-260`

The native server framework should expose:
- simple immediate invocations with minimal boilerplate,
- optional continuation support,
- optional execution priming hooks,
- and automatic accountable result wrapping.

### 9.8 With `T-262` and `T-290`

SDKs and cross-layer integration must treat:
- snapshot caching,
- context invalidation,
- continuation lifecycle,
- and runtime handoff
as first-class client/server concerns.

---

## 10. Conformance profiles

### 10.1 `LPEM-CORE`

Required support:
- signed inventory snapshots,
- immediate invocation,
- accountable results,
- invalidation handling.

### 10.2 `LPEM-CONTINUATION`

Adds:
- continuation contexts,
- follow-on invocation by `continuation_ref`,
- expiry and invalidation of continuation state.

### 10.3 `LPEM-PRIMED`

Adds:
- execution-primed invocation,
- runtime handoff contracts,
- policy-visible native-versus-bridge ceilings for primed contexts.

---

## 11. Parameters

| Parameter | Default | Meaning |
|---|---:|---|
| `SNAPSHOT_SIGNATURE_REQUIRED` | true | discovery snapshots must be signed |
| `SNAPSHOT_MAX_TTL_SEC` | 300 | maximum safe reuse window before refresh |
| `DEFAULT_PRIMING_LEVEL` | `IMMEDIATE_ONLY` | default invocation posture |
| `CONTINUATION_CONTEXT_MAX_TTL_SEC` | 900 | maximum continuation lifetime |
| `MAX_ACTIVE_CONTINUATIONS_PER_SESSION` | 16 | guardrail on continuation accumulation |
| `EXECUTION_PRIMING_REQUIRES_EXPLICIT_GRANT` | true | execution priming needs clear authority |
| `SESSION_REUSE_REQUIRES_AUTHORITY_MATCH` | true | warm reuse needs same authority context |
| `CHANGE_NOTIFICATION_INVALIDATES_BOUND_CONTEXTS` | true | snapshot invalidation cascades to contexts |
| `BRIDGE_EXECUTION_PRIMING_POLICY` | `DEGRADED_ONLY` | bridged priming must remain policy-distinct |
| `MANDATORY_RESULT_ACCOUNTABILITY` | true | every tool result must emit `CLM + CNF + EVD + PRV` |
| `RUNTIME_HANDOFF_REQUIRES_C23_LEASE` | true | priming never replaces lease issuance |
| `SIMPLE_PATH_MUST_REMAIN_AVAILABLE` | true | simple tools keep a cheap immediate path |

---

## 12. Formal requirements

1. **LPEM-R01** Every `tool_discovery` response SHALL produce or reference a signed `ToolInventorySnapshot`.
2. **LPEM-R02** Every `ToolInventorySnapshot` SHALL include `snapshot_id`, `inventory_hash`, `produced_at`, `expires_at`, and `signature_ref`.
3. **LPEM-R03** Every `tool_invocation` SHALL reference a specific `tool_ref` and the `snapshot_id` that justified it.
4. **LPEM-R04** Invocation input SHALL be canonicalized against the pinned input schema before execution-sensitive authorization is finalized.
5. **LPEM-R05** Every `tool_invocation` SHALL declare one `priming_level`.
6. **LPEM-R06** All conforming implementations SHALL support `IMMEDIATE_ONLY`.
7. **LPEM-R07** `CONTINUATION_READY` and `EXECUTION_PRIMED` MAY be profile-gated but, when supported, SHALL follow this specification's validity rules.
8. **LPEM-R08** Every `tool_result` SHALL remain distinct from `tool_invocation`.
9. **LPEM-R09** Every `tool_result` SHALL emit or reference `CLM`, `CNF`, `EVD`, and `PRV`.
10. **LPEM-R10** Any issued `ContinuationContext` SHALL include `context_id`, `parent_invocation_id`, `snapshot_id`, `authority_context_ref`, `policy_hash`, `provenance_floor`, and `expires_at`.
11. **LPEM-R11** A `ContinuationContext` SHALL fail closed on expiry, authority mismatch, grant invalidation, or snapshot invalidation.
12. **LPEM-R12** A continuation context SHALL NOT by itself authorize runtime execution.
13. **LPEM-R13** Any `RuntimeHandoffContract` SHALL be bound to one originating continuation context through `lease_binding_hash`.
14. **LPEM-R14** No active runtime work SHALL begin from a primed context unless a valid `C23` `ExecutionLease` has been issued.
15. **LPEM-R15** Warm-state reuse SHALL be valid only under matching session, security, authority, and snapshot-validity conditions.
16. **LPEM-R16** Warm-state reuse SHALL NOT survive grant expiry or authority-context change.
17. **LPEM-R17** `tool_change_notification` SHALL identify whether it invalidates tools, snapshots, or both.
18. **LPEM-R18** If a bound snapshot is invalidated, any dependent continuation context SHALL be rejected unless an explicit migration rule exists.
19. **LPEM-R19** Bridge-derived invocation, continuation, and priming surfaces SHALL remain explicitly policy-distinguishable from native surfaces.
20. **LPEM-R20** Bridge-derived primed contexts SHALL NOT claim a stronger provenance floor than the source system can support.
21. **LPEM-R21** If partial or progressive work is exposed before final completion, the exchange SHALL use an explicit continuation or downstream stream reference rather than smearing partial state into the final accountability bundle.
22. **LPEM-R22** Manifest disclosure of priming or continuation support SHALL occur through `C41`-compatible capability signaling rather than ad hoc hidden behavior.
23. **LPEM-R23** Execution priming SHALL require explicit authority posture sufficient for the downstream runtime policy being requested.
24. **LPEM-R24** Session-bound continuation contexts SHALL NOT survive into a new session unless explicitly re-authorized.
25. **LPEM-R25** The simple immediate path SHALL remain available even when advanced priming profiles are implemented.
26. **LPEM-R26** Server implementations SHALL expose clear failure reasons for invalidation, expiry, authority mismatch, and bridge-ceiling refusal.

---

## 13. Patent-style claims

1. A native tool-connectivity protocol in which tool discovery yields signed reusable inventory snapshots and tool invocation is bound to both a specific tool identity and a specific snapshot identity rather than to ambient endpoint state.
2. The protocol of claim 1, wherein a tool result may emit a bounded continuation context carrying authority, policy, provenance, and expiry bindings that permit future coordinated work without itself authorizing runtime execution.
3. The protocol of claim 1, wherein a tool result may emit a runtime handoff contract sufficient for a downstream runtime lease system to derive execution rights deterministically while preserving the rule that no runtime execution occurs without an explicit lease.
4. The protocol of claim 1, wherein native and bridged tool flows remain explicitly distinguishable across invocation, continuation, and execution-priming surfaces such that bridge-derived contexts cannot silently claim native-equivalent provenance or authority.

---

## 14. Risks and open questions

### 14.1 Primary risks

| Risk | Description | Mitigation |
|---|---|---|
| Shadow lease drift | primed contexts become de facto leases | explicit `C23`-only execution rule |
| Stale fast path | cached snapshots survive too long | signed expiry and invalidation |
| Warm-state authority leak | cached trust survives policy or grant change | strict authority/grant/session matching |
| Bridge confusion | translated contexts pretend to be native | explicit posture markers and policy ceilings |
| Advanced-path overdesign | simple tool cases become too expensive | preserve immediate path and profile-gate richer behavior |

### 14.2 Residual risk

Risk remains **HIGH** because the invention intentionally reaches across
tooling, security, session reuse, continuation, and runtime handoff surfaces.
That risk is acceptable because the design is still bounded by explicit
ownership lines:
- `C39` message classes remain fixed,
- `C40` remains security authority,
- `C23` remains runtime authority,
- and advanced behavior is expressed as explicit contexts rather than hidden
  ambient state.

### 14.3 Open questions

1. How aggressively should snapshot reuse be permitted across manifest
   supersession events when tool identity is stable but metadata changes?
2. Should bridge-derived continuation contexts ever be promotable to
   execution-primed contexts, or should that always require native revalidation?
3. What is the minimal runtime-handoff field set that lets `C23` derive leases
   deterministically without duplicating too much upstream state?

---

*End of C42 Master Technical Specification v1.0.0*
