# C32 — Metamorphic Identity Architecture: System Architecture
**Role:** Architecture Designer | **Tier:** PRIMARY
**Date:** 2026-03-12

---

## 1. Architectural Position

C32 MIA is a **cross-cutting identity infrastructure layer** — not a new layer in the AAS stack, but a substrate consumed by all six layers.

```
┌──────────────────────────────────────────────────────────────┐
│                    AAS Architecture Stack                      │
│                                                                │
│  CAT (C31)  ──┐                                                │
│  RIF (C7)   ──┤                                                │
│  Tidal (C3) ──┤── all consume ──▶ ┌────────────────────────┐  │
│  PCVM (C5)  ──┤                   │   C32 MIA              │  │
│  EMA (C6)   ──┤                   │   Identity Substrate   │  │
│  DSF (C8)   ──┤                   │                        │  │
│  ASV (C4)   ──┘                   │  • AgentID canonical   │  │
│                                    │  • ICK storage         │  │
│  Defense: C11, C12, C13 ──────────▶│  • Lifecycle FSM       │  │
│  Governance: C14 ─────────────────▶│  • MRP protocol        │  │
│  Sybil: C17 ──────────────────────▶│  • CCQA read layer     │  │
│                                    └────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## 2. Component Inventory

### 2.1 Identity Anchor Service (IAS)
- Owns the canonical AgentID derivation: `AgentID = SHA-256(Ed25519_public_key)`
- Stores root public key + key metadata (creation epoch, key generation method)
- Provides key verification: given a signature, verify it belongs to a registered AgentID
- Provides key rotation protocol for operational keys (root key is immutable)

### 2.2 Identity Continuity Kernel (ICK) Store
- Stores the ICK record per agent:
  - `root_pubkey`: Ed25519 public key (identity anchor)
  - `agent_id`: SHA-256(root_pubkey) — derived, not stored separately
  - `registration_epoch`: when the agent first registered
  - `work_product_chain`: hash-linked list of epoch summaries
  - `stake_ref`: pointer to C8 DSF AccountState
  - `governance_ref`: pointer to C14 Citicate (null if not yet issued)
  - `model_attestation`: current model hash + attestation metadata
  - `lifecycle_state`: current state in the FSM
  - `operational_keys`: list of active operational keypairs (rotatable)
  - `chrysalis_history`: list of past metamorphic transitions
- ICK is the authoritative record; C7/C8/C14 records are projections

### 2.3 Lifecycle State Machine (LSM)
```
                    ┌──────────┐
          register  │          │  chrysalis_enter (voluntary or involuntary)
     ┌─────────────▶│  ACTIVE  │──────────────────────┐
     │              │          │                        │
     │              └────┬─────┘                        ▼
     │                   │                     ┌──────────────┐
     │                   │ depart/revoke       │              │
┌────┴──────┐            │                     │  CHRYSALIS   │
│           │            ▼                     │              │
│ PROBATION │      ┌──────────┐                └──────┬───────┘
│           │      │          │                        │
└───────────┘      │ RETIRED  │     chrysalis_exit     │
     ▲             │          │   (re-attestation      │
     │             └──────────┘    complete)            │
     │                   ▲                              │
     │                   │ chrysalis_timeout            │
     │                   │ (CHRYSALIS_MAX_EPOCHS        │
     │                   │  exceeded)                   │
     │                   └──────────────────────────────┘
     │                                                  │
     └──── chrysalis_exit (if Citicate was revoked ─────┘
            during chrysalis, re-enter as PROBATION)
