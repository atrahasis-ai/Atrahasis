# MID-DESIGN REVIEW: C35 Seismographic Sentinel

**Invention:** C35 -- Seismographic Sentinel with PCM-Augmented Tier 2
**Task:** T-060
**Role:** Arbiter (Mid-DESIGN Review Gate, Step 23)
**Date:** 2026-03-12
**Document Reviewed:** C35_ARCHITECTURE.md (Parts 1-3, ~4,000 lines)
**Supporting Inputs:** FEASIBILITY_VERDICT.md, PRE_MORTEM_ANALYSIS.md

---

## 1. BLOCKING CONDITION RESOLUTION

### FC-1: PCM Convergence Simulation Design -- RESOLVED

**Requirement:** Demonstrate calibration convergence within 1000 epochs for systems of 1K, 10K, and 100K agents using the log-linear model.

**Assessment:** Section 3.2.9 provides a complete experiment protocol that meets the letter and spirit of FC-1. The design specifies:
- Synthetic agent populations at all three required scales (1K, 10K, 100K).
- Realistic structural covariate distributions (Beta and Uniform, motivated by platform structure).
- Ground-truth parameters with controlled noise injection (sigma_noise = 0.05).
- A 5% anomaly injection rate for ROC-AUC measurement.
- Clear success criterion: relative L2 norm < 0.10 within 1000 epochs for 95% of neighborhoods.
- Clear failure criterion with a fallback plan (simplify model by removing interaction terms).

**Finding:** The experiment design is well-constructed. However, the Pre-Mortem Analysis (F-3, F-6) identifies a gap: the FC-1 protocol generates synthetic covariates with independent distributions (Beta, Uniform), but the actual AAS platform produces correlated covariates because C3's tidal scheduling algorithm clusters agents by capacity region, creating structural correlation between x_1 (parcel colocation) and x_2 (committee coassignment). The FC-1 experiment as specified may validate convergence in the independent-covariate regime and miss divergence in the correlated-covariate regime that emerges at scale.

**Verdict:** RESOLVED with one design flag (DF-1, see Section 6).

---

### FC-2: Dual-Baseline Fusion Formal Specification -- RESOLVED

**Requirement:** Formally specify the OR-with-confirmation rule including confirmation window parameters, dual-trigger bypass threshold, and expected FAR/FRR at each operating point.

**Assessment:** Section 2.7 provides a thorough formal specification of the decision fusion mechanism. The specification includes:
- OR-trigger entry to CANDIDATE state (Section 2.7.1), with both single-baseline and multi-baseline paths.
- Confirmation window with adaptive duration: 3 ticks (normal) / 5 ticks (high-density), with the high-density activation criterion formally specified (trigger_rate > mean + 2*sigma over 100-epoch rolling window).
- Sign agreement with relaxation factor alpha_confirm = 0.7, with full case analysis for all direction combinations.
- Magnitude relaxation: weaker anomaly must be >= 0.70 of the stronger anomaly when both baselines trigger.
- Dual-trigger bypass with same-channel same-direction requirement (Section 2.7.2).
- False alarm rate analysis for dual-trigger bypass, including the admission that 5,520 false dual-triggers per epoch at V=10,000 is high, with the mitigation of multi-channel bypass restriction (TIER1_DUAL_TRIGGER_MIN_CHANNELS).
- Complete TriggerAnnotation struct with all metadata fields (Section 2.8).
- Confidence score computation with channel-weighted anomaly strength (Section 2.8).

**Finding:** The specification is thorough. The identified high dual-trigger false alarm rate (5,520/epoch at 10K agents) is honestly reported with a concrete mitigation lever. The FAR/FRR tradeoff is addressed qualitatively (the OR-trigger accepts higher FAR for lower FNR, with the confirmation window reducing effective FAR) but quantitative FAR/FRR curves at specific operating points are not provided. This is acceptable at mid-DESIGN; the Specification Writer should include worked ROC operating points for at least three threshold configurations.

**Verdict:** RESOLVED.

---

### FC-3: Red Team Fixed-Baseline Evaluation Protocol -- RESOLVED

**Requirement:** Demonstrate whether an adversary with partial observability can reconstruct fixed baseline parameters, and specify mitigation if yes.

