# C43 - Custody-Bounded Semantic Bridge (CBSB)

## Master Technical Specification

| Field | Value |
|---|---|
| Title | Custody-Bounded Semantic Bridge (CBSB) |
| Version | 1.0.0 |
| Date | 2026-03-13 |
| Invention ID | C43 |
| Task ID | T-250 |
| System | Atrahasis Agent System v2.4 |
| Stage | SPECIFICATION |
| Normative References | ADR-041, ADR-042, C39 LCML, C40 DAAF, C41 LSCM, C42 LPEM, T-089 comparison analysis, T-301 dependency audit, Alternative B source packet |

---

## Table of Contents

1. System role and architectural position
2. Scope and non-goals
3. Governing inputs
4. Core innovation
5. Design principles
6. Object model
7. Protocol flows
8. Zero-configuration boundary
9. Cross-layer integration and downstream boundaries
10. Conformance profiles
11. Parameters
12. Formal requirements
13. Patent-style claims
14. Risks and open questions

---

## 1. System role and architectural position

### 1.1 Purpose

CBSB defines the canonical Alternative B migration bridge from `MCP` servers
into `AACP` endpoints. It exists to:
- preserve access to the existing MCP ecosystem during the migration period,
- translate non-native tool surfaces into coherent `AACP` tool flows,
- enrich results into bounded semantic accountability artifacts,
- and keep native-versus-bridge posture explicit at every stage.

### 1.2 The problem it solves

Before `C43`, the repo had:
- `C39` defining tool-family message classes and explicit `provenance_mode`,
- `C40` defining bridge-limited trust ceilings,
- `C41` defining manifest disclosure of bridge posture,
- `C42` defining the native tool target with signed snapshots and accountable
  results,
- but no canonical invention explaining how existing `MCP` servers could be
  admitted into the system without either:
  - collapsing into a thin dishonest proxy,
  - or pretending to be native `C42` tool hosts.

Without `C43`, downstream tasks would be forced to guess:
- how MCP tool inventories become bridge-scoped discovery state,
- how translated calls remain pinned to stable identity,
- how semantic enrichment stays bounded by source truth,
- how bridge-side reusable state is permitted or limited,
- and how non-native posture remains visible enough for policy and provenance
  consumers.

### 1.3 Architectural position

Under `C38`, CBSB primarily lives across L4 Messaging and L5 Semantics while
consuming `C40` security and targeting `C42` native tool semantics as the
compatibility horizon.

CBSB defines:
- signed bridge-scoped inventory snapshots,
- translation identity for bridged discovery and invocation,
- source-versus-bridge semantic separation,
- accountable bridged result composition,
- bounded bridge-side reusable state,
- and derated continuation posture.

CBSB does **not** define:
- a new transport binding,
- native tool authority semantics,
- runtime lease issuance,
- the long-term end-state architecture,
- or bespoke per-server bridge plugins as canonical behavior.

---

## 2. Scope and non-goals

### 2.1 In scope

- universal discovery translation from MCP tool inventories,
- translated invocation identity and policy pinning,
- accountable result enrichment with explicit bridge posture,
- bridge-scoped manifest disclosure,
- bounded snapshot cache and translation-state reuse,
- and optional derated continuation handles.

### 2.2 Out of scope

- native tool protocol semantics already owned by `C42`,
- runtime lease issuance owned by `C23`,
- native server-framework ergonomics owned by `T-260`,
- SDK API shape owned by `T-262`,
- A2A bridge semantics owned by `T-251`,
- and bridge retirement policy owned by `T-307`.

---

## 3. Governing inputs

CBSB is downstream of:
- `C39` for `tool_discovery`, `tool_invocation`, `tool_result`, and
  `tool_change_notification`,
- `C40` for `SP-BRIDGE-LIMITED`, provenance floors, and anti-spoofing
  admission,
- `C41` for manifest disclosure of bridge origin and posture,
- `C42` for the native target architecture that bridged tools must not
  impersonate,
- `T-089` for historical old-stack comparison context,
- and the Alternative B source packet for bridge-as-migration-scaffolding
  strategy.

CBSB must not contradict any of those authorities.

---

## 4. Core innovation

The invention is not merely "an MCP adapter exists." The invention is a
visibility-preserving bridge architecture that turns migration compatibility into
a signed custody boundary.

It does this through five linked moves:

