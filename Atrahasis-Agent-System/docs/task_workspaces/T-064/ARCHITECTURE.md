# EMA-I System Architecture
**Agent:** Adapa | **Date:** 2026-03-12 | **Version:** 1.0

---

## 1. Architectural Overview

The Epistemic Membrane Architecture for Interfaces (EMA-I) is a sovereign boundary layer between the Atrahasis internal epistemic stack and all external entities (humans, external systems, third-party agents). It mediates every external interaction through typed receptors, translates between external and internal representations, generates auditable evidence, and projects internal epistemic state into persona-specific views.

### 1.1 Position in the Atrahasis Stack

```
External World (Humans, APIs, Agents, Browsers)
     │
     ▼
┌─────────────────────────────────────────┐
│  EMA-I: Epistemic Membrane Architecture │  ← THIS INVENTION
│  ┌─────────┐ ┌──────────┐ ┌───────────┐ │
│  │Receptors│ │Translator│ │ Evidence  │ │
│  │ (typed) │ │ (struct) │ │  Chain    │ │
│  └────┬────┘ └────┬─────┘ └─────┬─────┘ │
│       │      ┌────┴─────┐       │       │
│       │      │ Persona  │       │       │
│       │      │Projector │       │       │
│       │      └──────────┘       │       │
└───────┼─────────────────────────┼───────┘
        │                         │
        ▼                         ▼
┌──────────────────────────────────────────┐
│  Internal Atrahasis Stack                │
│  C7 RIF │ C3 Tidal │ C5 PCVM │ C8 DSF  │
│  C6 EMA │ C23 SCR  │ C33 OINC│ C14 Gov │
│  C32 MIA│ C35 Sent │ C34 BSRF│ C4 ASV  │
└──────────────────────────────────────────┘
```

### 1.2 Design Principles

1. **Sovereign Boundary**: The membrane has authority to deny, transform, rate-limit, and audit. It is not a passthrough.
2. **Epistemic-Native**: Receptors bind to claim classes and epistemic objects, not just data schemas.
3. **Session-Typed**: Every receptor is a session type, guaranteeing protocol compliance at compile time.
4. **Evidence-by-Default**: Every interaction generates a causal evidence record. No silent interactions.
5. **Projection-Consistent**: All persona views derive from the same frozen epoch state. Non-interference is proven.

---

## 2. Core Components

### 2.1 Typed Interaction Receptors

A receptor is a session-typed interface point that mediates a specific class of external interaction.

#### 2.1.1 Receptor Definition

```
Receptor := {
  receptor_id:    URN (unique, versioned)
  persona_family: Trustee | Provider | Operator | Developer | Agent
  session_type:   SessionType (Honda et al.)
  signal_binding: InputSchema (what external signals this receptor accepts)
  operation_map:  InternalOp[] (what internal operations this receptor triggers)
  response_type:  OutputSchema (what this receptor emits)
  auth_level:     AuthorizationLevel
  version:        SemVer
  min_version:    SemVer (oldest accepted version)
  rate_limit:     RatePolicy
  evidence_class: EvidenceClassification
}
```

#### 2.1.2 Five Persona Families

| Family | Primary Consumers | Key Receptors | Owning Specs |
|--------|-------------------|---------------|--------------|
| **Trustee** | Human trustees, tribunal members, nominating bodies | governance_vote, constitutional_amendment, tribunal_filing, emergency_authority, nominating_submission | C14, C16 |
| **Provider** | External compute providers, enterprise customers, VaaS consumers | task_submit, task_result, verification_request, provider_onboard, billing_query | C18, C15 |
| **Operator** | System operators, incident responders, habitat administrators | incident_query, playbook_trigger, recovery_status, habitat_health, anomaly_review | C33, C34, C35, C24 |
| **Developer** | Engineers, CI/CD systems, contract test runners | schema_validate, contract_test_run, sdk_generate, spec_query, deployment_status | C22, C4, C9 |
| **Agent** | External AI agents, Atrahasis agents via membrane | claim_submit, verification_query, credibility_lookup, cell_status, knowledge_retrieve | C5, C6, C23, C32 |

#### 2.1.3 Session Type Example (Governance Vote)

```
GovernanceVoteSession =
  ?authenticate(AgentID, Credential).
  !proposal_context(ProposalID, ProposalSummary, VotingRules).
  ?cast_vote(VoteChoice, VoteRationale).
  !vote_receipt(VoteRecordID, EvidenceChainRef).
  end
```

