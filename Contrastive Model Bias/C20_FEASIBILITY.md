# C20 — Contrastive Model Training Bias Framework — FEASIBILITY

**Invention ID:** C20
**Stage:** FEASIBILITY
**Date:** 2026-03-11
**Selected Concept:** C20-A (Contrastive Model Training Bias Framework — CMTBF)
**Normative Reference:** C17 Section 12 (Contrastive Learning Model, Phase 2+)

---

# PART 1 — DOMAIN TRANSLATOR: SUB-PROBLEM ANALOGIES

## Sub-Problem 1: How to detect model family dominance in training data

**Analogy: Crop monoculture detection in agriculture.** Agricultural inspectors detect monoculture risk by measuring Simpson's diversity index across planted species. If one species exceeds 60% of total acreage, the ecosystem is fragile. Apply the same principle: measure Simpson's diversity index across model families in training pairs. If any family exceeds a threshold, the training data is "monocultural" and the contrastive model will overfit to that family's behavioral signature.

## Sub-Problem 2: How to verify training pair labels without ground truth

**Analogy: Peer review in academic publishing.** No single reviewer can certify a paper's correctness. Instead, 2-3 independent reviewers assess it, and agreement among reviewers is the proxy for quality. Apply to training labels: require that each positive pair (same-origin) be confirmed by at least 2 independent evidence sources (e.g., L1 economic analysis + L2 statistical B score). Each negative pair (independent) must have at least 2 independence signals. This is the "label traceability chain."

## Sub-Problem 3: How to detect adversarial label poisoning

**Analogy: Counterfeit currency detection in central banking.** Central banks detect counterfeit bills not by examining each bill individually but by monitoring statistical anomalies in currency flow — unusual concentrations, serial number patterns, geographic clustering. Apply to training data: monitor for anomalous clusters of training pairs that share unusual feature distributions, temporal clustering, or source concentration. Spectral signature analysis is the mathematical equivalent.

---

# PART 2 — COMMERCIAL VIABILITY ASSESSOR (Early Activation)

**Score: 3.5/5 — Viable as Internal Infrastructure**

C20 is not revenue-generating. It is a quality assurance framework for C17's Phase 2 contrastive model. Commercial viability is measured by cost-effectiveness.

**Cost analysis:**
- Development cost: ~2-3 person-months of ML engineering to implement the 3-layer validation pipeline
- Per-training-cycle cost: ~4-8 GPU-hours for influence function analysis on 5,500 training pairs (one-time per quarterly retraining)
- Ongoing monitoring: <1% overhead on C17's Phase 2 pipeline (distribution checks, embedding monitoring)
- Human review: ~1 person-day per quarterly Training Data Quality Report

**Value proposition:** A biased contrastive model would either (a) produce false positives — falsely flagging legitimate agents as Sybils, causing governance injustice and Constitutional Tribunal challenges, or (b) produce false negatives — missing real Sybils, undermining MCSD Layer 2. Either outcome has costs far exceeding C20's operational overhead.

**Adoption barrier:** None — C20 is mandatory infrastructure for C17 Phase 2 deployment per Monitoring Flag 3.

---

# PART 3 — ADVERSARIAL ANALYST REPORT

## 10 Attacks Against CMTBF