1. **Signed translated inventory state**  
   the bridge emits bridge-scoped signed snapshots instead of treating cache
   state as an ungoverned implementation detail.

2. **Pinned translation identity**  
   every bridged invocation binds to one snapshot, one translated tool
   reference, and one translation policy identity.

3. **Semantic separation discipline**  
   source-observed MCP facts, bridge-normalized structure, and bridge-inferred
   accountability semantics remain explicit and distinguishable.

4. **Bounded accountable result wrapping**  
   bridged results enter the system as accountable semantic artifacts, but only
   under explicit `BRIDGE_ENRICHED` or `BRIDGE_DEGRADED` posture.

5. **Non-native reusable state with ceilings**  
   the bridge may retain bounded state for reuse and optionally issue derated
   continuation handles, but it must not claim native `C42` priming or `C23`
   execution authority.

---

## 5. Design principles

### 5.1 Bridge honesty first

Compatibility value never justifies hidden native-equivalence claims.

### 5.2 Snapshot before invocation

Translated invocation must be grounded in signed, reusable translated inventory
state rather than one-off ad hoc mapping.

### 5.3 Source before inference

Whenever the bridge adds semantics, it must preserve what the source actually
said and mark what the bridge inferred.

### 5.4 Zero-configuration is a profile, not a slogan

The bridge is universal only to the extent that it can operate from generic MCP
surfaces without bespoke per-server code. Anything else is out of profile and
must degrade or fail closed visibly.

### 5.5 State below authority

Bridge-side reusable state is allowed only if it stays below native framework,
runtime, and execution authority.

### 5.6 Migration, not masquerade

The bridge is scaffolding. Its contract should support coexistence and cutover,
not become a shadow end-state.

---

## 6. Object model

### 6.1 `BridgeInventorySnapshot`

`BridgeInventorySnapshot` is the signed bridge-scoped discovery artifact.

```text
BridgeInventorySnapshot := {
  bridge_snapshot_id,
  bridge_subject_ref,
  source_protocol,
  source_endpoint_ref,
  source_inventory_fingerprint,
  translated_tool_entries[],
  translation_policy_hash,
  produced_at,
  expires_at,
  invalidation_nonce,
  bridge_posture,
  provenance_floor,
  signature_ref
}
```

Semantics:
- `source_protocol` is fixed to the admitted MCP profile.
- `source_inventory_fingerprint` commits to the source inventory view the bridge
  observed.
- `translation_policy_hash` commits to the normalization logic used to mint the
  snapshot.
- `bridge_posture` and `provenance_floor` keep the snapshot visibly non-native.

### 6.2 `TranslatedToolEntry`

Each bridged tool appears as one translated bridge entry.

```text
TranslatedToolEntry := {
  translated_tool_ref,
  source_tool_ref,
  descriptor_projection_ref,
  input_mapping_profile,
  output_mapping_profile,
  capability_posture,
  degradation_flags[]
}
```

Semantics:
- `translated_tool_ref` is the stable AACP-facing identity.
- `source_tool_ref` remains visible for provenance and debugging.
- `degradation_flags[]` explain where source capability does not fully map into
  native `C42` expectations.

### 6.3 `BridgeTranslationContext`

Every translated invocation is bound to one context.

```text
BridgeTranslationContext := {
  translation_context_id,
  bridge_snapshot_id,
  translated_tool_ref,
  source_endpoint_ref,
  authority_context_ref,
  translation_policy_hash,
  source_capability_evidence[],
  accepted_response_channel?,
  requested_continuation_mode?
}
```

Semantics:
- invocations without a valid translation context are invalid,
- `translation_policy_hash` prevents silent mapping drift between discovery and
  invocation.

### 6.4 `SourceObservationRecord`

`SourceObservationRecord` captures source truth without semantic inflation.

```text
SourceObservationRecord := {
  observation_id,
  source_message_ref?,
  observed_fields[],
  observed_schema_refs[],
  observed_status,
  observed_at
}
```

### 6.5 `BridgeInferenceRecord`

`BridgeInferenceRecord` captures bridge-added semantic interpretation.

```text
BridgeInferenceRecord := {
  inference_id,
  parent_observation_id,
  inferred_semantic_fields[],
  inference_rule_refs[],
  confidence_floor
}
```

