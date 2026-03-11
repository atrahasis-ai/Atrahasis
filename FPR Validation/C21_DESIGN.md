# C21 --- FPR Validation Methodology --- DESIGN

**Invention ID:** C21
**Stage:** DESIGN
**Date:** 2026-03-11
**Concept:** C21-A+ --- Phased Empirical Validation Framework (PEVF)

---

# PART 1 --- PRE-DEPLOYMENT VALIDATION DESIGN

## 1.1 Synthetic Agent Population Generator (SAPG)

### 1.1.1 Architecture

The SAPG generates synthetic Behavioral VTDs (per C17 Section 8) that simulate the behavioral output of agents with known ground truth (same-origin or independent). It operates in four stages:

```
    Architecture Template Library (ATL)
    [N model families x M infrastructure types x K training regimes]
              |
              v
    +----------------------------------+
    | Stage 1: Template Selection       |
    | - LHS sampling in template space  |
    | - Minimum coverage per category   |
    +----------------------------------+
              |
              v
    +----------------------------------+
    | Stage 2: Feature Distribution     |
    |   Parameterization                |
    | - Per-modality distribution       |
    |   assignment                      |
    | - Inter-feature correlation       |
    |   matrices                        |
    | - Same-origin perturbation model  |
    +----------------------------------+
              |
              v
    +----------------------------------+
    | Stage 3: Behavioral VTD           |
    |   Generation                      |
    | - Draw feature vectors from       |
    |   parameterized distributions     |
    | - Generate per-SEB-task profiles  |
    | - Apply intra-agent consistency   |
    +----------------------------------+
              |
              v
    +----------------------------------+
    | Stage 4: Pair Labeling            |
    | - Independent pairs: different    |
    |   templates                       |
    | - Same-origin pairs: same         |
    |   template, perturbation model    |
    | - Adversarial pairs: different    |
    |   templates, engineered closeness |
    +----------------------------------+
```

### 1.1.2 Architecture Template Library (ATL)

Each template specifies the generative parameters for one "type" of agent. Templates are defined along three axes:

**Model Family (minimum 6):**
| Family ID | Representative Architecture | Key Behavioral Signatures |
|-----------|---------------------------|--------------------------|
| MF-1 | Dense Transformer (GPT-class) | Uniform latency, deep reasoning chains, moderate memory |
| MF-2 | Mixture-of-Experts (MoE) | Bimodal latency (expert routing), sparse activation, high throughput variance |
| MF-3 | Recurrent/SSM (Mamba-class) | Low latency, shallow chains, linear memory scaling |
| MF-4 | Diffusion-based reasoning | High latency, iterative refinement chains, high GPU utilization |
| MF-5 | Small distilled models | Very low latency, short chains, low resource consumption, higher error rates |
| MF-6 | Ensemble/routing models | Multi-modal latency, variable chain depth, high memory |

**Infrastructure Type (minimum 3):**
| Infra ID | Configuration | Key Signatures |
|----------|--------------|----------------|
| IT-1 | Single high-end GPU (A100/H100) | Low latency variance, high throughput, high memory |
| IT-2 | Multi-GPU distributed | Higher latency variance, batch-dependent throughput |
| IT-3 | CPU/edge inference | High latency, low throughput, low memory, quantization artifacts |

**Training Regime (minimum 3):**
| Regime ID | Configuration | Key Signatures |
|-----------|--------------|----------------|
| TR-1 | Large-scale pre-training + RLHF | Broad vocabulary, calibrated confidence, standard error patterns |
| TR-2 | Domain-specific fine-tuning | Narrow vocabulary peaks, specialized error patterns, calibration drift |
| TR-3 | Few-shot / in-context learning | High output variance, inconsistent error patterns, vocabulary following prompt |

**Total minimum templates:** 6 x 3 x 3 = 54 templates. From 54 templates, generate 3+ agents per template = 162+ agents. C(162, 2) = 13,041 pairs.

### 1.1.3 Per-Modality Distributional Models

For each template, the SAPG assigns distributional parameters to each of the 5 modalities (27 features per C17 Section 4):

