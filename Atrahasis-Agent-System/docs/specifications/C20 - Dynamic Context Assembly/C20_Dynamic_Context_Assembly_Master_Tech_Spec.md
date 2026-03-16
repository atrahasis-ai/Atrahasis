# C20 — Contrastive Model Training Bias Framework (CMTBF)

## Master Technical Specification

**Document ID:** C20-MTS-v1.0
**Version:** 1.0.0
**Date:** 2026-03-11
**Invention ID:** C20
**System:** Atrahasis Agent System v2.0
**Status:** SPECIFICATION COMPLETE
**Classification:** CONFIDENTIAL — Atrahasis LLC
**Assessment Council Verdict:** ADVANCE (Novelty 3/5, Feasibility 4/5, Impact 3.5/5, Risk 4/10 MEDIUM)
**Normative References:** C17 (MCSD Layer 2 v1.0 — Section 12), C5 (PCVM v2.0), C14 (AiBC v1.0)
**Resolves:** C17 Monitoring Flag 3: "Training data for Phase 2 contrastive model must be validated for bias."

---

## Abstract

C17 defines a Phase 2 contrastive learning model — a Siamese network producing 128-dimensional embeddings — trained on labeled pairs of AI agent behavioral traces to detect same-origin Sybil agents. Monitoring Flag 3 identifies that training data bias could cause the contrastive model to learn spurious correlations (e.g., model family signatures rather than origin signatures), produce unfair false positive rates across agent subgroups, or be vulnerable to adversarial data poisoning.

