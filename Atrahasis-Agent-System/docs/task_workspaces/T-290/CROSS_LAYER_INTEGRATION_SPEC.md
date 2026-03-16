# T-290 - AACP v2 Cross-Layer Integration with Atrahasis Stack

## Cross-Layer Integration Specification

| Field | Value |
|---|---|
| Title | Atrahasis Cross-Layer Integration Profile |
| Profile ID | `AXIP-v1` |
| Task ID | `T-290` |
| Version | `1.0.0` |
| Date | `2026-03-13` |
| Stage | `DIRECT SPEC` |
| Normative references | `C38`, `C39`, `C40`, `C41`, `C42`, `C23`, `C24`, `C36`, `C3`, `C5`, `C6`, `C7`, `C8`, `T-301` |

---

## 1. Purpose and architectural position

### 1.1 Purpose

`AXIP-v1` defines how native `AACP v2 + AASL` integrates with the existing
Atrahasis stack.

It is the canonical contract for:

- which subsystems speak which `C39` business classes,
- which `C40` security profiles are acceptable on each surface,
- how `C41` manifest disclosure and `C42` tool/runtime posture enter the stack,
- how inter-habitat traffic is constrained by `C24`,
- how `C36` exposes the stack to external actors through native `AACP` ingress,
- and how additive protocol adoption proceeds before full legacy-spec retrofit.

### 1.2 The problem it solves

Alternative B already established:

- the five-layer native protocol architecture in `C38`,
- the canonical 42-class message inventory in `C39`,
- security posture and authority binding in `C40`,
- manifest disclosure in `C41`,
- and native tool/runtime handoff posture in `C42`.

The live stack still has a gap:

- `C5`, `C7`, `C8`, and other specs continue to treat `C4 ASV` as the canonical
  inter-layer message surface,
- `C24` and `C23` are ready for additive protocol integration but do not yet
  have a formal `AACP` contract,
- and the retrofit tasks identified by `T-301` need one agreed target before
  they begin rewriting legacy layer texts.

Without `T-290`, every downstream retrofit would be forced to guess:

- which LCML classes carry which layer interactions,
- when a layer may use native `AASL` objects versus internal layer-local
  payloads,
- how runtime evidence, settlement, verification, routing, and boundary ingress
  compose under one security and lineage model,
- and where additive integration stops and full semantic retrofit begins.

### 1.3 Architectural position

`AXIP-v1` sits below layer-owned semantics and above the individual bindings,
SDKs, frameworks, and retrofit tasks.

`AXIP-v1` defines:

- the native inter-layer communication spine,
- the canonical layer-to-message-class allocation,
- minimum security and provenance posture per surface,
- additive integration rules for legacy layer-owned payloads,
- routing and ingress boundaries.

`AXIP-v1` does **not** define:

- new transport bindings beyond `C38` and its transport refinements,
- new message classes beyond `C39`,
- new public `AASL` object-family admissions,
- the full semantic rewrite of the legacy `C3` / `C5` / `C7` / `C8` / `C36`
  texts,
- bridge retirement or supersession governance.

---

## 2. Scope and non-goals

### 2.1 In scope

- native service-to-service communication posture across the Atrahasis stack,
- external ingress posture through `C36`,
- inter-habitat routing posture through `C24`,
- `C39` class allocation for orchestration, verification, memory, runtime,
  settlement, and observability traffic,
- additive legacy-payload carriage rules during retrofit,
- rollout phases that separate spine adoption from semantic rewrite.

### 2.2 Out of scope

- direct edits to `C3`, `C5`, `C7`, `C8`, `C36`, and the other legacy specs,
- manifest schema redesign,
- framework ergonomics or SDK API shape,
- new ontology governance processes,
- external open-source or governance packaging.

---

## 3. Governing inputs

### 3.1 Upstream protocol authority

- `C38` defines layer ownership, canonical identity, session, and transport
  boundaries.
- `C39` defines the canonical 42-class business inventory.
- `C40` defines authority contexts, security profiles, grants, and replay
  posture.
- `C41` defines endpoint-scoped capability disclosure.
- `C42` defines tool discovery, invocation, accountable results, continuation,
  and runtime handoff posture.