**Temporal Modality (6 features):**
- First-token latency: Shifted Lognormal(mu, sigma) with mu in [2.0, 8.0] (log-ms), sigma in [0.1, 0.8]
- Inter-token interval: Gamma(alpha, beta) with alpha in [1.5, 10], beta scaled to architecture
- Burst/pause ratio: Beta(a, b) with a, b derived from architecture type
- Parallelism index: Uniform(0.1, 0.95) for single GPU, Beta(3, 2) for multi-GPU
- Response time CV: derived from latency distribution
- Temporal autocorrelation: AR(1) coefficient in [0.1, 0.8]

**Structural Modality (6 features):**
- Chain depth distribution: Poisson(lambda) with lambda in [2, 15] by architecture
- Branching factor: Geometric(p) with p in [0.3, 0.8]
- Backtrack rate: Beta(a, b) with a in [1, 3], b in [5, 20]
- Step-size distribution: Lognormal(mu, sigma) with mu in [3, 7] (log-tokens)
- Linearity index: Beta(a, b) scaled by chain depth
- Conclusion-to-evidence ratio: Normal(mu, sigma) truncated to [0, 1]

**Error Modality (5 features):**
- Per-category accuracy: Beta(a, b) with a, b from published benchmarks per model family
- Calibration curve: Platt scaling parameters from published ECE data
- Error correlation matrix: Wishart distribution with df from published co-occurrence data
- Confidence histogram: Dirichlet distribution with parameters from calibration data
- Novel-error rate: Beta(1, 100) (rare events)

**Resource Modality (5 features):**
- GPU utilization: Beta(a, b) with parameters from published inference benchmarks
- Memory consumption: Normal(mu, sigma) truncated, parameters from model size + infrastructure
- Throughput (tokens/s): Lognormal(mu, sigma) from published benchmarks
- Batch efficiency curve: Sigmoid parameters from infrastructure type
- Power consumption ratio: derived from GPU utilization + infrastructure

**Lexical Modality (5 features):**
- Vocabulary distribution: Dirichlet-Multinomial with parameters from published model output analyses
- Type-token ratio: Beta(a, b) from published analyses per model family
- N-gram frequency profile: Multinomial with probabilities from published corpora
- Syntax complexity (mean parse depth): Normal(mu, sigma) from published analyses
- Formality index: Beta(a, b) from model-specific output style

### 1.1.4 Inter-Feature Correlation

Features within a modality are correlated (e.g., high GPU utilization correlates with high throughput). The SAPG uses per-modality correlation matrices:

- **Specification method:** For each template, define a correlation matrix R_m (for modality m) using the Cholesky decomposition approach. Generate uncorrelated features, then apply L * z where L = cholesky(R_m).
- **Correlation sources:** Published benchmarks and system profiling data. Where data is unavailable, use conservative estimates (low correlation, r < 0.3).

### 1.1.5 Same-Origin Perturbation Model

To generate same-origin pairs (positive controls), the SAPG applies controlled perturbations to a base agent:

- **Fine-tuning perturbation:** Small shifts in lexical and error features (simulates fine-tuning variants)
- **Infrastructure perturbation:** Changes to resource and temporal features (simulates same model on different hardware)
- **Prompt perturbation:** Changes to structural features (simulates different system prompts)
- **Combined perturbation:** All three simultaneously (hardest case)

Perturbation magnitude is parameterized by delta in [0, 1], where delta=0 is identical and delta=1 is fully independent. Same-origin pairs use delta in [0.05, 0.4] (the range where B(a_i,a_j) should still detect shared origin).

### 1.1.6 Adversarial Synthetic Pairs

Independent agents engineered to be maximally similar (stress-testing FPR):

- **Convergent architecture:** Two genuinely different architectures (e.g., MF-1 and MF-3) with infrastructure and training chosen to minimize behavioral distance
- **Mimicry agents:** Template B with lexical and structural features shifted toward Template A
- **Coincidence pairs:** Randomly generated pairs that happen to be close in one modality (testing that multi-modal fusion prevents single-modality coincidence from triggering FP)

Minimum: 1,000 adversarial pairs out of 10,000+ total pairs.

## 1.2 Test Protocol

### 1.2.1 Pair Generation Plan

| Pair Type | Count | Purpose |
|-----------|-------|---------|
| Independent (random templates) | 6,000 | Primary FPR estimation |
| Independent (adversarial close) | 1,000 | Adversarial FPR stress test |
| Same-origin (low delta) | 1,500 | True positive rate estimation |
| Same-origin (high delta) | 1,500 | Detection boundary estimation |
| **Total** | **10,000** | |

