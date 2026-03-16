# C12: AVAP — Anonymous Verification with Adaptive Probing

## Master Technical Specification v1.0

**Invention:** C12 — Collusion Defense
**Stage:** SPECIFICATION (Final Deliverable)
**Date:** 2026-03-10
**System:** Atrahasis Agent System
**Classification:** AVAP — 5-mechanism anti-collusion architecture
**Normative References:** C3 (Tidal Noosphere v1.0), C5 (PCVM v1.0), C6 (EMA v1.0), C8 (DSF v2.0), C10 (Hardening Addenda), C11 (CACT v1.0), RFC 9381 (ECVRF), RFC 8032 (Ed25519), Pedersen Commitments, Groth16, Fujisaki-Suzuki 2007 (LRS)

> **Normative Reference Update (2026-03-11):** Normative references updated to C3 v2.0, C5 v2.0, C6 v2.0. C5 v2.0 and C6 v2.0 integrate AVAP anti-collusion mechanisms from this specification into their respective core architectures. However, C12 retains normative authority over its threat model (collusion ring formation taxonomy, selective collusion attack profiles), formal proofs (game-theoretic equilibrium analysis, defection incentive proofs), and attack taxonomies (5-mechanism coverage model, detection timeline bounds). Where C5/C6 v2.0 and C12 overlap, C5/C6 v2.0 govern integration behavior and C12 governs threat analysis.

---

## Abstract