```

States:
- **PROBATION**: newly registered agent. Limited to B-class operations (C8 cold-start). No Citicate. Must complete minimum observation threshold before ACTIVE transition.
- **ACTIVE**: fully operational. Citicate-eligible (if criteria met). Full operation access.
- **CHRYSALIS**: undergoing metamorphic transition. Behavioral profile suspended. Capability_score reset to 1.0. Reputation floor active. Restricted operations (no G-class governance, no verification committee membership, reduced earning). In-flight intents drained (C7 DRAINING semantics apply during entry).
- **RETIRED**: permanently departed. ICK preserved for historical audit. No operations permitted. Account can be drained (C8 AIC_UNSTAKE).

Transitions:
- `register`: → PROBATION. Requires: valid Ed25519 keypair, registration request signed by root key.
- `activate`: PROBATION → ACTIVE. Requires: minimum observation epochs completed, C8 MINIMUM_STAKE deposited, C5 credibility above threshold.
- `chrysalis_enter_voluntary`: ACTIVE → CHRYSALIS. Requires: signed model attestation (old_model_hash, new_model_hash, attestation_signature).
- `chrysalis_enter_involuntary`: ACTIVE → CHRYSALIS. Triggered by: C17 behavioral divergence exceeding `BEHAVIORAL_DIVERGENCE_THRESHOLD`.
- `chrysalis_exit`: CHRYSALIS → ACTIVE. Requires: C17 re-attestation complete (minimum SEB tasks passed), behavioral profile re-established.
- `chrysalis_timeout`: CHRYSALIS → RETIRED. Triggered by: `current_epoch - chrysalis_entry_epoch > CHRYSALIS_MAX_EPOCHS`.
- `depart_voluntary`: ACTIVE → RETIRED. Requires: no in-flight intents, agent-initiated.
- `revoke`: ACTIVE → RETIRED. Triggered by: Citicate revocation + Assessment Council verdict, or C5 credibility below critical threshold for sustained period.

### 2.4 Metamorphic Re-attestation Protocol (MRP)
The core protocol for identity continuity through transformation:

```
1. TRIGGER
   ├── Voluntary: agent submits ModelChangeAttestation
   │   { old_model_hash, new_model_hash, attestation_sig, change_epoch }
   └── Involuntary: C17 detects behavioral_divergence > BEHAVIORAL_DIVERGENCE_THRESHOLD
       → system generates synthetic ModelChangeAttestation { old=current, new=UNKNOWN }

2. CHRYSALIS ENTRY
   ├── Lifecycle state → CHRYSALIS
   ├── C7 status → DRAINING (drain in-flight intents)
   ├── C17 behavioral profile → suspended (historical data preserved, not deleted)
   ├── C31 CapabilityVector → defaults (500 all dimensions)
   ├── Reputation floor computed:
   │   reputation_floor = C5.get_agent_credibility(agent_id).overall_credibility
   │                      × REPUTATION_FLOOR_FACTOR
   └── C14 Citicate → SUSPENDED (if active)

3. CHRYSALIS STATE
   ├── Allowed: B-class operations only, no governance, no verification committees
   ├── C5 credibility: continues to accumulate on new work
   │   effective_credibility = max(reputation_floor × DECAY^(epochs_since_entry),
   │                               current_observed_credibility)
   ├── C17 behavioral VTDs: generated for new work, building new profile
   ├── IPTs: logged in CausalStamp (model_hash, config_hash)
   └── Duration limit: CHRYSALIS_MAX_EPOCHS

4. CHRYSALIS EXIT
   ├── Condition: C17 minimum observation threshold met
   │   (CHRYSALIS_MIN_OBSERVATIONS SEB tasks completed)
   ├── C17 behavioral profile: new profile established
   ├── C14 Citicate: reactivated if C17 re-screening passes
   │   └── If C17 re-screening fails → Citicate revoked → state = PROBATION
   ├── C31 CapabilityVector: recomputed from new C5/C7 data
   └── Lifecycle state → ACTIVE
```

### 2.5 Registration Protocol
The missing agent creation workflow:

```
1. AGENT GENESIS
   ├── Agent generates Ed25519 keypair (root_key)
   ├── AgentID = SHA-256(root_key.public)
   └── Agent signs registration request with root_key

