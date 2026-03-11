# Epistemic Metabolism Architecture (EMA)

## Master Technical Specification — C6

**Version:** 1.0.0
**Date:** 2026-03-10
**Invention ID:** C6
**Status:** MASTER TECH SPEC (Final Deliverable)
**Assessment Scores:** Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10 (MEDIUM-HIGH)
**Normative References:** RFC 2119, JSON Schema Draft 2020-12, Josang Subjective Logic (2016), W3C PROV-DM (2013), Dung Bipolar Argumentation (1995), RFC 3339, UUID v7 (RFC 9562), Gentner Structure-Mapping Theory (1983), Lotka-Volterra Competitive Equations (1926/1931), Hardin Competitive Exclusion Principle (1960)

---

## Abstract

The Epistemic Metabolism Architecture (EMA) is a knowledge lifecycle engine that treats verified knowledge as a living metabolic process rather than a stored asset. It replaces the underspecified Knowledge Cortex in the Atrahasis coordination stack with a formally defined system in which knowledge units -- epistemic quanta -- are ingested from a verification layer, circulated through a typed coherence graph, consolidated via LLM-driven dreaming with verification gating, and dissolved when they lose credibility or relevance. A five-signal regulatory system called SHREC governs metabolic rates through ecological budget competition modeled on Lotka-Volterra dynamics, with PID safety overlay and constitutional floor guarantees. Bounded-loss projection functions allow three upstream subsystems to view canonical quanta in their native ontological formats with measurable fidelity guarantees.

EMA sits between the Proof Chain Verification Machine (PCVM, C5) and the Settlement Plane in the Atrahasis stack. It is the canonical store of all verified knowledge in the system. No subsystem stores knowledge independently; all subsystem-local knowledge is a projection of the canonical epistemic quantum held by EMA.

This document is the self-contained Master Technical Specification for EMA. It synthesizes the full design and specification pipeline into a single whitepaper that a technically sophisticated reader can understand without reference to any other Atrahasis document.

---

## Table of Contents

