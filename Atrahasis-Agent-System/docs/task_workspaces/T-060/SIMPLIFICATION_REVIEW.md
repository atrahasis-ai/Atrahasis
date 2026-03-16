# C35 Simplification Review

**Invention:** C35 -- Seismographic Sentinel with PCM-Augmented Tier 2
**Reviewer Role:** Simplification Agent
**Date:** 2026-03-12
**Architecture Version Reviewed:** 1.0.0
**Focus:** Removable complexity -- what can be cut, collapsed, or derived without losing essential capability

---

## Summary

The C35 architecture specifies a 4,056-line, three-tier detection pipeline with 86 logical parameters (128 registry slots), 7 cross-layer integration contracts, 14 API endpoints, and 6 attack-class defenses. The core detection chain -- STA/LTA per-agent triggers, PCM-corrected pairwise correlation, and epidemiological backward tracing -- is sound. But the architecture has accreted significant weight in three areas: over-parameterization, over-specified defensive mechanisms for low-probability threats, and integration surface area that exceeds what detection actually requires. This review identifies 19 simplification candidates across 6 categories. Net recommendation: 14 parameters can be eliminated or derived, 3 mechanisms can be removed, and 4 mechanisms can be substantially simplified, reducing total parameter count from 86 to approximately 62-66 and removing roughly 800-1,000 lines of specification without losing any capability that matters at the W0-W2 time horizon.

---

## Category 1: Parameter Elimination (Derivable or Redundant)

### S-01: Eliminate 10 PCM Interaction Terms Per Channel (40 parameters total)

**Component:** PCM log-linear model, Section 3.2.3, parameters gamma_12 through gamma_45 (registry slots 25-88, the interaction portion).

**Current state:** The PCM has 16 parameters per channel: 1 intercept, 5 main effects, 10 pairwise interactions. 10 interactions x 4 channels = 40 interaction parameters. The architecture justifies all 10 interactions with brief qualitative rationales (e.g., "parcel colocation x epoch coregistration: co-registered agents in the same parcel may share deployment infrastructure").

**What could be removed:** Start with main-effects-only (6 parameters per channel, 24 total). Add interaction terms only when the convergence experiment (FC-1, Section 3.2.9) demonstrates that they improve R-squared by at least 0.05 on held-out data. The architecture's own convergence experiment protocol already includes a "remove interaction terms first" failure criterion if convergence takes too long (Section 3.2.9, step 7). This means the architecture already acknowledges the interactions may not be needed.

**Capability lost:** Ability to model non-additive covariate effects from day one.

**Is it essential?** No. The PCM convergence experiment has not been run. The interactions are speculative. If committee co-assignment and parcel co-location interact multiplicatively, the main-effects model will underfit those pairs, producing larger residuals -- which is a *conservative* failure mode (more false positives, not fewer). Better to start simple and add complexity when data justifies it.

**Recommendation:** SIMPLIFY. Default to 6 parameters per channel (24 total). Reduce PCM registry slots from 64 to 24. Define a formal criterion for adding interactions post-W0. Net savings: 40 parameters eliminated, ~100 lines of interaction term specification removed.

---

### S-02: Derive Confirmation Window Durations From Trigger Density

**Component:** Tier 1 confirmation window, Section 2.7.1, parameters #8 (confirmation_window_normal = 3) and #9 (confirmation_window_extended = 5).

**Current state:** Two separate parameters define the confirmation window length under normal vs. high-density conditions. High-density is itself determined by parameter #10 (trigger_density_sigma_threshold = 2.0).

**What could be removed:** A single parameter (base_confirmation_window) with a deterministic rule: window = base + floor(density_z_score). At z=0, window=3. At z=2, window=5. At z=4, window=7. This collapses three parameters into one while preserving the adaptive behavior.

**Capability lost:** Independent tuning of normal vs. extended window duration.

**Is it essential?** No. The two windows differ by exactly 2 ticks. The relationship between density and required confirmation is monotonic. A formula replaces a lookup table with no loss of control.

**Recommendation:** SIMPLIFY. Collapse parameters #8, #9, #10 into a single base_confirmation_window with a derivation rule. Net savings: 2 parameters.

---

### S-03: Derive Channel Confidence Weights From Threshold Inverses