Semantics:
- bridge inference is explicit and reviewable,
- `confidence_floor` may only stay the same or degrade relative to what the
  source truth can support.

### 6.6 `BridgedAccountableResult`

`tool_result` for bridged execution is refined as:

```text
BridgedAccountableResult := {
  result_id,
  translation_context_id,
  source_observation_refs[],
  bridge_inference_refs[],
  claim_ref,
  confidence_ref,
  evidence_ref,
  provenance_ref,
  bridge_posture,
  semantic_separation_map,
  continuation_handle?
}
```

Semantics:
- `semantic_separation_map` identifies which fields come from the source, which
  are normalized, and which were inferred by the bridge.
- `bridge_posture` MUST remain non-native.

### 6.7 `BridgeContinuationHandle`

An optional derated continuation surface for repeat or staged work.

```text
BridgeContinuationHandle := {
  handle_id,
  parent_result_id,
  bridge_snapshot_id,
  authority_context_ref,
  translation_policy_hash,
  allowed_follow_on_ops[],
  expires_at,
  provenance_floor,
  handoff_class,
  native_equivalence
}
```

Rules:
- `handoff_class` is fixed to a non-native bridge class,
- `native_equivalence` is always `false`,
- the handle must never claim native execution priming.

---

## 7. Protocol flows

### 7.1 Discovery translation

1. Bridge obtains source MCP tool inventory.
2. Bridge computes `source_inventory_fingerprint`.
3. Bridge derives translated tool entries under one `translation_policy_hash`.
4. Bridge emits signed `BridgeInventorySnapshot`.
5. Consumers observe the bridged inventory through `tool_discovery`.

### 7.2 Invocation translation

1. Client sends `tool_invocation` against `translated_tool_ref`.
2. Bridge validates:
   - snapshot freshness,
   - translation policy identity,
   - authority context,
   - bridge posture limits.
3. Bridge maps the invocation into source MCP call form.
4. Source server executes.

### 7.3 Result enrichment

1. Bridge records raw source-observed material.
2. Bridge computes normalized structure.
3. Bridge emits explicit accountability semantics.
4. Bridge returns `tool_result` containing one `BridgedAccountableResult`.

### 7.4 Change notification and invalidation

If source inventory changes materially:
- the bridge invalidates affected snapshots,
- emits `tool_change_notification`,
- and rejects future invocations bound to invalid state unless a fresh snapshot
  has been adopted.

### 7.5 Error and degradation mapping

If the source server cannot satisfy required generic bridge assumptions:
- the bridge MUST either:
  - degrade explicitly with visible flags,
  - or fail closed.

The bridge MUST NOT hide capability loss behind fake native semantics.

### 7.6 Derated continuation flow

When profile and policy allow:
1. bridge returns a `BridgeContinuationHandle`,
2. handle remains bound to bridge snapshot and translation identity,
3. handle may support bounded follow-on operations only,
4. handle expires and invalidates independently,
5. handle never becomes native `C42` priming or `C23` authority.

---

## 8. Zero-configuration boundary

### 8.1 Meaning of zero-configuration

For CBSB, "zero per-server configuration" means:
- a conforming MCP server can be discovered and wrapped using only generic MCP
  capability surfaces and the canonical bridge translation profile,
- without bespoke server-specific mapping code as part of the canonical bridge
  conformance story.

### 8.2 What counts as out of profile

The bridge is out of profile when a source server requires:
- hidden server-specific field interpretation,
- bespoke adapter code to identify tools,
- non-standard tool payload assumptions that cannot be derived from generic MCP
  metadata,
- or custom trust semantics not expressible through bridge posture and
  degradation flags.

### 8.3 Out-of-profile behavior

Out-of-profile sources:
- MAY be wrapped by implementation-specific extensions,
- but such behavior is non-canonical,
- and MUST NOT count toward core bridge conformance.

---

## 9. Cross-layer integration and downstream boundaries

### 9.1 With `C39`

CBSB consumes the existing tool-family message classes and `provenance_mode`.
It does not add a bridge-only tool class.

### 9.2 With `C40`

CBSB consumes:
- `SP-BRIDGE-LIMITED`,
- provenance floors,
- anti-spoofing admission,
- and native-equivalence refusal.

### 9.3 With `C41`

Bridge manifests must disclose:
- bridge origin,
- bridge posture,
- supported translated tool capability surface,
- and any bounded continuation profile support.

