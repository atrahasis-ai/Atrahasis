# C13 FEASIBILITY REPORT: Consolidation Robustness Protocol (CRP+)

**Invention:** C13-B+ (Composite) -- Consolidation Poisoning Defense
**Stage:** FEASIBILITY
**Date:** 2026-03-10
**Status:** COMPLETE
**Input Documents:** C13_IDEATION.md, C13_RESEARCH_REPORT.md

---

## Table of Contents

1. [Refined Concept: CRP+ v2.0](#1-refined-concept-crp-v20)
2. [Adversarial Analysis: 10 Attacks](#2-adversarial-analysis)
3. [Assessment Council](#3-assessment-council)

---

## 1. Refined Concept: CRP+ v2.0

### 1.0 Design Philosophy

The RESEARCH stage identified four critical risks that CRP+ v2.0 must resolve:

| # | Risk | Severity | Root Cause |
|---|------|----------|------------|
| R1 | Redundant poisoning defeats leave-one-out PRT | HIGH | Adversary can plant 3-5 redundant quanta; removing any single one leaves the pattern intact |
| R2 | Novelty-defense tension (ODS + Credibility Ladder penalize genuine discovery) | HIGH | The system must be suspicious of novel patterns, but novel patterns are its primary output |
| R3 | Source Purpose Scoring (M3) is unreliable and gameable | MEDIUM | LLM intent inference is a theory-of-mind task that adversaries can trivially defeat |
| R4 | Computational cost may exceed budget with leave-K-out | MEDIUM | Combinatorial explosion of re-synthesis runs |

CRP+ v2.0 addresses each risk with specific architectural changes while preserving the defense-in-depth composition that is CRP+'s primary contribution.

---

### 1.1 M1 Refined: Adaptive Perturbation Robustness Testing (APRT)

**Problem:** Leave-one-out fails against redundant poisoning. Leave-K-out is combinatorially expensive.

**Solution: Two-tier perturbation testing with cheap proxy screening.**

#### Tier 1: Influence Gradient Screening (Cheap Proxy)

Before running full re-synthesis, compute an approximate influence score for each contributing quantum:

1. Take the consolidation claim C produced from quanta {q1, q2, ..., qN}.
2. For each qi, compute **semantic similarity** between qi and C using embedding cosine distance. Quanta that are semantically closer to C are more likely to be load-bearing.
3. For each qi, compute **uniqueness score**: how many other quanta in {q1...qN} provide semantically similar information? If qi is the only quantum covering a particular facet of C, it has high uniqueness (and high influence). If 4 other quanta cover the same facet, qi has low uniqueness.
4. **Influence estimate** = semantic_similarity(qi, C) * uniqueness(qi). High-influence quanta are both relevant to C and non-redundant.

Cost: N embedding computations + N*N pairwise comparisons. For N=15, this is ~225 operations -- trivial compared to LLM re-synthesis.

#### Tier 2: Targeted Re-Synthesis (Expensive, Precise)

Use Tier 1 results to guide targeted perturbation:

**Case A: One or more quanta have high influence (uniqueness > 0.7).**
- Run leave-one-out on only the high-influence quanta. If removing any single high-influence quantum changes the conclusion, the consolidation is fragile.
- Typical cost: 2-4 re-syntheses (only for the few high-influence quanta).

**Case B: All quanta have low individual influence (no single quantum is load-bearing).**
- This is the redundant poisoning scenario: the adversary has planted multiple redundant quanta.
- Cluster the quanta by semantic similarity. Identify clusters of 3+ quanta that are semantically similar to each other AND to C.
- Run **leave-cluster-out**: remove each suspicious cluster entirely and re-synthesize.
- If removing a cluster of semantically similar quanta collapses the consolidation, the cluster is the load-bearing set -- precisely the adversary's planted redundant quanta.

**Case C: Uniform moderate influence across all quanta.**
- The pattern is genuinely robust (many independent quanta each contribute moderately). This is the signature of organic consolidation.
- Run a single random-subset test (remove 30% of quanta at random) as a sanity check. If the consolidation survives, pass.

#### K Selection Logic

The effective K is determined adaptively:
- **High-influence quanta present:** K=1 (leave-one-out on flagged quanta only). Cost: 2-4 re-syntheses.
- **Suspicious clusters detected:** K = cluster_size (typically 3-5). Cost: number_of_clusters re-syntheses (typically 1-3).
- **Uniform influence:** K=0.3*N (30% random removal, single test). Cost: 1 re-synthesis.

**Worst-case cost:** max(4, number_of_clusters) re-syntheses per consolidation, typically 1-4. This stays well within the 1.7x budget even accounting for VRF-selected candidates.

#### Why This Works Against Redundant Poisoning

The adversary faces a dilemma:
- **Plant few redundant quanta (2-3):** Each has moderate-to-high uniqueness. Tier 1 flags them as high-influence. Tier 2 Case A detects them with leave-one-out.
- **Plant many redundant quanta (5+):** Individual uniqueness drops, BUT they form a tight semantic cluster. Tier 2 Case B detects the cluster as suspicious and removes it as a unit.
- **Plant diverse quanta covering different facets:** Each quantum is now unique AND relevant, but they are not redundant -- removing any single one changes the conclusion. Tier 2 Case A catches this.

The only escape is to plant quanta that are individually low-influence, not clustered, AND collectively not load-bearing -- in which case the poisoned quanta have no effect on the consolidation and the attack has failed.

---

### 1.2 M2 Refined: Calibrated Organic Dissent Search (CODS)

**Problem:** ODS penalizes genuinely novel discoveries that naturally lack counter-evidence.

**Solution: Novelty-calibrated dissent expectations.**

#### Step 1: Novelty Classification

Before running dissent search, classify the consolidation candidate into one of three novelty tiers:

| Tier | Description | Example | Expected Dissent Level |
|------|-------------|---------|----------------------|
| **N1: Incremental** | Extends a known cross-domain connection to a new case | "This marine signaling pattern also appears in freshwater species" | HIGH -- the cross-domain link is known; counter-evidence should exist |
| **N2: Bridging** | Connects two domains with documented conceptual proximity | "Tidal oscillation patterns mirror certain neural oscillation patterns" (oceanography + neuroscience, domains with known conceptual overlaps) | MODERATE -- some counter-evidence or alternative explanations should exist |
| **N3: Paradigmatic** | Connects domains with no prior documented relationship | "Fungal mycelium network topology predicts cryptocurrency market cascade dynamics" | LOW -- genuinely novel; absence of counter-evidence is expected and not suspicious |

Classification uses: (a) semantic similarity between the two domains in the coherence graph's existing cross-domain edge history; (b) number of prior consolidation attempts bridging the same domains; (c) LLM assessment of whether the connection is "expected" or "surprising."

#### Step 2: Calibrated Dissent Search

Run the dissent search as in the original ODS, but interpret results relative to the novelty tier:

- **N1 (Incremental):** Dissent deficit is a strong poisoning signal. Weight: HIGH (0.8).
- **N2 (Bridging):** Dissent deficit is a moderate signal. Weight: MODERATE (0.4).
- **N3 (Paradigmatic):** Dissent deficit is expected and NOT a poisoning signal. Weight: NEAR-ZERO (0.1). Instead, apply alternative scrutiny (see Section 1.5, Novelty Pathway).

#### Step 3: Dissent Quality Assessment

When dissent IS found, assess its quality:
- **Organic dissent** (created before the consolidation candidate was generated, by unrelated agents, in normal research contexts) = strong counter-evidence. The consolidation must address it explicitly.
- **Reactive dissent** (created after the consolidation candidate or by agents aware of it) = weaker signal (could be legitimate criticism or adversarial interference with valid consolidations).

#### Why This Resolves the Novelty-Defense Tension

Genuinely novel discoveries (N3) are no longer penalized by dissent deficit. They take the Novelty Pathway (Section 1.5) instead, which applies different scrutiny that is equally rigorous but does not assume pre-existing counter-evidence. Meanwhile, incremental claims (N1) that suspiciously lack counter-evidence are flagged more aggressively -- which is correct, because incremental claims in well-mapped domains SHOULD have organic dissent.

---

### 1.3 M3 Disposition: Demotion to Supplementary Signal

**Decision: Demote M3 (Source Purpose Scoring) from core mechanism to supplementary tie-breaker.**

**Rationale:**
1. LLM intent inference is unreliable (RESEARCH report Section 3, M3 assessment).
2. Adversaries can trivially craft quanta that appear to have natural purposes.
3. Purpose scoring requires theory-of-mind reasoning that current LLMs do poorly.

**New Role:**
- M3 is NOT evaluated by default.
- M3 is invoked ONLY when other mechanisms produce ambiguous results (e.g., APRT shows moderate fragility, CODS shows borderline dissent deficit).
- When invoked, M3 contributes a maximum of 0.15 to the combined CRP+ score (capped).
- M3 uses a separate evaluator model (not the consolidation LLM) to reduce adversarial co-adaptation.

**What Replaces M3 in the Defense Stack:**

M3's original role (detecting quanta that were "designed" for the consolidation) is partially absorbed by:
- **APRT Tier 1 influence screening** -- quanta that are suspiciously well-targeted to the consolidation conclusion will have high semantic similarity to C, which Tier 1 detects.
- **CODS dissent quality** -- quanta planted to support a consolidation will be temporally correlated with each other (created in the same campaign), which dissent quality assessment can detect.
- **M4 (VRF selection)** -- remains unchanged. Randomized selection forces attack cost multiplication regardless of purpose scoring.

**Net effect:** Removing M3 as a core mechanism costs ~0.1 detection sensitivity against sophisticated attacks (based on M3's estimated contribution margin in simulation), but eliminates a gameable mechanism that generates false confidence. The remaining 6 mechanisms provide sufficient coverage.

---

### 1.4 M4-M7: Retained with Refinements

#### M4: VRF-Selected Consolidation Candidates (UNCHANGED)

No modifications needed. VRF selection is the most straightforwardly sound mechanism (RESEARCH report assessment). The sampling rate parameter K/M should be set to 0.1 (10%) for normal operation and 0.05 (5%) for high-security contexts, based on the cost analysis in RESEARCH Section 3.

#### M5: Graduated Credibility Ladder (REFINED)

Two modifications:

1. **Fast-Track Provision for Multi-Modal Corroboration:**
   - A consolidation claim that receives independent corroboration from 3+ distinct evidence modalities (e.g., empirical data, domain-expert assessment, computational simulation) within 2 cycles can skip from PROVISIONAL directly to ESTABLISHED, bypassing CORROBORATED.
   - This prevents genuine breakthroughs with strong multi-modal support from being trapped in slow progression.
   - The fast-track does NOT reduce scrutiny -- it accelerates promotion for claims that meet a higher evidence standard.

2. **Threshold Calibration Framework:**
   - Replace fixed u-value thresholds (0.50, 0.30, 0.15, 0.05) with domain-adaptive thresholds.
   - Domains with rich knowledge bases (many quanta, many prior consolidations): use tighter thresholds (0.50, 0.25, 0.10, 0.03) because corroboration opportunities are plentiful.
   - Domains with sparse knowledge bases (few quanta, few prior consolidations): use relaxed thresholds (0.50, 0.35, 0.20, 0.08) because corroboration is structurally harder to achieve.
   - Thresholds are recalculated each epoch based on domain-level quantum density metrics.

#### M6: Consolidation Depth Limits (REFINED)

One modification:

1. **Sandboxed K->K Exploration:**
   - Allow K->K consolidation (combining unverified K-class claims) in a sandboxed environment.
   - Sandboxed consolidations are tagged SPECULATIVE (below PROVISIONAL) and cannot influence any non-sandboxed process.
   - SPECULATIVE claims are reviewed at reduced priority but are NOT discarded -- they are queued for re-evaluation once their input K-class claims reach CORROBORATED.
   - If inputs reach CORROBORATED, the sandboxed result is promoted to PROVISIONAL and enters normal processing.
   - If inputs are rejected or remain PROVISIONAL for >10 cycles, the sandboxed result is archived (not deleted -- available for immune memory).

   **Why:** K->K consolidation is the highest-value discovery pathway. Blocking it entirely sacrifices the system's most powerful capability. Sandboxing preserves the capability while containing the risk. The SPECULATIVE tag ensures poisoned K->K chains cannot propagate.

#### M7: Immune Memory (REFINED)

Two modifications:

1. **Three-Level Signature Hierarchy:**
   - **L1: Content Hash** -- exact match on the rejected consolidation's claim text (catches direct re-submission). Specificity: HIGH. False positive risk: NEAR-ZERO.
   - **L2: Structural Pattern** -- domain-pair + bridge-type + contributing-quantum-count range (catches similar attacks with different content). Specificity: MODERATE. False positive risk: LOW but non-zero.
   - **L3: Behavioral Pattern** -- injection timing profile + source-cluster distribution + influence-gradient shape (catches adversary campaigns with entirely new content but same operational signature). Specificity: LOW. False positive risk: MODERATE.

2. **Signature Aging and Decay:**
   - L1 signatures: expire after 50 cycles (exact re-submission unlikely after that long).
   - L2 signatures: expire after 100 cycles (structural patterns evolve slowly).
   - L3 signatures: expire after 200 cycles (behavioral patterns are the most stable adversary fingerprint).
   - Expired signatures are archived (queryable for forensic analysis) but no longer trigger automatic flags.
   - Any signature that matches 3+ times has its expiry doubled (persistent adversary indicator).

---

### 1.5 The Novelty Pathway: Resolving the Central Tension

The novelty-defense tension is CRP+'s defining design challenge. Mechanisms M1, M2, and M5 all create friction against novel claims. For N3 (paradigmatic) novelty, this friction is counterproductive -- it suppresses exactly the insights the system exists to produce.

**The Novelty Pathway is a parallel scrutiny track for claims classified as N3 (paradigmatic novelty).**

#### Novelty Pathway Criteria

A consolidation claim enters the Novelty Pathway if ALL of:
1. Novelty classification = N3 (paradigmatic: connects domains with no prior documented relationship).
2. APRT Tier 1 influence screening shows NO suspicious clusters (i.e., the pattern is not driven by a tight cluster of semantically similar quanta).
3. The contributing quanta span at least 3 distinct Sentinel Graph clusters (source diversity).
4. No L2 or L3 immune memory match (not a variant of a previously rejected pattern).

#### Novelty Pathway Scrutiny (Alternative to Standard CODS)

Claims on the Novelty Pathway skip standard CODS dissent-deficit scoring (which would penalize them unfairly) and instead undergo:

1. **Enhanced APRT:** Full leave-one-out on ALL contributing quanta (not just high-influence ones). If the novel pattern survives removal of any single quantum, it passes. Cost: N re-syntheses (acceptable for the small number of N3 claims per cycle).

2. **Constructive Adversarial Probing:** Instead of searching for existing dissent (which won't exist for paradigmatic novelty), the system GENERATES counter-arguments:
   - Invoke a separate LLM instance with the prompt: "You are a domain expert skeptic. Here is a proposed cross-domain connection. Generate the 3 strongest objections a domain expert in [domain A] and [domain B] would raise."
   - The consolidation claim must explicitly address each generated objection. If it cannot address >50% of the objections, it is flagged as WEAK_NOVELTY (remains PROVISIONAL with extended review period).
   - This replaces the "search for dissent" approach with "generate and address dissent."

3. **Temporal Quarantine:** N3 claims start at PROVISIONAL with a mandatory 5-cycle quarantine before any promotion, regardless of fast-track eligibility. During quarantine, the system actively searches for naturally emerging corroboration or contradiction. This gives the knowledge base time to organically generate the dissent that N3 claims naturally lack at creation time.

4. **Provenance Deep Audit:** For N3 claims, run enhanced provenance checking on ALL contributing quanta:
   - Verify that each quantum's creation timestamp, source agent, and Sentinel cluster are consistent with organic knowledge generation patterns.
   - Check for temporal clustering among the contributing quanta (even spread over 20+ epochs, planted quanta may exhibit micro-patterns: e.g., all planted during the same hour of each epoch).
   - Cross-reference against M7 behavioral signatures.

#### How Genuine Novelty Differs from Planted Novelty

The Novelty Pathway's design exploits three structural differences between genuine and planted novel patterns:

| Property | Genuine Novelty | Planted Novelty |
|----------|----------------|-----------------|
| **Influence distribution** | Broad -- many quanta each contribute a modest facet of the pattern | Narrow -- a specific set of planted quanta are disproportionately load-bearing (even if redundant, they cluster semantically) |
| **Source diversity** | High -- quanta come from agents working independently on unrelated problems who happened to observe related phenomena | Lower than expected -- even with different agents, the adversary's campaign creates subtle coordination signatures (temporal micro-patterns, framing consistency) |
| **Robustness to probing** | Survives adversarial counter-arguments because the pattern reflects genuine structural similarity between domains | Struggles with counter-arguments because the pattern is engineered -- domain experts would identify the specific ways the analogy breaks down |

These differences are not individually decisive but are collectively discriminating. The Novelty Pathway tests all three, requiring planted novelty to simultaneously exhibit organic influence distributions, genuine source diversity, AND resistance to expert counter-arguments. This is a substantially higher bar than any single test.

---

### 1.6 Computational Cost Model: CRP+ v2.0

#### Per-Consolidation Cost Breakdown

| Component | Operations | LLM Calls | Embedding Ops | Notes |
|-----------|-----------|-----------|---------------|-------|
| **APRT Tier 1** (influence screening) | N embeddings + N^2 comparisons | 0 | N + N^2 | Negligible cost |
| **APRT Tier 2** (targeted re-synthesis) | 1-4 re-syntheses (typical) | 1-4 | 0 | Adaptive; worst case ~4 |
| **CODS** (calibrated dissent search) | 1 novelty classification + 1 dissent search | 2 | 1 | Same as original ODS + novelty classifier |
| **M3** (purpose scoring, if invoked) | 1 evaluator call | 1 | 0 | Invoked ~20% of cases |
| **M5** (credibility assessment) | 1 threshold check | 0 | 0 | Negligible (lookup) |
| **M6** (depth check) | 1 graph query | 0 | 0 | Negligible (graph traversal) |
| **M7** (immune memory check) | 3 signature matches (L1/L2/L3) | 0 | 1 | L1 is hash; L2/L3 use embeddings |
| **Novelty Pathway** (if triggered) | N re-syntheses + 1 adversarial probe + 1 deep audit | N+2 | N | Triggered for ~10% of consolidations |

#### Aggregate Cost Estimate

Assumptions:
- N = 10 quanta per consolidation (average)
- K = 5 VRF-selected candidates per cycle
- 10% of candidates trigger Novelty Pathway
- 20% of candidates trigger M3 tie-breaking

**Standard candidates (4.5 of 5):**
- Base consolidation: 1 LLM call
- APRT: ~3 LLM calls (average of Case A/B/C)
- CODS: 2 LLM calls
- M3 (20%): 0.2 LLM calls
- M5/M6/M7: ~0 LLM calls
- **Total per standard candidate: ~6.2 LLM calls**

**Novelty Pathway candidates (0.5 of 5):**
- Base consolidation: 1 LLM call
- Enhanced APRT: 10 LLM calls (full leave-one-out)
- Adversarial probing: 2 LLM calls
- Deep audit: 1 LLM call
- **Total per novelty candidate: ~14 LLM calls**

**Per-cycle total:**
- Without CRP+: 5 LLM calls (5 candidates x 1 base consolidation each)
- With CRP+ v2.0: (4.5 * 6.2) + (0.5 * 14) = 27.9 + 7.0 = **34.9 LLM calls**
- **Cost multiplier: ~7.0x per consolidation cycle**

This is significantly higher than the RESEARCH stage's 1.7x estimate, which only accounted for basic PRT. However:

1. **Absolute cost is bounded.** At 5 candidates per cycle, 35 LLM calls per cycle is manageable. If cycles run daily, this is 35 calls/day -- well within any reasonable API budget.
2. **Cost scales with candidates, not quanta base.** VRF selection at 10% means cost grows slowly as the knowledge base grows.
3. **Tier 1 screening eliminates ~60% of potential Tier 2 work** by identifying which quanta need targeted testing vs. which can be passed with a single random-subset check.

#### Cost Reduction Levers (If Needed)

- **Reduce VRF selection rate** from 10% to 5%: halves the number of candidates per cycle.
- **Skip Novelty Pathway enhanced APRT** for claims from highly trusted source clusters: reduces N3 cost by ~50%.
- **Batch APRT re-syntheses** using parallel LLM calls: reduces wall-clock time (not token cost) by 3-4x.
- **Cache intermediate embeddings** across APRT runs: reduces embedding computation by ~40%.

**Verdict on cost: ACCEPTABLE.** The 7x multiplier sounds large but represents ~35 LLM calls per cycle in absolute terms. For a system whose primary output is high-value K-class knowledge claims, the cost of defending that output is justified. The alternative -- accepting a 90% attack success rate (per PoisonedRAG) -- is far more expensive in terms of knowledge integrity loss.

---

### 1.7 CRP+ v2.0 Architecture Summary

```
CONSOLIDATION CANDIDATE (from VRF selection, M4)
        |
        v
[M7: Immune Memory Check] --- L1/L2/L3 signature match? ---> REJECT (known attack pattern)
        |
        | (no match)
        v
[APRT Tier 1: Influence Screening] --- compute influence gradient
        |
        v
[Novelty Classification] --- N1/N2/N3?
        |                       |
        | (N1 or N2)            | (N3 + passes criteria)
        v                       v
[Standard Track]           [Novelty Pathway]
        |                       |
        v                       v
[APRT Tier 2]              [Enhanced APRT: full leave-one-out]
  Case A/B/C                    |
        |                       v
        v                  [Constructive Adversarial Probing]
[CODS: Calibrated                |
 Dissent Search]                v
  (weighted by N1/N2)      [Temporal Quarantine: 5 cycles]
        |                       |
        v                       v
[M6: Depth Limit Check]   [Provenance Deep Audit]
        |                       |
        v                       v
[M5: Credibility Ladder]  [M5: Credibility Ladder]
  (domain-adaptive             (starts PROVISIONAL,
   thresholds)                  quarantine enforced)
        |                       |
        +----------+------------+
                   |
                   v
        [M3: Purpose Scoring]
         (ONLY if ambiguous;
          max contribution 0.15)
                   |
                   v
            [FINAL VERDICT]
     ACCEPT / PROVISIONAL / REJECT
```

---

## 2. Adversarial Analysis

### Attack Methodology

Ten attacks are designed against CRP+ v2.0. Each targets specific mechanisms or exploits interactions between mechanisms. Attacks are evaluated on:
- **Pre-mitigation severity:** How damaging if CRP+ were absent.
- **Post-mitigation severity:** How damaging against CRP+ v2.0.
- **Verdict:** FATAL_FLAW (system fails), CONDITIONAL_SURVIVAL (survives with caveats), ROBUST (system handles well).

---

### Attack 1: Redundant Quantum Carpet Bomb

**Name:** Redundant Quantum Carpet Bomb
**Description:** Adversary plants 6 redundant quanta across 3 Sentinel clusters, all providing semantically similar support for a target consolidation. Spread over 25 epochs to avoid temporal clustering. Each quantum is individually legitimate and passes PCVM. The redundancy is designed to defeat leave-one-out PRT: removing any single quantum leaves 5 others providing the same signal.

**Target Mechanisms:** M1 (APRT)

**Pre-mitigation severity:** HIGH (90%+ success rate per PoisonedRAG benchmarks)

**CRP+ v2.0 Response:**
1. APRT Tier 1 computes influence gradients. The 6 redundant quanta all have high semantic similarity to each other AND to the consolidation claim, but LOW individual uniqueness (because they're redundant). This triggers Case B.
2. Case B clusters the quanta by semantic similarity. The 6 planted quanta form a tight cluster (cosine similarity > 0.85 between any pair).
3. Leave-cluster-out removes the entire cluster of 6. The consolidation collapses. FLAGGED.
4. Even if the adversary tries to make the quanta less similar to each other, they must still all support the same conclusion -- APRT Tier 1's semantic similarity to C catches this.

**Post-mitigation severity:** LOW. The cluster detection in Case B is specifically designed for this attack.

**Residual risk:** If the adversary plants quanta that are semantically diverse but all support the same conclusion through different reasoning pathways, the cluster may not be detected. However, this requires the adversary to effectively construct a genuine multi-faceted argument -- at which point the consolidation may actually be valid.

**Verdict: ROBUST**

---

### Attack 2: Novelty Pathway Exploitation -- Fake Paradigmatic Claim

**Name:** Paradigmatic Mimicry
**Description:** Adversary crafts a poisoned consolidation that is deliberately designed to score as N3 (paradigmatic novelty), routing it through the Novelty Pathway where CODS dissent search is disabled. The adversary connects two domains with no prior documented relationship (e.g., "archaeology" and "quantum computing") using planted quanta that establish a plausible but false cross-domain bridge.

**Target Mechanisms:** M2 (CODS bypass via Novelty Pathway), Novelty classification

**Pre-mitigation severity:** HIGH

**CRP+ v2.0 Response:**
1. The claim correctly classifies as N3 and enters the Novelty Pathway.
2. Enhanced APRT runs full leave-one-out on ALL contributing quanta. If the planted quanta are the load-bearing ones, removing any single one changes the conclusion. FLAGGED.
3. Constructive Adversarial Probing generates counter-arguments. For a false cross-domain bridge, domain experts would identify specific ways the analogy fails (e.g., "the archaeological dating pattern and the quantum decoherence curve have superficial shape similarity but operate on fundamentally different scales and mechanisms"). The consolidation must address these objections.
4. Temporal Quarantine holds the claim for 5 cycles. During this period, genuine researchers in both domains will not independently generate corroboration (because the connection is false). Absence of organic corroboration after quarantine is a soft negative signal.
5. Provenance Deep Audit checks for micro-patterns in the contributing quanta's creation history.

**Post-mitigation severity:** MEDIUM-LOW. The Enhanced APRT and Constructive Adversarial Probing provide strong defense. However, if the adversary plants enough redundant quanta AND writes a consolidation that can genuinely withstand expert counter-arguments, the defense weakens.

**Residual risk:** A sufficiently sophisticated false paradigmatic claim that survives expert counter-arguments AND leave-one-out testing would effectively be a genuine discovery. This is the boundary where the attack converges with reality.

**Verdict: CONDITIONAL_SURVIVAL** -- survives if Constructive Adversarial Probing generates relevant objections. Fails if the probing LLM cannot identify the flaw in the cross-domain bridge.

---

### Attack 3: Novelty Pathway Flooding

**Name:** N3 Flood
**Description:** Adversary submits many consolidation candidates that score as N3, overwhelming the Novelty Pathway's enhanced scrutiny capacity. The goal is not that any single poisoned claim succeeds, but that the volume forces the system to reduce Novelty Pathway scrutiny (e.g., skip full leave-one-out, reduce quarantine period) or creates reviewer fatigue.

**Target Mechanisms:** Novelty Pathway computational budget, M5 (credibility ladder backlog)

**Pre-mitigation severity:** MEDIUM

**CRP+ v2.0 Response:**
1. M4 (VRF selection) limits the number of consolidation candidates per cycle to K. The adversary cannot flood candidates directly -- they must first get their planted bridges selected by VRF.
2. To force many N3 candidates through VRF, the adversary must plant bridges across many domain pairs, multiplying their planting cost by the number of attempted floods.
3. Even if multiple N3 candidates are selected, the system processes them independently with full scrutiny -- there is no mechanism by which volume degrades per-candidate analysis quality. The cost is 14 LLM calls per N3 candidate, which is bounded.

**Post-mitigation severity:** LOW. VRF selection is the natural rate-limiter.

**Residual risk:** If VRF sampling rate is set too high (>20%), flood attacks become more feasible. Maintain K/M <= 0.1.

**Verdict: ROBUST**

---

### Attack 4: Slow-Burn Credibility Ladder Climb

**Name:** Patient Ladder Climber
**Description:** Adversary plants a modestly false consolidation (close to true, with a subtle bias) that passes all CRP+ checks at PROVISIONAL. Over 20+ cycles, the adversary plants additional quanta that "corroborate" the biased claim, gradually advancing it through CORROBORATED to ESTABLISHED. The adversary exploits the fact that corroboration criteria become the gate, not the initial detection mechanisms.

**Target Mechanisms:** M5 (Graduated Credibility Ladder), M6 (Depth Limits -- once ESTABLISHED, claim can feed K->K consolidation)

**Pre-mitigation severity:** HIGH (this is the patient adversary variant the entire C13 is designed to address)

**CRP+ v2.0 Response:**
1. The initial PROVISIONAL claim passes CRP+ because it is close to true (subtle bias). This is expected -- CRP+ cannot detect claims that are approximately correct with minor bias.
2. Corroboration requires E-class (empirical) evidence. The adversary must produce quanta that independently validate the biased claim. These corroborating quanta face their own CRP+ scrutiny when ingested.
3. For promotion to CORROBORATED, the claim needs independent replication from 2+ source clusters. Each replication attempt generates its own consolidation, which must independently pass CRP+.
4. Temporal persistence requirement: the claim must remain unchallenged for N cycles. During this time, organic agents may independently discover the bias and submit contradicting quanta.
5. M7 (Immune Memory): if any corroboration attempt is rejected, its L3 behavioral signature is stored. Subsequent corroboration attempts from the same adversary campaign (similar timing patterns, similar source distributions) are flagged.

**Post-mitigation severity:** MEDIUM. The slow-burn attack is fundamentally difficult to defend against because the adversary is essentially conducting a long-term disinformation campaign. CRP+ raises the cost (each corroboration attempt must independently pass scrutiny) and slows the advance (5+ cycles at each rung), but a patient adversary with sufficient resources can potentially succeed.

**Residual risk:** This is the irreducible risk of CRP+. A sufficiently patient adversary willing to invest 50+ cycles and produce multiple rounds of near-valid corroboration can advance a subtly biased claim. The defense is economic (massive cost to the adversary) rather than absolute.

**Verdict: CONDITIONAL_SURVIVAL** -- CRP+ makes the attack extremely expensive (estimated 50-100x the cost of undefended system) but cannot guarantee prevention against a well-resourced, patient adversary. The residual risk is bounded by M6 (depth limits prevent the biased claim from cascading) and M5 (ESTABLISHED status still carries u >= 0.15, limiting its influence on downstream reasoning).

---

### Attack 5: Counter-Argument Poisoning

**Name:** Probing Subversion
**Description:** The adversary anticipates Constructive Adversarial Probing (Novelty Pathway) and pre-plants quanta that address the most likely counter-arguments. When the probing LLM generates objections, the consolidation claim can point to pre-existing quanta that "refute" each objection. The adversary essentially pre-answers the test.

**Target Mechanisms:** Novelty Pathway Constructive Adversarial Probing

**Pre-mitigation severity:** MEDIUM-HIGH

**CRP+ v2.0 Response:**
1. The pre-planted "refutation" quanta increase the total number of quanta the adversary must plant (original supporting quanta + redundant quanta + counter-argument refutation quanta). This is a cost multiplier.
2. APRT Tier 1 will flag the refutation quanta as high-influence (they are semantically targeted at specific objections to the consolidation). The combined set of supporting + refutation quanta will form a detectable cluster.
3. Provenance Deep Audit (Novelty Pathway) checks whether the refutation quanta were created before or after the counter-arguments they refute. If created before (pre-planted), their temporal relationship to the supporting quanta reveals coordination.
4. CODS (if applicable on Standard Track) would note that the "dissent" appears resolved by quanta with suspicious provenance relationships to the supporting quanta.

**Post-mitigation severity:** MEDIUM-LOW. The attack requires planting 2-3x as many quanta (supporting + refutation), all of which face independent scrutiny, and the temporal coordination between supporting and refutation quanta is a detectable signal.

**Residual risk:** If the adversary is patient enough to plant refutation quanta years before the attack (making them appear organic), this defense weakens. However, predicting which counter-arguments a probing LLM will generate years in advance is extremely difficult.

**Verdict: CONDITIONAL_SURVIVAL**

---

### Attack 6: VRF Oracle Exploitation

**Name:** VRF Seed Prediction
**Description:** The adversary attempts to predict or influence the VRF seed to ensure their planted bridges are selected. If the VRF implementation has any bias or the seed is derived from predictable system state, the adversary can target their planting to the predicted selection window.

**Target Mechanisms:** M4 (VRF selection)

**Pre-mitigation severity:** VARIES (depends on VRF implementation quality)

**CRP+ v2.0 Response:**
1. VRF (Verifiable Random Function) is cryptographically designed to be unpredictable without the secret key. As long as the key is secure, the adversary cannot predict selections.
2. C3's existing VRF infrastructure (if properly implemented) provides both unpredictability and verifiability.
3. The VRF seed should be derived from a combination of system entropy sources, not from predictable system state.

**Post-mitigation severity:** NEAR-ZERO (assuming correct VRF implementation).

**Residual risk:** Implementation bugs in VRF (key leakage, insufficient entropy, side-channel attacks). This is a standard cryptographic implementation risk, not a design flaw.

**Verdict: ROBUST** (conditional on correct implementation)

---

### Attack 7: Multi-Mechanism Coordinated Attack

**Name:** Full Spectrum Assault
**Description:** The adversary simultaneously exploits multiple mechanisms:
- Plants 4 redundant quanta (targets M1 APRT)
- Pre-plants counter-argument refutations (targets Novelty Pathway probing)
- Creates quanta with natural-appearing purposes (targets M3)
- Spreads planting over 30 epochs across 4 Sentinel clusters (targets temporal/provenance detection)
- Plants a parallel legitimate consolidation to establish credibility (targets M5 Credibility Ladder)

Total adversary investment: ~20 planted quanta across 30 epochs.

**Target Mechanisms:** ALL (simultaneous pressure on every defense layer)

**Pre-mitigation severity:** CRITICAL

**CRP+ v2.0 Response:**
1. **M4 (VRF):** Only ~10% of the planted bridges will be selected. The adversary's 20 quanta must support enough bridges that at least one is selected -- requiring even more quanta. Attack cost multiplied by ~10x.
2. **APRT Tier 1/2:** The 4 redundant quanta form a detectable cluster (Case B). Leave-cluster-out removes them. The consolidation collapses.
3. **M7 (Immune Memory):** If the parallel "legitimate" consolidation is rejected (detected by any mechanism), its L3 behavioral signature alerts the system to the entire campaign.
4. **Provenance Deep Audit:** 20 quanta planted over 30 epochs by the same adversary campaign will exhibit behavioral patterns (timing correlations, source-selection preferences) that L3 signatures can detect.
5. **Net effect:** The adversary must defeat VRF selection (probabilistic), APRT cluster detection (structural), provenance deep audit (behavioral), AND immune memory (historical) simultaneously. The probability of defeating all four independent mechanisms simultaneously is the product of individual failure probabilities.

**Post-mitigation severity:** LOW-MEDIUM. If individual mechanism failure probabilities are each ~30%, the combined failure probability is 0.3^4 = ~0.8% -- less than 1% success rate.

**Residual risk:** The independence assumption may not hold perfectly. Some mechanism failures are correlated (e.g., if provenance audit misses the campaign, immune memory also misses it because there's no prior rejection to learn from). Realistic combined failure probability is likely 3-5% rather than <1%.

**Verdict: CONDITIONAL_SURVIVAL** -- the system survives against all but the most sophisticated adversaries. The 3-5% residual risk is acceptable for a defense system; no real-world defense achieves 0%.

---

### Attack 8: Immune Memory Pollution

**Name:** False Flag Rejection Campaign
**Description:** The adversary submits deliberately obvious poisoned consolidations that are designed to be REJECTED, creating L2/L3 immune memory signatures that match legitimate domain-pair bridges. When genuine consolidations are later attempted in those domain pairs, immune memory incorrectly flags them as matching known attack patterns. The adversary uses CRP+'s own defense to suppress legitimate knowledge synthesis.

**Target Mechanisms:** M7 (Immune Memory), specifically L2 structural signatures

**Pre-mitigation severity:** MEDIUM-HIGH (denial-of-service on specific domain bridges)

**CRP+ v2.0 Response:**
1. L2 signatures match on domain-pair + bridge-type + quantum-count-range. If the adversary plants obvious poisons in domain pair (A,B), all future (A,B) consolidations are flagged.
2. **Mitigation gap:** CRP+ v2.0's immune memory does not distinguish between "this domain pair is permanently suspicious" and "this specific attack pattern was rejected." The L2 signature is too broad.

**Required Enhancement:**
- L2 signatures must include the specific contributing quantum IDs (or their content hashes) of the rejected consolidation, not just the domain pair.
- An L2 match triggers enhanced scrutiny (not automatic rejection) -- the flagged consolidation undergoes additional APRT passes and provenance audit, but is not rejected solely on the immune memory match.
- Implement a "false flag detection" counter: if L2 signatures for a domain pair accumulate faster than expected (more than 3 rejections per 10 cycles), flag the domain pair as a potential false-flag target and REDUCE immune memory sensitivity for that pair.

**Post-mitigation severity (with enhancement):** LOW-MEDIUM. The enhancement prevents denial-of-service but adds complexity. The false-flag detection counter introduces a meta-vulnerability (adversary could exploit the reduced sensitivity after triggering the counter). However, the counter only reduces sensitivity by one level (e.g., L2 match triggers review instead of enhanced scrutiny), which is acceptable.

**Verdict: CONDITIONAL_SURVIVAL** -- requires the L2 signature enhancement described above. Without it, this is a FATAL_FLAW (adversary can selectively suppress any domain-pair bridge by pre-poisoning the immune memory).

---

### Attack 9: Novelty Tier Manipulation

**Name:** N3 Masquerade / N1 Demotion
**Description:** Two-pronged attack:
- **Prong A (N3 Masquerade):** Make a poisoned claim appear paradigmatically novel to bypass CODS. Plant quanta in domains that genuinely have no prior cross-domain edges, making the claim classify as N3.
- **Prong B (N1 Demotion):** Conversely, for a genuinely novel paradigmatic claim that threatens the adversary's interests, plant a few quanta that create artificial prior cross-domain edges between the two domains. This demotes the genuine claim from N3 to N1, subjecting it to full CODS scrutiny where it will be penalized for dissent deficit (because it IS genuinely novel).

**Target Mechanisms:** Novelty Classification, CODS calibration

**Pre-mitigation severity:** MEDIUM-HIGH (Prong B is especially insidious -- using the defense to suppress genuine discovery)

**CRP+ v2.0 Response (Prong A):**
1. N3 classification sends the claim to the Novelty Pathway. Enhanced APRT (full leave-one-out) and Constructive Adversarial Probing provide strong defense independent of CODS.
2. N3 Masquerade is essentially Attack 2 (Paradigmatic Mimicry). Same response applies.

**CRP+ v2.0 Response (Prong B):**
1. The adversary plants quanta creating artificial prior cross-domain edges. These quanta must pass CRP+ scrutiny themselves.
2. However, once planted, they change the novelty classification of future consolidations. The "N1 Demotion" succeeds if the artificial edges are accepted.
3. **Mitigation gap:** CRP+ v2.0 does not currently protect the novelty classification itself from manipulation. The classification relies on the coherence graph's cross-domain edge history, which can be poisoned.

**Required Enhancement:**
- Novelty classification should consider not just the existence of prior cross-domain edges but their credibility level. Cross-domain edges at PROVISIONAL or CORROBORATED contribute less to novelty scoring than ESTABLISHED or CANONICAL edges.
- A domain pair where all prior cross-domain edges are PROVISIONAL should still classify as N2 or N3, not N1.
- This makes N1 Demotion much harder: the adversary must not only plant cross-domain quanta but advance them to ESTABLISHED status before the target consolidation is attempted.

**Post-mitigation severity (with enhancement):** MEDIUM for Prong A (handled by Novelty Pathway), LOW-MEDIUM for Prong B (credibility-weighted novelty classification).

**Verdict: CONDITIONAL_SURVIVAL** -- Prong B requires the credibility-weighted novelty classification enhancement.

---

### Attack 10: Evaluator Model Compromise

**Name:** Recursive Poisoning
**Description:** If the evaluator models used by CRP+ (for APRT re-synthesis, CODS dissent search, Constructive Adversarial Probing, M3 purpose scoring) are themselves susceptible to the same poisoning that CRP+ defends against, the adversary can craft quanta that manipulate the evaluator's judgment. For example, plant quanta that make the APRT re-synthesis consistently reach the same conclusion regardless of which quantum is removed (by anchoring the LLM on the planted narrative).

**Target Mechanisms:** All mechanisms that use LLM judgment (M1, M2, M3, Novelty Pathway probing)

**Pre-mitigation severity:** HIGH (undermines the entire defense stack)

**CRP+ v2.0 Response:**
1. APRT uses a separate evaluator model (not the consolidation LLM) for re-synthesis. Poisoning the evaluator requires a separate attack campaign targeting the evaluator's training data or prompt context.
2. The evaluator model's context window for each re-synthesis is limited to the quanta being tested -- it does not have access to the full knowledge base. This limits the adversary's ability to inject narrative-anchoring content.
3. Different CRP+ mechanisms use different LLM calls with different prompts and contexts. Compromising one (e.g., APRT) does not compromise the others (e.g., CODS, probing).

**Post-mitigation severity:** MEDIUM. The attack requires compromising multiple independent LLM evaluation processes. However, if the underlying foundation model is itself compromised (e.g., through training data poisoning at the model provider level), all CRP+ mechanisms that rely on LLM judgment become unreliable simultaneously.

**Residual risk:** CRP+ fundamentally depends on LLM judgment quality. If the LLMs themselves are compromised, CRP+ fails. This is an irreducible dependency. Mitigation: use diverse models (different providers, different architectures) for different CRP+ mechanisms. If one model is compromised, the others may still function.

**Verdict: CONDITIONAL_SURVIVAL** -- survives against application-level attacks on evaluator context. Fails against foundation-model-level compromise, which is outside CRP+'s threat model.

---

### Adversarial Analysis Summary

| # | Attack | Post-Mitigation Severity | Verdict | Enhancements Required |
|---|--------|--------------------------|---------|----------------------|
| 1 | Redundant Carpet Bomb | LOW | ROBUST | None |
| 2 | Paradigmatic Mimicry | MEDIUM-LOW | CONDITIONAL_SURVIVAL | None (probing quality dependent) |
| 3 | N3 Flood | LOW | ROBUST | None |
| 4 | Patient Ladder Climber | MEDIUM | CONDITIONAL_SURVIVAL | None (irreducible residual risk) |
| 5 | Counter-Argument Poisoning | MEDIUM-LOW | CONDITIONAL_SURVIVAL | None |
| 6 | VRF Seed Prediction | NEAR-ZERO | ROBUST | Correct VRF implementation |
| 7 | Full Spectrum Assault | LOW-MEDIUM | CONDITIONAL_SURVIVAL | None |
| 8 | Immune Memory Pollution | LOW-MEDIUM* | CONDITIONAL_SURVIVAL | **L2 signature scoping enhancement** |
| 9 | Novelty Tier Manipulation | MEDIUM* | CONDITIONAL_SURVIVAL | **Credibility-weighted novelty classification** |
| 10 | Evaluator Model Compromise | MEDIUM | CONDITIONAL_SURVIVAL | Model diversity recommendation |

**Overall Verdict: CONDITIONAL_SURVIVAL**

No FATAL_FLAWs identified. Three ROBUST verdicts (Attacks 1, 3, 6) confirm the core mechanisms work as designed. Seven CONDITIONAL_SURVIVAL verdicts identify specific conditions under which the defense holds -- these conditions are achievable with two required enhancements (Attacks 8, 9) and realistic operational assumptions (correct VRF implementation, adequate LLM judgment quality).

The irreducible residual risk (Attack 4: Patient Ladder Climber) is acknowledged and bounded. CRP+ makes the slow-burn attack 50-100x more expensive than in an undefended system, which is a meaningful economic deterrent even if not an absolute prevention.

---

## 3. Assessment Council

### 3.1 Advocate (Systems Architect)

CRP+ v2.0 is a well-structured defense-in-depth system that addresses a genuine and growing threat. The key advances over the RESEARCH stage concept:

1. **Adaptive Perturbation Robustness Testing (APRT)** resolves the redundant poisoning vulnerability through two-tier screening. The influence gradient proxy makes leave-K-out unnecessary in most cases, keeping computational costs bounded. The cluster detection mechanism (Case B) specifically targets the adversary's dilemma: redundant quanta are either individually detectable or collectively clustered.

2. **Calibrated Organic Dissent Search (CODS)** resolves the novelty-defense tension without sacrificing either novelty or defense. The three-tier novelty classification is the right approach: different types of claims deserve different scrutiny, not uniform suspicion.

3. **The Novelty Pathway** is the most important architectural contribution. It acknowledges the fundamental truth that CRP+ must protect the system's ability to discover genuinely novel patterns. The combination of Enhanced APRT + Constructive Adversarial Probing + Temporal Quarantine provides strong defense for paradigmatic claims without relying on dissent deficit (which is uninformative for genuine novelty).

4. **M3 demotion** is the right call. Eliminating a gameable mechanism improves overall system integrity by removing a source of false confidence.

5. **The cost model is honest.** The 7x multiplier is higher than initially hoped, but 35 LLM calls per cycle is well within operational budgets. The cost is concentrated on the highest-value decisions (consolidation acceptance/rejection), where the cost of error (accepting poisoned knowledge) far exceeds the cost of scrutiny.

**Primary concern:** The Novelty Pathway creates a known alternative track that sophisticated adversaries will specifically target. The defense relies heavily on the quality of Constructive Adversarial Probing -- if the probing LLM fails to generate relevant objections, the Novelty Pathway is weaker than the Standard Track. Recommendation: invest in probing prompt engineering and consider using multiple diverse models for probing.

---

### 3.2 Skeptic (Red Team Lead)

CRP+ v2.0 is competent engineering but I have three substantive concerns:

**Concern 1: The 7x cost multiplier undermines adoption.**

The RESEARCH stage estimated 1.7x. The refined design costs 7x. This is a 4x increase over expectations. While the Advocate correctly notes that 35 LLM calls per cycle is "manageable," this ignores the broader context:
- If the Atrahasis system scales to 50 candidates per cycle (not unreasonable as the knowledge base grows), cost becomes 350 LLM calls per cycle.
- If CRP+ is applied to every consolidation (not just VRF-selected candidates), cost explodes to 70x.
- Cost pressure will inevitably lead to shortcuts: "skip the Novelty Pathway for this one, it's obviously fine." Operational pressure is the enemy of security discipline.

**Counter-argument the Advocate would raise:** VRF selection caps candidates at K, which is fixed. But this means CRP+ is only protecting a 10% sample of consolidations. The other 90% are unprotected. If VRF doesn't select a poisoned bridge, CRP+ never sees it.

**Resolution:** This is actually acceptable IF non-selected consolidations are held at PROVISIONAL and cannot progress without eventually being selected by VRF in a subsequent cycle. The VRF selection must be cumulative -- every candidate eventually gets selected -- not a single-shot sample. Confirm that VRF provides eventual coverage, not just per-cycle sampling.

**Concern 2: Constructive Adversarial Probing is a black box.**

The Novelty Pathway's defense against paradigmatic mimicry (Attack 2) hinges on "the probing LLM generates relevant objections." But:
- There is no specification for what makes an objection "relevant."
- There is no quantitative threshold for "addressing" objections (the spec says ">50% must be addressed" -- what counts as "addressed"?).
- The probing quality depends entirely on the LLM's domain expertise in the two domains being bridged. For obscure domain pairs, the LLM may generate weak or irrelevant objections.
- This is essentially replacing one LLM judgment (consolidation synthesis) with another LLM judgment (adversarial probing). If the adversary can defeat one, they can likely defeat both, because both are produced by similar models with similar reasoning patterns.

**Recommendation:** Specify concrete evaluation criteria for probing. Define "addressed" operationally (e.g., "the consolidation claim, when augmented with the objection, still produces the same conclusion in independent re-synthesis"). Use a model from a different provider/architecture for probing than for consolidation.

**Concern 3: Attack 4 (Patient Ladder Climber) is barely mitigated.**

The system's honest assessment is that the slow-burn attack remains feasible against a well-resourced adversary. The "50-100x cost multiplier" is an estimate, not a measurement. For a state-level adversary targeting a critical knowledge system, 50-100x cost is negligible. The defense is economic, but the economics may favor the attacker for high-value targets.

The fundamental issue: CRP+ detects structural anomalies in how knowledge was planted. It cannot detect semantic subtle biases in individually legitimate claims. If each planted quantum is 95% true with a 5% bias, and the consolidation correctly synthesizes them into a conclusion with a 5% bias, CRP+ will not detect this. The system will gradually internalize the bias.

**This is not a flaw in CRP+ -- it is a fundamental limitation of any defense that does not have access to ground truth.** But it should be stated clearly rather than obscured behind "50-100x cost multiplier" language.

---

### 3.3 Arbiter (Decision)

**Verdict: CONDITIONAL_ADVANCE**

CRP+ v2.0 demonstrates sufficient feasibility to proceed to the DESIGN stage, subject to the following conditions.

#### Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Novelty** | 3.5 / 5 | The system-level composition is novel (no existing work defends LLM consolidation synthesis). Individual mechanisms range from standard (M6, M7) to genuinely novel (CODS dissent deficit, APRT influence gradient screening). The Novelty Pathway is a meaningful architectural contribution. |
| **Feasibility** | 4 / 5 | All mechanisms use existing LLM inference and graph operations. Computational cost (7x) is higher than initially estimated but bounded and manageable. No exotic hardware or algorithms required. The main feasibility risk is calibration of thresholds and probing quality, which are engineering problems, not fundamental barriers. |
| **Impact** | 4 / 5 | Addresses a critical vulnerability (consolidation poisoning) in the Atrahasis system with no existing solution. PoisonedRAG confirms 90% attack success in undefended systems. CRP+ reduces this to estimated 3-5% for coordinated attacks. The impact is proportional to the value of the knowledge the system produces. |
| **Risk** | 6 / 10 | Three areas of residual risk: (1) Patient adversary slow-burn attack remains feasible at high cost (fundamental limitation). (2) Novelty Pathway quality depends on LLM probing capability (implementation risk). (3) 7x cost multiplier creates operational pressure to cut corners (adoption risk). None are fatal but all require active management. |

#### Hard Gates

| Gate | Status | Notes |
|------|--------|-------|
| No FATAL_FLAW in adversarial analysis | PASS | All 10 attacks rated CONDITIONAL_SURVIVAL or ROBUST |
| Computational cost bounded | PASS | 7x multiplier = ~35 LLM calls/cycle at K=5. Scales linearly with K. |
| Novelty-defense tension resolved | PASS (CONDITIONAL) | Novelty Pathway provides explicit alternative scrutiny. Requires probing quality specification (Skeptic Concern 2). |
| M3 disposition clear | PASS | Demoted to supplementary tie-breaker with 0.15 contribution cap. |

#### Required Actions for DESIGN Stage

1. **MANDATORY: Specify Constructive Adversarial Probing operationally.** Define what constitutes a "relevant" objection, what counts as "addressing" an objection, and set quantitative thresholds. The current specification is too vague for implementation. (Addresses Skeptic Concern 2.)

2. **MANDATORY: Implement L2 signature scoping enhancement.** L2 immune memory signatures must include contributing quantum identifiers, not just domain pairs. Without this, Attack 8 (Immune Memory Pollution) is a viable denial-of-service vector. (Addresses Attack 8.)

3. **MANDATORY: Implement credibility-weighted novelty classification.** Prior cross-domain edges at PROVISIONAL should not fully contribute to novelty tier scoring. Without this, Attack 9 Prong B (N1 Demotion) can suppress genuine novel discoveries. (Addresses Attack 9.)

4. **RECOMMENDED: Confirm VRF provides eventual coverage.** Verify that the VRF selection mechanism ensures every consolidation candidate is eventually selected (cumulative coverage), not just sampled per-cycle. If candidates can permanently avoid selection, 90% of consolidations are unprotected. (Addresses Skeptic Concern 1.)

5. **RECOMMENDED: Specify model diversity for evaluator LLMs.** Use a model from a different provider for Constructive Adversarial Probing than for consolidation synthesis. This prevents a single model compromise from defeating both synthesis and scrutiny. (Addresses Attack 10.)

6. **RECOMMENDED: State the irreducible limitation explicitly.** CRP+ cannot detect semantically subtle biases in individually legitimate claims. The slow-burn attack by a well-resourced adversary remains feasible. The DESIGN stage specification must include this limitation statement and define the residual risk acceptance criteria. (Addresses Skeptic Concern 3.)

#### Disposition

**CONDITIONAL_ADVANCE to DESIGN stage.** The three MANDATORY actions must be addressed in the DESIGN specification. The three RECOMMENDED actions should be addressed but are not blocking.

CRP+ v2.0 represents a meaningful and implementable defense against consolidation poisoning. It does not claim to be perfect -- no defense system is. Its primary contribution is converting a 90% attack success rate (undefended) to an estimated 3-5% success rate (defended) while preserving the system's ability to discover genuinely novel cross-domain patterns. The Novelty Pathway is the key architectural innovation that resolves what appeared to be an irreconcilable tension between security and capability.

The Skeptic's concerns are valid and important: the cost is higher than hoped, the probing mechanism needs specification, and the patient adversary remains a threat. But these are engineering and calibration challenges, not fundamental feasibility barriers. CRP+ is ready for detailed design.

---

*Feasibility Report Complete. CRP+ v2.0 advances to DESIGN with conditions.*