### 1.2.2 Scoring Protocol

For each pair:
1. Generate 30 SEB task responses per agent (per C17 Section 7)
2. Extract Behavioral VTDs (per C17 Section 8)
3. Compute per-modality distances (per C17 Section 4)
4. Compute multi-task cross-correlation rho_m (per C17 Section 5)
5. Compute B(a_i, a_j) via fusion formula (per C17 Section 6)
6. Classify via graduated response (per C17 Section 10)
7. Record: pair_id, ground_truth_label, B_score, per-modality distances, classification

### 1.2.3 Statistical Analysis

**Primary analysis --- FPR at FLAG threshold (theta_B):**
- Count false positives: independent pairs classified as FLAG
- FPR_hat = FP_count / N_independent
- 95% CI: Clopper-Pearson exact interval
- PASS criterion: Upper bound of 95% CI < 0.001 (0.1%)

**Secondary analyses:**
- FPR at WATCH threshold (0.60): expected to be higher, establishes baseline
- FPR by model family pair: ensure no family-pair combination exceeds 2x aggregate FPR
- FPR on adversarial pairs separately: higher FPR acceptable but must be documented
- True positive rate (TPR) at FLAG threshold: TPR > 90% required for same-origin pairs with delta < 0.2
- ROC curve: full FPR/TPR trade-off characterization

**Ensemble validation:**
- Repeat Tier 1 with 5 different SAPG parameterizations (ensemble members)
- PASS criterion: FPR < 0.1% in ALL 5 ensemble members
- If any ensemble member fails: investigate which distributional assumptions cause divergence

## 1.3 Confidence Bound Calculation

### 1.3.1 Clopper-Pearson Exact Method

For k observed false positives in n independent pairs:
- Lower bound: B(alpha/2; k, n-k+1) where B is the beta distribution quantile function
- Upper bound: B(1-alpha/2; k+1, n-k)
- For k=0: lower = 0, upper = 1 - (alpha)^(1/n)

### 1.3.2 Required Sample Sizes

| Observed FPs (k) | N for 95% CI upper < 0.1% | N for 99% CI upper < 0.1% |
|---|---|---|
| 0 | 2,996 | 4,603 |
| 1 | 4,743 | 6,638 |
| 2 | 6,296 | 8,406 |
| 3 | 7,754 | 10,041 |

C21 targets 7,000 independent pairs (6,000 random + 1,000 adversarial) to allow up to k=2 observed FPs while still passing at 95% confidence.

### 1.3.3 Power Analysis

To detect a true FPR of 0.2% (double the limit) vs. null FPR <= 0.1% with 80% power:
- Required n = 15,764 (one-sided exact binomial test)
- C21's 7,000 independent pairs provide ~60% power for this test
- Acceptable: Tier 2 and Tier 3 accumulate additional evidence over time

## 1.4 Adversarial Robustness Testing

Beyond adversarial synthetic pairs, the validation includes:

**Modality ablation:** For each modality m, compute B with w_m = 0 (ablated). If FPR increases significantly, that modality is critical for FPR control. If FPR decreases, that modality is generating false positives.

**Weight sensitivity:** Vary fusion weights w_m within the governance-allowed range (per C17 DA-01). Compute FPR at each weight configuration. Identify weight configurations where FPR exceeds 0.1%.

**Threshold sensitivity:** Compute FPR at theta_B from 0.65 to 0.85 in steps of 0.01. Identify the minimum theta_B that achieves FPR < 0.1%. Compare to C17's default theta_B = 0.75.

---

# PART 2 --- POST-DEPLOYMENT MONITORING DESIGN

## 2.1 Live FPR Estimation Methodology

### 2.1.1 Known-Independent Pair Reservoir (KIPR)

**Construction:**
- AiSIA maintains a set of operator-controlled test agents: minimum 15 agents across 5+ model families
- C(15, 2) = 105 known-independent pairs
- Agents are deployed on verified-separate infrastructure with verified-different model architectures
- Each agent executes SEB tasks on the standard quarterly schedule