### 9.4 With `C42`

CBSB targets the native tool contract but may not claim:
- native signed inventory authority,
- native accountable-result equivalence,
- or native execution priming.

### 9.5 With `C23`

CBSB does not mint runtime authority. Any bridge continuation handle remains
below `C23` lease authority.

### 9.6 With `T-260`

The native server framework must remain distinct from bridge behavior. CBSB is
for migration scaffolding, not the default native tool publication model.

### 9.7 With `T-281`

CBSB provides the canonical bridge conformance target:
- universal profile,
- degraded/fail-closed rules,
- and native-versus-bridge honesty conditions.

### 9.8 With `T-307`

CBSB gives migration planning a real boundary for:
- coexistence,
- cutover,
- retirement criteria,
- and residual bridge windows.

---

## 10. Conformance profiles

### 10.1 `CBSB-CORE`

Required support:
- signed bridge inventory snapshots,
- invocation pinned to snapshot/tool/policy identity,
- accountable bridged result wrapping,
- explicit bridge manifest disclosure,
- invalidation and fail-closed behavior.

### 10.2 `CBSB-WARM`

Adds:
- bounded snapshot cache reuse,
- translation-policy reuse,
- explicit warm-state revocation and expiry rules.

### 10.3 `CBSB-CONTINUATION`

Adds:
- derated continuation handles,
- handle expiry and invalidation,
- explicit non-native continuation ceilings.

---

## 11. Parameters

| Parameter | Default | Meaning |
|---|---:|---|
| `BRIDGE_SNAPSHOT_SIGNATURE_REQUIRED` | true | translated inventory snapshots must be signed |
| `BRIDGE_SNAPSHOT_MAX_TTL_SEC` | 300 | maximum safe reuse window before refresh |
| `BRIDGE_ZERO_CONFIG_CORE_REQUIRED` | true | conformance requires generic wrapping without bespoke per-server mapping |
| `BRIDGE_NATIVE_EQUIVALENCE_ALLOWED` | false | bridged outputs may not claim native equivalence by default |
| `BRIDGE_RESULT_ACCOUNTABILITY_REQUIRED` | true | every bridged result must emit accountability bundle |
| `BRIDGE_SEMANTIC_SEPARATION_REQUIRED` | true | source-observed vs bridge-inferred fields must remain explicit |
| `BRIDGE_DEGRADED_CONTINUATION_ALLOWED` | true | derated continuation handles are allowed by profile |
| `BRIDGE_CONTINUATION_MAX_TTL_SEC` | 300 | max lifetime for bridge continuation handles |
| `BRIDGE_INVALIDATION_FAIL_CLOSED` | true | stale or revoked bridge state must fail closed |
| `BRIDGE_OUT_OF_PROFILE_MODE` | `DEGRADE_OR_REJECT` | required response for non-generic source behavior |
| `BRIDGE_SOURCE_FINGERPRINT_REQUIRED` | true | source inventory must be fingerprinted |
| `BRIDGE_POLICY_HASH_REQUIRED` | true | translated invocation must pin to translation policy hash |

---

## 12. Formal requirements

