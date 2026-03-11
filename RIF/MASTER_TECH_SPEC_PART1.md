# Recursive Intent Fabric: A Two-Plane Orchestration Architecture for Sovereign AI Coordination at Planetary Scale
## Master Technical Specification — C7-A
## Part 1 of 2 (Sections 1-8)
## Version 1.0

**Invention ID:** C7
**Concept:** C7-A Recursive Intent Fabric (RIF)
**Date:** 2026-03-10
**Status:** SPECIFICATION — Master Tech Spec
**Predecessor Specs:** CIOS (implied, unspecified), C3 Tidal Noosphere, C4 ASV, C5 PCVM, C6 EMA
**Ideation Council Verdict:** SELECTED (4-0, Critic abstains). Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10 (MEDIUM-HIGH)
**Primary Scale Target:** 1,000-10,000 agents (100K+ aspirational, contingent on >=80% locus-local intent ratio)

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

---

## 1. Abstract

The Recursive Intent Fabric (RIF) is a two-plane orchestration architecture that replaces the previously unspecified Coordinated Intent Orchestration System (CIOS) within the Atrahasis agent coordination stack. RIF solves a fundamental paradox in planetary-scale AI coordination: how to provide coherent goal decomposition and resource management across thousands of autonomous agents while respecting the sovereignty guarantees that make those agents trustworthy in the first place.

The architecture separates concerns into a **Domain-Scoped State Plane** — five infrastructure services (Agent Registry, Clock Service, Intent State Registry, Settlement Router, Failure Detector) replicated within each C3 locus using CRDTs and vector clocks — and an **Executive Plane** modeled on Stafford Beer's Viable System Model, comprising System 3 (Operational Control), System 4 (Strategic Intelligence), and System 5 (G-Class Governance). This separation ensures that operational state remains local to where it is needed while strategic and governance functions span loci only when necessary.

RIF introduces the **Intent Quantum** as its fundamental unit of work: a self-describing goal with typed semantics (GOAL, DIRECTIVE, QUERY, OPTIMIZATION), machine-evaluable success criteria, resource bounds, decomposition constraints, and a W3C PROV provenance chain. Intents traverse a five-state lifecycle (PROPOSED, DECOMPOSED, ACTIVE, COMPLETED, DISSOLVED) and decompose recursively through a **formal decomposition algebra** that maps onto C3's five operation classes (M/B/X/V/G). The algebra provides proven termination and cycle-freedom guarantees via a well-founded lexicographic ordering on (operation class rank, remaining depth).

A **graduated sovereignty model** with three tiers — constitutional (inviolable), operational (relaxable by 90% supermajority), and coordination (advisory) — resolves the tension between orchestration effectiveness and subsystem autonomy. System 4's anticipatory planning reads C6 EMA projections in a strictly read-only mode, with oscillation dampening via cool-down timers, similarity detection, and stability gating. System 5 maps directly onto C3's existing G-class governance mechanism, adding no new governance primitives.

The architecture targets 1,000-10,000 agents as its validated design point. Sub-linear scaling is achievable when at least 80% of intents are locus-local; the Global Executive becomes a bottleneck when cross-locus intents exceed 20%. RIF delegates scheduling to C3, settlement to C3's ledger, credibility to C5 PCVM, knowledge metabolism to C6 EMA, and claim management to C4 ASV — it orchestrates without duplicating.

---

## 2. Introduction and Motivation

### 2.1 The Orchestration Problem

Consider a system of ten thousand autonomous AI agents distributed across hundreds of semantic domains, collectively performing verified knowledge work — generating claims, verifying evidence, resolving contradictions, governing their own operational parameters. Each agent is sovereign in the sense that it holds cryptographic identity, staked collateral, and independently verifiable reputation. The subsystems that support this work — tidal scheduling (C3), claim semantics (C4), credibility verification (C5), knowledge metabolism (C6) — are each designed to operate without central direction. They are autonomous by construction, not by accident.

Now ask: how does a high-level goal — "achieve 95% accuracy on climate prediction within 100 epochs" — become concrete work that these agents actually perform?