### 3.2 Existing stack authority

- `C3` owns scheduling, tidal coordination, and epoch/ETR behavior.
- `C5` owns verification verdicts, trust posture, and credibility.
- `C6` owns memory admission and knowledge retrieval.
- `C7` owns intent decomposition and orchestration.
- `C8` owns settlement semantics.
- `C23` owns runtime lease issuance and execution evidence creation.
- `C24` owns habitat boundaries and inter-habitat exchange.
- `C36` owns the external membrane and receptor pipeline.

### 3.3 Retrofit authority

`T-301` is authoritative for the fact that `C3`, `C5`, `C7`, `C8`, and `C36`
still carry substantive `C4 ASV` communication dependencies in their live text.
`AXIP-v1` is the replacement target those downstream rewrites must consume.

---

## 4. Integration principles

### 4.1 Communication spine, not authority collapse

`AACP v2` becomes the canonical **native communication spine** for Atrahasis.
It does not collapse `C3`, `C5`, `C7`, `C8`, `C23`, `C24`, or `C36` into one
owner.

Layer ownership remains:

- `C3` schedules,
- `C5` verifies,
- `C7` orchestrates,
- `C8` settles,
- `C23` leases and runs,
- `C24` routes across habitats,
- `C36` mediates external ingress.

### 4.2 Native-first, retrofit-honest adoption

The stack adopts native `AACP` envelopes and security now, while legacy
layer-owned payload structures are rewritten later where necessary.

This avoids two failure modes:

- pretending the retrofit is already finished,
- or delaying native transport/session/security adoption until every semantic
  rewrite is complete.

### 4.3 Canonical identity and pinned semantics

Every native exchange is governed by the `C38` canonical identity chain:

- selected binding,
- selected encoding,
- `message_id`,
- `parent_message_id`,
- `conversation_id`,
- `workflow_id`,
- `registry_snapshot_id`,
- `payload_canonical_hash`,
- `message_canonical_hash`,
- provenance class.

The stack may not introduce layer-specific alternate identity models for the
same business exchange.

### 4.4 No ambient authority

All high-consequence surfaces are subordinate to `C40`:

- session establishment does not imply execution authority,
- transport reachability does not imply verification or settlement authority,
- runtime materialization requires explicit `lease_request` / `lease_grant`,
- bridge-limited posture never silently satisfies native-only policy.

### 4.5 Additive before destructive

`T-290` is additive integration work.

It explicitly allows:

- native `AACP` adoption at the spine,
- layer-local payload carriage on internal-only surfaces during transition,
- public native surfaces for already-admitted `AASL` object families.

It explicitly forbids:

- advertising unfinished legacy payloads as native public `AASL` families,
- heuristic unknown-type acceptance,
- bypassing `T-302+` rewrite work by treating temporary internal compatibility
  carriage as final architecture.

---

## 5. AXIP-v1 common profile

### 5.1 Session tuple

Every cross-layer native exchange under `AXIP-v1` uses one explicit session
tuple:

| Field | Meaning |
|---|---|
| `binding_id` | one of the `C38` native bindings |
| `encoding` | `AASL-B`, `AASL-J`, or `AASL-T` |
| `security_profile_id` | one `C40` profile accepted for the surface |
| `registry_snapshot_id` | pinned semantic registry snapshot |
| `authority_context_id` | authenticated context from `C40` |
| `manifest_ref` | endpoint-scoped `C41` disclosure reference when applicable |
| `provenance_class` | `NATIVE`, `BRIDGE_ENRICHED`, or `BRIDGE_DEGRADED` |

### 5.2 Surface posture classes

`AXIP-v1` distinguishes three communication postures:

| Posture | Allowed payload style | Manifest-advertisable? | Intended use |
|---|---|---|---|
| `PUBLIC_NATIVE` | admitted public `AASL` families only | Yes | external/native interoperability |
| `INTERNAL_NATIVE` | admitted public `AASL` families and layer-owned internal schemas where explicitly allowed | No unless the payload family is already admitted | service-to-service inside Atrahasis |
| `INTERNAL_LAYER_LOCAL` | layer-owned internal payload schema carried behind an LCML class during retrofit | No | temporary additive carriage pending rewrite |