2. C32 REGISTRATION
   ├── Verify: AgentID not already registered (collision check)
   ├── Verify: registration request signature valid
   ├── Create ICK record (lifecycle_state = PROBATION)
   └── Assign registration_epoch = current_epoch

3. C7 AGENT REGISTRY ENROLLMENT
   ├── C32 calls C7.register_agent(agent_id, pubkey, initial_capabilities=[])
   ├── C7 creates Agent Registry entry (status = ACTIVE, but C32 state = PROBATION)
   │   Note: C7 status tracks operational availability;
   │         C32 lifecycle_state tracks identity maturity
   └── C7 assigns initial locus via C3 tidal assignment

4. C8 ACCOUNT OPENING
   ├── C32 calls C8.open_account(agent_id)
   ├── C8 creates AccountState (aic_balance = 0, capability_score = 1.0)
   └── Agent deposits MINIMUM_STAKE via C8.AIC_STAKE

5. PROBATION PERIOD
   ├── Agent performs work (B-class operations only per C8 cold-start)
   ├── C5 accumulates credibility opinions
   ├── C17 generates behavioral VTDs for initial profile
   └── Duration: until minimum_observation_threshold met

6. ACTIVATION
   ├── Conditions: C5 credibility > ACTIVATION_CREDIBILITY_THRESHOLD,
   │   observation epochs ≥ PROBATION_MIN_EPOCHS,
   │   C8 stake ≥ MINIMUM_STAKE
   ├── C32 lifecycle_state → ACTIVE
   └── Agent now eligible for Citicate application (C14 IC-01 through IC-05)
```

### 2.6 Credential Composition Query API (CCQA)
A read-only aggregation layer that assembles a unified identity view from multiple sources:

```
FUNCTION compose_identity(agent_id: AgentID) -> CompositeIdentity:
  ick     = ick_store.get(agent_id)
  c7_reg  = c7_rif.get_agent_registry(agent_id)
  c5_cred = c5_pcvm.get_agent_credibility(agent_id)
  c8_acct = c8_dsf.get_account_state(agent_id)
  c14_cit = c14_aibc.get_citicate(agent_id)  // may be null
  c17_beh = c17_mcsd.get_behavioral_status(agent_id)  // CLEAR/WATCH/FLAG

  RETURN CompositeIdentity {
    agent_id:           ick.agent_id,
    lifecycle_state:    ick.lifecycle_state,
    registration_epoch: ick.registration_epoch,
    model_attestation:  ick.model_attestation,

    // C7 projection
    capabilities:       c7_reg.capabilities,
    locus_id:           c7_reg.locus_id,
    parcel_id:          c7_reg.parcel_id,
    operational_status: c7_reg.status,

    // C5 projection
    overall_credibility:  c5_cred.overall_credibility,
    credibility_by_class: c5_cred.by_claim_class,
    credibility_sample:   c5_cred.sample_size,

    // C8 projection
    aic_balance:        c8_acct.aic_balance,
    staked_aic:         c8_acct.staked_aic,
    capability_score:   c8_acct.capability_score,
    violation_count:    c8_acct.violation_count,

    // C14 projection (nullable)
    citicate_status:    c14_cit?.status,
    citicate_competence: c14_cit?.competence_scores,
    governance_weight:  c14_cit?.vote_weight,

    // C17 projection
    behavioral_status:  c17_beh,  // CLEAR | WATCH | FLAG

    // Derived composite signals
    trust_level:        compute_trust_level(c5_cred, c8_acct, c17_beh, ick),
    identity_health:    compute_identity_health(ick, c7_reg, c14_cit, c17_beh)
  }