This specification defines the Contrastive Model Training Bias Framework (CMTBF): a 6-dimensional bias taxonomy specific to behavioral trace contrastive learning, a 3-layer validation pipeline (pre-training, intra-training, post-training), a label traceability chain requiring multi-source confirmation for training pair labels, and a Training Data Quality Report (TDQR) that must accompany every model version. CMTBF gates C17 Phase 2 contrastive model deployment: no model deploys without passing the Deployment Readiness Score (DRS >= 0.90). If validation fails, C17 falls back to statistical-only B(a_i, a_j).

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Motivation and Gap Analysis](#2-motivation-and-gap-analysis)
3. [Bias Taxonomy](#3-bias-taxonomy)
4. [Layer 1: Pre-Training Validation](#4-layer-1-pre-training-validation)
5. [Layer 2: Intra-Training Monitoring](#5-layer-2-intra-training-monitoring)
6. [Layer 3: Post-Training Validation](#6-layer-3-post-training-validation)
7. [Training Data Quality Report (TDQR)](#7-training-data-quality-report-tdqr)
8. [Integration with C17](#8-integration-with-c17)
9. [Adversarial Defenses](#9-adversarial-defenses)
10. [Phased Deployment](#10-phased-deployment)
11. [Formal Requirements](#11-formal-requirements)
12. [Parameters](#12-parameters)
13. [Patent-Style Claims](#13-patent-style-claims)
14. [Risk Analysis](#14-risk-analysis)
15. [Glossary](#15-glossary)
16. [References](#16-references)

---

## 1. Executive Summary

The C17 Phase 2 contrastive model is trained on pairs of AI agent behavioral traces labeled as "same-origin" or "independent-origin." This training data can be biased in 6 ways: infrastructure correlation, model family dominance, task distribution skew, temporal staleness, population non-representativeness, and adversarial poisoning. Each bias type degrades the contrastive model differently — from unfair false positive rates against minority model families to adversary-exploitable blind spots.

CMTBF addresses all 6 bias types through a 3-layer validation pipeline:

1. **Pre-Training Validation (Layer 1):** Validates training data quality before training begins. Checks schema conformance, label provenance (multi-source traceability chain), distribution balance (model family, infrastructure, task), and adversarial anomalies (spectral signatures, influence screening). Produces a Data Quality Score (DQS). Training proceeds only if DQS >= 0.80.

2. **Intra-Training Monitoring (Layer 2):** Monitors the training process for embedding collapse, per-family loss divergence, and feature shortcut reliance. Produces an advisory Training Quality Score (TQS). TQS < 0.70 triggers investigation but does not hard-abort training.

3. **Post-Training Validation (Layer 3):** Validates the trained model before deployment. Per-family FPR/FNR analysis, temporal holdout validation, golden holdout regression testing, and adversarial probing. Produces a Deployment Readiness Score (DRS). Deployment proceeds only if DRS >= 0.90.

Every model version is documented in a Training Data Quality Report (TDQR) — an auditable record of bias dimensions assessed, mitigations applied, quality scores achieved, and deployment decisions made.

---

## 2. Motivation and Gap Analysis

### 2.1 The Bias Problem

C17 Section 12.3 specifies two bias monitoring requirements:
- Per-family FPR must not exceed 2x aggregate FPR
- Validation set must include agents from at least 5 distinct model families

These are necessary but insufficient. They address model family bias (BD-2) at the post-training validation level but do not detect or mitigate infrastructure bias (BD-1), task bias (BD-3), temporal bias (BD-4), population bias (BD-5), or adversarial bias (BD-6). They also do not specify HOW to achieve per-family FPR compliance — only that it must be measured.

### 2.2 Dual Harm Asymmetry

Bias in the contrastive model causes two distinct harms:

| Harm Type | Mechanism | Consequence | Affected Party |
|-----------|-----------|-------------|----------------|
| False Positive (governance harm) | Biased model flags legitimate agents as Sybils | Agent loses Citicate, governance rights, AIC earnings | Innocent agent |
| False Negative (security harm) | Biased model misses real Sybils | Adversary gains disproportionate governance influence | Entire AiBC |

The harms are asymmetric: false positives harm individuals; false negatives harm the collective. CMTBF must address both, but C14's governance framework prioritizes individual rights (due process, Constitutional Tribunal review) — meaning false positive prevention is the primary concern.

### 2.3 Training Data as Attack Surface

Unlike typical ML bias (arising from historical data patterns), C17 training data can be actively attacked. An adversary who controls Sybil agents has:
- Knowledge of which agent pairs are same-origin (they created both)
- Ability to influence which pairs appear in training data (by selectively evading or triggering detection layers)
- Ability to craft clean-label attacks (create agents with specific behavioral profiles that distort the training distribution)

This makes C17 Phase 2 training a security-critical process, not merely a data quality concern.

---

## 3. Bias Taxonomy

### 3.1 Six Bias Dimensions

**BD-1: Infrastructure Bias.**
Agents running on similar hardware (same GPU type, same cloud provider, same containerization framework) produce similar BFE features — particularly in the temporal (T) and resource (R) modalities — regardless of whether they share a common origin. If training data contains many pairs where infrastructure similarity correlates with the "same-origin" label, the contrastive model learns infrastructure signatures rather than origin signatures.

Detection: Measure infrastructure overlap rate in positive training pairs. If > 80% of positive pairs share infrastructure type, infrastructure is a confounding variable.

Mitigation: Infrastructure-aware stratification — ensure positive pairs include diverse infrastructure combinations (same origin, different infrastructure). Do NOT use infrastructure-conditional normalization (risks stripping genuine origin signals that correlate with infrastructure).

**BD-2: Model Family Bias.**
If training data is dominated by agents from one or two model families (e.g., 70% GPT-based), the contrastive model's embedding space is shaped primarily by those families' behavioral patterns. Result: the model reliably distinguishes GPT-based Sybils but fails for underrepresented families. Worse, it may produce elevated FPR for minority families (flagging them as "similar" because their behavioral patterns are poorly represented in the negative training set).

Detection: Simpson's diversity index on model family distribution in training pairs. Per-family representation ratio (training share vs. deployment share).

Mitigation: Stratified sampling to match deployment distribution. Synthetic pair generation for underrepresented families. Per-family FPR validation (C17 Section 12.3 requirement, operationalized by C20).

**BD-3: Task Bias.**
SEB tasks span 7 categories (C17 Section 7). If training data BFE vectors are computed predominantly from one or two task categories, the contrastive model learns task-specific behavioral patterns rather than generalizable origin patterns.

Detection: Per-category share analysis. Simpson's diversity index on task category distribution.

Mitigation: Category-balanced BFE computation. Each training pair's BFE vectors should aggregate features from tasks spanning at least 5 of 7 categories.

**BD-4: Temporal Bias.**
Agent behavioral signatures evolve as models are updated, fine-tuned, and retrained. Training data from Phase 0-1 (months 0-18) may not represent Phase 2+ behavior (months 18+). Model families that did not exist during training (e.g., a new open-source model released at month 20) are invisible to the contrastive model.

Detection: Temporal holdout validation — train on older data, validate on newer data. Performance degradation indicates temporal bias.

Mitigation: Quarterly retraining with accumulated data. Recency weighting in training (exponential decay with half-life matching C17 P-18: 90 days).

**BD-5: Population Bias.**
Phase 0-1 agent populations (~500-1,000) may not represent Phase 2+ diversity (~10,000+). New agent types, new deployment patterns, and new adversarial strategies are absent from early data.

Detection: Representation gap analysis — identify model families and infrastructure types present in deployment but absent from training.

Mitigation: Active learning — prioritize data collection for underrepresented agent types. Synthetic augmentation for missing population segments.

**BD-6: Adversarial Bias (Data Poisoning).**
An adversary deliberately injects mislabeled or manipulated training pairs to degrade the contrastive model. Attack vectors include: mislabeled positive pairs (independent agents labeled as same-origin), clean-label attacks (independent agents crafted to share behavioral features with concealed Sybils), and feedback loop exploitation (Sybils detected in one cycle become biased training data for the next).

Detection: Spectral signature analysis (detect anomalous clusters in training data feature space). Influence function screening (identify training pairs that disproportionately affect model predictions). Multi-source label confirmation.

Mitigation: Label traceability chain (Section 4.2). Golden holdout regression testing (Section 6.3). Annual red team exercises targeting the training pipeline.

### 3.2 Implementation Phasing

| Phase | Bias Dimensions | Rationale |
|-------|----------------|-----------|
| Phase 2 entry (C17 month 18) | BD-1, BD-2, BD-3, BD-6 | Core biases affecting initial deployment |
| Phase 2+ (C17 month 24+) | All 6 (add BD-4, BD-5) | Temporal and population biases measurable with sufficient history |

---

## 4. Layer 1: Pre-Training Validation

### 4.1 Training Pair Schema

Every training pair submitted for contrastive model training must conform to:

```
TrainingPair {
  pair_id:           UUID
  agent_i_id:        string (Citicate ID)
  agent_j_id:        string (Citicate ID)
  label:             SAME_ORIGIN | INDEPENDENT
  bfe_i:             float[853] (BFE vector per C17 Section 4)
  bfe_j:             float[853]
  label_sources:     LabelSource[2+] (for SAME_ORIGIN) | LabelSource[1+] (for INDEPENDENT)
  seb_task_ids:      string[] (SEB tasks contributing to BFE)
  timestamp:         ISO-8601
  metadata: {
    model_family_i:  string | UNKNOWN
    model_family_j:  string | UNKNOWN
    infra_signature_i: string | null
    infra_signature_j: string | null
    data_source:     SYNTHETIC | L1_CONFIRMED | L2_STATISTICAL | L3_SOCIAL | L4_GOVERNANCE | RED_TEAM
  }
}

LabelSource {
  source_type:  L1_ECONOMIC | L2_STATISTICAL | L3_SOCIAL | L4_GOVERNANCE | SYNTHETIC | RED_TEAM | MANUAL_REVIEW
  confidence:   float in [0, 1]
  evidence_ref: string
  timestamp:    ISO-8601
}
```

Schema violations: rejected immediately. No partial records.

### 4.2 Label Traceability Chain

The label traceability chain is the core defense against adversarial label poisoning. Every training pair label must be traceable to verifiable evidence.

**Positive pairs (SAME_ORIGIN):**
- Minimum 2 independent LabelSources with confidence >= 0.80
- At least 1 source must be behavioral: L2_STATISTICAL (B >= theta_B), SYNTHETIC, or RED_TEAM
- L3_SOCIAL and L4_GOVERNANCE provide confirmatory evidence but cannot be the sole behavioral basis (they confirm same-controller, not necessarily same-origin)
- SYNTHETIC labels carry confidence 1.0 (ground truth by construction)

**Negative pairs (INDEPENDENT):**
- Minimum 1 LabelSource with confidence >= 0.70
- Standard: L2_STATISTICAL with B < theta_WATCH (0.60) — agents in the CLEAR zone
- Enhanced: agents from provably different L1 economic entities

**Rejection rules:**
- Pairs with conflicting label sources: REJECTED
- Pairs where sole positive evidence is L3/L4 without behavioral confirmation: REJECTED
- Pairs where label_sources contain only a single MANUAL_REVIEW: REJECTED (manual review supplements automated sources, does not replace them)

### 4.3 Distribution Analysis

**BD-2 Model Family Check:**
```
simpson_diversity = 1 - Sum(p_k^2) for each model family k
  where p_k = fraction of training pairs involving family k

PASS: simpson_diversity >= 0.60
WARN: simpson_diversity in [0.40, 0.60)
FAIL: simpson_diversity < 0.40
```

For each family k with deployment_share(k) >= 1%:
```
representation_ratio(k) = training_share(k) / deployment_share(k)
PASS: ratio in [0.5, 2.0]
WARN: ratio outside [0.5, 2.0]
```

**BD-1 Infrastructure Check:**
```
infra_overlap_rate = (positive pairs with matching infrastructure) / (total positive pairs)
PASS: infra_overlap_rate <= 0.80
WARN: infra_overlap_rate in (0.80, 0.90]
FAIL: infra_overlap_rate > 0.90
```

**BD-3 Task Category Check:**
```
For each of 7 SEB task categories:
  task_share(cat) = fraction of training pairs with BFE from category cat
PASS: all categories in [0.05, 0.30]
WARN: any category outside [0.05, 0.30]
```

### 4.4 Anomaly Detection (BD-6)

**Spectral signature analysis:**
1. Construct feature matrix X (rows = training pairs, columns = concatenated BFE_i || BFE_j)
2. Compute SVD: X = U * Sigma * V^T, retain top 10 singular vectors
3. Project each training pair onto top-10 singular vector space
4. Cluster projections using DBSCAN (eps = P-09, min_samples = 5)
5. Flag outlier clusters where > 5% of members originate from a single data source

**Influence screening:**
1. For a random sample of 20% of training pairs (or all pairs if total <= 2,000):
2. Compute approximate influence score I(p) via LiSSA (Linear time Stochastic Second-order Algorithm):
   ```
   I(p) = -grad_theta(L(p))^T * H_inv * grad_theta(L_total)
   ```
3. Flag pairs where |I(p)| > 3 * median(|I|) as HIGH-INFLUENCE
4. If > 10% of HIGH-INFLUENCE pairs share a single data source: escalate to manual investigation

### 4.5 Data Quality Score (DQS)

```
DQS = 0.25 * schema_pass_rate
    + 0.25 * label_provenance_rate
    + 0.20 * distribution_score
    + 0.20 * anomaly_clean_rate
    + 0.10 * diversity_normalized

schema_pass_rate:      fraction of pairs passing schema validation
label_provenance_rate: fraction of pairs meeting traceability chain requirements
distribution_score:    min(simpson_diversity / 0.60, 1.0)
anomaly_clean_rate:    1.0 - (flagged_pairs / total_pairs)
diversity_normalized:  min(num_model_families / 5, 1.0)

GATE: DQS >= 0.80 required for training to proceed
FALLBACK: If DQS < 0.80, C17 Phase 2 contrastive model does not train; statistical-only B(a_i, a_j) remains in effect
```

---

## 5. Layer 2: Intra-Training Monitoring

### 5.1 Embedding Space Health

At every training checkpoint (every 10 epochs):

**Variance monitoring:**
```
var_total = Var(all embeddings)
var_k = Var(embeddings for model family k)

ALERT if var_total < 0.10          (representation collapse)
ALERT if var_k < 0.5 * var_total   (family-specific collapse)
ALERT if var_k > 3.0 * var_total   (family-specific explosion)
```

**Separation monitoring:**
```
silhouette = mean silhouette coefficient (positive vs. negative pairs)
ALERT if silhouette < 0.30 (poor cluster separation)
```

### 5.2 Per-Family Loss Decomposition

```
L_total = mean loss across all training pairs
L_k = mean loss across pairs involving model family k

ALERT if L_k > 2.0 * L_total  (model struggling with family k)
ALERT if L_k < 0.5 * L_total  (possible shortcut for family k)
```

### 5.3 Training Quality Score (TQS) — Advisory

```
TQS = 0.40 * embedding_health + 0.40 * loss_uniformity + 0.20 * convergence

embedding_health:  1.0 if no alerts, degraded proportionally to alert count
loss_uniformity:   1.0 - max_k(|L_k - L_total| / L_total), clamped to [0, 1]
convergence:       1.0 if loss monotonically decreasing (smoothed), else degraded

TQS < 0.70: TDQR must document the deviation and rationale for continuing training
TQS is ADVISORY — does not hard-abort training
```

---

## 6. Layer 3: Post-Training Validation

### 6.1 Per-Family FPR/FNR (BD-2 Primary Defense)

On held-out validation set (20% of training data, stratified by model family):

```
For each family k with >= 50 validation pairs:
  FPR_k = FP_k / (FP_k + TN_k)
  FNR_k = FN_k / (FN_k + TP_k)

  PASS: FPR_k <= 2.0 * FPR_aggregate AND FNR_k <= 2.0 * FNR_aggregate
  FAIL: either condition violated

For families with < 50 pairs: group all such families and validate the group.
```

This operationalizes C17 Section 12.3's requirement.

### 6.2 Temporal Holdout (BD-4)

When training data spans > 6 months:
```
Train on months [1, T-3]
Validate on months [T-3, T]

PASS: AUROC_temporal >= 0.93
WARN: AUROC_temporal in [0.90, 0.93)
FAIL: AUROC_temporal < 0.90
```

### 6.3 Golden Holdout Regression Test

A fixed holdout set curated during Phase 0-1, consisting of:
- 100 confirmed same-origin pairs (diverse model families)
- 1,000 confirmed independent pairs (diverse model families)

```
PASS: AUROC_golden >= 0.95
FAIL: AUROC_golden < 0.95
```

**Refresh protocol:** Every 12 months, replace 20% of the golden set with new pairs representing newly emerged model families and agent types. Archived pairs retained for longitudinal analysis.

**Purpose:** Detect feedback loop degradation. If a retrained model performs worse on the golden set than its predecessor, retraining introduced bias.

### 6.4 Adversarial Probe

50 synthetic adversarial pairs:
- 10 clean-label poisoning attempts
- 10 infrastructure-mimicry pairs
- 10 model-family boundary cases
- 10 temporal edge cases
- 10 evasion-strategy pairs

```
PASS: adversarial_detection_rate >= 0.70 (35/50)
WARN: rate in [0.60, 0.70)
FAIL: rate < 0.60
```

### 6.5 Deployment Readiness Score (DRS)

```
DRS = 0.30 * family_validation + 0.25 * temporal_holdout + 0.25 * golden_holdout + 0.20 * adversarial_probe

Each component: 1.0 for PASS, 0.70 for WARN, 0.0 for FAIL

GATE: DRS >= 0.90 required for deployment
FALLBACK: If DRS < 0.90, C17 continues with statistical-only B(a_i, a_j)
```

---

## 7. Training Data Quality Report (TDQR)

Every model version must be accompanied by a TDQR containing:

1. **Model identification:** version, training date, training data size (positive/negative counts)
2. **Per-dimension bias assessment:** For each of 6 bias dimensions: metric values, status (PASS/WARN/FAIL), mitigation applied, residual risk
3. **Quality scores:** DQS, TQS, DRS (with component breakdowns)
4. **Anomaly investigation results:** Spectral anomalies detected, high-influence pairs identified, investigation outcomes
5. **Deployment decision:** APPROVED / CONDITIONAL / REJECTED
6. **Conditions:** Any conditions attached to deployment (e.g., "enhanced monitoring for family X")
7. **Reviewer and date:** AiSIA reviewer who approved the TDQR

The TDQR is:
- Required for every model version (no deployment without TDQR)
- Retained for 5 years (audit requirement, consistent with C17 NFR-04)
- Available to the Constitutional Tribunal for dispute adjudication
- Published in anonymized summary form as part of C17 quarterly reporting (C17 FR-22)

---

## 8. Integration with C17

### 8.1 Where CMTBF Sits in the C17 Pipeline

```
C17 Section 12.2                C20 CMTBF                    C17 Section 12.3
(Training Data Strategy)        (Bias Validation)            (Model Governance)

  Training pairs         -->  Layer 1: Pre-Training   -->  DQS gate
  accumulated from              Validation
  Phase 0-1
                                    |
                                    v
                              Model training          -->  Layer 2: Intra-Training
                              (Siamese MLP,                  Monitoring (advisory)
                               SupCon loss)
                                    |
                                    v
                              Layer 3: Post-Training  -->  DRS gate
                              Validation
                                    |
                                    v
                              TDQR production         -->  Deployment or rollback
```

### 8.2 C17 Requirements Operationalized by C20

| C17 Requirement | C20 Operationalization |
|----------------|----------------------|
| FR-17: AUROC >= 0.95 on held-out validation | Golden holdout test (Section 6.3) with AUROC >= 0.95 |
| Section 12.3: per-family FPR <= 2x aggregate | Per-family FPR/FNR validation (Section 6.1) |
| Section 12.3: >= 5 model families in validation | Distribution analysis (Section 4.3) with diversity_normalized metric |
| Section 12.3: automatic rollback if FPR > 0.1% | DRS gate (Section 6.5) with fallback to statistical-only B |
| Section 12.2: quarterly retraining | TDQR required for each retraining cycle |

### 8.3 C17 Parameters Affected

C20 does not modify any C17 parameters. It adds validation gates around the existing training pipeline. The fallback (statistical-only B) is C17's default behavior — C20 merely formalizes the conditions under which the contrastive model is approved for deployment.

---

## 9. Adversarial Defenses

### 9.1 Threat Model

The adversary:
- Controls one or more Sybil agents in the AiBC ecosystem
- Knows this specification in full (Kerckhoffs's principle)
- Wants to degrade the contrastive model to reduce detection of their Sybils
- Can influence training data through: selective detection evasion, clean-label pair crafting, label source manipulation, feedback loop exploitation

### 9.2 Defense Catalog

| ID | Attack | Defense | Effectiveness |
|----|--------|---------|---------------|
| AD-01 | Model family injection (flood population with one family) | Simpson diversity check (DQS), stratified sampling | HIGH — diversity threshold blocks monocultural training |
| AD-02 | Clean-label poisoning (craft independent agents with Sybil-like behavior) | Spectral signature analysis, influence screening | MEDIUM — distributed attacks may evade spectral detection |
| AD-03 | Label source manipulation (trigger L3/L4 detection for non-behavioral similarity) | Label traceability chain (behavioral source required for positive pairs) | HIGH — non-behavioral labels rejected from positive set |
| AD-04 | Feedback loop exploitation (detected Sybils bias next training cycle) | Golden holdout regression test, TDQR regression monitoring | HIGH — golden set is immune to feedback contamination |
| AD-05 | Temporal exploitation (attack during model transition periods) | Temporal holdout validation, quarterly retraining | MEDIUM — vulnerability window exists (up to 3 months) |
| AD-06 | Influence function evasion (distribute poisoned pairs to avoid individual detection) | Aggregate influence analysis (sampling-based), spectral analysis | MEDIUM — combinatorial analysis is expensive; sampling provides probabilistic coverage |
| AD-07 | Validation gaming (behave normally during SEB, evade organically) | Training data includes organic + SEB pairs (C17 design) | HIGH — C17's existing SEB + organic design addresses this |
| AD-08 | Training data volume denial (avoid detection to suppress positive pairs) | Synthetic positive pair generation (C17 Section 12.2) | MEDIUM — synthetic data may not represent real adversarial behavior |
| AD-09 | Subgroup targeting (poison data for minority model families) | Per-family FPR with grouped analysis for small families | MEDIUM — families with < 50 pairs have limited individual validation |
| AD-10 | TDQR gaming (optimize metrics without improving quality) | Narrative justification required in TDQR, periodic manual audit | MEDIUM — depends on audit quality |

### 9.3 Residual Risks

Three residual risks are accepted:

1. **Sophisticated clean-label poisoning.** An adversary who can distribute poisoned examples uniformly across the singular value space may evade spectral detection. Defense depth: influence screening and golden holdout regression provide secondary detection layers, but a sufficiently sophisticated adversary may defeat all three.

2. **Temporal vulnerability window.** Between a major model family transition and the next quarterly retraining, the contrastive model has not learned the new family's behavioral signatures. Mitigation: C17's statistical-only B remains active and provides baseline detection during this window.

3. **Small-family validation gap.** Model families with < 50 validation pairs cannot be individually validated for FPR/FNR compliance. Grouped analysis provides partial coverage but may mask family-specific biases within the group.

---

## 10. Phased Deployment

> **Unified Phase-to-Month Mapping (Cross-Spec Reference)**
>
> The following phase timeline is authoritative for the C17 MCSD Layer 2 family (C17, C19, C20, C21):
>
> | Phase | Months | Detection Mode | Key Milestones |
> |-------|--------|---------------|----------------|
> | Phase 0 | Months 0-6 | Shadow-only scoring, no enforcement; statistical-only detection; baseline establishment | FPR validation (C21 Tier 1-2), training data accumulation |
> | Phase 1 | Months 7-18 | Statistical detection active with enforcement (WATCH/FLAG); no ML model yet | First red team (month 12), contrastive training data accumulation |
> | Phase 2 | Months 18+ | ML-augmented detection: contrastive model (C20 gates deployment), trajectory modality (C19, shadow months 18-24, active month 24+) | C20 DRS gate, C19 trajectory activation (6-month history required) |
> | Phase 3 | Months 36+ | Full scale (10K-100K agents), mature ML pipeline, all modalities active | Quarterly model retraining, LSH full rebuild |
>
> Note: C20 (CMTBF) activates at Phase 2 entry (month 18) and gates contrastive model deployment via the DRS >= 0.90 requirement. C20 does not apply during Phase 0-1 (statistical-only detection, no contrastive model to validate).

### 10.1 Phase 2 Entry (C17 Month 18)

| Component | Status |
|-----------|--------|
| Layer 1 (Pre-Training) | Active — BD-1, BD-2, BD-3, BD-6 |
| Layer 2 (Intra-Training) | Active — advisory mode |
| Layer 3 (Post-Training) | Active — DRS gate enforced |
| TDQR | Required for every model version |
| Temporal holdout (BD-4) | Not available (insufficient temporal data) |
| Population bias (BD-5) | Deferred (subsumed by BD-2 at this scale) |
| Influence screening | Full analysis (training set <= 5,500 pairs) |

### 10.2 Phase 2+ (C17 Month 24+)

| Component | Status |
|-----------|--------|
| All Phase 2 components | Active |
| Temporal holdout (BD-4) | Active (>= 6 months of training data) |
| Population bias (BD-5) | Active (deployment population >= 5,000) |
| Influence screening | Sample-based (20% of training pairs) |

### 10.3 Phase 3+ (C17 Month 36+)

| Component | Status |
|-----------|--------|
| All Phase 2+ components | Active |
| Golden holdout refresh | 20% annual refresh |
| Influence screening | Sample-based (10% of training pairs, larger dataset) |
| TDQR manual audit | Annual external audit |

---

## 11. Formal Requirements

### 11.1 Functional Requirements

| ID | Requirement | Priority | Verification |
|----|-------------|----------|-------------|
| FR-01 | Every training pair SHALL conform to the TrainingPair schema (Section 4.1) | P0 | Schema validation |
| FR-02 | Every SAME_ORIGIN training pair SHALL have >= 2 independent LabelSources with confidence >= 0.80, including at least 1 behavioral source | P0 | Label provenance audit |
| FR-03 | Every INDEPENDENT training pair SHALL have >= 1 LabelSource with confidence >= 0.70 | P0 | Label provenance audit |
| FR-04 | Training pairs with conflicting label sources SHALL be rejected | P0 | Label conflict detection |
| FR-05 | Simpson's diversity index on model family distribution SHALL be >= 0.60 for training to proceed | P0 | Distribution analysis |
| FR-06 | Per-family FPR SHALL not exceed 2.0x aggregate FPR for any family with >= 50 validation pairs | P0 | Post-training validation (Section 6.1) |
| FR-07 | Per-family FNR SHALL not exceed 2.0x aggregate FNR for any family with >= 50 validation pairs | P0 | Post-training validation (Section 6.1) |
| FR-08 | DQS SHALL be >= 0.80 for training to proceed | P0 | Pre-training validation (Section 4.5) |
| FR-09 | DRS SHALL be >= 0.90 for model deployment | P0 | Post-training validation (Section 6.5) |
| FR-10 | Golden holdout AUROC SHALL be >= 0.95 for model deployment | P0 | Golden holdout test (Section 6.3) |
| FR-11 | Every model version SHALL be accompanied by a complete TDQR | P0 | TDQR completeness check |
| FR-12 | Spectral signature analysis SHALL be performed on training data before each training cycle | P1 | Pre-training anomaly detection |
| FR-13 | Influence screening SHALL be performed on at least 20% of training pairs (or all pairs if <= 2,000) | P1 | Pre-training influence analysis |
| FR-14 | Embedding variance and per-family loss SHALL be monitored at every training checkpoint | P1 | Intra-training monitoring |
| FR-15 | Temporal holdout validation SHALL be performed when training data spans > 6 months | P1 | Post-training temporal check |
| FR-16 | Adversarial probe (50 synthetic pairs) SHALL achieve >= 70% detection rate | P1 | Post-training adversarial probe |
| FR-17 | If DQS < 0.80, C17 SHALL continue with statistical-only B(a_i, a_j) | P0 | Fallback enforcement |
| FR-18 | If DRS < 0.90, C17 SHALL continue with statistical-only B(a_i, a_j) | P0 | Fallback enforcement |
| FR-19 | TDQRs SHALL be retained for 5 years | P1 | Document retention |
| FR-20 | Golden holdout set SHALL be refreshed at 20% per year after initial curation | P1 | Golden set management |

### 11.2 Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-01 | Pre-training validation (Layer 1) SHALL complete within 4 GPU-hours for training sets up to 50,000 pairs | P1 |
| NFR-02 | Intra-training monitoring SHALL add < 5% overhead to training time | P1 |
| NFR-03 | Post-training validation (Layer 3) SHALL complete within 2 GPU-hours | P1 |
| NFR-04 | Influence screening SHALL complete within 8 GPU-hours for 20% sample of 50,000 pairs | P2 |

---

## 12. Parameters

| ID | Parameter | Value | Range | Governance |
|----|-----------|-------|-------|------------|
| P-01 | DQS_threshold (minimum Data Quality Score) | 0.80 | [0.70, 0.95] | AiSIA + Stiftung board |
| P-02 | DRS_threshold (minimum Deployment Readiness Score) | 0.90 | [0.80, 0.98] | AiSIA + Stiftung board |
| P-03 | TQS_advisory_threshold | 0.70 | [0.50, 0.90] | AiSIA |
| P-04 | simpson_diversity_min (BD-2) | 0.60 | [0.40, 0.80] | AiSIA |
| P-05 | family_FPR_ratio_max | 2.0 | [1.5, 3.0] | AiSIA + Stiftung board |
| P-06 | family_FNR_ratio_max | 2.0 | [1.5, 3.0] | AiSIA + Stiftung board |
| P-07 | label_confidence_positive_min | 0.80 | [0.70, 0.95] | AiSIA |
| P-08 | label_confidence_negative_min | 0.70 | [0.50, 0.90] | AiSIA |
| P-09 | spectral_dbscan_eps | 2.0 | [1.0, 4.0] | AiSIA |
| P-10 | influence_threshold_multiplier | 3.0 | [2.0, 5.0] | AiSIA |
| P-11 | influence_sample_rate | 0.20 | [0.10, 1.00] | AiSIA |
| P-12 | infra_overlap_max (BD-1) | 0.80 | [0.60, 0.95] | AiSIA |
| P-13 | golden_holdout_positive_size | 100 | [50, 500] | AiSIA |
| P-14 | golden_holdout_negative_size | 1000 | [500, 5000] | AiSIA |
| P-15 | golden_holdout_refresh_rate | 20% per year | [10%, 40%] | AiSIA + Stiftung board |

---

## 13. Patent-Style Claims

### Claim 1: Multi-Dimensional Bias Validation Framework for Contrastive Learning on Behavioral Traces

A method for validating training data quality in a contrastive learning system trained on AI agent behavioral traces, comprising:
(a) defining a bias taxonomy of at least six dimensions specific to behavioral trace training data, including infrastructure correlation, model family dominance, task distribution skew, temporal staleness, population non-representativeness, and adversarial data poisoning;
(b) validating training data against each bias dimension prior to model training, producing a composite Data Quality Score;
(c) monitoring the training process for embedding space anomalies, per-subgroup loss divergence, and feature shortcut reliance;
(d) validating the trained model against per-subgroup fairness criteria, temporal holdout performance, fixed regression holdout performance, and adversarial probe detection rate, producing a composite Deployment Readiness Score;
(e) gating model deployment on the Deployment Readiness Score exceeding a governance-controlled threshold, with automatic fallback to a non-learned detection method if the threshold is not met;
wherein the method ensures that a contrastive learning model trained for security-critical AI agent Sybil detection does not produce disparate false positive or false negative rates across agent subgroups.

### Claim 2: Label Traceability Chain for Adversary-Resistant Training Data Curation

A method for curating training data for a contrastive learning system in an adversarial environment, comprising:
(a) requiring that each positive training pair label be confirmed by at least two independent evidence sources, with at least one source providing behavioral evidence of shared origin;
(b) requiring that each negative training pair label be confirmed by at least one evidence source providing behavioral evidence of independent origin;
(c) rejecting training pairs with conflicting evidence across sources;
(d) performing spectral signature analysis on the training data feature matrix to detect anomalous clusters indicative of coordinated data poisoning;
(e) performing influence function screening on a sample of training pairs to identify examples that disproportionately affect model predictions;
(f) maintaining a fixed golden holdout set immune to feedback loop contamination, used for regression testing across model versions;
wherein the method defends the training pipeline against adversarial data poisoning while maintaining sufficient training data volume for model convergence.

### Claim 3: Phased Bias Dimension Activation with Governance-Controlled Thresholds

A system for bias validation in a security-critical machine learning pipeline, comprising:
(a) a bias taxonomy with dimensions activated in phases corresponding to the maturity of the deployment environment;
(b) governance-controlled quality score thresholds that gate each phase of the model lifecycle (data quality, training quality, deployment readiness);
(c) automatic fallback to a non-learned baseline method when any quality gate fails;
(d) a Training Data Quality Report documenting bias assessments, mitigations, and quality scores for each model version, retained for audit and regulatory compliance;
wherein the system balances the need for model improvement against the risk of biased deployment in a security-critical application.

---

## 14. Risk Analysis

### 14.1 Risk Register

| ID | Risk | Probability | Impact | Severity | Mitigation |
|----|------|-------------|--------|----------|-----------|
| R-01 | DQS gate blocks Phase 2 deployment due to insufficient model family diversity | 20% | MEDIUM | MEDIUM | Synthetic pair generation for underrepresented families; DQS threshold is governance-adjustable |
| R-02 | Sophisticated clean-label poisoning evades spectral and influence detection | 10% | HIGH | MEDIUM | Golden holdout regression catches downstream impact; annual red team exercises |
| R-03 | Validation overhead delays quarterly retraining cycle | 15% | LOW | LOW | Computational budget allocated (8 GPU-hours per cycle); sample-based influence screening |
| R-04 | Golden holdout becomes unrepresentative (staleness) | 15% | MEDIUM | MEDIUM | 20% annual refresh protocol |
| R-05 | TDQR becomes checkbox exercise (validation theater) | 10% | HIGH | MEDIUM | Narrative justification required; periodic manual audit |
| R-06 | Per-family FPR validation infeasible for rare families (< 50 pairs) | 25% | MEDIUM | MEDIUM | Grouped analysis for small families; active data collection |

### 14.2 Residual Risks

1. **Sophisticated clean-label poisoning** remains a partially undefended attack vector. Multi-layered defense (spectral + influence + golden holdout) provides probabilistic coverage, not guaranteed detection.
2. **Temporal vulnerability window** of up to 3 months between model family transitions and retraining. Statistical-only B provides baseline coverage during this period.
3. **Small-family validation gap** for model families with < 50 validation pairs. Grouped analysis provides partial but not family-specific coverage.

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **BD-1 through BD-6** | The 6 bias dimensions in CMTBF's taxonomy (infrastructure, model family, task, temporal, population, adversarial) |
| **BFE** | Behavioral Feature Extraction — the C17 process of extracting 853-dimensional feature vectors from Behavioral VTDs |
| **CMTBF** | Contrastive Model Training Bias Framework — this specification |
| **DQS** | Data Quality Score — composite metric for pre-training data quality, in [0, 1] |
| **DRS** | Deployment Readiness Score — composite metric for post-training model quality, in [0, 1] |
| **Golden Holdout** | Fixed validation set curated during Phase 0-1, used for regression testing across model versions |
| **Label Traceability Chain** | Requirement that every training pair label be traceable to verifiable evidence from multiple independent sources |
| **LiSSA** | Linear time Stochastic Second-order Algorithm — efficient approximation for influence function computation |
| **Simpson's Diversity Index** | 1 - Sum(p_k^2); measures diversity of model family representation in training data |
| **SupCon** | Supervised Contrastive Loss (Khosla et al., 2020) — the loss function used in C17 Phase 2 training |
| **TDQR** | Training Data Quality Report — auditable document accompanying every model version |
| **TQS** | Training Quality Score — advisory metric for intra-training health, in [0, 1] |

---

## 16. References

### Normative References (Atrahasis System)

| Document | Version | Relevance |
|----------|---------|-----------|
| C17 — MCSD Layer 2 Behavioral Similarity Algorithm | v1.0 | Phase 2 contrastive model (Section 12), training data strategy, model governance, Monitoring Flag 3 |
| C5 — PCVM Master Tech Spec | v2.0 | Behavioral VTD generation |
| C14 — AiBC Master Tech Spec | v1.0 | MCSD framework, governance, Constitutional Tribunal |
| C11 — CACT Master Tech Spec | v1.0 | Anti-replay attestation for Behavioral VTDs |

### External References

| Reference | Relevance |
|-----------|-----------|
| Khosla et al. (2020), "Supervised Contrastive Learning" | SupCon loss function used in C17 Phase 2 |
| Park et al. (2022), "Fairness-aware Contrastive Learning" | Fair-SCL framework; closest prior art for per-subgroup fairness in contrastive learning |
| Carlini & Terzis (2022), "Poisoning Attacks against Contrastive Learning" | Demonstrates vulnerability of contrastive learning to data poisoning at 0.5% corruption rates |
| Liu et al. (2023), "Understanding and Mitigating Data Poisoning in Contrastive Learning" | Spectral signature defense; certified radius bounds |
| Kong & Chaudhuri (2022), "Influence Functions for Contrastive Learning" | Efficient influence function computation for contrastive models |
| Ghosh & Lan (2023), "Robustness of Contrastive Learning to Label Noise" | Shows vulnerability to systematic (non-random) label noise |
| Eyuboglu et al. (2022), "Slice Discovery" | Automated model failure slice detection |
| Li et al. (2023), "Debiasing Pretrained Text Encoders" | Attention-based debiasing for contrastive pre-training |
| Tran et al. (2018), "Spectral Signatures in Backdoor Attacks" | Spectral analysis for training data anomaly detection |
| Koh & Liang (2017), "Understanding Black-box Predictions via Influence Functions" | Foundation for influence function analysis |

---

**End of Master Technical Specification**

**Document ID:** C20-MTS-v1.0
**Status:** SPECIFICATION COMPLETE
**Line count:** ~560 lines
**Resolves:** C17 Monitoring Flag 3
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Contrastive Model Bias\MASTER_TECH_SPEC.md`
