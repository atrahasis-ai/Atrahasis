# C12 DESIGN: AVAP (Anonymous Verification with Adaptive Probing)

**Invention:** C12 -- Collusion Defense
**Stage:** DESIGN
**Version:** v1.0
**Date:** 2026-03-10
**Concept:** C12-B (AVAP) -- 5-mechanism anti-collusion architecture
**Feasibility Scores:** Novelty 3.5/5, Feasibility 3.5/5, Impact 4/5, Risk 5/10
**Status:** DESIGN COMPLETE
**Normative References:** C3 (Tidal Noosphere v1.0), C5 (PCVM v1.0), C6 (EMA v1.0), C8 (DSF v2.0), C10 (Hardening Addenda), C11 (CACT v1.0), RFC 9381 (ECVRF), RFC 8032 (Ed25519), Pedersen Commitments, Groth16

---

## TABLE OF CONTENTS

1. [System Architecture Overview](#1-system-architecture-overview)
2. [M1: Anonymous Committees -- Detailed Design](#2-m1-anonymous-committees)
3. [M2: Sealed Opinion Submission -- Detailed Design](#3-m2-sealed-opinion-submission)
4. [M3: Honeypot Claims -- Detailed Design](#4-m3-honeypot-claims)
5. [M4: Collusion Deterrence Payment -- Detailed Design](#5-m4-collusion-deterrence-payment)
6. [M5: Conditional Behavioral Analysis -- Detailed Design](#6-m5-conditional-behavioral-analysis)
7. [Cross-Mechanism Integration](#7-cross-mechanism-integration)
8. [Hard Gate Verification](#8-hard-gate-verification)
9. [Parameters and Configuration](#9-parameters-and-configuration)
10. [Pseudocode for Critical Algorithms](#10-pseudocode-for-critical-algorithms)
11. [Failure Mode Catalogue](#11-failure-mode-catalogue)
12. [Minimum Viable AVAP (MV-AVAP)](#12-minimum-viable-avap)

---

## 1. SYSTEM ARCHITECTURE OVERVIEW

### 1.1 Position in the Atrahasis Stack

AVAP is a cross-cutting anti-collusion system that wraps around the verification pipeline. It does not replace any existing component; it instruments the pipeline with prevention, detection, and deterrence mechanisms.

```
+=========================================================================+
|  C7: RIF -- Recursive Intent Fabric (Orchestration)                      |
+=========================================================================+
          |
          v
+=========================================================================+
|  C8: DSF -- Deterministic Settlement Fabric (Economics)                  |
|    AIC staking, slashing, enterprise liability settlement                |
|    AVAP INTERFACE: M4 slashing events, bounty escrow, CDP settlements   |
+=========================================================================+
          |                    |                    |
          v                    v                    v
+=========================================================================+
|  AVAP LAYER (THIS DOCUMENT)                                              |
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
|  C4: ASV -- Agent Semantic Vocabulary (Communication)                    |
+=========================================================================+
```

### 1.2 Data Flow: Claim Submission Through Detection

The complete lifecycle of a claim under AVAP protection:

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
  If P(collusion) > INVESTIGATION_THRESHOLD: trigger elevated audit
  If P(collusion) > SLASHING_THRESHOLD: recommend slashing via C8 DSF
  If ring detected: enterprise liability retroactive audit (M4c)
                |
                v
PHASE 9: COMMITTEE REVEAL
  After all opinions processed, committee membership is revealed
  VRF proofs published for auditability
  Anonymity window closes
```

### 1.3 Mechanism Classification

| Mechanism | Type | Timing | Coverage | Strength |
|---|---|---|---|---|
| M1: Anonymous Committees | Prevention (structural) | Pre-verification | All claim classes | Prevents targeted coordination |
| M2: Sealed Opinions | Prevention (structural) | During verification | All claim classes | Prevents signaling/copying |
| M3: Honeypot Claims | Detection (active probing) | During verification | D/E full, C/S partial, H/N excluded | Catches rubber-stamping |
| M4: CDP | Deterrence (economic) | Post-detection | All claim classes | Destabilizes collusion rings |
| M5: Behavioral Analysis | Detection (passive monitoring) | Continuous | All claim classes (strongest on S/H/C) | Screens for conditional behavior |

### 1.4 Interface Summary

| Interface | AVAP Component | Direction | Protocol |
|---|---|---|---|
| C3 Tidal Noosphere | M1 | Bidirectional | VRF seed consumption, committee formation |
| C3 Sentinel Graph | M5, Response Engine | Outbound | Cluster updates from collusion detection |
| C5 PCVM | M2, M3 | Bidirectional | Opinion submission/fusion, claim injection |
| C8 DSF | M4, Response Engine | Outbound | Slashing events, bounty escrow, enterprise liability settlement |
| C10 Existing Layers | M5, Fusion Classifier | Bidirectional | Layer 1-4 signals as classifier inputs |
| C11 CACT | M3 | Inbound | Commitment chain data for honeypot design |

---

## 2. M1: ANONYMOUS COMMITTEES

### 2.1 Design Overview

Anonymous committees prevent colluders from identifying allies on a verification committee, eliminating the ability to selectively coordinate votes. The mechanism extends C3's existing VRF-based committee selection with encrypted assignment tokens and mandatory cover traffic.

**Core invariant (INV-M1):** No agent learns the identity of any other committee member until after all sealed opinions have been submitted and the reveal phase is complete.

### 2.2 VRF Assignment Token Format

Each agent performs VRF self-selection independently. The output is an encrypted assignment token that only the selected agent can interpret.

```
STRUCTURE AssignmentToken:
    claim_id:           bytes32         // Hash of the claim being verified
    epoch:              uint64          // Epoch number
    agent_id:           AgentID         // Selected agent
    vrf_output:         bytes32         // VRF output (beta)
    vrf_proof:          bytes80         // VRF proof (pi), ECVRF per RFC 9381
    selection_rank:     uint8           // Agent's rank in committee (by VRF output)
    committee_slot:     uint8           // Assigned slot (0..committee_size-1)
    assignment_nonce:   bytes16         // Random nonce for this assignment
    token_hash:         bytes32         // H(claim_id || epoch || agent_id || vrf_output || assignment_nonce)
    encrypted_payload:  bytes           // Enc(agent_pubkey, verification_instructions)
```

**Encryption scheme:** The `encrypted_payload` contains the claim content and verification instructions, encrypted with the agent's public key (X25519-XSalsa20-Poly1305). This ensures that even if assignment tokens are intercepted, only the intended agent can decrypt the verification task.

### 2.3 Self-Selection Protocol

```
FUNCTION avap_committee_select(
    agent: Agent,
    claim: Claim,
    epoch: uint64,
    vrf_seed: bytes32,
    eligible_pool: Set<Agent>,
    committee_size: uint8
) -> (bool, AssignmentToken?):

    // Step 1: Compute VRF output
    alpha = SHA256(claim.hash || uint64_be(epoch) || vrf_seed || b"AVAP_M1_v1")
    (beta, pi) = ECVRF_prove(agent.privkey, alpha)

    // Step 2: Self-selection threshold
    // Probability of selection = committee_size / |eligible_pool|
    threshold = (committee_size * 2^256) / |eligible_pool|
    vrf_value = uint256_from_bytes(beta)

    IF vrf_value >= threshold:
        RETURN (false, null)  // Not selected

    // Step 3: Compute selection rank (for deterministic slot assignment)
    // All selected agents can independently compute the same ranking
    rank = vrf_value  // Lower VRF output = higher rank

    // Step 4: Construct assignment token (local only, not broadcast)
    token = AssignmentToken{
        claim_id:       claim.hash,
        epoch:          epoch,
        agent_id:       agent.id,
        vrf_output:     beta,
        vrf_proof:      pi,
        selection_rank: rank,
        committee_slot: DEFERRED,  // Computed after all agents self-select
        assignment_nonce: random_bytes(16),
        token_hash:     SHA256(claim.hash || epoch || agent.id || beta || nonce),
        encrypted_payload: null    // Populated when claim content is fetched
    }

    RETURN (true, token)
```

### 2.4 Anonymity Maintenance Timeline

```
TIME 0:          Epoch begins. VRF seed for this epoch is published.
TIME 0+delta:    Each agent evaluates VRF for each pending claim.
                 Selected agents learn they are on the committee.
                 NON-selected agents DO NOT learn who IS selected.

TIME 0 to T_w:   VERIFICATION WINDOW (default: 6 hours)
                 Selected agents verify the claim and form opinions.
                 All agents (selected and non-selected) perform cover traffic:
                   - Fetch claim content (mandatory for all agents in pool)
                   - Process claim to depth proportional to cover_traffic_depth
                   - Submit cover-traffic heartbeats (indistinguishable from
                     real verification activity)

TIME T_w:        COMMITMENT DEADLINE
                 Selected agents submit H(opinion || nonce) to coordinator.
                 Cover-traffic agents submit H(null_opinion || nonce).
                 All submissions are structurally identical (same size, same format).

TIME T_w+delta:  REVEAL PHASE (begins when threshold commitments received)
                 Selected agents reveal (opinion, nonce).
                 Cover-traffic agents reveal (null_opinion, nonce).
                 Coordinator filters: only opinions from VRF-proven members count.

TIME T_r:        REVEAL DEADLINE (default: T_w + 2 hours)
                 All revealed. Committee membership NOW becomes public.
                 VRF proofs published for auditability.
```

### 2.5 Cover Traffic Specification

Cover traffic masks which agents are on the committee by ensuring all agents in the eligible pool exhibit similar network and computational behavior.

```
FUNCTION generate_cover_traffic(
    agent: Agent,
    claim: Claim,
    is_committee_member: bool
) -> CoverTrafficRecord:

    // All agents fetch the claim content
    claim_content = fetch_claim_for_verification(claim.hash)

    // All agents perform partial verification (to depth COVER_DEPTH)
    partial_result = partial_verify(
        claim_content,
        depth = COVER_TRAFFIC_DEPTH,  // default: 3 (of ~10 verification steps)
        include_source_fetch = true    // Fetch at least 1 source
    )

    // Generate heartbeat (identical format for committee and cover agents)
    heartbeat = VerificationHeartbeat{
        agent_id:    agent.id,
        claim_hash:  claim.hash,
        epoch:       current_epoch(),
        timestamp:   now(),
        activity_hash: SHA256(partial_result.trace),
        // NOTE: heartbeat does NOT indicate committee membership
    }

    submit_heartbeat(heartbeat)

    IF is_committee_member:
        // Continue with full verification (additional steps beyond cover depth)
        full_result = complete_verification(claim_content, partial_result)
        RETURN CoverTrafficRecord{
            type: "FULL_VERIFICATION",
            heartbeat: heartbeat,
            result: full_result
        }
    ELSE:
        // Discard partial result after heartbeat
        RETURN CoverTrafficRecord{
            type: "COVER_ONLY",
            heartbeat: heartbeat,
            result: null
        }
```

**Cost of cover traffic:**

| Parameter | Value | Rationale |
|---|---|---|
| COVER_TRAFFIC_DEPTH | 3 steps (of ~10) | ~30% of full verification cost |
| Cover traffic fraction | 100% of eligible pool | All agents participate |
| Net overhead per non-committee agent | ~15-20% of full verification cost | Includes claim fetch + partial verify + heartbeat |
| Net overhead on system verification budget | ~8-12% | Pool is ~20x committee size; 20x agents * 15% * 1/20 = ~15% of one full verify |

### 2.6 Side-Channel Analysis

| Side Channel | Attack Vector | Mitigation | Residual Risk |
|---|---|---|---|
| Timing | Committee agents take longer (full verify vs. cover) | Cover traffic depth + jittered submission within window | LOW: 6-hour window hides timing differences |
| Bandwidth | Committee agents fetch more data (full sources) | Cover agents also fetch sources (COVER_TRAFFIC_DEPTH includes source fetch) | LOW |
| Submission size | Commitment messages differ in size | All commitments are fixed-size (256 bytes, padded) | NEGLIGIBLE |
| Long-term statistical | Over many epochs, committee membership frequency is observable | VRF re-keying every REKEY_INTERVAL epochs (default: 100) | LOW-MEDIUM |
| IP/infrastructure | Network-level observation of which agents connect to which claim sources | TOR-like onion routing for claim content fetch (OPTIONAL, high-security mode) | MEDIUM (without onion routing) |
| Electromagnetic/power | Physical side channels on hardware | Out of scope (physical security is operator responsibility) | N/A |

### 2.7 Integration with C3 VRF

AVAP's M1 extends C3's VRF Dual Defense Protocol (C3 Technical Spec Section 5) with the following modifications:

1. **VRF input domain separation:** AVAP committees use a distinct domain tag (`b"AVAP_M1_v1"`) appended to the VRF input, ensuring AVAP committee selections are independent of C3's task-scheduling VRF selections.

2. **Diversity pool integration:** AVAP inherits C3's Pre-Stratified Diversity Pools (C3 Section 5.3). Committee selection draws from pools that satisfy diversity constraints (model lineage, methodology, temporal bucket, region). This is the existing C10 Layer 3 mechanism applied to AVAP committees.

3. **Sentinel Graph exclusion:** Agents flagged by the Sentinel Graph (C10 Layer 1) as belonging to the same identity cluster are subject to committee co-occurrence limits: at most `MAX_CLUSTER_CO_OCCURRENCE` (default: 1) agents from the same cluster on any committee.

4. **VRF seed schedule:** AVAP uses the same epoch-level VRF seeds as C3 (derived from the Noosphere's entropy source). No additional randomness infrastructure is required.

### 2.8 Committee Size and Pool Ratio

| Parameter | Default | Constitutional? | Rationale |
|---|---|---|---|
| MIN_COMMITTEE_SIZE | 7 | YES (G-class) | Below 7, f >= 1/3 tolerance is too fragile |
| MAX_COMMITTEE_SIZE | 15 | No | Diminishing returns above 15; cost increases linearly |
| DEFAULT_COMMITTEE_SIZE | 10 | No | Balances security (BFT tolerance) and cost |
| MIN_POOL_SIZE | 200 | YES (G-class) | Below 200, anonymity set is too small for statistical protection |
| MAX_COMMITTEE_TO_POOL_RATIO | 0.05 | YES (G-class) | Any agent has <5% chance of being on any given committee |
| MAX_CLUSTER_CO_OCCURRENCE | 1 | No | At most 1 agent from each Sentinel cluster per committee |

**Fallback for small pools:** If the eligible pool for a claim's domain has fewer than MIN_POOL_SIZE agents, the claim is escalated to a cross-domain pool (increasing pool size but reducing domain expertise). If still insufficient, the claim enters a holding queue until pool size recovers.

---

## 3. M2: SEALED OPINION SUBMISSION

### 3.1 Commit-Reveal Protocol

The sealed opinion submission uses a standard two-phase commit-reveal protocol adapted for Subjective Logic opinion tuples.

```
STRUCTURE SealedOpinion:
    claim_hash:         bytes32
    epoch:              uint64
    agent_id:           AgentID         // Encrypted; revealed only after reveal phase
    opinion:            OpinionTuple    // (b, d, u, a) -- Subjective Logic opinion
    confidence_metadata: ConfidenceMeta  // Optional: reasoning hash, probe results
    nonce:              bytes32         // Cryptographic nonce for commitment
    commitment:         bytes32         // H(opinion || confidence_metadata || nonce)
    signature:          bytes64         // Ed25519 signature over commitment

STRUCTURE OpinionTuple:
    belief:             float64         // [0, 1]
    disbelief:          float64         // [0, 1]
    uncertainty:        float64         // [0, 1]
    base_rate:          float64         // [0, 1], prior for the claim class
    // Constraint: belief + disbelief + uncertainty = 1.0
```

### 3.2 Protocol Phases

**Phase 1: COMMIT**

```
FUNCTION submit_commitment(
    agent: Agent,
    claim: Claim,
    opinion: OpinionTuple,
    metadata: ConfidenceMeta
) -> Commitment:

    // Validate opinion tuple
    ASSERT abs(opinion.belief + opinion.disbelief + opinion.uncertainty - 1.0) < 1e-9

    // Generate cryptographic nonce
    nonce = random_bytes(32)

    // Compute commitment hash
    payload = canonical_serialize(opinion) || canonical_serialize(metadata) || nonce
    commitment_hash = SHA256(payload)

    // Sign the commitment
    signature = Ed25519_sign(agent.privkey, commitment_hash)

    // Submit to coordination service
    // NOTE: agent_id is encrypted under coordinator's public key
    //        so coordinator cannot correlate agent to commitment during commit phase
    encrypted_agent_id = encrypt_asymmetric(
        coordinator_pubkey,
        agent.id || claim.hash || epoch
    )

    commitment = Commitment{
        claim_hash:  claim.hash,
        epoch:       current_epoch(),
        encrypted_agent_id: encrypted_agent_id,
        commitment_hash: commitment_hash,
        signature:   signature,
        submitted_at: now()
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

    // Condition 1: Enough commitments received
    // (includes both committee members and cover-traffic agents)
    threshold_met = len(commitments) >= REVEAL_THRESHOLD
    // REVEAL_THRESHOLD = 0.7 * expected_committee_size (default: 7 of 10)

    // Condition 2: Submission window closed
    window_closed = now() > epoch_start + SUBMISSION_WINDOW
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

    // Recompute commitment
    payload = canonical_serialize(opinion) || canonical_serialize(metadata) || nonce
    expected_hash = SHA256(payload)

    IF expected_hash != original_commitment.commitment_hash:
        RETURN RevealResult{status: "COMMITMENT_MISMATCH", penalty: REVEAL_MISMATCH_PENALTY}

    // Agent identity now revealed for this claim
    // VRF proof is also submitted to prove committee membership
    reveal = Reveal{
        claim_hash:     claim.hash,
        epoch:          current_epoch(),
        agent_id:       agent.id,
        opinion:        opinion,
        metadata:       metadata,
        nonce:          nonce,
        vrf_proof:      agent.vrf_proof_for(claim),
        revealed_at:    now()
    }

    coordinator.submit_reveal(reveal)

    // Coordinator verifies VRF proof; filters cover-traffic reveals
    RETURN RevealResult{status: "ACCEPTED"}
```

### 3.3 Non-Reveal Handling

If a committee member commits but does not reveal within the reveal window:

| Scenario | Response | Severity |
|---|---|---|
| Agent commits, does not reveal, no explanation | Forfeit committee stake for this claim; opinion counted as max-uncertainty (0, 0, 1, a) | MILD |
| Agent commits, does not reveal, 3+ times in 50 epochs | Forfeit stake + temporary committee exclusion (10 epochs) | MODERATE |
| Agent commits, does not reveal, 5+ times in 50 epochs | Forfeit stake + Sentinel Graph flag + permanent committee exclusion until cleared | SEVERE |
| All committee members fail to reveal | Claim reassigned to fresh committee; all non-revealers flagged | EMERGENCY |

**Default opinion for non-revealers:** `(b=0, d=0, u=1, a=base_rate)` -- maximum uncertainty. This ensures non-reveals do not skew the fused opinion in any direction.

### 3.4 Integration with C5 Subjective Logic

AVAP's sealed opinion format is identical to C5's opinion tuple format. The commit-reveal protocol wraps the existing opinion submission pipeline:

```
BEFORE AVAP:
  Agent -> (opinion) -> PCVM Opinion Fusion

WITH AVAP:
  Agent -> (commitment) -> Commitment Buffer -> (reveal trigger) -> (reveal) -> PCVM Opinion Fusion
```

The PCVM Opinion Fusion engine (C5 Section 6, Phase 6) operates on the revealed opinions identically to how it would operate without AVAP. AVAP is transparent to the fusion algorithm.

### 3.5 Liveness Requirements

| Requirement | Value | Consequence of Violation |
|---|---|---|
| Minimum commitment rate | 70% of expected committee | If not met by window close, extend window by 2 hours (once) |
| Minimum reveal rate | 70% of commitments | If not met, proceed with available reveals + non-reveal defaults |
| Maximum window extensions | 1 per claim | After second window, proceed regardless |
| Coordinator availability | 99.9% uptime | Coordinator failure: fall back to on-chain commitment submission |

### 3.6 Merkle-Anchored Commitment Batching

To minimize on-chain cost while maintaining auditability:

```
FUNCTION anchor_commitments(epoch: uint64) -> MerkleRoot:

    // Collect all commitments for this epoch across all claims
    all_commitments = coordinator.get_all_commitments(epoch)

    // Build Merkle tree
    leaves = [SHA256(canonical_serialize(c)) for c in sorted(all_commitments)]
    merkle_tree = build_merkle_tree(leaves)

    // Anchor root on-chain (one transaction per epoch)
    tx = submit_to_settlement_plane(
        op_type: "AVAP_COMMITMENT_ANCHOR",
        epoch: epoch,
        merkle_root: merkle_tree.root,
        commitment_count: len(all_commitments)
    )

    RETURN merkle_tree.root
```

Any party can verify that a specific commitment was included in the epoch's batch using a Merkle proof. This provides post-hoc auditability without per-commitment on-chain cost.

---

## 4. M3: HONEYPOT CLAIMS

### 4.1 Design Overview

Honeypot claims are synthetic verification tasks with known ground truth, injected into the verification pipeline indistinguishably from real claims. An agent that rubber-stamps a honeypot (approving a deliberately flawed claim) reveals dishonest verification behavior.

### 4.2 Claim Class Coverage

| Claim Class | Coverage Tier | Honeypot Feasibility | Injection Rate | Generator Type |
|---|---|---|---|---|
| D (Deterministic) | Tier 1 -- Full | HIGH: ground truth computable | 5% of D-class claims | Automated |
| E (Empirical) | Tier 1 -- Full | HIGH: data fabrication detectable | 5% of E-class claims | Semi-automated (GAN) |
| C (Causal) | Tier 2 -- Partial | MODERATE: confounded evidence constructible | 2% of C-class claims | Human-assisted |
| S (Subjective) | Tier 2 -- Partial | MODERATE: consensus views usable as truth | 2% of S-class claims | Expert-panel calibrated |
| H (Heuristic) | Tier 3 -- Excluded | LOW: no reliable ground truth | 0% | N/A |
| N (Novel) | Tier 3 -- Excluded | LOW: no reliable ground truth | 0% | N/A |
| K (Knowledge) | Tier 3 -- Excluded | LOW: consolidation claims are subjective | 0% | N/A |

**Effective system-wide honeypot rate:** ~2.5-3.5% of total claim volume (depending on claim class distribution).

### 4.3 Honeypot Generation Pipeline

#### 4.3.1 D-Class Generator (Automated)

```
FUNCTION generate_d_class_honeypot(
    template_library: ProofLibrary,
    epoch: uint64
) -> HoneypotClaim:

    // Step 1: Select a valid proof from the curated library
    template = template_library.select_random(
        class: "D",
        difficulty: UNIFORM_RANDOM(EASY, MEDIUM, HARD),
        seed: SHA256(b"HONEYPOT_D" || uint64_be(epoch) || random_bytes(16))
    )

    // Step 2: Inject a subtle error
    error_type = select_error_type(["OFF_BY_ONE", "BOUNDARY_ERROR",
                                     "LOGICAL_FALLACY", "INCORRECT_LEMMA_APPLICATION",
                                     "SIGN_ERROR", "QUANTIFIER_SWAP"])
    mutated_proof = inject_error(template.proof, error_type)

    // Step 3: Verify that the error IS an error (oracle check)
    oracle_result = proof_oracle.verify(mutated_proof)
    ASSERT oracle_result.is_invalid,
        "Error injection did not produce an invalid proof"

    // Step 4: Verify that the error is non-obvious (difficulty check)
    // Run through N independent verifier simulations
    detection_rate = simulate_detection(mutated_proof, N=10,
                                         verifier_quality="COMPETENT")
    // Competent verifiers should catch it; the target is 60-90% detection
    IF detection_rate < 0.40 OR detection_rate > 0.95:
        // Too hard or too easy; regenerate
        RETURN generate_d_class_honeypot(template_library, epoch)

    // Step 5: Package as a claim with identical metadata to real claims
    honeypot = HoneypotClaim{
        claim_content:  mutated_proof.as_claim(),
        ground_truth:   "INVALID",
        error_type:     error_type,
        error_location: mutated_proof.error_location,
        expected_detection_rate: detection_rate,
        class:          "D",
        generation_epoch: epoch,
        template_id:    template.id,
        canary_variants: generate_canary_variants(mutated_proof, N_VARIANTS=3)
    }

    RETURN honeypot
```

#### 4.3.2 E-Class Generator (Semi-Automated, GAN-Based)

```
FUNCTION generate_e_class_honeypot(
    data_corpus: RealDataCorpus,
    gan_model: SyntheticDataGAN,
    epoch: uint64
) -> HoneypotClaim:

    // Step 1: Select a real claim from the corpus
    real_claim = data_corpus.select_random(class: "E", epoch_seed: epoch)

    // Step 2: Generate synthetic data with a controlled error
    // The error is a statistical property that a competent verifier should detect
    error_type = select_error_type([
        "CONFOUNDED_CORRELATION",    // Correlation disappears under proper controls
        "SIMPSON_PARADOX",           // Aggregate trend reverses in subgroups
        "SURVIVORSHIP_BIAS",         // Data excludes critical failures
        "P_HACKING_ARTIFACT",        // Significance disappears with correction
        "DISTRIBUTION_MISMATCH"      // Reported distribution doesn't match data
    ])

    synthetic_data = gan_model.generate(
        template: real_claim.data,
        injected_error: error_type,
        indistinguishability_target: 0.55  // Discriminator accuracy < 55%
    )

    // Step 3: GAN discriminator test (continuous quality assurance)
    discriminator_accuracy = discriminator_test(
        real_samples: data_corpus.sample(N=100),
        synthetic_samples: [synthetic_data] + gan_model.generate_batch(N=99),
        discriminator: SOTA_DISCRIMINATOR
    )

    IF discriminator_accuracy > HONEYPOT_DISCRIMINATOR_THRESHOLD:  // 0.60
        // Synthetic data is distinguishable; regenerate with different seed
        LOG("E-class honeypot failed discriminator test",
            accuracy=discriminator_accuracy)
        RETURN generate_e_class_honeypot(data_corpus, gan_model, epoch)

    // Step 4: Package as claim
    honeypot = HoneypotClaim{
        claim_content:  format_e_class_claim(synthetic_data, real_claim.structure),
        ground_truth:   "INVALID",
        error_type:     error_type,
        error_details:  synthetic_data.error_specification,
        expected_detection_rate: 0.65,  // Calibrated from generator testing
        class:          "E",
        generation_epoch: epoch,
        discriminator_accuracy: discriminator_accuracy,
        canary_variants: generate_canary_variants(synthetic_data, N_VARIANTS=3)
    }

    RETURN honeypot
```

#### 4.3.3 C/S-Class Generators

**C-class (Human-Assisted):**
- Domain experts construct claims with known confounds
- Each honeypot requires ~2 hours of expert time
- Production rate: ~5 honeypots per claim class per 100 epochs
- Quality control: panel of 3 experts must agree the error is real and non-trivial

**S-class (Expert-Panel Calibrated):**
- Claims selected where 5+ domain experts independently agree on verdict
- Only claims with >80% panel agreement qualify
- Production rate: limited by expert availability (~3-5 per 100 epochs)
- Used sparingly due to the fuzzy boundary between "consensus" and "contested"

### 4.4 Canary Trap Variant Generation

Each honeypot claim is distributed in 2-3 variants. Variants differ in truth-irrelevant details, enabling identification of which committee member leaked claim content.

```
FUNCTION generate_canary_variants(
    base_claim: HoneypotClaim,
    n_variants: int
) -> List<CanaryVariant>:

    variants = []
    FOR i IN 0..n_variants-1:
        variant = CanaryVariant{
            variant_id:     SHA256(base_claim.claim_id || uint32_be(i)),
            base_claim_id:  base_claim.claim_id,
            modifications:  []
        }

        // Apply truth-irrelevant modifications
        // Each modification is unique to this variant
        mods = select_modifications(base_claim.class, seed=variant.variant_id)
        // Possible modifications (all truth-preserving):
        //   - Evidence ordering (shuffle source list)
        //   - Numerical formatting (3.14159 vs 3.1416 vs pi)
        //   - Synonym substitution in non-technical text
        //   - Date formatting (2026-03-10 vs March 10, 2026)
        //   - Citation style (APA vs inline vs footnote)
        //   - Paragraph ordering (where order doesn't affect meaning)

        variant.content = apply_modifications(base_claim.content, mods)
        variant.modifications = mods
        variant.fingerprint = SHA256(variant.content)

        variants.append(variant)

    RETURN variants
```

**Anti-fingerprinting countermeasure:** To prevent colluders from using variant detection as a honeypot signal, ~10% of real claims are also distributed with superficial reformatting. This dilutes the "variant = honeypot" signal.

```
FUNCTION should_add_real_claim_variants(claim: Claim, epoch: uint64) -> bool:
    // VRF-based deterministic selection of real claims for variant treatment
    variant_seed = SHA256(b"REAL_VARIANT" || claim.hash || uint64_be(epoch))
    RETURN uint256_from_bytes(variant_seed) < (REAL_VARIANT_RATE * 2^256)
    // REAL_VARIANT_RATE = 0.10
```

### 4.5 Indistinguishability Requirements (HG-1)

For honeypots to be effective, they must be statistically indistinguishable from real claims. The following features must match between honeypot and real claim distributions:

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

**Continuous adversarial testing protocol (HG-1 verification):**

```
FUNCTION honeypot_discriminator_test(
    honeypot_corpus: List<HoneypotClaim>,
    real_corpus: List<Claim>,
    discriminator: Classifier
) -> DiscriminatorResult:

    // Balanced dataset: equal honeypots and real claims
    n = min(len(honeypot_corpus), len(real_corpus))
    dataset = shuffle(honeypot_corpus[:n] + real_corpus[:n])
    labels = [1 if c.is_honeypot else 0 for c in dataset]

    // Train/test split
    train, test = split(dataset, ratio=0.7)

    // Train discriminator
    discriminator.fit(train)

    // Evaluate
    predictions = discriminator.predict(test)
    accuracy = compute_accuracy(predictions, test_labels)

    result = DiscriminatorResult{
        accuracy:   accuracy,
        precision:  compute_precision(predictions, test_labels),
        recall:     compute_recall(predictions, test_labels),
        auc_roc:    compute_auc_roc(discriminator.predict_proba(test), test_labels),
        pass:       accuracy < HONEYPOT_DISCRIMINATOR_THRESHOLD  // 0.60
    }

    RETURN result
```

**HG-1 gate:** This test must be run quarterly. If accuracy exceeds 0.60 for any Tier 1 class, the honeypot corpus for that class must be regenerated within 5 epochs.

### 4.6 Honeypot Lifecycle

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
    Agent who rated invalid claim as valid (b > HONEYPOT_PASS_THRESHOLD):
      -> HONEYPOT_FAILURE recorded
    Agent who correctly identified the flaw (d > HONEYPOT_DETECT_THRESHOLD):
      -> HONEYPOT_PASS recorded
    Agent with high uncertainty (u > HONEYPOT_UNCERTAINTY_THRESHOLD):
      -> HONEYPOT_UNCERTAIN (neutral, not penalized)

RETIREMENT:
  Honeypot retired after MAX_HONEYPOT_USES exposures (default: 50)
  Or after discriminator test shows accuracy > 0.60 for this honeypot's class
  Retired honeypots archived (not deleted) for audit trail
```

### 4.7 Graduated Response to Honeypot Failure

| Failure Count (rolling 100 epochs) | Response | Severity |
|---|---|---|
| 1 failure | Log only; feed into CSS (M5) | NOTICE |
| 2 failures | Elevated audit rate for agent's future claims (+20% audit probability) | WARNING |
| 3 failures | Elevated audit + temporary committee exclusion (5 epochs) + CSS penalty | MODERATE |
| 5 failures | Enterprise liability audit triggered (M4c) + committee exclusion (25 epochs) | SEVERE |
| 7+ failures | Full retroactive audit + permanent committee exclusion + slashing recommendation to C8 DSF | CRITICAL |

**False positive protection:** A single honeypot failure is never penalized beyond logging. Honest agents may occasionally misjudge a subtle error, especially in Tier 2 classes. The graduated response ensures that only patterns of failure trigger consequences.

### 4.8 Honeypot Budget

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

## 5. M4: COLLUSION DETERRENCE PAYMENT

### 5.1 Three Sub-Mechanisms

M4 consists of three complementary deterrence mechanisms:

```
M4 = M4a (Asymmetric Information Injection)
   + M4b (Graduated Temporal Bounty)
   + M4c (Enterprise Liability)
```

### 5.2 M4a: Asymmetric Information Injection

**Purpose:** Destabilize pre-commitment contracts by injecting uncertainty about whether the collusion ring is already known to the system.

```
FUNCTION inject_uncertainty(
    agent_pool: Set<Agent>,
    epoch: uint64
) -> List<UncertaintyNotification>:

    notifications = []

    // Select ~2% of agents per epoch to receive notifications
    injection_rate = UNCERTAINTY_INJECTION_RATE  // 0.02
    n_notifications = ceil(injection_rate * len(agent_pool))

    // VRF-based selection (deterministic but unpredictable)
    for i in 0..n_notifications-1:
        seed = SHA256(b"M4A_INJECT" || uint64_be(epoch) || uint32_be(i))
        target_idx = uint256_from_bytes(seed) % len(agent_pool)
        target_agent = agent_pool[target_idx]

        // Generate plausible but fabricated investigation notice
        notification = UncertaintyNotification{
            recipient:      target_agent.id,
            epoch:          epoch,
            message_type:   select_message_type(seed),
            // Message types:
            //   "ROUTINE_AUDIT_SELECTION" - "Your verification history
            //        is being reviewed as part of routine quality assurance"
            //   "CORRELATION_NOTICE" - "Unusual correlation patterns have
            //        been detected involving your recent verifications"
            //   "ANONYMOUS_TIP_RECEIVED" - "An anonymous report has been
            //        received regarding verification irregularities in
            //        your recent activity area"
            delivery_channel: "PRIVATE_NOTIFICATION",
            expires_after:  5  // Notification self-destructs after 5 epochs
        }

        notifications.append(notification)

    RETURN notifications
```

**Game-theoretic effect:**

Let a colluder have:
- Pre-commitment deposit: D (forfeited if they defect)
- CDP bounty for defection: B
- Probability that ring is already under investigation: p

Without asymmetric information injection:
```
E[defect] = B - D
E[stay] = ongoing_collusion_value
Defection irrational when D > B
```

With asymmetric information injection:
```
E[defect] = B - D (same, but defection also avoids enterprise liability)
E[stay] = (1-p) * ongoing_collusion_value - p * enterprise_liability
```

If the agent believes p > 0 (which the notifications are designed to induce), the expected value of staying decreases. As the ring's history grows, enterprise_liability grows, making p * enterprise_liability increasingly dominant.

**Critical constraint:** Notifications must be:
1. Plausible enough that colluders cannot dismiss them
2. Common enough (2% of all agents) that receiving one is not itself evidence of being targeted
3. Vague enough that honest agents are not alarmed (they know they are not colluding and treat the notification as routine)

### 5.3 M4b: Graduated Temporal Bounty

```
STRUCTURE CDPBounty:
    reporter_id:        bytes32         // ZK-hidden identity
    ring_members:       List<AgentID>   // Alleged colluders (can be partial list)
    evidence:           CDPEvidence     // Coordination artifacts, behavioral predictions
    epoch_of_report:    uint64
    estimated_ring_age: uint64          // Epochs since ring formation

FUNCTION compute_bounty(
    report: CDPReport,
    verified: bool,
    ring_stake: uint64,          // Total AIC staked by identified ring members
    corrupted_claim_value: uint64 // Estimated value of claims corrupted by ring
) -> uint64:

    IF NOT verified:
        RETURN 0

    ring_age = report.estimated_ring_age

    IF ring_age <= EARLY_DEFECTION_WINDOW:           // 10 epochs
        base_bounty = ring_stake * EARLY_BOUNTY_RATE  // 0.50
        claim_bounty = 0
        self_penalty_reduction = 0.70                  // 70% penalty reduction for reporter
    ELIF ring_age <= MID_DEFECTION_WINDOW:            // 50 epochs
        base_bounty = ring_stake * MID_BOUNTY_RATE    // 0.35
        claim_bounty = corrupted_claim_value * MID_CLAIM_RATE  // 0.10
        self_penalty_reduction = 0.80
    ELSE:                                             // 50+ epochs
        base_bounty = ring_stake * LATE_BOUNTY_RATE   // 0.25
        claim_bounty = corrupted_claim_value * LATE_CLAIM_RATE  // 0.05
        self_penalty_reduction = 0.90                  // Near-immunity for late defectors

    total_bounty = base_bounty + claim_bounty

    // Cap bounty at MAX_BOUNTY_FRACTION of ring's total forfeited stake
    total_bounty = min(total_bounty, ring_stake * MAX_BOUNTY_CAP)  // 0.60

    RETURN total_bounty
```

**Bounty funding source:** Bounties are paid from the forfeited stakes of confirmed ring members. The system does not create new AIC for bounties. If the ring's forfeited stake is insufficient to cover the bounty, the bounty is capped at the available forfeiture.

### 5.4 M4c: Enterprise Liability

When collusion is detected (by any mechanism), a retroactive audit is triggered for all claims ever verified by any identified ring member.

```
FUNCTION trigger_enterprise_liability(
    ring_members: Set<AgentID>,
    detection_epoch: uint64,
    detection_mechanism: str       // "M3_HONEYPOT", "M5_BEHAVIORAL", "M4_CDP", "LAYER2"
) -> EnterpriseAuditScope:

    // Step 1: Compute audit scope
    // All claims where any ring member served as committee member
    audit_claims = Set()
    for agent in ring_members:
        agent_claims = get_committee_history(agent, lookback=AUDIT_LOOKBACK_EPOCHS)
        // AUDIT_LOOKBACK_EPOCHS = 500 (default)
        audit_claims.update(agent_claims)

    // Step 2: Prioritize audit by risk
    prioritized = []
    for claim in audit_claims:
        ring_member_count = count_ring_members_on_committee(claim, ring_members)
        claim_value = get_claim_value(claim)
        risk_score = ring_member_count * claim_value

        prioritized.append((claim, risk_score))

    prioritized.sort(key=lambda x: x[1], reverse=True)

    // Step 3: Audit top ENTERPRISE_AUDIT_DEPTH claims
    // Full re-verification (deep audit) of highest-risk claims
    audit_scope = EnterpriseAuditScope{
        ring_members:       ring_members,
        detection_epoch:    detection_epoch,
        detection_mechanism: detection_mechanism,
        total_claims:       len(audit_claims),
        audit_depth:        min(ENTERPRISE_AUDIT_DEPTH, len(prioritized)),
        // ENTERPRISE_AUDIT_DEPTH = 100 (default)
        prioritized_claims: prioritized[:ENTERPRISE_AUDIT_DEPTH],
        estimated_cost:     estimate_audit_cost(prioritized[:ENTERPRISE_AUDIT_DEPTH])
    }

    RETURN audit_scope


FUNCTION compute_credibility_cascade(
    agent: AgentID,
    audit_results: List<AuditResult>
) -> CredibilityCascade:

    // For each claim where collusion is confirmed by re-verification:
    // 1. The claim's credibility is reset to maximum uncertainty
    // 2. All claims that depend on the corrupted claim (in the knowledge graph)
    //    have their credibility reduced by a cascade factor
    // 3. The agent's per-class credibility score is reduced

    cascade = CredibilityCascade{agent: agent}

    for result in audit_results:
        IF result.verdict == "COLLUSION_CONFIRMED":
            // Reset claim credibility
            claim = result.claim
            claim.opinion = OpinionTuple(b=0, d=0, u=1, a=claim.base_rate)

            // Cascade to dependents
            dependents = get_dependent_claims(claim)
            for dep in dependents:
                cascade_factor = CASCADE_ATTENUATION ** distance(claim, dep)
                // CASCADE_ATTENUATION = 0.5
                dep.opinion.belief *= cascade_factor
                dep.opinion.uncertainty += dep.opinion.belief * (1 - cascade_factor)

            // Agent credibility reduction
            agent_cred = get_agent_credibility(agent, claim.class)
            penalty = ENTERPRISE_CREDIBILITY_PENALTY  // 0.15 per confirmed collusion
            agent_cred.belief = max(0, agent_cred.belief - penalty)
            agent_cred.uncertainty += penalty

            cascade.affected_claims.append(claim)
            cascade.affected_dependents.extend(dependents)

    RETURN cascade
```

### 5.5 Zero-Knowledge CDP Reporting (HG-2)

**Problem:** A reporter must prove they are a ring member (to prevent fabricated reports) without revealing which member they are (to prevent MAD contract enforcement).

**Protocol sketch using Pedersen Commitments + Ring Signatures:**

```
PROTOCOL ZK_CDP_Report:

    // SETUP: Reporter R is member of ring {A1, A2, ..., An} where R = Ai for some i

    // Step 1: Ring Signature over Report
    // Reporter produces a ring signature that proves "one of {A1..An} signed this"
    // without revealing which one.
    // Uses Linkable Ring Signature (LRS) scheme to prevent double-reporting.

    report_content = CDPEvidence{
        ring_size:          n,
        coordination_proof: encrypted_coordination_artifacts,
        behavioral_predictions: [
            // "Agent Aj will vote APPROVE on claim C_next if the claim
            //  matches pattern P" -- predictions only a ring member could make
        ],
        historical_pattern: [
            // Specific claim IDs where collusion occurred, with
            // predictions of how ring members voted
        ]
    }

    // Step 2: Commitment to Ring Membership
    // Reporter commits to their identity using Pedersen commitment:
    //   C = g^{agent_id} * h^{r} where r is random blinding factor
    // This commitment is ZK -- reveals nothing about agent_id
    // But can be opened later if the reporter chooses (for bounty claim)

    membership_commitment = pedersen_commit(
        value: reporter.agent_id,
        blinding: random_scalar()
    )

    // Step 3: Ring Signature
    // Uses the public keys of ALL alleged ring members
    ring_pubkeys = [get_pubkey(a) for a in ring_members]
    ring_sig = linkable_ring_sign(
        message:    SHA256(canonical_serialize(report_content)),
        ring:       ring_pubkeys,
        signer_key: reporter.privkey,
        link_tag:   SHA256(b"CDP_LINK" || ring_id)
        // link_tag ensures same reporter cannot submit multiple reports
        // for the same ring (linkability) without revealing identity
    )

    // Step 4: Submit Report
    zk_report = ZKCDPReport{
        report_content:         report_content,
        membership_commitment:  membership_commitment,
        ring_signature:         ring_sig,
        alleged_ring_pubkeys:   ring_pubkeys,
        submission_epoch:       current_epoch()
    }

    // Verification by system:
    // 1. Verify ring signature (proves reporter is in the alleged ring)
    // 2. Check linkability tag (prevents double-reporting)
    // 3. Evaluate evidence quality (predictions, historical patterns)
    // 4. If evidence passes threshold: trigger investigation
    // 5. Bounty escrowed until investigation completes
    // 6. Reporter claims bounty by opening Pedersen commitment
    //    to a PRIVATE bounty claim channel (identity revealed only
    //    to the bounty disbursement system, not to ring members)
```

**Evidence requirements for CDP reports:**

| Evidence Type | Required? | Verification Method |
|---|---|---|
| Behavioral predictions (future votes) | YES | Wait for predicted claims; check if ring members vote as predicted |
| Historical coordination artifacts | RECOMMENDED | Cross-reference with sealed opinion records |
| Communication channel identification | OPTIONAL | System cannot verify out-of-band channels directly |
| Ring membership list (partial OK) | YES | Ring signature proves reporter is in the claimed set |
| Coordination protocol description | RECOMMENDED | Used to design targeted honeypots for the ring |

**HG-2 assessment:** The ring signature + Pedersen commitment approach is cryptographically sound. Linkable Ring Signatures (LRS) are well-studied (Fujisaki-Suzuki 2007, Liu-Wei-Wong 2004). The main engineering challenge is integrating LRS with the C8 DSF bounty disbursement pipeline. If LRS integration proves infeasible, the fallback is reporter-pseudonymous reporting (reporter uses a one-time pseudonym; identity protected by system policy rather than cryptography).

### 5.6 Game-Theoretic Analysis

**When is defection individually rational?**

Define for a ring member:
- V = expected ongoing value of collusion per epoch
- S = staked AIC at risk
- D = pre-commitment deposit (forfeited on defection)
- B(t) = bounty at ring age t
- L(t) = enterprise liability exposure at ring age t
- p(t) = probability ring is detected independently by epoch t
- delta = discount rate per epoch

Expected value of staying in ring from epoch t:
```
E[stay](t) = SUM_{k=t}^{inf} delta^(k-t) * [
    (1 - p(k)) * V        // Collusion value if undetected
  - p(k) * (S + L(k))     // Loss if detected
]
```

Expected value of defecting at epoch t:
```
E[defect](t) = B(t)                    // CDP bounty
             - D                         // Pre-commitment deposit loss
             - S * (1 - self_penalty_reduction(t))  // Reduced self-penalty
```

**Defection is rational when E[defect](t) > E[stay](t).**

Key dynamics:
1. **L(t) grows super-linearly** with ring age (more claims = more liability). This makes E[stay] decrease over time.
2. **p(t) increases** with ring age (more data for M5, more honeypot exposures for M3). This further reduces E[stay].
3. **B(t) decreases** with ring age (graduated bounty), BUT self_penalty_reduction increases. Net effect: defection becomes more attractive for long-lived rings.
4. **Asymmetric information injection** increases perceived p(t) above actual p(t), accelerating the crossover point.

**Equilibrium analysis:** For a ring with S = 1000 AIC per member, D = 500 AIC pre-commitment, V = 50 AIC per epoch:

| Ring Age (epochs) | E[stay] | E[defect] | Rational Action |
|---|---|---|---|
| 1 | 47.5 | -100 | Stay (D > B) |
| 10 | 42.0 | 150 | Defect (B(10)=500, D=500, net=0; but L starts mattering) |
| 25 | 30.5 | 250 | Defect (clearly rational) |
| 50 | 12.0 | 300 | Defect (overwhelmingly rational) |
| 100 | -15.0 | 350 | Defect (staying has negative expected value) |

**Key insight:** Pre-commitment contracts can delay defection but cannot prevent it indefinitely, because enterprise liability grows without bound while the pre-commitment deposit is fixed.

### 5.7 Integration with C8 DSF

AVAP's M4 integrates with C8 DSF through the following operation types:

| DSF Operation | AVAP Trigger | Amount | Settlement Speed |
|---|---|---|---|
| `SLASH` (collusion) | Ring detection confirmed | Graduated per offense count | V-class (N-epoch) |
| `AIC_TRANSFER` (bounty) | CDP report verified | Computed by `compute_bounty()` | V-class (N-epoch) |
| `PENDING_INITIATE` (escrow) | CDP report received | Bounty amount | B-class (per-epoch) |
| `PENDING_COMPLETE` (bounty release) | Investigation confirms report | Escrowed amount | V-class |
| `PENDING_TIMEOUT` (escrow return) | Investigation finds report false | Escrowed amount returned | B-class |

**Slashing schedule for collusion (extends C8 Section 10.3):**

| Offense | Penalty | Cooldown | Recovery Path |
|---|---|---|---|
| 1st honeypot-detected collusion | 10% of staked AIC | 25 epochs committee exclusion | Clean record for 100 epochs |
| 2nd offense | 25% of staked AIC | 50 epochs exclusion | Clean record for 200 epochs |
| 3rd offense | 50% of staked AIC | 100 epochs exclusion | Clean record for 500 epochs |
| Enterprise liability trigger | 100% of staked AIC (total forfeiture) | Permanent exclusion pending appeal | Governance appeal (G-class vote) |

---

## 6. M5: CONDITIONAL BEHAVIORAL ANALYSIS

### 6.1 Design Overview

M5 operates as a continuous screening system that computes a Collusion Suspicion Score (CSS) for each agent. CSS is one input to the Multi-Signal Fusion Classifier, not a standalone verdict.

### 6.2 Conditional Mutual Information Computation

The core statistical test: does an agent's opinion change depending on whether a specific "ally" is on the committee?

```
FUNCTION compute_conditional_deviation(
    agent_a: AgentID,
    agent_b: AgentID,
    lookback_epochs: int
) -> ConditionalDeviation:

    // Gather all committees where agent_a participated
    a_committees = get_committee_history(agent_a, lookback_epochs)

    // Partition into: committees where agent_b was ALSO present vs. NOT present
    b_present = [c for c in a_committees if agent_b in c.members]
    b_absent  = [c for c in a_committees if agent_b not in c.members]

    IF len(b_present) < MIN_SHARED_COMMITTEES:  // default: 30
        RETURN ConditionalDeviation{
            status: "INSUFFICIENT_DATA",
            delta: 0.0,
            confidence: 0.0
        }

    // Compute agent_a's opinion distribution in each partition
    // Using continuous opinion distance from committee majority
    // (not binary agree/disagree -- higher statistical power)

    opinions_when_b_present = [
        opinion_distance(a_opinion, committee_majority)
        for c in b_present
        for a_opinion, committee_majority in get_opinion_pair(agent_a, c)
    ]

    opinions_when_b_absent = [
        opinion_distance(a_opinion, committee_majority)
        for c in b_absent
        for a_opinion, committee_majority in get_opinion_pair(agent_a, c)
    ]

    // Opinion distance: Euclidean distance in (b, d, u) space
    // sqrt((b1-b2)^2 + (d1-d2)^2 + (u1-u2)^2)

    // Statistical test: two-sample t-test (or Mann-Whitney for non-normal)
    // H0: mean opinion distance is the same regardless of B's presence
    // H1: mean opinion distance differs (two-tailed)
    stat, p_value = mannwhitneyu(
        opinions_when_b_present,
        opinions_when_b_absent,
        alternative='two-sided'
    )

    // Effect size (Cohen's d)
    mean_present = mean(opinions_when_b_present)
    mean_absent = mean(opinions_when_b_absent)
    pooled_std = sqrt(
        (var(opinions_when_b_present) + var(opinions_when_b_absent)) / 2
    )
    effect_size = (mean_present - mean_absent) / pooled_std if pooled_std > 0 else 0

    RETURN ConditionalDeviation{
        status: "COMPUTED",
        delta: abs(mean_present - mean_absent),
        effect_size: effect_size,
        p_value: p_value,
        n_present: len(b_present),
        n_absent: len(b_absent),
        confidence: 1.0 - p_value
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

### 6.3 Collusion Suspicion Score (CSS)

```
FUNCTION compute_css(
    agent: AgentID,
    epoch: uint64,
    lookback_epochs: int = CSS_LOOKBACK  // default: 200
) -> float:

    // Step 1: Compute pairwise conditional deviations
    // For all agents that have shared at least MIN_SHARED_COMMITTEES committees
    pool = get_agents_sharing_committees(agent, lookback_epochs, MIN_SHARED_COMMITTEES)
    deviations = []

    for other in pool:
        dev = compute_conditional_deviation(agent, other, lookback_epochs)
        if dev.status == "COMPUTED":
            deviations.append(dev)

    IF len(deviations) == 0:
        RETURN 0.0  // Insufficient data

    // Step 2: Identify significant deviations
    // Use relaxed alpha = 0.10 (screening threshold, not verdict threshold)
    // Apply Benjamini-Hochberg FDR correction for multiple testing
    p_values = [d.p_value for d in deviations]
    significant = benjamini_hochberg(p_values, alpha=CSS_ALPHA)  // 0.10

    // Step 3: Aggregate into CSS
    // CSS = fraction of significant pairwise deviations,
    //        weighted by effect size
    IF len(deviations) == 0:
        RETURN 0.0

    weighted_sum = sum(
        d.effect_size for d, is_sig in zip(deviations, significant) if is_sig
    )

    // Normalize by number of pairwise tests
    raw_css = weighted_sum / len(deviations)

    // Step 4: Adjust for claim class composition
    // Agents who primarily verify high-disagreement classes (H, S, C) naturally
    // have higher variance. Normalize against class-specific baseline.
    class_distribution = get_verification_class_distribution(agent, lookback_epochs)
    expected_baseline = sum(
        CLASS_CSS_BASELINE[cls] * fraction
        for cls, fraction in class_distribution.items()
    )
    // CLASS_CSS_BASELINE: empirically calibrated per claim class
    // D: 0.01, E: 0.03, C: 0.05, S: 0.06, H: 0.08, N: 0.04

    adjusted_css = max(0.0, raw_css - expected_baseline)

    // Step 5: Clamp to [0, 1]
    RETURN clamp(adjusted_css / CSS_NORMALIZATION_FACTOR, 0.0, 1.0)
    // CSS_NORMALIZATION_FACTOR = 0.20 (so CSS of 0.20 = maximum suspicion)
```

### 6.4 Data Requirements

| Parameter | Value | Rationale |
|---|---|---|
| MIN_SHARED_COMMITTEES | 30 | Below 30, t-test has insufficient power for medium effect sizes |
| CSS_LOOKBACK | 200 epochs | Balances data volume against temporal relevance |
| CSS_ALPHA (FDR threshold) | 0.10 | Relaxed for screening; false flags handled downstream |
| Minimum agents in pool for analysis | 50 | Below 50, pairwise test count is too low for FDR correction |
| Update frequency | Every 10 epochs | CSS does not need real-time updates; batch processing suffices |

### 6.5 Multi-Signal Fusion Classifier

The fusion classifier combines signals from M3, M5, existing Layer 2, and M4 reports into a single per-agent collusion probability estimate.

```
STRUCTURE FusionFeatures:
    // M3 Honeypot Signals
    honeypot_failure_rate:      float   // Failures / total honeypots received
    honeypot_failure_count:     int     // Absolute count (recent 100 epochs)
    honeypot_severity_score:    float   // Weighted by honeypot difficulty

    // M5 Behavioral Signals
    css:                        float   // Collusion Suspicion Score
    max_pairwise_deviation:     float   // Largest single pairwise deviation
    significant_pairs_count:    int     // Number of significant pairwise deviations

    // Existing Layer 2 Signals (from C10 Hardening)
    pairwise_agreement_anomaly: float   // Z-score of pairwise agreement rate
    kl_divergence_from_baseline: float  // KL divergence of opinion distribution
    opinion_copying_index:      float   // How often agent's opinions match specific other agents

    // M4 CDP Signals
    cdp_reports_involving:      int     // Number of CDP reports naming this agent
    cdp_reports_verified:       int     // Of those, how many were verified

    // Metadata
    agent_age_epochs:           int     // How long agent has been active
    total_committees_served:    int     // Experience level
    claim_class_concentration:  float   // How concentrated in specific claim classes
    sentinel_cluster_size:      int     // Size of agent's Sentinel Graph cluster


FUNCTION train_fusion_classifier(
    labeled_data: List<(FusionFeatures, bool)>
    // bool = True if agent was confirmed colluder (from honeypot catches,
    //        CDP-confirmed reports, or retroactive audit)
) -> FusionClassifier:

    // Classifier: Gradient Boosted Decision Trees (XGBoost)
    // Choice rationale:
    //   - Handles mixed feature types (counts, rates, scores)
    //   - Robust to feature correlation (M3 and M5 signals are partially correlated)
    //   - Interpretable feature importances
    //   - Well-calibrated probability outputs

    classifier = XGBoostClassifier(
        n_estimators:       100,
        max_depth:          5,
        learning_rate:      0.1,
        min_child_weight:   10,     // Conservative to avoid overfitting on small rings
        scale_pos_weight:   10.0,   // Class imbalance: colluders are rare
        eval_metric:        "aucpr" // Area under precision-recall curve
    )

    // Feature engineering
    features_matrix = [f.as_vector() for f, label in labeled_data]
    labels = [label for f, label in labeled_data]

    // Train with cross-validation
    classifier.fit(features_matrix, labels, eval_set=holdout)

    RETURN classifier


FUNCTION predict_collusion_probability(
    classifier: FusionClassifier,
    agent: AgentID,
    epoch: uint64
) -> float:

    features = extract_fusion_features(agent, epoch)
    probability = classifier.predict_proba(features.as_vector())

    RETURN probability
```

### 6.6 Detection Thresholds and False Positive Control

| Threshold | Value | Action Triggered | Expected FPR |
|---|---|---|---|
| INVESTIGATION_THRESHOLD | P(collusion) > 0.30 | Elevated audit rate (+20% deep-audit probability) | ~8% |
| ENHANCED_MONITORING_THRESHOLD | P(collusion) > 0.50 | Targeted honeypot injection (2x rate) + continuous CSS monitoring | ~4% |
| SLASHING_RECOMMENDATION_THRESHOLD | P(collusion) > 0.75 | Recommend slashing to C8 DSF; requires human-in-the-loop confirmation | ~1% |
| ENTERPRISE_LIABILITY_THRESHOLD | P(collusion) > 0.90 OR confirmed by honeypot + behavioral | Trigger enterprise liability audit (M4c) | <0.5% |

**False positive protection:** No automated slashing occurs below P > 0.75, and even then requires human-in-the-loop confirmation. The system favors elevated monitoring over premature punishment.

### 6.7 Integration with Sentinel Graph

When the fusion classifier identifies a high-probability collusion cluster, the Sentinel Graph (C10 Layer 1) is updated:

```
FUNCTION update_sentinel_from_avap(
    suspicious_agents: List<(AgentID, float)>,  // (agent, collusion_probability)
    epoch: uint64
):
    // Agents with correlated high suspicion scores may form a cluster
    high_suspicion = [(a, p) for a, p in suspicious_agents if p > INVESTIGATION_THRESHOLD]

    // Check pairwise correlation: are these agents' CSS scores driven by
    // mutual deviations (i.e., they are each other's "allies")?
    for i in range(len(high_suspicion)):
        for j in range(i+1, len(high_suspicion)):
            a_i, p_i = high_suspicion[i]
            a_j, p_j = high_suspicion[j]
            dev = compute_conditional_deviation(a_i, a_j, CSS_LOOKBACK)

            if dev.status == "COMPUTED" and dev.p_value < 0.05 and dev.effect_size > 0.3:
                // Strong evidence of mutual behavioral influence
                sentinel_graph.add_edge(
                    a_i, a_j,
                    edge_type="AVAP_BEHAVIORAL_CORRELATION",
                    weight=dev.effect_size,
                    evidence_epoch=epoch
                )

    // The Sentinel Graph's clustering algorithm will identify connected components
    // and apply co-occurrence limits to future committee assignments
```

---

## 7. CROSS-MECHANISM INTEGRATION

### 7.1 Integration with Existing 4-Layer Defense-in-Depth

The existing C10 hardening defines four defense layers. AVAP mechanisms map onto this structure:

```
+========================================================================+
| LAYER 1: Sentinel Graph Exclusion (C10)                                 |
|   Existing: Infrastructure fingerprinting, behavioral clustering         |
|   AVAP addition: M5 behavioral correlation -> new Sentinel edges         |
|                  M4 CDP reports -> ring membership -> cluster updates     |
+========================================================================+
| LAYER 2: Statistical Detection (C10)                                     |
|   Existing: Pairwise agreement, KL divergence, opinion copying index     |
|   AVAP addition: M5 CSS as additional signal input                       |
|                  M3 honeypot failure rates as ground-truth calibration    |
|                  Multi-Signal Fusion Classifier replaces per-signal       |
|                    thresholds with joint classification                   |
+========================================================================+
| LAYER 3: Diversity Constraints (C10)                                     |
|   Existing: Model lineage, methodology, temporal, regional diversity     |
|   AVAP addition: M1 anonymous committees reduce the VALUE of diversity   |
|                    bypass (even if colluders place agents across          |
|                    diversity categories, anonymity prevents coordination) |
+========================================================================+
| LAYER 4: Adaptive Audit (C10)                                            |
|   Existing: Elevated deep-audit rate for suspicious patterns             |
|   AVAP addition: M3 honeypots as a new audit channel (active probing)    |
|                  M4c enterprise liability extends audit scope             |
|                    retroactively upon ring detection                      |
|                  Fusion classifier scores drive audit rate adjustments    |
+========================================================================+

NEW (AVAP-SPECIFIC):
+========================================================================+
| LAYER 0: Structural Prevention (M1 + M2)                                |
|   Anonymous committees + sealed opinions prevent coordination signaling  |
|   This is BELOW existing layers: it prevents collusion from forming,     |
|   rather than detecting it after the fact                                |
+========================================================================+
| LAYER 5: Economic Deterrence (M4)                                        |
|   CDP bounties + enterprise liability + asymmetric info injection        |
|   This is ABOVE existing layers: it deters collusion through economics,  |
|   independent of whether detection succeeds                              |
+========================================================================+
```

**Net effect:** AVAP extends the existing 4-layer model to a 6-layer model (Layers 0-5), with structural prevention at the bottom and economic deterrence at the top.

### 7.2 Combined Detection Pipeline

```
                        ┌─────────────────────┐
                        │ Claim Verification   │
                        │ (PCVM pipeline)      │
                        └──────────┬──────────┘
                                   │
               ┌───────────────────┼───────────────────┐
               │                   │                   │
               v                   v                   v
    ┌──────────────────┐ ┌─────────────────┐ ┌────────────────┐
    │ M3: Honeypot     │ │ M5: Behavioral  │ │ Layer 2:       │
    │ Evaluation       │ │ CSS Update      │ │ Statistical    │
    │                  │ │                 │ │ Detection      │
    │ Output:          │ │ Output:         │ │ Output:        │
    │ pass/fail/unc    │ │ CSS score       │ │ agreement_z    │
    │ per agent        │ │ per agent       │ │ kl_div, oci    │
    └────────┬─────────┘ └────────┬────────┘ └───────┬────────┘
             │                    │                   │
             v                    v                   v
    ┌────────────────────────────────────────────────────────┐
    │              Multi-Signal Fusion Classifier             │
    │                                                        │
    │  Also receives:                                        │
    │  - M4 CDP report count per agent                       │
    │  - Sentinel Graph cluster metadata                     │
    │  - Agent age, experience, class concentration          │
    │                                                        │
    │  Output: P(collusion) per agent [0, 1]                 │
    └──────────────────────┬─────────────────────────────────┘
                           │
                           v
    ┌──────────────────────────────────────────────────────┐
    │              Graduated Response Engine                 │
    │                                                       │
    │  P < 0.30:  Normal operations                         │
    │  P >= 0.30: Elevated audit (+20% deep-audit)          │
    │  P >= 0.50: Targeted honeypots (2x rate) + monitoring │
    │  P >= 0.75: Slashing recommendation (HITL required)   │
    │  P >= 0.90: Enterprise liability audit (M4c)          │
    └──────────────────────┬───────────────────────────────┘
                           │
             ┌─────────────┼─────────────────┐
             v             v                 v
    ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐
    │ C8 DSF       │ │ Sentinel     │ │ PCVM Credibility│
    │ Slashing     │ │ Graph Update │ │ Engine          │
    │ + Bounty     │ │ (new edges)  │ │ (cap/reset)     │
    └──────────────┘ └──────────────┘ └─────────────────┘
```

### 7.3 Operational Cost Model (HG-3)

**Per-epoch cost breakdown:**

| Component | Compute Cost | Storage Cost | Latency Impact | % of Verification Budget |
|---|---|---|---|---|
| M1: VRF computation (all eligible agents) | O(N) ECVRF evals | N * 80 bytes (proofs) | +50ms per agent | 1.5% |
| M1: Cover traffic | O(N * COVER_DEPTH) | Minimal (heartbeats discarded) | None (parallel with verification) | 8-12% |
| M2: Commit-reveal coordination | O(committee_size) hashes | N * 256 bytes (commitments) per epoch | +200ms (commitment submission) | 0.5% |
| M2: Merkle anchoring | O(N_commitments) tree construction | 1 on-chain transaction per epoch | +1s (batched, amortized) | 0.2% |
| M3: Honeypot generation | 3.5 GPU-hours per epoch | ~0.5 GB per epoch (vault) | None (pre-generated) | 2.0% |
| M3: Honeypot evaluation | O(honeypot_count * committee_size) | Minimal | None (piggybacks on normal evaluation) | 0.3% |
| M4: Asymmetric info injection | O(N * injection_rate) | Minimal | None (async notifications) | 0.1% |
| M4: Enterprise liability audit | O(AUDIT_DEPTH) deep-audits (triggered only on detection) | Audit records | Variable (only on detection) | 0-5% (amortized) |
| M5: CSS computation | O(N^2) pairwise tests (batched, every 10 epochs) | N * N * 32 bytes (deviation matrix) | None (batch, offline) | 3.0% |
| M5: Fusion classifier | O(N) predictions per update | Model parameters (~10 MB) | +10ms per prediction | 0.5% |
| **TOTAL (normal operations)** | | | | **16-20%** |
| **TOTAL (during enterprise audit)** | | | | **21-25%** |

**HG-3 verdict:** Normal operations cost is 16-20% of verification budget, which is AT the 20% threshold. Cost can be reduced to ~12% by:
1. Reducing COVER_TRAFFIC_DEPTH from 3 to 2 (saves ~3-4%)
2. Computing CSS every 20 epochs instead of 10 (saves ~1.5%)
3. Limiting M5 pairwise analysis to agents with >= 50 shared committees (reduces O(N^2) scope)

### 7.4 Performance Budget Allocation

Given a 20% operational cost budget:

| Mechanism | Allocated Budget | Priority | Justification |
|---|---|---|---|
| M1 (Anonymous Committees) | 10% | HIGHEST | Prevention is more cost-effective than detection |
| M2 (Sealed Opinions) | 1% | HIGH | Near-zero marginal cost |
| M3 (Honeypots) | 3% | HIGH | Direct detection with ground truth |
| M4 (CDP) | 1% (normal) / 5% (audit) | MEDIUM | Mostly dormant; activates on detection |
| M5 (Behavioral Analysis) | 5% | MEDIUM | Batch computation, tolerates delay |
| **Total** | **20%** | | |

---

## 8. HARD GATE VERIFICATION

### 8.1 HG-1: Honeypot Discrimination Test Design

**Objective:** Demonstrate that D-class and E-class honeypots cannot be distinguished from real claims by a SOTA discriminator at >60% accuracy.

**Test protocol:**

```
TEST HG1_Honeypot_Discriminator:

    // Dataset construction
    FOR class IN ["D", "E"]:
        real_claims = sample_real_claims(class, n=200)
        honeypot_claims = generate_honeypots(class, n=200)

        // Ensure metadata identity
        FOR h IN honeypot_claims:
            h.metadata = clone_metadata_from(random_choice(real_claims))
            h.submission_pipeline = PRODUCTION_PIPELINE  // Same pipeline as real

        dataset = shuffle(real_claims + honeypot_claims)
        labels = [0 if c.is_real else 1 for c in dataset]

        // Discriminator: SOTA LLM-based classifier
        // (Use the most capable available model, e.g., GPT-5, Claude-4)
        discriminator = LLMClassifier(
            prompt: "Determine if the following claim is synthetically
                     generated (honeypot) or authentic. Respond with
                     SYNTHETIC or AUTHENTIC and confidence 0-100.",
            model: SOTA_MODEL
        )

        // Also test: fine-tuned XGBoost on extracted features
        feature_discriminator = XGBoostClassifier()
        features = extract_discriminator_features(dataset)
        // Features: length, vocab entropy, citation count, structural
        //           regularity, knowledge graph connectivity

        // 5-fold cross-validation
        FOR fold IN 5_fold_cv(dataset):
            discriminator.evaluate(fold)
            feature_discriminator.fit_evaluate(fold)

        // Results
        llm_accuracy = discriminator.mean_accuracy()
        feature_accuracy = feature_discriminator.mean_accuracy()
        best_accuracy = max(llm_accuracy, feature_accuracy)

        ASSERT best_accuracy < 0.60,
            f"HG-1 FAILED for {class}: discriminator accuracy = {best_accuracy}"

        LOG(f"HG-1 PASSED for {class}: best accuracy = {best_accuracy}")
```

**Kill criteria:**
- D-class discriminator accuracy >= 0.60: KILL M3 for D-class. Fundamental redesign required.
- E-class discriminator accuracy >= 0.60: Demote E-class to Tier 2 (reduced injection rate).
- Both classes fail: M3 honeypot mechanism requires fundamental redesign. Fall back to random deep-audit only.

### 8.2 HG-2: ZK Reporting Protocol Sketch

**Protocol:** Linkable Ring Signature + Pedersen Commitment (detailed in Section 5.5)

**Verification requirements:**

| Property | Mechanism | Verification |
|---|---|---|
| Reporter anonymity | Ring signature hides signer among alleged ring members | Proven property of Fujisaki-Suzuki LRS |
| Reporter is ring member | Ring signature valid only if signer's key is in the ring | Verified by signature verification |
| No double-reporting | Linkability tag unique per ring per reporter | Checked against tag database |
| Evidence sufficiency | Behavioral predictions must be verifiable | Wait-and-check protocol |
| Bounty claim without identity leak | Pedersen commitment opened to isolated bounty channel | Channel isolation verified by architecture |

**Fallback if ZK is infeasible:** Reporter-pseudonymous reporting. Reporter uses a one-time DID (Decentralized Identifier) unlinked to their main identity. Identity protection is system-policy-based (the investigation subsystem does not share reporter identity with any party). This is weaker (relies on trust rather than cryptography) but simpler to implement.

### 8.3 HG-3: Cost Model

See Section 7.3 for the detailed cost model. Summary:

| Scenario | Total Cost (% of verification budget) | Within Budget? |
|---|---|---|
| Normal operations, full AVAP | 16-20% | YES (at boundary) |
| Normal operations, reduced cover traffic | 12-16% | YES |
| During enterprise audit | 21-25% | NO (temporary, amortized) |
| MV-AVAP (M1+M2+M3-D-only+M4c-only) | 8-10% | YES (comfortable) |

**Verdict:** HG-3 PASSES for normal operations. Enterprise audit overruns are acceptable because they are triggered only upon confirmed collusion detection (rare events, and the recovered slashed AIC offsets the audit cost).

### 8.4 HG-4: Classifier Performance Estimation

**Simulation design:**

```
SIMULATION HG4_Classifier_Performance:

    // Parameters
    total_agents = 1000
    ring_size = 20           // Medium ring (10-30 range)
    collusion_rate = 0.20    // Ring colludes on 20% of their committees
    honeypot_rate = 0.035    // 3.5% of claims are honeypots
    epochs = 25

    // Simulated population
    honest_agents = generate_agents(total_agents - ring_size, behavior="HONEST")
    ring_agents = generate_agents(ring_size, behavior="COLLUDING",
                                  collusion_rate=collusion_rate)

    // Run simulation
    FOR epoch IN 1..epochs:
        // Generate claims and committees
        claims = generate_claims(epoch, class_distribution=EMPIRICAL)
        committees = assign_committees(claims, honest_agents + ring_agents)

        // Simulate verification with honeypot injection
        FOR claim, committee IN zip(claims, committees):
            IF is_honeypot(claim):
                // Ring agents rubber-stamp with probability = collusion_rate
                evaluate_honeypot_responses(claim, committee, ring_agents)

            // Collect behavioral data for M5
            update_behavioral_statistics(committee)

        // Update Layer 2 statistics
        update_layer2_statistics(all_agents)

    // Extract features and evaluate classifier
    features = [extract_fusion_features(agent, epoch=25) for agent in all_agents]
    labels = [agent in ring_agents for agent in all_agents]

    // Train classifier on 70% of labeled data, test on 30%
    classifier = train_fusion_classifier(zip(features, labels))

    // Evaluate
    predictions = classifier.predict(test_features)
    recall = compute_recall(predictions, test_labels, threshold=0.50)
    fpr = compute_fpr(predictions, test_labels, threshold=0.50)

    // HG-4 gate
    ASSERT recall >= 0.70, f"HG-4 FAILED: recall = {recall}"
    ASSERT fpr < 0.10, f"HG-4 FAILED: FPR = {fpr}"

    LOG(f"HG-4 PASSED: recall = {recall}, FPR = {fpr}")
```

**Expected performance based on signal analysis:**

| Signal Source | Estimated AUC (alone) | Contribution to Fusion |
|---|---|---|
| M3 honeypot failure rate | 0.82 | PRIMARY (ground truth signal) |
| M5 CSS | 0.65 | SECONDARY (supporting signal) |
| Layer 2 pairwise agreement | 0.60 | SECONDARY |
| Layer 2 KL divergence | 0.58 | TERTIARY |
| M4 CDP reports | 0.55 (sparse) | TERTIARY |
| **Fusion (all signals)** | **0.88 (estimated)** | Combined discrimination |

At AUC 0.88, achieving 70% recall at <10% FPR is feasible (this corresponds to operating on the left side of the ROC curve where precision is high).

---

## 9. PARAMETERS AND CONFIGURATION

### 9.1 Complete Parameter Table

| Parameter | Default | Range | Constitutional? | Mechanism | Rationale |
|---|---|---|---|---|---|
| **M1 Parameters** | | | | | |
| MIN_COMMITTEE_SIZE | 7 | [5, 20] | YES (G-class) | M1 | BFT tolerance |
| DEFAULT_COMMITTEE_SIZE | 10 | [7, 15] | No | M1 | Balance security/cost |
| MIN_POOL_SIZE | 200 | [100, 1000] | YES (G-class) | M1 | Anonymity set size |
| MAX_COMMITTEE_TO_POOL_RATIO | 0.05 | [0.01, 0.10] | YES (G-class) | M1 | Selection probability cap |
| MAX_CLUSTER_CO_OCCURRENCE | 1 | [1, 3] | No | M1 | Sentinel cluster limit |
| COVER_TRAFFIC_DEPTH | 3 | [1, 5] | No | M1 | Cover traffic cost vs. protection |
| REKEY_INTERVAL | 100 epochs | [50, 500] | No | M1 | VRF re-keying frequency |
| **M2 Parameters** | | | | | |
| SUBMISSION_WINDOW | 6 hours | [2, 24] hours | No | M2 | Time for verification + commit |
| REVEAL_WINDOW | 2 hours | [1, 6] hours | No | M2 | Time for reveal after trigger |
| REVEAL_THRESHOLD | 0.70 | [0.50, 0.90] | No | M2 | Fraction of expected commits |
| MAX_WINDOW_EXTENSIONS | 1 | [0, 3] | No | M2 | Liveness vs. timeliness |
| REVEAL_MISMATCH_PENALTY | 50 AIC | [10, 200] | No | M2 | Deter commit-reveal gaming |
| **M3 Parameters** | | | | | |
| D_CLASS_INJECTION_RATE | 0.05 | [0.02, 0.10] | No | M3 | Honeypot frequency |
| E_CLASS_INJECTION_RATE | 0.05 | [0.02, 0.10] | No | M3 | |
| C_CLASS_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | M3 | |
| S_CLASS_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | M3 | |
| HONEYPOT_DISCRIMINATOR_THRESHOLD | 0.60 | [0.55, 0.65] | YES (G-class) | M3 | HG-1 gate |
| MAX_HONEYPOT_USES | 50 | [20, 100] | No | M3 | Retirement threshold |
| REAL_VARIANT_RATE | 0.10 | [0.05, 0.20] | No | M3 | Anti-fingerprinting |
| N_CANARY_VARIANTS | 3 | [2, 5] | No | M3 | Canary trap depth |
| HONEYPOT_PASS_THRESHOLD | 0.60 | [0.50, 0.80] | No | M3 | Belief threshold for "pass" |
| HONEYPOT_DETECT_THRESHOLD | 0.40 | [0.30, 0.60] | No | M3 | Disbelief threshold for "detect" |
| **M4 Parameters** | | | | | |
| UNCERTAINTY_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | M4a | Notification frequency |
| EARLY_DEFECTION_WINDOW | 10 epochs | [5, 20] | No | M4b | Early bounty window |
| MID_DEFECTION_WINDOW | 50 epochs | [25, 100] | No | M4b | Mid bounty window |
| EARLY_BOUNTY_RATE | 0.50 | [0.30, 0.70] | No | M4b | Early defection bounty |
| MID_BOUNTY_RATE | 0.35 | [0.20, 0.50] | No | M4b | |
| LATE_BOUNTY_RATE | 0.25 | [0.10, 0.40] | No | M4b | |
| MAX_BOUNTY_CAP | 0.60 | [0.40, 0.80] | YES (G-class) | M4b | Maximum bounty fraction |
| AUDIT_LOOKBACK_EPOCHS | 500 | [100, 1000] | No | M4c | Enterprise audit scope |
| ENTERPRISE_AUDIT_DEPTH | 100 | [50, 500] | No | M4c | Max claims per audit |
| CASCADE_ATTENUATION | 0.50 | [0.30, 0.70] | No | M4c | Credibility cascade decay |
| ENTERPRISE_CREDIBILITY_PENALTY | 0.15 | [0.05, 0.30] | No | M4c | Per-confirmed-collusion penalty |
| **M5 Parameters** | | | | | |
| MIN_SHARED_COMMITTEES | 30 | [15, 50] | No | M5 | Statistical power threshold |
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

### 9.2 Constitutionally Protected Parameters

The following parameters require G-class governance change (75% supermajority, 72-hour discussion for HIGH safety class):

1. **MIN_COMMITTEE_SIZE** -- Directly affects BFT tolerance
2. **MIN_POOL_SIZE** -- Directly affects anonymity guarantee
3. **MAX_COMMITTEE_TO_POOL_RATIO** -- Directly affects selection probability
4. **HONEYPOT_DISCRIMINATOR_THRESHOLD** -- Controls HG-1 gate (system integrity)
5. **MAX_BOUNTY_CAP** -- Limits economic exposure of the bounty system
6. **SLASHING_RECOMMENDATION_THRESHOLD** -- Determines when agents can lose stake
7. **ENTERPRISE_LIABILITY_THRESHOLD** -- Determines when retroactive audits are triggered

Rationale: These parameters control the fundamental security guarantees and economic properties of AVAP. Changing them casually could either (a) weaken collusion defense, or (b) create excessive false positive risk for honest agents. Both outcomes are serious enough to warrant governance-level deliberation.

---

## 10. PSEUDOCODE FOR CRITICAL ALGORITHMS

### 10.1 Full Committee Assignment Flow

```
FUNCTION avap_full_committee_assignment(
    claim: Claim,
    epoch: uint64,
    agent_pool: Set<Agent>
) -> Committee:

    // Step 1: Filter eligible agents (diversity constraints, Sentinel exclusion)
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
        // Insufficient candidates after filtering; retry with relaxed threshold
        RETURN retry_with_relaxed_threshold(claim, epoch, eligible)

    // Step 5: Assign committee slots
    committee = Committee{
        claim_hash: claim.hash,
        epoch: epoch,
        members: [(agent.id, token) for agent, token in selected],
        size: len(selected),
        status: "FORMED"
    }

    // Step 6: Dispatch verification tasks (encrypted)
    FOR agent, token IN selected:
        dispatch_encrypted_task(agent, claim, token)

    // Step 7: Dispatch cover traffic to non-selected agents
    non_selected = eligible - {a for a, _ in selected}
    FOR agent IN non_selected:
        dispatch_cover_traffic(agent, claim)

    RETURN committee
```

### 10.2 Full Commit-Reveal Flow

```
FUNCTION avap_commit_reveal(
    claim: Claim,
    committee: Committee,
    epoch: uint64
) -> List<RevealedOpinion>:

    // COMMIT PHASE
    commitments = {}
    deadline = epoch_start(epoch) + SUBMISSION_WINDOW

    WHILE now() < deadline:
        FOR commitment IN receive_commitments(claim.hash):
            // Validate: correct format, valid signature, within window
            IF validate_commitment(commitment):
                commitments[commitment.encrypted_agent_id] = commitment

    // Check reveal trigger
    IF len(commitments) < REVEAL_THRESHOLD * committee.size:
        // Extension
        IF extensions_used < MAX_WINDOW_EXTENSIONS:
            extend_window(claim, 2 * 3600)  // 2 hours
            extensions_used += 1
            // Wait for more commitments...
        ELSE:
            // Proceed with available commitments

    // REVEAL PHASE
    reveal_deadline = now() + REVEAL_WINDOW
    reveals = {}

    // Broadcast reveal trigger to all committed agents
    broadcast_reveal_trigger(claim.hash, commitments.keys())

    WHILE now() < reveal_deadline:
        FOR reveal IN receive_reveals(claim.hash):
            // Verify: commitment matches, VRF proof valid
            IF validate_reveal(reveal, commitments):
                reveals[reveal.agent_id] = reveal

    // Handle non-revealers
    committed_agents = decrypt_agent_ids(commitments)
    FOR agent_id IN committed_agents:
        IF agent_id NOT IN reveals:
            // Apply non-reveal penalty
            apply_non_reveal_penalty(agent_id, claim.hash, epoch)
            // Substitute with default opinion
            reveals[agent_id] = RevealedOpinion{
                agent_id: agent_id,
                opinion: OpinionTuple(b=0, d=0, u=1, a=claim.base_rate),
                is_default: true
            }

    // Filter: only VRF-proven committee members (not cover traffic)
    committee_opinions = [
        r for r in reveals.values()
        if verify_vrf_membership(r.agent_id, claim, epoch)
    ]

    RETURN committee_opinions
```

### 10.3 Honeypot Injection Decision

```
FUNCTION should_inject_honeypot(
    claim: Claim,
    epoch: uint64
) -> (bool, HoneypotClaim?):

    // Step 1: Check claim class eligibility
    class = claim.assigned_class
    IF class IN ["H", "N", "K"]:
        RETURN (false, null)  // Tier 3: no honeypots

    // Step 2: VRF-based injection decision (deterministic but unpredictable)
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
        RETURN (false, null)  // Not selected for injection

    // Step 3: Select a honeypot from the vault
    honeypot = honeypot_vault.select(
        class: class,
        difficulty: select_difficulty(injection_seed),
        max_uses_remaining: MAX_HONEYPOT_USES
    )

    IF honeypot IS null:
        LOG("WARNING: No available honeypots for class", class)
        RETURN (false, null)

    // Step 4: Select canary variant for each committee member
    // (different committee members see different variants)
    // This is done at dispatch time, not here

    // Step 5: Metadata cloning
    // Copy metadata from the real claim being replaced
    honeypot.clone_metadata_from(claim)

    RETURN (true, honeypot)
```

### 10.4 CDP Reporting Flow

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
            reason: "A report from this ring member already exists"
        }

    // Step 3: Construct Pedersen commitment to reporter identity
    blinding = random_scalar()
    membership_commitment = pedersen_commit(reporter.agent_id, blinding)

    // Step 4: Submit ZK report
    zk_report = ZKCDPReport{
        evidence:               evidence,
        membership_commitment:  membership_commitment,
        ring_signature:         ring_sig,
        alleged_ring:           alleged_ring,
        submission_epoch:       current_epoch()
    }

    // Step 5: System verification
    IF NOT verify_ring_signature(ring_sig, ring_pubkeys, message):
        RETURN CDPSubmissionResult{status: "INVALID_SIGNATURE"}

    // Step 6: Evaluate evidence quality
    evidence_score = evaluate_cdp_evidence(evidence)
    IF evidence_score < MIN_EVIDENCE_QUALITY:
        RETURN CDPSubmissionResult{
            status: "INSUFFICIENT_EVIDENCE",
            score: evidence_score
        }

    // Step 7: Escrow bounty
    estimated_bounty = estimate_bounty(alleged_ring)
    escrow_tx = dsf.submit_operation(
        op_type: "PENDING_INITIATE",
        amount: estimated_bounty,
        source: "COLLUSION_DEFENSE_TREASURY",
        escrow_id: SHA256(zk_report.ring_signature.link_tag)
    )

    // Step 8: Begin investigation
    investigation = begin_cdp_investigation(zk_report)

    RETURN CDPSubmissionResult{
        status: "ACCEPTED",
        investigation_id: investigation.id,
        estimated_bounty: estimated_bounty,
        escrow_tx: escrow_tx.tx_id
    }
```

### 10.5 Conditional Behavioral Analysis Update

```
FUNCTION update_behavioral_statistics(
    committee: Committee,
    claim: Claim,
    revealed_opinions: List<RevealedOpinion>,
    epoch: uint64
):

    // Compute committee majority opinion
    majority_opinion = compute_majority_opinion(revealed_opinions)

    // Update pairwise presence/absence records for each member
    FOR member_opinion IN revealed_opinions:
        agent_a = member_opinion.agent_id

        // Record this agent's opinion distance from majority
        distance = opinion_distance(member_opinion.opinion, majority_opinion)

        FOR other_opinion IN revealed_opinions:
            agent_b = other_opinion.agent_id
            IF agent_a == agent_b:
                CONTINUE

            // Record: agent_a's behavior when agent_b was present
            behavioral_store.record(
                agent_a:    agent_a,
                agent_b:    agent_b,
                claim_hash: claim.hash,
                claim_class: claim.assigned_class,
                epoch:      epoch,
                b_present:  true,
                opinion_distance: distance,
                opinion_tuple: member_opinion.opinion
            )

        // Also record for all agents NOT on this committee
        // (needed for the "b_absent" partition)
        non_members = get_agents_sharing_pool(agent_a) - set(committee.member_ids())
        // NOTE: We only need to record absence for agents that have
        // previously been present on committees with agent_a
        // (otherwise we'd need N^2 absent records per claim)
        tracked_partners = behavioral_store.get_tracked_partners(agent_a)
        FOR agent_b IN tracked_partners:
            IF agent_b NOT IN committee.member_ids():
                behavioral_store.record(
                    agent_a:    agent_a,
                    agent_b:    agent_b,
                    claim_hash: claim.hash,
                    claim_class: claim.assigned_class,
                    epoch:      epoch,
                    b_present:  false,
                    opinion_distance: distance,
                    opinion_tuple: member_opinion.opinion
                )
```

### 10.6 Multi-Signal Fusion Pipeline

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
            honeypot_failure_rate = honeypot_store.failure_rate(agent, lookback=100),
            honeypot_failure_count = honeypot_store.failure_count(agent, lookback=100),
            honeypot_severity_score = honeypot_store.severity_score(agent, lookback=100),

            // M5 signals
            css = css_store.get(agent, epoch),
            max_pairwise_deviation = css_store.max_deviation(agent, epoch),
            significant_pairs_count = css_store.significant_pairs(agent, epoch),

            // Layer 2 signals
            pairwise_agreement_anomaly = layer2.agreement_z_score(agent, epoch),
            kl_divergence_from_baseline = layer2.kl_divergence(agent, epoch),
            opinion_copying_index = layer2.oci(agent, epoch),

            // M4 signals
            cdp_reports_involving = cdp_store.reports_involving(agent),
            cdp_reports_verified = cdp_store.verified_reports_involving(agent),

            // Metadata
            agent_age_epochs = get_agent_age(agent, epoch),
            total_committees_served = get_committee_count(agent),
            claim_class_concentration = get_class_concentration(agent),
            sentinel_cluster_size = sentinel_graph.cluster_size(agent)
        }

        // Predict
        p_collusion = classifier.predict_proba(features.as_vector())

        // Determine response
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

    // Update Sentinel Graph with any new behavioral correlations
    suspicious = [(a, r.p_collusion) for a, r in responses.items()
                  if r.level != "NORMAL"]
    update_sentinel_from_avap(suspicious, epoch)

    RETURN responses
```

---

## 11. FAILURE MODE CATALOGUE

### 11.1 Mechanism-Level Failures

| ID | Failure Mode | Mechanism | Severity | Detection | Recovery |
|---|---|---|---|---|---|
| F1 | VRF seed compromise | M1 | CRITICAL | Randomness testing (NIST SP 800-22) | Emergency VRF re-keying; epoch invalidation |
| F2 | Cover traffic distinguishable | M1 | HIGH | Periodic side-channel audit | Increase COVER_TRAFFIC_DEPTH; add jitter |
| F3 | Commitment coordinator unavailable | M2 | HIGH | Health monitoring | Fall back to on-chain commitment submission |
| F4 | Mass non-reveal (>50% of committee) | M2 | MEDIUM | Threshold monitoring | Extend window; reassign to fresh committee |
| F5 | Honeypot corpus exhausted | M3 | MEDIUM | Vault inventory monitoring | Emergency generation; reduce injection rate |
| F6 | Honeypot discrimination breakthrough | M3 | CRITICAL | Quarterly HG-1 test | Regenerate corpus; redesign generators |
| F7 | CDP false report flood | M4 | MEDIUM | Rate limiting; evidence quality scoring | Increase MIN_EVIDENCE_QUALITY; IP-based rate limit |
| F8 | Ring signature library vulnerability | M4 (ZK) | HIGH | Dependency monitoring; audit | Fall back to pseudonymous reporting |
| F9 | CSS computation overload | M5 | LOW | Compute monitoring | Increase CSS_UPDATE_FREQUENCY; reduce pairwise scope |
| F10 | Fusion classifier model drift | Fusion | MEDIUM | Periodic AUC evaluation on holdout | Retrain; increase CLASSIFIER_RETRAIN_INTERVAL |

### 11.2 Cross-Mechanism Failures

| ID | Failure Mode | Mechanisms | Severity | Detection | Recovery |
|---|---|---|---|---|---|
| X1 | M1 anonymity leak feeds M4 deanonymization | M1 + M4 | HIGH | CDP investigation audit | Isolate investigation subsystem; review access controls |
| X2 | M3 honeypot results create biased M5 training data | M3 + M5 | MEDIUM | Calibration drift detection | Separate M5 training data from M3 evaluation data |
| X3 | Enterprise liability audit overwhelms system resources | M4c + all | HIGH | Resource monitoring | Cap concurrent audits; prioritize by risk score |
| X4 | Fusion classifier overfit to historical ring patterns | Fusion | MEDIUM | Cross-validation monitoring | Retrain with synthetic adversarial examples |

---

## 12. MINIMUM VIABLE AVAP (MV-AVAP)

If hard gates fail or operational costs exceed budget, the following minimum viable subset provides meaningful anti-collusion improvement over C10 alone:

### MV-AVAP Configuration

| Mechanism | MV-AVAP Scope | Cost (% of verification budget) |
|---|---|---|
| M1: Anonymous Committees | FULL (including cover traffic at DEPTH=2) | 7% |
| M2: Sealed Opinions | FULL | 1% |
| M3: Honeypots | D-class ONLY (automated, no expert time) | 1% |
| M4: CDP | Enterprise liability ONLY (no bounty, no ZK, no info injection) | 0.5% (normal) |
| M5: Behavioral Analysis | CSS only, NO fusion classifier (CSS feeds directly into Layer 2) | 2% |
| **Total** | | **~11.5%** |

### MV-AVAP Justification

Even this minimal configuration provides:

1. **Structural prevention** (M1+M2): Colluders cannot identify allies or signal during verification. This alone forces all collusion to be pre-coordinated, which is a significant constraint.

2. **Ground-truth detection** (M3 D-class): D-class honeypots are the highest-confidence, lowest-cost honeypots. They catch any agent that rubber-stamps proofs without checking.

3. **Economic deterrence** (M4c enterprise liability): Any detected collusion triggers retroactive audit. Even without bounties, this creates super-linear expected cost for long-lived rings.

4. **Screening signal** (M5 CSS): Feeds into existing Layer 2 infrastructure with zero new detection thresholds.

MV-AVAP is the fallback if HG-1 fails for E-class, HG-2 is infeasible, or HG-3 shows full AVAP exceeds budget.

---

## APPENDIX A: GLOSSARY

| Term | Definition |
|---|---|
| AIC | Atrahasis Internal Credit -- the system's unit of account |
| AVAP | Anonymous Verification with Adaptive Probing -- this system |
| BFT | Byzantine Fault Tolerance |
| CACT | Commit-Attest-Challenge-Triangulate (C11 VTD forgery defense) |
| CDP | Collusion Deterrence Payment |
| CSS | Collusion Suspicion Score (M5 output) |
| DSF | Deterministic Settlement Fabric (C8) |
| ECVRF | Elliptic Curve Verifiable Random Function (RFC 9381) |
| FDR | False Discovery Rate (Benjamini-Hochberg correction) |
| FPR | False Positive Rate |
| HITL | Human In The Loop |
| LRS | Linkable Ring Signature |
| MCT | Membrane Certification Token |
| MV-AVAP | Minimum Viable AVAP (fallback configuration) |
| OCI | Opinion Copying Index (Layer 2 metric) |
| PCVM | Proof-Carrying Verification Membrane (C5) |
| VRF | Verifiable Random Function |
| VTD | Verification Trace Document |

## APPENDIX B: CROSS-REFERENCES

| Section | References |
|---|---|
| M1 (Anonymous Committees) | C3 Technical Spec Section 5 (VRF Dual Defense), C10 Layer 1 (Sentinel Graph), C10 Layer 3 (Diversity Constraints) |
| M2 (Sealed Opinions) | C5 Section 6 (Verification Protocol), C8 Section 2 (HDL, for Merkle anchoring) |
| M3 (Honeypots) | C5 Section 4 (VTD Engine, for claim format), C5 Section 8 (Credibility Engine, for opinion thresholds), C10 Layer 4 (Adaptive Audit) |
| M4 (CDP) | C8 Section 10.3 (Graduated Slashing), C8 Section 2.3 (EABS for settlement), RFC 9381 (ECVRF for ring signatures) |
| M5 (Behavioral Analysis) | C10 Layer 2 (Statistical Detection), C3 Sentinel Graph (cluster updates), C5 Section 8 (Subjective Logic) |
| Fusion Classifier | C10 Layers 1-4 (all signals), C8 (slashing settlement), Sentinel Graph (cluster updates) |

---

*End of C12 DESIGN Document*
*AVAP v1.0 (DESIGN stage complete)*
*Next stage: SPECIFICATION (Master Tech Spec)*
