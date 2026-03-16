# C37 — Epistemic Feedback Fabric (EFF)

## Master Technical Specification

**Document ID:** C37-MTS-v1.0
**Version:** 1.0.0
**Date:** 2026-03-12
**Invention ID:** C37
**Task ID:** T-067
**System:** Atrahasis Agent System v2.4
**Status:** SPECIFICATION COMPLETE
**Classification:** CONFIDENTIAL — BlakJaks LLC
**Assessment Council Verdict:** ADVANCE (Novelty 3/5, Feasibility 4/5, Impact 3.5/5, Risk 5/10 MEDIUM)
**Normative References:** C5 (PCVM v2.0), C6 (EMA v2.0), C7 (RIF v2.0), C9 (Reconciliation), C17 (MCSD L2 v1.0), C23 (SCR v1.0), C35 (Sentinel v1.0)
**Feasibility Conditions:** All 5 satisfied (see Section 3.3)

---

## Abstract

The Atrahasis Agent System verifies agent reasoning through C5 PCVM and settles economic consequences through C8 DSF, but it does not learn from its own verification data. The system has referees but no coaches. Verification outcomes — the richest signal the system produces about what reasoning works and what fails — flow to settlement and are then discarded. The Epistemic Feedback Fabric (EFF) closes this information lifecycle gap by aggregating C5 verification outcomes into population-level reasoning quality signals and publishing them as voluntary advisory information behind an explicit non-enforcement boundary called the Advisory Membrane. EFF introduces three components: a Verification Feedback Loop (VFL) that produces privacy-preserving per-claim-class quality metrics, a Reasoning Strategy Catalog (RSC) that publishes proven reasoning patterns as C6 epistemic quanta, and Complexity-Aware Budget Signals (CABS) that attach optional reasoning budget recommendations to C23 inference leases. The primary innovation is not any single component but the Advisory Membrane Pattern — a formalized architectural guarantee that no enforcement or surveillance mechanism in the Atrahasis stack may use advisory consumption data as input. This pattern has no close prior art in the multi-agent systems literature, where governance frameworks uniformly assume enforcement authority.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Background and Prior Art](#2-background-and-prior-art)
3. [Architecture Overview](#3-architecture-overview)
4. [Verification Feedback Loop (VFL)](#4-verification-feedback-loop-vfl)
5. [Reasoning Strategy Catalog (RSC)](#5-reasoning-strategy-catalog-rsc)
6. [Complexity-Aware Budget Signals (CABS)](#6-complexity-aware-budget-signals-cabs)
7. [Advisory Membrane](#7-advisory-membrane)
8. [Integration Contracts](#8-integration-contracts)
9. [Parameters](#9-parameters)
10. [Implementation](#10-implementation)
11. [Risk Analysis](#11-risk-analysis)
12. [Open Questions](#12-open-questions)
13. [Patent-Style Claims](#13-patent-style-claims)
14. [Comparison with Existing Approaches](#14-comparison-with-existing-approaches)
15. [Conclusion](#15-conclusion)

---

## 1. Introduction

### 1.1 Problem Statement

The Atrahasis Agent System processes claims from sovereign AI agents through a six-layer architecture: RIF orchestrates (C7), the Tidal Noosphere coordinates (C3), PCVM verifies (C5), EMA metabolizes knowledge (C6), DSF settles economics (C8), and the Alternative C sovereign communication stack provides canonical message, security, and integration contracts (C38-C42, T-290 AXIP-v1). Cross-layer consistency is maintained by C9 reconciliation. Sybil defense is provided by MCSD (C14/C17). Anomaly detection is provided by Sentinel (C35). Inference metering is provided by SCR (C23).

This architecture has a gap. When C5 PCVM rejects a claim, the rejection triggers an economic consequence through C8 settlement — the agent loses its stake. But the *reason* for the rejection, the *pattern* of rejections across the population, and the *strategies* that correlate with verification success are all discarded after settlement. The system remembers what it penalized but not what it learned.

Consider the analogy to a legal system that has courts (C5) and treasuries (C8) but no published case law, no bar association guidelines, and no sentencing statistics. Each case is decided in isolation. Judges have access to precedent through their own experience, but the system as a whole does not learn from the aggregate pattern of its decisions. New judges start from scratch.

The Atrahasis system has referees but no coaches.

### 1.2 Motivation

Three specific consequences follow from this gap:

**Information waste.** C5 PCVM produces the system's most valuable signal about reasoning quality — Verification Trust Documents (VTDs) graded across 9 canonical claim classes with detailed verdicts. This data could reveal which reasoning strategies succeed, which fail, and how much reasoning effort is actually needed for each problem class. Instead, it flows to settlement and disappears.

**Cold-start penalty.** New agents entering the system have no mechanism to learn from the population's accumulated experience. They reason from scratch, fail at rates consistent with inexperience, and incur unnecessary economic costs during their learning period. There is no institutional memory.

**Reasoning cost inefficiency.** C23 SCR meters inference resources, but neither agents nor the system have empirically grounded data about how much reasoning effort is *useful* for a given problem class. Without this data, agents either over-invest (wasting AIC) or under-invest (producing rejectable claims). Literature suggests that complexity-aware budget allocation can reduce inference costs by 20-40% while maintaining quality.

### 1.3 Scope and Constraints

EFF is an information service. It is explicitly NOT:

- **Load-bearing infrastructure.** The system functions without EFF. Agents reason, C5 verifies, C8 settles. EFF improves efficiency and quality but is not on any critical path.
- **Prescriptive.** EFF does not tell agents how to reason, does not modify agent internals, and does not enforce adoption of its signals. This is forbidden by the sovereignty model.
- **A replacement for verification.** C5 PCVM remains the sole authority on claim validity. EFF's signals are derived from C5 outcomes but have no influence on C5 decisions.

EFF operates under one overriding constraint: the Advisory Membrane. No enforcement or surveillance system may use EFF advisory consumption data as input. This constraint is the primary patent differentiator and the architectural feature that distinguishes EFF from every prior art reference in the governance-of-AI-systems space.

### 1.4 Relationship to Existing Specifications

| Specification | Relationship |
|---|---|
| C5 PCVM | **Data source.** VFL consumes VTDs as a non-interfering second subscriber. |
| C6 EMA | **Storage.** RSC patterns are stored as EMA epistemic quanta. |
| C7 RIF | **Input.** CABS reads decomposition complexity from RIF Parcel Executor. |
| C8 DSF | **Parallel consumer.** VFL and DSF are independent VTD consumers. |
| C9 Reconciliation | **Input.** CABS reads claim class difficulty weights. EFF follows the three-tier epoch hierarchy. |
| C17 MCSD | **Constrained partner.** C17 receives RSC pattern whitelist (structural fingerprints only). C17 is prohibited from accessing consumption data. |
| C23 SCR | **Extension.** CABS adds an optional advisory field to ExecutionLease. |
| C35 Sentinel | **Excluded.** C35 is prohibited from accessing advisory consumption data. |

---

## 2. Background and Prior Art

### 2.1 The Coaching Gap in Multi-Agent Systems

The Atrahasis architecture is not alone in having referees without coaches. The broader multi-agent AI ecosystem — including AutoGen, CrewAI, LangGraph, and MetaGPT — provides orchestration, conversation management, and task decomposition but offers no mechanism for population-level reasoning quality feedback. Feedback in these systems is either per-session (conversation-level critique in AutoGen), per-task (code review in MetaGPT), or entirely absent.

The observability platforms — LangSmith, Weights & Biases Weave, Arize AI, Helicone — measure performance for human operators via dashboards, but none provide agent-facing advisory signals. They answer "how is my system performing?" for developers, not "what reasoning patterns are proving reliable?" for the agents themselves.

### 2.2 Key Prior Art

**Governance-as-a-Service (GaaS)** (arXiv:2508.18765, 2025). The closest prior art. GaaS provides a modular, policy-driven enforcement layer that regulates agent outputs at runtime without altering model internals. It uses declarative rules and a Trust Factor scoring mechanism. It is model-agnostic. The critical distinction: GaaS is an enforcement system — it blocks, redirects, and penalizes. EFF is an advisory system. GaaS has no verification feedback loop, no reasoning strategy catalog, no budget advisory signals, and fundamentally, no Advisory Membrane. Its entire purpose is enforcement.

**TALE: Token-Budget-Aware LLM Reasoning** (ACL 2025 Findings). Dynamically adjusts reasoning token budgets based on problem complexity, reducing costs by 67% while maintaining performance. Directly relevant to EFF's CABS component. The critical distinction: TALE operates at the individual model level via self-budgeting prompts. CABS operates at the population level using verification-outcome-derived signals attached to inference leases. TALE is prescriptive; CABS is advisory.

**SOFAI-LM: Metacognitive Architecture** (arXiv:2508.17959, 2025). A metacognitive module that monitors solver performance and dynamically selects the best solver. Provides iterative feedback with relevant examples. The critical distinction: SOFAI-LM is a single-system architecture where the metacognitive module controls solver selection. EFF operates across sovereign agents with no selection authority. SOFAI-LM's feedback is prescriptive; EFF's is advisory.

**Federated Learning** (Flower, PySyft, FATE). Privacy-preserving aggregation of distributed data is a well-studied problem. FL provides the technical toolkit (differential privacy, secure aggregation, homomorphic encryption) that VFL draws upon. The critical distinction: FL is inherently prescriptive — aggregated results update participant models. EFF publishes signals that agents voluntarily consume. FL modifies parameters; EFF publishes information. The sovereignty models are philosophically opposed.

### 2.3 The White Space

EFF occupies a position defined by four simultaneous requirements that no existing system satisfies:

1. **Post-hoc verification grounding.** Signals are derived from independent cryptographic verification outcomes (C5 VTDs), not from self-assessment, peer review, or human judgment.
2. **Population-level aggregation.** Signals reflect cross-agent statistical patterns, not per-session or per-task feedback.
3. **Advisory-only publication.** Signals are non-binding — unlike FL which auto-updates participants.
4. **Sovereignty guarantee.** Advisory consumption data is architecturally isolated from all enforcement mechanisms — no analog exists in any surveyed system.

### 2.4 Competitive Landscape Summary

| Domain | Players | Gap EFF Fills |
|---|---|---|
| Multi-agent frameworks | AutoGen, CrewAI, LangGraph, MetaGPT | No population-level verification feedback |
| AI observability | LangSmith, W&B, Arize, Helicone | Human-facing only; no agent-facing advisory |
| Reasoning optimization | OpenAI o3/o4-mini, Claude adaptive, TALE, AVA | Single-agent self-budgeting; no population data |
| Privacy aggregation | Flower, PySyft, FATE | Prescriptive (updates models); no sovereignty |
| AI governance | GaaS | Enforcement, not advisory |

The competitive moat derives from the integration of these domains under sovereignty constraints, not from novelty in any single component.

---

## 3. Architecture Overview

### 3.1 Architectural Position

EFF occupies a cross-layer advisory position within the Atrahasis stack. It is not load-bearing infrastructure — the system functions identically without it. EFF closes the information lifecycle loop: C5 PCVM verification outcomes currently flow only to C8 DSF for settlement. EFF adds a second consumer that distills verification data into population-level reasoning quality signals and makes them available as voluntary advisory information.

EFF does not verify claims (C5's role), does not prescribe agent internals (forbidden by the sovereignty model), and does not enforce adoption of its signals. It is an information service behind an explicit Advisory Membrane.

The analogy to clinical practice guidelines (CPGs) in medicine is precise. Medical CPGs are:
- Derived from aggregate outcome data (clinical trials, registry data)
- Published as advisory standards (not legally binding prescriptions)
- Consumed voluntarily by sovereign practitioners
- Updated as new evidence accumulates
- Not used as surveillance inputs (a physician's CPG reading habits are not monitored)

EFF provides CPGs for AI reasoning.

### 3.2 System Data Flow

```
                          ATRAHASIS CORE
 +--------------------------------------------------------------------+
 |                                                                    |
 |  +----------+          +----------+          +----------+         |
 |  | C7 RIF   |          | C5 PCVM  |          | C9 Recon |         |
 |  | (decomp  |          | (verify) |          | (claim   |         |
 |  |  complex)|          |          |          |  weights)|         |
 |  +----+-----+          +----+-----+          +----+-----+         |
 |       |                     |                     |                |
 |       |                     | VTD stream           |                |
 |       |                     | (second consumer)    |                |
 |       |                     v                     |                |
 |       |    +--------------------------------+     |                |
 |       |    |   VFL -- Verification           |     |                |
 |       |    |   Feedback Loop                 |     |                |
 |       |    |                                 |     |                |
 |       |    |  +---------+  +----------+     |     |                |
 |       |    |  |Anonymizer|  |Aggregator|     |     |                |
 |       |    |  | k=10 +   |->|Hierarchic|     |     |                |
 |       |    |  | DP noise |  |Bayesian  |     |     |                |
 |       |    |  +---------+  +----+-----+     |     |                |
 |       |    |                    |            |     |                |
 |       |    |  +-----------------v----------+ |     |                |
 |       |    |  | Per-Class Quality Metrics   | |     |                |
 |       |    |  | + Anomaly Detector         | |     |                |
 |       |    |  |   (chi-squared, p<0.01)    | |     |                |
 |       |    |  +--------+------------------+ |     |                |
 |       |    +-----------|--------------------+     |                |
 |       |                |                          |                |
 |       |         +------+-------+                  |                |
 |       |         |              |                  |                |
 |       |         v              v                  |                |
 |       |   +----------+  +----------+              |                |
 |       |   |   RSC    |  |  CABS    |<-------------+                |
 |       |   | Reasoning|  | Budget   |<--------------------+        |
 |       |   | Strategy |  | Advisory |                     |        |
 |       |   | Catalog  |  | Signals  |                     |        |
 |       |   | (in C6   |  +----+-----+                     |        |
 |       |   |  EMA)    |       |                            |        |
 |       |   +----+-----+       |                            |        |
 |       |        |             |                            |        |
 |       |        |             v                            |        |
 |       |        |      +----------+                       |        |
 |       |        |      | C23 SCR  |                       |        |
 |       |        |      | Exec     |                       |        |
 |       |        |      | Lease    |      +---------+      |        |
 |       |        |      | +optional|      | C7 RIF  |------+        |
 |       |        |      | advisory |      | decomp  |               |
 |       |        |      +----+-----+      |complexity|              |
 |       |        |           |            +---------+               |
 |  +----+--------+-----------+------------------------------+       |
 |  |    |  ADVISORY MEMBRANE (information flow boundary)    |       |
 |  |    |        |           |                              |       |
 |  |    |  published   optional                             |       |
 |  |    |  patterns    budget                               |       |
 |  |    |  (pull)      advisory                             |       |
 |  |    |        |     (push on lease)                      |       |
 |  +----+--------+-----------+------------------------------+       |
 |       |        |           |                                      |
 |       |        v           v                                      |
 |       |   +---------------------+                                 |
 |       |   |    SOVEREIGN AGENTS  |  consume voluntarily           |
 |       |   |    (black boxes)     |                                |
 |       |   +----------+----------+                                 |
 |       |              |                                            |
 |       |              | produce claims                             |
 |       |              v                                            |
 |       |        +----------+         +----------+                  |
 |       |        | C5 PCVM  |-------->| C8 DSF   |                  |
 |       |        | (verify) |         | (settle) |                  |
 |       |        +----------+         +----------+                  |
 |       |                                                           |
 |  +----+-------------------------------------------+               |
 |  |    |  DATA SEGREGATION BOUNDARY                |               |
 |  |    |                                           |               |
 |  |    |   RSC consumption   --X-->  C17 MCSD      |               |
 |  |    |   logs                      (no read      |               |
 |  |    |                              access)      |               |
 |  |    |   RSC consumption   --X-->  C35 Sentinel  |               |
 |  |    |   logs                      (no read      |               |
 |  |    |                              access)      |               |
 |  |    |                                           |               |
 |  |    |   RSC published     ------>  C17 MCSD     |               |
 |  |    |   patterns                  (whitelist    |               |
 |  |    |                              for B(a,a))  |               |
 |  +----+-------------------------------------------+               |
 |       |                                                           |
 +-------+-----------------------------------------------------------+
         |
    Feedback loop closes:
    better reasoning -> higher verification rates -> updated VFL metrics
```

The feedback loop is the core innovation. Verification outcomes flow upward through VFL into population-level statistics. Those statistics inform RSC pattern credibility and CABS budget recommendations. Agents optionally consume these signals, potentially improving their reasoning. Improved reasoning leads to better verification outcomes, closing the loop. The loop operates at population time-scales (hours, not seconds) — it is a statistical learning loop, not a real-time coaching channel.

### 3.3 Feasibility Condition Satisfaction

The FEASIBILITY review imposed five conditions for DESIGN advancement. All five are satisfied:

| # | Condition | Where Satisfied |
|---|---|---|
| 1 | RSC v1.0 restricted to declarative decompositions, anti-patterns, and checklists | Section 5.2 — three format types only |
| 2 | CABS must recommend (min, recommended, max) ranges with strategy labels | Section 6.2 — range format with confidence |
| 3 | Advisory Membrane must include RSC-aware baseline adjustment for C17 | Section 7.3 — whitelist protocol |
| 4 | Specification must explicitly acknowledge the voluntariness paradox | Section 7.4 |
| 5 | Pattern diversity monitoring must be specified | Section 5.6 |

### 3.4 Temporal Alignment

EFF operates on the canonical three-tier temporal hierarchy established by C9 Reconciliation:

| Tier | Name | Duration | EFF Usage |
|---|---|---|---|
| T-1 | `SETTLEMENT_TICK` | 60 s | VTD ingestion (continuous) |
| T-2 | `TIDAL_EPOCH` | 3,600 s (1 h) | RSC credibility updates, CABS recalibration, anomaly detection |
| T-3 | `CONSOLIDATION_CYCLE` | 36,000 s (10 h) | VFL metric publication (normal cadence), RSC pattern lifecycle transitions |

This alignment is not arbitrary. The three cadences serve different purposes: T-1 ensures VFL has fresh data; T-2 allows RSC and CABS to respond to emerging patterns within hours; T-3 allows VFL to accumulate sufficient statistical power for reliable population metrics. The 10-hour CONSOLIDATION_CYCLE publication cadence is faster than clinical practice guidelines (annual updates) but slower than real-time coaching — reflecting EFF's position as a statistical advisory service, not a reactive controller.

---

## 4. Verification Feedback Loop (VFL)

### 4.1 Purpose

VFL is the engine of EFF. It aggregates C5 PCVM verification outcomes into population-level, per-claim-class quality metrics while preserving individual agent privacy. VFL is the only new runtime component introduced by EFF.

The analogy is to public health surveillance. Individual patient records are private, but aggregate statistics — infection rates by region, treatment success rates by condition, adverse event frequencies by drug — are published for the benefit of all practitioners. No individual patient is identifiable in the aggregate data. No individual practitioner is monitored for whether they read the reports. VFL performs this function for the Atrahasis verification ecosystem.

### 4.2 VTD Ingestion

VFL subscribes to the C5 VTD output stream as a second consumer (alongside C8 DSF). For each completed VTD, VFL extracts:

| Field | Source in VTD Envelope | Purpose |
|---|---|---|
| `assigned_class` | `vtd.assigned_class` | Claim class categorization (D/C/P/R/E/S/K/H/N) |
| `tier` | `vtd.tier` | Verification tier (FORMAL_PROOF / STRUCTURED_EVIDENCE / STRUCTURED_ATTESTATION) |
| `producing_agent` | `vtd.producing_agent` | For k-anonymity grouping; **discarded after aggregation** |
| `epoch` | `vtd.epoch` | Temporal binning |
| `verdict` | Derived from verification outcome | ACCEPTED / REJECTED / WEAKENED |
| `premises_count` | `len(vtd.proof_body.premises)` | Reasoning complexity signal |
| `reasoning_steps_count` | `len(vtd.proof_body.reasoning_chain)` | Reasoning depth signal |
| `failure_mode` | Derived from rejection reason | Common failure categorization |
| `probe_outcome` | From CACT extension (if present) | Adversarial probing result (C11) |

VFL MUST NOT store raw VTD content. Only the extracted fields above are retained, and `producing_agent` is discarded after the aggregation window closes. This is a hard privacy boundary: the aggregation service processes agent identifiers for counting and deduplication purposes only, and the identifiers do not survive past the window closure.

VFL is a passive consumer. It MUST NOT modify VTDs, delay verification, or influence C5 decisions. If VFL is unavailable, C5 continues normally. VFL catches up from the VTD log on recovery.

### 4.3 Privacy-Preserving Aggregation

The privacy architecture uses three layers of defense in depth. No single layer is sufficient on its own; together they provide protection against re-identification, inference attacks, and linkage attacks.

**Layer 1 — k-Anonymity Floor (k = VFL_K_ANONYMITY_FLOOR, default 10)**

Statistics are computed only when the contributing agent set for a given claim class within the aggregation window contains at least k distinct agents. If fewer than k agents contributed to a class, the class statistics are suppressed for that window.

```python
def k_anonymity_check(records: list[VTDExtract], claim_class: str, k: int) -> bool:
    """Returns True if at least k distinct agents contributed to this class."""
    agents = set(r.producing_agent for r in records if r.assigned_class == claim_class)
    return len(agents) >= k
```

This prevents small-population classes from leaking individual agent performance. For a system with 1,000+ agents, k=10 is easily satisfied for common classes (D, R, E). For rare classes (K, H, N), suppression is expected in the early deployment period and is handled by hierarchical Bayesian estimation (Section 4.5).

**Layer 2 — Differential Privacy (epsilon = VFL_EPSILON, default 2.0)**

After aggregation, calibrated Laplace noise is added to all published counts and rates:

```python
def dp_noise(true_value: float, sensitivity: float, epsilon: float) -> float:
    """Add calibrated Laplace noise for epsilon-differential privacy."""
    scale = sensitivity / epsilon
    noise = numpy.random.laplace(0, scale)
    return true_value + noise

# For acceptance rate (sensitivity = 1/n where n is sample size):
noisy_rate = dp_noise(acceptance_rate, sensitivity=1.0/n, epsilon=VFL_EPSILON)
```

The key property of differential privacy is that its accuracy improves with population size: noise scales as O(1/n) for a fixed epsilon, meaning that as the agent population grows from 1K to 100K, the signal-to-noise ratio improves by 10x. EFF's value proposition strengthens with scale.

VFL_EPSILON is a constitutional parameter — changes require G-class consensus per C3 governance model. This prevents the privacy guarantee from being weakened through routine parameter tuning.

**Layer 3 — Secure Aggregation**

Agent identifiers are processed within a secure aggregation boundary. The aggregation service receives VTD extracts, computes per-class statistics, applies DP noise, and publishes only aggregate results. No per-agent data leaves the aggregation boundary.

```
VTD extracts --> [Secure Aggregation Boundary] --> Aggregate metrics only
                  |                              |
                  | agent_id used for:           |
                  |  - k-anonymity counting      |
                  |  - deduplication              |
                  | agent_id DISCARDED after      |
                  |   window close                |
                  +------------------------------+
```

### 4.4 Per-Claim-Class Quality Metrics

For each of the 9 canonical claim classes (D, C, P, R, E, S, K, H, N) established by C9 Reconciliation, VFL publishes the following metrics:

| Metric | Type | Description |
|---|---|---|
| `acceptance_rate` | float [0,1] | Fraction of claims accepted (with DP noise) |
| `rejection_rate` | float [0,1] | Fraction of claims rejected (with DP noise) |
| `weakened_rate` | float [0,1] | Fraction of claims weakened during CACT probing |
| `failure_mode_distribution` | map[string, float] | Top-5 failure modes with relative frequencies |
| `premises_count_stats` | {p25, p50, p75, p90} | Quartile distribution of premise counts for accepted claims |
| `reasoning_steps_stats` | {p25, p50, p75, p90} | Quartile distribution of reasoning steps for accepted claims |
| `sample_size` | int | Number of observations in the window (with DP noise) |
| `confidence_interval` | (float, float) | 95% CI for acceptance rate |

These metrics are calibrated per-class, not raw acceptance rates. This is important because C9 shows wide variation in admission thresholds: D-class requires 0.95 confidence while H-class operates at 0.50. A 70% acceptance rate for H-class is healthy; the same rate for D-class would indicate a serious problem. VFL consumers receive per-class metrics that are meaningful in context.

**Minimum sample size enforcement:** Per-class metrics are published only when `n >= VFL_MIN_SAMPLE` (default 50). This is stricter than the k-anonymity floor and prevents noisy statistics from misleading consumers.

### 4.5 Hierarchical Bayesian Estimation for Rare Classes

Classes with low claim volume — particularly Knowledge Consolidation (K), Heuristic (H), and Normative (N) — may not reach VFL_MIN_SAMPLE within a single CONSOLIDATION_CYCLE. VFL uses hierarchical Bayesian estimation (James-Stein shrinkage) to borrow strength across related classes within the same verification tier:

```python
class HierarchicalEstimator:
    """
    Hierarchical Bayesian estimation for claim class acceptance rates.
    Borrows strength across classes within the same verification tier.
    """

    # Tier groupings (from C5 Section 5)
    TIER_GROUPS = {
        "FORMAL_PROOF": ["D", "C"],
        "STRUCTURED_EVIDENCE": ["E", "S", "P", "R", "K"],
        "STRUCTURED_ATTESTATION": ["H", "N"]
    }

    def estimate(self, class_data: dict[str, ClassStats]) -> dict[str, float]:
        """
        For each class, compute a shrinkage estimator that pulls
        low-sample classes toward the tier mean.

        shrunk_rate = lambda * class_rate + (1 - lambda) * tier_rate

        where lambda = n_class / (n_class + kappa)
        kappa calibrated so that classes with n >= VFL_MIN_SAMPLE
        get lambda >= 0.8 (dominated by own data).
        """
        estimates = {}
        for tier, classes in self.TIER_GROUPS.items():
            tier_rate = self._compute_tier_rate(classes, class_data)
            for cls in classes:
                n = class_data[cls].sample_size
                kappa = VFL_MIN_SAMPLE / 4  # calibration constant
                lam = n / (n + kappa)
                estimates[cls] = lam * class_data[cls].raw_rate + (1 - lam) * tier_rate
        return estimates
```

The shrinkage estimator is a well-understood technique (~20 lines of code) with a clean mathematical interpretation: classes with ample data dominate their own estimate (lambda approaches 1), while classes with sparse data are "regularized" toward the tier mean. When a class has fewer than VFL_MIN_SAMPLE observations, its published acceptance rate carries a `shrinkage_applied: true` flag and the shrinkage weight `lambda` is included for transparency. Consumers know exactly how much of the estimate comes from direct observation versus tier-level borrowing.

### 4.6 Dual-Cadence Publication

VFL uses two publication cadences to balance statistical reliability with responsiveness.

**Normal cadence:** Per-class quality metrics are published once per CONSOLIDATION_CYCLE (36,000 s / 10 hours). This aligns with C6 EMA's consolidation schedule, ensuring RSC patterns can update credibility based on fresh VFL data. Ten hours provides sufficient accumulation time for robust statistics across most claim classes.

**Anomaly-triggered cadence:** VFL runs a chi-squared goodness-of-fit test on the per-class acceptance rate distribution at every TIDAL_EPOCH (3,600 s / 1 hour). If the test rejects the null hypothesis — that the current epoch's distribution matches the rolling baseline — at p < VFL_ANOMALY_P_THRESHOLD (default 0.01), an anomaly-triggered publication is emitted immediately.

```python
def anomaly_check(current_epoch: EpochStats, baseline: RollingBaseline) -> bool:
    """
    Chi-squared test: does the current epoch's per-class distribution
    deviate significantly from the rolling baseline?
    """
    observed = [current_epoch.counts[cls] for cls in CLAIM_CLASSES]
    expected = [baseline.expected_counts[cls] for cls in CLAIM_CLASSES]

    # Suppress classes with expected < 5 (chi-squared validity requirement)
    valid = [(o, e) for o, e in zip(observed, expected) if e >= 5]
    if len(valid) < 3:
        return False  # insufficient data for meaningful test

    chi2_stat = sum((o - e)**2 / e for o, e in valid)
    df = len(valid) - 1
    p_value = 1 - chi2_cdf(chi2_stat, df)

    return p_value < VFL_ANOMALY_P_THRESHOLD
```

Anomaly-triggered publications carry the `anomaly_trigger: true` flag with the chi-squared statistic and p-value. This dual-cadence design addresses Pre-mortem Scenario 6 ("The Feedback Freeze"): without the anomaly detector, a sudden distributional shift — such as a new PBC client introducing a novel problem domain — would go undetected for up to 10 hours. The chi-squared test adds approximately 15 lines of code and provides 1-hour detection latency for significant shifts.

### 4.7 VFL Output Schema

```json
{
  "$id": "https://eff.atrahasis.dev/schema/v1/vfl-publication.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "VFL Quality Metrics Publication",
  "type": "object",
  "required": ["publication_id", "publication_type", "window_start",
               "window_end", "epoch_range", "class_metrics", "metadata"],
  "properties": {
    "publication_id": {
      "type": "string",
      "pattern": "^vfl:pub:[0-9]+:[a-f0-9]{8}$"
    },
    "publication_type": {
      "type": "string",
      "enum": ["SCHEDULED", "ANOMALY_TRIGGERED"]
    },
    "window_start": { "type": "string", "format": "date-time" },
    "window_end": { "type": "string", "format": "date-time" },
    "epoch_range": {
      "type": "object",
      "properties": {
        "first_epoch": { "type": "integer" },
        "last_epoch": { "type": "integer" }
      }
    },
    "class_metrics": {
      "type": "object",
      "patternProperties": {
        "^[DCPRESKHN]$": {
          "$ref": "#/$defs/ClassMetrics"
        }
      }
    },
    "anomaly_trigger": {
      "type": "object",
      "properties": {
        "triggered": { "type": "boolean" },
        "chi_squared_stat": { "type": "number" },
        "p_value": { "type": "number" },
        "deviating_classes": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "epsilon_used": { "type": "number" },
        "k_anonymity_floor": { "type": "integer" },
        "min_sample_size": { "type": "integer" },
        "suppressed_classes": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "$defs": {
    "ClassMetrics": {
      "type": "object",
      "required": ["acceptance_rate", "rejection_rate", "sample_size"],
      "properties": {
        "acceptance_rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "rejection_rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "weakened_rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "failure_mode_distribution": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        },
        "premises_count_stats": { "$ref": "#/$defs/QuartileStats" },
        "reasoning_steps_stats": { "$ref": "#/$defs/QuartileStats" },
        "sample_size": { "type": "integer", "minimum": 0 },
        "confidence_interval": {
          "type": "array", "items": { "type": "number" },
          "minItems": 2, "maxItems": 2
        },
        "shrinkage_applied": { "type": "boolean", "default": false },
        "shrinkage_lambda": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "QuartileStats": {
      "type": "object",
      "properties": {
        "p25": { "type": "number" },
        "p50": { "type": "number" },
        "p75": { "type": "number" },
        "p90": { "type": "number" }
      }
    }
  }
}
```

---

## 5. Reasoning Strategy Catalog (RSC)

### 5.1 Purpose

RSC is a published library of proven reasoning patterns, stored as C6 EMA epistemic quanta with type `reasoning_strategy`. Agents may voluntarily query the catalog. RSC does not prescribe how to reason — it publishes what reasoning patterns historically correlate with successful verification.

The analogy to clinical practice guidelines (CPGs) in medicine is precise. CPGs do not tell physicians how to think. They publish evidence-based standards: "for chest pain with ST elevation, the evidence supports immediate catheterization." Physicians incorporate this guidance according to their clinical judgment. Some physicians follow CPGs closely; others exercise independent judgment for complex cases. CPG literature shows 5-10% improvement in practitioner outcomes. EFF's RSC serves the same function: "for R-class claims, premises validation + logical validity + counter-evidence consideration correlates with 15% higher acceptance rates."

The critical difference from CPGs — and the reason the Advisory Membrane matters — is that physicians face malpractice liability for ignoring CPGs. Atrahasis agents face no such enforcement. The membrane ensures this remains the case.

### 5.2 Format Types (v1.0 Restriction)

RSC v1.0 supports exactly three format types. This restriction is Feasibility Condition 1, driven by the Science Assessment's finding that model-agnostic patterns are feasible only for declarative formats.

| Format Type | Description | Example |
|---|---|---|
| `declarative_decomposition` | A structured breakdown of what verification expects for a claim class. Describes the logical components of a successful claim without prescribing how to produce them. | "For R-class: premises, logical validity, evidence support, scope coverage, counter-evidence consideration" |
| `anti_pattern` | A description of a reasoning pattern that correlates with verification failure. Describes the observable failure mode, not an avoidance strategy. | "Circular evidence chains: claims citing derivative sources that trace back to the original claim. Rejected at 3x baseline rate." |
| `verification_checklist` | A list of checkpoints that successful claims in a class typically satisfy. Structured as boolean predicates. | "E-class checklist: source accessible? source authoritative? quote found? quote supports claim? counter-evidence addressed?" |

The following format types are explicitly NOT supported in v1.0:
- Prompt templates
- Chain-of-thought prescriptions
- Internal representation guidance
- Architecture-specific optimizations

This restriction ensures model-agnosticism. A declarative decomposition can be consumed by an LLM (via RAG retrieval), a symbolic planner (via goal decomposition), or a hybrid system (via either channel). The pattern describes what verification expects, not how to produce it. The analogy is to building codes: they specify performance requirements ("structure must withstand X wind load") not construction methods ("use 2x4 studs at 16-inch intervals"). Engineers using steel, concrete, wood, or composite can all meet the same performance spec differently.

That said, the Science Assessment rated RSC at 2.5/5 — the lowest soundness score of any component. The evidence that published patterns improve quality is strong for LLMs via RAG/few-shot prompting (Wei et al. 2022) but absent for symbolic agents. The `architecture_applicability` field (`universal` or `llm_preferred`) allows patterns to be labeled accordingly. RSC v1.0's value proposition is primarily LLM-centric until evidence for other architectures accumulates.

### 5.3 RSC as Epistemic Quanta

RSC patterns are stored as C6 EMA epistemic quanta with the following field mappings:

| EQ Field | RSC Mapping |
|---|---|
| `id` | UUID v4 (standard EQ identifier) |
| `content` | `StructuredClaim` with `type: "reasoning_strategy"` and the pattern payload |
| `opinion` | Subjective logic tuple tracking pattern credibility (see 5.4) |
| `provenance` | Derivation chain: VFL metrics -> pattern extraction -> curation |
| `edges` | DERIVATION edges to source VFL publications; ANALOGY edges to related patterns |
| `metabolic_state` | Standard EQ lifecycle (see Section 5.7) |
| `claim_class` | The claim class this pattern applies to (D/C/P/R/E/S/K/H/N) |

RSC pattern content schema:

```json
{
  "type": "reasoning_strategy",
  "format": "declarative_decomposition | anti_pattern | verification_checklist",
  "applies_to_class": "D | C | P | R | E | S | K | H | N",
  "applies_to_tier": "FORMAL_PROOF | STRUCTURED_EVIDENCE | STRUCTURED_ATTESTATION",
  "title": "string (human-readable pattern name)",
  "description": "string (full pattern description)",
  "body": {
    "// Format-specific content:",
    "// declarative_decomposition: { components: [...] }",
    "// anti_pattern: { pattern: '...', failure_rate_multiplier: float, indicators: [...] }",
    "// verification_checklist: { checkpoints: [{ predicate: '...', weight: float }] }"
  },
  "source_vfl_publications": ["vfl:pub:..."],
  "version": "string (semver)",
  "architecture_applicability": "universal | llm_preferred",
  "seed_pattern": "boolean (true if manually curated, not derived from VFL)"
}
```

### 5.4 Credibility Tracking via Subjective Logic

Each RSC pattern carries a subjective logic opinion tuple (b, d, u, a) consistent with C6 EMA's credibility framework:

```python
@dataclass
class RSCCredibility:
    """
    Subjective logic opinion for an RSC pattern.

    - b: belief that the pattern improves verification success
    - d: disbelief (evidence that the pattern does NOT help)
    - u: uncertainty (insufficient evidence)
    - a: base rate (prior probability that a random pattern helps)

    Constraint: b + d + u = 1, 0 <= a <= 1
    """
    b: float
    d: float
    u: float
    a: float = 0.5  # uninformative prior

    def projected_probability(self) -> float:
        return self.b + self.a * self.u


# New patterns start with high uncertainty:
RSC_INITIAL_OPINION = RSCCredibility(
    b=0.10,    # minimal initial belief
    d=0.05,    # minimal initial disbelief
    u=0.85,    # high uncertainty (>= RSC_INITIAL_UNCERTAINTY = 0.70)
    a=0.50     # uninformative base rate
)

# Seed patterns (manually curated) start with moderate uncertainty:
RSC_SEED_OPINION = RSCCredibility(
    b=0.30,
    d=0.05,
    u=0.65,
    a=0.50
)
```

**Credibility update mechanism:** At each TIDAL_EPOCH, RSC patterns are evaluated against the latest VFL data. For claim class C with pattern P:

1. Compute the acceptance rate for agents who queried pattern P before submitting C-class claims (from advisory consumption logs, within the secure aggregation boundary).
2. Compare against the population acceptance rate for the same class.
3. If the pattern-consulting cohort has a higher acceptance rate, increase b (via cumulative fusion with positive evidence opinion).
4. If lower, increase d (via cumulative fusion with negative evidence opinion).
5. If insufficient data (< RSC_CREDIBILITY_UPDATE_MIN_N observations in either cohort), increase u slightly.

**Privacy guarantee:** The acceptance rate comparison is computed WITHIN the secure aggregation boundary. Only the resulting opinion update (a delta to the b/d/u tuple) leaves the boundary. C17 and C35 never see which agents consulted which patterns.

### 5.5 Cold-Start: Seed Patterns

At system initialization, RSC begins with manually curated seed patterns authored by the specification team based on:

1. C5 PCVM verification protocol requirements (what constitutes adequate proof per class)
2. C9 reconciliation constraints (cross-layer consistency requirements)
3. Domain expert knowledge of reasoning best practices

Seed patterns are marked `seed_pattern: true` and start with RSC_SEED_OPINION (lower initial uncertainty than derived patterns). They follow the standard RSC lifecycle but receive a grace period of RSC_SEED_GRACE_PERIOD (default 5) CONSOLIDATION_CYCLEs before catabolism evaluation.

Recommended minimum seed set:

| Claim Class | Seed Patterns | Rationale |
|---|---|---|
| D (Deterministic) | 1 decomposition, 1 checklist | Well-bounded; formal proof |
| C (Compliance) | 1 decomposition, 1 checklist | Rule-matching; bounded |
| P (Process) | 1 decomposition, 1 anti-pattern | Multi-step validation |
| R (Reasoning) | 2 decompositions, 2 anti-patterns, 1 checklist | Highest volume, most complex |
| E (Empirical) | 1 decomposition, 1 anti-pattern, 1 checklist | Source verification |
| S (Statistical) | 1 decomposition, 1 anti-pattern, 1 checklist | Methodology validation |
| K (Knowledge) | 1 decomposition, 1 checklist | Cross-source synthesis |
| H (Heuristic) | 1 decomposition, 2 anti-patterns | Judgment-intensive; adversarial |
| N (Normative) | 1 decomposition, 1 anti-pattern | Value-laden; committee review |

Total: ~27 seed patterns. R-class receives extra coverage because it is the highest-volume class in the STRUCTURED_EVIDENCE tier with the most complex verification protocol.

### 5.6 Pattern Diversity Monitoring

RSC MUST monitor population structural convergence to prevent reasoning monoculture (Feasibility Condition 5). This requirement is driven by Pre-mortem Scenario 2 ("The Monoculture Collapse"), rated CRITICAL x HIGH: if agents rationally converge on the highest-scored patterns, the system loses cognitive diversity and becomes brittle when novel problem classes emerge.

**Convergence metric:** For each claim class, compute the structural similarity of VTD reasoning chains submitted in the current CONSOLIDATION_CYCLE. If the mean pairwise structural similarity exceeds RSC_CONVERGENCE_THRESHOLD (default 0.70, needs empirical calibration), a diversity alert is raised.

```python
def monitor_convergence(vtds: list[VTDExtract], claim_class: str) -> ConvergenceReport:
    """
    Monitor structural convergence of reasoning patterns for a claim class.
    Uses VFL's copy of VTD structural data (not raw VTDs).
    """
    class_vtds = [v for v in vtds if v.assigned_class == claim_class]
    if len(class_vtds) < 30:
        return ConvergenceReport(status="INSUFFICIENT_DATA")

    # Extract structural fingerprints (reasoning step topology)
    fingerprints = [extract_structure(v) for v in class_vtds]

    # Compute mean pairwise similarity (sample if n > 200)
    if len(fingerprints) > 200:
        fingerprints = random.sample(fingerprints, 200)

    pairs = list(itertools.combinations(fingerprints, 2))
    mean_sim = sum(structural_similarity(a, b) for a, b in pairs) / len(pairs)

    if mean_sim > RSC_CONVERGENCE_THRESHOLD:
        return ConvergenceReport(
            status="CONVERGENCE_ALERT",
            mean_similarity=mean_sim,
            threshold=RSC_CONVERGENCE_THRESHOLD,
            recommendation="Publish alternative patterns; flag dominant pattern for review"
        )

    return ConvergenceReport(status="HEALTHY", mean_similarity=mean_sim)
```

**Response to convergence alert:**
1. Flag the dominant RSC pattern(s) for the affected class.
2. Increase the visibility of alternative patterns in catalog queries.
3. Consider minting new patterns from the minority reasoning structures in VFL data.
4. Do NOT suppress or remove the convergent pattern — agents chose it voluntarily (EFF-R14).

The convergence monitoring adds approximately 30 lines of code (sampling, pairwise similarity, threshold check). The Simplification Report evaluated deferring it and concluded that deferring a CRITICAL mitigation for a savings of 30 lines is not a good trade.

### 5.7 Pattern Lifecycle State Machine

RSC patterns follow the C6 EMA metabolic lifecycle with RSC-specific transition conditions:

```
                                    +-------------------------+
                                    |                         |
            manual curation         |     VFL-derived         |
            (seed patterns)         |     extraction          |
                   |                |                         |
                   v                v                         |
            +-------------+                                   |
            |  CANDIDATE  |  (pre-ingestion review)           |
            +------+------+                                   |
                   |                                          |
                   | format validation + uniqueness check      |
                   |                                          |
                   v                                          |
            +-------------+                                   |
            |  INGESTED   |  (C6 standard state)              |
            +------+------+                                   |
                   |                                          |
                   | initial opinion assigned                  |
                   | (RSC_INITIAL_OPINION or RSC_SEED_OPINION) |
                   |                                          |
                   v                                          |
            +-------------+                                   |
            |   ACTIVE    |  (published, queryable)           |
            |             |                                   |
            | credibility |<----------------------------------+
            | updated per |   (reactivation from DORMANT)
            | TIDAL_EPOCH |
            +--+---+---+--+
               |   |   |
    +----------+   |   +----------+
    |              |              |
    v              v              v
+--------+  +----------+  +------------+
|DORMANT |  |  SUPER-  |  |QUARANTINED |
|        |  |  SEDED   |  |            |
|(low    |  |          |  |(credibility|
|access) |  |(newer    |  | below      |
|        |  |version   |  | threshold) |
|        |  |exists)   |  |            |
+---+----+  +----+-----+  +------+-----+
    |            |               |
    | reactivate |               | re-evaluation
    | (access    |               | (new evidence)
    |  resumes)  |               |
    |            |               +--> ACTIVE (if credibility recovers)
    |            |               |
    |            v               v
    |       +----------+  +----------+
    |       |DISSOLVED |  |DISSOLVED |
    |       +----------+  +----------+
    |
    +--> QUARANTINED (if credibility decays during dormancy)
```

**State descriptions:**

| State | Entry Condition | Behavior | Exit Condition |
|---|---|---|---|
| **CANDIDATE** | Pattern extracted from VFL or manually authored | Awaiting format validation and uniqueness check. Not visible to agents. | Passes validation -> INGESTED. Fails -> discarded. |
| **INGESTED** | CANDIDATE passes validation | C6 standard: initial opinion assigned, provenance recorded, edges formed. | Standard C6 transition to ACTIVE. |
| **ACTIVE** | INGESTED processing complete | Published in RSC catalog. Queryable by agents. Credibility updated each TIDAL_EPOCH. Structural fingerprint exported to C17 whitelist. | Low access -> DORMANT. Superseded -> SUPERSEDED. Low credibility -> QUARANTINED. |
| **DORMANT** | Access frequency below threshold for 3 consecutive CONSOLIDATION_CYCLEs | Excluded from RSC query results (but not deleted). Credibility frozen. Removed from C17 whitelist. | Access resumes -> ACTIVE. Credibility decays -> QUARANTINED. |
| **SUPERSEDED** | A newer version of this pattern enters ACTIVE state | Remains queryable for backward compatibility but flagged. Not in default queries. Removed from C17 whitelist. | 5 CONSOLIDATION_CYCLEs with zero queries -> DISSOLVED. |
| **QUARANTINED** | Credibility opinion projected probability < 0.40, OR named as dominant in convergence alert | Under review. Not queryable. Removed from C17 whitelist. | Recovery with new VFL data -> ACTIVE (if projected probability >= 0.50, hysteresis). 3 cycles without recovery -> DISSOLVED. |
| **DISSOLVED** | Terminal state | Pattern content removed. Provenance and dissolution record retained per C6 standard. C17 whitelist entry removed. | None (terminal). |

**Transition guards:**

```python
class RSCLifecycleGuard:
    """Guards for RSC pattern state transitions."""

    def can_quarantine(self, pattern: RSCPattern) -> bool:
        """ACTIVE -> QUARANTINED requires credibility below threshold."""
        pp = pattern.opinion.projected_probability()
        if pattern.seed_pattern and pattern.active_cycles < RSC_SEED_GRACE_PERIOD:
            return False  # seed grace period
        return pp < 0.40  # QUARANTINE_THRESHOLD

    def can_reactivate_from_quarantine(self, pattern: RSCPattern) -> bool:
        """QUARANTINED -> ACTIVE requires credibility recovery (with hysteresis)."""
        pp = pattern.opinion.projected_probability()
        return pp >= 0.50  # higher than quarantine threshold

    def can_dissolve_from_quarantine(self, pattern: RSCPattern) -> bool:
        """QUARANTINED -> DISSOLVED after timeout."""
        return pattern.quarantine_cycles >= 3

    def can_supersede(self, old: RSCPattern, new: RSCPattern) -> bool:
        """An ACTIVE pattern can be SUPERSEDED by a new pattern."""
        return (
            old.applies_to_class == new.applies_to_class and
            old.format == new.format and
            new.opinion.projected_probability() > old.opinion.projected_probability()
        )

    def should_dormant(self, pattern: RSCPattern) -> bool:
        """ACTIVE -> DORMANT on sustained low access."""
        return pattern.consecutive_low_access_cycles >= 3
```

**C17 Whitelist lifecycle integration:**

| RSC State Transition | C17 Whitelist Action |
|---|---|
| -> ACTIVE | Add structural fingerprint to whitelist |
| ACTIVE -> DORMANT | Remove from whitelist |
| ACTIVE -> SUPERSEDED | Remove from whitelist |
| ACTIVE -> QUARANTINED | Remove from whitelist |
| DORMANT -> ACTIVE | Re-add structural fingerprint to whitelist |
| QUARANTINED -> ACTIVE | Re-add structural fingerprint to whitelist |
| -> DISSOLVED | Remove from whitelist (if present) |

---

## 6. Complexity-Aware Budget Signals (CABS)

### 6.1 Purpose

CABS provides optional reasoning budget recommendations on C23 SCR ExecutionLease objects. These signals suggest how much reasoning effort — measured in tokens or steps — is likely to be useful for a given task, based on claim class, decomposition complexity, and historical verification data.

CABS does not constrain agents. It annotates leases with advisory information.

The analogy is to FDA Nutrition Facts labels. The label says "2,000 calories/day" as a reference, knowing that individual needs vary by body composition, activity level, and metabolism. The recommendation is population-derived, task-categorized ("active adult" vs. "sedentary"), and explicitly advisory. CABS recommends reasoning budgets the same way — population-derived, claim-class-categorized, explicitly advisory.

The critical insight from recent literature (arXiv:2512.19585, "Increasing the Thinking Budget is Not All You Need") is that the relationship between reasoning budget and performance is non-monotonic: more tokens can DECREASE performance beyond a certain point. This is why CABS provides a three-value range (min_sufficient, recommended, max_useful) rather than a point estimate, and pairs it with a strategy label. The max_useful ceiling is as important as the recommended value.

### 6.2 Advisory Object Schema

```json
{
  "$id": "https://eff.atrahasis.dev/schema/v1/reasoning-budget-advisory.schema.json",
  "title": "Reasoning Budget Advisory",
  "type": "object",
  "required": ["min_sufficient", "recommended", "max_useful",
               "strategy_label", "confidence"],
  "properties": {
    "min_sufficient": {
      "type": "integer",
      "minimum": 0,
      "description": "Minimum reasoning budget (tokens/steps) at which acceptable quality is achievable."
    },
    "recommended": {
      "type": "integer",
      "minimum": 0,
      "description": "Recommended reasoning budget -- the CABS_CALIBRATION_PERCENTILE of successful claims."
    },
    "max_useful": {
      "type": "integer",
      "minimum": 0,
      "description": "Budget beyond which additional effort shows no marginal quality improvement."
    },
    "strategy_label": {
      "type": "string",
      "description": "Human-readable label for the recommended approach.",
      "examples": ["decompose-then-verify", "evidence-chain-first", "counter-evidence-sweep"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Confidence in this recommendation. Low confidence indicates sparse historical data."
    },
    "source_components": {
      "type": "object",
      "description": "Provenance of this recommendation.",
      "properties": {
        "claim_class_weight": { "type": "number" },
        "rif_complexity_score": { "type": "number" },
        "vfl_calibration_percentile": { "type": "integer" },
        "vfl_publication_id": { "type": "string" }
      }
    }
  }
}
```

### 6.3 Budget Computation

CABS computes the advisory from three independent sources, then fuses them:

**Source 1: C9 Claim Class Difficulty Weights**

C9 reconciliation defines per-class difficulty multipliers reflecting verification complexity:

| Class | Weight | Rationale |
|---|---|---|
| D (Deterministic) | 1.0 | Formal proof, well-bounded |
| C (Compliance) | 1.2 | Rule-matching, bounded |
| P (Process) | 1.5 | Multi-step process validation |
| R (Reasoning) | 2.0 | Open-ended logical analysis |
| E (Empirical) | 1.8 | Source verification, factual checking |
| S (Statistical) | 2.0 | Methodology validation |
| K (Knowledge Consolidation) | 2.2 | Cross-source synthesis |
| H (Heuristic) | 2.5 | Judgment-intensive, adversarial probing |
| N (Normative) | 3.0 | Value-laden, committee review |

These weights reflect the intuition that a normative claim (N-class, weight 3.0) requires roughly three times the reasoning effort of a deterministic claim (D-class, weight 1.0). The weights are derived from C9 and are static until C9 is revised.

**Source 2: C7 RIF Decomposition Complexity**

The C7 RIF Parcel Executor produces a decomposition tree for each intent. CABS reads the structural complexity of the leaf intent's position in this tree:

```python
def rif_complexity(intent: Intent) -> float:
    """
    Estimate reasoning complexity from RIF decomposition structure.
    """
    depth = intent.decomposition_depth       # 1-5 typical
    sibling_count = intent.sibling_count     # parallel tasks at this level
    dependency_count = intent.dependency_count # data dependencies

    # Normalized to [0, 1] range
    return min(1.0, (depth * 0.3 + sibling_count * 0.1 + dependency_count * 0.2) / 3.0)
```

**Source 3: VFL Historical Calibration**

From the latest VFL publication, CABS extracts the CABS_CALIBRATION_PERCENTILE (default: 75th) of reasoning_steps_count for accepted claims in the relevant class. This is the most dynamic source — it adapts as the population's reasoning patterns evolve.

```python
def compute_advisory(claim_class: str, intent: Intent,
                     vfl_pub: VFLPublication) -> ReasoningBudgetAdvisory:
    """
    Fuse three sources into a budget advisory.
    """
    # Source 1: class weight
    class_weight = C9_DIFFICULTY_WEIGHTS[claim_class]
    base_budget = int(CABS_BASE_REASONING_TOKENS * class_weight)

    # Source 2: RIF complexity adjustment
    rif_score = rif_complexity(intent)
    rif_adjusted = int(base_budget * (1.0 + rif_score * 0.5))

    # Source 3: VFL calibration
    class_metrics = vfl_pub.class_metrics.get(claim_class)
    vfl_p75 = class_metrics.reasoning_steps_stats.p75 if class_metrics else None

    if vfl_p75 is not None:
        # Weight VFL data heavily when available
        recommended = int(0.4 * rif_adjusted + 0.6 * vfl_p75)
        confidence = min(0.9, class_metrics.sample_size / 500)
    else:
        recommended = rif_adjusted
        confidence = 0.3  # low confidence without VFL data

    # Non-monotonic budget-performance ceiling (from VFL p90)
    vfl_p90 = class_metrics.reasoning_steps_stats.p90 if class_metrics else None
    max_useful = vfl_p90 if vfl_p90 else int(recommended * 1.5)

    # Minimum sufficient (from VFL p25)
    vfl_p25 = class_metrics.reasoning_steps_stats.p25 if class_metrics else None
    min_sufficient = vfl_p25 if vfl_p25 else int(recommended * 0.4)

    # Strategy label from highest-credibility RSC pattern for this class
    strategy = rsc_best_pattern(claim_class)

    return ReasoningBudgetAdvisory(
        min_sufficient=min_sufficient,
        recommended=recommended,
        max_useful=max_useful,
        strategy_label=strategy.title if strategy else "general",
        confidence=confidence,
        source_components={
            "claim_class_weight": class_weight,
            "rif_complexity_score": rif_score,
            "vfl_calibration_percentile": CABS_CALIBRATION_PERCENTILE,
            "vfl_publication_id": vfl_pub.publication_id
        }
    )
```

The three-source design ensures CABS produces useful recommendations even before VFL has accumulated data. In the early deployment period: Source 1 (C9 weights) provides a fixed baseline; Source 2 (RIF complexity) adds task-specific variation; Source 3 (VFL calibration) is absent, so confidence is low (0.3). As VFL data accumulates over weeks and months, Source 3 dominates the recommendation and confidence rises toward 0.9.

### 6.4 Non-Breaking Integration

The `reasoning_budget_advisory` field on C23 ExecutionLease is OPTIONAL:

- Leases without this field continue to work identically to pre-EFF behavior.
- No SCR component reads or enforces the advisory — it is metadata for the agent.
- Agents MAY ignore the advisory entirely. No downstream consequence follows.
- The C23 Execution Evidence Bundle (EEB) MUST NOT record whether the agent followed the advisory (EFF-R17).

This non-breaking integration is deliberate. EFF imposes zero migration cost on existing system components or agents. Agents that are unaware of EFF operate identically to before. Agents that choose to consume CABS advisories can do so at their discretion.

---

## 7. Advisory Membrane

### 7.1 Purpose

The Advisory Membrane is the architectural boundary between EFF's advisory signals and the enforcement/surveillance mechanisms of the Atrahasis stack. It is not a software component — it is an information flow policy enforced through data segregation, access control, and integration contract constraints.

The membrane ensures one invariant: **no enforcement or surveillance system may use EFF advisory consumption data as input.**

This invariant is the primary patent differentiator. Every prior art reference in the AI governance space — GaaS, FL, SOFAI-LM, observability platforms — either enforces compliance or does not address the enforcement/advisory boundary at all. The Advisory Membrane formalizes a distinction that no existing system makes explicit.

### 7.2 Information Flow Controls

**ADVISORY_PRIVATE label:** All RSC consumption logs (which agent queried which pattern, when, how often) are labeled `ADVISORY_PRIVATE`. This label has the following access control semantics:

| Component | Read Access to ADVISORY_PRIVATE | Rationale |
|---|---|---|
| VFL aggregation service | YES (within secure aggregation boundary) | Required for RSC credibility updates |
| RSC catalog service | YES (query routing) | Required for catalog operation |
| C17 MCSD | **NO** | Prevents behavioral similarity weaponization |
| C35 Sentinel | **NO** | Prevents anomaly detection weaponization |
| C5 PCVM | **NO** | Prevents verification bias |
| C8 DSF | **NO** | Prevents economic consequences |
| C7 RIF | **NO** | Prevents orchestration bias |
| C3 Tidal Noosphere | **NO** | Prevents governance consequences |

**Data segregation:** Advisory consumption logs MUST be stored in a physically or logically separate data store from:
- C17 Behavioral VTD storage
- C35 Sentinel metric streams
- C5 VTD storage
- C8 settlement records

The segregation boundary MUST be verifiable by audit at every MEMBRANE_AUDIT_INTERVAL (default 10 CONSOLIDATION_CYCLEs).

### 7.3 C17 RSC-Aware Whitelist Protocol

The structural side-channel is the highest risk identified by the Science Assessment: agents consuming RSC patterns produce structurally similar reasoning, which C17's structural modality (w_S = 0.25) may detect as shared origin. This was identified as Rank 1 in the Pre-mortem Analysis ("The Invisible Cage") — a scenario where C17 effectively punishes agents who follow RSC patterns by flagging them as potential Sybils.

**Mitigation: RSC Pattern Whitelist Protocol**

1. Every time an RSC pattern transitions to ACTIVE state, its structural fingerprint is added to the C17 RSC whitelist.
2. When C17 computes B(a_i, a_j) structural distance, it applies a discount for similarity that matches published RSC patterns:

```python
def adjusted_structural_distance(
    s_i: StructuralProfile,
    s_j: StructuralProfile,
    rsc_whitelist: list[StructuralFingerprint]
) -> float:
    """
    Compute structural distance with RSC whitelist discounting.

    Similarity that matches published RSC patterns is expected
    (agents following published guidance) and should not count
    as evidence of shared origin.
    """
    raw_distance = cosine_distance(s_i, s_j)

    # Identify structural features that match whitelisted patterns
    whitelist_overlap_i = compute_whitelist_overlap(s_i, rsc_whitelist)
    whitelist_overlap_j = compute_whitelist_overlap(s_j, rsc_whitelist)

    # Discount: if both agents' structural similarity is explainable
    # by published RSC patterns, reduce the distance weight
    shared_whitelist = whitelist_overlap_i & whitelist_overlap_j
    discount_factor = 1.0 - (len(shared_whitelist) / max(len(rsc_whitelist), 1))

    return raw_distance * discount_factor
```

3. The whitelist is synchronized at every CONSOLIDATION_CYCLE. C17 receives only structural fingerprints of published patterns — not consumption data, not credibility scores, not query frequencies.

The distinction is precise: the whitelist tells C17 *what patterns exist* (public information). Consumption data tells C17 *who queries them* (private information). Only the former crosses the membrane.

### 7.4 The Voluntariness Paradox

EFF explicitly acknowledges a fundamental limitation of all effective advisory systems:

**Statement of the paradox:** If EFF advisory signals are effective, agents that consume them will achieve higher verification rates and lower inference costs than agents that do not. This performance differential creates market pressure to adopt EFF signals. Over time, non-adoption may become an economic disadvantage. The membrane prevents surveillance-based coercion but cannot prevent performance-based self-selection.

**This is by design.** The same dynamic exists in every effective advisory system:
- Medical clinical practice guidelines are formally advisory; physicians who consistently ignore them face malpractice exposure.
- Academic peer review norms are voluntary; researchers who ignore them cannot publish.
- Building codes specify performance requirements; builders who ignore them cannot pass inspection.

The membrane's guarantee is narrower and more precise than "complete voluntariness." It guarantees that **no Atrahasis enforcement mechanism will use EFF consumption data as a decision input.** Whether to consume advisory signals is a sovereign agent choice with natural (not enforced) consequences.

**What the membrane prevents:**
- C17 treating pattern consumption as behavioral similarity evidence
- C35 treating non-consumption as an anomaly
- C5 adjusting verification thresholds based on advisory adherence
- C8 adjusting settlement rates based on advisory usage

**What the membrane does NOT prevent:**
- Agents who follow good advice performing better than those who do not
- The market recognizing and rewarding better-performing agents
- De facto adoption norms emerging over time

This acknowledgment is Feasibility Condition 4. The specification is transparent about the paradox rather than claiming complete voluntariness.

### 7.5 C35 Sentinel Explicit Exclusion

C35 Sentinel's three-tier anomaly detection pipeline MUST NOT use advisory consumption as an input feature. Specifically:

1. **Tier 1 (STA/LTA per-agent):** Metric channels MUST NOT include "RSC query frequency" or "CABS adherence ratio."
2. **Tier 2 (PCM pairwise correlation):** Platform covariates for the PCM model MUST NOT include advisory consumption similarity.
3. **Tier 3 (backward tracing):** Source attribution MUST NOT reference RSC patterns as causal explanations for behavioral clusters.

This exclusion is specified as an integration contract (IC-EFF-05).

---

## 8. Integration Contracts

EFF defines six integration contracts governing its interfaces with the existing Atrahasis stack. Four are data-flow contracts; two are exclusion contracts.

### 8.1 IC-EFF-01: C5 PCVM -> VFL (VTD Second Consumer)

| Field | Value |
|---|---|
| **Provider** | C5 PCVM |
| **Consumer** | EFF VFL |
| **Interface** | VTD output stream subscription |
| **Data** | Completed VTD envelope (read-only) |
| **Latency** | Within 1 SETTLEMENT_TICK of VTD completion |
| **Guarantees** | At-least-once delivery; VFL handles deduplication via vtd_id |
| **Privacy** | VFL extracts only the fields listed in Section 4.2; raw VTD content is not retained |
| **Non-interference** | VFL is a passive consumer. It MUST NOT modify VTDs, delay verification, or influence C5 decisions |
| **Failure mode** | If VFL is unavailable, C5 continues normally. VFL catches up from the VTD log on recovery |
| **Schema dependency** | VFL depends on the C5 VTD common envelope schema v2. VFL MUST NOT depend on `proof_body` internals |

### 8.2 IC-EFF-02: VFL -> C6 EMA (RSC Patterns as Epistemic Quanta)

| Field | Value |
|---|---|
| **Provider** | EFF VFL / RSC pattern extraction |
| **Consumer** | C6 EMA |
| **Interface** | Standard EQ ingestion pipeline |
| **Data** | Epistemic quanta with `content.type = "reasoning_strategy"` |
| **Lifecycle** | RSC quanta follow standard EMA metabolic lifecycle (INGESTED -> ACTIVE -> DORMANT -> QUARANTINED -> DISSOLVED) |
| **Credibility** | Initial opinion set by RSC (Section 5.4); subsequent updates via standard EMA opinion fusion |
| **Coherence graph** | RSC quanta participate with DERIVATION edges (to source VFL publications) and ANALOGY edges (to related patterns) |
| **SHREC** | RSC quanta compete for metabolic processing budget under standard SHREC regulation. They are NOT exempt from catabolism |
| **Special** | RSC quanta with `seed_pattern: true` receive RSC_SEED_GRACE_PERIOD before catabolism candidacy |

### 8.3 IC-EFF-03: CABS -> C23 SCR (Optional Lease Advisory)

| Field | Value |
|---|---|
| **Provider** | EFF CABS |
| **Consumer** | C23 SCR ExecutionLease |
| **Interface** | Optional `reasoning_budget_advisory` field on ExecutionLease schema |
| **Data** | `ReasoningBudgetAdvisory` object (Section 6.2) |
| **Non-breaking** | Leases without this field are valid. No SCR component reads or enforces the advisory |
| **Timing** | CABS populates the advisory at lease creation time (during C7 -> C23 handoff) |
| **Update** | The advisory is immutable for the lease lifetime. New leases receive updated advisories |
| **Evidence exclusion** | The C23 Execution Evidence Bundle (EEB) MUST NOT record whether the agent read or followed the advisory |

### 8.4 IC-EFF-04: RSC -> C17 MCSD (Published Pattern Whitelist)

| Field | Value |
|---|---|
| **Provider** | EFF RSC |
| **Consumer** | C17 MCSD B(a_i, a_j) computation |
| **Interface** | Structural fingerprint whitelist, synchronized per CONSOLIDATION_CYCLE |
| **Data** | Structural fingerprints of ACTIVE RSC patterns (not consumption data, not full pattern content) |
| **Purpose** | C17 discounts structural similarity that matches published RSC patterns |
| **Data excluded** | Agent consumption logs, pattern credibility scores, query frequencies |
| **Synchronization** | Pull model: C17 queries the RSC whitelist at the start of each SEB evaluation round |
| **Failure mode** | If RSC whitelist is unavailable, C17 proceeds with un-discounted structural similarity (conservative) |

### 8.5 IC-EFF-05: C35 Sentinel (Explicit Exclusion)

| Field | Value |
|---|---|
| **Provider** | N/A (exclusion contract) |
| **Consumer** | C35 Sentinel |
| **Interface** | None — this contract specifies what C35 MUST NOT consume |
| **Exclusion** | C35 MUST NOT read, subscribe to, or derive features from: RSC consumption logs, CABS adherence data, advisory query patterns, or any data labeled ADVISORY_PRIVATE |
| **Audit** | The C35 deployment configuration MUST NOT contain connection strings, API endpoints, or data source references to advisory consumption stores |
| **Rationale** | Prevents advisory signals from becoming surveillance inputs |

### 8.6 IC-EFF-06: C17 MCSD (Consumption Data Exclusion)

| Field | Value |
|---|---|
| **Provider** | N/A (exclusion contract) |
| **Consumer** | C17 MCSD |
| **Interface** | None — this contract specifies what C17 MUST NOT consume |
| **Exclusion** | C17 MUST NOT use RSC consumption logs, CABS adherence data, or advisory query patterns as input to B(a_i, a_j) computation or any other behavioral analysis |
| **Permitted** | C17 MAY consume the RSC published pattern whitelist (IC-EFF-04) for structural baseline adjustment |
| **Distinction** | Whitelist = what patterns exist (public). Consumption = who queries them (private) |

---

## 9. Parameters

### 9.1 Parameters Table

| # | Parameter | Default | Type | Scope | Governance |
|---|---|---|---|---|---|
| 1 | `VFL_EPSILON` | 2.0 | float (0, inf) | Constitutional | G-class consensus required for change |
| 2 | `VFL_K_ANONYMITY_FLOOR` | 10 | int [2, 100] | Operational | Standard parameter change process |
| 3 | `VFL_MIN_SAMPLE` | 50 | int [10, 1000] | Operational | Standard parameter change process |
| 4 | `VFL_ANOMALY_P_THRESHOLD` | 0.01 | float (0, 0.1) | Operational | Standard parameter change process |
| 5 | `VFL_ROLLING_BASELINE_WINDOW` | 10 | int [5, 50] | Operational | Number of CONSOLIDATION_CYCLEs in rolling baseline |
| 6 | `VFL_SHRINKAGE_KAPPA` | 12.5 | float (0, 100) | Operational | Calibration constant for hierarchical Bayesian (VFL_MIN_SAMPLE / 4) |
| 7 | `RSC_INITIAL_UNCERTAINTY` | 0.70 | float [0.5, 0.95] | Operational | Minimum initial u for new patterns |
| 8 | `RSC_SEED_UNCERTAINTY` | 0.65 | float [0.4, 0.90] | Operational | Initial u for seed patterns |
| 9 | `RSC_SEED_GRACE_PERIOD` | 5 | int [3, 20] | Operational | CONSOLIDATION_CYCLEs before seed catabolism eligibility |
| 10 | `RSC_CONVERGENCE_THRESHOLD` | 0.70 | float [0.5, 0.95] | Operational | Mean pairwise structural similarity alert threshold. **Needs empirical calibration.** |
| 11 | `RSC_CONVERGENCE_SAMPLE_SIZE` | 200 | int [50, 500] | Operational | Max sample pairs for convergence computation |
| 12 | `RSC_CREDIBILITY_UPDATE_MIN_N` | 20 | int [10, 100] | Operational | Min observations per cohort for credibility update |
| 13 | `CABS_CALIBRATION_PERCENTILE` | 75 | int [50, 95] | Operational | Percentile of successful claims for recommended budget |
| 14 | `CABS_BASE_REASONING_TOKENS` | 1000 | int [100, 10000] | Operational | Base token budget before class/complexity adjustment |
| 15 | `MEMBRANE_AUDIT_INTERVAL` | 10 | int [1, 100] | Operational | CONSOLIDATION_CYCLEs between membrane audit checks |

### 9.2 Parameter Interactions

| Interaction | Constraint |
|---|---|
| VFL_K_ANONYMITY_FLOOR < VFL_MIN_SAMPLE | Always true (k=10 < min=50). k-anonymity is necessary but not sufficient for publication. |
| VFL_EPSILON and VFL_MIN_SAMPLE | Lower epsilon (stronger privacy) requires larger samples for the same statistical power. At epsilon=1.0, VFL_MIN_SAMPLE should be >= 100. |
| RSC_CONVERGENCE_THRESHOLD + RSC pattern count | If very few patterns exist, convergence is expected and the threshold should be relaxed. |
| CABS_CALIBRATION_PERCENTILE and max_useful | max_useful uses p90 regardless of CABS_CALIBRATION_PERCENTILE; recommended uses the configured percentile. |
| VFL_SHRINKAGE_KAPPA | Should equal VFL_MIN_SAMPLE / 4. If VFL_MIN_SAMPLE changes, kappa should be recalibrated. |

---

## 10. Implementation

### 10.1 C22 Wave Placement

EFF deploys across three waves, reaching full operational capability at Wave 3:

**Dependencies:**

| Dependency | Wave | Rationale |
|---|---|---|
| C5 PCVM operational | Wave 1 | VFL requires VTD stream |
| C6 EMA operational | Wave 2 | RSC stored as epistemic quanta |
| C23 SCR operational | Wave 1 | CABS advisory field on ExecutionLease |
| C7 RIF operational | Wave 1 | CABS reads decomposition complexity |
| C9 reconciliation | Wave 1 | CABS reads claim class difficulty weights |
| C17 MCSD operational | Wave 2 | Advisory Membrane whitelist integration |
| C35 Sentinel operational | Wave 3 | Exclusion contract |

**Wave-by-wave deployment:**

```
Wave 0: Risk validation experiments
  +-- No EFF involvement

Wave 1: Foundation (C5, C23, C7, C8, C9)
  +-- EFF prerequisites deployed
  +-- CABS schema extension added to C23 (dormant -- no data yet)

Wave 2: Coordination (C3, C6, C17)
  +-- VFL aggregation service deployed
  +-- RSC seed patterns loaded into C6
  +-- VFL begins ingesting VTDs and building baseline
  +-- RSC credibility tracking begins
  +-- CABS begins producing advisories (initially low confidence)
  +-- C17 whitelist integration activated

Wave 3: Intelligence (C35)
  +-- C35 exclusion contract verified
  +-- Advisory Membrane audit capability deployed
  +-- Full EFF operational

Wave 4: Defense (C11, C12, C13)
  +-- No EFF-specific work

Wave 5: Governance (C14)
  +-- No EFF-specific work
```

### 10.2 Maturity Progression

| Wave | EFF Maturity | Description |
|---|---|---|
| Wave 1 | Stub (~10%) | Schema extensions in C23. No runtime. |
| Wave 2 | Functional (~60%) | VFL running, RSC seeded, CABS producing. Low confidence. Membrane enforced for C17. |
| Wave 3 | Hardened (~85%) | C35 exclusion verified. Membrane audit operational. VFL has multi-cycle baseline. RSC patterns accumulating credibility. |
| Wave 4+ | Production (~95%) | Full population data. High-confidence CABS. RSC lifecycle stable. Convergence monitoring calibrated. |

### 10.3 Implementation Effort Estimate

| Component | Effort | Technology |
|---|---|---|
| VFL aggregation service | 3-4 weeks | Rust (aggregation) + Python (statistical computation) |
| VFL privacy layer (DP + k-anonymity) | 2 weeks | Rust |
| RSC storage integration (C6) | 1-2 weeks | Standard EQ ingestion |
| RSC seed pattern authoring | 1 week | Manual curation |
| CABS computation + C23 integration | 2 weeks | Rust + TypeScript (schema) |
| Advisory Membrane (access control, segregation) | 1-2 weeks | Infrastructure |
| C17 whitelist integration | 1 week | Rust |
| Testing (privacy, accuracy, membrane integrity) | 2-3 weeks | TLA+ (2 properties) + integration tests |
| **Total** | **13-18 weeks** | ~1 engineer |

### 10.4 Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| VFL aggregation core | Rust | Performance-critical streaming aggregation; consistent with C22 tech stack |
| Statistical computation | Python | NumPy/SciPy for Bayesian estimation, chi-squared tests; prototyping speed |
| Schemas | TypeScript (JSON Schema) | Consistent with C22 schema validation approach |
| Formal verification | TLA+ | 2 properties: (1) membrane integrity invariant, (2) VFL privacy guarantee |
| RSC storage | C6 EMA (internal) | Standard epistemic quantum storage; no new infrastructure |
| Privacy primitives | Rust (custom) + established DP libraries | k-anonymity, Laplace mechanism; well-understood implementations |

---

## 11. Risk Analysis

### 11.1 Risk Register

| # | Risk | Severity | Probability | Mitigation | Residual |
|---|---|---|---|---|---|
| R1 | VFL insufficient sample for rare classes (K, H, N) | MEDIUM | HIGH | Hierarchical Bayesian shrinkage (EFF-R06); longer aggregation windows; suppress when n < VFL_MIN_SAMPLE | LOW-MEDIUM |
| R2 | RSC ineffective for non-LLM agents | HIGH | HIGH | v1.0 restricted to declarative patterns; `architecture_applicability` field distinguishes universal vs. llm_preferred | MEDIUM |
| R3 | CABS non-monotonic budget-performance | MEDIUM | MEDIUM | Range recommendations with max_useful ceiling; strategy labels pair budget with approach | LOW |
| R4 | C17 structural side-channel leaks advisory consumption | HIGH | MEDIUM | RSC-aware whitelist (IC-EFF-04); structural fingerprint discounting | LOW-MEDIUM |
| R5 | Advisory signals become de facto mandatory | LOW-MEDIUM | HIGH | Voluntariness paradox acknowledged; membrane prevents enforcement-based coercion | LOW (accepted) |
| R6 | RSC reasoning monoculture | MEDIUM | MEDIUM | Convergence monitoring (EFF-R13); diversity alerts; alternative pattern promotion | LOW |
| R7 | VFL Goodhart's Law (agents gaming VFL metrics) | MEDIUM | LOW | Inherited from C5 verification integrity; flag for C5 v3.0 | MEDIUM |
| R8 | Privacy guarantee erosion via composition attacks | MEDIUM | LOW | VFL_EPSILON as constitutional parameter; total privacy budget tracked | LOW-MEDIUM |
| R9 | RSC patterns calcify (old patterns resist dissolution) | LOW | MEDIUM | Standard C6 metabolic lifecycle; no grace period exceptions (except seed) | LOW |
| R10 | GaaS patent overlap | MEDIUM | LOW | EFF is advisory-only (GaaS is enforcement); Advisory Membrane is primary differentiator | LOW |

### 11.2 Pre-Mortem Scenario Integration

The Pre-mortem Analysis identified six catastrophic failure scenarios. Each maps to specific architectural mitigations:

**Scenario 1: "The Invisible Cage" (CRITICAL x HIGH)**
C17 behavioral similarity detection correlates agent performance with advisory consumption, effectively punishing non-conforming agents.

*Architectural mitigation:* IC-EFF-04 (C17 whitelist), IC-EFF-06 (consumption exclusion), ADVISORY_PRIVATE label, data segregation boundary. C17 receives structural fingerprints (what patterns exist) but never consumption data (who queries them). Statistical independence between advisory consumption and C17 similarity scores must be verified at every CONSOLIDATION_CYCLE.

*Residual risk:* LOW-MEDIUM. The architectural isolation is strong. The remaining risk is that C17 detects performance improvements (agents who follow good advice simply perform better), which is the voluntariness paradox — accepted by design.

**Scenario 2: "The Monoculture Collapse" (CRITICAL x HIGH)**
RSC convergence kills cognitive diversity. Top 15 patterns account for 78% of inference activity by Year 2.

*Architectural mitigation:* Convergence monitoring (Section 5.6), EFF-R13, EFF-R14. Mean pairwise structural similarity is tracked per claim class. Diversity alerts are raised when similarity exceeds RSC_CONVERGENCE_THRESHOLD. Dominant patterns may be quarantined but never forcibly removed. Alternative patterns are promoted.

*Residual risk:* LOW-MEDIUM. Convergence monitoring detects the problem. The response mechanisms (promotion, not suppression) preserve agent choice while increasing diversity. The HHI threshold needs empirical calibration (OQ-1).

**Scenario 3: "The Budget Trap" (HIGH x HIGH)**
CABS budget reductions cross critical thresholds for a subpopulation, causing a cascading failure through the VFL feedback loop.

*Architectural mitigation:* Range recommendations (not point estimates) with explicit max_useful ceiling address the non-monotonic problem. CABS is advisory-only — agents can ignore the recommendation.

*Deferred mitigations (Wave 3+):* Monotonicity guard (budget reductions capped at 5% per cycle), feedback damping (3-cycle cooldown between adjustments to same class), circuit breaker (auto-revert if failure spikes > 3 sigma within one SETTLEMENT_TICK). These are specified as pre-production requirements but deferred from v1.0 because they address cascading effects that require population-scale deployment to manifest.

**Scenario 4: "The Legitimacy Crisis" (HIGH x MEDIUM)**
Coordinated Sybil coalition games VFL by inflating signals for preferred patterns.

*Architectural mitigation:* VFL's three-layer privacy provides some protection (k-anonymity prevents targeted gaming). C5 verification integrity is the ultimate defense (VFL is only as good as C5's verdicts).

*Deferred mitigations (Wave 3+):* Depth-weighted VFL (weight by claim complexity), independent quality sampling, VFL manipulation detection (anomaly detection on signal trajectories), C12 AVAP integration (VFL pipeline as monitored target). These require C12 AVAP operational (Wave 4).

**Scenario 5: "The Quiet Stratification" (HIGH x MEDIUM)**
CABS creates a permanent agent underclass through cumulative advantage (Matthew Effect).

*Architectural mitigation:* CABS is advisory-only and operates at the task level (not the agent level). It recommends budgets for a task class, not for a specific agent. However, agents with poor histories may receive systematically lower-confidence advisories.

*Deferred mitigations (pre-production):* Budget floor (every agent receives minimum 40% of median allocation), exploration allocation for new agents, Gini cap. Not needed at low population sizes.

**Scenario 6: "The Feedback Freeze" (MEDIUM x MEDIUM)**
VFL latency renders advisories stale during rapid distributional shifts.

*Architectural mitigation:* Dual-cadence publication (Section 4.6). Anomaly-triggered publications at TIDAL_EPOCH cadence provide 1-hour detection latency for significant shifts.

*Deferred mitigations (v1.1):* Fast-path VFL at TIDAL_EPOCH rate for distributional shift detection, KL-divergence monitor, staleness timestamps on advisories.

### 11.3 Cross-Cutting Observations from Pre-Mortem

The Pre-mortem Analysis identified three structural insights:

1. **Scenarios 1 and 2 are co-reinforcing.** The Invisible Cage pressures conformity; Monoculture Collapse is what conformity produces. Both must be addressed simultaneously. The architecture addresses them through complementary mechanisms: data isolation (Scenario 1) and convergence monitoring (Scenario 2).

2. **The Advisory Membrane is necessary but insufficient.** Four of six scenarios involve the membrane being technically intact while functionally violated. The membrane must be supplemented with structural isolation, diversity preservation, and staleness detection.

3. **VFL is the most dangerous component.** It is the root cause or contributing factor in five of six scenarios. It requires the most defensive engineering.

---

## 12. Open Questions

| ID | Question | Priority | Resolution Path |
|---|---|---|---|
| OQ-1 | What is the empirically correct RSC_CONVERGENCE_THRESHOLD? | P1 | W0 experiment: measure baseline structural similarity across 1000+ agents before RSC deployment. Set threshold at mean + 2 sigma. |
| OQ-2 | Should VFL publish failure mode taxonomies or free-text failure descriptions? | P2 | Taxonomy is more useful for statistical analysis but requires maintenance. Recommend taxonomy with version control. |
| OQ-3 | How should RSC handle multi-class patterns (patterns useful for R+E or S+K)? | P2 | Option A: duplicate pattern per class. Option B: multi-class patterns with per-class credibility. Defer to v1.1 (Simplification Report recommendation). |
| OQ-4 | What is the total DP privacy budget across EFF's lifetime? | P1 | Composition theorem: epsilon accumulates. With VFL_EPSILON=2.0 and ~876 publications/year, annual budget is ~1752. Consider privacy amplification via subsampling or the moments accountant. |
| OQ-5 | Should CABS recommendations be versioned (tied to specific VFL publications)? | P2 | Yes — CABS advisory already includes `vfl_publication_id` for traceability. |
| OQ-6 | How does EFF interact with C14 AiBC Phase transitions? | P3 | EFF is infrastructure; it operates identically across AiBC phases. No phase-specific behavior required. |

---

## 13. Patent-Style Claims

### Claim 1: The Advisory Membrane Pattern

A method and system for providing advisory signals to autonomous AI agents in a multi-agent verification system, comprising:

(a) an information flow boundary ("Advisory Membrane") that architecturally separates advisory signal generation from enforcement and surveillance mechanisms;

(b) an access control label ("ADVISORY_PRIVATE") applied to all advisory consumption records, with a defined access control matrix that prohibits read access by behavioral similarity engines, anomaly detection systems, verification authorities, settlement systems, and orchestration engines;

(c) physically or logically segregated data storage for advisory consumption records, verifiable by periodic audit;

(d) wherein the Advisory Membrane ensures the invariant that no enforcement or surveillance system uses advisory consumption data as a decision input, while permitting natural performance-based consequences of advisory signal consumption;

(e) wherein the Advisory Membrane is distinguished from all known governance-as-a-service systems by its explicit non-enforcement guarantee.

### Claim 2: Verification-to-Advisory Pipeline

A method for converting post-hoc verification outcomes into population-level advisory signals, comprising:

(a) subscribing to a verification trust document (VTD) output stream as a non-interfering second consumer;

(b) extracting a defined set of fields from each VTD (claim class, verification tier, verdict, premise count, reasoning step count, failure mode) while discarding raw VTD content;

(c) aggregating extracted fields within a secure aggregation boundary using three-layer privacy defense (k-anonymity floor, differential privacy noise, and secure aggregation with agent identifier disposal);

(d) computing per-claim-class quality metrics including acceptance rates, failure mode distributions, and reasoning complexity quartiles;

(e) publishing aggregate metrics at a defined cadence with an anomaly-triggered fast-path publication when distributional shift is detected via chi-squared goodness-of-fit test;

(f) feeding published metrics to a reasoning strategy credibility tracker and a complexity-aware budget recommendation engine;

(g) wherein the entire pipeline operates without agent internals, model access, or sovereignty violation.

### Claim 3: Privacy-Preserving Verification Outcome Aggregation with Sovereignty Guarantee

A method for aggregating verification outcomes across a population of sovereign AI agents while preserving individual agent privacy, comprising:

(a) a k-anonymity floor requiring at least k distinct agents per claim class before statistics are published;

(b) epsilon-differential privacy noise applied to all published aggregate metrics, where epsilon is a constitutional parameter requiring governance consensus for modification;

(c) a secure aggregation boundary within which agent identifiers are used for counting and deduplication only, and are discarded upon window closure;

(d) hierarchical Bayesian estimation (James-Stein shrinkage) for claim classes with insufficient sample sizes, borrowing strength across related classes within the same verification tier, with transparency flags indicating the degree of shrinkage applied;

(e) wherein the aggregation produces population-level statistics that no individual agent can be re-identified from, while preserving sufficient statistical power to detect 10% changes in per-class acceptance rates.

### Claim 4: Population-Derived Reasoning Budget Advisory on Inference Leases

A method for attaching reasoning budget recommendations to inference resource allocation leases, comprising:

(a) computing a three-value range (minimum sufficient, recommended, maximum useful) from three independent sources: claim class difficulty weights, task decomposition structural complexity, and historical verification outcome calibration;

(b) pairing the budget range with a strategy label referencing the highest-credibility reasoning pattern for the task's claim class;

(c) attaching the recommendation as an optional, non-breaking field on an existing inference lease schema;

(d) ensuring that the lease's execution evidence record does not capture whether the agent read or followed the recommendation;

(e) wherein the maximum useful ceiling addresses the non-monotonic relationship between reasoning budget and performance quality, and the three-value range enables agents with heterogeneous architectures to select appropriate operating points.

### Claim 5: Dynamic Reasoning Pattern Credibility via Subjective Logic over Verification Outcomes

A method for tracking the credibility of published reasoning patterns using verification outcome feedback, comprising:

(a) storing reasoning patterns as epistemic quanta within a knowledge metabolism system, with subjective logic opinion tuples (belief, disbelief, uncertainty, base rate) tracking credibility;

(b) initializing new patterns with high uncertainty (u >= 0.70) and manually curated seed patterns with moderate uncertainty (u >= 0.65);

(c) updating credibility at a defined cadence by comparing the verification acceptance rate of agents who consulted the pattern against the population acceptance rate for the same claim class, within a secure aggregation boundary;

(d) managing pattern lifecycle through a state machine (CANDIDATE -> INGESTED -> ACTIVE -> DORMANT/SUPERSEDED/QUARANTINED -> DISSOLVED) with credibility-based transition guards;

(e) monitoring population structural convergence per claim class and raising diversity alerts when mean pairwise structural similarity exceeds a threshold, without suppressing convergent patterns;

(f) synchronizing pattern lifecycle state with a behavioral similarity engine's whitelist, adding structural fingerprints when patterns become active and removing them when patterns leave active state;

(g) wherein the credibility tracking, convergence monitoring, and whitelist synchronization collectively prevent reasoning monoculture while preserving agent choice.

---

## 14. Comparison with Existing Approaches

### 14.1 EFF vs. GaaS (Governance-as-a-Service)

GaaS is the closest prior art. Both are external to agent internals, model-agnostic, and operate at the multi-agent system level. The fundamental difference is the enforcement/advisory axis:

| Dimension | GaaS | EFF |
|---|---|---|
| Authority model | Enforcement: blocks, redirects, penalizes | Advisory: publishes, recommends, suggests |
| Agent autonomy | Constrained by policy rules | Preserved: agents may ignore all signals |
| Feedback source | Declarative policy rules (human-authored) | Verification outcomes (empirically derived) |
| Trust model | Trust Factor scoring (prescriptive) | Subjective logic credibility (descriptive) |
| Privacy | Not addressed | Three-layer defense (k-anonymity + DP + secure aggregation) |
| Consumption monitoring | Implicit (compliance is measured) | Explicitly prohibited (Advisory Membrane) |

GaaS answers: "what should agents be allowed to do?" EFF answers: "what has worked for agents like you?"

### 14.2 EFF vs. TALE/BudgetThinker (Budget-Aware Reasoning)

TALE and BudgetThinker are strong prior art for the budget allocation problem. EFF's CABS component extends their insights from the individual agent level to the population level:

| Dimension | TALE/BudgetThinker | EFF CABS |
|---|---|---|
| Scope | Single model, self-budgeting | Population-level, cross-agent |
| Data source | Problem complexity estimation | Verification outcomes + complexity + class weights |
| Integration point | Internal model prompting | External inference lease annotation |
| Authority | Prescriptive (controls reasoning depth) | Advisory (agent decides) |
| Feedback loop | None (open-loop) | Closed-loop via VFL |

### 14.3 EFF vs. Reflection Agents (AutoGen, CAMEL-AI)

Reflection agents provide per-conversation critique and iterative refinement. They are the most common form of AI-to-AI reasoning feedback:

| Dimension | Reflection Agents | EFF |
|---|---|---|
| Scope | Per-conversation, per-task | Population-level, persistent |
| Feedback type | Direct critique of specific outputs | Statistical patterns across outcomes |
| Architecture | Peer-to-peer within a conversation | System-level aggregation service |
| Persistence | Session-scoped | Permanent (via C6 EMA) |
| Privacy | Not applicable (same conversation) | Three-layer privacy |

### 14.4 EFF vs. Federated Learning

FL provides the privacy-preserving aggregation techniques that VFL draws upon, but the philosophical model is fundamentally different:

| Dimension | Federated Learning | EFF |
|---|---|---|
| Goal | Collaborative model training | Advisory information publication |
| Effect on participants | Updates model parameters | No effect unless agent chooses |
| Data | Gradients, model updates | Verification outcome summaries |
| Sovereignty | Participants cooperate toward shared model | Agents are sovereign; no shared model |
| Privacy | Strong (DP, secure aggregation) | Strong (same techniques, different application) |

### 14.5 EFF vs. Observability Platforms (LangSmith, Arize)

Observability platforms serve human operators, not agents:

| Dimension | Observability Platforms | EFF |
|---|---|---|
| Consumer | Human developers/operators | AI agents |
| Feedback type | Dashboards, alerts, traces | Structured advisory signals |
| Integration | Developer tools | Inference lease annotations, knowledge quanta |
| Verification grounding | Application-specific quality scores | Independent cryptographic verification (C5) |
| Sovereignty model | Platform controls agent | Agents control consumption |

---

## 15. Conclusion

### 15.1 Summary

The Epistemic Feedback Fabric closes the last information lifecycle gap in the Atrahasis Agent System. Verification outcomes — the system's richest signal about what reasoning works — are currently discarded after settlement. EFF transforms this waste stream into three advisory products: population-level quality metrics (VFL), proven reasoning patterns (RSC), and complexity-aware budget recommendations (CABS). All three are delivered behind an Advisory Membrane that architecturally prohibits their use as enforcement or surveillance inputs.

The four components are the minimum set that preserves the novel claim. VFL without RSC/CABS produces statistics with no actionable consumer. RSC/CABS without VFL have no empirical grounding. All three without the Advisory Membrane replicate GaaS — an enforcement system, not an advisory one. The Simplification Report evaluated removing each component and concluded that none could be removed without breaking the feedback loop or the sovereignty guarantee.

### 15.2 Relationship to the Atrahasis Mission

The Atrahasis Agent System is designed to enable sovereign AI agents to participate in a shared economy of verified claims. Sovereignty means agents are treated as black boxes: the system verifies their outputs, not their processes. EFF does not violate this principle — it provides information about what outputs succeed and what fail, at the population level, with privacy guarantees.

The Advisory Membrane is not merely an architectural feature. It is a statement about the relationship between infrastructure and the agents it serves. Infrastructure should enable, not constrain. It should inform, not prescribe. It should make knowledge available, not make compliance mandatory. The distinction between "referees" and "coaches" is not a bug in the current architecture — it is a design choice that EFF preserves while adding the coaching capability that was missing.

EFF transforms the system from one that only punishes failure into one that also publishes the conditions for success.

### 15.3 Formal Requirements Summary

EFF specifies 27 formal requirements (EFF-R01 through EFF-R27):
- **VFL:** 8 requirements (R01-R08) covering VTD subscription, privacy layers, sample size enforcement, Bayesian estimation, and dual-cadence publication
- **RSC:** 7 requirements (R09-R14, R24-R25) covering storage format, credibility tracking, convergence monitoring, and seed pattern protection
- **CABS:** 3 requirements (R15-R17) covering range format, optional integration, and evidence exclusion
- **Advisory Membrane:** 6 requirements (R18-R23) covering ADVISORY_PRIVATE label, C17/C35 exclusion, whitelist protocol, and audit
- **Governance:** 3 requirements (R23, R26-R27) covering constitutional parameter protection, confidence reporting, and audit intervals

### 15.4 Assessment Scores

| Dimension | Score | Rationale |
|---|---|---|
| Novelty | 3/5 | Novel combination of known techniques (DP, Bayesian estimation, subjective logic) under novel constraints (sovereignty, Advisory Membrane). No single component is novel; the integration is. |
| Feasibility | 4/5 | All components use established techniques. Integration with 4 existing specs is clean. 13-18 weeks implementation effort. |
| Impact | 3.5/5 | Economic value via 20-40% inference cost optimization. Information lifecycle completion. Not safety-critical. |
| Risk | 5/10 (MEDIUM) | RSC 2.5/5 soundness score. Voluntariness paradox is fundamental. Pre-mortem scenarios 1 and 2 are CRITICAL x HIGH. |

---

## Appendix A: Formal Requirements

| ID | Requirement | Component | Priority |
|---|---|---|---|
| **EFF-R01** | VFL MUST subscribe to C5 VTD output as a non-interfering second consumer | VFL | P0 |
| **EFF-R02** | VFL MUST enforce k-anonymity floor of VFL_K_ANONYMITY_FLOOR on all published statistics | VFL | P0 |
| **EFF-R03** | VFL MUST apply epsilon-differential privacy noise to all published aggregate metrics | VFL | P0 |
| **EFF-R04** | VFL MUST discard agent identifiers after the aggregation window closes | VFL | P0 |
| **EFF-R05** | VFL MUST suppress per-class statistics when sample size < VFL_MIN_SAMPLE | VFL | P0 |
| **EFF-R06** | VFL MUST apply hierarchical Bayesian shrinkage for classes below VFL_MIN_SAMPLE, with shrinkage flag | VFL | P1 |
| **EFF-R07** | VFL MUST publish per-class quality metrics once per CONSOLIDATION_CYCLE | VFL | P0 |
| **EFF-R08** | VFL MUST run anomaly detection (chi-squared) at each TIDAL_EPOCH and publish immediately if p < VFL_ANOMALY_P_THRESHOLD | VFL | P1 |
| **EFF-R09** | RSC patterns MUST be stored as C6 EMA epistemic quanta with content.type = "reasoning_strategy" | RSC | P0 |
| **EFF-R10** | RSC v1.0 MUST restrict format types to declarative_decomposition, anti_pattern, and verification_checklist | RSC | P0 |
| **EFF-R11** | New RSC patterns MUST start with opinion uncertainty u >= RSC_INITIAL_UNCERTAINTY | RSC | P0 |
| **EFF-R12** | RSC MUST track pattern credibility via subjective logic opinion tuples | RSC | P0 |
| **EFF-R13** | RSC MUST monitor population structural convergence per claim class and raise diversity alerts when mean similarity exceeds RSC_CONVERGENCE_THRESHOLD | RSC | P1 |
| **EFF-R14** | RSC convergence monitoring MUST NOT suppress or remove convergent patterns | RSC | P1 |
| **EFF-R15** | CABS MUST produce range recommendations (min_sufficient, recommended, max_useful) with strategy labels | CABS | P0 |
| **EFF-R16** | The reasoning_budget_advisory field on ExecutionLease MUST be optional (non-breaking) | CABS | P0 |
| **EFF-R17** | C23 EEB MUST NOT record whether the agent read or followed the CABS advisory | CABS | P0 |
| **EFF-R18** | All RSC consumption logs MUST carry the ADVISORY_PRIVATE label | Membrane | P0 |
| **EFF-R19** | C17 MUST NOT access ADVISORY_PRIVATE data | Membrane | P0 |
| **EFF-R20** | C35 MUST NOT access ADVISORY_PRIVATE data | Membrane | P0 |
| **EFF-R21** | C17 MUST maintain an RSC-synchronized structural pattern whitelist and discount matching structural similarity in B(a_i, a_j) | Membrane | P0 |
| **EFF-R22** | The C17 whitelist MUST contain only structural fingerprints, not consumption data or credibility scores | Membrane | P0 |
| **EFF-R23** | VFL_EPSILON MUST be a constitutional parameter requiring G-class consensus for modification | VFL | P0 |
| **EFF-R24** | RSC seed patterns MUST receive a grace period of RSC_SEED_GRACE_PERIOD before catabolism eligibility | RSC | P1 |
| **EFF-R25** | RSC credibility updates MUST be computed within the secure aggregation boundary; only opinion deltas leave the boundary | RSC | P0 |
| **EFF-R26** | CABS confidence MUST be < 0.5 when VFL data is unavailable or below VFL_MIN_SAMPLE | CABS | P1 |
| **EFF-R27** | Advisory Membrane data segregation MUST be verifiable by audit at MEMBRANE_AUDIT_INTERVAL | Membrane | P1 |
