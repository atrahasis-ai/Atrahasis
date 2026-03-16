# Epistemic Metabolism Architecture (EMA)

## Master Technical Specification - v2.0.4

| Field | Value |
|---|---|
| **Title** | Epistemic Metabolism Architecture (EMA) |
| **Version** | 2.0.4 |
| **Supersedes** | v1.0.0 (C6 original), Patch Addendum v1.1 (PA-1 through PA-12), C10 SHREC/Coherence Hardening, C10 Defense-in-Depth Â§3, C13 CRP+ (see Supersession Note below) |
| **Classification** | DESIGN â€” Unified Specification |
| **Cycle** | C6 (unified rewrite) |
| **Date** | 2026-03-12 |

---

**Abstract.**
The Epistemic Metabolism Architecture (EMA) treats verified knowledge as a living substance â€” ingested from external sources, circulated through active reasoning, consolidated during offline "dreaming" phases, and eventually catabolised when no longer viable. Every knowledge fragment (an *epistemic quantum*) carries a subjective-logic opinion tuple and participates in a coherence graph whose edge dynamics enforce global consistency. A five-signal regulatory layer (SHREC) governs resource allocation through Lotka-Volterra ecological competition with a four-regime graduated controller. A seven-mechanism Consolidation Robustness Protocol (CRP+) hardens the dreaming pipeline against consolidation-poisoning attacks. Sharded coherence graph management enables scaling to billion-quantum deployments. This document is the single canonical reference for the EMA subsystem.

---

> **Supersession Note â€” C6/C13 Relationship:** This document supersedes C13 CRP+ with respect to the *specification and integration* of the seven CRP+ mechanisms (M1â€“M7), the credibility ladder, the novelty pathway, consolidation depth limits, immune memory, and CRP+ combined scoring. All normative requirements from C13 are absorbed here as CR-CRP1 through CR-CRP23, and all CRP+ invariants as INV-CRP1 through INV-CRP8. However, **C13 retains independent authority** over: (1) the original threat model and attack taxonomy for consolidation poisoning, which provides the security rationale referenced but not duplicated here; (2) the formal proofs and detection-rate analysis (including the 0.434â†’0.611 detection improvement metrics) that justify CRP+ mechanism design choices; and (3) any future C13-specific amendments to the consolidation-poisoning threat model that have not yet been integrated into C6. C13 is **not deprecated** â€” it remains the authoritative source for consolidation-poisoning threat analysis. Implementers SHOULD consult C13 for threat-model context and C6 for normative mechanism specifications.

---

## Table of Contents