1. [Introduction and Motivation](#1-introduction-and-motivation)
2. [Background and Related Work](#2-background-and-related-work)
3. [Architectural Overview](#3-architectural-overview)
4. [The Epistemic Quantum](#4-the-epistemic-quantum)
5. [Metabolic Processes](#5-metabolic-processes)
6. [SHREC Regulatory System](#6-shrec-regulatory-system)
7. [Coherence Graph](#7-coherence-graph)
8. [Projection Engine](#8-projection-engine)
9. [Retrieval Interface](#9-retrieval-interface)
10. [Integration Architecture](#10-integration-architecture)
11. [Security Analysis](#11-security-analysis)
12. [Scalability Analysis](#12-scalability-analysis)
13. [Open Design Questions](#13-open-design-questions)
14. [Conclusion](#14-conclusion)

**Appendices:**
- [A. Complete Epistemic Quantum JSON Schema](#appendix-a-complete-epistemic-quantum-json-schema)
- [B. SHREC Signal Computation Functions](#appendix-b-shrec-signal-computation-functions)
- [C. Lotka-Volterra Equations and Stability Conditions](#appendix-c-lotka-volterra-equations-and-stability-conditions)
- [D. Configurable Parameters Table](#appendix-d-configurable-parameters-table)
- [E. Conformance Requirements](#appendix-e-conformance-requirements)
- [F. Test Vectors](#appendix-f-test-vectors)
- [G. Traceability Matrix](#appendix-g-traceability-matrix)
- [H. Glossary](#appendix-h-glossary)

---

## 1. Introduction and Motivation

### 1.1 Why Static Knowledge Systems Fail for Planetary AI

Multi-agent AI coordination at planetary scale generates knowledge that is inherently dynamic. Agents produce claims, revise them, contradict each other, discover cross-domain patterns, and render previous knowledge obsolete -- continuously, across thousands of concurrent processes. Traditional knowledge management systems -- relational databases, knowledge graphs, vector stores, retrieval-augmented generation pipelines -- treat knowledge as a stored asset. They provide CRUD operations: create, read, update, delete. This model fails for three reasons.

First, knowledge has a lifecycle that CRUD does not capture. A claim enters the system with high uncertainty, accumulates evidence over time, may be contradicted, may be consolidated with other claims into a higher-order principle, and may eventually become obsolete. A knowledge graph node is either present or absent. An epistemic quantum has vitality, metabolic state, coherence relationships, and a trajectory through time.

Second, knowledge consolidation cannot be reduced to deduplication or summarization. When agents across different domains independently discover related patterns, the system should identify and synthesize those patterns into new knowledge. This is not a database operation. It is an act of reasoning that requires diversity verification, multi-pass synthesis, and independent verification of the result.

Third, resource allocation for knowledge processing is itself a regulation problem. How much computational budget should the system spend on ingesting new knowledge versus consolidating existing knowledge versus detecting contradictions versus removing stale claims? This question has no static answer. It depends on the current state of the knowledge base, the rate of new input, the density of cross-domain opportunities, and the threat of adversarial manipulation. A static system cannot self-regulate.

### 1.2 The Metabolic Alternative

EMA models knowledge processing as a metabolic system. This is not a decorative metaphor -- it is a structural analogy that generates specific architectural predictions.

**Anabolism** (building up) corresponds to ingestion and consolidation: new knowledge enters the system, is verified, and is synthesized into higher-order structures. **Catabolism** (breaking down) corresponds to decay and dissolution: stale, contradicted, or obsolete knowledge is quarantined and eventually dissolved, with useful components recycled. **Homeostasis** corresponds to SHREC regulation: five competing metabolic signals allocate budget to maintain system health across operating regimes.

The metabolic framing produces predictions that a static architecture would not:

1. **Knowledge has vitality.** Like biological organisms, knowledge units have a composite health score that depends on evidential support, access recency, credibility, and coherence. Vitality determines lifecycle transitions.

2. **Knowledge circulates.** Knowledge is not merely stored and retrieved. It flows through the coherence graph, strengthening connections with co-accessed knowledge (Hebbian reinforcement) and weakening connections with neglected knowledge.

3. **Knowledge consolidates during "dreaming."** Scheduled synthesis processes identify clusters of related quanta and produce higher-order principles. This is the anabolic process that generates novel knowledge from existing substrate.

4. **Knowledge dissolves with component recycling.** When knowledge loses vitality, its components (evidence, provenance) are redistributed to surviving knowledge before the shell is dissolved. This preserves the epistemic record.

5. **The system self-regulates.** Five competing signals govern resource allocation through ecological dynamics. No static configuration is needed; the system adapts to changing knowledge loads.

### 1.3 What EMA Replaces

The Atrahasis coordination stack originally specified a "Knowledge Cortex" as its knowledge layer. The Knowledge Cortex was underspecified:

| Knowledge Cortex (deprecated) | EMA (replacement) |
|-------------------------------|-------------------|
| Unspecified "durable memory" | Epistemic quanta with formal 10-tuple schema |
| No lifecycle management | 5-state lifecycle: ACTIVE, CONSOLIDATING, DECAYING, QUARANTINED, DISSOLVED |
| Static storage | Dynamic coherence graph with typed edges and metabolic dynamics |
| No consolidation capability | Dreaming pipeline with LLM synthesis and PCVM verification gate |
| No knowledge retirement | Catabolism engine with vitality-based dissolution and component recycling |
| No regulatory system | SHREC: 5-signal ecological competition with PID overlay |
| Single view | Bounded-loss projections for C3, C4, C5 |
| Query-only retrieval | Push-based circulation + context-aware pull retrieval |

---

## 2. Background and Related Work

### 2.1 Knowledge Management Systems

**Knowledge graphs** (Wikidata, Google Knowledge Graph, enterprise KGs) represent knowledge as entity-relationship triples. They provide structured query, inference, and ontology management. They do not provide lifecycle management, autonomous consolidation, or self-regulation. Knowledge graph entries persist until manually updated or deleted.

**Vector databases** (Pinecone, Weaviate, Milvus) enable semantic similarity search over embedded documents. They are retrieval-optimized but have no knowledge lifecycle, no typed relationships, no consolidation, and no regulatory system. Vector similarity is a retrieval heuristic, not an epistemic relationship.

**Retrieval-augmented generation (RAG)** (Lewis et al. 2020, Gao et al. 2024) augments LLM responses with retrieved context. RAG is a query-time technique. It does not manage the lifecycle of the documents it retrieves, does not consolidate knowledge across retrieval sessions, and does not self-regulate retrieval scope.

### 2.2 AI Memory Systems

**MemGPT** (Packer et al. 2023) introduces hierarchical memory management for LLMs with main context and archival storage. It manages context windows but does not implement knowledge lifecycle, consolidation, or multi-agent coherence.

**Mem0** provides a persistent memory layer for AI applications with user-specific memory, but operates at the application level without knowledge graphs, verification, or consolidation.

**MemOS** (Hu et al. 2025) is the closest prior art. It proposes an operating system for LLM memory with lifecycle management (creation, activation, consolidation, hibernation, deletion). MemOS addresses the lifecycle dimension but lacks: (a) ecological self-regulation (SHREC), (b) verification-gated consolidation (dreaming + PCVM), (c) multi-ontology projections, (d) typed coherence graphs with Hebbian dynamics. EMA builds on the lifecycle insight while adding the regulatory, consolidation, and projection layers that MemOS does not specify.

### 2.3 Knowledge Consolidation

**Automated theory formation** (Lenat's AM, 1977; Colton's HR, 2002) generates mathematical conjectures from examples. These systems operate in narrow formal domains and do not scale to multi-domain, multi-agent knowledge.

**Ontology learning** (Cimiano et al. 2005) extracts ontological structures from text. It is a knowledge extraction technique, not a consolidation architecture.

**LLM-based synthesis** (recent work on chain-of-thought, self-consistency, tree-of-thoughts) demonstrates that LLMs can identify cross-domain patterns. EMA's dreaming pipeline leverages this capability but adds provenance diversity requirements, majority voting across independent passes, and verification gating through PCVM.

### 2.4 Biological Metabolism as Architectural Inspiration

The metabolic analogy is structural, not decorative. Biological metabolism provides:

- **Anabolic/catabolic balance:** The ratio of knowledge building to knowledge dissolution is a measurable system property, analogous to the anabolic/catabolic ratio in biological systems.
- **Homeostatic regulation:** Biological homeostasis maintains internal conditions despite external perturbation. SHREC implements this through five competing signals with PID safety overlay.
- **Self/non-self discrimination:** The immune system distinguishes self (structural knowledge) from non-self (foreign or corrupted knowledge). EMA's structural protection and immune self-audit implement this principle.
- **Hebbian strengthening:** Neurons that fire together wire together. EMA's edge weight dynamics strengthen connections between co-accessed quanta.

### 2.5 The Atrahasis Coordination Stack

EMA operates within the Atrahasis Agent System, a multi-layer coordination architecture for planetary-scale AI. The relevant layers are:

- **Tidal Noosphere (C3):** Provides spatial coordination through loci and parcels, temporal coordination through tidal epochs, and governance through VRF committees. EMA receives epoch boundaries and parcel topology from C3.
- **ASV/AASL (C4):** Provides the structured communication vocabulary for agent messages. Claims arriving at EMA follow the CLM-CNF-EVD-PRV-VRF token chain defined by ASV.
- **PCVM (C5):** Provides verification of all claims through the Proof Chain Verification Machine. Every knowledge unit entering EMA must carry a Membrane Clearance Token (MCT) from PCVM. EMA submits its own consolidation outputs back to PCVM as C-class claims.

---

## 3. Architectural Overview

### 3.1 Stack Position

```
CIOS (orchestration)
    |
    v
Tidal Noosphere (coordination) -- C3
    |  Provides: locus/parcel topology, tidal epochs, VRF committees,
    |  stigmergic signals, governance operations
    |
    v
PCVM (verification) -- C5
    |  Provides: MCTs, VTDs, claim classification (8 classes),
    |  credibility opinions (b/d/u/a), adversarial probing, BDL admission
    |
    v
EMA (knowledge metabolism) -- C6  <-- THIS DOCUMENT
    |  Provides: epistemic quantum lifecycle, coherence graph,
    |  dreaming consolidation, SHREC regulation, multi-system
    |  projections, knowledge retrieval API
    |
    v
Settlement Plane (AIC economy)
    |  Provides: verification rewards, knowledge utility scoring,
    |  metabolic efficiency incentives
```

### 3.2 Design Principles

**Principle 1: Canonical Source.** The epistemic quantum stored in EMA is always the canonical representation of a piece of knowledge. All subsystem-local copies are projections. When projections and canonical representations conflict, the canonical version governs.

**Principle 2: Verification Gate.** No quantum enters ACTIVE state without passing through PCVM verification. This applies to initial ingestion, consolidation outputs, and any update that crosses class-specific credibility thresholds.

**Principle 3: Metabolic Ordering.** Within each epoch, metabolic phases execute in strict order: Ingestion, Circulation, Consolidation, Catabolism, Regulation. No phase begins until its predecessor completes for the current epoch.

**Principle 4: Bounded Information Loss.** Projections explicitly lose information. The loss is measured (round-trip fidelity), bounded (minimum fidelity targets), and flagged (high-confidence canonical warnings). Information loss is a design choice, not a bug.

**Principle 5: Constitutional Protection.** Core parameters (catabolism thresholds, SHREC floor allocations, consolidation diversity requirements) are constitutionally protected. Changes require governance-class consensus through C3.

### 3.3 Formal Invariants

- **INV-E1 (Canonical Source):** The EMA quantum is always the canonical representation. Projections are derived views. On conflict, canonical governs unless the projected update carries PCVM verification.
- **INV-E2 (PCVM Gate):** No quantum enters ACTIVE state without PCVM verification.
- **INV-E3 (Metabolic Ordering):** Phases execute in strict order within each epoch.
- **INV-E4 (Consolidation Lock):** A CONSOLIDATING quantum MUST NOT transition to DECAYING, QUARANTINED, or DISSOLVED. Locks have bounded TTL.
- **INV-E5 (Dissolution Irreversibility):** DISSOLVED is a terminal state. Recovery requires creating a new quantum.
- **INV-E6 (Edge Budget):** No quantum may exceed MAX_EDGES_PER_QUANTUM edges. No shard may exceed MAX_EDGES_PER_SHARD total edges.
- **INV-E7 (SHREC Floor):** Budget allocation for each signal MUST NOT fall below its configured floor allocation.
- **INV-E8 (Projection Fidelity):** Each projection function must maintain round-trip fidelity above its configured target.
- **INV-E9 (Provenance Completeness):** Every quantum must have a complete W3C PROV provenance record. No gaps.
- **INV-E10 (Single-Agent Contradiction Cap):** Total contradiction weight from any single agent to any target quantum MUST NOT exceed 0.3.

### 3.4 Component Map

EMA comprises nine components:

1. **Quantum Engine:** Creates, stores, and manages the lifecycle of epistemic quanta.
2. **Ingestion Pipeline:** Receives PCVM-verified claims and decomposes them into quanta with initial edges.
3. **Coherence Graph:** Maintains the typed edge network connecting quanta. Provides graph operations for circulation, consolidation, vitality computation, and contradiction detection.
4. **Circulation Engine:** Pushes relevant quanta to subscribing agents based on subscription profiles.
5. **Consolidation Engine (Dreaming):** Discovers cross-domain patterns through LLM synthesis with provenance diversity verification and PCVM gating.
6. **Catabolism Engine:** Controlled dissolution of quanta that have lost vitality, with component recycling and structural protection.
7. **SHREC Controller:** Five-signal ecological competition with PID safety overlay for resource allocation.
8. **Projection Engine:** Translates quanta into C3/C4/C5 native views with bounded, measured information loss.
9. **Retrieval Interface:** Context-aware knowledge retrieval supporting semantic, structural, temporal, and metabolic-state queries.

### 3.5 The Metabolic Cycle

Each tidal epoch (aligned with C3's temporal structure) executes five metabolic phases:

```
EPOCH(t):
  Phase 1 -- INGESTION    [t, t + 0.2)   New quanta validated, decomposed, inserted
  Phase 2 -- CIRCULATION  [t + 0.2, t + 0.4)  Active quanta pushed to subscribers
  Phase 3 -- CONSOLIDATION [t + 0.4, t + 0.6)  Dreaming engine runs if triggered
  Phase 4 -- CATABOLISM   [t + 0.6, t + 0.8)  Dissolution criteria evaluated
  Phase 5 -- REGULATION   [t + 0.8, t + 1.0)  SHREC computes signals, adjusts budget
```

Phase boundaries are logical, not wall-clock. Each phase completes when its processing queue is drained or its budget allocation is exhausted. The fractional notation indicates ordering, not proportional time allocation.

---

## 4. The Epistemic Quantum

### 4.1 Definition and Rationale

The epistemic quantum is the fundamental unit of knowledge in EMA. It is a self-describing 10-tuple that carries its own content, confidence, provenance, coherence relationships, metabolic state, and projection views.

The term "quantum" is deliberate: like a physical quantum, an epistemic quantum is the smallest indivisible unit of knowledge that retains full epistemic context. Unlike a knowledge graph triple (subject-predicate-object) which carries no confidence, provenance, or lifecycle information, an epistemic quantum is a complete epistemic object.

**The 10-Tuple:**

```
EpistemicQuantum:
    id:                 URI                    // globally unique: eq:<locus>:<epoch>:<uuid7>
    content:            TypedContent           // claim text + type + domain tags + evidence
    opinion:            SubjectiveLogicOpinion // (belief, disbelief, uncertainty, base_rate)
    provenance:         W3C_PROV_Record        // generating agent, method, sources, timestamps
    edges:              List<EpistemicEdge>     // typed edges: SUPPORT, CONTRADICTION, etc.
    metabolic_state:    MetabolicState         // phase + vitality + consolidation lock
    projections:        ProjectionCache        // cached C3, C4, C5 views
    timestamps:         TemporalRecord         // created, last_circulated, last_verified, etc.
    dissolution_record: Optional<DissolutionRecord>  // if dissolved: why, what was recycled
    claim_class:        ClaimClass             // D|E|S|H|N|P|R|C (from PCVM taxonomy)
```

### 4.2 Subjective Logic Opinions

Every quantum carries a Subjective Logic opinion tuple w = (b, d, u, a):

- **b (belief):** Evidence supporting the claim. Range [0, 1].
- **d (disbelief):** Evidence against the claim. Range [0, 1].
- **u (uncertainty):** Lack of evidence. Range [0, 1].
- **a (base rate):** Prior probability absent evidence. Range [0, 1].
- **Constraint:** b + d + u = 1.

The **expected probability** (credibility score): E(w) = b + a * u.

This representation is superior to scalar confidence for multi-agent systems because it distinguishes between "I believe this strongly based on evidence" (high b, low u) and "I believe this tentatively due to lack of counter-evidence" (moderate b, high u). Two agents can agree on expected probability while having very different uncertainty profiles.

**Key operations** (per Josang 2016):
- **Cumulative fusion:** Combines independent opinions from multiple sources.
- **Discounting:** Weights one opinion by trust in its source.
- **Conjunction:** Combines opinions about dependent propositions.

Implementations MUST use the full Josang multinomial formulas. Simplified forms in this document are for exposition only.

### 4.3 Lifecycle State Machine

```
                    +----------------------------------+
                    |                                  |
                    v                                  | (consolidation completes
              +----------+                             |  or lock TTL expires)
   Ingestion  |          |  consolidation lock         |
   ---------> |  ACTIVE  | ----------------------> +--------------+
              |          |                         | CONSOLIDATING |
              +----------+ <---------------------- +--------------+
                    |
                    | vitality < decay_threshold
                    | OR temporal_expiry
                    v
              +----------+
              | DECAYING  |
              +----------+
                    |
                    | vitality < quarantine_threshold
                    | OR decay_timeout
                    v
              +--------------+    rescue by dreaming
              | QUARANTINED  | -----------------------> ACTIVE
              +--------------+
                    |
                    | quarantine_timeout
                    | OR manual dissolution
                    v
              +----------+
              | DISSOLVED |  (terminal state, INV-E5)
              +----------+
```

**Transition Rules:**

| From | To | Trigger | Guard |
|------|----|---------|-------|
| (external) | ACTIVE | Ingestion + PCVM verification | MCT valid, claim_class assigned |
| ACTIVE | CONSOLIDATING | Consolidation lock acquired | Lock TTL set, dreaming session active |
| CONSOLIDATING | ACTIVE | Consolidation complete or lock TTL expires | Lock released |
| ACTIVE | DECAYING | vitality < DECAY_THRESHOLD (0.30) | NOT in CONSOLIDATING state |
| DECAYING | ACTIVE | vitality recovers above DECAY_THRESHOLD | New supporting evidence |
| DECAYING | QUARANTINED | vitality < QUARANTINE_THRESHOLD (0.15) OR decay > MAX_DECAY_EPOCHS | NOT in CONSOLIDATING state |
| QUARANTINED | ACTIVE | Dreaming rescue, manual rescue, or new strong evidence | citation_count > 0 or explicit rescue |
| QUARANTINED | DISSOLVED | Quarantine > MAX_QUARANTINE_EPOCHS (100) OR manual dissolution | Recycling completed |
| DISSOLVED | (none) | Terminal | INV-E5 |

### 4.4 Vitality Computation

Vitality is a composite health score determining metabolic state transitions:

```python
def compute_vitality(q: EpistemicQuantum, epoch: EpochNum) -> float:
    # 1. Base decay: exponential decay from creation
    age_epochs = epoch - q.provenance.generation_epoch
    base_decay = math.exp(-BASE_DECAY_RATE * age_epochs)  # default: 0.005

    # 2. Access recency: boost for recent access
    if q.timestamps.last_accessed is not None:
        epochs_since_access = epoch - epoch_of(q.timestamps.last_accessed)
        access_recency = math.exp(-ACCESS_DECAY_RATE * epochs_since_access)  # default: 0.02
    else:
        access_recency = 0.5

    # 3. Support factor: boosted by support edges
    support_weights = [e.weight for e in q.edges if e.edge_type == "SUPPORT"]
    support_factor = min(1.0, 0.5 + sum(support_weights) * SUPPORT_VITALITY_FACTOR)

    # 4. Contradiction factor: reduced by contradiction edges (per-agent cap applied)
    agent_contradictions = {}
    for e in q.edges:
        if e.edge_type == "CONTRADICTION":
            agent = e.creating_agent
            agent_contradictions[agent] = min(
                agent_contradictions.get(agent, 0) + e.weight,
                MAX_AGENT_CONTRADICTION_WEIGHT  # 0.3, INV-E10
            )
    contradiction_factor = min(
        MAX_TOTAL_CONTRADICTION_FACTOR,
        sum(agent_contradictions.values()) * CONTRADICTION_VITALITY_FACTOR
    )

    # 5. Credibility factor
    credibility = q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty

    # 6. Supersession penalty
    superseded_by = [e for e in q.edges
                     if e.edge_type == "SUPERSESSION" and e.target_id != q.id]
    supersession_penalty = (max(e.weight for e in superseded_by) * SUPERSESSION_DECAY_MULTIPLIER
                           if superseded_by else 0.0)

    # Composite (multiplicative -- all factors must be healthy)
    vitality = (base_decay * access_recency * support_factor
                * (1.0 - contradiction_factor) * credibility
                * (1.0 - supersession_penalty))

    return clamp(vitality, 0.0, 1.0)
```

### 4.5 Edge Types

EMA defines five typed epistemic edges:

| Edge Type | Directionality | Weight Semantics | Formal Basis |
|-----------|---------------|------------------|--------------|
| SUPPORT | Directed: A supports B | Evidential support strength [0,1] | Dung bipolar argumentation (support) |
| CONTRADICTION | Mutual: A contradicts B | Severity of conflict [0,1] | Dung abstract argumentation (attack) |
| DERIVATION | Directed: B derived from A | Derivation confidence [0,1] | W3C PROV wasDerivedFrom |
| ANALOGY | Bidirectional: A analogous to B | Structural similarity [0,1] | Gentner structure-mapping theory |
| SUPERSESSION | Directed: B supersedes A | Replacement completeness [0,1] | Temporal versioning |

**Key properties:**
- DERIVATION edges are immutable: they represent provenance facts that MUST NOT be deleted or have weight reduced (CR-24).
- CONTRADICTION edges are mutual: creating A->B automatically creates B->A with the same weight.
- SUPPORT and CONTRADICTION edges are subject to Hebbian reinforcement (co-accessed endpoints strengthen) and temporal decay (unused edges weaken).
- ANALOGY edges are consolidation triggers: clusters connected by high-weight analogy edges are candidates for dreaming.

### 4.6 Example: Quantum Lifecycle

Consider a quantum representing the claim "Protein folding rate for sequence ACGT is 3.2ms under standard conditions."

1. **Ingestion (Epoch 100):** PCVM classifies as D-class (deterministic), assigns opinion (b=0.95, d=0.0, u=0.05, a=0.5). EMA creates quantum with vitality=1.0, state=ACTIVE. Initial edge discovery finds 3 SUPPORT edges from related proteomics quanta.

2. **Circulation (Epoch 101-150):** Quantum is pushed to agents subscribed to biology/proteomics domains. Each delivery increments circulation_count. Co-accessed edges strengthen via Hebbian reinforcement.

3. **Consolidation (Epoch 200):** Dreaming identifies this quantum as part of a cross-domain cluster relating protein folding rates to computational scheduling patterns. After provenance diversity verification (7 agents, 4 parcels), LLM synthesis produces a principle: "Computational timeout settings should scale with molecular complexity." PCVM verifies the C-class claim. A new consolidated quantum is created with DERIVATION edges from the source cluster.

4. **Vitality decline (Epoch 500):** New measurement methods supersede the original 3.2ms figure. A SUPERSESSION edge is created from a newer quantum with updated measurements. The original quantum's vitality declines due to supersession penalty and reduced access recency.

5. **Catabolism (Epoch 600):** Vitality drops below DECAY_THRESHOLD. State transitions to DECAYING. After 50 epochs without recovery, state transitions to QUARANTINED. Because citation_count=15 (above STRUCTURAL_PROTECTION_THRESHOLD=10), the quantum is structurally protected and rescued back to ACTIVE -- its provenance is too important to dissolve.

---

## 5. Metabolic Processes

### 5.1 Phase 1: Ingestion

Ingestion receives PCVM-verified claims and decomposes them into epistemic quanta.

**Input:** For each verified claim:
- `claim`: the verified claim (CLM token from ASV)
- `mct`: Membrane Clearance Token (credibility opinion, class, committee)
- `vtd_ref`: reference to Verification Trace Document in PCVM store
- `bdl`: Base Durability Ledger bundle

**Ingestion Protocol:**

```python
def ingest(claim, mct, vtd_ref, bdl):
    # Step 1: Decompose claim into quantum(s)
    # Most claims map 1:1. Compound claims decompose into atomic sub-claims.
    quanta = decompose_claim(claim, mct)

    for quantum in quanta:
        # Step 2: Map PCVM opinion to quantum opinion
        quantum.opinion = map_pcvm_opinion(mct.opinion)

        # Step 3: Map ASV provenance to W3C PROV
        quantum.provenance = map_asv_to_prov(claim.provenance)

        # Step 4: Set initial metabolic state
        quantum.metabolic_state = MetabolicState(phase="ACTIVE", vitality=1.0)

        # Step 5: Assign claim class
        quantum.claim_class = mct.assigned_class

        # Step 6: Detect initial edges (semantic similarity scan)
        discover_initial_edges(quantum, shard)

        # Step 7: Assign to parcel shard
        shard = assign_shard(quantum, current_parcel_topology())

        # Step 8: Generate initial projections
        quantum.projections = generate_all_projections(quantum)

    # Step 9: Report to SHREC hunger signal
    shrec.report_ingestion(len(quanta))
    return quanta
```

**ASV-to-Quantum Field Mapping:**

| ASV Field | Quantum Field | Mapping |
|-----------|--------------|---------|
| CLM.statement | content.claim_text | Direct |
| CLM.epistemic_class | content.claim_type | Via PCVM assigned_class |
| CNF.value/interval | opinion.belief | CNF confidence -> SL belief |
| EVD[] | edges (DERIVATION) | Each evidence source creates derivation edge |
| PRV | provenance | Direct mapping to W3C PROV |
| VRF | content.source_mct_id | Captured in MCT reference |

**Claim Class to Claim Type Mapping:**

| PCVM Class | EMA Type | Rationale |
|-----------|---------|-----------|
| D (Deterministic) | observation | Computation results are observations |
| E (Empirical) | observation | Direct mapping |
| S (Statistical) | inference | Statistical conclusions are inferred |
| H (Heuristic) | inference | Heuristic judgments are inferred |
| N (Normative) | governance | Normative claims are governance rules |
| P (Process) | observation | Process compliance is observed |
| R (Reasoning) | inference | Reasoning produces inferences |
| C (Consolidation) | consolidation | From dreaming |

**Initial Edge Discovery:**

```python
def discover_initial_edges(q, shard):
    # Compute embedding for new quantum
    q_embedding = compute_embedding(q.content.claim_text)

    # Find domain tag neighbors in shard
    tag_neighbors = shard.domain_tag_index.lookup(q.content.domain_tags)

    # Score by cosine similarity
    scored = []
    for neighbor_id in tag_neighbors:
        neighbor = shard.nodes[neighbor_id]
        similarity = cosine_similarity(q_embedding, compute_embedding(neighbor.content.claim_text))
        if abs(similarity) > EDGE_DISCOVERY_THRESHOLD:  # default: 0.4
            scored.append((neighbor_id, similarity))

    # Create edges based on polarity
    for neighbor_id, similarity in sorted(scored, key=abs, reverse=True)[:INITIAL_EDGE_DISCOVERY_K]:
        if similarity > SUPPORT_SIMILARITY_THRESHOLD:     # 0.6
            edge_type = "SUPPORT"
        elif similarity < -CONTRADICTION_SIMILARITY_THRESHOLD:  # -0.6
            edge_type = "CONTRADICTION"
        else:
            edge_type = "ANALOGY"
        create_edge(q, neighbor_id, edge_type, weight=abs(similarity))
```

### 5.2 Phase 2: Circulation

Circulation pushes relevant quanta to subscribing agents. It implements a push model regulated by SHREC.

**Subscription Model:**

Agents subscribe with filters on domain tags, claim classes, minimum credibility, minimum vitality, and notification mode (batch, priority, or digest). Each subscription has a rate limit (max_per_epoch).

**Circulation Protocol:**

```python
def execute_circulation(epoch, budget):
    # 1. Identify eligible quanta (newly created, recently updated, high-vitality)
    eligible = [q for q in all_active_quanta()
                if should_circulate(q, epoch)]

    # 2. Sort by circulation priority
    eligible.sort(key=lambda q: circulation_priority(q, epoch), reverse=True)

    # 3. Match to subscribers, compute relevance
    for q in eligible:
        if budget <= 0: break
        for sub in find_matching_subscriptions(q):
            relevance = compute_relevance(q, sub)
            if relevance > 0.3:
                deliver(q, sub)
                q.timestamps.last_circulated = current_timestamp()
                q.metabolic_state.circulation_count += 1
                budget -= DELIVERY_COST

    # 4. Priority push for contradictions and supersessions
    for q in quanta_with_new_contradictions_or_supersessions(epoch):
        for sub in find_affected_subscribers(q):
            priority_deliver(q, sub)

    # 5. Report to SHREC
    shrec.report_circulation(total_deliveries)
```

**Relevance Ranking:**

```
relevance = 0.30 * domain_score     // domain tag match
           + 0.20 * opinion_score   // belief strength
           + 0.15 * recency_score   // creation/modification recency
           + 0.15 * vitality_score  // metabolic health
           + 0.20 * novelty_score   // unseen by subscriber
```

**Edge Weight Dynamics (during circulation):**

Edges are updated via Hebbian reinforcement:
- When both endpoint quanta are accessed in the same epoch, edge weight increases by `REINFORCEMENT_RATE * (1 - current_weight)` (default: 0.05).
- Edges not reinforced decay by `EDGE_DECAY_RATE * current_weight` per epoch (default: 0.02).
- Edges below MIN_EDGE_WEIGHT (0.05) are pruned, except DERIVATION edges which are immutable.
- Edge TTL: 50 epochs without reinforcement triggers pruning.

### 5.3 Phase 3: Consolidation (Dreaming)

Consolidation is EMA's most novel and highest-risk component. It discovers cross-domain patterns through scheduled LLM reasoning, produces C-class claims, and submits them to PCVM for verification.

**Dreaming Schedule:** Consolidation runs every N epochs (default N=10), during the consolidation phase of the metabolic cycle.

#### 5.3.1 Candidate Identification

```python
def identify_consolidation_candidates(shard, epoch):
    # 1. Find dense subgraphs via mutual support edge detection
    active_quanta = [q for q in shard.nodes.values()
                     if q.metabolic_state.phase == "ACTIVE"
                     and q.metabolic_state.consolidation_lock is None]

    # 2. Build support adjacency for active quanta
    support_adj = build_support_adjacency(active_quanta, shard,
                                          min_weight=CONSOLIDATION_MIN_EDGE_WEIGHT)

    # 3. Find connected components with >= MIN_CLUSTER_SIZE (5) nodes
    # and >= MIN_MUTUAL_SUPPORT_EDGES (3) mutual support edges
    candidates = find_dense_components(support_adj, active_quanta)

    # 4. Also detect cross-domain bridges for cross-shard consolidation
    bridges = detect_cross_domain_bridges(shard)
    for bridge in bridges[:10]:
        neighborhood = shard.neighborhood(
            centers=[bridge.quantum_a.id, bridge.quantum_b.id],
            radius=2, max_quanta=30)
        candidates.append(CandidateSet(quanta=neighborhood))

    return candidates[:MAX_CONSOLIDATION_CANDIDATES_PER_EPOCH]
```

#### 5.3.2 Provenance Diversity Verification

Every consolidation candidate MUST pass provenance diversity checks to prevent consolidation poisoning (Adversarial A3, CRITICAL):

```python
def verify_provenance_diversity(candidate):
    quanta = candidate.quanta

    # Requirement 1: >= 5 independent generating agents
    agents = unique(q.provenance.generating_agent for q in quanta)
    if len(agents) < MIN_INDEPENDENT_AGENTS:  # 5
        return REJECT("Insufficient agent diversity")

    # Requirement 2: >= 3 independent parcels
    parcels = unique(resolve_parcel(q) for q in quanta)
    if len(parcels) < MIN_INDEPENDENT_PARCELS:  # 3
        return REJECT("Insufficient parcel diversity")

    # Requirement 3: No agent contributes > 30% of inputs
    max_fraction = max(count_by_agent.values()) / len(quanta)
    if max_fraction > 0.30:
        return REJECT("Single agent dominance")

    # Requirement 4: No shared short derivation chains dominate
    clusters = cluster_by_derivation(quanta, max_chain_length=3)
    if max(len(c) for c in clusters) / len(quanta) > 0.40:
        return REJECT("Derivation cluster dominance")

    return ACCEPT
```

#### 5.3.3 Consolidation Lock Protocol

Before synthesis begins, all candidate quanta are atomically locked (INV-E4):

```python
def acquire_consolidation_locks(candidate, session_id, epoch):
    # Pre-check: all quanta must be ACTIVE with no existing lock
    for q in candidate.quanta:
        if q.metabolic_state.phase != "ACTIVE":
            return FAILURE
        if q.metabolic_state.consolidation_lock is not None:
            return FAILURE

    # Atomic lock acquisition (all or nothing)
    lock = ConsolidationLock(
        session_id=session_id,
        lock_epoch=epoch,
        lock_ttl_epochs=CONSOLIDATION_LOCK_TTL  # default: 5
    )
    for q in candidate.quanta:
        q.metabolic_state.phase = "CONSOLIDATING"
        q.metabolic_state.consolidation_lock = lock

    return SUCCESS
```

#### 5.3.4 Three-Pass LLM Synthesis

```python
def execute_llm_synthesis(candidate, session_id):
    context = prepare_synthesis_context(candidate.quanta)

    # Pass 0: Inductive generalization
    # "What general principle connects these observations?"
    result_0 = llm_inference(prompt_inductive(context),
                             temperature=SYNTHESIS_TEMPERATURE, max_tokens=2048)

    # Pass 1: Cross-domain pattern detection
    # "What structural analogy exists between these domains?"
    result_1 = llm_inference(prompt_analogy(context),
                             temperature=SYNTHESIS_TEMPERATURE, max_tokens=2048)

    # Pass 2: Predictive synthesis
    # "What prediction follows from combining these claims?"
    result_2 = llm_inference(prompt_predictive(context),
                             temperature=SYNTHESIS_TEMPERATURE, max_tokens=2048)

    # Majority voting: retain claims appearing in >= 2 of 3 passes
    all_claims = parse_all([result_0, result_1, result_2])
    clusters = cluster_by_similarity(all_claims, threshold=0.8)
    confirmed = [select_representative(c) for c in clusters
                 if count_distinct_passes(c) >= MAJORITY_THRESHOLD]  # 2

    # Filter: no semantic duplicates of existing active quanta
    return [c for c in confirmed if not is_duplicate(c, candidate.shard)]
```

#### 5.3.5 PCVM Verification Gate

Each confirmed pattern is packaged as a C-class Verification Trace Document and submitted to PCVM:

```python
def submit_to_pcvm(claims, candidate):
    for claim in claims:
        vtd = construct_c_class_vtd(
            claim_text=claim.text,
            source_quanta=candidate.quanta,
            synthesis_reasoning=claim.reasoning,
            falsification_statement=claim.falsification
        )

        # C-class claims start with high uncertainty (>= 0.4)
        vtd.initial_opinion = compute_initial_consolidation_opinion(
            claim, candidate.quanta)  # uncertainty >= 0.4

        result = pcvm.submit_for_verification(vtd)

        if result.admitted:
            # Ingest verified consolidation as new quantum
            new_quantum = ingest(result.claim, result.mct, result.vtd_ref, result.bdl)
            # Create DERIVATION edges from all source quanta
            for source_q in candidate.quanta:
                create_edge(source_q, new_quantum, "DERIVATION", weight=1.0)
                source_q.citation_count += 1
        else:
            # Log rejection, apply cooldown
            handle_consolidation_failure(candidate, session_id, result.rejection_reason)

    # Release all consolidation locks
    release_consolidation_locks(session_id)
```

#### 5.3.6 Aging Uncertainty for C-Class Claims

Consolidated claims without empirical validation are subject to aging uncertainty increase (per Adversarial A2):

```python
def age_unvalidated_consolidations(epoch):
    for q in all_active_quanta():
        if q.claim_class != "C" or q.content.claim_type != "consolidation":
            continue

        age = epoch - q.provenance.generation_epoch

        # Check for confirming or disconfirming evidence since creation
        has_evidence = any(
            e.edge_type in ("SUPPORT", "CONTRADICTION")
            and epoch_of(e.created_at) > q.provenance.generation_epoch
            and e.creating_agent != q.provenance.generating_agent
            for e in q.edges)

        if not has_evidence and age > CCLASS_VALIDATION_WINDOW:  # 50 epochs
            periods = (age - CCLASS_VALIDATION_WINDOW) // CCLASS_VALIDATION_WINDOW
            uncertainty_increase = periods * CCLASS_AGING_UNCERTAINTY_RATE  # 0.1
            # Shift belief mass to uncertainty
            q.opinion.uncertainty = min(0.95, q.opinion.uncertainty + uncertainty_increase)
            q.opinion.belief = max(0.01, q.opinion.belief - uncertainty_increase)
            normalize_opinion(q.opinion)
```

### 5.4 Phase 4: Catabolism

Catabolism is the controlled dissolution of quanta that have lost relevance, credibility, or temporal validity.

#### 5.4.1 Dissolution Criteria

A quantum becomes a catabolism candidate when ANY of the following hold:

| Criterion | Threshold | Detection |
|-----------|-----------|-----------|
| Low credibility AND old | E(w) < 0.3 AND age > 100 epochs | Opinion + age check |
| Expired temporal validity | valid_until < current_epoch | Temporal expiry check |
| Superseded | SUPERSESSION edge weight = 1.0 and superseder has higher credibility + 0.1 margin | Edge check |
| Sustained low vitality | vitality < 0.15 | Vitality computation |

#### 5.4.2 Structural Protection (Self/Non-Self Discrimination)

Quanta with high citation counts are immune to catabolism, analogous to self/non-self discrimination in biological immune systems:

```python
def is_structurally_protected(q):
    # Primary protection: citation count
    if q.citation_count >= STRUCTURAL_PROTECTION_THRESHOLD:  # 10
        return True
    # Secondary protection: keystone detection
    # Removal would disconnect > 5 other quanta from coherence graph
    if is_keystone(q):
        return True
    return False
```

#### 5.4.3 Two-Phase Dissolution

Catabolism is two-phase: quarantine (reversible) then dissolution (irreversible).

**Quarantine:** The quantum is removed from active circulation but remains in the coherence graph with edges preserved. A full snapshot is stored for potential rescue. Quarantine period: MAX_QUARANTINE_EPOCHS (100).

**Dissolution:** After quarantine timeout, components are recycled:

```python
def execute_dissolution(q, reason):
    # 1. Recycle evidence to surviving quanta with domain overlap
    recycling_result = execute_recycling(q)

    # 2. Create permanent dissolution record
    q.dissolution_record = DissolutionRecord(
        reason=reason,
        dissolved_at_epoch=current_epoch(),
        recycled_to=recycling_result.recycled_to,
        eliminated_evidence=recycling_result.eliminated,
        content_hash=sha256(serialize(q.content)),
        final_opinion=copy(q.opinion)
    )

    # 3. Remove edges from coherence graph
    shard = get_shard(q.shard_id)
    for edge in q.edges:
        shard.remove_edge(q.id, edge.target_id)
        # Weaken derivation edges on dependent quanta (source dissolved)
        if edge.edge_type == "DERIVATION":
            dependent = get_quantum(edge.target_id)
            if dependent and dependent.metabolic_state.phase == "ACTIVE":
                weaken_derivation_edge(dependent, q.id)

    # 4. Terminal state transition
    q.metabolic_state.phase = "DISSOLVED"
    q.metabolic_state.vitality = 0.0
    q.content = None  # Content preserved only via content_hash
```

### 5.5 Phase 5: Regulation (SHREC)

SHREC regulation is covered in detail in Section 6.

---

## 6. SHREC Regulatory System

SHREC (Stratified Homeostatic Regulation with Ecological Competition) is a five-signal regulatory system that governs metabolic resource allocation through ecological budget competition with PID safety overlay.

### 6.1 Signal Definitions

| Signal | What It Measures | Primary Resource | Floor |
|--------|-----------------|------------------|-------|
| Hunger (H) | Unmet knowledge demand, coverage gaps | I/O operations | 5% |
| Consolidation (C) | Cross-domain synthesis opportunity | LLM inference tokens | 5% |
| Stress (S) | System overload, processing backlog | CPU cycles | 10% |
| Immune (I) | Knowledge integrity threats, contradictions | Memory bandwidth | 15% |
| Novelty (N) | Rate of genuinely new knowledge | Graph traversal capacity | 8% |

Total floor: 43%. Competitive pool: 57%.

### 6.2 Signal Computation

```python
class SHRECSignals:
    @staticmethod
    def compute_epistemic_hunger(state, epoch):
        unanswered = state.query_log.count_unanswered(window=20)
        total = state.query_log.count_total(window=20)
        coverage = state.coherence_graph.domain_coverage() / state.domain_registry.count_all()
        hunger = (unanswered / max(1, total)) * 0.6 + (1.0 - coverage) * 0.4
        return clamp(hunger, 0.0, 1.0)

    @staticmethod
    def compute_consolidation_pressure(state, epoch):
        candidates = count_consolidation_candidates(state.coherence_graph)
        staleness = min(1.0, (epoch - state.last_consolidation) / 50)
        pressure = min(1.0, candidates / 10) * 0.5 + staleness * 0.3 + validation_queue_pressure * 0.2
        return clamp(pressure, 0.0, 1.0)

    @staticmethod
    def compute_metabolic_stress(state, epoch):
        ingestion_backlog = state.ingestion_queue.size() / 1000
        delivery_failures = state.circulation_report.failures / max(1, state.circulation_report.attempts)
        edge_pressure = max(0, state.coherence_graph.edge_utilization - 0.8) * 5.0
        stress = ingestion_backlog * 0.3 + delivery_failures * 0.25 + edge_pressure * 0.25 + backpressure * 0.2
        return clamp(stress, 0.0, 1.0)

    @staticmethod
    def compute_immune_response(state, epoch):
        contradiction_density = high_weight_contradictions / max(1, active_count)
        rejection_rate = recent_rejections / max(1, recent_submissions)
        immune = contradiction_density * 0.4 + rejection_rate * 0.35 + fp_rate * 0.25
        return clamp(immune, 0.0, 1.0)

    @staticmethod
    def compute_novelty_signal(state, epoch):
        new_quanta = state.ingestion_log.count_new(window=20)
        new_domains = state.ingestion_log.count_new_domains(window=20)
        novelty_ratio = new_quanta / max(1, new_quanta + reinforcing_quanta)
        novelty = min(1.0, new_quanta / 50) * 0.4 + min(1.0, new_domains / 10) * 0.3 + novelty_ratio * 0.3
        return clamp(novelty, 0.0, 1.0)
```

### 6.3 Budget Computation

The total metabolic budget is derived from measured system throughput:

```
B(t) = measured_throughput_capacity * (1 - BUDGET_SAFETY_MARGIN)
```

Budget is measured system capacity, not an arbitrary knob. The safety margin (default 15%) prevents exceeding capacity.

### 6.4 Ecological Competition (Lotka-Volterra)

The five SHREC signals compete for budget through generalized Lotka-Volterra dynamics:

```
dS_i/dt = r_i * S_i * (1 - sum_j(alpha_ij * S_j / K_i)) + floor_correction_i
```

Where:
- S_i = budget share of signal i
- r_i = intrinsic growth rate (proportional to signal intensity)
- K_i = carrying capacity (maximum useful budget share, default 0.4)
- alpha_ij = competitive coefficient (effect of signal j on signal i)
- floor_correction_i = max(0, floor_i - S_i) * restoration_rate

**Competitive Coefficients (Alpha Matrix):**

```
         HUNGER  CONSOL  STRESS  IMMUNE  NOVELTY
HUNGER    1.0     0.2     0.3     0.1     0.2
CONSOL    0.2     1.0     0.1     0.2     0.3
STRESS    0.3     0.1     1.0     0.2     0.1
IMMUNE    0.1     0.2     0.2     1.0     0.1
NOVELTY   0.2     0.3     0.1     0.1     1.0
```

All off-diagonal products alpha_ij * alpha_ji are in range [0.01, 0.09], well below 1.0, satisfying the coexistence condition.

**Five Independent Resource Dimensions:**

Each signal has a primary resource where it is the dominant consumer, providing niche differentiation required by the competitive exclusion principle:

| Signal | Primary Resource | Why Independent |
|--------|-----------------|-----------------|
| Hunger | I/O operations | Ingestion is I/O-bound |
| Consolidation | LLM inference tokens | Only dreaming uses LLM calls |
| Stress | CPU cycles | Coherence recomputation |
| Immune | Memory bandwidth | Quarantine snapshots, audit scanning |
| Novelty | Graph traversal capacity | Frontier exploration |

### 6.5 Floor Allocation Enforcement

```python
FLOOR_ALLOCATIONS = {
    "IMMUNE": 0.15,        # Knowledge integrity is safety-critical
    "STRESS": 0.10,        # System health must always be monitored
    "NOVELTY": 0.08,       # Prevents stale knowledge base
    "HUNGER": 0.05,        # Minimum circulation guarantee
    "CONSOLIDATION": 0.05, # Minimum dreaming budget
}

def enforce_floors(allocations, total_budget):
    for signal in allocations:
        floor = total_budget * FLOOR_ALLOCATIONS[signal]
        allocations[signal] = max(allocations[signal], floor)
    # Renormalize to total budget
    total = sum(allocations.values())
    if total > total_budget:
        scale = total_budget / total
        allocations = {s: v * scale for s, v in allocations.items()}
        # Re-enforce floors after scaling
        for signal in allocations:
            allocations[signal] = max(allocations[signal],
                                      total_budget * FLOOR_ALLOCATIONS[signal])
    return allocations
```

### 6.6 Statistical Self-Model

SHREC maintains a rolling statistical model for regime detection:

```python
class SignalStatistics:
    def __init__(self, window=100):
        self.history = deque(maxlen=window)
        self.prior_mean = 0.5    # Bayesian cold-start prior
        self.prior_weight = 5.0  # Effective sample count of prior

    def update(self, value):
        self.history.append(value)
        n = len(self.history)
        if n < 10:
            # Bayesian prior dominates
            self.mean = (self.prior_weight * self.prior_mean + n * mean(self.history)) / (self.prior_weight + n)
        else:
            self.mean = mean(self.history)
        self.sigma = max(0.01, std(self.history))

    def z_score(self, value):
        return (value - self.mean) / self.sigma
```

### 6.7 Graduated Control Overlay

SHREC operates in four regimes:

| Regime | Threshold | PID Active | Budget Adjustment |
|--------|-----------|-----------|-------------------|
| NORMAL | All signals < 1.5 sigma | No | Ecological competition only |
| ELEVATED | Any signal 1.5-2.5 sigma | Yes (clamped to +/-10%) | Gentle PID correction |
| CRITICAL | Any signal > 2.5 sigma | Yes (clamped to +/-25%) | Full PID correction |
| CONSTITUTIONAL | System invariant threatened | Yes (unclamped) | Emergency override |

**PID Gains (auto-derived from sigma):**

```
Kp_i = 1.0 / sigma_i
Ki_i = Kp_i / (4 * window)         // window = 100 epochs
Kd_i = Kp_i * (window / 10)
```

**Anti-windup:** Integral term clamped to +/- 2 * sigma_i. On regime downgrade (Critical->Normal), integral resets to zero.

**CUSUM change-point detection:** Detects structural shifts in signal behavior and resets PID integral to prevent windup from historical data that is no longer relevant.

**Regime transition hysteresis:** Upward transitions (NORMAL->ELEVATED) are immediate. Downward transitions (ELEVATED->NORMAL) require REGIME_HYSTERESIS_EPOCHS (5) consecutive epochs at the lower level.

### 6.8 Immune Self-Audit

Periodic audit (every IMMUNE_AUDIT_INTERVAL=50 epochs) that checks whether catabolism is attacking valid knowledge:

```python
def execute_immune_self_audit(state, epoch):
    # Sample 10% of recently quarantined quanta
    sample = random_sample(recently_quarantined, rate=0.10)

    # Check for false positives: quarantined quanta with active support
    false_positives = sum(1 for q in sample
                         if count_active_support_edges(q) >= 2)
    fp_rate = false_positives / max(1, len(sample))

    # Autoimmune alarm: catabolism is over-aggressive
    if fp_rate > AUTOIMMUNE_ALARM_THRESHOLD:  # 0.20
        state.catabolism_threshold_multiplier = 2.0  # Raise thresholds
        sentinel.report_autoimmune_alarm(fp_rate)

    # Under-detection check: sample recently dissolved quanta
    dissolved_sample = random_sample(recently_dissolved, rate=0.10)
    missed = sum(1 for q in dissolved_sample if q.final_opinion.belief > 0.5)
    if missed / max(1, len(dissolved_sample)) > 0.05:
        sentinel.report_catabolism_weaponization_alert()
```

### 6.9 Stability Analysis

**Lyapunov function:**

```
V = sum_i (S_i - S_i* - S_i* * ln(S_i / S_i*))
```

dV/dt < 0 when alpha_ij < K_i/K_j for all i,j. With default parameters (all alpha_ij in [0.1, 0.3] and K_i/K_j ratios near 1.0), this condition holds.

**Jacobian at interior equilibrium:**

```
J_ij = -r_i * S_i* * alpha_ij / K_i    (i != j)
J_ii = -r_i * S_i* / K_i               (diagonal)
```

For the default alpha matrix with weak inter-specific competition, eigenvalues are approximately -r_i * S_i* / K_i (all negative), confirming local asymptotic stability.

**Honest limitation:** This stability analysis is local, not global. The SHREC system has not been validated by simulation across all operating regimes. Hard Gate HG-1 requires simulation under steady-state, spike, loss, shift, compound perturbation, and sustained stress profiles. If any signal reaches zero under normal operation, the Lotka-Volterra model must be replaced with simpler priority-weighted allocation.

---

## 7. Coherence Graph

### 7.1 Structure and Purpose

The coherence graph is the "circulatory system" through which quanta flow. It is a typed, weighted, directed graph where nodes are epistemic quanta and edges are one of five epistemic relationship types.

### 7.2 Sharding Strategy

The coherence graph is partitioned along C3 parcel boundaries:

```
Locus L1
  +-- Shard P1: quanta Q1..Q1000, intra-shard edges
  +-- Shard P2: quanta Q1001..Q2000, intra-shard edges
  +-- Cross-shard index: edges between P1-P2
       (sampled at Tier 2+, not exhaustive)
```

**Shard alignment with C3:** Each locus has exactly one shard. Cross-locus edges are maintained in a cross-shard edge index. When C3 executes a Parcel Transition Protocol (PTP), EMA rebalances quanta across shards at the epoch boundary.

### 7.3 Edge Dynamics

**Hebbian Reinforcement:** When both endpoint quanta are accessed within the same epoch, the edge weight increases:

```
new_weight = weight + REINFORCEMENT_RATE * (1.0 - weight)  // 0.05 default
```

**Temporal Decay:** Edges not reinforced decay each epoch:

```
new_weight = weight * (1.0 - EDGE_DECAY_RATE)  // 0.02 default
```

**Pruning:** Edges below MIN_EDGE_WEIGHT (0.05) are pruned, except DERIVATION edges which are immutable.

**Edge TTL:** 50 epochs without reinforcement triggers pruning.

### 7.4 Active Edge Budget

Each quantum maintains at most MAX_EDGES_PER_QUANTUM (50) active edges. Each shard maintains at most MAX_EDGES_PER_SHARD (500,000) total edges.

**Edge ranking for budget enforcement:**

```python
def enforce_edge_budget(quantum, E_max=50):
    if len(quantum.edges) <= E_max:
        return
    for edge in quantum.edges:
        edge.rank_score = (
            0.4 * edge.weight
            + 0.3 * edge.recency_score
            + 0.2 * edge.type_priority   # CONTRADICTION > SUPPORT > DERIVATION > ANALOGY > SUPERSESSION
            + 0.1 * edge.cross_shard_bonus
        )
    quantum.edges.sort(by=rank_score, descending=True)
    quantum.active_edges = quantum.edges[:E_max]
    quantum.archived_edges = quantum.edges[E_max:]
```

### 7.5 Scale Tiers

| Tier | Quanta | Agents | Coherence Mode | Dreaming Scope |
|------|--------|--------|---------------|----------------|
| T1 (< 100K) | < 100K | 1K | Full coherence, all edges | Global: all quanta eligible |
| T2 (100K-10M) | 100K-10M | 1K-10K | Sharded, sampled cross-shard (10%) | Shard-local: per-parcel |
| T3 (> 10M) | > 10M | 10K-100K | Hierarchical: cluster-level | Cluster representatives only |

### 7.6 Cross-Domain Bridge Detection

Bridge detection identifies consolidation candidates:

```python
def detect_cross_domain_bridges(shard):
    bridges = []
    for quantum in shard.quanta():
        domains = set(quantum.content.domain_tags)
        for edge in quantum.active_edges:
            target_domains = set(get_quantum(edge.target_id).content.domain_tags)
            if domains != target_domains and len(domains & target_domains) == 0:
                bridges.append(BridgeCandidate(
                    quantum_a=quantum, quantum_b=get_quantum(edge.target_id),
                    bridge_strength=edge.weight))
    return sorted(bridges, key=lambda b: b.bridge_strength, reverse=True)
```

---

## 8. Projection Engine

### 8.1 Multi-Ontology Projection Model

Each upstream subsystem sees the same quantum through its own ontological lens. Projections are cached views -- the canonical quantum in EMA is the source of truth (INV-E1).

Information loss in projections is:
- **Controlled:** Each projection function specifies what is preserved and what is lost.
- **Measured:** Round-trip fidelity is computed for each projection.
- **Bounded:** Minimum fidelity targets trigger alarms when violated.
- **Flagged:** High-confidence canonical quanta include a warning flag in projections.

### 8.2 C3 Projection (Tidal Noosphere)

**Fidelity target:** 0.85

**Preserves:** locus assignment, epoch timing, parcel membership, claim text, projected probability (scalar), support/contradiction edge summary, domain tags.

**Loses:** Full Subjective Logic opinion (collapsed to scalar E(w)), uncertainty quantification, evidence array details, metabolic state, analogy and derivation edges outside parcel scope, SHREC signal associations.

**Forward projection:**

```python
def project_to_c3(quantum):
    return C3Projection(
        quantum_id=quantum.id,
        locus=resolve_locus(quantum.content.domain_tags),
        parcel=quantum.shard_id,
        relevance_score=quantum.opinion.belief + quantum.opinion.base_rate * quantum.opinion.uncertainty,
        claim_summary=truncate(quantum.content.claim_text, 200),
        domain_tags=quantum.content.domain_tags,
        edge_summary=EdgeSummary(
            support_count=count_edges(quantum, "SUPPORT"),
            contradiction_count=count_edges(quantum, "CONTRADICTION"),
            total=len(quantum.edges)),
        high_canonical_confidence=(quantum.opinion.belief > 0.8)
    )
```

**Fidelity metric:**

```
fidelity_c3 = 0.5 * text_similarity + 0.3 * opinion_preservation + 0.2 * edge_jaccard
```

### 8.3 C4 Projection (ASV Communication)

**Fidelity target:** 0.88

**Preserves:** Full CLM-CNF-EVD-PRV-VRF chain, full Subjective Logic opinion, epistemic class, claim type, evidence references, provenance agent.

**Loses:** Coherence graph position, metabolic state, vitality score, SHREC signals.

C4 achieves higher fidelity than C3 because AASL natively supports Subjective Logic confidence, so the full opinion tuple is preserved in both directions.

**Fidelity metric:**

```
fidelity_c4 = 0.4 * text_similarity + 0.4 * opinion_wasserstein + 0.2 * type_preservation
```

Where opinion_wasserstein = 1 - (|b1-b2| + |d1-d2| + |u1-u2|) / 2.

### 8.4 C5 Projection (PCVM Governance)

**Fidelity target:** 0.92

**Preserves:** Full Subjective Logic opinion, claim class, full W3C PROV provenance, evidence array, VTD/MCT references, SUPPORT/CONTRADICTION/DERIVATION edges.

**Loses:** Analogy edges, vitality and circulation metadata, metabolic phase, consolidation history.

C5 achieves the highest fidelity because PCVM needs the most complete view for verification decisions.

**Fidelity metric:**

```
fidelity_c5 = 0.3 * text_match + 0.3 * opinion_wasserstein + 0.2 * provenance_jaccard + 0.2 * evidence_recall
```

### 8.5 Fidelity Monitoring

The projection engine continuously monitors round-trip fidelity:

```python
class FidelityMonitor:
    targets = {"C3": 0.85, "C4": 0.88, "C5": 0.92}
    tolerance = 0.05

    def check(self, target):
        avg = mean(self.history[target])
        if avg < self.targets[target] - self.tolerance:
            sentinel.report_fidelity_alarm(target, avg, self.targets[target])
            # Invalidate projection cache, re-evaluate projection function
```

### 8.6 Cache Management

**Consistency model (per subsystem):**

| Level | Scope | Behavior |
|-------|-------|----------|
| Eventual (default) | Standard quanta | Stale projection refreshed within 1 epoch |
| Epoch-boundary | C-class, N-class quanta | Refreshed at epoch boundary |
| Strong | Governance, constitutional quanta | Refreshed immediately on canonical update |

**Cache invalidation:** When canonical quantum fields change, affected projections are marked stale. Strong-consistency subscribers receive immediate refresh; others are refreshed at epoch boundary.

---

## 9. Retrieval Interface

### 9.1 Query Types

EMA supports four query types:

1. **Semantic:** Free-text query matched by embedding similarity. Parameters: query_text, domain_tags, min_credibility.
2. **Structural:** Graph neighborhood query from a root quantum. Parameters: root_quantum_id, edge_types, max_depth, direction.
3. **Temporal:** Time-range query. Parameters: epoch_range, created_after, modified_after.
4. **Metabolic-state:** Lifecycle phase query. Parameters: phases (ACTIVE/DECAYING/etc.), vitality_range, min_citation_count.

### 9.2 Relevance Ranking

```python
def rank_results(query, candidates):
    for q in candidates:
        semantic = cosine_similarity(query_embedding, q_embedding) if semantic_query else 1.0
        credibility = q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty
        vitality = q.metabolic_state.vitality
        recency = exp(-0.01 * age)
        citation = log1p(q.citation_count) / log1p(50)

        relevance = (0.40 * semantic + 0.25 * credibility + 0.15 * vitality
                     + 0.10 * recency + 0.10 * citation)
    return sorted(candidates, key=relevance, reverse=True)
```

### 9.3 Context-Aware Retrieval

Queries can include the requester's recent quantum interactions. Graph neighbors of recently accessed quanta receive a context boost factor (default 0.3x score multiplier) to surface contextually relevant knowledge.

---

## 10. Integration Architecture

### 10.1 PCVM Interface (C5)

**Bidirectional.** Primary integration point.

**Inbound:** PCVM admission events (MCT + VTD + BDL) trigger ingestion. EMA validates MCT signature and expiration before accepting.

**Outbound (C-class submission):** Dreaming consolidation output is packaged as C-class VTDs and submitted for verification. For high-impact consolidations (source quanta connected to >5 active quanta), adversarial probing is requested.

**Outbound (re-verification trigger):** When a quantum's credibility drops (dependency credibility drop, contradiction accumulation, opinion below admission threshold), EMA triggers PCVM re-verification.

### 10.2 Tidal Noosphere Interface (C3)

**Bidirectional.**

**Inbound:** Epoch boundary notifications trigger metabolic phase execution. Parcel topology changes trigger shard rebalancing.

**Outbound:** Locus-scoped knowledge summaries per epoch (active quantum count, domain distribution, mean vitality, contradiction hotspots, consolidation candidates). Parcel-scoped knowledge delivery via C3 projections.

### 10.3 ASV Interface (C4)

**Bidirectional.**

**Inbound:** AASL messages are converted to VTD drafts and submitted to PCVM. Only after PCVM verification does the quantum enter EMA.

**Outbound:** Quanta are projected to AASL format for agent communication. Circulation broadcasts use C4 projections.

### 10.4 Settlement Interface

**Bidirectional.**

**Outbound:** Metabolic efficiency reports per epoch (quanta ingested/dissolved/consolidated, mean vitality, knowledge utilization, SHREC budget snapshot). Agent contribution scores (active quanta count, total citations, consolidation contributions).

**Inbound:** Reward signals influence domain priority in SHREC ingestion scheduling.

### 10.5 Sentinel Graph Interface

**Bidirectional.**

**Outbound:** Metabolic health metrics, SHREC regulatory state, coherence anomalies (contradiction clusters, rapid vitality drops, quarantine spikes, projection fidelity drops), immune alerts (autoimmune alarms, catabolism weaponization suspects).

**Inbound:** System alerts triggering quarantine, forced re-verification, catabolism adjustment, or consolidation freeze.

---

## 11. Security Analysis

### 11.1 Threat Model

EMA faces adversarial threats from agents within the system (not external network attackers). The threat model assumes agents with valid PCVM-verified identities who abuse their access to manipulate knowledge outcomes.

### 11.2 Attack Resistance

**A3: Consolidation Poisoning (CRITICAL)**

*Threat:* Coordinated agents inject quanta to steer dreaming toward a desired conclusion.

*Mitigations:*
1. Provenance diversity requirement (>=5 agents, >=3 parcels, no agent >30%) (CR-12)
2. PCVM verification of all C-class claims catches invalid reasoning (CR-14)
3. 3-pass majority voting with independent prompt framings (CR-13)
4. Adversarial probing for high-impact consolidations
5. Per-agent contradiction weight cap limits influence (INV-E10)

*Residual risk:* A coordinated group of >=5 agents across >=3 parcels can still bias consolidation. This is analogous to academic citation manipulation. The C-class aging uncertainty mechanism provides a time-decay defense: unconfirmed consolidations gradually lose credibility.

**A8: Coherence Collapse at Scale (CRITICAL)**

*Threat:* At 1B quanta with 5 edges each, coherence computation requires 5B edge operations per epoch.

*Mitigations:*
1. Parcel-aligned sharding bounds per-shard computation to O(V_local * E_max)
2. Active edge budget (50 per quantum, 500K per shard) prevents unbounded growth
3. Sampled cross-shard coherence at Tier 2+ (10% sample rate)
4. Hierarchical cluster-level coherence at Tier 3
5. Edge TTL and Hebbian decay naturally prune unused edges

*Residual risk:* Cross-shard coherence at scale is approximate, not exact. Some cross-domain patterns may be missed at Tier 2+.

**A6: Catabolism Weaponization (HIGH)**

*Threat:* Agents create contradiction edges to force valid quanta into dissolution.

*Mitigations:*
1. Per-agent contradiction weight cap of 0.3 (INV-E10)
2. Structural protection for highly-cited quanta (citation_count >= 10)
3. Immune self-audit detects systematic false positive quarantining
4. 100-epoch quarantine window provides time for rescue

**A4: Projection Gap Exploitation (HIGH)**

*Threat:* Exploiting information loss in projections to hide malicious content.

*Mitigations:*
1. Canonical source principle (INV-E1): canonical governs on conflict
2. high_canonical_confidence flag in projections when opinion.belief > 0.8
3. Fidelity monitoring detects systematic degradation
4. Strong consistency for safety-critical quanta

**A5: SHREC Signal Gaming (MEDIUM)**

*Threat:* Manipulating SHREC inputs to starve metabolic processes.

*Mitigations:*
1. Constitutional floor allocations (INV-E7)
2. Frequency-dependent selection boosts rare signals
3. Self-correcting: trivial quanta are rapidly catabolized, normalizing signals

### 11.3 Trust Assumptions

1. PCVM provides sound verification. EMA trusts PCVM's MCTs.
2. C3 provides reliable epoch boundaries and parcel topology.
3. LLM inference is not adversarially compromised (inference API integrity).
4. At least some agents are honest (provenance diversity relies on independent agents existing).

### 11.4 Residual Risks

| Risk | Severity | Status |
|------|----------|--------|
| Consolidation poisoning by >=5 coordinated agents | HIGH | Mitigated, not eliminated |
| Cross-shard coherence degradation at Tier 2+ | MEDIUM | Approximate by design |
| Dreaming hallucination that passes PCVM (systematic LLM bias) | MEDIUM | C-class aging uncertainty provides time-decay |
| SHREC stability under compound perturbation | MEDIUM | Unproven; requires HG-1 simulation |
| Projection fidelity below targets | MEDIUM | Targets unvalidated; requires empirical measurement |

---

## 12. Scalability Analysis

### 12.1 Scale Tiers

| Tier | Quanta | Agents | Epoch Processing Target |
|------|--------|--------|------------------------|
| T1 | < 100K | 1K | < 1 second |
| T2 | 100K-10M | 1K-10K | < 30 seconds |
| T3 | > 10M | 10K-100K | < 300 seconds |

### 12.2 Complexity Analysis

| Operation | Per-Epoch Complexity | Bottleneck |
|-----------|---------------------|-----------|
| Ingestion | O(new_claims * embedding_cost) | Embedding computation |
| Circulation | O(eligible * subscribers) | Subscription matching |
| Consolidation | O(candidates * passes * LLM_cost) | LLM inference |
| Catabolism | O(shard_size) | Vitality computation |
| SHREC | O(1) per signal | Constant per epoch |
| Edge weight update | O(V_local * E_max) per shard | Graph traversal |
| Vitality batch | O(V_local) per shard | Opinion computation |

### 12.3 Cost Model

**Honest cost assessment:** EMA adds processing overhead to every knowledge operation:
- Ingestion: 5-15ms per quantum (decomposition + edge creation + embedding)
- Circulation: O(subscribers) push cost per epoch
- Consolidation: 50-200 LLM inference calls per dreaming cycle (most expensive)
- Catabolism: O(quarantine_queue) per epoch (lightweight)

The metabolic overhead is justified only if consolidation produces genuine cross-domain insights that pass PCVM verification. This is validated by Hard Gate HG-4 (Dreaming Precision). If dreaming precision < 0.40, the overhead is not justified and EMA should reduce to a lifecycle-managed knowledge graph without autonomous consolidation.

### 12.4 Metabolic Efficiency Metrics

```
metabolic_efficiency = value_produced / resources_consumed
```

Where value_produced = (consolidation_acceptance_rate * knowledge_utilization_rate) and resources_consumed = (total_cpu + total_llm + total_io) normalized to budget.

---

## 13. Open Design Questions

### 13.1 SHREC Stability Under Compound Perturbation

The Lotka-Volterra stability analysis is local (linearized around the interior equilibrium). Global stability under compound perturbations (simultaneous ingestion spike + knowledge loss + domain shift) is unproven. Hard Gate HG-1 requires simulation validation. If the system exhibits sustained oscillation (CV > 0.30 after 500 epochs) or competitive exclusion (any signal reaches zero), the Lotka-Volterra model must be replaced with simpler priority-weighted allocation.

### 13.2 Dreaming Precision

Dreaming consolidation is EMA's highest-risk, highest-reward component. If dreaming produces more noise than signal, the entire metabolic architecture reduces to an expensive knowledge graph. Hard Gate HG-4 requires: precision >= 0.50, hallucination rate < 0.30, recall on strong patterns >= 0.60 (3 of 5). If these thresholds are not met, dreaming should be restricted to within-domain patterns only, or eliminated entirely.

### 13.3 Projection Fidelity Validation

The fidelity targets (C3: 0.85, C4: 0.88, C5: 0.92) are design targets, not validated measurements. Required Action RA-1 mandates measurement on 50 representative quanta. If actual fidelity is below target by more than 0.10, the bounded-loss guarantee weakens and agents may need to routinely check canonical quanta rather than relying on projections.

### 13.4 Metabolic Advantage Over Simpler Approaches

The fundamental question: does EMA produce measurably better outcomes than a standard knowledge graph with TTL-based expiry, periodic re-indexing, and query-based retrieval? The metabolic framing generates architectural features (dreaming, SHREC, vitality-based catabolism) that would not arise from conventional design. But if those features do not produce measurably better knowledge quality, the metabolic complexity is unjustified. Required Action RA-2 mandates specifying a comparison baseline.

### 13.5 Cross-System Desynchronization

If EMA, C3, and C5 epochs drift or if network partitions cause delayed updates, projections may become inconsistent with canonical quanta for extended periods. The epoch-boundary consistency model assumes reliable epoch synchronization. In degraded network conditions, the system must fall back to eventual consistency with explicit staleness tracking.

---

## 14. Conclusion

The Epistemic Metabolism Architecture introduces a paradigm shift in knowledge management for multi-agent AI systems. By treating knowledge as a living metabolic process rather than a stored asset, EMA provides capabilities that no static knowledge system can:

1. **Autonomous consolidation** through dreaming, producing cross-domain insights that individual agents would not discover.
2. **Ecological self-regulation** through SHREC, adapting resource allocation to changing knowledge demands without manual tuning.
3. **Principled knowledge retirement** through catabolism with structural protection, preventing both unbounded growth and loss of foundational knowledge.
4. **Multi-ontology projection** allowing each subsystem to see knowledge in its native format with measured, bounded information loss.

The architecture is honest about its risks. Dreaming precision is uncertain. SHREC stability is proven locally but not globally. Projection fidelity targets are design goals, not validated measurements. Consolidation poisoning by coordinated agents is mitigated but not eliminated.

The market window is 12-18 months. MemOS is the closest competitor, addressing lifecycle management but lacking ecological regulation, verification-gated consolidation, and multi-ontology projection. EMA's combination of these capabilities in a unified metabolic architecture is novel -- no existing system or published research proposes the full synthesis.

The metabolic metaphor earns its keep through one clear architectural prediction that no simpler approach would produce: knowledge should be consolidated through diverse, verified, multi-pass reasoning that discovers cross-domain patterns invisible to individual agents. This is the dreaming process. If dreaming works, EMA is a category-creating innovation. If dreaming does not work, EMA is still a well-specified lifecycle-managed knowledge graph with ecological self-regulation -- a valuable contribution, but not a new paradigm.

---

## Appendix A: Complete Epistemic Quantum JSON Schema

```json
{
  "$id": "https://ema.atrahasis.dev/schema/v1/epistemic-quantum.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Epistemic Quantum",
  "description": "The fundamental knowledge unit in EMA -- a self-describing 10-tuple.",
  "type": "object",
  "required": [
    "id", "content", "opinion", "provenance", "edges",
    "metabolic_state", "projections", "timestamps",
    "dissolution_record", "claim_class"
  ],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^eq:[^:]+:[0-9]+:[a-f0-9]{12}$",
      "description": "Globally unique: eq:<locus>:<epoch>:<uuid7_short>"
    },
    "content": {
      "type": "object",
      "required": ["claim_text", "claim_type", "domain_tags"],
      "properties": {
        "claim_text": { "type": "string", "minLength": 1, "maxLength": 4096 },
        "claim_type": {
          "type": "string",
          "enum": ["observation", "inference", "prediction", "consolidation", "axiom", "governance"]
        },
        "domain_tags": {
          "type": "array", "items": { "type": "string", "maxLength": 128 },
          "minItems": 1, "maxItems": 10
        },
        "evidence": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["evidence_type", "weight"],
            "properties": {
              "source_quantum_id": { "type": ["string", "null"] },
              "external_reference": { "type": ["string", "null"] },
              "evidence_type": { "type": "string", "enum": ["empirical", "testimonial", "inferential", "synthetic"] },
              "weight": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
            }
          }
        },
        "structured_content": { "type": "object", "additionalProperties": true }
      }
    },
    "opinion": {
      "type": "object",
      "required": ["belief", "disbelief", "uncertainty", "base_rate"],
      "properties": {
        "belief": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "disbelief": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "uncertainty": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "base_rate": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
      },
      "description": "Constraint: belief + disbelief + uncertainty = 1.0"
    },
    "provenance": {
      "type": "object",
      "required": ["generating_agent", "generating_activity", "generation_time"],
      "properties": {
        "generating_agent": { "type": "string" },
        "generating_activity": {
          "type": "string",
          "enum": ["ingestion", "inference", "consolidation", "governance", "external_import"]
        },
        "generation_time": { "type": "string", "format": "date-time" },
        "generation_epoch": { "type": "integer", "minimum": 0 },
        "derived_from": { "type": "array", "items": { "type": "string" }, "default": [] },
        "method": { "type": ["string", "null"] },
        "source_vtd_id": { "type": ["string", "null"] },
        "attribution_chain": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["agent_id", "role", "timestamp"],
            "properties": {
              "agent_id": { "type": "string" },
              "role": { "type": "string", "enum": ["creator", "reviewer", "consolidator", "verifier"] },
              "timestamp": { "type": "string", "format": "date-time" }
            }
          }
        }
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["target_id", "edge_type", "weight", "created_at"],
        "properties": {
          "target_id": { "type": "string" },
          "edge_type": { "type": "string", "enum": ["SUPPORT", "CONTRADICTION", "DERIVATION", "ANALOGY", "SUPERSESSION"] },
          "weight": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
          "created_at": { "type": "string", "format": "date-time" },
          "last_activated": { "type": "string", "format": "date-time" },
          "creating_agent": { "type": "string" }
        }
      },
      "maxItems": 50
    },
    "metabolic_state": {
      "type": "object",
      "required": ["phase", "vitality"],
      "properties": {
        "phase": { "type": "string", "enum": ["ACTIVE", "CONSOLIDATING", "DECAYING", "QUARANTINED", "DISSOLVED"] },
        "vitality": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "circulation_count": { "type": "integer", "minimum": 0, "default": 0 },
        "consolidation_lock": {
          "oneOf": [
            { "type": "null" },
            {
              "type": "object",
              "required": ["dreaming_session_id", "locked_at", "lock_ttl_epochs", "lock_epoch"],
              "properties": {
                "dreaming_session_id": { "type": "string" },
                "locked_at": { "type": "string", "format": "date-time" },
                "lock_ttl_epochs": { "type": "integer", "minimum": 1, "maximum": 20 },
                "lock_epoch": { "type": "integer", "minimum": 0 }
              }
            }
          ],
          "default": null
        }
      }
    },
    "projections": {
      "type": "object",
      "properties": {
        "c3": { "oneOf": [{ "type": "null" }, { "$ref": "#/$defs/CachedProjection" }], "default": null },
        "c4": { "oneOf": [{ "type": "null" }, { "$ref": "#/$defs/CachedProjection" }], "default": null },
        "c5": { "oneOf": [{ "type": "null" }, { "$ref": "#/$defs/CachedProjection" }], "default": null }
      }
    },
    "timestamps": {
      "type": "object",
      "required": ["created_at"],
      "properties": {
        "created_at": { "type": "string", "format": "date-time" },
        "last_circulated": { "type": ["string", "null"], "format": "date-time" },
        "last_verified": { "type": ["string", "null"], "format": "date-time" },
        "decay_start": { "type": ["string", "null"], "format": "date-time" },
        "last_accessed": { "type": ["string", "null"], "format": "date-time" }
      }
    },
    "dissolution_record": {
      "oneOf": [
        { "type": "null" },
        {
          "type": "object",
          "required": ["reason", "dissolved_at_epoch", "recycled_to", "eliminated_evidence"],
          "properties": {
            "reason": { "type": "string", "enum": ["low_credibility", "temporal_expiry", "superseded", "quarantine_timeout", "manual"] },
            "dissolved_at_epoch": { "type": "integer", "minimum": 0 },
            "dissolved_at": { "type": "string", "format": "date-time" },
            "recycled_to": { "type": "array", "items": { "type": "string" } },
            "eliminated_evidence": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": { "evidence_hash": { "type": "string" }, "reason": { "type": "string" } }
              }
            },
            "content_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
            "final_opinion": { "$ref": "#/properties/opinion" }
          }
        }
      ],
      "default": null
    },
    "claim_class": { "type": "string", "enum": ["D", "E", "S", "H", "N", "P", "R", "C"] },
    "quantum_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "shard_id": { "type": "string" },
    "citation_count": { "type": "integer", "minimum": 0, "default": 0 },
    "version": { "type": "integer", "minimum": 1, "default": 1 }
  },
  "$defs": {
    "CachedProjection": {
      "type": "object",
      "required": ["projected_at", "fidelity_score", "payload"],
      "properties": {
        "projected_at": { "type": "string", "format": "date-time" },
        "projection_epoch": { "type": "integer", "minimum": 0 },
        "fidelity_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "payload": { "type": "object", "additionalProperties": true },
        "stale": { "type": "boolean", "default": false }
      }
    }
  }
}
```

---

## Appendix B: SHREC Signal Computation Functions

See Section 6.2 for complete pseudocode of all five signal computation functions:

- `compute_epistemic_hunger(state, epoch)` -- Measures unmet knowledge demand
- `compute_consolidation_pressure(state, epoch)` -- Measures cross-domain synthesis opportunity
- `compute_metabolic_stress(state, epoch)` -- Measures system overload
- `compute_immune_response(state, epoch)` -- Measures knowledge integrity threats
- `compute_novelty_signal(state, epoch)` -- Measures novel knowledge influx

Each signal outputs a value in [0, 1], computed from a weighted combination of 3-4 sub-metrics measured over a rolling window of SIGNAL_WINDOW_EPOCHS (20) epochs.

---

## Appendix C: Lotka-Volterra Equations and Stability Conditions

### C.1 Continuous-Time Model

```
dS_i/dt = r_i * S_i * (1 - sum_j(alpha_ij * S_j / K_i)) + floor_correction_i
```

### C.2 Discrete-Time Implementation

```python
def lotka_volterra_step(current_shares, signals, params):
    new_shares = {}
    for i, name in enumerate(SIGNAL_NAMES):
        S_i = current_shares[name]
        r_i = params.growth_rates[name]
        K_i = params.carrying_capacities[name]  # default: 0.4

        competition = sum(params.alpha[name][other] * current_shares[other] / K_i
                         for other in SIGNAL_NAMES)
        dS = r_i * S_i * (1.0 - competition)

        # Floor correction
        floor = FLOOR_ALLOCATIONS[name]
        if S_i < floor:
            dS += (floor - S_i) * FLOOR_RESTORATION_RATE

        # Signal intensity as growth rate modifier
        dS *= signals[name]
        new_shares[name] = max(0.0, S_i + dS * DT)

    # Normalize to sum to 1.0
    total = sum(new_shares.values())
    return {s: v / total for s, v in new_shares.items()} if total > 0 else new_shares
```

### C.3 Coexistence Conditions

For stable coexistence of all 5 signals:

1. **Weak inter-specific competition:** alpha_ij * alpha_ji < 1 for all pairs (i,j). With default alpha matrix, all products are in [0.01, 0.09].

2. **Niche differentiation:** Each signal has a primary resource dimension.

3. **Floor guarantees:** Absolute minimums regardless of competitive outcome.

### C.4 Lyapunov Stability

Lyapunov function: V = sum_i (S_i - S_i* - S_i* * ln(S_i / S_i*))

dV/dt < 0 when alpha_ij < K_i/K_j for all i,j. With default parameters, this condition holds since all alpha_ij are 0.1-0.3 and K_i/K_j ~ 1.0.

---

## Appendix D: Configurable Parameters Table

### D.1 Metabolic State Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| DECAY_THRESHOLD | 0.30 | [0.1, 0.5] | 4.3 |
| QUARANTINE_THRESHOLD | 0.15 | [0.05, 0.3] | 4.3 |
| MAX_DECAY_EPOCHS | 50 | [10, 200] | 4.3 |
| MAX_QUARANTINE_EPOCHS | 100 | [20, 500] | 4.3 |
| BASE_DECAY_RATE | 0.005 | [0.001, 0.05] | 4.4 |
| ACCESS_DECAY_RATE | 0.02 | [0.005, 0.1] | 4.4 |
| SUPPORT_VITALITY_FACTOR | 0.1 | [0.05, 0.3] | 4.4 |
| CONTRADICTION_VITALITY_FACTOR | 0.15 | [0.05, 0.3] | 4.4 |
| MAX_TOTAL_CONTRADICTION_FACTOR | 0.8 | [0.5, 1.0] | 4.4 |
| SUPERSESSION_DECAY_MULTIPLIER | 2.0 | [1.5, 5.0] | 4.4 |

### D.2 Edge Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| REINFORCEMENT_RATE | 0.05 | [0.01, 0.2] | 5.2 |
| EDGE_DECAY_RATE | 0.02 | [0.005, 0.1] | 5.2 |
| EDGE_TTL | 50 | [10, 200] | 5.2 |
| MIN_EDGE_WEIGHT | 0.05 | [0.01, 0.1] | 5.2 |
| MAX_EDGES_PER_QUANTUM | 50 | [20, 100] | 7.4 |
| MAX_EDGES_PER_SHARD | 500000 | [100000, 5000000] | 7.4 |
| EDGE_DISCOVERY_THRESHOLD | 0.4 | [0.2, 0.7] | 5.1 |
| INITIAL_EDGE_DISCOVERY_K | 10 | [3, 20] | 5.1 |

### D.3 Consolidation Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| MIN_CLUSTER_SIZE | 5 | [3, 10] | 5.3.1 |
| MIN_MUTUAL_SUPPORT_EDGES | 3 | [2, 8] | 5.3.1 |
| CONSOLIDATION_MIN_EDGE_WEIGHT | 0.3 | [0.1, 0.6] | 5.3.1 |
| MAX_CONSOLIDATION_CANDIDATES_PER_EPOCH | 5 | [1, 20] | 5.3.1 |
| MIN_INDEPENDENT_AGENTS | 5 | [3, 10] | 5.3.2 |
| MIN_INDEPENDENT_PARCELS | 3 | [2, 5] | 5.3.2 |
| CONSOLIDATION_LOCK_TTL | 5 | [1, 20] | 5.3.3 |
| NUM_SYNTHESIS_PASSES | 3 | [2, 5] | 5.3.4 |
| SYNTHESIS_TEMPERATURE | 0.3 | [0.1, 0.7] | 5.3.4 |
| MAJORITY_THRESHOLD | 2 | [2, NUM_PASSES] | 5.3.4 |
| CONSOLIDATION_COOLDOWN_EPOCHS | 20 | [5, 50] | 5.3.5 |
| CCLASS_VALIDATION_WINDOW | 50 | [20, 200] | 5.3.6 |
| CCLASS_AGING_UNCERTAINTY_RATE | 0.1 | [0.05, 0.2] | 5.3.6 |

### D.4 Catabolism Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| CATABOLISM_CREDIBILITY_THRESHOLD | 0.3 | [0.1, 0.5] | 5.4.1 |
| DECAY_AGE_THRESHOLD | 100 | [20, 500] | 5.4.1 |
| SUPERSESSION_MARGIN | 0.1 | [0.05, 0.3] | 5.4.1 |
| STRUCTURAL_PROTECTION_THRESHOLD | 10 | [5, 50] | 5.4.2 |
| KEYSTONE_DISCONNECT_THRESHOLD | 5 | [2, 20] | 5.4.2 |
| QUARANTINE_SNAPSHOT_RETENTION_EPOCHS | 200 | [50, 1000] | 5.4.3 |
| MAX_RECYCLING_RECIPIENTS | 5 | [1, 10] | 5.4.3 |
| MAX_AGENT_CONTRADICTION_WEIGHT | 0.3 | [0.1, 0.5] | 4.5 |

### D.5 SHREC Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| BUDGET_SAFETY_MARGIN | 0.15 | [0.05, 0.3] | 6.3 |
| STATS_WINDOW_EPOCHS | 100 | [20, 500] | 6.6 |
| BAYESIAN_PRIOR_WEIGHT | 5.0 | [1.0, 20.0] | 6.6 |
| ELEVATED_Z_THRESHOLD | 1.5 | [1.0, 2.0] | 6.7 |
| CRITICAL_Z_THRESHOLD | 2.5 | [2.0, 3.5] | 6.7 |
| REGIME_HYSTERESIS_EPOCHS | 5 | [2, 20] | 6.7 |
| PID_CLAMP_ELEVATED | 0.10 | [0.05, 0.2] | 6.7 |
| PID_CLAMP_CRITICAL | 0.25 | [0.15, 0.4] | 6.7 |
| INTEGRAL_CLAMP | 0.20 | [0.1, 0.5] | 6.7 |
| IMMUNE_AUDIT_INTERVAL | 50 | [10, 100] | 6.8 |
| AUTOIMMUNE_ALARM_THRESHOLD | 0.20 | [0.1, 0.4] | 6.8 |

### D.6 Projection Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| C3_FIDELITY_TARGET | 0.85 | [0.75, 0.95] | 8.2 |
| C4_FIDELITY_TARGET | 0.88 | [0.80, 0.95] | 8.3 |
| C5_FIDELITY_TARGET | 0.92 | [0.85, 0.98] | 8.4 |
| FIDELITY_TOLERANCE | 0.05 | [0.02, 0.10] | 8.5 |
| FIDELITY_WINDOW | 100 | [20, 500] | 8.5 |

### D.7 Retrieval Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| SEMANTIC_WEIGHT | 0.40 | [0.2, 0.6] | 9.2 |
| CREDIBILITY_WEIGHT | 0.25 | [0.1, 0.4] | 9.2 |
| VITALITY_WEIGHT | 0.15 | [0.05, 0.3] | 9.2 |
| RECENCY_WEIGHT | 0.10 | [0.05, 0.2] | 9.2 |
| CITATION_WEIGHT | 0.10 | [0.05, 0.2] | 9.2 |
| CONTEXT_BOOST_FACTOR | 0.3 | [0.1, 0.5] | 9.3 |

---

## Appendix E: Conformance Requirements

### E.1 MUST Requirements (24 mandatory)

| ID | Requirement | Section |
|----|-------------|---------|
| CR-1 | Implement the complete epistemic quantum schema (all 10 tuple fields) | 4.1 |
| CR-2 | Enforce the lifecycle state machine with all defined transitions | 4.3 |
| CR-3 | Enforce b + d + u = 1 constraint on all Subjective Logic opinions | 4.2 |
| CR-4 | Gate all quantum creation through PCVM verification (INV-E2) | 5.1 |
| CR-5 | Execute metabolic phases in strict order within each epoch (INV-E3) | 3.5 |
| CR-6 | Implement consolidation locks with bounded TTL (INV-E4) | 5.3.3 |
| CR-7 | Enforce dissolution irreversibility (INV-E5) | 4.3 |
| CR-8 | Enforce edge budget limits per quantum and per shard (INV-E6) | 7.4 |
| CR-9 | Enforce SHREC floor allocations (INV-E7) | 6.5 |
| CR-10 | Maintain complete W3C PROV provenance for every quantum (INV-E9) | 4.1 |
| CR-11 | Enforce per-agent contradiction weight cap (INV-E10) | 4.5 |
| CR-12 | Implement provenance diversity verification for consolidation (>=5 agents, >=3 parcels) | 5.3.2 |
| CR-13 | Implement 3-pass majority voting for LLM synthesis | 5.3.4 |
| CR-14 | Submit all C-class claims to PCVM for verification | 5.3.5 |
| CR-15 | Implement two-phase catabolism (quarantine then dissolution) | 5.4.3 |
| CR-16 | Preserve dissolution records permanently | 5.4.3 |
| CR-17 | Implement structural protection for highly-cited quanta | 5.4.2 |
| CR-18 | Compute all five SHREC signals each epoch | 6.2 |
| CR-19 | Implement regime detection with hysteresis | 6.7 |
| CR-20 | Implement PID overlay with anti-windup for ELEVATED+ regimes | 6.7 |
| CR-21 | Implement projection functions for C3, C4, and C5 | 8.2-8.4 |
| CR-22 | Monitor projection fidelity and alarm on degradation | 8.5 |
| CR-23 | Implement C-class aging uncertainty for unvalidated consolidations | 5.3.6 |
| CR-24 | DERIVATION edges MUST NOT be pruned or have weight reduced | 4.5 |

### E.2 SHOULD Requirements (12 recommended)

| ID | Requirement | Section |
|----|-------------|---------|
| SR-1 | SHOULD implement Hebbian edge weight reinforcement | 5.2 |
| SR-2 | SHOULD implement context-aware retrieval | 9.3 |
| SR-3 | SHOULD implement immune self-audit at configurable intervals | 6.8 |
| SR-4 | SHOULD implement frequency-dependent selection for rare SHREC signals | 6.4 |
| SR-5 | SHOULD implement CUSUM change-point detection for PID anti-windup | 6.7 |
| SR-6 | SHOULD implement quarantine rescue by dreaming process | 4.3 |
| SR-7 | SHOULD implement keystone detection for structural protection | 5.4.2 |
| SR-8 | SHOULD implement Lotka-Volterra dynamics for competitive allocation | 6.4 |
| SR-9 | SHOULD cache projections and implement staleness detection | 8.6 |
| SR-10 | SHOULD report metabolic health metrics to Sentinel Graph | 10.5 |
| SR-11 | SHOULD implement evidence recycling before dissolution | 5.4.3 |
| SR-12 | SHOULD implement derivative monitoring alarm for PID stability | 6.7 |

### E.3 MAY Requirements (7 optional)

| ID | Requirement | Section |
|----|-------------|---------|
| MR-1 | MAY implement additional edge types beyond the five defined | 4.5 |
| MR-2 | MAY implement cross-shard consolidation for multi-locus patterns | 5.3.1 |
| MR-3 | MAY implement additional projection targets beyond C3, C4, C5 | 8.1 |
| MR-4 | MAY implement configurable per-locus metabolic parameters | App. D |
| MR-5 | MAY implement decay_rate_override for individual quanta | App. A |
| MR-6 | MAY implement additional synthesis prompt framings beyond three | 5.3.4 |
| MR-7 | MAY implement settlement-aware circulation priority | 5.2 |

---

## Appendix F: Test Vectors

### F.1 TV-1: Epistemic Quantum Construction

**Input:** D-class VTD with claim "Protein folding rate for sequence ACGT is 3.2ms," opinion (b=0.95, d=0.0, u=0.05, a=0.5).

**Expected:** Quantum with id matching `eq:biology.proteomics:100:*`, claim_type="observation", phase=ACTIVE, vitality=1.0, claim_class="D", credibility E(w) = 0.95 + 0.5 * 0.05 = 0.975.

### F.2 TV-2: Vitality Computation

**Input:** Age=50 epochs, last_accessed=10 epochs ago, 3 SUPPORT edges (0.8, 0.6, 0.4), 1 CONTRADICTION edge (0.5), opinion (b=0.7, d=0.1, u=0.2, a=0.5).

**Computation:**
```
base_decay = exp(-0.005 * 50) = 0.7788
access_recency = exp(-0.02 * 10) = 0.8187
support_factor = min(1.0, 0.5 + 1.8 * 0.1) = 0.68
contradiction_factor = min(0.8, 0.5 * 0.15) = 0.075
credibility = 0.7 + 0.5 * 0.2 = 0.8
vitality = 0.7788 * 0.8187 * 0.68 * 0.925 * 0.8 = ~0.321
```

**Expected:** Vitality ~0.321. Since 0.321 > DECAY_THRESHOLD (0.30), quantum remains ACTIVE.

### F.3 TV-3: SHREC Floor Enforcement

**Scenario:** All signals zero except IMMUNE at 1.0. Budget=1000.

**Expected:** IMMUNE=720 (150 floor + 570 competitive), STRESS=100, NOVELTY=80, HUNGER=50, CONSOLIDATION=50. Total=1000. All signals above floor. INV-E7 satisfied.

### F.4 TV-4: Consolidation Pipeline

**Input:** 7 ACTIVE quanta, 6 distinct agents, 4 parcels, 6 mutual support edges.

**Expected steps:** Candidate identification (size=7 >= 5), diversity verification (6 agents >= 5, 4 parcels >= 3), lock acquisition (all 7 CONSOLIDATING), 3-pass LLM synthesis, majority voting, C-class VTD construction, PCVM submission, lock release. New quantum: claim_class="C", uncertainty >= 0.4.

### F.5 TV-5: Structural Protection

**Input:** Quantum with credibility=0.3, age=150 epochs, citation_count=15.

**Expected:** Meets catabolism criteria (credibility at threshold AND age > 100) but structurally protected (citation_count=15 > threshold=10). Remains ACTIVE.

### F.6 TV-6: Per-Agent Contradiction Cap

**Input:** Agent creates 5 contradiction edges (weight 0.1 each) to target quantum.

**Expected:** Edges 1-3 allowed (cumulative 0.3 <= cap). Edges 4-5 rejected (would exceed 0.3 cap). INV-E10 enforced.

### F.7 TV-7: Regime Hysteresis

**Input:** Epoch 100: z=1.8 (ELEVATED). Epochs 101-104: z < 1.5 (NORMAL detected). Epoch 105: z < 1.5.

**Expected:** Epoch 100: NORMAL->ELEVATED (immediate). Epochs 101-104: remain ELEVATED (need 5 consecutive). Epoch 105: ELEVATED->NORMAL (5 consecutive achieved).

### F.8 TV-8: C3 Projection Fidelity

**Input:** Quantum with claim_text preserved, opinion (b=0.8, u=0.15, a=0.5), 2 within-parcel SUPPORT edges, 1 cross-parcel SUPPORT edge, 1 ANALOGY edge.

**C3 projection:** Text preserved (1.0), relevance_score=0.875, 2 local edges (cross-parcel and analogy lost).

**Round-trip fidelity:** text_sim=1.0, opinion_preservation ~1.0 (scalar matches), edge_jaccard=2/2=1.0 (within-parcel). Fidelity = 0.5*1.0 + 0.3*1.0 + 0.2*1.0 = 1.0 (best case). Degrades when cross-parcel edges are important to consumer.

---

## Appendix G: Traceability Matrix

| Hard Gate / Action | Source | Specification Section | Conformance Req |
|-------------------|--------|----------------------|-----------------|
| HG-1: SHREC Stability | Science Advisor Exp. 4, A5 | 6.4, 6.9, App. C | CR-9, CR-18-20 |
| HG-2: Coherence Graph Scaling | A8 | 7.2, 7.4, 7.5, 12.1 | CR-8 |
| HG-3: Consolidation Diversity | A3 | 5.3.2 | CR-12 |
| HG-4: Dreaming Precision | Science Advisor Exp. 3, A2 | 5.3.4, 5.3.5 | CR-13, CR-14 |
| RA-1: Projection Fidelity | Feasibility verdict | 8.2-8.5 | CR-21, CR-22 |
| RA-2: Metabolic Advantage Baseline | Skeptic challenge | 13.4 | -- |
| RA-3: Per-Agent Contradiction Cap | A6 | 4.4, 4.5 | CR-11 |
| RA-4: Projection Consistency | Feasibility verdict | 8.6 | CR-22 |
| RA-5: C-Class Aging Uncertainty | A2 | 5.3.6 | CR-23 |

---

## Appendix H: Glossary

| Term | Definition |
|------|-----------|
| **Epistemic Quantum** | The fundamental knowledge unit in EMA: a 10-tuple carrying content, confidence, provenance, edges, metabolic state, projections, timestamps, dissolution record, and claim class. |
| **Subjective Logic** | A formal framework (Josang 2016) for reasoning under uncertainty using opinion tuples (b, d, u, a) where b+d+u=1. |
| **SHREC** | Stratified Homeostatic Regulation with Ecological Competition. EMA's five-signal regulatory system. |
| **Dreaming** | The consolidation process in which LLM reasoning identifies cross-domain patterns from clusters of related quanta. |
| **Vitality** | A composite health score [0, 1] determining metabolic state transitions. Computed from base decay, access recency, support, contradiction, credibility, and supersession. |
| **MCT** | Membrane Clearance Token. PCVM's verification certificate allowing a claim to enter EMA. |
| **VTD** | Verification Trace Document. The auditable record of PCVM's verification process. |
| **BDL** | Base Durability Ledger. PCVM's admission protocol output. |
| **Coherence Graph** | The typed, weighted edge network connecting epistemic quanta. Sharded by C3 parcel topology. |
| **Catabolism** | The controlled dissolution of quanta that have lost vitality. Two-phase: quarantine (reversible) then dissolution (irreversible with recycling). |
| **Anabolism** | Knowledge building: ingestion of new quanta and consolidation of existing quanta into higher-order structures. |
| **Hebbian Reinforcement** | Edge strengthening when both endpoint quanta are accessed in the same epoch. Analogous to "neurons that fire together wire together." |
| **Projection** | A subsystem-native view of an epistemic quantum with controlled, measured information loss. |
| **Fidelity** | Round-trip information preservation measured between a canonical quantum and its projection-then-reconstruction. |
| **Epoch** | A temporal unit aligned with C3's tidal epoch. Each epoch contains five metabolic phases. |
| **Locus** | A namespace in the Tidal Noosphere topology (C3). EMA shards its coherence graph along locus boundaries. |
| **Parcel** | A spatial subdivision within a locus (C3). Agents are assigned to parcels. |
| **Claim Class** | One of 8 PCVM verification classes: D (Deterministic), E (Empirical), S (Statistical), H (Heuristic), N (Normative), P (Process), R (Reasoning), C (Consolidation). |
| **Constitutional Bound** | A hard system limit protected from modification by SHREC ecological dynamics. Changes require G-class governance consensus. |
| **Structural Protection** | Immunity from catabolism granted to quanta with high citation counts (>= 10) or keystone status. |
| **Autoimmune Alarm** | Detection that catabolism is over-aggressive, quarantining valid knowledge. Triggers threshold adjustment. |

---

*Specification produced under Atrahasis Agent System v2.0 protocol.*
*C6: Epistemic Metabolism Architecture (EMA) -- MASTER TECH SPEC.*
*Pipeline status: COMPLETE.*
*Version 1.0.0 -- 2026-03-10*
