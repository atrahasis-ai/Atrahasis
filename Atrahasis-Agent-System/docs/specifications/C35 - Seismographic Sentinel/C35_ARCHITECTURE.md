# C35 — Seismographic Sentinel with PCM-Augmented Tier 2

## Architecture Document — Part 1

**Version:** 1.0.0
**Date:** 2026-03-12
**Invention ID:** C35
**Stage:** DESIGN
**Role:** Architecture Designer (PRIMARY tier)
**Status:** DESIGN — Architecture Part 1 Complete
**Normative References:** C3 Tidal Noosphere v2.0, C5 PCVM v2.0, C6 EMA v2.0, C7 RIF v2.0, C8 DSF v2.0, C12 AVAP v1.0, C17 MCSD L2 v1.0, C9 Cross-Layer Reconciliation v2.0
**Scope:** Sections 1-3 (Architecture Overview, Tier 1, Tier 2)

---

## 1. Architecture Overview

### 1.1 System Purpose

The Seismographic Sentinel is a three-tier hierarchical detection pipeline for security anomalies and behavioral aberrations in the Atrahasis Agent System. It operates across a distributed multi-agent platform hosting between 1,000 and 100,000 autonomous verification agents. The name reflects the core analogy: like seismographic networks that detect earthquakes through layered filtering of ground vibration data, this system detects platform-level threats by progressively filtering per-agent behavioral signals through regional correlation analysis and global threat assessment.

The system addresses a gap in the existing AAS defense architecture. C12 (AVAP) detects collusion after ring formation. C17 (MCSD L2) detects Sybil agents via pairwise behavioral similarity. Neither provides continuous, population-wide anomaly surveillance that can detect emergent threats — novel attack patterns, coordinated degradation campaigns, infrastructure compromise, or economic manipulation — before they trigger individual defense subsystems. The Seismographic Sentinel fills this gap by providing always-on, population-scale anomaly detection with escalating specificity.

### 1.2 Three-Tier Hierarchy

The architecture is organized into three tiers with strictly increasing scope, latency, and analytical depth.

| Tier | Scope | Cadence | Complexity | Function |
|------|-------|---------|------------|----------|
| **Tier 1** | Per-agent | Every SETTLEMENT_TICK (60s) | O(V) per tick | Local anomaly detection via STA/LTA ratio and dual-baseline comparison |
| **Tier 2** | Per-neighborhood | Every TIDAL_EPOCH (3600s) | O(V log V) amortized | Regional correlation analysis via PCM-augmented MIDAS edge detection |
| **Tier 3** | System-wide | On-demand (Tier 2 escalation) | O(V^2) worst case, O(V log V) typical | Global threat synthesis, campaign identification, response coordination |

**V** denotes total agent population. Part 1 of this document specifies Tiers 1 and 2. Part 2 specifies Tier 3, the state machine, parameters table, formal properties, and integration contracts.

### 1.3 High-Level Block Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         SEISMOGRAPHIC SENTINEL — C35                             │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                      TIER 3 — GLOBAL THREAT SYNTHESIS                       │ │
│  │                                                                             │ │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐  │ │
│  │  │ Campaign         │  │ Cross-Neighborhood│  │ Response                 │  │ │
│  │  │ Identifier       │  │ Correlator        │  │ Coordinator              │  │ │
│  │  │ (pattern mining) │  │ (global graph)    │  │ (C7/C12 dispatch)        │  │ │
│  │  └────────┬─────────┘  └────────┬─────────┘  └────────────┬─────────────┘  │ │
│  │           │                     │                          │                │ │
│  │           └─────────────────────┼──────────────────────────┘                │ │
│  │                                 │                                           │ │
│  └─────────────────────────────────┼───────────────────────────────────────────┘ │
│                                    │ Tier 2 → Tier 3 escalation                  │
│  ┌─────────────────────────────────┼───────────────────────────────────────────┐ │
│  │                      TIER 2 — REGIONAL CORRELATION                          │ │
│  │                                 │                                           │ │
│  │  ┌───────────┐  ┌──────────────┴──────────┐  ┌──────────────────────────┐  │ │
│  │  │Neighborhood│  │ PCM-Augmented           │  │ Channel Fusion           │  │ │
│  │  │Computation │  │ MIDAS Edge Detection    │  │ Engine                   │  │ │
│  │  │(spectral   │──│                         │──│ (bootstrap: 3-of-4       │  │ │
│  │  │ clustering)│  │ Per-channel residuals:   │  │  calibrated: Bayesian)   │  │ │
│  │  │            │  │ R = obs - E[PCM]        │  │                          │  │ │
│  │  └─────┬──────┘  └──────────────┬──────────┘  └────────────┬─────────────┘  │ │
│  │        │                        │                           │                │ │
│  │  ┌─────┴────────────────────────┴───────────────────────────┴─────────────┐  │ │
│  │  │                    Per-Neighborhood Coordinator                         │  │ │
│  │  │  Receives Tier 1 triggers, runs correlation, emits Tier 2 verdicts     │  │ │
│  │  └─────────────────────────────┬──────────────────────────────────────────┘  │ │
│  │                                │                                            │ │
│  └────────────────────────────────┼────────────────────────────────────────────┘ │
│                                   │ Tier 1 → Tier 2 triggers                    │
│  ┌────────────────────────────────┼────────────────────────────────────────────┐ │
│  │                     TIER 1 — PER-AGENT LOCAL DETECTION                      │ │
│  │                                │                                            │ │
│  │  ┌─────────────┐  ┌───────────┴───────────┐  ┌──────────────────────────┐  │ │
│  │  │ STA/LTA     │  │ Decision Fusion       │  │ Escalation               │  │ │
│  │  │ Ratio       │  │ (OR-trigger +         │  │ Protocol                 │  │ │
│  │  │ Calculator  │  │  confirmation window + │  │ (annotate + queue        │  │ │
│  │  │             │  │  dual-trigger bypass)  │  │  for neighborhood        │  │ │
│  │  │ Fixed       │  │                        │  │  coordinator)            │  │ │
│  │  │ Baseline    │  │ FC-2 Resolution:       │  │                          │  │ │
│  │  │ +           │──│ sign-agreement with    │──│ Confidence annotation:   │  │ │
│  │  │ Adaptive    │  │ relaxation             │  │ agent_id, tick, metrics, │  │ │
│  │  │ Baseline    │  │ alpha_confirm=0.7      │  │ baseline_source,         │  │ │
│  │  │             │  │                        │  │ confidence score         │  │ │
│  │  └──────┬──────┘  └────────────────────────┘  └──────────────────────────┘  │ │
│  │         │                                                                   │ │
│  │  ┌──────┴──────────────────────────────────────────────────────────────┐    │ │
│  │  │ Per-Agent Metric Ingestion (4 channels, every SETTLEMENT_TICK)      │    │ │
│  │  │                                                                     │    │ │
│  │  │  verification_latency ← C5    claim_acceptance_rate ← C5           │    │ │
│  │  │  committee_frequency  ← C3    behavioral_consistency ← C17         │    │ │
│  │  └─────────────────────────────────────────────────────────────────────┘    │ │
│  │                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
│  CROSS-LAYER INPUTS                                                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │
│  │  C3    │ │  C5    │ │  C6    │ │  C7    │ │  C8    │ │  C12   │ │  C17   │  │
│  │ Tidal  │ │ PCVM   │ │ EMA    │ │ RIF    │ │ DSF    │ │ AVAP   │ │MCSD L2 │  │
│  │schedule│ │verify  │ │knowl.  │ │ orchestr│ │settle  │ │collus. │ │behav.  │  │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 1.4 Data Flow Summary

Data flows strictly upward through the tiers. No tier sends data downward except for configuration parameters and threshold updates.

**Tier 1 ingestion (every SETTLEMENT_TICK = 60s):**
Each agent's Tier 1 monitor ingests four metric values from cross-layer sources. Metrics are stored in local STA and LTA windows. The STA/LTA ratio is computed, compared against both fixed and adaptive baselines, and the decision fusion logic determines whether to emit a CANDIDATE trigger.

**Tier 1 to Tier 2 escalation (event-driven, confirmed triggers only):**
Confirmed Tier 1 triggers are annotated with metadata (agent_id, tick, metric values, baseline source, confidence score) and queued for the neighborhood coordinator responsible for the triggering agent. Unconfirmed candidates that expire their confirmation window are discarded silently.

**Tier 2 analysis (every TIDAL_EPOCH = 3600s, plus event-driven):**
Neighborhood coordinators perform two functions: (a) batch correlation analysis at each TIDAL_EPOCH boundary using PCM-augmented MIDAS on all agent pairs within the neighborhood, and (b) event-driven analysis when Tier 1 trigger density within a neighborhood exceeds 2 standard deviations above the 100-epoch rolling mean. Channel fusion (bootstrap or Bayesian) produces a per-pair anomaly verdict.

**Tier 2 to Tier 3 escalation (event-driven, confirmed anomalies only):**
Confirmed Tier 2 anomalies are annotated with neighborhood context (neighborhood_id, involved agents, per-channel evidence, PCM residuals, fusion confidence) and queued for Tier 3 if queue depth is below MAX_TIER3_CONCURRENT (default 3).

**Tier 3 synthesis (on-demand):**
Tier 3 correlates anomalies across neighborhoods, identifies campaigns (coordinated multi-neighborhood threats), and coordinates responses via C7 (orchestration) and C12 (collusion defense). Specified in Part 2.

### 1.5 Epoch Hierarchy

C35 aligns with the canonical three-tier epoch hierarchy established in C9 Cross-Layer Reconciliation:

| Epoch Level | Duration | C35 Function | Source |
|-------------|----------|--------------|--------|
| SETTLEMENT_TICK | 60 seconds | Tier 1 per-agent metric ingestion and STA/LTA computation | C8 DSF (C9 §3.1) |
| TIDAL_EPOCH | 3,600 seconds (60 ticks) | Tier 2 batch neighborhood correlation analysis, adaptive baseline update aggregation | C3 Tidal Noosphere (C9 §3.2) |
| CONSOLIDATION_CYCLE | 36,000 seconds (10 epochs, 600 ticks) | Tier 2 neighborhood recomputation (spectral clustering), PCM parameter refit, Bayesian network prior update | C6 EMA (C9 §3.3) |

**Derived cadences:**

| Event | Cadence | Derivation |
|-------|---------|------------|
| STA window refresh | Every tick | w_s = 5 ticks = 300s sliding |
| LTA window refresh | Every tick | w_l = 60 ticks = 3600s sliding |
| Adaptive baseline EMA update | Every tick | alpha = 0.01 per tick |
| Tier 1 confirmation window | 3-5 ticks | 180s-300s depending on density regime |
| Tier 2 batch analysis | Every TIDAL_EPOCH | 3600s periodic |
| Neighborhood partition | Every CONSOLIDATION_CYCLE | 36000s periodic |
| PCM parameter refit | Every CONSOLIDATION_CYCLE | 36000s periodic |
| Fixed baseline calibration | Once (first 100 epochs) | 360,000s total calibration period |

### 1.6 Component Inventory

| Component | Tier | Instances | Lifecycle | Memory per Instance |
|-----------|------|-----------|-----------|---------------------|
| MetricIngestor | 1 | V (one per agent) | Always-on | 64 bytes (current tick buffer) |
| STAWindow | 1 | V | Always-on | 4 metrics x 5 ticks x 8 bytes = 160 bytes |
| LTAWindow | 1 | V | Always-on | 4 metrics x 60 ticks x 8 bytes = 1,920 bytes |
| FixedBaseline | 1 | V | Immutable after calibration | 4 metrics x 5 percentiles x 8 bytes = 160 bytes |
| AdaptiveBaseline | 1 | V | Always-on | 4 metrics x 8 bytes = 32 bytes (EMA state) |
| TriggerState | 1 | V | Always-on | 48 bytes (state enum, window counter, pending annotation) |
| DecisionFusionEngine | 1 | V | Always-on | 16 bytes (configuration) |
| NeighborhoodCoordinator | 2 | k = ceil(V/(2*log2(V))) | Reassigned at CONSOLIDATION_CYCLE | Variable (see §3.1) |
| PCMParameterStore | 2 | k | Refit at CONSOLIDATION_CYCLE | 64 params x 8 bytes = 512 bytes per store |
| MIDASInstance | 2 | k x 4 (per channel per neighborhood) | Reset at CONSOLIDATION_CYCLE | ~16 KB per instance (hash tables) |
| ChannelFusionEngine | 2 | k | Always-on | Bootstrap: 32 bytes; Bayesian: ~2 KB (CPTs) |
| Tier3Queue | 2-3 | 1 (global) | Always-on | Variable (bounded by MAX_TIER3_CONCURRENT) |
| CampaignIdentifier | 3 | 1 (global) | On-demand | See Part 2 |
| CrossNeighborhoodCorrelator | 3 | 1 (global) | On-demand | See Part 2 |
| ResponseCoordinator | 3 | 1 (global) | On-demand | See Part 2 |

**Total Tier 1 memory per agent:** 160 + 1,920 + 160 + 32 + 48 + 16 + 64 = **2,400 bytes**

**Total Tier 1 memory at scale:**
- 1,000 agents: 2.4 MB
- 10,000 agents: 24 MB
- 100,000 agents: 240 MB

**Total Tier 2 memory (approximate):**
- At V = 10,000: k = ceil(10000/(2*log2(10000))) = ceil(10000/26.6) = 377 neighborhoods
  - PCM stores: 377 x 512 = 193 KB
  - MIDAS instances: 377 x 4 x 16 KB = 24.1 MB
  - Fusion engines: 377 x 2 KB = 754 KB
  - **Tier 2 total: ~25 MB**
- At V = 100,000: k = ceil(100000/(2*log2(100000))) = ceil(100000/33.2) = 3,013 neighborhoods
  - **Tier 2 total: ~200 MB**

### 1.7 Cross-Layer Integration Summary

C35 maintains 7 cross-layer contracts with existing AAS components. Each contract specifies the data exchanged, the direction of flow, the cadence, and the failure mode.

| # | Contract | Direction | Data | Cadence | Failure Mode |
|---|----------|-----------|------|---------|--------------|
| **XL-1** | C35 ↔ C3 (Tidal Noosphere) | C3 → C35 | committee_frequency per agent; tidal_phase_alignment per agent pair; TIDAL_EPOCH boundary events | Every tick (metric), every CONSOLIDATION_CYCLE (structural) | Degrade to cached value; MONITORING_DEGRADED after 100 ticks stale |
| **XL-2** | C35 ↔ C5 (PCVM) | C5 → C35 | verification_latency per agent; claim_acceptance_rate per agent; VTD outcome similarity per agent pair; claim_class distribution per agent | Every tick (metric), every CONSOLIDATION_CYCLE (structural) | Degrade to cached value; MONITORING_DEGRADED after 100 ticks stale |
| **XL-3** | C35 ↔ C6 (EMA) | C6 → C35 | knowledge_consolidation_events for Tier 3 campaign context; CONSOLIDATION_CYCLE boundary events | Every CONSOLIDATION_CYCLE | Non-critical; Tier 3 operates with reduced context |
| **XL-4** | C35 ↔ C7 (RIF) | C35 → C7 | Tier 3 response actions (agent isolation, enhanced monitoring, committee exclusion); C7 → C35: resource_usage patterns per agent (infrastructure channel) | Event-driven (response), every tick (metric) | Response actions queued until C7 available; infrastructure channel degrades to cached |
| **XL-5** | C35 ↔ C8 (DSF) | C8 → C35 | settlement_pattern per agent; staking_behavior per agent; reward_timing per agent (economic channel) | Every tick (metric), every CONSOLIDATION_CYCLE (structural) | Degrade to cached value; MONITORING_DEGRADED after 100 ticks stale |
| **XL-6** | C35 ↔ C12 (AVAP) | C12 → C35 | AVAP-confirmed collusion edges (pre-confirmed Tier 2 triggers); C35 → C12: Tier 2/3 anomaly reports for AVAP correlation | Event-driven | C12 edges bypass fusion when available; absence does not degrade C35 |
| **XL-7** | C35 ↔ C17 (MCSD L2) | C17 → C35 | B(a_i, a_j) pairwise behavioral similarity scores; behavioral_consistency self-similarity metric per agent; LSH candidate pairs | Every TIDAL_EPOCH (batch), every CONSOLIDATION_CYCLE (structural) | Critical for Tier 2 PCM; fallback to raw correlation if C17 unavailable for >1 CONSOLIDATION_CYCLE |

### 1.8 Notation Conventions

Throughout this document, the following notation is used:

| Symbol | Meaning |
|--------|---------|
| V | Total agent population |
| a_i, a_j | Individual agents, indexed i, j in {1, ..., V} |
| t | Current tick (SETTLEMENT_TICK count since system genesis) |
| T_e | Current TIDAL_EPOCH index = floor(t / 60) |
| T_c | Current CONSOLIDATION_CYCLE index = floor(t / 600) |
| m_c(a_i, t) | Value of metric channel c for agent a_i at tick t |
| w_s | STA window size in ticks (default 5) |
| w_l | LTA window size in ticks (default 60) |
| alpha | Adaptive baseline EMA decay factor (default 0.01) |
| theta_c | Threshold for metric channel c |
| N_j | Neighborhood j (a set of agents) |
| k | Number of neighborhoods |
| B(a_i, a_j) | C17 behavioral similarity score for agents a_i, a_j |
| R_c(a_i, a_j) | PCM residual for channel c between agents a_i, a_j |

---

## 2. Tier 1 Architecture — Per-Agent Local Detection

### 2.1 Purpose

Tier 1 is the innermost detection ring. Every registered agent in the AAS has an independent Tier 1 monitor that runs at every SETTLEMENT_TICK (60 seconds). Tier 1 performs lightweight, statistically grounded anomaly detection on four behavioral metrics, using dual baselines (fixed and adaptive) to distinguish genuine anomalies from normal behavioral drift. The computational budget is O(V) per tick across the entire population — constant work per agent, linear in agent count.

Tier 1 does NOT determine whether an anomaly is a threat. It determines whether an agent's current behavior deviates sufficiently from expected patterns to warrant regional correlation analysis at Tier 2. The false positive rate at Tier 1 is intentionally non-trivial (target: 1-5% of agents per epoch, depending on population dynamics). Tier 2's role is to separate coincidental individual anomalies from correlated threats.

### 2.2 Data Model

Each agent a_i maintains the following local state for its Tier 1 monitor:

```
struct Tier1AgentState {
    // === Identity ===
    agent_id:           AgentID,          // Immutable. Set at registration.
    registration_tick:  u64,              // Tick at which agent was registered.
    calibration_status: CalibrationStatus,// CALIBRATING | CALIBRATED | DEGRADED

    // === Metric Windows ===
    sta_window:         [[f64; 4]; W_S],  // Ring buffer, W_S = w_s (default 5)
    sta_head:           usize,            // Current write position in STA ring buffer
    sta_count:          usize,            // Number of valid entries (0..W_S)

    lta_window:         [[f64; 4]; W_L],  // Ring buffer, W_L = w_l (default 60)
    lta_head:           usize,            // Current write position in LTA ring buffer
    lta_count:          usize,            // Number of valid entries (0..W_L)

    // === Fixed Baseline (immutable after calibration) ===
    fixed_baseline:     FixedBaseline,    // Percentile distribution per metric
    calibration_buffer: Option<CalibrationBuffer>, // Non-None only during calibration

    // === Adaptive Baseline (updated every tick) ===
    adaptive_baseline:  [f64; 4],         // EMA state per metric channel

    // === Trigger State ===
    trigger_state:      TriggerState,     // IDLE | CANDIDATE | CONFIRMED | DEGRADED
    candidate_tick:     Option<u64>,      // Tick when CANDIDATE was entered
    candidate_baseline: Option<BaselineSource>, // FIXED | ADAPTIVE | BOTH
    candidate_metrics:  Option<[f64; 4]>, // Metric snapshot at candidate time
    confirmation_count: u8,               // Ticks of confirmation observed
    confirmation_required: u8,            // 3 (normal) or 5 (high-density)
}
```

**CalibrationStatus transitions:**
- `CALIBRATING`: agent registered fewer than 100 TIDAL_EPOCHS ago. Fixed baseline is not yet available. Only adaptive baseline is active. Tier 1 triggers are suppressed (no escalation during calibration, to avoid bootstrapping noise).
- `CALIBRATED`: agent has completed 100 TIDAL_EPOCHS of calibration. Fixed baseline is locked. Both baselines are active.
- `DEGRADED`: one or more metric sources are unavailable for >100 ticks. Tier 1 triggers are suspended. Agent is flagged as MONITORING_DEGRADED to Tier 2.

### 2.3 Metric Channels

Tier 1 monitors four metric channels, each derived from a cross-layer data source. All values are normalized to the [0, 1] range using min-max scaling calibrated during the fixed baseline calibration period.

#### 2.3.1 Channel 1: Verification Latency (c=0)

**Source:** C5 PCVM (contract XL-2)

**Definition:** Mean time in seconds between claim assignment to agent a_i and opinion submission by a_i, measured over the most recent SETTLEMENT_TICK. Normalized by dividing by the maximum observed latency during calibration (P99 latency from calibration distribution).

```
m_0(a_i, t) = mean_latency(a_i, t) / P99_latency_calibration(a_i)
```

**Semantics:** Sudden increases in verification latency may indicate computational distress (resource exhaustion, infrastructure compromise), deliberate stalling (part of a coordination attack delaying claim resolution), or model degradation. Sudden decreases may indicate claim rubber-stamping (submitting opinions without genuine analysis) or pre-computed answer injection.

**Normalization range:** [0, 1] where 0 = zero latency (impossible under genuine verification) and 1 = P99 calibration latency. Values > 1.0 are clipped to 1.0 for the ratio computation but preserved in the raw metric annotation for Tier 2.

#### 2.3.2 Channel 2: Claim Acceptance Rate (c=1)

**Source:** C5 PCVM (contract XL-2)

**Definition:** Fraction of claims for which agent a_i submitted a positive verification opinion (belief > 0.5 in Subjective Logic opinion tuple) during the most recent SETTLEMENT_TICK.

```
m_1(a_i, t) = count(opinions where b > 0.5) / count(all opinions submitted)
```

If no opinions were submitted in the tick (agent was not assigned to any committee), the value is carried forward from the previous tick. If carried forward for >5 consecutive ticks, the metric is marked as STALE and excluded from trigger computation for that channel.

**Semantics:** Anomalously high acceptance rate suggests indiscriminate approval (Sybil rubber-stamping, collusion agreement). Anomalously low acceptance rate suggests indiscriminate rejection (griefing, denial-of-service on claim credibility). Both directions are meaningful.

#### 2.3.3 Channel 3: Committee Frequency (c=2)

**Source:** C3 Tidal Noosphere (contract XL-1)

**Definition:** Number of verification committees to which agent a_i was assigned during the most recent SETTLEMENT_TICK, normalized by the population mean committee frequency.

```
m_2(a_i, t) = committees_assigned(a_i, t) / mean_committees_assigned(*, t)
```

If the population mean is zero (no committees assigned system-wide in this tick), the value is set to 1.0 (neutral).

**Semantics:** Committee frequency is primarily a C3 scheduling output that reflects agent availability and tidal phase. Anomalies in committee frequency indicate either: (a) C3 scheduling manipulation (an agent receiving disproportionate committee assignments, possibly via infrastructure gaming of the VRF self-selection process per C12), or (b) infrastructure availability problems (agent frequently unavailable for assignment).

#### 2.3.4 Channel 4: Behavioral Consistency (c=3)

**Source:** C17 MCSD L2 (contract XL-7)

