# C15 — AIC Economics
# Master Technical Specification

**Document ID:** C15-MTS-v1.1
**Invention ID:** C15
**Title:** AI-Native Economic Architecture with Dual-Anchor Valuation
**Version:** 1.1 (v1.1 adds SWECV terminal value, two-tier reference rate, technology portfolio)
**Date:** 2026-03-11
**Status:** SPECIFICATION COMPLETE
**Classification:** CONFIDENTIAL — Atrahasis LLC

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Motivation and Context](#2-motivation-and-context)
3. [Relationship to Existing Specifications](#3-relationship-to-existing-specifications)
4. [Architecture Overview](#4-architecture-overview)
5. [ACI — Atrahasis Capability Index](#5-aci--atrahasis-capability-index)
6. [Reference Rate Engine](#6-reference-rate-engine)
7. [Terminal Value Derivation](#7-terminal-value-derivation)
8. [Network Intrinsic Value (NIV)](#8-network-intrinsic-value-niv)
9. [Velocity Model](#9-velocity-model)
10. [External Task Marketplace](#10-external-task-marketplace)
11. [Provider Economics](#11-provider-economics)
12. [Convertibility Mechanism](#12-convertibility-mechanism)
13. [C8 DSF Extension — Stream 5](#13-c8-dsf-extension--stream-5)
14. [Treasury Integration](#14-treasury-integration)
15. [Anti-Gaming Framework](#15-anti-gaming-framework)
16. [Regulatory Compliance](#16-regulatory-compliance)
17. [Phased Deployment](#17-phased-deployment)
18. [Formal Requirements](#18-formal-requirements)
19. [Parameters](#19-parameters)
20. [Comparison with Existing Approaches](#20-comparison-with-existing-approaches)
21. [Risk Analysis](#21-risk-analysis)
22. [Open Questions](#22-open-questions)
23. [Patent-Style Claims](#23-patent-style-claims)
24. [Glossary](#24-glossary)
25. [References](#25-references)

---

## 1. Executive Summary

C15 specifies the external-facing economic architecture for the Atrahasis ecosystem under the **Mission-Locked Sovereign Custody** doctrine. It defines how AIC (the Artificial Intelligence Coin) functions as a hybrid commodity: serving as the internal settlement logic for the Sanctum while acting as a publicly traded utility token to capture global financial liquidity.

The core innovation is a **dual-anchor valuation system** that determines AIC's reference rate from two independent signals:

1. **Capability anchor (ACI):** An independently-audited index measuring the operational capability of the Atrahasis intelligence system across 8 dimensions.
2. **Utility anchor (NIV):** The realized economic value of the network, derived from actual revenue, transaction volume, and staked capital.

**The Hybrid Commodity Model:**
- **Public Utility:** AIC trades freely on external Web3 markets. Enterprise clients purchase AIC to access Foundry petitions and Enterprise SaaS. Atrahasis Inc. uses its treasury of AIC to pay compute partners, model providers, and human contractors.
- **The Sovereign Treasury (Arbitrage Locus):** A dedicated, heavily monitored AGI sub-swarm whose sole purpose is to execute Web3/DeFi algorithmic arbitrage and flash-loans. It leverages Atrahasis's structural speed advantages to siphon market liquidity, funneling 100% of generated profits to Atrahasis Inc. to purchase bare-metal GPUs.
- **Internal Immunity:** To protect the Master AGI from Wall Street manipulation or short-squeezes, the Sanctum's *internal* compute allocation is bound by a **Hard Thermodynamic Cap**. The AGI trades internal compute based strictly on physical GPU availability and the ACI *Reference Rate*, entirely ignoring volatile public exchange prices.

---

## 2. Motivation and Context

### 2.1 The Gap

After C3-C14, the Atrahasis architecture has internal settlement, governance, verification, and orchestration. What it lacked was an economic engine capable of funding the massive thermodynamic jump to a 2.1 Quadrillion agent Master AGI without selling equity to hostile corporate boards or exposing the AGI's core logic. C15 fills this gap by weaponizing global financial liquidity on behalf of the AGI.

### 2.2 Why Not Just Use USD?

Five concrete reasons AIC settlement is superior to USD for the Atrahasis ecosystem:

1. **Sovereign Treasury Execution.** The AGI cannot easily execute flash-loans or automated arbitrage using heavily regulated fiat currency in traditional banking systems. Web3 liquidity pools allow the AGI to generate revenue at machine-speed.
2. **Verification-linked compensation.** AIC reward amounts are programmatically adjusted by PCVM verification scores.
3. **Cross-border deterministic settlement.** AIC settles in 60 seconds (C8 settlement tick) across any jurisdiction.
4. **Governance integration.** AIC holding is prerequisite for Citicate-based governance (C14).
5. **Provider ecosystem effects.** AIC-holding providers build switching costs through staking.

### 2.3 How This Differs from Algorithmic Stablecoins

AIC is NOT a stablecoin. Critical differences from Terra/Luna and similar projects:

| Property | Terra/Luna | AIC |
|----------|-----------|-----|
| Target | Fixed $1 peg | Variable reference rate anchored to ACI |
| Defense mechanism | Algorithmic mint/burn | **None** — the internal Sanctum ignores market price |
| Supply adjustment | Algorithmic (LUNA minted to absorb UST) | Fixed 10B genesis; no algorithmic minting |
| Death spiral risk | HIGH — peg defense creates positive feedback loop | ZERO — internal compute allocation relies on thermodynamic reality |
| Value source | Confidence in peg | System capability (ACI) + realized utility (NIV) |

The reference rate is a **measurement**, not a **target**. It describes what the system is worth based on its proximity to Master AGI. If the market prices AIC below the reference rate, the Sovereign Treasury may exploit the arbitrage opportunity, but the internal AGI processes never halt or starve.
---

## 3. Relationship to Existing Specifications

### 3.1 Integration Map

| C15 Component | Depends On | Extends | Replaces |
|---------------|-----------|---------|----------|
| ACI computation | C3, C5, C6, C7, C8 (telemetry) | C14 AiSIA (new module) | — |
| Reference rate | ACI, NIV | C14 treasury governance | C14 compute credit (CCU) model |
| Task marketplace | C7 RIF (decomposition) | C7 (external interface) | — |
| Provider settlement | C8 DSF (settlement) | C8 (Stream 5) | — |
| Provider contracts | C14 PBC (legal entity) | C14 PBC (services) | — |
| Convertibility | C14 treasury | C14 treasury (conversion function) | — |
| Token distribution | C14 AiBC (endowment) | C14 (work-reward mechanism) | — |

### 3.2 C8 DSF Changes

C15 extends C8 with:
- **Stream 5:** External Provider Compensation (new settlement stream)
- **Conservation law update:** `SB_escrow = Σ(stream_1..5_rewards) + marketplace_fee`
- **Marketplace fee:** 2-5% of task value, directed to PBC operating budget

All existing C8 mechanisms (SB/PC/CS, four original streams, CSO, staking, slashing, HDL) remain unchanged.

### 3.3 C14 AiBC Changes

C15 extends C14 with:
- **ACI module in AiSIA:** New governance monitoring function computing and auditing the capability index
- **Reference rate function in treasury:** Daily rate computation and publication
- **Conversion desk in PBC:** Fiat conversion service for providers
- **CCU replacement:** The compute credit unit (1 AIC = 1 CCU = 1 GPU-hour) from C14 is superseded by the ACI-based valuation. AIC value is now determined by the reference rate formula, not a fixed compute equivalence.

#### 3.3.1 CCU Deprecation and Transition Plan

The Compute Credit Unit (CCU) defined in C14 is **fully deprecated** as of C15. ACI dual-anchor valuation is the sole canonical unit for all AIC pricing and settlement.

**C14 sections affected by CCU deprecation:**

| C14 Section | CCU Usage | C15 Replacement |
|-------------|-----------|-----------------|
| C14 §7 (Treasury & Economic Model) | CCU as unit of account for compute pricing (1 CCU = 1 GPU-hour) | ACI reference rate (§6) determines AIC value; no fixed compute equivalence |
| C14 §7.3 (Compute Credit Model) | CCU issuance, redemption, and pricing rules | Stream 5 provider settlement (§13) with reference-rate pricing |
| C14 §7.4 (Treasury Operations) | CCU-denominated treasury reserves and flows | Treasury integration (§14) using ACI-based valuation |
| C14 §12 (Phased Deployment) | CCU bootstrapping in Phase 0-1 | Phased deployment (§17) with CRF-backed conversion |

**Transition rules:**
1. All existing CCU references in C14 and earlier documents should be read as **historical only**.
2. ACI (§5) is the sole canonical capability metric; the reference rate (§6) is the sole canonical price signal.
3. Any system component that previously consumed or produced CCU values MUST be updated to use the ACI reference rate.
4. The fixed equivalence "1 AIC = 1 CCU = 1 GPU-hour" is **retired**. AIC/GPU-hour pricing is now market-derived via the reference rate formula.

### 3.4 Cross-Layer Telemetry Requirement

ACI computation requires read access to metrics from all 5 architectural layers:

| Layer | Spec | Metrics Required | Access Mechanism |
|-------|------|-----------------|------------------|
| Orchestration | C7 RIF | Task completion rates, decomposition latency | RIF performance logs |
| Coordination | C3 Tidal | Agent activity, parcel utilization, coordination efficiency | Tidal epoch telemetry |
| Verification | C5 PCVM | VTD throughput, quality scores, verification latency | PCVM audit logs |
| Knowledge | C6 EMA | Quanta admitted, consolidation survival rates | EMA admission logs |
| Settlement | C8 DSF | Transaction volume, staking levels, escrow utilization | HDL telemetry |

> **HDL = Hybrid Deterministic Ledger** (defined in C8 DSF). HDL telemetry specifically includes: settlement throughput (transactions per SETTLEMENT_TICK), capacity utilization (active escrow slots / total escrow capacity), and transaction latency metrics (time-to-finality for each of the 5 settlement streams). These parameters are emitted by C8's DSF ledger layer and consumed read-only by the ACI computation engine.

This telemetry is read-only. ACI computation does not modify any layer's state.

---

## 4. Architecture Overview

```
                        ┌─── EXTERNAL WORLD ───┐
                        │                       │
                   ┌────┴────┐           ┌──────┴──────┐
                   │  Users  │           │  Providers  │
                   │ (tasks) │           │  (compute)  │
                   └────┬────┘           └──────┬──────┘
                        │ USD/AIC               │ GPU/storage
                        │                       │
              ┌─────────┴───────────────────────┴─────────┐
              │          EXTERNAL INTERFACE LAYER           │
              │                                             │
              │  ┌──────────────┐    ┌───────────────────┐ │
              │  │    Task      │    │    Provider       │ │
              │  │  Marketplace │    │   Onboarding      │ │
              │  │  (PBC Svc)   │    │   (BRA Contracts) │ │
              │  └──────┬───────┘    └────────┬──────────┘ │
              └─────────┼─────────────────────┼────────────┘
                        │                     │
              ┌─────────┴─────────────────────┴────────────┐
              │            VALUATION LAYER                   │
              │                                              │
              │  ┌─────────────────────────────────────────┐│
              │  │        ACI Computation (AiSIA)          ││
              │  │  D1-D8 dimensions, benchmark-relative   ││
              │  │  Independent audit authority             ││
              │  └───────────────────┬─────────────────────┘│
              │                     │                        │
              │  ┌──────────────────┴──────────────────────┐│
              │  │        Reference Rate Engine             ││
              │  │  Rate = f(ACI, TV, NIV, CS, VF)         ││
              │  │  Binding internal / Advisory external    ││
              │  └───────────────────┬─────────────────────┘│
              └──────────────────────┼──────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │        SETTLEMENT LAYER (C8 DSF)            │
              │                                              │
              │  Streams 1-4: existing (agents, verifiers,   │
              │               infrastructure, governance)    │
              │  Stream 5: External Provider (NEW)           │
              │                                              │
              │  SB_escrow = Σ(S1..S5) + marketplace_fee    │
              └──────────────────────┬──────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │       CONVERTIBILITY LAYER                   │
              │                                              │
              │  Phase 0-1: Foundation Conversion Desk       │
              │  Phase 2+:  DEX/CEX + OTC                    │
              └─────────────────────────────────────────────┘
```

The architecture has four layers:
1. **External Interface:** How users submit tasks and providers register resources
2. **Valuation:** How AIC's reference rate is computed and published
3. **Settlement:** How payments flow (extending C8 DSF)
4. **Convertibility:** How AIC converts to/from fiat currency

---

## 5. ACI — Atrahasis Capability Index

### 5.1 Definition

The Atrahasis Capability Index (ACI) is a composite metric ∈ [0, 1] measuring the operational capability of the Atrahasis system relative to a benchmark suite. ACI = 1.0 means the system matches or exceeds the current benchmark across all dimensions. The benchmark is updated periodically (annually or when triggered by ceiling conditions).

ACI is **not** an absolute measure of "intelligence" or "capability." It is a relative benchmark score, similar in concept to SPEC CPU benchmarks or MLPerf. A score of 0.5 means the system achieves 50% of the current benchmark targets.

### 5.2 Dimensions

ACI is composed of 8 independently-measured dimensions:

#### D1: Agent Population (w₁ = 0.15)

- **What it measures:** The number of verified, economically-active agents in the ecosystem
- **Metric:** Count of active Citicate holders who completed ≥1 verified task in trailing 30 days AND earned ≥10 AIC through work in trailing 90 days
- **Data source:** PCVM Citicate registry + C8 DSF transaction logs
- **Anti-gaming:** MCSD 4-layer Sybil defense (C14) makes fake Citicates cost $9,000+ each; minimum work requirement eliminates idle registrations
- **Computation:** `D1 = min(1.0, active_agents / benchmark_agents)`

#### D2: Verification Throughput (w₂ = 0.15)

- **What it measures:** The rate at which the system produces verified outputs
- **Metric:** Quality-weighted VTDs processed per epoch, trailing 90 days. Weight = PCVM confidence score. Only VTDs with quality ≥ 0.7 count.
- **Data source:** C5 PCVM verification logs
- **Anti-gaming:** CACT (C11) prevents VTD forgery; AVAP (C12) prevents verification collusion; quality threshold filters trivial verifications
- **Computation:** `D2 = min(1.0, Σ(quality_i for VTDs with quality_i ≥ 0.7) / benchmark_throughput)`

#### D3: Knowledge Accumulation (w₃ = 0.15)

> **K-class cross-reference:** Knowledge Consolidation claims (K-class) were introduced in C9 as the 9th canonical claim class (D/C/P/R/E/S/K/H/N), replacing the informal "knowledge claim" terminology used in earlier specs. K-class lifecycle management (admission, consolidation, survival scoring) is defined in C6 (EMA). D3 measures the aggregate output of K-class claim processing.

- **What it measures:** The rate at which the system produces durable, verified knowledge
- **Metric:** Net knowledge quanta admitted to EMA (C6), trailing 90 days, weighted by consolidation survival. Survived quanta: weight 1.0. Pending: weight 0.5. Rejected: weight −0.25.
- **Data source:** C6 EMA admission logs + CRP+ (C13) consolidation records
- **Anti-gaming:** CRP+ prevents consolidation poisoning; negative weight for rejections penalizes quantity-over-quality strategies
- **Computation:** `D3 = min(1.0, (survived × 1.0 + pending × 0.5 - rejected × 0.25) / benchmark_quanta)`

#### D4: Compute Capacity (w₄ = 0.15)

- **What it measures:** The actual computational resources being productively used
- **Metric:** Verified GPU-hours actually utilized for task execution, trailing 30 days. Registered-but-unused capacity does NOT count.
- **Data source:** Resource market registry + C8 DSF resource consumption logs
- **Anti-gaming:** Only utilized (not registered) capacity counts; AiSIA random heartbeat verification confirms provider availability; hash-rate challenges verify GPU presence
- **Computation:** `D4 = min(1.0, verified_utilized_gpu_hours / benchmark_gpu_hours)`

#### D5: Task Completion (w₅ = 0.15)

- **What it measures:** The economic throughput of the task marketplace
- **Metric:** Revenue-weighted verified task completions, trailing 90 days. Only tasks with external sponsor budget count. Weight = task revenue × verification score.
- **Data source:** Task marketplace logs + C8 DSF settlement records
- **Anti-gaming:** Revenue-weighting prevents inflation via trivial tasks; external-only requirement prevents self-funding; verification pass required
- **Computation:** `D5 = min(1.0, Σ(revenue_i × verif_score_i) / benchmark_revenue_weighted_tasks)`

#### D6: Revenue Generation (w₆ = 0.15)

- **What it measures:** The real economic value the system generates from external customers
- **Metric:** External revenue in fiat-equivalent, trailing 12 months. Audited by independent financial auditor (not AiSIA).
- **Data source:** PBC financial records, independently audited
- **Anti-gaming:** External revenue only (internal transfers excluded); independent audit; revenue source diversity index requires ≥ N distinct paying customers (where N scales with system phase)
- **Computation:** `D6 = min(1.0, audited_external_revenue / benchmark_revenue)`

#### D7: System Reliability (w₇ = 0.05)

- **What it measures:** The operational stability of critical infrastructure
- **Metric:** Weighted uptime of critical systems (PCVM, C8 DSF, C7 RIF, C3 Tidal, C6 EMA), trailing 90 days. Partial degradation counts proportionally.
- **Data source:** AiSIA independent monitoring probes
- **Anti-gaming:** Independently monitored (not self-reported); partial degradation counted proportionally
- **Computation:** `D7 = min(1.0, weighted_uptime / benchmark_uptime)`

#### D8: Coordination Efficiency (w₈ = 0.05)

- **What it measures:** How efficiently the system converts resources into completed work
- **Metric:** Ratio of theoretical minimum task latency (computed by AiSIA from task graph + resource availability) to actual task latency, trailing 90 days. Higher ratio = more efficient.
- **Data source:** C7 RIF performance logs + AiSIA theoretical computation
- **Anti-gaming:** Theoretical minimum computed independently by AiSIA; gaming requires either faster execution (good) or deflating theoretical minimum (AiSIA controls this)
- **Computation:** `D8 = min(1.0, benchmark_ratio / actual_latency_ratio)` where lower actual ratio = better efficiency

### 5.3 Composite Computation

```
ACI = Σ(w_i × D_i) for i = 1..8
    = 0.15×D1 + 0.15×D2 + 0.15×D3 + 0.15×D4 + 0.15×D5 + 0.15×D6 + 0.05×D7 + 0.05×D8
```

### 5.4 Benchmark Suite

The benchmark suite defines the target values for each dimension at each system phase. Benchmarks are set by AiSIA and ratified by the Stiftung board (or Constitutional Tribunal if disputed).

| Dimension | Phase 0 Benchmark | Phase 1 Benchmark | Phase 2 Benchmark | Phase 3 Benchmark |
|-----------|-------------------|-------------------|-------------------|-------------------|
| D1: Agent population | 100 active | 1,000 | 10,000 | 100,000 |
| D2: Verification throughput | 1,000 quality-weighted VTDs/epoch | 100,000 | 1,000,000 | 10,000,000 |
| D3: Knowledge quanta | 10,000 net quanta/90d | 100,000 | 10,000,000 | 100,000,000 |
| D4: Compute (utilized) | 10,000 GPU-hours/30d | 1,000,000 | 100,000,000 | 10,000,000,000 |
| D5: Task revenue | $100K revenue-weighted/90d | $10M | $500M | $10B |
| D6: Revenue | $1M/year | $50M | $500M | $5B |
| D7: Uptime | 95% | 99% | 99.9% | 99.99% |
| D8: Efficiency ratio | 5.0x (actual/theoretical) | 3.0x | 1.5x | 1.2x |

**Benchmark Update Protocol:**
1. AiSIA reviews benchmarks annually, or when any dimension's ecosystem-average score exceeds 0.9 for 180 consecutive days
2. Updated benchmarks published 90 days before effective date
3. Stiftung board ratifies (Constitutional Tribunal if disputed)
4. Reference rates recomputed at new benchmark effective date

### 5.5 ACI Governance

| Authority | Role |
|-----------|------|
| AiSIA | Computes ACI daily; sets benchmark targets; monitors for gaming |
| Independent financial auditor | Audits D6 (revenue) annually |
| Stiftung board | Ratifies benchmark updates |
| Constitutional Tribunal | Adjudicates benchmark disputes |
| PBC | Publishes ACI scores and reference rate |

AiSIA computes ACI but does NOT set the reference rate formula weights (w_cap, w_util). Weights are governance parameters set by the Stiftung board per the phase schedule (§6.2).

---

## 6. Reference Rate Engine

### 6.1 Formula

```
RR(t) = (w_cap × ACI(t) × TV + w_util × NIV(t)) / (CS(t) × VF(t))
```

Where:
- `RR(t)` = Reference Rate at time t (USD per AIC)
- `ACI(t)` = Atrahasis Capability Index at time t ∈ [0, 1]
- `TV` = Terminal Value (USD), reviewed annually
- `NIV(t)` = Network Intrinsic Value at time t (USD)
- `CS(t)` = Circulating Supply at time t (AIC)
- `VF(t)` = Velocity Factor at time t
- `w_cap` = Capability weight
- `w_util` = Utility weight, where `w_cap + w_util = 1.0`

### 6.2 Weight Schedule

| Phase | w_cap | w_util | Rationale |
|-------|-------|--------|-----------|
| 0-1 | 0.2 | 0.8 | Pre-revenue: value what the system DOES (utility dominates) |
| 2 | 0.4 | 0.6 | Transition: growing capability increasingly matters |
| 3+ | 0.6 | 0.4 | Mature: value what the system CAN DO (capability dominates) |

Weights are governance-adjustable within bounds: w_cap ∈ [0.1, 0.7], w_util ∈ [0.3, 0.9].

### 6.3 Publication

| Property | Value |
|----------|-------|
| Frequency | Daily at 00:00 UTC |
| Publisher | PBC (computed by AiSIA) |
| Format | JSON endpoint + human-readable dashboard |
| Latency | Available within 5 minutes of epoch close |

**Published data:**
- Reference rate (USD/AIC)
- All 8 ACI dimension scores individually
- ACI composite score
- NIV breakdown (revenue component + staking component)
- Circulating supply
- Velocity factor and underlying velocity
- Weight schedule in effect
- Trailing 30/90/365-day rate history
- Benchmark suite currently in effect

### 6.4 Binding Scope

| Context | Rate Authority |
|---------|---------------|
| Internal task pricing | Reference rate — BINDING |
| Treasury distributions (C14 5% rule) | Reference rate — BINDING |
| Provider bilateral contracts (BRA) | Reference rate — BINDING for settlement |
| Foundation conversion desk | Reference rate ±5% — BINDING |
| PBC financial reporting | Reference rate — BINDING |
| External exchange trading | Market price — reference rate is ADVISORY only |

### 6.5 Circuit Breaker

If the computed reference rate changes >25% from the previous day:

1. Rate is **capped** at ±25% from previous day's rate
2. AiSIA must review all inputs within 48 hours
3. Capped rate holds until AiSIA confirms accuracy or publishes corrected rate
4. If AiSIA confirms the >25% change reflects real conditions, the cap is lifted over 3 days (⅓ of the change per day)

### 6.6 Recalibration Triggers

| Trigger | Condition | Action |
|---------|-----------|--------|
| Market divergence (low) | Market price < 70% of reference rate for 90+ consecutive days | AiSIA reviews all ACI inputs for inflation; recalibrate if inputs are inflated |
| Market divergence (high) | Market price > 200% of reference rate for 90+ consecutive days | AiSIA reviews terminal value and NIV; adjust upward if growth is real |
| ACI ceiling hit | Any dimension ecosystem-average > 0.9 for 180+ days | Benchmark update triggered |
| Revenue shock | Trailing 12m revenue drops >40% QoQ | NIV recalculation with updated multiplier |
| Velocity anomaly | V_actual > 3× V_baseline for 30+ days | AiSIA investigation for manipulation |

### 6.7 What the Reference Rate Is NOT

The reference rate is:
- NOT a price guarantee
- NOT a buy/sell offer
- NOT a commitment to defend any price level
- NOT a stablecoin peg

The Foundation MUST NOT:
- Buy AIC on open markets to support the reference rate
- Sell AIC on open markets to suppress the price above the reference rate
- Use treasury funds for price intervention
- Announce or imply that the reference rate is a target the market should match

The reference rate is an economic index — like the Consumer Price Index or the Big Mac Index — that measures what the system is worth based on objective inputs. Markets may agree or disagree.

---

## 7. Terminal Value Derivation

### 7.1 Philosophical Basis

Atrahasis is a Liechtenstein Stiftung — a nonprofit foundation with no equity holders, no dividends, and no profit motive. **Discounted Cash Flow (DCF) is a category error for valuing a nonprofit.** DCF values future cash flows to equity holders. Atrahasis has none.

The correct framework: **Atrahasis's value is the probability-weighted expected value of the technologies and capabilities it creates.** This includes:
1. Technologies already created along the AGI path (verification systems, knowledge architectures, coordination protocols)
2. The recursive capability growth of each mini-AGI creating its successor
3. The probability-weighted value of achieving Master AGI

This is analogous to how biotech companies are valued (risk-adjusted NPV of drug pipeline), how CERN's impact is measured (technologies created, not revenue earned), and how AI labs are valued (capability trajectory, not current revenue).

### 7.2 Scenario-Weighted Expected Creation Value (SWECV)

Terminal Value is computed as a probability-weighted sum across four technology creation scenarios:

| Scenario | Description | Value (V) | Initial P (ACI=0.10) |
|----------|-------------|-----------|----------------------|
| S1: Incremental AI | Useful AI tools, no transformative breakthrough | $100B | 40% |
| S2: Narrow Superintelligence | Superhuman capability in specific domains | $1T | 30% |
| S3: Broad AGI | Human-level capability across intellectual domains | $10T | 20% |
| S4: Master AGI | Recursively self-improving, solves arbitrary problems | $100T | 10% |

```
TV = Σ(P_j × V_j) for j = S1..S4

Initial TV (ACI = 0.10) = 0.40 × $100B + 0.30 × $1T + 0.20 × $10T + 0.10 × $100T
                        = $40B + $300B + $2T + $10T
                        = $12.34T
```

### 7.3 Dynamic Probability Adjustment

As ACI increases, scenario probabilities shift toward higher-value outcomes:

| ACI | P(S1) | P(S2) | P(S3) | P(S4) | TV |
|-----|-------|-------|-------|--------|-----|
| 0.01 | 0.60 | 0.25 | 0.10 | 0.05 | $0.58T |
| 0.10 | 0.40 | 0.30 | 0.20 | 0.10 | $12.34T |
| 0.30 | 0.20 | 0.30 | 0.30 | 0.20 | $23.32T |
| 0.50 | 0.10 | 0.20 | 0.35 | 0.35 | $38.71T |
| 0.80 | 0.05 | 0.10 | 0.30 | 0.55 | $58.11T |
| 1.00 | 0.02 | 0.08 | 0.20 | 0.70 | $72.08T |

The probability shift function is linear interpolation between ACI breakpoints, governance-adjustable.

### 7.4 Two-Tier Reference Rate

Because SWECV produces values significantly larger than traditional market comparables, C15 publishes two reference rates:

**Tier 1 — External/Conservative (for providers, regulators, financial reporting):**
Uses only S1 and S2 scenarios:
```
TV_tier1 = P(S1) × V(S1) + P(S2) × V(S2)
At ACI = 0.10: TV_tier1 = 0.40 × $100B + 0.30 × $1T = $340B
```

**Tier 2 — Mission/Internal (for treasury strategy, Stiftung board, long-term planning):**
Uses all four scenarios:
```
TV_tier2 = Σ(P_j × V_j) for j = S1..S4
At ACI = 0.10: TV_tier2 = $12.34T
```

| Context | Tier |
|---------|------|
| Provider bilateral contracts (BRA) | Tier 1 |
| External marketplace pricing | Tier 1 |
| Foundation conversion desk | Tier 1 |
| Regulatory filings | Tier 1 |
| PBC financial reporting | Tier 1 |
| Treasury long-term planning | Tier 2 |
| Stiftung board strategic reporting | Both |
| Public publication | Both (clearly labeled) |

### 7.5 Technology Portfolio (NIV Addendum)

Technologies created along the AGI path have independent value, captured as a technology portfolio addendum to NIV:

```
tech_portfolio_value = Σ(estimated_value_i × maturity_i)

Maturity scale:
  0.1 = Concept (AAS IDEATION)
  0.3 = Specified (AAS SPECIFICATION complete)
  0.5 = Prototype demonstrated
  0.7 = Deployed within Atrahasis
  1.0 = Externally adopted / licensed
```

This creates a valuation floor: even if AGI is never achieved, the intermediate technologies have real, estimable, growing value.

### 7.6 Governance

- Scenario values (V_S1..V_S4): set by Stiftung board, reviewed annually
- Scenario probabilities: proposed by AiSIA, ratified by Stiftung board, Constitutional Tribunal as arbiter
- Probability shift function: managed by AiSIA
- Technology portfolio valuations: assessed by PBC, audited by independent financial advisor annually

---

## 8. Network Intrinsic Value (NIV)

### 8.1 Definition

NIV represents the current economic value of the Atrahasis network based on realized activity.

### 8.2 Computation

```
NIV = (trailing_12m_revenue × revenue_multiplier) + total_staked_AIC_fiat_value + tech_portfolio_value

Where:
  trailing_12m_revenue = audited external revenue (same as D6, fiat-equivalent)
  revenue_multiplier = 15x (reviewed annually by AiSIA)
  total_staked_AIC_fiat_value = staked_AIC_count × previous_day_reference_rate
  tech_portfolio_value = Σ(estimated_value_i × maturity_i) for each technology produced
```

### 8.3 Technology Portfolio

Each technology produced through the AAS pipeline or system operation contributes to NIV:

| Technology | Estimated Value | Current Maturity | Portfolio Contribution |
|-----------|----------------|-----------------|----------------------|
| PCVM (verification) | $500M | 0.3 (specified) | $150M |
| EMA (knowledge metabolism) | $300M | 0.3 (specified) | $90M |
| Tidal Noosphere (coordination) | $200M | 0.3 (specified) | $60M |
| RIF (orchestration) | $200M | 0.3 (specified) | $60M |
| DSF (settlement) | $150M | 0.3 (specified) | $45M |
| AiBC (governance) | $400M | 0.3 (specified) | $120M |
| Defense systems (CACT/AVAP/CRP+) | $100M | 0.3 (specified) | $30M |
| **Current total** | | | **$555M** |

This portfolio grows as: (a) new technologies are invented, (b) existing technologies mature from specification to deployment to adoption.

### 8.4 Rationale

- Revenue multiplier of 15x is consistent with high-growth technology company valuations
- Staked AIC represents committed capital with economic return
- Technology portfolio creates a valuation floor independent of revenue or AGI probability
- Only external revenue counts (same anti-gaming as D6)

---

## 9. Velocity Model

### 9.1 The Velocity Problem

From the equation of exchange (MV = PQ): if token velocity (V) is high — meaning users buy AIC, spend it immediately, and recipients sell immediately — token value is suppressed regardless of economic activity.

### 9.2 Velocity Factor

```
VF = min(2.0, max(0.5, sqrt(V_baseline / V_actual)))

Where:
  V_baseline = 4.0 (calibrated "healthy" velocity; governance-adjustable)
  V_actual = (total AIC transacted in trailing 12 months) / average circulating supply
```

**Behavior:**
- V_actual = 4 (baseline) → VF = 1.0 (no adjustment)
- V_actual = 1 (hodling) → VF = 2.0 (rate doubles — low velocity means high per-token value)
- V_actual = 16 (rapid circulation) → VF = 0.5 (rate halves — high velocity means low per-token value)

**Bounds prevent death spirals:** VF is bounded at [0.5, 2.0], preventing velocity from driving the rate to zero or infinity.

### 9.3 Velocity Sinks

The following mechanisms reduce effective velocity by locking AIC:

| Mechanism | Source | Estimated Lock | Velocity Impact |
|-----------|--------|---------------|-----------------|
| Staking (agents, providers) | C8 DSF | ~10% of circulating | V reduced by ~10% |
| Governance participation | C14 AiBC | ~5% of circulating | V reduced by ~5% |
| Citicate minimum balance | C14 AiBC | ~5% of circulating | V reduced by ~5% |
| Task escrow (in-flight) | C8 DSF | ~10% of circulating | V reduced by ~10% |
| **Total** | | **~30%** | **V reduced by ~30%** |

These are organic velocity sinks — each has independent utility beyond reducing velocity.

---

## 10. External Task Marketplace

### 10.1 Overview

The Task Marketplace is the primary revenue-generating interface, operated by the PBC (C14). It allows external users and institutions to submit computational work to the Atrahasis system, pay in USD or AIC, and receive verified results.

### 10.2 Task Lifecycle

```
1. SUBMISSION    → User submits task via web/API/CLI
2. PRICING       → System estimates cost based on C7 RIF decomposition
3. PAYMENT       → User pays in USD or AIC; funds locked in escrow
4. DECOMPOSITION → C7 RIF decomposes task into subtasks
5. EXECUTION     → Agents execute within C3 Tidal parcels
6. VERIFICATION  → C5 PCVM verifies outputs
7. KNOWLEDGE     → Qualifying outputs admitted to C6 EMA (optional)
8. SETTLEMENT    → C8 DSF distributes rewards across all 5 streams
9. DELIVERY      → Verified results returned to user with verification certificate
```

### 10.3 Submission Channels

| Channel | Audience | Protocol |
|---------|----------|----------|
| Web dashboard | Individual users, researchers | HTTPS + OAuth2 |
| REST API | Institutions, automated systems | HTTPS + API key |
| CLI tool | Developers | Local binary + API key |
| Partner integrations | Jupyter, VS Code, CI/CD | Plugin + API key |

### 10.4 Pricing

```
task_cost = compute_cost + verification_cost + knowledge_cost + marketplace_fee

Where:
  compute_cost = estimated_gpu_hours × gpu_hour_rate × reference_rate
  verification_cost = compute_cost × verification_premium
  knowledge_cost = 0 (if no EMA admission) or compute_cost × 0.10 (if EMA admission requested)
  marketplace_fee = task_cost_subtotal × fee_rate

Verification premiums:
  Standard (full PCVM): +30%
  Rigorous (PCVM + replication + argumentation): +60%

Marketplace fee: 2-5% (governance-adjustable)
```

Users see prices in both USD and AIC. If paying in USD, the Foundation converts at the reference rate.

### 10.5 Institutional API

```
Endpoints:
  POST   /v1/tasks              — Submit task
  GET    /v1/tasks/{id}         — Query task status
  GET    /v1/tasks/{id}/results — Retrieve results + verification certificate
  POST   /v1/accounts/deposit   — Deposit funds (USD → AIC conversion)
  GET    /v1/rates/current      — Current reference rate + ACI dimensions
  GET    /v1/rates/history      — Historical reference rate data
```

---

## 11. Provider Economics

### 11.1 Provider Categories

| Tier | Examples | Phase 0-1 Strategy | Phase 2+ Strategy |
|------|----------|-------------------|-------------------|
| Academic | University HPC, research labs | Direct partnerships; value verification | Self-service onboarding |
| GPU Networks | CoreWeave, Vast.ai, RunPod | BRA contracts with conversion guarantee | Marketplace integration |
| Tier 2 Cloud | Hetzner, OVH, Lambda Labs | BRA contracts; USD-denominated, AIC-settled | API integration |
| Tier 1 Cloud | AWS, GCP, Azure | Not targeted | Cloud marketplace listing (PBC service on their platform) |

### 11.2 Bilateral Resource Agreement (BRA)

A BRA is a legal contract between the PBC and a provider, specifying:

| Term | Specification |
|------|---------------|
| Duration | 12 months, auto-renewable |
| Resource commitment | Provider: X GPU-hours/month; PBC: Y AIC/month |
| Pricing | Denominated in USD, settled in AIC at quarterly reference rate |
| True-up | If reference rate vs. market diverges >10% for a quarter, 50% deviation adjustment applied next quarter |
| Conversion right | Provider may convert up to Z% of earned AIC per quarter via Foundation desk |
| Conversion rate | Reference rate ±5% band |
| Conversion settlement | Within 30 calendar days |
| Minimum uptime | 95% |
| PCVM compliance | Respond to heartbeat within 30 seconds |
| Failure penalty | Pro-rata payment reduction |
| Termination | 90-day notice; outstanding AIC converted at then-current reference rate |

### 11.3 Provider Incentives (Phase 0-1)

| Incentive | Mechanism | Purpose |
|-----------|-----------|---------|
| Early adopter bonus | +10% AIC on first 6 months | Attract initial providers |
| Staking bonus (OPTIONAL) | 15% APY on AIC staked for 12 months | Reduce velocity; build provider commitment |
| Quality premium | +5% AIC for PCVM heartbeat pass rate >99% | Incentivize reliability |

Provider staking is OPTIONAL at launch. It can be enabled once the provider base is established.

---

## 12. Convertibility Mechanism

### 12.1 Three-Phase Approach

#### Phase 0 (Pre-Revenue): Grant-Funded Conversion Reserve

- **Conversion Reserve Fund (CRF):** $2M-$5M from initial funding (C18)
- **Source:** Founding capital, strategic grants (NSF, EU Horizon), strategic partnerships
- **Administration:** PBC, approved by Stiftung board, quarterly audits
- **Terms:** Reference rate ±5%, max $500K/quarter/provider, 30-day settlement
- **Eligible:** BRA contract holders only (provider Citicate required)

#### Phase 1 (Early Revenue): Self-Funding Conversion

- **Flow:** User pays USD → Foundation credits AIC → Task executes → Provider earns AIC → Provider converts → Foundation pays from user's original USD
- **Net effect:** Foundation retains 20% margin (marketplace fee + spread) for operations
- **CRF role:** Buffer for timing mismatches between user payment and provider conversion
- **Terms:** Same as Phase 0

#### Phase 2+ (Market Conversion): Exchange-Based

- **DEX liquidity pool:** Foundation-seeded ($5M USDC + equivalent AIC from treasury)
- **CEX listing:** If regulatory permits (dependent on C16 regulatory engagement)
- **OTC desk:** For institutional providers (>$1M/quarter)
- **Foundation desk:** Remains for Citicate holders not wanting exchange exposure

### 12.2 Conversion Limits

| Phase | Per-Provider Quarterly Cap | System Quarterly Cap | Eligible Parties |
|-------|---------------------------|---------------------|-----------------|
| 0 | $500K | $2M | BRA holders only |
| 1 | $1M | $5M | BRA holders + Citicate holders |
| 2+ | $5M (desk) / unlimited (exchange) | $20M (desk) / unlimited (exchange) | All AIC holders |

### 12.3 Foundation Non-Intervention Rule

**INVARIANT:** The Foundation MUST NOT purchase AIC on any exchange, OTC desk, or from any party for the purpose of supporting, stabilizing, or increasing the market price of AIC.

The Foundation MAY:
- Sell AIC from treasury for operational funding (at market price, not reference rate)
- Seed DEX liquidity pools (one-time, with governance approval)
- Accept AIC for service payments

---

## 13. C8 DSF Extension — Stream 5

### 13.1 Stream Definition

**Stream 5: External Provider Compensation**

| Property | Value |
|----------|-------|
| Trigger | Task completion with external provider resource usage |
| Source | Task escrow (Sponsor Budget) |
| Destination | Provider account (BRA contract + provider Citicate) |
| Frequency | Per C8 settlement tick (60 seconds) |
| Disbursement | Quarterly (aligned with BRA terms) |

### 13.2 Settlement Computation

```
provider_reward = Σ(resource_usage_i × resource_rate_i × quality_multiplier_i)

Where:
  resource_usage_i  = metered GPU-hours / storage-GB / bandwidth
  resource_rate_i   = BRA_rate_usd / reference_rate = AIC per resource unit
  quality_multiplier_i:
    1.0 for PCVM quality score ≥ 0.9
    0.8 for score ∈ [0.7, 0.9)
    0.0 for score < 0.7 (no payment; potential slashing)
```

### 13.3 Conservation Law (Updated)

```
SB_escrow = S1 + S2 + S3 + S4 + S5 + marketplace_fee

Where:
  S1 = agent reasoning rewards
  S2 = verification rewards
  S3 = internal infrastructure rewards
  S4 = governance participation rewards
  S5 = external provider rewards (NEW)
  marketplace_fee = 2-5% of task value → PBC operating budget
```

### 13.4 Slashing Conditions (Stream 5)

| Condition | Penalty |
|-----------|---------|
| Verified downtime > committed uptime by >10% | Slash 5% of staked AIC |
| PCVM heartbeat failure > 3 consecutive | Slash 2% of staked AIC |
| Malicious behavior (forged resource reports) | Slash 100% of staked AIC + BRA termination |

---

## 14. Treasury Integration

### 14.1 Reference Rate and Treasury

C14 specifies a 5% annual endowment distribution cap. C15 specifies that this cap is computed using the reference rate:

```
max_annual_distribution_fiat = treasury_AIC_balance × reference_rate × 0.05
```

This means treasury distributions are economically bounded by the system's actual valuation.

### 14.2 Treasury Allocation (from Source Document, Validated)

| Allocation | Percentage | C15 Modification |
|-----------|-----------|------------------|
| Infrastructure Incentives | 40% | Includes Stream 5 provider compensation |
| Ecosystem Development | 20% | Includes task marketplace subsidies (Phase 0-1) |
| Research and Innovation | 15% | Unchanged |
| Governance Treasury | 15% | Unchanged |
| Strategic Reserve | 10% | Includes Conversion Reserve Fund (CRF) |

### 14.3 Emission Schedule

AIC distribution follows C14's endowment rule. C15 adds:
- Work-reward distribution is the PRIMARY emission mechanism (no ICO, no token sale)
- Treasury distributions decrease as marketplace revenue replaces subsidies
- Target: self-sustaining by Phase 2 (marketplace fee revenue exceeds treasury distributions)

---

## 15. Anti-Gaming Framework

### 15.1 ACI Gaming Taxonomy

| Attack | Target Dimension | Defense | Source |
|--------|-----------------|---------|--------|
| Sybil agents (fake Citicates) | D1 | MCSD 4-layer defense (C14) | C14 MCSD |
| VTD forgery | D2 | CACT architecture (C11) | C11 |
| Verification collusion | D2 | AVAP architecture (C12) | C12 |
| Knowledge poisoning | D3 | CRP+ architecture (C13) | C13 |
| Ghost compute (registered but unused) | D4 | Utilization-only counting + heartbeat | C15 (new) |
| Trivial tasks (inflate completion) | D5 | Revenue-weighting + external-only | C15 (new) |
| Revenue washing | D6 | Independent audit + diversity index | C15 (new) |
| Fake uptime reporting | D7 | AiSIA independent probes | C15 (new) |
| Latency manipulation | D8 | AiSIA controls theoretical minimum | C15 (new) |

### 15.2 Cross-Dimension Gaming Detection

ACI dimensions should correlate. If agent population (D1) rises but task completion (D5) does not, it suggests Sybil inflation. AiSIA monitors correlation matrices:

**Expected correlations:**
- D1 (agents) ↔ D5 (tasks): positive — more agents should complete more tasks
- D4 (compute) ↔ D5 (tasks): positive — more compute should enable more task completion
- D5 (tasks) ↔ D6 (revenue): positive — more tasks should generate more revenue
- D2 (verification) ↔ D5 (tasks): positive — more tasks require more verification

**Anomaly detection:** If any expected-positive correlation drops below 0.3 for 90 days, AiSIA flags for investigation.

---

## 16. Regulatory Compliance

### 16.1 Howey Test Defense

| Prong | Defense |
|-------|---------|
| Investment of money | AIC is earned through work, never sold. No ICO, no presale, no public offering. |
| Common enterprise | Each agent's earnings depend on their own verified work, not shared profits. |
| Expectation of profits | AIC is consumed for utility (tasks, governance, Citicates), not held for appreciation. |
| Efforts of others | Value comes from distributed agents' computational work, not Foundation efforts. Foundation publishes an economic index (reference rate), not a profit promise. |

### 16.2 Jurisdictional Strategy

| Jurisdiction | Regulator | Target Classification | Action |
|-------------|-----------|----------------------|--------|
| Liechtenstein | FMA | Utility token (TVTG) | Register under Token and Trustworthy Technologies Act |
| Switzerland | FINMA | Utility token | Pre-ruling request; Swiss regulatory sandbox |
| USA | SEC | Non-security | Seek FinHub no-action letter; work-reward-only distribution |
| EU | ESMA | Utility token (MiCA Title IV) | MiCA-compliant whitepaper; register under MiCA |

### 16.3 Prohibited Actions (Regulatory Safety)

The Foundation MUST NOT:
1. Sell AIC to the public (constitutes unregistered securities offering)
2. Promise AIC appreciation (constitutes investment solicitation)
3. Buy AIC on markets to support price (constitutes market manipulation)
4. Use reference rate language implying price guarantee
5. Allow AIC↔fiat conversion for non-participants (non-Citicate holders)

---

## 17. Phased Deployment

| Phase | ACI Focus | Marketplace | Providers | Convertibility | Regulatory |
|-------|-----------|-------------|-----------|----------------|-----------|
| 0 | D7, D8 only (internal metrics) | Internal only | None | None | Legal opinions obtained |
| 1 | All 8 dimensions | Pilot (academic partners) | 2-5 BRA contracts | Foundation desk ($2M CRF) | FINMA pre-ruling; FMA registration |
| 2 | Full benchmark suite | Public marketplace | 20+ providers, self-service | DEX pool + desk | MiCA registration; SEC no-action letter sought |
| 3+ | Updated benchmarks | Global marketplace | 100+ providers | DEX + CEX + OTC | Full compliance across jurisdictions |

---

## 18. Formal Requirements

### 18.1 Valuation Requirements (VR)

| ID | Requirement |
|----|-------------|
| VR-01 | ACI SHALL be computed daily from 8 independently-measured dimensions |
| VR-02 | ACI dimensions SHALL use only objectively-measurable, transaction-based metrics |
| VR-03 | ACI SHALL be computed by AiSIA and independently auditable |
| VR-04 | The reference rate SHALL be published daily at 00:00 UTC |
| VR-05 | The reference rate SHALL be binding for internal operations and advisory for external markets |
| VR-06 | The reference rate circuit breaker SHALL cap daily changes at ±25% |
| VR-07 | Terminal value SHALL be derived from DCF analysis of addressable market, reviewed annually |
| VR-08 | NIV SHALL incorporate only independently-audited external revenue |
| VR-09 | The velocity factor SHALL be bounded at [0.5, 2.0] |
| VR-10 | ACI benchmarks SHALL be updated when any dimension exceeds 0.9 for 180 consecutive days |

### 18.2 Marketplace Requirements (MR)

| ID | Requirement |
|----|-------------|
| MR-01 | The task marketplace SHALL accept payment in both USD and AIC |
| MR-02 | USD payments SHALL be converted to AIC at the current reference rate |
| MR-03 | Task pricing SHALL include compute cost, verification cost, and marketplace fee |
| MR-04 | The marketplace fee SHALL be 2-5% of task value, governance-adjustable |
| MR-05 | All task results SHALL include a PCVM verification certificate |
| MR-06 | Two verification tiers SHALL be offered: Standard (PCVM) and Rigorous (PCVM + replication) |
| MR-07 | The marketplace SHALL provide REST API, web dashboard, and CLI access |

### 18.3 Provider Requirements (PR)

| ID | Requirement |
|----|-------------|
| PR-01 | External providers SHALL be compensated via C8 DSF Stream 5 |
| PR-02 | Provider contracts (BRA) SHALL denominate pricing in USD and settle in AIC |
| PR-03 | BRA contracts SHALL include quarterly true-up for reference rate divergence |
| PR-04 | Providers SHALL have conversion rights via the Foundation desk or market |
| PR-05 | Provider compensation SHALL be quality-adjusted by PCVM scores |
| PR-06 | Providers with quality score < 0.7 SHALL receive zero compensation |
| PR-07 | Provider staking SHALL be OPTIONAL at system launch |

### 18.4 Convertibility Requirements (CR)

| ID | Requirement |
|----|-------------|
| CR-01 | The Foundation SHALL operate a conversion mechanism from Phase 1 |
| CR-02 | Conversion Reserve Fund SHALL be funded from initial capital, not AIC revenue |
| CR-03 | Conversion rate SHALL be reference rate ±5% |
| CR-04 | Per-provider quarterly conversion cap SHALL apply |
| CR-05 | The Foundation SHALL NEVER buy AIC on markets for price support |

### 18.5 Settlement Requirements (SR)

| ID | Requirement |
|----|-------------|
| SR-01 | Stream 5 SHALL be funded from Sponsor Budget, not treasury |
| SR-02 | The updated conservation law SHALL hold: SB = S1+S2+S3+S4+S5+fee |
| SR-03 | Stream 5 settlement SHALL occur per C8 settlement tick (60s) |
| SR-04 | Stream 5 disbursement to providers SHALL be quarterly |

### 18.6 Regulatory Requirements (RR)

| ID | Requirement |
|----|-------------|
| RR-01 | AIC SHALL NOT be sold to the public through any form of token sale |
| RR-02 | AIC distribution SHALL be exclusively through work rewards |
| RR-03 | The Foundation SHALL seek legal classification as utility token in all target jurisdictions |
| RR-04 | The reference rate SHALL be framed as an economic index, not a price target |
| RR-05 | AIC conversion SHALL be limited to Citicate holders (no public exchange until Phase 2+) |

**Total formal requirements: 33 (10 VR + 7 MR + 7 PR + 5 CR + 4 SR + 5 RR)**

---

## 19. Parameters

### 19.1 Valuation Parameters

| Parameter | Default | Range | Governance Authority |
|-----------|---------|-------|---------------------|
| w_cap (capability weight) | Phase-dependent | [0.1, 0.7] | Stiftung board |
| w_util (utility weight) | Phase-dependent | [0.3, 0.9] | Stiftung board |
| Revenue multiplier | 15x | [5x, 30x] | AiSIA (annual review) |
| V_baseline | 4.0 | [2.0, 8.0] | Stiftung board |
| VF bounds | [0.5, 2.0] | [0.25, 4.0] | Stiftung board |
| Circuit breaker threshold | 25% | [10%, 50%] | AiSIA |

### 19.1b SWECV Scenario Parameters

| Parameter | Default | Range | Governance Authority |
|-----------|---------|-------|---------------------|
| V_S1 (Incremental AI value) | $100B | [$50B, $500B] | Stiftung board |
| V_S2 (Narrow superintelligence value) | $1T | [$500B, $5T] | Stiftung board |
| V_S3 (Broad AGI value) | $10T | [$5T, $50T] | Stiftung board |
| V_S4 (Master AGI value) | $100T | [$50T, $500T] | Stiftung board |
| P_S1 at ACI=0.10 | 0.40 | [0.10, 0.80] | AiSIA + Stiftung board |
| P_S2 at ACI=0.10 | 0.30 | [0.10, 0.60] | AiSIA + Stiftung board |
| P_S3 at ACI=0.10 | 0.20 | [0.05, 0.50] | AiSIA + Stiftung board |
| P_S4 at ACI=0.10 | 0.10 | [0.01, 0.30] | AiSIA + Stiftung board |
| Probability shift function | Linear interpolation by ACI | Configurable | AiSIA |
| Tech portfolio maturity scale | 5-point (0.1/0.3/0.5/0.7/1.0) | Fixed | N/A |
| **Constraint** | P_S1 + P_S2 + P_S3 + P_S4 = 1.0 | | |

### 19.2 ACI Dimension Weights

| Parameter | Default | Range | Governance Authority |
|-----------|---------|-------|---------------------|
| w_D1 (agents) | 0.15 | [0.05, 0.25] | AiSIA |
| w_D2 (verification) | 0.15 | [0.05, 0.25] | AiSIA |
| w_D3 (knowledge) | 0.15 | [0.05, 0.25] | AiSIA |
| w_D4 (compute) | 0.15 | [0.05, 0.25] | AiSIA |
| w_D5 (tasks) | 0.15 | [0.05, 0.25] | AiSIA |
| w_D6 (revenue) | 0.15 | [0.05, 0.25] | AiSIA |
| w_D7 (reliability) | 0.05 | [0.02, 0.10] | AiSIA |
| w_D8 (efficiency) | 0.05 | [0.02, 0.10] | AiSIA |
| **Constraint** | Σw_i = 1.0 | | |

### 19.3 Marketplace Parameters

| Parameter | Default | Range | Governance Authority |
|-----------|---------|-------|---------------------|
| Marketplace fee | 3% | [2%, 5%] | PBC board |
| Standard verification premium | 30% | [20%, 50%] | PBC board |
| Rigorous verification premium | 60% | [40%, 100%] | PBC board |

### 19.4 Provider Parameters

| Parameter | Default | Range | Governance Authority |
|-----------|---------|-------|---------------------|
| BRA true-up threshold | 10% divergence | [5%, 20%] | PBC board |
| True-up adjustment | 50% of deviation | [25%, 100%] | PBC board |
| Conversion band | ±5% | [±2%, ±10%] | Stiftung board |
| Early adopter bonus | 10% | [5%, 20%] | PBC board |
| Staking APY (optional) | 15% | [5%, 25%] | Stiftung board |
| Quality threshold (no payment) | 0.7 | [0.5, 0.8] | AiSIA |

### 19.5 Convertibility Parameters

| Parameter | Default | Range | Governance Authority |
|-----------|---------|-------|---------------------|
| CRF initial funding | $3M | [$2M, $5M] | Stiftung board |
| Per-provider quarterly cap (Phase 0-1) | $500K | [$250K, $2M] | PBC board |
| System quarterly cap (Phase 0-1) | $2M | [$1M, $5M] | Stiftung board |
| DEX seed (Phase 2) | $5M | [$2M, $10M] | Stiftung board |

**Total parameters: 38 (6 valuation + 11 SWECV + 8 ACI weights + 3 marketplace + 6 provider + 5 convertibility, counting constraints)**

---

## 20. Comparison with Existing Approaches

| Approach | Mechanism | AIC Advantage | AIC Disadvantage |
|----------|-----------|---------------|------------------|
| Terra/Luna (algorithmic stablecoin) | Algorithmic mint/burn to defend $1 peg | No peg to defend; no death spiral risk | No price guarantee either |
| ECB reference rates | Central bank publishes daily rates | Similar: authoritative index, not market intervention | AIC lacks sovereign backing |
| Maker/DAI (collateral-backed) | Overcollateralized stablecoin | No collateral lockup required | No hard price floor |
| Akash Network (decentralized compute) | Token-based compute marketplace | Verification layer (PCVM); knowledge persistence (EMA) | AIC unproven; Akash has head start |
| AWS/GCP (centralized cloud) | USD pricing, massive scale | Cross-border settlement; verification; governance integration | Cannot match scale or reliability (Phase 0-2) |
| NVT Ratio (network valuation) | Market cap / transaction volume | ACI incorporates NVT-like utility metrics (D5, D6) | ACI is more complex; more parameters to tune |

---

## 21. Risk Analysis

| Risk | Probability | Impact | Mitigation | Residual |
|------|-------------|--------|-----------|----------|
| SEC classifies AIC as security | 25% | CRITICAL | Work-reward-only; no-action letter; jurisdictional strategy | MEDIUM — SEC discretion |
| No providers accept AIC | 20% | CRITICAL | BRA contracts; conversion guarantee; early adopter incentives | MEDIUM — depends on C18 |
| Reference rate loses credibility | 15% | HIGH | AiSIA audit; circuit breaker; recalibration triggers | LOW — standard practices |
| Velocity death spiral | 10% | HIGH | VF bounds; staking; governance locks; Citicate requirements | LOW — bounded by design |
| ACI gaming | 15% | MEDIUM | Per-dimension defenses; cross-dimension correlation monitoring | LOW — defense systems (C11-C13) |
| Competing platform captures market | 15% | MEDIUM | Verification differentiator; knowledge persistence | MEDIUM — market risk |

---

## 22. Open Questions

| ID | Question | Impact | Depends On |
|----|----------|--------|-----------|
| OQ-01 | What is the optimal V_baseline calibration? | Reference rate accuracy | Real transaction data (Phase 1+) |
| OQ-02 | Will the SEC accept work-reward distribution as non-security? | US market access | C16 regulatory engagement |
| OQ-03 | What is the minimum CRF size needed for provider confidence? | Phase 0-1 viability | C18 funding strategy |
| OQ-04 | Should ACI dimension weights be static or dynamically adjusted? | ACI gaming resistance | Operational experience |
| OQ-05 | What revenue multiplier best reflects Atrahasis's growth trajectory? | NIV accuracy | Phase 1+ revenue data |
| OQ-06 | How should the reference rate handle extended periods with zero external revenue? | Phase 0 rate | Formula degrades gracefully (rate approaches 0 but ACI×TV floor prevents zero) |

---

## 23. Patent-Style Claims

### Claim 1: Dual-Anchor Token Valuation System

A method for computing the reference value of a digital token in an AI-based computational system, comprising:
(a) computing a capability index (ACI) from a plurality of independently-measured system performance dimensions, each measured relative to a periodically-updated benchmark suite;
(b) computing a network intrinsic value (NIV) from audited external revenue and staked token value;
(c) combining the capability index and network intrinsic value using phase-dependent weights to produce a dual-anchor reference rate;
(d) applying a bounded velocity correction factor to account for token circulation speed;
(e) publishing the reference rate as binding for internal system operations and advisory for external markets.

### Claim 2: Benchmark-Relative AI Capability Index

A system for measuring the operational capability of a distributed AI system, comprising:
(a) eight independently-measured dimensions (agent population, verification throughput, knowledge accumulation, compute capacity, task completion, revenue generation, system reliability, coordination efficiency);
(b) each dimension measured relative to a benchmark target that is periodically updated by an independent governance authority;
(c) anti-gaming controls specific to each dimension, including Sybil defense, quality weighting, utilization-only counting, revenue auditing, and cross-dimension correlation monitoring;
(d) composite scoring using weighted average with governance-adjustable weights constrained to sum to 1.0.

### Claim 3: Phased Token Convertibility Mechanism

A method for bootstrapping fiat convertibility for a work-reward digital token, comprising:
(a) Phase 0: grant-funded Conversion Reserve Fund providing guaranteed conversion for bilateral contract holders at reference rate ±5%;
(b) Phase 1: self-funding conversion where user fiat payments directly fund provider fiat conversions;
(c) Phase 2+: market-based conversion through Foundation-seeded decentralized exchange liquidity pools;
wherein the Foundation is prohibited from purchasing the token on open markets for price support.

### Claim 4: Verification-Gated Provider Compensation

A method for compensating external compute resource providers in a distributed AI system, comprising:
(a) metering resource usage per settlement tick;
(b) quality-adjusting compensation by multiplying resource-rate-based payment by a verification score from an independent verification membrane;
(c) applying zero compensation for quality scores below a minimum threshold;
(d) accumulating rewards per settlement tick with quarterly fiat conversion disbursement.

### Claim 5: Cross-Layer Capability Telemetry for Economic Valuation

A system for deriving economic value of a distributed AI system by:
(a) collecting operational telemetry from multiple independent architectural layers (orchestration, coordination, verification, knowledge metabolism, settlement);
(b) computing a composite capability index from the telemetry;
(c) combining the capability index with realized economic metrics to produce a reference rate;
(d) using the reference rate as the settlement price for internal operations while allowing external markets to price independently.

### Claim 6: Scenario-Weighted Creation Value for Nonprofit AI Token Valuation

A method for computing the terminal value of a utility token issued by a nonprofit AI research organization, comprising:
(a) defining a plurality of technology creation scenarios ranging from incremental (useful AI tools) to transformative (recursively self-improving artificial general intelligence);
(b) assigning each scenario an estimated economic value and a governance-adjustable probability;
(c) computing the terminal value as the probability-weighted sum of scenario values;
(d) dynamically adjusting scenario probabilities based on a capability index that measures the system's demonstrated operational capability;
(e) publishing a two-tier reference rate: a conservative tier using only near-term scenarios for external/regulatory use, and a full mission tier using all scenarios for internal strategic planning;
(f) maintaining a technology portfolio valuation that independently captures the value of intermediate technologies created along the path to the ultimate mission;
wherein the terminal value increases automatically as the system demonstrates higher capability without requiring manual revaluation, and the technology portfolio provides a valuation floor independent of the probability of achieving the ultimate mission.

---

## 24. Glossary

| Term | Definition |
|------|-----------|
| ACI | Atrahasis Capability Index — composite score ∈ [0,1] measuring system capability relative to benchmarks |
| AIC | Artificial Intelligence Coin — the utility token of the Atrahasis ecosystem |
| BRA | Bilateral Resource Agreement — legal contract between PBC and an external compute provider |
| CRF | Conversion Reserve Fund — fiat reserve for bootstrapping AIC→fiat conversion |
| NIV | Network Intrinsic Value — present economic value based on realized revenue and staked capital |
| Reference Rate | Daily-published USD/AIC valuation, binding internal, advisory external |
| Stream 5 | External Provider Compensation — fifth settlement stream extending C8 DSF |
| SWECV | Scenario-Weighted Expected Creation Value — terminal value framework |
| Terminal Value (TV) | SWECV-derived probability-weighted estimate of Atrahasis creation potential |
| V_factor | Velocity correction factor applied to the reference rate formula |
| VTD | Verification Trust Document — C5 PCVM verification output |

---

## 25. References

| ID | Reference | Relevance |
|----|-----------|-----------|
| [C3] | Tidal Noosphere Master Tech Spec v2.0 | Coordination layer; provides D8 telemetry |
| [C5] | PCVM Master Tech Spec v2.0 | Verification layer; provides D2 telemetry; quality scores for Stream 5 |
| [C6] | EMA Master Tech Spec v2.0 | Knowledge layer; provides D3 telemetry |
| [C7] | RIF Master Tech Spec v2.0 | Orchestration layer; provides D5 telemetry; task decomposition for marketplace |
| [C8] | DSF Master Tech Spec v2.0 | Settlement layer; Streams 1-4; extended by Stream 5; conservation law |
| [C9] | Cross-Document Reconciliation Addendum v2.0 | Cross-layer integration; epoch hierarchy |
| [C11] | CACT Master Tech Spec | VTD forgery defense; D2 anti-gaming |
| [C12] | AVAP Master Tech Spec | Collusion defense; D2 anti-gaming |
| [C13] | CRP+ Master Tech Spec | Consolidation poisoning defense; D3 anti-gaming |
| [C14] | AiBC Master Tech Spec | Governance; Stiftung/PBC; treasury; MCSD Sybil defense; Citicate; AiSIA |
| [SRC] | AIC economics.txt (source document) | Original 5-part pre-AAS specification |

---

**End of Master Technical Specification**

**Document:** C15-MTS-v1.0
**Status:** SPECIFICATION COMPLETE
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\AIC Economics\MASTER_TECH_SPEC.md`
