# C20 — Contrastive Model Training Bias Framework — DESIGN

**Invention ID:** C20
**Stage:** DESIGN
**Date:** 2026-03-11
**Selected Concept:** C20-A (Contrastive Model Training Bias Framework — CMTBF)
**Normative Reference:** C17 Section 12 (Contrastive Learning Model, Phase 2+)

---

# PART 1 — ARCHITECTURE

## 1.1 System Overview

CMTBF is a 3-layer validation pipeline that wraps C17's Phase 2 contrastive model training:

```
Training Data              Pre-Training            Intra-Training           Post-Training
Sources                    Validation               Monitoring               Validation
                           (Layer 1)                (Layer 2)                (Layer 3)
+-------------------+     +------------------+     +------------------+     +-------------------+
| Synthetic pairs   |     |                  |     |                  |     |                   |
| L1 confirmed      | --> | Schema check     | --> | Embedding        | --> | Per-family FPR    |
| L2 statistical    |     | Label provenance |     |   variance       |     | Temporal holdout  |
| L3/4 detections   |     | Distribution     |     | Per-family loss  |     | Adversarial probe |
| Red team          |     |   analysis       |     | Feature          |     | Population sim    |
+-------------------+     | Anomaly          |     |   importance     |     | Golden holdout    |
                           |   detection      |     | Shortcut test    |     |   regression      |
                           | Influence        |     |                  |     |                   |
                           |   screening      |     | TQS >= 0.70?    |     | DRS >= 0.90?      |
                           |                  |     |                  |     |                   |
                           | DQS >= 0.80?     |     | ABORT if fail    |     | DEPLOY if pass    |
                           |                  |     |                  |     | ROLLBACK if fail  |
                           | BLOCK if fail    |     |                  |     |                   |
                           +------------------+     +------------------+     +-------------------+
                                                                                     |
                                                                                     v
                                                                            +-------------------+
                                                                            | Training Data     |
                                                                            | Quality Report    |
                                                                            | (TDQR)            |
                                                                            +-------------------+
```

## 1.2 Bias Taxonomy

### Six Bias Dimensions

| ID | Dimension | Definition | Detection Phase | Mitigation Phase |
|----|-----------|-----------|-----------------|------------------|
| BD-1 | Infrastructure Bias | Agents on similar hardware produce similar BFE features regardless of origin, causing false positive training labels | Pre-Training | Pre-Training |
| BD-2 | Model Family Bias | Training data dominated by one or few model families, causing the contrastive model to learn family signatures rather than origin signatures | Pre-Training | Pre-Training |
| BD-3 | Task Bias | Training data over-represents certain SEB task categories, causing the model to not generalize across task types | Pre-Training | Pre-Training |
| BD-4 | Temporal Bias | Training data from one time period does not generalize to another due to model evolution and infrastructure changes | Post-Training | Quarterly retraining |
| BD-5 | Population Bias | Training data from small Phase 0-1 population does not represent Phase 2+ agent diversity | Post-Training | Active learning + synthetic augmentation |
| BD-6 | Adversarial Bias | Adversary deliberately injects mislabeled or manipulated training pairs to degrade model performance | Pre-Training | Pre-Training + Post-Training |

### Implementation Phasing

| Phase | Dimensions Active | Rationale |
|-------|------------------|-----------|
| Phase 2 entry (month 18) | BD-1, BD-2, BD-3, BD-6 | Core biases that affect initial deployment |
| Phase 2+ (month 24+) | All 6 | Temporal and population biases become measurable with sufficient history |

## 1.3 Layer 1: Pre-Training Validation

