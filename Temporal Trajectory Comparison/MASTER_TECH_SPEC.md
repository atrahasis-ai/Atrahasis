# C19 — Temporal Trajectory Comparison

## Master Technical Specification

**Document ID:** C19-MTS-v1.0
**Version:** 1.0.0
**Date:** 2026-03-11
**Invention ID:** C19
**System:** Atrahasis Agent System v2.0
**Status:** SPECIFICATION COMPLETE
**Classification:** CONFIDENTIAL — BlakJaks LLC
**Normative References:** C17 (MCSD Layer 2 v1.0 — B(a_i, a_j) algorithm), C5 (PCVM v2.0), C14 (AiBC v1.0 — MCSD §4.3), C11 (CACT v1.0)
**Resolves:** C17 MF-5 ("Temporal trajectory comparison should be evaluated for Phase 2 inclusion"), C17 OQ-05 ("How should B handle agents that undergo major model upgrades?")

---

## Abstract

C17 defines pairwise behavioral similarity B(a_i, a_j) using five modalities — temporal, structural, error, resource, and lexical — compared at a point in time. This specification defines a sixth modality: **temporal trajectory comparison**, which detects correlated behavioral drift over time. The core insight: AI agents from the same creator tend to drift in similar directions when updated, because they share training data, RLHF preferences, and fine-tuning methodology. Two agents that independently drift toward the same behavioral changes over months are likely same-origin — even if their current behavioral profiles differ.

C19 specifies a hybrid architecture combining drift direction correlation (cosine similarity on cumulative displacement vectors) with trajectory shape comparison (band-constrained Dynamic Time Warping). Population-mean de-trending isolates idiosyncratic agent drift from systematic environmental changes. Per-modality trajectory decomposition preserves C17's interpretability architecture, and multi-task trajectory consistency gating extends C17's anti-coincidence framework to the longitudinal domain.