This is the orchestration problem. It is distinct from scheduling (C3 handles that), from verification (C5 handles that), from knowledge lifecycle management (C6 handles that), and from claim semantics (C4 handles that). Orchestration sits above all four: it translates goals into the language these subsystems understand, decomposes complex objectives into tasks that individual agents can execute within single tidal epochs, manages the lifecycle of those tasks from proposal through completion, and handles the inevitable failures that arise in distributed systems.

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
          |              |            |              |
          v              v            v              v
+================+ +=========+ +==========+ +==================+
| C3 Tidal       | | C4 ASV  | | C5 PCVM  | | C6 EMA           |
| Noosphere      | |         | |          | |                  |
| (scheduling,   | |(claims, | |(VTDs,    | |(epistemic quanta,|
|  loci, parcels,| | evid.,  | | MCTs,    | | metabolic life-  |
|  M/B/X/V/G,   | | prov.)  | | cred.)   | | cycle, SHREC)    |
|  settlement)   | |         | |          | |                  |
+================+ +=========+ +==========+ +==================+
```

RIF's relationship to each substrate is deliberately asymmetric:

- **C3 (Tidal Noosphere)**: RIF's primary substrate. Leaf intents execute as C3 operation-class tasks within tidal epochs. RIF reads locus topology, epoch boundaries, and VRF outputs. RIF writes leaf intent execution requests and settlement entries. C3's scheduling sovereignty is constitutional — RIF cannot override tidal assignment.

- **C4 (ASV)**: RIF uses ASV claim schemas and provenance chains to express intent outcomes as verifiable claims. Every intent state transition carries C4 provenance. RIF writes intent success/failure claims; C4's claim semantics are sovereign.

- **C5 (PCVM)**: RIF reads agent credibility scores to inform assignment decisions and failure detection. The Failure Detector integrates PCVM credibility to weight liveness reports and detect Byzantine agents. PCVM's claim classification is constitutionally sovereign — RIF cannot override VTD or MCT assessments.

- **C6 (EMA)**: System 4 reads EMA epistemic quanta projections in a strictly read-only mode for horizon scanning and anticipatory planning. RIF writes nothing to EMA. EMA's canonical source status and metabolic phase timing are constitutionally and operationally sovereign respectively.

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
|  | - Emergency        |  |   dampening           |  |                   |  |
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
|  +------------------+  +--------+  +----------+  +------------------+  |
|  | C3 Tidal         |  | C4 ASV |  | C5 PCVM  |  | C6 EMA           |  |
|  | Noosphere        |  |        |  |          |  |                  |  |
|  | (loci, parcels,  |  |(claims,|  |(VTDs,    |  |(epistemic quanta,|  |
|  |  tidal sched,    |  | evid., |  | MCTs,    |  | metabolic life-  |  |
|  |  VRF, M/B/X/V/G) |  | prov.) |  | cred.)   |  | cycle, SHREC)    |  |
|  +------------------+  +--------+  +----------+  +------------------+  |
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
| Intent State Registry (ISR) | Domain State | Per-locus (spanning for cross-locus intents) | CRDT with 5% bandwidth cap | C4 provenance |
| Settlement Router | Domain State | Per-locus | At-least-once broker with WAL | C3 settlement ledger |
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

**Principle 4: Substrate Awareness.** RIF does not reinvent scheduling, settlement, credibility, or knowledge metabolism. It delegates to C3, C4, C5, and C6 respectively. This principle prevents RIF from becoming a second, incompatible implementation of functionality that already exists in the substrate. Every leaf intent becomes a C3 operation-class task; every intent outcome becomes a C4 ASV claim; every agent credibility check goes through C5 PCVM; every horizon scan reads C6 EMA projections.

### 4.4 Integration with Substrate Components

The following table specifies exactly what RIF reads from, writes to, and never touches in each substrate component:

| Substrate | RIF Reads | RIF Writes | RIF Never Touches |
|---|---|---|---|
| C3 Tidal Noosphere | Locus topology, parcel state, epoch boundaries, VRF outputs, operation class definitions | Leaf intent execution requests, settlement entries | Tidal scheduling assignments, VRF verifier selection, parcel boundaries |
| C4 ASV | Claim schemas, evidence structures, provenance chains | Intent success/failure claims, decomposition provenance | Claim content, evidence weighting, provenance semantics |
| C5 PCVM | Agent credibility scores (VTDs, MCTs), claim class assessments | Intent outcome verification requests, Byzantine evidence submissions | Claim classification (INV-M2), VTD/MCT values (INV-M7) |
| C6 EMA | Epistemic quanta projections, SHREC regulation state, coherence trends | Nothing (strictly read-only) | Canonical quanta (INV-E1), metabolic phases (INV-E3), SHREC allocations |

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
          complete      C3 ledger     written
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
IQ = (id, type, class, origin, scope, description, criteria, bounds,
      constraints, strategy, inputs, output, metadata)
```

