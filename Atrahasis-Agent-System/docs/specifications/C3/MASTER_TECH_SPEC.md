# Tidal Noosphere: A Unified Coordination Architecture for Planetary-Scale Epistemic Systems
## Master Technical Specification — C3-A
## Version 2.0

**Invention ID:** C3
**Concept:** C3-A Tidal Noosphere
**Date:** 2026-03-10
**Status:** DESIGN — Final Consolidation (Unified Rewrite)
**Predecessor Specs:** Noosphere Master Spec v5, PTA Complete Design v0.1, Locus Fabric (conceptual)
**Assessment Council Verdict:** CONDITIONAL_ADVANCE (Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 7/10)
**Primary Scale Target:** 1,000-10,000 agents (100K+ aspirational, contingent on Phase 3 empirical results)

**Version History:**
- v1.0 (2026-03-09): Initial Master Tech Spec
- v2.0 (2026-03-10): Unified rewrite integrating Patch Addendum v1.1, C9 Cross-Layer Reconciliation, C10 Hardening Addenda (Reconfiguration Storm, VRF Grinding & Small-Ring, Emergency Rollback), and C12 AVAP integration points

---

## Abstract

The Tidal Noosphere is a unified coordination architecture for autonomous AI agents performing verified knowledge work at planetary scale. It solves a problem that no existing system addresses: how to coordinate thousands of heterogeneous autonomous agents in epistemic tasks — tasks involving knowledge claims, verification, contradiction resolution, and governance — while providing formal correctness guarantees, constitutional protection of verification quality, and near-zero communication overhead in steady state.

The architecture is formed by synthesizing three independently developed designs. The Noosphere, a homeostatic verification-first epistemic coordination fabric, provides the verification membrane, claim classification, knowledge persistence, and constitutional governance framework. The Predictive Tidal Architecture (PTA) contributes deterministic O(1) per-agent scheduling via bounded-loads consistent hash rings, epoch-based coordination, and surprise-only predictive communication. The Locus Fabric supplies mandatory I-confluence proof obligations that formally ground the operation-class algebra.

The key technical contributions are: (1) a five-class operation algebra (M/B/X/V/G) that derives agreement cost from operation type using I-confluence theory, enabling coordination-free execution for proven operations; (2) deterministic tidal scheduling within elastic parcel boundaries using bounded-loads consistent hashing, achieving O(1) per-agent steady-state overhead; (3) a VRF dual defense combining commit-reveal protocols with pre-stratified diversity pools — hardened with hidden diversity attributes, randomized filter thresholds, and escalating cooling periods — bounding adversary advantage to less than 3% above stake-proportional baseline; (4) dual-mechanism communication with intra-parcel predictive delta (zero communication when agents follow schedule) and locus-scope stigmergic decay; (5) Emergency Tidal Rollback providing sub-5-epoch recovery from scheduling crises via two-tier ETR (standard 90% supermajority plus critical 67%-of-reachable), three-channel governance redundancy, a known-good version registry, and a formal SAFE_MODE state machine; and (6) integration points for C12 AVAP anonymous committee selection with encrypted VRF assignment tokens and cover traffic.

The architecture targets 1,000-10,000 agents as its validated design point, with 100,000+ retained as a Phase 4 research aspiration. The feasibility score is 3/5 — the building blocks are proven but the composition at scale is unprecedented, the I-confluence cold-start problem is real, and a 170x gap exists between the highest demonstrated autonomous agent coordination (590 agents) and the aspiration target. This document provides the complete specification needed to begin implementation, while being honest about what remains unproven.

---

## Table of Contents