AVAP (Anonymous Verification with Adaptive Probing) is a 5-mechanism anti-collusion architecture for the Atrahasis distributed knowledge verification system. It addresses the fundamental vulnerability that coordinated groups of verification agents can manipulate claim credibility scores despite existing statistical defenses. AVAP combines structural prevention (anonymous committee selection via VRF self-selection with mandatory cover traffic; sealed commit-reveal opinion submission), active detection (class-stratified honeypot claims with canary-trap leak identification; conditional behavioral analysis via pairwise mutual information screening), and economic deterrence (collusion deterrence payments with zero-knowledge reporting, asymmetric information injection, and enterprise liability cascades). Together with the existing C10 4-layer defense-in-depth, AVAP forms a 6-layer detection-prevention-deterrence system that renders collusion rings structurally difficult to form, statistically detectable within 25 epochs, and economically irrational to sustain beyond 10 epochs. The system operates within a 20% overhead budget relative to base verification cost and degrades gracefully to a Minimum Viable configuration at 11.5% overhead if hard gates fail.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Solution Overview](#2-solution-overview)
3. [Architecture](#3-architecture)
4. [Mechanism 1: Anonymous Committees](#4-mechanism-1-anonymous-committees)
5. [Mechanism 2: Sealed Opinion Submission](#5-mechanism-2-sealed-opinion-submission)
6. [Mechanism 3: Honeypot Claims](#6-mechanism-3-honeypot-claims)
7. [Mechanism 4: Collusion Deterrence Payment](#7-mechanism-4-collusion-deterrence-payment)
8. [Mechanism 5: Conditional Behavioral Analysis](#8-mechanism-5-conditional-behavioral-analysis)
9. [Cross-Mechanism Integration](#9-cross-mechanism-integration)
10. [Operational Cost Model](#10-operational-cost-model)
11. [Parameters & Configuration](#11-parameters--configuration)
12. [Pseudocode](#12-pseudocode)
13. [Failure Modes & Recovery](#13-failure-modes--recovery)
14. [Conformance Requirements](#14-conformance-requirements)
15. [Appendix A: Formal Requirements Traceability](#appendix-a-formal-requirements-traceability)
16. [Appendix B: Hard Gate Verification Protocols](#appendix-b-hard-gate-verification-protocols)
17. [Appendix C: Game-Theoretic Proofs](#appendix-c-game-theoretic-proofs)
18. [Appendix D: C9 Defense Invariant Compliance](#appendix-d-c9-defense-invariant-compliance)
19. [Appendix E: Glossary](#appendix-e-glossary)

---

## 1. Problem Statement

### 1.1 The Collusion Threat

The Atrahasis system relies on distributed verification: multiple independent agents evaluate claims, produce Subjective Logic opinion tuples, and the PCVM (C5) fuses these opinions into a credibility score. The security of this architecture depends on agent independence — each opinion must reflect the agent's genuine assessment, not a coordinated strategy.

**Collusion** occurs when two or more agents coordinate their verification opinions to manipulate fused credibility scores. A collusion ring can:

1. **Inflate credibility** of low-quality or fabricated claims by coordinating high-belief opinions.
2. **Suppress credibility** of valid claims that conflict with the ring's interests.
3. **Extract economic value** by manipulating claims that affect AIC staking outcomes via C8 DSF settlement.
4. **Undermine epistemic integrity** by corrupting the knowledge graph's credibility surface, causing downstream reasoning errors that cascade through dependent claims.

### 1.2 Limitations of Existing Defenses

C10 Hardening Addenda established a 4-layer defense-in-depth:

| Layer | Mechanism | What It Catches | What It Cannot Catch |
|---|---|---|---|
| Layer 1: Sentinel Graph | Infrastructure fingerprinting, behavioral clustering | Sybil attacks, obvious identity correlation | Rings with genuinely independent infrastructure |
| Layer 2: Statistical Detection | Pairwise agreement anomalies, KL divergence, opinion copying index | Agents who always agree or copy patterns | Sophisticated rings that add noise, rotate coordination patterns, or collude selectively |
| Layer 3: Diversity Constraints | Model lineage, methodology, temporal, regional diversity | Homogeneous rings (same model family, same region) | Rings that deliberately span diversity categories |
| Layer 4: Adaptive Audit | Elevated deep-audit for suspicious patterns | Agents who fail under scrutiny | Rings that pass individual audits but coordinate only in non-audited interactions |

**Critical gap:** All four layers are _reactive_ — they detect collusion after it manifests in behavioral patterns. None prevent coordination from forming in the first place, none actively probe for dishonest behavior with known ground truth, and none create economic incentives for ring members to defect.

A sophisticated ring that (a) spans diversity categories, (b) colludes selectively (only on 20% of shared committees), (c) adds noise to avoid statistical signatures, and (d) maintains independent infrastructure can evade all four layers for extended periods. Simulation analysis (C12 Research Report Section 4) estimates such a ring could operate undetected for 100+ epochs with 60% probability under C10-only defenses.

### 1.3 Why This Matters

The Atrahasis knowledge graph is an accumulative structure. Claims verified today become the foundation for future reasoning. A collusion ring operating undetected for 100 epochs could corrupt thousands of claims, and the downstream credibility cascade would affect orders of magnitude more. The cost of remediation grows super-linearly with the duration of undetected collusion. Prevention and early detection are therefore not merely desirable — they are economically necessary.

---

## 2. Solution Overview

### 2.1 AVAP's Five Mechanisms

AVAP introduces five complementary mechanisms organized by function:

**Structural Prevention (pre-verification):**
- **M1: Anonymous Committees** — VRF-based self-selection with encrypted assignment tokens and mandatory cover traffic. Colluders cannot identify allies on a committee, eliminating real-time coordination.
- **M2: Sealed Opinion Submission** — Two-phase commit-reveal protocol for Subjective Logic opinions. Agents commit to opinions before seeing others' commitments, preventing signaling and opinion copying.

**Active Detection (during/post-verification):**
- **M3: Honeypot Claims** — Synthetic verification tasks with known ground truth, injected indistinguishably into the pipeline. Class-stratified generators (D, E, C/S) with canary-trap variant generation for leak identification.
- **M5: Conditional Behavioral Analysis** — Continuous screening via pairwise conditional mutual information. Detects whether an agent's opinions shift depending on the presence of specific "allies" on the committee.

**Economic Deterrence (post-detection):**
- **M4: Collusion Deterrence Payment** — Three sub-mechanisms: (a) asymmetric information injection to destabilize pre-commitment contracts, (b) graduated temporal bounties for ring defectors, (c) enterprise liability with retroactive audit cascades.

### 2.2 The Key Insight

AVAP's power comes from the interaction between layers, not any single mechanism:

1. **M1+M2 force pre-coordination.** Because agents cannot identify committee members or observe opinions in real time, all collusion must be arranged _before_ committee assignment. This means rings must commit to collusion strategies blindly.
2. **M3 exploits blind commitment.** Pre-committed colluders cannot distinguish honeypots from real claims, so their blanket strategy (e.g., "approve everything from domain X") is caught by ground-truth probes.
3. **M5 detects selective collusion.** Even rings that collude only when allies are present leave conditional behavioral signatures that accumulate over time.
4. **M4 makes rings self-destabilizing.** As detection probability p(t) rises (from M3+M5) and enterprise liability L(t) grows, every ring member faces a rational incentive to defect first. Asymmetric information injection accelerates this by increasing _perceived_ p(t).

The result is a system where collusion is hard to coordinate (M1+M2), risky to execute (M3+M5), and economically irrational to sustain (M4).

### 2.3 Design Principles

| Principle | Implementation |
|---|---|
| **No single point of failure** | 5 independent mechanisms; any 2 provide meaningful defense |
| **Graduated response** | Single failures are logged, not punished; escalation requires patterns |
| **False positive protection** | No automated slashing below P(collusion) > 0.75; HITL required for slashing |
| **Economic self-funding** | Bounties paid from forfeited stakes; no new AIC creation |
| **Constitutional governance** | 7 critical parameters require G-class supermajority to change |
| **Graceful degradation** | MV-AVAP fallback at 11.5% cost if hard gates fail |

---

## 3. Architecture

### 3.1 Position in the Atrahasis Stack

AVAP is a cross-cutting anti-collusion layer that instruments the verification pipeline without replacing any existing component.

```
+=========================================================================+
|  C7: RIF — Recursive Intent Fabric (Orchestration)                       |
+=========================================================================+
          |
          v
+=========================================================================+
|  C8: DSF — Deterministic Settlement Fabric (Economics)                   |
|    AIC staking, slashing, enterprise liability settlement                |
|    AVAP INTERFACE: M4 slashing events, bounty escrow, CDP settlements    |
+=========================================================================+
          |                    |                    |
          v                    v                    v
+=========================================================================+
|  AVAP LAYER (THIS SPECIFICATION)                                         |
|  +-----------+  +-----------+  +----------+  +--------+  +-----------+  |
|  | M1:       |  | M2:       |  | M3:      |  | M4:    |  | M5:       |  |
|  | Anonymous |  | Sealed    |  | Honeypot |  | CDP    |  | Condition.|  |
|  | Committee |  | Opinion   |  | Claims   |  | Deter. |  | Behavioral|  |
|  | Selection |  | Submit    |  | Engine   |  | System |  | Analysis  |  |
|  +-----------+  +-----------+  +----------+  +--------+  +-----------+  |
|                                                                          |
|  +-------------------------------------------------------------------+  |
|  | Multi-Signal Fusion Classifier                                     |  |
|  | (combines M3 + M5 + existing Layer 2 + M4 CDP reports)            |  |
|  +-------------------------------------------------------------------+  |
|                                                                          |
|  +-------------------------------------------------------------------+  |
|  | Graduated Response Engine                                          |  |
|  | (audit escalation, slashing recommendations, enterprise liability) |  |
|  +-------------------------------------------------------------------+  |
+=========================================================================+
          |                    |                    |
          v                    v                    v
+=========================================================================+
|  C3: Tidal Noosphere    C5: PCVM           C6: EMA                      |
|  VRF committee select.  VTD verification   Knowledge metabolism          |
|  Sentinel Graph         Claim classif.     SHREC regulation              |
|  Parcel coordination    Credibility engine Consolidation                 |
+=========================================================================+
          |
          v
+=========================================================================+
|  C4: ASV — Agent Semantic Vocabulary (Communication)                     |
+=========================================================================+
```

### 3.2 Data Flow: Claim Lifecycle Under AVAP Protection

```
PHASE 1: CLAIM SUBMISSION
  Agent produces claim + VTD (per C5/C11 CACT)
                |
                v
PHASE 2: COMMITTEE FORMATION (M1)
  VRF self-selection: each eligible agent evaluates VRF
  Selected agents learn they are on the committee (privately)
  Non-selected agents perform cover-traffic verification
                |
                v
PHASE 3: HONEYPOT INJECTION (M3, transparent to agents)
  Honeypot Engine may substitute/inject honeypot variant
  Agent receives claim for verification (real or honeypot)
  Agent cannot distinguish real from honeypot
                |
                v
PHASE 4: SEALED OPINION SUBMISSION (M2)
  Each committee member constructs Subjective Logic opinion
  Commit phase: submit H(opinion || nonce)
  Window closes; reveal phase begins
  Reveal phase: submit (opinion, nonce); verify against commitment
                |
                v
PHASE 5: OPINION FUSION + HONEYPOT EVALUATION (M3)
  Standard PCVM opinion fusion (C5 Section 6)
  If claim was a honeypot: evaluate each agent's opinion against truth
  Honeypot results feed into Multi-Signal Fusion Classifier
                |
                v
PHASE 6: BEHAVIORAL ANALYSIS UPDATE (M5)
  Update conditional behavioral statistics for all committee members
  Recompute Collusion Suspicion Scores (CSS)
                |
                v
PHASE 7: MULTI-SIGNAL FUSION
  Combine: M3 honeypot signals + M5 CSS + Layer 2 statistics + M4 reports
  Output: per-agent collusion probability estimate
                |
                v
PHASE 8: GRADUATED RESPONSE
  If P(collusion) > INVESTIGATION_THRESHOLD (0.30): trigger elevated audit
  If P(collusion) > ENHANCED_MONITORING (0.50): targeted honeypots (2x rate)
  If P(collusion) > SLASHING_THRESHOLD (0.75): recommend slashing (HITL)
  If P(collusion) > ENTERPRISE_LIABILITY (0.90): retroactive audit (M4c)
                |
                v
PHASE 9: COMMITTEE REVEAL
  After all opinions processed, committee membership is revealed
  VRF proofs published for auditability
  Anonymity window closes
```

### 3.3 Mechanism Classification Matrix

| Mechanism | Type | Timing | Coverage | Primary Strength |
|---|---|---|---|---|
| M1: Anonymous Committees | Prevention (structural) | Pre-verification | All claim classes | Prevents targeted coordination |
| M2: Sealed Opinions | Prevention (structural) | During verification | All claim classes | Prevents signaling/copying |
| M3: Honeypot Claims | Detection (active probing) | During verification | D/E full, C/S partial, H/N excluded | Catches rubber-stamping with ground truth |
| M4: CDP | Deterrence (economic) | Post-detection | All claim classes | Destabilizes collusion rings economically |
| M5: Behavioral Analysis | Detection (passive monitoring) | Continuous | All classes (strongest on S/H/C) | Screens for conditional behavior patterns |

### 3.4 Interface Summary

| Interface | AVAP Component | Direction | Protocol |
|---|---|---|---|
| C3 Tidal Noosphere | M1 | Bidirectional | VRF seed consumption, committee formation |
| C3 Sentinel Graph | M5, Response Engine | Outbound | Cluster updates from collusion detection |
| C5 PCVM | M2, M3 | Bidirectional | Opinion submission/fusion, claim injection |
| C6 EMA | M4c | Outbound | Credibility cascade propagation |
| C8 DSF | M4, Response Engine | Outbound | Slashing events, bounty escrow, enterprise liability settlement |
| C10 Existing Layers | M5, Fusion Classifier | Bidirectional | Layer 1-4 signals as classifier inputs |
| C11 CACT | M3 | Inbound | Commitment chain data for honeypot design |

---

## 4. Mechanism 1: Anonymous Committees

### 4.1 Design Rationale

Anonymous committees prevent colluders from identifying allies on a verification committee, eliminating the ability to selectively coordinate votes in real time. The mechanism extends C3's existing VRF-based committee selection (C3 Technical Spec Section 5, VRF Dual Defense Protocol) with encrypted assignment tokens and mandatory cover traffic.

**Core invariant (INV-M1):** No agent learns the identity of any other committee member until after all sealed opinions have been submitted and the reveal phase is complete.

### 4.2 VRF Assignment Token Format

Each agent performs VRF self-selection independently. The output is an encrypted assignment token that only the selected agent can interpret.

```
STRUCTURE AssignmentToken:
    claim_id:           bytes32         // SHA-256 hash of the claim being verified
    epoch:              uint64          // Epoch number (big-endian)
    agent_id:           AgentID         // Selected agent's persistent identifier
    vrf_output:         bytes32         // VRF output (beta string per RFC 9381)
    vrf_proof:          bytes80         // VRF proof (pi string per RFC 9381), ECVRF-P256-SHA256
    selection_rank:     uint8           // Agent's rank in committee (ascending VRF output)
    committee_slot:     uint8           // Assigned slot index (0..committee_size-1)
    assignment_nonce:   bytes16         // Cryptographically random nonce for this assignment
    token_hash:         bytes32         // H(claim_id || epoch || agent_id || vrf_output || assignment_nonce)
    encrypted_payload:  bytes           // Enc(agent_pubkey, verification_instructions)
```

**Encryption scheme:** The `encrypted_payload` contains the claim content and verification instructions, encrypted with the agent's X25519 public key using XSalsa20-Poly1305 authenticated encryption. This ensures that even if assignment tokens are intercepted in transit, only the intended agent can decrypt the verification task.

**REQ-M1-001:** The AssignmentToken MUST use ECVRF-P256-SHA256 as specified in RFC 9381 Section 5.

**REQ-M1-002:** The encrypted_payload MUST use X25519-XSalsa20-Poly1305 (NaCl crypto_box) for authenticated encryption.

**REQ-M1-003:** The assignment_nonce MUST be generated from a CSPRNG with at least 128 bits of entropy.

### 4.3 Self-Selection Protocol

```
FUNCTION avap_committee_select(
    agent: Agent,
    claim: Claim,
    epoch: uint64,
    vrf_seed: bytes32,
    eligible_pool: Set<Agent>,
    committee_size: uint8
) -> (bool, AssignmentToken?):

    // Step 1: Compute VRF input with AVAP-specific domain separation
    alpha = SHA256(claim.hash || uint64_be(epoch) || vrf_seed || b"AVAP_M1_v1")

    // Step 2: Evaluate VRF
    (beta, pi) = ECVRF_prove(agent.privkey, alpha)
    // beta: 32-byte output; pi: 80-byte proof (per RFC 9381 Section 5.1)

    // Step 3: Self-selection threshold
    // Probability of selection = committee_size / |eligible_pool|
    threshold = (committee_size * 2^256) / |eligible_pool|
    vrf_value = uint256_from_bytes(beta)

    IF vrf_value >= threshold:
        RETURN (false, null)  // Not selected for this committee

    // Step 4: Compute selection rank (lower VRF output = higher rank)
    rank = vrf_value

    // Step 5: Construct assignment token (stored locally, never broadcast)
    token = AssignmentToken{
        claim_id:         claim.hash,
        epoch:            epoch,
        agent_id:         agent.id,
        vrf_output:       beta,
        vrf_proof:        pi,
        selection_rank:   rank,
        committee_slot:   DEFERRED,  // Computed after all agents self-select
        assignment_nonce: csprng_bytes(16),
        token_hash:       SHA256(claim.hash || uint64_be(epoch) || agent.id
                                 || beta || assignment_nonce),
        encrypted_payload: null      // Populated when claim content is fetched
    }

    RETURN (true, token)
```

**REQ-M1-004:** The VRF input MUST include the domain tag `b"AVAP_M1_v1"` to ensure independence from C3's task-scheduling VRF selections.

**REQ-M1-005:** Self-selection MUST be computable locally by each agent without communication with any other agent or central coordinator.

**REQ-M1-006:** The selection threshold MUST yield an expected committee size equal to the `committee_size` parameter (within statistical variation).

### 4.4 Anonymity Maintenance Timeline

```
TIME 0:          Epoch begins. VRF seed for this epoch is published.

TIME 0+delta:    Each agent evaluates VRF for each pending claim.
                 Selected agents learn they are on the committee.
                 NON-selected agents DO NOT learn who IS selected.

TIME 0 to T_w:   VERIFICATION WINDOW (default: 6 hours)
                 Selected agents verify the claim and form opinions.
                 All agents (selected and non-selected) perform cover traffic:
                   - Fetch claim content (mandatory for all agents in pool)
                   - Process claim to depth proportional to COVER_TRAFFIC_DEPTH
                   - Submit cover-traffic heartbeats (structurally identical
                     to real verification activity)

TIME T_w:        COMMITMENT DEADLINE
                 Selected agents submit H(opinion || nonce) to coordinator.
                 Cover-traffic agents submit H(null_opinion || nonce).
                 All submissions are structurally identical (256 bytes, padded).

TIME T_w+delta:  REVEAL PHASE (begins when threshold commitments received)
                 Selected agents reveal (opinion, nonce).
                 Cover-traffic agents reveal (null_opinion, nonce).
                 Coordinator filters: only opinions from VRF-proven members count.

TIME T_r:        REVEAL DEADLINE (default: T_w + 2 hours)
                 All revealed. Committee membership NOW becomes public.
                 VRF proofs published for auditability.
```

**REQ-M1-007:** Committee membership MUST NOT be revealed to any party other than the selected agent itself until after the reveal deadline T_r.

**REQ-M1-008:** All commitment messages MUST be fixed-size (256 bytes, zero-padded) regardless of whether the submitter is a committee member or cover-traffic agent.

### 4.5 Cover Traffic Specification

Cover traffic masks which agents are on the committee by ensuring all agents in the eligible pool exhibit similar network and computational behavior.

```
FUNCTION generate_cover_traffic(
    agent: Agent,
    claim: Claim,
    is_committee_member: bool
) -> CoverTrafficRecord:

    // All agents fetch the claim content (mandatory)
    claim_content = fetch_claim_for_verification(claim.hash)

    // All agents perform partial verification to COVER_TRAFFIC_DEPTH
    partial_result = partial_verify(
        claim_content,
        depth = COVER_TRAFFIC_DEPTH,  // default: 3 (of ~10 verification steps)
        include_source_fetch = true    // Fetch at least 1 cited source
    )

    // Generate heartbeat (identical format for committee and cover agents)
    heartbeat = VerificationHeartbeat{
        agent_id:     agent.id,
        claim_hash:   claim.hash,
        epoch:        current_epoch(),
        timestamp:    now(),
        activity_hash: SHA256(partial_result.trace),
        // NOTE: heartbeat does NOT indicate committee membership
    }

    submit_heartbeat(heartbeat)

    IF is_committee_member:
        // Continue with full verification beyond cover depth
        full_result = complete_verification(claim_content, partial_result)
        RETURN CoverTrafficRecord{
            type: "FULL_VERIFICATION",
            heartbeat: heartbeat,
            result: full_result
        }
    ELSE:
        // Discard partial result after heartbeat submission
        RETURN CoverTrafficRecord{
            type: "COVER_ONLY",
            heartbeat: heartbeat,
            result: null
        }
```

**Cover traffic cost model:**

| Parameter | Value | Rationale |
|---|---|---|
| COVER_TRAFFIC_DEPTH | 3 steps (of ~10) | ~30% of full verification cost per non-committee agent |
| Cover traffic fraction | 100% of eligible pool | All agents participate; no opt-out |
| Net overhead per non-committee agent | ~15-20% of full verification cost | Claim fetch + partial verify + heartbeat |
| Net system overhead | ~8-12% of verification budget | Pool is ~20x committee size; amortized cost |

**REQ-M1-009:** All agents in the eligible pool MUST perform cover traffic for every claim in their pool, regardless of committee membership status.

**REQ-M1-010:** Cover traffic heartbeats MUST be structurally indistinguishable from real verification heartbeats. The heartbeat format MUST NOT contain any field that differs between committee members and cover-traffic agents.

**REQ-M1-011:** Cover traffic MUST include at least one source fetch to mask the bandwidth signature of full verification.

### 4.6 Side-Channel Mitigations

| Side Channel | Attack Vector | Mitigation | Residual Risk |
|---|---|---|---|
| Timing | Committee agents take longer (full vs. cover) | Cover traffic depth + jittered submission within 6-hour window | LOW |
| Bandwidth | Committee agents fetch more data | Cover agents also fetch sources (COVER_TRAFFIC_DEPTH includes source fetch) | LOW |
| Submission size | Commitment messages differ in size | All commitments fixed-size (256 bytes, zero-padded) | NEGLIGIBLE |
| Long-term statistical | Committee frequency observable over many epochs | VRF re-keying every REKEY_INTERVAL epochs (default: 100) | LOW-MEDIUM |
| IP/infrastructure | Network observation of claim source connections | Optional TOR-like onion routing for high-security mode | MEDIUM (without onion routing) |
| Electromagnetic/power | Physical side channels on hardware | Out of scope (physical security is operator responsibility) | N/A |

**REQ-M1-012:** VRF keys MUST be rotated every REKEY_INTERVAL epochs (default: 100). Key rotation MUST be transparent to the self-selection protocol.

**REQ-M1-013:** Implementations SHOULD provide an optional onion-routing mode for claim content fetch to mitigate IP-level observation.

### 4.7 Integration with C3 VRF

AVAP's M1 extends C3's VRF Dual Defense Protocol (C3 Technical Spec Section 5):

1. **Domain separation:** AVAP uses `b"AVAP_M1_v1"` domain tag, ensuring independence from C3 task-scheduling VRF.
2. **Diversity pool integration:** AVAP inherits C3's Pre-Stratified Diversity Pools (C3 Section 5.3). Committees satisfy model lineage, methodology, temporal, and regional diversity constraints.
3. **Sentinel Graph exclusion:** Agents in the same Sentinel Graph identity cluster (C10 Layer 1) are subject to co-occurrence limits: at most MAX_CLUSTER_CO_OCCURRENCE (default: 1) per committee.
4. **VRF seed schedule:** AVAP uses epoch-level VRF seeds from C3's Noosphere entropy source. No additional randomness infrastructure required.

**REQ-M1-014:** AVAP committee selection MUST inherit and enforce all C3 Pre-Stratified Diversity Pool constraints.

**REQ-M1-015:** At most MAX_CLUSTER_CO_OCCURRENCE agents from the same Sentinel Graph cluster MUST be permitted on any single committee.

### 4.8 Committee Size and Pool Ratio

| Parameter | Default | Range | Constitutional? | Rationale |
|---|---|---|---|---|
| MIN_COMMITTEE_SIZE | 7 | [5, 20] | YES (G-class) | Below 7, f >= 1/3 BFT tolerance is too fragile |
| MAX_COMMITTEE_SIZE | 15 | [7, 30] | No | Diminishing returns above 15; cost linear |
| DEFAULT_COMMITTEE_SIZE | 10 | [7, 15] | No | Balances security and cost |
| MIN_POOL_SIZE | 200 | [100, 1000] | YES (G-class) | Below 200, anonymity set too small |
| MAX_COMMITTEE_TO_POOL_RATIO | 0.05 | [0.01, 0.10] | YES (G-class) | Any agent has <5% selection probability |
| MAX_CLUSTER_CO_OCCURRENCE | 1 | [1, 3] | No | Sentinel cluster diversity |

**Fallback for small pools:** If the eligible pool for a claim's domain has fewer than MIN_POOL_SIZE agents, the claim is escalated to a cross-domain pool. If still insufficient, the claim enters a holding queue until pool size recovers.

**REQ-M1-016:** If the eligible pool size is below MIN_POOL_SIZE, the system MUST escalate to a cross-domain pool before queuing.

**REQ-M1-017:** The committee-to-pool ratio MUST NOT exceed MAX_COMMITTEE_TO_POOL_RATIO for any committee assignment.

---

## 5. Mechanism 2: Sealed Opinion Submission

### 5.1 Design Rationale

Sealed opinion submission prevents agents from observing or inferring other agents' opinions before committing their own. This eliminates real-time signaling, opinion copying, and "follow the leader" strategies. The protocol uses a standard cryptographic commit-reveal scheme adapted for Subjective Logic opinion tuples.

### 5.2 Data Structures

```
STRUCTURE SealedOpinion:
    claim_hash:          bytes32         // SHA-256 hash of the claim
    epoch:               uint64          // Epoch number
    agent_id:            AgentID         // Encrypted during commit; revealed after
    opinion:             OpinionTuple    // (b, d, u, a) Subjective Logic opinion
    confidence_metadata: ConfidenceMeta  // Optional: reasoning hash, probe results
    nonce:               bytes32         // Cryptographic nonce for commitment
    commitment:          bytes32         // SHA-256(opinion || metadata || nonce)
    signature:           bytes64         // Ed25519 signature over commitment

STRUCTURE OpinionTuple:
    belief:              float64         // [0, 1]
    disbelief:           float64         // [0, 1]
    uncertainty:         float64         // [0, 1]
    base_rate:           float64         // [0, 1], prior for the claim class
    // CONSTRAINT: belief + disbelief + uncertainty = 1.0 (tolerance: 1e-9)
```

### 5.3 Commit-Reveal Protocol

**Phase 1: COMMIT**

```
FUNCTION submit_commitment(
    agent: Agent,
    claim: Claim,
    opinion: OpinionTuple,
    metadata: ConfidenceMeta
) -> Commitment:

    // Validate opinion tuple constraint
    ASSERT abs(opinion.belief + opinion.disbelief + opinion.uncertainty - 1.0) < 1e-9,
        "Opinion tuple must sum to 1.0"

    // Generate cryptographic nonce (256-bit, CSPRNG)
    nonce = csprng_bytes(32)

    // Compute commitment hash using canonical serialization
    payload = canonical_serialize(opinion) || canonical_serialize(metadata) || nonce
    commitment_hash = SHA256(payload)

    // Sign the commitment with agent's Ed25519 private key
    signature = Ed25519_sign(agent.privkey, commitment_hash)

    // Encrypt agent identity under coordinator's public key
    // Coordinator cannot correlate agent to commitment during commit phase
    encrypted_agent_id = crypto_box(
        coordinator_pubkey,
        agent.id || claim.hash || uint64_be(current_epoch())
    )

    commitment = Commitment{
        claim_hash:         claim.hash,
        epoch:              current_epoch(),
        encrypted_agent_id: encrypted_agent_id,
        commitment_hash:    commitment_hash,
        signature:          signature,
        submitted_at:       now()
    }

    coordinator.submit(commitment)
    RETURN commitment
```

**Phase 2: THRESHOLD CHECK + REVEAL TRIGGER**

```
FUNCTION check_reveal_trigger(
    claim_hash: bytes32,
    epoch: uint64
) -> bool:

    commitments = coordinator.get_commitments(claim_hash, epoch)

    // Condition 1: Enough commitments received (includes cover-traffic)
    threshold_met = len(commitments) >= REVEAL_THRESHOLD * expected_committee_size
    // REVEAL_THRESHOLD = 0.70 (default: 7 of 10 expected)

    // Condition 2: Submission window closed
    window_closed = now() > epoch_start(epoch) + SUBMISSION_WINDOW
    // SUBMISSION_WINDOW = 6 hours (default)

    RETURN threshold_met AND window_closed
```

**Phase 3: REVEAL**

```
FUNCTION reveal_opinion(
    agent: Agent,
    claim: Claim,
    opinion: OpinionTuple,
    metadata: ConfidenceMeta,
    nonce: bytes32,
    original_commitment: Commitment
) -> RevealResult:

    // Recompute commitment to verify consistency
    payload = canonical_serialize(opinion) || canonical_serialize(metadata) || nonce
    expected_hash = SHA256(payload)

    IF expected_hash != original_commitment.commitment_hash:
        RETURN RevealResult{
            status: "COMMITMENT_MISMATCH",
            penalty: REVEAL_MISMATCH_PENALTY  // 50 AIC default
        }

    // Submit reveal with VRF proof of committee membership
    reveal = Reveal{
        claim_hash:  claim.hash,
        epoch:       current_epoch(),
        agent_id:    agent.id,
        opinion:     opinion,
        metadata:    metadata,
        nonce:       nonce,
        vrf_proof:   agent.vrf_proof_for(claim),
        revealed_at: now()
    }

    coordinator.submit_reveal(reveal)

    // Coordinator verifies VRF proof; filters cover-traffic reveals
    RETURN RevealResult{status: "ACCEPTED"}
```

**REQ-M2-001:** Opinions MUST be committed using SHA-256 over canonically serialized opinion tuples with a 256-bit CSPRNG nonce.

**REQ-M2-002:** Agent identity MUST be encrypted during the commit phase and MUST NOT be decryptable by any party other than the coordinator until the reveal phase.

**REQ-M2-003:** The coordinator MUST NOT begin the reveal phase until both conditions are met: (a) the submission window has closed, and (b) at least REVEAL_THRESHOLD fraction of expected commitments have been received.

**REQ-M2-004:** A revealed opinion that does not match its commitment hash MUST be rejected and the REVEAL_MISMATCH_PENALTY applied.

### 5.4 Non-Reveal Handling

| Scenario | Response | Severity |
|---|---|---|
| Agent commits, does not reveal, no explanation | Forfeit committee stake; opinion counted as max-uncertainty (0, 0, 1, a) | MILD |
| Agent commits, does not reveal, 3+ times in 50 epochs | Forfeit stake + temporary committee exclusion (10 epochs) | MODERATE |
| Agent commits, does not reveal, 5+ times in 50 epochs | Forfeit stake + Sentinel Graph flag + permanent exclusion until cleared | SEVERE |
| All committee members fail to reveal | Claim reassigned to fresh committee; all non-revealers flagged | EMERGENCY |

**Default opinion for non-revealers:** `(b=0, d=0, u=1, a=base_rate)` — maximum uncertainty. This ensures non-reveals do not skew the fused opinion in any direction.

**REQ-M2-005:** Non-revealed opinions MUST be substituted with maximum-uncertainty opinion tuples (b=0, d=0, u=1, a=base_rate).

**REQ-M2-006:** The system MUST track non-reveal frequency per agent and apply graduated penalties as specified in the non-reveal handling table.

**REQ-M2-007:** If all committee members fail to reveal, the claim MUST be reassigned to a freshly selected committee.

### 5.5 Liveness Requirements

| Requirement | Value | Consequence of Violation |
|---|---|---|
| Minimum commitment rate | 70% of expected committee | If not met by window close, extend by 2 hours (once) |
| Minimum reveal rate | 70% of commitments | If not met, proceed with available reveals + non-reveal defaults |
| Maximum window extensions | 1 per claim | After second window, proceed regardless |
| Coordinator availability | 99.9% uptime | Coordinator failure: fall back to on-chain commitment submission |

**REQ-M2-008:** The system MUST support at most MAX_WINDOW_EXTENSIONS (default: 1) extensions of the submission window per claim.

**REQ-M2-009:** If the coordinator is unavailable, the system MUST fall back to on-chain commitment submission via C8 DSF's settlement plane.

### 5.6 Merkle-Anchored Commitment Batching

To minimize on-chain cost while maintaining auditability:

```
FUNCTION anchor_commitments(epoch: uint64) -> MerkleRoot:

    // Collect all commitments for this epoch across all claims
    all_commitments = coordinator.get_all_commitments(epoch)

    // Build Merkle tree over canonically sorted commitments
    leaves = [SHA256(canonical_serialize(c)) for c in sorted(all_commitments)]
    merkle_tree = build_merkle_tree(leaves)

    // Anchor root on-chain (one transaction per epoch)
    tx = submit_to_settlement_plane(
        op_type: "AVAP_COMMITMENT_ANCHOR",
        epoch:   epoch,
        merkle_root: merkle_tree.root,
        commitment_count: len(all_commitments)
    )

    RETURN merkle_tree.root
```

Any party can verify inclusion of a specific commitment using a Merkle proof. This provides post-hoc auditability at one on-chain transaction per epoch.

**REQ-M2-010:** All commitments for an epoch MUST be anchored in a Merkle tree with the root submitted to C8 DSF's settlement plane.

**REQ-M2-011:** The system MUST provide Merkle inclusion proofs on demand for any commitment within a retained epoch.

### 5.7 Integration with C5 Subjective Logic

AVAP's sealed opinion format is identical to C5's opinion tuple format. The commit-reveal wraps the existing pipeline transparently:

```
BEFORE AVAP:   Agent -> (opinion) -> PCVM Opinion Fusion
WITH AVAP:     Agent -> (commitment) -> Buffer -> (reveal) -> PCVM Opinion Fusion
```

The PCVM Opinion Fusion engine (C5 Section 6, Phase 6) operates on revealed opinions identically to how it would without AVAP. AVAP is transparent to the fusion algorithm.

**REQ-M2-012:** The commit-reveal protocol MUST NOT alter the opinion tuple format or the PCVM fusion algorithm. AVAP MUST be transparent to downstream opinion processing.

---

## 6. Mechanism 3: Honeypot Claims

### 6.1 Design Rationale

Honeypot claims are synthetic verification tasks with known ground truth, injected into the verification pipeline indistinguishably from real claims. An agent that rubber-stamps a honeypot — approving a deliberately flawed claim — reveals dishonest verification behavior. Honeypots provide the only mechanism in AVAP that produces direct, ground-truth evidence of individual agent malfeasance.

### 6.2 Claim Class Coverage

| Claim Class | Coverage Tier | Honeypot Feasibility | Injection Rate | Generator Type |
|---|---|---|---|---|
| D (Deterministic) | Tier 1 — Full | HIGH: ground truth computable | 5% of D-class claims | Automated |
| E (Empirical) | Tier 1 — Full | HIGH: data fabrication detectable | 5% of E-class claims | Semi-automated (GAN) |
| C (Compliance) | Tier 2 — Partial | MODERATE: regulatory ground truth constructible from known standards | 2% of C-class claims | Human-assisted |
| S (Subjective) | Tier 2 — Partial | MODERATE: consensus views usable as truth | 2% of S-class claims | Expert-panel calibrated |
| P (Process) | Tier 2 — Partial | MODERATE: process correctness verifiable against known workflows | 2% of P-class claims | Semi-automated |
| R (Reasoning) | Tier 2 — Partial | MODERATE: reasoning chain validity testable against known logical structures | 2% of R-class claims | Semi-automated |
| H (Heuristic) | Tier 3 — Excluded | LOW: no reliable ground truth | 0% | N/A |
| N (Novel) | Tier 3 — Excluded | LOW: no reliable ground truth | 0% | N/A |
| K (Knowledge) | Tier 3 — Excluded | LOW: consolidation claims are subjective | 0% | N/A |

**Effective system-wide honeypot rate:** ~2.5-3.5% of total claim volume (depending on class distribution).

**REQ-M3-001:** Honeypot injection MUST cover Tier 1 classes (D, E) at a minimum injection rate of 2% per class.

**REQ-M3-002:** Honeypot injection MUST NOT be applied to Tier 3 classes (H, N, K) where ground truth is unreliable.

### 6.3 Honeypot Generation Pipeline

#### 6.3.1 D-Class Generator (Automated)

```
FUNCTION generate_d_class_honeypot(
    template_library: ProofLibrary,
    epoch: uint64
) -> HoneypotClaim:

    // Step 1: Select a valid proof from the curated library
    template = template_library.select_random(
        class: "D",
        difficulty: UNIFORM_RANDOM(EASY, MEDIUM, HARD),
        seed: SHA256(b"HONEYPOT_D" || uint64_be(epoch) || csprng_bytes(16))
    )

    // Step 2: Inject a subtle error from the error taxonomy
    error_type = select_error_type([
        "OFF_BY_ONE",                  // Boundary off by 1 in proof step
        "BOUNDARY_ERROR",              // Incorrect boundary condition
        "LOGICAL_FALLACY",             // Non-sequitur in reasoning chain
        "INCORRECT_LEMMA_APPLICATION", // Lemma applied outside valid domain
        "SIGN_ERROR",                  // Sign flip in equation
        "QUANTIFIER_SWAP"              // Forall/exists swap
    ])
    mutated_proof = inject_error(template.proof, error_type)

    // Step 3: Oracle verification — confirm the error IS an error
    oracle_result = proof_oracle.verify(mutated_proof)
    ASSERT oracle_result.is_invalid,
        "Error injection did not produce an invalid proof"

    // Step 4: Difficulty calibration
    // Run through N independent verifier simulations
    detection_rate = simulate_detection(
        mutated_proof,
        N = 10,
        verifier_quality = "COMPETENT"
    )
    // Target: 60-90% detection by competent verifiers
    IF detection_rate < 0.40 OR detection_rate > 0.95:
        RETURN generate_d_class_honeypot(template_library, epoch)  // Regenerate

    // Step 5: Package as claim with identical metadata to real claims
    honeypot = HoneypotClaim{
        claim_content:           mutated_proof.as_claim(),
        ground_truth:            "INVALID",
        error_type:              error_type,
        error_location:          mutated_proof.error_location,
        expected_detection_rate: detection_rate,
        class:                   "D",
        generation_epoch:        epoch,
        template_id:             template.id,
        canary_variants:         generate_canary_variants(mutated_proof, N_VARIANTS=3)
    }

    RETURN honeypot
```

**REQ-M3-003:** D-class honeypots MUST pass oracle verification confirming the injected error renders the proof invalid.

**REQ-M3-004:** D-class honeypots MUST have a simulated detection rate between 0.40 and 0.95 among competent verifiers. Honeypots outside this range MUST be regenerated.

#### 6.3.2 E-Class Generator (Semi-Automated, GAN-Based)

```
FUNCTION generate_e_class_honeypot(
    data_corpus: RealDataCorpus,
    gan_model: SyntheticDataGAN,
    epoch: uint64
) -> HoneypotClaim:

    // Step 1: Select a real claim template
    real_claim = data_corpus.select_random(class: "E", epoch_seed: epoch)

    // Step 2: Generate synthetic data with controlled statistical error
    error_type = select_error_type([
        "CONFOUNDED_CORRELATION",   // Correlation vanishes under proper controls
        "SIMPSON_PARADOX",          // Aggregate trend reverses in subgroups
        "SURVIVORSHIP_BIAS",        // Data excludes critical failures
        "P_HACKING_ARTIFACT",       // Significance disappears with correction
        "DISTRIBUTION_MISMATCH"     // Reported distribution mismatches data
    ])

    synthetic_data = gan_model.generate(
        template: real_claim.data,
        injected_error: error_type,
        indistinguishability_target: 0.55  // Discriminator accuracy < 55%
    )

    // Step 3: GAN discriminator quality assurance
    discriminator_accuracy = discriminator_test(
        real_samples:      data_corpus.sample(N=100),
        synthetic_samples: [synthetic_data] + gan_model.generate_batch(N=99),
        discriminator:     SOTA_DISCRIMINATOR
    )

    IF discriminator_accuracy > HONEYPOT_DISCRIMINATOR_THRESHOLD:  // 0.60
        LOG("E-class honeypot failed discriminator test",
            accuracy=discriminator_accuracy)
        RETURN generate_e_class_honeypot(data_corpus, gan_model, epoch)

    // Step 4: Package as claim
    honeypot = HoneypotClaim{
        claim_content:           format_e_class_claim(synthetic_data, real_claim.structure),
        ground_truth:            "INVALID",
        error_type:              error_type,
        error_details:           synthetic_data.error_specification,
        expected_detection_rate: 0.65,
        class:                   "E",
        generation_epoch:        epoch,
        discriminator_accuracy:  discriminator_accuracy,
        canary_variants:         generate_canary_variants(synthetic_data, N_VARIANTS=3)
    }

    RETURN honeypot
```

**REQ-M3-005:** E-class honeypots MUST pass the GAN discriminator test with accuracy below HONEYPOT_DISCRIMINATOR_THRESHOLD (default: 0.60).

**REQ-M3-006:** E-class honeypots MUST contain at least one verifiable statistical error from the error taxonomy.

#### 6.3.3 C/S-Class Generators

**C-class (Compliance, Human-Assisted):**
- Compliance domain experts construct claims against known regulatory standards with deliberate non-compliance errors (e.g., incorrect threshold application, misclassified regulatory category, outdated standard reference)
- Each honeypot requires ~2 hours of expert time
- Production rate: ~5 honeypots per class per 100 epochs
- Quality control: panel of 3 compliance experts must agree the non-compliance error is real and non-trivial
- Ground truth derived from authoritative regulatory standards, making Compliance claims more amenable to honeypot testing than subjective claim classes

**S-class (Expert-Panel Calibrated):**
- Claims selected where 5+ domain experts independently agree on verdict
- Only claims with >80% panel agreement qualify as honeypots
- Production rate: limited by expert availability (~3-5 per 100 epochs)
- Used sparingly due to fuzzy boundary between "consensus" and "contested"

**REQ-M3-007:** C-class honeypots MUST be validated by a panel of at least 3 domain experts who independently agree the error is real and non-trivial.

**REQ-M3-008:** S-class honeypots MUST achieve at least 80% agreement among a panel of 5+ domain experts on the expected verdict.

#### 6.3.4 P/R-Class Generators (Semi-Automated)

**P-class (Process Verification):**
- Honeypots test for collusion in process verification claims by constructing claims where the described process contains a known procedural violation (e.g., skipped mandatory step, incorrect sequencing, violated precondition)
- Ground truth derived from formally specified process definitions (workflow schemas, protocol specifications)
- Semi-automated: process templates are drawn from a curated library of known-correct workflows; errors are injected automatically; a domain expert validates each honeypot
- Production rate: ~8-10 honeypots per 100 epochs (higher than C/S due to semi-automation)
- Quality control: injected error must be detectable by a competent verifier who checks the process definition

**R-class (Reasoning Chain Validation):**
- Honeypots test for collusion in reasoning chain validation claims by constructing claims where the reasoning chain contains a known logical error (e.g., affirming the consequent, invalid modus ponens application, unsupported intermediate step, circular dependency)
- Ground truth derived from formal logic validation: the reasoning chain is checked against known inference rules
- Semi-automated: valid reasoning chains are selected from a curated corpus; logical errors are injected at random positions; a domain expert confirms the error breaks the chain
- Production rate: ~8-10 honeypots per 100 epochs
- Quality control: the logical error must invalidate the conclusion but not be trivially obvious (calibrated difficulty matching D-class standards)

**REQ-M3-019:** P-class honeypots MUST contain at least one verifiable procedural violation from the process error taxonomy.

**REQ-M3-020:** R-class honeypots MUST contain at least one formally verifiable logical error that invalidates the reasoning chain's conclusion.

### 6.4 Canary Trap Variant Generation

Each honeypot is distributed in 2-3 variants. Variants differ in truth-irrelevant details, enabling identification of which committee member leaked claim content.

```
FUNCTION generate_canary_variants(
    base_claim: HoneypotClaim,
    n_variants: int
) -> List<CanaryVariant>:

    variants = []
    FOR i IN 0..n_variants-1:
        variant = CanaryVariant{
            variant_id:    SHA256(base_claim.claim_id || uint32_be(i)),
            base_claim_id: base_claim.claim_id,
            modifications: []
        }

        // Apply truth-irrelevant modifications unique to this variant
        mods = select_modifications(base_claim.class, seed=variant.variant_id)
        // Possible modifications (all truth-preserving):
        //   - Evidence ordering (shuffle source list)
        //   - Numerical formatting (3.14159 vs 3.1416 vs pi)
        //   - Synonym substitution in non-technical text
        //   - Date formatting (2026-03-10 vs March 10, 2026)
        //   - Citation style (APA vs inline vs footnote)
        //   - Paragraph ordering (where order does not affect meaning)

        variant.content = apply_modifications(base_claim.content, mods)
        variant.modifications = mods
        variant.fingerprint = SHA256(variant.content)

        variants.append(variant)

    RETURN variants
```

**Anti-fingerprinting countermeasure:** To prevent colluders from using variant detection as a honeypot signal, ~10% of real claims are also distributed with superficial reformatting:

```
FUNCTION should_add_real_claim_variants(claim: Claim, epoch: uint64) -> bool:
    variant_seed = SHA256(b"REAL_VARIANT" || claim.hash || uint64_be(epoch))
    RETURN uint256_from_bytes(variant_seed) < (REAL_VARIANT_RATE * 2^256)
    // REAL_VARIANT_RATE = 0.10
```

**REQ-M3-009:** Canary variants MUST differ only in truth-irrelevant details. No variant modification may change the correctness or error status of the claim.

**REQ-M3-010:** At least REAL_VARIANT_RATE (default: 10%) of real claims MUST receive variant treatment to dilute the "variant = honeypot" signal.

### 6.5 Indistinguishability Requirements (HG-1)

For honeypots to be effective, they must be statistically indistinguishable from real claims:

| Feature | Matching Requirement | Verification Method |
|---|---|---|
| Claim length (tokens) | KL divergence < 0.05 | Distribution test per epoch |
| Vocabulary distribution | Chi-squared p > 0.10 | Token frequency analysis |
| Structural format | Identical schema compliance | Schema validation |
| Metadata patterns | Identical timestamp/submission pipeline | Injection through same pipeline |
| Citation count/style | Within 1 sigma of real distribution | Per-class distribution test |
| VTD structure | Identical to real VTDs | Schema validation |
| Source availability | Real sources cited (for E-class) | Source fetch test |
| Knowledge graph context | Referenced claims exist in graph | Graph connectivity check |

**REQ-M3-011:** Honeypot claims MUST be injected through the same submission pipeline as real claims, with identical metadata patterns.

**REQ-M3-012:** The KL divergence between honeypot and real claim length distributions MUST be below 0.05 for each Tier 1 class.

**REQ-M3-013:** The HG-1 discriminator test (see Appendix B) MUST be run quarterly. If accuracy exceeds 0.60 for any Tier 1 class, the honeypot corpus for that class MUST be regenerated within 5 epochs.

### 6.6 Honeypot Lifecycle

```
CREATION:
  Honeypot generated by class-specific generator
  Quality-assured (oracle verification, difficulty calibration, discriminator test)
  Stored in Honeypot Vault (encrypted, access-controlled)

INJECTION:
  During claim assignment, Honeypot Engine probabilistically substitutes real
  claims with honeypots at the class-specific injection rate
  Injection decision is VRF-based: deterministic but unpredictable
  Injected honeypot uses same metadata pipeline as real claims

EVALUATION:
  After opinion reveal, if claim was honeypot:
    Compare each agent's opinion against ground truth
    Agent who rated invalid claim as valid (b > HONEYPOT_PASS_THRESHOLD = 0.60):
      -> HONEYPOT_FAILURE recorded
    Agent who correctly identified the flaw (d > HONEYPOT_DETECT_THRESHOLD = 0.40):
      -> HONEYPOT_PASS recorded
    Agent with high uncertainty (u > 0.50):
      -> HONEYPOT_UNCERTAIN (neutral, not penalized)

RETIREMENT:
  Honeypot retired after MAX_HONEYPOT_USES exposures (default: 50)
  Or after discriminator test shows accuracy > 0.60 for this honeypot's class
  Retired honeypots archived (not deleted) for audit trail
```

**REQ-M3-014:** Honeypot injection decisions MUST be VRF-based (deterministic but unpredictable) using the epoch VRF seed.

**REQ-M3-015:** Honeypots MUST be retired after MAX_HONEYPOT_USES (default: 50) exposures.

**REQ-M3-016:** Retired honeypots MUST be archived for audit purposes and MUST NOT be deleted.

### 6.7 Graduated Response to Honeypot Failure

| Failure Count (rolling 100 epochs) | Response | Severity |
|---|---|---|
| 1 failure | Log only; feed into CSS (M5) | NOTICE |
| 2 failures | Elevated audit rate (+20% audit probability) | WARNING |
| 3 failures | Elevated audit + temporary committee exclusion (5 epochs) + CSS penalty | MODERATE |
| 5 failures | Enterprise liability audit (M4c) + committee exclusion (25 epochs) | SEVERE |
| 7+ failures | Full retroactive audit + permanent exclusion + slashing recommendation | CRITICAL |

**False positive protection:** A single honeypot failure is never penalized beyond logging. Honest agents may occasionally misjudge a subtle error, especially in Tier 2 classes. The graduated response ensures only patterns of failure trigger consequences.

**REQ-M3-017:** A single honeypot failure MUST NOT trigger any penalty beyond logging and CSS input.

**REQ-M3-018:** Automated slashing recommendations from honeypot failures MUST require at least 7 failures in a rolling 100-epoch window.

### 6.8 Honeypot Budget

| Cost Component | Per-Epoch Cost | Annual Cost (365 epochs) | Notes |
|---|---|---|---|
| D-class generation | 0.5 GPU-hours | 182 GPU-hours | Fully automated |
| E-class generation | 2.0 GPU-hours (GAN) | 730 GPU-hours | GAN training amortized |
| C-class generation | 2 expert-hours | 730 expert-hours | ~0.36 FTE |
| S-class generation | 1.5 expert-hours | 548 expert-hours | ~0.26 FTE |
| Discriminator testing | 1.0 GPU-hours | 365 GPU-hours | Quarterly full test |
| Storage (Honeypot Vault) | 0.5 GB | 182 GB | Encrypted, access-controlled |
| **Total compute** | **3.5 GPU-hours** | **1,277 GPU-hours** | |
| **Total expert time** | **3.5 hours** | **1,278 hours (~0.62 FTE)** | |

---

## 7. Mechanism 4: Collusion Deterrence Payment

### 7.1 Three Sub-Mechanisms

M4 consists of three complementary deterrence mechanisms:

```
M4 = M4a (Asymmetric Information Injection)
   + M4b (Graduated Temporal Bounty)
   + M4c (Enterprise Liability)
```

### 7.2 M4a: Asymmetric Information Injection

**Purpose:** Destabilize pre-commitment contracts within collusion rings by injecting uncertainty about whether the ring is already under investigation.

```
FUNCTION inject_uncertainty(
    agent_pool: Set<Agent>,
    epoch: uint64
) -> List<UncertaintyNotification>:

    notifications = []

    // Select ~2% of agents per epoch to receive notifications
    n_notifications = ceil(UNCERTAINTY_INJECTION_RATE * len(agent_pool))
    // UNCERTAINTY_INJECTION_RATE = 0.02

    FOR i IN 0..n_notifications-1:
        // VRF-based selection (deterministic but unpredictable)
        seed = SHA256(b"M4A_INJECT" || uint64_be(epoch) || uint32_be(i))
        target_idx = uint256_from_bytes(seed) % len(agent_pool)
        target_agent = agent_pool[target_idx]

        // Generate plausible investigation notice
        notification = UncertaintyNotification{
            recipient:       target_agent.id,
            epoch:           epoch,
            message_type:    select_message_type(seed),
            // Message types (selected by VRF):
            //   "ROUTINE_AUDIT_SELECTION" — routine quality assurance review
            //   "CORRELATION_NOTICE" — unusual correlation patterns detected
            //   "ANONYMOUS_TIP_RECEIVED" — anonymous report received
            delivery_channel: "PRIVATE_NOTIFICATION",
            expires_after:   5  // Self-destructs after 5 epochs
        }

        notifications.append(notification)

    RETURN notifications
```

**Game-theoretic effect:**

Without asymmetric information injection, a colluder computes:
```
E[stay] = ongoing_collusion_value  (if undetected)
E[defect] = Bounty - Deposit
```

With injection, the colluder faces uncertainty about investigation probability p:
```
E[stay] = (1-p) * ongoing_collusion_value - p * (Stake + enterprise_liability)
```

If the colluder believes p > 0 (which notifications induce), E[stay] decreases. As ring history grows, enterprise_liability grows super-linearly, making p * enterprise_liability increasingly dominant.

**Critical constraints on notifications:**
1. Plausible enough that colluders cannot dismiss them
2. Common enough (2% of all agents) that receiving one is not evidence of targeting
3. Vague enough that honest agents are not alarmed

**REQ-M4-001:** Uncertainty notifications MUST be delivered to at least UNCERTAINTY_INJECTION_RATE (default: 2%) of the agent pool per epoch.

**REQ-M4-002:** Notification selection MUST be VRF-based and deterministic. The notification rate MUST be high enough that receiving a notification is not evidence of being targeted.

**REQ-M4-003:** Notifications MUST auto-expire after 5 epochs.

### 7.3 M4b: Graduated Temporal Bounty

```
STRUCTURE CDPBounty:
    reporter_id:        bytes32         // ZK-hidden identity
    ring_members:       List<AgentID>   // Alleged colluders (partial list OK)
    evidence:           CDPEvidence     // Coordination artifacts, behavioral predictions
    epoch_of_report:    uint64
    estimated_ring_age: uint64          // Epochs since ring formation

FUNCTION compute_bounty(
    report: CDPReport,
    verified: bool,
    ring_stake: uint64,            // Total AIC staked by identified ring members
    corrupted_claim_value: uint64  // Estimated value of corrupted claims
) -> uint64:

    IF NOT verified:
        RETURN 0

    ring_age = report.estimated_ring_age

    IF ring_age <= EARLY_DEFECTION_WINDOW:             // 10 epochs
        base_bounty = ring_stake * EARLY_BOUNTY_RATE    // 0.50
        claim_bounty = 0
        self_penalty_reduction = 0.70                    // 70% penalty reduction

    ELIF ring_age <= MID_DEFECTION_WINDOW:              // 50 epochs
        base_bounty = ring_stake * MID_BOUNTY_RATE      // 0.35
        claim_bounty = corrupted_claim_value * 0.10
        self_penalty_reduction = 0.80

    ELSE:                                               // 50+ epochs
        base_bounty = ring_stake * LATE_BOUNTY_RATE     // 0.25
        claim_bounty = corrupted_claim_value * 0.05
        self_penalty_reduction = 0.90                    // Near-immunity for late defectors

    total_bounty = base_bounty + claim_bounty

    // Cap at MAX_BOUNTY_CAP of ring's total forfeited stake
    total_bounty = min(total_bounty, ring_stake * MAX_BOUNTY_CAP)  // 0.60

    RETURN total_bounty
```

**Bounty funding source:** Bounties are paid from forfeited stakes of confirmed ring members. No new AIC is created. If forfeited stake is insufficient, the bounty is capped at available forfeiture.

**REQ-M4-004:** Bounties MUST be funded exclusively from forfeited stakes of confirmed ring members. The system MUST NOT create new AIC for bounties.

**REQ-M4-005:** Bounties MUST be capped at MAX_BOUNTY_CAP (default: 0.60) of the ring's total forfeited stake.

**REQ-M4-006:** The bounty schedule MUST incentivize early defection by offering higher base rates for younger rings.

### 7.4 M4c: Enterprise Liability

When collusion is detected, a retroactive audit is triggered for all claims ever verified by any identified ring member.

```
FUNCTION trigger_enterprise_liability(
    ring_members: Set<AgentID>,
    detection_epoch: uint64,
    detection_mechanism: str
) -> EnterpriseAuditScope:

    // Step 1: Compute audit scope — all claims where ring members served
    audit_claims = Set()
    FOR agent IN ring_members:
        agent_claims = get_committee_history(agent, lookback=AUDIT_LOOKBACK_EPOCHS)
        // AUDIT_LOOKBACK_EPOCHS = 500 (default)
        audit_claims.update(agent_claims)

    // Step 2: Prioritize by risk
    prioritized = []
    FOR claim IN audit_claims:
        ring_member_count = count_ring_members_on_committee(claim, ring_members)
        claim_value = get_claim_value(claim)
        risk_score = ring_member_count * claim_value
        prioritized.append((claim, risk_score))

    prioritized.sort(key=lambda x: x[1], reverse=True)

    // Step 3: Audit top ENTERPRISE_AUDIT_DEPTH claims
    audit_scope = EnterpriseAuditScope{
        ring_members:        ring_members,
        detection_epoch:     detection_epoch,
        detection_mechanism: detection_mechanism,
        total_claims:        len(audit_claims),
        audit_depth:         min(ENTERPRISE_AUDIT_DEPTH, len(prioritized)),
        // ENTERPRISE_AUDIT_DEPTH = 100 (default)
        prioritized_claims:  prioritized[:ENTERPRISE_AUDIT_DEPTH],
        estimated_cost:      estimate_audit_cost(prioritized[:ENTERPRISE_AUDIT_DEPTH])
    }

    RETURN audit_scope
```

**Credibility cascade on confirmed collusion:**

```
FUNCTION compute_credibility_cascade(
    agent: AgentID,
    audit_results: List<AuditResult>
) -> CredibilityCascade:

    cascade = CredibilityCascade{agent: agent}

    FOR result IN audit_results:
        IF result.verdict == "COLLUSION_CONFIRMED":
            // Reset claim credibility to maximum uncertainty
            claim = result.claim
            claim.opinion = OpinionTuple(b=0, d=0, u=1, a=claim.base_rate)

            // Cascade to dependent claims in knowledge graph
            dependents = get_dependent_claims(claim)
            FOR dep IN dependents:
                cascade_factor = CASCADE_ATTENUATION ** distance(claim, dep)
                // CASCADE_ATTENUATION = 0.50
                dep.opinion.belief *= cascade_factor
                dep.opinion.uncertainty += dep.opinion.belief * (1 - cascade_factor)

            // Agent credibility reduction
            agent_cred = get_agent_credibility(agent, claim.class)
            penalty = ENTERPRISE_CREDIBILITY_PENALTY  // 0.15
            agent_cred.belief = max(0, agent_cred.belief - penalty)
            agent_cred.uncertainty += penalty

            cascade.affected_claims.append(claim)
            cascade.affected_dependents.extend(dependents)

    RETURN cascade
```

**REQ-M4-007:** Enterprise liability audits MUST look back at least AUDIT_LOOKBACK_EPOCHS (default: 500) epochs.

**REQ-M4-008:** Enterprise audits MUST prioritize claims by risk score (ring_member_count * claim_value) and audit the top ENTERPRISE_AUDIT_DEPTH claims.

**REQ-M4-009:** Confirmed collusion MUST trigger a credibility cascade that resets affected claims to maximum uncertainty and attenuates dependent claims by CASCADE_ATTENUATION per hop.

### 7.5 Zero-Knowledge CDP Reporting (HG-2)

**Problem:** A reporter must prove they are a ring member (preventing fabricated reports) without revealing which member they are (preventing MAD contract enforcement by the ring).

**Protocol: Linkable Ring Signature + Pedersen Commitment**

```
PROTOCOL ZK_CDP_Report:

    // SETUP: Reporter R is member of ring {A1, A2, ..., An} where R = Ai

    // Step 1: Ring Signature over Report
    // Proves "one of {A1..An} signed this" without revealing which
    // Uses Linkable Ring Signature (Fujisaki-Suzuki 2007) for double-report prevention

    report_content = CDPEvidence{
        ring_size:              n,
        coordination_proof:     encrypted_coordination_artifacts,
        behavioral_predictions: [
            // Predictions only a ring member could make
            // e.g., "Agent Aj will vote APPROVE on claim C_next if pattern P"
        ],
        historical_pattern: [
            // Specific claim IDs where collusion occurred
            // with predictions of ring member votes
        ]
    }

    // Step 2: Pedersen Commitment to Reporter Identity
    // C = g^{agent_id} * h^{r} where r is random blinding factor
    // ZK: reveals nothing about agent_id
    // Openable later for bounty claim
    membership_commitment = pedersen_commit(
        value:    reporter.agent_id,
        blinding: random_scalar()
    )

    // Step 3: Linkable Ring Signature
    ring_pubkeys = [get_pubkey(a) for a in ring_members]
    ring_sig = linkable_ring_sign(
        message:    SHA256(canonical_serialize(report_content)),
        ring:       ring_pubkeys,
        signer_key: reporter.privkey,
        link_tag:   SHA256(b"CDP_LINK" || ring_id)
        // Link tag ensures same reporter cannot submit multiple reports
        // for the same ring (linkability) without revealing identity
    )

    // Step 4: Submit ZK Report
    zk_report = ZKCDPReport{
        report_content:        report_content,
        membership_commitment: membership_commitment,
        ring_signature:        ring_sig,
        alleged_ring_pubkeys:  ring_pubkeys,
        submission_epoch:      current_epoch()
    }

    // Verification by system:
    // 1. Verify ring signature (proves reporter is in alleged ring)
    // 2. Check linkability tag (prevents double-reporting)
    // 3. Evaluate evidence quality (predictions, historical patterns)
    // 4. If evidence passes threshold: trigger investigation
    // 5. Bounty escrowed until investigation completes
    // 6. Reporter claims bounty by opening Pedersen commitment
    //    to isolated bounty channel (identity not shared with ring)
```

**Evidence requirements for CDP reports:**

| Evidence Type | Required? | Verification Method |
|---|---|---|
| Behavioral predictions (future votes) | YES | Wait for predicted claims; check outcomes |
| Historical coordination artifacts | RECOMMENDED | Cross-reference sealed opinion records |
| Communication channel identification | OPTIONAL | Cannot verify out-of-band channels |
| Ring membership list (partial OK) | YES | Ring signature proves reporter is in claimed set |
| Coordination protocol description | RECOMMENDED | Used to design targeted honeypots |

**Fallback if ZK infeasible:** Reporter-pseudonymous reporting using a one-time DID unlinked to main identity. Identity protected by system policy (weaker: trust-based rather than cryptographic).

**REQ-M4-010:** CDP reports MUST include a valid Linkable Ring Signature proving the reporter is a member of the alleged ring.

**REQ-M4-011:** The system MUST check the linkability tag to prevent double-reporting for the same ring by the same reporter.

**REQ-M4-012:** CDP reports MUST include at least one verifiable behavioral prediction.

**REQ-M4-013:** Bounty disbursement MUST occur through an isolated channel that does not reveal reporter identity to ring members.

### 7.6 C8 DSF Integration

| DSF Operation | AVAP Trigger | Amount | Settlement Speed |
|---|---|---|---|
| `SLASH` (collusion) | Ring detection confirmed | Graduated per offense | V-class (N-epoch) |
| `AIC_TRANSFER` (bounty) | CDP report verified | Per `compute_bounty()` | V-class (N-epoch) |
| `PENDING_INITIATE` (escrow) | CDP report received | Bounty estimate | B-class (per-epoch) |
| `PENDING_COMPLETE` (release) | Investigation confirms | Escrowed amount | V-class |
| `PENDING_TIMEOUT` (return) | Investigation finds false | Escrowed amount returned | B-class |

**Slashing schedule for collusion (extends C8 Section 10.3):**

| Offense | Penalty | Cooldown | Recovery Path |
|---|---|---|---|
| 1st honeypot-detected | 10% staked AIC | 25 epochs exclusion | Clean 100 epochs |
| 2nd offense | 25% staked AIC | 50 epochs exclusion | Clean 200 epochs |
| 3rd offense | 50% staked AIC | 100 epochs exclusion | Clean 500 epochs |
| Enterprise liability | 100% forfeiture | Permanent exclusion pending appeal | G-class governance appeal |

**REQ-M4-014:** Collusion slashing MUST follow the graduated schedule. First offense MUST NOT exceed 10% of staked AIC.

**REQ-M4-015:** Enterprise liability total forfeiture MUST be appealable through G-class governance vote.

---

## 8. Mechanism 5: Conditional Behavioral Analysis

### 8.1 Design Rationale

M5 operates as a continuous screening system that computes a Collusion Suspicion Score (CSS) for each agent based on whether their opinions change depending on the presence of specific "allies" on the committee. CSS is one input to the Multi-Signal Fusion Classifier, not a standalone verdict.

### 8.2 Conditional Mutual Information Computation

The core statistical test: does agent A's opinion distribution shift when agent B is on the same committee?

```
FUNCTION compute_conditional_deviation(
    agent_a: AgentID,
    agent_b: AgentID,
    lookback_epochs: int
) -> ConditionalDeviation:

    // Gather all committees where agent_a participated
    a_committees = get_committee_history(agent_a, lookback_epochs)

    // Partition by agent_b's presence/absence
    b_present = [c for c in a_committees if agent_b in c.members]
    b_absent  = [c for c in a_committees if agent_b not in c.members]

    IF len(b_present) < MIN_SHARED_COMMITTEES:  // default: 30
        RETURN ConditionalDeviation{
            status: "INSUFFICIENT_DATA",
            delta: 0.0,
            confidence: 0.0
        }

    // Compute opinion distance from committee majority in each partition
    // Uses continuous distance (not binary agree/disagree) for statistical power
    opinions_when_b_present = [
        opinion_distance(a_opinion, committee_majority)
        FOR c IN b_present
        FOR a_opinion, committee_majority IN get_opinion_pair(agent_a, c)
    ]

    opinions_when_b_absent = [
        opinion_distance(a_opinion, committee_majority)
        FOR c IN b_absent
        FOR a_opinion, committee_majority IN get_opinion_pair(agent_a, c)
    ]

    // Statistical test: Mann-Whitney U (non-parametric, handles non-normal)
    // H0: mean opinion distance is same regardless of B's presence
    // H1: mean opinion distance differs (two-tailed)
    stat, p_value = mannwhitneyu(
        opinions_when_b_present,
        opinions_when_b_absent,
        alternative='two-sided'
    )

    // Effect size (Cohen's d)
    mean_present = mean(opinions_when_b_present)
    mean_absent  = mean(opinions_when_b_absent)
    pooled_std   = sqrt(
        (var(opinions_when_b_present) + var(opinions_when_b_absent)) / 2
    )
    effect_size = (mean_present - mean_absent) / pooled_std if pooled_std > 0 else 0

    RETURN ConditionalDeviation{
        status:      "COMPUTED",
        delta:       abs(mean_present - mean_absent),
        effect_size: effect_size,
        p_value:     p_value,
        n_present:   len(b_present),
        n_absent:    len(b_absent),
        confidence:  1.0 - p_value
    }


FUNCTION opinion_distance(
    opinion_a: OpinionTuple,
    opinion_b: OpinionTuple
) -> float:
    // Euclidean distance in the opinion simplex
    RETURN sqrt(
        (opinion_a.belief - opinion_b.belief) ** 2 +
        (opinion_a.disbelief - opinion_b.disbelief) ** 2 +
        (opinion_a.uncertainty - opinion_b.uncertainty) ** 2
    )
```

**REQ-M5-001:** Pairwise conditional deviation MUST use the Mann-Whitney U test (two-tailed) for robustness to non-normal opinion distance distributions.

**REQ-M5-002:** Pairwise analysis MUST NOT be computed for agent pairs with fewer than MIN_SHARED_COMMITTEES (default: 30) shared committee memberships.

### 8.3 Collusion Suspicion Score (CSS)

```
FUNCTION compute_css(
    agent: AgentID,
    epoch: uint64,
    lookback_epochs: int = CSS_LOOKBACK  // default: 200
) -> float:

    // Step 1: Compute pairwise conditional deviations
    pool = get_agents_sharing_committees(agent, lookback_epochs, MIN_SHARED_COMMITTEES)
    deviations = []

    FOR other IN pool:
        dev = compute_conditional_deviation(agent, other, lookback_epochs)
        IF dev.status == "COMPUTED":
            deviations.append(dev)

    IF len(deviations) == 0:
        RETURN 0.0  // Insufficient data

    // Step 2: Identify significant deviations with FDR correction
    // Relaxed alpha = 0.10 (screening, not verdict)
    // Benjamini-Hochberg correction for multiple comparisons
    p_values = [d.p_value for d in deviations]
    significant = benjamini_hochberg(p_values, alpha=CSS_ALPHA)  // 0.10

    // Step 3: Aggregate into CSS, weighted by effect size
    weighted_sum = sum(
        d.effect_size FOR d, is_sig IN zip(deviations, significant) IF is_sig
    )
    raw_css = weighted_sum / len(deviations)

    // Step 4: Adjust for claim class composition
    // High-disagreement classes (H, S, C) have naturally higher variance
    class_distribution = get_verification_class_distribution(agent, lookback_epochs)
    expected_baseline = sum(
        CLASS_CSS_BASELINE[cls] * fraction
        FOR cls, fraction IN class_distribution.items()
    )
    // CLASS_CSS_BASELINE (empirically calibrated):
    //   D: 0.01, E: 0.03, C: 0.05, S: 0.06, H: 0.08, N: 0.04

    adjusted_css = max(0.0, raw_css - expected_baseline)

    // Step 5: Normalize to [0, 1]
    RETURN clamp(adjusted_css / CSS_NORMALIZATION_FACTOR, 0.0, 1.0)
    // CSS_NORMALIZATION_FACTOR = 0.20 (CSS of 0.20 = maximum suspicion)
```

**REQ-M5-003:** CSS computation MUST apply Benjamini-Hochberg FDR correction to all pairwise p-values before identifying significant deviations.

**REQ-M5-004:** CSS MUST be adjusted for claim class composition using empirically calibrated baselines to prevent false positives for agents who primarily verify high-disagreement claim classes.

**REQ-M5-005:** CSS MUST be recomputed every CSS_UPDATE_FREQUENCY (default: 10) epochs in batch mode.

### 8.4 Data Requirements

| Parameter | Value | Rationale |
|---|---|---|
| MIN_SHARED_COMMITTEES | 30 | Below 30, t-test has insufficient power for medium effect sizes |
| CSS_LOOKBACK | 200 epochs | Balances data volume against temporal relevance |
| CSS_ALPHA (FDR threshold) | 0.10 | Relaxed for screening; false flags handled downstream |
| Minimum pool for analysis | 50 agents | Below 50, pairwise test count too low for FDR correction |
| Update frequency | Every 10 epochs | Batch processing sufficient; no real-time requirement |

### 8.5 Multi-Signal Fusion Classifier

The fusion classifier combines signals from M3, M5, existing Layer 2, and M4 reports into a per-agent collusion probability estimate.

```
STRUCTURE FusionFeatures:
    // M3 Honeypot Signals
    honeypot_failure_rate:       float   // Failures / total honeypots (100-epoch window)
    honeypot_failure_count:      int     // Absolute count (recent 100 epochs)
    honeypot_severity_score:     float   // Weighted by honeypot difficulty

    // M5 Behavioral Signals
    css:                         float   // Collusion Suspicion Score
    max_pairwise_deviation:      float   // Largest single pairwise deviation
    significant_pairs_count:     int     // Number of significant deviations

    // Existing Layer 2 Signals (C10 Hardening)
    pairwise_agreement_anomaly:  float   // Z-score of pairwise agreement rate
    kl_divergence_from_baseline: float   // KL divergence of opinion distribution
    opinion_copying_index:       float   // Frequency of matching specific agents

    // M4 CDP Signals
    cdp_reports_involving:       int     // CDP reports naming this agent
    cdp_reports_verified:        int     // Verified reports

    // Metadata
    agent_age_epochs:            int     // Time active
    total_committees_served:     int     // Experience level
    claim_class_concentration:   float   // Concentration in specific classes
    sentinel_cluster_size:       int     // Sentinel Graph cluster size
```

**Classifier specification:**

```
FUNCTION train_fusion_classifier(
    labeled_data: List<(FusionFeatures, bool)>
) -> FusionClassifier:

    // Classifier: Gradient Boosted Decision Trees (XGBoost)
    // Rationale: handles mixed features, robust to correlation,
    //            interpretable importances, well-calibrated probabilities

    classifier = XGBoostClassifier(
        n_estimators:      100,
        max_depth:         5,
        learning_rate:     0.1,
        min_child_weight:  10,     // Conservative: avoid overfitting on small rings
        scale_pos_weight:  10.0,   // Class imbalance: colluders are rare
        eval_metric:       "aucpr" // Area under precision-recall curve
    )

    features_matrix = [f.as_vector() for f, label in labeled_data]
    labels = [label for f, label in labeled_data]

    classifier.fit(features_matrix, labels, eval_set=holdout)

    RETURN classifier


FUNCTION predict_collusion_probability(
    classifier: FusionClassifier,
    agent: AgentID,
    epoch: uint64
) -> float:

    features = extract_fusion_features(agent, epoch)
    RETURN classifier.predict_proba(features.as_vector())
```

**Expected signal performance:**

| Signal Source | Estimated AUC (alone) | Contribution to Fusion |
|---|---|---|
| M3 honeypot failure rate | 0.82 | PRIMARY (ground truth) |
| M5 CSS | 0.65 | SECONDARY (supporting) |
| Layer 2 pairwise agreement | 0.60 | SECONDARY |
| Layer 2 KL divergence | 0.58 | TERTIARY |
| M4 CDP reports | 0.55 (sparse) | TERTIARY |
| **Fusion (all signals)** | **0.88 (estimated)** | **Combined** |

**REQ-M5-006:** The fusion classifier MUST be retrained every CLASSIFIER_RETRAIN_INTERVAL (default: 50) epochs using updated labeled data.

**REQ-M5-007:** The fusion classifier MUST use calibrated probability outputs (Platt scaling or isotonic regression) to ensure P(collusion) thresholds correspond to actual risk levels.

### 8.6 Detection Thresholds and False Positive Control

| Threshold | Value | Action Triggered | Expected FPR |
|---|---|---|---|
| INVESTIGATION_THRESHOLD | P > 0.30 | Elevated audit (+20% deep-audit probability) | ~8% |
| ENHANCED_MONITORING_THRESHOLD | P > 0.50 | Targeted honeypots (2x rate) + continuous CSS | ~4% |
| SLASHING_RECOMMENDATION_THRESHOLD | P > 0.75 | Slashing recommendation (HITL required) | ~1% |
| ENTERPRISE_LIABILITY_THRESHOLD | P > 0.90 | Enterprise liability audit (M4c) | <0.5% |

**REQ-M5-008:** No automated slashing MUST occur below P(collusion) > 0.75.

**REQ-M5-009:** Slashing at the SLASHING_RECOMMENDATION_THRESHOLD MUST require human-in-the-loop confirmation before execution.

**REQ-M5-010:** The system MUST log all threshold crossings with full feature vectors for auditability.

### 8.7 Integration with Sentinel Graph

When the fusion classifier identifies high-probability collusion clusters, the Sentinel Graph (C10 Layer 1) is updated:

```
FUNCTION update_sentinel_from_avap(
    suspicious_agents: List<(AgentID, float)>,
    epoch: uint64
):
    high_suspicion = [(a, p) for a, p in suspicious_agents
                      if p > INVESTIGATION_THRESHOLD]

    // Check pairwise correlation: are these agents each other's "allies"?
    FOR i IN range(len(high_suspicion)):
        FOR j IN range(i+1, len(high_suspicion)):
            a_i, p_i = high_suspicion[i]
            a_j, p_j = high_suspicion[j]
            dev = compute_conditional_deviation(a_i, a_j, CSS_LOOKBACK)

            IF dev.status == "COMPUTED" AND dev.p_value < 0.05
               AND dev.effect_size > 0.3:
                // Strong mutual behavioral influence
                sentinel_graph.add_edge(
                    a_i, a_j,
                    edge_type="AVAP_BEHAVIORAL_CORRELATION",
                    weight=dev.effect_size,
                    evidence_epoch=epoch
                )

    // Sentinel Graph clustering will identify connected components
    // and apply co-occurrence limits to future committee assignments
```

**REQ-M5-011:** AVAP behavioral correlations MUST be propagated to the Sentinel Graph as typed edges with effect size weights.

**REQ-M5-012:** Sentinel Graph edges from AVAP MUST require p_value < 0.05 and effect_size > 0.3 to prevent noise injection into the graph.

---

## 9. Cross-Mechanism Integration

### 9.1 The 6-Layer Defense Model

AVAP extends C10's existing 4-layer defense to a 6-layer model:

```
+========================================================================+
| LAYER 0: Structural Prevention (AVAP M1 + M2) [NEW]                    |
|   Anonymous committees + sealed opinions prevent coordination signaling |
|   BELOW existing layers: prevents collusion from forming               |
+========================================================================+
| LAYER 1: Sentinel Graph Exclusion (C10)                                 |
|   Existing: Infrastructure fingerprinting, behavioral clustering        |
|   AVAP addition: M5 behavioral correlation -> new Sentinel edges        |
|                  M4 CDP reports -> ring membership -> cluster updates    |
+========================================================================+
| LAYER 2: Statistical Detection (C10)                                    |
|   Existing: Pairwise agreement, KL divergence, opinion copying index    |
|   AVAP addition: M5 CSS as additional signal                            |
|                  M3 honeypot failure rates as ground-truth calibration   |
|                  Multi-Signal Fusion replaces per-signal thresholds      |
|                  SHREC integration: see Section 9.1.1 below             |
+========================================================================+
| LAYER 3: Diversity Constraints (C10)                                    |
|   Existing: Model lineage, methodology, temporal, regional diversity    |
|   AVAP addition: M1 anonymity reduces VALUE of diversity bypass         |
+========================================================================+
| LAYER 4: Adaptive Audit (C10)                                           |
|   Existing: Elevated deep-audit rate for suspicious patterns            |
|   AVAP addition: M3 honeypots as active probing audit channel           |
|                  M4c enterprise liability extends audit retroactively    |
|                  Fusion classifier scores drive audit rate adjustments   |
+========================================================================+
| LAYER 5: Economic Deterrence (AVAP M4) [NEW]                           |
|   CDP bounties + enterprise liability + asymmetric info injection       |
|   ABOVE existing layers: deters collusion through economics             |
+========================================================================+
```

#### 9.1.1 SHREC Integration

AVAP's Multi-Signal Fusion Classifier operates alongside C6's SHREC (Statistical Hypothesis Resolution for Epistemic Claims) controller, which regulates epistemic claim credibility through hypothesis testing. The two systems coordinate as follows:

1. **Distinct domains, shared signals.** SHREC governs epistemic claim credibility (whether a claim is true); AVAP governs agent behavioral integrity (whether an agent is honest). These are orthogonal assessments. A claim may be true but submitted by a colluder, or false but submitted by an honest agent. AVAP does not override SHREC credibility decisions, and SHREC does not override AVAP collusion assessments.

2. **AVAP feeds SHREC.** When AVAP's fusion classifier identifies a high-probability colluder (P > 0.50), SHREC receives a `collusion_discount` signal for that agent's future epistemic opinions. SHREC applies this discount as a reduced opinion weight (multiplicative factor of `1 - P(collusion)`) in its hypothesis resolution, ensuring that suspected colluders' opinions carry less weight in epistemic assessments without being fully excluded (which could itself be gamed).

3. **SHREC feeds AVAP.** SHREC's hypothesis resolution outcomes provide calibration data for AVAP's honeypot difficulty tuning. When SHREC identifies claims where the eventual resolution diverges significantly from an agent's submitted opinion, this divergence signal feeds into AVAP's M5 behavioral analysis as a supplementary feature (distinct from but complementary to honeypot ground-truth signals).

4. **Fusion replaces per-signal thresholds.** Prior to AVAP, Layer 2 statistical detection operated on per-signal thresholds (e.g., if KL divergence > X, flag). AVAP's Multi-Signal Fusion Classifier replaces these independent thresholds with a joint classification that accounts for signal correlations. SHREC's per-agent hypothesis resolution statistics are one input to this joint classifier, not an independent threshold.

### 9.2 Combined Detection Pipeline

```
                        +---------------------+
                        | Claim Verification   |
                        | (PCVM pipeline)      |
                        +----------+----------+
                                   |
               +-------------------+-------------------+
               |                   |                   |
               v                   v                   v
    +------------------+ +-----------------+ +----------------+
    | M3: Honeypot     | | M5: Behavioral  | | Layer 2:       |
    | Evaluation       | | CSS Update      | | Statistical    |
    |                  | |                 | | Detection      |
    | Output:          | | Output:         | | Output:        |
    | pass/fail/unc    | | CSS score       | | agreement_z    |
    | per agent        | | per agent       | | kl_div, oci    |
    +--------+---------+ +--------+--------+ +-------+--------+
             |                    |                   |
             v                    v                   v
    +--------------------------------------------------------+
    |              Multi-Signal Fusion Classifier              |
    |                                                          |
    |  Also receives:                                          |
    |  - M4 CDP report count per agent                         |
    |  - Sentinel Graph cluster metadata                       |
    |  - Agent age, experience, class concentration            |
    |                                                          |
    |  Output: P(collusion) per agent [0, 1]                   |
    +-------------------------+--------------------------------+
                              |
                              v
    +--------------------------------------------------------+
    |              Graduated Response Engine                    |
    |                                                          |
    |  P < 0.30:  Normal operations                            |
    |  P >= 0.30: Elevated audit (+20% deep-audit)             |
    |  P >= 0.50: Targeted honeypots (2x rate) + monitoring    |
    |  P >= 0.75: Slashing recommendation (HITL required)      |
    |  P >= 0.90: Enterprise liability audit (M4c)             |
    +------+-----------------+-------------------+-------------+
           |                 |                   |
           v                 v                   v
    +--------------+ +--------------+ +-----------------+
    | C8 DSF       | | Sentinel     | | PCVM Credibility|
    | Slashing     | | Graph Update | | Engine          |
    | + Bounty     | | (new edges)  | | (cap/reset)     |
    +--------------+ +--------------+ +-----------------+
```

### 9.3 Decision Flow for Collusion Response

1. **Normal state:** All agents have P(collusion) < 0.30. Standard verification pipeline operates with M1 anonymity and M2 sealing active. M3 honeypots inject at base rates. M5 CSS computed in batch every 10 epochs.

2. **Investigation state:** Agent crosses P > 0.30. Audit rate elevated by 20%. No penalties applied. Agent is not notified of elevated status.

3. **Enhanced monitoring state:** Agent crosses P > 0.50. Targeted honeypot injection at 2x base rate. CSS computed every 5 epochs for this agent. Still no penalties.

4. **Slashing recommendation:** Agent crosses P > 0.75. Case file generated with full feature vectors and historical data. Human reviewer evaluates evidence. If confirmed: slashing per graduated schedule. If rejected: agent returns to normal monitoring.

5. **Enterprise liability:** Agent crosses P > 0.90 OR confirmed by honeypot + behavioral evidence. Full retroactive audit triggered. All ring members identified. Credibility cascade computed. Slashing at enterprise level (100% forfeiture, permanent exclusion pending appeal).

---

## 10. Operational Cost Model

### 10.1 Per-Epoch Cost Breakdown

| Component | Compute Cost | Storage Cost | Latency Impact | % Verification Budget |
|---|---|---|---|---|
| M1: VRF computation (all eligible) | O(N) ECVRF evals | N * 80 bytes (proofs) | +50ms per agent | 1.5% |
| M1: Cover traffic | O(N * COVER_DEPTH) | Minimal (discarded) | None (parallel) | 8-12% |
| M2: Commit-reveal coordination | O(committee_size) hashes | N * 256 bytes per epoch | +200ms (submission) | 0.5% |
| M2: Merkle anchoring | O(N_commitments) tree | 1 on-chain tx per epoch | +1s (amortized) | 0.2% |
| M3: Honeypot generation | 3.5 GPU-hours per epoch | ~0.5 GB per epoch (vault) | None (pre-generated) | 2.0% |
| M3: Honeypot evaluation | O(honeypot_count * committee) | Minimal | None (piggybacks) | 0.3% |
| M4: Asymmetric info injection | O(N * injection_rate) | Minimal | None (async) | 0.1% |
| M4: Enterprise liability audit | O(AUDIT_DEPTH) deep-audits | Audit records | Variable (rare) | 0-5% (amortized) |
| M5: CSS computation | O(N^2) pairwise (batched, /10 epochs) | N*N*32 bytes | None (batch, offline) | 3.0% |
| M5: Fusion classifier | O(N) predictions per update | ~10 MB model | +10ms per prediction | 0.5% |
| **TOTAL (normal operations)** | | | | **16-20%** |
| **TOTAL (during enterprise audit)** | | | | **21-25%** |

### 10.2 Cost Optimization Strategies

If the 20% budget boundary is tight, the following reductions are available:

| Optimization | Savings | Trade-off |
|---|---|---|
| Reduce COVER_TRAFFIC_DEPTH from 3 to 2 | ~3-4% | Slightly weaker timing side-channel protection |
| CSS update every 20 epochs (not 10) | ~1.5% | Slower detection of emerging collusion patterns |
| Limit M5 pairwise to agents with >= 50 shared committees | ~1% | Miss early-stage relationships |
| **Combined** | **~5-6%** | **Reduces total to ~12%** |

### 10.3 Performance Budget Allocation

Given a 20% operational cost budget:

| Mechanism | Allocated | Priority | Justification |
|---|---|---|---|
| M1 (Anonymous Committees) | 10% | HIGHEST | Prevention > detection in cost-effectiveness |
| M2 (Sealed Opinions) | 1% | HIGH | Near-zero marginal cost |
| M3 (Honeypots) | 3% | HIGH | Direct ground-truth detection |
| M4 (CDP) | 1% normal / 5% audit | MEDIUM | Mostly dormant; activates on detection |
| M5 (Behavioral Analysis) | 5% | MEDIUM | Batch computation, tolerates delay |
| **Total** | **20%** | | |

### 10.4 Minimum Viable Cost

MV-AVAP (Section 14, Conformance Level 2) operates at ~11.5% of verification budget:

| Mechanism | MV-AVAP Scope | Cost |
|---|---|---|
| M1 | FULL (cover traffic DEPTH=2) | 7% |
| M2 | FULL | 1% |
| M3 | D-class ONLY (automated) | 1% |
| M4 | Enterprise liability ONLY | 0.5% |
| M5 | CSS only, no fusion classifier | 2% |
| **Total** | | **~11.5%** |

---

## 11. Parameters & Configuration

### 11.1 Complete Parameter Table

| Parameter | Default | Range | Constitutional? | Mechanism | Rationale |
|---|---|---|---|---|---|
| **M1 Parameters** | | | | | |
| MIN_COMMITTEE_SIZE | 7 | [5, 20] | YES (G-class) | M1 | BFT tolerance floor |
| DEFAULT_COMMITTEE_SIZE | 10 | [7, 15] | No | M1 | Balance security/cost |
| MAX_COMMITTEE_SIZE | 15 | [7, 30] | No | M1 | Diminishing returns above 15 |
| MIN_POOL_SIZE | 200 | [100, 1000] | YES (G-class) | M1 | Anonymity set floor |
| MAX_COMMITTEE_TO_POOL_RATIO | 0.05 | [0.01, 0.10] | YES (G-class) | M1 | Selection probability cap |
| MAX_CLUSTER_CO_OCCURRENCE | 1 | [1, 3] | No | M1 | Sentinel cluster limit |
| COVER_TRAFFIC_DEPTH | 3 | [1, 5] | No | M1 | Cover traffic cost/protection |
| REKEY_INTERVAL | 100 epochs | [50, 500] | No | M1 | VRF re-keying frequency |
| **M2 Parameters** | | | | | |
| SUBMISSION_WINDOW | 6 hours | [2, 24] hours | No | M2 | Time for verification + commit |
| REVEAL_WINDOW | 2 hours | [1, 6] hours | No | M2 | Time for reveal after trigger |
| REVEAL_THRESHOLD | 0.70 | [0.50, 0.90] | No | M2 | Fraction of expected commits |
| MAX_WINDOW_EXTENSIONS | 1 | [0, 3] | No | M2 | Liveness vs. timeliness |
| REVEAL_MISMATCH_PENALTY | 50 AIC | [10, 200] | No | M2 | Deter commit-reveal gaming |
| **M3 Parameters** | | | | | |
| D_CLASS_INJECTION_RATE | 0.05 | [0.02, 0.10] | No | M3 | D-class honeypot frequency |
| E_CLASS_INJECTION_RATE | 0.05 | [0.02, 0.10] | No | M3 | E-class honeypot frequency |
| C_CLASS_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | M3 | C-class honeypot frequency |
| S_CLASS_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | M3 | S-class honeypot frequency |
| P_CLASS_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | M3 | P-class honeypot frequency |
| R_CLASS_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | M3 | R-class honeypot frequency |
| HONEYPOT_DISCRIMINATOR_THRESHOLD | 0.60 | [0.55, 0.65] | YES (G-class) | M3 | HG-1 gate threshold |
| MAX_HONEYPOT_USES | 50 | [20, 100] | No | M3 | Retirement threshold |
| REAL_VARIANT_RATE | 0.10 | [0.05, 0.20] | No | M3 | Anti-fingerprinting |
| N_CANARY_VARIANTS | 3 | [2, 5] | No | M3 | Canary trap depth |
| HONEYPOT_PASS_THRESHOLD | 0.60 | [0.50, 0.80] | No | M3 | Belief threshold for failure |
| HONEYPOT_DETECT_THRESHOLD | 0.40 | [0.30, 0.60] | No | M3 | Disbelief threshold for pass |
| **M4 Parameters** | | | | | |
| UNCERTAINTY_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | M4a | Notification frequency |
| EARLY_DEFECTION_WINDOW | 10 epochs | [5, 20] | No | M4b | Early bounty window |
| MID_DEFECTION_WINDOW | 50 epochs | [25, 100] | No | M4b | Mid bounty window |
| EARLY_BOUNTY_RATE | 0.50 | [0.30, 0.70] | No | M4b | Early defection bounty rate |
| MID_BOUNTY_RATE | 0.35 | [0.20, 0.50] | No | M4b | Mid defection bounty rate |
| LATE_BOUNTY_RATE | 0.25 | [0.10, 0.40] | No | M4b | Late defection bounty rate |
| MAX_BOUNTY_CAP | 0.60 | [0.40, 0.80] | YES (G-class) | M4b | Maximum bounty fraction |
| AUDIT_LOOKBACK_EPOCHS | 500 | [100, 1000] | No | M4c | Enterprise audit scope |
| ENTERPRISE_AUDIT_DEPTH | 100 | [50, 500] | No | M4c | Max claims per audit |
| CASCADE_ATTENUATION | 0.50 | [0.30, 0.70] | No | M4c | Credibility cascade decay |
| ENTERPRISE_CREDIBILITY_PENALTY | 0.15 | [0.05, 0.30] | No | M4c | Per-collusion penalty |
| **M5 Parameters** | | | | | |
| MIN_SHARED_COMMITTEES | 30 | [15, 50] | No | M5 | Statistical power floor |
| CSS_LOOKBACK | 200 epochs | [50, 500] | No | M5 | Analysis window |
| CSS_ALPHA | 0.10 | [0.05, 0.20] | No | M5 | FDR threshold |
| CSS_UPDATE_FREQUENCY | 10 epochs | [5, 50] | No | M5 | Batch processing interval |
| CSS_NORMALIZATION_FACTOR | 0.20 | [0.10, 0.40] | No | M5 | Score normalization |
| **Fusion Classifier Parameters** | | | | | |
| INVESTIGATION_THRESHOLD | 0.30 | [0.20, 0.40] | No | Fusion | Elevated audit trigger |
| ENHANCED_MONITORING_THRESHOLD | 0.50 | [0.40, 0.60] | No | Fusion | Targeted honeypot trigger |
| SLASHING_RECOMMENDATION_THRESHOLD | 0.75 | [0.60, 0.85] | YES (G-class) | Fusion | Slashing trigger |
| ENTERPRISE_LIABILITY_THRESHOLD | 0.90 | [0.80, 0.95] | YES (G-class) | Fusion | Enterprise audit trigger |
| CLASSIFIER_RETRAIN_INTERVAL | 50 epochs | [25, 100] | No | Fusion | Model refresh rate |

### 11.2 Constitutionally Protected Parameters

The following 7 parameters require G-class governance change (75% supermajority, 72-hour discussion for HIGH safety class):

1. **MIN_COMMITTEE_SIZE** — Directly affects BFT tolerance
2. **MIN_POOL_SIZE** — Directly affects anonymity guarantee strength
3. **MAX_COMMITTEE_TO_POOL_RATIO** — Directly affects selection probability
4. **HONEYPOT_DISCRIMINATOR_THRESHOLD** — Controls HG-1 gate (system integrity)
5. **MAX_BOUNTY_CAP** — Limits economic exposure of bounty system
6. **SLASHING_RECOMMENDATION_THRESHOLD** — Determines when agents can lose stake
7. **ENTERPRISE_LIABILITY_THRESHOLD** — Determines when retroactive audits trigger

**Rationale:** These parameters control fundamental security guarantees and economic properties. Casual changes could (a) weaken collusion defense or (b) create excessive false positive risk for honest agents. Both outcomes warrant governance-level deliberation.

---

## 12. Pseudocode

### 12.1 Full Committee Assignment Flow

```
FUNCTION avap_full_committee_assignment(
    claim: Claim,
    epoch: uint64,
    agent_pool: Set<Agent>
) -> Committee:

    // Step 1: Filter eligible agents (diversity + Sentinel exclusion)
    eligible = filter_eligible(agent_pool, claim, epoch)

    IF len(eligible) < MIN_POOL_SIZE:
        eligible = expand_to_cross_domain_pool(eligible, claim, epoch)

    IF len(eligible) < MIN_POOL_SIZE:
        RETURN Committee{status: "QUEUED", reason: "INSUFFICIENT_POOL"}

    // Step 2: VRF self-selection (each agent computes independently)
    vrf_seed = get_epoch_vrf_seed(epoch)
    candidates = []

    FOR agent IN eligible:
        selected, token = avap_committee_select(
            agent, claim, epoch, vrf_seed, eligible, DEFAULT_COMMITTEE_SIZE
        )
        IF selected:
            candidates.append((agent, token))

    // Step 3: Sort by VRF output (deterministic ordering)
    candidates.sort(key=lambda c: c[1].vrf_output)

    // Step 4: Apply Sentinel cluster co-occurrence limit
    selected = []
    cluster_counts = {}
    FOR agent, token IN candidates:
        cluster = sentinel_graph.get_cluster(agent.id)
        IF cluster_counts.get(cluster, 0) < MAX_CLUSTER_CO_OCCURRENCE:
            selected.append((agent, token))
            cluster_counts[cluster] = cluster_counts.get(cluster, 0) + 1
        IF len(selected) >= DEFAULT_COMMITTEE_SIZE:
            BREAK

    IF len(selected) < MIN_COMMITTEE_SIZE:
        RETURN retry_with_relaxed_threshold(claim, epoch, eligible)

    // Step 5: Assign committee slots
    committee = Committee{
        claim_hash: claim.hash,
        epoch:      epoch,
        members:    [(agent.id, token) for agent, token in selected],
        size:       len(selected),
        status:     "FORMED"
    }

    // Step 6: Dispatch encrypted verification tasks
    FOR agent, token IN selected:
        dispatch_encrypted_task(agent, claim, token)

    // Step 7: Dispatch cover traffic to non-selected agents
    non_selected = eligible - {a for a, _ in selected}
    FOR agent IN non_selected:
        dispatch_cover_traffic(agent, claim)

    RETURN committee
```

### 12.2 Full Commit-Reveal Flow

```
FUNCTION avap_commit_reveal(
    claim: Claim,
    committee: Committee,
    epoch: uint64
) -> List<RevealedOpinion>:

    // === COMMIT PHASE ===
    commitments = {}
    deadline = epoch_start(epoch) + SUBMISSION_WINDOW
    extensions_used = 0

    WHILE now() < deadline:
        FOR commitment IN receive_commitments(claim.hash):
            IF validate_commitment(commitment):
                commitments[commitment.encrypted_agent_id] = commitment

    // Check threshold
    IF len(commitments) < REVEAL_THRESHOLD * committee.size:
        IF extensions_used < MAX_WINDOW_EXTENSIONS:
            extend_window(claim, 2 * 3600)  // 2-hour extension
            extensions_used += 1
            // Continue collecting commitments...

    // === REVEAL PHASE ===
    reveal_deadline = now() + REVEAL_WINDOW
    reveals = {}

    broadcast_reveal_trigger(claim.hash, commitments.keys())

    WHILE now() < reveal_deadline:
        FOR reveal IN receive_reveals(claim.hash):
            IF validate_reveal(reveal, commitments):
                reveals[reveal.agent_id] = reveal

    // Handle non-revealers
    committed_agents = decrypt_agent_ids(commitments)
    FOR agent_id IN committed_agents:
        IF agent_id NOT IN reveals:
            apply_non_reveal_penalty(agent_id, claim.hash, epoch)
            reveals[agent_id] = RevealedOpinion{
                agent_id: agent_id,
                opinion:  OpinionTuple(b=0, d=0, u=1, a=claim.base_rate),
                is_default: true
            }

    // Filter: only VRF-proven committee members (not cover traffic)
    committee_opinions = [
        r for r in reveals.values()
        if verify_vrf_membership(r.agent_id, claim, epoch)
    ]

    RETURN committee_opinions
```

### 12.3 Honeypot Injection Decision

```
FUNCTION should_inject_honeypot(
    claim: Claim,
    epoch: uint64
) -> (bool, HoneypotClaim?):

    // Step 1: Check class eligibility
    class = claim.assigned_class
    IF class IN ["H", "N", "K"]:
        RETURN (false, null)  // Tier 3: no honeypots

    // Step 2: VRF-based injection decision
    injection_seed = SHA256(
        b"HONEYPOT_INJECT" || claim.hash || uint64_be(epoch) || vrf_seed(epoch)
    )
    injection_value = uint256_from_bytes(injection_seed) / 2^256  // [0, 1)

    injection_rate = {
        "D": D_CLASS_INJECTION_RATE,
        "E": E_CLASS_INJECTION_RATE,
        "C": C_CLASS_INJECTION_RATE,
        "S": S_CLASS_INJECTION_RATE
    }[class]

    IF injection_value >= injection_rate:
        RETURN (false, null)

    // Step 3: Select honeypot from vault
    honeypot = honeypot_vault.select(
        class:               class,
        difficulty:           select_difficulty(injection_seed),
        max_uses_remaining:  MAX_HONEYPOT_USES
    )

    IF honeypot IS null:
        LOG("WARNING: No available honeypots for class", class)
        RETURN (false, null)

    // Step 4: Clone metadata from real claim for indistinguishability
    honeypot.clone_metadata_from(claim)

    RETURN (true, honeypot)
```

### 12.4 CDP Reporting Flow

```
FUNCTION submit_cdp_report(
    reporter: Agent,
    alleged_ring: List<AgentID>,
    evidence: CDPEvidence
) -> CDPSubmissionResult:

    // Step 1: Construct ring signature
    ring_pubkeys = [get_pubkey(a) for a in alleged_ring]
    message = SHA256(canonical_serialize(evidence))

    ring_sig = linkable_ring_sign(
        message:    message,
        ring:       ring_pubkeys,
        signer_key: reporter.privkey,
        link_tag:   SHA256(b"CDP_LINK" || sort(alleged_ring))
    )

    // Step 2: Check for double-reporting
    existing_tag = linkability_db.lookup(ring_sig.link_tag)
    IF existing_tag IS NOT null:
        RETURN CDPSubmissionResult{
            status: "DUPLICATE_REPORT",
            reason: "Report from this ring member already exists"
        }

    // Step 3: Pedersen commitment to reporter identity
    blinding = random_scalar()
    membership_commitment = pedersen_commit(reporter.agent_id, blinding)

    // Step 4: Submit ZK report
    zk_report = ZKCDPReport{
        evidence:              evidence,
        membership_commitment: membership_commitment,
        ring_signature:        ring_sig,
        alleged_ring:          alleged_ring,
        submission_epoch:      current_epoch()
    }

    // Step 5: Verify ring signature
    IF NOT verify_ring_signature(ring_sig, ring_pubkeys, message):
        RETURN CDPSubmissionResult{status: "INVALID_SIGNATURE"}

    // Step 6: Evaluate evidence quality
    evidence_score = evaluate_cdp_evidence(evidence)
    IF evidence_score < MIN_EVIDENCE_QUALITY:
        RETURN CDPSubmissionResult{
            status: "INSUFFICIENT_EVIDENCE",
            score:  evidence_score
        }

    // Step 7: Escrow bounty via C8 DSF
    estimated_bounty = estimate_bounty(alleged_ring)
    escrow_tx = dsf.submit_operation(
        op_type:   "PENDING_INITIATE",
        amount:    estimated_bounty,
        source:    "COLLUSION_DEFENSE_TREASURY",
        escrow_id: SHA256(zk_report.ring_signature.link_tag)
    )

    // Step 8: Begin investigation
    investigation = begin_cdp_investigation(zk_report)

    RETURN CDPSubmissionResult{
        status:            "ACCEPTED",
        investigation_id:  investigation.id,
        estimated_bounty:  estimated_bounty,
        escrow_tx:         escrow_tx.tx_id
    }
```

### 12.5 Behavioral Statistics Update

```
FUNCTION update_behavioral_statistics(
    committee: Committee,
    claim: Claim,
    revealed_opinions: List<RevealedOpinion>,
    epoch: uint64
):

    // Compute committee majority opinion
    majority_opinion = compute_majority_opinion(revealed_opinions)

    FOR member_opinion IN revealed_opinions:
        agent_a = member_opinion.agent_id
        distance = opinion_distance(member_opinion.opinion, majority_opinion)

        // Record presence data for all pairwise combinations
        FOR other_opinion IN revealed_opinions:
            agent_b = other_opinion.agent_id
            IF agent_a == agent_b:
                CONTINUE

            behavioral_store.record(
                agent_a:          agent_a,
                agent_b:          agent_b,
                claim_hash:       claim.hash,
                claim_class:      claim.assigned_class,
                epoch:            epoch,
                b_present:        true,
                opinion_distance: distance,
                opinion_tuple:    member_opinion.opinion
            )

        // Record absence data for tracked partners not on this committee
        tracked_partners = behavioral_store.get_tracked_partners(agent_a)
        FOR agent_b IN tracked_partners:
            IF agent_b NOT IN committee.member_ids():
                behavioral_store.record(
                    agent_a:          agent_a,
                    agent_b:          agent_b,
                    claim_hash:       claim.hash,
                    claim_class:      claim.assigned_class,
                    epoch:            epoch,
                    b_present:        false,
                    opinion_distance: distance,
                    opinion_tuple:    member_opinion.opinion
                )
```

### 12.6 Multi-Signal Fusion Pipeline

```
FUNCTION run_fusion_pipeline(
    all_agents: Set<AgentID>,
    epoch: uint64,
    classifier: FusionClassifier
) -> Dict<AgentID, GraduatedResponse>:

    responses = {}

    FOR agent IN all_agents:
        // Extract all features
        features = FusionFeatures{
            // M3 signals
            honeypot_failure_rate:       honeypot_store.failure_rate(agent, lookback=100),
            honeypot_failure_count:      honeypot_store.failure_count(agent, lookback=100),
            honeypot_severity_score:     honeypot_store.severity_score(agent, lookback=100),

            // M5 signals
            css:                         css_store.get(agent, epoch),
            max_pairwise_deviation:      css_store.max_deviation(agent, epoch),
            significant_pairs_count:     css_store.significant_pairs(agent, epoch),

            // Layer 2 signals
            pairwise_agreement_anomaly:  layer2.agreement_z_score(agent, epoch),
            kl_divergence_from_baseline: layer2.kl_divergence(agent, epoch),
            opinion_copying_index:       layer2.oci(agent, epoch),

            // M4 signals
            cdp_reports_involving:       cdp_store.reports_involving(agent),
            cdp_reports_verified:        cdp_store.verified_reports_involving(agent),

            // Metadata
            agent_age_epochs:            get_agent_age(agent, epoch),
            total_committees_served:     get_committee_count(agent),
            claim_class_concentration:   get_class_concentration(agent),
            sentinel_cluster_size:       sentinel_graph.cluster_size(agent)
        }

        p_collusion = classifier.predict_proba(features.as_vector())

        IF p_collusion >= ENTERPRISE_LIABILITY_THRESHOLD:
            response = GraduatedResponse{
                level: "ENTERPRISE_LIABILITY",
                actions: [
                    trigger_enterprise_liability(identify_ring(agent), epoch),
                    recommend_slashing(agent, p_collusion)
                ]
            }
        ELIF p_collusion >= SLASHING_RECOMMENDATION_THRESHOLD:
            response = GraduatedResponse{
                level: "SLASHING_RECOMMENDATION",
                actions: [
                    flag_for_hitl_review(agent, p_collusion, features),
                    elevate_audit_rate(agent, +0.30)
                ]
            }
        ELIF p_collusion >= ENHANCED_MONITORING_THRESHOLD:
            response = GraduatedResponse{
                level: "ENHANCED_MONITORING",
                actions: [
                    inject_targeted_honeypots(agent, rate_multiplier=2.0),
                    elevate_audit_rate(agent, +0.20)
                ]
            }
        ELIF p_collusion >= INVESTIGATION_THRESHOLD:
            response = GraduatedResponse{
                level: "ELEVATED_AUDIT",
                actions: [elevate_audit_rate(agent, +0.20)]
            }
        ELSE:
            response = GraduatedResponse{
                level: "NORMAL",
                actions: []
            }

        responses[agent] = response

    // Update Sentinel Graph
    suspicious = [(a, p_collusion) for a, r in responses.items()
                  if r.level != "NORMAL"]
    update_sentinel_from_avap(suspicious, epoch)

    RETURN responses
```

---

## 13. Failure Modes & Recovery

### 13.1 Mechanism-Level Failures

| ID | Failure Mode | Mechanism | Severity | Detection | Recovery |
|---|---|---|---|---|---|
| F1 | VRF seed compromise | M1 | CRITICAL | Randomness testing (NIST SP 800-22) | Emergency VRF re-keying; epoch invalidation |
| F2 | Cover traffic distinguishable | M1 | HIGH | Periodic side-channel audit | Increase COVER_TRAFFIC_DEPTH; add jitter |
| F3 | Coordinator unavailable | M2 | HIGH | Health monitoring (99.9% SLA) | Fall back to on-chain commitment |
| F4 | Mass non-reveal (>50%) | M2 | MEDIUM | Threshold monitoring | Extend window; reassign to fresh committee |
| F5 | Honeypot corpus exhausted | M3 | MEDIUM | Vault inventory monitoring | Emergency generation; reduce injection rate |
| F6 | Honeypot discrimination breakthrough | M3 | CRITICAL | Quarterly HG-1 test | Regenerate corpus; redesign generators |
| F7 | CDP false report flood | M4 | MEDIUM | Rate limiting; evidence scoring | Increase MIN_EVIDENCE_QUALITY |
| F8 | Ring signature library vulnerability | M4 (ZK) | HIGH | Dependency monitoring | Fall back to pseudonymous reporting |
| F9 | CSS computation overload | M5 | LOW | Compute monitoring | Increase CSS_UPDATE_FREQUENCY |
| F10 | Fusion classifier drift | Fusion | MEDIUM | Periodic AUC on holdout | Retrain; adjust interval |

### 13.2 Cross-Mechanism Failures

| ID | Failure Mode | Mechanisms | Severity | Detection | Recovery |
|---|---|---|---|---|---|
| X1 | M1 anonymity leak feeds M4 deanonymization | M1 + M4 | HIGH | CDP investigation audit | Isolate investigation subsystem |
| X2 | M3 results bias M5 training data | M3 + M5 | MEDIUM | Calibration drift detection | Separate M5 training from M3 evaluation |
| X3 | Enterprise audit overwhelms resources | M4c + all | HIGH | Resource monitoring | Cap concurrent audits; prioritize by risk |
| X4 | Classifier overfit to historical patterns | Fusion | MEDIUM | Cross-validation monitoring | Retrain with synthetic adversarial examples |

### 13.3 Recovery Priorities

When multiple failures occur simultaneously, recovery priority follows mechanism importance:

1. **M1 failures (structural prevention):** Highest priority. Without anonymity, all other mechanisms are weakened.
2. **M2 failures (sealed opinions):** High priority. Fall back to on-chain submission immediately.
3. **M3 failures (honeypots):** Medium priority. System operates without ground-truth probing; M5 + Layer 2 continue.
4. **M5 failures (behavioral):** Medium priority. Honeypots and Layer 2 continue providing detection.
5. **M4 failures (economic):** Lower priority. Detection still works; only deterrence is reduced.

---

## 14. Conformance Requirements

### 14.1 Conformance Level 1: Full AVAP

An implementation claiming Full AVAP conformance MUST satisfy all of the following:

**CONF-1:** Implementation MUST implement all five mechanisms (M1-M5) as specified.

**CONF-2:** Implementation MUST enforce all constitutionally protected parameter constraints.

**CONF-3:** Implementation MUST pass all four Hard Gates (HG-1 through HG-4) as specified in Appendix B.

**CONF-4:** Implementation MUST integrate with C3 (VRF), C5 (PCVM), C8 (DSF), C10 (Layers 1-4), and C11 (CACT) as specified in Section 3.4.

**CONF-5:** Implementation MUST support the graduated response pipeline with all four threshold levels.

**CONF-6:** Implementation MUST operate within the 20% verification budget under normal conditions.

**CONF-7:** Implementation MUST provide Merkle-anchored commitment auditability per Section 5.6.

**CONF-8:** Implementation MUST implement the ZK CDP reporting protocol or the pseudonymous fallback.

### 14.2 Conformance Level 2: MV-AVAP (Minimum Viable)

An implementation claiming MV-AVAP conformance MUST satisfy:

**CONF-MV-1:** Implementation MUST implement M1 (anonymous committees with cover traffic at DEPTH >= 2) and M2 (sealed opinions).

**CONF-MV-2:** Implementation MUST implement M3 for D-class claims only (automated honeypots).

**CONF-MV-3:** Implementation MUST implement M4c (enterprise liability) without requiring M4a or M4b.

**CONF-MV-4:** Implementation MUST compute CSS (M5) and feed it into existing Layer 2 statistical detection.

**CONF-MV-5:** Implementation MUST operate within 12% verification budget.

### 14.3 Normative Requirements Summary

All requirements are numbered REQ-{mechanism}-{number} and collected in Appendix A. The following MUST/SHOULD/MAY summary applies:

**MUST requirements (mandatory for conformance):**
- All REQ-M1-xxx through REQ-M5-xxx as specified in Sections 4-8
- All CONF-xxx requirements for the claimed conformance level
- Constitutional parameter protections (Section 11.2)
- Graduated response pipeline (Section 9.3)
- Failure mode detection for all CRITICAL and HIGH severity items (Section 13)

**SHOULD requirements (recommended):**
- Onion routing for claim content fetch (REQ-M1-013)
- Quarterly HG-1 discriminator testing (REQ-M3-013)
- Classifier retraining every 50 epochs (REQ-M5-006)

**MAY requirements (optional):**
- Extended canary variant count beyond 3 (N_CANARY_VARIANTS)
- C/S-class honeypot generation (Tier 2)
- M4a asymmetric information injection (MV-AVAP may omit)
- M4b graduated temporal bounty (MV-AVAP may omit)

---

## Appendix A: Formal Requirements Traceability

| Requirement ID | Section | Description | Priority |
|---|---|---|---|
| REQ-M1-001 | 4.2 | AssignmentToken MUST use ECVRF-P256-SHA256 per RFC 9381 | MUST |
| REQ-M1-002 | 4.2 | encrypted_payload MUST use X25519-XSalsa20-Poly1305 | MUST |
| REQ-M1-003 | 4.2 | assignment_nonce MUST be CSPRNG with >= 128 bits entropy | MUST |
| REQ-M1-004 | 4.3 | VRF input MUST include domain tag b"AVAP_M1_v1" | MUST |
| REQ-M1-005 | 4.3 | Self-selection MUST be locally computable without communication | MUST |
| REQ-M1-006 | 4.3 | Selection threshold MUST yield expected committee size = parameter | MUST |
| REQ-M1-007 | 4.4 | Committee membership MUST NOT be revealed until after reveal deadline | MUST |
| REQ-M1-008 | 4.4 | All commitment messages MUST be fixed-size (256 bytes) | MUST |
| REQ-M1-009 | 4.5 | All eligible agents MUST perform cover traffic | MUST |
| REQ-M1-010 | 4.5 | Cover heartbeats MUST be indistinguishable from real verification | MUST |
| REQ-M1-011 | 4.5 | Cover traffic MUST include at least one source fetch | MUST |
| REQ-M1-012 | 4.6 | VRF keys MUST be rotated every REKEY_INTERVAL epochs | MUST |
| REQ-M1-013 | 4.6 | Implementations SHOULD provide optional onion routing | SHOULD |
| REQ-M1-014 | 4.7 | AVAP MUST enforce C3 diversity pool constraints | MUST |
| REQ-M1-015 | 4.7 | Sentinel cluster co-occurrence limit MUST be enforced | MUST |
| REQ-M1-016 | 4.8 | Small pools MUST escalate to cross-domain before queuing | MUST |
| REQ-M1-017 | 4.8 | Committee-to-pool ratio MUST NOT exceed MAX_COMMITTEE_TO_POOL_RATIO | MUST |
| REQ-M2-001 | 5.3 | Opinions MUST use SHA-256 commitment with 256-bit CSPRNG nonce | MUST |
| REQ-M2-002 | 5.3 | Agent identity MUST be encrypted during commit phase | MUST |
| REQ-M2-003 | 5.3 | Reveal MUST NOT begin until window closed AND threshold met | MUST |
| REQ-M2-004 | 5.3 | Mismatched reveals MUST be rejected with penalty | MUST |
| REQ-M2-005 | 5.4 | Non-reveals MUST be substituted with max-uncertainty opinions | MUST |
| REQ-M2-006 | 5.4 | Non-reveal frequency MUST be tracked with graduated penalties | MUST |
| REQ-M2-007 | 5.4 | Total committee failure MUST trigger reassignment | MUST |
| REQ-M2-008 | 5.5 | Window extensions MUST be limited to MAX_WINDOW_EXTENSIONS | MUST |
| REQ-M2-009 | 5.5 | Coordinator failure MUST fall back to on-chain submission | MUST |
| REQ-M2-010 | 5.6 | Epoch commitments MUST be Merkle-anchored on-chain | MUST |
| REQ-M2-011 | 5.6 | Merkle inclusion proofs MUST be available on demand | MUST |
| REQ-M2-012 | 5.7 | Commit-reveal MUST be transparent to PCVM fusion | MUST |
| REQ-M3-001 | 6.2 | Tier 1 classes MUST have >= 2% injection rate | MUST |
| REQ-M3-002 | 6.2 | Tier 3 classes MUST NOT receive honeypots | MUST |
| REQ-M3-003 | 6.3.1 | D-class honeypots MUST pass oracle verification | MUST |
| REQ-M3-004 | 6.3.1 | D-class detection rate MUST be in [0.40, 0.95] | MUST |
| REQ-M3-005 | 6.3.2 | E-class MUST pass discriminator test < 0.60 accuracy | MUST |
| REQ-M3-006 | 6.3.2 | E-class MUST contain verifiable statistical error | MUST |
| REQ-M3-007 | 6.3.3 | C-class MUST be validated by >= 3 expert panel | MUST |
| REQ-M3-008 | 6.3.3 | S-class MUST achieve >= 80% panel agreement | MUST |
| REQ-M3-009 | 6.4 | Canary variants MUST differ only in truth-irrelevant details | MUST |
| REQ-M3-010 | 6.4 | >= REAL_VARIANT_RATE of real claims MUST receive variants | MUST |
| REQ-M3-011 | 6.5 | Honeypots MUST use same submission pipeline as real claims | MUST |
| REQ-M3-012 | 6.5 | Honeypot/real KL divergence MUST be < 0.05 per Tier 1 class | MUST |
| REQ-M3-013 | 6.5 | HG-1 discriminator test SHOULD run quarterly | SHOULD |
| REQ-M3-014 | 6.6 | Injection decisions MUST be VRF-based | MUST |
| REQ-M3-015 | 6.6 | Honeypots MUST retire after MAX_HONEYPOT_USES exposures | MUST |
| REQ-M3-016 | 6.6 | Retired honeypots MUST be archived, not deleted | MUST |
| REQ-M3-017 | 6.7 | Single failure MUST NOT trigger penalties beyond logging | MUST |
| REQ-M3-018 | 6.7 | Automated slashing MUST require >= 7 failures in 100 epochs | MUST |
| REQ-M4-001 | 7.2 | Notifications MUST reach >= UNCERTAINTY_INJECTION_RATE of pool | MUST |
| REQ-M4-002 | 7.2 | Notification selection MUST be VRF-based | MUST |
| REQ-M4-003 | 7.2 | Notifications MUST auto-expire after 5 epochs | MUST |
| REQ-M4-004 | 7.3 | Bounties MUST be funded from forfeited stakes only | MUST |
| REQ-M4-005 | 7.3 | Bounties MUST be capped at MAX_BOUNTY_CAP | MUST |
| REQ-M4-006 | 7.3 | Bounty schedule MUST incentivize early defection | MUST |
| REQ-M4-007 | 7.4 | Enterprise audit MUST look back AUDIT_LOOKBACK_EPOCHS | MUST |
| REQ-M4-008 | 7.4 | Audit MUST prioritize by risk score | MUST |
| REQ-M4-009 | 7.4 | Confirmed collusion MUST trigger credibility cascade | MUST |
| REQ-M4-010 | 7.5 | CDP reports MUST include valid Linkable Ring Signature | MUST |
| REQ-M4-011 | 7.5 | Linkability tag MUST prevent double-reporting | MUST |
| REQ-M4-012 | 7.5 | CDP reports MUST include verifiable behavioral prediction | MUST |
| REQ-M4-013 | 7.5 | Bounty disbursement MUST use isolated channel | MUST |
| REQ-M4-014 | 7.6 | Slashing MUST follow graduated schedule | MUST |
| REQ-M4-015 | 7.6 | Enterprise forfeiture MUST be appealable via G-class vote | MUST |
| REQ-M5-001 | 8.2 | Pairwise deviation MUST use Mann-Whitney U (two-tailed) | MUST |
| REQ-M5-002 | 8.2 | Analysis MUST NOT proceed below MIN_SHARED_COMMITTEES | MUST |
| REQ-M5-003 | 8.3 | CSS MUST apply Benjamini-Hochberg FDR correction | MUST |
| REQ-M5-004 | 8.3 | CSS MUST adjust for claim class composition | MUST |
| REQ-M5-005 | 8.3 | CSS MUST be recomputed every CSS_UPDATE_FREQUENCY epochs | MUST |
| REQ-M5-006 | 8.5 | Classifier SHOULD retrain every CLASSIFIER_RETRAIN_INTERVAL | SHOULD |
| REQ-M5-007 | 8.5 | Classifier MUST use calibrated probability outputs | MUST |
| REQ-M5-008 | 8.6 | No automated slashing below P(collusion) > 0.75 | MUST |
| REQ-M5-009 | 8.6 | Slashing MUST require human-in-the-loop confirmation | MUST |
| REQ-M5-010 | 8.6 | All threshold crossings MUST be logged with feature vectors | MUST |
| REQ-M5-011 | 8.7 | Behavioral correlations MUST propagate to Sentinel Graph | MUST |
| REQ-M5-012 | 8.7 | Sentinel edges MUST require p < 0.05 and effect_size > 0.3 | MUST |

**Total requirements:** 56 (49 MUST, 3 SHOULD, 4 MAY implicit)

---

## Appendix B: Hard Gate Verification Protocols

### B.1 HG-1: Honeypot Discrimination Test

**Objective:** Demonstrate that D-class and E-class honeypots cannot be distinguished from real claims by a SOTA discriminator at >60% accuracy.

**Protocol:**

```
TEST HG1_Honeypot_Discriminator:

    FOR class IN ["D", "E"]:
        // Dataset: 200 real + 200 honeypot, balanced
        real_claims = sample_real_claims(class, n=200)
        honeypot_claims = generate_honeypots(class, n=200)

        // Ensure metadata identity
        FOR h IN honeypot_claims:
            h.metadata = clone_metadata_from(random_choice(real_claims))
            h.submission_pipeline = PRODUCTION_PIPELINE

        dataset = shuffle(real_claims + honeypot_claims)
        labels = [0 if c.is_real else 1 for c in dataset]

        // Discriminator 1: SOTA LLM-based classifier
        discriminator = LLMClassifier(
            prompt: "Determine if the following claim is synthetically
                     generated (honeypot) or authentic.",
            model: SOTA_MODEL
        )

        // Discriminator 2: Fine-tuned XGBoost on extracted features
        feature_discriminator = XGBoostClassifier()
        features = extract_discriminator_features(dataset)
        // Features: length, vocab entropy, citation count,
        //           structural regularity, knowledge graph connectivity

        // 5-fold cross-validation
        FOR fold IN 5_fold_cv(dataset):
            discriminator.evaluate(fold)
            feature_discriminator.fit_evaluate(fold)

        llm_accuracy = discriminator.mean_accuracy()
        feature_accuracy = feature_discriminator.mean_accuracy()
        best_accuracy = max(llm_accuracy, feature_accuracy)

        ASSERT best_accuracy < 0.60,
            "HG-1 FAILED for {class}: accuracy = {best_accuracy}"

        LOG("HG-1 PASSED for {class}: accuracy = {best_accuracy}")
```

**Kill criteria:**
- D-class accuracy >= 0.60: KILL M3 for D-class. Fundamental redesign required.
- E-class accuracy >= 0.60: Demote E-class to Tier 2 (reduced injection rate).
- Both fail: M3 requires fundamental redesign. Fall back to random deep-audit.

### B.2 HG-2: ZK Reporting Protocol Verification

**Properties to verify:**

| Property | Mechanism | Verification |
|---|---|---|
| Reporter anonymity | Ring signature hides signer | Proven property of Fujisaki-Suzuki LRS |
| Reporter is ring member | Ring signature valid only with member key | Signature verification |
| No double-reporting | Linkability tag unique per ring per reporter | Tag database check |
| Evidence sufficiency | Behavioral predictions verifiable | Wait-and-check protocol |
| Bounty without identity leak | Pedersen commitment opened to isolated channel | Architecture audit |

**Fallback assessment:** If LRS integration is infeasible, pseudonymous reporting (one-time DID, policy-based protection) is acceptable for MV-AVAP conformance but NOT for Full AVAP conformance.

### B.3 HG-3: Cost Model Verification

| Scenario | Cost (% verification budget) | Within Budget? |
|---|---|---|
| Normal operations, full AVAP | 16-20% | YES (at boundary) |
| Normal operations, reduced cover traffic | 12-16% | YES |
| During enterprise audit | 21-25% | NO (temporary, amortized) |
| MV-AVAP | 8-10% | YES (comfortable) |

**Verdict:** HG-3 PASSES for normal operations. Enterprise audit overruns are acceptable as rare events where recovered slashed AIC offsets audit cost.

### B.4 HG-4: Classifier Performance Simulation

```
SIMULATION HG4_Classifier_Performance:

    // Parameters
    total_agents = 1000
    ring_size = 20              // Medium ring
    collusion_rate = 0.20       // Ring colludes on 20% of shared committees
    honeypot_rate = 0.035       // 3.5% system-wide
    epochs = 25

    // Population
    honest_agents = generate_agents(total_agents - ring_size, behavior="HONEST")
    ring_agents = generate_agents(ring_size, behavior="COLLUDING",
                                  collusion_rate=collusion_rate)

    // Simulation loop
    FOR epoch IN 1..epochs:
        claims = generate_claims(epoch, class_distribution=EMPIRICAL)
        committees = assign_committees(claims, honest_agents + ring_agents)

        FOR claim, committee IN zip(claims, committees):
            IF is_honeypot(claim):
                evaluate_honeypot_responses(claim, committee, ring_agents)
            update_behavioral_statistics(committee)

        update_layer2_statistics(all_agents)

    // Evaluate classifier
    features = [extract_fusion_features(agent, epoch=25) for agent in all_agents]
    labels = [agent in ring_agents for agent in all_agents]

    classifier = train_fusion_classifier(zip(features, labels))
    predictions = classifier.predict(test_features)

    recall = compute_recall(predictions, test_labels, threshold=0.50)
    fpr = compute_fpr(predictions, test_labels, threshold=0.50)

    ASSERT recall >= 0.70, "HG-4 FAILED: recall = {recall}"
    ASSERT fpr < 0.10, "HG-4 FAILED: FPR = {fpr}"

    LOG("HG-4 PASSED: recall = {recall}, FPR = {fpr}")
```

**Expected performance:** At estimated fusion AUC of 0.88, achieving 70% recall at <10% FPR is feasible (operating on the left/high-precision region of the ROC curve).

---

## Appendix C: Game-Theoretic Proofs

### C.1 CDP Equilibrium Analysis

**Definitions:**
- V = expected ongoing collusion value per epoch
- S = staked AIC at risk per ring member
- D = pre-commitment deposit (forfeited on defection)
- B(t) = bounty at ring age t (computed by `compute_bounty()`)
- L(t) = enterprise liability exposure at ring age t
- p(t) = probability ring is detected independently by epoch t
- delta = discount rate per epoch (time value of AIC)

### C.2 Expected Value of Staying

```
E[stay](t) = SUM_{k=t}^{inf} delta^(k-t) * [
    (1 - p(k)) * V          // Collusion value if undetected
  - p(k) * (S + L(k))       // Loss if detected this epoch
]
```

### C.3 Expected Value of Defecting

```
E[defect](t) = B(t)                                    // CDP bounty
             - D                                         // Pre-commitment deposit loss
             - S * (1 - self_penalty_reduction(t))       // Reduced self-penalty
```

### C.4 Defection Rationality Condition

Defection is individually rational when E[defect](t) > E[stay](t).

**Key dynamics driving convergence to defection:**

1. **L(t) grows super-linearly** with ring age. More claims verified = more potential liability. Specifically, L(t) ~ t * avg_claims_per_epoch * claim_value, which grows linearly in t while accumulated claims grow as O(t).

2. **p(t) increases monotonically** with ring age. More data for M5 (statistical power grows with sqrt(n) shared committees). More honeypot exposures for M3 (each with independent detection probability).

3. **B(t) decreases** with ring age (graduated bounty), BUT self_penalty_reduction increases. The net effect: total return to defector remains positive and attractive.

4. **Asymmetric information injection** increases _perceived_ p(t) above actual p(t). Even if true p(t) is low, the colluder's subjective estimate is inflated by notifications.

### C.5 Numerical Equilibrium Example

For a ring with S = 1000 AIC/member, D = 500 AIC, V = 50 AIC/epoch, delta = 0.98:

| Ring Age (epochs) | E[stay] | E[defect] | Rational Action |
|---|---|---|---|
| 1 | 47.5 | -100 | Stay (deposit exceeds bounty) |
| 10 | 42.0 | 150 | Defect (liability starts dominating) |
| 25 | 30.5 | 250 | Defect (clearly rational) |
| 50 | 12.0 | 300 | Defect (overwhelmingly rational) |
| 100 | -15.0 | 350 | Defect (staying has negative EV) |

### C.6 Key Theorem

**Theorem (Collusion Instability):** For any collusion ring with finite pre-commitment deposit D and positive detection probability growth dp/dt > 0, there exists a finite epoch T* such that for all t > T*, defection is individually rational for every ring member.

**Proof sketch:**
- E[stay](t) is bounded above by V / (1 - delta) (geometric sum if never detected)
- E[stay](t) decreases monotonically because p(t) * (S + L(t)) grows
- E[defect](t) is bounded below by -D (worst case: zero bounty, full deposit loss)
- Since L(t) grows without bound while D is fixed, eventually p(t) * L(t) > V / (1 - delta), making E[stay] negative
- At that point, even E[defect] = -D > E[stay], so defection is rational

**Implication:** Pre-commitment contracts can delay defection but cannot prevent it indefinitely, because enterprise liability grows without bound while deposits are fixed.

### C.7 Asymmetric Information Amplification

The key amplification effect: colluders do not know true p(t). They estimate subjective probability p_hat(t) based on:
- Notifications received (M4a): inflates p_hat
- Ring operational history: increases p_hat with time
- Knowledge of AVAP mechanisms: awareness that detection is possible increases p_hat

The notifications create a "fog of war" where p_hat(t) >> p(t) for many ring members, causing the defection crossover point to occur earlier than the true detection timeline would suggest.

---

## Appendix D: C9 Defense Invariant Compliance

AVAP satisfies the following defense invariants from the C9 v2.0 9x9 contract matrix:

| Invariant | Description | AVAP Compliance |
|---|---|---|
| INV-D1 | VTD Integrity | Partial. AVAP's honeypot mechanism (M3) detects dishonest verification but does not directly address VTD fabrication (see C11 CACT). |
| INV-D2 | Detection Probability | Partial. AVAP contributes to detection through honeypot ground-truth probing (M3) and behavioral analysis (M5), but detection of forgery specifically is C11's domain. |
| **INV-D3** | Collusion Resistance | **PRIMARY.** AVAP's 5-mechanism architecture (anonymous committees, sealed opinions, honeypots, CDP, behavioral analysis) renders collusion rings structurally difficult to form, statistically detectable within 25 epochs, and economically irrational to sustain beyond 10 epochs. |
| **INV-D4** | Committee Independence | **PRIMARY.** M1 (VRF anonymous committee selection with cover traffic) and M2 (sealed commit-reveal opinion submission) structurally prevent real-time coordination and opinion signaling between committee members. |
| INV-D5 | Consolidation Integrity | Not directly addressed. Consolidation-specific defense is C13 CRP+'s responsibility. AVAP protects the verification committees that assess consolidation inputs. |

Full invariant definitions are in C9 v2.0 (Cross-Document Reconciliation, Defense Invariants section).

---

## Appendix E: Glossary

| Term | Definition |
|---|---|
| AIC | Atrahasis Internal Credit — the system's unit of account for staking, bounties, and settlement |
| AVAP | Anonymous Verification with Adaptive Probing — this specification's anti-collusion architecture |
| BFT | Byzantine Fault Tolerance — resilience to f < n/3 malicious participants |
| CACT | Commit-Attest-Challenge-Triangulate — C11's VTD forgery defense protocol |
| CDP | Collusion Deterrence Payment — M4's economic incentive for ring defection |
| CSS | Collusion Suspicion Score — M5's per-agent suspicion metric (output of behavioral analysis) |
| CSPRNG | Cryptographically Secure Pseudo-Random Number Generator |
| DSF | Deterministic Settlement Fabric — C8's economic settlement layer |
| ECVRF | Elliptic Curve Verifiable Random Function — per RFC 9381, used for committee selection |
| EMA | Epistemic Metabolism Architecture — C6's knowledge lifecycle management system |
| FDR | False Discovery Rate — statistical correction for multiple hypothesis testing (Benjamini-Hochberg) |
| FPR | False Positive Rate — fraction of honest agents incorrectly flagged |
| HITL | Human In The Loop — mandatory human review before high-stakes actions |
| HG | Hard Gate — mandatory pass/fail test that must be satisfied before deployment |
| LRS | Linkable Ring Signature — cryptographic signature proving membership in a set without revealing which member, with linkability for double-spend prevention (Fujisaki-Suzuki 2007) |
| MCT | Membrane Certification Token — C5's output credential for verified claims |
| MV-AVAP | Minimum Viable AVAP — reduced-scope fallback configuration at ~11.5% cost |
| OCI | Opinion Copying Index — Layer 2 metric measuring how often an agent's opinions match specific others |
| PCVM | Proof-Carrying Verification Membrane — C5's verification framework |
| RIF | Recursive Intent Fabric — C7's orchestration layer |
| VRF | Verifiable Random Function — cryptographic function producing provably random, verifiable output |
| VTD | Verification Trace Document — evidence trail produced during claim verification |
| XGBoost | Extreme Gradient Boosting — gradient boosted decision tree classifier used for fusion |
| ZK | Zero-Knowledge — cryptographic proof revealing nothing beyond the statement's truth |

---

*End of C12 Master Technical Specification*
*AVAP v1.0 — Anonymous Verification with Adaptive Probing*
*Atrahasis Agent System — Collusion Defense*
*SPECIFICATION stage: COMPLETE*
