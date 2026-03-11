# Cross-Layer Reconciliation Addendum

**Version:** 1.0.0
**Date:** 2026-03-10
**Status:** SPECIFICATION
**Authority:** This document is the canonical cross-layer integration specification for the Atrahasis architecture stack. Where layer-specific Master Tech Specs (C3-C8) conflict with this document on cross-layer matters, this document takes precedence.

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

---

## 1. Purpose and Scope

### 1.1 Purpose

The Atrahasis architecture consists of six layers, each specified independently as a Master Tech Spec (C3 through C8). These specifications were produced sequentially through the Atrahasis Agent System (AAS) pipeline, with each later layer informed by but not formally constrained by earlier layers.

This document resolves the cross-layer inconsistencies identified by a systematic reconciliation scan (C9) and establishes the canonical integration specification that bridges all six layers.

### 1.2 Scope

This addendum covers:
- **Temporal alignment** — canonical epoch hierarchy across all layers
- **Claim class taxonomy** — unified 9-class taxonomy with cross-layer mappings
- **Cross-layer type definitions** — canonical types for inter-layer communication
- **Integration contract directory** — summary of all bidirectional contracts
- **Errata** — specific corrections to layer specs where inconsistencies exist

This addendum does NOT:
- Modify internal algorithms of any layer
- Change any layer's API surface
- Override any layer's sovereignty over its own domain
- Introduce new architectural components

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

---

## 2. Architecture Stack Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 6: RIF — Recursive Intent Fabric (C7)                │
│  Purpose: Intent decomposition, agent assignment, lifecycle  │
├─────────────────────────────────────────────────────────────┤
│  Layer 5: Tidal Noosphere (C3)                              │
│  Purpose: Coordination, CRDT state, topology, governance     │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: PCVM — Proof-Carrying Verification Membrane (C5)  │
│  Purpose: Claim verification, classification, credibility    │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: EMA — Epistemic Metabolism Architecture (C6)      │
│  Purpose: Knowledge lifecycle, consolidation, circulation    │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: DSF — Deterministic Settlement Fabric (C8)        │
│  Purpose: Economic settlement, budgets, capacity market      │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: ASV — Atrahasis Semantic Vocabulary (C4)          │
│  Purpose: Structured communication vocabulary                │
└─────────────────────────────────────────────────────────────┘
```

Data flows are bidirectional between adjacent and non-adjacent layers. See §9 for the complete contract directory.

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

Time ──────────────────────────────────────────────────────────►

SETTLEMENT_TICKS:  |1|2|3|...|58|59|60|1|2|3|...|58|59|60|...
                   └──── TIDAL_EPOCH 1 ───┘└──── TIDAL_EPOCH 2 ───┘
                   └────────────────── CONSOLIDATION_CYCLE (partial) ─
```

### 3.3 Intra-Tidal-Epoch Timeline

Within each TIDAL_EPOCH (3600s = 60 ticks):