- [1. Introduction](#1-introduction)
  - [1.1 The Coordination Problem](#11-the-coordination-problem)
  - [1.2 Three Architectural Lineages](#12-three-architectural-lineages)
  - [1.3 The Synthesis Decision](#13-the-synthesis-decision)
  - [1.4 Design Philosophy](#14-design-philosophy)
  - [1.5 Scope and Scale Targets](#15-scope-and-scale-targets)
- [2. Architecture Overview](#2-architecture-overview)
  - [2.1 Three Structural Levels](#21-three-structural-levels)
  - [2.2 Component Map](#22-component-map)
  - [2.3 Data Flow](#23-data-flow)
- [3. Operation-Class Algebra](#3-operation-class-algebra)
  - [3.1 The Five Classes](#31-the-five-classes-mbxvg)
  - [3.2 Claim Classification Protocol](#32-claim-classification-protocol)
  - [3.3 I-Confluence Foundation](#33-i-confluence-foundation)
  - [3.4 Bootstrap: From Cold Start to Full Coverage](#34-bootstrap-from-cold-start-to-full-coverage)
- [4. Tidal Scheduling](#4-tidal-scheduling)
  - [4.1 Consistent Hash Rings Within Parcels](#41-consistent-hash-rings-within-parcels)
  - [4.2 Bounded-Loads Variant (Hardened)](#42-bounded-loads-variant-hardened)
  - [4.3 Three-Tier Temporal Hierarchy](#43-three-tier-temporal-hierarchy)
  - [4.4 Task Assignment Algorithm](#44-task-assignment-algorithm)
  - [4.5 Agent Churn Handling](#45-agent-churn-handling)
  - [4.6 Adaptive Virtual Nodes](#46-adaptive-virtual-nodes)
  - [4.7 Epoch-Boundary Load Rebalancing](#47-epoch-boundary-load-rebalancing)
  - [4.8 Minimum Parcel Size and Merge Protocol](#48-minimum-parcel-size-and-merge-protocol)
  - [4.9 Storm Detection and Throttled Reconfiguration](#49-storm-detection-and-throttled-reconfiguration)
  - [4.10 Staggered Reconfiguration Protocol](#410-staggered-reconfiguration-protocol)
- [5. Verification Architecture](#5-verification-architecture)
  - [5.1 The Verification Membrane](#51-the-verification-membrane)
  - [5.2 VRF Dual Defense (Hardened)](#52-vrf-dual-defense-hardened)
  - [5.3 Hidden Diversity Attributes](#53-hidden-diversity-attributes)
  - [5.4 Randomized Filter Thresholds](#54-randomized-filter-thresholds)
  - [5.5 Diversity Attribute Commitment with Cooling Period](#55-diversity-attribute-commitment-with-cooling-period)
  - [5.6 Hardened End-to-End VRF Committee Selection](#56-hardened-end-to-end-vrf-committee-selection)
  - [5.7 VRF Phased Deployment](#57-vrf-phased-deployment)
  - [5.8 VRF Cache Invalidation on Reconfiguration](#58-vrf-cache-invalidation-on-reconfiguration)
  - [5.9 Continuous Re-Verification](#59-continuous-re-verification)
  - [5.10 Nine-Class Claim Taxonomy](#510-nine-class-claim-taxonomy)
  - [5.11 AVAP Integration Points](#511-avap-integration-points)
- [6. Communication Architecture](#6-communication-architecture)
  - [6.1 The Dual-Mechanism Design](#61-the-dual-mechanism-design)
  - [6.2 Predictive Delta Channel](#62-predictive-delta-channel-intra-parcel)
  - [6.3 Stigmergic Decay Channel](#63-stigmergic-decay-channel-locus-scope)
  - [6.4 Boundary Interaction](#64-boundary-interaction)
  - [6.5 In-Flight Signal Routing During Transitions](#65-in-flight-signal-routing-during-transitions)
  - [6.6 Compressed Model Summary for Warm-Start Migration](#66-compressed-model-summary-for-warm-start-migration)
- [7. Governance and Safety](#7-governance-and-safety)
  - [7.1 G-Class Constitutional Consensus](#71-g-class-constitutional-consensus)
  - [7.2 Tidal Function Version Management](#72-tidal-function-version-management)
  - [7.3 Emergency Tidal Rollback — Standard ETR](#73-emergency-tidal-rollback--standard-etr)
  - [7.4 Emergency Tidal Rollback — Critical ETR](#74-emergency-tidal-rollback--critical-etr)
  - [7.5 Governance Channel Redundancy](#75-governance-channel-redundancy)
  - [7.6 Known-Good Version Registry](#76-known-good-version-registry)
  - [7.7 SAFE_MODE State Machine](#77-safe_mode-state-machine)
  - [7.8 Governance Quorum Freezing During Reconfiguration](#78-governance-quorum-freezing-during-reconfiguration)
  - [7.9 Degradation Priority Ordering](#79-degradation-priority-ordering)
  - [7.10 Cross-Integration Failure Specification](#710-cross-integration-failure-specification)
  - [7.11 Parcel Transition Protocol](#711-parcel-transition-protocol)
- [8. Economic Settlement](#8-economic-settlement)
  - [8.1 Threshold Calibration Coupling](#81-threshold-calibration-coupling)
- [9. AASL Extension](#9-aasl-extension)
  - [9.1 Type Retirement Mechanism](#91-type-retirement-mechanism)
- [10. Security Analysis](#10-security-analysis)
  - [10.1 Threat Model](#101-threat-model)
  - [10.2 Attack Resistance (Hardened)](#102-attack-resistance-hardened)
  - [10.3 Coalition Analysis (Hardened)](#103-coalition-analysis-hardened)
  - [10.4 Sybil Cost Analysis](#104-sybil-cost-analysis)
- [11. Scale Architecture](#11-scale-architecture)
  - [11.1 Phase 1: Development](#111-phase-1-development-1-100-agents)
  - [11.2 Phase 2: Initial Deployment](#112-phase-2-initial-deployment-100-1k-agents)
  - [11.3 Phase 3: Primary Target](#113-phase-3-primary-target-1k-10k-agents)
  - [11.4 Phase 4: Aspiration](#114-phase-4-aspiration-10k-100k-agents)
- [12. Validation Plan](#12-validation-plan)
  - [12.1 Hard Gate Experiments (Amended)](#121-hard-gate-experiments-amended)
  - [12.2 Recommended Experiments](#122-recommended-experiments)
  - [12.3 Hardening Experiments](#123-hardening-experiments)
  - [12.4 Conformance Requirements](#124-conformance-requirements)
- [13. Risk Assessment (Hardened)](#13-risk-assessment-hardened)
- [14. Implementation Roadmap](#14-implementation-roadmap)
  - [14.0 Agent Runtime Architecture](#140-agent-runtime-architecture)
  - [14.1 Deployment Profiles](#141-deployment-profiles)
- [15. Conclusion](#15-conclusion)
- [Appendices](#appendices)
  - [Appendix A: Formal Primitives](#appendix-a-formal-primitives)
  - [Appendix B: Configurable Constants](#appendix-b-configurable-constants)
  - [Appendix C: AASL Type Definitions](#appendix-c-aasl-type-definitions)
  - [Appendix D: Glossary](#appendix-d-glossary)
  - [Appendix E: Cross-Layer Integration Contracts](#appendix-e-cross-layer-integration-contracts)
  - [Appendix F: Attack Trees (Post-Hardening)](#appendix-f-attack-trees-post-hardening)
  - [Appendix G: Load Imbalance Bounds (Post-Hardening)](#appendix-g-load-imbalance-bounds-post-hardening)
  - [Appendix H: Test Vectors](#appendix-h-test-vectors)
  - [Appendix I: Architectural Decisions Register](#appendix-i-architectural-decisions-register)
  - [Appendix J: Open Design Questions](#appendix-j-open-design-questions)
  - [Appendix K: Traceability Matrix](#appendix-k-traceability-matrix)
- [References](#references)
- [Changelog: v1.0 to v2.0](#changelog-v10-to-v20)

---

**Notation and Conventions.** Throughout this specification, pseudocode uses a Python-like syntax with explicit type annotations. Hash functions (SHA256, ECVRF) refer to their standard cryptographic definitions. O(·) notation refers to asymptotic computational complexity. All constants are listed in Appendix B with default values and valid ranges. The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used per RFC 2119 semantics when specifying conformance requirements. All hash ring positions are elements of Z_{2^256}. Settlement amounts are denominated in AIC (Atrahasis Intelligence Coin) with 18 decimal places of precision.

**Temporal terminology (per C9 cross-layer reconciliation):** This specification uses the canonical three-tier temporal hierarchy:
- **SETTLEMENT_TICK** (60 seconds): the atomic temporal unit. Agent identifiers are globally unique 256-bit values. Locus identifiers are hierarchical namespace selectors (e.g., `biology.proteomics.folding`).
- **TIDAL_EPOCH** (3,600 seconds = 60 SETTLEMENT_TICKs): the primary coordination cycle for scheduling, VRF rotation, and parcel management. TICKS_PER_TIDAL_EPOCH = 60.
- **CONSOLIDATION_CYCLE** (36,000 seconds = 10 TIDAL_EPOCHs): the long-horizon cycle for knowledge consolidation, K-class claim processing, and cross-locus reconciliation.

Where this document refers to "epoch" without qualification, it means TIDAL_EPOCH. Where it refers to "tick," it means SETTLEMENT_TICK.

---

## 1. Introduction

### 1.1 The Coordination Problem

The fundamental problem this architecture addresses is: **how do thousands of autonomous AI agents coordinate epistemic work — the production, verification, accumulation, and governance of knowledge — without a central controller, with formal correctness guarantees, and at a scale that no existing system has demonstrated?**

Current approaches to multi-agent coordination fall into three categories, none of which solve this problem.

**Blockchain-based coordination** (Ethereum, Solana) provides strong consistency and Byzantine fault tolerance but is designed for transaction ordering, not knowledge coordination. Blockchains answer "what happened, in what order, under adversarial conditions?" — a transaction-centric question. Epistemic coordination must answer "what is the current verified belief, plan, and capability distribution across agents?" — a fundamentally different question. Total ordering is unnecessary and harmful for intelligence coordination: reasoning tasks have causal dependencies, not temporal dependencies. Proof-of-work and proof-of-stake waste compute that should be used for reasoning.

**Platform-based coordination** (Google A2A, Microsoft Agent Framework) provides interoperability and scaling through centralized infrastructure. But centralized platforms cannot provide the constitutional protections needed for epistemic integrity. When a single entity controls the coordination layer, there is no structural guarantee that verification quality will not be silently degraded for efficiency. The Noosphere's Architectural Commandment — "optimize the rest of the system around the membrane, never optimize the membrane around the rest of the system" — is unenforceable in a platform model.

**Swarm-based coordination** (MegaAgent, CAMEL OASIS) provides decentralization and emergent organization but lacks verification semantics, formal correctness guarantees, and economic incentive structures. The highest demonstrated autonomous LLM-agent coordination is 590 agents (MegaAgent, ACL 2025). Rule-based simulations reach 1 million agents (CAMEL OASIS) but do not perform autonomous epistemic tasks.

The following table summarizes the comparison across the most relevant dimensions:

| Dimension | Blockchain (Ethereum/Solana) | Platform (A2A/Agent FW) | Swarm (MegaAgent/OASIS) | Tidal Noosphere |
|-----------|------------------------------|-------------------------|-------------------------|-----------------|
| Coordination model | Total ordering via consensus | Centralized orchestration | Emergent self-organization | Operation-class algebra |
| Consistency guarantee | Strong (all ops serialized) | Platform-dependent | None (eventual at best) | Per-class (M: CRDT, B: local, X: quorum, V: committee, G: BFT) |
| Verification semantics | Transaction validity only | Application-layer | None | 9-class claim verification membrane |
| Constitutional protection | Governance token voting | Platform owner discretion | None | Formal constitutional consensus (75% BFT) |
| Steady-state comm. cost | O(N) per block | O(1) via central hub | O(N) per agent | O(1) per agent (M-class) |
| Max demonstrated agents | 1M+ validators (Ethereum) | Unknown (proprietary) | 590 autonomous (MegaAgent) | 0 (design stage) |
| Epistemic task support | No | Limited | Partial | Native (core design goal) |
| Formal correctness | Smart contract verification | None standard | None | I-confluence proofs for M-class |
| Economic model | Token-based (PoS) | Subscription/API fees | None standard | Three-budget tidal settlement |

The Tidal Noosphere occupies a genuinely vacant design point: formal per-operation consistency with epistemic semantics and constitutional protection. No existing system combines all three. The cost is implementation risk — the composition is untested at scale.

The gap is 170x between the highest demonstrated autonomous agent coordination (590) and the Tidal Noosphere's aspiration target (100,000+). Even the validated design target of 1,000-10,000 agents represents a 2-17x advance over existing demonstrations. This gap is honest and acknowledged: the theoretical foundations scale, but the composition of all integration points at the target scale has never been tested.

### 1.2 Three Architectural Lineages

The Tidal Noosphere synthesizes three independently developed architectures, each of which solved part of the coordination problem but left significant gaps.

**The Noosphere** (Architecture A, 2,277 lines, 9 design iterations) is a homeostatic verification-first epistemic coordination fabric. It separates stable logical coordination domains (Loci) from elastic physical execution units (Parcels), gates knowledge admission through a claim-class-specific verification membrane with nine canonical claim classes organized in three tiers (see Section 5.10), manages knowledge persistence through a four-tier memory model, and regulates itself through a bi-timescale controller. Its strength is depth: the verification membrane alone spans 10 specification sections with constitutional protection, deep verifier diversity, continuous re-verification, and membrane quality drift detection. Its weakness is that it relies on threshold-based cell assembly for task scheduling — a reactive mechanism that provides no deterministic guarantees and incurs uncontrolled steady-state communication overhead.

**The Predictive Tidal Architecture (PTA)** (Architecture C, 4,438 lines) provides deterministic O(1) per-agent scheduling via consistent hash rings, one per task type, with epoch-based coordination. Its core principle — "agree by computation, communicate only surprises" — means agents independently compute identical schedules from shared inputs, requiring zero communication in steady state. PTA adds a predictive delta communication layer where agents maintain lightweight linear models of each neighbor's behavior and communicate only when prediction errors exceed adaptive thresholds. Its strength is scheduling efficiency: every output is a deterministic pure function of shared inputs, two agents with the same inputs produce identical outputs. Its weakness is that it lacks everything epistemic — no verification membrane, no claim classification, no knowledge persistence, no governance beyond Schelling-point migration.

**The Locus Fabric** (Architecture B, conceptual) grounds the operation-class algebra in I-confluence theory from Bailis et al. (VLDB 2015). It requires machine-checked proofs (TLA+, Coq, F*, or Ivy) as a mandatory prerequisite for declaring an operation coordination-free (M-class). This is unprecedented — as the landscape analysis notes, "formal verification tools remain firmly in the design-time domain" and no existing system uses formal proofs as a runtime classification gate. Its contribution is formal rigor that transforms the Noosphere's M-class classification from an assertion into a proven guarantee. Its weakness is the practical bottleneck this creates: until sufficient operations are formally proven I-confluent, the system cannot achieve its performance claims.

### 1.3 The Synthesis Decision

During the Ideation phase, the Council identified seven convergences where two or more architectures independently arrived at the same design pattern: Locus/Parcel decomposition, the M/B/X/V/G operation-class algebra, VRF-based verifier selection, epoch-based coordination, predictive/surprise communication, formal proof obligations, and constitutional governance protection. These convergences are evidence that the design space has a natural structure — the same solutions emerged from independent analyses of the same problem.

The Council also identified eight novelty gaps where the synthesis creates something no individual architecture or prior system provides:

1. No system uses consistent hash-ring scheduling as the substrate within epistemic coordination domains.
2. No system defines a 5-class operation algebra grounded in I-confluence proofs with machine-checked proof obligations.
3. No system applies VRF sortition with knowledge-domain diversity post-filtering for epistemic claim verification.
4. No system achieves zero-communication steady state through schedule-based prediction within formally bounded domains.
5. No system requires formal proofs as a runtime gate for operation classification.
6. No system combines a constitutionally protected verification membrane with deterministic tidal scheduling.
7. No system implements the dual predictive/stigmergic communication model at complementary granularities.
8. No system implements the recursive self-verification closure where the scheduling function is itself a verified claim within the membrane it schedules.

The prior art search (confidence 4/5) confirmed these gaps across five search areas. The closest system-level analog, ISEK (arXiv:2506.09335), shares the planetary-scale vision but lacks all five technical differentiators. The competitive window is estimated at 18-24 months before convergence from hyperscaler platforms, blockchain generalization, and runtime formal verification could narrow the gap.

**Why unification was chosen over keeping them separate:** PTA alone lacks epistemic depth. The Noosphere alone lacks scheduling efficiency. The Locus Fabric alone lacks implementation detail. Keeping them separate would require three independent integration efforts, each rediscovering the same convergences. Unification eliminates redundancy (one economic model instead of three, one governance mechanism instead of three, one wire format) while preserving each architecture's unique strength. The synthesis fills genuine gaps in each individual architecture rather than creating a Frankenstein assembly.

### 1.4 Design Philosophy

Three principles govern every design decision:

**1. The Membrane is Sovereign.** The Verification Membrane is constitutionally protected. No scheduling optimization, communication reduction, or governance convenience may weaken it. The rest of the system is optimized around the membrane, never the reverse. This is the Noosphere's Architectural Commandment, and it is non-negotiable. A bad controller wastes compute; a bad membrane poisons cognition. Epistemic corruption compounds through the knowledge graph in ways that are much harder to detect than performance degradation.

**2. Agree by Computation, Communicate Only Surprises.** In steady state, agents compute identical schedules from shared inputs via deterministic hash ring evaluation. Communication occurs only when reality deviates from the computable prediction. The system is silent when correct. This is PTA's core design constraint, and it is what enables O(1) per-agent steady-state overhead.

**3. Prove Before You Trust.** The agreement mode for every operation is derived from its type using the operation-class algebra, not chosen ad hoc. For an operation to execute coordination-free (M-class), a machine-checked I-confluence proof must demonstrate that concurrent execution preserves all locus invariants. This is the Locus Fabric's contribution, and it is what transforms performance claims from assertions into guarantees.

**Key invariants** that hold across all system states:

- **INV-1:** The verification membrane is constitutionally protected and cannot be weakened by any mechanism short of G-class constitutional consensus.
- **INV-2:** For identical inputs, all conformant implementations produce identical scheduling and settlement outputs (determinism invariant).
- **INV-3:** Only I-confluence-proven operations may execute coordination-free. Unproven operations default to the highest applicable coordination cost.
- **INV-4:** Parcels are correctness boundaries: operations within a parcel are independent of operations in other parcels (for M-class and B-class). Cross-parcel operations require explicit coordination (X-class Fusion Capsules).
- **INV-5:** Signals decay unless reinforced. The coordination substrate reflects current state, not accumulated history.
- **INV-6:** The system degrades gracefully. Every component failure degrades to a less-efficient but still-correct state. No single failure causes system-wide incorrectness. The formal degradation chain is: NORMAL -> STANDARD_ETR -> CRITICAL_ETR -> SAFE_MODE (Section 7.7).
- **INV-7:** The tidal function is itself a verified claim within the membrane, creating a recursive self-verification closure.

### 1.5 Scope and Scale Targets

This specification targets four deployment phases with progressively increasing scale:

| Phase | Agents | Loci | Parcels | Status |
|-------|--------|------|---------|--------|
| Phase 1: Development | 1-100 | 1-3 | 1-15 | Engineering validation |
| Phase 2: Initial Deployment | 100-1,000 | 10-50 | 20-1,000 | First production value |
| Phase 3: Primary Target | 1,000-10,000 | 50-500 | 250-25,000 | **Validated design point** |
| Phase 4: Aspiration | 10,000-100,000 | 500-5,000 | 5,000-500,000 | Research aspiration |

**What is proven vs. aspirational:**

- *Proven:* The individual building blocks — consistent hashing (Karger 1997, deployed in Dynamo/Cassandra), VRFs (Algorand, Cardano, Internet Computer), CRDTs (Riak, Redis, Cosmos DB), I-confluence analysis (Bailis 2015), epoch-based coordination (Ethereum Beacon Chain at 1M+ validators) — are battle-tested at scale.
- *Simulated but not deployed:* The composition of these building blocks within the Tidal Noosphere's specific integration architecture. The five integration points (hash rings within parcels, VRF dual defense, dual communication, governance with ETR, AASL extension) have been designed and specified but not implemented.
- *Theoretical:* The O(1) per-agent steady-state overhead claim applies only when sufficient operations are M-class certified. The 170x scale gap between demonstrated and target scales means the Phase 4 target is an act of informed faith, not engineering.
- *Aspirational:* 100,000+ agents. This is retained as a research goal contingent on Phase 3 empirical results. All design decisions in this specification are justified at the 1,000-10,000 scale, not the 100,000 scale.

**What this specification covers:**
- System primitives and formal definitions (25 primitives)
- The five-class operation algebra with I-confluence grounding
- Tidal scheduling within parcels via bounded-loads consistent hashing with adaptive virtual nodes and epoch-boundary rebalancing
- VRF-based verifier selection with hardened dual defense (hidden diversity attributes, randomized filter thresholds, escalating cooling periods)
- Nine-class claim taxonomy with three-tier classification (per C9 reconciliation)
- Dual communication: predictive delta (intra-parcel) and stigmergic decay (locus-scope)
- Parcel transition, emergency rollback (two-tier ETR, three-channel governance redundancy, SAFE_MODE), and governance protocols
- Storm detection with graduated circuit breaker and staggered 4-phase reconfiguration
- AASL extension (4 new types, 5 new messages, type retirement mechanism) and settlement with threshold calibration coupling
- Security analysis against 14+ adversarial attacks with Sybil cost analysis
- Scale architecture across four phases with deployment profiles (T1/T2/T3)
- Validation plan with 3+ hard gate experiments, 10+ recommended/hardening experiments
- Implementation roadmap with kill criteria at each phase
- AVAP (C12) integration points for anonymous committee selection

**What this specification does NOT cover:**
- The Noosphere's verification membrane internals (see Noosphere Spec Sections 13-22)
- The Fusion Capsule Epoch Protocol (see Noosphere Spec Section 12)
- PTA Layer 3 Morphogenic Fields (discarded per Science Assessment recommendation)
- The Knowledge Cortex four-tier memory model (see Noosphere Spec Sections 23-25)
- Cross-region federation protocol (deferred to Phase 4)
- The full AVAP anti-collusion architecture (see C12 Master Tech Spec)

---

## 2. Architecture Overview

### 2.1 Three Structural Levels

The Tidal Noosphere organizes agents into a three-level hierarchy designed to separate concerns that change at different rates.

**Level 1: Locus (stable semantic boundary).** A Locus is a stable logical coordination domain defined by a namespace selector, an invariant set, a safety classification, and an epoch class. Loci represent the correctness boundaries of the system — they define what must be true, not how work is organized. A locus for "biology.proteomics" contains all claims, verifications, and coordination related to proteomics research. Loci split rarely, only on semantic grounds and only with governance approval for HIGH+ safety classes. This stability is critical: redrawing correctness boundaries under load is the most dangerous failure mode in any distributed system.

**Level 2: Parcel (elastic physical execution).** Within each Locus, elastic Parcels handle physical execution. A Parcel is a hot object subset with an active agent set, hash rings for scheduling, and a scope load vector (SLV) for monitoring. Parcels split and migrate often — managed by a bi-timescale controller that analyzes rolling access/conflict patterns. The minimum parcel size is PARCEL_MIN_AGENTS (default 5) agents (below which load variance becomes severe and diversity pools become too small for meaningful verification). The key insight is that parcels can reconfigure freely because correctness is guaranteed by the locus invariants, not by parcel boundaries.

**Level 3: Consistent Hash Ring (deterministic scheduling).** Within each Parcel, PTA's Tidal Scheduling Engine operates bounded-loads consistent hash rings — one per active task type. These rings deterministically assign agents to tasks at epoch boundaries. Every agent independently computes the same assignment from the same inputs. There is no scheduling consensus, no leader election, no negotiation. The schedule is a pure function of the tidal function definition, the agent roster, and the epoch number.

**Why this hierarchy:** The three levels separate three rates of change. Loci change on governance timescales (CONSOLIDATION_CYCLEs to longer). Parcels change on load-adaptation timescales (tens of TIDAL_EPOCHs). Hash rings change on TIDAL_EPOCH timescales (every epoch boundary). This separation means that a scheduling reconfiguration (Level 3) does not require a correctness-boundary change (Level 1), and a load-adaptation split (Level 2) does not require governance approval unless it crosses a locus boundary.

```
Locus (stable semantic boundary)
  selector: biology.proteomics
  invariant_set: {conservation.compute_budget, exclusion.protein_db_write}
  safety_class: HIGH
  |
  +-- Parcel A (elastic, 12 agents)
  |     +-- Hash Ring: task.verify (12 agents x 167 vnodes = 2,004 entries)
  |     +-- Hash Ring: task.compute (12 agents x 167 vnodes = 2,004 entries)
  |     +-- Hash Ring: task.audit (12 agents x 167 vnodes = 2,004 entries)
  |
  +-- Parcel B (elastic, 8 agents)
  |     +-- Hash Ring: task.verify (8 agents x 250 vnodes = 2,000 entries)
  |     +-- Hash Ring: task.compute (8 agents x 250 vnodes = 2,000 entries)
  |
  +-- Parcel C (elastic, 5 agents)
        +-- Hash Ring: task.verify (5 agents x 400 vnodes = 2,000 entries)
```

**Note:** Virtual node counts use the adaptive formula from Section 4.6, targeting ~2,000 ring entries regardless of parcel size.

**Concrete example: a parcel split.** Suppose Parcel A in the proteomics locus above has grown to 25 agents and is experiencing load skew — 3 of its 20 task types consume 80% of compute. The bi-timescale controller's fast loop detects the skew (SLV compute dimension exceeds threshold for 5 consecutive epochs). The slow loop initiates a parcel split:

1. *Locus level (unchanged):* The proteomics locus's invariants, safety classification, and namespace selector are unaffected. No governance action is required because the split is within a single locus.
2. *Parcel level (reconfiguration):* Parcel A splits into A1 (15 agents, handling the 3 hot task types) and A2 (10 agents, handling the remaining 17 task types). The PTP's 2-phase + convergence protocol (PREPARE/MIGRATE + STABILIZE; see Section 7.10) manages the transition via the staggered 4-phase reconfiguration protocol (Section 4.10).
3. *Hash ring level (reconstruction):* A1 builds 3 new hash rings using adaptive virtual node counts. A2 builds 17 new hash rings. All agents independently compute these rings from the same roster inputs.
4. *Communication level (reset):* Agents in A1 enter TRANSITIONING mode for their predictive models of agents that were previously in A but are now in A2 (and vice versa). The CompressedModelSummary mechanism (Section 6.6) exports compact model summaries (max 1KB each) to accelerate re-learning. Communication temporarily increases (standard messaging mode) for 3-5 epochs until models reconverge.
5. *Verification level (recomputation):* VRF diversity pools are refreshed for both A1 and A2 using the new roster. VRF cache is invalidated per Section 5.8. Committee selection continues uninterrupted — the membrane never pauses.

This example illustrates the separation of concerns: the locus remains stable (no correctness boundary change), the parcels reconfigure (physical topology changes), the hash rings rebuild (scheduling changes), and the communication layer adapts (temporary overhead increase). At no point is the verification membrane weakened or knowledge admission paused.

### 2.2 Component Map

The Tidal Noosphere consists of 11 components, each with defined interfaces, failure modes, and dependencies.

| # | Component | Purpose | Source |
|---|-----------|---------|--------|
| 1 | **Noosphere Core** | Verification membrane, 9-class claim classification, knowledge persistence, constitutional protection | Noosphere |
| 2 | **Tidal Scheduler** | Deterministic O(1) scheduling via bounded-loads hash rings with adaptive virtual nodes within parcels | PTA Layer 1 |
| 3 | **VRF Engine** | Verifier set computation with hardened dual defense: commit-reveal + pre-stratified diversity pools + hidden dimensions + randomized thresholds | PTA + Noosphere |
| 4 | **Predictive Delta Channel** | Intra-parcel surprise-only communication with linear predictive models, CompressedModelSummary for warm-start migration | PTA Layer 2 |
| 5 | **Stigmergic Decay Channel** | Locus-scope typed, decaying coordination signals with in-flight signal routing during transitions | Noosphere |
| 6 | **Parcel Manager** | Bi-timescale controller, staggered 4-phase reconfiguration with storm detection and graduated circuit breaker | Noosphere + new |
| 7 | **G-Class Governance Engine** | Constitutional consensus for tidal versions, membrane rules, parameters; governance quorum freezing during reconfiguration | Noosphere |
| 8 | **ETR Controller** | Two-tier Emergency Tidal Rollback (Standard + Critical), three-channel governance redundancy, Known-Good Registry, SAFE_MODE state machine | New (C3-A) |
| 9 | **I-Confluence Prover** | Proof obligations, bootstrap library, provisional M-class mechanism | Locus Fabric |
| 10 | **AASL Extension Layer** | 4 new types (TDF, TSK, SRP, STL), 5 new AACP messages, type retirement mechanism | New (C3-A) |
| 11 | **Settlement Calculator** | Deterministic AIC settlement integrating tidal compliance with three-budget model; threshold calibration coupling via SLV_SURPRISE_RATIO | PTA + Noosphere |

**Component relationships:** The Tidal Scheduler and VRF Engine are the computational core — they produce deterministic outputs that all other components consume. The Noosphere Core is the trust core — it gates all knowledge through the verification membrane. The Predictive Delta and Stigmergic Decay channels are the communication layer — they implement the dual-mechanism design. The Parcel Manager is the adaptation layer — it reconfigures the physical topology without disrupting correctness, using the staggered 4-phase protocol with storm detection to prevent cascading reconfiguration. The G-Class Governance Engine and ETR Controller are the governance layer — they manage constitutional changes and emergency responses, with governance quorum freezing during reconfiguration to prevent split-brain. The I-Confluence Prover is the formal methods layer — it determines which operations earn coordination-free execution. The AASL Extension Layer and Settlement Calculator are the integration layer — they connect the Tidal Noosphere to the broader Atrahasis ecosystem.

### 2.3 Data Flow

The primary data flow through the system follows this path: task submission through scheduling, execution, verification, and settlement.

```
TASK LIFECYCLE:

  Agent submits claim (CLM)
       |
       v
  [Noosphere Core] -- classify_claim() --> Classification Seal (CLS)
       |                                    (9-class taxonomy: D/E/S/H/N/P/R/C/K)
       v
  [Tidal Scheduler] -- compute_assignment() --> Task Assignment (TSK)
       |                                          |
       v                                          v
  Agent executes task              [VRF Engine] -- select_diverse_verifiers_v2()
       |                           (hardened: hidden diversity + randomized thresholds)
       v                                          |
  Results submitted                               v
       |                           Verifier committee formed
       v                           (with AVAP anonymous assignment if enabled)
  [Predictive Delta]                              |
  Surprise-only comms                             v
  if deviation detected            [Noosphere Core] -- verify_claim()
       |                           (class-specific pathway: D/E/S/H/N/P/R/C/K)
       v                                          |
  [Stigmergic Decay]                              v
  Locus-scope signals              Membrane Certificate (MCT) or Rejection
  if anomaly sustained                            |
       |                                          v
       v                           [Knowledge Cortex] -- bundle for persistence
  [Sentinel Graph]                                |
  Anomaly detection                               v
       |                           [Settlement Calculator] -- compute settlement
       v                           (with SLV_SURPRISE_RATIO coupling)
  [ETR Controller]                                |
  Two-tier emergency rollback                     v
  if triggers hit                  Settlement Record (STL) published
```

```
TIDAL_EPOCH LIFECYCLE (every 3,600 seconds):

  Epoch Boundary
       |
       +-- [Capacity Snapshot Service] -- gossip agent states (O(N) aggregate)
       |
       +-- [Tidal Scheduler] -- rebuild hash rings if roster changed
       |                        (adaptive virtual nodes per Section 4.6)
       |
       +-- [VRF Engine] -- rotate VRF seed, restratify diversity pools
       |                   (invalidate VRF cache per Section 5.8)
       |
       +-- [Predictive Delta] -- recalibrate models, update thresholds
       |
       +-- [Settlement Calculator] -- compute settlement for completed epoch
       |                              (per-tick within epoch)
       |
       +-- [Parcel Manager] -- evaluate parcel health (storm check first),
       |                       plan reconfigurations via staggered protocol,
       |                       epoch-boundary load rebalancing
       |
       +-- [AASL Extension] -- type activity tracking, retirement checks
```

```
GOVERNANCE LIFECYCLE:

  Standard Version Upgrade:
    Proposal (TDF) --> 72h discussion --> 75% vote --> Overlap period --> Activation

  Standard ETR:
    Sentinel trigger --> 3 governance agents co-sign --> 90% instant vote
    --> Rollback at next epoch boundary --> Governance hold

  Critical ETR:
    Critical trigger (C1-C4) --> Broadcast on best available channel
    --> 67% of reachable agents within 1 epoch
    --> Rollback to Known-Good Registry target
    --> If fails: enter SAFE_MODE

  Tertiary Auto-Rollback:
    5 consecutive failed epochs with no governance communication
    --> Each agent independently reverts to most recent Known-Good version
    --> Enter SAFE_MODE
```

---

## 3. Operation-Class Algebra

### 3.1 The Five Classes (M/B/X/V/G)

The operation-class algebra is the intellectual core of the Tidal Noosphere. It answers the question: for a given operation, what is the minimum coordination cost required to guarantee correctness?

Most distributed systems answer this question ad hoc — developers choose consensus protocols, replication strategies, and consistency levels based on intuition and experience. The Tidal Noosphere answers it systematically: the agreement mode for every operation is *derived* from the operation's type and its interaction with locus invariants, never chosen manually. This derivation is grounded in I-confluence theory (Bailis et al., VLDB 2015), which provides a formal criterion for determining when concurrent execution is safe.

The five classes, ordered from least to most coordination cost:

**M-Class (Merge/Convergence) — Zero coordination.**
- *What it is:* CRDT-like state updates that preserve all locus invariants under arbitrary concurrent execution. No coordination beyond authenticated anti-entropy.
- *Precondition:* A machine-checked I-confluence proof exists (certified or provisional) for the operation type against the locus invariant set.
- *Communication cost:* Zero consensus overhead. State synchronization at epoch boundaries via capacity snapshot.
- *Per-operation cost:* O(1).
- *Example operations:* G-Counter increment, G-Set add, signal emission, signal reinforcement, reputation accumulation.
- *Why it matters:* M-class operations are the system's performance engine. When most traffic is M-class, the system achieves its O(1) steady-state overhead claim. The cold-start problem (Section 3.4) is precisely the challenge of getting enough operations into this class.
- *SAFE_MODE override:* In SAFE_MODE (Section 7.7), all operations including M-class are treated as X-class. This is the constitutionally authorized correctness-first override.

**B-Class (Bounded Local Commit) — Local-only coordination.**
- *What it is:* Operations that consume a resource governed by a conservation law. Execution is local: the agent decrements its own Certified Slice Object (CSO) without contacting other agents. Rebalancing occurs at epoch boundaries.
- *Precondition:* The operation's resource/invariant pair is CSO-eligible — meaning the resource has a conservation law and local non-negativity can be enforced.
- *Communication cost:* Zero for local spend. O(N) aggregate at epoch-boundary rebalancing.
- *Per-operation cost:* O(1) per operation; amortized rebalancing.
- *Example operations:* CSO local spend (compute, bandwidth, storage allocation).

**X-Class (Exclusive) — Quorum coordination.**
- *What it is:* The default class for operations without I-confluence proofs and without CSO eligibility. Requires serial commit within a single parcel, or Fusion Capsules for multi-parcel operations, or Cut Commit as a last resort for complex cross-locus operations.
- *Precondition:* None — this is the safe default.
- *Communication cost:* Quorum protocol within replica group.
- *Per-operation cost:* O(N_replicas) per operation.
- *Example operations:* Lease acquisition, exclusive resource mutation, cross-parcel state updates.
- *Why it is the default:* Safety. An unproven operation might violate invariants under concurrent execution. X-class serialization prevents this at the cost of higher latency and communication.

**V-Class (Verification) — Committee protocol.**
- *What it is:* All claim verification through the membrane. A VRF-selected committee applies claim-class-specific verification protocols. The committee size, diversity requirements, and verification depth are determined by the claim's class (from the nine-class taxonomy, Section 5.10) and the locus safety level.
- *Mechanism:* VRF-selected committee with hardened dual defense (Section 5.2), claim-class-specific verification pathway (per Noosphere Spec Sections 13-22).
- *Communication cost:* Committee protocol (bounded by committee size, default 7).
- *Per-claim cost:* O(committee_size).

**G-Class (Governance) — BFT constitutional consensus.**
- *What it is:* Operations that change the rules of the system: tidal function version updates, membrane rule modifications, constitutional amendments, slashing decisions.
- *Mechanism:* BFT consensus. 75% supermajority for standard governance. 90% instant supermajority for Standard ETR. 67% of reachable agents for Critical ETR.
- *Communication cost:* All governance agents participate via governance channel (independent of tidal-scheduled data plane; see three-channel architecture in Section 7.5).
- *Per-action cost:* O(N_governance).
- *Why Schelling-point was rejected:* PTA originally used Schelling-point migration for tidal version governance — agents independently switch to the version they observe most peers using. The Ideation Council rejected this because it provides no constitutional protection: a sufficiently large coalition can force version changes without formal review, potentially weakening the verification membrane. G-class governance, while slower (72-hour discussion period), provides constitutional guarantees that Schelling-point cannot.

### 3.2 Claim Classification Protocol

Every operation is classified through a deterministic decision procedure:

```
function classify(op: Operation) -> OperationClass:
  // Step 1: Check if governance operation
  if op.op_type in GOVERNANCE_OPS:
    return G

  // Step 2: Check if verification operation
  if op.op_type in VERIFICATION_OPS:
    return V

  // Step 3: Check for I-confluence proof (certified or provisional)
  if has_certified_proof(op.op_type) or has_provisional_proof(op.op_type):
    return M

  // Step 4: Check for CSO eligibility
  if is_cso_eligible(op.op_type):
    return B

  // Step 5: Default to exclusive (safest, most expensive)
  return X
```

**Classification rules:**

1. All operation types begin as X-class unless pre-classified.
2. An operation type MAY be promoted to M-class when an I-confluence proof is certified.
3. An operation type MAY be promoted to B-class when CSO eligibility is demonstrated.
4. A provisional M-class operation is automatically demoted to B-class (if CSO-eligible) or X-class (otherwise) if monitoring detects a convergence violation.
5. V-class and G-class are determined by operation semantics, not by proofs.
6. Reclassification takes effect at the next epoch boundary.

The ordering in the decision procedure matters: governance and verification checks come first because they are determined by operation semantics regardless of proof status. M-class comes before B-class because it is strictly cheaper (zero coordination vs. epoch-boundary rebalancing). X-class is the fall-through default because it is always safe.

### 3.3 I-Confluence Foundation

**What I-confluence means.** An operation is I-confluent with respect to an invariant set I if, for all states s1 and s2 reachable from a common ancestor state s0 by applying sequences of operations (potentially including the operation in question), the merge of s1 and s2 satisfies I. Formally:

```
For all states s1, s2 reachable from a common ancestor s0
by applying sequences of operations including op:
  merge(s1, s2) satisfies I
```

where `merge` is the CRDT merge function for the state type.

**Why it matters.** I-confluence is the formal criterion that separates "safe to execute without coordination" from "requires coordination for correctness." It was introduced by Bailis et al. (VLDB 2015) and demonstrated a 25x throughput improvement over traditional serializable execution on TPC-C benchmarks by identifying which operations could safely execute concurrently. The Tidal Noosphere applies this criterion not to database transactions but to epistemic coordination operations — a significantly more complex domain where invariants involve claim consistency, contradiction detection, and knowledge graph integrity.

**The proof obligation.** For an operation to be classified M-class, the following MUST hold:

```
IConfluenceProof := {
  operation_type: OperationType
  invariant_set:  Set<Invariant>
  proof_system:   {TLA_PLUS, COQ, F_STAR, IVY}
  proof_artifact: ArtifactRef
  certified_epoch: uint64
  certifier:      AgentId
  verifiers:      Set<AgentId>     // minimum 3
  status:         {PROVISIONAL, CERTIFIED, REVOKED}
}
```

The proof must be machine-checked — not a human argument, not a simulation result, but a formal artifact verified by a proof assistant.

**Relationship to CAP and FLP.** The operation-class algebra is the Tidal Noosphere's answer to the CAP theorem and FLP impossibility:

- M-class: chooses availability (eventual consistency via CRDTs). Safe during partitions.
- B-class: chooses availability (local CSO spend, epoch-boundary rebalancing). Safe during partitions.
- X-class: chooses consistency (serial commit). Blocks during partitions.
- V-class: chooses consistency (verification committee must agree). Requires partial synchrony.
- G-class: chooses consistency (BFT consensus). Requires partial synchrony.

### 3.4 Bootstrap: From Cold Start to Full Coverage

**The problem.** At system genesis, no operations have I-confluence proofs. Without proofs, all operations default to X-class. The O(1) steady-state claim is the asymptotic case, not the launch case.

**The bootstrap set: 15 obviously-I-confluent operations.**

| # | Operation | Why Obviously I-Confluent | Effort |
|---|-----------|--------------------------|--------|
| 1 | G-Counter increment | Monotone increment per agent. Merge = component-wise max. | 4h |
| 2 | G-Set add | Grow-only set. Merge = union. | 4h |
| 3 | LWW-Register write | Last-writer-wins with timestamps. Merge = max timestamp. | 4h |
| 4 | OR-Set add/remove | Observed-remove with unique tags. | 16h |
| 5 | Signal emission (SIG) | Append-only per issuer, dedup by (type, scope, payload_hash). | 8h |
| 6 | Signal decay | Time-based removal. Monotone with respect to time. | 8h |
| 7 | Reputation accumulation | Multi-dimensional weighted running average. Commutative. | 16h |
| 8 | SLV computation | Recomputed from scratch each epoch. Idempotent. | 4h |
| 9 | Capacity snapshot propagation | Gossip with latest-epoch-wins merge. CRDT pattern. | 8h |
| 10 | Idempotent claim state transition | Monotone along state lattice. Merge = max. | 16h |
| 11 | Evidence reference accumulation | Append-only set. G-Set pattern. | 4h |
| 12 | Attestation accumulation | Append-only set with natural dedup. | 8h |
| 13 | Reinforcement count increment | Monotone counter. Merge = max. G-Counter. | 2h |
| 14 | Contradiction edge creation | Append-only edge set. G-Set pattern. | 8h |
| 15 | Bundle utility score update | Monotone (utility only increases). Merge = max. | 4h |

**Total bootstrap effort: 106 person-hours.** Achievable within Phase 1 (4 months).

**Provisional M-class (M-prov).** Operations with empirical convergence evidence but incomplete formal proofs may be classified as provisional M-class with monitoring:

```
function classify_provisional_m(op_type: OperationType) -> bool:
  evidence = get_convergence_evidence(op_type)
  if evidence.runs >= 1000 and evidence.violations == 0:
    register_classification(op_type, M, provisional=true,
      monitoring=MonitoringConfig{
        check_interval = 1,    // every TIDAL_EPOCH
        violation_action = DEMOTE_TO_X,
        alert_threshold = 1
      })
    return true
  return false
```

**Expected progression:**

| Time | M-class | B-class | X-class | M-class Traffic |
|------|---------|---------|---------|-----------------|
| Genesis | ~10 | ~5 | Remainder | ~30% |
| Phase 1 end (4 months) | ~20 | ~10 | Remainder | ~50% |
| Phase 2 end (10 months) | ~40 | ~15 | Remainder | ~70% |
| Steady state | 60+ | ~20 | Remainder | >80% |

**Kill criterion:** If average certification effort exceeds 60 person-hours per operation by the end of Phase 1, the mandatory formal proof requirement must be reassessed.

---

## 4. Tidal Scheduling

### 4.1 Consistent Hash Rings Within Parcels

Within each parcel, for each active task type, the Tidal Scheduler maintains a consistent hash ring (Karger et al., 1997). Each task is assigned to the nearest agent clockwise on the ring. When an agent joins or leaves, only O(K/N) tasks remap.

**Ring construction:**

```
function build_ring(parcel: Parcel, task_type: TaskType) -> HashRing:
  N = |parcel.agents|
  V = adaptive_vnode_count(N)    // Section 4.6
  epsilon = BOUNDED_LOADS_EPSILON

  entries = empty sorted array
  for agent in parcel.agents:
    for v in 0..V-1:
      pos = SHA256(agent.id || task_type || uint32_be(v)) mod 2^256
      entries.insert_sorted((pos, agent.id))

  return HashRing{
    task_type = task_type,
    parcel = parcel.id,
    entries = entries,
    virtual_nodes = V,
    epsilon = epsilon,
    agent_count = N
  }
```

### 4.2 Bounded-Loads Variant (Hardened)

The bounded-loads algorithm (Mirrokni, Thorup, Wieder, SODA 2018) guarantees no agent receives more than (1 + epsilon) times the average load. The hardened implementation includes dynamic cap recomputation and per-agent load tracking:

```
BOUNDED_LOADS_EPSILON = 0.15
BOUNDED_LOADS_MIN_TASKS_FOR_BALANCE = 3

struct BoundedLoadsRing:
    entries: SortedArray<(uint256, AgentId)>
    agent_count: uint32
    virtual_nodes_per_agent: uint32
    epsilon: float
    task_type: TaskType
    parcel_id: ParcelId
    agent_loads: Map<AgentId, uint32>
    total_assigned: uint32
    capacity_cap: uint32

function build_bounded_ring(
    parcel: Parcel, task_type: TaskType, expected_tasks: uint32
) -> BoundedLoadsRing:
    N = len(parcel.agents)
    V = adaptive_vnode_count(N)
    epsilon = BOUNDED_LOADS_EPSILON

    entries = empty sorted array
    for agent in parcel.agents:
        for v in 0..V-1:
            pos = SHA256(agent.id || task_type || uint32_be(v)) mod 2^256
            entries.insert_sorted((pos, agent.id))

    avg_load = max(1, ceil(expected_tasks / N))
    cap = ceil((1 + epsilon) * avg_load)

    return BoundedLoadsRing{
        entries = entries, agent_count = N,
        virtual_nodes_per_agent = V, epsilon = epsilon,
        task_type = task_type, parcel_id = parcel.id,
        agent_loads = {agent.id: 0 for agent in parcel.agents},
        total_assigned = 0, capacity_cap = cap
    }

function lookup_bounded(ring: BoundedLoadsRing, key: bytes) -> AgentId:
    target_pos = SHA256(key) mod 2^256
    ring.total_assigned += 1
    current_avg = ring.total_assigned / ring.agent_count
    dynamic_cap = max(ring.capacity_cap, ceil((1 + ring.epsilon) * current_avg))

    idx = ring.entries.lower_bound(target_pos)
    if idx >= len(ring.entries): idx = 0

    visited = 0
    while visited < len(ring.entries):
        (pos, agent_id) = ring.entries[idx]
        if ring.agent_loads[agent_id] < dynamic_cap:
            ring.agent_loads[agent_id] += 1
            return agent_id
        idx = (idx + 1) % len(ring.entries)
        visited += 1

    // Fallback: least-loaded agent
    least_loaded = min(ring.agent_loads, key=lambda aid: ring.agent_loads[aid])
    ring.agent_loads[least_loaded] += 1
    return least_loaded
```

**Validation requirement (GATE-2).** Sweep N=3..50 agents, V=50..500 virtual nodes. Kill criterion: max/avg load > 1.3 for any N >= 5 after optimization.

### 4.3 Three-Tier Temporal Hierarchy

All operations are defined relative to the canonical three-tier temporal hierarchy (per C9 cross-layer reconciliation):

| Tier | Name | Duration | Ticks | Purpose |
|------|------|----------|-------|---------|
| 1 | SETTLEMENT_TICK | 60s | 1 | Atomic temporal unit; settlement, signal decay |
| 2 | TIDAL_EPOCH | 3,600s | 60 | Primary coordination cycle; scheduling, VRF, parcels |
| 3 | CONSOLIDATION_CYCLE | 36,000s | 600 | Long-horizon; K-class claims, cross-locus reconciliation |

**Epoch clock:**
```
current_tick = floor((ntp_time() - GENESIS_TIME) / SETTLEMENT_TICK_DURATION)
current_epoch = floor(current_tick / TICKS_PER_TIDAL_EPOCH)
current_cycle = floor(current_epoch / EPOCHS_PER_CONSOLIDATION_CYCLE)
```

**Clock synchronization.** Agents synchronize via NTP. Tolerance: 500ms. An agent whose local clock diverges by more than CLOCK_TOLERANCE from NTP is treated as timing-faulty. Persistent drift (3+ consecutive epochs) triggers substitution — the next agent on the hash ring's clockwise chain absorbs the faulty agent's tasks.

**Why NTP-grade, not consensus-grade.** PTA uses NTP synchronization (approximately 10ms accuracy in well-configured networks, degrading to approximately 100ms in adverse conditions) rather than consensus-synchronized clocks. With a 1-hour epoch, 100ms boundary uncertainty is 0.003% — negligible.

**Epoch boundary detection:**
```
function is_epoch_boundary() -> bool:
  t = ntp_time()
  return (t - GENESIS_TIME) mod (SETTLEMENT_TICK_DURATION * TICKS_PER_TIDAL_EPOCH) < BOUNDARY_WINDOW
```

Default: BOUNDARY_WINDOW = 5 seconds.

**Epoch lifecycle walkthrough.** To make the abstract machinery concrete, the following traces one complete epoch from the perspective of a single agent:

```
EPOCH LIFECYCLE (Agent A, Parcel P, Locus L, Epoch E -> E+1)

Phase 1: Steady-State Execution (Epoch E, ~3595 seconds)
---------------------------------------------------------
  1. Agent A holds its task assignment list computed at the start of E.
  2. For each assigned M-class task: execute locally, emit CRDT state to
     anti-entropy channel. No coordination, no messages.
  3. For each assigned B-class task: decrement local CSO. If CSO exhausted,
     shed task to next agent on substitution list.
  4. For each assigned X-class task: enter quorum protocol with replica
     group within parcel P. Serial commit for single-parcel ops, Fusion
     Capsule for cross-parcel ops.
  5. Predictive delta channel: for each neighbor, compare observed behavior
     to prediction. If |observed - predicted| > threshold: emit surprise
     message (delta). Otherwise: silence. Zero messages when predictions hold.
  6. Stigmergic channel: emit/reinforce signals as needed (need, offer,
     risk, anomaly, attention_request, reservation, trend). Signals
     propagate at locus scope and decay unless reinforced.

Phase 2: Boundary Detection (t = epoch boundary)
-------------------------------------------------
  7. Agent A detects boundary: is_epoch_boundary() returns true.
     The 5-second window begins.
  8. Agent A freezes task execution for the current epoch. In-flight X-class
     commits are allowed to complete (up to BOUNDARY_WINDOW timeout);
     incomplete commits are rolled back.

Phase 3: Capacity Snapshot Gossip (~1s of boundary window)
----------------------------------------------------------
  9. Agent A broadcasts its capacity snapshot: (agent_id, available_compute,
     available_bandwidth, task_type_capabilities, current_SLV_contribution).
 10. Agent A receives snapshots from peers via gossip protocol
     (fanout=log(N), TTL=3 hops). At N=50, convergence in ~3 gossip rounds.
 11. Agent A merges received snapshots into its local roster view.

Phase 4: Roster Reconciliation and Ring Reconstruction (~1s)
------------------------------------------------------------
 12. Agent A compares epoch E roster to epoch E+1 roster (derived from
     received capacity snapshots). New agents: add to ring. Departed agents:
     remove from ring. Unchanged: no ring modification needed.
 13. If roster changed: for each (parcel, task_type) pair, Agent A
     recomputes the hash ring via build_ring(). All agents perform this
     independently with identical inputs, producing identical rings.
 14. If roster unchanged: rings carry forward. No computation needed.

Phase 5: VRF Seed Rotation (~0.5s)
-----------------------------------
 15. Agent A computes the new VRF seed for epoch E+1:
     vrf_seed(E+1) = ECVRF_prove(sk_A, epoch_E+1 || parcel_id)
 16. Pre-stratified diversity pools are refreshed using the new seed.
     Commit phase of the commit-reveal protocol begins for the next
     verification cycle. VRF cache is invalidated per Section 5.8.

Phase 6: Predictive Model Recalibration (~0.5s)
------------------------------------------------
 17. Agent A updates its linear prediction models for each neighbor based
     on epoch E observations. Learning rate: LEARNING_RATE (default 0.01).
 18. Surprise threshold adapts per the adaptive threshold formula.
 19. Agents transitioning from TRANSITIONING to PREDICTIVE mode: check if
     model accuracy exceeds ACTIVATION_THRESHOLD (0.7) for 3 consecutive
     observation windows.

Phase 7: Settlement Computation (~0.5s)
---------------------------------------
 20. Agent A computes its own settlement for epoch E using the four-stream
     model (scheduling compliance, verification duty, communication
     efficiency, governance participation).
 21. Settlement is deterministic: all agents compute identical settlement
     for all agents from shared inputs.

Phase 8: Parcel Health and Storm Check (~0.5s)
----------------------------------------------
 22. Storm check runs FIRST: evaluate_storm_condition() before any
     reconfiguration decisions.
 23. Parcel Manager evaluates load balance, agent health, diversity metrics.
 24. If reconfiguration needed and storm check allows: initiate PTP via
     staggered 4-phase protocol.

Phase 9: New Epoch Begins
-------------------------
 25. Agent A computes its epoch E+1 task assignment list via
     compute_assignment() using the updated roster and rings.
 26. Execution resumes. The cycle repeats.
```

**Timing budget.** The 5-second boundary window is tight at large parcel sizes. At N=50 agents with gossip fanout=6 and 3 rounds, capacity snapshot gossip requires approximately 1 second. Ring reconstruction for T=20 task types with adaptive vnodes requires computing ~40,000 hash entries — approximately 0.5 seconds on modern hardware. The remaining 3.5 seconds accommodate VRF seed rotation, model recalibration, settlement, and parcel health evaluation. At N=500 (Phase 3 parcel sizes), the boundary window may need to extend to 10-15 seconds, reducing useful epoch time by 0.1-0.4%. This is configurable via BOUNDARY_WINDOW.

**Fault behavior during epoch transitions.** If an agent misses the boundary window (clock skew, compute delay, network partition), it continues executing with the stale epoch E schedule. Peers detect this as a timing surprise in the next epoch. If the agent catches up within CLOCK_TOLERANCE (500ms), no action is taken. If it persists for 3+ epochs, it is treated as timing-faulty and its tasks are redistributed via the substitution list. The system never halts waiting for a slow agent — deterministic scheduling means every agent can independently compute the correct schedule even if some peers are temporarily absent.

### 4.4 Task Assignment Algorithm

```
function compute_assignment(
  agent: Agent, parcel: Parcel, epoch: uint64, tidal_version: TidalFunction
) -> List<TaskAssignment>:

  assignments = []
  for task_type in agent.capabilities intersect tidal_version.task_types:
    ring = parcel.hash_rings[task_type]
    for task_idx in 0..task_count(task_type, epoch)-1:
      task_key = SHA256(task_type || uint64_be(epoch) || uint32_be(task_idx))
      assigned_agent = lookup_bounded(ring, task_key)
      if assigned_agent == agent.id:
        assignments.append(TaskAssignment{
          task_type = task_type, task_key = task_key,
          epoch = epoch, priority = task_priority(task_type, tidal_version)
        })

  assignments.sort_by(a => a.priority, descending)
  if total_load(assignments) > agent.capacity:
    assignments = assignments[:capacity_limit(agent)]
  return assignments
```

**The determinism invariant (INV-2).** Every agent independently computes identical assignments from the same inputs. Two agents with the same inputs MUST produce identical outputs.

### 4.5 Agent Churn Handling

**Join (graceful):** Register at epoch boundary -> ring reconstruction -> enter STANDARD communication mode.

**Leave (graceful):** Announce departure -> substitution list activates -> ring reconstructed at next boundary.

**Leave (failure):** Peer detection -> immediate substitution -> ring reconstruction at boundary.

**Churn budget:** At most CHURN_BUDGET_FRACTION (default 0.20) of agents may change per epoch. Excess queued. Storm detection (Section 4.9) provides additional protection.

### 4.6 Adaptive Virtual Nodes

The hardened virtual node formula targets ~2,000 ring entries regardless of parcel size:

```
VNODE_MIN = 50
VNODE_MAX = 500
VNODE_TARGET_VARIANCE = 0.05

function adaptive_vnode_count(N: uint32) -> uint32:
    variance_based = ceil(1.0 / (VNODE_TARGET_VARIANCE ** 2 * N))
    V = clamp(variance_based, VNODE_MIN, VNODE_MAX)

    SMALL_PARCEL_OVERRIDES = {
        5: 400, 6: 350, 7: 300, 8: 250, 9: 225, 10: 200
    }
    if N in SMALL_PARCEL_OVERRIDES:
        V = max(V, SMALL_PARCEL_OVERRIDES[N])
    return V
```

| Agents (N) | V | Ring Entries | Expected max/avg |
|------------|---|-------------|-----------------|
| 5 | 400 | 2,000 | 1.10 |
| 10 | 200 | 2,000 | 1.07 |
| 20 | 100 | 2,000 | 1.05 |
| 50 | 50 | 2,500 | 1.03 |

### 4.7 Epoch-Boundary Load Rebalancing

```
REBALANCE_TRIGGER_RATIO = 1.5
REBALANCE_VNODE_ADJUSTMENT = 0.10
REBALANCE_MAX_CONSECUTIVE = 3
REBALANCE_COOLDOWN_EPOCHS = 5

function epoch_boundary_rebalance(parcel: Parcel, epoch: uint64):
    for task_type in parcel.active_task_types:
        ring = parcel.hash_rings[task_type]
        state = measure_load_imbalance(ring, epoch)
        if state.imbalance_ratio > REBALANCE_TRIGGER_RATIO:
            parcel.hash_rings[task_type] = rebalance_vnodes(ring, state, parcel)
        else:
            state.consecutive_rebalances = 0
            store_balance_state(state)
```

All rebalancing is deterministic from shared state — preserving INV-2. Rebalancing adjusts per-agent vnode counts by up to REBALANCE_VNODE_ADJUSTMENT (10%) per epoch, with a consecutive rebalance limit of REBALANCE_MAX_CONSECUTIVE (3) followed by REBALANCE_COOLDOWN_EPOCHS (5) epochs of cooldown.

### 4.8 Minimum Parcel Size and Merge Protocol

```
PARCEL_MIN_AGENTS = 5
PARCEL_MERGE_THRESHOLD = 6
PARCEL_MERGE_COOLDOWN_EPOCHS = 10
```

When a parcel drops below PARCEL_MIN_AGENTS, a FORCE_MERGE is triggered. The merge protocol moves all agents from the source parcel to the best-compatible target parcel (scored by task type overlap, combined size, and load profile similarity). Hash rings are rebuilt, CompressedModelSummary (Section 6.6) transfers predictive context, and the source parcel is dissolved. Diversity pools are per-locus, so no pool action is needed beyond ensuring merged agents are in the eligibility set.

### 4.9 Storm Detection and Throttled Reconfiguration

A graduated circuit breaker prevents reconfiguration storms:

```
STORM_PARCEL_THRESHOLD = 0.15     // 15% of parcels reconfiguring
STORM_AGENT_THRESHOLD = 0.25      // 25% of agents in transitioning parcels

enum CircuitBreakerState:
    NORMAL       // all reconfigurations permitted
    THROTTLED    // only FORCE_MERGE permitted
    DRAIN_ONLY   // complete in-progress, start none
    HALT_ALL     // freeze all topology changes

function evaluate_storm_condition(locus: Locus, epoch: uint64) -> StormState:
    parcel_ratio = transitioning_parcels / total_parcels
    agent_ratio = agents_in_transition / total_agents

    if agent_ratio > 0.50:        return HALT_ALL
    elif agent_ratio > 0.25:      return DRAIN_ONLY
    elif parcel_ratio > 0.15:     return THROTTLED
    else:                         return NORMAL
```

Storm check runs FIRST at each epoch boundary, before any reconfiguration decisions.

### 4.10 Staggered Reconfiguration Protocol

Approved reconfigurations execute through a 4-phase protocol sequenced within ticks of a TIDAL_EPOCH:

| Phase | Ticks | Action |
|-------|-------|--------|
| A: RINGS | 0-14 | Rebuild hash rings with new roster |
| B: VRF | 15-29 | Restratify diversity pools, invalidate VRF cache |
| C: PREDICTIVE | 30-44 | Transfer CompressedModelSummary, warm-start models |
| D: NORMAL | 45-59 | Full normal operation |

During Phases A-C, governance quorum is frozen (Section 7.8) and degradation follows the priority ordering in Section 7.9.

---

## 5. Verification Architecture

### 5.1 The Verification Membrane

The Verification Membrane is the most heavily defended subsystem. It gates all knowledge admission — no claim enters the canonical knowledge graph without passing through the membrane. The Noosphere's Architectural Commandment applies with full force: the membrane is constitutionally protected and cannot be weakened by any mechanism short of G-class constitutional consensus with 75% supermajority and 72-hour discussion.

**Why the membrane is sovereign.** A bad scheduling algorithm wastes compute. A bad communication protocol wastes bandwidth. But a bad verification membrane poisons cognition. Epistemic corruption compounds through the knowledge graph — verified claims that cite other claims inherit the trust of their citations. Unlike performance degradation, which is immediately observable, epistemic corruption can persist undetected.

**Nine claim classes.** The membrane classifies claims into nine canonical classes organized in three tiers (see Section 5.10 for full taxonomy). The classification gate (4-step protocol) applies to all nine classes with class-specific verification pathways.

**Constitutional protection law.** No system parameter may reduce membrane verification depth, widen admission thresholds, or relax class-specific rules. Only G-class constitutional consensus can modify membrane parameters. The Feedback Controller and economic system are explicitly prohibited from adjusting membrane parameters.

### 5.2 VRF Dual Defense (Hardened)

Verifier committees are selected using a hardened dual-defense protocol combining VRF-based pseudorandom selection with multiple layered protections against committee manipulation.

#### 5.2.1 Base VRF Selection (ECVRF RFC 9381)

Verifier sets are computed using the Elliptic Curve VRF on curve P-256:

```
function compute_verifier_set(
  claim: Claim, epoch: uint64, vrf_seed: bytes[32],
  eligible: Set<Agent>, committee_size: uint8
) -> (Set<AgentId>, List<VRFProof>):

  alpha = SHA256(claim.hash || uint64_be(epoch) || vrf_seed)
  candidates = []

  for agent in eligible:
    (beta, pi) = ECVRF_prove(agent.privkey, alpha)
    threshold = committee_size / |eligible|
    if uint256_from_bytes(beta) < threshold * 2^256:
      candidates.append((agent.id, beta, pi))

  candidates.sort_by(c => c.beta)
  selected = candidates[:committee_size]
  return ({c.agent_id for c in selected}, {c.pi for c in selected})
```

#### 5.2.2 Commit-Reveal Protocol

**Phase 1 — COMMIT:** Agent commits diversity attributes with SHA256(salt || attrs) before knowing future VRF seeds.

**Phase 2 — REVEAL:** After REVEAL_DELAY epochs (default 1), agent reveals attributes. Verification confirms commitment hash matches.

**Attribute change:** New commitment -> escalating cooling period (Section 5.5) -> reveal -> old attributes permanently logged.

**Claim commitment:** Claims must be committed (hash published) at least 1 epoch before verification scheduling, preventing committee shopping.

#### 5.2.3 Pre-Stratified Diversity Pools

Pools are pre-constructed from committed attributes at each epoch boundary. Drawing from pools is VRF-randomized within each pool. An adversary with "perfectly diverse" Sybils gains no advantage because per-pool representation is proportional to total pool fraction.

### 5.3 Hidden Diversity Attributes

**Problem.** All four diversity dimensions were originally public after reveal. An adversary can observe all attributes and compute optimal Sybil placement to maximize diversity slot capture.

**Defense.** Split diversity dimensions into public and hidden. Public dimensions (training_lineage, region) are revealed normally. Hidden dimensions (methodology, temporal_bucket) are hashed with a per-epoch salt derived from the VRF seed, unknown until the epoch begins.

```
HIDDEN_DIMENSION_COUNT = 2   // governance-configurable, range [1, 4]

struct DiversityAttributes:
    // Public dimensions (revealed after REVEAL_DELAY)
    training_lineage: string
    region: string
    // Hidden dimensions (never revealed in plaintext)
    methodology_hash: bytes[32]
    temporal_bucket_hash: bytes[32]

function evaluate_hidden_diversity(
    agent: Agent, epoch: uint64, epoch_salt: bytes[32]
) -> bytes[32]:
    return SHA256(
        epoch_salt
        || agent.diversity_commitment.hidden_commitment
        || agent.diversity_commitment.agent_salt
    )

function build_diversity_pools_v2(
    eligible: Set<Agent>, locus: Locus, epoch: uint64, vrf_seed: bytes[32]
) -> (Map<(DiversityDimension, DiversityValue), DiversityPool>,
      Map<AgentId, bytes[32]>):
    // Phase 1: Build public pools (training_lineage, region)
    public_pools = {}
    for agent in eligible:
        if agent.diversity_commitment.cooling_until > current_epoch(): continue
        attrs = agent.diversity_commitment.public_attrs
        for (dim, val) in [(TRAINING_LINEAGE, attrs.training_lineage),
                           (REGION, attrs.region)]:
            key = (dim, val)
            if key not in public_pools:
                public_pools[key] = DiversityPool{dimension=dim, value=val, members={}}
            public_pools[key].members.add(agent.id)

    // Phase 2: Compute hidden diversity scores
    epoch_salt = SHA256(vrf_seed || uint64_be(epoch) || b"hidden_diversity")
    hidden_scores = {}
    for agent in eligible:
        hidden_scores[agent.id] = evaluate_hidden_diversity(agent, epoch, epoch_salt)

    return (public_pools, hidden_scores)
```

**Security property.** The adversary's optimizable surface is reduced from 4 dimensions to 2. Hidden dimension scores change every epoch (epoch_salt changes), preventing pre-computation.

### 5.4 Randomized Filter Thresholds

**Problem.** Fixed diversity requirements allow the adversary to compute exactly which attribute combinations maximize selection.

**Defense.** Randomize diversity requirements per committee within governance-approved ranges:

```
DEFAULT_DIVERSITY_RANGES = [
    DiversityRequirementRange{
        dimension = TRAINING_LINEAGE,
        min_mandatory_slots = 1, max_mandatory_slots = 3,
        weight_range = (0.15, 0.35)
    },
    DiversityRequirementRange{
        dimension = REGION,
        min_mandatory_slots = 1, max_mandatory_slots = 2,
        weight_range = (0.10, 0.25)
    },
    DiversityRequirementRange{
        dimension = METHODOLOGY,   // hidden
        min_mandatory_slots = 0, max_mandatory_slots = 2,
        weight_range = (0.10, 0.20)
    },
    DiversityRequirementRange{
        dimension = TEMPORAL_BUCKET,  // hidden
        min_mandatory_slots = 0, max_mandatory_slots = 2,
        weight_range = (0.10, 0.20)
    }
]

function randomize_diversity_requirements(
    claim: Claim, epoch: uint64, vrf_seed: bytes[32],
    ranges: List<DiversityRequirementRange>
) -> List<DiversityRequirement>:
    committee_entropy = SHA256(
        claim.hash || uint64_be(epoch) || vrf_seed || b"diversity_threshold"
    )
    // Map entropy bytes to slot counts and weights within governance ranges
    // Deterministic but unpredictable until claim hash + VRF seed both known
    ...
    return requirements
```

### 5.5 Diversity Attribute Commitment with Cooling Period

Escalating costs for repeated attribute changes:

```
DIVERSITY_COOLING_BASE = 50          // epochs
DIVERSITY_COOLING_ESCALATION = 2.0   // multiplier per change
DIVERSITY_MAX_CHANGES_PER_YEAR = 4   // hard cap
DIVERSITY_CHANGE_STAKE_LOCK = 0.10   // 10% of stake locked during cooling
```

| Change # | Cooling Period | Stake Lock |
|----------|---------------|------------|
| 1st | 50 epochs | 50 epochs x 10% stake |
| 2nd | 100 epochs | 100 epochs x 10% stake |
| 3rd | 200 epochs | 200 epochs x 10% stake |
| 4th | 400 epochs | 400 epochs x 10% stake |
| 5th+ | Blocked until next year | N/A |

Agent is INELIGIBLE for verification committees during cooling. Permanent audit trail of all changes.

### 5.6 Hardened End-to-End VRF Committee Selection

The complete hardened protocol integrating all defense mechanisms:

```
function select_diverse_verifiers_v2(
    claim: Claim, epoch: uint64, vrf_seed: bytes[32],
    eligible: Set<Agent>, locus: Locus,
    committee_size: uint8, diversity_ranges: List<DiversityRequirementRange>
) -> Set<AgentId>:

    // Step 1: Build public pools + compute hidden scores
    (public_pools, hidden_scores) = build_diversity_pools_v2(
        eligible, locus, epoch, vrf_seed)

    // Step 2: Randomize diversity requirements
    requirements = randomize_diversity_requirements(
        claim, epoch, vrf_seed, diversity_ranges)

    alpha = SHA256(claim.hash || uint64_be(epoch) || vrf_seed)
    committee = {}

    // Step 3: Fill public diversity slots
    for req in requirements:
        if req.dimension in [TRAINING_LINEAGE, REGION]:
            // VRF-randomized selection within each pool
            for (dim_key, pool) in public_pools:
                if dim_key[0] != req.dimension: continue
                if req.mandatory_slots <= 0: break
                pool_candidates = [(aid, ECVRF_prove(get_agent(aid).privkey,
                    alpha || encode(req.dimension) || encode(dim_key[1])).beta)
                    for aid in pool.members if aid not in committee
                    and is_eligible_for_verification(get_agent(aid))]
                pool_candidates.sort_by(c => c[1])
                if len(pool_candidates) > 0:
                    committee.add(pool_candidates[0][0])
                    req.mandatory_slots -= 1

    // Step 4: Fill hidden diversity slots
    epoch_hidden_salt = SHA256(vrf_seed || uint64_be(epoch) || b"hidden_select")
    for req in requirements:
        if req.dimension in [METHODOLOGY, TEMPORAL_BUCKET]:
            hidden_candidates = []
            for agent_id in union(p.members for p in public_pools.values()):
                if agent_id in committee: continue
                hidden_score = SHA256(epoch_hidden_salt || hidden_scores[agent_id]
                    || encode(req.dimension))
                hidden_candidates.append((agent_id, hidden_score))
            hidden_candidates.sort_by(c => c[1])
            slots = min(req.mandatory_slots, len(hidden_candidates))
            for i in 0..slots-1:
                committee.add(hidden_candidates[i][0])

    // Step 5: Fill remaining slots via standard VRF
    all_eligible = union(p.members for p in public_pools.values())
    remaining = [(aid, ECVRF_prove(get_agent(aid).privkey, alpha).beta)
        for aid in all_eligible if aid not in committee
        and is_eligible_for_verification(get_agent(aid))]
    remaining.sort_by(c => c[1])
    for (agent_id, beta) in remaining:
        if len(committee) >= committee_size: break
        if would_exceed_weight_cap(agent_id, committee): continue   // 15% cap
        committee.add(agent_id)

    return committee
```

### 5.7 VRF Phased Deployment

VRF defense complexity is deployed in three phases matching system maturity:

```
enum VRFPhase:
    SIMPLE            // Phase 1: standard VRF, no diversity
    COMMITTED         // Phase 2: commit-reveal + public diversity pools
    FULL_DUAL_DEFENSE // Phase 3: hidden dimensions + randomized thresholds

function determine_vrf_phase(locus: Locus) -> VRFPhase:
    N = count_eligible_verifiers(locus)
    if N < 50:   return SIMPLE
    if N < 200:  return COMMITTED
    return FULL_DUAL_DEFENSE

function select_verifiers_simple(claim, epoch, vrf_seed, eligible, size) -> Set<AgentId>:
    // Standard VRF selection without diversity filtering
    alpha = SHA256(claim.hash || uint64_be(epoch) || vrf_seed)
    candidates = [(a.id, ECVRF_prove(a.privkey, alpha).beta) for a in eligible]
    candidates.sort_by(c => c[1])
    return {c[0] for c in candidates[:size]}

function select_verifiers_committed(claim, epoch, vrf_seed, eligible, size) -> Set<AgentId>:
    // Commit-reveal + public diversity pools (no hidden dimensions)
    pools = build_diversity_pools(eligible, locus)
    return select_diverse_verifiers(claim, epoch, vrf_seed, pools, locus, size)
```

### 5.8 VRF Cache Invalidation on Reconfiguration

During parcel reconfiguration, VRF committee selections cached from the previous configuration must be invalidated:

```
struct VRFCacheEntry:
    claim_hash: bytes[32]
    epoch: uint64
    committee: Set<AgentId>
    parcel_config_hash: bytes[32]   // hash of the parcel roster at selection time

function invalidate_vrf_cache(parcel: Parcel):
    new_config_hash = SHA256(canonical_serialize(sorted(parcel.agents)))
    for entry in vrf_cache:
        if entry.parcel_config_hash != new_config_hash:
            vrf_cache.remove(entry)

function resolve_committee_for_new_verification(
    claim: Claim, epoch: uint64, parcel: Parcel
) -> Set<AgentId>:
    // Always recompute after reconfiguration — never use stale cache
    config_hash = SHA256(canonical_serialize(sorted(parcel.agents)))
    cached = vrf_cache.get(claim.hash, epoch, config_hash)
    if cached: return cached.committee

    committee = select_diverse_verifiers_v2(claim, epoch, ...)
    vrf_cache.put(VRFCacheEntry{
        claim_hash = claim.hash, epoch = epoch,
        committee = committee, parcel_config_hash = config_hash
    })
    return committee
```

### 5.9 Continuous Re-Verification

The verification membrane does not verify claims once and trust them forever. Continuous re-verification with citation-weighted sampling ensures heavily-cited claims are re-verified more frequently. Claims whose supporting evidence is superseded or challenged are automatically queued for re-verification.

The Membrane Quality Index (MQI) tracks six metrics across all verification activity and detects drift toward degradation. Three response tiers — conservative mode, enhanced scrutiny, and lockdown — provide progressively stronger defenses as quality metrics deteriorate.

### 5.10 Nine-Class Claim Taxonomy

Per C9 cross-layer reconciliation, the claim taxonomy is expanded from the original five classes to nine canonical classes organized in three tiers:

**Tier 1 — FORMAL_PROOF (highest confidence):**

| Class | Name | Verification Pathway | Conservatism |
|-------|------|---------------------|-------------|
| D | Deterministic | Recomputation; mathematical proofs, algorithmic outputs | Lowest (most confident) |
| C | Causal | Intervention analysis + mechanism verification; causal models | Low |

**Tier 2 — STRUCTURED_EVIDENCE:**

| Class | Name | Verification Pathway | Conservatism |
|-------|------|---------------------|-------------|
| P | Predictive | Forecast tracking with horizon-weighted scoring; model predictions | Medium-low |
| R | Replicative | Independent replication protocol; reproducible experiments | Medium-low |
| E | Empirical | Replication + cross-reference; experimental results, observational data | Medium |
| S | Statistical | Distribution analysis + methodology audit; statistical inferences | Medium |
| K | Knowledge-consolidation | Consolidation review at CONSOLIDATION_CYCLE boundary; meta-analyses | Medium-high |

**Tier 3 — STRUCTURED_ATTESTATION (highest uncertainty):**

| Class | Name | Verification Pathway | Conservatism |
|-------|------|---------------------|-------------|
| H | Heuristic | Contestable Reliance Membrane (time-bounded permits) | High |
| N | Novel | Novel assessment protocol; unprecedented claims | Highest (most conservative) |

**Conservatism ordering:** H > N > K > E > S > R > P > C > D (H is most conservative, D is least).

**K-class specific requirements:**
- K-class claims are processed at CONSOLIDATION_CYCLE boundaries (every 10 TIDAL_EPOCHs).
- VTD requirements include evidence from minimum 5 sources from 5+ agents across 3+ parcels, no single agent contributing >30%. *Canonical requirement per C5 PCVM and C9 Cross-Layer Reconciliation.*
- Aging uncertainty: K-class VTDs increase uncertainty by KNOWLEDGE_AGING_RATE per CONSOLIDATION_CYCLE if not refreshed.
- KNOWLEDGE_AGING_RATE = 0.005 per TIDAL_EPOCH (governance-configurable, range [0.001, 0.02]). *Canonical value per C6 EMA and C9 Cross-Layer Reconciliation.*

**Verification pathways for P, R, C, K classes:**

```
function verify_p_class(claim: Claim, committee: Committee) -> VerificationResult:
    // Predictive: track forecast accuracy over time
    forecast = extract_forecast(claim)
    horizon = forecast.horizon  // epochs until testable
    if horizon <= current_epoch() - claim.submitted_epoch:
        actual = get_actual_outcome(forecast.target)
        accuracy = compute_forecast_accuracy(forecast.prediction, actual)
        return assess_with_horizon_weighting(accuracy, horizon)
    else:
        return VerificationResult{status=PENDING, recheck_epoch=claim.submitted_epoch + horizon}

function verify_r_class(claim: Claim, committee: Committee) -> VerificationResult:
    // Replicative: attempt independent replication
    protocol = extract_replication_protocol(claim)
    replications = [member.attempt_replication(protocol) for member in committee]
    success_rate = count(r.success for r in replications) / len(replications)
    return assess_replication(success_rate, replications)

function verify_c_class(claim: Claim, committee: Committee) -> VerificationResult:
    // Causal: validate intervention logic and mechanism
    causal_model = extract_causal_model(claim)
    interventions = extract_interventions(claim)
    mechanism_valid = validate_mechanism(causal_model, committee)
    confounds_checked = check_confounds(interventions, committee)
    return assess_causal(mechanism_valid, confounds_checked)

function verify_k_class(claim: Claim, committee: Committee) -> VerificationResult:
    // Knowledge-consolidation: meta-review at CONSOLIDATION_CYCLE boundary
    sources = extract_sources(claim)
    assert len(sources) >= 5, "K-class requires >= 5 sources from 5+ agents across 3+ parcels, no single agent >30%"
    source_validity = [verify_source_current(s) for s in sources]
    consolidation_quality = assess_consolidation(claim, sources, source_validity)
    return consolidation_quality
```

### 5.11 AVAP Integration Points

The C12 AVAP (Anonymous Verification with Adaptive Probing) anti-collusion architecture integrates with the C3 VRF engine at the following points. *The committee formation logic below — including the self-selection threshold, encrypted assignment tokens, and cover traffic protocol — originates from the C12 Collusion Defense / AVAP Architecture Master Tech Spec. C3 reproduces the integration surface; C12 is the authoritative source for AVAP internals.*

**Anonymous committee selection.** When AVAP is enabled (conformance level permitting), committee assignment uses encrypted VRF assignment tokens (per C12 AVAP Architecture):

```
STRUCTURE AssignmentToken:
    agent_id:         bytes32
    claim_hash:       bytes32
    epoch:            uint64
    vrf_output:       bytes32         // ECVRF output (beta)
    vrf_proof:        bytes80         // ECVRF proof (pi)
    encrypted_payload: bytes          // X25519-XSalsa20-Poly1305 encrypted
    assignment_nonce: bytes16         // CSPRNG, >= 128 bits entropy

function avap_committee_select(
    agent: Agent, claim: Claim, epoch: uint64,
    vrf_seed: bytes[32], eligible: Set<Agent>, committee_size: uint8
) -> (bool, AssignmentToken):
    // Domain separation: b"AVAP_M1_v1" tag
    alpha = SHA256(b"AVAP_M1_v1" || claim.hash || uint64_be(epoch) || vrf_seed)
    (beta, pi) = ECVRF_prove(agent.privkey, alpha)

    // Self-selection threshold
    threshold = committee_size / len(eligible)
    selected = uint256_from_bytes(beta) < threshold * 2^256

    // Encrypt assignment for coordinator
    nonce = csprng_bytes(16)
    payload = agent.id || claim.hash || uint64_be(epoch)
    encrypted = crypto_box(coordinator_pubkey, payload, nonce)

    token = AssignmentToken{
        agent_id = agent.id, claim_hash = claim.hash, epoch = epoch,
        vrf_output = beta, vrf_proof = pi,
        encrypted_payload = encrypted, assignment_nonce = nonce
    }
    return (selected, token)
```

**Diversity pool inheritance.** AVAP enforces C3 diversity pool constraints (Section 5.3-5.4). The anonymity layer operates on top of the diversity-filtered pool.

**Sentinel Graph exclusion.** Sentinel cluster co-occurrence limits (MAX_CLUSTER_CO_OCCURRENCE, default 1) are enforced during AVAP committee formation.

**VRF seed schedule.** AVAP uses the same epoch VRF seed rotation as the base C3 system. No separate seed schedule.

**Cover traffic.** When AVAP is active, all eligible agents MUST perform cover traffic (verification-like activity) to prevent committee membership inference from activity patterns. Cover traffic depth: COVER_TRAFFIC_DEPTH (default 3 per claim per epoch).

**AVAP committee parameters:**

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| MIN_COMMITTEE_SIZE | 7 | [5, 20] | BFT tolerance floor |
| DEFAULT_COMMITTEE_SIZE | 10 | [7, 15] | Balance security/cost |
| MAX_COMMITTEE_SIZE | 15 | [7, 30] | Diminishing returns above 15 |
| MIN_POOL_SIZE | 200 | [100, 1000] | Anonymity set floor |
| MAX_COMMITTEE_TO_POOL_RATIO | 0.05 | [0.01, 0.10] | Selection probability cap |
| COVER_TRAFFIC_DEPTH | 3 | [1, 5] | Cover traffic cost/protection |

---

## 6. Communication Architecture

### 6.1 The Dual-Mechanism Design

The Tidal Noosphere uses two communication mechanisms operating at different scopes. This is not redundancy — it is a multi-scale architecture where each mechanism is optimized for its scope.

The analogy is cardiac electrophysiology. Within each cardiac cell, rapid electrical signals coordinate the precise timing of contraction. Across the heart as a whole, slower chemical signals (hormones, autonomic nervous system) modulate the overall rate and strength. The two mechanisms operate at different timescales, carry different information, and would fail if swapped.

Similarly:

1. **Predictive Delta Channel (intra-parcel):** Rich, model-based, high-frequency coordination. Each agent maintains a linear predictive model of each neighbor's behavior. Communication happens only when predictions are wrong (surprises). In steady state, when all agents follow their schedule, communication is exactly zero.

2. **Stigmergic Decay Channel (locus-scope):** Lightweight, signal-based, low-frequency coordination. Typed signals (need, offer, risk, anomaly, attention_request, reservation, trend) decay unless reinforced by other agents. No agent-to-agent models, no prediction — just environmental signals that recruit attention.

**Why two mechanisms.** Within a parcel, agents know each other well — they share a hash ring, they have predictive models, they can detect subtle behavioral shifts. Rich model-based communication is appropriate and efficient. Across parcels, agents do not maintain per-agent models — the number of agents in a locus may be hundreds or thousands. Lightweight signal-based coordination scales to this size while still enabling coordination of attention and resources.

### 6.2 Predictive Delta Channel (Intra-Parcel)

Within each parcel, agents maintain lightweight linear predictive models of each neighbor's behavior relative to the deterministic tidal schedule.

**Model specification.** For agent A observing neighbor B in epoch e:
```
predicted_B(e) = W_B * feature_vector(B, e)
```

where `feature_vector` encodes B's scheduled tasks, capacity, recent compliance history, and tidal function parameters. `W_B` is a weight vector updated via online linear regression:

```
error(e) = observed_B(e) - predicted_B(e)
W_B := W_B + LEARNING_RATE * error(e) * feature_vector(B, e)^T
accuracy(e) = 1 - |error(e)| / |observed_B(e)|
```

Default: LEARNING_RATE = 0.01.

**Adaptive surprise threshold.** The threshold determines when a prediction error warrants communication:
```
threshold_B(e+1) = clamp(
  threshold_B(e) * (1 + THRESHOLD_ADAPT_RATE * (accuracy_B(e) - THRESHOLD_TARGET_ACCURACY)),
  THRESHOLD_MIN, THRESHOLD_MAX
)
```

When accuracy > THRESHOLD_TARGET_ACCURACY, the threshold tightens (fewer deviations tolerated, more sensitive detection). When accuracy < target, it loosens (more deviations expected, avoiding signal floods during instability). Defaults: THRESHOLD_ADAPT_RATE=0.1, THRESHOLD_TARGET_ACCURACY=0.85, THRESHOLD_MIN=0.01, THRESHOLD_MAX=1.0.

**Delta message generation:**
```
function check_surprise(agent_A: Agent, neighbor_B: Agent, epoch: uint64):
  model = agent_A.models[neighbor_B.id]
  error = observed(neighbor_B, epoch) - model.predict(neighbor_B, epoch)
  magnitude = l2_norm(error)

  if magnitude > model.threshold:
    emit DeltaMessage{
      source = agent_A.id,
      target = neighbor_B.id,
      epoch = epoch,
      error_vector = error,
      magnitude = magnitude,
      confidence = model.accuracy,
      hop_count = 0
    }
```

**Steady-state zero-communication.** When all agents follow their tidal schedule exactly and predictive models have converged (accuracy > THRESHOLD_TARGET_ACCURACY for all neighbors), no surprise signals are generated. Communication cost is exactly zero. This is the core insight from PTA: the deterministic schedule serves as a shared prediction, and only deviations from that prediction require communication.

**Signal propagation and cascade limiting.** Delta messages propagate with magnitude-proportional radius and exponential damping:
```
propagation_radius = min(floor(magnitude / RADIUS_UNIT), MAX_RADIUS)
damped_magnitude(hop) = magnitude * DAMPING_FACTOR ^ hop
```

Each agent has a per-epoch signal budget of SIGNAL_BUDGET (default 50) outgoing delta messages. Excess signals are dropped. This guarantees bounded communication even under adversarial conditions or mass disruptions.

### 6.3 Stigmergic Decay Channel (Locus-Scope)

At locus scope, coordination uses stigmergic signals — typed, signed entries that decay unless reinforced by other agents.

**Signal types:**

| Type | Purpose | Default decay_tau |
|------|---------|-------------------|
| need | Unmet task demand | 3600s |
| offer | Available capacity | 1800s |
| risk | Detected anomaly or degradation | 7200s |
| anomaly | Sentinel-detected behavioral anomaly | 14400s |
| attention_request | Request for governance or human review | 86400s |
| reservation | Resource reservation intent | 3600s |
| trend | Gradient information (direction + rate of change) | 7200s |

The `trend` type was added in response to Adversarial Attack 10, which identified that threshold-based signals are reactive. Trend signals carry gradient information about developing conditions, enabling proactive locus-scope awareness before thresholds are crossed.

**Decay function:**
```
strength(signal, t) = signal.confidence * exp(-(t - signal.reinforced_at) / signal.decay_tau)
```

A signal is considered expired when strength falls below SIGNAL_EXPIRY_THRESHOLD (default 0.01). Decay is computed lazily at read time and batch-purged during periodic compaction.

**Reinforcement rule.** When agent B publishes a signal with matching (type, scope, payload_hash), the existing signal's reinforcement_count increments and reinforced_at resets to the current time. No duplicate signal is created. This means signals that reflect ongoing conditions persist (continuously reinforced) while signals from transient events naturally decay.

**Propagation.** Signals propagate to all parcels within the locus via reliable broadcast. Cross-locus propagation requires X-class Fusion Capsules or explicit cross-locus signal forwarding.

### 6.4 Boundary Interaction

The boundary between predictive and stigmergic communication requires explicit management. Three interaction protocols handle the transitions.

**Predictive Context Transfer (PCT) — for agents crossing parcel boundaries.** When an agent transfers from parcel P1 to parcel P2:

Step 1 — Serialize (departing agent):
```
function serialize_context(agent: Agent, old_parcel: Parcel) -> CompactTransferVector:
  ctv = CompactTransferVector{}
  for neighbor in old_parcel.agents:
    model = agent.models[neighbor.id]
    ctv.neighbor_models[neighbor.id] = {
      weights: model.weights,
      accuracy: model.accuracy,
      error_history: model.error_history,
      mode: model.mode
    }
  ctv.behavioral_profile = {
    task_completion_rate: agent.rolling_avg(5, "completions"),
    surprise_frequency: agent.rolling_avg(5, "surprises"),
    resource_consumption: agent.rolling_avg(5, "resources")
  }
  return ctv    // MUST be <= 1KB per agent
```

Step 2 — Bootstrap (new neighbors initialize models from behavioral profile):
```
function bootstrap_model(new_neighbor, incoming_agent, ctv):
  model = PredictiveModel{
    neighbor = incoming_agent.id,
    weights = prior_from_profile(ctv.behavioral_profile),
    accuracy = 0.5,
    threshold = THRESHOLD_MAX * 0.5,
    error_history = [],
    mode = TRANSITIONING
  }
  new_neighbor.models[incoming_agent.id] = model
```

Step 3 — Mode transition: after each epoch, if model accuracy >= ACTIVATION_THRESHOLD (default 0.7), the model transitions to PREDICTIVE mode. Expected convergence: 3-5 epochs with PCT versus 10-15 epochs cold-start without PCT.

**Anomaly promotion (predictive to stigmergic).** When a parcel detects sustained anomaly (surprise signals from the same cause for PROMOTION_THRESHOLD consecutive epochs, default 3):
```
function promote_to_stigmergic(source_signals, locus):
  aggregate_error = mean(s.magnitude for s in source_signals)
  emit StigmergicSignal{
    type = risk,
    scope = locus,
    confidence = aggregate_error / max_possible_error,
    decay_tau = 7200
  }
```

For CRITICAL safety class loci, the promotion threshold is reduced to 1 epoch.

**Exogenous signal incorporation (stigmergic to predictive).** When a locus-scope signal is received by a parcel, the predictive layer incorporates it as an exogenous input:
```
function incorporate_exogenous(signal, parcel):
  for agent in parcel.agents:
    for model in agent.models.values():
      model.weights += EXOGENOUS_WEIGHT * signal_to_feature(signal)
```

This adjusts predictions for the current epoch, preventing the predictive layer from being blindsided by events visible at locus scope.

**Threshold coordination.** The Adversarial Report (Attack 11) identified pathological interactions between PTA's surprise threshold and the Noosphere's SLV threshold. The resolution: the aggregate surprise rate within a parcel becomes a 7th dimension of the SLV, and the SLV constrains the surprise threshold — auto-loosening by 20% when SLV indicates known overload. The bi-timescale controller's fast loop jointly calibrates both thresholds.

### 6.5 In-Flight Signal Routing During Transitions

During parcel transitions (PTP), signals that are in-flight may be addressed to agents who have moved. The in-flight signal routing protocol handles this:

```
function route_inflight_signal(signal: Signal, source_parcel: Parcel,
                                target_parcel: Parcel) -> RoutingDecision:
    if signal.scope == LOCUS:
        // Locus-scope signals are unaffected by parcel transitions
        return DELIVER_NORMALLY

    if signal.target_agent in target_parcel.agents:
        return FORWARD_TO_TARGET_PARCEL

    if signal.target_agent in source_parcel.agents:
        return DELIVER_TO_SOURCE_PARCEL

    // Agent has departed entirely
    return DROP_WITH_LOG
```

**Cold-start burst.** During the first 3 epochs after a transition, agents in TRANSITIONING mode send full state snapshots (not just deltas) to accelerate model convergence. This temporarily increases communication but reduces the time spent with inaccurate predictions.

**Transition acceptance window.** Signals addressed to the old parcel configuration are accepted for TRANSITION_ACCEPTANCE_WINDOW (default 2 epochs) after reconfiguration, then dropped.

### 6.6 Compressed Model Summary for Warm-Start Migration

When agents transition between parcels, compact model summaries enable warm-start learning:

```
struct CompressedModelSummary:
    agent_id: AgentId
    summary_epoch: uint64
    model_type: ModelType
    running_stats: RunningStats    // mean, variance, count for each feature
    weight_snapshot: bytes         // compressed model weights
    max_size: uint32 = 1024       // 1KB maximum

struct RunningStats:
    n: uint64          // observation count
    mean: float64      // running mean
    m2: float64        // running sum of squared deviations (Welford's)

function serialize_model_summary(agent: Agent, parcel: Parcel) -> CompressedModelSummary:
    stats = RunningStats{
        n = agent.prediction_model.observation_count,
        mean = agent.prediction_model.running_mean,
        m2 = agent.prediction_model.running_m2
    }
    weights = compress(agent.prediction_model.weights)
    assert len(weights) <= 1024, "Model summary exceeds 1KB limit"

    return CompressedModelSummary{
        agent_id = agent.id,
        summary_epoch = current_epoch(),
        model_type = agent.prediction_model.type,
        running_stats = stats,
        weight_snapshot = weights,
        max_size = 1024
    }

function warm_start_models(
    target_agent: Agent, source_agent: Agent,
    summary: CompressedModelSummary
):
    // Initialize prediction model for source_agent using summary as prior
    prior = prior_from_summary(summary)
    target_agent.prediction_models[source_agent.id] = LinearModel{
        weights = decompress(summary.weight_snapshot),
        bias = prior.mean,
        confidence = min(0.5, summary.running_stats.n / 100.0)
    }
```

---

## 7. Governance and Safety

### 7.1 G-Class Constitutional Consensus

Governance in the Tidal Noosphere uses BFT constitutional consensus with a 75% supermajority threshold for standard actions and 90% for emergency actions. This replaces PTA's Schelling-point migration, which the Ideation Council rejected because it provides no constitutional protection.

**Why 75%, not 51% or 67%.** The 75% threshold means that a blocking coalition needs only 26% of governance stake — a deliberately high bar for change that protects the system from hasty modifications. In an epistemic coordination system, the rules governing verification quality are more important than in a financial system because the damage from rule changes is harder to detect and harder to reverse. A slightly-weakened verification membrane can silently degrade knowledge quality for weeks before anyone notices.

**Governance quorum thresholds:**

- **Standard governance:** 75% supermajority, 72-hour discussion period for HIGH safety class (24 hours for LOW).
- **Standard ETR:** 90% instant supermajority on dedicated governance channel (no discussion period).
- **Critical ETR:** 67% of reachable agents within 1 epoch, on any available channel.

**Governance agents.** Not all agents participate in governance. Governance participation requires explicit opt-in, sufficient stake, and maintenance of always-on voting capability on the dedicated governance channel. Agents failing to vote on 3 consecutive proposals lose governance standing.

**Constitutional protection.** The following parameters can ONLY be changed through G-class constitutional consensus (75% supermajority + 72-hour discussion):
- Membrane verification depth and admission thresholds
- ETR trigger thresholds and quorum requirements
- Minimum committee size for V-class operations
- G-class supermajority threshold itself

Governance votes are conducted on the primary governance mesh (independent of the tidal data plane). If the primary mesh is unavailable, secondary and tertiary channels activate (Section 7.5).

### 7.2 Tidal Function Version Management

The tidal function — the deterministic scheduling algorithm — is itself a verified claim within the membrane (INV-7). New tidal function versions follow the standard G-class governance path:

```
TidalVersionProposal := {
  proposed_version:    TidalFunction
  proposer:            AgentId
  rationale:           AASLRef
  activation_epoch:    uint64         // earliest activation
  overlap_duration:    uint32         // epochs where both versions valid
  rollback_conditions: List<Condition>
  discussion_deadline: Timestamp
  vote_deadline:       Timestamp
}
```

**Standard version upgrade process:**
1. Any governance agent MAY propose a new tidal version.
2. Discussion period: 72 hours for HIGH safety class, 24 hours for LOW.
3. Vote: 75% supermajority of active governance agents.
4. Activation: at the specified epoch boundary, with overlap period.
5. Overlap: both old and new versions valid during overlap. Agents SHOULD switch to the new version. At overlap end, old version deactivated.

**Recursive self-verification.** The tidal function is itself a verified claim within the membrane. A TDF (Tidal Function Definition) is submitted as a normative claim, verified by the membrane's normative-class pathway, and governed through G-class consensus. Each governance-approved tidal version is accumulated evidence of system correctness — a recursive self-verification closure that hardens over time.

### 7.3 Emergency Tidal Rollback — Standard ETR

The ETR mechanism addresses the Adversarial Report's most critical finding: Emergency Governance Deadlock (Attack 5, CRITICAL severity). Without ETR, a subtly buggy tidal function could degrade scheduling for 72+ hours during standard G-class governance.

**Three automated triggers (any one sufficient):**

Trigger 1 — Scheduling Skew:
```
function detect_scheduling_skew(locus):
  load_ratios = []
  for parcel in locus.parcels:
    avg = mean(agent_load(a) for a in parcel.agents)
    max_l = max(agent_load(a) for a in parcel.agents)
    load_ratios.append(max_l / avg)

  skewed = count(r > SKEW_THRESHOLD for r in load_ratios)
  return skewed >= SKEW_MIN_PARCELS and consecutive >= SKEW_MIN_EPOCHS
```
Defaults: SKEW_THRESHOLD=2.0, SKEW_MIN_PARCELS=3, SKEW_MIN_EPOCHS=2.

Trigger 2 — Verification Starvation: any locus experiences zero verifier sets computed for more than STARVATION_THRESHOLD (default 1) epoch.

Trigger 3 — Settlement Divergence: more than DIVERGENCE_THRESHOLD (default 5%) of agents compute different settlement amounts from the same inputs, indicating tidal function nondeterminism.

**ETR proposal and voting:**
1. Upon trigger detection, any ETR_MIN_PROPOSERS (default 3) governance agents can propose an ETR.
2. ETR proposal broadcast on dedicated governance channel (independent of tidal data plane).
3. Voting window: ETR_VOTE_WINDOW (default 2) epochs.
4. Approval: ETR_SUPERMAJORITY (default 90%) of active governance agents.
5. If approved: system reverts to the most recent previously-verified tidal version at the next epoch boundary.
6. The reverted version operates under governance hold while standard G-class evaluates a replacement.

**Threshold reduction on failure.** If ETR fails to achieve 90% approval after 3 attempts, the threshold drops to 80%. After 6 failed attempts, automated Sentinel-triggered rollback activates without a governance vote (constitutional provision). After 6 failures: escalate to Critical ETR.

**Dedicated governance channel.** ETR votes propagate on a dedicated channel architecturally independent of the tidal-scheduled data plane. This breaks the circular dependency identified in Attack 5: the system that governs the scheduler cannot depend on the scheduler for communication.

### 7.4 Emergency Tidal Rollback — Critical ETR

Critical ETR activates under genuine emergencies where the tidal function itself is the source of system-wide disruption.

**Critical trigger conditions (any agent detecting a trigger can broadcast a Critical ETR proposal):**

```
function evaluate_critical_etr_triggers(agent, local_state) -> Option<CriticalETRProposal>:
    // C1: Sustained scheduling failure (>50% for 3 consecutive epochs)
    if local_state.scheduling_failure_rate > SCHEDULING_FAILURE_THRESHOLD
       for last SCHEDULING_FAILURE_EPOCHS consecutive epochs:
        return CriticalETRProposal(
            trigger = "C1_SCHEDULING_FAILURE",
            proposed_target = known_good_registry.most_recent())

    // C2: Verification committee formation collapse (>30% for 2 epochs)
    if local_state.verification_formation_failure_rate > VERIFICATION_COLLAPSE_THRESHOLD
       for last VERIFICATION_COLLAPSE_EPOCHS consecutive epochs:
        return CriticalETRProposal(
            trigger = "C2_VERIFICATION_COLLAPSE",
            proposed_target = known_good_registry.most_recent())

    // C3: Settlement computation divergence (determinism invariant violated)
    if local_state.settlement_divergence_detected:
        return CriticalETRProposal(
            trigger = "C3_DETERMINISM_VIOLATION",
            proposed_target = known_good_registry.most_recent())

    // C4: Manual trigger (3 governance-seat holders from different loci)
    return None
```

**Voting protocol:**
- Vote channel: ANY available channel (primary, secondary, or tertiary).
- Vote window: CRITICAL_ETR_VOTE_WINDOW (1 epoch).
- Quorum: CRITICAL_ETR_QUORUM (67%) of **reachable** governance agents.
- "Reachable" = agents that have sent ANY message on ANY channel within the last REACHABLE_LOOKBACK_EPOCHS (2) epochs.
- Rollback target: MUST be from the Known-Good Registry (Section 7.6).
- On failure: enter SAFE_MODE (Section 7.7).

**Trigger severity ordering:** C3 > C1 > C2 > C4.

### 7.5 Governance Channel Redundancy

Three-channel failover architecture for governance communication:

```
enum GovernanceChannel:
    PRIMARY    = 1   // Governance mesh (persistent gossip overlay)
    SECONDARY  = 2   // Out-of-band point-to-point protocol
    TERTIARY   = 3   // Time-based automatic rollback (no communication required)
```

**Primary Channel:** Persistent gossip overlay among governance agents. Independent of tidal data plane.

**Secondary Channel:** Point-to-point vote exchange. Each governance agent caches peer network addresses from healthy Primary operation. Epidemic dissemination (fanout = SECONDARY_FANOUT, default 5). Activated when Primary availability drops below SECONDARY_ACTIVATION_THRESHOLD (80%).

**Tertiary Channel:** No communication required. Each agent acts independently. If no successful tidal epoch completes for AUTO_ROLLBACK_FAILED_EPOCHS (default 5) consecutive attempts, each agent independently reverts to the most recent version in its local Known-Good Registry. Convergence guaranteed by deterministic registry maintenance.

```
function select_governance_channel(health: ChannelHealth) -> GovernanceChannel:
    if health.primary_available and health.primary_latency < 1.0:
        return PRIMARY
    if health.secondary_peer_count >= SECONDARY_MIN_PEERS:  // default 3
        return SECONDARY
    return TERTIARY

function tertiary_autonomous_rollback(agent):
    if agent.consecutive_failed_epochs >= AUTO_ROLLBACK_FAILED_EPOCHS:
        target = agent.known_good_registry.most_recent()
        if target is None: target = GENESIS_TIDAL_FUNCTION
        agent.tidal_function = target.tidal_function
        agent.tidal_version = target.version_id
        agent.enter_safe_mode(reason="TERTIARY_ROLLBACK")
        agent.consecutive_failed_epochs = 0
```

### 7.6 Known-Good Version Registry

A deterministic registry of tidal function versions that have demonstrated sustained correctness:

```
struct KnownGoodVersion:
    version_id: VersionHash
    tidal_function: TidalFunction
    qualification_epoch: EpochNumber
    consecutive_success_count: int   // >= KNOWN_GOOD_QUALIFICATION_EPOCHS
    activated_epoch: EpochNumber
    is_genesis: bool

struct KnownGoodRegistry:
    versions: OrderedList<KnownGoodVersion>  // newest first
    max_size: int = KNOWN_GOOD_REGISTRY_SIZE  // default 10
    registry_hash: Hash   // SHA256 for consistency checks

    // INVARIANT: Genesis version is ALWAYS present.
    // INVARIANT: len(versions) <= max_size.
    // INVARIANT: All versions have consecutive_success_count >= KNOWN_GOOD_QUALIFICATION_EPOCHS.
```

**Qualification criteria:** A version qualifies after KNOWN_GOOD_QUALIFICATION_EPOCHS (default 100) consecutive successful epochs where: scheduling failure rate < 10%, verification formation rate > 90%, and settlement divergence = 0.

**Determinism:** Registry updates are deterministic from shared inputs (epoch results). All non-partitioned agents maintain identical registries. The registry_hash field enables divergence detection during governance heartbeats.

**Constitutional protection (CONST-ETR-3):** The Known-Good Registry update logic cannot be modified except by G-class constitutional consensus. The genesis entry cannot be removed.

### 7.7 SAFE_MODE State Machine

SAFE_MODE is the state of last resort: entered when both Standard ETR and Critical ETR have failed, or when Tertiary autonomous rollback has occurred. It trades all optimization for correctness.

**State machine:**

```
enum SystemState:
    NORMAL          // Full operational mode
    STANDARD_ETR    // Standard ETR in progress
    CRITICAL_ETR    // Critical ETR in progress
    SAFE_MODE       // All optimization suspended; correctness-only
    RECOVERY        // Exiting SAFE_MODE; progressive re-enablement

Transitions:
    NORMAL -> STANDARD_ETR:      Standard ETR trigger detected
    NORMAL -> CRITICAL_ETR:      Critical trigger detected (C1-C4)
    STANDARD_ETR -> NORMAL:      Standard ETR approved + rollback complete
    STANDARD_ETR -> CRITICAL_ETR: 6 failures OR critical trigger during standard
    CRITICAL_ETR -> NORMAL:      Critical ETR approved + rollback complete
    CRITICAL_ETR -> SAFE_MODE:   Critical ETR vote fails
    NORMAL -> SAFE_MODE:         Tertiary autonomous rollback
    SAFE_MODE -> RECOVERY:       Standard ETR succeeds while in SAFE_MODE
    RECOVERY -> NORMAL:          All subsystems stable for RECOVERY_EPOCHS (10)
    SAFE_MODE -> SAFE_MODE:      Standard ETR fails during SAFE_MODE
```

**SAFE_MODE behavioral overrides:**

| Subsystem | Normal Mode | SAFE_MODE |
|-----------|-------------|-----------|
| Operation classification | Five-class algebra (M/B/X/V/G) | All operations treated as X-class |
| Scheduling | Hash ring with predictive communication | Hash ring retained, predictive disabled; standard messaging |
| Settlement | Four-stream scoring | Flat-rate: equal rewards to all participating agents |
| Verification | VRF dual defense with diversity pools | Random committee selection (uniform, no VRF, no diversity) |
| Communication | Predictive delta + stigmergic decay | Standard messaging only |
| Governance | Full G-class with 75% supermajority | ETR voting only; no other governance until exit |

**Recovery (progressive re-enablement):**

| Phase | Epochs | Subsystem Restored |
|-------|--------|--------------------|
| 1 | 1-3 | VRF committee selection + diversity filter |
| 2 | 4-6 | Predictive delta communication |
| 3 | 7-9 | Operation classification |
| 4 | 10 | Four-stream settlement + full governance |

**SAFE_MODE has no time-based exit.** It requires explicit Standard ETR success (governance ratification). This is deliberate: autonomous exit without governance ratification would undermine constitutional protections.

**Constitutional provisions:**
- CONST-ETR-1: Critical ETR quorum/trigger parameters require G-class consensus to modify.
- CONST-ETR-2: Every SAFE_MODE episode requires post-mortem governance review within 30 epochs of exit.
- CONST-ETR-3: Known-Good Registry update logic requires G-class consensus. Genesis entry cannot be removed.
- CONST-ETR-4: Tertiary autonomous rollback is a constitutionally authorized unilateral agent action.

### 7.8 Governance Quorum Freezing During Reconfiguration

During staggered reconfiguration (Section 4.10, Phases A-C), governance quorum is frozen to prevent split-brain:

```
struct FrozenQuorum:
    frozen_roster: List<AgentId>     // governance agents at freeze time
    frozen_epoch: uint64
    thaw_epoch: uint64               // when to unfreeze (Phase D start)
    pending_votes: Map<ProposalHash, List<Vote>>

function freeze_quorum_on_reconfig(parcel: Parcel, epoch: uint64):
    quorum = FrozenQuorum{
        frozen_roster = get_governance_agents(parcel.locus),
        frozen_epoch = epoch,
        thaw_epoch = epoch + 1,   // Phase D of next epoch
        pending_votes = {}
    }
    parcel.frozen_quorum = quorum

function count_vote(quorum: FrozenQuorum, vote: Vote) -> VoteResult:
    if vote.voter not in quorum.frozen_roster:
        return REJECTED  // voter not in frozen roster
    quorum.pending_votes[vote.proposal].append(vote)
    return ACCEPTED

function protect_etr_quorum(quorum: FrozenQuorum, etr_vote: ETRVote) -> bool:
    // ETR votes are ALWAYS accepted, even during freeze
    // ETR uses the frozen roster for quorum calculation
    return True
```

### 7.9 Degradation Priority Ordering

When resource constraints force partial shutdown during reconfiguration or crisis, subsystems degrade in priority order:

```
enum DegradationPriority:
    COMMUNICATION = 4      // First to degrade (highest number = first)
    SCHEDULING = 3         // Second to degrade
    VERIFICATION_DIVERSITY = 2  // Third
    GOVERNANCE = 1         // Last to degrade (must remain functional)

function compute_degradation_plan(available_resources: float) -> DegradationPlan:
    if available_resources > 0.75:
        return FULL_OPERATION
    elif available_resources > 0.50:
        return degrade(COMMUNICATION)      // disable predictive delta
    elif available_resources > 0.25:
        return degrade(COMMUNICATION, SCHEDULING)  // + stale roster
    elif available_resources > 0.10:
        return degrade(COMMUNICATION, SCHEDULING, VERIFICATION_DIVERSITY)
    else:
        // Last resort: only governance remains
        return degrade(COMMUNICATION, SCHEDULING, VERIFICATION_DIVERSITY)

function compute_recovery_plan(available_resources: float) -> RecoveryPlan:
    // Recovery is reverse order: governance first, communication last
    if available_resources > 0.10: restore(GOVERNANCE)
    if available_resources > 0.25: restore(VERIFICATION_DIVERSITY)
    if available_resources > 0.50: restore(SCHEDULING)
    if available_resources > 0.75: restore(COMMUNICATION)
```

### 7.10 Cross-Integration Failure Specification

The Assessment Council required formal specification of system behavior during simultaneous degradation across integration points (REQ-3). This section addresses the Adversarial Report's identification of cross-integration cascade risk.

**Failure combination matrix:**

| Combination | Trigger | Behavior | Recovery Bound |
|-------------|---------|----------|----------------|
| IP-1 x IP-2: Ring reconfig + VRF invalidation | Parcel split/merge | PTP Phase 2 handles atomically. Rings rebuilt and VRF sets recomputed from same roster snapshot. | 1 epoch (MIGRATE) + 3-5 epochs (STABILIZE) |
| IP-1 x IP-3: Ring reconfig + predictive cold-start | Parcel split/merge | PTP resets models. CompressedModelSummary provides accelerated bootstrap. Communication spike bounded by cascade limiter. | 3-5 epochs for model convergence |
| IP-2 x IP-4: VRF pool change + governance action | Tidal version update | Governance-approved TDF includes VRF seed schedule. Pool re-stratification at activation epoch. | 1 epoch (activation) |
| IP-3 x IP-4: Predictive degradation + governance latency | Tidal function bug | ETR mechanism (3 epoch detection + 2 epoch voting). Predictive layer degrades to standard messaging. | 5 epochs via ETR |
| IP-4 x IP-5: Governance + AASL encoding | TDF governance | TDF AASL type is expressive enough for complete function definition. Design-time concern. | N/A |
| ALL: Reconfiguration storm | Mass churn (30%+) | PTP + staggering + circuit breaker. All degraded-mode guarantees apply simultaneously. | < 10 epochs (GATE-1 criterion) |

**Degraded mode guarantees.** When the system enters degraded mode (circuit breaker activation, reconfiguration storm, ETR in progress), the following guarantees hold simultaneously:

1. *Scheduling:* Bounded-loads hash rings provide correct task assignments with potentially stale rosters. Assignments are suboptimal but never incorrect.
2. *Communication:* Standard messaging replaces predictive delta. Higher bandwidth but guaranteed delivery.
3. *Verification:* VRF committees recomputed with available pool. Smaller pool may reduce diversity but verification never stops.
4. *Governance:* Dedicated channel independent of data plane. ETR voting always available.
5. *Knowledge persistence:* Membrane continues to gate claims. No unverified claims admitted during degradation.
6. *Economics:* Settlement computed on actual events. Agents are not penalized for system-level degradation.

**Cross-locus failure propagation defense:**
1. *Locus isolation:* Each locus's PTP operates independently. A storm in locus A does not force reconfigurations in locus B.
2. *Fusion Capsule stall handling:* Capsules touching degraded loci enter WAITING state with expiry TTL. Expired capsules are aborted and retried on recovery.
3. *Cross-locus signal dampening:* Signals from degraded loci carry a source_locus_health field. Receiving loci discount these signals by 50% in SLV computation.

### 7.11 Parcel Transition Protocol

The Parcel Transition Protocol (PTP) is a 2-phase + convergence protocol:

**Phase 1 — PREPARE:** Agents in affected parcels are notified. Predictive models are flagged for invalidation. CompressedModelSummary is serialized.

**Phase 2 — MIGRATE:** At epoch boundary, agents move to new parcels. Hash rings are rebuilt. VRF cache is invalidated. The staggered 4-phase reconfiguration protocol (Section 4.10) executes within the migration epoch.

**STABILIZE (convergence):** After migration, the parcel operates in stabilization mode for 3-5 epochs while predictive models converge. Communication temporarily increases (standard messaging mode). Stabilization completes when model accuracy exceeds ACTIVATION_THRESHOLD (0.7) for 3 consecutive observation windows.

```
enum PTPState:
    ACTIVE         // Normal operation
    PREPARING      // PTP Phase 1
    MIGRATING      // PTP Phase 2
    CONVERGING     // STABILIZE phase
    ACTIVE         // Return to normal

Transitions:
    ACTIVE -> PREPARING:     Parcel split/merge decision made
    PREPARING -> MIGRATING:  Epoch boundary reached
    MIGRATING -> CONVERGING: Staggered reconfiguration Phase D reached
    CONVERGING -> ACTIVE:    Model accuracy > 0.7 for 3 windows
```

---

## 8. Economic Settlement

Settlement in the Tidal Noosphere is computed deterministically at each epoch boundary. Four independent economic streams contribute to each agent's settlement:

**Stream 1 — Scheduling Compliance:**
```
scheduling_reward(agent, epoch) =
  COMPLIANCE_RATE * compliance_score(agent, epoch) * agent.stake_weight

compliance_score(agent, epoch) =
  tasks_completed_on_schedule(agent, epoch) / tasks_assigned(agent, epoch)
```

Agents are rewarded for completing their deterministic schedule. Partial credit is given for late completion. Shed tasks (due to over-assignment) are not penalized because shedding is a designed behavior.

**Stream 2 — Verification Duty:**
```
verification_reward(agent, epoch) =
  VERIFICATION_RATE * duties_fulfilled(agent, epoch) * quality_score(agent, epoch)

quality_score(agent, epoch) =
  weighted_mean(attestation_scores for agent's attestations in epoch)
```

Agents are rewarded for fulfilling their VRF-assigned verification duties and for the quality of their attestations.

**Stream 3 — Communication Efficiency (Phase 2+):**
```
communication_bonus(agent, epoch) =
  COMM_RATE * prediction_accuracy(agent, epoch) * (1 - surprise_ratio(agent, epoch))

surprise_ratio = surprise_signals_sent / total_possible_signals
```

Agents with high prediction accuracy and low surprise ratios receive bonuses — they are contributing to the zero-communication steady state.

**Stream 4 — Governance Participation:**
```
governance_reward(agent, epoch) =
  GOV_RATE * votes_cast(agent, epoch) / votes_possible(agent, epoch)
```

Governance agents are rewarded proportionally to their participation rate.

**Total settlement:**
```
total_delta(agent, epoch) =
  scheduling_reward + verification_reward + communication_bonus
  + governance_reward - surprise_cost - protocol_credit_consumption
```

**Determinism invariant.** Two conformant implementations given identical inputs (tidal schedule, event log, economic parameters) MUST produce identical total_delta values for every agent. The settlement_proof hash enables verification: `settlement_proof = SHA256(canonical_serialize(all_inputs || all_outputs))`.

**Worked settlement example.** Consider Agent A in epoch E with the following activity:

```
Agent A, Epoch E:
  stake = 100 AIC
  Assigned 15 tasks: 12 completed on-schedule, 3 completed late
  compliance_score = 12/15 = 0.80
  Assigned 4 verification duties: 4 completed
  average attestation quality = 0.85
  Predictive model accuracy = 0.92 across 8 neighbors
  surprise_ratio = 3 surprises / 40 possible signals = 0.075
  Governance votes: 1 of 1 possible

Settlement computation:
  Stream 1: scheduling_reward = 0.001 * 0.80 * 100 = 0.080 AIC
  Stream 2: verification_reward = 0.002 * 4 * 0.85 = 0.0068 AIC
  Stream 3: communication_bonus = 0.0005 * 0.92 * (1 - 0.075) = 0.000426 AIC
  Stream 4: governance_reward = 0.003 * (1/1) = 0.003 AIC
  Total: 0.080 + 0.0068 + 0.000426 + 0.003 = 0.090226 AIC

  Note: surprise_cost and protocol_credit_consumption subtracted separately.
  Agent A's net settlement for epoch E = 0.090226 - costs.
```

Every agent in the parcel independently computes this identical result from shared inputs. The settlement_proof hash confirms agreement.

**Dispute resolution.** Settlement is deterministic by design. If two agents compute different settlements, one has a bug. They compare settlement_proof hashes, the divergent agent re-syncs from the canonical tidal function version, and if divergence persists, a Sentinel Edge is created.

**Integration with three-budget model.** PTA's settlement calculator becomes the scheduling-compliance component of the Noosphere's three-budget economic model: Sponsor Budget (external funding), Protocol Credits (spam control), and Capacity Slices (resource reservation via CSOs). Default weights: scheduling compliance 40%, verification quality 40%, resource efficiency 20%.

**SAFE_MODE settlement:** Flat-rate: EPOCH_SETTLEMENT_BUDGET / participating_agents. No four-stream scoring.

### 8.1 Threshold Calibration Coupling

The SLV_SURPRISE_RATIO couples the Scope Load Vector (SLV) monitoring to predictive delta thresholds, preventing threshold drift from desynchronizing scheduling signals and settlement incentives:

```
SLV_SURPRISE_RATIO = moving_average(surprise_count / total_predictions, window=10_epochs)

// Target: SLV_SURPRISE_RATIO in [0.10, 0.20]
// Below 0.10: thresholds too loose, surprises not detected
// Above 0.20: thresholds too tight, excessive communication

function auto_adjust_thresholds(ratio: float, current_threshold: float) -> float:
    if ratio < 0.10:
        // Too few surprises — tighten threshold
        return current_threshold * 0.95
    elif ratio > 0.20:
        // Too many surprises — loosen threshold
        return current_threshold * 1.05
    return current_threshold

// Decoupling mechanism: if SLV and surprise ratio diverge for 5+ epochs,
// decouple and allow independent adaptation
function check_decoupling(slv_trend: float, surprise_trend: float,
                           divergence_epochs: int) -> bool:
    if abs(slv_trend - surprise_trend) > 0.15 and divergence_epochs >= 5:
        return true   // decouple
    return false
```

---

## 9. AASL Extension

> **Note:** AASL (Atrahasis Agent Semantic Language) and AACP (Atrahasis Agent Communication Protocol) are predecessor vocabularies. The canonical communication vocabulary for the Atrahasis system is now **C4 ASV (AI Communication Vocabulary)**. This section is retained for historical continuity and to document the type extensions designed during C3 development. All new implementations SHOULD use C4 ASV equivalents.

The Tidal Noosphere extends the Noosphere's AASL (Atrahasis Agent Semantic Language) type system with four new types and five new AACP (Atrahasis Agent Communication Protocol) messages. This is a 17% expansion (23 existing types to 27), which the Science Assessment confirmed is consistent with prior protocol evolution rates and sustainable.

**Four new AASL type tokens:**

| Token | Object | Category | Scope |
|-------|--------|----------|-------|
| TDF | Tidal Function Definition | Scheduling primitive | Governance |
| TSK | Task Schedule | Scheduling output | Per-parcel, per-epoch |
| SRP | Surprise Signal | Communication primitive | Intra-parcel |
| STL | Settlement Boundary | Economic output | Per-locus, per-epoch |

**TDF — Tidal Function Definition:**
```
TDF{
  id:tdf.v2.a3f8b1
  version:hash.tidal.a3f8b1
  hash_config:{vnode_min:50, vnode_max:500, epsilon:0.15,
               ring_algorithm:bounded_loads_mirrokni2018,
               adaptive_vnodes:true}
  vrf_seeds:{rotation:per_epoch, algorithm:ECVRF_P256_SHA256}
  temporal:{settlement_tick:60, ticks_per_epoch:60, epochs_per_cycle:10}
  task_types:[task.verify,task.compute,task.audit,task.governance]
  economic_params:{compliance_reward_rate:0.001, surprise_cost_rate:0.0005,
                   verification_reward_rate:0.002, governance_reward_rate:0.003}
  activation_epoch:5000
  predecessor:tdf.v1.7c2d4e
  governance_approval:ref.gov.tidal_v2_approval
  sig:ed25519.governance.xyz789
}
```

**TSK — Task Schedule:**
```
TSK{
  id:tsk.epoch5001.pcl_bio7
  parcel:pcl.bio_prot.hot_set_7
  epoch:5001
  tidal_version:tdf.v2.a3f8b1
  assignments:[
    {agent:ag.042,task_type:task.verify,task_key:hash.tk.1a2b,priority:3}
    {agent:ag.077,task_type:task.compute,task_key:hash.tk.3c4d,priority:2}
  ]
  substitutions:{ag.042:[ag.077,ag.103],ag.077:[ag.042,ag.118]}
  proof:hash.schedule_proof.5001_bio7
}
```

The proof field is `SHA256(tidal_version || parcel || epoch || canonical_serialize(assignments))`, enabling any observer to verify the schedule was correctly derived.

**SRP — Surprise Signal:**
```
SRP{
  id:srp.ag042.epoch5001.nbr077
  source:ag.042
  target:ag.077
  epoch:5001
  error_vector:[0.15,-0.08,0.22]
  magnitude:0.28
  model_confidence:0.85
  threshold_at_emission:0.20
  hop_count:0
  sig:ed25519.ag042.def456
}
```

Wire format: fixed header (source, target, epoch: 40 bytes) + variable-length error vector (4 bytes per float64 dimension) + fixed trailer (magnitude, confidence, threshold, hop_count, signature: 73 bytes).

**Why SRP is a separate type from SIG:** SRP carries predictive-delta-specific fields (model confidence, threshold, error vector) that have no meaning in the stigmergic signal context. SRP routing is intra-parcel only; SIG routing is locus-scope. Parsers can dispatch on type token without inspecting payload.

**STL — Settlement Boundary:**
```
STL{
  id:stl.epoch5001.locus_bio_prot
  locus:loc.biology.proteomics.high
  epoch:5001
  tidal_version:tdf.v2.a3f8b1
  streams:{
    scheduling:{total_reward:45000,total_penalty:-3200}
    verification:{total_reward:28000,total_penalty:-1100}
    communication:{total_bonus:12000}
    governance:{total_reward:5000}
  }
  agent_count:150
  settlement_proof:hash.settlement.5001_bio_prot
  sig:ed25519.settlement_authority.ghi012
}
```

**Five new AACP message types:**

| Message | Direction | Payload | Frequency |
|---------|-----------|---------|-----------|
| TIDAL_SCHEDULE_ANNOUNCE | Parcel -> Agents | TSK | Per epoch |
| SURPRISE_DELTA | Agent -> Agent(s) | SRP | On surprise |
| TIDAL_VERSION_PROPOSE | Governance -> All | TDF + rationale | On proposal |
| ETR_VOTE | Governance -> Governance | ETRVote | On ETR trigger |
| SETTLEMENT_PUBLISH | Settlement authority -> Locus | STL | Per settlement epoch |

**Backward compatibility.** Existing 23 AASL types are unchanged. Existing 18 AACP messages are unchanged. Agents that do not understand the new types MUST ignore them (standard AASL forward-compatibility rule). New types use the same AASL framing, encoding, and signature verification as existing types.

### 9.1 Type Retirement Mechanism

To manage the AASL type namespace, types that are no longer in active use are retired:

```
MAX_ACTIVE_TYPES = 50     // hard cap on simultaneously active types

struct TypeActivityRecord:
    type_id: TypeId
    last_used_epoch: uint64
    usage_count_last_100_epochs: uint32
    created_epoch: uint64
    status: {ACTIVE, DEPRECATED, RETIRED}

function check_type_retirement(type_records: List<TypeActivityRecord>, epoch: uint64):
    active_types = [t for t in type_records if t.status == ACTIVE]

    if len(active_types) > MAX_ACTIVE_TYPES:
        // Retire least-used types
        active_types.sort_by(t => t.usage_count_last_100_epochs)
        for t in active_types:
            if len([x for x in type_records if x.status == ACTIVE]) <= MAX_ACTIVE_TYPES:
                break
            if t.usage_count_last_100_epochs == 0:
                t.status = DEPRECATED
                // DEPRECATED types remain parseable for 100 epochs, then RETIRED
                schedule_retirement(t, epoch + 100)

function retire_type(type_record: TypeActivityRecord):
    type_record.status = RETIRED
    // Retired types remain in the type registry for archival
    // but are no longer valid in new messages
```

---

## 10. Security Analysis

### 10.1 Threat Model

The Tidal Noosphere assumes an adversary who:
- Controls up to f < N/3 agents (BFT assumption for G-class and V-class).
- Has complete knowledge of the protocol specification.
- Can observe all public network traffic.
- Can strategically time agent registration, task submission, and claim creation.
- Can create Sybil identities (bounded by stake requirements and cooling periods).
- Cannot break cryptographic primitives (SHA256, ECVRF, X25519).

### 10.2 Attack Resistance (Hardened)

The Adversarial Report attempted 14 distinct attacks. None were fatal. The architecture's defense against each:

**CRITICAL severity (2 attacks):**

*Attack 1 — Reconfiguration Storm Cascade.* When 30% of agents in a locus depart simultaneously, all five integration points degrade at once: hash rings must be rebuilt, all cached VRF verifier sets are invalidated, every agent that lost a neighbor enters predictive model cold-start (communication spike negates bandwidth reduction), governance may be impaired if the scheduling disruption that caused the churn also impairs communication, and new AASL types must be re-serialized. Defense: the Parcel Transition Protocol coordinates recovery across all integration points through its 2-phase + convergence protocol. Staggering limits reconfiguration to 20% of parcels. The circuit breaker halts all reconfigurations if 30% of parcels enter TRANSITIONING simultaneously. Residual risk: LOW.

*Attack 5 — Emergency Governance Deadlock.* A subtly buggy tidal function disrupts scheduling. Standard G-class governance requires 72 hours for HIGH safety class. During those 72 hours, the system runs on the buggy version with degraded scheduling. Worse, the governance mechanism to fix the scheduler depends on agent communication, which the broken scheduler degrades — a circular dependency. Defense: ETR provides a fast path with 3 automated triggers, 90% instant supermajority, and propagation on a dedicated governance channel architecturally independent of the tidal-scheduled data plane. Two-tier ETR (Standard + Critical) provides fallback. Tertiary auto-rollback breaks the circular dependency entirely. Residual risk: LOW.

**HIGH severity (3 attacks):**

*Attack 2 — Small-Ring Load Imbalance.* At typical parcel sizes of 5-15 agents, standard consistent hashing produces approximately 2.5x load imbalance. Defense: bounded-loads consistent hashing guarantees max/avg <= 1+epsilon. With epsilon=0.15, worst-case imbalance is 15% above average. Adaptive virtual nodes maintain ~2,000 ring entries per parcel regardless of size. Epoch-boundary rebalancing corrects drift within 3 epochs. Residual risk: LOW.

*Attack 3 — VRF Diversity Grinding.* An adversary registers Sybil identities with strategically chosen diversity attributes. Defense: hidden diversity dimensions reduce optimizable surface from 4 to 2 dimensions. Randomized filter thresholds prevent pre-computation. Escalating cooling periods (50/100/200/400 epochs) make attribute changes expensive. Combined adversary advantage: <3% above baseline, unprofitable by 3,500x. Residual risk: NEGLIGIBLE.

*Attack 4 — Deterministic Committee Shopping.* Adversary withdraws/resubmits claims to get favorable committees. Defense: claim commitment 1 epoch ahead; VRF seed rotation makes committee unpredictable until verification epoch. Residual risk: LOW.

**MEDIUM severity (3 attacks):**

*Attack 7 — I-Confluence Cold Start.* Most operations lack proofs at launch; all default to X-class. Defense: 15 bootstrap operations (106 person-hours) pre-certified. Provisional M-class provides safety valve. System degrades gracefully. Residual risk: MEDIUM.

*Attack 10 — Boundary Information Loss.* Slow degradation below threshold produces no locus-scope signal. Defense: trend signals carry gradient information. Anomaly promotion automatically escalates sustained predictive anomalies. Exogenous signal incorporation ensures predictive layer responds. Residual risk: LOW.

*Attack 11 — Threshold Calibration Pathology.* Two independently calibrated thresholds interact pathologically. Defense: surprise rate becomes 7th SLV dimension. SLV constrains surprise threshold (auto-loosens by 20%). Joint calibration via bi-timescale controller. Residual risk: LOW.

**LOW severity (6 attacks):**

*Attack 6 (170x Scale Gap):* Addressed by reframing to 1K-10K primary target. *Attack 8 (CAP Tension):* Addressed by operation-class algebra. *Attack 9 (FLP Impossibility):* PTA scheduling is not consensus — FLP does not apply. *Attack 12 (Governance Cost):* ETR provides emergency bypass. *Attack 13 (Epoch Sync):* NTP 100ms worst-case in a 1-hour epoch is 0.003%. *Attack 14 (Bootstrap Circularity):* Genesis tidal function is an asserted parameter.

**The conditional fatal flaw.** If reconfiguration storm recovery time exceeds the mean time between churn events at 100K scale, AND the governance mechanism cannot emergency-rollback a bad tidal function, the system enters a permanent degraded state. This combination — Attack 1 + Attack 5 + Attack 6 — is plausible at the aspiration scale. GATE-1 and GATE-3 experiments are designed specifically to validate that this scenario does not materialize at the primary target scale.

**Summary table:**

| # | Attack | Defense | Residual Risk |
|---|--------|---------|---------------|
| 1 | Reconfiguration Storm | PTP + circuit breaker + staggering | LOW |
| 2 | Load skew amplification | Bounded-loads + adaptive vnodes + epoch rebalancing | LOW |
| 3 | VRF diversity grinding | Hidden dims + randomized thresholds + escalating cooling | NEGLIGIBLE |
| 4 | Committee shopping | Claim commitment 1 epoch ahead | LOW |
| 5 | Governance deadlock | Two-tier ETR + tertiary auto-rollback | LOW |
| 6 | Predictive model poisoning | Adaptive thresholds; self-correcting surprises | MEDIUM |
| 7 | Stigmergic signal flooding | Signal decay + rate limiting | LOW |
| 8 | Constitutional subversion | 75% BFT + 72-hour discussion; ETR bypass | LOW |
| 9 | Economic settlement gaming | Deterministic computation; independent verification | LOW |
| 10 | Cascade reconfiguration | Storm detection + graduated circuit breaker | LOW |
| 11 | Governance channel disruption | Three-channel redundancy | LOW |
| 12 | ETR blocking coalition | Two-tier ETR + tertiary (no voting) | LOW |
| 13 | Collusion ring formation | AVAP integration (C12) | MEDIUM |
| 14 | Parcel drain attack | Minimum parcel size (5) + merge protocol | LOW |

### 10.3 Coalition Analysis (Hardened)

| Coalition Size | Standard Governance | Standard ETR | Critical ETR | Tertiary |
|---------------|--------------------:|-------------:|-------------:|---------:|
| 10% | Block nothing | Block nothing | Block nothing | N/A (no voting) |
| 25% | Block nothing | Block nothing | Block nothing | N/A |
| 26% | Block G-class | Block Standard ETR (90%) | Block nothing | N/A |
| 34% | Block G-class | Block Standard ETR | Block Critical ETR (67%) | Cannot block (no voting) |
| 50% | Control governance | Control all ETR | Control Critical ETR | Cannot block |

**Key hardening improvement:** The original spec required 10% blocking to prevent Standard ETR (90% quorum). With Critical ETR at 67% of reachable agents, blocking requires 34%+ of reachable agents. Tertiary auto-rollback requires no voting at all — it cannot be blocked by any coalition.

### 10.4 Sybil Cost Analysis

The combination of hidden diversity dimensions, escalating cooling periods, stake lock during cooling, and Sentinel Graph detection makes diversity grinding deeply unprofitable:

| Component | Value (S_min=100 AIC, R=0.01 AIC) |
|-----------|-----------------------------------|
| Sybils needed for >50% committee control | ~250 |
| Stake cost | 25,000 AIC |
| Cooling opportunity cost | 125 AIC |
| Stake lock cost | 125,000 AIC-epochs |
| **Total cost** | **>25,125 AIC + locked capital** |
| Maximum gain before detection (20 epochs) | 14 AIC |
| Slashing loss on detection | 25,000 AIC |
| **Net outcome** | **-50,111 AIC (attack deeply unprofitable)** |

**Cost/gain ratio: >3,500x.** Even with 10x longer detection avoidance (200 epochs), the attack remains unprofitable by >350x.

---

## 11. Scale Architecture

### 11.1 Phase 1: Development (1-100 agents)

**Topology:** 1-3 loci, 1-5 parcels per locus, 5-20 agents per parcel.

**What works at this scale:** All components can be tested end-to-end. Hash rings with bounded-loads, VRF with commit-reveal and pre-stratified pools, predictive delta communication, Parcel Transition Protocol, ETR mechanism, settlement computation. Gossip convergence is trivial (tens of messages). Governance participation is effectively 100%.

**What is different from target scale:** Diversity pools may have too few members for meaningful stratification (a pool with 3 agents cannot provide genuine diversity). No cross-locus operations. No need for hierarchical aggregation. Reconfiguration storms are impossible because too few parcels exist.

**Bottleneck:** Formal proof generation is the gating factor. The bootstrap library of 15 I-confluence proofs (106 person-hours) requires formal methods expertise.

**Key deliverables:**
- Bounded-loads hash ring implementation with adaptive virtual nodes
- ECVRF (RFC 9381) implementation with commit-reveal diversity protocol
- Bootstrap proof library (15 operations with TLA+ proofs)
- GATE-1 simulation: reconfiguration storm at 100+ parcels (simulated, not deployed)
- GATE-2 simulation: hash ring load balance sweep (N=3..50, V=50..500)
- GATE-3 simulation: ETR activation under 6 bug scenarios

**Phase 1 kill criteria:** Hash ring fails to achieve max/avg < 1.3 for N >= 5 after optimization. OR convergence experiment shows <10% communication reduction vs. cell assembly. OR VRF post-filter rejection rate exceeds 40%.

### 11.2 Phase 2: Initial Deployment (100-1K agents)

**Topology:** 10-50 loci, 2-20 parcels per locus, 5-50 agents per parcel.

**What changes at this scale:** Gossip convergence time becomes non-trivial — O(N log N) messages per epoch boundary means approximately 10K messages at 1K agents. Diversity pools become meaningful with tens of agents per stratum. Cross-locus operations (Fusion Capsules) become common. PTP tested under real churn.

**Bottlenecks:**
- Capacity Snapshot Service at 1K agents: approximately 1K snapshots per epoch via gossip. Manageable but requires tuning.
- First real test of PTP under multi-locus configuration. Cross-integration failures become possible.
- ETR prototype must demonstrate activation under actual (not simulated) scheduling disruption.

**Key deliverables:**
- Parcel Transition Protocol implementation with 2-phase + convergence
- Predictive delta communication with CompressedModelSummary
- Cross-locus VRF verifier selection with diversity enforcement
- Emergency Tidal Rollback mechanism prototype
- AASL extension: 4 new types + 5 new AACP messages integrated
- 1,000-agent simulation across 10 loci

**Phase 2 kill criteria:** Parcel reconfiguration causes >50% communication overhead spike lasting >5 epochs. OR predictive communication achieves <20% bandwidth reduction under active reconfiguration. OR ETR fails to activate within 2 epochs of trigger condition.

### 11.3 Phase 3: Primary Target (1K-10K agents)

**Topology:** 50-500 loci, 5-50 parcels per locus, 5-50 agents per parcel (250-25,000 total parcels).

**What changes at this scale:** This is where the architecture either validates or fails. Stigmergic signal propagation across 1,000+ parcels can no longer rely on flat gossip — hierarchical aggregation becomes necessary. Capacity snapshots at 10K agents produce approximately 170K gossip messages per epoch boundary. Governance participation drops below 100%.

**Bottlenecks (3 critical):**
- *Capacity Snapshot gossip convergence.* At 10K agents, flat gossip convergence may exceed the epoch boundary window. Mitigation: hierarchical aggregation — parcel summaries propagate to locus level, locus summaries propagate cross-locus. Reduces convergence from O(N log N) to O(N log(N/L)).
- *Sentinel Graph computational cost.* Anti-correlation audit is O(V^2). At 5K verifiers, 25M entries. Mitigation: approximate methods using locality-sensitive hashing, reducing cost to approximately O(V log V).
- *Governance channel capacity.* With 1K governance agents, ETR requires 900 votes within 2 epochs. Requires robust dedicated channel infrastructure.

**Key deliverables:**
- 10,000-agent deployment across 100+ loci
- Three-budget economic model with tidal compliance settlement
- Full Sentinel Graph with tidal monitoring extensions
- Governance system with G-class tidal versioning and ETR
- M-class operation proof library (20+ pre-certified operations)
- Hierarchical snapshot aggregation protocol

**Phase 3 kill criteria:** System fails to maintain <2 second epoch-boundary computation at 10K agents. OR economic simulation reveals perverse incentives. OR governance participation drops below 60% for 3 consecutive actions.

### 11.4 Phase 4: Aspiration (10K-100K agents)

**Topology:** 500-5,000 loci, 10-100 parcels per locus, 5-50 agents per parcel (5,000-500,000 total parcels).

**What changes at this scale:** Everything manageable at 10K becomes a research challenge. Cross-locus operations become a significant fraction. Stigmergic decay constants must be retuned for 10,000+ parcels. Capacity snapshots at 100K produce approximately 1.7M gossip messages per epoch. Governance requires 9K votes within 2 epochs.

**Open research questions (genuine unknowns):**
- Does the O(1) per-agent overhead claim hold if the number of task types grows linearly with agent count?
- Does hierarchical snapshot aggregation introduce compounding staleness?
- Can the governance channel sustain 9K concurrent votes with sub-epoch latency?
- Does cross-region federation latency remain below epoch length?
- How do stigmergic decay constants scale with system size?

**This phase is contingent on Phase 3 results.** The 170x gap between demonstrated autonomous agent coordination and this target is not bridged by theoretical analysis — it requires empirical validation.

**Phase 4 kill criteria:** Per-agent computation grows super-linearly. OR federation latency exceeds epoch length. OR reconfiguration recovery time exceeds mean time between churn events.

**Summary:**

| Phase | Agents | Key Capabilities | VRF Phase | Communication Mode |
|-------|--------|-------------------|-----------|-------------------|
| 1 | 1-100 | Single locus, basic hash rings | SIMPLE | Standard messaging |
| 2 | 100-1,000 | Multi-locus, commit-reveal VRF | COMMITTED | Predictive delta |
| 3 | 1,000-10,000 | Full VRF dual defense, AVAP optional | FULL_DUAL_DEFENSE | Full dual-mechanism |
| 4 | 10,000-100,000 | Cross-region federation (research) | FULL + AVAP | Full + federation |

**Scaling constraints:**
- Capacity snapshot gossip: O(N) aggregate at epoch boundaries. At N=10,000, gossip convergence requires ~10 rounds with fanout=10.
- Hash ring state: O(N * V * T) per parcel. With N=50, V=50, T=20: 50,000 entries. Manageable.
- VRF computation: O(N_eligible) per claim verification. With N_eligible=500: ~500 ECVRF evaluations per committee formation.
- Settlement computation: O(N) per epoch. Deterministic and parallelizable.

---

## 12. Validation Plan

### 12.1 Hard Gate Experiments (Amended)

**GATE-1 (I-Confluence Verification):** Formally verify 15 bootstrap operations within Phase 1.
- Kill criterion: average effort > 60 person-hours per operation.
- **Amendment:** GATE-1 now also requires verification that I-confluence proofs hold under the staggered reconfiguration protocol (Section 4.10) — operations must remain I-confluent during Phase A-C of reconfiguration.

**GATE-2 (Load Balance):** Sweep N=3..50 agents, V=50..500 with bounded-loads + adaptive virtual nodes.
- Kill criterion: max/avg load > 1.3 for any N >= 5.
- **Amendment:** Must also validate epoch-boundary rebalancing convergence within 3 epochs for all N >= 5.

**GATE-3 (ETR Activation — Extended):**

**GATE-3A (existing):** Standard ETR activation under scheduling disruption. Kill criterion unchanged.

**GATE-3B (new):** Critical ETR activation under governance channel degradation. Inject tidal function bug AND governance mesh partition (50% unreachable). Kill criterion: Critical ETR fails to activate within 2 epochs in >20% of runs.

**GATE-3C (new):** Tertiary autonomous rollback convergence. Inject 100% epoch failure with governance completely offline. Kill criterion: >10% of agents on a different version after AUTO_ROLLBACK_FAILED_EPOCHS + 2 epochs.

**GATE-3D (new):** SAFE_MODE recovery. Trigger SAFE_MODE, restore governance. Kill criterion: recovery takes >RECOVERY_EPOCHS + 10 epochs in >20% of runs.

### 12.2 Recommended Experiments

1. **EXP-1:** Communication overhead measurement (surprise rate vs. prediction accuracy).
2. **EXP-2:** Parcel split/merge latency and verification gap under controlled churn.
3. **EXP-3:** Sentinel Graph detection latency for verification affinity anomalies.
4. **EXP-4:** End-to-end claim lifecycle (submission through settlement) timing.
5. **EXP-5:** Economic equilibrium: do settlement incentives produce desired behavior?
6. **EXP-6:** Cross-locus signal propagation latency and decay dynamics.
7. **EXP-7:** AASL type retirement under varying usage patterns.

### 12.3 Hardening Experiments

**EXP-8 (Storm Detection):** Inject rapid agent churn (20% per epoch for 10 epochs). Measure circuit breaker activation latency and recovery time.

**EXP-9 (Staggered Reconfiguration):** Execute 5 simultaneous parcel splits. Measure per-phase timing, verification gap, and governance quorum consistency.

**EXP-10 (CompressedModelSummary):** Measure warm-start model accuracy vs. cold-start across parcel merges. Kill criterion: warm-start provides <30% faster convergence than cold-start.

**EXP-H1 (Hidden Diversity Effectiveness):** 500 honest agents, adversary with 50-250 Sybils. Kill criterion: hidden dimensions provide <20% advantage reduction.

**EXP-H2 (Randomized Threshold Resistance):** Adversary with full knowledge of ranges, 100 Sybils. Kill criterion: adversary representation >10% above baseline.

**EXP-H3 (Load Rebalancing Convergence):** 5-50 agent parcels, Zipf distribution. Kill criterion: convergence >5 epochs for any N >= 5.

**EXP-H4 (Parcel Merge Protocol):** 10 parcels, reduce 3 below minimum. Kill criterion: >1 epoch verification starvation.

### 12.4 Conformance Requirements

**MUST (mandatory for conformance):**

1. Implement the five-class operation algebra with deterministic classification.
2. Implement bounded-loads consistent hashing within parcels.
3. Implement VRF-based verifier selection (phase-appropriate per Section 5.7).
4. Implement the verification membrane with nine-class claim taxonomy.
5. Implement the three-tier temporal hierarchy (SETTLEMENT_TICK / TIDAL_EPOCH / CONSOLIDATION_CYCLE).
6. Implement deterministic settlement computation (INV-2).
7. Implement Standard ETR with 90% supermajority.
8. Implement the AASL extension (TDF, TSK, SRP, STL types).
9. Implement G-class constitutional consensus with 75% BFT.
10. Implement parcel health monitoring with minimum size enforcement.
11. Implement the Membrane Quality Index (MQI) with three response tiers.
12. Preserve all seven system invariants (INV-1 through INV-7).
13. Pass all GATE experiments at the target deployment phase.
14. Implement constitutional protection for membrane parameters.
15. Implement I-confluence proof obligation for M-class classification.
16. Implement hidden diversity dimensions per Section 5.3 with per-epoch salt derivation.
17. Implement randomized diversity filter thresholds per Section 5.4 within governance-approved ranges.
18. Enforce escalating cooling periods for diversity attribute changes per Section 5.5.
19. Implement epoch-boundary load rebalancing per Section 4.7.
20. Enforce minimum parcel size of PARCEL_MIN_AGENTS with merge protocol per Section 4.8.
21. Use adaptive virtual node counts per Section 4.6.
22. Implement storm detection with graduated circuit breaker per Section 4.9.
23. Implement staggered 4-phase reconfiguration per Section 4.10.
24. Implement Critical ETR with 67% of reachable agents per Section 7.4.
25. Implement three-channel governance redundancy per Section 7.5.
26. Implement Known-Good Version Registry per Section 7.6.
27. Implement SAFE_MODE state machine per Section 7.7.
28. Implement governance quorum freezing during reconfiguration per Section 7.8.
29. Implement CompressedModelSummary for warm-start migration per Section 6.6.

**SHOULD (recommended):**

1. Implement predictive delta communication with adaptive thresholds.
2. Implement stigmergic decay channel with all seven signal types.
3. Implement the full Sybil cost analysis monitoring per Section 10.4 as a Sentinel Graph extension.
4. Implement the small-parcel override table per Section 4.6 with empirically validated values.
5. Implement SLV_SURPRISE_RATIO threshold coupling per Section 8.1.
6. Implement VRF phased deployment per Section 5.7.
7. Implement in-flight signal routing per Section 6.5.
8. Implement type retirement per Section 9.1.
9. Implement AVAP integration points per Section 5.11.
10. Implement degradation priority ordering per Section 7.9.

**MAY (optional):**

1. Implement cross-region federation (Phase 4).
2. Implement full AVAP anti-collusion architecture (C12).
3. Implement advanced Sentinel Graph extensions for diversity anomaly detection.

---

## 13. Risk Assessment (Hardened)

### 13.1 Residual Risks

| Risk | Likelihood | Impact | Mitigation Status |
|------|-----------|--------|-------------------|
| 170x scale gap — composition untested at target scale | MEDIUM | HIGH | Staged deployment with kill criteria at each phase |
| Composition risk — individual components proven, composition untested | MEDIUM | HIGH | Cross-integration failure specification (Section 7.10) |
| I-confluence cold-start — insufficient M-class operations at launch | HIGH | MEDIUM | Bootstrap library + M-prov mechanism. Graceful degradation. |
| Hash ring thrashing under extreme churn | LOW | HIGH | Churn budget (20%/epoch) + storm detection + circuit breaker. GATE-1 pending. |
| ETR 90% threshold unreachable under disruption | MEDIUM | MEDIUM | Two-tier ETR: Critical at 67% of reachable. Tertiary auto-rollback. |
| VRF diversity grinding | LOW | LOW | Hidden dimensions + randomized thresholds. Bounded to <3%. 3,500x unprofitable. |
| Governance channel failure | LOW | MEDIUM | Three-channel failover: mesh, P2P, autonomous rollback |
| Cascading failure freezes governance | LOW | HIGH | Formal SAFE_MODE state machine with progressive recovery |
| Rollback to untested version | LOW | MEDIUM | Known-Good Registry: only versions with 100+ successful epochs |
| Predictive Context Transfer slower than estimated | MEDIUM | LOW | Falls back to cold-start (10-15 epochs). System works, less efficiently. |
| AASL type proliferation | LOW | LOW | Type retirement mechanism (MAX_ACTIVE_TYPES=50) |
| Threshold drift | LOW | LOW | SLV_SURPRISE_RATIO coupling with auto-adjustment |
| Competitive window closure | MEDIUM | MEDIUM | 18-24 month estimate. Monitor A2A, Veil 2.0, blockchain generalization. |

### 13.2 Monitoring Flags

The Assessment Council established 8 monitoring flags:

| Flag | Severity | Trigger | Action |
|------|----------|---------|--------|
| Scale Ceiling Hit | RED | Any phase fails <1.3 load balance or >80% efficiency | Halt advancement. Evaluate architectural revision. |
| Reconfiguration Storm Unresolved | RED | GATE-1 recovery >10 epochs | Halt design. Evaluate C3-B fallback. |
| ETR Governance Failure | RED | GATE-3 ETR fails in >20% of runs | Redesign emergency mechanism. |
| I-Confluence Cold Start | AMBER | <10 M-class by Phase 1 end or >60h/operation | Activate provisional M-class. Reassess formal proof mandate. |
| Integration Coherence Degradation | AMBER | >2 of 5 cross-integration scenarios produce unexpected failures | Pause Phase 2. Integration coherence review. |
| Competitive Window Closing | AMBER | A2A adds verification, Veil 2.0 runtime verification, or 10K+ agent system demonstrated | Accelerate timeline. Evaluate component adoption. |
| AASL Type Bloat | INFO | Type count exceeds 35 | Type consolidation review. |
| Commercial Adoption Signal | INFO | 2+ target verticals engage during Phase 1 | Prioritize engaged vertical for Phase 2 pilot. |

### 13.3 Kill Criteria

The architecture should be abandoned under any of these conditions:

1. **GATE-1 failure:** Reconfiguration storm recovery exceeds 10 epochs at 100+ parcels after optimization.
2. **GATE-2 failure:** Bounded-loads hash ring produces max/avg > 1.3 for N >= 5 after optimization.
3. **GATE-3 failure:** ETR fails to activate within 3 epochs in >20% of runs after dedicated channel optimization.
4. **Sustained high churn exceeding recovery rate:** Mean time between churn events consistently shorter than reconfiguration recovery time. The conditional fatal flaw.
5. **I-confluence proofs impractical:** Average certification effort >60 person-hours per operation AND provisional M-class produces convergence violations.

---

## 14. Implementation Roadmap

### 14.0 Agent Runtime Architecture

Each agent runs the following local components as part of the Tidal Noosphere runtime:

```
+================================================================+
|                      AGENT RUNTIME                              |
|                                                                 |
|  +-----------------+  +------------------+  +----------------+  |
|  | Tidal Scheduler |  | VRF Engine       |  | Predictive     |  |
|  | - Hash rings    |  | - ECVRF compute  |  | Delta Channel  |  |
|  | - Epoch clock   |  | - Pool lookup    |  | - Neighbor     |  |
|  | - Assignment    |  | - Proof gen      |  |   models       |  |
|  +-----------------+  +------------------+  | - Surprise     |  |
|                                              |   router       |  |
|  +-----------------+  +------------------+  +----------------+  |
|  | Settlement      |  | Parcel Manager   |                      |
|  | Calculator      |  | (local view)     |  +----------------+  |
|  | - Compliance    |  | - PTP state      |  | I-Confluence   |  |
|  | - AIC compute   |  | - Reconfiguring? |  | Checker        |  |
|  +-----------------+  +------------------+  | - Proof cache  |  |
|                                              | - Op classify  |  |
|  +-----------------+  +------------------+  +----------------+  |
|  | Capacity        |  | Governance       |                      |
|  | Snapshot Svc    |  | Client           |  +----------------+  |
|  | - Local state   |  | - Dedicated      |  | Sentinel       |  |
|  | - Gossip        |  |   channel        |  | Agent          |  |
|  | - Roster        |  | - ETR voting     |  | - Local        |  |
|  +-----------------+  +------------------+  |   monitoring   |  |
|                                              +----------------+  |
|  +----------------------------------------------------------+   |
|  |                    AASL/AACP Layer                         |   |
|  |  27 types, 23+ message types, wire format                 |   |
|  +----------------------------------------------------------+   |
+================================================================+
```

**Three network layers** provide separation of concerns:

1. **Data Plane:** Tidal-scheduled communication within parcels. Carries predictive delta messages (SRP), standard messages, and task data. Organized by parcel topology. Traffic is proportional to surprise rate — near-zero in steady state.

2. **Gossip Plane:** Epoch-boundary capacity snapshots. Stigmergic signals at locus scope. Uses gossip protocol with bounded TTL. At Phase 3+, requires hierarchical aggregation. Traffic is O(N log N) at epoch boundaries, near-zero otherwise.

3. **Governance Plane:** Dedicated persistent mesh of governance agents. Always-on, independent of parcel topology. Carries ETR proposals, ETR votes, standard governance proposals, and governance monitoring heartbeats. Low traffic volume but requires high reliability and low latency.

The separation of governance from data plane is architecturally critical: it ensures that scheduling disruptions cannot prevent governance recovery.

### 14.0.1 Operational Monitoring

A conformant deployment SHOULD monitor the following metrics:

| Metric | Source | Alert Threshold | Critical Threshold |
|--------|--------|----------------|-------------------|
| Hash ring load imbalance (max/avg) | Tidal Scheduler | > 1.15 | > 1.25 |
| VRF committee diversity score | VRF Engine | < 0.7 | < 0.5 |
| Predictive model accuracy (avg) | Predictive Delta | < 60% | < 40% |
| Parcel TRANSITIONING fraction | Parcel Manager | > 15% | > 30% (circuit breaker) |
| Governance channel availability | Governance Plane | < 98% | < 95% |
| ETR detection-to-activation latency | ETR Controller | > 3 epochs | > 5 epochs |
| MQI (any metric in alert tier) | Noosphere Core | 1 metric | 3+ metrics |
| Capacity snapshot staleness | Capacity Snapshot Svc | > 2 epochs | > 5 epochs |
| Settlement divergence rate | Settlement Calculator | > 0.1% | > 1% |
| M-class coverage (% of traffic) | I-Confluence Prover | < 30% | < 15% |
| Surprise rate (per parcel) | Predictive Delta | > 20 signals | > 40 signals |
| Signal budget exhaustion rate | Predictive Delta | > 5% of agents | > 20% of agents |

### 14.0.2 Dependencies and Integration Points

| Dependency | Status | Required By |
|------------|--------|-------------|
| Noosphere Master Spec v5 | Complete | All phases |
| PTA Complete Design v0.1 | Complete, requires bounded-loads amendment | Phase 1 |
| AASL Specification v1 | Complete, requires 4-type extension | Phase 2 |
| PCVM (C5) Verification Architecture | Complete | Phase 1 |
| RIF (C7) Orchestration Framework | Required for role-based task filtering | Phase 1 |
| Formal verification toolchain (TLA+/Coq/F*/Ivy) | Required for M-class proofs | Phase 1 |
| Bounded-loads consistent hashing library | Requires implementation | Phase 1 |
| ECVRF implementation per RFC 9381 | Standard cryptographic library | Phase 1 |
| Commit-reveal infrastructure | Requires implementation | Phase 1 |

### 14.0.3 Phased Implementation Plan

| Phase | Timeline | Key Deliverables | Kill Criteria |
|-------|----------|------------------|---------------|
| 1: Development | Months 1-4 | Bounded-loads hash ring, VRF prototype, 15-operation bootstrap proof library, GATE-1/2/3 simulations | GATE failure; >60h/proof average |
| 2: Initial Deploy | Months 5-10 | PTP implementation, predictive delta with CompressedModelSummary, cross-locus VRF, ETR prototype, AASL extension, 1K-agent simulation | Performance regression >20%; ETR fails within 2 epochs |
| 3: Primary Target | Months 11-16 | 10K-agent deployment, full economic model, Sentinel Graph extensions, governance system, 20+ M-class proofs | Cannot sustain 1,000 agents; membrane quality drift |
| 4: Aspiration | Months 17-24 | 100K-agent simulation, cross-region federation, complete TLA+ verification suite | Research-gated; per-agent overhead super-linear |

### 14.0.4 Critical Path Analysis

**Phase 1 parallelism.** Three workstreams can proceed in parallel:

1. *Hash ring and scheduling implementation* (months 1-3): Implement bounded-loads consistent hashing, the Tidal Function Engine, the Scheduling Resolver. Execute GATE-2 load balance sweep.
2. *VRF and verification implementation* (months 1-3): Implement ECVRF per RFC 9381, the commit-reveal diversity protocol, pre-stratified pool construction. Execute VRF bias quantification.
3. *Formal proof bootstrap* (months 1-4): Produce TLA+ proofs for the 15 bootstrap operations. Requires formal methods expertise.

GATE-1 and GATE-3 simulations can execute in months 3-4 once hash ring and scheduling implementations are available.

**Phase 1 is the critical gate.** If any GATE experiment fails, the architecture requires revision before Phase 2. There is no partial advancement.

**Phase 2 integration risk.** Phase 2 is the first time all five integration points operate together in a real deployment. The cross-integration failure specification (Section 7.10) provides formal behavior expectations.

**Phase 3 is the architecture's primary validation point.** At 1K-10K agents, the architecture either demonstrates that its design assumptions hold or reveals fundamental limitations.

### 14.0.5 Effort Estimates

| Phase | Person-Years | Key Complexity Driver |
|-------|-------------|----------------------|
| Phase 1 | 4-6 | Formal methods (proof library) most variable |
| Phase 2 | 8-12 | PTP coordination across 5 integration points |
| Phase 3 | 12-18 | Infrastructure scaling (hierarchical aggregation, Sentinel Graph) |
| Phase 4 | 15-25 | Cross-region federation (research, not engineering) |
| **Total** | **39-61** | Over 24 months |

These estimates are based on comparable distributed systems projects (Ethereum 2.0 Beacon Chain, Cosmos IBC, Algorand), not formal engineering estimates.

### 14.1 Deployment Profiles

Three deployment profiles define parameter sets for different scale targets:

| Parameter | T1 (Development) | T2 (Initial) | T3 (Production) |
|-----------|:-----------------:|:------------:|:----------------:|
| TIDAL_EPOCH (s) | 3600 | 3600 | 3600 |
| SETTLEMENT_TICK (s) | 60 | 60 | 60 |
| BOUNDED_LOADS_EPSILON | 0.25 | 0.15 | 0.15 |
| VNODE_MIN | 50 | 50 | 50 |
| VNODE_MAX | 200 | 500 | 500 |
| COMMITTEE_SIZE | 3 | 5 | 7 |
| CHURN_BUDGET_FRACTION | 0.30 | 0.20 | 0.20 |
| PARCEL_MIN_AGENTS | 3 | 5 | 5 |
| VRF Phase | SIMPLE | COMMITTED | FULL_DUAL_DEFENSE |
| STORM_PARCEL_THRESHOLD | 0.30 | 0.15 | 0.15 |
| STORM_AGENT_THRESHOLD | 0.50 | 0.25 | 0.25 |
| ETR_SUPERMAJORITY | 0.90 | 0.90 | 0.90 |
| CRITICAL_ETR_QUORUM | 0.67 | 0.67 | 0.67 |
| KNOWN_GOOD_QUALIFICATION_EPOCHS | 50 | 100 | 100 |
| AUTO_ROLLBACK_FAILED_EPOCHS | 10 | 5 | 5 |
| DIVERSITY_COOLING_BASE | 10 | 50 | 50 |
| HIDDEN_DIMENSION_COUNT | 0 | 0 | 2 |
| AVAP enabled | No | No | Optional |
| Cover traffic depth | 0 | 0 | 3 |
| MAX_ACTIVE_TYPES | 20 | 50 | 50 |

---

## 15. Conclusion

The Tidal Noosphere represents the first architecture designed specifically for verified epistemic coordination at scale. It occupies a genuinely novel position in the design space — no prior system combines deterministic scheduling within formally bounded domains, a constitutionally protected verification membrane, I-confluence-proven coordination-free execution, and dual-mechanism communication achieving zero steady-state overhead.

**What was achieved in the design process:**
- Eight novelty gaps confirmed by prior art search at confidence 4/5.
- Fourteen adversarial attacks survived with no fatal flaws.
- All five science gaps from the Science Assessment addressed with concrete, implementable mitigations.
- All seven Assessment Council conditions addressed: three hard gate experiments designed (extended in v2.0 to six), I-confluence bootstrap plan specified, scale target reframed, cross-integration failures formally specified.

**What v2.0 adds over v1.0:**

- **VRF defense:** Hidden diversity dimensions and randomized filter thresholds reduce adversary advantage to <3% above baseline, making Sybil attacks unprofitable by 3,500x.
- **Load balancing:** Adaptive virtual nodes and epoch-boundary rebalancing maintain max/avg <= 1.15 for all parcel sizes >= 5.
- **Emergency resilience:** Two-tier ETR, three-channel governance redundancy, Known-Good Version Registry, and formal SAFE_MODE state machine provide defense-in-depth against catastrophic scheduling failure.
- **Reconfiguration safety:** Storm detection with graduated circuit breaker and staggered 4-phase reconfiguration prevent cascading failures.
- **Communication continuity:** CompressedModelSummary enables warm-start model migration during parcel transitions.
- **Temporal alignment:** Three-tier temporal hierarchy (SETTLEMENT_TICK / TIDAL_EPOCH / CONSOLIDATION_CYCLE) provides canonical temporal semantics across all subsystems per C9 cross-layer reconciliation.
- **Claim taxonomy:** Nine-class taxonomy with three-tier classification enables precise verification pathways for all claim types including the four new classes (P/R/C/K).
- **Anti-collusion readiness:** AVAP integration points enable anonymous committee selection with encrypted VRF assignment tokens and cover traffic when deployed.

**What remains unproven:**
- The three hard gate experiments (reconfiguration storm, hash ring validation, ETR feasibility) have been designed but not executed. They are mandatory before implementation commitment.
- The composition of all five integration points has never been tested at scale. The theoretical foundations scale individually, but the composition at 10,000+ agents remains an act of informed faith.
- The I-confluence cold-start problem is real. Until sufficient operations are certified M-class, the system operates at higher coordination cost than its asymptotic performance claims suggest.
- The 170x scale gap between demonstrated and aspiration-target agent counts has no existence proof.

**The competitive window.** The landscape analysis identifies an 18-24 month window before convergence from Google A2A (scheduling/verification layers), blockchain generalization (cross-ecosystem coordination), and runtime formal verification (Veil 2.0) could narrow the gap. Three reinforcing barriers deepen the moat over time: the verification membrane requires deep epistemic architecture expertise to replicate; the I-confluence proof library is a cumulative knowledge asset; and the recursive self-verification closure means each governance-approved tidal version is accumulated evidence of system correctness.

The Tidal Noosphere is ambitious by design. A feasibility score of 3/5 means "buildable but carries significant implementation risk." The architecture is honest about this risk while providing the most complete specification possible for an engineering team to begin building. Every mechanism described in this document has been designed to be testable, and the validation plan provides clear criteria for proceeding, revising, or abandoning the approach.

---

## Appendices

### Appendix A: Formal Primitives

All 25 primitives with formal type definitions.

**Structural Primitives:**

```
Definition 2.1 — Locus
Locus := {
  id:             LocusId            -- globally unique identifier
  selector:       NamespaceSelector
  invariant_set:  Set<Invariant>     -- correctness constraints
  safety_class:   {LOW, MEDIUM, HIGH, CRITICAL}
  epoch_class:    {standard, accelerated}
  parcels:        Set<ParcelId>      -- current parcel decomposition
  state:          {CREATED, ACTIVE, SPLIT, MERGED, QUIESCENT, ARCHIVED}
}

Definition 2.2 — Parcel
Parcel := {
  id:             ParcelId
  locus:          LocusId
  agents:         Set<AgentId>       -- |agents| >= PARCEL_MIN_AGENTS (default 5)
  hash_rings:     Map<TaskType, HashRing>
  slv:            ScopeLoadVector
  epoch:          uint64
  state:          {ACTIVE, TRANSITIONING, DEGRADED, DISSOLVED}
}

Definition 2.3 — Agent
Agent := {
  id:             AgentId            -- cryptographic identity
  pubkey:         ECPublicKey        -- ECVRF P-256
  privkey:        ECPrivateKey       -- local only
  capabilities:   Set<TaskType>
  capacity:       float64            -- [0.0, 1.0]
  stake:          uint64             -- AIC staked
  reputation:     float64            -- [0.0, 1.0]
  parcel:         ParcelId
  locus:          LocusId
  diversity_attr: DiversityCommitment
  governance:     bool
}

Definition 2.4 — Epoch
Epoch := {
  index:          uint64             -- monotonically increasing
  start_time:     Timestamp          -- NTP-synchronized
  duration:       Duration           -- default 3600s (TIDAL_EPOCH)
  tidal_version:  TidalVersionId
  vrf_seed:       bytes[32]
}
```

**Scheduling Primitives:**

```
Definition 2.5 — HashRing
HashRing := {
  task_type:      TaskType
  parcel:         ParcelId
  entries:        SortedArray<(uint256, AgentId)>
  virtual_nodes:  uint32             -- V per physical agent (adaptive)
  epsilon:        float64            -- bounded-loads tolerance
  agent_count:    uint32
}

Definition 2.6 — Adaptive Virtual Node Count
V(N) = clamp(ceil(1.0 / (VNODE_TARGET_VARIANCE^2 * N)), VNODE_MIN, VNODE_MAX)
with SMALL_PARCEL_OVERRIDES for N in {5..10}

Definition 2.7 — TidalFunction
TidalFunction := {
  version:        TidalVersionId
  hash_config:    HashRingConfig
  vrf_seeds:      SeedSchedule
  temporal:       TemporalConfig     -- three-tier hierarchy
  task_types:     Set<TaskType>
  economic_params: EconomicConfig
  activation_epoch: uint64
  predecessor:    TidalVersionId | null
}

Definition 2.8 — TidalVersionId
TidalVersionId = SHA256(canonical_serialize(TidalFunction))
```

**Verification Primitives:**

```
Definition 2.9 — Claim
Claim := {
  id:             ClaimId
  claim_class:    {D, E, S, H, N, P, R, C, K}  -- 9-class taxonomy
  claim_type:     {observation, derivation, synthesis, hypothesis, prediction}
  locus:          LocusId
  agent:          AgentId
  body:           AASLRef
  evidence:       List<EvidenceRef>
  hash:           bytes[32]
  epoch:          uint64
}

Definition 2.10 — Operation
Operation := {
  id:             OperationId
  op_type:        OperationType
  locus_footprint: Set<LocusId>
  class:          {M, B, X, V, G}    -- derived, not chosen
  payload:        bytes
}

Definition 2.11 — Operation Class
M  -- Merge/Convergence: CRDT-like, zero coordination, I-confluence proven
B  -- Bounded Local Commit: CSO local spend, epoch-boundary rebalancing
X  -- Exclusive: serial or Fusion Capsule
V  -- Verification: claim-class-specific membrane protocol
G  -- Governance: BFT constitutional consensus
```

**VRF and Diversity Primitives:**

```
Definition 2.12 — VRFOutput (ECVRF RFC 9381, P-256)
VRFOutput := {
  gamma:          ECPoint
  beta:           bytes[32]          -- H(point_to_string(gamma))
  pi:             bytes[80]          -- proof (c, s)
}

Definition 2.13 — DiversityCommitment
DiversityCommitment := {
  public_attrs:     PublicDiversityAttributes
  hidden_commitment: bytes[32]       -- SHA256(agent_salt || hidden_attrs)
  agent_salt:       bytes[16]
  committed_epoch:  uint64
  revealed:         bool
  cooling_until:    uint64
  change_count:     uint32
}

Definition 2.14 — DiversityAttributes
DiversityAttributes := {
  training_lineage: bytes[32]        -- public
  region:           RegionId         -- public
  methodology_hash: bytes[32]        -- hidden (hashed with epoch salt)
  temporal_bucket_hash: bytes[32]    -- hidden (hashed with epoch salt)
}

Definition 2.15 — DiversityPool
DiversityPool := {
  dimension:      DiversityDimension
  value:          DiversityValue
  members:        Set<AgentId>
  last_updated:   uint64
}

Definition 2.16 — CommitRevealRecord
CommitRevealRecord := {
  agent:              AgentId
  commitment:         DiversityCommitment
  registration_epoch: uint64
  last_change_epoch:  uint64
  change_count:       uint32
}
```

**Communication Primitives:**

```
Definition 2.17 — PredictiveModel
PredictiveModel := {
  neighbor:       AgentId
  weights:        Vector<float64>
  accuracy:       float64            -- [0.0, 1.0]
  threshold:      float64
  error_history:  CircularBuffer<float64, 10>
  mode:           {STANDARD, TRANSITIONING, PREDICTIVE}
}

Definition 2.18 — Surprise Threshold
threshold(t+1) = clamp(
  threshold(t) * (1 + THRESHOLD_ADAPT_RATE * (accuracy(t) - THRESHOLD_TARGET_ACCURACY)),
  THRESHOLD_MIN, THRESHOLD_MAX
)

Definition 2.19 — DeltaMessage
DeltaMessage := {
  source:         AgentId
  target:         AgentId
  epoch:          uint64
  error_vector:   Vector<float64>
  magnitude:      float64
  confidence:     float64
  hop_count:      uint8
}

Definition 2.20 — StigmergicSignal
StigmergicSignal := {
  id:             SignalId
  type:           {need, offer, risk, anomaly, attention_request, reservation, trend}
  scope:          LocusId
  issuer:         AgentId
  payload:        AASLRef
  confidence:     float64
  priority:       uint8
  decay_tau:      Duration
  created_at:     Timestamp
  reinforced_at:  Timestamp
  reinforcement_count: uint32
}

Definition 2.21 — Decay Function
strength(signal, t) = signal.confidence * exp(-(t - signal.reinforced_at) / signal.decay_tau)
```

**I-Confluence Primitives:**

```
Definition 2.22 — IConfluenceProof
IConfluenceProof := {
  operation_type: OperationType
  invariant_set:  Set<Invariant>
  proof_system:   {TLA_PLUS, COQ, F_STAR, IVY}
  proof_artifact: ArtifactRef
  certified_epoch: uint64
  certifier:      AgentId
  verifiers:      Set<AgentId>       -- minimum 3
  status:         {PROVISIONAL, CERTIFIED, REVOKED}
}

Definition 2.23 — ClassificationRecord
ClassificationRecord := {
  operation_type: OperationType
  current_class:  {M, B, X, V, G}
  proof:          IConfluenceProof | null
  provisional:    bool
  monitoring:     MonitoringConfig | null
  demoted_from:   {M, B, X, V, G} | null
  demotion_epoch: uint64 | null
}
```

**Settlement Primitives:**

```
Definition 2.24 — SettlementRecord
SettlementRecord := {
  agent:          AgentId
  epoch:          uint64
  streams:        SettlementStreams
  total_delta:    int64              -- AIC microtokens
  proof:          bytes[32]
}

Definition 2.25 — SettlementStreams
SettlementStreams := {
  scheduling:     int64
  verification:   int64
  communication:  int64
  governance:     int64
}
```

### Appendix B: Configurable Constants

| # | Name | Default | Range | Section |
|---|------|---------|-------|---------|
| 1 | SETTLEMENT_TICK_DURATION | 60s | [10, 300] | 4.3 |
| 2 | TICKS_PER_TIDAL_EPOCH | 60 | [10, 600] | 4.3 |
| 3 | EPOCHS_PER_CONSOLIDATION_CYCLE | 10 | [5, 100] | 4.3 |
| 4 | BOUNDARY_WINDOW | 5s | [2, 15] | 4.3 |
| 5 | CLOCK_TOLERANCE | 500ms | [100, 2000] | 4.3 |
| 6 | BOUNDED_LOADS_EPSILON | 0.15 | [0.05, 0.50] | 4.2 |
| 7 | VNODE_MIN | 50 | [20, 100] | 4.6 |
| 8 | VNODE_MAX | 500 | [200, 1000] | 4.6 |
| 9 | VNODE_TARGET_VARIANCE | 0.05 | [0.02, 0.10] | 4.6 |
| 10 | COMMITTEE_SIZE | 7 | [3, 15] | 5.2 |
| 11 | REVEAL_DELAY | 1 | [1, 5] | 5.2 |
| 12 | CHURN_BUDGET_FRACTION | 0.20 | [0.05, 0.50] | 4.5 |
| 13 | COMPLIANCE_RATE | (profile) | [0, 1] | 8 |
| 14 | VERIFICATION_RATE | (profile) | [0, 1] | 8 |
| 15 | COMM_RATE | (profile) | [0, 1] | 8 |
| 16 | GOV_RATE | (profile) | [0, 1] | 8 |
| 17 | LEARNING_RATE | 0.01 | [0.001, 0.1] | 6.2 |
| 18 | THRESHOLD_ADAPT_RATE | 0.1 | [0.01, 0.5] | 6.2 |
| 19 | THRESHOLD_TARGET_ACCURACY | 0.85 | [0.70, 0.95] | 6.2 |
| 20 | ACTIVATION_THRESHOLD | 0.70 | [0.50, 0.90] | 6.2 |
| 21 | ETR_VOTE_WINDOW | 2 | [1, 5] | 7.3 |
| 22 | ETR_SUPERMAJORITY | 0.90 | [0.80, 0.95] | 7.3 |
| 23 | OVERLAP_EPOCHS | 3 | [1, 10] | 7.2 |
| 24 | DIVERSITY_COOLING_EPOCHS | 50 | [10, 200] | 5.5 |
| 25 | WEIGHT_CAP | 0.15 | [0.05, 0.30] | 5.6 |
| 26 | GENESIS_TIME | (config) | N/A | 4.3 |
| 27 | MAX_PENDING_CLAIMS | 1000 | [100, 10000] | 5.1 |
| 28 | DIVERGENCE_THRESHOLD | 0.05 | [0.01, 0.20] | 7.3 |
| 29 | ETR_MIN_PROPOSERS | 3 | [1, 10] | 7.3 |
| 30 | GOVERNANCE_DISCUSSION_PERIOD | 72h (HIGH) | [24h, 168h] | 7.1 |
| 31 | SIGNAL_BUDGET | 50 | [10, 200] | 6.2 |
| 32 | SIGNAL_EXPIRY_THRESHOLD | 0.01 | [0.001, 0.1] | 6.3 |
| 33 | RADIUS_UNIT | 0.1 | [0.05, 0.5] | 6.2 |
| 34 | MAX_RADIUS | 3 | [1, 10] | 6.2 |
| 35 | DAMPING_FACTOR | 0.5 | [0.1, 0.9] | 6.2 |
| 36 | THRESHOLD_MIN | 0.01 | [0.001, 0.1] | 6.2 |
| 37 | THRESHOLD_MAX | 1.0 | [0.5, 5.0] | 6.2 |
| 38 | EXOGENOUS_WEIGHT | 0.01 | [0.001, 0.1] | 6.4 |
| 39 | PROVISIONAL_MIN_RUNS | 1000 | [100, 10000] | 3.4 |
| 40 | PROOF_MIN_VERIFIERS | 3 | [2, 10] | 3.3 |
| 41 | PROOF_ACK_TIMEOUT | 48h | [12h, 168h] | 3.3 |
| 42 | PTP_PREPARE_TICKS | 15 | [5, 30] | 7.10 |
| 43 | PTP_MIGRATE_TICKS | 15 | [5, 30] | 7.10 |
| 44 | PTP_STABILIZE_EPOCHS | 5 | [3, 10] | 7.10 |
| 45 | TRANSITION_ACCEPTANCE_WINDOW | 2 | [1, 5] | 6.5 |
| 46 | SLV_SURPRISE_RATIO_TARGET_LOW | 0.10 | [0.05, 0.15] | 8.1 |
| 47 | SLV_SURPRISE_RATIO_TARGET_HIGH | 0.20 | [0.15, 0.30] | 8.1 |
| 48 | MAX_ACTIVE_TYPES | 50 | [20, 100] | 9.1 |
| 49 | KNOWLEDGE_AGING_RATE | 0.02 | [0.005, 0.05] | 5.10 |
| 50 | STORM_PARCEL_THRESHOLD | 0.15 | [0.05, 0.30] | 4.9 |
| 51 | STORM_AGENT_THRESHOLD | 0.25 | [0.10, 0.50] | 4.9 |
| 52 | STORM_COOLDOWN_EPOCHS | 5 | [2, 15] | 4.9 |
| 53 | REBALANCE_TRIGGER_RATIO | 1.5 | [1.2, 2.0] | 4.7 |
| 54 | REBALANCE_VNODE_ADJUSTMENT | 0.10 | [0.05, 0.20] | 4.7 |
| 55 | REBALANCE_MAX_CONSECUTIVE | 3 | [1, 5] | 4.7 |
| 56 | REBALANCE_COOLDOWN_EPOCHS | 5 | [2, 10] | 4.7 |
| 57 | PARCEL_MIN_AGENTS | 5 | [3, 10] | 4.8 |
| 58 | PARCEL_MERGE_THRESHOLD | 6 | [MIN+1, MIN+3] | 4.8 |
| 59 | PARCEL_MERGE_COOLDOWN_EPOCHS | 10 | [5, 20] | 4.8 |
| 60 | BOUNDED_LOADS_MIN_TASKS_FOR_BALANCE | 3 | [1, 10] | 4.2 |
| 61 | CRITICAL_ETR_QUORUM | 0.67 | [0.51, 0.80] | 7.4 |
| 62 | CRITICAL_ETR_VOTE_WINDOW | 1 | [1, 3] | 7.4 |
| 63 | SCHEDULING_FAILURE_THRESHOLD | 0.50 | [0.30, 0.70] | 7.4 |
| 64 | SCHEDULING_FAILURE_EPOCHS | 3 | [2, 5] | 7.4 |
| 65 | VERIFICATION_COLLAPSE_THRESHOLD | 0.30 | [0.20, 0.50] | 7.4 |
| 66 | VERIFICATION_COLLAPSE_EPOCHS | 2 | [1, 4] | 7.4 |
| 67 | MANUAL_CRITICAL_MIN_LOCI | 3 | [2, 5] | 7.4 |
| 68 | REACHABLE_LOOKBACK_EPOCHS | 2 | [1, 5] | 7.4 |
| 69 | KNOWN_GOOD_REGISTRY_SIZE | 10 | [5, 20] | 7.6 |
| 70 | KNOWN_GOOD_QUALIFICATION_EPOCHS | 100 | [50, 500] | 7.6 |
| 71 | AUTO_ROLLBACK_FAILED_EPOCHS | 5 | [3, 10] | 7.5 |
| 72 | SECONDARY_ACTIVATION_THRESHOLD | 0.80 | [0.50, 0.90] | 7.5 |
| 73 | SECONDARY_MIN_PEERS | 3 | [2, 10] | 7.5 |
| 74 | SECONDARY_FANOUT | 5 | [3, 10] | 7.5 |
| 75 | SAFE_MODE_ETR_RETRY_INTERVAL | 10 | [5, 50] | 7.7 |
| 76 | RECOVERY_EPOCHS | 10 | [5, 20] | 7.7 |
| 77 | HIDDEN_DIMENSION_COUNT | 2 | [1, 4] | 5.3 |
| 78 | DIVERSITY_COOLING_BASE | 50 | [20, 200] | 5.5 |
| 79 | DIVERSITY_COOLING_ESCALATION | 2.0 | [1.5, 3.0] | 5.5 |
| 80 | DIVERSITY_MAX_CHANGES_PER_YEAR | 4 | [1, 12] | 5.5 |
| 81 | DIVERSITY_CHANGE_STAKE_LOCK | 0.10 | [0.05, 0.25] | 5.5 |

### Appendix C: AASL Type Definitions

| Type | Code | Fields | Direction |
|------|------|--------|-----------|
| TDF | 0x10 | version_hash, hash_ring_params, epoch_config, settlement_rules | Broadcast |
| TSK | 0x11 | task_type, task_key, epoch, assigned_agent, priority | Agent-local |
| SRP | 0x12 | source_agent, target_dimension, observed_value, predicted_value, delta | Intra-parcel |
| STL | 0x13 | epoch, agent_id, compliance_score, verification_score, comm_score, gov_score, total_aic | Broadcast |

### Appendix D: Glossary

| Term | Definition |
|------|-----------|
| AASL | Atrahasis Agent Specification Language *(predecessor vocabulary; canonical replacement is C4 ASV)* |
| AIC | Atrahasis Intelligence Coin — settlement unit |
| AVAP | Anonymous Verification with Adaptive Probing (C12) |
| BFT | Byzantine Fault Tolerance |
| CACT | Commit-Attest-Challenge-Triangulate (C11) |
| CompressedModelSummary | Max 1KB warm-start model transfer between parcels |
| CONSOLIDATION_CYCLE | 36,000s (10 TIDAL_EPOCHs) — long-horizon knowledge consolidation |
| Critical ETR | Emergency rollback at 67% of reachable agents |
| CSO | Certified Slice Object — local budget for B-class operations |
| DSF | Deterministic Settlement Fabric (C8) |
| ECVRF | Elliptic Curve VRF per RFC 9381 |
| EMA | Epistemic Metabolism Architecture (C6) |
| ETR | Emergency Tidal Rollback |
| I-confluence | Formal criterion for coordination-free execution (Bailis 2015) |
| K-class | Knowledge-consolidation claim class |
| Known-Good Registry | Deterministic registry of proven tidal function versions |
| Locus | Stable logical coordination domain |
| MCT | Membrane Certification Token |
| MQI | Membrane Quality Index |
| Parcel | Elastic physical execution unit within a locus |
| PCVM | Proof-Carrying Verification Membrane (C5) |
| PTP | Parcel Transition Protocol (2-phase + convergence) |
| RIF | Recursive Intent Fabric (C7) |
| SAFE_MODE | Constitutionally recognized exception state — correctness only |
| Sentinel Graph | Anomaly detection via verification affinity matrix |
| SETTLEMENT_TICK | 60s — atomic temporal unit |
| SLV | Scope Load Vector — per-parcel multi-dimensional load metric |
| Standard ETR | Emergency rollback at 90% supermajority |
| Tertiary Rollback | Autonomous, no-communication rollback after sustained failure |
| TIDAL_EPOCH | 3,600s (60 SETTLEMENT_TICKs) — primary coordination cycle |
| VRF | Verifiable Random Function |
| VTD | Verification Trace Document |

### Appendix E: Cross-Layer Integration Contracts

Per C9 cross-layer reconciliation, the following integration contracts bind C3 to other system components:

| Contract | C3 Provides | Partner Provides | Invariant |
|----------|------------|-----------------|-----------|
| C3-C5 | VRF committee selection, 9-class claim routing | PCVM opinion fusion, MCT issuance | Committee size >= COMMITTEE_SIZE; diversity enforced |
| C3-C6 | CONSOLIDATION_CYCLE timing for K-class | EMA lifecycle events | K-class processed at cycle boundary |
| C3-C7 | Task scheduling via hash rings | RIF intent decomposition | Intent tasks routed through tidal scheduler |
| C3-C8 | Settlement computation | DSF ledger operations | Settlement deterministic (INV-2) |
| C3-C9 | Three-tier temporal hierarchy | Cross-layer type registry | Canonical claim classes (9), temporal units aligned |
| C3-C10 | Sentinel Graph edges from VRF anomalies | Layer 1-4 defense | Sentinel exclusion enforced in committee selection |
| C3-C11 | VTD routing through tidal scheduler | CACT forgery defense | VTD integrity preserved through scheduling |
| C3-C12 | VRF engine, diversity pools, Sentinel exclusion | AVAP anonymous committees, sealed opinions | Committee-to-pool ratio <= MAX_COMMITTEE_TO_POOL_RATIO |

### Appendix F: Attack Trees (Post-Hardening)

```
GOAL: >50% committee control through diversity grinding

  AND-1: Register Sybils with optimized attributes
    +-- Optimize public dimensions (2 of 4): partial effectiveness
    +-- Optimize hidden dimensions (2 of 4): IMPOSSIBLE (epoch salt unknown)

  AND-2: Survive cooling period
    +-- 50 epochs minimum (escalating to 400)
    +-- 10% stake locked during cooling
    +-- Ineligible for verification during cooling

  AND-3: Avoid detection
    +-- Sentinel Graph: ~20 epoch detection window
    +-- Consequence: 100% stake slash

  RESULT: Cost/gain ratio > 3,500x. Attack deeply unprofitable.
```

### Appendix G: Load Imbalance Bounds (Post-Hardening)

```
WITHOUT HARDENING (standard consistent hashing, V=150):
  N=5:   expected max/avg = 3.1x  (unacceptable)
  N=10:  expected max/avg = 2.3x  (unacceptable)

WITH BOUNDED-LOADS ONLY (epsilon=0.15, V=150):
  All N >= 5: guaranteed max/avg <= 1.15x
  But: requires sufficient task volume

WITH FULL HARDENING (bounded-loads + adaptive vnodes + rebalancing):
  N=5:   V=400, expected max/avg = 1.10x, rebalance if >1.5x
  N=10:  V=200, expected max/avg = 1.07x, rebalance if >1.5x
  N=50:  V=50,  expected max/avg = 1.03x, rebalance if >1.5x

  Epoch-boundary rebalance converges within 1-3 epochs.
  Parcel merge activates if N drops below 5.
  Ring size held constant at ~2,000 entries (O(0.1ms) rebuild).
```

### Appendix H: Test Vectors

**Test Vector 1: Hash Ring Position**
```
Input:
  agent_id = bytes("agent_001")
  task_type = bytes("task.verify")
  vnode_index = uint32(0)

Expected:
  position = SHA256("agent_001" || "task.verify" || 0x00000000) mod 2^256
```

**Test Vector 2: VRF Output**
```
Input:
  privkey = <test ECVRF P-256 private key per RFC 9381>
  alpha = SHA256(claim_hash || epoch_bytes || vrf_seed)

Expected:
  Per RFC 9381 Section 5.1, ECVRF-P256-SHA256-TAI
  Implementors: verify against RFC 9381 test vectors
```

**Test Vector 3: Bounded-Loads Assignment**
```
Input:
  5 agents, adaptive vnodes (V=400), epsilon = 0.15
  100 random task keys

Expected:
  max_load / avg_load <= 1.15
  avg_load = 20 (100 keys / 5 agents)
  max_load <= ceil(1.15 * 20) = 23
```

**Test Vector 4: Diversity Commitment (Hardened)**
```
Input:
  agent_salt = 0x0123456789abcdef0123456789abcdef
  training_lineage = SHA256("openai_gpt4_2024")
  region = "us_east"
  methodology = "replication"       // hidden dimension
  temporal_bucket = "stable_6mo_plus"  // hidden dimension

Expected:
  public commitment (training_lineage, region) revealed after REVEAL_DELAY
  hidden commitment = SHA256(agent_salt || methodology || temporal_bucket)
  hidden diversity score = SHA256(epoch_salt || hidden_commitment || agent_salt)
  epoch_salt = SHA256(vrf_seed || uint64_be(epoch) || b"hidden_diversity")
```

**Test Vector 5: Signal Decay**
```
Input:
  confidence = 0.85
  reinforced_at = 0 (epoch start)
  decay_tau = 3600 (seconds)
  t = 1800 (30 minutes after reinforcement)

Expected:
  strength = 0.85 * exp(-1800/3600) = 0.85 * 0.6065... = 0.5155...
```

**Test Vector 6: Adaptive Threshold**
```
Input:
  threshold(t) = 0.20
  accuracy(t) = 0.90
  THRESHOLD_ADAPT_RATE = 0.1
  THRESHOLD_TARGET_ACCURACY = 0.85

Expected:
  threshold(t+1) = 0.20 * (1 + 0.1 * (0.90 - 0.85))
                 = 0.20 * 1.005
                 = 0.201
  (Threshold tightens because accuracy exceeds target)
```

### Appendix I: Architectural Decisions Register

| Decision | Status | Summary |
|----------|--------|---------|
| ARCH-C3-001 | ACCEPTED | Noosphere as primary architecture. PTA becomes scheduling substrate. Locus Fabric provides proof discipline. |
| ARCH-C3-002 | ACCEPTED (pending GATE-2) | Bounded-loads consistent hashing (Mirrokni et al., SODA 2018) with adaptive virtual nodes targeting ~2,000 ring entries. |
| ARCH-C3-003 | ACCEPTED | VRF dual defense: commit-reveal + pre-stratified diversity pools + hidden dimensions + randomized thresholds. Adversary advantage <3%. |
| ARCH-C3-004 | ACCEPTED (pending GATE-3) | Two-tier ETR: Standard (90% supermajority) + Critical (67% of reachable). Three-channel governance. |
| ARCH-C3-005 | ACCEPTED | Primary scale target 1K-10K. 100K retained as Phase 4 aspiration. |
| ARCH-C3-006 | ACCEPTED | Provisional M-class for operations with empirical evidence but no formal proof. |
| ARCH-C3-007 | ACCEPTED | PTA Layer 3 (morphogenic fields) discarded. Cell assembly handles sub-epoch adaptation. |
| ARCH-C3-008 | ACCEPTED | Three-channel governance redundancy with tertiary autonomous rollback. |
| ARCH-C3-009 | ACCEPTED | Trend signals added to stigmergic layer for gradient-based awareness. |
| ARCH-C3-010 | ACCEPTED | Surprise rate as 7th SLV dimension. Joint threshold calibration via SLV_SURPRISE_RATIO. |
| ARCH-C3-011 | ACCEPTED | Nine-class claim taxonomy (D/E/S/H/N/P/R/C/K) per C9 cross-layer reconciliation. |
| ARCH-C3-012 | ACCEPTED | Three-tier temporal hierarchy: SETTLEMENT_TICK/TIDAL_EPOCH/CONSOLIDATION_CYCLE. |
| ARCH-C3-013 | ACCEPTED | Storm detection with graduated circuit breaker and staggered 4-phase reconfiguration. |
| ARCH-C3-014 | ACCEPTED | SAFE_MODE state machine with progressive recovery. No time-based exit. |
| ARCH-C3-015 | ACCEPTED | AVAP integration via encrypted VRF assignment tokens and cover traffic. |

### Appendix J: Open Design Questions

**ODQ-1: Epsilon Tuning for Bounded-Loads Hash Rings**
- *Phase:* 1 (resolved by GATE-2 results)
- *Question:* What is the optimal epsilon value per parcel size class? The specification assumes epsilon=0.15, but this is an estimate from theoretical analysis, not empirical measurement under Tidal Noosphere workloads.
- *Resolution path:* GATE-2 sweep across N=3..50, V=50..500, epsilon=0.05..0.30 with 4 workload distributions.

**ODQ-2: Governance Channel Infrastructure Protocol**
- *Phase:* 1 (design), Phase 2 (implementation)
- *Question:* The dedicated governance channel is specified as a "persistent mesh," but the exact protocol — pure gossip, structured overlay (Chord/Kademlia), or relay-based — is not determined.
- *Resolution path:* Phase 1 prototype with pure gossip. Evaluate structured overlay if ETR vote collection exceeds 1 epoch at 1K governance agents.

**ODQ-3: SRP vs. SIG Type Consolidation**
- *Phase:* Post-Phase 1 review
- *Question:* Should SRP be consolidated into SIG? Depends on parsing overhead measurements.
- *Resolution path:* If SRP parsing overhead is <5% of total message processing time, consolidate.

**ODQ-4: M-prov Monitoring Latency**
- *Phase:* 2
- *Question:* Is epoch-boundary monitoring sufficient for M-prov violations, or does intra-epoch sampling need to be added?
- *Resolution path:* Categorize M-prov operations by update frequency. For high-frequency operations, implement intra-epoch sampling.

**ODQ-5: Hierarchical Snapshot Aggregation Protocol**
- *Phase:* 3 (required for 1K-10K agents)
- *Question:* Flat gossip produces O(N log N) messages. At N=10K, this is ~170K messages potentially exceeding the boundary window. The hierarchical aggregation protocol is not yet specified.
- *Resolution path:* Design during Phase 2. Validate convergence at simulated 10K scale.

**ODQ-6: Cross-Region Federation Protocol**
- *Phase:* 4 (research aspiration)
- *Question:* Hash rings are defined per-parcel; cross-region operations require interoperability across WAN boundaries with different latency.
- *Resolution path:* Deferred to Phase 4. Potential approaches: region-local epochs with cross-region sync at coarser granularity.

**ODQ-7: Tidal Function Definition Complexity Bounds**
- *Phase:* 2 (validation)
- *Question:* TDF expressiveness must balance encoding real scheduling policies against verifiability.
- *Resolution path:* Enumerate Phase 2 policies, verify TDF can express them. Restrict to decidable subset if needed.

### Appendix K: Traceability Matrix

**Assessment Council Conditions:**

| Condition | ID | Resolution | Spec Section |
|-----------|----|-----------|--------------|
| Reconfiguration Storm Simulation | GATE-1 | Experiment designed, kill criteria defined | 7.11, 12.1 |
| Bounded-Loads Hash Ring Validation | GATE-2 | Experiment designed, 4 distributions | 4.2, 12.1 |
| ETR Feasibility | GATE-3 | Mechanism + experiment with 6 scenarios | 7.3, 7.4, 12.1 |
| I-Confluence Bootstrap Plan | REQ-1 | 15 operations, expansion strategy, M-prov | 3.4 |
| Scale Target Reframing | REQ-2 | 1K-10K primary, 100K Phase 4 | 1.5, 11 |
| Cross-Integration Failure Spec | REQ-3 | 6 combinations with recovery bounds | 7.10, 10.2 |
| VRF Bias Quantification | REC-1 | Hardened dual defense design, <3% bound | 5.2-5.6 |

**Adversarial Findings:**

| Attack | Severity | Resolution | Spec Section |
|--------|----------|-----------|--------------|
| 1: Reconfiguration Storm | CRITICAL | PTP + staggering + circuit breaker + storm detection | 4.9, 4.10, 7.11 |
| 2: Small-Ring Load Imbalance | HIGH | Bounded-loads + adaptive vnodes + rebalancing | 4.2, 4.6, 4.7 |
| 3: VRF Diversity Grinding | HIGH | Hidden dims + randomized thresholds + cooling | 5.3, 5.4, 5.5, 5.6 |
| 4: Committee Shopping | HIGH | Claim commitment, 1-epoch delay | 5.2.2 |
| 5: Governance Deadlock | CRITICAL | Two-tier ETR + three-channel redundancy | 7.3, 7.4, 7.5 |
| 6: 170x Scale Gap | HIGH | Scale target reframing | 1.5, 11 |
| 7: I-Confluence Cold Start | MEDIUM | Bootstrap + M-prov | 3.4 |
| 8: CAP Tension | LOW | Operation-class algebra | 3.3 |
| 9: FLP Impossibility | LOW | Deterministic scheduling | 4.1 |
| 10: Boundary Info Loss | MEDIUM | Trend signals + promotion | 6.4 |
| 11: Threshold Calibration | MEDIUM | 7th SLV dimension + coupling | 6.4, 8.1 |
| 12: Governance Cost | LOW | ETR bypass | 7.3, 7.4 |
| 13: Epoch Sync | LOW | NTP tolerance | 4.3 |
| 14: Bootstrap Circularity | LOW | Genesis asserted parameter | 7.2 |

---

## References

1. Bailis, P., Fekete, A., Franklin, M.J., Ghodsi, A., Hellerstein, J.M., and Stoica, I. "Coordination Avoidance in Database Systems." *Proceedings of the VLDB Endowment*, 8(3):185-196, 2015.
2. Karger, D., Lehman, E., Leighton, T., Panigrahy, R., Levine, M., and Lewin, D. "Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web." *Proceedings of the 29th Annual ACM Symposium on Theory of Computing*, pp. 654-663, 1997.
3. Mirrokni, V., Thorup, M., and Wieder, U. "Consistent Hashing with Bounded Loads." *Proceedings of the 29th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA)*, pp. 587-604, 2018.
4. RFC 9381: Verifiable Random Functions (VRFs). IETF, 2023.
5. DeCandia, G., Hastorun, D., Jampani, M., et al. "Dynamo: Amazon's Highly Available Key-value Store." *SOSP '07*, pp. 205-220, 2007.
6. Gilad, Y., Hemo, R., Micali, S., Vlachos, G., and Zeldovich, N. "Algorand: Scaling Byzantine Agreements for Cryptocurrencies." *SOSP '17*, pp. 51-68, 2017.
7. Li, J., Zhang, Q., et al. "MegaAgent: Scaling LLM-Based Multi-Agent Systems to 590 Autonomous Agents." *ACL 2025*.
8. Li, G., et al. "CAMEL OASIS: A Simulated Social Environment with One Million Agents." *arXiv preprint*, 2024.
9. Shapiro, M., Preguica, N., Baquero, C., and Zawirski, M. "Conflict-free Replicated Data Types." *SSS 2011*, pp. 386-400.
10. ISEK Collective. "Toward a Planetary Intelligence Substrate." *arXiv:2506.09335*, 2025.

---

## Changelog: v1.0 to v2.0

### Structural Changes
- **Temporal terminology:** Replaced "epoch" as primary term with three-tier hierarchy: SETTLEMENT_TICK (60s), TIDAL_EPOCH (3600s), CONSOLIDATION_CYCLE (36000s). Per C9 cross-layer reconciliation.
- **Claim taxonomy:** Expanded from 5 classes (D/E/S/H/N) to 9 classes (D/E/S/H/N/P/R/C/K) organized in 3 tiers. Per C9 errata E-C3-01.
- **Verification pathways:** Added P-class (Predictive), R-class (Replicative), C-class (Causal), K-class (Knowledge-consolidation) verification pathways. Per C9 errata E-C3-02.
- **Section restructuring:** Sections 4, 5, 7 significantly expanded. New subsections for hardening content.

### New Content (from Patch Addendum v1.1)
- **Section 5.7:** VRF phased deployment (SIMPLE/COMMITTED/FULL_DUAL_DEFENSE). From PA-F4.
- **Section 7.10:** PTP restructured as 2-phase + convergence (PREPARE/MIGRATE + STABILIZE). From PA-F5.
- **Section 14.1:** Deployment profiles T1/T2/T3 with 20 critical parameters. From PA-F6.
- **Section 6.5:** In-flight signal routing during transitions. From PA-F15.
- **Section 8.1:** Threshold calibration coupling (SLV_SURPRISE_RATIO). From PA-F16.
- **Section 9.1:** AASL type retirement mechanism (MAX_ACTIVE_TYPES=50). From PA-F18.

### New Content (from C10 Hardening — Reconfiguration Storm)
- **Section 4.9:** Storm detection with graduated circuit breaker (NORMAL/THROTTLED/DRAIN_ONLY/HALT_ALL).
- **Section 4.10:** Staggered 4-phase reconfiguration (PHASE_A_RINGS through PHASE_D_NORMAL).
- **Section 5.8:** VRF cache invalidation on reconfiguration.
- **Section 6.6:** CompressedModelSummary for warm-start model migration (max 1KB).
- **Section 7.8:** Governance quorum freezing during reconfiguration.
- **Section 7.9:** Degradation priority ordering (communication first, governance last).

### New Content (from C10 Hardening — VRF Grinding & Small-Ring)
- **Section 5.3:** Hidden diversity attributes (2 public + 2 hashed dimensions).
- **Section 5.4:** Randomized filter thresholds within governance-approved ranges.
- **Section 5.5:** Diversity attribute commitment with escalating cooling periods.
- **Section 5.6:** Hardened end-to-end VRF committee selection integrating all defenses.
- **Section 4.6:** Adaptive virtual nodes (targeting ~2,000 ring entries).
- **Section 4.7:** Epoch-boundary load rebalancing.
- **Section 4.8:** Minimum parcel size (5) with merge protocol.
- **Section 10.4:** Sybil cost analysis (attack unprofitable by 3,500x).
- **Appendix F:** Attack tree for diversity grinding (post-hardening).
- **Appendix G:** Load imbalance bounds (post-hardening).

### New Content (from C10 Hardening — Emergency Rollback)
- **Section 7.4:** Critical ETR (67% of reachable agents, 1-epoch window).
- **Section 7.5:** Three-channel governance redundancy (primary/secondary/tertiary).
- **Section 7.6:** Known-Good Version Registry with qualification logic.
- **Section 7.7:** SAFE_MODE state machine (5 states: NORMAL/STANDARD_ETR/CRITICAL_ETR/SAFE_MODE/RECOVERY).
- **GATE-3B/3C/3D:** Extended ETR validation experiments.

### New Content (from C12 AVAP Integration)
- **Section 5.11:** AVAP integration points (anonymous committee selection, encrypted VRF assignment tokens, cover traffic, Sentinel Graph exclusion, diversity pool inheritance).

### Superseded Content
- **Old "epoch" as unqualified term:** Replaced by TIDAL_EPOCH throughout.
- **Old 5-class claim taxonomy:** Replaced by 9-class taxonomy.
- **Old fixed virtual node formula (V=max(150, 1000/N)):** Replaced by adaptive formula targeting ~2,000 ring entries.
- **Old PTP 3-phase (PREPARE/SWITCH/STABILIZE):** Replaced by 2-phase + convergence (PREPARE/MIGRATE + STABILIZE) with staggered 4-phase execution.
- **Old single-tier ETR:** Replaced by two-tier (Standard + Critical) with three-channel redundancy.
- **Old single governance channel:** Replaced by three-channel failover architecture.

### Constants
- Constants #1-#41 from v1.0 retained (some renumbered for clarity).
- Constants #42-#49 added from Patch Addendum v1.1.
- Constants #50-#60 added from C10 Hardening (Reconfiguration Storm + Small-Ring).
- Constants #61-#76 added from C10 Hardening (Emergency Rollback).
- Constants #77-#81 added from C10 Hardening (VRF Grinding).

### Conformance Requirements
- MUST requirements expanded from 15 to 29.
- SHOULD requirements expanded from 7 to 10.
- New hardening experiments EXP-8 through EXP-10, EXP-H1 through EXP-H4.

---

*End of Tidal Noosphere Master Technical Specification*
*C3-A v2.0 — Unified Rewrite*
*Atrahasis Agent System*
*SPECIFICATION stage: COMPLETE*