### Attack 1: Overwhelming Model Family Injection
**Description:** Adversary floods Phase 0-1 with agents from a single model family (e.g., 500 Llama-based agents), ensuring training data is dominated by that family. When Phase 2 contrastive model deploys, it flags all Llama agents as "similar" (high false positive rate for Llama) while being blind to Sybils from other families.
**Severity:** HIGH
**C20 Defense:** Model family distribution monitoring (Simpson's diversity index). Training data DQS gate rejects data with diversity index < 0.60.
**Residual risk:** Adversary cannot control ALL agents in the ecosystem, but can skew the population enough to degrade diversity metrics. Defense is effective if threshold is calibrated.

### Attack 2: Clean-Label Poisoning
**Description:** Adversary creates genuinely independent agents that happen to share behavioral patterns with their (concealed) Sybils. These independent agents are correctly labeled as "negative" (independent). But their presence in training data "pulls" the negative cluster toward the Sybil behavioral space, making the boundary less discriminative.
**Severity:** HIGH
**C20 Defense:** Spectral signature analysis detects anomalous clusters in the negative training set. Influence function analysis identifies training pairs that disproportionately affect model predictions on suspicious test pairs.
**Residual risk:** Sophisticated adversary can distribute poisoned examples to avoid spectral clustering. This is the hardest attack to defend against.

### Attack 3: Temporal Data Staleness Exploitation
**Description:** Adversary waits for a major model family transition (e.g., GPT-4 to GPT-5) and registers Sybils immediately after the transition. The contrastive model, trained on GPT-4-era data, has not learned GPT-5 behavioral signatures and cannot detect GPT-5-based Sybils.
**Severity:** MEDIUM
**C20 Defense:** Temporal holdout validation detects performance degradation on newer data. Quarterly retraining incorporates new data. Automatic rollback if FPR exceeds limits.
**Residual risk:** There is an inherent vulnerability window between a model transition and the next retraining cycle (up to 3 months).

### Attack 4: Label Source Manipulation
**Description:** Adversary causes their Sybil agents to be detected by Layer 3 (social graph) but not Layer 2 (behavioral). The Layer 3 detection generates "confirmed same-origin" labels for training data — but these labels are based on social coordination, not behavioral similarity. Training on these misleading labels degrades behavioral detection.
**Severity:** MEDIUM
**C20 Defense:** Label provenance tracking with source-specific confidence weights. Layer 3/4 detections carry lower confidence for behavioral training (they confirm same-controller, not same-origin). Multi-source confirmation requires behavioral evidence for positive pair labels.
**Residual risk:** If multi-source confirmation is too strict, training data volume decreases, weakening the model.

### Attack 5: Infrastructure Mimicry
**Description:** Adversary deploys independent agents on identical infrastructure to make them appear same-origin in BFE features. These independent-but-infrastructure-identical pairs become false positives in training data validation (flagged as suspicious when they are actually legitimate).
**Severity:** LOW
**C20 Defense:** Infrastructure-aware stratification separates infrastructure correlation from origin correlation. Training pairs are stratified to include same-infrastructure-different-origin pairs.
**Residual risk:** If infrastructure-identical pairs are excluded from training, the model may lose the ability to distinguish infrastructure similarity from origin similarity.

### Attack 6: Validation Gaming
**Description:** Adversary submits agents that behave "normally" during SEB evaluation but switch to evasive behavior afterward. Training data from SEB is valid, but the contrastive model trained on SEB data does not generalize to organic behavior.
**Severity:** MEDIUM
**C20 Defense:** C17 already includes organic behavioral observation alongside SEB (Section 7). Training data includes both SEB and organic pairs. Task bias monitoring ensures SEB/organic balance.
**Residual risk:** Minimal — C17's design already addresses this.

### Attack 7: Training Data Volume Denial
**Description:** Adversary suppresses the generation of positive training pairs by ensuring their Sybils are not detected by any layer during Phase 0-1. With fewer positive pairs, the contrastive model has insufficient training data and C20's DQS gate prevents deployment.
**Severity:** LOW
**C20 Defense:** Synthetic positive pair generation (C17 Section 12.2) supplements organic detections. DQS threshold is calibrated to be achievable with synthetic + organic data combined.
**Residual risk:** Synthetic data may not fully represent real adversarial Sybil behavior.

### Attack 8: Influence Function Evasion
**Description:** Adversary crafts poisoned training pairs that individually have low influence (below detection threshold) but collectively shift the decision boundary. Each pair is "innocent" in isolation; the attack is distributed.
**Severity:** MEDIUM
**C20 Defense:** Aggregate influence analysis (measure collective influence of subsets, not just individual pairs). Spectral analysis on the full training set detects distributed anomalies.
**Residual risk:** Aggregate influence analysis is computationally expensive (combinatorial over subsets). Practical implementation must use sampling-based approximation.

### Attack 9: Subgroup Targeting
**Description:** Adversary poisons training data to increase FPR specifically for a minority model family (e.g., a small open-source model used by <5% of agents). This model family has few representatives in validation data, so the per-family FPR violation is not detected with statistical significance.
**Severity:** MEDIUM
**C20 Defense:** Per-family FPR monitoring with Bonferroni correction for multiple comparisons. Minimum sample size requirement for per-family validation (at least 50 pairs per family).
**Residual risk:** Families with <50 pairs cannot be individually validated. Grouped validation (all families with <50 pairs analyzed together) provides partial coverage.

### Attack 10: Feedback Loop Exploitation
**Description:** Adversary exploits the retraining cycle: Phase 2 model detects Sybils, which become training data for the next retraining cycle. Adversary crafts Sybils that, when detected, produce training examples that degrade the next model iteration. This creates a self-reinforcing degradation loop.
**Severity:** HIGH
**C20 Defense:** Holdout-based regression testing — each retrained model is validated against a fixed "golden" holdout set from Phase 0-1. If performance on the golden set degrades, retraining is rejected. The golden set is curated once and never updated (preventing contamination).
**Residual risk:** The golden set may become stale as the agent population evolves. Periodic golden set refresh introduces re-contamination risk.

---

# PART 4 — FEASIBILITY VERDICT

## Ideation Council Reconvened (with Research Data)

### Visionary:
Research confirms all 6 bias dimensions are scientifically grounded. The adversarial attacks validate the need for multi-layered defense. I maintain the CMTBF concept with phased implementation.

### Systems Thinker:
The 3-layer validation pipeline is implementable with proven components. The main engineering risk is influence function computation cost, which Kong & Chaudhuri (2022) confirm is feasible for C17's MLP scale. I refine the architecture to include the golden holdout set for regression testing (from Attack 10 defense).

### Critic:
Research confirms novelty score 3 (novel combination, not breakthrough). Individual techniques are well-known. The domain-specific taxonomy and adversarial label provenance chain are the genuinely novel elements. I accept ADVANCE with the condition that the specification clearly delineate C20-original contributions from applied prior art.

---

## Assessment Council Preliminary Verdict

```json
{
  "type": "FEASIBILITY_VERDICT",
  "invention_id": "C20",
  "stage": "FEASIBILITY",
  "decision": "ADVANCE",
  "novelty_score": 3,
  "feasibility_score": 4,
  "impact_score": 3.5,
  "risk_score": 4,
  "risk_level": "MEDIUM",
  "required_actions": [
    "Specify concrete algorithm for multi-source label confirmation (label traceability chain)",
    "Define golden holdout set curation protocol",
    "Specify computational budget for influence function analysis per retraining cycle"
  ],
  "monitoring_flags": [
    "Per-family FPR validation requires minimum 50 pairs per family — may not be achievable for rare families at Phase 2 entry",
    "Aggregate influence function analysis is computationally expensive — sampling-based approximation must be validated",
    "Clean-label poisoning remains a residual risk with no complete defense"
  ],
  "pivot_direction": null,
  "rationale": "CMTBF is a feasible and necessary framework for C17 Phase 2 deployment. All component technologies are proven. The 6-dimension bias taxonomy is domain-specific and novel in combination. Adversarial risks are real but manageable through multi-layered defense. Phased implementation aligns with C17's deployment timeline."
}
```

---

**End of FEASIBILITY.**
