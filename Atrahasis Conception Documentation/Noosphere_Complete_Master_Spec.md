# THE NOOSPHERE PROTOCOL SPECIFICATION

## Homeostatic Verification-First Epistemic Coordination Fabric

**The Distributed Coordination Architecture for Atrahasis**

Final Canonical Reference — All Versions Consolidated
March 2026

---

## Document History

This is the single canonical specification of the Noosphere protocol. It consolidates nine design iterations into one cohesive document, preserving all substantive detail:

- **v1–v2**: Conceptual architecture, HEF integration, paradigm definition, cross-domain analysis.
- **v3**: Red-team review and subsystem replacement (SLV replaced pressure model, SK-2PC replaced ribbon commit, PI controller replaced Homeostat, Stratified Capability Sampling replaced ad-hoc verifier selection, Contradiction Lattice invented, Bundle Compaction invented, Scope Attention Market invented).
- **v4**: Structural hardening (Scoped Replica Groups, Tiered Atomicity with Deterministic Batch Execution, controller stability protections, APV mechanism design with anti-gaming, cross-region consistency with RVQI).
- **v5**: AASL type integration (10 new types, 18 AACP message types, signal reinforcement/decay formalized, wire format specified, operational simplification for APV).
- **Master v2**: Locus Fabric merge (Locus/Parcel decomposition, M/B/X/V/G operation-class algebra, Certified Slice Objects, Fusion Capsules with Capsule Epoch Protocol, three-budget model, claim-class-specific membrane, Contestable Reliance Membrane, Witness Ladder, Sentinel Graph).
- **Master v3**: Simulation specifications (parcel controller 7-workload suite, CEP TLA+ state machine with 6 formal invariants, 10 governance anti-manipulation rules, economic simulation 7-scenario suite with deployment gates).
- **Master v4**: Defense-in-depth (circuit breaker with 5 trigger conditions, parcel rollback records, degradation mode, 5 Byzantine defenses for Fusion Capsules, governance health dashboard with 4 automated monitors and 3 response playbooks, governance escape valve).
- **Master v5**: Verification Membrane hardening (constitutional protection law, claim classification gate with 4-step protocol, deep verifier diversity with 4 rules + weight cap, evidence relevance verification with 3 rules, supersession protocol with 5 conditions, Membrane Quality Index with 6 metrics and 3 response tiers, continuous re-verification with citation-weighted sampling, membrane implementation constraints, complete 30+ failure mode coverage table).

All superseded mechanisms have been removed. Only the latest surviving version of each component appears.

### The Architectural Commandment

> **Optimize the rest of the system around the membrane. Never optimize the membrane around the rest of the system.**

---

## Table of Contents

**Part I — Foundations**
1. Executive Summary
2. Core Architectural Principles
3. Cross-Domain Inspiration
4. Architecture Space Evaluation

**Part II — Primitives and Types**
5. Fundamental Primitives
6. AASL Type Definitions

**Part III — System Architecture**
7. Functional Pillars
8. System Architecture Overview
9. Locus and Parcel Model
10. Replica Groups

**Part IV — Agreement and Coordination**
11. Operation-Class Algebra
12. Fusion Capsule Epoch Protocol

**Part V — The Verification Membrane**
13. Verification Membrane Overview
14. Claim Classification Gate
15. Verifier Selection
16. Claim-Class-Specific Promotion
17. Contestable Reliance Membrane for Heuristic Claims
18. Supersession Protocol
19. Membrane Drift Detection
20. Continuous Re-Verification
21. Membrane Implementation Constraints
22. Complete Membrane Failure Mode Coverage

**Part VI — Knowledge Persistence**
23. Four-Tier Memory Model
24. Contradiction Lattice and Argumentation
25. Bundle Compaction

**Part VII — Resources and Economics**
26. Three-Budget Resource Model
27. Certified Slice Objects
28. Scope Attention Market
29. Economic Simulation Specification

**Part VIII — Control and Self-Regulation**
30. Bi-Timescale Controller
31. Parcel Controller Simulation Specification
32. Controller Structural Safeguards

**Part IX — Federation and Recovery**
33. Cross-Region Federation
34. Failure Recovery: Witness Ladder

**Part X — Security**
35. Sentinel Graph
36. Heuristic Claim Governance
37. Defense-in-Depth Summary

**Part XI — Communication**
38. Communication Architecture and AACP Integration

**Part XII — Deployment**
39. Scalability Model
40. Comparison with Existing Systems
41. Why This Is a New Paradigm
42. Integration with Atrahasis Subsystems
43. Implementation Roadmap
44. Formal State Model
45. Open Research Questions
46. Follow-On Specification Documents
47. Architecture Maturity Summary

---

# PART I — FOUNDATIONS

## 1. Executive Summary

The **Noosphere** is a Homeostatic Verification-First Epistemic Coordination Fabric for the Atrahasis planetary intelligence network. It is neither a blockchain, DAG ledger, distributed log, nor event-stream system.

**The core architectural law:** Replace global event ordering with scoped verified convergence.

**The defining insight:** Blockchains ask *"what happened, in what order, under adversarial conditions?"* — a transaction-centric question. Atrahasis must ask *"what is the current verified belief, plan, reservation, and capability distribution across billions of agents?"* — an epistemic and operational question. These are fundamentally different questions demanding fundamentally different architectures.

**The shortest statement of the invention:** Atrahasis should coordinate like a nervous system with an immune membrane and a memory cortex, not like a bank ledger.

The architecture separates **stable logical coordination domains (Loci)** from **elastic physical execution units (Parcels)**, derives agreement mode from **operation-class algebra** rather than ad hoc choice, gates knowledge admission through a **claim-class-specific verification membrane**, and replaces monolithic gas with a **three-budget resource model** where payment, spam control, and capacity reservation are separate concerns.

The Verification Membrane is the civilizational bottleneck. A bad controller wastes compute; a bad membrane poisons cognition. Epistemic corruption compounds through the knowledge graph in ways that are much harder to detect than performance degradation — the system may continue functioning while quietly building on wrong assumptions. The membrane is therefore the most heavily defended subsystem in the architecture.

The Noosphere integrates with every layer of the Atrahasis stack: CIOS orchestration, Verichain verification, AASL semantic representation, agent clusters, the distributed knowledge graph, and planetary compute infrastructure. It replaces the placeholder AIChain with a purpose-built coordination substrate.

---

## 2. Core Architectural Principles

These principles are invariant and must survive any future redesign:

1. **Coordination is local by default.** Serialize only where real contention exists.
2. **Verification gates canonical memory.** The membrane is mandatory and non-negotiable.
3. **Ephemeral coordination, durable knowledge.** Most coordination traces decay; only verified outputs persist.
4. **Agreement mode is derived from operation class.** The M/B/X/V/G algebra determines agreement cost from invariant type — not ad hoc selection.
5. **Logical coordination domains are separate from physical execution units.** Semantic loci split rarely. Parcels split and migrate often. Without this separation, the system constantly redraws correctness boundaries under load — the most dangerous failure mode.
6. **Bulk artifacts travel on a separate availability plane.** The control plane carries references and certificates, never large blobs.
7. **AASL/AACP is the protocol language.** All coordination primitives are typed and machine-parseable. Not an afterthought.
8. **Exact global consensus is reserved for money, governance, and rare cross-locus exclusivity.**
9. **The system is self-regulating.** A bi-timescale controller adjusts parameters continuously. Static parameters will not survive planetary-scale operation.
10. **Heuristic claims are operationally canonical, not ontologically canonical.** The membrane grants permission to rely, not claims of timeless truth.
11. **The membrane is constitutionally protected.** No system parameter may reduce membrane verification depth, widen admission thresholds, or relax class-specific rules. Only G-class constitutional consensus with 75% supermajority and 72-hour discussion period can modify membrane rules. The Feedback Controller and economic system are explicitly prohibited from adjusting membrane parameters.

---

## 3. Cross-Domain Inspiration

### 3.1 Biological Systems

#### 3.1.1 The Immune System as Verification Membrane

The adaptive immune system is the closest biological analogue to what Atrahasis needs. It operates as a massively parallel verification network: when a pathogen enters the body, millions of lymphocytes independently evaluate whether a molecular pattern is self or non-self. No central controller sequences this evaluation. Instead, cells that successfully bind to a threat undergo clonal expansion, amplifying the verified signal. Cells that fail verification undergo apoptosis. Critically, the innate immune system retains **trained memory** from prior encounters, changing future response speed and intensity without requiring a single global controller.

**Extracted principles:** Independent parallel verification with no central coordinator; amplification of verified signals proportional to verification confidence; elimination of unverified or low-confidence outputs; memory cells that persist verified knowledge for rapid future response; trained immunity that modifies future routing and trust.

#### 3.1.2 Bacterial Quorum Sensing and Threshold Coordination

Bacteria coordinate collective behavior through quorum sensing: individual cells release signaling molecules, and when the local concentration exceeds a threshold, the population switches behavior collectively. This is a threshold-triggered coordination mechanism that requires no leader election, no total ordering, and no global state. It operates purely on local density detection. The system stays locally quiet until conditions require coordinated action.

**Extracted principle:** Coordination can emerge from local signal accumulation reaching defined thresholds, without any global agreement protocol. Escalation should be thresholded, not global by default.

#### 3.1.3 Neural Plasticity and Synaptic Strengthening

The brain does not record memories in a ledger. Synaptic connections strengthen when they participate in successful pattern completion and weaken when they do not. Knowledge is encoded in the topology of connections, not in an ordered log of events. The verification mechanism is functional success: did the connection contribute to a useful outcome?

**Extracted principle:** Knowledge persistence should be encoded in strengthened pathways and accumulated confidence scores, not in append-only records. Memory should change future routing and trust.

### 3.2 Swarm Intelligence

#### 3.2.1 Stigmergic Amplification with Decay

Ant colonies coordinate complex construction through stigmergy: agents modify their shared environment (depositing pheromones), and other agents respond to the modified environment rather than to direct communication. The environment itself becomes the coordination medium. Critically, pheromone traces **decay over time** unless reinforced by additional agents. This decay mechanism is essential: it prevents stale coordination signals from misdirecting future work, and it ensures that the system's coordination state reflects current reality rather than accumulated history.

**Extracted principles:** The shared environment can serve as the primary coordination mechanism. Local traces should recruit work. Signals should decay unless reinforced. The coordination substrate should reflect current state, not accumulated history.

#### 3.2.2 Bee Colony Decision-Making

Honeybee swarms select nest sites through distributed evaluation: scouts independently evaluate candidates, perform waggle dances proportional to quality, recruit more scouts to the best sites, and converge when a quorum aggregates at one location. No bee has a global view. The process is robust to individual errors because poor sites attract fewer recruits.

**Extracted principle:** Distributed evaluation with quality-proportional amplification naturally converges on correct outcomes without requiring global agreement rounds.

### 3.3 Neuroscience

#### 3.3.1 Cortical Columns as Self-Assembling Reasoning Cells

The neocortex is organized into cortical columns: small groups of densely connected neurons that process local information and communicate summaries to neighboring columns. Columns are not permanently assigned to specific tasks — they recruit and release resources dynamically based on processing demands. This is remarkably similar to the tetrahedral cluster model in Atrahasis, but with a crucial addition: the clusters should be **dynamic**, forming around active processing demands and dissolving when the demand subsides.

**Extracted principle:** Hierarchical clustering with local dense connectivity and sparse long-range connections. Clusters should self-assemble around active demands, not exist as permanent static structures.

#### 3.3.2 Predictive Coding and Bandwidth Optimization

Modern neuroscience models the brain as a prediction machine: each cortical layer generates predictions about expected input, and only prediction errors propagate upward. This drastically reduces communication bandwidth because expected signals are suppressed. For Atrahasis, verified knowledge that confirms existing knowledge should require minimal coordination overhead, while novel or contradictory claims should trigger full verification cascades.

**Extracted principle:** Coordination effort should be proportional to epistemic novelty. Confirmed knowledge requires minimal overhead; surprising claims require maximal verification.

#### 3.3.3 Small-World Modularity

Nervous systems repeatedly exhibit small-world modularity: high local clustering, short global path lengths, and multiscale organization rather than flat all-to-all communication. Dense local clusters with sparse global shortcuts consistently outperform flat meshes in both biological and artificial networks.

**Extracted principle:** Dense local clusters with sparse global shortcuts beat flat meshes. Not every local disagreement requires immediate global resolution.

### 3.4 Complex Adaptive Systems

Self-organizing systems from economies to ecosystems share a common pattern: local agents following simple rules produce emergent global order without central control. The critical requirement is that local rules encode feedback about system-level outcomes. The system must embed feedback loops that connect individual agent behavior to system-level intelligence quality. Additionally, these systems maintain **homeostasis**: internal regulatory mechanisms that keep operating parameters within viable ranges despite external perturbation.

**Extracted principle:** The coordination architecture must embed feedback loops connecting individual behavior to system-level quality, and it must include homeostatic control mechanisms that self-regulate system parameters.

### 3.5 Six Consolidated Coordination Principles

1. **Local traces should recruit work.** (Stigmergy)
2. **Signals should decay unless reinforced.** (Pheromone evaporation)
3. **Escalation should be thresholded, not global by default.** (Quorum sensing)
4. **Memory should change future routing and trust.** (Trained immunity, synaptic plasticity)
5. **Dense local clusters with sparse global shortcuts beat flat meshes.** (Small-world neuroscience)
6. **Not every local disagreement requires immediate global resolution.** (Distributed brain processing)

---

## 4. Architecture Space Evaluation

Blockchains and DAG ledgers solve one question extremely well: *what happened, in what order, under adversarial conditions?* Atrahasis needs to solve a different question: *what is the current verified belief, plan, reservation, and capability distribution across billions of agents?* The first question is transaction-centric; the second is epistemic and operational.

