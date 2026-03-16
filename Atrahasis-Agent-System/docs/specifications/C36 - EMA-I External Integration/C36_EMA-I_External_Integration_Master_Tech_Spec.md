# C36 - Epistemic Membrane Architecture for Interfaces (EMA-I)

## Master Technical Specification

**Version:** 1.1.0  
**Date:** 2026-03-14  
**Status:** APPROVED  
**Task:** T-064 Human and External Interface Layer; T-RENOVATE-006 Four-Membrane Isolation Rewrite  
**Agent:** Adapa (origin); renovated by Ninkasi  
**Document ID:** C36-MTS-v1.1

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Problem Statement](#2-problem-statement)
3. [Architecture Overview](#3-architecture-overview)
4. [Typed Interaction Receptors](#4-typed-interaction-receptors)
5. [Structured Translation Engine](#5-structured-translation-engine)
6. [Interaction Evidence Chain](#6-interaction-evidence-chain)
7. [Persona Projection Engine](#7-persona-projection-engine)
8. [Security Architecture](#8-security-architecture)
9. [Cross-Spec Integration Map](#9-cross-spec-integration-map)
10. [Transport Bindings](#10-transport-bindings)
11. [Deployment and Wave Integration](#11-deployment-and-wave-integration)
12. [Parameters](#12-parameters)
13. [Conformance Requirements](#13-conformance-requirements)
14. [Claims](#14-claims)
15. [Future Work](#15-future-work)
- [Appendix A: Session Type Formalism](#appendix-a-session-type-formalism)
- [Appendix B: Translation Galois Connection](#appendix-b-translation-galois-connection)
- [Appendix C: Persona Privilege Lattice Proof Sketch](#appendix-c-persona-privilege-lattice-proof-sketch)
- [Appendix D: Exemplar Receptor Definitions](#appendix-d-exemplar-receptor-definitions)
- [Appendix E: Evidence Record Schema](#appendix-e-evidence-record-schema)
- [Appendix F: Glossary](#appendix-f-glossary)

---

## 1. Introduction

The Atrahasis Agent System defines coordination, verification, knowledge metabolism, orchestration, settlement, identity, runtime execution, governance, economics, monitoring, and security. What it historically did not define well enough was the externalization boundary: how humans, counterparties, developers, public observers, enterprise systems, and native machine agents interact with the stack without collapsing the sovereignty model.

EMA-I fills that gap. It is not a generic API gateway. It is the canonical boundary architecture for all externally reachable interaction surfaces. It mediates, translates, evidences, projects, and rate-limits every external interaction.

Under the sovereignty pivot, EMA-I is not one flat ingress plane. It governs three externally reachable membranes:

- `Public` for accountability, notices, proofs, and bounded public artifacts
- `Enterprise` for tightly bounded derivative services and leased execution wrappers
- `Foundry` for petition intake, licensing operations, release-managed derivative delivery, and supervised external invention workflows

`Sanctum` is not externally reachable. It has zero direct receptors.

### 1.1 Scope

**In scope:**
- Typed interaction receptors with session-type discipline
- Four-membrane capability isolation: `Sanctum`, `Foundry`, `Enterprise`, `Public`
- Structured Translation Engine (deterministic, no natural-language admission path in v1.1)
- Interaction Evidence Chain with causal tracking
- Persona Projection Engine with non-interference guarantees
- Membrane-aware authentication, authorization, rate limiting, and bypass detection
- Transport bindings and compatibility posture
- Cross-spec integration for governance, commercialization, verification, runtime, and public accountability
- C22-aligned rollout sequencing

**Out of scope:**
- UI composition details
- Mobile-native UI families
- Natural-language interpretation as a primary control path
- Direct exposure of Sanctum capability
- Open public task marketplaces
- Unrestricted external invention APIs

### 1.2 Relationship to Other Specifications

EMA-I sits between the external world and the internal Atrahasis stack. It:

- **Consumes** C3 (osmosis boundary and epoch timing), C5 (verification surfaces), C6 (knowledge retrieval), C14 (governance taxonomy and release law), C15 (economics), C16 (outreach), C18 (Foundry and enterprise externalization policy), C22 (deployment sequence), C24 (habitat health), C32 (identity), C33 (incident response), C34 (recovery), C35 (membrane monitoring), C38/C39/T-290 (native communication semantics and carriage), C40 (trust anchors), and C45 (bounded service execution surface)
- **Produces** evidence records for C5, incident signals for C33, commercial bookkeeping intents for C8, membrane traffic signals for C35, and bounded externalization bundles for public and enterprise surfaces

### 1.3 Design Principles

1. **Sovereign boundary**: EMA-I has authority to deny, transform, rate-limit, and audit. It is never a passthrough proxy.
2. **Sanctum stays dark**: No external identity, transport, or SDK surface may bind directly to Sanctum capability.
3. **Membrane-typed externalization**: Every receptor belongs to exactly one externally reachable membrane: `PUBLIC`, `ENTERPRISE`, or `FOUNDRY`.
4. **Derivative-only exposure**: External users receive proofs, bounded services, supervised execution, or licensed derivative outcomes rather than raw access to recursion-critical machinery.
5. **Session-typed and evidence-first**: Every receptor is session-typed and every interaction yields an evidence record.
6. **Projection-consistent**: All persona views derive from frozen epoch state and satisfy non-interference.
7. **Native machine boundary**: Machine-facing receptors use native sovereign message and identity surfaces and may not silently satisfy inner-membrane trust policy through translated or legacy carriers.
8. **Transport subordinate to policy**: Transports implement the membrane policy; they do not define it.

---

## 2. Problem Statement

### 2.1 The Interface Gap

The Atrahasis stack defines deep internal mechanics, but it did not cleanly specify how users interact with those mechanics under the new sovereignty doctrine.

| User | Needs | Missing or Underspecified |
|------|-------|---------------------------|
| Human trustee | Vote on proposals, file tribunal cases, exercise emergency authority | Governance interfaces assumed by C14 but not architected |
| Foundry counterparty | Submit invention petitions, receive bounded status, report licensing milestones | C18 assumes commercialization but not the membrane |
| Enterprise customer | Invoke bounded derivative services, query usage, inspect service policy | Enterprise surface not separated from the core |
| Public observer | Inspect proofs, notices, approved artifacts, bounded system status | No canonical public accountability membrane |
| System operator | Query incidents, review anomalies, inspect recovery | Operations views assumed by C33/C34/C35 |
| Software developer | Validate schemas, generate SDKs, inspect receptor contracts | Tooling assumed by C22 and downstream specs |
| External AI agent | Submit claims, inspect verification status, invoke bounded machine surfaces | Agent-facing boundaries existed only implicitly |

### 2.2 Why a Generic API Gateway Is Insufficient

Generic gateways are insufficient because Atrahasis requires:

1. **Semantic translation** from human or machine inputs into epistemic operations rather than flat route dispatch.
2. **Capability membrane enforcement** between `Public`, `Enterprise`, `Foundry`, and the sealed `Sanctum`.
3. **Evidence-by-default** so interaction history is causal and auditable, not just access logging.
4. **Persona-specific projections** so the same system state can be rendered safely for trustees, operators, developers, the public, and machine clients.
5. **Epoch awareness** so external actions align with C3 timing and governance semantics.

---

## 3. Architecture Overview

### 3.1 Structural Position

```text
External Actors
      |
      v
+------------------------------------------------------+
| EMA-I Membrane Control Fabric                        |
|                                                      |
|  Public membrane      -> proofs, notices, docs       |
|  Enterprise membrane  -> bounded services            |
|  Foundry membrane     -> petitions, licensing        |
|                                                      |
|  Receptor Registry                                   |
|  Structured Translation Engine                       |
|  Interaction Evidence Chain                          |
|  Persona Projection Engine                           |
|  Auth/AuthZ/Rate/Compatibility Gates                 |
+------------------------------------------------------+
      |
      v
  Outer-surface owners: C14, C18, C5, C8, C33, C35, C45

  NO DIRECT RECEPTOR PATH
      |
      v
  Sanctum (sealed recursion-critical core)
  inward promotion only via C3 osmotic boundary
```

### 3.2 Request Lifecycle

Every external interaction follows this pipeline:

```text
1. RECEIVE       transport binding receives raw request
2. AUTHENTICATE  identity verified (OIDC, MIA, mTLS, service identity, or public posture)
3. CLASSIFY      target membrane determined
4. BIND          persona family determined, receptor matched
5. VALIDATE      session type checked against receptor definition
6. TRANSLATE     external representation converted to internal operation descriptor
7. AUTHORIZE     operation descriptor checked against persona permissions
8. MEMBRANE GATE crossing policy checked; direct Sanctum target fails closed
9. DISPATCH      operation sent to owning subsystem
10. RESPOND      internal result translated into membrane-bounded response
11. EVIDENCE     interaction evidence record generated asynchronously
12. EMIT         response delivered to caller
```

Critical invariants:

- Translation never confers authority.
- Membrane gating is independent of persona authorization.
- A request may be authenticated and still be denied for targeting the wrong membrane.
- No receptor chain may terminate in a direct Sanctum surface.

### 3.3 Four-Membrane Isolation Rules

| Membrane | Role | Admitted Actors | Allowed Exposure | Forbidden |
|----------|------|-----------------|------------------|-----------|
| `Sanctum` | Recursion-critical core, hidden novelty engine, self-improvement substrate | Native internal loci only | None through EMA-I | Any external receptor, bridged identity, raw model access, transport reachability |
| `Foundry` | Petition intake, supervised invention workflow, release-law review, licensing operations | Vetted counterparties, trustees, designated operators | Petition receipts, bounded status, derivative release packets, license reporting | General-purpose inference, raw traces, unscreened uploads into Sanctum |
| `Enterprise` | Bounded derivative service delivery and leased execution wrappers | Enterprise customers, attested agents, designated operators | Narrow service requests, usage reports, service policies, continuation handles | Open-ended invention requests, recursive tooling, unrestricted data-plane access |
| `Public` | Accountability, notices, approved research artifacts, proof surfaces | Public observers, developers, trustees, auditors | Proof bundles, release notes, public docs, bounded health and governance signals | Hidden-state introspection, privileged execution, raw novelty artifacts |

Any inward promotion from `Public`, `Enterprise`, or `Foundry` toward internal loci is governed by the C3 osmotic boundary and its quarantine rules. EMA-I may route toward that boundary, but may never bypass it.

---

## 4. Typed Interaction Receptors

### 4.1 Receptor Definition

A receptor is a session-typed interface point that mediates one class of external interaction.

```text
Receptor := {
  receptor_id      : URN
  persona_family   : PersonaFamily
  membrane_class   : MembraneClass   -- one of {PUBLIC, ENTERPRISE, FOUNDRY}
  session_type     : S
  signal_binding   : Schema
  operation_map    : OpDescriptor[]
  response_type    : Schema
  auth_level       : AuthLevel
  rate_policy      : RatePolicy
  release_profile  : ReleaseProfile
  version          : SemVer
  min_version      : SemVer
  evidence_class   : EvidenceClass
}
```

`SANCTUM` is not a legal `membrane_class` for any EMA-I receptor.

### 4.2 Persona Families

EMA-I organizes receptors by six persona families. Persona family and membrane class are related but distinct: the same membrane may expose different projections to different personas.

#### 4.2.1 Trustee Family

Consumers: trustees, tribunal members, constitutional officers, nominating bodies.

| Receptor | Membrane | Session Type Summary | Internal Target | Auth Level |
|----------|----------|---------------------|-----------------|------------|
| `governance_vote` | `PUBLIC` | Auth -> Proposal Context -> Cast Vote -> Receipt | C14 GTP -> C3 G-class | `TRUSTEE` |
| `constitutional_amendment` | `PUBLIC` | Auth -> Amendment Draft -> Review -> Ratification | C14 Constitution -> C3 G-class | `TRUSTEE_QUORUM` |
| `tribunal_filing` | `PUBLIC` | Auth -> Case Submission -> Evidence Attach -> Ack | C14 Tribunal | `TRUSTEE` |
| `emergency_authority` | `PUBLIC` | Auth -> Emergency Declaration -> Confirmation -> Activation | C14 Emergency -> C3 ETR | `TRUSTEE_SUPERMAJORITY` |
| `nominating_submission` | `PUBLIC` | Auth -> Candidate Package -> Validation -> Confirmation | C16 | `NOMINATING_BODY` |
| `cfr_query` | `PUBLIC` | Auth -> CFI Request -> CFI Report | C14 | `TRUSTEE` |

#### 4.2.2 Counterparty Family

Consumers: Foundry petitioners, licensees, enterprise customers, and other vetted commercial counterparties.

| Receptor | Membrane | Session Type Summary | Internal Target | Auth Level |
|----------|----------|---------------------|-----------------|------------|
| `foundry_petition` | `FOUNDRY` | Auth -> Petition Dossier -> Scope Review -> Intake Receipt | C18 Foundry desk -> C7 intake docket | `COUNTERPARTY` |
| `invention_status` | `FOUNDRY` | Auth -> Petition Ref -> Milestone Status -> Bounded Report | C18 Foundry pipeline | `COUNTERPARTY` |
| `license_report` | `FOUNDRY` | Auth -> License Ref -> Usage or Milestone Report -> Receipt | C18 licensing compliance -> C8 bookkeeping | `LICENSEE` |
| `counterparty_onboard` | `FOUNDRY` | Auth -> Credential and Ownership Package -> Vetting -> Activation | C18 -> C32/C40 | `COUNTERPARTY_NEW` |
| `enterprise_request` | `ENTERPRISE` | Auth -> Capability Selection -> Bounded Execution -> Response | C45 bounded service surface | `ENTERPRISE` |
| `enterprise_usage_query` | `ENTERPRISE` | Auth -> Period Selection -> Usage and Billing Report | C8 -> C18 bookkeeping | `ENTERPRISE` |

#### 4.2.3 Operator Family

Consumers: system operators, incident responders, habitat administrators.

| Receptor | Membrane | Session Type Summary | Internal Target | Auth Level |
|----------|----------|---------------------|-----------------|------------|
| `incident_query` | `FOUNDRY` | Auth -> Filter Criteria -> Capsule List -> Detail | C33 | `OPERATOR` |
| `playbook_trigger` | `FOUNDRY` | Auth -> Playbook Selection -> Parameters -> Status | C33 | `OPERATOR_SENIOR` |
| `recovery_status` | `FOUNDRY` | Auth -> Layer Selection -> Predicate Status -> Boot Progress | C34 | `OPERATOR` |
| `habitat_health` | `FOUNDRY` | Auth -> Habitat Selection -> Health Report | C24 | `OPERATOR` |
| `anomaly_review` | `FOUNDRY` | Auth -> Alert Selection -> Correlation Context -> Disposition | C35 | `OPERATOR` |
| `layer_status` | `FOUNDRY` | Auth -> Layer Selection -> Status Report | C3/C5/C6/C7/C8 | `OPERATOR` |

#### 4.2.4 Developer Family

Consumers: engineers, CI systems, contract-test runners, SDK consumers.

| Receptor | Membrane | Session Type Summary | Internal Target | Auth Level |
|----------|----------|---------------------|-----------------|------------|
| `schema_validate` | `ENTERPRISE` | Auth -> Native Semantic Object -> Validation Report | Native schema validator | `DEVELOPER` |
| `contract_test_run` | `ENTERPRISE` | Auth -> Test Suite Selection -> Results | C9 | `DEVELOPER` |
| `sdk_generate` | `ENTERPRISE` | Auth -> Language and Version -> SDK Package | Receptor Registry | `DEVELOPER` |
| `spec_query` | `PUBLIC` | Auth -> Spec ID -> Spec Content | Spec repository | `DEVELOPER` |
| `receptor_discover` | `PUBLIC` | Auth -> Persona Filter -> Receptor Catalog | Receptor Registry | `DEVELOPER` |
| `deployment_status` | `PUBLIC` | Auth -> Wave Selection -> Status Report | C22 | `DEVELOPER` |

#### 4.2.5 Public Family

Consumers: public observers, external auditors, researchers, review bodies.

| Receptor | Membrane | Session Type Summary | Internal Target | Auth Level |
|----------|----------|---------------------|-----------------|------------|
| `proof_query` | `PUBLIC` | Auth or Anon -> Predicate Selection -> Proof Bundle | C5 commitments; future C48 refinement | `PUBLIC` |
| `release_bundle_query` | `PUBLIC` | Auth or Anon -> Bundle Ref -> Approved Artifact Package | C18 release registry | `PUBLIC` |
| `governance_notice_query` | `PUBLIC` | Auth or Anon -> Notice Filter -> Governance or Policy Notice | C14 notice log | `PUBLIC` |
| `public_status_query` | `PUBLIC` | Auth or Anon -> Surface Selection -> Bounded Status Report | C22/C33 public projection | `PUBLIC` |

#### 4.2.6 Agent Family

Consumers: attested external agents and delegated outer-membrane agents.

| Receptor | Membrane | Session Type Summary | Internal Target | Auth Level |
|----------|----------|---------------------|-----------------|------------|
| `claim_submit` | `PUBLIC` | Auth -> Claim Object -> Submission Receipt | C5 | `AGENT` |
| `verification_query` | `PUBLIC` | Auth -> Claim Ref -> Verification Status | C5 | `AGENT` |
| `credibility_lookup` | `PUBLIC` | Auth -> Agent Ref -> Credibility Report | C5 | `AGENT` |
| `enterprise_capability_query` | `ENTERPRISE` | Auth -> Capability Ref -> Lease or Policy Surface | C45/C42 | `AGENT` |
| `bounded_knowledge_query` | `ENTERPRISE` | Auth -> Query Params -> Knowledge Results | C6 bounded projection | `AGENT` |
| `identity_register` | `PUBLIC` | Auth -> Registration Package -> AgentID and Receipt | C32 | `AGENT_NEW` |
| `epoch_query` | `PUBLIC` | Auth -> Epoch Ref -> Epoch Status and Timing | C3 | `AGENT` |

### 4.3 Receptor Registry

The receptor registry is the canonical machine-readable catalog of all active receptors.

**Registry operations:**
- `list(persona_family?) -> Receptor[]`
- `describe(receptor_id, version?) -> ReceptorDefinition`
- `negotiate(receptor_id, version_range) -> ReceptorVersion`
- `export(format) -> OpenAPI | GraphQL SDL | Proto3 | AACP Capability Manifest`

**Registry properties:**
- Receptor definitions are immutable once published
- Deprecated receptors continue to function until `min_version`
- Registry responses are membrane-filtered
- Registry itself is exposed through `receptor_discover`

### 4.4 Receptor Composition

Receptors may be composed when one receptor's output safely feeds another's input.

**Composition rules:**
- Only structured-path receptors are composable
- Output type of receptor A must be a subtype of receptor B's input type
- Authorization of a composed chain is the join of component authorizations
- Composition may only move outward or laterally across membranes
- No composed chain may terminate in a direct Sanctum target
- Evidence captures all intermediate results

**Composition is not supported for:**
- Cross-persona compositions that would escalate membrane privilege
- Receptors whose side effects mutate data consumed later in the same chain

---

## 5. Structured Translation Engine

### 5.1 Translation Model

The STE performs deterministic, bidirectional translation between external representations and internal operation descriptors.

For each receptor `R`, the STE defines:

- `alpha_R`: external input -> internal operation descriptor
- `gamma_R`: internal result -> membrane-bounded external response

`alpha_R` produces data, not authority. `gamma_R` applies release and membrane rules before emission.

### 5.2 Translation Categories

| Category | Direction | Example | Internal Target |
|----------|-----------|---------|-----------------|
| Governance -> G-class | Inbound | Trustee vote -> governance claim | C14/C3 |
| Petition -> Foundry docket | Inbound | Counterparty petition -> intake record | C18/C7 |
| License -> Bookkeeping | Inbound | License milestone report -> settlement intent | C18/C8 |
| Enterprise request -> Lease-bounded execution | Inbound | Service invocation -> bounded execution descriptor | C45/C42 |
| Public proof query -> Accountability bundle | Inbound | Proof predicate request -> proof descriptor | C5; future C48 |
| Claim -> Verification | Inbound | Agent claim assertion -> verification request | C5 |
| Knowledge -> Bounded retrieval | Inbound | Agent retrieval -> bounded knowledge query | C6 |
| State -> Projection | Outbound | Internal state -> persona-specific view | PPE |

### 5.3 Translation Residuals

If translation loses information, the lost content is captured in `translation_residual`. This supports auditability, redesign triage, and accountability review.

### 5.4 Translation Invariants

1. Soundness: every valid input yields a valid operation descriptor.
2. Type preservation: translated claim class matches receptor declaration.
3. Determinism: identical inputs yield identical outputs.
4. Residual completeness: output plus residual is auditably equivalent to original input.
5. Membrane preservation: translation may narrow capability, but may never widen membrane class.

---

## 6. Interaction Evidence Chain

### 6.1 Purpose

Every membrane interaction produces a causal evidence record. The chain exists for:

1. audit,
2. verification feed,
3. incident correlation,
4. accountability publication and release governance.

### 6.2 Evidence Record Structure

```json
{
  "evidence_id": "uuid-v7",
  "timestamp": "2026-03-14T18:45:12.123456789Z",
  "tidal_epoch": "epoch-42157",
  "receptor_id": "urn:atrahasis:receptor:counterparty:foundry_petition:v1.1",
  "persona": "Counterparty",
  "membrane_class": "FOUNDRY",
  "actor_id": "sha256:...",
  "input_hash": "sha256:...",
  "translation_result": { "op_type": "FOUNDRY_PETITION", "claim_class": null },
  "translation_residual": { "lost_fields": [], "residual_size_bytes": 0 },
  "internal_ops_triggered": ["op:c18:foundry:intake:42157-001"],
  "response_hash": "sha256:...",
  "prev_evidence_hash": "sha256:...",
  "evidence_hash": "sha256:...",
  "evidence_class": "SIGNIFICANT",
  "retention_days": 365
}
```

### 6.3 Evidence Classification

| Class | Trigger | Retention | PCVM Commit | OINC Forward |
|-------|---------|-----------|-------------|--------------|
| `ROUTINE` | Public status query, developer spec query, agent epoch query | P-10 | No | No |
| `SIGNIFICANT` | Foundry petition, agent claim submission, enterprise request | P-11 | Yes (batch) | No |
| `HIGH_CONSEQUENCE` | Governance vote, license milestone settlement, operator playbook trigger | P-12 | Yes (immediate) | Yes |
| `EMERGENCY` | Membrane bypass detection, emergency authority, release-law breach | P-13 | Yes (immediate) | Yes |

### 6.4 Evidence Chain Integrity

- Records are append-only and hash-chained
- Periodic commitments are made to C5 at interval P-02
- Evidence is partitioned by epoch and membrane for efficient review

### 6.5 Causal Tracking

`internal_ops_triggered` contains causal effects only. Temporal correlation alone is insufficient.

### 6.6 Asynchronous Generation

Evidence generation is write-behind, but commits must complete before the epoch boundary. Recovery reconstructs missing evidence from dispatch logs if necessary.

---

## 7. Persona Projection Engine

### 7.1 Projection Function

```text
Projection(P, M, E) :=
  state(E)
  |> authorize(P, M)
  |> transform(P.rendering_rules, M.release_profile)
  |> format(P.output_format)
```

Each projection is a pure function of state, persona, membrane, and epoch.

### 7.2 Epoch Binding

Projections are computed against frozen epoch state. Intra-epoch live views may include explicitly marked speculative sections for operator use.

### 7.3 Non-Interference

The privilege lattice is:

```text
          Trustee
         /       \
    Operator   Developer
       |          |
  Counterparty   Agent
        \        /
           Public
```

For any `P_low <= P_high`, changes visible only at `P_high` must not alter `P_low` projections.

### 7.4 Per-Persona Rendering

| Persona | Rendering Rules | Language Register |
|---------|-----------------|-------------------|
| Trustee | Governance decisions, CFI trends, tribunal status, emergency posture | Legal and constitutional |
| Counterparty | Petition status, license obligations, bounded commercial reports | Commercial and contractual |
| Operator | Incident severity, layer health, recovery posture, anomaly context | Operational and technical |
| Developer | Contract tests, schemas, receptor contracts, deployment snapshots | Engineering |
| Public | Proof bundles, release notices, bounded status summaries | Accountability and public review |
| Agent | Typed machine objects, verification states, capability descriptors | Structured machine format |

### 7.5 Projection Computation Strategy

- Precompute operator and public status projections at epoch boundaries
- Compute trustee and counterparty projections lazily
- Support delta refresh for monotone public and enterprise surfaces
- Require full recomputation for non-monotone governance surfaces

---

## 8. Security Architecture

### 8.1 Authentication

| Actor Type | Method | Identity Binding |
|-----------|--------|-----------------|
| Human trustee or operator | OAuth 2.1 / OIDC with institutional role binding | Trustee or Operator persona |
| Institutional counterparty | OIDC/SAML plus optional mTLS | Counterparty persona |
| Enterprise workload | SP-NATIVE-ATTESTED workload identity plus contract-bound service identity | Counterparty or Agent persona |
| Native agent | C32 MIA AgentID and signature chain under SP-NATIVE-ATTESTED | Agent persona |
| Native delegated agent | C32 MIA AgentID plus bounded native grant | Agent persona |
| Public observer | Anonymous or low-trust authenticated posture | Public persona |
| CI system | Native service account plus sovereign signing profile | Developer persona |

Authentication always occurs before receptor binding and translation.

### 8.2 Authorization Model

Authorization operates at three levels:

1. persona-level admission,
2. receptor-level minimum auth,
3. operation-level grant check.

Membrane gating is a fourth, independent level. A valid identity does not imply a valid membrane crossing.

### 8.3 Rate Limiting

Rate limits apply per persona, per receptor, per actor, and per membrane. Public surfaces are rate-limited aggressively for abuse control; Foundry surfaces are rate-limited for intake quality; enterprise surfaces are rate-limited for contractual fairness and cost control.

### 8.4 Membrane Completeness and Sanctum Darkness

All external interactions must pass through an EMA-I receptor. Direct access to internal components is prohibited.

Additional hard rules:

- `SANCTUM_DIRECT_RECEPTOR_COUNT` is fixed at zero.
- Native machine transports may terminate only on explicitly declared `PUBLIC` or `ENTERPRISE` receptors.
- Any attempt to present a translated or non-native machine identity as Sanctum-equivalent is an emergency event.
- C35 monitors for membrane bypass, shadow ingress, and quarantine escape patterns.

### 8.5 Receptor Version Security

- Receptors declare `version` and `min_version`
- Downgrade attempts are logged
- Version lag is bounded by P-09

---

## 9. Cross-Spec Integration Map

### 9.1 Inbound: External to Internal via EMA-I

| Persona | Receptor | Target Spec | Target Operation | Membrane |
|---------|----------|-------------|------------------|----------|
| Trustee | `governance_vote` | C14 -> C3 | Governance decision | `PUBLIC` |
| Trustee | `emergency_authority` | C14 -> C3 | Emergency activation | `PUBLIC` |
| Counterparty | `foundry_petition` | C18 -> C7 | Intake docket creation | `FOUNDRY` |
| Counterparty | `license_report` | C18 -> C8 | License bookkeeping intent | `FOUNDRY` |
| Counterparty | `enterprise_request` | C45 | Bounded service invocation | `ENTERPRISE` |
| Operator | `incident_query` | C33 | Capsule retrieval | `FOUNDRY` |
| Operator | `recovery_status` | C34 | Predicate status query | `FOUNDRY` |
| Developer | `contract_test_run` | C9 | Contract execution | `ENTERPRISE` |
| Public | `proof_query` | C5 | Accountability proof retrieval | `PUBLIC` |
| Agent | `claim_submit` | C5 | Claim submission | `PUBLIC` |
| Agent | `bounded_knowledge_query` | C6 | Bounded knowledge retrieval | `ENTERPRISE` |

### 9.2 Outbound: Internal to External via EMA-I

| Source Spec | Integration | Target Surface |
|-------------|-------------|----------------|
| C5 | Evidence commitments and proof bundles | Public accountability |
| C33 | Incident evidence and bounded notices | Operator and public status surfaces |
| C8 | Bookkeeping responses for Foundry and enterprise commercial flows | Counterparty surfaces |
| C35 | Membrane traffic patterns and bypass alerts | Operator surfaces |
| C18 | Release-governed derivative bundles and petition status | Foundry and enterprise surfaces |
| C45 | Lease-bounded execution results | Enterprise surfaces |

### 9.3 Contract Bindings

Every integration point must define:

- preconditions,
- postconditions,
- invariants,
- membrane class,
- release profile,
- evidence consequence.

---

## 10. Transport Bindings

### 10.1 Supported Transports

| Transport | Primary Use | Generation Source | Notes |
|-----------|-------------|-------------------|-------|
| REST/HTTP 2 | Public and enterprise request-response | OpenAPI 3.1 | Default human and service transport |
| GraphQL | Privileged projection queries | GraphQL SDL | Developer and operator views |
| gRPC | High-performance enterprise and machine calls | Proto3 | Enterprise and agent surfaces |
| WebSocket or SSE | Status and event feeds | Registry-generated channel schemas | Public and operator updates |
| AACP-native binding | Native machine interaction | Capability manifest | Preferred machine surface |

### 10.2 Transport Invariant

All transports route through the same receptor pipeline. Transport logic handles serialization and connection management only.

### 10.3 Transport Posture

- Native machine traffic uses the sovereign Alternative C stack and its canonical manifests.
- Legacy translated carriers are not part of the forward EMA-I transport posture.
- No machine transport may reach Foundry licensing control paths or any Sanctum-adjacent surface without passing the declared receptor pipeline.

### 10.4 Schema Generation

The registry generates transport-specific schemas and SDKs:

- `sdk_generate("typescript", "v1.1")`
- `sdk_generate("python", "v1.1")`
- `sdk_generate("rust", "v1.1")`

Generated SDKs must preserve session-type ordering and membrane metadata.

---

## 11. Deployment and Wave Integration

### 11.1 C22 Sequence Mapping

EMA-I follows the renovated C22 sequence: `Sanctum + Foundry -> Enterprise -> Public`.

| Sequence Stage | EMA-I Focus | Receptors | Dependencies |
|----------------|------------|-----------|--------------|
| `W0/W1 bootstrap` | Public governance plus Foundry intake and operator control | Trustee, Operator, Foundry Counterparty receptors | C14, C18, C33, C34, C35, C40 |
| `W1/W2 parallel Sanctum+Foundry` | No Sanctum receptors; inward routing only via C3 boundary | Membrane gate, evidence, Foundry workflow | C3, C18, C40 |
| `W2/W3 enterprise expansion` | Bounded derivative service surfaces | Enterprise Counterparty, Agent, Developer enterprise receptors | C45, C42, C8 |
| `W3/W4 public accountability expansion` | Public proof and bounded status surfaces | Public receptors | C5, C14, future C48 alignment |
| `W4/W5 hardening` | Full non-interference proof, native transport hardening, complete evidence commitments | All receptors | C5, C35, C40 |

### 11.2 Maturity Tiers

| Tier | Coverage | Evidence |
|------|----------|---------|
| `Stub` | Registry, governance, and operator minimum surfaces | Foundry intake and public governance functional |
| `Functional` | Foundry and enterprise surfaces with evidence chain | Petition and enterprise request paths work end-to-end |
| `Hardened` | Public proof surfaces, native transport gates, membrane monitoring | All outer interactions run through membrane with evidence |
| `Production` | Formal non-interference, release-law enforcement, zero direct Sanctum exposure | Full membrane guarantees operational |

---

## 12. Parameters

| ID | Parameter | Default | Range | Governor |
|----|-----------|---------|-------|----------|
| P-01 | MAX_RECEPTOR_COMPOSITION_DEPTH | 3 | 1-10 | Stiftung Board |
| P-02 | EVIDENCE_CHAIN_COMMIT_INTERVAL | 100 records | 10-1000 | Operations |
| P-03 | PROJECTION_CACHE_TTL | 3600s | 60-7200 | Operations |
| P-04 | RATE_LIMIT_TRUSTEE_RPM | 60 | 10-300 | Stiftung Board |
| P-05 | RATE_LIMIT_COUNTERPARTY_RPM | 120 | 20-1000 | Operations |
| P-06 | RATE_LIMIT_OPERATOR_RPM | 300 | 60-1500 | Operations |
| P-07 | RATE_LIMIT_DEVELOPER_RPM | 1200 | 300-6000 | Operations |
| P-08 | RATE_LIMIT_AGENT_RPM | 6000 | 1000-30000 | Operations |
| P-09 | MIN_RECEPTOR_VERSION_LAG | 2 major versions | 1-5 | Stiftung Board |
| P-10 | EVIDENCE_RETENTION_ROUTINE | 90 days | 30-365 | Stiftung Board |
| P-11 | EVIDENCE_RETENTION_SIGNIFICANT | 365 days | 180-730 | Stiftung Board |
| P-12 | EVIDENCE_RETENTION_HIGH_CONSEQUENCE | 2555 days | 1095-perpetual | Stiftung Board |
| P-13 | EVIDENCE_RETENTION_EMERGENCY | perpetual | perpetual | Constitutional |
| P-14 | PROJECTION_STALENESS_MAX | 3600s | 60-36000 | Operations |
| P-15 | PCVM_COMMIT_THRESHOLD | SIGNIFICANT | ROUTINE-EMERGENCY | Stiftung Board |
| P-16 | MEMBRANE_BYPASS_ALERT_THRESHOLD | 1 event | 1-10 | Constitutional |
| P-17 | SANCTUM_DIRECT_RECEPTOR_COUNT | 0 | fixed at 0 | Constitutional |
| P-18 | BRIDGE_MEMBRANE_SCOPE | PUBLIC and ENTERPRISE only | fixed enum | Constitutional |
| P-19 | PUBLIC_PROOF_BUNDLE_MAX_BYTES | 256 KB | 16 KB-10 MB | Operations |
| P-20 | FOUNDRY_INTAKE_DOSSIER_MAX_BYTES | 10 MB | 256 KB-200 MB | Foundry Office |

---

## 13. Conformance Requirements

### 13.1 Receptor Requirements

| ID | Requirement | Verification |
|----|-------------|-------------|
| REQ-01 | Every receptor MUST have a unique versioned URN | Registry validation |
| REQ-02 | Every receptor MUST declare a session type | Type checker |
| REQ-03 | Every receptor MUST belong to exactly one persona family | Registry validation |
| REQ-04 | Every receptor MUST belong to exactly one membrane class | Registry validation |
| REQ-05 | `SANCTUM` MUST NOT be a valid membrane class for any EMA-I receptor | Static validation |
| REQ-06 | Every receptor MUST declare input and response schemas | Schema validation |
| REQ-07 | Registry export MUST support OpenAPI, GraphQL, Proto3, and capability manifests | Export validation |

### 13.2 Translation Requirements

| ID | Requirement | Verification |
|----|-------------|-------------|
| REQ-08 | STE abstraction MUST produce valid internal operation descriptors | Property test |
| REQ-09 | Translation MUST preserve declared claim class and membrane class | Property test |
| REQ-10 | Translation MUST be deterministic | Property test |
| REQ-11 | Translation residuals MUST be captured when information is lost | Property test |
| REQ-12 | Translation MUST NOT confer authority | Architecture review |
| REQ-13 | Translation MUST NOT widen membrane scope | Property test |

### 13.3 Evidence Requirements

| ID | Requirement | Verification |
|----|-------------|-------------|
| REQ-14 | Every membrane interaction MUST generate an evidence record | Integration test |
| REQ-15 | Evidence records MUST include membrane class and causal links | Causal completeness test |
| REQ-16 | Evidence chain MUST be hash-chained | Chain integrity test |
| REQ-17 | Records above `PCVM_COMMIT_THRESHOLD` MUST be committed to C5 | C5 integration test |

### 13.4 Projection Requirements

| ID | Requirement | Verification |
|----|-------------|-------------|
| REQ-18 | Projection computation MUST be a pure function of state, persona, membrane, and epoch | Architecture review |
| REQ-19 | Projections MUST satisfy non-interference across the privilege lattice | Formal proof |
| REQ-20 | Public projections MUST exclude hidden-state and recursion-critical content | Projection test |
| REQ-21 | Enterprise projections MUST expose only bounded derivative capability | Service-surface review |
| REQ-22 | Foundry projections MUST exclude raw novelty-engine internals | Release-law review |

### 13.5 Security Requirements

| ID | Requirement | Verification |
|----|-------------|-------------|
| REQ-23 | Authentication MUST occur before receptor binding and translation | Pipeline ordering test |
| REQ-24 | Authorization MUST be independent of translation | Architecture review |
| REQ-25 | Membrane gating MUST be enforced independently of persona authorization | Integration test |
| REQ-26 | All external interactions MUST pass through an EMA-I receptor | Network audit |
| REQ-27 | Membrane bypass detection MUST trigger `EMERGENCY` evidence and C33 incident forwarding | Integration test |
| REQ-28 | Any translated or non-native machine identity presented as Sanctum-equivalent MUST fail closed | Security test |
| REQ-29 | Machine transports MUST terminate only on explicitly declared native receptors | Transport audit |

### 13.6 Integration Requirements

| ID | Requirement | Verification |
|----|-------------|-------------|
| REQ-30 | Trustee governance receptors MUST produce C14-compatible governance operations | C14 integration test |
| REQ-31 | Counterparty Foundry receptors MUST produce C18-compatible intake and license operations | C18 integration test |
| REQ-32 | Enterprise receptors MUST produce C45-compatible bounded execution descriptors | C45 integration test |
| REQ-33 | Public proof receptors MUST produce C5-compatible accountability queries | C5 integration test |
| REQ-34 | All transports MUST route through the same receptor pipeline | Transport invariant test |
| REQ-35 | Generated SDKs MUST preserve session ordering and membrane metadata | SDK validation test |

---

## 14. Claims

### Claim 1: Membrane-Typed Interface Architecture

A method for mediating external interactions with a sovereign epistemic system, wherein every interface receptor is bound to exactly one externally reachable membrane selected from `PUBLIC`, `ENTERPRISE`, or `FOUNDRY`, and no receptor may target a sealed inner `SANCTUM` capability.

### Claim 2: Session-Typed Externalization with Independent Membrane Gating

A method wherein session-typed receptors translate external inputs into internal operation descriptors, while a separate membrane gate independently determines whether the requested crossing is lawful, such that successful translation never implies execution authority.

### Claim 3: Causal Evidence Chain for Membrane Interactions

A method for producing hash-chained causal evidence records for every membrane interaction, wherein each record includes persona, membrane class, translation residuals, and causal references to triggered internal operations.

### Claim 4: Non-Interfering Persona Projections Over Bounded Membranes

A method for computing persona-specific views of sovereign system state from frozen epochs, wherein the views satisfy non-interference and are additionally constrained by membrane-specific release profiles.

---

## 15. Future Work

### 15.1 Natural-Language Translation Path

- Interpretive translation for ambiguous inputs
- Separate admission queue and risk scoring
- Mandatory confirmation for high-consequence operations

### 15.2 Mobile-Native Receptor Family

- Mobile-optimized public and trustee surfaces
- Offline caching with epoch-boundary refresh

### 15.3 Streaming Projections

- Continuous public status feeds
- Enterprise lease event streams
- Operator incident channels with speculative markers

### 15.4 Public Proof Ledger Integration

- Tight integration with future C48 accountability outputs
- Standard proof bundle packaging and predicate catalogs

---

## Appendix A: Session Type Formalism

```text
S ::= !T.S
    | ?T.S
    | S1 + S2
    | S1 & S2
    | mu X.S
    | end
```

Example:

```text
FoundryPetitionSession =
  ?Authenticate(Credential).
  ?SubmitPetition(Dossier, Scope, Constraints).
  !IntakeDecision(accepted | rejected, receipt, evidence_ref).
  end
```

---

## Appendix B: Translation Galois Connection

For each receptor `R`, the STE defines a Galois connection `(alpha_R, gamma_R)` between:

- external representation lattice `E`
- internal operation lattice `I`

Residuals capture the information difference between original input and the concretized form of the translated result.

---

## Appendix C: Persona Privilege Lattice Proof Sketch

For any `P_low <= P_high` and any state change `delta` visible only at `P_high`:

```text
Projection(P_low, M, E) = Projection(P_low, M, E + delta)
```

This holds because the authorize stage removes state outside the lower persona's admissible set before transformation and formatting.

---

## Appendix D: Exemplar Receptor Definitions

### D.1 governance_vote

```yaml
receptor_id: "urn:atrahasis:receptor:trustee:governance_vote:v1.1"
persona_family: Trustee
membrane_class: PUBLIC
session_type: "GovernanceVoteSession"
signal_binding:
  type: object
  required: [proposal_id, vote_choice]
response_type:
  type: object
  properties:
    vote_record_id: { type: string }
    evidence_ref: { type: string }
auth_level: TRUSTEE
rate_policy: { rpm: 30, burst: 5 }
release_profile: constitutional
version: "1.1.0"
min_version: "1.0.0"
evidence_class: HIGH_CONSEQUENCE
```

### D.2 foundry_petition

```yaml
receptor_id: "urn:atrahasis:receptor:counterparty:foundry_petition:v1.1"
persona_family: Counterparty
membrane_class: FOUNDRY
session_type: "FoundryPetitionSession"
signal_binding:
  type: object
  required: [petition_id, objective, dossier_hash]
response_type:
  type: object
  properties:
    intake_status: { type: string, enum: [accepted, rejected, review_required] }
    receipt_id: { type: string }
    evidence_ref: { type: string }
auth_level: COUNTERPARTY
rate_policy: { rpm: 6, burst: 2 }
release_profile: foundry_confidential
version: "1.1.0"
min_version: "1.0.0"
evidence_class: SIGNIFICANT
```

### D.3 proof_query

```yaml
receptor_id: "urn:atrahasis:receptor:public:proof_query:v1.1"
persona_family: Public
membrane_class: PUBLIC
session_type: "ProofQuerySession"
signal_binding:
  type: object
  required: [predicate_id]
response_type:
  type: object
  properties:
    predicate_id: { type: string }
    proof_bundle_ref: { type: string }
    disclosure_level: { type: string, enum: [public, public_redacted] }
auth_level: PUBLIC
rate_policy: { rpm: 120, burst: 20 }
release_profile: public_accountability
version: "1.1.0"
min_version: "1.0.0"
evidence_class: ROUTINE
```

---

## Appendix E: Evidence Record Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:atrahasis:emai:evidence:v1.1",
  "type": "object",
  "required": [
    "evidence_id",
    "timestamp",
    "tidal_epoch",
    "receptor_id",
    "persona",
    "membrane_class",
    "actor_id",
    "input_hash",
    "translation_result",
    "response_hash",
    "prev_evidence_hash",
    "evidence_hash",
    "evidence_class"
  ],
  "properties": {
    "evidence_id": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "tidal_epoch": { "type": "string" },
    "receptor_id": { "type": "string" },
    "persona": {
      "type": "string",
      "enum": ["Trustee", "Counterparty", "Operator", "Developer", "Public", "Agent"]
    },
    "membrane_class": {
      "type": "string",
      "enum": ["PUBLIC", "ENTERPRISE", "FOUNDRY"]
    },
    "actor_id": { "type": "string" },
    "input_hash": { "type": "string" },
    "translation_result": { "type": "object" },
    "translation_residual": { "type": "object" },
    "internal_ops_triggered": { "type": "array", "items": { "type": "string" } },
    "response_hash": { "type": "string" },
    "prev_evidence_hash": { "type": "string" },
    "evidence_hash": { "type": "string" },
    "evidence_class": {
      "type": "string",
      "enum": ["ROUTINE", "SIGNIFICANT", "HIGH_CONSEQUENCE", "EMERGENCY"]
    },
    "retention_days": { "type": "integer" }
  }
}
```

---

## Appendix F: Glossary

| Term | Definition |
|------|------------|
| `Receptor` | Session-typed interface point mediating one class of external interaction |
| `Persona Family` | One of six audience categories: Trustee, Counterparty, Operator, Developer, Public, Agent |
| `Membrane Class` | One of the three externally reachable EMA-I membranes: PUBLIC, ENTERPRISE, FOUNDRY |
| `Sanctum` | Sealed recursion-critical core with zero direct receptors |
| `STE` | Structured Translation Engine |
| `IEC` | Interaction Evidence Chain |
| `PPE` | Persona Projection Engine |
| `Release Profile` | Policy that bounds what may be emitted through a receptor |
| `Native Machine Boundary` | Rule that machine-facing receptors use native sovereign carriers and may not be satisfied by translated or legacy identity surfaces |
| `Membrane Completeness` | Property that all external interactions pass through EMA-I |

---

## Cross-References

| Spec | Relationship |
|------|-------------|
| C3 | Epoch timing and osmotic intake boundary |
| C5 | Verification surfaces and public proof bundles |
| C8 | Bookkeeping intents for Foundry and enterprise commercial flows |
| C14 | Governance and release-law authority |
| C18 | Foundry and enterprise externalization policy |
| C22 | Sequencing authority for membrane rollout |
| C24 | Habitat health data for operator projections |
| C32 | Agent identity and registration |
| C33 | Incident management and operator playbooks |
| C34 | Recovery status surfaces |
| C35 | Membrane monitoring and bypass detection |
| C40 | Trust anchors and native trust posture |
| C45 | Bounded enterprise execution surface |

---

*Document generated by Adapa for T-064 and renovated by Ninkasi for T-RENOVATE-006.*