The trajectory modality activates at Phase 2 for agent pairs with >= 6 months of overlapping behavioral history, contributing weight w_Traj = 0.14 to the B formula. Computational cost is negligible (< 1% addition to C17's compute budget). This specification replaces C17 MTS Section 11 in its entirety.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Architecture Overview](#2-architecture-overview)
3. [Monthly Behavioral Snapshot Extraction](#3-monthly-behavioral-snapshot-extraction)
4. [Population-Mean De-Trending](#4-population-mean-de-trending)
5. [Drift Direction Comparison](#5-drift-direction-comparison)
6. [DTW Shape Comparison](#6-dtw-shape-comparison)
7. [Direction-Shape Fusion](#7-direction-shape-fusion)
8. [Multi-Task Trajectory Consistency](#8-multi-task-trajectory-consistency)
9. [Integration with C17 B Formula](#9-integration-with-c17-b-formula)
10. [Discontinuity Detection and Trajectory Reset](#10-discontinuity-detection-and-trajectory-reset)
11. [Drift Anomaly Detection](#11-drift-anomaly-detection)
12. [Trajectory Explanation Format](#12-trajectory-explanation-format)
13. [Phased Deployment](#13-phased-deployment)
14. [Anti-Gaming Defenses](#14-anti-gaming-defenses)
15. [Formal Requirements](#15-formal-requirements)
16. [Parameters](#16-parameters)
17. [Patent-Style Claims](#17-patent-style-claims)
18. [Risk Analysis](#18-risk-analysis)
19. [C17 Modification Summary](#19-c17-modification-summary)
20. [Glossary](#20-glossary)

---

## 1. Motivation

### 1.1 The Drift Detection Gap

C17's five modalities compare agents at a point in time (within a rolling observation window). This detects same-origin agents whose current behavioral profiles are similar. However, it misses two scenarios:

1. **Deliberate initial diversification, convergent updates.** An adversary creates Sybil agents with deliberately different initial behavioral profiles, then applies the same updates over time. The agents' current profiles differ (low B), but their drift patterns correlate (undetected by C17).

2. **Long-term behavioral convergence.** Two same-origin agents deployed in different environments develop different surface behaviors, but when both are updated with the same training data, they drift in the same direction — converging in behavioral change even while maintaining different absolute profiles.

C17 FEASIBILITY Attack 4 (Gradual Behavioral Drift) identified this gap. C17 Assessment MF-5 flagged temporal trajectory comparison for Phase 2 evaluation. C19 fills this gap.

### 1.2 Core Insight

Behavioral drift is not random. It is driven by model updates, training data changes, and RLHF preference shifts — all of which are controlled by the agent's creator. Agents from the same creator, receiving the same updates, drift in correlated directions through behavioral feature space. This correlation persists even when:

- Agents have different current behavioral profiles (different initial conditions)
- Updates are applied at different times (temporal misalignment of 1-2 months)
- Agents operate in different task environments (different organic task distributions)

The trajectory modality detects this correlated drift — a signal that is orthogonal to point-in-time similarity and adds genuine new information to B(a_i, a_j).

### 1.3 Scope

C19 specifies the temporal trajectory modality ONLY. It does not modify:
- C17's 5 core modalities (feature extraction, distance metrics, weights)
- C17's SEB, LSH, or graduated response protocols
- C17's contrastive learning model (Phase 2)
- C17's PCVM/CACT/AiSIA integration points (beyond trajectory-specific extensions)

C19 extends C17 Section 11, adding the trajectory modality as a 6th input to the B formula when activation criteria are met.

---

## 2. Architecture Overview

### 2.1 Trajectory Comparison Pipeline

```
  Agent a_i Behavioral VTDs (12-month rolling window)
  Agent a_j Behavioral VTDs (12-month rolling window)
            |                           |
            v                           v
  +-------------------+      +-------------------+
  | Monthly Behavioral |      | Monthly Behavioral |
  | Snapshot (MBS)     |      | Snapshot (MBS)     |
  | Extraction         |      | Extraction         |
  | (per modality,     |      | (per modality,     |
  |  per month)        |      |  per month)        |
  +---------+----------+      +---------+----------+
            |                           |
            v                           v
  +---------------------------------------------------+
  | Population-Mean De-Trending                        |
  | MBS_idio = MBS - MBS_pop (trimmed mean)            |
  +------------------------+---------------------------+
                           |
              +------------+------------+
              |                         |
              v                         v
  +--------------------+    +--------------------+
  | Drift Direction    |    | DTW Shape          |
  | Comparison         |    | Comparison         |
  |                    |    |                    |
  | Cumulative         |    | Sakoe-Chiba band   |
  | displacement       |    | w=2, Symmetric2    |
  | cosine similarity  |    | Cosine point dist  |
  | (per modality)     |    | (per modality)     |
  +---------+----------+    +---------+----------+
            |                         |
            +------------+------------+
                         |
                         v
  +---------------------------------------------------+
  | Direction-Shape Fusion                             |
  | d_Traj_m = 0.60 * d_dir_m + 0.40 * DTW_norm_m     |
  | d_Traj = Sum(w_m_traj * d_Traj_m)                  |
  +------------------------+---------------------------+
                           |
                           v
  +---------------------------------------------------+
  | Multi-Task Trajectory Consistency (rho_Traj)       |
  | Per-SEB-category trajectory distances               |
  | rho_Traj = 1 - CV(d_Traj across categories)        |
  +------------------------+---------------------------+
                           |
                           v
  +---------------------------------------------------+
  | Integration with C17 B Formula                     |
  | Trajectory term: w_Traj * d_Traj * rho_Traj        |
  +---------------------------------------------------+
```

### 2.2 Component Ownership

| Component | Owner | Storage |
|-----------|-------|---------|
| MBS extraction | AiSIA (C14) | AiSIA-controlled store |
| MBS_pop computation | AiSIA (C14) | Monthly population statistics |
| Trajectory comparison | AiSIA (C14) | Internal (part of B computation) |
| Discontinuity detection | AiSIA (C14) | Agent trajectory metadata |
| Trajectory explanation | AiSIA (C14) | Appended to BSR (C17 Section 10.4) |

---

## 3. Monthly Behavioral Snapshot Extraction

### 3.1 Definition

A Monthly Behavioral Snapshot MBS_m(a, t) for agent a, modality m, and calendar month t is the mean of all BFE feature vectors for modality m extracted from Behavioral VTDs generated by agent a during month t.

### 3.2 Extraction

```
MBS_m(a, t) = mean({ BFE_m(vtd) : vtd in VTDs(a, month=t) })

Where BFE_m(vtd) is the modality-m feature vector extracted from a single Behavioral VTD,
using the same feature extraction as C17 Section 4.
```

Each feature is z-score normalized against population statistics for month t:

```
MBS_m_z(a, t)[i] = (MBS_m(a, t)[i] - pop_mean_m(t)[i]) / pop_std_m(t)[i]
```

### 3.3 Dimensionality

| Modality | Snapshot Dims | Source |
|----------|--------------|--------|
| Temporal (T) | 24 | C17 Section 4.2 |
| Structural (S) | 32 | C17 Section 4.3 |
| Error (E) | 23 | C17 Section 4.4 |
| Resource (R) | 21 | C17 Section 4.5 |
| Lexical (L) | 753 | C17 Section 4.6 |

### 3.4 Validity Requirements

- **Minimum VTDs per month:** >= 5 Behavioral VTDs in the calendar month for a valid snapshot
- **Months with < 5 VTDs:** marked as missing (handled per Section 6.5)
- **Minimum valid snapshots for trajectory:** >= 6 valid monthly snapshots within any 9-month window

### 3.5 Storage

- Monthly snapshots retained for 24 months (vs. 12 months for raw VTDs)
- Stored in AiSIA-controlled store alongside Behavioral VTDs
- Snapshot size: ~850 floats per agent per month per modality = ~3.4 KB per agent per month (all modalities)
- At Phase 3 (100K agents): ~340 MB per month, ~8 GB for 24-month retention

---

## 4. Population-Mean De-Trending

### 4.1 Purpose

All agents may drift systematically due to environmental changes: SEB task pool refresh (20% quarterly), system-wide updates, seasonal task distribution shifts. Population-mean de-trending removes these systematic effects to isolate agent-specific (idiosyncratic) drift that carries the same-origin signal.

### 4.2 Population-Mean Snapshot

```
MBS_pop_m(t) = TrimmedMean({ MBS_m_z(a, t) : a in active_agents(t) }, trim=0.10)
```

Where TrimmedMean removes the top and bottom 10% of values per dimension before averaging. The trim resists bias from same-origin clusters that might dominate the population mean.

**active_agents(t):** All agents with a valid MBS for month t.

### 4.3 Idiosyncratic Snapshot

```
MBS_idio_m(a, t) = MBS_m_z(a, t) - MBS_pop_m(t)
```

### 4.4 Computation Cadence

- Population-mean snapshots computed monthly at month-end
- Historical population means are immutable once computed (deterministic comparison)
- Population means are NOT published to agents (information asymmetry, C17 Section 14.4)

### 4.5 Minimum Population Requirement

Population-mean de-trending activates when >= 50 agents have valid MBS for the month. Below this threshold, raw MBS_m_z is used without de-trending, and the trajectory similarity threshold is increased by 0.10 (higher bar for trajectory-only detection to compensate for systematic drift confounds).

---

## 5. Drift Direction Comparison

### 5.1 Cumulative Displacement Vector

For agent a with valid idiosyncratic snapshots at months t_1 (earliest) through t_n (most recent) in the overlap window with agent b:

```
drift_dir_m(a) = MBS_idio_m(a, t_n) - MBS_idio_m(a, t_1)
```

This vector represents the total direction of idiosyncratic behavioral drift in modality m over the comparison window.

### 5.2 Direction Distance

```
d_dir_m(a_i, a_j) = 1 - |cosine_similarity(drift_dir_m(a_i), drift_dir_m(a_j))|
```

Absolute cosine similarity is used: both positively correlated drift (cosine ~ +1) and anti-correlated drift (cosine ~ -1) indicate a shared cause. Independent agents have uncorrelated drift (cosine ~ 0).

**Range:** d_dir_m in [0, 1].
- d_dir_m = 0: drift directions are perfectly (anti-)correlated
- d_dir_m = 1: drift directions are orthogonal (uncorrelated)

### 5.3 Edge Case: Zero Drift

If ||drift_dir_m(a)|| < epsilon (epsilon = 0.01 after normalization), the agent has effectively zero idiosyncratic drift in modality m. In this case:
- d_dir_m is undefined and excluded from the trajectory distance computation for that modality
- If both agents have zero drift in modality m, d_dir_m is set to 0.5 (neutral — no evidence either way)
- Zero-drift anomaly detection is handled separately (Section 11)

---

## 6. DTW Shape Comparison

### 6.1 Input Sequences

For each modality m, the input to DTW is the sequence of idiosyncratic monthly snapshots over the overlap window:

```
seq_m(a) = [MBS_idio_m(a, t_1), MBS_idio_m(a, t_2), ..., MBS_idio_m(a, t_n)]
```

Where t_1 through t_n are the calendar months in the overlap window (both agents have valid snapshots or interpolated values).

### 6.2 DTW Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Step pattern | Symmetric2 (Sakoe-Chiba Type IV) | Steps: (1,0), (0,1), (1,1) with weights 1, 1, 2. Prevents pathological many-to-one mappings. |
| Band width (w) | 2 months | Warping path cannot deviate > 2 months from diagonal. Handles staggered updates of up to 2 months. |
| Point distance | Cosine distance: 1 - cosine_similarity(x_i, y_j) | Uniform across modalities. Appropriate for aggregate monthly vectors. |
| Normalization | Path-length normalization: DTW_raw / path_length | Ensures distance is independent of trajectory length. |

### 6.3 DTW Computation

```
Given:
  X = seq_m(a_i) of length n
  Y = seq_m(a_j) of length m
  Band width w = 2

Initialize cost matrix D[0..n, 0..m] = infinity
D[0, 0] = 0

For i = 1 to n:
  For j = max(1, i-w) to min(m, i+w):
    cost = cosine_distance(X[i], Y[j])
    D[i, j] = cost + min(
      D[i-1, j]   + cost * 1,    // vertical step (weight 1)
      D[i, j-1]   + cost * 1,    // horizontal step (weight 1)
      D[i-1, j-1] + cost * 2     // diagonal step (weight 2)
    )

DTW_raw_m = D[n, m]
path_length = length of optimal warping path (backtraced)
DTW_norm_m(a_i, a_j) = DTW_raw_m / path_length
```

**Range:** DTW_norm_m in [0, 1] (cosine distance per point is in [0, 1]).

### 6.4 Complexity

Per modality: O(n * (2w+1) * d) where n = trajectory length (months), w = band width, d = modality dimensionality.

For n=12, w=2, d=30 (average): 12 * 5 * 30 = 1,800 operations per modality per pair.
Across 5 modalities: 9,000 operations per pair. Negligible.

### 6.5 Missing Month Handling

If a month is marked as missing (< 5 VTDs):
- **Single missing month:** Linearly interpolate from adjacent valid months
- **Two consecutive missing months:** Linearly interpolate (maximum interpolation span)
- **Three or more consecutive missing months:** Trajectory is split into segments at the gap. Each segment must have >= 3 valid months to be compared. Segment distances are averaged, weighted by segment length.

---

## 7. Direction-Shape Fusion

### 7.1 Per-Modality Trajectory Distance

```
d_Traj_m(a_i, a_j) = beta * d_dir_m(a_i, a_j) + (1 - beta) * DTW_norm_m(a_i, a_j)

Where:
  beta = 0.60 (drift direction weight)
  (1 - beta) = 0.40 (DTW shape weight)
```

**Rationale:** Drift direction is the primary signal (agents from the same creator drift in the same direction). DTW shape captures the supplementary signal (the pattern of drift unfolds similarly over time). The 60/40 split reflects this priority.

### 7.2 Cross-Modality Aggregation

```
d_Traj(a_i, a_j) = Sum_{m in M_valid} (w_m_traj_norm * d_Traj_m(a_i, a_j))

Where:
  M_valid = modalities with valid trajectory data (both agents have valid data)
  w_m_traj = C17 adversary weights: T=0.30, S=0.25, E=0.20, R=0.15, L=0.10
  w_m_traj_norm = w_m_traj / Sum(w for m in M_valid)  (renormalized to available modalities)
```

If a modality is excluded (zero drift, insufficient data), the remaining modalities' weights are renormalized to sum to 1.0.

**Range:** d_Traj in [0, 1].

### 7.3 DTW Disablement Governance

If empirical evaluation during Phase 2 shows DTW adds < 5% detection improvement over drift direction alone (measured by AUROC delta on known same-origin pairs), AiSIA may disable DTW via governance:
- Set beta = 1.0 (direction only)
- Requires Stiftung board ratification
- 30-day notice period

---

## 8. Multi-Task Trajectory Consistency

### 8.1 Purpose

Analogous to C17's multi-task cross-correlation (rho_m), the trajectory consistency coefficient rho_Traj distinguishes genuine correlated drift (consistent across task types) from coincidental trajectory similarity in one task category.

### 8.2 Per-Task-Category Trajectories

For each of the 7 SEB task categories (C17 Section 7.2) and each modality m:

```
MBS_m_c(a, t) = mean of BFE_m features from VTDs in task category c during month t
```

**Validity:** Requires >= 2 VTDs in category c during month t for a valid per-category snapshot.

### 8.3 Per-Category Trajectory Distance

Compute d_Traj_m_c(a_i, a_j) for each valid category c using the same direction-shape fusion (Section 7.1).

### 8.4 Trajectory Consistency Coefficient

```
For each modality m:
  d_values = [d_Traj_m_c for c in valid_categories]  (minimum 3 valid categories)

  rho_Traj_m = 1 - CV(d_values)
  CV = std(d_values) / mean(d_values)
  rho_Traj_m clamped to [0, 1]

Aggregate:
  rho_Traj = mean(rho_Traj_m for m in M_valid)
```

**Interpretation:**
- rho_Traj close to 1: trajectory similarity is consistent across task categories (likely shared origin)
- rho_Traj close to 0: trajectory similarity varies wildly by category (likely coincidence)

### 8.5 Minimum Category Requirement

Multi-task trajectory consistency requires valid per-category trajectories in >= 3 of 7 SEB categories. If fewer than 3 categories have valid data, rho_Traj defaults to 0.5 (neutral) and a flag is set indicating insufficient task diversity for trajectory consistency assessment.

---

## 9. Integration with C17 B Formula

### 9.1 Updated B Formula (Phase 2, Trajectory Active)

When trajectory comparison is active for both agents in a pair:

```
B(a_i, a_j) = 1 - [ Sum_{m in {T,S,E,R,L}} (w'_m * d_m_mean * rho_m)
                     + w_Traj * d_Traj(a_i, a_j) * rho_Traj ]
```

### 9.2 Updated Weight Table

| Modality | 5-Modality Weight (C17) | 6-Modality Weight (C19, trajectory active) |
|----------|------------------------|-------------------------------------------|
| Temporal (T) | 0.30 | 0.26 |
| Structural (S) | 0.25 | 0.22 |
| Error (E) | 0.20 | 0.17 |
| Resource (R) | 0.15 | 0.13 |
| Lexical (L) | 0.10 | 0.08 |
| Trajectory (Traj) | N/A | 0.14 |
| **Total** | **1.00** | **1.00** |

Weight redistribution is proportional to current weight: each modality donates approximately the same fraction (13-17%) of its weight.

### 9.3 Activation Criteria

Trajectory comparison activates for a pair (a_i, a_j) when ALL of the following are true:
1. Phase 2 or later is active
2. Both agents have >= 6 valid monthly snapshots
3. The overlap window (months where both have valid snapshots) spans >= 6 months
4. Population-mean de-trending is active (>= 50 agents with valid MBS)

When inactive, the standard C17 5-modality weights apply without modification.

### 9.4 Interaction with B_combined (Phase 2)

When both the contrastive learned model (C17 Section 12) and trajectory comparison are active:

```
B_combined = alpha * B_statistical_6mod + (1 - alpha) * B_learned
```

Where B_statistical_6mod uses the 6-modality formula from Section 9.1. The contrastive model's embedding input should include trajectory features (aggregate d_Traj and rho_Traj) as additional input dimensions, extending the encoder input from 853 to 855 dimensions.

---

## 10. Discontinuity Detection and Trajectory Reset

### 10.1 Purpose

When an agent undergoes a major model architecture change (e.g., migrating from GPT-4 to Llama-3), its behavioral profile shifts discontinuously. Pre-discontinuity trajectory data is not comparable to post-discontinuity data. C19 detects these discontinuities and resets the trajectory.

This resolves C17 OQ-05: "How should B handle agents that undergo major model upgrades?"

### 10.2 Discontinuity Detection

A discontinuity at month t for agent a in modality m:

```
delta_m(a, t) = ||MBS_m(a, t) - MBS_m(a, t-1)||_2

Discontinuity if: delta_m(a, t) > mu_delta_m(t) + k * sigma_delta_m(t)

Where:
  mu_delta_m(t) = population mean of delta_m(*, t)
  sigma_delta_m(t) = population std of delta_m(*, t)
  k = 3 (default, adjustable [2, 5])
```

### 10.3 Multi-Modality Confirmation

A **confirmed discontinuity** requires detection in >= 3 of 5 modalities simultaneously. Single-modality discontinuities are treated as noise or task-specific variation — not model changes.

### 10.4 Reset Protocol

1. Agent's trajectory is split at the discontinuity month
2. Only post-discontinuity snapshots are used for future trajectory comparison
3. Trajectory comparison deactivates for this agent until 6 new post-discontinuity monthly snapshots accumulate
4. During deactivation, 5-modality weights apply for pairs involving this agent

### 10.5 Reset Frequency Monitoring

| Resets per year | Classification | Action |
|----------------|----------------|--------|
| 0-1 | Normal | No action. Legitimate model upgrades are infrequent. |
| 2 | Elevated | Agent added to trajectory-reset watch list. Enhanced SEB frequency. |
| 3+ | Anomalous | Flagged for AiSIA investigation. Possible trajectory evasion attempt. |

### 10.6 Governance

- Discontinuity threshold (k sigma): adjustable by AiSIA, range [2, 5]
- Multi-modality confirmation threshold: adjustable by AiSIA, range [2, 5] modalities
- Reset frequency limits: adjustable by AiSIA, range [1, 3] per year for Normal classification

---

## 11. Drift Anomaly Detection

### 11.1 Drift Suppression Anomaly

Agents with near-zero idiosyncratic drift are suspicious — all agents naturally drift as their task portfolios evolve and models are updated. Near-zero drift suggests deliberate drift suppression to avoid trajectory comparison (FEASIBILITY Attack 4 defense).

```
Anomaly condition:
  ||drift_dir_m(a)|| < 0.1 * median_drift_magnitude_m
  for >= 3 modalities simultaneously
  for >= 3 consecutive months

Action: Agent added to drift-suppression watch list. Enhanced SEB frequency (quarterly instead of annual).
```

### 11.2 Anomalous Drift Magnitude

Agents with extremely high idiosyncratic drift (> 5x population median) in multiple modalities may be injecting noise to obscure their trajectory (FEASIBILITY Attack 3 defense).

```
Anomaly condition:
  ||drift_dir_m(a)|| > 5.0 * median_drift_magnitude_m
  for >= 3 modalities simultaneously

Action: Flag for investigation. High drift magnitude combined with performance degradation (C5 PCVM quality metrics) is strong evidence of noise injection.
```

---

## 12. Trajectory Explanation Format

### 12.1 Extension to C17 BSR

When trajectory comparison contributes to a WATCH or FLAG decision, the Behavioral Similarity Report (C17 Section 10.4) is extended with a TRAJECTORY ANALYSIS section:

```
TRAJECTORY ANALYSIS
===================
Comparison window: [start_month] to [end_month] ([n] months, [v] valid snapshots each)
Population-mean de-trending: [applied | not applied (insufficient population)]
Discontinuities detected: [none | list with months]

Per-modality trajectory breakdown:
  [Modality] (w=[traj_weight]):
    Drift direction distance: [d_dir_m]
    DTW shape distance:       [DTW_norm_m]
    Fused trajectory dist:    [d_Traj_m]
    Task-category consistency: [rho_Traj_m]

Aggregate trajectory distance: [d_Traj]
Aggregate trajectory consistency: [rho_Traj]
Trajectory contribution to B: w_Traj * d_Traj * rho_Traj = [value]

Interpretation:
  [Human-readable summary of which modalities show correlated drift,
   over which time period, and across which task categories.]

Drift anomalies: [none | drift suppression | excessive drift magnitude]
```

### 12.2 Tribunal Readability

The trajectory explanation is designed for non-technical adjudication by the Constitutional Tribunal (C14). The interpretation section must:
- State in plain language whether the agents' behavioral changes over time are correlated
- Identify which types of behavioral change (timing, reasoning structure, errors, etc.) show correlation
- State the time period over which correlation was observed
- Note any caveats (short trajectory, limited task categories, population-mean instability)

---

## 13. Phased Deployment

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
> Note: C19 introduces a sub-phase within Phase 2 — trajectory shadow mode (months 18-24) followed by trajectory active deployment (month 24+, contingent on 6 months of shadow validation data). C20 gates contrastive model deployment at Phase 2 entry via the DRS >= 0.90 requirement.

### 13.1 Phase 0-1: Data Accumulation

| Component | Status |
|-----------|--------|
| MBS extraction | **Active** — monthly snapshots computed and stored from Phase 0 |
| Population-mean computation | **Active** — computed monthly once >= 50 agents |
| Trajectory comparison | **Inactive** — insufficient history |
| Weight allocation | 5-modality C17 weights (trajectory not active) |

**Phase 0-1 goal:** Accumulate 6+ months of monthly snapshots. Validate MBS extraction. Monitor population-mean drift magnitude. Build baseline for drift magnitude statistics.

### 13.2 Phase 2: Shadow Activation (Months 18-24)

| Component | Status |
|-----------|--------|
| All Phase 0-1 components | Active |
| Trajectory comparison | **Shadow mode** — computed and logged but does not affect B score |
| Discontinuity detection | Active |
| Drift anomaly detection | Active (logging only) |

**Phase 2 shadow goal:** Validate trajectory modality FPR/FNR. Compare trajectory-enhanced B against 5-modality B on known pairs. Calibrate thresholds.

### 13.3 Phase 2: Active Deployment (Month 24+)

| Component | Status |
|-----------|--------|
| All shadow components | Active |
| Trajectory comparison | **Active** — contributes to B with w_Traj = 0.14 |
| 6-modality weights | Active for qualifying pairs |

**Activation criteria:**
- 6 months of shadow data demonstrating trajectory FPR < 0.05% (isolation) and trajectory-enhanced B FPR < 0.1% (combined)
- AiSIA recommendation with empirical analysis
- Stiftung board ratification

### 13.4 Phase 3: Mature Operation

| Component | Status |
|-----------|--------|
| All Phase 2 components | Active, mature |
| DTW evaluation | Empirical assessment: if DTW adds < 5% detection improvement, governance may set beta=1.0 |
| Population de-trending | May upgrade to PCA de-trending (top-k principal components) if empirical data shows higher-order systematic structure |

---

## 14. Anti-Gaming Defenses

### 14.1 Defense Catalog

| ID | Attack | Defense | Effectiveness |
|----|--------|---------|---------------|
| TG-01 | Synchronized update avoidance (stagger updates > 2 months) | Drift direction comparison is alignment-insensitive; DTW band handles <= 2 months; dynamic band widening for high-direction-similarity pairs | HIGH |
| TG-02 | Decorrelated update strategy (different training data per agent) | Economic deterrent (separate training pipelines = cost multiplier); 5 core modalities still detect base-model similarity | HIGH (by design) |
| TG-03 | Noise injection into drift | Multi-month averaging; drift magnitude anomaly detection; performance degradation detection via PCVM | MEDIUM |
| TG-04 | Mimicking population-mean drift (zero idiosyncratic drift) | Drift suppression anomaly detection; population mean published only quarterly (info asymmetry); per-task-category deconfounding | MEDIUM |
| TG-05 | Trajectory replay (mimic legitimate agent's trajectory) | Individual trajectories not published (info asymmetry); engineering a specific trajectory requires precise update calibration (expensive) | HIGH |
| TG-06 | Model architecture switch to break trajectory | Discontinuity detection and reset; frequent resets flagged as anomalous | HIGH |
| TG-07 | Boiling-frog decorrelation (gradually diverge updates) | Cumulative evidence in rolling window; WATCH persistence (6 months); historical record | MEDIUM |
| TG-08 | Opposite-direction updates (anti-correlated drift) | Absolute cosine similarity detects anti-correlation as suspicious | HIGH |
| TG-09 | Trajectory length inequality exploitation (stagger registration) | Minimum overlap requirement (6 months); staggered registration detectable by Layer 3 | HIGH |
| TG-10 | Spurious correlation exploitation (identify false positives to discredit system) | Population-mean de-trending; multi-task consistency; moderate weight (0.14); whitelist mechanism | MEDIUM-HIGH |

### 14.2 Information Asymmetry

Agents MUST NOT have access to:
- Their own monthly behavioral snapshots
- Population-mean drift vectors (published only as quarterly anonymized aggregates per C17)
- Their own trajectory comparison scores or distances
- Other agents' trajectory data

This extends C17 Section 14.4 to trajectory-specific data.

---

## 15. Formal Requirements

### 15.1 Functional Requirements

| ID | Requirement | Priority | Verification |
|----|-------------|----------|-------------|
| C19-FR-01 | Monthly Behavioral Snapshots SHALL be computed for all agents with >= 5 VTDs in a calendar month, for each of the 5 modalities | P0 | MBS pipeline validation |
| C19-FR-02 | Population-mean de-trending SHALL use trimmed mean (trim=0.10) and SHALL activate when >= 50 agents have valid MBS | P0 | De-trending validation |
| C19-FR-03 | Drift direction distance SHALL use absolute cosine similarity: d_dir = 1 - \|cos(drift_i, drift_j)\| | P0 | Unit test |
| C19-FR-04 | DTW SHALL use Symmetric2 step pattern with Sakoe-Chiba band width w=2 and cosine point distance | P0 | Unit test |
| C19-FR-05 | DTW distance SHALL be path-length normalized to [0, 1] | P0 | Unit test |
| C19-FR-06 | Direction-shape fusion SHALL use beta=0.60 for direction, (1-beta)=0.40 for DTW shape | P0 | Unit test |
| C19-FR-07 | Cross-modality aggregation SHALL use C17 adversary weights renormalized to available modalities | P0 | Unit test |
| C19-FR-08 | Multi-task trajectory consistency (rho_Traj) SHALL be computed across >= 3 of 7 SEB task categories | P0 | Integration test |
| C19-FR-09 | Trajectory comparison SHALL activate only when both agents have >= 6 valid monthly snapshots with >= 6-month overlap | P0 | Activation logic test |
| C19-FR-10 | When trajectory is active, B formula SHALL use 6-modality weights per Section 9.2 | P0 | B computation test |
| C19-FR-11 | When trajectory is inactive, B formula SHALL use C17's standard 5-modality weights unchanged | P0 | B computation test |
| C19-FR-12 | Discontinuity detection SHALL require simultaneous detection in >= 3 of 5 modalities at > k sigma | P0 | Detection test |
| C19-FR-13 | Trajectory reset SHALL deactivate trajectory comparison for the affected agent until 6 new post-discontinuity snapshots accumulate | P0 | Reset protocol test |
| C19-FR-14 | Agents with >= 3 trajectory resets per year SHALL be flagged for AiSIA investigation | P1 | Monitoring test |
| C19-FR-15 | Drift suppression anomaly detection SHALL flag agents with drift magnitude < 0.1x median for >= 3 modalities for >= 3 months | P1 | Anomaly detection test |
| C19-FR-16 | WATCH and FLAG decisions involving trajectory contribution SHALL include the trajectory explanation format per Section 12 | P0 | Explanation generation test |
| C19-FR-17 | Monthly snapshots SHALL be retained for 24 months | P1 | Data lifecycle test |
| C19-FR-18 | Missing months SHALL be linearly interpolated (max 2 consecutive); gaps > 2 months SHALL split the trajectory into segments | P1 | Missing data handling test |

### 15.2 Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| C19-NFR-01 | Trajectory comparison for one agent pair SHALL complete in < 10 ms | P1 |
| C19-NFR-02 | Monthly snapshot extraction for all agents SHALL complete within 1 hour of month-end | P1 |
| C19-NFR-03 | Population-mean computation SHALL complete within 10 minutes of MBS extraction completion | P1 |
| C19-NFR-04 | Trajectory comparison SHALL add < 1% to C17's total B computation time | P1 |

---

## 16. Parameters

| ID | Parameter | Value | Range | Governance |
|----|-----------|-------|-------|------------|
| C19-P-01 | w_Traj (trajectory weight) | 0.14 | [0.05, 0.20] | AiSIA + Stiftung board |
| C19-P-02 | beta (direction vs. shape fusion) | 0.60 | [0.40, 1.00] | AiSIA + Stiftung board |
| C19-P-03 | DTW band width (w) | 2 months | [1, 4] months | AiSIA |
| C19-P-04 | Min valid snapshots for activation | 6 | [4, 12] | AiSIA |
| C19-P-05 | Min overlap window for activation | 6 months | [4, 12] months | AiSIA |
| C19-P-06 | Trimmed mean trim percentage | 10% | [5%, 20%] | AiSIA |
| C19-P-07 | Min population for de-trending | 50 agents | [20, 200] | AiSIA |
| C19-P-08 | Discontinuity threshold (k sigma) | 3.0 | [2.0, 5.0] | AiSIA |
| C19-P-09 | Discontinuity modality confirmation | 3 of 5 | [2, 5] of 5 | AiSIA |
| C19-P-10 | Drift suppression threshold | 0.1x median | [0.05, 0.20]x median | AiSIA |
| C19-P-11 | Drift magnitude anomaly threshold | 5.0x median | [3.0, 10.0]x median | AiSIA |
| C19-P-12 | Max consecutive interpolated months | 2 | [1, 3] | AiSIA |
| C19-P-13 | MBS retention window | 24 months | [12, 36] months | AiSIA |
| C19-P-14 | Min VTDs per month for valid snapshot | 5 | [3, 10] | AiSIA |

---

## 17. Patent-Style Claims

### Claim 1: Temporal Trajectory Comparison for AI Agent Sybil Detection

A method for detecting same-origin artificial intelligence agents by comparing their behavioral drift trajectories over time, comprising:
(a) extracting monthly behavioral snapshots from verification trace documents for each agent across multiple behavioral modalities;
(b) computing and subtracting a population-mean trajectory to isolate idiosyncratic agent-specific drift;
(c) comparing idiosyncratic drift between agent pairs using both drift direction correlation (cosine similarity on cumulative displacement vectors) and trajectory shape similarity (band-constrained Dynamic Time Warping);
(d) gating the trajectory comparison with multi-task consistency to distinguish genuine correlated drift from coincidental similarity;
(e) incorporating the trajectory distance as an additional modality in a multi-modal behavioral similarity score;
wherein agents from the same creator are detected by their correlated behavioral changes over time, even when their current behavioral profiles differ.

### Claim 2: Population-Mean De-Trending for Behavioral Drift Analysis

A method for isolating agent-specific behavioral drift from systematic environmental drift in a population of AI agents, comprising:
(a) computing per-modality monthly behavioral snapshots for each agent;
(b) computing a trimmed population mean across all agents for each modality and each month;
(c) subtracting the population mean from each agent's snapshot to produce an idiosyncratic drift component;
(d) comparing idiosyncratic drift components between agent pairs to detect correlated drift indicative of shared origin;
wherein systematic environmental changes (task pool updates, system-wide modifications) that would cause false positive detections are removed, leaving only the agent-specific drift signal that reveals shared creator origin.

### Claim 3: Discontinuity Detection and Trajectory Reset for Model Architecture Changes

A method for handling major model architecture changes in a behavioral trajectory comparison system, comprising:
(a) monitoring monthly behavioral change magnitude against population statistics;
(b) detecting discontinuities when change magnitude exceeds a threshold in multiple behavioral modalities simultaneously;
(c) resetting the agent's trajectory history at the discontinuity point, using only post-discontinuity data for future comparisons;
(d) monitoring reset frequency as an indicator of potential trajectory evasion attempts;
wherein the system adapts to legitimate model upgrades while detecting adversarial attempts to break trajectory comparison through frequent architecture switching.

---

## 18. Risk Analysis

### 18.1 Risk Register

| ID | Risk | Probability | Impact | Severity | Mitigation |
|----|------|-------------|--------|----------|-----------|
| C19-R-01 | Population-mean de-trending removes too much signal (homogeneous population) | 15% | MEDIUM | LOW-MEDIUM | Monitor idiosyncratic/total drift ratio; fallback to model-family-specific de-trending |
| C19-R-02 | DTW band width too narrow for common staggered updates | 10% | LOW | LOW | Governed parameter; monitor band boundary hits; widen if needed |
| C19-R-03 | Per-task-category trajectories have insufficient data for rho_Traj | 20% | LOW | LOW | Minimum 3-category requirement; default rho_Traj=0.5 when insufficient |
| C19-R-04 | Trajectory false positives from model-family systematic drift (imperfect de-trending) | 15% | MEDIUM | MEDIUM | Multi-task consistency gating; moderate weight (0.14); whitelist |
| C19-R-05 | Adversary successfully injects noise to obscure drift direction | 10% | MEDIUM | LOW-MEDIUM | Multi-month averaging; drift magnitude anomaly detection; PCVM quality monitoring |
| C19-R-06 | 6-month activation delay allows adversary to evade during early period | 20% | LOW | LOW | By design — 5-modality B operates from day 1; trajectory is supplementary |

### 18.2 Residual Risks

1. **Decorrelated update strategy.** An adversary willing to maintain separate training pipelines for each Sybil agent can produce genuinely decorrelated drift. This is the intended economic deterrent — the cost multiplier applies.

2. **Slow decorrelation (boiling frog).** An adversary who gradually introduces divergent updates can eventually decorrelate trajectories. The rolling window and WATCH persistence provide partial defense, but a sufficiently patient adversary (12+ months of sustained decorrelation) can exit detection. This is an inherent limitation of any longitudinal comparison with finite memory.

---

## 19. C17 Modification Summary

C19 requires the following modifications to C17-MTS-v1.0:

| C17 Section | Modification | Type |
|-------------|-------------|------|
| Section 3.1 (System Diagram) | Add trajectory comparison block after BFE | Extension |
| Section 6.1 (Primary Formula) | No change (trajectory not active in Phase 0-1) | None |
| Section 6.3 (Weight Constraints) | Add w_Traj to constraint set: w_Traj in [0.05, 0.20] | Extension |
| Section 6.4 (Phase 2+ Formula) | Update to include trajectory term | Modification |
| **Section 11 (Temporal Trajectory)** | **Full replacement with C19 specification** | **Replacement** |
| Section 12.1 (Contrastive Encoder) | Input dims: 853 -> 855 (add d_Traj, rho_Traj) | Modification |
| Section 15.3 (Phase 2 Components) | Trajectory row: reference C19 specification | Update |
| Section 16 FR-18 | "DTW on monthly BFE snapshots" -> "per C19 specification" | Update |
| Section 17 P-22 | Validated (w_Traj = 0.14) | Confirmed |
| Section 17 P-23 | trajectory_min_history: 6 months / 6 windows (was 6 months / 4 windows) | Correction |
| Section 20 OQ-05 | **RESOLVED** — discontinuity detection and trajectory reset (C19 Section 10) | Resolution |
| New parameters | C19-P-01 through C19-P-14 added | Extension |

---

## 20. Glossary

| Term | Definition |
|------|-----------|
| **beta** | Direction-shape fusion weight: 0.60 for direction, 0.40 for shape |
| **d_dir_m** | Drift direction distance for modality m (absolute cosine distance on displacement vectors) |
| **d_Traj** | Aggregate trajectory distance across all modalities |
| **d_Traj_m** | Fused trajectory distance for modality m (beta * direction + (1-beta) * DTW) |
| **Discontinuity** | A statistically significant behavioral break (> k sigma in >= 3 modalities) indicating model architecture change |
| **Drift direction** | The cumulative displacement vector of an agent's idiosyncratic behavioral snapshots over time |
| **DTW** | Dynamic Time Warping — algorithm for comparing time series with temporal misalignment |
| **DTW_norm_m** | Path-length normalized DTW distance for modality m |
| **MBS** | Monthly Behavioral Snapshot — aggregated behavioral feature vector per agent per modality per month |
| **MBS_idio** | Idiosyncratic MBS — agent-specific snapshot after population-mean subtraction |
| **MBS_pop** | Population-mean MBS — trimmed mean of all agents' snapshots for a given month |
| **rho_Traj** | Multi-task trajectory consistency coefficient — measures whether trajectory similarity is consistent across SEB task categories |
| **Sakoe-Chiba band** | DTW constraint limiting warping to a band of width w around the diagonal |
| **Symmetric2** | DTW step pattern allowing horizontal, vertical, and diagonal steps with weights 1, 1, 2 |
| **Trajectory reset** | Clearing pre-discontinuity trajectory data after a confirmed model architecture change |
| **w_Traj** | Weight of the trajectory modality in the B formula (0.14 when active) |

---

**End of Master Technical Specification**

**Document ID:** C19-MTS-v1.0
**Status:** SPECIFICATION COMPLETE
**Line count:** ~600 lines
**Resolves:** C17 MF-5 (trajectory evaluation), C17 OQ-05 (model upgrade handling)
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Temporal Trajectory Comparison\MASTER_TECH_SPEC.md`
