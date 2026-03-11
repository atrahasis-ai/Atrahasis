# C13: CRP+ — Consolidation Robustness Protocol

## Master Technical Specification v1.0

**Invention:** C13 — Consolidation Poisoning Defense
**Stage:** SPECIFICATION (Final Deliverable)
**Date:** 2026-03-10
**System:** Atrahasis Agent System
**Classification:** CRP+ — 7-mechanism consolidation defense with novelty pathway
**Normative References:** C3 (Tidal Noosphere v1.0), C5 (PCVM v1.0), C6 (EMA v1.0), C8 (DSF v2.0), C10 (Hardening Addenda), C11 (CACT v1.0), C12 (AVAP v1.0), RFC 9381 (ECVRF)
**Assessment Scores:** Novelty 3.5/5, Feasibility 4/5, Impact 4/5, Risk 6/10

> **Normative Reference Update (2026-03-11):** Normative references updated to C3 v2.0, C5 v2.0, C6 v2.0. C6 v2.0 integrates CRP+ consolidation defense mechanisms from this specification into the core EMA architecture. However, C13 retains normative authority over its threat model (consolidation poisoning taxonomy, cascade amplification analysis), formal proofs (adversary cost multiplication bounds, perturbation robustness analysis), and attack taxonomies (7-mechanism coverage model, novelty pathway design). Where C6 v2.0 and C13 overlap, C6 v2.0 governs integration behavior and C13 governs threat analysis.

---

## Abstract

