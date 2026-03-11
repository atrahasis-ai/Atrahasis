# C21 --- FPR Validation Methodology --- FEASIBILITY

**Invention ID:** C21
**Stage:** FEASIBILITY
**Date:** 2026-03-11
**Concept:** C21-A --- Phased Empirical Validation Framework (PEVF)

---

# PART 1 --- DOMAIN TRANSLATOR: SUB-PROBLEM ANALOGIES

## Sub-Problem 1: Generating realistic synthetic agents without real data

**Analogy: Weather Forecasting Ensemble Models (Meteorology)**
Climate scientists generate "synthetic weather" using General Circulation Models (GCMs) parameterized from physical laws --- not from historical data alone. Each GCM variant uses different parameterizations of sub-grid processes (cloud formation, convection, radiation) to produce ensemble members that span the space of plausible climates. The ensemble's spread represents structural uncertainty.

**Design insight:** The SAPG should generate agent populations as an "ensemble" --- multiple parameterizations of each modality, each representing a plausible but distinct behavioral profile. The spread of the ensemble represents the uncertainty about real agent behavioral diversity. Validation passes only if FPR < 0.1% holds across ALL ensemble parameterizations, not just the central estimate.

## Sub-Problem 2: Validating the validator (who checks the synthetic agents?)

**Analogy: Calibration Standards in Metrology (National Institute of Standards and Technology)**
NIST maintains primary measurement standards that calibrate secondary standards, which calibrate working instruments. The calibration chain is traceable to fundamental physical constants. When a new measurement technique is introduced, it must be validated against the existing calibration chain before it can be used operationally.

**Design insight:** The calibration budget (50-100 real pairs) is the "primary standard." Synthetic agents are the "secondary standard." The validation protocol requires that synthetic FPR and real FPR agree within a specified tolerance (calibration tolerance). If they diverge, the synthetic generator is recalibrated against the real data before proceeding. This creates a traceable calibration chain.

## Sub-Problem 3: Detecting FPR drift in a non-stationary population

**Analogy: Seismological Network Monitoring (Geophysics)**
Seismic networks continuously monitor ground motion. The background noise level (analogous to baseline FPR) changes over time due to weather, construction, and ocean waves. Seismologists use adaptive noise models that re-estimate background levels continuously, detecting earthquakes (FPR exceedances) as deviations from the adaptive baseline.

**Design insight:** Post-deployment FPR monitoring should use an adaptive baseline model. As the agent population changes (new architectures, new model families), the expected B-score distribution among independent pairs will shift. The monitoring system should re-estimate the baseline from the known-independent reservoir and detect FPR exceedances relative to the current baseline, not a fixed historical baseline.

---

# PART 2 --- ADVERSARIAL ANALYST REPORT (10 ATTACKS)

## Attack 1: Synthetic Population Bias
**Attack:** Adversary studies the SAPG parameters (if published or leaked) and designs agents whose behavioral profiles fall in under-represented regions of the synthetic population, where FPR calibration is weakest.
**Severity:** MEDIUM-HIGH
**Mitigation:** Coverage-guided generation ensures all regions are tested. But adversary may find gaps between coverage regions. Defense: continuous recalibration with real data (Tier 2/3) closes gaps over time.

## Attack 2: Distribution Mismatch Exploitation
**Attack:** The SAPG uses distributional assumptions (e.g., lognormal latency) that don't match a novel architecture's true distribution. Adversary deploys agents with unusual distributions that create false positives with legitimate agents.
**Severity:** MEDIUM
**Mitigation:** Calibration budget validates distributional assumptions. SAPG includes heavy-tailed and mixture distributions as adversarial variants. Tier 2/3 provide ongoing real-data correction.

## Attack 3: Ground Truth Poisoning (Tier 2)
**Attack:** During Phase 0 shadow deployment, adversary registers genuinely independent agents that are designed to appear same-origin (behavioral mimicry). These pairs are labeled as "independent" in ground truth but trigger false positives, artificially inflating the measured FPR and causing unnecessary theta_B increases.
**Severity:** MEDIUM
**Mitigation:** Ground truth establishment uses multiple independent signals (infrastructure attestation, organizational verification, model card). Adversary must fool all signals simultaneously.