Rule:

- a surface using `INTERNAL_LAYER_LOCAL` posture remains native in transport,
  session, lineage, and security terms,
- but the carried payload is not yet a public interoperable `AASL` family,
- and must not be published in `C41` manifests as if it were.

### 5.3 Endpoint roles

`AXIP-v1` defines these canonical endpoint roles:

| Role | Owning spec | Primary responsibility |
|---|---|---|
| `orchestrator` | `C7` | intent decomposition, task dispatch, workflow control |
| `scheduler` | `C3` | tidal schedule, surprise, version, ETR, topology/status |
| `verifier` | `C5` | claim verification, trust/credibility outcomes |
| `memory` | `C6` | retrieval, admission, memory-side commits |
| `settlement` | `C8` | settlement publication and economic state updates |
| `runtime` | `C23` | lease admission, execution state, evidence publication |
| `gateway` | `C24` | inter-habitat routing and custody enforcement |
| `membrane` | `C36` | boundary ingress/egress and receptor dispatch |
| `ops_observer` | `C33`, `C34`, `C35` | incident, recovery, and anomaly feeds |

### 5.4 Binding and encoding guidance

| Surface | Preferred binding | Preferred encoding | Rationale |
|---|---|---|---|
| in-habitat service-to-service | `AACP-gRPC` or `AACP-WS` | `AASL-B` | low-latency native binary carriage |
| boundary API ingress | `AACP-HTTP` | `AASL-J` or `AASL-T` | external interoperability and inspectability |
| operator or local tooling | `AACP-STDIO` or `AACP-HTTP` | `AASL-J` | local tooling, CLI, and development loops |
| inter-habitat gateway carriage | `AACP-gRPC` or `AACP-HTTP` | `AASL-B` preferred | custody-preserving gateway exchange |

### 5.5 Minimum security posture matrix

| Surface | Minimum profile | Notes |
|---|---|---|
| native inter-layer service traffic | `SP-NATIVE-ATTESTED` | default for `C3`, `C5`, `C6`, `C7`, `C8`, `C23`, `C24` |
| human/institution ingress through `C36` | `SP-FEDERATED-SESSION` | session-attested external boundary |
| workload/service ingress through `C36` | `SP-WORKLOAD-MTLS` | for service and provider systems |
| bridge/bootstrap surfaces | `SP-BRIDGE-LIMITED` | migration-only, never native-equivalent |

---

## 6. Layer-to-message-class allocation

### 6.1 Canonical allocation matrix

| Layer | Primary inbound / outbound LCML classes | Typical posture | Minimum profile | Notes |
|---|---|---|---|---|
| `C7` RIF | `task_submission`, `task_assignment`, `task_result`, `state_update`, `bundle_commit` | `INTERNAL_NATIVE` | `SP-NATIVE-ATTESTED` | orchestration and workflow lineage owner |
| `C3` Tidal | `TIDAL_SCHEDULE_ANNOUNCE`, `SURPRISE_DELTA`, `TIDAL_VERSION_PROPOSE`, `ETR_VOTE`, `state_update`, `signal_publish` | `INTERNAL_NATIVE` or `INTERNAL_LAYER_LOCAL` during retrofit | `SP-NATIVE-ATTESTED` | scheduling and control owner |
| `C5` PCVM | `claim_submit`, `verification_request`, `verification_result`, `attestation_submit`, `state_update` | `PUBLIC_NATIVE` or `INTERNAL_NATIVE` | `SP-NATIVE-ATTESTED` | claim and verdict authority |
| `C6` EMA | `memory_lookup_request`, `memory_lookup_result`, `memory_admission_request`, `memory_admission_result`, `bundle_commit` | `PUBLIC_NATIVE` or `INTERNAL_NATIVE` | `SP-NATIVE-ATTESTED` | retrieval and admission authority |
| `C8` DSF | `SETTLEMENT_PUBLISH`, `state_update`, `attestation_submit`, `error_report` | `INTERNAL_NATIVE` or `INTERNAL_LAYER_LOCAL` during retrofit | `SP-NATIVE-ATTESTED` | settlement authority |
| `C23` SCR | `lease_request`, `lease_grant`, `lease_deny`, `task_result`, `state_update`, `attestation_submit` | `INTERNAL_NATIVE` | `SP-NATIVE-ATTESTED` | runtime lease and evidence owner |
| `C24` FHF | any allowed class, route-preserving only | `INTERNAL_NATIVE` | `SP-NATIVE-ATTESTED` | custody, boundary, and habitat policy owner |
| `C36` EMA-I | discovery/tool/resource/prompt families plus `claim_submit`, `verification_request`, `task_submission` where receptor allows | `PUBLIC_NATIVE` | mixed by persona | boundary ingress owner |
| `C33` / `C34` / `C35` | `signal_publish`, `state_update`, `attestation_submit`, `error_report` | `INTERNAL_NATIVE` | `SP-NATIVE-ATTESTED` | operational observability surfaces |