```
Tick 1-55  (0:00 - 55:00): Normal operations
    • EABS settlement cycles (55 cycles)
    • V-class operations submitted to PCVM
    • B-class settlement rewards distributed per tick
    • C6 ingestion, circulation, catabolism

Tick 56-58 (55:00 - 58:00): Verification finalization
    • C5 audit selection (random deep-audit at tick 56)
    • C5 verification window closes
    • V-class settlement checkpoint

Tick 59    (58:00 - 59:00): Settlement reporting
    • C5 sends verification quality reports to C8
    • C6 sends metabolic efficiency reports to C8
    • C3 computes scheduling compliance scores

Tick 60    (59:00 - 60:00): Epoch boundary
    • C3 BOUNDARY_WINDOW operations (5s within this tick):
      - Capacity snapshot gossip
      - Hash ring reconstruction (if roster changed)
      - VRF seed rotation
      - Predictive model recalibration
    • C8 cumulative tidal settlement computation
    • G-class governance reward distribution
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

**INV-T1 (Temporal Consistency):** TIDAL_EPOCH = 60 × SETTLEMENT_TICK. This ratio is a constitutional parameter modifiable only through G-class governance with 90% supermajority.

---

## 4. Canonical Claim Class Taxonomy

### 4.1 Nine Canonical Classes

The Atrahasis verification system recognizes 9 claim classes, organized into 3 verification tiers. C5 (PCVM) is the authoritative classifier — no other layer may override PCVM's class assignment.

#### Tier 1: FORMAL_PROOF (2 classes)

**D-class (Deterministic).** A claim whose truth value is decidable by deterministic computation. Verification: replay computation on stated inputs. Examples: hash computations, sorting results, mathematical calculations.

**C-class (Compliance).** A claim that a system, process, or output conforms to a specified regulation, standard, or constitutional parameter. Verification: matching against a finite rule set. Examples: EU AI Act Article 11 compliance, constitutional parameter satisfaction.

#### Tier 2: STRUCTURED_EVIDENCE (5 classes)

**P-class (Process).** A claim that a specified process was followed during the production of another claim. Verification: check execution traces against declared process specification. Examples: research protocol adherence, pipeline stage execution.

**R-class (Reasoning).** A claim derived from logical inference over premises. Verification: check logical validity, premise support, and assumption disclosure. Examples: architectural arguments, I-confluence proofs.

**E-class (Empirical).** A claim derived from observation or measurement of external phenomena. Verification: check cited sources, cross-reference, assess source reliability. Examples: benchmark scores, market data, experimental results.

**S-class (Statistical).** A claim derived from statistical analysis of data. Verification: check methodology, sample adequacy, test appropriateness, conclusion validity. Examples: load balancing efficiency, performance comparisons.

**K-class (Knowledge Consolidation).** A claim produced by EMA's consolidation (dreaming) process, synthesizing patterns across multiple epistemic quanta from diverse sources. Verification: check source quantum provenance (≥5 agents, ≥3 parcels, no agent >30%), reasoning chain validity, falsification statement quality, and cross-domain coherence. K-class claims start with high uncertainty (u ≥ 0.4) and are subject to aging uncertainty increase without empirical validation.

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
  initial_opinion:      SLOpinion       # (b, d, u, a) with u ≥ 0.4, a = 0.6
  consolidation_cycle:  uint64          # Which cycle produced this
```

### 4.5 Aging Uncertainty for K-Class

K-class claims without empirical validation are subject to aging uncertainty increase:

```
aging_rate_k = 0.005 per TIDAL_EPOCH (per C6 Adversarial A2 mitigation)

IF tidal_epochs_since_creation > 100 AND NOT empirically_validated:
    u_new = min(u + aging_rate_k, 0.95)
    b_new = b × (1 - aging_rate_k / (1 - u))
    d unchanged
    Renormalize: b + d + u = 1
```

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
G → {M, B, X, V, G}    Governance may decompose into anything
V → {M, B, X}           Verification cannot spawn governance/verification
X → {M, B}              Exclusive decomposes into simpler operations
B → {M}                 Bounded decomposes only into merge reads
M → ∅                   Merge operations are terminal
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

### 6.1 C4 Epistemic Class → C5 Claim Class

C4 defines 6 epistemic classes for semantic annotation. These map to C5 claim classes as follows:

| C4 `epistemic_class` | Primary C5 Class | Override Condition | Override Class |
|----------------------|------------------|-------------------|----------------|
| `observation` | E (Empirical) | Evidence quality_class = "computational_result" | D (Deterministic) |
| `correlation` | S (Statistical) | — | — |
| `causation` | R (Reasoning) | Evidence includes experimental/RCT data | S (Statistical) |
| `inference` | R (Reasoning) | Confidence method = "model_derived" | H (Heuristic) |
| `prediction` | H (Heuristic) | Confidence method = "statistical" with interval | S (Statistical) |
| `prescription` | N (Normative) | — | — |

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

### 6.3 ASV Token → PCVM Intake Flow

```
C4 ASV Message:                    C5 PCVM Intake:
  CLM (claim)          ──────►      Claim content + proposed class
  CLM.epistemic_class  ──────►      Preliminary class (via §6.2 mapping)
  CNF (confidence)     ──────►      Initial SL opinion seed
  EVD[] (evidence)     ──────►      VTD dependencies
  PRV (provenance)     ──────►      VTD provenance chain
  VRF (verification)   ◄──────      MCT output (SL opinion + final class)
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

### 7.3 Claim Class → Settlement Mapping

| Claim Class | Difficulty Weight | Settlement Type | Rationale |
|-------------|------------------|-----------------|-----------|
| D | 1.0 | B-class fast | Recomputation — fast, cheap |
| C | 1.3 | B-class fast | Rule matching — fast, slightly complex |
| P | 1.5 | B-class fast | Trace checking — fast |
| E | 1.5 | V-class standard | Observation requires time |
| K | 1.8 | V-class standard | Consolidation requires multi-source verification |
| S | 2.0 | V-class standard | Sample accumulation |
| R | 2.0 | V-class standard | Logical verification |
| H | 2.5 | V-class standard | Expert review |
| N | 3.0 | G-class slow | Value judgments, governance review |

### 7.4 Capability Score (C8, unchanged)

```
effective_stake = AIC_collateral × min(1 + ln(1 + raw_score), 3.0)

