# C34 — Seismographic Sentinel with PCM-Augmented Tier 2: Landscape Report

**Role:** Landscape Analyst | **Tier:** OPERATIONAL
**Invention:** C34 — Seismographic Sentinel | **Stage:** RESEARCH
**Date:** 2026-03-11

---

## 1. Industry Landscape

Five domains surveyed for overlap, gaps, and positioning relative to C34's three-tier hierarchical detection pipeline (STA/LTA triggering, PCM-augmented neighborhood quorum, epidemiological backward tracing).

### 1.1 Graph-Based Anomaly Detection Systems

**Current state.** Graph anomaly detection is a mature and rapidly evolving field. The 2025 TKDE survey "Deep Graph Anomaly Detection: A Survey and New Perspectives" catalogs hundreds of methods across node-level, edge-level, and graph-level anomaly detection. Key recent advances include:

- **Residual-based methods.** Ma et al. (2024, TKDE) published "Rethinking Unsupervised Graph Anomaly Detection with Deep Learning: Residuals and Objectives," which uses reconstruction residuals as anomaly scores. This is conceptually adjacent to C34's PCM residual approach, but operates on learned graph representations rather than structural covariates.
- **Context correlation discrepancy.** CoCo (Wang et al., 2025, TKDE) detects anomalies by evaluating variances in node correlations using Transformers for both global and local contextual features. The correlation-based detection philosophy overlaps with C34 Tier 2, but CoCo does not distinguish "expected" from "anomalous" correlation via a structural model.
- **Temporal correlation graphs.** Recent work constructs Temporal Correlation Graphs (TCGs) capturing similarity, causality, and synchronization dependencies. This parallels C34's spectral neighborhood clustering, but TCGs do not model "permitted" correlation from covariates.
- **Causal graph profiling.** A 2025 paper (arXiv:2508.09504) proposes causal graph profiling via structural divergence for anomaly detection in cyber-physical systems, using structural changes in causal graphs as anomaly indicators.

**Gap relative to C34.** No graph anomaly detection system computes expected inter-agent correlation from structural covariates (shared task types, network topology, resource pools) and detects anomalies only in the residual. All existing systems treat raw correlation as the signal. C34's PCM (Permitted Correlation Model) inverts this: expected correlation is normal, only unexplained correlation is anomalous. This distinction is critical in a multi-agent system where legitimate task-sharing creates high baseline correlation.

### 1.2 Sybil and Collusion Defense in Distributed Systems

**Current state.** Sybil detection research accelerated in 2025, driven by blockchain airdrop fraud and AI agent proliferation:

- **Behavioral similarity in blockchain.** A 2025 method detects Sybil addresses via subgraph feature propagation, extracting transaction timing and participation features that capture "consistency of sybil address behavior operations" (arXiv:2505.09313). Achieves >0.9 precision/recall/F1 on a 193K-address dataset.
- **Behavioral analysis with zero-knowledge proofs.** Chakraborty et al. (2025, IEEE) integrate behavioral analysis with ZKPs for multi-layered Sybil detection.
- **SybilShield.** Agent-aided social network-based defense using trust relationships across multiple communities.
- **MCSD (C17).** AAS's own 4-layer Sybil defense including the C17 behavioral similarity layer with 5-modality pairwise B(a_i, a_j) metric.
- **AVAP (C12).** AAS's collusion defense using adversarial verification assignment perturbation.

**Gap relative to C34.** Existing Sybil defenses operate at the identity/account level (is this address fake?) or the behavioral-pair level (are these two addresses the same operator?). C34 operates at the neighborhood/cluster level: given a group of agents in a spectral neighborhood, is their joint correlation pattern anomalous after accounting for structural covariates? This is a higher-order detection primitive. Additionally, no Sybil defense system uses epidemiological backward tracing to attribute confirmed anomalies to specific operators via overdispersion analysis.

### 1.3 Network Monitoring and Intrusion Detection Systems (IDS)

**Current state.** IDS research in 2025 is dominated by multi-modal fusion and deep learning:

- **Multi-modal fusion IDS.** Multimodal fusion-based few-shot IDS (Nature Scientific Reports, 2025) merges traffic feature graphs with network feature sets. CATCH (ICLR 2025) provides channel-aware multivariate time series anomaly detection via frequency patching and a Channel Fusion Module.
- **Ensemble voting.** Ensemble voting classifiers combining SVM, Random Forest, and Logistic Regression for IoT intrusion detection (Sensors, 2024). Soft voting across heterogeneous classifiers is well-established.
- **Information fusion.** Moldovan (2025, WIREs) reviews information fusion-based techniques for improving complex anomaly detection across multiple data sources.
- **Hierarchical detection.** Hierarchical federated learning for IoT anomaly detection with fog-layer aggregation reducing latency.

**Gap relative to C34.** IDS systems use multi-channel fusion but treat channels as complementary data sources to be combined (ensemble fusion). C34's 4-channel quorum (verification, behavioral, infrastructure, economic; >=3 of 4 anomalous) is a fundamentally different design: channels are independent evidence dimensions, and the quorum threshold requires agreement across structurally distinct detection modalities before escalation. No IDS implements a k-of-n quorum across semantically distinct channels with explicit independence assumptions. Additionally, no IDS uses STA/LTA ratio triggering adapted from seismology as the per-agent first-stage detector.

### 1.4 Multi-Agent System Security

**Current state.** Multi-agent system (MAS) security has become a priority discipline as agents move from demos to production:

- **SentinelAgent (May 2025).** The closest prior art. An LLM-powered oversight agent that builds execution graphs in real time and applies anomaly detection at node, edge, and path levels. Detects prompt injection, unsafe tool usage, and multi-agent collusion. Validated on an email assistant and Microsoft's Magentic-One system.
- **Non-human identity anomaly detection.** Security Boulevard (Jan 2026) describes anomaly detection for AI agents establishing baselines for normal behavior and flagging deviations in API call frequency, data access patterns, and agent-to-agent communication.
- **Enterprise adoption.** Gartner predicts 40% of enterprise applications will feature embedded agents by 2026, driving security requirements. Obsidian Security's 2025 landscape report catalogs identity-first controls and real-time behavioral monitoring.

**Gap relative to C34.** SentinelAgent uses LLM-based semantic reasoning over execution graphs, which is fundamentally different from C34's statistical approach (STA/LTA ratios, PCM residuals, overdispersion). SentinelAgent operates at the task/intent level (did this agent make a bad tool call?), while C34 operates at the behavioral-statistical level (is this agent's aggregate pattern anomalous relative to structural expectations?). SentinelAgent has no concept of spectral neighborhood clustering, permitted correlation modeling, or epidemiological attribution. C34 and SentinelAgent are complementary, not competitive: SentinelAgent detects per-action semantic violations, C34 detects statistical behavioral anomalies across populations.

### 1.5 Behavioral Fingerprinting

**Current state.** Behavioral fingerprinting has emerged as both an attack vector and a defense mechanism:

- **Traffic fingerprinting.** Research shows LLM agent interactions leave distinctive fingerprints in encrypted traffic, enabling adversaries to infer agent activities and profile users (arXiv:2510.07176).
- **C17 behavioral similarity.** AAS's own 5-modality behavioral similarity metric (temporal, structural, error, resource, lexical) with pairwise B(a_i, a_j) scores.
- **Website fingerprinting with multi-agent LLMs.** Saxena et al. (2025, arXiv:2509.12462) use multi-agent LLMs to redefine website fingerprinting attacks.