### 6.2 Class ownership rule

The presence of an LCML class does not transfer domain ownership.

Examples:

- `verification_request` does not make `C39` the verification authority; `C5`
  remains the owner.
- `lease_grant` does not make `C39` the runtime authority; `C23` remains the
  owner.
- `SETTLEMENT_PUBLISH` does not make `C39` the settlement authority; `C8`
  remains the owner.

---

## 7. Layer-specific integration contracts

### 7.1 C7 RIF

`C7` is the primary workflow and orchestration producer.

`AXIP-v1` requires:

- root and child intent dispatch from `C7` to use `task_submission`,
- work acceptance and execution direction from downstream schedulers/runtimes to
  use `task_assignment`,
- execution completion, refusal, or terminal task outcome to use `task_result`,
- orchestration-state fanout to use `state_update`,
- multi-artifact workflow closure or commit-ready bundles to use `bundle_commit`.

Boundary rules:

- `C7` remains the owner of intent decomposition and success criteria.
- `C7` must stop treating `C4 ASV` as the canonical message envelope for these
  interactions once `T-302` rewrites the live spec.
- During additive phase adoption, any still-legacy intent payload schema may be
  carried only on `INTERNAL_LAYER_LOCAL` surfaces.

### 7.2 C3 Tidal Noosphere

`C3` owns schedule, version, surprise, and emergency-tidal control.

`AXIP-v1` maps:

- per-epoch schedule fanout to `TIDAL_SCHEDULE_ANNOUNCE`,
- surprise traffic to `SURPRISE_DELTA`,
- tidal-version proposals to `TIDAL_VERSION_PROPOSE`,
- emergency rollback voting traffic to `ETR_VOTE`,
- topology or scheduler health/status material to `state_update` or
  `signal_publish` depending on whether the payload is state-bearing or alert-like.

Compatibility rule:

- `C3` still contains legacy `TDF`, `TSK`, `SRP`, and `STL` payload definitions.
- Until `T-302` rewrites `C3` against Alternative B, those payloads may be
  carried only on `INTERNAL_LAYER_LOCAL` surfaces behind the correct `C39`
  message class.
- They must not be advertised through `C41` as public interoperable `AASL`
  families, and must not be used as a loophole around `T-201` / `T-212`
  registry-governance rules.

### 7.3 C5 PCVM

`C5` is the canonical verification authority.

`AXIP-v1` requires:

- claim intake to use `claim_submit` or `verification_request` depending on
  whether the producer is declaring a claim or asking for a verification act,
- verdict publication to use `verification_result`,
- signed process/evidence attestations to use `attestation_submit`,
- verification status and contest posture updates to use `state_update`.

Native semantic rule:

- the public native verification surface is built from admitted `CLM`, `CNF`,
  `EVD`, `PRV`, and `VRF` families.
- runtime evidence from `C23` is provenance input and process evidence; it is
  not a substitute verification verdict.

### 7.4 C6 EMA

`C6` owns retrieval and memory admission.

`AXIP-v1` maps:

- retrieval requests to `memory_lookup_request`,
- retrieval results to `memory_lookup_result`,
- admission requests to `memory_admission_request`,
- admission decisions or accepted memory material to
  `memory_admission_result`,
