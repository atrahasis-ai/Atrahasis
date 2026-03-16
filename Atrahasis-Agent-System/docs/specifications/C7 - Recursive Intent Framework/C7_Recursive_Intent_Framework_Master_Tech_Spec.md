# Recursive Intent Fabric: A Two-Plane Orchestration Architecture for Sovereign AI Coordination at Planetary Scale
## Master Technical Specification — C7-A
## Version 2.0

**Invention ID:** C7
**Concept:** C7-A Recursive Intent Fabric (RIF)
**Date:** 2026-03-10
**Status:** SPECIFICATION — Master Tech Spec v2.0
**Predecessor Specs:** CIOS (implied, unspecified), C3 Tidal Noosphere, Alternative C communication authority (C38-C42, T-290 AXIP-v1), C5 PCVM, C6 EMA
**Ideation Council Verdict:** SELECTED (4-0, Critic abstains). Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10 (MEDIUM-HIGH)
**Primary Scale Target:** 1,000-10,000 agents (100K+ aspirational, contingent on >=80% locus-local intent ratio)

**v2.0 Changes:** This version unifies the original v1.0 specification with Patch Addendum F47-F51 (37 schema conflicts resolved, HotStuff consensus, strategy selection algorithm, resource contention protocol) and C9 Cross-Layer Reconciliation errata (E-C7-01: settlement routing corrected to C8 DSF). All patches are woven inline; no separate addendum required.

---

## Table of Contents