**Gap relative to C34.** Behavioral fingerprinting research focuses on pairwise comparison (are these two agents the same?). C34's Tier 2 extends this to neighborhood-level analysis: within a spectrally-clustered group of agents, does the joint behavioral correlation pattern exceed what structural covariates predict? This is a group-level extension of pairwise fingerprinting that no existing system implements. C34's Tier 1 STA/LTA adds a temporal dimension (is this agent's short-term behavior anomalous relative to its own long-term baseline?) that is absent from static fingerprinting approaches.

---

## 2. Technology Gaps -- What No Existing System Does

### G1: Permitted Correlation Model (PCM) with Structural-Covariate Adjustment

**No direct precedent found.** All graph anomaly detection and behavioral similarity systems treat observed correlation as the raw signal. C34's PCM computes the expected correlation between agents from structural covariates (shared task types, co-location in network topology, shared resource pools, common verification committees) and flags only the residual as anomalous. This is analogous to regression-adjusted analysis in epidemiology, but no system applies this principle to inter-agent correlation in a distributed verification system. The Science Assessment rates the linear additive model as a limitation (non-linear interactions between covariates are possible), but the concept itself is novel.

### G2: STA/LTA Ratio Adapted for Agent Behavioral Monitoring

**No precedent outside seismology and geophysics.** STA/LTA is the standard seismic event trigger (Allen, 1978; Withers et al., 1998). Recent applications extend to microseismic monitoring in mining (V-STA/LTA, 2025), glacier cryoseismology, and mass movement detection. However, no application of STA/LTA to behavioral time series of software agents, network entities, or computational processes was found. C34 further extends STA/LTA with dual baselines (fixed + adaptive), which is novel even within seismology. The Science Assessment notes that the dual-baseline decision fusion rule is unresolved.

### G3: 4-Channel Quorum Fusion with Independence Assumption

**No precedent for k-of-n quorum across semantically distinct anomaly channels.** IDS systems use ensemble voting (soft/hard) across models trained on the same data modality. C34's quorum requires >=3 of 4 structurally distinct channels (verification, behavioral, infrastructure, economic) to independently flag an anomaly. Each channel measures a different dimension of agent behavior. The independence assumption means that correlated false positives across channels are unlikely, dramatically reducing the false alarm rate. The Science Assessment notes that channel independence may not hold perfectly (correlation under certain attack types), but the design principle of requiring cross-domain agreement has no precedent in anomaly detection literature.

### G4: Epidemiological Overdispersion Analysis for Digital Attribution

**Novel cross-domain application.** Epidemiological overdispersion (variance-to-mean ratio exceeding Poisson expectation) is used in disease surveillance to identify superspreader events (Lloyd-Smith et al., 2005). Cyber threat attribution uses ML-based behavioral analysis and intelligence fusion, but does not apply epidemiological cluster analysis. C34's Tier 3 uses overdispersion in anomaly incidence across agents to identify operator-level groupings: if a single operator controls multiple agents, their anomaly patterns will be more clustered (overdispersed) than expected under independent operation. The Science Assessment rates this SOUND WITH CAVEATS, noting sample size concerns at low anomaly counts.

### G5: Integration of G1-G4 Within a Single Hierarchical Pipeline

**No system combines all four innovations.** The prior art search found systems that implement subsets: SentinelAgent has hierarchical graph-based detection but uses LLM reasoning, not statistical methods. IDS systems have multi-channel fusion but not PCM residuals. Sybil detectors have behavioral similarity but not STA/LTA triggering or epidemiological attribution. The integration of STA/LTA triggering (Tier 1) feeding PCM-augmented neighborhood quorum (Tier 2) feeding epidemiological backward tracing (Tier 3) into a single pipeline with controlled escalation is unprecedented.

### G6 (Additional): Spectral Clustering for Agent Neighborhood Definition in Security Context

While spectral clustering is well-studied (Ng et al., 2001; von Luxburg, 2007) and adversarial robustness of spectral methods is an active research area (arXiv:2412.14738, 2025), no system uses spectral clustering over agent interaction graphs to define "neighborhoods" for correlation-based anomaly detection. The use of spectral clusters as the unit of analysis for Tier 2 detection is a novel application of an established technique.

---

## 3. Adjacent Technologies -- Potential Competitors or Complements

### 3.1 SentinelAgent (May 2025) -- Monitor

**Type:** Potential competitor (alternative approach to same problem space).
**Description:** LLM-powered graph-based anomaly detection for multi-agent systems. Builds execution graphs, applies semantic anomaly detection at node/edge/path levels.
**Relationship to C34:** Fundamentally different method (LLM semantic reasoning vs. statistical/epidemiological). SentinelAgent detects per-action semantic violations; C34 detects population-level behavioral anomalies. Complementary in practice. Risk: if SentinelAgent scales well and adds statistical features, it could reduce C34's value proposition.
**Action:** Monitor SentinelAgent's evolution. Assess whether LLM-based detection can achieve C34's false positive rates at scale.

### 3.2 Deep Graph Anomaly Detection (TKDE 2025 Survey Ecosystem) -- Monitor

**Type:** Complement (potential Tier 2 enhancement).
**Description:** GNN-based anomaly detection methods including GAE, DOMINANT, AnomalyDAE, and newer residual-based approaches.
**Relationship to C34:** GNN methods could augment or replace the linear PCM with learned covariate adjustment. The PCM's linear additive model is a deliberate simplicity choice; a GNN could learn non-linear covariate interactions at the cost of interpretability.
**Action:** Track residual-based graph anomaly detection methods. Evaluate whether GNN-learned residuals outperform PCM's linear residuals for the AAS agent population structure.

### 3.3 CATCH Channel-Aware Anomaly Detection (ICLR 2025) -- Monitor

**Type:** Complement (potential alternative to 4-channel quorum).
**Description:** Channel-aware multivariate time series anomaly detection via frequency patching with a Channel Fusion Module.
**Relationship to C34:** CATCH's channel fusion is learned (attention-based), while C34's quorum is fixed (>=3 of 4). CATCH could provide a more adaptive fusion mechanism if channel correlations vary over time.
**Action:** Evaluate whether learned channel fusion outperforms fixed quorum for C34's four channels. Fixed quorum has the advantage of interpretability and auditability.

### 3.4 Blockchain Sybil Detection via Subgraph Features (2025) -- Monitor

**Type:** Complement (potential Tier 3 enhancement).
**Description:** Subgraph-based feature propagation using lightGBM for Sybil detection in blockchain airdrops. Extracts transaction timing, amount, and network structure features.
**Relationship to C34:** The subgraph feature extraction approach could enhance C34's Tier 3 operator attribution by providing additional structural features for overdispersion analysis.
**Action:** Evaluate whether subgraph features improve operator-agent mapping accuracy beyond overdispersion alone.

### 3.5 Federated Graph Neural Networks for Privacy-Preserving Anomaly Detection -- Monitor

**Type:** Complement (deployment alternative).
**Description:** Federated learning over hierarchical GNNs for distributed anomaly detection with privacy preservation (MDPI, 2025).
**Relationship to C34:** If C34 must operate across organizational boundaries (multi-tenant AAS deployments), federated learning could enable privacy-preserving Tier 2 analysis without centralizing agent behavioral data.
**Action:** Track federated anomaly detection maturity. Relevant only if AAS moves to multi-tenant deployment.

### 3.6 Deterministic Simulation Testing (Antithesis, Jepsen) -- Complement

**Type:** Critical testing complement.
**Description:** Deterministic simulation platforms for exhaustive fault injection and invariant verification of distributed systems.
**Relationship to C34:** C34's three-tier pipeline has complex emergent behavior under adversarial conditions. Deterministic simulation can verify that: (a) Tier 1 STA/LTA correctly triggers under adversarial behavioral shifts, (b) Tier 2 PCM residuals correctly identify anomalous neighborhoods, (c) Tier 3 overdispersion correctly attributes operators. C22 already specifies Rust as the core implementation language; Madsim/Turmoil crates provide deterministic async runtimes.
**Action:** Define testable invariants for each tier. Integrate simulation testing from W0 (per C22 implementation plan).

---

## 4. Market Positioning

### 4.1 Positioning Matrix

| Dimension | SentinelAgent | Graph AD (GNN) | IDS (Multi-modal) | Sybil Detectors | C17 (MCSD L2) | **C34** |
|-----------|--------------|----------------|-------------------|-----------------|---------------|---------|
| Per-agent triggering | No (graph-level) | No (node-level) | Yes (flow-level) | No | No (pairwise) | **STA/LTA dual-baseline** |
| Covariate-adjusted correlation | No | Partial (learned) | No | No | No | **PCM structural residuals** |
| Multi-channel quorum | No | No | Ensemble voting | No | No | **4-channel k-of-n** |
| Neighborhood clustering | No | Partial (GNN hops) | No | No | LSH buckets | **Spectral clusters** |
| Backward attribution | Root-cause (LLM) | No | No | No | No | **Epidemiological overdispersion** |
| Scale target | Small MAS (<100) | 10K-1M nodes | Network flows | Blockchain addresses | 1K-100K agents | **1K-100K agents** |
| Method | LLM semantic | Deep learning | ML ensemble | ML classification | Statistical | **Statistical + epidemiological** |

### 4.2 Unique Position Statement

C34 occupies an unoccupied niche: **statistical-epidemiological hierarchical detection for multi-agent verification systems, where expected inter-agent correlation is modeled from structural covariates and only residual anomalies trigger escalation through a multi-channel quorum to operator-level attribution via overdispersion analysis.**

No existing system combines:
1. Seismological STA/LTA as per-agent behavioral trigger
2. Structural-covariate-adjusted permitted correlation modeling
3. k-of-n quorum across semantically distinct detection channels
4. Epidemiological backward tracing for operator attribution
5. Integration within a hierarchical pipeline with controlled escalation and scaling guarantees

### 4.3 Why the Gap Persists

Three structural reasons:

1. **Domain specificity of the PCM concept.** Computing "permitted correlation" requires deep knowledge of why agents correlate: shared tasks, co-scheduling, common resource pools. This knowledge is available in AAS (via C3 scheduling, C7 orchestration, C8 settlement) but not in generic graph systems. Generic anomaly detectors cannot distinguish structural correlation from collusive correlation because they lack the domain model.

2. **Cross-disciplinary synthesis barrier.** C34 combines techniques from seismology (STA/LTA), graph theory (spectral clustering), multivariate statistics (PCM residuals), multi-sensor fusion (quorum thresholds), and epidemiology (overdispersion). These fields rarely cross-pollinate. The seismology-to-agent-monitoring transfer requires recognizing that agent behavioral time series share properties with seismic waveforms (bursty, non-stationary, with a meaningful ratio between short-term and long-term energy).

3. **The integration problem is harder than any component.** Each component has partial prior art; no one has combined them because the integration requires solving the information flow between tiers (Tier 1 feeds Tier 2 feeds Tier 3) with controlled escalation, scaling guarantees at each tier, and cross-layer data dependencies (C5 verification data, C8 economic data, C3 scheduling data, C17 behavioral data).

### 4.4 Competitive Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SentinelAgent adds statistical methods | MEDIUM. Natural evolution if it scales beyond small MAS. | MEDIUM. Would partially address C34's Tier 1 and Tier 2 space. | C34's PCM concept is deeply coupled to AAS domain knowledge; generic statistical additions to SentinelAgent would lack covariate adjustment. |
| GNN-based methods learn PCM-equivalent residuals | LOW-MEDIUM. Residual-based graph AD is trending. | HIGH. Could obsolete linear PCM with superior learned model. | C34 should define PCM as an interface (expected correlation model) that can be backed by linear, GNN, or hybrid implementations. |
| Blockchain Sybil detectors add operator attribution | LOW. Blockchain Sybil detection focuses on address-level, not operator-level. | LOW. Blockchain context is structurally different from AAS. | Monitor for overdispersion-based methods in blockchain research. |
| Major cloud provider ships hierarchical anomaly detection for AI agents | LOW-MEDIUM. Cloud providers are investing in agent security (Obsidian, CrowdStrike). | HIGH. Well-resourced competitor could build similar pipeline. | C34's integration with AAS-specific layers (C3, C5, C7, C8, C12, C17) is a moat. Generic cloud solutions would lack this integration. |
| C17 MCSD L2 evolves to subsume C34 | LOW. C17 is pairwise similarity; C34 is population-level. | MEDIUM. Overlap in behavioral analysis. | C34 and C17 are designed as complementary: C17 provides pairwise B(a_i, a_j) that feeds into C34's Tier 2 behavioral channel. Clear interface boundary. |

---

## 5. Component Readiness

Estimate of what fraction of C34 is off-the-shelf versus novel development, broken down by tier.

### Tier 1: Per-Agent STA/LTA with Dual Baselines

| Component | Readiness | Source |
|-----------|-----------|--------|
| STA/LTA algorithm | OFF-THE-SHELF (100%). Well-implemented in seismology libraries (ObsPy, IRISSeismic). | Allen (1978), Withers et al. (1998) |
| Adaptive baseline (LTA that adjusts to regime changes) | PARTIAL (60%). Adaptive STA/LTA variants exist in seismology; adaptation to agent behavioral time series requires tuning. | V-STA/LTA (2025) |
| Fixed baseline (offline calibrated) | OFF-THE-SHELF (90%). Standard statistical baseline from training data. | Standard practice |
| Dual-baseline decision fusion | NOVEL (20%). No precedent for combining fixed + adaptive STA/LTA baselines with a fusion rule. Science Assessment flags this as unresolved. | C34 innovation |
| Agent behavioral time series extraction | PARTIAL (50%). Requires integration with C5 (verification events), C7 (intent submissions), C8 (settlement). AAS-specific. | AAS integration |

**Tier 1 overall: ~60% off-the-shelf, ~40% novel development.**

### Tier 2: PCM Residuals + Spectral Neighborhood + 4-Channel Quorum

| Component | Readiness | Source |
|-----------|-----------|--------|
| Spectral clustering | OFF-THE-SHELF (95%). Well-implemented in scikit-learn, SciPy. | Ng et al. (2001), von Luxburg (2007) |
| PCM (Permitted Correlation Model) | NOVEL (10%). No direct precedent. The concept of computing expected correlation from structural covariates and detecting only residuals is C34's primary innovation. Linear model construction is straightforward; identifying the right covariates and validating the model requires significant R&D. | C34 innovation |
| 4-channel quorum threshold | PARTIAL (40%). k-of-n voting is standard; applying it across semantically distinct anomaly channels with independence assumptions is novel. | Voting theory + C34 innovation |
| Channel data extraction (verification, behavioral, infrastructure, economic) | PARTIAL (50%). Requires deep AAS integration. C5 provides verification data, C17 provides behavioral similarity, C3/C7 provide infrastructure, C8 provides economic. | AAS integration |
| Near-quadratic PCM precomputation mitigation | NOVEL (15%). Science Assessment flags hidden O(V^2) in PCM precomputation. Spectral clustering amortizes this, but the amortization strategy requires novel design. | C34 innovation |

**Tier 2 overall: ~35% off-the-shelf, ~65% novel development.**

### Tier 3: Epidemiological Backward Tracing

| Component | Readiness | Source |
|-----------|-----------|--------|
| Overdispersion analysis (variance/mean ratio) | OFF-THE-SHELF (90%). Standard epidemiological statistic. Negative binomial models for overdispersed count data are well-established. | Lloyd-Smith et al. (2005) |
| Application to operator-agent attribution | NOVEL (15%). The concept of using overdispersion in anomaly incidence to infer operator-agent mappings is a novel cross-domain application. | C34 innovation |
| Integration with C12 AVAP collusion defense | PARTIAL (40%). C12 provides the adversarial verification assignment framework; linking backward tracing results to AVAP actions requires interface design. | AAS integration |
| Sample size adequacy at low anomaly counts | NOVEL (20%). Science Assessment flags concern about statistical power when anomalies are rare. Bootstrap or Bayesian methods may be needed. | C34 design challenge |

**Tier 3 overall: ~40% off-the-shelf, ~60% novel development.**

### Overall C34: ~45% off-the-shelf, ~55% novel development.

---

## 6. Adoption Barriers

### B1: PCM Model Validation (Severity: HIGH)

The PCM is C34's most novel and most uncertain component. Validating that the structural covariates (shared tasks, co-scheduling, network topology) explain a sufficient fraction of legitimate inter-agent correlation requires empirical data from a running AAS deployment. Until such data exists, the PCM cannot be calibrated, and false positive/negative rates cannot be estimated.

**Mitigation:** W0 experiment (per C22) should include a PCM calibration study using simulated agent populations with known ground-truth correlation structures. The tidal scheduling experiment already planned for W0 provides the scheduling data needed for one covariate dimension.

### B2: Dual-Baseline Decision Fusion (Severity: MEDIUM-HIGH)

The Science Assessment flags the dual-baseline (fixed + adaptive) STA/LTA decision fusion as unresolved. Without a principled fusion rule, Tier 1 may either over-trigger (both baselines flag independently) or under-trigger (requiring both to agree). The correct fusion depends on the operational regime (normal vs. under-attack), which creates a chicken-and-egg problem.

**Mitigation:** Start with a simple rule (either baseline triggers escalation) and refine based on empirical false positive rates. Formally analyze the ROC characteristics of OR-fusion vs. AND-fusion vs. weighted combination.

### B3: Spectral Clustering Adversarial Vulnerability (Severity: MEDIUM)

The Science Assessment rates spectral clustering as CONDITIONALLY SOUND, noting adversarial vulnerability. An adversary who understands the clustering algorithm can manipulate agent interaction patterns to end up in a favorable neighborhood (one with high baseline correlation, masking their anomalous correlation).

**Mitigation:** (a) Randomize the clustering algorithm (add noise to the affinity matrix before spectral decomposition), (b) use ensemble of multiple clustering runs, (c) periodically re-cluster on different time windows.

### B4: Cross-Layer Data Dependency Complexity (Severity: MEDIUM)

C34 requires data from 6 AAS layers (C3 scheduling, C5 verification, C6 knowledge, C7 orchestration, C8 settlement, C17 behavioral similarity) plus C12 collusion defense output. This creates a wide integration surface. Any layer's API change or data format change can break C34's pipeline.

**Mitigation:** Define stable, versioned data contracts between C34 and each source layer. Use C9 cross-layer integration contracts as the interface specification. C34 should consume data via pull (polling stable APIs) rather than push (relying on layers to emit events in a specific format).

### B5: Scaling of PCM Precomputation (Severity: MEDIUM)

The Science Assessment identifies a hidden near-quadratic term in PCM precomputation: computing expected correlation for all agent pairs in a neighborhood is O(k^2) per neighborhood, where k is neighborhood size. For large neighborhoods, this dominates. The overall scaling claim of O(V log V) depends on neighborhoods being small relative to V.

**Mitigation:** (a) Cap neighborhood size via spectral clustering granularity (target k <= sqrt(V)), (b) use sampling-based approximation for large neighborhoods, (c) precompute PCM covariates incrementally (update on agent join/leave rather than recomputing from scratch).

### B6: Epidemiological Sample Size at Low Anomaly Rates (Severity: MEDIUM)

Tier 3 overdispersion analysis requires sufficient anomaly observations to detect non-Poisson clustering. In a well-functioning system, anomalies are rare. With fewer than ~30 anomaly events per analysis window, overdispersion tests have low statistical power.

**Mitigation:** (a) Accumulate anomaly events over longer windows (weeks/months rather than hours), (b) use Bayesian overdispersion estimation (conjugate Gamma-Poisson model) which handles small samples better than frequentist tests, (c) accept that Tier 3 is a slow, strategic detection layer that produces results on a weekly/monthly cadence rather than real-time.

### B7 (Additional): Interpretability and Auditability (Severity: LOW-MEDIUM)

C34's pipeline produces multi-step inferences (STA/LTA trigger -> PCM residual -> quorum agreement -> overdispersion attribution). Explaining to a human auditor why a specific operator was flagged requires tracing through all three tiers. This is more complex than single-stage detection systems.

**Mitigation:** Design the pipeline with full provenance logging at each tier. Each escalation should carry a structured explanation: "Agent A triggered STA/LTA at time T (ratio X); neighborhood N showed PCM residual Y with quorum channels [V, B, E] flagged; overdispersion analysis attributed agents {A, B, C} to operator group with variance/mean ratio Z."

---

## 7. Timing Assessment

**Verdict: FAVORABLE.**

Several converging trends make 2026 favorable timing for C34:

1. **Multi-agent systems entering production.** Gartner's 40% enterprise agent adoption prediction for 2026, plus Anthropic, Google (A2A protocol), and Salesforce (Agentforce) investments, create demand for agent-level security that goes beyond traditional application security. C34 addresses a problem that is becoming real.

2. **SentinelAgent validates the problem space.** The May 2025 publication of SentinelAgent (graph-based anomaly detection for multi-agent systems) confirms that the research community recognizes MAS anomaly detection as an important problem. C34 proposes a different (statistical vs. LLM-based) solution to the same recognized problem.

3. **Graph anomaly detection tools are maturing.** The 2025 TKDE survey, ICLR publications (CATCH), and NeurIPS publications on graph AD provide a foundation of techniques that C34 can build upon. The spectral clustering and residual-based detection components can leverage this ecosystem.

4. **Sybil defense is a live concern.** Blockchain airdrop fraud in 2024-2025 has driven significant investment in behavioral Sybil detection. The techniques being developed (behavioral similarity, temporal clustering, subgraph features) are directly relevant to C34's Tier 2.

5. **AAS dependency readiness.** C17 (MCSD L2 behavioral similarity) is PIPELINE COMPLETE, providing the pairwise B(a_i, a_j) data that feeds C34's behavioral channel. C12 (AVAP collusion defense) is PIPELINE COMPLETE, providing the framework into which C34's Tier 3 attribution results feed. The integration surface exists.

**Unfavorable factor:** The PCM concept has no validation data. Until AAS is deployed (or realistically simulated) at scale, the PCM cannot be calibrated. This timing constraint is inherent to any novel detection method in a system that does not yet exist at production scale. The W0 risk validation experiments (per C22) are the correct mitigation.

---

## 8. Summary of Findings

**Industry coverage.** Five domains surveyed (graph anomaly detection, Sybil/collusion defense, IDS, multi-agent security, behavioral fingerprinting). None implements C34's combined architecture. SentinelAgent (2025) is the closest system overall but uses a fundamentally different method (LLM semantic reasoning vs. statistical/epidemiological). Graph AD research provides the richest component ecosystem but lacks the PCM concept and the hierarchical pipeline integration.

**Six confirmed technology gaps:**
- G1: PCM structural-covariate-adjusted correlation (no direct precedent)
- G2: STA/LTA for agent behavioral monitoring (novel cross-domain application)
- G3: 4-channel quorum across semantically distinct channels (no precedent)
- G4: Epidemiological overdispersion for operator attribution (novel cross-domain application)
- G5: Integration of G1-G4 in a single hierarchical pipeline (no precedent)
- G6: Spectral clustering for security neighborhood definition (novel application of established technique)

**Adjacent technologies to monitor:**
- SentinelAgent (potential competitor if it adds statistical methods)
- Deep graph AD / GNN residual methods (potential PCM enhancement or replacement)
- CATCH channel-aware fusion (potential alternative to fixed quorum)
- Blockchain Sybil detectors with subgraph features (potential Tier 3 enhancement)
- Federated graph NNs (deployment alternative for multi-tenant)
- Deterministic simulation testing (critical testing complement)

**Component readiness:** ~45% off-the-shelf, ~55% novel development. Tier 1 is most ready (~60% off-the-shelf); Tier 2 is least ready (~35% off-the-shelf) due to the PCM's novelty.

**Adoption barriers:** 7 barriers identified. PCM model validation (B1) and dual-baseline fusion (B2) are the highest severity. All have identified mitigations.

**Market position:** Unoccupied niche. The gap persists because the PCM concept requires domain-specific knowledge that generic systems lack, the cross-disciplinary synthesis (seismology + graph theory + epidemiology) is unusual, and the integration problem is harder than any individual component.

**Timing:** FAVORABLE. Multi-agent systems entering production, SentinelAgent validating the problem space, maturing graph AD tools, and AAS dependency readiness all converge to make 2026 the right time for C34. The primary timing constraint is the absence of production-scale validation data for the PCM, which the W0 experiments are designed to address.