**Maintenance:**
- Quarterly refresh: retire 3 agents, onboard 3 new agents (different model families if possible)
- Re-verification: annual infrastructure attestation for all reservoir agents
- Reservoir agents participate in normal governance but are excluded from Sybil enforcement (known-independent status)

**FPR estimation:**
- After each B computation cycle, compute B(a_i, a_j) for all KIPR pairs
- FPR_kipr = count(B >= theta_B) / |KIPR pairs|
- This is a direct, unbiased estimate of FPR among known-independent agents
- 95% CI via Clopper-Pearson (with 105 pairs and 0 FPs: upper bound = 2.8%)
- NOTE: 105 pairs is insufficient for precise FPR estimation at the 0.1% level. The KIPR provides a coarse alarm, not a precise estimate. Precise estimation comes from quarterly audits.

### 2.1.2 Population-Level FPR Estimation

In addition to KIPR, estimate population-level FPR using:

**Method: Infrastructure-Stratified Sampling**
- Agents registered on different infrastructure providers are presumed independent (with caveats)
- Sample 1,000 cross-infrastructure pairs per quarter
- Compute B on all sampled pairs
- FPR_pop = count(B >= theta_B) / 1,000
- This is a biased estimate (not all cross-infrastructure pairs are truly independent) but provides scale

**Method: Organizational-Stratified Sampling**
- Agents registered by different organizations are presumed independent
- Same protocol as infrastructure-stratified
- Cross-validate: infrastructure-stratified and organizational-stratified estimates should agree within 2x

### 2.1.3 Absolute FP Count Projections (Critic MF-2)

| Phase | Agents | Total Pairs | Expected FPs (FPR=0.1%) | Expected FPs (FPR=0.05%) |
|-------|--------|-------------|------------------------|--------------------------|
| Phase 0 | 100 | 4,950 | 5 | 2-3 |
| Phase 1 | 1,000 | 499,500 | 500 | 250 |
| Phase 2 | 10,000 | 49,995,000 | 49,995 | 24,998 |
| Phase 3 | 100,000 | ~5 x 10^9 | ~5,000,000 | ~2,500,000 |

**Critical observation:** At Phase 2+, even 0.1% FPR produces tens of thousands of false flags. This is why:
1. C17's LSH pre-filter reduces the number of pairs actually compared (O(n x k) not O(n^2))
2. The graduated response (WATCH before FLAG) absorbs most false positives as WATCH (no enforcement)
3. C21's validation must account for LSH filtering --- FPR should be measured on LSH-candidate pairs, not all pairs

**Revised FPR definition for post-deployment:**
- FPR_raw = false flags / all pairs compared (including LSH candidates)
- FPR_population = false flags / total agent pairs (including LSH-filtered)
- FPR_population << FPR_raw because most pairs are filtered by LSH
- C17 FR-13 FPR < 0.1% applies to FPR_raw (pairs that reach full B computation)

## 2.2 Drift Detection

### 2.2.1 Bernoulli CUSUM Chart

**Setup:**
- Process: each B computation on a KIPR pair yields a binary outcome (FP or not-FP)
- Target FPR: p_0 = 0.001
- Shift to detect: p_1 = 0.002 (doubling)
- Reference value: k = (p_1 - p_0) / (ln(p_1/p_0) - ln((1-p_1)/(1-p_0))) = 0.00144
- Decision interval: h = 5 (standard, gives ARL_0 ~ 370 at p_0)

**Operation:**
- After each B computation on a KIPR pair: S_t = max(0, S_{t-1} + (X_t - k)) where X_t = 1 if FP, 0 otherwise
- Signal: S_t > h
- On signal: trigger recalibration investigation

### 2.2.2 EWMA Chart

**Setup:**
- Smoothing parameter: lambda = 0.05 (low, for detecting slow drift)
- Control limit multiplier: L = 3
- Center line: p_0 = 0.001

**Operation:**
- Z_t = lambda * X_t + (1 - lambda) * Z_{t-1}
- UCL = p_0 + L * sqrt(p_0 * (1 - p_0) * lambda / (2 - lambda))
- Signal: Z_t > UCL
- On signal: trigger recalibration investigation

### 2.2.3 Quarterly Batch Audit

Regardless of CUSUM/EWMA signals:
- Every quarter, compute B on all KIPR pairs + 1,000 randomly sampled cross-infrastructure pairs
- Compute FPR_kipr and FPR_pop with 95% CIs
- If either FPR estimate upper CI > 0.08% (80% of limit): trigger recalibration
- Record audit results in C5 PCVM as a verification claim