raw_score = 0.4 × reputation
          + 0.4 × verification_track_record
          + 0.2 × claim_class_accuracy

claim_class_accuracy: evaluated across all 9 classes (VRF-assigned, not self-selected)
```

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
```

### 8.4 Subjective Logic

```
type SLOpinion = {
    belief:     float64  // b ≥ 0
    disbelief:  float64  // d ≥ 0
    uncertainty: float64 // u ≥ 0
    base_rate:  float64  // a ∈ [0, 1]
}
// Constraint: b + d + u = 1
// Expected probability: E(w) = b + a × u
```

### 8.5 Economic Types

```
type AIC           = decimal(18, 8)  // Atrahasis Intelligence Coin
type ProtocolCredit = decimal(18, 8) // Non-transferable, 10%/tick decay
type CapacitySlice = uint64          // CSO-backed resource unit
```

---

## 9. Integration Contract Directory

### 9.1 Contract Matrix

```
         C3    C4    C5    C6    C7    C8
C3       —     →     ↔     ↔     ↔     ↔
C4       —     —     —     →     →     →
C5       ←     —     —     ↔     →     →
C6       ←     ←     ←     —     →     →
C7       ←     ←     ←     ←     —     ↔
C8       ←     ←     ←     ←     ←     —

→ = provides data to
← = receives data from
↔ = bidirectional
— = no direct contract
```

### 9.2 Contract Details

**C3 → C5:** VRF output per tidal epoch (committee selection), operation scheduling for V-class.
**C5 → C3:** Verification results fed to settlement calculator.

**C3 → C6:** Epoch boundary notifications, parcel topology changes.
**C6 → C3:** Locus-scoped knowledge summaries per tidal epoch.

**C3 ↔ C7:** C3 provides scheduling, G-class voting, VRF, topology. C7 submits leaf intents, settlement entries.

**C3 ↔ C8:** C3 provides CRDT infrastructure, Sentinel Graph clustering. C8 replicates ledger state via C3 PN-Counters.

**C4 → C6:** ASV tokens (CLM/CNF/EVD/PRV) enter EMA via ingestion pipeline.
**C4 → C7:** INT claim type for intent provenance chains.
**C4 → C8:** Economic message schemas.

**C5 ↔ C6:** C5 provides MCTs, VTDs, claim classification. C6 submits K-class VTDs, triggers re-verification.

**C5 → C7:** Agent credibility scores, claim class assessments.
**C5 → C8:** Verification reports, credibility scores, attestations.

**C6 → C7:** Knowledge projections, SHREC state, metabolic phase (read-only).
**C6 → C8:** Knowledge contribution reports, metabolic efficiency.

**C7 ↔ C8:** C7 submits intent budgets, task completions. C8 provides stake availability queries.

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

**E-C4-01:** C4 should add an informative appendix (non-normative) describing its position in the Atrahasis stack and the epistemic_class → claim_class mapping from §6.1 of this document. C4's core specification is unchanged.

### 10.3 C5 PCVM

**E-C5-01:** C5's 8-class taxonomy should be extended to 9 classes with the addition of K-class (Knowledge Consolidation) as defined in §4.1 of this document. K-class parameters: Tier 2, committee size 5, admission threshold 0.70, base rate 0.6, half-life 120 days.

**E-C5-02:** Conservatism ordering updated from `H > N > E > S > R > P > C > D` to `H > N > K > E > S > R > P > C > D`.

### 10.4 C6 EMA

**E-C6-01:** C6's claim class mapping table (Lines 469-478) should replace "C (Consolidation)" with "K (Knowledge Consolidation)". All references to submitting consolidation outputs "as C-class claims" should read "as K-class claims".

**E-C6-02:** C6's `claim_class` field in the EpistemicQuantum definition (Line 251) should use the 9-class enum: `D|E|S|H|N|P|R|C|K`.

