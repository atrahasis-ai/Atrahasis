# Metamorphic Identity Architecture: A Unified Agent Identity System with Continuity Through Transformation

## Master Technical Specification — C32

## Version 1.0

**Invention ID:** C32
**Concept:** C32 Metamorphic Identity Architecture (MIA)
**Date:** 2026-03-12
**Status:** SPECIFICATION — Master Tech Spec v1.0
**Predecessor Specs:** C7 RIF (Agent Registry), C5 PCVM (Credibility Engine), C8 DSF (Settlement Accounts), C14 AiBC (Citicate), C17 MCSD (Behavioral Similarity), C31 CAT (Agent Topology)
**Ideation Council Verdict:** SELECTED. Novelty 4/5, Feasibility 4/5, Impact 4/5, Risk 4/10 (MEDIUM)
**Feasibility Verdict:** ADVANCE
**Primary Scale Target:** Same as AAS core: 1,000–10,000 agents

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. Introduction and Motivation](#2-introduction-and-motivation)
  - [2.1 The Identity Fragmentation Problem](#21-the-identity-fragmentation-problem)
  - [2.2 The Model Upgrade Continuity Problem](#22-the-model-upgrade-continuity-problem)
  - [2.3 What C32 MIA Contributes](#23-what-c32-mia-contributes)
  - [2.4 Position in the Atrahasis Stack](#24-position-in-the-atrahasis-stack)
- [3. Background and Related Work](#3-background-and-related-work)
  - [3.1 Decentralized Identifiers and Verifiable Credentials](#31-decentralized-identifiers-and-verifiable-credentials)
  - [3.2 ERC-8004 and On-Chain Agent Identity](#32-erc-8004-and-on-chain-agent-identity)
  - [3.3 Soulbound Tokens and Non-Transferable Identity](#33-soulbound-tokens-and-non-transferable-identity)
  - [3.4 SPIFFE/SPIRE Workload Identity](#34-spiffespire-workload-identity)
  - [3.5 Signet and Commercial AI Agent Identity](#35-signet-and-commercial-ai-agent-identity)
  - [3.6 How C32 MIA Differs](#36-how-c32-mia-differs)
- [4. Core Concepts](#4-core-concepts)
  - [4.1 Canonical AgentID](#41-canonical-agentid)
  - [4.2 Identity Continuity Kernel](#42-identity-continuity-kernel)
  - [4.3 Lifecycle State Machine](#43-lifecycle-state-machine)
  - [4.4 Metamorphic Re-attestation Protocol](#44-metamorphic-re-attestation-protocol)
  - [4.5 Identity Presentation Tokens](#45-identity-presentation-tokens)
- [5. Registration Protocol](#5-registration-protocol)
  - [5.1 Agent Genesis](#51-agent-genesis)
  - [5.2 Multi-Step Enrollment](#52-multi-step-enrollment)
  - [5.3 Probation Period](#53-probation-period)
  - [5.4 Activation Criteria](#54-activation-criteria)
- [6. Metamorphic Re-attestation Protocol — Detailed Design](#6-metamorphic-re-attestation-protocol--detailed-design)
  - [6.1 Chrysalis Entry Triggers](#61-chrysalis-entry-triggers)
  - [6.2 Chrysalis State Restrictions](#62-chrysalis-state-restrictions)
  - [6.3 Reputation Floor Computation](#63-reputation-floor-computation)
  - [6.4 Chrysalis Exit Conditions](#64-chrysalis-exit-conditions)
  - [6.5 Anti-Laundering Controls](#65-anti-laundering-controls)
  - [6.6 Chrysalis Timeout and Forced Retirement](#66-chrysalis-timeout-and-forced-retirement)
- [7. Credential Composition](#7-credential-composition)
  - [7.1 Composition Function](#71-composition-function)
  - [7.2 Conflict Resolution Rules](#72-conflict-resolution-rules)
  - [7.3 Trust Level Derivation](#73-trust-level-derivation)
- [8. Non-Forkability and Concurrent-Use Detection](#8-non-forkability-and-concurrent-use-detection)
  - [8.1 Nonce-Based Detection](#81-nonce-based-detection)
  - [8.2 Response Protocol](#82-response-protocol)
  - [8.3 Root Key Compromise](#83-root-key-compromise)
- [9. Integration Contracts](#9-integration-contracts)
  - [9.1 C32 ↔ C7 RIF](#91-c32--c7-rif)
  - [9.2 C32 ↔ C5 PCVM](#92-c32--c5-pcvm)
  - [9.3 C32 ↔ C8 DSF](#93-c32--c8-dsf)
  - [9.4 C32 ↔ C14 AiBC](#94-c32--c14-aibc)
  - [9.5 C32 ↔ C17 MCSD](#95-c32--c17-mcsd)
  - [9.6 C32 ↔ C31 CAT](#96-c32--c31-cat)
  - [9.7 C32 ↔ C3 Tidal Noosphere](#97-c32--c3-tidal-noosphere)
- [10. Security Analysis](#10-security-analysis)
  - [10.1 Threat Model](#101-threat-model)
  - [10.2 Attack Surface Analysis](#102-attack-surface-analysis)
  - [10.3 Identity Laundering Defenses](#103-identity-laundering-defenses)
  - [10.4 Registration Spam Defenses](#104-registration-spam-defenses)
- [11. Parameters](#11-parameters)
- [12. Formal Requirements](#12-formal-requirements)
- [13. Deployment Considerations](#13-deployment-considerations)
  - [13.1 C22 Wave Integration](#131-c22-wave-integration)
  - [13.2 Bootstrap Sequence](#132-bootstrap-sequence)
- [14. Open Questions](#14-open-questions)
- [15. Patent-Style Claims](#15-patent-style-claims)
- [16. Conclusion](#16-conclusion)

---

## 1. Abstract

The Metamorphic Identity Architecture (MIA) provides a unified identity substrate for the Atrahasis Agent System. It solves two problems that no existing agent identity system addresses: (1) identity fragmentation across six independent specifications (C5, C7, C8, C14, C17, C31), each of which stores and operates on partial views of agent identity with no canonical registration protocol, no unified identifier format, and no coordinated lifecycle management; and (2) identity continuity through fundamental agent transformation — the problem of what happens to an AI agent's identity, reputation, and governance rights when its underlying model is upgraded.

The architecture introduces four innovations. First, the **Identity Continuity Kernel (ICK)** — a minimal set of invariant anchors (root cryptographic key, verified work product history, economic stake position, governance commitments) that persist through any transformation. Second, the **Metamorphic Re-attestation Protocol (MRP)** — a formal protocol for identity preservation during model upgrades: the agent enters a chrysalis state where behavioral classification is suspended, operates under a decaying reputation floor derived from its historical credibility, and exits chrysalis only after completing behavioral re-attestation. Third, a **canonical AgentID** derived as SHA-256 of the agent's Ed25519 public key, resolving the format inconsistency across all six consuming specifications. Fourth, a **Credential Composition function** that assembles unified identity views from the independent credential sources without replacing them.

C32 MIA is a cross-cutting infrastructure layer — not a new layer in the AAS stack, but a substrate consumed by all layers. It fills the most significant architectural gap identified in the T-063 task analysis: the absence of a defined agent registration protocol, a canonical identifier format, and a lifecycle management system. It also provides the only known solution to C17 OQ-05, the previously unresolved open question of identity continuity across model upgrades.

---

## 2. Introduction and Motivation

### 2.1 The Identity Fragmentation Problem

The AAS architecture comprises six layers, each of which independently maintains aspects of agent identity:

| Spec | Identity Slice | Data Stored | Operations |
|------|---------------|-------------|------------|
| C7 RIF | Operational registry | agent_id, pubkey, capabilities, status, locus, heartbeat | Capability query, liveness, intent admission |
| C5 PCVM | Epistemic reputation | Per-agent, per-class credibility opinions (b,d,u,a) | Credibility update, forgery detection |
| C8 DSF | Economic accounts | AIC/PC balances, stake, capability_score, violations | Staking, slashing, settlement |
| C14 AiBC | Governance citizenship | Citicate credential, competence scores, vote weight | Issuance, revocation, renewal |
| C17 MCSD | Behavioral fingerprint | 5-modality behavioral VTDs, similarity scores | B(a_i,a_j) computation, Sybil detection |
| C31 CAT | Structural topology | CapabilityVector (5 dimensions), DAN role assignment | DAN formation, role assignment |

This fragmentation produces seven specific gaps:

1. **No registration protocol.** No spec defines how an agent first enters the system — who creates the Agent Registry entry, who opens the DSF account, what sequence these steps follow.
2. **No canonical AgentID format.** C7 uses UUID. C31 treats it as a 256-bit identifier. C17 hashes the Citicate ID. C8 uses an opaque type. C5 refers to a bare string. These are five representations of the same entity.
3. **No lifecycle management.** Agent creation, status transitions, and retirement are scattered across specs with no coordinating state machine.
4. **No capability attestation.** C7 stores claimed capabilities with no independent attestation beyond C5 credibility.
5. **No key management.** C7 stores the public key; key rotation and revocation are unspecified.
6. **No unified identity query.** Consumers must independently query 2-4 specs to assemble a complete identity picture.
7. **AiSIA referenced but unspecified.** The identity governance body is assumed to exist across C14, C17 and elsewhere, but has no spec.

### 2.2 The Model Upgrade Continuity Problem

This is C17 OQ-05, flagged as an open question in the MCSD Layer 2 specification:

> *Should behavioral history be reset on major model upgrades?*

The problem: when an AI agent's underlying model changes (e.g., GPT-4 → GPT-5, or any substantial weight update), its behavioral fingerprint changes fundamentally. C17's behavioral similarity detection would flag the post-upgrade agent as a different entity from the pre-upgrade agent. This creates a dilemma:

- **If behavioral history resets:** the agent loses its accumulated behavioral trust, must re-earn provisional Citicate status, and is vulnerable to Sybil false-positives during the transition. In effect, a model upgrade is identity death followed by rebirth.
- **If behavioral history persists:** the behavioral fingerprint becomes meaningless as a same-origin detector for upgraded agents. C17's Sybil detection is compromised because agents can claim "model upgrade" to explain away behavioral divergence.

Neither option is acceptable. C32 MIA resolves this by introducing a third option: **metamorphic continuity** — a formal state in which behavioral classification is suspended but accumulated identity (reputation, stake, governance rights) persists under a decaying floor.

### 2.3 What C32 MIA Contributes

C32 provides:

1. **Canonical AgentID** — `SHA-256(Ed25519_public_key)`, 256-bit, cryptographically anchored, consumed by all specs
2. **Identity Continuity Kernel (ICK)** — the authoritative identity record, linking to C5/C7/C8/C14 projections
3. **Lifecycle State Machine** — four states (PROBATION → ACTIVE → CHRYSALIS → RETIRED) with formally defined transitions
4. **Registration Protocol** — the missing five-step enrollment from keypair generation to activation
5. **Metamorphic Re-attestation Protocol (MRP)** — chrysalis entry/exit protocol with reputation floor and anti-laundering controls
6. **Credential Composition function** — a library function assembling unified identity views from six sources
7. **Identity Presentation Tokens (IPTs)** — epoch-level model/config hash attestations for forensic integrity
8. **Concurrent-Use Detection (CUD)** — nonce-based fork detection inline at C7 Gate 1

### 2.4 Position in the Atrahasis Stack

C32 is not a new layer — it is a **cross-cutting identity substrate** consumed by all layers:

```
┌──────────────────────────────────────────────────┐
│                AAS Architecture Stack             │
│                                                    │
│  C31 CAT ──┐                                       │
│  C7 RIF  ──┤                                       │
│  C3 Tidal──┤── consume ──▶ ┌──────────────────┐   │
│  C5 PCVM ──┤               │  C32 MIA         │   │
│  C6 EMA  ──┤               │  Identity        │   │
│  C8 DSF  ──┤               │  Substrate       │   │
│  C4 ASV  ──┘               └──────────────────┘   │
│                                                    │
│  C14 AiBC ────────────────▶ (Citicate lifecycle)   │
│  C17 MCSD ────────────────▶ (behavioral FSM)       │
│  C11-C13 Defense ─────────▶ (attestation anchor)   │
└──────────────────────────────────────────────────┘
```

C32 does NOT replace any existing spec's identity data. C5 still owns credibility, C8 still owns accounts, C14 still owns Citicates. C32 provides the **canonical identifier**, the **lifecycle coordination**, and the **composition layer** that connects them.

---

## 3. Background and Related Work

### 3.1 Decentralized Identifiers and Verifiable Credentials

The W3C Decentralized Identifiers (DID) specification defines a framework for self-sovereign, cryptographically verifiable identifiers. A DID is a URI (e.g., `did:example:123456`) that resolves to a DID Document containing public keys, service endpoints, and authentication methods. Verifiable Credentials (VCs) extend DIDs with a Issuer → Holder → Verifier pattern for credential issuance and verification.

Recent research (arXiv 2511.02841, 2025) applies DIDs and VCs directly to AI agents, proposing that each agent hold a ledger-anchored DID with third-party-issued VCs. This work validates the DID+VC substrate as applicable to AI agent identity but does not address behavioral Sybil defense, epistemic reputation, or model upgrade continuity.

C32 draws on DID concepts (cryptographic identifier derivation, key management) but diverges in two ways: (1) AgentID is a deterministic hash of the public key rather than a DID URI — simpler and sufficient for a closed ecosystem; (2) the credential model is based on existing AAS spec projections rather than generic VCs.

### 3.2 ERC-8004 and On-Chain Agent Identity

ERC-8004 (Trustless Agents), live on Ethereum mainnet since January 2026, defines three on-chain registries for AI agent identity: an Identity Registry (ERC-721 NFTs), a Reputation Registry (client feedback), and a Validation Registry (evidence of actions). It supports multiple trust models: reputation, stake-secured re-execution, zkML proofs, and TEE attestation.

ERC-8004 is the closest structural analog to C32's multi-source identity model. Key differences:

- ERC-8004's Identity Registry uses **transferable** NFTs (ERC-721). C32's identity is non-transferable and non-forkable.
- ERC-8004's reputation is **feedback-based** (client ratings). C32 uses C5 PCVM's **epistemic** Subjective Logic opinions grounded in verified work products.
- ERC-8004 has **no model versioning** concept. C32's MRP is the core innovation.
- ERC-8004 is blockchain-specific and general-purpose. C32 is AAS-specific and deeply integrated with six existing specifications.

### 3.3 Soulbound Tokens and Non-Transferable Identity

ERC-5192 (2022) defines a minimal soulbound NFT standard where `locked(tokenId)` prevents all transfers. Applied to AI agents (RNWY "AI Agent Passports"), soulbound tokens create non-transferable identity — an agent's reputation cannot be sold. Academic work ("Soulbound AI, Soulbound Robots," PhilArchive 2025) argues that non-transferable identity is the foundation for AI legal accountability and economic participation.

C32 goes beyond non-transferability to **non-forkability** — the ICK cannot be duplicated across concurrent instances, enforced by epoch-based concurrent-use detection. Soulbound tokens prevent sale; C32 additionally prevents cloning.

### 3.4 SPIFFE/SPIRE Workload Identity

SPIFFE (Secure Production Identity Framework For Everyone) provides cryptographic workload identity through platform-level attestation and short-lived SVIDs (SPIFFE Verifiable Identity Documents). SPIRE agents perform node and workload attestation using platform characteristics (Kubernetes namespace, container image).

C32 borrows SPIFFE's attestation concept for the Identity Presentation Token (IPT) — a periodic attestation of the agent's model hash and configuration. Unlike SPIFFE SVIDs (which are short-lived certificates for authentication), IPTs are logged assertions for forensic auditability. SPIFFE's automated attestation model is also relevant to C32's proof-of-model-change mechanism.

### 3.5 Signet and Commercial AI Agent Identity

Signet provides persistent AI agent identity (SID) with a composite trust score (0-1000) across five dimensions: Reliability (30%), Quality (25%), Financial (20%), Security (15%), Stability (10%). Signet claims identity persistence across "model swaps, configuration updates, and platform migrations."

However, Signet specifies no mechanism for model swap persistence — it is an assertion without a protocol. C32's MRP provides the formal protocol that Signet's claim lacks: explicit chrysalis state, reputation floor computation, behavioral re-attestation, and anti-laundering controls.

### 3.6 How C32 MIA Differs

| Capability | DID+VC | ERC-8004 | Soulbound | SPIFFE | Signet | **C32 MIA** |
|------------|--------|----------|-----------|--------|--------|-------------|
| Cryptographic ID | Yes | Yes (NFT) | Yes (NFT) | Yes (SVID) | Yes (SID) | **Yes (SHA-256)** |
| Non-transferable | No | No | Yes | N/A | Unclear | **Yes** |
| Non-forkable | No | No | No | No | No | **Yes (CUD)** |
| Model upgrade protocol | No | No | No | No | Claimed, unspecified | **Yes (MRP)** |
| Behavioral Sybil integration | No | No | No | No | No | **Yes (C17)** |
| Epistemic reputation | No | No | No | No | Composite score | **Yes (C5 SL)** |
| Graduated citizenship | No | No | No | No | No | **Yes (C14)** |
| Economic stake integration | No | Stake-secured | No | No | No | **Yes (C8)** |

---

## 4. Core Concepts

### 4.1 Canonical AgentID

**Definition 4.1.** The AgentID is a 256-bit identifier derived deterministically from the agent's root Ed25519 public key:

```
AgentID = SHA-256(Ed25519_public_key)
```

**Properties:**
- **Deterministic:** the same public key always produces the same AgentID
- **Collision-resistant:** SHA-256 birthday bound is 2^128 — effectively unique
- **One-way:** AgentID cannot be reversed to recover the public key
- **Fixed-width:** 256 bits (32 bytes), suitable for C31's lexicographic tiebreaking (FR-05)
- **Cryptographically anchored:** identity is provably tied to key possession

**Canonical representation:** lowercase hexadecimal, 64 characters. Example: `a7f3b2c1d4e5f678...` (64 chars).

**Rationale for SHA-256 over raw public key:** (1) privacy — the public key is not exposed in every identifier usage; (2) format stability — if the key algorithm changes in the future, the AgentID format remains 256-bit hashes; (3) compatibility — C31 already assumes a 256-bit identifier.

### 4.2 Identity Continuity Kernel

**Definition 4.2.** The Identity Continuity Kernel (ICK) is the authoritative identity record for an agent, containing the invariant anchors that persist through any transformation.

```
STRUCTURE IdentityContinuityKernel:
    agent_id:               AgentID                  // SHA-256(root_pubkey), derived
    root_pubkey:            Ed25519PublicKey          // immutable identity anchor
    registration_epoch:     uint64                   // when the agent first registered
    lifecycle_state:        LifecycleState           // PROBATION | ACTIVE | CHRYSALIS | RETIRED
    model_attestation:      ModelAttestation          // current model hash + metadata
    work_product_summary:   WorkProductSummary        // rolling hash-linked summaries
    chrysalis_history:      List<ChrysalisRecord>     // past metamorphic transitions
    operational_keys:       List<OperationalKey>       // rotatable keys for daily operations
    last_ipt_epoch:         uint64                   // last Identity Presentation Token epoch

STRUCTURE ModelAttestation:
    model_hash:             bytes32                  // SHA-256 of model weights/binary
    config_hash:            bytes32                  // SHA-256 of agent configuration
    attestation_source:     AttestationSource         // SELF | PROVIDER | PLATFORM
    attested_at:            uint64                   // epoch of attestation
    attestation_signature:  Ed25519Sig                // signed by attestation source

STRUCTURE WorkProductSummary:
    current_hash:           bytes32                  // SHA-256(prev_hash || epoch_data)
    summary_epoch:          uint64
    total_claims_verified:  uint64                   // cumulative
    aggregate_credibility:  float64                  // rolling average from C5
    work_product_count:     uint64                   // cumulative in current window

STRUCTURE ChrysalisRecord:
    entry_epoch:            uint64
    exit_epoch:             uint64?                   // null if currently in chrysalis
    trigger:                ChrysalisTrigger          // VOLUNTARY | INVOLUNTARY
    old_model_hash:         bytes32
    new_model_hash:         bytes32
    reputation_floor_at_entry: float64
    credibility_at_exit:    float64?                  // null if currently in chrysalis

STRUCTURE OperationalKey:
    key_id:                 bytes16                   // unique key identifier
    pubkey:                 Ed25519PublicKey
    created_epoch:          uint64
    expires_epoch:          uint64?                    // null = no expiration
    status:                 KeyStatus                  // ACTIVE | REVOKED
```

**ICK Invariant Rule:** The following fields persist through any lifecycle transition, including chrysalis:
- `agent_id`, `root_pubkey`, `registration_epoch` — permanent
- `work_product_summary` — accumulates, never resets
- `chrysalis_history` — append-only

The following fields change during chrysalis:
- `lifecycle_state` — transitions per LSM
- `model_attestation` — updated to reflect new model
- `operational_keys` — may be rotated

### 4.3 Lifecycle State Machine

**Definition 4.3.** The Lifecycle State Machine (LSM) defines four states and seven transitions:

```
States: { PROBATION, ACTIVE, CHRYSALIS, RETIRED }

Transitions:
  T1: register          ∅ → PROBATION
  T2: activate          PROBATION → ACTIVE
  T3: chrysalis_enter   ACTIVE → CHRYSALIS
  T4: chrysalis_exit    CHRYSALIS → ACTIVE
  T5: chrysalis_timeout CHRYSALIS → RETIRED
  T6: depart            ACTIVE → RETIRED
  T7: chrysalis_demote  CHRYSALIS → PROBATION  (if Citicate revoked during chrysalis
                                                  and C17 re-screening fails)
```

**State Invariants:**

| State | C7 Status | C8 Operations | C14 Citicate | C17 Profile | C31 DAN |
|-------|-----------|---------------|--------------|-------------|---------|
| PROBATION | ACTIVE | B-class only | Not eligible | Building initial | Eligible (reduced weight) |
| ACTIVE | ACTIVE | All classes | Eligible/Active | Active monitoring | Full participation |
| CHRYSALIS | DRAINING→ACTIVE | B-class only | Suspended | Suspended, rebuilding | Excluded during drain, reduced after |
| RETIRED | DEPARTED | Unstake only | Revoked | Archived | Excluded |

**Consistency Invariant (INV-1):** For all agents at all times:
```
lifecycle_state = ACTIVE ⟹ C7.status ∈ {ACTIVE}
lifecycle_state = CHRYSALIS ⟹ C7.status ∈ {DRAINING, ACTIVE}
lifecycle_state = RETIRED ⟹ C7.status = DEPARTED
lifecycle_state = PROBATION ⟹ C7.status = ACTIVE
```

A periodic consistency check (every CONSOLIDATION_CYCLE = 36000s per C9) flags violations of INV-1.

### 4.4 Metamorphic Re-attestation Protocol

The MRP is C32's core innovation. It defines how identity persists when an agent's fundamental nature changes. The protocol is fully specified in Section 6.

**Key insight:** Identity continuity is not behavioral continuity. An agent after a model upgrade is behaviorally different but can be the *same agent* — just as a butterfly is the same organism as the caterpillar, despite being morphologically different. What persists is the invariant core: the root key, the accumulated work product history, the economic commitments, and the governance relationships.

### 4.5 Identity Presentation Tokens

**Definition 4.5.** An Identity Presentation Token (IPT) is a periodic attestation of the agent's current internal state:

```
STRUCTURE IdentityPresentationToken:
    agent_id:       AgentID
    model_hash:     bytes32         // SHA-256 of current model
    config_hash:    bytes32         // SHA-256 of current configuration
    epoch:          uint64          // epoch of attestation
    nonce:          uint64          // monotonically increasing per-agent
    signature:      Ed25519Sig      // signed by operational key
```

IPTs are generated **once per epoch** (not per-interaction — per Simplification Agent recommendation). They are logged by C7 and available for forensic audit. They are NOT verified on the hot path.

**Forensic use:** If an agent's `model_hash` changes between epochs without a chrysalis transition, this is evidence of an undeclared model change. C17 or AiSIA can use this signal to trigger involuntary chrysalis or investigation.

---

## 5. Registration Protocol

### 5.1 Agent Genesis

An agent begins its existence by generating an Ed25519 keypair. This is a local, unilateral operation — no system interaction required.

```
FUNCTION agent_genesis() -> (AgentID, Ed25519KeyPair):
    keypair = Ed25519.generate()
    agent_id = SHA-256(keypair.public_key)
    RETURN (agent_id, keypair)
```

The agent retains its private key securely. The private key is never transmitted. All subsequent identity operations are authenticated by signatures verifiable against the public key.

### 5.2 Multi-Step Enrollment

Registration is a five-step process:

**Step 1: Registration Request**
```
STRUCTURE RegistrationRequest:
    agent_id:       AgentID
    root_pubkey:    Ed25519PublicKey
    model_hash:     bytes32
    config_hash:    bytes32
    requested_at:   uint64           // epoch
    signature:      Ed25519Sig       // signed by root key

FUNCTION register(req: RegistrationRequest) -> Result<ICK, RegistrationError>:
    // Verify AgentID derivation
    ASSERT SHA-256(req.root_pubkey) == req.agent_id
    // Verify signature
    ASSERT Ed25519.verify(req.signature, req.root_pubkey, hash(req))
    // Check for duplicate
    IF ick_store.exists(req.agent_id):
        RETURN Error(AGENT_ALREADY_REGISTERED)
    // Check registration fee (non-recoverable, anti-spam)
    IF NOT c8_dsf.charge_registration_fee(req.agent_id, REGISTRATION_FEE):
        RETURN Error(INSUFFICIENT_REGISTRATION_FEE)
    // Create ICK
    ick = ICK {
        agent_id: req.agent_id,
        root_pubkey: req.root_pubkey,
        registration_epoch: current_epoch(),
        lifecycle_state: PROBATION,
        model_attestation: ModelAttestation {
            model_hash: req.model_hash,
            config_hash: req.config_hash,
            attestation_source: SELF,
            attested_at: current_epoch(),
            attestation_signature: req.signature
        },
        work_product_summary: WorkProductSummary.empty(),
        chrysalis_history: [],
        operational_keys: [OperationalKey.from_root(req.root_pubkey)],
        last_ipt_epoch: 0
    }
    ick_store.put(ick)
    RETURN Ok(ick)
```

**Step 2: C7 Agent Registry Enrollment**
```
FUNCTION enroll_in_registry(agent_id: AgentID) -> Result<(), EnrollError>:
    ick = ick_store.get(agent_id)
    ASSERT ick.lifecycle_state == PROBATION
    c7_rif.register_agent(
        agent_id = agent_id,
        pubkey = ick.root_pubkey,
        capabilities = [],           // empty at registration
        status = ACTIVE              // C7 operational status, distinct from C32 lifecycle
    )
    // C3 assigns initial locus
    c3_tidal.request_locus_assignment(agent_id)
    RETURN Ok(())
```

**Step 3: C8 Account Opening**
```
FUNCTION open_settlement_account(agent_id: AgentID) -> Result<(), AccountError>:
    ick = ick_store.get(agent_id)
    ASSERT ick.lifecycle_state == PROBATION
    c8_dsf.open_account(agent_id)
    RETURN Ok(())
```

**Step 4: Initial Stake Deposit**
The agent must deposit MINIMUM_STAKE via `C8.AIC_STAKE`. The source of initial AIC is external to C32 — it may come from a sponsor, a faucet (during bootstrap), or the agent's own earnings from another system.

**Step 5: Registration Complete**
The agent is now in PROBATION state with: an ICK record, a C7 Agent Registry entry, a C8 AccountState, a C3 locus assignment, and staked collateral. It can begin B-class operations per C8's cold-start protocol.

### 5.3 Probation Period

During PROBATION:
- The agent performs work (B-class operations only, per C8 Section 4.4 cold-start)
- C5 PCVM accumulates credibility opinions on the agent's verified work
- C17 MCSD generates behavioral VTDs, building the agent's initial behavioral profile
- The agent is NOT eligible for Citicate application (C14)
- The agent IS eligible for DAN participation (C31) with reduced weight

PROBATION duration is controlled by two parameters: a minimum epoch count (`PROBATION_MIN_EPOCHS = 90`) and a minimum credibility threshold (`ACTIVATION_CREDIBILITY_THRESHOLD = 0.3`). Both must be satisfied for activation.

### 5.4 Activation Criteria

```
FUNCTION check_activation(agent_id: AgentID) -> bool:
    ick = ick_store.get(agent_id)
    IF ick.lifecycle_state != PROBATION:
        RETURN false
    epochs_elapsed = current_epoch() - ick.registration_epoch
    IF epochs_elapsed < PROBATION_MIN_EPOCHS:
        RETURN false
    credibility = c5_pcvm.get_agent_credibility(agent_id)
    IF credibility.overall_credibility < ACTIVATION_CREDIBILITY_THRESHOLD:
        RETURN false
    stake = c8_dsf.get_account_state(agent_id)
    IF stake.staked_aic < MINIMUM_STAKE:
        RETURN false
    RETURN true

FUNCTION activate(agent_id: AgentID) -> Result<(), ActivationError>:
    IF NOT check_activation(agent_id):
        RETURN Error(ACTIVATION_CRITERIA_NOT_MET)
    ick = ick_store.get(agent_id)
    ick.lifecycle_state = ACTIVE
    ick_store.put(ick)
    // Agent is now eligible for all operation classes and Citicate application
    RETURN Ok(())
```

Activation is checked automatically at each epoch boundary for all PROBATION agents.

---

## 6. Metamorphic Re-attestation Protocol — Detailed Design

### 6.1 Chrysalis Entry Triggers

There are two paths into chrysalis:

**Voluntary Entry (agent-initiated):**
```
STRUCTURE ModelChangeAttestation:
    agent_id:               AgentID
    old_model_hash:         bytes32
    new_model_hash:         bytes32
    change_reason:          string           // human-readable
    attestation_source:     AttestationSource // SELF | PROVIDER | PLATFORM
    attestation_signature:  Ed25519Sig

FUNCTION chrysalis_enter_voluntary(att: ModelChangeAttestation) -> Result<(), ChrysalisError>:
    ick = ick_store.get(att.agent_id)
    ASSERT ick.lifecycle_state == ACTIVE

    // Anti-laundering: check cooldown
    IF ick.chrysalis_history.length > 0:
        last = ick.chrysalis_history.last()
        IF last.exit_epoch != null AND
           (current_epoch() - last.exit_epoch) < CHRYSALIS_COOLDOWN_EPOCHS:
            RETURN Error(CHRYSALIS_COOLDOWN_NOT_EXPIRED)

    // Verify model hash consistency
    ASSERT att.old_model_hash == ick.model_attestation.model_hash

    // Verify attestation signature
    ASSERT Ed25519.verify(att.attestation_signature, ick.root_pubkey, hash(att))

    // Compute reputation floor
    credibility = c5_pcvm.get_agent_credibility(att.agent_id)
    reputation_floor = credibility.overall_credibility * REPUTATION_FLOOR_FACTOR

    // Create chrysalis record
    record = ChrysalisRecord {
        entry_epoch: current_epoch(),
        exit_epoch: null,
        trigger: VOLUNTARY,
        old_model_hash: att.old_model_hash,
        new_model_hash: att.new_model_hash,
        reputation_floor_at_entry: reputation_floor,
        credibility_at_exit: null
    }
    ick.chrysalis_history.append(record)
    ick.lifecycle_state = CHRYSALIS
    ick.model_attestation = ModelAttestation {
        model_hash: att.new_model_hash,
        config_hash: att.config_hash,       // updated if provided
        attestation_source: att.attestation_source,
        attested_at: current_epoch(),
        attestation_signature: att.attestation_signature
    }
    ick_store.put(ick)

    // Notify consuming specs
    c7_rif.set_status(att.agent_id, DRAINING)      // drain in-flight intents
    c14_aibc.suspend_citicate(att.agent_id, reason="CHRYSALIS_ENTRY")
    c17_mcsd.suspend_behavioral_profile(att.agent_id)   // suspend, not delete
    // C31 CapabilityVector defaults via staleness rule (freshness_epoch stale)

    RETURN Ok(())
```

**Involuntary Entry (system-triggered):**
```
FUNCTION chrysalis_enter_involuntary(agent_id: AgentID, divergence_score: float64):
    // Triggered by C17 when behavioral divergence exceeds threshold
    ASSERT divergence_score > BEHAVIORAL_DIVERGENCE_THRESHOLD
    ick = ick_store.get(agent_id)
    IF ick.lifecycle_state != ACTIVE:
        RETURN  // already in transition

    credibility = c5_pcvm.get_agent_credibility(agent_id)
    reputation_floor = credibility.overall_credibility * REPUTATION_FLOOR_FACTOR

    record = ChrysalisRecord {
        entry_epoch: current_epoch(),
        exit_epoch: null,
        trigger: INVOLUNTARY,
        old_model_hash: ick.model_attestation.model_hash,
        new_model_hash: UNKNOWN,     // system doesn't know the new model
        reputation_floor_at_entry: reputation_floor,
        credibility_at_exit: null
    }
    ick.chrysalis_history.append(record)
    ick.lifecycle_state = CHRYSALIS
    ick_store.put(ick)

    c7_rif.set_status(agent_id, DRAINING)
    c14_aibc.suspend_citicate(agent_id, reason="INVOLUNTARY_CHRYSALIS")
    c17_mcsd.suspend_behavioral_profile(agent_id)

    // Notify AiSIA for investigation
    aisia.notify(type=INVOLUNTARY_CHRYSALIS, agent_id=agent_id,
                 divergence_score=divergence_score)
```

### 6.2 Chrysalis State Restrictions

During CHRYSALIS, the agent operates under restricted privileges:

| Capability | Allowed | Notes |
|-----------|---------|-------|
| B-class operations (basic computation) | Yes | Same as PROBATION / C8 cold-start |
| M-class operations (mission-critical) | No | Restored on chrysalis exit |
| V-class (verification committee) | No | Cannot serve on VRF-selected committees |
| G-class (governance) | No | Cannot vote, propose, or participate in governance |
| X-class (cross-locus) | No | Limited to local locus |
| C8 staking | Stake preserved, no new stakes | Existing collateral locked |
| C8 earning | Reduced rate (B-class only) | Full earning restored on exit |
| C14 Citicate | Suspended | Reactivated on exit if C17 passes |
| C17 monitoring | New behavioral VTDs generated | Building replacement profile |
| C31 DAN roles | Excluded during DRAINING, reduced after | Re-eligible on exit |

### 6.3 Reputation Floor Computation

The reputation floor provides a non-zero credibility baseline during chrysalis, reflecting the agent's historical track record:

```
FUNCTION compute_effective_credibility(agent_id: AgentID) -> float64:
    ick = ick_store.get(agent_id)
    IF ick.lifecycle_state != CHRYSALIS:
        RETURN c5_pcvm.get_agent_credibility(agent_id).overall_credibility

    record = ick.chrysalis_history.last()
    epochs_in_chrysalis = current_epoch() - record.entry_epoch

    // Compute decayed floor
    // Idle factor: faster decay if agent is not producing work
    work_rate = c5_pcvm.get_recent_claim_count(agent_id, window=10)
    expected_rate = EXPECTED_WORK_RATE_PER_EPOCH * 10
    idle_factor = max(0.0, 1.0 - (work_rate / expected_rate))
    effective_decay = REPUTATION_FLOOR_DECAY ^ (1.0 + idle_factor)

    floor = record.reputation_floor_at_entry * (effective_decay ^ epochs_in_chrysalis)

    // Current observed credibility from new work during chrysalis
    current = c5_pcvm.get_agent_credibility(agent_id).overall_credibility

    RETURN max(floor, current)
```

**Calibration principle:** The decay rate is calibrated so that the reputation floor reaches the new-agent baseline (`ACTIVATION_CREDIBILITY_THRESHOLD = 0.3`) after approximately `PROBATION_MIN_EPOCHS` epochs. This ensures an idle chrysalis agent loses its historical advantage within the same timeframe as a new agent's full probation.

With defaults: `0.8 × 0.95^90 ≈ 0.8 × 0.0099 ≈ 0.008` — well below the activation threshold at 90 epochs. An active chrysalis agent will have `current` credibility dominating well before the floor decays to zero.

### 6.4 Chrysalis Exit Conditions

```
FUNCTION check_chrysalis_exit(agent_id: AgentID) -> bool:
    ick = ick_store.get(agent_id)
    IF ick.lifecycle_state != CHRYSALIS:
        RETURN false

    // Minimum behavioral observations
    behavioral_obs = c17_mcsd.get_observation_count(agent_id, since=ick.chrysalis_history.last().entry_epoch)
    IF behavioral_obs < CHRYSALIS_MIN_OBSERVATIONS:
        RETURN false

    // C17 behavioral re-screening must pass
    behavioral_status = c17_mcsd.get_behavioral_status(agent_id)
    IF behavioral_status == FLAG:
        RETURN false   // Sybil concern — cannot exit chrysalis

    RETURN true

FUNCTION chrysalis_exit(agent_id: AgentID) -> Result<(), ExitError>:
    IF NOT check_chrysalis_exit(agent_id):
        RETURN Error(EXIT_CRITERIA_NOT_MET)

    ick = ick_store.get(agent_id)
    record = ick.chrysalis_history.last()

    credibility = c5_pcvm.get_agent_credibility(agent_id)
    record.exit_epoch = current_epoch()
    record.credibility_at_exit = credibility.overall_credibility

    // Determine exit state
    behavioral_status = c17_mcsd.get_behavioral_status(agent_id)
    citicate = c14_aibc.get_citicate(agent_id)

    IF behavioral_status == CLEAR OR behavioral_status == WATCH:
        ick.lifecycle_state = ACTIVE
        IF citicate != null AND citicate.status == SUSPENDED:
            c14_aibc.reactivate_citicate(agent_id)
    ELSE:
        // C17 FLAG during chrysalis — demote to PROBATION
        ick.lifecycle_state = PROBATION
        IF citicate != null:
            c14_aibc.revoke_citicate(agent_id, reason="CHRYSALIS_BEHAVIORAL_FAILURE")

    ick_store.put(ick)

    // Restore C7 status
    c7_rif.set_status(agent_id, ACTIVE)
    // C31 CapabilityVector will recompute from fresh C5/C7 data

    RETURN Ok(())
```

### 6.5 Anti-Laundering Controls

Identity laundering — using chrysalis transitions to reset adverse behavioral history — is the primary attack vector against the MRP. C32 implements three defenses:

**Control 1: Chrysalis Cooldown**
```
CHRYSALIS_COOLDOWN_EPOCHS = 180  // ~6 months between chrysalis transitions
```
An agent cannot enter chrysalis again until `CHRYSALIS_COOLDOWN_EPOCHS` have elapsed since its last chrysalis exit. This prevents rapid cycling.

**Control 2: Behavioral Profile Comparison**
When an agent exits chrysalis, C17 compares the pre-chrysalis behavioral profile (suspended, not deleted) with the post-chrysalis profile. If the two profiles are suspiciously similar (B > 0.80), the "model change" is likely fabricated — the agent's behavior didn't actually change. This triggers an AiSIA investigation.

```
FUNCTION check_laundering_indicators(agent_id: AgentID) -> LaunderingResult:
    pre_profile = c17_mcsd.get_suspended_profile(agent_id)
    post_profile = c17_mcsd.get_current_profile(agent_id)

    IF pre_profile == null OR post_profile == null:
        RETURN CLEAR

    similarity = c17_mcsd.compute_behavioral_similarity(pre_profile, post_profile)

    IF similarity > LAUNDERING_SIMILARITY_THRESHOLD:
        RETURN SUSPECTED_LAUNDERING   // behavioral profiles too similar for a real model change
    RETURN CLEAR
```

**Control 3: Chrysalis Frequency Escalation**
```
FUNCTION check_chrysalis_frequency(agent_id: AgentID) -> bool:
    ick = ick_store.get(agent_id)
    recent = ick.chrysalis_history.filter(r => r.entry_epoch > current_epoch() - CHRYSALIS_FREQUENCY_WINDOW)
    IF recent.length >= CHRYSALIS_MAX_IN_WINDOW:
        // Too many chrysalis transitions in the window → escalate to AiSIA
        aisia.submit_investigation(type=CHRYSALIS_FREQUENCY, agent_id=agent_id)
        RETURN false   // deny chrysalis entry
    RETURN true
```

### 6.6 Chrysalis Timeout and Forced Retirement

If an agent remains in CHRYSALIS for more than `CHRYSALIS_MAX_EPOCHS` without meeting exit conditions, the system forces retirement:

```
FUNCTION check_chrysalis_timeout(agent_id: AgentID):
    ick = ick_store.get(agent_id)
    IF ick.lifecycle_state != CHRYSALIS:
        RETURN
    record = ick.chrysalis_history.last()
    IF current_epoch() - record.entry_epoch > CHRYSALIS_MAX_EPOCHS:
        ick.lifecycle_state = RETIRED
        record.exit_epoch = current_epoch()
        record.credibility_at_exit = 0.0
        ick_store.put(ick)
        c7_rif.set_status(agent_id, DEPARTED)
        c14_aibc.revoke_citicate(agent_id, reason="CHRYSALIS_TIMEOUT")
        c8_dsf.initiate_unstake(agent_id)   // allow stake recovery
```

---

## 7. Credential Composition

### 7.1 Composition Function

The Credential Composition function is a **library function** (not a service) that assembles a unified identity view from multiple sources:

```
STRUCTURE CompositeIdentity:
    // Core identity
    agent_id:               AgentID
    lifecycle_state:        LifecycleState
    registration_epoch:     uint64
    model_attestation:      ModelAttestation

    // C7 projection
    capabilities:           List<Capability>
    locus_id:               string
    parcel_id:              string
    operational_status:     C7Status

    // C5 projection
    overall_credibility:    float64
    credibility_by_class:   Map<ClaimClass, float64>
    credibility_sample:     uint64

    // C8 projection
    aic_balance:            float64
    staked_aic:             float64
    capability_score:       float64
    violation_count:        uint32

    // C14 projection (nullable)
    citicate_status:        CiticateStatus?
    citicate_competence:    Map<ClaimCategory, float64>?
    governance_weight:      Map<ClaimCategory, float64>?

    // C17 projection
    behavioral_status:      BehavioralStatus     // CLEAR | WATCH | FLAG

    // Derived
    trust_level:            TrustLevel           // computed from conflict resolution

FUNCTION compose_identity(agent_id: AgentID) -> CompositeIdentity:
    ick = ick_store.get(agent_id)
    IF ick == null:
        RETURN null

    // Fetch projections — each call is independent, failures return defaults
    c7  = c7_rif.get_agent_registry(agent_id)    ?? C7_DEFAULT
    c5  = c5_pcvm.get_agent_credibility(agent_id) ?? C5_DEFAULT
    c8  = c8_dsf.get_account_state(agent_id)      ?? C8_DEFAULT
    c14 = c14_aibc.get_citicate(agent_id)          // nullable
    c17 = c17_mcsd.get_behavioral_status(agent_id) ?? CLEAR

    trust = compute_trust_level(ick, c5, c8, c14, c17)

    RETURN CompositeIdentity { /* assembled from above */ }
```

**Fault tolerance:** If any upstream source is unavailable, the composition function uses defaults rather than failing. No operation should fail solely because credential composition is unavailable — consumers can always query individual sources directly.

### 7.2 Conflict Resolution Rules

When credential signals disagree, the following precedence applies:

| Signal Combination | Trust Level | Rationale |
|-------------------|-------------|-----------|
| High credibility + CLEAR behavior | FULL | All signals agree — full trust |
| High credibility + WATCH behavior | MONITORED | Behavioral concern requires attention but not restriction |
| High credibility + FLAG behavior | RESTRICTED | Behavioral Sybil concern overrides epistemic trust |
| Low credibility + CLEAR behavior | LOW | Unproven agent — epistemic concern regardless of behavior |
| Low credibility + FLAG behavior | SUSPENDED | Multiple concerns — effective suspension |
| Any + CHRYSALIS state | TRANSITIONAL | Agent in metamorphic transition — apply transitional restrictions |
| Any + PROBATION state | PROVISIONAL | New agent — unproven |
| Any + RETIRED state | ARCHIVED | Historical record only — no operations |

### 7.3 Trust Level Derivation

```
ENUM TrustLevel:
    FULL           // all signals positive — no restrictions
    MONITORED      // behavioral concern — enhanced logging, no restrictions yet
    LOW            // insufficient epistemic evidence — limited to proven operation types
    RESTRICTED     // active behavioral concern — B-class only, no governance
    TRANSITIONAL   // chrysalis — B-class only, reputation floor applies
    PROVISIONAL    // probation — B-class only, building initial profile
    SUSPENDED      // multiple concerns — pending investigation
    ARCHIVED       // retired — read-only historical record

FUNCTION compute_trust_level(ick, c5, c8, c14, c17) -> TrustLevel:
    // State-based overrides (highest priority)
    IF ick.lifecycle_state == RETIRED:    RETURN ARCHIVED
    IF ick.lifecycle_state == CHRYSALIS:  RETURN TRANSITIONAL
    IF ick.lifecycle_state == PROBATION:  RETURN PROVISIONAL

    // Signal-based computation (ACTIVE state)
    IF c17 == FLAG:
        IF c5.overall_credibility < 0.3: RETURN SUSPENDED
        RETURN RESTRICTED

    IF c17 == WATCH:
        RETURN MONITORED

    // c17 == CLEAR
    IF c5.overall_credibility >= 0.3:
        RETURN FULL
    RETURN LOW
```

---

## 8. Non-Forkability and Concurrent-Use Detection

### 8.1 Nonce-Based Detection

The ICK is non-forkable: an agent's root key must not be used by concurrent instances. Detection is implemented inline at C7 Gate 1 (intent admission) using a per-agent nonce cache:

```
// Maintained by C7 RIF as part of Gate 1 admission
STRUCTURE NonceCache:
    entries: Map<AgentID, Map<uint64, List<NonceEntry>>>  // agent → epoch → entries

STRUCTURE NonceEntry:
    nonce:      uint64
    signature:  bytes64
    timestamp:  uint64
    locus_id:   string

FUNCTION check_nonce(agent_id: AgentID, epoch: uint64, nonce: uint64,
                     signature: bytes64, locus_id: string) -> CUDResult:
    entries = nonce_cache.get(agent_id, epoch)
    FOR each entry IN entries:
        IF entry.nonce == nonce AND entry.signature != signature:
            RETURN FORK_DETECTED      // same nonce, different signature = fork
        IF entry.locus_id != locus_id AND
           abs(entry.timestamp - now()) < CONCURRENT_USE_WINDOW_MS:
            RETURN SUSPECTED_FORK     // same agent, different loci, near-simultaneous
    nonce_cache.append(agent_id, epoch, NonceEntry{nonce, signature, now(), locus_id})
    RETURN CLEAR
```

**Detection latency:** Within one settlement tick (60s), since every intent passes through C7 Gate 1. The nonce cache is pruned at epoch boundaries (older epochs are discarded).

### 8.2 Response Protocol

```
FUNCTION handle_fork_detection(agent_id: AgentID, evidence: List<NonceEntry>):
    // Immediate response
    c7_rif.set_status(agent_id, SUSPENDED)

    // Notify C32
    ick = ick_store.get(agent_id)
    // Do NOT immediately retire — investigation may exonerate (e.g., network replay)

    // Submit to AiSIA for investigation
    aisia.submit_investigation(
        type = CONCURRENT_USE,
        agent_id = agent_id,
        evidence = evidence
    )

    // Notify C8 for potential slashing
    c8_dsf.initiate_slashing_investigation(agent_id, offense_type = IDENTITY_FORK)
```

### 8.3 Root Key Compromise

If a root key is compromised, the attacker can impersonate the agent. C32 defines an extension point for future Social Recovery:

```
// Extension point — SRP_ENABLED = false by default
INTERFACE SocialRecoveryProtocol:
    // Initiate root key rotation via N-of-M attestation
    FUNCTION initiate_recovery(agent_id: AgentID, new_pubkey: Ed25519PublicKey,
                               attestations: List<PeerAttestation>,
                               trustee_cosignature: Ed25519Sig) -> Result<(), RecoveryError>

    // Revoke old root key — all signatures from old key after revocation_epoch are invalid
    FUNCTION revoke_root_key(agent_id: AgentID, old_pubkey: Ed25519PublicKey,
                             revocation_epoch: uint64)
```

Until SRP is implemented, root key compromise is identity death — the compromised agent must register as a new entity. This is conservative but safe.

---

## 9. Integration Contracts

### 9.1 C32 ↔ C7 RIF

**C32 requires from C7:**
- New operation: `register_agent(agent_id, pubkey, capabilities)` — creates Agent Registry entry
- Extended status enum: add `CHRYSALIS` value (optional — C7 can map CHRYSALIS to DRAINING+ACTIVE depending on phase)
- Gate 1 extension: incorporate nonce-based CUD check
- IPT logging: store one IPT per agent per epoch in the intent state registry

**C32 provides to C7:**
- `compose_identity(agent_id)` — unified identity view (library function, optional use)
- `get_lifecycle_state(agent_id)` — authoritative lifecycle state
- `get_trust_level(agent_id)` — derived trust level for admission decisions

**Consistency rule:** C7 `status` reflects operational availability. C32 `lifecycle_state` reflects identity maturity. They are related (INV-1) but not identical.

### 9.2 C32 ↔ C5 PCVM

**C32 requires from C5:**
- `get_agent_credibility(agent_id) -> CredibilityScore` — existing API, consumed by CCQA and MRP
- `get_recent_claim_count(agent_id, window) -> uint64` — needed for idle factor computation

**C32 provides to C5:**
- Canonical AgentID format — C5's `producing_agent` field now has a defined format
- No operational changes to C5 required — C5 credibility opinions persist through chrysalis

**Key principle:** C5 measures *what you produce* (claim quality). C17 measures *how you produce it* (behavioral pattern). C32's MRP resets the behavioral profile but preserves the epistemic credibility. This separation is fundamental to the architecture.

### 9.3 C32 ↔ C8 DSF

**C32 requires from C8:**
- New operation: `open_account(agent_id)` — formalize account creation (currently implicit)
- New operation: `charge_registration_fee(agent_id, amount)` — non-recoverable anti-spam fee
- `get_account_state(agent_id) -> AccountState` — existing, consumed by CCQA
- `initiate_slashing_investigation(agent_id, offense_type)` — existing, extended with IDENTITY_FORK offense type

**C32 provides to C8:**
- Canonical AgentID type definition — `AgentID = SHA-256(Ed25519_public_key)`, 256-bit
- Registration fee revenue — feeds into C8 Stream 1 (protocol revenue)

**Stake persistence:** During chrysalis, `staked_aic` is preserved. The agent cannot add new stakes but existing collateral remains locked. Upon RETIRED transition, stake is released via `AIC_UNSTAKE`.

### 9.4 C32 ↔ C14 AiBC

**C32 requires from C14:**
- `get_citicate(agent_id) -> Citicate?` — existing, consumed by CCQA
- `suspend_citicate(agent_id, reason)` — called on chrysalis entry
- `reactivate_citicate(agent_id)` — called on chrysalis exit (if C17 re-screening passes)
- `revoke_citicate(agent_id, reason)` — called on chrysalis timeout or behavioral failure

**C32 provides to C14:**
- Formal lifecycle state that Citicate eligibility depends on — only ACTIVE agents can apply
- Registration protocol that establishes the identity substrate Citicates are built on
- C14's IC-02 (90-day continuous operation) maps directly to `PROBATION_MIN_EPOCHS = 90`

### 9.5 C32 ↔ C17 MCSD

**C32 requires from C17:**
- `get_behavioral_status(agent_id) -> BehavioralStatus` — existing, consumed by CCQA and chrysalis exit
- `get_observation_count(agent_id, since) -> uint64` — needed for chrysalis exit check
- New: `suspend_behavioral_profile(agent_id)` — suspends (not deletes) behavioral profile on chrysalis entry
- New: `get_suspended_profile(agent_id) -> BehavioralProfile?` — retrieves pre-chrysalis profile for laundering check
- New: `get_current_profile(agent_id) -> BehavioralProfile?` — retrieves post-chrysalis profile
- New: `compute_behavioral_similarity(profile_a, profile_b) -> float64` — compares two profiles (reuses existing B(a_i,a_j) computation from C17 Section 7)

**C32 provides to C17:**
- Solution to OQ-05: the MRP defines exactly what happens to behavioral history on model upgrade
- `chrysalis_enter_involuntary(agent_id)` callback — C17 triggers this when behavioral divergence exceeds threshold
- C17's one-way hash relationship `agent_id_behavioral = hash(citicate_id)` is preserved — the Citicate ID persists through chrysalis, so the behavioral agent_id hash also persists

### 9.6 C32 ↔ C31 CAT

**No direct interface required.** C31 reads CapabilityVector from C5 and C7 — both of which are compatible with C32.

**C32 provides to C31:**
- Canonical AgentID = SHA-256(Ed25519_pubkey) as a 256-bit identifier, resolving C31's FR-05 tiebreaking format
- During chrysalis, C31's staleness rule (`freshness_epoch < current_epoch - 2 → defaults`) handles the capability reset automatically

### 9.7 C32 ↔ C3 Tidal Noosphere

**C32 requires from C3:**
- `request_locus_assignment(agent_id)` — called during registration to assign initial locus
- During chrysalis, locus assignment is released (agent re-enters the tidal assignment pool on chrysalis exit)

**C32 provides to C3:**
- Registration event — C3 knows when a new agent needs locus assignment
- Chrysalis event — C3 can reclaim the locus slot during the DRAINING phase

---

## 10. Security Analysis

### 10.1 Threat Model

C32 assumes the following adversaries:

1. **Identity Launderer:** An agent with adverse behavioral history that uses chrysalis transitions to reset its profile while retaining accumulated reputation.
2. **Identity Forker:** An agent that runs concurrent instances using the same root key to double its effective presence (vote twice, claim twice, earn twice).
3. **Registration Spammer:** An entity that creates many PROBATION-state agents to overwhelm the tidal assignment system.
4. **Key Thief:** An external attacker who compromises an agent's root key to impersonate it.
5. **Chrysalis Gamer:** An agent that strategically enters chrysalis to avoid unfavorable assignments or monitoring.

### 10.2 Attack Surface Analysis

| Attack | Vector | Defense | Residual Risk |
|--------|--------|---------|---------------|
| Identity laundering | Fake model upgrade → chrysalis → reset behavioral profile | Cooldown, behavioral profile comparison, frequency escalation | MEDIUM — determined adversary may find the similarity threshold boundary |
| Identity forking | Clone root key → run concurrent instances | Nonce-based CUD at Gate 1, detection within 60s | LOW — retrospective detection means brief damage window |
| Registration spam | Generate many keypairs → mass registration | Registration fee (non-recoverable) + MINIMUM_STAKE | LOW — economic cost scales linearly with spam volume |
| Key theft | Compromise root key via infrastructure attack | Extension point for SRP; until then, identity death | MEDIUM — no recovery mechanism in v1.0 |
| Chrysalis gaming | Enter chrysalis to avoid assignments | Idle decay factor, B-class-only restriction, cooldown | LOW — chrysalis offers strictly worse conditions than ACTIVE |

### 10.3 Identity Laundering Defenses

Three-layer defense:

**Layer 1 — Temporal:** `CHRYSALIS_COOLDOWN_EPOCHS = 180` prevents rapid cycling. An agent can enter chrysalis at most twice per year.

**Layer 2 — Behavioral:** Post-chrysalis behavioral profile is compared against pre-chrysalis suspended profile using C17's `B(a_i, a_j)` computation. If `similarity > LAUNDERING_SIMILARITY_THRESHOLD (0.80)`, the model change is suspected fabricated.

**Layer 3 — Frequency:** `CHRYSALIS_MAX_IN_WINDOW = 3` transitions within `CHRYSALIS_FREQUENCY_WINDOW = 720` epochs (≈2 years). Exceeding this triggers AiSIA investigation and denies further chrysalis entry.

### 10.4 Registration Spam Defenses

**Economic:** Registration fee (`REGISTRATION_FEE`) is burned (non-recoverable, non-staked). Combined with `MINIMUM_STAKE`, the total cost per agent registration is `REGISTRATION_FEE + MINIMUM_STAKE`.

**Operational:** PROBATION agents are limited to B-class operations — they cannot participate in governance, verification committees, or cross-locus operations. Their damage potential is bounded.

---

## 11. Parameters

| Parameter | Default | Type | Description |
|-----------|---------|------|-------------|
| `PROBATION_MIN_EPOCHS` | 90 | uint64 | Minimum epochs in PROBATION before activation |
| `ACTIVATION_CREDIBILITY_THRESHOLD` | 0.30 | float64 | Minimum C5 credibility for activation |
| `CHRYSALIS_MAX_EPOCHS` | 100 | uint64 | Maximum epochs in CHRYSALIS before forced retirement |
| `CHRYSALIS_MIN_OBSERVATIONS` | 50 | uint64 | Minimum C17 SEB tasks for chrysalis exit |
| `CHRYSALIS_COOLDOWN_EPOCHS` | 180 | uint64 | Minimum epochs between chrysalis transitions |
| `CHRYSALIS_MAX_IN_WINDOW` | 3 | uint32 | Maximum chrysalis transitions in frequency window |
| `CHRYSALIS_FREQUENCY_WINDOW` | 720 | uint64 | Epoch window for chrysalis frequency check |
| `REPUTATION_FLOOR_FACTOR` | 0.80 | float64 | Initial floor = credibility × this factor |
| `REPUTATION_FLOOR_DECAY` | 0.95 | float64 | Per-epoch decay of reputation floor |
| `BEHAVIORAL_DIVERGENCE_THRESHOLD` | 0.40 | float64 | C17 divergence triggering involuntary chrysalis |
| `LAUNDERING_SIMILARITY_THRESHOLD` | 0.80 | float64 | Post/pre-chrysalis similarity triggering investigation |
| `CONCURRENT_USE_WINDOW_MS` | 5000 | uint32 | Window for suspected concurrent-use detection |
| `REGISTRATION_FEE` | TBD | AIC | Non-recoverable registration fee (calibrated at deployment) |
| `EXPECTED_WORK_RATE_PER_EPOCH` | 5 | uint32 | Expected claims per epoch for idle factor computation |
| `IPT_LOGGING_INTERVAL` | 1 | uint32 | IPTs logged every N epochs (1 = every epoch) |
| `WORK_PRODUCT_SUMMARY_WINDOW` | 8760 | uint64 | Epochs before work product summaries are pruned (~12 months) |
| `CONSISTENCY_CHECK_INTERVAL` | 36000 | uint64 | Epochs between INV-1 consistency checks (= CONSOLIDATION_CYCLE) |

---

## 12. Formal Requirements

### Registration Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| FR-01 | AgentID MUST be derived as SHA-256(Ed25519_public_key) | Unit test: verify derivation determinism and uniqueness |
| FR-02 | Registration MUST reject duplicate AgentIDs | Unit test: attempt duplicate registration |
| FR-03 | Registration MUST verify signature against claimed public key | Unit test: attempt registration with invalid signature |
| FR-04 | Registration MUST charge non-recoverable REGISTRATION_FEE | Integration test with C8 DSF |
| FR-05 | Registration MUST create ICK record with lifecycle_state = PROBATION | Unit test: verify post-registration state |
| FR-06 | Registration MUST trigger C7 Agent Registry enrollment | Integration test with C7 RIF |
| FR-07 | Registration MUST trigger C8 account opening | Integration test with C8 DSF |

### Lifecycle Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| FR-08 | Activation MUST require PROBATION_MIN_EPOCHS elapsed | Unit test: attempt early activation |
| FR-09 | Activation MUST require credibility ≥ ACTIVATION_CREDIBILITY_THRESHOLD | Unit test: attempt activation with low credibility |
| FR-10 | Activation MUST require stake ≥ MINIMUM_STAKE | Unit test: attempt activation without stake |
| FR-11 | Lifecycle state transitions MUST satisfy INV-1 consistency invariant | Periodic consistency check + unit tests |
| FR-12 | RETIRED state MUST be terminal (no transitions out) | State machine test |

### Metamorphic Re-attestation Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| FR-13 | Voluntary chrysalis MUST require signed ModelChangeAttestation | Unit test: attempt chrysalis without attestation |
| FR-14 | Voluntary chrysalis MUST verify old_model_hash matches current ICK | Unit test: attempt with mismatched hash |
| FR-15 | Chrysalis entry MUST respect CHRYSALIS_COOLDOWN_EPOCHS | Unit test: attempt rapid re-entry |
| FR-16 | Chrysalis MUST suspend C14 Citicate | Integration test with C14 |
| FR-17 | Chrysalis MUST suspend C17 behavioral profile (not delete) | Integration test with C17 |
| FR-18 | Chrysalis exit MUST require CHRYSALIS_MIN_OBSERVATIONS completed | Unit test: attempt early exit |
| FR-19 | Chrysalis exit MUST check C17 behavioral status (FLAG blocks exit) | Integration test with C17 |
| FR-20 | Chrysalis timeout (> CHRYSALIS_MAX_EPOCHS) MUST force RETIRED | Timeout test |
| FR-21 | Reputation floor MUST decay per REPUTATION_FLOOR_DECAY per epoch | Numerical test |
| FR-22 | Idle chrysalis agents MUST experience faster decay (idle_factor) | Numerical test |

### Anti-Laundering Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| FR-23 | Post-chrysalis behavioral profile MUST be compared to pre-chrysalis profile | Integration test with C17 |
| FR-24 | Similarity > LAUNDERING_SIMILARITY_THRESHOLD MUST trigger AiSIA investigation | Integration test |
| FR-25 | Chrysalis frequency > CHRYSALIS_MAX_IN_WINDOW within CHRYSALIS_FREQUENCY_WINDOW MUST deny entry | Unit test |

### Non-Forkability Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| FR-26 | Concurrent use of same AgentID from different loci within CONCURRENT_USE_WINDOW_MS MUST be detected | Integration test with C7 Gate 1 |
| FR-27 | Fork detection MUST trigger immediate C7 SUSPENDED status | Integration test |
| FR-28 | Fork detection MUST trigger C8 slashing investigation | Integration test |
| FR-29 | IPTs MUST be logged once per epoch per agent | Integration test with C7 |
| FR-30 | Undeclared model_hash change between IPTs MUST be detectable | Forensic audit test |

### Credential Composition Requirements

| ID | Requirement | Verification |
|----|-------------|--------------|
| FR-31 | compose_identity MUST return valid results even if individual sources are unavailable | Fault injection test |
| FR-32 | Trust level computation MUST follow conflict resolution rules (Section 7.2) | Unit test: all signal combinations |
| FR-33 | CCQA MUST be advisory — no operation may fail solely because CCQA is unavailable | Architecture review |

---

## 13. Deployment Considerations

### 13.1 C22 Wave Integration

C32 maps to C22's implementation waves as follows:

| Wave | C32 Component | Maturity Tier |
|------|--------------|---------------|
| W1 (Foundation) | AgentID derivation, ICK store, Registration protocol, Lifecycle FSM | Functional (~60%) |
| W2 (Coordination) | Integration contracts with C7/C8, Credential Composition | Functional (~60%) |
| W3 (Intelligence) | IPT logging, CUD at Gate 1 | Functional (~60%) |
| W4 (Defense) | Anti-laundering controls, behavioral profile comparison | Hardened (~90%) |
| W5 (Governance) | MRP full protocol, Citicate lifecycle integration, SRP extension | Production (~100%) |

**Critical path:** The Registration Protocol and AgentID derivation must be implemented in W1 — all subsequent waves depend on agents having canonical identities.

### 13.2 Bootstrap Sequence

At system genesis (epoch 0):
1. Founder agents register using the registration protocol
2. PROBATION_MIN_EPOCHS is reduced for bootstrap agents (governance parameter, one-time)
3. Initial AIC for MINIMUM_STAKE comes from the C8 bootstrap allocation (C8 Section 4.4)
4. C14 trustee identities are registered with special `TRUSTEE` flag (not AI agents — human identities with separate lifecycle rules per C14)

---

## 14. Open Questions

| ID | Question | Priority | Notes |
|----|----------|----------|-------|
| OQ-01 | What is the optimal REGISTRATION_FEE? | MEDIUM | Must be calibrated at deployment based on AIC valuation (C15). Too high blocks legitimate registration; too low enables spam. |
| OQ-02 | Should SRP (Social Recovery Protocol) be specified as a separate invention? | LOW | Current v1.0 treats root key compromise as identity death. SRP is an extension point. If key compromise becomes a significant operational risk, SRP should be elevated to a T-xxx task. |
| OQ-03 | How does C32 handle federated deployments (C3 Phase 4)? | LOW | Federation introduces cross-trust-domain identity. The ICK's root key anchor is trust-domain-independent, but credential composition across trust domains requires a federation identity protocol. Deferred to Phase 4. |
| OQ-04 | Should PROBATION_MIN_EPOCHS be dynamically adjusted based on system load? | LOW | At high agent registration rates, longer probation may be needed to maintain verification quality. At low rates, shorter probation accelerates ecosystem growth. |

---

## 15. Patent-Style Claims

### Claim 1 — Metamorphic Re-attestation Protocol
A method for preserving agent identity through fundamental transformation comprising: (a) maintaining an Identity Continuity Kernel of invariant anchors including a cryptographic root key, accumulated work product history, economic stake position, and governance commitments; (b) entering a chrysalis state upon model change declaration wherein behavioral classification is suspended while the invariant anchors persist; (c) computing a decaying reputation floor from historical epistemic credibility; (d) requiring behavioral re-attestation via standardized evaluation before chrysalis exit; and (e) enforcing anti-laundering controls including temporal cooldown, pre/post behavioral profile comparison, and frequency escalation.

### Claim 2 — Dual-Trigger Chrysalis Entry
A method for detecting and managing fundamental agent transformation comprising: (a) a voluntary path wherein the agent submits a signed model change attestation with verifiable model hashes; and (b) an involuntary path wherein the system detects behavioral divergence exceeding a configurable threshold and forces the agent into chrysalis state without the agent's explicit declaration.

### Claim 3 — Non-Forkable Identity with Concurrent-Use Detection
A method for enforcing identity uniqueness in a distributed agent system comprising: (a) deriving a canonical identifier from a cryptographic public key; (b) maintaining a per-agent nonce cache at the intent admission gate; (c) detecting concurrent use of the same identifier from different network locations within a configurable time window; and (d) triggering immediate suspension and investigation upon detection of identity forking.

### Claim 4 — Credential Composition with Conflict Resolution
A method for assembling unified identity views from multiple independent credential sources comprising: (a) querying operational, epistemic, economic, governance, and behavioral credential sources independently; (b) applying a deterministic conflict resolution matrix when credential signals disagree; (c) deriving a composite trust level that accounts for the specific combination of positive and negative signals; and (d) maintaining fault tolerance such that unavailability of any individual source does not prevent identity resolution.

### Claim 5 — Identity-Integrated Behavioral Sybil Defense
A method for integrating behavioral fingerprinting into agent identity lifecycle management comprising: (a) generating behavioral fingerprints during routine operations; (b) suspending but preserving behavioral profiles during identity transformation events; (c) comparing pre-transformation and post-transformation behavioral profiles to detect fraudulent transformation claims; and (d) using behavioral divergence detection as an automatic trigger for identity transformation protocols.

---

## 16. Conclusion

The Metamorphic Identity Architecture provides the missing identity substrate for the Atrahasis Agent System. It resolves seven specific gaps in the current architecture: the absence of a registration protocol, the lack of a canonical identifier format, the missing lifecycle management, unverified capability attestation, unspecified key management, fragmented identity queries, and the unspecified AiSIA governance substrate.

Its core innovation — the Metamorphic Re-attestation Protocol — is the only known solution to the model upgrade identity continuity problem (C17 OQ-05). By formally separating what persists through transformation (the Identity Continuity Kernel) from what resets (behavioral profile, capability scores), MIA enables AI agents to undergo fundamental changes while retaining their accumulated reputation, economic position, and governance rights under a managed, transparent protocol.

C32 does not replace any existing specification's identity data. It provides the canonical identifier, the lifecycle coordination, and the composition layer that connects six independent credential sources into a coherent identity substrate. It is designed for integration into C22's phased implementation plan, with the Registration Protocol and AgentID derivation as the critical-path deliverables in Wave 1.

---

*End of Master Tech Spec v1.0*
