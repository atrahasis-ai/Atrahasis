# C32 — Metamorphic Identity Architecture: Science Assessment
**Role:** Science Advisor | **Tier:** PRIMARY
**Date:** 2026-03-12

---

## 1. Cryptographic Foundations

### 1.1 Ed25519 Key Derivation for AgentID
**Claim:** AgentID = SHA-256(Ed25519_public_key), yielding a 256-bit canonical identifier.

**Assessment:** SOUND.
- Ed25519 (RFC 8032) produces 256-bit public keys from 256-bit private keys using Curve25519
- SHA-256 is collision-resistant (no known practical collisions); birthday bound is 2^128
- Deterministic derivation: same public key always produces same AgentID — desirable for identity anchoring
- One-way: AgentID cannot be reversed to recover the public key — provides a level of pseudonymity
- Concern: key compromise requires full identity migration (new keypair → new AgentID). This is by design in C32 (root key is the identity anchor), but the migration protocol must handle reputation transfer carefully to prevent identity laundering

### 1.2 Key Rotation vs Root Key Persistence
**Claim:** The root Ed25519 key persists as the identity anchor; operational keys can rotate.

**Assessment:** SOUND with caveats.
- Standard pattern in hierarchical key management (root CA → intermediate → leaf)
- Risk: root key has infinite lifetime by design. Long-lived keys are targets. Hardware security module (HSM) or threshold key management would mitigate but adds complexity
- The AAS context (AI agents, not humans) makes HSM attachment awkward — agents run in cloud/compute environments, not hardware wallets
- Mitigation: C32 should define a key compromise recovery protocol. Current design treats root key loss as identity death, which is correct but harsh

### 1.3 Non-Forkability and Concurrent-Use Detection
**Claim:** ICK is non-forkable; concurrent instances using the same root key trigger Sybil investigation.

**Assessment:** SOUND in principle, CHALLENGING in practice.
- Detecting concurrent use requires either: (a) a global uniqueness check on every signature (expensive), or (b) epoch-based nonce tracking where duplicate nonces from the same key indicate concurrent use
- Epoch-based approach is feasible: each agent signs with `(epoch, sequence_number)`. If two signatures from the same key appear in the same epoch with the same or overlapping sequence ranges, concurrent use is detected
- Latency: detection is retrospective (after signatures appear), not preventive. A fork can operate for up to one epoch before detection
- This is consistent with C5 PCVM's existing retrospective verification model

## 2. Identity Continuity Through Transformation

### 2.1 Metamorphic Re-attestation Protocol (MRP)
**Claim:** An agent undergoing a model upgrade enters a chrysalis state; behavioral profile is suspended but ICK persists. Upon exit, the agent re-establishes behavioral trust through graduated re-entry.

**Assessment:** NOVEL and SOUND.
- The formal separation of "what persists" (ICK invariants) from "what resets" (behavioral profile, capability scores) is a well-defined mathematical partition
- The reputation floor concept (`effective_credibility = max(reputation_floor × decay_factor, current_observed_credibility)`) is sound — it's a standard smoothing function with exponential decay
- Key question: what constitutes a valid "model change" triggering chrysalis? Options:
  - (a) Self-declared (agent claims model upgrade) — exploitable for identity laundering
  - (b) Verifiable model hash change (cryptographic proof that the model binary/weights changed) — requires model provider attestation infrastructure
  - (c) Behavioral divergence detection (system detects that behavioral fingerprint has changed significantly) — passive, but delayed
- Recommendation: combine (b) and (c). Require verifiable model hash attestation for voluntary chrysalis entry, and use behavioral divergence detection as an involuntary chrysalis trigger

### 2.2 Reputation Floor Decay
**Claim:** `reputation_floor = historical_credibility × decay_factor^(epochs_in_chrysalis)`