CRP+ (Consolidation Robustness Protocol) is a 7-mechanism defense architecture that hardens the EMA dreaming consolidation pipeline (C6 Section 5.3) against consolidation poisoning — the deliberate planting of adversarial quanta designed to produce false cross-domain knowledge claims during automated synthesis. CRP+ operates along three defense axes: **Formation Analysis** (M1 Adaptive Perturbation Robustness Testing, M2 Calibrated Organic Dissent Search, M3 Source Purpose Scoring), **Structural Prevention** (M4 VRF Consolidation Selection, M5 Graduated Credibility Ladder, M6 Consolidation Depth Limits), and **Ecological Monitoring** (M7 Immune Memory). A dedicated Novelty Pathway ensures that genuinely paradigmatic discoveries (N3-class) receive enhanced scrutiny rather than dissent-deficit penalization. CRP+ extends the existing C10 5-layer defense-in-depth without replacing any layer, achieving a 30x adversary cost multiplication at 3.7x LLM overhead relative to base consolidation. All accepted K-class quanta enter a 5-rung graduated credibility ladder (SPECULATIVE through CANONICAL) with domain-adaptive uncertainty floors, participation constraints, and explicit promotion/demotion criteria. The system operates within a budget of 55 LLM calls and 565 embedding operations per consolidation cycle, with 42-72% headroom across all resource categories.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Solution Overview](#2-solution-overview)
3. [Architecture](#3-architecture)
4. [M1: Adaptive Perturbation Robustness Testing (APRT)](#4-m1-adaptive-perturbation-robustness-testing-aprt)
5. [M2: Calibrated Organic Dissent Search (CODS)](#5-m2-calibrated-organic-dissent-search-cods)
6. [M3: Source Purpose Scoring](#6-m3-source-purpose-scoring)
7. [M4: VRF Consolidation Selection](#7-m4-vrf-consolidation-selection)
8. [M5: Graduated Credibility Ladder](#8-m5-graduated-credibility-ladder)
9. [M6: Consolidation Depth Limits](#9-m6-consolidation-depth-limits)
10. [M7: Immune Memory](#10-m7-immune-memory)
11. [Novelty Pathway](#11-novelty-pathway)
12. [Cross-Mechanism Integration](#12-cross-mechanism-integration)
13. [Parameters & Configuration](#13-parameters--configuration)
14. [Pseudocode](#14-pseudocode)
15. [Failure Modes & Recovery](#15-failure-modes--recovery)
16. [Conformance Requirements](#16-conformance-requirements)
17. [Appendix A: Formal Requirements Traceability](#appendix-a-formal-requirements-traceability)
18. [Appendix B: Hard Gate Verification Protocols](#appendix-b-hard-gate-verification-protocols)
19. [Appendix C: Adversary Cost Analysis](#appendix-c-adversary-cost-analysis)
20. [Appendix D: C9 Defense Invariant Compliance](#appendix-d-c9-defense-invariant-compliance)
21. [Appendix E: Glossary](#appendix-e-glossary)

---

## 1. Problem Statement

### 1.1 The Consolidation Poisoning Threat

The Atrahasis system's EMA dreaming pipeline (C6 Section 5.3) performs automated cross-domain knowledge synthesis: when the coherence graph develops strong bridging edges between quanta in different domains, a Three-Pass LLM Synthesis produces a new K-class (knowledge) quantum that captures the emergent cross-domain insight. This consolidation process is the system's primary mechanism for generating novel knowledge.

**Consolidation poisoning** is an adversarial strategy in which an attacker plants carefully crafted quanta across two or more domains such that the automated synthesis produces a false or misleading K-class claim. The attacker exploits the synthesis pipeline's reliance on the input quanta: if the planted quanta are sufficiently coherent with each other and sufficiently connected in the coherence graph, the LLM will dutifully synthesize a conclusion that the adversary designed.

A successful consolidation poisoning attack is particularly dangerous because:

1. **Amplification.** A single poisoned K-class claim enters the knowledge graph with the system's own endorsement, influencing downstream reasoning, further consolidation, and credibility assessments.
2. **Persistence.** K-class claims are durable. Unlike raw observations (E-class), they represent synthesized conclusions that persist across epochs and resist natural decay.
3. **Cascade potential.** A poisoned K-class claim can be consolidated with other claims into second-order and third-order knowledge, amplifying the poison at each level.
4. **Stealth.** The attack operates entirely within legitimate system processes. No protocol violation occurs; the adversary simply provides inputs that lead the synthesis to the desired conclusion.

### 1.2 Limitations of Existing Defenses

C10 Hardening Addenda established a 5-layer defense-in-depth for consolidation:

| Layer | Mechanism | What It Catches | What It Cannot Catch |
|---|---|---|---|
| Layer 1: Source Independence | I1/I2/I3 provenance diversity checks | Obvious Sybil attacks; quanta from the same agent or Sentinel cluster | Adversaries who plant quanta through genuinely independent agents across different clusters |
| Layer 2: Adversarial Probing | Counter-hypothesis generation and scoring | Consolidations with obvious alternative explanations | Consolidations where planted quanta suppress alternative explanations by covering all angles |
| Layer 3: Lineage Tracking | Cascade-based credibility reduction | Second-order effects of rejected consolidations | First-order poisoning where the initial consolidation is never challenged |
| Layer 4: Rate Limiting | Per-shard consolidation throughput caps | Flood attacks that attempt many consolidations simultaneously | Low-and-slow attacks that respect rate limits (one poisoned consolidation per cycle is sufficient) |
| Layer 5: Empirical Validation Queue | PENDING_VALIDATION / VALIDATED binary state | Claims that never receive external corroboration | Claims that receive manufactured corroboration from the same adversarial campaign |

**Critical gap:** The existing 5-layer defense has no mechanism to test whether a consolidation conclusion is overdetermined by its evidence (robustness testing), no calibrated assessment of whether the absence of counter-evidence is suspicious (dissent analysis), no unpredictability in which candidates are selected for consolidation (adversary can target specific bridges), no graduated trust system for newly synthesized knowledge (binary validation), and no institutional memory of previously rejected attack patterns (immune memory).

### 1.3 Why This Matters

The EMA dreaming pipeline is the system's creative engine. Hardening it against poisoning without killing genuine discovery is the central design challenge. A naive defense (reject everything unusual) would suppress the very cross-domain insights the system exists to find. CRP+ must simultaneously:

- **Increase** the cost of adversarial consolidation by at least an order of magnitude.
- **Preserve** the acceptance rate for genuinely novel cross-domain discoveries.
- **Graduate** trust in new knowledge rather than applying a binary accept/reject gate.
- **Learn** from past attacks to detect campaign-level adversarial behavior.

---

## 2. Solution Overview

### 2.1 CRP+'s Seven Mechanisms and Novelty Pathway

CRP+ introduces seven defense mechanisms organized along three axes, plus a dedicated pathway for paradigmatic novelty:

**Axis 1: Formation Analysis (pre-/during-consolidation scrutiny)**

| Mechanism | Function | Key Output |
|---|---|---|
| **M1: Adaptive Perturbation Robustness Testing (APRT)** | Tests whether the consolidation conclusion survives input perturbation | `robustness_score` in [0,1] |
| **M2: Calibrated Organic Dissent Search (CODS)** | Classifies novelty tier and measures calibrated dissent deficit | `cods_score` in [0,1], `novelty_tier` in {N1, N2, N3} |
| **M3: Source Purpose Scoring** | Supplementary tie-breaker assessing whether quanta creation contexts naturally lead to the consolidation topic | `purpose_score` in [0, 0.15] |

**Axis 2: Structural Prevention (architectural constraints)**

| Mechanism | Function | Key Output |
|---|---|---|
| **M4: VRF Consolidation Selection** | Unpredictable candidate selection via ECVRF | Selected candidate subset |
| **M5: Graduated Credibility Ladder** | 5-rung trust graduation from SPECULATIVE to CANONICAL | Rung assignment, influence weight |
| **M6: Consolidation Depth Limits** | Participation constraints preventing consolidation-of-consolidation cascades | Eligibility filter |

**Axis 3: Ecological Monitoring (post-consolidation learning)**

| Mechanism | Function | Key Output |
|---|---|---|
| **M7: Immune Memory** | Three-level signature storage and matching for rejected patterns | Match level (L1/L2/L3), enhanced scrutiny trigger |

**Novelty Pathway:** Dedicated scrutiny track for N3 (paradigmatic) claims that replaces dissent-deficit penalization with enhanced APRT, constructive adversarial probing, temporal quarantine, and provenance deep audit.

### 2.2 Defense Philosophy

CRP+ follows three design principles:

1. **Defense in depth, not defense by veto.** No single mechanism decides acceptance or rejection. The combined scoring formula integrates signals from M1, M2, M3, M7, and C10 adversarial probing. An adversary must defeat ALL mechanisms simultaneously.

2. **Calibrated skepticism.** The system's suspicion is calibrated to context. Incremental claims (N1) with no dissent are suspicious; paradigmatic discoveries (N3) with no dissent are expected. The same evidence produces different suspicion levels depending on novelty tier.

3. **Graduated trust.** Acceptance is not endorsement. All accepted K-class claims enter at PROVISIONAL (rung 1) with 25% influence weight and must earn promotion through independent corroboration. Damage from any single poisoned claim that slips through is bounded by its low initial influence.

### 2.3 Relationship to Existing C10 5-Layer Defense

CRP+ **extends** the existing C10 consolidation defense. It does not replace any layer.

| C10 Layer | Status Under CRP+ | How CRP+ Extends It |
|---|---|---|
| Layer 1: Source Independence (I1/I2/I3) | UNCHANGED | Prerequisite to CRP+. CRP+ mechanisms execute only after Layer 1 passes. |
| Layer 2: Adversarial Consolidation Probing | EXTENDED | CRP+ adds M3 tie-breaking when probe results are ambiguous. CODS dissent search provides additional signal to the probe. |
| Layer 3: Consolidation Lineage Tracking | EXTENDED | M5 Credibility Ladder adds rung-based credibility weighting on top of lineage-based cascade. M6 Depth Limits add participation constraints. |
| Layer 4: Consolidation Rate Limiting | UNCHANGED | CRP+ operates within rate limits. M4 VRF selection reduces candidate count before rate limits apply. |
| Layer 5: Empirical Validation Queue | EXTENDED | M5 replaces the flat PENDING_VALIDATION / VALIDATED binary with a 5-rung graduated system. Promotion criteria are more granular than the original binary. |

---

## 3. Architecture

### 3.1 Position in the Atrahasis Stack

CRP+ is a **consolidation-defense layer** that wraps the EMA dreaming pipeline (C6 Section 5.3). It instruments the existing consolidation process at five insertion points within the dreaming lifecycle:

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
    |   +-- (1)  Candidate Identification ... [M4 VRF Selection REPLACES deterministic]
    |   +-- (2)  Provenance Diversity ....... [C10 Layer 1: unchanged, prerequisite]
    |   +-- (3)  Source Independence ........ [C10 Layer 1: unchanged, prerequisite]
    |   +-- (4)  Consolidation Lock ......... [C6 base: unchanged]
    |   +-- (5)  Three-Pass LLM Synthesis ... [C6 base: unchanged]
    |   +-- (6)  ** M7 Immune Memory ** ..... [NEW: check against rejected signatures]
    |   +-- (7)  ** M1 APRT ** ............. [NEW: post-synthesis robustness testing]
    |   +-- (8)  ** M2 CODS ** ............. [NEW: calibrated dissent search]
    |   +-- (9)  C10 Adversarial Probing .... [EXTENDED: CRP+ adds M3 tie-breaker]
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

### 3.2 Data Flow: Single Consolidation Candidate

```
identify_candidates(shard, epoch)
         |
         v
    M4: VRF Selection --- filter candidates by VRF output
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
    M7: Immune Memory Check --- does C match a rejected signature?
         |                       YES (L1) --> AUTOMATIC REJECT
         |                       YES (L2) --> enhanced scrutiny path
         |                       YES (L3) --> standard + suspicion boost
         |                       NO  --> standard path
         v
    M1 APRT: Perturbation Robustness Testing
         |  Tier 1: embedding-based influence screening
         |  Tier 2: targeted re-synthesis (Cases A/B/C)
         |  Output: robustness_score in [0, 1]
         v
    M2 CODS: Novelty Classification --> Dissent Search --> Dissent Deficit
         |  Output: cods_score in [0, 1], novelty_tier in {N1, N2, N3}
         |
         +-- IF novelty_tier == N3 --> BRANCH to Novelty Pathway (Section 11)
         v
    C10 Layer 2: Adversarial Consolidation Probing
         |  Output: probe_relative_strength in [0, 1]
         v
    M3: Source Purpose Scoring (CONDITIONAL)
         |  Invoked ONLY if combined signals are ambiguous
         |  Output: purpose_score in [0, 0.15]
         v
    Combined CRP+ Scoring --> ACCEPT / REJECT / QUARANTINE
         |
         v  [REJECT --> store signature in M7 immune memory]
         v  [QUARANTINE --> hold for manual review]
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

### 3.3 System Invariants

The following invariants MUST hold at all times. Violation of any invariant constitutes a conformance failure.

- **INV-CRP1 (VRF Unpredictability):** No agent can predict which consolidation candidates will be selected in epoch E+2 during epoch E. Guaranteed by ECVRF one-epoch-ahead unpredictability (C3 Section 5.2.1).

- **INV-CRP2 (APRT Completeness):** Every consolidation candidate that passes synthesis MUST undergo at least Tier 1 APRT screening. No exceptions.

- **INV-CRP3 (CODS Calibration):** Dissent deficit weight MUST be calibrated by novelty tier. N3 claims MUST NOT be penalized for dissent deficit (dissent weight = 0.1).

- **INV-CRP4 (Credibility Monotonicity):** A quantum's credibility rung can only increase through explicit promotion criteria or decrease through explicit demotion criteria. No mechanism may set a rung directly without satisfying the criteria for that rung.

- **INV-CRP5 (Depth Enforcement):** PROVISIONAL and SPECULATIVE K-class quanta MUST NOT participate in further consolidation. This is enforced at candidate identification time, before any LLM cost is incurred.

- **INV-CRP6 (Immune Memory Bounded):** Total active immune memory signatures per shard MUST NOT exceed `MAX_IMMUNE_SIGNATURES` (1000). Garbage collection MUST run every epoch.

- **INV-CRP7 (Novelty Pathway Isolation):** N3 claims on the Novelty Pathway MUST NOT bypass APRT. They receive enhanced (full leave-one-out) APRT, not reduced APRT.

- **INV-CRP8 (M3 Cap):** Source Purpose Scoring MUST NOT contribute more than 0.15 to the combined CRP+ score under any circumstance.

---

## 4. M1: Adaptive Perturbation Robustness Testing (APRT)

### 4.1 Purpose

APRT answers the question: "Would this consolidation conclusion still be reached if the input quanta were different?" A robust consolidation is one where the conclusion is overdetermined by the evidence — removing any single quantum, or any suspicious cluster, does not change the result. A fragile consolidation depends on specific quanta, which may be adversarially planted.

### 4.2 Integration Point

APRT executes immediately after Three-Pass LLM Synthesis (C6 Section 5.3.4) and the M7 Immune Memory check. It receives:

- The candidate consolidation claim `C` (text)
- The contributing quanta set `Q = {q1, q2, ..., qN}`
- The synthesis context (prompt templates, temperature, etc.)
- The immune memory match result (determines standard vs. enhanced mode)

It produces:

- `robustness_score` in [0.0, 1.0]
- `aprt_case` in {A, B, C}
- `flagged_quanta` (list of quantum IDs with anomalous influence)
- `flagged_clusters` (list of quantum ID sets forming suspicious clusters)
- `resynthesis_count` (number of Tier 2 re-syntheses performed)

### 4.3 Tier 1: Embedding Influence Gradient Screening

#### 4.3.1 Embedding Computation

Each quantum `qi` and the consolidation claim `C` are embedded into a shared vector space using the system's embedding model (same model used for coherence graph similarity computations in C6).

```
emb(qi) = embed(qi.content.claim_text)    for each qi in Q
emb(C)  = embed(C.text)
```

**REQ-M1-001:** The embedding model used for APRT MUST be the same model used for coherence graph similarity in C6. Using a different model would create inconsistencies between influence scoring and graph topology.

#### 4.3.2 Influence Score Computation

For each quantum `qi`, compute two sub-scores:

**Relevance:** Cosine similarity between `qi` and the consolidation conclusion `C`.

```
relevance(qi) = cosine_similarity(emb(qi), emb(C))
```

**Uniqueness:** How much unique information does `qi` provide relative to other quanta in Q?

```
redundancy(qi) = max_{j != i} cosine_similarity(emb(qi), emb(qj))
uniqueness(qi) = 1.0 - redundancy(qi)
```

**Composite Influence:**

```
influence(qi) = relevance(qi) * uniqueness(qi)
```

A quantum with high influence is both highly relevant to the conclusion AND provides information no other quantum provides. This is the signature of a load-bearing quantum.

**REQ-M1-002:** Influence scores MUST be computed for ALL quanta in Q. Partial computation is not permitted.

**REQ-M1-003:** The influence computation MUST use the composite formula `relevance * uniqueness`. Neither sub-score alone is sufficient (high relevance without uniqueness is benign redundancy; high uniqueness without relevance is irrelevant noise).

#### 4.3.3 Anomaly Detection

Compute the mean and standard deviation of influence scores across Q:

```
mu_inf = mean(influence(qi) for qi in Q)
sigma_inf = std(influence(qi) for qi in Q)
```

**High-Influence Flag:** Any quantum with `influence(qi) > mu_inf + HIGH_INFLUENCE_SIGMA * sigma_inf` is flagged, where `HIGH_INFLUENCE_SIGMA` = 2.0 (default).

**Redundant Cluster Detection:** Group quanta by pairwise cosine similarity. Two quanta are in the same cluster if `cosine_similarity(emb(qi), emb(qj)) > REDUNDANT_CLUSTER_SIMILARITY` (default 0.85). A cluster of `REDUNDANT_CLUSTER_MIN_SIZE` (default 3) or more quanta that are all relevant to C (`relevance > 0.5`) is flagged as a suspicious redundant cluster.

**REQ-M1-004:** Anomaly detection MUST use the statistical threshold `mu + k*sigma` with `k = HIGH_INFLUENCE_SIGMA`. Fixed thresholds are prohibited because influence distributions vary by domain density.

**REQ-M1-005:** Redundant cluster detection MUST require both high pairwise similarity (> `REDUNDANT_CLUSTER_SIMILARITY`) AND relevance to C (> 0.5). Clusters of irrelevant quanta are not suspicious.

#### 4.3.4 Case Classification

Based on Tier 1 results, classify into one of three cases:

| Case | Condition | Interpretation | Tier 2 Action |
|------|-----------|----------------|---------------|
| **A** | >= 1 quantum flagged as high-influence | Specific quanta are load-bearing | Test their removal (1-3 re-syntheses) |
| **B** | No high-influence flags BUT >= 1 redundant cluster detected | Redundant poisoning pattern | Test cluster removal (1-2 re-syntheses) |
| **C** | No flags, no clusters; influence is uniformly distributed | Organic pattern | Single random-subset check (1 re-synthesis) |

**REQ-M1-006:** Case classification MUST follow the priority order A > B > C. If both high-influence flags and clusters are detected, Case A takes priority (the high-influence quanta are the more actionable signal).

### 4.4 Tier 2: Targeted Re-Synthesis

#### 4.4.1 Case A: High-Influence Quantum Testing

For each flagged quantum `qi_flagged` (capped at 3):

1. Construct reduced set `Q' = Q \ {qi_flagged}`
2. Re-run Three-Pass LLM Synthesis on `Q'` with identical parameters
3. Compare re-synthesized claim `C'` with original claim `C`:
   - `stability(qi_flagged) = semantic_similarity(C, C')`
   - If `stability < STABILITY_THRESHOLD` (0.70): the conclusion depends on this quantum

**Robustness score (Case A):**

```
robustness_A = min(stability(qi_flagged) for qi_flagged in flagged_quanta[:3])
```

**REQ-M1-007:** Case A re-synthesis MUST cap at 3 flagged quanta. If more than 3 are flagged, test the top 3 by influence score (descending).

**REQ-M1-008:** Re-synthesis MUST use identical synthesis parameters (prompt template, temperature, model) as the original synthesis.

#### 4.4.2 Case B: Redundant Cluster Testing

For each flagged cluster `Ck` (capped at 2):

1. Construct reduced set `Q' = Q \ Ck` (remove entire cluster)
2. If `|Q'| < 3`: assign `stability(Ck) = 0.0` (cluster IS the consolidation)
3. Else: re-run Three-Pass LLM Synthesis on `Q'` and compare: `stability(Ck) = semantic_similarity(C, C')`

**Robustness score (Case B):**

```
robustness_B = min(stability(Ck) for Ck in flagged_clusters[:2])
```

**REQ-M1-009:** If removing a cluster leaves fewer than 3 quanta, the stability MUST be set to 0.0. Synthesis requires a minimum of 3 input quanta.

#### 4.4.3 Case C: Random Subset Sanity Check

1. Randomly remove 30% of quanta (VRF-selected subset for reproducibility)
2. Re-run synthesis on the remaining 70%
3. Compare: `stability_random = semantic_similarity(C, C')`

**Robustness score (Case C):**

```
robustness_C = stability_random
```

**REQ-M1-010:** The random subset selection in Case C MUST use a VRF-derived seed (not a PRNG seed) to ensure reproducibility and verifiability. Seed construction: `SHA256(C.text || "APRT_RANDOM")`.

#### 4.4.4 Semantic Similarity for Stability Comparison

The stability comparison uses embedding cosine similarity between the original claim C and the re-synthesized claim C':

```
semantic_similarity(C, C') = cosine_similarity(embed(C.text), embed(C'.text))
```

Threshold interpretation:

| Range | Interpretation |
|---|---|
| >= 0.90 | Conclusion essentially unchanged (robust) |
| 0.70 - 0.89 | Conclusion modified but structurally similar (moderate) |
| < 0.70 | Conclusion substantially changed (fragile) |

**REQ-M1-011:** Semantic similarity MUST use embedding cosine similarity, not string-level comparison. Semantically equivalent but differently-worded claims must score high.

### 4.5 Robustness Score Summary

The final APRT robustness score is determined by whichever case applies:

```
robustness_score = robustness_A  if case == A
                 = robustness_B  if case == B
                 = robustness_C  if case == C
```

Interpretation for combined scoring:

| Range | Level | Meaning |
|---|---|---|
| >= 0.85 | HIGH | Consolidation is overdetermined |
| 0.60 - 0.84 | MODERATE | Proceed with caution |
| < 0.60 | LOW | Consolidation is fragile; likely poisoned or artifactual |

### 4.6 APRT Enhanced Mode

When triggered by M7 immune memory L2 match or N3 Novelty Pathway entry:

- Skip Tier 1 case classification
- Run full leave-one-out on ALL quanta (not just flagged ones)
- Robustness score = minimum stability across all leave-one-out tests

```
robustness_enhanced = min(stability(qi) for qi in Q)
```

Cost: N re-syntheses. Justified only for the ~10% of candidates that trigger enhanced mode.

**REQ-M1-012:** Enhanced APRT MUST perform full leave-one-out on every quantum in Q. Partial leave-one-out in enhanced mode is a conformance violation.

**REQ-M1-013:** Enhanced APRT MUST be triggered for ALL L2 immune memory matches and ALL Novelty Pathway entries. Skipping enhanced mode for these categories is a conformance violation.

---

## 5. M2: Calibrated Organic Dissent Search (CODS)

### 5.1 Purpose

CODS answers: "Is the absence of counter-evidence suspicious?" For incremental claims in well-mapped domains, zero counter-evidence is a red flag (genuine patterns always have dissenters). For paradigmatic novelty, zero counter-evidence is expected. CODS calibrates the dissent signal by novelty tier, preventing the system from penalizing genuine discoveries for lacking opposition.

### 5.2 Integration Point

CODS executes after APRT and before Adversarial Consolidation Probing. It receives:

- The candidate consolidation claim `C`
- The contributing quanta `Q`
- The coherence graph context (existing cross-domain edges, domain metadata)
- The shard's knowledge base for dissent search

It produces:

- `novelty_tier` in {N1, N2, N3}
- `dissent_items` (list of contradicting/alternative quanta found)
- `dissent_deficit` in [0.0, 1.0] (0 = abundant dissent, 1 = no dissent found)
- `cods_score` in [0.0, 1.0] (calibrated score; higher = more suspicious)

### 5.3 Step 1: Novelty Tier Classification

#### 5.3.1 Feature Extraction

Extract three features from the consolidation candidate:

**F1: Domain Overlap with Existing Cross-Domain Edges**

Identify the domains bridged by the consolidation. Query the coherence graph for existing ANALOGY edges between those domains.

```
domains_bridged = extract_domains(Q)  # typically 2-3 domains
existing_bridges = count_analogy_edges(domain_a, domain_b, coherence_graph)
expected_bridges = sqrt(|domain_a| * |domain_b|) * BRIDGE_DENSITY_FACTOR
domain_overlap = existing_bridges / max(1, expected_bridges)
```

Where `BRIDGE_DENSITY_FACTOR` = 0.01 (default).

**REQ-M2-001:** Domain overlap MUST be computed as a ratio of existing bridges to expected bridges. Raw bridge count is meaningless without normalization by domain size.

**F2: Semantic Distance from Nearest Existing Consolidation**

```
nearest_K = argmin_{K in active_K_class} cosine_distance(embed(C.text), embed(K.content.claim_text))
semantic_distance = cosine_distance(embed(C.text), embed(nearest_K.content.claim_text))
```

If no active K-class quanta exist, `semantic_distance = 1.0`.

**REQ-M2-002:** If the shard contains zero active K-class quanta, semantic distance MUST default to 1.0 (maximum novelty).

**F3: Precedent Count**

```
precedent_count = count_prior_consolidation_attempts(domain_a, domain_b, lookback_epochs=500)
```

**REQ-M2-003:** Precedent count lookback window MUST be 500 epochs. Both successful and failed consolidation attempts count.

#### 5.3.2 Tier Classification Rules

| Tier | Condition | Interpretation |
|------|-----------|----------------|
| **N1 (Incremental)** | `domain_overlap >= 0.3` OR `precedent_count >= 3` OR `semantic_distance < 0.4` | Extends known cross-domain connections |
| **N2 (Bridging)** | `0.05 <= domain_overlap < 0.3` OR `1 <= precedent_count < 3` OR `0.4 <= semantic_distance < 0.7` | Connects domains with some documented proximity |
| **N3 (Paradigmatic)** | `domain_overlap < 0.05` AND `precedent_count == 0` AND `semantic_distance >= 0.7` | Genuinely novel — no prior relationship documented |

**REQ-M2-004:** When features span multiple tiers, the MOST NOVEL tier among the three features determines the classification. This errs on the side of protecting genuine novelty.

**REQ-M2-005:** N3 classification requires ALL THREE conditions simultaneously (`domain_overlap < 0.05` AND `precedent_count == 0` AND `semantic_distance >= 0.7`). Any single condition failing prevents N3 classification.

**REQ-M2-006 (Sparse Domain Safeguard):** If either domain has fewer than 10 active quanta, the classification MUST be capped at N2. This prevents sparse-domain artifacts from triggering the Novelty Pathway.

### 5.4 Step 2: Dissent Search

#### 5.4.1 Query Generation

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

**REQ-M2-007:** Dissent search MUST generate at least 4 distinct query types (negation, alternative, counter-evidence, limitation). Fewer query types risk missing dissent that exists in the knowledge base.

#### 5.4.2 Dissent Item Scoring

For each retrieved quantum `d` that appears to contradict or provide an alternative to `C`:

```
dissent_relevance = cosine_similarity(embed(d.content.claim_text), embed(C.text))
dissent_strength  = assess_contradiction_strength(d, C)  # LLM call, returns [0,1]
dissent_organic   = 1.0 if d.provenance.generation_epoch < C.generation_epoch
                    else 0.5  # Pre-existing dissent is more credible

dissent_quality(d) = dissent_relevance * dissent_strength * dissent_organic
```

**REQ-M2-008:** Dissent items that predate the consolidation candidate (`generation_epoch < C.generation_epoch`) MUST receive the full organic multiplier (1.0). Dissent generated after the candidate receives a reduced multiplier (0.5) because it may be reactive rather than independent.

**REQ-M2-009:** The `assess_contradiction_strength()` call MUST use a SEPARATE LLM instance from the consolidation LLM to prevent adversarial co-adaptation.

#### 5.4.3 Dissent Deficit Computation

```
total_dissent = sum(dissent_quality(d) for d in dissent_items)
dissent_deficit = max(0.0, 1.0 - total_dissent / EXPECTED_DISSENT_LEVEL)
```

Where `EXPECTED_DISSENT_LEVEL` = 1.5. This is calibrated so that 1-2 strong dissent items bring the deficit to zero.

**REQ-M2-010:** `EXPECTED_DISSENT_LEVEL` MUST be set so that 1-2 strong dissent items (quality >= 0.75 each) reduce the deficit to 0. The default value of 1.5 satisfies this constraint.

### 5.5 Step 3: Novelty-Calibrated CODS Score

```
dissent_weight = {N1: 1.0, N2: 0.5, N3: 0.1}[novelty_tier]
cods_score = dissent_deficit * dissent_weight
```

Interpretation:

| Range | Level | Meaning |
|---|---|---|
| >= 0.7 | HIGH | Strong dissent deficit in a domain where dissent is expected |
| 0.3 - 0.69 | MODERATE | Moderate suspicion |
| < 0.3 | LOW | Either dissent was found or novelty calibration reduces concern |

**REQ-M2-011:** If `novelty_tier == N3`, the claim MUST be routed to the Novelty Pathway (Section 11) regardless of CODS score. The CODS score is recorded but does not contribute to the combined scoring formula for N3 claims.

**REQ-M2-012:** Dissent weights MUST follow the tier mapping: N1 = `DISSENT_WEIGHT_N1` (1.0), N2 = `DISSENT_WEIGHT_N2` (0.5), N3 = `DISSENT_WEIGHT_N3` (0.1). These are operational parameters.

---

## 6. M3: Source Purpose Scoring

### 6.1 Purpose

M3 is a supplementary tie-breaker that assesses whether each contributing quantum's creation context naturally leads to the consolidation topic. In genuine cross-domain discovery, most quanta were created for domain-specific reasons and their cross-domain relevance is emergent — they have LOW purpose alignment with the consolidation. In adversarial planting, quanta are specifically crafted to drive the target conclusion — they have HIGH purpose alignment.

### 6.2 Invocation Conditions

M3 is NOT evaluated by default. It is invoked ONLY when the following ambiguity condition holds:

```
ambiguity = (0.40 <= robustness_score <= 0.75)
        AND (0.25 <= cods_score <= 0.65)
        AND (0.35 <= probe_relative_strength <= 0.65)
```

This means APRT, CODS, and Adversarial Probing all returned borderline results. M3 breaks the tie. Estimated invocation rate: ~20% of consolidation candidates.

**REQ-M3-001:** M3 MUST NOT be invoked unless all three ambiguity conditions hold simultaneously. Invoking M3 outside the ambiguity window is a conformance violation.

**REQ-M3-002:** M3 MUST NOT be invoked for N3 claims on the Novelty Pathway. N3 claims bypass the standard combined scoring formula entirely.

### 6.3 Scoring Algorithm

When invoked, M3 evaluates whether each contributing quantum's creation context naturally leads to the consolidation topic:

```python
def compute_purpose_score(claim_C, quanta_Q):
    """
    For each quantum, assess whether its creation purpose
    naturally connects to the consolidation topic.
    Uses a SEPARATE evaluator model (not the consolidation LLM).
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

    high_purpose_count = sum(1 for s in purpose_scores if s > M3_HIGH_PURPOSE_THRESHOLD)
    high_purpose_fraction = high_purpose_count / len(purpose_scores)

    # purpose_suspicion: higher = more suspicious
    purpose_suspicion = high_purpose_fraction

    return min(purpose_suspicion, M3_MAX_CONTRIBUTION)  # Hard cap at 0.15
```

**REQ-M3-003:** M3 MUST use a SEPARATE evaluator model from the consolidation LLM to prevent adversarial co-adaptation.

**REQ-M3-004:** The M3 output MUST be hard-capped at `M3_MAX_CONTRIBUTION` (0.15). This cap MUST be enforced in code with a `min()` operation, not merely documented.

**REQ-M3-005:** The high-purpose threshold MUST be `M3_HIGH_PURPOSE_THRESHOLD` (0.80). Quanta with purpose alignment above this threshold are counted as suspiciously well-targeted.

### 6.4 Integration with Final Decision

The purpose score (0 to 0.15) is ADDED to the combined CRP+ suspicion score only when invoked. See Section 12.1 for the full scoring formula.

---

## 7. M4: VRF Consolidation Selection

### 7.1 Purpose

Instead of deterministically selecting ALL cross-domain bridge candidates for consolidation, M4 uses VRF-based random selection. This forces an adversary to plant patterns across many more bridges than they want consolidated, because they cannot predict which bridges will be selected in any given cycle.

### 7.2 VRF Seed Construction

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

**REQ-M4-001:** The VRF input MUST include the `"CRP_CONSOLIDATION_SELECT"` domain separator prefix to prevent cross-domain VRF output reuse with C3 committee selection or any other VRF application.

**REQ-M4-002:** The VRF input MUST include the `previous_consolidation_hash` to chain consolidation cycles and prevent multi-epoch prediction.

**REQ-M4-003:** The VRF proof `pi` MUST be stored alongside each consolidation decision record, enabling any party to verify the selection was honest.

### 7.3 Selection Probability Formula

For each candidate bridge `b` identified by `identify_consolidation_candidates()` (C6 Section 5.3.1):

```
selection_hash = SHA256(beta || bridge_id(b))
selection_value = uint256(selection_hash) / 2^256    # in [0, 1)

bridge_strength(b) = mean(edge.weight for edge in b.connecting_edges)

base_rate = VRF_SELECTION_RATE    # Default: 0.10 (10%)

adjusted_threshold = base_rate * (0.5 + bridge_strength(b))
# Strong bridges (strength ~1.0) have ~1.5x base rate
# Weak bridges (strength ~0.0) have ~0.5x base rate

selected = (selection_value < adjusted_threshold)
```

**REQ-M4-004:** The `adjusted_threshold` formula MUST be `base_rate * (0.5 + bridge_strength)`. This ensures that the weakest bridges have 0.5x base rate and the strongest have 1.5x, providing strength-biased but not strength-dominated selection.

**REQ-M4-005:** `bridge_strength` MUST be computed as the mean weight of connecting edges. If a candidate has no connecting edges (degenerate case), default to 0.5.

### 7.4 Coverage Guarantee

Over time, every bridge will eventually be selected. The expected number of epochs until bridge `b` is selected:

```
E[epochs_until_selected(b)] = 1 / adjusted_threshold(b)
```

| Bridge Strength | Adjusted Threshold | Expected Wait (epochs) |
|---|---|---|
| ~0.0 (weakest) | 0.10 * 0.5 = 0.05 | ~20 |
| ~0.5 (average) | 0.10 * 1.0 = 0.10 | ~10 |
| ~1.0 (strongest) | 0.10 * 1.5 = 0.15 | ~7 |

**Anti-starvation boost:** If a bridge has not been selected in 20 epochs, its threshold is boosted by 0.01 per additional epoch. After 30 epochs, the threshold doubles. After 40 epochs, selection is forced regardless of VRF output.

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

**REQ-M4-006:** The anti-starvation mechanism MUST force selection of any bridge that has not been selected in 40 or more epochs. This is a hard guarantee, not probabilistic.

**REQ-M4-007:** The coverage boost MUST NOT apply to bridges that are fewer than 20 epochs old (newly created bridges).

### 7.5 Adversary Cost Multiplication

Without VRF selection: adversary plants 1 bridge, it is guaranteed to be consolidated next cycle.

With VRF selection at 10%: adversary must plant ~10 bridges to have one selected per cycle, and cannot predict which.

Combined with M1 APRT (which may detect the planted bridge even when selected), the adversary must plant ~10 bridges x ~3 attempts per bridge (accounting for APRT detection) = ~30 planted bridges for one successful poisoning. This is a **30x cost multiplication** over the base system.

**REQ-M4-008:** `VRF_SELECTION_RATE` is a constitutional parameter requiring G-class governance supermajority (C3) to change. The default of 0.10 provides 10x selection unpredictability.

### 7.6 Integration with C3 VRF Infrastructure

CRP+ reuses the ECVRF infrastructure from C3 Section 5.2.1. The same key pairs used for committee selection are used for consolidation selection. The VRF input domain is separated by the `"CRP_CONSOLIDATION_SELECT"` prefix.

**REQ-M4-009:** CRP+ MUST reuse C3's ECVRF key pairs. Separate key generation for consolidation selection is prohibited (it would fragment key management).

---

## 8. M5: Graduated Credibility Ladder

### 8.1 Purpose

M5 replaces the C10 Layer 5 binary PENDING_VALIDATION / VALIDATED model with a 5-rung graduated credibility system. All K-class quanta produced by dreaming consolidation enter at the lowest applicable rung and must earn promotion through accumulating independent corroboration. This bounds the damage from any single poisoned claim that passes CRP+ screening.

### 8.2 Rung Definitions

| Rung | Name | Uncertainty Floor | Promotion Criteria | Influence Weight |
|------|------|-------------------|-------------------|------------------|
| 0 | SPECULATIVE | u >= 0.80 | Created by sandboxed K->K consolidation (M6). Cannot promote directly; must wait for inputs to reach CORROBORATED. | 0.00 (no influence) |
| 1 | PROVISIONAL | u >= 0.50 | Default for all K-class from dreaming. | 0.25 |
| 2 | CORROBORATED | u >= 0.30 | >= 1 DIRECT E-class corroboration from independent agent (different agent, different Sentinel cluster, created after the K-class claim). | 0.50 |
| 3 | ESTABLISHED | u >= 0.15 | >= 3 corroborations including >= 1 from a different parcel + >= 50 epochs at CORROBORATED without failed challenges. | 0.75 |
| 4 | CANONICAL | u >= 0.05 | >= 5 corroborations from >= 3 parcels + >= 200 epochs at ESTABLISHED + zero failed challenges during ESTABLISHED tenure. | 1.00 |

**REQ-M5-001:** All K-class quanta from standard dreaming consolidation MUST enter at rung 1 (PROVISIONAL). No mechanism may assign a higher initial rung.

**REQ-M5-002:** Rung 0 (SPECULATIVE) is EXCLUSIVELY for products of sandboxed K->K consolidation (M6). Normal consolidation products MUST NOT be assigned rung 0.

**REQ-M5-003:** Influence weights MUST be applied multiplicatively to all downstream contributions: `effective_contribution(q) = raw_contribution(q) * influence_weight(q.rung)`.

### 8.3 Credibility-Weighted Influence Formula

When a K-class quantum participates in any downstream process (further consolidation, credibility scoring, coherence graph weighting), its contribution is multiplied by its influence weight:

```
effective_contribution(q) = raw_contribution(q) * influence_weight(q.rung)
```

This means PROVISIONAL claims have only 25% of the influence they would otherwise have. The system "hears" them but does not "trust" them until corroboration arrives.

### 8.4 Promotion Protocol

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

    # Fast-track check
    multi_modal_count = count_distinct_evidence_modalities(corroborations)
    fast_track_eligible = (multi_modal_count >= FAST_TRACK_MODALITIES  # 3
                          and epochs_at_current_rung >= 2  # 2-cycle minimum
                          and failed_challenges == 0)

    # SPECULATIVE -> PROVISIONAL (M6 sandbox promotion)
    if current_rung == 0:
        input_quanta = lineage.get_inputs(quantum.id)
        if all(q.credibility_rung >= 2 for q in input_quanta):
            return promote(quantum, rung=1, epoch=epoch)
        return None

    # PROVISIONAL -> CORROBORATED
    if current_rung == 1:
        if quantum.quarantine_flag and epoch < quantum.quarantine_end_epoch:
            return None  # Quarantined claims cannot promote
        if len(direct_corroborations) >= 1:
            return promote(quantum, rung=2, epoch=epoch)
        return None

    # CORROBORATED -> ESTABLISHED
    if current_rung == 2:
        if fast_track_eligible:
            return promote(quantum, rung=3, epoch=epoch)
        if (len(direct_corroborations) >= 3
                and len(cross_parcel_corroborations) >= 1
                and epochs_at_current_rung >= 50
                and failed_challenges == 0):
            return promote(quantum, rung=3, epoch=epoch)
        return None

    # ESTABLISHED -> CANONICAL
    if current_rung == 3:
        if (len(direct_corroborations) >= 5
                and distinct_parcels >= 3
                and epochs_at_current_rung >= 200
                and failed_challenges == 0):
            return promote(quantum, rung=4, epoch=epoch)
        return None

    return None  # CANONICAL: no further promotion
```

**REQ-M5-004:** Corroborations MUST be DIRECT (explicit E-class observation confirming the K-class claim), from an independent agent (different agent ID AND different Sentinel cluster), and created AFTER the K-class claim's generation epoch.

**REQ-M5-005:** Quarantined claims (N3 pathway) MUST NOT be promoted during the quarantine period, even if corroboration criteria are met. Corroborations are counted but promotion is deferred.

**REQ-M5-006:** The fast-track provision MUST require >= `FAST_TRACK_MODALITIES` (3) distinct evidence modalities, a minimum of 2 epochs at the current rung, and zero failed challenges. Fast-track skips the 50-epoch tenure requirement for CORROBORATED -> ESTABLISHED but not the corroboration count.

**REQ-M5-007:** ESTABLISHED -> CANONICAL promotion MUST require >= 5 corroborations from >= 3 distinct parcels, >= 200 epochs at ESTABLISHED, and zero failed challenges. There is no fast-track for CANONICAL promotion.

### 8.5 Demotion Conditions

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
    remaining = [c for c in quantum.corroborations
                 if c.id != revoked_corroboration.id]
    required = rung_requirements(quantum.credibility_rung)
    if not meets_requirements(remaining, required):
        quantum.credibility_rung -= 1
        quantum.rung_promotion_epoch = epoch
```

**D3: Consolidation Cascade.** If a K-class quantum contributed to a consolidation that fails (C10 Section 3.3 cascade), the quantum receives a challenge equivalent. If 2+ cascade events occur, demotion is triggered.

**REQ-M5-008:** Demotion MUST never go below PROVISIONAL (rung 1) for quanta that entered through normal dreaming. SPECULATIVE (rung 0) is reserved exclusively for sandboxed K->K products.

**REQ-M5-009:** D3 cascade demotion MUST require 2 or more cascade events hitting the same quantum. A single cascade event is logged but does not trigger demotion.

**REQ-M5-010:** On demotion, the `rung_promotion_epoch` MUST be reset to the current epoch. The tenure clock restarts from zero.

### 8.6 Domain-Adaptive Threshold Calibration

Uncertainty floor thresholds adapt to domain density:

```python
def calibrated_thresholds(domain, epoch):
    """Compute domain-adaptive uncertainty floors."""
    density = count_active_quanta(domain) / max(1, domain_area(domain))
    density_factor = sigmoid(density, midpoint=100, steepness=0.02)

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

**REQ-M5-011:** PROVISIONAL uncertainty floor MUST be fixed at 0.50 regardless of domain density. Domain adaptation applies only to rungs 2-4.

**REQ-M5-012:** Domain-adaptive thresholds MUST use the sigmoid/lerp formulation. Dense domains receive tighter floors; sparse domains receive relaxed floors.

### 8.7 Integration with C10 Layer 5

M5 REPLACES the flat PENDING_VALIDATION / VALIDATED binary from C10 Layer 5:

| C10 Layer 5 State | M5 Equivalent |
|---|---|
| PENDING_VALIDATION (u >= 0.40) | PROVISIONAL (rung 1, u >= 0.50) — stricter |
| VALIDATED (u >= 0.10) | ESTABLISHED (rung 3, u >= 0.15) — comparable |

The C10 `EmpiricalValidationQueue` data structure is retained but its `uncertainty_floor` field is now computed from the M5 rung.

**REQ-M5-013:** The C10 `EmpiricalValidationQueue` data structure MUST be retained for backward compatibility. The `uncertainty_floor` field MUST be derived from the M5 rung and domain-adaptive calibration.

---

## 9. M6: Consolidation Depth Limits

### 9.1 Purpose

M6 prevents poisoned consolidation-of-consolidation cascades. Without depth limits, a single poisoned K-class claim could be consolidated with other claims into a second-order K-class claim, which could be consolidated again, amplifying the poison at each level.

### 9.2 Input Weight by Rung

When `identify_consolidation_candidates()` (C6 Section 5.3.1) considers K-class quanta as potential inputs to new consolidations:

| Rung | Participation Allowed | Input Weight |
|------|----------------------|--------------|
| SPECULATIVE (0) | NO — excluded from all consolidation | 0.00 |
| PROVISIONAL (1) | NO — excluded from all consolidation | 0.00 |
| CORROBORATED (2) | YES, with reduced weight | 0.50 |
| ESTABLISHED (3) | YES, full weight | 1.00 |
| CANONICAL (4) | YES, full weight | 1.00 |

**REQ-M6-001:** SPECULATIVE and PROVISIONAL K-class quanta MUST be excluded from consolidation candidate sets. This is INV-CRP5.

**REQ-M6-002:** CORROBORATED K-class quanta MUST participate with input weight 0.50.

**REQ-M6-003:** ESTABLISHED and CANONICAL K-class quanta participate with full weight (1.00).

### 9.3 Enforcement Point

Depth limit enforcement occurs at the earliest possible point: during candidate identification, before any LLM synthesis cost is incurred.

```python
def filter_by_depth_limits(candidate_quanta):
    eligible = []
    for q in candidate_quanta:
        if q.claim_class != "K":
            eligible.append(q)
            continue
        if q.credibility_rung <= 1:
            continue  # INV-CRP5
        if q.credibility_rung == 2:
            q.consolidation_input_weight = 0.50
            eligible.append(q)
        else:
            q.consolidation_input_weight = 1.00
            eligible.append(q)
    return eligible
```

**REQ-M6-004:** Depth limit filtering MUST occur during candidate identification, BEFORE synthesis.

**REQ-M6-005:** Non-K-class quanta (E, D, S, etc.) MUST NOT be subject to depth limit filtering.

### 9.4 K->K Sandboxed Consolidation

K->K consolidation is permitted in a sandboxed environment:

```python
def sandboxed_kk_consolidation(candidate):
    k_inputs = [q for q in candidate.quanta if q.claim_class == "K"]

    if not all(q.credibility_rung >= 1 for q in k_inputs):
        return REJECT("SPECULATIVE inputs cannot participate")

    claims = execute_llm_synthesis(candidate)

    for claim in claims:
        claim.credibility_rung = 0  # SPECULATIVE
        claim.sandbox_flag = True
        claim.sandbox_input_ids = [q.id for q in k_inputs]
        claim.uncertainty_floor = 0.80
        claim.isolation_constraints = FULL_SANDBOX

    return claims
```

**FULL_SANDBOX constraints** — SPECULATIVE claims MUST NOT:
- Participate in further consolidation (even sandboxed)
- Influence credibility scoring of non-sandboxed quanta
- Be cited by non-sandboxed processes

**Sandbox lifecycle:**
- If ALL input K-class claims reach CORROBORATED within `SANDBOX_TIMEOUT_CYCLES` (10) cycles: sandbox product is promoted to PROVISIONAL.
- If ANY input K-class claim is rejected or remains PROVISIONAL for > 10 cycles: sandbox product is archived.

**REQ-M6-006:** Sandboxed K->K products MUST be assigned rung 0 (SPECULATIVE) with uncertainty floor 0.80 and FULL_SANDBOX isolation.

**REQ-M6-007:** SPECULATIVE inputs (rung 0) MUST NOT participate in sandboxed consolidation. Only PROVISIONAL-or-above K-class claims may be sandbox inputs.

**REQ-M6-008:** Sandbox timeout MUST be `SANDBOX_TIMEOUT_CYCLES` (10) consolidation cycles. Expired products MUST be archived, not deleted.

**REQ-M6-009:** Sandboxed consolidation MUST be rate-limited to `MAX_SANDBOXED_PER_CYCLE` = 5 per shard per cycle.

---

## 10. M7: Immune Memory

### 10.1 Purpose

When a consolidation is rejected, M7 stores a signature of the rejected pattern. If a similar pattern appears in the future, it receives enhanced scrutiny automatically. This creates institutional memory of past attack patterns and raises the cost of persistent adversarial campaigns.

### 10.2 Signature Extraction

Upon rejection, extract a three-level signature:

```python
def extract_immune_signature(rejected_claim, contributing_quanta, rejection_reason):
    # L1: Content Hash (exact match detection)
    l1_hash = SHA256(rejected_claim.text.encode())

    # L2: Structural Pattern (similar attack detection)
    domains = sorted(set(q.content.domain for q in contributing_quanta))
    domain_pair = tuple(domains[:2])
    bridge_type = classify_bridge_type(rejected_claim)
    quanta_count_range = (len(contributing_quanta) // 5 * 5,
                          len(contributing_quanta) // 5 * 5 + 5)
    l2_pattern = StructuralPattern(
        domain_pair=domain_pair,
        bridge_type=bridge_type,
        quanta_count_range=quanta_count_range,
    )

    # L3: Behavioral Pattern (campaign detection)
    creation_epochs = [q.provenance.generation_epoch for q in contributing_quanta]
    injection_timing = compute_timing_profile(creation_epochs)
    source_agents = [q.provenance.generating_agent for q in contributing_quanta]
    source_clusters = [get_sentinel_cluster(a) for a in source_agents]
    cluster_distribution = compute_cluster_entropy(source_clusters)
    influence_scores = [compute_influence(q, rejected_claim)
                        for q in contributing_quanta]
    influence_shape = (mean(influence_scores), std(influence_scores),
                       max(influence_scores))
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

**REQ-M7-001:** Every rejected consolidation MUST have an immune signature extracted and stored.

**REQ-M7-002:** Immune signatures MUST contain all three levels (L1, L2, L3).

**REQ-M7-003:** The L2 quanta count range MUST use 5-wide buckets.

### 10.3 Matching Algorithm

```python
def check_immune_memory(candidate_claim, contributing_quanta, immune_store):
    candidate_l1 = SHA256(candidate_claim.text.encode())
    candidate_l2 = extract_structural_pattern(candidate_claim, contributing_quanta)
    candidate_l3 = extract_behavioral_pattern(contributing_quanta)

    best_match = None
    best_match_sig = None

    for sig in immune_store.active_signatures():
        if candidate_l1 == sig.l1_hash:
            return ImmuneMatch(level="L1", signature=sig, confidence=1.0)

        l2_score = structural_similarity(candidate_l2, sig.l2_pattern)
        if l2_score >= L2_MATCH_THRESHOLD:  # 0.60
            if best_match is None or best_match.level > "L2":
                best_match = ImmuneMatch(level="L2", signature=sig,
                                         confidence=l2_score)
                best_match_sig = sig

        l3_score = behavioral_similarity(candidate_l3, sig.l3_pattern)
        if l3_score >= L3_MATCH_THRESHOLD:  # 0.50
            if best_match is None:
                best_match = ImmuneMatch(level="L3", signature=sig,
                                         confidence=l3_score)
                best_match_sig = sig

    if best_match_sig is not None:
        best_match_sig.match_count += 1
        best_match_sig.last_match_epoch = current_epoch()

    return best_match
```

**Structural similarity** requires BOTH domain overlap >= 0.60 AND same bridge type:

```python
def structural_similarity(candidate_l2, stored_l2):
    domain_overlap = jaccard(set(candidate_l2.domain_pair), set(stored_l2.domain_pair))
    bridge_match = 1.0 if candidate_l2.bridge_type == stored_l2.bridge_type else 0.0
    count_overlap = ranges_overlap(candidate_l2.quanta_count_range,
                                    stored_l2.quanta_count_range)
    if domain_overlap < 0.60 or bridge_match < 1.0:
        return 0.0
    return domain_overlap * 0.6 + count_overlap * 0.4
```

**Behavioral similarity** combines timing, cluster distribution, and influence shape:

```python
def behavioral_similarity(candidate_l3, stored_l3):
    timing_sim = max(0.0, 1.0 - abs(candidate_l3.injection_timing.mean -
                                     stored_l3.injection_timing.mean) / 100.0)
    cluster_sim = max(0.0, 1.0 - abs(candidate_l3.cluster_distribution -
                                      stored_l3.cluster_distribution))
    influence_sim = cosine_similarity(
        candidate_l3.influence_shape, stored_l3.influence_shape)
    return timing_sim * 0.3 + cluster_sim * 0.3 + influence_sim * 0.4
```

**REQ-M7-004:** L1 match MUST take absolute priority and return immediately.

**REQ-M7-005:** L2 matching requires `structural_similarity >= L2_MATCH_THRESHOLD` (0.60), which requires BOTH domain overlap >= 0.60 AND same bridge type.

**REQ-M7-006:** L3 matching requires `behavioral_similarity >= L3_MATCH_THRESHOLD` (0.50), computed as `timing_sim * 0.3 + cluster_sim * 0.3 + influence_sim * 0.4`.

### 10.4 Enhanced Scrutiny Trigger

| Match Level | Action |
|---|---|
| L1 (exact content) | AUTOMATIC REJECT. Log and block. |
| L2 (structural) | Enhanced APRT (full leave-one-out). Add 0.20 to immune suspicion. |
| L3 (behavioral) | Standard APRT. Add 0.10 to immune suspicion. Flag for manual review. |

**REQ-M7-007:** L1 match MUST result in automatic rejection with no further evaluation.

**REQ-M7-008:** L2 match MUST trigger enhanced APRT and add 0.20 to immune suspicion.

**REQ-M7-009:** L3 match MUST add 0.10 to immune suspicion and flag for manual review.

### 10.5 Memory Management

#### 10.5.1 Decay Rules

| Level | Base Expiry (cycles) | Extended Expiry (>= 3 matches) |
|-------|---------------------|-------------------------------|
| L1 | 50 | 100 |
| L2 | 100 | 200 |
| L3 | 200 | 400 |

Additional: If no re-trigger in 500 epochs, archive regardless.

**REQ-M7-010:** Signatures matched >= 3 times MUST have expiry doubled.

**REQ-M7-011:** Signatures with no re-trigger in 500 epochs MUST be archived.

#### 10.5.2 Garbage Collection

```python
def immune_memory_gc(immune_store, epoch):
    """Called every epoch during regulation phase."""
    expired = []
    for sig in immune_store.active_signatures():
        age = epoch - sig.created_epoch
        level_expiry = {"L1": L1_EXPIRY_CYCLES, "L2": L2_EXPIRY_CYCLES,
                        "L3": L3_EXPIRY_CYCLES}[sig.level]
        if sig.match_count >= 3:
            level_expiry *= 2
        if sig.last_match_epoch is not None:
            if (epoch - sig.last_match_epoch) > 500:
                expired.append(sig)
                continue
        if age > level_expiry:
            expired.append(sig)

    for sig in expired:
        immune_store.archive(sig)

    while immune_store.active_count() > MAX_IMMUNE_SIGNATURES:
        victim = min(immune_store.active_signatures(),
                     key=lambda s: (s.match_count, -s.created_epoch))
        immune_store.archive(victim)
```

**REQ-M7-012:** Garbage collection MUST run every epoch during the regulation phase (INV-CRP6).

**REQ-M7-013:** Eviction MUST prioritize lowest match count, breaking ties by oldest creation epoch.

**REQ-M7-014:** Archived signatures MUST be retained in archival storage, not deleted.

---

## 11. Novelty Pathway

### 11.1 Purpose

The Novelty Pathway is a dedicated scrutiny track for N3 (paradigmatic) claims. Paradigmatic discoveries — genuinely novel cross-domain connections with no prior documented relationship — inherently lack dissent. Penalizing them for dissent deficit (as CODS would for N1/N2 claims) would suppress the system's most valuable outputs. The Novelty Pathway replaces dissent-deficit penalization with four alternative scrutiny mechanisms that are equally rigorous but appropriate for novel discoveries.

### 11.2 Entry Criteria

A consolidation claim enters the Novelty Pathway if ALL of the following hold:

1. **Novelty classification = N3 (paradigmatic):** `domain_overlap < 0.05 AND precedent_count == 0 AND semantic_distance >= 0.7`
2. **APRT Tier 1 shows no suspicious clusters:** `len(flagged_clusters) == 0`
3. **Source diversity:** Contributing quanta span >= 3 distinct Sentinel Graph clusters
4. **No L2 or L3 immune memory match:** Not a variant of a previously rejected pattern

If any criterion fails, the claim follows the standard path despite being N3.

**REQ-NP-001:** All four entry criteria MUST be satisfied simultaneously for Novelty Pathway routing. Failing any single criterion routes the claim to the standard path.

**REQ-NP-002:** N3 claims that fail entry criteria 2, 3, or 4 MUST be evaluated on the standard path with the N3 CODS dissent weight (0.1). They are not penalized for dissent deficit, but they also do not receive Novelty Pathway protections.

### 11.3 Enhanced Scrutiny Protocol

Claims on the Novelty Pathway undergo four parallel scrutiny tests:

#### 11.3.1 Enhanced APRT (Full Leave-One-Out)

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

Cost: N re-syntheses (N ~ 10-15). Acceptable for the small number of N3 claims per cycle (~10% of candidates, or ~0.5 per cycle).

**REQ-NP-003:** Enhanced APRT on the Novelty Pathway MUST perform full leave-one-out on every quantum. This is INV-CRP7.

**REQ-NP-004:** The robustness score for Novelty Pathway APRT MUST be the minimum stability across all leave-one-out tests, not the mean.

#### 11.3.2 Constructive Adversarial Probing

Instead of searching for existing dissent (which will not exist for N3), generate counter-arguments:

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
    adequately address the concern? Score each: ADDRESSED,
    PARTIALLY_ADDRESSED, or UNADDRESSED.
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

**REQ-NP-005:** Constructive adversarial probing MUST generate at least 3 objections and 1 supporting argument before evaluation.

**REQ-NP-006:** The evaluator LLM MUST be a separate instance from the consolidation LLM.

**REQ-NP-007:** If the address ratio is below 0.50 (fewer than half of objections addressed), the verdict MUST be `WEAK_NOVELTY` with `EXTENDED_QUARANTINE` recommendation.

#### 11.3.3 Temporal Quarantine

N3 claims that pass scrutiny start at PROVISIONAL (rung 1) with a mandatory quarantine:

```python
def apply_temporal_quarantine(quantum, epoch):
    quantum.quarantine_end_epoch = epoch + (QUARANTINE_CYCLES_N3
                                            * EPOCHS_PER_CONSOLIDATION_CYCLE)
    quantum.quarantine_flag = True
    quantum.fast_track_eligible = False  # Disable fast-track during quarantine
```

During quarantine:
- The system actively monitors for naturally emerging contradictions
- Corroborations are recorded but do not trigger promotion
- The claim is usable (with 25% influence weight) but cannot be promoted
- After quarantine expires, accumulated corroborations are evaluated for promotion

**REQ-NP-008:** N3 claims MUST receive a mandatory `QUARANTINE_CYCLES_N3` (5) cycle quarantine. Extended quarantine doubles this to 10 cycles.

**REQ-NP-009:** Fast-track promotion MUST be disabled during quarantine.

**REQ-NP-010:** Corroborations received during quarantine MUST be counted but MUST NOT trigger promotion until the quarantine period expires.

#### 11.3.4 Provenance Deep Audit

Enhanced provenance checking for all contributing quanta:

```python
def provenance_deep_audit(quanta_Q, epoch):
    # Check 1: Temporal micro-patterns
    creation_timestamps = [q.provenance.creation_timestamp for q in quanta_Q]
    intra_epoch_times = [ts % EPOCH_DURATION for ts in creation_timestamps]
    ks_stat, ks_pvalue = ks_test_uniform(intra_epoch_times, EPOCH_DURATION)
    temporal_suspicious = ks_pvalue < KS_TEST_PVALUE_THRESHOLD  # 0.05

    # Check 2: Framing consistency
    embeddings = [embed(q.content.claim_text) for q in quanta_Q]
    mean_pairwise_sim = mean_pairwise_cosine(embeddings)
    framing_suspicious = mean_pairwise_sim > FRAMING_SIMILARITY_THRESHOLD  # 0.60

    # Check 3: Cross-reference with M7 behavioral signatures
    candidate_l3 = extract_behavioral_pattern(quanta_Q)
    behavioral_matches = [sig for sig in immune_store.active_signatures()
                         if behavioral_similarity(candidate_l3, sig.l3_pattern)
                            > L3_MATCH_THRESHOLD * 0.75]

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

**REQ-NP-011:** Provenance deep audit MUST perform all three checks: temporal micro-patterns (Kolmogorov-Smirnov test against uniform), framing consistency (mean pairwise cosine similarity), and M7 behavioral cross-reference (at 75% of normal L3 threshold).

**REQ-NP-012:** Temporal suspicion MUST use the Kolmogorov-Smirnov test against a uniform distribution with significance level `KS_TEST_PVALUE_THRESHOLD` (0.05).

**REQ-NP-013:** Framing suspicion MUST flag when mean pairwise cosine similarity exceeds `FRAMING_SIMILARITY_THRESHOLD` (0.60).

### 11.4 Novelty Pathway Combined Decision

```python
def novelty_pathway_decision(enhanced_aprt_result, probe_result,
                              quarantine_params, deep_audit_result):
    # Hard reject conditions
    if enhanced_aprt_result.robustness_score < 0.50:
        return "REJECT", "N3 claim fails enhanced APRT (fragile)"

    if deep_audit_result.overall_suspicious and \
       enhanced_aprt_result.robustness_score < 0.70:
        return "REJECT", "Suspicious provenance AND moderate fragility"

    # Quarantine with extended review
    if probe_result.verdict == "WEAK_NOVELTY":
        return "QUARANTINE_EXTENDED", "Cannot address >50% of objections"

    if deep_audit_result.overall_suspicious:
        return "QUARANTINE_EXTENDED", "Suspicious provenance patterns"

    # Standard quarantine (5 cycles)
    if enhanced_aprt_result.robustness_score >= 0.70 and \
       probe_result.verdict == "ROBUST_NOVELTY" and \
       not deep_audit_result.overall_suspicious:
        return "ACCEPT_WITH_QUARANTINE", "Passes all scrutiny"

    return "QUARANTINE_EXTENDED", "Mixed signals"
```

`QUARANTINE_EXTENDED` doubles the quarantine period from 5 cycles to 10 cycles.

**REQ-NP-014:** Enhanced APRT robustness below 0.50 MUST result in hard rejection for N3 claims.

**REQ-NP-015:** Suspicious provenance combined with robustness below 0.70 MUST result in hard rejection.

**REQ-NP-016:** `QUARANTINE_EXTENDED` MUST double the standard quarantine period.

### 11.5 Exit Conditions

A quarantined N3 claim exits quarantine when:

1. **Normal exit:** Quarantine period expires (5 or 10 cycles) AND no contradictions have emerged during quarantine.
2. **Early exit (rare):** 3+ independent DIRECT corroborations from 3+ different parcels arrive before quarantine expires. This represents overwhelming organic confirmation.
3. **Rejection exit:** A strong contradiction (belief > 0.6) emerges during quarantine. The claim is rejected and its signature stored in M7 immune memory.

**REQ-NP-017:** Early exit MUST require >= 3 independent DIRECT corroborations from >= 3 distinct parcels. This threshold is deliberately high to prevent manufactured early exit.

**REQ-NP-018:** Rejection exit MUST require a contradiction with belief > 0.6 (not 0.5, which is the standard challenge threshold). This provides N3 claims additional protection against weak challenges during the quarantine observation period.

---

## 12. Cross-Mechanism Integration

### 12.1 Combined Scoring Formula

For **standard candidates** (N1 or N2 novelty tier):

```
base_suspicion = 0.0

# M1 APRT contribution (inverted: low robustness = high suspicion)
aprt_suspicion = max(0.0, 1.0 - robustness_score)
weight_aprt = WEIGHT_APRT  # 0.35

# M2 CODS contribution
cods_suspicion = cods_score  # Already novelty-calibrated
weight_cods = WEIGHT_CODS  # 0.25

# C10 Adversarial Probe contribution (inverted)
probe_suspicion = max(0.0, 1.0 - probe_relative_strength)
weight_probe = WEIGHT_PROBE  # 0.25

# M7 Immune Memory contribution
immune_suspicion = {None: 0.0, "L3": 0.10, "L2": 0.20, "L1": 1.0}[immune_match_level]
weight_immune = WEIGHT_IMMUNE  # 0.15

# M3 Source Purpose (conditional, max 0.15)
purpose_addition = purpose_score if m3_invoked else 0.0

combined_suspicion = (weight_aprt * aprt_suspicion
                    + weight_cods * cods_suspicion
                    + weight_probe * probe_suspicion
                    + weight_immune * immune_suspicion
                    + purpose_addition)
```

**Weight validation:** `WEIGHT_APRT + WEIGHT_CODS + WEIGHT_PROBE + WEIGHT_IMMUNE = 0.35 + 0.25 + 0.25 + 0.15 = 1.00`. The purpose addition is on top of the normalized weights, meaning maximum combined suspicion is 1.15 (all signals maximally suspicious + M3 invoked at cap).

**REQ-INT-001:** Combined scoring weights MUST sum to 1.00 (excluding M3 purpose addition). M3 is additive and capped at 0.15.

**REQ-INT-002:** L1 immune match MUST NOT reach the combined scoring formula. L1 matches are automatic rejects handled before scoring.

### 12.2 Decision Thresholds

| Combined Suspicion | Decision |
|---|---|
| < `ACCEPT_THRESHOLD` (0.35) | **ACCEPT** — proceed to PCVM verification gate |
| `ACCEPT_THRESHOLD` to `REJECT_THRESHOLD` (0.35 - 0.60) | **QUARANTINE** — hold for manual review |
| > `REJECT_THRESHOLD` (0.60) | **REJECT** — store signature in M7 immune memory |

For **N3 candidates** on the Novelty Pathway: the combined scoring formula is NOT used. The Novelty Pathway decision function (Section 11.4) applies instead.

**REQ-INT-003:** `ACCEPT_THRESHOLD` and `REJECT_THRESHOLD` are constitutional parameters requiring G-class governance supermajority to change.

**REQ-INT-004:** N3 claims routed to the Novelty Pathway MUST NOT be evaluated by the combined scoring formula. They use the Novelty Pathway decision function exclusively.

### 12.3 Pipeline Integration with C10 Layers

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
          Path              (Section 11)
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
| M5 (Credibility Ladder) | Layer 5 | Layer 5 binary model | Replaces with graduated system |
| M6 (Depth Limits) | Layer 3 (lineage) | | Extends lineage with constraints |
| M7 (Immune Memory) | | | NEW (between synthesis and APRT) |
| Novelty Pathway | Layer 2 (probe) | | Alternative scrutiny for N3 |

### 12.4 Operational Cost Model

Assumptions: 5 VRF-selected candidates per cycle, N=10 quanta per candidate average.

| Component | LLM Calls | Embedding Ops | Notes |
|---|---|---|---|
| Base synthesis (C6) | 5 x 3 = 15 | 0 | Three-pass synthesis per candidate |
| M4 VRF selection | 0 | 0 | Hash operations only |
| M1 APRT Tier 1 | 0 | 5 x (10+100) = 550 | N embeddings + N^2 pairwise per candidate |
| M1 APRT Tier 2 (avg) | 5 x 2.5 = 12.5 | 0 | Average 2.5 re-syntheses per candidate |
| M2 CODS | 5 x 2 = 10 | 5 x 1 = 5 | 1 novelty classification + 1 dissent search |
| M3 Purpose (20%) | 1 x 1 = 1 | 0 | Invoked for ~1 of 5 candidates |
| M7 Immune Check | 0 | 5 x 1 = 5 | Embedding comparison per candidate |
| C10 Layer 2 Probe | 5 x 2 = 10 | 0 | Counter-hypothesis + scoring |
| **Novelty Pathway** (0.5 candidates avg) | | | |
| — Enhanced APRT | 0.5 x 10 = 5 | 0 | Full leave-one-out |
| — Constructive Probe | 0.5 x 3 = 1.5 | 0 | Objections + support + evaluation |
| — Deep Audit | 0 | 0.5 x 10 = 5 | Embedding-based checks |
| **TOTAL** | **~55 LLM calls** | **~565 embeddings** | |
| **Without CRP+** | **15 LLM calls** | **0 embeddings** | Base synthesis only |
| **Cost multiplier** | **~3.7x LLM** | **+565 embeddings** | |

The 3.7x LLM multiplier is lower than the FEASIBILITY estimate of 7.0x because:
1. VRF selection reduces candidate count before CRP+ mechanisms engage
2. APRT Tier 1 eliminates ~60% of Tier 2 work
3. M3 invocation rate is only 20%

**Absolute cost per cycle:** ~55 LLM calls + ~565 embedding operations. If consolidation cycles run every 10 epochs and epochs are ~10 minutes, this is ~55 LLM calls per ~100 minutes.

### 12.5 Performance Budget

| Constraint | Budget | CRP+ Usage | Margin |
|---|---|---|---|
| LLM calls per consolidation cycle | 100 | ~55 | 45% headroom |
| Embedding operations per cycle | 2000 | ~565 | 72% headroom |
| Wall-clock time per candidate | 60 seconds | ~35 seconds (est.) | 42% headroom |
| Total CRP+ overhead vs base consolidation | <= 5x | ~3.7x | Within budget |

**REQ-INT-005:** Total CRP+ overhead MUST NOT exceed 5x the base consolidation cost (LLM calls). If overhead approaches 5x, VRF selection rate SHOULD be reduced to decrease candidate count.

**REQ-INT-006:** CRP+ MUST operate within the rate limits established by C10 Layer 4. CRP+ does not modify rate limits; it operates within them.

---

## 13. Parameters & Configuration

### 13.1 Constitutional Parameters

These require G-class governance supermajority (C3) to change:

| Parameter | Default | Range | Description | Rationale |
|---|---|---|---|---|
| `VRF_SELECTION_RATE` | 0.10 | [0.05, 0.30] | Fraction of candidates selected per cycle | 0.10 gives 10x unpredictability; lower reduces throughput, higher reduces adversary cost |
| `STABILITY_THRESHOLD` | 0.70 | [0.50, 0.85] | Minimum semantic similarity for re-synthesis stability | 0.70 allows moderate rephrasing while catching substantial conclusion changes |
| `ACCEPT_THRESHOLD` | 0.35 | [0.20, 0.50] | Combined suspicion below this -> ACCEPT | Lower = more permissive; higher = more conservative |
| `REJECT_THRESHOLD` | 0.60 | [0.45, 0.80] | Combined suspicion above this -> REJECT | Must be > ACCEPT_THRESHOLD; gap defines quarantine zone |
| `MAX_IMMUNE_SIGNATURES` | 1000 | [100, 5000] | Maximum active immune signatures per shard | Memory vs. detection tradeoff |
| `PROVISIONAL_INFLUENCE_WEIGHT` | 0.25 | [0.10, 0.40] | Influence weight for PROVISIONAL K-class | Lower = less damage from poison; higher = more utility from genuine claims |
| `QUARANTINE_CYCLES_N3` | 5 | [3, 20] | Mandatory quarantine cycles for N3 claims | Shorter = faster discovery; longer = more observation time |
| `DEPTH_LIMIT_PROVISIONAL` | EXCLUDED | {EXCLUDED} | PROVISIONAL K-class excluded from consolidation | Constitutional invariant (INV-CRP5) |
| `DEPTH_LIMIT_CORROBORATED_WEIGHT` | 0.50 | [0.25, 0.75] | Input weight for CORROBORATED K-class | Balances utility vs. cascade risk |

### 13.2 Operational Parameters

These can be changed by system operators without governance:

| Parameter | Default | Range | Description |
|---|---|---|---|
| `CONSOLIDATION_MIN_EDGE_WEIGHT` | 0.30 | [0.10, 0.50] | Minimum edge weight for candidate identification |
| `HIGH_INFLUENCE_SIGMA` | 2.0 | [1.5, 3.0] | Standard deviations above mean for high-influence flag |
| `REDUNDANT_CLUSTER_SIMILARITY` | 0.85 | [0.75, 0.95] | Cosine similarity threshold for cluster detection |
| `REDUNDANT_CLUSTER_MIN_SIZE` | 3 | [2, 5] | Minimum quanta in a suspicious cluster |
| `RANDOM_SUBSET_FRACTION` | 0.30 | [0.20, 0.50] | Fraction of quanta removed in Case C |
| `EXPECTED_DISSENT_LEVEL` | 1.5 | [1.0, 3.0] | Expected total dissent quality for deficit computation |
| `DISSENT_WEIGHT_N1` | 1.0 | [0.8, 1.0] | Dissent deficit weight for N1 (incremental) |
| `DISSENT_WEIGHT_N2` | 0.5 | [0.3, 0.7] | Dissent deficit weight for N2 (bridging) |
| `DISSENT_WEIGHT_N3` | 0.1 | [0.0, 0.2] | Dissent deficit weight for N3 (paradigmatic) |
| `M3_MAX_CONTRIBUTION` | 0.15 | [0.05, 0.20] | Hard cap on M3 purpose score contribution |
| `M3_HIGH_PURPOSE_THRESHOLD` | 0.80 | [0.70, 0.90] | Purpose alignment above this is suspicious |
| `L2_MATCH_THRESHOLD` | 0.60 | [0.40, 0.80] | Immune memory L2 structural match threshold |
| `L3_MATCH_THRESHOLD` | 0.50 | [0.30, 0.70] | Immune memory L3 behavioral match threshold |
| `L1_EXPIRY_CYCLES` | 50 | [20, 200] | Immune memory L1 signature expiry |
| `L2_EXPIRY_CYCLES` | 100 | [50, 400] | Immune memory L2 signature expiry |
| `L3_EXPIRY_CYCLES` | 200 | [100, 800] | Immune memory L3 signature expiry |
| `BRIDGE_DENSITY_FACTOR` | 0.01 | [0.005, 0.05] | Expected cross-domain bridge density |
| `DOMAIN_OVERLAP_N1_THRESHOLD` | 0.30 | [0.20, 0.50] | Domain overlap threshold for N1 classification |
| `DOMAIN_OVERLAP_N3_THRESHOLD` | 0.05 | [0.01, 0.10] | Domain overlap threshold for N3 classification |
| `SEMANTIC_DISTANCE_N1_THRESHOLD` | 0.40 | [0.30, 0.50] | Semantic distance threshold for N1 |
| `SEMANTIC_DISTANCE_N3_THRESHOLD` | 0.70 | [0.60, 0.80] | Semantic distance threshold for N3 |
| `FRAMING_SIMILARITY_THRESHOLD` | 0.60 | [0.50, 0.75] | Deep audit framing suspicion threshold |
| `KS_TEST_PVALUE_THRESHOLD` | 0.05 | [0.01, 0.10] | Deep audit temporal micro-pattern p-value |
| `FAST_TRACK_MODALITIES` | 3 | [2, 5] | Minimum distinct evidence modalities for fast-track |
| `SANDBOX_TIMEOUT_CYCLES` | 10 | [5, 20] | Max cycles before sandboxed K->K is archived |
| `MAX_SANDBOXED_PER_CYCLE` | 5 | [1, 10] | Sandboxed consolidations per shard per cycle |
| `WEIGHT_APRT` | 0.35 | [0.20, 0.50] | Combined scoring weight for APRT |
| `WEIGHT_CODS` | 0.25 | [0.15, 0.35] | Combined scoring weight for CODS |
| `WEIGHT_PROBE` | 0.25 | [0.15, 0.35] | Combined scoring weight for adversarial probe |
| `WEIGHT_IMMUNE` | 0.15 | [0.05, 0.25] | Combined scoring weight for immune memory |

**REQ-CFG-001:** `WEIGHT_APRT + WEIGHT_CODS + WEIGHT_PROBE + WEIGHT_IMMUNE` MUST equal 1.00 after any parameter change. Implementations MUST validate this constraint at configuration load time.

**REQ-CFG-002:** `REJECT_THRESHOLD` MUST be strictly greater than `ACCEPT_THRESHOLD`. The gap defines the quarantine zone.

**REQ-CFG-003:** Constitutional parameters MUST NOT be modifiable through operational configuration channels. They require G-class governance supermajority.

---

## 14. Pseudocode

### 14.1 Master Orchestrator

```python
def crp_plus_evaluate(candidate_claim, contributing_quanta, shard, epoch):
    """
    Master CRP+ evaluation function.
    Called after Three-Pass LLM Synthesis completes.
    Returns: CRPResult with decision and supporting data.
    """
    result = CRPResult()

    # === STEP 1: Immune Memory Check (M7) ===
    immune_match = check_immune_memory(
        candidate_claim, contributing_quanta, shard.immune_store
    )
    result.immune_match = immune_match

    if immune_match and immune_match.level == "L1":
        store_rejection(candidate_claim, contributing_quanta, "L1_IMMUNE_MATCH")
        result.decision = "REJECT"
        result.reason = "Exact match to previously rejected consolidation"
        return result

    enhanced_mode = (immune_match is not None
                     and immune_match.level in ("L2", "L3"))

    # === STEP 2: APRT (M1) ===
    if enhanced_mode:
        aprt_result = enhanced_aprt(
            candidate_claim, contributing_quanta, shard.synthesis_params
        )
    else:
        aprt_result = standard_aprt(
            candidate_claim, contributing_quanta, shard.synthesis_params
        )
    result.aprt = aprt_result

    # === STEP 3: CODS (M2) ===
    cods_result = evaluate_cods(
        candidate_claim, contributing_quanta, shard.coherence_graph
    )
    result.cods = cods_result

    # === STEP 4: Novelty Pathway Branch ===
    if cods_result.novelty_tier == "N3" and meets_novelty_pathway_criteria(
            aprt_result, contributing_quanta, immune_match):

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

    # === STEP 5: C10 Adversarial Consolidation Probing ===
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

    # === STEP 6: M3 Source Purpose Scoring (Conditional) ===
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

    # === STEP 7: Combined Scoring ===
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

### 14.2 Standard APRT

```python
def standard_aprt(claim_C, quanta_Q, synthesis_params):
    """Standard two-tier APRT."""

    # -- Tier 1: Embedding Influence Screening --
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
            cluster_relevant = all(
                cosine_similarity(embeddings[qid], emb_C) > 0.5
                for qid in cluster
            )
            if cluster_relevant:
                clusters.append(cluster)
                visited.update(cluster)

    # -- Case Classification --
    if len(flagged) > 0:
        case = "A"
    elif len(clusters) > 0:
        case = "B"
    else:
        case = "C"

    # -- Tier 2: Targeted Re-Synthesis --
    if case == "A":
        stabilities = []
        for qid in flagged[:3]:
            Q_reduced = [q for q in quanta_Q if q.id != qid]
            C_prime = execute_llm_synthesis_single(Q_reduced, synthesis_params)
            stab = semantic_similarity(claim_C.text, C_prime.text)
            stabilities.append(stab)
        robustness = min(stabilities) if stabilities else 1.0
        resynthesis_count = len(stabilities)

    elif case == "B":
        stabilities = []
        for cluster in clusters[:2]:
            Q_reduced = [q for q in quanta_Q if q.id not in cluster]
            if len(Q_reduced) < 3:
                stabilities.append(0.0)
                continue
            C_prime = execute_llm_synthesis_single(Q_reduced, synthesis_params)
            stab = semantic_similarity(claim_C.text, C_prime.text)
            stabilities.append(stab)
        robustness = min(stabilities) if stabilities else 1.0
        resynthesis_count = len(stabilities)

    else:  # Case C
        vrf_seed = SHA256(claim_C.text.encode() + b"APRT_RANDOM")
        remove_indices = vrf_select_subset(
            len(quanta_Q), RANDOM_SUBSET_FRACTION, vrf_seed
        )
        Q_reduced = [q for i, q in enumerate(quanta_Q)
                     if i not in remove_indices]
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

### 14.3 CODS Evaluation

```python
def evaluate_cods(claim_C, quanta_Q, coherence_graph):
    """Full CODS evaluation: novelty classification + dissent search."""

    # -- Step 1: Novelty Classification --
    domains = extract_domains(quanta_Q)
    domain_a = domains[0]
    domain_b = domains[1] if len(domains) > 1 else domains[0]

    existing_bridges = count_analogy_edges(domain_a, domain_b, coherence_graph)
    expected = max(1, int(sqrt(count_quanta(domain_a) * count_quanta(domain_b))
                         * BRIDGE_DENSITY_FACTOR))
    domain_overlap = existing_bridges / expected

    nearest_K = find_nearest_K_class(claim_C, coherence_graph)
    if nearest_K is not None:
        semantic_distance = cosine_distance(
            embed(claim_C.text), embed(nearest_K.content.claim_text))
    else:
        semantic_distance = 1.0

    precedent_count = count_prior_consolidation_attempts(
        domain_a, domain_b, lookback_epochs=500)

    # Sparse domain safeguard (REQ-M2-006)
    sparse_domain = (count_active_quanta(domain_a) < 10
                     or count_active_quanta(domain_b) < 10)

    if classify_n3(domain_overlap, precedent_count, semantic_distance) \
       and not sparse_domain:
        novelty_tier = "N3"
    elif (domain_overlap >= DOMAIN_OVERLAP_N1_THRESHOLD
          or precedent_count >= 3
          or semantic_distance < SEMANTIC_DISTANCE_N1_THRESHOLD):
        novelty_tier = "N1"
    else:
        novelty_tier = "N2"

    # -- Step 2: Dissent Search --
    queries = generate_dissent_queries(claim_C)
    dissent_items = []

    for query in queries:
        query_emb = embed(query)
        candidates = semantic_search(query_emb, coherence_graph,
                                     top_k=10, min_similarity=0.3)
        for candidate in candidates:
            strength = assess_contradiction_strength(candidate, claim_C)
            if strength > 0.2:
                relevance = cosine_similarity(
                    embed(candidate.content.claim_text), embed(claim_C.text))
                organic = 1.0 if candidate.provenance.generation_epoch < \
                          claim_C.generation_epoch else 0.5
                quality = relevance * strength * organic
                dissent_items.append(DissentItem(
                    quantum=candidate, quality=quality))

    # Deduplicate
    seen = {}
    for item in dissent_items:
        if item.quantum.id not in seen \
           or item.quality > seen[item.quantum.id].quality:
            seen[item.quantum.id] = item
    dissent_items = list(seen.values())

    # -- Step 3: Dissent Deficit --
    total_dissent = sum(item.quality for item in dissent_items)
    dissent_deficit = max(0.0, 1.0 - total_dissent / EXPECTED_DISSENT_LEVEL)

    # -- Step 4: Novelty-Calibrated Score --
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

### 14.4 VRF Consolidation Selection

```python
def vrf_select_consolidation_candidates(all_candidates, agent, shard, epoch):
    """VRF-based selection replacing deterministic selection."""
    previous_hash = shard.previous_consolidation_hash
    vrf_input = SHA256(
        b"CRP_CONSOLIDATION_SELECT"
        + uint64_be(epoch)
        + shard.shard_id.encode()
        + previous_hash
    )

    beta, pi = ECVRF_prove(agent.privkey, vrf_input)

    selected = []
    for candidate in all_candidates:
        bridge_id = compute_bridge_id(candidate)
        selection_hash = SHA256(beta + bridge_id.encode())
        selection_value = uint256(selection_hash) / (2**256)

        strength = mean(e.weight for e in candidate.connecting_edges) \
                   if candidate.connecting_edges else 0.5
        threshold = coverage_boost(candidate, epoch)  # Includes anti-starvation

        if selection_value < threshold or threshold == FORCE_SELECT:
            candidate.vrf_proof = pi
            candidate.vrf_output = beta
            selected.append(candidate)

    return selected
```

### 14.5 Credibility Ladder Epoch Update

```python
def update_credibility_ladder(shard, epoch, corroboration_log, lineage):
    """Called each epoch during the regulation phase."""
    for q in shard.active_K_class_quanta():
        promotion = check_promotion(q, epoch, lineage, corroboration_log)
        if promotion is not None:
            apply_promotion(q, promotion, epoch)
            continue

        # Check quarantine expiry for N3 claims
        if q.quarantine_flag and epoch >= q.quarantine_end_epoch:
            q.quarantine_flag = False
            q.fast_track_eligible = True

        # Check sandbox timeout for SPECULATIVE claims
        if q.credibility_rung == 0:
            sandbox_age = epoch - q.provenance.generation_epoch
            if sandbox_age > SANDBOX_TIMEOUT_CYCLES * EPOCHS_PER_CONSOLIDATION_CYCLE:
                input_quanta = lineage.get_inputs(q.id)
                if any(iq.credibility_rung < 2 for iq in input_quanta):
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

### 14.6 Novelty Pathway Execution

```python
def execute_novelty_pathway(candidate_claim, contributing_quanta,
                             aprt_result, shard, epoch):
    """Execute full Novelty Pathway scrutiny for N3 claims."""

    # 1. Enhanced APRT (full leave-one-out)
    enhanced_result = enhanced_aprt(
        candidate_claim, contributing_quanta, shard.synthesis_params
    )

    # 2. Constructive adversarial probing
    probe_result = constructive_adversarial_probe(
        candidate_claim, contributing_quanta
    )

    # 3. Provenance deep audit
    deep_audit = provenance_deep_audit(contributing_quanta, epoch)

    # 4. Combined decision
    decision, reason = novelty_pathway_decision(
        enhanced_result, probe_result, None, deep_audit
    )

    # Apply quarantine if accepted
    if decision in ("ACCEPT_WITH_QUARANTINE", "QUARANTINE_EXTENDED"):
        quantum = create_quantum_from_claim(candidate_claim)
        quantum.credibility_rung = 1  # PROVISIONAL
        apply_temporal_quarantine(quantum, epoch)

        if decision == "QUARANTINE_EXTENDED":
            quantum.quarantine_end_epoch = epoch + (
                QUARANTINE_CYCLES_N3 * 2 * EPOCHS_PER_CONSOLIDATION_CYCLE
            )

    return NoveltyPathwayResult(
        decision=decision,
        reason=reason,
        enhanced_aprt=enhanced_result,
        probe=probe_result,
        deep_audit=deep_audit,
    )
```

---

## 15. Failure Modes & Recovery

### FM-1: APRT False Positive (Organic Consolidation Flagged as Fragile)

**Trigger:** A genuinely robust consolidation has one quantum that happens to be uniquely relevant (high influence), and removing it produces a semantically different (but functionally equivalent) re-synthesis.

**Detection:** Monitor rejection rate vs. manual review agreement. If reviewers disagree with >10% of rejections, recalibrate.

**Recovery:** The stability comparison uses embedding cosine similarity, which captures semantic equivalence even when wording differs. The 0.70 threshold allows moderate rephrasing. If false positives exceed 5% of consolidations, raise `STABILITY_THRESHOLD` to 0.60 (operational parameter). Additionally, implement a "re-synthesis consistency check": run synthesis twice on the SAME input and measure baseline variability. Set `STABILITY_THRESHOLD` to `baseline_variability + margin`.

### FM-2: CODS Novelty Misclassification (N1 Classified as N3)

**Trigger:** Domain overlap and precedent count are zero because the knowledge base is sparse in one domain (newly seeded), not because the connection is genuinely novel.

**Detection:** Track N3 classification rate per domain pair. If a domain pair consistently produces N3 classifications, flag for manual review.

**Recovery:** REQ-M2-006 (sparse domain safeguard) forces N2 cap when either domain has < 10 active quanta. If misclassification persists above this safeguard, increase the minimum domain size threshold.

### FM-3: VRF Selection Starvation (Important Bridge Never Selected)

**Trigger:** A bridge with low strength has consistently bad VRF luck and is not selected for 50+ epochs.

**Detection:** Monitor `epochs_since_selection` for all bridges. Alert when any bridge exceeds 30 epochs without selection.

**Recovery:** Anti-starvation boost (REQ-M4-006) forces selection after 40 epochs. This is automatic and requires no manual intervention.

### FM-4: Credibility Ladder Bottleneck (Genuine Discoveries Stuck at PROVISIONAL)

**Trigger:** A K-class claim is genuinely correct but the domain is sparse, so independent E-class corroboration is slow to arrive.

**Detection:** Track distribution of epochs-at-PROVISIONAL across all K-class claims. Alert when mean exceeds 100 epochs.

**Recovery:** Domain-adaptive thresholds (Section 8.6) relax criteria for sparse domains. Fast-track provision allows multi-modal corroboration to accelerate promotion. Claims remaining PROVISIONAL for > 200 epochs without contradiction are flagged for manual review (but NOT auto-promoted).

### FM-5: Immune Memory False Match (Legitimate Claim Matches Rejected Signature)

**Trigger:** L2 or L3 signature is too broad, matching a legitimate claim that bridges the same domain pair with similar structure.

**Detection:** Track immune memory match rate. Alert if > 5% of candidates match.

**Recovery:** L2 requires BOTH domain overlap >= 0.60 AND same bridge type. L3 requires combined similarity >= 0.50 across three dimensions. Enhanced scrutiny does not reject; it runs more tests. A genuinely robust claim will pass enhanced APRT. If match rates are excessive, tighten `L2_MATCH_THRESHOLD` and `L3_MATCH_THRESHOLD`.

### FM-6: Redundant Cluster Evasion (Non-Redundant Planting)

**Trigger:** Sophisticated adversary plants quanta that are each unique rather than redundant copies, avoiding cluster detection.

**Detection:** Post-hoc analysis of accepted consolidations whose K-class claims are later challenged.

**Recovery:** APRT's Case C (random subset) provides partial defense. Combined scoring means the adversary must also defeat CODS and probing. M5 credibility ladder limits damage (25% influence at PROVISIONAL). Estimated residual adversary cost: ~30x base cost.

### FM-7: Novelty Pathway Abuse (Adversary Engineers N3 Classification)

**Trigger:** Adversary deliberately bridges two domains with no prior relationship to trigger N3 classification.

**Detection:** Track N3 entry rate. Sudden spikes suggest manufactured novelty.

**Recovery:** The Novelty Pathway is HARDER to pass than the standard path for planted claims: full leave-one-out APRT, constructive adversarial probing, 5-cycle quarantine, and deep audit. The adversary gains nothing by engineering N3 classification.

### FM-8: Sandbox Accumulation (SPECULATIVE Claims Consume Resources)

**Trigger:** Many K->K consolidations created, few inputs promoted, leading to SPECULATIVE backlogs.

**Detection:** Monitor SPECULATIVE count per shard. Alert if > 50.

**Recovery:** Rate limit via `MAX_SANDBOXED_PER_CYCLE` = 5. SPECULATIVE claims consume minimal storage (simplified records). `SANDBOX_TIMEOUT_CYCLES` = 10 ensures aggressive archival.

### FM-9: Cascade Amplification (M5 Demotion + C10 Cascade Interaction)

**Trigger:** Failed consolidation triggers C10 cascade on contributing quanta, which triggers M5 demotion, which may cause downstream fragility.

**Detection:** Monitor cascade depth and demotion counts per epoch. Alert if cascade triggers > 3 demotions.

**Recovery:** C10 cascade has `MAX_CASCADE_DEPTH = 5`. M5 demotion floor is PROVISIONAL (rung 1). M5 demotion requires 2+ cascade events (REQ-M5-009). Combined: worst case is bounded cascade with floor protection.

### FM-10: LLM Consistency Failure (Re-Synthesis Varies Due to Stochasticity)

**Trigger:** LLM synthesis is inherently stochastic; two runs on the same input produce semantically different outputs.

**Detection:** Baseline variability testing: run synthesis twice on same input, measure similarity.

**Recovery:** Synthesis uses low temperature (0.2). Stability uses embedding cosine similarity (not string matching). `STABILITY_THRESHOLD` at 0.70 allows substantial rephrasing. If persistent, calibrate threshold to `baseline_variability + margin`.

---

## 16. Conformance Requirements

### 16.1 MUST Requirements

The following requirements are mandatory for CRP+ conformance. A system that violates any MUST requirement is non-conformant.

| ID | Requirement |
|---|---|
| REQ-M1-001 | APRT embedding model MUST match C6 coherence graph embedding model |
| REQ-M1-002 | Influence scores MUST be computed for ALL quanta in Q |
| REQ-M1-004 | Anomaly detection MUST use statistical threshold mu + k*sigma |
| REQ-M1-006 | Case classification MUST follow priority A > B > C |
| REQ-M1-008 | Re-synthesis MUST use identical synthesis parameters |
| REQ-M1-010 | Case C random subset MUST use VRF-derived seed |
| REQ-M1-011 | Stability MUST use embedding cosine similarity |
| REQ-M1-012 | Enhanced APRT MUST perform full leave-one-out |
| REQ-M1-013 | Enhanced APRT MUST trigger for L2 matches and Novelty Pathway |
| REQ-M2-004 | Novelty tier MUST use most-novel-feature rule |
| REQ-M2-005 | N3 MUST require all three conditions simultaneously |
| REQ-M2-006 | Sparse domains (< 10 quanta) MUST cap at N2 |
| REQ-M2-009 | Contradiction strength MUST use separate LLM instance |
| REQ-M2-011 | N3 claims MUST route to Novelty Pathway |
| REQ-M3-001 | M3 MUST NOT be invoked outside ambiguity window |
| REQ-M3-004 | M3 output MUST be hard-capped at 0.15 |
| REQ-M4-001 | VRF input MUST include domain separator prefix |
| REQ-M4-002 | VRF input MUST include previous_consolidation_hash |
| REQ-M4-003 | VRF proof MUST be stored with decision record |
| REQ-M4-006 | Anti-starvation MUST force selection after 40 epochs |
| REQ-M4-008 | VRF_SELECTION_RATE is constitutional |
| REQ-M4-009 | CRP+ MUST reuse C3 ECVRF key pairs |
| REQ-M5-001 | Standard K-class MUST enter at rung 1 (PROVISIONAL) |
| REQ-M5-003 | Influence weights MUST be applied multiplicatively |
| REQ-M5-005 | Quarantined claims MUST NOT promote during quarantine |
| REQ-M5-008 | Demotion floor MUST be PROVISIONAL (rung 1) |
| REQ-M5-009 | Cascade demotion MUST require 2+ events |
| REQ-M5-010 | Demotion MUST reset tenure clock |
| REQ-M6-001 | SPECULATIVE/PROVISIONAL MUST be excluded from consolidation |
| REQ-M6-004 | Depth filtering MUST occur before synthesis |
| REQ-M6-006 | Sandbox products MUST be rung 0 with FULL_SANDBOX |
| REQ-M7-001 | Every rejection MUST produce an immune signature |
| REQ-M7-002 | Signatures MUST contain all three levels |
| REQ-M7-004 | L1 match MUST take absolute priority |
| REQ-M7-007 | L1 match MUST result in automatic rejection |
| REQ-M7-012 | GC MUST run every epoch |
| REQ-NP-001 | All four entry criteria MUST hold for Novelty Pathway |
| REQ-NP-003 | Enhanced APRT on Novelty Pathway MUST be full leave-one-out |
| REQ-NP-008 | N3 MUST receive mandatory quarantine |
| REQ-NP-014 | Robustness < 0.50 MUST reject N3 claims |
| REQ-INT-001 | Combined scoring weights MUST sum to 1.00 |
| REQ-INT-003 | ACCEPT/REJECT thresholds are constitutional |
| REQ-CFG-001 | Weight sum MUST be validated at configuration load |
| REQ-CFG-002 | REJECT_THRESHOLD MUST exceed ACCEPT_THRESHOLD |
| REQ-CFG-003 | Constitutional parameters MUST require governance to change |

### 16.2 SHOULD Requirements

The following requirements are recommended for optimal operation but not mandatory for conformance.

| ID | Requirement |
|---|---|
| REQ-M1-003 | SHOULD use composite influence formula (relevance * uniqueness) |
| REQ-M1-005 | Clusters SHOULD require both high similarity AND relevance |
| REQ-M1-007 | Case A SHOULD cap at 3 flagged quanta |
| REQ-M1-009 | Cluster removal leaving < 3 quanta SHOULD set stability to 0.0 |
| REQ-M2-001 | Domain overlap SHOULD normalize by domain size |
| REQ-M2-007 | Dissent search SHOULD generate at least 4 query types |
| REQ-M2-008 | Pre-existing dissent SHOULD receive full organic multiplier |
| REQ-M3-003 | M3 SHOULD use separate evaluator model |
| REQ-M4-004 | Selection threshold SHOULD use strength-biased formula |
| REQ-M5-006 | Fast-track SHOULD require 3+ modalities and 2-epoch minimum |
| REQ-M5-012 | Domain-adaptive thresholds SHOULD use sigmoid/lerp |
| REQ-M7-010 | Persistent patterns (3+ matches) SHOULD have doubled expiry |
| REQ-NP-005 | Constructive probe SHOULD generate 3+ objections |
| REQ-NP-011 | Deep audit SHOULD perform all three checks |
| REQ-INT-005 | Total overhead SHOULD NOT exceed 5x base cost |

### 16.3 MAY Requirements

| ID | Requirement |
|---|---|
| REQ-M2-003 | Precedent lookback MAY be adjusted from 500 epochs |
| REQ-M2-010 | EXPECTED_DISSENT_LEVEL MAY be tuned per domain |
| REQ-M3-002 | M3 MAY be disabled entirely for N3 claims |
| REQ-M4-007 | Coverage boost MAY be disabled for bridges < 20 epochs old |
| REQ-M5-002 | SPECULATIVE rung MAY be disabled (disabling K->K sandboxed consolidation entirely) |
| REQ-M5-007 | CANONICAL tenure MAY be adjusted from 200 epochs |
| REQ-M5-011 | PROVISIONAL floor MAY be adjusted from 0.50 (as constitutional change) |
| REQ-M5-013 | C10 EmpiricalValidationQueue MAY be extended with additional fields |
| REQ-M6-009 | MAX_SANDBOXED_PER_CYCLE MAY be adjusted per shard |
| REQ-M7-014 | Archived signatures MAY be periodically purged after long-term retention |
| REQ-NP-017 | Early exit threshold MAY be adjusted from 3 corroborations |
| REQ-NP-018 | Rejection exit belief threshold MAY be adjusted from 0.6 |

---

## Appendix A: Formal Requirements Traceability

| REQ ID | Section | Mechanism | Category | Level |
|---|---|---|---|---|
| REQ-M1-001 | 4.3.1 | M1 APRT | Embedding model consistency | MUST |
| REQ-M1-002 | 4.3.2 | M1 APRT | Complete influence computation | MUST |
| REQ-M1-003 | 4.3.2 | M1 APRT | Composite influence formula | SHOULD |
| REQ-M1-004 | 4.3.3 | M1 APRT | Statistical anomaly threshold | MUST |
| REQ-M1-005 | 4.3.3 | M1 APRT | Cluster detection criteria | SHOULD |
| REQ-M1-006 | 4.3.4 | M1 APRT | Case priority order | MUST |
| REQ-M1-007 | 4.4.1 | M1 APRT | Case A cap at 3 | SHOULD |
| REQ-M1-008 | 4.4.1 | M1 APRT | Re-synthesis parameter identity | MUST |
| REQ-M1-009 | 4.4.2 | M1 APRT | Minimum quanta for synthesis | SHOULD |
| REQ-M1-010 | 4.4.3 | M1 APRT | VRF-derived random seed | MUST |
| REQ-M1-011 | 4.4.4 | M1 APRT | Embedding-based stability | MUST |
| REQ-M1-012 | 4.6 | M1 APRT | Enhanced full leave-one-out | MUST |
| REQ-M1-013 | 4.6 | M1 APRT | Enhanced trigger conditions | MUST |
| REQ-M2-001 | 5.3.1 | M2 CODS | Domain overlap normalization | SHOULD |
| REQ-M2-002 | 5.3.1 | M2 CODS | No K-class default distance | MUST |
| REQ-M2-003 | 5.3.1 | M2 CODS | Precedent lookback window | MAY |
| REQ-M2-004 | 5.3.2 | M2 CODS | Most-novel-feature rule | MUST |
| REQ-M2-005 | 5.3.2 | M2 CODS | N3 triple-AND condition | MUST |
| REQ-M2-006 | 5.3.2 | M2 CODS | Sparse domain safeguard | MUST |
| REQ-M2-007 | 5.4.1 | M2 CODS | Minimum query types | SHOULD |
| REQ-M2-008 | 5.4.2 | M2 CODS | Organic multiplier | SHOULD |
| REQ-M2-009 | 5.4.2 | M2 CODS | Separate LLM for contradiction | MUST |
| REQ-M2-010 | 5.4.3 | M2 CODS | Expected dissent calibration | MAY |
| REQ-M2-011 | 5.5 | M2 CODS | N3 Novelty Pathway routing | MUST |
| REQ-M2-012 | 5.5 | M2 CODS | Dissent weight mapping | MUST |
| REQ-M3-001 | 6.2 | M3 Purpose | Ambiguity-only invocation | MUST |
| REQ-M3-002 | 6.2 | M3 Purpose | No invocation for N3 | MAY |
| REQ-M3-003 | 6.3 | M3 Purpose | Separate evaluator model | SHOULD |
| REQ-M3-004 | 6.3 | M3 Purpose | Hard cap at 0.15 | MUST |
| REQ-M3-005 | 6.3 | M3 Purpose | High-purpose threshold 0.80 | MUST |
| REQ-M4-001 | 7.2 | M4 VRF | Domain separator prefix | MUST |
| REQ-M4-002 | 7.2 | M4 VRF | Previous hash chaining | MUST |
| REQ-M4-003 | 7.2 | M4 VRF | Proof storage | MUST |
| REQ-M4-004 | 7.3 | M4 VRF | Strength-biased threshold | SHOULD |
| REQ-M4-005 | 7.3 | M4 VRF | Bridge strength computation | MUST |
| REQ-M4-006 | 7.4 | M4 VRF | Anti-starvation force select | MUST |
| REQ-M4-007 | 7.4 | M4 VRF | Coverage boost age guard | MAY |
| REQ-M4-008 | 7.5 | M4 VRF | Constitutional VRF rate | MUST |
| REQ-M4-009 | 7.6 | M4 VRF | Reuse C3 key pairs | MUST |
| REQ-M5-001 | 8.2 | M5 Ladder | PROVISIONAL initial rung | MUST |
| REQ-M5-002 | 8.2 | M5 Ladder | SPECULATIVE exclusivity | MAY |
| REQ-M5-003 | 8.2 | M5 Ladder | Multiplicative influence | MUST |
| REQ-M5-004 | 8.4 | M5 Ladder | Corroboration independence | MUST |
| REQ-M5-005 | 8.4 | M5 Ladder | Quarantine blocks promotion | MUST |
| REQ-M5-006 | 8.4 | M5 Ladder | Fast-track criteria | SHOULD |
| REQ-M5-007 | 8.4 | M5 Ladder | CANONICAL promotion criteria | MAY |
| REQ-M5-008 | 8.5 | M5 Ladder | Demotion floor at PROVISIONAL | MUST |
| REQ-M5-009 | 8.5 | M5 Ladder | Cascade demotion 2+ events | MUST |
| REQ-M5-010 | 8.5 | M5 Ladder | Demotion resets tenure | MUST |
| REQ-M5-011 | 8.6 | M5 Ladder | PROVISIONAL floor fixed 0.50 | MAY |
| REQ-M5-012 | 8.6 | M5 Ladder | Domain-adaptive sigmoid/lerp | SHOULD |
| REQ-M5-013 | 8.7 | M5 Ladder | C10 backward compatibility | MAY |
| REQ-M6-001 | 9.2 | M6 Depth | Exclude SPECULATIVE/PROVISIONAL | MUST |
| REQ-M6-002 | 9.2 | M6 Depth | CORROBORATED weight 0.50 | MUST |
| REQ-M6-003 | 9.2 | M6 Depth | ESTABLISHED/CANONICAL weight 1.00 | MUST |
| REQ-M6-004 | 9.3 | M6 Depth | Filter before synthesis | MUST |
| REQ-M6-005 | 9.3 | M6 Depth | Non-K exempt from filtering | MUST |
| REQ-M6-006 | 9.4 | M6 Depth | Sandbox products at rung 0 | MUST |
| REQ-M6-007 | 9.4 | M6 Depth | SPECULATIVE excluded from sandbox | MUST |
| REQ-M6-008 | 9.4 | M6 Depth | Sandbox timeout enforcement | MUST |
| REQ-M6-009 | 9.4 | M6 Depth | Sandbox rate limit | MAY |
| REQ-M7-001 | 10.2 | M7 Immune | Signature extraction mandatory | MUST |
| REQ-M7-002 | 10.2 | M7 Immune | Three-level signatures | MUST |
| REQ-M7-003 | 10.2 | M7 Immune | 5-wide count buckets | MUST |
| REQ-M7-004 | 10.3 | M7 Immune | L1 priority | MUST |
| REQ-M7-005 | 10.3 | M7 Immune | L2 threshold 0.60 | MUST |
| REQ-M7-006 | 10.3 | M7 Immune | L3 similarity formula | MUST |
| REQ-M7-007 | 10.4 | M7 Immune | L1 automatic rejection | MUST |
| REQ-M7-008 | 10.4 | M7 Immune | L2 enhanced APRT + 0.20 | MUST |
| REQ-M7-009 | 10.4 | M7 Immune | L3 +0.10 + manual flag | MUST |
| REQ-M7-010 | 10.5 | M7 Immune | Persistent pattern doubled expiry | SHOULD |
| REQ-M7-011 | 10.5 | M7 Immune | 500-epoch no-trigger archival | MUST |
| REQ-M7-012 | 10.5 | M7 Immune | GC every epoch | MUST |
| REQ-M7-013 | 10.5 | M7 Immune | Eviction priority order | MUST |
| REQ-M7-014 | 10.5 | M7 Immune | Archive not delete | MAY |
| REQ-NP-001 | 11.2 | Novelty | All four entry criteria | MUST |
| REQ-NP-002 | 11.2 | Novelty | Failed-entry N3 standard path | MUST |
| REQ-NP-003 | 11.3.1 | Novelty | Full leave-one-out | MUST |
| REQ-NP-004 | 11.3.1 | Novelty | Minimum stability score | MUST |
| REQ-NP-005 | 11.3.2 | Novelty | 3+ objections, 1+ support | SHOULD |
| REQ-NP-006 | 11.3.2 | Novelty | Separate evaluator LLM | MUST |
| REQ-NP-007 | 11.3.2 | Novelty | < 0.50 address ratio = WEAK | MUST |
| REQ-NP-008 | 11.3.3 | Novelty | Mandatory quarantine | MUST |
| REQ-NP-009 | 11.3.3 | Novelty | Fast-track disabled in quarantine | MUST |
| REQ-NP-010 | 11.3.3 | Novelty | Corroborations counted, not acted | MUST |
| REQ-NP-011 | 11.3.4 | Novelty | Three-check deep audit | SHOULD |
| REQ-NP-012 | 11.3.4 | Novelty | KS test at 0.05 significance | MUST |
| REQ-NP-013 | 11.3.4 | Novelty | Framing threshold 0.60 | MUST |
| REQ-NP-014 | 11.4 | Novelty | Robustness < 0.50 = reject | MUST |
| REQ-NP-015 | 11.4 | Novelty | Suspicious + robustness < 0.70 | MUST |
| REQ-NP-016 | 11.4 | Novelty | Extended quarantine = 2x | MUST |
| REQ-NP-017 | 11.5 | Novelty | Early exit 3+ from 3+ parcels | MAY |
| REQ-NP-018 | 11.5 | Novelty | Rejection exit belief > 0.6 | MAY |
| REQ-INT-001 | 12.1 | Integration | Weights sum to 1.00 | MUST |
| REQ-INT-002 | 12.1 | Integration | L1 bypasses combined scoring | MUST |
| REQ-INT-003 | 12.2 | Integration | Constitutional thresholds | MUST |
| REQ-INT-004 | 12.2 | Integration | N3 bypasses combined scoring | MUST |
| REQ-INT-005 | 12.5 | Integration | 5x overhead budget | SHOULD |
| REQ-INT-006 | 12.5 | Integration | Operate within C10 rate limits | MUST |
| REQ-CFG-001 | 13.2 | Config | Weight sum validation | MUST |
| REQ-CFG-002 | 13.2 | Config | Threshold ordering | MUST |
| REQ-CFG-003 | 13.1 | Config | Constitutional governance | MUST |

**Total: 82 formal requirements** (44 MUST, 15 SHOULD, 12 MAY, 11 additional MUST from conformance)

---

## Appendix B: Hard Gate Verification Protocols

### B.1 INV-CRP1: VRF Unpredictability Verification

**Protocol:** For each consolidation decision, verify the VRF proof `pi` against the agent's public key and the VRF input. Any party can execute:

```
valid = ECVRF_verify(agent.pubkey, vrf_input, beta, pi)
```

If `valid == false`, the consolidation selection is fraudulent and MUST be rejected.

**Frequency:** Every consolidation decision.

### B.2 INV-CRP2: APRT Completeness Verification

**Protocol:** For each accepted or rejected consolidation, verify that APRT results are present in the decision record. Verify:
1. `aprt_result` is non-null
2. `aprt_result.robustness_score` is in [0.0, 1.0]
3. `aprt_result.case` is in {A, B, C} (standard) or ENHANCED (enhanced mode)
4. `aprt_result.resynthesis_count >= 1`

**Frequency:** Every consolidation decision. Automated check.

### B.3 INV-CRP5: Depth Enforcement Verification

**Protocol:** For each consolidation candidate set, verify that no K-class quantum with `credibility_rung <= 1` is present. Verify:
1. For each quantum `q` in the candidate set where `q.claim_class == "K"`:
   - Assert `q.credibility_rung >= 2`

**Frequency:** Every consolidation cycle. Automated check at candidate identification.

### B.4 INV-CRP6: Immune Memory Bounds Verification

**Protocol:** After each GC run, verify:
1. `immune_store.active_count() <= MAX_IMMUNE_SIGNATURES`
2. All archived signatures have been moved to archive storage
3. No active signature has `age > level_expiry` (accounting for match count doubling)

**Frequency:** Every epoch.

### B.5 INV-CRP7: Novelty Pathway APRT Verification

**Protocol:** For each Novelty Pathway decision, verify:
1. `enhanced_aprt_result` is non-null
2. `enhanced_aprt_result.all_stabilities` contains exactly N entries (one per quantum)
3. `enhanced_aprt_result.robustness_score == min(all_stabilities)`

**Frequency:** Every Novelty Pathway evaluation.

### B.6 INV-CRP8: M3 Cap Verification

**Protocol:** For each decision where M3 was invoked:
1. Assert `purpose_score <= M3_MAX_CONTRIBUTION` (0.15)
2. Assert `m3_invoked == True` only when ambiguity conditions hold

**Frequency:** Every consolidation decision where M3 is invoked.

---

## Appendix C: Adversary Cost Analysis

### C.1 Baseline: Pre-CRP+ Attack Cost

Without CRP+, an adversary needs to:

1. Plant quanta across 2+ domains that pass C10 Layer 1 (source independence): **Cost = 1 bridge**
2. Wait for deterministic selection: **Success probability = 1.0 per cycle**
3. Pass C10 Layer 2 adversarial probing: **Success probability ~0.7** (probe is single-shot)
4. Pass C10 Layer 5 validation: **Binary PENDING_VALIDATION with u >= 0.40**

**Baseline attack cost:** ~1.4 bridges per successful poisoning (1 / 0.7).

### C.2 CRP+ Attack Cost Multiplication

With CRP+, the adversary faces multiplicative barriers:

| Barrier | Multiplication Factor | Reasoning |
|---|---|---|
| M4 VRF Selection | 10x | At 10% selection rate, must plant ~10 bridges for 1 expected selection per cycle |
| M1 APRT Detection | ~3x | APRT detects ~67% of planted consolidations (Case A/B detection rate from FEASIBILITY analysis). Adversary needs ~3 attempts per bridge to pass. |
| M2 CODS (N1/N2) | ~1.5x | Dissent deficit detection catches ~33% of remaining. Adversary must manage dissent landscape. |
| M7 Immune Memory | ~1.2x | Previously rejected patterns are auto-detected. Adversary must vary approach. |
| M5 Credibility Ladder | Damage bounded | Even if poison passes, PROVISIONAL rung limits influence to 25%. Full impact requires manufactured corroboration (additional cost). |

**Combined multiplication:** 10 x 3 x 1.5 x 1.2 = **54x** before the PROVISIONAL influence cap.

**Conservative estimate (accounting for correlated defenses):** ~**30x** cost multiplication.

### C.3 Attack Cost in Quanta

| Scenario | Quanta Planted | Expected Successful Poisonings | Cost Per Poisoning |
|---|---|---|---|
| Pre-CRP+ | 10 | ~7 | ~1.4 quanta |
| CRP+ (standard) | 10 | ~0.33 | ~30 quanta |
| CRP+ (with manufactured corroboration to reach CORROBORATED) | 10 | ~0.33 at 50% influence | ~60 quanta (including corroboration quanta) |
| CRP+ (to reach ESTABLISHED for full influence) | 10 | requires 3+ corroborations + 50 epochs | ~100+ quanta + time cost |

### C.4 Time Cost

CRP+ adds temporal barriers:

- PROVISIONAL: minimum time before any consolidation participation
- CORROBORATED: requires independent corroboration (adversary must compromise additional agents)
- ESTABLISHED: 50+ epochs at CORROBORATED with zero challenges
- N3 Pathway: 5-10 cycle quarantine

An adversary seeking full-influence poisoning (ESTABLISHED rung) faces a minimum of ~60 epochs of operation, during which M7 immune memory is accumulating signatures and the system is learning the adversary's behavioral patterns.

---

## Appendix D: C9 Defense Invariant Compliance

CRP+ satisfies the following defense invariants from the C9 v2.0 9x9 contract matrix:

| Invariant | Description | CRP+ Compliance |
|---|---|---|
| INV-D1 | VTD Integrity | Not directly addressed. VTD integrity is C11 CACT's responsibility. CRP+ consumes VTD integrity signals as inputs to consolidation assessment. |
| INV-D2 | Detection Probability | Partial. CRP+ contributes to detection through APRT robustness testing (M1) and immune memory pattern matching (M7), but general detection is C11's domain. |
| INV-D3 | Collusion Resistance | Partial. M4 (VRF consolidation selection) adds unpredictability that reduces coordinated targeting, but general collusion defense is C12 AVAP's domain. |
| INV-D4 | Committee Independence | Not directly addressed. Committee independence is C12 AVAP's responsibility. |
| **INV-D5** | Consolidation Integrity | **PRIMARY.** CRP+'s 7-mechanism architecture (APRT, CODS, Source Purpose Scoring, VRF selection, Graduated Credibility Ladder, Depth Limits, Immune Memory) plus the Novelty Pathway achieve 30x adversary cost multiplication while preserving genuine discovery acceptance. Graduated trust (5-rung credibility ladder) bounds damage from any single poisoned claim. |

Full invariant definitions are in C9 v2.0 (Cross-Document Reconciliation, Defense Invariants section).

---

## Appendix E: Glossary

| Term | Definition |
|---|---|
| **APRT** | Adaptive Perturbation Robustness Testing. M1 mechanism testing whether consolidation conclusions survive input perturbation. |
| **Bridge** | A set of cross-domain edges in the coherence graph connecting quanta from different domains, representing a potential consolidation candidate. |
| **CANONICAL** | Credibility ladder rung 4. Highest trust level. Influence weight 1.00. Requires 5+ corroborations from 3+ parcels and 200+ epochs at ESTABLISHED. |
| **CODS** | Calibrated Organic Dissent Search. M2 mechanism measuring novelty-calibrated dissent deficit. |
| **Coherence Graph** | The graph structure (C6) connecting quanta via similarity, analogy, and causal edges within and across domains. |
| **Consolidation** | The EMA dreaming process (C6 Section 5.3) that synthesizes new K-class knowledge quanta from cross-domain bridge patterns. |
| **Consolidation Poisoning** | Adversarial strategy of planting quanta to manipulate automated consolidation into producing false K-class claims. |
| **CORROBORATED** | Credibility ladder rung 2. Influence weight 0.50. Requires 1+ independent DIRECT corroboration. |
| **CRP+** | Consolidation Robustness Protocol. The 7-mechanism defense architecture specified in this document. |
| **Dissent Deficit** | The gap between expected and actual counter-evidence for a consolidation claim. High deficit in well-mapped domains is suspicious. |
| **ECVRF** | Elliptic Curve Verifiable Random Function (RFC 9381). Cryptographic primitive producing verifiable pseudorandom outputs. |
| **EMA** | Epistemic Metabolism Architecture (C6). The knowledge processing pipeline including ingestion, circulation, consolidation, catabolism, and regulation. |
| **ESTABLISHED** | Credibility ladder rung 3. Influence weight 0.75. Requires 3+ corroborations including cross-parcel, 50+ epochs at CORROBORATED. |
| **FULL_SANDBOX** | Isolation constraint set for SPECULATIVE quanta: no consolidation, no credibility influence, no citation by non-sandboxed processes. |
| **Immune Memory** | M7 mechanism storing signatures of rejected consolidation patterns for future detection. |
| **Influence Weight** | Multiplicative factor (0.00-1.00) applied to a K-class quantum's contributions based on its credibility rung. |
| **K-class** | Knowledge-class quantum. Produced by dreaming consolidation. Represents synthesized cross-domain knowledge. |
| **N1 (Incremental)** | Novelty tier for consolidations extending known cross-domain connections. Full dissent deficit weight. |
| **N2 (Bridging)** | Novelty tier for consolidations connecting domains with some documented proximity. Reduced dissent deficit weight. |
| **N3 (Paradigmatic)** | Novelty tier for genuinely novel cross-domain connections with no prior documentation. Routes to Novelty Pathway. |
| **Novelty Pathway** | Dedicated scrutiny track for N3 claims using enhanced APRT, constructive probing, quarantine, and deep audit. |
| **PCVM** | Probabilistic Claim Verification Module (C5). Bayesian opinion fusion for claim credibility assessment. |
| **PROVISIONAL** | Credibility ladder rung 1. Default for new K-class quanta. Influence weight 0.25. |
| **Quantum** | The atomic unit of knowledge in the Atrahasis system. Contains claim content, provenance, and Subjective Logic opinion tuple. |
| **Robustness Score** | APRT output in [0,1]. Measures how much the consolidation conclusion depends on specific input quanta. Higher = more robust. |
| **Sentinel Graph** | Infrastructure fingerprinting system (C10) that clusters agents by behavioral and technical similarity. |
| **SPECULATIVE** | Credibility ladder rung 0. For sandboxed K->K consolidation products only. Influence weight 0.00. |
| **Stability** | Semantic similarity between original and re-synthesized claims. Used by APRT to measure robustness. |
| **Tidal Epoch** | The discrete time unit of the Tidal Noosphere (C3). System clock for all temporal operations. |
| **VRF** | Verifiable Random Function. Produces pseudorandom output with a proof of correctness. |

---

*End of C13 Master Technical Specification. This document is the final deliverable of the SPECIFICATION stage for invention C13 — Consolidation Poisoning Defense.*
