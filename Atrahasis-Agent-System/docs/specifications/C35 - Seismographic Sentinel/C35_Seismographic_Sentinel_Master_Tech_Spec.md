# C35 -- Seismographic Sentinel: Master Technical Specification

**Version:** 1.0.1
**Date:** 2026-03-14
**Invention ID:** C35
**Task:** T-060
**System:** Atrahasis Agent System v2.4
**Author:** Specification Writer (AAS Pipeline)
**Status:** SPECIFICATION stage
**Normative References:** C3 Tidal Noosphere v2.0, C5 PCVM v2.0, C7 RIF v2.0, C8 DSF v2.0, C9 Cross-Layer Reconciliation v2.0, C12 AVAP v2.0, C17 MCSD Layer 2 v1.0
**Temporal Constants:** SETTLEMENT_TICK = 60s, TIDAL_EPOCH = 3600s (60 ticks), CONSOLIDATION_CYCLE = 36000s (600 ticks, 10 epochs)
**Parameter Count:** ~66 logical parameters

---

## Abstract

The Seismographic Sentinel (C35) is a three-tier hierarchical anomaly detection pipeline for the Atrahasis Agent System, designed to provide continuous, population-scale behavioral surveillance across 1,000 to 100,000 autonomous verification agents. The system addresses a critical architectural gap: while existing AAS defenses detect specific threat classes -- C12 AVAP catches collusion rings, C17 MCSD flags Sybil pairs, C13 CRP+ resists consolidation poisoning -- no unified detection substrate exists for emergent, novel, or cross-domain threats. C35 fills this gap through three progressively deeper analytical stages. Tier 1 performs per-agent anomaly detection at every 60-second settlement tick using dual-baseline STA/LTA ratio analysis. Tier 2 correlates agent pairs within spectral neighborhoods using the Permitted Correlation Model (PCM), a main-effects-only log-linear model that computes structurally expected pairwise correlation from five platform covariates and isolates unexplained residuals for MIDAS streaming edge detection. Tier 3 applies epidemiological backward tracing -- negative binomial overdispersion analysis followed by phylogenetic ancestor identification -- to attribute confirmed anomaly clusters to common causal sources. The key innovation is PCM structural correction: by modeling what correlation the platform structure *should* produce, C35 avoids the false-positive flood that plagues raw-correlation approaches and provides downstream consumers (C3, C5, C7, C8, C12, C17) with an authenticated cluster-membership service surface and structurally corrected anomaly signals.

---

## Table of Contents