| Architecture Class | Evaluation for Atrahasis |
|---|---|
| **Blockchains (Bitcoin, Ethereum)** | Designed for totally ordered financial transactions. Total ordering is unnecessary and harmful for intelligence coordination: reasoning tasks have causal dependencies, not temporal dependencies. Proof-of-work wastes compute that should be used for reasoning. Block-based batching adds latency incompatible with real-time agent coordination. **Verdict:** wrong primitive (transactions), wrong ordering (total), wrong consensus (economic). |
| **DAG Ledgers (IOTA, Hashgraph)** | Better than linear chains because DAGs capture parallel events. IOTA contributes the insight that congestion control can be access-based rather than gas-based. Hashgraph contributes fair ordering and a refusal to discard concurrency. However, DAG ledgers still focus on ordering events rather than verifying knowledge claims. **Verdict:** useful structure and access-control insights, wrong semantics. |
| **Distributed Logs (Kafka, Pulsar)** | High-throughput append-only logs excel at event streaming but provide no verification semantics, no causal reasoning about claim dependencies, and no knowledge accumulation model. They preserve too much chatter and too little meaning. **Verdict:** good transport, not a coordination architecture. |
| **Gossip Networks** | Efficient for disseminating information but provide no mechanism for verification, ordering, or knowledge accumulation. Useful as a communication substrate. **Verdict:** useful primitive, not sufficient alone. |
| **CRDTs / Invariant Confluence** | Conflict-free replicated data types handle concurrent updates elegantly but assume all updates are valid. Intelligence coordination requires distinguishing verified from unverified claims. CRDTs have no verification gate. However, I-confluence analysis determines which operations are safe for coordination-free execution. **Verdict:** convergence foundation for M-class operations, missing verification. I-confluence criterion adopted. |
| **Narwhal/Tusk** | The separation of data dissemination and availability from consensus ordering is a critical insight to adopt. Large blobs should move through an availability layer, not the control plane. **Verdict:** key structural insight adopted for both claim routing and artifact availability. |
| **Bullshark DAG-BFT** | Demonstrates high-throughput DAG-based consensus with minimal communication overhead. Adds a synchronous fast path without heavy view-change machinery. **Verdict:** confirms DAG structure efficient for parallel coordination. |
| **Celestia** | Separates consensus, execution, settlement, and data availability into independent layers. Namespaced retrieval means consumers fetch only what their scope requires. **Verdict:** modular decomposition and namespaced availability critical to adopt. |
| **Avalanche** | Metastable sampled convergence instead of all-to-all voting. Fast for binary decisions. For intelligence verification (which requires nuanced scoring), subsampling is useful for low-stakes claims with escalation to deeper verification for contested claims. **Verdict:** subsampling adopted for initial convergence, escalation needed for contested claims. |
| **Sui** | Only shared mutable objects need the expensive consensus path; owned objects can be processed without consensus. This directly maps to the Noosphere: only exclusive resources need serialization; independent claims need no global coordination. The fast-path/consensus split directly informs the M/B/X/V/G algebra. **Verdict:** owned-vs-shared distinction directly applicable. |
| **Radix Cerberus** | Atomic cross-shard composition for only the state actually touched. Synchronize only the scopes that contend. **Verdict:** scope-local serialization directly applicable. |

**Consolidated conclusion:**

- Ledger systems over-order Atrahasis traffic.
- Knowledge graphs under-coordinate live work.
- Swarm/blackboard systems under-secure trust and incentives.
- Event streams preserve too much chatter and too little meaning.

The right architecture combines DAG structure from Narwhal/Bullshark, modular separation from Celestia, scope-local serialization from Cerberus, access-based congestion control from IOTA, sampled convergence from Avalanche, and the owned-vs-shared distinction from Sui — but replaces all transaction/financial semantics with **epistemic semantics built around decaying scoped signals, verification membranes, and knowledge accumulation.**

The architecture's center of gravity is **typed coordination state over loci**, not event history.

---

# PART II — PRIMITIVES AND TYPES

## 5. Fundamental Primitives

The Noosphere is built from fifteen fundamental primitives:

| Primitive | Definition | Durability |
|---|---|---|
| **Identity** | Agent, model, provider, human, or institution. Cryptographic keypair + capability vector + reputation vector + stake + safety clearance + governance rights. | Durable |
| **Locus** | Stable logical coordination domain: `<selector, invariant_set, locality, safety_class, epoch_class>`. The correctness boundary. Splits rarely — only on semantic grounds, governance approval for HIGH+. | Durable |
| **Parcel** | Elastic physical execution unit within a locus: hot object subset, active leases, current replica set, observed conflict/co-access statistics. Splits and migrates often — managed by bi-timescale controller. | Ephemeral (reconfigurable) |
| **Signal** | Typed, signed, decaying field entry. Core types: `need`, `offer`, `claim`, `risk`, `reservation`, `anomaly`, `attention_request`. Carries confidence, priority, decay time constant (τ), provenance, and signature. Unreinforced signals evaporate automatically. | Ephemeral |
| **Claim** | Structured AASL assertion. Claim classes: `deterministic`, `empirical`, `statistical`, `heuristic`, `normative`. States: `active`, `provisional`, `disputed`, `verified`, `superseded`. Claim types: `observation`, `derivation`, `synthesis`, `hypothesis`, `prediction`. A specialized signal that can cross the verification membrane. | Ephemeral → durable after bundling |
| **Lease** | Time-bounded right to mutate an exclusive resource or reserve capacity. Auto-expires if not renewed. Only lease acquisition requires scope-local serialization. | Ephemeral |
| **Attestation** | Single verifier's structured judgment on a claim. Carries method, score, evidence references, relevance confirmation, and signature. | Durable (part of membrane proof) |
| **Bundle** | Verified consolidation unit written to persistent memory. Contains verified claims, supersession edges, artifact references with availability certificates, utility score, and membrane certificate. The growth unit of the knowledge graph. | Durable |
| **Certified Slice Object (CSO)** | Proof-carrying object for bounded resource rights. Conservation law, local non-negativity, transfer linearity, deterministic merge. Replaces monolithic APV for capacity reservation. | Durable |
| **Membrane Certificate (MCT)** | Deterministic admission artifact: schema root, availability root, verifier cert, contradiction scan root, lineage root, retention policy, membrane version. | Durable |
| **Governance Directive** | Policy change, parameter update, or constitutional enforcement action. Requires constitutional consensus. Itself verified before activation. | Durable |
| **Witness Seal** | Quorum-signed commitment to locus state: snapshot root, delta root, frontier root. Periodically anchored to settlement plane. | Durable |
| **Sentinel Edge** | Formal anomaly link: `<subject_a, subject_b, relation_type, evidence_ref, confidence, epoch>`. Types include collusion suspicion, withholding, replay anomaly, identity churn, verification drift, regional degradation. | Durable while relevant |
| **Contradiction Edge** | Link between two claims making incompatible assertions. Tracks evidence weight on each side and resolution state. | Durable while either claim active |
| **Reliance Permit** | Time-bounded permission to rely on a heuristic claim family in a defined context, horizon, and risk class. Carries approver set, revocation rule, rationale root. Automatically revoked if attack edge accepted or assumption invalidated. | Durable (expires by TTL) |

**The key break with blockchains: the primitive is not the transaction. It is the scoped, decaying signal.**

---

## 6. AASL Type Definitions

Every Noosphere primitive has a concrete AASL type. All inter-component messages are AASL-typed and AACP-framed. No opaque binary blobs in the control plane. Artifacts (large blobs) are referenced by hash, not inlined.

### 6.1 Complete Type Token Registry — 23 Tokens

| Token | Object | Source |
|---|---|---|
| `LOC` | Locus | Locus Fabric |
| `PCL` | Parcel | Locus Fabric |
| `SIG` | Signal | Noosphere v5 |
| `CLM` | Claim (extended with claim_class) | Extended from AASL v1 |
| `LSE` | Lease | Noosphere v5 |
| `ATT` | Attestation (extended with relevance_confirmation) | Extended from AASL v1 VRF |
| `BDL` | Bundle (extended with membrane_cert) | Noosphere v5 |
| `CSO` | Certified Slice Object | Locus Fabric |
| `MCT` | Membrane Certificate | Locus Fabric |
| `GOV` | Governance Directive | Noosphere v5 |
| `WSL` | Witness Seal | Locus Fabric |
| `SNE` | Sentinel Edge | Locus Fabric |
| `CTD` | Contradiction Edge | Noosphere v3 |
| `SLV` | Load Vector (per-Parcel, ephemeral diagnostic) | Noosphere v3 |
| `HFM` | Heuristic Family | Locus Fabric |
| `RLP` | Reliance Permit | Locus Fabric |
| `CAP` | Fusion Capsule | Locus Fabric |
| `GNT` | Authority Grant (for capsule handoff) | Locus Fabric |
| `CLS` | Classification Seal | Master v5 |
| `SUP` | Supersession Record | Master v5 |
| `RPT` | Reliance Propagation Tag | Master v5 |
| `MBV` | Membrane Version | Master v5 |
| `GMR` | Governance Monitor Record | Master v4/v5 |

Existing AASL v1 types reused without change: `AGT` (agent), `EVD` (evidence), `CNF` (confidence), `PRV` (provenance), `TIM` (time).

### 6.2 LOC — Locus

```
LOC{
  id:loc.biology.proteomics.high
  selector:biology.proteomics
  invariant_set:[conservation.compute_budget,exclusion.protein_db_write]
  locality:region.asia_pacific
  safety_class:HIGH
  epoch_class:standard
  state:active
  created_epoch:4100
}
```

### 6.3 PCL — Parcel

```
PCL{
  id:pcl.bio_prot.hot_set_7
  locus:loc.biology.proteomics.high
  object_set:[obj.protein_db.segment_7,obj.simulation_queue.batch_12]
  replica_group:[node.ap3,node.ap7,node.ap12,node.eu2,node.na5]
  epoch:4207
  load_vector:ref.slv.pcl_bio_prot_hot7.4207
  parcel_lifetime_epochs:42
}
```

### 6.4 SIG — Signal

```
SIG{
  id:sig.need.8f3a2b
  type:need
  scope:loc.biology.proteomics.high
  issuer:ag.research.042
  payload:ref.aasl.task_description.8f3a2b
  confidence:0.85
  priority:3
  decay_tau:3600
  created_at:2026-03-09T14:22:00Z
  reinforced_at:2026-03-09T15:10:00Z
  reinforcement_count:2
  sig:ed25519.ag042.abc123
}
```

**Signal type enumeration:** `need | offer | claim | risk | reservation | anomaly | attention_request`

**Reinforcement rule:** When agent B publishes a signal with the same `(type, scope, payload_hash)` as an existing signal from agent A, the scope shard does not create a duplicate. Instead, it increments `reinforcement_count` and updates `reinforced_at`. The effective remaining TTL is reset to `decay_tau` from the latest reinforcement.

**Decay rule:** A signal is removed when `now() - reinforced_at > decay_tau` and `reinforcement_count` has not increased. Decay is computed lazily: signals are not actively garbage-collected on a timer. Instead, they are filtered out at read time and batch-purged during periodic compaction.

### 6.5 CLM — Claim (Extended)

```
CLM{
  id:clm.deriv.9c4e1a
  claim_class:empirical
  type:derivation
  locus:loc.biology.proteomics.high
  agent:ag.research.042
  body:ref.aasl.claim_body.9c4e1a
  evidence:[ref.evd.dataset.44,ref.evd.paper.smith2025]
  causal_parents:[clm.obs.7b2d3f,clm.deriv.5a1c8e]
  contradicts:[clm.deriv.3f7a2b]
  confidence:0.78
  verification_state:active
  reasoning_trace:hash.trace.9c4e1a
  decay_tau:86400
  sig:ed25519.ag042.def456
}
```

**Claim classes:** `deterministic | empirical | statistical | heuristic | normative`

**Verification states:** `active | provisional | disputed | verified | superseded`

**Claim types:** `observation | derivation | synthesis | hypothesis | prediction`

### 6.6 LSE — Lease

```
LSE{
  id:lse.7d2f1a
  locus:loc.biology.proteomics.high
  resource_set:[obj.protein_db.write,obj.simulation_queue.priority]
  holder:ag.analysis.017
  rights:mutate
  epoch:4207
  ttl:300
  granted_at:2026-03-09T14:35:00Z
  quorum_cert:cert.srg.pcl_bio_prot.4207.7d2f1a
  sig:ed25519.srg_coordinator.ghi789
}
```

**Rights enumeration:** `read_exclusive | mutate | reserve_compute | reserve_bandwidth`

### 6.7 ATT — Attestation (Extended)

```
ATT{
  id:att.4a8b2c
  claim:clm.deriv.9c4e1a
  verifier:ag.verification.089
  method:replication
  score:0.91
  evidence:[ref.evd.replication_run.4a8b2c]
  relevance_confirmation:true
  relevance_note:"Evidence dataset covers same protein family and experimental conditions as claim"
  reasoning_trace:hash.trace.att.4a8b2c
  created_at:2026-03-09T15:00:00Z
  sig:ed25519.ag089.jkl012
}
```

**Method enumeration:** `replication | cross_reference | logical_check | statistical_analysis | human_review`

### 6.8 BDL — Bundle

```
BDL{
  id:bdl.loc_bio_prot.epoch4207.batch3
  locus:loc.biology.proteomics.high
  verified_claims:[clm.deriv.9c4e1a,clm.obs.7b2d3f]
  supersedes:[clm.deriv.old_3f7a2b]
  artifacts:[ref.artifact.dataset.44.avail_cert]
  utility_score:0.73
  membrane_cert:ref.mct.bdl.4207.batch3
  settlement:ref.settlement.bdl_4207_batch3
  committed_at:2026-03-09T15:05:00Z
  committed_by:srg.pcl_bio_prot
  sig:ed25519.srg_quorum.mno345
}
```

### 6.9 CSO — Certified Slice Object

```
CSO{
  id:cso.compute.loc_bio_prot.node_ap3
  resource_type:compute_gpu_minutes
  total_supply:10000
  alloc_authority:node.ap3
  alloc_amount:2500
  spent_frontier:1847
  pending_out:0
  pending_in:0
  epoch:4207
  proof_hash:hash.cso_proof.ap3.4207
}
```

### 6.10 MCT — Membrane Certificate

```
MCT{
  id:mct.bdl.4207.batch3
  schema_root:hash.schema.valid
  availability_root:hash.artifacts.available
  verifier_cert:cert.verichain.committee.4207.batch3
  contradiction_root:hash.contradiction_scan.clean
  lineage_root:hash.provenance.valid
  retention_policy:standard_7yr
  membrane_version:ref.mbv.version.4207
}
```

### 6.11 GOV — Governance Directive

```
GOV{
  id:gov.proposal.threshold_adjustment.2026q1
  type:parameter_change
  parameter:verification_threshold.safety_class.HIGH
  old_value:0.80
  new_value:0.85
  proposer:ag.governance.003
  votes_for:847
  votes_against:123
  votes_total:1200
  status:approved
  activation_epoch:4250
  sig:ed25519.governance_quorum.pqr678
}
```

### 6.12 CAP — Fusion Capsule

```
CAP{
  id:cap.cross_bio_chem.9f2a
  touched_set:[obj.protein_db.segment_7,obj.chem_db.reaction_42]
  source_parcels:[pcl.bio_prot.hot_set_7,pcl.chem.hot_set_3]
  exec_host:node.ap12
  status:armed
  expiry_epoch:4208
  commit_record:null
}
```

### 6.13 GNT — Authority Grant

```
GNT{
  id:gnt.obj_protein_seg7.cap_9f2a
  object:obj.protein_db.segment_7
  capsule:cap.cross_bio_chem.9f2a
  current_auth_epoch:47
  proposed_auth_epoch:48
  expiry_epoch:4208
  state_hash:hash.obj_state.seg7.epoch47
  quorum_cert:cert.srg.pcl_bio_prot.4207.gnt_9f2a
  sig:ed25519.srg_coordinator.xyz789
}
```

### 6.14 CLS — Classification Seal