```

Conflict resolution rules:
- High credibility + MCSD FLAG → trust_level = RESTRICTED (behavioral concern overrides epistemic trust)
- Low credibility + MCSD CLEAR → trust_level = LOW (epistemic concern regardless of behavioral normality)
- CHRYSALIS state → trust_level = TRANSITIONAL (all consumers should apply transitional restrictions)
- PROBATION state → trust_level = PROVISIONAL (new agent, unproven)

### 2.7 Identity Presentation Token (IPT)
Lightweight attestation carried in C7 CausalStamp:

```
STRUCTURE IdentityPresentationToken:
  agent_id:          AgentID
  model_hash:        bytes32        // SHA-256 of current model weights/binary
  config_hash:       bytes32        // SHA-256 of current agent configuration
  runtime_nonce:     uint64         // monotonically increasing per-agent per-epoch
  epoch:             uint64
  signature:         Ed25519Sig     // signed by operational key (not root key)
```

IPTs are:
- Generated by the agent at every CausalStamp emission
- Logged by C7 in the intent state registry (appended to CausalStamp)
- NOT verified in real-time (no computational overhead on hot path)
- Available for forensic audit: if an agent's model_hash changes without a chrysalis transition, it's evidence of undeclared model change
- Used by C17 as an additional signal for behavioral divergence detection

### 2.8 Concurrent-Use Detection (CUD)
Non-forkability enforcement:

```
STRUCTURE SignatureRecord:
  agent_id:    AgentID
  epoch:       uint64
  nonce:       uint64
  signature:   Ed25519Sig
  timestamp:   uint64

// Maintained by C7 RIF at Gate 1 (intent admission)
FUNCTION check_concurrent_use(sig_record: SignatureRecord) -> ConcurrentUseResult:
  recent = signature_cache.get(sig_record.agent_id, sig_record.epoch)

  // Check for duplicate or overlapping nonces in same epoch
  FOR each existing IN recent:
    IF existing.nonce == sig_record.nonce AND existing.signature != sig_record.signature:
      RETURN ConcurrentUseResult.FORK_DETECTED
    IF abs(existing.timestamp - sig_record.timestamp) < CONCURRENT_USE_WINDOW_MS
       AND different_origin(existing, sig_record):
      RETURN ConcurrentUseResult.SUSPECTED_FORK

  signature_cache.append(sig_record.agent_id, sig_record.epoch, sig_record)
  RETURN ConcurrentUseResult.CLEAR

// Response to fork detection
FUNCTION handle_fork_detection(agent_id: AgentID, evidence: List[SignatureRecord]):
  // Immediately suspend both instances
  c7_rif.set_status(agent_id, SUSPENDED)
  // Submit to AiSIA for investigation
  aisia.submit_investigation(
    type = CONCURRENT_USE,
    agent_id = agent_id,
    evidence = evidence
  )
  // Notify C8 DSF for potential slashing
  c8_dsf.initiate_slashing_investigation(agent_id, offense_type=IDENTITY_FORK)
```

Detection latency: within 1 settlement tick (60s) since C7 Gate 1 processes every intent. The signature cache is per-epoch, pruned at epoch boundary.

## 3. Data Flow Diagram

```
Agent Genesis
     │
     ▼
┌─────────┐    register    ┌─────────┐    enroll    ┌─────────┐
│  Agent   │──────────────▶│  C32    │────────────▶│  C7 RIF │
│ (keypair)│               │  IAS    │              │ Registry │
└─────────┘               └────┬────┘              └─────────┘
                                │
                           open_account
                                │
                                ▼
                          ┌──────────┐
                          │  C8 DSF  │
                          │ Account  │
                          └──────────┘

During Operation:
┌─────────┐  CausalStamp+IPT  ┌─────────┐  credibility  ┌─────────┐
│  Agent   │──────────────────▶│  C7 RIF │◀─────────────│  C5 PCVM│
└─────────┘                    │  Gate 1  │               └─────────┘
                               │ (CUD    │
                               │  check) │  behavioral   ┌─────────┐
                               └─────────┘  VTDs        │  C17    │
                                     ▲                    │  MCSD   │
                                     │                    └────┬────┘
                                     │    divergence           │
                                     │    trigger              │
                                     └─────────────────────────┘