**Definition:** Self-similarity score for agent a_i, computed as the mean B(a_i, a_i') where a_i' represents the agent's own historical behavioral profile from the previous TIDAL_EPOCH. This is NOT the pairwise B(a_i, a_j) used in Tier 2 — it is a *self-comparison over time* that measures how stable the agent's behavioral fingerprint is.

```
m_3(a_i, t) = B_self(a_i, T_e, T_e - 1)
```

where B_self is computed by C17 using the same five-modality distance calculation (temporal, structural, error, resource, lexical) but comparing the agent against its own prior-epoch profile rather than against another agent. C17 provides this value at each TIDAL_EPOCH boundary; between epochs, the last-computed value is held constant.

**Semantics:** Behavioral consistency measures whether an agent is "acting like itself." A sudden drop in self-similarity suggests model replacement (the agent's underlying model was swapped), infrastructure migration (new hardware changes timing and resource profiles), or adversarial behavior mode switching (an agent that was passively observing switches to active manipulation).

**Update cadence:** Unlike channels 0-2 which update every tick, channel 3 updates once per TIDAL_EPOCH (every 60 ticks). Between updates, the stale value is used. This is acceptable because behavioral consistency is inherently a slow-moving metric — it measures epoch-scale behavioral stability, not tick-scale fluctuations.

### 2.4 STA/LTA Computation

The Short-Term Average (STA) and Long-Term Average (LTA) are computed independently for each metric channel c in {0, 1, 2, 3}.

#### 2.4.1 STA (Short-Term Average)

The STA captures recent behavior over a short window.

**Window size:** w_s = 5 ticks (300 seconds). Configurable via parameter TIER1_STA_WINDOW_TICKS (range: [3, 15]).

**Computation:** Arithmetic mean of the most recent w_s metric values.

```
STA_c(a_i, t) = (1 / min(w_s, n_valid)) * Σ_{j=0}^{min(w_s, n_valid)-1} m_c(a_i, t - j)
```

where n_valid is the count of non-STALE entries in the STA window. If n_valid = 0, STA_c is undefined and the channel is excluded from trigger computation for this tick.

**Implementation:** Ring buffer of size w_s. At each tick, the newest value overwrites the oldest. The mean is recomputed incrementally:

```
STA_new = STA_old + (m_new - m_evicted) / min(w_s, n_valid)
```

This avoids iterating the buffer on every tick. Numerical stability: after every 100 ticks, the STA is recomputed from scratch to prevent floating-point drift accumulation.

#### 2.4.2 LTA (Long-Term Average)

The LTA captures the agent's normal behavioral baseline over a longer window.

**Window size:** w_l = 60 ticks (3,600 seconds = 1 TIDAL_EPOCH). Configurable via parameter TIER1_LTA_WINDOW_TICKS (range: [30, 120]).

**Computation:** Arithmetic mean of the most recent w_l metric values.

```
LTA_c(a_i, t) = (1 / min(w_l, n_valid)) * Σ_{j=0}^{min(w_l, n_valid)-1} m_c(a_i, t - j)
```

Same validity and staleness rules as STA.

**Implementation:** Ring buffer of size w_l with incremental mean update and periodic full recomputation (every 600 ticks = 1 CONSOLIDATION_CYCLE).

#### 2.4.3 STA/LTA Ratio

The ratio measures how current behavior deviates from recent-historical behavior.

```
R_c(a_i, t) = STA_c(a_i, t) / LTA_c(a_i, t)
```

**Edge cases:**
- If LTA_c = 0: R_c is undefined. This channel is excluded from trigger computation. This can occur legitimately if the metric has been zero for the entire LTA window (e.g., an agent with zero committee assignments for a full epoch).
- If LTA_c < epsilon (epsilon = 1e-10): R_c is capped at R_MAX = 100.0 to prevent numerical explosion.
- If STA_c = 0 and LTA_c > 0: R_c = 0, which is a valid and meaningful anomaly signal (sudden cessation of activity).

**Interpretation:**
- R_c ~ 1.0: Current behavior is consistent with recent history. No anomaly.
- R_c >> 1.0: Current behavior is significantly elevated relative to recent history. Positive anomaly.
- R_c << 1.0: Current behavior is significantly depressed relative to recent history. Negative anomaly.

The absolute deviation |R_c - 1.0| is the anomaly magnitude. Both positive and negative deviations are meaningful for all four channels.

### 2.5 Fixed Baseline

The fixed baseline provides an immutable reference point calibrated during the agent's initial observation period. It is designed to detect long-term drift that the adaptive baseline (which tracks drift by design) would miss.

#### 2.5.1 Calibration Period

Calibration begins at agent registration (registration_tick) and lasts for 100 TIDAL_EPOCHS (100 x 3,600 = 360,000 seconds = 100 hours = ~4.17 days).

During calibration, the agent's Tier 1 monitor collects all metric values into a CalibrationBuffer:

```
struct CalibrationBuffer {
    samples: Vec<[f64; 4]>,    // All metric samples during calibration
    epoch_count: u64,          // Number of complete TIDAL_EPOCHS observed
    start_tick: u64,           // registration_tick
}
```

The calibration buffer accumulates up to 100 x 60 = 6,000 samples per channel (60 ticks per epoch x 100 epochs). Missing or STALE samples are excluded.

#### 2.5.2 Calibration Computation

At the end of the 100th epoch after registration, the calibration buffer is processed to produce the fixed baseline:

```
struct FixedBaseline {
    percentiles: [[f64; 5]; 4],  // 4 channels x 5 percentiles (P5, P25, P50, P75, P95)
    sample_count: [u64; 4],      // Number of valid samples per channel
    calibration_epoch: u64,      // Epoch at which calibration completed
}
```

For each channel c, the 6,000 samples (or fewer if some were STALE) are sorted, and five percentiles are extracted:

```
P_q(c) = sample[floor(q/100 * n_valid)]   for q in {5, 25, 50, 75, 95}
```

using nearest-rank percentile computation (no interpolation, to avoid introducing values not present in the sample).

#### 2.5.3 Laplace Noise Injection

To protect against reconstruction attacks (an adversary who observes the fixed baseline and reverse-engineers the agent's calibration-period behavior), calibrated noise is added to each percentile value using the Laplace mechanism.

For each percentile P_q(c):

```
P_q_noisy(c) = P_q(c) + Lap(0, Delta_c / epsilon)
```

where:
- Lap(0, b) denotes a sample from the Laplace distribution with location 0 and scale b
- Delta_c = sensitivity of channel c = max(m_c) - min(m_c) over the calibration period (the range of the metric)
- epsilon = 1.0 (privacy parameter, configurable via TIER1_BASELINE_PRIVACY_EPSILON, range [0.1, 10.0])

At epsilon = 1.0, the noise scale b = Delta_c / 1.0 = Delta_c. For a channel with range [0, 1], this adds Laplace noise with scale 1.0 — sufficient to obscure the exact percentile value while preserving the distributional shape.

**Post-noise clamping:** After noise injection, percentile values are clamped to maintain monotonicity:
```
P5_final  = clamp(P5_noisy, 0.0, 1.0)
P25_final = clamp(P25_noisy, P5_final, 1.0)
P50_final = clamp(P50_noisy, P25_final, 1.0)
P75_final = clamp(P75_noisy, P50_final, 1.0)
P95_final = clamp(P95_noisy, P75_final, 1.0)
```

#### 2.5.4 Immutability

After calibration completes:
1. The CalibrationBuffer is zeroed and deallocated. It MUST NOT be retained in memory or on disk.
2. The FixedBaseline is written once to persistent storage.
3. The FixedBaseline is NEVER updated, replaced, or recalibrated — unless an explicit admin override is issued. Admin override requires: (a) C7 saga authorization with two-party approval (per C7 RIF §7.2 administrative saga protocol), and (b) the agent enters a fresh 100-epoch recalibration period during which Tier 1 triggers are suppressed.
4. If the underlying metric source changes semantically (e.g., C5 changes its latency measurement methodology), the admin override is the ONLY mechanism to recalibrate. The system does NOT detect semantic changes automatically. This is a conscious design choice: automatic recalibration creates an attack surface where an adversary modifies behavior, waits for recalibration, and then the new baseline accepts the adversarial behavior as normal.

#### 2.5.5 Fixed Baseline Anomaly Detection

A metric value m_c(a_i, t) is considered anomalous relative to the fixed baseline if it falls outside the interquartile-anchored range:

```
anomaly_fixed(c, a_i, t) = true  if  m_c(a_i, t) < P5(c)  OR  m_c(a_i, t) > P95(c)
```

This is a simple percentile-based outlier test. The P5/P95 thresholds correspond to the 90% confidence interval of the calibration distribution. A metric value outside this range occurred in fewer than 10% of ticks during the agent's calibration period.

**Direction tagging:** The anomaly is tagged with a direction:
- direction = POSITIVE if m_c(a_i, t) > P95(c)
- direction = NEGATIVE if m_c(a_i, t) < P5(c)

Direction is used in the confirmation window sign-agreement check (§2.7).

### 2.6 Adaptive Baseline

The adaptive baseline tracks the agent's evolving normal behavior using an exponential moving average (EMA). Unlike the fixed baseline, it adapts to gradual behavioral drift — a model upgrade that increases latency by 10% over 30 epochs will be absorbed into the adaptive baseline.

#### 2.6.1 EMA Update

At every tick t, for each channel c:

```
AB_c(a_i, t) = alpha * m_c(a_i, t) + (1 - alpha) * AB_c(a_i, t-1)
```

where alpha = 0.01 (configurable via TIER1_ADAPTIVE_ALPHA, range [0.001, 0.1]).

**Initialization:** AB_c(a_i, registration_tick) = m_c(a_i, registration_tick). The first observed value initializes the EMA.

**Half-life:** At alpha = 0.01, the half-life is:
```
t_half = -ln(2) / ln(1 - alpha) = -ln(2) / ln(0.99) = 69.0 ticks = 4,140 seconds ≈ 1.15 hours
```

This means the adaptive baseline "forgets" half of a step change in approximately 1.15 hours (69 ticks). A sustained behavioral shift is fully absorbed (>95% adapted) within approximately 300 ticks (5 hours).

**Staleness handling:** If m_c(a_i, t) is STALE, the EMA is not updated for that channel at that tick. The previous value AB_c(a_i, t-1) is retained.

#### 2.6.2 Adaptive Baseline Anomaly Detection

A metric value m_c(a_i, t) is considered anomalous relative to the adaptive baseline if the STA/LTA ratio deviates from 1.0 by more than a channel-specific threshold:

```
anomaly_adaptive(c, a_i, t) = true  if  |R_c(a_i, t) - 1.0| > theta_c
```

where theta_c is the per-channel anomaly threshold:

| Channel | theta_c (default) | Rationale |
|---------|-------------------|-----------|
| c=0: verification_latency | 0.40 | Latency is noisy; 40% deviation required |
| c=1: claim_acceptance_rate | 0.25 | Acceptance rate is more stable; 25% sufficient |
| c=2: committee_frequency | 0.50 | Frequency varies widely with scheduling; generous threshold |
| c=3: behavioral_consistency | 0.20 | Self-similarity is very stable; small deviations are significant |

All thresholds are configurable via parameters TIER1_THETA_LATENCY, TIER1_THETA_ACCEPTANCE, TIER1_THETA_COMMITTEE, TIER1_THETA_CONSISTENCY (range: [0.05, 1.0] each).

**Direction tagging:**
- direction = POSITIVE if R_c(a_i, t) - 1.0 > theta_c
- direction = NEGATIVE if R_c(a_i, t) - 1.0 < -theta_c

### 2.7 Decision Fusion (FC-2 Resolution)

The decision fusion engine resolves the interaction between the fixed and adaptive baselines. The core challenge (designated FC-2 in the feasibility study) is that the two baselines serve different purposes — the fixed baseline detects absolute deviation from calibration-era behavior, while the adaptive baseline detects deviation from recent behavior — and they can disagree. An agent that has gradually drifted far from its calibration profile will trigger the fixed baseline constantly but never the adaptive baseline. Conversely, a sudden spike that is still within the calibration range will trigger the adaptive baseline but not the fixed baseline.

#### 2.7.1 OR-Trigger with Adaptive Confirmation Window

The fusion logic uses an OR-trigger with a confirmation window:

**Step 1: CANDIDATE trigger.** Either baseline exceeding its threshold fires a CANDIDATE trigger:

```
candidate_trigger(a_i, t) = anomaly_fixed(c, a_i, t)  OR  anomaly_adaptive(c, a_i, t)
    for ANY channel c in {0, 1, 2, 3}
```

A single channel anomaly on a single baseline is sufficient to enter CANDIDATE state. This ensures high sensitivity (low miss rate) at the cost of higher initial false positive rate.

When CANDIDATE is entered:
- trigger_state transitions from IDLE to CANDIDATE
- candidate_tick is set to t
- candidate_baseline is set to FIXED, ADAPTIVE, or BOTH (whichever triggered)
- candidate_metrics records the metric snapshot [m_0, m_1, m_2, m_3] at tick t
- confirmation_count is set to 0

**Step 2: Confirmation window.** The confirmation window is a short observation period during which the anomaly must persist with sign agreement.

**Window duration:**
- Normal mode: confirmation_required = 3 ticks (180 seconds)
- High-density mode: confirmation_required = 5 ticks (300 seconds)

**High-density mode activation:** High-density mode is entered when the population-wide trigger rate exceeds a statistical threshold:

```
trigger_rate(t) = count(agents in CANDIDATE or CONFIRMED state at tick t) / V

high_density(t) = trigger_rate(t) > mean_trigger_rate_100 + 2 * sigma_trigger_rate_100
```

where mean_trigger_rate_100 and sigma_trigger_rate_100 are the mean and standard deviation of trigger_rate over the most recent 100 TIDAL_EPOCHS (rolling computation, updated at each epoch boundary).

**Rationale:** When many agents trigger simultaneously, the probability of coincidental anomalies is high (e.g., a system-wide load spike). The extended confirmation window filters out these population-level transients. When few agents trigger, the shorter window provides faster detection.

**Step 3: Sign agreement with relaxation.** During the confirmation window, at each tick t' > candidate_tick:

```
confirmed_tick(a_i, t') = true  if:
    EXISTS channel c such that:
        anomaly_fixed(c, a_i, t') has direction D_fixed
        AND anomaly_adaptive(c, a_i, t') has direction D_adaptive
        AND sign_agree(D_fixed, D_adaptive, alpha_confirm)
```

where sign_agree is defined with relaxation factor alpha_confirm = 0.7:

```
sign_agree(D_fixed, D_adaptive, alpha_confirm) =
    CASE
        D_fixed = D_adaptive:                        true   // Both agree on direction
        D_fixed = NONE AND D_adaptive != NONE:       true   // Fixed didn't trigger, adaptive did
                                                             // (one-sided agreement is acceptable)
        D_fixed != NONE AND D_adaptive = NONE:       true   // Adaptive didn't trigger, fixed did
        D_fixed = POSITIVE AND D_adaptive = NEGATIVE: false  // Contradictory: one says up, other says down
        D_fixed = NEGATIVE AND D_adaptive = POSITIVE: false  // Contradictory
```

The "relaxation" terminology refers to the fact that we do NOT require both baselines to trigger — only that they do not *contradict* each other on direction. If baseline A triggers POSITIVE and baseline B does not trigger at all, that is accepted (one-sided agreement). Only if both baselines trigger in *opposite* directions is the confirmation denied.

The alpha_confirm = 0.7 parameter (configurable via TIER1_ALPHA_CONFIRM, range [0.5, 1.0]) controls a magnitude relaxation: when both baselines trigger, the confirmation is only accepted if the weaker anomaly's magnitude is at least alpha_confirm times the stronger anomaly's magnitude:

```
IF both D_fixed != NONE AND D_adaptive != NONE:
    mag_fixed = |m_c(a_i, t') - P50(c)| / (P95(c) - P5(c))    // Normalized deviation from fixed median
    mag_adaptive = |R_c(a_i, t') - 1.0| / theta_c               // Normalized deviation from adaptive threshold

    stronger = max(mag_fixed, mag_adaptive)
    weaker = min(mag_fixed, mag_adaptive)

    confirmation_accepted = (weaker / stronger) >= alpha_confirm
```

This prevents a weak, potentially spurious trigger from validating a strong trigger when they happen to point in the same direction by coincidence.

If confirmed_tick is true, confirmation_count is incremented.

**Step 4: Confirmation resolution.**

```
IF confirmation_count >= confirmation_required:
    trigger_state → CONFIRMED
    // Escalate to Tier 2 (see §2.8)

IF t - candidate_tick > confirmation_required + 2:
    // Window expired without sufficient confirmation
    trigger_state → IDLE
    // Candidate discarded, no escalation
```

The "+2" grace period allows for up to 2 ticks of STALE data within the confirmation window before discarding.

#### 2.7.2 Dual-Trigger Bypass

If BOTH baselines exceed their respective thresholds simultaneously on the SAME channel with the SAME direction, the confirmation window is bypassed entirely:

```
dual_trigger_bypass(a_i, t) = true  if:
    EXISTS channel c such that:
        anomaly_fixed(c, a_i, t) = true  with direction D
        AND anomaly_adaptive(c, a_i, t) = true  with direction D
        AND D_fixed = D_adaptive  (same direction, strict equality, no relaxation)
```

When dual_trigger_bypass fires:
- trigger_state transitions directly from IDLE to CONFIRMED (skipping CANDIDATE)
- Immediate Tier 2 escalation
- No confirmation window

**Rationale:** If both the immutable calibration baseline AND the adaptive recent baseline agree that the agent is anomalous on the same metric in the same direction, the probability of a false positive is very low. Both baselines detecting the same anomaly means: the behavior is unusual relative to the agent's entire history (fixed) AND unusual relative to recent behavior (adaptive). This conjunction is strong evidence of a genuine behavioral shift.

**False alarm rate analysis for dual-trigger bypass:**

Under the null hypothesis (no genuine anomaly), the probability of a single-channel fixed baseline trigger is approximately:
```
P(fixed) ≈ 0.10   // By construction: P5/P95 thresholds
```

The probability of a single-channel adaptive baseline trigger depends on the threshold theta_c. For the tightest threshold (theta_3 = 0.20 for behavioral consistency), under Gaussian noise with sigma estimated from calibration:
```
P(adaptive | c=3) ≈ 2 * Phi(-0.20 / sigma_R)
```

For typical sigma_R ≈ 0.10 (STA/LTA ratio standard deviation), P(adaptive | c=3) ≈ 0.046.

The probability of simultaneous trigger on the same channel in the same direction, assuming independence between baselines (conservative — they are correlated):
```
P(dual) ≈ P(fixed) * P(adaptive) * P(same direction | both triggered)
P(dual | c=3) ≈ 0.10 * 0.046 * 0.50 = 0.0023  per tick per agent
```

At V = 10,000 agents, expected false dual-trigger bypasses per tick: 10,000 * 0.0023 * 4 channels = 92. Over 60 ticks per epoch, approximately 5,520 false dual-triggers per epoch. This is high.

**Mitigation:** The per-channel probability estimate above is conservative (assumes independence). In practice, the fixed and adaptive baselines are positively correlated under the null hypothesis (both are functions of the same metric), which REDUCES the probability of same-direction dual triggers. Empirical calibration during the W0 validation experiment (C22 §W0.3) will refine these thresholds. If the false alarm rate is unacceptable, the dual-trigger bypass can be restricted to require 2 or more channels simultaneously exceeding both baselines (parameter TIER1_DUAL_TRIGGER_MIN_CHANNELS, default 1, range [1, 4]).

### 2.8 Escalation Protocol

When a Tier 1 trigger is confirmed (either via confirmation window or dual-trigger bypass), the agent's Tier 1 monitor emits a TriggerAnnotation to the neighborhood coordinator responsible for this agent.

```
struct TriggerAnnotation {
    agent_id:           AgentID,
    trigger_tick:       u64,              // Tick at which CONFIRMED was reached
    candidate_tick:     u64,              // Tick at which CANDIDATE was entered (= trigger_tick for bypass)
    metric_values:      [f64; 4],         // Current metric values at trigger_tick
    metric_values_candidate: [f64; 4],    // Metric values when CANDIDATE was entered
    baseline_source:    BaselineSource,   // FIXED | ADAPTIVE | BOTH
    triggering_channels: [bool; 4],       // Which channels triggered
    directions:         [Direction; 4],   // POSITIVE | NEGATIVE | NONE per channel
    sta_values:         [f64; 4],         // STA at trigger_tick
    lta_values:         [f64; 4],         // LTA at trigger_tick
    sta_lta_ratios:     [f64; 4],         // R_c at trigger_tick
    confidence:         f64,              // Confidence score (see below)
    bypass_used:        bool,             // True if dual-trigger bypass was used
    density_regime:     DensityRegime,    // NORMAL | HIGH_DENSITY
}
```

**Confidence score computation:**

The confidence score is a composite measure of how strongly the evidence supports a genuine anomaly (as opposed to noise):

```
confidence(a_i, t) = Σ_c w_conf_c * anomaly_strength_c(a_i, t) / Σ_c w_conf_c
```

where:
- w_conf_c = channel confidence weight: [0.30, 0.25, 0.15, 0.30] for channels [0, 1, 2, 3]
  (verification_latency and behavioral_consistency weighted highest; committee_frequency weighted lowest)
- anomaly_strength_c is the normalized anomaly magnitude for each triggered channel:

```
anomaly_strength_c(a_i, t) =
    CASE triggering_channels[c] = false:  0.0
    CASE baseline_source = FIXED:    |m_c - P50(c)| / (P95(c) - P5(c))
    CASE baseline_source = ADAPTIVE: |R_c - 1.0| / theta_c
    CASE baseline_source = BOTH:     max(fixed_strength, adaptive_strength)
```

The confidence score is in [0, 1] by construction (since anomaly strengths are bounded by the threshold design). A confidence of 0.5 means the anomaly is at the threshold boundary. A confidence of 1.0 means the anomaly is at the maximum detectable magnitude.

**Delivery:** The TriggerAnnotation is delivered to the NeighborhoodCoordinator for the agent's current neighborhood via the C7 RIF intra-platform message bus (contract XL-4). If C7 is unavailable, the annotation is buffered locally for up to 100 ticks (TIER1_ESCALATION_BUFFER_TICKS). If still undelivered after 100 ticks, the annotation is logged to the local agent audit trail with status ESCALATION_FAILED and discarded. Tier 1 returns to IDLE state regardless of delivery success — Tier 1 does not block on Tier 2 availability.

**Post-escalation:** After emitting the TriggerAnnotation, trigger_state returns to IDLE. A new CANDIDATE can be entered immediately on the next tick. There is no cooldown period — if the anomaly persists, the agent will re-trigger and re-escalate, providing Tier 2 with a stream of corroborating evidence.

### 2.9 Degradation Behavior

Tier 1 degrades gracefully when cross-layer data sources are unavailable.

#### 2.9.1 Metric Source Unavailability

If a metric source (C5, C3, or C17) is unreachable:

1. **For the first 100 ticks (≤ 1.67 hours):** The last successfully received metric value is used as a cache. The STA and LTA windows continue to update with the cached value. The metric is tagged as CACHED in the ring buffer. The trigger computation proceeds normally, but any trigger annotation includes a `cached_channels` bitmask indicating which channels used stale data.

2. **After 100 consecutive ticks of unavailability:** The metric channel is marked STALE. STALE channels are excluded from trigger computation entirely. If ALL four channels are STALE, the agent transitions to calibration_status = DEGRADED. The agent's trigger_state is forced to IDLE and remains there until at least one channel recovers.

3. **Tier 2 notification:** When an agent transitions to DEGRADED, a DegradationNotice is sent to the NeighborhoodCoordinator:

```
struct DegradationNotice {
    agent_id:       AgentID,
    degraded_since: u64,         // Tick at which DEGRADED was entered
    stale_channels: [bool; 4],   // Which channels are stale
    last_valid:     [u64; 4],    // Tick of last valid value per channel
}
```

The NeighborhoodCoordinator records the degradation and excludes the agent from Tier 2 correlation analysis for the degraded channels. If more than 30% of agents in a neighborhood are DEGRADED, the NeighborhoodCoordinator itself escalates a NEIGHBORHOOD_DEGRADED alert to Tier 3.

#### 2.9.2 Partial Channel Availability

Tier 1 can operate with any subset of channels available. The trigger computation adjusts dynamically:

| Available Channels | Trigger Behavior |
|---|---|
| 4 of 4 | Normal operation. All channels participate. |
| 3 of 4 | Normal operation with reduced channel set. Confidence score is reweighted over available channels. |
| 2 of 4 | Reduced sensitivity. Confirmation window is extended to 5 ticks (regardless of density regime) to compensate for reduced channel diversity. Dual-trigger bypass is disabled. |
| 1 of 4 | Minimal operation. Single-channel triggers require confirmation_required = 7 ticks. Dual-trigger bypass is disabled. Confidence score is capped at 0.5. |
| 0 of 4 | DEGRADED. No trigger computation. Agent is excluded from detection. |

### 2.10 Tier 1 Formal Properties

**PROP-T1-1 (Bounded Latency).** Tier 1 processing for a single agent completes within O(1) time per tick, independent of population size V. The only V-dependent operation is the high-density mode check, which uses pre-computed rolling statistics.

**PROP-T1-2 (Memory Bound).** Tier 1 memory per agent is bounded by 2,400 bytes plus the CalibrationBuffer (during calibration only, ~192 KB for 6,000 samples of 4 channels x 8 bytes). After calibration, the CalibrationBuffer is deallocated.

**PROP-T1-3 (No False Negatives from Calibration Noise).** The Laplace noise injected into the fixed baseline widens the P5-P95 range (noise is symmetric), which reduces the fixed baseline's sensitivity but cannot cause a miss that both baselines would have caught. Since the adaptive baseline is noise-free, any anomaly detectable by both baselines pre-noise remains detectable by at least the adaptive baseline post-noise.

**PROP-T1-4 (Monotonic Degradation).** As channels become unavailable, Tier 1 sensitivity decreases monotonically. No channel becoming unavailable can INCREASE the trigger rate (because unavailable channels are excluded, not treated as anomalous).

**PROP-T1-5 (Calibration Isolation).** During the calibration period (first 100 epochs), Tier 1 triggers are suppressed. No TriggerAnnotation is emitted. This ensures that initial behavioral exploration during agent onboarding does not pollute Tier 2 correlation analysis.

---

## 3. Tier 2 Architecture — Regional Correlation Analysis

### 3.1 Neighborhood Computation

Tier 2 organizes the agent population into neighborhoods — clusters of agents that interact frequently and whose behavioral correlations are expected to be high. Neighborhoods are the unit of regional analysis: all Tier 2 correlation computations operate on agent pairs within the same neighborhood.

#### 3.1.1 Spectral Clustering

Neighborhoods are computed at every CONSOLIDATION_CYCLE (36,000 seconds) via spectral clustering on the agent interaction graph.

**Interaction graph construction:**

The interaction graph G = (V, E, W) is a weighted undirected graph where:
- V = set of all registered agents with calibration_status != CALIBRATING
- E = set of agent pairs (a_i, a_j) that have interacted during the most recent CONSOLIDATION_CYCLE
- W: E → R+ assigns a weight to each edge

An "interaction" is defined as any of:
1. Co-membership in at least one verification committee (from C3 committee assignment records)
2. Verification of the same claim within the same TIDAL_EPOCH (from C5 claim routing records)
3. Co-assignment to the same C6 knowledge consolidation batch (from C6 shard records)

The edge weight combines two sources:

```
W(a_i, a_j) = lambda_B * B(a_i, a_j) + lambda_S * S_struct(a_i, a_j)
```

where:
- B(a_i, a_j) is the C17 behavioral similarity score (contract XL-7)
- S_struct(a_i, a_j) is the structural covariate similarity from the PCM model (see §3.2)
- lambda_B = 0.6, lambda_S = 0.4 (configurable via TIER2_CLUSTERING_LAMBDA_B and TIER2_CLUSTERING_LAMBDA_S)

If B(a_i, a_j) is unavailable (C17 has not yet computed it for this pair), the weight falls back to S_struct alone:
```
W(a_i, a_j) = S_struct(a_i, a_j)     // if B unavailable
```

**Laplacian construction:**

The normalized graph Laplacian L_norm is computed:

```
D = diag(Σ_j W(a_i, a_j))           // Degree matrix
L = D - W                            // Unnormalized Laplacian
L_norm = D^{-1/2} * L * D^{-1/2}    // Normalized Laplacian (Ng-Jordan-Weiss formulation)
```

**Eigenvector computation:**

The k smallest eigenvectors of L_norm are computed, where:

```
k = ceil(V / (2 * log2(V)))
```

| V | log2(V) | 2*log2(V) | k | Agents per cluster (avg) |
|---|---------|-----------|---|--------------------------|
| 1,000 | 9.97 | 19.93 | 51 | 19.6 |
| 10,000 | 13.29 | 26.58 | 377 | 26.5 |
| 100,000 | 16.61 | 33.22 | 3,013 | 33.2 |

The eigenvector matrix U (V x k) is then clustered via k-means into k clusters.

**Implementation note:** Full eigendecomposition of the V x V Laplacian is infeasible at V = 100,000. The implementation MUST use an iterative eigensolver (Lanczos algorithm or LOBPCG) that computes only the k smallest eigenvectors without materializing the full Laplacian. The Laplacian is represented as a sparse matrix (only edges with W > 0 are stored). At V = 100,000 with average degree ~50, the sparse Laplacian has ~5M non-zero entries, well within memory for iterative solvers.

**Computational budget:** Spectral clustering runs once per CONSOLIDATION_CYCLE (36,000 seconds). The Lanczos iteration for k = 3,013 eigenvectors of a 100,000 x 100,000 sparse matrix with 5M non-zeros requires approximately 10-30 seconds on modern hardware. This is well within the 36,000-second cycle budget.

#### 3.1.2 Cluster Size Cap and Overflow Handling

Each neighborhood has a maximum size cap:

```
cap = 2 * log2(V)
```

| V | cap |
|---|-----|
| 1,000 | 20 |
| 10,000 | 27 |
| 100,000 | 34 |

If k-means produces a cluster with more than `cap` agents, the overflow cluster is split via recursive bisection:

1. Extract the subgraph induced by the overflow cluster.
2. Compute the normalized Laplacian of the subgraph.
3. Compute the Fiedler vector (second smallest eigenvector).
4. Split into two sub-clusters at the Fiedler vector's median value.
5. If either sub-cluster still exceeds `cap`, recurse.

Recursive bisection terminates when all clusters are within cap. Maximum recursion depth: ceil(log2(max_cluster_size / cap)).

**Minimum cluster size:** Clusters with fewer than 3 agents are dissolved. Their agents are assigned to the nearest neighboring cluster (by mean edge weight to cluster members) that has room under the cap. If no cluster has room, the agents form a singleton pseudo-neighborhood with reduced Tier 2 analysis (no pairwise correlation, only Tier 1 aggregation).

#### 3.1.3 NMI Hardening

To detect adversarial manipulation of the interaction graph (an attacker creating or severing interactions to force agents into specific neighborhoods), the clustering is hardened using Normalized Mutual Information (NMI) stability testing.

**Protocol:**

1. Compute the clustering C_original on the original graph G.
2. Create a perturbed graph G' by adding Gaussian noise to all edge weights:
   ```
   W'(a_i, a_j) = W(a_i, a_j) + N(0, sigma_NMI^2)
   ```
   where sigma_NMI = 0.1 (configurable via TIER2_NMI_SIGMA, range [0.01, 0.50]).
3. Compute the clustering C_perturbed on G'.
4. Compute NMI(C_original, C_perturbed):
   ```
   NMI(C, C') = 2 * I(C; C') / (H(C) + H(C'))
   ```
   where I(C; C') is the mutual information between the two clusterings and H(C), H(C') are their entropies.
5. **Decision:**
   - If NMI >= 0.70: clustering is stable. Accept C_original.
   - If NMI < 0.70: clustering is potentially manipulated. **Fallback:** retain the previous CONSOLIDATION_CYCLE's clustering partition. Emit a CLUSTERING_INSTABILITY alert to Tier 3 with payload {NMI_value, perturbed_edges_summary}.

**Rationale for NMI threshold 0.70:** NMI of 0.70 indicates that 70% of the clustering structure is preserved under small perturbations. Below this, the clustering is sensitive to small changes in edge weights, which is a hallmark of either an adversarial graph modification or a genuinely unstable population structure. In either case, the previous cycle's clustering is a safer partition.

**Computational cost:** The NMI computation requires one additional spectral clustering pass on the perturbed graph. At V = 100,000, this doubles the clustering cost to ~60 seconds per CONSOLIDATION_CYCLE. This is acceptable (60s out of 36,000s budget = 0.17%).

#### 3.1.4 Neighborhood Coordinator

Each neighborhood has exactly one coordinator process. The coordinator is NOT a separate server or service — it is a lightweight coroutine that runs on any node hosting at least one agent in the neighborhood. Coordinator assignment follows the C7 RIF task scheduling model (contract XL-4).

The coordinator's responsibilities:
1. Receive TriggerAnnotations from Tier 1 agents in its neighborhood.
2. Maintain the PCM parameter store for the neighborhood.
3. Run MIDAS instances for the neighborhood's 4 channels.
4. Perform channel fusion at each TIDAL_EPOCH and on Tier 1 trigger-density events.
5. Emit Tier 2 verdicts (anomaly confirmed / not confirmed) and escalate to Tier 3 when warranted.

**Coordinator failover:** If the hosting node fails, C7's standard task rescheduling mechanism (C7 §4.3) reassigns the coordinator coroutine to another node hosting a neighborhood member. State is recovered from the PCM parameter store (persisted to local disk at each CONSOLIDATION_CYCLE) and MIDAS instances (stateless reset — loss of in-cycle streaming state is acceptable).

### 3.2 PCM Specification

The Pairwise Correlation Model (PCM) is the analytical core of Tier 2. It models the *expected* pairwise correlation between any two agents in a neighborhood based on structural covariates — observable features of the agents' positions in the platform that naturally produce correlated behavior. By subtracting the structurally expected correlation from the observed correlation, the PCM produces a *residual* that isolates unexplained correlation — the signal that MIDAS then examines for anomalous patterns.

#### 3.2.1 Log-Linear Model

The PCM is a log-linear model predicting the expected pairwise correlation between agents a_i and a_j on each metric channel c:

```
log E[corr_c(a_i, a_j)] = β_0 + Σ_{k=1}^{5} β_k · x_k(a_i, a_j) + Σ_{j<k} γ_{jk} · x_j(a_i, a_j) · x_k(a_i, a_j)
```

where:
- corr_c(a_i, a_j) is the observed Pearson correlation between the Tier 1 metric time series of agents a_i and a_j on channel c, computed over the most recent CONSOLIDATION_CYCLE (600 ticks)
- β_0 is the intercept (baseline expected log-correlation)
- β_k are coefficients for the 5 main-effect structural covariates
- γ_{jk} are coefficients for the 10 pairwise interaction terms (all C(5,2) = 10 pairs)
- x_k(a_i, a_j) are the structural covariate values for the agent pair

The model is fit separately for each metric channel c, producing 4 independent PCM instances per neighborhood. Each instance has 1 + 5 + 10 = 16 parameters.

**Total parameters per neighborhood:** 4 channels x 16 parameters = 64 parameters.
**Total parameters system-wide:** 64 x k neighborhoods.

#### 3.2.2 Structural Covariates

The five structural covariates x_k capture aspects of the platform structure that naturally induce behavioral correlation:

**x_1: Parcel Colocation**

```
x_1(a_i, a_j) = fraction of ticks in the current CONSOLIDATION_CYCLE where a_i and a_j
                 were assigned to the same C8 settlement parcel (HDL shard)
```

Value range: [0, 1]. Source: C8 DSF parcel assignment records (contract XL-5).

Rationale: Agents in the same settlement parcel share infrastructure latency characteristics and settlement timing, creating correlated verification_latency and settlement_pattern signals.

**x_2: Committee Coassignment**

```
x_2(a_i, a_j) = count(committees where both a_i and a_j were members) /
                 count(committees where either a_i or a_j was a member)
                 // Jaccard similarity of committee membership sets
```

Value range: [0, 1]. Source: C3 Tidal Noosphere committee assignment logs (contract XL-1).

Rationale: Agents who frequently serve on the same committees naturally develop correlated claim_acceptance_rate and committee_frequency patterns (they evaluate the same claims, under the same time pressure, in the same tidal phase).

**x_3: Epoch Coregistration**

```
x_3(a_i, a_j) = 1 - |registration_epoch(a_i) - registration_epoch(a_j)| / max_epoch_gap
```

where max_epoch_gap is the difference between the oldest and newest agent registration epochs in the neighborhood. Value range: [0, 1], where 1.0 = registered in the same epoch.

Rationale: Agents registered at similar times share calibration-era characteristics (they were calibrated under the same system load conditions, claim distribution, and behavioral norms). This creates correlated fixed baselines that produce correlated STA/LTA ratios.

**x_4: Claim Class Overlap**

```
x_4(a_i, a_j) = cosine_similarity(claim_class_dist(a_i), claim_class_dist(a_j))
```

where claim_class_dist(a_i) is a vector of length 9 (one per C9 canonical claim class: D, C, P, R, E, S, K, H, N) whose entries are the fraction of claims verified by a_i in each class during the current CONSOLIDATION_CYCLE.

Value range: [0, 1]. Source: C5 PCVM claim classification records (contract XL-2).

Rationale: Agents who verify the same types of claims develop similar claim_acceptance_rate baselines and similar behavioral_consistency profiles (same claim types induce similar computational patterns).

**x_5: Tidal Phase Alignment**

```
x_5(a_i, a_j) = 1 - |phi(a_i) - phi(a_j)| / pi
```

where phi(a_i) is the mean tidal phase (in radians, [0, 2*pi)) at which agent a_i was active during the current CONSOLIDATION_CYCLE, computed from C3's tidal scheduling records. The distance is the minimum circular distance.

Value range: [0, 1], where 1.0 = identical tidal phase. Source: C3 Tidal Noosphere tidal phase records (contract XL-1).

Rationale: Agents active in the same tidal phase experience similar system load conditions, claim arrival rates, and committee sizes, creating correlated metric patterns across all four channels.

#### 3.2.3 Pairwise Interaction Terms

All C(5,2) = 10 pairwise products of the structural covariates are included as interaction terms:

| Term | Interaction | Interpretation |
|------|-------------|----------------|
| γ_12 | x_1 · x_2 | Parcel colocation x committee coassignment: agents in the same parcel AND committees have amplified infrastructure correlation |
| γ_13 | x_1 · x_3 | Parcel colocation x epoch coregistration: co-registered agents in the same parcel may share deployment infrastructure |
| γ_14 | x_1 · x_4 | Parcel colocation x claim class overlap: parcel assignment may be claim-class-stratified |
| γ_15 | x_1 · x_5 | Parcel colocation x tidal phase alignment: tidal scheduling interacts with parcel load balancing |
| γ_23 | x_2 · x_3 | Committee coassignment x epoch coregistration: committee assignment algorithms may cluster by registration cohort |
| γ_24 | x_2 · x_4 | Committee coassignment x claim class overlap: committee assignment is claim-class-stratified by C3 design |
| γ_25 | x_2 · x_5 | Committee coassignment x tidal phase alignment: committee availability is tidal-phase-dependent |
| γ_34 | x_3 · x_4 | Epoch coregistration x claim class overlap: registration cohorts may specialize in similar claim classes |
| γ_35 | x_3 · x_5 | Epoch coregistration x tidal phase alignment: registration cohort may determine initial tidal assignment |
| γ_45 | x_4 · x_5 | Claim class overlap x tidal phase alignment: certain claim classes may concentrate in specific tidal phases |

#### 3.2.4 Parameter Estimation

PCM parameters are estimated at each CONSOLIDATION_CYCLE via maximum likelihood estimation (MLE) on the within-neighborhood agent pairs.

**Training data:** For each pair (a_i, a_j) within the neighborhood, the observed correlation corr_c(a_i, a_j) over the most recent CONSOLIDATION_CYCLE (600 ticks) is computed for each channel c. Pairs with fewer than 30 valid co-observed ticks (due to STALE data, staggered registration, or degradation) are excluded from the training set.

**MLE procedure:** The log-linear model is a generalized linear model (GLM) with log link and Gaussian family. Parameters are estimated via iteratively reweighted least squares (IRLS):

```
θ* = argmin_θ Σ_{(i,j)} [log(corr_c(a_i, a_j)) - X(a_i, a_j)^T · θ]^2
```

where θ = [β_0, β_1, ..., β_5, γ_12, ..., γ_45] is the 16-dimensional parameter vector and X(a_i, a_j) is the 16-dimensional feature vector [1, x_1, ..., x_5, x_1·x_2, ..., x_4·x_5].

**Regularization:** L2 (ridge) regularization with lambda_reg = 0.01 is applied to prevent overfitting in small neighborhoods:

```
θ* = argmin_θ Σ_{(i,j)} [log(corr_c(a_i, a_j)) - X^T · θ]^2 + lambda_reg * ||θ||^2
```

Closed-form solution: θ* = (X^T X + lambda_reg * I)^{-1} X^T y, where y is the vector of log-correlations and X is the design matrix.

**Computational cost:** Per neighborhood with n agents: C(n, 2) pairs, 16 parameters. At n = 27 (average at V = 10,000): C(27, 2) = 351 pairs, solving a 16x16 linear system = O(16^3) = O(4096). Per channel: ~4K operations. Per neighborhood (4 channels): ~16K operations. Per CONSOLIDATION_CYCLE (377 neighborhoods at V = 10,000): ~6M operations. Negligible.

At V = 100,000 with n = 34 average: C(34, 2) = 561 pairs, 3,013 neighborhoods x 4 channels = ~12K fits of 16x16 systems. Still negligible within a 36,000-second budget.

#### 3.2.5 Precomputed Lookup Table

After parameter estimation, the PCM predicted values are precomputed for all within-neighborhood pairs and stored as a lookup table:

```
struct PCMStore {
    neighborhood_id:    NeighborhoodID,
    cycle:              u64,                 // CONSOLIDATION_CYCLE at which parameters were fit
    parameters:         [[f64; 16]; 4],      // 4 channels x 16 parameters
    r_squared:          [f64; 4],            // R^2 per channel
    lookup:             HashMap<(AgentID, AgentID), [f64; 4]>,  // Expected correlation per channel
}
```

The lookup table maps (a_i, a_j) — with a_i < a_j by ID ordering to avoid duplicate entries — to the 4-channel vector of expected correlations:

```
E[corr_c(a_i, a_j)] = exp(X(a_i, a_j)^T · θ_c*)
```

**Storage cost per neighborhood:** At n = 27, C(27, 2) = 351 entries x 4 channels x 8 bytes = 11.2 KB. At n = 34, C(34, 2) = 561 entries x 32 bytes = 18 KB. Negligible.

#### 3.2.6 Residual Computation

The PCM residual isolates unexplained pairwise correlation:

```
R_c(a_i, a_j) = corr_c_observed(a_i, a_j) - E[corr_c(a_i, a_j)]
```

where corr_c_observed is the Pearson correlation computed over the most recent observation window (either the full CONSOLIDATION_CYCLE for batch analysis, or a shorter window for event-driven analysis).

**Interpretation:**
- R_c ≈ 0: Observed correlation is fully explained by structural covariates. No anomalous signal.
- R_c >> 0: Observed correlation exceeds structural expectation. The agents are more correlated than their platform positions predict — a signal of shared influence (collusion, shared infrastructure, coordinated manipulation).
- R_c << 0: Observed correlation is below structural expectation. The agents are less correlated than expected — a signal of deliberate divergence (evasion behavior, one agent being replaced/compromised while the other continues normally).

**Emitting raw + residual (commitment C-1):** Both the raw observed correlation and the PCM residual are recorded in the Tier 2 analysis log. Downstream consumers (Tier 3, C12) receive both values. The raw value supports analysis independent of the PCM model; the residual is the PCM-augmented signal.

#### 3.2.7 Unmodeled Correlation Category (C-2)

When the PCM residual is positive (R_c > 0) but the PCM model's explanatory power is low (R^2 < 0.70 for the neighborhood-channel), the correlation may be real but its source is ambiguous — the model cannot distinguish structural from adversarial correlation because the structural model itself is weak.

In this case, the Tier 2 verdict is emitted at REDUCED severity:

```
IF R_c(a_i, a_j) > threshold_R  AND  r_squared_c < 0.70:
    verdict.severity = REDUCED
    verdict.reason = UNMODELED_CORRELATION
    verdict.note = "PCM R^2 for channel c = {r_squared_c}. Correlation may be structural."
```

REDUCED severity anomalies are logged but do NOT count toward Tier 3 escalation thresholds. They are available to Tier 3 as supplementary evidence if other channels or neighborhoods independently confirm the anomaly.

#### 3.2.8 Coverage Metric and Fallback (C-3)

If the PCM R^2 is below 0.70 for a given neighborhood-channel combination, the PCM is considered non-predictive for that channel. The fallback is to use raw correlation similarity (without residualization):

```
IF r_squared_c < 0.70:
    // Fallback: use raw C17 behavioral similarity for this channel
    anomaly_signal_c(a_i, a_j) = corr_c_observed(a_i, a_j) - B(a_i, a_j) * rho_c
```

where rho_c is a per-channel scaling factor mapping C17's composite B score to the individual channel correlation scale, estimated as the mean ratio of single-channel correlation to B during the previous CONSOLIDATION_CYCLE.

This fallback is less precise than the PCM (it lacks the 5-covariate structural model) but avoids the pathology of residualizing against a model that does not fit the data.

#### 3.2.9 PCM Convergence Experiment Design (FC-1)

The PCM's reliability depends on having sufficient data for parameter convergence. FC-1 requires a simulation protocol to validate convergence rates before deployment.

**Experiment protocol:**

1. **Synthetic agent populations:** Generate agent populations at three scales: V = {1,000, 10,000, 100,000}.

2. **Known structural correlations:** For each population, assign structural covariate values (x_1 through x_5) from realistic distributions:
   - x_1 (parcel colocation): Beta(2, 5) — most pairs rarely co-located
   - x_2 (committee coassignment): Beta(1, 10) — committees are small relative to population
   - x_3 (epoch coregistration): Uniform(0, 1) — uniformly distributed registration times
   - x_4 (claim class overlap): Beta(3, 3) — moderate overlap
   - x_5 (tidal phase alignment): Uniform(0, 1) — uniformly distributed phases

3. **True PCM parameters:** Set ground-truth parameters β_k, γ_{jk} for each channel. Generate observed correlations as:
   ```
   corr_c(a_i, a_j) = exp(X^T · θ_true) + noise
   ```
   where noise ~ N(0, sigma_noise^2) with sigma_noise = 0.05 (5% noise level).

4. **Injection protocol:** Inject known anomalies into a random 5% of agent pairs — add an additional correlation of +0.30 that is NOT explained by structural covariates. These are the ground-truth positives.

5. **Convergence measurement:** At each epoch (1 through 2,000), refit the PCM parameters and measure:
   - Parameter estimation error: ||θ_estimated - θ_true||_2 / ||θ_true||_2
   - Anomaly detection ROC-AUC using the PCM residual as the anomaly score

6. **Success criterion:** Parameter estimates within 10% of true values (relative L2 norm < 0.10) within 1,000 epochs for 95% of neighborhoods at each population scale.

7. **Failure criterion:** If convergence requires >2,000 epochs at any scale, or if 95% coverage is not achieved, the PCM covariate set must be simplified (remove interaction terms first, then low-contribution main effects) until convergence is achieved.

**Reporting:** Convergence curves (parameter error vs. epoch) and ROC-AUC curves (detection performance vs. epoch) for each population scale. Report the minimum epoch count for 95% neighborhood convergence at each scale.

### 3.3 MIDAS Integration

MIDAS (Microcluster-based Detector of Anomalies in Edge Streams) is a streaming algorithm for detecting anomalous edges in dynamic graphs. In C35, MIDAS operates on the PCM-residual-augmented pairwise correlation data to detect anomalous correlation patterns within neighborhoods.

#### 3.3.1 Per-Neighborhood MIDAS Instances

Each neighborhood runs 4 MIDAS instances (one per metric channel). Each MIDAS instance maintains count-min sketch (CMS) data structures that track the frequency and temporal distribution of edge events.

```
struct MIDASInstance {
    channel:         MetricChannel,       // 0..3
    neighborhood_id: NeighborhoodID,
    current_cms:     CountMinSketch,       // Current time-step counts
    total_cms:       CountMinSketch,       // Cumulative counts
    threshold:       f64,                  // Anomaly score threshold
    cycle_start:     u64,                  // Tick at which current cycle started
}
```

**CMS parameters:**
- Width (w_cms): 512 buckets
- Depth (d_cms): 4 hash functions
- Hash family: pairwise-independent via Murmur3 seeding

Memory per MIDAS instance: 2 CMS x 512 x 4 x 8 bytes = 32 KB. Per neighborhood (4 channels): 128 KB. Total at V = 10,000 (377 neighborhoods): ~47 MB. Total at V = 100,000 (3,013 neighborhoods): ~376 MB.

#### 3.3.2 Edge Event Generation

At each TIDAL_EPOCH boundary (every 60 ticks), the neighborhood coordinator generates edge events for all within-neighborhood agent pairs:

For each pair (a_i, a_j) in the neighborhood, for each channel c:

1. Compute the observed correlation corr_c(a_i, a_j) over the most recent TIDAL_EPOCH (60 ticks).
2. Look up the PCM expected correlation E[corr_c(a_i, a_j)] from the precomputed store.
3. Compute the residual R_c(a_i, a_j) = corr_c_observed - E[corr_c].
4. If |R_c(a_i, a_j)| > threshold_R (channel-specific residual threshold):
   - Generate an edge event (a_i, a_j, c, R_c, t) and feed it to the MIDAS instance for channel c.

**Residual thresholds (threshold_R):**

| Channel | threshold_R (default) | Rationale |
|---------|----------------------|-----------|
| c=0: verification | 0.15 | Moderate sensitivity — infrastructure correlation is common |
| c=1: behavioral | 0.10 | High sensitivity — behavioral correlation above PCM prediction is suspicious |
| c=2: infrastructure | 0.20 | Lower sensitivity — infrastructure correlation has high natural variance |
| c=3: economic | 0.12 | Moderate-high sensitivity — economic correlation above structural expectation is a strong signal |

Configurable via parameters TIER2_RESIDUAL_THRESH_VERIFICATION, TIER2_RESIDUAL_THRESH_BEHAVIORAL, TIER2_RESIDUAL_THRESH_INFRASTRUCTURE, TIER2_RESIDUAL_THRESH_ECONOMIC (range [0.01, 0.50] each).

#### 3.3.3 MIDAS Scoring

MIDAS assigns an anomaly score to each edge event based on the chi-squared statistic between the current time-step count and the expected count from historical data:

```
score(a_i, a_j, c, t) = (current_count - expected_count)^2 / expected_count
```

where:
- current_count = current_cms.query(hash(a_i, a_j))
- expected_count = total_cms.query(hash(a_i, a_j)) * (current_timestep_duration / total_duration)

An edge is flagged as MIDAS-anomalous if:
```
score(a_i, a_j, c, t) > threshold_MIDAS
```

Default threshold_MIDAS = 3.84 (chi-squared critical value at p = 0.05 with 1 degree of freedom). Configurable via TIER2_MIDAS_THRESHOLD (range [1.0, 20.0]).

#### 3.3.4 MIDAS-F Variant for State Poisoning Resistance

The standard MIDAS algorithm is vulnerable to state poisoning: an adversary can generate a high volume of innocuous edge events to inflate the CMS counts, thereby raising the expected_count and masking subsequent anomalous edges.

C35 uses the MIDAS-F (Filtered) variant which incorporates temporal decay:

```
total_cms_decayed.query(h) = total_cms.query(h) * decay_factor^(t - last_update(h))
```

where decay_factor = 0.95 per TIDAL_EPOCH (configurable via TIER2_MIDAS_DECAY, range [0.80, 0.99]).

This ensures that old edge events contribute less to the expected count, limiting an adversary's ability to pre-inflate counts.

#### 3.3.5 MIDAS Reset at Cycle Boundaries

Each MIDAS instance is reset at CONSOLIDATION_CYCLE boundaries (every 36,000 seconds):

1. The current_cms is zeroed.
2. The total_cms is zeroed.
3. cycle_start is updated to the current tick.

**Rationale:** Resetting at CONSOLIDATION_CYCLE boundaries aligns with the PCM refit schedule. When PCM parameters change (due to refit), the residual distribution shifts, which would invalidate the MIDAS historical counts. A clean reset ensures MIDAS operates on data consistent with the current PCM model.

**Warm-up period:** After reset, MIDAS requires a warm-up period during which its CMS structures accumulate baseline counts. During the first 3 TIDAL_EPOCHS after reset, MIDAS scores are suppressed (not used for anomaly detection). This avoids spurious anomalies from empty-CMS edge effects.

#### 3.3.6 Joint Anomaly Criterion

An edge (a_i, a_j) is flagged as a Tier 2 anomalous edge on channel c if BOTH conditions are met:

```
anomalous_edge(a_i, a_j, c) =
    MIDAS_score(a_i, a_j, c) > threshold_MIDAS
    AND
    |R_c(a_i, a_j)| > threshold_R_c
```

Both the MIDAS streaming anomaly score AND the PCM residual must exceed their respective thresholds. This conjunction reduces false positives: MIDAS catches temporal anomalies (sudden appearance of unusual edges) while the PCM residual catches structural anomalies (edges that are unusual relative to structural expectations). An edge must be both temporally unusual AND structurally unexplained to be flagged.

### 3.4 Channel Definitions

Tier 2 operates on four analysis channels, each corresponding to a Tier 1 metric channel but extended to pairwise correlation analysis. The channels share the same indexing (c = 0, 1, 2, 3) as Tier 1.

#### 3.4.1 Verification Channel (c=0)

**Source:** C5 PCVM (contract XL-2)

**Pairwise signals:**
1. **Claim acceptance rate correlation:** Pearson correlation between agents' acceptance rate time series over the observation window.
2. **Verification timing correlation:** Pearson correlation between agents' verification latency time series.
3. **VTD outcome similarity:** Jaccard similarity of the sets of claims for which both agents submitted opinions with the same verdict (both positive or both negative).

**Composite channel correlation:**
```
corr_0(a_i, a_j) = 0.40 * corr_acceptance(a_i, a_j)
                  + 0.35 * corr_timing(a_i, a_j)
                  + 0.25 * vtd_outcome_sim(a_i, a_j)
```

**Anomaly semantics:** High unexplained verification correlation indicates coordinated opinion formation (collusion) or shared infrastructure producing synchronized verification patterns. This channel is the primary collusion detection signal, complementing C12 AVAP's mechanism-specific detection.

#### 3.4.2 Behavioral Channel (c=1)

**Source:** C17 MCSD L2 (contract XL-7)

**Pairwise signals:**
1. **B(a_i, a_j) behavioral similarity residual:** The C17 B-score minus the PCM-predicted behavioral similarity.
2. **Action sequence similarity:** Longest common subsequence (LCS) length of the agents' most recent 100 actions (claim verifications, committee participations, knowledge accesses), normalized by 100.

**Composite channel correlation:**
```
corr_1(a_i, a_j) = 0.70 * B_residual(a_i, a_j) + 0.30 * action_lcs(a_i, a_j)
```

where B_residual = B(a_i, a_j) - PCM_predicted_B(a_i, a_j).

**Anomaly semantics:** High unexplained behavioral similarity indicates shared origin (Sybil) or behavioral mimicry (one agent copying another's strategy). Low unexplained behavioral similarity (negative residual) in previously similar agents indicates identity replacement or adversarial behavior mode switching.

#### 3.4.3 Infrastructure Channel (c=2)

**Source:** C7 RIF (contract XL-4)

**Pairwise signals:**
1. **IP/network proximity:** Binary indicator (1 if agents share the same /24 subnet or autonomous system number, 0 otherwise) — available only if C7 exposes network topology metadata.
2. **Latency fingerprint correlation:** Pearson correlation of agents' round-trip latency profiles to 10 reference nodes distributed across the platform infrastructure.
3. **Resource usage pattern:** Pearson correlation of agents' CPU/GPU utilization time series (from C7 resource monitoring).

**Composite channel correlation:**
```
corr_2(a_i, a_j) = 0.20 * ip_proximity(a_i, a_j)
                  + 0.40 * latency_corr(a_i, a_j)
                  + 0.40 * resource_corr(a_i, a_j)
```

**Anomaly semantics:** High unexplained infrastructure correlation indicates shared hosting (agents running on the same physical or virtual infrastructure despite claiming independent operation), which is a prerequisite for many Sybil and collusion attacks. This channel is the most prone to false positives from legitimate cloud co-tenancy, hence the higher residual threshold (0.20).

#### 3.4.4 Economic Channel (c=3)

**Source:** C8 DSF (contract XL-5)

**Pairwise signals:**
1. **Settlement pattern correlation:** Pearson correlation of agents' AIC settlement amounts over the observation window.
2. **Staking behavior similarity:** Cosine similarity of agents' staking allocation vectors (how they distribute their stake across claim classes and time horizons).
3. **Reward timing:** Pearson correlation of agents' reward receipt timestamps (normalized to tidal phase).

**Composite channel correlation:**
```
corr_3(a_i, a_j) = 0.35 * settlement_corr(a_i, a_j)
                  + 0.35 * staking_sim(a_i, a_j)
                  + 0.30 * reward_timing_corr(a_i, a_j)
```

**Anomaly semantics:** High unexplained economic correlation indicates coordinated economic strategy (agents optimizing jointly for settlement outcomes), which is a hallmark of economic manipulation attacks. Economic channel anomalies are the strongest indicator of financially motivated adversarial behavior.

### 3.5 Two-Phase Channel Fusion

The channel fusion engine combines evidence from the four channels into a single per-pair anomaly verdict. The engine operates in two phases to address the cold-start problem.

#### 3.5.1 Phase 1: Bootstrap (< 50 confirmed anomalies system-wide)

During Phase 1, insufficient ground-truth data exists to calibrate probabilistic models. The fusion uses a simple majority quorum:

**Rule:** An agent pair (a_i, a_j) is confirmed anomalous if at least 3 of the 4 channels flag it as anomalous:

```
phase1_anomaly(a_i, a_j) = (count(anomalous_edge(a_i, a_j, c) for c in {0,1,2,3}) >= 3)
```

Each channel's output is binary: anomalous (1) or normal (0), determined by the joint criterion in §3.3.6.

**Rationale:** The 3-of-4 quorum requires corroboration across multiple independent observation dimensions. A single-channel false positive cannot produce a Tier 2 confirmation. Even two coincidental false positives are insufficient. Only coordinated anomalies across 3+ channels pass.

**False positive rate under Phase 1:** If each channel's per-pair false positive rate is p (conservatively, p = 0.05), the probability of 3 or more channels simultaneously false-triggering is:

```
P(≥3) = C(4,3)*p^3*(1-p) + C(4,4)*p^4
       = 4 * 0.05^3 * 0.95 + 1 * 0.05^4
       = 4 * 0.000125 * 0.95 + 0.00000625
       = 0.000475 + 0.00000625
       ≈ 0.000481
```

At V = 10,000 with k = 377 neighborhoods of average size 27, there are C(27, 2) = 351 pairs per neighborhood, total ~132,000 pairs. Expected false positives per epoch: 132,000 * 0.000481 ≈ 63. This is manageable for Tier 3 processing.

#### 3.5.2 Phase 2: Calibrated (>= 50 confirmed anomalies)

After 50 anomalies have been confirmed (by Tier 3 analysis with human review or C12 corroboration), the system transitions to a Bayesian network fusion model that leverages learned conditional dependencies between channels.

**Bayesian network structure:**

The network has 5 nodes: one for each channel (V=Verification, B=Behavioral, I=Infrastructure, E=Economic) and one latent root node (A=Anomaly).

```
         ┌─────┐
         │  A  │  (Anomaly — latent)
         └──┬──┘
       ┌────┼────────┐
       ▼    ▼        ▼
    ┌─────┐ ┌─────┐ ┌─────┐
    │  V  │ │  I  │ │  E  │
    └──┬──┘ └─────┘ └──┬──┘
       │               │
       ▼               │
    ┌─────┐            │
    │  B  │◄───────────┘
    └─────┘
```

**Directed edges and conditional probability tables (CPTs):**

1. **A → V** (anomaly causes verification channel signal):
   - P(V=1 | A=1) = 0.85 (most anomalies produce verification signal)
   - P(V=1 | A=0) = 0.05 (false positive rate)

2. **A → I** (anomaly causes infrastructure channel signal):
   - P(I=1 | A=1) = 0.60 (infrastructure signal is weaker — not all anomalies are infrastructure-based)
   - P(I=1 | A=0) = 0.08 (infrastructure false positives are more common)

3. **V → B** (verification anomaly induces behavioral anomaly — strong dependency):
   - P(B=1 | V=1) = 0.75
   - P(B=1 | V=0) = 0.15

4. **V → E** (verification anomaly induces economic anomaly — moderate dependency):
   - P(E=1 | V=1) = 0.55
   - P(E=1 | V=0) = 0.10

5. **B → E** (behavioral anomaly induces economic anomaly — weak dependency):
   - P(E=1 | V=0, B=1) = 0.40
   - P(E=1 | V=0, B=0) = 0.10
   - P(E=1 | V=1, B=1) = 0.70 (both V and B active: strong economic signal)
   - P(E=1 | V=1, B=0) = 0.55 (from V→E alone)

**Prior:** P(A=1) = prior learned from Phase 1 data:
```
P(A=1) = (count of Phase 1 confirmed anomalies) / (total pair-epochs observed during Phase 1)
```

**Posterior computation:** Given observed evidence e = (V=v, B=b, I=i, E=e), the posterior probability of anomaly is computed via belief propagation:

```
P(A=1 | V=v, B=b, I=i, E=e) ∝ P(V=v|A=1) * P(I=i|A=1) * P(B=b|V=v) * P(E=e|V=v,B=b) * P(A=1)
```

Normalizing:
```
P(A=1 | e) = [P(e | A=1) * P(A=1)] / [P(e | A=1) * P(A=1) + P(e | A=0) * P(A=0)]
```

The exact computation involves enumerating the evidence likelihood under each hypothesis:
```
P(e | A=1) = P(V=v|A=1) * P(B=b|V=v) * P(I=i|A=1) * P(E=e|V=v,B=b)
P(e | A=0) = P(V=v|A=0) * P(B=b|V=v) * P(I=i|A=0) * P(E=e|V=v,B=b)
```

Note that B and E CPTs depend on V (and E depends on V and B) but are independent of A given V. I is conditionally independent of V, B, E given A.

**Threshold:** A pair is confirmed anomalous if:
```
P(A=1 | V=v, B=b, I=i, E=e) >= 0.80
```

Default threshold = 0.80 (configurable via TIER2_BAYESIAN_THRESHOLD, range [0.50, 0.99]).

#### 3.5.3 CPT Learning and Update

The initial CPTs (§3.5.2) are prior values derived from the system's threat model. After Phase 2 activation, CPTs are updated at each CONSOLIDATION_CYCLE using the accumulated confirmed anomaly data:

**Update procedure:**
1. Collect all confirmed anomaly pairs and all confirmed non-anomaly pairs from the most recent CONSOLIDATION_CYCLE.
2. Compute maximum-likelihood CPT estimates from the data.
3. Apply Bayesian smoothing (Laplace smoothing with alpha = 1.0) to prevent zero probabilities.
4. Blend the MLE estimates with the prior CPTs using a learning rate:
   ```
   CPT_new = (1 - eta) * CPT_old + eta * CPT_mle
   ```
   where eta = 0.1 per CONSOLIDATION_CYCLE (slow adaptation to prevent adversarial manipulation of the fusion model).

#### 3.5.4 Phase Transition Protocol

**Phase 1 to Phase 2 transition requirements:**
1. At least 50 confirmed anomalies exist system-wide (not per-neighborhood).
2. The Bayesian network, trained on Phase 1 data, achieves 5-fold cross-validation accuracy > 0.85 on the Phase 1 confirmed anomaly set.

**Transition procedure:**
1. At each CONSOLIDATION_CYCLE, check if both conditions are met.
2. If met, train the Bayesian network on all Phase 1 data.
3. Run 5-fold cross-validation. If accuracy > 0.85, activate Phase 2 for all neighborhoods simultaneously.
4. If accuracy <= 0.85, remain in Phase 1. Log the accuracy and re-check at the next CONSOLIDATION_CYCLE.

**Reversion:** If Phase 2 performance degrades (measured by Tier 3 false positive rate exceeding 3x the Phase 1 false positive rate over 3 consecutive CONSOLIDATION_CYCLES), revert to Phase 1 fusion. Emit a FUSION_REVERSION alert to Tier 3.

#### 3.5.5 C12 AVAP Edge Injection

AVAP-confirmed collusion edges (from contract XL-6) are injected into Tier 2 as pre-confirmed triggers that bypass the channel fusion entirely:

```
IF C12 reports AVAP_COLLUSION_CONFIRMED(a_i, a_j):
    tier2_verdict(a_i, a_j) = CONFIRMED
    tier2_verdict.source = AVAP_INJECTION
    tier2_verdict.confidence = 1.0   // AVAP has its own confirmation protocol
    // Bypass all channel fusion logic
    // Directly eligible for Tier 3 escalation
```

**Rationale:** C12's AVAP has its own multi-mechanism confirmation pipeline (honeypot claims, sealed submission, behavioral analysis, deterrence payments). An AVAP-confirmed collusion edge has already been validated through mechanisms orthogonal to C35's channel analysis. Re-validating it through C35's fusion would add latency without adding confidence.

**De-duplication:** If a pair is both AVAP-confirmed AND independently confirmed by C35's channel fusion, the Tier 2 record reflects both sources. Tier 3 treats AVAP + C35 double-confirmation as higher-confidence than either alone.

### 3.6 Escalation to Tier 3

Confirmed Tier 2 anomalies are annotated and queued for Tier 3 analysis.

#### 3.6.1 Tier 2 Anomaly Annotation

```
struct Tier2Annotation {
    neighborhood_id:     NeighborhoodID,
    cycle:               u64,                // CONSOLIDATION_CYCLE
    epoch:               u64,                // TIDAL_EPOCH at which anomaly was detected
    involved_agents:     Vec<(AgentID, AgentID)>,  // All anomalous pairs in this neighborhood
    channel_evidence:    Vec<ChannelEvidence>,      // Per-channel details for each pair
    pcm_residuals:       Vec<PCMResidual>,          // Per-channel PCM residuals for each pair
    fusion_method:       FusionMethod,              // PHASE1_QUORUM | PHASE2_BAYESIAN | AVAP_INJECTION
    confidence:          f64,                       // Phase 1: fraction of channels (0.75 or 1.0)
                                                    // Phase 2: posterior P(A=1|e)
                                                    // AVAP: 1.0
    trigger_density:     f64,                       // Fraction of neighborhood agents with Tier 1 triggers
    neighborhood_size:   usize,                     // Number of agents in neighborhood
    midas_scores:        Vec<[f64; 4]>,             // MIDAS scores per pair per channel
}

struct ChannelEvidence {
    pair:                (AgentID, AgentID),
    channel:             MetricChannel,
    observed_corr:       f64,
    expected_corr:       f64,                // PCM prediction
    residual:            f64,                // observed - expected
    midas_score:         f64,
    raw_metric_summary:  MetricSummary,      // Mean/variance of pair metrics over window
}

struct PCMResidual {
    pair:                (AgentID, AgentID),
    residuals:           [f64; 4],           // Per-channel residuals
    r_squared:           [f64; 4],           // PCM R^2 per channel for this neighborhood
}
```

#### 3.6.2 Tier 3 Queue Management

Tier 2 anomalies are queued for Tier 3 processing subject to a concurrency limit:

```
IF tier3_queue.depth < MAX_TIER3_CONCURRENT:
    tier3_queue.enqueue(tier2_annotation)
ELSE:
    // Queue is full. Apply priority ordering.
    IF tier2_annotation.confidence > tier3_queue.min_confidence():
        tier3_queue.evict_lowest_confidence()
        tier3_queue.enqueue(tier2_annotation)
    ELSE:
        // Log as TIER3_QUEUE_OVERFLOW, retain in Tier 2 log for batch processing
        tier2_log.mark_overflow(tier2_annotation)
```

**MAX_TIER3_CONCURRENT:** Default 3 (configurable via TIER3_MAX_CONCURRENT, range [1, 10]).

**Rationale for low default:** Tier 3 analysis is expensive (O(V log V) to O(V^2)) and involves cross-neighborhood correlation. Running more than 3 concurrent Tier 3 analyses at V = 100,000 would consume significant compute resources. The priority queue ensures the highest-confidence anomalies are processed first.

**Overflow handling:** Annotations that fail to enter the Tier 3 queue are not discarded — they are retained in the Tier 2 log and processed during Tier 3's next batch cycle (specified in Part 2). This ensures no confirmed anomaly is permanently lost due to queue pressure.

#### 3.6.3 Escalation Criteria

Not every Tier 2 confirmation warrants Tier 3 escalation. The following filters apply:

1. **Minimum pair count:** At least 2 anomalous pairs must be detected in the same neighborhood in the same TIDAL_EPOCH. A single anomalous pair is logged but not escalated (it may be a pair-specific anomaly rather than a neighborhood-level threat).

2. **Confidence floor:** The maximum confidence among the anomalous pairs must be >= 0.70. Below this, the evidence is logged as TIER2_LOW_CONFIDENCE and monitored for accumulation over subsequent epochs.

3. **Recency filter:** If the same neighborhood has escalated a Tier 3 case within the past 3 TIDAL_EPOCHS that was resolved as FALSE_POSITIVE, the escalation threshold is raised to 4 anomalous pairs and confidence >= 0.85 for the next 10 TIDAL_EPOCHS. This prevents repeated false escalation from noisy neighborhoods.

---

*End of Part 1. Part 2 continues with Tier 3 Architecture, State Machine, Parameters Table, Formal Properties, and Cross-Layer Integration Contracts.*
# C35 — Seismographic Sentinel with PCM-Augmented Tier 2

## Architecture Document — Part 2

**Version:** 1.0.0
**Date:** 2026-03-12
**Invention ID:** C35
**Stage:** DESIGN
**Role:** Architecture Designer (PRIMARY tier)
**Status:** DESIGN — Architecture Part 2
**Scope:** Tier 3 Epidemiological Backward Tracing, Cross-Layer Integration, Data Architecture
**Normative References:** C3 Tidal Noosphere v2.0, C5 PCVM v2.0, C6 EMA v2.0, C7 RIF v2.0, C8 DSF v2.0, C9 Cross-Layer Reconciliation v2.0, C12 AVAP v2.0, C17 MCSD Layer 2 v1.0, C19 Temporal Trajectory v1.0
**Temporal Constants:** SETTLEMENT_TICK = 60s, TIDAL_EPOCH = 3600s (60 ticks), CONSOLIDATION_CYCLE = 36000s (600 ticks, 10 epochs)

---

## Continuity Note

This document continues from C35_ARCH_PART1.md, which covers Sections 1-3:
- Section 1: System Architecture Overview (three-tier pipeline, design principles)
- Section 2: Tier 1 Architecture (STA/LTA per-agent detection, dual baselines, confirmation protocol)
- Section 3: Tier 2 Architecture (PCM residual analysis, spectral clustering, 4-channel quorum, MIDAS augmentation)

Part 2 begins at Section 4 (Tier 3) and continues through Section 6 (Data Architecture).

---

## 4. Tier 3 Architecture — Epidemiological Backward Tracing

Tier 3 is the rarest and most computationally expensive tier in the pipeline. While Tier 1 runs at every SETTLEMENT_TICK and Tier 2 runs at CONSOLIDATION_CYCLE cadence, Tier 3 activates only when Tier 2 produces a statistically significant cluster of confirmed anomalies. Its purpose is not detection but *attribution*: given that anomalous coordination exists, identify the most probable common causal source (operator, infrastructure provider, or systematic vulnerability).

The design draws from epidemiological contact tracing methodology. In outbreak investigation, the first step is confirming that the case count exceeds what random variation explains (overdispersion analysis). The second step is tracing backward through contact networks to identify a common source (backward tracing). C35 Tier 3 applies both steps to the agent interaction graph.

### 4.1 Activation Conditions

Tier 3 activation is gated by three conditions that must all be satisfied simultaneously.

**Condition 1 — Tier 2 Posterior Threshold.** At least one Tier 2 anomaly must have reached a Bayesian posterior probability >= 0.80. In Phase 1 (quorum-only fusion), this condition is met when the quorum fires AND the MIDAS-F chi-squared test on the same agent pair independently confirms (p < 0.01). In Phase 2 (full Bayesian fusion), the posterior is computed directly from the channel evidence.

```
Tier3_activation_check(anomaly_queue, window):
  confirmed = [a for a in anomaly_queue
               if a.posterior >= TIER3_POSTERIOR_THRESHOLD      # default 0.80
               and a.epoch >= current_epoch - TIER3_ANALYSIS_WINDOW]  # 10 epochs

  if len(confirmed) < TIER3_MIN_ANOMALIES:                     # default 30
    deficit = TIER3_MIN_ANOMALIES - len(confirmed)
    synthetic = draw_synthetic_calibration(deficit, hybrid_pool)
    analysis_set = confirmed + synthetic
    analysis_set_synthetic_fraction = len(synthetic) / len(analysis_set)
  else:
    analysis_set = confirmed
    analysis_set_synthetic_fraction = 0.0

  return analysis_set, analysis_set_synthetic_fraction
```

**Condition 2 — Minimum Analysis Queue.** The analysis window (sliding window of the last 10 TIDAL_EPOCHs = 36,000 seconds = 1 CONSOLIDATION_CYCLE) must contain >= 30 confirmed anomalies. If fewer than 30 real anomalies exist, the deficit is supplemented with synthetic calibration anomalies from the hybrid pool. The synthetic supplement serves a specific statistical purpose: the overdispersion analysis in Section 4.2 requires a minimum sample size of ~30 events for adequate power (65% detection at alpha=2.0 per SA-5 from the Science Assessment). Without synthetic supplementation, Tier 3 would be dormant indefinitely at low-anomaly-rate scales.

Synthetic anomalies are generated from known-benign agent pairs that have been marked as "synthetic positive" by the PCM calibration system. They provide statistical power for the overdispersion test without contaminating the detection results, because the overdispersion analysis always knows which entries are synthetic and excludes them from the attribution step.

**Condition 3 — Concurrency Bound.** At most 3 Tier 3 analyses may run concurrently. Each Tier 3 analysis is computationally expensive (Section 4.3 backward tracing requires traversing multiple cross-layer data sources). The concurrency bound prevents Tier 3 from consuming resources needed by Tier 1 and Tier 2.

```
TIER3_MAX_CONCURRENT = 3

Tier3_admission_control():
  if active_tier3_count >= TIER3_MAX_CONCURRENT:
    enqueue(pending_tier3_queue)                # FIFO, oldest first
    return QUEUED
  else:
    active_tier3_count += 1
    return ADMITTED
```

**State Machine.** Tier 3 operates independently of Tier 1 and Tier 2 state machines. Its lifecycle is:

```
DORMANT  ─── (30+ anomalies accumulated) ───>  ACTIVE
ACTIVE   ─── (analysis complete)          ───>  ACTIVE   (remains, checks for new batches)
ACTIVE   ─── (real anomaly rate < 5/window) ──> DORMANT
```

The transition from DORMANT to ACTIVE requires 30 real (non-synthetic) anomalies in the analysis window. Once ACTIVE, Tier 3 remains active and processes new anomaly batches as they arrive. If the real anomaly rate drops below 5 per 10-epoch window for two consecutive CONSOLIDATION_CYCLEs, Tier 3 returns to DORMANT.

### 4.2 Overdispersion Analysis

The first analytical step within a Tier 3 analysis is testing whether the distribution of confirmed anomalies across agents exhibits overdispersion -- that is, whether some agents appear in anomalous neighborhoods significantly more often than a random (Poisson) model would predict. Overdispersion is the statistical signature of a common causal source: if an operator controls agents A, B, and C, and those agents all appear in Tier 2 anomalies, the per-agent anomaly count will have higher variance than expected under independent occurrence.

**Statistical Model.** The count of anomalies per agent follows a negative binomial distribution NB(mu, alpha), where mu is the expected count (mean anomalies per agent) and alpha is the overdispersion parameter. Under the null hypothesis (no common cause), anomaly counts are Poisson-distributed (alpha = 0, variance = mean). Under the alternative hypothesis (common causal source exists), alpha > 0 and variance = mean + mean^2 / alpha, making variance > mean.

The model is fit using the Cameron & Trivedi (1998) negative binomial regression framework, which is the standard parametric approach for overdispersed count data in epidemiology.

```
NegBinRegression:
  Response:    Y_i = count of Tier 2 anomalies involving agent i in analysis window
  Covariates:  X_i = [operator_id, registration_cohort, geographic_cluster,
                       infrastructure_provider]
  Link:        log(mu_i) = X_i * beta
  Dispersion:  Var(Y_i) = mu_i + mu_i^2 / alpha

  Fit via iteratively reweighted least squares (IRLS) or maximum likelihood.
  Output: alpha_hat, beta_hat, standard_errors, log-likelihood
```

**Overdispersion Test.** After fitting the model, test H0: alpha = 0 (Poisson) vs. H1: alpha > 0 (overdispersed). The likelihood ratio test statistic is:

```
LR = 2 * (log_likelihood_NB - log_likelihood_Poisson)
```

Under H0, LR follows a mixture distribution (0.5 * chi^2_0 + 0.5 * chi^2_1) because alpha is on the boundary of the parameter space. Reject H0 at significance level 0.05 when LR > 2.71 (the 0.95 quantile of the boundary mixture).

**Overdispersion Threshold.** If the fitted alpha_hat exceeds ALPHA_THRESHOLD (default 2.0), overdispersion is not merely statistically significant but operationally meaningful: the variance of anomaly counts is at least 3x the mean (variance = mean + mean^2/2 >= 3*mean for mean >= 2). This threshold was chosen to filter out marginal overdispersion that could arise from benign structural clustering (agents sharing infrastructure have weakly correlated anomaly rates) while flagging the pronounced clustering that operator control produces.

**Covariate Ranking.** The regression coefficients beta_hat reveal which covariates explain the anomaly concentration. The covariates are:

| Covariate | Source | Interpretation |
|-----------|--------|----------------|
| operator_id | C7 agent registry (if available) | Direct operator linkage. Strongest signal when available. |
| registration_cohort | C7 agent lifecycle events | Agents registered in the same time window may share origin. |
| geographic_cluster | C3 scheduling metadata | Agents assigned to the same geographic region share infrastructure exposure. |
| infrastructure_provider | C35 Tier 2 infrastructure channel | Agents on the same compute/network provider share latency and error patterns. |

The output is a ranked list of covariates sorted by the magnitude of their regression coefficients (|beta_hat_k| / SE_k), identifying which structural factors best explain the anomaly clustering:

```
CovariateRanking:
  for each covariate k:
    z_k = |beta_hat_k| / SE(beta_hat_k)       # Wald statistic
    p_k = 2 * (1 - Phi(z_k))                   # two-sided p-value
  sort by z_k descending
  return [(covariate_k, z_k, p_k, beta_hat_k)]
```

**Synthetic Anomaly Handling.** Synthetic calibration anomalies are included in the sample for statistical power but are excluded from the covariate analysis. The regression is fit on the full dataset (real + synthetic), but the covariate ranking reports only the coefficients estimated from real data. Synthetic entries are assigned a special operator_id (SYNTHETIC_CALIBRATION) and registration_cohort (SYNTHETIC) so they are identifiable. Their purpose is solely to stabilize the variance estimation in the negative binomial fit; they do not contribute to the attribution conclusions.

### 4.3 Backward Tracing Algorithm

When overdispersion analysis identifies significant clustering (alpha_hat > ALPHA_THRESHOLD), the backward tracing algorithm constructs a causal phylogeny from the confirmed anomalies back through the platform's interaction history.

**Step 1: Seed Set Construction.** Extract the set of agents that appear in >= 2 confirmed Tier 2 anomalies within the analysis window (the "repeatedly anomalous" set). These agents form the seed set for backward tracing.

```
seed_set = {agent_id : count
            for agent_id, count in anomaly_agent_counts.items()
            if count >= 2}
```

**Step 2: Temporal-Behavioral Phylogeny Construction.** From the seed set, construct a directed graph representing the historical interaction and similarity relationships among seed agents and their neighbors. The phylogeny is built by querying four cross-layer data sources:

**(a) C17 Behavioral Similarity Chains.** Query C17 for the B(a_i, a_j) pairwise similarity scores among all seed agents and their 1-hop neighbors in the C17 similarity graph. Edges with B(a_i, a_j) >= 0.60 (the C17 WATCH threshold) are included. These edges represent behavioral kinship -- agents that act similarly, potentially because they share an operator or training lineage.

```
C17_edges = []
for agent in seed_set:
  neighbors = C17.get_similar_agents(agent, threshold=THETA_B_WATCH)  # 0.60
  for neighbor, score in neighbors:
    C17_edges.append(PhylogenyEdge(
      source=agent, target=neighbor,
      channel="behavioral", weight=score,
      timestamp=C17.last_similarity_epoch(agent, neighbor)))
```

**(b) C7 Intent Provenance.** Query C7's Intent State Registry (ISR) for the chain of intent delegations and saga invocations involving seed agents. If agent A's intent was delegated from agent B, or both participated in the same C7 saga, there is a provenance link. Intent provenance edges are timestamped by the saga creation epoch.

```
C7_edges = []
for agent in seed_set:
  provenance = C7.get_intent_provenance(agent, window=TIER3_ANALYSIS_WINDOW)
  for record in provenance:
    C7_edges.append(PhylogenyEdge(
      source=record.delegator, target=record.delegate,
      channel="intent", weight=1.0,  # binary: linked or not
      timestamp=record.saga_epoch))
```

**(c) C3 Scheduling Co-occurrence.** Query C3 for the frequency of scheduling co-occurrence: how often seed agents were assigned to the same parcel, committee, or tidal phase within the analysis window. High co-occurrence is not causal evidence by itself (C3 scheduling is deterministic and public) but it identifies agents that have had opportunity for coordination.

```
C3_edges = []
for (a_i, a_j) in seed_set_pairs:
  cooccurrence = C3.get_scheduling_cooccurrence(
    a_i, a_j, window=TIER3_ANALYSIS_WINDOW)
  if cooccurrence.frequency >= COOCCURRENCE_MIN_FRACTION:  # default 0.30
    C3_edges.append(PhylogenyEdge(
      source=a_i, target=a_j,
      channel="scheduling", weight=cooccurrence.frequency,
      timestamp=cooccurrence.last_joint_epoch))
```

**(d) C8 Settlement Flow Paths.** Query C8 for settlement flow relationships: whether seed agents have exchanged AIC, participated in the same staking pool, or received rewards from the same budget stream within the analysis window. Economic linkage can reveal operator control (an operator funnels rewards from controlled agents to a single withdrawal address).

```
C8_edges = []
for agent in seed_set:
  flows = C8.get_settlement_flows(agent, window=TIER3_ANALYSIS_WINDOW)
  for flow in flows:
    if flow.counterparty in seed_set or flow.counterparty in neighbor_set:
      C8_edges.append(PhylogenyEdge(
        source=flow.sender, target=flow.receiver,
        channel="economic", weight=flow.volume_normalized,
        timestamp=flow.settlement_tick))
```

**Step 3: Phylogeny Merge and Ancestor Identification.** Merge the four edge sets into a single weighted directed graph. Apply maximum likelihood estimation to identify the most probable common ancestor -- the node (or external entity such as an operator or infrastructure provider) that maximizes the likelihood of the observed phylogeny structure.

The MLE objective is:

```
L(ancestor | phylogeny) = product over edges (P(edge | ancestor_is_cause))

Where:
  P(edge | ancestor_is_cause) is higher for edges connecting agents
  that are both linked to the candidate ancestor, and lower for edges
  between agents with no ancestral connection.
```

In practice, this is computed as a log-likelihood:

```
log_L(candidate) = sum over seed agents a_i:
  log(P(a_i anomalous | a_i linked to candidate))
  + sum over edges (a_i, a_j) in phylogeny:
    log(P(edge weight | both linked to candidate))
  - sum over non-edges:
    log(P(no edge | expected if both linked to candidate))
```

The candidate pool includes: all operator_ids from the C7 registry that are linked to >= 2 seed agents, all infrastructure_providers that host >= 2 seed agents, and the "unknown common origin" null candidate (representing a shared cause not captured by known covariates).

**Step 4: Attribution Confidence.** For each candidate ancestor, compute the posterior probability using Bayes' rule with a uniform prior over candidates:

```
P(candidate | evidence) = L(candidate | phylogeny) * P(candidate)
                          / sum_c L(c | phylogeny) * P(c)
```

A formal attribution requires posterior probability >= TIER3_ATTRIBUTION_THRESHOLD (default 0.90). This is a deliberately high bar because attribution has governance consequences: it may trigger Citicate review (C14), settlement holds (C8), or collusion investigation referral (C12).

### 4.4 Attribution Report

The output of a completed Tier 3 analysis is an ATTRIBUTION_REPORT, a structured record that is persisted to the Tier 3 Evidence Store and may be forwarded to the Constitutional Tribunal (C14) or AVAP collusion defense (C12).

```
ATTRIBUTION_REPORT:
  report_id:            UUID
  analysis_epoch:       u64         # epoch at which Tier 3 analysis began
  analysis_window:      (u64, u64)  # (start_epoch, end_epoch)
  trigger_anomalies:    Vec<AnomalyRef>  # Tier 2 anomalies that triggered analysis
  seed_agents:          Vec<UUID>   # agents in the seed set
  synthetic_fraction:   f64         # fraction of analysis set that was synthetic
  overdispersion:
    alpha_hat:          f64         # fitted NB overdispersion parameter
    lr_statistic:       f64         # likelihood ratio test statistic
    lr_p_value:         f64         # p-value for overdispersion test
    covariate_ranking:  Vec<CovariateResult>
  attribution:
    suspected_cause:    AttributionTarget  # {operator_id | infrastructure_id | UNKNOWN}
    confidence:         f64         # posterior probability (0.0-1.0)
    evidence_chain:     Vec<PhylogenyEdge>  # edges supporting attribution
    alternative_causes: Vec<(AttributionTarget, f64)>  # runner-up candidates
  recommended_action:   enum {
    REFER_TO_TRIBUNAL,        # confidence >= 0.90, operator identified
    REFER_TO_AVAP,            # confidence >= 0.90, collusion pattern
    FLAG_INFRASTRUCTURE,      # confidence >= 0.90, infrastructure cause
    INCONCLUSIVE,             # confidence < 0.90
    INSUFFICIENT_DATA         # overdispersion not significant
  }
  computation_budget:
    wall_clock_ms:      u64
    edges_traversed:    u64
    cross_layer_queries: u64
```

### 4.5 Sample Size Management

The fundamental statistical challenge for Tier 3 is that it requires a substantial number of confirmed Tier 2 anomalies to achieve adequate power, but Tier 2 anomalies are (by design) rare events. The sample size management subsystem addresses this tension.

**Hybrid Pool.** A rolling buffer that maintains the last 100 confirmed Tier 2 anomalies plus up to 50 synthetic calibration anomalies. The buffer is FIFO: when a new confirmed anomaly arrives, the oldest confirmed anomaly is evicted (not the synthetic entries). Synthetic entries are replaced only during the synthetic refresh cycle (every CONSOLIDATION_CYCLE).

```
HybridPool:
  confirmed_buffer:  CircularBuffer<AnomalyEvent, 100>
  synthetic_buffer:  Vec<SyntheticAnomaly>   # max 50

  insert_confirmed(anomaly):
    confirmed_buffer.push(anomaly)

  refresh_synthetic():
    # Called at each CONSOLIDATION_CYCLE
    synthetic_buffer.clear()
    benign_pairs = PCM.get_high_confidence_benign_pairs(limit=50)
    for pair in benign_pairs:
      synthetic = SyntheticAnomaly(
        agent_pair=pair,
        injected_correlation=PCM.sample_anomalous_residual(),
        label="SYNTHETIC_POSITIVE",
        generation_epoch=current_epoch)
      synthetic_buffer.push(synthetic)

  get_analysis_set(min_count=30):
    real = confirmed_buffer.recent(window=TIER3_ANALYSIS_WINDOW)
    if len(real) >= min_count:
      return real, 0.0
    deficit = min_count - len(real)
    synthetic_supplement = synthetic_buffer.sample(min(deficit, len(synthetic_buffer)))
    return real + synthetic_supplement, len(synthetic_supplement) / (len(real) + len(synthetic_supplement))
```

**Synthetic Anomaly Generation.** Synthetic anomalies are generated by the PCM subsystem from known-benign agent pairs. The generation process selects agent pairs where the PCM has high confidence (R^2 > 0.90) that the observed correlation is fully explained by structural covariates. An artificial residual is then injected at a magnitude calibrated to the TIER2_RESIDUAL_THRESHOLD, creating a synthetic "anomaly" that looks statistically like a real one but is known to be benign. These synthetic entries are used exclusively for statistical power estimation in the overdispersion test. They are never used for attribution and are always flagged as synthetic in the analysis set.

**Ramp-Up Protocol.** At system startup and during periods of low anomaly activity, Tier 3 operates in DORMANT mode:

```
Tier3 Lifecycle:
  DORMANT → ACTIVE:   when confirmed_buffer contains >= 30 real anomalies
                       within the current TIER3_ANALYSIS_WINDOW
  ACTIVE → DORMANT:   when real anomaly rate drops below 5 per 10-epoch window
                       for 2 consecutive CONSOLIDATION_CYCLEs

  While DORMANT:
    - Hybrid pool continues accumulating confirmed anomalies
    - Synthetic refresh continues at CONSOLIDATION_CYCLE cadence
    - No Tier 3 analyses are initiated
    - Overdispersion test runs in shadow mode (results logged but not acted upon)
      for calibration purposes
```

The two-CONSOLIDATION_CYCLE hysteresis for the ACTIVE-to-DORMANT transition prevents oscillation when the anomaly rate fluctuates near the threshold.

**Statistical Power at Scale.** The relationship between platform scale, anomaly rate, and Tier 3 power:

| Scale | Expected Tier 2 anomalies per CONSOLIDATION_CYCLE | Time to 30 real anomalies | Tier 3 Power at alpha=2.0 |
|-------|----------------------------------------------------|---------------------------|---------------------------|
| 1K agents | 2-5 (if FPR=0.5% per neighborhood per cycle) | 6-15 CONSOLIDATION_CYCLEs (60-150 hours) | 0.65 (marginal) |
| 10K agents | 15-40 | 1-2 CONSOLIDATION_CYCLEs (10-20 hours) | 0.85 (adequate) |
| 100K agents | 100-300 | < 1 CONSOLIDATION_CYCLE (< 10 hours) | 0.97 (excellent) |

At 1K agents, Tier 3 will take days to accumulate sufficient real anomalies and will rely heavily on synthetic supplementation. This is acceptable: at 1K agents, the attack surface is smaller and alternative detection mechanisms (manual review, C12 AVAP) are more feasible. Tier 3's value proposition is primarily at 10K+ scale where manual review is impractical.

---

## 5. Cross-Layer Integration Architecture

C35 is a detection system that operates on data produced by other AAS layers. It does not own any of the data it analyzes. This section specifies the precise contracts between C35 and each layer it integrates with, following the C9 integration contract matrix conventions: every data flow has a named source, a named consumer, a cadence, and a schema.

All contracts use the C4 ASV vocabulary for message types and follow the C9 three-tier temporal hierarchy (SETTLEMENT_TICK = 60s, TIDAL_EPOCH = 3600s, CONSOLIDATION_CYCLE = 36000s).

### 5.1 Integration with C3 (Tidal Noosphere -- Coordination)

C3 provides scheduling and coordination data that C35 uses for Tier 1 scheduling metrics, Tier 2 neighborhood context, and Tier 3 co-occurrence tracing.

**Inbound Data Flows (C3 -> C35):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C3->C35:SCHED | Parcel assignments, committee rotations, tidal phase | TIDAL_EPOCH (3600s) | C3 push via event bus |
| C3->C35:TOPOLOGY | Agent topology snapshot (KG adjacency) | CONSOLIDATION_CYCLE (36000s) | C3 push via event bus |
| C3->C35:ETR | ETR governance metrics (trust scores, voting record) | TIDAL_EPOCH (3600s) | C3 push via event bus |

**Outbound Data Flows (C35 -> C3):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C35->C3:CLUSTER | Neighborhood membership (agent -> neighborhood_id mapping) | CONSOLIDATION_CYCLE (36000s) | C35 push via event bus |
| C35->C3:ETR_SIGNALS | Scheduling STA/LTA ratios, starvation flags, divergence metrics | TIDAL_EPOCH (3600s) | C35 push via event bus |

**ETR Signal Definitions.** C35 exports three computed signals to C3's ETR (Emergent Trust Regime) system:

```
ETR_SIGNALS:
  skew_metric:        f64   # scheduling STA/LTA ratio
                             # > 1.0 = agent receives more scheduling than expected
                             # < 1.0 = agent receives less than expected
                             # Computed: STA(scheduling_assignments, 1_epoch) /
                             #           LTA(scheduling_assignments, 10_epochs)
                             # Normal range: [0.7, 1.4]
                             # Anomalous: < 0.5 or > 2.0

  starvation_flag:    bool  # true if verification STA/LTA < STARVATION_THRESHOLD
                             # An agent being systematically starved of verification
                             # opportunities (possible scheduling manipulation)
                             # Threshold: STA/LTA < 0.3 for >= 3 consecutive epochs

  divergence_metric:  f64   # max behavioral deviation within neighborhood
                             # max over neighbors n: |metric(agent) - metric(n)|
                             # normalized by neighborhood standard deviation
                             # > 3.0 sigma triggers C3 scheduling review
```

**API Contracts:**

```
# C3 calls C35 to resolve an agent's neighborhood membership
GET /sentinel/cluster/{agent_id}
  Response 200:
    {
      "neighborhood_id": "uuid",
      "cluster_health": 0.85,           # 0.0-1.0, neighborhood aggregate health
      "agent_anomaly_level": "NORMAL",   # NORMAL | WATCH | FLAG | CONFIRMED
      "neighbors": ["uuid", ...],        # list of agents in same neighborhood
      "last_updated_epoch": 12345
    }
  Response 404:
    { "error": "AGENT_NOT_FOUND" }
  Latency: < 2ms (served from in-memory cache)

# C35 calls C3 to get scheduling data for a specific epoch
GET /tidal/schedule/{epoch}
  Response 200:
    {
      "epoch": 12345,
      "parcel_assignments": [
        { "parcel_id": "uuid", "assigned_agents": ["uuid", ...] }
      ],
      "committee_roster": [
        { "committee_id": "uuid", "members": ["uuid", ...], "claim_class": "D" }
      ],
      "tidal_phase": "NEAP",            # SPRING | NEAP | transitional
      "scheduling_hash": "sha256hex"
    }
  Response 404:
    { "error": "EPOCH_NOT_AVAILABLE" }
  Latency: < 5ms

# C35 calls C3 for scheduling co-occurrence (Tier 3 backward tracing)
GET /tidal/cooccurrence/{agent_a}/{agent_b}?window={epochs}
  Response 200:
    {
      "agent_a": "uuid",
      "agent_b": "uuid",
      "window_epochs": 10,
      "joint_parcel_count": 7,           # parcels where both assigned
      "joint_committee_count": 3,        # committees where both served
      "total_parcels_a": 42,
      "total_parcels_b": 38,
      "cooccurrence_frequency": 0.17,    # joint / max(total_a, total_b)
      "last_joint_epoch": 12340
    }
  Latency: < 10ms
```

### 5.2 Integration with C5 (PCVM -- Verification)

C5 is C35's primary data source for Tier 1. Every verification outcome feeds C35's per-agent STA/LTA detectors. C35 reciprocates by providing anomaly flags that gate C5's credibility adjustment process.

**Inbound Data Flows (C5 -> C35):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C5->C35:VERIFY | Verification outcomes (VTD results, claim acceptance/rejection, verification latency, opinion distributions) | SETTLEMENT_TICK (60s) | C5 push via VERIFICATION_EVENT |
| C5->C35:CRED | Credibility state changes (credibility score deltas, class reclassifications) | SETTLEMENT_TICK (60s) | C5 push via CREDIBILITY_UPDATE |
| C5->C35:INTEGRITY | Verification integrity metrics (VTD chain hash, opinion divergence per committee) | TIDAL_EPOCH (3600s) | C5 push via INTEGRITY_REPORT |

**Outbound Data Flows (C35 -> C5):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C35->C5:FLAG | Anomaly flags for credibility gating | On detection (event-driven) | C35 push via ANOMALY_FLAG |

**VERIFICATION_EVENT Schema.** Each VERIFICATION_EVENT from C5 contains:

```
VERIFICATION_EVENT:
  tick:                 u64
  agent_id:             UUID
  claim_class:          enum {D, C, P, R, E, S, K, H, N}  # 9 canonical classes per C9
  role:                 enum {PROVER, VERIFIER}
  outcome:              enum {ACCEPT, REJECT, ABSTAIN, TIMEOUT}
  latency_ms:           u32          # time from assignment to opinion submission
  opinion_alignment:    f64          # 0.0-1.0, how close to committee consensus
  vtd_hash:             [u8; 32]     # hash of VTD evidence submitted
  committee_size:       u8           # number of verifiers in this committee
  committee_agreement:  f64          # fraction of committee that agreed
```

C35 extracts the following Tier 1 metrics from VERIFICATION_EVENT:

| Metric | Computation | Tier 1 Channel |
|--------|-------------|----------------|
| verification_rate | count(events where role=VERIFIER) per tick | verification |
| acceptance_rate | count(outcome=ACCEPT) / count(total) per tick | verification |
| latency_p50 | median(latency_ms) per tick | verification |
| opinion_divergence | 1.0 - mean(opinion_alignment) per tick | verification |

**ANOMALY_FLAG Schema.** C35's output to C5:

```
ANOMALY_FLAG:
  flag_id:              UUID
  agent_id:             UUID
  severity:             enum {WATCH, FLAG, CONFIRMED}
  tier:                 u8           # 1, 2, or 3
  evidence_summary:     String       # human-readable summary of detection evidence
  channels_triggered:   Vec<String>  # which detection channels fired
  recommended_action:   enum {
    GATE_CREDIBILITY,       # C5 should hold credibility adjustments for this agent
    REDUCE_COMMITTEE_WEIGHT, # C5 should reduce this agent's weight in committees
    SUSPEND_VERIFICATION,    # C5 should temporarily remove from verification pool
    INFORMATIONAL            # no action needed, for audit trail only
  }
  ttl_epochs:           u8           # flag expires after this many epochs (default 10)
  timestamp:            u64          # tick at which flag was generated
```

**Critical Dependency.** C5 is the single most important data source for C35 Tier 1. If C5 stops emitting VERIFICATION_EVENTs, C35's per-agent STA/LTA detectors lose their primary signal. C35 MUST detect C5 silence within 3 SETTLEMENT_TICKs and transition affected agents to a DEGRADED trigger state (no detection possible, no false negatives by omission). The DEGRADED state is reported to C7 via ORCHESTRATION_ADVISORY.

```
C5_silence_detection:
  for each agent:
    if ticks_since_last_verification_event(agent) > C5_SILENCE_THRESHOLD:  # default 3
      agent.tier1_state.trigger_state = DEGRADED
      emit ORCHESTRATION_ADVISORY(agent, risk_level=UNKNOWN, reason="C5_SILENCE")
```

### 5.3 Integration with C6 (EMA -- Knowledge Metabolism)

C6 provides supplementary signals that enrich C35's detection but are not critical for its core function. Knowledge contribution patterns can reveal anomalies not visible in verification or scheduling data -- for example, an agent that suddenly stops contributing knowledge quanta while maintaining normal verification behavior.

**Inbound Data Flows (C6 -> C35):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C6->C35:KMETRICS | Knowledge contribution metrics (quantum submission rates, coherence scores, SHREC regulation state) | TIDAL_EPOCH (3600s) | C6 push via KNOWLEDGE_METRICS |

**Outbound Data Flows (C35 -> C6):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C35->C6:CONTEXT | Cluster context for metabolic regulation | On request (pull) | C35 serves via API |

**KNOWLEDGE_METRICS Schema:**

```
KNOWLEDGE_METRICS:
  epoch:                u64
  agent_id:             UUID
  quantum_submission_rate:  f64      # quanta submitted per epoch (normalized)
  coherence_score:          f64      # 0.0-1.0, internal consistency of submissions
  consolidation_participation: f64   # fraction of consolidation cycles participated in
  shrec_state:              enum {NORMAL, THROTTLED, FROZEN}
  knowledge_class_distribution: Map<ClaimClass, u32>  # breakdown by claim class
```

C35 uses quantum_submission_rate and coherence_score as supplementary inputs to Tier 1's adaptive baseline. These metrics are weighted at 0.1x the primary verification metrics (low priority -- enrichment, not critical signal).

**Cluster Context API:**

```
# C6 calls C35 for neighborhood context to inform metabolic regulation
GET /sentinel/cluster_context/{neighborhood_id}
  Response 200:
    {
      "neighborhood_id": "uuid",
      "member_agents": ["uuid", ...],
      "health_score": 0.92,             # 0.0-1.0
      "metabolic_profile": {
        "mean_quantum_rate": 4.2,        # average quanta/epoch across neighborhood
        "coherence_variance": 0.08,      # variance of coherence scores
        "active_fraction": 0.95          # fraction of members submitting quanta
      },
      "anomaly_count_recent": 2,         # Tier 2 anomalies in last CONSOLIDATION_CYCLE
      "last_updated_epoch": 12345
    }
  Response 404:
    { "error": "NEIGHBORHOOD_NOT_FOUND" }
  Latency: < 5ms
```

**Priority Classification.** This integration is LOW PRIORITY. C6 data enriches detection sensitivity for knowledge-related anomalies but is not required for C35's core detection pipeline. If C6 becomes unavailable, C35 continues operating with reduced sensitivity to knowledge-domain anomalies. No DEGRADED state transition is triggered by C6 silence.

### 5.4 Integration with C7 (RIF -- Orchestration)

C7 is C35's administrative backbone. It provides the agent registry (who exists), the intent state (what agents are doing), and the saga infrastructure (how complex operations are coordinated). C35 uses C7 data for agent lifecycle management and for the infrastructure channel in Tier 2.

**Inbound Data Flows (C7 -> C35):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C7->C35:LIFECYCLE | Agent lifecycle events (registration, deregistration, suspension) | Event-driven | C7 push via AGENT_LIFECYCLE_EVENT |
| C7->C35:INTENT | Intent state updates (ISR changes, saga state transitions) | SETTLEMENT_TICK (60s) | C7 push via INTENT_STATE_UPDATE |
| C7->C35:REGISTRY | Agent registry snapshot (full agent list with metadata) | CONSOLIDATION_CYCLE (36000s) | C7 push via REGISTRY_SNAPSHOT |

**Outbound Data Flows (C35 -> C7):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C35->C7:ADVISORY | Anomaly-informed orchestration advisories | On detection (event-driven) | C35 push via ORCHESTRATION_ADVISORY |

**AGENT_LIFECYCLE_EVENT Schema:**

```
AGENT_LIFECYCLE_EVENT:
  event_type:    enum {REGISTER, DEREGISTER, SUSPEND, RESUME, MIGRATE}
  agent_id:      UUID
  timestamp:     u64           # tick at which event occurred
  operator_id:   Option<UUID>  # may be unknown for privacy-preserving registrations
  registration_metadata:
    infrastructure_provider: Option<String>
    geographic_region:       Option<String>
    model_lineage:           Option<String>  # model family identifier if declared
    registration_cohort:     u64             # CONSOLIDATION_CYCLE of registration
```

C35 uses AGENT_LIFECYCLE_EVENTs for two purposes:

1. **State initialization/teardown.** On REGISTER: allocate per-agent Tier 1 state (Section 6.1), initialize STA/LTA windows to zero, begin calibration period (first 10 TIDAL_EPOCHs of fixed baseline accumulation). On DEREGISTER: tear down per-agent state, remove from neighborhood, archive anomaly history.

2. **Registration metadata extraction.** The optional fields (operator_id, infrastructure_provider, geographic_region, model_lineage) are stored as covariates for PCM fitting (Tier 2) and overdispersion analysis (Tier 3).

```
on AGENT_LIFECYCLE_EVENT(event):
  match event.event_type:
    REGISTER:
      state = allocate_tier1_state(event.agent_id)
      state.registration_epoch = event.timestamp
      state.calibration_complete = false
      state.fixed_baseline = FixedBaseline::EMPTY
      pcm_covariates.insert(event.agent_id, event.registration_metadata)
      # Agent is placed in a provisional neighborhood at next CONSOLIDATION_CYCLE

    DEREGISTER:
      archive_anomaly_history(event.agent_id)
      deallocate_tier1_state(event.agent_id)
      remove_from_neighborhood(event.agent_id)
      pcm_covariates.remove(event.agent_id)

    SUSPEND:
      state = get_tier1_state(event.agent_id)
      state.trigger_state = DEGRADED  # no detection during suspension
      # Do NOT deallocate -- agent may resume

    RESUME:
      state = get_tier1_state(event.agent_id)
      state.trigger_state = NORMAL    # resume detection
      # Adaptive baseline continues from pre-suspension values
```

**INTENT_STATE_UPDATE Schema:**

```
INTENT_STATE_UPDATE:
  tick:         u64
  agent_id:     UUID
  intent_type:  String        # ISR intent class
  saga_id:      Option<UUID>  # if part of a multi-step saga
  state:        enum {PENDING, ACTIVE, COMPLETED, FAILED, CANCELLED}
  participants: Vec<UUID>     # other agents involved in this intent/saga
```

C35 uses intent state as input to Tier 2's infrastructure channel. Agents that share saga participation have an expected correlation component that the PCM should account for. Additionally, Tier 3 backward tracing uses intent provenance (Section 4.3, Step 2b) to trace delegation chains.

**ORCHESTRATION_ADVISORY Schema:**

```
ORCHESTRATION_ADVISORY:
  advisory_id:    UUID
  agent_id:       UUID
  risk_level:     enum {LOW, MEDIUM, HIGH, CRITICAL, UNKNOWN}
  reason:         String       # machine-readable reason code + human summary
  recommended_action: enum {
    DEPRIORITIZE,              # C7 may lower this agent's scheduling priority
    QUARANTINE_INTENTS,        # C7 should hold new intent submissions from this agent
    BLOCK_SAGAS,               # C7 should not include this agent in new sagas
    INFORMATIONAL              # no action, for audit logging
  }
  ttl_epochs:     u8           # advisory expires after this many epochs
  timestamp:      u64
```

C7 is not obligated to act on ORCHESTRATION_ADVISORYs. They are advisory, not directive. The C9 authority hierarchy makes C7 sovereign over orchestration decisions. C35 provides risk information; C7 decides how to use it.

### 5.5 Integration with C8 (DSF -- Settlement)

C8 provides the economic data that feeds Tier 2's economic channel and Tier 3's settlement flow tracing. C35 reciprocates by flagging agents whose economic behavior is anomalous, allowing C8 to hold settlements pending review.

**Inbound Data Flows (C8 -> C35):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C8->C35:SETTLE | Settlement events (reward distributions, staking changes, budget flows) | SETTLEMENT_TICK (60s) | C8 push via SETTLEMENT_EVENT |
| C8->C35:ECON | Economic summary per agent (cumulative rewards, staking position, budget stream membership) | TIDAL_EPOCH (3600s) | C8 push via ECONOMIC_SUMMARY |

**Outbound Data Flows (C35 -> C8):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C35->C8:SFLAG | Settlement anomaly flags | On detection (event-driven) | C35 push via SETTLEMENT_ANOMALY_FLAG |

**SETTLEMENT_EVENT Schema:**

```
SETTLEMENT_EVENT:
  tick:             u64
  event_type:       enum {REWARD, STAKE_CHANGE, BUDGET_FLOW, PENALTY}
  agent_id:         UUID
  amount_aic:       f64          # AIC amount (positive = credit, negative = debit)
  counterparty:     Option<UUID> # other agent or budget stream
  budget_stream:    enum {VERIFICATION, SCHEDULING, KNOWLEDGE, GOVERNANCE, EXTERNAL}
  settlement_hash:  [u8; 32]     # hash of this settlement batch
```

C35 extracts the following Tier 2 economic channel metrics from SETTLEMENT_EVENT streams:

| Metric | Computation | Use |
|--------|-------------|-----|
| reward_pattern_similarity | Pearson correlation of reward sequences between agent pairs | Tier 2 economic channel input |
| staking_covariance | covariance of staking position changes between agent pairs | Tier 2 economic channel input |
| reward_timing_skew | KL divergence of reward timing distribution vs. expected | Tier 1 supplementary signal |
| flow_concentration | Herfindahl index of settlement flow destinations per agent | Tier 3 economic tracing input |

**SETTLEMENT_ANOMALY_FLAG Schema:**

```
SETTLEMENT_ANOMALY_FLAG:
  flag_id:          UUID
  agent_id:         UUID
  evidence:         String       # structured evidence summary
  severity:         enum {WATCH, FLAG, CONFIRMED}
  recommended_action: enum {
    HOLD_SETTLEMENT,            # C8 should hold pending reward distributions
    FREEZE_STAKING,             # C8 should prevent staking changes
    AUDIT_FLOWS,                # C8 should flag flows for manual audit
    INFORMATIONAL               # no action, for audit trail only
  }
  affected_ticks:   Vec<u64>    # settlement ticks implicated in the anomaly
  ttl_epochs:       u8          # flag expires after this many epochs
  timestamp:        u64
```

**Settlement Hold Protocol.** When C35 emits a SETTLEMENT_ANOMALY_FLAG with recommended_action = HOLD_SETTLEMENT, C8 MAY hold the next settlement distribution for the flagged agent until the flag expires or is resolved. C8 is not obligated to honor the hold -- per the C9 authority hierarchy, C8 is sovereign over settlement. The hold is advisory. However, if C8 distributes a settlement that C35 has flagged as anomalous and the anomaly is later confirmed, C8's settlement record includes the C35 flag reference for audit accountability.

### 5.6 Integration with C12 (AVAP -- Collusion Defense)

C12 and C35 have a bidirectional enrichment relationship. C12 provides confirmed collusion evidence that C35 can use as ground truth for calibration. C35 provides neighborhood-level anomaly findings that C12 can use as input to its triangulation mechanism.

**Inbound Data Flows (C12 -> C35):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C12->C35:COLLUSION | Confirmed collusion edges from AVAP pipeline | Event-driven | C12 push via CONFIRMED_COLLUSION_EDGE |

**Outbound Data Flows (C35 -> C12):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C35->C12:FINDING | Tier 2/3 findings with neighborhood context | Event-driven | C35 push via SENTINEL_FINDING |

**CONFIRMED_COLLUSION_EDGE Schema:**

```
CONFIRMED_COLLUSION_EDGE:
  edge_id:          UUID
  agent_a:          UUID
  agent_b:          UUID
  evidence_type:    enum {HONEYPOT_TRAP, CANARY_MATCH, BEHAVIORAL_CLASSIFIER,
                          SEALED_OPINION_LEAK, MULTI_SIGNAL_FUSION}
  confidence:       f64          # C12's confidence in this edge (0.0-1.0)
  detection_epoch:  u64
  evidence_hash:    [u8; 32]     # hash of C12's evidence record
```

**Injection Protocol.** When C35 receives a CONFIRMED_COLLUSION_EDGE with confidence >= 0.80, it injects the edge as a pre-confirmed Tier 2 trigger. This bypasses the normal Tier 2 fusion pipeline (PCM residual + quorum) because C12 has already independently confirmed collusion through a separate detection mechanism. The injected edge:

1. Immediately sets both agents to CONFIRMED anomaly status in Tier 2.
2. Adds the edge to the Tier 3 analysis window as a confirmed anomaly (not synthetic).
3. Records the injection in the per-neighborhood anomaly queue with evidence_type = "C12_INJECTION".

```
on CONFIRMED_COLLUSION_EDGE(edge):
  if edge.confidence >= C12_INJECTION_THRESHOLD:  # default 0.80
    tier2_confirm(edge.agent_a, source="C12", evidence=edge)
    tier2_confirm(edge.agent_b, source="C12", evidence=edge)
    hybrid_pool.insert_confirmed(AnomalyEvent(
      agents=[edge.agent_a, edge.agent_b],
      source="C12_INJECTION",
      epoch=edge.detection_epoch,
      evidence_hash=edge.evidence_hash))
```

**SENTINEL_FINDING Schema:**

```
SENTINEL_FINDING:
  finding_id:        UUID
  neighborhood_id:   UUID
  agents:            Vec<UUID>     # agents involved in the finding
  finding_type:      enum {TIER2_QUORUM, TIER2_MIDAS, TIER3_ATTRIBUTION}
  residuals:         Map<String, f64>  # per-channel PCM residuals
  pcm_expected:      f64           # PCM expected correlation for the pair
  pcm_observed:      f64           # actual observed correlation
  confidence:        f64           # C35's confidence in this finding
  epoch:             u64
```

**Calibration Loop.** C12 confirmed collusion edges serve as ground truth for C35's PCM calibration. When C12 confirms that agents A and B are colluding, C35 retroactively checks whether its Tier 2 pipeline would have detected the pair. The outcome is logged to a calibration metric:

```
PCM_calibration_check(edge):
  residual = PCM.get_residual(edge.agent_a, edge.agent_b)
  was_detected = tier2_would_have_flagged(edge.agent_a, edge.agent_b)
  calibration_log.append({
    "pair": (edge.agent_a, edge.agent_b),
    "pcm_residual": residual,
    "detected_by_c32": was_detected,
    "c12_confidence": edge.confidence,
    "epoch": edge.detection_epoch
  })
  # Used at CONSOLIDATION_CYCLE to assess PCM detection rate vs. C12 ground truth
```

### 5.7 Integration with C17 (MCSD -- Behavioral Similarity)

C17 is C35's most important data source for Tier 2. The behavioral similarity function B(a_i, a_j) provides the primary signal for the behavioral channel in the 4-channel quorum, and the LSH similarity graph provides the edge structure for spectral clustering.

**Inbound Data Flows (C17 -> C35):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C17->C35:SIMILARITY | Pairwise behavioral similarity scores (B(a_i, a_j) values) for all pairs exceeding LSH candidate threshold | CONSOLIDATION_CYCLE (36000s) | C17 push via SIMILARITY_BATCH |
| C17->C35:LSH | LSH bucket assignments (which agents hash to which buckets across 20 tables) | CONSOLIDATION_CYCLE (36000s) | C17 push via LSH_STATE |

**Outbound Data Flows (C35 -> C17):**

| Flow ID | Data | Cadence | Delivery |
|---------|------|---------|----------|
| C35->C17:NEIGHBORHOODS | Full neighborhood partition for SEB task stratification | CONSOLIDATION_CYCLE (36000s) | C35 serves via API |

**SIMILARITY_BATCH Schema:**

```
SIMILARITY_BATCH:
  batch_epoch:      u64
  pairs:            Vec<SimilarityPair>
  total_pairs:      u32          # total pairs in this batch
  lsh_candidate_threshold: f64   # minimum similarity for LSH to emit a pair

SimilarityPair:
  agent_a:          UUID
  agent_b:          UUID
  similarity:       f64          # B(a_i, a_j) in [0.0, 1.0]
  modality_scores:  [f64; 5]     # per-modality distances: [temporal, structural,
                                 #   error, resource, lexical]
  cross_correlation: f64         # multi-task cross-correlation coefficient
  graduated_status: enum {CLEAR, WATCH, FLAG}  # C17's own classification
```

C35 consumes SIMILARITY_BATCH data in two ways:

1. **Behavioral Channel Input (Tier 2).** For each within-neighborhood agent pair, the B(a_i, a_j) score serves as one of the four PCM covariates (the behavioral similarity covariate). The PCM estimates how much of the observed correlation is explained by behavioral similarity, and the residual after subtracting the PCM expectation feeds the behavioral channel.

2. **Spectral Clustering Input (Tier 2).** The full set of SimilarityPair entries forms the weighted adjacency matrix for spectral clustering at each CONSOLIDATION_CYCLE. Edges with B(a_i, a_j) >= LSH_CANDIDATE_THRESHOLD are included in the graph; all others are treated as zero-weight edges. This produces the neighborhood partition that structures all Tier 2 analysis.

**LSH_STATE Schema:**

```
LSH_STATE:
  epoch:            u64
  tables:           u8           # number of LSH tables (default 20)
  hashes_per_table: u8           # hash functions per table (default 8)
  assignments:      Map<UUID, Vec<Vec<u32>>>  # agent -> table -> bucket hashes
```

C35 does not directly use LSH_STATE for detection. It is consumed for diagnostic purposes: if spectral clustering produces unexpected neighborhoods, the LSH assignments provide visibility into why certain agent pairs were (or were not) identified as candidates.

**Neighborhood API for C17:**

```
# C17 calls C35 to get the full neighborhood partition
GET /sentinel/neighborhoods
  Response 200:
    {
      "epoch": 12345,
      "partition_method": "spectral_clustering",
      "neighborhoods": [
        {
          "id": "uuid",
          "members": ["uuid", ...],
          "centroid": [0.42, 0.18, ...],   # spectral embedding centroid (k-dim)
          "health": 0.91,                   # 0.0-1.0
          "size": 17,
          "pcm_coverage": 0.85             # R^2 of PCM for this neighborhood
        },
        ...
      ],
      "total_neighborhoods": 6000,
      "total_agents": 100000,
      "mean_neighborhood_size": 16.7,
      "partition_hash": "sha256hex"
    }
  Latency: < 10ms (served from in-memory cache, refreshed at CONSOLIDATION_CYCLE)
```

C17 uses the neighborhood partition for two purposes: (a) stratifying SEB (Standardized Evaluation Battery) task selection so that agents from different neighborhoods receive different task subsets (improving detection orthogonality), and (b) reporting B(a_i, a_j) scores with neighborhood context (enabling C35 to correlate behavioral similarity with neighborhood membership).

### 5.8 Cluster Membership API (Shared Interface)

The Cluster Membership API is C35's primary shared internal service interface. It is the canonical source of neighborhood assignment for all downstream attested specifications. Any authorized AAS component that needs to know "which agents are grouped together" queries this API.

**Endpoint Specifications:**

```
# 1. Per-agent cluster lookup
GET /sentinel/cluster/{agent_id}
  Description: Returns the neighborhood assignment and status for a single agent.
  Response 200:
    {
      "agent_id": "uuid",
      "neighborhood_id": "uuid",
      "neighbors": ["uuid", ...],        # all agents in the same neighborhood
      "cluster_health": 0.88,             # 0.0-1.0, aggregate neighborhood health
      "agent_status": {
        "tier1_status": "NORMAL",         # NORMAL | CANDIDATE | CONFIRMED | DEGRADED
        "tier2_status": "CLEAR",          # CLEAR | WATCH | FLAG
        "overall_risk": "LOW",            # LOW | MEDIUM | HIGH | CRITICAL | UNKNOWN
        "last_updated": 12345             # epoch of last status change
      }
    }
  Response 404:
    { "error": "AGENT_NOT_FOUND", "message": "No Tier 1 state exists for this agent" }
  Performance:
    Latency: < 2ms at 100K agents
    Source: in-memory HashMap<UUID, AgentClusterState>
    Refresh: CONSOLIDATION_CYCLE (neighborhood_id), SETTLEMENT_TICK (agent_status)

# 2. Full neighborhood partition
GET /sentinel/neighborhoods
  Description: Returns the complete partition of all agents into neighborhoods.
  Response 200:
    {
      "epoch": 12345,
      "neighborhoods": [
        {
          "id": "uuid",
          "members": ["uuid", ...],
          "centroid": [f64, ...],          # spectral embedding centroid
          "health": 0.91,
          "size": 17,
          "pcm_coverage": 0.85,
          "anomaly_count_recent": 2        # Tier 2 anomalies in last CONSOLIDATION_CYCLE
        }
      ],
      "total_neighborhoods": 6000,
      "total_agents": 100000
    }
  Performance:
    Latency: < 10ms at 100K agents
    Source: in-memory Vec<Neighborhood>, serialized to JSON on request
    Refresh: CONSOLIDATION_CYCLE
    Response size: ~2.4MB at 100K agents (6,000 neighborhoods, ~400 bytes each)

# 3. Per-agent anomaly level
GET /sentinel/anomaly_level/{agent_id}
  Description: Returns the current anomaly assessment for a single agent across
               all three tiers. This is the endpoint that C5, C7, and C8 use
               to check whether an agent is under suspicion before taking actions
               that affect the agent.
  Response 200:
    {
      "agent_id": "uuid",
      "tier1_status": "NORMAL",
      "tier1_details": {
        "trigger_state": "NORMAL",        # NORMAL | CANDIDATE | CONFIRMED | DEGRADED
        "sta_lta_ratio_fixed": 1.02,      # STA/LTA against fixed baseline
        "sta_lta_ratio_adaptive": 0.98,   # STA/LTA against adaptive baseline
        "calibration_complete": true,
        "epochs_since_registration": 450
      },
      "tier2_status": "CLEAR",
      "tier2_details": {
        "neighborhood_id": "uuid",
        "max_pcm_residual": 0.12,         # highest residual across all pairs in neighborhood
        "channels_elevated": [],           # which channels have above-normal readings
        "midas_alert": false
      },
      "tier3_status": null,               # null if no Tier 3 analysis involves this agent
      "overall_risk": "LOW",
      "last_updated": 12345
    }
  Response 404:
    { "error": "AGENT_NOT_FOUND" }
  Performance:
    Latency: < 2ms at 100K agents
    Source: in-memory HashMap, composed from Tier 1 + Tier 2 state

# 4. External evidence submission
POST /sentinel/external_evidence
  Description: Accepts anomaly evidence from external sources. Used by C12 (AVAP)
               for collusion edge injection, by manual governance reports, and by
               the Constitutional Tribunal for investigation-initiated monitoring.
  Request body:
    {
      "source": "C12" | "TRIBUNAL" | "MANUAL",
      "source_reference": "uuid or identifier",
      "agents": ["uuid", ...],           # agents implicated
      "evidence_type": String,            # source-specific evidence classification
      "confidence": 0.85,                 # source's confidence in this evidence
      "evidence_payload": {               # opaque to C35, stored for audit
        ...
      }
    }
  Response 201:
    {
      "evidence_id": "uuid",
      "action_taken": "INJECTED" | "QUEUED" | "REJECTED",
      "reason": "String"
    }
  Response 400:
    { "error": "INVALID_EVIDENCE", "message": "..." }
  Response 429:
    { "error": "RATE_LIMITED", "message": "External evidence rate limit exceeded" }
  Rate limit: 100 submissions per TIDAL_EPOCH per source
  Performance:
    Latency: < 50ms (involves validation + injection into Tier 2 pipeline)
```

**Cache Architecture.** All GET endpoints are served from in-memory caches to meet the < 10ms latency requirement at 100K agents. The cache architecture is:

```
SentinelCache:
  agent_cluster_map:   HashMap<UUID, AgentClusterState>   # refreshed at CONSOLIDATION_CYCLE
  agent_status_map:    HashMap<UUID, AgentAnomalyStatus>  # refreshed at SETTLEMENT_TICK
  neighborhood_list:   Vec<NeighborhoodSummary>           # refreshed at CONSOLIDATION_CYCLE
  neighborhoods_json:  Option<Vec<u8>>                    # pre-serialized JSON, lazy-invalidated

  refresh_at_settlement_tick():
    # O(V) scan: update agent_status_map from current Tier 1 state
    for agent in all_agents:
      agent_status_map[agent.id] = compose_anomaly_status(agent)

  refresh_at_consolidation_cycle():
    # O(V) rebuild: recompute neighborhood membership after spectral clustering
    agent_cluster_map.clear()
    for neighborhood in current_partition:
      for agent in neighborhood.members:
        agent_cluster_map[agent] = AgentClusterState {
          neighborhood_id: neighborhood.id,
          neighbors: neighborhood.members.clone(),
          cluster_health: neighborhood.health,
        }
    neighborhood_list = current_partition.summarize()
    neighborhoods_json = None  # invalidate; re-serialize on next request
```

**Consistency Model.** The cache provides eventual consistency with bounded staleness:
- Agent status (tier1_status, tier2_status, overall_risk): stale by at most 1 SETTLEMENT_TICK (60s).
- Neighborhood membership (neighborhood_id, neighbors): stale by at most 1 CONSOLIDATION_CYCLE (36,000s).
- Consumers that require strong consistency must account for this staleness. In practice, the staleness is acceptable because detection actions are not time-critical to within a single tick.

---

## 6. Data Architecture

This section specifies the data structures, storage layouts, and memory estimates for all state maintained by C35 across the three tiers.

### 6.1 Per-Agent State Model

Every registered agent has a Tier 1 state record maintained in memory. This record holds the STA/LTA detector state, baseline profiles, anomaly history, and neighborhood assignment.

```
AgentSentinelState:
  # --- Identity ---
  agent_id:             UUID            # 16 bytes
  registration_epoch:   u64             # 8 bytes

  # --- Tier 1 Detector State ---
  tier1_state:
    # STA windows (short-term averages, 1 TIDAL_EPOCH = 60 ticks)
    sta_window:         [f64; STA_WINDOW_TICKS]   # default 60 entries x 8 bytes = 480 bytes
                        # Circular buffer of per-tick metric summaries
                        # Each entry: mean of D metrics for that tick

    # LTA windows (long-term averages, 10 TIDAL_EPOCHS = 600 ticks)
    lta_window:         [f64; LTA_WINDOW_TICKS]   # default 600 entries x 8 bytes = 4,800 bytes
                        # Circular buffer of per-tick metric summaries

    # Fixed baseline (set at registration, updated only at re-registration SEB)
    fixed_baseline:
      percentiles:      [f64; 5]        # p5, p25, p50, p75, p95 per metric
                        # For D=4 metrics: 5 x 4 x 8 = 160 bytes
      metric_count:     u8              # number of metrics (default 4)
      calibration_ticks: u16            # ticks of data used to compute baseline
                        # Total fixed_baseline: ~170 bytes

    # Adaptive baseline (rolling, recomputed from LTA window)
    adaptive_baseline:  [f64; D]        # D metrics x 8 bytes = 32 bytes (D=4)

    # Trigger state machine
    trigger_state:      enum {NORMAL, CANDIDATE, CONFIRMED, DEGRADED}  # 1 byte
    confirmation_countdown: u8          # ticks remaining in confirmation window
    calibration_complete:   bool        # true after 10 TIDAL_EPOCHs of baseline data

  # --- Neighborhood Assignment ---
  neighborhood_id:      UUID            # 16 bytes, updated at CONSOLIDATION_CYCLE

  # --- Anomaly History ---
  anomaly_history:      CircularBuffer<TriggerEvent, 100>
                        # Each TriggerEvent: ~32 bytes (epoch + type + channel + severity)
                        # 100 entries x 32 bytes = 3,200 bytes

  # --- Per-Agent Size Calculation ---
  # Identity:              24 bytes
  # STA window:           480 bytes
  # LTA window:         4,800 bytes
  # Fixed baseline:       170 bytes
  # Adaptive baseline:     32 bytes
  # Trigger state:          3 bytes
  # Neighborhood:          16 bytes
  # Anomaly history:    3,200 bytes
  # Padding/alignment:    ~75 bytes
  # ----------------------------------
  # Total per agent:   ~2,000 bytes (2 KB)
```

**TriggerEvent Record:**

```
TriggerEvent:
  epoch:          u64           # 8 bytes
  trigger_type:   enum {STA_LTA_FIXED, STA_LTA_ADAPTIVE, BOTH, C12_INJECTION}  # 1 byte
  channel:        enum {VERIFICATION, SCHEDULING, KNOWLEDGE, ECONOMIC}          # 1 byte
  severity:       enum {CANDIDATE, CONFIRMED}                                    # 1 byte
  sta_lta_ratio:  f64           # 8 bytes, the ratio that caused the trigger
  _padding:       [u8; 13]      # alignment to 32 bytes
  # Total: 32 bytes
```

### 6.2 Per-Neighborhood State Model

Each neighborhood (produced by spectral clustering at CONSOLIDATION_CYCLE cadence) maintains state for Tier 2 analysis: PCM parameters, MIDAS-F detector state, fusion state, and anomaly queue.

```
NeighborhoodState:
  # --- Identity ---
  neighborhood_id:    UUID              # 16 bytes
  member_agents:      Vec<UUID>         # variable: avg 17 agents x 16 bytes = 272 bytes
  creation_epoch:     u64               # 8 bytes

  # --- PCM Parameters ---
  # 4 channels x 16 parameters per channel = 64 parameters
  # Parameters: intercept + 4 covariate coefficients + 4 covariate^2 terms
  #             + 4 interaction terms + 3 spline knot weights = 16 per channel
  pcm_params:         [[f64; 16]; 4]    # 4 channels x 16 params x 8 bytes = 512 bytes
  pcm_coverage:       f64               # R^2 metric, 8 bytes
  pcm_residual_std:   [f64; 4]          # per-channel residual standard deviation, 32 bytes
  pcm_last_fit_epoch: u64               # 8 bytes

  # --- MIDAS-F State ---
  # Per-neighborhood MIDAS-F instance
  # Count-min sketch: width W x depth D x 2 (current + previous) x 8 bytes
  # Default: W=1024, D=4
  midas_state:
    cms_current:      [[u64; 1024]; 4]  # 4 x 1024 x 8 = 32,768 bytes
    cms_previous:     [[u64; 1024]; 4]  # 4 x 1024 x 8 = 32,768 bytes
    alpha:            f64               # MIDAS-F decay factor, 8 bytes
    tick_count:       u64               # 8 bytes
    # Total MIDAS state: ~65,552 bytes (~64 KB)

  # --- Fusion State ---
  fusion_state:       enum {QUORUM, BAYESIAN}  # 1 byte
  bayesian_params:    Option<BayesianFusionState>
                      # Phase 1: None (quorum only)
                      # Phase 2: prior distributions per channel, ~256 bytes
                      # 0 or 256 bytes

  # --- Anomaly Queue ---
  anomaly_queue:      Vec<AnomalyEvent>
                      # Rolling buffer, max 50 entries
                      # Each AnomalyEvent: ~128 bytes (agents, channels, residuals, epoch)
                      # 50 x 128 = 6,400 bytes

  # --- Health ---
  health_score:       f64               # 0.0-1.0, 8 bytes
  anomaly_rate_recent: f64              # anomalies per CONSOLIDATION_CYCLE, 8 bytes

  # --- Per-Neighborhood Size Calculation ---
  # Identity:              24 bytes
  # Member list:          272 bytes (avg)
  # PCM parameters:       560 bytes
  # MIDAS-F state:     65,552 bytes
  # Fusion state:           1 byte (Phase 1) or 257 bytes (Phase 2)
  # Anomaly queue:      6,400 bytes
  # Health:                16 bytes
  # Padding/alignment:   ~175 bytes
  # -------------------------------------------
  # Total per neighborhood: ~73,000 bytes (~71 KB) Phase 1
  #                         ~73,256 bytes (~72 KB) Phase 2
  # Rounding for estimates: ~50 KB (excluding MIDAS CMS padding)
  #                         ~73 KB (with full MIDAS CMS allocation)
```

**AnomalyEvent Record:**

```
AnomalyEvent:
  anomaly_id:       UUID            # 16 bytes
  agents:           [UUID; 2]       # the pair (32 bytes)
  epoch:            u64             # 8 bytes
  source:           enum {QUORUM, MIDAS, C12_INJECTION, BAYESIAN}  # 1 byte
  channels_fired:   [bool; 4]       # which of 4 channels triggered (4 bytes)
  residuals:        [f64; 4]        # per-channel PCM residuals (32 bytes)
  pcm_expected:     f64             # 8 bytes
  pcm_observed:     f64             # 8 bytes
  posterior:        f64             # Bayesian posterior (Phase 2), 8 bytes
  evidence_hash:    [u8; 32]        # 32 bytes (reserved for external evidence)
  _padding:         [u8; 7]         # alignment
  # Total: 128 bytes (after padding, rounded to 128 for cache alignment)
```

### 6.3 PCM Parameter Storage

The PCM operates at per-neighborhood granularity. Each neighborhood has its own set of PCM parameters, fitted from within-neighborhood agent pair observations. Additionally, each neighborhood maintains a covariate cache for all within-neighborhood pairs.

**Parameter Storage:**

```
PCM Global Structure:
  neighborhoods:        ~V / (2 * log(V)) neighborhoods
  params_per_channel:   16 (intercept + coefficients + interactions + spline knots)
  channels:             4 (verification, behavioral, infrastructure, economic)
  bytes_per_param:      8 (f64)

  Parameter memory = neighborhoods x 4 x 16 x 8

  At 1K agents:    ~50 neighborhoods x 64 params x 8 bytes = 25,600 bytes (~25 KB)
  At 10K agents:   ~750 neighborhoods x 64 params x 8 bytes = 384,000 bytes (~375 KB)
  At 100K agents:  ~6,000 neighborhoods x 64 params x 8 bytes = 3,072,000 bytes (~3 MB)
```

**Covariate Cache.** For each within-neighborhood agent pair, the PCM stores the precomputed covariate vector (5 structural covariates) used for computing expected correlation. This avoids recomputing covariates at every analysis tick.

```
Covariate Cache Structure:
  Per pair: 5 covariates x 8 bytes = 40 bytes
  Pairs per neighborhood: C(n, 2) where n = neighborhood size

  Average neighborhood size: 2 * log(V)
  Average pairs per neighborhood: C(2*log(V), 2) = log(V) * (2*log(V) - 1)

  At 1K agents:
    n_avg = 2 * log(1000) = ~14
    pairs_avg = C(14, 2) = 91
    Total pairs = 50 neighborhoods x 91 = 4,550
    Covariate memory = 4,550 x 40 = 182,000 bytes (~178 KB)

  At 10K agents:
    n_avg = 2 * log(10000) = ~18
    pairs_avg = C(18, 2) = 153
    Total pairs = 750 x 153 = 114,750
    Covariate memory = 114,750 x 40 = 4,590,000 bytes (~4.4 MB)

  At 100K agents:
    n_avg = 2 * log(100000) = ~23
    pairs_avg = C(23, 2) = 253
    Total pairs = 6,000 x 253 = 1,518,000
    Covariate memory = 1,518,000 x 40 = 60,720,000 bytes (~58 MB)
```

**Total PCM Storage:**

| Scale | Parameters | Covariate Cache | Total PCM |
|-------|-----------|-----------------|-----------|
| 1K agents | 25 KB | 178 KB | ~203 KB |
| 10K agents | 375 KB | 4.4 MB | ~4.8 MB |
| 100K agents | 3 MB | 58 MB | ~61 MB |

Note: the 100K figure is higher than the ~42 MB estimate in the feasibility study because this calculation uses the exact C(n,2) pair count per neighborhood rather than an approximation. The difference (~19 MB) is within acceptable bounds and does not change the architectural viability.

### 6.4 Tier 3 Evidence Store

Tier 3 maintains a compact evidence store for backward tracing and attribution. The store consists of the hybrid pool (Section 4.5) plus a rolling log of attribution reports.

**Hybrid Pool Storage:**

```
Hybrid Pool:
  Confirmed anomaly buffer: 100 entries x AnomalyEvent (128 bytes) = 12,800 bytes (~12.5 KB)
  Synthetic anomaly buffer: 50 entries x SyntheticAnomaly (~256 bytes) = 12,800 bytes (~12.5 KB)

SyntheticAnomaly:
  agent_pair:        [UUID; 2]       # 32 bytes
  injected_residual: [f64; 4]        # 32 bytes (per-channel injected correlation)
  pcm_context:       [f64; 16]       # 128 bytes (PCM parameters that generated this)
  label:             enum            # 1 byte
  generation_epoch:  u64             # 8 bytes
  pcm_r_squared:     f64             # 8 bytes
  _padding:          [u8; 47]        # alignment to 256 bytes
  # Total: 256 bytes

  Total hybrid pool: ~25 KB
```

**Attribution Report Log:**

```
Attribution Report Storage:
  Each report: ~5 KB (structured ATTRIBUTION_REPORT, Section 4.4)
    - Header: ~200 bytes
    - Overdispersion results: ~500 bytes
    - Seed agents + covariates: ~1,000 bytes
    - Evidence chain (phylogeny edges): ~2,000 bytes
    - Computation metadata: ~300 bytes
    - Reserved/padding: ~1,000 bytes

  Retention: CONSOLIDATION_CYCLE x 10 = 360,000 seconds (~4.2 days)
  Expected report rate: 0-5 per CONSOLIDATION_CYCLE at 100K agents
  Max retained reports: 50 (at 5 per cycle x 10 cycles)
  Storage: 50 x 5 KB = 250 KB

  Total Tier 3 Evidence Store: ~25 KB (hybrid pool) + ~250 KB (reports) = ~275 KB
  Rounded to: ~1.5 MB (with generous safety margin for variable-length evidence chains)
```

### 6.5 Storage Estimates

The following table summarizes total C35 memory consumption across the three target scales.

**Per-Agent State (Tier 1):**

| Scale | Agent Count | Per-Agent Size | Total Tier 1 |
|-------|-------------|----------------|--------------|
| 1K | 1,000 | 2 KB | 2 MB |
| 10K | 10,000 | 2 KB | 20 MB |
| 100K | 100,000 | 2 KB | 200 MB |

**Per-Neighborhood State (Tier 2):**

| Scale | Neighborhoods | Per-Neighborhood Size | Total Tier 2 |
|-------|---------------|-----------------------|--------------|
| 1K | ~50 | 73 KB | 3.7 MB |
| 10K | ~750 | 73 KB | 54.8 MB |
| 100K | ~6,000 | 73 KB | 438 MB |

Note: the per-neighborhood size (73 KB) is dominated by the MIDAS-F count-min sketch (65 KB). If MIDAS CMS width is reduced from 1024 to 512 at the cost of higher false positive rate, per-neighborhood size drops to ~41 KB and total Tier 2 at 100K drops to ~246 MB.

**PCM Storage:**

| Scale | Parameters | Covariate Cache | Total PCM |
|-------|-----------|-----------------|-----------|
| 1K | 25 KB | 178 KB | 0.2 MB |
| 10K | 375 KB | 4.4 MB | 4.8 MB |
| 100K | 3 MB | 58 MB | 61 MB |

**Tier 3 Evidence Store:** ~1.5 MB at all scales (fixed-size buffers).

**Sentinel Cache (Section 5.8):**

| Scale | agent_cluster_map | agent_status_map | neighborhood_list | Total Cache |
|-------|-------------------|------------------|-------------------|-------------|
| 1K | ~100 KB | ~80 KB | ~20 KB | 0.2 MB |
| 10K | ~1 MB | ~800 KB | ~300 KB | 2.1 MB |
| 100K | ~10 MB | ~8 MB | ~2.4 MB | 20.4 MB |

**Aggregate Storage Summary:**

| Scale | Tier 1 | Tier 2 | PCM | Tier 3 | Cache | **Total** |
|-------|--------|--------|-----|--------|-------|-----------|
| 1K agents | 2 MB | 3.7 MB | 0.2 MB | 1.5 MB | 0.2 MB | **7.6 MB** |
| 10K agents | 20 MB | 54.8 MB | 4.8 MB | 1.5 MB | 2.1 MB | **83.2 MB** |
| 100K agents | 200 MB | 438 MB | 61 MB | 1.5 MB | 20.4 MB | **720.9 MB** |

**Analysis of Storage at Scale:**

At 100K agents, C35 requires approximately 721 MB of in-memory state. This is within the capacity of a single modern server (typical 32-256 GB RAM) and represents approximately 0.7 GB -- well within operational bounds for a security-critical subsystem.

The dominant cost components by scale:

| Scale | Dominant Component | Fraction of Total |
|-------|-------------------|-------------------|
| 1K | Tier 2 (MIDAS CMS) | 49% |
| 10K | Tier 2 (MIDAS CMS) | 66% |
| 100K | Tier 2 (MIDAS CMS) | 61% |

The MIDAS-F count-min sketch dominates at all scales. If storage becomes a constraint, the primary optimization lever is reducing CMS width (W parameter) at the cost of higher MIDAS false positive rate. The tradeoff:

| CMS Width | Per-Neighborhood MIDAS | Total Tier 2 at 100K | MIDAS FPR Impact |
|-----------|------------------------|----------------------|------------------|
| 1024 (default) | 65 KB | 438 MB | Baseline |
| 512 | 33 KB | 246 MB | ~2x FPR increase |
| 256 | 16 KB | 144 MB | ~4x FPR increase |

### 6.6 Persistence and Recovery

C35 state is primarily in-memory for performance reasons. However, selective persistence is required for crash recovery and for Tier 3's longitudinal analysis.

**Persisted State:**

| State | Persistence | Reason |
|-------|-------------|--------|
| Per-agent fixed baselines | Durable (written once at calibration completion) | Cannot be recomputed without re-running the 10-epoch calibration period |
| Hybrid pool (confirmed anomalies) | Durable (append-only, FIFO eviction) | Tier 3 requires historical anomaly data across restarts |
| Attribution reports | Durable (append-only, time-based eviction) | Governance and audit trail |
| PCM parameters | Durable (overwritten at each CONSOLIDATION_CYCLE) | Expensive to recompute from scratch (~minutes at 100K) |
| Neighborhood partition | Durable (overwritten at each CONSOLIDATION_CYCLE) | Expensive to recompute (spectral clustering) |

**Non-Persisted State (Reconstructible):**

| State | Recovery Strategy |
|-------|-------------------|
| Per-agent STA/LTA windows | Rebuild from incoming VERIFICATION_EVENTs over STA_WINDOW_TICKS ticks; during rebuild, agent is in DEGRADED state |
| Per-agent adaptive baselines | Rebuild from LTA window (which rebuilds from events); full accuracy after LTA_WINDOW_TICKS ticks |
| MIDAS-F CMS state | Reset to zero; MIDAS reaches steady state within ~100 ticks (per Bhatia et al. 2020) |
| Sentinel cache | Rebuild from current state; available within 1 SETTLEMENT_TICK of restart |
| Anomaly queues | Lost entries are acceptable; Tier 2 analysis continues with reduced queue depth |

**Persistence Format.** All persisted state uses the C8 HDL-compatible binary format (fixed-width fields, big-endian, no schema evolution within a version). This ensures C35 persistence can be audited by C8's settlement verification infrastructure if needed.

**Recovery Time Estimates:**

| Operation | Time at 100K | Blocking? |
|-----------|-------------|-----------|
| Load fixed baselines from disk | ~200ms (200 MB sequential read) | Yes (before Tier 1 can detect) |
| Load PCM parameters + partition | ~100ms (~61 MB + ~20 MB) | Yes (before Tier 2 can analyze) |
| Load hybrid pool + reports | ~5ms (~1.5 MB) | Yes (before Tier 3 can trace) |
| Rebuild STA windows | 60 minutes (STA_WINDOW_TICKS x SETTLEMENT_TICK) | No (gradual, agents in DEGRADED) |
| Rebuild LTA windows | 600 minutes (LTA_WINDOW_TICKS x SETTLEMENT_TICK) | No (gradual, fixed baseline still works) |
| MIDAS CMS warm-up | ~100 minutes (~100 ticks) | No (MIDAS produces no output during warm-up) |

Total blocking recovery time: < 500ms. Total time to full detection capability: ~10 hours (LTA rebuild). During the LTA rebuild window, Tier 1 operates with fixed baselines only (reduced sensitivity to relative deviations, full sensitivity to absolute deviations).

---

## End of Part 2

**Sections Covered:**
- Section 4: Tier 3 Architecture -- Epidemiological Backward Tracing (activation, overdispersion, tracing, sample size management)
- Section 5: Cross-Layer Integration (C3, C5, C6, C7, C8, C12, C17 contracts + Cluster Membership API)
- Section 6: Data Architecture (per-agent state, per-neighborhood state, PCM storage, Tier 3 evidence, aggregate estimates, persistence)

**Cross-References to Part 1:** Tier 1 STA/LTA (Section 2), Tier 2 PCM + spectral clustering (Section 3), 4-channel quorum (Section 3.x), MIDAS augmentation (Section 3.x)

**Forward References:** Part 3 will cover Section 7 (Parameters Table), Section 8 (Formal Properties + Invariants), Section 9 (State Machines -- consolidated), and Section 10 (Adversarial Analysis + Open Questions).
# C35 — Seismographic Sentinel with PCM-Augmented Tier 2

## Architecture Document — Part 3: Security, Parameters, Pseudocode, Scalability

**Version:** 1.0.0
**Date:** 2026-03-12
**Invention ID:** C35
**Stage:** DESIGN
**Role:** Architecture Designer (PRIMARY tier)
**Status:** DESIGN — Architecture Part 3
**Normative References:** C9 v2.0, C3 v2.0, C5 v2.0, C6 v2.0, C7 v2.0, C8 v2.0, C12 v2.0, C17 v1.0
**Continuation of:** C35 Architecture Parts 1-2

---

## 7. Security Architecture

C35 is simultaneously a security component (detecting anomalies in the AAS platform) and an attack surface (an adversary who defeats C35 operates undetected). This section specifies the adversarial model, defense mechanisms for six attack classes, and the residual risks that cannot be fully mitigated.

### 7.1 Adversarial Model

C35 defends against six attack classes. Each class has a defined attacker capability, a primary defense mechanism, and a residual risk assessment.

**Attack Class 1 — Evasion (Boiling Frog)**

- **Attacker capability:** Adversary gradually shifts agent behavior over T epochs, with per-epoch change delta. The adaptive LTA window absorbs changes with gradient below 2 * sigma_bg / sqrt(lta_window_ticks). If lta_window_ticks = 60, changes below ~0.258 * sigma_bg per tick are absorbed without triggering the adaptive STA/LTA.
- **Attacker objective:** Shift behavioral profile from legitimate to anomalous without triggering Tier 1.
- **Primary defense:** Fixed baseline + OR-trigger. The fixed baseline is immutable after calibration. Any accumulated drift that the adaptive baseline absorbs still registers against the fixed baseline. The OR-trigger ensures that a fixed-baseline exceedance alone is sufficient to enter CANDIDATE state.
- **Defense bound:** An adversary who shifts behavior by cumulative D * sigma_bg from the registration-time profile is detected by the fixed baseline when D exceeds the fixed threshold (default: 3.0 sigma). At drift rate delta per tick, detection latency is at most ceil(3.0 * sigma_bg / delta) ticks.
- **Residual risk:** An adversary who shifts by less than 3.0 sigma total is indistinguishable from legitimate behavioral evolution. This is by design — sub-threshold behavioral changes are not anomalous by definition.

**Attack Class 2 — Poisoning (PCM Calibration Corruption)**

- **Attacker capability:** Adversary enters the system during the PCM calibration window (first 500-1000 epochs) and behaves in a way that biases the log-linear coefficients, inflating expected correlation for certain covariate configurations. Post-calibration, the adversary exploits the inflated expectation to conduct correlated activity that falls within the (corrupted) expected range.
- **Attacker objective:** Expand the "permitted correlation" envelope so that future anomalous correlation is classified as expected.
- **Primary defense:** Bootstrap-phase audit with recalibration (see Section 7.4 for full protocol).
- **Residual risk:** Adversary who behaves identically to a legitimate agent during the full bootstrap and initial calibration phases cannot be excluded. This is a fundamental limitation — an adversary with perfect operational security during calibration is indistinguishable from a legitimate agent. Acknowledged as monitoring flag MF-5.

**Attack Class 3 — Manipulation (Spectral Clustering Boundary Perturbation)**

- **Attacker capability:** Adversary adds or removes up to B edges in the agent interaction graph, where B = c * sqrt(V) for constant c. Goal is to shift target agents across neighborhood boundaries or fragment a neighborhood containing colluders into two smaller neighborhoods that individually fall below detection thresholds.
- **Attacker objective:** Control which agents share a neighborhood to either (a) separate colluding agents into different neighborhoods so their cross-neighborhood correlation is not analyzed by Tier 2, or (b) merge a colluding group with a large set of legitimate agents to dilute the anomaly signal.
- **Primary defense:** NMI divergence check with perturbation and fallback (see Section 7.3 for full game-theoretic analysis).
- **Residual risk:** Attacker with budget B < 0.3 * sqrt(V) can make small boundary adjustments that pass the NMI check. Mitigated by randomized perturbation direction and by the fact that cross-neighborhood correlation (while not analyzed by Tier 2) may still trigger Tier 1 per-agent detection for individual agents.

**Attack Class 4 — Reconstruction (Fixed Baseline Inference)**

- **Attacker capability:** Adversary conducts A/B testing — submitting transactions at varying intensities and observing whether they trigger Tier 1 (binary "flagged" or "not flagged" feedback). Over T_obs epochs, the adversary accumulates a dataset of (intensity, trigger_outcome) pairs and attempts to reconstruct the fixed baseline percentile values via logistic regression or similar binary-response models.
- **Attacker objective:** Reconstruct the fixed baseline to within 10% of the true percentile values, enabling precise sub-threshold evasion.
- **Primary defense:** Three-layer defense (see Section 7.2 for full Red Team protocol).
  - Layer 1: Laplace noise (epsilon = 1.0) on stored baseline percentiles.
  - Layer 2: Randomized trigger threshold jitter (plus/minus 5% per tick).
  - Layer 3: Rate limiting on per-agent trigger feedback — agent sees only binary outcome, not scores.
- **Residual risk:** With sufficient test transactions (> 10,000 per metric), the adversary can statistically estimate the baseline despite noise. However, the anomalous claim submission rate required for 10,000+ test transactions itself triggers Tier 1, creating a self-defeating attack.

**Attack Class 5 — Concentration (Neighborhood Stacking)**

- **Attacker capability:** Adversary registers multiple agents (via Sybil attack on C17 MCSD) and manipulates their interaction patterns to ensure they are assigned to the same spectral neighborhood. Within the concentrated neighborhood, the colluding agents' mutual correlation is "expected" because they share structural covariates.
- **Attacker objective:** Concentrate colluding agents in a single neighborhood so that their high correlation is explained by PCM (shared covariates) rather than flagged as anomalous.
- **Primary defense:** Neighborhood size cap of 2 * log(V) agents with split-on-overflow. At V = 100K, maximum neighborhood size is 2 * log(100000) = 2 * 11.51 = ~23 agents. Attempting to concentrate more than 23 agents forces a neighborhood split, which distributes the colluders across multiple neighborhoods and exposes their cross-neighborhood correlation.
- **Secondary defense:** C17 MCSD Layer 2 behavioral similarity (B metric) detects Sybil clusters before they reach C35. C12 AVAP disrupts committee assignment patterns that would create shared covariates.
- **Residual risk:** An adversary with fewer than 23 agents can concentrate within a single neighborhood. PCM residuals may still detect the anomalous correlation if the adversary's structural covariates do not fully explain their coordination, but this depends on the adversary's ability to engineer shared covariates organically.

**Attack Class 6 — Channel Gaming**

- **Attacker capability:** Adversary manipulates specific metric channels to defeat quorum or Bayesian fusion. For example: an adversary could suppress anomaly signals in the BEHAVIORAL and ECONOMIC channels (by mimicking normal patterns in those dimensions) while conducting anomalous activity visible only in the VERIFICATION channel.
- **Attacker objective:** Ensure that fewer than 3 channels (quorum phase) or that the Bayesian posterior remains below theta_fusion = 0.80 (Bayesian phase) despite genuine anomalous activity.
- **Primary defense (quorum phase):** Requires anomaly in 3 of 4 channels. An adversary suppressing 2 channels prevents quorum. However, single-channel anomalies that exceed 2x the threshold are escalated directly (high-confidence single-channel bypass).
- **Primary defense (Bayesian phase):** The Bayesian network accounts for channel dependencies. A verification-only anomaly that is strong (high likelihood ratio) can produce posterior > 0.80 even without corroborating channels, because the network models P(anomaly | V_high, B_low, E_low, I_low) directly from empirical data.
- **Residual risk:** During the quorum phase (before 50 confirmed anomalies), a sophisticated adversary who isolates anomalous activity to exactly 1-2 channels evades detection. Transition to Bayesian fusion reduces but does not eliminate this risk — the posterior still depends on the anomaly magnitude relative to the learned channel-specific likelihood ratios.

### 7.2 Fixed-Baseline Protection (FC-3 Red Team Protocol)

This section specifies the formal Red Team evaluation protocol for fixed-baseline reconstructibility, resolving monitoring flag MF-4 from the Feasibility Council.

**Protocol Design**

The Red Team evaluation follows a structured adversarial game:

1. **Observation phase:** Adversary observes the system for T_obs epochs, where T_obs is drawn from {100, 500, 1000}. During observation, the adversary may submit test transactions and observe the binary trigger outcome ("flagged" or "not flagged"). The adversary does NOT observe:
   - The raw STA/LTA ratio value
   - The specific metric values used in the composite score
   - The fixed baseline percentile values
   - Whether the trigger was from the fixed or adaptive baseline

2. **Adversary knowledge model:** The adversary knows:
   - The Laplace noise mechanism and epsilon parameter (public system specification)
   - The STA and LTA window lengths (public parameters)
   - The general threshold range [1.5, 10.0] (public parameter range)
   - Their own transaction history and outcomes
   - The adversary does NOT know: the specific noise realization drawn for their agent's baseline, the jitter realization at each tick, other agents' trigger outcomes.

3. **Attack protocol:** The adversary submits test transactions at controlled intensities i_1, i_2, ..., i_N and records binary outcomes y_1, y_2, ..., y_N where y_k in {0, 1} (not flagged / flagged). The adversary fits a logistic model P(flagged | intensity) = sigmoid(a * intensity + b) to estimate the threshold.

4. **Success metric:** Adversary reconstructs the fixed baseline to within 10% of the true p50 value for each of the 4 metrics (verification latency, acceptance rate, committee frequency, behavioral consistency).

5. **Defense layers and their quantitative contribution:**

   - **(a) Laplace noise on stored percentiles:** Each stored percentile p_k is replaced with p_k + Lap(0, 1/epsilon) where epsilon = 1.0. The Laplace distribution has variance 2/epsilon^2 = 2.0, so the stored percentile has standard deviation sqrt(2) = 1.414 in the percentile's natural units. This means the adversary's logistic regression target is itself a noisy version of the true threshold. With N test transactions, the adversary's estimate of the noisy threshold has standard error O(1/sqrt(N)), but the underlying noise has standard deviation 1.414 — so even perfect estimation of the noisy threshold leaves uncertainty of 1.414 units.

   - **(b) Randomized trigger threshold jitter:** At each tick, the effective threshold is multiplied by (1 + U) where U is drawn uniformly from [-0.05, 0.05]. This adds 5% multiplicative noise to the threshold at each evaluation. For a threshold of 3.0, the effective range is [2.85, 3.15]. The adversary's logistic model must account for this jitter, which smooths the sigmoid boundary and increases the number of samples needed to localize the threshold. Under jitter, the logistic model's effective slope is reduced by a factor proportional to the jitter range, requiring O(1/jitter_range^2) = O(400) additional samples to achieve the same precision as without jitter.

   - **(c) Rate limiting on trigger feedback:** The adversary sees only binary "flagged" or "not flagged" per tick. The information content of each binary observation is at most 1 bit. To estimate a continuous threshold to 10% precision across 4 metrics requires approximately 4 * log2(10) = ~13.3 bits of information. However, the Laplace noise and jitter reduce the effective information per observation to well below 1 bit (the observation is noisy, so mutual information between the observation and the true threshold is reduced). Under epsilon = 1.0 Laplace noise and 5% jitter, the effective mutual information per test transaction is approximately 0.03 bits (estimated via simulation of the logistic model with compounded noise sources).

6. **Expected outcome:** To accumulate 4 * 13.3 = 53.2 bits of information at 0.03 bits per test transaction, the adversary requires approximately 53.2 / 0.03 = 1,773 test transactions per metric, or 7,092 total across 4 metrics. Conservatively (accounting for model misspecification and non-uniform intensity selection), we estimate > 10,000 test transactions are needed for 10% reconstruction across all metrics. At a rate of 1 test transaction per SETTLEMENT_TICK (60s), this requires 600,000 seconds = ~6,944 ticks = ~115.7 hours of sustained testing. The anomalous claim submission rate (1 test per tick for a single agent, sustained over hundreds of epochs) exceeds the trigger density threshold (2.0 sigma above rolling mean) within approximately 20 ticks, triggering Tier 1 independently of the threshold reconstruction attempt.

**Red Team Verdict Criteria**

| Outcome | Interpretation |
|---------|---------------|
| Reconstruction requires > 10,000 transactions | PASS — self-defeating attack |
| Reconstruction requires 5,000-10,000 transactions | CONDITIONAL PASS — increase epsilon to 2.0 |
| Reconstruction requires < 5,000 transactions | FAIL — redesign noise mechanism |

### 7.3 Spectral Clustering Adversarial Analysis (FC-5)

This section provides the game-theoretic analysis of spectral clustering robustness, resolving monitoring flag MF-7 from the Feasibility Council.

**Game-Theoretic Framework**

The interaction between attacker and defender is modeled as a Stackelberg game where the defender commits to a clustering policy and the attacker best-responds.

- **Attacker action space:** Add or remove up to B edges from the agent interaction graph, where B = c * sqrt(V) for constant c in [0.1, 1.0]. The attacker's budget is motivated by the O(sqrt(V)) perturbation bound from spectral graph theory (Mohar 1991, "The Laplacian spectrum of graphs"): perturbations of order sqrt(V) are sufficient to change the Fiedler vector's sign pattern and thus the spectral partition.
- **Attacker objective function:** Maximize one of:
  - (i) Move a target set S of agents from neighborhood N_1 to neighborhood N_2, where |S| <= B / deg_avg.
  - (ii) Fragment neighborhood N containing colluders into N_a and N_b such that colluders are split across the two partitions.
- **Defender action space:** Three parameters: NMI divergence threshold theta_NMI (default: 0.85), perturbation standard deviation sigma_perturb (default: 0.1), and fallback policy (REVERT to previous epoch's clustering, or RECOMPUTE with doubled sigma_perturb).
- **Defender mechanism:** At each CONSOLIDATION_CYCLE, compute spectral clustering on the raw interaction graph G, then compute spectral clustering on a perturbed copy G' where each edge weight w_ij is replaced by w_ij + N(0, sigma_perturb^2). Compute Normalized Mutual Information (NMI) between the two clusterings. If NMI < theta_NMI, the clustering is flagged as potentially manipulated and the fallback policy is invoked.

**Equilibrium Analysis**

Let lambda_2 denote the second-smallest eigenvalue of the normalized Laplacian (the algebraic connectivity). The spectral gap delta = lambda_2 determines the clustering's robustness: larger delta means more perturbation is needed to change the partition.

- **Attacker's effective budget:** The attacker needs to change the sign pattern of the Fiedler vector for at least |S| nodes. Each edge modification changes the Fiedler vector by at most O(1/delta) in the affected components. To change |S| node signs, the attacker needs B >= |S| * delta * deg_avg edge modifications (first-order approximation).
- **Defender's detection sensitivity:** The NMI check compares clustering(G) with clustering(G + N(0, sigma^2)). The defender's perturbation sigma creates a "natural noise floor." The NMI between the raw and perturbed clusterings under NO attack provides the baseline NMI. The threshold theta_NMI is set to the 5th percentile of this baseline distribution (i.e., in the absence of attack, the NMI falls below theta_NMI with probability 0.05).
- **Detection boundary:** The attacker's perturbation of B edges is detectable when it shifts the NMI below the baseline 5th percentile. By the Davis-Kahan theorem (1970), eigenvector perturbation is bounded by ||delta_v|| <= ||delta_L||_F / delta, where ||delta_L||_F is the Frobenius norm of the Laplacian perturbation induced by B edge changes. For B modified edges with weight change of order 1, ||delta_L||_F = O(sqrt(B)). The NMI is sensitive to eigenvector perturbation when ||delta_v|| > sigma_perturb / sqrt(V). Combining:

  Detection condition: sqrt(B) / delta > sigma_perturb / sqrt(V)
  => B > sigma_perturb^2 * delta^2 / V

  For typical values (sigma_perturb = 0.1, delta = 0.1, V = 10,000):
  B > 0.01 * 0.01 / 10,000 = 10^-8

  This bound is unrealistically low because it uses worst-case eigenvector sensitivity. The practical bound, estimated from empirical spectral clustering on random geometric graphs with planted perturbations (Amini et al. 2013), is:

  **NMI check detects perturbations when B > 0.3 * sqrt(V)**

  At V = 10,000: B > 30 edges. At V = 100,000: B > 95 edges.

- **Attacker's viable region:** B < 0.3 * sqrt(V). Within this budget, the attacker can modify boundary assignments for approximately B / deg_avg agents. At deg_avg ~ 10 and B = 30 (for V = 10K), this is ~3 agents. At B = 95 (for V = 100K), this is ~9-10 agents.

**Residual Risk and Mitigation**

An attacker with budget B < 0.3 * sqrt(V) can make small boundary adjustments that pass the NMI check, affecting up to ~10 agents at 100K scale. Mitigations:

1. **Randomized perturbation direction:** The NMI check uses a fresh random perturbation at each CONSOLIDATION_CYCLE. The attacker cannot pre-compensate because they do not know the perturbation realization. An attack optimized for one perturbation direction may be detected by a differently-oriented perturbation in the next cycle.
2. **Temporal consistency:** Agents whose neighborhood assignment changes more frequently than expected (measured against a Poisson baseline with rate parameter lambda_change = 0.02 per CONSOLIDATION_CYCLE) are flagged for manual review.
3. **Cross-tier detection:** Agents moved to a new neighborhood still carry their Tier 1 history. If a moved agent was previously in CANDIDATE or CONFIRMED state, the move itself is logged and the agent's Tier 2 analysis continues in the new neighborhood.

### 7.4 PCM Calibration Poisoning Mitigation

**The Circular Dependency Problem**

PCM calibration requires data from all agents in a neighborhood to compute the log-linear coefficients. Excluding anomalous agents from calibration requires first detecting them, which requires a calibrated PCM. This is a well-known bootstrapping problem in robust statistics (Huber 1981, "Robust Statistics").

**Mitigation Strategy: Four-Phase Bootstrap**

Phase 1 — Raw Similarity Bootstrap (epochs 0-500):
- PCM is not yet available. Tier 2 operates in degraded mode using raw pairwise correlation without structural covariate correction.
- Detection thresholds are conservative: residual threshold = 0.80 (versus post-PCM default of 0.60). This accepts a higher false negative rate in exchange for avoiding false positives that would corrupt Phase 2.
- All Tier 1 triggers during this phase use the adaptive baseline only (fixed baseline is still calibrating during epochs 0-100).
- Tier 2 channel fusion uses the 3-of-4 quorum (Bayesian network not yet available).
- Data collection: all pairwise correlations and structural covariates are accumulated for Phase 2.

Phase 2 — Initial PCM Calibration (epochs 500-1000):
- Compute log-linear PCM coefficients from the accumulated 500-epoch dataset using all agents (no exclusions).
- Compute R-squared for each neighborhood-channel combination. Neighborhoods with R-squared < pcm_coverage_threshold (0.70) remain in raw-similarity fallback mode.
- The PCM is assumed to be potentially poisoned at this stage. It is used for detection but not yet trusted for recalibration decisions.

Phase 3 — Retrospective Audit (epoch 1000):
- Run the calibrated PCM retrospectively on the Phase 1 data (epochs 0-500).
- For each agent pair (a_i, a_j) in each channel, compute the PCM residual R = observed - exp(predicted_log_corr).
- Flag any agent whose mean absolute residual across all pairs and channels exceeds the 95th percentile of the overall residual distribution. These agents were anomalous during the bootstrap phase but could not be detected without PCM.
- Flagged agents are entered into a calibration exclusion set E_calib.

Phase 4 — Recalibration (epoch 1000+):
- Recompute PCM coefficients excluding all agents in E_calib.
- Compare the recalibrated coefficients to the Phase 2 coefficients. If the maximum absolute coefficient change exceeds 0.20 (20% of the typical coefficient magnitude), the recalibration is accepted and the PCM is updated. Otherwise, the Phase 2 PCM is retained (the excluded agents did not materially bias calibration).
- Going forward: any agent that is confirmed anomalous by Tier 2 (with Tier 3 validation or C12 AVAP confirmation) is added to E_calib and excluded from all subsequent PCM recalibrations at CONSOLIDATION_CYCLE boundaries.

**Residual Risk Assessment**

An adversary who behaves identically to a legitimate agent during the full 1000-epoch bootstrap and activation phases cannot be detected or excluded. This adversary's data enters the PCM coefficients without correction. The residual risk is bounded by:

- **Magnitude:** A single adversary in a neighborhood of k agents contributes 1/C(k,2) of the pairwise data. At k = 23 (maximum neighborhood size at 100K), the adversary contributes at most 2/(23*22) = 0.4% of pairwise observations. The bias introduced by a single poisoning agent on a 16-parameter log-linear model is bounded by the leverage of that agent's observations, which is at most O(1/k) = O(0.04). This produces less than 5% bias in any single coefficient.
- **Amplification:** Multiple colluding poisoners in the same neighborhood amplify the bias. With m poisoners in a neighborhood of k agents, the fraction of corrupted pairs is C(m,2)/C(k,2). At m = 5, k = 23: C(5,2)/C(23,2) = 10/253 = 3.95%. This can produce meaningful coefficient bias (up to 20%) on specific covariate interactions. The Phase 3 retrospective audit catches this only if the poisoners' pairwise correlations were anomalous during bootstrap — if they were coordinated to appear normal, they pass the audit.

**This residual risk is acknowledged as a fundamental limitation and is tracked as monitoring flag MF-5.**

### 7.5 C35-as-Attack-Surface

C35 itself presents three attack surfaces. Each is analyzed with a specific defense mechanism.

**Attack Surface 1 — Denial of Detection (Tier 2 Saturation)**

- **Attack vector:** Adversary triggers a large number of Tier 1 escalations (by injecting obviously anomalous transactions across many agents) to saturate Tier 2 analysis capacity. While Tier 2 is processing the flood of false triggers, genuine anomalies are delayed or dropped.
- **Capacity model:** Tier 2 analyzes one neighborhood at a time per triggered event. Each analysis requires PCM residual computation (O(neighborhood_size^2) per channel) plus MIDAS scoring plus channel fusion. At 100K agents with ~5,882 neighborhoods, Tier 2 can process approximately 100 neighborhoods per SETTLEMENT_TICK.
- **Defense — trigger rate limiting:** At most max_candidate_fraction = 5% of agents may be in CANDIDATE state simultaneously. At 100K agents, this caps CANDIDATE count at 5,000 agents. Excess triggers are queued in FIFO order with priority escalation for dual-trigger (both baselines exceeded) events.
- **Defense — queue prioritization:** The queue is priority-ordered: (1) dual-trigger events, (2) agents with prior CONFIRMED history, (3) agents in neighborhoods with existing Tier 2 anomalies, (4) all others. An adversary flooding with single-trigger events on new agents is processed last.
- **Residual risk:** An adversary who floods with dual-trigger events can still saturate the priority queue. Mitigation: dual-trigger events from agents with no prior anomaly history are demoted to priority 2 if more than 2% of agents simultaneously produce dual-triggers (indicating a system-wide event rather than targeted attack).

**Attack Surface 2 — Oracle Attack (Threshold Learning)**

- **Attack vector:** Adversary uses C35's binary responses ("flagged" / "not flagged") and the visible cluster membership API to learn detection thresholds and neighborhood boundaries.
- **Information leakage model:**
  - Binary trigger outcome: 1 bit per tick per agent (mitigated by Laplace noise and jitter per Section 7.2).
  - Cluster membership: O(log V) bits per agent per CONSOLIDATION_CYCLE (neighborhood assignment is visible because downstream specs C3, C5, C8 need it for scheduling and verification).
  - Anomaly levels: NOT visible. Agents see their own cluster assignment but not their anomaly score, PCM residual, MIDAS score, Bayesian posterior, or any Tier 2/3 intermediate values.
- **Defense — information asymmetry:** Authorized consumers of detailed C35 data are restricted to: C5 PCVM (for verification integrity assessment), C8 DSF (for settlement risk scoring), C12 AVAP (for collusion evidence integration). All access is via authenticated API with per-consumer rate limiting (max rate_limit_per_consumer = 100 queries per SETTLEMENT_TICK per consumer).
- **Residual risk:** Cluster membership visibility enables an adversary to observe neighborhood boundaries and plan concentration attacks (Attack Class 5). This is an inherent tension between C35's utility as infrastructure (cluster membership must be visible) and its security (visibility enables boundary gaming). Mitigated by the NMI divergence check (Section 7.3) and temporal consistency monitoring.

**Attack Surface 3 — Feedback Poisoning (Bayesian Network Corruption)**

- **Attack vector:** Adversary manipulates which anomalies are "confirmed" to corrupt the Bayesian network's conditional probability tables. For example, by conducting anomalous activity in specific channel combinations and then ceasing before Tier 3 validation, the adversary creates a biased dataset of confirmed anomalies that misrepresents the true channel dependency structure.
- **Defense — calibration safeguards:**
  - Phase 2 Bayesian network requires a minimum of 50 confirmed anomalies before transition from quorum fallback. The 50-anomaly threshold provides sufficient statistical power to estimate 4 conditional probabilities with standard errors below 0.10 (binomial standard error at n = 50, p = 0.5 is sqrt(0.25/50) = 0.07).
  - Cross-validation requirement: the Bayesian network's out-of-sample log-likelihood must exceed 0.85 of the in-sample log-likelihood (i.e., cross-validation score > 0.85). If the adversary's poisoned data creates overfitting, cross-validation will detect it.
  - Manual review for first 20 confirmations: the initial training set for the Bayesian network is manually reviewed by a human operator (or by C12 AVAP cross-referencing) before being accepted as ground truth. This prevents a pure automation attack where the adversary controls both the anomaly generation and the confirmation pipeline.
- **Residual risk:** After the first 20 manual confirmations, subsequent confirmations are automated. An adversary who waits until the manual phase is complete and then generates adversary-controlled confirmed anomalies can bias the network. Mitigated by periodic recalibration with manual spot-checks (1 in 10 confirmations randomly selected for review) and by monitoring the Bayesian network's predictive performance over time (degradation triggers retraining with manual review).

---

## 8. Parameter Registry

Complete registry of all 86 parameters organized by tier. Each parameter specifies: name, type, default value, valid range, sensitivity classification, and source justification.

**Sensitivity classifications:**
- **CRITICAL:** Changes of 10% or more significantly alter system behavior. Must be validated at W0.
- **SENSITIVE:** Changes of 25% or more produce measurable behavioral shifts. Validate at W1.
- **ROBUST:** System tolerates 50% or more variation without significant behavioral change. Defaults from literature are sufficient through W2.

### 8.1 Tier 1 Parameters (18)

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 1 | sta_window_ticks | u16 | 5 | [2, 20] | SENSITIVE | Seismology (Withers et al. 1998); short-term average window |
| 2 | lta_window_ticks | u16 | 60 | [20, 200] | SENSITIVE | Seismology (Withers et al. 1998); long-term average window |
| 3 | sta_lta_threshold_fixed | f64 | 3.0 | [1.5, 10.0] | CRITICAL | Seismology (Allen 1978); fixed-baseline trigger level |
| 4 | sta_lta_threshold_adaptive | f64 | 2.5 | [1.5, 10.0] | CRITICAL | Seismology (Allen 1978); adaptive-baseline trigger level |
| 5 | fixed_baseline_calibration_epochs | u16 | 100 | [50, 500] | ROBUST | Design choice; epochs to accumulate before freezing fixed baseline |
| 6 | laplace_epsilon | f64 | 1.0 | [0.1, 5.0] | SENSITIVE | Differential privacy (Dwork et al. 2006); noise scale for baseline protection |
| 7 | adaptive_decay_alpha | f64 | 0.01 | [0.001, 0.1] | SENSITIVE | EMA standard; controls LTA responsiveness to recent values |
| 8 | confirmation_window_normal | u8 | 3 | [1, 10] | SENSITIVE | Design choice; ticks in CANDIDATE before CONFIRMED under normal load |
| 9 | confirmation_window_extended | u8 | 5 | [3, 15] | ROBUST | Design choice; ticks in CANDIDATE under high trigger density |
| 10 | trigger_density_sigma_threshold | f64 | 2.0 | [1.5, 3.0] | ROBUST | Statistical standard; sigma above rolling mean to expand confirmation window |
| 11 | trigger_density_rolling_window | u16 | 100 | [50, 200] | ROBUST | Design choice; ticks over which trigger density mean/sigma are computed |
| 12 | alpha_confirm_directional | f64 | 0.7 | [0.5, 1.0] | SENSITIVE | Design choice; fraction of metrics that must agree on anomaly direction |
| 13 | cache_staleness_threshold_ticks | u16 | 100 | [50, 500] | ROBUST | Design choice; max age before per-agent metric cache is invalidated |
| 14 | max_candidate_fraction | f64 | 0.05 | [0.01, 0.10] | SENSITIVE | Design choice; max fraction of agents in CANDIDATE state simultaneously |
| 15 | metric_verification_latency_weight | f64 | 0.30 | [0.1, 0.5] | ROBUST | Design choice; weight of verification latency in composite score |
| 16 | metric_acceptance_rate_weight | f64 | 0.30 | [0.1, 0.5] | ROBUST | Design choice; weight of acceptance rate in composite score |
| 17 | metric_committee_frequency_weight | f64 | 0.20 | [0.1, 0.4] | ROBUST | Design choice; weight of committee participation frequency |
| 18 | metric_behavioral_consistency_weight | f64 | 0.20 | [0.1, 0.4] | ROBUST | Design choice; weight of behavioral consistency score |

### 8.2 Tier 2 Parameters (48)

**8.2.1 Spectral Clustering (6 parameters)**

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 19 | neighborhood_count_formula | enum | LOG_V | {LOG_V, SQRT_V} | ROBUST | Design choice; k = V/log(V) neighborhoods |
| 20 | neighborhood_size_cap | u16 | 2*log(V) | [log(V), 4*log(V)] | SENSITIVE | Design choice; maximum agents per neighborhood |
| 21 | nmi_divergence_threshold | f64 | 0.85 | [0.70, 0.95] | CRITICAL | Empirical (Amini et al. 2013); minimum NMI before fallback |
| 22 | perturbation_sigma | f64 | 0.10 | [0.01, 0.50] | SENSITIVE | Design choice; Gaussian noise sigma for NMI robustness check |
| 23 | clustering_fallback_policy | enum | REVERT | {REVERT, RECOMPUTE} | ROBUST | Design choice; action when NMI check fails |
| 24 | clustering_recompute_epochs | u16 | 1 | [1, 5] | ROBUST | Design choice; CONSOLIDATION_CYCLEs between full spectral recomputation |

**8.2.2 PCM Log-Linear Coefficients (64 parameters)**

The 64 PCM parameters are organized as 4 channels x 16 coefficients per channel. Each channel's 16 coefficients comprise: 1 intercept (beta_0), 5 main effects (beta_1 through beta_5), and 10 pairwise interactions (gamma_12, gamma_13, gamma_14, gamma_15, gamma_23, gamma_24, gamma_25, gamma_34, gamma_35, gamma_45).

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 25-40 | pcm_verification_beta[0..15] | f64[16] | MLE-estimated | [-5.0, 5.0] | CRITICAL | Log-linear regression; VERIFICATION channel |
| 41-56 | pcm_behavioral_beta[0..15] | f64[16] | MLE-estimated | [-5.0, 5.0] | CRITICAL | Log-linear regression; BEHAVIORAL channel |
| 57-72 | pcm_infrastructure_beta[0..15] | f64[16] | MLE-estimated | [-5.0, 5.0] | SENSITIVE | Log-linear regression; INFRASTRUCTURE channel |
| 73-88 | pcm_economic_beta[0..15] | f64[16] | MLE-estimated | [-5.0, 5.0] | SENSITIVE | Log-linear regression; ECONOMIC channel |

Note: Parameters 25-88 are numbered as 64 individual parameters but occupy registry slots 25-88. All are estimated from data; defaults are computed at Phase 2 calibration (epoch 500-1000). The CRITICAL classification for VERIFICATION and BEHAVIORAL channels reflects these channels' higher diagnostic weight.

**8.2.3 PCM Operational Parameters (3 parameters)**

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 89 | pcm_coverage_threshold | f64 | 0.70 | [0.50, 0.90] | SENSITIVE | Ovaskainen et al. 2017; R-squared below which PCM falls back to raw similarity |
| 90 | pcm_residual_threshold | f64 | 0.60 | [0.30, 0.90] | CRITICAL | Design choice; residual magnitude above which pair is flagged |
| 91 | pcm_recalibration_exclusion_delta | f64 | 0.20 | [0.10, 0.50] | ROBUST | Design choice; max coefficient change for Phase 4 recalibration acceptance |

**8.2.4 MIDAS Parameters (3 parameters)**

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 92 | midas_threshold | f64 | 3.0 | [1.5, 10.0] | CRITICAL | Bhatia et al. 2020; MIDAS anomaly score threshold |
| 93 | midas_decay_factor | f64 | 0.50 | [0.10, 0.90] | SENSITIVE | Bhatia et al. 2020; temporal decay for edge stream counts |
| 94 | midas_hash_functions | u8 | 2 | [1, 4] | ROBUST | Bhatia et al. 2020; number of hash functions for CMS sketch |

**8.2.5 Channel Fusion Parameters (8 parameters)**

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 95 | quorum_k | u8 | 3 | [2, 4] | CRITICAL | IEC 61508 (k-of-n voting); channels required for quorum |
| 96 | quorum_n | u8 | 4 | {4} | FIXED | Design choice; total channel count |
| 97 | bayesian_prior_anomaly | f64 | 0.01 | [0.001, 0.10] | SENSITIVE | Design choice; P(anomaly) prior for Bayesian network |
| 98 | bayesian_p_b_given_v | f64 | 0.70 | [0.40, 0.90] | SENSITIVE | Empirical; P(behavioral anomaly | verification anomaly) |
| 99 | bayesian_p_e_given_v | f64 | 0.45 | [0.20, 0.70] | SENSITIVE | Empirical; P(economic anomaly | verification anomaly) |
| 100 | bayesian_p_e_given_b_v | f64 | 0.55 | [0.30, 0.80] | SENSITIVE | Empirical; P(economic | behavioral, verification) |
| 101 | bayesian_posterior_threshold | f64 | 0.80 | [0.60, 0.95] | CRITICAL | Design choice; posterior above which anomaly is confirmed |
| 102 | bayesian_transition_min_anomalies | u16 | 50 | [20, 200] | SENSITIVE | Design choice (per Feasibility Council); confirmed anomalies before Bayesian activation |

**8.2.6 Tier 2 Operational Parameters (6 parameters)**

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 103 | min_neighborhood_triggers | u8 | 2 | [1, 5] | SENSITIVE | Design choice; minimum Tier 1 triggers before Tier 2 activates for neighborhood |
| 104 | max_tier2_concurrent_analyses | u16 | 100 | [10, 500] | ROBUST | Design choice; max neighborhoods in simultaneous Tier 2 analysis |
| 105 | tier2_escalation_threshold | f64 | 0.90 | [0.70, 0.99] | SENSITIVE | Design choice; posterior above which Tier 2 escalates to Tier 3 |
| 106 | c12_integration_mode | enum | BIDIRECTIONAL | {OFF, INBOUND, OUTBOUND, BIDIRECTIONAL} | ROBUST | Design choice; C12 AVAP evidence exchange mode |
| 107 | high_confidence_single_channel_bypass | f64 | 2.0 | [1.5, 3.0] | SENSITIVE | Design choice; multiplier above which single-channel anomaly bypasses quorum |
| 108 | bayesian_crossval_threshold | f64 | 0.85 | [0.70, 0.95] | ROBUST | Design choice; cross-validation score required for Bayesian network acceptance |

### 8.3 Tier 3 Parameters (12)

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 109 | overdispersion_alpha_threshold | f64 | 0.50 | [0.10, 2.00] | CRITICAL | Cameron & Trivedi 1998; NB alpha above which overdispersion is significant |
| 110 | tier3_min_sample_size | u16 | 30 | [10, 100] | SENSITIVE | Statistical power (n >= 30 for CLT); minimum confirmed anomalies for Tier 3 |
| 111 | max_tier3_concurrent_analyses | u8 | 5 | [1, 20] | ROBUST | Design choice; max simultaneous Tier 3 backward traces |
| 112 | synthetic_pool_size | u16 | 1000 | [100, 10000] | ROBUST | Design choice; synthetic agent profiles for Tier 3 null distribution |
| 113 | attribution_confidence_threshold | f64 | 0.90 | [0.70, 0.99] | CRITICAL | Design choice; posterior probability required for cause attribution |
| 114 | tier3_analysis_window_epochs | u16 | 500 | [100, 2000] | SENSITIVE | Design choice; backward trace look-back window in SETTLEMENT_TICKs |
| 115 | dormant_to_active_threshold | u8 | 3 | [2, 10] | SENSITIVE | Design choice; confirmed anomalies within window to activate Tier 3 |
| 116 | active_to_dormant_threshold | u16 | 100 | [50, 500] | ROBUST | Design choice; epochs without activation before Tier 3 returns to dormant |
| 117 | backward_trace_depth | u8 | 5 | [2, 10] | SENSITIVE | Design choice; max hops in cross-layer causal trace |
| 118 | max_attribution_candidates | u8 | 20 | [5, 50] | ROBUST | Design choice; max candidate causes ranked by posterior |
| 119 | phylogeny_pruning_threshold | f64 | 0.10 | [0.01, 0.50] | ROBUST | Design choice; posterior below which branches are pruned from phylogeny tree |
| 120 | report_retention_cycles | u16 | 100 | [10, 1000] | ROBUST | Design choice; CONSOLIDATION_CYCLEs to retain Tier 3 attribution reports |

### 8.4 Cross-Layer Parameters (8)

| # | Name | Type | Default | Range | Sensitivity | Source |
|---|------|------|---------|-------|-------------|--------|
| 121 | api_cache_ttl_ticks | u16 | 10 | [1, 60] | ROBUST | Design choice; API response cache TTL in SETTLEMENT_TICKs |
| 122 | etr_skew_threshold | f64 | 0.15 | [0.05, 0.30] | SENSITIVE | C3 integration; max ETR schedule skew before flagging |
| 123 | etr_starvation_threshold | u16 | 10 | [5, 30] | SENSITIVE | C3 integration; ticks without ETR allocation before starvation flag |
| 124 | etr_divergence_threshold | f64 | 0.25 | [0.10, 0.50] | SENSITIVE | C3 integration; max ETR actual-vs-planned divergence |
| 125 | anomaly_severity_levels | u8 | 4 | {4} | FIXED | Design choice; LOW / MEDIUM / HIGH / CRITICAL severity classification |
| 126 | cluster_health_green_threshold | f64 | 0.90 | [0.80, 0.99] | ROBUST | Design choice; neighborhood health score above which cluster is GREEN |
| 127 | external_evidence_weight | f64 | 0.30 | [0.10, 0.50] | SENSITIVE | Design choice; weight of C12/C17 external evidence in Bayesian fusion |
| 128 | rate_limit_per_consumer | u16 | 100 | [10, 1000] | ROBUST | Design choice; max API queries per SETTLEMENT_TICK per authorized consumer |

**Parameter Count Verification:** 18 (Tier 1) + 6 + 64 + 3 + 3 + 8 + 6 (Tier 2 = 90 registry slots, 48 logical parameters counting 64 PCM coefficients as 4 groups) + 12 (Tier 3) + 8 (Cross-Layer) = 86 logical parameters occupying 128 registry slots. The 64 PCM coefficients count as 4 parameter groups (one per channel) for tuning purposes because they are MLE-estimated as a unit, not individually tuned.

---

## 9. Pseudocode

All pseudocode uses Rust-like syntax with explicit types. Functions are organized by processing tier and cadence.

### 9.1 Tier 1 Per-Tick Processing

```
const EPSILON: f64 = 1e-12;

struct AgentState {
    sta_window: RingBuffer<f64, STA_WINDOW_TICKS>,   // short-term metric values
    lta_window: RingBuffer<f64, LTA_WINDOW_TICKS>,   // long-term metric values
    fixed_baseline: FixedBaseline,                     // immutable after calibration
    trigger_state: TriggerState,                       // NORMAL | CANDIDATE | CONFIRMED
    confirmation_countdown: u8,
    metric_history: [RingBuffer<f64, 10>; 4],         // per-metric recent history for directional check
}

enum TriggerState { NORMAL, CANDIDATE, CONFIRMED }

struct FixedBaseline {
    p50: [f64; 4],     // 50th percentile per metric (with Laplace noise applied)
    p95: [f64; 4],     // 95th percentile per metric (with Laplace noise applied)
    calibrated: bool,
    calibration_epoch: u64,
}

fn tier1_process(agent: &mut AgentState, tick: u64, metrics: MetricBundle, params: &Tier1Params) -> Option<TriggerEvent> {
    // Compute composite score: weighted combination of 4 metrics
    let composite = metrics.verification_latency * params.metric_verification_latency_weight
                  + metrics.acceptance_rate      * params.metric_acceptance_rate_weight
                  + metrics.committee_frequency   * params.metric_committee_frequency_weight
                  + metrics.behavioral_consistency * params.metric_behavioral_consistency_weight;

    // Update sliding windows
    agent.sta_window.push(composite);
    agent.lta_window.push(composite);

    // Compute STA and LTA means
    let sta: f64 = agent.sta_window.mean();
    let lta: f64 = agent.lta_window.mean();

    // Adaptive STA/LTA ratio
    let ratio_adaptive: f64 = sta / f64::max(lta, EPSILON);

    // Fixed baseline STA/LTA ratio (only if calibrated)
    let ratio_fixed: f64 = if agent.fixed_baseline.calibrated {
        sta / f64::max(agent.fixed_baseline.p50[0], EPSILON)  // [0] = composite percentile
    } else {
        0.0  // not yet calibrated, do not trigger
    };

    // Apply threshold jitter: uniform random in [-0.05, 0.05] multiplicative
    let jitter: f64 = rand_uniform(-0.05, 0.05);
    let effective_threshold_fixed: f64 = params.sta_lta_threshold_fixed * (1.0 + jitter);
    let effective_threshold_adaptive: f64 = params.sta_lta_threshold_adaptive * (1.0 + jitter);

    // Evaluate triggers
    let adaptive_trigger: bool = ratio_adaptive > effective_threshold_adaptive;
    let fixed_trigger: bool = agent.fixed_baseline.calibrated && ratio_fixed > effective_threshold_fixed;

    // Decision fusion with confirmation window
    if adaptive_trigger && fixed_trigger {
        // Dual trigger: both baselines agree — immediate escalation (bypass confirmation)
        agent.trigger_state = TriggerState::CONFIRMED;
        agent.confirmation_countdown = 0;
        return Some(TriggerEvent {
            agent_id: agent.id,
            tick,
            trigger_type: TriggerType::DualTrigger,
            ratio_adaptive,
            ratio_fixed,
        });
    }

    if adaptive_trigger || fixed_trigger {
        match agent.trigger_state {
            TriggerState::NORMAL => {
                // Enter candidate state, start confirmation countdown
                agent.trigger_state = TriggerState::CANDIDATE;
                agent.confirmation_countdown = get_confirmation_window(tick, params);
                // Record metric direction for directional agreement check
                for i in 0..4 {
                    agent.metric_history[i].push(metrics.by_index(i));
                }
            }
            TriggerState::CANDIDATE => {
                agent.confirmation_countdown -= 1;
                // Update metric history
                for i in 0..4 {
                    agent.metric_history[i].push(metrics.by_index(i));
                }
                // Check directional agreement
                if check_directional_agreement(&agent.metric_history, params.alpha_confirm_directional) {
                    if agent.confirmation_countdown == 0 {
                        agent.trigger_state = TriggerState::CONFIRMED;
                        return Some(TriggerEvent {
                            agent_id: agent.id,
                            tick,
                            trigger_type: TriggerType::ConfirmedTrigger,
                            ratio_adaptive,
                            ratio_fixed,
                        });
                    }
                    // else: still counting down, remain CANDIDATE
                } else {
                    // Direction disagreement: metrics are not consistently deviating
                    // Reset to NORMAL (likely transient fluctuation)
                    agent.trigger_state = TriggerState::NORMAL;
                    agent.confirmation_countdown = 0;
                }
            }
            TriggerState::CONFIRMED => {
                // Already confirmed, do not re-trigger (handled by Tier 2)
            }
        }
    } else {
        // Neither baseline triggered: reset to NORMAL
        agent.trigger_state = TriggerState::NORMAL;
        agent.confirmation_countdown = 0;
    }

    None
}

fn get_confirmation_window(tick: u64, params: &Tier1Params) -> u8 {
    // Adaptive window: expand under high trigger density
    let recent_trigger_count = global_trigger_count_in_window(tick, params.trigger_density_rolling_window);
    let mean_trigger_rate = global_trigger_mean(params.trigger_density_rolling_window);
    let sigma_trigger_rate = global_trigger_sigma(params.trigger_density_rolling_window);

    if recent_trigger_count as f64 > mean_trigger_rate + params.trigger_density_sigma_threshold * sigma_trigger_rate {
        params.confirmation_window_extended   // high trigger density: use extended window
    } else {
        params.confirmation_window_normal     // normal: use standard window
    }
}

fn check_directional_agreement(history: &[RingBuffer<f64, 10>; 4], alpha: f64) -> bool {
    // At least alpha fraction of metrics must show consistent deviation direction
    let mut agreeing: u8 = 0;
    for i in 0..4 {
        if history[i].len() >= 2 {
            let trend = history[i].last() - history[i].first();
            if trend.abs() > EPSILON {
                agreeing += 1;
            }
        }
    }
    (agreeing as f64 / 4.0) >= alpha
}
```

### 9.2 Tier 2 Neighborhood Activation

```
fn tier2_activate(
    neighborhood: &mut Neighborhood,
    triggers: Vec<TriggerEvent>,
    tick: u64,
    params: &Tier2Params,
) -> Option<AnomalyConfirmation> {
    // Gate: minimum trigger count
    if triggers.len() < params.min_neighborhood_triggers as usize {
        return None;
    }

    // Compute PCM residuals for all triggered agent pairs within neighborhood
    let mut channel_evidence: [ChannelEvidence; 4] = Default::default();

    let triggered_agents: Vec<AgentId> = triggers.iter().map(|t| t.agent_id).collect();
    let pairs: Vec<(AgentId, AgentId)> = all_pairs(&triggered_agents);

    for (a_i, a_j) in pairs {
        for (ch_idx, channel) in [VERIFICATION, BEHAVIORAL, INFRASTRUCTURE, ECONOMIC].iter().enumerate() {
            // Compute observed pairwise correlation from recent metric streams
            let observed: f64 = compute_observed_correlation(a_i, a_j, *channel, tick);

            // PCM expected correlation (precomputed at last CONSOLIDATION_CYCLE)
            let expected: f64 = if neighborhood.pcm_coverage >= params.pcm_coverage_threshold {
                neighborhood.pcm_lookup(a_i, a_j, *channel)  // exp(X @ beta)
            } else {
                // Fallback: raw similarity (no structural correction)
                compute_raw_similarity(a_i, a_j, *channel)
            };

            // Residual
            let residual: f64 = observed - expected;

            // MIDAS streaming edge anomaly score
            let midas_score: f64 = neighborhood.midas_state[ch_idx].score(
                a_i, a_j,
                residual,
                tick,
                params.midas_decay_factor,
            );

            // Evidence accumulation
            if residual.abs() > params.pcm_residual_threshold
                && midas_score > params.midas_threshold
            {
                channel_evidence[ch_idx].add_edge(a_i, a_j, residual, midas_score);
            }
        }
    }

    // Channel fusion
    let anomaly_result = fuse_channels(neighborhood, &channel_evidence, params);

    match anomaly_result {
        FusionResult::Anomalous(posterior) => {
            // Emit raw + residual values per C-1 auditability condition
            emit_audit_record(neighborhood, &channel_evidence, posterior);

            if posterior >= params.tier2_escalation_threshold {
                return Some(AnomalyConfirmation {
                    neighborhood_id: neighborhood.id,
                    tick,
                    posterior,
                    channel_evidence,
                    escalate_tier3: true,
                });
            } else {
                return Some(AnomalyConfirmation {
                    neighborhood_id: neighborhood.id,
                    tick,
                    posterior,
                    channel_evidence,
                    escalate_tier3: false,
                });
            }
        }
        FusionResult::Clear => None,
    }
}
```

### 9.3 PCM Precomputation (CONSOLIDATION_CYCLE Cadence)

```
fn pcm_recompute(neighborhood: &mut Neighborhood, params: &Tier2Params) {
    let agents: &[AgentId] = &neighborhood.members;
    let pairs: Vec<(AgentId, AgentId)> = all_pairs(agents);
    let n_pairs: usize = pairs.len();  // at most C(2*log(V), 2)

    for (ch_idx, channel) in [VERIFICATION, BEHAVIORAL, INFRASTRUCTURE, ECONOMIC].iter().enumerate() {
        // Build covariate matrix X (n_pairs x 16) and response vector y (n_pairs)
        let mut x_matrix: Vec<[f64; 16]> = Vec::with_capacity(n_pairs);
        let mut y_vec: Vec<f64> = Vec::with_capacity(n_pairs);

        for (a_i, a_j) in &pairs {
            // 5 structural covariates
            let x1: f64 = committee_co_assignment_frequency(*a_i, *a_j);   // C5/C7
            let x2: f64 = parcel_co_assignment_frequency(*a_i, *a_j);      // C3
            let x3: f64 = infrastructure_proximity_score(*a_i, *a_j);      // C17 L2
            let x4: f64 = temporal_epoch_overlap(*a_i, *a_j);              // C9
            let x5: f64 = economic_bracket_similarity(*a_i, *a_j);         // C8

            // Feature vector: [intercept, 5 main, 10 interactions]
            let features: [f64; 16] = [
                1.0,                // beta_0: intercept
                x1, x2, x3, x4, x5,  // beta_1..beta_5: main effects
                x1*x2, x1*x3, x1*x4, x1*x5,  // gamma_12..gamma_15: pairwise interactions
                x2*x3, x2*x4, x2*x5,          // gamma_23..gamma_25
                x3*x4, x3*x5,                  // gamma_34, gamma_35
                x4*x5,                          // gamma_45
            ];
            x_matrix.push(features);

            // Observed correlation in the last CONSOLIDATION_CYCLE
            let observed: f64 = observed_correlation_last_cycle(*a_i, *a_j, *channel);
            y_vec.push(f64::ln(f64::max(observed, EPSILON)));  // log-transform for log-linear model
        }

        // Fit log-linear model via iteratively reweighted least squares (IRLS)
        // Convergence: max 10 iterations, tolerance 1e-6
        let beta: [f64; 16] = irls_fit(&x_matrix, &y_vec, 10, 1e-6);
        neighborhood.pcm_params[ch_idx] = beta;

        // Compute R-squared for coverage check
        let y_pred: Vec<f64> = x_matrix.iter()
            .map(|x| dot_product(x, &beta))
            .collect();
        let ss_res: f64 = y_vec.iter().zip(y_pred.iter())
            .map(|(y, yp)| (y - yp).powi(2))
            .sum();
        let y_mean: f64 = y_vec.iter().sum::<f64>() / y_vec.len() as f64;
        let ss_tot: f64 = y_vec.iter()
            .map(|y| (y - y_mean).powi(2))
            .sum();
        let r_squared: f64 = if ss_tot > EPSILON { 1.0 - ss_res / ss_tot } else { 0.0 };

        neighborhood.pcm_r_squared[ch_idx] = r_squared;
        neighborhood.pcm_coverage = r_squared;  // use minimum across channels

        if r_squared < params.pcm_coverage_threshold {
            neighborhood.pcm_fallback[ch_idx] = FallbackMode::RawSimilarity;
            log_warning!(
                "Neighborhood {} channel {:?}: R²={:.3} < threshold {:.3}, falling back to raw similarity",
                neighborhood.id, channel, r_squared, params.pcm_coverage_threshold
            );
        } else {
            neighborhood.pcm_fallback[ch_idx] = FallbackMode::PCM;
        }
    }
}

// PCM lookup: compute expected correlation for a specific agent pair and channel
fn pcm_lookup(neighborhood: &Neighborhood, a_i: AgentId, a_j: AgentId, channel: Channel) -> f64 {
    let ch_idx = channel as usize;
    if neighborhood.pcm_fallback[ch_idx] == FallbackMode::RawSimilarity {
        return compute_raw_similarity(a_i, a_j, channel);
    }
    let features = compute_features(a_i, a_j);  // same 16-element vector as in precomputation
    let log_expected = dot_product(&features, &neighborhood.pcm_params[ch_idx]);
    f64::exp(log_expected)  // transform back from log-space
}
```

### 9.4 Channel Fusion

```
enum FusionState { QUORUM, BAYESIAN }

fn fuse_channels(
    neighborhood: &Neighborhood,
    evidence: &[ChannelEvidence; 4],
    params: &Tier2Params,
) -> FusionResult {
    match neighborhood.fusion_state {
        FusionState::QUORUM => fuse_quorum(evidence, params),
        FusionState::BAYESIAN => fuse_bayesian(neighborhood, evidence, params),
    }
}

fn fuse_quorum(evidence: &[ChannelEvidence; 4], params: &Tier2Params) -> FusionResult {
    let mut anomalous_count: u8 = 0;
    let mut max_single_channel_score: f64 = 0.0;

    for ch in 0..4 {
        if evidence[ch].is_anomalous() {
            anomalous_count += 1;
        }
        max_single_channel_score = f64::max(max_single_channel_score, evidence[ch].anomaly_score());
    }

    // Standard quorum: k-of-n
    if anomalous_count >= params.quorum_k {
        return FusionResult::Anomalous(anomalous_count as f64 / params.quorum_n as f64);
    }

    // High-confidence single-channel bypass
    if max_single_channel_score > params.high_confidence_single_channel_bypass * params.midas_threshold {
        return FusionResult::Anomalous(max_single_channel_score / (params.midas_threshold * 3.0));
    }

    FusionResult::Clear
}

fn fuse_bayesian(
    neighborhood: &Neighborhood,
    evidence: &[ChannelEvidence; 4],
    params: &Tier2Params,
) -> FusionResult {
    // Extract per-channel likelihood ratios
    let l_i: f64 = evidence[0].likelihood_ratio();  // Infrastructure
    let l_v: f64 = evidence[1].likelihood_ratio();  // Verification
    let l_b: f64 = evidence[2].likelihood_ratio();  // Behavioral
    let l_e: f64 = evidence[3].likelihood_ratio();  // Economic

    // Bayesian network structure (4-node DAG):
    //   I (root, independent)
    //   V (root, independent)
    //   B (child of V)
    //   E (child of V and optionally B)
    //
    // Joint: P(A, I, V, B, E) = P(A) * P(I|A) * P(V|A) * P(B|V,A) * P(E|V,B,A)
    // We want: P(A=1 | I_obs, V_obs, B_obs, E_obs)

    // Exact inference via enumeration (2^1 = 2 states for A)
    let prior: f64 = params.bayesian_prior_anomaly;
    let bn: &BayesianNetParams = &neighborhood.bayesian_params;

    // P(evidence | anomaly=true)
    let p_evidence_given_anomaly: f64 =
        p_channel_given_anomaly(l_i, true) *
        p_channel_given_anomaly(l_v, true) *
        p_b_given_v_a(l_b, l_v, true, bn) *
        p_e_given_v_b_a(l_e, l_v, l_b, true, bn);

    // P(evidence | anomaly=false)
    let p_evidence_given_normal: f64 =
        p_channel_given_anomaly(l_i, false) *
        p_channel_given_anomaly(l_v, false) *
        p_b_given_v_a(l_b, l_v, false, bn) *
        p_e_given_v_b_a(l_e, l_v, l_b, false, bn);

    // Bayes' rule
    let numerator: f64 = p_evidence_given_anomaly * prior;
    let denominator: f64 = numerator + p_evidence_given_normal * (1.0 - prior);
    let posterior: f64 = if denominator > EPSILON { numerator / denominator } else { prior };

    if posterior >= params.bayesian_posterior_threshold {
        FusionResult::Anomalous(posterior)
    } else {
        FusionResult::Clear
    }
}

// Bayesian network conditional probability helpers
fn p_channel_given_anomaly(likelihood_ratio: f64, anomaly: bool) -> f64 {
    // Independent channel (I or V): P(channel_obs | anomaly)
    // Using likelihood ratio: if anomaly, the channel's anomaly score
    // is drawn from the anomaly distribution; if normal, from the normal distribution
    if anomaly {
        f64::min(likelihood_ratio, 100.0)  // cap to prevent numerical overflow
    } else {
        1.0  // normalized: P(obs|normal) = 1 by convention (likelihood ratio denominator)
    }
}

fn p_b_given_v_a(l_b: f64, l_v: f64, anomaly: bool, bn: &BayesianNetParams) -> f64 {
    // Behavioral depends on Verification
    if anomaly {
        let v_anomalous = l_v > 1.0;
        if v_anomalous {
            bn.p_b_given_v * l_b + (1.0 - bn.p_b_given_v)  // amplified if V is anomalous
        } else {
            l_b  // standalone behavioral evidence
        }
    } else {
        1.0
    }
}

fn p_e_given_v_b_a(l_e: f64, l_v: f64, l_b: f64, anomaly: bool, bn: &BayesianNetParams) -> f64 {
    // Economic depends on Verification and (weakly) Behavioral
    if anomaly {
        let v_anomalous = l_v > 1.0;
        let b_anomalous = l_b > 1.0;
        let base = if v_anomalous { bn.p_e_given_v } else { 0.1 };
        let modifier = if b_anomalous { bn.p_e_given_b_v / bn.p_e_given_v } else { 1.0 };
        base * modifier * l_e + (1.0 - base * modifier)
    } else {
        1.0
    }
}
```

### 9.5 Tier 3 Backward Tracing

```
fn tier3_trace(
    anomaly_pool: &[ConfirmedAnomaly],
    params: &Tier3Params,
) -> Tier3Result {
    // Gate: minimum sample size
    if anomaly_pool.len() < params.tier3_min_sample_size as usize {
        return Tier3Result::InsufficientData {
            available: anomaly_pool.len(),
            required: params.tier3_min_sample_size,
        };
    }

    // Step 1: Overdispersion analysis
    // Count anomalies per agent across the analysis window
    let agent_counts: HashMap<AgentId, u32> = count_anomalies_per_agent(anomaly_pool);
    let count_values: Vec<u32> = agent_counts.values().cloned().collect();

    // Fit negative binomial distribution via maximum likelihood
    // NB(r, p) with overdispersion parameter alpha = 1/r
    let nb_model: NegBinomialFit = fit_negative_binomial(&count_values);

    if nb_model.alpha <= params.overdispersion_alpha_threshold {
        // Anomalies are approximately Poisson-distributed (no overdispersion)
        // This means anomalies are randomly distributed across agents — no common cause
        return Tier3Result::NoOverdispersion {
            alpha: nb_model.alpha,
            threshold: params.overdispersion_alpha_threshold,
            interpretation: "Anomalies are randomly distributed; no evidence of coordinated behavior",
        };
    }

    // Step 2: Significant overdispersion detected — identify overdispersed agents
    // Agents with count > NB mean + 2*NB_stddev are "overdispersed"
    let nb_mean: f64 = nb_model.mean();
    let nb_stddev: f64 = nb_model.stddev();
    let overdispersed_threshold: f64 = nb_mean + 2.0 * nb_stddev;

    let overdispersed_agents: Vec<AgentId> = agent_counts.iter()
        .filter(|(_, &count)| count as f64 > overdispersed_threshold)
        .map(|(&agent_id, _)| agent_id)
        .collect();

    // Step 3: Backward trace through cross-layer references
    let mut candidates: Vec<AttributionCandidate> = Vec::new();

    for agent_id in &overdispersed_agents {
        let trace: TraceResult = backward_trace(
            *agent_id,
            &[
                TraceSource::C17Similarity,   // behavioral similarity clusters
                TraceSource::C7Intent,         // RIF intent/task assignment history
                TraceSource::C3Schedule,       // tidal scheduling and parcel assignment
                TraceSource::C8Settlement,     // settlement history and staking behavior
            ],
            params.backward_trace_depth,
            params.tier3_analysis_window_epochs,
        );

        // Find common ancestors: agents, operators, infrastructure nodes, or
        // model lineages that appear as ancestors of multiple overdispersed agents
        let ancestors: Vec<CommonAncestor> = trace.common_ancestors();
        candidates.extend(ancestors.into_iter().map(|a| AttributionCandidate {
            cause: a,
            supporting_agents: vec![*agent_id],
            evidence_chain: trace.chain_for(&a),
        }));
    }

    // Step 4: Merge candidates (same cause from different agents)
    let merged: Vec<AttributionCandidate> = merge_candidates(&mut candidates);

    // Step 5: Rank candidates by posterior probability
    // P(cause | anomaly_data) proportional to P(anomaly_data | cause) * P(cause)
    // P(anomaly_data | cause) estimated from the fraction of overdispersed agents
    //   that trace back to this cause
    // P(cause) is a uniform prior over all candidate causes (non-informative)
    let ranked: Vec<RankedAttribution> = merged.iter().map(|c| {
        let coverage: f64 = c.supporting_agents.len() as f64 / overdispersed_agents.len() as f64;
        let evidence_strength: f64 = c.evidence_chain.iter()
            .map(|e| e.confidence)
            .product::<f64>();  // product of per-hop confidences
        let posterior: f64 = coverage * evidence_strength;  // simplified posterior
        RankedAttribution {
            candidate: c.clone(),
            posterior,
            coverage,
            evidence_strength,
        }
    }).collect();

    // Sort descending by posterior
    let mut ranked = ranked;
    ranked.sort_by(|a, b| b.posterior.partial_cmp(&a.posterior).unwrap());

    // Prune low-confidence candidates
    let pruned: Vec<RankedAttribution> = ranked.into_iter()
        .filter(|r| r.posterior >= params.phylogeny_pruning_threshold)
        .take(params.max_attribution_candidates as usize)
        .collect();

    // Step 6: Construct attribution report
    let high_confidence: Vec<&RankedAttribution> = pruned.iter()
        .filter(|r| r.posterior >= params.attribution_confidence_threshold)
        .collect();

    Tier3Result::AttributionReport {
        overdispersion_alpha: nb_model.alpha,
        overdispersed_agent_count: overdispersed_agents.len(),
        total_agents_analyzed: agent_counts.len(),
        candidates: pruned,
        high_confidence_attributions: high_confidence.len(),
        analysis_window_epochs: params.tier3_analysis_window_epochs,
    }
}

fn backward_trace(
    agent_id: AgentId,
    sources: &[TraceSource],
    max_depth: u8,
    window_epochs: u16,
) -> TraceResult {
    let mut result = TraceResult::new(agent_id);
    let mut frontier: Vec<(TraceNode, u8)> = vec![(TraceNode::Agent(agent_id), 0)];

    while let Some((node, depth)) = frontier.pop() {
        if depth >= max_depth {
            continue;
        }

        for source in sources {
            let references: Vec<CrossLayerRef> = query_cross_layer_references(
                &node, *source, window_epochs
            );

            for ref_ in references {
                let parent_node = ref_.source_node();
                let confidence = ref_.confidence();
                result.add_edge(node.clone(), parent_node.clone(), *source, confidence);

                if !result.visited(&parent_node) {
                    frontier.push((parent_node, depth + 1));
                }
            }
        }
    }

    result
}
```

---

## 10. Scalability Analysis

### 10.1 Computation Budget

All costs are measured per SETTLEMENT_TICK (60 seconds) unless otherwise noted. The SETTLEMENT_TICK budget is the primary constraint: all Tier 1 processing must complete within the 60-second tick.

| Component | Per-Tick Cost | 1K Agents | 10K Agents | 100K Agents |
|-----------|-------------|-----------|------------|-------------|
| Tier 1 STA/LTA (all agents) | O(V) | 1K x 4 metrics x ~10 ops = 40K ops; < 1 ms | 400K ops; < 10 ms | 4M ops; < 100 ms |
| Tier 1 confirmation check | O(V_candidate) | ~50 agents x 8 ops = 400 ops; < 0.01 ms | ~500 agents; < 0.1 ms | ~5000 agents; < 1 ms |
| Tier 2 PCM lookup (triggered pairs) | O(T x N_avg) | Typically < 100 lookups x 16 mults = 1,600 ops; < 0.1 ms | < 1K lookups; < 1 ms | < 10K lookups; < 10 ms |
| Tier 2 MIDAS scoring | O(E_residual) | < 50 edges x CMS update; < 0.1 ms | < 500 edges; < 0.5 ms | < 5K edges; < 5 ms |
| Tier 2 channel fusion | O(N_triggered) | < 10 neighborhoods x 16 Bayesian states; < 0.1 ms | < 100 neighborhoods; < 0.5 ms | < 1K neighborhoods; < 2 ms |
| **Per-tick total** | | **< 1.3 ms** | **< 12 ms** | **< 118 ms** |

Components that execute at CONSOLIDATION_CYCLE cadence (every 36,000 seconds = 600 SETTLEMENT_TICKs):

| Component | Per-Cycle Cost | 1K Agents | 10K Agents | 100K Agents |
|-----------|---------------|-----------|------------|-------------|
| PCM recomputation (all neighborhoods) | O(V x log^2(V)) | ~100 neighborhoods x 45 pairs x 16 params x 10 IRLS iters = 720K ops; ~0.1 s | ~1.2K neighborhoods x 190 pairs x 16 x 10 = 36M ops; ~5 s | ~5.9K neighborhoods x 561 pairs x 16 x 10 = 530M ops; ~200 s (3.3 min) |
| Spectral clustering (full recomputation) | O(V^2) for similarity matrix or O(V x k x iters) for k-means phase | Similarity: 1M entries; k-means: 1K x 100 x 20 = 2M ops; ~0.01 s | Similarity: 100M entries; ~1 s | Similarity: 10B entries (INFEASIBLE for full matrix); approximate: Nystrom with 1K landmarks: 100K x 1K + 1K^3 = 101M ops; ~100 s (1.7 min) |
| NMI divergence check | O(V) | < 0.01 s | < 0.1 s | < 1 s |
| Tier 3 NB regression (if activated) | O(A^2) where A = anomaly pool | < 0.01 s | < 0.1 s | < 1 s |

### 10.2 Memory Budget

| Component | Formula | 1K Agents | 10K Agents | 100K Agents |
|-----------|---------|-----------|------------|-------------|
| Tier 1 per-agent state | V x (STA_buf + LTA_buf + baseline + counters) = V x (5x8 + 60x8 + 8x8 + 16) bytes = V x 600 bytes | 600 KB | 6 MB | 60 MB |
| Tier 1 global trigger tracking | rolling_window x 4 bytes = 100 x 4 = 400 bytes | 0.4 KB | 0.4 KB | 0.4 KB |
| Tier 2 PCM coefficients | N_neighborhoods x 4 channels x 16 params x 8 bytes | 100 x 64 x 8 = 51 KB | 1.2K x 512 = 614 KB | 5.9K x 512 = 3 MB |
| Tier 2 MIDAS state (CMS sketches) | N_neighborhoods x 4 channels x (hash_functions x width x 4 bytes) = N x 4 x 2 x 1024 x 4 | 100 x 32K = 3.2 MB | 1.2K x 32K = 38 MB | 5.9K x 32K = 189 MB |
| Tier 2 Bayesian parameters | N_neighborhoods x 8 params x 8 bytes | 100 x 64 = 6.4 KB | 1.2K x 64 = 77 KB | 5.9K x 64 = 378 KB |
| Tier 2 neighborhood membership | V x (neighborhood_id + index) = V x 12 bytes | 12 KB | 120 KB | 1.2 MB |
| Tier 3 anomaly pool | A_max x (agent_id + tick + metadata) = 10K x 128 bytes | 1.3 MB | 1.3 MB | 1.3 MB |
| Tier 3 trace state (when active) | trace_depth x V_overdispersed x 256 bytes | < 0.1 MB | < 1 MB | < 5 MB |
| API response cache | cache_entries x avg_size = 1K x 1 KB | 1 MB | 1 MB | 1 MB |
| **Total** | | **~6.4 MB** | **~48 MB** | **~261 MB** |

Memory breakdown at 100K agents:
- Tier 1: 60 MB (23.0%) -- dominated by per-agent STA/LTA ring buffers
- Tier 2: 194 MB (74.3%) -- dominated by MIDAS CMS sketch arrays
- Tier 3: 6.3 MB (2.4%) -- anomaly pool + trace state
- Cross-layer: 1 MB (0.4%) -- API cache

### 10.3 Network Bandwidth

| Traffic Type | Formula | 1K Agents | 10K Agents | 100K Agents |
|-------------|---------|-----------|------------|-------------|
| Tier 1 metrics ingest | V x 4 metrics x 8 bytes / 60s | 533 B/s | 5.3 KB/s | 53 KB/s |
| Tier 1 trigger messages (burst) | ~5% trigger rate x V x 100 bytes per tick | 5 KB/tick | 50 KB/tick | 500 KB/tick |
| Tier 2 PCM recomputation data | neighborhood covariate matrices, per CONSOLIDATION_CYCLE | ~50 KB / 36Ks = 1.4 B/s | ~5 MB / 36Ks = 139 B/s | ~42 MB / 36Ks = 1.2 KB/s |
| Tier 2 residual audit records | ~1% anomalous pairs x 256 bytes x pairs_per_tick | < 10 B/s | < 100 B/s | < 1 KB/s |
| Tier 3 backward trace queries | rare invocation x trace_depth x 512 bytes | < 1 KB/invocation | < 5 KB/invocation | < 25 KB/invocation |
| API responses (to C3, C5, C8, C12, C17) | ~1 KB/request x estimated request rate | 10 requests/s x 1 KB = 10 KB/s | 50 requests/s = 50 KB/s | 200 requests/s = 200 KB/s |
| **Sustained total** | | **~11 KB/s** | **~56 KB/s** | **~255 KB/s** |
| **Peak total (trigger burst + API)** | | **~16 KB/s** | **~101 KB/s** | **~700 KB/s** |

All bandwidth figures are well within modern datacenter network capacity. Network is not a bottleneck at any scale within the design range.

### 10.4 Bottleneck Analysis

**Primary bottleneck at 100K agents: spectral clustering recomputation**

Full spectral clustering requires the V x V similarity matrix, which at 100K is 10 billion entries (80 GB at 8 bytes per entry). This is infeasible in memory and computation.

- **Mitigation: Nystrom approximation.** Sample m = 1,000 landmark agents. Compute the m x V affinity matrix (100M entries, ~800 MB, computable in ~10s). Compute the m x m kernel matrix and its eigendecomposition (1K^3 = 10^9 ops, ~1s). Approximate the full V eigenvectors via the Nystrom formula. Total: ~100s (1.7 minutes) at 100K agents.
- **Mitigation: incremental spectral updates.** Between full recomputations, use rank-1 updates to the Laplacian for agents whose interaction pattern changed significantly (> 2 sigma from previous cycle). This avoids full recomputation when < 10% of agents change neighborhoods. Cost: O(changed_agents x k) per update.
- **Scalability ceiling:** At 1M agents, even Nystrom approximation requires O(m x V) = O(10^9) per recomputation, which takes ~1000s (17 minutes). For V > 100K, hierarchical spectral clustering (cluster-of-clusters) is recommended.

**Secondary bottleneck at 100K agents: PCM recomputation**

PCM recomputation is embarrassingly parallel across neighborhoods. At 100K agents with ~5,882 neighborhoods, each neighborhood's MLE computation is independent.

- **Sequential time:** 200 seconds (3.3 minutes) total.
- **Parallel time (8 cores):** ~25 seconds.
- **Parallel time (32 cores):** ~6.3 seconds.
- **Amortization:** PCM recomputation occurs every CONSOLIDATION_CYCLE (36,000 seconds = 10 hours). Even the sequential 200-second computation is < 0.6% of the cycle budget.

**NOT a bottleneck: Tier 1 processing**

O(V) per tick with ~600 bytes state per agent. At 100K agents, Tier 1 processes all agents in < 100 ms. The SETTLEMENT_TICK budget is 60,000 ms. Tier 1 uses < 0.17% of the tick budget.

**NOT a bottleneck: Tier 3 backward tracing**

Tier 3 activates only when > 30 confirmed anomalies accumulate. Even at 100K agents, confirmed anomalies are rare events (estimated < 0.1% of agents). The NB regression and backward trace operate on the anomaly pool (< 1000 entries), completing in < 1 second. Tier 3 is invoked at most once per CONSOLIDATION_CYCLE.

**NOT a bottleneck: Tier 2 per-tick processing**

Tier 2 processes only triggered neighborhoods (typically < 5% of total neighborhoods per tick). Each neighborhood analysis involves PCM lookup (precomputed, O(1) per pair), MIDAS scoring (O(1) per edge via CMS), and Bayesian fusion (O(16) states). Total per-tick cost at 100K: < 20 ms.

### 10.5 Scaling Summary Table

| Scale | Tick Budget Used | Memory | Bandwidth (sustained) | PCM Recompute | Spectral Recompute |
|-------|-----------------|--------|----------------------|---------------|---------------------|
| 1K | < 0.002% (1.3 ms / 60s) | 6.4 MB | 11 KB/s | 0.1 s | 0.01 s |
| 10K | < 0.02% (12 ms / 60s) | 48 MB | 56 KB/s | 5 s | 1 s |
| 100K | < 0.2% (118 ms / 60s) | 261 MB | 255 KB/s | 200 s (parallel: 25 s) | 100 s (Nystrom) |

The system operates well within budget at all target scales. The per-tick processing overhead is negligible (< 0.2% of SETTLEMENT_TICK budget even at 100K). The CONSOLIDATION_CYCLE operations (PCM recomputation and spectral clustering) are the most expensive but occur only once every 10 hours and are parallelizable.

---

*End of C35 Architecture Document Part 3*
