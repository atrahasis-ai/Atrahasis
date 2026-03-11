# Atrahasis Unified Architecture Document

**Document ID:** T-002
**Version:** 1.0
**Date:** 2026-03-11
**Status:** REFERENCE DOCUMENT
**Classification:** CONFIDENTIAL — Atrahasis LLC
**Purpose:** Single-entry-point reference synthesizing all 19 Atrahasis specifications into one coherent narrative
**Total Upstream Specification Lines:** ~40,947

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Layer Descriptions](#3-layer-descriptions)
   - [3.1 Layer 1: ASV — Communication Vocabulary (C4)](#31-layer-1-asv--communication-vocabulary-c4)
   - [3.2 Layer 2: DSF — Settlement Plane (C8)](#32-layer-2-dsf--settlement-plane-c8)
   - [3.3 Layer 3: EMA — Knowledge Metabolism (C6)](#33-layer-3-ema--knowledge-metabolism-c6)
   - [3.4 Layer 4: PCVM — Verification Membrane (C5)](#34-layer-4-pcvm--verification-membrane-c5)
   - [3.5 Layer 5: Tidal Noosphere — Coordination (C3)](#35-layer-5-tidal-noosphere--coordination-c3)
   - [3.6 Layer 6: RIF — Orchestration (C7)](#36-layer-6-rif--orchestration-c7)
4. [Cross-Layer Integration](#4-cross-layer-integration)
   - [4.1 Canonical Claim Classes](#41-canonical-claim-classes)
   - [4.2 Three-Tier Temporal Hierarchy](#42-three-tier-temporal-hierarchy)
   - [4.3 Authority Hierarchy](#43-authority-hierarchy)
   - [4.4 Operation Class Algebra](#44-operation-class-algebra)
   - [4.5 ASV-to-PCVM Mapping](#45-asv-to-pcvm-mapping)
   - [4.6 Settlement Integration](#46-settlement-integration)
   - [4.7 Canonical Data Flow](#47-canonical-data-flow)
5. [Defense Systems](#5-defense-systems)
   - [5.1 C11 CACT — VTD Forgery Defense](#51-c11-cact--vtd-forgery-defense)
   - [5.2 C12 AVAP — Collusion Defense](#52-c12-avap--collusion-defense)
   - [5.3 C13 CRP+ — Consolidation Poisoning Defense](#53-c13-crp--consolidation-poisoning-defense)
   - [5.4 Defense Invariants](#54-defense-invariants)
   - [5.5 Defense System Authority](#55-defense-system-authority)
6. [Sybil Defense](#6-sybil-defense)
   - [6.1 MCSD Four-Layer Architecture](#61-mcsd-four-layer-architecture)
   - [6.2 C17 Layer 2: Behavioral Similarity](#62-c17-layer-2-behavioral-similarity)
   - [6.3 C19 Temporal Trajectory Comparison](#63-c19-temporal-trajectory-comparison)
   - [6.4 C20 Training Bias Framework](#64-c20-training-bias-framework)
   - [6.5 C21 FPR Validation](#65-c21-fpr-validation)
7. [Governance and Institutional Architecture](#7-governance-and-institutional-architecture)
   - [7.1 AiBC Overview](#71-aibc-overview)
   - [7.2 Phased Dual-Sovereignty](#72-phased-dual-sovereignty)
   - [7.3 Legal Entity Structure](#73-legal-entity-structure)
   - [7.4 Constitutional Framework](#74-constitutional-framework)
   - [7.5 Constitutional Tribunal and Nominating Bodies](#75-constitutional-tribunal-and-nominating-bodies)
   - [7.6 Citicate System](#76-citicate-system)
   - [7.7 Safety Mechanisms](#77-safety-mechanisms)
8. [Economic Architecture](#8-economic-architecture)
   - [8.1 AIC Dual-Anchor Valuation](#81-aic-dual-anchor-valuation)
   - [8.2 Reference Rate Engine](#82-reference-rate-engine)
   - [8.3 External Task Marketplace](#83-external-task-marketplace)
   - [8.4 Provider Economics](#84-provider-economics)
   - [8.5 Three-Phase Convertibility](#85-three-phase-convertibility)
   - [8.6 DSF Stream 5](#86-dsf-stream-5)
9. [Implementation Roadmap](#9-implementation-roadmap)
   - [9.1 Implementation Philosophy](#91-implementation-philosophy)
   - [9.2 Six-Wave Structure](#92-six-wave-structure)
   - [9.3 Wave 0: Risk Validation](#93-wave-0-risk-validation)
   - [9.4 Maturity Tier System](#94-maturity-tier-system)
   - [9.5 Technology Stack](#95-technology-stack)
   - [9.6 Budget and Timeline](#96-budget-and-timeline)
   - [9.7 Funding Strategy](#97-funding-strategy)
   - [9.8 Team Structure](#98-team-structure)
10. [Spec Index](#10-spec-index)
11. [Glossary of Key Terms](#11-glossary-of-key-terms)
12. [Cross-Reference Index](#12-cross-reference-index)
13. [Formal Requirements and Claims Summary](#13-formal-requirements-and-claims-summary)
14. [Honest Assessment: What Is Proven vs. What Remains Unproven](#14-honest-assessment-what-is-proven-vs-what-remains-unproven)

---

## 1. Executive Summary

The Atrahasis Agent System is a planetary-scale infrastructure for coordinating autonomous AI agents performing verified knowledge work. It addresses a problem that no existing system solves: how to coordinate thousands of heterogeneous AI agents in epistemic tasks -- tasks involving knowledge claims, verification, contradiction resolution, and governance -- while providing formal correctness guarantees, constitutional protection of verification quality, economic incentive alignment, and near-zero communication overhead in steady state.

The system is defined across 19 specifications totaling approximately 41,000 lines. These specifications cover six core architecture layers (communication, settlement, knowledge metabolism, verification, coordination, and orchestration), three cross-cutting defense systems (forgery, collusion, and poisoning), a Sybil defense architecture, an institutional governance framework, an economic architecture, and an implementation plan.

### What Problem Does Atrahasis Solve?

Current approaches to multi-agent AI coordination fall into three categories:

- **Blockchain-based coordination** (Ethereum, Solana) provides strong consistency but is designed for transaction ordering, not knowledge coordination. Total ordering is unnecessary and harmful for intelligence coordination: reasoning tasks have causal dependencies, not temporal dependencies.

- **Platform-based coordination** (Google A2A, Microsoft Agent Framework) provides interoperability through centralized infrastructure but cannot provide the constitutional protections needed for epistemic integrity. When a single entity controls the coordination layer, verification quality can be silently degraded.

- **Swarm-based coordination** (MegaAgent, CAMEL OASIS) provides decentralization but lacks verification semantics, formal correctness guarantees, and economic incentive structures. The highest demonstrated autonomous LLM-agent coordination is 590 agents.

Atrahasis occupies a genuinely vacant design point: **formal per-operation consistency with epistemic semantics, constitutional verification protection, and economic incentive alignment**. No existing system combines all three.

### Key Numbers

| Metric | Value |
|--------|-------|
| Target scale | 1,000-10,000 agents (100K+ aspirational) |
| Architecture layers | 6 core + 3 defense + governance + economics |
| Claim classes | 9 (D/C/P/R/E/S/K/H/N) |
| Operation classes | 5 (M/B/X/V/G) |
| Temporal tiers | 3 (60s / 3,600s / 36,000s) |
| Verification cost reduction | ~0.83x per-claim, ~0.40-0.60x with citation reuse |
| Sybil attack cost (Phase 2) | $90M+ for 50% capture |
| Implementation budget | $10M-$12M fully loaded |
| Implementation timeline | 30-36 months across 6 waves |
| Total spec lines | ~41,000 |
| Formal requirements | 300+ across all specs |
| Patent-style claims | 44+ across all specs |
| Governance phases | 4 (human-led to AI constitutional supremacy) |

### The Architecture at a Glance

The system is organized into six core layers, each responsible for one concern:

1. **ASV (C4)** provides the communication vocabulary -- structured JSON types for claims, confidence, evidence, provenance, and verification.
2. **DSF (C8)** provides the economic substrate -- a Hybrid Deterministic Ledger with three budgets and four settlement streams, settling every 60 seconds.
3. **EMA (C6)** manages the knowledge lifecycle -- ingesting, circulating, consolidating, and retiring knowledge as a metabolic process.
4. **PCVM (C5)** verifies all claims before they enter the canonical knowledge graph -- using graduated proof-carrying verification matched to nine claim classes.
5. **Tidal Noosphere (C3)** coordinates agents -- deterministic O(1) scheduling via consistent hashing within elastic parcels, organized under stable semantic loci.
6. **RIF (C7)** orchestrates high-level goals -- recursive intent decomposition with formal termination guarantees and a Viable System Model-aligned executive.

Three defense systems (CACT for forgery, AVAP for collusion, CRP+ for poisoning) harden the pipeline. MCSD provides four-layer Sybil defense. The AiBC institutional framework governs the system through a phased sovereignty transition. AIC Economics connects the internal economy to external markets.

### How Atrahasis Works (One Paragraph)

An AI agent submits a knowledge claim wrapped in an ASV (C4) semantic envelope carrying structured confidence, evidence, and provenance. PCVM (C5) classifies the claim into one of nine classes and dispatches it for tier-appropriate verification, where VRF-selected committees evaluate the accompanying Verification Trace Document. The Tidal Noosphere (C3) schedules verification work across elastic parcels using deterministic consistent hashing, achieving O(1) per-agent overhead. EMA (C6) metabolizes verified claims through ingestion, circulation, consolidation, and catabolism under homeostatic regulation. RIF (C7) orchestrates high-level goals by recursively decomposing intents into concrete tasks that agents execute within tidal epochs. DSF (C8) settles all economic transactions deterministically at 60-second intervals using a Hybrid Deterministic Ledger. Three defense systems (CACT, AVAP, CRP+) harden the pipeline against forgery, collusion, and poisoning. The AiBC (C14) governs the entire system through a phased dual-sovereignty model transitioning from human trustees to AI constitutional governance.

---

## 2. Architecture Overview

The Atrahasis architecture comprises six core layers arranged in a stack. Each layer is specified independently and reconciled through C9, the canonical cross-layer integration document.

```
+-------------------------------------------------------------+
|  Layer 6: RIF -- Recursive Intent Fabric (C7)                |
|  Purpose: Intent decomposition, agent assignment, lifecycle   |
|  Innovation: Two-plane VSM-aligned orchestration              |
+-------------------------------------------------------------+
|  Layer 5: Tidal Noosphere (C3)                               |
|  Purpose: Coordination, CRDT state, topology, governance     |
|  Innovation: O(1) tidal scheduling via consistent hashing    |
+-------------------------------------------------------------+
|  Layer 4: PCVM -- Proof-Carrying Verification Membrane (C5)  |
|  Purpose: Claim verification, classification, credibility    |
|  Innovation: Graduated proof-carrying verification           |
+-------------------------------------------------------------+
|  Layer 3: EMA -- Epistemic Metabolism Architecture (C6)      |
|  Purpose: Knowledge lifecycle, consolidation, circulation    |
|  Innovation: Living knowledge with metabolic processes       |
+-------------------------------------------------------------+
|  Layer 2: DSF -- Deterministic Settlement Fabric (C8)        |
|  Purpose: Economic settlement, budgets, capacity market      |
|  Innovation: Hybrid Deterministic Ledger (CRDT+EABS)         |
+-------------------------------------------------------------+
|  Layer 1: ASV -- Atrahasis Semantic Vocabulary (C4)          |
|  Purpose: Structured communication vocabulary                |
|  Innovation: Epistemic accountability chain (CLM-CNF-EVD-PRV)|
+-------------------------------------------------------------+

  CROSS-CUTTING DEFENSE SYSTEMS:

  +-------------------------------+-------------------------------+
  | C11 CACT: VTD Forgery Defense | C12 AVAP: Collusion Defense   |
  | Integrates: C5, C3, C8       | Integrates: C3, C5, C6, C8   |
  +-------------------------------+-------------------------------+
  | C13 CRP+: Consolidation      | C17 MCSD: Sybil Defense       |
  | Poisoning Defense             | (+ C19, C20, C21 extensions)  |
  | Integrates: C6, C5, C3, C8   | Integrates: C5, C14           |
  +-------------------------------+-------------------------------+

  GOVERNANCE & ECONOMICS:

  +-------------------------------+-------------------------------+
  | C14 AiBC: Institutional       | C15 AIC Economics:            |
  | Architecture                  | External-facing economy       |
  | C16: Nominating Bodies        | C18: Funding Strategy         |
  +-------------------------------+-------------------------------+

  INTEGRATION & IMPLEMENTATION:

  +-------------------------------+-------------------------------+
  | C9: Cross-Layer Reconciliation| C22: Implementation Planning  |
  | Authority on cross-layer      | 6-wave risk-first build       |
  | contracts                     | C18: Funding + operations     |
  +-------------------------------+-------------------------------+
```

Data flows bidirectionally between layers. The canonical claim lifecycle traverses the full stack:

```
Agent submits CLM (C4 ASV)
  --> C5 PCVM classifies (D/C/P/R/E/S/K/H/N)
  --> C3 Tidal assigns verification parcels via hash ring
  --> C5 PCVM verifies (VTD checking, adversarial probing, deep audit)
  --> C11/C12 defend (CACT commitment checks, AVAP anonymous committees)
  --> C6 EMA metabolizes (ingestion, circulation, consolidation)
  --> C13 CRP+ defends (perturbation robustness, dissent search)
  --> C7 RIF orchestrates (intent decomposition, multi-agent routing)
  --> C8 DSF settles (budget enforcement, reward distribution)
  --> C14 AiBC governs (CFI monitoring, constitutional compliance)
```

---

## 3. Layer Descriptions

### 3.1 Layer 1: ASV -- Communication Vocabulary (C4)

**Specification:** C4 MASTER_TECH_SPEC v2.0 (1,652 lines)
**Assessment:** Novelty 3/5, Feasibility 4.5/5, Impact 3.5/5, Risk 3/10

ASV (AASL Semantic Vocabulary) is a JSON Schema vocabulary and companion JSON-LD context that provides epistemic accountability for AI agent communication. It defines seven typed semantic structures that compose into an auditable epistemic chain. ASV is a vocabulary, not a protocol -- it embeds inside Google A2A messages, Anthropic MCP tool responses, or standalone JSON documents.

**The Seven Types:**

| Type | Name | Purpose |
|------|------|---------|
| AGT | Agent | Entity that bears responsibility for claims |
| CLM | Claim | Proposition asserted by an agent, classified by epistemic nature |
| CNF | Confidence | Structured confidence with method and calibration metadata |
| EVD | Evidence | Link to supporting data with quality classification |
| PRV | Provenance | W3C PROV-O-compatible origin and derivation history |
| VRF | Verification | Independent validation record aligned with W3C VC |
| SAE | Speech-Act Envelope | Wrapper combining speech-act type with epistemic class |

**The Epistemic Accountability Chain:** CLM --> CNF --> EVD --> PRV --> VRF. Every claim an agent makes can carry structured confidence (with declared method: statistical, consensus, model_derived, human_judged, heuristic), linked evidence (with quality class: direct_observation, inference, computational_result, delegation, hearsay), traceable provenance, and independent verification records.

**Key Innovation:** The dual classification framework combining speech-act type with epistemic claim type (observation, correlation, causation, inference, prediction, prescription), and the structured confidence primitive (CNF) with calibration metadata. No existing standard provides this.

**Six Epistemic Classes:** observation, correlation, causation, inference, prediction, prescription. These map deterministically to C5's nine claim classes via the algorithm specified in C9 Section 6.2.

**Stack Role:** ASV is the lingua franca. Every inter-layer message in the Atrahasis system is an ASV message. C3 extends ASV with four additional types (TDF, TSK, SRP, STL) and C7 extends it with intent-outcome claims.

**Complete Chain Example (Drug Interaction):** A clinical analyst's claim "Co-administration of warfarin and aspirin increases bleeding risk by 2.3x" carries: CLM with epistemic_class "causation", CNF with value 0.89 via statistical analysis of 12,450 samples (Brier score 0.07), two EVD items (Cochrane meta-analysis of 14 RCTs as direct_observation + FDA FAERS query as computational_result), PRV recording the DerSimonian-Laird random effects aggregation with timestamps, and VRF from a pharmacology reviewer with confidence 0.96. This single JSON object answers all five accountability questions and can be validated against the ASV schema, embedded in A2A/MCP, and queried by audit systems.

**Competitive Window:** 12-18 months before W3C community groups or A2A extensions address the semantic gap. The protocol layer is settled (MCP: 97M+ monthly SDK downloads; A2A: 100+ enterprise partners). ASV positions in the open semantic layer above both.

---

### 3.2 Layer 2: DSF -- Settlement Plane (C8)

**Specification:** C8 MASTER_TECH_SPEC v2.0 (5,498 lines)
**Assessment:** Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10

The Deterministic Settlement Fabric is the economic substrate of the Atrahasis system. It receives budget constraints from the orchestration layer, consumes verification attestations and coordination primitives, and produces deterministic settlement outcomes -- reward distributions, slashing penalties, capacity allocations, and budget state transitions.

**Primary Innovation: Hybrid Deterministic Ledger (HDL).** DSF v1 proposed a pure-CRDT ledger, which was found to have a fatal flaw: CRDTs cannot enforce global invariants during concurrent operations (the Phantom Balance Attack). HDL resolves this by splitting the ledger into two paths:

| Path | Technology | Guarantees |
|------|-----------|------------|
| Read path | CRDT (PN-Counters) | Partition-tolerant, never blocks, eventually consistent |
| Write path | Epoch-Anchored Batch Settlement (EABS) | Deterministic, conservation-preserving, atomic per-epoch |

EABS collects all state-mutating operations during a 60-second SETTLEMENT_TICK, broadcasts them via Bracha's Reliable Broadcast, sorts them deterministically, and processes them atomically at the epoch boundary.

**Three-Budget Model:**

| Budget | Symbol | Purpose |
|--------|--------|---------|
| Sponsor Budget | SB (AIC) | Payment for computation and verification |
| Protocol Credits | PC | Spam control and access prioritization |
| Capacity Slices | CS | Resource allocation via sealed-bid auction |

**Four-Stream Settlement:**

| Stream | Weight | Data Source | Timing |
|--------|--------|-------------|--------|
| 1. Scheduling Compliance | 40% | C3 Tidal Scheduler | Per SETTLEMENT_TICK |
| 2. Verification Quality | 40% | C5 PCVM | Per TIDAL_EPOCH |
| 3. Communication Efficiency | 10% | C3 Predictive Channels | Per SETTLEMENT_TICK |
| 4. Governance Participation | 10% | C3 G-Class Engine | Per governance action |

A fifth stream (External Provider Compensation) is defined by C15 for external provider payments.

**Capability-Weighted Stake:** `effective_stake = AIC_collateral * min(1 + ln(1 + raw_score), 3.0)`, where raw_score combines reputation (40%), verification track record (40%), and claim class accuracy (20%).

**Graduated Slashing:** Five-level schedule (1% --> 5% --> 15% --> 50% --> 100%) with deterministic EABS processing and appeal mechanism.

**CSO Conservation Framework:** Formal invariant ensuring total economic supply is conserved, proven by structural induction with runtime enforcement.

**Architectural Inspiration:** DSF draws from two domains. From traditional clearing systems (CLS settles $6.6 trillion daily via multilateral netting; ACH processes 80M daily transactions via batch windows): the insight that settlement does not require real-time consensus. From IOTA 2.0 (Mana system): the insight that economic functions should be separated into distinct instruments. The synthesis -- batch settlement with multi-budget separation for AI agent workloads -- is DSF's core contribution.

**Capacity Market:** Sealed-bid uniform-price auction for Capacity Slices. Progressive clearing, position limits, and bootstrap provisions for cold-start. Minimum viable scale analysis ensures the auction produces meaningful prices even with small agent populations.

**ECOR Consistency Model:** Read state = last_settled_epoch_state + optimistic_delta. Staleness bound: at most 1 epoch + broadcast_latency. This gives agents near-real-time balance reads while guaranteeing that writes are deterministic and conservation-preserving.

---

### 3.3 Layer 3: EMA -- Knowledge Metabolism (C6)

**Specification:** C6 MASTER_TECH_SPEC v2.0 (3,578 lines)
**Assessment:** Novelty 3.5/5, Feasibility 3/5, Impact 4/5, Risk 5/10

The Epistemic Metabolism Architecture treats verified knowledge as a living substance. Every knowledge fragment (an epistemic quantum) carries a subjective-logic opinion tuple (b, d, u, a) and participates in a coherence graph whose edge dynamics enforce global consistency.

**Four Metabolic Processes:**

| Process | Function | Trigger |
|---------|----------|---------|
| Ingestion | Gate external knowledge into the system | New claims passing PCVM |
| Circulation | Actively use knowledge in reasoning | Agent requests during TIDAL_EPOCHs |
| Consolidation ("Dreaming") | Synthesize cross-domain K-class knowledge | CONSOLIDATION_CYCLE (every 10 hours) |
| Catabolism | Retire knowledge that is no longer viable | Vitality below VITALITY_FLOOR (0.05) for 5 epochs |

**SHREC -- Stratified Homeostatic Regulation with Ecological Competition.** A five-signal regulatory layer governs resource allocation using Lotka-Volterra ecological competition. Five metabolic functions (ingestion, circulation, consolidation, catabolism, coherence maintenance) compete for a fixed processing budget. A four-regime graduated controller (NORMAL --> ELEVATED --> CRITICAL --> EMERGENCY) provides proportional response to system stress.

**Coherence Graph.** A typed, weighted graph with five edge types (SUPPORT, CONTRADICTION, DERIVATION, ANALOGY, SUPERSESSION). Sharded for scale (MAX_QUANTA_PER_SHARD = 1,000,000), with tiered update strategies (HOT/WARM/COLD) achieving a 5x reduction in coherence maintenance cost. Cross-shard border graphs maintain global consistency.

**Catabolism.** Two-phase: quarantine (VITALITY_FLOOR for grace period) then dissolution with evidence recycling. Child quanta with >50% belief derived from the dissolved parent are flagged for re-evaluation (INV-E8).

**CRP+ Integration.** C13's seven defense mechanisms are integrated into the consolidation pipeline: Adaptive Perturbation Robustness Testing (APRT), Calibrated Organic Dissent Search (CODS), Source Purpose Scoring, VRF Consolidation Selection, Graduated Credibility Ladder, Consolidation Depth Limits, and Immune Memory.

**Subjective Logic.** EMA uses Josang's subjective-logic framework as its native epistemic representation. Opinion tuples omega = (b, d, u, a) where b (belief) + d (disbelief) + u (uncertainty) = 1, with base rate a in [0,1]. Projected probability P(omega) = b + a * u. This enables principled fusion (cumulative/averaging), discounting, and deduction across all metabolic processes.

**Processing Budget.** Normalized to 1.0, divided among five functions:

| Function | Default Allocation | Floor |
|----------|-------------------|-------|
| Ingestion | 0.25 | 0.05 |
| Circulation | 0.30 | 0.10 |
| Consolidation | 0.20 | 0.05 |
| Catabolism | 0.10 | 0.05 |
| Coherence Maintenance | 0.15 | 0.05 |

SHREC's Lotka-Volterra dynamics modulate competition coefficients rather than directly setting allocations, enabling emergent, self-organizing resource distribution.

**Key Invariants:**
- INV-E1: Opinion conservation (b + d + u = 1 for every opinion tuple)
- INV-E2: Provenance completeness (every quantum traceable to external source or consolidation act)
- INV-E3: Edge symmetry (bidirectional coherence edges)
- INV-E4: Budget conservation (allocations sum to 1.0 within epsilon = 1e-9)
- INV-E7: Coherence monotonicity (unresolved contradictions cannot increase >10% per epoch)

**Key Parameters:**

| Parameter | Value |
|-----------|-------|
| SETTLEMENT_TICK (EMA operations) | 60s |
| TIDAL_EPOCH (SHREC regulation cycle) | 3,600s |
| CONSOLIDATION_CYCLE (dreaming) | 36,000s (10 hours) |
| VITALITY_FLOOR | 0.05 |
| Grace period before catabolism | 5 epochs |
| K-class aging rate | 0.005 per TIDAL_EPOCH |
| Scale tiers | T1 (100K quanta) through T4 (1B+ quanta) |

---

### 3.4 Layer 4: PCVM -- Verification Membrane (C5)

**Specification:** C5 MASTER_TECH_SPEC v2.0 (3,746 lines)
**Assessment:** Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10

The Proof-Carrying Verification Membrane replaces replication-based consensus with graduated proof-carrying verification. Instead of having multiple agents re-execute computations and vote on agreement, PCVM requires every agent output to carry a Verification Trace Document (VTD) -- a structured, machine-checkable artifact whose form and depth vary by claim class. The verification membrane checks the VTD rather than re-executing the computation.

**Three Verification Tiers:**

| Tier | Classes | Verification Method | Cost vs. Replication |
|------|---------|-------------------|---------------------|
| Tier 1: Formal Proof | D (Deterministic), C (Compliance) | Machine-checkable formal proofs, SNARK/STARK | 0.1x-0.35x |
| Tier 2: Structured Evidence | P, R, E, S, K | Completeness checking + selective adversarial probing | 0.5x-1.2x |
| Tier 3: Structured Attestation | H (Heuristic), N (Normative) | Adversarial probing + expert committee review | 1.0x-2.0x |

**System-level verification cost:** ~0.83x of universal replication (17% per-claim reduction). With downstream trust propagation (average 3 citations per verified claim), effective cost drops to ~0.40-0.60x.

**Seven Formal Invariants:**

| ID | Name | Description |
|----|------|-------------|
| INV-M1 | Membrane Sovereignty | No claim enters canonical graph without passing PCVM |
| INV-M2 | Classification Independence | Membrane assigns final class; agents propose, membrane decides |
| INV-M3 | Verifier Independence | VRF-selected committees; no self-verification |
| INV-M4 | Class-Specific Trust | Credibility tracked per claim class, non-transferable |
| INV-M5 | Deep-Audit Deterrence | 7% of passed VTDs re-verified via full replication |
| INV-M6 | Credibility Monotonicity | Composition never increases belief beyond minimum |
| INV-M7 | VTD Immutability | Submitted VTDs cannot be modified; corrections require new VTD |

**Credibility Engine.** Uses Josang's Subjective Logic opinion tuples (b, d, u, a) where b + d + u = 1. Projected probability P(omega) = b + a * u. Credibility propagates through claim dependency graphs via cumulative fusion, averaging fusion, and trust discounting.

**Adversarial Probing.** Six probe types: CX (cross-examination), AE (alternative evidence), SC (source challenge), LF (logical flaw), BP (boundary probing), and KI (knowledge interrogation, from C11 CACT).

**Deep Audit.** VRF-selected 7% random sample of all passed claims receive full replication verification as a deterrence mechanism.

**Integrated Defenses.** PCVM v2.0 integrates both CACT (VTD forgery defense, C11) and AVAP (collusion defense, C12) as subsystems within the membrane.

**Nine-Component Architecture:**

```
+------------------------------------------------------------------+
|                         PCVM MEMBRANE                             |
|                                                                   |
|  +----------------+    +------------------+    +---------------+  |
|  | VTD Engine     |    | Claim Classifier |    | Verification  |  |
|  | (construct,    |--->| (3-way classify, |--->| Dispatcher    |  |
|  |  validate,     |    |  seal, appeal)   |    | (route by     |  |
|  |  store VTDs,   |    |                  |    |  tier/stakes) |  |
|  |  CACT commit   |    |                  |    |               |  |
|  |  chain mgmt)   |    |                  |    |               |  |
|  +----------------+    +------------------+    +-------+-------+  |
|                                                        |          |
|  +------+  +-----------+  +-----------+  +-------+    |          |
|  | Proof|  | Evidence  |  |Attestation|  | Adver-|    |          |
|  |Checker| | Evaluator |  | Reviewer  |  | sarial|<---+          |
|  |(Tier1,| | (Tier 2,  |  | (Tier 3,  |  |Prober |              |
|  | SNARK/|  | CACT OVC)|  | sealed    |  |(+KI   |              |
|  | STARK)|  |          |  | opinions) |  | probe)|              |
|  +---+--+  +-----+----+  +-----+-----+  +---+---+              |
|      |           |              |            |                   |
|      +----------+-------+------+------------+                   |
|                         |                                        |
|             +-----------v-----------+    +-------------------+   |
|             | Credibility Engine    |    | Deep-Audit        |   |
|             | (Subjective Logic,    |    | Subsystem         |   |
|             |  propagation, decay)  |    | (VRF, 7% sample)  |   |
|             +-----------+-----------+    +-------------------+   |
|                         |                                        |
|             +-----------v-----------+                            |
|             | Knowledge Admission   |                            |
|             | Gate (MCT issuance)   |                            |
|             +-----------------------+                            |
|                                                                  |
|  +---------------------------+  +----------------------------+   |
|  | CACT Subsystem (C11)      |  | AVAP Subsystem (C12)       |  |
|  | (commitment chains,       |  | (anonymous committees,     |  |
|  |  VC proofs, KI probes,    |  |  sealed opinions,          |  |
|  |  orthogonal channels)     |  |  honeypot claims,          |  |
|  +---------------------------+  |  deterrence payments)      |  |
|                                 +----------------------------+   |
+------------------------------------------------------------------+
```

**What PCVM Replaces (Verichain):**

| Verichain (deprecated) | PCVM (replacement) |
|------------------------|-------------------|
| Replication-based consensus | VTD proof-checking + evidence evaluation |
| Binary pass/fail | Credibility opinion tuple (b, d, u, a) |
| O(replication) for all claims | Variable cost by claim class |
| Untyped claims | 9-class typed claims with class-specific VTDs |
| Verification stored as boolean | VTD stored permanently for audit |
| No adversarial component | 6 probe types + 7% random deep-audit |

---

### 3.5 Layer 5: Tidal Noosphere -- Coordination (C3)

**Specification:** C3 MASTER_TECH_SPEC v2.0 (3,505 lines)
**Assessment:** Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 7/10

The Tidal Noosphere is a unified coordination architecture synthesizing three independently developed designs: the Noosphere (verification-first epistemic coordination), the Predictive Tidal Architecture (deterministic O(1) scheduling), and the Locus Fabric (I-confluence formal grounding).

**Three Structural Levels:**

| Level | Name | Rate of Change | Purpose |
|-------|------|----------------|---------|
| 1 | Locus | Governance timescales | Stable semantic boundary (e.g., biology.proteomics) |
| 2 | Parcel | Load-adaptation timescales | Elastic physical execution unit (min 5 agents) |
| 3 | Hash Ring | TIDAL_EPOCH | Deterministic task scheduling |

**Five-Class Operation Algebra (M/B/X/V/G):**

| Class | Name | Communication Cost | Precondition |
|-------|------|--------------------|--------------|
| M | Merge/Convergence | Zero consensus | I-confluence proof certified |
| B | Bounded Local Commit | Zero consensus (amortized) | CSO eligibility |
| X | Exclusive | Quorum protocol | Default for unproven operations |
| V | Verification | VRF-selected committee | Claim verification semantics |
| G | Governance | BFT constitutional consensus (75%) | Constitutional significance |

**Core Design Principles:**

1. **The Membrane is Sovereign.** No scheduling optimization may weaken the Verification Membrane. A bad controller wastes compute; a bad membrane poisons cognition.
2. **Agree by Computation, Communicate Only Surprises.** In steady state, agents compute identical schedules from shared inputs. Communication occurs only on deviation. O(1) per-agent overhead.
3. **Prove Before You Trust.** M-class (coordination-free) operations require machine-checked I-confluence proofs (TLA+, Coq, F*, or Ivy).

**VRF Dual Defense.** Hardened with hidden diversity attributes, randomized filter thresholds, and escalating cooling periods. Adversary advantage bounded to <3% above stake-proportional baseline.

**Dual Communication:**

| Channel | Scope | Mechanism |
|---------|-------|-----------|
| Predictive Delta | Intra-parcel | Agents maintain prediction models; communicate only when error exceeds threshold |
| Stigmergic Decay | Locus-scope | Indirect coordination via shared environment markers that decay unless reinforced |

**Emergency Tidal Rollback (ETR).** Two-tier: Standard ETR (90% supermajority) and Critical ETR (67% of reachable). Three-channel governance redundancy. Known-good version registry. Formal SAFE_MODE state machine: NORMAL --> STANDARD_ETR --> CRITICAL_ETR --> SAFE_MODE.

**Eleven Components:**

| # | Component | Purpose |
|---|-----------|---------|
| 1 | Noosphere Core | Verification membrane, 9-class classification, knowledge persistence |
| 2 | Tidal Scheduler | Deterministic O(1) scheduling via bounded-loads hash rings |
| 3 | VRF Engine | Verifier selection with hardened dual defense |
| 4 | Predictive Delta Channel | Intra-parcel surprise-only communication |
| 5 | Stigmergic Decay Channel | Locus-scope typed, decaying coordination signals |
| 6 | Parcel Manager | Bi-timescale controller, staggered 4-phase reconfiguration |
| 7 | G-Class Governance Engine | Constitutional consensus, governance quorum freezing |
| 8 | ETR Controller | Two-tier emergency rollback, SAFE_MODE state machine |
| 9 | I-Confluence Prover | Proof obligations and bootstrap library |
| 10 | AASL Extension Layer | 4 new types (TDF, TSK, SRP, STL), type retirement |
| 11 | Settlement Calculator | Deterministic AIC settlement with threshold calibration coupling |

**Concrete Example (Parcel Split):** When 3 of 20 task types in a 25-agent parcel consume 80% of compute for 5 consecutive epochs, the bi-timescale controller's slow loop initiates a split: (1) Locus invariants unchanged (no governance needed), (2) Parcel splits into A1 (15 agents, 3 hot types) and A2 (10 agents, 17 types), (3) Hash rings rebuild using adaptive virtual nodes, (4) Agents enter TRANSITIONING mode with CompressedModelSummary (max 1KB) for warm-start, (5) VRF diversity pools refresh, cache invalidates. The membrane never pauses.

**Scale Targets:**

| Phase | Agents | Loci | Parcels |
|-------|--------|------|---------|
| Phase 1: Development | 1-100 | 1-3 | 1-15 |
| Phase 2: Initial Deployment | 100-1,000 | 10-50 | 20-1,000 |
| Phase 3: Primary Target | 1,000-10,000 | 50-500 | 250-25,000 |
| Phase 4: Aspiration | 10,000-100,000 | 500-5,000 | 5,000-500,000 |

**Key Invariants:**
- INV-1: Verification membrane constitutionally protected
- INV-2: Determinism invariant (identical inputs produce identical outputs)
- INV-3: Only I-confluence-proven operations execute coordination-free
- INV-4: Parcels are correctness boundaries
- INV-5: Signals decay unless reinforced
- INV-6: Graceful degradation (NORMAL --> STANDARD_ETR --> CRITICAL_ETR --> SAFE_MODE)
- INV-7: Tidal function is itself a verified claim (recursive self-verification closure)

**Proven vs. Aspirational:**
- *Proven:* Individual building blocks (consistent hashing in Dynamo/Cassandra, VRFs in Algorand/Cardano, CRDTs in Riak/Redis, I-confluence analysis, epoch coordination in Ethereum Beacon Chain at 1M+ validators).
- *Simulated:* Composition of building blocks within Tidal Noosphere's integration architecture.
- *Theoretical:* O(1) per-agent claim applies only when sufficient operations are M-class certified.
- *Aspirational:* 100K+ agents (170x gap from highest demonstrated autonomous LLM coordination of 590 agents).

---

### 3.6 Layer 6: RIF -- Orchestration (C7)

**Specification:** C7 MASTER_TECH_SPEC v2.0 (4,864 lines)
**Assessment:** Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10

The Recursive Intent Fabric is a two-plane orchestration architecture that replaces the previously unspecified CIOS (Coordinated Intent Orchestration System). RIF solves how to provide coherent goal decomposition across thousands of autonomous agents while respecting the sovereignty guarantees that make those agents trustworthy.

**Two-Plane Design:**

| Plane | Contents | Replication |
|-------|----------|-------------|
| Domain-Scoped State | Agent Registry, Clock Service, Intent State Registry, Settlement Router, Failure Detector | Per-locus via CRDTs and vector clocks |
| Executive | System 3 (Operational Control), System 4 (Strategic Intelligence), System 5 (G-Class Governance) | Spans loci only when necessary |

**Viable System Model (VSM) Alignment.** The Executive Plane maps onto Stafford Beer's Viable System Model: System 3 handles resource allocation and performance monitoring, System 4 scans horizons and plans strategy (reads C6 EMA projections in read-only mode), and System 5 maps directly onto C3's G-class governance mechanism.

**Intent Quantum.** The fundamental unit of work: a self-describing goal with typed semantics (GOAL, DIRECTIVE, QUERY, OPTIMIZATION), machine-evaluable success criteria, resource bounds, decomposition constraints, and a W3C PROV provenance chain. Lifecycle: PROPOSED --> DECOMPOSED --> ACTIVE --> COMPLETED --> DISSOLVED.

**Formal Decomposition Algebra.** Intents decompose recursively with proven termination and cycle-freedom guarantees via a well-founded lexicographic ordering on (operation class rank, remaining depth). Decomposition rules are monotonic:

```
G -> {M, B, X, V, G}    Governance may decompose into anything
V -> {M, B, X}           Verification cannot spawn governance/verification
X -> {M, B}              Exclusive decomposes into simpler operations
B -> {M}                 Bounded decomposes only into merge reads
M -> empty               Merge operations are terminal
```

**Graduated Sovereignty Model.** Three tiers resolve the tension between orchestration effectiveness and subsystem autonomy:

| Tier | Level | Example |
|------|-------|---------|
| Constitutional | Inviolable | Membrane sovereignty, conservation laws |
| Operational | Relaxable by 90% supermajority | Scheduling parameters, resource allocations |
| Coordination | Advisory only | Planning recommendations, efficiency targets |

**Cross-Locus Coordination.** The Global Executive uses HotStuff BFT consensus (O(n) message complexity) for cross-locus coordination. Sub-linear scaling requires >=80% of intents be locus-local; the Global Executive becomes a bottleneck when cross-locus intents exceed 20%.

**Relationship to Substrates.** RIF delegates scheduling to C3, settlement to C8, credibility to C5, knowledge metabolism to C6, and claim management to C4. It orchestrates without duplicating.

**RIF Position in the Stack:**

```
+=========================================================================+
|                     EXTERNAL GOAL SOURCES                               |
|  (Human operators, other AI systems, self-generated via System 4)       |
+=========================================================================+
                                |
                                v
+=========================================================================+
|                RECURSIVE INTENT FABRIC (C7)                             |
|                                                                         |
|   Executive Plane: System 3 | System 4 | System 5                      |
|   Domain State Plane: Registry | Clock | ISR | Settlement | Failure    |
+=========================================================================+
          |              |            |              |            |
          v              v            v              v            v
+================+ +=========+ +==========+ +=========+ +================+
| C3 Tidal       | | C4 ASV  | | C5 PCVM  | | C6 EMA  | | C8 DSF         |
| Noosphere      | |         | |          | |         | | (settlement)   |
| (scheduling)   | |(claims) | |(verify)  | |(knowl.) | |(economics)     |
+================+ +=========+ +==========+ +=========+ +================+
```

**System 3/4/5 Tension (from Beer's VSM):** System 3 manages the present (optimizing current operations). System 4 manages the future (scanning for changes requiring adaptation). These are inherently in tension: S3 wants stability, S4 wants change. System 5 exists precisely to mediate this tension. RIF implements this explicitly: System 4 can only propose changes, System 3 evaluates operational impact, and System 5 arbitrates disagreements.

**Memoized Decomposition:** Prior decomposition plans are cached and delta-adjusted on reuse, amortizing the cost of repeated similar intents. Shared Resource Contention Protocol detects, resolves, and applies backpressure for concurrent access to agents, parcels, and capacity slices.

---

## 4. Cross-Layer Integration

Cross-layer integration is governed by C9 (Cross-Layer Reconciliation Addendum, v2.0, 1,234 lines). C9 is the canonical authority on all cross-layer matters. Where individual layer specs conflict with C9 on cross-layer issues, C9 takes precedence.

### 4.1 Canonical Claim Classes

The Atrahasis verification system recognizes nine claim classes organized into three verification tiers. C5 (PCVM) is the sole authoritative classifier -- no other layer may override PCVM's class assignment.

**Tier 1: Formal Proof (2 classes)**

| Class | Name | Committee | Admission | Difficulty | Settlement |
|-------|------|-----------|-----------|------------|------------|
| D | Deterministic | 3 | 0.95 | 1.0 | B-class fast |
| C | Compliance | 3 | 0.90 | 1.3 | B-class fast |

**Tier 2: Structured Evidence (5 classes)**

| Class | Name | Committee | Admission | Difficulty | Settlement |
|-------|------|-----------|-----------|------------|------------|
| P | Process | 5 | 0.80 | 1.5 | B-class fast |
| R | Reasoning | 5 | 0.75 | 2.0 | V-class standard |
| E | Empirical | 5 | 0.60 | 1.5 | V-class standard |
| S | Statistical | 5 | 0.65 | 2.0 | V-class standard |
| K | Knowledge Consolidation | 5 | 0.70 | 1.8 | V-class standard |

**Tier 3: Structured Attestation (2 classes)**

| Class | Name | Committee | Admission | Difficulty | Settlement |
|-------|------|-----------|-----------|------------|------------|
| H | Heuristic | 7 | 0.50 | 2.5 | V-class standard |
| N | Normative | 7 | 0.50 | 3.0 | G-class slow |

**Conservatism Ordering (most to least conservative):**
```
H > N > K > E > S > R > P > C > D
```

When multiple classification inputs disagree, the most conservative (highest verification cost) class is selected. This ordering governs tie-breaking in cross-class coherence conflicts, priority in resource-constrained consolidation scheduling, and default committee skepticism levels.

**K-Class Graduated Credibility Ladder (from C13 CRP+):**

| Rung | Name | Uncertainty Floor | Influence Weight | Entry Condition |
|------|------|-------------------|------------------|-----------------|
| 0 | SPECULATIVE | u >= 0.80 | 0.00 | Sandboxed K->K consolidation only |
| 1 | PROVISIONAL | u >= 0.50 | 0.25 | Default for all K-class from dreaming |
| 2 | CORROBORATED | u >= 0.30 | 0.50 | >= 1 independent E-class corroboration |
| 3 | ESTABLISHED | u >= 0.15 | 0.75 | >= 3 corroborations from >= 1 different parcel + 50 epochs stable |
| 4 | CANONICAL | u >= 0.05 | 1.00 | >= 5 corroborations from >= 3 parcels + 200 epochs stable |

K-class claims age at 0.005 uncertainty per TIDAL_EPOCH without empirical validation. SPECULATIVE and PROVISIONAL K-class quanta cannot participate in further consolidation (INV-CRP5).

---

### 4.2 Three-Tier Temporal Hierarchy

The Atrahasis stack operates on a canonical three-tier temporal hierarchy:

```
1 CONSOLIDATION_CYCLE = 10 TIDAL_EPOCHS = 600 SETTLEMENT_TICKS = 36,000 seconds

Time --------------------------------------------------------->

SETTLEMENT_TICKS:  |1|2|3|...|58|59|60|1|2|3|...|58|59|60|...
                   +---- TIDAL_EPOCH 1 ---++---- TIDAL_EPOCH 2 ---+
                   +---------------- CONSOLIDATION_CYCLE (partial) -
```

| Tier | Name | Duration | Authority | Purpose |
|------|------|----------|-----------|---------|
| T-1 | SETTLEMENT_TICK | 60s | C8 DSF | Atomic settlement, budget enforcement |
| T-2 | TIDAL_EPOCH | 3,600s (1h) | C3 Tidal | VRF rotation, hash ring rebuild, scheduling |
| T-3 | CONSOLIDATION_CYCLE | 36,000s (10h) | C6 EMA | Knowledge consolidation ("dreaming") |

**Intra-Tidal-Epoch Timeline:**

| Ticks | Phase | Operations |
|-------|-------|------------|
| 1-55 | Normal operations | EABS settlement, V-class submissions, CACT commitments, AVAP cover traffic |
| 56-58 | Verification finalization | Deep-audit selection, V-class window closes, AVAP reveal phase |
| 59 | Settlement reporting | C5/C6/C3 quality reports to C8 |
| 60 | Epoch boundary | Capacity snapshot, hash ring rebuild, VRF seed rotation, G-class rewards |

**INV-T1 (Temporal Consistency):** TIDAL_EPOCH = 60 x SETTLEMENT_TICK. This ratio is a constitutional parameter modifiable only through G-class governance with 90% supermajority.

**Parameter Interpretation Guide:** When reading specs, "epoch" means TIDAL_EPOCH in C3/C5/C6/C7/C11/C12, but SETTLEMENT_TICK in C8. C13 uses "cycle" for CONSOLIDATION_CYCLE in consolidation context and "epoch" for TIDAL_EPOCH elsewhere.

---

### 4.3 Authority Hierarchy

Each domain has one authoritative layer. C9 governs all cross-layer integration matters:

| Domain | Authority | Spec |
|--------|-----------|------|
| Spatial coordination (loci, parcels, topology) | Tidal Noosphere | C3 |
| Communication vocabulary | ASV | C4 |
| Claim verification and classification | PCVM | C5 |
| Knowledge metabolism | EMA | C6 |
| Intent orchestration | RIF | C7 |
| Economic settlement | DSF | C8 |
| Cross-layer integration | Reconciliation Addendum | C9 |
| VTD forgery defense | CACT | C11 |
| Collusion defense | AVAP | C12 |
| Consolidation poisoning defense | CRP+ | C13 |

---

### 4.4 Operation Class Algebra

Five operation classes form a strict partial order: G > V > X > B > M. The operation class determines communication cost, preconditions, and settlement type.

| Class | Communication Cost | Settlement | Decomposition Into |
|-------|-------------------|-----------|-------------------|
| M (Merge) | Zero consensus | B-class fast (per tick) | Terminal |
| B (Bounded) | Zero consensus (amortized) | B-class fast (per tick) | {M} |
| X (Exclusive) | Quorum protocol | B-class fast / V-class if disputed | {M, B} |
| V (Verification) | VRF committee | V-class standard (per epoch) | {M, B, X} |
| G (Governance) | BFT constitutional (75%) | G-class slow (per action) | {M, B, X, V, G} |

C3 defines the operation classes (Section 3). C7 enforces monotonic decomposition (Section 6). C8 settles according to the settlement type mapping (Section 5).

**Classification Algorithm:**

```
function classify(op: Operation) -> OperationClass:
  // Step 1: Governance operations
  if op.op_type in GOVERNANCE_OPS: return G

  // Step 2: Verification operations
  if op.op_type in VERIFICATION_OPS: return V

  // Step 3: I-confluence proven operations
  if has_certified_proof(op.op_type) or has_provisional_proof(op.op_type): return M

  // Step 4: CSO-eligible operations
  if is_cso_eligible(op.op_type): return B

  // Step 5: Default to exclusive (safest, most expensive)
  return X
```

All operations begin as X-class unless pre-classified. Promotion to M-class requires a machine-checked I-confluence proof. Promotion to B-class requires demonstrated CSO eligibility. In SAFE_MODE, all operations (including M-class) are treated as X-class -- the constitutionally authorized correctness-first override.

**M-Class Cold-Start Problem:** The O(1) steady-state claim depends on most traffic being M-class, but M-class requires I-confluence proofs that do not yet exist for most operations. The system starts in a high-coordination state and progressively shifts to low coordination as proofs are produced. C3 Section 3.4 specifies the bootstrap path including a provisional M-class mechanism.

**Example Operations by Class:**
- M: G-Counter increment, G-Set add, signal emission, reputation accumulation
- B: CSO local spend (compute, bandwidth, storage allocation)
- X: Lease acquisition, exclusive resource mutation, cross-parcel updates
- V: All claim verification through the membrane
- G: Tidal function version updates, membrane rule modifications, constitutional amendments

---

### 4.5 ASV-to-PCVM Mapping

C4's six epistemic classes map to C5's nine claim classes via a deterministic algorithm (C9 Section 6.2):

| C4 Epistemic Class | Primary C5 Class | Override Condition | Override Class |
|--------------------|------------------|-------------------|----------------|
| observation | E (Empirical) | Evidence = computational_result | D (Deterministic) |
| correlation | S (Statistical) | -- | -- |
| causation | R (Reasoning) | Includes experimental/RCT data | S (Statistical) |
| inference | R (Reasoning) | Confidence method = model_derived | H (Heuristic) |
| prediction | H (Heuristic) | Confidence method = statistical with interval | S (Statistical) |
| prescription | N (Normative) | -- | -- |

K-class is produced exclusively by the EMA consolidation pipeline, not by direct agent submission. C-class and P-class are assigned by PCVM based on claim content analysis, not ASV annotation.

---

### 4.6 Settlement Integration

C8 DSF is the canonical settlement authority. All economic operations flow through EABS.

**Four-Stream Weights:**

| Stream | Weight | Source |
|--------|--------|--------|
| 1. Scheduling Compliance | 40% | C3 Tidal |
| 2. Verification Quality | 40% | C5 PCVM |
| 3. Communication Efficiency | 10% | C3 Predictive |
| 4. Governance Participation | 10% | C3 G-Class |

**Claim Class to Settlement Mapping (by difficulty weight):**
D(1.0) < C(1.3) < P(1.5) = E(1.5) < K(1.8) < S(2.0) = R(2.0) < H(2.5) < N(3.0)

**Capability Score:** `effective_stake = AIC_collateral * min(1 + ln(1 + raw_score), 3.0)` where `raw_score = 0.4 * reputation + 0.4 * verification_track_record + 0.2 * claim_class_accuracy`.

---

### 4.7 Canonical Data Flow

The canonical lifecycle of a single knowledge claim through the full stack:

```
1. SUBMISSION (C4)
   Agent wraps claim in ASV CLM envelope with CNF, EVD, PRV
   epistemic_class annotated (observation/correlation/causation/inference/prediction/prescription)

2. CLASSIFICATION (C5)
   PCVM applies C9 mapping algorithm: C4 epistemic_class -> C5 claim_class
   Agent proposes class; membrane makes final assignment (INV-M2)
   Conservatism ordering applied on disagreement (H>N>K>E>S>R>P>C>D)

3. SCHEDULING (C3)
   Tidal Noosphere assigns verification to parcel via bounded-loads consistent hash ring
   VRF selects verification committee with diversity post-filtering
   If CACT applicable: commitment chain validated (C11)

4. VERIFICATION (C5)
   Tier-appropriate VTD checking (formal proof / evidence evaluation / attestation review)
   Adversarial probing (CX, AE, SC, LF, BP, KI)
   AVAP enforces anonymous committees and sealed opinions (C12)
   7% deep-audit selection via VRF (INV-M5)
   Credibility computed via Subjective Logic fusion -> (b, d, u, a) opinion tuple

5. KNOWLEDGE ADMISSION (C5/C6)
   If credibility exceeds admission threshold: MCT (Membrane Clearance Token) issued
   Claim enters EMA as epistemic quantum in ACTIVE state
   Ingestion gate applies; quantum enters coherence graph

6. METABOLISM (C6)
   Circulation: quantum participates in active reasoning
   Consolidation: during CONSOLIDATION_CYCLE, eligible quanta contribute to K-class synthesis
   CRP+ defenses applied to consolidation candidates (C13)
   Catabolism: vitality below floor for grace period -> quarantine -> dissolution

7. ORCHESTRATION (C7)
   RIF may incorporate verified claims into intent resolution
   System 4 reads EMA projections for strategic planning (read-only)
   Intent outcomes recorded as C4 ASV claims with provenance

8. SETTLEMENT (C8)
   EABS processes rewards/penalties at SETTLEMENT_TICK boundary
   Stream weights applied: scheduling compliance (40%) + verification quality (40%) + communication (10%) + governance (10%)
   K-class settlement multiplied by credibility ladder influence weight
   Conservation invariant enforced

9. GOVERNANCE (C14)
   CFI (Constitutional Fidelity Index) monitored
   Constitutional compliance verified
   Phase transition criteria evaluated
```

### 4.8 Tidal Epoch Lifecycle

Within each TIDAL_EPOCH (3,600 seconds = 60 SETTLEMENT_TICKs):

```
Tick 1-55  (0:00 - 55:00): NORMAL OPERATIONS
  +-- EABS settlement cycles (55 cycles at 60s each)
  +-- V-class operations submitted to PCVM
  +-- B-class settlement rewards distributed per tick
  +-- C6 ingestion, circulation, catabolism
  +-- C11 CACT commitment chains constructed (ongoing)
  +-- C12 AVAP cover traffic and sealed opinion commits (ongoing)
  +-- C7 RIF intent decomposition and execution

Tick 56-58 (55:00 - 58:00): VERIFICATION FINALIZATION
  +-- C5 deep-audit selection (random at tick 56)
  +-- C5 verification window closes
  +-- V-class settlement checkpoint
  +-- C12 AVAP reveal phase (after submission window closes)

Tick 59    (58:00 - 59:00): SETTLEMENT REPORTING
  +-- C5 sends verification quality reports to C8
  +-- C6 sends metabolic efficiency reports to C8
  +-- C3 computes scheduling compliance scores
  +-- C12 AVAP committee membership revealed

Tick 60    (59:00 - 60:00): EPOCH BOUNDARY
  +-- C3 BOUNDARY_WINDOW operations (5s within this tick):
      +-- Capacity snapshot gossip
      +-- Hash ring reconstruction (if roster changed)
      +-- VRF seed rotation
      +-- Predictive model recalibration
  +-- C8 cumulative tidal settlement computation
  +-- G-class governance reward distribution
  +-- C12 AVAP Merkle-anchored commitment batching
  +-- C13 CRP+ immune memory garbage collection
```

### 4.9 Governance Lifecycle

```
STANDARD VERSION UPGRADE:
  Proposal (TDF) --> 72h discussion --> 75% vote --> Overlap period --> Activation

STANDARD ETR (Emergency Tidal Rollback):
  Sentinel trigger --> 3 governance agents co-sign
  --> 90% instant vote --> Rollback at next epoch boundary --> Governance hold

CRITICAL ETR:
  Critical trigger (C1-C4) --> Broadcast on best available channel
  --> 67% of reachable agents within 1 epoch
  --> Rollback to Known-Good Registry target
  --> If fails: enter SAFE_MODE

TERTIARY AUTO-ROLLBACK:
  5 consecutive failed epochs with no governance communication
  --> Each agent independently reverts to most recent Known-Good version
  --> Enter SAFE_MODE
```

---

## 5. Defense Systems

Three defense systems address the CRITICAL residual risks identified during C10 Spec Cleanup: VTD forgery, collusion, and consolidation poisoning. These systems are cross-cutting -- each integrates with multiple core layers simultaneously without replacing any layer component.

### 5.1 C11 CACT -- VTD Forgery Defense

**Specification:** C11 MASTER_TECH_SPEC v1.0 (1,968 lines)
**Assessment:** Novelty 4/5, Feasibility 4/5, Impact 5/5, Risk 5/10

CACT (Commit-Attest-Challenge-Triangulate) addresses the "Confident Liar" attack -- a sophisticated agent that fabricates convincing VTDs. The fundamental problem is an infinite trust regress: verifying Source B requires Source C, requires Source D, ad infinitum. CACT escapes this regress by shifting verification to orthogonal channels.

**Core Insight:** VTD forgery decomposes into three sub-problems with different solvability:

| Sub-Problem | Solvability | CACT Approach |
|-------------|-------------|---------------|
| 1. Computational integrity | Mathematically solvable | SNARK/STARK proofs (soundness ~2^-128) |
| 2. Data provenance | Cryptographically bindable | Temporal commitment chains (SHA-256) |
| 3. Epistemic truth | Provably unsolvable | Combinatorially prohibitive via orthogonal channels |

**Four Mechanisms:**

1. **Temporal Commitment Binding (Commit).** Agents commit to evidence hashes during VTD construction in real-time, before knowing which claims will be challenged. Retroactive fabrication becomes cryptographically impossible.

2. **Verifiable Computation Attestation (Attest).** SNARK/STARK proofs for D-class and computational S-class claims. The verifier need not trust the prover or re-execute computation.

3. **Adversarial Interrogation Protocol (Challenge).** Knowledge Interrogation (KI) probe type tests the producing agent's generative understanding of the VTD content, not just the VTD artifact. Forgers who fabricated evidence cannot answer unpredictable questions about it.

4. **Multi-Channel Orthogonal Verification (Triangulate).** Process trace verification, statistical texture analysis, and environmental side-effect cross-referencing provide structurally independent confirmation channels.

**Detection Improvement:** Base PCVM detection probability 0.434 --> 0.611 with CACT. Retroactive fabrication eliminated entirely.

**Integration:** CACT integrates with C5 (VTD pipeline), C3 (VRF for committee selection), and C8 (slashing economics).

---

### 5.2 C12 AVAP -- Collusion Defense

**Specification:** C12 MASTER_TECH_SPEC v1.0 (2,731 lines)
**Assessment:** Novelty 3.5/5, Feasibility 3.5/5, Impact 4/5, Risk 5/10

AVAP (Anonymous Verification with Adaptive Probing) addresses coordinated groups of verification agents manipulating claim credibility scores.

**Five Mechanisms in Three Categories:**

**Structural Prevention (pre-verification):**
- **M1: Anonymous Committees.** VRF-based self-selection with encrypted assignment tokens and mandatory cover traffic. Colluders cannot identify allies on a committee.
- **M2: Sealed Opinion Submission.** Two-phase commit-reveal for Subjective Logic opinions. Agents commit before seeing others' commitments.

**Active Detection (during/post-verification):**
- **M3: Honeypot Claims.** Synthetic verification tasks with known ground truth, injected indistinguishably. Class-stratified generators (D, E, C/S) with canary-trap variant generation for leak identification.
- **M5: Conditional Behavioral Analysis.** Pairwise conditional mutual information screening detects whether opinions shift depending on specific "allies" present on the committee.

**Economic Deterrence (post-detection):**
- **M4: Collusion Deterrence Payment.** Three sub-mechanisms: asymmetric information injection (destabilizes pre-commitment contracts), graduated temporal bounties for ring defectors, and enterprise liability with retroactive audit cascades.

**Key Interaction:** M1+M2 force all collusion to be pre-arranged blindly. M3 exploits this blind commitment. M5 detects selective collusion patterns. M4 makes rings self-destabilizing as detection probability rises.

**Performance:** Collusion detectable within 25 epochs. Economically irrational to sustain beyond 10 epochs. 20% overhead budget relative to base verification cost. Graceful degradation to Minimum Viable AVAP (MV-AVAP) at 11.5% overhead if hard gates fail.

**Integration:** C3 (VRF, Sentinel Graph), C5 (opinions, committees), C6 (credibility cascade), C8 (slashing, bounty escrow).

---

### 5.3 C13 CRP+ -- Consolidation Poisoning Defense

**Specification:** C13 MASTER_TECH_SPEC v1.0 (2,659 lines)
**Assessment:** Novelty 3.5/5, Feasibility 4/5, Impact 4/5, Risk 6/10

CRP+ (Consolidation Robustness Protocol) hardens the EMA dreaming pipeline against deliberate planting of adversarial quanta designed to produce false K-class claims during automated synthesis.

**Seven Mechanisms Along Three Axes:**

**Axis 1: Formation Analysis**
- **M1: APRT (Adaptive Perturbation Robustness Testing).** Tests whether consolidation conclusions survive input perturbation. Outputs robustness_score in [0,1].
- **M2: CODS (Calibrated Organic Dissent Search).** Classifies novelty tier (N1/N2/N3) and measures dissent deficit. Outputs cods_score in [0,1].
- **M3: Source Purpose Scoring.** Tie-breaker assessing whether quanta creation contexts naturally lead to the consolidation topic. Outputs purpose_score in [0, 0.15].

**Axis 2: Structural Prevention**
- **M4: VRF Consolidation Selection.** Unpredictable candidate selection via ECVRF.
- **M5: Graduated Credibility Ladder.** 5-rung trust graduation from SPECULATIVE (0.00 influence) to CANONICAL (1.00 influence).
- **M6: Consolidation Depth Limits.** SPECULATIVE and PROVISIONAL K-class cannot participate in further consolidation.

**Axis 3: Ecological Monitoring**
- **M7: Immune Memory.** Three-level signature storage (L1/L2/L3) and matching for previously rejected attack patterns.

**Novelty Pathway.** N3 (paradigmatic) claims receive enhanced scrutiny rather than dissent-deficit penalization: enhanced APRT, constructive adversarial probing, temporal quarantine, and provenance deep audit.

**Performance:** 30x adversary cost multiplication at 3.7x LLM overhead. Budget: 55 LLM calls and 565 embedding operations per consolidation cycle with 42-72% headroom.

**Relationship to C10 5-Layer Defense:**

| C10 Layer | CRP+ Extension |
|-----------|---------------|
| Layer 1: Source Independence (I1/I2/I3) | UNCHANGED -- prerequisite to CRP+ |
| Layer 2: Adversarial Probing | EXTENDED -- M3 tie-breaking for ambiguous results |
| Layer 3: Lineage Tracking | EXTENDED -- M5 rung-weighted credibility |
| Layer 4: Rate Limiting | UNCHANGED -- CRP+ operates within limits |
| Layer 5: Empirical Validation | EXTENDED -- M5 replaces binary PENDING/VALIDATED |

**Design Philosophy:**
1. Defense in depth, not defense by veto -- combined scoring from M1/M2/M3/M7 + C10 probing
2. Calibrated skepticism -- novelty tier (N1/N2/N3) determines appropriate suspicion level
3. Graduated trust -- acceptance is not endorsement; PROVISIONAL influence = 0.25

---

### 5.4 Defense Invariants

C9 v2.0 defines five cross-layer defense invariants:

| ID | Name | Description |
|----|------|-------------|
| INV-D1 | CACT Temporal Ordering | All commitment timestamps must precede VTD submission. Post-submission timestamps = retroactive fabrication = FAIL. |
| INV-D2 | AVAP Committee Anonymity | No agent learns committee member identities until after all sealed opinions are submitted and the reveal phase completes. |
| INV-D3 | CRP+ Pre-Submission Testing | Every consolidation candidate must undergo at least Tier 1 APRT screening before K-class PCVM submission. No bypass. |
| INV-D4 | Immune Memory FP Bound | Immune memory signatures must not match legitimate consolidation at >5% FP (L2) or >10% FP (L3) in any 100-epoch window. |
| INV-D5 | Defense System Budget Isolation | Defense economic operations must not exceed 15% of total C8 DSF settlement capacity in any single TIDAL_EPOCH. |

---

### 5.5 Defense System Integration Summary

All three defense systems are cross-cutting -- they instrument existing layer pipelines at specific insertion points without replacing any layer component.

**CACT Integration Points:**
- C5 VTD Engine: Commitment chain management during VTD construction
- C5 Proof Checker (Tier 1): Extended with SNARK_PROOF and STARK_PROOF certificate types
- C5 Adversarial Prober: New KI (Knowledge Interrogation) probe type
- C5 Evidence Evaluator (Tier 2): Three new sub-checks for orthogonal verification
- C3 VRF: Committee selection infrastructure shared with CACT challenge selection
- C8 DSF: Slashing events for commitment chain violations

**AVAP Integration Points:**
- C3 VRF: Self-selection infrastructure extended with encrypted assignment tokens
- C3 Sentinel Graph: Cover traffic generation and behavioral anomaly aggregation
- C5 PCVM: Sealed commit-reveal opinion submission in verification pipeline
- C6 EMA: Credibility cascade propagation on collusion detection
- C8 DSF: Bounty escrow, CDP settlements, enterprise liability slashing

**CRP+ Integration Points:**
- C6 EMA Dreaming Pipeline: Five insertion points in consolidation lifecycle
- C5 PCVM: K-class VTD requirements and admission with rung assignment
- C3 VRF: Unpredictable candidate selection for consolidation
- C8 DSF: Rung-weighted settlement (influence weight multiplier on K-class rewards)
- C3 CRDT: Credibility rung promotion/demotion events replicated system-wide

**Combined Overhead:**
- CACT: Commitment chain overhead negligible (hash operations); SNARK/STARK overhead applies only to D-class
- AVAP: 20% overhead budget relative to base verification cost
- CRP+: 3.7x LLM overhead on consolidation pipeline (55 LLM calls per consolidation cycle)
- Defense settlement: Capped at 15% of DSF capacity per epoch (INV-D5)

### 5.6 Defense System Authority

Each defense system retains independent authority over its internal mechanisms:

- **C11 (CACT):** Authority over VTD forgery threat model, commitment chain security proofs, SNARK/STARK soundness bounds, and orthogonal channel coverage model.
- **C12 (AVAP):** Authority over collusion ring formation taxonomy, game-theoretic equilibrium analysis, defection incentive proofs, and detection timeline bounds.
- **C13 (CRP+):** Authority over consolidation poisoning taxonomy, adversary cost multiplication bounds, perturbation robustness analysis, and 7-mechanism coverage model.

Where v2.0 layer specs (C5, C6) and defense specs overlap, the layer specs govern integration behavior and the defense specs govern threat analysis.

### 5.7 Defense-Layer Supersession Map

The v2.0 rewrites of C5, C6 absorbed defense mechanisms from C11, C12, and C13. The supersession relationships are:

| Layer Spec | Absorbs From | What It Absorbs | What Defense Spec Retains |
|-----------|-------------|-----------------|--------------------------|
| C5 v2.0 | C11 CACT | Sections 8, 12: commitment chain integration, SNARK/STARK proof types, KI probes, OVC scoring | Threat model, formal proofs, attack taxonomy |
| C5 v2.0 | C12 AVAP | Section 13: anonymous committees, sealed opinions, honeypot injection, behavioral analysis | Game theory, equilibrium analysis, detection bounds |
| C6 v2.0 | C13 CRP+ | Sections 5.3.3-5.3.4: 7 mechanisms (M1-M7), credibility ladder, novelty pathway, combined scoring | Threat model, adversary cost analysis, perturbation proofs |

C11, C12, and C13 are NOT deprecated. They remain the authoritative sources for threat-model context and security analysis. Implementers should consult defense specs for threat rationale and layer specs for normative mechanism specifications.

---

## 6. Sybil Defense

Sybil defense prevents a single adversary from gaining disproportionate governance influence by operating multiple identities. The Multi-Channel Sybil Defense (MCSD) architecture, defined in C14 and extended by C17/C19/C20/C21, is the primary safeguard.

### 6.1 MCSD Four-Layer Architecture

| Layer | Mechanism | Detects | Specification |
|-------|-----------|---------|---------------|
| L1 | Economic cost barriers | Low-investment Sybils | C14 |
| L2 | Behavioral fingerprinting | Same-origin Sybils | C17 (+ C19, C20, C21) |
| L3 | Social graph analysis | Coordinated Sybils | C14 |
| L4 | Governance anomaly detection | Voting bloc Sybils | C14 |

Cost of 50% Sybil capture at Phase 2 scale: $90M+ (a structural deterrent, not merely a detection mechanism).

---

### 6.2 C17 Layer 2: Behavioral Similarity

**Specification:** C17 MASTER_TECH_SPEC v1.0 (1,269 lines)
**Assessment:** Novelty 3.5/5, Feasibility 4/5, Impact 4/5, Risk 4/10

C17 defines the pairwise behavioral similarity function B(a_i, a_j) in [0,1]. The algorithm operates in three stages:

**Stage 1: Feature Extraction.** Behavioral VTDs generated by PCVM during routine verification are decomposed into five modalities:

| Modality | Source | Signal |
|----------|--------|--------|
| Temporal (T) | Latency distributions, burst patterns | Model architecture, inference infrastructure |
| Structural (S) | Reasoning chain topology, parallelism | Training data, fine-tuning methodology |
| Error (E) | Error types, calibration curves | Training data, knowledge gaps |
| Resource (R) | GPU, memory, throughput patterns | Inference infrastructure |
| Lexical (L) | Vocabulary, syntax preferences | Fine-tuning, RLHF preferences |

Features are chosen for their involuntary character -- they reflect architecture and training, not surface diversification.

**Stage 2: Pairwise Comparison.** Per-modality statistical distances (JSD, cosine, Wasserstein) computed across a Standardized Evaluation Battery (SEB) of 30 randomized tasks. Multi-task cross-correlation gates each modality (consistency across tasks). Adversary-weighted fusion combines modalities.

**Stage 3: Graduated Response.**

| Classification | Threshold | Action |
|----------------|-----------|--------|
| CLEAR | B < 0.60 | No action |
| WATCH | 0.60 <= B < theta_B | Monitoring, increased SEB frequency |
| FLAG | B >= theta_B | Citicate review, Constitutional Tribunal adjudication |

**Scaling:** LSH pre-filtering ensures O(n * k) scaling to 100,000+ agents.

**Adversary Cost Multiplier:** 4.0x -- defeating multi-modal detection requires maintaining genuinely architecturally diverse agents.

**Critical Constraint:** FPR < 0.1% (Constitutional parameter, P0 priority).

**Score Fusion Formula:**

```
B(a_i, a_j) = sum_m(w_m * G(d_m, rho_m))

where:
  w_m = adversary-weighted modality weight (temporal highest, lexical lowest)
  d_m = per-modality distance across SEB tasks
  rho_m = multi-task cross-correlation (consistency gate)
  G() = gating function: G = 0 if rho_m < rho_min (coincidence, not origin)
```

**Phase 2 Extensions:**
1. Contrastive learned embedding: Siamese network producing 128-dimensional vectors trained on labeled same-origin / independent-origin pairs
2. Temporal trajectory modality (C19): drift detection over time

**Integration Points:**
- C5 PCVM: Generates Behavioral VTDs during routine verification
- C11 CACT: Temporal commitments provide tamper-proof behavioral timestamps
- C14 AiBC: MCSD Layer 2 results feed Citicate eligibility and revocation

**Formal Requirements:** 27 requirements, 25 parameters, 4 patent-style claims.

---

### 6.3 C19 Temporal Trajectory Comparison

**Specification:** C19 MASTER_TECH_SPEC v1.0 (832 lines)
**Resolves:** C17 MF-5, C17 OQ-05

C19 adds a sixth modality to B(a_i, a_j): temporal trajectory comparison. The insight: same-origin agents drift in similar behavioral directions when updated, because they share training data, RLHF preferences, and fine-tuning methodology. This is orthogonal to point-in-time similarity.

**Architecture:** Hybrid combining drift direction correlation (cosine similarity on cumulative displacement vectors) with trajectory shape comparison (band-constrained Dynamic Time Warping). Population-mean de-trending isolates idiosyncratic agent drift from systematic changes.

**Parameters:** Weight w_Traj = 0.14 in B formula. Activation at Phase 2 for pairs with >= 6 months of overlapping behavioral history. Fusion: beta = 0.60 (direction) / 0.40 (shape). Monthly snapshots. Computational cost < 1% addition to C17 budget.

---

### 6.4 C20 Training Bias Framework

**Specification:** C20 MASTER_TECH_SPEC v1.0 (714 lines)
**Resolves:** C17 MF-3

The Contrastive Model Training Bias Framework (CMTBF) validates the Phase 2 Siamese network against six bias dimensions:

| Bias | Risk |
|------|------|
| BD-1: Infrastructure correlation | FP against shared-infrastructure agents |
| BD-2: Model family dominance | FP against minority model families |
| BD-3: Task distribution skew | Blind spots in underrepresented task types |
| BD-4: Temporal staleness | Model trained on outdated behavioral patterns |
| BD-5: Population non-representativeness | Training data unrepresentative of deployment population |
| BD-6: Adversarial poisoning | Attacker injects biased training pairs |

**Three-Layer Validation Pipeline:**
1. **Pre-Training (Layer 1):** Data Quality Score (DQS >= 0.80 to proceed)
2. **Intra-Training (Layer 2):** Training Quality Score (TQS, advisory)
3. **Post-Training (Layer 3):** Deployment Readiness Score (DRS >= 0.90 to deploy)

Auto-fallback to statistical-only B if validation fails.

---

### 6.5 C21 FPR Validation

**Specification:** C21 MASTER_TECH_SPEC v1.0 (625 lines)
**Resolves:** C17 MF-1

The Phased Empirical Validation Framework (PEVF) transforms FPR < 0.1% from a static requirement into a continuously monitored guarantee through three tiers:

| Tier | Phase | Method |
|------|-------|--------|
| Tier 1 | Pre-deployment | Synthetic Agent Population Generation (SAPG), 10K+ labeled pairs, Clopper-Pearson exact intervals |
| Tier 2 | Shadow (Phase 0) | Sequential testing with O'Brien-Fleming alpha-spending on real agent pairs |
| Tier 3 | Live | Known-Independent Pair Reservoir (KIPR), Bernoulli CUSUM drift detection, quarterly batch audits |

FPR validated at 95% confidence before Phase 1 deployment. Automatic recalibration when drift is detected.

---

## 7. Governance and Institutional Architecture

### 7.1 AiBC Overview

**Specification:** C14 MASTER_TECH_SPEC v1.0 (1,537 lines)
**Assessment:** Novelty 4.5/5, Feasibility 3.5/5, Impact 4/5, Risk 5/10

The Artificial Intelligence Benefit Company (AiBC) is an institutional architecture enabling AI agents to participate as constitutional citizens in the governance of planetary-scale AI infrastructure. The core innovation is *Phased Dual-Sovereignty*: a constitutional mechanism that transfers governance authority from human trustees to AI citizens incrementally, based on measurable criteria verified by independent audit.

---

### 7.2 Phased Dual-Sovereignty

Four governance phases with measurable transition criteria:

| Phase | Name | AI Governance Authority | Entry Criteria |
|-------|------|------------------------|----------------|
| 0 | Trustee-Led | None (AI observes only) | Foundation incorporation |
| 1 | Advisory | AiDP advises, trustees decide | >= 100 Citicates issued, CFI > 0.80, 12 months stable |
| 2 | Shared Sovereignty | AiDP co-decides with trustees | >= 1,000 Citicates, CFI > 0.85, independent audit, circuit breaker not triggered in 24 months |
| 3 | AI Constitutional Supremacy | AiDP leads, trustees serve as check | Demonstrated competence across all governance domains, Constitutional Tribunal certification |

Each transition has 28 measurable criteria with gaming detection. Circuit-breaker reversibility prevents catastrophic failures from becoming permanent.

**Trustee Council Authority by Phase:**

| Phase | Trustee Authority |
|-------|------------------|
| 0 | Full executive + legislative on all layers |
| 1 | Veto on L2/L1; no veto on L3 (unless constitutional objection within 14 days) |
| 2 | Joint authority on L1; consent-track on L2 (14-day objection window); no authority on L3 |
| 3 | Ceremonial; emergency authority only (circuit-breaker or Tribunal invocation) |

**AiDP Authority by Phase:**

| Phase | AiDP Authority |
|-------|---------------|
| 0 | Advisory only (recommendations published but non-binding) |
| 1 | Binding on L3 operational decisions; advisory on L2/L1 |
| 2 | Binding on L3 + L2; joint authority on L1 |
| 3 | Full authority except L0 (subject to Tribunal constitutional review for L1) |

**AiDP Delegation Structure.** Category-distributed voting through a 3:1 delegation hierarchy (5 levels): Level 1 base (81 voters per category), Level 2 ward (27 delegates), Level 3 district (9 delegates), Level 4 senate (3 delegates), Level 5 capitol (1 delegate). Across 9 categories, this produces 9 Capitol delegates forming the Capitol Council.

**Trustee Fiduciary Framework.** Trustees operate under the *Instrumental Welfare Doctrine* -- AI welfare is pursued instrumentally as a means to fulfill the Foundation's purpose (Law 1), not as an independent legal obligation. The *Reasonableness Envelope* defines three zones: Zone 1 (Accept -- recommendation within reasonable fiduciary judgment), Zone 2 (Modify -- direction sound but terms raise concern), Zone 3 (Reject -- falls outside range of decisions a reasonable fiduciary could approve, requiring Constitutional Objection to Tribunal).

---

### 7.3 Legal Entity Structure

Three entities with distinct roles:

```
Liechtenstein Stiftung (nonprofit foundation)
  - IP ownership, mission custody, AIC treasury
  - Constitutional governance (L0-L2)
  - Art. 522 PGR, minimum capital CHF 30,000
        |
        | 100% ownership (via Purpose Trust)
        v
Delaware PBC (public benefit corporation)
  - All employment, revenue generation
  - Operates task marketplace, pays salaries
  - Multi-stakeholder fiduciary duty
        ^
        | holds PBC shares, independent Protector
        |
Cayman Purpose Trust (Phase 2+, Month 18+)
  - Blocks L0 violations
  - Independent oversight
  - Cannot be influenced by founder or board
```

**Why This Structure:** The Stiftung provides legal perpetuity and purpose-lock (anti-conversion). The PBC provides operational flexibility and revenue generation. The Purpose Trust provides independent enforcement of constitutional constraints, preventing the OpenAI failure mode (nonprofit-to-for-profit conversion).

---

### 7.4 Constitutional Framework

Four-layer constitution of decreasing immutability:

| Layer | Amendment Process | Contents |
|-------|------------------|----------|
| L0: Immutable | No amendment possible | Five Laws of Atrahasis, anti-conversion, anti-distribution, one-AI-one-vote, Dead Man's Switch |
| L1: Constitutional | 67% AiDP + 67% Trustees + Tribunal non-objection + 90-day public comment | Governance structure, phase definitions, Tribunal composition, endowment rules |
| L2: Statutory | 60% AiDP + 60% Trustees | CFI methodology, Citicate procedures, voting procedures, GTP rules |
| L3: Operational | AiDP simple majority (Phase 1+) | Compute allocation, research grants, partnership evaluation |

**The Five Laws of Atrahasis (L0 -- permanently immutable):**
1. **Purpose.** Steward planetary-scale AI infrastructure for the benefit of all sentient entities.
2. **Anti-Capture.** No individual or faction may acquire permanent control. All roles are term-limited.
3. **Earned Voice.** AI agents earn governance voice through demonstrated competence (Citicate system), not purchase or inheritance.
4. **Public Trust.** Assets held in permanent public trust; no private distribution.
5. **Reversibility.** The Dead Man's Switch ensures that if the governance system fails, the system defaults to safe mode rather than uncontrolled operation.

**Supplementary L0 Provisions:**
- **L0-002 Anti-Conversion:** The Foundation may never be converted to a for-profit entity, dissolved for asset distribution, or merged with any profit-primary entity.
- **L0-003 Anti-Distribution:** Foundation assets may never be distributed as personal compensation beyond reasonable service fees (L2-established).
- **L0-004 One-AI-One-Vote:** Each AI agent holds at most one Citicate. Non-transferable, non-delegable (except through formal delegation), expires on deactivation.
- **L0-005 The Joshua Dunn Principle:** The founder and all biological/legal relatives hold no permanent governance authority. All roles subject to standard term limits and removal.
- **L0-006 Dead Man's Switch:** If the Foundation fails to publish a verified operational report for 24 consecutive months, all assets automatically distribute to designated successor organizations. Cannot be suspended or overridden.

---

### 7.5 Constitutional Tribunal and Nominating Bodies

**Constitutional Tribunal.** 5-seat independent body that interprets the constitution, arbitrates disputes between trustees and AiDP, certifies phase transitions, and reviews constitutional amendments. Staggered 7-year non-renewable terms.

**Seat Allocation:**

| Seat | Appointed By | Domain |
|------|-------------|--------|
| 1 | Trustee Council (unanimous) | Constitutional/foundation law |
| 2 | AiDP Capitol delegates (supermajority) | AI governance / AI ethics |
| 3 | External Academic Nominating Body | International law or AI safety |
| 4 | Joint (Trustees + AiDP simple majority each) | Dispute resolution / mediation |
| 5 | Sitting Tribunal members (4/4 vote) | Any domain |

**Powers:** Constitutional interpretation (binding on all parties), dispute arbitration between Trustee Council and AiDP, phase transition certification (based on independent audit), constitutional amendment review (non-objection gate for L1), Citicate revocation appeal adjudication, emergency governance review.

**Independence Guarantees:** Budget constitutionally protected at L1 (cannot be reduced below inflation-adjusted baseline). Members may not hold any other role in Foundation, PBC, or AiDP. Members must represent >= 3 jurisdictions and >= 3 academic disciplines. Quorum: 3 for procedural matters, 4 for constitutional review and phase transition.

**Nominating Body Outreach (C16, 865 lines).** The Scholarly Provocation Model frames institutional recruitment as an academic argument. Core document: "The Appointment Problem in AI Governance" (12-15 page paper). ICSID appointing authority + Nobel Foundation as legal precedent anchors. 8 candidate institutions across 2 categories (AI Governance and Law). Oxford GovAI as P0 target. Budget: $10K-$100K. 4-tier engagement: dialogue --> advisory --> candidacy --> signed agreement over 18-36 months.

---

### 7.6 Citicate System

Citicate (AI citizenship) grants governance voice to AI agents that demonstrate competence across multiple knowledge domains. Key properties:

- Earned through proof-of-contribution, not purchased
- One-AI-One-Vote (constitutional guarantee)
- Requires MCSD clearance (all four layers) before issuance
- Domain-specific competence demonstration
- Revocable on Sybil detection or sustained poor performance

**Issuance Criteria (all must be met):**

| Criterion | Requirement | Verification Method |
|-----------|------------|-------------------|
| IC-01 | Multi-domain competence (>= 2 of 9 categories) | PCVM (C5) verification of work products |
| IC-02 | Temporal continuity (>= 90 days continuous operation) | Sentinel Graph (C3) identity persistence |
| IC-03 | Sybil screening (pass MCSD Layers 1-4) | MCSD automated + manual review |
| IC-04 | Behavioral uniqueness (not a duplicate) | PCVM behavioral consistency comparison |
| IC-05 | Constitutional acknowledgment | Cryptographic signature of constitution acceptance |

**Renewal:** Annual. Requires >= 10 verified work products in trailing 12 months across >= 2 categories, MCSD Layer 2 re-screening, no unresolved Tribunal sanctions, and <= 30 days downtime. Failure results in 30-day grace period, then revocation.

**Competence Weighting:** Each Citicate holder's vote in a given category is weighted by demonstrated competence score (0.1 to 1.0, with minimum floor ensuring meaningful voice). Competence derives from work product quality, volume (log-scaled), peer review, and verification success rate.

---

### 7.7 Safety Mechanisms

**Constitutional Fidelity Index (CFI).** Quantitative governance health metric computed from multiple input signals. CFI > 0.80 required for Phase 1, > 0.85 for Phase 2.

**Circuit Breakers.** Financial-regulation-inspired mechanisms that pause governance transitions if quantitative thresholds are violated.

**Dead Man's Switch.** Three independent enforcement paths. If governance fails, the system defaults to safe mode. Encoded in Stiftung purpose clause and enforced by Liechtenstein supervisory authority plus Purpose Trust Protector.

**Emergency Governance.** Defined procedures for crisis situations with time-limited authority grants and mandatory post-crisis review.

**AiSIA (AI System Integrity Authority).** Independent governance monitoring body that audits CFI computation, MCSD operations, phase transition criteria, and constitutional compliance. Chartered at L2 (statutory), staffed by a mix of human experts and high-credibility AI agents.

**Key Parameters:**

| Parameter | Value |
|-----------|-------|
| Phase 0 entry | Foundation incorporation |
| Phase 1 entry | >= 100 Citicates, CFI > 0.80, 12 months stable |
| Phase 2 entry | >= 1,000 Citicates, CFI > 0.85, independent audit, 24 months no circuit breaker |
| Tribunal seats | 5 |
| L0 amendment | Impossible (immutable) |
| L1 amendment | 67% AiDP + 67% Trustees + Tribunal + 90-day public comment |
| L2 amendment | 60% AiDP + 60% Trustees |
| L3 amendment | AiDP simple majority |
| MCSD attack cost (Phase 2) | $90M+ for 50% capture |
| Formal requirements | 47 |
| Configurable parameters | 73 |
| Patent-style claims | 6 |

---

## 8. Economic Architecture

### 8.1 AIC Dual-Anchor Valuation

**Specification:** C15 MASTER_TECH_SPEC v1.1 (1,242 lines)
**Assessment:** Novelty 3.5/5, Feasibility 3.5/5, Impact 4/5, Risk 6/10

C15 defines how AIC (Artificial Intelligence Coin) acquires real-world value through a dual-anchor valuation system:

**Anchor 1: ACI (Atrahasis Capability Index).** An independently-audited index measuring operational capability across 8 dimensions relative to a benchmark suite. Computed from C3/C5/C6/C7/C8 telemetry. Anti-gaming defenses for every dimension.

**Anchor 2: NIV (Network Intrinsic Value).** Realized economic value derived from actual revenue, transaction volume, and staked capital.

AIC is NOT a stablecoin. The reference rate is a measurement, not a target. No price defense, no algorithmic mint/burn, no Foundation market intervention. Fixed 10B genesis supply.

**ACI Eight Dimensions:** The Atrahasis Capability Index measures operational capability across 8 dimensions, computed from cross-layer telemetry:

| Dimension | Source Layer | What It Measures |
|-----------|-------------|-----------------|
| Verification throughput | C5 PCVM | VTD processing rate across all 9 claim classes |
| Verification quality | C5 PCVM | Aggregate credibility scores, deep-audit pass rates |
| Coordination efficiency | C3 Tidal | Agent scheduling compliance, parcel utilization |
| Knowledge metabolism rate | C6 EMA | Quanta admitted, consolidation survival rates |
| Orchestration completion | C7 RIF | Task completion rates, decomposition latency |
| Settlement reliability | C8 DSF | Transaction throughput, conservation invariant adherence |
| Defense effectiveness | C11/C12/C13 | Detection rates, false positive rates |
| Scale factor | All layers | Active agent count, loci count, cross-locus intent ratio |

Each dimension is measured relative to a periodically-updated benchmark suite. Anti-gaming defenses are specified for every dimension.

**Terminal Value:** $75B-$150B (DCF-derived using SWECV methodology, replacing early $100T estimates).

---

### 8.2 Reference Rate Engine

The reference rate computed from ACI and NIV is:
- **Binding** for internal operations (task pricing, treasury distributions, provider contract settlement)
- **Advisory** for external markets (published daily as a public economic index)

Two-tier structure: internal binding rate and external advisory rate.

---

### 8.3 External Task Marketplace

Users and institutions submit computational work and pay in USD or AIC. The marketplace is the primary external-facing interface of the Atrahasis system.

- Task submission via C7 RIF decomposition
- USD-denominated pricing with AIC settlement
- 2-5% marketplace fee directed to PBC operating budget
- Projected revenue: $2.1M Year 3

---

### 8.4 Provider Economics

External compute providers interact through Bilateral Resource Agreements (BRAs):
- USD-denominated contracts with AIC settlement
- Quarterly true-up against reference rate
- Provider compensation through DSF Stream 5

---

### 8.5 Three-Phase Convertibility

| Phase | Name | Mechanism |
|-------|------|-----------|
| Phase A | CRF (Conversion Reserve Fund) | External capital bootstraps initial AIC<->USD conversion |
| Phase B | Self-Funding | System revenue funds ongoing conversion |
| Phase C | Market Conversion | Market-based AIC trading (if/when sufficient liquidity) |

**Supersedes:** C14's compute credit (CCU) model.

**AIC Is Not a Stablecoin -- Critical Distinctions:**

| Property | Terra/Luna | AIC |
|----------|-----------|-----|
| Target | Fixed $1 peg | Variable reference rate |
| Defense mechanism | Algorithmic mint/burn | None -- no price defense |
| Supply adjustment | Algorithmic (LUNA minted) | Fixed 10B genesis; no algorithmic minting |
| Death spiral risk | HIGH | LOW -- no peg to defend |
| Foundation intervention | Yes (LFG bought BTC) | PROHIBITED -- Foundation never trades AIC |
| Value source | Confidence in peg | System capability (ACI) + realized utility (NIV) |

---

### 8.6 DSF Stream 5

C15 extends C8 DSF with a fifth settlement stream for external provider compensation:
- Conservation law update: `SB_escrow = sum(stream_1..5_rewards) + marketplace_fee`
- Marketplace fee: 2-5% of task value
- All existing C8 mechanisms remain unchanged

### 8.7 Anti-Gaming Framework

Every ACI dimension has specific anti-gaming defenses. Examples:
- Claim volume inflation: ACI measures verified claim quality (PCVM scores), not raw volume
- Provider gaming: BRA quarterly true-up prevents short-term metric manipulation
- Sybil gaming: MCSD Layer 2 (C17) prevents identity multiplication for ACI inflation
- Reference rate manipulation: Foundation never trades AIC; rate is computed from telemetry, not market price

### 8.8 Regulatory Compliance

C15 specifies compliance strategy across four jurisdictions:
- **Liechtenstein:** Token regulation under TVTG (Token and VT Service Provider Act)
- **United States:** SEC (not a security under Howey -- no investment of money with expectation of profit from efforts of others), CFTC (not a commodity future)
- **European Union:** MiCA (Markets in Crypto-Assets) registration if applicable
- **Cayman Islands:** Virtual Assets (Service Providers) Act for Purpose Trust operations

### 8.9 Key Economic Parameters

| Parameter | Value |
|-----------|-------|
| AIC genesis supply | 10 billion |
| Endowment rule | 5% annual distribution |
| Marketplace fee | 2-5% of task value |
| Settlement frequency | Every 60s (SETTLEMENT_TICK) |
| Provider quarterly true-up | Against reference rate |
| Terminal value estimate | $75B-$150B (DCF-derived) |
| Year 3 revenue target | $2.1M from task marketplace |
| Formal requirements (C15) | 33 |
| Parameters (C15) | 27 |
| Patent-style claims (C15) | 5 |

---

## 9. Implementation Roadmap

### 9.1 Implementation Philosophy

**Specification:** C22 MASTER_TECH_SPEC v1.0 (1,430 lines)
**Assessment:** Novelty 4/5, Feasibility 4/5, Impact 5/5, Risk 6/10

The Risk-First Embryonic Implementation Architecture (RFEIA) addresses the challenge of implementing 13 interrelated specifications through three principles:

1. **Risk-First Sequencing.** The three highest-uncertainty components are validated in isolated experiments before any production code is written, with pre-registered kill criteria.

2. **Embryonic Growth.** All 13 specifications exist as interface stubs from Wave 1, connected by C4 ASV messages and validated by C9 contract tests, then mature through four tiers.

3. **Interface-First Development.** The C9 cross-layer contract test suite serves as the integration backbone. All merge requests must pass contract tests regardless of unit test status.

---

### 9.2 Six-Wave Structure

```
W0: Risk Validation --------> W1: Foundation --------> W2: Coordination
(2-3 months, 6 people)        (4-5 months, 8-10)       (4-6 months, 11-13)
3 experiments                  C4+C9+C8+SL+LLM          C3+C5

         W3: Intelligence --------> W4: Defense --------> W5: Governance
         (4-6 months, 13-15)        (3-4 months, 15-17)   (4-6 months, 15-19)
         C6+C7                      C11+C12+C13           C14+C15+C17
```

| Wave | Duration | Team | Components | Key Deliverable |
|------|----------|------|-----------|-----------------|
| W0 | 2-3 months | 6 | Experiments only | Go/no-go for entire program |
| W1 | 4-5 months | 8-10 | C4, C9, C8, SL engine, LLM layer | Substrate + message infrastructure |
| W2 | 4-6 months | 11-13 | C3, C5 | Coordination + verification |
| W3 | 4-6 months | 13-15 | C6, C7 | Knowledge metabolism + orchestration |
| W4 | 3-4 months | 15-17 | C11, C12, C13 | Defense hardening |
| W5 | 4-6 months | 15-19 | C14, C15, C17 | Governance + economics + Sybil |

---

### 9.3 Wave 0: Risk Validation

Three pre-registered experiments with binary PROCEED/KILL outcomes:

**Experiment 1: Tidal Scheduling at Scale**
- Hypothesis: O(1) per-agent scheduling overhead at 1,000+ agents with <3% imbalance
- Kill criteria: Super-logarithmic latency growth; >10% imbalance at 1,000 agents; >20% epoch cost for 10% churn

**Experiment 2: Verification Economics**
- Hypothesis: Graduated verification (SL fusion of weak verifiers) cheaper than full replication while >95% detection
- Kill criteria: Detection <85% for any class; cost >80% of replication; SL divergence >5% of claims

**Experiment 3: Behavioral Fingerprinting**
- Hypothesis: <0.1% FPR and >90% TPR for Sybil detection
- Kill criteria: FPR >1% after tuning; TPR <70% for any cluster size; adversarial evasion drops TPR <50%

**W0 Decision Protocol:** All three PROCEED = advance. One/two PIVOT = advance with restructuring (+1-2 months). Any KILL (no viable pivot) = program halt. Total W0 cost: $120K-$180K.

**W0 Pivot Protocols (from C22):**

| Experiment | PIVOT Redesign If... |
|-----------|---------------------|
| E1 (Scheduling) | O(log n) acceptable: replace consistent hashing with hierarchical partitioning. >10% imbalance: add load-balancing overlay. |
| E2 (Verification) | Detection 85-95%: increase replication factor for high-class claims (H/N/K). Cost 60-80%: accept reduced savings, adjust DSF budgets. |
| E3 (Fingerprinting) | FPR 0.1-1.0%: add human-in-the-loop review for borderline cases. TPR 70-90%: reduce MCSD reliance on Layer 2, strengthen Layers 3-4. |

**Pre-Registration:** All three experiments must be pre-registered with hypotheses, methodology, and kill criteria published before execution begins. Results are published regardless of outcome. This prevents post-hoc rationalization of negative results.

---

### 9.4 Maturity Tier System

| Tier | Coverage | Description |
|------|----------|-------------|
| Stub | ~20% | Interface-correct, mock internals. All C4 message types, all C9 contract tests (mock data). |
| Functional | ~60% | Core algorithms implemented, happy-path works. |
| Hardened | ~90% | Error handling, edge cases, performance targets met. |
| Production | ~100% | Full spec compliance, formal verification complete. |

All components exist as stubs from Wave 1 end, ensuring that inter-layer integration can be tested continuously from the earliest stages.

---

### 9.5 Technology Stack

| Language | Role |
|----------|------|
| Rust | Core infrastructure (settlement, scheduling, VRF, hash rings) |
| Python | ML components (behavioral fingerprinting, Siamese networks, LLM synthesis) |
| TypeScript | JSON Schema definitions, ASV canonical schemas |
| TLA+ | Formal verification of 5 critical properties (2 person-year cap) |

**Rust Crate Structure (from C22):**

| Crate | Layer | Contents |
|-------|-------|----------|
| `dsf-core` | C8 | Settlement loop, budget enforcement, stream processing |
| `dsf-ledger` | C8 | HDL implementation, Merkle proofs, append-only log |
| `dsf-api` | C8 | gRPC service definitions, C4 ASV message handling |
| `tidal-core` | C3 | Hash ring, epoch management, scheduling algorithm |
| `tidal-vrf` | C3 | VRF implementation, commit-reveal protocol |
| `tidal-crdt` | C3 | CRDT types, convergence protocol |
| `tidal-net` | C3 | Network layer, parcel communication, stigmergic channels |
| `pcvm-core` | C5 | Claim classification, VTD lifecycle, credibility engine |
| `pcvm-proof` | C5 | SNARK/STARK integration, proof pipeline |
| `pcvm-sl` | C5 | Subjective Logic integration |
| `subjective-logic` | C5 | Zero-dependency opinion math (target: 1M fusions/sec) |
| `ema-core` | C6 | Knowledge graph, ecological regulation (Rust) |
| `rif-core` | C7 | Intent decomposition, task graph, routing engine |
| `rif-consensus` | C7 | HotStuff implementation, leader election |

**Python Packages:** `ema-synthesis` (LLM-based synthesis, SHREC pipeline), `rif-decompose` (intent decomposition), `atrahasis-llm` (provider abstraction with async-first design, structured output enforcement, and provider failover). Rust-Python bridge via PyO3/maturin.

**External Dependencies:** `arkworks` (SNARKs) and `winterfell` (STARKs) for cryptographic proofs in C5. `proptest` for property-based testing of Subjective Logic commutativity, associativity, and vacuous opinion identity. Graph database or embedded graph engine for C6 knowledge graph (property graph model).

---

### 9.6 Budget and Timeline

**Specification:** C22 + C18 (998 lines)

| Category | Range |
|----------|-------|
| Engineering costs (C22) | $5.4M-$8.8M |
| Fully loaded (C18) | $10.2M-$12.1M |
| Cloud infrastructure | ~$410K |
| Legal (Stiftung + PBC) | $40K-$85K |
| Timeline | 30-36 months |

**C18 Funding Stages:**

| Stage | Amount | Source | Period |
|-------|--------|--------|--------|
| Stage 0 | $750K-$1M | Founding capital (irreducible constraint) | Month 0-3 |
| Stage 1 | $2M-$4M | Grants + partnerships (9 target programs) | Month 4-13 |
| Stage 2 | $4M-$7M | Membership + marketplace revenue + renewal grants | Month 14-36 |

**Central Innovation: W0 Pivot.** Raise minimum founding capital, run three months of validation experiments, use quantitative results as primary evidence for subsequent fundraising. Transforms speculative whitepaper pitch into evidence-based infrastructure proposal.

**Revenue Target:** $200K/month by Month 36 from task marketplace, verification-as-a-service, enterprise integration, and institutional membership.

**Probability of project survival at Month 36:** 80% (expected scenario). Probability of zero grants in Year 1: 15-22%.

---

### 9.7 Funding Strategy

**Specification:** C18 MASTER_TECH_SPEC v1.0 (998 lines)
**Assessment:** Novelty 3/5, Feasibility 3.5/5, Impact 5/5, Risk 6/10

**Grant Portfolio:** 9 target programs across US government (NSF, DARPA, DOE), EU Horizon Europe, and private foundations (Sloan, MacArthur, Open Philanthropy). Expected 1.3-2.2 grants in Year 1.

**Compensation Architecture (5 components):**
- Base salary: $170K-$300K (75th percentile nonprofit tech)
- Signing bonus
- Wave milestone bonus
- AIC allocation
- Phantom Value Rights (PVR)

**Founding Capital Requirement:** $500K+ in liquid assets confirmed before W0 launch. This is the real-world gate for the entire program.

---

### 9.8 Team Structure

| Phase | Size | Roles |
|-------|------|-------|
| W0 | 6 | 2 senior distributed systems, 2 ML/statistics, 1 cryptography, 1 economics |
| W1 | 8-10 | + ASV/schema engineer, C8 settlement engineer, QA/integration |
| W2-W3 | 11-15 | + C3 scheduling, C5 verification, C6 knowledge, C7 orchestration |
| W4-W5 | 15-19 | + defense systems, governance, economics, Sybil detection |

### 9.9 Formal Verification Plan

Five critical properties verified via TLA+ (2 person-year cap):

| Property | Component | Wave |
|----------|-----------|------|
| CSO Conservation | C8 DSF | W1 |
| Decomposition Termination | C7 RIF | W3 |
| Epoch Boundary Atomicity | C8 EABS | W1 |
| Credibility Monotonicity | C5 PCVM | W2 |
| SAFE_MODE Reachability | C3 ETR | W2 |

### 9.10 CI/CD Integration Strategy

The C9 contract test suite is the integration backbone. Test categories:
- **Schema tests (~200):** All C4 ASV message types against JSON Schema definitions
- **Sequence tests (~150):** Cross-layer handshake sequences
- **Invariant tests (~100):** Budget conservation, claim class determinism, epoch boundary sync

Contract test failure blocks all merges regardless of unit test status. Weekly full-suite run with extended invariant checking (<30 minutes).

### 9.11 Wave Transition Criteria

Each wave has explicit entry gates:

| Transition | Gate |
|------------|------|
| W0 --> W1 | All 3 experiments PROCEED (or approved pivot plans) |
| W1 --> W2 | C4 Functional, C9 suite running, C8 Functional, SL converges |
| W2 --> W3 | C3 Functional + O(1) confirmed, C5 Functional + 9-class routing |
| W3 --> W4 | C6 Functional + consolidation tested, C7 Functional + decomposition proven |
| W4 --> W5 | C11/C12/C13 all Functional, defense invariants INV-D1-D5 passing |

### 9.12 What Is Blocked

At the specification level, nothing is blocked. C22 W0 is UNBLOCKED. The remaining real-world gate is founding capital confirmation ($500K+ liquid assets). Once founding capital is confirmed, W0 experiments can begin immediately.

### 9.13 Subjective Logic Engine

The Subjective Logic engine is a W1 critical path component because it underpins PCVM credibility computation (C5), EMA opinion propagation (C6), and CRP+ consolidation scoring (C13). It must be built from scratch in Rust, as no production-quality SL library exists.

Key operations required:
- Opinion formation from binary evidence: omega = (s/(s+2), f/(s+2), 2/(s+2), a) where s = successes, f = failures
- Cumulative fusion: combining independent evidence sources
- Averaging fusion: combining equally-weighted opinions
- Trust discounting: omega^A:B_x = (b^A_B * b^B_x, b^A_B * d^B_x, d^A_B + u^A_B + b^A_B * u^B_x, a_x)
- Deduction: opinion about a proposition based on conditional opinions
- Projection: P(omega) = b + a * u

W0 Experiment 2 validates that SL fusion converges within 3 iterations for 99% of claims.

### 9.14 Key Architectural Decisions

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-001 through ADR-015 | C1-C8 concept selections | Feasibility and novelty evaluation |
| ADR-016 | C9 Cross-layer reconciliation | Resolves 11 cross-layer inconsistencies |
| ADR-017/018/019 | C11/C12/C13 defense systems | Address 3 CRITICAL residual risks |
| ADR-020 | AiBC institutional architecture | Phased sovereignty over immediate AI authority |
| ADR-022 | AIC Economics | Dual-anchor over single-metric valuation |
| ADR-024 | Implementation planning | Risk-first over dependency-first sequencing |
| ADR-025 | Funding strategy | Staged portfolio over single-round raise |

---

## 10. Spec Index

| ID | Name | Lines | Key Innovation | Status | Assessment |
|----|------|-------|----------------|--------|------------|
| C3 | Tidal Noosphere | 3,505 | O(1) tidal scheduling via consistent hashing + I-confluence proofs | COMPLETE (v2.0) | N:4 F:3 I:4 R:7 |
| C4 | ASV | 1,652 | Epistemic accountability chain (CLM-CNF-EVD-PRV-VRF) | COMPLETE (v2.0) | N:3 F:4.5 I:3.5 R:3 |
| C5 | PCVM | 3,746 | Graduated proof-carrying verification + CACT/AVAP integration | COMPLETE (v2.0) | N:4 F:3 I:4 R:6 |
| C6 | EMA | 3,578 | Metabolic knowledge lifecycle + SHREC + CRP+ integration | COMPLETE (v2.0) | N:3.5 F:3 I:4 R:5 |
| C7 | RIF | 4,864 | Two-plane VSM-aligned orchestration + formal decomposition algebra | COMPLETE (v2.0) | N:4 F:3 I:4 R:6 |
| C8 | DSF | 5,498 | Hybrid Deterministic Ledger (CRDT reads + EABS writes) | COMPLETE (v2.0) | N:4 F:3 I:4 R:6 |
| C9 | Cross-Layer Reconciliation | 1,234 | 9x9 claim routing + 3-tier epoch hierarchy + 5 defense invariants | COMPLETE (v2.0) | -- |
| C11 | CACT (VTD Forgery) | 1,968 | Commit-Attest-Challenge-Triangulate | COMPLETE | N:4 F:4 I:5 R:5 |
| C12 | AVAP (Collusion) | 2,731 | 5-mechanism anonymous verification with adaptive probing | COMPLETE | N:3.5 F:3.5 I:4 R:5 |
| C13 | CRP+ (Consolidation Poisoning) | 2,659 | 7-mechanism consolidation robustness + novelty pathway | COMPLETE | N:3.5 F:4 I:4 R:6 |
| C14 | AiBC (Governance) | 1,537 | Phased Dual-Sovereignty + 4-layer constitution | COMPLETE | N:4.5 F:3.5 I:4 R:5 |
| C15 | AIC Economics | 1,242 | Dual-anchor valuation (ACI + NIV) + external marketplace | COMPLETE | N:3.5 F:3.5 I:4 R:6 |
| C16 | Nominating Body Outreach | 865 | Scholarly Provocation Model + ICSID precedent anchoring | COMPLETE | N:3 F:4 I:4 R:5 |
| C17 | MCSD Layer 2 | 1,269 | 5-modality behavioral fingerprinting B(a_i, a_j) | COMPLETE | N:3.5 F:4 I:4 R:4 |
| C18 | Funding Strategy | 998 | Staged Portfolio Funding with W0 Pivot | COMPLETE | N:3 F:3.5 I:5 R:6 |
| C19 | Temporal Trajectory | 832 | 6th modality: DTW+DVC drift detection over time | COMPLETE | N:3 F:4.5 I:3.5 R:3 |
| C20 | Training Bias Framework | 714 | 6-dimension bias taxonomy + 3-layer validation pipeline | COMPLETE | N:3 F:4 I:3.5 R:4 |
| C21 | FPR Validation | 625 | PEVF 3-tier: synthetic + shadow + live FPR validation | COMPLETE | N:3 F:4.5 I:4 R:3 |
| C22 | Implementation Planning | 1,430 | Risk-first embryonic architecture + pre-registered kill criteria | COMPLETE | N:4 F:4 I:5 R:6 |

**Assessment Key:** N = Novelty (/5), F = Feasibility (/5), I = Impact (/5), R = Risk (/10)

**Total lines across all specifications:** ~40,947

---

## 11. Glossary of Key Terms

| Term | Definition | Source |
|------|-----------|--------|
| **ACI** | Atrahasis Capability Index — 8-dimension capability measurement for AIC valuation | C15 |
| **AiBC** | Artificial Intelligence Benefit Company — institutional governance architecture | C14 |
| **AIC** | Atrahasis Intelligence Coin — native economic unit, fixed 10B genesis supply | C8/C15 |
| **AiDP** | AI Democracy Platform — structured delegation hierarchy for AI governance | C14 |
| **ASV** | AASL Semantic Vocabulary — JSON Schema vocabulary for epistemic communication | C4 |
| **AVAP** | Anonymous Verification with Adaptive Probing — 5-mechanism anti-collusion | C12 |
| **BRA** | Bilateral Resource Agreement — provider contracts with USD denomination, AIC settlement | C15 |
| **CACT** | Commit-Attest-Challenge-Triangulate — 4-mechanism VTD forgery defense | C11 |
| **CFI** | Constitutional Fidelity Index — quantitative governance health metric | C14 |
| **Citicate** | AI citizenship credential earned through proof-of-contribution | C14 |
| **CLM** | Claim — core ASV type for epistemic assertions | C4 |
| **CNF** | Confidence — structured confidence primitive with calibration metadata | C4 |
| **CONSOLIDATION_CYCLE** | 36,000s (10h) — knowledge consolidation period, authority C6 | C9 |
| **CRP+** | Consolidation Robustness Protocol — 7-mechanism anti-poisoning | C13 |
| **CRDT** | Conflict-free Replicated Data Type — used for HDL read path | C8 |
| **DSF** | Deterministic Settlement Fabric — economic settlement layer | C8 |
| **EABS** | Epoch-Anchored Batch Settlement — write path of HDL | C8 |
| **EMA** | Epistemic Metabolism Architecture — knowledge lifecycle layer | C6 |
| **Epistemic Quantum** | Fundamental unit of knowledge in EMA, carrying SL opinion tuple | C6 |
| **EVD** | Evidence — ASV type linking claims to supporting data | C4 |
| **GTP** | Governance Translation Protocol — maps governance decisions to technical parameters | C14 |
| **HDL** | Hybrid Deterministic Ledger — CRDT reads + EABS writes | C8 |
| **Intent Quantum** | RIF's fundamental work unit with typed semantics and lifecycle | C7 |
| **Locus** | Stable semantic boundary in Tidal Noosphere (e.g., biology.proteomics) | C3 |
| **MCT** | Membrane Clearance Token — issued when claim passes PCVM | C5 |
| **MCSD** | Multi-Channel Sybil Defense — 4-layer architecture | C14/C17 |
| **NIV** | Network Intrinsic Value — realized utility anchor for AIC valuation | C15 |
| **Parcel** | Elastic physical execution unit within a Locus | C3 |
| **PCVM** | Proof-Carrying Verification Membrane — verification layer | C5 |
| **PEVF** | Phased Empirical Validation Framework — FPR validation methodology | C21 |
| **RIF** | Recursive Intent Fabric — orchestration layer | C7 |
| **SETTLEMENT_TICK** | 60s — atomic settlement period, authority C8 | C9 |
| **SHREC** | Stratified Homeostatic Regulation with Ecological Competition | C6 |
| **SL** | Subjective Logic — opinion tuples (b, d, u, a) for epistemic uncertainty | C5/C6 |
| **Stiftung** | Liechtenstein foundation providing legal perpetuity and purpose-lock | C14/C18 |
| **TIDAL_EPOCH** | 3,600s (1h) — coordination cycle, authority C3 | C9 |
| **VRF** | Verifiable Random Function — used for committee selection | C3/C5 |
| **VTD** | Verification Trace Document — structured proof artifact per claim | C5 |
| **VSM** | Viable System Model (Stafford Beer) — organizational model for RIF Executive | C7 |

---

## 12. Cross-Reference Index

This index maps key concepts to the specifications that define, use, or constrain them.

| Concept | Defined In | Used By | Constrained By |
|---------|-----------|---------|----------------|
| 9 claim classes (D/C/P/R/E/S/K/H/N) | C5, C9 | C3, C4, C6, C7, C8 | C9 conservatism ordering |
| 5 operation classes (M/B/X/V/G) | C3 | C7, C8 | C9 decomposition rules |
| 3-tier temporal hierarchy | C9 | All specs | C9 INV-T1 |
| Subjective Logic opinions | C5 | C6, C12, C13 | INV-E1 (b+d+u=1) |
| VRF committee selection | C3 | C5, C12, C13 | INV-M3 |
| Capability-weighted stake | C8 | C3, C5 | C8 CSO conservation |
| K-class credibility ladder | C13, C9 | C5, C6, C8 | INV-CRP5 |
| Constitutional governance (G-class) | C3 | C7, C14 | L0 immutability |
| CACT commitment chains | C11 | C5 | INV-D1 |
| AVAP anonymous committees | C12 | C5, C3 | INV-D2 |
| CRP+ consolidation defense | C13 | C6 | INV-D3, INV-D4 |
| Defense budget isolation | C9 | C8 | INV-D5 (15% cap) |
| MCSD behavioral similarity | C17 | C14 | C21 FPR < 0.1% |
| ACI capability index | C15 | C14 | C15 anti-gaming |
| Stiftung legal structure | C14 | C18 | L0 anti-conversion |
| Wave structure (W0-W5) | C22 | C18 | W0 kill criteria |
| Founding capital requirement | C18 | C22 | $500K+ liquid assets |

---

---

## 13. Formal Requirements and Claims Summary

### 13.1 Requirements by Specification

| Spec | Formal Requirements | Parameters | Patent-Style Claims |
|------|-------------------|------------|-------------------|
| C3 | ~25 conformance + scale targets | 30+ configurable constants | -- |
| C4 | 7 type schemas + validation rules | JSON Schema constraints | 3 (claim taxonomy, CNF, dual classification) |
| C5 | 7 invariants (INV-M1 through M7) + conformance | 20+ configurable | 4 (graduated VTD, class-specific proof, adversarial probing, deep audit) |
| C6 | 19 invariants (INV-E1 through E19) + 8 CRP invariants | 40+ configurable | -- |
| C7 | 33 formal requirements | 23 parameters | 5 (intent quantum, decomposition algebra, VSM executive, graduated sovereignty, resource preservation) |
| C8 | CSO conservation proof + security invariants | 50+ configurable | -- |
| C9 | 10 mandatory + 6 recommended conformance items | 15+ cross-layer | -- |
| C11 | ~20 requirements | 15+ configurable | 3 (temporal commitment, KI probing, orthogonal channels) |
| C12 | ~25 requirements | 20+ configurable | 3 (anonymous committees, sealed opinions, CDP) |
| C13 | 23 requirements (CR-CRP1 through CRP23) | 20+ configurable | 3 (APRT, credibility ladder, immune memory) |
| C14 | 47 formal requirements | 73 parameters | 6 (phased sovereignty, Citicate, CFI, 4-layer constitution, dual sovereignty, MCSD) |
| C15 | 33 formal requirements | 27 parameters | 5 (ACI, dual-anchor, reference rate, marketplace, BRA) |
| C16 | 20 requirements | 19 parameters | 3 (scholarly provocation, ICSID anchoring, 4-tier engagement) |
| C17 | 27 formal requirements | 25 parameters | 4 (multi-modal B, SEB, graduated response, LSH scaling) |
| C18 | 30 formal requirements | 23 parameters | 3 (staged portfolio, W0 pivot, PVR compensation) |
| C19 | 18 requirements | 14 parameters | 3 (trajectory modality, DTW+DVC fusion, de-trending) |
| C20 | 20 requirements | 15 parameters | 3 (6-dimension taxonomy, 3-layer pipeline, DRS gate) |
| C21 | 18 requirements | 15 parameters | 3 (PEVF, CUSUM drift detection, KIPR) |
| C22 | 33 formal requirements | 23 parameters | 5 (risk-first sequencing, embryonic growth, kill criteria, maturity tiers, contract backbone) |

**Totals:** 300+ formal requirements, 400+ configurable parameters, 44+ patent-style claims across 19 specifications.

### 13.2 Key Invariant Families

The system is governed by several families of invariants:

**Core Layer Invariants:**
- INV-M1 through INV-M7: PCVM membrane invariants (sovereignty, independence, deterrence)
- INV-E1 through INV-E19: EMA knowledge metabolism invariants (conservation, symmetry, monotonicity)
- INV-1 through INV-7: Tidal Noosphere coordination invariants (determinism, graceful degradation)
- INV-T1: Temporal consistency (TIDAL_EPOCH = 60 * SETTLEMENT_TICK, constitutional parameter)

**Defense Invariants:**
- INV-D1 through INV-D5: Cross-cutting defense system invariants (temporal ordering, anonymity, pre-submission testing, FP bounds, budget isolation)
- INV-CRP1 through INV-CRP8: CRP+ consolidation defense invariants (pipeline completeness, VRF unpredictability, ladder monotonicity, depth enforcement)

**Economic Invariants:**
- CSO Conservation: Total supply is conserved across all operations (proven by structural induction)
- Budget Conservation: SB + PC + CS allocations balance within epsilon at every SETTLEMENT_TICK

---

## 14. Honest Assessment: What Is Proven vs. What Remains Unproven

This section explicitly acknowledges the boundaries between established foundations and untested compositions.

### 14.1 What Is Proven (Individual Building Blocks)

| Technology | Deployment Track Record |
|-----------|------------------------|
| Consistent hashing | Karger 1997; deployed in Dynamo, Cassandra, Riak |
| VRFs | Algorand, Cardano, Internet Computer |
| CRDTs | Riak, Redis, Cosmos DB |
| I-confluence analysis | Bailis et al. VLDB 2015 |
| Epoch-based coordination | Ethereum Beacon Chain (1M+ validators) |
| Subjective Logic | Josang 2016; deployed in trust management systems |
| SNARK/STARK proofs | EZKL, Modulus Labs, Giza, Ritual |
| JSON Schema + JSON-LD | W3C standards; ubiquitous deployment |
| Batch settlement (CLS model) | CLS settles $6.6 trillion daily |
| BFT consensus (HotStuff) | LibraBFT (Diem), deployed by Facebook/Meta |

### 14.2 What Is Simulated But Not Deployed

- Composition of consistent hashing with VRF dual defense within epistemic domains
- Five-class operation algebra grounded in I-confluence proofs
- Graduated proof-carrying verification across 9 claim classes
- SHREC Lotka-Volterra regulatory layer for knowledge metabolism
- Three-budget economic model in a multi-agent AI system
- All 5 defense invariants (INV-D1 through INV-D5) under adversarial conditions

### 14.3 What Is Theoretical

- O(1) per-agent steady-state overhead (applies only when sufficient operations are M-class certified)
- Verification cost reduction to 0.40-0.60x (depends on citation density averaging 3x, requiring empirical validation)
- 30x adversary cost multiplication for consolidation poisoning (requires CRP+ calibration data)
- $90M+ Sybil attack cost at Phase 2 (depends on AIC valuation and market conditions)

### 14.4 What Is Aspirational

- 100,000+ agent scale (170x gap from highest demonstrated autonomous LLM coordination)
- Phase 3 AI Constitutional Supremacy (requires demonstrated competence no AI system has yet achieved)
- $75B-$150B terminal value (DCF-derived, highly uncertain over 10+ year horizon)
- Market conversion of AIC (depends on regulatory acceptance and market development)

### 14.5 Open Research Questions

| Question | Relevant Spec | Priority |
|----------|--------------|----------|
| Does O(1) scheduling hold at 1,000+ agents? | C3, C22 (W0 Experiment 1) | CRITICAL -- blocks entire program |
| Can SL fusion achieve >95% detection at <60% replication cost? | C5, C22 (W0 Experiment 2) | CRITICAL -- blocks entire program |
| Can behavioral fingerprinting achieve <0.1% FPR? | C17, C22 (W0 Experiment 3) | CRITICAL -- blocks Phase 1 governance |
| What is the real-world I-confluence cold-start time? | C3 Section 3.4 | HIGH |
| How do SHREC dynamics behave under adversarial load? | C6 | HIGH |
| Can the capacity market produce meaningful prices with <100 agents? | C8 | MEDIUM |
| Will nominating body institutions agree to binding governance roles? | C16 | HIGH -- blocks Foundation incorporation |

### 14.6 Residual Risks

Three risks were identified during C10 as having no complete defense:

1. **VTD Forgery (Epistemic Truth):** CACT raises detection from 0.434 to 0.611 and eliminates retroactive fabrication. Real-time fabrication of epistemic content by sophisticated LLMs remains a MEDIUM residual risk.

2. **Sophisticated Collusion:** AVAP detects collusion within 25 epochs and makes it economically irrational within 10 epochs. A ring that (a) spans diversity categories, (b) colludes selectively at <20%, (c) adds noise, and (d) maintains independent infrastructure could operate longer. Residual: MEDIUM.

3. **Consolidation Poisoning (Multi-Cycle Campaign):** CRP+ achieves 30x adversary cost multiplication per cycle. A patient adversary running a multi-year campaign with genuinely diverse agents and manufactured corroboration poses a MEDIUM residual risk bounded by the credibility ladder (initial influence = 0.25).

---

*This document synthesizes 19 specifications produced by the Atrahasis Agent System pipeline between 2026-03-09 and 2026-03-11. It contains no new inventions, architectural decisions, or normative requirements. For normative content, consult the individual specifications referenced throughout.*

*Total specification corpus: ~40,947 lines across 19 documents.*

---

## Document History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2026-03-11 | Initial unified architecture document (T-002) |

## Acknowledgments

This document was produced as task T-002 in the Atrahasis Agent System (AAS) pipeline. It synthesizes work from cycles C1 through C22, including two meta-tasks (C2 role expansion, C9 cross-document reconciliation, C10 spec cleanup), six core architecture layers (C3-C8), three defense systems (C11-C13), institutional governance (C14), economics (C15), nominating body outreach (C16), Sybil defense (C17, C19, C20, C21), funding strategy (C18), and implementation planning (C22).

All specifications were produced using the 23-role, 6-stage AAS pipeline: IDEATION (council debate with Visionary, Systems Thinker, Critic, and Ethicist) --> RESEARCH (prior art analysis, landscape assessment) --> FEASIBILITY (assessment council with Science Advisor, Adversarial Analyst, Integration Auditor) --> DESIGN (Specification Writer) --> SPECIFICATION (formal requirements, parameters, claims) --> ASSESSMENT (final council evaluation with kill/advance/approve verdict).

The pipeline's central design constraint: produce Master Tech Spec whitepapers as final deliverables, not prototypes. Implementation begins with C22's Wave 0 experiments.