**Component:** Tier 1 confidence score, Section 2.8, parameters #15-#18 (metric_*_weight, values 0.30, 0.30, 0.20, 0.20).

**Current state:** Four separate weight parameters for the composite confidence score. They are manually set and sum to 1.0.

**What could be removed:** Derive weights as the inverse of the channel threshold (theta_c), normalized. Channels with tighter thresholds (lower theta_c) are inherently more informative when they trigger, so they should carry more weight. The current defaults roughly follow this pattern already (behavioral_consistency has theta=0.20 and weight=0.20; committee_frequency has theta=0.50 and weight=0.20 -- but committee's weight should be lower under the inverse-threshold rule, which it should be).

**Capability lost:** Independent manual tuning of confidence weights separate from detection thresholds.

**Is it essential?** No. The current weight values are "design choice" (per parameter registry). They have no empirical basis. Deriving them from thresholds is both simpler and more principled.

**Recommendation:** SIMPLIFY. Derive weights = (1/theta_c) / sum(1/theta_c). Eliminate 4 parameters. Net savings: 4 parameters.

---

### S-04: Collapse Tier 2 Residual Thresholds Into a Single Parameter

**Component:** Tier 2 MIDAS edge event generation, Section 3.3.2, four per-channel residual thresholds (threshold_R per channel: 0.15, 0.10, 0.20, 0.12).

**Current state:** Four separate thresholds, one per channel. The values differ by a factor of 2x (0.10 to 0.20). Each has its own rationale paragraph.

**What could be removed:** A single base_residual_threshold parameter (default 0.15) with per-channel scaling factors derived from the channel's natural variance (which the PCM already computes as pcm_residual_std per neighborhood-channel). The threshold for channel c becomes: base_residual_threshold * (pcm_residual_std_c / mean_pcm_residual_std).

**Capability lost:** Independent manual tuning of per-channel residual sensitivity.

**Is it essential?** No. The per-channel thresholds are "design choice" defaults that have not been empirically validated. The PCM already tracks residual standard deviation per channel, which is the natural scaling basis. Using it automatically adapts thresholds to the actual data distribution rather than hardcoded guesses.

**Recommendation:** SIMPLIFY. Single base_residual_threshold, derive per-channel from PCM statistics. Net savings: 3 parameters.

---

### S-05: Eliminate clustering_recompute_epochs (Always 1)

**Component:** Tier 2 spectral clustering, parameter #24 (clustering_recompute_epochs = 1, range [1, 5]).

**Current state:** Configurable number of CONSOLIDATION_CYCLEs between full spectral recomputations. Default is 1 (recompute every cycle). The architecture never describes a scenario where a value other than 1 is appropriate.

**What could be removed:** The parameter. Spectral clustering always runs every CONSOLIDATION_CYCLE. If compute budget is an issue at extreme scale, the Nystrom approximation (Section 10.4) handles it. Skipping cycles creates stale neighborhoods with no mechanism to detect when staleness becomes harmful.

**Capability lost:** Ability to skip expensive recomputations.

**Is it essential?** No. The Nystrom approximation already solves the computational cost problem. A skip-cycles parameter is a second solution to the same problem, and the inferior one (stale data vs. approximate data).

**Recommendation:** REMOVE. Hardcode to 1. Net savings: 1 parameter.

---

### S-06: Eliminate anomaly_severity_levels (Fixed Enum, Not a Parameter)

**Component:** Cross-layer parameters, parameter #125 (anomaly_severity_levels = 4, fixed value).

**Current state:** A "parameter" whose value is fixed at 4 and marked as "{4}" in the valid range. It defines the count of severity levels: LOW, MEDIUM, HIGH, CRITICAL.

**What could be removed:** This is not a parameter. It is a type definition. The severity levels are an enum used throughout the specification. Changing the number of levels would require rewriting every API schema, every consumer, and every integration contract. It should be a constant, not a parameter slot.

**Capability lost:** None. It was never tunable.

**Is it essential?** It was never a parameter in any meaningful sense.

**Recommendation:** REMOVE from parameter registry. Declare as a constant enum. Net savings: 1 parameter slot.

---

### S-07: Eliminate quorum_n (Fixed at 4 by Architecture)

**Component:** Channel fusion, parameter #96 (quorum_n = 4, fixed value "{4}").

**Current state:** The total number of channels is architecturally fixed at 4. The parameter is marked as FIXED in the registry. Changing it would require defining new channels, new data sources, new integration contracts.

**What could be removed:** Same argument as S-06. This is a structural constant, not a tunable parameter.

**Capability lost:** None.

**Recommendation:** REMOVE from parameter registry. Declare as a constant. Net savings: 1 parameter slot.

---

### S-08: Derive Tier 3 active_to_dormant_threshold From dormant_to_active

**Component:** Tier 3 lifecycle, parameters #115 (dormant_to_active_threshold = 3) and #116 (active_to_dormant_threshold = 100).

**Current state:** Two independent thresholds for the DORMANT/ACTIVE state machine. The dormant-to-active threshold requires 3 confirmed anomalies; active-to-dormant requires 100 epochs without activation.

**What could be removed:** The active-to-dormant threshold can be derived as: dormant_to_active_threshold * expected_anomaly_interarrival_epochs * hysteresis_factor. Or more simply: just use a fixed ratio (active_to_dormant = 30 * dormant_to_active). The hysteresis is the point -- it should be proportional to the activation threshold, not independently tuned.

**Capability lost:** Independent tuning of activation vs. deactivation hysteresis.

**Is it essential?** No. The relationship is inherently coupled. Setting them independently creates a risk of pathological oscillation that a ratio constraint prevents.

**Recommendation:** SIMPLIFY. Derive active_to_dormant as a fixed multiple of dormant_to_active. Net savings: 1 parameter.

---

**Category 1 Total:** 14 parameters eliminated or derivable. Registry shrinks from 128 slots to approximately 112-114 slots; logical parameters from 86 to approximately 66-68.

---

## Category 2: Over-Engineered Defense Mechanisms

### S-09: Simplify NMI Hardening to a Lighter Mechanism

**Component:** Spectral clustering NMI hardening, Section 3.1.3.

**Current state:** The architecture computes spectral clustering TWICE per CONSOLIDATION_CYCLE -- once on the real graph, once on a Gaussian-perturbed copy -- then computes Normalized Mutual Information between the two clusterings to detect adversarial manipulation. At 100K agents, this doubles the spectral clustering cost to ~200 seconds.

**What could be removed:** Replace full NMI check with a cheaper membership stability test. Instead of re-clustering the perturbed graph, compute how many agents would change neighborhood assignment if their top-K edge weights were perturbed by sigma_NMI. This requires only scanning each agent's neighborhood boundary (edges to agents in other neighborhoods), which is O(V * avg_degree) -- much cheaper than a full eigendecomposition.

Specifically: for each agent, compute stability_score = min_cross_neighborhood_edge_weight / max_within_neighborhood_edge_weight. If stability_score < threshold for more than X% of agents, the clustering is unstable. This catches the same attack class (boundary perturbation) at O(V * deg) instead of O(V * k * iters) for a second spectral decomposition.

**Capability lost:** Full information-theoretic stability measurement (NMI). The simpler check only detects agents near boundaries, not global structural instability.

**Is it essential?** The game-theoretic analysis in Section 7.3 already shows the practical detection boundary is B > 0.3 * sqrt(V) -- about 30 edges at 10K agents. The NMI check catches these perturbations because they affect enough of the structure to shift the clustering. But the boundary stability check catches the same perturbations because all edge-budget attacks MUST target boundary agents. The NMI check's advantage is detecting coordinated perturbations that individually are sub-threshold but collectively shift the partition -- but Section 7.3 shows this requires B > 0.3*sqrt(V) edges anyway, which also shifts boundary stability scores.

**Recommendation:** SIMPLIFY. Replace double-spectral-clustering NMI check with boundary stability scan. Retain NMI as an optional diagnostic computed every 10th CONSOLIDATION_CYCLE rather than every cycle. Net savings: ~50% reduction in CONSOLIDATION_CYCLE compute cost; ~80 lines of NMI specification; 1 parameter reduced in criticality (nmi_divergence_threshold moves from CRITICAL to diagnostic).

---

### S-10: Remove Laplace Noise on Fixed Baseline (Section 2.5.3)

**Component:** Fixed baseline Laplace noise injection, Section 2.5.3.

**Current state:** After computing fixed baseline percentiles, Laplace noise is added to each value with epsilon=1.0. Post-noise clamping enforces monotonicity. The purpose is to "protect against reconstruction attacks" where an adversary infers the baseline from trigger observations.

**What could be removed:** The entire Laplace noise mechanism. The architecture's own Red Team analysis (Section 7.2) shows that the primary defense against baseline reconstruction is NOT the Laplace noise -- it is the combination of (b) randomized trigger threshold jitter (5% per tick) and (c) binary-only feedback. The Laplace noise contributes ~1.414 units of standard deviation to the stored baseline, but the threshold jitter contributes fresh noise at every evaluation tick. The jitter is the dominant defense.

Furthermore, the Laplace noise degrades the fixed baseline's detection accuracy. The clamping operation (Section 2.5.3) can compress the P5-P95 range, reducing the baseline's ability to distinguish normal from anomalous behavior. This is a self-inflicted wound: the system deliberately worsens its own detector to defend against a reconstruction attack that the jitter already defeats.

**Capability lost:** Formal differential privacy guarantee on stored percentiles. An adversary who gains read access to the baseline storage (not just trigger observations) can reconstruct exact percentile values.

**Is it essential?** No. Read access to baseline storage is an infrastructure compromise, which is a different threat class than the A/B testing attack the noise is designed for. Infrastructure compromise requires infrastructure defense (encryption at rest, access control), not statistical obfuscation that degrades detection accuracy.

**Recommendation:** REMOVE. Keep threshold jitter (which is lightweight and effective). Remove Laplace noise injection. Remove post-noise clamping logic. Reduce parameter #6 (laplace_epsilon) from the registry. Net savings: 1 parameter, ~30 lines of specification, improved fixed baseline accuracy.

---

### S-11: Defer Four-Phase PCM Bootstrap Poisoning Protocol

**Component:** PCM calibration poisoning mitigation, Section 7.4.

**Current state:** A four-phase protocol spanning 1000+ epochs: (1) raw similarity bootstrap, (2) initial PCM calibration, (3) retrospective audit at epoch 1000, (4) recalibration with exclusion set. Each phase has specific threshold values, operational modes, and fallback behaviors.

**What could be removed:** Phases 3 and 4. The retrospective audit and recalibration are defense against an adversary who behaves normally during the entire 1000-epoch bootstrap then activates. The architecture's own analysis (Section 7.4, "Residual Risk Assessment") acknowledges this adversary is fundamentally undetectable: "An adversary who behaves identically to a legitimate agent during the full 1000-epoch bootstrap and activation phases cannot be detected or excluded." It then bounds the impact of a single poisoner at <5% coefficient bias and notes that even 5 coordinated poisoners produce at most 20% bias.

Since the retrospective audit only catches poisoners whose behavior WAS anomalous during bootstrap (which Phase 1 could have caught in real-time with lower thresholds), and the recalibration only acts if coefficient change exceeds 20% (which means 5+ coordinated poisoners), the practical value of Phases 3-4 is marginal.

**Capability lost:** Detection of moderate-scale calibration poisoning (3-5 poisoners in a neighborhood) after the fact.

**Is it essential?** Not for W0-W2. The architecture already has two defenses: (a) Phase 1 conservative thresholds filter obvious anomalies during bootstrap, and (b) C12 AVAP independently detects colluding agents. Adding Phases 3-4 catches a narrow case (poisoners who are anomalous enough to bias coefficients by 20%+ but not anomalous enough to trigger Phase 1's conservative thresholds) that is unlikely at early deployment scales.

**Recommendation:** SIMPLIFY. Specify Phases 1-2 only for W0-W2. Document Phases 3-4 as a "future hardening" item to be revisited when the PCM has real calibration data. Net savings: ~120 lines of specification, reduced operational complexity during bootstrap.

---

## Category 3: Tier 3 Complexity vs. Firing Frequency

### S-12: Simplify Tier 3 Synthetic Anomaly Pool

**Component:** Tier 3 sample size management, Sections 4.2 and 4.5.

**Current state:** Tier 3 requires a minimum of 30 confirmed anomalies to run overdispersion analysis. When fewer than 30 real anomalies exist, synthetic calibration anomalies are generated from known-benign agent pairs with injected residuals. The hybrid pool maintains 100 confirmed + 50 synthetic entries. Synthetic anomalies are generated by the PCM subsystem, are included in the negative binomial fit for statistical power, but excluded from covariate analysis and attribution.

**What could be removed:** The entire synthetic anomaly generation mechanism. Instead, simply raise the activation threshold to match available data, or lower the minimum sample size.

The justification for synthetic supplementation is that the overdispersion test requires n >= 30 for adequate power (65% at alpha=2.0). But 65% power at n=30 means a 35% miss rate even with sufficient data. At n=15-20 (which is achievable within 1-2 CONSOLIDATION_CYCLEs at 10K agents), power drops to perhaps 45-55%. This is weaker, but Tier 3 is a last-resort attribution mechanism, not a primary detector. Tiers 1 and 2 handle detection. Tier 3 adds attribution value but is not a hard dependency.

The alternative: set tier3_min_sample_size = 15 and accept reduced statistical power. Document the power curve. Let the system accumulate real data rather than manufacturing synthetic data to hit an arbitrary threshold.

**Capability lost:** Statistical power guarantee for overdispersion analysis at low-anomaly-rate scales.

**Is it essential?** No. At 1K agents (where synthetic supplementation matters most), the architecture itself notes that "Tier 3 will take days to accumulate sufficient real anomalies... This is acceptable: at 1K agents, the attack surface is smaller and alternative detection mechanisms (manual review, C12 AVAP) are more feasible" (Section 4.5). If Tier 3 dormancy is acceptable at 1K agents, then a lower-powered Tier 3 is equally acceptable -- the difference between "dormant" and "running at reduced power" is marginal.

**Recommendation:** SIMPLIFY. Remove synthetic anomaly generation. Lower tier3_min_sample_size to 15. Accept reduced power at small scales. Net savings: ~80 lines of specification (SyntheticAnomaly struct, HybridPool refresh logic, synthetic generation from PCM); 1 parameter (#112, synthetic_pool_size) eliminated; conceptual simplification of Tier 3 data flow.

---

### S-13: Flatten Tier 3 Backward Tracing to Two Data Sources

**Component:** Tier 3 backward tracing, Section 4.3, Steps 2a-2d.

**Current state:** The backward trace queries four cross-layer data sources: (a) C17 behavioral similarity chains, (b) C7 intent provenance, (c) C3 scheduling co-occurrence, (d) C8 settlement flow paths. Each source has its own query pattern, edge weight semantics, and API contract.

**What could be removed:** Sources (c) and (d). C3 scheduling co-occurrence is explicitly acknowledged as non-causal ("not causal evidence by itself... identifies agents that have had opportunity for coordination" -- Section 4.3, Step 2c). C8 settlement flow paths are useful for economic attribution but overlap significantly with the Tier 2 economic channel, which already flags correlated settlement patterns BEFORE they reach Tier 3.

The two remaining sources -- C17 behavioral similarity and C7 intent provenance -- provide the strongest causal signals: behavioral kinship (shared operator/lineage) and operational linkage (shared sagas/delegations). These are the sources that actually identify common ancestors. Co-occurrence and settlement flows enrich the picture but don't change the attribution conclusion in the vast majority of cases.

**Capability lost:** Economic flow tracing (detecting fund tunneling through multiple agents) and scheduling co-occurrence evidence in attribution reports.

**Is it essential?** Economic flow tracing is valuable but can be deferred. At W0-W2 scale (<10K agents), settlement patterns are sparse enough for manual audit when Tier 3 identifies the suspect agents via behavioral/intent tracing. C3 scheduling co-occurrence is weak evidence by the architecture's own admission.

**Recommendation:** SIMPLIFY. Implement Tier 3 with C17 + C7 sources only. Define C3 and C8 trace sources as "enrichment extensions" for post-W2. Net savings: ~60 lines of specification, 2 fewer cross-layer query contracts in Tier 3, reduced Tier 3 latency.

---

## Category 4: Cross-Layer Integration Surface

### S-14: Downgrade C6 Integration From Contract to Advisory

**Component:** C6 (EMA) integration, Section 5.3.

**Current state:** C6 provides quantum_submission_rate and coherence_score as supplementary Tier 1 inputs, weighted at 0.1x the primary metrics. C35 reciprocates with a cluster_context API. Three data flows are defined (C6->C35:KMETRICS inbound, C35->C6:CONTEXT outbound, plus full API schema).

**What could be removed:** The entire bidirectional integration contract. The architecture itself classifies this as "LOW PRIORITY" and states: "C6 data enriches detection sensitivity for knowledge-related anomalies but is not required for C35's core detection pipeline. If C6 becomes unavailable, C35 continues operating with reduced sensitivity to knowledge-domain anomalies. No DEGRADED state transition is triggered by C6 silence."

If C6 unavailability has no detection consequence, the integration contract is non-essential infrastructure that adds specification surface area and implementation burden without proportional value.

**Capability lost:** Knowledge-domain anomaly enrichment (0.1x weight signals). C6 loses access to neighborhood context for metabolic regulation.

**Is it essential?** No. The 0.1x weight means C6 signals contribute less than 5% to any composite score. The cluster context API for C6 metabolic regulation is a convenience, not a dependency -- C6's SHREC regulation operates independently of C35 neighborhoods.

**Recommendation:** REMOVE contract. C6 can consume the public cluster membership API (Section 5.8) if it wants neighborhood context. C35 does not ingest C6 metrics. Revisit as a "nice-to-have" enrichment at W3+. Net savings: ~60 lines of specification, 1 fewer integration contract, 1 fewer API endpoint.

---

### S-15: Simplify ETR Signal Export to C3

**Component:** C3 integration, Section 5.1, outbound flow C35->C3:ETR_SIGNALS.

**Current state:** C35 exports three computed signals to C3's ETR system: skew_metric, starvation_flag, and divergence_metric. Each has its own threshold parameter (#122, #123, #124), computation logic, and anomaly semantics.

**What could be removed:** The ETR signal export entirely, or at minimum reduce to a single composite signal. C35 is a detection system. Its job is to detect anomalies and report them. Computing specialized signals for C3's trust regime is scope creep -- C3 should derive scheduling anomaly signals from C35's standard anomaly_level API, not from a bespoke signal interface.

The skew_metric is literally "scheduling STA/LTA ratio" -- which is already the core computation C35 does for its own Tier 1. If C3 needs this value, C35 can expose it through the existing per-agent anomaly_level API (Section 5.8, endpoint #3), not through a separate ETR_SIGNALS push.

**Capability lost:** Pre-computed scheduling-specific signals tailored for C3's consumption.

**Is it essential?** No. C3 can compute its own scheduling skew from the raw data it already has (it is the scheduling system), or consume C35's standard anomaly flags. Three bespoke signals with three bespoke thresholds for one consumer is disproportionate.

**Recommendation:** SIMPLIFY. Remove ETR_SIGNALS outbound flow. Add scheduling-related fields to the per-agent anomaly_level API response. Eliminate parameters #122, #123, #124 (etr_skew_threshold, etr_starvation_threshold, etr_divergence_threshold). Net savings: 3 parameters, ~40 lines of specification, 1 fewer outbound data flow.

---

### S-16: Merge Duplicate API Endpoints

**Component:** Cluster Membership API, Section 5.8, and C3 integration, Section 5.1.

**Current state:** The same neighborhood lookup is available through two different endpoints: GET /sentinel/cluster/{agent_id} (Section 5.8, endpoint #1) and the C3-specific neighborhood lookup described in Section 5.1. The response schemas are nearly identical but not quite (the C3 version includes tidal_phase, the generic version does not).

**What could be removed:** The C3-specific endpoint. All consumers should use the Cluster Membership API with optional query parameters for enrichment fields. One endpoint, one schema, one cache.

**Capability lost:** None. Same data, consolidated access.

**Recommendation:** SIMPLIFY. Single canonical endpoint with optional fields. Net savings: ~20 lines of duplicate specification.

---

## Category 5: Bayesian Network Complexity

### S-17: Defer Bayesian Network Until Empirical Data Exists

**Component:** Phase 2 channel fusion, Section 3.5.2.

**Current state:** The architecture specifies a full Bayesian network with 5 nodes (A, V, B, I, E), directed edges with conditional probability tables, prior values "derived from the system's threat model," CPT learning and update at CONSOLIDATION_CYCLE cadence, cross-validation requirements, reversion protocol, and ~200 lines of specification + pseudocode.

The Phase 1 quorum (3-of-4) is the actual operational mode until 50 confirmed anomalies exist. The feasibility study estimates this takes 6-15 CONSOLIDATION_CYCLEs (60-150 hours) at 1K agents, and 1-2 cycles at 10K agents. At W0-W1 scale, Phase 1 quorum is the only mechanism that will fire.

**What could be removed:** The full Bayesian network specification. Replace with: "Phase 2 fusion will use a learned model (Bayesian network, logistic regression, or other calibrated classifier) trained on confirmed anomaly data. The specific model structure will be determined by analysis of Phase 1 data. Transition criteria: >= 50 confirmed anomalies, cross-validation accuracy > 0.85."

This preserves the design intent (transition from quorum to learned model) without pre-committing to a specific network structure that has no empirical basis. The CPT values in Section 3.5.2 (P(V=1|A=1) = 0.85, P(I=1|A=1) = 0.60, etc.) are invented numbers justified as "derived from the system's threat model." No threat model was run to produce them. They are guesses.

**Capability lost:** A fully specified Bayesian network ready for implementation at W0.

**Is it essential?** No. The Bayesian network cannot activate until 50 confirmed anomalies exist. By that time, real data will be available to inform the network structure. Pre-specifying the structure and CPT values creates a false sense of precision. A simpler approach: keep the quorum as the permanent fallback, and add a learned model when data supports it.

**Recommendation:** SIMPLIFY. Specify Phase 2 as "learned fusion model, structure TBD after Phase 1 data analysis." Retain quorum as permanent fallback. Eliminate parameters #97-#102 (bayesian_prior_anomaly through bayesian_transition_min_anomalies) except for #101 (bayesian_posterior_threshold, which applies to any learned model) and #102 (transition_min_anomalies). Net savings: 4 parameters, ~150 lines of BN specification and pseudocode.

---

### S-18: Is the Quorum Sufficient By Itself?

**Component:** Channel fusion, Section 3.5.1.

**Current state:** The 3-of-4 quorum has a false positive rate of ~0.000481 per pair per epoch. At 132K pairs, that is ~63 false positives per epoch. The architecture treats this as "manageable for Tier 3 processing."

**Analysis:** 63 false positives per epoch is quite good. For comparison, the Bayesian network's advantage is reducing this further by accounting for channel dependencies. But the Bayesian network introduces significant complexity (CPTs, learning, cross-validation, reversion) to achieve a marginal improvement over an already-low false positive rate.

The question is whether the Bayesian network's added detection capability (catching anomalies that are strong in only 1-2 channels, via the high posterior from channel dependency modeling) justifies the complexity. The architecture already addresses this case with the "high-confidence single-channel bypass" (parameter #107): if a single channel's anomaly score exceeds 2x the MIDAS threshold, it bypasses the quorum. This is a simpler mechanism that catches the most important case the Bayesian network would catch.

**Recommendation:** This reinforces S-17. The quorum + single-channel bypass may be sufficient permanently. The Bayesian network should be treated as an optional enhancement, not a core architectural component. KEEP the quorum and single-channel bypass. DEFER the Bayesian network.

---

## Category 6: Specification Bloat

### S-19: Consolidate Redundant Data Model Specifications

**Component:** Per-agent state model specified three times with inconsistent details.

**Current state:** The per-agent state is specified in:
- Section 2.2 (Tier1AgentState struct): STA window = 5 ticks, LTA window = 60 ticks, total 2,400 bytes.
- Section 6.1 (AgentSentinelState struct): STA window = 60 entries (480 bytes), LTA window = 600 entries (4,800 bytes), total ~2,000 bytes (labeled as "2 KB"). This contradicts Section 2.2's window sizes.
- Section 10.2 (Memory Budget table): Per-agent state = V x 600 bytes. This contradicts both prior figures.

These inconsistencies are not simplification per se, but they indicate that the architecture was written in parts without reconciliation. The three specifications should be a single canonical definition.

**Recommendation:** SIMPLIFY. Single canonical per-agent struct in Section 2.2. Remove duplicate definitions from Sections 6.1 and 10.2; reference Section 2.2 instead. Reconcile the window sizes and memory estimates.

---

## Summary of Recommendations

| ID | Category | Action | Params Saved | Lines Saved (est.) |
|----|----------|--------|-------------|-------------------|
| S-01 | PCM interactions | SIMPLIFY (main-effects first) | 40 (logical: 4 groups) | ~100 |
| S-02 | Confirmation window | SIMPLIFY (derive from density) | 2 | ~15 |
| S-03 | Channel weights | SIMPLIFY (derive from thresholds) | 4 | ~10 |
| S-04 | Residual thresholds | SIMPLIFY (derive from PCM stats) | 3 | ~15 |
| S-05 | Recompute epochs | REMOVE | 1 | ~5 |
| S-06 | Severity levels | REMOVE from registry | 1 slot | ~2 |
| S-07 | quorum_n | REMOVE from registry | 1 slot | ~2 |
| S-08 | Active-to-dormant | SIMPLIFY (derive ratio) | 1 | ~5 |
| S-09 | NMI hardening | SIMPLIFY (boundary stability) | 0 (reduce criticality) | ~80 |
| S-10 | Laplace noise | REMOVE | 1 | ~30 |
| S-11 | PCM 4-phase bootstrap | SIMPLIFY (defer phases 3-4) | 0 | ~120 |
| S-12 | Synthetic anomalies | SIMPLIFY (lower threshold) | 1 | ~80 |
| S-13 | Backward trace sources | SIMPLIFY (2 of 4 sources) | 0 | ~60 |
| S-14 | C6 integration | REMOVE contract | 0 | ~60 |
| S-15 | ETR signals | SIMPLIFY (remove bespoke) | 3 | ~40 |
| S-16 | Duplicate API | SIMPLIFY (merge endpoints) | 0 | ~20 |
| S-17 | Bayesian network | SIMPLIFY (defer to post-Phase 1) | 4 | ~150 |
| S-18 | Quorum sufficiency | KEEP quorum + bypass | 0 | 0 |
| S-19 | Redundant state specs | SIMPLIFY (consolidate) | 0 | ~30 |
| **TOTAL** | | | **~62 params saved** | **~824 lines** |

Note: the "62 params saved" includes the 40 interaction parameters from S-01 (which occupy 40 registry slots but are logically grouped as 4 parameter sets). In terms of logical parameter count (per the architecture's own 86-count): approximately 20 logical parameters are eliminated or derivable.

---

## What to KEEP Without Modification

The following components are well-specified and proportional to their value. Do not touch them.

1. **Tier 1 STA/LTA core** (Sections 2.4-2.6). Clean, lightweight, well-bounded. The seismological analogy is sound and the math is standard.

2. **PCM main-effects model** (Section 3.2, minus interactions). The 5 structural covariates are well-chosen and the log-linear fit is computationally cheap. This is the genuine value-add of C35.

3. **MIDAS-F integration** (Section 3.3). Lightweight, constant-memory, proven algorithm. The joint criterion (MIDAS + PCM residual) is a clean conjunction.

4. **Dual-trigger bypass** (Section 2.7.2). Simple, well-justified, low false positive rate. Good design.

5. **Tier 2 to Tier 3 escalation criteria** (Section 3.6.3). The minimum pair count, confidence floor, and recency filter are practical and well-motivated.

6. **XL-1 (C3), XL-2 (C5), XL-5 (C8), XL-6 (C12), XL-7 (C17) integration contracts**. These are the five essential data sources. They are well-specified with appropriate failure modes.

7. **Neighborhood size cap with split-on-overflow** (Section 3.1.2). Clean mechanism, prevents adversarial concentration.

8. **Persistence and recovery model** (Section 6.6). Pragmatic distinction between persisted and reconstructible state. Recovery time estimates are useful.

---

## Concluding Assessment

C35's core design is sound: STA/LTA local detection feeding PCM-corrected regional correlation feeding epidemiological attribution. The three-tier hierarchy is the right structure. The problem is not the architecture -- it is the weight. The document specifies mechanisms for threats that do not exist yet (Laplace noise against baseline reconstruction, four-phase bootstrap poisoning defense, full Bayesian network with invented CPTs), consumes parameter slots on derived quantities, and maintains integration contracts that its own text classifies as non-essential.

The simplest version that works is: 4-channel STA/LTA with dual baselines and confirmation, feeding spectral neighborhoods with main-effects-only PCM and MIDAS, using a 3-of-4 quorum with single-channel bypass, escalating to negative binomial overdispersion analysis with 2-source backward tracing. That is C35 at approximately 60-65% of its current specification size, 75% of its parameters, and very close to 100% of its detection capability at W0-W2 scale.
