# C35 Assumption Validation Report — Science Advisor Reconciliation

**Stage:** RESEARCH → FEASIBILITY gate
**Invention:** C35 — Seismographic Sentinel with PCM-Augmented Tier 2
**Role:** Science Advisor (Reconciliation per §6 Step 11)
**Date:** 2026-03-12

---

## Purpose

This report maps each Ideation Council assumption to corresponding research findings (Prior Art Report, Landscape Report, Science Assessment), flagging contradictions and validating or invalidating each assumption.

---

## Assumption Mapping

### A-1: STA/LTA is applicable to agent behavioral monitoring

**Ideation assumption:** STA/LTA ratio trigger from seismology can be adapted to per-agent metric streams (verification latency, acceptance rate, committee frequency, behavioral consistency).

**Research findings:**
- **Prior Art (PA-05, PA-06):** STA/LTA is mature seismology technique (Allen 1978; Withers et al. 1998). No prior application to multi-agent verification security found. Cross-domain transfer is novel.
- **Science Assessment (SA-1):** PARTIALLY_SOUND. The core STA/LTA mechanism transfers cleanly — both seismic signals and agent metrics are noisy time series where detecting transient deviations from background is the goal. The detection theory (Neyman-Pearson framework) applies directly.
- **Concern:** Agent behavioral metrics may have heavier tails and more non-stationarity than seismic signals. STA/LTA assumes approximately stationary background, which degrades under distributional shift.

**Verdict:** VALIDATED WITH CAVEAT. The transfer is sound in principle. The dual-baseline scheme (fixed + adaptive) partially addresses non-stationarity but has an **unresolved decision fusion problem** — how to combine the two baselines' outputs when they disagree. This must be resolved at FEASIBILITY.

---

### A-2: Fixed + adaptive dual baselines prevent boiling-frog evasion

**Ideation assumption:** Running fixed baseline in parallel with adaptive STA/LTA prevents slow-ramp evasion where adversary gradually shifts behavior until the adaptive baseline accommodates the anomaly.

**Research findings:**
- **Science Assessment (SA-1):** The fixed baseline catches what the adaptive misses (slow ramp), and the adaptive catches what the fixed misses (legitimate drift). But the **fusion rule is unspecified** — OR (either triggers) maximizes recall but increases false positives; AND minimizes false positives but misses evasions visible to only one baseline.
- **Prior Art:** No direct precedent for dual-baseline parallel STA/LTA. Standard seismology uses single adaptive baseline.
- **Monitoring Flag MF-4 (fixed-baseline reconstructibility):** Science Assessment confirms this is a real concern — if adversary can observe system behavior during calibration window, they can infer the fixed baseline parameters.

**Verdict:** PARTIALLY VALIDATED. The concept is sound but the decision fusion rule is formally unresolved. MF-4 (fixed baseline reconstructibility by adversary) remains an **open risk** requiring Red Team evaluation at FEASIBILITY.

---

### A-3: PCM computes expected correlation from structural covariates

**Ideation assumption:** E[corr(a_i, a_j)] = Σ_k f_k(structural_overlap_k) provides a principled model of expected inter-agent correlation, and residuals R = observed - expected reliably isolate genuine anomalies from structurally-explained similarity.

**Research findings:**
- **Prior Art (PA-03, PA-04):** Configuration-model residual networks (Newman 2010) and covariate-adjusted association networks (Ovaskainen et al. 2017, ecology) are methodological predecessors. They validate the approach of removing structural expectations from observed associations. However, neither operates in adversarial settings with streaming updates.
- **Science Assessment (SA-2):** PARTIALLY_SOUND. The linear additive form assumes covariate independence — i.e., that the contribution of parcel overlap to expected correlation is independent of committee co-assignment contribution. This is **unlikely to hold** (agents on the same parcel AND same committee interact more than additive). Interaction terms are needed.
- **Landscape:** PCM concept has NO direct precedent in multi-agent security. This is confirmed as the most novel component.

**Verdict:** PARTIALLY VALIDATED. The core approach (residual = observed - structural expectation) is well-grounded in prior art. The specific linear additive form needs revision — **interaction terms between covariates are needed**, or a non-linear model (e.g., log-linear as in ecology). This is addressable but changes the computational complexity.

---

### A-4: PCM calibration converges within reasonable time

**Ideation assumption (IC-1, carried via merge):** PCM calibration period of ~1000 epochs provides reliable structural estimates.

**Research findings:**
- **Science Assessment (SA-2):** The convergence rate depends on the number of structural covariates and the rate at which agent pairs co-occur in different structural configurations. With 5 covariates and ~1000 agents, each agent pair needs to be observed under multiple structural configurations for reliable estimation.
- **Monitoring Flag MF-2:** The Science Assessment does NOT provide a definitive convergence bound. The proposed experiment (EXP-3 simulation) is needed to validate.
- **Prior Art:** Ecological covariate-adjusted networks (Ovaskainen et al.) typically need hundreds of observation periods for stable estimates. In AAS, 1 observation period = 1 SETTLEMENT_TICK (60s), so 1000 epochs = ~16.7 hours. This is plausible for initial calibration.