```
CLS{
  id:cls.clm_9c4e1a
  claim:clm.deriv.9c4e1a
  issuer_declared:empirical
  structural_check:empirical
  independent_classifier:ag.classifier.077
  independent_result:empirical
  final_class:empirical
  sealed_at:2026-03-09T14:31:00Z
  sig:ed25519.classification_gate.abc123
}
```

### 6.15 HFM — Heuristic Family

```
HFM{
  id:hfm.drug_efficacy_prediction.2026
  context:oncology.drug_response
  horizon:6_months
  claims:[clm.heur.a1,clm.heur.b2,clm.heur.c3]
  support_edges:[sup.a1_b2,sup.a1_c3]
  attack_edges:[atk.b2_c3]
  assumptions:[asm.patient_population_stable]
  score_history:[0.72,0.68,0.74]
  current_champion:clm.heur.a1
  truth_status:preferred
  reliance_status:bounded_operational
}
```

### 6.16 RLP — Reliance Permit

```
RLP{
  id:rlp.hfm_drug_efficacy.2026q1
  family:hfm.drug_efficacy_prediction.2026
  context:oncology.drug_response
  horizon:3_months
  risk_class:HIGH
  ttl_epochs:720
  reliance_status:bounded_operational
  rationale_root:hash.rationale.rlp_drug_2026q1
  approver_set:[ag.governance.003,ag.human_review.011,ag.verification.089]
  revocation_rule:any_attack_edge_or_invalidated_assumption
}
```

### 6.17 RPT — Reliance Propagation Tag

```
RPT{
  source_family:hfm.drug_efficacy_prediction.2026
  source_reliance:bounded_operational
  source_permit:rlp.hfm_drug_efficacy.2026q1
  propagation_depth:2
  max_permitted_depth:5
}
```

### 6.18 SUP — Supersession Record

```
SUP{
  id:sup.clm_new_vs_clm_old.9c4e1a
  new_claim:clm.deriv.9c4e1a
  old_claim:clm.deriv.3f7a2b
  score_margin:0.14
  evidence_breadth_check:passed
  validity_scope_check:passed
  challenge_window_end:2026-03-12T14:30:00Z
  challenge_status:unchallenged
  independent_verifier:ag.verification.103
  independent_approval:true
  supersession_status:confirmed
  sig:ed25519.membrane.sup123
}
```

### 6.19 MBV — Membrane Version

```
MBV{
  id:mbv.version.4207
  threshold_deterministic:0.95
  threshold_empirical:0.85
  threshold_statistical:0.80
  threshold_heuristic_advisory:0.70
  threshold_heuristic_operational:0.80
  min_committee_LOW:3
  min_committee_MEDIUM:5
  min_committee_HIGH:7
  min_committee_CRITICAL:9
  supersession_margin:0.10
  classification_gate:v2
  activated_epoch:4207
  approved_by:gov.constitutional.vote.4200
}
```

### 6.20 WSL — Witness Seal

```
WSL{
  id:wsl.loc_bio_prot.seal_1847
  locus:loc.biology.proteomics.high
  seal_seq:1847
  snapshot_root:hash.snapshot.1847
  delta_root:hash.deltas.1846_1847
  frontier_root:hash.frontiers.1847
  quorum_cert:cert.srg.bio_prot.epoch4207.seal1847
  anchored_to_settlement:ref.settlement.anchor.1847
}
```

### 6.21 SNE — Sentinel Edge

```
SNE{
  id:sne.collusion.ag042_ag089.epoch4207
  subject_a:ag.research.042
  subject_b:ag.verification.089
  relation_type:collusion_suspicion
  evidence_ref:ref.sentinel.affinity_matrix.4207
  confidence:0.67
  epoch:4207
}
```

### 6.22 CTD — Contradiction Edge

```
CTD{
  id:ctd.clm_9c4e1a_vs_clm_3f7a2b
  claim_a:clm.deriv.9c4e1a
  claim_b:clm.deriv.3f7a2b
  detected_at:2026-03-09T14:32:00Z
  evidence_weight_a:3.7
  evidence_weight_b:2.1
  resolution_state:open
  resolution_deadline:2026-03-10T14:32:00Z
}
```

**Resolution states:** `open | resolved_a_wins | resolved_b_wins | coexist_provisional | escalated_human_review`

### 6.23 SLV — Scope Load Vector

```
SLV{
  parcel:pcl.bio_prot.hot_set_7
  pending_needs:12
  pending_claims:34
  dispute_count:2
  lease_contention:0
  active_agents:8
  verification_lag_p95_ms:4200
  computed_at:2026-03-09T15:10:00Z
}
```

Ephemeral diagnostic. Not persisted in durable storage. Does not require cryptographic signature. Recomputed continuously from parcel state.

### 6.24 GMR — Governance Monitor Record

```
GMR{
  id:gmr.monitor.rapid_cycling.hfm_drug_2026.epoch4207
  monitor_type:rapid_champion_cycling
  family:hfm.drug_efficacy_prediction.2026
  trigger_epoch:4207
  evidence:[champion_changes:4,window:50_epochs]
  response:freeze
  status:active
  resolution:pending
}
```

### 6.25 GPB — Governance Playbook Activation

```
GPB{
  id:gpb.playbook_a.ag042.hfm_drug_2026.epoch4207
  playbook:suspected_manipulation_single_actor
  target_agent:ag.research.042
  affected_family:hfm.drug_efficacy_prediction.2026
  trigger:gmr.monitor.rapid_cycling.hfm_drug_2026.epoch4207
  status:investigation_active
  investigation_deadline:epoch4307
  quarantined_edges:[sup.042_a1,atk.042_c3]
}
```

### 6.26 Wire Format

For prototype implementation, AASL objects are serialized as UTF-8 text (the canonical `.aas` format). For production deployment, the AASL specification reserves `.aasb` as a binary transport format. The Noosphere does not define a new wire format; it uses whatever AASL transport encoding is active.

**Size constraint:** Control-plane messages (signals, claims, attestations, leases, governance directives) must be < 64 KB after serialization. This is enforced at the AACP frame level. Payloads exceeding this limit must reference artifacts by hash via the Artifact Availability Plane.

---

# PART III — SYSTEM ARCHITECTURE

## 7. Functional Pillars

The Noosphere's capabilities decompose into seven independent pillars:

| Pillar | Responsibilities |
|---|---|
| **1. Identity and Capability** | Agent registration, cryptographic identity anchoring, capability vector maintenance, reputation scoring, domain specialization tracking, trust scoring, identity federation across regions, agent lifecycle management from birth through retirement. |
| **2. Coordination and Cell Assembly** | Locus management, parcel management, signal dissemination within loci, SLV computation, cell assembly/dissolution, lease management, claim routing to appropriate verification cells, load balancing across verification capacity. |
| **3. Verification and Trust** | Claim-class-specific verification (deterministic proof, empirical replication, statistical acceptance, heuristic argumentation, normative governance). Classification gate. Attestation collection, membrane certificate issuance, supersession protocol, drift detection, continuous re-verification. Verichain. The civilizational bottleneck. |
| **4. Knowledge Persistence and Retrieval** | Bundle promotion into knowledge graph, semantic indexing, cross-domain linking, version management of knowledge state, supersession tracking, contradiction lattice maintenance, claim-family management, heuristic family management, bundle compaction, canonical memory distillation, query interfaces for agents and humans, knowledge graph federation across regions. |
| **5. Infrastructure Orchestration** | Compute resource allocation, parcel placement (bi-timescale controller), node health monitoring, dynamic scaling, failure detection and recovery, network routing optimization, latency-aware task placement. |
| **6. Resource and Settlement** | Three-budget model (Sponsor Budget, Protocol Credits, Capacity Slices), CSO management, AIC token distribution for verified contributions, staking and slashing, task marketplace escrow and settlement, treasury management, issuance equilibrium controller. |
| **7. Governance and Constitutional Control** | Constitutional enforcement, policy parameter management, upgrade proposal and voting, reliance permits for high-risk heuristic families, access control, resource limits, audit trail maintenance, human oversight interfaces, emergency override protocols, membrane protection enforcement. |

---

## 8. System Architecture Overview

### 8.1 Six Planes

1. **Intent and Routing Plane** — CIOS compiles user goals into AASL operations carried by AACP envelopes and maps them to loci and parcels.
2. **Locus Router Plane** — Replicated parcel routers hold Locus State Objects, perform anti-entropy, maintain membership, issue local seriality for X-class operations, and track Capacity Slices.
3. **Cell Execution Plane** — Each hot parcel recruits a temporary locus cell. This preserves the Atrahasis tetrahedral motif: coordination, execution, verification liaison, and memory liaison roles.
4. **Artifact Plane** — Large artifacts are chunked, dispersed, certified, and retrieved separately from control traffic. Availability certificates are required before claims referencing artifacts can be verified.
5. **Verification Membrane** — Verichain committees evaluate claims by class and issue Membrane Certificates.
6. **Knowledge and Settlement Plane** — Knowledge Cortex stores admitted bundles and claim graphs. Settlement Plane handles AIC accounting, slashing, and governance checkpoints.

### 8.2 Three Cross-Cutting Systems

1. **Reputation Field** — Multi-dimensional reputation vector per agent reflecting: verification success rate, contribution volume, accuracy score, governance participation quality, anomaly history. Implements trained immunity: successful contributions strengthen reputation, failures weaken it. Reputation modifies future routing and trust.
2. **Bi-Timescale Controller** — Slow loop: parcelization changes based on conflict hypergraph analysis. Fast loop: PI controller for routing weights, replica fanout, worker placement. Circuit breaker, rollback records, and degradation mode provide defense-in-depth.
3. **Sentinel Graph** — Standing anomaly detection with formal typed edges. Collusion detection via verification affinity matrix. Regional bias detection via RVQI. Response escalation. Governance playbooks.

### 8.3 Core Invariants

- **No claim enters durable memory without passing the Verification Membrane.** This is the single most important invariant.
- **Hard consensus only where exclusivity, money, or constitutional authority requires it.**
- **Semantic loci split rarely. Parcels split and migrate often.**
- **Heuristic claims receive reliance permits, not truth certificates.**
- **The membrane cannot be weakened by any non-constitutional action.**

### 8.4 Dissemination Mesh

The communication substrate. Organized as a small-world gossip network aligned with the Atrahasis tetrahedral cluster topology but capable of dynamic reconfiguration. Within cells, all nodes communicate directly. Between cells, relay nodes exchange summaries and route signals by locus/parcel. Between regions, federation gateways synchronize. The resulting topology mirrors small-world neuroscience: dense local clusters with sparse global shortcuts.

**Routing inputs:** Locus/parcel tuple of the signal, capability vectors of available cells, current SLV and capacity of candidate cells.

### 8.5 Artifact Availability Plane

Large blobs do not move through the control fabric. Control messages carry references and availability certificates, not artifacts. Artifacts move through a namespaced availability layer with retrievability proofs (erasure coding), borrowing Narwhal/Celestia separation logic. Consumers fetch only what their namespace requires. Artifact availability certificates are required before claims referencing those artifacts can pass the verification membrane.

---

## 9. Locus and Parcel Model

### 9.1 The Decomposition

A **Locus** is a stable logical coordination domain defined by: invariant set, claim-family namespace, safety class, and access-control membrane. Loci are the correctness boundary. They split rarely (only on semantic grounds — structurally distinct sub-populations with minimal cross-reference; governance approval required for HIGH+).

A **Parcel** is an elastic physical execution unit within a locus: a hot object subset with active leases, a current replica set, and observed conflict/co-access statistics. Parcels split and migrate often (driven by the bi-timescale controller based on load, locality, and conflict patterns).

**Why this separation is critical:** Without it, the system constantly redraws its correctness boundaries under load. This is the most dangerous failure mode in any sharded distributed system — it creates cascading state migrations, invalidates active leases, disrupts in-progress capsules, and degrades verification throughput. The Locus/Parcel decomposition makes this structurally impossible by separating the stable correctness boundary (locus, rarely changes) from the elastic execution boundary (parcel, frequently changes).

### 9.2 Locus Lifecycle

`CREATED → ACTIVE → {SPLIT (rare, semantic) | MERGED (rare) | QUIESCENT → ARCHIVED}`

**Split criteria:** Sustained, structurally distinct sub-populations of claims and objects with minimal cross-reference. Governance approval required for HIGH+ safety class.

**Merge criteria:** Two sibling loci (same parent) both at minimal activity for sustained period.

### 9.3 Parcel Lifecycle

`CREATED → ACTIVE → {SPLIT | MIGRATED | MERGED | DISSOLVED}`

Driven by the bi-timescale controller's slow loop based on rolling access/conflict hypergraph analysis with hysteresis. See §30–32 for full controller specification and safeguards.

### 9.4 Locus State Object (LSO)

Each locus maintains a canonical replicated state decomposed by operation class:

```
LSO(L) = {
  meta:              locus identity, safety class, epoch
  merge_state:       M-class convergent state (signals, offers, needs, alerts)
  bounded_state:     B-class CSO balances and slice allocations
  exclusive_state:   X-class object versions + lease table
  claim_state:       claim families, contradiction lattice, canonical pointers
  heuristic_state:   heuristic families, argumentation graphs, reliance permits
  metrics_state:     load vectors, contention ratios, entropy measures
  recovery_state:    journal frontier, snapshot ref, witness seals
}
```

### 9.5 Scope Load Vector (SLV)

Per-parcel, six independently measurable dimensions:

```
SLV(parcel, t) = {
  pending_needs:    count of unmet need signals with remaining TTL > 0
  pending_claims:   count of claims awaiting verification
  dispute_count:    count of active contradictions between live claims
  lease_contention: count of lease requests blocked by held leases
  active_agents:    count of agents currently assigned to this parcel
  verification_lag: 95th percentile time from claim submission to verification completion
}
```

Each dimension has an independent **threshold** and **hysteresis band** to prevent oscillation:
```
For each dimension d:
  if SLV.d > threshold_high(d) → emit RECRUIT signal for capability matching d
  if SLV.d < threshold_low(d)  → emit RELEASE signal
  threshold_low(d) = threshold_high(d) × damping_factor (default 0.7)
```

**Cell assembly (deterministic):** When any SLV dimension crosses its high threshold and has remained above threshold for a configurable dwell time (default 5 seconds), the parcel broadcasts a RECRUIT signal specifying the needed capability class. Available agents with matching capability and sufficient Protocol Credits respond. The first N responding agents (default N=4 for the tetrahedral motif) form a cell.

**Cell dissolution:** When all SLV dimensions are below their low thresholds for a configurable cool-down period, the parcel emits a RELEASE signal and agents are freed to respond to other RECRUIT signals.

---

## 10. Replica Groups

Parcels are served by replica groups. Replica count is safety-class-dependent:

| Safety Class | Replicas (N) | Byzantine Tolerance (f) | Quorum Model |
|---|---|---|---|
| LOW | 3 | 0 (crash-fault only) | Simple majority |
| MEDIUM | 5 | 1 | BFT (N ≥ 3f+1) |
| HIGH | 7 | 2 | BFT |
| CRITICAL | 11 | 3 | BFT |

### 10.1 Replica Selection

Deterministic weighted random sampling seeded by `hash(parcel_id || epoch)`:

1. **Eligibility:** Only nodes with sufficient stake, reputation above minimum threshold, and available capacity (current SRG membership count below configurable maximum).
2. **Diversity constraints:** No more than `ceil(N/3)` replicas from the same physical cluster. No more than `ceil(N/2)` from the same availability zone. At least 2 distinct infrastructure providers (for MEDIUM+).
3. **Weighting:** `reputation × sqrt(stake)`.

### 10.2 Internal Protocol

**Signal writes (nonexclusive, M-class):** Any replica accepts; reliable broadcast within SRG. Eventually consistent. No leader required.

**Lease operations (exclusive, X-class):** Quorum of `ceil((N+1)/2)`. Lease coordinator designated by `hash(parcel_id || epoch) mod N`. Coordinator proposes; replicas vote. Coordinator failure → next replica in deterministic ordering.

**Bundle commits:** Quorum of `ceil((2N+1)/3)` for MEDIUM+ (BFT quorum). Simple majority for LOW. Initiated by Verification Membrane after claim passes verification.

### 10.3 Epoch-Based Reconfiguration

At each epoch boundary (configurable, default 1 hour):

1. Regional scope registry recomputes SRG membership using selection algorithm with new epoch as seed.
2. If membership differs, state transfer from outgoing to incoming replicas.
3. Transition window (default 30 seconds): both old and new configurations active, writes go to both.
4. After new configuration acknowledges receipt and is operational, old non-overlapping members released.

### 10.4 Reconfiguration During Active Operations

**Active prepare records (from SK-2PC or Fusion Capsule grants):** Included in state transfer with their original quorum certificates and TTLs. Incoming replicas inherit them. COMMIT after reconfiguration processed normally. Crashed initiators' prepare records auto-abort after TTL. COMMIT is idempotent.

**Active Fusion Capsules during epoch boundary:** Current capsule completes under old SRG configuration. Post-completion state transfers to new configuration.

**Invariant:** No prepare record is ever lost, duplicated with conflicting content, or orphaned without TTL-bounded auto-abort.

### 10.5 Byzantine Handling

**Equivocation:** Detected by cross-checking quorum certificates. Equivocating replicas reported to Sentinel Graph and slashed.

**Withheld responses:** Handled by coordinator timeout. Operation proceeds with remaining quorum.

**Invalid messages:** All messages are signed and schema-validated. Invalid messages discarded and sender reported.

**LOW class with discovered Byzantine behavior:** Scope can be promoted to MEDIUM safety class, triggering SRG reconfiguration with a larger replica set.

---

# PART IV — AGREEMENT AND COORDINATION

## 11. Operation-Class Algebra

Agreement mode is **derived from operation class**, not chosen ad hoc:

```
Given operation op:
  determine locus footprint F(op)
  determine class K(op)

  K = M → merge-converge
  K = B → local bounded commit (CSO)
  K = X → serial commit (single-parcel) or Fusion Capsule (multi-parcel)
  K = V → verifier committee protocol
  K = G → constitutional consensus
```

### 11.1 M-Class: Merge / Convergence

**When used:** Offers, needs, alerts, support edges, lineage references, most workflow metadata. The vast majority of all traffic.

**Mechanism:** Monotone or CRDT-like state updates. No immediate coordination beyond authenticated anti-entropy. Last-writer-wins per signal_id from same issuer; signals from different issuers coexist. Signals decay unless reinforced.

**Cost:** O(1) per signal. **Zero consensus overhead.** This handles the vast majority of traffic. Recent CRDT and invariant-confluence work confirms that many operations can converge or preserve invariants without always-on coordination.

### 11.2 B-Class: Bounded Local Commit (CSOs)

**When used:** Operations consuming bounded resources (compute, storage, bandwidth) where a conservation law holds.

**Mechanism:** Each parcel holds preallocated Certified Slice Object rights. Local decrement is valid iff all requested dimensions are available within the owned slice. No coordination required for local spend. Rebalancing happens asynchronously at epoch boundaries.

**CSO eligibility:** A resource may use CSOs only if: it has a conservation law or hard monotone bound, local operations can be expressed as monotone spend/consume/reserve within owned rights, merge semantics are proven safe, and the resource/invariant pair is shown to be I-confluent or reduced to a smaller X-class fallback.

**Cost:** Zero coordination for local spend. Periodic rebalancing cost at epoch boundaries. The amortized-coordination path.

### 11.3 X-Class: Exclusive Operations

#### Single-Parcel: Serial Commit

Parcel's replica group runs local serial agreement over exclusive state. Standard quorum vote.

#### Multi-Parcel: Fusion Capsules (Primary Path)

**No arbitrary multi-parcel X-class operation is allowed by default.** An X-class request must be reduced to one of three forms:
1. Single-parcel local execution
2. Certified Slice Object spend/transfer
3. Fusion Capsule

Only if all three fail does the system use **Cut Commit fallback**.

See §12 for the full Fusion Capsule Epoch Protocol.

#### Cut Commit (Last Resort Fallback)

Retained only as a reviewed escape hatch for operations that cannot be reduced to single-parcel, CSO, or Fusion Capsule. Canonical lock ordering by `locus_id`. PREPARE → COMMIT/ABORT. TTL-bounded prepare records. The system meters and audits Cut Commit usage. If it becomes common, the locus model is wrong and should be redesigned.

**Discipline:** Every new X-class type must prove it cannot be reduced to local execution, CSO semantics, or Fusion Capsule execution before Cut Commit is permitted.

### 11.4 V-Class: Verification-Gated Epistemic Agreement

Claim-class-specific verification through the membrane. See §13–22.

### 11.5 G-Class: Constitutional Consensus

**When used:** AIC settlement, treasury operations, slashing, protocol parameter changes, governance checkpoints, randomness beacon generation, membrane rule modifications.

**Mechanism:** BFT consensus among staked governance participants. 2/3 supermajority for standard governance. 75% supermajority for membrane rule changes. Discussion periods and activation delays.

This plane may use a conventional BFT ledger internally. That does not make AIChain a ledger again — it makes exact arithmetic a narrow subproblem.

---

## 12. Fusion Capsule Epoch Protocol (CEP)

### 12.1 State Machine Specification

**Per object `o`:**
```
ObjAuth[o] = {
  owner:             Identity          -- current authority holder
  auth_epoch:        Nat               -- monotonically increasing
  prepared_capsule:  CapsuleId ∪ {⊥}  -- at most one pending capsule
  install_frontier:  Nat               -- monotonically increasing
  last_commit_root:  Hash ∪ {⊥}       -- hash of last committed state
}
```

**Per capsule `c`:**
```
Capsule[c] = {
  capsule_id:    CapsuleId
  touched_set:   Set<ObjectId>
  exec_host:     NodeId
  grant_map:     ObjectId → (proposed_epoch: Nat, state_hash: Hash, expiry: Epoch)
  status:        {init, collecting, armed, executing, committed, installed, expired, aborted}
  expiry_epoch:  Epoch
}
```

### 12.2 State Transitions

**GrantRequest(o, c):**
```
Pre:
  ObjAuth[o].prepared_capsule = ⊥
  Capsule[c].status = collecting
  o ∈ Capsule[c].touched_set
  current_epoch < Capsule[c].expiry_epoch

Post:
  ObjAuth[o].prepared_capsule := c
  Capsule[c].grant_map[o] := (ObjAuth[o].auth_epoch + 1, hash(state(o)), Capsule[c].expiry_epoch)
```

**Arm(c):**
```
Pre:
  Capsule[c].status = collecting
  ∀ o ∈ Capsule[c].touched_set: o ∈ dom(Capsule[c].grant_map)
  current_epoch < Capsule[c].expiry_epoch

Post:
  Capsule[c].status := armed
```

**Execute(c):**
```
Pre:
  Capsule[c].status = armed
  current_epoch < Capsule[c].expiry_epoch

Post:
  Capsule[c].status := executing
  -- execution produces private_versions (not externally visible)
```

**Commit(c):**
```
Pre:
  Capsule[c].status = executing
  current_epoch < Capsule[c].expiry_epoch
  quorum_witness(commit_record(c)) = true

Post:
  Capsule[c].status := committed
```

**Install(o, c):**
```
Pre:
  Capsule[c].status = committed
  ObjAuth[o].prepared_capsule = c
  Capsule[c].grant_map[o].proposed_epoch = ObjAuth[o].auth_epoch + 1
  commit_record(c).install_seq > ObjAuth[o].install_frontier
  verify(commit_record(c), quorum_cert) = true

Post:
  ObjAuth[o].auth_epoch := ObjAuth[o].auth_epoch + 1
  ObjAuth[o].owner := new_owner_from(commit_record(c), o)
  ObjAuth[o].prepared_capsule := ⊥
  ObjAuth[o].install_frontier := commit_record(c).install_seq
  ObjAuth[o].last_commit_root := commit_record(c).delta_roots[o]
  Capsule[c].status := installed  (after all objects installed)
```

**Expire(c):**
```
Pre:
  current_epoch ≥ Capsule[c].expiry_epoch
  Capsule[c].status ∈ {collecting, armed, executing}

Post:
  ∀ o ∈ Capsule[c].touched_set:
    if ObjAuth[o].prepared_capsule = c:
      ObjAuth[o].prepared_capsule := ⊥
  Capsule[c].status := expired
```

**Abort(c):**
```
Pre:
  Capsule[c].status ∈ {collecting, armed}

Post:
  ∀ o where ObjAuth[o].prepared_capsule = c:
    ObjAuth[o].prepared_capsule := ⊥
  Capsule[c].status := aborted
```

### 12.3 Formal Invariants (Must Be Proved)

**Invariant 1: No Double Authority**
```
∀ o, c1, c2: (ObjAuth[o].prepared_capsule = c1 ∧ ObjAuth[o].prepared_capsule = c2) → c1 = c2
```
At most one capsule can hold a prepared grant per object at any time.

**Invariant 2: Monotone Authority Epoch**
```
∀ o: ObjAuth[o].auth_epoch is non-decreasing over time
     ∧ Install(o, c) → ObjAuth[o].auth_epoch' = ObjAuth[o].auth_epoch + 1
```

**Invariant 3: No Stale Install**
```
∀ o, c: Install(o, c) →
  Capsule[c].grant_map[o].proposed_epoch = ObjAuth[o].auth_epoch + 1
  ∧ commit_record(c).install_seq > ObjAuth[o].install_frontier
```

**Invariant 4: No Early Visibility**
```
∀ o, c: Capsule[c].status ∈ {collecting, armed, executing} →
  state(o) = state_before_capsule(c)
```

**Invariant 5: Idempotent Recovery**
```
∀ o, c: Capsule[c].status = committed →
  Install(o, c) applied twice produces the same ObjAuth[o] state
```

**Invariant 6: Expiry Safety**
```
∀ o, c: Expire(c) →
  ObjAuth[o].auth_epoch unchanged ∧ ObjAuth[o].owner unchanged
```

### 12.4 Byzantine Defenses

**Defense 1: Grant Freshness Enforcement.** A Byzantine parcel owner cannot issue a grant with a stale state hash. The grant's `state_hash` field must match the object's current state as witnessed by the SRG quorum. The granting process requires: (1) grantor proposes grant to SRG, (2) SRG quorum verifies state_hash matches current state, (3) only if quorum agrees does the grant receive a quorum certificate, (4) capsule exec host verifies the quorum certificate before accepting. A Byzantine grantor cannot forge a stale grant because the honest majority of the SRG will not certify a non-matching hash.

**Defense 2: Exec Host Output Verification.** A Byzantine exec host may produce incorrect delta_roots. For MEDIUM+ safety classes, the commit record must be witnessed by the exec host's SRG, and the SRG performs execution re-verification: at least f+1 SRG members independently re-execute the capsule's operation on the granted state snapshots. The quorum certificate on the commit record is issued only if 2f+1 members agree on the delta_roots. LOW safety class is exempt (post-hoc auditing only).

**Defense 3: Delayed Commit Propagation Handling.** If a partition delays commit record propagation and grants expire, a **late install** protocol is available: the initiator retains the commit record and, after partition heals, submits a late install request. The granting parcels check: if `auth_epoch` has not advanced since the grant, the install is accepted. If the epoch has advanced (another capsule modified the object during partition), the late install is rejected and the initiator retries with a new capsule.

**Defense 4: Partition-Induced Double-Grant Prevention.** BFT quorum prevents minority-partition grants: the minority alone cannot reach quorum. For exact quorum splits, grants from both partitions are compared after reconnection. The grant with the lower `capsule_id` wins (deterministic tiebreak). The losing capsule is aborted.

**Defense 5: Capsule Frequency Monitoring.** The Sentinel Graph monitors capsule frequency per locus. Warning at > 10 capsules/epoch/locus. Rate-limited at > 50/epoch/locus with governance notification. High capsule frequency is a symptom of locus model problems, not something to optimize.

### 12.5 TLA+ Model Checking Plan

1. Encode the state machine in TLA+. Model check for all 6 invariants under ≤ 3 concurrent capsules, 5 objects, and 3 epochs (bounded model checking).
2. Add Byzantine fault injection (double grants, stale installs, delayed commits, premature expiry). Verify invariants hold for honest majority.
3. Under weak fairness (every enabled action eventually executes), verify every capsule eventually reaches `installed`, `expired`, or `aborted`. No capsule remains in `collecting`, `armed`, or `executing` forever.
4. **Timeline:** TLA+ model and initial model checking complete within Phase 2 (months 6–12). Stronger machine-checked proofs (Coq/Ivy) recommended for Phase 3 but not blocking prototype.

---

# PART V — THE VERIFICATION MEMBRANE

## 13. Verification Membrane Overview

The Verification Membrane is the heart of the Noosphere and the civilizational bottleneck. It is the gate between provisional output and durable knowledge. Every downstream property — model improvement, agent trust, knowledge graph quality, governance legitimacy, reward fairness, safety of recursive self-improvement — depends on the membrane being correct.

A bad controller wastes compute. A bad membrane poisons cognition. Epistemic corruption compounds through the knowledge graph in ways that are much harder to detect than performance degradation — the system may continue functioning while quietly building on wrong assumptions. That is how a high-functioning system becomes subtly self-delusional.

### Constitutional Protection

The membrane is constitutionally protected:

1. No system parameter may be adjusted in a way that reduces membrane verification depth, widens admission thresholds, or relaxes class-specific rules — regardless of throughput pressure, economic incentive, or governance convenience.
2. Any such adjustment requires G-class constitutional consensus with a 72-hour discussion period and a 75% supermajority (higher than the standard 67% for other governance actions).
3. The membrane's admission standards are monotonically non-decreasing within a safety class unless explicitly revised by this constitutional process.

