# C21 --- FPR Validation Methodology

## Master Technical Specification

**Document ID:** C21-MTS-v1.0
**Version:** 1.0.0
**Date:** 2026-03-11
**Invention ID:** C21
**System:** Atrahasis Agent System v2.0
**Status:** SPECIFICATION COMPLETE
**Classification:** CONFIDENTIAL --- BlakJaks LLC
**Normative References:** C17 (MCSD Layer 2 v1.0), C5 (PCVM v2.0), C14 (AiBC v1.0 --- MCSD Section 4.3), C8 (DSF v2.0)
**Resolves:** C17 MF-1 ("FPR must be validated empirically before deployment")

---

## Abstract

C17 (MCSD Layer 2 Behavioral Similarity Algorithm) computes B(a_i, a_j) in [0,1] to detect same-origin AI agents. Its critical constraint --- FPR < 0.1% (C17 FR-13, P0; C17 P-21, Constitutional) --- must be validated empirically before the algorithm is applied to real governance decisions. C17 MF-1 requires this validation during Phase 0 using synthetic agent populations.

This specification defines the Phased Empirical Validation Framework (PEVF): a three-tier methodology for validating and continuously monitoring B(a_i,a_j)'s false positive rate. Tier 1 (pre-deployment) generates a synthetic agent population from architecture-specific distributional priors, computes B on 10,000+ labeled pairs, and establishes FPR confidence bounds via Clopper-Pearson exact intervals. Tier 2 (shadow validation) applies sequential testing with O'Brien-Fleming alpha-spending to real agent pairs during Phase 0 shadow deployment. Tier 3 (live monitoring) maintains a Known-Independent Pair Reservoir (KIPR) of operator-controlled test agents, applies Bernoulli CUSUM drift detection, and conducts quarterly batch audits.

The PEVF ensures that FPR < 0.1% is validated at 95% confidence before Phase 1 deployment, continuously monitored during live operation, and automatically recalibrated when drift is detected.

---

## Table of Contents