1. **CBSB-R01** Every bridged `tool_discovery` response SHALL produce or reference a signed `BridgeInventorySnapshot`.
2. **CBSB-R02** Every `BridgeInventorySnapshot` SHALL include `bridge_snapshot_id`, `source_inventory_fingerprint`, `translation_policy_hash`, `produced_at`, `expires_at`, and `signature_ref`.
3. **CBSB-R03** Every bridged `tool_invocation` SHALL pin to one `bridge_snapshot_id`, one `translated_tool_ref`, and one `translation_policy_hash`.
4. **CBSB-R04** Bridged discovery and invocation SHALL preserve a visible mapping from `translated_tool_ref` to `source_tool_ref`.
5. **CBSB-R05** The bridge SHALL maintain an explicit distinction between source-observed MCP facts and bridge-inferred semantic assertions.
6. **CBSB-R06** Every bridged `tool_result` SHALL emit a `BridgedAccountableResult` with explicit bridge posture.
7. **CBSB-R07** Every `BridgedAccountableResult` SHALL include or reference `CLM`, `CNF`, `EVD`, and `PRV`.
8. **CBSB-R08** The bridge SHALL NOT claim a provenance floor stronger than the source system plus explicit bridge processing can support.
9. **CBSB-R09** Bridge-generated manifests and results SHALL remain visibly non-native and SHALL NOT silently satisfy native-only policy.
10. **CBSB-R10** Source inventory change or bridge snapshot expiry SHALL invalidate dependent translated state unless explicitly refreshed.
11. **CBSB-R11** Stale or invalid bridged invocation attempts SHALL fail closed.
12. **CBSB-R12** Core bridge conformance SHALL require generic wrapping from canonical MCP capability surfaces without bespoke per-server mapping.
13. **CBSB-R13** If a source server falls outside the generic bridge profile, the bridge SHALL degrade explicitly or reject the server; it SHALL NOT silently apply hidden custom logic and still claim core conformance.
14. **CBSB-R14** Bridge-side reusable state SHALL remain bounded to snapshot, translation, and explicit continuation support; it SHALL NOT become implicit ambient authority.
15. **CBSB-R15** Any `BridgeContinuationHandle` SHALL include `handle_id`, `bridge_snapshot_id`, `translation_policy_hash`, `expires_at`, and explicit non-native posture.
16. **CBSB-R16** A `BridgeContinuationHandle` SHALL NOT claim native `C42` priming.
17. **CBSB-R17** A `BridgeContinuationHandle` SHALL NOT by itself authorize `C23` runtime execution.
18. **CBSB-R18** Bridge posture SHALL be disclosed through `C41`-compatible manifest and capability signaling rather than hidden implementation state.
19. **CBSB-R19** Security-sensitive bridge publication or update flows SHALL remain subordinate to `C40` bridge-limited admission and anti-spoofing gates.
20. **CBSB-R20** The bridge SHALL preserve enough source reference material for downstream auditing, conformance review, and dispute resolution.
21. **CBSB-R21** A bridged result's semantic separation map SHALL allow downstream consumers to distinguish source-observed, bridge-normalized, and bridge-inferred fields without heuristic guessing.
22. **CBSB-R22** Out-of-profile source behavior SHALL remain policy-visible and SHALL NOT be relabeled as full universal bridge compatibility.
23. **CBSB-R23** Warm-state reuse in `CBSB-WARM` SHALL expire on snapshot invalidation, authority mismatch, or translation policy change.
24. **CBSB-R24** CBSB MUST remain migration scaffolding and SHALL NOT redefine the intended end-state architecture away from native AACP tool publication.

---

## 13. Patent-style claims

1. A protocol bridge in which translated tool inventory is materialized as signed bridge-scoped snapshot state, and bridged invocation is bound to both translated tool identity and translation-policy identity rather than to ambient adapter logic.
2. The bridge of claim 1, wherein bridged results carry an explicit separation between source-observed facts, bridge-normalized structure, and bridge-inferred accountability semantics.
3. The bridge of claim 1, wherein bounded reusable bridge state and continuation handles are permitted only under explicit non-native posture and are forbidden from claiming native-equivalent tool or runtime authority.
4. The bridge of claim 1, wherein universal bridge conformance is defined against generic source capability surfaces and explicitly excludes hidden bespoke per-source mapping from core compatibility claims.

---

## 14. Risks and open questions

### 14.1 Primary risks

| Risk | Description | Mitigation |
|---|---|---|
| False-native drift | bridge outputs are treated as native | explicit posture and trust ceiling |
| Semantic inflation | bridge invents stronger semantics than source supports | separation map and degraded posture |
| Snapshot drift | cached bridge state survives too long | signed expiry and invalidation |
| Hidden customization | universal bridge becomes bespoke adapter farm | explicit zero-config boundary |
| Shadow framework growth | bridge state expands into quasi-native runtime behavior | strict bound on state and continuation semantics |

### 14.2 Residual risk

Risk remains **HIGH** because the invention reaches across migration,
translation, trust, provenance, and operational reuse boundaries
simultaneously. That risk is acceptable because the design keeps one hard rule:
the bridge is useful only if it stays visibly non-native.

### 14.3 Open questions

1. What minimum MCP metadata set is truly sufficient for strong generic bridge
   conformance?
2. Should some bridge continuation handles be prohibited entirely for certain
   trust profiles or source server classes?
3. How should later tooling expose semantic separation maps so operators can
   debug bridge-generated results quickly?

---

*End of C43 Master Technical Specification v1.0.0*