1. [Introduction and Motivation](#1-introduction-and-motivation)
2. [Background and Related Work](#2-background-and-related-work)
3. [Architecture Overview](#3-architecture-overview)
4. [The Epistemic Quantum](#4-the-epistemic-quantum)
5. [Metabolic Processes](#5-metabolic-processes)
6. [SHREC â€” Stratified Homeostatic Regulation with Ecological Competition](#6-shrec)
7. [Coherence Graph](#7-coherence-graph)
   - 7.6 [Contradiction Lattice](#76-contradiction-lattice)
8. [Projection Engine](#8-projection-engine)
9. [Retrieval](#9-retrieval)
10. [Integration with Atrahasis Subsystems](#10-integration)
11. [Security Considerations](#11-security)
12. [Scalability and Deployment](#12-scalability)
13. [Open Questions and Future Work](#13-open-questions)
14. [Conclusion](#14-conclusion)
- [Appendix A: Canonical JSON Schema](#appendix-a)
- [Appendix B: State-Machine Transition Table](#appendix-b)
- [Appendix C: Reference Algorithms](#appendix-c)
- [Appendix D: Parameter Table and Deployment Profiles](#appendix-d)
- [Appendix E: Conformance Requirements](#appendix-e)
- [Appendix F: Test Vectors](#appendix-f)
- [Appendix G: Cross-Reference Matrix](#appendix-g)
- [Appendix H: Glossary](#appendix-h)
- [Changelog](#changelog)

---

## 1  Introduction and Motivation

### 1.1  The Knowledge Lifecycle Problem

Contemporary AI systems treat knowledge as a static store â€” facts are added, occasionally updated, and implicitly trusted once present. This model breaks down when:

1. **Source reliability varies.** A peer-reviewed journal and a blog post should not carry equal epistemic weight.
2. **Knowledge decays.** Empirical findings are superseded; statistical relationships drift.
3. **Contradictions emerge.** Independent sources may assert mutually exclusive claims; the system must reason about, not merely detect, such conflicts.
4. **Scale defeats naÃ¯ve consistency.** Global coherence checking is O(nÂ²) in the number of knowledge fragments; billion-scale deployments demand structural innovation.
5. **Consolidation introduces risk.** Offline synthesis ("dreaming") can be exploited to launder low-credibility claims into high-trust consolidated knowledge.

EMA addresses all five by modelling knowledge as a metabolic process: quanta are *ingested*, *circulated*, *consolidated*, and *catabolised* under continuous homeostatic regulation, with a hardened consolidation pipeline providing defense in depth.

### 1.2  Design Principles

| Principle | Manifestation |
|---|---|
| **Epistemic humility** | Every quantum carries explicit uncertainty via subjective-logic opinions (b, d, u, a). |
| **Ecological resource management** | Lotka-Volterra competition allocates finite processing budget across metabolic functions. |
| **Graduated regulatory control** | Four-regime SHREC controller (NORMAL â†’ ELEVATED â†’ CRITICAL â†’ EMERGENCY) provides proportional response to system stress. |
| **Coherence as structure** | A typed, weighted graph (SUPPORT, CONTRADICTION, DERIVATION, ANALOGY, SUPERSESSION) replaces ad-hoc consistency checks. |
| **Bounded projections** | Lossy but bounded-error projections serve peer subsystems (C3, C4, C5) without exposing internal complexity. |
| **Defense in depth** | Seven-mechanism CRP+ protocol, source independence verification, adversarial probing, and consolidation lineage tracking protect the dreaming pipeline. |
| **Metabolic lifecycle** | Two-phase catabolism (quarantine â†’ dissolution with evidence recycling) ensures graceful knowledge retirement. |

### 1.3  Scope

This specification defines:

- The epistemic quantum data model (Section 4).
- Four metabolic processes: ingestion, circulation, consolidation, catabolism (Section 5).
- The SHREC regulatory layer with four-regime controller (Section 6).
- The sharded coherence graph with tiered update strategies (Section 7).
- The projection engine for C3/C4/C5 subsystem interfaces (Section 8).
- Retrieval interfaces (Section 9).
- Integration points with Atrahasis subsystems including PCVM degraded mode (Section 10).
- Security considerations including CRP+ consolidation defense (Section 11).
- Scalability design with T1â€“T4 scale tiers and deployment profiles (Section 12).

### 1.4  Normative Language

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used per RFC 2119.

### 1.5  Temporal Hierarchy

EMA operates on a three-tier temporal hierarchy established by the Atrahasis temporal framework:

| Tier | Name | Duration | Purpose |
|---|---|---|---|
| T-1 | `SETTLEMENT_TICK` | 60 s | Fine-grained opinion updates, edge weight adjustments, vitality recalculation |
| T-2 | `TIDAL_EPOCH` | 3 600 s (1 h) | SHREC regulation cycle, coherence graph maintenance, catabolism evaluation |
| T-3 | `CONSOLIDATION_CYCLE` | 36 000 s (10 h) | Dreaming/consolidation pipeline execution (= 10 TIDAL_EPOCHs) |

All temporal references in this specification use these canonical durations.

---

## 2  Background and Related Work

### 2.1  Subjective Logic

JÃ¸sang's subjective-logic framework represents epistemic states as opinion tuples Ï‰ = (b, d, u, a) where:

- **b** (belief): evidence-based support for a proposition.
- **d** (disbelief): evidence-based opposition.
- **u** (uncertainty): uncommitted evidence mass.
- **a** (base rate): prior probability in the absence of evidence.
- **Constraint:** b + d + u = 1, with 0 â‰¤ a â‰¤ 1.

The *projected probability* P(Ï‰) = b + a Â· u maps opinions to point probabilities when needed.

EMA uses subjective logic as its native epistemic representation, enabling principled fusion (cumulative/averaging), discounting, and deduction across all metabolic processes.

### 2.2  Lotka-Volterra Dynamics

The classical Lotka-Volterra competition model governs how species with overlapping niches share resources:

```
dNáµ¢/dt = ráµ¢ Â· Náµ¢ Â· (1 - (Náµ¢ + Î£â±¼ Î±áµ¢â±¼ Â· Nâ±¼) / Káµ¢)
```

where ráµ¢ is intrinsic growth, Káµ¢ is carrying capacity, and Î±áµ¢â±¼ is competition coefficient.

EMA adapts this model: the five metabolic "species" (ingestion, circulation, consolidation, catabolism, coherence maintenance) compete for a fixed processing budget. SHREC signals modulate competition coefficients rather than directly setting allocations, enabling emergent, self-organising resource distribution.

### 2.3  Coherence Graphs

EMA's coherence graph extends labelled-graph approaches (Thagard's ECHO, Brewka's preferred subtheories) with:

- Typed edges (five canonical types).
- Weight decay tied to the temporal hierarchy.
- Shard-based partitioning for scale.
- Cross-shard border graphs for global consistency.

### 2.4  W3C PROV Provenance Model

All epistemic quanta carry W3C PROV-compatible provenance records (prov:Entity, prov:Activity, prov:Agent), enabling full lineage tracking from ingestion through consolidation to dissolution.

### 2.5  Consolidation Poisoning Threat Model

The dreaming/consolidation pipeline synthesises new knowledge from clusters of existing quanta. This creates an attack surface: an adversary who controls a subset of ingested sources can craft inputs designed to:

1. Launder low-credibility claims into high-trust K-class consolidated knowledge.
2. Exploit the trust amplification inherent in synthesis.
3. Gradually shift the system's belief state through repeated consolidation cycles.

The CRP+ protocol (Section 5.3.4) and defense-in-depth measures (Section 5.3.3) address this threat systematically.

---

## 3  Architecture Overview

### 3.1  System Context

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    ATRAHASIS CORE                          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚   C3    â”‚  â”‚   C4    â”‚  â”‚   C5    â”‚  â”‚    PCVM     â”‚  â”‚
â”‚  â”‚ Tidal   â”‚  â”‚  ASV    â”‚  â”‚ SentGr  â”‚  â”‚  Proof      â”‚  â”‚
â”‚  â”‚Noosph.  â”‚  â”‚  Comms  â”‚  â”‚  Graph  â”‚  â”‚  Chains     â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚       â”‚            â”‚            â”‚               â”‚          â”‚
â”‚       â–¼            â–¼            â–¼               â–¼          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚              C6 â€” EMA (this spec)                    â”‚  â”‚
â”‚  â”‚                                                      â”‚  â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚  â”‚
â”‚  â”‚  â”‚ Ingest   â”‚ â”‚ Circulateâ”‚ â”‚Consolidatâ”‚ â”‚Catabol â”‚  â”‚  â”‚
â”‚  â”‚  â”‚          â”‚ â”‚          â”‚ â”‚  + CRP+  â”‚ â”‚  ise   â”‚  â”‚  â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚  â”‚
â”‚  â”‚       â–²            â–²            â–²            â–²       â”‚  â”‚
â”‚  â”‚       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜       â”‚  â”‚
â”‚  â”‚                    â”Œâ”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”                     â”‚  â”‚
â”‚  â”‚                    â”‚   SHREC   â”‚                     â”‚  â”‚
â”‚  â”‚                    â”‚ 4-regime  â”‚                     â”‚  â”‚
â”‚  â”‚                    â”‚controller â”‚                     â”‚  â”‚
â”‚  â”‚                    â””â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜                     â”‚  â”‚
â”‚  â”‚                    â”Œâ”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”                     â”‚  â”‚
â”‚  â”‚                    â”‚ Coherence â”‚                     â”‚  â”‚
â”‚  â”‚                    â”‚  Graph    â”‚                     â”‚  â”‚
â”‚  â”‚                    â”‚ (sharded) â”‚                     â”‚  â”‚
â”‚  â”‚                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                     â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 3.2  Metabolic Pipeline Overview

```
External   â”€â”€â–º  INGEST  â”€â”€â–º  CIRCULATE  â”€â”€â–º  CONSOLIDATE  â”€â”€â–º  output
Sources         (gate)       (active)        (dreaming)        K-class
                  â”‚                              â”‚              quanta
                  â”‚                              â–¼
                  â”‚                         â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                  â”‚                         â”‚  CRP+   â”‚
                  â”‚                         â”‚ 7-mech  â”‚
                  â”‚                         â”‚ defense â”‚
                  â”‚                         â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜
                  â”‚                              â”‚
                  â”‚                              â–¼
                  â–¼                          PCVM gate
              CATABOLISE  â—„â”€â”€  (vitality < floor for grace period)
              quarantine
              then dissolve
              (evidence recycled)
```

### 3.3  System Invariants

The following invariants MUST hold at all times:

**Core EMA Invariants (INV-E1 through INV-E10):**

| ID | Invariant | Description |
|---|---|---|
| **INV-E1** | Opinion conservation | b + d + u = 1 for every opinion tuple. |
| **INV-E2** | Provenance completeness | Every quantum has a non-empty provenance chain traceable to at least one external source or a consolidation act. |
| **INV-E3** | Edge symmetry | If quantum A has an edge to quantum B of type T, then B has a reciprocal edge to A of the same type T. |
| **INV-E4** | Budget conservation | The sum of all metabolic process allocations equals the total processing budget (within floating-point tolerance Îµ = 1e-9). |
| **INV-E5** | Vitality non-negativity | Vitality â‰¥ VITALITY_FLOOR (0.05) for all quanta not in QUARANTINED or DISSOLVED state. Grace period of 5 epochs applies before catabolism candidacy. |
| **INV-E6** | State-machine validity | Every quantum occupies exactly one lifecycle state; only transitions listed in the state-machine table (Appendix B) are permitted. |
| **INV-E7** | Coherence monotonicity (local) | Within a single TIDAL_EPOCH, the number of unresolved contradictions MUST NOT increase by more than 10%. |
| **INV-E8** | Catabolism evidence recycling | When a quantum is dissolved, all outgoing SUPPORT and DERIVATION edges are examined; child quanta with >50% belief derived from the dissolved parent MUST be flagged for re-evaluation. |
| **INV-E9** | Projection fidelity bounds | Each projection type (C3, C4, C5) maintains measured round-trip fidelity above its minimum threshold. |
| **INV-E10** | Claim-class immutability | A quantum's claim_class MUST NOT change after initial classification, except via K-class consolidation or administrative G-class override. |

**SHREC Controller Invariants (INV-E11 through INV-E14):**

| ID | Invariant | Description |
|---|---|---|
| **INV-E11** | Budget conservation under all regimes | The sum of all five metabolic allocations equals 1.0 (within Îµ = 1e-9) after every SHREC epoch step, regardless of active regime. |
| **INV-E12** | Floor enforcement after combination | Every metabolic allocation â‰¥ its floor value after the combine step. No regime may drive an allocation below its floor. |
| **INV-E13** | Regime monotonicity within epoch | The regime level MUST NOT decrease within a single epoch step. Downgrades require HYSTERESIS_EPOCHS (5) consecutive epochs at reduced stress. |
| **INV-E14** | Emergency freeze stability | While in EMERGENCY regime, allocations MUST remain identical to the values frozen at entry (within Îµ = 1e-9). |

**Coherence Sharding Invariants (INV-E15 through INV-E19):**

| ID | Invariant | Description |
|---|---|---|
| **INV-E15** | Shard quantum limit | No shard contains more than MAX_QUANTA_PER_SHARD (1 000 000) active quanta. |
| **INV-E16** | Cross-edge representation | Every cross-shard edge appears in both endpoint shards' cross_edges sets AND in the border graph. |
| **INV-E17** | Tier consistency | Edge tier classification (HOT/WARM/COLD) is consistent with access frequency thresholds. |
| **INV-E18** | Budget enforcement | Shard intra-edge count â‰¤ MAX_INTRA_EDGES_PER_SHARD; cross-edge count â‰¤ MAX_CROSS_EDGES_PER_SHARD. |
| **INV-E19** | Border graph completeness | The border graph contains exactly the set of cross-shard edges that exist across all shards. |

**CRP+ Invariants (INV-CRP1 through INV-CRP8):**

| ID | Invariant | Description |
|---|---|---|
| **INV-CRP1** | Pipeline completeness | Every consolidation candidate MUST pass through all applicable CRP+ mechanisms before PCVM submission. |
| **INV-CRP2** | VRF unpredictability | VRF selection outcomes MUST NOT be predictable from public inputs alone; the secret key is never exposed. |
| **INV-CRP3** | Credibility ladder monotonicity | Rung promotions require sustained evidence accumulation over â‰¥ PROMOTION_OBSERVATION_WINDOW epochs; demotions are immediate upon threshold violation. |
| **INV-CRP4** | Depth limit enforcement | Quanta at SPECULATIVE or PROVISIONAL rungs MUST NOT participate as sources in consolidation synthesis. |
| **INV-CRP5** | Immune memory bounded growth | Immune memory store grows at most O(n) with total quarantine/rejection events; garbage collection runs every epoch. |
| **INV-CRP6** | Novelty pathway integrity | N3 paradigmatic claims entering the novelty pathway MUST complete all four enhanced checks (enhanced APRT, constructive adversarial probing, temporal quarantine, provenance deep audit) before standard pathway admission. |
| **INV-CRP7** | Score reproducibility | CRP+ combined scores MUST be deterministically reproducible given the same inputs and VRF proof. |
| **INV-CRP8** | Constitutional parameter protection | Parameters marked as constitutional MUST NOT be modified without G-class governance approval. |

### 3.4  Claim Classes

EMA recognises nine canonical claim classes, each governing admission thresholds, committee sizes, aging rates, and consolidation eligibility:

| Code | Name | Committee Size | Admission Threshold | Difficulty Weight | Base Rate | Half-Life |
|---|---|---|---|---|---|---|
| **D** | Definitional | 3 | 0.85 | 0.5 | 0.9 | âˆž |
| **E** | Empirical | 5 | 0.70 | 1.0 | 0.5 | 90 days |
| **S** | Statistical | 5 | 0.75 | 1.2 | 0.5 | 60 days |
| **H** | Heuristic | 3 | 0.60 | 0.8 | 0.6 | 180 days |
| **N** | Normative | 3 | 0.65 | 0.7 | 0.5 | 365 days |
| **P** | Predictive | 5 | 0.80 | 1.5 | 0.4 | 30 days |
| **R** | Relational | 3 | 0.70 | 0.9 | 0.6 | 120 days |
| **C** | Compliance | 3 | 0.90 | 0.3 | 0.95 | âˆž |
| **K** | Knowledge Consolidation | 5 | 0.70 | 1.8 | 0.6 | 120 days |

> **Note on K-class vs C-class:** In versions prior to v2.0, the letter "C" was overloaded between Compliance claims and Consolidation outputs. K-class (Knowledge Consolidation) now exclusively denotes quanta produced by the dreaming/consolidation pipeline. C-class exclusively denotes Compliance claims. The K-class aging rate is 0.005 per TIDAL_EPOCH.

> **Canonical conservatism ordering (C9):** The nine claim classes are ordered by epistemic conservatism â€” the degree of evidentiary caution required before a claim is admitted and propagated. The canonical ordering from most conservative to least conservative is: **H > N > K > E > S > R > P > C > D**. This ordering governs tie-breaking in cross-class coherence conflicts, priority in resource-constrained consolidation scheduling, and default committee skepticism levels. As the primary K-class consumer, EMA MUST respect this ordering when resolving conflicts between K-class consolidated outputs and claims of other classes.

### 3.5  Processing Budget

The total processing budget is normalised to 1.0 and divided among five metabolic functions:

| Function | Symbol | Default Allocation | Floor |
|---|---|---|---|
| Ingestion | N_ingest | 0.25 | 0.05 |
| Circulation | N_circ | 0.30 | 0.10 |
| Consolidation | N_consol | 0.20 | 0.05 |
| Catabolism | N_catab | 0.10 | 0.05 |
| Coherence maintenance | N_coher | 0.15 | 0.05 |

Allocations are adjusted every TIDAL_EPOCH by the SHREC controller (Section 6). Floors are enforced under all regimes (INV-E12).

---

## 4  The Epistemic Quantum

### 4.1  Data Model

An epistemic quantum is the fundamental unit of knowledge in EMA. It is represented as a 10-tuple:

```
EQ = (id, content, opinion, provenance, edges, metabolic_state,
      projections, timestamps, dissolution_record, claim_class)
```

| Field | Type | Description |
|---|---|---|
| `id` | UUID v4 | Globally unique identifier. Immutable after creation. |
| `content` | StructuredClaim | The knowledge assertion itself â€” a typed, machine-readable claim. |
| `opinion` | (b, d, u, a) | Subjective-logic opinion tuple. b + d + u = 1 (INV-E1). |
| `provenance` | W3C PROV chain | Full lineage from source through transformations. |
| `edges` | Set\<Edge\> | Connections to other quanta in the coherence graph (Section 7). |
| `metabolic_state` | Enum | Current lifecycle state (Section 4.3). |
| `projections` | Map\<Target, Projection\> | Cached lossy projections for C3, C4, C5 subsystems. |
| `timestamps` | TimestampRecord | Created, last_accessed, last_modified, floor_entry_epoch, quarantine_entry_epoch. |
| `dissolution_record` | DissolutionRecord? | Non-null only for DISSOLVED quanta. Contains dissolution reason, evidence redistribution log. |
| `claim_class` | Enum{D,E,S,H,N,P,R,C,K} | One of nine canonical classes (Section 3.4). Immutable after classification (INV-E10). |

### 4.2  Opinion Semantics

#### 4.2.1  Representation

Every quantum carries an opinion Ï‰ = (b, d, u, a):

```python
@dataclass(frozen=True)
class Opinion:
    b: float  # belief âˆˆ [0, 1]
    d: float  # disbelief âˆˆ [0, 1]
    u: float  # uncertainty âˆˆ [0, 1]
    a: float  # base rate âˆˆ [0, 1]

    def __post_init__(self):
        assert abs(self.b + self.d + self.u - 1.0) < 1e-9, "INV-E1 violation"
        assert 0 <= self.a <= 1

    @property
    def projected_probability(self) -> float:
        return self.b + self.a * self.u
```

#### 4.2.2  Fusion Operations

EMA employs two fusion strategies:

- **Cumulative fusion (âŠ•):** Used when combining independent evidence from different sources. Accumulates evidence, reducing uncertainty.
- **Averaging fusion (âŠ›):** Used when combining dependent or same-source evidence. Averages beliefs without reducing uncertainty.

```python
def cumulative_fuse(w1: Opinion, w2: Opinion) -> Opinion:
    """JÃ¸sang cumulative fusion for independent sources."""
    k = w1.u + w2.u - w1.u * w2.u
    if k < 1e-12:
        return Opinion(b=(w1.b + w2.b) / 2, d=(w1.d + w2.d) / 2, u=0.0, a=(w1.a + w2.a) / 2)
    b = (w1.b * w2.u + w2.b * w1.u) / k
    d = (w1.d * w2.u + w2.d * w1.u) / k
    u = (w1.u * w2.u) / k
    a = (w1.a + w2.a) / 2  # average base rate
    return Opinion(b=b, d=d, u=u, a=a)

def discount(source_opinion: Opinion, claim_opinion: Opinion) -> Opinion:
    """Discount a claim opinion by source trustworthiness."""
    b = source_opinion.b * claim_opinion.b
    d = source_opinion.b * claim_opinion.d
    u = 1 - b - d
    return Opinion(b=b, d=d, u=u, a=claim_opinion.a)
```

#### 4.2.3  Opinion Freezing

During PCVM outage (Section 10.1), opinions are frozen:

```python
@dataclass
class QuantumOpinionState:
    opinion: Opinion
    opinion_frozen: bool = False  # True during PCVM degraded mode
```

When `opinion_frozen` is True, no fusion or update operations are permitted on the quantum's opinion. Opinions unfreeze when PCVM recovers and queued verifications drain.

### 4.3  Lifecycle State Machine

Each quantum occupies exactly one of six states:

```
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    external â”€â”€â”€â”€â”€â”€â–ºâ”‚ INGESTED â”‚
    source          â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜
                         â”‚ classify + initial opinion
                         â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚  ACTIVE  â”‚â—„â”€â”€â”€ re-evaluation
                    â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜     (from QUARANTINED)
                         â”‚
              â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
              â”‚          â”‚          â”‚
              â–¼          â–¼          â–¼
         â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
         â”‚CONSOLI-â”‚ â”‚DORMANT â”‚ â”‚QUARANTINEDâ”‚
         â”‚DATED   â”‚ â”‚        â”‚ â”‚           â”‚
         â””â”€â”€â”€â”¬â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”¬â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜
             â”‚          â”‚            â”‚
             â”‚          â”‚ reactivate â”‚ dissolve
             â”‚          â–¼            â–¼
             â”‚     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
             â””â”€â”€â”€â”€â–ºâ”‚  ACTIVE  â”‚ â”‚DISSOLVED â”‚
                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

| State | Description | Allowed Transitions |
|---|---|---|
| **INGESTED** | Newly arrived, awaiting classification and initial opinion formation. | â†’ ACTIVE |
| **ACTIVE** | Participating in reasoning, edge formation, and retrieval. | â†’ DORMANT, â†’ QUARANTINED, â†’ CONSOLIDATED |
| **DORMANT** | Low access frequency; excluded from hot-tier coherence updates. | â†’ ACTIVE (reactivation), â†’ QUARANTINED |
| **CONSOLIDATED** | Product of dreaming pipeline; carries K-class claim_class. | â†’ ACTIVE (upon re-verification) |
| **QUARANTINED** | Under review for catabolism or re-evaluation. | â†’ ACTIVE (re-evaluation succeeds), â†’ DISSOLVED |
| **DISSOLVED** | Terminal state. Content removed, provenance and dissolution_record retained. | (none â€” terminal) |

State transitions are governed by the transition table in Appendix B.

### 4.4  Vitality Computation

Vitality is a composite health score that determines catabolism candidacy:

```python
VITALITY_FLOOR = 0.05
VITALITY_GRACE_PERIOD = 5  # TIDAL_EPOCHs

def compute_vitality(eq: EpistemicQuantum, current_epoch: int) -> float:
    """Multiplicative vitality with floor and grace period."""
    # Component 1: Opinion strength (projected probability)
    opinion_factor = eq.opinion.projected_probability

    # Component 2: Access recency (exponential decay)
    epochs_since_access = current_epoch - eq.timestamps.last_accessed_epoch
    recency_factor = math.exp(-0.1 * epochs_since_access)

    # Component 3: Coherence support (normalised incoming support weight)
    support_edges = [e for e in eq.edges if e.edge_type == EdgeType.SUPPORT and e.direction == INCOMING]
    coherence_factor = min(1.0, sum(e.weight for e in support_edges) / 3.0)

    # Component 4: Claim-class longevity modifier
    longevity = get_claim_longevity_modifier(eq.claim_class)

    # Multiplicative composition
    raw_vitality = opinion_factor * recency_factor * coherence_factor * longevity

    return max(VITALITY_FLOOR, raw_vitality)


def evaluate_catabolism_candidate(eq: EpistemicQuantum, current_epoch: int) -> bool:
    """Determine if a quantum is a catabolism candidate.

    A quantum becomes a candidate only after its vitality has been
    at or near the floor for VITALITY_GRACE_PERIOD consecutive epochs.
    """
    vitality = compute_vitality(eq, current_epoch)

    if vitality <= VITALITY_FLOOR * 1.1:  # within 10% of floor
        if eq.timestamps.floor_entry_epoch is None:
            eq.timestamps.floor_entry_epoch = current_epoch
            return False
        elif (current_epoch - eq.timestamps.floor_entry_epoch) >= VITALITY_GRACE_PERIOD:
            return True
        else:
            return False
    else:
        eq.timestamps.floor_entry_epoch = None  # reset grace period
        return False
```

### 4.5  Edge Types

Quanta are connected by five canonical edge types in the coherence graph:

| Edge Type | Semantics | Weight Range | Reciprocal |
|---|---|---|---|
| **SUPPORT** | A provides evidence for B | [0.0, 1.0] | Yes (INV-E3) |
| **CONTRADICTION** | A and B are mutually inconsistent | [0.0, 1.0] | Yes (INV-E3) |
| **DERIVATION** | B was derived from A (directed, but reciprocal stored) | [0.0, 1.0] | Yes (INV-E3) |
| **ANALOGY** | A and B are structurally similar | [0.0, 1.0] | Yes (INV-E3) |
| **SUPERSESSION** | B supersedes A (directed, but reciprocal stored) | [0.0, 1.0] | Yes (INV-E3) |

#### 4.5.1  Contradiction Edge Caps

Per-agent contradiction weight is capped to prevent monopolistic blocking:

```python
MAX_CONTRADICTION_WEIGHT_PER_AGENT = 0.3

def create_contradiction_edge_with_cap(
    source_quantum: EpistemicQuantum,
    target_quantum: EpistemicQuantum,
    proposed_weight: float,
    creating_agent: AgentID,
    existing_contradictions: List[Edge]
) -> Edge:
    """Create contradiction edge with per-agent weight cap.

    Instead of rejecting edges that exceed the cap, they are created
    at reduced weight (minimum 0.05).
    """
    agent_existing = [e for e in existing_contradictions
                      if e.creating_agent == creating_agent]
    agent_total_weight = sum(e.weight for e in agent_existing)

    remaining_budget = MAX_CONTRADICTION_WEIGHT_PER_AGENT - agent_total_weight

    if remaining_budget <= 0:
        actual_weight = 0.05  # minimum weight, never rejected
    else:
        actual_weight = max(0.05, min(proposed_weight, remaining_budget))

    return Edge(
        source=source_quantum.id,
        target=target_quantum.id,
        edge_type=EdgeType.CONTRADICTION,
        weight=actual_weight,
        creating_agent=creating_agent
    )
```

### 4.6  Claim Decomposition

Compound claims are decomposed into atomic sub-claims before processing:

```python
DECOMPOSITION_SIBLING_WEIGHT = 0.3

def decompose_claim(content: StructuredClaim) -> List[StructuredClaim]:
    """Decompose a compound claim into atomic sub-claims.

    Each sub-claim inherits the parent's provenance and receives
    ANALOGY edges to siblings at DECOMPOSITION_SIBLING_WEIGHT.
    """
    sub_claims = _extract_sub_claims(content)

    if len(sub_claims) <= 1:
        return [content]  # already atomic

    atomic_claims = []
    for sc in sub_claims:
        if _is_assertive(sc):
            atomic_claims.append(sc)

    # Create sibling edges between decomposed claims
    for i, c1 in enumerate(atomic_claims):
        for c2 in atomic_claims[i+1:]:
            create_edge(c1, c2, EdgeType.ANALOGY, weight=DECOMPOSITION_SIBLING_WEIGHT)

    return atomic_claims


def _extract_sub_claims(content: StructuredClaim) -> List[StructuredClaim]:
    """Extract individual assertions from a compound claim.
    Implementation uses NLP clause boundary detection."""
    # ... implementation detail ...
    pass

def _is_assertive(claim: StructuredClaim) -> bool:
    """Check if a clause makes a testable assertion."""
    # ... implementation detail ...
    pass
```

### 4.6  Four-Tier Memory Model

The original Noosphere architecture (C3 Â§1.2) defined a four-tier memory model â€” working, short-term, long-term, and archival â€” but deferred its specification to the knowledge subsystem. C6 EMA implements this model through a combination of lifecycle states (Â§4.3), coherence graph edge tiers (Â§4.5, Â§7.3.1), and the Archive Layer (Â§5.4.3). This section formally defines the mapping and specifies the tier assignment rules.

#### 4.6.1  Tier Definitions

| Memory Tier | Definition | Storage Characteristics | C6 Constructs |
|-------------|-----------|------------------------|---------------|
| **Working** | Quanta actively participating in current-epoch reasoning, verification, or consolidation. The "foreground" of epistemic processing. | Highest priority for opinion updates, coherence checks, and retrieval. Full HOT-tier edge processing every epoch. | ACTIVE state + HOT coherence tier (accessed within last 1 TIDAL_EPOCH) |
| **Short-term** | Quanta recently active but not accessed in the current epoch. Available for rapid retrieval and reasoning reactivation. Background candidates for circulation. | Moderate priority. WARM-tier edge updates (every 5 epochs). Eligible for vitality-driven promotion back to Working or demotion to Long-term. | ACTIVE state + WARM coherence tier (accessed within last 5 TIDAL_EPOCHs) |
| **Long-term** | Quanta retained for structural coherence and historical context but not recently accessed. Includes dormant quanta. May be reactivated on retrieval or cross-reference. | Low priority. COLD-tier edge updates (every 10 epochs). Subject to vitality decay. Catabolism candidates after grace period at vitality floor. | ACTIVE state + COLD coherence tier (5+ epochs since access) OR DORMANT state |
| **Archival** | Dissolved quanta whose content has been removed but whose provenance, dissolution records, and edge tombstones are retained for historical tracing. Read-only, immutable. | No opinion updates, no edge processing, no vitality computation. Partitioned by CONSOLIDATION_CYCLE. Compacted after retention period. | DISSOLVED state â†’ Archive Layer (Â§5.4.3) |

**Special states that span tiers:**
- **INGESTED** quanta are transitional â€” they exist for at most one TIDAL_EPOCH before entering ACTIVE (Working tier). They are not assigned a memory tier.
- **CONSOLIDATED** quanta are transitional â€” K-class products of the dreaming pipeline, awaiting re-verification. They are logically in Working tier during verification.
- **QUARANTINED** quanta are held outside the tier system â€” they are suspended from reasoning, retrieval, and edge processing pending catabolism review or re-evaluation.

#### 4.6.2  Tier Assignment

Tier assignment is a derived property computed from lifecycle state and access recency. It is NOT stored as a field on the quantum â€” it is computed at query time or at epoch boundaries for operational purposes.

```python
def classify_memory_tier(
    eq: EpistemicQuantum,
    current_epoch: int
) -> str:
    """Assign a quantum to its memory tier.

    Returns: WORKING | SHORT_TERM | LONG_TERM | ARCHIVAL | TRANSITIONAL | SUSPENDED
    """
    if eq.metabolic_state == MetabolicState.DISSOLVED:
        return "ARCHIVAL"
    if eq.metabolic_state == MetabolicState.QUARANTINED:
        return "SUSPENDED"
    if eq.metabolic_state in (MetabolicState.INGESTED, MetabolicState.CONSOLIDATED):
        return "TRANSITIONAL"
    if eq.metabolic_state == MetabolicState.DORMANT:
        return "LONG_TERM"

    # ACTIVE state â€” tier depends on access recency
    epochs_since_access = current_epoch - eq.timestamps.last_accessed_epoch
    if epochs_since_access <= HOT_THRESHOLD:       # 1 epoch
        return "WORKING"
    elif epochs_since_access <= WARM_THRESHOLD:     # 5 epochs
        return "SHORT_TERM"
    else:
        return "LONG_TERM"
```

#### 4.6.3  Tier Transitions

Tier transitions are automatic and driven by access patterns and metabolic state changes:

```
   retrieval or                                vitality decay
   reasoning access                            (no access)
        â”‚                                           â”‚
        â–¼                                           â–¼
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”   no access    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   no access    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚ WORKING â”‚â”€â”€â”€â”€â”€â”€(1 epoch)â”€â”€â–ºâ”‚ SHORT_TERM â”‚â”€â”€â”€â”€â”€â”€(5 epochs)â”€â”€â–ºâ”‚ LONG_TERM â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                â””â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜
        â–²                           â–²                              â”‚
        â”‚     retrieval             â”‚     retrieval          vitality at
        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                        floor for
                                                            5+ epochs
                                                                 â”‚
                                                                 â–¼
                                                          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                                                          â”‚ QUARANTINED  â”‚
                                                          â”‚ (SUSPENDED)  â”‚
                                                          â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                                                                 â”‚ dissolve
                                                                 â–¼
                                                          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    archive at
                                                          â”‚DISSOLVED â”‚â”€â”€â”€(next CONSOL.)â”€â”€â–º  ARCHIVAL
                                                          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Promotion (toward Working):** Any retrieval or reasoning access immediately promotes a quantum toward Working tier by updating `last_accessed_epoch`. DORMANT quanta are first reactivated to ACTIVE state (Â§4.3), then placed in Working tier.

**Demotion (toward Archival):** Driven by elapsed time without access. No explicit action is needed â€” tier classification is a function of access recency. Demotion through the tier boundary is continuous and passive.

**Tier-catabolism interaction.** Catabolism candidacy (Â§4.4) is not triggered by tier membership â€” it is triggered by vitality falling to the floor for 5+ epochs. However, Long-term tier membership strongly correlates with low vitality because the `recency_factor` in vitality computation (Â§4.4) decays exponentially with `epochs_since_access`. A quantum that has been in Long-term tier for many epochs will naturally approach the vitality floor.

#### 4.6.4  Operational Implications

| Tier | Opinion Updates | Coherence Edge Updates | Retrieval Priority | SHREC Budget Impact |
|------|----------------|----------------------|-------------------|-------------------|
| Working | Every SETTLEMENT_TICK (60s) | Every TIDAL_EPOCH (1h) | Highest | Counts toward Ïƒ_C (Circulation Load) |
| Short-term | Every SETTLEMENT_TICK (60s) | Every 5 TIDAL_EPOCHs | High | Counts toward Ïƒ_C |
| Long-term | Every SETTLEMENT_TICK (60s) | Every 10 TIDAL_EPOCHs | Low | Contributes to Ïƒ_X (Catabolism Urgency) when near floor |
| Archival | None | None | Read-only provenance queries | No SHREC impact |

**SHREC interaction.** The four tiers provide SHREC with a natural basis for budget allocation:
- High Working/Short-term ratio â†’ system is actively reasoning â†’ Ïƒ_C increases â†’ circulation budget rises.
- High Long-term ratio â†’ knowledge is stagnating â†’ Ïƒ_X may increase â†’ catabolism budget rises.
- High Archival growth rate â†’ dissolution pipeline is busy â†’ monitor for consolidation-poisoning signals.

SHREC does not directly manage tier assignments â€” tiers are emergent from access patterns. SHREC influences tiers indirectly by allocating more budget to circulation (promoting access) or catabolism (accelerating dissolution).

#### 4.6.5  Cross-Reference to C3

C3 Â§1.2 references the "Knowledge Cortex four-tier memory model (see Noosphere Spec Sections 23-25)" as deferred to the knowledge subsystem. This section satisfies that deferral:

| C3 Reference | C6 Implementation |
|--------------|-------------------|
| "Four-tier memory model" | Â§4.6 (this section) â€” Working/Short-term/Long-term/Archival |
| "Working memory" | ACTIVE + HOT coherence tier |
| "Short-term memory" | ACTIVE + WARM coherence tier |
| "Long-term memory" | ACTIVE + COLD coherence tier, plus DORMANT state |
| "Archival memory" | DISSOLVED â†’ Archive Layer (Â§5.4.3) |
| Noosphere Spec Sections 23-25 | Replaced by C6 Â§Â§4.3, 4.4, 4.6, 5.4.3, 7.3.1 |

#### 4.6.6  Conformance Requirements

| ID | Requirement | Testable Criterion |
|----|------------|-------------------|
| CR-MTM-1 | Tier assignment is deterministic from state and access recency | `classify_memory_tier()` produces identical results for identical inputs |
| CR-MTM-2 | Tier assignment is consistent with coherence graph edge tiers | ACTIVE quanta classified as WORKING have only HOT-tier edges; SHORT_TERM have WARM or HOT; no contradictions with INV-E17 |
| CR-MTM-3 | DORMANT quanta are always classified as LONG_TERM | No DORMANT quantum is classified as WORKING or SHORT_TERM |
| CR-MTM-4 | DISSOLVED quanta are always classified as ARCHIVAL | No DISSOLVED quantum is classified as any other tier |
| CR-MTM-5 | Tier distribution is reported as a SHREC diagnostic | SHREC state includes per-tier quantum counts at each TIDAL_EPOCH |

---

## 5  Metabolic Processes

### 5.1  Ingestion

Ingestion is the gateway process: external assertions are received, classified, assigned initial opinions, decomposed if compound, and admitted to ACTIVE state.

#### 5.1.1  Ingestion Pipeline

```
External   â”€â”€â–º  Validate   â”€â”€â–º  Classify   â”€â”€â–º  Decompose   â”€â”€â–º  Form Initial   â”€â”€â–º  ACTIVE
Assertion       Structure       Claim Class      (if compound)    Opinion
```

1. **Structural validation.** The incoming assertion MUST conform to the StructuredClaim schema. Malformed inputs are rejected with a diagnostic code.
2. **Claim classification.** The assertion is classified into one of nine claim classes (D, E, S, H, N, P, R, C, K). K-class is reserved for consolidation outputs; external claims classified as K MUST be rejected.
3. **Compound decomposition.** If the claim contains multiple assertive sub-claims, it is decomposed via `decompose_claim()` (Section 4.6). Each atomic sub-claim proceeds independently.
4. **Initial opinion formation.** The initial opinion is computed by discounting the claim's self-assessment by the source's trustworthiness opinion:
   ```python
   initial_opinion = discount(source_trustworthiness, claim_self_assessment)
   ```
5. **PCVM submission.** The new quantum is submitted to the Proof Chain Verification Machine for verification. If PCVM is in degraded mode, the quantum is queued (Section 10.1).
6. **State transition.** On successful verification (or queuing), the quantum transitions INGESTED â†’ ACTIVE.

#### 5.1.2  Ingestion Rate Control

Ingestion rate is governed by SHREC allocation N_ingest:

```python
max_ingestions_per_tick = floor(N_ingest * TOTAL_CAPACITY / COST_PER_INGESTION)
```

When the queue exceeds capacity, claims are prioritised by:
1. Source trustworthiness (descending).
2. Claim class difficulty weight (ascending â€” easier claims first for throughput).
3. Arrival order (FIFO tiebreaker).

### 5.2  Circulation

Circulation maintains the active knowledge base: updating opinions based on new evidence, adjusting edge weights, and managing access patterns.

#### 5.2.1  Opinion Update Cycle

Every SETTLEMENT_TICK (60 s), active quanta undergo opinion updates:

1. **Evidence aggregation.** New evidence from peer subsystems and external sources is collected.
2. **Fusion.** Cumulative fusion for independent evidence; averaging fusion for dependent evidence.
3. **Edge propagation.** Opinion changes propagate along SUPPORT and DERIVATION edges with distance decay.
4. **Consistency check.** CONTRADICTION edges trigger belief revision when both endpoints have high belief (b > 0.7).

#### 5.2.2  Access Tracking

Every retrieval or reasoning access updates the quantum's `last_accessed_epoch`, which feeds into vitality computation and edge tier classification (HOT/WARM/COLD).

### 5.3  Consolidation (Dreaming)

Consolidation is the most complex metabolic process: it synthesises new K-class knowledge from clusters of active quanta during CONSOLIDATION_CYCLE intervals (36 000 s = 10 TIDAL_EPOCHs). The pipeline includes defense-in-depth mechanisms and the CRP+ protocol to prevent consolidation poisoning.

#### 5.3.1  Consolidation Pipeline Overview

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    CONSOLIDATION PIPELINE                                â”‚
â”‚                                                                          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚ Cluster  â”‚â”€â”€â–ºâ”‚ 3-Pass   â”‚â”€â”€â–ºâ”‚  Source   â”‚â”€â”€â–ºâ”‚      CRP+            â”‚  â”‚
â”‚  â”‚Selection â”‚   â”‚   LLM    â”‚   â”‚Independ- â”‚   â”‚  7-Mechanism          â”‚  â”‚
â”‚  â”‚          â”‚   â”‚Synthesis â”‚   â”‚  ence     â”‚   â”‚  Defense              â”‚  â”‚
â”‚  â”‚          â”‚   â”‚(2-temp)  â”‚   â”‚Verificat.â”‚   â”‚                       â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚ M1: APRT              â”‚  â”‚
â”‚                                                â”‚ M2: CODS              â”‚  â”‚
â”‚                                                â”‚ M3: Source Purpose    â”‚  â”‚
â”‚                                                â”‚ M4: VRF Selection     â”‚  â”‚
â”‚                                                â”‚ M5: Credibility Ladderâ”‚  â”‚
â”‚                                                â”‚ M6: Depth Limits      â”‚  â”‚
â”‚                                                â”‚ M7: Immune Memory     â”‚  â”‚
â”‚                                                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚                                                            â”‚              â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚              â”‚
â”‚  â”‚  Adversarial     â”‚â—„â”€â”€â”‚ Lineage  â”‚â—„â”€â”€â”‚   Novelty    â”‚â—„â”€â”€â”˜              â”‚
â”‚  â”‚  Probing         â”‚   â”‚ Tracking â”‚   â”‚   Pathway    â”‚                  â”‚
â”‚  â”‚  (C10)           â”‚   â”‚  (C10)   â”‚   â”‚  (if N3)     â”‚                  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                  â”‚
â”‚           â”‚                                                               â”‚
â”‚           â–¼                                                               â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                                                    â”‚
â”‚  â”‚  PCVM Gate       â”‚â”€â”€â–º ACTIVE (K-class quantum)                        â”‚
â”‚  â”‚  (or queue if    â”‚                                                    â”‚
â”‚  â”‚   degraded)      â”‚                                                    â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                                                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

#### 5.3.2  Three-Pass LLM Synthesis with Two-Temperature Strategy

Consolidation uses a three-pass synthesis with two temperature settings:

```python
EXPLORATION_TEMPERATURE = 0.7   # Phase A: creative exploration
SYNTHESIS_TEMPERATURE = 0.3     # Phase B: precise filtering

def three_pass_synthesis(cluster: List[EpistemicQuantum]) -> ConsolidationCandidate:
    """Three-pass LLM synthesis with two-temperature strategy.

    Pass 1 (Exploration, T=0.7): Generate diverse candidate syntheses.
    Pass 2 (Filtering, T=0.3): Select and refine the most coherent candidates.
    Pass 3 (Validation, T=0.3): Verify internal consistency and provenance.
    """

    # Pass 1: Exploration â€” generate candidate syntheses
    candidates = []
    for _ in range(NUM_EXPLORATION_CANDIDATES):
        candidate = llm_synthesise(
            cluster,
            temperature=EXPLORATION_TEMPERATURE,
            prompt_type="creative_synthesis"
        )
        candidates.append(candidate)

    # Pass 2: Filtering â€” select best candidates at low temperature
    filtered = llm_filter(
        candidates,
        temperature=SYNTHESIS_TEMPERATURE,
        criteria=["coherence", "novelty", "evidence_coverage"]
    )

    # Pass 3: Validation â€” verify consistency
    for candidate in filtered:
        validation = llm_validate(
            candidate,
            source_cluster=cluster,
            temperature=SYNTHESIS_TEMPERATURE,
            checks=["internal_consistency", "provenance_traceable", "no_hallucination"]
        )
        if validation.passed:
            return ConsolidationCandidate(
                content=candidate.content,
                source_cluster=cluster,
                opinion=compute_initial_k_opinion(candidate, cluster),
                provenance=build_consolidation_provenance(candidate, cluster)
            )

    return None  # no candidate passed validation
```

#### 5.3.3  Defense-in-Depth Layer (C10 Hardening)

Before CRP+ mechanisms, consolidation candidates pass through three defense layers:

##### 5.3.3.1  Source Independence Verification

```python
ROOT_COVERAGE_THRESHOLD = 0.50
TEMPORAL_CLUSTER_MIN_SPAN = 10  # TIDAL_EPOCHs
CLUSTER_DOMINANCE_THRESHOLD = 0.30

def verify_source_independence(candidate: ConsolidationCandidate) -> IndependenceResult:
    """Verify that consolidation sources are genuinely independent.

    Three checks:
    I1 â€” Provenance chain independence: source quanta trace to diverse roots.
    I2 â€” Temporal clustering detection: sources not suspiciously co-temporal.
    I3 â€” Sentinel Graph cluster diversity: sources span multiple Sentinel clusters.
    """
    sources = candidate.source_cluster
    roots = set()

    # I1: Provenance chain independence
    for source in sources:
        chain_roots = trace_provenance_roots(source)
        roots.update(chain_roots)

    root_coverage = len(roots) / max(1, len(sources))
    i1_pass = root_coverage >= ROOT_COVERAGE_THRESHOLD

    # I2: Temporal clustering detection
    creation_times = [s.timestamps.created for s in sources]
    time_span = max(creation_times) - min(creation_times)
    time_span_epochs = time_span / TIDAL_EPOCH_SECONDS
    i2_pass = time_span_epochs >= TEMPORAL_CLUSTER_MIN_SPAN

    # I3: Sentinel Graph cluster diversity
    cluster_ids = set()
    for source in sources:
        if source.sentinel_cluster_id is not None:
            cluster_ids.add(source.sentinel_cluster_id)

    if len(cluster_ids) > 0:
        most_common_count = max(Counter(
            s.sentinel_cluster_id for s in sources
            if s.sentinel_cluster_id is not None
        ).values())
        dominance = most_common_count / len(sources)
        i3_pass = dominance < CLUSTER_DOMINANCE_THRESHOLD
    else:
        i3_pass = True  # no Sentinel data available, pass by default

    return IndependenceResult(
        passed=i1_pass and i2_pass and i3_pass,
        root_coverage=root_coverage,
        temporal_span_epochs=time_span_epochs,
        cluster_dominance=dominance if cluster_ids else 0.0,
        checks={"I1": i1_pass, "I2": i2_pass, "I3": i3_pass}
    )


def trace_provenance_roots(quantum: EpistemicQuantum) -> Set[SourceID]:
    """Trace provenance chain to root external sources."""
    roots = set()
    visited = set()
    stack = [quantum.provenance]

    while stack:
        prov = stack.pop()
        if prov.id in visited:
            continue
        visited.add(prov.id)

        if prov.is_external_source:
            roots.add(prov.source_id)
        else:
            stack.extend(prov.parents)

    return roots
```

> **CR-H10** (MUST): Consolidation candidates MUST pass source independence verification. Failure on any of I1, I2, or I3 triggers quarantine of the candidate for manual review.

##### 5.3.3.2  Adversarial Consolidation Probing

```python
COMPETITIVE_THRESHOLD = 0.40
LOW_CONFIDENCE_UNCERTAINTY_FLOOR = 0.50

def probe_consolidation_adversarially(
    candidate: ConsolidationCandidate,
    knowledge_base: KnowledgeBase
) -> ProbingResult:
    """Generate and test counter-hypotheses against consolidation candidate.

    If a counter-hypothesis scores competitively (within COMPETITIVE_THRESHOLD
    of the candidate), the candidate's uncertainty is elevated.
    """
    # Generate counter-hypotheses
    counter_hypotheses = generate_counter_hypotheses(candidate, knowledge_base)

    competitive_counters = []
    for counter in counter_hypotheses:
        counter_score = evaluate_hypothesis_score(counter, knowledge_base)
        candidate_score = evaluate_hypothesis_score(candidate, knowledge_base)

        if counter_score >= candidate_score * (1 - COMPETITIVE_THRESHOLD):
            competitive_counters.append(counter)

    if competitive_counters:
        # Elevate uncertainty
        adjusted_opinion = apply_uncertainty_elevation(
            candidate.opinion,
            num_competitive=len(competitive_counters),
            floor=LOW_CONFIDENCE_UNCERTAINTY_FLOOR
        )
        candidate.opinion = adjusted_opinion

    return ProbingResult(
        competitive_counter_count=len(competitive_counters),
        opinion_adjusted=len(competitive_counters) > 0,
        adjusted_opinion=candidate.opinion
    )


def apply_consolidation_probe(candidate: ConsolidationCandidate) -> ConsolidationCandidate:
    """Apply adversarial probe and adjust candidate accordingly."""
    result = probe_consolidation_adversarially(candidate, get_knowledge_base())
    if result.competitive_counter_count > 0:
        # Ensure minimum uncertainty
        if candidate.opinion.u < LOW_CONFIDENCE_UNCERTAINTY_FLOOR:
            remaining = 1.0 - LOW_CONFIDENCE_UNCERTAINTY_FLOOR
            ratio = remaining / max(1e-9, candidate.opinion.b + candidate.opinion.d)
            candidate.opinion = Opinion(
                b=candidate.opinion.b * ratio,
                d=candidate.opinion.d * ratio,
                u=LOW_CONFIDENCE_UNCERTAINTY_FLOOR,
                a=candidate.opinion.a
            )
    return candidate
```

> **CR-H11** (MUST): Every consolidation candidate MUST undergo adversarial probing. Candidates with competitive counter-hypotheses MUST have uncertainty elevated to at least LOW_CONFIDENCE_UNCERTAINTY_FLOOR.

##### 5.3.3.3  Consolidation Lineage Tracking

```python
MAX_CASCADE_DEPTH = 5
CASCADE_REDUCTION_FACTOR = 0.15
MAX_CASCADE_REDUCTION = 0.10

@dataclass
class ConsolidationLineage:
    """Track consolidation derivation chains for credibility cascading."""
    quantum_id: UUID
    parent_consolidation_ids: List[UUID]
    generation: int  # 0 = direct from primary sources, 1 = from K-class, etc.
    consolidation_timestamp: float

def cascade_credibility_on_consolidation_failure(
    failed_quantum: EpistemicQuantum,
    lineage_db: LineageDatabase
) -> List[CredibilityAdjustment]:
    """When a consolidated quantum fails re-evaluation, cascade
    credibility reductions to downstream dependents.

    Uses sqrt-diluted cascading: reduction at depth d is
    min(CASCADE_REDUCTION_FACTOR / sqrt(d), MAX_CASCADE_REDUCTION).
    """
    adjustments = []
    queue = [(failed_quantum.id, 1)]  # (quantum_id, depth)
    visited = set()

    while queue:
        current_id, depth = queue.pop(0)
        if current_id in visited or depth > MAX_CASCADE_DEPTH:
            continue
        visited.add(current_id)

        # Find dependents
        dependents = lineage_db.get_dependents(current_id)
        for dep_id in dependents:
            reduction = min(
                CASCADE_REDUCTION_FACTOR / math.sqrt(depth),
                MAX_CASCADE_REDUCTION
            )
            adjustments.append(CredibilityAdjustment(
                quantum_id=dep_id,
                reduction=reduction,
                reason=f"cascade from {failed_quantum.id} at depth {depth}"
            ))
            queue.append((dep_id, depth + 1))

    return adjustments
```

> **CR-H12** (MUST): Consolidation lineage MUST be tracked for all K-class quanta. When a consolidated quantum fails re-evaluation, credibility reductions MUST cascade to dependents with sqrt-diluted attenuation up to MAX_CASCADE_DEPTH.

#### 5.3.4  CRP+ â€” Consolidation Robustness Protocol

The CRP+ protocol provides seven mechanisms across three axes (verification, selection, containment) that every consolidation candidate MUST pass (INV-CRP1).

##### 5.3.4.1  M1 â€” Aggregate Perturbation Robustness Testing (APRT)

APRT tests whether a synthesis conclusion remains stable when individual source quanta are perturbed or removed:

```python
STABILITY_THRESHOLD = 0.70

def aprt_test(candidate: ConsolidationCandidate, enhanced: bool = False) -> APRTResult:
    """Aggregate Perturbation Robustness Testing.

    Standard mode: stratified subset testing.
    Enhanced mode (for novelty pathway): full leave-one-out.

    Cases:
      A â€” High-influence source removal: remove top-3 by opinion strength.
      B â€” Redundant cluster pruning: remove sources sharing >0.8 similarity.
      C â€” Random subset (30%): stochastic stability check.
    """
    source_cluster = candidate.source_cluster
    original_conclusion = candidate.content

    if enhanced:
        # Full leave-one-out for novelty pathway
        perturbation_sets = [[s for j, s in enumerate(source_cluster) if j != i]
                             for i in range(len(source_cluster))]
    else:
        # Standard three-case stratified testing
        perturbation_sets = []

        # Case A: Remove top-3 by opinion strength
        sorted_by_strength = sorted(source_cluster,
                                     key=lambda s: s.opinion.projected_probability,
                                     reverse=True)
        case_a = [s for s in source_cluster if s not in sorted_by_strength[:3]]
        perturbation_sets.append(case_a)

        # Case B: Remove redundant cluster members
        case_b = remove_redundant_sources(source_cluster, similarity_threshold=0.8)
        perturbation_sets.append(case_b)

        # Case C: Random 70% subset
        k = max(1, int(len(source_cluster) * 0.7))
        case_c = random.sample(source_cluster, k)
        perturbation_sets.append(case_c)

    # Test each perturbation
    stability_scores = []
    for perturbed_set in perturbation_sets:
        if len(perturbed_set) < 2:
            continue
        re_synthesis = llm_synthesise(perturbed_set, temperature=SYNTHESIS_TEMPERATURE)
        similarity = compute_semantic_similarity(original_conclusion, re_synthesis.content)
        stability_scores.append(similarity)

    avg_stability = sum(stability_scores) / max(1, len(stability_scores))

    return APRTResult(
        stable=avg_stability >= STABILITY_THRESHOLD,
        avg_stability=avg_stability,
        per_case_scores=stability_scores,
        enhanced=enhanced
    )
```

##### 5.3.4.2  M2 â€” Calibrated Opponent-aware Dissent Search (CODS)

CODS classifies novelty and searches for calibrated dissenting evidence:

```python
EXPECTED_DISSENT_LEVEL = 1.5

def cods_evaluate(candidate: ConsolidationCandidate,
                  knowledge_base: KnowledgeBase) -> CODSResult:
    """Calibrated Opponent-aware Dissent Search.

    1. Classify novelty level: N1 (incremental), N2 (moderate), N3 (paradigmatic).
    2. Search for dissenting evidence with novelty-calibrated weights.
    3. Compute dissent score.
    """
    # Step 1: Novelty classification
    novelty = classify_novelty(candidate, knowledge_base)
    # N1: extends existing cluster, N2: bridges clusters, N3: contradicts established

    # Step 2: Search for dissent
    dissent_weight_map = {
        NoveltyLevel.N1: 1.0,   # full weight â€” incremental claims need normal dissent
        NoveltyLevel.N2: 0.5,   # moderate discount â€” bridging claims expected to face some
        NoveltyLevel.N3: 0.1    # heavy discount â€” paradigmatic claims face most dissent
    }
    dissent_weight = dissent_weight_map[novelty]

    dissenting_quanta = search_dissenting_evidence(candidate, knowledge_base)
    weighted_dissent = sum(
        d.opinion.d * dissent_weight for d in dissenting_quanta
    )

    dissent_score = weighted_dissent / EXPECTED_DISSENT_LEVEL

    return CODSResult(
        novelty_level=novelty,
        dissent_score=min(1.0, dissent_score),
        dissenting_count=len(dissenting_quanta),
        weighted_dissent=weighted_dissent
    )
```

##### 5.3.4.3  M3 â€” Source Purpose Scoring

A conditional tie-breaker that evaluates source alignment with consolidation purpose:

```python
M3_MAX_CONTRIBUTION = 0.15
M3_HIGH_PURPOSE_THRESHOLD = 0.80

def source_purpose_score(candidate: ConsolidationCandidate) -> float:
    """Source Purpose Scoring â€” conditional tie-breaker.

    Evaluates whether sources were 'purpose-aligned' for the consolidation.
    Only applied as an additive bonus when other mechanisms are inconclusive.
    Capped at M3_MAX_CONTRIBUTION.
    """
    purpose_scores = []
    for source in candidate.source_cluster:
        # Evaluate source's alignment with the consolidated claim's domain
        alignment = compute_domain_alignment(source, candidate.content)
        purpose_scores.append(alignment)

    avg_purpose = sum(purpose_scores) / max(1, len(purpose_scores))

    if avg_purpose >= M3_HIGH_PURPOSE_THRESHOLD:
        return M3_MAX_CONTRIBUTION
    else:
        return avg_purpose * M3_MAX_CONTRIBUTION
```

##### 5.3.4.4  M4 â€” VRF Consolidation Selection

Verifiable Random Function-based selection prevents adversarial timing of consolidation:

```python
VRF_SELECTION_RATE = 0.10          # 10% selected per cycle
VRF_ANTI_STARVATION_BOOST = 20     # epochs before boost
VRF_FORCED_SELECTION_EPOCH = 40    # epochs before forced selection

def vrf_select_for_consolidation(
    candidates: List[EpistemicQuantum],
    vrf_secret_key: bytes,
    current_epoch: int
) -> List[EpistemicQuantum]:
    """ECVRF-based selection for consolidation candidates.

    Uses VRF to select ~10% of candidates per cycle, ensuring
    unpredictable selection (INV-CRP2).

    Anti-starvation: quanta not selected for VRF_ANTI_STARVATION_BOOST
    epochs get boosted probability. Forced selection after
    VRF_FORCED_SELECTION_EPOCH epochs.
    """
    selected = []

    for candidate in candidates:
        # Compute VRF output
        vrf_input = f"{candidate.id}:{current_epoch}".encode()
        vrf_output, vrf_proof = ecvrf_prove(vrf_secret_key, vrf_input)
        selection_value = int.from_bytes(vrf_output[:8], 'big') / (2**64)

        # Compute selection threshold with anti-starvation
        epochs_since_last = current_epoch - candidate.last_consolidation_epoch
        if epochs_since_last >= VRF_FORCED_SELECTION_EPOCH:
            threshold = 1.0  # guaranteed selection
        elif epochs_since_last >= VRF_ANTI_STARVATION_BOOST:
            boost = (epochs_since_last - VRF_ANTI_STARVATION_BOOST) / \
                    (VRF_FORCED_SELECTION_EPOCH - VRF_ANTI_STARVATION_BOOST)
            threshold = VRF_SELECTION_RATE + boost * (1.0 - VRF_SELECTION_RATE)
        else:
            threshold = VRF_SELECTION_RATE

        if selection_value < threshold:
            selected.append(candidate)
            candidate.vrf_proof = vrf_proof  # attach proof for auditability

    return selected
```

##### 5.3.4.5  M5 â€” Graduated Credibility Ladder

Every quantum occupies a rung on a five-level credibility ladder:

| Rung | Name | Uncertainty Threshold | Trust Modifier |
|---|---|---|---|
| 0 | SPECULATIVE | u â‰¥ 0.80 | 0.00 |
| 1 | PROVISIONAL | u â‰¥ 0.50 | 0.25 |
| 2 | CORROBORATED | u â‰¥ 0.30 | 0.50 |
| 3 | ESTABLISHED | u â‰¥ 0.15 | 0.75 |
| 4 | CANONICAL | u â‰¥ 0.05 | 1.00 |

```python
PROMOTION_OBSERVATION_WINDOW = 10  # TIDAL_EPOCHs

@dataclass
class CredibilityState:
    rung: int  # 0-4
    rung_name: str
    epochs_at_rung: int
    trust_modifier: float

def evaluate_rung(quantum: EpistemicQuantum) -> int:
    """Determine appropriate credibility rung based on current uncertainty."""
    u = quantum.opinion.u
    if u >= 0.80:
        return 0  # SPECULATIVE
    elif u >= 0.50:
        return 1  # PROVISIONAL
    elif u >= 0.30:
        return 2  # CORROBORATED
    elif u >= 0.15:
        return 3  # ESTABLISHED
    else:
        return 4  # CANONICAL

def update_credibility_rung(quantum: EpistemicQuantum, current_epoch: int):
    """Update credibility rung with promotion/demotion rules.

    Promotions: require PROMOTION_OBSERVATION_WINDOW sustained epochs (INV-CRP3).
    Demotions: immediate upon threshold violation (INV-CRP3).
    """
    target_rung = evaluate_rung(quantum)

    if target_rung > quantum.credibility.rung:
        # Promotion â€” requires sustained evidence
        if quantum.credibility.epochs_at_rung >= PROMOTION_OBSERVATION_WINDOW:
            quantum.credibility.rung = target_rung
            quantum.credibility.epochs_at_rung = 0
        # else: stay, keep accumulating
    elif target_rung < quantum.credibility.rung:
        # Demotion â€” immediate
        quantum.credibility.rung = target_rung
        quantum.credibility.epochs_at_rung = 0
    else:
        quantum.credibility.epochs_at_rung += 1

    quantum.credibility.rung_name = RUNG_NAMES[quantum.credibility.rung]
    quantum.credibility.trust_modifier = TRUST_MODIFIERS[quantum.credibility.rung]
```

Domain-adaptive thresholds MAY adjust rung boundaries for specific claim classes (e.g., P-class predictive claims may use tighter thresholds).

**K-class credibility rung lifecycle (C9 v2.0):** K-class quanta produced by the consolidation pipeline follow a mandatory five-rung credibility lifecycle:

1. **SPECULATIVE (rung 0):** Initial assignment for K-class quanta that emerge from consolidation with high residual uncertainty (u â‰¥ 0.80). Excluded from further consolidation (INV-CRP4). Cannot serve as sources for downstream synthesis.
2. **PROVISIONAL (rung 1):** K-class quanta that have accumulated partial corroboration but remain below the participation threshold. Kâ†’K second-generation consolidation outputs are capped at this rung (Section 5.3.4.6). Excluded from further consolidation (INV-CRP4).
3. **CORROBORATED (rung 2):** The first rung at which a K-class quantum may participate as a consolidation source, but only at 0.50 weight (M6 depth limits). Requires sustained evidence accumulation over â‰¥ PROMOTION_OBSERVATION_WINDOW epochs for promotion from PROVISIONAL.
4. **ESTABLISHED (rung 3):** K-class quanta with strong evidentiary support (u < 0.15). Participates in consolidation at full weight. Eligible to serve as authoritative sources in cross-subsystem projections (C3, C4, C5).
5. **CANONICAL (rung 4):** The highest credibility rung, reserved for K-class quanta with near-minimal uncertainty (u < 0.05). Participates at full weight. Represents the system's most trusted consolidated knowledge.

Promotion through the ladder requires sustained evidence at each rung for â‰¥ PROMOTION_OBSERVATION_WINDOW (10 TIDAL_EPOCHs). Demotion is immediate upon threshold violation (INV-CRP3). This lifecycle ensures that consolidated knowledge earns trust incrementally and that the dreaming pipeline cannot fast-track low-quality synthesis into high-credibility positions.

##### 5.3.4.6  M6 â€” Consolidation Depth Limits

Depth limits prevent low-credibility quanta from participating in consolidation:

```python
def check_consolidation_eligibility(quantum: EpistemicQuantum) -> EligibilityResult:
    """Check whether a quantum may participate in consolidation (INV-CRP4).

    SPECULATIVE (rung 0): excluded entirely.
    PROVISIONAL (rung 1): excluded entirely.
    CORROBORATED (rung 2): participates at 0.50 weight.
    ESTABLISHED (rung 3): participates at full weight.
    CANONICAL (rung 4): participates at full weight.
    """
    rung = quantum.credibility.rung

    if rung <= 1:
        return EligibilityResult(eligible=False, weight=0.0,
                                  reason="Below CORROBORATED threshold")
    elif rung == 2:
        return EligibilityResult(eligible=True, weight=0.50,
                                  reason="CORROBORATED â€” half weight")
    else:
        return EligibilityResult(eligible=True, weight=1.0,
                                  reason=f"Rung {rung} â€” full weight")


def filter_consolidation_sources(
    cluster: List[EpistemicQuantum]
) -> List[Tuple[EpistemicQuantum, float]]:
    """Filter and weight sources for consolidation based on depth limits."""
    eligible = []
    for eq in cluster:
        result = check_consolidation_eligibility(eq)
        if result.eligible:
            eligible.append((eq, result.weight))
    return eligible
```

**Kâ†’K consolidation sandboxing:** When K-class quanta are used as sources for further consolidation (second-generation), the synthesis is sandboxed with additional APRT testing and the resulting quantum's initial credibility rung is capped at PROVISIONAL.

##### 5.3.4.7  M7 â€” Immune Memory

Immune memory maintains signatures of previously quarantined or rejected claims to detect recurrence:

```python
L2_MATCH_THRESHOLD = 0.60
L3_MATCH_THRESHOLD = 0.50

@dataclass
class ImmuneSignature:
    level: int  # 1, 2, or 3
    signature: bytes
    created_epoch: int
    source_quantum_id: UUID
    rejection_reason: str

class ImmuneMemoryStore:
    """Three-level immune memory (INV-CRP5).

    L1: Content hash â€” exact duplicate detection.
    L2: Structural pattern â€” similar claim structure (cosine similarity).
    L3: Behavioral pattern â€” similar submission patterns from same source cluster.
    """

    def __init__(self):
        self.l1_signatures: Dict[bytes, ImmuneSignature] = {}
        self.l2_signatures: List[ImmuneSignature] = []
        self.l3_signatures: List[ImmuneSignature] = []

    def check_immune_match(self, candidate: ConsolidationCandidate) -> Optional[ImmuneSignature]:
        """Check candidate against all three levels of immune memory."""
        # L1: Exact content hash
        content_hash = compute_content_hash(candidate.content)
        if content_hash in self.l1_signatures:
            return self.l1_signatures[content_hash]

        # L2: Structural similarity
        candidate_structure = extract_structural_pattern(candidate.content)
        for sig in self.l2_signatures:
            similarity = cosine_similarity(candidate_structure, sig.signature)
            if similarity >= L2_MATCH_THRESHOLD:
                return sig

        # L3: Behavioral pattern
        candidate_behavior = extract_behavioral_pattern(candidate)
        for sig in self.l3_signatures:
            similarity = behavioral_similarity(candidate_behavior, sig.signature)
            if similarity >= L3_MATCH_THRESHOLD:
                return sig

        return None

    def record_rejection(self, candidate: ConsolidationCandidate, reason: str,
                         current_epoch: int):
        """Record rejection at all three signature levels."""
        # L1
        content_hash = compute_content_hash(candidate.content)
        self.l1_signatures[content_hash] = ImmuneSignature(
            level=1, signature=content_hash,
            created_epoch=current_epoch,
            source_quantum_id=candidate.source_cluster[0].id,
            rejection_reason=reason
        )

        # L2
        structural = extract_structural_pattern(candidate.content)
        self.l2_signatures.append(ImmuneSignature(
            level=2, signature=structural,
            created_epoch=current_epoch,
            source_quantum_id=candidate.source_cluster[0].id,
            rejection_reason=reason
        ))

        # L3
        behavioral = extract_behavioral_pattern(candidate)
        self.l3_signatures.append(ImmuneSignature(
            level=3, signature=behavioral,
            created_epoch=current_epoch,
            source_quantum_id=candidate.source_cluster[0].id,
            rejection_reason=reason
        ))

    def garbage_collect(self, current_epoch: int, max_age_epochs: int = 1000):
        """GC runs every epoch (INV-CRP5). Remove expired signatures."""
        cutoff = current_epoch - max_age_epochs
        self.l1_signatures = {
            k: v for k, v in self.l1_signatures.items()
            if v.created_epoch >= cutoff
        }
        self.l2_signatures = [s for s in self.l2_signatures if s.created_epoch >= cutoff]
        self.l3_signatures = [s for s in self.l3_signatures if s.created_epoch >= cutoff]
```

##### 5.3.4.8  CRP+ Combined Scoring

All mechanisms feed into a combined score:

```python
WEIGHT_APRT = 0.35
WEIGHT_CODS = 0.25
WEIGHT_PROBE = 0.25
WEIGHT_IMMUNE = 0.15

ACCEPT_THRESHOLD = 0.35
QUARANTINE_THRESHOLD = 0.60

def compute_crp_plus_score(
    aprt_result: APRTResult,
    cods_result: CODSResult,
    probe_result: ProbingResult,
    immune_match: Optional[ImmuneSignature],
    purpose_score: float
) -> CRPPlusScore:
    """Compute combined CRP+ score.

    Score = WEIGHT_APRT * (1 - aprt_stability)
          + WEIGHT_CODS * cods_dissent_score
          + WEIGHT_PROBE * probe_score
          + WEIGHT_IMMUNE * immune_score
          + purpose_addition

    Decision:
      score < ACCEPT_THRESHOLD  â†’ ACCEPT
      ACCEPT_THRESHOLD â‰¤ score â‰¤ QUARANTINE_THRESHOLD â†’ QUARANTINE
      score > QUARANTINE_THRESHOLD â†’ REJECT
    """
    aprt_component = WEIGHT_APRT * (1.0 - aprt_result.avg_stability)
    cods_component = WEIGHT_CODS * cods_result.dissent_score
    probe_component = WEIGHT_PROBE * (probe_result.competitive_counter_count /
                                       max(1, probe_result.competitive_counter_count + 1))
    immune_component = WEIGHT_IMMUNE * (1.0 if immune_match is not None else 0.0)
    purpose_addition = purpose_score  # already capped at M3_MAX_CONTRIBUTION

    total = aprt_component + cods_component + probe_component + immune_component + purpose_addition

    if total < ACCEPT_THRESHOLD:
        decision = Decision.ACCEPT
    elif total <= QUARANTINE_THRESHOLD:
        decision = Decision.QUARANTINE
    else:
        decision = Decision.REJECT

    return CRPPlusScore(
        total=total,
        components={
            "APRT": aprt_component,
            "CODS": cods_component,
            "PROBE": probe_component,
            "IMMUNE": immune_component,
            "PURPOSE": purpose_addition
        },
        decision=decision
    )
```

#### 5.3.5  Novelty Pathway

N3 (paradigmatic) claims that pass initial CRP+ screening enter an enhanced evaluation pathway:

```python
NOVELTY_QUARANTINE_MIN_CYCLES = 5
NOVELTY_QUARANTINE_MAX_CYCLES = 10

def novelty_pathway_check(candidate: ConsolidationCandidate) -> bool:
    """Determine if candidate qualifies for novelty pathway entry.

    Entry criteria (ALL must be met):
    1. Classified as N3 (paradigmatic) by CODS.
    2. No suspicious source clusters (I3 check passed).
    3. Sources span 3+ Sentinel Graph clusters.
    4. No immune memory match at any level.
    """
    cods = cods_evaluate(candidate, get_knowledge_base())
    if cods.novelty_level != NoveltyLevel.N3:
        return False

    independence = verify_source_independence(candidate)
    if not independence.checks["I3"]:
        return False

    sentinel_clusters = count_sentinel_clusters(candidate.source_cluster)
    if sentinel_clusters < 3:
        return False

    immune_match = immune_memory.check_immune_match(candidate)
    if immune_match is not None:
        return False

    return True


def execute_novelty_pathway(candidate: ConsolidationCandidate,
                            current_epoch: int) -> NoveltyPathwayResult:
    """Execute the four enhanced checks of the novelty pathway (INV-CRP6).

    1. Enhanced APRT (full leave-one-out).
    2. Constructive adversarial probing.
    3. Temporal quarantine (5-10 cycles).
    4. Provenance deep audit (KS test, framing consistency, M7 cross-ref).
    """
    results = {}

    # Check 1: Enhanced APRT â€” full leave-one-out
    aprt = aprt_test(candidate, enhanced=True)
    results["enhanced_aprt"] = aprt
    if not aprt.stable:
        return NoveltyPathwayResult(passed=False, reason="Enhanced APRT failed", results=results)

    # Check 2: Constructive adversarial probing
    adversarial = constructive_adversarial_probe(candidate)
    results["adversarial_probe"] = adversarial
    if adversarial.fatal_counter_found:
        return NoveltyPathwayResult(passed=False, reason="Fatal counter-hypothesis", results=results)

    # Check 3: Temporal quarantine
    quarantine_cycles = compute_quarantine_duration(candidate, current_epoch)
    # Clamp to [NOVELTY_QUARANTINE_MIN_CYCLES, NOVELTY_QUARANTINE_MAX_CYCLES]
    quarantine_cycles = max(NOVELTY_QUARANTINE_MIN_CYCLES,
                            min(NOVELTY_QUARANTINE_MAX_CYCLES, quarantine_cycles))
    candidate.quarantine_entry_epoch = current_epoch
    candidate.quarantine_duration = quarantine_cycles
    results["quarantine"] = {"cycles": quarantine_cycles, "entry_epoch": current_epoch}

    # Check 4: Provenance deep audit
    audit = provenance_deep_audit(candidate)
    results["provenance_audit"] = audit
    if not audit.passed:
        return NoveltyPathwayResult(passed=False, reason=f"Provenance audit failed: {audit.reason}",
                                     results=results)

    return NoveltyPathwayResult(passed=True, reason="All novelty checks passed", results=results)


def provenance_deep_audit(candidate: ConsolidationCandidate) -> AuditResult:
    """Deep provenance audit for novelty pathway.

    1. KS test for temporal distribution anomalies.
    2. Framing consistency check across sources.
    3. M7 immune memory cross-reference.
    """
    # KS test: check if source creation times follow expected distribution
    creation_times = [s.timestamps.created for s in candidate.source_cluster]
    ks_stat, ks_p = ks_test_uniform(creation_times)
    if ks_p < 0.05:
        return AuditResult(passed=False, reason="Temporal distribution anomaly (KS p < 0.05)")

    # Framing consistency: check if sources use suspiciously similar framing
    framing_scores = pairwise_framing_similarity(candidate.source_cluster)
    avg_framing = sum(framing_scores) / max(1, len(framing_scores))
    if avg_framing > 0.90:
        return AuditResult(passed=False, reason="Suspicious framing consistency (>0.90)")

    # M7 cross-reference: check individual sources against immune memory
    for source in candidate.source_cluster:
        match = immune_memory.check_immune_match_for_source(source)
        if match is not None:
            return AuditResult(passed=False, reason=f"Source {source.id} matches immune signature")

    return AuditResult(passed=True, reason="All deep audit checks passed")
```

#### 5.3.6  Complete Consolidation Execution

```python
def execute_consolidation_cycle(
    knowledge_base: KnowledgeBase,
    vrf_secret_key: bytes,
    current_epoch: int
) -> List[EpistemicQuantum]:
    """Execute one full consolidation cycle.

    Called every CONSOLIDATION_CYCLE (36000s = 10 TIDAL_EPOCHs).
    """
    new_quanta = []

    # Step 1: Select candidate clusters via VRF
    active_quanta = knowledge_base.get_active_quanta()
    eligible_sources = filter_consolidation_sources(
        [(eq, 1.0) for eq in active_quanta]
    )
    clusters = identify_consolidation_clusters(eligible_sources)
    selected_clusters = vrf_select_for_consolidation(clusters, vrf_secret_key, current_epoch)

    for cluster in selected_clusters:
        # Step 2: Three-pass synthesis
        candidate = three_pass_synthesis(cluster)
        if candidate is None:
            continue

        # Step 3: Source independence verification (C10)
        independence = verify_source_independence(candidate)
        if not independence.passed:
            quarantine_candidate(candidate, "Source independence failure")
            continue

        # Step 4: CRP+ evaluation
        aprt_result = aprt_test(candidate)
        cods_result = cods_evaluate(candidate, knowledge_base)
        probe_result = probe_consolidation_adversarially(candidate, knowledge_base)
        immune_match = immune_memory.check_immune_match(candidate)
        purpose_score = source_purpose_score(candidate)

        crp_score = compute_crp_plus_score(
            aprt_result, cods_result, probe_result, immune_match, purpose_score
        )

        if crp_score.decision == Decision.REJECT:
            immune_memory.record_rejection(candidate, "CRP+ rejection", current_epoch)
            continue
        elif crp_score.decision == Decision.QUARANTINE:
            quarantine_candidate(candidate, f"CRP+ quarantine (score={crp_score.total:.3f})")
            continue

        # Step 5: Novelty pathway check
        if novelty_pathway_check(candidate):
            novelty_result = execute_novelty_pathway(candidate, current_epoch)
            if not novelty_result.passed:
                quarantine_candidate(candidate, f"Novelty pathway: {novelty_result.reason}")
                continue

        # Step 6: Adversarial probing (C10)
        candidate = apply_consolidation_probe(candidate)

        # Step 7: Lineage recording
        lineage = ConsolidationLineage(
            quantum_id=candidate.id,
            parent_consolidation_ids=[s.id for s in cluster if s.claim_class == 'K'],
            generation=max((s.lineage.generation for s in cluster if hasattr(s, 'lineage')),
                          default=-1) + 1,
            consolidation_timestamp=time.time()
        )
        lineage_db.record(lineage)

        # Step 8: PCVM submission
        new_quantum = create_k_class_quantum(candidate, lineage)
        submit_to_pcvm(new_quantum)  # may queue if degraded mode
        new_quanta.append(new_quantum)

    # Epoch maintenance
    immune_memory.garbage_collect(current_epoch)

    return new_quanta
```

### 5.4  Catabolism

Catabolism removes quanta that are no longer viable, using a two-phase process: quarantine followed by dissolution with evidence recycling.

#### 5.4.1  Catabolism Triggers

A quantum enters catabolism evaluation when:

1. `evaluate_catabolism_candidate()` returns True (vitality at floor for grace period).
2. A CONTRADICTION edge accumulates sufficient weight to drive disbelief above a threshold.
3. Manual flagging by administrative process.
4. Cascading credibility reduction pushes the quantum below viability (Section 5.3.3.3).
5. An H-class quantum becomes a non-frontier member of a RETIRED heuristic family for at least `HEURISTIC_FAMILY_RETIREMENT_MIN_EPOCHS`.

#### 5.4.2  Two-Phase Dissolution

**Phase 1 â€” Quarantine:**
The quantum transitions to QUARANTINED state. During quarantine:
- The quantum is excluded from retrieval results.
- Opinions are not updated (effectively frozen).
- A re-evaluation window of 3 TIDAL_EPOCHs allows for recovery if new supporting evidence arrives.
- `quarantine_entry_epoch` is recorded in timestamps.

**Phase 2 â€” Dissolution:**
If no recovery occurs during the quarantine window:

```python
@dataclass
class RecyclingTransfer:
    target_quantum_id: UUID
    evidence_type: str  # "support_weight", "provenance_link", "edge_transfer"
    amount: float

@dataclass
class RecyclingResult:
    dissolved_quantum_id: UUID
    transfers: List[RecyclingTransfer]
    dissolution_confidence: float
    provenance_chain: List[ProvenanceRecord]

def execute_recycling(quantum: EpistemicQuantum) -> RecyclingResult:
    """Execute evidence recycling during dissolution (INV-E8).

    1. Examine all outgoing SUPPORT and DERIVATION edges.
    2. For each child quantum deriving >50% belief from this parent,
       flag for re-evaluation.
    3. Transfer recyclable evidence to surviving quanta.
    4. Compute dissolution confidence.
    5. Build provenance chain for the dissolution event.
    """
    transfers = []

    # Examine outgoing edges
    for edge in quantum.edges:
        if edge.edge_type in (EdgeType.SUPPORT, EdgeType.DERIVATION):
            child = get_quantum(edge.target)
            parent_contribution = estimate_belief_contribution(quantum, child)

            if parent_contribution > 0.50:
                # Flag for re-evaluation (INV-E8)
                flag_for_reevaluation(child, reason=f"Parent {quantum.id} dissolved")

            # Check if evidence can be recycled
            if not _check_contradiction(quantum, child):
                transfer = RecyclingTransfer(
                    target_quantum_id=child.id,
                    evidence_type="support_weight",
                    amount=edge.weight * 0.5  # 50% of original weight transfers
                )
                transfers.append(transfer)

    # Compute dissolution confidence
    dissolution_confidence = max(0.1, quantum.credibility.trust_modifier * 0.5)

    # Build provenance chain
    provenance_chain = build_provenance_chain(quantum, transfers)

    # Execute state transition
    quantum.metabolic_state = MetabolicState.DISSOLVED
    quantum.dissolution_record = DissolutionRecord(
        timestamp=time.time(),
        reason="Catabolism â€” vitality exhaustion",
        evidence_redistributed=len(transfers),
        dissolution_confidence=dissolution_confidence
    )

    # Remove content, retain provenance
    quantum.content = None

    return RecyclingResult(
        dissolved_quantum_id=quantum.id,
        transfers=transfers,
        dissolution_confidence=dissolution_confidence,
        provenance_chain=provenance_chain
    )


def _check_contradiction(source: EpistemicQuantum, target: EpistemicQuantum) -> bool:
    """Check if source and target have active contradiction edges."""
    for edge in source.edges:
        if (edge.target == target.id and
            edge.edge_type == EdgeType.CONTRADICTION and
            edge.weight > 0.1):
            return True
    return False

def build_provenance_chain(quantum: EpistemicQuantum,
                            transfers: List[RecyclingTransfer]) -> List[ProvenanceRecord]:
    """Build W3C PROV-compatible chain for dissolution event."""
    records = []
    records.append(ProvenanceRecord(
        activity_type="dissolution",
        entity_id=quantum.id,
        timestamp=time.time(),
        attributes={
            "dissolution_type": "catabolism",
            "transfer_count": len(transfers),
            "original_claim_class": quantum.claim_class
        }
    ))
    for transfer in transfers:
        records.append(ProvenanceRecord(
            activity_type="evidence_recycling",
            entity_id=transfer.target_quantum_id,
            timestamp=time.time(),
            attributes={
                "source_quantum": str(quantum.id),
                "evidence_type": transfer.evidence_type,
                "amount": transfer.amount
            }
        ))
    return records
```

#### 5.4.3  Archive Layer

Dissolution removes content but retains provenance stubs in the active system. Without an archive specification, dissolved quanta accumulate indefinitely in the active store, consuming space without providing retrieval value, and historical knowledge becomes irrecoverable.

The Archive Layer moves dissolved quantum records from the active metabolic store to a cold-tier archive optimized for long-term retention, space efficiency, and historical retrieval.

##### 5.4.3.1  Archive Scope

The archive stores **dissolved quantum records** â€” provenance, dissolution records, edge tombstones, and metadata â€” but NOT content (which was removed at dissolution). It also stores **superseded consolidation records** â€” when a K-class quantum is re-consolidated, the prior version's provenance chain is archived.

The archive does NOT store active, dormant, or quarantined quanta. Those remain in the metabolic store.

##### 5.4.3.2  Archive Record

Each archived quantum produces a compact record:

```
ArchiveRecord:
  quantum_id:          UUID        -- original quantum ID
  claim_class:         str         -- claim class at dissolution
  ingestion_epoch:     EpochID     -- when the quantum entered the system
  dissolution_epoch:   EpochID     -- when dissolution completed
  archive_epoch:       EpochID     -- when moved to archive
  lifespan_epochs:     int         -- dissolution_epoch - ingestion_epoch

  # Provenance (preserved in full)
  provenance_chain:    List[ProvenanceRecord]   -- W3C PROV records
  dissolution_record:  DissolutionRecord        -- reason, confidence, transfers

  # Graph context (tombstone summary, not full edges)
  edge_summary:
    support_targets:   List[UUID]  -- quanta this quantum supported
    derivation_targets: List[UUID] -- quanta derived from this quantum
    contradiction_targets: List[UUID] -- quanta this quantum contradicted
    total_edge_count:  int
    recycling_transfers: List[RecyclingTransfer]

  # Integrity
  archive_hash:        SHA-256     -- hash of this record
  prev_archive_hash:   SHA-256     -- chain integrity within archive partition
```

Content fields (`content`, `structured_claim`, `opinion`) are NOT archived â€” they were removed at dissolution. If content recovery is needed, the provenance chain points to source quanta (which may themselves be archived or active).

##### 5.4.3.3  Archive Timing

Dissolved quanta are moved to the archive at the next CONSOLIDATION_CYCLE boundary after dissolution. This provides a buffer during which:
- Downstream quanta flagged for re-evaluation (Section 5.4.2) can reference the dissolved quantum's metadata
- C34 BSRF recovery can access dissolution records if a recovery event occurs within the same consolidation cycle

The archive transfer is a batch operation:

```python
def archive_dissolved_quanta(current_cycle: int) -> int:
    """Move dissolved quanta to archive at CONSOLIDATION_CYCLE boundary.
    Returns count of archived records."""
    candidates = query_quanta(
        state=MetabolicState.DISSOLVED,
        dissolved_before=current_cycle  # dissolved in a prior cycle
    )
    archived = 0
    for quantum in candidates:
        record = build_archive_record(quantum)
        archive_store.append(record)
        active_store.remove_provenance_stub(quantum.id)
        archived += 1
    return archived
```

##### 5.4.3.4  Archive Partitioning

Archives are partitioned by CONSOLIDATION_CYCLE for efficient range queries and retention enforcement:

```
archive/
  cycle_00001/    -- ArchiveRecords from first consolidation cycle
  cycle_00002/
  ...
  cycle_NNNNN/
```

Each partition is immutable once sealed. Partitions are hash-chained (`prev_archive_hash`) within the partition for tamper detection.

Cross-partition queries (e.g., "find all dissolved K-class quanta from the last 100 cycles") use partition-level indexes on `claim_class`, `dissolution_epoch`, and `quantum_id`.

##### 5.4.3.5  Retention Policy

Archive retention is governed by claim class:

| Claim Class | Retention | Rationale |
|-------------|-----------|-----------|
| G (Governance) | Perpetual | Constitutional and governance decisions are permanently archived |
| K (Knowledge Consolidation) | Perpetual | Consolidation lineage must remain traceable for CRP+ immune memory |
| H (Heuristic) | 10 CONSOLIDATION_CYCLEs (~100 hours) | Heuristics are ephemeral by design |
| D, C, P, R, E, S, N | ARCHIVE_RETENTION_CYCLES (default: 100) | Standard retention, configurable |

After active retention expires, eligible records are handed to the Bundle Compaction Engine (Section 5.4.4) rather than being immediately collapsed to a one-line summary. Bundle compaction is lossless with respect to the pre-compaction archive representation: every archived record entering the engine remains reconstructable byte-for-byte from the compacted bundle manifest plus chunk store.

When a heuristic family transitions to `RETIRED` (Section 7.2.5), archived H-class members sharing the same `heuristic_family_id` SHOULD be queued together for Bundle Compaction once all holds clear. This preserves version lineage while allowing stale heuristic branches to age out of hot and warm storage as one unit.

Only non-perpetual classes MAY later be reduced to a statistical summary, and only after the compacted bundle itself has exceeded `COMPACTED_BUNDLE_RETENTION_CYCLES` with no recovery hold, governance hold, or pending re-verification. G-class and K-class records skip this final lossy summarization step and retain their compacted bundles indefinitely.

##### 5.4.3.6  Archive Retrieval

The archive supports read-only queries for:

- **Provenance tracing**: Given a quantum_id, retrieve its full dissolution provenance. Used by C5 PCVM for deep-audit verification of historical claims.
- **Lineage reconstruction**: Given a K-class quantum_id, retrieve all source quanta that contributed to its consolidation (via `derivation_targets`). Used by CRP+ immune memory (Section 5.3.4.7) to verify historical attack patterns.
- **Statistical queries**: Dissolution rate by claim class, average lifespan by claim class, recycling transfer patterns. Used by SHREC (Section 6) for budget allocation tuning.
- **Governance audit**: All G-class archive records within a date range. Used by AiSIA (C14 Section 16) for governance compliance monitoring.
- **Bundle-backed reconstruction**: Given a `quantum_id` or `bundle_id`, reconstruct the exact pre-compaction archive record from a compacted bundle. Used by C5 PCVM, C34 BSRF, and forensic operators when archived data has already passed through BCE.

Archive retrieval is always read-only. Archived records are never modified, reactivated, or returned to the metabolic store. If the target record resides inside a compacted bundle, retrieval reconstructs the exact archived representation on demand without permanently expanding the bundle. A dissolved quantum that is later found to have been incorrectly dissolved is addressed by ingesting new evidence â€” not by resurrecting the archived record.

##### 5.4.3.7  Integration Points

| Consumer | What Archive Provides | Interface |
|----------|----------------------|-----------|
| **CRP+ Immune Memory (5.3.4.7)** | Historical attack patterns for L1/L2/L3 matching | `query(claim_class=K, dissolution_reason=crp_quarantine)` |
| **C5 PCVM** | Historical claim provenance for deep-audit | `provenance_trace(quantum_id)` |
| **C14 AiSIA** | Governance record audit trail | `query(claim_class=G, epoch_range)` |
| **C34 BSRF** | Recovery-time provenance verification | Partition-level access during recovery |
| **C33 OINC** | Incident correlation with historical knowledge events | `query(dissolution_epoch, claim_class)` |
| **SHREC (Section 6)** | Dissolution statistics for budget tuning | `statistics(claim_class, epoch_range)` |

##### 5.4.3.8  Parameters

| Parameter | Default | Range | Governor |
|-----------|---------|-------|----------|
| ARCHIVE_RETENTION_CYCLES | 100 | 10â€“1000 | Operations |
| ARCHIVE_COMPACTION_BATCH_SIZE | 1000 | 100â€“10000 | Operations |
| ARCHIVE_PARTITION_SIZE_MAX | 100,000 records | 10,000â€“1,000,000 | Operations |

#### 5.4.4  Bundle Compaction Engine

The Bundle Compaction Engine (BCE) reduces cold-tier storage cost for related archived knowledge without losing information relative to the pre-compaction archive representation. BCE is not a second consolidation pipeline: it does not synthesize new claims, adjust opinions, or collapse disagreement. It only rewrites storage layout for groups of related records that are already cold, sealed, and semantically closed enough to compact safely.

Lossless means: every pre-compaction `ArchiveRecord` or superseded consolidation record entering BCE MUST be reconstructable byte-for-byte from the compacted bundle manifest plus chunk store. BCE does NOT restore content already removed during dissolution; the guarantee applies to the archive-level representation entering BCE.

##### 5.4.4.1  Bundle Eligibility

An epistemic bundle is a connected cold-tier record set selected by one or more of:
- shared `family_id`
- shared `heuristic_family_id`
- shared provenance roots
- direct SUPPORT / DERIVATION / SUPERSESSION connectivity
- common archive partition and consolidation window

A bundle may be compacted only if:

1. every member is an `ArchiveRecord` or superseded consolidation record already admitted to cold storage;
2. no member is under open re-verification, recovery hold, governance hold, or active contradiction arbitration;
3. all internal SUPPORT / DERIVATION / SUPERSESSION edges are either captured inside the bundle or emitted as explicit boundary references;
4. bundle cardinality is at least `BUNDLE_COMPACTION_MIN_RECORDS` or total canonical bytes exceed `BUNDLE_TARGET_CHUNK_SIZE * 4`;
5. every member has a canonical serialization and `original_record_hash`.

ACTIVE, DORMANT, and QUARANTINED quanta MUST NOT enter BCE. BCE operates after catabolism and archive admission, not instead of them.

If all archived members in a candidate bundle belong to the same RETIRED heuristic family, the BCE scheduler SHOULD multiply that bundle's queue priority by `HEURISTIC_FAMILY_BUNDLE_PRIORITY` so stale heuristic branches compact before unrelated cold storage.

##### 5.4.4.2  Compaction Bundle Manifest

```python
@dataclass
class BundleMemberManifest:
    quantum_id: UUID
    original_record_hash: bytes
    original_byte_length: int
    claim_class: str
    chunk_refs: List[bytes]              # ordered SHA-256 chunk hashes
    provenance_ref_ids: List[bytes]      # dictionary entries used by this member
    edge_ref_ids: List[bytes]            # dictionary entries used by this member
    boundary_refs: List[UUID]            # edges leaving the bundle

@dataclass
class CompactionBundle:
    bundle_id: bytes
    source_partition: str
    created_cycle: int
    member_manifests: Dict[UUID, BundleMemberManifest]
    provenance_dictionary: Dict[bytes, ProvenanceRecord]
    edge_dictionary: Dict[bytes, dict]
    chunk_store: Dict[bytes, bytes]      # hash -> canonical byte chunk
    pre_compaction_root: bytes
    bundle_root: bytes
    original_bytes: int
    compacted_bytes: int
    reversible: bool
```

`bundle_id = SHA256(source_partition || canonical_serialize(sorted(member_hashes)) || created_cycle)`

The `pre_compaction_root` is a Merkle root over the ordered `original_record_hash` set. `bundle_root` is a Merkle root over the manifest plus `chunk_store`. A bundle is valid only when `reversible = True`.

##### 5.4.4.3  Reference Algorithm

```python
def compact_bundle(records: List[ArchiveRecord], current_cycle: int) -> CompactionBundle:
    normalized_records = []
    provenance_dict = {}
    edge_dict = {}

    for record in records:
        canonical = canonical_serialize(record)
        original_hash = SHA256(canonical)
        normalized = intern_repeated_structures(
            canonical, provenance_dict, edge_dict)
        normalized_records.append((record.quantum_id, canonical, normalized, original_hash))

    chunk_store = {}
    manifests = {}

    for quantum_id, canonical, normalized, original_hash in normalized_records:
        chunks = rolling_chunk(normalized, target_size=BUNDLE_TARGET_CHUNK_SIZE)
        refs = []
        for chunk in chunks:
            chunk_hash = SHA256(chunk)
            chunk_store.setdefault(chunk_hash, chunk)
            refs.append(chunk_hash)

        manifests[quantum_id] = BundleMemberManifest(
            quantum_id=quantum_id,
            original_record_hash=original_hash,
            original_byte_length=len(canonical),
            claim_class=extract_claim_class(canonical),
            chunk_refs=refs,
            provenance_ref_ids=extract_provenance_refs(normalized),
            edge_ref_ids=extract_edge_refs(normalized),
            boundary_refs=extract_boundary_refs(canonical)
        )

    bundle = CompactionBundle(
        bundle_id=derive_bundle_id(manifests, current_cycle),
        source_partition=current_archive_partition(),
        created_cycle=current_cycle,
        member_manifests=manifests,
        provenance_dictionary=provenance_dict,
        edge_dictionary=edge_dict,
        chunk_store=chunk_store,
        pre_compaction_root=merkle_root([m.original_record_hash for m in manifests.values()]),
        bundle_root=compute_bundle_root(manifests, provenance_dict, edge_dict, chunk_store),
        original_bytes=sum(m.original_byte_length for m in manifests.values()),
        compacted_bytes=estimate_bundle_bytes(provenance_dict, edge_dict, chunk_store),
        reversible=True
    )

    for quantum_id, canonical, _, _ in normalized_records:
        reconstructed = reconstruct_bundle_member(bundle, quantum_id)
        assert SHA256(reconstructed) == manifests[quantum_id].original_record_hash
        assert reconstructed == canonical

    seal_bundle(bundle)
    delete_source_records(records)
    return bundle
```

If any reconstruction check fails, the compaction attempt MUST abort and leave source records intact.

##### 5.4.4.4  Reconstruction Protocol

```python
def reconstruct_bundle_member(bundle: CompactionBundle, quantum_id: UUID) -> bytes:
    manifest = bundle.member_manifests[quantum_id]
    normalized = b"".join(bundle.chunk_store[h] for h in manifest.chunk_refs)
    canonical = expand_dictionaries(
        normalized,
        provenance_dictionary=bundle.provenance_dictionary,
        edge_dictionary=bundle.edge_dictionary
    )
    if SHA256(canonical) != manifest.original_record_hash:
        raise ReconstructionError(f"Hash mismatch for {quantum_id}")
    return canonical
```

Bundle-backed reconstruction is transparent to callers: retrieval by `quantum_id` MUST return the same canonical archive record regardless of whether the record is stored raw or inside a compacted bundle. Reconstruction failures are fail-closed events and MUST emit alerts to C33 OINC and C34 BSRF.

##### 5.4.4.5  Holds, Expiry, and Final Summaries

BCE obeys the following hold rules:
- any open re-verification on a member blocks compaction;
- any governance or legal hold blocks compaction and later lossy summarization;
- any BSRF recovery hold blocks source-record deletion until the hold clears.

After a bundle is sealed, non-perpetual classes MAY be reduced to a statistical summary only after `COMPACTED_BUNDLE_RETENTION_CYCLES` if:
- no member is under any hold,
- the bundle has been reconstructed successfully at least once during integrity audit, and
- a summary record preserving `bundle_id`, member IDs, lifespan statistics, and dissolution reasons is persisted.

Perpetual G-class and K-class bundles MUST remain reconstructable and MUST NOT be reduced to summary-only form.

##### 5.4.4.6  Integration Points

| Consumer | What BCE Provides | Interface |
|----------|-------------------|-----------|
| **Archive retrieval (5.4.3.6)** | Exact record reconstruction after cold-tier compaction | `reconstruct(quantum_id)` |
| **C5 PCVM** | Deep-audit access to compacted historical provenance | `reconstruct(quantum_id)` |
| **C34 BSRF** | Recovery-time byte-exact archive replay | partition scan + `reconstruct(quantum_id)` |
| **C33 OINC** | Compaction failure and integrity audit events | `emit(bundle_id, event_type)` |
| **SHREC (Section 6)** | Storage pressure and compaction ratio metrics | `bundle_stats(epoch_range)` |

##### 5.4.4.7  Parameters

| Parameter | Default | Range | Governor |
|-----------|---------|-------|----------|
| BUNDLE_COMPACTION_MIN_RECORDS | 32 | 4-1000 | Operations |
| BUNDLE_TARGET_CHUNK_SIZE | 4096 bytes | 512-65536 bytes | Operations |
| BUNDLE_MAX_RECONSTRUCT_MS | 500 ms | 50-5000 ms | Operations |
| COMPACTED_BUNDLE_RETENTION_CYCLES | 100 | 10-1000 | Operations |

---

## 6  SHREC â€” Stratified Homeostatic Regulation with Ecological Competition

### 6.1  Overview

SHREC governs how the fixed processing budget is distributed among the five metabolic functions. It combines:

1. **Five regulatory signals** that measure system health.
2. **Lotka-Volterra ecological competition** for emergent resource allocation.
3. **A four-regime graduated controller** that escalates intervention proportionally.
4. **Floor enforcement** ensuring minimum viability of all metabolic functions.
5. **Statistical self-model** for anomaly detection.
6. **Immune self-audit** for quality assurance.

### 6.2  Five Regulatory Signals

| Signal | Symbol | Measures | Range |
|---|---|---|---|
| **Ingestion Pressure** | Ïƒ_I | Ratio of queued claims to ingestion capacity | [0, âˆž) |
| **Circulation Load** | Ïƒ_C | Active quanta requiring opinion updates per tick | [0, âˆž) |
| **Consolidation Readiness** | Ïƒ_K | Fraction of clusters meeting consolidation criteria | [0, 1] |
| **Catabolism Urgency** | Ïƒ_X | Fraction of quanta at or near vitality floor | [0, 1] |
| **Coherence Stress** | Ïƒ_H | Unresolved contradictions / total edges | [0, 1] |

Signal intensities are measured at every TIDAL_EPOCH and fed into the Lotka-Volterra dynamics.

### 6.3  Lotka-Volterra Competition Model

The five metabolic functions are modelled as competing species sharing a fixed resource pool:

```python
@dataclass
class SHRECControllerState:
    allocations: Dict[str, float]          # current budget allocations
    floors: Dict[str, float]               # minimum allocations
    signals: Dict[str, float]              # current signal intensities
    regime: str                            # NORMAL, ELEVATED, CRITICAL, EMERGENCY
    regime_epoch_count: int                # epochs in current regime
    frozen_allocations: Optional[Dict[str, float]]  # for EMERGENCY
    pid_integral: Dict[str, float]         # PID integral terms
    pid_prev_error: Dict[str, float]       # PID previous errors

    # Competition coefficients (Î±_ij)
    competition_matrix: Dict[Tuple[str, str], float]

SPECIES = ["ingest", "circ", "consol", "catab", "coher"]

# Intrinsic growth rates
GROWTH_RATES = {
    "ingest": 0.15, "circ": 0.20, "consol": 0.10,
    "catab": 0.10, "coher": 0.15
}

# Carrying capacities (soft targets)
CARRYING_CAPACITIES = {
    "ingest": 0.30, "circ": 0.35, "consol": 0.25,
    "catab": 0.15, "coher": 0.20
}
```

#### 6.3.1  Corrected LV Step (PA-1)

Signal intensity modulates ONLY the competitive dynamics; floor correction is applied AFTER the LV step:

```python
def lotka_volterra_step(state: SHRECControllerState, dt: float = 1.0) -> Dict[str, float]:
    """Compute one LV competition step.

    CRITICAL: Signal intensity modulates competition coefficients,
    NOT allocations directly. Floor correction applied AFTER.
    """
    new_alloc = {}

    for i in SPECIES:
        N_i = state.allocations[i]
        r_i = GROWTH_RATES[i]
        K_i = CARRYING_CAPACITIES[i]
        sigma_i = state.signals[i]

        # Competition term: sum of Î±_ij * N_j, modulated by signal intensity
        competition = 0.0
        for j in SPECIES:
            if i != j:
                alpha_ij = state.competition_matrix.get((i, j), 0.1)
                # Signal intensity modulates competitive pressure
                modulated_alpha = alpha_ij * (1.0 + sigma_i)
                competition += modulated_alpha * state.allocations[j]

        # LV dynamics
        dN_i = r_i * N_i * (1.0 - (N_i + competition) / K_i)
        new_alloc[i] = max(0.0, N_i + dN_i * dt)

    # Normalise to sum to 1.0
    total = sum(new_alloc.values())
    if total > 0:
        new_alloc = {k: v / total for k, v in new_alloc.items()}

    # Floor correction AFTER normalisation
    new_alloc = enforce_floors(new_alloc, state.floors)

    return new_alloc


def enforce_floors(alloc: Dict[str, float], floors: Dict[str, float]) -> Dict[str, float]:
    """Enforce minimum allocations, redistributing deficit proportionally."""
    result = dict(alloc)

    # Phase 1: lift any species below floor
    deficit = 0.0
    for species in SPECIES:
        if result[species] < floors[species]:
            deficit += floors[species] - result[species]
            result[species] = floors[species]

    # Phase 2: redistribute deficit from above-floor species proportionally
    if deficit > 0:
        above_floor = {s: result[s] - floors[s] for s in SPECIES if result[s] > floors[s]}
        total_above = sum(above_floor.values())
        if total_above > 0:
            for s, surplus in above_floor.items():
                reduction = deficit * (surplus / total_above)
                result[s] -= reduction

    # Phase 3: final normalisation
    total = sum(result.values())
    result = {k: v / total for k, v in result.items()}

    return result
```

### 6.4  Statistical Self-Model

SHREC maintains a rolling statistical model of its own signal history for anomaly detection:

```python
SIGNAL_HISTORY_WINDOW = 50  # TIDAL_EPOCHs

def compute_z_scores(state: SHRECControllerState) -> Dict[str, float]:
    """Compute z-scores for each signal relative to historical distribution."""
    z_scores = {}
    for signal_name, current_value in state.signals.items():
        history = state.signal_history[signal_name][-SIGNAL_HISTORY_WINDOW:]
        if len(history) < 5:
            z_scores[signal_name] = 0.0
            continue
        mean = sum(history) / len(history)
        variance = sum((x - mean) ** 2 for x in history) / len(history)
        std = math.sqrt(variance) if variance > 0 else 1e-6
        z_scores[signal_name] = (current_value - mean) / std
    return z_scores
```

### 6.5  Budget Conservation Enforcement

Budget conservation (INV-E4, INV-E11) is enforced iteratively after every allocation computation:

```python
BUDGET_EPSILON = 1e-9

def enforce_budget_conservation(
    allocations: Dict[str, float],
    floors: Dict[str, float]
) -> Dict[str, float]:
    """Iterative budget conservation to ensure sum = 1.0 and all floors met.

    Runs up to 10 iterations to converge.
    """
    result = dict(allocations)

    for iteration in range(10):
        # Check floors
        for species in SPECIES:
            if result[species] < floors[species]:
                result[species] = floors[species]

        # Normalise
        total = sum(result.values())
        if abs(total - 1.0) < BUDGET_EPSILON:
            break
        result = {k: v / total for k, v in result.items()}

        # Verify floors still hold after normalisation
        all_floors_met = all(result[s] >= floors[s] - BUDGET_EPSILON for s in SPECIES)
        if all_floors_met:
            break

    assert abs(sum(result.values()) - 1.0) < BUDGET_EPSILON, "INV-E4/INV-E11 violation"
    return result
```

### 6.6  PID Controller

The PID controller provides additional correction in ELEVATED and CRITICAL regimes:

```python
PID_KP = 0.5   # Proportional gain
PID_KI = 0.1   # Integral gain
PID_KD = 0.05  # Derivative gain

def compute_pid_correction(
    state: SHRECControllerState,
    target_allocations: Dict[str, float]
) -> Dict[str, float]:
    """Compute PID corrections based on error between target and current allocation."""
    corrections = {}

    for species in SPECIES:
        error = target_allocations[species] - state.allocations[species]

        # Update integral (with anti-windup)
        state.pid_integral[species] += error
        state.pid_integral[species] = max(-1.0, min(1.0, state.pid_integral[species]))

        # Derivative
        derivative = error - state.pid_prev_error.get(species, 0.0)
        state.pid_prev_error[species] = error

        # PID output
        correction = PID_KP * error + PID_KI * state.pid_integral[species] + PID_KD * derivative
        corrections[species] = correction

    return corrections
```

### 6.7  Four-Regime Graduated Controller

The SHREC controller operates in four regimes, escalating based on system stress:

| Regime | Entry Condition | LV Active | PID Active | Clamp Bounds | Behaviour |
|---|---|---|---|---|---|
| **NORMAL** | max(z) < 1.5 | Yes | No | N/A | Pure LV allocation |
| **ELEVATED** | max(z) â‰¥ 1.5 | Yes | Yes | Â±10% | LV + bounded PID correction |
| **CRITICAL** | max(z) â‰¥ 2.5 | Secondary | Yes (primary) | Â±25% | PID-driven with LV as fallback |
| **EMERGENCY** | max(z) â‰¥ 4.0 OR invariant violation | No | No | Frozen | Static hold at entry values |

> **CONSTITUTIONAL regime (deprecated):** Versions prior to v2.0 defined a CONSTITUTIONAL regime with unclamped PID. This has been replaced by EMERGENCY (static hold), which provides deterministic stability guarantees.

#### 6.7.1  Regime Transition Logic

```python
REGIME_THRESHOLDS = {
    "NORMAL_TO_ELEVATED": 1.5,
    "ELEVATED_TO_CRITICAL": 2.5,
    "CRITICAL_TO_EMERGENCY": 4.0,
}

HYSTERESIS_EPOCHS = 5  # consecutive epochs required for downgrade

def compute_regime(state: SHRECControllerState,
                   z_scores: Dict[str, float]) -> str:
    """Determine current regime based on z-scores and transition rules.

    Upgrades: immediate on threshold crossing.
    Downgrades: require HYSTERESIS_EPOCHS consecutive epochs below threshold (INV-E13).
    """
    max_z = max(abs(z) for z in z_scores.values())
    current = state.regime

    # Check for invariant violations (force EMERGENCY)
    invariant_violations = check_invariant_violations(state)
    if invariant_violations:
        return "EMERGENCY"

    # Upgrade checks (immediate)
    if max_z >= REGIME_THRESHOLDS["CRITICAL_TO_EMERGENCY"]:
        return "EMERGENCY"
    elif max_z >= REGIME_THRESHOLDS["ELEVATED_TO_CRITICAL"]:
        if current in ("NORMAL", "ELEVATED"):
            return "CRITICAL"
        return current
    elif max_z >= REGIME_THRESHOLDS["NORMAL_TO_ELEVATED"]:
        if current == "NORMAL":
            return "ELEVATED"
        return current

    # Downgrade checks (require hysteresis)
    if current == "EMERGENCY":
        if max_z < REGIME_THRESHOLDS["ELEVATED_TO_CRITICAL"]:
            state.downgrade_counter = state.downgrade_counter + 1
            if state.downgrade_counter >= HYSTERESIS_EPOCHS:
                state.downgrade_counter = 0
                return "CRITICAL"
        else:
            state.downgrade_counter = 0
        return "EMERGENCY"

    elif current == "CRITICAL":
        if max_z < REGIME_THRESHOLDS["NORMAL_TO_ELEVATED"]:
            state.downgrade_counter += 1
            if state.downgrade_counter >= HYSTERESIS_EPOCHS:
                state.downgrade_counter = 0
                return "NORMAL"
        elif max_z < REGIME_THRESHOLDS["ELEVATED_TO_CRITICAL"]:
            state.downgrade_counter += 1
            if state.downgrade_counter >= HYSTERESIS_EPOCHS:
                state.downgrade_counter = 0
                return "ELEVATED"
        else:
            state.downgrade_counter = 0
        return "CRITICAL"

    elif current == "ELEVATED":
        if max_z < REGIME_THRESHOLDS["NORMAL_TO_ELEVATED"]:
            state.downgrade_counter += 1
            if state.downgrade_counter >= HYSTERESIS_EPOCHS:
                state.downgrade_counter = 0
                return "NORMAL"
        else:
            state.downgrade_counter = 0
        return "ELEVATED"

    return current


def check_invariant_violations(state: SHRECControllerState) -> List[str]:
    """Check for invariant violations that force EMERGENCY regime."""
    violations = []
    total = sum(state.allocations.values())
    if abs(total - 1.0) > 1e-6:
        violations.append(f"INV-E4: budget sum {total} != 1.0")
    for species in SPECIES:
        if state.allocations[species] < state.floors[species] - 1e-6:
            violations.append(f"INV-E12: {species} below floor")
    return violations
```

#### 6.7.2  Controller Combination

```python
ELEVATED_CLAMP = 0.10   # Â±10%
CRITICAL_CLAMP = 0.25   # Â±25%

def combine_controllers(
    state: SHRECControllerState,
    lv_allocations: Dict[str, float],
    pid_corrections: Dict[str, float],
    regime: str
) -> Dict[str, float]:
    """Combine LV and PID outputs according to current regime."""

    if regime == "NORMAL":
        # Pure LV
        return lv_allocations

    elif regime == "ELEVATED":
        # LV + clamped PID
        combined = {}
        for s in SPECIES:
            correction = max(-ELEVATED_CLAMP, min(ELEVATED_CLAMP, pid_corrections[s]))
            combined[s] = lv_allocations[s] + correction
        return combined

    elif regime == "CRITICAL":
        # PID primary, LV secondary
        combined = {}
        for s in SPECIES:
            correction = max(-CRITICAL_CLAMP, min(CRITICAL_CLAMP, pid_corrections[s]))
            # PID drives, LV provides baseline
            combined[s] = state.allocations[s] + correction
        return combined

    elif regime == "EMERGENCY":
        # Frozen static hold (INV-E14)
        if state.frozen_allocations is None:
            state.frozen_allocations = dict(state.allocations)
        return dict(state.frozen_allocations)

    else:
        raise ValueError(f"Unknown regime: {regime}")
```

#### 6.7.3  Complete SHREC Epoch Step

```python
def shrec_epoch_step(state: SHRECControllerState) -> SHRECControllerState:
    """Execute one complete SHREC epoch step.

    Called every TIDAL_EPOCH (3600s).
    """
    # 1. Measure signals
    state.signals = measure_all_signals()

    # 2. Update signal history
    for signal_name, value in state.signals.items():
        state.signal_history.setdefault(signal_name, []).append(value)

    # 3. Compute z-scores
    z_scores = compute_z_scores(state)

    # 4. Determine regime
    new_regime = compute_regime(state, z_scores)
    if new_regime != state.regime:
        log_regime_transition(state.regime, new_regime, z_scores)
        if new_regime == "EMERGENCY":
            state.frozen_allocations = dict(state.allocations)
        state.regime = new_regime
        state.regime_epoch_count = 0
    else:
        state.regime_epoch_count += 1

    # 5. Compute LV allocations
    lv_alloc = lotka_volterra_step(state)

    # 6. Compute PID corrections (if applicable)
    pid_corr = compute_pid_correction(state, lv_alloc)

    # 7. Combine according to regime
    combined = combine_controllers(state, lv_alloc, pid_corr, state.regime)

    # 8. Enforce budget conservation and floors
    final = enforce_budget_conservation(combined, state.floors)

    # 9. Verify invariants
    assert abs(sum(final.values()) - 1.0) < BUDGET_EPSILON, "INV-E11"
    for s in SPECIES:
        assert final[s] >= state.floors[s] - BUDGET_EPSILON, f"INV-E12: {s}"
    if state.regime == "EMERGENCY" and state.frozen_allocations:
        for s in SPECIES:
            assert abs(final[s] - state.frozen_allocations[s]) < BUDGET_EPSILON, f"INV-E14: {s}"

    # 10. Apply
    state.allocations = final

    return state
```

### 6.8  Immune Self-Audit

SHREC performs periodic immune self-audits to detect regulatory dysfunction:

```python
IMMUNE_AUDIT_LOOKBACK_EPOCHS = 5

def immune_self_audit(state: SHRECControllerState, current_epoch: int) -> AuditReport:
    """Audit recent quarantine and dissolution actions for anomalies.

    Lookback window: IMMUNE_AUDIT_LOOKBACK_EPOCHS (5 epochs).
    """
    recently_quarantined = get_recently_quarantined(
        current_epoch - IMMUNE_AUDIT_LOOKBACK_EPOCHS, current_epoch
    )
    recently_dissolved = get_recently_dissolved(
        current_epoch - IMMUNE_AUDIT_LOOKBACK_EPOCHS, current_epoch
    )

    anomalies = []

    # Check 1: Quarantine rate anomaly
    quarantine_rate = len(recently_quarantined) / max(1, get_active_quantum_count())
    if quarantine_rate > 0.05:
        anomalies.append(f"High quarantine rate: {quarantine_rate:.3f}")

    # Check 2: Dissolution rate anomaly
    dissolution_rate = len(recently_dissolved) / max(1, get_active_quantum_count())
    if dissolution_rate > 0.02:
        anomalies.append(f"High dissolution rate: {dissolution_rate:.3f}")

    # Check 3: Claim class distribution skew
    class_distribution = Counter(q.claim_class for q in recently_quarantined)
    for cls, count in class_distribution.items():
        if count > len(recently_quarantined) * 0.5:
            anomalies.append(f"Quarantine skew: {cls} class dominates ({count}/{len(recently_quarantined)})")

    return AuditReport(
        epoch=current_epoch,
        lookback=IMMUNE_AUDIT_LOOKBACK_EPOCHS,
        quarantine_count=len(recently_quarantined),
        dissolution_count=len(recently_dissolved),
        anomalies=anomalies,
        recommendation="ELEVATED" if anomalies else "NORMAL"
    )


def get_recently_quarantined(start_epoch: int, end_epoch: int) -> List[EpistemicQuantum]:
    """Retrieve quanta quarantined within the epoch range."""
    return [q for q in knowledge_base.all_quanta()
            if q.metabolic_state == MetabolicState.QUARANTINED
            and start_epoch <= q.timestamps.quarantine_entry_epoch <= end_epoch]

def get_recently_dissolved(start_epoch: int, end_epoch: int) -> List[EpistemicQuantum]:
    """Retrieve quanta dissolved within the epoch range."""
    return [q for q in knowledge_base.all_quanta()
            if q.metabolic_state == MetabolicState.DISSOLVED
            and q.dissolution_record is not None
            and start_epoch <= q.dissolution_record.epoch <= end_epoch]
```

### 6.9  Stability Analysis

The SHREC system's stability can be characterised by the eigenvalues of the Jacobian of the LV system at equilibrium. The four-regime controller provides progressively stronger stabilisation:

1. **NORMAL:** LV dynamics converge to a stable fixed point if all eigenvalues have negative real parts. The competition matrix is calibrated to ensure this.
2. **ELEVATED:** PID correction with Â±10% clamp dampens oscillations that the LV system alone might exhibit.
3. **CRITICAL:** PID-primary control provides direct proportional stabilisation, bypassing potentially unstable LV dynamics.
4. **EMERGENCY:** Static hold guarantees zero-variance stability at the cost of adaptivity.

The hysteresis requirement (HYSTERESIS_EPOCHS = 5) for downgrades prevents regime oscillation at threshold boundaries.

---

## 7  Coherence Graph

### 7.1  Overview

The coherence graph is a typed, weighted, bidirectional graph where nodes are epistemic quanta and edges represent epistemic relationships. It serves as the structural backbone for consistency maintenance, contradiction detection, and belief revision.

At scale, the graph is partitioned into shards with a border graph maintaining cross-shard relationships. Edges are classified into access tiers (HOT/WARM/COLD) to enable efficient tiered updates.

### 7.2  Graph Structure and Sharding

#### 7.2.1  Core Data Model

```python
@dataclass
class CoherenceEdge:
    source_id: UUID
    target_id: UUID
    edge_type: EdgeType          # SUPPORT, CONTRADICTION, DERIVATION, ANALOGY, SUPERSESSION
    weight: float                # [0.0, 1.0]
    created_epoch: int
    last_accessed_epoch: int
    last_updated_epoch: int
    access_count: int
    tier: str                    # HOT, WARM, COLD
    creating_agent: Optional[AgentID]

@dataclass
class CoherenceShard:
    shard_id: int
    quanta: Dict[UUID, EpistemicQuantum]
    intra_edges: Dict[Tuple[UUID, UUID], CoherenceEdge]
    cross_edges: Dict[Tuple[UUID, UUID], CoherenceEdge]  # edges to other shards

    @property
    def quantum_count(self) -> int:
        return len(self.quanta)

    @property
    def intra_edge_count(self) -> int:
        return len(self.intra_edges)

    @property
    def cross_edge_count(self) -> int:
        return len(self.cross_edges)

@dataclass
class BorderGraph:
    """Global graph of cross-shard edges (INV-E19).

    Maintained as a lightweight structure mapping shard pairs
    to their connecting edges.
    """
    edges: Dict[Tuple[int, int], List[CoherenceEdge]]  # (shard_i, shard_j) -> edges
    shard_connectivity: Dict[int, Set[int]]              # shard_id -> connected shards
```

#### 7.2.2  Shard Limits

| Parameter | Value | Description |
|---|---|---|
| `MAX_QUANTA_PER_SHARD` | 1 000 000 | Maximum active quanta per shard (INV-E15) |
| `MAX_INTRA_EDGES_PER_SHARD` | 5 000 000 | Maximum intra-shard edges (INV-E18) |
| `MAX_CROSS_EDGES_PER_SHARD` | 500 000 | Maximum cross-shard edges per shard (INV-E18) |
| `CROSS_SHARD_BONUS` | 0.2 | Bonus weight for cross-shard edges (PA-4) |

When a shard exceeds MAX_QUANTA_PER_SHARD, it is split. The split algorithm:
1. Compute graph partition (e.g., METIS) minimising cross-partition edges.
2. Create two new shards from the partition.
3. Reclassify edges (intra vs cross) for both new shards.
4. Update the border graph.

#### 7.2.3  Cross-Shard Bonus

```python
CROSS_SHARD_BONUS = 0.2

def compute_cross_shard_bonus(
    source_shard: int,
    target_shard: int
) -> float:
    """Cross-shard edges receive a bonus to incentivise global coherence.

    Returns 0.2 for cross-shard edges, 0.0 for same-shard.
    """
    if source_shard != target_shard:
        return CROSS_SHARD_BONUS
    return 0.0
```

#### 7.2.4  Claim Family Graph

The claim family graph is a materialized overlay grouping quanta that express the same proposition lineage across revisions, decompositions, evidence extensions, and supersession. The coherence graph remains the source of truth for graph edges; the family graph is derived from `DERIVATION` and `SUPERSESSION` edges plus lineage references supplied by PCVM. Each `CoherenceEngine` instance maintains a `ClaimFamilyIndex` alongside shard state.

```python
@dataclass
class ClaimFamilyMembership:
    quantum_id: UUID
    family_id: UUID
    root_quantum_id: UUID
    parent_ids: Set[UUID]
    relation: str  # ROOT, REVISION, DECOMPOSITION, EVIDENCE_EXTENSION, CONSOLIDATION_OUTPUT
    frontier: bool

@dataclass
class ClaimFamilyIndex:
    memberships: Dict[UUID, ClaimFamilyMembership]
    families: Dict[UUID, Set[UUID]]
    frontier: Dict[UUID, Set[UUID]]          # family_id -> active family boundary
    upstream_families: Dict[UUID, Set[UUID]] # consolidation family -> source families
```

Membership rules:

1. A newly ingested quantum without validated lineage parents starts a new family and becomes its root.
2. A revision, decomposition child, or evidence-extension quantum joins the parent family.
3. A K-class consolidation output starts a new family; source family IDs are recorded in `upstream_families` rather than merging distinct families.
4. A `SUPERSESSION` edge sets `frontier = False` on superseded members and promotes the replacement to the family frontier.
5. Family membership is shard-agnostic; shard splits and moves MUST preserve `family_id`, parent links, and frontier state.

Family-scoped operations are used for re-evaluating descendants after supersession or contradiction, retrieving all current revisions of a proposition, and preventing family-internal reinforcement from masquerading as independent evidence in downstream credibility propagation.

#### 7.2.5  Heuristic Family Store

The claim family graph tracks proposition lineage. H-class quanta need an additional storage discipline because multiple heuristic variants may address the same operational problem without being revisions of a single proposition. EMA therefore maintains a heuristic family store for H-class quanta only. It is a materialized overlay, not a second truth store: coherence edges and claim-family lineage remain authoritative, while the heuristic family store indexes versioning, alternative variants, and retirement state for pragmatic recommendations.

```python
class HeuristicFamilyStatus(Enum):
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"

@dataclass
class HeuristicFamilyMembership:
    quantum_id: UUID
    heuristic_family_id: UUID
    version: int
    relation: str          # ROOT, REVISION, SPECIALIZATION, ALTERNATIVE
    context_tags: Set[str]
    frontier: bool
    retired: bool

@dataclass
class HeuristicFamilyRecord:
    heuristic_family_id: UUID
    canonical_problem: str
    evaluation_axes: Tuple[str, ...]
    status: HeuristicFamilyStatus
    root_quantum_id: UUID
    frontier_ids: Set[UUID]
    deprecated_ids: Set[UUID]
    retired_epoch: Optional[int]
    retirement_reason: Optional[str]

@dataclass
class HeuristicFamilyStore:
    memberships: Dict[UUID, HeuristicFamilyMembership]
    families: Dict[UUID, HeuristicFamilyRecord]
    by_problem: Dict[str, Set[UUID]]
```

Membership and lifecycle rules:

1. Only H-class quanta may enter the heuristic family store.
2. A newly admitted H-class quantum without an accepted family reference starts a new heuristic family and becomes version 1.
3. An H-class revision or specialization joins the existing family and increments the family version counter.
4. Multiple frontier members are permitted only when their `context_tags` are disjoint and the family has no more than `HEURISTIC_FAMILY_FRONTIER_MAX` simultaneous frontiers.
5. A superseded heuristic remains queryable for audit but is marked `DEPRECATED` and removed from the frontier.
6. A family transitions from `DEPRECATED` to `RETIRED` when no frontier member remains above the H-class admission threshold for `HEURISTIC_FAMILY_RETIREMENT_MIN_EPOCHS`, or when a G-class governance directive explicitly retires the family.
7. RETIRED families remain reconstructable from archive and bundle storage, but default retrieval excludes them unless the caller explicitly opts in.

Heuristic families are the unit of pragmatic versioning and retirement. Claim-family lineage answers "which proposition version produced this quantum?" The heuristic family store answers "which recommendation family does this heuristic belong to, what is the current frontier, and when is the family retired?"

### 7.3  Edge Dynamics and Tiered Updates

#### 7.3.1  Edge Tier Classification

Edges are classified into three access tiers based on recency:

| Tier | Criteria | Update Frequency |
|---|---|---|
| **HOT** | Accessed within last 1 TIDAL_EPOCH | Every epoch |
| **WARM** | Accessed within last 5 TIDAL_EPOCHs | Every 5 epochs |
| **COLD** | Not accessed in 5+ epochs | Every 10 epochs |

```python
HOT_THRESHOLD = 1     # epochs since last access
WARM_THRESHOLD = 5    # epochs since last access

def classify_edge_tier(edge: CoherenceEdge, current_epoch: int) -> str:
    """Classify edge into HOT/WARM/COLD tier (INV-E17)."""
    epochs_since_access = current_epoch - edge.last_accessed_epoch

    if epochs_since_access <= HOT_THRESHOLD:
        return "HOT"
    elif epochs_since_access <= WARM_THRESHOLD:
        return "WARM"
    else:
        return "COLD"


def reclassify_shard_edges(shard: CoherenceShard, current_epoch: int):
    """Reclassify all edges in a shard by tier."""
    for edge in shard.intra_edges.values():
        edge.tier = classify_edge_tier(edge, current_epoch)
    for edge in shard.cross_edges.values():
        edge.tier = classify_edge_tier(edge, current_epoch)
```

#### 7.3.2  Edge Weight Updates

```python
WEIGHT_DECAY_RATE = 0.01  # per TIDAL_EPOCH for inactive edges
SUPPORT_REINFORCEMENT = 0.05  # on access

def update_edge_weight(edge: CoherenceEdge, current_epoch: int,
                       accessed: bool = False) -> float:
    """Update edge weight based on access and decay."""
    if accessed:
        edge.last_accessed_epoch = current_epoch
        edge.access_count += 1
        # Reinforce on access
        edge.weight = min(1.0, edge.weight + SUPPORT_REINFORCEMENT)
    else:
        # Decay inactive edges
        epochs_inactive = current_epoch - edge.last_updated_epoch
        decay = WEIGHT_DECAY_RATE * epochs_inactive
        edge.weight = max(0.01, edge.weight - decay)

    edge.last_updated_epoch = current_epoch
    return edge.weight
```

#### 7.3.3  Tiered Epoch Update

```python
COHERENCE_COMPUTATION_BUDGET_SECONDS = 1800  # 30 minutes (50% of TIDAL_EPOCH)

def epoch_coherence_update(engine: CoherenceEngine, current_epoch: int):
    """Execute tiered coherence update for one TIDAL_EPOCH.

    HOT edges: updated every epoch.
    WARM edges: updated every 5 epochs.
    COLD edges: updated every 10 epochs.

    Total computation bounded to COHERENCE_COMPUTATION_BUDGET_SECONDS.
    """
    start_time = time.time()

    for shard in engine.shards.values():
        # Reclassify tiers
        reclassify_shard_edges(shard, current_epoch)

        # HOT edges â€” always processed
        hot_edges = [e for e in shard.intra_edges.values() if e.tier == "HOT"]
        for edge in hot_edges:
            if time.time() - start_time > COHERENCE_COMPUTATION_BUDGET_SECONDS:
                log_warning("Coherence computation budget exceeded")
                return
            update_edge_weight(edge, current_epoch)

        # WARM edges â€” every 5 epochs
        if current_epoch % 5 == 0:
            warm_edges = [e for e in shard.intra_edges.values() if e.tier == "WARM"]
            for edge in warm_edges:
                if time.time() - start_time > COHERENCE_COMPUTATION_BUDGET_SECONDS:
                    return
                update_edge_weight(edge, current_epoch)

        # COLD edges â€” every 10 epochs
        if current_epoch % 10 == 0:
            cold_edges = [e for e in shard.intra_edges.values() if e.tier == "COLD"]
            for edge in cold_edges:
                if time.time() - start_time > COHERENCE_COMPUTATION_BUDGET_SECONDS:
                    return
                update_edge_weight(edge, current_epoch)

    # Update border graph
    update_border_graph(engine, current_epoch)

    # Enforce per-shard edge budgets
    for shard in engine.shards.values():
        enforce_shard_edge_budget(shard)


def update_border_graph(engine: CoherenceEngine, current_epoch: int):
    """Rebuild border graph from all shards' cross-edges (INV-E19)."""
    engine.border_graph = BorderGraph(edges={}, shard_connectivity={})

    for shard in engine.shards.values():
        for edge in shard.cross_edges.values():
            target_shard_id = engine.get_shard_for_quantum(edge.target_id)
            pair = (min(shard.shard_id, target_shard_id),
                    max(shard.shard_id, target_shard_id))

            if pair not in engine.border_graph.edges:
                engine.border_graph.edges[pair] = []
            engine.border_graph.edges[pair].append(edge)

            # Update connectivity
            engine.border_graph.shard_connectivity.setdefault(
                shard.shard_id, set()).add(target_shard_id)
            engine.border_graph.shard_connectivity.setdefault(
                target_shard_id, set()).add(shard.shard_id)
```

### 7.4  Edge Budget Enforcement

Each shard maintains edge budgets (INV-E18):

```python
def enforce_shard_edge_budget(shard: CoherenceShard):
    """Enforce per-shard edge limits by pruning lowest-rank edges."""
    # Intra-edge budget
    if shard.intra_edge_count > MAX_INTRA_EDGES_PER_SHARD:
        excess = shard.intra_edge_count - MAX_INTRA_EDGES_PER_SHARD
        ranked = sorted(shard.intra_edges.values(), key=compute_edge_rank)
        for edge in ranked[:excess]:
            del shard.intra_edges[(edge.source_id, edge.target_id)]

    # Cross-edge budget
    if shard.cross_edge_count > MAX_CROSS_EDGES_PER_SHARD:
        excess = shard.cross_edge_count - MAX_CROSS_EDGES_PER_SHARD
        ranked = sorted(shard.cross_edges.values(), key=compute_edge_rank)
        for edge in ranked[:excess]:
            del shard.cross_edges[(edge.source_id, edge.target_id)]


def compute_edge_rank(edge: CoherenceEdge) -> float:
    """Compute edge rank for budget enforcement (lower = more pruneable).

    Rank considers: weight, access recency, tier, edge type.
    CONTRADICTION edges receive a bonus (less pruneable).
    """
    type_bonus = 0.3 if edge.edge_type == EdgeType.CONTRADICTION else 0.0
    tier_bonus = {"HOT": 0.5, "WARM": 0.2, "COLD": 0.0}[edge.tier]
    cross_bonus = CROSS_SHARD_BONUS if edge.source_id != edge.target_id else 0.0

    return edge.weight + tier_bonus + type_bonus + cross_bonus
```

### 7.5  Scale Tiers

EMA defines four scale tiers with tier-appropriate strategies:

| Tier | Quantum Count | Shard Count | Strategy |
|---|---|---|---|
| **T1** | < 10 000 | 1 | No sharding; full coherence update every epoch |
| **T2** | 10 000 â€“ 1 000 000 | 1 â€“ 10 | Basic sharding; tiered updates |
| **T3** | 1M â€“ 1B | 10 â€“ 1 000 | Full sharding; border graph; computation budgeting |
| **T4** | > 1B | 1 000+ | Probabilistic edge sampling (20% per epoch); distributed border graph |

```python
def determine_scale_tier(total_quanta: int) -> str:
    if total_quanta < 10_000:
        return "T1"
    elif total_quanta < 1_000_000:
        return "T2"
    elif total_quanta < 1_000_000_000:
        return "T3"
    else:
        return "T4"

T4_SAMPLING_RATE = 0.20  # 20% edge sampling per epoch at T4

def t4_probabilistic_update(shard: CoherenceShard, current_epoch: int):
    """At T4 scale, sample 20% of edges for update per epoch.

    This provides statistical coverage while bounding computation.
    Over 5 epochs, all edges are expected to be updated at least once.
    """
    all_edges = list(shard.intra_edges.values())
    sample_size = int(len(all_edges) * T4_SAMPLING_RATE)
    sampled = random.sample(all_edges, min(sample_size, len(all_edges)))

    for edge in sampled:
        update_edge_weight(edge, current_epoch)
```

### 7.6  Contradiction Lattice

The Contradiction Lattice is the canonical data structure for tracking, ordering, and resolving contradictions within the coherence graph. It replaces the ad-hoc detection described in earlier versions with a formal partially ordered set of contradiction records that supports subsumption-aware resolution, temporal tracking, and INV-E7 enforcement.

#### 7.6.1  Motivation

Contradiction edges (Section 4.5) record pairwise inconsistencies between quanta, but raw edges alone do not capture:

- **Contradiction clusters** â€” groups of contradictions with a common root cause.
- **Subsumption** â€” cases where resolving one contradiction automatically resolves others.
- **Resolution history** â€” what was done, by whom, and whether the outcome proved stable.
- **Monotonicity enforcement** â€” the INV-E7 guarantee that unresolved contradictions increase by at most 10% per TIDAL_EPOCH.

The Contradiction Lattice addresses all four gaps.

#### 7.6.2  Data Model

```python
from enum import Enum
from typing import Optional, Set, FrozenSet

class ContradictionState(Enum):
    DETECTED    = "DETECTED"      # Identified, awaiting arbitration
    ARBITRATING = "ARBITRATING"   # Arbitration in progress this epoch
    RESOLVED    = "RESOLVED"      # Resolved by belief revision
    DISSOLVED   = "DISSOLVED"     # One or both endpoints dissolved (catabolism)
    SUPERSEDED  = "SUPERSEDED"    # Subsumed by a higher-level resolution

@dataclass
class ContradictionRecord:
    """A tracked contradiction in the lattice."""
    contradiction_id: UUID
    edge_key: Tuple[UUID, UUID]       # The CONTRADICTION edge (source, target)
    detected_epoch: int
    state: ContradictionState
    resolution_epoch: Optional[int]

    # Belief state at detection
    source_belief_at_detection: float   # source quantum b at detection time
    target_belief_at_detection: float   # target quantum b at detection time
    edge_weight_at_detection: float     # CONTRADICTION edge weight at detection

    # Subsumption links (lattice ordering)
    parent_id: Optional[UUID]           # Contradiction that subsumes this one
    child_ids: Set[UUID]                # Contradictions subsumed by this one

    # Resolution outcome
    resolution_method: Optional[str]    # "ARBITRATION", "DISSOLUTION", "SUPERSESSION"
    loser_quantum_id: Optional[UUID]    # Which quantum lost belief
    belief_delta: Optional[float]       # How much belief was transferred

    # Provenance
    creating_agent: Optional[AgentID]   # Agent that created the contradiction edge
    arbitrating_agent: Optional[AgentID]  # Agent or process that arbitrated

@dataclass
class ContradictionLattice:
    """Partially ordered set of contradiction records.

    The ordering is by subsumption: contradiction A >= B iff resolving
    A automatically resolves B. This forms a lattice because:
    - The meet (greatest lower bound) of two contradictions is their
      deepest shared root contradiction.
    - The join (least upper bound) is the shallowest contradiction
      that subsumes both.
    - The bottom element is the empty contradiction (trivially subsumed
      by all).
    """
    records: Dict[UUID, ContradictionRecord]
    roots: Set[UUID]                    # Records with parent_id = None

    # Per-epoch counters for INV-E7 enforcement
    epoch_detected: Dict[int, int]      # epoch -> count detected that epoch
    epoch_resolved: Dict[int, int]      # epoch -> count resolved that epoch

    @property
    def unresolved_count(self) -> int:
        return sum(1 for r in self.records.values()
                   if r.state in (ContradictionState.DETECTED,
                                  ContradictionState.ARBITRATING))

    @property
    def total_count(self) -> int:
        return len(self.records)

    def sigma_h(self) -> float:
        """Compute coherence stress signal for SHREC (Section 6.2).

        Ïƒ_H = unresolved contradictions / total contradiction edges.
        Returns 0.0 when no contradictions exist.
        """
        if self.total_count == 0:
            return 0.0
        return self.unresolved_count / self.total_count
```

Each coherence shard (Section 7.2) maintains its own ContradictionLattice instance. Cross-shard contradictions are registered in both endpoint shards' lattices with identical `contradiction_id` values.

#### 7.6.3  Detection Protocol

Contradiction detection runs during the circulation consistency check (Section 5.2.1, step 4) and during ingestion of new quanta:

```python
CONTRADICTION_ACTIVATION_BELIEF = 0.7    # Both endpoints must exceed
CONTRADICTION_ACTIVATION_WEIGHT = 0.3    # Edge weight must exceed

def detect_contradictions(
    shard: CoherenceShard,
    lattice: ContradictionLattice,
    current_epoch: int
) -> List[ContradictionRecord]:
    """Scan for newly activated contradictions.

    A contradiction is 'activated' when both endpoints have belief > 0.7
    and the CONTRADICTION edge weight > 0.3. Previously detected
    contradictions are not re-detected.
    """
    new_records = []
    existing_edge_keys = {r.edge_key for r in lattice.records.values()}

    for edge in shard.intra_edges.values():
        if edge.edge_type != EdgeType.CONTRADICTION:
            continue
        if (edge.source_id, edge.target_id) in existing_edge_keys:
            continue

        source_q = shard.quanta[edge.source_id]
        target_q = shard.quanta[edge.target_id]

        if (source_q.opinion.b > CONTRADICTION_ACTIVATION_BELIEF and
            target_q.opinion.b > CONTRADICTION_ACTIVATION_BELIEF and
            edge.weight > CONTRADICTION_ACTIVATION_WEIGHT):

            record = ContradictionRecord(
                contradiction_id=uuid4(),
                edge_key=(edge.source_id, edge.target_id),
                detected_epoch=current_epoch,
                state=ContradictionState.DETECTED,
                resolution_epoch=None,
                source_belief_at_detection=source_q.opinion.b,
                target_belief_at_detection=target_q.opinion.b,
                edge_weight_at_detection=edge.weight,
                parent_id=None,
                child_ids=set(),
                resolution_method=None,
                loser_quantum_id=None,
                belief_delta=None,
                creating_agent=edge.creating_agent,
                arbitrating_agent=None
            )
            lattice.records[record.contradiction_id] = record
            lattice.roots.add(record.contradiction_id)
            new_records.append(record)

    # Update epoch counter
    lattice.epoch_detected.setdefault(current_epoch, 0)
    lattice.epoch_detected[current_epoch] += len(new_records)

    return new_records
```

#### 7.6.4  Subsumption and Lattice Ordering

Two contradictions are related by subsumption when resolving one implies resolution of the other. Subsumption is detected by examining the derivation graph:

```python
def check_subsumption(
    parent_record: ContradictionRecord,
    child_record: ContradictionRecord,
    shard: CoherenceShard
) -> bool:
    """Contradiction P subsumes contradiction C if:

    1. One endpoint of C is derived (DERIVATION edge) from an endpoint
       of P, AND the derivation weight > 0.5; OR
    2. Both endpoints of C are within derivation distance 2 of the
       endpoints of P (shared root cause).

    Subsumption is transitive: if P >= C and C >= D, then P >= D.
    """
    p_nodes = set(parent_record.edge_key)
    c_nodes = set(child_record.edge_key)

    # Check direct derivation
    for c_node in c_nodes:
        for p_node in p_nodes:
            edge = shard.intra_edges.get((p_node, c_node))
            if (edge and edge.edge_type == EdgeType.DERIVATION
                    and edge.weight > 0.5):
                return True

    # Check shared root within distance 2
    p_ancestors = _get_derivation_ancestors(p_nodes, shard, max_depth=2)
    c_ancestors = _get_derivation_ancestors(c_nodes, shard, max_depth=2)
    if p_ancestors & c_ancestors:
        return True

    return False


def update_lattice_ordering(
    lattice: ContradictionLattice,
    new_record: ContradictionRecord,
    shard: CoherenceShard
):
    """Insert a new contradiction into the lattice ordering."""
    for existing_id, existing_record in lattice.records.items():
        if existing_id == new_record.contradiction_id:
            continue
        if existing_record.state in (ContradictionState.DISSOLVED,
                                      ContradictionState.SUPERSEDED):
            continue

        if check_subsumption(existing_record, new_record, shard):
            # Existing subsumes new â€” new becomes child of existing
            new_record.parent_id = existing_id
            existing_record.child_ids.add(new_record.contradiction_id)
            lattice.roots.discard(new_record.contradiction_id)
            return

        if check_subsumption(new_record, existing_record, shard):
            # New subsumes existing â€” existing becomes child of new
            existing_record.parent_id = new_record.contradiction_id
            new_record.child_ids.add(existing_id)
            lattice.roots.discard(existing_id)
```

#### 7.6.5  Resolution Protocol

Resolution proceeds in three phases: arbitration, propagation, and cascading subsumption resolution.

**Phase 1 â€” Arbitration.** The quantum with weaker coherence support loses belief.

```python
def arbitrate_contradiction(
    record: ContradictionRecord,
    shard: CoherenceShard,
    current_epoch: int
) -> ContradictionRecord:
    """Arbitrate a contradiction by comparing coherence support.

    The quantum with fewer weighted SUPPORT edges loses belief.
    The loser's belief is reduced by the contradiction edge weight,
    and the surplus is transferred to uncertainty.
    """
    record.state = ContradictionState.ARBITRATING

    source_q = shard.quanta[record.edge_key[0]]
    target_q = shard.quanta[record.edge_key[1]]

    source_support = _weighted_support(source_q, shard)
    target_support = _weighted_support(target_q, shard)

    if source_support >= target_support:
        loser, winner = target_q, source_q
    else:
        loser, winner = source_q, target_q

    # Reduce loser's belief by the contradiction edge weight
    edge = shard.intra_edges[(record.edge_key[0], record.edge_key[1])]
    delta = min(loser.opinion.b, edge.weight)
    loser.opinion.b -= delta
    loser.opinion.u += delta
    loser.opinion = normalize(loser.opinion)

    record.loser_quantum_id = loser.id
    record.belief_delta = delta
    record.resolution_method = "ARBITRATION"
    record.state = ContradictionState.RESOLVED
    record.resolution_epoch = current_epoch
    record.arbitrating_agent = None  # System process

    return record


def _weighted_support(quantum: EpistemicQuantum,
                      shard: CoherenceShard) -> float:
    """Sum of weight * source.opinion.b for all SUPPORT edges
    pointing to this quantum."""
    total = 0.0
    for edge in shard.intra_edges.values():
        if (edge.target_id == quantum.id and
                edge.edge_type == EdgeType.SUPPORT):
            source = shard.quanta.get(edge.source_id)
            if source:
                total += edge.weight * source.opinion.b
    return total
```

**Phase 2 â€” Propagation.** Belief changes from arbitration propagate along DERIVATION edges with exponential distance decay.

```python
PROPAGATION_DECAY_FACTOR = 0.5    # Per hop
MAX_PROPAGATION_DEPTH = 3

def propagate_belief_change(
    origin_quantum: EpistemicQuantum,
    delta: float,
    shard: CoherenceShard,
    depth: int = 0
):
    """Propagate a belief reduction along DERIVATION edges."""
    if depth >= MAX_PROPAGATION_DEPTH or abs(delta) < 0.01:
        return

    decayed_delta = delta * PROPAGATION_DECAY_FACTOR
    for edge in shard.intra_edges.values():
        if (edge.source_id == origin_quantum.id and
                edge.edge_type == EdgeType.DERIVATION):
            child = shard.quanta.get(edge.target_id)
            if child:
                child_delta = min(child.opinion.b, decayed_delta * edge.weight)
                child.opinion.b -= child_delta
                child.opinion.u += child_delta
                child.opinion = normalize(child.opinion)
                propagate_belief_change(child, child_delta, shard, depth + 1)
```

**Phase 3 â€” Cascading subsumption resolution.** When a root contradiction is resolved, its subsumed children are resolved automatically.

```python
def cascade_resolution(
    lattice: ContradictionLattice,
    resolved_record: ContradictionRecord,
    current_epoch: int
):
    """Resolve all contradictions subsumed by a resolved parent."""
    for child_id in resolved_record.child_ids:
        child = lattice.records.get(child_id)
        if child and child.state == ContradictionState.DETECTED:
            child.state = ContradictionState.SUPERSEDED
            child.resolution_epoch = current_epoch
            child.resolution_method = "SUPERSESSION"
            # Recurse into grandchildren
            cascade_resolution(lattice, child, current_epoch)
```

#### 7.6.6  INV-E7 Monotonicity Enforcement

INV-E7 requires that unresolved contradictions increase by at most 10% per TIDAL_EPOCH. The lattice enforces this bound:

```python
def enforce_inv_e7(
    lattice: ContradictionLattice,
    current_epoch: int
) -> bool:
    """Check and enforce INV-E7.

    If the unresolved count would exceed the 10% growth bound, the
    oldest unresolved contradictions are force-arbitrated in age order
    until the bound is satisfied.

    Returns True if enforcement was needed.
    """
    prev_epoch = current_epoch - 1
    prev_unresolved = sum(
        1 for r in lattice.records.values()
        if r.state in (ContradictionState.DETECTED,
                       ContradictionState.ARBITRATING)
        and r.detected_epoch < current_epoch
    )
    current_unresolved = lattice.unresolved_count
    max_allowed = int(prev_unresolved * 1.10) + 1  # +1 for rounding

    if current_unresolved <= max_allowed:
        return False

    # Force-arbitrate oldest unresolved contradictions
    excess = current_unresolved - max_allowed
    unresolved = sorted(
        (r for r in lattice.records.values()
         if r.state == ContradictionState.DETECTED),
        key=lambda r: r.detected_epoch
    )
    # Note: actual arbitration requires shard context;
    # caller must provide shard reference
    return True  # Signal that force-arbitration is required
```

#### 7.6.7  SHREC Integration

The SHREC coherence stress signal Ïƒ_H (Section 6.2) is computed directly from the lattice via `ContradictionLattice.sigma_h()`. The signal feeds into the SHREC graduated controller (Section 6.7) to influence metabolic budget allocation. High Ïƒ_H (many unresolved contradictions relative to total) biases the budget toward circulation and catabolism to accelerate resolution.

#### 7.6.8  Cross-Layer Integration

- **C5 PCVM (Section 10.3):** When C5 admits a new claim that contradicts an existing quantum (semantic similarity > 0.7, semantic contradiction > 0.8), C5 emits a contradiction notification. EMA's ingestion pipeline (Section 5.1) creates the CONTRADICTION edge, and the lattice detection protocol (Section 7.6.3) registers the activated record.
- **C35 Sentinel Graph:** Contradiction resolution events (arbitration or dissolution of quanta with b > 0.8) are emitted as anomaly signals to C35's verification channel. Sudden spikes in contradiction detection rate trigger elevated Ïƒ_H, which in turn triggers SHREC regime escalation and Sentinel alerting.
- **Catabolism (Section 5.4):** When catabolism dissolves a quantum that is an endpoint of an active contradiction, the lattice transitions the record to DISSOLVED state. No arbitration is needed â€” the contradiction is removed by dissolution.

### 7.7  Bridge Detection

Bridge edges â€” those whose removal would disconnect significant graph components â€” receive special protection:

```python
def detect_bridge_edges(shard: CoherenceShard) -> Set[Tuple[UUID, UUID]]:
    """Identify bridge edges within a shard using Tarjan's algorithm.

    Bridge edges are never pruned during budget enforcement.
    """
    # ... Tarjan's bridge-finding algorithm ...
    pass
```

Bridge edges are exempted from budget pruning and receive a rank bonus in `compute_edge_rank()`.

---

## 8  Projection Engine

### 8.1  Overview

The projection engine provides lossy but bounded-error views of epistemic quanta to peer Atrahasis subsystems. Each projection type is tailored to the consuming subsystem's needs.

### 8.2  Projection Types

| Target | Format | Fidelity Range | Key Transformation |
|---|---|---|---|
| **C3 (Tidal Noosphere)** | Simplified opinion + topic vector | 0.55 â€“ 0.75 | Collapse edge structure to topic relevance score |
| **C4 (ASV Communication)** | Natural-language summary + confidence | 0.82 â€“ 0.90 | Generate human-readable summary from structured claim |
| **C5 (Sentinel Graph)** | Node attributes + trust score | 0.90 â€“ 0.97 | Map opinion to scalar trust, preserve provenance links |

### 8.3  Reconstruction Functions

Reconstruction functions measure round-trip fidelity (INV-E9):

```python
@dataclass
class ReconstructionResult:
    original_quantum_id: UUID
    reconstructed_opinion: Opinion
    fidelity_score: float  # [0, 1]
    reconstruction_method: str
    loss_vector: Dict[str, float]  # per-field loss

def reconstruct_from_c3(
    projection: C3Projection,
    original: EpistemicQuantum
) -> ReconstructionResult:
    """Reconstruct quantum from C3 (Tidal Noosphere) projection.

    C3 projections lose edge structure and fine-grained provenance.
    Expected fidelity: 0.55-0.75.
    """
    # Reconstruct opinion from topic relevance score
    topic_score = projection.topic_relevance
    reconstructed_b = topic_score * 0.7  # approximate
    reconstructed_u = 1.0 - topic_score
    reconstructed_d = max(0.0, 1.0 - reconstructed_b - reconstructed_u)
    reconstructed_opinion = Opinion(
        b=reconstructed_b, d=reconstructed_d,
        u=reconstructed_u, a=original.opinion.a
    )

    fidelity = measure_round_trip_fidelity(original.opinion, reconstructed_opinion)

    return ReconstructionResult(
        original_quantum_id=original.id,
        reconstructed_opinion=reconstructed_opinion,
        fidelity_score=fidelity,
        reconstruction_method="c3_topic_inversion",
        loss_vector={
            "opinion": 1.0 - fidelity,
            "edges": 1.0,  # fully lost in C3 projection
            "provenance": 0.7  # mostly lost
        }
    )


def reconstruct_from_c4(
    projection: C4Projection,
    original: EpistemicQuantum
) -> ReconstructionResult:
    """Reconstruct from C4 (ASV) projection.

    C4 projections retain confidence and claim structure.
    Expected fidelity: 0.82-0.90.
    """
    confidence = projection.confidence
    reconstructed_b = confidence
    reconstructed_u = max(0.0, 1.0 - confidence * 1.1)
    reconstructed_d = max(0.0, 1.0 - reconstructed_b - reconstructed_u)
    reconstructed_opinion = Opinion(
        b=reconstructed_b, d=reconstructed_d,
        u=reconstructed_u, a=original.opinion.a
    )

    fidelity = measure_round_trip_fidelity(original.opinion, reconstructed_opinion)

    return ReconstructionResult(
        original_quantum_id=original.id,
        reconstructed_opinion=reconstructed_opinion,
        fidelity_score=fidelity,
        reconstruction_method="c4_confidence_inversion",
        loss_vector={
            "opinion": 1.0 - fidelity,
            "edges": 0.5,
            "provenance": 0.3
        }
    )


def reconstruct_from_c5(
    projection: C5Projection,
    original: EpistemicQuantum
) -> ReconstructionResult:
    """Reconstruct from C5 (Sentinel Graph) projection.

    C5 projections retain trust score and provenance links.
    Expected fidelity: 0.90-0.97.
    """
    trust = projection.trust_score
    reconstructed_b = trust
    reconstructed_d = max(0.0, (1.0 - trust) * 0.3)
    reconstructed_u = max(0.0, 1.0 - reconstructed_b - reconstructed_d)
    reconstructed_opinion = Opinion(
        b=reconstructed_b, d=reconstructed_d,
        u=reconstructed_u, a=original.opinion.a
    )

    fidelity = measure_round_trip_fidelity(original.opinion, reconstructed_opinion)

    return ReconstructionResult(
        original_quantum_id=original.id,
        reconstructed_opinion=reconstructed_opinion,
        fidelity_score=fidelity,
        reconstruction_method="c5_trust_inversion",
        loss_vector={
            "opinion": 1.0 - fidelity,
            "edges": 0.2,
            "provenance": 0.05
        }
    )


def measure_round_trip_fidelity(original: Opinion, reconstructed: Opinion) -> float:
    """Measure fidelity of round-trip projection-reconstruction.

    Uses cosine similarity on the (b, d, u) vector.
    """
    orig_vec = [original.b, original.d, original.u]
    recon_vec = [reconstructed.b, reconstructed.d, reconstructed.u]

    dot = sum(a * b for a, b in zip(orig_vec, recon_vec))
    mag_orig = math.sqrt(sum(a ** 2 for a in orig_vec))
    mag_recon = math.sqrt(sum(a ** 2 for a in recon_vec))

    if mag_orig < 1e-9 or mag_recon < 1e-9:
        return 0.0

    return dot / (mag_orig * mag_recon)
```

### 8.4  Fidelity Monitoring

Fidelity is monitored continuously. If measured fidelity drops below the minimum for a projection type, an alert is raised and the projection is flagged for recalibration:

```python
FIDELITY_MINIMUMS = {"C3": 0.50, "C4": 0.75, "C5": 0.85}

def monitor_fidelity(projection_type: str, fidelity: float):
    minimum = FIDELITY_MINIMUMS[projection_type]
    if fidelity < minimum:
        raise FidelityAlert(
            f"{projection_type} fidelity {fidelity:.3f} below minimum {minimum}"
        )
```

---

## 9  Retrieval

### 9.1  Query Interface

EMA exposes a retrieval interface for active quanta:

```python
@dataclass
class RetrievalQuery:
    topic: Optional[str]
    claim_class: Optional[str]
    family_id: Optional[UUID]
    heuristic_family_id: Optional[UUID]
    min_belief: Optional[float]
    min_vitality: Optional[float]
    max_results: int = 100
    semantic_top_k: int = 256
    similarity_floor: float = 0.35
    include_dormant: bool = False
    include_retired_heuristics: bool = False

def retrieve(query: RetrievalQuery) -> List[RetrievalResult]:
    """Retrieve quanta matching query criteria.

    Topic-bearing retrieval uses the semantic index for candidate generation,
    then ranks results by relevance * vitality * opinion_strength.
    QUARANTINED and DISSOLVED quanta are never returned.
    """
    if query.topic:
        candidate_ids = coherence_engine.semantic_index.lookup(
            text=query.topic,
            top_k=query.semantic_top_k,
            claim_class=query.claim_class,
            family_id=query.family_id,
            heuristic_family_id=query.heuristic_family_id,
            similarity_floor=query.similarity_floor,
            include_dormant=query.include_dormant,
            include_retired_heuristics=query.include_retired_heuristics
        )
    else:
        candidate_ids = coherence_engine.iter_active_quantum_ids(
            include_dormant=query.include_dormant
        )

    candidates = []

    for quantum_id in candidate_ids:
        quantum = coherence_engine.get_quantum(quantum_id)
        if quantum.metabolic_state in (MetabolicState.QUARANTINED,
                                       MetabolicState.DISSOLVED):
            continue
        if quantum.metabolic_state == MetabolicState.DORMANT and not query.include_dormant:
            continue

        if query.claim_class and quantum.claim_class != query.claim_class:
            continue
        if query.family_id:
            membership = coherence_engine.claim_family_index.memberships.get(quantum.id)
            if not membership or membership.family_id != query.family_id:
                continue
        heuristic_membership = coherence_engine.heuristic_family_store.memberships.get(quantum.id)
        if query.heuristic_family_id:
            if (not heuristic_membership or
                heuristic_membership.heuristic_family_id != query.heuristic_family_id):
                continue
        if heuristic_membership:
            heuristic_family = coherence_engine.heuristic_family_store.families[
                heuristic_membership.heuristic_family_id
            ]
            if (heuristic_family.status == HeuristicFamilyStatus.RETIRED and
                not query.include_retired_heuristics):
                continue
        if query.min_belief and quantum.opinion.b < query.min_belief:
            continue

        vitality = compute_vitality(quantum, current_epoch)
        if query.min_vitality and vitality < query.min_vitality:
            continue

        relevance = compute_topic_relevance(quantum, query.topic) if query.topic else 1.0
        score = relevance * vitality * quantum.opinion.projected_probability

        candidates.append(RetrievalResult(quantum=quantum, score=score))

        # Update access tracking
        quantum.timestamps.last_accessed_epoch = current_epoch

    candidates.sort(key=lambda r: r.score, reverse=True)
    return candidates[:query.max_results]
```

### 9.2  Semantic Index

EMA uses a shard-aware semantic index as the candidate-generation layer for knowledge discovery. The coherence graph remains authoritative for quanta and edges; the semantic index is a retrieval accelerator built from normalized quantum content and refreshed whenever quantum state changes.

Each indexed quantum contributes a semantic fingerprint derived from:

1. Canonical structured claim content after C4-normalized field ordering.
2. Claim-class and credibility-rung markers.
3. Provenance-root summaries and claim-family / heuristic-family metadata when present.
4. Local coherence neighborhood summaries (support, contradiction, derivation, and supersession context).

Only ACTIVE quanta are indexed by default. DORMANT quanta MAY remain indexed for recall continuity but MUST be marked as dormant and filtered unless the caller explicitly opts in. RETIRED heuristic families MAY remain indexed for historical search but MUST be marked retired and filtered unless the caller explicitly opts in. QUARANTINED and DISSOLVED quanta MUST be removed from the semantic index within one refresh interval.

```python
SEMANTIC_INDEX_DIMENSIONS = 768
SEMANTIC_INDEX_PROBE_COUNT = 16
SEMANTIC_INDEX_CANDIDATE_MULTIPLIER = 4
SEMANTIC_INDEX_REFRESH_EPOCHS = 1

@dataclass
class SemanticIndexEntry:
    quantum_id: UUID
    shard_id: int
    embedding: Vector[float]
    claim_class: str
    family_id: Optional[UUID]
    heuristic_family_id: Optional[UUID]
    heuristic_family_status: Optional[str]
    metabolic_state: str
    last_indexed_epoch: int

@dataclass
class SemanticIndex:
    shard_indexes: Dict[int, ApproximateNearestNeighbor]
    entries: Dict[UUID, SemanticIndexEntry]

    def lookup(self, text: str, top_k: int,
               claim_class: Optional[str] = None,
               family_id: Optional[UUID] = None,
               heuristic_family_id: Optional[UUID] = None,
               similarity_floor: float = 0.35,
               include_dormant: bool = False,
               include_retired_heuristics: bool = False) -> List[UUID]:
        query_vec = embed_semantic_query(normalize_query(text))
        per_shard_k = max(
            8,
            math.ceil((top_k * SEMANTIC_INDEX_CANDIDATE_MULTIPLIER) /
                      len(self.shard_indexes))
        )
        merged = []

        for shard_id, ann in self.shard_indexes.items():
            for quantum_id, sim in ann.search(
                query_vec,
                k=per_shard_k,
                probes=SEMANTIC_INDEX_PROBE_COUNT
            ):
                entry = self.entries[quantum_id]
                if sim < similarity_floor:
                    continue
                if claim_class and entry.claim_class != claim_class:
                    continue
                if family_id and entry.family_id != family_id:
                    continue
                if heuristic_family_id and entry.heuristic_family_id != heuristic_family_id:
                    continue
                if entry.metabolic_state == "DORMANT" and not include_dormant:
                    continue
                if (entry.heuristic_family_status == "RETIRED" and
                    not include_retired_heuristics):
                    continue
                merged.append((quantum_id, sim))

        merged.sort(key=lambda item: item[1], reverse=True)
        return dedupe_keep_order([q for q, _ in merged[:top_k]])
```

Shard-local indexes are updated on ingestion, consolidation, supersession, contradiction-driven relabeling, and catabolic state changes. Query execution fans out to local ANN indexes, merges candidates globally, and hands the reduced set back to Section 9.1 for vitality- and opinion-aware reranking.

### 9.3  Provenance Retrieval

Full provenance chains can be retrieved for any quantum, including dissolved quanta (which retain provenance even after content removal). When a `family_id` is supplied, EMA SHOULD also return the family root, active frontier members, and any `upstream_families` references for consolidation-derived branches. When a `heuristic_family_id` is supplied, EMA SHOULD also return current frontier heuristics, deprecated members, and the family's retirement status.

---

## 10  Integration with Atrahasis Subsystems

### 10.1  PCVM Integration and Degraded Mode

The Proof Chain Verification Machine (PCVM) provides cryptographic verification of knowledge claims. EMA submits quanta for PCVM verification during ingestion and consolidation.

#### 10.1.1  PCVM Degraded Mode

When PCVM is unavailable, EMA operates in degraded mode:

```python
MAX_QUEUE_DEPTH_PER_LOCUS = 1000
PCVM_OUTAGE_DETECTION_EPOCHS = 3
PCVM_RECOVERY_DRAIN_RATE = 50  # verifications per SETTLEMENT_TICK

@dataclass
class PCVMDegradedMode:
    """PCVM degraded mode handler.

    Activated after PCVM_OUTAGE_DETECTION_EPOCHS consecutive
    failed verification attempts.
    """
    active: bool = False
    activation_epoch: Optional[int] = None
    ingestion_queue: Dict[str, List[EpistemicQuantum]] = field(default_factory=dict)
    total_queued: int = 0

    def detect_outage(self, consecutive_failures: int, current_epoch: int) -> bool:
        """Detect PCVM outage and activate degraded mode."""
        if consecutive_failures >= PCVM_OUTAGE_DETECTION_EPOCHS:
            if not self.active:
                self.active = True
                self.activation_epoch = current_epoch
                self.freeze_all_opinions()
                log_critical(f"PCVM degraded mode activated at epoch {current_epoch}")
            return True
        return False

    def queue_for_verification(self, quantum: EpistemicQuantum,
                                locus: str) -> bool:
        """Queue quantum for later verification.

        Returns False if queue is full for this locus.
        """
        if locus not in self.ingestion_queue:
            self.ingestion_queue[locus] = []

        if len(self.ingestion_queue[locus]) >= MAX_QUEUE_DEPTH_PER_LOCUS:
            return False  # reject â€” queue full

        self.ingestion_queue[locus].append(quantum)
        self.total_queued += 1
        quantum.opinion_frozen = True  # freeze opinion until verified
        return True

    def drain_queue(self, pcvm: PCVM) -> int:
        """Drain verification queue after PCVM recovery.

        Processes PCVM_RECOVERY_DRAIN_RATE items per SETTLEMENT_TICK.
        """
        processed = 0

        for locus in list(self.ingestion_queue.keys()):
            while (self.ingestion_queue[locus] and
                   processed < PCVM_RECOVERY_DRAIN_RATE):
                quantum = self.ingestion_queue[locus].pop(0)
                result = pcvm.verify(quantum)
                if result.verified:
                    quantum.opinion_frozen = False
                    quantum.metabolic_state = MetabolicState.ACTIVE
                else:
                    quantum.metabolic_state = MetabolicState.QUARANTINED
                processed += 1

            if not self.ingestion_queue[locus]:
                del self.ingestion_queue[locus]

        self.total_queued -= processed

        # Check if recovery complete
        if self.total_queued == 0:
            self.active = False
            self.activation_epoch = None
            self.unfreeze_all_opinions()
            log_info("PCVM degraded mode deactivated â€” queue drained")

        return processed

    def freeze_all_opinions(self):
        """Freeze all active quantum opinions during PCVM outage."""
        for quantum in knowledge_base.get_active_quanta():
            quantum.opinion_frozen = True

    def unfreeze_all_opinions(self):
        """Unfreeze opinions after PCVM recovery."""
        for quantum in knowledge_base.get_active_quanta():
            quantum.opinion_frozen = False
```

### 10.2  C3 Integration (Tidal Noosphere)

EMA provides topic-clustered knowledge to C3's deliberation pools via C3 projections (Section 8). C3 may request knowledge on specific topics, triggering retrieval and projection.

### 10.3  C4 Integration (ASV Communication)

EMA provides natural-language knowledge summaries to C4 for inter-agent communication. C4 projections include confidence scores derived from subjective-logic opinions.

### 10.4  C5 Integration (Sentinel Graph)

EMA provides trust-scored knowledge to C5's trust evaluation framework. C5 projections preserve provenance links, enabling C5 to trace trust chains.

### 10.5  Temporal Synchronisation

All EMA operations synchronise with the Atrahasis temporal hierarchy:
- **SETTLEMENT_TICK (60s):** Opinion updates, edge weight adjustments, retrieval access tracking.
- **TIDAL_EPOCH (3600s):** SHREC regulation, coherence graph tiered updates, catabolism evaluation, immune self-audit.
- **CONSOLIDATION_CYCLE (36000s):** Dreaming/consolidation pipeline execution.

---

## 11  Security Considerations

### 11.1  Threat Model

EMA's primary threats:

| Threat | Attack Surface | Mitigation |
|---|---|---|
| **Consolidation poisoning** | Crafted inputs designed to launder claims via dreaming | CRP+ 7-mechanism defense (Section 5.3.4), source independence verification (Section 5.3.3.1) |
| **Opinion manipulation** | Adversarial fusion inputs to shift belief | Source discounting, per-agent contradiction caps (Section 4.5.1) |
| **Coherence graph manipulation** | Adversarial edge creation to fragment/distort graph | Edge budget enforcement (Section 7.4), bridge detection (Section 7.7) |
| **Temporal coordination** | Timed submissions to exploit LV dynamics | VRF selection (Section 5.3.4.4), temporal clustering detection (I2) |
| **Source spoofing** | False provenance to bypass independence checks | W3C PROV verification, PCVM proof chains |
| **Regulatory evasion** | Crafted patterns to trigger/avoid SHREC regimes | Statistical self-model (Section 6.4), immune self-audit (Section 6.8) |

### 11.2  Defense Architecture

The defense architecture operates at three layers:

1. **Ingestion gate:** Source discounting, claim decomposition, PCVM verification.
2. **Consolidation hardening:** Source independence (C10), CRP+ mechanisms, adversarial probing, lineage tracking.
3. **Ongoing regulation:** SHREC four-regime controller, coherence graph maintenance, catabolism.

### 11.3  Constitutional Parameters

The following parameters are protected by G-class governance requirements (INV-CRP8):

- `STABILITY_THRESHOLD`, `EXPECTED_DISSENT_LEVEL`, `VRF_SELECTION_RATE`
- `ACCEPT_THRESHOLD`, `QUARANTINE_THRESHOLD`
- `PROMOTION_OBSERVATION_WINDOW`
- All credibility ladder rung thresholds
- `MAX_CASCADE_DEPTH`, `CASCADE_REDUCTION_FACTOR`

Modification of these parameters requires a G-class governance proposal, review, and approval.

---

## 12  Scalability and Deployment

### 12.1  Scale Tier Strategies

See Section 7.5 for the four scale tiers (T1â€“T4). Key scalability properties:

- **Horizontal sharding:** Each shard is independently processable, enabling parallel coherence updates.
- **Tiered computation:** HOT/WARM/COLD edge classification reduces per-epoch work.
- **Border graph:** Lightweight cross-shard representation enables global consistency without full-graph traversal.
- **Probabilistic sampling (T4):** 20% edge sampling provides statistical coverage at billion-quantum scale.

### 12.2  Deployment Profiles

| Parameter | T1 Dev/Test | T2 Prod Small | T3 Prod Large |
|---|---|---|---|
| Max quanta | 10 000 | 1 000 000 | 1 000 000 000 |
| Shards | 1 | 1 â€“ 10 | 10 â€“ 1 000 |
| SETTLEMENT_TICK | 60 s | 60 s | 60 s |
| TIDAL_EPOCH | 3 600 s | 3 600 s | 3 600 s |
| CONSOLIDATION_CYCLE | 36 000 s | 36 000 s | 36 000 s |
| Coherence budget | unlimited | 1 800 s | 1 800 s |
| SHREC history window | 10 epochs | 50 epochs | 50 epochs |
| VRF selection rate | 0.50 | 0.10 | 0.10 |
| Immune GC frequency | 10 epochs | 1 epoch | 1 epoch |
| Max queue depth/locus | 100 | 1 000 | 1 000 |
| PCVM drain rate | 10/tick | 50/tick | 50/tick |
| CRP+ mechanisms | M1, M5 only | All 7 | All 7 |
| Novelty pathway | Disabled | Enabled | Enabled |
| Edge tier updates | All every epoch | HOT/WARM/COLD | HOT/WARM/COLD + T4 sampling |
| Cross-shard bonus | N/A | 0.2 | 0.2 |

### 12.3  Performance Targets

| Metric | T1 | T2 | T3 |
|---|---|---|---|
| Ingestion throughput | 100/tick | 1 000/tick | 10 000/tick |
| Retrieval latency (p99) | < 10 ms | < 50 ms | < 200 ms |
| Coherence update (per epoch) | < 1 s | < 300 s | < 1 800 s |
| Consolidation cycle | < 60 s | < 3 600 s | < 36 000 s |

---

## 13  Open Questions and Future Work

1. **Federated EMA.** How do multiple EMA instances federate knowledge across organisational boundaries while preserving provenance integrity?
2. **Adaptive competition coefficients.** Can the LV competition matrix learn optimal coefficients from operational history?
3. **Continuous consolidation.** Is the batch CONSOLIDATION_CYCLE model optimal, or would continuous micro-consolidation yield better knowledge currency?
4. **Multi-modal quanta.** Extension of StructuredClaim to handle non-textual knowledge (images, sensor data, time series).
5. **Formal verification.** Can the SHREC stability properties be machine-verified using techniques from control theory?
6. **CRP+ calibration.** Optimal weight tuning (WEIGHT_APRT, WEIGHT_CODS, etc.) across different deployment contexts â€” currently based on simulation, not operational data.
7. **Immune memory false positives.** L2 and L3 matching thresholds may reject legitimate novel claims that structurally resemble previously-rejected attacks. Adaptive thresholds could mitigate this.

---

## 14  Conclusion

The Epistemic Metabolism Architecture v2.0 provides a comprehensive framework for managing knowledge as a living metabolic process. Key advances in this unified specification:

1. **Four-regime SHREC controller** replaces the ambiguous dual-controller design with graduated, deterministic regulation from NORMAL through EMERGENCY.
2. **CRP+ seven-mechanism consolidation defense** hardens the dreaming pipeline against the consolidation-poisoning threat, with formal invariants and constitutional parameter protection.
3. **Sharded coherence graph** with tiered updates enables scaling from development (T1) to billion-quantum production (T4) deployments.
4. **K-class terminology** resolves the C-class overloading, cleanly separating Compliance (C) from Knowledge Consolidation (K) claims.
5. **Unified temporal hierarchy** aligns all operations to the three-tier SETTLEMENT_TICK / TIDAL_EPOCH / CONSOLIDATION_CYCLE framework.
6. **PCVM degraded mode** ensures graceful degradation when verification infrastructure is unavailable.
7. **Vitality floor and grace period** prevent premature catabolism while ensuring eventual cleanup.

The system is designed for defence in depth: no single mechanism is trusted to prevent all failure modes. Instead, layered defenses â€” from source discounting at ingestion through CRP+ at consolidation to immune self-audit at regulation â€” provide overlapping protection.

---

## Appendix A: Canonical JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EpistemicQuantum",
  "type": "object",
  "required": ["id", "content", "opinion", "provenance", "edges",
               "metabolic_state", "projections", "timestamps",
               "claim_class", "credibility_rung"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "content": {
      "type": "object",
      "description": "StructuredClaim representation"
    },
    "opinion": {
      "type": "object",
      "required": ["b", "d", "u", "a"],
      "properties": {
        "b": { "type": "number", "minimum": 0, "maximum": 1 },
        "d": { "type": "number", "minimum": 0, "maximum": 1 },
        "u": { "type": "number", "minimum": 0, "maximum": 1 },
        "a": { "type": "number", "minimum": 0, "maximum": 1 }
      },
      "additionalProperties": false
    },
    "opinion_frozen": {
      "type": "boolean",
      "default": false,
      "description": "True during PCVM degraded mode"
    },
    "provenance": {
      "type": "object",
      "description": "W3C PROV-compatible provenance chain"
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["target_id", "edge_type", "weight"],
        "properties": {
          "target_id": { "type": "string", "format": "uuid" },
          "edge_type": {
            "type": "string",
            "enum": ["SUPPORT", "CONTRADICTION", "DERIVATION", "ANALOGY", "SUPERSESSION"]
          },
          "weight": { "type": "number", "minimum": 0, "maximum": 1 },
          "tier": {
            "type": "string",
            "enum": ["HOT", "WARM", "COLD"]
          },
          "creating_agent": { "type": "string" }
        }
      }
    },
    "metabolic_state": {
      "type": "string",
      "enum": ["INGESTED", "ACTIVE", "DORMANT", "CONSOLIDATED", "QUARANTINED", "DISSOLVED"]
    },
    "projections": {
      "type": "object",
      "properties": {
        "C3": { "type": "object" },
        "C4": { "type": "object" },
        "C5": { "type": "object" }
      }
    },
    "timestamps": {
      "type": "object",
      "required": ["created", "last_accessed", "last_modified"],
      "properties": {
        "created": { "type": "number" },
        "last_accessed": { "type": "number" },
        "last_modified": { "type": "number" },
        "last_accessed_epoch": { "type": "integer" },
        "floor_entry_epoch": {
          "type": ["integer", "null"],
          "description": "Epoch when vitality first reached floor (PA-7)"
        },
        "quarantine_entry_epoch": {
          "type": ["integer", "null"],
          "description": "Epoch when quantum entered QUARANTINED state"
        }
      }
    },
    "dissolution_record": {
      "type": ["object", "null"],
      "properties": {
        "timestamp": { "type": "number" },
        "reason": { "type": "string" },
        "evidence_redistributed": { "type": "integer" },
        "dissolution_confidence": { "type": "number" }
      }
    },
    "claim_class": {
      "type": "string",
      "enum": ["D", "E", "S", "H", "N", "P", "R", "C", "K"],
      "description": "C = Compliance, K = Knowledge Consolidation"
    },
    "credibility_rung": {
      "type": "integer",
      "minimum": 0,
      "maximum": 4,
      "description": "CRP+ credibility ladder position (0=SPECULATIVE, 4=CANONICAL)"
    }
  }
}
```

---

## Appendix B: State-Machine Transition Table

| From State | To State | Trigger | Conditions |
|---|---|---|---|
| INGESTED | ACTIVE | Classification + initial opinion complete | PCVM verification passed (or queued in degraded mode) |
| ACTIVE | DORMANT | Access recency below threshold | epochs_since_access > DORMANCY_THRESHOLD |
| ACTIVE | QUARANTINED | Catabolism candidate or CRP+ quarantine | evaluate_catabolism_candidate() returns True, OR CRP+ score in quarantine range |
| ACTIVE | CONSOLIDATED | Selected for consolidation synthesis | Source quantum contributes to a new K-class quantum |
| DORMANT | ACTIVE | Reactivation | New access or evidence arrives |
| DORMANT | QUARANTINED | Vitality at floor for grace period | Same conditions as ACTIVE â†’ QUARANTINED |
| CONSOLIDATED | ACTIVE | Re-verification | K-class quantum passes PCVM re-verification |
| QUARANTINED | ACTIVE | Re-evaluation succeeds | New evidence restores vitality above floor; or CRP+ re-evaluation passes |
| QUARANTINED | DISSOLVED | Quarantine window expires without recovery | 3 TIDAL_EPOCHs without supporting evidence |
| DISSOLVED | â€” | Terminal | No transitions from DISSOLVED |

---

## Appendix C: Reference Algorithms

### C.1  Subjective Logic Fusion

See Section 4.2.2 for cumulative fusion and discounting implementations.

### C.2  Corrected Lotka-Volterra Step

See Section 6.3.1 for the corrected LV step where signal intensity modulates competitive dynamics (not allocations directly) and floor correction is applied AFTER normalisation. This replaces the buggy v1.0 implementation.

### C.3  Evidence Recycling

See Section 5.4.2 for the complete `execute_recycling()` implementation.

### C.4  CRP+ Combined Scoring

See Section 5.3.4.8 for the `compute_crp_plus_score()` implementation.

### C.5  Sharded Coherence Update

See Section 7.3.3 for the `epoch_coherence_update()` implementation.

---

## Appendix D: Parameter Table and Deployment Profiles

### D.1  Core Parameters

| Parameter | Value | Section | Description |
|---|---|---|---|
| `SETTLEMENT_TICK` | 60 s | 1.5 | Fine-grained update interval |
| `TIDAL_EPOCH` | 3 600 s | 1.5 | SHREC regulation cycle |
| `CONSOLIDATION_CYCLE` | 36 000 s | 1.5 | Dreaming pipeline interval (10 TIDAL_EPOCHs) |
| `VITALITY_FLOOR` | 0.05 | 4.4 | Minimum vitality for non-terminal quanta |
| `VITALITY_GRACE_PERIOD` | 5 epochs | 4.4 | Epochs at floor before catabolism candidacy |
| `MAX_CONTRADICTION_WEIGHT_PER_AGENT` | 0.3 | 4.5.1 | Per-agent contradiction weight cap |
| `DECOMPOSITION_SIBLING_WEIGHT` | 0.3 | 4.6 | Edge weight between decomposed sibling claims |

### D.2  SHREC Parameters

| Parameter | Value | Section | Description |
|---|---|---|---|
| `PID_KP` | 0.5 | 6.6 | PID proportional gain |
| `PID_KI` | 0.1 | 6.6 | PID integral gain |
| `PID_KD` | 0.05 | 6.6 | PID derivative gain |
| `ELEVATED_CLAMP` | Â±10% | 6.7 | PID clamp in ELEVATED regime |
| `CRITICAL_CLAMP` | Â±25% | 6.7 | PID clamp in CRITICAL regime |
| `HYSTERESIS_EPOCHS` | 5 | 6.7.1 | Epochs required for regime downgrade |
| `SIGNAL_HISTORY_WINDOW` | 50 epochs | 6.4 | Rolling window for z-score computation |
| `IMMUNE_AUDIT_LOOKBACK_EPOCHS` | 5 | 6.8 | Lookback window for immune self-audit |
| `NORMAL_TO_ELEVATED` | z â‰¥ 1.5 | 6.7 | Regime transition threshold |
| `ELEVATED_TO_CRITICAL` | z â‰¥ 2.5 | 6.7 | Regime transition threshold |
| `CRITICAL_TO_EMERGENCY` | z â‰¥ 4.0 | 6.7 | Regime transition threshold |

### D.3  Coherence Graph Parameters

| Parameter | Value | Section | Description |
|---|---|---|---|
| `MAX_QUANTA_PER_SHARD` | 1 000 000 | 7.2.2 | Maximum quanta per shard (INV-E15) |
| `MAX_INTRA_EDGES_PER_SHARD` | 5 000 000 | 7.2.2 | Maximum intra-shard edges (INV-E18) |
| `MAX_CROSS_EDGES_PER_SHARD` | 500 000 | 7.2.2 | Maximum cross-shard edges (INV-E18) |
| `CROSS_SHARD_BONUS` | 0.2 | 7.2.3 | Weight bonus for cross-shard edges |
| `HOT_THRESHOLD` | 1 epoch | 7.3.1 | Hot tier access recency |
| `WARM_THRESHOLD` | 5 epochs | 7.3.1 | Warm tier access recency |
| `WEIGHT_DECAY_RATE` | 0.01/epoch | 7.3.2 | Edge weight decay rate |
| `COHERENCE_COMPUTATION_BUDGET` | 1 800 s | 7.3.3 | Max coherence computation per epoch |
| `T4_SAMPLING_RATE` | 0.20 | 7.5 | Probabilistic edge sampling at T4 |

### D.4  CRP+ Parameters

| Parameter | Value | Section | Constitutional | Description |
|---|---|---|---|---|
| `STABILITY_THRESHOLD` | 0.70 | 5.3.4.1 | Yes | APRT minimum stability |
| `EXPECTED_DISSENT_LEVEL` | 1.5 | 5.3.4.2 | Yes | CODS dissent normalisation |
| `M3_MAX_CONTRIBUTION` | 0.15 | 5.3.4.3 | No | Source purpose score cap |
| `M3_HIGH_PURPOSE_THRESHOLD` | 0.80 | 5.3.4.3 | No | High purpose threshold |
| `VRF_SELECTION_RATE` | 0.10 | 5.3.4.4 | Yes | VRF per-cycle selection rate |
| `VRF_ANTI_STARVATION_BOOST` | 20 epochs | 5.3.4.4 | No | Boost trigger epoch |
| `VRF_FORCED_SELECTION_EPOCH` | 40 epochs | 5.3.4.4 | No | Forced selection epoch |
| `PROMOTION_OBSERVATION_WINDOW` | 10 epochs | 5.3.4.5 | Yes | Min epochs for rung promotion |
| `WEIGHT_APRT` | 0.35 | 5.3.4.8 | Yes | APRT component weight |
| `WEIGHT_CODS` | 0.25 | 5.3.4.8 | Yes | CODS component weight |
| `WEIGHT_PROBE` | 0.25 | 5.3.4.8 | Yes | Probe component weight |
| `WEIGHT_IMMUNE` | 0.15 | 5.3.4.8 | Yes | Immune component weight |
| `ACCEPT_THRESHOLD` | 0.35 | 5.3.4.8 | Yes | CRP+ accept threshold |
| `QUARANTINE_THRESHOLD` | 0.60 | 5.3.4.8 | Yes | CRP+ quarantine/reject boundary |
| `L2_MATCH_THRESHOLD` | 0.60 | 5.3.4.7 | No | Immune L2 structural match |
| `L3_MATCH_THRESHOLD` | 0.50 | 5.3.4.7 | No | Immune L3 behavioral match |
| `NOVELTY_QUARANTINE_MIN_CYCLES` | 5 | 5.3.5 | No | Min quarantine for N3 claims |
| `NOVELTY_QUARANTINE_MAX_CYCLES` | 10 | 5.3.5 | No | Max quarantine for N3 claims |

### D.5  Defense-in-Depth Parameters (C10)

| Parameter | Value | Section | Description |
|---|---|---|---|
| `ROOT_COVERAGE_THRESHOLD` | 0.50 | 5.3.3.1 | Minimum provenance root diversity |
| `TEMPORAL_CLUSTER_MIN_SPAN` | 10 epochs | 5.3.3.1 | Minimum temporal span for sources |
| `CLUSTER_DOMINANCE_THRESHOLD` | 0.30 | 5.3.3.1 | Max single-cluster dominance |
| `COMPETITIVE_THRESHOLD` | 0.40 | 5.3.3.2 | Counter-hypothesis competitiveness |
| `LOW_CONFIDENCE_UNCERTAINTY_FLOOR` | 0.50 | 5.3.3.2 | Minimum uncertainty after probing |
| `MAX_CASCADE_DEPTH` | 5 | 5.3.3.3 | Max credibility cascade depth |
| `CASCADE_REDUCTION_FACTOR` | 0.15 | 5.3.3.3 | Base cascade reduction |
| `MAX_CASCADE_REDUCTION` | 0.10 | 5.3.3.3 | Max reduction per cascade step |

### D.6  PCVM Degraded Mode Parameters

| Parameter | Value | Section | Description |
|---|---|---|---|
| `MAX_QUEUE_DEPTH_PER_LOCUS` | 1 000 | 10.1.1 | Max queued items per locus |
| `PCVM_OUTAGE_DETECTION_EPOCHS` | 3 | 10.1.1 | Consecutive failures for outage detection |
| `PCVM_RECOVERY_DRAIN_RATE` | 50/tick | 10.1.1 | Queue drain rate on recovery |

### D.7  Dreaming Parameters

| Parameter | Value | Section | Description |
|---|---|---|---|
| `EXPLORATION_TEMPERATURE` | 0.7 | 5.3.2 | Phase A (exploration) LLM temperature |
| `SYNTHESIS_TEMPERATURE` | 0.3 | 5.3.2 | Phase B (filtering) LLM temperature |

### D.8  Retrieval Parameters

| Parameter | Value | Section | Description |
|---|---|---|---|
| `SEMANTIC_INDEX_DIMENSIONS` | 768 | 9.2 | Embedding width for semantic fingerprints |
| `SEMANTIC_INDEX_PROBE_COUNT` | 16 | 9.2 | ANN probes per shard query |
| `SEMANTIC_INDEX_CANDIDATE_MULTIPLIER` | 4 | 9.2 | Oversampling factor before final rerank |
| `SEMANTIC_INDEX_REFRESH_EPOCHS` | 1 | 9.2 | Max epochs between mutation and index refresh |
| `SEMANTIC_SIMILARITY_FLOOR` | 0.35 | 9.1, 9.2 | Minimum similarity retained from ANN results |

### D.9  Bundle Compaction Parameters

| Parameter | Value | Section | Description |
|---|---|---|---|
| `BUNDLE_COMPACTION_MIN_RECORDS` | 32 | 5.4.4.1, 5.4.4.7 | Minimum record count before bundle compaction becomes eligible |
| `BUNDLE_TARGET_CHUNK_SIZE` | 4096 bytes | 5.4.4.3, 5.4.4.7 | Target canonical chunk size for deduplicated bundle storage |
| `BUNDLE_MAX_RECONSTRUCT_MS` | 500 ms | 5.4.4.7 | Maximum acceptable reconstruction latency per member |
| `COMPACTED_BUNDLE_RETENTION_CYCLES` | 100 | 5.4.3.5, 5.4.4.5, 5.4.4.7 | Cycles a compacted bundle must remain available before non-perpetual summary reduction |

### D.10  Heuristic Family Store Parameters

| Parameter | Value | Section | Description |
|---|---|---|---|
| `HEURISTIC_FAMILY_FRONTIER_MAX` | 3 | 7.2.5 | Maximum simultaneous frontier heuristics in one family when context tags are disjoint |
| `HEURISTIC_FAMILY_RETIREMENT_MIN_EPOCHS` | 30 | 5.4.1, 7.2.5 | Minimum epochs without a viable frontier before a deprecated heuristic family becomes retired |
| `HEURISTIC_FAMILY_BUNDLE_PRIORITY` | 1.5 | 5.4.4.1, 7.2.5 | Priority multiplier for bundle-compaction scheduling of retired heuristic families |

---

## Appendix E: Conformance Requirements

### E.1  Core EMA Requirements (from v1.0)

| ID | Level | Requirement |
|---|---|---|
| CR-1 | MUST | Every quantum carries a valid subjective-logic opinion with b + d + u = 1 (INV-E1). |
| CR-2 | MUST | Every quantum has a non-empty W3C PROV provenance chain (INV-E2). |
| CR-3 | MUST | All coherence edges are reciprocal (INV-E3). |
| CR-4 | MUST | Budget allocations sum to 1.0 within Îµ = 1e-9 (INV-E4). |
| CR-5 | MUST | Vitality â‰¥ VITALITY_FLOOR for non-terminal quanta (INV-E5). |
| CR-6 | MUST | Every quantum occupies exactly one lifecycle state (INV-E6). |
| CR-7 | MUST | Unresolved contradictions increase by at most 10% per TIDAL_EPOCH (INV-E7). |
| CR-8 | MUST | Dissolved quanta trigger re-evaluation of high-dependency children (INV-E8). |
| CR-9 | MUST | Projection fidelity remains above type-specific minimums (INV-E9). |
| CR-10 | MUST | Claim class is immutable after classification except via K-class consolidation or G-class override (INV-E10). |
| CR-11 | MUST | Only the six defined lifecycle states are permitted. |
| CR-12 | MUST | State transitions follow the transition table (Appendix B). |
| CR-13 | MUST | INGESTED â†’ ACTIVE requires PCVM verification or degraded-mode queuing. |
| CR-14 | MUST | Catabolism uses two-phase dissolution (quarantine then dissolve). |
| CR-15 | MUST | Evidence recycling occurs during dissolution. |
| CR-16 | MUST | SHREC floor allocations are enforced under all regimes. |
| CR-17 | MUST | Consolidation produces K-class quanta only. |
| CR-18 | MUST | External claims classified as K-class are rejected at ingestion. |
| CR-19 | MUST | Signal intensities modulate LV competition coefficients, not allocations directly. |
| CR-20 | MUST | Floor correction is applied AFTER LV normalisation. |
| CR-21 | MUST | Per-agent contradiction weight is capped at MAX_CONTRADICTION_WEIGHT_PER_AGENT. |
| CR-22 | MUST | Contradiction edges exceeding the cap are created at reduced weight (min 0.05), never rejected. |
| CR-23 | MUST | Compound claims are decomposed before processing. |
| CR-24 | MUST | Vitality grace period (5 epochs) must elapse before catabolism candidacy. |
| CR-25 | SHOULD | Quanta near the vitality floor should be monitored with increasing frequency. |
| CR-26 | SHOULD | SHREC regime transitions should be logged with full z-score context. |
| CR-27 | SHOULD | Retrieval results should be sorted by relevance * vitality * opinion strength. |
| CR-28 | SHOULD | Dormant quanta should be excluded from retrieval unless explicitly requested. |
| CR-29 | SHOULD | Cross-shard edges should receive the CROSS_SHARD_BONUS weight addition. |
| CR-30 | SHOULD | Bridge edges should be protected from budget pruning. |
| CR-31 | SHOULD | Statistical self-model should use at least 50 epochs of history. |
| CR-32 | SHOULD | Immune self-audit should run every TIDAL_EPOCH. |
| CR-33 | MAY | Domain-adaptive credibility ladder thresholds may adjust rung boundaries. |
| CR-34 | MAY | Reconstruction functions may use alternative similarity metrics. |
| CR-35 | MAY | T1 deployments may disable sharding and tiered updates. |
| CR-36 | MAY | T1 deployments may use simplified CRP+ (M1 + M5 only). |
| CR-37 | MAY | Adaptive LV competition coefficients may be implemented. |
| CR-38 | MUST | Bundle compaction MUST be lossless with respect to the pre-compaction archive representation. |
| CR-39 | MUST | Only archived or superseded cold-tier records may enter the Bundle Compaction Engine. |
| CR-40 | MUST | Every compacted member MUST reconstruct to its `original_record_hash` before source records are deleted. |
| CR-41 | SHOULD | Retrieval should be transparent across raw archive storage and compacted bundle storage. |
| CR-42 | MAY | Implementations may use alternative deterministic chunking algorithms if reconstruction remains lossless. |

### E.2  SHREC Controller Requirements (from C10 Hardening)

| ID | Level | Requirement |
|---|---|---|
| CR-S1 | MUST | Budget conservation holds under all four regimes (INV-E11). |
| CR-S2 | MUST | Floor enforcement applies after LV+PID combination (INV-E12). |
| CR-S3 | MUST | Regime downgrades require HYSTERESIS_EPOCHS consecutive epochs (INV-E13). |
| CR-S4 | MUST | EMERGENCY regime freezes allocations at entry values (INV-E14). |
| CR-S5 | MUST | Invariant violations force EMERGENCY regime immediately. |
| CR-S6 | MUST | PID clamp bounds are Â±10% (ELEVATED) and Â±25% (CRITICAL). |
| CR-S7 | SHOULD | Regime transitions should trigger audit logging. |
| CR-S8 | MAY | PID integral anti-windup may use alternative clamping strategies. |

### E.3  Coherence Sharding Requirements (from C10 Hardening)

| ID | Level | Requirement |
|---|---|---|
| CR-C1 | MUST | No shard exceeds MAX_QUANTA_PER_SHARD (INV-E15). |
| CR-C2 | MUST | Cross-shard edges appear in both endpoint shards and the border graph (INV-E16). |
| CR-C3 | MUST | Edge tier classification is consistent with access frequency (INV-E17). |
| CR-C4 | MUST | Per-shard edge budgets are enforced (INV-E18). |
| CR-C5 | MUST | Border graph is complete and consistent (INV-E19). |
| CR-C6 | MUST | Coherence computation stays within COHERENCE_COMPUTATION_BUDGET. |
| CR-C7 | SHOULD | Shard splits should minimise cross-partition edges. |
| CR-C8 | SHOULD | T4 probabilistic sampling should achieve statistical coverage over 5 epochs. |
| CR-C9 | MAY | Alternative graph partitioning algorithms may be used. |
| CR-C10 | MUST | Claim family membership is materialized from derivation, supersession, and lineage metadata and preserved across shard splits and moves. |
| CR-C11 | SHOULD | Retrieval should support family-scoped queries and frontier-only inspection of proposition lineages. |
| CR-C12 | MUST | Semantic index entries are refreshed within SEMANTIC_INDEX_REFRESH_EPOCHS after ingestion, consolidation, supersession, or catabolic state change. |
| CR-C13 | MUST | QUARANTINED and DISSOLVED quanta are excluded from semantic-index candidate generation. |
| CR-C14 | SHOULD | Topic-bearing retrieval should use semantic index candidate generation before vitality/opinion reranking. |

### E.4  Defense-in-Depth Requirements (from C10)

| ID | Level | Requirement |
|---|---|---|
| CR-H10 | MUST | Consolidation candidates MUST pass source independence verification (I1, I2, I3). |
| CR-H11 | MUST | Every consolidation candidate MUST undergo adversarial probing. |
| CR-H12 | MUST | Consolidation lineage MUST be tracked; credibility cascading on failure is mandatory. |

### E.5  CRP+ Requirements (from C13)

| ID | Level | Requirement |
|---|---|---|
| CR-CRP1 | MUST | Every consolidation candidate passes through all applicable CRP+ mechanisms (INV-CRP1). |
| CR-CRP2 | MUST | VRF selection is unpredictable from public inputs (INV-CRP2). |
| CR-CRP3 | MUST | Credibility promotions require sustained evidence over PROMOTION_OBSERVATION_WINDOW (INV-CRP3). |
| CR-CRP4 | MUST | Credibility demotions are immediate upon threshold violation (INV-CRP3). |
| CR-CRP5 | MUST | SPECULATIVE and PROVISIONAL quanta are excluded from consolidation sources (INV-CRP4). |
| CR-CRP6 | MUST | Immune memory growth is bounded O(n); GC runs every epoch (INV-CRP5). |
| CR-CRP7 | MUST | N3 paradigmatic claims complete all four novelty pathway checks (INV-CRP6). |
| CR-CRP8 | MUST | CRP+ scores are deterministically reproducible (INV-CRP7). |
| CR-CRP9 | MUST | Constitutional parameters require G-class governance approval to modify (INV-CRP8). |
| CR-CRP10 | MUST | CORROBORATED quanta participate in consolidation at 0.50 weight only. |
| CR-CRP11 | MUST | Kâ†’K consolidation is sandboxed with additional APRT and capped at PROVISIONAL rung. |
| CR-CRP12 | MUST | Immune memory records rejections at all three signature levels (L1, L2, L3). |
| CR-CRP13 | MUST | CRP+ combined score uses the canonical weight formula (APRT 0.35, CODS 0.25, PROBE 0.25, IMMUNE 0.15). |
| CR-CRP14 | MUST | Decision thresholds: ACCEPT < 0.35, QUARANTINE 0.35-0.60, REJECT > 0.60. |
| CR-CRP15 | SHOULD | VRF anti-starvation boost should activate after 20 epochs. |
| CR-CRP16 | SHOULD | VRF forced selection should activate after 40 epochs. |
| CR-CRP17 | SHOULD | Source purpose scoring should be applied only as a tie-breaker. |
| CR-CRP18 | SHOULD | Novelty pathway temporal quarantine should be 5-10 CONSOLIDATION_CYCLEs. |
| CR-CRP19 | SHOULD | Provenance deep audit should include KS test, framing consistency, and M7 cross-reference. |
| CR-CRP20 | SHOULD | Immune L2 matching should use cosine similarity at threshold 0.60. |
| CR-CRP21 | MAY | Domain-adaptive credibility thresholds may vary by claim class. |
| CR-CRP22 | MAY | Alternative VRF constructions may be used if INV-CRP2 is maintained. |
| CR-CRP23 | MAY | Immune memory GC max_age may be deployment-specific. |

### E.6  PCVM Degraded Mode Requirements

| ID | Level | Requirement |
|---|---|---|
| CR-P1 | MUST | PCVM outage detection activates after PCVM_OUTAGE_DETECTION_EPOCHS consecutive failures. |
| CR-P2 | MUST | Opinions are frozen during PCVM degraded mode. |
| CR-P3 | MUST | Queue depth per locus does not exceed MAX_QUEUE_DEPTH_PER_LOCUS. |
| CR-P4 | MUST | Queue drains at PCVM_RECOVERY_DRAIN_RATE on recovery. |
| CR-P5 | SHOULD | Queued quanta should be processed in FIFO order. |
| CR-P6 | MAY | Queue overflow may use priority-based eviction. |

### E.7  Four-Tier Memory Model Requirements

| ID | Level | Requirement |
|---|---|---|
| CR-MTM-1 | MUST | Tier assignment is deterministic from metabolic state and access recency. |
| CR-MTM-2 | MUST | Tier assignment is consistent with coherence graph edge tiers (INV-E17). |
| CR-MTM-3 | MUST | DORMANT quanta are always classified as LONG_TERM. |
| CR-MTM-4 | MUST | DISSOLVED quanta are always classified as ARCHIVAL. |
| CR-MTM-5 | SHOULD | Tier distribution is reported as a SHREC diagnostic at each TIDAL_EPOCH. |

### E.8  Heuristic Family Store Requirements

| ID | Level | Requirement |
|---|---|---|
| CR-HFS-1 | MUST | Only H-class quanta may be assigned a `heuristic_family_id`. |
| CR-HFS-2 | MUST | Heuristic family membership, frontier state, and retirement state are preserved across shard moves and archive transitions. |
| CR-HFS-3 | MUST | RETIRED heuristic families are excluded from default retrieval and semantic-index candidate generation unless the caller explicitly opts in. |
| CR-HFS-4 | SHOULD | Simultaneous frontier heuristics in one family should be limited to disjoint context tags and `HEURISTIC_FAMILY_FRONTIER_MAX`. |
| CR-HFS-5 | SHOULD | Archived members of a RETIRED heuristic family should be queued together for bundle compaction. |

---

## Appendix F: Test Vectors

### TV-1: Opinion Fusion

```
Input:  Ï‰1 = (0.6, 0.1, 0.3, 0.5), Ï‰2 = (0.4, 0.2, 0.4, 0.5)
Fusion: cumulative_fuse(Ï‰1, Ï‰2)
Expected: b â‰ˆ 0.632, d â‰ˆ 0.158, u â‰ˆ 0.211, a = 0.5
```

### TV-2: Vitality Computation

```
Input:  opinion = (0.7, 0.1, 0.2, 0.5), epochs_since_access = 5,
        support_weight_sum = 2.0, claim_class = "E"
Expected: vitality > VITALITY_FLOOR (0.05)
```

### TV-3: SHREC Budget Conservation

```
Input:  allocations = {ingest: 0.25, circ: 0.30, consol: 0.20, catab: 0.10, coher: 0.15}
Post-LV: sum(allocations) == 1.0 Â± 1e-9
Post-floor: all(alloc[s] >= floor[s]) for s in SPECIES
```

### TV-4: K-class Consolidation Output

```
Input:  cluster of 5 E-class quanta with avg belief > 0.7
Process: three_pass_synthesis() â†’ CRP+ evaluation â†’ PCVM submission
Expected: output quantum has claim_class = "K" (NOT "C")
          output quantum has credibility_rung = PROVISIONAL (if Kâ†’K) or per CRP+ evaluation
```

### TV-5: Regime Transition

```
Input:  NORMAL regime, max z-score = 1.8
Expected: transition to ELEVATED (threshold 1.5 crossed)
Input:  ELEVATED regime, max z-score = 1.2 for 5 consecutive epochs
Expected: transition to NORMAL (hysteresis satisfied)
Input:  ELEVATED regime, max z-score = 1.2 for 4 consecutive epochs
Expected: remain ELEVATED (hysteresis not yet satisfied)
```

### TV-6: Contradiction Edge Cap (Corrected per PA-8)

```
Input:  Agent A has existing contradiction edges totaling weight 0.28 to target quantum.
        Agent A proposes new contradiction edge with weight 0.10.
Expected: Edge created at weight 0.02 (remaining budget = 0.30 - 0.28 = 0.02).
          Edge is NOT rejected.

Input:  Agent A has existing contradiction edges totaling weight 0.30.
        Agent A proposes new contradiction edge.
Expected: Edge created at minimum weight 0.05.
          Edge is NOT rejected.
```

### TV-7: CRP+ Combined Score

```
Input:  APRT stability = 0.85, CODS dissent = 0.30,
        Probe competitive = 0/5, No immune match, purpose = 0.10
Score:  0.35 * (1 - 0.85) + 0.25 * 0.30 + 0.25 * 0.0 + 0.15 * 0.0 + 0.10
     =  0.0525 + 0.075 + 0 + 0 + 0.10 = 0.2275
Decision: ACCEPT (< 0.35)
```

### TV-8: Credibility Ladder Promotion

```
Input:  Quantum at CORROBORATED (rung 2) with u = 0.12 for 10 consecutive epochs.
Expected: Promote to ESTABLISHED (rung 3).

Input:  Same quantum at rung 2, u = 0.12 for only 8 epochs.
Expected: Remain at CORROBORATED (promotion requires PROMOTION_OBSERVATION_WINDOW = 10).

Input:  Quantum at ESTABLISHED (rung 3), u suddenly rises to 0.55.
Expected: Immediate demotion to PROVISIONAL (rung 1).
```

### TV-9: Source Independence Verification

```
Input:  5 sources, 3 unique provenance roots, temporal span = 12 epochs,
        max cluster dominance = 0.25.
Expected: I1 pass (3/5 = 0.60 â‰¥ 0.50), I2 pass (12 â‰¥ 10), I3 pass (0.25 < 0.30).
          Overall: PASS.

Input:  5 sources, 2 unique provenance roots, temporal span = 8 epochs.
Expected: I1 fail (2/5 = 0.40 < 0.50), I2 fail (8 < 10).
          Overall: FAIL.
```

### TV-10: PCVM Degraded Mode

```
Input:  3 consecutive PCVM verification failures.
Expected: Degraded mode activated. All opinions frozen.
          New ingestions queued (up to MAX_QUEUE_DEPTH_PER_LOCUS).
          On PCVM recovery, queue drains at PCVM_RECOVERY_DRAIN_RATE per tick.
```

### TV-11: Heuristic Family Retirement

```
Input:  H-class family HF-7 with q1=ROOT version 1, q2=REVISION version 2,
        q2 frontier=True, q1 frontier=False, q2 belief drops below 0.60
        for 35 consecutive epochs, no replacement frontier admitted.
Expected: Family status transitions ACTIVE -> DEPRECATED -> RETIRED.
          Default retrieval excludes q1 and q2.
          Archived family members become bundle-compaction candidates.
```

---

## Appendix G: Cross-Reference Matrix

| Specification | Sections Integrated | Integration Points |
|---|---|---|
| C6 v1.0.0 (original) | All (1â€“14, App Aâ€“H) | Base document |
| C6 Patch Addendum v1.1 | PA-1 through PA-12 | PA-1â†’Â§6.3.1, PA-2â†’Â§5.4.2, PA-3â†’Â§8.3, PA-4â†’Â§7.2.3, PA-5â†’Â§4.6, PA-6â†’Â§12.2, PA-7â†’Â§4.4, PA-8â†’Â§4.5.1, PA-9â†’Â§10.1.1, PA-10â†’Â§5.3.2, PA-11â†’Â§6.8, PA-12â†’Â§3.4 |
| C9 Reconciliation | Errata E-C6-01, E-C6-02 | K-class relabelingâ†’Â§3.4, CONSOLIDATION_CYCLE=36000sâ†’Â§1.5 |
| C10 SHREC/Coherence Hardening | Sections 1â€“4 | 4-regime controllerâ†’Â§6.7, Sharded coherenceâ†’Â§7.2, INV-E11â€“E19 |
| C10 Defense-in-Depth Â§3 | Source independence, Adversarial probing, Lineage tracking | Â§5.3.3, CR-H10â€“H12 |
| C13 CRP+ | Sections 4â€“12 | M1â€“M7â†’Â§5.3.4, Novelty pathwayâ†’Â§5.3.5, Scoringâ†’Â§5.3.4.8, INV-CRP1â€“CRP8 |

---

## Appendix H: Glossary

| Term | Definition |
|---|---|
| **APRT** | Aggregate Perturbation Robustness Testing â€” M1 of CRP+. Tests synthesis stability under source perturbation. |
| **Base rate (a)** | Prior probability in the absence of evidence, part of the subjective-logic opinion tuple. |
| **Border graph** | Lightweight global graph of cross-shard edges enabling inter-shard consistency. |
| **C-class (Compliance)** | Claim class for regulatory/compliance assertions. Immutable, no aging. |
| **Catabolism** | The metabolic process of retiring non-viable knowledge through quarantine and dissolution. |
| **Circulation** | The metabolic process of maintaining active knowledge via opinion updates and edge propagation. |
| **Claim class** | One of nine categories (D, E, S, H, N, P, R, C, K) governing a quantum's admission, aging, and consolidation rules. |
| **Claim family graph** | Materialized overlay indexing quanta by shared proposition lineage across revision, decomposition, supersession, and consolidation output. |
| **CODS** | Calibrated Opponent-aware Dissent Search â€” M2 of CRP+. Classifies novelty and searches for calibrated dissent. |
| **Coherence graph** | Typed, weighted, bidirectional graph connecting epistemic quanta via five edge types. |
| **CONSOLIDATION_CYCLE** | 36 000 s (10 TIDAL_EPOCHs). Interval between dreaming/consolidation pipeline executions. |
| **Consolidation (Dreaming)** | Offline synthesis of new K-class knowledge from clusters of existing quanta. |
| **Credibility ladder** | Five-rung scale (SPECULATIVE â†’ CANONICAL) tracking quantum trustworthiness over time. |
| **CRP+** | Consolidation Robustness Protocol. Seven-mechanism defense against consolidation poisoning. |
| **Cumulative fusion** | Subjective-logic operation combining independent evidence sources, reducing uncertainty. |
| **Dissolution** | Terminal phase of catabolism: content removed, provenance retained, evidence recycled. |
| **ECVRF** | Elliptic Curve Verifiable Random Function, used for unpredictable consolidation selection (M4). |
| **Edge tier** | Access-frequency classification (HOT/WARM/COLD) determining update frequency. |
| **Four-tier memory model** | Working/Short-term/Long-term/Archival memory classification derived from lifecycle state and access recency (Â§4.6). Satisfies C3 Â§1.2 deferral. |
| **EMERGENCY regime** | SHREC regime that freezes allocations at entry values. Triggered by z â‰¥ 4.0 or invariant violation. |
| **Epistemic quantum (EQ)** | Fundamental knowledge unit: a 10-tuple carrying content, opinion, provenance, edges, and metadata. |
| **Evidence recycling** | Transfer of support evidence from a dissolved quantum to surviving dependents. |
| **Family frontier** | Active, non-superseded boundary set for a claim family used for retrieval and re-evaluation. |
| **Floor** | Minimum allocation for each metabolic function, enforced under all SHREC regimes. |
| **G-class** | Governance class. Required for modifying constitutional parameters. |
| **Grace period** | VITALITY_GRACE_PERIOD (5 epochs) at vitality floor before catabolism candidacy. |
| **Heuristic family** | Versioned grouping of H-class quanta that address the same operational problem across revisions, alternatives, and specializations. |
| **Heuristic family store** | Materialized C6 overlay tracking H-class family membership, frontier state, deprecation, and retirement. |
| **Hysteresis** | HYSTERESIS_EPOCHS (5) consecutive low-stress epochs required for SHREC regime downgrade. |
| **Immune memory** | Three-level signature store (L1 hash, L2 structural, L3 behavioral) for detecting recurrent attacks (M7). |
| **Immune self-audit** | SHREC periodic audit of quarantine/dissolution rates for anomaly detection. |
| **Ingestion** | The metabolic process of receiving, classifying, and admitting new knowledge. |
| **K-class (Knowledge Consolidation)** | Claim class for quanta produced by the dreaming/consolidation pipeline. Replaces the overloaded "C-class" for consolidation. |
| **Lotka-Volterra (LV)** | Ecological competition model governing resource allocation among metabolic functions. |
| **N3 (paradigmatic)** | Novelty classification for claims that contradict established knowledge. Triggers novelty pathway. |
| **Novelty pathway** | Enhanced evaluation path for N3 paradigmatic claims: enhanced APRT, adversarial probing, temporal quarantine, provenance deep audit. |
| **Opinion** | Subjective-logic tuple (b, d, u, a) representing epistemic state. |
| **PCVM** | Proof Chain Verification Machine. Cryptographic verification infrastructure for knowledge claims. |
| **PCVM degraded mode** | Operating state when PCVM is unavailable: opinions frozen, ingestion queued. |
| **PID controller** | Proportional-integral-derivative controller providing additional SHREC correction in ELEVATED and CRITICAL regimes. |
| **Projected probability** | P(Ï‰) = b + aÂ·u. Maps opinion to point probability. |
| **Projection** | Lossy but bounded-error view of a quantum for a peer subsystem (C3, C4, C5). |
| **Bundle compaction** | Lossless storage rewrite that deduplicates related archived records without losing information relative to the pre-compaction archive representation. |
| **Compaction bundle** | Cold-tier package containing deduplicated chunks plus a manifest sufficient to reconstruct each archived member record byte-for-byte. |
| **Semantic fingerprint** | Canonicalized vector representation of a quantum's content, class, provenance, and local graph context used for retrieval candidate generation. |
| **Semantic index** | Shard-aware approximate-nearest-neighbor retrieval layer that narrows candidate quanta before vitality/opinion reranking. |
| **Quarantine** | Intermediate state before dissolution; quantum excluded from retrieval, subject to re-evaluation window. |
| **SETTLEMENT_TICK** | 60 s. Fine-grained update interval. |
| **SHREC** | Stratified Homeostatic Regulation with Ecological Competition. Five-signal regulatory layer with four-regime controller. |
| **Source independence** | Verification that consolidation sources trace to diverse, temporally spread, non-clustered origins. |
| **Subjective logic** | JÃ¸sang's framework for reasoning under uncertainty using opinion tuples. |
| **TIDAL_EPOCH** | 3 600 s (1 h). SHREC regulation cycle interval. |
| **Vitality** | Composite health score determining catabolism candidacy. Multiplicative composition with floor. |
| **Working tier** | Memory tier for quanta actively accessed within last 1 TIDAL_EPOCH. Highest processing priority (Â§4.6). |
| **Short-term tier** | Memory tier for quanta accessed within last 5 TIDAL_EPOCHs. Moderate priority (Â§4.6). |
| **Long-term tier** | Memory tier for ACTIVE+COLD or DORMANT quanta. Low priority, catabolism candidates (Â§4.6). |
| **Archival tier** | Memory tier for DISSOLVED quanta in the Archive Layer (Â§4.6, Â§5.4.3). Read-only, immutable. |
| **VRF** | Verifiable Random Function. Used for unpredictable consolidation selection (M4). |
| **W3C PROV** | Provenance model for tracking knowledge lineage. |

---

## Changelog

### v2.0 (2026-03-10)

**Unified rewrite** integrating C6 v1.0.0, Patch Addendum v1.1 (PA-1 through PA-12), C10 SHREC/Coherence Hardening, C10 Defense-in-Depth Â§3, C9 Reconciliation Errata, and C13 CRP+.

#### Breaking Changes
- **K-class relabeling (PA-12, E-C6-01):** "C-class" for consolidation outputs replaced by "K-class" (Knowledge Consolidation) throughout. C-class now exclusively denotes Compliance claims. Claim class enum expanded to 9 entries: D, E, S, H, N, P, R, C, K.
- **CONSTITUTIONAL regime removed:** Replaced by EMERGENCY regime (static hold) in the four-regime SHREC controller.
- **CONSOLIDATION_CYCLE = 36 000 s (E-C6-02):** Changed from previous value to align with C9 three-tier temporal hierarchy (= 10 TIDAL_EPOCHs).

#### New Capabilities
- **CRP+ seven-mechanism consolidation defense (C13):** M1 APRT, M2 CODS, M3 Source Purpose Scoring, M4 VRF Consolidation Selection, M5 Graduated Credibility Ladder, M6 Consolidation Depth Limits, M7 Immune Memory. Woven into Section 5.3.4.
- **Novelty Pathway (C13):** Enhanced evaluation for N3 paradigmatic claims with four checks. Section 5.3.5.
- **Four-regime SHREC controller (C10):** NORMAL/ELEVATED/CRITICAL/EMERGENCY with defined transition thresholds, hysteresis, and PID clamp bounds. Replaces Section 6.7 entirely.
- **Sharded coherence graph (C10):** Shard limits, border graph, tiered HOT/WARM/COLD edge updates, T4 probabilistic sampling. Woven into Section 7.
- **Source independence verification (C10):** I1 provenance roots, I2 temporal clustering, I3 Sentinel cluster diversity. Section 5.3.3.1.
- **Adversarial consolidation probing (C10):** Counter-hypothesis generation and uncertainty elevation. Section 5.3.3.2.
- **Consolidation lineage tracking (C10):** sqrt-diluted credibility cascading. Section 5.3.3.3.
- **PCVM degraded mode (PA-9):** Queued ingestion, frozen opinions, recovery drain. Section 10.1.1.
- **Two-temperature dreaming (PA-10):** T=0.7 exploration, T=0.3 filtering. Section 5.3.2.
- **T4 scale tier (C10):** >1B quanta with probabilistic edge sampling.

#### Bug Fixes
- **PA-1:** LV signal multiplication ordering corrected â€” signal intensity modulates competition coefficients, floor correction applied AFTER normalisation.
- **PA-8 / TV-6:** Contradiction edges exceeding per-agent cap are now created at reduced weight (min 0.05), not rejected.

#### Definitions Provided (previously missing)
- **PA-2:** `execute_recycling()` â€” complete evidence recycling implementation.
- **PA-3:** `reconstruct_from_c3/c4/c5()` â€” reconstruction functions with fidelity measurement.
- **PA-4:** `compute_cross_shard_bonus()` â€” cross-shard edge bonus definition.
- **PA-5:** `decompose_claim()` â€” compound claim decomposition.
- **PA-6:** Deployment profiles table (T1/T2/T3).
- **PA-7:** Vitality floor (0.05) and grace period (5 epochs) with `evaluate_catabolism_candidate()`.
- **PA-11:** Immune self-audit lookback window (5 epochs).

#### New Invariants
- INV-E11 through INV-E14: SHREC controller invariants.
- INV-E15 through INV-E19: Coherence sharding invariants.
- INV-CRP1 through INV-CRP8: CRP+ invariants.

#### New Conformance Requirements
- CR-H10, CR-H11, CR-H12: Defense-in-depth requirements.
- CR-S1 through CR-S8: SHREC controller requirements.
- CR-C1 through CR-C9: Coherence sharding requirements.
- CR-CRP1 through CR-CRP23: CRP+ requirements.
- CR-P1 through CR-P6: PCVM degraded mode requirements.

#### Schema Additions
- `opinion_frozen` (boolean): PCVM degraded mode flag.
- `floor_entry_epoch` (integer|null): Vitality grace period tracking.
- `quarantine_entry_epoch` (integer|null): Quarantine timing.
- `credibility_rung` (integer 0-4): CRP+ credibility ladder position.
- `"K"` added to `claim_class` enum.
- `tier` (HOT/WARM/COLD) added to edge schema.

### v2.0.4 â€” T-085 Heuristic Family Store (2026-03-12)

Added Section 7.2.5 specifying a heuristic family store for H-class quanta, including family membership, frontier management, deprecation, and retirement rules. Extended retrieval and semantic-index filtering with `heuristic_family_id` and retired-family opt-in behavior, added 3 heuristic-family parameters plus 5 conformance requirements (CR-HFS-1 through CR-HFS-5), and added TV-11 plus glossary entries. Agent: Inanna.

### v2.0.3 â€” T-087 Bundle Compaction Engine (2026-03-12)

Added Section 5.4.4 specifying a lossless Bundle Compaction Engine for archived knowledge bundles. BCE compacts related cold-tier records using chunked manifests and exact reconstruction checks, integrates with archive retention so non-perpetual records compact before any final summary reduction, and adds 4 bundle-compaction parameters plus 5 conformance requirements (CR-38 through CR-42). Agent: Ninsubur.

### v2.0.2 â€” T-080 Four-Tier Memory Model (2026-03-12)

Added Section 4.6 formalizing the four-tier memory model (Working/Short-term/Long-term/Archival) deferred by C3 Â§1.2. Tier assignment is a derived property computed from lifecycle state (Â§4.3) and coherence graph edge tiers (Â§7.3.1), with Archival mapped to the Archive Layer (Â§5.4.3). Added 5 conformance requirements (CR-MTM-1 through CR-MTM-5) in Appendix E.7, 5 glossary entries. Agent: Enki.

---

*End of document.*