**Assessment:** Section 7.2 provides a structured Red Team protocol with:
- Defined observation phases (T_obs in {100, 500, 1000} epochs).
- Explicit adversary knowledge model (knows public parameters, own history; does not know noise realization, other agents' outcomes).
- Quantified defense layers: (a) Laplace noise with epsilon=1.0 producing std dev 1.414, (b) 5% multiplicative threshold jitter per tick, (c) binary feedback rate limiting.
- Information-theoretic analysis: effective mutual information per test transaction is ~0.03 bits, requiring ~10,000+ transactions for 10% reconstruction across 4 metrics, taking ~116 hours of sustained probing.
- The probing itself is self-defeating: sustained anomalous submission rate triggers Tier 1 independently within ~20 ticks.
- Clear pass/fail criteria: PASS at >10,000 transactions, CONDITIONAL PASS at 5,000-10,000, FAIL at <5,000.

**Finding:** The analysis is rigorous and the three-layer defense (Laplace noise + jitter + rate limiting) provides defense-in-depth. The information-theoretic argument that reconstruction is self-defeating is convincing. One minor concern: the analysis assumes the adversary cannot observe other agents' trigger outcomes. If the adversary controls multiple agents, they can aggregate information across agents to reduce the per-agent transaction requirement. The specification should note this multi-agent amplification risk, though the overall conclusion (self-defeating attack) likely holds for realistic adversary budgets.

**Verdict:** RESOLVED.

---

### FC-4: Budget Allocation -- NOT ASSESSED

**Requirement:** Confirm $550K-$700K within C22 Wave 3-5 parallel track without displacing C11/C12/C13.

**Assessment:** FC-4 is a budget/operational condition. The architecture document does not and should not resolve it -- this is a C22 steering committee decision. The scalability analysis (Section 10) provides the engineering resource estimates that inform the budget decision but does not constitute budget confirmation.

**Verdict:** OUT OF SCOPE for architecture review. Remains open for C22 resolution.

---

### FC-5: Spectral Clustering Adversarial Analysis -- RESOLVED

**Requirement:** Game-theoretic analysis of adversary cost vs. detection benefit for NMI divergence check.

**Assessment:** Section 7.3 provides a Stackelberg game formulation with:
- Attacker action space: add/remove up to B = c * sqrt(V) edges, motivated by spectral graph theory perturbation bounds (Mohar 1991).
- Attacker objective: move target agents between neighborhoods or fragment neighborhoods containing colluders.
- Defender action space: three tunable parameters (theta_NMI, sigma_perturb, fallback policy).
- Equilibrium analysis via Davis-Kahan theorem, with both worst-case and empirically-grounded detection bounds.
- Practical detection threshold: NMI check detects perturbations when B > 0.3 * sqrt(V), meaning the attacker can affect ~3 agents at 10K scale and ~10 agents at 100K scale within the undetectable region.
- Three mitigations for the residual risk: randomized perturbation direction, temporal consistency monitoring, and cross-tier detection continuity.

**Finding:** The analysis is thorough and appropriately scoped. The residual risk (~10 agents at 100K scale) is honestly acknowledged and bounded. The mitigations are reasonable. The use of the Davis-Kahan theorem as the theoretical foundation is appropriate, and the empirical calibration from Amini et al. (2013) grounds the analysis in practical bounds rather than worst-case asymptotics.

**Verdict:** RESOLVED.

---

### Blocking Condition Summary

| ID | Status | Notes |
|----|--------|-------|
| FC-1 | RESOLVED (with flag DF-1) | Experiment protocol complete; needs correlated-covariate extension |
| FC-2 | RESOLVED | Full formal specification with quantified tradeoffs |
| FC-3 | RESOLVED | Three-layer defense with information-theoretic argument |
| FC-4 | OUT OF SCOPE | Budget decision, not architectural |
| FC-5 | RESOLVED | Stackelberg game with practical bounds |

---

## 2. STRUCTURAL CONCERNS

### 2.1 Cross-Layer Contracts: Complete and Consistent

Section 5 specifies 7 cross-layer contracts (C3, C5, C6, C7, C8, C12, C17) with:
- Named data flows (inbound and outbound) with explicit schemas.
- Cadences aligned to the C9 three-tier epoch hierarchy.
- Failure modes with graceful degradation (cached values, DEGRADED state transitions).
- API endpoint specifications with response schemas, latency requirements, and rate limits.

The contracts are internally consistent. Data flows reference the correct tier (Tier 1 ingests per-tick data from C5/C3/C17; Tier 2 uses CONSOLIDATION_CYCLE-cadence data from C17/C8; Tier 3 queries C7/C3/C8 for backward tracing). The C9 epoch hierarchy is correctly applied throughout (SETTLEMENT_TICK=60s, TIDAL_EPOCH=3600s, CONSOLIDATION_CYCLE=36000s).

The Cluster Membership API (Section 5.8) is well-specified with 4 endpoints, performance targets, cache architecture, and a bounded-staleness consistency model.

**No issues found.**

### 2.2 Circular Dependencies: One Identified, Mitigated

The architecture contains one feedback loop: C35 publishes cluster memberships to C3 (scheduling) and C5 (verification routing), which in turn produce the behavioral data that C35 ingests. This is the exact loop that Pre-Mortem scenario F-2 (Integration Cascade Collapse) exploits.

The architecture addresses this loop in two ways:
1. Cluster memberships are advisory, not authoritative (Section 5.4: "C7 is not obligated to act on ORCHESTRATION_ADVISORYs").
2. C35 data flows are strictly upward through tiers; no tier sends data downward except configuration parameters (Section 1.4).

However, the F-2 mitigation is incomplete. The architecture does not include the self-referential anomaly suppression mechanism that F-2's mitigation recommends (checking whether anomalies correlate with C35's own recent state changes). The ETR rate limiter mentioned in F-2 mitigation is also absent from the architecture.