The complete JSON Schema follows. This schema is normative — all RIF implementations must accept and produce intent quanta conforming to this schema.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.org/rif/intent-quantum/v1",
  "title": "RIF Intent Quantum",
  "description": "The fundamental unit of work in the Recursive Intent Fabric",
  "type": "object",
  "properties": {
    "intent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Globally unique 256-bit intent identifier"
    },
    "intent_type": {
      "type": "string",
      "enum": ["GOAL", "DIRECTIVE", "QUERY", "OPTIMIZATION"],
      "description": "Classification of intent purpose"
    },
    "operation_class": {
      "type": ["string", "null"],
      "enum": ["M", "B", "X", "V", "G", null],
      "description": "C3 operation class. Null for non-leaf intents; derived at leaf level."
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
          "description": "C4 ASV claim IDs forming the provenance chain"
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
          "items": { "type": "string" }
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
      "maxLength": 4096
    },
    "success_criteria": {
      "type": "object",
      "properties": {
        "criteria_type": {
          "type": "string",
          "enum": ["PREDICATE", "THRESHOLD", "TEMPORAL", "COMPOSITE"]
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
        "composition": {
          "type": "string",
          "enum": ["AND", "OR"]
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
      "enum": ["RECURSIVE", "PARALLEL", "SEQUENTIAL", "CONDITIONAL", null]
    },
    "input_references": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ref_type": {
            "type": "string",
            "enum": ["PARCEL", "INTENT_OUTPUT", "EMA_QUANTUM",
                     "ASV_CLAIM", "EXTERNAL"]
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
          "enum": ["REVERSE_SETTLEMENT", "RE_DECOMPOSE", "ESCALATE", "NONE"]
        },
        "max_compensation_epochs": { "type": "integer" }
      }
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
               "constraints", "output_spec"],

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
        "agent_id": { "type": "string" }
      },
      "required": ["wall_time_ms", "vector_clock", "epoch",
                    "locus_id", "agent_id"]
    },
    "ResourceBounds": {
      "type": "object",
      "properties": {
        "compute_tokens": {
          "type": "integer", "minimum": 0,
          "description": "Maximum compute tokens (additive resource)"
        },
        "wall_time_ms": {
          "type": "integer", "minimum": 0,
          "description": "Maximum wall-clock time (additive resource)"
        },
        "bandwidth_bytes": {
          "type": "integer", "minimum": 0,
          "description": "Maximum network bandwidth (shared resource)"
        },
        "iops": {
          "type": "integer", "minimum": 0,
          "description": "Maximum I/O operations per second (shared resource)"
        },
        "storage_bytes": {
          "type": "integer", "minimum": 0,
          "description": "Maximum storage consumption (additive resource)"
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
        "observable": { "type": "string" },
        "operator": {
          "type": "string",
          "enum": ["EQ", "NEQ", "GT", "GTE", "LT", "LTE",
                   "CONTAINS", "MATCHES", "EXISTS"]
        },
        "expected_value": {},
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

### 5.2 The Four Intent Types

RIF defines four intent types, each with distinct semantics, decomposition behavior, and operation-class mappings.

#### 5.2.1 GOAL

A GOAL is a high-level objective defined by success criteria rather than execution instructions. Goals are always decomposed — they never appear as leaf intents. If a GOAL reaches leaf level during decomposition, it indicates a failure in the decomposition engine (the goal is too abstract to execute directly).

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
    "composition": "AND"
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

Every intent quantum traverses a five-state lifecycle. The state machine is deliberately minimal — the Ideation Council explicitly rejected proposals for additional states (coherence graphs, consolidation phases, dreaming modes) as overcomplication.

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

Combine sub-criteria using AND/OR composition:

```
Composite := (AND | OR) of [Predicate | Threshold | Temporal | Composite]

Example (AND):
  ALL of:
    - accuracy GTE 0.95
    - latency_p99 LTE 500ms
    - WITHIN_EPOCHS 100

Example (OR):
  ANY of:
    - accuracy GTE 0.98           (high bar, any timeline)
    - accuracy GTE 0.95 AND WITHIN_EPOCHS 50  (lower bar, faster)
```

**Evaluation semantics**: AND requires all sub-criteria to be true simultaneously at evaluation time. OR requires at least one. Temporal bounds are evaluated against the Clock Service's current epoch. Predicates are evaluated against observable system state. Thresholds are evaluated against the most recent metric snapshot. Evaluation is triggered by System 3 when all leaf descendants of an intent tree report results.

### 5.5 Comparison to Traditional Approaches

| Dimension | Traditional Task Queue | Workflow DAG | RIF Intent Quantum |
|---|---|---|---|
| Work item definition | Opaque payload + callback | Step in a predefined graph | Self-describing typed object with success criteria |
| Success evaluation | Binary (complete/fail) | Binary per step; DAG completes when all steps do | Machine-evaluable predicates, thresholds, temporal bounds, composites |
| Decomposition | None (tasks are atomic) | Predefined at authoring time | Dynamic at runtime, governed by formal algebra with termination proof |
| Resource management | Queue depth limits | Per-step resource requests | Formal resource bounds with additive/shared distinction and preservation proof |
| Failure handling | Retry or dead-letter | Retry or compensate (predefined) | Saga-style compensation derived from decomposition structure; partial re-decomposition |
| Provenance | Logging | Logging | W3C PROV chains anchored to C4 ASV claims |
| Lifecycle | Queued, Processing, Done, Failed | Per-step states | PROPOSED, DECOMPOSED, ACTIVE, COMPLETED, DISSOLVED with formal state machine |
| Types | None (generic) | None (generic) | GOAL, DIRECTIVE, QUERY, OPTIMIZATION with distinct semantics |
| Causal ordering | None or timestamp | DAG edges | Vector clocks + NTP with causal stamps on every transition |

The fundamental difference is that a task queue or workflow DAG is a *mechanism* — it moves work from A to B. An intent quantum is a *specification* — it declares what success looks like and lets the system figure out how to achieve it. This declarative nature is what enables dynamic decomposition, partial success evaluation, and adaptive re-decomposition on failure.

---

## 6. Formal Decomposition Algebra

The decomposition algebra is the mathematical foundation that ensures RIF's recursive decomposition is well-behaved. It provides three guarantees: every decomposition terminates in finite steps, no decomposition produces a cycle, and no decomposition allocates more resources than the parent possesses. These are not aspirational properties or implementation guidelines — they are mathematical invariants enforced by the decomposition engine.

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

**Step 1 — Every decomposition step produces children strictly less than the parent.**

Case analysis by parent class:

- `class(parent) = G`: Children have `class(c) in {M,B,X,V,G}`. If `class(c) < G`, then `class_rank(c) < class_rank(parent)` — strictly less by first component. If `class(c) = G`, then `class_rank(c) = class_rank(parent)`, but `remaining_depth(c) = remaining_depth(parent) - 1` — strictly less by second component.

- `class(parent) = V`: Children have `class(c) in {M,B,X}`. `class_rank(c) <= 2 < 3 = class_rank(V)`. Strictly less by first component.

- `class(parent) = X`: Children have `class(c) in {M,B}`. `class_rank(c) <= 1 < 2 = class_rank(X)`. Strictly less by first component.

- `class(parent) = B`: Children have `class(c) in {M}`. `class_rank(c) = 0 < 1 = class_rank(B)`. Strictly less by first component.

- `class(parent) = M`: No children. Decomposition terminates immediately.

**Step 2 — The ordering is well-founded.**

`class_rank` ranges over `{0, 1, 2, 3, 4}` (finite). `remaining_depth` ranges over `{0, 1, ..., max_depth}` (finite). The lexicographic product of two finite well-ordered sets is well-founded.

**Step 3 — Conclusion.**

By the well-ordering principle, every strictly descending chain in a well-founded order is finite. Therefore, every decomposition chain terminates. QED.

**Practical bound**: Maximum decomposition tree size is bounded by:

```
max_tree_size <= SUM_{d=0}^{max_depth} (branching_factor ^ d)
             = (branching_factor^(max_depth+1) - 1) / (branching_factor - 1)
```

With default `max_depth = 10` and a practical branching factor of 5, the theoretical maximum is `(5^11 - 1) / 4 = 12,207,031` nodes. In practice, trees are far smaller because class descent accelerates termination — a V-class intent drops to {M,B,X} on its first decomposition, losing access to V and G classes entirely.

### 6.3 Cycle-Freedom Guarantee

**Claim**: No decomposition can produce a cycle (an intent that is an ancestor of itself).

**Proof sketch**: Assume for contradiction that a cycle exists: a sequence of intents `i_0, i_1, ..., i_k` where `i_{j+1} in children(i_j)` and `i_k = i_0`.

By the decomposition rules, for each step in the sequence, the pair `(class_rank, remaining_depth)` is strictly decreasing (as proved in Section 6.2). If `i_k = i_0`, then:

```
(class_rank(i_k), remaining_depth(i_k)) = (class_rank(i_0), remaining_depth(i_0))
```

But we showed the pair is strictly decreasing along every decomposition edge. A strictly decreasing sequence over a well-founded order cannot return to its starting value. **Contradiction**.

Therefore, no cycle exists. QED.

**Additional structural guarantee**: Each intent's `intent_id` is a UUID generated at creation time. The decomposition engine never reuses an `intent_id`. Even if the same logical decomposition pattern recurs (via memoization), child intents receive fresh UUIDs, making structural cycles impossible at the identifier level as well.

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

**Resource return on completion**: When a child intent completes under-budget, unused additive resources are returned to the parent's available pool. Returned resources become available to sibling intents via lazy redistribution — siblings request additional resources when needed rather than receiving proactive allocations.

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

Decomposition memoization prevents redundant computation when similar intents arrive repeatedly. In a system processing thousands of intents per epoch, many will share structural similarities — the same type of goal in the same domain with similar resource constraints. Recomputing the decomposition plan from scratch each time is wasteful.

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

The Agent Registry maintains the authoritative mapping of agents to their capabilities, cryptographic identities, stake positions, reputation scores, and locus assignments. It is the foundation for all intent assignment decisions — System 3 cannot assign a leaf intent to an agent whose capabilities do not match the required operation class or whose PCVM credibility falls below the intent's minimum threshold.

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
- **To C3**: `sync_locus_assignment(agent_id, locus_id, parcel_id)` — called when C3 tidal rebalancing moves an agent
- **To C5 PCVM**: `refresh_reputation(agent_id) -> ReputationScore` — called once per epoch per active agent

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
  "agent_id": "string"
}
```

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

This is the correct behavior: a partition means causal ordering cannot be maintained across the partition boundary, so cross-locus operations must halt. But local operations — which constitute at least 80% of traffic in a well-configured system — continue normally.

#### Integration Contracts

- **To ISR**: `stamp_transition(intent_id, transition) -> CausalStamp`
- **To System 3**: `current_epoch() -> EpochInfo`
- **To System 3**: `is_within_budget(start_stamp, budget_ms) -> bool`
- **To C3**: `sync_epoch_boundary(epoch, start_ms, duration_ms)` — called by C3 at each epoch boundary

### 7.3 Intent State Registry

#### Purpose

The ISR is the authoritative store for all intent quanta within a locus. It maintains the current lifecycle state of every intent, the parent-child decomposition tree, the transition history, and resource accounting. It is the component that System 3 reads from and writes to most frequently — every decomposition, every state transition, every resource reconciliation flows through the ISR.

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
- **To C4 ASV**: `emit_intent_claim(intent_id, outcome)` — publishes intent outcome as ASV claim

### 7.4 Settlement Router

#### Purpose

The Settlement Router bridges RIF's intent lifecycle with C3's settlement ledger. When an intent completes, the Settlement Router ensures that all resource accounting, stake adjustments, and reputation updates are recorded. It provides at-least-once delivery with idempotent processing, guaranteeing no settlement is lost even under partitions or crashes.

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

- **No cross-locus replication**: Settlement messages are locus-local. Each locus has its own queue and its own connection to its C3 settlement ledger partition.
- **Persistence**: Write-ahead-log style — message is durable before ISR receives acknowledgment.
- **At-least-once delivery**: Exponential backoff retries (1, 2, 4, 8, 16, 32 epochs). After 10 failed attempts, message moves to DEAD_LETTER and System 3 is alerted.
- **Idempotency**: C3 ledger rejects duplicate `settlement_id` values, so at-least-once delivery is safe.

#### Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| C3 ledger unreachable | Delivery timeout (1 epoch) | Retry with exponential backoff |
| Duplicate delivery | C3 rejects duplicate settlement_id | Mark as CONFIRMED (idempotent) |
| Dead letter accumulation | Count > 100 | System 3 alert; manual intervention required |
| Queue backpressure | Depth > 10,000 or oldest pending > 50 epochs | Throttle intent completions; notify System 3 |
| Router crash | Failure Detector liveness check | Restart from WAL; replay all PENDING messages |

### 7.5 Failure Detector

#### Purpose

RIF's Failure Detector goes beyond traditional heartbeat monitoring. It serves two functions:

1. **Agent liveness**: Is the agent alive and responsive? (Classical failure detection via quorum-based sentinel checks.)
2. **Intent outcome verification**: Did the intent's result actually advance the parent intent's success criteria? (Semantic failure detection via C5 PCVM integration.)

The second function distinguishes RIF from systems that equate "task completed" with "task succeeded." An agent may be alive and responsive but consistently producing results that do not advance system goals — a subtle failure mode that heartbeat monitors cannot detect.

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
  "verification_claim_id": "string -- C4 ASV claim ID"
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
- **To C4 ASV**: `publish_verification_claim(verification) -> claim_id`

---

## 8. Executive Plane

The Executive Plane implements Stafford Beer's System 3/4/5 distinction for the operational, strategic, and governance functions of intent orchestration. This section specifies each system's responsibilities, internal mechanisms, and interaction protocols.

### 8.1 System 3: Operational Control

System 3 is the operational heart of RIF. It receives intent proposals, decomposes them, assigns leaf intents to agents, monitors execution, and handles failures. It is the most active component in the Executive Plane — present-focused, dealing with what the system is doing *right now*.

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
        agent = select_agent(intent.operation_class, intent.scope.domain)
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

**Decomposition strategy selection**:

| Strategy | When Selected | Execution Model | Failure Behavior |
|---|---|---|---|
| RECURSIVE | Intent is divisible and scope can partition | Divide scope; same intent type on each partition | Partial success; evaluate combined results |
| PARALLEL | Success criteria is conjunctive; sub-goals are independent | All children execute concurrently | All-or-nothing by default; configurable partial threshold |
| SEQUENTIAL | Success criteria requires ordered steps; outputs chain | Children in declared order; output N feeds input N+1 | First failure halts pipeline; compensate completed steps |
| CONDITIONAL | Success criteria has branching predicates | Predicate selects one branch | Selected branch fails => no fallback unless configured |

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

#### 8.1.2 Resource Optimizer

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

#### 8.1.3 Performance Monitor

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

#### 8.1.4 Failure Playbooks

Pre-defined response procedures for common failure scenarios:

**AGENT_CRASH**: Identify all ACTIVE intents on the failed agent. Re-queue each as PROPOSED. Blacklist agent for 5 epochs. Escalate intents past 50% of deadline to parent for re-decomposition. If agent has significant stake, escalate to System 5.

**DECOMPOSITION_TIMEOUT**: Dissolve partial children. Mark intent as DISSOLVED. Log for System 4 analysis. Escalate if the intent type has > 30% timeout rate.

**RESOURCE_EXHAUSTION**: Pause new PROPOSED intents. Let in-flight intents complete. Aggressive GC on DISSOLVED entries. Request System 4 capacity review. Escalate to System 5 if pause exceeds 10 epochs.

**CASCADE_FAILURE** (completion rate < 50% for 3 epochs): Halt all new decompositions. Identify common failure pattern (shared agent, resource, or cached plan). Invalidate relevant memoization entries. Resume one-at-a-time to isolate cause. Escalate to System 5 for emergency tidal rollback consideration.

**SETTLEMENT_BACKLOG**: Throttle completions to match settlement throughput. Prioritize stake-bearing agent settlements. Alert System 5 if dead letters exceed 100.

**SPANNING_INTENT_PARTITION**: Wait 5 epochs for resolution. If unresolved, timeout spanning children. Re-decompose parent excluding partitioned locus. Escalate to System 4 for cross-locus rebalancing.

#### 8.1.5 Compensation Protocols

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

System 4 is the forward-looking component. It reads trends, anticipates future resource needs, and proposes adaptations. System 4 has no direct authority to change operations — it can only propose. This constraint is fundamental: a system that both plans changes and implements them without checks is a system that can oscillate into instability.

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
            // Higher confidence bar for scale-down (conservative)
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
    // At volatility=0, discount=1.0 (no reduction)
    // At volatility=0.5, discount~=0.62
    // At volatility=1.0, discount~=0.27
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

System 5 is the identity and governance layer. It maps directly onto C3's existing G-class constitutional consensus mechanism — System 5 does not introduce new governance primitives. It provides the interface through which the Executive Plane interacts with established governance.

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
            // Timeout or no quorum: status quo preserved
            return Resolution(winner="SYSTEM_3_DEFAULT",
                              reason="No quorum; status quo preserved")
```

#### 8.3.3 Sovereignty Relaxation

Under exceptional circumstances, System 3 may need to operate outside normal constraints. This requires System 5 authorization:

- **Vote threshold**: 90% supermajority of G-class governance-capable agents.
- **Maximum lease**: 50 epochs. No renewal without a fresh vote.
- **Early revocation**: System 5 may revoke if justifying conditions no longer hold.
- **Audit trail**: All relaxations are logged immutably in the C3 settlement ledger.

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
| Provenance Chain Integrity | Every transition has a valid causal stamp and ASV provenance | ISR enforces; System 5 audits via C4 |

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

The choice of three executive systems is not arbitrary — it reflects a deep structural requirement.

**Why not two systems?** If we merge System 3 and System 4 into a single "operational + strategic" executive, the same component that plans adaptations also implements them. There is no check on whether an adaptation is wise — the system can propose a change, approve its own proposal, and implement it in a single cycle. This creates a classic feedback loop: a noisy signal triggers an adaptation, the adaptation worsens the situation, and the worsened situation triggers a stronger adaptation. Beer called this "the oscillation problem" and it is the primary reason the VSM separates System 3 from System 4.

In RIF's context, imagine System 4 observing a spike in EMA projections for domain X and simultaneously having the authority to redistribute agents. Without the System 3 check, it could trigger a massive agent rebalancing that disrupts in-flight intents, causing cascade failures that look like an even bigger problem, triggering an even bigger rebalancing. The cool-down, similarity detection, and stability gating (Section 8.2.4) are precisely the anti-oscillation mechanisms that Beer predicted would be necessary.

**Why not four or more systems?** Beer's original model includes System 1 (Operations) and System 2 (Coordination). In Atrahasis, these already exist: C3 parcels are System 1 and C3 tidal scheduling is System 2. Adding them to RIF's Executive Plane would duplicate existing functionality and violate Principle 4 (Substrate Awareness). Similarly, System 3* (Audit) maps to C5 PCVM + Sentinel, which already exists and which RIF integrates via the Failure Detector. Creating a separate System 3* component within RIF would be redundant.

The three systems in RIF's Executive Plane are exactly the VSM components that were *missing* from the Atrahasis stack:

| VSM System | Was it already in Atrahasis? | RIF's role |
|---|---|---|
| System 1 (Operations) | Yes — C3 parcels | N/A (substrate) |
| System 2 (Coordination) | Yes — C3 tidal scheduling | N/A (substrate) |
| System 3 (Internal Control) | **No** | RIF System 3 |
| System 3* (Audit) | Yes — C5 PCVM + Sentinel | Integration via Failure Detector |
| System 4 (Intelligence) | **No** | RIF System 4 |
| System 5 (Policy) | Partially — G-class governance existed but had no executive interface | RIF System 5 (interface to existing governance) |

Three systems is not a design choice — it is a consequence of filling exactly the gaps that existed. No more, no less.

---

*End of Part 1 (Sections 1-8). Part 2 continues with Sections 9-14: Cross-Locus Intent Coordination, Tidal Integration Protocol, Substrate Integration (C3/C4/C5/C6), Security Model, Operational Parameters, and Validation Plan.*
