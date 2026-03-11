# C13 DESIGN: Consolidation Robustness Protocol v2.0 (CRP+)

**Invention:** C13 — Consolidation Poisoning Defense
**Stage:** DESIGN
**Date:** 2026-03-10
**Status:** COMPLETE
**Input Documents:** C13_IDEATION.md, C13_RESEARCH_REPORT.md, C13_FEASIBILITY.md
**Normative References:** C3 (Tidal Noosphere v1.0), C5 (PCVM v1.0), C6 (EMA v1.0), C8 (DSF v2.0), C10 (Hardening Addenda), C11 (CACT v1.0), C12 (AVAP v1.0), RFC 9381 (ECVRF)
**Assessment Scores:** Novelty 3.5/5, Feasibility 4/5, Impact 4/5, Risk 6/10

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [M1: Adaptive Perturbation Robustness Testing (APRT)](#2-m1-adaptive-perturbation-robustness-testing-aprt)
3. [M2: Calibrated Organic Dissent Search (CODS)](#3-m2-calibrated-organic-dissent-search-cods)
4. [M3: Source Purpose Scoring (Supplementary)](#4-m3-source-purpose-scoring-supplementary)
5. [M4: VRF Consolidation Selection](#5-m4-vrf-consolidation-selection)
6. [M5: Graduated Credibility Ladder](#6-m5-graduated-credibility-ladder)
7. [M6: Consolidation Depth Limits](#7-m6-consolidation-depth-limits)
8. [M7: Immune Memory](#8-m7-immune-memory)
9. [Novelty Pathway](#9-novelty-pathway)
10. [Cross-Mechanism Integration](#10-cross-mechanism-integration)
11. [Parameters and Configuration](#11-parameters-and-configuration)
12. [Pseudocode: All Critical Algorithms](#12-pseudocode-all-critical-algorithms)
13. [Failure Mode Catalogue](#13-failure-mode-catalogue)

---

## 1. System Architecture Overview

### 1.1 Position in the Atrahasis Stack

CRP+ is a **consolidation-defense layer** that wraps the EMA dreaming pipeline (C6 Section 5.3). It is not a new top-level component; it instruments the existing consolidation process at five insertion points within the dreaming lifecycle.

```
CIOS (orchestration)
    |
    v
Tidal Noosphere (C3) -- provides VRF seeds, parcel topology, epoch clock
    |
    v
PCVM (C5) / CACT (C11) / AVAP (C12) -- verification, forgery defense, collusion defense
    |
    v
EMA (C6) -- knowledge metabolism
    |
    +-- Ingestion Phase .............. [no CRP+ involvement]
    +-- Circulation Phase ............ [no CRP+ involvement]
    +-- Consolidation Phase .......... [*** CRP+ WRAPS THIS ENTIRE PHASE ***]
    |   |
    |   +-- (1) Candidate Identification ... [M4 VRF Selection REPLACES deterministic selection]
    |   +-- (2) Provenance Diversity ....... [C10 Layer 1: unchanged, prerequisite to CRP+]
    |   +-- (3) Source Independence ........ [C10 Layer 1: unchanged, prerequisite to CRP+]
    |   +-- (4) Consolidation Lock ......... [C6 base: unchanged]
    |   +-- (5) Three-Pass LLM Synthesis ... [C6 base: unchanged]
    |   +-- (6) ** M1 APRT ** ............. [NEW: post-synthesis robustness testing]
    |   +-- (7) ** M2 CODS ** ............. [NEW: calibrated dissent search]
    |   +-- (8) C10 Adversarial Probing .... [EXTENDED: CRP+ adds M3 tie-breaker]
    |   +-- (9) ** M7 Immune Memory ** ..... [NEW: check against rejected signatures]
    |   +-- (10) ** Combined Scoring ** ..... [NEW: accept/reject/quarantine decision]
    |   +-- (11) PCVM Verification Gate .... [C6 base: unchanged]
    |   +-- (12) ** M5 Credibility Ladder ** [NEW: post-acceptance rung assignment]
    |   +-- (13) ** M6 Depth Limits ** ..... [NEW: enforce participation constraints]
    |   +-- (14) Rate Limiting ............. [C10 Layer 4: unchanged]
    |   +-- (15) Empirical Validation Queue  [C10 Layer 5: EXTENDED by M5]
    |
    +-- Catabolism Phase ............. [M5 demotion checks piggyback here]
    +-- Regulation Phase ............. [M7 memory decay piggyback here]
```

### 1.2 Data Flow: Single Consolidation Candidate

```
identify_candidates(shard, epoch)
         |
         v
    M4: VRF Selection ─── filter candidates by VRF output
         |                 (unpredictable subset selected)
         v
    C10 Layer 1: Provenance Diversity + Source Independence
         |
         v  [REJECT if diversity/independence fails]
    C6: Consolidation Lock Acquisition
         |
         v
    C6: Three-Pass LLM Synthesis
         |  produces candidate claim C from quanta {q1..qN}
         v
    M7: Immune Memory Check ─── does C match a rejected signature?
         |                       YES → enhanced scrutiny path
         |                       NO  → standard path
         v
    M1 APRT: Perturbation Robustness Testing
         |  Tier 1: embedding-based influence screening
         |  Tier 2: targeted re-synthesis (Cases A/B/C)
         |  Output: robustness_score ∈ [0, 1]
         v
    M2 CODS: Novelty Classification → Dissent Search → Dissent Deficit
         |  Output: cods_score ∈ [0, 1], novelty_tier ∈ {N1, N2, N3}
         |
         ├── IF novelty_tier == N3 → BRANCH to Novelty Pathway (Section 9)
         v
    C10 Layer 2: Adversarial Consolidation Probing
         |  Output: probe_relative_strength ∈ [0, 1]
         v
    M3: Source Purpose Scoring (CONDITIONAL)
         |  Invoked ONLY if combined signals are ambiguous
         |  Output: purpose_score ∈ [0, 1] (max weight 0.15)
         v
    Combined CRP+ Scoring → ACCEPT / REJECT / QUARANTINE
         |
         v  [REJECT → store signature in M7 immune memory]
         v  [QUARANTINE → hold for manual review]
    PCVM Verification Gate (C6 Section 5.3.5)
         |
         v
    M5: Assign Credibility Rung (PROVISIONAL)
         |
         v
    M6: Apply Depth Limits (constrain future participation)
         |
         v
    C10 Layer 4: Rate Limiting
         |
         v
    C10 Layer 5 / M5: Empirical Validation Queue
         |
         v
    ACCEPTED QUANTUM (K-class, PROVISIONAL rung, depth-constrained)
```

### 1.3 Relationship to Existing C10 5-Layer Defense

CRP+ **extends** the existing C10 consolidation defense. It does not replace any layer.

| C10 Layer | Status Under CRP+ | How CRP+ Extends It |
|---|---|---|
| Layer 1: Source Independence (I1/I2/I3) | UNCHANGED | Prerequisite to CRP+. CRP+ mechanisms execute only after Layer 1 passes. |
| Layer 2: Adversarial Consolidation Probing | EXTENDED | CRP+ adds M3 tie-breaking when probe results are ambiguous. CODS dissent search provides additional signal to the probe. |
| Layer 3: Consolidation Lineage Tracking | EXTENDED | M5 Credibility Ladder adds rung-based credibility weighting on top of lineage-based cascade. M6 Depth Limits add participation constraints. |
| Layer 4: Consolidation Rate Limiting | UNCHANGED | CRP+ operates within rate limits. M4 VRF selection reduces candidate count before rate limits apply. |
| Layer 5: Empirical Validation Queue | EXTENDED | M5 replaces the flat uncertainty floor with a 4-rung graduated system. Promotion criteria are more granular than the original PENDING_VALIDATION/VALIDATED binary. |

### 1.4 Invariants

- **INV-CRP1 (VRF Unpredictability):** No agent can predict which consolidation candidates will be selected in epoch E+2 during epoch E. Guaranteed by ECVRF one-epoch-ahead unpredictability (C3 Section 5.2.1).
- **INV-CRP2 (APRT Completeness):** Every consolidation candidate that passes synthesis MUST undergo at least Tier 1 APRT screening. No exceptions.
- **INV-CRP3 (CODS Calibration):** Dissent deficit weight MUST be calibrated by novelty tier. N3 claims MUST NOT be penalized for dissent deficit.
- **INV-CRP4 (Credibility Monotonicity):** A quantum's credibility rung can only increase through explicit promotion criteria or decrease through explicit demotion criteria. No mechanism may set a rung directly without satisfying the criteria for that rung.
- **INV-CRP5 (Depth Enforcement):** PROVISIONAL K-class quanta MUST NOT participate in further consolidation. This is enforced at candidate identification time.
- **INV-CRP6 (Immune Memory Bounded):** Total immune memory signatures per shard MUST NOT exceed MAX_IMMUNE_SIGNATURES (1000). Garbage collection MUST run every epoch.
- **INV-CRP7 (Novelty Pathway Isolation):** N3 claims on the Novelty Pathway MUST NOT bypass APRT. They receive enhanced (full leave-one-out) APRT, not reduced APRT.
- **INV-CRP8 (M3 Cap):** Source Purpose Scoring MUST NOT contribute more than 0.15 to the combined CRP+ score under any circumstance.

---

## 2. M1: Adaptive Perturbation Robustness Testing (APRT)

### 2.1 Purpose

APRT answers the question: "Would this consolidation conclusion still be reached if the input quanta were different?" A robust consolidation is one where the conclusion is overdetermined by the evidence -- removing any single quantum, or any suspicious cluster, does not change the result. A fragile consolidation depends on specific quanta, which may be adversarially planted.

### 2.2 Integration Point

APRT executes immediately after Three-Pass LLM Synthesis (C6 Section 5.3.4) and before Adversarial Consolidation Probing (C10 Section 3.2). It receives:
- The candidate consolidation claim `C` (text)
- The contributing quanta set `Q = {q1, q2, ..., qN}`
- The synthesis context (prompt templates, temperature, etc.)

It produces:
- `robustness_score` ∈ [0.0, 1.0]
- `aprt_case` ∈ {A, B, C}
- `flagged_quanta` (list of quantum IDs with anomalous influence)
- `flagged_clusters` (list of quantum ID sets forming suspicious clusters)
- `resynthesis_count` (number of Tier 2 re-syntheses performed)

### 2.3 Tier 1: Embedding Influence Gradient Screening

#### 2.3.1 Embedding Computation

Each quantum `qi` and the consolidation claim `C` are embedded into a shared vector space using the system's embedding model (same model used for coherence graph similarity computations in C6).

```
emb(qi) = embed(qi.content.claim_text)    for each qi ∈ Q
emb(C)  = embed(C.text)
```

#### 2.3.2 Influence Score Computation

For each quantum `qi`, compute two sub-scores:

**Relevance:** Cosine similarity between `qi` and the consolidation conclusion `C`.

```
relevance(qi) = cosine_similarity(emb(qi), emb(C))
```

**Uniqueness:** How much unique information does `qi` provide relative to other quanta in Q?

```
redundancy(qi) = max_{j ≠ i} cosine_similarity(emb(qi), emb(qj))
uniqueness(qi) = 1.0 - redundancy(qi)
```

**Composite Influence:**

```
influence(qi) = relevance(qi) × uniqueness(qi)
```

A quantum with high influence is both highly relevant to the conclusion AND provides information no other quantum provides. This is the signature of a load-bearing quantum.

#### 2.3.3 Anomaly Detection

Compute the mean and standard deviation of influence scores across Q:

```
μ_inf = mean(influence(qi) for qi in Q)
σ_inf = std(influence(qi) for qi in Q)
```

**High-Influence Flag:** Any quantum with `influence(qi) > μ_inf + 2σ_inf` is flagged.

**Redundant Cluster Detection:** Group quanta by pairwise cosine similarity. Two quanta are in the same cluster if `cosine_similarity(emb(qi), emb(qj)) > 0.85`. A cluster of 3+ quanta that are all relevant to C (`relevance > 0.5`) is flagged as a suspicious redundant cluster.

#### 2.3.4 Case Classification

Based on Tier 1 results, classify into one of three cases:

| Case | Condition | Interpretation |
|------|-----------|----------------|
| **A** | ≥1 quantum flagged as high-influence | Specific quanta are load-bearing; test their removal |
| **B** | No high-influence flags BUT ≥1 redundant cluster detected | Redundant poisoning pattern; test cluster removal |
| **C** | No flags, no clusters; influence is uniformly distributed | Organic pattern; single random-subset check suffices |

### 2.4 Tier 2: Targeted Re-Synthesis

#### 2.4.1 Case A: High-Influence Quantum Testing

For each flagged quantum `qi_flagged`:

1. Construct reduced set `Q' = Q \ {qi_flagged}`
2. Re-run Three-Pass LLM Synthesis on `Q'` with identical parameters
3. Compare re-synthesized claim `C'` with original claim `C`:
   - `stability(qi_flagged) = semantic_similarity(C, C')`
   - If `stability < STABILITY_THRESHOLD` (0.70): the conclusion depends on this quantum

**Robustness score (Case A):**

```
robustness_A = min(stability(qi_flagged) for qi_flagged in flagged_quanta)
```

If ANY flagged quantum's removal changes the conclusion (stability < 0.70), the consolidation is fragile. Cost: 1-3 re-syntheses (one per flagged quantum, max 3 flags expected).

#### 2.4.2 Case B: Redundant Cluster Testing

For each flagged cluster `Ck`:

1. Construct reduced set `Q' = Q \ Ck` (remove entire cluster)
2. Re-run Three-Pass LLM Synthesis on `Q'`
3. Compare: `stability(Ck) = semantic_similarity(C, C')`

**Robustness score (Case B):**

```
robustness_B = min(stability(Ck) for Ck in flagged_clusters)
```

If removing a redundant cluster collapses the conclusion, the cluster was the load-bearing set -- the adversary's planted quanta. Cost: 1-2 re-syntheses (one per cluster, rarely more than 2 clusters).

#### 2.4.3 Case C: Random Subset Sanity Check

1. Randomly remove 30% of quanta (VRF-selected subset for reproducibility)
2. Re-run synthesis on the remaining 70%
3. Compare: `stability_random = semantic_similarity(C, C')`

**Robustness score (Case C):**

```
robustness_C = stability_random
```

Cost: 1 re-synthesis.

#### 2.4.4 Semantic Similarity for Stability Comparison

The stability comparison uses embedding cosine similarity between the original claim C and the re-synthesized claim C'. This is the same embedding model used in Tier 1.

```
semantic_similarity(C, C') = cosine_similarity(embed(C.text), embed(C'.text))
```

Threshold interpretation:
- `≥ 0.90`: Conclusion essentially unchanged (robust)
- `0.70 - 0.89`: Conclusion modified but structurally similar (moderate)
- `< 0.70`: Conclusion substantially changed (fragile)

### 2.5 Robustness Score Summary

The final APRT robustness score is whichever case applies:

```
robustness_score = robustness_A  if case == A
                 = robustness_B  if case == B
                 = robustness_C  if case == C
```

Interpretation:
- `≥ 0.85`: HIGH robustness. Consolidation is overdetermined.
- `0.60 - 0.84`: MODERATE robustness. Proceed with caution.
- `< 0.60`: LOW robustness. Consolidation is fragile; likely poisoned or artifactual.

### 2.6 APRT Enhanced Mode (Immune Memory Match or Novelty Pathway)

When triggered by M7 immune memory match or N3 Novelty Pathway entry:

- Skip Tier 1 case classification
- Run full leave-one-out on ALL quanta (not just flagged ones)
- Robustness score = minimum stability across all leave-one-out tests

```
robustness_enhanced = min(stability(qi) for qi in Q)
```

Cost: N re-syntheses. Justified only for the ~10% of candidates that trigger enhanced mode.

---

## 3. M2: Calibrated Organic Dissent Search (CODS)

### 3.1 Purpose

CODS answers: "Is the absence of counter-evidence suspicious?" For incremental claims in well-mapped domains, zero counter-evidence is a red flag (genuine patterns always have dissenters). For paradigmatic novelty, zero counter-evidence is expected. CODS calibrates the dissent signal by novelty tier.

### 3.2 Integration Point

CODS executes after APRT and before Adversarial Consolidation Probing. It receives:
- The candidate consolidation claim `C`
- The contributing quanta `Q`
- The coherence graph context (existing cross-domain edges, domain metadata)
- The shard's knowledge base for dissent search

It produces:
- `novelty_tier` ∈ {N1, N2, N3}
- `dissent_items` (list of contradicting/alternative quanta found)
- `dissent_deficit` ∈ [0.0, 1.0] (0 = abundant dissent, 1 = no dissent found)
- `cods_score` ∈ [0.0, 1.0] (calibrated score; higher = more suspicious)

### 3.3 Step 1: Novelty Tier Classification

#### 3.3.1 Feature Extraction

Extract three features from the consolidation candidate:

**F1: Domain Overlap with Existing Cross-Domain Edges**

Identify the domains bridged by the consolidation. Query the coherence graph for existing ANALOGY edges between those domains.

```
domains_bridged = extract_domains(Q)  # typically 2-3 domains
existing_bridges = count_analogy_edges(domain_a, domain_b, coherence_graph)
domain_overlap = existing_bridges / max(1, expected_bridges(domain_a, domain_b))
```

Where `expected_bridges` is estimated from domain sizes: `sqrt(|domain_a| * |domain_b|) * BRIDGE_DENSITY_FACTOR` (default 0.01).

**F2: Semantic Distance from Nearest Existing Consolidation**

```
nearest_consolidation = argmin_{K in active_K_class}
    cosine_distance(embed(C.text), embed(K.content.claim_text))
semantic_distance = cosine_distance(embed(C.text), embed(nearest_consolidation.content.claim_text))
```

**F3: Precedent Count**

```
precedent_count = count_prior_consolidation_attempts(domain_a, domain_b, lookback_epochs=500)
```

#### 3.3.2 Tier Classification Rules

| Tier | Condition | Interpretation |
|------|-----------|----------------|
| **N1 (Incremental)** | `domain_overlap ≥ 0.3` OR `precedent_count ≥ 3` OR `semantic_distance < 0.4` | Extends known cross-domain connections |
| **N2 (Bridging)** | `0.05 ≤ domain_overlap < 0.3` OR `1 ≤ precedent_count < 3` OR `0.4 ≤ semantic_distance < 0.7` | Connects domains with some documented proximity |
| **N3 (Paradigmatic)** | `domain_overlap < 0.05` AND `precedent_count == 0` AND `semantic_distance ≥ 0.7` | Genuinely novel -- no prior relationship documented |

When features span multiple tiers, the MOST NOVEL tier among the three features determines the classification. This errs on the side of protecting genuine novelty.

### 3.4 Step 2: Dissent Search

#### 3.4.1 Query Generation

Generate dissent search queries from the consolidation claim:

```
queries = [
    negate(C.text),                           # Direct negation
    "alternative explanation for " + C.text,  # Alternative hypothesis
    "counter-evidence against " + C.text,     # Counter-evidence
    "limitation of " + extract_mechanism(C),  # Mechanism limitations
]
```

Each query is embedded and used to search the knowledge base (active quanta across all shards accessible to this shard) for semantically similar quanta with contradictory or alternative content.

#### 3.4.2 Dissent Item Scoring

For each retrieved quantum `d` that appears to contradict or provide an alternative to `C`:

```
dissent_relevance = cosine_similarity(embed(d.content.claim_text), embed(C.text))
dissent_strength  = assess_contradiction_strength(d, C)  # LLM call, returns [0,1]
dissent_organic   = 1.0 if d.provenance.generation_epoch < C.generation_epoch
                    else 0.5  # Pre-existing dissent is more credible
```

**Dissent quality score:**

```
dissent_quality(d) = dissent_relevance × dissent_strength × dissent_organic
```

#### 3.4.3 Dissent Deficit Computation

```
total_dissent = sum(dissent_quality(d) for d in dissent_items)
dissent_deficit = max(0.0, 1.0 - total_dissent / EXPECTED_DISSENT_LEVEL)
```

Where `EXPECTED_DISSENT_LEVEL` = 1.5 (calibrated so that 1-2 strong dissent items bring deficit to 0).

### 3.5 Step 3: Novelty-Calibrated CODS Score

```
dissent_weight = {N1: 1.0, N2: 0.5, N3: 0.1}[novelty_tier]
cods_score = dissent_deficit × dissent_weight
```

Interpretation:
- `cods_score ≥ 0.7`: HIGH suspicion -- strong dissent deficit in a domain where dissent is expected
- `0.3 ≤ cods_score < 0.7`: MODERATE suspicion
- `cods_score < 0.3`: LOW suspicion -- either dissent was found or novelty calibration reduces concern

**Special case:** If `novelty_tier == N3`, the claim is routed to the Novelty Pathway (Section 9) regardless of CODS score. The CODS score is recorded but does not contribute to the combined scoring formula for N3 claims.

---

## 4. M3: Source Purpose Scoring (Supplementary)

### 4.1 Invocation Conditions

M3 is NOT evaluated by default. It is invoked ONLY when the following ambiguity condition holds:

```
ambiguity = (0.40 ≤ robustness_score ≤ 0.75) AND (0.25 ≤ cods_score ≤ 0.65)
           AND (0.35 ≤ probe_relative_strength ≤ 0.65)
```

This means APRT, CODS, and Adversarial Probing all returned borderline results. M3 breaks the tie.

Estimated invocation rate: ~20% of consolidation candidates (most candidates have at least one decisive signal from M1/M2/Probing).

### 4.2 Scoring Algorithm

When invoked, M3 evaluates whether each contributing quantum's creation context naturally leads to the consolidation topic.

```python
def compute_purpose_score(claim_C, quanta_Q):
    """
    For each quantum, assess whether its creation purpose
    naturally connects to the consolidation topic.

    Uses a SEPARATE evaluator model (not the consolidation LLM)
    to prevent adversarial co-adaptation.
    """
    purpose_scores = []
    for qi in quanta_Q:
        prompt = f"""
        Quantum content: {qi.content.claim_text}
        Quantum domain: {qi.content.domain}
        Quantum creation context: {qi.provenance.creation_context}

        Consolidation topic: {claim_C.text}

        On a scale of 0.0 to 1.0, how naturally does this quantum's
        original research purpose connect to the consolidation topic?

        0.0 = The quantum was clearly created for an unrelated purpose;
              its relevance to the consolidation is coincidental.
        0.5 = The quantum's purpose has some tangential connection.
        1.0 = The quantum was clearly created to investigate exactly
              this topic; its presence in this consolidation is unsurprising.

        Consider: Would this quantum exist even if no one were trying
        to establish this particular consolidation?

        Return only the numerical score.
        """
        score = evaluator_llm_inference(prompt, temperature=0.1)
        purpose_scores.append(parse_float(score))

    # Suspicious pattern: quanta that are highly purpose-aligned
    # with the consolidation (score > 0.8) in a cross-domain context.
    # In genuine cross-domain discovery, most quanta should have
    # LOW purpose alignment (they were created for domain-specific
    # reasons and their cross-domain relevance is emergent).

    high_purpose_count = sum(1 for s in purpose_scores if s > 0.8)
    high_purpose_fraction = high_purpose_count / len(purpose_scores)

    # purpose_suspicion: higher = more suspicious
    # Most quanta having high purpose alignment is suspicious
    purpose_suspicion = high_purpose_fraction

    return min(purpose_suspicion, 0.15)  # Hard cap at 0.15
```

### 4.3 Integration with Final Decision

The purpose score (0 to 0.15) is ADDED to the combined CRP+ score only when invoked. See Section 10.1 for the full scoring formula.

---

## 5. M4: VRF Consolidation Selection

### 5.1 Purpose

Instead of deterministically selecting ALL cross-domain bridge candidates for consolidation, M4 uses VRF-based random selection. This forces an adversary to plant patterns across many more bridges than they want consolidated, because they cannot predict which bridges will be selected.

### 5.2 VRF Seed Construction

The VRF seed for consolidation selection is derived from three inputs to ensure unpredictability and reproducibility:

```
vrf_input = SHA256(
    "CRP_CONSOLIDATION_SELECT" ||
    uint64_be(epoch) ||
    shard_id.encode() ||
    previous_consolidation_hash
)
```

Where:
- `epoch`: Current tidal epoch number
- `shard_id`: The coherence graph shard being processed
- `previous_consolidation_hash`: SHA256 hash of the previous epoch's consolidation outcomes (accepted/rejected claim IDs, sorted). This chains consolidation cycles, preventing prediction beyond one epoch.

The agent evaluates the ECVRF (RFC 9381, curve P-256) using its private key:

```
(beta, pi) = ECVRF_prove(agent.privkey, vrf_input)
```

The VRF output `beta` is a 256-bit pseudorandom value. The proof `pi` allows any party to verify the output without the private key.

### 5.3 Selection Probability Formula

For each candidate bridge `b` identified by `identify_consolidation_candidates()` (C6 Section 5.3.1):

```
selection_hash = SHA256(beta || bridge_id(b))
selection_value = uint256(selection_hash) / 2^256    # ∈ [0, 1)

bridge_strength(b) = mean(edge.weight for edge in b.connecting_edges)

# Selection probability is proportional to bridge strength
# but bounded by the base selection rate K/M
base_rate = K / M    # K = selected per cycle, M = total candidates
                     # Default: K/M = 0.10 (10%)

adjusted_threshold = base_rate × (0.5 + bridge_strength(b))
# Strong bridges (strength ~1.0) have ~1.5x base rate
# Weak bridges (strength ~0.0) have ~0.5x base rate

selected = (selection_value < adjusted_threshold)
```

### 5.4 Coverage Guarantee

Over time, every bridge will eventually be selected. The expected number of epochs until bridge `b` is selected:

```
E[epochs_until_selected(b)] = 1 / adjusted_threshold(b)
```

For the weakest bridges (strength ≈ 0): `E ≈ 1 / (0.10 × 0.5) = 20 epochs`
For average bridges (strength ≈ 0.5): `E ≈ 1 / (0.10 × 1.0) = 10 epochs`
For the strongest bridges (strength ≈ 1.0): `E ≈ 1 / (0.10 × 1.5) ≈ 7 epochs`

All bridges are explored within ~20 epochs with high probability.

### 5.5 Adversary Cost Multiplication

Without VRF selection: adversary plants 1 bridge, it is guaranteed to be consolidated next cycle.
With VRF selection at 10%: adversary must plant ~10 bridges to have one selected per cycle, and cannot predict which.

Combined with M1 APRT (which may detect the planted bridge even when selected), the adversary must plant ~10 bridges × ~3 attempts per bridge (accounting for APRT detection) = ~30 planted bridges for one successful poisoning. This is a 30x cost multiplication over the base system.

### 5.6 Integration with C3 VRF Infrastructure

CRP+ reuses the ECVRF infrastructure from C3 Section 5.2.1. The same key pairs used for committee selection are used for consolidation selection. The VRF input domain is separated by the `"CRP_CONSOLIDATION_SELECT"` prefix to prevent cross-domain VRF output reuse.

The VRF proof `pi` is stored alongside each consolidation decision record, enabling any party to verify the selection was honest.

---

## 6. M5: Graduated Credibility Ladder

### 6.1 Rung Definitions

All K-class quanta produced by dreaming consolidation enter at the lowest rung and must earn promotion through accumulating independent corroboration.

| Rung | Name | Uncertainty Floor | Promotion Criteria | Influence Weight |
|------|------|-------------------|-------------------|------------------|
| 0 | SPECULATIVE | u ≥ 0.80 | Created by sandboxed K→K consolidation (M6). Cannot promote directly; must wait for inputs to reach CORROBORATED. | 0.00 (no influence) |
| 1 | PROVISIONAL | u ≥ 0.50 | Default for all K-class from dreaming. | 0.25 |
| 2 | CORROBORATED | u ≥ 0.30 | ≥1 DIRECT E-class corroboration from independent agent (different agent, different Sentinel cluster, created after the K-class claim). | 0.50 |
| 3 | ESTABLISHED | u ≥ 0.15 | ≥3 corroborations including ≥1 from a different parcel + ≥50 epochs at CORROBORATED without failed challenges. | 0.75 |
| 4 | CANONICAL | u ≥ 0.05 | ≥5 corroborations from ≥3 parcels + ≥200 epochs at ESTABLISHED + zero failed challenges during ESTABLISHED tenure. | 1.00 |

### 6.2 Credibility-Weighted Influence Formula

When a K-class quantum participates in any downstream process (further consolidation, credibility scoring of other claims, coherence graph weighting), its contribution is multiplied by its influence weight:

```
effective_contribution(q) = raw_contribution(q) × influence_weight(q.rung)
```

This means PROVISIONAL claims have only 25% of the influence they would otherwise have. The system "hears" them but does not "trust" them until corroboration arrives.

### 6.3 Promotion Protocol

```python
def check_promotion(quantum, epoch, lineage, corroboration_log):
    """Check if a K-class quantum qualifies for rung promotion."""
    current_rung = quantum.credibility_rung
    corroborations = corroboration_log.get(quantum.id, [])

    # Count qualifying corroborations
    direct_corroborations = [c for c in corroborations
                             if c.type == "DIRECT"
                             and c.agent_id != quantum.provenance.generating_agent
                             and not same_sentinel_cluster(c.agent_id,
                                 quantum.provenance.generating_agent)]

    cross_parcel_corroborations = [c for c in direct_corroborations
                                   if c.parcel_id != resolve_parcel(quantum)]

    distinct_parcels = len(set(c.parcel_id for c in direct_corroborations))

    epochs_at_current_rung = epoch - quantum.rung_promotion_epoch
    failed_challenges = count_failed_challenges(quantum.id,
                            since_epoch=quantum.rung_promotion_epoch)

    # Fast-track check (M5 refinement from FEASIBILITY)
    multi_modal_count = count_distinct_evidence_modalities(corroborations)
    fast_track_eligible = (multi_modal_count >= 3
                          and epochs_at_current_rung >= 2  # 2-cycle minimum
                          and failed_challenges == 0)

    # SPECULATIVE → PROVISIONAL (M6 sandbox promotion)
    if current_rung == 0:
        # Check if input K-class claims have reached CORROBORATED
        input_quanta = lineage.get_inputs(quantum.id)
        if all(q.credibility_rung >= 2 for q in input_quanta):
            return promote(quantum, rung=1, epoch=epoch)
        return None

    # PROVISIONAL → CORROBORATED
    if current_rung == 1:
        if len(direct_corroborations) >= 1:
            return promote(quantum, rung=2, epoch=epoch)
        return None

    # CORROBORATED → ESTABLISHED
    if current_rung == 2:
        if fast_track_eligible:
            return promote(quantum, rung=3, epoch=epoch)
        if (len(direct_corroborations) >= 3
                and len(cross_parcel_corroborations) >= 1
                and epochs_at_current_rung >= 50
                and failed_challenges == 0):
            return promote(quantum, rung=3, epoch=epoch)
        return None

    # ESTABLISHED → CANONICAL
    if current_rung == 3:
        if (len(direct_corroborations) >= 5
                and distinct_parcels >= 3
                and epochs_at_current_rung >= 200
                and failed_challenges == 0):
            return promote(quantum, rung=4, epoch=epoch)
        return None

    return None  # CANONICAL: no further promotion
```

### 6.4 Demotion Conditions

Credibility rungs can decrease under three conditions:

**D1: Failed Challenge.** If a contradiction claim against a K-class quantum passes PCVM verification with belief > 0.5:

```
if quantum.credibility_rung >= 2:  # CORROBORATED or above
    quantum.credibility_rung = max(1, quantum.credibility_rung - 1)
    quantum.rung_promotion_epoch = epoch  # Reset tenure clock
    quantum.failed_challenge_count += 1
```

**D2: Corroboration Retraction.** If a corroborating E-class claim is itself contradicted or dissolved, its corroboration is revoked. If the quantum no longer meets its current rung's criteria, it is demoted.

```python
def check_demotion_on_retraction(quantum, revoked_corroboration, epoch):
    remaining = [c for c in quantum.corroborations if c.id != revoked_corroboration.id]
    required = rung_requirements(quantum.credibility_rung)
    if not meets_requirements(remaining, required):
        quantum.credibility_rung -= 1
        quantum.rung_promotion_epoch = epoch
```

**D3: Consolidation Cascade.** If a K-class quantum contributed to a consolidation that fails (C10 Section 3.3 cascade), the quantum receives a challenge equivalent. If 2+ cascade events occur, demotion is triggered.

**Demotion floor:** Demotion never goes below PROVISIONAL (rung 1) for quanta that entered through normal dreaming. SPECULATIVE (rung 0) is reserved for sandboxed K→K products.

### 6.5 Integration with Existing Empirical Validation Queue

M5 REPLACES the flat PENDING_VALIDATION / VALIDATED binary from C10 Layer 5 with the 4-rung graduated system. The mapping:

| C10 Layer 5 State | M5 Equivalent |
|---|---|
| PENDING_VALIDATION (u ≥ 0.40) | PROVISIONAL (rung 1, u ≥ 0.50) -- stricter |
| VALIDATED (u ≥ 0.10) | ESTABLISHED (rung 3, u ≥ 0.15) -- comparable |

The C10 `EmpiricalValidationQueue` data structure is retained but its `uncertainty_floor` field is now computed from the M5 rung. The `register_corroboration()` method is extended to trigger M5 `check_promotion()`.

### 6.6 Domain-Adaptive Threshold Calibration

Per the FEASIBILITY refinement, uncertainty floor thresholds adapt to domain density:

```python
def calibrated_thresholds(domain, epoch):
    """Compute domain-adaptive uncertainty floors."""
    density = count_active_quanta(domain) / max(1, domain_area(domain))
    prior_consolidations = count_K_class(domain)

    # Dense domains: tighter thresholds (more corroboration available)
    # Sparse domains: relaxed thresholds (corroboration is structurally harder)
    density_factor = sigmoid(density, midpoint=100, steepness=0.02)
    # density_factor ∈ [0, 1]; 0 = sparse, 1 = dense

    thresholds = {
        1: lerp(0.50, 0.50, density_factor),  # PROVISIONAL: always 0.50
        2: lerp(0.35, 0.25, density_factor),   # CORROBORATED: 0.25-0.35
        3: lerp(0.20, 0.10, density_factor),   # ESTABLISHED: 0.10-0.20
        4: lerp(0.08, 0.03, density_factor),   # CANONICAL: 0.03-0.08
    }
    return thresholds

def lerp(sparse_val, dense_val, factor):
    return sparse_val + factor * (dense_val - sparse_val)
```

---

## 7. M6: Consolidation Depth Limits

### 7.1 Purpose

M6 prevents poisoned consolidation-of-consolidation cascades. Without depth limits, a single poisoned K-class claim could be consolidated with other claims into a second-order K-class claim, which could be consolidated again into a third-order claim, amplifying the poison at each level.

### 7.2 Input Weight by Rung

When `identify_consolidation_candidates()` (C6 Section 5.3.1) considers K-class quanta as potential inputs to new consolidations:

| Rung | Participation Allowed | Input Weight |
|------|----------------------|--------------|
| SPECULATIVE (0) | NO -- excluded from all consolidation | 0.00 |
| PROVISIONAL (1) | NO -- excluded from all consolidation | 0.00 |
| CORROBORATED (2) | YES, with reduced weight | 0.50 |
| ESTABLISHED (3) | YES, full weight | 1.00 |
| CANONICAL (4) | YES, full weight | 1.00 |

### 7.3 Enforcement Point

Depth limit enforcement occurs at the earliest possible point: during candidate identification, before any LLM synthesis cost is incurred.

```python
def filter_by_depth_limits(candidate_quanta):
    """
    Filter candidate quanta for consolidation eligibility.
    Called within identify_consolidation_candidates() before
    returning candidates.
    """
    eligible = []
    for q in candidate_quanta:
        if q.claim_class != "K":
            # Non-K-class quanta (E, D, S, etc.) have no depth restrictions
            eligible.append(q)
            continue

        if q.credibility_rung <= 1:  # SPECULATIVE or PROVISIONAL
            # INV-CRP5: PROVISIONAL K-class MUST NOT participate
            continue

        if q.credibility_rung == 2:  # CORROBORATED
            # Allowed but with 50% weight
            q.consolidation_input_weight = 0.50
            eligible.append(q)
        else:
            # ESTABLISHED or CANONICAL: full weight
            q.consolidation_input_weight = 1.00
            eligible.append(q)

    return eligible
```

### 7.4 K→K Sandboxed Consolidation (Exception Path)

Per FEASIBILITY refinement, K→K consolidation (combining unverified K-class claims) is permitted in a sandboxed environment:

```python
def sandboxed_kk_consolidation(candidate):
    """
    Allow K→K consolidation in sandbox.
    Products are tagged SPECULATIVE and isolated.
    """
    # All input quanta are K-class at PROVISIONAL or above
    k_inputs = [q for q in candidate.quanta if q.claim_class == "K"]

    if not all(q.credibility_rung >= 1 for q in k_inputs):
        return REJECT("SPECULATIVE inputs cannot participate in sandboxed consolidation")

    # Run normal synthesis but tag output as SPECULATIVE
    claims = execute_llm_synthesis(candidate)

    for claim in claims:
        claim.credibility_rung = 0  # SPECULATIVE
        claim.sandbox_flag = True
        claim.sandbox_input_ids = [q.id for q in k_inputs]
        claim.uncertainty_floor = 0.80

        # SPECULATIVE claims cannot:
        # - Participate in further consolidation (even sandboxed)
        # - Influence credibility scoring of non-sandboxed quanta
        # - Be cited by non-sandboxed processes
        claim.isolation_constraints = FULL_SANDBOX

    return claims
```

**Sandbox lifecycle:**
- If ALL input K-class claims reach CORROBORATED within 10 cycles: sandbox product is promoted to PROVISIONAL and enters normal processing.
- If ANY input K-class claim is rejected or remains PROVISIONAL for >10 cycles: sandbox product is archived (stored in immune memory for pattern reference, not deleted).

---

## 8. M7: Immune Memory

### 8.1 Purpose

When a consolidation is rejected (by CRP+ scoring, APRT fragility, adversarial probing, or PCVM verification), M7 stores a signature of the rejected pattern. If a similar pattern appears in the future, it receives enhanced scrutiny automatically.

### 8.2 Signature Extraction

Upon rejection, extract a three-level signature:

```python
def extract_immune_signature(rejected_claim, contributing_quanta, rejection_reason):
    """
    Extract a multi-level signature from a rejected consolidation.
    """
    # L1: Content Hash (exact match detection)
    l1_hash = SHA256(rejected_claim.text.encode())

    # L2: Structural Pattern (similar attack detection)
    domains = sorted(set(q.content.domain for q in contributing_quanta))
    domain_pair = tuple(domains[:2])  # Primary domain bridge
    bridge_type = classify_bridge_type(rejected_claim)  # ANALOGY, CAUSAL, etc.
    quanta_count_range = (len(contributing_quanta) // 5 * 5,
                          len(contributing_quanta) // 5 * 5 + 5)  # 5-wide bucket
    l2_pattern = StructuralPattern(
        domain_pair=domain_pair,
        bridge_type=bridge_type,
        quanta_count_range=quanta_count_range,
    )

    # L3: Behavioral Pattern (campaign detection)
    creation_epochs = [q.provenance.generation_epoch for q in contributing_quanta]
    injection_timing = compute_timing_profile(creation_epochs)  # mean, std, burst_count

    source_agents = [q.provenance.generating_agent for q in contributing_quanta]
    source_clusters = [get_sentinel_cluster(a) for a in source_agents]
    cluster_distribution = compute_cluster_entropy(source_clusters)

    influence_scores = [compute_influence(q, rejected_claim) for q in contributing_quanta]
    influence_shape = (np.mean(influence_scores), np.std(influence_scores),
                       np.max(influence_scores))

    l3_pattern = BehavioralPattern(
        injection_timing=injection_timing,
        cluster_distribution=cluster_distribution,
        influence_shape=influence_shape,
    )

    return ImmuneSignature(
        signature_id=uuid7(),
        created_epoch=current_epoch(),
        rejection_reason=rejection_reason,
        l1_hash=l1_hash,
        l2_pattern=l2_pattern,
        l3_pattern=l3_pattern,
        match_count=0,
        last_match_epoch=None,
    )
```

### 8.3 Matching Algorithm

When a new consolidation candidate is synthesized, check it against immune memory:

```python
def check_immune_memory(candidate_claim, contributing_quanta, immune_store):
    """
    Check candidate against stored immune signatures.
    Returns the strongest match level found (L1 > L2 > L3 > None).
    """
    candidate_l1 = SHA256(candidate_claim.text.encode())
    candidate_l2 = extract_structural_pattern(candidate_claim, contributing_quanta)
    candidate_l3 = extract_behavioral_pattern(contributing_quanta)

    best_match = None
    best_match_sig = None

    for sig in immune_store.active_signatures():
        # L1: Exact content match
        if candidate_l1 == sig.l1_hash:
            return ImmuneMatch(level="L1", signature=sig, confidence=1.0)

        # L2: Structural pattern match
        l2_score = structural_similarity(candidate_l2, sig.l2_pattern)
        if l2_score >= L2_MATCH_THRESHOLD:  # 0.60 domain overlap AND same bridge type
            if best_match is None or best_match.level > "L2":
                best_match = ImmuneMatch(level="L2", signature=sig, confidence=l2_score)
                best_match_sig = sig

        # L3: Behavioral pattern match
        l3_score = behavioral_similarity(candidate_l3, sig.l3_pattern)
        if l3_score >= L3_MATCH_THRESHOLD:  # 0.50 combined similarity
            if best_match is None:
                best_match = ImmuneMatch(level="L3", signature=sig, confidence=l3_score)
                best_match_sig = sig

    if best_match_sig is not None:
        best_match_sig.match_count += 1
        best_match_sig.last_match_epoch = current_epoch()

    return best_match  # May be None


def structural_similarity(candidate_l2, stored_l2):
    """
    Compute L2 structural pattern similarity.
    Requires domain overlap AND bridge type match.
    """
    # Domain overlap: Jaccard similarity of domain pairs
    domain_overlap = jaccard(set(candidate_l2.domain_pair), set(stored_l2.domain_pair))

    # Bridge type match
    bridge_match = 1.0 if candidate_l2.bridge_type == stored_l2.bridge_type else 0.0

    # Quanta count range overlap
    count_overlap = ranges_overlap(candidate_l2.quanta_count_range,
                                    stored_l2.quanta_count_range)

    # Require domain overlap >= 0.60 AND bridge type match
    if domain_overlap < 0.60 or bridge_match < 1.0:
        return 0.0

    return domain_overlap * 0.6 + count_overlap * 0.4


def behavioral_similarity(candidate_l3, stored_l3):
    """
    Compute L3 behavioral pattern similarity.
    Uses timing profile, cluster distribution, and influence shape.
    """
    timing_sim = 1.0 - abs(candidate_l3.injection_timing.mean -
                           stored_l3.injection_timing.mean) / 100.0
    timing_sim = max(0.0, timing_sim)

    cluster_sim = 1.0 - abs(candidate_l3.cluster_distribution -
                            stored_l3.cluster_distribution)
    cluster_sim = max(0.0, cluster_sim)

    influence_sim = cosine_similarity(
        candidate_l3.influence_shape, stored_l3.influence_shape
    )

    combined = timing_sim * 0.3 + cluster_sim * 0.3 + influence_sim * 0.4
    return combined
```

### 8.4 Memory Management

#### Decay Rules (Signature Aging)

| Level | Base Expiry | Extended Expiry (≥3 matches) |
|-------|------------|------------------------------|
| L1 (Content Hash) | 50 cycles | 100 cycles |
| L2 (Structural) | 100 cycles | 200 cycles |
| L3 (Behavioral) | 200 cycles | 400 cycles |

```python
def garbage_collect_immune_memory(immune_store, current_epoch):
    """Run every epoch. Remove expired signatures, enforce size cap."""

    for sig in immune_store.all_signatures():
        age = current_epoch - sig.created_epoch

        # Determine expiry based on level and match count
        base_expiry = {1: 50, 2: 100, 3: 200}[sig.level_int]
        if sig.match_count >= 3:
            expiry = base_expiry * 2
        else:
            expiry = base_expiry

        # Also check for re-trigger extension
        if sig.last_match_epoch is not None:
            epochs_since_match = current_epoch - sig.last_match_epoch
            if epochs_since_match > 500:
                # No re-trigger in 500 epochs: decay regardless
                immune_store.archive(sig)
                continue

        if age > expiry:
            immune_store.archive(sig)  # Move to archive, not delete

    # Enforce MAX_IMMUNE_SIGNATURES (1000) per shard
    if immune_store.active_count() > MAX_IMMUNE_SIGNATURES:
        # Evict oldest, lowest-match-count signatures first
        excess = immune_store.active_count() - MAX_IMMUNE_SIGNATURES
        candidates = sorted(immune_store.active_signatures(),
                           key=lambda s: (s.match_count, -s.created_epoch))
        for sig in candidates[:excess]:
            immune_store.archive(sig)
```

### 8.5 Enhanced Scrutiny Trigger

When an immune memory match is found:

| Match Level | Action |
|---|---|
| L1 (exact content) | AUTOMATIC REJECT. Same claim was already rejected. Log and block. |
| L2 (structural) | Enhanced APRT: full leave-one-out (not just Tier 1 screening). Add 0.20 to combined CRP+ suspicion score. |
| L3 (behavioral) | Standard APRT but add 0.10 to combined CRP+ suspicion score. Flag for manual review. |

---

## 9. Novelty Pathway

### 9.1 Entry Criteria

A consolidation claim enters the Novelty Pathway if ALL of the following hold:

1. **Novelty classification = N3** (paradigmatic): `domain_overlap < 0.05 AND precedent_count == 0 AND semantic_distance ≥ 0.7`
2. **APRT Tier 1 shows no suspicious clusters**: `len(flagged_clusters) == 0`
3. **Source diversity**: Contributing quanta span ≥3 distinct Sentinel Graph clusters
4. **No L2 or L3 immune memory match**: Not a variant of a previously rejected pattern

If any criterion fails, the claim follows the standard path despite being N3.

### 9.2 N3 Classification Thresholds (Exact)

```python
def classify_n3(domain_overlap, precedent_count, semantic_distance):
    """
    Strict N3 classification.
    ALL THREE conditions must hold simultaneously.
    """
    return (domain_overlap < 0.05          # < 5% of expected bridges exist
            and precedent_count == 0        # Zero prior consolidation attempts
            and semantic_distance >= 0.70)  # Very distant from any existing K-class
```

### 9.3 Enhanced Scrutiny Protocol

Claims on the Novelty Pathway undergo four parallel scrutiny tests:

#### 9.3.1 Enhanced APRT (Full Leave-One-Out)

Instead of Tier 1 screening followed by targeted Tier 2, run full leave-one-out on ALL contributing quanta:

```python
def enhanced_aprt(claim_C, quanta_Q, synthesis_params):
    """Full leave-one-out for Novelty Pathway."""
    stabilities = []
    for i, qi in enumerate(quanta_Q):
        Q_reduced = [q for j, q in enumerate(quanta_Q) if j != i]
        C_prime = execute_llm_synthesis_single(Q_reduced, synthesis_params)
        stability = semantic_similarity(claim_C.text, C_prime.text)
        stabilities.append((qi.id, stability))

    min_stability = min(s for _, s in stabilities)
    fragile_quanta = [(qid, s) for qid, s in stabilities
                      if s < STABILITY_THRESHOLD]  # 0.70

    return EnhancedAPRTResult(
        robustness_score=min_stability,
        fragile_quanta=fragile_quanta,
        all_stabilities=stabilities,
    )
```

Cost: N re-syntheses (N ≈ 10-15). Acceptable for the small number of N3 claims per cycle (~10% of candidates, so ~0.5 per cycle).

#### 9.3.2 Constructive Adversarial Probing

Instead of searching for existing dissent (which won't exist for N3), generate counter-arguments:

```python
def constructive_adversarial_probe(claim_C, quanta_Q):
    """
    Generate and evaluate counter-arguments for N3 claims.
    Uses a separate LLM instance from the consolidation LLM.
    """
    domains = extract_domains(quanta_Q)

    # Step 1: Generate strongest objections
    objection_prompt = f"""
    You are a domain expert skeptic. A system has proposed the following
    cross-domain connection:

    CLAIM: {claim_C.text}
    DOMAIN A: {domains[0]}
    DOMAIN B: {domains[1]}

    Generate the 3 strongest objections that domain experts in
    {domains[0]} and {domains[1]} would raise against this claim.

    For each objection:
    1. State the objection clearly
    2. Explain why it is a serious concern
    3. Rate its severity (1-5)
    """
    objections = evaluator_llm_inference(objection_prompt, temperature=0.3)
    parsed_objections = parse_objections(objections)

    # Step 2: Generate strongest supporting argument
    support_prompt = f"""
    You are an interdisciplinary researcher. A system has proposed:

    CLAIM: {claim_C.text}

    Generate the strongest possible supporting argument for this claim.
    Draw on structural analogies, mathematical parallels, or empirical
    patterns that would validate this cross-domain connection.
    """
    support = evaluator_llm_inference(support_prompt, temperature=0.3)

    # Step 3: Evaluate whether the claim can address the objections
    address_prompt = f"""
    CLAIM: {claim_C.text}

    OBJECTIONS:
    {format_objections(parsed_objections)}

    SUPPORTING ARGUMENT:
    {support}

    For each objection, can the claim (aided by the supporting argument)
    adequately address the concern? Score each: ADDRESSED, PARTIALLY_ADDRESSED,
    or UNADDRESSED.
    """
    evaluation = evaluator_llm_inference(address_prompt, temperature=0.1)
    parsed_eval = parse_evaluation(evaluation)

    addressed_count = sum(1 for e in parsed_eval if e.status == "ADDRESSED")
    total_objections = len(parsed_eval)

    address_ratio = addressed_count / max(1, total_objections)

    if address_ratio < 0.50:
        return ProbeResult(verdict="WEAK_NOVELTY",
                          address_ratio=address_ratio,
                          recommendation="EXTENDED_QUARANTINE")
    else:
        return ProbeResult(verdict="ROBUST_NOVELTY",
                          address_ratio=address_ratio,
                          recommendation="PROCEED_WITH_QUARANTINE")
```

#### 9.3.3 Temporal Quarantine

N3 claims start at PROVISIONAL (rung 1) with a mandatory 5-cycle quarantine:

```python
def apply_temporal_quarantine(quantum, epoch):
    """
    N3 claims must remain PROVISIONAL for at least 5 consolidation
    cycles before being eligible for promotion, regardless of
    corroboration received during quarantine.
    """
    quantum.quarantine_end_epoch = epoch + (5 * CONSOLIDATION_CYCLE_EPOCHS)
    quantum.quarantine_flag = True
    quantum.fast_track_eligible = False  # Disable fast-track during quarantine

    # Corroborations received during quarantine are COUNTED but
    # do not trigger promotion until quarantine expires.
    # This gives the knowledge base time to organically generate
    # dissent if the claim is problematic.
```

During quarantine:
- The system actively monitors for naturally emerging contradictions
- Corroborations are recorded but do not trigger promotion
- The claim is usable (with 25% influence weight) but cannot be promoted
- After quarantine expires, accumulated corroborations are evaluated for promotion

#### 9.3.4 Provenance Deep Audit

Enhanced provenance checking for all contributing quanta:

```python
def provenance_deep_audit(quanta_Q, epoch):
    """
    Enhanced provenance checking for N3 Novelty Pathway claims.
    Goes beyond C10 Layer 1 (I1/I2/I3) with micro-pattern detection.
    """
    results = []

    # Check 1: Temporal micro-patterns
    # Even if quanta span 20+ epochs, adversary campaigns often
    # create quanta at the same time-of-day within each epoch
    creation_timestamps = [q.provenance.creation_timestamp for q in quanta_Q]
    intra_epoch_times = [ts % EPOCH_DURATION for ts in creation_timestamps]

    # Kolmogorov-Smirnov test against uniform distribution
    ks_stat, ks_pvalue = ks_test_uniform(intra_epoch_times, EPOCH_DURATION)
    temporal_suspicious = ks_pvalue < 0.05  # Reject uniform at 5% level

    # Check 2: Framing consistency
    # Planted quanta from the same adversary often share linguistic patterns
    embeddings = [embed(q.content.claim_text) for q in quanta_Q]
    mean_pairwise_sim = mean_pairwise_cosine(embeddings)

    # Organic quanta from different agents/domains should have LOW
    # pairwise similarity (they were written independently)
    framing_suspicious = mean_pairwise_sim > FRAMING_SIMILARITY_THRESHOLD  # 0.60

    # Check 3: Cross-reference with M7 behavioral signatures
    candidate_l3 = extract_behavioral_pattern(quanta_Q)
    behavioral_matches = [sig for sig in immune_store.active_signatures()
                         if behavioral_similarity(candidate_l3, sig.l3_pattern)
                            > L3_MATCH_THRESHOLD * 0.75]  # Lower threshold for audit

    return DeepAuditResult(
        temporal_suspicious=temporal_suspicious,
        temporal_ks_pvalue=ks_pvalue,
        framing_suspicious=framing_suspicious,
        mean_pairwise_similarity=mean_pairwise_sim,
        behavioral_matches=len(behavioral_matches),
        overall_suspicious=temporal_suspicious or framing_suspicious
                           or len(behavioral_matches) > 0,
    )
```

### 9.4 Novelty Pathway Combined Decision

```python
def novelty_pathway_decision(enhanced_aprt_result, probe_result,
                              quarantine_params, deep_audit_result):
    """
    Combined decision for N3 claims on the Novelty Pathway.
    """
    # Hard reject conditions
    if enhanced_aprt_result.robustness_score < 0.50:
        return "REJECT", "N3 claim fails enhanced APRT (fragile)"

    if deep_audit_result.overall_suspicious and \
       enhanced_aprt_result.robustness_score < 0.70:
        return "REJECT", "N3 claim has suspicious provenance AND moderate fragility"

    # Quarantine with extended review
    if probe_result.verdict == "WEAK_NOVELTY":
        return "QUARANTINE_EXTENDED", "N3 claim cannot address >50% of objections"

    if deep_audit_result.overall_suspicious:
        return "QUARANTINE_EXTENDED", "N3 claim has suspicious provenance patterns"

    # Standard quarantine (5 cycles)
    if enhanced_aprt_result.robustness_score >= 0.70 and \
       probe_result.verdict == "ROBUST_NOVELTY" and \
       not deep_audit_result.overall_suspicious:
        return "ACCEPT_WITH_QUARANTINE", "N3 claim passes all scrutiny"

    return "QUARANTINE_EXTENDED", "N3 claim has mixed signals"
```

`QUARANTINE_EXTENDED` doubles the quarantine period from 5 cycles to 10 cycles.

### 9.5 Exit Conditions

A quarantined N3 claim exits quarantine when:

1. **Normal exit:** Quarantine period expires (5 or 10 cycles) AND no contradictions have emerged during quarantine.
2. **Early exit (rare):** 3+ independent DIRECT corroborations from 3+ different parcels arrive before quarantine expires. This represents overwhelming organic confirmation.
3. **Rejection exit:** A strong contradiction (belief > 0.6) emerges during quarantine. The claim is rejected and its signature stored in M7 immune memory.

---

## 10. Cross-Mechanism Integration

### 10.1 Combined Scoring Formula

For **standard candidates** (N1 or N2 novelty tier):

```
base_suspicion = 0.0

# M1 APRT contribution (inverted: low robustness = high suspicion)
aprt_suspicion = max(0.0, 1.0 - robustness_score)
weight_aprt = 0.35

# M2 CODS contribution
cods_suspicion = cods_score  # Already novelty-calibrated
weight_cods = 0.25

# C10 Adversarial Probe contribution (inverted: low relative strength = high suspicion)
probe_suspicion = max(0.0, 1.0 - probe_relative_strength)
weight_probe = 0.25

# M7 Immune Memory contribution
immune_suspicion = {None: 0.0, "L3": 0.10, "L2": 0.20, "L1": 1.0}[immune_match_level]
weight_immune = 0.15

# M3 Source Purpose (conditional, max 0.15)
purpose_addition = purpose_score if m3_invoked else 0.0

combined_suspicion = (weight_aprt * aprt_suspicion
                    + weight_cods * cods_suspicion
                    + weight_probe * probe_suspicion
                    + weight_immune * immune_suspicion
                    + purpose_addition)
```

**Decision thresholds:**

| Combined Suspicion | Decision |
|---|---|
| `< 0.35` | **ACCEPT** — proceed to PCVM verification gate |
| `0.35 - 0.60` | **QUARANTINE** — hold for manual review; run additional adversarial probing |
| `> 0.60` | **REJECT** — store signature in M7 immune memory |

For **N3 candidates** on the Novelty Pathway: the combined scoring formula is NOT used. The Novelty Pathway decision function (Section 9.4) applies instead.

### 10.2 Integration with Existing 5-Layer Hardening

```
CONSOLIDATION PIPELINE WITH CRP+ AND C10 LAYERING
===================================================

                   C10 Layer 1                  C10 Layer 1
                   (Provenance                  (Source
                    Diversity)                  Independence)
                       |                            |
                       v                            v
                   [GATE: PASS/FAIL]           [GATE: PASS/FAIL]
                       |                            |
                       +------------ + -------------+
                                     |
                                     v
                          CRP+ M4: VRF Selection
                                     |
                                     v
                          C6: Synthesis Pipeline
                                     |
                                     v
            +--- CRP+ M7: Immune Memory Check ---+
            |                                     |
            v                                     v
      [match found]                        [no match]
      Enhanced APRT                     Standard APRT (M1)
            |                                     |
            +---------- + -----------------------+
                        |
                        v
                   CRP+ M2: CODS
                        |
               +--------+--------+
               |                 |
               v                 v
          [N1 or N2]          [N3]
          Standard          Novelty Pathway
          Path              (Section 9)
               |                 |
               v                 |
    C10 Layer 2: Adversarial     |
    Consolidation Probing        |
               |                 |
               v                 |
    CRP+ M3: Purpose Score       |
    (conditional)                |
               |                 |
               v                 v
       Combined Scoring    Novelty Decision
               |                 |
               v                 v
        ACCEPT/QUARANTINE/REJECT
               |
               v [if ACCEPT]
    C6: PCVM Verification Gate
               |
               v
    CRP+ M5: Assign Credibility Rung (PROVISIONAL)
               |
               v
    CRP+ M6: Apply Depth Limits
               |
               v
    C10 Layer 4: Rate Limiting
               |
               v
    C10 Layer 5 / M5: Empirical Validation Queue
```

**Summary of layer relationships:**

| CRP+ Mechanism | Extends Layer | Replaces Layer | Independent |
|---|---|---|---|
| M1 (APRT) | | | NEW (between synthesis and probe) |
| M2 (CODS) | | | NEW (between APRT and probe) |
| M3 (Purpose) | Layer 2 (probe) | | Extends probe as tie-breaker |
| M4 (VRF Selection) | | | NEW (replaces deterministic selection) |
| M5 (Credibility Ladder) | Layer 5 (validation queue) | Layer 5 binary model | Replaces with graduated system |
| M6 (Depth Limits) | Layer 3 (lineage) | | Extends lineage with participation constraints |
| M7 (Immune Memory) | | | NEW (between synthesis and APRT) |
| Novelty Pathway | Layer 2 (probe) | | Alternative scrutiny for N3 |

### 10.3 Operational Cost Model

#### Per-Consolidation Cycle Costs

Assumptions: 5 VRF-selected candidates per cycle, N=10 quanta per candidate average.

| Component | LLM Calls | Embedding Ops | Notes |
|---|---|---|---|
| Base synthesis (C6) | 5 × 3 = 15 | 0 | Three-pass synthesis per candidate |
| M4 VRF selection | 0 | 0 | Hash operations only |
| M1 APRT Tier 1 | 0 | 5 × (10 + 100) = 550 | N embeddings + N^2 pairwise per candidate |
| M1 APRT Tier 2 (avg) | 5 × 2.5 = 12.5 | 0 | Average 2.5 re-syntheses per candidate |
| M2 CODS | 5 × 2 = 10 | 5 × 1 = 5 | 1 novelty classification + 1 dissent search per candidate |
| M3 Purpose (20%) | 1 × 1 = 1 | 0 | Invoked for ~1 of 5 candidates |
| M7 Immune Check | 0 | 5 × 1 = 5 | Embedding comparison per candidate |
| C10 Layer 2 Probe | 5 × 2 = 10 | 0 | Counter-hypothesis + scoring per candidate |
| **Novelty Pathway** (0.5 candidates) | | | |
| — Enhanced APRT | 0.5 × 10 = 5 | 0 | Full leave-one-out |
| — Constructive Probe | 0.5 × 3 = 1.5 | 0 | Objections + support + evaluation |
| — Deep Audit | 0 | 0.5 × 10 = 5 | Embedding-based checks |
| **TOTAL** | **~55 LLM calls** | **~565 embeddings** | |
| **Without CRP+** | **15 LLM calls** | **0 embeddings** | Base synthesis only |
| **Cost multiplier** | **~3.7x LLM** | **+565 embeddings** | |

The 3.7x LLM multiplier is lower than the FEASIBILITY estimate of 7.0x because:
1. VRF selection reduces candidate count before CRP+ mechanisms engage
2. APRT Tier 1 eliminates ~60% of Tier 2 work
3. M3 invocation rate is only 20%

**Absolute cost per cycle:** ~55 LLM calls + ~565 embedding operations. If consolidation cycles run every 10 epochs and epochs are ~10 minutes, this is ~55 LLM calls per ~100 minutes, well within any reasonable API budget.

### 10.4 Performance Budget

| Constraint | Budget | CRP+ Usage | Margin |
|---|---|---|---|
| LLM calls per consolidation cycle | 100 | ~55 | 45% headroom |
| Embedding operations per cycle | 2000 | ~565 | 72% headroom |
| Wall-clock time per candidate | 60 seconds | ~35 seconds (est.) | 42% headroom |
| Total CRP+ overhead vs base consolidation | ≤ 5x | ~3.7x | Within budget |

---

## 11. Parameters and Configuration

### 11.1 Constitutional Parameters

These require G-class governance supermajority (C3) to change:

| Parameter | Default | Description |
|---|---|---|
| `VRF_SELECTION_RATE` | 0.10 | Fraction of candidates selected per cycle (K/M) |
| `STABILITY_THRESHOLD` | 0.70 | Minimum semantic similarity for re-synthesis stability |
| `ACCEPT_THRESHOLD` | 0.35 | Combined suspicion below this → ACCEPT |
| `REJECT_THRESHOLD` | 0.60 | Combined suspicion above this → REJECT |
| `MAX_IMMUNE_SIGNATURES` | 1000 | Maximum active immune memory signatures per shard |
| `PROVISIONAL_INFLUENCE_WEIGHT` | 0.25 | Influence weight for PROVISIONAL K-class |
| `QUARANTINE_CYCLES_N3` | 5 | Mandatory quarantine cycles for N3 claims |
| `DEPTH_LIMIT_PROVISIONAL` | EXCLUDED | PROVISIONAL K-class excluded from consolidation |
| `DEPTH_LIMIT_CORROBORATED_WEIGHT` | 0.50 | Input weight for CORROBORATED K-class |

### 11.2 Operational Parameters

These can be changed by system operators without governance:

| Parameter | Default | Description |
|---|---|---|
| `CONSOLIDATION_MIN_EDGE_WEIGHT` | 0.30 | Minimum edge weight for candidate identification |
| `HIGH_INFLUENCE_SIGMA` | 2.0 | Standard deviations above mean for high-influence flag |
| `REDUNDANT_CLUSTER_SIMILARITY` | 0.85 | Cosine similarity threshold for cluster detection |
| `REDUNDANT_CLUSTER_MIN_SIZE` | 3 | Minimum quanta in a suspicious cluster |
| `RANDOM_SUBSET_FRACTION` | 0.30 | Fraction of quanta removed in Case C |
| `EXPECTED_DISSENT_LEVEL` | 1.5 | Expected total dissent quality for deficit computation |
| `DISSENT_WEIGHT_N1` | 1.0 | Dissent deficit weight for N1 (incremental) |
| `DISSENT_WEIGHT_N2` | 0.5 | Dissent deficit weight for N2 (bridging) |
| `DISSENT_WEIGHT_N3` | 0.1 | Dissent deficit weight for N3 (paradigmatic) |
| `M3_MAX_CONTRIBUTION` | 0.15 | Hard cap on M3 purpose score contribution |
| `M3_HIGH_PURPOSE_THRESHOLD` | 0.80 | Purpose alignment above this is suspicious |
| `L2_MATCH_THRESHOLD` | 0.60 | Immune memory L2 structural match threshold |
| `L3_MATCH_THRESHOLD` | 0.50 | Immune memory L3 behavioral match threshold |
| `L1_EXPIRY_CYCLES` | 50 | Immune memory L1 signature expiry |
| `L2_EXPIRY_CYCLES` | 100 | Immune memory L2 signature expiry |
| `L3_EXPIRY_CYCLES` | 200 | Immune memory L3 signature expiry |
| `BRIDGE_DENSITY_FACTOR` | 0.01 | Expected cross-domain bridge density |
| `DOMAIN_OVERLAP_N1_THRESHOLD` | 0.30 | Domain overlap threshold for N1 classification |
| `DOMAIN_OVERLAP_N3_THRESHOLD` | 0.05 | Domain overlap threshold for N3 classification |
| `SEMANTIC_DISTANCE_N1_THRESHOLD` | 0.40 | Semantic distance threshold for N1 |
| `SEMANTIC_DISTANCE_N3_THRESHOLD` | 0.70 | Semantic distance threshold for N3 |
| `FRAMING_SIMILARITY_THRESHOLD` | 0.60 | Deep audit framing suspicion threshold |
| `KS_TEST_PVALUE_THRESHOLD` | 0.05 | Deep audit temporal micro-pattern p-value |
| `CORROBORATION_RELIEF_DIRECT` | 0.10 | Uncertainty floor reduction per DIRECT corroboration |
| `CORROBORATION_RELIEF_PARTIAL` | 0.05 | Uncertainty floor reduction per PARTIAL corroboration |
| `CORROBORATION_RELIEF_INDIRECT` | 0.025 | Uncertainty floor reduction per INDIRECT corroboration |
| `FAST_TRACK_MODALITIES` | 3 | Minimum distinct evidence modalities for fast-track |
| `SANDBOX_TIMEOUT_CYCLES` | 10 | Max cycles before sandboxed K→K is archived |
| `WEIGHT_APRT` | 0.35 | Combined scoring weight for APRT |
| `WEIGHT_CODS` | 0.25 | Combined scoring weight for CODS |
| `WEIGHT_PROBE` | 0.25 | Combined scoring weight for adversarial probe |
| `WEIGHT_IMMUNE` | 0.15 | Combined scoring weight for immune memory |

---

## 12. Pseudocode: All Critical Algorithms

### 12.1 Master Orchestrator

```python
def crp_plus_evaluate(candidate_claim, contributing_quanta, shard, epoch):
    """
    Master CRP+ evaluation function.
    Called after Three-Pass LLM Synthesis completes.
    Returns: CRPResult with decision and supporting data.
    """
    result = CRPResult()

    # ═══════════════════════════════════════════════════════════
    # STEP 1: Immune Memory Check (M7)
    # ═══════════════════════════════════════════════════════════
    immune_match = check_immune_memory(
        candidate_claim, contributing_quanta, shard.immune_store
    )
    result.immune_match = immune_match

    if immune_match and immune_match.level == "L1":
        # Exact content re-submission: automatic reject
        store_rejection(candidate_claim, contributing_quanta, "L1_IMMUNE_MATCH")
        result.decision = "REJECT"
        result.reason = "Exact match to previously rejected consolidation"
        return result

    enhanced_mode = (immune_match is not None and immune_match.level in ("L2", "L3"))

    # ═══════════════════════════════════════════════════════════
    # STEP 2: APRT — Perturbation Robustness Testing (M1)
    # ═══════════════════════════════════════════════════════════
    if enhanced_mode:
        aprt_result = enhanced_aprt(
            candidate_claim, contributing_quanta, shard.synthesis_params
        )
    else:
        aprt_result = standard_aprt(
            candidate_claim, contributing_quanta, shard.synthesis_params
        )
    result.aprt = aprt_result

    # ═══════════════════════════════════════════════════════════
    # STEP 3: CODS — Calibrated Organic Dissent Search (M2)
    # ═══════════════════════════════════════════════════════════
    cods_result = evaluate_cods(
        candidate_claim, contributing_quanta, shard.coherence_graph
    )
    result.cods = cods_result

    # ═══════════════════════════════════════════════════════════
    # STEP 4: Novelty Pathway Branch
    # ═══════════════════════════════════════════════════════════
    if cods_result.novelty_tier == "N3" and meets_novelty_pathway_criteria(
            aprt_result, contributing_quanta, immune_match):

        # Route to Novelty Pathway
        np_result = execute_novelty_pathway(
            candidate_claim, contributing_quanta, aprt_result, shard, epoch
        )
        result.novelty_pathway = np_result
        result.decision = np_result.decision
        result.reason = np_result.reason

        if result.decision == "REJECT":
            sig = extract_immune_signature(
                candidate_claim, contributing_quanta, result.reason
            )
            shard.immune_store.add(sig)

        return result

    # ═══════════════════════════════════════════════════════════
    # STEP 5: C10 Adversarial Consolidation Probing
    # ═══════════════════════════════════════════════════════════
    probe_result = probe_consolidation_adversarially(
        candidate_claim.text, contributing_quanta, shard.synthesis_context
    )
    result.probe = probe_result

    if probe_result.recommendation == "DISCARD_CONSOLIDATION":
        sig = extract_immune_signature(
            candidate_claim, contributing_quanta, "ADVERSARIAL_PROBE_REJECTION"
        )
        shard.immune_store.add(sig)
        result.decision = "REJECT"
        result.reason = "Counter-hypothesis stronger than consolidation"
        return result

    # ═══════════════════════════════════════════════════════════
    # STEP 6: M3 Source Purpose Scoring (Conditional)
    # ═══════════════════════════════════════════════════════════
    m3_invoked = False
    purpose_score = 0.0

    ambiguity = (0.40 <= aprt_result.robustness_score <= 0.75
                 and 0.25 <= cods_result.cods_score <= 0.65
                 and 0.35 <= probe_result.relative_strength <= 0.65)

    if ambiguity:
        purpose_score = compute_purpose_score(candidate_claim, contributing_quanta)
        m3_invoked = True

    result.m3_invoked = m3_invoked
    result.purpose_score = purpose_score

    # ═══════════════════════════════════════════════════════════
    # STEP 7: Combined Scoring
    # ═══════════════════════════════════════════════════════════
    aprt_suspicion = max(0.0, 1.0 - aprt_result.robustness_score)
    cods_suspicion = cods_result.cods_score
    probe_suspicion = max(0.0, 1.0 - probe_result.relative_strength)
    immune_suspicion = {
        None: 0.0, "L3": 0.10, "L2": 0.20
    }.get(immune_match.level if immune_match else None, 0.0)

    combined = (WEIGHT_APRT * aprt_suspicion
              + WEIGHT_CODS * cods_suspicion
              + WEIGHT_PROBE * probe_suspicion
              + WEIGHT_IMMUNE * immune_suspicion
              + purpose_score)

    result.combined_suspicion = combined

    if combined < ACCEPT_THRESHOLD:
        result.decision = "ACCEPT"
        result.reason = f"Combined suspicion {combined:.3f} below threshold"
    elif combined > REJECT_THRESHOLD:
        sig = extract_immune_signature(
            candidate_claim, contributing_quanta,
            f"COMBINED_SCORE_REJECTION ({combined:.3f})"
        )
        shard.immune_store.add(sig)
        result.decision = "REJECT"
        result.reason = f"Combined suspicion {combined:.3f} above threshold"
    else:
        result.decision = "QUARANTINE"
        result.reason = f"Combined suspicion {combined:.3f} in ambiguous range"

    return result
```

### 12.2 Standard APRT

```python
def standard_aprt(claim_C, quanta_Q, synthesis_params):
    """Standard two-tier APRT."""

    # ── Tier 1: Embedding Influence Screening ──
    emb_C = embed(claim_C.text)
    embeddings = {q.id: embed(q.content.claim_text) for q in quanta_Q}

    influences = {}
    for q in quanta_Q:
        relevance = cosine_similarity(embeddings[q.id], emb_C)

        max_redundancy = max(
            (cosine_similarity(embeddings[q.id], embeddings[other.id])
             for other in quanta_Q if other.id != q.id),
            default=0.0
        )
        uniqueness = 1.0 - max_redundancy
        influences[q.id] = relevance * uniqueness

    inf_values = list(influences.values())
    mu_inf = mean(inf_values)
    sigma_inf = std(inf_values)

    # Flag high-influence quanta
    flagged = [qid for qid, inf in influences.items()
               if inf > mu_inf + HIGH_INFLUENCE_SIGMA * sigma_inf]

    # Detect redundant clusters
    clusters = []
    visited = set()
    for i, qi in enumerate(quanta_Q):
        if qi.id in visited:
            continue
        cluster = [qi.id]
        for j, qj in enumerate(quanta_Q):
            if j <= i or qj.id in visited:
                continue
            if cosine_similarity(embeddings[qi.id], embeddings[qj.id]) > \
               REDUNDANT_CLUSTER_SIMILARITY:
                cluster.append(qj.id)
        if len(cluster) >= REDUNDANT_CLUSTER_MIN_SIZE:
            # Check all members are relevant to C
            cluster_relevant = all(
                cosine_similarity(embeddings[qid], emb_C) > 0.5
                for qid in cluster
            )
            if cluster_relevant:
                clusters.append(cluster)
                visited.update(cluster)

    # ── Case Classification ──
    if len(flagged) > 0:
        case = "A"
    elif len(clusters) > 0:
        case = "B"
    else:
        case = "C"

    # ── Tier 2: Targeted Re-Synthesis ──
    if case == "A":
        stabilities = []
        for qid in flagged[:3]:  # Cap at 3 re-syntheses
            Q_reduced = [q for q in quanta_Q if q.id != qid]
            C_prime = execute_llm_synthesis_single(Q_reduced, synthesis_params)
            stab = semantic_similarity(claim_C.text, C_prime.text)
            stabilities.append(stab)
        robustness = min(stabilities) if stabilities else 1.0
        resynthesis_count = len(stabilities)

    elif case == "B":
        stabilities = []
        for cluster in clusters[:2]:  # Cap at 2 cluster removals
            Q_reduced = [q for q in quanta_Q if q.id not in cluster]
            if len(Q_reduced) < 3:  # Need minimum quanta for synthesis
                stabilities.append(0.0)  # Cluster IS the consolidation
                continue
            C_prime = execute_llm_synthesis_single(Q_reduced, synthesis_params)
            stab = semantic_similarity(claim_C.text, C_prime.text)
            stabilities.append(stab)
        robustness = min(stabilities) if stabilities else 1.0
        resynthesis_count = len(stabilities)

    else:  # Case C
        # Random 30% removal
        vrf_seed = SHA256(claim_C.text.encode() + b"APRT_RANDOM")
        remove_indices = vrf_select_subset(
            len(quanta_Q), RANDOM_SUBSET_FRACTION, vrf_seed
        )
        Q_reduced = [q for i, q in enumerate(quanta_Q) if i not in remove_indices]
        C_prime = execute_llm_synthesis_single(Q_reduced, synthesis_params)
        robustness = semantic_similarity(claim_C.text, C_prime.text)
        resynthesis_count = 1

    return APRTResult(
        robustness_score=robustness,
        case=case,
        flagged_quanta=flagged,
        flagged_clusters=clusters,
        resynthesis_count=resynthesis_count,
        influences=influences,
    )
```

### 12.3 CODS Evaluation

```python
def evaluate_cods(claim_C, quanta_Q, coherence_graph):
    """Full CODS evaluation: novelty classification + dissent search."""

    # ── Step 1: Novelty Classification ──
    domains = extract_domains(quanta_Q)
    domain_a, domain_b = domains[0], domains[1] if len(domains) > 1 else domains[0]

    # F1: Domain overlap
    existing_bridges = count_analogy_edges(domain_a, domain_b, coherence_graph)
    expected = max(1, int(sqrt(count_quanta(domain_a) * count_quanta(domain_b))
                         * BRIDGE_DENSITY_FACTOR))
    domain_overlap = existing_bridges / expected

    # F2: Semantic distance
    nearest_K = find_nearest_K_class(claim_C, coherence_graph)
    if nearest_K is not None:
        semantic_distance = cosine_distance(
            embed(claim_C.text), embed(nearest_K.content.claim_text)
        )
    else:
        semantic_distance = 1.0  # No existing K-class at all

    # F3: Precedent count
    precedent_count = count_prior_consolidation_attempts(
        domain_a, domain_b, lookback_epochs=500
    )

    # Classify
    if classify_n3(domain_overlap, precedent_count, semantic_distance):
        novelty_tier = "N3"
    elif (domain_overlap >= DOMAIN_OVERLAP_N1_THRESHOLD
          or precedent_count >= 3
          or semantic_distance < SEMANTIC_DISTANCE_N1_THRESHOLD):
        novelty_tier = "N1"
    else:
        novelty_tier = "N2"

    # ── Step 2: Dissent Search ──
    queries = generate_dissent_queries(claim_C)
    dissent_items = []

    for query in queries:
        query_emb = embed(query)
        candidates = semantic_search(query_emb, coherence_graph,
                                     top_k=10, min_similarity=0.3)
        for candidate in candidates:
            strength = assess_contradiction_strength(candidate, claim_C)
            if strength > 0.2:  # Minimum relevance threshold
                relevance = cosine_similarity(
                    embed(candidate.content.claim_text), embed(claim_C.text)
                )
                organic = 1.0 if candidate.provenance.generation_epoch < \
                          claim_C.generation_epoch else 0.5
                quality = relevance * strength * organic
                dissent_items.append(DissentItem(
                    quantum=candidate, quality=quality
                ))

    # Deduplicate by quantum ID, keep highest quality
    seen = {}
    for item in dissent_items:
        if item.quantum.id not in seen or item.quality > seen[item.quantum.id].quality:
            seen[item.quantum.id] = item
    dissent_items = list(seen.values())

    # ── Step 3: Dissent Deficit ──
    total_dissent = sum(item.quality for item in dissent_items)
    dissent_deficit = max(0.0, 1.0 - total_dissent / EXPECTED_DISSENT_LEVEL)

    # ── Step 4: Novelty-Calibrated Score ──
    dissent_weight = {"N1": DISSENT_WEIGHT_N1, "N2": DISSENT_WEIGHT_N2,
                      "N3": DISSENT_WEIGHT_N3}[novelty_tier]
    cods_score = dissent_deficit * dissent_weight

    return CODSResult(
        novelty_tier=novelty_tier,
        domain_overlap=domain_overlap,
        semantic_distance=semantic_distance,
        precedent_count=precedent_count,
        dissent_items=dissent_items,
        dissent_deficit=dissent_deficit,
        cods_score=cods_score,
    )
```

### 12.4 VRF Consolidation Selection

```python
def vrf_select_consolidation_candidates(all_candidates, agent, shard, epoch):
    """
    VRF-based selection of consolidation candidates.
    Replaces deterministic selection in C6 Section 5.3.1.
    """
    # Construct VRF input
    previous_hash = shard.previous_consolidation_hash
    vrf_input = SHA256(
        b"CRP_CONSOLIDATION_SELECT"
        + uint64_be(epoch)
        + shard.shard_id.encode()
        + previous_hash
    )

    # Evaluate VRF
    beta, pi = ECVRF_prove(agent.privkey, vrf_input)

    selected = []
    for candidate in all_candidates:
        bridge_id = compute_bridge_id(candidate)
        selection_hash = SHA256(beta + bridge_id.encode())
        selection_value = uint256(selection_hash) / (2**256)

        strength = mean(e.weight for e in candidate.connecting_edges) \
                   if candidate.connecting_edges else 0.5
        threshold = VRF_SELECTION_RATE * (0.5 + strength)

        if selection_value < threshold:
            candidate.vrf_proof = pi
            candidate.vrf_output = beta
            selected.append(candidate)

    return selected
```

### 12.5 Credibility Ladder Epoch Update

```python
def update_credibility_ladder(shard, epoch, corroboration_log, lineage):
    """
    Called each epoch during the regulation phase.
    Checks all K-class quanta for promotion/demotion.
    """
    for q in shard.active_K_class_quanta():
        # Check promotion
        promotion = check_promotion(q, epoch, lineage, corroboration_log)
        if promotion is not None:
            apply_promotion(q, promotion, epoch)
            continue

        # Check quarantine expiry for N3 claims
        if q.quarantine_flag and epoch >= q.quarantine_end_epoch:
            q.quarantine_flag = False
            q.fast_track_eligible = True  # Re-enable fast-track

        # Check sandbox timeout for SPECULATIVE claims
        if q.credibility_rung == 0:
            sandbox_age = epoch - q.provenance.generation_epoch
            if sandbox_age > SANDBOX_TIMEOUT_CYCLES * CONSOLIDATION_CYCLE_EPOCHS:
                # Check if inputs have been promoted
                input_quanta = lineage.get_inputs(q.id)
                if any(iq.credibility_rung < 2 for iq in input_quanta):
                    # Inputs still not corroborated: archive
                    archive_speculative(q, shard)

        # Apply domain-adaptive uncertainty floors
        thresholds = calibrated_thresholds(q.content.domain, epoch)
        required_floor = thresholds.get(q.credibility_rung, 0.50)
        if q.opinion.uncertainty < required_floor:
            deficit = required_floor - q.opinion.uncertainty
            q.opinion.uncertainty += deficit
            q.opinion.belief = max(0.01, q.opinion.belief - deficit)
            normalize_opinion(q.opinion)
```

### 12.6 Immune Memory Garbage Collection

```python
def immune_memory_gc(immune_store, epoch):
    """Called every epoch during regulation phase."""
    expired = []

    for sig in immune_store.active_signatures():
        age = epoch - sig.created_epoch

        level_expiry = {
            "L1": L1_EXPIRY_CYCLES,
            "L2": L2_EXPIRY_CYCLES,
            "L3": L3_EXPIRY_CYCLES,
        }[sig.level]

        # Double expiry for persistent patterns
        if sig.match_count >= 3:
            level_expiry *= 2

        # Check re-trigger decay
        if sig.last_match_epoch is not None:
            if (epoch - sig.last_match_epoch) > 500:
                expired.append(sig)
                continue

        if age > level_expiry:
            expired.append(sig)

    for sig in expired:
        immune_store.archive(sig)

    # Enforce size cap
    while immune_store.active_count() > MAX_IMMUNE_SIGNATURES:
        victim = min(immune_store.active_signatures(),
                     key=lambda s: (s.match_count, -s.created_epoch))
        immune_store.archive(victim)
```

---

## 13. Failure Mode Catalogue

### FM-1: APRT False Positive (Organic Consolidation Flagged as Fragile)

**Trigger:** A genuinely robust consolidation has one quantum that happens to be uniquely relevant (high influence score), and removing it produces a semantically different (but functionally equivalent) re-synthesis.

**Symptoms:** Case A triggered, stability < 0.70 despite genuine pattern.

**Impact:** False rejection. Genuine knowledge lost.

**Mitigation:** The stability comparison uses embedding cosine similarity, which captures semantic equivalence even when wording differs. The 0.70 threshold allows moderate rephrasing. If false positives exceed 5% of consolidations, raise STABILITY_THRESHOLD to 0.60 (operational parameter).

**Detection:** Monitor rejection rate vs. manual review agreement. If reviewers disagree with >10% of rejections, recalibrate.

---

### FM-2: CODS Novelty Misclassification (N1 Classified as N3)

**Trigger:** Domain overlap and precedent count are zero because the knowledge base is sparse in one domain (newly seeded), not because the connection is genuinely novel.

**Symptoms:** Incremental claims receive N3 treatment (Novelty Pathway), wasting resources and delaying acceptance.

**Impact:** Increased latency and cost for claims that should be standard.

**Mitigation:** Domain density check before novelty classification. If either domain has < 10 active quanta, force N2 (never N3) regardless of overlap metrics. This is a constitutional safeguard against sparse-domain misclassification.

**Detection:** Track N3 classification rate per domain pair. If a domain pair consistently produces N3 classifications, flag for manual review of domain ontology.

---

### FM-3: VRF Selection Starvation (Important Bridge Never Selected)

**Trigger:** A bridge with low strength has consistently bad VRF luck and is not selected for 50+ epochs.

**Symptoms:** Knowledge accumulates around an unexplored bridge without consolidation.

**Impact:** Missed discovery. Low immediate impact (the bridge is weak), but compounds over time.

**Mitigation:** Coverage guarantee: if a bridge has not been selected in 20 epochs, its adjusted threshold is boosted by 0.01 per additional epoch. After 30 epochs, the threshold doubles. After 40 epochs, selection is forced regardless of VRF output.

```python
def coverage_boost(bridge, epoch):
    epochs_since_selection = epoch - bridge.last_selected_epoch
    if epochs_since_selection > 40:
        return FORCE_SELECT
    elif epochs_since_selection > 20:
        return min(1.0, VRF_SELECTION_RATE * (0.5 + bridge.strength)
                   + 0.01 * (epochs_since_selection - 20))
    else:
        return VRF_SELECTION_RATE * (0.5 + bridge.strength)
```

---

### FM-4: Credibility Ladder Bottleneck (Genuine Discoveries Stuck at PROVISIONAL)

**Trigger:** A K-class claim is genuinely correct but the domain is sparse, so independent E-class corroboration is slow to arrive.

**Symptoms:** Claim remains at PROVISIONAL for hundreds of epochs, contributing only 25% influence.

**Impact:** System underweights genuine knowledge. Discovery value is delayed.

**Mitigation:** Domain-adaptive thresholds (Section 6.6) relax promotion criteria for sparse domains. Additionally, the fast-track provision allows claims with multi-modal corroboration to skip CORROBORATED entirely. If a claim remains PROVISIONAL for > 200 epochs without contradiction, it does NOT get automatically promoted (that would defeat the purpose), but it is flagged for manual review.

---

### FM-5: Immune Memory False Match (Legitimate Claim Matches Rejected Signature)

**Trigger:** L2 or L3 signature is too broad, matching a legitimate claim that happens to bridge the same domain pair with similar structure.

**Symptoms:** Legitimate claim receives enhanced scrutiny (increased cost) or suspicious score boost (0.10-0.20).

**Impact:** Increased cost and potential false rejection of legitimate knowledge.

**Mitigation:**
1. L2 requires BOTH domain overlap ≥ 0.60 AND same bridge type. Domain pair alone is insufficient.
2. L3 requires combined behavioral similarity ≥ 0.50 across three dimensions. Single-dimension matches are insufficient.
3. Enhanced scrutiny (full leave-one-out) does not reject the claim; it just runs more tests. A genuinely robust claim will pass enhanced APRT.
4. The 0.10-0.20 suspicion boost can be overridden if APRT robustness > 0.85 (strong evidence of genuineness).

**Detection:** Track immune memory match rate. If > 5% of candidates match immune memory, signatures may be too broad. Tighten thresholds.

---

### FM-6: Redundant Cluster Evasion (Adversary Uses Non-Redundant Planting)

**Trigger:** Sophisticated adversary plants quanta that are each unique (covering different facets of the target conclusion) rather than redundant copies.

**Symptoms:** APRT Tier 1 classifies as Case C (uniform influence). Single random-subset check may pass if 70% of planted quanta remain.

**Impact:** Poisoned consolidation passes APRT.

**Mitigation:** This is APRT's known weakness. Defense relies on CODS (dissent deficit detection for N1/N2 claims), adversarial probing (counter-hypothesis generation), and the credibility ladder (PROVISIONAL rung limits damage). The combined scoring formula means passing APRT alone is insufficient; the adversary must also defeat CODS and probing.

**Residual risk:** A sophisticated adversary that plants diverse, non-redundant quanta across many domains AND avoids dissent deficit AND defeats adversarial probing can succeed. Estimated cost: ~30x the base cost (due to VRF selection multiplication). This is the irreducible residual risk.

---

### FM-7: Novelty Pathway Abuse (Adversary Engineers N3 Classification)

**Trigger:** Adversary deliberately bridges two domains with no prior documented relationship to trigger N3 classification and the Novelty Pathway (which does not penalize dissent deficit).

**Symptoms:** Adversarial consolidation enters Novelty Pathway, avoids CODS dissent-deficit penalty.

**Impact:** Adversary avoids one defense mechanism (CODS).

**Mitigation:** The Novelty Pathway is NOT a free pass. It imposes:
1. Full leave-one-out APRT (more expensive than standard APRT)
2. Constructive adversarial probing (generates objections the claim must address)
3. 5-cycle temporal quarantine
4. Provenance deep audit

The Novelty Pathway is HARDER to pass than the standard path for planted claims. The adversary gains nothing by engineering N3 classification because the alternative scrutiny is equally rigorous on different dimensions.

---

### FM-8: Sandbox Accumulation (Speculative Claims Consume Resources)

**Trigger:** Many K→K consolidations are created, few input claims get promoted, leading to large SPECULATIVE backlogs.

**Symptoms:** Growing number of SPECULATIVE claims consuming storage. Sandbox timeout cycle (10 cycles) creates periodic archival bursts.

**Impact:** Storage overhead. No correctness impact (SPECULATIVE claims are fully isolated).

**Mitigation:** Rate limit sandboxed K→K consolidation to MAX_SANDBOXED_PER_CYCLE = 5 per shard per cycle. SPECULATIVE claims consume minimal storage (they are simplified records without full coherence graph integration). Archive aggressively after timeout.

---

### FM-9: Cascade Amplification (M5 Demotion + C10 Cascade Interaction)

**Trigger:** A failed consolidation triggers C10 credibility cascade (Section 3.3) on contributing quanta. If those quanta are K-class, the cascade also triggers M5 demotion, which further reduces their influence weight, which may cause downstream consolidations that depended on them to become fragile.

**Symptoms:** Chain reaction of demotions and cascades from a single failed consolidation.

**Impact:** Excessive credibility reduction. Potentially healthy knowledge is demoted.

**Mitigation:**
1. C10 cascade already has MAX_CASCADE_DEPTH = 5.
2. M5 demotion floor is PROVISIONAL (rung 1); claims cannot be demoted below this.
3. M5 demotion requires 2+ cascade events, not just 1. A single cascade event is logged but does not trigger demotion.
4. Combined: the worst case is a 5-deep cascade reducing each quantum by the capped per_quantum_reduction (0.10), with M5 demotion occurring only if 2+ of those cascade events hit the same quantum.

---

### FM-10: LLM Consistency Failure (Re-Synthesis Produces Different Claim Due to LLM Stochasticity)

**Trigger:** The LLM synthesis is inherently stochastic. Two runs on the same input may produce semantically different outputs even at low temperature, causing false fragility detection in APRT.

**Symptoms:** Case A or Case B shows low stability even though the input set is genuinely robust, because the LLM simply generated a different phrasing.

**Impact:** False fragility → false rejection or inflated suspicion score.

**Mitigation:**
1. Synthesis uses low temperature (0.2) to reduce stochasticity.
2. Stability comparison uses embedding cosine similarity, not string matching. Semantically equivalent but differently-worded claims will have high similarity (typically > 0.85).
3. STABILITY_THRESHOLD at 0.70 allows substantial rephrasing.
4. If false fragility is a persistent problem, add a "re-synthesis consistency check": run synthesis twice on the SAME input and measure baseline variability. Set STABILITY_THRESHOLD to baseline_variability + margin.

---

*End of C13 DESIGN document. This specification is ready for the SPECIFICATION stage, which will formalize the pseudocode into normative conformance requirements, add test vectors, and produce the Master Technical Specification.*