**Verdict:** PLAUSIBLE BUT UNVALIDATED. The 1000-epoch estimate is reasonable by analogy to ecological networks, but no formal convergence proof exists. **EXP-3 simulation is BLOCKING for FEASIBILITY advancement.**

---

### A-5: Spectral clustering effectively partitions agent neighborhoods

**Ideation assumption:** Spectral clustering at each CONSOLIDATION_CYCLE creates meaningful agent neighborhoods for Tier 2 regional correlation analysis, with cap at 2*log(V) and split-on-overflow.

**Research findings:**
- **Science Assessment (SA-3):** CONDITIONALLY_SOUND. Spectral clustering is appropriate for the non-adversarial case. However, it is **vulnerable to specific adversarial graph perturbations** — an attacker who controls O(√V) edges can significantly alter cluster boundaries (Bojchevski & Gunnemann, 2019). The 2*log(V) cap mitigates concentration attacks but does not address boundary manipulation.
- **Prior Art:** Spectral clustering is standard (Ng et al. 2001). Adversarial robustness of spectral clustering is an active research area.
- **Landscape:** Robust spectral methods exist (certified robustness, Zugner et al. 2020) but add computational cost.

**Verdict:** CONDITIONALLY VALIDATED. Works in non-adversarial settings. Under adversarial conditions, cluster boundary manipulation is a real attack vector. Mitigation options: (a) robust spectral methods, (b) randomized perturbation of clustering input, (c) detection of adversarial graph modification. Must be addressed at FEASIBILITY.

---

### A-6: 4-channel quorum (≥3 of 4) is effective for confirmation

**Ideation assumption:** Requiring ≥3 of 4 channels (verification, behavioral, infrastructure, economic) to register anomalous provides robust confirmation with low false positive rate.

**Research findings:**
- **Science Assessment (SA-4):** PARTIALLY_SOUND. The 3-of-4 threshold is reasonable as a heuristic. However, it is **not statistically optimal under channel correlation** — if channels are correlated (e.g., verification anomaly implies behavioral anomaly), then 3-of-4 does not provide the independence-based reduction in false positive rate that the design assumes. A weighted fusion (e.g., Bayesian network over channels with learned conditional dependencies) would be more principled.
- **Prior Art:** Multi-sensor fusion is well-studied. Dempster-Shafer theory and Bayesian fusion provide formal frameworks. Fixed k-of-n voting is used in safety-critical systems (IEC 61508 2oo3 voting) but those assume independent channels.
- **Landscape:** No system uses 4-channel quorum for multi-agent anomaly detection specifically.

**Verdict:** PARTIALLY VALIDATED. The heuristic is acceptable as a starting point but should be replaced with principled multi-channel fusion at DESIGN. The 3-of-4 can serve as a simplified fallback. Channel correlation analysis is needed.

---

### A-7: Epidemiological backward tracing identifies causal sources

**Ideation assumption:** Overdispersion analysis from confirmed Tier 2 anomalies can trace backward to identify common operator-agent mappings or infrastructure causes.

**Research findings:**
- **Science Assessment (SA-5):** SOUND WITH CAVEATS. Overdispersion analysis is valid epidemiological methodology (Cameron & Trivedi, 1998). The concern is **sample size** — at the stated 1K-100K scale with "rare" Tier 3 invocations, there may be insufficient confirmed anomalies to achieve statistical power for overdispersion detection. Need ≥30 confirmed anomalies per analysis window.
- **Prior Art:** Contact tracing and overdispersion analysis are standard epidemiology. R₀ estimation and superspreader identification are well-established. No application to multi-agent digital systems found.
- **Landscape:** Novel cross-domain application. The epidemiological framing is a genuine contribution.

**Verdict:** VALIDATED WITH SAMPLE SIZE CAVEAT. The methodology is sound. The practical concern is that Tier 3 may not fire often enough to accumulate sufficient sample sizes. Mitigation: lower the Tier 3 activation threshold, or use synthetic/simulated anomalies for calibration.

---

### A-8: Scaling is O(V) Tier 1, O(V log V) amortized Tier 2

**Ideation assumption:** The pipeline scales to 1K-100K agents with stated complexity bounds.

**Research findings:**
- **Science Assessment (SA-6):** SOUND EXCEPT for a **hidden near-quadratic term in PCM precomputation**. PCM must compute E[corr] for all agent pairs within each neighborhood. With neighborhoods of size 2*log(V), the per-neighborhood cost is O(log²V), and with V/log(V) neighborhoods, the total is O(V log V). BUT the structural covariate matrix itself must be recomputed at each CONSOLIDATION_CYCLE, and if covariates reference global state (e.g., committee assignments across all agents), this becomes O(V²) in the worst case.
- **Mitigation:** Restrict PCM to within-neighborhood pairs only (not all pairs globally). Use sparse data structures for structural covariate matrix.