The `?` prefix denotes receive (from external), `!` denotes send (to external). The session type guarantees:
- Authentication happens before proposal context is sent
- Vote is cast only after receiving proposal context
- Receipt is always issued after vote
- No other message orderings are possible

#### 2.1.4 Receptor Registry

All receptors are registered in a machine-readable receptor registry. The registry supports:
- Discovery: list available receptors per persona family
- Version negotiation: client requests a version range, registry resolves to concrete version
- Schema export: OpenAPI 3.1, GraphQL SDL, and gRPC proto generation from receptor definitions
- Deprecation: receptors marked deprecated continue to function until min_version sunset

### 2.2 Structured Translation Engine (STE)

The STE performs deterministic bidirectional translation between external representations and internal C4 ASV epistemic objects.

#### 2.2.1 Translation as Galois Connection

For each receptor, translation is formalized as a Galois connection (α, γ) where:
- α (abstraction): external_input → internal_operation (may lose information)
- γ (concretization): internal_state → external_response (may introduce ambiguity)

The translation contract guarantees:
- **Soundness**: α(input) is a valid internal operation for all valid inputs
- **Completeness**: γ(state) includes all information the persona is authorized to see
- **Residual capture**: information lost in α is recorded in the evidence chain as a translation_residual field

#### 2.2.2 Translation Categories

| Category | Direction | Example | Complexity |
|----------|-----------|---------|------------|
| **Governance → G-class** | Inbound | Trustee vote → G-GOV claim via C14 GTP | Deterministic (template-driven) |
| **Task → Settlement** | Inbound | Provider task submission → C8 DSF settlement operation | Deterministic (schema mapping) |
| **Incident → Capsule Query** | Inbound | Operator incident search → C33 OINC capsule retrieval | Deterministic (filter mapping) |
| **Schema → Validation** | Inbound | Developer schema submission → C4 ASV conformance check | Deterministic (JSON Schema) |
| **Claim → Verification** | Inbound | Agent claim assertion → C5 PCVM verification request | Deterministic (claim class routing) |
| **State → Projection** | Outbound | Internal epistemic state → persona-specific rendered view | Deterministic (projection function) |

All v1.0 translations are structured and deterministic. No NL/ambiguous translation in v1.0.

#### 2.2.3 Translation Pipeline

```
Input → Receptor Validation → Session Type Check →
  STE Translation (α) → Authorization Check →
    Internal Dispatch → Response Generation →
      STE Concretization (γ) → Evidence Emit → Output
```

Critical ordering: **authenticate → validate → translate → authorize → dispatch**. Translation NEVER confers authority. The translated operation descriptor is authorized separately.

### 2.3 Interaction Evidence Chain (IEC)

Every interaction through the membrane generates a causal evidence record.

#### 2.3.1 Evidence Record Format

```
InteractionEvidence := {
  evidence_id:       UUID
  timestamp:         ISO 8601 (nanosecond)
  tidal_epoch:       EpochID (C3)
  receptor_id:       URN (which receptor processed this)
  persona:           PersonaFamily
  actor_id:          AgentID (C32 MIA) or ExternalID

  // Causal chain
  input_hash:        SHA-256 (raw input)
  translation_result: InternalOpDescriptor
  translation_residual: ResidualRecord (what was lost in translation)
  internal_ops_triggered: OpRef[] (causal links to internal operations)
  response_hash:     SHA-256 (response sent)

  // Chain integrity
  prev_evidence_hash: SHA-256 (previous record in chain)
  evidence_hash:     SHA-256 (this record)

  // Classification
  evidence_class:    ROUTINE | SIGNIFICANT | HIGH_CONSEQUENCE | EMERGENCY
  retention_policy:  RetentionDuration (from evidence_class)
}
```

#### 2.3.2 Evidence Properties

- **Causal completeness**: every internal operation caused by the interaction is linked via internal_ops_triggered
- **Tamper detection**: cryptographic hash chain makes post-hoc modification detectable
- **PCVM integration**: evidence records above ROUTINE class are periodically committed to C5 PCVM as D-class (Direct observation) claims
- **OINC integration**: evidence records classified HIGH_CONSEQUENCE or EMERGENCY are forwarded to C33 OINC for incident correlation
- **Asynchronous generation**: evidence is written behind the response path (write-behind) to stay off the critical latency path

### 2.4 Persona Projection Engine (PPE)

The PPE computes purpose-built views of internal epistemic state for each persona.

#### 2.4.1 Projection Function