### 10.5 C7 RIF

**E-C7-01:** C7's Settlement Router (§11.5) references "C3 settlement ledger". This should read "C8 DSF settlement ledger, accessed via C3's CRDT replication infrastructure".

### 10.6 C8 DSF

**E-C8-01:** C8's claim class difficulty weights (Lines 3837-3841) should use the full 9-class table from §7.3 of this document. The "P (Primary) x1.0, R (Replication) x0.7, C (Challenge) x1.3" modifiers are removed — P, R, and C are full claim classes, not modifiers.

**E-C8-02:** C8's `epoch_duration_ms` (60000ms) corresponds to SETTLEMENT_TICK in the canonical temporal hierarchy. All C8 epoch references are SETTLEMENT_TICKs. No change to C8's internal logic is required.

---

## 11. Invariants

### 11.1 Temporal Invariants

**INV-T1 (Epoch Ratio).** TIDAL_EPOCH = 60 × SETTLEMENT_TICK. Constitutional parameter.

**INV-T2 (Consolidation Ratio).** CONSOLIDATION_CYCLE = 10 × TIDAL_EPOCH. Governance-configurable.

**INV-T3 (Boundary Ordering).** Settlement tick boundaries are subsets of tidal epoch boundaries. Every tidal epoch boundary is also a settlement tick boundary. Not every settlement tick boundary is a tidal epoch boundary.

### 11.2 Classification Invariants

**INV-C1 (PCVM Sovereignty).** PCVM (C5) is the sole authority for claim class assignment. No other layer may override PCVM's classification.

**INV-C2 (Conservatism).** When classification inputs disagree, the most conservative class is selected per the ordering H > N > K > E > S > R > P > C > D.

**INV-C3 (Completeness).** Every claim entering any layer's knowledge store must have a PCVM-assigned class. No unclassified claims exist in the canonical state.

**INV-C4 (K-Class Provenance).** K-class claims must have source quanta from ≥5 independent agents across ≥3 parcels, with no single agent contributing >30%.

### 11.3 Settlement Invariants

**INV-S1 (Authority).** C8 DSF is the sole settlement authority. C3's settlement calculator feeds data to C8; it does not independently settle.

**INV-S2 (Monotonic Difficulty).** Difficulty weights are weakly monotonically increasing with conservatism ordering (within each verification tier).

**INV-S3 (Complete Coverage).** Every claim class has a defined difficulty weight and settlement type. No claim class is unsettleable.

---

## 12. Conformance Requirements

### 12.1 Mandatory

Any implementation of the Atrahasis stack MUST:

1. Use the three-tier temporal hierarchy from §3
2. Support all 9 claim classes from §4
3. Implement the C4→C5 mapping from §6 for ASV message intake
4. Route all settlement through C8 DSF per §7
5. Use canonical type definitions from §8 for cross-layer communication

### 12.2 Recommended

Implementations SHOULD:

1. Include this document's errata (§10) in their copies of layer-specific specs
2. Validate cross-layer contracts (§9) at integration testing time
3. Monitor INV-T1 through INV-S3 at runtime

---

## Appendix A: Claim Class Quick Reference

```
┌──────────────────────────────────────────────────────────────────────┐
│ TIER 1: FORMAL_PROOF (committee: 3)                                  │
│   D — Deterministic    threshold: 0.95  weight: 1.0  settle: B-fast │
│   C — Compliance       threshold: 0.90  weight: 1.3  settle: B-fast │
├──────────────────────────────────────────────────────────────────────┤
│ TIER 2: STRUCTURED_EVIDENCE (committee: 5)                           │
│   P — Process          threshold: 0.80  weight: 1.5  settle: B-fast │
│   R — Reasoning        threshold: 0.75  weight: 2.0  settle: V-std  │
│   E — Empirical        threshold: 0.60  weight: 1.5  settle: V-std  │
│   S — Statistical      threshold: 0.65  weight: 2.0  settle: V-std  │
│   K — Knowledge Consol threshold: 0.70  weight: 1.8  settle: V-std  │
├──────────────────────────────────────────────────────────────────────┤
│ TIER 3: STRUCTURED_ATTESTATION (committee: 7)                        │
│   H — Heuristic        threshold: 0.50  weight: 2.5  settle: V-std  │
│   N — Normative        threshold: 0.50  weight: 3.0  settle: G-slow │
└──────────────────────────────────────────────────────────────────────┘

Conservatism: H > N > K > E > S > R > P > C > D
```