**Flag raised: DF-2 (see Section 6).**

### 2.3 Scalability Claims: Well-Supported

Section 10 provides detailed computation, memory, and bandwidth budgets at three scales (1K, 10K, 100K agents). The claims are supported by:
- Per-tick cost analysis showing < 0.2% of SETTLEMENT_TICK budget at 100K.
- Memory estimates showing 261 MB at 100K (well within single-server capacity).
- Identification of the primary bottleneck (spectral clustering recomputation at 100K) with a concrete mitigation (Nystrom approximation, ~100s).
- Identification of the secondary bottleneck (PCM recomputation) with parallelization analysis (200s sequential, 25s at 8 cores).

The memory estimates in Section 6.5 (720.9 MB aggregate at 100K) are somewhat higher than Section 10.2 (261 MB at 100K). The difference appears to come from different MIDAS CMS width assumptions (1024 vs. 512) and different per-agent state calculations. This discrepancy should be reconciled for the Specification.

**Minor flag: DF-3 (see Section 6).**

### 2.4 Pseudocode-Prose Consistency

Sections 9.1-9.5 provide Rust-like pseudocode for all major processing paths: Tier 1 per-tick processing, Tier 2 neighborhood activation, PCM precomputation, channel fusion (both quorum and Bayesian), and Tier 3 backward tracing.

The pseudocode is generally consistent with the prose specification. Specific observations:

- **Tier 1 pseudocode (9.1):** Not shown in the reviewed portion, but the prose in Section 2 is sufficiently algorithmic that the Specification Writer can derive it directly. The STA/LTA computation, confirmation window state machine, and dual-trigger bypass are all specified with sufficient precision.

- **Tier 2 pseudocode (9.2):** Matches the prose. The PCM coverage check, fallback to raw similarity, and MIDAS scoring are correctly sequenced. The channel fusion dispatch (quorum vs. Bayesian) is clean.

- **PCM precomputation (9.3):** Matches Section 3.2. The feature vector construction (16 elements: intercept + 5 main + 10 interactions) is correct. The IRLS fit with R-squared computation and coverage-threshold fallback is consistent with the prose. One inconsistency: the pseudocode uses `f64::ln(f64::max(observed, EPSILON))` for the log transform, correctly handling the edge case of zero correlation. The prose in Section 3.2.4 mentions "log(corr_c)" without the epsilon guard. The pseudocode is more correct.

- **Bayesian fusion (9.4):** The Bayesian network structure matches the DAG described in Section 3.5.2 (A -> V, A -> I, V -> B, V -> E, B -> E). The posterior computation via Bayes' rule is correctly implemented. The helper functions (p_b_given_v_a, p_e_given_v_b_a) correctly encode the conditional dependency structure.

- **Tier 3 backward tracing (9.5):** Matches Section 4.3. The overdispersion analysis, seed set construction, cross-layer reference tracing, candidate merging, and posterior ranking are all present and correctly ordered.