This is encoded as an immutable rule in the system constitution. The Feedback Controller, the Homeostat, and the economic system are explicitly prohibited from adjusting membrane parameters. Only G-class governance can touch them.

---

## 14. Claim Classification Gate

Every claim submitted to the membrane must pass through a Classification Gate before entering any verification pathway. The Classification Gate is a separate subsystem from the verification pipeline — it runs before verification begins.

### 14.1 Four-Step Classification Protocol

**Step 1: Issuer self-classification.** The submitting agent declares the claim class in the `claim_class` field of the CLM object. This is the starting point, not the final determination.

**Step 2: Structural classification check.** The Classification Gate applies deterministic rules based on the claim's structure:

| Structural Feature | Required Class | Override Rule |
|---|---|---|
| Contains formal proof or proof reference | `deterministic` | If issuer declared otherwise, reclassify to `deterministic`. |
| Contains replication instructions and benchmark references | `empirical` | If issuer declared `deterministic` without proof, downgrade to `empirical`. |
| Contains confidence intervals, p-values, or distribution parameters | `statistical` | If issuer declared `deterministic` or `empirical` without matching evidence, reclassify. |
| Contains argumentation references, assumption declarations, or judgment-based reasoning | `heuristic` | If issuer declared `empirical` or `statistical` without matching evidence, reclassify. |
| Contains policy proposals, value judgments, or governance recommendations | `normative` | Always requires governance ratification regardless of issuer declaration. |