- [1. Abstract](#1-abstract)
- [2. Introduction and Motivation](#2-introduction-and-motivation)
  - [2.1 The Orchestration Problem](#21-the-orchestration-problem)
  - [2.2 Why Existing Approaches Fail](#22-why-existing-approaches-fail)
  - [2.3 What RIF Contributes](#23-what-rif-contributes)
  - [2.4 Position in the Atrahasis Stack](#24-position-in-the-atrahasis-stack)
- [3. Background and Related Work](#3-background-and-related-work)
  - [3.1 HTN Planning and BDI Architectures](#31-htn-planning-and-bdi-architectures)
  - [3.2 Stafford Beer's Viable System Model](#32-stafford-beers-viable-system-model)
  - [3.3 Intent-Based Networking](#33-intent-based-networking)
  - [3.4 Workflow Engines and Saga Patterns](#34-workflow-engines-and-saga-patterns)
  - [3.5 Hierarchical Orchestration Systems](#35-hierarchical-orchestration-systems)
  - [3.6 How RIF Differs](#36-how-rif-differs)
- [4. Architecture Overview](#4-architecture-overview)
  - [4.1 Two-Plane Design](#41-two-plane-design)
  - [4.2 Component Inventory](#42-component-inventory)
  - [4.3 Design Principles](#43-design-principles)
  - [4.4 Integration with Substrate Components](#44-integration-with-substrate-components)
- [5. Intent Quantum](#5-intent-quantum)
  - [5.1 Formal Definition and JSON Schema](#51-formal-definition-and-json-schema)
  - [5.2 The Four Intent Types](#52-the-four-intent-types)
  - [5.3 Lifecycle State Machine](#53-lifecycle-state-machine)
  - [5.4 Success Criteria Specification Language](#54-success-criteria-specification-language)
  - [5.5 Comparison to Traditional Approaches](#55-comparison-to-traditional-approaches)
- [6. Formal Decomposition Algebra](#6-formal-decomposition-algebra)
  - [6.1 Operation Class Decomposition Rules](#61-operation-class-decomposition-rules)
  - [6.2 Termination Guarantee](#62-termination-guarantee)
  - [6.3 Cycle-Freedom Guarantee](#63-cycle-freedom-guarantee)
  - [6.4 Resource Bound Preservation](#64-resource-bound-preservation)
  - [6.5 Decomposition Budget Mechanics](#65-decomposition-budget-mechanics)
  - [6.6 Memoization Strategy](#66-memoization-strategy)
- [7. Domain-Scoped State Plane](#7-domain-scoped-state-plane)
  - [7.1 Agent Registry](#71-agent-registry)
  - [7.2 Clock Service](#72-clock-service)
  - [7.3 Intent State Registry](#73-intent-state-registry)
  - [7.4 Settlement Router](#74-settlement-router)
  - [7.5 Failure Detector](#75-failure-detector)
- [8. Executive Plane](#8-executive-plane)
  - [8.1 System 3: Operational Control](#81-system-3-operational-control)
  - [8.2 System 4: Strategic Intelligence](#82-system-4-strategic-intelligence)
  - [8.3 System 5: G-Class Governance](#83-system-5-g-class-governance)
  - [8.4 The System 3-System 4 Communication Protocol](#84-the-system-3-system-4-communication-protocol)
  - [8.5 Why Three Systems, Not Two or Four](#85-why-three-systems-not-two-or-four)
- [9. Graduated Sovereignty Model](#9-graduated-sovereignty-model)
  - [9.1 The Sovereignty Deadlock Problem](#91-the-sovereignty-deadlock-problem)
  - [9.2 Three-Tier Formal Specification](#92-three-tier-formal-specification)
  - [9.3 Sovereignty Relaxation Protocol](#93-sovereignty-relaxation-protocol)
  - [9.4 Safety Guarantees](#94-safety-guarantees)
- [10. Recursive Decomposition Hierarchy](#10-recursive-decomposition-hierarchy)
  - [10.1 Overview](#101-overview)
  - [10.2 Global Executive (GE)](#102-global-executive-ge)
  - [10.3 Locus Decomposer (LD)](#103-locus-decomposer-ld)
  - [10.4 Parcel Executor (PE)](#104-parcel-executor-pe)
  - [10.5 Cross-Level Communication Protocol](#105-cross-level-communication-protocol)
  - [10.6 Locus Fault Tolerance](#106-locus-fault-tolerance)
- [11. Integration Contracts](#11-integration-contracts)
  - [11.1 RIF <-> C3 Tidal Noosphere](#111-rif---c3-tidal-noosphere)
  - [11.2 RIF <-> Native Communication Stack](#112-rif---native-communication-stack)
  - [11.3 RIF <-> C5 PCVM](#113-rif---c5-pcvm)
  - [11.4 RIF <-> C6 EMA](#114-rif---c6-ema)
  - [11.5 RIF <-> C8 DSF Settlement Plane](#115-rif---c8-dsf-settlement-plane)
- [12. Intent Admission Control](#12-intent-admission-control)
  - [12.1 Gate Architecture](#121-gate-architecture)
  - [12.2 Admission Criteria](#122-admission-criteria)
  - [12.3 Security Properties](#123-security-properties)
  - [12.4 Rejection and Appeal](#124-rejection-and-appeal)
- [13. Scalability and Security](#13-scalability-and-security)
  - [13.1 Overhead Model](#131-overhead-model)
  - [13.2 Cross-Locus Bottleneck Analysis](#132-cross-locus-bottleneck-analysis)
  - [13.3 Degradation Profiles](#133-degradation-profiles)
  - [13.4 Adversarial Defenses](#134-adversarial-defenses)
  - [13.5 Byzantine Tolerance](#135-byzantine-tolerance)
  - [13.6 Partition Safety Properties](#136-partition-safety-properties)
- [14. Deployment Roadmap](#14-deployment-roadmap)
  - [14.1 Phase 1: Bootstrap (1-100 Agents)](#141-phase-1-bootstrap-1100-agents)
  - [14.2 Phase 2: Multi-Locus (100-1,000 Agents)](#142-phase-2-multi-locus-1001000-agents)
  - [14.3 Phase 3: Full Hierarchy (1,000-10,000 Agents)](#143-phase-3-full-hierarchy-100010000-agents)
  - [14.4 Phase 4: Planetary Scale (10,000-100,000 Agents) — Aspirational](#144-phase-4-planetary-scale-10000100000-agents--aspirational)
  - [14.5 Hard Gate Experiment Designs](#145-hard-gate-experiment-designs)
  - [14.6 Risk Mitigation](#146-risk-mitigation)
  - [14.7 Phase Transition Summary](#147-phase-transition-summary)
- [15. Conclusion](#15-conclusion)
  - [15.1 Summary of Contributions](#151-summary-of-contributions)
  - [15.2 Open Research Questions](#152-open-research-questions)
  - [15.3 Relationship to Broader Atrahasis Vision](#153-relationship-to-broader-atrahasis-vision)
- [Appendix A: Complete Intent Quantum JSON Schema (Normative)](#appendix-a-complete-intent-quantum-json-schema-normative)
- [Appendix B: Decomposition Algebra Formal Rules](#appendix-b-decomposition-algebra-formal-rules)
- [Appendix C: Sovereignty Invariant Catalog](#appendix-c-sovereignty-invariant-catalog)
- [Appendix D: Message Type Catalog](#appendix-d-message-type-catalog)
- [Appendix E: Parameter Reference](#appendix-e-parameter-reference)
- [Appendix F: Glossary](#appendix-f-glossary)
- [Appendix G: Test Vectors](#appendix-g-test-vectors)
- [Appendix H: Changelog](#appendix-h-changelog)

---

## 1. Abstract

The Recursive Intent Fabric (RIF) is a two-plane orchestration architecture that replaces the previously unspecified Coordinated Intent Orchestration System (CIOS) within the Atrahasis agent coordination stack. RIF solves a fundamental paradox in planetary-scale AI coordination: how to provide coherent goal decomposition and resource management across thousands of autonomous agents while respecting the sovereignty guarantees that make those agents trustworthy in the first place.

The architecture separates concerns into a **Domain-Scoped State Plane** — five infrastructure services (Agent Registry, Clock Service, Intent State Registry, Settlement Router, Failure Detector) replicated within each C3 locus using CRDTs and vector clocks — and an **Executive Plane** modeled on Stafford Beer's Viable System Model, comprising System 3 (Operational Control), System 4 (Strategic Intelligence), and System 5 (G-Class Governance). This separation ensures that operational state remains local to where it is needed while strategic and governance functions span loci only when necessary.

RIF introduces the **Intent Quantum** as its fundamental unit of work: a self-describing goal with typed semantics (GOAL, DIRECTIVE, QUERY, OPTIMIZATION), machine-evaluable success criteria, resource bounds, decomposition constraints, and a W3C PROV provenance chain. Intents traverse a five-state lifecycle (PROPOSED, DECOMPOSED, ACTIVE, COMPLETED, DISSOLVED) and decompose recursively through a **formal decomposition algebra** that maps onto C3's five operation classes (M/B/X/V/G). The algebra provides proven termination and cycle-freedom guarantees via a well-founded lexicographic ordering on (operation class rank, remaining depth).

A **graduated sovereignty model** with three tiers — constitutional (inviolable), operational (relaxable by 90% supermajority), and coordination (advisory) — resolves the tension between orchestration effectiveness and subsystem autonomy. System 4's anticipatory planning reads C6 EMA projections in a strictly read-only mode, with oscillation dampening via cool-down timers, similarity detection, and stability gating. System 5 maps directly onto C3's existing G-class governance mechanism, adding no new governance primitives.

The Global Executive uses the **HotStuff BFT consensus protocol** (Yin et al., 2019) for cross-locus coordination, providing O(n) message complexity per round via threshold signature aggregation — a significant improvement over classic PBFT's O(n^2). HotStuff's pipelined three-phase commit (PREPARE, PRE-COMMIT, COMMIT) and simple leader rotation ensure both high throughput and robust liveness under partial synchrony.

The architecture targets 1,000-10,000 agents as its validated design point. Sub-linear scaling is achievable when at least 80% of intents are locus-local; the Global Executive becomes a bottleneck when cross-locus intents exceed 20%. RIF delegates scheduling to C3, settlement to C8 DSF, credibility to C5 PCVM, knowledge metabolism to C6 EMA, and canonical claim/provenance carriage to the Alternative C communication stack — it orchestrates without duplicating.

---

## 2. Introduction and Motivation

### 2.1 The Orchestration Problem

Consider a system of ten thousand autonomous AI agents distributed across hundreds of semantic domains, collectively performing verified knowledge work — generating claims, verifying evidence, resolving contradictions, governing their own operational parameters. Each agent is sovereign in the sense that it holds cryptographic identity, staked collateral, and independently verifiable reputation. The subsystems that support this work — tidal scheduling (C3), native claim semantics and lineage (`C38`-`C42`, `T-290`), credibility verification (C5), knowledge metabolism (C6) — are each designed to operate without central direction. They are autonomous by construction, not by accident.

Now ask: how does a high-level goal — "achieve 95% accuracy on climate prediction within 100 epochs" — become concrete work that these agents actually perform?

This is the orchestration problem. It is distinct from scheduling (C3 handles that), from verification (C5 handles that), from knowledge lifecycle management (C6 handles that), and from native claim semantics and lineage (handled by the Alternative C stack). Orchestration sits above all four: it translates goals into the language these subsystems understand, decomposes complex objectives into tasks that individual agents can execute within single tidal epochs, manages the lifecycle of those tasks from proposal through completion, and handles the inevitable failures that arise in distributed systems.

The Atrahasis architecture, as specified through C3-C6, had a conspicuous gap. The Coordinated Intent Orchestration System (CIOS) was referenced in eight or more documents but never formally specified. It was an implied centralized executive coordinating decentralized autonomous subsystems — a conceptual contradiction that became increasingly untenable as the autonomous subsystems grew more sophisticated. CIOS needed to answer three questions it had never been asked:

1. **Decomposition**: How does a high-level goal become concrete, agent-executable work assignments with formal termination guarantees?
2. **Resource management**: How does the system ensure that decomposed tasks do not collectively exceed the resources available, and how are unused resources reclaimed?
3. **Governance integration**: How does the orchestration layer respect the sovereignty constraints that make the underlying systems trustworthy?

RIF is the answer to all three.

### 2.2 Why Existing Approaches Fail

The orchestration problem for planetary-scale AI coordination differs from any problem that existing systems were designed to solve. This is not a rhetorical claim — it is a structural observation about why off-the-shelf solutions are insufficient.

**Centralized orchestration creates a single point of failure and a throughput ceiling.** A centralized executive that performs goal decomposition via LLM inference incurs O(goals x inference_cost) computational overhead. At 10,000 agents generating hundreds of goals per epoch, this becomes the system's throughput bottleneck. More fundamentally, a single coordinator contradicts the sovereignty guarantees that make autonomous agents trustworthy. If one entity can override any agent's behavior, the system's trust model collapses.

**Traditional workflow engines lack intent lifecycle semantics.** Systems like Temporal and Apache Airflow manage task execution admirably, but they treat tasks as opaque work items with binary outcomes (success/failure). They have no concept of typed intents with machine-evaluable success criteria, no formal decomposition algebra, and no mechanism for partial success evaluation. They cannot express "achieve 95% accuracy" as a first-class lifecycle object that decomposes, monitors its own progress, and recomposes on partial failure.

**Kubernetes-style orchestration assumes fungible workers.** Container orchestrators like Kubernetes and Borg assign workloads to nodes based on resource requests and node capacity. They assume that any node with sufficient resources can run any workload. In Atrahasis, agents are not fungible — they have domain-specific capabilities, cryptographic identities, stake positions, and reputation scores. The assignment of a verification task to an agent with low PCVM credibility is not merely suboptimal; it violates the system's trust model.

**Intent-based networking (IBN) addresses the wrong layer.** IETF RFC 9315 formalizes intent as a declarative specification of network configuration. IBN systems translate "ensure 99.9% uptime for service X" into router configurations. This is valuable but operates at the infrastructure layer, not the application layer. RIF's intents are epistemic — they concern knowledge claims, verification procedures, and governance decisions, not network topology.

**No existing system provides formal decomposition guarantees.** Hierarchical Task Network (HTN) planners decompose abstract tasks into primitive operations, but they do not provide formal proofs of termination or cycle-freedom in the context of distributed execution with resource bounds. BDI architectures model agent intentions but do not address multi-agent goal decomposition at scale.

### 2.3 What RIF Contributes

RIF's contributions are architectural, formal, and integrative:

| Contribution | Description |
|---|---|
| **Intent Quantum** | A self-describing work unit with typed semantics, lifecycle management, success criteria, resource bounds, and provenance. Unlike workflow tasks, intents carry their own evaluation logic. |
| **Formal Decomposition Algebra** | Operation-class-aware decomposition with proven termination (via well-founded lexicographic ordering) and cycle-freedom (via strict descent). No existing orchestration system provides comparable formal guarantees. |
| **Two-Plane Separation** | Domain state replicates per-locus via CRDTs with bounded bandwidth; executive functions span loci only when necessary. This achieves sub-linear scaling when most work is locus-local. |
| **VSM-Aligned Executive** | System 3 (operational), System 4 (strategic), System 5 (governance) provide a principled separation of present-focused operations from future-focused planning, with governance as arbiter — not as a monolithic executive. |
| **Graduated Sovereignty** | Three-tier sovereignty model (constitutional/operational/coordination) resolves the paradox between orchestration effectiveness and subsystem autonomy. |
| **Memoized Decomposition** | Prior decomposition plans are cached and delta-adjusted on reuse, amortizing the cost of repeated similar intents. |
| **Resource Bound Preservation** | Formal proof that child intents cannot collectively exceed parent resource envelopes, with explicit handling of additive vs. shared resources. |
| **Shared Resource Contention Protocol** | Detection, resolution, and backpressure mechanisms for managing concurrent access to agents, parcels, and capacity slices. |

### 2.4 Position in the Atrahasis Stack

RIF sits above the four substrate components and below external goal sources:

```
+=========================================================================+
|                     EXTERNAL GOAL SOURCES                               |
|  (Human operators, other AI systems, self-generated via System 4)       |
+=========================================================================+
                                |
                                v
+=========================================================================+
|                RECURSIVE INTENT FABRIC (C7 — THIS SPEC)                 |
|                                                                         |
|   Executive Plane: System 3 | System 4 | System 5                      |
|   Domain State Plane: Registry | Clock | ISR | Settlement | Failure    |
+=========================================================================+
          |              |            |              |            |
          v              v            v              v            v
+================+ +=========+ +==========+ +=========+ +================+
| C3 Tidal       | | Native Comm | | C5 PCVM  | | C6 EMA  | | C8 DSF         |
| Noosphere      | |         | |          | |         | | (settlement)   |
| (scheduling,   | |(claims, | |(VTDs,    | |(epist.  | |(EABS, budgets, |
|  loci, parcels,| | evid.,  | | MCTs,    | | quanta, | | capacity mkt)  |
|  M/B/X/V/G)    | | prov.)  | | cred.)   | | SHREC)  | |                |
+================+ +=========+ +==========+ +=========+ +================+
```

RIF's relationship to each substrate is deliberately asymmetric:

- **C3 (Tidal Noosphere)**: RIF's primary substrate. Leaf intents execute as C3 operation-class tasks within tidal epochs. RIF reads locus topology, epoch boundaries, and VRF outputs. RIF writes leaf intent execution requests. C3's scheduling sovereignty is constitutional — RIF cannot override tidal assignment.

- **Alternative C communication stack**: RIF uses native sovereign claim objects and lineage references to express intent outcomes as verifiable claims. Every intent state transition carries native provenance. RIF writes intent success/failure claims through canonical message and semantic contracts; final claim semantics remain subordinate to C5 and `AXIP-v1`.

- **C5 (PCVM)**: RIF reads agent credibility scores to inform assignment decisions and failure detection. The Failure Detector integrates PCVM credibility to weight liveness reports and detect Byzantine agents. PCVM's claim classification is constitutionally sovereign — RIF cannot override VTD or MCT assessments.

- **C6 (EMA)**: System 4 reads EMA epistemic quanta projections in a strictly read-only mode for horizon scanning and anticipatory planning. RIF writes nothing to EMA. EMA's canonical source status and metabolic phase timing are constitutionally and operationally sovereign respectively.

- **C8 (DSF)**: The Settlement Router forwards all intent-related economic transactions to C8 DSF's settlement ledger, accessed via C3's CRDT replication infrastructure. C8 is the canonical settlement authority; RIF does not settle independently.

---

## 3. Background and Related Work

RIF draws on five intellectual traditions, synthesizing elements from each while departing from all of them in ways that the distributed AI orchestration problem demands.

### 3.1 HTN Planning and BDI Architectures

**Hierarchical Task Network (HTN) planning** (Erol, Hendler, and Nau, 1994) decomposes abstract tasks into primitive operations through recursive application of decomposition methods. An HTN planner maintains a task network — a partially ordered set of tasks with constraints — and applies methods that replace non-primitive tasks with sub-networks of simpler tasks. The process terminates when all tasks in the network are primitive.

RIF's decomposition engine is structurally an HTN planner, but differs in three critical respects. First, RIF's decomposition operates over typed intents with machine-evaluable success criteria rather than STRIPS-style preconditions and effects. The success criteria language (Section 5.4) enables evaluation of partial success, threshold achievement, and temporal bounds — concepts absent from classical HTN planning. Second, RIF provides formal termination and cycle-freedom proofs grounded in the operation-class partial order (Section 6), whereas HTN planners typically rely on finite method libraries for termination. Third, RIF's decomposition is resource-bounded: every decomposition step must provably preserve the parent's resource envelope, a constraint that HTN planners do not address.

**Belief-Desire-Intention (BDI) architectures** (Rao and Georgeff, 1995) model agents as having beliefs about the world, desires they wish to achieve, and intentions they have committed to pursuing. BDI agents select plans from a plan library based on their current beliefs and desires, committing to intentions that become the focus of execution.

RIF's intent quantum is philosophically descended from BDI intentions but operates at the system level rather than the individual agent level. A BDI agent maintains its own intention stack; RIF maintains an intent tree that spans many agents across multiple loci. The key departure is that RIF's intents are first-class lifecycle objects with formal state machines, whereas BDI intentions are internal mental states of individual agents.

### 3.2 Stafford Beer's Viable System Model

The Viable System Model (VSM), developed by Stafford Beer (1972, 1979, 1985), describes the organizational structure necessary for any system to be viable — that is, capable of maintaining its identity and purpose in a changing environment. The VSM identifies five necessary subsystems:

- **System 1** (Operations): The primary activities that produce the system's outputs.
- **System 2** (Coordination): Anti-oscillatory mechanisms that prevent System 1 units from interfering with each other.
- **System 3** (Internal Control): Resource allocation, performance monitoring, and operational optimization across System 1 units.
- **System 3*** (Audit): Sporadic investigation to verify that System 1 reports match reality.
- **System 4** (Intelligence): Environmental scanning, strategic planning, and adaptation.
- **System 5** (Policy): Identity, purpose, and conflict resolution between Systems 3 and 4.

The model's deepest insight is recursion: each System 1 unit is itself a viable system with its own five subsystems, and the whole organization is a System 1 unit of a larger viable system.

RIF maps onto the VSM as follows:

| VSM System | Atrahasis Mapping | Notes |
|---|---|---|
| System 1 | C3 parcels and their agent workloads | Already exists; RIF does not modify |
| System 2 | C3 tidal scheduling | Already exists; RIF does not modify |
| System 3 | RIF System 3 (Operational Control) | **NEW** — decomposition, resource optimization, failure playbooks |
| System 3* | C5 PCVM + Sentinel | Already exists; RIF integrates via Failure Detector |
| System 4 | RIF System 4 (Strategic Intelligence) | **NEW** — horizon scanning, anticipatory planning, adaptation proposals |
| System 5 | C3 G-class governance + RIF System 5 interface | Governance mechanism exists; RIF provides the executive interface |

The critical insight from Beer that shaped RIF's design is the **System 3/System 4 distinction**. System 3 manages the present — optimizing what the system is currently doing. System 4 manages the future — scanning the environment for changes that require adaptation. These two functions are inherently in tension: System 3 wants stability (to optimize current operations), while System 4 wants change (to adapt to emerging conditions). System 5 exists precisely to mediate this tension.

RIF implements this tension explicitly through the Adaptation Proposal Protocol (Section 8.4), where System 4 can only propose changes, System 3 evaluates their operational impact, and System 5 arbitrates disagreements. This prevents the pathological case where a single executive both plans changes and implements them without checks.

### 3.3 Intent-Based Networking

Intent-Based Networking (IBN), formalized in IETF RFC 9315, introduced the concept of expressing desired outcomes rather than specific configurations. An IBN system accepts declarative intents ("ensure service X has 99.9% uptime") and translates them into network configurations, continuously monitoring whether the intent is satisfied and adjusting configurations as needed.

RIF borrows three concepts from IBN:

1. **Intent as a first-class object** with lifecycle management. IBN systems track whether an intent is being satisfied and can distinguish between "intent accepted," "intent active," and "intent fulfilled." RIF's five-state lifecycle (Section 5.3) extends this with DECOMPOSED (a state absent in IBN because network intents are typically atomic) and DISSOLVED (explicit garbage collection).

2. **Continuous evaluation** of intent satisfaction. IBN systems do not simply execute-and-forget; they continuously verify that the intent remains satisfied. RIF adapts this to epistemic work, where success criteria evaluation occurs when leaf descendants report results and may trigger re-decomposition on partial failure.

3. **Declarative rather than imperative specification**. IBN intents describe what, not how. RIF's GOAL intent type follows this principle — a GOAL specifies success criteria but not execution instructions, leaving decomposition to System 3.

RIF departs from IBN in a fundamental way: IBN intents translate into configurations of existing infrastructure, whereas RIF intents decompose into work that agents perform. IBN operates at the infrastructure layer; RIF operates at the epistemic application layer. IBN's "translation" step maps intents to a known configuration space; RIF's "decomposition" step maps intents to a dynamically constructed tree of sub-intents, which is a fundamentally harder problem requiring the formal algebra of Section 6.

### 3.4 Workflow Engines and Saga Patterns

**Temporal** (formerly Cadence) and similar workflow engines provide durable execution of long-running business processes. They guarantee that a workflow will complete even if individual workers crash, by persisting workflow state and replaying from checkpoints. The saga pattern (Garcia-Molina and Salem, 1987) extends this to distributed transactions: when a multi-step transaction partially fails, compensating transactions undo the completed steps.

RIF incorporates both concepts:

- **Durable intent state**: The Intent State Registry (Section 7.3) persists every intent and every state transition with causal stamps. Intent trees survive component crashes and are reconstructable from the ISR's CRDT-replicated state.

- **Compensation protocols**: RIF implements saga-style compensation (Section 8.1) for partial decomposition or execution failures. When a child intent fails and recovery is not possible, compensation transactions reverse the settlements of completed siblings.

Where RIF diverges from workflow engines is in the nature of the work being coordinated. Workflow engines execute predefined step sequences with known compensation logic. RIF decomposes goals into step sequences at runtime using an inference-driven decomposition engine, and the compensation logic is derived from the decomposition structure rather than predefined. This makes RIF's coordination problem strictly harder: the system must reason about compensation for decomposition plans it created dynamically, not plans that a developer specified in advance.

### 3.5 Hierarchical Orchestration Systems

**Kubernetes** and **Google Borg** implement hierarchical orchestration for container workloads. Borg's architecture — a central Borgmaster with per-cell Borglets — inspired Kubernetes' control plane / kubelet separation. Both systems schedule work onto a pool of machines based on resource requests and constraints.

RIF's three-level decomposition hierarchy (Global Executive, Locus Decomposers, Parcel Executors) mirrors this pattern structurally. The Global Executive handles cross-locus intents (analogous to Borg's cross-cell scheduling), Locus Decomposers handle domain-local intents (analogous to cell-level scheduling), and Parcel Executors assign work to individual agents (analogous to Borglets).

The key difference is that Kubernetes assumes fungible nodes — any node with sufficient CPU and memory can run any container. RIF's agents are heterogeneous, with domain-specific capabilities, credibility scores, and stake positions. Assignment in RIF is a constraint satisfaction problem over capabilities, credibility, and resource bounds, not a bin-packing problem over CPU and memory. Furthermore, RIF's work items (intents) have success criteria that are evaluated post-execution, whereas Kubernetes pods either run or they do not.

### 3.6 How RIF Differs

The following table summarizes how RIF relates to each tradition:

| Tradition | What RIF Borrows | Where RIF Departs |
|---|---|---|
| HTN Planning | Recursive task decomposition via methods | Typed intents with success criteria; formal termination proofs; resource-bounded decomposition |
| BDI Architectures | Intentions as first-class objects with commitment | System-level intent trees spanning thousands of agents, not individual agent mental states |
| Viable System Model | System 3/4/5 separation; recursive structure | Computational implementation with formal protocols, not organizational theory; integration with operation-class algebra |
| Intent-Based Networking | Intent lifecycle; continuous evaluation; declarative spec | Epistemic application layer, not infrastructure; dynamic decomposition, not configuration translation |
| Workflow Engines / Sagas | Durable execution; compensation protocols | Runtime decomposition (not predefined workflows); inference-driven compensation |
| Kubernetes / Borg | Hierarchical orchestration; resource management | Heterogeneous agents with credibility; success criteria evaluation; sovereignty constraints |

What makes RIF genuinely novel is the combination: a system that decomposes goals like an HTN planner, manages its executive functions like a viable system, treats intents as lifecycle objects like an IBN system, provides durability and compensation like a workflow engine, and orchestrates hierarchically like Kubernetes — but does all of this for heterogeneous sovereign agents performing verified epistemic work at planetary scale.

---

## 4. Architecture Overview

### 4.1 Two-Plane Design

RIF's architecture separates into two planes with distinct replication models, failure domains, and scaling characteristics.

```
+=========================================================================+
|                        EXECUTIVE PLANE                                  |
|                                                                         |
|  +-------------------+  +---------------------+  +------------------+  |
|  |    SYSTEM 5        |  |     SYSTEM 4         |  |    SYSTEM 3       |  |
|  |  G-Class           |  |  Strategic            |  |  Operational      |  |
|  |  Governance        |  |  Intelligence         |  |  Control          |  |
|  |                    |  |                       |  |                   |  |
|  | - Constitutional   |  | - Horizon Scanning    |  | - Intent Decomp   |  |
|  |   consensus        |  | - Anticipatory        |  | - Resource Opt    |  |
|  | - Conflict         |  |   capacity planning   |  | - Perf Monitor    |  |
|  |   resolution       |  | - Adaptation          |  | - Failure Play    |  |
|  | - Sovereignty      |  |   proposals           |  | - Compensation    |  |
|  |   relaxation       |  | - Oscillation         |  | - Decomp Memo     |  |
|  | - Emergency        |  |   dampening           |  | - Contention Mgmt |  |
|  |   rollback         |  |                       |  |                   |  |
|  +--------+-----------+  +----------+------------+  +--------+----------+  |
|           |                         |                         |            |
|           |    S5 arbitrates        |   S4 proposes           |            |
|           +<------------------------+                         |            |
|           |                         +<------------------------+            |
|           |    S5 constrains S3     |   S3 reports to S4      |            |
|           +-------------------------------------------------->+            |
|                                                                            |
+=====+======================+===================+================+==========+
      |                      |                   |                |
      | G-class ops          | V-class verify    | X/B/M execute  | Events
      v                      v                   v                v
+=========================================================================+
|                   DOMAIN-SCOPED STATE PLANE                             |
|                        (per-locus replication)                          |
|                                                                         |
|  +---------------+  +-----------+  +--------+  +---------+  +--------+ |
|  | Agent         |  | Clock     |  | Intent |  | Settle- |  | Failure| |
|  | Registry      |  | Service   |  | State  |  | ment    |  | Detect-| |
|  | (CRDT)        |  | (NTP +    |  | Regis- |  | Router  |  | or     | |
|  |               |  |  Vector)  |  | try    |  | (ALO)   |  | (Sent.)| |
|  +-------+-------+  +-----+-----+  +---+----+  +----+----+  +---+----+ |
|          |                |             |            |            |      |
+=========================================================================+
           |                |             |            |            |
           v                v             v            v            v
+=========================================================================+
|                     SUBSTRATE LAYER                                     |
|                                                                         |
|  +------------------+  +--------+  +----------+  +---------+  +------+ |
|  | C3 Tidal         |  | Native Comm |  | C5 PCVM  |  | C6 EMA  |  |C8 DSF| |
|  | Noosphere        |  |        |  |          |  |         |  |      | |
|  | (loci, parcels,  |  |(claims,|  |(VTDs,    |  |(epist.  |  |(EABS,| |
|  |  tidal sched,    |  | evid., |  | MCTs,    |  | quanta, |  | set- | |
|  |  VRF, M/B/X/V/G) |  | prov.) |  | cred.)   |  | SHREC)  |  | tle) | |
|  +------------------+  +--------+  +----------+  +---------+  +------+ |
+=========================================================================+
```

**The Domain-Scoped State Plane** contains five infrastructure services. Each service is replicated within a C3 locus using CRDTs, with minimal cross-locus traffic. The key design property is *locality*: the vast majority of state reads and writes occur within a single locus. Cross-locus replication is limited to capability summaries (Agent Registry), vector clock updates (Clock Service), spanning intent stubs (ISR), and aggregate failure statistics (Failure Detector). This locality property is what enables sub-linear scaling.

**The Executive Plane** contains three systems that span loci as needed. System 3 (Operational Control) is the workhorse — it decomposes intents, optimizes resources, monitors performance, and handles failures. System 4 (Strategic Intelligence) is the forward-looking observer — it reads trends and proposes adaptations. System 5 (G-Class Governance) is the arbiter — it resolves conflicts, authorizes sovereignty relaxation, and enforces constitutional constraints.

The two planes communicate through well-defined contracts. The Executive Plane reads from and writes to the Domain State Plane's services. The Domain State Plane notifies the Executive Plane of events (agent failures, settlement backpressure, clock anomalies). The separation ensures that infrastructure failures (e.g., a CRDT divergence in the Agent Registry) do not directly crash executive functions, and that executive decisions (e.g., a faulty System 4 proposal) do not corrupt infrastructure state.

### 4.2 Component Inventory

| Component | Plane | Scope | Replication Model | Primary Substrate |
|---|---|---|---|---|
| Agent Registry | Domain State | Per-locus | CRDT (intra-locus: full; cross-locus: capability summaries) | C3 parcels |
| Clock Service | Domain State | Per-locus + federation | NTP + vector clocks | C3 epoch timing |
| Intent State Registry (ISR) | Domain State | Per-locus (spanning for cross-locus intents) | CRDT with 5% bandwidth cap | Native provenance lineage |
| Settlement Router | Domain State | Per-locus | At-least-once broker with WAL | C8 DSF settlement ledger |
| Failure Detector | Domain State | Per-locus | Sentinel-integrated quorum | C5 credibility |
| System 3 (Operational Control) | Executive | Cross-locus (leader per intent tree) | Leader election per intent tree | C3 operation classes |
| System 4 (Strategic Intelligence) | Executive | Global (read-only observers) | Stateless observers | C6 EMA projections |
| System 5 (G-Class Governance) | Executive | Global | C3 G-class BFT consensus | C3 constitutional consensus |

### 4.3 Design Principles

Four principles govern every design decision in RIF:

**Principle 1: Graduated Sovereignty.** Subsystem autonomy is not a binary property. RIF defines three sovereignty tiers:

- *Constitutional sovereignty* (inviolable): PCVM claim classification, VTD/MCT immutability, EMA canonical source status, DISSOLVED state irreversibility. These cannot be overridden under any circumstances — not by System 3, not by System 5, not by unanimous vote. They define what the system *is*.

- *Operational sovereignty* (default-on, relaxable via governance): VRF committee composition, EMA metabolic phase timing, SHREC budget allocations, operation class assignments. These can be temporarily relaxed by a 90% G-class supermajority vote with a maximum 50-epoch lease and automatic reversion.

- *Coordination sovereignty* (advisory): Agent task preferences, locus workload distribution hints, resource reservation suggestions. These are respected when possible but can be overridden by System 3 for load balancing.

**Principle 2: Recursion.** The three-level decomposition hierarchy (Global Executive, Locus Decomposers, Parcel Executors) mirrors C3's structural hierarchy (loci, parcels, agents). Each level can be understood as a viable system in the VSM sense. This recursive structure means that adding loci adds decomposition capacity proportionally, avoiding the centralized bottleneck that plagued the original CIOS concept.

**Principle 3: Formal Decomposition.** Intent decomposition is not a heuristic process — it is governed by a formal algebra with proven termination and cycle-freedom guarantees (Section 6). The operation-class partial order (G > V > X > B > M) constrains which child classes may appear, and the lexicographic ordering on (class rank, remaining depth) ensures that every decomposition chain is finite. This is not an aspirational property; it is a mathematical invariant.

**Principle 4: Substrate Awareness.** RIF does not reinvent scheduling, settlement, credibility, or knowledge metabolism. It delegates to C3, the native communication stack, C5, C6, and C8 respectively. This principle prevents RIF from becoming a second, incompatible implementation of functionality that already exists in the substrate. Every leaf intent becomes a C3 operation-class task; every intent outcome becomes a native sovereign claim object; every agent credibility check goes through C5 PCVM; every horizon scan reads C6 EMA projections; every settlement entry routes to C8 DSF.

### 4.4 Integration with Substrate Components

The following table specifies exactly what RIF reads from, writes to, and never touches in each substrate component:

| Substrate | RIF Reads | RIF Writes | RIF Never Touches |
|---|---|---|---|
| C3 Tidal Noosphere | Locus topology, parcel state, epoch boundaries, VRF outputs, operation class definitions | Leaf intent execution requests | Tidal scheduling assignments, VRF verifier selection, parcel boundaries |
| Native communication stack | Claim objects, evidence references, provenance chains | Intent success/failure claims, decomposition provenance | Claim content, evidence weighting, provenance semantics |
| C5 PCVM | Agent credibility scores (VTDs, MCTs), claim class assessments | Intent outcome verification requests, Byzantine evidence submissions | Claim classification (INV-M2), VTD/MCT values (INV-M7) |
| C6 EMA | Epistemic quanta projections, SHREC regulation state, coherence trends | Nothing (strictly read-only) | Canonical quanta (INV-E1), metabolic phases (INV-E3), SHREC allocations |
| C8 DSF | Settlement confirmation, idempotency enforcement, stake availability | Settlement entries (via Settlement Router) | Settlement computation algorithms, capacity market internals |

**Intent data flow through the substrate**:

```
                          EXTERNAL
                          REQUEST
                             |
                             v
                    +------------------+
                    |  Intent Proposal |
                    |  (PROPOSED)      |
                    +--------+---------+
                             |
                    validate & admit
                             |
                             v
                    +------------------+
                    |  System 3:       |
                    |  Decomposition   |
                    |  Engine          |
                    +--------+---------+
                             |
              decompose into child intents
                             |
               +-------------+-------------+
               |             |             |
               v             v             v
          +---------+   +---------+   +---------+
          | Child 1 |   | Child 2 |   | Child 3 |
          | (DECOMP)|   | (DECOMP)|   | (DECOMP)|
          +----+----+   +----+----+   +----+----+
               |             |             |
          further decomp     |        leaf (M-class)
          if needed          |             |
               |             v             v
               |        leaf (B-class) +--------+
               v             |         | ACTIVE |
          +---------+        v         +---+----+
          | Sub-    |   +--------+         |
          | children|   | ACTIVE |     execute via
          +---------+   +---+----+     C3 scheduler
               |            |             |
               v            v             v
          all children  settle via    result parcel
          complete      C8 DSF        written
               |            |             |
               +------+-----+------+------+
                      |            |
                      v            v
               +------------------+
               |  Parent intent   |
               |  evaluates       |
               |  success criteria|
               +--------+---------+
                        |
                   criteria met?
                   /           \
                 yes            no
                 /               \
                v                 v
         +----------+     +-------------+
         |COMPLETED |     | Compensate  |
         +----+-----+     | or re-decomp|
              |           +-------------+
              v
         +-----------+
         | DISSOLVED |
         | (GC after |
         |  100 ep.) |
         +-----------+
```

---

## 5. Intent Quantum

The intent quantum is RIF's fundamental primitive — the atomic unit of work, goal, query, or optimization that flows through the system. Unlike traditional task queues where work items are opaque payloads with a callback, an intent quantum is a self-describing, typed, lifecycle-managed object that carries its own success criteria, resource bounds, decomposition constraints, and provenance chain.

The name "quantum" is deliberate: an intent quantum is the smallest indivisible unit of purposeful action in the system. A leaf intent quantum maps to exactly one C3 operation-class execution by exactly one agent within exactly one tidal epoch. Non-leaf intents decompose into smaller quanta, but the decomposition is governed by formal rules (Section 6) that guarantee termination.

### 5.1 Formal Definition and JSON Schema

An intent quantum is formally defined as a tuple:

```
IQ = (id, type, class, origin, scope, description, content, authorization,
      criteria, bounds, constraints, strategy, inputs, output,
      compensation, lifecycle_state, parent_id, child_ids, provenance, metadata)
```

The complete JSON Schema follows. This schema is normative — all RIF implementations must accept and produce intent quanta conforming to this schema. This unified schema resolves 37 field-level conflicts between the v1.0 Section 5.1 and Appendix A schemas (see Appendix H, Changelog entry PA-1/F47 for the complete conflict inventory).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.org/rif/intent-quantum/v2",
  "title": "IntentQuantum",
  "description": "The fundamental unit of work in the Recursive Intent Fabric. A self-describing goal with typed semantics, machine-evaluable success criteria, resource bounds, decomposition constraints, and W3C PROV provenance.",
  "type": "object",
  "properties": {
    "intent_id": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "Globally unique 256-bit identifier (64 hex characters)"
    },
    "intent_type": {
      "type": "string",
      "enum": ["GOAL", "DIRECTIVE", "QUERY", "OPTIMIZATION"],
      "description": "GOAL=open-ended objective, DIRECTIVE=specific instruction, QUERY=information request, OPTIMIZATION=improve existing state"
    },
    "operation_class": {
      "type": ["string", "null"],
      "enum": ["M", "B", "X", "V", "G", null],
      "description": "C3 operation class. Null for non-leaf intents; derived at leaf level by map_to_operation_class()."
    },
    "origin": {
      "type": "object",
      "properties": {
        "proposer_agent_id": { "type": "string" },
        "proposer_locus_id": { "type": "string" },
        "proposal_epoch": { "type": "integer" },
        "causal_stamp": { "$ref": "#/$defs/CausalStamp" },
        "provenance_chain": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Native claim object IDs forming the provenance chain"
        }
      },
      "required": ["proposer_agent_id", "proposer_locus_id",
                    "proposal_epoch", "causal_stamp"]
    },
    "scope": {
      "type": "object",
      "properties": {
        "domain": { "type": "string" },
        "target_loci": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "target_parcels": {
          "type": "array",
          "items": { "type": "string" }
        },
        "requires_exclusive_access": { "type": "boolean", "default": false },
        "is_bounded_local": { "type": "boolean", "default": true },
        "affects_governance": { "type": "boolean", "default": false },
        "requires_verification": { "type": "boolean", "default": false }
      },
      "required": ["domain", "target_loci"]
    },
    "description": {
      "type": "string",
      "maxLength": 4096,
      "description": "Human-readable description of the intent's purpose"
    },
    "content": {
      "type": ["string", "null"],
      "description": "Structured intent specification in natural language or domain-specific format. Null for intents where description is sufficient."
    },
    "authorization": {
      "type": ["object", "null"],
      "description": "GovernanceToken; required for cross-locus and G-class intents, null otherwise.",
      "properties": {
        "token_id": { "type": "string" },
        "granted_by": { "type": "string", "description": "G-class vote ID or System 5 authorization" },
        "scope": { "type": "string", "enum": ["CROSS_LOCUS", "G_CLASS", "SOVEREIGNTY_RELAXATION"] },
        "expiry_epoch": { "type": "integer" }
      }
    },
    "success_criteria": {
      "type": "object",
      "properties": {
        "criteria_type": {
          "type": "string",
          "enum": ["PREDICATE", "THRESHOLD", "TEMPORAL", "COMPOSITE"],
          "description": "Discriminator for which criteria fields are populated"
        },
        "predicates": {
          "type": "array",
          "items": { "$ref": "#/$defs/SuccessPredicate" }
        },
        "thresholds": {
          "type": "array",
          "items": { "$ref": "#/$defs/SuccessThreshold" }
        },
        "temporal_bound": { "$ref": "#/$defs/TemporalBound" },
        "aggregation": {
          "type": "string",
          "enum": ["ALL_REQUIRED", "WEIGHTED_THRESHOLD", "ANY_REQUIRED"],
          "default": "ALL_REQUIRED",
          "description": "ALL_REQUIRED=all predicates/thresholds must pass, WEIGHTED_THRESHOLD=weighted sum >= threshold, ANY_REQUIRED=at least one must pass"
        },
        "threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Required when aggregation=WEIGHTED_THRESHOLD: minimum weighted sum of predicate results"
        }
      },
      "required": ["criteria_type"]
    },
    "resource_bounds": { "$ref": "#/$defs/ResourceBounds" },
    "constraints": {
      "type": "object",
      "properties": {
        "max_depth": {
          "type": "integer", "minimum": 1, "maximum": 20, "default": 10
        },
        "decomposition_budget_ms": {
          "type": "integer", "minimum": 100, "maximum": 60000, "default": 5000
        },
        "decomposition_token_limit": {
          "type": "integer", "minimum": 100, "maximum": 1000000, "default": 10000
        },
        "deadline_epoch": { "type": ["integer", "null"] },
        "priority": {
          "type": "integer", "minimum": 0, "maximum": 100, "default": 50
        },
        "min_agent_credibility": {
          "type": "number", "minimum": 0, "maximum": 1, "default": 0.5
        },
        "allow_spanning": { "type": "boolean", "default": true }
      },
      "required": ["max_depth", "decomposition_budget_ms",
                    "decomposition_token_limit"]
    },
    "decomposition_strategy": {
      "type": ["string", "null"],
      "enum": ["RECURSIVE", "PARALLEL", "SEQUENTIAL", "CONDITIONAL", null],
      "default": null,
      "description": "Null when proposed; System 3 assigns via select_strategy(). RECURSIVE is default when assigned."
    },
    "input_references": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ref_type": {
            "type": "string",
            "enum": ["PARCEL", "INTENT_OUTPUT", "EMA_QUANTUM",
                     "NATIVE_CLAIM_OBJECT", "EXTERNAL"]
          },
          "ref_id": { "type": "string" },
          "required": { "type": "boolean", "default": true }
        },
        "required": ["ref_type", "ref_id"]
      }
    },
    "output_spec": {
      "type": "object",
      "properties": {
        "output_type": {
          "type": "string",
          "enum": ["PARCEL", "CLAIM", "METRIC", "NONE"]
        },
        "output_schema_ref": { "type": ["string", "null"] },
        "output_parcel_target": { "type": ["string", "null"] }
      },
      "required": ["output_type"]
    },
    "compensation": {
      "type": ["object", "null"],
      "properties": {
        "strategy": {
          "type": "string",
          "enum": ["REVERSE_SETTLEMENT", "RE_DECOMPOSE", "ESCALATE",
                   "SAGA_ROLLBACK", "COMPENSATING_INTENT", "ABANDON", "NONE"],
          "description": "REVERSE_SETTLEMENT=undo settlement entries, RE_DECOMPOSE=retry with different strategy, ESCALATE=push to parent, SAGA_ROLLBACK=execute compensation intents in reverse, COMPENSATING_INTENT=execute specified compensation intent, ABANDON=mark as failed with no compensation, NONE=no compensation needed"
        },
        "compensation_intents": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Intent IDs to execute for SAGA_ROLLBACK or COMPENSATING_INTENT strategies"
        },
        "timeout_epochs": { "type": "integer", "description": "Maximum epochs allowed for compensation to complete" }
      }
    },
    "lifecycle_state": {
      "type": "string",
      "enum": ["PROPOSED", "DECOMPOSED", "ACTIVE", "COMPLETED", "DISSOLVED"],
      "description": "Current lifecycle state. Set to PROPOSED on creation."
    },
    "parent_intent_id": {
      "type": ["string", "null"],
      "description": "Null for root intents"
    },
    "child_intent_ids": {
      "type": "array",
      "items": { "type": "string" },
      "default": []
    },
    "provenance": {
      "type": ["object", "null"],
      "description": "W3C PROV compatible provenance record. Distinct from origin.provenance_chain (which tracks native claim object IDs)."
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_epoch": { "type": "integer" },
        "last_modified_epoch": { "type": "integer" },
        "tags": { "type": "array", "items": { "type": "string" } },
        "annotations": {
          "type": "object",
          "additionalProperties": { "type": "string" }
        }
      }
    }
  },
  "required": ["intent_id", "intent_type", "origin", "scope",
               "description", "success_criteria", "resource_bounds",
               "constraints", "output_spec", "lifecycle_state"],

  "$defs": {
    "CausalStamp": {
      "type": "object",
      "properties": {
        "wall_time_ms": { "type": "integer" },
        "vector_clock": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "epoch": { "type": "integer" },
        "locus_id": { "type": "string" },
        "agent_id": { "type": "string" },
        "signature": {
          "type": "string",
          "description": "Ed25519 signature over (wall_time_ms, vector_clock, epoch, locus_id, agent_id)"
        }
      },
      "required": ["wall_time_ms", "vector_clock", "epoch",
                    "locus_id", "agent_id", "signature"]
    },
    "ResourceBounds": {
      "type": "object",
      "properties": {
        "compute_tokens": {
          "type": "integer", "minimum": 1,
          "description": "Maximum compute tokens (additive resource)"
        },
        "wall_time_ms": {
          "type": "integer", "minimum": 1,
          "description": "Maximum wall-clock time in milliseconds (additive resource)"
        },
        "bandwidth_bytes": {
          "type": "integer", "minimum": 0,
          "description": "Maximum network bandwidth in bytes (shared resource)"
        },
        "iops": {
          "type": "integer", "minimum": 0,
          "description": "Maximum I/O operations per second (shared resource)"
        },
        "storage_bytes": {
          "type": "integer", "minimum": 0,
          "description": "Maximum storage consumption in bytes (additive resource)"
        },
        "stake_required": {
          "type": "number", "minimum": 0,
          "description": "Minimum stake the executing agent must hold"
        }
      },
      "required": ["compute_tokens", "wall_time_ms"]
    },
    "SuccessPredicate": {
      "type": "object",
      "properties": {
        "predicate_id": { "type": "string" },
        "observable": {
          "type": "string",
          "description": "The metric or state observable to evaluate"
        },
        "operator": {
          "type": "string",
          "enum": ["EQ", "NEQ", "GT", "GTE", "LT", "LTE",
                   "CONTAINS", "MATCHES", "EXISTS"]
        },
        "expected_value": {},
        "expression": {
          "type": ["string", "null"],
          "description": "Optional machine-evaluable expression override. When present, takes precedence over observable+operator+expected_value."
        },
        "weight": {
          "type": "number", "minimum": 0, "maximum": 1, "default": 1.0,
          "description": "Weight for WEIGHTED_THRESHOLD aggregation"
        },
        "required": {
          "type": "boolean", "default": true,
          "description": "If true, this predicate must pass regardless of aggregation mode"
        },
        "description": { "type": "string" }
      },
      "required": ["predicate_id", "observable", "operator", "expected_value"]
    },
    "SuccessThreshold": {
      "type": "object",
      "properties": {
        "threshold_id": { "type": "string" },
        "metric": { "type": "string" },
        "operator": { "type": "string", "enum": ["GTE", "LTE"] },
        "value": { "type": "number" },
        "description": { "type": "string" }
      },
      "required": ["threshold_id", "metric", "operator", "value"]
    },
    "TemporalBound": {
      "type": "object",
      "properties": {
        "bound_type": {
          "type": "string",
          "enum": ["WITHIN_EPOCHS", "BEFORE_EPOCH", "AFTER_EPOCH"]
        },
        "epoch_value": { "type": "integer" },
        "description": { "type": "string" }
      },
      "required": ["bound_type", "epoch_value"]
    }
  }
}
```

**Migration Notes** (for implementers upgrading from v1.0):
- The `composition` field (values `"AND"`, `"OR"`) maps to `aggregation` as: `AND` -> `ALL_REQUIRED`, `OR` -> `ANY_REQUIRED`.
- The `max_compensation_epochs` field maps to `timeout_epochs`.
- The `network_bytes` field maps to `bandwidth_bytes`.
- The `decomposition_budget_tokens` field maps to `decomposition_token_limit`.
- Appendix A is the sole normative schema. The v1.0 Section 5.1 and Appendix A schemas are both superseded by this unified definition.


### 5.2 The Four Intent Types

RIF defines four intent types, each with distinct semantics, decomposition behavior, and operation-class mappings.

#### 5.2.1 GOAL

A GOAL is a high-level objective defined by success criteria rather than execution instructions. Goals are always decomposed -- they never appear as leaf intents. If a GOAL reaches leaf level during decomposition, it indicates a failure in the decomposition engine (the goal is too abstract to execute directly).

**Semantics**: "Achieve this outcome, however the system sees fit."

**Decomposition**: Always decomposes into DIRECTIVE, QUERY, or OPTIMIZATION children (or sub-GOALs for large objectives). System 3 selects the decomposition strategy based on the goal's success criteria structure.

**Example**:
```json
{
  "intent_type": "GOAL",
  "operation_class": null,
  "description": "Achieve 95% accuracy on climate prediction domain within 100 epochs",
  "success_criteria": {
    "criteria_type": "COMPOSITE",
    "thresholds": [
      { "threshold_id": "accuracy", "metric": "climate.prediction.accuracy",
        "operator": "GTE", "value": 0.95 }
    ],
    "temporal_bound": { "bound_type": "WITHIN_EPOCHS", "epoch_value": 100 },
    "aggregation": "ALL_REQUIRED"
  }
}
```

#### 5.2.2 DIRECTIVE

A DIRECTIVE is a specific instruction to execute. Directives may decompose further (when complex) or may be leaf intents (when simple enough for a single agent in a single epoch). Leaf directives map to exactly one C3 operation class.

**Semantics**: "Do this specific thing."

**Decomposition**: May decompose into sub-DIRECTIVEs or QUERY children. Leaf directives map to M (merge/read), B (bounded local), X (exclusive access), V (verification), or G (governance) based on scope flags.

**Operation class derivation at leaf level**:
- `scope.requires_exclusive_access = true` => X-class
- `scope.is_bounded_local = true` (default) => B-class
- Otherwise => M-class (default for directives)

**Example**:
```json
{
  "intent_type": "DIRECTIVE",
  "operation_class": "B",
  "description": "Retrain local model on updated parcel data",
  "success_criteria": {
    "criteria_type": "PREDICATE",
    "predicates": [
      { "predicate_id": "model_updated", "observable": "parcel.model.version",
        "operator": "GT", "expected_value": 42 }
    ]
  }
}
```

#### 5.2.3 QUERY

A QUERY is an information retrieval request. Queries are always M-class (merge operations) at leaf level because they read but do not mutate system state.

**Semantics**: "Retrieve this information."

**Decomposition**: May decompose into sub-QUERYs that target different loci or parcels (scatter-gather pattern). Leaf queries are always M-class.

**Example**:
```json
{
  "intent_type": "QUERY",
  "operation_class": "M",
  "description": "Retrieve current accuracy metrics for climate domain across all loci",
  "success_criteria": {
    "criteria_type": "PREDICATE",
    "predicates": [
      { "predicate_id": "result_populated", "observable": "output.records_count",
        "operator": "GT", "expected_value": 0 }
    ]
  },
  "output_spec": {
    "output_type": "PARCEL",
    "output_schema_ref": "https://atrahasis.org/schemas/metrics-report/v1"
  }
}
```

#### 5.2.4 OPTIMIZATION

An OPTIMIZATION is a system self-improvement proposal originating from System 4's anticipatory planning. Optimizations go through the Adaptation Proposal Protocol (Section 8.4) before becoming intents. They may map to any operation class at leaf level depending on what the optimization requires.

**Semantics**: "Improve this aspect of system operation."

**Decomposition**: May decompose into DIRECTIVE and QUERY children. If the optimization affects governance parameters, leaf intents may be G-class.

**Operation class derivation at leaf level**:
- `scope.affects_governance = true` => G-class
- `scope.requires_verification = true` => V-class
- Otherwise => B-class (default for optimizations)

**Example**:
```json
{
  "intent_type": "OPTIMIZATION",
  "operation_class": null,
  "description": "Rebalance agent distribution across loci to match projected demand",
  "success_criteria": {
    "criteria_type": "THRESHOLD",
    "thresholds": [
      { "threshold_id": "balance_ratio",
        "metric": "loci.agent_distribution.gini_coefficient",
        "operator": "LTE", "value": 0.15 }
    ]
  },
  "scope": {
    "domain": "system_operations",
    "target_loci": ["*"],
    "affects_governance": false
  }
}
```

### 5.3 Lifecycle State Machine

Every intent quantum traverses a five-state lifecycle. The state machine is deliberately minimal -- the Ideation Council explicitly rejected proposals for additional states (coherence graphs, consolidation phases, dreaming modes) as overcomplication.

```
                                +----------+
                                | PROPOSED |
                                +----+-----+
                                     |
                        +------------+------------+
                        |                         |
               validate & admit            admission rejected
               + decompose                        |
                        |                         v
                        v                   +-----------+
                  +------------+            | DISSOLVED |
             +--->| DECOMPOSED |----------->| (terminal)|
             |    +-----+------+  budget    +-----------+
             |          |         exhausted
             |   activate leaves     or no valid
             |   (all children       decomposition
             |    registered)
             |          |
             |          v
             |    +--------+
             |    | ACTIVE  |----------------------------+
             |    +----+----+                            |
             |         |                                 |
             |    partial failure                   deadline / resource
             |    requires re-decomp               exhausted / cancel
             |    (ACTIVE -> DECOMPOSED)                 |
             |         |                                 |
             |         v                                 v
             |   success criteria                  +-----------+
             |   evaluated                         | DISSOLVED |
             |         |                           | (terminal)|
             |         v                           +-----------+
             |   +-----------+
             |   | COMPLETED |
             |   +-----+-----+
             |         |
             |    GC after 100 epochs
             |         |
             |         v
             +---+-----------+
                 | DISSOLVED |
                 | (terminal)|
                 +-----------+
```

**State Transition Table**:

| From | To | Trigger | Conditions |
|---|---|---|---|
| PROPOSED | DECOMPOSED | System 3 admission gate passed; decomposition completes successfully | Valid intent; decomposition plan produced; all child intents registered in ISR |
| PROPOSED | DISSOLVED | Admission rejected or decomposition fails | Invalid intent schema, no capable agents, decomposition budget exhausted |
| DECOMPOSED | ACTIVE | All leaf children assigned to agents; non-leaf children begin their own decomposition | Resource bounds validated; agent capabilities confirmed |
| DECOMPOSED | DISSOLVED | Parent dissolved, compensation triggered, or decomposition budget exceeded | Cascading dissolution from parent or sibling failure |
| ACTIVE | COMPLETED | All leaf descendants report results; success criteria evaluated | Outcome recorded as SUCCESS, PARTIAL_SUCCESS, FAILURE, or TIMEOUT |
| ACTIVE | DECOMPOSED | Partial failure requires re-decomposition | Some children failed but decomposition strategy supports partial recovery (e.g., PARALLEL with partial-success threshold) |
| ACTIVE | DISSOLVED | Deadline exceeded, resource exhausted, explicit cancellation, or parent dissolution | Terminal failure; compensation protocol triggered |
| COMPLETED | DISSOLVED | Retention period expires (default: 100 epochs after completion) | GC-eligible; transition log compacted |
| DISSOLVED | (none) | Terminal state | Entry removed after GC retention |

**Invariants**:

1. DISSOLVED is terminal. No transition exits DISSOLVED. This is constitutionally sovereign (INV-E5 by analogy with EMA's DISSOLVED state irreversibility).
2. Forward-only transitions except ACTIVE -> DECOMPOSED, which is the sole backward transition. It exists to support partial failure recovery without full compensation.
3. No coherence graph for intents. Intents are not knowledge objects; they do not undergo consolidation, dreaming, or coherence evaluation.
4. Every transition is recorded in the ISR transition log with a CausalStamp (Section 7.2), ensuring complete auditability and causal ordering.

**The ACTIVE -> DECOMPOSED Special Case**:

When a child intent fails during execution and the parent's decomposition strategy supports partial recovery, the parent transitions backward from ACTIVE to DECOMPOSED. System 3 then re-decomposes only the failed portion:

```
function handle_partial_failure(parent_id, failed_child_id):
    parent = isr.get_intent(parent_id)
    children = isr.get_children(parent_id)

    completed = [c for c in children
                 if c.lifecycle_state == COMPLETED and c.result.outcome == SUCCESS]
    failed = [c for c in children
              if c.lifecycle_state in {COMPLETED(FAILURE), COMPLETED(TIMEOUT)}]

    if parent.decomposition_strategy == PARALLEL:
        success_ratio = len(completed) / len(children)
        if success_ratio >= parent.partial_success_threshold:
            // Enough succeeded; parent completes with PARTIAL_SUCCESS
            complete_parent(parent_id, "PARTIAL_SUCCESS")
            return

    // Re-decompose: transition parent back to DECOMPOSED
    isr.transition_intent(parent_id, "DECOMPOSED",
                          reason="PARTIAL_FAILURE_REDECOMP")

    // Create replacement children for the failed scope only
    failed_scope = aggregate_scope(failed)
    replacement = create_replacement_intent(parent, failed_scope)
    decompose_intent(replacement, parent.current_depth + 1)
```

### 5.4 Success Criteria Specification Language

The success criteria language provides four evaluation modes that can be composed into complex conditions. This language replaces the informal "task complete" notifications found in traditional workflow systems with machine-evaluable predicates that System 3 can evaluate automatically.

#### 5.4.1 Predicate-Based Criteria

Boolean conditions over observable system state, addressed by dot-path notation:

```
Predicate := observable OPERATOR expected_value

Operators:
  EQ       -- observable == expected_value
  NEQ      -- observable != expected_value
  GT       -- observable > expected_value
  GTE      -- observable >= expected_value
  LT       -- observable < expected_value
  LTE      -- observable <= expected_value
  CONTAINS -- observable (collection) contains expected_value
  MATCHES  -- observable (string) matches expected_value (regex)
  EXISTS   -- observable is non-null (expected_value is boolean: true = must exist)

Examples:
  parcel.model.version GT 42
  locus.agent_count GTE 10
  output.classification.label EQ "positive"
  agent.capabilities CONTAINS "inference"
  result.error_log EXISTS false
```

#### 5.4.2 Threshold-Based Criteria

Numeric metrics evaluated against thresholds. Used for quantitative goals where the success condition is a continuous value crossing a boundary:

```
Threshold := metric (GTE | LTE) value

Examples:
  domain_x.classification.accuracy GTE 0.95
  system.latency_p99_ms LTE 500
  locus.resource_utilization LTE 0.85
```

#### 5.4.3 Temporal Criteria

Bounds on when success must be achieved:

```
TemporalBound :=
  | WITHIN_EPOCHS n    -- must complete within n epochs of activation
  | BEFORE_EPOCH e     -- must complete before epoch e
  | AFTER_EPOCH e      -- must not start before epoch e

Examples:
  WITHIN_EPOCHS 100    -- complete within 100 epochs
  BEFORE_EPOCH 50000   -- hard deadline at epoch 50000
  AFTER_EPOCH 49000    -- earliest start at epoch 49000
```

#### 5.4.4 Composite Criteria

Combine sub-criteria using aggregation modes:

```
Composite := aggregation of [Predicate | Threshold | Temporal | Composite]

Aggregation Modes:
  ALL_REQUIRED        -- all sub-criteria must be satisfied
  ANY_REQUIRED        -- at least one sub-criteria must be satisfied
  WEIGHTED_THRESHOLD  -- weighted sum of predicate results >= threshold value

Example (ALL_REQUIRED):
  ALL of:
    - accuracy GTE 0.95
    - latency_p99 LTE 500ms
    - WITHIN_EPOCHS 100

Example (ANY_REQUIRED):
  ANY of:
    - accuracy GTE 0.98           (high bar, any timeline)
    - accuracy GTE 0.95 AND WITHIN_EPOCHS 50  (lower bar, faster)

Example (WEIGHTED_THRESHOLD with threshold=0.7):
  Weighted sum >= 0.7 of:
    - p1: accuracy GTE 0.90 (weight=0.6, required=true)
    - p2: coverage GTE 0.80 (weight=0.4, required=false)
```

**Evaluation semantics**: ALL_REQUIRED requires all sub-criteria to be true simultaneously at evaluation time. ANY_REQUIRED requires at least one. WEIGHTED_THRESHOLD computes the weighted sum of satisfied predicates and compares to the threshold value; predicates marked `required=true` must pass regardless of the weighted sum. Temporal bounds are evaluated against the Clock Service's current epoch. Predicates are evaluated against observable system state. Thresholds are evaluated against the most recent metric snapshot. Evaluation is triggered by System 3 when all leaf descendants of an intent tree report results.

### 5.5 Comparison to Traditional Approaches

| Dimension | Traditional Task Queue | Workflow DAG | RIF Intent Quantum |
|---|---|---|---|
| Work item definition | Opaque payload + callback | Step in a predefined graph | Self-describing typed object with success criteria |
| Success evaluation | Binary (complete/fail) | Binary per step; DAG completes when all steps do | Machine-evaluable predicates, thresholds, temporal bounds, composites |
| Decomposition | None (tasks are atomic) | Predefined at authoring time | Dynamic at runtime, governed by formal algebra with termination proof |
| Resource management | Queue depth limits | Per-step resource requests | Formal resource bounds with additive/shared distinction and preservation proof |
| Failure handling | Retry or dead-letter | Retry or compensate (predefined) | Saga-style compensation derived from decomposition structure; partial re-decomposition |
| Provenance | Logging | Logging | W3C PROV chains anchored to native sovereign claim objects |
| Lifecycle | Queued, Processing, Done, Failed | Per-step states | PROPOSED, DECOMPOSED, ACTIVE, COMPLETED, DISSOLVED with formal state machine |
| Types | None (generic) | None (generic) | GOAL, DIRECTIVE, QUERY, OPTIMIZATION with distinct semantics |
| Causal ordering | None or timestamp | DAG edges | Vector clocks + NTP with causal stamps on every transition |

The fundamental difference is that a task queue or workflow DAG is a *mechanism* -- it moves work from A to B. An intent quantum is a *specification* -- it declares what success looks like and lets the system figure out how to achieve it. This declarative nature is what enables dynamic decomposition, partial success evaluation, and adaptive re-decomposition on failure.

---

## 6. Formal Decomposition Algebra

The decomposition algebra is the mathematical foundation that ensures RIF's recursive decomposition is well-behaved. It provides three guarantees: every decomposition terminates in finite steps, no decomposition produces a cycle, and no decomposition allocates more resources than the parent possesses. These are not aspirational properties or implementation guidelines -- they are mathematical invariants enforced by the decomposition engine.

### 6.1 Operation Class Decomposition Rules

C3's five operation classes form a strict partial order that governs which child classes may appear during decomposition:

```
    G  (Governance -- constitutional consensus)
    |
    V  (Verification -- cross-agent validation)
    |
    X  (Exclusive -- single-agent exclusive access)
    |
    B  (Bounded -- bounded local operations)
    |
    M  (Merge -- read-only merge operations)
```

**Formal decomposition rules**: Let `class(i)` denote the operation class of intent `i`, and `children(i)` the set of child intents produced by decomposing `i`.

```
Rule G-DECOMP:
  class(i) = G  ==>  for all c in children(i): class(c) in {M, B, X, V, G}
  Governance intents may decompose into any operation class.

Rule V-DECOMP:
  class(i) = V  ==>  for all c in children(i): class(c) in {M, B, X}
  Verification cannot spawn governance or further verification.

Rule X-DECOMP:
  class(i) = X  ==>  for all c in children(i): class(c) in {M, B}
  Exclusive operations decompose into simpler, non-exclusive operations.

Rule B-DECOMP:
  class(i) = B  ==>  for all c in children(i): class(c) in {M}
  Bounded local operations decompose only into merge reads.

Rule M-TERMINAL:
  class(i) = M  ==>  children(i) = empty set
  Merge operations are terminal. They cannot decompose further.
```

**Visual decomposition matrix**:

```
Parent \ Child |  M  |  B  |  X  |  V  |  G  |
---------------|-----|-----|-----|-----|-----|
      G        |  Y  |  Y  |  Y  |  Y  |  Y  |
      V        |  Y  |  Y  |  Y  |  N  |  N  |
      X        |  Y  |  Y  |  N  |  N  |  N  |
      B        |  Y  |  N  |  N  |  N  |  N  |
      M        | (terminal -- no children)      |
```

**Rationale for each restriction**:

- **V cannot spawn V**: Verification of verification creates infinite regress. A single V-class operation produces a verifiable result; if that result needs further verification, the parent's parent handles it.
- **V cannot spawn G**: Verification is an operational check, not a governance action. If verification reveals a governance need, it reports upward.
- **X cannot spawn X**: Exclusive access is non-composable. An X-class operation holds a lock; nesting locks invites deadlock. If multiple exclusive resources are needed, the work is decomposed into B/M operations with explicit sequencing.
- **B cannot spawn B**: Bounded local operations are already near-atomic. Further decomposition yields only M-class merge reads.

### 6.2 Termination Guarantee

**Claim**: Every intent decomposition terminates in a finite number of steps.

**Proof sketch**: Define a well-founded ordering on intents as a pair `(class_rank, remaining_depth)` where:

```
class_rank(M) = 0
class_rank(B) = 1
class_rank(X) = 2
class_rank(V) = 3
class_rank(G) = 4

remaining_depth(i) = i.constraints.max_depth - current_depth(i)
```

Define the lexicographic order: `(r1, d1) < (r2, d2)` iff `r1 < r2`, or (`r1 == r2` and `d1 < d2`).

**Step 1 -- Every decomposition step produces children strictly less than the parent.**

Case analysis by parent class:

- `class(parent) = G`: Children have `class(c) in {M,B,X,V,G}`. If `class(c) < G`, then `class_rank(c) < class_rank(parent)` -- strictly less by first component. If `class(c) = G`, then `class_rank(c) = class_rank(parent)`, but `remaining_depth(c) = remaining_depth(parent) - 1` -- strictly less by second component.

- `class(parent) = V`: Children have `class(c) in {M,B,X}`. `class_rank(c) <= 2 < 3 = class_rank(V)`. Strictly less by first component.

- `class(parent) = X`: Children have `class(c) in {M,B}`. `class_rank(c) <= 1 < 2 = class_rank(X)`. Strictly less by first component.

- `class(parent) = B`: Children have `class(c) in {M}`. `class_rank(c) = 0 < 1 = class_rank(B)`. Strictly less by first component.

- `class(parent) = M`: No children. Decomposition terminates immediately.

**Step 2 -- The ordering is well-founded.**

`class_rank` ranges over `{0, 1, 2, 3, 4}` (finite). `remaining_depth` ranges over `{0, 1, ..., max_depth}` (finite). The lexicographic product of two finite well-ordered sets is well-founded.

**Step 3 -- Conclusion.**

By the well-ordering principle, every strictly descending chain in a well-founded order is finite. Therefore, every decomposition chain terminates. QED.

**Practical bound**: Maximum decomposition tree size is bounded by:

```
max_tree_size <= SUM_{d=0}^{max_depth} (branching_factor ^ d)
             = (branching_factor^(max_depth+1) - 1) / (branching_factor - 1)
```

With default `max_depth = 10` and a practical branching factor of 5, the theoretical maximum is `(5^11 - 1) / 4 = 12,207,031` nodes. In practice, trees are far smaller because class descent accelerates termination -- a V-class intent drops to {M,B,X} on its first decomposition, losing access to V and G classes entirely.

### 6.3 Cycle-Freedom Guarantee

**Claim**: No decomposition can produce a cycle (an intent that is an ancestor of itself).

**Proof sketch**: Assume for contradiction that a cycle exists: a sequence of intents `i_0, i_1, ..., i_k` where `i_{j+1} in children(i_j)` and `i_k = i_0`.

By the decomposition rules, for each step in the sequence, the pair `(class_rank, remaining_depth)` is strictly decreasing (as proved in Section 6.2). If `i_k = i_0`, then:

```
(class_rank(i_k), remaining_depth(i_k)) = (class_rank(i_0), remaining_depth(i_0))
```

But we showed the pair is strictly decreasing along every decomposition edge. A strictly decreasing sequence over a well-founded order cannot return to its starting value. **Contradiction**.

Therefore, no cycle exists. QED.

**Additional structural guarantee**: Each intent's `intent_id` is a 256-bit identifier generated at creation time. The decomposition engine never reuses an `intent_id`. Even if the same logical decomposition pattern recurs (via memoization), child intents receive fresh identifiers, making structural cycles impossible at the identifier level as well.

### 6.4 Resource Bound Preservation

**Invariant**: No decomposition step allocates more resources to children than the parent possesses.

RIF distinguishes two resource categories because they have different composition semantics:

**Additive resources** (compute_tokens, wall_time_ms, storage_bytes): Children divide the parent's budget. The sum of children's allocations must not exceed the parent's allocation minus decomposition overhead.

```
For resource r classified as ADDITIVE:
  SUM(child.resource_bounds.r for child in children)
      <= parent.resource_bounds.r - decomposition_overhead.r
```

**Shared resources** (bandwidth_bytes, iops): Children contend for a common pool. Each child may use up to the parent's bound, but they share the capacity.

```
For resource r classified as SHARED:
  MAX(child.resource_bounds.r for child in children)
      <= parent.resource_bounds.r
```

**Formal validation pseudocode**:

```
function validate_resource_partition(parent_bounds, children):
    overhead = ResourceBounds(
        compute_tokens = DECOMP_OVERHEAD_TOKENS,   // default: 100
        wall_time_ms   = DECOMP_OVERHEAD_MS,       // default: 500
        storage_bytes  = 0,
        bandwidth_bytes = 0,
        iops           = 0
    )

    // Validate additive resources
    for field in [compute_tokens, wall_time_ms, storage_bytes]:
        child_sum = sum(c.resource_bounds[field] for c in children)
        parent_available = parent_bounds[field] - overhead[field]
        if child_sum > parent_available:
            return FAILURE(resource=field, deficit=child_sum - parent_available)

    // Validate shared resources
    for field in [bandwidth_bytes, iops]:
        child_max = max(c.resource_bounds[field] for c in children)
        if child_max > parent_bounds[field]:
            return FAILURE(resource=field, deficit=child_max - parent_bounds[field])

    return SUCCESS
```

**Resource return on completion**: When a child intent completes under-budget, unused additive resources are returned to the parent's available pool. Returned resources become available to sibling intents via lazy redistribution -- siblings request additional resources when needed rather than receiving proactive allocations.

```
function return_unused_resources(child):
    for field in ADDITIVE_FIELDS:
        allocated = child.resource_accounting.allocated[field]
        consumed  = child.resource_accounting.consumed[field]
        returned  = allocated - consumed
        if returned > 0:
            child.resource_accounting.returned_to_parent[field] = returned
            // Parent's Resource Optimizer picks up this surplus
```

### 6.5 Decomposition Budget Mechanics

Decomposition itself is a computational process that consumes resources. Without explicit budgets, a malicious or poorly constructed intent could cause unbounded decomposition inference. Two independent limits prevent this:

**Wall-clock limit** (`decomposition_budget_ms`):

```
Default:    5,000 ms (5 seconds)
Range:      [100, 60,000]

Behavior:
  - Timer starts when decompose_intent() is called
  - Timer is checked at every recursive call and every strategy selection step
  - If elapsed > budget: DECOMPOSITION_BUDGET_EXHAUSTED
```

**Computation limit** (`decomposition_token_limit`):

```
Default:    10,000 tokens
Range:      [100, 1,000,000]

Behavior:
  - Token counter increments with each inference step during
    strategy selection and decomposition rule application
  - If consumed > limit: TOKEN_BUDGET_EXHAUSTED
```

**On budget exhaustion**, decomposition fails cleanly:

1. All partially-created children are dissolved (DISSOLVED with reason "PARENT_DECOMP_BUDGET_EXHAUSTED").
2. An explicit DecompositionFailedEvent is emitted for System 4 analysis.
3. The intent transitions to DISSOLVED.
4. If the intent has a parent, the parent is notified of child failure and may re-decompose or compensate.

### 6.6 Memoization Strategy

Decomposition memoization prevents redundant computation when similar intents arrive repeatedly. In a system processing thousands of intents per epoch, many will share structural similarities -- the same type of goal in the same domain with similar resource constraints. Recomputing the decomposition plan from scratch each time is wasteful.

#### 6.6.1 Cache Key

```
cache_key = (intent_type, scope_hash, context_hash)

where:
  intent_type  = GOAL | DIRECTIVE | QUERY | OPTIMIZATION
  scope_hash   = SHA256(scope.domain, scope.target_loci, scope.flags)
  context_hash = SHA256(relevant_system_state_at_decomposition_time)
```

The context hash captures the system state that is relevant to decomposition decisions:

```
function context_hash(intent):
    relevant_state = {
        "agent_capabilities": agent_registry.get_capability_summary(
            intent.scope.target_loci),
        "locus_topology": c3.get_topology_hash(intent.scope.target_loci),
        "active_policies": system5.get_active_policy_hash(),
        "resource_availability": get_resource_snapshot(intent.scope.target_loci)
    }
    return SHA256(canonical_json(relevant_state))
```

#### 6.6.2 Cache Hit Behavior

On cache hit, the prior plan is not blindly reused. A delta is computed between the cached state snapshot and the current state:

| Delta Type | Criteria | Action |
|---|---|---|
| NONE | `context_hash` unchanged | Reuse plan exactly (fresh UUIDs for children) |
| MINOR | < 20% of agents changed; topology unchanged; policies unchanged | Delta-adjust agent assignments and resource bounds |
| MAJOR | >= 20% of agents changed, OR topology changed, OR policies changed | Invalidate cache entry; recompute from scratch |

Delta adjustment for MINOR changes replaces unavailable agents with new capable agents and adjusts resource bounds for changed availability. If any leaf cannot be re-assigned (no capable agent available), the cache entry is invalidated and fresh decomposition proceeds.

#### 6.6.3 Cache Configuration

```
max_entries:        10,000
default_ttl_epochs: 50
eviction_policy:    LRU (Least Recently Used)

Invalidation Triggers:
  1. Agent departure or arrival in target locus     -> MINOR delta on next access
  2. C3 tidal rebalancing changes locus structure   -> MAJOR invalidation for affected loci
  3. G-class governance changes active policies     -> MAJOR invalidation (all plans)
  4. Decomposition rules change (requires G-class)  -> Full cache flush
```

---

## 7. Domain-Scoped State Plane

The Domain-Scoped State Plane contains five infrastructure services that provide the operational foundation for RIF. The key design decision is *scoping*: each service is primarily locus-local, with minimal cross-locus replication. This ensures that the state plane scales with the number of loci rather than with the total number of agents or intents system-wide.

### 7.1 Agent Registry

#### Purpose

The Agent Registry maintains the authoritative mapping of agents to their capabilities, cryptographic identities, stake positions, reputation scores, and locus assignments. It is the foundation for all intent assignment decisions -- System 3 cannot assign a leaf intent to an agent whose capabilities do not match the required operation class or whose PCVM credibility falls below the intent's minimum threshold.

#### Data Model

Each agent entry contains:

```json
{
  "agent_id": "uuid",
  "pubkey": "ed25519-public-key",
  "capabilities": [
    {
      "operation_class": "M|B|X|V|G",
      "domain": "string (e.g., 'inference', 'storage', 'verification')",
      "capacity": "number [0,1] -- normalized capacity",
      "attested_epoch": "integer -- last attestation epoch"
    }
  ],
  "stake": {
    "amount": "number >= 0",
    "locked_until_epoch": "integer"
  },
  "reputation": {
    "composite_score": "number [0,1] -- PCVM-derived",
    "intent_completion_rate": "number [0,1]",
    "last_failure_epoch": "integer|null",
    "total_intents_completed": "integer >= 0"
  },
  "locus_id": "string",
  "parcel_id": "string",
  "status": "ACTIVE|SUSPENDED|DRAINING|DEPARTED",
  "last_heartbeat_epoch": "integer",
  "current_assignment_count": "integer >= 0",
  "version_vector": { "locus_id": "integer", ... }
}
```

**Cross-locus capability summary** (the only structure that crosses locus boundaries):

```json
{
  "locus_id": "string",
  "summary_epoch": "integer",
  "agent_count": "integer",
  "aggregate_capabilities": [
    {
      "operation_class": "M|B|X|V|G",
      "domain": "string",
      "total_capacity": "number",
      "available_capacity": "number"
    }
  ],
  "digest": "sha256 -- hash of full registry state for consistency checks"
}
```

#### CRDT Replication Model

- **Intra-locus**: Full state CRDT replication using Last-Writer-Wins Register for scalar fields and Observed-Remove Set for the capabilities list. Convergence guaranteed within 2 tidal epochs under normal conditions. CRDT traffic budget: at most 2% of locus network capacity. If exceeded, replication frequency halves until budget is met.

- **Cross-locus**: Only `AgentCapabilitySummary` objects replicate. Summaries are computed once per epoch by the locus coordinator and broadcast via C3 parcel gossip. Stale summaries (older than 10 epochs) are discarded by receivers.

#### Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| Agent crash | Heartbeat timeout (3 consecutive epochs) | Status -> SUSPENDED; reassign active intents |
| CRDT divergence | Digest mismatch on periodic audit (every 10 epochs) | Full state reconciliation from locus coordinator |
| Byzantine agent | PCVM credibility drop below 0.3 | Status -> SUSPENDED; stake slashing proposal to System 5 |
| Locus partition | No cross-locus summary received for 5 epochs | Mark locus as PARTITIONED; freeze cross-locus intent assignment |

#### Integration Contracts

- **To System 3**: `query_capable_agents(operation_class, domain, min_capacity) -> List[AgentId]`
- **To Failure Detector**: `report_agent_liveness(agent_id, epoch, alive: bool)`
- **To C3**: `sync_locus_assignment(agent_id, locus_id, parcel_id)` -- called when C3 tidal rebalancing moves an agent
- **To C5 PCVM**: `refresh_reputation(agent_id) -> ReputationScore` -- called once per epoch per active agent

### 7.2 Clock Service

#### Purpose

The Clock Service provides a shared notion of time across agents within a locus and a causally consistent ordering of events across loci. RIF needs both wall-clock time (for decomposition budgets, TTLs, and epoch alignment) and causal ordering (for intent state transitions that must respect happens-before relationships).

#### Dual Time Model

The Clock Service maintains two complementary time representations:

**Wall-clock time** via NTP federation:
```json
{
  "locus_id": "string",
  "wall_clock": {
    "timestamp_ms": "integer -- ms since Unix epoch",
    "uncertainty_ms": "integer [0,500] -- clock uncertainty bound",
    "ntp_stratum": "integer [1,15]",
    "last_sync_epoch": "integer"
  },
  "epoch_info": {
    "current_epoch": "integer",
    "epoch_start_ms": "integer",
    "epoch_duration_ms": "integer",
    "tidal_phase": "RISING|HIGH|FALLING|LOW"
  }
}
```

**Causal ordering** via vector clocks:
```json
{
  "vector_clock": { "locus_id": "logical_timestamp", ... }
}
```

Every intent state transition receives a **CausalStamp** combining both:

```json
{
  "wall_time_ms": "integer",
  "vector_clock": { "locus_id": "integer", ... },
  "epoch": "integer",
  "locus_id": "string",
  "agent_id": "string",
  "signature": "Ed25519 signature over (wall_time_ms, vector_clock, epoch, locus_id, agent_id)"
}
```

#### Temporal Hierarchy Alignment (per C9 Reconciliation)

The Clock Service aligns with the canonical three-tier temporal hierarchy defined by C9:

- **SETTLEMENT_TICK**: 60-second economic settlement cycle (C8 DSF authority)
- **TIDAL_EPOCH**: 3600-second coordination cycle = 60 SETTLEMENT_TICKs (C3 authority)
- **CONSOLIDATION_CYCLE**: 36000-second knowledge metabolism cycle = 10 TIDAL_EPOCHs (C6 authority)

All RIF epoch references are TIDAL_EPOCHs (3600s) unless explicitly stated otherwise.

#### Replication and Synchronization

- **Intra-locus NTP federation**: Each locus elects a stratum-1 time source (or federates with external NTP). Agents synchronize to stratum-2 with +/-500ms maximum tolerated skew.
- **Cross-locus vector clocks**: Piggyback on all cross-locus messages. Each locus maintains vector clock entries for loci it has communicated with in the last 100 epochs. Older entries are pruned.
- **Epoch alignment**: All loci share the same epoch numbering from C3 tidal scheduling. Epoch boundaries are authoritative from C3; the Clock Service tracks them.

#### Partition Behavior

When a network partition isolates a locus:

1. Vector clock entries for the remote locus stop advancing.
2. The remote locus is marked PARTITIONED in vector clock metadata.
3. All non-local intent processing targeting the partitioned locus is frozen.
4. Local intent processing continues unimpeded.

This is the correct behavior: a partition means causal ordering cannot be maintained across the partition boundary, so cross-locus operations must halt. But local operations -- which constitute at least 80% of traffic in a well-configured system -- continue normally.

#### Integration Contracts

- **To ISR**: `stamp_transition(intent_id, transition) -> CausalStamp`
- **To System 3**: `current_epoch() -> EpochInfo`
- **To System 3**: `is_within_budget(start_stamp, budget_ms) -> bool`
- **To C3**: `sync_epoch_boundary(epoch, start_ms, duration_ms)` -- called by C3 at each epoch boundary

### 7.3 Intent State Registry

#### Purpose

The ISR is the authoritative store for all intent quanta within a locus. It maintains the current lifecycle state of every intent, the parent-child decomposition tree, the transition history, and resource accounting. It is the component that System 3 reads from and writes to most frequently -- every decomposition, every state transition, every resource reconciliation flows through the ISR.

#### Data Model

**ISR Entry** (one per intent quantum):

```json
{
  "intent_id": "uuid",
  "intent": "{ full IntentQuantum object }",
  "lifecycle_state": "PROPOSED|DECOMPOSED|ACTIVE|COMPLETED|DISSOLVED",
  "parent_intent_id": "uuid|null",
  "children_intent_ids": ["uuid", ...],
  "assigned_agent_id": "uuid|null -- non-null only for leaf intents in ACTIVE state",
  "assigned_locus_id": "string",
  "spanning_loci": ["string", ... ],
  "transition_log": [
    {
      "from_state": "string",
      "to_state": "string",
      "causal_stamp": "CausalStamp",
      "reason": "string",
      "trigger_agent_id": "string"
    }
  ],
  "result": {
    "outcome": "SUCCESS|PARTIAL_SUCCESS|FAILURE|TIMEOUT",
    "output_parcel_ids": ["string", ...],
    "success_criteria_evaluation": { "criterion_id": true|false, ... },
    "completion_epoch": "integer"
  },
  "resource_accounting": {
    "allocated": "ResourceBounds",
    "consumed": "ResourceBounds",
    "returned_to_parent": "ResourceBounds"
  },
  "version_vector": { "locus_id": "integer", ... },
  "gc_eligible_epoch": "integer|null"
}
```

**Cross-locus spanning intent stub** (the minimal information replicated to remote loci):

```json
{
  "intent_id": "uuid",
  "root_intent_id": "uuid",
  "originating_locus_id": "string",
  "operation_class": "M|B|X|V|G",
  "required_capabilities": [
    { "domain": "string", "min_capacity": "number" }
  ],
  "resource_bounds": "ResourceBounds",
  "deadline_epoch": "integer",
  "lifecycle_state": "string",
  "causal_stamp": "CausalStamp"
}
```

#### CRDT Replication

- **Intra-locus**: Full CRDT replication using operation-based CRDTs with state transitions as operations. Conflict resolution: causal stamp ordering; ties broken by agent_id lexicographic order.
- **Cross-locus**: Only `SpanningIntentStub` objects replicate. Full intent state remains in the originating locus.
- **Bandwidth budget**: 5% of locus network capacity. When exceeded, replication batches grow larger (more ops per message, fewer messages) and transition log entries older than 10 epochs are elided.
- **GC policy**: DISSOLVED entries retained for 100 epochs after `gc_eligible_epoch`, then hard-deleted. Transition logs are compacted after 50 epochs: only first, last, and failure transitions are retained.

#### Resource Reservation Index (Shared Resource Contention)

The ISR is extended with a resource reservation index for managing concurrent access to agents, parcels, and capacity slices:

```
STRUCTURE ResourceReservation:
    resource_id:     string          // agent_id, parcel_id, or capacity_slice_id
    resource_type:   enum { AGENT, PARCEL, CAPACITY_SLICE }
    intent_id:       string          // the intent holding this reservation
    operation_class: enum { M, B, X, V, G }
    priority:        int             // from intent.constraints.priority
    deadline_epoch:  int | null      // from intent.constraints.deadline_epoch
    reserved_epoch:  int             // epoch when reservation was made
    expiry_epoch:    int             // reserved_epoch + 2 * TIDAL_EPOCH_DURATION

// ISR maintains a map: resource_id -> List[ResourceReservation]
// sorted by (operation_class rank DESC, deadline_epoch ASC, intent_id ASC)
```

**Contention Detection**: Triggered whenever a new leaf intent is assigned to an agent or parcel:

```
FUNCTION detect_contention(new_intent: IntentQuantum,
                           target_resource_id: string,
                           resource_type: ResourceType) -> ContentionResult:

    existing = isr.resource_index.get(target_resource_id)
    IF existing == null OR len(existing) == 0:
        RETURN ContentionResult { contended: false }

    // Check for exclusive access conflict
    IF resource_type == AGENT:
        active_count = count(r FOR r IN existing
                             IF r.intent_id != new_intent.intent_id
                             AND isr.get_state(r.intent_id) == ACTIVE)
        IF active_count > 0 AND new_intent.scope.requires_exclusive_access:
            RETURN ContentionResult {
                contended: true,
                reason: EXCLUSIVE_CONFLICT,
                blocking_intents: [r.intent_id FOR r IN existing IF active]
            }

    // Check for capacity overload
    IF resource_type == AGENT:
        concurrent_leaves = count(r FOR r IN existing
                                  IF isr.get_state(r.intent_id) IN [ACTIVE, DECOMPOSED])
        IF concurrent_leaves >= MAX_CONCURRENT_LEAVES:  // default: 3
            RETURN ContentionResult {
                contended: true,
                reason: CAPACITY_OVERLOAD,
                blocking_intents: [r.intent_id FOR r IN existing],
                queue_position: concurrent_leaves - MAX_CONCURRENT_LEAVES + 1
            }

    RETURN ContentionResult { contended: false }
```

**Contention Resolution**: Follows a strict priority ordering:

```
FUNCTION resolve_contention(new_intent: IntentQuantum,
                            contention: ContentionResult,
                            target_resource_id: string) -> ResolutionAction:

    new_rank = class_rank(new_intent.operation_class)
    new_priority = new_intent.constraints.priority
    new_deadline = new_intent.constraints.deadline_epoch

    // Rule 1: Higher operation class wins
    FOR blocker_id IN contention.blocking_intents:
        blocker = isr.get_intent(blocker_id)
        blocker_rank = class_rank(blocker.operation_class)

        IF new_rank > blocker_rank:
            RETURN ResolutionAction {
                action: PREEMPT,
                preempt_intent_id: blocker_id,
                reason: "operation_class " + new_intent.operation_class +
                        " > " + blocker.operation_class
            }

    // Rule 2: Within same operation class, earlier deadline wins
    same_class_blockers = [b FOR b IN contention.blocking_intents
                           IF class_rank(isr.get_intent(b).operation_class) == new_rank]

    FOR blocker_id IN same_class_blockers:
        blocker = isr.get_intent(blocker_id)
        IF new_deadline != null AND blocker.constraints.deadline_epoch != null:
            IF new_deadline < blocker.constraints.deadline_epoch:
                RETURN ResolutionAction {
                    action: PREEMPT,
                    preempt_intent_id: blocker_id,
                    reason: "deadline " + str(new_deadline) +
                            " < " + str(blocker.constraints.deadline_epoch)
                }
        // If new has a deadline and blocker does not, new wins
        IF new_deadline != null AND blocker.constraints.deadline_epoch == null:
            RETURN ResolutionAction {
                action: PREEMPT,
                preempt_intent_id: blocker_id,
                reason: "deadline-bearing intent takes priority over open-ended"
            }

    // Rule 3: Tie-break by intent_id hash (deterministic, no favoritism)
    FOR blocker_id IN same_class_blockers:
        IF hash(new_intent.intent_id) < hash(blocker_id):
            RETURN ResolutionAction {
                action: PREEMPT,
                preempt_intent_id: blocker_id,
                reason: "hash tie-break"
            }

    // New intent loses all comparisons -> queue it
    RETURN ResolutionAction {
        action: QUEUE,
        queue_position: contention.queue_position,
        estimated_wait_epochs: estimate_wait(contention.blocking_intents)
    }
```

**Backpressure Mechanism**:

```
CONSTANT MAX_CONCURRENT_LEAVES = 3    // per agent
CONSTANT QUEUE_EXPIRY_EPOCHS   = 2    // in tidal epochs

FUNCTION apply_backpressure(agent_id: string,
                            new_intent: IntentQuantum) -> BackpressureResult:

    reservations = isr.resource_index.get(agent_id)
    active_leaves = count(r FOR r IN reservations
                          IF isr.get_state(r.intent_id) IN [ACTIVE]
                          AND r.resource_type == AGENT)

    IF active_leaves < MAX_CONCURRENT_LEAVES:
        // No backpressure needed; assign immediately
        isr.resource_index.add(agent_id, ResourceReservation {
            resource_id:     agent_id,
            resource_type:   AGENT,
            intent_id:       new_intent.intent_id,
            operation_class: new_intent.operation_class,
            priority:        new_intent.constraints.priority,
            deadline_epoch:  new_intent.constraints.deadline_epoch,
            reserved_epoch:  current_epoch(),
            expiry_epoch:    current_epoch() + QUEUE_EXPIRY_EPOCHS
        })
        RETURN BackpressureResult { action: ASSIGN_NOW }

    // Agent is at capacity. Queue the intent.
    queue_entry = QueueEntry {
        intent_id:    new_intent.intent_id,
        agent_id:     agent_id,
        queued_epoch: current_epoch(),
        expiry_epoch: current_epoch() + QUEUE_EXPIRY_EPOCHS
    }
    isr.assignment_queue.enqueue(agent_id, queue_entry)

    RETURN BackpressureResult {
        action:               QUEUED,
        queue_position:       isr.assignment_queue.depth(agent_id),
        expiry_epoch:         queue_entry.expiry_epoch,
        estimated_wait_epochs: estimate_wait_from_queue(agent_id)
    }


FUNCTION process_assignment_queue(agent_id: string):
    // Called when an agent completes a leaf intent (ACTIVE -> COMPLETED/DISSOLVED)
    // or when a reservation expires.

    // 1. Remove completed/expired reservations
    isr.resource_index.remove_if(agent_id,
        r -> isr.get_state(r.intent_id) IN [COMPLETED, DISSOLVED]
             OR r.expiry_epoch <= current_epoch())

    // 2. Process queue
    WHILE isr.resource_index.active_count(agent_id) < MAX_CONCURRENT_LEAVES:
        next = isr.assignment_queue.dequeue(agent_id)
        IF next == null:
            BREAK   // queue empty

        // Check expiry
        IF next.expiry_epoch <= current_epoch():
            // Expired: transition intent to DISSOLVED with reason QUEUE_TIMEOUT
            isr.transition_intent(next.intent_id, DISSOLVED, "QUEUE_TIMEOUT")
            // Trigger compensation at parent
            parent_id = isr.get_intent(next.intent_id).parent_intent_id
            IF parent_id != null:
                notify_parent_of_child_failure(parent_id, next.intent_id,
                                                "QUEUE_TIMEOUT")
            CONTINUE

        // Assign
        isr.resource_index.add(agent_id, ResourceReservation {
            resource_id:     agent_id,
            resource_type:   AGENT,
            intent_id:       next.intent_id,
            operation_class: isr.get_intent(next.intent_id).operation_class,
            priority:        isr.get_intent(next.intent_id).constraints.priority,
            deadline_epoch:  isr.get_intent(next.intent_id).constraints.deadline_epoch,
            reserved_epoch:  current_epoch(),
            expiry_epoch:    current_epoch() + QUEUE_EXPIRY_EPOCHS
        })
        pe_execute_intent(isr.get_intent(next.intent_id),
                          agent_registry.get(agent_id))
```

#### Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| CRDT divergence | Periodic Merkle root comparison (every 5 epochs) | Incremental reconciliation from Merkle diff |
| Orphaned intents | Parent DISSOLVED but children still ACTIVE | Children receive forced DISSOLVED with reason "PARENT_DISSOLVED" |
| Spanning intent unreachable | Remote locus PARTITIONED for > 5 epochs | Spanning intent transitions to COMPLETED(TIMEOUT); compensation at parent |
| Storage exhaustion | Utilization > 90% | Aggressive GC: reduce DISSOLVED retention to 10 epochs; alert System 3 |

#### Integration Contracts

- **To System 3**: `propose_intent(intent_quantum) -> intent_id`
- **To System 3**: `transition_intent(intent_id, new_state, reason) -> CausalStamp`
- **To System 3**: `query_intents(filter) -> List[ISREntry]`
- **To System 3**: `get_intent_tree(root_intent_id) -> Tree[ISREntry]`
- **To Settlement Router**: `notify_settlement(intent_id, outcome)`
- **To native communication layer**: `emit_intent_claim(intent_id, outcome)` -- publishes intent outcome as a native sovereign claim object
- **To Failure Detector**: QUEUE_TIMEOUT dissolution events reported for agent health tracking. An agent causing > 5 queue timeouts in 10 epochs triggers a liveness investigation.

### 7.4 Settlement Router

#### Purpose

The Settlement Router connects RIF's intent lifecycle with C8 DSF's settlement ledger, accessed via C3's CRDT replication infrastructure. When an intent completes, the Settlement Router ensures that all resource accounting, stake adjustments, and reputation updates are recorded. It provides at-least-once delivery with idempotent processing, guaranteeing no settlement is lost even under partitions or crashes.

#### Data Model

**Settlement Message**:

```json
{
  "settlement_id": "uuid -- idempotency key",
  "intent_id": "uuid",
  "settlement_type": "RESOURCE_RETURN|STAKE_ADJUSTMENT|REPUTATION_UPDATE|
                       COMPENSATION_DEBIT|COMPLETION_CREDIT",
  "entries": [
    {
      "agent_id": "string",
      "resource_type": "string",
      "amount": "number",
      "direction": "CREDIT|DEBIT"
    }
  ],
  "causal_stamp": "CausalStamp",
  "delivery_attempts": "integer >= 0",
  "first_attempt_epoch": "integer",
  "last_attempt_epoch": "integer",
  "status": "PENDING|DELIVERED|CONFIRMED|DEAD_LETTER"
}
```

#### Delivery Semantics

- **No cross-locus replication**: Settlement messages are locus-local. Each locus has its own queue and its own connection to its C8 DSF settlement ledger partition (via C3 CRDT infrastructure).
- **Persistence**: Write-ahead-log style -- message is durable before ISR receives acknowledgment.
- **At-least-once delivery**: Exponential backoff retries (1, 2, 4, 8, 16, 32 epochs). After 10 failed attempts, message moves to DEAD_LETTER and System 3 is alerted.
- **Idempotency**: C8 DSF ledger rejects duplicate `settlement_id` values, so at-least-once delivery is safe.

#### Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| C8 DSF ledger unreachable | Delivery timeout (1 epoch) | Retry with exponential backoff |
| Duplicate delivery | C8 DSF rejects duplicate settlement_id | Mark as CONFIRMED (idempotent) |
| Dead letter accumulation | Count > 100 | System 3 alert; manual intervention required |
| Queue backpressure | Depth > 10,000 or oldest pending > 50 epochs | Throttle intent completions; notify System 3 |
| Router crash | Failure Detector liveness check | Restart from WAL; replay all PENDING messages |

### 7.5 Failure Detector

#### Purpose

RIF's Failure Detector goes beyond traditional heartbeat monitoring. It serves two functions:

1. **Agent liveness**: Is the agent alive and responsive? (Classical failure detection via quorum-based sentinel checks.)
2. **Intent outcome verification**: Did the intent's result actually advance the parent intent's success criteria? (Semantic failure detection via C5 PCVM integration.)

The second function distinguishes RIF from systems that equate "task completed" with "task succeeded." An agent may be alive and responsive but consistently producing results that do not advance system goals -- a subtle failure mode that heartbeat monitors cannot detect.

#### Sentinel-Based Liveness

Sentinels are agents with PCVM credibility >= 0.5 (configurable). Each epoch, the top-K credible agents are selected as sentinels (K = 2 * quorum to provide headroom for sentinel failures). An agent is declared dead only when `sentinel_quorum` sentinels (default: 3) agree within the same epoch window.

**Liveness Report**:
```json
{
  "agent_id": "string",
  "locus_id": "string",
  "epoch": "integer",
  "alive": "boolean",
  "response_latency_ms": "integer|null",
  "reporter_agent_id": "string",
  "reporter_credibility": "number [0,1]"
}
```

#### Intent Outcome Verification

A configurable fraction of completed intents (default: 10%) undergo outcome verification. An independent verifier evaluates whether the intent's completion actually advanced the parent intent's success criteria:

```json
{
  "intent_id": "string",
  "parent_intent_id": "string",
  "verifier_agent_id": "string",
  "verification_epoch": "integer",
  "advancement_score": "number [0,1] -- how much completion advanced parent's criteria",
  "byzantine_suspicion": "number [0,1] -- PCVM-derived suspicion of executing agent",
  "verification_claim_id": "string -- native verification object ID"
}
```

When `advancement_score` falls below 0.2 (configurable) or `byzantine_suspicion` exceeds 0.7 (configurable), the Failure Detector flags the intent and reports to System 3. Persistent non-advancement from the same agent triggers a Byzantine evidence submission to C5 PCVM.

#### Replication

- **Intra-locus**: Liveness reports broadcast to all sentinels. Quorum-based consensus.
- **Cross-locus**: Only aggregate failure statistics (failures per epoch, locus health score). Individual reports do not cross boundaries.

#### Integration Contracts

- **To Agent Registry**: `report_agent_liveness(agent_id, epoch, alive)`
- **To ISR**: `flag_non_advancing_intent(intent_id, advancement_score)`
- **To System 3**: `report_agent_failure(agent_id, failure_type, evidence)`
- **To C5 PCVM**: `query_agent_credibility(agent_id) -> score`
- **To C5 PCVM**: `submit_byzantine_evidence(agent_id, evidence)`
- **To native communication layer**: `publish_verification_claim(verification) -> claim_id`

---

## 8. Executive Plane

The Executive Plane implements Stafford Beer's System 3/4/5 distinction for the operational, strategic, and governance functions of intent orchestration. This section specifies each system's responsibilities, internal mechanisms, and interaction protocols.

### 8.1 System 3: Operational Control

System 3 is the operational heart of RIF. It receives intent proposals, decomposes them, assigns leaf intents to agents, monitors execution, and handles failures. It is the most active component in the Executive Plane -- present-focused, dealing with what the system is doing *right now*.

#### 8.1.1 Intent Decomposition Engine

The decomposition engine receives PROPOSED intents and transforms them into trees of child intents. Decomposition continues recursively until every leaf maps to a single C3 operation class executable by a single agent within a single epoch.

```
function decompose_intent(intent, depth):
    // --- Guard clauses ---
    if depth > intent.constraints.max_depth:
        return FAILURE("MAX_DEPTH_EXCEEDED")

    if wall_clock_elapsed(intent.decomposition_start) > intent.constraints.decomposition_budget_ms:
        return FAILURE("DECOMPOSITION_BUDGET_EXHAUSTED")

    if tokens_consumed > intent.constraints.decomposition_token_limit:
        return FAILURE("TOKEN_BUDGET_EXHAUSTED")

    // --- Memoization cache check ---
    cache_key = (intent.intent_type, hash(intent.scope), context_hash(intent))
    cached = memo_cache.get(cache_key)
    if cached != null and cached.ttl > current_epoch():
        delta = compute_state_delta(cached.snapshot, current_state())
        if delta.is_minor():
            return SUCCESS(cached.plan.apply_delta(delta), source="CACHE_HIT")

    // --- Leaf check ---
    if is_leaf_operation(intent):
        validate_resource_bounds(intent)
        agent = select_agent(intent.operation_class, intent.scope.domain,
                             intent.resource_bounds)
        if agent == null: return FAILURE("NO_CAPABLE_AGENT")
        return LEAF(intent, agent)

    // --- Strategy selection ---
    strategy = select_strategy(intent)

    // --- Apply decomposition rules ---
    children = apply_decomposition_rules(intent, strategy)

    // --- Validate operation class monotonicity ---
    for child in children:
        assert class_rank(child.operation_class) <= class_rank(intent.operation_class)

    // --- Validate resource bounds preservation ---
    validate_resource_partition(intent.resource_bounds, children)

    // --- Recursive decomposition ---
    results = []
    for child in children:
        child_result = decompose_intent(child, depth + 1)
        if child_result.is_failure():
            for created in results:
                dissolve_subtree(created)  // Compensate siblings
            return FAILURE("CHILD_DECOMPOSITION_FAILED", child_result)
        results.append(child_result)

    // --- Memoize and register ---
    plan = DecompositionPlan(strategy, results)
    memo_cache.put(cache_key, plan, ttl=current_epoch() + 50)
    for result in results:
        isr.register_intent_tree(result)
    isr.transition_intent(intent.intent_id, "DECOMPOSED")

    return SUCCESS(plan, source="COMPUTED")
```

#### 8.1.2 Strategy Selection Algorithm

The `select_strategy()` function determines which decomposition strategy to apply. It follows a five-step decision process:

```
FUNCTION select_strategy(intent: IntentQuantum) -> DecompositionStrategy:
    // ---------------------------------------------------------------
    // Step 0: Honor explicit proposer preference (Tier 3, A-02)
    // ---------------------------------------------------------------
    IF intent.decomposition_strategy != null:
        candidate = intent.decomposition_strategy
        IF validate_strategy_compatibility(intent, candidate):
            RETURN candidate
        // else: proposer preference is incompatible; fall through to auto-select

    // ---------------------------------------------------------------
    // Step 1: Classify by intent_type
    // ---------------------------------------------------------------
    MATCH intent.intent_type:

        CASE QUERY:
            // Queries are read-only. If multiple data sources, parallelize.
            IF count_independent_data_sources(intent.scope) > 1:
                RETURN PARALLEL
            ELSE:
                RETURN SEQUENTIAL

        CASE DIRECTIVE:
            GOTO step_2_structural_analysis

        CASE GOAL:
            GOTO step_2_structural_analysis

        CASE OPTIMIZATION:
            // Optimizations are System 4 proposals. Always CONDITIONAL
            // unless the optimization has been pre-decomposed by S4.
            IF intent.input_references contains ref_type == "EMA_QUANTUM":
                RETURN CONDITIONAL
            ELSE:
                GOTO step_2_structural_analysis

    // ---------------------------------------------------------------
    // Step 2: Structural analysis of success criteria
    // ---------------------------------------------------------------
    step_2_structural_analysis:

    criteria = intent.success_criteria

    // 2a: If criteria have branching predicates, use CONDITIONAL.
    IF criteria.criteria_type == "COMPOSITE"
       AND has_branching_predicates(criteria):
        RETURN CONDITIONAL

    // 2b: If criteria are conjunctive with independent sub-goals,
    //     use PARALLEL.
    IF criteria.aggregation IN ["ALL_REQUIRED", "WEIGHTED_THRESHOLD"]
       AND all_predicates_are_independent(criteria.predicates):
        RETURN PARALLEL

    // 2c: If criteria require ordered evaluation (output chaining),
    //     use SEQUENTIAL.
    IF has_output_chain_dependency(intent):
        RETURN SEQUENTIAL

    // ---------------------------------------------------------------
    // Step 3: Resource and depth heuristics
    // ---------------------------------------------------------------

    remaining_depth = intent.constraints.max_depth - current_depth(intent)

    // 3a: If remaining depth <= 2, prefer PARALLEL to minimize tree height
    IF remaining_depth <= 2:
        RETURN PARALLEL

    // 3b: If resource bounds are tight, prefer SEQUENTIAL
    estimated_children = estimate_child_count(intent)
    per_child_compute = intent.resource_bounds.compute_tokens / estimated_children
    IF per_child_compute < 100:
        RETURN SEQUENTIAL

    // ---------------------------------------------------------------
    // Step 4: Historical success rate lookup
    // ---------------------------------------------------------------
    history = memo_cache.get_strategy_stats(
        intent_type   = intent.intent_type,
        operation_class = intent.operation_class,
        domain        = intent.scope.domain
    )

    IF history != null AND history.sample_count >= 10:
        best = history.best_strategy_by_weighted_success()
        IF best.success_rate >= 0.7:
            RETURN best.strategy

    // ---------------------------------------------------------------
    // Step 5: Default fallback by operation class
    // ---------------------------------------------------------------
    MATCH intent.operation_class:
        CASE G:     RETURN SEQUENTIAL   // Governance: ordered deliberation
        CASE V:     RETURN PARALLEL     // Verification: independent checks
        CASE X:     RETURN SEQUENTIAL   // Exclusive: serialize access
        CASE B:     RETURN PARALLEL     // Bounded: independent local ops
        CASE M:     RETURN PARALLEL     // Merge: parallel reads
        CASE null:  RETURN RECURSIVE    // Non-leaf, class not yet assigned

    RETURN RECURSIVE


FUNCTION validate_strategy_compatibility(intent: IntentQuantum,
                                          strategy: DecompositionStrategy) -> bool:
    IF strategy == CONDITIONAL:
        RETURN has_branching_predicates(intent.success_criteria)
    IF strategy == SEQUENTIAL:
        RETURN estimate_child_count(intent) >= 2
    IF strategy == PARALLEL:
        RETURN NOT has_output_chain_dependency(intent)
    RETURN true  // RECURSIVE is always valid


FUNCTION has_branching_predicates(criteria: SuccessCriteria) -> bool:
    IF criteria.predicates == null OR len(criteria.predicates) < 2:
        RETURN false
    observables = group_by(criteria.predicates, p -> p.observable)
    FOR obs, preds IN observables:
        IF len(preds) >= 2:
            operators = set(p.operator FOR p IN preds)
            IF ("GT" IN operators AND "LTE" IN operators)
               OR ("GTE" IN operators AND "LT" IN operators)
               OR ("EQ" IN operators AND "NEQ" IN operators):
                RETURN true
    RETURN false


FUNCTION has_output_chain_dependency(intent: IntentQuantum) -> bool:
    IF intent.input_references == null:
        RETURN false
    RETURN any(ref.ref_type == "INTENT_OUTPUT" FOR ref IN intent.input_references)


FUNCTION estimate_child_count(intent: IntentQuantum) -> int:
    base = max(len(intent.success_criteria.predicates OR []), 1)
    scope_factor = len(intent.scope.target_loci)
    RETURN max(base * scope_factor, 2)
```

**Strategy Selection Summary Table**:

| Strategy | Primary Selection Trigger | Fallback For | Failure Behavior |
|---|---|---|---|
| RECURSIVE | Default for unclassified non-leaf intents (null operation_class) | None | Partial success; evaluate combined results |
| PARALLEL | Independent conjunctive sub-goals; V/B/M-class defaults; depth <= 2 | Low depth budget | All-or-nothing by default; configurable partial threshold |
| SEQUENTIAL | Output chain dependency; G/X-class defaults; tight resource bounds | Ordered criteria | First failure halts pipeline; compensate completed steps |
| CONDITIONAL | Branching predicates; EMA-driven optimizations | Mutually exclusive paths | Selected branch fails => no fallback unless configured |

**Operation class mapping at leaf level**:

```
function map_to_operation_class(leaf):
    match leaf.intent_type:
        GOAL       => ERROR("GOAL cannot be leaf")
        DIRECTIVE  => if scope.requires_exclusive_access: X
                      elif scope.is_bounded_local: B
                      else: M
        QUERY      => M  (always -- queries are read-only)
        OPTIMIZATION => if scope.affects_governance: G
                        elif scope.requires_verification: V
                        else: B
```

**Agent Selection with Contention Awareness**:

```
FUNCTION select_agent(operation_class, domain, resource_bounds) -> AgentRecord | null:
    candidates = agent_registry.query_capable_agents(
        operation_class = operation_class,
        domain          = domain,
        min_capacity    = resource_bounds.compute_tokens
    )

    // Filter by contention: prefer agents with available capacity
    candidates = sort(candidates, key = c -> (
        isr.resource_index.active_count(c.agent_id),   // fewer assignments first
        -c.credibility_score                             // higher credibility second
    ))

    FOR candidate IN candidates:
        contention = detect_contention(
            current_intent, candidate.agent_id, AGENT)
        IF NOT contention.contended:
            RETURN candidate

    // All candidates contended; return least-loaded candidate
    // (backpressure will queue it)
    IF len(candidates) > 0:
        RETURN candidates[0]

    RETURN null
```

#### 8.1.3 Resource Optimizer

The Resource Optimizer tracks allocations across the intent tree and reclaims unused margins:

```
function reconcile_resources(parent_id):
    parent = isr.get_intent(parent_id)
    children = isr.get_children(parent_id)

    total_allocated = sum(c.resource_accounting.allocated for c in children)
    total_consumed = sum(c.resource_accounting.consumed
                         for c in children if c.lifecycle_state == COMPLETED)
    total_returned = total_allocated - total_consumed

    parent.resource_accounting.returned_to_parent += total_returned

    if parent.parent_intent_id != null:
        notify_parent_of_surplus(parent.parent_intent_id, total_returned)
```

Redistribution rules:
- Returned resources are available to siblings of the returning child.
- Redistribution is lazy: siblings request additional resources when needed.
- Resources cannot flow upward past a completed parent.

#### 8.1.4 Performance Monitor

System 3 tracks operational metrics and feeds them to System 4:

| Metric | Granularity | Alert Threshold |
|---|---|---|
| Intent completion rate | Per-locus, per-epoch | < 80% over 5-epoch window |
| Decomposition latency | Per-intent | > 2x mean over 10-epoch window |
| Decomposition depth (actual) | Per-intent | > 80% of max_depth |
| Resource utilization | Per-locus, per-epoch | > 90% (overload) or < 20% (underload) |
| Proposed queue depth | Per-locus | > 1,000 (backlog forming) |
| Cross-locus intent ratio | Per-locus, per-epoch | > 30% (excessive cross-locus traffic) |
| Memoization hit rate | Per-locus, per-epoch | < 10% after 100 epochs (cache ineffective) |
| Contention rate | Per-locus, per-epoch | > 20% of leaf assignments |

#### 8.1.5 Failure Playbooks

Pre-defined response procedures for common failure scenarios:

**AGENT_CRASH**: Identify all ACTIVE intents on the failed agent. Re-queue each as PROPOSED. Blacklist agent for 5 epochs. Escalate intents past 50% of deadline to parent for re-decomposition. If agent has significant stake, escalate to System 5.

**DECOMPOSITION_TIMEOUT**: Dissolve partial children. Mark intent as DISSOLVED. Log for System 4 analysis. Escalate if the intent type has > 30% timeout rate.

**RESOURCE_EXHAUSTION**: Pause new PROPOSED intents. Let in-flight intents complete. Aggressive GC on DISSOLVED entries. Request System 4 capacity review. Escalate to System 5 if pause exceeds 10 epochs.

**CASCADE_FAILURE** (completion rate < 50% for 3 epochs): Halt all new decompositions. Identify common failure pattern (shared agent, resource, or cached plan). Invalidate relevant memoization entries. Resume one-at-a-time to isolate cause. Escalate to System 5 for emergency tidal rollback consideration.

**SETTLEMENT_BACKLOG**: Throttle completions to match settlement throughput. Prioritize stake-bearing agent settlements. Alert System 5 if dead letters exceed 100.

**SPANNING_INTENT_PARTITION**: Wait 5 epochs for resolution. If unresolved, timeout spanning children. Re-decompose parent excluding partitioned locus. Escalate to System 4 for cross-locus rebalancing.

#### 8.1.6 Compensation Protocols

Saga-style rollback for partial failures:

```
function compensate_subtree(intent_id, reason):
    intent = isr.get_intent(intent_id)
    children = isr.get_children(intent_id)

    // Phase 1: Stop active children (depth-first, leaves first)
    for child in reverse_topological_order(children):
        if child.lifecycle_state == ACTIVE:
            cancel_agent_execution(child.assigned_agent_id, child.intent_id)
            isr.transition_intent(child.intent_id, "DISSOLVED",
                                  reason="COMPENSATION:" + reason)
        elif child.lifecycle_state == DECOMPOSED:
            compensate_subtree(child.intent_id, reason)  // Recurse
        elif child.lifecycle_state == COMPLETED:
            settlement_router.submit_settlement(
                child.intent_id, "COMPENSATION_DEBIT",
                reverse_entries(child.resource_accounting))
            isr.transition_intent(child.intent_id, "DISSOLVED",
                                  reason="COMPENSATION:" + reason)

    // Phase 2: Dissolve the parent
    isr.transition_intent(intent_id, "DISSOLVED",
                          reason="COMPENSATION:" + reason)

    // Phase 3: Notify upward
    if intent.parent_intent_id != null:
        notify_parent_child_compensated(intent.parent_intent_id, intent_id)
```

**Compensation guarantees**: All settlements for compensated intents are reversed via COMPENSATION_DEBIT. Compensation is idempotent (compensating DISSOLVED is a no-op). Compensation is eventually consistent (settlement reversals may lag state changes).

### 8.2 System 4: Strategic Intelligence

System 4 is the forward-looking component. It reads trends, anticipates future resource needs, and proposes adaptations. System 4 has no direct authority to change operations -- it can only propose. This constraint is fundamental: a system that both plans changes and implements them without checks is a system that can oscillate into instability.

#### 8.2.1 Horizon Scanning via EMA Projections

System 4 reads C6 EMA projections in strictly read-only mode:

```
function horizon_scan(locus_id, window_epochs):
    projections = ema.get_projections(locus_id, window_epochs)  // READ-ONLY

    trends = []
    for projection in projections:
        if projection.growth_rate > TREND_THRESHOLD:
            trends.append(Trend(
                domain=projection.domain, direction="RISING",
                confidence=projection.confidence,
                projected_impact=estimate_intent_volume_impact(projection)))
        if projection.growth_rate < -TREND_THRESHOLD:
            trends.append(Trend(
                domain=projection.domain, direction="FALLING",
                confidence=projection.confidence,
                projected_impact=estimate_resource_reclamation(projection)))

    return HorizonReport(
        locus_id, scan_epoch=current_epoch(),
        trends=trends,
        overall_volatility=compute_volatility(projections))
```

#### 8.2.2 Anticipatory Capacity Planning

Based on horizon scans, System 4 predicts future resource needs:

```
function plan_capacity(horizon):
    proposals = []
    for trend in horizon.trends:
        if trend.direction == "RISING" and trend.confidence > 0.6:
            needed = project_resource_needs(trend, lookahead_epochs=20)
            current = get_current_capacity(horizon.locus_id, trend.domain)
            if needed > current * 1.2:
                proposals.append(CapacityProposal(
                    action="SCALE_UP", domain=trend.domain,
                    target_capacity=needed * 1.1,
                    confidence=trend.confidence))

        elif trend.direction == "FALLING" and trend.confidence > 0.7:
            freeable = estimate_freeable_resources(horizon.locus_id, trend.domain)
            if freeable > 0:
                proposals.append(CapacityProposal(
                    action="SCALE_DOWN", domain=trend.domain,
                    freeable_capacity=freeable,
                    confidence=trend.confidence))

    return CapacityPlan(proposals, horizon_volatility=horizon.overall_volatility)
```

#### 8.2.3 Volatility-Aware Confidence Discounting

When EMA projection volatility is high, System 4 discounts the confidence of its own proposals:

```
function discount_confidence(raw_confidence, volatility):
    // Sigmoid discount: high volatility => sharply reduced confidence
    discount_factor = 1.0 / (1.0 + exp(4.0 * (volatility - 0.5)))
    return raw_confidence * discount_factor
```

**Minimum confidence thresholds by proposal category (after discount)**:

| Category | Min Confidence | Rationale |
|---|---|---|
| CAPACITY_CHANGE | 0.5 | Moderate; errors are recoverable |
| DECOMPOSITION_RULE_UPDATE | 0.7 | Higher bar; affects all future decompositions |
| THRESHOLD_ADJUSTMENT | 0.4 | Low bar; continuously adjustable |
| AGENT_REBALANCING | 0.6 | Moderate; disruptive but reversible |
| OPERATION_CLASS_REMAPPING | 0.8 | High bar; system-wide impact |

#### 8.2.4 Oscillation Dampening

Three mechanisms prevent System 4 from causing oscillatory behavior:

**1. Cool-down timer**: After any accepted proposal, no similar proposal may be submitted for `cool_down_epochs` (default: 5 epochs). "Similar" is defined by proposal category.

**2. Similarity detector**: Proposals with > 85% cosine similarity to a proposal made within the last 20 epochs are blocked. Similarity is computed over the normalized parameter change vectors. This catches inverse proposals (undo-what-was-just-done) and near-inverse proposals.

**3. Stability gating**: Certain proposal categories require N consecutive stable epochs (default: 3) before submission. "Stable" means the relevant metric has varied by less than the stability threshold across the required window.

```
function count_stable_epochs(metric_name, threshold):
    consecutive = 0
    epochs = get_metric_history(metric_name, window=10)
    for i in range(len(epochs) - 1, 0, -1):
        variation = abs(epochs[i] - epochs[i-1]) / max(epochs[i-1], 0.001)
        if variation < threshold:
            consecutive += 1
        else:
            break
    return consecutive
```

### 8.3 System 5: G-Class Governance

System 5 is the identity and governance layer. It maps directly onto C3's existing G-class constitutional consensus mechanism -- System 5 does not introduce new governance primitives. It provides the interface through which the Executive Plane interacts with established governance.

#### 8.3.1 Governance Scope

| Domain | Authority | Mechanism |
|---|---|---|
| System 3 vs System 4 conflict resolution | Final arbiter when System 3 rejects System 4 and System 4 escalates | G-class vote (66% quorum) |
| Operational sovereignty relaxation | Temporarily relax operational constraints | 90% supermajority; max 50-epoch lease; automatic reversion |
| Emergency tidal rollback | Coordinate state rollback on systemic failure | 90% supermajority; 3-epoch timeout |
| System identity constraints | Define invariants no operational/strategic action may violate | Constitutional rules; immutable except by G-class amendment |
| Stake slashing | Authorize stake slashing for proven Byzantine behavior | G-class vote with PCVM evidence required |

#### 8.3.2 Conflict Resolution Protocol

When System 3 rejects a System 4 proposal and System 4 escalates:

```
function resolve_conflict(system3_position, system4_proposal):
    conflict = ConflictPackage(
        system3_position, system4_proposal,
        performance_context=get_recent_metrics(window=20),
        horizon_context=get_recent_horizon_reports(window=20))

    vote_result = c3.g_class_vote(
        topic="S3_S4_CONFLICT", package=conflict,
        quorum_threshold=0.66, timeout_epochs=5)

    match vote_result.outcome:
        "SYSTEM_4_ACCEPTED":
            system3.apply_proposal(system4_proposal)
            return Resolution(winner="SYSTEM_4")
        "SYSTEM_3_SUSTAINED":
            system4.acknowledge_rejection(system4_proposal.proposal_id)
            return Resolution(winner="SYSTEM_3")
        "COMPROMISE":
            system3.apply_proposal(vote_result.compromise_changes)
            return Resolution(winner="COMPROMISE")
        default:
            return Resolution(winner="SYSTEM_3_DEFAULT",
                              reason="No quorum; status quo preserved")
```

#### 8.3.3 Sovereignty Relaxation

Under exceptional circumstances, System 3 may need to operate outside normal constraints. This requires System 5 authorization:

- **Vote threshold**: 90% supermajority of G-class governance-capable agents.
- **Maximum lease**: 50 epochs. No renewal without a fresh vote.
- **Early revocation**: System 5 may revoke if justifying conditions no longer hold.
- **Audit trail**: All relaxations are logged immutably in the C8 DSF settlement ledger.

**Sovereignty relaxation record**:
```json
{
  "relaxation_id": "uuid",
  "requester": "SYSTEM_3",
  "constraint_relaxed": "string",
  "original_value": "...",
  "relaxed_value": "...",
  "justification": "string",
  "lease_epochs": "integer (max 50)",
  "vote_result": {
    "votes_for": "integer",
    "votes_against": "integer",
    "total_eligible": "integer",
    "supermajority_met": "boolean"
  },
  "status": "REQUESTED|APPROVED|DENIED|ACTIVE|EXPIRED|REVOKED",
  "expiry_epoch": "integer|null"
}
```

#### 8.3.4 Emergency Tidal Rollback (ETR)

When systemic failure is detected (cascading failures across loci, ledger corruption, Byzantine supermajority):

```
function emergency_rollback(trigger):
    // Phase 1: Halt all intent processing
    system3.halt_all_intent_processing()
    broadcast_all_loci("EMERGENCY_HALT", trigger)

    // Phase 2: Vote (90% supermajority, 3-epoch timeout)
    vote = c3.g_class_vote(
        topic="EMERGENCY_ROLLBACK", package=trigger,
        quorum_threshold=0.90, timeout_epochs=3)

    if not vote.supermajority_met:
        system3.resume_intent_processing()
        return ABORTED("Supermajority not reached")

    // Phase 3: Determine safe rollback epoch
    rollback_epoch = determine_safe_epoch(trigger)

    // Phase 4: Execute rollback via C3
    c3.tidal_rollback(rollback_epoch)

    // Phase 5: Reconstruct ISR state
    isr.rebuild_from_epoch(rollback_epoch)

    // Phase 6: Resume
    system3.resume_intent_processing()

    return COMPLETED(rollback_epoch, intents_dissolved=isr.count_dissolved_by_rollback())
```

#### 8.3.5 System Identity Constraints

Six invariants that define what the system is and is not:

| Constraint | Description | Enforcement |
|---|---|---|
| Decomposition Termination | All decompositions must terminate (Section 6.2) | System 3 enforces max_depth; System 5 audits |
| Resource Bound Integrity | Children cannot exceed parent bounds (Section 6.4) | System 3 validates at decomposition; System 5 audits settlements |
| Operation Class Monotonicity | Children cannot have higher class than parent (Section 6.1) | System 3 enforces; System 5 validates logs |
| Governance Primacy | No operational action overrides a G-class decision | System 5 intercepts contradicting actions |
| Settlement Completeness | Every COMPLETED intent has a corresponding settlement | Settlement Router guarantees; System 5 audits |
| Provenance Chain Integrity | Every transition has a valid causal stamp and native provenance | ISR enforces; System 5 audits via canonical lineage rules |

### 8.4 The System 3-System 4 Communication Protocol

System 3 and System 4 communicate exclusively through formal **Adaptation Proposals**. This protocol is the mechanism by which future-oriented intelligence influences present-focused operations without bypassing governance.

**Proposal lifecycle**:

```
System 4                    System 3                    System 5
   |                           |                           |
   |-- submit_proposal() ----->|                           |
   |                           |                           |
   |                    cool-down check                    |
   |                    similarity check                   |
   |                    stability gate                     |
   |                           |                           |
   |                    if all gates pass:                  |
   |                    evaluate operational impact         |
   |                           |                           |
   |                    accept/reject/defer                |
   |<-- proposal_outcome ------|                           |
   |                           |                           |
   |  if rejected and S4 escalates:                        |
   |                           |                           |
   |-- escalate_to_s5() ------+-------------------------->|
   |                           |                    G-class vote
   |                           |<---- resolution ---------|
   |<---- resolution ----------|                           |
```

**Adaptation proposal structure**:

```json
{
  "proposal_id": "uuid",
  "proposer": "SYSTEM_4",
  "epoch": "integer",
  "category": "CAPACITY_CHANGE|DECOMPOSITION_RULE_UPDATE|
               THRESHOLD_ADJUSTMENT|AGENT_REBALANCING|
               OPERATION_CLASS_REMAPPING",
  "description": "string",
  "justification": {
    "horizon_report_id": "string",
    "supporting_metrics": [
      { "metric_name": "string", "current_value": "number",
        "projected_value": "number", "confidence": "number" }
    ],
    "risk_assessment": "LOW|MEDIUM|HIGH"
  },
  "proposed_changes": [
    { "parameter": "string", "current_value": "...",
      "proposed_value": "...", "rollback_value": "..." }
  ],
  "cool_down_epochs": "integer (default: 5)",
  "stability_gate": {
    "required_stable_epochs": "integer (default: 3)",
    "stability_metric": "string",
    "stability_threshold": "number"
  },
  "status": "PENDING|ACCEPTED|REJECTED|DEFERRED|
             COOLDOWN_BLOCKED|SIMILARITY_BLOCKED"
}
```

**Proposal submission flow**:

```
function submit_proposal(proposal):
    // 1. Cool-down check
    last_similar = find_last_similar_proposal(proposal.category)
    if last_similar != null:
        if current_epoch() - last_similar.epoch < proposal.cool_down_epochs:
            return BLOCKED("cool_down",
                           retry_after=last_similar.epoch + proposal.cool_down_epochs)

    // 2. Similarity detection
    for recent in get_proposals_in_window(proposal.category, window_epochs=20):
        if cosine_similarity(proposal.proposed_changes,
                             recent.proposed_changes) > 0.85:
            return BLOCKED("similar_proposal_recent", similar_id=recent.proposal_id)

    // 3. Stability gate
    if proposal.stability_gate != null:
        stable = count_stable_epochs(
            proposal.stability_gate.stability_metric,
            proposal.stability_gate.stability_threshold)
        if stable < proposal.stability_gate.required_stable_epochs:
            return DEFERRED("stability_gate_not_met",
                            stable_epochs=stable,
                            required=proposal.stability_gate.required_stable_epochs)

    // 4. Submit to System 3
    system3.receive_proposal(proposal)
    return PENDING
```

### 8.5 Why Three Systems, Not Two or Four

The choice of three executive systems is not arbitrary -- it reflects a deep structural requirement.

**Why not two systems?** If we merge System 3 and System 4 into a single "operational + strategic" executive, the same component that plans adaptations also implements them. There is no check on whether an adaptation is wise -- the system can propose a change, approve its own proposal, and implement it in a single cycle. This creates a classic feedback loop: a noisy signal triggers an adaptation, the adaptation worsens the situation, and the worsened situation triggers a stronger adaptation. Beer called this "the oscillation problem" and it is the primary reason the VSM separates System 3 from System 4.

**Why not four or more systems?** Beer's original model includes System 1 (Operations) and System 2 (Coordination). In Atrahasis, these already exist: C3 parcels are System 1 and C3 tidal scheduling is System 2. Adding them to RIF's Executive Plane would duplicate existing functionality and violate Principle 4 (Substrate Awareness). Similarly, System 3* (Audit) maps to C5 PCVM + Sentinel, which already exists and which RIF integrates via the Failure Detector.

The three systems in RIF's Executive Plane are exactly the VSM components that were *missing* from the Atrahasis stack:

| VSM System | Was it already in Atrahasis? | RIF's role |
|---|---|---|
| System 1 (Operations) | Yes -- C3 parcels | N/A (substrate) |
| System 2 (Coordination) | Yes -- C3 tidal scheduling | N/A (substrate) |
| System 3 (Internal Control) | **No** | RIF System 3 |
| System 3* (Audit) | Yes -- C5 PCVM + Sentinel | Integration via Failure Detector |
| System 4 (Intelligence) | **No** | RIF System 4 |
| System 5 (Policy) | Partially -- G-class governance existed but had no executive interface | RIF System 5 (interface to existing governance) |

Three systems is not a design choice -- it is a consequence of filling exactly the gaps that existed. No more, no less.

---

## 9. Graduated Sovereignty Model

### 9.1 The Sovereignty Deadlock Problem

Any orchestration layer that coordinates autonomous subsystems faces a fundamental paradox. The subsystems -- C3 (Tidal Noosphere), the native communication stack, C5 (PCVM), and C6 (EMA) -- were designed to operate with sovereignty over their internal state. C5 alone decides how claims are classified. C6 alone decides when to consolidate knowledge. C3 alone schedules its tidal epochs. If the orchestration layer can override these decisions, sovereignty is illusory; if it cannot, orchestration is impossible.

This is the sovereignty deadlock: absolute sovereignty prevents orchestration, and absolute orchestration destroys sovereignty.

RIF resolves this deadlock not by choosing one extreme but by stratifying the concept itself. Not all sovereignty protections carry the same weight. The immutability of PCVM's classification taxonomy (a property that defines what the system *is*) occupies a fundamentally different category from a preferred SHREC allocation ratio (a tunable parameter). Treating them identically -- both inviolable, or both overridable -- is the source of the deadlock.

Graduated sovereignty partitions every system parameter into one of three tiers, each with distinct authorization requirements, modification protocols, and reversion semantics.

### 9.2 Three-Tier Formal Specification

```
+=========================================================================+
|                     GRADUATED SOVEREIGNTY MODEL                         |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 1 -- CONSTITUTIONAL (Immutable)                              | |
|  |  Authorization: NEVER modifiable at runtime                       | |
|  |  Reversion: N/A -- cannot be changed                               | |
|  |  Enforcement: System 5 audit + hard-coded assertion               | |
|  |  Defines: What the system IS                                      | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 2 -- OPERATIONAL (Governance-Relaxable)                      | |
|  |  Authorization: 90% G-class supermajority                         | |
|  |  Reversion: Auto-revert after lease (max 50 epochs)               | |
|  |  Enforcement: System 5 vote + lease monitor                       | |
|  |  Defines: How the system NORMALLY operates                        | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 3 -- COORDINATION (Advisory)                                 | |
|  |  Authorization: System 3 may override unilaterally                | |
|  |  Reversion: Continuous adjustment                                 | |
|  |  Enforcement: Performance monitoring + System 4 feedback          | |
|  |  Defines: What the system PREFERS                                 | |
|  +-------------------------------------------------------------------+ |
+=========================================================================+
```

#### 9.2.1 Tier 1 -- Constitutional Invariants

Constitutional invariants define properties so fundamental that their violation would constitute a different system entirely. They cannot be relaxed, suspended, or overridden under any circumstances. Violation of a constitutional invariant triggers immediate rejection of the offending action, immutable audit logging, and -- if the invariant was somehow bypassed -- system halt and rollback.

| ID | Invariant | Description | Cross-Reference | Enforcement |
|---|---|---|---|---|
| C-01 | PCVM Classification Integrity | Claim classification taxonomy immutable at runtime | C5 PCVM S3.1 | System 5 audit; ISR rejects targeting intents |
| C-02 | VTD Immutability | Verified Trust Documents are append-only; no mutation | C5 PCVM S4.2 | Admission Gate S12; ISR hard-reject |
| C-03 | EMA Canonical Source | EMA is sole authority for epistemic quanta; RIF reads only | C6 EMA S2.1 | System 4 interface read-only by construction |
| C-04 | Decomposition Termination | All decompositions terminate in finite steps; max_depth hard cap 20 | S6.2 | System 3 depth guard (hard-coded) |
| C-05 | Operation Class Monotonicity | Children have equal or lower class rank than parent | S6.1 | System 3 assertion in decompose_intent() |
| C-06 | Resource Bound Integrity | Children cannot exceed parent resource envelopes | S6.4 | System 3 validate_resource_partition() |
| C-07 | Provenance Chain Completeness | Every intent transition carries valid CausalStamp traceable via native sovereign claim objects | S3.2, S3.3 | ISR rejects transitions without CausalStamp |
| C-08 | Settlement Completeness | Every COMPLETED intent produces a settlement entry in C8 DSF ledger | S3.4 | Settlement Router at-least-once guarantee |

**Constitutional enforcement pseudocode:**

```
function enforce_constitutional(action: SystemAction) -> EnforcementResult:
    for invariant in CONSTITUTIONAL_INVARIANTS:
        violation = invariant.check(action)
        if violation != null:
            // Log immutably -- this attempt is recorded regardless of outcome
            audit_log.append(ConstitutionalViolationAttempt(
                invariant_id = invariant.id,
                action       = action,
                epoch        = current_epoch(),
                violation    = violation
            ))
            // Hard reject -- no appeal, no override, no governance vote
            return EnforcementResult.HARD_REJECT(
                invariant_id = invariant.id,
                reason       = violation.description
            )
    return EnforcementResult.PASS
```

The critical design choice is that constitutional enforcement is *two-layered*: the `enforce_constitutional()` function runs inline on every system action (prevention), and System 5 runs a continuous background audit against all ISR state (detection). Even if one layer has a bug, the other catches violations. This defense-in-depth is what makes the "NEVER" guarantee credible rather than aspirational.

#### 9.2.2 Tier 2 -- Operational Constraints

Operational constraints govern resource allocations, composition rules, and timing parameters. They represent the system's normal operating envelope -- sensible defaults that should hold under typical conditions but may need temporary adjustment during exceptional circumstances.

| ID | Constraint | Default | Relaxation Bounds | Cross-Reference |
|---|---|---|---|---|
| O-01 | VRF Composition Rules | Standard C3 VRF composition | Expanded composition sets | C3 S5.3 |
| O-02 | Metabolic Timing Windows | C6-defined epoch boundaries | Extend/contract up to 2x | C6 S4.1 |
| O-03 | SHREC Allocation Ratios | C6 defaults | Shift within +/-20% | C6 S6.2 |
| O-04 | Cross-Locus Intent Threshold | 20% of locus traffic | Increase to 40% max | S13.2 |
| O-05 | Decomposition Depth Soft Limit | 10 levels | Increase to 15 (hard max 20 per C-04) | S6.5 |
| O-06 | Memoization Cache TTL | 50 epochs | Extend to 100 epochs | S6.6 |
| O-07 | Agent Credibility Floor | 0.5 PCVM score | Lower to 0.3 during capacity shortage | S5.1 |
| O-08 | Settlement Retry Limit | 10 attempts | Increase to 20 during congestion | S3.4 |
| O-09 | Failure Detector Quorum | 3 sentinels | Reduce to 2 during low-agent conditions | S3.5 |
| O-10 | ISR Bandwidth Cap | 5% of locus network | Increase to 8% during high-intent periods | S3.3 |

Each operational constraint has a well-defined relaxation range. The requested relaxed value must fall within this range; requests exceeding the bounds are rejected before reaching the vote. This prevents "relaxation creep" -- the gradual widening of bounds through repeated requests.

#### 9.2.3 Tier 3 -- Coordination Parameters

Coordination parameters are advisory hints that System 3 may override unilaterally based on operational needs. No governance vote is required. These parameters express preferences, not requirements.

| ID | Parameter | Default | Override Authority |
|---|---|---|---|
| A-01 | Agent Workload Preferences | Agent-declared | System 3 intent assignment |
| A-02 | Preferred Decomposition Strategy | Intent-declared | System 3 strategy selector |
| A-03 | Locus Affinity Hints | Agent-declared | System 3 cross-locus routing |
| A-04 | Priority Boost Requests | Proposer-declared | System 3 queue management |
| A-05 | Output Format Preferences | Intent-declared | Parcel Executor normalization |
| A-06 | Monitoring Verbosity | Locus-default | System 3 performance monitor |

### 9.3 Sovereignty Relaxation Protocol

When operational conditions require temporary deviation from Tier 2 constraints, the Sovereignty Relaxation Protocol activates. The protocol has five phases: Request, Vote, Activation, Monitoring, and Termination.

#### 9.3.1 Request Phase

System 3 or System 4 identifies an operational condition that would benefit from temporarily relaxing a Tier 2 constraint. The requester constructs a formal relaxation request:

```json
{
  "$schema": "https://atrahasis.org/rif/sovereignty-relaxation-request/v1",
  "type": "object",
  "properties": {
    "request_id":               { "type": "string", "format": "uuid" },
    "requester":                { "type": "string", "enum": ["SYSTEM_3", "SYSTEM_4"] },
    "request_epoch":            { "type": "integer" },
    "constraint_id":            { "type": "string", "description": "O-01 through O-10" },
    "current_value":            { "description": "Current enforced value" },
    "requested_value":          { "description": "Proposed relaxed value" },
    "justification": {
      "type": "object",
      "properties": {
        "trigger_condition":    { "type": "string" },
        "supporting_metrics":   { "type": "array", "items": {
          "type": "object",
          "properties": {
            "metric_name":      { "type": "string" },
            "current_value":    { "type": "number" },
            "threshold_value":  { "type": "number" },
            "window_epochs":    { "type": "integer" }
          }
        }},
        "impact_assessment":    { "type": "string" },
        "risk_if_denied":       { "type": "string" }
      },
      "required": ["trigger_condition", "supporting_metrics",
                    "impact_assessment", "risk_if_denied"]
    },
    "requested_lease_epochs":   { "type": "integer", "minimum": 1, "maximum": 50 },
    "anti_cascade_declaration": {
      "type": "object",
      "properties": {
        "dependent_constraints": { "type": "array", "items": { "type": "string" } },
        "cascade_risk":          { "type": "string", "enum": ["NONE","LOW","MEDIUM","HIGH"] },
        "mitigation":            { "type": "string" }
      },
      "required": ["dependent_constraints", "cascade_risk"]
    }
  },
  "required": ["request_id", "requester", "request_epoch", "constraint_id",
               "current_value", "requested_value", "justification",
               "requested_lease_epochs", "anti_cascade_declaration"]
}
```

#### 9.3.2 Vote Phase

The request undergoes three pre-validation checks before reaching the G-class vote:

```
function process_relaxation_request(
    request: SovereigntyRelaxationRequest
) -> RelaxationOutcome:

    // PRE-CHECK 1: Constitutional guard
    if request.constraint_id in CONSTITUTIONAL_INVARIANTS:
        return DENIED("CONSTITUTIONAL_INVIOLABLE")

    // PRE-CHECK 2: Relaxation bounds
    bounds = OPERATIONAL_CONSTRAINTS[request.constraint_id].relaxation_bounds
    if not bounds.contains(request.requested_value):
        return DENIED("EXCEEDS_RELAXATION_BOUNDS", max=bounds.max)

    // PRE-CHECK 3: Anti-cascade
    active = get_active_relaxations()
    cascade_count = count_related(
        request.anti_cascade_declaration.dependent_constraints, active
    )
    if cascade_count >= MAX_CONCURRENT_RELATED_RELAXATIONS:  // default: 2
        return DENIED("ANTI_CASCADE_LIMIT", active_related=cascade_count)

    // G-CLASS VOTE: 90% supermajority, 3-epoch timeout
    vote_result = c3.g_class_vote(
        topic     = "SOVEREIGNTY_RELAXATION",
        package   = RelaxationVotePackage(request, active, system_health()),
        quorum    = 0.90,
        timeout   = 3  // epochs
    )

    if not vote_result.supermajority_met:
        return DENIED("SUPERMAJORITY_NOT_MET",
                       for=vote_result.votes_for,
                       against=vote_result.votes_against)

    // ACTIVATE LEASE
    lease = SovereigntyLease(
        relaxation_id  = request.request_id,
        constraint_id  = request.constraint_id,
        original_value = request.current_value,
        relaxed_value  = request.requested_value,
        start_epoch    = current_epoch(),
        expiry_epoch   = current_epoch() + request.requested_lease_epochs,
        vote_record    = vote_result,
        status         = "ACTIVE"
    )
    activate_lease(lease)
    return APPROVED(lease)
```

#### 9.3.3 Lease Structure and Lifecycle

Every approved relaxation creates a time-bounded lease. The lease stores the original value immutably -- guaranteeing that reversion restores the exact pre-relaxation state.

```json
{
  "$schema": "https://atrahasis.org/rif/sovereignty-lease/v1",
  "type": "object",
  "properties": {
    "relaxation_id":    { "type": "string", "format": "uuid" },
    "constraint_id":    { "type": "string" },
    "original_value":   { "description": "Value to revert to on expiry" },
    "relaxed_value":    { "description": "Currently active relaxed value" },
    "start_epoch":      { "type": "integer" },
    "expiry_epoch":     { "type": "integer" },
    "vote_record": {
      "type": "object",
      "properties": {
        "votes_for":      { "type": "integer" },
        "votes_against":  { "type": "integer" },
        "total_eligible": { "type": "integer" },
        "vote_epoch":     { "type": "integer" }
      }
    },
    "monitoring": {
      "type": "object",
      "properties": {
        "health_check_interval_epochs": { "type": "integer", "default": 5 },
        "revocation_trigger_metric":    { "type": "string" },
        "revocation_threshold":         { "type": "number" }
      }
    },
    "status": { "type": "string", "enum": ["ACTIVE","EXPIRED","REVOKED","SUPERSEDED"] }
  }
}
```

#### 9.3.4 Monitoring and Automatic Reversion

System 5 monitors all active leases every epoch. Three conditions trigger reversion:

```
function monitor_active_leases():
    for lease in get_active_leases():

        // CONDITION 1: Lease expiry (temporal bound)
        if current_epoch() >= lease.expiry_epoch:
            revert_constraint(lease.constraint_id, lease.original_value)
            lease.status = "EXPIRED"
            continue

        // CONDITION 2: Health degradation (operational bound)
        if lease.monitoring.revocation_trigger_metric != null:
            val = get_metric(lease.monitoring.revocation_trigger_metric)
            if val > lease.monitoring.revocation_threshold:
                revert_constraint(lease.constraint_id, lease.original_value)
                lease.status = "REVOKED"
                lease.revocation_reason = "Health metric exceeded threshold"

        // CONDITION 3: Cascade revocation (dependency bound)
        for dep in lease.dependent_constraints:
            if was_recently_revoked(dep, within_epochs=5):
                revert_constraint(lease.constraint_id, lease.original_value)
                lease.status = "REVOKED"
                lease.revocation_reason = "Dependent relaxation revoked"
```

#### 9.3.5 Anti-Cascade Invariant

The anti-cascade invariant prevents sovereignty relaxations from amplifying into unbounded constraint erosion.

**Formal statement:** At any epoch *e*, for all pairs (L1, L2) of active leases, if L1.dependent_constraints intersects L2.dependent_constraints is non-empty, the count of active leases in that overlapping cluster must not exceed `MAX_CONCURRENT_RELATED_RELAXATIONS` (default: 2).

This is enforced at request time (pre-check 3 in S9.3.2) and again at monitoring time (condition 3 in S9.3.4). The request-time check prevents new relaxations from creating oversized clusters. The monitoring-time check revokes existing relaxations if a related relaxation is revoked, preventing orphaned relaxations from persisting in a now-unstable cluster.

### 9.4 Safety Guarantees

#### 9.4.1 No Permanent Sovereignty Loss

**Claim:** No sovereignty relaxation can permanently alter a Tier 2 constraint.

**Proof sketch:**

1. Every approved relaxation creates a lease with `expiry_epoch = start_epoch + requested_lease_epochs`.
2. `requested_lease_epochs` has hard maximum 50 (enforced at request validation).
3. `monitor_active_leases()` runs every epoch; reverts any lease where `current_epoch() >= expiry_epoch`.
4. Lease renewal requires a *fresh* 90% supermajority vote -- no automatic renewal exists.
5. `original_value` is stored immutably at lease creation.
6. Even if monitoring experiences transient failure (delayed by *k* epochs), the Failure Detector detects monitor failure within 3 epochs (S3.5), bounding maximum overshoot to `50 + 3 = 53` epochs. No permanent alteration is possible. QED.

#### 9.4.2 No Cascade Amplification

**Claim:** Sovereignty relaxations cannot cascade into unbounded constraint erosion.

**Proof sketch:** The anti-cascade invariant (S9.3.5) bounds cluster size at `MAX_CONCURRENT_RELATED_RELAXATIONS`. With 10 Tier 2 constraints and a cluster limit of 2, the maximum concurrent relaxations is 10 (all constraints relaxed independently). Each has a 50-epoch maximum lease. Full reversion occurs within 50 epochs of the last granted lease. QED.

#### 9.4.3 Constitutional Inviolability

**Claim:** No runtime action can violate a Tier 1 constitutional invariant.

**Proof sketch:** (1) `enforce_constitutional()` runs on every system action before execution. (2) If any constitutional invariant check fails, the action receives HARD_REJECT with no appeal mechanism. (3) The relaxation protocol explicitly rejects requests targeting constitutional IDs before reaching the vote. (4) The invariant set is defined at compile time in an immutable data structure. (5) System 5 continuously audits constitutional compliance independently. Two-layer defense (inline enforcement + background audit) ensures that even a single-layer bug is caught. QED.

---

## 10. Recursive Decomposition Hierarchy

### 10.1 Overview

The three-level decomposition hierarchy maps the logical structure of intent decomposition onto the physical structure of the C3 locus network. Each level has a distinct scope, replication strategy, and failure model.

```
+=========================================================================+
|                   RECURSIVE DECOMPOSITION HIERARCHY                     |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |                    GLOBAL EXECUTIVE (GE)                          | |
|  |  Scope: Cross-locus intents + G-class governance                  | |
|  |  Instances: 1 logical (BFT-replicated, 3f+1 nodes)               | |
|  |  Throughput: 100 cross-locus intents/epoch                        | |
|  +----+---------------------------+----------------------------+-----+ |
|       |                           |                            |       |
|       v                           v                            v       |
|  +-----------+             +-----------+              +-----------+    |
|  | Locus     |             | Locus     |              | Locus     |    |
|  | Decomposer|             | Decomposer|              | Decomposer|    |
|  | (LD-A)    |             | (LD-B)    |              | (LD-C)    |    |
|  +-----+-----+             +-----+-----+              +-----+-----+    |
|        |                         |                           |         |
|   +----+----+              +-----+-----+               +----+----+    |
|   v    v    v              v     v     v               v    v    v    |
|  +--+ +--+ +--+          +--+ +--+ +--+             +--+ +--+ +--+  |
|  |PE| |PE| |PE|          |PE| |PE| |PE|             |PE| |PE| |PE|  |
|  +--+ +--+ +--+          +--+ +--+ +--+             +--+ +--+ +--+  |
|  Parcel Executors         Parcel Executors            Parcel Executors |
+=========================================================================+
```

### 10.2 Global Executive (GE)

#### 10.2.1 Scope and Responsibilities

The Global Executive handles only intents that *must* span loci. Specifically:

- **Cross-locus intents:** Any intent whose `scope.target_loci` contains more than one locus ID.
- **G-class intents:** Any intent with `operation_class = G` (governance operations).
- **System 4 adaptation proposals** affecting multiple loci.
- **System 5 conflict resolutions** and sovereignty relaxation votes.

Intents that are purely local (single locus in `target_loci`, non-G-class) bypass the GE entirely. This is the key to sub-linear scaling: if 80%+ of intents are locus-local, 80%+ of the system's work never touches the GE.

#### 10.2.2 HotStuff BFT Replication

The GE is a single logical instance replicated across `3f + 1` nodes using the **HotStuff** BFT consensus protocol (Yin et al., 2019), where `f` is the maximum tolerated Byzantine failures. HotStuff is selected for six properties:

1. **Linear message complexity:** O(n) messages per round (vs. O(n^2) for classic PBFT), achieved through threshold signatures aggregated by the leader.
2. **Pipelined phases:** HotStuff pipelines its three phases (PREPARE, PRE-COMMIT, COMMIT) such that a new proposal can begin before the previous one fully commits, increasing throughput.
3. **Optimistic responsiveness:** In the common case (honest leader, synchronous network), consensus completes in the time of actual message delays, not worst-case timeout bounds.
4. **Simple leader rotation:** Replaces PBFT's complex view-change protocol with a straightforward leader rotation after each decision (or on timeout).
5. **Safety under asynchrony:** Safety (no two honest replicas commit conflicting states) holds regardless of network timing assumptions.
6. **Liveness under partial synchrony:** Progress is guaranteed after GST (Global Stabilization Time) when the leader is honest -- matches the partial synchrony model assumed by the Atrahasis stack.

```
GE Replication Configuration:
  f                   = 1 (default; tolerates 1 Byzantine node)
  replicas            = 3f + 1 = 4
  consensus_protocol  = HotStuff (linear, pipelined)
  message_complexity  = O(n) per round (threshold signatures)
  leader_rotation     = Per tidal epoch, round-robin among GE seats
                        (fallback: on leader timeout = 2 * epoch_duration)
  liveness            = Guaranteed under partial synchrony with honest leader
  safety              = BFT: tolerates f < n/3 Byzantine replicas
  state_sync          = Merkle-diff, every 10 epochs
  checkpoint          = Every 50 epochs; 2 retained
  threshold_signature = BLS12-381 (n-of-n aggregation for O(n)->O(1) verification)
```

**GE replicated state includes:** active cross-locus intents, pending governance votes, locus capability summaries, routing table (locus health scores, available capacity), current epoch, and leader ID.

#### 10.2.3 HotStuff Consensus Round

The GE's HotStuff consensus is the mechanism that implements C3's G-class governance operations at the cross-locus level:

```
FUNCTION ge_hotstuff_round(proposal: IntentQuantum | GovernanceVote) -> ConsensusResult:
    // HotStuff 3-phase pipeline (PREPARE -> PRE-COMMIT -> COMMIT)

    leader = ge_seats[current_epoch % len(ge_seats)]

    // Phase 1: PREPARE
    // Leader proposes; replicas validate and send partial threshold signatures
    prepare_msg = HotStuffMessage {
        type:      PREPARE,
        proposal:  proposal,
        view:      current_epoch,
        leader_id: leader.id,
        qc:        last_committed_qc    // quorum certificate from previous round
    }
    leader.broadcast(prepare_msg)
    prepare_votes = leader.collect_threshold_sigs(phase=PREPARE, quorum=2f+1)
    prepare_qc = aggregate_threshold_signatures(prepare_votes)

    // Phase 2: PRE-COMMIT
    // Leader sends prepare_qc; replicas lock on proposal
    precommit_msg = HotStuffMessage {
        type:      PRE_COMMIT,
        proposal:  proposal,
        view:      current_epoch,
        qc:        prepare_qc
    }
    leader.broadcast(precommit_msg)
    precommit_votes = leader.collect_threshold_sigs(phase=PRE_COMMIT, quorum=2f+1)
    precommit_qc = aggregate_threshold_signatures(precommit_votes)

    // Phase 3: COMMIT
    // Leader sends precommit_qc; replicas commit
    commit_msg = HotStuffMessage {
        type:      COMMIT,
        proposal:  proposal,
        view:      current_epoch,
        qc:        precommit_qc
    }
    leader.broadcast(commit_msg)
    commit_votes = leader.collect_threshold_sigs(phase=COMMIT, quorum=2f+1)
    commit_qc = aggregate_threshold_signatures(commit_votes)

    // Committed: apply to GE state
    ge_state.apply(proposal)

    RETURN ConsensusResult {
        status:    COMMITTED,
        qc:        commit_qc,
        epoch:     current_epoch,
        proposal:  proposal
    }


FUNCTION ge_leader_timeout_handler():
    // If leader fails to drive consensus within 2 * epoch_duration:
    //   1. Replicas increment view (epoch stays the same, view is logical)
    //   2. Next leader in round-robin takes over
    //   3. New leader includes highest QC it has seen (key HotStuff liveness property)
    //   4. No complex view-change sub-protocol (unlike classic PBFT)
    next_leader_idx = (current_leader_idx + 1) % len(ge_seats)
    new_view_msg = HotStuffMessage {
        type:      NEW_VIEW,
        view:      current_view + 1,
        leader_id: ge_seats[next_leader_idx].id,
        highest_qc: local_highest_qc
    }
    broadcast(new_view_msg)
```

**G-class mapping flow:**

```
C3 G-class governance operation
    |
    v
System 5 receives G-class intent (operation_class = G)
    |
    v
System 5 packages governance vote via GovernanceVoteRequest
    |
    v
GE routes to HotStuff consensus round (ge_hotstuff_round)
    |
    v
HotStuff commits with 2f+1 threshold signatures
    |
    v
Result returned to System 5 as VoteResult
    |
    v
System 5 applies governance outcome (relaxation, parameter change, etc.)
```

#### 10.2.4 Throughput Model

```
GE Throughput Budget:
  Target:     100 cross-locus intents per epoch
  Hard limit: 200 (backpressure above this)
  Per-intent: ~5ms routing decision + ~15ms HotStuff consensus round
  At f=1 (4 replicas): 4 messages per consensus round (O(n), leader collects)
  At f=2 (7 replicas): 7 messages per consensus round (O(n), leader collects)

Routing Decision for cross-locus intent:
  1. Read locus capability summaries     O(L)       L = target loci
  2. Select optimal locus assignment     O(L*logA)  A = agents
  3. Produce SpanningIntentStubs         O(L)
  4. Commit via HotStuff                 O(n)       n = replicas
```

### 10.3 Locus Decomposer (LD)

#### 10.3.1 Scope

The Locus Decomposer is the workhorse of the hierarchy. Each C3 locus has exactly one LD instance (with active-passive failover per S10.5). The LD:

- Receives intents from the GE (cross-locus sub-intents) or directly from local agents (locus-local intents).
- Applies the decomposition algebra (S6) to produce child intents.
- Assigns leaf intents to Parcel Executors.
- Manages the locus-local Intent State Registry.
- Reports completion/failure upward to the GE (for spanning intents) or evaluates parent success criteria directly (for locus-local intents).

#### 10.3.2 Domain Knowledge

Each LD maintains domain-specific knowledge for efficient decomposition: a local agent capability index, a memoization cache (S6.6), the C3 parcel topology, historical decomposition statistics (average depth, branching factor, failure rates by operation class), and current throughput metrics. This domain knowledge is what enables locus-local intents to be decomposed without touching the GE.

#### 10.3.3 Decomposition to Parcel Tasks

```
function ld_decompose_and_assign(intent: IntentQuantum):
    // Step 1: Decompose using System 3 engine (S4.1.1)
    result = decompose_intent(intent, depth=0)
    if result.is_failure():
        handle_decomposition_failure(intent, result)
        return

    // Step 2: Assign each leaf intent to a Parcel Executor
    for leaf in result.plan.leaves():
        // Contention-aware agent selection (PA-5/F51 integrated)
        agent = select_agent(
            operation_class = leaf.operation_class,
            domain          = leaf.scope.domain,
            resource_bounds = leaf.resource_bounds
        )
        if agent == null:
            if intent.constraints.allow_spanning:
                escalate_to_ge(leaf)    // Cross-locus escalation
            else:
                handle_no_agent_failure(intent, leaf)
            continue

        // Step 3: Apply backpressure if agent is at capacity
        bp_result = apply_backpressure(agent.agent_id, leaf)
        if bp_result.action == QUEUED:
            // Intent is queued; will be assigned when capacity frees
            continue

        // Step 4: Map leaf to C3 tidal schedule
        parcel_executor = get_parcel_executor(agent.parcel_id)
        parcel_executor.enqueue(leaf, agent)

        // Step 5: Transition leaf to ACTIVE
        isr.transition_intent(leaf.intent_id, "ACTIVE",
                              reason="ASSIGNED_TO_AGENT")
```

### 10.4 Parcel Executor (PE)

#### 10.4.1 Scope

The Parcel Executor connects RIF intents with C3's tidal scheduling. Each PE maps 1:1 to a C3 parcel and handles:

- Receiving leaf intents from the LD.
- Scheduling execution within C3 tidal epochs via `c3.schedule_operation()`.
- Monitoring execution progress via C3 callbacks.
- Reporting completion or failure back to the LD.

#### 10.4.2 Execution Mapping

```
function pe_execute_intent(leaf: IntentQuantum, agent: AgentRecord):
    // Map intent to C3 operation
    c3_op = map_intent_to_c3_operation(leaf)

    // Submit to tidal scheduler
    result = c3.schedule_operation(
        operation = c3_op,
        agent_id  = agent.agent_id,
        parcel_id = agent.parcel_id,
        deadline  = leaf.constraints.deadline_epoch,
        priority  = leaf.constraints.priority
    )

    if result.status == "REJECTED":
        report_to_ld(leaf.intent_id, ExecutionReport(
            outcome = "FAILURE",
            reason  = "C3_SCHEDULE_REJECTED",
            details = result.rejection_reason
        ))
        return

    // Register callback -- C3 notifies PE on completion
    register_callback(result.execution_id, lambda res:
        pe_handle_result(leaf, res))

function pe_handle_result(leaf: IntentQuantum, result: C3ExecutionResult):
    match result.status:
        case "COMPLETED":
            outcome = evaluate_leaf_success_criteria(
                leaf.success_criteria, result.output
            )
            report_to_ld(leaf.intent_id, ExecutionReport(
                outcome            = outcome,
                output_parcel_ids  = result.output_parcel_ids,
                resource_consumed  = result.resource_consumed,
                completion_epoch   = current_epoch()
            ))
        case "FAILED":
            report_to_ld(leaf.intent_id, ExecutionReport(
                outcome           = "FAILURE",
                reason            = result.failure_reason,
                resource_consumed = result.resource_consumed
            ))
        case "TIMEOUT":
            report_to_ld(leaf.intent_id, ExecutionReport(
                outcome           = "TIMEOUT",
                resource_consumed = result.resource_consumed
            ))

    // Trigger assignment queue processing for the agent
    process_assignment_queue(agent.agent_id)
```

### 10.5 Cross-Level Communication Protocol

All messages between hierarchy levels share a common envelope:

```json
{
  "$schema": "https://atrahasis.org/rif/cross-level-envelope/v1",
  "properties": {
    "message_id":          { "type": "string", "format": "uuid" },
    "direction":           { "enum": ["DOWNWARD", "UPWARD", "LATERAL"] },
    "source_level":        { "enum": ["GE", "LD", "PE"] },
    "target_level":        { "enum": ["GE", "LD", "PE"] },
    "source_id":           { "type": "string" },
    "target_id":           { "type": "string" },
    "message_type":        { "enum": [
      "INTENT_ASSIGNMENT", "EXECUTION_REPORT", "STATUS_QUERY",
      "STATUS_RESPONSE", "CANCEL_INTENT", "RESOURCE_UPDATE",
      "LOCUS_HEALTH_REPORT", "ESCALATION"
    ]},
    "payload":             { "type": "object" },
    "causal_stamp":        { "$ref": "#/$defs/CausalStamp" },
    "delivery_guarantee":  { "enum": ["AT_LEAST_ONCE","EXACTLY_ONCE","BEST_EFFORT"] },
    "ttl_epochs":          { "type": "integer", "default": 10 }
  }
}
```

**Delivery guarantees:**

- **AT_LEAST_ONCE:** Persisted in durable outbox, retried with exponential backoff (1, 2, 4, 8, ... epochs, max 32). Receiver deduplicates by `message_id`. Used for all state-changing messages.
- **EXACTLY_ONCE:** AT_LEAST_ONCE with sender-side deduplication tracking. Used for settlement messages only.
- **BEST_EFFORT:** Fire-and-forget. Used for status queries, health reports, and resource advertisements. Staleness is acceptable.

**Lateral messages** between Locus Decomposers route via the GE's routing table when direct LD-to-LD connectivity is unavailable, ensuring partitioned loci can communicate indirectly through any non-partitioned GE replica.

### 10.6 Locus Fault Tolerance

#### 10.6.1 Active-Passive Replication

Each LD runs as an active-passive pair. The active instance handles all decomposition. The passive receives state updates via synchronous WAL replication (sync lag tolerance: 1 epoch maximum; full ISR snapshot every 10 epochs).

#### 10.6.2 Failover Protocol

```
FAILOVER PROTOCOL (target: 1-epoch total recovery)

Phase 1: DETECT (< 0.5 epoch)
  Trigger (ANY of):
    - Active LD misses 3 consecutive heartbeats
    - Active LD misses 2 consecutive state syncs to passive
    - GE receives no LOCUS_HEALTH_REPORT for 3 epochs
    - Local sentinels reach quorum on LD liveness = false

Phase 2: VERIFY (< 0.25 epoch)
    - Passive sends 3 direct health probes (100ms each) to active
    - If active responds: FALSE ALARM -- cancel failover
    - If no response: cross-check with Failure Detector quorum
    - Proceed to PROMOTE only if quorum confirms

Phase 3: PROMOTE (< 0.1 epoch)
    1. Passive acquires LD leadership lock (distributed lock via C3)
    2. Replay un-applied WAL entries
    3. Transition to ACTIVE role
    4. Notify GE of leadership change
    5. Notify all local PEs of leadership change

Phase 4: STABILIZE (< 0.15 epoch)
    1. Reconcile ISR state (query PEs for in-flight intent status)
    2. Resume normal decomposition
    3. Spawn new passive LD instance (may take several epochs)
    4. Begin synchronous replication to new passive
```

```
+------------------+-------------------+
| Phase            | Time Budget       |
+------------------+-------------------+
| DETECT           | < 0.50 epoch      |
| VERIFY           | < 0.25 epoch      |
| PROMOTE          | < 0.10 epoch      |
| STABILIZE        | < 0.15 epoch      |
+------------------+-------------------+
| TOTAL            | < 1.00 epoch      |
+------------------+-------------------+
```

#### 10.6.3 Emergency Bypass

If both active and passive LD are unavailable, emergency bypass activates:

1. GE suspends the affected locus (no new intents routed to it).
2. In-flight leaf intents continue at PE level (PEs operate independently for active intents).
3. All PROPOSED intents are frozen (no new decompositions).
4. GE re-routes pending cross-locus intents to other loci with available capacity.
5. System 4 is notified for capacity planning.
6. When a new LD comes online, it rebuilds state from ISR snapshot + PE status queries.

---

## 11. Integration Contracts

RIF is a coordination layer, not a self-contained system. It delegates scheduling to C3, provenance carriage to the native communication stack, credibility to C5, knowledge metabolism to C6, and settlement accounting to C8 DSF. This section specifies the bidirectional contracts that make those delegations precise.

### 11.1 RIF <-> C3 Tidal Noosphere

#### 11.1.1 What C3 Provides to RIF

| Capability | Interface | Timing |
|---|---|---|
| Locus topology | `c3.get_topology(locus_id) -> Topology` | Refreshed every epoch |
| Epoch boundaries | `c3.on_epoch_boundary(callback)` -- event-driven | Real-time |
| Operation scheduling | `c3.schedule_operation(op, agent, parcel, deadline, priority)` | Synchronous within epoch |
| G-class consensus | `c3.g_class_vote(topic, package, quorum, timeout) -> VoteResult` | Bounded by timeout |
| VRF outputs | `c3.get_vrf_output(epoch, seed) -> VRFOutput` | Per-epoch, deterministic |
| CRDT replication | `c3.crdt_replicate(data, target_loci)` | Async, convergent |

#### 11.1.2 What RIF Provides to C3

| Capability | Interface | Timing |
|---|---|---|
| Leaf intent execution | PE submits via `c3.schedule_operation()` | Per-intent |
| Governance proposals | Packaged as G-class vote topics | As-needed |

#### 11.1.3 Timing Constraints

- **Epoch alignment:** RIF must complete all intent lifecycle transitions before epoch boundaries. An intent must be in a stable lifecycle state (PROPOSED, DECOMPOSED, ACTIVE, COMPLETED, or DISSOLVED) at every epoch boundary.
- **Scheduling deadline:** Leaf intents must be submitted at least 1 epoch before their `deadline_epoch` to allow C3 scheduling headroom.
- **Temporal hierarchy alignment:** RIF operations align to the three-tier temporal hierarchy defined by C9: SETTLEMENT_TICK (60s), TIDAL_EPOCH (3600s), and CONSOLIDATION_CYCLE (36000s). Intent lifecycle transitions occur on SETTLEMENT_TICK boundaries. Sovereignty relaxation leases are measured in TIDAL_EPOCH units. System 4 horizon scanning operates on CONSOLIDATION_CYCLE timescales.

#### 11.1.4 Message Types

```
RIF -> C3:
  ScheduleOperationRequest { intent_id, operation_class, agent_id,
    parcel_id, resource_allocation, deadline_epoch, priority,
    input_parcel_refs, output_parcel_target }
  GovernanceVoteRequest { topic, package, quorum_threshold, timeout_epochs }

C3 -> RIF:
  EpochBoundaryEvent { epoch, start_ms, duration_ms, tidal_phase }
  OperationResult { execution_id, intent_id, status, output_parcel_ids,
    resource_consumed }
  VoteResult { topic, outcome, votes_for, votes_against,
    total_eligible, compromise_changes }
```

### 11.2 RIF <-> Native Communication Stack

#### 11.2.1 Intent Encoding in Native Sovereign Objects

RIF intent outcomes are expressed as native sovereign claim objects via the canonical `INTENT_OUTCOME` semantic object:

```json
{
  "object_type": "INTENT_OUTCOME",
  "description": "Intent outcome claim",
  "fields": {
    "intent_id":                     { "type": "string", "format": "uuid" },
    "intent_type":                   { "enum": ["GOAL","DIRECTIVE","QUERY","OPTIMIZATION"] },
    "operation_class":               { "enum": ["M","B","X","V","G", null] },
    "outcome":                       { "enum": ["SUCCESS","PARTIAL_SUCCESS","FAILURE","TIMEOUT"] },
    "success_criteria_evaluation":   { "type": "object", "additionalProperties": { "type": "boolean" } },
    "resource_consumed":             { "$ref": "#/$defs/ResourceBounds" },
    "executing_agent_id":            { "type": "string" },
    "parent_intent_id":              { "type": ["string", "null"] },
    "output_parcel_ids":             { "type": "array", "items": { "type": "string" } },
    "completion_epoch":              { "type": "integer" }
  },
  "evidence_requirements": {
    "min_confidence": 0.7,
    "requires_verification": true,
    "verification_class": "V"
  }
}
```

#### 11.2.2 Provenance Chain Integration

Every intent's provenance chain is a sequence of native sovereign claim object IDs, forming an immutable audit trail:

```
Intent Provenance Chain:
  claim_0: Intent proposal     (who proposed, when, justification)
  claim_1: Decomposition       (strategy selected, children produced)
  claim_2: Agent assignment    (which agent, capability match score)
  claim_3: Execution result    (outcome, evidence)
  claim_4: Verification        (if V-class verification performed)
  claim_5: Settlement record   (resource accounting)
```

Each claim references the previous via `prior_claim_id`, and the full chain is verifiable through the native lineage verification interface.

### 11.3 RIF <-> C5 PCVM

#### 11.3.1 Intent Admission Verification

C5 PCVM provides credibility assessments that RIF uses for agent selection (min 0.5 score, S5.1), sentinel selection for the Failure Detector (min sentinel credibility, S3.5), Byzantine detection (credibility drops flag agents for exclusion), and intent outcome verification (credibility-weighted reporting).

#### 11.3.2 Interface Contracts

```
RIF reads from C5:
  pcvm.get_agent_credibility(agent_id) -> {
    composite_score, vtd_count, mct_score, last_update_epoch }
  pcvm.get_claim_class_assessment(claim_id) -> {
    assessed_class, confidence, assessor_count }

RIF writes to C5:
  pcvm.submit_byzantine_evidence(agent_id, evidence) -> {
    evidence_id, accepted }
  pcvm.request_verification(intent_id, claim_id) -> {
    verification_request_id, estimated_completion_epoch }
```

#### 11.3.3 Sovereignty Boundary

The sovereignty boundary between RIF and C5 is precise: RIF may *read* PCVM scores but cannot *set* them. RIF may *submit* evidence but cannot *adjudicate* it -- C5 performs its own assessment. The PCVM classification taxonomy (VTD structure, MCT computation) is constitutional invariant C-01/C-02. C5 credibility updates propagate asynchronously; RIF tolerates staleness up to 5 epochs.

### 11.4 RIF <-> C6 EMA

#### 11.4.1 Read-Only Projections

RIF's relationship with C6 EMA is strictly read-only. System 4 reads EMA projections for horizon scanning and anticipatory capacity planning:

```
RIF reads from C6:
  ema.get_projections(locus_id, window_epochs) -> List[Projection]
  ema.get_coherence_trend(locus_id, window_epochs) -> CoherenceTrend
  ema.get_shrec_state(locus_id) -> SHRECState
  ema.get_metabolic_phase(locus_id) -> MetabolicPhase
```

#### 11.4.2 Staleness Metadata and Discounting

All EMA responses include staleness metadata. System 4 applies a multiplicative confidence discount:

```
confidence_discount = 1.0 / (1.0 + 0.1 * staleness_epochs)

  staleness=0:   discount = 1.00  (fresh)
  staleness=5:   discount = 0.67
  staleness=10:  discount = 0.50
  staleness=20:  discount = 0.33
```

This discount propagates through all System 4 confidence calculations (S4.2.4), ensuring that stale data automatically receives less weight in strategic decisions.

#### 11.4.3 Metabolic Phase Coordination

RIF intent scheduling respects C6 metabolic phases:

| Phase | RIF Behavior |
|---|---|
| ANABOLISM (growth) | Favor GOAL/QUERY intents; boost decomposition budgets by 1.5x |
| CATABOLISM (pruning) | Favor OPTIMIZATION intents; reduce decomposition depth limits by 2 |
| HOMEOSTASIS (stable) | Balanced operation; standard resource allocation |

This coordination ensures that RIF's intent processing aligns with the broader epistemic metabolism of the system, avoiding situations where RIF aggressively decomposes knowledge-producing goals during a catabolism phase when the system is actively pruning.

### 11.5 RIF <-> C8 DSF (Settlement Plane)

> **v2.0 correction (E-C7-01):** All settlement operations route to the C8 Distributed Settlement Fabric, not to C3 internal settlement mechanisms. C3's CRDT replication infrastructure provides the transport layer, but C8 DSF is the canonical settlement authority.

#### 11.5.1 What C8 DSF Provides to RIF

| Capability | Interface | Timing |
|---|---|---|
| Settlement ledger partition | Per-locus settlement partition | Persistent |
| Idempotency enforcement | `dsf.settle(msg) -> {ACCEPTED, DUPLICATE, REJECTED}` | At-least-once, async |
| Settlement confirmation | Settlement receipt with canonical timestamp | Async callback |
| Claim class accounting | 9 canonical claim classes (D, C, P, R, E, S, K, H, N) per C9 | Per-settlement |

#### 11.5.2 What RIF Provides to C8 DSF

| Capability | Interface | Timing |
|---|---|---|
| Settlement entries | Settlement Router via `dsf.settle()` (transported via C3 CRDT) | At-least-once |
| Intent cost records | Per-intent cost accounting per S11.5.3 | Per COMPLETED intent |

#### 11.5.3 Intent Cost Accounting

Every intent incurs costs that must be accounted for:

```
Intent Cost Model:
  decomposition_cost = tokens_consumed * TOKEN_RATE
  execution_cost     = resource_consumed * RESOURCE_RATE[type]
  cross_locus_cost   = cross_locus_messages * CROSS_LOCUS_RATE
  verification_cost  = (if V-class) VERIFICATION_FLAT_FEE
  governance_cost    = (if G-class) GOVERNANCE_FLAT_FEE
  total_cost         = sum of all components

Settlement Flow:
  1. Proposing agent pays decomposition_cost at DECOMPOSED transition
  2. Executing agent pays execution_cost at COMPLETED transition
  3. Cross-locus costs split between originating and destination loci
  4. Verification/governance costs borne by requesting level
```

The Settlement Router forwards all intent-related transactions to the C8 DSF settlement ledger atomically (via C3 CRDT infrastructure), using `settlement_id` as idempotency key to guarantee exactly-once accounting.

#### 11.5.4 Settlement Lag Bounds

- **Normal operation:** Settlement messages may lag intent completion by up to 32 epochs.
- **Backpressure:** Under high load, lag may extend to 50 epochs.
- **Invariant:** No intent remains in COMPLETED state without a corresponding C8 DSF settlement entry for more than 50 epochs (enforced by System 5 audit).

### 11.6 Integration Summary

| Subsystem | RIF Reads | RIF Writes | Sovereignty Tier |
|---|---|---|---|
| C3 Tidal Noosphere | Topology, epochs, VRF, CRDT transport | Leaf execution requests, governance votes | Constitutional (scheduling) |
| Native communication stack | Provenance verification | intent outcome objects, provenance entries | Constitutional (immutability) |
| C5 PCVM | Credibility scores, claim assessments | Byzantine evidence, verification requests | Constitutional (taxonomy) |
| C6 EMA | Projections, coherence, metabolic phase | (none -- read-only) | Constitutional (canonical source) |
| C8 DSF | Settlement confirmation, idempotency | Settlement entries (via Settlement Router) | Operational (accounting) |

---

## 12. Intent Admission Control

### 12.1 Gate Architecture

The Intent Admission Gate is a sequential filter pipeline positioned between intent proposers and the ISR. Every intent must pass all six gates in order. Failure at any gate rejects the intent immediately.

```
                       INTENT PROPOSAL
                            |
                            v
                +------------------------+
                |  Gate 1: PROVENANCE    |  Verify origin, signatures, causal stamp
                +----------+-------------+
                            |  PASS
                            v
                +------------------------+
                |  Gate 2: AUTHORIZATION |  Verify proposer authority for scope
                +----------+-------------+
                            |  PASS
                            v
                +------------------------+
                |  Gate 3: SCHEMA        |  Validate IntentQuantum schema
                +----------+-------------+
                            |  PASS
                            v
                +------------------------+
                |  Gate 4: RESOURCE      |  Verify resource bounds are satisfiable
                +----------+-------------+
                            |  PASS
                            v
                +------------------------+
                |  Gate 5: IMPACT        |  Constitutional check + cross-locus check
                +----------+-------------+
                            |  PASS
                            v
                +------------------------+
                |  Gate 6: RATE LIMIT    |  Per-agent, per-locus rate limiting
                +----------+-------------+
                            |  PASS
                            v
                   ISR.propose_intent()
                   (PROPOSED state)
```

### 12.2 Admission Criteria

**Gate 1 -- Provenance:** Verifies proposer exists in Agent Registry and is ACTIVE, validates Ed25519 signature on CausalStamp, checks CausalStamp epoch is within 2 of current, and verifies provenance chain via native sovereign claim objects.

**Gate 2 -- Authorization:** Verifies agent has capability for the intended operation class, confirms sufficient stake for requested resources, checks scope authorization (cross-locus requires explicit `allow_spanning`), and verifies G-class capability for governance-affecting intents.

**Gate 3 -- Schema:** Validates intent against the IntentQuantum JSON schema (S5.1 -- the single normative schema as unified by v2.0), verifies success criteria are well-formed and machine-evaluable, and confirms resource bounds are non-zero.

**Gate 4 -- Resource Feasibility:** Checks requested resources do not exceed 50% of any target locus capacity, verifies deadline is achievable given estimated minimum epochs, and confirms current system load (PROPOSED queue depth) is below `MAX_PROPOSED_QUEUE_DEPTH` (default: 10,000).

**Gate 5 -- Impact Assessment:** Runs `enforce_constitutional()` to check all constitutional invariants, checks cross-locus ratio against threshold (O-04), and requires System 5 pre-approval for governance-affecting intents.

**Gate 6 -- Rate Limiting:** Per-agent: 100 intents/epoch. Per-locus: 10,000 intents/epoch. High-priority intents (priority > 80) get a 2x fast-track allowance.

### 12.3 Security Properties

The six-gate pipeline provides the following security properties:

1. **Identity assurance:** No intent can enter the system without cryptographic proof of origin (Gate 1).
2. **Capability enforcement:** An agent cannot propose work beyond its authorized capabilities (Gate 2).
3. **Well-formedness:** Malformed intents are caught before consuming decomposition resources (Gate 3).
4. **Resource bounding:** No single intent can monopolize locus capacity (Gate 4).
5. **Constitutional protection:** Intents targeting protected invariants are rejected before admission (Gate 5).
6. **Fairness:** Rate limiting prevents any single agent or locus from flooding the system (Gate 6).

### 12.4 Rejection and Appeal

When an intent fails admission, it is recorded in the ISR as DISSOLVED (it never reaches PROPOSED). A detailed rejection record is created including the gate ID, rejection reason, proposer agent ID, epoch, and whether appeal is permitted.

| Gate | Appeal Mechanism | Conditions |
|---|---|---|
| PROVENANCE | None | Cryptographic failure is absolute |
| AUTHORIZATION | SYSTEM_3_REVIEW | Agent may request capability re-assessment |
| SCHEMA | None | Must be fixed by proposer |
| RESOURCE | SYSTEM_3_REVIEW | Re-submission permitted if conditions change |
| IMPACT | SYSTEM_5_OVERRIDE | Constitutional violations: no appeal. Cross-locus: sovereignty relaxation possible |
| RATE_LIMIT | Automatic | Rate limits reset each epoch; re-submit next epoch |

All rejections are logged immutably and available for System 4 trend analysis (e.g., high rejection rates may signal misconfigured agents or systemic resource exhaustion).

---

## 13. Scalability and Security

### 13.1 Overhead Model

#### 13.1.1 Per-Intent Overhead

```
Per-Intent Cost Breakdown:
  Admission (6 gates):                      ~2ms total
  Decomposition (cached):                   ~50ms typical
  Decomposition (uncached):                 ~500ms typical
  ISR Registration (CRDT per tree node):    ~10ms per node
  Agent Selection (per leaf):               ~1ms per leaf
  Contention Check (per leaf):              ~0.5ms per leaf
  Execution:                                Delegated to C3
  Success Criteria Evaluation:              ~5ms per node
  Settlement (to C8 DSF):                   ~2ms per intent
  GC (deferred, batched):                   ~0.1ms amortized

Typical per-intent total RIF overhead:
  Cached decomposition:    ~71ms
  Uncached decomposition:  ~521ms
```

#### 13.1.2 Per-Epoch Overhead (Per Locus)

```
At 1000 active intents, 100 agents, 10 loci:
  ISR CRDT replication:               ~50KB   (5% network budget)
  Resource Reservation Index sync:    ~10KB   (1% network budget)
  Agent Registry CRDT sync:           ~20KB   (2% network budget)
  Clock Service sync:                 ~1KB    (<1% network budget)
  Failure Detector heartbeats:        ~6KB    (<1% network budget)
  Settlement Router flush (to DSF):   ~10KB   (<1% network budget)
  Performance metrics export:         ~2KB    (fixed)
  Cross-locus capability summary:     ~5KB    (<1% network budget)
  ---------------------------------------------------------------
  Total:                              ~104KB  (~10% of bandwidth)
```

### 13.2 Cross-Locus Bottleneck Analysis

The cross-locus intent ratio is the primary scalability metric:

```
cross_locus_ratio = intents with |target_loci| > 1 / total intents
```

**Threshold:** 20% (operational constraint O-04; relaxable to 40%).

```
At 20% cross-locus (nominal):
  GE processes 200 of 1000 intents/epoch
  HotStuff time: 200 * 15ms = 3s
  At 60s epochs: 5.0% of epoch consumed -> very comfortable

At 40% cross-locus (relaxed maximum):
  GE processes 400 of 1000 intents/epoch
  HotStuff time: 400 * 15ms = 6s
  At 60s epochs: 10.0% of epoch consumed -> comfortable

At >40%:
  System enters degradation mode (S13.3)
```

> **v2.0 note:** HotStuff's O(n) message complexity and ~15ms consensus rounds (vs. classic PBFT's O(n^2) and ~50ms) provide approximately 3x headroom improvement at the GE level compared to v1.0 projections. This headroom is reserved for growth, not consumed by relaxing the cross-locus threshold beyond 40%.

The locality principle ensures sub-linear scaling: if 80%+ of intents are locus-local, adding loci increases total capacity without proportionally increasing GE load. The system scales as O(L) in total throughput but O(1) in per-locus overhead, as long as the locality assumption holds.

### 13.3 Degradation Profiles

#### 13.3.1 Cross-Locus Overload

```
Trigger: cross_locus_ratio > 20% sustained 5 epochs

Sequence:
  1. System 3 activates cross-locus throttle
     - New cross-locus intents queued at reduced priority
     - Local intents unaffected
  2. If ratio > 30% for 3 more epochs:
     - GE rejects low-priority cross-locus intents
     - System 4 proposes agent rebalancing
  3. If ratio > 40% (even with relaxation):
     - GE enters backpressure: max 50 cross-locus intents/epoch
     - Remaining deferred to next epoch
     - System 5 notified for emergency action

Recovery: ratio drops below 15% for 5 consecutive epochs
Hysteresis: prevents oscillation between throttled/normal modes
```

#### 13.3.2 Locus Failure

```
Trigger: LD failover or complete locus loss

Impact:
  Local intents:     All ACTIVE at failed locus are at risk
  Spanning intents:  Children at failed locus timeout after 5 epochs
  GE load:           Unchanged
  Other loci:        Unaffected except for spanning intent timeouts

Sequence:
  1. LD failover activates (target: 1 epoch)
  2. If failover succeeds: reconcile within 2 epochs
  3. If failover fails: emergency bypass (S10.6.3)
  4. If locus down > 50 epochs: all intents DISSOLVED(LOCUS_LOST),
     compensation settlements issued via C8 DSF
```

#### 13.3.3 Network Partition

Three partition types, each with distinct behavior:

- **Single-locus partition:** Isolated locus continues local operations normally. Cross-locus intents involving it timeout at 5 epochs. GE marks locus as PARTITIONED. On heal: ISR reconciliation via Merkle diff.

- **Multi-locus partition:** Each partition group operates independently. GE replicas may diverge between partitions. On heal: HotStuff view change + ISR reconciliation.

- **GE partition:** If majority partition (> 2f+1 replicas): GE continues in majority. If no majority: GE halts, all cross-locus intents freeze. Local operations at all loci continue unaffected. On heal: HotStuff view change + pending operation replay.

#### 13.3.4 Resource Contention Overload

```
Trigger: contention_rate > 20% of leaf assignments sustained 5 epochs

Sequence:
  1. System 3 Performance Monitor alerts System 4
  2. System 4 analyzes contention patterns:
     - Per-agent: specific agents overloaded?
     - Per-domain: specific domains under-provisioned?
     - Per-operation-class: X-class monopolizing agents?
  3. System 4 proposes capacity rebalancing
  4. If contention persists: System 3 increases MAX_CONCURRENT_LEAVES
     (requires Tier 2 relaxation if above default range)

Recovery: contention_rate drops below 10% for 5 consecutive epochs
```

### 13.4 Adversarial Defenses

#### 13.4.1 Intent Injection

A malicious agent submitting intents designed to consume resources, extract information, or disrupt operations faces nine layers of defense:

| Layer | Defense | Mechanism |
|---|---|---|
| Gate 1 | Identity verification | Ed25519 on CausalStamp |
| Gate 2 | Capability + stake | Must hold stake, have capability |
| Gate 4 | Resource cap | Cannot request > 50% locus capacity |
| Gate 5 | Constitutional guard | Cannot target protected invariants |
| Gate 6 | Rate limit | 100/agent/epoch; 10K/locus/epoch |
| Decomposition | Resource preservation | Children cannot exceed parent |
| Execution | C3 sandbox | Resource-bounded execution |
| Post-execution | Failure Detector | 10% sample verification |
| Post-execution | PCVM update | Bad actors lose credibility |

**Worst-case single-agent resource consumption per epoch:** Rate limit of 100 intents, but System 3's resource optimizer prevents single-agent monopoly. Practical maximum: ~30% of locus capacity per agent. The contention protocol (S7.3) further bounds this by limiting each agent to MAX_CONCURRENT_LEAVES (default: 3) simultaneous leaf assignments.

#### 13.4.2 Sovereignty Exploitation

A coalition attempting to permanently weaken constraints faces:

- **Anti-cascade invariant:** Limits concurrent related relaxations to 2.
- **No automatic renewal:** Fresh 90% vote required for each lease.
- **Constitutional hard-coding:** Tier 1 invariants rejected before vote.
- **Bounded relaxation ranges:** Values outside defined range rejected.
- **Supermajority barrier:** Corrupting 90% of G-class agents is extremely expensive.
- **Monitoring independence:** Monitoring function is not a relaxable constraint.

**Formal bound:** Even if ALL 10 Tier 2 constraints are simultaneously relaxed (requiring 10 separate 90% supermajority votes), full reversion occurs within 50 epochs of the last granted lease. Constitutional invariants remain inviolable throughout.

### 13.5 Byzantine Tolerance

#### 13.5.1 GE Level

HotStuff with `3f+1` replicas (default f=1, 4 replicas). Safety: no two honest replicas commit conflicting states -- holds under asynchrony. Liveness: progress guaranteed with `2f+1` honest and reachable replicas and honest leader (under partial synchrony). Leader rotation every tidal epoch prevents long-lived Byzantine leaders. Leader timeout (2 * epoch_duration) triggers automatic view change with O(n) message complexity (no complex view-change sub-protocol as in classic PBFT).

#### 13.5.2 Locus Level

Sentinel-based detection via the Failure Detector. Sentinels are `2 * sentinel_quorum` agents with highest PCVM credibility. Quorum of 3 (default) tolerates 1 Byzantine sentinel. Credibility-weighted voting with 2/3 weighted majority threshold.

#### 13.5.3 Intent Level

Critical intents use V-class verification (separate agent validates result). 10% of completed intents are randomly sampled for outcome verification. Agents with declining PCVM credibility are excluded from assignment. Compensation settlements (routed to C8 DSF) reverse damage from detected Byzantine execution.

### 13.6 Partition Safety Properties

1. **No split-brain decomposition:** LD leadership lock prevents two LDs from decomposing simultaneously.
2. **No split-brain governance:** 90% supermajority means at most one partition can approve governance actions.
3. **No double-spend:** Resource bounds enforced at decomposition by single LD; settlement messages to C8 DSF are idempotent.
4. **Progress in majority partition:** GE majority continues cross-locus processing; minority processes locus-local only.
5. **Convergence on heal:** GE via HotStuff view change; ISR via Merkle-diff CRDT; Agent Registry via CRDT convergence; Clock Service via vector clock merge; Settlement Router via idempotent replay to C8 DSF.

---

## 14. Deployment Roadmap

### 14.1 Phase 1: Bootstrap (1-100 Agents)

```
+=========================================================+
|                    PHASE 1: BOOTSTRAP                    |
|                    (1-100 agents)                        |
|                                                          |
|  Single locus, no Global Executive                       |
|                                                          |
|  +-----------------------------------------------------+|
|  |              LOCUS ALPHA (sole locus)                ||
|  |  Locus Decomposer (active only, no passive)         ||
|  |  4 Parcel Executors                                  ||
|  |  Domain State Plane:                                 ||
|  |    Agent Registry (single instance, no CRDT)         ||
|  |    Clock Service (local NTP only)                    ||
|  |    ISR (single instance, no replication)             ||
|  |    Settlement Router (local, to C8 DSF)              ||
|  |    Failure Detector (1 sentinel)                     ||
|  |  Executive Plane:                                    ||
|  |    System 3 (full decomposition engine)              ||
|  |    System 4 (monitoring only, no EMA integration)    ||
|  |    System 5 (simple majority, no BFT)                ||
|  +-----------------------------------------------------+|
+=========================================================+

Configuration:
  GE:                     DISABLED
  LD replication:         NONE
  ISR replication:        NONE
  BFT:                    DISABLED
  Sovereignty relaxation: Simple majority (>50%)
  Settlement target:      C8 DSF (single partition)
```

**Activation criteria for Phase 2:** Agent count exceeds 100, OR single-locus utilization exceeds 80% sustained for 50 epochs, OR System 4 projects growth rate > 10 agents/epoch.

### 14.2 Phase 2: Multi-Locus (100-1,000 Agents)

```
+=========================================================================+
|                      PHASE 2: MULTI-LOCUS                               |
|  +-------------------------------------------------------------------+ |
|  |  GLOBAL EXECUTIVE (4 replicas, f=1 HotStuff)                      | |
|  +----+----------------------------+-----------------------------+---+ |
|       |                            |                             |     |
|  +----+-------+            +-------+------+           +----------+-+  |
|  | LOCUS ALPHA |            | LOCUS BETA   |           | LOCUS GAMMA| |
|  | LD (A/P)    |            | LD (A/P)     |           | LD (A/P)   | |
|  | 4-8 PEs     |            | 4-8 PEs      |           | 4-8 PEs    | |
|  | Full Domain |            | Full Domain  |           | Full Domain| |
|  | State Plane |            | State Plane  |           | State Plane| |
|  +-------------+            +--------------+           +------------+ |
+=========================================================================+

New capabilities:
  - Cross-locus intent routing via GE (HotStuff consensus)
  - SpanningIntentStub replication
  - System 4 EMA integration (read-only)
  - Full Failure Detector with sentinel quorum (3)
  - ISR CRDT (intra-locus full, cross-locus stubs)
  - Resource Reservation Index with contention protocol
  - 90% supermajority sovereignty relaxation
  - C8 DSF multi-partition settlement

Locus Splitting Protocol:
  1. System 4 proposes split when locus > 200 agents or > 80% utilization
  2. System 3 identifies parcel partition point
  3. New locus bootstrapped with subset of parcels and agents
  4. ISR entries migrated; Agent Registry updated; GE routing table updated
  5. Resource Reservation Index rebuilt from migrated ISR state
```

**Activation criteria for Phase 3:** Total agents exceed 1,000, OR locus count exceeds 10, OR GE throughput exceeds 80% sustained for 50 epochs.

### 14.3 Phase 3: Full Hierarchy (1,000-10,000 Agents)

```
Configuration:
  Loci:                   10-50
  GE:                     7 replicas (f=2), geo-distributed, HotStuff
  LD replication:         Active-Passive with warm standby
  ISR:                    CRDT + Merkle audit every 5 epochs
  Failure Detector:       Quorum 5
  BFT:                    GE f=2 (HotStuff), FD f=1 per locus

Performance Targets:
  Intent admission:            < 5ms p99
  Decomposition (cached):     < 100ms p99
  Decomposition (uncached):   < 1s p99
  Cross-locus routing:        < 200ms p99 (HotStuff: ~15ms consensus)
  Failover:                   < 1 epoch
  ISR CRDT convergence:       < 2 epochs intra-locus
  Settlement lag (C8 DSF):    < 5 epochs p99

New capabilities:
  - Hierarchical locus grouping (region -> locus -> parcel)
  - GE leader geo-affinity (HotStuff round-robin with region weighting)
  - Cross-region latency-aware routing
  - Decomposition memoization sharing across loci (read-only)
  - Advanced Failure Detector: cross-locus Byzantine detection
  - Contention analytics: System 4 trend analysis on resource contention
```

**Activation criteria for Phase 4:** Total agents exceed 10,000, OR locus count exceeds 50, OR cross-region traffic exceeds 30% sustained.

### 14.4 Phase 4: Planetary Scale (10,000-100,000 Agents) -- Aspirational

```
+=========================================================================+
|  FEDERATED GLOBAL EXECUTIVE                                             |
|  5-10 regional GE instances, each 7 replicas (f=2), HotStuff           |
|  Cross-region: federated consensus (1 representative per region)        |
+---+----------+----------+----------+----------+------------------------+
    |          |          |          |          |
 Region A   Region B   Region C   Region D   Region E
 10-20 loci 10-20 loci 10-20 loci 10-20 loci 10-20 loci
+=========================================================================+

Architectural Changes:
  1. Federated GE (regional HotStuff + cross-region federation)
  2. Hierarchical ISR (parcel/locus/region tiers)
  3. Tiered decomposition cache (L1 local, L2 regional, L3 global)
  4. Adaptive epoch duration (30-120s based on load)
  5. Gossip-based capability discovery (O(L*logL) vs O(L^2))

Estimated Parameters:
  Total loci:            50-100
  Total agents:          10K-100K
  Regions:               5-10
  Intents per epoch:     100K-1M
  Cross-region ratio:    Target < 5%
  ISR storage per locus: ~1GB
  Network overhead:      < 10% of locus bandwidth
```

### 14.5 Hard Gate Experiment Designs

Before progressing from SPECIFICATION to full implementation, four hard gates must be cleared:

**Gate 1: Decomposition Algebra Verification.** TLA+ and Alloy models must prove termination (P1), cycle-freedom (P2), resource bound preservation (P3), and operation class monotonicity (P4). Target state space: up to max_depth=20, branching=10 in TLA+; up to 20 intents in Alloy.

**Gate 2: Locality Ratio Validation.** Simulation across four workload profiles (Steady, Bursty, Skewed, Migration) must demonstrate cross-locus ratio < 20% at p95 under steady workload and < 30% under burst. GE throughput must remain below 80% utilization. Simulation must use HotStuff consensus timing (~15ms/round, O(n) messages) rather than generic BFT assumptions.

**Gate 3: Sovereignty Relaxation Safety.** Formal verification (TLA+ or SPIN) must prove bounded relaxation duration (S1), constitutional inviolability (S2), anti-cascade bound (S3), and reversion completeness (S4). Adversarial simulation must show that 89% collusion fails to pass the 90% supermajority threshold.

**Gate 4: Locus Failover Latency.** Fault injection across six scenarios (clean crash, crash during decomposition, crash during settlement, double failure, Byzantine LD, partition during failover) must demonstrate total failover time < 1 epoch for clean crash, zero intent loss, zero duplicates, exact settlement balance (verified against C8 DSF), and zero split-brain occurrences. Contention protocol behavior during failover must be verified: queued assignments must survive or be properly dissolved.

### 14.6 Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Cross-locus ratio exceeds 20% | Medium | High | Monitoring flag; agent rebalancing; sovereignty relaxation to 40% |
| Decomposition depth explosion | Low | High | Hard max_depth=20 (constitutional); decomposition budget (time+compute) |
| System 3/4 oscillation | Medium | Medium | Cool-down (5 epochs); similarity detection; 3 stable epochs gate |
| Locus failure cascade | Low | Critical | Active-passive LD; emergency bypass; GE rerouting |
| Byzantine coalition | Very Low | Critical | 90% supermajority; PCVM credibility; two-layer enforcement |
| EMA projection staleness | Medium | Low | Staleness metadata; confidence discounting; volatility awareness |
| Resource contention deadlock | Low | Medium | Backpressure protocol; queue expiry; System 4 capacity analysis |
| C8 DSF settlement lag | Low | Medium | At-least-once delivery; idempotency keys; System 5 audit |

### 14.7 Phase Transition Summary

```
+--------+--------+------+----------+--------+--------+----------+-----------+
| Phase  | Agents | Loci | GE       | LD     | ISR    | BFT      | Sov.      |
|        |        |      |          | Repl.  | Repl.  |          | Relax.    |
+--------+--------+------+----------+--------+--------+----------+-----------+
| 1      | 1-100  | 1    | OFF      | None   | None   | OFF      | >50%      |
| 2      | 100-1K | 2-10 | 4rep     | A/P    | CRDT   | HotStuff | 90% super |
|        |        |      | HotStuff |        |        | GE f=1   |           |
| 3      | 1K-10K | 10-50| 7rep     | A/P+   | CRDT+  | HotStuff | Full      |
|        |        |      | HotStuff | warm   | Merkle | GE f=2   | protocol  |
|        |        |      |          |        |        | FD f=1   |           |
| 4*     | 10K+   | 50+  | Fed      | A/P+   | 3-tier | HotStuff | Federated |
|        |        |      | 5-10 reg | cross- | hier.  | Reg f=2  |           |
|        |        |      | HotStuff | region |        | + fed    |           |
+--------+--------+------+----------+--------+--------+----------+-----------+
* Phase 4 is aspirational; open research questions remain (S15.2).
```

---

## 15. Conclusion

### 15.1 Summary of Contributions

The Recursive Intent Fabric introduces seven architectural contributions to the Atrahasis agent system:

**1. Intent Quantum as First-Class Object.** By elevating intents from ephemeral messages to persistent, typed objects with a 5-state lifecycle, RIF makes goals, their decomposition, their execution, and their outcomes all first-class citizens of the system. This enables provenance tracking, resource accounting, and formal reasoning about system behavior -- none of which are possible with message-passing orchestration.

**2. Formal Decomposition Algebra.** The operation-class-aware decomposition rules (G->any, V->M/B/X, X->M/B, B->M, M->terminal) with monotonic descent, bounded depth, and resource preservation provide mathematically grounded termination guarantees. This is not a soft claim -- it is verifiable via TLA+ and Alloy model checking.

**3. Two-Plane Separation.** By separating domain-scoped infrastructure (replicated per-locus) from executive functions (spanning loci as needed), RIF achieves the critical property that most work is local. The Domain-Scoped State Plane keeps agent registries, intent states, resource reservations, and settlement routing close to where work happens. The Executive Plane (Systems 3/4/5) provides operational control, strategic intelligence, and governance without centralized bottlenecks.

**4. Graduated Sovereignty.** The three-tier sovereignty model resolves the fundamental paradox between subsystem autonomy and orchestration effectiveness. Constitutional invariants are absolutely inviolable. Operational constraints are temporarily relaxable via governance supermajority with bounded leases and automatic reversion. Coordination parameters are advisory. This is more nuanced and more rigorous than either absolute sovereignty or absolute override.

**5. VSM-Aligned Executive.** Mapping System 3 (operational), System 4 (strategic), and System 5 (governance) onto Stafford Beer's Viable System Model provides a theoretically grounded framework for managing the inherent tension between operational efficiency and strategic adaptation. The oscillation dampening mechanisms (cool-down, similarity detection, stability gating) prevent the System 3/4 feedback loop from becoming unstable.

**6. Substrate-Aware Integration.** RIF does not reinvent what the Atrahasis subsystems already provide. It delegates scheduling to C3, provenance to the native communication stack, credibility to C5, knowledge metabolism to C6, and settlement to C8 DSF -- with precisely defined integration contracts, sovereignty boundaries, and staleness handling. This makes RIF a *coordination layer*, not a replacement for any existing subsystem.

**7. Shared Resource Contention Protocol.** The detection, resolution, and backpressure mechanisms (S7.3) provide formal guarantees against resource contention deadlocks. Priority ordering by operation class rank, deadline, and deterministic tie-breaking ensures that high-value work always progresses, while the assignment queue with bounded expiry prevents indefinite starvation.

### 15.2 Open Research Questions

Several questions remain open for future investigation:

**Q1: Federated GE Consensus Latency.** Can the federated Global Executive (Phase 4) maintain safety properties with cross-region latency exceeding one epoch? HotStuff's partial synchrony model (safety under asynchrony, liveness after GST) provides stronger guarantees than classic PBFT, but planetary-scale deployment may require adaptive timeout tuning that interacts with the leader rotation schedule.

**Q2: Optimal Region Sizing.** What is the optimal number of loci per region for balancing locality (keeping intents within a region) against load distribution (spreading work across regions)? This is likely workload-dependent and may require adaptive region boundaries.

**Q3: Adaptive Epoch Interaction.** How does adaptive epoch duration (Phase 4) interact with C3's tidal scheduling, which assumes fixed epoch boundaries? Variable epoch lengths may create synchronization challenges at the RIF-C3 boundary. The three-tier temporal hierarchy (SETTLEMENT_TICK / TIDAL_EPOCH / CONSOLIDATION_CYCLE) defined by C9 provides fixed anchor points that may constrain adaptation ranges.

**Q4: Cross-Region Cache Coherence.** Can decomposition memoization sharing across regions violate locality assumptions in the decomposition algebra? If a cached decomposition plan references agents that exist only in the originating region, the plan may be invalid in the consuming region.

**Q5: Empirical Locality Validation.** The 80% locality assumption (< 20% cross-locus intents) is theoretically motivated but empirically unvalidated. Real workload characterization studies are needed to confirm or refine this target.

**Q6: Compensation Protocol Completeness.** The saga-style compensation protocols for partial decomposition failure require formal verification that compensation actions themselves cannot fail in ways that leave the system in an inconsistent state.

**Q7: Long-Term Sovereignty Dynamics.** While individual sovereignty relaxations are proven bounded, the long-term statistical dynamics of repeated relaxation-reversion cycles have not been analyzed. Could the system develop "relaxation habits" that, while individually safe, collectively shift its operating point?

**Q8: Contention Protocol Fairness Under Adversarial Load.** The deterministic hash-based tie-breaking in the contention resolution protocol is fair in expectation but could be exploited by an adversary who can choose intent IDs. Analysis is needed on whether VRF-based tie-breaking would provide stronger fairness guarantees without introducing additional complexity.

### 15.3 Relationship to Broader Atrahasis Vision

RIF occupies a specific niche in the Atrahasis architecture: it is the *intent translation layer* that converts high-level goals into concrete, schedulable, accountable work assignments. It sits between the human-facing goal specification interface (above RIF) and the substrate systems that actually execute work (below RIF).

The broader Atrahasis vision -- planetary-scale AI coordination with formal governance -- requires all layers to function in concert: C3 provides the tidal scheduling substrate, the Alternative C stack provides native semantic and provenance contracts, C5 provides credibility assessment, C6 provides epistemic metabolism, RIF (C7) provides the recursive intent orchestration that ties them together, and C8 DSF provides the settlement accounting that closes the economic loop. The remaining inventions in the pipeline will address the layers above and below RIF, completing the full stack.

RIF's graduated sovereignty model, in particular, establishes a pattern that may generalize beyond intent orchestration. Any system that must coordinate autonomous subsystems faces the sovereignty deadlock. The three-tier approach -- immutable constitution, governance-relaxable operations, advisory coordination -- offers a principled resolution that other Atrahasis components may adopt.

---

## Appendix A: Complete Intent Quantum JSON Schema (Non-Normative Reference)

> **v2.0 note:** The single normative IntentQuantum JSON Schema is defined inline in Section 5.1. This appendix is retained as a non-normative quick reference. In case of any discrepancy between this appendix and Section 5.1, Section 5.1 is authoritative.

The normative schema in Section 5.1 resolves all 37 field-level conflicts identified during the v1.0 review (see Appendix H, entry PA-1/F47). Key resolution decisions:

1. **Title:** `"IntentQuantum"` (PascalCase, matching type name in pseudocode).
2. **ID format:** 256-bit hex (`^[0-9a-f]{64}$`), not UUID.
3. **Both `description` and `content`** retained as separate fields.
4. **Scope fields:** All four boolean flags (`requires_exclusive_access`, `is_bounded_local`, `affects_governance`, `requires_verification`) retained from the structured schema.
5. **CausalStamp:** Unified with all six fields (`wall_time_ms`, `vector_clock`, `epoch`, `locus_id`, `agent_id`, `signature`).
6. **Success criteria:** Merged structured predicates (observable, operator, expected_value) with expression override and weight/required flags.
7. **Compensation strategy:** Unified 7-value enum combining both original enum sets.
8. **Resource bounds:** Uses `bandwidth_bytes` (not `network_bytes`), retains `iops`.
9. **Constraints:** Uses `decomposition_token_limit` (not `decomposition_budget_tokens`), three required fields.
10. **Required top-level fields:** `["intent_id", "intent_type", "origin", "scope", "description", "success_criteria", "resource_bounds", "constraints", "output_spec", "lifecycle_state"]`.

---

## Appendix B: Decomposition Algebra Formal Rules

| Parent Class | Permitted Child Classes | Terminal? | Notes |
|---|---|---|---|
| G (Governance) | G, V, X, B, M | No | May produce any class; only class that can produce G children |
| V (Verification) | M, B, X | No | Cannot produce G or V children |
| X (Exclusive) | M, B | No | Cannot produce V, X, or G children |
| B (Bounded) | M | No | Can only produce terminal M children |
| M (Merge) | -- | Yes | Terminal; cannot be decomposed further |

**Class rank ordering:** G(4) > V(3) > X(2) > B(1) > M(0)

**Monotonicity rule:** For every parent-child pair, `ClassRank(child) <= ClassRank(parent)`. If `ClassRank(child) == ClassRank(parent)`, then `depth(child) > depth(parent)` (strict depth increase ensures progress).

**Termination guarantees:**
1. `max_depth` hard cap (constitutional invariant C-04, maximum 20).
2. `decomposition_budget` (wall-clock ms + compute tokens) limits decomposition time.
3. Monotonic class descent ensures finite decomposition paths.

**Resource preservation rule:** For any intent `i` with children `{c_1, ..., c_n}`:
```
sum(c_j.resource_bounds.compute_tokens for j in 1..n) + decomposition_overhead
    <= i.resource_bounds.compute_tokens

sum(c_j.resource_bounds.wall_time_ms for j in 1..n) + decomposition_overhead
    <= i.resource_bounds.wall_time_ms
```

Unused resource margins are returned to the parent upon child completion.

---

## Appendix C: Sovereignty Invariant Catalog

### C.1 Constitutional Invariants (Tier 1)

| ID | Invariant | Enforcement | Cross-Ref |
|---|---|---|---|
| C-01 | PCVM Classification Integrity | System 5 audit + ISR reject | C5 S3.1 |
| C-02 | VTD Immutability | Admission Gate + ISR reject | C5 S4.2 |
| C-03 | EMA Canonical Source | Read-only interface by construction | C6 S2.1 |
| C-04 | Decomposition Termination | Hard-coded depth guard (max 20) | S6.2 |
| C-05 | Operation Class Monotonicity | System 3 assertion | S6.1 |
| C-06 | Resource Bound Integrity | System 3 validation | S6.4 |
| C-07 | Provenance Chain Completeness | ISR rejects without CausalStamp | S3.2 |
| C-08 | Settlement Completeness | Settlement Router ALO guarantee (to C8 DSF) | S3.4 |

### C.2 Operational Constraints (Tier 2)

| ID | Constraint | Default | Relaxation Range | Max Lease |
|---|---|---|---|---|
| O-01 | VRF Composition | Standard | Expanded sets | 50 epochs |
| O-02 | Metabolic Timing | C6 default | 0.5x - 2x | 50 epochs |
| O-03 | SHREC Ratios | C6 default | +/-20% | 50 epochs |
| O-04 | Cross-Locus Threshold | 20% | 20-40% | 50 epochs |
| O-05 | Decomp Depth Soft Limit | 10 | 10-15 | 50 epochs |
| O-06 | Memo Cache TTL | 50 epochs | 50-100 | 50 epochs |
| O-07 | Credibility Floor | 0.5 | 0.3-0.5 | 50 epochs |
| O-08 | Settlement Retry | 10 | 10-20 | 50 epochs |
| O-09 | FD Quorum | 3 | 2-3 | 50 epochs |
| O-10 | ISR Bandwidth Cap | 5% | 5-8% | 50 epochs |

### C.3 Coordination Parameters (Tier 3)

| ID | Parameter | Default | Override By |
|---|---|---|---|
| A-01 | Agent Workload Preferences | Agent-declared | System 3 |
| A-02 | Preferred Decomposition Strategy | Intent-declared | System 3 |
| A-03 | Locus Affinity Hints | Agent-declared | System 3 |
| A-04 | Priority Boost Requests | Proposer-declared | System 3 |
| A-05 | Output Format Preferences | Intent-declared | PE |
| A-06 | Monitoring Verbosity | Locus-default | System 3 |

---

## Appendix D: Message Type Catalog

### D.1 Cross-Level Messages

| Type | Direction | From | To | Delivery | Purpose |
|---|---|---|---|---|---|
| INTENT_ASSIGNMENT | Down | GE | LD | ALO | Assign spanning intent sub-task |
| INTENT_ASSIGNMENT | Down | LD | PE | ALO | Assign leaf intent to parcel |
| CANCEL_INTENT | Down | GE | LD | ALO | Cancel spanning intent |
| CANCEL_INTENT | Down | LD | PE | ALO | Cancel leaf intent |
| RESOURCE_UPDATE | Down | GE | LD | BE | Updated resource allocation |
| EXECUTION_REPORT | Up | PE | LD | ALO | Leaf execution outcome |
| EXECUTION_REPORT | Up | LD | GE | ALO | Aggregated subtree outcome |
| LOCUS_HEALTH_REPORT | Up | LD | GE | BE | Locus metrics per epoch |
| ESCALATION | Up | LD | GE | ALO | Intent cannot be handled locally |
| ESCALATION | Up | PE | LD | ALO | Execution failure requiring intervention |
| STATUS_QUERY | Lateral | LD | LD | BE | Query spanning intent status |
| STATUS_RESPONSE | Lateral | LD | LD | BE | Return spanning intent state |

### D.2 Integration Messages

| Type | From | To | Delivery | Purpose |
|---|---|---|---|---|
| ScheduleOperationRequest | RIF (PE) | C3 | Sync | Submit leaf to tidal scheduler |
| OperationResult | C3 | RIF (PE) | Callback | Execution outcome |
| EpochBoundaryEvent | C3 | RIF | Event | Epoch transition notification |
| SettlementMessage | RIF (SR) | C8 DSF | ALO | Intent cost accounting (via C3 CRDT) |
| GovernanceVoteRequest | RIF (S5) | C3 | Sync | Submit G-class vote |
| VoteResult | C3 | RIF (S5) | Sync | Vote outcome |
| Intent Outcome Object | RIF | Native communication stack | ALO | Intent outcome provenance |
| CredibilityQuery | RIF | C5 | Sync | Agent credibility lookup |
| ByzantineEvidence | RIF (FD) | C5 | ALO | Report Byzantine behavior |
| ProjectionQuery | RIF (S4) | C6 | Sync | EMA projections read |
| MetabolicPhaseQuery | RIF (S3) | C6 | Sync | Current metabolic state |

*ALO = At-Least-Once, BE = Best-Effort, Sync = Synchronous request-response*

### D.3 Sovereignty Protocol Messages

| Type | From | To | Delivery | Purpose |
|---|---|---|---|---|
| RelaxationRequest | S3/S4 | S5 | ALO | Request Tier 2 relaxation |
| RelaxationVotePackage | S5 | C3 (G-class) | Sync | Submit to governance vote |
| RelaxationOutcome | S5 | S3/S4 | ALO | Vote result + lease (if approved) |
| LeaseExpiry | S5 (monitor) | S3 | ALO | Constraint reverted to original |
| LeaseRevocation | S5 (monitor) | S3 | ALO | Lease revoked early (health/cascade) |

### D.4 Contention Protocol Messages

| Type | From | To | Delivery | Purpose |
|---|---|---|---|---|
| ContentionDetected | ISR | LD | ALO | Resource conflict detected during assignment |
| PreemptionNotice | LD | PE | ALO | Active intent preempted by higher-priority |
| QueueAssignment | LD | ISR | ALO | Intent queued for deferred assignment |
| QueueExpiry | ISR | LD | ALO | Queued intent expired without assignment |
| AssignmentReady | ISR | LD | ALO | Agent capacity freed; queued intent ready |

---

## Appendix E: Parameter Reference

| Parameter | Default | Range | Location | Description |
|---|---|---|---|---|
| MAX_DEPTH_HARD | 20 | Fixed (C-04) | System 3 | Absolute maximum decomposition depth |
| MAX_DEPTH_SOFT | 10 | 10-15 (O-05) | System 3 | Default decomposition depth limit |
| DECOMP_BUDGET_MS | 5000 | 100-60000 | Per-intent | Wall-clock budget for decomposition |
| DECOMP_TOKEN_LIMIT | 10000 | 100-1000000 | Per-intent | Compute token budget for decomposition |
| CROSS_LOCUS_THRESHOLD | 0.20 | 0.20-0.40 (O-04) | GE | Max cross-locus intent ratio |
| AGENT_CREDIBILITY_FLOOR | 0.5 | 0.3-0.5 (O-07) | Agent Registry | Min PCVM score for assignment |
| SENTINEL_QUORUM | 3 | 2-3 (O-09) | Failure Detector | Min sentinels for liveness quorum |
| ISR_BANDWIDTH_CAP | 0.05 | 0.05-0.08 (O-10) | ISR | Max network fraction for replication |
| ISR_GC_TTL_EPOCHS | 100 | 50-200 | ISR | Epochs before DISSOLVED intent GC |
| MEMO_CACHE_TTL | 50 | 50-100 (O-06) | System 3 | Decomposition cache entry lifetime |
| SETTLEMENT_RETRY_MAX | 10 | 10-20 (O-08) | Settlement Router | Max settlement delivery attempts |
| GE_REPLICAS | 4 | 4-70 | GE | HotStuff replica count (3f+1) |
| GE_LEADER_ROTATION | Per epoch | Per epoch | GE | HotStuff round-robin leader rotation |
| GE_LEADER_TIMEOUT | 2 * epoch_duration | 1-4x | GE | Timeout before view change |
| GE_CHECKPOINT_INTERVAL | 50 | 25-100 | GE | Epochs between state checkpoints |
| GE_THROUGHPUT_TARGET | 100 | 50-200 | GE | Cross-locus intents/epoch target |
| GE_THROUGHPUT_HARD | 200 | 100-400 | GE | Backpressure threshold |
| GE_THRESHOLD_SIG | BLS12-381 | Fixed | GE | Threshold signature scheme |
| LD_HEARTBEAT_MISS_THRESHOLD | 3 | 2-5 | Failure Detector | Missed heartbeats before failover |
| LD_STATE_SYNC_INTERVAL | 1 | 1 | LD | Epochs between passive sync |
| LD_SNAPSHOT_INTERVAL | 10 | 5-20 | LD | Epochs between full snapshots |
| RATE_LIMIT_AGENT_EPOCH | 100 | 50-500 | Admission Gate | Max intents per agent per epoch |
| RATE_LIMIT_LOCUS_EPOCH | 10000 | 5000-50000 | Admission Gate | Max intents per locus per epoch |
| MAX_PROPOSED_QUEUE | 10000 | 5000-50000 | ISR | Max PROPOSED intents before overload |
| SOVEREIGNTY_SUPERMAJORITY | 0.90 | Fixed | System 5 | Required vote fraction for relaxation |
| SOVEREIGNTY_LEASE_MAX | 50 | Fixed | System 5 | Max lease duration in epochs |
| MAX_CONCURRENT_RELAXATIONS | 2 | Fixed | System 5 | Anti-cascade cluster limit |
| VOTE_TIMEOUT_EPOCHS | 3 | 2-5 | System 5 | G-class vote timeout |
| S4_COOLDOWN_EPOCHS | 5 | 3-10 | System 4 | Min epochs between S4 proposals |
| S4_STABILITY_GATE | 3 | 2-5 | System 4 | Consecutive stable epochs for adaptation |
| STALENESS_DECAY_RATE | 0.1 | 0.05-0.2 | System 4 | EMA staleness discount coefficient |
| PARTITION_DETECT_EPOCHS | 5 | 3-10 | Clock Service | Epochs without clock advance = partition |
| MESSAGE_TTL_EPOCHS | 10 | 5-32 | Cross-level | Default message expiry |
| MESSAGE_RETRY_MAX_EPOCHS | 32 | 16-64 | Cross-level | Max retry backoff |
| MAX_CONCURRENT_LEAVES | 3 | 2-5 | Agent Registry / ISR | Max concurrent leaf intents per agent |
| QUEUE_EXPIRY_EPOCHS | 2 | 1-5 | ISR | Tidal epochs before queued assignment expires |
| CONTENTION_ALERT_THRESHOLD | 0.20 | 0.10-0.30 | Performance Monitor | Contention rate triggering System 4 alert |
| SETTLEMENT_TICK | 60s | Fixed (C9) | Temporal Hierarchy | Base settlement interval |
| TIDAL_EPOCH | 3600s | Fixed (C9) | Temporal Hierarchy | Tidal scheduling epoch |
| CONSOLIDATION_CYCLE | 36000s | Fixed (C9) | Temporal Hierarchy | Long-term consolidation interval |

---

## Appendix F: Glossary

| Term | Definition |
|---|---|
| Agent | An autonomous computational entity registered in a C3 locus, capable of executing operations |
| Alternative C communication stack | Native sovereign message, security, and semantic authority used for claim carriage and provenance references |
| Backpressure | Mechanism that queues new intent assignments when an agent reaches MAX_CONCURRENT_LEAVES capacity |
| BFT | Byzantine Fault Tolerance; ability to function correctly with up to f malicious participants |
| Bounded (B) | Operation class for bounded local commit operations; near-atomic scope |
| CausalStamp | Cryptographically signed record of wall_time_ms, vector clock, epoch, locus_id, agent_id, and Ed25519 signature attached to every state transition |
| Claim Class | One of 9 canonical classes (D, C, P, R, E, S, K, H, N) defined by C9 for settlement categorization |
| CONSOLIDATION_CYCLE | Third tier of the temporal hierarchy (36000s); long-term consolidation interval defined by C9 |
| Constitutional Invariant | A Tier 1 system property that cannot be modified under any circumstances at runtime |
| Contention | Condition where multiple intents compete for the same shared resource (agent, parcel, or capacity slice) |
| CRDT | Conflict-free Replicated Data Type; data structure that converges across replicas without coordination |
| Decomposition Algebra | The formal rules governing how intents of each operation class may be decomposed into children |
| DISSOLVED | Terminal lifecycle state for intents that were rejected, timed out, or explicitly cancelled |
| DSF | Distributed Settlement Fabric (C8); settlement ledger and accounting infrastructure. Settlement Router forwards to DSF via C3's CRDT replication layer |
| EMA | Epistemic Metabolism Architecture (C6); manages knowledge growth, consolidation, and pruning |
| Epoch | A discrete time interval in C3's tidal scheduling system; the fundamental unit of time in Atrahasis |
| Exclusive (X) | Operation class for single-agent exclusive access operations |
| GE | Global Executive; the top level of the decomposition hierarchy handling cross-locus intents |
| G-class | Governance operation class; requires G-class consensus (via C3) for execution |
| Governance (G) | Operation class for constitutional consensus operations |
| HotStuff | HotStuff BFT consensus protocol (Yin et al., 2019); linear message complexity O(n), pipelined 3-phase commit (PREPARE, PRE-COMMIT, COMMIT), tolerating f Byzantine nodes with 3f+1 replicas. Uses BLS12-381 threshold signatures for O(n)->O(1) verification |
| Intent Quantum | The fundamental unit of work in RIF; a self-describing goal with lifecycle, resources, and provenance |
| ISR | Intent State Registry; locus-local CRDT-replicated registry tracking all intent lifecycle states |
| LD | Locus Decomposer; handles intent decomposition within a single C3 locus |
| Lease | A time-bounded authorization for temporary relaxation of a Tier 2 operational constraint |
| Locus | A logical partition in C3's topology containing agents, parcels, and local infrastructure |
| MCT | Multi-Criteria Trust score computed by C5 PCVM |
| Merge (M) | Terminal operation class for read-only merge/convergence operations |
| Metabolic Phase | One of ANABOLISM, CATABOLISM, or HOMEOSTASIS as defined by C6 EMA |
| Operation Class | One of M (Merge), B (Bounded), X (Exclusive), V (Verification), G (Governance) |
| Parcel | A data unit in C3's storage model; the smallest addressable unit of state |
| PCVM | Proof-Carrying Verifiable Merit (C5); credibility and trust assessment system |
| PE | Parcel Executor; leaf-level component bridging RIF intents with C3 tidal scheduling |
| Provenance | An immutable chain of native sovereign claim objects recording the full history of an intent's lifecycle |
| Resource Reservation Index | ISR extension tracking which resources are reserved by which intents, enabling contention detection |
| RIF | Recursive Intent Fabric (C7); this system |
| SETTLEMENT_TICK | First tier of the temporal hierarchy (60s); base settlement interval defined by C9 |
| Settlement Router | Domain State Plane component that forwards intent cost accounting to C8 DSF's settlement ledger (via C3 CRDT infrastructure) |
| SHREC | Resource allocation mechanism in C6 EMA |
| Sovereignty Relaxation | Temporary, governance-approved modification of a Tier 2 operational constraint |
| SpanningIntentStub | A lightweight reference to a cross-locus intent, stored in remote loci for tracking |
| TIDAL_EPOCH | Second tier of the temporal hierarchy (3600s); tidal scheduling epoch defined by C9 |
| Tidal Noosphere | C3; provides locus topology, epoch scheduling, VRF, and CRDT replication infrastructure |
| Verification (V) | Operation class for cross-agent validation operations |
| VRF | Verifiable Random Function; used for agent selection and committee composition |
| VSM | Viable System Model (Stafford Beer); theoretical foundation for the Executive Plane |
| VTD | Verified Trust Document; append-only credential in C5 PCVM |
| WAL | Write-Ahead Log; used for synchronous LD replication to passive instance |

---

## Appendix G: Test Vectors

### G.1 Simple Locus-Local Decomposition

This test vector traces a GOAL intent through decomposition, execution, and settlement within a single locus.

```
INPUT:
  IntentQuantum {
    intent_id:    "a1b2c3d4...0001"
    intent_type:  GOAL
    content:      "Analyze dataset-42 and produce summary report"
    scope:        { target_loci: ["locus-alpha"], domain: "analytics" }
    origin:       { proposer_agent_id: "agent-007", proposer_locus_id: "locus-alpha" }
    constraints:  { max_depth: 5, decomposition_budget_ms: 3000,
                    decomposition_token_limit: 500 }
    resource_bounds: { compute_tokens: 1000, wall_time_ms: 60000 }
    success_criteria: {
      criteria_type: "PREDICATE",
      predicates: [
        { predicate_id: "p1", observable: "output.report",
          operator: "EXISTS", expected_value: true, required: true },
        { predicate_id: "p2", observable: "output.report.sections",
          operator: "GTE", expected_value: 3, required: true }
      ],
      aggregation: "ALL_REQUIRED"
    }
    lifecycle_state: PROPOSED
  }

ADMISSION (6 gates): ALL PASS
  Gate 1: agent-007 exists, ACTIVE, signature valid, epoch current
  Gate 2: agent-007 has X-class capability in analytics domain
  Gate 3: Schema valid (against S5.1 normative schema)
  Gate 4: 1000 tokens < 50% of locus-alpha capacity (10000)
  Gate 5: No constitutional violation; single locus (no cross-locus check)
  Gate 6: agent-007 at 3 intents this epoch (< 100 limit)

STRATEGY SELECTION (select_strategy):
  Step 0: No explicit strategy (null) -> auto-select
  Step 1: intent_type = GOAL -> goto step_2
  Step 2: criteria aggregation = ALL_REQUIRED, predicates independent -> PARALLEL
  Result: PARALLEL

DECOMPOSITION (by LD-alpha, System 3):
  Depth 0: GOAL -> operation_class derived as X (Exclusive)
    Strategy: PARALLEL (selected by select_strategy)
    Child 1: DIRECTIVE "Load dataset-42"
      operation_class: M (terminal)
      resource_bounds: { compute: 200, wall: 10000 }
    Child 2: DIRECTIVE "Run analysis pipeline on loaded data"
      operation_class: B (Bounded)
      resource_bounds: { compute: 500, wall: 30000 }
    Child 3: DIRECTIVE "Format results as summary report"
      operation_class: M (terminal)
      resource_bounds: { compute: 200, wall: 15000 }
    Decomposition overhead: 100 tokens (total children + overhead = 1000)

  Depth 1: B-class child 2 decomposes further
    Child 2a: DIRECTIVE "Statistical summary"
      operation_class: M (terminal)
      resource_bounds: { compute: 250, wall: 15000 }
    Child 2b: DIRECTIVE "Anomaly detection"
      operation_class: M (terminal)
      resource_bounds: { compute: 200, wall: 12000 }
    Decomposition overhead: 50 tokens

CONTENTION CHECK (per leaf):
  child-01 -> agent-012: detect_contention() -> not contended (0 active)
  child-02a -> agent-003: detect_contention() -> not contended (1 active < 3)
  child-02b -> agent-009: detect_contention() -> not contended (0 active)
  child-03 -> agent-012: detect_contention() -> not contended (1 active < 3)

FINAL INTENT TREE:
  a1b2...0001 (GOAL, X, depth=0)
    +-- child-01 (DIRECTIVE, M, depth=1) "Load dataset-42"
    +-- child-02 (DIRECTIVE, B, depth=1) "Run analysis pipeline"
    |     +-- child-02a (DIRECTIVE, M, depth=2) "Statistical summary"
    |     +-- child-02b (DIRECTIVE, M, depth=2) "Anomaly detection"
    +-- child-03 (DIRECTIVE, M, depth=1) "Format report"

EXECUTION SEQUENCE (parallel strategy):
  Epoch E:    child-01 assigned to PE-3, agent-012 -> COMPLETED (success)
              child-02a assigned to PE-1, agent-003 -> COMPLETED (success)
              child-02b assigned to PE-2, agent-009 -> COMPLETED (success)
  Epoch E+1:  child-02 -> COMPLETED (both children succeeded)
              child-03 assigned to PE-3, agent-012 -> COMPLETED (success)

SUCCESS CRITERIA EVALUATION:
  p1: output.report EXISTS -> TRUE (report produced by child-03)
  p2: output.report.sections GTE 3 -> TRUE (4 sections)
  Aggregation: ALL_REQUIRED -> PASS

LIFECYCLE TRANSITIONS:
  E-1:  PROPOSED -> DECOMPOSED (admission passed, decomposition complete)
  E:    DECOMPOSED -> ACTIVE (all children accepted by executors)
  E+1:  ACTIVE -> COMPLETED (success criteria met)
  E+101: COMPLETED -> (GC after 100 epochs) -> DISSOLVED

SETTLEMENT (to C8 DSF):
  decomposition_cost: 150 tokens * TOKEN_RATE = 0.15 credits
  execution_cost:     850 tokens * RESOURCE_RATE = 0.85 credits
  cross_locus_cost:   0 (single locus)
  total_cost:         1.00 credits, charged to agent-007
  settlement_target:  C8 DSF (via C3 CRDT infrastructure)
```

### G.2 Cross-Locus Spanning Intent

```
INPUT:
  IntentQuantum {
    intent_id:    "a1b2c3d4...0002"
    intent_type:  QUERY
    content:      "Find all references to 'quantum coherence' across all loci"
    scope:        { target_loci: ["locus-alpha", "locus-beta", "locus-gamma"],
                    domain: "search" }
    constraints:  { max_depth: 3, allow_spanning: true,
                    decomposition_budget_ms: 2000,
                    decomposition_token_limit: 300 }
    resource_bounds: { compute_tokens: 3000, wall_time_ms: 120000 }
  }

STRATEGY SELECTION:
  Step 0: No explicit strategy -> auto-select
  Step 1: intent_type = QUERY, count_independent_data_sources = 3 -> PARALLEL

ROUTING (GE via HotStuff):
  Cross-locus intent detected (3 loci)
  HotStuff consensus round: ~15ms, 4 messages (f=1)
  GE decomposes into 3 per-locus sub-intents:
    sub-alpha: { target_loci: ["locus-alpha"], compute: 1000 }
    sub-beta:  { target_loci: ["locus-beta"],  compute: 1000 }
    sub-gamma: { target_loci: ["locus-gamma"], compute: 900 }
    GE overhead: 100 tokens
  SpanningIntentStubs broadcast to all 3 loci

EXECUTION:
  Each sub-intent decomposes locally at its LD into M-class queries
  Contention checks performed per-agent at each LD
  Results propagate: PE -> LD -> GE
  GE aggregates results and evaluates parent success criteria

SETTLEMENT (to C8 DSF):
  cross_locus_cost: 3 messages * CROSS_LOCUS_RATE = 0.03 credits
  (split between locus-alpha as originator and beta/gamma as destinations)
  settlement_target: C8 DSF (via C3 CRDT infrastructure)
```

### G.3 Sovereignty Relaxation Trace

```
TRIGGER: cross_locus_ratio = 0.25 for 5 consecutive epochs (exceeds O-04 = 0.20)

REQUEST:
  System 3 submits SovereigntyRelaxationRequest:
    constraint_id:           "O-04"
    current_value:           0.20
    requested_value:         0.35
    justification:
      trigger_condition:     "Sustained cross-locus ratio above threshold"
      supporting_metrics:    [{ metric: "cross_locus_ratio", current: 0.25,
                                threshold: 0.20, window: 5 }]
      impact_assessment:     "Allow GE to process additional 15% cross-locus traffic"
      risk_if_denied:        "Increasing rejection rate for cross-locus intents"
    requested_lease_epochs:  20
    anti_cascade:            { dependent: ["O-10"], cascade_risk: "LOW" }

PRE-VALIDATION:
  Check 1: O-04 is Tier 2 (not constitutional) -> PASS
  Check 2: 0.35 within relaxation bounds [0.20, 0.40] -> PASS
  Check 3: No active relaxations on O-10 -> cascade count = 0 < 2 -> PASS

G-CLASS VOTE (via HotStuff consensus at GE):
  Eligible voters: 50 G-class agents
  Votes for:       47 (94%)
  Votes against:   3 (6%)
  Supermajority:   94% >= 90% -> PASS

LEASE CREATED:
  relaxation_id:  "rel-001"
  constraint_id:  "O-04"
  original_value: 0.20
  relaxed_value:  0.35
  start_epoch:    1000
  expiry_epoch:   1020
  status:         ACTIVE

MONITORING (every epoch):
  Epoch 1005: cross_locus_ratio = 0.28 -> within relaxed threshold -> OK
  Epoch 1010: cross_locus_ratio = 0.22 -> trending down -> OK
  Epoch 1015: cross_locus_ratio = 0.18 -> below original threshold -> OK
  Epoch 1020: LEASE EXPIRED -> revert O-04 to 0.20
  Epoch 1020+: normal operation resumes at 0.20 threshold
```

### G.4 Contention Resolution Trace

```
SCENARIO: Two intents compete for agent-042

EXISTING STATE:
  agent-042 has 3 active leaf intents (at MAX_CONCURRENT_LEAVES)
  Reservations:
    - intent-A (M-class, priority 50, no deadline)
    - intent-B (B-class, priority 60, deadline epoch 1050)
    - intent-C (M-class, priority 40, no deadline)

NEW INTENT:
  intent-D (X-class, priority 70, deadline epoch 1045)
  Submitted to LD for assignment to agent-042

CONTENTION DETECTION:
  detect_contention(intent-D, "agent-042", AGENT)
  -> concurrent_leaves = 3 >= MAX_CONCURRENT_LEAVES (3)
  -> ContentionResult { contended: true, reason: CAPACITY_OVERLOAD,
                         blocking_intents: [A, B, C] }

CONTENTION RESOLUTION:
  resolve_contention(intent-D, contention, "agent-042")

  Rule 1: Higher operation class wins
    intent-D class rank: X(2)
    intent-A class rank: M(0) -> X > M
    -> PREEMPT intent-A (operation_class X > M)

RESULT:
  ResolutionAction { action: PREEMPT, preempt_intent_id: "intent-A",
                     reason: "operation_class X > M" }

POST-RESOLUTION:
  1. intent-A transitions to DISSOLVED(PREEMPTED)
  2. intent-A's parent notified for compensation
  3. intent-D assigned to agent-042 in freed slot
  4. ResourceReservation created for intent-D
  5. process_assignment_queue("agent-042") runs
     -> queue is empty, no further assignments
```

---

## Appendix H: Changelog (v1.0 to v2.0)

This appendix documents all changes from v1.0 to v2.0 of the C7 RIF Master Technical Specification. Changes are grouped by source.

### H.1 PA-1/F47 -- Dual Schema Conflict Resolution (HIGH)

**Sections affected:** S5.1, Appendix A

37 field-level conflicts between the Section 5.1 schema and the Appendix A schema were resolved. A single normative IntentQuantum JSON schema is now defined inline in Section 5.1. Key resolution decisions include:

| # | Resolution Summary |
|---|---|
| 1 | Title: `"IntentQuantum"` (PascalCase) |
| 2-3 | Both `description` (max 4096, human-readable) and `content` (structured spec) retained |
| 4 | ID format: 256-bit hex pattern, not UUID |
| 5-8 | All scope boolean flags retained from structured schema |
| 9 | `target_loci.minItems: 1` enforced |
| 10-13 | All CausalStamp fields retained (wall_time_ms, vector_clock, epoch, locus_id, agent_id) |
| 14 | Ed25519 `signature` added to CausalStamp |
| 15 | `authorization` (GovernanceToken) added |
| 16 | `decomposition_strategy` nullable with default RECURSIVE |
| 17 | `decomposition_token_limit` name used (not budget_tokens), added to required |
| 18 | `allow_spanning` default: true |
| 19 | Three required constraint fields |
| 20 | `bandwidth_bytes` name used (not network_bytes) |
| 21 | `iops` field retained |
| 22 | Minimums: 1 for compute_tokens/wall_time_ms, 0 for optional |
| 23 | `criteria_type` discriminator retained |
| 24 | Merged structured predicates with expression override + weight/required |
| 25-26 | `thresholds` and `temporal_bound` arrays retained |
| 27-28 | `aggregation` with 3-value enum + threshold field |
| 29-31 | `lifecycle_state`, `parent_intent_id`, `child_intent_ids` added |
| 32 | W3C PROV `provenance` object added |
| 33 | Unified 7-value compensation strategy enum |
| 34-35 | `timeout_epochs` and `compensation_intents` fields |
| 36 | `metadata` with created/modified epochs retained |
| 37 | 10 required top-level fields |

Appendix A redesignated as non-normative reference.

### H.2 PA-2/F48 -- Strategy Selection Algorithm (MEDIUM)

**Sections affected:** S6.5 (or S8.1 in v2.0 structure)

The `select_strategy()` function, previously called but never defined, is now fully specified with:

- 5-step decision process (honor preference, classify by type, structural analysis, resource heuristics, historical lookup, default by class)
- 4 helper functions (`validate_strategy_compatibility`, `has_branching_predicates`, `has_output_chain_dependency`, `estimate_child_count`)
- Updated strategy selection summary table

### H.3 PA-3/F49 -- Operation Class Name Corrections (MEDIUM)

**Sections affected:** Appendix B, Appendix F (Glossary), all inline references

Three canonical name corrections applied throughout the document:

| Code | Incorrect (v1.0) | Correct (v2.0) |
|---|---|---|
| B | "Branch" (in some locations) | "Bounded" (everywhere) |
| X | "Cross-reference" (in some locations) | "Exclusive" (everywhere) |

### H.4 PA-4/F50 -- PBFT to HotStuff BFT (MEDIUM)

**Sections affected:** S10.2, S13.2, S13.3, S13.5, S13.6, S14, Appendix E, Appendix F

All references to "PBFT" as the GE consensus protocol replaced with "HotStuff":

| Change | Detail |
|---|---|
| Consensus protocol | HotStuff (Yin et al., 2019) |
| Message complexity | O(n^2) -> O(n) per round |
| Consensus round time | ~50ms -> ~15ms |
| Messages at f=1 | 16 -> 4 per round |
| Messages at f=2 | 49 -> 7 per round |
| Commit step complexity | O(n^2) -> O(n) |
| Leader rotation | Per tidal epoch, round-robin |
| View change | Simple (HotStuff built-in) vs. complex (PBFT sub-protocol) |
| Threshold signatures | BLS12-381 added |
| Throughput at 20% cross-locus | 10s (PBFT) -> 3s (HotStuff) per epoch |
| Throughput at 40% cross-locus | 20s (PBFT) -> 6s (HotStuff) per epoch |

New pseudocode added: `ge_hotstuff_round()` (3-phase pipeline) and `ge_leader_timeout_handler()`.

### H.5 PA-5/F51 -- Shared Resource Contention Protocol (MEDIUM)

**Sections affected:** S7.3 (new), S10.3.3, S8.1 (agent selection), Appendix D, Appendix E

New contention management subsystem added to the Domain-Scoped State Plane:

| Component | Description |
|---|---|
| ResourceReservation structure | Tracks per-resource reservations with class, priority, deadline |
| Resource Reservation Index | ISR extension mapping resource_id to sorted reservation list |
| `detect_contention()` | Checks for exclusive access conflicts and capacity overload |
| `resolve_contention()` | Priority ordering: operation class > deadline > hash tie-break |
| `apply_backpressure()` | Queues assignments when agent at MAX_CONCURRENT_LEAVES |
| `process_assignment_queue()` | Drains queue on capacity free, handles expiry |
| `select_agent()` (updated) | Contention-aware: prefers agents with available capacity |
| New parameters | MAX_CONCURRENT_LEAVES (3), QUEUE_EXPIRY_EPOCHS (2) |
| New metrics | Contention rate added to Performance Monitor |
| New messages | 5 contention protocol messages added to Appendix D |

### H.6 PA-6/E-C7-01 -- Settlement Router Target Correction (ERRATA)

**Sections affected:** S3.4, S7.4, S8.3, S11.5, S13, S14, Appendix C, Appendix D, Appendix F

Per C9 Cross-Layer Reconciliation erratum E-C7-01:

| Change | Detail |
|---|---|
| Settlement target | "C3 settlement ledger" -> "C8 DSF settlement ledger (via C3 CRDT infrastructure)" |
| Locations corrected | 9 inline references + integration table + glossary |
| New integration section | S11.5 now specifies full RIF <-> C8 DSF contract |
| New glossary entry | DSF (Distributed Settlement Fabric) added |

### H.7 C9 Cross-Layer Reconciliation Integration

**Sections affected:** S11.1.3, Appendix E, Appendix F

Additional C9 material integrated:

| Integration | Detail |
|---|---|
| Three-tier temporal hierarchy | SETTLEMENT_TICK (60s) / TIDAL_EPOCH (3600s) / CONSOLIDATION_CYCLE (36000s) referenced in timing constraints |
| 9 canonical claim classes | D, C, P, R, E, S, K, H, N referenced in C8 DSF integration |
| Temporal parameters | Added to Appendix E parameter reference |
| Glossary entries | SETTLEMENT_TICK, TIDAL_EPOCH, CONSOLIDATION_CYCLE, Claim Class, DSF added |

### H.8 Structural Changes

| Change | Detail |
|---|---|
| Document unification | Part 1 + Part 2 merged into single continuous document |
| Version marking | v1.0 -> v2.0 throughout |
| Date | Updated to 2026-03-10 |
| Table of Contents | Unified; Part 2 ToC removed |
| Appendix A | Redesignated as non-normative reference (points to S5.1) |
| Appendix H | New: this changelog |
| Contribution count | 6 contributions (v1.0) -> 7 contributions (v2.0, adding contention protocol) |
| Open questions | 7 questions (v1.0) -> 8 questions (v2.0, adding contention fairness) |

---

*End of C7 RIF Master Technical Specification v2.0*