### 1.3.1 Schema Validation
Every training pair must conform to:
```
TrainingPair {
  pair_id:           string (UUID)
  agent_i_id:        string
  agent_j_id:        string
  label:             "SAME_ORIGIN" | "INDEPENDENT"
  bfe_i:             BFE_Vector (853 dimensions, per C17 Section 4)
  bfe_j:             BFE_Vector (853 dimensions)
  label_sources:     LabelSource[] (min 2 for SAME_ORIGIN, min 1 for INDEPENDENT)
  task_ids:          string[] (SEB task IDs that generated the BFE data)
  timestamp:         ISO-8601
  infrastructure_i:  InfraSignature | null
  infrastructure_j:  InfraSignature | null
  metadata: {
    model_family_i:  string | "UNKNOWN"
    model_family_j:  string | "UNKNOWN"
    data_source:     "SYNTHETIC" | "L1_CONFIRMED" | "L2_STATISTICAL" | "L3_SOCIAL" | "L4_GOVERNANCE" | "RED_TEAM"
  }
}

LabelSource {
  source_type:       "L1_ECONOMIC" | "L2_STATISTICAL" | "L3_SOCIAL" | "L4_GOVERNANCE" | "SYNTHETIC" | "RED_TEAM" | "MANUAL_REVIEW"
  confidence:        float in [0, 1]
  evidence_ref:      string (reference to detection record)
  timestamp:         ISO-8601
}
```

### 1.3.2 Label Provenance Verification (Label Traceability Chain)

**Rule for positive pairs (SAME_ORIGIN):**
- MUST have >= 2 independent LabelSources with confidence >= 0.80
- At least one source must be behavioral (L2_STATISTICAL or SYNTHETIC or RED_TEAM)
- Non-behavioral sources (L3_SOCIAL, L4_GOVERNANCE) contribute confirmatory evidence but cannot be the sole behavioral basis
- SYNTHETIC labels are accepted with confidence 1.0 (ground truth by construction)

**Rule for negative pairs (INDEPENDENT):**
- MUST have >= 1 LabelSource with confidence >= 0.70
- Standard source: L2_STATISTICAL with B(a_i, a_j) < theta_WATCH (0.60)
- Enhanced source: agents from provably different creators (different L1 economic entities)

**Rejection criteria:**
- Pairs with conflicting labels across sources are REJECTED (not used for training)
- Pairs where the sole evidence is L3/L4 (social/governance) without behavioral confirmation are REJECTED from positive set

### 1.3.3 Distribution Analysis

**Model family distribution check (BD-2):**
```
simpson_diversity = 1 - Sum(p_k^2)  for each model family k
where p_k = fraction of training pairs involving family k

PASS if simpson_diversity >= 0.60
WARN if simpson_diversity in [0.40, 0.60)
FAIL if simpson_diversity < 0.40
```

**Per-family representation check:**
```
For each model family k with deployment_share(k) >= 0.01:
  training_share(k) MUST be in [0.5 * deployment_share(k), 2.0 * deployment_share(k)]
  Else: WARNING — family k is under/over-represented
```

**Infrastructure distribution check (BD-1):**
```
For positive pairs: measure infrastructure_overlap_rate
  = fraction of positive pairs where infrastructure_i == infrastructure_j

If infrastructure_overlap_rate > 0.80:
  WARNING — positive pairs may reflect infrastructure similarity, not origin similarity
  Mitigation: add infrastructure-diverse positive pairs (same origin, different infrastructure)
```

**Task category distribution check (BD-3):**
```
For each of 7 SEB task categories:
  task_share(category) MUST be in [0.05, 0.30]
  Else: WARNING — task distribution skewed
```

### 1.3.4 Anomaly Detection

**Spectral signature analysis (BD-6):**
1. Construct the feature matrix X of all training pairs (each row = concatenated BFE vectors)
2. Compute top-k singular vectors of X (k = 10)
3. Project each training pair onto these singular vectors
4. Detect outlier clusters using DBSCAN (eps = 2.0, min_samples = 5)
5. If an outlier cluster contains > 5% of training pairs from a single source: FLAG for manual review

**Individual influence screening (BD-6):**
1. For each training pair p, estimate its influence I(p) on the model's loss using the approximation from Kong & Chaudhuri (2022):
   ```
   I(p) = -grad_theta(L(p))^T * H^{-1} * grad_theta(L_total))
   where H = Hessian of total loss, approximated via LiSSA
   ```
2. Pairs with |I(p)| > 3 * median(|I|) are flagged as HIGH-INFLUENCE
3. HIGH-INFLUENCE pairs undergo manual provenance review
4. If > 10% of high-influence pairs originate from a single source: FLAG for investigation