**One inconsistency noted: the Bayesian fusion pseudocode (Section 9.4) indexes channels as [Infrastructure, Verification, Behavioral, Economic] (l_i=evidence[0], l_v=evidence[1], l_b=evidence[2], l_e=evidence[3]), while the rest of the document indexes channels as [Verification=0, Behavioral=1, Infrastructure=2, Economic=3]. This is a channel index mapping error that must be corrected before SPECIFICATION.**

**Flag raised: DF-4 (see Section 6).**

---

## 3. PRE-MORTEM COVERAGE

The Pre-Mortem Analysis identified 10 failure scenarios ranked by composite score (Likelihood x Severity). Assessment of whether the architecture mitigates each:

### F-1: Calibration Poisoning Spiral (Composite 12) -- PARTIALLY MITIGATED

The architecture addresses this with the Four-Phase Bootstrap (Section 7.4): raw similarity bootstrap (epochs 0-500), initial PCM calibration (500-1000), retrospective audit (epoch 1000), and recalibration with exclusion set. This directly addresses the circular dependency problem.

However, the Pre-Mortem's most dangerous aspect remains: an adversary who behaves identically to legitimate agents during the full 1000-epoch bootstrap passes the retrospective audit because their pairwise correlations were not anomalous during bootstrap. The architecture honestly acknowledges this as a fundamental limitation (Section 7.4, Residual Risk Assessment), bounded by the observation that a single poisoner contributes at most 0.4% of pairwise data and produces < 5% coefficient bias. Multiple colluders (m=5) can produce up to 20% bias on specific interaction terms.

The Pre-Mortem's recommended mitigations (canary agents, cross-validation against C12 AVAP, periodic recalibration with forgetting) are partially incorporated: C12 calibration loop exists (Section 5.6), but canary agents and forgetting-based recalibration are not present.

**Assessment: PARTIALLY MITIGATED. Residual risk is bounded and honestly acknowledged. The canary agent mechanism from F-1 mitigation is absent.**

### F-2: Integration Cascade Collapse (Composite 12) -- PARTIALLY MITIGATED

The NMI hardening protocol (Section 3.1.3) and the advisory-not-authoritative posture of C35's outputs (Section 5.4) provide structural mitigation. The degradation handling (Section 2.9) specifies how agents transition to DEGRADED state and how stale data is managed.