**Assessment:** SOUND.
- Exponential decay is the standard approach in trust systems (Jøsang's Subjective Logic uses opinion aging)
- The decay rate is a tunable parameter. Too fast → chrysalis is punitive (agents delay necessary upgrades). Too slow → identity laundering is profitable
- Calibration: the decay rate should be set such that the reputation floor reaches the "new agent" baseline after approximately the same number of epochs as a full Citicate probationary period. This ensures that an agent who stays in chrysalis too long loses its advantage over a genuinely new agent
- C5 PCVM already implements opinion aging via `uncertainty_increase_per_epoch` — the MRP decay should use a consistent mathematical framework

### 2.3 Work Product Graph Persistence
**Claim:** The ICK retains a hash-linked chain of work product summaries that persist through metamorphosis.

**Assessment:** SOUND.
- Hash-linked chains (Merkle chains) are well-understood data structures
- Pruning to summary statistics after an aging window is standard (C6 EMA catabolism provides the pattern)
- The hash chain provides tamper-evident provenance: any retroactive modification of historical summaries is detectable
- Storage: summary records are compact (estimated ~1KB per epoch summary × 12 months ≈ ~500KB per agent for the rolling window). Manageable

## 3. Integration with Existing AAS Components

### 3.1 C5 PCVM Compatibility
**Assessment:** COMPATIBLE.
- C5's per-agent, per-class Subjective Logic opinions can be read directly as the epistemic reputation component of the ICK
- The MRP's behavioral profile reset does NOT require resetting C5 credibility opinions — these are claim-verification-based, not behavioral. An agent's verified work history persists through metamorphosis
- C17 behavioral fingerprints are the component that resets. This is a clean separation: C5 measures *what you produce*, C17 measures *how you produce it*
- The chrysalis state maps to C17's provisional Citicate status (no voting, reduced earning)

### 3.2 C7 RIF Agent Registry Compatibility
**Assessment:** COMPATIBLE with minor extension.
- C7's Agent Registry needs: (a) a `REGISTER_AGENT` operation, (b) a `CHRYSALIS` status value added to the existing {ACTIVE, SUSPENDED, DRAINING, DEPARTED} enum, (c) key rotation protocol
- The existing `status` field and lifecycle transition logic in C7 can accommodate the MRP state machine without architectural changes

### 3.3 C8 DSF Account Compatibility
**Assessment:** COMPATIBLE.
- C8's `AccountState` is keyed by `AgentID` — the canonical AgentID format change (to SHA-256 derivation) requires updating the type definition but not the data structure
- The cold-start protocol (Section 4.4) maps directly to C32's PROBATION state
- Stake persistence through chrysalis is natural — the `staked_aic` field is part of the ICK invariants

### 3.4 C14 AiBC Citicate Compatibility
**Assessment:** COMPATIBLE.
- The Citicate becomes a specific credential type within the ICK framework
- Citicate issuance criteria (IC-01 through IC-05) remain as-is — they become the requirements for transitioning from PROBATION to Citicate eligibility
- The chrysalis → ACTIVE transition does not require Citicate re-issuance (the Citicate persists as an ICK invariant) but does require C17 behavioral re-attestation for the Citicate to remain active

### 3.5 C17 MCSD Compatibility
**Assessment:** COMPATIBLE — C32 provides the solution to C17 OQ-05.
- The MRP defines exactly what happens to behavioral history on model upgrade: behavioral fingerprint is reset, new SEB tasks are administered, provisional status applies until minimum observation threshold is met
- The one-way hash relationship `agent_id_behavioral = hash(citicate_id)` remains valid — the Citicate ID persists through metamorphosis, so the behavioral agent_id hash also persists, but the behavioral *data* is reset

### 3.6 C31 CAT Compatibility
**Assessment:** COMPATIBLE.
- C31 reads CapabilityVector from C5/C7 — these components are compatible with C32
- The 256-bit AgentID for lexicographic tiebreaking (FR-05) is now formally defined as SHA-256(Ed25519_pubkey), resolving the format ambiguity
- During chrysalis, an agent's CapabilityVector defaults (500 on all dimensions per C31's staleness rule) — this is correct behavior for an agent in transition

## 4. Assumption Validation Report

| Ideation Assumption | Research Finding | Status |
|---------------------|-----------------|--------|
| No existing system handles model upgrade identity continuity | Confirmed. Signet claims persistence but has no specified mechanism. ERC-8004 has no model versioning concept. OpenID Foundation framework doesn't address it. | VALIDATED |
| DID/VC provides relevant substrate for identifier + credential patterns | Confirmed. arXiv 2511.02841 applies DID+VC to AI agents. W3C standards are mature. | VALIDATED |
| Behavioral fingerprinting integration with identity is novel | Confirmed. No prior art combines behavioral Sybil detection with identity lifecycle transitions. | VALIDATED |
| Subjective Logic reputation is more rigorous than feedback-based | Confirmed. Jøsang's TNA-SL provides formal trust propagation. ERC-8004/Signet use simple feedback/composite scores. | VALIDATED |
| Non-forkable identity is achievable | Partially validated. Epoch-based concurrent-use detection is feasible but retrospective (up to 1-epoch delay). Prevention is not possible without a central authority or consensus mechanism. | PARTIALLY VALIDATED |
| Chrysalis state can preserve identity while resetting behavioral profile | Confirmed sound. The partition of ICK invariants (root key, work products, stake, governance) vs. reset components (behavioral profile, capability scores) is mathematically clean. | VALIDATED |
| Verifiable proof-of-model-change is achievable | Uncertain. Requires model provider attestation infrastructure or verifiable model hashing. Not all model providers offer signed attestations. May need a fallback to behavioral divergence detection. | NEEDS DESIGN WORK |

## 5. Overall Scientific Assessment

The Metamorphic Identity Architecture is scientifically sound. The cryptographic foundations (Ed25519, SHA-256, hash chains) are well-established. The identity continuity model (ICK invariants + MRP) is novel but mathematically well-defined. The integration with existing AAS components (C5, C7, C8, C14, C17, C31) is compatible without requiring architectural changes to those specs.

The main scientific uncertainty is the proof-of-model-change mechanism. This requires design-time resolution, not scientific validation — the question is which attestation method to use, not whether attestation is possible.

**Confidence:** 4 (solid)