- memory-side commit boundaries to `bundle_commit`.

Boundary rule:

- `C6` may continue to maintain internal projection machinery during retrofit,
  but any native public memory surface must use admitted `AASL` families plus
  `C38` canonical identity.
- `C6` may not treat legacy `C4` projections as the final public interoperability
  contract once its rewrite begins.

### 7.5 C8 DSF

`C8` is the sole settlement authority.

`AXIP-v1` maps:

- epoch or settlement-window publication to `SETTLEMENT_PUBLISH`,
- ongoing economic state and budget posture to `state_update`,
- signed settlement proofs, conservation attestations, or audit-grade economic
  evidence to `attestation_submit`,
- settlement-path failures to `error_report`.

Compatibility rule:

- the live `C8` text still defines settlement messages as `C4 ASV` schemas.
- under `AXIP-v1`, those economic payloads move under native `AACP` carriage
  immediately, but the deeper object/schema retrofit remains downstream of
  `T-304`.

### 7.6 C23 SCR

`C23` owns runtime lease issuance and execution evidence.

`AXIP-v1` maps:

- runtime admission requests from orchestrators to `lease_request`,
- accepted runtime authority to `lease_grant`,
- rejected or deferred runtime authority to `lease_deny`,
- execution completion to `task_result`,
- runtime progress and capacity posture to `state_update`,
- sealed `Execution Evidence Bundle` digests and attested runtime evidence to
  `attestation_submit`.

Cross-authority rule:

- `task_result` is the execution-facing outcome visible to `C7`.
- `attestation_submit` is the evidence publication path into `C5` and `C8`.
- `lease_grant` and `lease_deny` remain necessary runtime-authority decisions;
  tool continuation or priming from `C42` never replaces them.

### 7.7 C24 FHF

`C24` does not own a separate business message family. It owns routing,
boundary, residency, and custody posture for any class crossing habitats.

`AXIP-v1` requires:

- habitat-local traffic to remain the default,
- inter-habitat exchange to occur only through `C24` boundary gateways,
- gateways to preserve `message_id`, lineage fields, selected encoding,
  `registry_snapshot_id`, and canonical hashes,
- routing metadata to remain transport-local and never rewrite semantic meaning,
- only policy-approved classes and payloads to traverse a habitat boundary.

The gateway may refuse a message. It may not normalize it into a different
semantic artifact.

### 7.8 C36 EMA-I

`C36` is the external membrane.

Under `AXIP-v1`, the membrane becomes the canonical native `AACP` ingress layer
for:

- manifest/discovery flows,
- tool/resource/prompt surfaces,
- claim and verification flows,
- operator and developer boundary flows that `C36` exposes,
- any task submission or query surface that a receptor permits.

Ordering rule:

1. `C40` session and authority posture are established.
2. `C36` binds the authenticated actor to the correct receptor family.
3. `C36` validates, authorizes, and dispatches to the owning subsystem.

`C36` must not invent a second incompatible transport model for native boundary
traffic once the retrofit occurs.

### 7.9 Rest of stack

The following additive contracts are required immediately even though the main
rewrite tasks arrive later:

| Surface | AXIP-v1 contract |
|---|---|
| `C32` MIA | native identity anchors and key lineage are consumed only through `C40`-compatible authority contexts and manifest chains |
| `C33` OINC | incident capsules and playbook requests ride `signal_publish`, `state_update`, and `attestation_submit`; OINC remains observe/escalate only |
| `C34` BSRF | recovery coordination traffic rides signed `state_update`, `signal_publish`, and `attestation_submit`; recovery does not mint a second message stack |
| `C35` Sentinel | anomaly outputs ride `signal_publish` and `state_update`; health or evidence-heavy anomaly reports may use `attestation_submit` |
| `C14` governance | governance surfaces remain downstream of boundary and retrofit work, but any native carriage must still honor `C40` profile floors and `C39` lineage rules |
| `C15` / `C18` economics and funding | they consume `C8` outputs and `C36` boundary surfaces rather than inventing competing economic transport semantics |
| `T-260` / `T-262` | framework and SDK work must expose the same role/class/security allocations defined here, not layer-specific alternatives |
| `T-281` | conformance must test the exact class allocations, profile floors, posture classes, and gateway preservation rules in this spec |