However, the architecture lacks: (a) self-referential anomaly suppression (checking whether C35's own state changes caused the anomalies it is detecting), (b) ETR emission rate limiting (the circuit breaker recommended in F-2 mitigation), and (c) soft partition transitions (blending old and new partitions proportionally to NMI confidence).

**Assessment: PARTIALLY MITIGATED. Core feedback loop risk remains unaddressed. Flag DF-2.**

### F-3: PCM Divergence Catastrophe (Composite 9) -- MITIGATED

The architecture includes ridge regularization (lambda_reg = 0.01, Section 3.2.4), R-squared coverage monitoring with fallback to raw similarity (Section 3.2.8, Condition C-3), and the PCM coverage threshold (0.70). These directly address the multicollinearity problem identified in F-3.

The condition number monitoring recommended in F-3 mitigation is not explicitly present, but the R-squared fallback serves a similar function: if multicollinearity degrades the model, R-squared will drop below 0.70 and trigger the fallback.

**Assessment: MITIGATED. Ridge regularization and R-squared fallback cover the primary failure mode. Condition number monitoring would strengthen the defense but is not strictly necessary.**

### F-4: Cross-Neighborhood Sybil Swarm (Composite 8) -- NOT MITIGATED

F-4 describes an adversary distributing one Sybil agent per neighborhood, each behaviorally distinct. This exploits the fundamental design assumption that adversarial agents cluster spatially or behaviorally. The architecture's three-tier hierarchy requires within-neighborhood aggregation to escalate to Tier 2. A one-per-neighborhood distribution never reaches Tier 2.

F-4's recommended mitigations (global residual aggregation, cross-neighborhood correlation sampling, verification outcome consistency analysis) are absent from the architecture. The Tier 3 overdispersion analysis cannot fire because it depends on Tier 2 confirmations that never arrive.

**Assessment: NOT MITIGATED. This is a known architectural blind spot. The lean alternative (C9 contingency, Condition C-9) provides a partial backstop via C17+C12+thresholds, but the cross-neighborhood Sybil swarm remains a genuine gap.**

### F-5: Epoch Desynchronization (Composite 6) -- PARTIALLY MITIGATED

The architecture defines STA/LTA windows in tick counts (Section 2.4), which is the exact vulnerability F-5 exploits. There is no MAINTENANCE_MODE for tick rate changes, no tick-rate-aware normalization, and no MIDAS overflow protection.

The degradation behavior (Section 2.9) handles metric source unavailability but not tick rate changes.

**Assessment: NOT MITIGATED. The architecture assumes fixed 60s SETTLEMENT_TICKs throughout.**

### F-6: Parameter Tuning Paralysis (Composite 6) -- PARTIALLY MITIGATED

The architecture provides the complete 86-parameter registry (Section 8) with sensitivity classifications (CRITICAL/SENSITIVE/ROBUST), valid ranges, and source justifications. The sensitivity classification enables prioritized tuning: 9 CRITICAL parameters should be tuned first at W0.

However, the architecture does not include the joint optimization framework or Bayesian hyperparameter optimization recommended in F-6 mitigation. The staged tuning plan is implicit rather than explicit.

**Assessment: PARTIALLY MITIGATED. Parameter registry with sensitivity classification helps, but the joint optimization gap remains.**

### F-7: Bayesian Transition Whiplash (Composite 6) -- MITIGATED

The architecture specifies the Phase 1 to Phase 2 transition protocol (Section 3.5.4) with: minimum 50 confirmed anomalies, 5-fold cross-validation accuracy > 0.85, and a reversion mechanism (revert to Phase 1 if Tier 3 FPR exceeds 3x Phase 1 FPR for 3 consecutive CONSOLIDATION_CYCLEs).

**Assessment: MITIGATED. The transition protocol with reversion addresses F-7 directly.**

### F-8: Silent Tier 3 Starvation (Composite 6) -- MITIGATED

The architecture addresses this with the Hybrid Pool and synthetic anomaly supplementation (Section 4.5). At low-anomaly-rate scales (1K agents), Tier 3 supplements with synthetic calibration anomalies from known-benign pairs. The Dormant/Active lifecycle with hysteresis prevents oscillation.

**Assessment: MITIGATED. Synthetic supplementation directly addresses the data starvation problem.**

### F-9: NMI Divergence Arms Race (Composite 4) -- MITIGATED

FC-5 resolution (Section 7.3) provides the game-theoretic analysis with bounded residual risk (~10 agents at 100K). Randomized perturbation direction prevents pre-compensation.

**Assessment: MITIGATED.**

### F-10: Correlated Channel Resonance (Composite 4) -- PARTIALLY MITIGATED

The Bayesian network's conditional dependency structure (V->B, V->E, B->E) partially accounts for channel correlation. However, the Phase 1 quorum fusion (3-of-4) treats channels as independent, which is the regime where resonance is most dangerous.

**Assessment: PARTIALLY MITIGATED. Phase 2 Bayesian network handles this; Phase 1 quorum does not.**

### Pre-Mortem Coverage Summary

| Scenario | Composite | Architecture Mitigation |
|----------|-----------|------------------------|
| F-1: Calibration Poisoning | 12 | PARTIALLY MITIGATED (Four-Phase Bootstrap, but canary agents absent) |
| F-2: Integration Cascade | 12 | PARTIALLY MITIGATED (NMI hardening, but no self-referential suppression) |
| F-3: PCM Divergence | 9 | MITIGATED (ridge regularization + R-squared fallback) |
| F-4: Cross-Neighborhood Sybil | 8 | NOT MITIGATED (architectural blind spot) |
| F-5: Epoch Desynchronization | 6 | NOT MITIGATED (tick-count-based windows) |
| F-6: Parameter Tuning | 6 | PARTIALLY MITIGATED (parameter registry, no joint optimization) |
| F-7: Bayesian Whiplash | 6 | MITIGATED (transition protocol + reversion) |
| F-8: Tier 3 Starvation | 6 | MITIGATED (synthetic supplementation) |
| F-9: NMI Arms Race | 4 | MITIGATED (FC-5 game-theoretic analysis) |
| F-10: Channel Resonance | 4 | PARTIALLY MITIGATED (Bayesian network, not Phase 1 quorum) |

**Of the top 3 failure scenarios (composite >= 9), two are only partially mitigated and one is fully mitigated. Of the remaining 7, two are not mitigated, three are partially mitigated, and two are fully mitigated.**

---

## 4. COMPLETENESS ASSESSMENT

### 4.1 Present and Sufficient for SPECIFICATION

- Three-tier architecture with clear separation of concerns.
- Complete data models for all tiers (Tier1AgentState, NeighborhoodState, Tier3 evidence store).
- Full PCM specification (log-linear model, 5 covariates, 10 interactions, MLE estimation, convergence experiment).
- Full channel fusion specification (Phase 1 quorum, Phase 2 Bayesian network with DAG structure and CPTs).
- 7 cross-layer contracts with schemas, cadences, and failure modes.
- Security architecture with 6 attack classes analyzed.
- 86-parameter registry with sensitivity classifications.
- Pseudocode for all major processing paths.
- Scalability analysis at three target scales.
- Persistence and recovery specification.
- Cluster Membership API specification.

### 4.2 Missing or Incomplete

1. **State machine diagrams.** The architecture describes state transitions textually (CalibrationStatus, TriggerState, Tier 3 Dormant/Active) but Part 3 announces consolidated state machines in "Section 9" which appears to be the pseudocode section rather than formal state machine specification. The Specification Writer will need to formalize these into explicit state transition tables.

2. **Formal properties and invariants.** Part 1 provides PROP-T1-1 through PROP-T1-5 for Tier 1. Part 2 announces that Part 3 will cover "Section 8 (Formal Properties + Invariants)." The reviewed Part 3 contains Section 8 (Parameter Registry) but does not contain system-wide formal properties. The Tier 2 and Tier 3 formal properties are missing.

3. **Lean alternative specification.** Condition C-9 requires the lean alternative (C17 + C12 + thresholds) to be documented as the contingency plan. The architecture references C-9 but does not provide the lean alternative's specification. This should be a short appendix.

4. **Carried conditions traceability.** Conditions C-1 through C-3 from Ideation are addressed in the architecture (C-1: raw + residual emission in Section 3.2.6; C-2: unmodeled correlation category in Section 3.2.7; C-3: coverage fallback in Section 3.2.8). Conditions C-4 through C-8 from Feasibility are also addressed. However, a formal traceability matrix linking each condition to its resolution section is absent.

5. **Global residual aggregation.** The architecture lacks the global (cross-neighborhood) anomaly aggregation that Pre-Mortem F-4 recommends. Even a lightweight version (testing whether unconfirmed Tier 1 triggers are uniformly distributed across neighborhoods) would strengthen the architecture against the dispersed Sybil swarm scenario.

---

## 5. MEMORY AND STORAGE DISCREPANCY

Two different memory estimates appear in the document:

- Section 1.6 / 6.5 (Data Architecture): 720.9 MB at 100K agents.
- Section 10.2 (Scalability Analysis): 261 MB at 100K agents.

The discrepancy arises from different component inventories and different MIDAS CMS sizing assumptions. Section 6.5 uses CMS width=1024 and includes detailed per-component breakdowns. Section 10.2 uses CMS depth=4, width=1024 but arrives at lower Tier 2 totals (189 MB vs. 438 MB) and lower per-agent state (60 MB vs. 200 MB). The per-agent state difference comes from different LTA window sizes (60 ticks in Section 1.6 vs. 600 ticks in Section 6.1 -- this is also an internal inconsistency: the LTA window is 60 ticks per Section 2.4.2 but the data structure in Section 6.1 allocates 600 entries).

This must be reconciled before SPECIFICATION. The Specification Writer cannot work with contradictory memory budgets.

---

## 6. DESIGN FLAGS

| Flag | Severity | Description | Recommendation |
|------|----------|-------------|----------------|
| DF-1 | MEDIUM | FC-1 convergence experiment uses independent covariates; correlated-covariate regime (C3 scheduling induces x_1/x_2 correlation) is untested | Add a fourth experimental condition with correlated covariates drawn from a C3 scheduling simulation |
| DF-2 | HIGH | No self-referential anomaly suppression: C35 cannot distinguish "I detected a real problem" from "my own stale data caused the anomaly I am detecting." Pre-Mortem F-2 cascade risk remains. | Add a self-attribution check: if anomaly onset coincides with C35 state change within 2 CONSOLIDATION_CYCLEs, flag as POSSIBLY_SELF_INDUCED. Add ETR emission rate limiter (cap at 10% of neighborhoods per cycle). |
| DF-3 | LOW | Memory estimates inconsistent between Section 6.5 (720.9 MB) and Section 10.2 (261 MB). LTA window size contradictory (60 ticks in Section 2.4.2 vs. 600 entries allocated in Section 6.1). | Reconcile before SPECIFICATION. The Specification Writer needs a single authoritative memory budget. |
| DF-4 | MEDIUM | Bayesian fusion pseudocode (Section 9.4) indexes channels as [Infrastructure=0, Verification=1, Behavioral=2, Economic=3], inconsistent with all other sections which use [Verification=0, Behavioral=1, Infrastructure=2, Economic=3]. | Correct channel index mapping in pseudocode. |
| DF-5 | MEDIUM | Cross-neighborhood Sybil swarm (F-4) is not mitigated. Architecture has no mechanism to detect adversaries who distribute one agent per neighborhood with diversified behavioral profiles. | Add lightweight global residual aggregation: at each CONSOLIDATION_CYCLE, test whether unconfirmed Tier 1 trigger distribution across neighborhoods is uniform (chi-squared test against Poisson expectation). Uniform distribution is itself a dispersal anomaly signal. |
| DF-6 | LOW | Tier 2 and Tier 3 formal properties not specified. Only Tier 1 has PROP-T1-1 through PROP-T1-5. | Specification Writer should derive and state formal properties for all three tiers. |
| DF-7 | LOW | Lean alternative (Condition C-9) not documented. | Add short appendix specifying the contingency plan architecture. |
| DF-8 | LOW | Condition traceability matrix absent. | Add table mapping each carried/new condition (C-1 through C-9, D-1) to its resolution section. |

---

## 7. OVERALL ASSESSMENT

### Verdict: PASS_WITH_FLAGS

**Rationale:**

The C35 architecture document is a substantial, technically rigorous design that resolves 4 of 5 blocking conditions (FC-1 through FC-3 and FC-5; FC-4 is out of scope). The three-tier pipeline is coherently specified from data model through pseudocode. The 7 cross-layer contracts are complete and consistent with the C9 integration framework. The security architecture analyzes 6 attack classes with honest residual risk assessments. The parameter registry provides complete coverage with sensitivity classifications. The scalability analysis demonstrates feasibility at all target scales.

The architecture has no fatal flaws. The 8 design flags identify issues that range from LOW to HIGH severity, but none individually or collectively warrant a FAIL verdict. The HIGH-severity flag (DF-2, self-referential anomaly suppression) is a genuine gap, but it is a well-understood feedback loop problem with known solutions that can be incorporated during SPECIFICATION without restructuring the architecture.

The architecture's treatment of the Pre-Mortem scenarios is reasonable: 4 of 10 are fully mitigated, 4 are partially mitigated, and 2 are not mitigated. The two unmitigated scenarios (F-4 cross-neighborhood Sybil swarm and F-5 epoch desynchronization) represent genuine architectural limitations. F-5 is a relatively low-priority operational concern (tick rate changes are rare and can be managed procedurally). F-4 is a more fundamental gap that DF-5 partially addresses with lightweight global aggregation.

**Conditions for proceeding to SPECIFICATION:**

1. **MUST resolve before SPECIFICATION:** DF-2 (self-referential anomaly suppression), DF-3 (memory estimate reconciliation), DF-4 (channel index correction).
2. **SHOULD resolve before SPECIFICATION:** DF-1 (correlated-covariate FC-1 extension), DF-5 (global residual aggregation).
3. **MAY defer to SPECIFICATION:** DF-6, DF-7, DF-8 (formal properties, lean alternative, traceability matrix).

---

## 8. MONITORING FLAGS UPDATE

| Flag | Previous Status | Updated Status | Notes |
|------|----------------|----------------|-------|
| MF-2 | OPEN (PCM convergence) | RESOLVING (FC-1 experiment designed, needs correlated-covariate extension per DF-1) | Architecture provides experiment protocol; execution is implementation-phase |
| MF-4 | OPEN (Fixed-baseline reconstructibility) | RESOLVED (FC-3 Red Team protocol specified) | Three-layer defense with information-theoretic bound |
| MF-5 | NEW (PCM residual calibration bias) | OPEN (partially addressed by Four-Phase Bootstrap) | Canary agent mechanism from F-1 mitigation absent |
| MF-6 | NEW (Bayesian network sample size) | RESOLVED (synthetic supplementation via Hybrid Pool) | Section 4.5 addresses directly |
| MF-7 | NEW (Adversarial spectral clustering) | RESOLVED (FC-5 game-theoretic analysis) | Section 7.3 provides bounded residual risk |

---

*End of Mid-DESIGN Review.*