### 1.3.5 Data Quality Score (DQS)

```
DQS = 0.25 * schema_pass_rate
    + 0.25 * label_provenance_pass_rate
    + 0.20 * distribution_score
    + 0.20 * anomaly_clean_rate
    + 0.10 * diversity_index_normalized

where:
  schema_pass_rate = fraction of pairs passing schema validation
  label_provenance_pass_rate = fraction of pairs meeting provenance requirements
  distribution_score = min(simpson_diversity / 0.60, 1.0)  (capped at 1.0)
  anomaly_clean_rate = 1 - (flagged_pairs / total_pairs)
  diversity_index_normalized = min(num_model_families / 5, 1.0)

GATE: Training proceeds only if DQS >= 0.80
FALLBACK: If DQS < 0.80, C17 continues with statistical-only B(a_i, a_j)
```

## 1.4 Layer 2: Intra-Training Monitoring

### 1.4.1 Embedding Space Monitoring
During training, at every checkpoint (every 10 epochs):

**Embedding variance:**
```
var_total = Var(embeddings across all training pairs)
var_family_k = Var(embeddings for family k)

ALERT if var_total < 0.10 (representation collapse)
ALERT if any var_family_k < 0.5 * var_total (family-specific collapse)
```

**Cluster separation:**
```
silhouette_score = mean silhouette coefficient for positive/negative clusters
ALERT if silhouette_score < 0.30 (poor separation — model not learning)
```

### 1.4.2 Per-Family Loss Decomposition
```
L_total = (1/N) * Sum(L(pair_i))
L_family_k = (1/N_k) * Sum(L(pair_i) for pair_i involving family k)

ALERT if L_family_k > 2.0 * L_total (model struggling with family k)
ALERT if L_family_k < 0.5 * L_total (model may have shortcut for family k)
```

### 1.4.3 Feature Importance via Permutation
At each checkpoint:
1. For each of the 5 BFE modalities (T, S, E, R, L):
   a. Permute that modality's features across training pairs
   b. Measure validation loss increase
2. Feature importance = (permuted_loss - baseline_loss) / baseline_loss

**ALERT if any single modality importance > 0.60** — model may be over-relying on one modality (shortcut risk)
**ALERT if infrastructure-correlated feature importance > model-family-correlated feature importance** — model learning infrastructure, not origin

### 1.4.4 Training Quality Score (TQS)
```
TQS = 0.30 * embedding_health
    + 0.30 * loss_uniformity
    + 0.20 * feature_balance
    + 0.20 * convergence_stability

where:
  embedding_health = 1 if no collapse/separation alerts, else degraded
  loss_uniformity = 1 - max_k(|L_family_k - L_total| / L_total)
  feature_balance = 1 - max_modality_importance
  convergence_stability = 1 if loss is monotonically decreasing (with noise), else degraded

GATE: Training aborted if TQS < 0.70 at any checkpoint
```

## 1.5 Layer 3: Post-Training Validation

### 1.5.1 Per-Family FPR/FNR Validation
On held-out validation set (20% of training data, stratified by model family):

```
For each model family k with >= 50 validation pairs:
  FPR_k = false positives for family k / total negatives involving family k
  FNR_k = false negatives for family k / total positives involving family k

  PASS if FPR_k <= 2.0 * FPR_aggregate AND FNR_k <= 2.0 * FNR_aggregate
  FAIL if either condition violated
```

For families with < 50 validation pairs: grouped analysis (all small families pooled).

### 1.5.2 Temporal Holdout Validation
If training data spans > 6 months:
```
Train on data from months 1 through T-3
Validate on data from months T-3 through T

AUROC_temporal >= 0.93 required
PASS if met, WARN if AUROC in [0.90, 0.93), FAIL if AUROC < 0.90
```

### 1.5.3 Golden Holdout Regression Test
A fixed "golden" holdout set curated during Phase 0-1 (never updated after initial curation):
- 100 positive pairs (confirmed same-origin)
- 1,000 negative pairs (confirmed independent)
- Diverse across model families and infrastructure types

```
AUROC_golden >= 0.95 required
PASS if met, FAIL if not

Purpose: detect feedback loop degradation (Attack 10)
```