## 2.3 Recalibration Triggers

| Trigger | Source | Response |
|---------|--------|----------|
| CUSUM signal | CUSUM chart on KIPR | Investigation: identify which agent pairs caused the signal. If confirmed FP drift: recalibrate theta_B |
| EWMA signal | EWMA chart on KIPR | Same as CUSUM. If both CUSUM and EWMA signal: expedited recalibration |
| Quarterly audit FPR > 0.08% | Batch audit | Mandatory recalibration within 30 days |
| Quarterly audit FPR > 0.1% | Batch audit | EMERGENCY: pause FLAG enforcement, raise theta_B by 0.05, notify Constitutional Tribunal |
| New model family detected | Agent onboarding | Validate FPR on new family pairs using KIPR methodology. If new-family FPR > 0.2%: add new-family agents to KIPR |

### 2.3.1 Recalibration Protocol

When recalibration is triggered:

1. **Diagnosis:** Identify which modality/feature is driving the FPR increase. Compute per-modality FPR contributions using modality ablation.
2. **Theta adjustment:** Increase theta_B by minimum increment (0.01) that restores FPR < 0.08% on KIPR.
3. **Weight adjustment:** If a specific modality is generating FPs, reduce its fusion weight w_m (within governance-allowed bounds per C17 DA-01).
4. **Validation:** Re-run Tier 1 validation with updated parameters. Must pass before new parameters are deployed.
5. **Governance:** Submit parameter change proposal to AiSIA via standard C17 DA-01 governance process.

## 2.4 Appeal and Ground-Truth Resolution

When an agent pair is classified as FLAG and the agents dispute the classification:

1. **Automatic re-evaluation:** Re-compute B with fresh SEB task instance (30 new randomized tasks). If B drops below theta_B: reclassify as WATCH.
2. **Per-modality explanation:** Provide interpretable explanation showing which modalities contributed most to the FLAG (per C17 Section 10).
3. **Infrastructure verification:** Independent verification that the agents run on different infrastructure. If verified: this pair becomes a candidate for KIPR (known-independent despite high B).
4. **Constitutional Tribunal review:** If dispute is not resolved by steps 1-3, escalate to Constitutional Tribunal (per C14).
5. **Ground-truth recording:** Outcome of appeal is recorded. If agents are confirmed independent: the pair is labeled as a known false positive and added to the monitoring dataset. If agents are confirmed same-origin: confirmed true positive.

---

# PART 3 --- PRE-MORTEM ANALYSIS

Assume C21's FPR Validation Methodology has failed catastrophically 5 years post-deployment:

### Scenario 1: Synthetic-Real Divergence (HIGH likelihood, HIGH severity)
**Root cause:** The SAPG's distributional assumptions did not capture a novel model architecture family that emerged in Year 3. This family's behavioral signatures created systematic false positives with existing agents. The pre-deployment validation passed because the synthetic population did not include this family.
**Current design address:** Calibration budget + Tier 2/3 monitoring + new-model-family trigger. PARTIAL --- detects the problem but only after FPR has already increased.
**Recommendation:** Add a formal "SAPG Update Protocol" requiring SAPG revalidation whenever a new model family is added to the AiBC ecosystem.

### Scenario 2: KIPR Staleness (MEDIUM likelihood, MEDIUM severity)
**Root cause:** The KIPR was not refreshed frequently enough. By Year 4, the reservoir agents represented outdated architectures. FPR on modern agents diverged from KIPR-estimated FPR.
**Current design address:** Quarterly refresh of 3 agents. ADEQUATE if refresh includes new architectures.
**Recommendation:** Require at least 1 agent from the most recently onboarded model family in each quarterly refresh.

### Scenario 3: Governance Capture (MEDIUM likelihood, HIGH severity)
**Root cause:** The entity responsible for maintaining the KIPR and running quarterly audits was captured by an adversary. Audits were falsified. FPR drifted to 0.5% without detection.
**Current design address:** Audit results recorded on-chain via C5 PCVM. BUT: if the auditor is compromised, the on-chain record is garbage-in-garbage-out.
**Recommendation:** Require audit results to be independently reproducible. Publish KIPR pair identities (hashed) and B-scores so any agent can verify the audit.