---

## Appendix B: Epoch Hierarchy Derivation Proof

**Claim:** The three-tier temporal hierarchy introduces no contradictions with existing C3, C5, C6, C7, or C8 parameters.

**Proof:**

1. **C3 consistency:** C3 defines EPOCH_DURATION = 3600s. We define TIDAL_EPOCH = 3600s. Identity mapping. ✓

2. **C5 consistency:** C5 references "1-hour tidal epoch clock" with verification window T+0 to T+50min. TIDAL_EPOCH = 3600s = 60 minutes. T+50min = tick 51 of 60. ✓

3. **C6 consistency:** C6 defines consolidation "every N epochs (default N=10)". With TIDAL_EPOCH = 3600s, this gives CONSOLIDATION_CYCLE = 10 × 3600s = 36000s = 10 hours. ✓

4. **C7 consistency:** C7 references "settlement lag up to 32 epochs". With TIDAL_EPOCH = 3600s, this gives 32 hours maximum lag. C7's staleness tolerance of "5 epochs" = 5 hours. These are coordination-scale timescales, consistent with TIDAL_EPOCH. ✓

5. **C8 consistency:** C8 defines epoch_duration_ms = 60000. We define SETTLEMENT_TICK = 60s = 60000ms. Identity mapping. C8's internal EABS logic, throughput benchmarks (42K msg/s at 60s), and staleness bounds (~63s) are all unchanged. ✓

6. **Inter-tier consistency:** 60 SETTLEMENT_TICKs × 60s = 3600s = 1 TIDAL_EPOCH. The ratio is exact (integer). Tidal epoch boundaries are aligned with settlement tick boundaries (tick 60 of each tidal epoch = epoch boundary). ✓

**QED.** □

---

## Appendix C: Configurable Parameters

| # | Parameter | Default | Range | Authority | Section |
|---|-----------|---------|-------|-----------|---------|
| 1 | SETTLEMENT_TICK_DURATION | 60s | [30s, 300s] | C8 | §3.1 |
| 2 | TICKS_PER_TIDAL_EPOCH | 60 | [12, 120] | C9 (constitutional) | §3.1 |
| 3 | TIDAL_EPOCHS_PER_CONSOLIDATION | 10 | [5, 50] | C6 | §3.1 |
| 4 | K_CLASS_ADMISSION_THRESHOLD | 0.70 | [0.60, 0.85] | C9 | §4.3 |
| 5 | K_CLASS_BASE_RATE | 0.6 | [0.5, 0.7] | C9 | §4.3 |
| 6 | K_CLASS_HALF_LIFE_DAYS | 120 | [60, 365] | C9 | §4.5 |
| 7 | K_CLASS_AGING_RATE | 0.005/epoch | [0.001, 0.01] | C9 | §4.5 |
| 8 | K_CLASS_AGING_THRESHOLD_EPOCHS | 100 | [50, 500] | C9 | §4.5 |
| 9 | K_CLASS_DIFFICULTY_WEIGHT | 1.8 | [1.2, 2.5] | C9 | §7.3 |
| 10 | K_CLASS_MIN_SOURCE_AGENTS | 5 | [3, 10] | C6 | §4.4 |
| 11 | K_CLASS_MIN_SOURCE_PARCELS | 3 | [2, 5] | C6 | §4.4 |
| 12 | K_CLASS_MAX_AGENT_CONCENTRATION | 0.30 | [0.20, 0.50] | C6 | §4.4 |

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
| EABS | Epoch-Anchored Batch Settlement — C8's write protocol | C8 |
| MCT | Membrane Clearance Token — C5's verification output | C5 |
| VTD | Verification Trace Document — C5's proof artifact | C5 |
| SL Opinion | Subjective Logic opinion tuple (b, d, u, a) | C5 |
| CSO | Certified Slice Object — proof-carrying resource right | C3/C8 |
| K-class | Knowledge Consolidation claim — EMA dreaming output | C9 |
| AIC | Atrahasis Intelligence Coin — economic token | C8 |
| Protocol Credit | Non-transferable spam-control token, 10%/tick decay | C8 |
| Capacity Slice | CSO-backed resource unit for compute/storage/bandwidth | C8 |

---

*End of Cross-Layer Reconciliation Addendum v1.0.0*