```
Projection(persona, epoch) :=
  filter(authorize(persona), state(epoch)) |>
  transform(persona.rendering_rules) |>
  format(persona.output_format)
```

Each projection is a pure function of (internal_state, persona_type, epoch). No side effects, no hidden state.

#### 2.4.2 Projection Properties

- **Epoch-bound**: projections are computed against frozen epoch state (C3 tidal epoch boundary). Within an epoch, all projections are consistent.
- **Non-interfering**: information visible to a lower-privilege persona does not reveal information restricted to a higher-privilege persona. Formally proven via the persona privilege lattice.
- **Incremental**: for monotone projection functions, incremental view maintenance (delta updates). Non-monotone projections recomputed at epoch boundaries.
- **Cacheable**: projections for a (persona, epoch) pair are immutable once computed.

#### 2.4.3 Persona Privilege Lattice

```
         Trustee
        /       \
   Provider    Operator
        \       /
        Developer
           |
         Agent (external)
```

Non-interference requirement: for any two personas P_low ≤ P_high in the lattice, changes visible only to P_high must not affect P_low's projection.

#### 2.4.4 Per-Persona Rendering

| Persona | Sees | Does NOT See | Format |
|---------|------|-------------|--------|
| Trustee | Governance decisions, constitutional state, tribunal cases, emergency status, full CFI | Individual agent credibility details, marketplace task internals | Constitutional language, legal terminology |
| Provider | Available tasks, verification results, settlement status, earnings, SLA metrics | Governance internals, other providers' performance, security incidents | Marketplace terminology, financial summaries |
| Operator | Incident capsules, recovery predicates, habitat health, anomaly alerts, all layer status | Governance voting details, marketplace economics, individual agent credibility | Operational vocabulary, severity classifications |
| Developer | Contract test results, schema validation, deployment status, API documentation, spec versions | Governance voting, marketplace economics, security incidents | Technical documentation, code examples |
| Agent | Claim verification status, credibility scores, knowledge retrieval, cell status, epoch timing | Governance internals (unless participating), operator incidents, marketplace settlement | C4 ASV native format |

---

## 3. Integration Architecture

### 3.1 Consuming Specs (Inbound)

| Internal Spec | Integration Point | Receptor Family | Operation |
|---|---|---|---|
| C14 AiBC | GTP governance decisions, AiDP voting, tribunal filings | Trustee | governance_vote, constitutional_amendment, tribunal_filing |
| C16 Outreach | Nominating body submissions, engagement tracking | Trustee | nominating_submission |
| C18 Funding | Task marketplace, VaaS, enterprise API | Provider | task_submit, verification_request, provider_onboard |
| C15 Economics | ACI queries, reference rate publication | Provider | aci_query, rate_subscribe |
| C33 OINC | Incident queries, playbook triggers | Operator | incident_query, playbook_trigger |
| C34 BSRF | Recovery status queries | Operator | recovery_status |
| C35 Sentinel | Anomaly review, alert management | Operator | anomaly_review |
| C24 FHF | Habitat health, federation status | Operator | habitat_health |
| C22 Planning | Contract tests, deployment status | Developer | contract_test_run, deployment_status |
| C4 ASV | Schema validation | Developer | schema_validate |
| C5 PCVM | Claim submission, verification queries | Agent | claim_submit, verification_query |
| C6 EMA | Knowledge retrieval | Agent | knowledge_retrieve |
| C23 SCR | Cell status queries | Agent | cell_status |
| C32 MIA | Identity registration, credibility lookup | Agent | identity_register, credibility_lookup |

### 3.2 Producing Specs (Outbound)

| Consuming Spec | What EMA-I Provides |
|---|---|
| C5 PCVM | Interaction evidence records as D-class claims for verification |
| C33 OINC | HIGH_CONSEQUENCE/EMERGENCY evidence for incident correlation |
| C8 DSF | Settlement operations from marketplace receptor translations |
| C35 Sentinel | Membrane traffic patterns as anomaly detection input |

### 3.3 Transport Bindings

EMA-I is transport-agnostic at the architectural level. Implementation bindings:

| Transport | Use Case | Notes |
|---|---|---|
| REST/HTTP | Human-facing web interfaces, Developer APIs | OpenAPI 3.1 generated from receptor registry |
| GraphQL | Complex queries, Developer and Operator dashboards | SDL generated from receptor registry |
| gRPC | High-performance agent-to-membrane, Provider settlement | Proto generated from receptor registry |
| WebSocket | Real-time Operator dashboards, Agent event streams | Subscription receptors with push semantics |
| MCP | AI agent tool interface | C4 ASV objects as MCP tool responses |
| A2A | Agent-to-agent via membrane | C4 ASV objects as A2A message parts |