**Verdict:** CONDITIONALLY VALIDATED. Tier 1 O(V) is clean. Tier 2 O(V log V) holds if PCM is restricted to within-neighborhood computation. The global covariate matrix must be sparse or precomputed incrementally. This is a design constraint, not a fundamental blocker.

---

### A-9: Cross-layer integration with C3, C5, C6, C7, C8, C12, C17 is feasible

**Ideation assumption:** C35 can integrate with 7 existing specifications through cluster membership API and cross-layer contracts.

**Research findings:**
- **Science Assessment (SA-8 / integration section):** SOUND. The integration points are well-defined:
  - C17 provides B(a_i, a_j) behavioral similarity → Tier 1/2 input
  - C12 AVAP provides confirmed edges → pre-confirmed Tier 2 triggers
  - C9 defines temporal hierarchy → epoch alignment
  - C3 provides scheduling data → STA/LTA inputs
  - C5 provides verification outcomes → primary Tier 1 metric
  - C8 provides settlement data → economic channel for Tier 2
- **No contradictions found.** Integration coherence rated 3.5/5 by Science Advisor.
- **Landscape:** C35 uniquely benefits from AAS's existing authority hierarchy (C9) and pre-existing behavioral fingerprinting (C17). No comparable integration opportunity exists in any surveyed system.

**Verdict:** VALIDATED. Integration is architecturally coherent. Complexity is high (7 cross-layer contracts) but manageable within C9 framework.

---

## Monitoring Flag Status

| Flag | Status | Research Outcome |
|------|--------|-----------------|
| MF-1: Quorum integration sufficiency | OPEN | SA-4 raises concerns about statistical optimality of 3-of-4 under correlation. Revisiting IC-3 adaptive topology not yet warranted but flag remains active. |
| MF-2: PCM convergence bounds | OPEN | No formal proof. SA-2 establishes plausibility by analogy. EXP-3 simulation required for validation. |
| MF-3: Composition novelty sufficiency | RESOLVED | Prior Art Report confirms HIGH composite novelty. PCM is genuinely novel (no direct precedent). Composition of 6 innovations is unprecedented. Novelty revised upward to 3.5-4.0. |
| MF-4: Fixed-baseline reconstructibility | OPEN | SA-1 confirms this is a real risk. Red Team evaluation at FEASIBILITY required. |

---

## Contradictions Found

### Contradiction C-1: Linear additive PCM vs. covariate dependence
- **Ideation assumed:** Linear additive model Σ_k f_k(overlap_k)
- **Research found:** Covariates are likely dependent; interaction terms needed
- **Impact:** MEDIUM — changes PCM computational model, may increase complexity
- **Resolution:** Accept non-linear model at FEASIBILITY. Log-linear or kernel-based alternatives exist.

### Contradiction C-2: Channel independence for quorum
- **Ideation assumed:** 4 channels are sufficiently independent that 3-of-4 provides robust confirmation
- **Research found:** Channels are likely correlated (verification ↔ behavioral especially)
- **Impact:** MEDIUM — reduces effective diversity of the quorum
- **Resolution:** Model channel correlations explicitly. Consider weighted fusion instead of simple voting.

### Contradiction C-3: STA/LTA dual-baseline fusion
- **Ideation assumed:** Running fixed + adaptive in parallel with trigger-on-either is sufficient
- **Research found:** Decision fusion rule is formally unspecified; OR/AND have different trade-off profiles
- **Impact:** LOW-MEDIUM — design gap, not a fundamental flaw
- **Resolution:** Specify fusion rule at DESIGN based on desired FAR/FRR operating point.

### No Fatal Contradictions Found
All contradictions are addressable. None invalidates the core architecture.

---

## Summary Verdict

**RESEARCH SURVIVES.** C35's core architecture (three-tier hierarchical detection with PCM-augmented Tier 2) is validated by research with addressable modifications:

1. PCM needs non-linear extension (interaction terms) — validated approach, increased complexity
2. Quorum needs correlation-aware fusion — well-studied alternatives available
3. Dual-baseline fusion rule needs formal specification — design-stage task
4. Spectral clustering needs adversarial hardening — active research, mitigations exist
5. Tier 3 sample size concern — mitigable by threshold adjustment

**Novelty confirmed:** 3.5-4.0 (revised upward from IC-2's 3.0 due to PCM novelty and composition uniqueness)
**Feasibility confirmed:** 3.5-4.0 (revised slightly downward from IC-2's 4.5 due to PCM complexity increase and unresolved fusion problems)

**Recommendation:** ADVANCE to FEASIBILITY.
