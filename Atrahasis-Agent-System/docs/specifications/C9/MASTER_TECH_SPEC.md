# Cross-Layer Reconciliation Addendum

**Version:** 2.0.0
**Date:** 2026-03-10
**Status:** SPECIFICATION
**Authority:** This document is the canonical cross-layer integration specification for the Atrahasis architecture stack. Where layer-specific Master Tech Specs (C3-C8) conflict with this document on cross-layer matters, this document takes precedence. Where defense-system specs (C11-C13) conflict with this document on cross-layer integration matters, this document takes precedence on integration contracts; individual defense specs retain authority over their internal mechanisms.

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Architecture Stack Overview](#2-architecture-stack-overview)
3. [Canonical Temporal Hierarchy](#3-canonical-temporal-hierarchy)
4. [Canonical Claim Class Taxonomy](#4-canonical-claim-class-taxonomy)
5. [Operation Class Algebra](#5-operation-class-algebra)
6. [ASV Integration Mapping](#6-asv-integration-mapping)
7. [Settlement Integration](#7-settlement-integration)
8. [Cross-Layer Type Registry](#8-cross-layer-type-registry)
9. [Integration Contract Directory](#9-integration-contract-directory)
10. [Errata to Existing Specifications](#10-errata-to-existing-specifications)
11. [Invariants](#11-invariants)
12. [Conformance Requirements](#12-conformance-requirements)

Appendices:
- A: [Claim Class Quick Reference](#appendix-a-claim-class-quick-reference)
- B: [Epoch Hierarchy Derivation Proof](#appendix-b-epoch-hierarchy-derivation-proof)
- C: [Configurable Parameters](#appendix-c-configurable-parameters)
- D: [Glossary](#appendix-d-glossary)
- E: [Defense System Integration Map](#appendix-e-defense-system-integration-map)
- F: [Changelog](#appendix-f-changelog)

---

## 1. Purpose and Scope

### 1.1 Purpose

The Atrahasis architecture consists of six layers, each specified independently as a Master Tech Spec (C3 through C8). These specifications were produced sequentially through the Atrahasis Agent System (AAS) pipeline, with each later layer informed by but not formally constrained by earlier layers.

This document resolves the cross-layer inconsistencies identified by a systematic reconciliation scan (C9) and establishes the canonical integration specification that bridges all six layers.

**v2.0 Extension:** Following v1.0's reconciliation of the six core layers, three defense-system specifications were produced: C11 (CACT, VTD forgery defense), C12 (AVAP, collusion defense), and C13 (CRP+, consolidation poisoning defense). These defense systems are cross-cutting -- each integrates with multiple core layers simultaneously. Version 2.0 of this addendum extends v1.0 with the canonical cross-layer integration requirements for C11, C12, and C13, ensuring that defense-system interactions with the core stack are formally specified and that no cross-layer conflicts arise from their deployment.

### 1.2 Scope

This addendum covers:
- **Temporal alignment** -- canonical epoch hierarchy across all layers
- **Claim class taxonomy** -- unified 9-class taxonomy with cross-layer mappings
- **Cross-layer type definitions** -- canonical types for inter-layer communication
- **Integration contract directory** -- summary of all bidirectional contracts
- **Errata** -- specific corrections to layer specs where inconsistencies exist
- **Defense system integration** (v2.0) -- cross-layer contracts for C11 CACT, C12 AVAP, and C13 CRP+
- **K-class extended lifecycle** (v2.0) -- graduated credibility ladder and depth limits from CRP+
- **Defense settlement flows** (v2.0) -- economic integration of defense-system operations with C8 DSF

This addendum does NOT:
- Modify internal algorithms of any layer
- Change any layer's API surface
- Override any layer's sovereignty over its own domain
- Introduce new architectural components
- Override defense-system sovereignty over their internal mechanisms (C11/C12/C13 retain authority over their own algorithms)

### 1.3 Authority Hierarchy

| Domain | Authoritative Layer | Rationale |
|--------|-------------------|-----------|
| Spatial coordination (loci, parcels, topology) | C3 | Tidal Noosphere defines the substrate |
| Communication vocabulary | C4 | ASV is the semantic layer |
| Claim verification and classification | C5 | PCVM is constitutionally sovereign |
| Knowledge metabolism | C6 | EMA owns the knowledge lifecycle |
| Intent orchestration | C7 | RIF is the orchestration layer |
| Economic settlement | C8 | DSF is the settlement authority |
| Cross-layer integration | **C9 (this document)** | Reconciliation addendum |
| VTD forgery defense | **C11** | CACT is the canonical VTD anti-forgery spec |
| Collusion defense | **C12** | AVAP is the canonical anti-collusion spec |
| Consolidation poisoning defense | **C13** | CRP+ is the canonical anti-poisoning spec |

---

## 2. Architecture Stack Overview

```
+-------------------------------------------------------------+
|  Layer 6: RIF -- Recursive Intent Fabric (C7)                |
|  Purpose: Intent decomposition, agent assignment, lifecycle   |
+-------------------------------------------------------------+
|  Layer 5: Tidal Noosphere (C3)                               |
|  Purpose: Coordination, CRDT state, topology, governance     |
+-------------------------------------------------------------+
|  Layer 4: PCVM -- Proof-Carrying Verification Membrane (C5)  |
|  Purpose: Claim verification, classification, credibility    |
+-------------------------------------------------------------+
|  Layer 3: EMA -- Epistemic Metabolism Architecture (C6)      |
|  Purpose: Knowledge lifecycle, consolidation, circulation    |
+-------------------------------------------------------------+
|  Layer 2: DSF -- Deterministic Settlement Fabric (C8)        |
|  Purpose: Economic settlement, budgets, capacity market      |
+-------------------------------------------------------------+
|  Layer 1: ASV -- Atrahasis Semantic Vocabulary (C4)          |
|  Purpose: Structured communication vocabulary               |
+-------------------------------------------------------------+

  CROSS-CUTTING DEFENSE SYSTEMS (v2.0):

  +---------------------------------------------------------+
  |  C11: CACT -- Commit-Attest-Challenge-Triangulate        |
  |  Scope: VTD forgery defense                              |
  |  Integrates with: C5 (VTD pipeline), C3 (VRF), C8 (econ)|
  +---------------------------------------------------------+
  |  C12: AVAP -- Anonymous Verification with Adaptive Probing|
  |  Scope: Collusion defense                                |
  |  Integrates with: C3 (VRF/Sentinel), C5 (opinions),     |
  |                   C6 (credibility cascade), C8 (slashing)|
  +---------------------------------------------------------+
  |  C13: CRP+ -- Consolidation Robustness Protocol          |
  |  Scope: Consolidation poisoning defense                  |
  |  Integrates with: C6 (dreaming), C5 (K-class VTDs),     |
  |                   C3 (VRF), C8 (credibility settlement)  |
  +---------------------------------------------------------+
```

Data flows are bidirectional between adjacent and non-adjacent layers. Defense systems are cross-cutting: they instrument existing layer pipelines without replacing any layer component. See SS9 for the complete contract directory and Appendix E for the defense system integration map.

---

## 3. Canonical Temporal Hierarchy

### 3.1 Three-Tier Epoch System

The Atrahasis stack operates on a three-tier temporal hierarchy. Each tier serves a different operational purpose:

**Definition 3.1 (Settlement Tick).** A SETTLEMENT_TICK is the fundamental settlement cycle, during which C8's Epoch-Anchored Batch Settlement (EABS) collects and processes all state-mutating economic operations. Duration: 60 seconds. Authority: C8 DSF.

**Definition 3.2 (Tidal Epoch).** A TIDAL_EPOCH is the coordination cycle, during which C3's Tidal Noosphere performs epoch-boundary operations: VRF seed rotation, hash ring reconstruction, capacity snapshots, and predictive model recalibration. Duration: 3600 seconds = 60 SETTLEMENT_TICKs. Authority: C3 Tidal Noosphere.

**Definition 3.3 (Consolidation Cycle).** A CONSOLIDATION_CYCLE is the knowledge metabolism cycle, during which C6's EMA executes its dreaming/consolidation phase. Duration: 36000 seconds = 10 TIDAL_EPOCHs = 600 SETTLEMENT_TICKs. Authority: C6 EMA.

### 3.2 Tier Relationships

```
1 CONSOLIDATION_CYCLE = 10 TIDAL_EPOCHS = 600 SETTLEMENT_TICKS = 36,000 seconds

Time ------------------------------------------------------------>

SETTLEMENT_TICKS:  |1|2|3|...|58|59|60|1|2|3|...|58|59|60|...
                   +---- TIDAL_EPOCH 1 ---++---- TIDAL_EPOCH 2 ---+
                   +------------------ CONSOLIDATION_CYCLE (partial) -
```

### 3.3 Intra-Tidal-Epoch Timeline

Within each TIDAL_EPOCH (3600s = 60 ticks):

```
Tick 1-55  (0:00 - 55:00): Normal operations
    - EABS settlement cycles (55 cycles)
    - V-class operations submitted to PCVM
    - B-class settlement rewards distributed per tick
    - C6 ingestion, circulation, catabolism
    - C11 CACT commitment chains constructed (ongoing)
    - C12 AVAP cover traffic and sealed opinion commits (ongoing)

Tick 56-58 (55:00 - 58:00): Verification finalization
    - C5 audit selection (random deep-audit at tick 56)
    - C5 verification window closes
    - V-class settlement checkpoint
    - C12 AVAP reveal phase (after submission window closes)

Tick 59    (58:00 - 59:00): Settlement reporting
    - C5 sends verification quality reports to C8
    - C6 sends metabolic efficiency reports to C8
    - C3 computes scheduling compliance scores
    - C12 AVAP committee membership revealed (post-reveal deadline)

Tick 60    (59:00 - 60:00): Epoch boundary
    - C3 BOUNDARY_WINDOW operations (5s within this tick):
      - Capacity snapshot gossip
      - Hash ring reconstruction (if roster changed)
      - VRF seed rotation
      - Predictive model recalibration
    - C8 cumulative tidal settlement computation
    - G-class governance reward distribution
    - C12 AVAP Merkle-anchored commitment batching (1 on-chain tx)
    - C13 CRP+ immune memory garbage collection (regulation phase)
```

### 3.4 Parameter Interpretation Guide

When reading existing Master Tech Specs, interpret "epoch" as follows:

| Specification | When it says "epoch" | It means |
|---------------|---------------------|----------|
| C3 | All occurrences | TIDAL_EPOCH (3600s) |
| C4 | N/A (no epoch references) | N/A |
| C5 | All occurrences | TIDAL_EPOCH (3600s) |
| C6 | "every N epochs" (consolidation) | TIDAL_EPOCH (3600s) |
| C7 | "epoch" in deadlines, staleness | TIDAL_EPOCH (3600s) |
| C7 | N/A | (C7 does not define its own epoch duration) |
| C8 | `epoch_duration_ms`, all epoch references | SETTLEMENT_TICK (60s) |
| C11 | All occurrences | TIDAL_EPOCH (3600s) |
| C12 | All occurrences | TIDAL_EPOCH (3600s) |
| C13 | "cycle" (consolidation context) | CONSOLIDATION_CYCLE (36000s) |
| C13 | "epoch" (all other contexts) | TIDAL_EPOCH (3600s) |

**INV-T1 (Temporal Consistency):** TIDAL_EPOCH = 60 x SETTLEMENT_TICK. This ratio is a constitutional parameter modifiable only through G-class governance with 90% supermajority.

---

## 4. Canonical Claim Class Taxonomy

### 4.1 Nine Canonical Classes

The Atrahasis verification system recognizes 9 claim classes, organized into 3 verification tiers. C5 (PCVM) is the authoritative classifier -- no other layer may override PCVM's class assignment.

#### Tier 1: FORMAL_PROOF (2 classes)

**D-class (Deterministic).** A claim whose truth value is decidable by deterministic computation. Verification: replay computation on stated inputs. Examples: hash computations, sorting results, mathematical calculations.

**C-class (Compliance).** A claim that a system, process, or output conforms to a specified regulation, standard, or constitutional parameter. Verification: matching against a finite rule set. Examples: EU AI Act Article 11 compliance, constitutional parameter satisfaction.

#### Tier 2: STRUCTURED_EVIDENCE (5 classes)

**P-class (Process).** A claim that a specified process was followed during the production of another claim. Verification: check execution traces against declared process specification. Examples: research protocol adherence, pipeline stage execution.

**R-class (Reasoning).** A claim derived from logical inference over premises. Verification: check logical validity, premise support, and assumption disclosure. Examples: architectural arguments, I-confluence proofs.

**E-class (Empirical).** A claim derived from observation or measurement of external phenomena. Verification: check cited sources, cross-reference, assess source reliability. Examples: benchmark scores, market data, experimental results.

**S-class (Statistical).** A claim derived from statistical analysis of data. Verification: check methodology, sample adequacy, test appropriateness, conclusion validity. Examples: load balancing efficiency, performance comparisons.

**K-class (Knowledge Consolidation).** A claim produced by EMA's consolidation (dreaming) process, synthesizing patterns across multiple epistemic quanta from diverse sources. Verification: check source quantum provenance (>=5 agents, >=3 parcels, no agent >30%), reasoning chain validity, falsification statement quality, and cross-domain coherence. K-class claims start with high uncertainty (u >= 0.4) and are subject to aging uncertainty increase without empirical validation.

#### Tier 3: STRUCTURED_ATTESTATION (2 classes)

**H-class (Heuristic).** A claim derived from expert judgment, model prediction, or pragmatic assessment. Verification: check that alternatives were considered, criteria are appropriate, no known contradictions. Examples: technology recommendations, architectural decisions.

**N-class (Normative).** A claim about values, ethics, or policy that invokes a normative framework. Verification: check constitutional alignment, stakeholder coverage, framework application consistency. Normative claims are verified for consistency and completeness, not for truth. Examples: ethical guidelines, governance policies.

### 4.2 Conservatism Ordering

When multiple classification inputs disagree, the most conservative (highest verification cost) class is selected:

```
H > N > K > E > S > R > P > C > D
```

### 4.3 Class Parameters

| Class | Letter | Tier | Committee Size | Admission Threshold | Difficulty Weight | Settlement Type | SL Base Rate (a) | SL Decay Model |
|-------|--------|------|---------------|--------------------|--------------------|-----------------|------------------|----------------|
| Deterministic | D | 1 | 3 | 0.95 | 1.0 | B-class fast | 0.5 | None (proofs don't expire) |
| Compliance | C | 1 | 3 | 0.90 | 1.3 | B-class fast | 0.5 | On regulation change |
| Process | P | 2 | 5 | 0.80 | 1.5 | B-class fast | 0.5 | On process spec change |
| Reasoning | R | 2 | 5 | 0.75 | 2.0 | V-class standard | 0.5 | On premise change |
| Empirical | E | 2 | 5 | 0.60 | 1.5 | V-class standard | 0.5 | Half-life 90-365 days |
| Statistical | S | 2 | 5 | 0.65 | 2.0 | V-class standard | 0.5 | On new data availability |
| Knowledge Consolidation | K | 2 | 5 | 0.70 | 1.8 | V-class standard | 0.6 | Half-life 120 days |
| Heuristic | H | 3 | 7 | 0.50 | 2.5 | V-class standard | 0.7 | Half-life 180 days |
| Normative | N | 3 | 7 | 0.50 | 3.0 | G-class slow | 0.5 | On constitutional amendment |

### 4.4 K-Class VTD Requirements

A K-class Verification Trace Document (VTD) must include:

```yaml
K-Class VTD:
  claim_text:           string          # The consolidated claim
  claim_class:          "K"             # Knowledge Consolidation
  source_quanta:        List<QuantumID> # Minimum 5 quanta
  source_agents:        List<AgentID>   # Minimum from 3 distinct parcels
  agent_concentration:  float           # Max any single agent: 0.30
  synthesis_reasoning:  string          # LLM reasoning chain
  falsification_statement: string       # How this claim could be disproven
  voting_record:        VotingRecord    # 3-pass majority (per C6 CR-13)
  initial_opinion:      SLOpinion       # (b, d, u, a) with u >= 0.4, a = 0.6
  consolidation_cycle:  uint64          # Which cycle produced this
```

### 4.5 Aging Uncertainty for K-Class

K-class claims without empirical validation are subject to aging uncertainty increase:

```
aging_rate_k = 0.005 per TIDAL_EPOCH (per C6 Adversarial A2 mitigation)

IF tidal_epochs_since_creation > 100 AND NOT empirically_validated:
    u_new = min(u + aging_rate_k, 0.95)
    b_new = b * (1 - aging_rate_k / (1 - u))
    d unchanged
    Renormalize: b + d + u = 1
```

### 4.6 K-Class Extended Lifecycle: Graduated Credibility Ladder (v2.0, CRP+ Integration)

C13 CRP+ introduces a 5-rung graduated credibility system for K-class claims that replaces the binary PENDING_VALIDATION / VALIDATED model from C10 Layer 5. This section establishes the canonical cross-layer definition of the credibility ladder.

#### 4.6.1 Rung Definitions

| Rung | Name | Uncertainty Floor | Influence Weight | Entry Condition |
|------|------|-------------------|------------------|-----------------|
| 0 | SPECULATIVE | u >= 0.80 | 0.00 | Product of sandboxed K->K consolidation (M6). Cannot promote directly. |
| 1 | PROVISIONAL | u >= 0.50 | 0.25 | Default for all K-class from standard dreaming consolidation. |
| 2 | CORROBORATED | u >= 0.30 | 0.50 | >= 1 DIRECT E-class corroboration from independent agent (different agent, different Sentinel cluster, created after the K-class claim). |
| 3 | ESTABLISHED | u >= 0.15 | 0.75 | >= 3 corroborations including >= 1 from a different parcel + >= 50 epochs at CORROBORATED without failed challenges. |
| 4 | CANONICAL | u >= 0.05 | 1.00 | >= 5 corroborations from >= 3 parcels + >= 200 epochs at ESTABLISHED + zero failed challenges during ESTABLISHED tenure. |

**Cross-layer implications:**
- C6 (EMA): Uncertainty floors are enforced at the EMA level. EMA must not store a K-class quantum with uncertainty below its rung floor.
- C5 (PCVM): PCVM admission of K-class claims must set initial rung to PROVISIONAL (rung 1) for standard consolidation products or SPECULATIVE (rung 0) for sandboxed K->K products. PCVM must not admit a K-class claim at a higher rung.
- C8 (DSF): Settlement rewards for K-class claims are multiplied by the influence weight of the claim's current rung. See SS7.5.
- C3 (Tidal Noosphere): Credibility rung promotion/demotion events are replicated via C3 CRDT infrastructure.

#### 4.6.2 Influence Weight Application

When a K-class quantum participates in any downstream process (further consolidation, credibility scoring, coherence graph weighting), its contribution is multiplied by its influence weight:

```
effective_contribution(q) = raw_contribution(q) * influence_weight(q.rung)
```

PROVISIONAL claims have only 25% of the influence they would otherwise have. SPECULATIVE claims have zero influence on any downstream process.

#### 4.6.3 Relationship to SS4.5 Aging Uncertainty

The SS4.5 aging uncertainty mechanism and the credibility ladder operate independently but synergistically:

- Aging uncertainty increases `u` over time for unvalidated claims (SS4.5).
- Rung uncertainty floors set a minimum `u` based on the current rung (SS4.6.1).
- The effective uncertainty is `max(aging_u, rung_floor_u)`.
- A claim that ages past its rung floor experiences no additional floor-based penalty (the aging mechanism already dominates).
- A claim that is promoted to a higher rung (lower floor) benefits from the promotion only if its aging uncertainty has not already exceeded the new floor.

#### 4.6.4 Consolidation Depth Limits (CRP+ M6)

K-class participation in further consolidation is constrained by rung:

| Rung | Participation in Consolidation | Input Weight |
|------|-------------------------------|--------------|
| SPECULATIVE (0) | EXCLUDED | 0.00 |
| PROVISIONAL (1) | EXCLUDED | 0.00 |
| CORROBORATED (2) | Allowed with reduced weight | 0.50 |
| ESTABLISHED (3) | Allowed with full weight | 1.00 |
| CANONICAL (4) | Allowed with full weight | 1.00 |

**INV-CRP5 (Depth Enforcement):** PROVISIONAL and SPECULATIVE K-class quanta MUST NOT participate in further consolidation. This is enforced at candidate identification time (C6 dreaming pipeline), before any LLM synthesis cost is incurred. Authority: C13 CRP+.

---

## 5. Operation Class Algebra

### 5.1 Canonical Definition (C3 Authority)

Five operation classes form a strict partial order: G > V > X > B > M.

| Class | Name | Communication Cost | Precondition |
|-------|------|--------------------|--------------|
| M | Merge/Convergence | Zero consensus | I-confluence proof certified |
| B | Bounded Local Commit | Zero consensus (amortized rebalancing) | CSO eligibility |
| X | Exclusive | Quorum protocol | Default for unproven operations |
| V | Verification | VRF-selected committee | Claim verification semantics |
| G | Governance | BFT constitutional consensus | Constitutional significance |

### 5.2 Decomposition Rules (C7 Authority)

C7 RIF enforces monotonic decomposition:

```
G -> {M, B, X, V, G}    Governance may decompose into anything
V -> {M, B, X}           Verification cannot spawn governance/verification
X -> {M, B}              Exclusive decomposes into simpler operations
B -> {M}                 Bounded decomposes only into merge reads
M -> empty               Merge operations are terminal
```

### 5.3 Settlement Type Mapping (C8 Authority)

| Operation Class | Settlement Type | Settlement Timing |
|----------------|-----------------|-------------------|
| M | B-class fast | Per SETTLEMENT_TICK |
| B | B-class fast | Per SETTLEMENT_TICK |
| X | B-class fast (V-class if disputed) | Per SETTLEMENT_TICK (or TIDAL_EPOCH if disputed) |
| V | V-class standard | Per TIDAL_EPOCH |
| G | G-class slow | Per governance action |

---

## 6. ASV Integration Mapping

### 6.1 C4 Epistemic Class -> C5 Claim Class

C4 defines 6 epistemic classes for semantic annotation. These map to C5 claim classes as follows:

| C4 `epistemic_class` | Primary C5 Class | Override Condition | Override Class |
|----------------------|------------------|-------------------|----------------|
| `observation` | E (Empirical) | Evidence quality_class = "computational_result" | D (Deterministic) |
| `correlation` | S (Statistical) | -- | -- |
| `causation` | R (Reasoning) | Evidence includes experimental/RCT data | S (Statistical) |
| `inference` | R (Reasoning) | Confidence method = "model_derived" | H (Heuristic) |
| `prediction` | H (Heuristic) | Confidence method = "statistical" with interval | S (Statistical) |
| `prescription` | N (Normative) | -- | -- |

### 6.2 Mapping Algorithm

```
FUNCTION map_c4_to_c5(clm: ASV.CLM) -> ClaimClass:
    MATCH clm.epistemic_class:
        "observation":
            IF has_evidence(clm, "computational_result"): RETURN D
            RETURN E
        "correlation":
            RETURN S
        "causation":
            IF has_evidence(clm, "computational_result"): RETURN S
            RETURN R
        "inference":
            IF clm.confidence.method == "model_derived": RETURN H
            RETURN R
        "prediction":
            IF clm.confidence.method == "statistical"
               AND clm.confidence.interval IS NOT NULL: RETURN S
            RETURN H
        "prescription":
            RETURN N

FUNCTION has_evidence(clm, quality_class) -> bool:
    RETURN any(e.quality_class == quality_class for e in clm.evidence)
```

### 6.3 ASV Token -> PCVM Intake Flow

```
C4 ASV Message:                    C5 PCVM Intake:
  CLM (claim)          ------>      Claim content + proposed class
  CLM.epistemic_class  ------>      Preliminary class (via SS6.2 mapping)
  CNF (confidence)     ------>      Initial SL opinion seed
  EVD[] (evidence)     ------>      VTD dependencies
  PRV (provenance)     ------>      VTD provenance chain
  VRF (verification)   <------      MCT output (SL opinion + final class)
```

### 6.4 ASV Extensions

C4's core 7 types (AGT, CLM, CNF, EVD, PRV, VRF, SAE) are extended by:

| Extension | Source | Purpose |
|-----------|--------|---------|
| INT claim type | C7 RIF | Intent outcome claims with intent_id, outcome, operation_class |
| TDF type | C3 | Tidal Function Definition for governance |
| TSK type | C3 | Task Stake Keep for settlement |
| SRP type | C3 | Surprise delta for predictive communication |
| STL type | C3 | Settlement publication |

---

## 7. Settlement Integration

### 7.1 Settlement Authority

C8 (DSF) is the canonical settlement authority. All economic operations flow through C8's EABS protocol.

**Correction (INC-10):** C7's Settlement Router forwards intent-related transactions to C8 DSF, not directly to C3. C3's settlement calculator is a component that feeds scheduling compliance data to C8.

### 7.2 Four-Stream Settlement

| # | Stream | Weight | Data Source | Timing |
|---|--------|--------|-------------|--------|
| 1 | Scheduling Compliance | 40% | C3 Tidal Scheduler | Per SETTLEMENT_TICK |
| 2 | Verification Quality | 40% | C5 PCVM | Per TIDAL_EPOCH |
| 3 | Communication Efficiency | 10% | C3 Predictive Channels | Per SETTLEMENT_TICK |
| 4 | Governance Participation | 10% | C3 G-Class Engine | Per governance action |

### 7.3 Claim Class -> Settlement Mapping

| Claim Class | Difficulty Weight | Settlement Type | Rationale |
|-------------|------------------|-----------------|-----------|
| D | 1.0 | B-class fast | Recomputation -- fast, cheap |
| C | 1.3 | B-class fast | Rule matching -- fast, slightly complex |
| P | 1.5 | B-class fast | Trace checking -- fast |
| E | 1.5 | V-class standard | Observation requires time |
| K | 1.8 | V-class standard | Consolidation requires multi-source verification |
| S | 2.0 | V-class standard | Sample accumulation |
| R | 2.0 | V-class standard | Logical verification |
| H | 2.5 | V-class standard | Expert review |
| N | 3.0 | G-class slow | Value judgments, governance review |

### 7.4 Capability Score (C8, unchanged)

```
effective_stake = AIC_collateral * min(1 + ln(1 + raw_score), 3.0)

raw_score = 0.4 * reputation
          + 0.4 * verification_track_record
          + 0.2 * claim_class_accuracy

claim_class_accuracy: evaluated across all 9 classes (VRF-assigned, not self-selected)
```

### 7.5 Defense System Settlement Integration (v2.0)

Defense systems C11, C12, and C13 introduce new economic flows that are settled through C8 DSF. This section canonicalizes those flows.

#### 7.5.1 CACT Staking Costs (C11 -> C8)

| Economic Event | DSF Operation | Amount | Settlement Speed | Authority |
|----------------|---------------|--------|------------------|-----------|
| Commitment chain fraud detected | `SLASH` (VERIFICATION_FRAUD Level 3) | 22.5% of stake (15% * 1.5x severity) | V-class (per TIDAL_EPOCH) | C11 SS4.6.3 |
| OVC quality bonus (OVC > 0.80) | `AIC_TRANSFER` (reward) | +10% on settlement reward | B-class (per SETTLEMENT_TICK) | C11 SS4.6.3 |
| KI failure (agent fails interrogation) | No direct slashing | Credibility adjustment only | N/A | C11 SS4.3.3 |

**Integration contract:** C11 CACT violations are routed through C5 PCVM's existing VERIFICATION_FRAUD slashing category to C8 DSF. No new slashing category is created. CACT extends the existing severity multiplier table (C8 Section 10.3.1).

#### 7.5.2 CDP Bounty Treasury (C12 -> C8)

| Economic Event | DSF Operation | Amount | Settlement Speed | Authority |
|----------------|---------------|--------|------------------|-----------|
| Ring detection confirmed | `SLASH` (collusion) | Graduated: 10%/25%/50%/100% of staked AIC | V-class | C12 SS7.6 |
| CDP report verified (bounty payout) | `AIC_TRANSFER` (bounty) | Per `compute_bounty()` formula | V-class | C12 SS7.3 |
| CDP report received (bounty escrow) | `PENDING_INITIATE` (escrow) | Bounty estimate | B-class | C12 SS7.6 |
| Investigation confirms ring | `PENDING_COMPLETE` (release) | Escrowed amount | V-class | C12 SS7.6 |
| Investigation finds false report | `PENDING_TIMEOUT` (return) | Escrowed amount returned | B-class | C12 SS7.6 |

**Bounty funding invariant:** Bounties are paid exclusively from forfeited stakes of confirmed ring members. No new AIC is created for bounty payments. If forfeited stake is insufficient, the bounty is capped at available forfeiture. Authority: C12 SS7.3.

#### 7.5.3 Enterprise Liability Slashing (C12 -> C8)

C12 AVAP defines a graduated collusion slashing schedule that extends C8 Section 10.3:

| Offense | Penalty | Cooldown | Recovery Path |
|---------|---------|----------|---------------|
| 1st honeypot-detected collusion | 10% staked AIC | 25 epochs exclusion | Clean 100 epochs |
| 2nd offense | 25% staked AIC | 50 epochs exclusion | Clean 200 epochs |
| 3rd offense | 50% staked AIC | 100 epochs exclusion | Clean 500 epochs |
| Enterprise liability (P > 0.90) | 100% forfeiture | Permanent exclusion pending appeal | G-class governance appeal |

**Cross-layer requirement:** Enterprise liability total forfeiture (100%) MUST be appealable through G-class governance vote (C3). This is the only defense-system slashing that requires governance intervention for reversal.

#### 7.5.4 Credibility-Weighted Settlement (C13 -> C8)

C13 CRP+ introduces credibility-weighted influence for K-class claims that affects settlement:

```
K_class_settlement_reward(claim) = base_reward(claim)
                                 * difficulty_weight(K)     # 1.8
                                 * influence_weight(claim.rung)
```

| Rung | Influence Weight | Effective Settlement Multiplier |
|------|-----------------|--------------------------------|
| SPECULATIVE | 0.00 | 0.00 (no settlement reward) |
| PROVISIONAL | 0.25 | 0.45 (1.8 * 0.25) |
| CORROBORATED | 0.50 | 0.90 (1.8 * 0.50) |
| ESTABLISHED | 0.75 | 1.35 (1.8 * 0.75) |
| CANONICAL | 1.00 | 1.80 (1.8 * 1.00) |

**Cross-layer requirement:** C8 DSF MUST apply the rung-based influence weight when computing settlement rewards for K-class claims. The rung is read from C6 EMA's quantum metadata (replicated via C3 CRDT infrastructure).

---

## 8. Cross-Layer Type Registry

### 8.1 Temporal Types

```
type SettlementTick    = uint64    // 60-second increments (C8)
type TidalEpoch        = uint64    // 3600-second increments (C3)
type ConsolidationCycle = uint64   // 36000-second increments (C6)
```

### 8.2 Identity Types

```
type AgentID    = string  // "ag:<locus>:<uuid7>"
type LocusID    = string  // "locus:<region>:<name>"
type ParcelID   = string  // "parcel:<locus>:<index>"
type ClaimID    = string  // "claim:<class>:<uuid7>"
type QuantumID  = string  // "eq:<locus>:<epoch>:<uuid7>"
type IntentID   = string  // "intent:<uuid>"
```

### 8.3 Enumeration Types

```
type ClaimClass     = D | E | S | H | N | P | R | C | K
type OperationClass = M | B | X | V | G
type SettlementType = B_FAST | V_STANDARD | G_SLOW
type MetabolicPhase = ANABOLISM | CATABOLISM | HOMEOSTASIS
type CredibilityRung = SPECULATIVE | PROVISIONAL | CORROBORATED | ESTABLISHED | CANONICAL  // v2.0
```

### 8.4 Subjective Logic

```
type SLOpinion = {
    belief:     float64  // b >= 0
    disbelief:  float64  // d >= 0
    uncertainty: float64 // u >= 0
    base_rate:  float64  // a in [0, 1]
}
// Constraint: b + d + u = 1
// Expected probability: E(w) = b + a * u
```

### 8.5 Economic Types

```
type AIC           = decimal(18, 8)  // Atrahasis Intelligence Coin
type ProtocolCredit = decimal(18, 8) // Non-transferable, 10%/tick decay
type CapacitySlice = uint64          // CSO-backed resource unit
```

### 8.6 Defense System Types (v2.0)

#### 8.6.1 CACT Types (C11)

```
type CommitmentHash    = string  // "^[a-f0-9]{64}$" (SHA-256)
type CommitmentChainID = string  // "^cc:[a-f0-9]{16}$"
type AttestationProof  = {
    proof_system:        ProofSystem     // GROTH16 | PLONK | STARK_FRI | NOVA
    proof_data:          bytes           // Base64-encoded proof
    public_inputs_hash:  CommitmentHash  // SHA-256 of public inputs
    circuit_id:          string          // Registered verification circuit ID
    verification_key_hash: CommitmentHash
}
type ProofSystem       = GROTH16 | PLONK | STARK_FRI | NOVA
type ChallengeRecord   = {
    vtd_id:              string
    challenge_type:      ChallengeType   // COMMITMENT_OPEN | KI_PROBE | ENV_AUDIT
    result:              ChallengeResult // SURVIVED | WEAKENED | FAILED
    credibility_adjustment: float64
}
type ChallengeType     = COMMITMENT_OPEN | KI_PROBE | ENV_AUDIT
type ChallengeResult   = SURVIVED | WEAKENED | FAILED
type OVCScore          = float64  // [0.0, 1.0] Orthogonal Verification Coverage
```

#### 8.6.2 AVAP Types (C12)

```
type AnonymousAssignmentToken = {
    claim_id:           bytes32         // SHA-256 of claim
    epoch:              TidalEpoch
    agent_id:           AgentID
    vrf_output:         bytes32         // VRF output (beta string, RFC 9381)
    vrf_proof:          bytes80         // VRF proof (pi string)
    selection_rank:     uint8
    committee_slot:     uint8
    assignment_nonce:   bytes16         // CSPRNG, 128-bit entropy
    token_hash:         bytes32
    encrypted_payload:  bytes           // X25519-XSalsa20-Poly1305 encrypted
}
type SealedOpinion = {
    claim_hash:          bytes32
    epoch:               TidalEpoch
    agent_id:            AgentID        // Encrypted during commit phase
    opinion:             SLOpinion
    nonce:               bytes32        // 256-bit CSPRNG
    commitment:          bytes32        // SHA-256(opinion || metadata || nonce)
    signature:           bytes64        // Ed25519 over commitment
}
type HoneypotClaim = {
    claim_content:       string
    ground_truth:        HoneypotVerdict // VALID | INVALID
    error_type:          string
    class:               ClaimClass
    generation_epoch:    TidalEpoch
    canary_variants:     List<CanaryVariant>
}
type HoneypotVerdict   = VALID | INVALID
type CollusionSuspicionScore = float64  // [0.0, 1.0]
```

#### 8.6.3 CRP+ Types (C13)

```
type PerturbationResult = {
    robustness_score:    float64        // [0.0, 1.0]
    aprt_case:           APRTCase       // A | B | C
    flagged_quanta:      List<QuantumID>
    flagged_clusters:    List<List<QuantumID>>
    resynthesis_count:   uint8
}
type APRTCase          = A | B | C
type DissentScore = {
    novelty_tier:        NoveltyTier    // N1 | N2 | N3
    dissent_deficit:     float64        // [0.0, 1.0]
    cods_score:          float64        // [0.0, 1.0] (novelty-calibrated)
}
type NoveltyTier       = N1 | N2 | N3
type ImmunitySignature = {
    signature_id:        string         // uuid7
    created_epoch:       TidalEpoch
    l1_hash:             CommitmentHash // SHA-256 of rejected claim text
    l2_pattern:          StructuralPattern
    l3_pattern:          BehavioralPattern
    match_count:         uint32
    last_match_epoch:    TidalEpoch?
}
// CredibilityRung defined in SS8.3
```

---

## 9. Integration Contract Directory

### 9.1 Contract Matrix

```
         C3    C4    C5    C6    C7    C8    C11   C12   C13
C3       --    ->    <->   <->   <->   <->   <-    <->   <-
C4       --    --    --    ->    ->    ->    --    --    --
C5       <-    --    --    <->   ->    ->    <->   <->   <-
C6       <-    <-    <-    --    ->    ->    --    <-    <->
C7       <-    <-    <-    <-    --    <->   --    --    --
C8       <-    <-    <-    <-    <-    --    <-    <-    <-
C11      ->    --    <->   --    --    ->    --    <-    --
C12      <->   --    <->   ->    --    ->    ->    --    --
C13      ->    --    ->    <->   --    ->    --    --    --

-> = provides data to
<- = receives data from
<-> = bidirectional
-- = no direct contract
```

### 9.2 Contract Details (Core Layers, unchanged from v1.0)

**C3 -> C5:** VRF output per tidal epoch (committee selection), operation scheduling for V-class.
**C5 -> C3:** Verification results fed to settlement calculator.

**C3 -> C6:** Epoch boundary notifications, parcel topology changes.
**C6 -> C3:** Locus-scoped knowledge summaries per tidal epoch.

**C3 <-> C7:** C3 provides scheduling, G-class voting, VRF, topology. C7 submits leaf intents, settlement entries.

**C3 <-> C8:** C3 provides CRDT infrastructure, Sentinel Graph clustering. C8 replicates ledger state via C3 PN-Counters.

**C4 -> C6:** ASV tokens (CLM/CNF/EVD/PRV) enter EMA via ingestion pipeline.
**C4 -> C7:** INT claim type for intent provenance chains.
**C4 -> C8:** Economic message schemas.

**C5 <-> C6:** C5 provides MCTs, VTDs, claim classification. C6 submits K-class VTDs, triggers re-verification.

**C5 -> C7:** Agent credibility scores, claim class assessments.
**C5 -> C8:** Verification reports, credibility scores, attestations.

**C6 -> C7:** Knowledge projections, SHREC state, metabolic phase (read-only).
**C6 -> C8:** Knowledge contribution reports, metabolic efficiency.

**C7 <-> C8:** C7 submits intent budgets, task completions. C8 provides stake availability queries.

### 9.3 Defense System Contracts (v2.0)

#### 9.3.1 C11 (CACT) Contracts

**C11 <-> C5 (PCVM):** CACT extends the PCVM verification pipeline. C11 adds the `cact_extension` field to the VTD envelope schema, extends the D-class proof types with SNARK_PROOF and STARK_PROOF, adds the KI probe type (6th probe type) to the Adversarial Probing System, adds process trace and environmental audit phases to Tier 2 verification, and adds OVC-based belief caps to the Credibility Engine. C5 provides the VTD verification pipeline infrastructure. Data flows bidirectionally: C11 instruments C5 pipeline phases and C5 provides verification results back.

**C11 -> C3 (Tidal Noosphere):** CACT uses C3's VRF engine for KI question generation seeds, environmental audit source selection, and commitment challenge selection. CACT uses the existing VRF domain separator pattern with CACT-specific separators (e.g., `b"KI_PROBE"`, `b"ENV_AUDIT"`). CACT feeds three new metrics to C3's Sentinel Graph: commitment chain integrity failure rate, KI failure rate per agent, and environmental audit discrepancy rate. No changes to C3's VRF mechanism or Sentinel Graph structure are required.

**C11 -> C8 (DSF):** CACT violations (commitment chain fraud, KI failure patterns) are routed through C5 PCVM's existing VERIFICATION_FRAUD slashing category to C8 DSF. CACT adds the OVC quality bonus (+10% settlement reward for OVC > 0.80). No new C8 slashing categories are needed.

#### 9.3.2 C12 (AVAP) Contracts

**C12 <-> C3 (Tidal Noosphere):** AVAP extends C3's VRF Dual Defense Protocol for anonymous committee selection (M1). AVAP uses the domain tag `b"AVAP_M1_v1"` for domain separation from C3 task-scheduling VRF. AVAP inherits C3's Pre-Stratified Diversity Pools and enforces Sentinel Graph co-occurrence limits (MAX_CLUSTER_CO_OCCURRENCE = 1). AVAP feeds behavioral correlation edges back to the Sentinel Graph when the fusion classifier identifies high-probability collusion clusters. AVAP uses epoch-level VRF seeds from C3's entropy source.

**C12 <-> C5 (PCVM):** AVAP wraps the PCVM opinion submission pipeline with sealed commit-reveal (M2). The commit-reveal protocol is transparent to the PCVM Opinion Fusion engine -- revealed opinions are identical in format to non-AVAP opinions. AVAP's honeypot claims (M3) are injected through the same submission pipeline as real claims. Honeypot evaluation occurs after opinion reveal, comparing agent opinions against ground truth. AVAP Merkle-anchors commitment batches on C8 DSF's settlement plane via C5.

**C12 -> C6 (EMA, via Sentinel Graph):** When collusion is confirmed and enterprise liability is triggered (M4c), the credibility cascade propagates through the knowledge graph. Affected claims are reset to maximum uncertainty. Dependent claims are attenuated by CASCADE_ATTENUATION (0.50) per hop. This cascade operates through C6's existing credibility graph infrastructure.

**C12 -> C8 (DSF):** AVAP defines five DSF operations: SLASH (collusion), AIC_TRANSFER (bounty), PENDING_INITIATE (escrow), PENDING_COMPLETE (release), and PENDING_TIMEOUT (return). See SS7.5.2 and SS7.5.3 for details. All bounties are funded from forfeited stakes; no new AIC creation.

#### 9.3.3 C13 (CRP+) Contracts

**C13 <-> C6 (EMA):** CRP+ wraps C6's entire consolidation phase (dreaming pipeline, Section 5.3). CRP+ inserts at five points: M4 VRF selection replaces deterministic candidate identification, M7 immune memory check after synthesis, M1 APRT after immune check, M2 CODS after APRT, M5 credibility ladder assignment after PCVM verification. CRP+ also piggybacks on C6's catabolism phase (M5 demotion checks) and regulation phase (M7 memory decay). C6 provides the Three-Pass LLM Synthesis, coherence graph, and quantum metadata. CRP+ writes back rung assignments and depth limit constraints to C6's quantum store.

**C13 -> C5 (PCVM):** K-class VTDs produced by CRP+-instrumented consolidation are submitted to PCVM for verification through the existing C6 -> C5 pathway. PCVM treats these identically to other K-class VTDs. CRP+ sets the initial rung on the quantum metadata before PCVM submission. PCVM does not modify the rung.

**C13 -> C3 (Tidal Noosphere):** CRP+ uses C3's ECVRF infrastructure for consolidation candidate selection (M4). The VRF input uses the domain separator `"CRP_CONSOLIDATION_SELECT"` to prevent cross-domain VRF output reuse. CRP+ reuses C3's ECVRF key pairs -- separate key generation for consolidation selection is prohibited. Rung promotion/demotion events are replicated via C3 CRDT infrastructure.

**C13 -> C8 (DSF):** K-class settlement rewards are multiplied by the credibility rung's influence weight (see SS7.5.4). No new slashing categories are needed for CRP+ -- consolidation-related penalties are handled through existing C10/C6 mechanisms.

#### 9.3.4 Inter-Defense Contracts

**C12 -> C11:** AVAP's honeypot engine (M3) uses CACT commitment chain data to design indistinguishable honeypots. Honeypot VTDs include plausible CACT extensions.

**C11 and C12 are otherwise independent:** CACT operates on VTD verification (individual claim integrity). AVAP operates on committee behavior (collective verification integrity). They share no runtime data flow.

**C13 is downstream of C11 and C12:** CRP+ operates on consolidated knowledge produced after CACT-verified and AVAP-protected verification has occurred. CRP+ assumes that K-class VTDs entering the consolidation pipeline have already passed CACT and AVAP scrutiny.

---

## 10. Errata to Existing Specifications

### 10.1 C3 Tidal Noosphere

**E-C3-01:** C3's `claim_class` enum (Line 2048) should be extended from `{deterministic, empirical, statistical, heuristic, normative}` to include `{process, reasoning, compliance, knowledge_consolidation}`. The full canonical enum: `{deterministic, empirical, statistical, heuristic, normative, process, reasoning, compliance, knowledge_consolidation}`.

**E-C3-02:** C3's verification pathways (Lines 800-808) should include entries for P/R/C/K classes:
- P: Trace replay + cross-reference
- R: Premise verification + logical audit
- C: Rule-set matching + constitutional compliance
- K: Source provenance + reasoning chain + falsification audit

**E-C3-03:** When this addendum uses "TIDAL_EPOCH", it refers to C3's "EPOCH_DURATION" (3600s). No change to C3 required.

### 10.2 C4 ASV

**E-C4-01:** C4 should add an informative appendix (non-normative) describing its position in the Atrahasis stack and the epistemic_class -> claim_class mapping from SS6.1 of this document. C4's core specification is unchanged.

### 10.3 C5 PCVM

**E-C5-01:** C5's 8-class taxonomy should be extended to 9 classes with the addition of K-class (Knowledge Consolidation) as defined in SS4.1 of this document. K-class parameters: Tier 2, committee size 5, admission threshold 0.70, base rate 0.6, half-life 120 days.

**E-C5-02:** Conservatism ordering updated from `H > N > E > S > R > P > C > D` to `H > N > K > E > S > R > P > C > D`.

### 10.4 C6 EMA

**E-C6-01:** C6's claim class mapping table (Lines 469-478) should replace "C (Consolidation)" with "K (Knowledge Consolidation)". All references to submitting consolidation outputs "as C-class claims" should read "as K-class claims".

**E-C6-02:** C6's `claim_class` field in the EpistemicQuantum definition (Line 251) should use the 9-class enum: `D|E|S|H|N|P|R|C|K`.

### 10.5 C7 RIF

**E-C7-01:** C7's Settlement Router (SS11.5) references "C3 settlement ledger". This should read "C8 DSF settlement ledger, accessed via C3's CRDT replication infrastructure".

### 10.6 C8 DSF

**E-C8-01:** C8's claim class difficulty weights (Lines 3837-3841) should use the full 9-class table from SS7.3 of this document. The "P (Primary) x1.0, R (Replication) x0.7, C (Challenge) x1.3" modifiers are removed -- P, R, and C are full claim classes, not modifiers.

**E-C8-02:** C8's `epoch_duration_ms` (60000ms) corresponds to SETTLEMENT_TICK in the canonical temporal hierarchy. All C8 epoch references are SETTLEMENT_TICKs. No change to C8's internal logic is required.

### 10.7 C11 CACT (v2.0)

**E-C11-01:** C11 references "8+1 claim class system" (Section 4.7). This should read "9 claim classes" using the canonical taxonomy from SS4.1 of this document. The "+1" notation (referring to K-class as an addendum class) is deprecated; K-class is a first-class member of the taxonomy.

**E-C11-02:** C11's CACT VTD envelope extension (Section 4.2.2) uses `cact_extension` as the field name. This is the canonical field name for the CACT extension in the VTD envelope schema. All layers referencing CACT data on VTDs MUST use this field name.

**E-C11-03:** C11 states D-class CACT commitment chains are REQUIRED and other classes are OPTIONAL (Section 4.3.1). This creates a credibility cap of CACT_ABSENT_CREDIBILITY_CAP (0.70) for non-D-class VTDs without commitment chains. This cap is additive with any other credibility caps (the effective cap is the minimum of all applicable caps).

### 10.8 C12 AVAP (v2.0)

**E-C12-01:** C12's claim class coverage table for honeypots (Section 6.2) uses "C (Causal)" and "S (Subjective)" labels. These should be read as "C (Compliance)" and "S (Statistical)" per the canonical taxonomy. The honeypot coverage assignments remain unchanged; only the label terminology is corrected.

**E-C12-02:** C12's M1 committee size defaults (Section 4.8) define MIN_COMMITTEE_SIZE = 7 and DEFAULT_COMMITTEE_SIZE = 10. These override the per-class committee sizes in SS4.3 of this document when AVAP is active. The AVAP committee size takes precedence because anonymous verification requires a larger committee for BFT tolerance. The per-class sizes in SS4.3 apply only when AVAP is not active (e.g., during bootstrap).

**E-C12-03:** C12's sealed opinion nonce is 256-bit (32 bytes), while C11's CACT commitment assignment nonce is 128-bit (16 bytes). Both are acceptable for their respective purposes (C12's nonce protects opinion secrecy which requires higher entropy; C11's nonce prevents replay which is adequately served by 128 bits).

### 10.9 C13 CRP+ (v2.0)

**E-C13-01:** C13's M5 credibility ladder (Section 8) replaces C10 Layer 5's binary PENDING_VALIDATION / VALIDATED model. The C10 `EmpiricalValidationQueue` data structure is retained for backward compatibility, but its `uncertainty_floor` field is derived from the M5 rung and domain-adaptive calibration. This is the canonical replacement; implementations MUST NOT maintain both the old binary model and the new ladder simultaneously.

**E-C13-02:** C13's M6 depth limits (Section 9) introduce a new enforcement point in C6's consolidation candidate identification. This enforcement MUST occur before any LLM synthesis cost is incurred. C6 implementations MUST call the depth-limit filter as the first step of candidate identification.

**E-C13-03:** C13's immune memory signatures (M7, Section 10) use three levels: L1 (exact content hash), L2 (structural pattern), and L3 (behavioral pattern). The L1 hash uses SHA-256 over the rejected claim text, which is consistent with the hashing standard used throughout the stack (C11 CACT commitment chains, C12 AVAP sealed opinions).

---

## 11. Invariants

### 11.1 Temporal Invariants

**INV-T1 (Epoch Ratio).** TIDAL_EPOCH = 60 x SETTLEMENT_TICK. Constitutional parameter.

**INV-T2 (Consolidation Ratio).** CONSOLIDATION_CYCLE = 10 x TIDAL_EPOCH. Governance-configurable.

**INV-T3 (Boundary Ordering).** Settlement tick boundaries are subsets of tidal epoch boundaries. Every tidal epoch boundary is also a settlement tick boundary. Not every settlement tick boundary is a tidal epoch boundary.

### 11.2 Classification Invariants

**INV-C1 (PCVM Sovereignty).** PCVM (C5) is the sole authority for claim class assignment. No other layer may override PCVM's classification.

**INV-C2 (Conservatism).** When classification inputs disagree, the most conservative class is selected per the ordering H > N > K > E > S > R > P > C > D.

**INV-C3 (Completeness).** Every claim entering any layer's knowledge store must have a PCVM-assigned class. No unclassified claims exist in the canonical state.

**INV-C4 (K-Class Provenance).** K-class claims must have source quanta from >=5 independent agents across >=3 parcels, with no single agent contributing >30%.

### 11.3 Settlement Invariants

**INV-S1 (Authority).** C8 DSF is the sole settlement authority. C3's settlement calculator feeds data to C8; it does not independently settle.

**INV-S2 (Monotonic Difficulty).** Difficulty weights are weakly monotonically increasing with conservatism ordering (within each verification tier).

**INV-S3 (Complete Coverage).** Every claim class has a defined difficulty weight and settlement type. No claim class is unsettleable.

### 11.4 Defense System Invariants (v2.0)

**INV-D1 (CACT Temporal Ordering).** All commitments in a CACT commitment chain MUST have timestamps that precede the VTD submission timestamp. A commitment with a timestamp after VTD submission constitutes retroactive fabrication and MUST cause the commitment chain verification to FAIL. Authority: C11 SS4.3.1.

**INV-D2 (AVAP Committee Anonymity).** No agent MUST learn the identity of any other committee member until after all sealed opinions have been submitted and the reveal phase is complete. Committee membership MUST NOT be revealed to any party other than the selected agent itself until after the reveal deadline T_r. Authority: C12 SS4.4, INV-M1.

**INV-D3 (CRP+ Pre-Submission Testing).** Every consolidation candidate that passes Three-Pass LLM Synthesis MUST undergo at least Tier 1 APRT screening before K-class PCVM submission. No K-class claim produced by the dreaming pipeline may bypass perturbation robustness testing. This is INV-CRP2. Authority: C13 SS4.2.

**INV-D4 (Immune Memory False Positive Bound).** Immune memory signatures (C13 M7) MUST NOT match legitimate consolidation patterns at a rate exceeding 5% false positive (L2 level) or 10% false positive (L3 level) in any rolling 100-epoch window. If these bounds are exceeded, the matching thresholds (L2_MATCH_THRESHOLD, L3_MATCH_THRESHOLD) MUST be tightened by 0.05 per violation until the false positive rate drops below the bound. Authority: C13 SS10.3. Monitoring responsibility: C6 EMA (measures consolidation acceptance rates) cross-referenced with C13 (measures match rates).

**INV-D5 (Defense System Budget Isolation).** Defense system economic operations (CACT slashing, AVAP bounties, CRP+ rung-weighted settlement) MUST NOT consume more than 15% of total C8 DSF settlement capacity in any single TIDAL_EPOCH. If this threshold is approached, defense system settlement operations are queued to the next epoch. This prevents a defense-system event (e.g., a large enterprise liability audit) from starving normal settlement operations.

---

## 12. Conformance Requirements

### 12.1 Mandatory

Any implementation of the Atrahasis stack MUST:

1. Use the three-tier temporal hierarchy from SS3
2. Support all 9 claim classes from SS4
3. Implement the C4->C5 mapping from SS6 for ASV message intake
4. Route all settlement through C8 DSF per SS7
5. Use canonical type definitions from SS8 for cross-layer communication
6. (v2.0) Implement the CredibilityRung type and enforce rung-based uncertainty floors for K-class claims per SS4.6
7. (v2.0) Enforce INV-CRP5 (depth limits): PROVISIONAL and SPECULATIVE K-class quanta excluded from consolidation input
8. (v2.0) Route all defense-system economic operations through C8 DSF per SS7.5
9. (v2.0) Use defense system type definitions from SS8.6 for cross-layer defense system communication
10. (v2.0) Enforce all defense system invariants (INV-D1 through INV-D5) from SS11.4

### 12.2 Recommended

Implementations SHOULD:

1. Include this document's errata (SS10) in their copies of layer-specific specs
2. Validate cross-layer contracts (SS9) at integration testing time
3. Monitor INV-T1 through INV-S3 at runtime
4. (v2.0) Monitor INV-D1 through INV-D5 at runtime
5. (v2.0) Implement the defense system contract matrix (SS9.1) with explicit interface validation
6. (v2.0) Test defense system integration using the contract details in SS9.3 as acceptance criteria

### 12.3 Defense System Conformance (v2.0)

Implementations deploying defense systems MUST additionally:

1. **C11 CACT:** Implement commitment chain verification as Phase 0 of PCVM verification (before class-specific verification). D-class VTDs MUST include CACT commitment chains. Other classes incur a credibility cap (CACT_ABSENT_CREDIBILITY_CAP = 0.70) if chains are absent.

2. **C12 AVAP:** Implement anonymous committee selection (M1) and sealed opinion submission (M2) for all verification committees. Cover traffic MUST be indistinguishable from real verification traffic. The commit-reveal protocol MUST be transparent to the PCVM Opinion Fusion engine.

3. **C13 CRP+:** Implement VRF consolidation selection (M4), APRT robustness testing (M1), and the graduated credibility ladder (M5) for all K-class claims produced by dreaming consolidation. Depth limits (M6) MUST be enforced at candidate identification time.

---

## Appendix A: Claim Class Quick Reference

```
+----------------------------------------------------------------------+
| TIER 1: FORMAL_PROOF (committee: 3)                                   |
|   D -- Deterministic    threshold: 0.95  weight: 1.0  settle: B-fast |
|   C -- Compliance       threshold: 0.90  weight: 1.3  settle: B-fast |
+----------------------------------------------------------------------+
| TIER 2: STRUCTURED_EVIDENCE (committee: 5)                            |
|   P -- Process          threshold: 0.80  weight: 1.5  settle: B-fast |
|   R -- Reasoning        threshold: 0.75  weight: 2.0  settle: V-std  |
|   E -- Empirical        threshold: 0.60  weight: 1.5  settle: V-std  |
|   S -- Statistical      threshold: 0.65  weight: 2.0  settle: V-std  |
|   K -- Knowledge Consol threshold: 0.70  weight: 1.8  settle: V-std  |
+----------------------------------------------------------------------+
| TIER 3: STRUCTURED_ATTESTATION (committee: 7)                         |
|   H -- Heuristic        threshold: 0.50  weight: 2.5  settle: V-std  |
|   N -- Normative        threshold: 0.50  weight: 3.0  settle: G-slow |
+----------------------------------------------------------------------+

Conservatism: H > N > K > E > S > R > P > C > D

K-Class Credibility Ladder (v2.0):
  Rung 0 SPECULATIVE:  u>=0.80  weight=0.00  (sandboxed K->K only)
  Rung 1 PROVISIONAL:  u>=0.50  weight=0.25  (default entry)
  Rung 2 CORROBORATED: u>=0.30  weight=0.50  (1+ direct corroboration)
  Rung 3 ESTABLISHED:  u>=0.15  weight=0.75  (3+ corr, cross-parcel, 50 ep)
  Rung 4 CANONICAL:    u>=0.05  weight=1.00  (5+ corr, 3+ parcels, 200 ep)
```

---

## Appendix B: Epoch Hierarchy Derivation Proof

**Claim:** The three-tier temporal hierarchy introduces no contradictions with existing C3, C5, C6, C7, or C8 parameters.

**Proof:**

1. **C3 consistency:** C3 defines EPOCH_DURATION = 3600s. We define TIDAL_EPOCH = 3600s. Identity mapping.

2. **C5 consistency:** C5 references "1-hour tidal epoch clock" with verification window T+0 to T+50min. TIDAL_EPOCH = 3600s = 60 minutes. T+50min = tick 51 of 60.

3. **C6 consistency:** C6 defines consolidation "every N epochs (default N=10)". With TIDAL_EPOCH = 3600s, this gives CONSOLIDATION_CYCLE = 10 x 3600s = 36000s = 10 hours.

4. **C7 consistency:** C7 references "settlement lag up to 32 epochs". With TIDAL_EPOCH = 3600s, this gives 32 hours maximum lag. C7's staleness tolerance of "5 epochs" = 5 hours. These are coordination-scale timescales, consistent with TIDAL_EPOCH.

5. **C8 consistency:** C8 defines epoch_duration_ms = 60000. We define SETTLEMENT_TICK = 60s = 60000ms. Identity mapping. C8's internal EABS logic, throughput benchmarks (42K msg/s at 60s), and staleness bounds (~63s) are all unchanged.

6. **Inter-tier consistency:** 60 SETTLEMENT_TICKs x 60s = 3600s = 1 TIDAL_EPOCH. The ratio is exact (integer). Tidal epoch boundaries are aligned with settlement tick boundaries (tick 60 of each tidal epoch = epoch boundary).

7. **C11 consistency (v2.0):** C11 CACT commitment chains are epoch-bound, with timestamps referencing the tidal epoch clock. CACT's commitment rate limit (MAX_COMMITMENTS_PER_EPOCH = 100) uses TIDAL_EPOCH. No contradiction.

8. **C12 consistency (v2.0):** C12 AVAP's verification window (6 hours, default) spans multiple TIDAL_EPOCHs. AVAP's VRF re-keying interval (REKEY_INTERVAL = 100 epochs) uses TIDAL_EPOCHs. AVAP's Merkle-anchored commitment batching occurs once per epoch = once per TIDAL_EPOCH. No contradiction.

9. **C13 consistency (v2.0):** C13 CRP+ uses "cycle" to refer to CONSOLIDATION_CYCLE (10 TIDAL_EPOCHs) in consolidation contexts, and "epoch" for TIDAL_EPOCH in all other contexts. CRP+ M7 immune memory expiry uses consolidation cycles (e.g., L1_EXPIRY_CYCLES = 50 cycles = 500 TIDAL_EPOCHs). No contradiction.

**QED.**

---

## Appendix C: Configurable Parameters

### C.1 Core Layer Parameters (v1.0)

| # | Parameter | Default | Range | Authority | Section |
|---|-----------|---------|-------|-----------|---------|
| 1 | SETTLEMENT_TICK_DURATION | 60s | [30s, 300s] | C8 | SS3.1 |
| 2 | TICKS_PER_TIDAL_EPOCH | 60 | [12, 120] | C9 (constitutional) | SS3.1 |
| 3 | TIDAL_EPOCHS_PER_CONSOLIDATION | 10 | [5, 50] | C6 | SS3.1 |
| 4 | K_CLASS_ADMISSION_THRESHOLD | 0.70 | [0.60, 0.85] | C9 | SS4.3 |
| 5 | K_CLASS_BASE_RATE | 0.6 | [0.5, 0.7] | C9 | SS4.3 |
| 6 | K_CLASS_HALF_LIFE_DAYS | 120 | [60, 365] | C9 | SS4.5 |
| 7 | K_CLASS_AGING_RATE | 0.005/epoch | [0.001, 0.01] | C9 | SS4.5 |
| 8 | K_CLASS_AGING_THRESHOLD_EPOCHS | 100 | [50, 500] | C9 | SS4.5 |
| 9 | K_CLASS_DIFFICULTY_WEIGHT | 1.8 | [1.2, 2.5] | C9 | SS7.3 |
| 10 | K_CLASS_MIN_SOURCE_AGENTS | 5 | [3, 10] | C6 | SS4.4 |
| 11 | K_CLASS_MIN_SOURCE_PARCELS | 3 | [2, 5] | C6 | SS4.4 |
| 12 | K_CLASS_MAX_AGENT_CONCENTRATION | 0.30 | [0.20, 0.50] | C6 | SS4.4 |

### C.2 CACT Parameters (v2.0, C11)

| # | Parameter | Default | Range | Governance | Section |
|---|-----------|---------|-------|------------|---------|
| 13 | MAX_COMMITMENTS_PER_EPOCH | 100 | [10, 1000] | Operator | C11 SS5.2 |
| 14 | CACT_ABSENT_CREDIBILITY_CAP | 0.70 | [0.50, 0.90] | G-class | C11 SS4.3.1 |
| 15 | KI_PASS_THRESHOLD | 0.80 | [0.60, 0.95] | G-class | C11 SS5.4 |
| 16 | KI_MARGINAL_THRESHOLD | 0.50 | [0.30, 0.70] | Operator | C11 SS4.3.3 |
| 17 | KI_TIMEOUT_MS | 30000 | [10000, 60000] | Operator | C11 SS4.3.3 |
| 18 | PROCESS_TRACE_ABSENT_CAP | 0.75 | [0.60, 0.90] | G-class | C11 SS4.3.4 |
| 19 | OVC_MIN_CAP | 0.50 | [0.30, 0.70] | G-class | C11 SS4.5 |
| 20 | OVC_MAX_CAP | 0.95 | [0.85, 1.00] | G-class | C11 SS4.5 |
| 21 | OVC_WEIGHT_COMMITMENT | 0.30 | [0.20, 0.40] | G-class | C11 SS4.4 |
| 22 | OVC_WEIGHT_KI | 0.25 | [0.15, 0.35] | G-class | C11 SS4.4 |
| 23 | OVC_WEIGHT_PROCESS | 0.20 | [0.10, 0.30] | G-class | C11 SS4.4 |
| 24 | OVC_WEIGHT_ENV | 0.25 | [0.15, 0.35] | G-class | C11 SS4.4 |
| 25 | VC_QUALITY_BONUS | 0.10 | [0.05, 0.20] | Operator | C11 SS4.6.3 |
| 26 | BOOTSTRAP_RELAXATION_EPOCHS | 100 | [50, 500] | G-class | C11 SS6.2 |

### C.3 AVAP Parameters (v2.0, C12)

| # | Parameter | Default | Range | Constitutional | Section |
|---|-----------|---------|-------|----------------|---------|
| 27 | MIN_COMMITTEE_SIZE | 7 | [5, 20] | YES (G-class) | C12 SS4.8 |
| 28 | DEFAULT_COMMITTEE_SIZE | 10 | [7, 15] | No | C12 SS4.8 |
| 29 | MIN_POOL_SIZE | 200 | [100, 1000] | YES (G-class) | C12 SS4.8 |
| 30 | MAX_COMMITTEE_TO_POOL_RATIO | 0.05 | [0.01, 0.10] | YES (G-class) | C12 SS4.8 |
| 31 | MAX_CLUSTER_CO_OCCURRENCE | 1 | [1, 3] | No | C12 SS4.8 |
| 32 | COVER_TRAFFIC_DEPTH | 3 | [2, 5] | No | C12 SS4.5 |
| 33 | REVEAL_THRESHOLD | 0.70 | [0.50, 0.90] | No | C12 SS5.3 |
| 34 | REVEAL_MISMATCH_PENALTY | 50 AIC | [10, 200] | No | C12 SS5.3 |
| 35 | HONEYPOT_D_INJECTION_RATE | 0.05 | [0.02, 0.10] | No | C12 SS6.2 |
| 36 | HONEYPOT_E_INJECTION_RATE | 0.05 | [0.02, 0.10] | No | C12 SS6.2 |
| 37 | UNCERTAINTY_INJECTION_RATE | 0.02 | [0.01, 0.05] | No | C12 SS7.2 |
| 38 | EARLY_BOUNTY_RATE | 0.50 | [0.30, 0.70] | No | C12 SS7.3 |
| 39 | MAX_BOUNTY_CAP | 0.60 | [0.40, 0.80] | No | C12 SS7.3 |
| 40 | AUDIT_LOOKBACK_EPOCHS | 500 | [200, 1000] | No | C12 SS7.4 |
| 41 | INVESTIGATION_THRESHOLD | 0.30 | [0.20, 0.40] | No | C12 SS8.6 |
| 42 | SLASHING_RECOMMENDATION_THRESHOLD | 0.75 | [0.60, 0.90] | No | C12 SS8.6 |
| 43 | REKEY_INTERVAL | 100 | [50, 500] | No | C12 SS4.6 |
| 44 | CSS_LOOKBACK | 200 | [100, 500] | No | C12 SS8.3 |

### C.4 CRP+ Parameters (v2.0, C13)

| # | Parameter | Default | Range | Constitutional | Section |
|---|-----------|---------|-------|----------------|---------|
| 45 | VRF_SELECTION_RATE | 0.10 | [0.05, 0.30] | YES (G-class) | C13 SS7.3 |
| 46 | STABILITY_THRESHOLD | 0.70 | [0.50, 0.85] | YES (G-class) | C13 SS4.4.1 |
| 47 | CRP_ACCEPT_THRESHOLD | 0.35 | [0.20, 0.50] | YES (G-class) | C13 SS12.2 |
| 48 | CRP_REJECT_THRESHOLD | 0.60 | [0.45, 0.80] | YES (G-class) | C13 SS12.2 |
| 49 | MAX_IMMUNE_SIGNATURES | 1000 | [100, 5000] | YES (G-class) | C13 SS10.5 |
| 50 | PROVISIONAL_INFLUENCE_WEIGHT | 0.25 | [0.10, 0.40] | YES (G-class) | C13 SS8.2 |
| 51 | QUARANTINE_CYCLES_N3 | 5 | [3, 20] | YES (G-class) | C13 SS11.3.3 |
| 52 | DEPTH_LIMIT_CORROBORATED_WEIGHT | 0.50 | [0.25, 0.75] | YES (G-class) | C13 SS9.2 |
| 53 | HIGH_INFLUENCE_SIGMA | 2.0 | [1.5, 3.0] | No | C13 SS4.3.3 |
| 54 | REDUNDANT_CLUSTER_SIMILARITY | 0.85 | [0.75, 0.95] | No | C13 SS4.3.3 |
| 55 | EXPECTED_DISSENT_LEVEL | 1.5 | [1.0, 3.0] | No | C13 SS5.4.3 |
| 56 | L2_MATCH_THRESHOLD | 0.60 | [0.40, 0.80] | No | C13 SS10.3 |
| 57 | L3_MATCH_THRESHOLD | 0.50 | [0.30, 0.70] | No | C13 SS10.3 |
| 58 | WEIGHT_APRT | 0.35 | [0.20, 0.50] | No | C13 SS12.1 |
| 59 | WEIGHT_CODS | 0.25 | [0.15, 0.35] | No | C13 SS12.1 |
| 60 | WEIGHT_PROBE | 0.25 | [0.15, 0.35] | No | C13 SS12.1 |
| 61 | WEIGHT_IMMUNE | 0.15 | [0.05, 0.25] | No | C13 SS12.1 |
| 62 | SANDBOX_TIMEOUT_CYCLES | 10 | [5, 20] | No | C13 SS9.4 |
| 63 | MAX_SANDBOXED_PER_CYCLE | 5 | [1, 10] | No | C13 SS9.4 |
| 64 | FAST_TRACK_MODALITIES | 3 | [2, 5] | No | C13 SS8.4 |

---

## Appendix D: Glossary

| Term | Definition | Authority |
|------|-----------|-----------|
| SETTLEMENT_TICK | 60-second economic settlement cycle | C8 |
| TIDAL_EPOCH | 3600-second coordination cycle (= 60 ticks) | C3 |
| CONSOLIDATION_CYCLE | 36000-second knowledge metabolism cycle (= 10 tidal epochs) | C6 |
| Claim Class | One of 9 verification categories: D/E/S/H/N/P/R/C/K | C5 + C9 |
| Operation Class | One of 5 coordination categories: M/B/X/V/G | C3 |
| Settlement Type | One of 3 settlement timings: B_FAST/V_STANDARD/G_SLOW | C8 |
| EABS | Epoch-Anchored Batch Settlement -- C8's write protocol | C8 |
| MCT | Membrane Clearance Token -- C5's verification output | C5 |
| VTD | Verification Trace Document -- C5's proof artifact | C5 |
| SL Opinion | Subjective Logic opinion tuple (b, d, u, a) | C5 |
| CSO | Certified Slice Object -- proof-carrying resource right | C3/C8 |
| K-class | Knowledge Consolidation claim -- EMA dreaming output | C9 |
| AIC | Atrahasis Intelligence Coin -- economic token | C8 |
| Protocol Credit | Non-transferable spam-control token, 10%/tick decay | C8 |
| Capacity Slice | CSO-backed resource unit for compute/storage/bandwidth | C8 |
| CACT | Commit-Attest-Challenge-Triangulate -- VTD forgery defense architecture | C11 |
| Commitment Chain | Sequential hash-linked log of cryptographic commitments to evidence artifacts | C11 |
| OVC Score | Orthogonal Verification Coverage -- measure of independent verification channel coverage | C11 |
| Knowledge Interrogation (KI) | Adversarial probe testing whether a VTD producer possesses claimed generative knowledge | C11 |
| AVAP | Anonymous Verification with Adaptive Probing -- anti-collusion architecture | C12 |
| Anonymous Assignment Token | VRF-based encrypted committee assignment preserving member anonymity | C12 |
| Sealed Opinion | Commit-reveal wrapped Subjective Logic opinion preventing signaling | C12 |
| Honeypot Claim | Synthetic verification task with known ground truth for detecting dishonest agents | C12 |
| CDP | Collusion Deterrence Payment -- economic mechanism for ring defection incentives | C12 |
| CSS | Collusion Suspicion Score -- per-agent measure of conditional behavioral anomaly | C12 |
| CRP+ | Consolidation Robustness Protocol -- consolidation poisoning defense | C13 |
| APRT | Adaptive Perturbation Robustness Testing -- tests whether consolidation survives input changes | C13 |
| CODS | Calibrated Organic Dissent Search -- novelty-calibrated dissent deficit analysis | C13 |
| Credibility Rung | One of 5 graduated trust levels for K-class claims: SPECULATIVE through CANONICAL | C13 |
| Immune Memory | Three-level signature storage for rejected consolidation patterns | C13 |
| Novelty Pathway | Dedicated scrutiny track for paradigmatic (N3) discoveries | C13 |

---

## Appendix E: Defense System Integration Map (v2.0)

```
DEFENSE SYSTEM INTEGRATION WITH 6-LAYER STACK
===============================================

                    C11 CACT          C12 AVAP          C13 CRP+
                    (VTD Forgery)     (Collusion)       (Consolidation
                                                         Poisoning)

Layer 6: RIF (C7)      .                .                  .
                        .                .                  .

Layer 5: C3 Noosphere  VRF seeds       VRF seeds          VRF seeds
                       Sentinel feed    Sentinel edges     CRDT replication
                       Epoch clock      Diversity pools    (rung events)
                        |               Committee select    |
                        |                |                  |

Layer 4: C5 PCVM       VTD extension   Sealed opinions    K-class VTD
                       Commitment chain  Honeypot inject   submission
                       KI probes         Opinion fusion     |
                       Process trace     (transparent)      |
                       Env audit          |                 |
                       OVC scoring        |                 |
                       Credibility cap    |                 |
                        |                |                  |

Layer 3: C6 EMA         .              Credibility        Dreaming pipeline
                         .              cascade            APRT, CODS
                         .              (on collusion)     Immune memory
                         .                |                Credibility ladder
                         .                |                Depth limits
                         .                |                 |

Layer 2: C8 DSF        Fraud slashing  Ring slashing      Rung-weighted
                       OVC bonus        Bounty escrow      settlement
                                        Enterprise liab.    |
                                         |                  |

Layer 1: C4 ASV          .                .                 .

LEGEND:
  VRF seeds     = Uses C3 VRF with domain-separated inputs
  Sentinel      = Reads from / writes to Sentinel Graph
  VTD extension = Extends VTD envelope schema
  Sealed opinions = Wraps opinion submission with commit-reveal
  Dreaming pipeline = Wraps C6 consolidation phase
  Slashing      = Routes slashing events through C8 DSF

CROSS-DEFENSE FLOWS:
  C12 --> C11: Honeypot engine uses CACT data for indistinguishable honeypots
  C13 downstream of C11/C12: CRP+ assumes K-class inputs have passed
                              CACT verification and AVAP-protected committee review
```

---

## Appendix F: Changelog

### v2.0.0 (2026-03-10)

**Purpose:** Extend v1.0 with cross-layer integration requirements for defense systems C11 (CACT), C12 (AVAP), and C13 (CRP+).

**Changes:**

| Section | Change Type | Description |
|---------|-------------|-------------|
| SS1.1 | UPDATED | Added v2.0 extension paragraph describing defense system scope |
| SS1.2 | UPDATED | Added defense system integration, K-class lifecycle, and defense settlement to scope |
| SS1.3 | UPDATED | Added C11/C12/C13 to authority hierarchy table |
| SS2 | UPDATED | Added cross-cutting defense systems to architecture stack diagram |
| SS3.3 | UPDATED | Added C11/C12/C13 activities to intra-tidal-epoch timeline |
| SS3.4 | UPDATED | Added C11/C12/C13 to parameter interpretation guide |
| SS4.6 | NEW | K-class extended lifecycle: graduated credibility ladder (CRP+ integration) |
| SS4.6.1 | NEW | Rung definitions with uncertainty floors and influence weights |
| SS4.6.2 | NEW | Influence weight application formula |
| SS4.6.3 | NEW | Relationship between aging uncertainty and credibility ladder |
| SS4.6.4 | NEW | Consolidation depth limits (CRP+ M6) |
| SS7.5 | NEW | Defense system settlement integration |
| SS7.5.1 | NEW | CACT staking costs (C11 -> C8) |
| SS7.5.2 | NEW | CDP bounty treasury (C12 -> C8) |
| SS7.5.3 | NEW | Enterprise liability slashing (C12 -> C8) |
| SS7.5.4 | NEW | Credibility-weighted settlement (C13 -> C8) |
| SS8.3 | UPDATED | Added CredibilityRung to enumeration types |
| SS8.6 | NEW | Defense system types: CACT (SS8.6.1), AVAP (SS8.6.2), CRP+ (SS8.6.3) |
| SS9.1 | UPDATED | Extended contract matrix to include C11/C12/C13 |
| SS9.3 | NEW | Defense system contracts (C11, C12, C13) with full detail |
| SS9.3.4 | NEW | Inter-defense contracts |
| SS10.7 | NEW | C11 CACT errata (E-C11-01 through E-C11-03) |
| SS10.8 | NEW | C12 AVAP errata (E-C12-01 through E-C12-03) |
| SS10.9 | NEW | C13 CRP+ errata (E-C13-01 through E-C13-03) |
| SS11.4 | NEW | Defense system invariants (INV-D1 through INV-D5) |
| SS12.1 | UPDATED | Added mandatory conformance items 6-10 for defense systems |
| SS12.2 | UPDATED | Added recommended items 4-6 for defense system monitoring |
| SS12.3 | NEW | Defense system conformance requirements |
| Appendix A | UPDATED | Added K-class credibility ladder summary |
| Appendix B | UPDATED | Added C11/C12/C13 consistency proofs (items 7-9) |
| Appendix C | UPDATED | Added C.2 (CACT), C.3 (AVAP), C.4 (CRP+) parameter tables |
| Appendix D | UPDATED | Added 15 defense system glossary entries |
| Appendix E | NEW | Defense system integration map (visual) |
| Appendix F | NEW | This changelog |

**Preserved from v1.0:** All original content in SS1-SS12 and Appendices A-D is preserved. No v1.0 content was removed or modified in meaning. v2.0 additions are marked with "(v2.0)" inline or placed in new sections/subsections.

---

*End of Cross-Layer Reconciliation Addendum v2.0.0*