## Attack 4: Known-Independent Reservoir Compromise (Tier 3)
**Attack:** Adversary compromises one or more agents in the known-independent reservoir, replacing them with same-origin clones. This corrupts the baseline FPR estimate.
**Severity:** MEDIUM-HIGH
**Mitigation:** Reservoir agents should be operator-controlled (AiSIA-operated test agents), not drawn from the general population. Periodic re-verification of reservoir agents.

## Attack 5: Threshold Gaming
**Attack:** Adversary creates Sybil agents whose B-scores fall just below theta_B (in the WATCH zone), avoiding FLAG classification while still being same-origin. If C21's validation only measures FPR at the FLAG threshold, the WATCH-zone evasion is undetected.
**Severity:** LOW (C17's graduated response already handles this --- WATCH triggers monitoring)
**Mitigation:** C21 should validate FPR at multiple thresholds, not just theta_B.

## Attack 6: Temporal Evasion of CUSUM
**Attack:** Adversary introduces false-positive-inducing agents in small bursts, below the CUSUM detection threshold. Over time, the cumulative FPR exceeds 0.1% but no single burst triggers the CUSUM alarm.
**Severity:** MEDIUM
**Mitigation:** Combine CUSUM (detects sustained shifts) with EWMA (detects gradual drift) and periodic batch audits (quarterly, catching cumulative effects). Triple redundancy in monitoring.

## Attack 7: Calibration Budget Manipulation
**Attack:** During the calibration phase (50-100 real pairs), adversary ensures the available real pairs are unrepresentative of the broader population, causing the synthetic generator to be miscalibrated.
**Severity:** LOW-MEDIUM
**Mitigation:** Calibration pairs should be selected by the system operator, not self-selected by agents. Use stratified sampling across model families.

## Attack 8: Feature Space Dimensionality Attack
**Attack:** Adversary creates agents with behavioral profiles that are indistinguishable in the PCA-reduced space (5-8 dimensions) but distinct in the full 27-dimensional space. This exploits the information loss from dimensionality reduction in the coverage criterion.
**Severity:** LOW
**Mitigation:** PCA-based coverage is for the synthetic generation phase only (ensuring diversity). The actual B(a_i,a_j) computation uses all 27 dimensions. This attack affects coverage validation, not FPR measurement.

## Attack 9: Sequential Testing Exploitation
**Attack:** Adversary front-loads benign behavior during Phase 0, passing interim analyses (which are conservative under O'Brien-Fleming). Then switches to Sybil behavior after final analysis passes.
**Severity:** MEDIUM
**Mitigation:** Tier 3 live monitoring catches post-validation behavioral changes. Validation is not a one-time gate --- it is the first layer of continuous assurance.

## Attack 10: Regulatory Capture of Validation Authority
**Attack:** Adversary gains influence over the Validation Monitoring Authority (VMA), causing it to relax validation standards, accept insufficient evidence, or delay response to FPR exceedances.
**Severity:** MEDIUM-HIGH
**Mitigation:** VMA decisions are recorded on-chain (via C5 PCVM). Validation criteria are constitutional parameters (immutable). VMA can adjust operational parameters but cannot change FPR_hard_limit.

**Adversarial Summary:** 0 attacks are fatal. 2 are MEDIUM-HIGH (reservoir compromise, regulatory capture). 4 are MEDIUM. 4 are LOW or LOW-MEDIUM. The three-tier structure provides defense-in-depth: Tier 1 failures are caught by Tier 2, Tier 2 failures are caught by Tier 3, and constitutional parameters bound the worst case. The primary residual risk is that ALL tiers share a dependency on the FPR_hard_limit being correctly set (if 0.1% is too permissive or too restrictive, all tiers calibrate to the wrong target).

---

# PART 3 --- COMMERCIAL VIABILITY (Early Assessment)

**Cost:** C21 is a validation methodology, not a deployed system. Costs are:
- Synthetic agent generation: one-time compute cost ~$500-$2,000 (generating 10,000+ agent profiles)
- Tier 1 validation: one-time compute cost ~$100-$500 (running B on all pairs)
- Tier 2 shadow monitoring: incremental cost folded into Phase 0 operations
- Tier 3 live monitoring: ongoing but lightweight (~100 reservoir pairs, quarterly audits)
- Total: <$5,000 for initial validation, <$1,000/quarter for ongoing monitoring
- **Verdict:** Negligible cost. Not a commercial barrier.

**Value:** C21 resolves C17 MF-1 (P0 monitoring flag). Without FPR validation, C17 cannot deploy, MCSD Layer 2 is non-functional, and Phase 1 Citicate issuance is blocked. C21 is on the critical path.

---

# PART 4 --- FEASIBILITY VERDICT

## Refined Concept Summary

**C21-A+ (Phased Empirical Validation Framework with Ensemble Generation and Adaptive Monitoring):**

1. **Tier 1 --- Pre-Deployment Synthetic Validation:**
   - Synthetic Agent Population Generator (SAPG) with ensemble parameterization across 5 modalities
   - Minimum 10,000 independent pairs (142+ agents from 30+ distinct type configurations)
   - Coverage-guided diversity via PCA-reduced space with Latin Hypercube Sampling
   - Adversarial synthetic agents designed to stress FPR boundaries
   - Clopper-Pearson exact 95% CI; pass criterion: upper bound < 0.1%
   - Multi-threshold validation (not just theta_B)

2. **Tier 2 --- Shadow Validation (Phase 0):**
   - Sequential testing with O'Brien-Fleming alpha-spending, 4 interim analyses
   - Ground truth via infrastructure attestation + organizational verification + model card
   - Calibration budget: 50-100 real pairs to validate synthetic-vs-real FPR
   - Calibration tolerance: synthetic FPR estimate within 2x of real FPR estimate
   - Batch-aware arrival handling

3. **Tier 3 --- Live Monitoring (Post-Deployment):**
   - Known-independent reservoir: minimum 100 operator-controlled pairs, refreshed quarterly
   - Dual detection: Bernoulli CUSUM + EWMA with redundant parameterization
   - Adaptive baseline re-estimation from reservoir
   - Quarterly batch audit: full recomputation of FPR on reservoir + random sample
   - Recalibration trigger: CUSUM/EWMA signal OR quarterly FPR > 0.08%
   - Recalibration mechanism: theta_B increase (more conservative)

**Scores:**
- Novelty: 3/5 (novel combination --- synthetic agent ensemble generation for FPR validation is not found in prior art)
- Feasibility: 4/5 (all components use established statistical methods; synthetic generation feasible for 4/5 modalities)
- Impact: 4/5 (resolves C17 MF-1, unblocks Phase 1)
- Risk: 3/10 (LOW-MEDIUM --- primary risk is synthetic validity, mitigated by calibration budget)

```json
{
  "type": "ASSESSMENT_COUNCIL_VERDICT",
  "invention_id": "C21",
  "stage": "FEASIBILITY",
  "decision": "ADVANCE",
  "novelty_score": 3,
  "feasibility_score": 4,
  "impact_score": 4,
  "risk_score": 3,
  "risk_level": "LOW-MEDIUM",
  "required_actions": [],
  "monitoring_flags": [
    "MF-1: Structural modality distributional assumptions are the weakest link in synthetic generation. Design must include explicit uncertainty bounds for this modality.",
    "MF-2: Absolute FP count projections must appear in MASTER_TECH_SPEC (Critic dissent from IDEATION)."
  ],
  "operational_conditions": [],
  "pivot_direction": null,
  "rationale": "C21-A+ is a well-grounded validation methodology combining established statistical techniques (Clopper-Pearson, sequential testing, CUSUM) with a novel synthetic agent population generator calibrated by real-data comparison. All components are feasible with current technology. The primary risk (synthetic validity) is explicitly mitigated by the calibration budget. No architectural or scientific blockers. ADVANCE to DESIGN."
}
```

---

*End of FEASIBILITY Stage*