1. [Motivation and Gap Analysis](#1-motivation-and-gap-analysis)
2. [Architecture Overview](#2-architecture-overview)
3. [Tier 1: Pre-Deployment Synthetic Validation](#3-tier-1-pre-deployment-synthetic-validation)
4. [Tier 2: Shadow Validation](#4-tier-2-shadow-validation)
5. [Tier 3: Live Monitoring](#5-tier-3-live-monitoring)
6. [Recalibration Protocol](#6-recalibration-protocol)
7. [Appeal and Ground-Truth Resolution](#7-appeal-and-ground-truth-resolution)
8. [Absolute False Positive Projections](#8-absolute-false-positive-projections)
9. [Integration with C17, C5, C14](#9-integration-with-c17-c5-c14)
10. [Formal Requirements](#10-formal-requirements)
11. [Parameters](#11-parameters)
12. [Patent-Style Claims](#12-patent-style-claims)
13. [Risk Analysis](#13-risk-analysis)
14. [Open Questions](#14-open-questions)
15. [Glossary](#15-glossary)
16. [References](#16-references)

---

## 1. Motivation and Gap Analysis

### 1.1 The Validation Gap

C17 specifies B(a_i, a_j) and requires FPR < 0.1% (C17 FR-13, P0). C17 P-21 makes this limit Constitutional (immutable). (C21 inherits this as C21 P-01.) C17 MF-1 states: "FPR must be measured empirically during Phase 0 with synthetic agent populations before applying to real governance."

But C17 does not specify:
- How to generate synthetic agent populations for testing
- What statistical methodology establishes FPR confidence bounds
- How to continuously monitor FPR after deployment
- When and how to recalibrate if FPR drifts

C21 fills this gap with a complete validation methodology.

### 1.2 Why Empirical Validation Is Non-Negotiable

FPR cannot be derived analytically from B(a_i, a_j)'s formula because it depends on the empirical distribution of behavioral features across the agent population. Two facts make empirical validation essential:

1. **Distribution dependence.** B is a function of statistical distances between feature vectors. The false positive rate depends on how close genuinely independent agents' features are --- which is a property of the population, not the algorithm.

2. **Scale amplification.** At Phase 2 (10,000 agents), there are ~50 million agent pairs. Even FPR = 0.1% produces ~50,000 false flags among LSH candidates. The real-world impact of FPR must be validated, not assumed.

### 1.3 Scope

C21 specifies:
- Pre-deployment validation (Tier 1): synthetic populations, statistical tests, pass criteria
- Shadow validation (Tier 2): real-agent sequential testing during Phase 0
- Live monitoring (Tier 3): continuous FPR tracking, drift detection, recalibration
- Appeal resolution: process for disputed FLAG classifications

C21 does not modify B(a_i, a_j) itself (C17's domain) or the graduated response protocol (C17 Section 10). C21 validates the system that C17 specifies.

---

## 2. Architecture Overview

```
                    TIER 1: PRE-DEPLOYMENT
                    (Before Phase 0 Shadow)

    +------------------------------------------+
    | Synthetic Agent Population Generator      |
    | (SAPG)                                    |
    |                                           |
    | Architecture Template Library (54+ types) |
    | Per-modality distributional models         |
    | Same-origin perturbation model             |
    | Adversarial pair generation                |
    +--------------------+---------------------+
                         |
                         v
    +------------------------------------------+
    | Test Protocol                             |
    |                                           |
    | 10,000+ labeled pairs                     |
    | B(a_i, a_j) computation (C17 pipeline)    |
    | Clopper-Pearson 95% CI                    |
    | Ensemble validation (5 parameterizations) |
    | PASS: CI upper bound < 0.1%              |
    +--------------------+---------------------+
                         |
              PASS       |       FAIL
              |          |          |
              v          |          v
    Proceed to Tier 2    |    Recalibrate C17
                         |    theta_B / weights
                         |    and re-run Tier 1

                    TIER 2: SHADOW VALIDATION
                    (Phase 0, No Enforcement)

    +------------------------------------------+
    | Sequential Testing                        |
    |                                           |
    | O'Brien-Fleming alpha-spending             |
    | 4 interim analyses                        |
    | Ground truth: infrastructure + org + model |
    | Calibration budget: 50-100 real pairs     |
    +--------------------+---------------------+
                         |
              PASS       |       FAIL
              |          |          |
              v          |          v
    Proceed to Phase 1   |    Recalibrate and
    + activate Tier 3    |    extend Phase 0

                    TIER 3: LIVE MONITORING
                    (Phase 1+ Continuous)

    +------------------------------------------+
    | Known-Independent Pair Reservoir (KIPR)   |
    | 15+ agents, 105+ pairs, quarterly refresh |
    |                                           |
    | Bernoulli CUSUM drift detection            |
    | Quarterly batch audit (KIPR + 1000 pairs) |
    | Infrastructure-stratified FPR estimation  |
    |                                           |
    | Recalibration triggers:                   |
    | - CUSUM signal                            |
    | - Quarterly FPR > 0.08%                   |
    | - New model family onboarded              |
    +------------------------------------------+
```

---

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
> C21 tier-to-phase mapping: Tier 1 (pre-deployment synthetic validation) completes before Phase 0 shadow deployment. Tier 2 (shadow validation) runs during Phase 0 (months 0-6). Tier 2 completion authorizes Phase 1 entry. Tier 3 (live monitoring) activates at Phase 1 (month 7+) and runs continuously thereafter.

## 3. Tier 1: Pre-Deployment Synthetic Validation

### 3.1 Synthetic Agent Population Generator (SAPG)

The SAPG generates synthetic Behavioral VTDs (per C17 Section 8) for agents with known ground truth. It is parameterized by an Architecture Template Library (ATL).

#### 3.1.1 Architecture Template Library

Templates are defined along three axes:

**Model Families (minimum 6):** Dense Transformer, Mixture-of-Experts, Recurrent/SSM, Diffusion-based, Small Distilled, Ensemble/Routing. Each family has characteristic behavioral signatures in temporal, structural, and resource modalities.

**Infrastructure Types (minimum 3):** Single high-end GPU, Multi-GPU distributed, CPU/edge. Each type has characteristic temporal and resource signatures.

**Training Regimes (minimum 3):** Large-scale pre-training + RLHF, Domain-specific fine-tuning, Few-shot/in-context. Each regime has characteristic error and lexical signatures.

**Minimum template count:** 6 x 3 x 3 = 54. Minimum 3 agents per template. Minimum 162 agents total.

#### 3.1.2 Per-Modality Distributional Models

For each template, the SAPG assigns parametric distributions to each of C17's 27 behavioral features across 5 modalities:

- **Temporal (6 features):** Shifted lognormal for latencies, gamma for inter-token intervals, beta for ratios, AR(1) for autocorrelation. Parameters from published inference benchmarks (MLPerf, vLLM).
- **Structural (6 features):** Poisson for chain depth, geometric for branching, beta for rates, lognormal for step sizes. Parameters from published chain-of-thought analyses. NOTE: This modality has the weakest distributional grounding (C21 MF-1).
- **Error (5 features):** Beta for accuracies, Platt-scaled calibration from published ECE data, Wishart for error correlation, Dirichlet for confidence histograms.
- **Resource (5 features):** Beta for utilization, truncated normal for memory, lognormal for throughput. Parameters from published hardware benchmarks.
- **Lexical (5 features):** Dirichlet-multinomial for vocabulary, beta for type-token ratio, multinomial for n-grams. Parameters from published model output analyses.

Intra-modality feature correlations are encoded via Cholesky decomposition of per-modality correlation matrices, with correlation coefficients estimated from published benchmarks or set conservatively (r < 0.3) when data is unavailable.

#### 3.1.3 Same-Origin Perturbation Model

Same-origin agent pairs are generated by applying controlled perturbations to a base agent's feature vectors:

- **Perturbation types:** Fine-tuning (lexical + error shift), infrastructure (resource + temporal shift), prompt (structural shift), combined (all modalities).
- **Perturbation magnitude:** delta in [0.05, 0.4], where delta = 0 is identical and delta = 1 is fully independent.
- **Purpose:** Establish true positive rate (TPR) and characterize the detection boundary.

#### 3.1.4 Adversarial Synthetic Pairs

Independent agents engineered to be maximally similar, stress-testing the FPR boundary:

- **Convergent architecture pairs:** Different templates with infrastructure and training chosen to minimize behavioral distance.
- **Mimicry pairs:** One template's features shifted toward another template's profile.
- **Coincidence pairs:** Random pairs that are close in exactly one modality (testing multi-modal fusion).
- **Minimum count:** 1,000 adversarial pairs.

### 3.2 Test Protocol

#### 3.2.1 Pair Generation

| Type | Count | Purpose |
|------|-------|---------|
| Independent (random templates) | 6,000 | Primary FPR estimation |
| Independent (adversarial close) | 1,000 | Adversarial FPR stress test |
| Same-origin (low delta, < 0.2) | 1,500 | TPR estimation |
| Same-origin (high delta, 0.2-0.4) | 1,500 | Detection boundary |
| **Total** | **10,000** | |

#### 3.2.2 Scoring

For each pair: generate 30 SEB task responses per agent, extract Behavioral VTDs, compute B(a_i, a_j) via C17's full pipeline (5-modality distances, multi-task cross-correlation, adversary-weighted fusion), classify via graduated response.

#### 3.2.3 Primary Analysis: FPR at FLAG Threshold

- FPR_hat = (false positives at FLAG) / (total independent pairs)
- 95% confidence interval: Clopper-Pearson exact method
- **PASS criterion: upper bound of 95% CI < 0.001 (0.1%)**

With 7,000 independent pairs and 0 observed FPs: upper bound = 0.043% (PASS). With 1 FP: need to verify upper bound < 0.1% (passes at 7,000). With 2 FPs: upper bound = 0.092% (borderline PASS at 7,000). With 3 FPs: upper bound = 0.118% (FAIL at 7,000 --- would need recalibration or more pairs).

#### 3.2.4 Secondary Analyses

- FPR at WATCH threshold (0.60): documented but no pass/fail criterion
- Per-model-family-pair FPR: no family pair may exceed 2x aggregate FPR (per C17 bias monitoring requirement)
- Adversarial-pair FPR separately: documented, expected to be higher than random-pair FPR
- TPR at FLAG threshold for delta < 0.2: must exceed 90%
- Full ROC curve: FPR vs. TPR across theta_B range [0.50, 0.90]

#### 3.2.5 Ensemble Validation

Repeat the full Tier 1 protocol with 5 different SAPG parameterizations, each varying distributional parameters within plausible ranges:
- Ensemble member 1: Central estimates for all parameters
- Ensemble members 2-5: Each shifts one modality's parameters to the boundary of the plausible range (high variance, low variance, shifted mean, heavy tails)

**PASS criterion: FPR < 0.1% in ALL 5 ensemble members.** If any member fails, investigate which distributional assumption causes divergence and widen the ensemble.

### 3.3 Tier 1 -> Tier 2 Handoff

After Tier 1 completes, produce a Tier 1 Validation Report containing:
- Overall FPR estimate with 95% CI
- Per-model-family-pair FPR matrix (identifying elevated-risk combinations)
- TPR estimate by perturbation magnitude
- Recommended theta_B (may differ from C17 default of 0.75 if Tier 1 analysis suggests adjustment)
- Priority model families for Tier 2 shadow validation (families with highest pairwise FPR)

---

## 4. Tier 2: Shadow Validation

### 4.1 Phase 0 Shadow Deployment

During C17 Phase 0, B(a_i, a_j) is computed on real agents in shadow mode (no governance enforcement). Tier 2 uses this shadow data for sequential FPR validation.

### 4.2 Ground Truth Establishment

For each agent pair in the shadow dataset, independence is established via:

1. **Infrastructure attestation:** Verified-different infrastructure providers (cloud accounts, hardware, IP ranges)
2. **Organizational verification:** Different registered organizations (with identity verification)
3. **Model card:** Different declared model architectures
4. **Consensus rule:** A pair is labeled "independent" only if ALL THREE signals agree. If any signal is ambiguous, the pair is excluded from the validation dataset.

### 4.3 Sequential Testing Protocol

**Design:** Group sequential test with O'Brien-Fleming alpha-spending.

- Total alpha = 0.05 (95% confidence)
- Number of interim analyses: 4 (at information fractions 0.25, 0.50, 0.75, 1.00)
- Target sample size: 500 independent pairs (per C17 Phase 0 minimum)
- O'Brien-Fleming z-boundaries: (4.05, 2.86, 2.34, 2.02)

**At each interim analysis k:**
1. Compute cumulative FPR_hat = FP_count / n_k
2. Compute test statistic z_k = (FPR_hat - 0.001) / sqrt(0.001 * 0.999 / n_k)
3. If z_k < -z_boundary_k (FPR significantly below limit): early PASS
4. If z_k > z_boundary_k (FPR significantly above limit): early FAIL --- halt deployment, recalibrate
5. Otherwise: continue to next interim analysis

**Batch-aware scheduling:** Interim analyses are triggered when the accumulated independent-pair count crosses 125, 250, 375, 500 (not at fixed calendar dates).

### 4.4 Calibration Budget

**Purpose:** Validate that Tier 1 synthetic FPR estimates correspond to real FPR.

- Select 50-100 real agent pairs from Phase 0 shadow data where ground truth is established with high confidence
- Compute B on these pairs and measure FPR_real
- Compare to the Tier 1 FPR estimate for the corresponding model-family combinations
- **Calibration tolerance:** FPR_real must be within 3x of FPR_synthetic for matching family pairs
- If calibration fails: update SAPG distributional parameters using real data, re-run Tier 1, and re-validate

### 4.5 Tier 2 Completion Criteria

Tier 2 passes when:
1. Sequential test reaches PASS at any interim analysis, AND
2. Calibration budget confirms synthetic-real correspondence within tolerance

Tier 2 passage authorizes Phase 1 deployment with Tier 3 monitoring activated.

---

## 5. Tier 3: Live Monitoring

### 5.1 Known-Independent Pair Reservoir (KIPR)

**Construction:**
- AiSIA maintains minimum 15 operator-controlled test agents
- Agents span 5+ model families, 3+ infrastructure types
- Deployed on verified-separate infrastructure with verified-different architectures
- C(15, 2) = 105 known-independent pairs

**Maintenance:**
- Quarterly refresh: retire 3 agents, onboard 3 new agents
- At least 1 new agent must be from the most recently onboarded model family in the general population
- Annual re-verification of infrastructure attestation for all reservoir agents
- Reservoir agents participate in normal SEB but are excluded from Sybil enforcement

### 5.2 Bernoulli CUSUM Drift Detection

**Configuration:**
- Target: p_0 = 0.001 (FPR)
- Shift to detect: p_1 = 0.002 (doubling of FPR)
- Reference value: k = 0.00144
- Decision interval: h = 5

**Operation:** After each B computation cycle on KIPR pairs:
- For each pair yielding a false positive (B >= theta_B): X_t = 1; otherwise X_t = 0
- S_t = max(0, S_{t-1} + X_t - k)
- If S_t > h: TRIGGER recalibration investigation

**Note on statistical power:** With 105 KIPR pairs per cycle, and quarterly cycles, the CUSUM accumulates ~420 observations per year. At p_0 = 0.001, the expected false positives per year is 0.42. The CUSUM will detect a sustained doubling (p_1 = 0.002) with ARL_1 ~ 100 observations, corresponding to approximately one quarter of data. This is adequate for detecting persistent drift but will not catch transient spikes --- quarterly batch audits cover transient effects.

### 5.3 Quarterly Batch Audit

Every quarter:
1. Compute B on all 105+ KIPR pairs
2. Compute B on 1,000 randomly sampled cross-infrastructure pairs from the general population
3. Compute FPR_kipr and FPR_pop with Clopper-Pearson 95% CIs
4. Record results as a PCVM verification claim (C5)

**Trigger thresholds:**
- FPR_kipr upper CI > 0.08%: RECALIBRATION ADVISORY (investigate within 30 days)
- FPR_kipr upper CI > 0.1%: RECALIBRATION MANDATORY (pause FLAG enforcement, raise theta_B by 0.05)
- FPR_pop upper CI > 2x FPR_kipr: RESERVOIR DIVERGENCE WARNING (KIPR may not represent population; expand reservoir)

### 5.4 New Model Family Onboarding

When a new model family is detected in the agent population (not represented in existing KIPR):
1. Onboard at least 2 test agents from the new family into KIPR
2. Compute B between new-family agents and all existing KIPR agents
3. If new-family pairwise FPR > 0.2%: escalate to recalibration before onboarding more agents from this family
4. Add new-family agents to permanent KIPR roster

---

## 6. Recalibration Protocol

### 6.1 Triggers

| Trigger | Source | Urgency |
|---------|--------|---------|
| CUSUM signal | Tier 3 CUSUM chart | ADVISORY (30-day investigation) |
| Quarterly FPR > 0.08% | Tier 3 batch audit | MANDATORY (30-day recalibration) |
| Quarterly FPR > 0.1% | Tier 3 batch audit | EMERGENCY (immediate pause + recalibration) |
| New family FPR > 0.2% | Tier 3 new family onboarding | MANDATORY (block new family until resolved) |
| Calibration budget failure | Tier 2 | MANDATORY (re-run Tier 1 with updated SAPG) |

### 6.2 Recalibration Steps

1. **Diagnosis:** Compute per-modality FPR contributions via modality ablation. Identify the modality or feature driving FPR increase.
2. **Parameter adjustment (choose one or more):**
   - Increase theta_B by minimum increment (0.01) to restore FPR < 0.08% on KIPR
   - Reduce problematic modality's fusion weight w_m (within C17 DA-01 governance bounds)
   - Update SEB task pool to include tasks that better discriminate the problematic modality
3. **Re-validation:** Run Tier 1 with updated parameters. Must pass ensemble validation.
4. **Governance:** Submit parameter change proposal to AiSIA (per C17 DA-01). Requires standard governance approval.
5. **Deployment:** Roll out updated parameters. Monitor with elevated frequency (monthly instead of quarterly) for 2 cycles.

### 6.3 Emergency Recalibration

When FPR > 0.1% is confirmed:
1. **Immediate:** Pause FLAG enforcement. All FLAG classifications are downgraded to WATCH until recalibration completes. WATCH monitoring continues.
2. **Within 24 hours:** Notify Constitutional Tribunal. Begin diagnosis.
3. **Within 7 days:** Deploy recalibrated theta_B (increased by minimum 0.05).
4. **Within 30 days:** Complete full Tier 1 re-validation with updated parameters.
5. **Restoration:** FLAG enforcement resumes only after Tier 1 re-validation passes.

---

## 7. Appeal and Ground-Truth Resolution

When an agent pair disputes a FLAG classification:

1. **Automatic re-evaluation:** Assign fresh SEB task instance (30 new randomized tasks). Recompute B. If B < theta_B on fresh tasks: reclassify as WATCH.
2. **Explanation:** Provide per-modality distance breakdown showing which modalities contributed most.
3. **Infrastructure verification:** Independent verification that agents run on different infrastructure. If verified independent: pair becomes KIPR candidate.
4. **Tribunal escalation:** If steps 1-3 do not resolve, escalate to Constitutional Tribunal (C14).
5. **Ground-truth recording:** Outcome recorded. Confirmed-independent pairs with high B are added to FPR monitoring dataset (known false positives). Confirmed same-origin pairs are true positives.

This appeal process generates labeled data that improves future FPR estimation and SAPG calibration.

---

## 8. Absolute False Positive Projections

FPR as a rate does not convey operational impact. The following table projects absolute false positive counts at each deployment phase, assuming FPR_raw = 0.1% on LSH-candidate pairs:

| Phase | Agents | LSH Candidate Pairs (est.) | Expected FPs (FPR=0.1%) | Expected FPs (FPR=0.05%) | Graduated Response |
|-------|--------|---------------------------|------------------------|--------------------------|-------------------|
| 0 | 100 | ~2,000 | 2 | 1 | Manageable |
| 1 | 1,000 | ~50,000 | 50 | 25 | WATCH absorbs ~80% |
| 2 | 10,000 | ~500,000 | 500 | 250 | Requires automated triage |
| 3 | 100,000 | ~5,000,000 | 5,000 | 2,500 | Requires automated triage + appeal capacity |

**Notes:**
- LSH candidate pair estimates assume k=20 neighbors per agent (C17 LSH configuration)
- WATCH classification absorbs ~80% of false flags (B in [0.60, theta_B)); only ~20% reach FLAG
- At Phase 2+, automated triage is required: auto-resolve FLAGS where fresh SEB re-evaluation drops B below theta_B
- Maximum tolerable absolute FP count should be set per phase by AiSIA governance

---

## 9. Integration with C17, C5, C14

### 9.1 C17 Integration Points

| C17 Component | C21 Usage |
|---------------|-----------|
| B(a_i, a_j) pipeline (Sections 4-6) | Tier 1/2/3 scoring --- C21 runs C17's exact pipeline |
| Behavioral VTD schema (Section 8) | SAPG generates synthetic VTDs conforming to this schema |
| SEB (Section 7) | Tier 1 simulates SEB; Tier 2/3 use real SEB data |
| theta_B and w_m parameters (DA-01) | Recalibration protocol adjusts these parameters |
| Graduated response (Section 10) | C21 measures FPR at FLAG threshold; WATCH statistics are secondary |
| LSH pre-filter (Section 9) | Post-deployment FPR_raw is measured on LSH candidates |
| Bias monitoring (FR-13) | Per-model-family FPR validation in Tier 1 |

### 9.2 C5 (PCVM) Integration

- Tier 3 quarterly audit results are recorded as PCVM verification claims
- Recalibration events are recorded as PCVM governance claims
- Appeal outcomes are recorded as PCVM dispute resolution claims

### 9.3 C14 (AiBC) Integration

- Tier 2 completion is a prerequisite for Phase 1 Citicate issuance
- Emergency recalibration pauses FLAG enforcement (governance impact)
- Constitutional Tribunal handles appeal escalations
- FPR_hard_limit (0.1%) is a Constitutional parameter (C17 P-21, inherited as C21 P-01) --- C21 cannot modify it

---

## 10. Formal Requirements

| ID | Requirement | Priority | Verification |
|----|-------------|----------|-------------|
| FR-01 | SAPG SHALL generate synthetic Behavioral VTDs conforming to C17 Section 8 schema | P0 | Schema validation |
| FR-02 | ATL SHALL contain minimum 54 templates (6 families x 3 infra x 3 training) | P0 | Template count check |
| FR-03 | Tier 1 SHALL generate minimum 7,000 independent pairs and 3,000 same-origin pairs | P0 | Pair count check |
| FR-04 | Tier 1 SHALL include minimum 1,000 adversarial close pairs | P1 | Pair count check |
| FR-05 | Tier 1 PASS criterion: Clopper-Pearson 95% CI upper bound < 0.1% on independent pairs | P0 | Statistical test |
| FR-06 | Tier 1 SHALL validate FPR across 5 ensemble parameterizations; ALL must pass | P0 | Ensemble results |
| FR-07 | Per-model-family-pair FPR SHALL NOT exceed 2x aggregate FPR in any Tier 1 ensemble member | P1 | Per-family analysis |
| FR-08 | TPR at FLAG threshold for same-origin pairs (delta < 0.2) SHALL exceed 90% | P1 | TPR calculation |
| FR-09 | Tier 2 SHALL use O'Brien-Fleming alpha-spending with total alpha = 0.05 and 4 interim analyses | P0 | Protocol compliance |
| FR-10 | Tier 2 ground truth SHALL require consensus of infrastructure, organizational, and model-card verification | P0 | Ground truth protocol |
| FR-11 | Calibration budget SHALL include 50-100 real agent pairs; synthetic FPR must be within 3x of real FPR for matching families | P0 | Calibration check |
| FR-12 | KIPR SHALL contain minimum 15 operator-controlled test agents spanning 5+ model families | P0 | Reservoir audit |
| FR-13 | Tier 3 SHALL implement Bernoulli CUSUM with parameters k=0.00144, h=5 | P1 | Configuration check |
| FR-14 | Quarterly batch audit SHALL compute FPR on KIPR pairs + 1,000 cross-infrastructure pairs | P0 | Audit records |
| FR-15 | Emergency recalibration SHALL pause FLAG enforcement within 24 hours of confirmed FPR > 0.1% | P0 | Incident response |
| FR-16 | All recalibration events SHALL be recorded as PCVM verification claims (C5) | P1 | PCVM records |
| FR-17 | New model family onboarding SHALL add minimum 2 test agents to KIPR | P1 | Onboarding protocol |
| FR-18 | Tier 1 -> Tier 2 handoff SHALL include per-family FPR matrix and priority families for shadow validation | P1 | Handoff report |

---

## 11. Parameters

> **Parameter numbering convention:** C21 parameters use the C21-P-XX namespace. P-01 is inherited from C17 P-21 (FPR_hard_limit) and is listed here for completeness — C17 P-21 is the authoritative source. All other parameters (P-02 through P-15) are C21-local. When referencing C21 parameters from other specs, use the prefix "C21 P-XX" to distinguish from C17's parameter numbering.

| ID | Parameter | Default | Adjustable | Governance |
|----|-----------|---------|------------|------------|
| P-01 | FPR_hard_limit (inherited: C17 P-21) | 0.1% | No | Constitutional (C17 P-21, immutable) |
| P-02 | tier1_min_independent_pairs | 7,000 | Yes (increase only) | AiSIA proposal |
| P-03 | tier1_min_adversarial_pairs | 1,000 | Yes (increase only) | AiSIA proposal |
| P-04 | tier1_ensemble_count | 5 | Yes (increase only) | AiSIA proposal |
| P-05 | tier1_confidence_level | 95% | Yes (increase only) | AiSIA proposal |
| P-06 | tier2_alpha | 0.05 | No | Fixed (statistical convention) |
| P-07 | tier2_interim_count | 4 | Yes | AiSIA proposal |
| P-08 | tier2_min_pairs | 500 | Yes (increase only) | AiSIA proposal |
| P-09 | calibration_tolerance | 3x | Yes (decrease = stricter) | AiSIA proposal |
| P-10 | kipr_min_agents | 15 | Yes (increase only) | AiSIA proposal |
| P-11 | kipr_min_families | 5 | Yes (increase only) | AiSIA proposal |
| P-12 | cusum_k | 0.00144 | Yes | AiSIA proposal |
| P-13 | cusum_h | 5 | Yes | AiSIA proposal |
| P-14 | quarterly_audit_sample_size | 1,000 | Yes (increase only) | AiSIA proposal |
| P-15 | recalibration_advisory_threshold | 0.08% | Yes (decrease = stricter) | AiSIA proposal |

---

## 12. Patent-Style Claims

### Claim 1

A method for validating the false positive rate of a pairwise behavioral similarity function applied to AI agents, comprising:

(a) generating a synthetic agent population using an Architecture Template Library that parameterizes behavioral feature distributions across model families, infrastructure types, and training regimes;

(b) generating labeled agent pairs including independent pairs, same-origin pairs, and adversarial-close independent pairs;

(c) computing the behavioral similarity score for each labeled pair using the pairwise similarity function under test;

(d) computing a confidence interval on the observed false positive rate using an exact binomial method;

(e) repeating steps (a)-(d) with multiple ensemble parameterizations of the Architecture Template Library to validate robustness to distributional assumptions;

wherein the validation passes only if the confidence interval upper bound is below a specified threshold for all ensemble parameterizations.

### Claim 2

A system for continuous monitoring of false positive rate in a deployed behavioral similarity function for AI agents, comprising:

(a) a Known-Independent Pair Reservoir of operator-controlled test agents with verified-independent ground truth;

(b) a cumulative sum (CUSUM) drift detection chart operating on binary false-positive outcomes from the reservoir;

(c) periodic batch audits computing false positive rate on the reservoir and a random sample of the general population;

(d) recalibration triggers that pause enforcement and adjust classification thresholds when the monitored false positive rate exceeds specified bounds;

wherein the monitoring system maintains continuous statistical assurance that the false positive rate remains below a constitutional limit.

### Claim 3

A method for calibrating a synthetic agent population generator against real agent data, comprising:

(a) generating synthetic agent populations from architecture-specific distributional priors;

(b) measuring the false positive rate of a similarity function on the synthetic population;

(c) measuring the false positive rate on a calibration budget of real agent pairs with verified ground truth;

(d) comparing synthetic and real false positive rates for matching model-family combinations;

(e) updating the synthetic generator's distributional parameters if synthetic and real rates diverge beyond a specified tolerance;

wherein the calibration ensures that pre-deployment validation using synthetic data is predictive of real-world performance.

---

## 13. Risk Analysis

| ID | Risk | Likelihood | Severity | Impact | Mitigation |
|----|------|-----------|----------|--------|------------|
| R-01 | SAPG distributional assumptions do not match real agent diversity | 25% | HIGH | Tier 1 validation is non-predictive | Ensemble validation + calibration budget + SAPG update protocol |
| R-02 | Structural modality distributions poorly characterized | 30% | MEDIUM | Tier 1 FPR estimate unreliable for structural-driven FPs | Conservative structural parameters + wider ensemble spread on structural modality |
| R-03 | KIPR becomes unrepresentative of population | 15% | MEDIUM | Tier 3 FPR estimates diverge from true FPR | Quarterly refresh with newest model families + reservoir divergence warning |
| R-04 | Ground truth establishment has false independence labels | 10% | HIGH | Tier 2 FPR is underestimated (FPs are hidden as "not-FP") | Triple-signal consensus rule (infra + org + model) |
| R-05 | Base rate amplification overwhelms dispute resolution at scale | 20% | MEDIUM | Legitimate agents excluded from governance during dispute backlog | Automatic re-evaluation on fresh SEB + absolute FP count governance |
| R-06 | Adversary games SAPG by studying its parameters | 10% | LOW | Adversary creates agents in SAPG blind spots | SAPG parameters are operational (not published); Tier 2/3 catch real-world gaps |

---

## 14. Open Questions

| ID | Question | Priority | Owner | Expected Resolution |
|----|----------|----------|-------|-------------------|
| OQ-01 | What are the actual distributional parameters for structural modality features (chain depth, branching factor) across real model families? | P1 | Science Advisor | Phase 0 shadow data (month 3) |
| OQ-02 | Should the maximum tolerable absolute FP count be a governance parameter per phase? | P2 | AiSIA | Policy decision before Phase 2 |
| OQ-03 | Can SAPG be augmented with GAN-based generation after Tier 2 calibration data is available? | P2 | Architecture Designer | Phase 1 research |

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **ATL** | Architecture Template Library --- catalog of synthetic agent type definitions |
| **CUSUM** | Cumulative Sum control chart for sequential change detection |
| **FPR** | False Positive Rate --- fraction of independent pairs incorrectly classified as same-origin |
| **KIPR** | Known-Independent Pair Reservoir --- operator-maintained set of verified-independent test agents |
| **PEVF** | Phased Empirical Validation Framework --- C21's three-tier methodology |
| **SAPG** | Synthetic Agent Population Generator --- system for creating synthetic behavioral profiles |
| **SEB** | Standardized Evaluation Battery --- C17's randomized task set for behavioral comparison |
| **TPR** | True Positive Rate --- fraction of same-origin pairs correctly classified |
| **VTD** | Verification Trace Document --- behavioral data generated during PCVM verification |

---

## 16. References

1. ISO/IEC 19795-1:2021 --- Biometric performance testing and reporting
2. Clopper, C. J. & Pearson, E. S. (1934) --- "The use of confidence or fiducial limits illustrated in the case of the binomial"
3. O'Brien, P. C. & Fleming, T. R. (1979) --- "A multiple testing procedure for clinical trials"
4. Lan, K. K. G. & DeMets, D. L. (1983) --- "Discrete sequential boundaries for clinical trials"
5. Page, E. S. (1954) --- "Continuous inspection schemes"
6. C17-MTS-v1.0 --- MCSD Layer 2 Behavioral Similarity Algorithm
7. C5-MTS-v2.0 --- PCVM (Proof-Carrying Verification Model)
8. C14-MTS-v1.0 --- AiBC (Artificial Intelligence Benefit Company)
9. NIST SP 800-76-2 --- Biometric Specifications for Personal Identity Verification
10. FDA Guidance on Adaptive Designs for Clinical Trials (2019)

---

*End of Master Technical Specification*

**Document ID:** C21-MTS-v1.0
**Line Count:** ~580
**Status:** SPECIFICATION COMPLETE