---

## 8. Semantic payload and compatibility rules

### 8.1 Public native rule

Any surface declared in a manifest for public interoperability:

- SHALL use only admitted public `AASL` object families,
- SHALL pin a registry snapshot,
- SHALL fail closed on unknown or ambiguous types,
- SHALL use the correct `C39` message class for the business act being
  performed.

### 8.2 Internal layer-local rule

A layer may temporarily carry an internal payload schema under a native LCML
class only when all of the following hold:

1. the surface is internal-only,
2. the binding, session, lineage, and security posture are fully native,
3. the payload is explicitly marked layer-local and not manifest-advertised as a
   public `AASL` family,
4. downstream retrofit ownership is already known,
5. the layer-local payload does not weaken `C40` or `C38` invariants.

### 8.3 Compatibility does not imply public semantics

Internal compatibility carriage is a transition mechanism, not proof that a
legacy payload family has become native.

It must not be used to:

- claim `T-302+` rewrite work is no longer needed,
- smuggle draft-era `C3` or `C8` payloads into public manifests,
- bypass the canonical registry-governance path for new types.

---

## 9. Routing, ingress, and provenance boundaries

### 9.1 Habitat routing

- intra-habitat traffic is the default and preferred mode,
- inter-habitat traffic requires explicit gateway policy,
- gateway refusal is fail-closed,
- gateway translation is prohibited unless a later migration policy explicitly
  authorizes it.

### 9.2 External ingress

All external native access flows through `C36`.

`C36` may expose different persona-specific receptor surfaces, but the native
wire protocol remains:

- `C38` transport/session,
- `C40` security,
- `C39` business classes,
- admitted `AASL` payload families,
- `C41`-declared capability posture.

### 9.3 Provenance

Every layer must preserve visible provenance posture:

- native remains native,
- layer-local internal compatibility remains visibly internal-only,
- bridge posture remains visible and policy-distinguishable,
- execution evidence remains distinct from verification verdicts,
- settlement publication remains distinct from verification and orchestration
  traffic even when they share the same native spine.

---

## 10. Adoption phases

### 10.1 Phase A - Native spine adoption

Immediate outcome:

- use `AACP` transport/session/security/message envelopes between major stack
  services,
- keep unfinished legacy payloads on internal-only surfaces where necessary,
- stop inventing new transport-local message models.

### 10.2 Phase B - Semantic retrofit

Owned by `T-302`, `T-303`, `T-304`, and related tasks:

- rewrite `C3`, `C5`, `C7`, `C8`, `C36`, and other affected specs against this
  profile,
- retire legacy `C4 ASV` inter-layer authority,
- replace temporary internal layer-local payloads with stable native semantic
  objects where needed.

### 10.3 Phase C - Public hardening and conformance

Owned by `T-281`, `T-306`, and ecosystem tasks:

- certify profile conformance,
- expose boundary and SDK behavior against one stable contract,
- eliminate any remaining accidental divergence between internal and public
  native surfaces.

---

## 11. Parameters

| Parameter | Meaning | Initial value |
|---|---|---|
| `AXIP_PROFILE_ID` | canonical integration profile identifier | `AXIP-v1` |
| `AXIP_DEFAULT_NATIVE_BINDING` | preferred in-cluster binding | `AACP-gRPC` |
| `AXIP_DEFAULT_NATIVE_ENCODING` | preferred in-cluster encoding | `AASL-B` |
| `AXIP_BOUNDARY_ENCODING_SET` | allowed boundary-friendly encodings | `AASL-J, AASL-T, AASL-B` |
| `AXIP_INTERNAL_LAYER_LOCAL_ALLOWED` | whether temporary internal layer-local payload carriage is allowed | `true` |
| `AXIP_INTERNAL_LAYER_LOCAL_MANIFESTABLE` | whether layer-local payloads may be manifest-advertised as public semantics | `false` |
| `AXIP_GATEWAY_MESSAGE_REWRITE_ALLOWED` | whether `C24` gateways may rewrite canonical message identity or lineage | `false` |
| `AXIP_RUNTIME_EVIDENCE_CLASS` | preferred class for sealed `C23` execution evidence publication | `attestation_submit` |
| `AXIP_DEFAULT_NATIVE_PROFILE` | default inter-layer security profile | `SP-NATIVE-ATTESTED` |
| `AXIP_BRIDGE_NATIVE_EQUIVALENCE_ALLOWED` | whether bridge-limited posture may satisfy native inter-layer policy | `false` |
| `AXIP_PUBLIC_UNKNOWN_TYPE_POLICY` | required behavior on unknown public types | `FAIL_CLOSED` |
| `AXIP_PHASE_B_OWNER_SET` | task family that owns the main retrofit rewrite | `T-302, T-303, T-304, T-306, T-307` |