### 1.5.4 Adversarial Probe
Submit 50 synthetic adversarial pairs (designed to test known attack vectors):
- 10 clean-label poisoning attempts
- 10 infrastructure-mimicry pairs
- 10 model-family boundary cases
- 10 temporal edge cases (agents near model transition boundaries)
- 10 evasion-strategy pairs (agents with deliberate behavioral diversification)

```
adversarial_detection_rate >= 0.70 required (detect at least 35/50)
PASS if met, WARN if in [0.60, 0.70), FAIL if < 0.60
```

### 1.5.5 Deployment Readiness Score (DRS)
```
DRS = 0.30 * per_family_pass_rate
    + 0.25 * temporal_holdout_normalized
    + 0.25 * golden_holdout_normalized
    + 0.20 * adversarial_probe_normalized

where each component is 1.0 if PASS, scaled down for WARN, 0 for FAIL

GATE: Deployment proceeds only if DRS >= 0.90
FALLBACK: If DRS < 0.90, C17 continues with statistical-only B(a_i, a_j)
```

## 1.6 Training Data Quality Report (TDQR)

Every model version must be accompanied by a TDQR containing:

```
TDQR {
  model_version:     string
  training_date:     ISO-8601
  training_data_size: { positive: int, negative: int }

  bias_dimensions: {
    BD1_infrastructure: {
      infrastructure_overlap_rate: float
      mitigation_applied: string
      status: "PASS" | "WARN" | "FAIL"
    }
    BD2_model_family: {
      simpson_diversity: float
      per_family_representation: { family: string, training_share: float, deployment_share: float }[]
      status: "PASS" | "WARN" | "FAIL"
    }
    BD3_task: {
      per_category_share: { category: string, share: float }[]
      status: "PASS" | "WARN" | "FAIL"
    }
    BD4_temporal: {
      temporal_coverage: { start: ISO-8601, end: ISO-8601 }
      holdout_AUROC: float | null
      status: "PASS" | "WARN" | "FAIL" | "N/A"
    }
    BD5_population: {
      training_population_size: int
      deployment_population_size: int
      representation_gaps: string[]
      status: "PASS" | "WARN" | "FAIL" | "N/A"
    }
    BD6_adversarial: {
      spectral_anomalies_detected: int
      high_influence_pairs: int
      investigation_outcomes: string[]
      status: "PASS" | "WARN" | "FAIL"
    }
  }

  quality_scores: {
    DQS: float
    TQS: float
    DRS: float
  }

  deployment_decision: "APPROVED" | "CONDITIONAL" | "REJECTED"
  conditions: string[]
  reviewer: string
  review_date: ISO-8601
}
```

---

# PART 2 — PRE-MORTEM ANALYSIS

**Assumption: CMTBF has failed catastrophically 5 years after deployment.**

## Failure Scenario 1: Validation Theater (Likelihood: MEDIUM)
**Root cause:** The 3-layer validation pipeline becomes a checkbox exercise. Quality scores (DQS, TQS, DRS) are optimized by gaming the metrics rather than genuinely improving data quality. Example: training data is resampled to pass the Simpson diversity threshold, but the resampling removes the most informative training pairs.
**Severity:** HIGH — defeats the purpose of C20 entirely.
**Design response:** TDQR requires narrative justification for every mitigation action, not just metric compliance. Periodic manual audit of TDQR quality.

## Failure Scenario 2: Threshold Ossification (Likelihood: MEDIUM)
**Root cause:** DQS >= 0.80, TQS >= 0.70, DRS >= 0.90 are set at design time and never updated. As the agent population grows and diversifies, these thresholds become either too strict (blocking valid deployments) or too lenient (passing biased models).
**Severity:** MEDIUM — causes either deployment delays or bias leakage.
**Design response:** Thresholds are governance-controlled parameters (AiSIA + Stiftung board) with quarterly review. Range bounds specified in parameter table.