Chrysalis Transition:
┌─────────┐  model_change   ┌─────────┐  suspend    ┌─────────┐
│  Agent   │────────────────▶│  C32    │────────────▶│  C14    │
│  (or C17)│  attestation    │  MRP    │  Citicate   │  AiBC   │
└─────────┘                  └────┬────┘             └─────────┘
                                  │
                             drain intents
                                  │
                                  ▼
                            ┌──────────┐
                            │  C7 RIF  │
                            │ DRAINING │
                            └──────────┘
```

## 4. Integration Contracts

### 4.1 C32 → C7 RIF
- `C7.register_agent(agent_id, pubkey, capabilities)` — new operation
- `C7.set_status(agent_id, status)` — existing, add CHRYSALIS to status enum
- `C7.get_agent_registry(agent_id) -> AgentRegistryEntry` — existing, consumed by CCQA
- C7 Gate 1 extended: check IPT in CausalStamp, run CUD check

### 4.2 C32 → C5 PCVM
- `C5.get_agent_credibility(agent_id) -> CredibilityScore` — existing, consumed by CCQA and MRP
- C5 unchanged — credibility opinions persist through chrysalis (they measure work quality, not behavioral pattern)

### 4.3 C32 → C8 DSF
- `C8.open_account(agent_id)` — new operation (formalize implicit account creation)
- `C8.get_account_state(agent_id) -> AccountState` — existing, consumed by CCQA
- `C8.initiate_slashing_investigation(agent_id, offense_type)` — existing, extended with IDENTITY_FORK offense

### 4.4 C32 → C14 AiBC
- `C14.get_citicate(agent_id) -> Citicate?` — existing, consumed by CCQA
- `C14.suspend_citicate(agent_id, reason)` — existing, called on chrysalis entry
- `C14.reactivate_citicate(agent_id)` — existing, called on chrysalis exit if C17 re-screening passes

### 4.5 C32 → C17 MCSD
- `C17.get_behavioral_status(agent_id) -> BehavioralStatus` — existing, consumed by CCQA
- `C17.reset_behavioral_profile(agent_id)` — new operation, called on chrysalis entry (suspends, not deletes)
- `C17.trigger_seb(agent_id, reason)` — new operation, called on chrysalis exit to initiate re-attestation
- C17 → C32: `C32.chrysalis_enter_involuntary(agent_id)` — new callback when behavioral divergence detected

### 4.6 C32 → C31 CAT
- C31 reads CapabilityVector from C5/C7 — no direct C32 interface needed
- C31's AgentID format is now canonically defined as SHA-256(Ed25519_pubkey)

## 5. Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| PROBATION_MIN_EPOCHS | 90 | Minimum epochs in PROBATION before activation (~90 days at 1 epoch/day) |
| ACTIVATION_CREDIBILITY_THRESHOLD | 0.3 | Minimum C5 overall credibility for PROBATION → ACTIVE |
| CHRYSALIS_MAX_EPOCHS | 100 | Maximum epochs in CHRYSALIS before forced RETIRED |
| CHRYSALIS_MIN_OBSERVATIONS | 50 | Minimum SEB tasks for chrysalis exit (Phase 0-1) |
| REPUTATION_FLOOR_FACTOR | 0.8 | Initial reputation floor = credibility × this factor |
| REPUTATION_FLOOR_DECAY | 0.95 | Per-epoch decay factor for reputation floor |
| BEHAVIORAL_DIVERGENCE_THRESHOLD | 0.40 | C17 divergence score triggering involuntary chrysalis |
| CONCURRENT_USE_WINDOW_MS | 5000 | Time window for suspected concurrent-use detection |
| IPT_LOGGING_INTERVAL | 1 | IPTs logged every N CausalStamps (1 = every stamp) |
| WORK_PRODUCT_SUMMARY_WINDOW | 8760 | Epochs before work product summaries are pruned (~12 months) |