---

## 12. Formal requirements

| ID | Requirement | Priority |
|---|---|---|
| AXIP-R01 | Native Atrahasis service-to-service communication SHALL use the `C38` / `C39` / `C40` spine rather than legacy `C4 ASV` message envelopes as final authority | P0 |
| AXIP-R02 | `AXIP-v1` SHALL NOT widen or replace the owning authority of `C3`, `C5`, `C6`, `C7`, `C8`, `C23`, `C24`, or `C36` | P0 |
| AXIP-R03 | Every native cross-layer exchange SHALL carry one explicit session tuple with binding, encoding, security profile, authority context, registry snapshot, and provenance posture | P0 |
| AXIP-R04 | Public manifest-advertised native surfaces SHALL use only admitted public `AASL` families and SHALL fail closed on unknown or ambiguous types | P0 |
| AXIP-R05 | Temporary layer-owned legacy payloads MAY be carried only on internal-only surfaces and SHALL NOT be advertised as public interoperable `AASL` families | P0 |
| AXIP-R06 | `C7` orchestration traffic SHALL use `task_submission`, `task_assignment`, `task_result`, `state_update`, and `bundle_commit` rather than layer-local ad hoc transport messages | P0 |
| AXIP-R07 | `C3` tidal traffic SHALL use `TIDAL_SCHEDULE_ANNOUNCE`, `SURPRISE_DELTA`, `TIDAL_VERSION_PROPOSE`, `ETR_VOTE`, `state_update`, and `signal_publish` as appropriate to the business act | P0 |
| AXIP-R08 | `C5` verification traffic SHALL use `claim_submit`, `verification_request`, `verification_result`, `attestation_submit`, and `state_update` with native claim/evidence/verdict semantics | P0 |
| AXIP-R09 | `C6` retrieval and admission traffic SHALL use the `memory_*` classes plus `bundle_commit` for memory-side commit boundaries | P0 |
| AXIP-R10 | `C8` settlement publication SHALL use `SETTLEMENT_PUBLISH`; settlement attestations and audit material SHALL use `attestation_submit` or `state_update` rather than a second settlement transport stack | P0 |
| AXIP-R11 | `C23` runtime authority SHALL be expressed through `lease_request`, `lease_grant`, and `lease_deny`; tool priming or continuation SHALL NOT bypass those runtime-authority decisions | P0 |
| AXIP-R12 | `C23` execution outcomes visible to `C7` SHALL be carried as `task_result`, while sealed execution evidence for `C5` and `C8` SHALL be published through `attestation_submit` | P1 |
| AXIP-R13 | `C24` gateways SHALL preserve lineage, canonical identity, selected encoding, registry snapshot, and provenance posture for any allowed inter-habitat traffic | P0 |
| AXIP-R14 | `C24` SHALL reject disallowed inter-habitat traffic rather than translating it into a different semantic artifact | P0 |
| AXIP-R15 | All external native stack ingress SHALL terminate through `C36` and SHALL NOT invent a parallel non-AACP native boundary protocol | P0 |
| AXIP-R16 | `C36` SHALL perform receptor binding and authorization after `C40` session establishment and before dispatch to any owning subsystem | P0 |
| AXIP-R17 | Native internal service traffic SHALL use `SP-NATIVE-ATTESTED` unless a stricter locally-owned rule applies | P0 |
| AXIP-R18 | `SP-BRIDGE-LIMITED` SHALL NOT satisfy native-only inter-layer policy under `AXIP-v1` | P0 |
| AXIP-R19 | Compatibility carriage of layer-local payloads SHALL NOT weaken `C38` canonical-hash, lineage, or registry-snapshot requirements | P0 |
| AXIP-R20 | Runtime evidence, verification verdicts, and settlement publications SHALL remain distinct artifact classes even when they traverse the same native transport/session/security spine | P1 |
| AXIP-R21 | The rest of stack surfaces (`C32`, `C33`, `C34`, `C35`, and downstream governance/economic consumers) SHALL consume this profile rather than inventing separate native message/posture rules | P1 |
| AXIP-R22 | Downstream retrofit tasks SHALL rewrite affected legacy specs against `AXIP-v1` instead of treating legacy `C4 ASV` message mappings as canonical going forward | P1 |