## Failure Scenario 3: Golden Holdout Staleness (Likelihood: HIGH)
**Root cause:** The golden holdout set, curated during Phase 0-1, becomes unrepresentative of the Phase 3+ agent population. New model families, new attack vectors, and new infrastructure types are not represented. The golden holdout AUROC passes even when the model is biased against new agent types.
**Severity:** HIGH — regression test becomes meaningless.
**Design response:** Golden holdout refresh protocol: every 12 months, 20% of the golden set is replaced with new pairs. Replacement pairs must include representatives from all model families added since last refresh. Old pairs are archived, not deleted.

## Failure Scenario 4: Adversarial Adaptation (Likelihood: HIGH)
**Root cause:** Adversary reads C20 specification and crafts attacks that exploit specific detection mechanisms. Example: poisoned pairs are designed to have "normal" spectral signatures by spreading them uniformly across the singular value space.
**Severity:** MEDIUM — specific detection methods fail but multi-layered defense limits damage.
**Design response:** Annual red team exercise specifically targeting C20's validation pipeline. Randomize detection parameters (DBSCAN eps, influence threshold multiplier) within documented ranges.

## Failure Scenario 5: Computational Budget Squeeze (Likelihood: MEDIUM)
**Root cause:** As training data grows from 5,500 pairs (Phase 2) to 50,000+ pairs (Phase 3+), influence function analysis becomes computationally expensive. Budget pressure leads to skipping influence analysis or using degraded approximations.
**Severity:** LOW-MEDIUM — adversarial bias detection weakens.
**Design response:** Influence function sampling: analyze a random 20% subset of training pairs per cycle. If anomalies are detected in the sample, trigger full analysis. Budget ceiling: 8 GPU-hours per quarterly retraining cycle.

---

# PART 3 — SIMPLIFICATION REVIEW

**Question: What is the simplest version of C20 that preserves the core value?**

## Removable Without Material Impact

1. **BD-5 (Population Bias):** At Phase 2 entry, population bias is indistinguishable from model family bias (BD-2). Population bias becomes meaningful only at Phase 3+ scale. BD-2 monitoring subsumes BD-5 for initial deployment.
   - **Recommendation:** Defer BD-5 to Phase 3. Retain in taxonomy but do not implement initially.
   - **Impact if removed:** Minimal — BD-2 catches the same issues at Phase 2 scale.

2. **Intra-training feature importance via permutation:** Computationally expensive (5x forward passes per checkpoint) and provides limited actionable information for a 3-layer MLP. The post-training per-family FPR check (Layer 3) catches the same problems more directly.
   - **Recommendation:** Make optional (recommended but not required for DQS gate).
   - **Impact if removed:** TQS loses one signal; compensated by stronger post-training validation.

3. **Full influence function analysis on every training pair:** At Phase 2 scale (5,500 pairs), feasible. At Phase 3+ (50,000+ pairs), expensive.
   - **Recommendation:** Sample-based influence analysis (20% of pairs) with escalation to full analysis on anomaly detection.
   - **Impact if removed:** Distributed adversarial attacks become harder to detect; mitigated by spectral analysis.

## Not Removable

1. **Label traceability chain (multi-source confirmation):** Core defense against adversarial label poisoning. Without it, the training pipeline is an open attack surface.
2. **Per-family FPR validation:** Core defense against model family bias. Without it, the contrastive model may discriminate against minority model families.
3. **Golden holdout regression test:** Core defense against feedback loop degradation. Without it, quarterly retraining may silently degrade.
4. **TDQR documentation:** Audit trail for governance. Without it, bias decisions are opaque.

## Simplified Architecture

After simplification:
- Layer 1 (Pre-Training): schema + label provenance + distribution analysis + spectral anomaly detection + sampled influence screening. BD-1, BD-2, BD-3, BD-6 active.
- Layer 2 (Intra-Training): embedding variance + per-family loss decomposition + optional feature importance. Lightweight monitoring, not a hard gate (TQS becomes advisory).
- Layer 3 (Post-Training): per-family FPR/FNR + golden holdout regression + adversarial probe. DRS remains the deployment gate.

**Net effect:** Reduces computational overhead by ~40% while retaining all critical bias detection capabilities. TQS downgraded from hard gate to advisory (training continues if TQS < 0.70 but TDQR documents the deviation).

---

**End of DESIGN.**