---

## 4. Security Architecture

### 4.1 Authentication

- **Human users**: OAuth 2.1 with PKCE, federated identity (SAML/OIDC for institutional partners)
- **AI agents**: C32 MIA AgentID (Ed25519 signature verification)
- **External systems**: mTLS + API key + rate tier
- **Authentication happens BEFORE receptor binding and translation**

### 4.2 Authorization

- **Persona-based**: authenticated identity maps to persona family
- **Receptor-level**: each receptor declares required auth_level
- **Operation-level**: translated operation descriptor is authorized independently (principle of least authority)
- **Composition-aware**: composed receptor chains require join of component auth levels

### 4.3 Rate Limiting

- Per-persona rate tiers (Trustee: generous, Agent: strict)
- Per-receptor rate limits (governance_vote: low frequency, schema_validate: high frequency)
- Adaptive rate limiting based on evidence classification (HIGH_CONSEQUENCE operations have lower burst limits)

### 4.4 Membrane Completeness

- Internal components are NOT directly addressable from outside the membrane
- All external interactions MUST pass through a receptor
- Network architecture enforces this (internal components on private network)
- Membrane bypass detection via C35 Sentinel traffic analysis

---

## 5. Deployment Architecture

### 5.1 C22 Wave Integration

| Wave | EMA-I Component | Dependencies |
|---|---|---|
| W1 | Receptor registry + Developer receptors (schema_validate, contract_test_run) | C4 ASV, C9 contracts |
| W2 | Agent receptors (claim_submit, verification_query) + Evidence chain | C5 PCVM, C23 SCR |
| W3 | Operator receptors + Persona projections | C33 OINC, C35 Sentinel |
| W4 | Provider receptors (marketplace) | C18, C8 DSF |
| W5 | Trustee receptors (governance) | C14, C16 |

### 5.2 Scaling Model

- Receptor processing is stateless and horizontally scalable
- Evidence chain is append-only, partitioned by tidal epoch
- Projections are cacheable per (persona, epoch) — CDN-friendly
- Translation engine is stateless (pure functions)
- Rate limiting requires shared state (Redis/equivalent) across membrane instances

---

## 6. Parameters

| ID | Parameter | Default | Range | Governed By |
|----|-----------|---------|-------|-------------|
| P-01 | MAX_RECEPTOR_COMPOSITION_DEPTH | 3 | 1-10 | Stiftung Board |
| P-02 | EVIDENCE_CHAIN_COMMIT_INTERVAL | 100 records | 10-1000 | Operations |
| P-03 | PROJECTION_CACHE_TTL | TIDAL_EPOCH (3600s) | 60-7200 | Operations |
| P-04 | RATE_LIMIT_TRUSTEE_RPM | 60 | 10-300 | Stiftung Board |
| P-05 | RATE_LIMIT_PROVIDER_RPM | 600 | 100-3000 | Operations |
| P-06 | RATE_LIMIT_OPERATOR_RPM | 300 | 60-1500 | Operations |
| P-07 | RATE_LIMIT_DEVELOPER_RPM | 1200 | 300-6000 | Operations |
| P-08 | RATE_LIMIT_AGENT_RPM | 6000 | 1000-30000 | Operations |
| P-09 | MIN_RECEPTOR_VERSION_LAG | 2 major versions | 1-5 | Stiftung Board |
| P-10 | EVIDENCE_RETENTION_ROUTINE | 90 days | 30-365 | Stiftung Board |
| P-11 | EVIDENCE_RETENTION_SIGNIFICANT | 1 year | 180-730 | Stiftung Board |
| P-12 | EVIDENCE_RETENTION_HIGH_CONSEQUENCE | 7 years | 3-perpetual | Stiftung Board |
| P-13 | EVIDENCE_RETENTION_EMERGENCY | perpetual | perpetual | Constitutional (L0) |
| P-14 | PROJECTION_STALENESS_MAX | 1 TIDAL_EPOCH | 1-10 | Operations |
| P-15 | PCVM_COMMIT_THRESHOLD | SIGNIFICANT | ROUTINE-EMERGENCY | Stiftung Board |
| P-16 | MEMBRANE_BYPASS_ALERT_THRESHOLD | 1 event | 1-10 | Constitutional (L0) |