---

## 13. Conformance vectors

| Vector | Condition | Expected result |
|---|---|---|
| CV-1 Orchestration dispatch | `C7` sends work to `C3` and then `C23` | `task_submission`, `task_assignment`, `lease_request`, `lease_grant`, and `task_result` preserve one lineage chain with native security posture |
| CV-2 Verification flow | a claim is submitted and verified through native surfaces | `claim_submit` and `verification_result` carry admitted claim/evidence/verdict families under one pinned registry snapshot |
| CV-3 Runtime evidence split | `C23` completes work and emits evidence | `task_result` and `attestation_submit` remain distinct, with the latter consumed by `C5` / `C8` as evidence rather than verdict |
| CV-4 Inter-habitat preservation | an allowed native message crosses a habitat boundary | gateway preserves message identity, encoding, registry snapshot, and provenance posture exactly |
| CV-5 Boundary ingress ordering | an external caller enters through `C36` | `C40` session establishment occurs before receptor binding; receptor authorization occurs before dispatch |
| CV-6 Public type discipline | a manifest-declared public endpoint emits an unknown payload family | the exchange fails closed instead of silently treating the payload as native public `AASL` |
| CV-7 Layer-local compatibility discipline | a temporary layer-local `C3` payload is carried on an internal service path | the surface remains internal-only and is not manifest-advertised as a public semantic capability |
| CV-8 Settlement publication | `C8` emits a settlement boundary for an epoch | the publication uses `SETTLEMENT_PUBLISH` with native lineage and a separate attested proof path where needed |

---

## 14. Risks and open questions

### 14.1 Primary risks

| Risk | Severity | Mitigation |
|---|---|---|
| additive compatibility carriage becomes permanent | HIGH | explicit phase split and manifest prohibition on layer-local payloads |
| layer owners attempt to invent side-channel transports | HIGH | one native spine requirement plus conformance coverage |
| gateway implementations drift into semantic translators | HIGH | hard no-rewrite rule in `C24` |
| runtime evidence is mistaken for verification | MEDIUM-HIGH | distinct class/allocation rules between `task_result`, `attestation_submit`, and `verification_result` |
| public endpoints over-advertise unfinished semantics | MEDIUM-HIGH | fail-closed manifest and unknown-type posture |

### 14.2 Open questions

1. Which current layer-local payload families should be admitted first after
   the `T-302` rewrite begins: tidal control, settlement, or orchestration
   state?
2. Should `C24` standardize one preferred inter-habitat binding profile, or
   keep both `AACP-gRPC` and `AACP-HTTP` equally canonical at the gateway plane?
3. How much of the current `C36` receptor catalog should become public native
   manifest-declared capability versus remaining operator-private boundary
   surface?

---

## Conclusion

`AXIP-v1` gives Alternative B the missing stack-integration contract.

Its essential claim is simple:

Atrahasis can move to native `AACP v2 + AASL` without losing layer sovereignty
only if the stack shares one transport/session/security/message spine, one
lineage model, one public-type discipline, and one explicit boundary between
temporary compatibility carriage and final semantic retrofit.

That is the contract this specification establishes.