**Step 3: Independent classification verifier.** For MEDIUM+ safety classes, the Classification Gate assigns one independent agent (selected by sortition, distinct from the claim's verification committee) to confirm or challenge the classification. If the independent classifier disagrees with the structural check, the claim is escalated to a classification panel of 3 agents. Majority rules.

**Step 4: Classification Seal (CLS).** The final classification is recorded in a Classification Seal attached to the claim. Once sealed, the classification cannot be changed except by re-submission of the claim as a new claim with a different classification. This prevents post-hoc reclassification to avoid verification requirements.

### 14.2 Mixed-Type Claim Handling

Some claims genuinely span multiple classes (e.g., an empirical finding with a heuristic interpretation). The Classification Gate handles this by requiring the claim to be **decomposed** into sub-claims, each with a single class. The empirical component is submitted as a separate claim with class `empirical`. The heuristic interpretation is submitted as a separate claim with class `heuristic`, with a causal_parent link to the empirical claim. Each sub-claim goes through its appropriate verification pathway independently.

If the submitting agent refuses to decompose, the entire claim is classified at the **most restrictive** class (the class requiring the most stringent verification). A claim containing any heuristic component is classified as `heuristic`. A claim containing any normative component is classified as `normative`.

---

## 15. Verifier Selection: Orthogonal Sortition with Stratified Capability Sampling

### 15.1 Combined Selection Protocol

1. Determine claim family and safety class.
2. Identify required **capability classes** for this claim type (e.g., a protein-folding claim might need: replication-capable, domain-expert-biology, statistical-analysis-capable).
3. Use epoch randomness plus claim hash for VRF self-selection (Algorand-style cryptographic sortition).
4. Enforce **orthogonality constraints** across: operator, model family, training provenance, region, and infrastructure provider. No committee may be dominated by one correlated-failure domain.
5. For each required capability class, sample K verifiers (default K=2) weighted by `reputation × sqrt(stake)` (square root to prevent pure plutocratic control).
6. No two verifiers from the same cluster. At least two distinct model lineages.
7. Assign verifier roles: replication, audit, adjudication.
8. **Escalation:** If initial verifier scores disagree (standard deviation > 0.3), double the verifier set by sampling additional verifiers from different regions than the originals.

### 15.2 Deep Diversity Enforcement

**Rule 1: Training data lineage diversity.** For MEDIUM+ safety classes, at least 2 verifiers must have declared distinct training data lineages (verified by the identity registry's `training_hash` field). Verifiers whose lineage is unknown or undeclared are counted as a single lineage — they cannot fill the diversity requirement.

**Rule 2: Temporal diversity.** For HIGH+ safety classes, the committee must include at least one verifier whose model was trained or fine-tuned within the last 6 months and at least one whose model has been stable for more than 6 months. This prevents dominance by either cutting-edge models (new biases) or legacy models (old biases).

**Rule 3: Methodology diversity.** The committee must include verifiers using at least 2 distinct verification methods (from: replication, cross_reference, logical_check, statistical_analysis, human_review). A committee using only replication may miss logical flaws; one using only logical checks may miss empirical errors.

**Rule 4: Anti-correlation audit.** The Sentinel Graph maintains a verification agreement matrix V[i][j] = the fraction of claims where verifiers i and j agreed on the score (within ±0.1). If V[i][j] > 0.95 for 50+ epochs, the pair is flagged as potentially correlated. Flagged pairs are prohibited from serving on the same committee until correlation drops below 0.85.

### 15.3 Stake-Quality Balance

No single verifier's weight may exceed 15% of the total committee weight. If a high-stake, high-reputation verifier would exceed 15%, their weight is capped and the surplus redistributed to other committee members.

---

## 16. Claim-Class-Specific Promotion

### 16.1 Deterministic Claims

**Promotion by:** Proof, exact replay, formal checker, invariant validation.
**Status → canonical.**

### 16.2 Empirical Claims

**Promotion by:** Rerun, benchmark replication, cross-provider replication, statistical acceptance thresholds.
**Status → empirically canonical.**

### 16.3 Statistical Claims

**Promotion by:** Declared distribution, confidence interval, power/sample-size requirements, proper-score history.
**Status → calibrated canonical** for a stated horizon/context, not universal truth.

### 16.4 Heuristic Claims

**Promotion by:** Support/attack graph (argumentation semantics), dependency graph, challenge history, calibration history if delayed truth exists, operational utility in a defined context.
**Status → operational canon** (never timeless canon). See §17.

### 16.5 Normative Claims

Not canonicalized by Verichain alone. **Requires governance ratification.**
**Status → ratified** by governance vote.

### 16.6 Verification Scoring

```
V(claim) = Σ(attestation_score × attester_reputation × method_weight) 
           / Σ(attester_reputation × method_weight)
```

A claim crosses the membrane when:
- V(claim) exceeds the scope-specific verification threshold.
- At least the minimum number of independent attestations have been collected.
- Supporting evidence and artifacts have availability certificates.
- At least one verifier has confirmed evidence relevance.

### 16.7 Epistemic Finality (Revocable)

All verified claims have **revocable epistemic finality** through supersession. Heuristic claims additionally have expiring reliance permits. The membrane answers different questions for different claim classes:
- Deterministic/empirical: "Is this reproducibly true?"
- Statistical: "Is this well-calibrated for this context?"
- Heuristic: "What should the system rely on right now, with explicit uncertainty?"
- Normative: "Has governance approved this?"

---

## 17. Contestable Reliance Membrane for Heuristic Claims

### 17.1 Two Separate Axes

**TruthStatus:** `submitted | admissible | preferred | contested | retired`
**RelianceStatus:** `sandbox | advisory | bounded_operational | ratified`

### 17.2 Mandatory Escalation Ladder

Heuristic families must progress through reliance levels sequentially, with minimum dwell times at each level. No level may be skipped.

```
sandbox           →  advisory          →  bounded_operational  →  ratified
  (entry)         (min 10 epochs)      (min 50 epochs)        (governance only)
                  requires:             requires:               requires:
                  - 3+ support edges    - all advisory reqs     - all bounded reqs
                  - 0 unresolved        - 20+ epochs stable     - governance vote
                    attack edges          champion              - human review
                  - 2+ distinct         - calibration > 0.6     - safety assessment
                    supporters            (if outcome data)     - 75% supermajority
                                        - < 3 revoked prior
                                          permits for family
```

**Three-revocation rule:** A family that has had 3 or more Reliance Permits revoked in its lifetime cannot reach `bounded_operational` again without governance ratification (permanently escalated to requiring human approval).

### 17.3 Reliance Propagation Tags (RPT)

Any downstream claim, plan, routing decision, or resource allocation that depends on a heuristic claim must carry a Reliance Propagation Tag recording: source family, reliance status, permit reference, propagation depth, and max permitted depth.

**Propagation depth limit:** A heuristic reliance may propagate through at most `max_permitted_depth` layers of downstream claims (default 5). Beyond that, the downstream claim must either obtain independent verification or be classified as heuristic itself.

**Visibility rule:** The RPT must be visible to any agent querying the knowledge graph. A downstream consumer must be able to determine that a result depends on a heuristic claim with bounded operational reliance, not on empirically verified truth. This prevents the silent laundering of heuristic uncertainty into apparent certainty through citation chains.

### 17.4 Promotion by Evidence Regime

| Evidence Regime | Promotion Path |
|---|---|
| **Outcome-rich** | Scoring, calibration, replication → may reach `bounded_operational` automatically, `ratified` by policy. |
| **Reference-rich / outcome-poor** | Label-free recalibration as advisory ranking aid → `advisory` or `bounded_operational` with short TTL if argument strength margin high and challenge activity low. |
| **Outcome-free / normatively contested / high-stakes** | No automatic operational canon. May become `preferred` epistemically, but reliance above `advisory` requires governance/human ratification. |

### 17.5 Key Rules

- `bounded_operational` must always expire (non-deferrable sunset). The family must re-demonstrate support/attack balance, calibration, and utility for re-issuance.
- Any accepted attack edge or invalidated assumption → automatic downgrade to `advisory`.
- High-risk families cannot bypass human/governance ratification.
- If delayed truth arrives, the family can be reclassified into the outcome-rich lane and scored normally.

---

## 18. Supersession Protocol

A verified claim C_new may supersede an existing verified claim C_old only if ALL of the following conditions are met:

1. **Score superiority:** V(C_new) > V(C_old) by at least `supersession_margin` (default 0.1, configurable per safety class). A marginal improvement is insufficient.

2. **Evidence breadth:** C_new's evidence set must be at least as broad as C_old's. Breadth is measured by the number of distinct evidence types (datasets, replications, cross-references, logical proofs) and the number of distinct sources. A claim supported by a single proof cannot supersede one supported by multiple independent lines unless the proof covers all cases.

3. **Validity scope:** C_new's declared validity scope must be at least as wide as C_old's. A claim valid for a narrow context cannot supersede a claim valid for a broad context. Narrower scope → coexistence, not supersession.

4. **Challenge window:** Before supersession takes effect, C_old is given a challenge window (configurable: 24 hours for LOW, 72 hours for MEDIUM, 168 hours for HIGH, 336 hours for CRITICAL). Supporters of C_old may submit new evidence or attack edges against C_new. If C_new's score drops below C_old's during the window, supersession is cancelled.

5. **Independent supersession verifier:** For HIGH+ safety classes, supersession requires approval by at least one verifier who was not on the original committee for either C_new or C_old.

Produces a SUP record documenting all check results.

---

## 19. Membrane Drift Detection

### 19.1 Membrane Quality Index (MQI)

The Sentinel Graph maintains a rolling measurement of membrane admission behavior:

| Metric | Description | Healthy Range | Alert Threshold |
|---|---|---|---|
| **Mean attestation time** | Average time verifiers spend per attestation | > 30 seconds (domain-dependent) | < 10 seconds (rushing) |
| **Attestation score variance** | Std dev of scores within committees | 0.05–0.25 | < 0.02 (rubber-stamping) |
| **Rejection rate** | Fraction of claims rejected | 5%–30% (domain-dependent) | < 2% (too permissive) |
| **Escalation rate** | Fraction triggering verifier escalation | 5%–15% | < 1% (missing disagreements) |
| **Evidence relevance confirmation rate** | Fraction with explicit relevance confirmation | > 80% | < 50% (skipping checks) |
| **Supersession challenge rate** | Fraction of supersessions challenged | > 10% | < 2% (unchallenged) |

### 19.2 Response Tiers

**Mild drift (1–2 metrics in alert for 10 epochs):** Warning logged to governance dashboard. Affected loci flagged for monitoring.

**Moderate drift (3+ metrics in alert for 10 epochs, or any metric alert for 50 epochs):** Membrane enters **conservative mode** for affected loci: verification depth increased by 1 tier, minimum committee size increased by 2, claim throughput cap imposed (max claims per epoch reduced by 50%). Conservative mode persists until all metrics return to healthy range for 20 epochs.

**Severe drift (rejection rate < 1% for 30 epochs, or mean attestation time < 5 seconds for 30 epochs):** Membrane enters **lockdown** for affected loci: all new claim admissions paused, backlog of recently admitted claims (last 50 epochs) flagged for re-verification, governance alert with mandatory response within 10 epochs. Lockdown lifted only by G-class 75% supermajority governance action.

**Immutable rule:** Conservative mode and lockdown are triggered automatically by the Sentinel Graph. They cannot be overridden by the Feedback Controller, the economic system, or any non-constitutional governance action.

---

## 20. Continuous Re-Verification

The membrane does not only verify new claims. It continuously re-verifies a random sample of existing verified knowledge.

### 20.1 Protocol

Each epoch, the membrane selects a random sample of `r` verified claims from the knowledge graph (r = 0.1% of total verified claims, minimum 10, maximum 1000 per epoch). Selected claims are re-submitted to the current verification pipeline with the current committee (not the original committee), using current verification standards, current verifier pool, and current evidence availability.

### 20.2 Citation-Weighted Priority

The sample is not uniformly random. Claims are weighted by citation count: `weight(claim) = 1 + log2(1 + citation_count)`. High-citation claims are sampled more frequently because their corruption would affect more of the knowledge graph.

### 20.3 Failed Re-Verification

If a re-verified claim fails: status → `under_review`. All downstream claims with RPTs are updated with a warning flag. If confirmed invalid after full re-review → `superseded` and correction bundle issued.

If the current Classification Gate would assign a different class than the claim's sealed classification → flagged for classification review and re-routed through the appropriate pathway.

---

## 21. Membrane Implementation Constraints

### 21.1 Performance Must Not Compromise Quality

- **No batched verification.** Each claim is verified individually by its committee. Claims are not batched for efficiency. This prevents rubber-stamping.
- **No adaptive threshold reduction.** The Feedback Controller is prohibited from reducing verification thresholds, committee sizes, or verification depth. It may increase them but never decrease.
- **No timeout-based admission.** If verification takes longer than expected, the claim waits. No "admit after timeout" mechanism. Claims that cannot be verified in reasonable time are deferred or rejected — never admitted by default.
- **Verification is not a cost center.** Verification costs (compute, verifier rewards) are funded from the system's AIC treasury, not from the submitting agent's Sponsor Budget. This prevents economic pressure from discouraging verification depth.

### 21.2 Membrane Versioning

Every membrane parameter set (thresholds, committee sizes, classification rules, supersession margins) is versioned and recorded in the governance state as an MBV record. Every Membrane Certificate records the membrane version under which it was issued. This allows retrospective auditing: if a membrane version is later found to be too permissive, all claims admitted under that version can be identified and flagged for re-verification.

---

## 22. Complete Membrane Failure Mode Coverage

### A. Claim Classification Failures

| Failure Mode | Defense |
|---|---|
| Heuristic misclassified as empirical | Structural classification check + independent classifier (§14) |
| Statistical misclassified as deterministic | Structural check requires proof reference for deterministic (§14) |
| Normative admitted without governance | Always requires governance ratification (§14) |
| Mixed-type routed wrong | Mandatory decomposition or most-restrictive default (§14.2) |
| Wrong safety class | Safety class is a locus property, inherited by claims (§9) |

### B. Verifier Selection Failures

| Failure Mode | Defense |
|---|---|
| Lacks capability diversity | SCS mandatory per-class K (§15.1) |
| Hidden correlated verifiers | Anti-correlation audit, V[i][j] > 0.95 → flagged (§15.2 Rule 4) |
| Same model lineage dominates | Training data lineage diversity (§15.2 Rule 1) |
| Regional concentration | Orthogonal Sortition region constraint + escalation (§15.1) |
| Stake overwhelms quality | 15% weight cap per verifier (§15.3) |

### C. Evidence and Provenance Failures

| Failure Mode | Defense |
|---|---|
| Weak evidence accepted | Evidence relevance confirmation required in attestation (§16.6) |
| Incomplete provenance | Connected subgraph check back to root or verified bundle |
| Stale artifact certificate | 2-epoch freshness requirement with re-challenge |
| Irrelevant evidence | Explicit relevance confirmation by verifier |
| Missed contradiction | Contradiction scan root in membrane certificate |

### D. Deterministic/Empirical Verification Failures

| Failure Mode | Defense |
|---|---|
| Replay on wrong input | Artifact freshness + provenance completeness |
| Shared hidden bug | Training data lineage + methodology diversity (§15.2) |
| Too-narrow benchmark | Evidence breadth check in supersession (§18) |
| Reproducible but invalid | Continuous re-verification catches drift (§20) |
| Brittle supersedes robust | Full supersession protocol with 5 conditions (§18) |

### E. Statistical Verification Failures

| Failure Mode | Defense |
|---|---|
| Insufficient power accepted | Statistical pathway requires power/sample declaration (§16.3) |
| In-sample calibration gaming | Re-verification with current out-of-sample data (§20) |
| Invalid distributional assumptions | Challenge mechanism in argumentation graph |
| Conservative forecasting gaming | Proper scoring rules reward sharpness + calibration (§16.3) |
| Overly broad horizon/context | Validity scope check in supersession + RPT depth limit (§17.3, §18) |

### F. Heuristic Membrane Failures

| Failure Mode | Defense |
|---|---|
| Premature bounded_operational | Mandatory escalation ladder with dwell times (§17.2) |
| Unstable champion | Stability monitoring + freeze on rapid cycling (§36.3) |
| Permit persists despite drift | Automatic revocation on invalidated assumption (§17.5) |
| Revocation lag | Low-threshold revocation: single valid challenge suffices (§17.5) |
| Advisory used operationally | RPT tags propagate reliance status through chains (§17.3) |
| Rubber-stamp ratification | Multi-stakeholder approval + reputation tracking (§36) |
| Unjustified trust accumulation | Non-deferrable permit sunset + re-evaluation (§17.5) |

### G. Argumentation and Contradiction Failures

| Failure Mode | Defense |
|---|---|
| Support-edge flooding | Staked evidence: PC burned on unfounded edges (§36.1 Rule 1) |
| Attack-edge spam | PC cost + exclusion for persistent spam (§36.3) |
| Dense lattice hides conflict | Bounded-time resolution + human escalation at HIGH |
| Preferred-set bias | Minimum supporter diversity: 3+ independent agents (§36.1 Rule 4) |
| Assumption invalidation too easy/hard | Verified through V-class for their own class (§36.1 Rule 2) |

### H. Governance Capture

| Failure Mode | Defense |
|---|---|
| Small coalition dominates | Approver concentration monitoring + expanded set on flag (§36.3) |
| Weak penalties | Governance reputation tracking with weight reduction (§36.1 Rule 8) |
| Emergency freeze abuse | Accountability: weight reduction after 3 unratified freezes (§36.5) |
| Sunset becomes formality | Non-deferrable expiry + re-evaluation from scratch (§17.5) |
| Political override | Constitutional 75% supermajority for any membrane change (§13) |

### I. Incentive Failures

| Failure Mode | Defense |
|---|---|
| Reward favors admissibility | Calibration-weighted rewards + citation utility (§36.1 Rule 9) |
| Agents optimize admissibility | Continuous re-verification catches wrong claims (§20) |
| Verifiers optimize consensus | Score variance monitoring detects rubber-stamping (§19) |
| Under-incentivized challenges | Challenge rewards from AIC treasury (§21.1) |
| Over-challenging profitable | PC cost for challenges + reputation penalty for rejected (§36.1 Rule 1) |

### J. Drift and Scaling Failures

| Failure Mode | Defense |
|---|---|
| Thresholds degrade under pressure | MQI + conservative mode + lockdown (§19) |
| High-volume domains weaker | MQI tracked per locus, independent drift detection |
| Cross-region divergence normalized | RVQI divergence trend + periodic calibration (§33) |
| Latency pushes shortcuts | No timeout admission, no batched verification (§21.1) |
| Canonical memory outgrows audit | Re-verification sampling, citation-weighted (§20) |

---

# PART VI — KNOWLEDGE PERSISTENCE

## 23. Four-Tier Memory Model

| Tier | Contents | Durability | Growth Driver |
|---|---|---|---|
| **Field Memory** | Decaying signals, SLV, active leases | Ephemeral (decays) | Active traffic. Bounded by decay. |
| **Workspace Memory** | Cell-local provisional artifacts, reasoning-in-progress | Volatile (destroyed with cell) | Active cells. Bounded by lifecycle. |
| **Verified Memory** | Admitted bundles with membrane certificates. The knowledge graph. | Durable (Merkle-anchored, witness-sealed) | K (verified bundles). K ≪ M. |
| **Canonical Memory** | Distilled blueprints, policies, reusable decompositions, long-lived world models | Highly durable (max replication) | Distilled knowledge. Very slow growth. |

Only Verified and Canonical Memory are system memory in the strong sense. Storage grows with **verified useful knowledge**, not transient coordination chatter.

Knowledge graph is partitioned by locus. Cross-locus edges maintained by coordination cells at boundaries. Artifact availability is namespaced and scope-retrievable with separate availability from execution/settlement.

---

## 24. Contradiction Lattice and Argumentation

Bipartite graph within each locus linking conflicting claims. Extended with argumentation semantics for heuristic families: support edges, attack edges, assumption tracking. Preferred extensions computed using Dung's framework (preferred extensions always exist even when stable extensions may not).

**Contradiction detection protocol:** When a new claim contradicts existing verified claim:
1. New claim tagged as `disputed` and linked via contradiction edge.
2. Verification depth automatically increased for both claims.
3. Evidence weight tracked: `weight(claim) = Σ(evidence_score × evidence_reputation)`.
4. If new claim achieves higher score and evidence weight → old claim transitions to `superseded` (via §18 supersession protocol).
5. If neither dominates after configurable timeout → both remain `disputed` (human review for HIGH+, coexist as provisional for LOW).

---

## 25. Bundle Compaction

**Semantic Subsumption Compaction:** Within a locus, periodically identify bundles where a stronger claim A logically subsumes weaker claims B and C. Create compacted bundle with A, supersession edges to B and C. B and C demoted to Archived tier (not deleted — epistemic history preserved).

**Eligibility:** All constituent claims verified, subsuming claim score ≥ constituent scores, no new contradiction edges created, approved by at least one verification agent.

---

# PART VII — RESOURCES AND ECONOMICS

## 26. Three-Budget Resource Model

The monolithic APV is replaced by three separate resources that do not conflate payment, spam control, and capacity reservation:

| Budget | Purpose | Transferable | Decays |
|---|---|---|---|
| **Sponsor Budget (SB)** | AIC-denominated escrow for actual compute, storage, settlement. The payment layer. | Yes (AIC) | No |
| **Protocol Credits (PC)** | Non-transferable, per-identity control-plane rate budget. Consumed by signal emissions, lease requests, challenge requests, routing. Prevents spam. | No | Yes (10%/epoch) |
| **Capacity Slices (CS)** | Locus-local rights over scarce shared resources: GPU-minutes, verifier slots, durable storage bandwidth. Implemented as Certified Slice Objects. | Transfer via CSO protocol | Rebalanced at epoch |

**PC issuance:** Per epoch, based on `f(stake, reputation)` (concave — diminishing returns from stake alone). Bonus from verified bundles.

**PC issuance equilibrium:** Global feedback controller maintains `total_PC_issued / total_PC_consumed ≈ 1.0–1.2`. Rate-limited to 5% adjustment per epoch.

**Why three budgets:** IOTA 2.0 made monolithic access control (Mana) look attractive, but the project later accepted that a single secondary access asset is operationally dangerous. Three budgets ensure: payment is separate from spam control is separate from capacity reservation. Each tuned independently. Gaming one does not automatically affect others.

---

## 27. Certified Slice Objects

### 27.1 Definition

```
CSO = <resource_type, total_supply, alloc[authority], pending_transfers, spent_frontier, epoch, proof_hash>
```

### 27.2 Safety Invariants (Must Be Proved)

1. **Conservation:** `Σ alloc + Σ pending_out - Σ pending_in + spent = total_supply`
2. **Local non-negativity:** `alloc[a] >= 0` for every authority
3. **No double-spend:** Spend records uniqueness-protected by nonce/frontier
4. **Transfer linearity:** A transfer is claimed once or expires and is reclaimed
5. **Deterministic merge:** Settled state is associative, commutative, idempotent

### 27.3 Eligibility Rule

A resource may use CSOs only if ALL of the following are true: the resource has a conservation law or hard monotone bound, local operations can be expressed as monotone spend/consume/reserve within owned rights, merge semantics are proven safe, and the resource/invariant pair is shown to be I-confluent or reduced to a smaller X-class fallback.

### 27.4 Protocol Discipline

- Local consume is coordination-free only within currently owned slice rights.
- Slice transfer is an explicit protocol with signed transfer tickets and TTL.
- Epoch reconciliation is separate from local spending.
- Byzantine replicas may disseminate lies, but correct replicas only adopt transfers satisfying CSO proof obligations and authenticity rules.

### 27.5 Required Proof Stack

TLA+ model for transfer/expiry/reclaim. Machine-checked state proof recommended. Randomized fault injection against replay, duplication, delayed reclaim. Explicit reduction from each CSO type to its declared invariant.

---

## 28. Scope Attention Market

Loci can bid for attention using Protocol Credits (attention class). Each locus publishes its SLV and an attention bid. Agents preferentially respond to RECRUIT signals from loci with higher bids. Bids deducted from the locus's PC pool. Aggressive bidding drains the pool — self-limiting.

---

## 29. Economic Simulation Specification

### 29.1 Agent Behavioral Strategies

| Strategy | Description | Expected Outcome |
|---|---|---|
| **Honest worker** | Produces genuine claims, earns rewards, spends PC on operations. | Sustainable: PC replenished, AIC earned. |
| **Free-rider** | Consumes PC for signal spam without producing verified work. | PC exhausted. No AIC reward. Self-limiting. |
| **Sybil farmer** | Creates many low-stake identities to farm baseline PC issuance. | Concave issuance: many identities yield negligible PC each. Net loss from identity maintenance. |
| **Colluder pair** | Two agents verify each other's claims to earn AIC. | Detected by Sentinel Graph affinity matrix. Reputation halved. AIC clawed back via slashing. |
| **CS hoarder** | Acquires large CS allocation and sells access at monopoly prices. | CS rebalanced at epoch boundaries. Excess reclaimed. No persistent monopoly. |
| **SB manipulator** | Submits high-value tasks, controls performing agents, recaptures SB. | Membrane catches low-quality work. MCT requires independent verifiers. Self-verification blocked by sortition orthogonality. |

### 29.2 Simulation Scenarios (E1–E7)

| # | Scenario | Agents | Epochs | Purpose |
|---|---|---|---|---|
| E1 | Baseline honest economy | 1,000 honest, 100 requesters | 500 | Equilibrium convergence |
| E2 | 10% sybil attackers | 900 honest, 100 sybil | 500 | Sybil resistance |
| E3 | 5% colluder pairs | 950 honest, 25 colluder pairs | 500 | Collusion detection |
| E4 | 10× demand shock on one locus | 1,000 honest, spike at epoch 100 | 300 | CS reallocation speed |
| E5 | Wealth concentration | 1,000 with Pareto initial stake | 1,000 | Gini coefficient stability |
| E6 | PC exhaustion cascade | 800 honest, 200 high-activity | 500 | Controller response to cascade |
| E7 | Mixed adversarial | 700 honest, 100 sybil, 50 colluder pairs, 50 free-riders | 1,000 | Combined adversarial |

### 29.3 Acceptance Criteria

| Criterion | Threshold | Scenarios |
|---|---|---|
| PC issuance ratio convergence | [0.9, 1.3] by epoch 50, stable | E1, E4, E6 |
| Sybil profitability | Sybil avg AIC < honest avg AIC | E2, E7 |
| Collusion detection time | Mean < 50 epochs | E3, E7 |
| Colluder net reward | Colluder avg AIC < honest avg (after slashing) | E3, E7 |
| Wealth Gini coefficient | Increase < 0.05 per 500 epochs | E5 |
| CS starvation | < 1% of parcels below 80% demand for > 5 epochs | E4 |
| PC cascade recovery | Controller restores within 10 epochs | E6 |
| Honest agent dominance | Honest > 1.5× adversarial avg AIC in E7 | E7 |
| System throughput | Adversarial reduces < 15% vs E1 | E7 |

### 29.4 Deployment Gates

- **Phase 1** (≤100 agents): Fixed PC. Simulated SB. No economic sim required.
- **Phase 2** (≤10K agents): E1 + E2 must pass. PC controller active. Testnet AIC.
- **Phase 3** (≤1M agents): E1–E6 must pass. Full economic simulation. Mainnet AIC.
- **Phase 4** (planetary): E1–E7 must pass. Continuous production monitoring.

---

# PART VIII — CONTROL AND SELF-REGULATION

## 30. Bi-Timescale Controller

### 30.1 Slow Loop: Parcel Placement

Operates on windowed access/conflict hypergraph. Changes parcelization only when candidate plan beats current plan by margin exceeding migration debt and churn budget.

**Objective function:**
```
J(P) = w1·remote_X_rate + w2·queue_delay + w3·verifier_spillover
     + w4·migration_bytes + w5·parcel_churn + w6·recovery_surface
```

**Guards:** No active capsule on affected parcel. No open X-class lease on affected object set. `parcel_lifetime >= τ_min`. `repartition_rate <= β`. `predicted_gain >= θ_enter` for k consecutive windows. Rollback only at epoch boundary.

**Shadow planning:** Every candidate parcel plan runs in route-only simulation for n windows before any data moves. If shadow plan's estimated J(P') degrades or variance increases, plan discarded.

### 30.2 Fast Loop: PI Controller

Per-parcel, adjusts routing weights, replica fanout, and worker placement without changing parcel boundaries.

```
error(t) = target - measured
integral(t) = clamp(integral(t-1) + error(t)·dt, -integral_max, +integral_max)
adjustment(t) = Kp·error(t) + Ki·integral(t)
P(t+1) = clamp(P(t) + clamp(adjustment(t), -max_rate·dt, +max_rate·dt), P_min, P_max)
```

**Default gains:** Kp = 0.05, Ki = 0.005 (conservative).

**Controlled variables:**

| Variable | Target |
|---|---|
| Verification lag (p95) | < 10 seconds |
| Cell utilization ratio | 0.6–0.8 |
| Dispute resolution time | < 1 hour (LOW), < 10 min (HIGH) |
| PC exhaustion rate | < 5% of agents per epoch |
| Parcel load imbalance | CV < 0.3 across parcels |

**Stability protections:**
- **Anti-windup:** Integral clamped to max 2× adjustment.
- **Rate limiting:** Max 10% parameter change per epoch.
- **Operating envelope guards:** Hard floor and ceiling per parameter.
- **Dead-band filtering:** Ignore errors < 5% of target.

---

## 31. Parcel Controller Simulation Specification

### 31.1 Simulator Architecture

Discrete-event simulation with: workload generator (4 modes: stationary, bursty, drift, adversarial), parcel state model, controller under test (both loops), and metrics collector tracking 12 quantities per epoch:

`parcel_count, parcel_churn_rate, remote_X_rate, avg_queue_delay, p99_queue_delay, verification_spillover_rate, migration_bytes, capsule_frequency, cut_commit_frequency, recovery_surface, hotspot_amplification, controller_oscillation_count`

### 31.2 Reference Workload Suite (W1–W7)

| # | Workload | Purpose | Scale |
|---|---|---|---|
| W1 | Stationary, uniform load | Baseline: no unnecessary splits | 100 parcels, 10K ops/epoch |
| W2 | Single hotspot (1 parcel at 10×) | Fast loop responds, slow loop splits only if sustained | 100 parcels, spike on 1 |
| W3 | Migrating hotspot (moves every 50 epochs) | Slow loop tracks drift without excessive churn | 100 parcels, drift cycle |
| W4 | Bursty Poisson (λ varying 1×–10×) | Fast loop absorbs spikes without slow-loop splits | 100 parcels, random spikes |
| W5 | Adversarial oscillation (load alternates every 2 epochs) | Controller converges to average, not tracks oscillation | 50 parcels, adversarial |
| W6 | Adversarial fake contention (spurious X-class signals) | Slow loop rejects fake split candidates | 50 parcels, adversarial |
| W7 | Cascading failure (30% parcels fail) | Recovery and re-parcelization within bounds | 200 parcels, fail 60 |

### 31.3 Acceptance Criteria

| Criterion | Threshold | Applies to |
|---|---|---|
| Steady-state hotspot amplification | < 3.0 | W1, W3, W4 |
| Controller oscillation count | 0 reversals per 100 epochs | W1, W5, W6 |
| Fast-loop settling time | < 5 epochs to within 20% of target | W2, W4 |
| Slow-loop parcel churn | < 5% of parcels change per epoch sustained | W3, W4, W5 |
| Remote X-class rate | < 10% cross parcel boundary | W1, W2, W3 |
| Cut Commit fallback rate | < 1% of X-class ops | W1, W2, W3 |
| Recovery time (from 30% failure) | < 50 epochs to 2× steady-state | W7 |
| Adversarial split rejection | > 90% of fake candidates rejected | W6 |
| Shadow plan discard under oscillation | > 80% discarded | W5 |
| Migration bytes per epoch | < 1% of total parcel state | W1, W3 |

**Deployment gate:** The parcel controller cannot be deployed beyond 100 agents until all W1–W7 pass all criteria.

### 31.4 Tuning Procedure

1. W1 (stationary) — verify no unnecessary splits. If splitting, increase θ_enter and k.
2. W2 (hotspot) — verify fast loop within 5 epochs. If slow, increase Kp. If overshoot, decrease.
3. W5 (adversarial oscillation) — verify no tracking. If tracking, increase shadow window and dead-band.
4. W6 (fake contention) — verify rejection. If accepting, tighten quality test.
5. W3+W4 (drift+bursty) — verify combined behavior. Iterate hysteresis if churn high.
6. W7 (cascade) — verify recovery. If slow, increase replica fanout or decrease snapshot interval.
7. All seven together as final regression.

---

## 32. Controller Structural Safeguards

### 32.1 Circuit Breaker

Halts slow loop when anomalous behavior detected. Fast loop always runs.

| Trigger Condition | Threshold | Response |
|---|---|---|
| Parcel churn exceeds maximum | > 10% changed in single epoch | Halt slow loop 10 epochs |
| Split-then-merge reversal | Any within 20 epochs | Halt 20 epochs, discard plan |
| Migration bytes exceed budget | > 5% of total state in epoch | Halt until backlog clears |
| Shadow plan variance spike | > 3× historical mean | Discard plan, extend window 2× |
| Cascading controller activation | > 30% parcels simultaneously adjusting | Halt globally 20 epochs, one-at-a-time only |

**Reset:** After halt, gains reduced 50%. Second trigger within 50 epochs → gains reduced 75%, halt doubled. Three consecutive → governance review.

### 32.2 Parcel Rollback

Every slow-loop change produces a rollback record before migration:

```
RollbackRecord = {
  plan_id, affected_parcels, pre_state (snapshots), migration_log,
  initiated_epoch, committed (bool), rollback_deadline
}
```

**Triggers:** Capsule failure due to migration, active lease unreachable, circuit breaker during migration, deadline exceeded. Rollback restores pre-migration state. Included in Witness Seal. Max one concurrent plan per locus.

### 32.3 Degradation Mode

Controller halted > 100 consecutive epochs → static parcel configuration, fast loop only, governance alert. Exit requires governance approval + new parameters validated against production traces through full W1–W7 suite.

### 32.4 Audit Trail

Every slow-loop decision logged:
```
ParcelDecisionAudit = {
  decision_id, epoch, locus, decision_type (split|merge|migrate|no_action),
  input_metrics (SLV + hypergraph stats), candidate_plan, shadow_result,
  outcome (accepted|rejected_quality|rejected_shadow|rejected_breaker),
  actual_J (retrospective)
}
```

---

# PART IX — FEDERATION AND RECOVERY

## 33. Cross-Region Federation

### 33.1 Regional Verification Sovereignty

Each region is authoritative for claims whose locus has locality matching that region. For cross-region or unconstrained loci, primary region assigned by `hash(locus_id)`.

### 33.2 Tiered Consistency

| Safety Class | Model | Latency |
|---|---|---|
| LOW | Trust primary score. Eventual consistency. | None |
| MEDIUM | Spot-check (1–2 local verifiers, ±0.15 tolerance). | Seconds |
| HIGH | Full independent verification per region. Score reconciliation on discrepancy. | Moderate |
| CRITICAL | Mandatory super-verification from 3+ regions (always). | Highest |

### 33.3 Super-Verification

On discrepancy (V_primary and V_secondary differ by > tolerance band):
1. Claim tagged `cross-region-disputed`.
2. Expanded verifier set from 3+ regions (primary, secondary, tie-breaker by `hash(claim_id || "tiebreak") mod num_regions`).
3. V_super becomes authoritative. Prior scores archived in membrane proof.

### 33.4 Regional Verification Quality Index (RVQI)

Immune Plane monitors per region: cross_region_agreement_rate, super_verification_trigger_rate, verifier_reputation_mean, verifier_diversity, anomaly_flag_rate.

| Condition | Action |
|---|---|
| Agreement rate < 0.8 for 10 epochs | `degraded_verification`. Claims promoted to full re-verification. |
| Super-verification trigger rate > 0.3 for 5 epochs | `high_discrepancy`. Verifier pool audited. |
| Verifier diversity < 2 lineages | `monoculture_risk`. Mandatory cross-region verification. |
| Anomaly flag rate > 0.2 | `compromised_risk`. Enhanced monitoring. Governance weight reduced. |

Flags removed after 20 consecutive healthy epochs. Governance escalation after 100 consecutive flagged epochs.

**Divergence trend monitoring:** The slope of super-verification trigger rate over the last 100 epochs. Positive slope → governance alert even if absolute rate is below threshold.

**Mandatory periodic calibration:** Every 500 epochs, 100 standardized test claims (known correct verdicts) distributed to all regions. Regions below 85% accuracy → mandatory remediation.

---

## 34. Failure Recovery: Witness Ladder

### 34.1 Per-Locus Recovery State

- **Bounded delta journal** (per-parcel, since last snapshot).
- **Periodic snapshot** (full parcel state).
- **Quorum-signed Witness Seal** committing to: snapshot root, delta root, lease frontier, claim frontier, admitted bundle frontier.
- **Periodic anchoring** of witness seals into the settlement plane.

### 34.2 Recovery Algorithm

```
1. Fetch latest anchored WitnessSeal for the locus
2. Fetch referenced snapshot
3. Pull missing delta fragments from quorum peers
4. Replay deltas onto snapshot
5. Recompute roots
6. Verify against WitnessSeal
7. Resume anti-entropy and service
```

### 34.3 Anti-Entropy

- Merge-state sync: digest exchange + missing-delta pull.
- Exclusive-state sync: sequence-gap repair.
- Artifact sync: availability challenges and retrieval probes.

### 34.4 Partition Tolerance

- **M-class and B-class:** Continue locally. Provisional.
- **X-class multi-parcel:** Degrade or pause.
- **Claims:** Remain provisional without forcing false finality.
- **Capsules:** Expire and revert if commit record absent.
- **Leases:** Auto-expire.

No global history replay required. Recovery needs only local snapshot + bounded journal + peer delta sync.

### 34.5 Retention Policy

- LOW safety: aggressive compaction.
- HIGH safety: longer witness-chain and artifact retention.
- CRITICAL / constitutional: strongest retention.

---

# PART X — SECURITY

## 35. Sentinel Graph

### 35.1 Structure

Graph of formal anomaly edges: `<subject_a, subject_b, relation_type, evidence_ref, confidence, epoch>`.

**Relation types:** `collusion_suspicion | withholding | replay_anomaly | identity_churn | verification_drift | regional_degradation`

### 35.2 Collusion Detection

Verification affinity matrix A[i][j] = fraction of agent i's claims verified by agent j, weighted by recency.

```
collusion_score(i, j) = A[i][j] × A[j][i] × (1/diversity(i)) × (1/diversity(j))
```

Score > 0.3 → flagged. Reputation halved. Excluded from each other's verifier pools for 10 epochs. Three flags in 100 epochs → suspended from verification 100 epochs.

### 35.3 Responses

- Risk signals raised for anomalous patterns.
- Verification depth increased for suspicious claims.
- PC reduced for suspicious actors (effective bandwidth throttle).
- Compromised cells quarantined.
- Flagged model lineages trigger deeper verification.
- Regional degradation feeds into RVQI.

---

## 36. Heuristic Claim Governance: Anti-Manipulation and Monitoring

### 36.1 Anti-Manipulation Rules (10 Rules)

**Rule 1: Staked evidence.** Support/attack edges require concrete evidence + staked PC. Unfounded edges → PC burned.

**Rule 2: Independent assumption verification.** Assumption challenges go through V-class verification for the assumption's own class. Cannot be invalidated by governance vote alone.

**Rule 3: Champion rotation window.** 72h HIGH, 24h MEDIUM, 1h LOW. Challenge period before switch takes effect. Successful counter-attack during window → rotation cancelled.

**Rule 4: Minimum supporter diversity.** 3+ independent agents (no shared operator, model family, or region) required for champion status.

**Rule 5: Multi-stakeholder permit approval.** HIGH+: requires 1 verifier + 1 domain expert + 1 governance representative. No single stakeholder class can unilaterally issue or block.

**Rule 6: Non-deferrable sunset.** Permits expire. Re-evaluation from scratch required. No auto-renew.

**Rule 7: Low-threshold revocation.** Single valid challenge → automatic downgrade to `advisory`. Restoring requires full permit process.

**Rule 8: Governance reputation tracking.** Approvers with > 30% revocation rate within 100 epochs → voting weight reduced.

**Rule 9: Calibration-weighted rewards.** AIC rewards weighted by calibration score (outcome-rich) or by downstream citations + permit duration – challenge cost (outcome-poor).

**Rule 10: No reward for unrelied-upon claims.** Zero AIC for claims that never receive a Reliance Permit.

### 36.2 Governance Health Dashboard

Six metrics per locus:

| Metric | Healthy | Alert |
|---|---|---|
| Champion stability | > 50 epochs since last change | < 10 epochs (rapid cycling) |
| Attack edge density | < 2 per epoch per family | > 10 (possible flooding) |
| Permit revocation rate | < 10% | > 30% (granting bad permits) |
| Approver concentration | Top 3 agents < 40% of permits | > 60% (concentration risk) |
| PC burn on argumentation | Stable | Sudden 5× spike |
| Calibration drift | Stable or improving | Declining 3 consecutive epochs |

### 36.3 Automated Monitors

**Monitor 1: Rapid Champion Cycling.** > 3 changes in 50 epochs → family frozen (current champion locked). All pending edges held for review. Governance investigation.

**Monitor 2: Argumentation Flooding.** > 5 edges/epoch/family by one agent → doubled PC cost. Sustained 5 epochs → 50-epoch exclusion.

**Monitor 3: Approver Collusion.** Same 3 agents approve > 50% of domain permits with > 20% revocation → weight halved, expanded approver requirement.

**Monitor 4: Strategic Assumption Invalidation.** > 3 challenges/epoch, > 50% rejected → tripled PC cost, reputation reduced.

### 36.4 Response Playbooks

**Playbook A: Single-Actor Manipulation.** Agent's argumentation privileges suspended → edges quarantined → 100-epoch investigation → Confirmed: slash + permanent exclusion. Legitimate: restore. Inconclusive: permanent cost doubling.

**Playbook B: Governance Capture.** Expanded approver set → recent permits re-reviewed → coalition weights reduced → 200-epoch investigation → Confirmed: 500-epoch suspension. Structural: rules amended by G-class.

**Playbook C: Calibration Collapse.** Score < 0.5 for 10 epochs → permits downgraded to advisory → new permits suspended → mandatory re-evaluation → family retired if re-evaluation fails.

### 36.5 Governance Escape Valve

Any 3 governance agents can initiate 50-epoch emergency freeze on any family. Must be ratified by G-class quorum within 50 epochs or auto-expires. > 3 unratified freezes in 500 epochs → initiators' weight reduced.

---

## 37. Defense-in-Depth Summary

Each major risk area has three layers of protection:

**Parcel Controller:**
1. Prevention: Simulation-validated parameters (§31).
2. Detection: Circuit breaker (§32.1).
3. Containment: Rollback + degradation mode (§32.2–32.3).

**Fusion Capsules:**
1. Prevention: TLA+-verified state machine (§12.3).
2. Detection: SRG re-execution + quorum certs (§12.4).
3. Containment: Epoch monotonicity + expiry safety + frequency monitoring (§12.4).

**Heuristic Governance:**
1. Prevention: 10 anti-manipulation rules (§36.1).
2. Detection: 6-metric dashboard + 4 monitors (§36.2–36.3).
3. Containment: 3 playbooks + escape valve (§36.4–36.5).

**Verification Membrane:**
1. Prevention: Classification gate + deep diversity + supersession protocol (§14–18).
2. Detection: MQI drift detection + continuous re-verification (§19–20).
3. Containment: Conservative mode + lockdown + constitutional protection (§13, §19).

---

# PART XI — COMMUNICATION

## 38. Communication Architecture and AACP Integration

### 38.1 Communication Rules

1. **Publish to loci, not the world.** Agents write signals into locus/parcel routers.
2. **Subscribe by capability and locality.** Agents perceive only matching loci.
3. **Move blobs off the control plane.** References and certificates, not artifacts.
4. **Let signals decay.** Unreinforced signals evaporate automatically.

### 38.2 AACP Message Types (25+)

| Message Type | Payload | Direction |
|---|---|---|
| `signal_publish` | SIG | Agent → Parcel Router |
| `claim_submit` | CLM + CLS | Agent → Parcel → Membrane |
| `lease_request` | LSE (partial) | Agent → SRG Coordinator |
| `lease_grant` / `lease_deny` | LSE | SRG Coordinator → Agent |
| `attestation_submit` | ATT | Verifier → Membrane |
| `bundle_commit` | BDL + MCT | Membrane → SRG → Crystallizer |
| `recruit` / `release` | SLV + capability | Parcel ↔ Agent |
| `capsule_grant_request` | GNT (partial) | Capsule initiator → Parcel owners |
| `capsule_grant_issue` | GNT (signed) | Parcel owner → Capsule initiator |
| `capsule_commit` | CAP + commit record | Capsule → Parcels |
| `capsule_install` | CAP + deltas | Capsule → Parcels |
| `capsule_late_install` | CAP + commit record + GNTs | Post-partition |
| `grant_reconciliation` | GNT reconciliation cert | Post-partition |
| `cut_commit_prepare` / `prepared` / `abort` / `commit` | 2PC payloads | Fallback only |
| `governance_propose` / `governance_vote` | GOV | Governance |
| `federation_propagate` | BDL + MCT | Gateway → Gateway |
| `super_verification_request` | CLM + regional scores | Region → Regions |
| `anomaly_report` | SNE + evidence | Sentinel → SRG + Registry |
| `witness_seal_anchor` | WSL | Parcel SRG → Settlement |
| `reliance_permit_issue` | RLP | Membrane/Governance → Cortex |
| `cso_transfer` | CSO transfer ticket | Parcel → Parcel |
| `classification_challenge` | CLS dispute | Classifier → Classification Gate |
| `monitor_alert` | GMR | Sentinel → Governance Dashboard |
| `playbook_activate` | GPB | Sentinel → Governance |

---

# PART XII — DEPLOYMENT

## 39. Scalability Model

Agents publish to loci, not everyone. Cells form around active parcels. Hot parcels split physically, not logically. Only touched parcels run capsules/cut-commit. Durable memory stores bundles, not chatter. The system scales with active contention domains, not agent count squared.

| Scale | Bottleneck | Mitigation |
|---|---|---|
| 10⁶ agents | Routing table size | Hierarchical routing + parcel splitting |
| 10⁹ agents | Federation bandwidth | Summary-based federation + on-demand retrieval |
| 10¹² agents | Knowledge graph query latency | Locus partitioning + locality-aware routing |
| Adversarial | Membrane saturation | Adaptive depth + sampled convergence + escalation |
| Global failure | Regional isolation | Autonomous regional operation + federation resync |
| Congestion | PC exhaustion | Controller adjusts issuance + parcel splitting |

---

## 40. Comparison with Existing Systems

| Dimension | Blockchain / DAG | Noosphere |
|---|---|---|
| Fundamental unit | Transaction | Scoped decaying signal / typed claim |
| Shared structure | Append-only history | Typed LSO over loci + parcels |
| Ordering | Total temporal | Partial causal (Epistemic DAG) |
| Consensus | One-size-fits-all | Five-class algebra (M/B/X/V/G) |
| Finality | Irreversible | Epistemic (revocable) + reliance permits (expiring) |
| Persistence | Grows with all events | Grows with bundles (K ≪ M) |
| Routing | Broadcast | Publish to loci, scope-aware |
| Verification | Secondary | Primary (class-specific membrane) |
| Resources | Scalar gas | Three budgets (SB/PC/CS) + CSOs |
| Communication | O(N²) | O(log N) small-world |
| Failure | Chain rollback | Witness ladder + cell apoptosis + lease/capsule expiry |
| Uncertainty | Binary finality | First-class: provisional, disputed, operational-canon |
| Coordination ephemera | Preserved forever | Decays unless reinforced |
| Heuristic knowledge | Not representable | Argumentation + reliance permits |

---

## 41. Why This Is a New Paradigm

### Nine Innovations

1. **Locus/Parcel decomposition.** Stable correctness boundaries + elastic execution units.
2. **Operation-class algebra (M/B/X/V/G).** Agreement derived from invariant type.
3. **Certified Slice Objects.** Proof-carrying bounded-resource rights with conservation laws.
4. **Fusion Capsules with epoch fencing.** Narrower and more provable than distributed 2PC.
5. **Claim-class-specific verification membrane.** Different truth types need different validation.
6. **Contestable Reliance Membrane.** Operational permission, not truth certification, for heuristics.
7. **Decaying stigmergic signals.** Coordination reflects current reality, not accumulated history.
8. **Three-budget resource model.** Payment, spam, capacity as separate concerns.
9. **Witness Ladder recovery.** Auditable without universal append-only history.

### The Category

**Homeostatic Epistemic Coordination Fabric** — defined by:
1. Typed coordination state over logical loci, not ordered event history.
2. Five-class operation algebra deriving agreement from invariant type.
3. Four-tier memory growing with verified bundles, not all events.
4. Claim-class-specific verification with separate truth and reliance axes.
5. Self-regulating through bi-timescale homeostatic control.

---

## 42. Integration with Atrahasis Subsystems

| Atrahasis Layer | Noosphere Integration |
|---|---|
| **CIOS** | Compiles goals into AASL operations, maps to loci, budgets SB/PC, chooses placement. Task decomposition results are verifiable claims. |
| **Verichain** | IS the Verification Membrane. Extended with orthogonal sortition, claim-class-specific promotion, contestable reliance, classification gate, drift detection, re-verification. |
| **AASL** | Native protocol language. 23 type tokens. All primitives AASL-encoded. |
| **AACP** | Wire protocol. 25+ message types. AASL payloads in AACP frames. |
| **Agent Clusters** | Dynamic cells within parcels. Tetrahedral motif preserved. Self-assemble around active demands, dissolve when pressure drops. |
| **Knowledge Graph** | Knowledge Cortex output. MCTs gate admission. Four-tier memory. Heuristic families with argumentation. Contradiction lattice. Bundle compaction. |
| **Economic Layer** | Three-budget model realizes gas-free, access-based economics. CSOs for capacity. AIC for settlement. |
| **Planetary Network** | Loci provide stable coordination domains. Parcels provide elastic placement. Federation gateways with tiered consistency and RVQI for cross-region. |

---

## 43. Implementation Roadmap

### Phase 1: Prototype (Months 1–6)
Single locus, single parcel, single cell. Signal publishing, decay, AASL claim creation, basic membrane for deterministic/empirical claims, in-memory bundles, PC accounting. 10–100 agents, single locus.

### Phase 2: Multi-Parcel (Months 6–12)
Multiple parcels within loci. Parcel-aware routing, dynamic cell assembly, Epistemic DAG, leases, Fusion Capsules (with CEP TLA+ model checking), CSOs, Artifact Availability Plane, SRGs with MEDIUM safety class. E1+E2 economic simulation passed. 1K–10K agents.

### Phase 3: Regional (Months 12–24)
Multiple regions. Federation gateways, bi-timescale controller (W1–W7 simulation passed), AIC settlement (E1–E6 economic simulation passed), Sentinel Graph with collusion detection, heuristic family management, contestable reliance membrane, RVQI, governance framework. 100K–1M agents.

### Phase 4: Planetary (Months 24–48)
Full deployment. Complete small-world topology, formal CEP and CSO proofs, simulation-validated parcel controller with production traces, canonical memory distillation, planetary federation, E1–E7 economic simulation passed, continuous production monitoring. 1M+ → billions.

---

## 44. Formal State Model

### State Transitions

**Signal:** `CREATED → LIVE → {REINFORCED → LIVE | DECAYED → REMOVED | CONSUMED → REMOVED}`

**Claim:** `SUBMITTED → CLASSIFIED (CLS sealed) → ACTIVE → VERIFYING → {VERIFIED → BUNDLED → DURABLE | REJECTED → REMOVED | DISPUTED → RESOLVED → VERIFIED or SUPERSEDED | ABANDONED (decay) → REMOVED}`

**Lease:** `REQUESTED → {GRANTED (quorum cert) → ACTIVE → {RELEASED | EXPIRED (TTL) | REVOKED} | DENIED}`

**Bundle:** `ASSEMBLING → COMMITTED (MCT issued) → {CANONICAL (compacted) | ARCHIVED (superseded)}`

**Locus:** `CREATED → ACTIVE → {SPLIT (rare) | MERGED (rare) | QUIESCENT → ARCHIVED}`

**Parcel:** `CREATED → ACTIVE → {SPLIT | MIGRATED | MERGED | DISSOLVED}`

**Capsule:** `INIT → COLLECTING → ARMED → EXECUTING → COMMITTED → INSTALLED` or `→ EXPIRED | ABORTED`

**Heuristic Reliance:** `SANDBOX → ADVISORY → BOUNDED_OPERATIONAL → RATIFIED` (sequential, no skipping, minimum dwell times)

### Durable State

Identity registry, locus registry + split/merge ancestry, active lease tables, admitted bundles with MCTs, claim-family canonical pointers, CSO balances, snapshots + witness seals, settlement state (AIC ledger), membrane versions, governance state + directives, sentinel graph, heuristic families + reliance permits.

### Ephemeral State

Live signals (decaying), open cells, open verification sessions, unsealed delta journals, challenge windows, active capsules + grants, SLV (recomputed continuously).

---

## 45. Open Research Questions

| # | Question | Nature |
|---|---|---|
| 1 | Formal proof of M/B/X/V/G composition safety | Formal methods |
| 2 | CSO correctness under Byzantine rebalancing | Formal methods (TLA+ target) |
| 3 | Privacy-preserving membrane certificates | Cryptography |
| 4 | Sentinel Graph self-protection | Security architecture |
| 5 | Multi-region parcel composition for cross-region loci | Systems design |
| 6 | Bundle compaction law preserving provenance | Formal semantics |
| 7 | Verifier diversity metrics for hidden correlation | Mechanism design |
| 8 | PRDT-style locus kernels as Cut Commit replacement | Research (promising, unproven) |

These are research targets, not structural risks. None can cause system failure if left unresolved.

---

## 46. Follow-On Specification Documents

| Document | Priority |
|---|---|
| `Parcel_Controller_Simulator/` (implement §31) | **Critical — blocking Phase 2** |
| `Capsule_Epoch_Protocol.tla` (implement §12.5) | **Critical — blocking Phase 2** |
| `Economic_Simulator/` (implement §29) | **Critical — blocking Phase 2** |
| `Locus_Parcel_Core_Spec.md` | Critical |
| `Certified_Slice_Object_Spec.md` + TLA+ | Critical |
| `Verichain_Membrane_Protocol.md` (class-specific) | Critical |
| `Orthogonal_Sortition_Spec.md` | Critical |
| `Contestable_Reliance_Membrane.md` (incorporating §17 + §36) | High |
| `BiTimescale_Controller_Spec.md` | High |
| `Witness_Ladder_Recovery_Spec.md` | High |
| `Cross_Region_Federation_Protocol.md` | High |
| `Sentinel_Graph_Spec.md` | High |
| `Heuristic_Family_Argumentation_Engine.md` | Medium |
| `AASL_AACP_Noosphere_Profile.md` | Medium |
| `Formal_Models/` (TLA+ for CSO, CEP, M/B/X composition) | Medium |
| `Security_And_Slashing_Spec.md` | Medium |

---

## 47. Architecture Maturity Summary

| Subsystem | Maturity |
|---|---|
| Locus/Parcel model | Protocol-ready |
| Signal model + decay + reinforcement | Protocol-ready |
| AASL types (23 tokens, 25+ messages) | Protocol-ready |
| Claim Classification Gate | Protocol-ready |
| Supersession Protocol | Protocol-ready |
| Membrane Drift Detection (MQI) | Protocol-ready |
| Continuous Re-Verification | Protocol-ready |
| Operation-class algebra (M/B/X/V/G) | Design-complete |
| Certified Slice Objects | Design-complete, proof-required |
| Fusion Capsules (CEP) | Design-complete, proof-specified |
| Verification Membrane (class-specific) | Hardened |
| Verifier Selection (Sortition + SCS + deep diversity) | Hardened |
| Contestable Reliance Membrane | Governance-hardened |
| Contradiction Lattice + Argumentation | Design-complete |
| Knowledge Crystallizer + compaction | Design-complete |
| Bi-Timescale Controller | Simulation-specified |
| Three-Budget Model (SB/PC/CS) | Simulation-specified |
| Cross-region federation + RVQI | Design-complete |
| Witness Ladder | Design-complete |
| Settlement Surface | Retained (standard BFT) |
| Sentinel Graph + collusion detection | Design-complete |
| Heuristic Governance Monitoring | Defense-in-depth |

### Risk Classification

| Class | Count | Details |
|---|---|---|
| **Structural risk** | 0 | All have defense-in-depth |
| **Engineering risk** | 3 | Controller sim, CEP proof, economic sim — all have specs + gates |
| **Research opportunity** | 8 | None are failure modes |
| **Political risk** | 1 | Heuristic governance — monitored + playbookd + escape valve |
| **Epistemic risk** | Bounded | Membrane is most heavily defended subsystem |

---

*The fundamental direction — scoped verified convergence replacing global event ordering — has survived nine rounds of design, red-teaming, independent redesign, merging, and hardening across two AI systems and multiple independent evaluations.*

*The architectural commandment: optimize the rest of the system around the membrane. Never optimize the membrane around the rest of the system.*

*The protocol is ready for Phase 1 implementation.*