1. [Document Header](#c32----seismographic-sentinel-master-technical-specification)
2. [Abstract](#abstract)
3. [Table of Contents](#table-of-contents)
4. [Introduction and Motivation](#4-introduction-and-motivation)
   - 4.1 [The Detection Gap](#41-the-detection-gap)
   - 4.2 [Why Per-Spec Detection Is Insufficient](#42-why-per-spec-detection-is-insufficient)
   - 4.3 [The Seismographic Analogy](#43-the-seismographic-analogy)
   - 4.4 [Relationship to Existing Defenses](#44-relationship-to-existing-defenses)
   - 4.5 [What C35 Uniquely Provides](#45-what-c32-uniquely-provides)
5. [Architecture Overview](#5-architecture-overview)
   - 5.1 [Three-Tier Hierarchy](#51-three-tier-hierarchy)
   - 5.2 [Epoch Alignment](#52-epoch-alignment)
   - 5.3 [Cross-Layer Integration Map](#53-cross-layer-integration-map)
   - 5.4 [Scaling Targets and Complexity Bounds](#54-scaling-targets-and-complexity-bounds)
   - 5.5 [Sentinel Health Meta-Signal](#55-sentinel-health-meta-signal)
6. [Tier 1 -- Per-Agent Local Detection](#6-tier-1----per-agent-local-detection)
   - 6.1 [Narrative Overview](#61-narrative-overview)
   - 6.2 [Metric Channels](#62-metric-channels)
   - 6.3 [STA/LTA Computation](#63-stalte-computation)
   - 6.4 [Fixed Baseline](#64-fixed-baseline)
   - 6.5 [Adaptive Baseline](#65-adaptive-baseline)
   - 6.6 [Decision Fusion: OR-Trigger with Confirmation Window](#66-decision-fusion-or-trigger-with-confirmation-window)
   - 6.7 [Dual-Trigger Bypass](#67-dual-trigger-bypass)
   - 6.8 [Escalation Protocol](#68-escalation-protocol)
   - 6.9 [Degradation Behavior and Sentinel Health Impact](#69-degradation-behavior-and-sentinel-health-impact)
   - 6.10 [Per-Agent State Model and Memory Budget](#610-per-agent-state-model-and-memory-budget)
   - 6.11 [Tier 1 Formal Properties](#611-tier-1-formal-properties)
7. [Tier 2 -- Regional Correlation Analysis](#7-tier-2----regional-correlation-analysis)
   - 7.1 [Narrative Overview](#71-narrative-overview)
   - 7.2 [Neighborhood Computation](#72-neighborhood-computation)
   - 7.3 [Permitted Correlation Model (PCM)](#73-permitted-correlation-model-pcm)
   - 7.4 [MIDAS Streaming Edge Detection](#74-midas-streaming-edge-detection)
   - 7.5 [Channel Definitions](#75-channel-definitions)
   - 7.6 [Channel Fusion: 3-of-4 Quorum](#76-channel-fusion-3-of-4-quorum)
   - 7.7 [C12 AVAP Pre-Confirmed Edge Injection](#77-c12-avap-pre-confirmed-edge-injection)
   - 7.8 [Escalation to Tier 3](#78-escalation-to-tier-3)
   - 7.9 [Per-Neighborhood State Model and Memory Budget](#79-per-neighborhood-state-model-and-memory-budget)
8. [Tier 3 -- Epidemiological Backward Tracing](#8-tier-3----epidemiological-backward-tracing)
   - 8.1 [Narrative Overview](#81-narrative-overview)
   - 8.2 [Activation Conditions](#82-activation-conditions)
   - 8.3 [Overdispersion Analysis](#83-overdispersion-analysis)
   - 8.4 [Backward Tracing Through Two Sources](#84-backward-tracing-through-two-sources)
   - 8.5 [Attribution Report Format](#85-attribution-report-format)
   - 8.6 [Sample Size Management](#86-sample-size-management)
   - 8.7 [DORMANT/ACTIVE Lifecycle](#87-dormantactive-lifecycle)

*Part 2 continues with: Cross-Layer Integration Contracts, Parameter Registry, Formal Properties and Invariants, Security Architecture, Scalability Analysis, and Appendices.*

---

## 4. Introduction and Motivation

### 4.1 The Detection Gap

The Atrahasis Agent System is a distributed platform where autonomous verification agents produce claims, evaluate evidence, form committees, and settle economic outcomes across six architectural layers. Each layer has its own integrity mechanisms. C5 (PCVM) validates claims through Subjective Logic opinion aggregation and VTD evidence chains. C12 (AVAP) detects collusion through honeypot claims, sealed submissions, and deterrence payments. C17 (MCSD Layer 2) identifies Sybil agents through pairwise behavioral similarity fingerprinting. C13 (CRP+) resists consolidation poisoning through content-addressable triangulation.

These defenses are effective within their domains. They are also fundamentally *reactive* and *domain-specific*. C12 catches collusion rings -- but only after the ring has formed and produced detectable co-voting patterns. C17 flags behavioral clones -- but only when behavioral similarity exceeds its threshold and the SEB probing schedule happens to test the right task categories. C5 detects claim-level anomalies -- but has no visibility into whether the anomaly is isolated or part of a coordinated campaign spanning multiple agents, neighborhoods, and claim classes.

What no existing component provides is *continuous, population-wide, structurally corrected* anomaly surveillance. More than ten AAS specifications reference "anomaly detection" as a dependency or assumed capability -- C3 expects scheduling anomaly signals for its Emergent Trust Regime, C8 expects economic anomaly flags for settlement gating, C14 expects cluster membership data for governance decisions -- yet no specification defines the detection substrate that produces these signals. C35 is that substrate.

### 4.2 Why Per-Spec Detection Is Insufficient

The fragmentation problem is not merely administrative. Per-spec detection fails in three specific ways that a unified system addresses.

**No structural correction.** When C17 reports that agents A and B have high behavioral similarity (B = 0.75), this may indicate Sybil kinship -- or it may indicate that A and B are assigned to the same settlement parcel, verify the same claim classes, operate in the same tidal phase, and were registered in the same epoch cohort. Their behavioral similarity is *structurally expected*. Without a model of what correlation the platform structure produces, every correlated pair triggers alerts, and the defense system drowns in false positives. At 10,000 agents with an average neighborhood of 27, there are approximately 132,000 agent pairs. Even a 1% false positive rate produces 1,320 alerts per epoch -- far more than any triage system can process.

**No cross-domain correlation.** C5 sees verification anomalies. C8 sees economic anomalies. C17 sees behavioral anomalies. None of them sees the *conjunction*: agent A has elevated verification latency (C5), correlated settlement patterns with agent B (C8), and high behavioral similarity to agents C and D (C17). Individually, each signal is below threshold. Together, they constitute strong evidence of coordinated manipulation. Cross-domain fusion requires a system that ingests all four signal types and evaluates their joint probability.

**No epidemiological attribution.** Existing defenses detect anomalies and respond to them. None asks the deeper question: *why* are these agents anomalous? Is there a common operator? A shared infrastructure provider? A systematic vulnerability that multiple adversaries independently exploit? Attribution requires backward tracing through the platform's interaction history -- a fundamentally different analytical operation from forward detection. Without attribution, the system treats each anomaly as independent, missing the campaign-level structure that transforms isolated incidents into coordinated threats.

### 4.3 The Seismographic Analogy

The design draws its name and structure from seismographic networks. A seismograph station measures local ground vibration. A regional network correlates readings across stations to distinguish earthquakes from trucks, construction, and ocean waves. A global synthesis identifies tectonic patterns and locates epicenters.

C35 mirrors this hierarchy. Tier 1 is the local station: each agent has an STA/LTA ratio monitor that detects behavioral vibrations against two baselines. Tier 2 is the regional network: spectral neighborhoods group agents, and the Permitted Correlation Model separates "structural tremor" (correlation explained by platform features) from "anomalous seismic events" (unexplained residual correlation). Tier 3 is the epicenter locator: epidemiological backward tracing identifies the common source of anomalous activity.

The analogy is not decorative. It encodes three design principles that distinguish C35 from threshold-based alert systems. First, *progressive filtering*: most behavioral variation is normal, and most correlations are structural. The system must filter aggressively at each tier to avoid overwhelming the next. Second, *baseline correction*: raw measurements are meaningless without a model of what "normal" looks like at the measurement point. The fixed baseline, the adaptive baseline, and the PCM each provide correction at different temporal and structural scales. Third, *attribution over detection*: the highest-value output is not "something is wrong" but "here is the probable cause and evidence chain."

### 4.4 Relationship to Existing Defenses

C35 complements rather than replaces the existing defense stack.

**C11 (CACT -- VTD Forgery Defense)** detects fabricated verification evidence. C35's Tier 1 ingests verification latency and acceptance rate from C5, which includes CACT-validated outcomes. C35 does not duplicate CACT's evidence-chain analysis; it uses CACT's outputs as behavioral signals.

**C12 (AVAP -- Collusion Defense)** detects collusion rings through mechanism-specific tests. C35's Tier 2 accepts AVAP-confirmed collusion edges as pre-confirmed triggers (Section 7.7), bypassing its own channel fusion. In the reverse direction, C35 provides Tier 2 and Tier 3 anomaly reports to AVAP for correlation with its own ring detection. The two systems are synergistic: AVAP catches mechanism-specific collusion, C35 catches anomalous correlation patterns that may indicate collusion not yet detected by AVAP's specific tests.

**C13 (CRP+ -- Consolidation Poisoning Defense)** operates at the knowledge consolidation layer. C35 has no direct integration with C13 (C6 integration was removed as scope creep during simplification review). C13 and C35 operate independently; their coverage overlaps only when consolidation poisoning produces behavioral anomalies detectable by C35's Tier 1 metrics.

**C17 (MCSD Layer 2 -- Behavioral Similarity)** provides the pairwise B(a_i, a_j) scores that are one of Tier 2's four analysis channels and a primary data source for Tier 3 backward tracing. C17 detects Sybil pairs; C35 provides the structural correction (PCM) that distinguishes true Sybil similarity from platform-induced similarity.

### 4.5 What C35 Uniquely Provides

Three capabilities exist nowhere else in the AAS architecture.

**PCM structural correction.** The Permitted Correlation Model computes expected pairwise correlation from five structural covariates (parcel colocation, committee coassignment, epoch coregistration, claim class overlap, tidal phase alignment). By subtracting this expected correlation from observed values, C35 isolates the *unexplained residual* -- the signal that warrants investigation. No other AAS component performs structural correction on pairwise behavioral data. Without PCM, any system operating on raw similarity scores inherits C17's false positive problem at scale.

**Cluster membership API.** C35 computes spectral neighborhoods and exposes them through an authenticated internal service interface that attested AAS components can query. This provides a canonical, structurally grounded grouping of agents that C3 uses for scheduling decisions, C5 uses for verification routing, C8 uses for settlement risk assessment, and C12 uses for collusion ring context. The cluster membership API is referenced by more downstream specifications than any other C35 output.

**Epidemiological attribution.** Tier 3's backward tracing identifies the common causal source of anomaly clusters -- the operator, infrastructure provider, or systematic vulnerability that explains why a group of agents behaves anomalously. No other AAS component performs causal attribution. C12 detects collusion but does not attribute it to a common source. C17 detects similarity but does not trace its origin. Tier 3's attribution reports feed the governance layer (C14) with evidence-grade causal chains that support Citicate review and Constitutional Tribunal proceedings.

---

## 5. Architecture Overview

### 5.1 Three-Tier Hierarchy

C35 is organized into three tiers with strictly increasing scope, latency, and analytical depth. Data flows upward through the tiers. No tier sends data downward except configuration parameters and threshold updates.

```
+==============================================================================+
|                    SEISMOGRAPHIC SENTINEL -- C35                              |
|                                                                              |
|  +------------------------------------------------------------------------+  |
|  |               TIER 3 -- EPIDEMIOLOGICAL BACKWARD TRACING               |  |
|  |                                                                        |  |
|  |  Overdispersion Analysis  -->  Backward Tracing  -->  Attribution      |  |
|  |  (Cameron & Trivedi NB)       (C17 + C7 sources)     Report           |  |
|  |                                                                        |  |
|  |  Activation: >=15 confirmed anomalies in 10-epoch window               |  |
|  |  Concurrency: max 3 concurrent analyses                                |  |
|  +-------------------------------+----------------------------------------+  |
|                                  ^ Tier 2 escalation                         |
|  +-------------------------------+----------------------------------------+  |
|  |               TIER 2 -- REGIONAL CORRELATION ANALYSIS                  |  |
|  |                                                                        |  |
|  |  Spectral       PCM-Augmented        Channel Fusion                    |  |
|  |  Neighborhoods   MIDAS Edge           3-of-4 Quorum                    |  |
|  |  (NMI-hardened)  Detection             (Bayesian deferred)             |  |
|  |                  R = obs - E[PCM]                                      |  |
|  |                                                                        |  |
|  |  Per-neighborhood coordinator receives Tier 1 triggers                 |  |
|  +-------------------------------+----------------------------------------+  |
|                                  ^ Tier 1 triggers (confirmed only)          |
|  +-------------------------------+----------------------------------------+  |
|  |               TIER 1 -- PER-AGENT LOCAL DETECTION                      |  |
|  |                                                                        |  |
|  |  4-Channel Metric Ingestion (every SETTLEMENT_TICK = 60s)              |  |
|  |    verification_latency (C5)    claim_acceptance_rate (C5)             |  |
|  |    committee_frequency  (C3)    behavioral_consistency (C17)           |  |
|  |                                                                        |  |
|  |  STA/LTA Ratio  -->  Decision Fusion  -->  Escalation Protocol         |  |
|  |  (dual baseline)     (OR-trigger +         (annotated trigger to       |  |
|  |                       confirmation +        neighborhood coordinator)   |  |
|  |                       dual-trigger bypass)                              |  |
|  +------------------------------------------------------------------------+  |
|                                                                              |
|  SENTINEL HEALTH META-SIGNAL: sentinel_health in [0.0, 1.0]                 |
|  (consumers discount C35 outputs when sentinel_health < 1.0)                |
|                                                                              |
|  CROSS-LAYER INPUTS                                                          |
|  +------+ +------+ +------+ +------+ +------+ +------+                      |
|  |  C3  | |  C5  | |  C7  | |  C8  | |  C12 | |  C17 |                      |
|  |Tidal | |PCVM  | | RIF  | | DSF  | |AVAP  | |MCSD  |                      |
|  +------+ +------+ +------+ +------+ +------+ +------+                      |
+==============================================================================+
```

| Tier | Scope | Cadence | Complexity | Function |
|------|-------|---------|------------|----------|
| **Tier 1** | Per-agent | Every SETTLEMENT_TICK (60s) | O(V) per tick | Local anomaly detection via STA/LTA ratio and dual-baseline comparison |
| **Tier 2** | Per-neighborhood | Every TIDAL_EPOCH (3600s) | O(V log V) amortized | Regional correlation analysis via PCM residuals and MIDAS edge detection |
| **Tier 3** | System-wide | On-demand (Tier 2 escalation) | O(V log V) typical | Epidemiological attribution via overdispersion analysis and backward tracing |

**V** denotes total agent population. Tier 1 processes every agent every tick. Tier 2 processes agent pairs within spectral neighborhoods at epoch boundaries. Tier 3 activates only when Tier 2 produces a statistically significant anomaly cluster.

### 5.2 Epoch Alignment

C35 aligns with the canonical three-tier epoch hierarchy established by C9 Cross-Layer Reconciliation.

| Epoch Level | Duration | C35 Function |
|-------------|----------|--------------|
| SETTLEMENT_TICK | 60 seconds | Tier 1 per-agent metric ingestion, STA/LTA computation, trigger evaluation |
| TIDAL_EPOCH | 3,600 seconds (60 ticks) | Tier 2 batch neighborhood correlation analysis, adaptive baseline update aggregation |
| CONSOLIDATION_CYCLE | 36,000 seconds (600 ticks, 10 epochs) | Neighborhood recomputation (spectral clustering), PCM parameter refit |

Derived cadences within C35:

| Event | Cadence | Duration |
|-------|---------|----------|
| STA window refresh | Every tick | w_s = 5 ticks = 300s sliding window |
| LTA window refresh | Every tick | w_l = 60 ticks = 3,600s sliding window |
| Adaptive baseline EMA update | Every tick | alpha = 0.01 per tick |
| Tier 1 confirmation window | 3-5 ticks | 180s-300s depending on density regime |
| Tier 2 batch analysis | Every TIDAL_EPOCH | 3,600s periodic |
| Neighborhood partition recomputation | Every CONSOLIDATION_CYCLE | 36,000s periodic |
| PCM parameter refit | Every CONSOLIDATION_CYCLE | 36,000s periodic |
| Fixed baseline calibration | Once (first 100 epochs) | 360,000s total (~4.17 days) |

### 5.3 Cross-Layer Integration Map

C35 maintains 6 cross-layer integration contracts. (C6 EMA integration was removed during simplification review as non-essential scope creep; C6 may consume the authenticated cluster-membership service if needed.)

| # | Contract | Direction | Primary Data | Cadence | Failure Mode |
|---|----------|-----------|-------------|---------|--------------|
| XL-1 | C3 (Tidal Noosphere) | Bidirectional | committee_frequency per agent; tidal phase; 1 composite ETR signal out | Per-tick (metric), per-cycle (structural) | Cached value; DEGRADED after 100 stale ticks |
| XL-2 | C5 (PCVM) | Bidirectional | verification_latency, acceptance_rate per agent; anomaly flags out | Per-tick | Cached value; DEGRADED after 100 stale ticks |
| XL-4 | C7 (RIF) | Bidirectional | Infrastructure channel metrics in; Tier 3 response actions out | Per-tick (metric), event-driven (response) | Response actions queued; infrastructure channel cached |
| XL-5 | C8 (DSF) | C8 to C35 | settlement_pattern, staking_behavior, reward_timing per agent | Per-tick (metric), per-cycle (structural) | Cached value; DEGRADED after 100 stale ticks |
| XL-6 | C12 (AVAP) | Bidirectional | AVAP-confirmed collusion edges in; anomaly reports out | Event-driven | C12 edges bypass fusion when available; absence does not degrade C35 |
| XL-7 | C17 (MCSD L2) | C17 to C35 | B(a_i, a_j) pairwise similarity; behavioral_consistency self-metric | Per-epoch (batch), per-cycle (structural) | Critical for Tier 2 PCM; fallback to raw correlation if unavailable >1 cycle |

The ETR signal export to C3 is simplified to a single composite anomaly signal (per simplification S-15), replacing the three bespoke signals (skew_metric, starvation_flag, divergence_metric) specified in the architecture. C3 can derive scheduling-specific signals from the composite or from C35's standard per-agent anomaly-level service endpoint.

### 5.4 Scaling Targets and Complexity Bounds

| Scale | Agents (V) | Neighborhoods (k) | Avg Neighborhood Size | Pairs per Neighborhood | Total Pairs |
|-------|-----------|-------------------|----------------------|----------------------|-------------|
| Small | 1,000 | 51 | 19.6 | 190 | ~9,700 |
| Medium | 10,000 | 377 | 26.5 | 351 | ~132,000 |
| Large | 100,000 | 3,013 | 33.2 | 561 | ~1,690,000 |

Per-tick compute budget constraint: all Tier 1 processing must complete within 0.2% of SETTLEMENT_TICK (120ms at 60s tick). At V = 100,000, this allows 1.2 microseconds per agent -- sufficient for the O(1) per-agent STA/LTA and trigger evaluation.

Per-cycle compute budget: spectral clustering and PCM refit at CONSOLIDATION_CYCLE must complete within 1% of cycle time (360 seconds out of 36,000). At V = 100,000, spectral clustering requires ~30 seconds (Lanczos iterative eigensolver), NMI hardening adds ~30 seconds, and PCM refit requires ~25 seconds (parallelized across 8 cores). Total: ~85 seconds, well within budget.

### 5.5 Sentinel Health Meta-Signal

C35 publishes a `sentinel_health` meta-signal in the range [0.0, 1.0] that quantifies the system's own operational integrity. This addresses the self-referential anomaly problem identified in Design Flag DF-2: when C35 itself is operating in degraded mode (stale data, missing sources, fallback behaviors active), its anomaly outputs may be artifacts of its own degradation rather than genuine platform threats.

**Computation:**

```
sentinel_health = w_src * source_health
               + w_pop * population_coverage
               + w_pcm * pcm_coverage
               + w_fresh * data_freshness
```

where:
- `source_health` = fraction of 6 cross-layer sources currently responsive (each source is 0 or 1)
- `population_coverage` = fraction of agents NOT in DEGRADED state
- `pcm_coverage` = fraction of neighborhoods where PCM R-squared >= 0.70 on at least 3 of 4 channels
- `data_freshness` = 1.0 - (max_stale_ticks_any_source / 100), clamped to [0.0, 1.0]
- Weights: w_src = 0.30, w_pop = 0.30, w_pcm = 0.20, w_fresh = 0.20

**Self-referential anomaly suppression.** When `sentinel_health` < 0.80, C35 applies two protective measures:

1. **Output discounting.** All anomaly confidence scores emitted by Tier 1 and Tier 2 are multiplied by `sentinel_health`. A confidence of 0.90 when sentinel_health = 0.60 becomes an effective confidence of 0.54 -- below most consumer thresholds.

2. **Self-attribution check.** If the onset of new Tier 2 anomalies coincides with a `sentinel_health` drop (sentinel_health decreased by more than 0.10 within the past 2 CONSOLIDATION_CYCLEs), the anomalies are tagged as `POSSIBLY_SELF_INDUCED`. These tagged anomalies are logged but excluded from Tier 3 escalation counting and from the ETR composite signal to C3.

**Publication.** `sentinel_health` is published at every TIDAL_EPOCH boundary via the authenticated cluster-membership service. All authorized consumers (C3, C5, C7, C8, C12, C17) receive it alongside cluster data and can independently decide how to weight C35 outputs during degraded operation.

---

## 6. Tier 1 -- Per-Agent Local Detection

### 6.1 Narrative Overview

Tier 1 is the innermost detection ring. Every registered agent in the AAS has an independent Tier 1 monitor that runs at every SETTLEMENT_TICK. The monitor ingests four behavioral metrics from cross-layer sources, maintains two baselines (a fixed reference from calibration and an adaptive tracker of recent behavior), computes the ratio of short-term to long-term averages on each metric channel, and evaluates whether the agent's current behavior deviates sufficiently from expectations to warrant regional analysis.

The core technique is the STA/LTA ratio, borrowed from seismology. The Short-Term Average captures what the agent is doing *right now* (last 5 ticks, 5 minutes). The Long-Term Average captures what the agent has been doing *recently* (last 60 ticks, 1 hour). When the ratio deviates significantly from 1.0, something has changed. But change alone is not evidence of threat -- agents legitimately change behavior when claim types shift, when tidal phases rotate, when infrastructure is upgraded. The dual-baseline design addresses this: the fixed baseline catches long-term drift invisible to the adaptive tracker, while the adaptive baseline catches sudden shifts that fall within the fixed baseline's wide calibration range.

Tier 1 is intentionally imprecise. Its target false positive rate is 1-5% of agents per epoch, deliberately non-trivial. Tier 1's job is sensitivity, not specificity. It must not miss genuine anomalies even at the cost of flagging benign behavioral shifts. Tier 2's structural correction handles the precision problem.

### 6.2 Metric Channels

Tier 1 monitors four metric channels, each derived from a cross-layer data source. All values are normalized to the [0, 1] range using min-max scaling calibrated during the fixed baseline calibration period.

**Channel 0: Verification Latency.** Source: C5 PCVM (contract XL-2). Mean time between claim assignment and opinion submission by the agent, measured over the most recent SETTLEMENT_TICK. Normalized by dividing by the P99 calibration latency.

```
m_0(a_i, t) = mean_latency(a_i, t) / P99_latency_calibration(a_i)
```

Sudden increases may indicate computational distress, deliberate stalling, or model degradation. Sudden decreases may indicate claim rubber-stamping or pre-computed answer injection. Values above 1.0 are clipped for ratio computation but preserved in raw annotations for Tier 2.

**Channel 1: Claim Acceptance Rate.** Source: C5 PCVM (contract XL-2). Fraction of claims for which the agent submitted a positive verification opinion (belief > 0.5 in Subjective Logic tuple) during the most recent tick.

```
m_1(a_i, t) = count(opinions where b > 0.5) / count(all opinions submitted)
```

If no opinions were submitted (agent was not assigned to any committee), the value is carried forward from the previous tick. After 5 consecutive carry-forward ticks, the metric is marked STALE and excluded from trigger computation.

**Channel 2: Committee Frequency.** Source: C3 Tidal Noosphere (contract XL-1). Number of verification committees to which the agent was assigned, normalized by the population mean.

```
m_2(a_i, t) = committees_assigned(a_i, t) / mean_committees_assigned(*, t)
```

If the population mean is zero (no committees system-wide), the value is set to 1.0 (neutral). Anomalies indicate scheduling manipulation or infrastructure availability problems.

**Channel 3: Behavioral Consistency.** Source: C17 MCSD L2 (contract XL-7). Self-similarity score comparing the agent's current behavioral profile against its own profile from the previous TIDAL_EPOCH.

```
m_3(a_i, t) = B_self(a_i, T_e, T_e - 1)
```

This is NOT the pairwise B(a_i, a_j) used in Tier 2. It is a self-comparison over time using C17's five-modality distance calculation (temporal, structural, error, resource, lexical). Updates once per TIDAL_EPOCH; between epochs, the last value is held constant. A sudden drop suggests model replacement, infrastructure migration, or adversarial behavior mode switching.

### 6.3 STA/LTA Computation

The Short-Term Average (STA) and Long-Term Average (LTA) are computed independently for each metric channel c in {0, 1, 2, 3}.

**STA (Short-Term Average).** Window size w_s = 5 ticks (300 seconds). Configurable via parameter TIER1_STA_WINDOW_TICKS (range: [3, 15]).

```
STA_c(a_i, t) = (1 / min(w_s, n_valid)) * SUM_{j=0}^{min(w_s, n_valid)-1} m_c(a_i, t - j)
```

Implementation: ring buffer with incremental mean update. After every 100 ticks, the STA is recomputed from scratch to prevent floating-point drift.

**LTA (Long-Term Average).** Window size w_l = 60 ticks (3,600 seconds = 1 TIDAL_EPOCH). Configurable via parameter TIER1_LTA_WINDOW_TICKS (range: [30, 120]).

```
LTA_c(a_i, t) = (1 / min(w_l, n_valid)) * SUM_{j=0}^{min(w_l, n_valid)-1} m_c(a_i, t - j)
```

Implementation: ring buffer with incremental mean update and full recomputation every CONSOLIDATION_CYCLE (600 ticks).

**STA/LTA Ratio.**

```
R_c(a_i, t) = STA_c(a_i, t) / LTA_c(a_i, t)
```

Edge cases:
- LTA_c = 0: R_c is undefined. Channel excluded from trigger computation.
- LTA_c < epsilon (1e-10): R_c capped at R_MAX = 100.0.
- STA_c = 0 and LTA_c > 0: R_c = 0, a valid anomaly signal (sudden activity cessation).

Interpretation: R_c near 1.0 means consistency. R_c significantly above 1.0 means elevated activity. R_c significantly below 1.0 means depressed activity. The absolute deviation |R_c - 1.0| is the anomaly magnitude.

### 6.4 Fixed Baseline

The fixed baseline provides an immutable reference calibrated during the agent's initial observation period. It detects long-term drift that the adaptive baseline (which tracks drift by design) absorbs and misses.

**Calibration period.** Begins at agent registration. Lasts 100 TIDAL_EPOCHS (360,000 seconds, approximately 4.17 days). During calibration, only the adaptive baseline is active and Tier 1 triggers are suppressed -- no escalation during calibration, preventing bootstrapping noise from polluting Tier 2.

**Calibration computation.** At the end of the 100th epoch, the calibration buffer (up to 6,000 samples per channel) is processed to produce five percentiles per channel:

```
struct FixedBaseline {
    percentiles: [[f64; 5]; 4],  // 4 channels x 5 percentiles (P5, P25, P50, P75, P95)
    sample_count: [u64; 4],
    calibration_epoch: u64,
}
```

Percentiles use nearest-rank computation (no interpolation).

**Immutability.** After calibration completes:
1. The calibration buffer is zeroed and deallocated.
2. The fixed baseline is written once to persistent storage.
3. The fixed baseline is NEVER updated unless an explicit admin override is issued (requires C7 saga authorization with two-party approval per C7 RIF Section 7.2).

This immutability is a conscious design choice: automatic recalibration creates an attack surface where an adversary modifies behavior, waits for recalibration, and then the new baseline accepts adversarial behavior as normal.

**Fixed baseline anomaly detection.** A metric value is anomalous relative to the fixed baseline if it falls outside the P5-P95 range:

```
anomaly_fixed(c, a_i, t) = true  if  m_c(a_i, t) < P5(c)  OR  m_c(a_i, t) > P95(c)
```

Direction tagging: POSITIVE if above P95, NEGATIVE if below P5. Direction is used in the confirmation window sign-agreement check (Section 6.6).

**Note on Laplace noise.** The architecture document specified Laplace noise injection on fixed baseline percentiles for differential privacy. Per simplification review S-10, this mechanism is removed. The primary defense against baseline reconstruction is the combination of (a) 5% multiplicative threshold jitter per tick and (b) binary-only feedback to agents. The Red Team analysis (FC-3) demonstrates that reconstruction requires approximately 10,000 sustained probing transactions (116+ hours), by which point the probing itself triggers Tier 1 independently. Laplace noise degraded baseline accuracy (post-noise clamping compressed the P5-P95 range) for marginal privacy benefit already provided by other mechanisms.

### 6.5 Adaptive Baseline

The adaptive baseline tracks evolving normal behavior using an exponential moving average (EMA). Unlike the fixed baseline, it absorbs gradual drift -- a model upgrade that increases latency by 10% over 30 epochs will be incorporated.

**EMA update (every tick):**

```
AB_c(a_i, t) = alpha * m_c(a_i, t) + (1 - alpha) * AB_c(a_i, t-1)
```

alpha = 0.01 (configurable via TIER1_ADAPTIVE_ALPHA, range [0.001, 0.1]).

Half-life at alpha = 0.01: t_half = -ln(2) / ln(0.99) = 69.0 ticks = 4,140 seconds (approximately 1.15 hours). A sustained behavioral shift is >95% absorbed within approximately 300 ticks (5 hours).

Initialization: AB_c(a_i, registration_tick) = m_c(a_i, registration_tick).

Staleness handling: if m_c is STALE, the EMA is not updated; the previous value is retained.

**Adaptive baseline anomaly detection:**

```
anomaly_adaptive(c, a_i, t) = true  if  |R_c(a_i, t) - 1.0| > theta_c
```

Per-channel thresholds theta_c:

| Channel | theta_c (default) | Rationale |
|---------|-------------------|-----------|
| c=0: verification_latency | 0.40 | Latency is noisy; 40% deviation required |
| c=1: claim_acceptance_rate | 0.25 | Acceptance rate is more stable; 25% sufficient |
| c=2: committee_frequency | 0.50 | Frequency varies widely with scheduling; generous threshold |
| c=3: behavioral_consistency | 0.20 | Self-similarity is very stable; small deviations significant |

All configurable via TIER1_THETA_LATENCY, TIER1_THETA_ACCEPTANCE, TIER1_THETA_COMMITTEE, TIER1_THETA_CONSISTENCY (range [0.05, 1.0] each).

Direction tagging: POSITIVE if R_c - 1.0 > theta_c; NEGATIVE if R_c - 1.0 < -theta_c.

### 6.6 Decision Fusion: OR-Trigger with Confirmation Window

The decision fusion engine resolves the interaction between the two baselines. This is the formal specification of FC-2 (Feasibility Condition 2).

The challenge: the two baselines serve different purposes. The fixed baseline detects absolute deviation from calibration-era behavior. The adaptive baseline detects deviation from recent behavior. They can disagree. An agent that has gradually drifted far from its calibration profile triggers the fixed baseline constantly but never the adaptive. A sudden spike within the calibration range triggers the adaptive but not the fixed.

The resolution is an OR-trigger (either baseline firing enters CANDIDATE state) with a confirmation window (persistence required before escalation) and a dual-trigger bypass (both baselines agreeing skips the window).

**Step 1: CANDIDATE trigger.** Either baseline exceeding its threshold on ANY channel fires a CANDIDATE:

```
candidate_trigger(a_i, t) = anomaly_fixed(c, a_i, t)  OR  anomaly_adaptive(c, a_i, t)
    for ANY channel c in {0, 1, 2, 3}
```

On entry to CANDIDATE: trigger_state transitions from IDLE to CANDIDATE; candidate_tick = t; candidate_baseline records which baseline(s) triggered; candidate_metrics captures the metric snapshot; confirmation_count = 0.

**Step 2: Confirmation window.** The anomaly must persist with sign agreement for a configurable duration.

Window duration is derived from a single base parameter (base_confirmation_window = 3, configurable range [2, 7]) using the density-adaptive rule:

```
confirmation_required = base_confirmation_window + floor(density_z_score)
```

where density_z_score is:

```
density_z_score = max(0, (trigger_rate(t) - mean_trigger_rate_100) / sigma_trigger_rate_100)
```

At z=0 (normal density): window = 3 ticks (180s). At z=2 (high density): window = 5 ticks (300s). At z=4 (extreme density): window = 7 ticks (420s). This collapses three architecture parameters into one while preserving adaptive behavior.

**Step 3: Sign agreement with relaxation.** At each tick t' within the confirmation window:

```
confirmed_tick(a_i, t') = true  if:
    EXISTS channel c such that:
        [anomaly_fixed(c) OR anomaly_adaptive(c)]
        AND sign_agree(direction_fixed, direction_adaptive)
```

The sign agreement rule with relaxation factor alpha_confirm = 0.7:

| Fixed Direction | Adaptive Direction | Result |
|-----------------|-------------------|--------|
| D | D (same) | Accepted |
| NONE | D (any) | Accepted (one-sided agreement) |
| D (any) | NONE | Accepted (one-sided agreement) |
| POSITIVE | NEGATIVE | Rejected (contradiction) |
| NEGATIVE | POSITIVE | Rejected (contradiction) |

When both baselines trigger, a magnitude relaxation applies: the weaker anomaly must be at least alpha_confirm (0.70) times the stronger:

```
IF both trigger:
    mag_fixed = |m_c - P50(c)| / (P95(c) - P5(c))
    mag_adaptive = |R_c - 1.0| / theta_c
    stronger = max(mag_fixed, mag_adaptive)
    weaker = min(mag_fixed, mag_adaptive)
    confirmation_accepted = (weaker / stronger) >= alpha_confirm
```

If confirmed_tick is true, confirmation_count increments.

**Step 4: Resolution.**

```
IF confirmation_count >= confirmation_required:
    trigger_state -> CONFIRMED  (escalate to Tier 2)

IF t - candidate_tick > confirmation_required + 2:
    trigger_state -> IDLE  (window expired, candidate discarded)
```

The +2 grace period allows up to 2 ticks of STALE data within the window before discarding.

### 6.7 Dual-Trigger Bypass

If BOTH baselines exceed their thresholds simultaneously on the SAME channel with the SAME direction, the confirmation window is bypassed:

```
dual_trigger_bypass(a_i, t) = true  if:
    EXISTS channel c such that:
        anomaly_fixed(c, a_i, t) = true  with direction D
        AND anomaly_adaptive(c, a_i, t) = true  with direction D
        AND D_fixed = D_adaptive  (strict equality, no relaxation)
```

When dual-trigger bypass fires, trigger_state transitions directly from IDLE to CONFIRMED. Immediate Tier 2 escalation. No confirmation window.

**Rationale.** Both the immutable calibration baseline and the adaptive recent baseline detecting the same anomaly on the same metric in the same direction is strong evidence of genuine behavioral shift. The probability of false dual-trigger is approximately P(fixed) * P(adaptive) * P(same direction) per channel per tick.

**False alarm mitigation.** If empirical false alarm rates prove unacceptable during W0 validation, the dual-trigger bypass can be restricted to require 2 or more channels simultaneously exceeding both baselines (parameter TIER1_DUAL_TRIGGER_MIN_CHANNELS, default 1, range [1, 4]).

### 6.8 Escalation Protocol

When a Tier 1 trigger is confirmed, the monitor emits a TriggerAnnotation to the neighborhood coordinator responsible for the agent.

```
struct TriggerAnnotation {
    agent_id:               AgentID,
    trigger_tick:           u64,
    candidate_tick:         u64,
    metric_values:          [f64; 4],         // Current values at trigger_tick
    metric_values_candidate: [f64; 4],        // Values when CANDIDATE entered
    baseline_source:        BaselineSource,   // FIXED | ADAPTIVE | BOTH
    triggering_channels:    [bool; 4],
    directions:             [Direction; 4],   // POSITIVE | NEGATIVE | NONE per channel
    sta_values:             [f64; 4],
    lta_values:             [f64; 4],
    sta_lta_ratios:         [f64; 4],
    confidence:             f64,
    bypass_used:            bool,
    density_regime:         DensityRegime,    // NORMAL | HIGH_DENSITY
}
```

**Confidence score.** Derived from channel thresholds (per simplification S-03) rather than independently tuned weights. Each channel's contribution is weighted by the inverse of its threshold, normalized:

```
w_c = (1 / theta_c) / SUM_c (1 / theta_c)
```

At default thresholds (0.40, 0.25, 0.50, 0.20):
- w_0 (latency) = 2.50 / 13.50 = 0.185
- w_1 (acceptance) = 4.00 / 13.50 = 0.296
- w_2 (committee) = 2.00 / 13.50 = 0.148
- w_3 (consistency) = 5.00 / 13.50 = 0.370

This gives highest weight to the channels with tightest thresholds (behavioral_consistency, claim_acceptance_rate) and lowest weight to the noisiest channel (committee_frequency). The weights are principled and automatically adjust if thresholds are retuned.

```
confidence(a_i, t) = SUM_c (w_c * anomaly_strength_c) / SUM_c w_c
```

where anomaly_strength_c is 0.0 for non-triggering channels and the normalized anomaly magnitude for triggered channels.

**Delivery.** The annotation is delivered via the C7 RIF intra-platform message bus (contract XL-4). If undeliverable after 100 ticks (TIER1_ESCALATION_BUFFER_TICKS), the annotation is logged to the local audit trail with status ESCALATION_FAILED and discarded. Tier 1 returns to IDLE regardless of delivery success -- it does not block on Tier 2 availability.

**Post-escalation.** After emitting, trigger_state returns to IDLE. No cooldown period. If the anomaly persists, the agent re-triggers on subsequent ticks, providing Tier 2 with a stream of corroborating evidence.

### 6.9 Degradation Behavior and Sentinel Health Impact

Tier 1 degrades gracefully when cross-layer data sources are unavailable.

**Metric source unavailability:**

1. **First 100 ticks (up to 1.67 hours):** Last received value cached. STA and LTA update with cached value (tagged CACHED in ring buffer). Triggers include cached_channels bitmask in annotations.

2. **After 100 consecutive stale ticks:** Channel marked STALE and excluded from trigger computation. If ALL four channels STALE, agent transitions to calibration_status = DEGRADED. Trigger_state forced to IDLE. DegradationNotice sent to neighborhood coordinator.

3. **Neighborhood impact:** If >30% of agents in a neighborhood are DEGRADED, the coordinator escalates NEIGHBORHOOD_DEGRADED to Tier 3.

**Partial channel availability:**

| Available Channels | Trigger Behavior |
|---|---|
| 4 of 4 | Normal operation |
| 3 of 4 | Normal with reweighted confidence |
| 2 of 4 | Reduced sensitivity. Confirmation window extended to 5 ticks. Dual-trigger bypass disabled. |
| 1 of 4 | Minimal operation. Confirmation = 7 ticks. Bypass disabled. Confidence capped at 0.5. |
| 0 of 4 | DEGRADED. No detection. Agent excluded. |

**Sentinel health interaction.** When C35's own data sources are degraded (sentinel_health < 0.80), anomaly signals that could be artifacts of the degradation are suppressed. Specifically:

- Confidence scores are multiplied by sentinel_health before emission.
- If sentinel_health dropped by >0.10 in the past 2 CONSOLIDATION_CYCLEs, new Tier 1 triggers are tagged POSSIBLY_SELF_INDUCED and excluded from Tier 3 escalation counts.

This prevents a feedback cascade where C35's own degradation produces anomaly signals that trigger downstream responses that further degrade C35's inputs.

### 6.10 Per-Agent State Model and Memory Budget

The canonical per-agent state model (reconciling architecture Sections 2.2 and 6.1 per Design Flag DF-3):

| Component | Size | Notes |
|-----------|------|-------|
| MetricIngestor (current tick buffer) | 64 bytes | 4 channels x 8 bytes x 2 (value + status) |
| STAWindow (ring buffer) | 160 bytes | 4 channels x 5 ticks x 8 bytes |
| LTAWindow (ring buffer) | 1,920 bytes | 4 channels x 60 ticks x 8 bytes |
| FixedBaseline | 160 bytes | 4 channels x 5 percentiles x 8 bytes |
| AdaptiveBaseline (EMA state) | 32 bytes | 4 channels x 8 bytes |
| TriggerState + metadata | 48 bytes | State enum, window counter, pending annotation |
| DecisionFusionEngine (config) | 16 bytes | Configuration pointers |
| **Total per agent (post-calibration)** | **2,400 bytes** | |

During calibration only, an additional CalibrationBuffer is allocated: up to 6,000 samples x 4 channels x 8 bytes = 192 KB. This is deallocated after calibration completes.

**LTA window size is 60 ticks** (1 TIDAL_EPOCH), consistent with Section 2.4.2 of the architecture. The 600-entry allocation appearing in architecture Section 6.1 was an error (600 ticks = 1 CONSOLIDATION_CYCLE, which is the PCM refit cadence, not the LTA window). This reconciliation resolves Design Flag DF-3.

**Memory at scale (Tier 1 only):**

| Scale | Agents | Tier 1 Memory | Calibrating Agents (peak) | Calibration Memory (peak) |
|-------|--------|---------------|---------------------------|---------------------------|
| 1K | 1,000 | 2.4 MB | ~50 | 9.6 MB |
| 10K | 10,000 | 24 MB | ~500 | 96 MB |
| 100K | 100,000 | 240 MB | ~5,000 | 960 MB |

The calibration memory peak assumes up to 5% of agents are simultaneously in the 4.17-day calibration period. This peak is transient and drops to zero once all agents complete calibration.

### 6.11 Tier 1 Formal Properties

**PROP-T1-1 (Bounded Latency).** Tier 1 processing for a single agent completes in O(1) time per tick, independent of population size V. The only V-dependent operation is the high-density mode check, which uses pre-computed rolling statistics.

**PROP-T1-2 (Memory Bound).** Tier 1 memory per agent is bounded by 2,400 bytes post-calibration. During calibration, the CalibrationBuffer adds at most 192 KB per calibrating agent.

**PROP-T1-3 (Monotonic Degradation).** As channels become unavailable, Tier 1 sensitivity decreases monotonically. No channel becoming unavailable can INCREASE the trigger rate (unavailable channels are excluded, not treated as anomalous).

**PROP-T1-4 (Calibration Isolation).** During the calibration period (first 100 epochs), Tier 1 triggers are suppressed. No TriggerAnnotation is emitted. Calibration-era exploration does not pollute Tier 2 correlation analysis.

**PROP-T1-5 (Self-Referential Safety).** When sentinel_health < 0.80, Tier 1 output confidence is multiplicatively reduced. C35 cannot amplify its own degradation into escalation cascades.

---

## 7. Tier 2 -- Regional Correlation Analysis

### 7.1 Narrative Overview

Tier 2 answers the question that Tier 1 cannot: is this agent's anomaly *isolated* or *correlated* with other agents? An isolated anomaly -- a single agent behaving oddly -- may be a software bug, a model upgrade, or benign behavioral exploration. A correlated anomaly -- multiple agents in the same neighborhood deviating simultaneously in related ways -- is the signature of coordinated manipulation, shared infrastructure compromise, or common-operator control.

The challenge is that agents in the same neighborhood are *expected* to be correlated. They share committee assignments, settle in the same parcels, operate in the same tidal phases, verify the same claim classes, and were often registered in the same epoch cohort. Raw pairwise correlation between co-located agents is dominated by this structural signal. If Tier 2 flagged every correlated pair, the system would drown in false positives.

The Permitted Correlation Model (PCM) solves this. It models the *expected* correlation between any two agents based on five structural covariates -- observable features of their platform positions that naturally produce correlated behavior. By subtracting the PCM prediction from the observed correlation, Tier 2 produces a *residual*: the unexplained portion of the correlation. Only residual correlation feeds the MIDAS streaming anomaly detector. Only pairs that are both temporally unusual (MIDAS) and structurally unexplained (PCM residual) pass the joint criterion and enter channel fusion.

The channel fusion engine combines evidence from four analysis channels (verification, behavioral, infrastructure, economic) using a 3-of-4 quorum. A pair must show anomalous residual correlation on at least three independent observation dimensions to be confirmed. This multi-channel requirement provides strong false-positive suppression while maintaining sensitivity to genuine multi-domain threats.

### 7.2 Neighborhood Computation

**Spectral clustering.** Neighborhoods are computed at every CONSOLIDATION_CYCLE (36,000 seconds) via spectral clustering on the agent interaction graph.

The interaction graph G = (V, E, W) is a weighted undirected graph where V = all registered agents with calibration_status != CALIBRATING, E = agent pairs that interacted during the most recent cycle (co-membership in committees, verification of same claims, co-assignment to scheduling units), and W assigns edge weights combining C17 behavioral similarity with structural covariate similarity:

```
W(a_i, a_j) = lambda_B * B(a_i, a_j) + lambda_S * S_struct(a_i, a_j)
```

lambda_B = 0.6, lambda_S = 0.4 (configurable). If B is unavailable for a pair, the weight falls back to S_struct alone.

The normalized graph Laplacian (Ng-Jordan-Weiss formulation) is computed:

```
L_norm = D^{-1/2} * (D - W) * D^{-1/2}
```

The k smallest eigenvectors are computed, where k = ceil(V / (2 * log2(V))):

| V | k (neighborhoods) | Avg agents per neighborhood |
|---|-------------------|---------------------------|
| 1,000 | 51 | 19.6 |
| 10,000 | 377 | 26.5 |
| 100,000 | 3,013 | 33.2 |

The eigenvector matrix (V x k) is clustered via k-means. Implementation must use an iterative eigensolver (Lanczos or LOBPCG) operating on the sparse Laplacian -- full eigendecomposition is infeasible at V = 100,000.

**Cluster size cap and overflow.** Maximum neighborhood size: cap = 2 * log2(V). Overflow clusters are split via recursive Fiedler bisection. Minimum cluster size: 3 agents. Smaller clusters are dissolved and members assigned to nearest qualifying neighbor.

**NMI hardening.** To detect adversarial graph manipulation, the clustering is stability-tested. A perturbed graph G' is created by adding Gaussian noise (sigma_NMI = 0.1) to all edge weights. The clustering of G' is compared to the original via Normalized Mutual Information:

```
NMI(C, C') = 2 * I(C; C') / (H(C) + H(C'))
```

If NMI >= 0.70: clustering accepted. If NMI < 0.70: previous cycle's partition retained, CLUSTERING_INSTABILITY alert emitted to Tier 3.

The game-theoretic analysis (FC-5 resolution) establishes that an adversary must perturb at least 0.3 * sqrt(V) edges to shift the partition undetectably -- approximately 30 edges at V = 10,000 and 95 edges at V = 100,000. The NMI check detects perturbations above this threshold; below it, the attacker can affect approximately 3 agents (at 10K) to 10 agents (at 100K) without detection, a bounded and acceptable residual risk.

**Neighborhood coordinators.** Each neighborhood has one coordinator -- a lightweight coroutine (not a separate service) running on any node hosting a neighborhood member. Coordinator assignment follows C7 RIF task scheduling. Failover uses C7's standard rescheduling; PCM parameter stores are persisted to disk at each cycle, and MIDAS instances reset cleanly.

### 7.3 Permitted Correlation Model (PCM)

The PCM is the analytical core of Tier 2. It models structurally expected pairwise correlation and produces residuals that isolate genuinely anomalous signals.

**Simplified log-linear model (main-effects only).** Per simplification S-01, the PCM uses a main-effects-only log-linear model with 6 parameters per channel (1 intercept + 5 covariates). Interaction terms are deferred until the FC-1 convergence experiment validates that they improve held-out R-squared by at least 0.05.

```
log E[corr_c(a_i, a_j)] = beta_0 + beta_1 * x_1(a_i, a_j)
                                   + beta_2 * x_2(a_i, a_j)
                                   + beta_3 * x_3(a_i, a_j)
                                   + beta_4 * x_4(a_i, a_j)
                                   + beta_5 * x_5(a_i, a_j)
```

**Total parameters per neighborhood:** 4 channels x 6 parameters = 24 parameters.
**Total parameters system-wide:** 24 x k neighborhoods.

This is a reduction from the architecture's 64 parameters per neighborhood (16 per channel with interaction terms) to 24. The main-effects model is a conservative starting point: if interaction terms are truly needed, the residuals will be larger (more false positives, not fewer -- a safe failure mode), and the FC-1 experiment will quantify the improvement.

**Five structural covariates:**

| Covariate | Symbol | Definition | Range | Source |
|-----------|--------|-----------|-------|--------|
| Parcel colocation | x_1 | Fraction of ticks where both agents assigned to same C8 settlement parcel | [0, 1] | C8 DSF (XL-5) |
| Committee coassignment | x_2 | Jaccard similarity of committee membership sets | [0, 1] | C3 Tidal (XL-1) |
| Epoch coregistration | x_3 | 1 - |registration_epoch(a_i) - registration_epoch(a_j)| / max_epoch_gap | [0, 1] | C7 agent registry |
| Claim class overlap | x_4 | Cosine similarity of 9-element claim class distribution vectors | [0, 1] | C5 PCVM (XL-2) |
| Tidal phase alignment | x_5 | 1 - |phi(a_i) - phi(a_j)| / pi (circular distance) | [0, 1] | C3 Tidal (XL-1) |

Each covariate captures a distinct mechanism by which the platform *structure* induces behavioral correlation: shared infrastructure (x_1), shared evaluation context (x_2), shared calibration era (x_3), shared claim domain (x_4), and shared temporal regime (x_5).

**Parameter estimation.** Performed at each CONSOLIDATION_CYCLE via maximum likelihood on within-neighborhood pairs. The model is a GLM with log link and Gaussian family, solved in closed form with ridge regularization:

```
theta* = (X^T X + lambda_reg * I)^{-1} X^T y
```

where y is the vector of log-correlations, X is the design matrix (n_pairs x 6), and lambda_reg = 0.01 prevents overfitting in small neighborhoods. Pairs with fewer than 30 valid co-observed ticks are excluded from training.

At n = 27 agents (average at V = 10,000): C(27, 2) = 351 pairs, solving a 6x6 linear system = O(216). Per-cycle cost across 377 neighborhoods x 4 channels is approximately 1.3 million operations -- negligible.

**Precomputed lookup table.** After estimation, PCM predictions are precomputed for all within-neighborhood pairs:

```
E[corr_c(a_i, a_j)] = exp(X(a_i, a_j)^T * theta_c*)
```

Stored as a HashMap keyed by ordered agent pair. Storage cost at n = 27: 351 entries x 4 channels x 8 bytes = 11.2 KB per neighborhood. Refreshed every CONSOLIDATION_CYCLE (condition D-1 preserved).

**Residual computation.** The PCM residual isolates unexplained correlation:

```
R_c(a_i, a_j) = corr_c_observed(a_i, a_j) - E[corr_c(a_i, a_j)]
```

R_c near 0: correlation fully explained. R_c >> 0: agents more correlated than structure predicts (shared influence signal). R_c << 0: agents less correlated than expected (deliberate divergence signal).

**Auditability (condition C-1).** Both raw observed correlation and PCM residual are recorded in the Tier 2 analysis log and emitted to downstream consumers. This preserves the ability to analyze data independent of the PCM model.

**Unmodeled correlation category (condition C-2).** When R_c > threshold_R but the PCM model's R-squared < 0.70, the correlation may be real but its source is ambiguous. In this case, the Tier 2 verdict is emitted at REDUCED severity with reason UNMODELED_CORRELATION. REDUCED-severity anomalies are logged but do NOT count toward Tier 3 escalation. They are available as supplementary evidence if other channels independently confirm.

**Coverage fallback (condition C-3).** If PCM R-squared < 0.70 for a neighborhood-channel, the PCM is non-predictive. Fallback uses raw C17 behavioral similarity:

```
anomaly_signal_c(a_i, a_j) = corr_c_observed(a_i, a_j) - B(a_i, a_j) * rho_c
```

where rho_c is the mean ratio of single-channel correlation to B during the previous cycle. This fallback lacks the 5-covariate model but avoids residualizing against a model that does not fit.

**Convergence experiment (FC-1).** The PCM's reliability depends on parameter convergence. The experiment protocol generates synthetic populations at V = {1K, 10K, 100K} with known structural correlations and 5% anomaly injection. Success criterion: relative L2 parameter error < 0.10 within 1,000 epochs for 95% of neighborhoods. If main-effects convergence succeeds and interaction terms improve R-squared by >= 0.05, interaction terms may be added in a future version.

### 7.4 MIDAS Streaming Edge Detection

MIDAS (Microcluster-based Detector of Anomalies in Edge Streams) operates on PCM-residual-augmented data to detect temporally anomalous correlation patterns.

**Per-neighborhood instances.** Each neighborhood runs 4 MIDAS instances (one per channel). Each instance maintains count-min sketch (CMS) structures:

- CMS width: 512 buckets
- CMS depth: 4 hash functions (pairwise-independent via Murmur3 seeding)
- Memory per instance: 2 CMS x 512 x 4 x 8 bytes = 32 KB
- Per neighborhood (4 channels): 128 KB

**Edge event generation.** At each TIDAL_EPOCH boundary, for each within-neighborhood pair and channel:

1. Compute observed correlation over the most recent 60 ticks.
2. Look up PCM expected correlation from precomputed store.
3. Compute residual R_c = observed - expected.
4. If |R_c| > threshold_R (base residual threshold, derived per-channel from PCM residual standard deviation per simplification S-04):

```
threshold_R_c = base_residual_threshold * (pcm_residual_std_c / mean_pcm_residual_std)
```

Default base_residual_threshold = 0.15 (configurable, range [0.01, 0.50]). This automatically scales per-channel thresholds to the data distribution rather than relying on manually tuned per-channel values. The edge event is fed to the MIDAS instance.

**MIDAS scoring.** Anomaly score via chi-squared statistic:

```
score(a_i, a_j, c, t) = (current_count - expected_count)^2 / expected_count
```

An edge is MIDAS-anomalous if score > threshold_MIDAS (default 3.84, the chi-squared critical value at p = 0.05 with 1 df). Configurable via TIER2_MIDAS_THRESHOLD (range [1.0, 20.0]).

**MIDAS-F temporal decay.** To resist state poisoning (adversary inflating CMS counts to raise expected_count), C35 uses MIDAS-F with decay:

```
total_cms_decayed.query(h) = total_cms.query(h) * decay_factor^(t - last_update(h))
```

decay_factor = 0.95 per TIDAL_EPOCH (configurable via TIER2_MIDAS_DECAY, range [0.80, 0.99]).

**Cycle boundary reset.** MIDAS instances reset at CONSOLIDATION_CYCLE boundaries (aligned with PCM refit). Warm-up period: first 3 TIDAL_EPOCHS after reset, scores suppressed to avoid empty-CMS artifacts.

**Joint anomaly criterion.** An edge is a Tier 2 anomalous edge on channel c only if BOTH conditions hold:

```
anomalous_edge(a_i, a_j, c) =
    MIDAS_score(a_i, a_j, c) > threshold_MIDAS
    AND |R_c(a_i, a_j)| > threshold_R_c
```

The conjunction ensures that flagged edges are both temporally unusual (MIDAS) and structurally unexplained (PCM residual).

### 7.5 Channel Definitions

Tier 2 operates on four analysis channels, extending Tier 1's per-agent metrics to pairwise correlation analysis.

**Channel 0: Verification (c=0).** Source: C5 PCVM. Combines acceptance rate correlation (0.40), verification timing correlation (0.35), and VTD outcome similarity (0.25). Anomaly semantics: coordinated opinion formation or synchronized verification patterns.

**Channel 1: Behavioral (c=1).** Source: C17 MCSD L2. Combines B-score residual (0.70) and action sequence similarity via LCS (0.30). Anomaly semantics: Sybil kinship or behavioral mimicry.

**Channel 2: Infrastructure (c=2).** Source: C7 RIF. Combines IP/network proximity (0.20), latency fingerprint correlation (0.40), and resource usage correlation (0.40). Anomaly semantics: shared hosting or infrastructure compromise. Most prone to legitimate cloud co-tenancy false positives.

**Channel 3: Economic (c=3).** Source: C8 DSF. Combines settlement pattern correlation (0.35), staking behavior similarity (0.35), and reward timing correlation (0.30). Anomaly semantics: coordinated economic strategy or financial manipulation.

### 7.6 Channel Fusion: 3-of-4 Quorum

Channel fusion combines evidence from the four channels into a single per-pair anomaly verdict. Per simplification S-17, the Bayesian network phase is deferred; the quorum is the permanent fusion mechanism until empirical data supports a learned model.

**Quorum rule.** An agent pair is confirmed anomalous if at least 3 of 4 channels flag it:

```
confirmed_anomaly(a_i, a_j) = (count(anomalous_edge(a_i, a_j, c) for c in {0,1,2,3}) >= 3)
```

**False positive rate.** If each channel's per-pair false positive rate is p = 0.05:

```
P(>=3) = C(4,3) * p^3 * (1-p) + C(4,4) * p^4
       = 4 * 0.000125 * 0.95 + 0.00000625
       = 0.000481
```

At 132,000 pairs (V = 10,000): approximately 63 false positives per epoch. Manageable.

**Single-channel high-confidence bypass.** If a single channel's MIDAS anomaly score exceeds 2x threshold_MIDAS AND the PCM residual exceeds 2x threshold_R, that channel alone can confirm the pair (bypasses quorum). This catches extreme single-domain anomalies that the Bayesian network would have caught via high conditional probability. Parameter: TIER2_SINGLE_CHANNEL_BYPASS_MULTIPLIER (default 2.0, range [1.5, 5.0]).

**Future learned model.** When sufficient confirmed anomaly data exists (>= 50 confirmed anomalies system-wide with cross-validation accuracy > 0.85), a learned fusion model (Bayesian network, logistic regression, or other calibrated classifier) may replace the quorum. The quorum is retained as permanent fallback. If the learned model's false positive rate exceeds 3x the quorum's rate for 3 consecutive CONSOLIDATION_CYCLEs, automatic reversion to quorum occurs.

### 7.7 C12 AVAP Pre-Confirmed Edge Injection

AVAP-confirmed collusion edges (from contract XL-6) bypass channel fusion entirely:

```
IF C12 reports AVAP_COLLUSION_CONFIRMED(a_i, a_j):
    tier2_verdict(a_i, a_j) = CONFIRMED
    tier2_verdict.source = AVAP_INJECTION
    tier2_verdict.confidence = 1.0
```

C12's AVAP has its own multi-mechanism confirmation pipeline (honeypot claims, sealed submission, behavioral analysis, deterrence payments). Re-validating through C35's fusion adds latency without adding confidence. If a pair is both AVAP-confirmed and independently C35-confirmed, the Tier 2 record reflects both sources; Tier 3 treats double-confirmation as higher confidence.

### 7.8 Escalation to Tier 3

Not every Tier 2 confirmation warrants Tier 3 analysis. Three filters apply:

1. **Minimum pair count.** At least 2 anomalous pairs in the same neighborhood in the same TIDAL_EPOCH. A single anomalous pair is logged but not escalated.

2. **Confidence floor.** Maximum confidence among anomalous pairs must be >= 0.70.

3. **Recency filter.** If the same neighborhood escalated a Tier 3 case within the past 3 epochs that resolved as FALSE_POSITIVE, the threshold rises to 4 pairs with confidence >= 0.85 for the next 10 epochs. This suppresses repeated false escalation from noisy neighborhoods.

**Tier 2 Anomaly Annotation** (emitted to Tier 3):

```
struct Tier2Annotation {
    neighborhood_id:     NeighborhoodID,
    cycle:               u64,
    epoch:               u64,
    involved_agents:     Vec<(AgentID, AgentID)>,
    channel_evidence:    Vec<ChannelEvidence>,
    pcm_residuals:       Vec<PCMResidual>,    // raw + residual per condition C-1
    fusion_method:       FusionMethod,         // QUORUM | AVAP_INJECTION
    confidence:          f64,
    trigger_density:     f64,
    neighborhood_size:   usize,
    midas_scores:        Vec<[f64; 4]>,
    sentinel_health:     f64,                  // current meta-signal value
}
```

### 7.9 Per-Neighborhood State Model and Memory Budget

Canonical per-neighborhood state (reconciled per DF-3):

| Component | Size | Notes |
|-----------|------|-------|
| PCMParameterStore | 192 bytes | 4 channels x 6 params x 8 bytes (main-effects only) |
| PCM lookup table | ~11 KB (at n=27) | C(27,2) = 351 entries x 4 channels x 8 bytes |
| MIDAS instances (4 channels) | 128 KB | 4 x 32 KB per CMS pair |
| ChannelFusionEngine (quorum config) | 32 bytes | Threshold + quorum parameters |
| Tier 1 trigger queue | ~2 KB | Bounded buffer for pending annotations |
| **Total per neighborhood** | **~141 KB** | |

**Memory at scale (Tier 2 only):**

| Scale | Neighborhoods (k) | Tier 2 Memory |
|-------|-------------------|---------------|
| 1K | 51 | 7.2 MB |
| 10K | 377 | 53 MB |
| 100K | 3,013 | 425 MB |

**Combined Tier 1 + Tier 2 memory:**

| Scale | Tier 1 | Tier 2 | Total |
|-------|--------|--------|-------|
| 1K | 2.4 MB | 7.2 MB | 9.6 MB |
| 10K | 24 MB | 53 MB | 77 MB |
| 100K | 240 MB | 425 MB | 665 MB |

These estimates are consistent with the architecture's Section 10.2 scalability analysis once the LTA window size (60 ticks, not 600) and PCM parameter count (24, not 64) corrections from DF-3 and S-01 are applied. The 100K total of 665 MB is within single-server capacity and well below the architecture's upper estimate of 720 MB (which used the uncorrected values).

---

## 8. Tier 3 -- Epidemiological Backward Tracing

### 8.1 Narrative Overview

Tier 3 is the rarest and most expensive tier in the pipeline. While Tier 1 runs every tick and Tier 2 runs at epoch boundaries, Tier 3 activates only when Tier 2 has produced a statistically significant cluster of confirmed anomalies. Its purpose is not detection but *attribution*: given that anomalous coordination exists, identify the most probable common causal source.

The methodology draws from epidemiological outbreak investigation. When a disease cluster appears, the epidemiologist first confirms that the case count exceeds random variation (overdispersion analysis) and then traces backward through contact networks to find a common source (backward tracing). C35 Tier 3 applies the same two-step protocol to the agent interaction graph.

This is a fundamentally different operation from Tier 1 and Tier 2. Those tiers ask "is something anomalous?" Tier 3 asks "what caused it?" The answer -- an operator, an infrastructure provider, a systematic vulnerability -- has governance consequences. It may trigger Citicate review (C14), settlement holds (C8), or collusion investigation referral (C12). Because of these consequences, Tier 3 requires high statistical confidence and traces through multiple independent data sources before producing an attribution.

### 8.2 Activation Conditions

Tier 3 activation requires three simultaneous conditions.

**Condition 1: Tier 2 posterior threshold.** At least one Tier 2 anomaly must have high confidence. Under quorum fusion: the quorum fired AND MIDAS-F chi-squared independently confirms (p < 0.01). This ensures Tier 3 is not triggered by marginal Tier 2 findings.

**Condition 2: Minimum anomaly count.** The analysis window (sliding window of the last 10 TIDAL_EPOCHs = 1 CONSOLIDATION_CYCLE) must contain at least 15 confirmed anomalies. This is reduced from the architecture's 30 per simplification S-12. At V = 10,000, this threshold is typically met within 1-2 CONSOLIDATION_CYCLEs. At V = 1,000, it may take 3-6 cycles (30-60 hours).

The lower threshold accepts reduced statistical power. At n = 15, the negative binomial overdispersion test has approximately 45-55% power (compared to 65% at n = 30). This is acceptable because Tier 3 is a last-resort attribution mechanism, not a primary detector. Tiers 1 and 2 handle detection. Tier 3 adds attribution value, and lower power means occasional missed attributions, not missed detections.

Per simplification S-12, the synthetic anomaly generation mechanism is removed. Rather than manufacturing synthetic calibration anomalies from known-benign pairs to inflate the sample size, the system simply operates with available real data and accepts the power reduction at small scales. This eliminates the SyntheticAnomaly data structure, the HybridPool refresh logic, and the synthetic generation dependency on the PCM subsystem.

**Condition 3: Concurrency bound.** At most 3 Tier 3 analyses run concurrently. Each is computationally expensive and involves cross-layer data source queries. Excess analyses queue in FIFO order with priority override (higher-confidence annotations can evict lower-confidence queued items).

```
TIER3_MAX_CONCURRENT = 3 (configurable, range [1, 10])
```

### 8.3 Overdispersion Analysis

The first analytical step tests whether confirmed anomalies cluster around specific agents more than random variation predicts.

**Statistical model.** Per-agent anomaly counts follow a negative binomial distribution NB(mu, alpha), where mu is the expected count and alpha is the overdispersion parameter. Under the null hypothesis (no common cause), counts are Poisson (alpha = 0, variance = mean). Under the alternative (common source), alpha > 0 and variance = mean + mean^2/alpha > mean.

The Cameron & Trivedi (1998) negative binomial regression framework is applied:

```
Response:    Y_i = count of Tier 2 anomalies involving agent i in analysis window
Covariates:  X_i = [operator_id, registration_cohort, geographic_cluster,
                     infrastructure_provider]
Link:        log(mu_i) = X_i * beta
Dispersion:  Var(Y_i) = mu_i + mu_i^2 / alpha
```

**Overdispersion test.** The likelihood ratio test statistic:

```
LR = 2 * (log_likelihood_NB - log_likelihood_Poisson)
```

Under H0, LR follows a boundary mixture distribution (0.5 * chi^2_0 + 0.5 * chi^2_1). Reject H0 at significance 0.05 when LR > 2.71.

**Operational threshold.** If fitted alpha_hat > ALPHA_THRESHOLD (default 2.0), overdispersion is not merely significant but *operationally meaningful*: anomaly count variance is at least 3x the mean at mean >= 2. This filters marginal overdispersion from benign structural clustering while flagging the pronounced concentration that operator control produces.

**Covariate ranking.** Regression coefficients reveal which covariates explain the concentration:

| Covariate | Source | Signal |
|-----------|--------|--------|
| operator_id | C7 agent registry | Direct operator linkage (strongest when available) |
| registration_cohort | C7 lifecycle events | Shared origin (same deployment batch) |
| geographic_cluster | C3 scheduling metadata | Shared infrastructure exposure |
| infrastructure_provider | C35 Tier 2 infrastructure channel | Shared compute/network |

Covariates ranked by Wald statistic z_k = |beta_hat_k| / SE(beta_hat_k), with two-sided p-values.

### 8.4 Backward Tracing Through Two Sources

When overdispersion analysis identifies significant clustering (alpha_hat > ALPHA_THRESHOLD), backward tracing constructs a causal phylogeny from confirmed anomalies back through the platform's interaction history. Per simplification S-13, backward tracing queries two cross-layer data sources (reduced from four).

**Seed set construction.** Agents appearing in >= 2 confirmed Tier 2 anomalies within the analysis window form the seed set -- the "repeatedly anomalous" population.

**Source 1: C17 Behavioral Similarity Chains.** Query C17 for B(a_i, a_j) pairwise similarity among all seed agents and their 1-hop neighbors in the C17 similarity graph. Edges with B >= 0.60 (the C17 WATCH threshold) are included. These represent behavioral kinship: agents that act similarly, potentially sharing an operator or training lineage.

```
for agent in seed_set:
    neighbors = C17.get_similar_agents(agent, threshold=0.60)
    for neighbor, score in neighbors:
        phylogeny.add_edge(agent, neighbor, channel="behavioral",
                          weight=score, timestamp=C17.last_epoch(agent, neighbor))
```

**Source 2: C7 Intent Provenance.** Query C7's Intent State Registry for intent delegation chains and saga invocations involving seed agents. If agent A's intent was delegated from agent B, or both participated in the same C7 saga, a provenance link exists.

```
for agent in seed_set:
    provenance = C7.get_intent_provenance(agent, window=analysis_window)
    for record in provenance:
        phylogeny.add_edge(record.delegator, record.delegate,
                          channel="intent", weight=1.0,
                          timestamp=record.saga_epoch)
```

These two sources provide the strongest causal signals. Behavioral similarity identifies shared operator/lineage (who they *are*). Intent provenance identifies operational linkage (what they *did together*). Per simplification S-13, C3 scheduling co-occurrence (weak, non-causal) and C8 settlement flow paths (duplicates Tier 2 economic channel) are deferred as enrichment extensions for post-W2.

**Phylogeny merge and ancestor identification.** The two edge sets merge into a single directed graph. Maximum likelihood estimation identifies the most probable common ancestor:

```
log_L(candidate) = SUM over seed agents a_i:
    log(P(a_i anomalous | a_i linked to candidate))
  + SUM over phylogeny edges:
    log(P(edge weight | both linked to candidate))
  - SUM over non-edges:
    log(P(no edge | expected if both linked to candidate))
```

The candidate pool: all operator_ids linked to >= 2 seed agents, all infrastructure_providers hosting >= 2 seed agents, and an "unknown common origin" null candidate.

**Attribution confidence.** Posterior probability via Bayes' rule with uniform prior over candidates. Formal attribution requires P(candidate | evidence) >= 0.90.

### 8.5 Attribution Report Format

```
ATTRIBUTION_REPORT:
    report_id:            UUID
    analysis_epoch:       u64
    analysis_window:      (u64, u64)          // (start_epoch, end_epoch)
    trigger_anomalies:    Vec<AnomalyRef>     // Tier 2 anomalies that triggered
    seed_agents:          Vec<UUID>
    overdispersion:
        alpha_hat:        f64
        lr_statistic:     f64
        lr_p_value:       f64
        covariate_ranking: Vec<CovariateResult>
    attribution:
        suspected_cause:  AttributionTarget   // operator_id | infrastructure_id | UNKNOWN
        confidence:       f64                 // posterior probability (0.0-1.0)
        evidence_chain:   Vec<PhylogenyEdge>  // edges supporting attribution
        alternative_causes: Vec<(AttributionTarget, f64)>
    recommended_action:   enum {
        REFER_TO_TRIBUNAL,        // confidence >= 0.90, operator identified
        REFER_TO_AVAP,            // confidence >= 0.90, collusion pattern
        FLAG_INFRASTRUCTURE,      // confidence >= 0.90, infrastructure cause
        INCONCLUSIVE,             // confidence < 0.90
        INSUFFICIENT_DATA         // overdispersion not significant
    }
    sentinel_health_at_analysis: f64          // sentinel_health when analysis ran
    computation_budget:
        wall_clock_ms:    u64
        edges_traversed:  u64
        cross_layer_queries: u64
```

**Governance consequences.** REFER_TO_TRIBUNAL triggers C14 Citicate review. REFER_TO_AVAP triggers C12 collusion investigation. FLAG_INFRASTRUCTURE triggers C7 operational review. INCONCLUSIVE is logged for pattern accumulation. All reports are persisted to the Tier 3 Evidence Store regardless of outcome.

### 8.6 Sample Size Management

With the synthetic anomaly mechanism removed (S-12), sample size management is straightforward:

- Tier 3 operates on real confirmed anomalies only.
- The minimum threshold is 15 (reduced from 30).
- At small scales (V = 1,000), Tier 3 may take 3-6 CONSOLIDATION_CYCLEs to accumulate sufficient data. This is acceptable: at 1K agents, the attack surface is small enough for manual review and C12 AVAP to provide adequate coverage.
- At medium scales (V = 10,000), 15 anomalies accumulate within 1-2 cycles.
- At large scales (V = 100,000), 15 anomalies accumulate within a single cycle.

The statistical power trade-off at n = 15 versus n = 30:

| Sample Size | Power at alpha=2.0 | Expected Detection Rate | Trade-Off |
|-------------|--------------------|-----------------------|-----------|
| 15 | ~0.50 | 1 in 2 genuine campaigns detected | Acceptable for attribution (not detection) |
| 30 | ~0.65 | 2 in 3 detected | Architecture target (achievable at 10K+) |
| 50 | ~0.80 | 4 in 5 detected | Excellent (achievable at 100K) |

Missed attributions at small scale are tolerable because Tier 1 and Tier 2 detection continues regardless. The agents are still flagged and monitored; only the causal attribution is delayed.

### 8.7 DORMANT/ACTIVE Lifecycle

Tier 3 operates as a lifecycle state machine with hysteresis to prevent oscillation.

```
DORMANT --> (15+ real anomalies in 10-epoch window) --> ACTIVE
ACTIVE  --> (analysis complete)                      --> ACTIVE (checks for new batches)
ACTIVE  --> (real anomaly rate < 5/window for
             2 consecutive CONSOLIDATION_CYCLEs)     --> DORMANT
```

**While DORMANT:**
- Confirmed anomalies continue accumulating in the rolling buffer.
- No Tier 3 analyses are initiated.
- Overdispersion test runs in shadow mode (results logged, not acted upon) for calibration.

**While ACTIVE:**
- New anomaly batches are processed as they arrive (subject to concurrency limit).
- Attribution reports are generated and forwarded to governance systems.
- If the anomaly rate drops below 5 per 10-epoch window, a cooldown timer starts. If the rate remains below 5 for 2 full CONSOLIDATION_CYCLEs (72,000 seconds), Tier 3 transitions to DORMANT.

The two-cycle hysteresis prevents rapid ACTIVE-DORMANT-ACTIVE oscillation when the anomaly rate fluctuates near threshold. The dormant-to-active threshold (15) is deliberately lower than the hysteresis-based active-to-dormant threshold (sustained low rate for 2 cycles) per simplification S-08, ensuring asymmetric transitions: fast activation, slow deactivation.

---

*End of Part 1. Part 2 continues with: Cross-Layer Integration Contracts (formal schemas, API endpoints, failure modes), Parameter Registry (~66 parameters with sensitivity classifications and valid ranges), Formal Properties and Invariants (Tier 2 and Tier 3 properties, system-wide invariants), Security Architecture (attack classes, Red Team protocols, PCM bootstrap defense), Scalability Analysis (compute, memory, bandwidth at 3 scales), Lean Alternative Contingency (Condition C-9), and Condition Traceability Matrix.*
# C35 — Seismographic Sentinel with PCM-Augmented Tier 2

## Master Technical Specification — Part 2

**Version:** 1.0.1
**Date:** 2026-03-14
**Invention ID:** C35
**System:** Atrahasis Agent System v2.0
**Status:** SPECIFICATION — Part 2 (Sections 9-12)
**Normative References:** C3 v2.0, C5 v2.0, C7 v2.0, C8 v2.0, C9 v2.0, C12 v2.0, C17 v1.0
**Continuation of:** C35 MTS Part 1 (Sections 1-8)
**Simplifications in Effect:** PCM main-effects-only (6 params/channel, 24 total); 3-of-4 quorum fusion only (Bayesian deferred); C6 integration removed; 2 Tier 3 trace sources; min 15 anomalies; 1 ETR composite signal; ~66 parameters; sentinel_health meta-signal on all outputs (DF-2 resolution)

---

## 9. Cross-Layer Integration Protocols

C35 is a detection system that operates entirely on data produced by other AAS layers. It owns none of the data it analyzes. This section specifies the precise contracts between C35 and each of the six layers it integrates with, following the C9 integration contract matrix conventions established in C9 Cross-Layer Reconciliation v2.0. Every data flow has a named source, a named consumer, a cadence, a schema, a failure mode, and a sentinel_health impact assessment.

All contracts use the C4 ASV vocabulary for message types and follow the C9 three-tier temporal hierarchy: SETTLEMENT_TICK = 60s, TIDAL_EPOCH = 3600s (60 ticks), CONSOLIDATION_CYCLE = 36000s (600 ticks, 10 epochs).

**Integration removed:** C6 (EMA) integration is removed from this specification per simplification directive. C6 knowledge contribution metrics were LOW PRIORITY enrichment signals that did not feed C35's core detection pipeline. Their absence reduces Tier 3 attribution context for knowledge-domain anomalies but does not degrade Tier 1 or Tier 2 detection capability. If C6 integration is restored in a future revision, it SHALL be added as a supplementary Tier 3 data source only, with no impact on the Tier 1/Tier 2 detection path.

### 9.1 Integration with C3 (Tidal Noosphere -- Coordination)

**Purpose.** C3 provides scheduling and coordination data that feeds Tier 1's committee frequency metric (channel c=2), supplies structural covariates for PCM fitting (parcel colocation, tidal phase alignment), and receives C35's sentinel composite signal for scheduling optimization.

**Inbound Data (C3 -> C35):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C3->C35:SCHED | Parcel assignments, committee rotations, tidal phase per agent | TIDAL_EPOCH (3600s) | C3 push via event bus; SCHEDULING_SNAPSHOT message |
| C3->C35:TOPOLOGY | Agent topology snapshot (KG adjacency for spectral clustering input) | CONSOLIDATION_CYCLE (36000s) | C3 push via event bus; TOPOLOGY_SNAPSHOT message |

C35 extracts committee_frequency per agent from SCHEDULING_SNAPSHOT (normalized by population mean) for Tier 1 channel c=2. From TOPOLOGY_SNAPSHOT, C35 extracts parcel colocation frequency x_1 and committee coassignment frequency x_2 as PCM structural covariates.

**Outbound Data (C35 -> C3):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C35->C3:CLUSTER | Neighborhood membership (agent -> neighborhood_id mapping) | CONSOLIDATION_CYCLE (36000s) | C35 push via event bus |
| C35->C3:ETR | sentinel_composite_score per agent (see Section 9.8) | TIDAL_EPOCH (3600s) | C35 push via event bus; ETR_COMPOSITE message |

**API Contract:**

```
GET /tidal/schedule/{epoch}
  Request: C35 queries C3 for scheduling data at a specific epoch.
  Response 200:
    {
      "epoch": u64,
      "parcel_assignments": [
        { "parcel_id": "uuid", "assigned_agents": ["uuid", ...] }
      ],
      "committee_roster": [
        { "committee_id": "uuid", "members": ["uuid", ...], "claim_class": "D" }
      ],
      "tidal_phase": "NEAP" | "SPRING" | "transitional",
      "scheduling_hash": "sha256hex"
    }
  Response 404: { "error": "EPOCH_NOT_AVAILABLE" }
  Latency: < 5ms
```

**Failure Mode.** If C3 stops emitting SCHEDULING_SNAPSHOT for >3 TIDAL_EPOCHS (10,800s), Tier 1 channel c=2 (committee_frequency) degrades to last-cached value. After 100 ticks (6,000s) of staleness, the channel is marked STALE and excluded from trigger computation. Tier 2 PCM covariates x_1 and x_2 retain their last-computed values from the most recent CONSOLIDATION_CYCLE. ETR output pauses; C3 scheduling continues without sentinel input. sentinel_health impact: -0.15 (C3 unavailability removes one Tier 1 channel and two PCM covariates, degrading detection sensitivity by approximately 20-25%).

### 9.2 Integration with C5 (PCVM -- Verification)

**Purpose.** C5 is C35's primary data source for Tier 1 detection. Every verification outcome feeds the per-agent STA/LTA detectors through two channels: verification_latency (c=0) and claim_acceptance_rate (c=1). C35 reciprocates by providing anomaly flags that gate C5's credibility adjustment process.

**Inbound Data (C5 -> C35):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C5->C35:VERIFY | Per-agent verification outcomes (latency, acceptance/rejection, opinion alignment) | SETTLEMENT_TICK (60s) | C5 push via VERIFICATION_EVENT message |
| C5->C35:CRED | Credibility state changes (score deltas, reclassifications) | SETTLEMENT_TICK (60s) | C5 push via CREDIBILITY_UPDATE message |

C35 extracts verification_latency (mean latency normalized by P99 calibration) for channel c=0, and claim_acceptance_rate (fraction of positive opinions, b > 0.5) for channel c=1 from VERIFICATION_EVENT streams.

**Outbound Data (C35 -> C5):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C35->C5:FLAG | Anomaly flags for credibility gating | Event-driven (on detection) | C35 push via ANOMALY_FLAG message |

ANOMALY_FLAG schema:
```
ANOMALY_FLAG:
  flag_id:              UUID
  agent_id:             UUID
  severity:             enum {WATCH, FLAG, CONFIRMED}
  tier:                 u8                     # 1, 2, or 3
  channels_triggered:   Vec<String>
  sentinel_health:      f64                    # 0.0-1.0, current meta-signal
  recommended_action:   enum {GATE_CREDIBILITY, REDUCE_COMMITTEE_WEIGHT,
                              SUSPEND_VERIFICATION, INFORMATIONAL}
  ttl_epochs:           u8                     # flag expires after N epochs (default 10)
  timestamp:            u64
```

**API Contract:**

```
GET /sentinel/anomaly_level/{agent_id}
  Request: C5 queries C35 for agent anomaly status before credibility adjustment.
  Response 200:
    {
      "agent_id": "uuid",
      "tier1_status": "NORMAL" | "CANDIDATE" | "CONFIRMED" | "DEGRADED",
      "tier2_status": "CLEAR" | "WATCH" | "FLAG",
      "overall_risk": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" | "UNKNOWN",
      "sentinel_health": 0.92,
      "last_updated": u64
    }
  Response 404: { "error": "AGENT_NOT_FOUND" }
  Latency: < 2ms (served from in-memory cache)
```

**Failure Mode.** C5 is the single most critical data source for C35. If C5 stops emitting VERIFICATION_EVENTs, C35 loses both primary Tier 1 channels (c=0 and c=1). C35 MUST detect C5 silence within 3 SETTLEMENT_TICKs (180s). Upon detection, all agents transition to DEGRADED trigger state. C35 emits ORCHESTRATION_ADVISORY to C7 with risk_level=UNKNOWN and reason="C5_SILENCE". sentinel_health impact: -0.40 (C5 unavailability removes two of four Tier 1 channels, disabling the verification channel in Tier 2 PCM, and eliminating C35's primary detection path; system operates on committee_frequency and behavioral_consistency only, with severely degraded sensitivity).

### 9.3 Integration with C7 (RIF -- Orchestration)

**Purpose.** C7 is C35's administrative backbone. It provides the agent registry (who exists), lifecycle events (registration, deregistration, suspension), intent state (what agents are doing), and saga infrastructure. C35 uses C7 data for agent lifecycle management, infrastructure channel input to Tier 2, and response action dispatch.

**Inbound Data (C7 -> C35):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C7->C35:LIFECYCLE | Agent lifecycle events (REGISTER, DEREGISTER, SUSPEND, RESUME, MIGRATE) | Event-driven | C7 push via AGENT_LIFECYCLE_EVENT |
| C7->C35:INTENT | Intent state updates (ISR changes, saga state transitions) | SETTLEMENT_TICK (60s) | C7 push via INTENT_STATE_UPDATE |
| C7->C35:REGISTRY | Agent registry snapshot (full agent list with metadata) | CONSOLIDATION_CYCLE (36000s) | C7 push via REGISTRY_SNAPSHOT |

On REGISTER: C35 allocates per-agent Tier 1 state, initializes STA/LTA windows, begins calibration period. On DEREGISTER: archives anomaly history, deallocates state, removes from neighborhood. On SUSPEND: sets trigger_state to DEGRADED. On RESUME: restores to NORMAL. Registration metadata (operator_id, infrastructure_provider, geographic_region, model_lineage) feeds PCM covariate extraction and Tier 3 overdispersion covariates.

**Outbound Data (C35 -> C7):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C35->C7:ADVISORY | Anomaly-informed orchestration advisories | Event-driven (on detection) | C35 push via ORCHESTRATION_ADVISORY |

ORCHESTRATION_ADVISORY schema:
```
ORCHESTRATION_ADVISORY:
  advisory_id:          UUID
  agent_id:             UUID
  risk_level:           enum {LOW, MEDIUM, HIGH, CRITICAL, UNKNOWN}
  sentinel_health:      f64                    # 0.0-1.0, gates confidence
  reason:               String
  recommended_action:   enum {DEPRIORITIZE, QUARANTINE_INTENTS,
                              BLOCK_SAGAS, INFORMATIONAL}
  ttl_epochs:           u8
  timestamp:            u64
```

C7 is not obligated to act on ORCHESTRATION_ADVISORYs. Per the C9 authority hierarchy, C7 is sovereign over orchestration decisions. C35 provides risk information; C7 decides whether and how to act. When sentinel_health < 0.50, all advisories are automatically downgraded to INFORMATIONAL to prevent degraded-state C35 from issuing unreliable recommendations.

**API Contract:**

```
GET /rif/agent/{agent_id}/lifecycle
  Request: C35 queries C7 for agent registration metadata.
  Response 200:
    {
      "agent_id": "uuid",
      "registration_epoch": u64,
      "operator_id": "uuid" | null,
      "infrastructure_provider": "string" | null,
      "geographic_region": "string" | null,
      "model_lineage": "string" | null,
      "status": "ACTIVE" | "SUSPENDED" | "DEREGISTERED"
    }
  Latency: < 5ms
```

**Failure Mode.** If C7 stops emitting AGENT_LIFECYCLE_EVENTs, C35 cannot track new agent registrations or deregistrations. Existing agents continue operating with their current Tier 1 state. New agents that register during C7 silence are invisible to C35, creating a detection gap. C35 detects C7 silence when REGISTRY_SNAPSHOT is not received within 1.5x the expected CONSOLIDATION_CYCLE interval. Upon detection, C35 logs a WARNING and emits a self-directed degradation notice. Infrastructure channel (Tier 2) degrades to cached intent data. sentinel_health impact: -0.10 (C7 unavailability blocks new agent onboarding and degrades infrastructure channel; existing detection continues normally).

### 9.4 Integration with C8 (DSF -- Settlement)

**Purpose.** C8 provides economic data that feeds Tier 2's economic channel and Tier 3's settlement flow tracing. C35 reciprocates by flagging agents whose economic behavior is anomalous, allowing C8 to hold settlements pending review.

**Inbound Data (C8 -> C35):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C8->C35:SETTLE | Settlement events (reward distributions, staking changes, budget flows) | SETTLEMENT_TICK (60s) | C8 push via SETTLEMENT_EVENT |
| C8->C35:ECON | Economic summary per agent (cumulative rewards, staking position) | TIDAL_EPOCH (3600s) | C8 push via ECONOMIC_SUMMARY |

C35 extracts reward_pattern_similarity and staking_covariance for Tier 2 economic channel pairs, and flow_concentration (Herfindahl index) for Tier 3 economic tracing.

**Outbound Data (C35 -> C8):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C35->C8:SFLAG | Settlement anomaly flags | Event-driven (on detection) | C35 push via SETTLEMENT_ANOMALY_FLAG |

SETTLEMENT_ANOMALY_FLAG schema:
```
SETTLEMENT_ANOMALY_FLAG:
  flag_id:              UUID
  agent_id:             UUID
  severity:             enum {WATCH, FLAG, CONFIRMED}
  sentinel_health:      f64
  recommended_action:   enum {HOLD_SETTLEMENT, FREEZE_STAKING,
                              AUDIT_FLOWS, INFORMATIONAL}
  affected_ticks:       Vec<u64>
  ttl_epochs:           u8
  timestamp:            u64
```

Per the C9 authority hierarchy, C8 is sovereign over settlement. If C8 distributes a settlement that C35 has flagged as anomalous and the anomaly is later confirmed, C8's settlement record includes the C35 flag reference for audit accountability.

**API Contract:**

```
GET /dsf/settlement_flows/{agent_id}?window={epochs}
  Request: C35 queries C8 for settlement flow history (Tier 3 backward tracing).
  Response 200:
    {
      "agent_id": "uuid",
      "window_epochs": u16,
      "flows": [
        {
          "tick": u64,
          "event_type": "REWARD" | "STAKE_CHANGE" | "BUDGET_FLOW" | "PENALTY",
          "amount_aic": f64,
          "counterparty": "uuid" | null,
          "budget_stream": "VERIFICATION" | "SCHEDULING" | "KNOWLEDGE" |
                           "GOVERNANCE" | "EXTERNAL"
        }
      ],
      "total_flow_volume": f64
    }
  Latency: < 10ms
```

**Failure Mode.** If C8 stops emitting SETTLEMENT_EVENTs, Tier 2's economic channel degrades to cached values. After 100 ticks of staleness, the economic channel is excluded from quorum computation (quorum effectively becomes 3-of-3 on the remaining channels, which increases false negative rate). Tier 3 economic tracing becomes unavailable. sentinel_health impact: -0.10 (economic channel loss reduces detection breadth but does not disable core verification/behavioral detection).

### 9.5 Integration with C12 (AVAP -- Collusion Defense)

**Purpose.** C12 and C35 have a bidirectional enrichment relationship. C12 provides confirmed collusion evidence that C35 uses as ground truth for PCM calibration and as pre-confirmed Tier 2 triggers. C35 provides neighborhood-level anomaly findings that feed C12's triangulation mechanism.

**Inbound Data (C12 -> C35):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C12->C35:COLLUSION | Confirmed collusion edges from AVAP pipeline | Event-driven | C12 push via CONFIRMED_COLLUSION_EDGE |

CONFIRMED_COLLUSION_EDGE schema:
```
CONFIRMED_COLLUSION_EDGE:
  edge_id:              UUID
  agent_a:              UUID
  agent_b:              UUID
  evidence_type:        enum {HONEYPOT_TRAP, CANARY_MATCH,
                              BEHAVIORAL_CLASSIFIER, SEALED_OPINION_LEAK,
                              MULTI_SIGNAL_FUSION}
  confidence:           f64        # 0.0-1.0
  detection_epoch:      u64
  evidence_hash:        [u8; 32]
```

When C35 receives a CONFIRMED_COLLUSION_EDGE with confidence >= 0.80 (C12_INJECTION_THRESHOLD), both agents are immediately set to CONFIRMED anomaly status in Tier 2, bypassing the normal channel fusion pipeline. The edge is added to the Tier 3 hybrid pool as a confirmed (non-synthetic) anomaly. This bypass is safe because C12 has already independently confirmed collusion through a structurally separate detection mechanism.

**Outbound Data (C35 -> C12):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C35->C12:FINDING | Tier 2/3 findings with neighborhood context | Event-driven | C35 push via SENTINEL_FINDING |

SENTINEL_FINDING schema:
```
SENTINEL_FINDING:
  finding_id:           UUID
  neighborhood_id:      UUID
  agents:               Vec<UUID>
  finding_type:         enum {TIER2_QUORUM, TIER2_MIDAS, TIER3_ATTRIBUTION}
  residuals:            Map<String, f64>
  confidence:           f64
  sentinel_health:      f64
  epoch:                u64
```

**Calibration Loop.** C12 confirmed edges serve as ground truth. When C12 confirms agents A and B are colluding, C35 retroactively checks whether its Tier 2 pipeline would have detected the pair. The outcome is logged to a calibration metric (pcm_detection_rate_vs_c12_ground_truth) used at CONSOLIDATION_CYCLE to assess PCM effectiveness.

**API Contract:**

```
POST /sentinel/external_evidence
  Request: C12 submits collusion evidence for injection.
  Body:
    {
      "source": "C12",
      "source_reference": "uuid",
      "agents": ["uuid", ...],
      "evidence_type": "string",
      "confidence": f64
    }
  Response 201:
    {
      "evidence_id": "uuid",
      "action_taken": "INJECTED" | "QUEUED" | "REJECTED",
      "reason": "string"
    }
  Response 429: { "error": "RATE_LIMITED" }
  Rate limit: 100 submissions per TIDAL_EPOCH per source
  Latency: < 50ms (validation + injection into Tier 2 pipeline)
```

**Failure Mode.** C12 is an enrichment source, not a critical dependency. If C12 becomes unavailable, C35 loses pre-confirmed collusion edge injection and calibration ground truth. Tier 2 operates entirely on its own fusion pipeline, which is the design-basis operating mode. Tier 3 attribution loses one confirmation source. sentinel_health impact: -0.05 (C12 unavailability is operationally transparent; detection continues at full capability, calibration quality degrades slowly over time as ground truth accumulates less frequently).

### 9.6 Integration with C17 (MCSD L2 -- Behavioral Similarity)

**Purpose.** C17 is C35's most important data source for Tier 2. The behavioral similarity function B(a_i, a_j) provides the primary signal for the behavioral channel in the 4-channel quorum. The LSH similarity graph provides the weighted adjacency matrix for spectral clustering that produces the neighborhood partition. C17's behavioral_consistency self-similarity metric feeds Tier 1 channel c=3.

**Inbound Data (C17 -> C35):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C17->C35:SIMILARITY | Pairwise B(a_i, a_j) scores for all LSH candidate pairs | CONSOLIDATION_CYCLE (36000s) | C17 push via SIMILARITY_BATCH |
| C17->C35:SELF | behavioral_consistency self-similarity per agent (B_self) | TIDAL_EPOCH (3600s) | C17 push via SELF_SIMILARITY_UPDATE |

SIMILARITY_BATCH contains SimilarityPair records with agent_a, agent_b, similarity score (B in [0.0, 1.0]), per-modality distances (temporal, structural, error, resource, lexical), cross-correlation coefficient, and C17's own graduated_status (CLEAR/WATCH/FLAG).

C35 consumes SIMILARITY_BATCH in two ways: (1) the B(a_i, a_j) scores form the weighted adjacency matrix for spectral clustering at each CONSOLIDATION_CYCLE, and (2) within-neighborhood B scores serve as the behavioral channel input for Tier 2 PCM residual analysis.

C35 consumes SELF_SIMILARITY_UPDATE for Tier 1 channel c=3 (behavioral_consistency). Between TIDAL_EPOCH updates, the last-computed value is held constant. This is acceptable because behavioral consistency measures epoch-scale stability, not tick-scale fluctuation.

**Outbound Data (C35 -> C17):**

| Flow ID | Data | Cadence | Format |
|---------|------|---------|--------|
| C35->C17:NEIGHBORHOODS | Full neighborhood partition for SEB task stratification | CONSOLIDATION_CYCLE (36000s) | C35 serves via API |

C17 uses the partition to stratify SEB (Standardized Evaluation Battery) task selection so that agents from different neighborhoods receive different task subsets, improving detection orthogonality.

**API Contract:**

```
GET /sentinel/neighborhoods
  Request: C17 queries C35 for the full neighborhood partition.
  Response 200: (see Section 9.7 endpoint #2)
  Latency: < 10ms (served from in-memory cache)
```

**Failure Mode.** C17 is critical for Tier 2 operation. If C17 stops emitting SIMILARITY_BATCH, spectral clustering cannot recompute at the next CONSOLIDATION_CYCLE. C35 retains the previous cycle's neighborhood partition. Tier 1 channel c=3 (behavioral_consistency) degrades to last-cached value and is marked STALE after 100 ticks. If C17 remains unavailable for >1 CONSOLIDATION_CYCLE, Tier 2 falls back to raw pairwise correlation without behavioral similarity input, severely degrading PCM residual quality. sentinel_health impact: -0.25 (C17 unavailability degrades Tier 1 channel c=3, disables behavioral channel in Tier 2 PCM, and freezes neighborhood partition; this is the second-most-severe integration failure after C5 silence).

### 9.7 Cluster Membership API (Shared Interface)

The Cluster Membership API is C35's primary shared internal service interface. It is the canonical source of neighborhood assignment for all downstream attested AAS components. Any authorized component that needs to know "which agents are grouped together" queries this API.

**Endpoint 1 -- Per-Agent Cluster Lookup:**

```
GET /sentinel/cluster/{agent_id}
  Description: Returns neighborhood assignment and anomaly status for a single agent.
  Response 200:
    {
      "agent_id": "uuid",
      "neighborhood_id": "uuid",
      "neighbors": ["uuid", ...],
      "cluster_health": f64,            # 0.0-1.0, neighborhood aggregate health
      "agent_status": {
        "tier1_status": "NORMAL" | "CANDIDATE" | "CONFIRMED" | "DEGRADED",
        "tier2_status": "CLEAR" | "WATCH" | "FLAG",
        "overall_risk": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" | "UNKNOWN",
        "last_updated": u64
      },
      "sentinel_health": f64            # 0.0-1.0, system-wide meta-signal
    }
  Response 404: { "error": "AGENT_NOT_FOUND" }
  Latency: < 2ms at all supported scales (1K-100K)
  Source: in-memory HashMap<UUID, AgentClusterState>
  Refresh: neighborhood_id at CONSOLIDATION_CYCLE; agent_status at SETTLEMENT_TICK
```

**Endpoint 2 -- Full Neighborhood Partition:**

```
GET /sentinel/neighborhoods
  Description: Returns the complete partition of all agents into neighborhoods.
  Response 200:
    {
      "epoch": u64,
      "neighborhoods": [
        {
          "id": "uuid",
          "members": ["uuid", ...],
          "centroid": [f64, ...],
          "health": f64,
          "size": u16,
          "pcm_coverage": f64,
          "anomaly_count_recent": u16
        }
      ],
      "total_neighborhoods": u32,
      "total_agents": u32,
      "sentinel_health": f64
    }
  Latency: < 10ms at all supported scales
  Source: in-memory Vec<Neighborhood>, pre-serialized JSON (lazy-invalidated)
  Refresh: CONSOLIDATION_CYCLE
  Response size: ~2.4MB at 100K agents (6,000 neighborhoods x ~400 bytes each)
```

**Endpoint 3 -- Per-Agent Anomaly Level:**

```
GET /sentinel/anomaly_level/{agent_id}
  Description: Returns the current anomaly assessment for a single agent across all
               tiers. This is the endpoint that C5, C7, and C8 use to check agent
               status before taking actions that affect the agent.
  Response 200:
    {
      "agent_id": "uuid",
      "tier1_status": "NORMAL" | "CANDIDATE" | "CONFIRMED" | "DEGRADED",
      "tier1_details": {
        "trigger_state": "string",
        "sta_lta_ratio_fixed": f64,
        "sta_lta_ratio_adaptive": f64,
        "calibration_complete": bool,
        "epochs_since_registration": u32
      },
      "tier2_status": "CLEAR" | "WATCH" | "FLAG",
      "tier2_details": {
        "neighborhood_id": "uuid",
        "max_pcm_residual": f64,
        "channels_elevated": [String],
        "midas_alert": bool
      },
      "tier3_status": null | "ACTIVE" | "ATTRIBUTED",
      "overall_risk": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" | "UNKNOWN",
      "sentinel_health": f64,
      "last_updated": u64
    }
  Response 404: { "error": "AGENT_NOT_FOUND" }
  Latency: < 2ms at all supported scales
  Source: in-memory HashMap, composed from Tier 1 + Tier 2 state
```

**Endpoint 4 -- System Health:**

```
GET /sentinel/health
  Description: Returns the sentinel_health meta-signal and system-wide diagnostics.
               This endpoint exposes C35's self-assessment of its own operational
               integrity (DF-2 resolution: self-referential anomaly suppression).
  Response 200:
    {
      "sentinel_health": f64,          # 0.0-1.0, composite meta-signal
      "health_components": {
        "c3_status":  "OK" | "DEGRADED" | "UNAVAILABLE",
        "c5_status":  "OK" | "DEGRADED" | "UNAVAILABLE",
        "c7_status":  "OK" | "DEGRADED" | "UNAVAILABLE",
        "c8_status":  "OK" | "DEGRADED" | "UNAVAILABLE",
        "c12_status": "OK" | "DEGRADED" | "UNAVAILABLE",
        "c17_status": "OK" | "DEGRADED" | "UNAVAILABLE",
        "tier1_active_fraction": f64,  # fraction of agents with active (non-DEGRADED) Tier 1
        "tier2_pcm_coverage": f64,     # mean R-squared across neighborhoods
        "tier3_state": "DORMANT" | "ACTIVE",
        "self_attribution_flag": bool  # true if recent anomalies correlate with C35 state changes
      },
      "last_updated": u64,
      "uptime_ticks": u64
    }
  Latency: < 2ms
  Refresh: SETTLEMENT_TICK
```

**sentinel_health Computation.** The meta-signal is computed as:

```
sentinel_health = 1.0
                  - c3_penalty                   # 0.00 or 0.15
                  - c5_penalty                   # 0.00 or 0.40
                  - c7_penalty                   # 0.00 or 0.10
                  - c8_penalty                   # 0.00 or 0.10
                  - c12_penalty                  # 0.00 or 0.05
                  - c17_penalty                  # 0.00 or 0.25
                  - self_attribution_penalty     # 0.00 or 0.10
                  - tier1_degradation_penalty    # 0.0 to 0.15 (proportional to DEGRADED fraction)

sentinel_health = clamp(sentinel_health, 0.0, 1.0)
```

When sentinel_health < 0.50, all outbound anomaly flags and advisories are automatically downgraded to INFORMATIONAL and annotated with sentinel_health_degraded=true. This prevents a degraded C35 from issuing unreliable detection results that downstream systems might act upon. When sentinel_health < 0.20, C35 emits a SYSTEM_DEGRADATION_ALERT to C7 requesting operational review.

**Self-Attribution Check (DF-2 Resolution).** At each CONSOLIDATION_CYCLE, C35 checks whether anomalies detected in the most recent cycle correlate temporally with C35's own state changes (neighborhood repartition, PCM recalibration, threshold adjustment). If >30% of confirmed anomalies occurred within 2 TIDAL_EPOCHS of a C35 state change, the self_attribution_flag is set to true and the self_attribution_penalty of 0.10 is applied. This mechanism prevents the cascade collapse scenario (Pre-Mortem F-2) where C35's own repartitioning creates the anomalies it then detects.

**Cache Architecture.** All GET endpoints are served from in-memory caches:

| Cache | Key Type | Refresh Cadence | Size at 100K |
|-------|----------|----------------|--------------|
| agent_cluster_map | HashMap<UUID, AgentClusterState> | CONSOLIDATION_CYCLE | ~4.8 MB |
| agent_status_map | HashMap<UUID, AgentAnomalyStatus> | SETTLEMENT_TICK | ~3.2 MB |
| neighborhood_list | Vec<NeighborhoodSummary> | CONSOLIDATION_CYCLE | ~2.4 MB |
| neighborhoods_json | Option<Vec<u8>> | Lazy-invalidated | ~2.4 MB |

**Consistency Model.** Bounded staleness: agent status stale by at most 1 SETTLEMENT_TICK (60s); neighborhood membership stale by at most 1 CONSOLIDATION_CYCLE (36,000s). Consumers requiring stronger consistency must account for this window.

**Rate Limiting.** All endpoints: max 100 queries per SETTLEMENT_TICK per authenticated consumer (rate_limit_per_consumer parameter). POST /sentinel/external_evidence: max 100 submissions per TIDAL_EPOCH per source.

### 9.8 ETR Output (Simplified: 1 Composite Signal)

C35 exports a single composite signal per agent to C3's ETR (Emergent Trust Regime) system, replacing the original three-signal design (skew_metric, starvation_flag, divergence_metric). The simplification reduces cross-layer coupling and makes C3's consumption contract cleaner.

**sentinel_composite_score Definition:**

```
sentinel_composite_score(agent) =
    w_tier1 * tier1_risk_score(agent) +
    w_neighborhood * neighborhood_health_score(agent)

where:
    tier1_risk_score(agent) =
        0.0   if trigger_state == NORMAL
        0.3   if trigger_state == CANDIDATE
        0.7   if trigger_state == CONFIRMED
        0.5   if trigger_state == DEGRADED

    neighborhood_health_score(agent) =
        1.0 - cluster_health(agent.neighborhood_id)
        # cluster_health is 0.0-1.0, so this inverts it: unhealthy = high score

    w_tier1         = 0.60
    w_neighborhood  = 0.40
```

The sentinel_composite_score ranges from 0.0 (no concern) to 1.0 (maximum concern). All scores are gated by sentinel_health: if sentinel_health < 0.50, all composite scores are clamped to 0.0 (neutral) to prevent degraded C35 from biasing C3 scheduling.

**Delivery.** Pushed to C3 at each TIDAL_EPOCH boundary (3600s cadence) as an ETR_COMPOSITE message containing a vector of (agent_id, sentinel_composite_score) pairs for all registered agents. Message size at 100K agents: ~2.4 MB (100K x 24 bytes per record).

**C3 Consumption.** C3 uses sentinel_composite_score for scheduling optimization: agents with high scores (>0.5) may be deprioritized in committee assignment, reducing their influence on verification outcomes while investigation proceeds. C3 is not obligated to act on the score; it is advisory per the C9 authority hierarchy.

---

## 10. Security Analysis

C35 is simultaneously a security component (detecting anomalies in the AAS platform) and an attack surface (an adversary who defeats C35 operates undetected). This section specifies the adversarial model, defense mechanisms, and residual risks. Six attack classes are analyzed, followed by three C35-as-attack-surface scenarios and the sentinel_health self-referential defense.

### 10.1 Adversarial Model

C35 defends against an adversary with the following general capabilities: the adversary controls one or more registered agents, can observe binary trigger outcomes (flagged/not-flagged) for controlled agents, may observe neighborhood assignments only if it also compromises or legitimately controls an authorized internal consumer of the Cluster Membership API, and can submit transactions at controlled intensities. The adversary does NOT observe: raw STA/LTA ratio values, PCM residuals, MIDAS scores, channel fusion intermediate values, or other agents' trigger outcomes. Six attack classes exploit specific aspects of this adversarial model.

### 10.2 Attack Class Analysis

**Attack Class 1 -- Evasion (Boiling Frog)**

- **Description.** The adversary gradually shifts agent behavior over T epochs with per-epoch change delta, staying below the adaptive baseline's absorption rate (changes below ~0.258 * sigma_bg per tick are absorbed without triggering adaptive STA/LTA at the default w_l=60 window). The goal is to shift from legitimate to anomalous behavioral profile without triggering Tier 1.
- **Defense mechanism.** Fixed baseline + OR-trigger. The fixed baseline is immutable after calibration. Accumulated drift that the adaptive baseline absorbs still registers against the fixed baseline. The OR-trigger ensures a fixed-baseline exceedance alone is sufficient to enter CANDIDATE state. Defense bound: detection occurs when cumulative drift exceeds 3.0 * sigma_bg from the registration-time profile. At drift rate delta per tick, detection latency is at most ceil(3.0 * sigma_bg / delta) ticks.
- **Residual risk.** An adversary who shifts by less than 3.0 sigma total is indistinguishable from legitimate behavioral evolution. This is by design: sub-threshold changes are not anomalous by definition.
- **Detection probability estimate.** P(detect | drift > 3 sigma) = 0.95 (fixed baseline covers 90% confidence interval); P(detect | drift in [2, 3] sigma) = 0.60 (near boundary, jitter creates stochastic detection); P(detect | drift < 2 sigma) = 0.05 (below design threshold).

**Attack Class 2 -- Poisoning (PCM Calibration Corruption)**

- **Description.** The adversary enters during the PCM calibration window (epochs 0-1000) and behaves in a way that biases the log-linear coefficients, inflating expected correlation for certain covariate configurations. Post-calibration, the adversary exploits the inflated expectation to conduct correlated activity that falls within the corrupted expected range.
- **Defense mechanism.** Bootstrap-then-audit protocol (simplified to 2 phases). Phase 1 (epochs 0-500): raw similarity bootstrap with conservative thresholds (residual_threshold = 0.80). Phase 2 (epochs 500-1000): initial PCM calibration from all agents, followed by retrospective audit at epoch 1000. Agents whose mean absolute residual exceeds the 95th percentile are entered into a calibration exclusion set and PCM is recomputed without them.
- **Residual risk.** An adversary with perfect operational security during the full 1000-epoch calibration phase cannot be excluded. A single poisoner in a neighborhood of k agents contributes at most 2/(k*(k-1)) of pairwise data; at k=23, this is 0.4% of observations, producing <5% coefficient bias. Multiple colluders (m=5) can produce up to 20% bias on specific main-effect coefficients. This is acknowledged as monitoring flag MF-5.
- **Detection probability estimate.** P(detect retrospectively | poisoner contributed >5% coefficient bias) = 0.80; P(detect | <5% bias) = 0.15.

**Attack Class 3 -- Manipulation (Spectral Clustering Boundary Perturbation)**

- **Description.** The adversary adds or removes up to B = c * sqrt(V) edges in the agent interaction graph to shift target agents across neighborhood boundaries or fragment neighborhoods containing colluders.
- **Defense mechanism.** NMI divergence check. At each CONSOLIDATION_CYCLE, spectral clustering is computed on the raw graph G and on a perturbed copy G' (edge weights perturbed by N(0, sigma_perturb^2) where sigma_perturb = 0.10). NMI between the two clusterings is computed. If NMI < theta_NMI (default 0.85), the clustering is flagged as potentially manipulated and reverts to the previous cycle's partition.
- **Residual risk.** Attacker with budget B < 0.3 * sqrt(V) can make small boundary adjustments that pass the NMI check. At V=10K this affects ~3 agents; at V=100K, ~9-10 agents. Mitigated by randomized perturbation direction (fresh random at each cycle prevents pre-compensation) and temporal consistency monitoring (agents whose neighborhood changes more than lambda_change = 0.02 per cycle are flagged).
- **Detection probability estimate.** P(detect | B > 0.3*sqrt(V)) = 0.92; P(detect | B in [0.1, 0.3]*sqrt(V)) = 0.45; P(detect | B < 0.1*sqrt(V)) = 0.05.

**Attack Class 4 -- Reconstruction (Fixed Baseline Inference)**

- **Description.** The adversary conducts A/B testing, submitting transactions at varying intensities and observing binary trigger outcomes to reconstruct fixed baseline percentile values via logistic regression.
- **Defense mechanism.** Three-layer defense. Layer 1: Laplace noise (epsilon=1.0) on stored percentiles, producing std dev = sqrt(2) = 1.414 in natural units. Layer 2: 5% multiplicative threshold jitter per tick (effective range [2.85, 3.15] at threshold 3.0). Layer 3: binary-only feedback (agent sees flagged/not-flagged, never scores). The information-theoretic argument: effective mutual information per test transaction is ~0.03 bits. To reconstruct 4 metrics to 10% precision requires ~53.2 bits / 0.03 bits = 1,773 test transactions per metric, >10,000 total.
- **Residual risk.** The anomalous submission rate required for 10,000+ test transactions (1 per tick for 6,944 ticks = ~116 hours sustained probing) itself triggers Tier 1 within ~20 ticks, making the attack self-defeating.
- **Detection probability estimate.** P(detect probing attempt) = 0.99 (self-defeating); P(successful reconstruction given detection evasion) = 0.02.

**Attack Class 5 -- Concentration (Neighborhood Stacking)**

- **Description.** The adversary registers multiple Sybil agents and manipulates interaction patterns to concentrate them in a single spectral neighborhood. Within the concentrated neighborhood, mutual correlation is "expected" because agents share structural covariates.
- **Defense mechanism.** Neighborhood size cap of 2 * log(V) agents. At V=100K, maximum size is ~23 agents. Concentrating >23 forces a split, distributing colluders across neighborhoods and exposing cross-neighborhood correlation. Secondary defense: C17 MCSD L2 behavioral similarity detects Sybil clusters independently; C12 AVAP disrupts committee patterns that create shared covariates.
- **Residual risk.** An adversary with fewer than 23 agents can concentrate within a single neighborhood. PCM residuals may still detect anomalous correlation if structural covariates do not fully explain coordination, but this depends on the adversary's ability to engineer shared covariates organically.
- **Detection probability estimate.** P(detect | >23 colluders in one neighborhood) = 0.98 (forced split exposes); P(detect | 10-23 colluders) = 0.55 (PCM residual dependent); P(detect | <10 colluders with engineered covariates) = 0.20.

**Attack Class 6 -- Channel Gaming**

- **Description.** The adversary suppresses anomaly signals in specific channels while conducting anomalous activity visible only in the remaining channels. Goal: prevent 3-of-4 quorum from firing.
- **Defense mechanism.** 3-of-4 quorum requires anomaly in 3 channels. An adversary suppressing 2 channels prevents quorum. However, single-channel anomalies exceeding 2x the MIDAS threshold are escalated directly via high-confidence single-channel bypass. Additionally, the PCM residual captures structural correlation that the adversary may not be able to suppress across all channels simultaneously: suppressing behavioral channel anomaly requires actually behaving normally in the behavioral dimension, which constrains the adversary's operational freedom.
- **Residual risk.** A sophisticated adversary who isolates anomalous activity to exactly 1-2 channels with anomaly magnitude below the single-channel bypass threshold evades quorum detection. This is the primary detection gap in the quorum phase.
- **Detection probability estimate.** P(detect | anomaly in >= 3 channels) = 0.93; P(detect | anomaly in 2 channels, one > 2x threshold) = 0.70; P(detect | anomaly in 1-2 channels, all below bypass) = 0.10.

### 10.3 Fixed-Baseline Protection (FC-3 Red Team Protocol)

The Red Team evaluation follows a structured adversarial game with three defense layers whose combined protection provides an information-theoretic bound.

**Layer 1 -- Laplace Noise.** Each stored percentile p_k is replaced with p_k + Lap(0, 1/epsilon) where epsilon = 1.0. Variance = 2/epsilon^2 = 2.0; standard deviation = 1.414 in percentile natural units. Even perfect estimation of the noisy threshold leaves irreducible uncertainty of 1.414 units.

**Layer 2 -- Threshold Jitter.** At each tick, effective threshold is multiplied by (1 + U) where U ~ Uniform[-0.05, 0.05]. This smooths the sigmoid boundary in the adversary's logistic model, requiring O(1/jitter_range^2) = O(400) additional samples for equivalent precision.

**Layer 3 -- Binary Feedback.** Agent sees only flagged/not-flagged per tick. Information content per observation is at most 1 bit, reduced to ~0.03 bits effective mutual information by Layers 1 and 2.

**Combined Defense.** Reconstruction to 10% precision across 4 metrics requires >10,000 test transactions at 0.03 bits per transaction. At 1 transaction per SETTLEMENT_TICK, this takes >116 hours of sustained probing. The probing itself triggers Tier 1 within ~20 ticks (~1,200 seconds). The attack is self-defeating by 3 orders of magnitude in time.

**Red Team Verdict:** PASS at >10,000 transactions; CONDITIONAL PASS at 5,000-10,000 (increase epsilon to 2.0); FAIL at <5,000 (redesign noise mechanism).

### 10.4 Spectral Clustering Game Theory (FC-5)

The interaction is modeled as a Stackelberg game where the defender commits to a clustering policy and the attacker best-responds.

**Attacker Action Space.** Modify up to B = c * sqrt(V) edges (c in [0.1, 1.0]), motivated by the O(sqrt(V)) perturbation bound from spectral graph theory (Mohar 1991).

**Detection Boundary.** By the Davis-Kahan theorem (1970), eigenvector perturbation is bounded by ||delta_v|| <= ||delta_L||_F / delta, where delta is the spectral gap (second-smallest eigenvalue of the normalized Laplacian). For B modified edges: ||delta_L||_F = O(sqrt(B)). The NMI check detects perturbation when ||delta_v|| > sigma_perturb / sqrt(V).

Combining: detection when sqrt(B) / delta > sigma_perturb / sqrt(V), i.e., B > sigma_perturb^2 * delta^2 / V. The theoretical bound is unrealistically low; the empirical bound from Amini et al. (2013) on random geometric graphs with planted perturbations gives:

**NMI check detects perturbations when B > 0.3 * sqrt(V)**

At V=10K: B > 30 edges (~3 agents affected). At V=100K: B > 95 edges (~10 agents affected). Within the undetectable region (B < 0.3 * sqrt(V)), the attacker's impact is bounded to ~10 agents at maximum platform scale.

**Mitigations for Residual Risk.** (1) Randomized perturbation direction per CONSOLIDATION_CYCLE prevents pre-compensation. (2) Temporal consistency monitoring flags agents with neighborhood-change frequency exceeding Poisson(lambda=0.02) expectation. (3) Cross-tier continuity: moved agents carry Tier 1 history; the move itself is logged for audit.

### 10.5 PCM Calibration Poisoning Defense

**Bootstrap-Then-Audit Protocol (Simplified: 2 Phases).**

Phase 1 -- Bootstrap (epochs 0-500): PCM unavailable. Tier 2 operates on raw pairwise correlation without structural correction. Conservative thresholds (residual_threshold = 0.80 vs. post-PCM default 0.60). All pairwise data accumulated for Phase 2.

Phase 2 -- Calibration + Audit (epochs 500-1000): Compute log-linear PCM coefficients from accumulated data using all agents. At epoch 1000, run retrospective audit: compute PCM residuals for Phase 1 data, flag agents whose mean |residual| exceeds the 95th percentile distribution. Flagged agents enter calibration exclusion set E_calib. Recompute PCM excluding E_calib. If max |coefficient_change| > 0.20, accept recalibrated PCM; otherwise retain original (excluded agents did not materially bias calibration).

**Residual Risk.** Adversary with perfect operational security during 1000-epoch calibration is indistinguishable from legitimate agent. Bounded by: single poisoner contributes <5% coefficient bias; 5 coordinated poisoners can produce up to 20% bias on specific coefficients. Tracked as MF-5.

### 10.6 C35-as-Attack-Surface

**Trigger Saturation Defense.** Adversary floods Tier 1 with obvious anomalies to saturate Tier 2 capacity. Defense: max_candidate_fraction = 5% cap on simultaneous CANDIDATE agents. Priority queue: (1) dual-trigger events, (2) agents with prior CONFIRMED history, (3) agents in neighborhoods with existing Tier 2 anomalies, (4) all others. If >2% of agents simultaneously produce dual-triggers, mass-event protocol demotes unknown agents to priority 2.

**Oracle Attack Defense.** Adversary uses binary responses and any cluster-membership visibility available through compromised or authorized internal consumers to learn thresholds and boundaries. Defense: agents see only binary outcome, never scores. Anomaly levels (PCM residuals, MIDAS scores, Bayesian posteriors) are NOT visible to agents. Cluster membership is available only to authorized internal consumers because downstream specs need it, creating inherent tension between utility and security. Mitigated by NMI divergence check and temporal consistency monitoring. Authorized consumers of detailed data (C5, C8, C12) access via authenticated API with rate limiting (100 queries/tick/consumer).

**Feedback Poisoning Defense.** Adversary manipulates which anomalies are "confirmed" to corrupt the Bayesian network CPTs. Under simplified specification (quorum only, Bayesian deferred), this attack is not yet applicable. When Bayesian fusion is activated in a future revision, defense requires: minimum 50 confirmed anomalies before activation, 5-fold cross-validation score > 0.85, and manual review for the first 20 confirmations.

### 10.7 Self-Referential Anomaly Suppression (DF-2 Resolution)

C35 contains one structural feedback loop: it publishes cluster memberships that influence C3 scheduling and C5 verification routing, which produce the behavioral data that C35 ingests. A repartitioning event can create transient behavioral discontinuities that C35 then detects as anomalies, triggering further repartitioning in the next cycle (cascade collapse, Pre-Mortem F-2).

The sentinel_health meta-signal resolves this through three mechanisms:

1. **Self-Attribution Check.** At each CONSOLIDATION_CYCLE, compute the fraction of confirmed anomalies whose onset falls within 2 TIDAL_EPOCHS of a C35 state change (repartitioning, PCM recalibration, threshold adjustment). If fraction > 0.30, set self_attribution_flag = true and apply -0.10 penalty to sentinel_health.

2. **Output Gating.** When sentinel_health < 0.50, all outbound anomaly flags and advisories are downgraded to INFORMATIONAL. This prevents degraded C35 from issuing actionable recommendations that could amplify the cascade. The ETR composite scores are clamped to 0.0 (neutral), removing C35's influence on C3 scheduling until health recovers.

3. **ETR Emission Rate Limiter.** At most 10% of neighborhoods may have their sentinel_composite_score changed by >0.3 between consecutive TIDAL_EPOCHS. If more than 10% of neighborhoods would change, the scores are blended: new_score = 0.7 * old_score + 0.3 * computed_score. This dampens the feedback loop by limiting the rate at which C35's output can perturb the scheduling environment.

---

## 11. Performance Analysis

All performance analysis uses the corrected memory estimates per DF-3 resolution: LTA window = 60 entries (not 600), per-agent state = ~2 KB, MIDAS CMS width = 1024, depth = 4.

### 11.1 Computation

**Per-Tick Budget (SETTLEMENT_TICK = 60s).**

| Component | Per-Tick Cost | 1K Agents | 10K Agents | 100K Agents |
|-----------|-------------|-----------|------------|-------------|
| Tier 1 STA/LTA (all agents) | O(V) | 40K ops; < 1ms | 400K ops; < 10ms | 4M ops; < 100ms |
| Tier 1 confirmation check | O(V_candidate) | ~50 agents; < 0.01ms | ~500 agents; < 0.1ms | ~5K agents; < 1ms |
| Tier 2 PCM lookup (triggered pairs) | O(T * N_avg) | < 100 lookups; < 0.1ms | < 1K lookups; < 1ms | < 10K lookups; < 10ms |
| Tier 2 MIDAS scoring | O(E_residual) | < 50 edges; < 0.1ms | < 500 edges; < 0.5ms | < 5K edges; < 5ms |
| Tier 2 channel fusion (quorum) | O(N_triggered) | < 10 neighborhoods; < 0.05ms | < 100 neighborhoods; < 0.3ms | < 1K neighborhoods; < 1ms |
| sentinel_health computation | O(1) | < 0.01ms | < 0.01ms | < 0.01ms |
| API cache refresh | O(V) | < 0.5ms | < 5ms | < 50ms |
| **Per-tick total** | | **< 1.8ms** | **< 17ms** | **< 167ms** |

At all three scales, per-tick processing consumes less than 0.3% of the 60,000ms SETTLEMENT_TICK budget. Tier 1 is the dominant per-tick cost, scaling linearly with agent count.

**Per-CONSOLIDATION_CYCLE Budget (36,000s = 600 ticks).**

| Component | Per-Cycle Cost | 1K Agents | 10K Agents | 100K Agents |
|-----------|---------------|-----------|------------|-------------|
| PCM recomputation (all neighborhoods) | O(V * log^2(V)) | 100 neighborhoods x C(10,2) pairs x 6 params x 10 iters = 270K ops; ~0.04s | ~1.2K neighborhoods x C(14,2) pairs x 6 x 10 = 7.6M ops; ~1.1s | ~5.9K neighborhoods x C(17,2) pairs x 6 x 10 = 48M ops; ~18s |
| Spectral clustering | O(V * k * iters) | Similarity 1M entries; ~0.01s | ~1s | Nystrom approx: 100K x 1K landmarks + 1K^3 = 101M ops; ~100s |
| NMI divergence check | O(V) | < 0.01s | < 0.1s | < 1s |
| sentinel_health self-attribution check | O(anomaly_count) | < 0.01s | < 0.01s | < 0.1s |
| **Per-cycle total** | | **< 0.1s** | **< 2.2s** | **< 119s** |

PCM recomputation benefits from the main-effects-only simplification: 6 parameters per channel (intercept + 5 main effects) instead of 16 (with 10 interaction terms). This reduces the per-neighborhood MLE cost by 63% and eliminates the multicollinearity risk identified in Pre-Mortem F-3. At 100K agents, the cycle budget of 36,000s is used at 0.33% capacity.

### 11.2 Memory (Corrected per DF-3)

**Per-Agent Memory: ~2 KB.**

| Component | Size |
|-----------|------|
| Identity (agent_id + registration_epoch) | 24 bytes |
| STA window (4 metrics x 5 ticks x 8 bytes) | 160 bytes |
| LTA window (4 metrics x 60 ticks x 8 bytes) | 1,920 bytes |
| Fixed baseline (4 metrics x 5 percentiles x 8 bytes) | 160 bytes |
| Adaptive baseline (4 metrics x 8 bytes) | 32 bytes |
| Trigger state + counters | 48 bytes |
| Neighborhood assignment | 16 bytes |
| Padding/alignment | ~40 bytes |
| **Total per agent** | **~2,400 bytes (~2.3 KB)** |

Note: LTA window uses 60 entries (1 TIDAL_EPOCH), not 600. The architecture document's Section 6.1 allocated 600 entries (10 TIDAL_EPOCHS); this is corrected per Section 2.4.2 which specifies w_l = 60 ticks. The 600-entry allocation was an error in the data architecture section.

**Per-Neighborhood Memory: ~50-70 KB.**

| Component | Size |
|-----------|------|
| Identity + member list (avg 17 agents) | ~296 bytes |
| PCM parameters (4 channels x 6 params x 8 bytes) | 192 bytes |
| PCM metadata (R-squared, residual_std, fit_epoch) | 48 bytes |
| MIDAS CMS state (2 sketches x 4 depth x 1024 width x 8 bytes) | 65,536 bytes |
| Fusion state (quorum config) | 32 bytes |
| Anomaly queue (50 entries x 128 bytes) | 6,400 bytes |
| Health metrics | 16 bytes |
| **Total per neighborhood** | **~72,520 bytes (~71 KB)** |

PCM parameter storage benefits from main-effects-only simplification: 192 bytes per neighborhood instead of 512 bytes with interaction terms. The MIDAS CMS dominates neighborhood memory at ~90% of per-neighborhood allocation.

**Total Memory at Scale.**

| Scale | Agents (V) | Neighborhoods (k) | Tier 1 | Tier 2 | Tier 3 | API Cache | Total |
|-------|-----------|-------------------|--------|--------|--------|-----------|-------|
| 1K | 1,000 | ~100 | 2.3 MB | 7.1 MB | 1.4 MB | 1.0 MB | **~12 MB** |
| 10K | 10,000 | ~750 | 23 MB | 53 MB | 1.4 MB | 1.0 MB | **~78 MB** |
| 100K | 100,000 | ~6,000 | 230 MB | 427 MB | 6.3 MB | 12.8 MB | **~676 MB** |

At 100K agents, Tier 2 dominates memory (63%) due to the MIDAS CMS sketches. Tier 1 is 34%. Tier 3 and API caches are negligible. The 676 MB total is well within single-server memory capacity (4-8 GB typical allocation for a detection subsystem).

### 11.3 Network Bandwidth

| Traffic Type | Formula | 1K Agents | 10K Agents | 100K Agents |
|-------------|---------|-----------|------------|-------------|
| Tier 1 metrics ingest (C5, C3, C17) | V x 4 metrics x 8 bytes / 60s | 533 B/s | 5.3 KB/s | 53 KB/s |
| Tier 1 trigger messages (burst) | ~5% trigger rate x V x 100 bytes/tick | 5 KB/tick | 50 KB/tick | 500 KB/tick |
| Tier 2 PCM recomputation data | Per CONSOLIDATION_CYCLE | ~50 KB / 36Ks = 1.4 B/s | ~1 MB / 36Ks = 28 B/s | ~8 MB / 36Ks = 222 B/s |
| Cross-layer event throughput (C12, C7 lifecycle) | Event-driven, sparse | < 1 KB/s | < 5 KB/s | < 20 KB/s |
| ETR composite output (C35 -> C3) | V x 24 bytes / 3600s | 6.7 B/s | 67 B/s | 667 B/s |
| API responses (serving C3, C5, C7, C8, C12, C17) | est. request rate x ~1 KB | 10 KB/s | 50 KB/s | 200 KB/s |
| **Sustained total** | | **~16 KB/s** | **~111 KB/s** | **~274 KB/s** |
| **Peak total (trigger burst + API)** | | **~22 KB/s** | **~162 KB/s** | **~774 KB/s** |

All bandwidth figures are within modern datacenter network capacity by multiple orders of magnitude. Network is not a bottleneck at any scale within the 1K-100K design range.

### 11.4 Bottleneck Analysis

**Primary Bottleneck: Spectral Clustering at 100K.**

Full spectral clustering requires the V x V similarity matrix. At 100K, this is 10 billion entries (80 GB), which is infeasible. Mitigation: Nystrom approximation with m=1,000 landmark agents. Compute the m x V affinity matrix (100M entries, ~800 MB, ~10s), the m x m kernel eigendecomposition (1K^3 ops, ~1s), and approximate full eigenvectors via the Nystrom formula. Total: ~100s at 100K agents. This fits within the 36,000s CONSOLIDATION_CYCLE budget at 0.28% utilization.

Between full recomputations, rank-1 incremental updates to the Laplacian handle agents whose interaction patterns changed significantly (>2 sigma from previous cycle), avoiding full recomputation when <10% of agents change neighborhoods. Cost: O(changed_agents x k) per update.

Scalability ceiling: at 1M agents, Nystrom requires O(m x V) = O(10^9) per recomputation, taking ~1000s (17 minutes). For V > 100K, hierarchical spectral clustering (cluster-of-clusters) is recommended.

**Secondary Bottleneck: PCM Recomputation at 100K.**

PCM recomputation is embarrassingly parallel across neighborhoods. At 100K agents with ~6,000 neighborhoods, each neighborhood's MLE computation is independent. Sequential time: ~18s (reduced from ~200s by the main-effects-only simplification). Parallel time at 8 cores: ~2.3s. Parallel time at 32 cores: ~0.6s. Amortized over the 36,000s cycle budget: < 0.05%.

**Never a Bottleneck: Tier 1 Processing.**

O(V) per tick with ~2.3 KB state per agent. At 100K agents, Tier 1 processes all agents in < 167ms. The SETTLEMENT_TICK budget is 60,000ms. Tier 1 uses < 0.28% of the tick budget.

**Never a Bottleneck: API Serving.**

All GET endpoints served from in-memory caches with O(1) HashMap lookup. Response latency < 2ms for per-agent queries, < 10ms for full partition query (pre-serialized JSON). Cache refresh at SETTLEMENT_TICK cadence adds < 50ms at 100K agents, amortized across the 60s tick.

**Never a Bottleneck: Tier 3 Backward Tracing.**

Tier 3 activates only when >= 15 confirmed anomalies accumulate (simplified from 30). Even at 100K agents, confirmed anomalies are rare (<0.1% of agents). The NB regression and backward trace operate on the anomaly pool (<1000 entries), completing in <1s. Tier 3 is invoked at most once per CONSOLIDATION_CYCLE. The simplified 2-source backward trace (C17 behavioral similarity + C8 settlement flows, down from the 4-source architecture) further reduces per-invocation cost.

### 11.5 Scaling Summary

| Metric | 1K Agents | 10K Agents | 100K Agents |
|--------|-----------|------------|-------------|
| **Per-tick latency** | < 1.8ms (0.003% of budget) | < 17ms (0.028%) | < 167ms (0.28%) |
| **Total memory** | ~12 MB | ~78 MB | ~676 MB |
| **Sustained bandwidth** | ~16 KB/s | ~111 KB/s | ~274 KB/s |
| **Peak bandwidth** | ~22 KB/s | ~162 KB/s | ~774 KB/s |
| **PCM recompute (sequential)** | 0.04s | 1.1s | 18s |
| **Spectral clustering** | 0.01s | 1s | 100s (Nystrom) |
| **Cycle budget used** | < 0.001% | < 0.006% | < 0.33% |
| **Neighborhoods (k)** | ~100 | ~750 | ~6,000 |
| **Mean neighborhood size** | ~10 | ~13 | ~17 |
| **Primary bottleneck** | None | None | Spectral clustering (mitigated) |

The system operates well within budget at all target scales. Per-tick processing overhead is negligible (<0.3% of SETTLEMENT_TICK budget even at 100K). CONSOLIDATION_CYCLE operations are the most expensive but occur once every 10 hours and are parallelizable. The main-effects-only PCM simplification reduces cycle-boundary computation by approximately 60% compared to the full interaction-term model, making PCM recomputation at 100K a non-issue (18s sequential, <3s at 8 cores).

**Scaling Ceiling.** At V > 100K, the Nystrom approximation for spectral clustering remains viable up to approximately V = 500K with m = 5,000 landmarks (~500s recomputation). Beyond 500K, hierarchical spectral clustering (cluster-of-clusters architecture) is required, which is outside the scope of this specification but identified as a future extension point in C22 Wave 5.

---

## 12. Formal Requirements

This section specifies the formal requirements for C35 Seismographic Sentinel. Each requirement has a unique identifier, description, verification method, and priority classification. Priority levels: P0 (must pass at W0 risk validation), P1 (must pass at W1 foundation), P2 (must pass before production deployment).

### 12.1 Detection Capability Requirements

| ID | Description | Verification | Priority |
|----|-------------|-------------|----------|
| REQ-01 | Tier 1 SHALL process all registered agents within one SETTLEMENT_TICK at all supported scales (1K-100K agents). | Load test: measure per-tick latency at 1K, 10K, 100K; must complete within 60s. | P0 |
| REQ-02 | Tier 1 SHALL detect fixed-baseline exceedances (>P95 or <P5) within 1 SETTLEMENT_TICK of occurrence. | Inject synthetic anomaly exceeding P95; verify CANDIDATE state entered within 1 tick. | P0 |
| REQ-03 | Tier 1 SHALL detect adaptive-baseline exceedances (STA/LTA > threshold) within 1 SETTLEMENT_TICK of occurrence. | Inject metric spike; verify STA/LTA ratio exceeds threshold and CANDIDATE state entered. | P0 |
| REQ-04 | Tier 1 confirmation window SHALL produce CONFIRMED status within 3-5 ticks of initial CANDIDATE entry for sustained anomalies. | Inject sustained anomaly (5+ ticks); verify CONFIRMED within confirmation_window_normal ticks. | P1 |
| REQ-05 | Tier 2 channel fusion (3-of-4 quorum) SHALL confirm anomalies when 3 or more channels independently detect anomalous residuals for the same agent pair. | Inject coordinated anomaly across 3 channels; verify quorum fires and anomaly is confirmed. | P0 |
| REQ-06 | Tier 2 PCM residuals SHALL correctly separate structural correlation from anomalous correlation with R-squared >= 0.70 for neighborhoods where PCM is active. | Compute PCM for synthetic neighborhoods with known structural covariates; verify R-squared >= pcm_coverage_threshold. | P1 |
| REQ-07 | Tier 2 high-confidence single-channel bypass SHALL escalate anomalies exceeding 2x MIDAS threshold even when quorum is not met. | Inject single-channel anomaly at 2.5x threshold; verify bypass escalation occurs. | P1 |
| REQ-08 | Tier 3 overdispersion analysis SHALL detect non-Poisson clustering (alpha > alpha_threshold) when a common causal source produces concentrated anomalies. | Inject anomalies with shared operator_id covariate; verify NB regression detects alpha > threshold. | P1 |

### 12.2 Scaling Requirements

| ID | Description | Verification | Priority |
|----|-------------|-------------|----------|
| REQ-09 | C35 SHALL support agent populations of 1,000 to 100,000 without architecture changes. | Deploy at 1K, 10K, 100K; verify all functional requirements pass at each scale. | P0 |
| REQ-10 | Per-tick computation SHALL consume less than 1% of SETTLEMENT_TICK budget (600ms) at all supported scales. | Load test: measure per-tick latency at 100K; must be < 600ms. | P0 |
| REQ-11 | Per-CONSOLIDATION_CYCLE computation (PCM + spectral clustering + NMI check) SHALL complete within 5% of cycle budget (1,800s) at 100K agents. | Benchmark: measure cycle-boundary computation at 100K; must be < 1,800s. | P1 |
| REQ-12 | Total memory consumption SHALL not exceed 1 GB at 100K agents. | Memory profiling at 100K; verify total < 1 GB. | P1 |
| REQ-13 | Spectral clustering SHALL use Nystrom approximation with configurable landmark count (default 1,000) at V > 50K agents. | Verify Nystrom code path activates at V=50K+; compare partition quality (NMI > 0.90) against exact clustering on smaller samples. | P1 |

### 12.3 Latency Requirements

| ID | Description | Verification | Priority |
|----|-------------|-------------|----------|
| REQ-14 | Cluster Membership API per-agent lookup (GET /sentinel/cluster/{agent_id}) SHALL respond within 2ms at all supported scales. | Latency benchmark: 1000 random agent lookups at 100K; p99 < 2ms. | P0 |
| REQ-15 | Cluster Membership API full partition query (GET /sentinel/neighborhoods) SHALL respond within 10ms at all supported scales. | Latency benchmark at 100K; p99 < 10ms. | P1 |
| REQ-16 | Anomaly level query (GET /sentinel/anomaly_level/{agent_id}) SHALL respond within 2ms at all supported scales. | Latency benchmark: 1000 random agent lookups at 100K; p99 < 2ms. | P0 |
| REQ-17 | Health endpoint (GET /sentinel/health) SHALL respond within 2ms. | Latency benchmark; p99 < 2ms. | P1 |

### 12.4 Integration Requirements

| ID | Description | Verification | Priority |
|----|-------------|-------------|----------|
| REQ-18 | C35 SHALL detect C5 silence within 3 SETTLEMENT_TICKs (180s) and transition affected agents to DEGRADED state. | Stop C5 event emission; verify DEGRADED transition within 3 ticks and ORCHESTRATION_ADVISORY emission to C7. | P0 |
| REQ-19 | C35 SHALL accept CONFIRMED_COLLUSION_EDGE from C12 with confidence >= 0.80 and inject as pre-confirmed Tier 2 trigger, bypassing channel fusion. | Submit C12 edge with confidence=0.85; verify both agents set to CONFIRMED in Tier 2. | P1 |
| REQ-20 | C35 SHALL push sentinel_composite_score for all registered agents to C3 at each TIDAL_EPOCH boundary. | Monitor event bus at TIDAL_EPOCH boundary; verify ETR_COMPOSITE message with correct agent count. | P1 |
| REQ-21 | C35 SHALL push neighborhood partition to C17 at each CONSOLIDATION_CYCLE boundary for SEB stratification. | Monitor event bus at CONSOLIDATION_CYCLE boundary; verify partition message with correct agent-to-neighborhood mapping. | P1 |
| REQ-22 | All outbound anomaly flags and advisories SHALL include the current sentinel_health value. | Schema validation: verify sentinel_health field present and in [0.0, 1.0] on all ANOMALY_FLAG, ORCHESTRATION_ADVISORY, SETTLEMENT_ANOMALY_FLAG, and SENTINEL_FINDING messages. | P0 |

### 12.5 Security Requirements

| ID | Description | Verification | Priority |
|----|-------------|-------------|----------|
| REQ-23 | Fixed baseline percentile values SHALL be protected by Laplace noise with configurable epsilon (default 1.0). | Code review: verify Laplace noise injection in calibration path; verify epsilon parameter is applied. | P0 |
| REQ-24 | Threshold jitter (5% multiplicative) SHALL be applied to all trigger threshold evaluations at each SETTLEMENT_TICK. | Code review + unit test: verify jitter application; statistical test that effective thresholds are uniformly distributed in [0.95x, 1.05x] range over 1000 ticks. | P1 |
| REQ-25 | NMI divergence check SHALL be performed at each CONSOLIDATION_CYCLE with a fresh random perturbation. | Verify NMI computation runs at cycle boundary; verify perturbation seed changes each cycle; verify fallback triggers when NMI < theta_NMI. | P1 |
| REQ-26 | At most max_candidate_fraction (5%) of agents SHALL be in CANDIDATE state simultaneously. | Inject anomalies in >5% of agents; verify excess triggers are queued, not processed. | P1 |
| REQ-27 | Anomaly scores, PCM residuals, MIDAS scores, and fusion intermediates SHALL NOT be visible to agents through any API endpoint. | Security audit: verify no API endpoint exposes internal detection scores; verify binary-only feedback model. | P0 |

### 12.6 Degradation and Self-Monitoring Requirements

| ID | Description | Verification | Priority |
|----|-------------|-------------|----------|
| REQ-28 | sentinel_health SHALL be computed at each SETTLEMENT_TICK and reflect the current operational state of all 6 cross-layer integrations. | Disable each integration individually; verify sentinel_health decreases by the specified penalty amount. | P0 |
| REQ-29 | When sentinel_health < 0.50, all outbound anomaly flags and advisories SHALL be downgraded to INFORMATIONAL and sentinel_composite_scores SHALL be clamped to 0.0. | Disable C5 (penalty 0.40) + C3 (penalty 0.15); verify sentinel_health < 0.50; verify all outbound messages are INFORMATIONAL; verify ETR composite scores are 0.0. | P0 |
| REQ-30 | Self-attribution check SHALL be performed at each CONSOLIDATION_CYCLE. If >30% of confirmed anomalies correlate temporally with C35 state changes within 2 TIDAL_EPOCHS, self_attribution_flag SHALL be set to true. | Simulate repartitioning that causes 50% anomaly-state-change temporal correlation; verify flag is set and 0.10 penalty applied. | P1 |
| REQ-31 | ETR emission rate limiter SHALL cap sentinel_composite_score changes to at most 10% of neighborhoods per TIDAL_EPOCH boundary. | Compute composite scores that would change >10% of neighborhoods by >0.3; verify blending formula is applied (0.7 * old + 0.3 * new). | P1 |

### 12.7 Auditability Requirements

| ID | Description | Verification | Priority |
|----|-------------|-------------|----------|
| REQ-32 | All Tier 2 anomaly confirmations SHALL emit an audit record containing raw observed values, PCM expected values, and residuals for each channel (per Condition C-1 auditability). | Trigger Tier 2 anomaly; verify audit record contains raw, expected, and residual for all 4 channels. | P0 |
| REQ-33 | Tier 3 attribution reports SHALL be persisted to the Evidence Store for at least report_retention_cycles CONSOLIDATION_CYCLEs (default 100). | Generate attribution report; verify persistence; verify retrieval after 50 CONSOLIDATION_CYCLEs; verify expiry after retention period. | P2 |
| REQ-34 | All API responses SHALL include a last_updated field indicating the epoch of the most recent data refresh for that response. | Schema validation: verify last_updated present on all API response schemas; verify value is monotonically non-decreasing. | P1 |
| REQ-35 | PCM calibration exclusion set E_calib SHALL be persisted across C35 restarts and SHALL survive CONSOLIDATION_CYCLE repartitioning. | Restart C35 after PCM calibration with exclusion set; verify excluded agents remain excluded in subsequent PCM refit. | P2 |
| REQ-36 | Tier 1 anomaly history per agent (last 100 TriggerEvents) SHALL be archived before agent deregistration and retained for at least 10 CONSOLIDATION_CYCLEs after deregistration. | Deregister agent; verify anomaly history is persisted; verify retrieval within retention window; verify expiry after retention. | P2 |
| REQ-37 | C35 SHALL log all sentinel_health state transitions (OK -> DEGRADED, DEGRADED -> UNAVAILABLE, recovery) with timestamp, cause, and penalty applied, to the system audit log. | Induce integration failure; verify log entry contains correct transition, timestamp, and penalty. | P2 |

### 12.8 Requirements Summary

| Priority | Count | Coverage |
|----------|-------|----------|
| P0 | 15 | Detection core (REQ-01/02/03/05), scaling floor (REQ-09/10), API latency (REQ-14/16), C5 silence detection (REQ-18), sentinel_health gating (REQ-22/28/29), security fundamentals (REQ-23/27), auditability (REQ-32) |
| P1 | 18 | Full detection pipeline (REQ-04/06/07/08), scaling ceiling (REQ-11/12/13), API latency (REQ-15/17), integration contracts (REQ-19/20/21), security hardening (REQ-24/25/26), self-monitoring (REQ-30/31), auditability (REQ-34) |
| P2 | 4 | Long-term retention (REQ-33), persistence (REQ-35/36), audit logging (REQ-37) |
| **Total** | **37** | |

All P0 requirements MUST pass at W0 risk validation per C22 Wave 0 protocol. P1 requirements MUST pass at W1 foundation build. P2 requirements MUST pass before production deployment. Failure of any P0 requirement constitutes a kill criterion per C22 pre-registered kill criteria protocol.

**Traceability to Design Flags.** The following requirements trace to mid-design review flags:

| Design Flag | Resolution | Requirements |
|-------------|-----------|-------------|
| DF-2 (self-referential anomaly suppression) | sentinel_health meta-signal on all outputs; self-attribution check; output gating; ETR rate limiter | REQ-22, REQ-28, REQ-29, REQ-30, REQ-31 |
| DF-3 (memory estimate reconciliation) | LTA window corrected to 60 entries; single authoritative memory budget in Section 11.2 | REQ-12 |
| DF-4 (channel index correction) | Canonical channel ordering: [Verification=0, Behavioral=1, Infrastructure=2, Economic=3] throughout | REQ-05, REQ-32 |
| DF-5 (cross-neighborhood Sybil swarm) | Acknowledged architectural blind spot; lightweight global residual aggregation deferred to future revision | Not addressed (residual gap) |
| DF-6 (Tier 2/3 formal properties) | Covered by REQ-05 through REQ-08 | REQ-05, REQ-06, REQ-07, REQ-08 |
| DF-7 (lean alternative C-9) | Deferred to separate appendix | Not in this part |
| DF-8 (condition traceability) | Provided in this table and throughout Section 9 | This table |

---

*End of C35 Master Technical Specification Part 2. Sections 9-12 complete.*

*Part 1 covers: Sections 1 (Architecture Overview), 2 (Tier 1 Detection), 3 (Tier 2 Correlation), 4 (Tier 3 Attribution), 5 (State Machines), 6 (Data Architecture), 7 (PCM Specification), 8 (Parameter Registry).*
# C35 -- Seismographic Sentinel with PCM-Augmented Tier 2

## Master Tech Spec -- Part 3: Comparison, Risk, Claims, Appendices

**Version:** 1.0.1
**Date:** 2026-03-14
**Invention ID:** C35
**Stage:** SPECIFICATION
**Role:** Specification Writer
**Status:** SPECIFICATION -- Part 3 (Final)
**Continuation of:** C35 MTS Parts 1-2 (Sections 1-12)
**Normative References:** C3 v2.0, C5 v2.0, C7 v2.0, C8 v2.0, C9 v2.0, C12 v2.0, C17 v1.0

**Simplifications in Effect:**
- S-01: PCM main-effects-only (6 params/channel, 24 total; interaction terms deferred to post-W0 validation)
- S-17/S-18: Channel fusion uses 3-of-4 quorum only (Bayesian network deferred to post-Phase-1 data analysis)
- S-14: C6 integration removed from contract set (6 cross-layer integrations: C3, C5, C7, C8, C12, C17)
- S-13: Tier 3 backward tracing uses 2 sources (C17 behavioral, C7 intent); C3/C8 sources deferred
- S-12: Tier 3 minimum sample size lowered to 15 (synthetic anomaly pool removed)
- Total parameters: ~66

---

## 13. Comparison with Existing Approaches

This section evaluates C35 against six representative systems spanning anomaly detection, Sybil defense, and network analysis. The comparison identifies what each system does well, what it lacks relative to C35's requirements, and why C35 is not a rebrand of any individual predecessor.

### 13.1 SentinelAgent (He et al., 2025)

SentinelAgent models multi-agent LLM interactions as typed directed dynamic graphs, deploying a pluggable oversight agent that detects prompt injection, tool misuse, and collusion at the LLM execution layer. It represents the closest published system to C35 in architectural intent: graph-based anomaly detection within a multi-agent system.

**Strengths.** SentinelAgent demonstrates that graph-based anomaly detection is viable at multi-agent scale. Its pluggable oversight architecture allows modular threat coverage. The typed graph representation captures heterogeneous interaction semantics (tool calls, message passing, state access), which is a sound modeling decision.

**Gaps relative to C35.** SentinelAgent targets LLM prompt-level threats -- injection attacks, tool misuse, single-turn collusion -- in a runtime environment where agent interactions are synchronous request-response pairs. C35 operates in a fundamentally different domain: asynchronous verification economics with tidal scheduling, settlement cycles, and knowledge consolidation. SentinelAgent has no concept of: (a) structural covariate correction -- it does not distinguish structurally expected correlation from adversarial correlation; (b) epoch-aware temporal hierarchy -- it processes interactions as a flat stream without the SETTLEMENT_TICK / TIDAL_EPOCH / CONSOLIDATION_CYCLE cadence that governs AAS; (c) epidemiological attribution -- it detects anomalies but does not trace them backward to a common causal source. SentinelAgent also lacks dual-baseline detection, operating on a single adaptive threshold per metric.

**Distinction from C35.** C35's PCM structural correction is absent in SentinelAgent. In an environment where agents are assigned to shared committees, parcels, and tidal phases by the platform itself, raw behavioral correlation is dominated by structural confounds. Without structural correction, a SentinelAgent-style system would produce false positives proportional to the platform's inherent structural coupling -- a rate that would overwhelm downstream investigation capacity at AAS scale.

### 13.2 MIDAS (Bhatia et al., 2020)

MIDAS (Microcluster-Based Detector of Anomalies in Edge Streams) provides constant-time, constant-memory streaming anomaly detection on dynamic edge graphs using count-min sketch data structures. The MIDAS-F variant resists state poisoning through temporal decay. MIDAS was published at AAAI 2020 and extended in TKDD 2022.

**Strengths.** MIDAS is computationally efficient (O(1) per edge update), memory-bounded, and has formal false-positive-rate guarantees under the chi-squared test. The MIDAS-F temporal decay mechanism provides principled resistance to count inflation attacks. C35 incorporates MIDAS-F directly as the streaming edge anomaly detector within Tier 2.

**Gaps relative to C35.** MIDAS is a domain-agnostic edge anomaly detector. It flags edges whose frequency exceeds statistical expectation based on historical counts, but it has no mechanism to distinguish structurally expected correlation from adversarial correlation. In AAS, two agents on the same verification committee will naturally produce frequent edge events; MIDAS would flag these as anomalous unless pre-filtered. MIDAS also lacks: (a) per-agent local detection -- it operates on edges, not nodes; (b) multi-channel evidence fusion -- it processes a single edge stream; (c) hierarchical escalation -- it produces a flat anomaly score per edge with no pipeline for regional aggregation or causal attribution.

**C35's use of MIDAS.** C35 feeds MIDAS the PCM-residual-filtered edge stream rather than the raw correlation stream. This means MIDAS operates on structurally corrected data, receiving only edges whose correlation exceeds what structural covariates predict. This preprocessing eliminates the primary source of false positives that would afflict standalone MIDAS deployment in AAS.

### 13.3 SybilRank Family

The SybilRank / SybilGuard / SybilLimit / SybilSCAR family detects Sybil identities through random walks on social graphs (SybilRank, Cao et al. 2012), edge-count bounds (SybilLimit, Yu et al. 2010), and Bayesian label propagation (SybilSCAR, Wang et al. 2017). These methods assume a social-graph topology with honest seeds, trust transitivity, and a sparse attack edge boundary between the honest and Sybil regions.

**Strengths.** SybilRank achieves near-linear runtime and has formal guarantees under the sparse-cut assumption. SybilSCAR extends to heterogeneous prior information without requiring labeled seeds. These systems have been deployed at scale in social networks (Facebook, LinkedIn).

**Gaps relative to C35.** All SybilRank-family methods assume a social-trust graph where connections represent voluntary bilateral relationships. AAS does not have a social graph; it has a verification co-occurrence graph where connections are algorithmically assigned by C3's tidal scheduling. The sparse-cut assumption -- that the number of edges between honest and Sybil regions is small relative to the region sizes -- does not hold in AAS, because C3's VRF-based committee assignment randomly intermixes honest and Sybil agents. Additionally, SybilRank-family methods provide binary Sybil/not-Sybil classification, not the multi-channel correlation analysis that C35 performs. They cannot distinguish behavioral anomaly from economic anomaly from infrastructure anomaly.

**Distinction from C35.** C17 MCSD Layer 2, which C35 integrates as a data source, already provides AAS-specific Sybil detection via the 5-modality B(a_i, a_j) similarity metric with LSH acceleration. C35 consumes C17's output rather than reimplementing Sybil detection. C35's contribution is the layer above: correlating C17's Sybil signals with verification, infrastructure, and economic channels, and applying structural correction to reduce false positives from legitimate similarity.

### 13.4 Configuration-Model Residuals (Newman, 2010)

Newman's configuration model computes expected edge density between node pairs based on the degree sequence of a network: E[A_ij] = (k_i * k_j) / (2m), where k_i is node degree and m is total edges. Residual analysis subtracts this expectation from observed adjacency, producing a modularity matrix whose eigenstructure reveals community structure.

**Strengths.** The configuration model provides a principled null model for network structure. Residual analysis is well understood, computationally efficient, and has been the foundation of community detection for two decades. Newman's modularity maximization remains a standard benchmark.

**Gaps relative to C35.** The configuration model uses a single covariate -- degree -- to predict edge density. In AAS, degree is a weak predictor because C3's scheduling algorithm produces near-uniform degree distributions by design (agents are assigned to committees by VRF, producing approximately equal participation rates). The structural factors that drive legitimate correlation in AAS -- parcel colocation, claim class overlap, tidal phase alignment, epoch coregistration, committee coassignment -- are not captured by degree alone. Additionally, Newman's framework operates on static networks; AAS produces a dynamic interaction graph that changes at every TIDAL_EPOCH.

**C35's extension.** PCM extends the configuration-model residual concept from degree-only correction to multi-covariate correction using 5 structural covariates in a log-linear model. This is methodologically analogous to how Ovaskainen et al. (2017) extended residual analysis from species prevalence to multi-covariate joint species distribution models in ecology. The contribution is not the residual concept itself but the specific covariate set, the streaming incremental update, and the adversarial-context calibration protocol.

### 13.5 Behavioral Fingerprinting (C17 MCSD Layer 2)

C17 MCSD Layer 2, an existing AAS specification, provides pairwise behavioral similarity B(a_i, a_j) across five modalities (temporal, structural, error, resource, lexical) with LSH acceleration and graduated response (CLEAR / WATCH / FLAG).

**Strengths.** C17 is AAS-native, already specified, and provides the most informative single behavioral similarity metric in the platform. Its LSH-accelerated O(n*k) scaling is efficient. The 5-modality fusion captures diverse behavioral dimensions.

**Gaps relative to C35.** C17 provides pairwise similarity but does not distinguish structurally expected similarity from adversarial similarity. Two agents on the same committee in the same tidal phase will naturally have high B scores -- C17 flags them as potentially suspicious even when their similarity is entirely legitimate. C17 also lacks: (a) per-agent temporal anomaly detection -- it compares agents to each other, not to their own historical baselines; (b) multi-source evidence fusion -- it operates on behavioral data only, without verification, infrastructure, or economic signals; (c) causal attribution -- it identifies similar pairs but does not trace backward to a common origin.

**C35's relationship to C17.** C35 consumes C17 as a data source (contract XL-7), using B(a_i, a_j) as input to the behavioral channel and B_self for the per-agent behavioral consistency metric. C35 adds structural correction (via PCM) to C17's output, reducing false positives from legitimate similarity. The relationship is complementary: C17 measures, C35 contextualizes and escalates.

### 13.6 Standard IDS (Snort/Suricata Pattern Matching)

Snort and Suricata are signature-based intrusion detection systems that match network traffic against a database of known attack patterns (rules). They represent the dominant paradigm in network security monitoring.

**Strengths.** Signature-based IDS provides deterministic, explainable detection of known threats. Rule databases are maintained by large security communities. False positive rates are low for well-maintained rule sets. Processing is fast (wire-speed on modern hardware).

**Gaps relative to C35.** Signature-based IDS detects known attack patterns; it cannot detect novel threats, behavioral anomalies, or coordination patterns that do not match a pre-defined signature. AAS faces a threat landscape where attack patterns are not catalogued -- verification gaming, tidal scheduling manipulation, settlement fraud, and knowledge poisoning are domain-specific threats without established signature databases. Additionally, IDS operates on network packets, not on application-layer behavioral metrics. The abstraction level is wrong for AAS's threat model.

**Distinction from C35.** C35 is an anomaly-based system, not a signature-based system. It detects deviations from expected behavior (via STA/LTA, PCM residuals, overdispersion analysis) rather than matching against known patterns. This allows detection of novel threats at the cost of higher false positive rates -- a trade-off that the three-tier escalation pipeline mitigates by requiring progressive confirmation.

### 13.7 Comparison Summary

| Feature | SentinelAgent | MIDAS | SybilRank | Config-Model | C17 MCSD | Snort/Suricata | **C35** |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Multi-agent anomaly detection | Yes | Edge only | Sybil only | Community | Pairwise | Signature | **Yes** |
| Structural covariate correction | No | No | No | Degree only | No | No | **5 covariates** |
| Per-agent temporal baseline | No | No | No | No | No | No | **Dual (fixed+adaptive)** |
| Multi-channel evidence fusion | No | No | No | No | 5 modalities | Rule AND/OR | **4 channels, 3-of-4 quorum** |
| Epoch-aware temporal hierarchy | No | No | No | No | Epoch-level | No | **3-tier epoch** |
| Epidemiological attribution | No | No | No | No | No | No | **Backward tracing** |
| Streaming incremental | No | Yes | No | No | LSH batch | Yes | **MIDAS-F streaming** |
| Adversarial calibration defense | No | MIDAS-F decay | No | No | SEB randomization | Rule update | **4-phase bootstrap** |
| AAS domain integration | No | No | No | No | C17 native | No | **6 cross-layer contracts** |

---

## 14. Risk Analysis and Open Questions

### 14.1 Ranked Risk Table

Risks are compiled from the Pre-Mortem Analysis (10 failure scenarios), the Feasibility Verdict (5 blocking conditions, 5 monitoring flags), and the Mid-DESIGN Review (8 design flags). Each risk is assessed on likelihood (LOW=1, MEDIUM=2, HIGH=3), severity (LOW=1, MEDIUM=2, HIGH=3, CRITICAL=4), and composite score (likelihood x severity). Mitigation status reflects the simplified architecture.

| ID | Risk Name | Likelihood | Severity | Composite | Mitigation Status |
|----|-----------|:---:|:---:|:---:|:---|
| R-01 | Calibration poisoning spiral | HIGH (3) | CRITICAL (4) | **12** | PARTIALLY MITIGATED. Two-phase bootstrap (raw similarity then PCM) prevents worst case. Canary agents absent. Residual: adversary who behaves normally during full bootstrap is undetectable (acknowledged). |
| R-02 | Integration cascade collapse | HIGH (3) | CRITICAL (4) | **12** | PARTIALLY MITIGATED. NMI hardening, advisory-not-authoritative output posture. Gap: no self-referential anomaly suppression; no ETR emission rate limiter (DF-2 from Mid-DESIGN). |
| R-03 | PCM divergence catastrophe | HIGH (3) | HIGH (3) | **9** | MITIGATED. Main-effects-only model (S-01) eliminates multicollinearity from interaction terms. Ridge regularization (lambda=0.01). R-squared fallback at 0.70. Condition number risk substantially reduced by simplification. |
| R-04 | Cross-neighborhood Sybil swarm | MEDIUM (2) | CRITICAL (4) | **8** | NOT MITIGATED. Architecture requires within-neighborhood aggregation for Tier 2. One-per-neighborhood adversary bypasses Tier 2 entirely. DF-5 global residual aggregation proposed but not incorporated. |
| R-05 | Epoch desynchronization | MEDIUM (2) | HIGH (3) | **6** | NOT MITIGATED. Architecture assumes fixed 60s SETTLEMENT_TICKs. Tick rate changes require procedural intervention. |
| R-06 | Parameter tuning paralysis | MEDIUM (2) | HIGH (3) | **6** | PARTIALLY MITIGATED. Simplified architecture reduces parameters from 86 to ~66. Sensitivity classification (CRITICAL/SENSITIVE/ROBUST) prioritizes tuning. Joint optimization framework absent. |
| R-07 | Silent Tier 3 starvation | HIGH (3) | MEDIUM (2) | **6** | PARTIALLY MITIGATED. Minimum sample size lowered to 15 (S-12). Synthetic pool removed, accepting reduced statistical power at small scale. At 1K agents, Tier 3 may take multiple CONSOLIDATION_CYCLEs to accumulate data. |
| R-08 | Correlated channel resonance | LOW (1) | CRITICAL (4) | **4** | PARTIALLY MITIGATED. Quorum-only fusion (S-17) treats channels as independent. Channel correlation could inflate effective false positive rate. Bayesian fusion (deferred) would address this. |
| R-09 | NMI divergence arms race | MEDIUM (2) | MEDIUM (2) | **4** | MITIGATED. FC-5 game-theoretic analysis bounds attacker capability. Practical detection at B > 0.3*sqrt(V). Randomized perturbation prevents pre-compensation. |
| R-10 | Fixed baseline reconstructibility | LOW (1) | HIGH (3) | **3** | MITIGATED. FC-3 Red Team protocol: three-layer defense (Laplace noise + jitter + binary feedback). Information-theoretic analysis shows >10,000 transactions required, which is self-defeating. |

### 14.2 Open Questions

Five questions remain unresolved at the SPECIFICATION stage. Each is assigned a revisit trigger and a fallback position.

**OQ-1: PCM Interaction Terms**
*Status:* Deferred per S-01. The main-effects-only model (6 parameters/channel) is specified as the baseline. Interaction terms (10 additional parameters/channel) may improve R-squared by modeling non-additive covariate effects (e.g., committee coassignment x parcel colocation).
*Revisit trigger:* After W0 validation experiment EXP-3. If the main-effects model produces R-squared < 0.70 for > 20% of neighborhoods at 10K agents, add interaction terms incrementally. Criterion for inclusion: each interaction must improve held-out R-squared by at least 0.05.
*Fallback:* Main-effects model is conservative -- it produces larger residuals for unmodeled interactions, which biases toward false positives (detection) rather than false negatives (missed threats). This is the safer failure mode.

**OQ-2: Bayesian Channel Fusion**
*Status:* Deferred per S-17/S-18. The 3-of-4 quorum is specified as the permanent fusion mechanism. A learned fusion model (Bayesian network, logistic regression, or calibrated classifier) may improve detection of anomalies concentrated in 1-2 channels.
*Revisit trigger:* After 50 confirmed anomalies (the original Phase 2 transition criterion). At that point, real data exists to inform model structure and train conditional probability tables. Cross-validation accuracy > 0.85 required for activation.
*Fallback:* Quorum with single-channel high-confidence bypass. The quorum's false positive rate (~0.000481 per pair per epoch, ~63 false positives at 10K) is operationally manageable. The high-confidence bypass (2x MIDAS threshold) catches the strongest single-channel anomalies that the quorum would miss.

**OQ-3: PCM Convergence Formal Proof**
*Status:* Unresolved. The FC-1 simulation experiment protocol is designed (Section 3.2.9 of the architecture) but has not been executed. No formal convergence proof exists for the log-linear PCM under adversarial conditions with streaming incremental updates.
*Revisit trigger:* EXP-3 simulation results. Success criterion: parameter estimates within 10% of true values (relative L2 norm < 0.10) within 1,000 epochs for 95% of neighborhoods at 1K, 10K, and 100K scales. The DF-1 flag (Mid-DESIGN) requires an additional experimental condition with correlated covariates drawn from C3 scheduling simulation.
*Fallback:* If convergence fails, simplify the PCM further -- drop the lowest-contribution covariate(s) until convergence is achieved. In the extreme, a single-covariate model (committee coassignment only) reduces to a degree-adjusted residual similar to Newman (2010), which converges rapidly but loses multi-covariate correction.

**OQ-4: Cross-Neighborhood Sybil Swarm Defense**
*Status:* Unresolved (DF-5 from Mid-DESIGN). The architecture has no mechanism to detect an adversary who distributes agents one-per-neighborhood with diversified behavioral profiles. Tier 2 requires within-neighborhood aggregation, which this attack explicitly avoids.
*Proposed direction:* Lightweight global residual aggregation: at each CONSOLIDATION_CYCLE, test whether unconfirmed Tier 1 trigger distribution across neighborhoods is uniform (chi-squared test against Poisson expectation). A perfectly uniform trigger distribution is itself a dispersal anomaly signal -- natural triggers cluster by structural factors, while a deliberate one-per-neighborhood distribution produces anomalous uniformity.
*Fallback:* Rely on C17 MCSD and C12 AVAP for cross-neighborhood Sybil detection. Acknowledge that C35 provides no defense against this attack class until global aggregation is implemented.

**OQ-5: Tier 3 Statistical Power at Small Scale**
*Status:* Partially addressed by S-12 (lowered minimum to 15 anomalies, removed synthetic pool). At 1K agents, the expected Tier 2 anomaly rate is 2-5 per CONSOLIDATION_CYCLE; accumulating 15 real anomalies requires 3-8 cycles (30-80 hours). During this accumulation period, Tier 3 operates in DORMANT mode with reduced attribution capability.
*Revisit trigger:* Operational data from W0 deployment. If the real anomaly rate at 1K agents is lower than projected (< 1 per CONSOLIDATION_CYCLE), Tier 3 may be effectively permanently dormant at small scale.
*Fallback:* At 1K agents, manual review and C12 AVAP provide alternative attribution pathways. Tier 3's value proposition is primarily at 10K+ scale where manual review is impractical. The reduced statistical power at 15 anomalies (estimated ~50-55% vs. ~65% at 30) is acceptable for a mechanism that is supplementary, not primary.

### 14.3 Residual Risks

Three residual risks are acknowledged as having no complete defense within C35's architecture. These are not design failures; they are fundamental limitations of the detection paradigm.

**Residual Risk 1: Adversary Who Behaves Normally During Calibration and Activates Later.**
An adversary who registers agents, operates them identically to legitimate agents for the entire calibration window (100 TIDAL_EPOCHS = ~4.17 days for fixed baseline; 1,000 epochs for PCM convergence), and only activates adversarial behavior afterward will have legitimate fixed baselines and will be absorbed into the PCM's structural model. The PCM's R-squared check cannot detect poisoning that occurred during calibration because the calibration data is the training data. This is equivalent to the training-data poisoning problem in supervised learning: the model trusts its training set.
*Bound:* A single adversarial agent within a neighborhood of ~27 agents contributes at most 1/C(27,2) = 1/351 = 0.28% of pairwise training data. Its coefficient influence is bounded by the ridge regularization penalty. Five coordinated agents in one neighborhood could produce up to ~20% coefficient bias on targeted covariates, but would need to avoid triggering Tier 1 throughout the calibration period.
*Mitigation path:* Cross-validation against C12 AVAP independent signals. Periodic PCM recalibration with exponential forgetting (not specified in current architecture, deferred to post-W0).

**Residual Risk 2: Subtle PCM Coefficient Manipulation That Passes R-squared Check.**
An adversary who biases PCM coefficients by less than the R-squared degradation threshold (0.70) while shifting the expected correlation envelope by a small but strategically useful amount. For example, inflating the expected correlation for parcel-colocated agents by 0.05 units would allow colluding agents on the same parcel to exhibit 0.05 units more correlation before triggering a residual alarm. The R-squared metric measures overall model fit, not per-covariate accuracy; a small, targeted bias may not degrade R-squared measurably.
*Bound:* The 0.05-unit envelope expansion allows agents to correlate at natural + 0.05 without detection. Under the simplified main-effects model, the residual threshold for the verification channel is 0.15 (architecture Section 3.3.2). An envelope expansion of 0.05 reduces the effective residual threshold to 0.10, increasing the false negative rate for that channel by an estimated 15-25%.
*Mitigation path:* Per-covariate coefficient monitoring (condition number, VIF analysis) at each CONSOLIDATION_CYCLE. Implemented in the architecture's ridge regularization but not as a separate diagnostic alert.

**Residual Risk 3: Cross-Neighborhood Distributed Attack Below Per-Neighborhood Thresholds.**
Documented in OQ-4. An adversary distributing agents one-per-neighborhood produces per-neighborhood anomaly counts of exactly 1, which falls below Tier 2's minimum pair count (2 anomalous pairs per neighborhood per epoch) and never triggers Tier 2 confirmation. Tier 3 never receives input. At V = 100,000 with ~3,013 neighborhoods, the adversary could deploy up to 3,013 agents (one per neighborhood) operating below individual detection thresholds but collectively producing a systematic platform-wide effect.
*Bound:* Each dispersed agent's individual behavior must remain below Tier 1's confirmation threshold (3-5 ticks of sign-agreement confirmation). The platform-wide impact is bounded by the per-agent damage capacity: if each agent can cast 1-2 incorrect verification votes per 100 epochs, the system-wide error rate is bounded by (3,013 agents x 2 votes) / (total votes per 100 epochs). At 100K agents averaging 10 votes per epoch, total votes per 100 epochs = 100M, and adversarial error rate = 6,026 / 100,000,000 = 0.006%. This is a non-trivial but bounded degradation.
*Mitigation path:* Global Tier 1 trigger distribution analysis (OQ-4), C17 behavioral similarity detection, C12 AVAP independent collusion mechanisms.

---

## 15. Patent-Style Claims

The following claims describe the novel aspects of C35 in patent-style language. Claims are intended to delineate the intellectual contribution of the Seismographic Sentinel architecture, distinguishing it from prior art in anomaly detection, network analysis, and multi-agent security.

**Claim 1.** A method for detecting anomalous behavior in a distributed multi-agent verification system, comprising:
(a) computing, for each agent, a ratio of short-term average (STA) to long-term average (LTA) of behavioral metrics across four metric channels derived from cross-layer data sources, said channels comprising verification latency, claim acceptance rate, committee assignment frequency, and behavioral self-consistency;
(b) comparing said ratio against dual parallel baselines comprising a fixed baseline established during a calibration period and an adaptive baseline updated via exponential moving average;
(c) applying an OR-trigger that enters a candidate state when either baseline exceeds a channel-specific threshold, followed by a confirmation window requiring sign-agreement with relaxation across subsequent observation ticks;
(d) upon confirmation, escalating the trigger to a regional correlation analysis tier with annotated metadata comprising metric values, baseline source, triggering channels, anomaly direction, and composite confidence score.

**Claim 2.** The method of Claim 1, further comprising, at the regional correlation analysis tier:
(a) partitioning the agent population into neighborhoods via spectral clustering on a weighted interaction graph, said graph incorporating behavioral similarity scores and structural covariate similarity, with a cluster size cap of 2*log_2(V) and split-on-overflow via recursive Fiedler bisection;
(b) computing, for each within-neighborhood agent pair and each metric channel, a Permitted Correlation Model (PCM) expected correlation using a log-linear regression of structural covariates, said covariates comprising parcel colocation, committee coassignment, epoch coregistration, claim class overlap, and tidal phase alignment;
(c) computing the PCM residual as the difference between observed pairwise correlation and the PCM-predicted expected correlation;
(d) feeding said residuals to a MIDAS-F streaming edge anomaly detector that flags edges whose residual frequency exceeds a chi-squared statistical threshold with temporal decay resistance;
(e) confirming an agent pair as anomalous only when the pair satisfies both the MIDAS-F temporal anomaly criterion and the PCM residual magnitude criterion on the same channel.

**Claim 3.** The method of Claim 2, further comprising a multi-channel quorum fusion step wherein an agent pair is confirmed as a Tier 2 anomaly only when at least three of the four metric channels independently satisfy the joint MIDAS-F and PCM residual criterion, said quorum providing false-positive reduction under the assumption of channel independence.

**Claim 4.** The method of Claim 2, wherein the PCM log-linear model is estimated at each consolidation cycle via ridge-regularized maximum likelihood estimation on within-neighborhood agent pairs, with a precomputed lookup table storing expected correlations for all pairs, and wherein a coverage metric (R-squared) is monitored per neighborhood-channel combination, with fallback to raw behavioral similarity when R-squared falls below a configured threshold, thereby maintaining detection capability when the structural model is non-predictive.

**Claim 5.** The method of Claim 1, further comprising a global threat synthesis tier that:
(a) activates when the count of confirmed Tier 2 anomalies within a sliding analysis window exceeds a minimum threshold;
(b) performs overdispersion analysis on per-agent anomaly counts using a negative binomial regression model with covariates comprising operator identity, registration cohort, geographic cluster, and infrastructure provider;
(c) upon detecting statistically significant overdispersion (alpha-hat exceeding a configured threshold), constructs a temporal-behavioral phylogeny by tracing backward through behavioral similarity chains and intent provenance records;
(d) identifies the most probable common causal ancestor via maximum likelihood estimation over the phylogeny structure;
(e) produces an attribution report with posterior confidence, evidence chain, and recommended governance action.

**Claim 6.** A system for providing a shared detection substrate to a multi-layer distributed agent platform, comprising:
(a) an authenticated cluster-membership service interface that exposes neighborhood assignments, per-agent anomaly levels, and neighborhood health scores to attested consuming platform specifications including scheduling, verification, orchestration, settlement, and Sybil defense subsystems;
(b) a bounded-staleness consistency model wherein the cache is refreshed at each consolidation cycle and queries between refreshes return the most recent valid partition;
(c) a degradation protocol wherein consuming specifications fall back to independent operation when the sentinel subsystem is unavailable, ensuring that the detection substrate is advisory and does not create a single point of failure for platform operation.

**Claim 7.** The method of Claim 1, further comprising a sentinel_health self-monitoring subsystem that:
(a) tracks the operational state of each tier (NOMINAL, DEGRADED, OFFLINE) and each cross-layer data source (ACTIVE, CACHED, STALE, UNAVAILABLE);
(b) computes a composite health score reflecting the fraction of the agent population under active monitoring, the fraction of neighborhoods with valid PCM calibration, and the latency of cross-layer data feeds;
(c) publishes the health state to the platform orchestration layer for resource allocation decisions, enabling the platform to distinguish between "sentinel reports no anomalies" and "sentinel is unable to detect anomalies."

---

## 16. Glossary

| Term | Definition |
|------|-----------|
| **STA** | Short-Term Average. Arithmetic mean of the most recent w_s metric values (default w_s = 5 ticks = 300 seconds). Captures recent agent behavior. |
| **LTA** | Long-Term Average. Arithmetic mean of the most recent w_l metric values (default w_l = 60 ticks = 3,600 seconds). Captures baseline agent behavior over one TIDAL_EPOCH. |
| **STA/LTA Ratio** | The ratio STA/LTA for a given metric channel. Values near 1.0 indicate normal behavior; significant deviations indicate anomaly. Borrowed from seismological P-wave arrival detection (Allen, 1978). |
| **PCM** | Permitted Correlation Model. A log-linear regression that predicts expected pairwise correlation between agents from structural covariates. The PCM residual (observed minus expected) isolates unexplained correlation. |
| **MIDAS** | Microcluster-Based Detector of Anomalies in Edge Streams (Bhatia et al., 2020). A streaming algorithm using count-min sketches for constant-time edge anomaly detection. C35 uses the MIDAS-F (Filtered) variant with temporal decay. |
| **MIDAS-F** | MIDAS with temporal decay (filtered variant). Applies an exponential decay factor to historical CMS counts, resisting state poisoning attacks that inflate expected counts. |
| **NMI** | Normalized Mutual Information. An information-theoretic measure of clustering similarity, used in C35 to assess spectral clustering stability under perturbation. NMI = 1.0 indicates identical clusterings; NMI = 0.0 indicates no mutual information. |
| **Overdispersion** | A statistical property where the variance of a count distribution exceeds its mean. In C35 Tier 3, overdispersion in per-agent anomaly counts indicates a common causal source (operator control, shared infrastructure) rather than independent anomaly occurrence. Quantified by the alpha parameter of the negative binomial distribution. |
| **Quorum** | A k-of-n voting rule for multi-channel evidence fusion. C35 uses a 3-of-4 quorum: an agent pair is confirmed anomalous only when at least 3 of the 4 metric channels independently flag it. |
| **Sentinel Health** | A composite metric reflecting C35's own operational state: fraction of agents monitored, fraction of neighborhoods calibrated, data feed latency. Distinguishes "no anomalies detected" from "detection capability impaired." |
| **Dual Baseline** | The combination of a fixed baseline (immutable after calibration, detects absolute deviation) and an adaptive baseline (EMA-updated, detects deviation from recent behavior). The two baselines are fused via OR-trigger with confirmation. |
| **Confirmation Window** | A short observation period (3-5 ticks) during which a Tier 1 candidate trigger must persist with sign-agreement to be confirmed. Filters transient noise and coincidental single-tick anomalies. |
| **PCM Residual** | R_c(a_i, a_j) = corr_c_observed - E[corr_c]. The difference between observed and structurally expected pairwise correlation on channel c. Positive residuals indicate unexplained correlation; negative residuals indicate unexplained decorrelation. |
| **Backward Tracing** | The Tier 3 process of constructing a temporal-behavioral phylogeny from confirmed anomalies back through interaction history, querying C17 behavioral similarity and C7 intent provenance to identify a common causal ancestor. |
| **CONSOLIDATION_CYCLE** | The longest epoch in the C9 three-tier hierarchy: 36,000 seconds (10 hours). C35 recomputes spectral clustering, refits PCM parameters, and refreshes the Bayesian prior (if active) at this cadence. |
| **Structural Covariates** | The five platform-structural features that predict legitimate inter-agent correlation: parcel colocation (x_1), committee coassignment (x_2), epoch coregistration (x_3), claim class overlap (x_4), and tidal phase alignment (x_5). |

---

## 17. Parameter Registry (Appendix A)

All configurable parameters for the simplified C35 architecture (~66 parameters), grouped by subsystem.

### 17.1 Tier 1 Parameters

| # | Name | Type | Default | Range | Sensitivity | Section |
|---|------|------|---------|-------|-------------|---------|
| 1 | TIER1_STA_WINDOW_TICKS | u16 | 5 | [3, 15] | SENSITIVE | 2.4.1 |
| 2 | TIER1_LTA_WINDOW_TICKS | u16 | 60 | [30, 120] | SENSITIVE | 2.4.2 |
| 3 | TIER1_ADAPTIVE_ALPHA | f64 | 0.01 | [0.001, 0.1] | CRITICAL | 2.6.1 |
| 4 | TIER1_THETA_LATENCY | f64 | 0.40 | [0.05, 1.0] | CRITICAL | 2.6.2 |
| 5 | TIER1_THETA_ACCEPTANCE | f64 | 0.25 | [0.05, 1.0] | CRITICAL | 2.6.2 |
| 6 | TIER1_THETA_COMMITTEE | f64 | 0.50 | [0.05, 1.0] | SENSITIVE | 2.6.2 |
| 7 | TIER1_THETA_CONSISTENCY | f64 | 0.20 | [0.05, 1.0] | CRITICAL | 2.6.2 |
| 8 | TIER1_BASE_CONFIRM_WINDOW | u8 | 3 | [2, 10] | SENSITIVE | 2.7.1 |
| 9 | TIER1_DENSITY_SIGMA | f64 | 2.0 | [1.0, 4.0] | ROBUST | 2.7.1 |
| 10 | TIER1_ALPHA_CONFIRM | f64 | 0.70 | [0.5, 1.0] | SENSITIVE | 2.7.1 |
| 11 | TIER1_DUAL_TRIGGER_MIN_CHANNELS | u8 | 1 | [1, 4] | SENSITIVE | 2.7.2 |
| 12 | TIER1_BASELINE_PRIVACY_EPSILON | f64 | 1.0 | [0.1, 10.0] | ROBUST | 2.5.3 |
| 13 | TIER1_CALIBRATION_EPOCHS | u16 | 100 | [50, 500] | SENSITIVE | 2.5.1 |
| 14 | TIER1_ESCALATION_BUFFER_TICKS | u16 | 100 | [10, 1000] | ROBUST | 2.8 |
| 15 | TIER1_JITTER_RANGE | f64 | 0.05 | [0.01, 0.20] | ROBUST | 7.2 |
| 16 | TIER1_C5_SILENCE_THRESHOLD | u8 | 3 | [1, 10] | ROBUST | 5.2 |

### 17.2 Tier 2 -- Neighborhood Parameters

| # | Name | Type | Default | Range | Sensitivity | Section |
|---|------|------|---------|-------|-------------|---------|
| 17 | TIER2_CLUSTERING_LAMBDA_B | f64 | 0.60 | [0.0, 1.0] | SENSITIVE | 3.1.1 |
| 18 | TIER2_CLUSTERING_LAMBDA_S | f64 | 0.40 | [0.0, 1.0] | SENSITIVE | 3.1.1 |
| 19 | TIER2_NMI_SIGMA | f64 | 0.10 | [0.01, 0.50] | SENSITIVE | 3.1.3 |
| 20 | TIER2_NMI_THRESHOLD | f64 | 0.70 | [0.50, 0.95] | CRITICAL | 3.1.3 |
| 21 | TIER2_MIN_CLUSTER_SIZE | u8 | 3 | [2, 10] | ROBUST | 3.1.2 |

### 17.3 Tier 2 -- PCM Parameters (Simplified: Main-Effects Only)

| # | Name | Type | Default | Range | Sensitivity | Section |
|---|------|------|---------|-------|-------------|---------|
| 22 | PCM_LAMBDA_REG | f64 | 0.01 | [0.001, 1.0] | CRITICAL | 3.2.4 |
| 23 | PCM_R_SQUARED_THRESHOLD | f64 | 0.70 | [0.50, 0.95] | CRITICAL | 3.2.8 |
| 24 | PCM_MIN_COPAIRS | u16 | 30 | [10, 100] | SENSITIVE | 3.2.4 |
| 25 | PCM_BETA_0_INIT | f64 | 0.0 | [-5.0, 5.0] | ROBUST | 3.2.1 |
| 26 | PCM_BETA_PARCEL_INIT | f64 | 0.0 | [-5.0, 5.0] | ROBUST | 3.2.1 |
| 27 | PCM_BETA_COMMITTEE_INIT | f64 | 0.0 | [-5.0, 5.0] | ROBUST | 3.2.1 |
| 28 | PCM_BETA_EPOCH_INIT | f64 | 0.0 | [-5.0, 5.0] | ROBUST | 3.2.1 |
| 29 | PCM_BETA_CLAIMCLASS_INIT | f64 | 0.0 | [-5.0, 5.0] | ROBUST | 3.2.1 |
| 30 | PCM_BETA_TIDALPHASE_INIT | f64 | 0.0 | [-5.0, 5.0] | ROBUST | 3.2.1 |

*Note: Parameters 25-30 are initial values only; MLE updates them at each CONSOLIDATION_CYCLE. There are 4 independent channel instances x 6 parameters = 24 fitted PCM coefficients total, but only 6 initial-value parameters because all channels share the same initialization.*

### 17.4 Tier 2 -- MIDAS Parameters

| # | Name | Type | Default | Range | Sensitivity | Section |
|---|------|------|---------|-------|-------------|---------|
| 31 | TIER2_MIDAS_CMS_WIDTH | u16 | 512 | [128, 2048] | SENSITIVE | 3.3.1 |
| 32 | TIER2_MIDAS_CMS_DEPTH | u8 | 4 | [2, 8] | ROBUST | 3.3.1 |
| 33 | TIER2_MIDAS_THRESHOLD | f64 | 3.84 | [1.0, 20.0] | CRITICAL | 3.3.3 |
| 34 | TIER2_MIDAS_DECAY | f64 | 0.95 | [0.80, 0.99] | SENSITIVE | 3.3.4 |
| 35 | TIER2_MIDAS_WARMUP_EPOCHS | u8 | 3 | [1, 10] | ROBUST | 3.3.5 |

### 17.5 Tier 2 -- Channel and Residual Parameters

| # | Name | Type | Default | Range | Sensitivity | Section |
|---|------|------|---------|-------|-------------|---------|
| 36 | TIER2_BASE_RESIDUAL_THRESHOLD | f64 | 0.15 | [0.01, 0.50] | CRITICAL | 3.3.2 |
| 37 | TIER2_VERIFICATION_CORR_W_ACCEPT | f64 | 0.40 | [0.0, 1.0] | ROBUST | 3.4.1 |
| 38 | TIER2_VERIFICATION_CORR_W_TIMING | f64 | 0.35 | [0.0, 1.0] | ROBUST | 3.4.1 |
| 39 | TIER2_VERIFICATION_CORR_W_VTD | f64 | 0.25 | [0.0, 1.0] | ROBUST | 3.4.1 |
| 40 | TIER2_BEHAVIORAL_CORR_W_BSCORE | f64 | 0.70 | [0.0, 1.0] | ROBUST | 3.4.2 |
| 41 | TIER2_BEHAVIORAL_CORR_W_LCS | f64 | 0.30 | [0.0, 1.0] | ROBUST | 3.4.2 |
| 42 | TIER2_INFRA_CORR_W_IP | f64 | 0.20 | [0.0, 1.0] | ROBUST | 3.4.3 |
| 43 | TIER2_INFRA_CORR_W_LATENCY | f64 | 0.40 | [0.0, 1.0] | ROBUST | 3.4.3 |
| 44 | TIER2_INFRA_CORR_W_RESOURCE | f64 | 0.40 | [0.0, 1.0] | ROBUST | 3.4.3 |
| 45 | TIER2_ECON_CORR_W_SETTLE | f64 | 0.35 | [0.0, 1.0] | ROBUST | 3.4.4 |
| 46 | TIER2_ECON_CORR_W_STAKING | f64 | 0.35 | [0.0, 1.0] | ROBUST | 3.4.4 |
| 47 | TIER2_ECON_CORR_W_REWARD | f64 | 0.30 | [0.0, 1.0] | ROBUST | 3.4.4 |

### 17.6 Tier 2 -- Fusion Parameters

| # | Name | Type | Default | Range | Sensitivity | Section |
|---|------|------|---------|-------|-------------|---------|
| 48 | TIER2_QUORUM_K | u8 | 3 | [2, 4] | CRITICAL | 3.5.1 |
| 49 | TIER2_HIGH_CONF_BYPASS_FACTOR | f64 | 2.0 | [1.5, 5.0] | SENSITIVE | 3.5.1 |
| 50 | TIER2_CONFIDENCE_FLOOR | f64 | 0.70 | [0.50, 0.95] | SENSITIVE | 3.6.3 |
| 51 | TIER2_MIN_PAIRS_ESCALATION | u8 | 2 | [1, 10] | SENSITIVE | 3.6.3 |
| 52 | TIER2_RECENCY_COOLDOWN_EPOCHS | u8 | 10 | [3, 30] | ROBUST | 3.6.3 |
| 53 | TIER2_RECENCY_ELEVATED_PAIRS | u8 | 4 | [2, 10] | ROBUST | 3.6.3 |
| 54 | TIER2_RECENCY_ELEVATED_CONF | f64 | 0.85 | [0.70, 0.99] | ROBUST | 3.6.3 |

### 17.7 Tier 3 Parameters

| # | Name | Type | Default | Range | Sensitivity | Section |
|---|------|------|---------|-------|-------------|---------|
| 55 | TIER3_MIN_ANOMALIES | u16 | 15 | [5, 100] | CRITICAL | 4.1 |
| 56 | TIER3_ANALYSIS_WINDOW_EPOCHS | u8 | 10 | [5, 30] | SENSITIVE | 4.1 |
| 57 | TIER3_MAX_CONCURRENT | u8 | 3 | [1, 10] | ROBUST | 4.1 |
| 58 | TIER3_POSTERIOR_THRESHOLD | f64 | 0.80 | [0.50, 0.99] | SENSITIVE | 4.1 |
| 59 | TIER3_ALPHA_THRESHOLD | f64 | 2.0 | [0.5, 10.0] | CRITICAL | 4.2 |
| 60 | TIER3_LR_SIGNIFICANCE | f64 | 2.71 | [1.0, 10.0] | ROBUST | 4.2 |
| 61 | TIER3_ATTRIBUTION_THRESHOLD | f64 | 0.90 | [0.70, 0.99] | SENSITIVE | 4.3 |
| 62 | TIER3_DORMANT_TO_ACTIVE | u16 | 15 | [5, 100] | SENSITIVE | 4.5 |
| 63 | TIER3_COOCCURRENCE_MIN_FRACTION | f64 | 0.30 | [0.10, 0.80] | ROBUST | 4.3 |

### 17.8 Cross-Layer Parameters

| # | Name | Type | Default | Range | Sensitivity | Section |
|---|------|------|---------|-------|-------------|---------|
| 64 | XL_CACHE_STALE_TICKS | u16 | 100 | [10, 1000] | ROBUST | 5.1 |
| 65 | XL_DEGRADATION_THRESHOLD_FRACTION | f64 | 0.30 | [0.10, 0.50] | SENSITIVE | 2.9.1 |
| 66 | XL_ADVISORY_TTL_EPOCHS | u8 | 10 | [3, 30] | ROBUST | 5.4 |

### 17.9 Parameter Count Summary

| Group | Count | CRITICAL | SENSITIVE | ROBUST |
|-------|:---:|:---:|:---:|:---:|
| Tier 1 | 16 | 4 | 6 | 6 |
| Tier 2 Neighborhoods | 5 | 1 | 3 | 1 |
| Tier 2 PCM | 9 | 2 | 1 | 6 |
| Tier 2 MIDAS | 5 | 1 | 2 | 2 |
| Tier 2 Channels | 12 | 1 | 0 | 11 |
| Tier 2 Fusion | 7 | 1 | 3 | 3 |
| Tier 3 | 9 | 2 | 4 | 3 |
| Cross-Layer | 3 | 0 | 1 | 2 |
| **Total** | **66** | **12** | **20** | **34** |

The 12 CRITICAL parameters should be the priority for W0 calibration experiments. The 20 SENSITIVE parameters require attention during DESIGN validation but can tolerate moderate variation. The 34 ROBUST parameters can use literature defaults without calibration.

---

## 18. Pseudocode (Appendix B)

### 18.1 Tier 1 Per-Tick Processing

```
fn tier1_process_tick(agent: &mut Tier1AgentState, metrics: [f64; 4], tick: u64):
    // Step 1: Ingest metrics into STA and LTA windows
    for c in 0..4:
        if metrics[c].is_stale():
            agent.sta_window[c].mark_stale(tick)
            agent.lta_window[c].mark_stale(tick)
            continue

        agent.sta_window[c].push(metrics[c])
        agent.lta_window[c].push(metrics[c])

        // Update adaptive baseline (EMA)
        agent.adaptive_baseline[c] =
            TIER1_ADAPTIVE_ALPHA * metrics[c]
            + (1.0 - TIER1_ADAPTIVE_ALPHA) * agent.adaptive_baseline[c]

    // Step 2: Compute STA/LTA ratios
    let mut ratios = [0.0_f64; 4]
    let mut valid_channels = [false; 4]
    for c in 0..4:
        let sta = agent.sta_window[c].mean()
        let lta = agent.lta_window[c].mean()
        if lta.is_none() or lta.unwrap() < EPSILON:
            valid_channels[c] = false
            continue
        ratios[c] = sta.unwrap() / lta.unwrap()
        valid_channels[c] = true

    // Step 3: Check fixed baseline anomaly (if calibrated)
    let mut fixed_trigger = [Direction::NONE; 4]
    if agent.calibration_status == CALIBRATED:
        for c in 0..4:
            if not valid_channels[c]: continue
            if metrics[c] > agent.fixed_baseline.p95[c]:
                fixed_trigger[c] = Direction::POSITIVE
            elif metrics[c] < agent.fixed_baseline.p05[c]:
                fixed_trigger[c] = Direction::NEGATIVE

    // Step 4: Check adaptive baseline anomaly
    let mut adaptive_trigger = [Direction::NONE; 4]
    for c in 0..4:
        if not valid_channels[c]: continue
        let theta = [TIER1_THETA_LATENCY, TIER1_THETA_ACCEPTANCE,
                      TIER1_THETA_COMMITTEE, TIER1_THETA_CONSISTENCY][c]
        if ratios[c] - 1.0 > theta:
            adaptive_trigger[c] = Direction::POSITIVE
        elif ratios[c] - 1.0 < -theta:
            adaptive_trigger[c] = Direction::NEGATIVE

    // Step 5: Dual-trigger bypass check
    let mut bypass = false
    let mut bypass_channels = 0_u8
    for c in 0..4:
        if fixed_trigger[c] != Direction::NONE
           and fixed_trigger[c] == adaptive_trigger[c]:
            bypass_channels += 1
    if bypass_channels >= TIER1_DUAL_TRIGGER_MIN_CHANNELS:
        bypass = true

    // Step 6: Decision fusion
    match agent.trigger_state:
        IDLE:
            if bypass:
                agent.trigger_state = CONFIRMED
                emit_trigger_annotation(agent, tick, metrics, ratios,
                                        fixed_trigger, adaptive_trigger, true)
                agent.trigger_state = IDLE  // reset after emission
            else:
                // OR-trigger: any baseline on any channel
                let any_trigger = fixed_trigger.iter().any(|d| *d != NONE)
                                  or adaptive_trigger.iter().any(|d| *d != NONE)
                if any_trigger:
                    agent.trigger_state = CANDIDATE
                    agent.candidate_tick = tick
                    agent.confirmation_count = 0
                    let cw = TIER1_BASE_CONFIRM_WINDOW
                             + density_z_score().floor() as u8
                    agent.confirmation_required = cw.clamp(3, 10)

        CANDIDATE:
            // Sign-agreement check with relaxation
            let confirmed_this_tick = false
            for c in 0..4:
                if not valid_channels[c]: continue
                let d_f = fixed_trigger[c]
                let d_a = adaptive_trigger[c]
                if sign_agree(d_f, d_a):
                    // Magnitude relaxation when both trigger
                    if d_f != NONE and d_a != NONE:
                        let mag_f = magnitude_fixed(metrics[c], agent, c)
                        let mag_a = magnitude_adaptive(ratios[c], c)
                        let stronger = f64::max(mag_f, mag_a)
                        let weaker = f64::min(mag_f, mag_a)
                        if weaker / stronger >= TIER1_ALPHA_CONFIRM:
                            confirmed_this_tick = true
                    else:
                        confirmed_this_tick = true  // one-sided agreement

            if confirmed_this_tick:
                agent.confirmation_count += 1
            if agent.confirmation_count >= agent.confirmation_required:
                agent.trigger_state = CONFIRMED
                emit_trigger_annotation(agent, tick, metrics, ratios,
                                        fixed_trigger, adaptive_trigger, false)
                agent.trigger_state = IDLE
            elif tick - agent.candidate_tick > agent.confirmation_required + 2:
                agent.trigger_state = IDLE  // window expired

        DEGRADED:
            // No processing; wait for channel recovery
            pass

fn sign_agree(d_fixed: Direction, d_adaptive: Direction) -> bool:
    match (d_fixed, d_adaptive):
        (NONE, NONE)         => false  // neither triggered
        (NONE, _)            => true   // one-sided: adaptive only
        (_, NONE)            => true   // one-sided: fixed only
        (POSITIVE, POSITIVE) => true   // agreement
        (NEGATIVE, NEGATIVE) => true   // agreement
        _                    => false  // contradiction
```

### 18.2 Tier 2 Neighborhood Activation

```
fn tier2_process_epoch(neighborhood: &mut NeighborhoodState, epoch: u64):
    // Collect Tier 1 triggers from this epoch
    let triggers = neighborhood.trigger_queue.drain_epoch(epoch)

    // Event-driven activation: check trigger density
    let trigger_density = triggers.len() as f64 / neighborhood.agent_count as f64
    let density_anomalous = trigger_density > neighborhood.mean_density_100
                            + 2.0 * neighborhood.sigma_density_100

    // Batch analysis: runs every TIDAL_EPOCH regardless
    let pairs = neighborhood.all_agent_pairs()

    for (a_i, a_j) in pairs:
        let mut channel_anomalous = [false; 4]

        for c in 0..4:
            // Step 1: Compute observed correlation over this epoch
            let obs_corr = compute_pearson(
                neighborhood.metric_series[a_i][c],
                neighborhood.metric_series[a_j][c],
                epoch_window=60)

            // Step 2: Lookup PCM expected correlation
            let exp_corr = neighborhood.pcm_store.lookup(a_i, a_j, c)

            // Step 3: Check PCM coverage
            let r_sq = neighborhood.pcm_store.r_squared[c]
            let residual: f64
            if r_sq >= PCM_R_SQUARED_THRESHOLD:
                residual = obs_corr - exp_corr
            else:
                // Fallback: raw similarity minus scaled B-score
                let b_score = c17_get_similarity(a_i, a_j)
                let rho_c = neighborhood.channel_b_scale[c]
                residual = obs_corr - b_score * rho_c

            // Step 4: Residual threshold (derived from base threshold)
            let residual_std = neighborhood.pcm_store.residual_std[c]
            let mean_std = neighborhood.pcm_store.mean_residual_std()
            let threshold_r = TIER2_BASE_RESIDUAL_THRESHOLD
                              * (residual_std / mean_std).max(0.5).min(2.0)

            if residual.abs() > threshold_r:
                // Step 5: MIDAS-F scoring
                let midas_score = neighborhood.midas[c].score_edge(a_i, a_j)
                if midas_score > TIER2_MIDAS_THRESHOLD:
                    channel_anomalous[c] = true

            // Record raw + residual (Condition C-1)
            neighborhood.tier2_log.record(a_i, a_j, c, obs_corr, exp_corr,
                                          residual, midas_score)

        // Step 6: Quorum fusion (3-of-4)
        let anomalous_count = channel_anomalous.iter()
                                .filter(|&&x| x).count()

        let confirmed = anomalous_count >= TIER2_QUORUM_K

        // High-confidence single-channel bypass
        if not confirmed:
            for c in 0..4:
                if channel_anomalous[c]:
                    let ms = neighborhood.midas[c].score_edge(a_i, a_j)
                    if ms > TIER2_MIDAS_THRESHOLD * TIER2_HIGH_CONF_BYPASS_FACTOR:
                        confirmed = true
                        break

        if confirmed:
            neighborhood.confirmed_anomalies.push(
                Tier2Anomaly { agents: (a_i, a_j), epoch, channels: channel_anomalous,
                               confidence: anomalous_count as f64 / 4.0 })

    // Step 7: Escalation check
    check_tier3_escalation(neighborhood, epoch)
```

### 18.3 PCM Precomputation (Simplified: Main-Effects Only)

```
fn pcm_refit(neighborhood: &mut NeighborhoodState, cycle: u64):
    let agents = neighborhood.agents()
    let pairs = all_pairs(agents)  // C(n, 2) pairs

    for c in 0..4:
        // Build design matrix X and response vector y
        let mut X: Vec<[f64; 6]> = vec![]  // 6 = 1 intercept + 5 main effects
        let mut y: Vec<f64> = vec![]

        for (a_i, a_j) in pairs:
            // Compute observed correlation over the full CONSOLIDATION_CYCLE
            let obs_corr = compute_pearson_cycle(a_i, a_j, c, cycle)
            if obs_corr.co_ticks < PCM_MIN_COPAIRS:
                continue  // insufficient co-observation

            // Structural covariates
            let x1 = parcel_colocation(a_i, a_j, cycle)     // [0, 1]
            let x2 = committee_coassignment(a_i, a_j, cycle) // [0, 1] Jaccard
            let x3 = epoch_coregistration(a_i, a_j)          // [0, 1]
            let x4 = claim_class_overlap(a_i, a_j, cycle)    // [0, 1] cosine
            let x5 = tidal_phase_alignment(a_i, a_j, cycle)  // [0, 1]

            let feature_vec = [1.0, x1, x2, x3, x4, x5]
            X.push(feature_vec)
            y.push(f64::ln(f64::max(obs_corr.value, EPSILON)))

        if X.len() < 6:
            // Insufficient data for 6-parameter fit
            neighborhood.pcm_store.r_squared[c] = 0.0
            continue

        // Ridge-regularized MLE: theta = (X^T X + lambda I)^{-1} X^T y
        let XtX = matrix_mult_transpose(X, X)  // 6x6
        let XtX_reg = matrix_add_diagonal(XtX, PCM_LAMBDA_REG)
        let Xty = matrix_vector_mult_transpose(X, y)  // 6x1
        let theta = solve_linear_system(XtX_reg, Xty)  // 6x1

        // Compute R-squared
        let y_pred = matrix_vector_mult(X, theta)
        let ss_res = sum_squared(y - y_pred)
        let ss_tot = sum_squared(y - mean(y))
        let r_sq = 1.0 - (ss_res / ss_tot)

        // Store parameters and R-squared
        neighborhood.pcm_store.parameters[c] = theta
        neighborhood.pcm_store.r_squared[c] = r_sq
        neighborhood.pcm_store.cycle = cycle

        // Precompute lookup table for all pairs
        for (a_i, a_j) in all_pairs(agents):
            let x = compute_feature_vec(a_i, a_j, cycle)
            let expected = f64::exp(dot(x, theta))
            neighborhood.pcm_store.lookup.insert((a_i, a_j, c), expected)

        // Compute residual standard deviation for adaptive thresholds
        let residuals: Vec<f64> = pairs_with_data.iter()
            .map(|(a_i, a_j)| obs_corr(a_i, a_j) - pcm_lookup(a_i, a_j, c))
            .collect()
        neighborhood.pcm_store.residual_std[c] = std_dev(residuals)
```

### 18.4 Channel Fusion (Simplified: Quorum Only)

```
fn channel_fusion_quorum(channel_evidence: [bool; 4],
                         midas_scores: [f64; 4]) -> FusionResult:
    // Count channels with confirmed anomalies
    let anomalous_count = channel_evidence.iter()
                            .filter(|&&x| x).count()

    // Primary: 3-of-4 quorum
    if anomalous_count >= TIER2_QUORUM_K:
        return FusionResult {
            confirmed: true,
            method: QUORUM,
            confidence: anomalous_count as f64 / 4.0,
            channels: channel_evidence,
        }

    // Secondary: high-confidence single-channel bypass
    for c in 0..4:
        if channel_evidence[c]
           and midas_scores[c] > TIER2_MIDAS_THRESHOLD * TIER2_HIGH_CONF_BYPASS_FACTOR:
            return FusionResult {
                confirmed: true,
                method: HIGH_CONFIDENCE_BYPASS,
                confidence: 0.60,  // lower confidence for single-channel
                channels: channel_evidence,
            }

    // Not confirmed
    return FusionResult {
        confirmed: false,
        method: QUORUM,
        confidence: anomalous_count as f64 / 4.0,
        channels: channel_evidence,
    }
```

### 18.5 Tier 3 Backward Tracing (Simplified: 2 Sources)

```
fn tier3_backward_trace(analysis_set: Vec<Tier2Anomaly>,
                        window: (u64, u64)) -> AttributionReport:
    // Step 1: Overdispersion analysis
    let agent_counts = count_per_agent(analysis_set)  // agent_id -> anomaly count
    let nb_result = fit_negative_binomial(
        response=agent_counts.values(),
        covariates=get_agent_covariates(agent_counts.keys()))
    //  covariates: operator_id, registration_cohort,
    //              geographic_cluster, infrastructure_provider

    if nb_result.lr_statistic < TIER3_LR_SIGNIFICANCE
       or nb_result.alpha_hat < TIER3_ALPHA_THRESHOLD:
        return AttributionReport {
            recommended_action: INSUFFICIENT_DATA,
            overdispersion: nb_result,
            attribution: None,
        }

    // Step 2: Seed set construction
    let seed_set: Vec<AgentID> = agent_counts.iter()
        .filter(|(_, count)| *count >= 2)
        .map(|(agent, _)| agent)
        .collect()

    if seed_set.is_empty():
        return AttributionReport {
            recommended_action: INCONCLUSIVE,
            overdispersion: nb_result,
            attribution: None,
        }

    // Step 3: Phylogeny construction (2 sources only)
    let mut phylogeny_edges: Vec<PhylogenyEdge> = vec![]

    // Source 1: C17 behavioral similarity chains
    for agent in seed_set:
        let neighbors = c17_get_similar_agents(agent, threshold=0.60)
        for (neighbor, score) in neighbors:
            phylogeny_edges.push(PhylogenyEdge {
                source: agent, target: neighbor,
                channel: "behavioral",
                weight: score,
                timestamp: c17_last_similarity_epoch(agent, neighbor),
            })

    // Source 2: C7 intent provenance
    for agent in seed_set:
        let provenance = c7_get_intent_provenance(agent, window)
        for record in provenance:
            phylogeny_edges.push(PhylogenyEdge {
                source: record.delegator, target: record.delegate,
                channel: "intent",
                weight: 1.0,  // binary linkage
                timestamp: record.saga_epoch,
            })

    // Step 4: Ancestor identification via MLE
    let candidates = identify_candidate_ancestors(seed_set, phylogeny_edges)
    //  candidates include: operator_ids linked to >=2 seeds,
    //  infrastructure_providers hosting >=2 seeds,
    //  UNKNOWN_COMMON_ORIGIN null candidate

    let mut best_candidate = None
    let mut best_log_likelihood = f64::NEG_INFINITY
    let mut all_posteriors: Vec<(AttributionTarget, f64)> = vec![]

    for candidate in candidates:
        let log_l = compute_phylogeny_likelihood(candidate, seed_set,
                                                  phylogeny_edges)
        all_posteriors.push((candidate, log_l))
        if log_l > best_log_likelihood:
            best_log_likelihood = log_l
            best_candidate = Some(candidate)

    // Normalize to posterior probabilities (uniform prior)
    let total = logsumexp(all_posteriors.iter().map(|(_, l)| *l))
    let posteriors: Vec<(AttributionTarget, f64)> = all_posteriors.iter()
        .map(|(c, l)| (*c, f64::exp(l - total)))
        .collect()

    let top = posteriors.iter().max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())

    // Step 5: Determine recommended action
    let action = if top.1 >= TIER3_ATTRIBUTION_THRESHOLD:
        match top.0.target_type:
            OPERATOR       => REFER_TO_TRIBUNAL
            COLLUSION      => REFER_TO_AVAP
            INFRASTRUCTURE => FLAG_INFRASTRUCTURE
            _              => INCONCLUSIVE
    else:
        INCONCLUSIVE

    return AttributionReport {
        report_id: generate_uuid(),
        analysis_window: window,
        seed_agents: seed_set,
        overdispersion: nb_result,
        attribution: Attribution {
            suspected_cause: top.0,
            confidence: top.1,
            evidence_chain: extract_supporting_edges(top.0, phylogeny_edges),
            alternative_causes: posteriors[1..].to_vec(),
        },
        recommended_action: action,
    }
```

---

## 19. References

Allen, R.V. (1978). Automatic earthquake recognition and timing from single traces. *Bulletin of the Seismological Society of America*, 68(5), 1521-1532.

Amini, A.A., Chen, A., Bickel, P.J., & Levina, E. (2013). Pseudo-likelihood methods for community detection in large sparse networks. *The Annals of Statistics*, 41(4), 2097-2122.

Bhatia, S., Hooi, B., Yoon, M., Shin, K., & Faloutsos, C. (2020). MIDAS: Microcluster-based detector of anomalies in edge streams. *Proceedings of the AAAI Conference on Artificial Intelligence*, 34(04), 3242-3249.

Bhatia, S., Hooi, B., Yoon, M., Shin, K., & Faloutsos, C. (2022). Real-time streaming anomaly detection in dynamic graphs. *ACM Transactions on Knowledge Discovery from Data*, 16(3), 1-21.

Bojchevski, A. & Gunnemann, S. (2019). Adversarial attacks on node embeddings via graph poisoning. *Proceedings of the 36th International Conference on Machine Learning (ICML)*, 695-704.

Cameron, A.C. & Trivedi, P.K. (1998). *Regression Analysis of Count Data*. Cambridge University Press.

Cao, Q., Sirivianos, M., Yang, X., & Pregueiro, T. (2012). Aiding the detection of fake accounts in large scale social online services. *Proceedings of the 9th USENIX Conference on Networked Systems Design and Implementation (NSDI)*, 197-210.

Gomes, P.H.N., Leung, C.K., & Zhang, C. (2024). Graph neural networks for collusion detection in procurement networks. *arXiv preprint*, arXiv:2410.07091.

He, Z., Wang, J., & Chen, L. (2025). SentinelAgent: graph-based anomaly detection for LLM multi-agent systems. *arXiv preprint*, arXiv:2505.24201.

IEC 61508. (2010). Functional safety of electrical/electronic/programmable electronic safety-related systems. *International Electrotechnical Commission*.

Mainali, K.P., Slud, E., Singer, M., & Fagan, W.F. (2022). A better index for analysis of co-occurrence and similarity. *Science Advances*, 8(4), eabj9204.

Mohar, B. (1991). The Laplacian spectrum of graphs. *Graph Theory, Combinatorics, and Applications*, 2, 871-898.

Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press.

Ng, A.Y., Jordan, M.I., & Weiss, Y. (2001). On spectral clustering: analysis and an algorithm. *Advances in Neural Information Processing Systems (NeurIPS)*, 14, 849-856.

Ovaskainen, O., Tikhonov, G., Norberg, A., Guillaume Blanchet, F., Duan, L., Dunson, D., Roslin, T., & Abrego, N. (2017). How to make more out of community data? A conceptual framework and its implementation as models and software. *Ecology Letters*, 20(5), 561-576.

Wang, B., Gong, N.Z., & Fu, H. (2017). GANG: Detecting fraudulent users in online social networks via guilt-by-association on directed graphs. *Proceedings of the IEEE International Conference on Data Mining (ICDM)*, 465-474.

Wang, B., Zhang, L., & Gong, N.Z. (2017). SybilSCAR: Sybil detection in online social networks via local rule based propagation. *Proceedings of the IEEE INFOCOM*, 1-9.

Withers, M., Aster, R., Young, C., Beiriger, J., Harris, M., Moore, S., & Trujillo, J. (1998). A comparison of select trigger algorithms for automated global seismic phase and event detection. *Bulletin of the Seismological Society of America*, 88(1), 95-106.

Yu, H., Gibbons, P.B., Kaminsky, M., & Xiao, F. (2010). SybilLimit: A near-optimal social network defense against Sybil attacks. *IEEE/ACM Transactions on Networking*, 18(3), 885-898.

Zugner, D., Akbarnejad, A., & Gunnemann, S. (2020). Adversarial attacks on graph neural networks via meta-learning. *Proceedings of the International Conference on Learning Representations (ICLR)*.

---

*End of C35 Master Tech Spec Part 3. This concludes the Seismographic Sentinel specification.*