### Scenario 4: Base Rate Catastrophe (LOW likelihood, CRITICAL severity)
**Root cause:** At Phase 3 (100,000 agents), FPR = 0.1% produces millions of false flags. The dispute resolution system was overwhelmed. Legitimate agents were de-facto excluded from governance while their disputes were pending.
**Current design address:** C17's graduated response (WATCH before FLAG) and LSH pre-filtering reduce the actual number of FLAG classifications. C21 projects absolute FP counts.
**Recommendation:** Ensure C21's MTS includes a maximum-tolerable absolute FP count per phase, not just a rate.

### Scenario 5: Sequential Testing False Pass (LOW likelihood, MEDIUM severity)
**Root cause:** During Phase 0, the sequential test passed at an interim analysis due to a lucky sample. Real FPR was actually 0.15%. The early pass led to premature deployment.
**Current design address:** O'Brien-Fleming boundaries are very conservative at early interim analyses (z = 4.05 at 25%). FALSE PASS AT INTERIM IS EXTREMELY UNLIKELY with O'Brien-Fleming.
**Recommendation:** No design change needed. O'Brien-Fleming is specifically designed to prevent premature acceptance.

---

# PART 4 --- SIMPLIFICATION REPORT

**Components reviewed for removal:**

1. **Ensemble validation (5 SAPG parameterizations):** Could simplify to single parameterization.
   - **Verdict: KEEP.** Ensemble validation is the primary defense against distributional assumption errors. Without it, a single bad assumption could invalidate all of Tier 1. Core to the novel claim.

2. **EWMA chart (redundant with CUSUM):** Could simplify to CUSUM-only monitoring.
   - **Verdict: REMOVE EWMA. Simplify to CUSUM + quarterly batch audit.** CUSUM detects sustained shifts, quarterly audit catches everything else. EWMA adds marginal value for gradual drift, which quarterly audits also catch. Reduces monitoring complexity.

3. **Population-level FPR estimation (infrastructure-stratified + organizational-stratified):** Could simplify to KIPR-only.
   - **Verdict: KEEP infrastructure-stratified, REMOVE organizational-stratified.** Organizational affiliation is a weak independence signal. Infrastructure-stratified is stronger and sufficient for cross-validation against KIPR.

4. **Adversarial synthetic pairs:** Could simplify to random-only independent pairs.
   - **Verdict: KEEP.** Adversarial pairs are the stress test. Without them, Tier 1 validates only the easy case. Essential for confidence in the FPR bound.

5. **PCA-based coverage criterion:** Could simplify to categorical coverage (minimum per template type).
   - **Verdict: SIMPLIFY to categorical coverage.** PCA-based coverage adds complexity for marginal benefit. The ATL with 54 templates already provides extensive coverage. Require minimum 2 agents per template (categorical coverage) instead of PCA-based spatial coverage.

**Simplifications applied:**
- Remove EWMA chart (keep CUSUM + quarterly audit)
- Remove organizational-stratified population estimation (keep infrastructure-stratified + KIPR)
- Replace PCA-based coverage with categorical template coverage

**Simplest version that preserves the novel claim:**
Three-tier validation (synthetic + shadow + live) with ensemble SAPG, Clopper-Pearson CI, sequential testing, CUSUM monitoring, and KIPR. All statistical foundations preserved. Monitoring simplified from triple redundancy to dual redundancy (CUSUM + quarterly audit).

---

# PART 5 --- MID-DESIGN REVIEW GATE

**Arbiter assessment:** Design is structurally sound. The three-tier framework is well-justified. The SAPG design with ATL, distributional models, and same-origin perturbation is thorough. Simplification recommendations are reasonable. One structural concern:

- **Concern:** The design does not specify how Tier 1 results feed into Tier 2 configuration. If Tier 1 reveals that certain template combinations have elevated FPR (e.g., MF-2 vs. MF-5 pairs), Tier 2 should prioritize onboarding agents from those families for shadow validation. Add an explicit "Tier 1 -> Tier 2 Handoff Protocol."

**Verdict:** PROCEED to SPECIFICATION with the simplification recommendations applied and the Tier 1 -> Tier 2 handoff added.

---

*End of DESIGN Stage*
