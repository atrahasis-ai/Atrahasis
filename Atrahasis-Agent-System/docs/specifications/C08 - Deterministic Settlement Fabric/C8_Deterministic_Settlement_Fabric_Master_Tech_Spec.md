# Deterministic Settlement Fabric v2.0 — Master Technical Specification

**Invention ID:** C8
**System:** Atrahasis Planetary-Scale Distributed AI Agent System
**Stage:** SPECIFICATION
**Version:** 2.0.1 (Unified — incorporates Patch Addendum v2.0.1, C9 Reconciliation Errata, and T-304 economics retrofit)
**Date:** 2026-03-15
**Classification:** Whitepaper — Self-Contained Technical Specification
**Target Audience:** Systems architects, distributed systems researchers, mechanism designers
**Supersedes:** All prior C8 documents (Part 1, Part 2, Patch Addendum v2.0.1)
**Renovation Note (T-304, 2026-03-15):** DSF capacity economics are now interpreted against the Alternative C sovereign compute posture: sovereign habitats and native services are the default capacity base, `C45` leased cognition is a temporary outer-membrane lane only, and `C47` adaptation/quarantine spend is treasury-planned promotion work rather than permanent market dependence.

---

# Table of Contents

1. Introduction and Motivation
2. Hybrid Deterministic Ledger Specification
3. Three-Budget Economic Model
4. Capability-Weighted Stake
5. Multi-Rate Settlement Engine
6. Four-Stream Settlement
7. Intent-Budgeted Settlement
8. Capacity Market
9. CSO Conservation Framework
10. Graduated Slashing System
11. Treasury and Governance
12. Integration Specifications
13. Security Analysis
14. Scalability and Deployment
15. Conclusion and Future Work
Appendix A: Notation and Symbols
Appendix B: Parameter Reference Table
Appendix C: Data Structure Definitions
Appendix D: Economic Simulation Scenarios E1-E11
Appendix E: Governance Parameter Reference
Appendix F: Adversarial Finding Resolution Matrix
Appendix G: Hard Gate Resolution Summary
Appendix H: Cross-Layer API Surface
Appendix I: Failure Mode Catalogue
Appendix J: Monitoring Specification
Appendix K: Formal Verification Roadmap
Appendix L: Changelog

---

# Section 1: Introduction and Motivation

## 1.1 The Problem: Economic Settlement for Autonomous AI Agent Systems

Planetary-scale AI agent systems — networks of thousands to hundreds of thousands of autonomous agents performing distributed computation, verification, and coordination — require an economic substrate. Without one, there is no mechanism to:

- **Allocate scarce resources** (compute, storage, bandwidth) among competing agents with heterogeneous capabilities and demands.
- **Incentivize quality** in task execution and verification, where the outputs are epistemic (knowledge claims, inference results) rather than deterministically checkable.
- **Punish defection** when agents submit fraudulent work, free-ride on others' verification, or attempt to monopolize shared infrastructure.
- **Prevent spam** in open, semi-open, or operator-mediated ingress surfaces where the cost of generating plausible-looking agent messages is near zero.
- **Coordinate at scale** without centralized orchestration that creates single points of failure and trust concentration.

The Atrahasis system is one such network. It comprises six architectural layers:

```
Layer 6: RIF — Recursive Intent Fabric (Orchestration)          C7
Layer 5: Tidal Noosphere (Coordination, CRDT state, topology)   C3
Layer 4: PCVM — Probabilistic Claim Verification Machine        C5
Layer 3: EMA — Epistemic Metabolism Architecture                 C6
Layer 2: DSF — Deterministic Settlement Fabric (THIS DOCUMENT)   C8
Layer 1: Alternative C sovereign communication authority         C38-C42 / T-290
```

DSF is the economic settlement layer. It receives budget constraints from the orchestration layer above (RIF intent resource_bounds), consumes verification attestations and coordination primitives from C3/C5/C6 below, and produces deterministic settlement outcomes — reward distributions, slashing penalties, capacity allocations, and budget state transitions — that all layers consume.

## 1.2 Why Existing Solutions Are Insufficient

Three categories of existing solution have been considered and rejected, each for specific architectural reasons.

### 1.2.1 Blockchain Settlement (Ethereum, Solana, Cosmos)

Public blockchain settlement provides strong consistency guarantees but introduces overhead that is mismatched to AI agent workloads:

- **Latency.** Ethereum L1 finality (~12 minutes), Solana (~400ms), and even optimistic rollups (7-day challenge windows) impose settlement delays that are either too slow for per-epoch agent operations or require trust assumptions (centralized sequencers) that undermine decentralization.
- **Cost.** On-chain settlement costs scale with network congestion. During peak periods, Ethereum gas costs make micro-settlement (rewarding individual task completions worth fractions of a dollar) economically irrational.
- **Single-budget conflation.** Ethereum's gas serves simultaneously as spam control, computation payment, and resource allocation signal. EIP-1559 improved price discovery but did not separate these concerns. During congestion, legitimate low-value agent operations are priced out identically to spam.
- **Consensus overhead.** Full BFT consensus (Tendermint, HotStuff, Narwhal-Tusk) provides total ordering guarantees that settlement does not always need. For read-heavy workloads (balance queries, capacity checks), consensus is wasted coordination.

### 1.2.2 Centralized Runtime Billing (Cloud and Leased Provider Models)

Centralized runtime billing (AWS-style metered usage, leased-provider invoices, or internal accounting databases) provides low latency and simplicity but creates:

- **Single point of failure and trust.** A centralized billing authority can arbitrarily modify balances, deny service, or extract rents. For an autonomous agent system, this reintroduces the principal-agent problem that decentralization was meant to solve.
- **No verifiable conservation.** Without distributed verification, there is no guarantee that the total economic supply is conserved. The billing authority can inflate or deflate at will.
- **No credible commitment.** Slashing penalties and staking mechanisms require credible commitment — the guarantee that penalties will be enforced even if the penalized party controls infrastructure. Centralized systems cannot provide this against the operator.

### 1.2.3 No Economy (Pure Coordination)

Some multi-agent frameworks (AutoGPT, CrewAI, LangGraph) operate without internal economics, relying on external funding (user-provided API keys, provider credits, or centrally sponsored runtime) and centralized orchestration. This works for small-scale, short-lived agent teams but cannot support:

- **Persistent agent populations** that must sustain themselves economically across unbounded time horizons.
- **Adversarial environments** where agents have incentives to defect, free-ride, or manipulate.
- **Resource allocation** at scale, where thousands of agents compete for finite compute and bandwidth.

## 1.3 DSF's Position: CLS-Meets-IOTA for AI Agents

DSF draws architectural inspiration from two domains:

**From traditional clearing systems (CLS, ACH, SWIFT):** The insight that settlement does not require real-time consensus. CLS settles $6.6 trillion daily in foreign exchange using multilateral netting and batch processing, reducing gross settlement by ~96%. ACH processes 80 million transactions daily in the United States using same-day and next-day batch windows. DSF adopts this batch settlement paradigm: operations are collected during epochs and settled atomically at epoch boundaries.

**From IOTA 2.0 (Mana, congestion control):** The insight that economic functions should be separated into distinct instruments. IOTA 2.0 separates its native token (value transfer) from Mana (congestion control and access). DSF extends this to a three-budget model: Sponsor Budget (payment), Protocol Credits (spam control), and Capacity Slices (resource allocation).

The synthesis — **batch settlement with multi-budget separation, purpose-built for AI agent workloads** — is DSF's core architectural contribution.

## 1.4 Temporal Hierarchy and Terminology

Throughout this document, "epoch" refers to the SETTLEMENT_TICK — the atomic settlement period of 60 seconds. This is the canonical timing unit for all DSF operations.

The Atrahasis stack operates on a three-tier temporal hierarchy established by C9 Cross-Layer Reconciliation:

| Tier | Name | Duration | Authority | Relationship |
|------|------|----------|-----------|--------------|
| 1 | SETTLEMENT_TICK | 60 seconds | C8 (DSF) | Atomic settlement period |
| 2 | TIDAL_EPOCH | 3600 seconds | C3 (Tidal Noosphere) | 60 SETTLEMENT_TICKs |
| 3 | CONSOLIDATION_CYCLE | 36000 seconds | C6 (EMA) | 10 TIDAL_EPOCHs = 600 SETTLEMENT_TICKs |

```
TERMINOLOGY NOTE (C9 Reconciliation):

Throughout this document, "epoch" refers to the SETTLEMENT_TICK — the
atomic settlement period of 60 seconds. This is distinct from:

  - TIDAL_EPOCH (C3): 3600 seconds = 60 SETTLEMENT_TICKs.
    One TIDAL_EPOCH encompasses a full tidal phase cycle in the
    Noosphere. DSF settles 60 times per TIDAL_EPOCH.

  - V-class period: default 5 SETTLEMENT_TICKs (300 seconds).
    Verification settlement accumulates over multiple ticks.

  - G-class period: variable, 10-50 SETTLEMENT_TICKs typical.

Canonical constant: SETTLEMENT_TICK_MS = 60000
```

## 1.5 The v1 Fatal Flaw and v2 Resolution

DSF v1 proposed a pure-CRDT (Conflict-free Replicated Data Type) ledger for all economic state, claiming that consensus was unnecessary for settlement. The Adversarial Analysis and Science Assessment identified a fatal flaw:

**CRDTs cannot enforce global invariants during concurrent operations.**

Specifically:

- **Phantom Balance Attack (FATAL).** If agent A has balance 100 and concurrently issues transfers of 80 to B and 80 to C at different network replicas, both operations are locally valid. A CRDT merge applies both, resulting in balance -60 — a conservation violation. No CRDT merge function can prevent this without coordination, because preventing it requires knowing the global state before applying each operation.

- **Slashing Ordering Attack (CRITICAL).** Graduated slashing penalties (1% -> 5% -> 15% -> 50% -> 100%) require causal ordering. Without consensus on operation order, an attacker can race a stake withdrawal against a slashing event across different replicas.

- **Conservation Verification (NEAR UNSOUND).** The CSO conservation invariant requires consistent global snapshots for verification. CRDTs provide only eventual consistency — at any moment, different replicas may disagree on balances.

DSF v2 resolves all three through the **Hybrid Deterministic Ledger (HDL)**:

| Property | v1 (Pure CRDT) | v2 (HDL) |
|---|---|---|
| Read path | CRDT | CRDT (unchanged) |
| Write path | CRDT | Epoch-Anchored Batch Settlement (EABS) |
| Conservation | Formal proof only | Formal proof + runtime enforcement |
| Ordering | None (eventual) | Deterministic canonical ordering per epoch |
| Coordination | None | Lightweight Reliable Broadcast (not full BFT) |
| Fault tolerance | Partition-tolerant reads | Partition-tolerant reads + crash-fault-tolerant writes (f < n/3) |

**The key insight:** Determinism does not require eliminating coordination — it requires ensuring that all honest nodes process the same inputs in the same order. EABS achieves this by collecting all state-mutating operations during an epoch, broadcasting them via Reliable Broadcast, sorting them deterministically, and processing them atomically at the epoch boundary.

## 1.6 Document Roadmap

This document specifies the complete DSF architecture:

- **Section 2** specifies the Hybrid Deterministic Ledger — the primary technical contribution. It includes CRDT read-path data structures with merge proofs, the complete EABS write-path protocol (five phases, Bracha's Reliable Broadcast, deterministic ordering, settlement function), the ECOR consistency model, fault model, conservation enforcement with proof sketch, and test vectors.

- **Section 3** defines the Three-Budget Economic Model: Sponsor Budget (AIC), Protocol Credits (PC), and Capacity Slices (CS), with lifecycle mechanics, cross-budget friction analysis, and equilibrium proofs.

- **Section 4** specifies the Capability-Weighted Stake system: formula derivation, input components, Sybil resistance, cold-start protocol, and game-theoretic analysis.

- **Section 5** details the Multi-Rate Settlement Engine: B/V/G settlement classes, epoch boundary protocol, NPV normalization, and cross-class timing.

- **Section 6** covers the Four-Stream Settlement computation: stream metrics, reward distribution, cross-stream interactions, and simulation scenarios.

- **Section 7** specifies Intent-Budgeted Settlement: RIF integration, budget mechanics, worker protections, and settlement type mapping.

- **Section 8** defines the Capacity Market: sealed-bid uniform-price auction, progressive clearing, position limits, bootstrap provisions, and minimum viable scale analysis.

- **Section 9** presents the CSO Conservation Framework: formal invariant definitions, proof by structural induction, pending state lifecycle, runtime enforcement, recovery protocols, and I-confluence analysis.

- **Section 10** covers the Graduated Slashing System: five-level schedule, deterministic EABS processing, violation types, appeal mechanism, and formal properties.

- **Section 11** specifies Treasury and Governance: treasury-first issuance, constitutional protections, governance voting, and parameter adjustment procedures.

- **Section 12** details Integration Specifications: exact data flows, frequencies, consistency guarantees, and failure handling for C3, the Alternative C communication stack, C5, C6, and C7 integrations.

- **Section 13** contains the Security Analysis: threat model, adversarial findings, security invariants, attack surface enumeration, and defense-in-depth strategy.

- **Section 14** covers Scalability and Deployment: scale targets, bottleneck analysis, deployment phases, parameter sensitivity, and migration protocols.

- **Section 15** concludes with a summary of contributions, open research questions, and the development roadmap.

---

# Section 2: Hybrid Deterministic Ledger Specification

The Hybrid Deterministic Ledger (HDL) is the primary research contribution of DSF v2.0. It resolves the fundamental tension between CRDT availability — partition-tolerant, coordination-free reads — and financial consistency — conservation-preserving, deterministically-ordered writes — by splitting the ledger into two paths with distinct consistency guarantees unified under the ECOR consistency model.

## 2.1 Architecture Overview

```
+=========================================================================+
|                    HYBRID DETERMINISTIC LEDGER (HDL)                     |
|                                                                         |
|  +---------------------------------+  +-------------------------------+ |
|  |         READ PATH               |  |         WRITE PATH            | |
|  |   CRDT-Replicated State         |  |   Epoch-Anchored Batch        | |
|  |                                 |  |   Settlement (EABS)           | |
|  |  +---------------------------+  |  |  +--------------------------+ | |
|  |  | PN-Counter per account    |  |  |  | Operation Collector      | | |
|  |  | (AIC, PC, CS balances)    |  |  |  | (per-epoch buffer)       | | |
|  |  +---------------------------+  |  |  +--------------------------+ | |
|  |  | State Vector              |  |  |  | Reliable Broadcast       | | |
|  |  | (version tracking)        |  |  |  | (Bracha's RBC)           | | |
|  |  +---------------------------+  |  |  +--------------------------+ | |
|  |  | Optimistic Delta Cache    |  |  |  | Deterministic Orderer    | | |
|  |  | (current-epoch pending)   |  |  |  | (canonical sort)         | | |
|  |  +---------------------------+  |  |  +--------------------------+ | |
|  |                                 |  |  | Settlement Function      | | |
|  |  Guarantees:                    |  |  | (atomic batch processor)  | | |
|  |  - Partition tolerant           |  |  +--------------------------+ | |
|  |  - Never blocks                 |  |  | Conservation Checker     | | |
|  |  - Eventually consistent        |  |  | (invariant enforcement)  | | |
|  |                                 |  |  +--------------------------+ | |
|  |                                 |  |                               | |
|  |                                 |  |  Guarantees:                  | |
|  |                                 |  |  - Deterministic              | |
|  |                                 |  |  - Conservation-preserving    | |
|  |                                 |  |  - Atomic per-epoch           | |
|  +---------------------------------+  +-------------------------------+ |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |              ECOR Consistency Model                                | |
|  |  Read state = last_settled_epoch_state + optimistic_delta          | |
|  |  Staleness bound: at most 1 epoch + broadcast_latency             | |
|  +-------------------------------------------------------------------+ |
+=========================================================================+
```

## 2.2 CRDT Read Path

### 2.2.1 Data Structures

Each account in the HDL maintains a PN-Counter (Positive-Negative Counter) CRDT for each budget type. The PN-Counter is a well-studied CRDT that supports both increment and decrement operations with guaranteed convergence.

**Definition 2.1 (PN-Counter).** A PN-Counter is a pair of grow-only maps (P, N) where P[i] and N[i] record the cumulative increments and decrements attributed to node i, respectively. The counter value is Sigma(P) - Sigma(N).

```
STRUCTURE PNCounter:
    positive: Map<NodeID, uint64>   // Increment vector
    negative: Map<NodeID, uint64>   // Decrement vector

    FUNCTION value() -> int64:
        RETURN sum(positive.values()) - sum(negative.values())

    FUNCTION increment(node_id: NodeID, amount: uint64):
        positive[node_id] += amount

    FUNCTION decrement(node_id: NodeID, amount: uint64):
        negative[node_id] += amount

    FUNCTION merge(other: PNCounter) -> PNCounter:
        result = PNCounter{}
        FOR each node_id IN union(self.positive.keys(), other.positive.keys()):
            result.positive[node_id] = max(self.positive[node_id], other.positive[node_id])
        FOR each node_id IN union(self.negative.keys(), other.negative.keys()):
            result.negative[node_id] = max(self.negative[node_id], other.negative[node_id])
        RETURN result
```

**Definition 2.2 (AccountState).** The complete economic state of a single agent, represented as a CRDT-mergeable structure:

```
STRUCTURE AccountState:
    // Identity
    account_id:          AgentID

    // Budget balances (CRDT-mergeable)
    aic_balance:         PNCounter                    // Sponsor Budget (AIC) — free balance
    staked_aic:          PNCounter                    // AIC locked as collateral for stake
    collateral_held:     PNCounter                    // Pending state collateral deposits
    pc_balance:          PNCounter                    // Protocol Credits (non-transferable)
    cs_allocation:       Map<ResourceType, PNCounter> // Capacity Slices per resource type

    // Pending state tracking
    pending_out:         PNCounter                    // Outbound pending transitions
    pending_in:          PNCounter                    // Inbound pending transitions

    // Settlement metadata
    last_settled_epoch:  uint64                       // Last EABS settlement epoch
    capability_score:    float64                      // Cached, range [1.0, 3.0]
    violation_count:     uint32                       // Monotonic (except appeal decrement)

    // CRDT synchronization
    state_vector:        Map<NodeID, uint64>          // Lamport timestamps per node

    FUNCTION merge(other: AccountState) -> AccountState:
        ASSERT self.account_id == other.account_id
        result = AccountState{account_id: self.account_id}

        // All PNCounter fields: element-wise max merge
        result.aic_balance = self.aic_balance.merge(other.aic_balance)
        result.staked_aic = self.staked_aic.merge(other.staked_aic)
        result.collateral_held = self.collateral_held.merge(other.collateral_held)
        result.pc_balance = self.pc_balance.merge(other.pc_balance)
        result.pending_out = self.pending_out.merge(other.pending_out)
        result.pending_in = self.pending_in.merge(other.pending_in)

        // CS allocation: merge per resource type
        all_types = union(self.cs_allocation.keys(), other.cs_allocation.keys())
        FOR each rt IN all_types:
            self_counter = self.cs_allocation.get(rt, PNCounter{})
            other_counter = other.cs_allocation.get(rt, PNCounter{})
            result.cs_allocation[rt] = self_counter.merge(other_counter)

        // Scalar fields: last-writer-wins by epoch
        result.last_settled_epoch = max(self.last_settled_epoch, other.last_settled_epoch)
        result.capability_score = IF self.last_settled_epoch >= other.last_settled_epoch
                                  THEN self.capability_score
                                  ELSE other.capability_score
        result.violation_count = max(self.violation_count, other.violation_count)

        // State vector: element-wise max
        FOR each node_id IN union(self.state_vector.keys(), other.state_vector.keys()):
            result.state_vector[node_id] = max(
                self.state_vector.get(node_id, 0),
                other.state_vector.get(node_id, 0))

        RETURN result
```

**Definition 2.3 (HDL State Vector).** Per-node metadata tracking settlement progress:

```
STRUCTURE HDLStateVector:
    node_id:         NodeID
    epoch_settled:   uint64              // Last fully settled epoch
    epoch_collecting: uint64             // Current epoch being collected
    account_versions: Map<AgentID, uint64>  // Per-account version counters
    global_version:  uint64              // Monotonic global version

    FUNCTION is_stale(other: HDLStateVector) -> bool:
        RETURN self.epoch_settled < other.epoch_settled

    FUNCTION staleness_bound(other: HDLStateVector) -> uint64:
        RETURN other.epoch_settled - self.epoch_settled
```

### 2.2.2 Merge Semantics and Convergence Proof

**Theorem 2.1 (CRDT Convergence).** The AccountState merge operation satisfies commutativity, associativity, and idempotency. Therefore, AccountState forms a join-semilattice, and all replicas converge to the same state after all messages in transit are delivered.

**Proof.**

*Commutativity:* merge(A, B) = merge(B, A).

Every component of the merge function uses either max() or PNCounter.merge(), both of which are commutative. For max(x, y) = max(y, x) trivially. For PNCounter.merge(), commutativity follows from the commutativity of max() applied element-wise to the positive and negative maps. The union() of key sets is commutative. The `Map<ResourceType, PNCounter>` for cs_allocation applies PNCounter merge per key, with union of key sets — this composition preserves commutativity by the same argument. The added `collateral_held` field uses PNCounter merge (commutative). Therefore the overall merge is commutative.

*Associativity:* merge(merge(A, B), C) = merge(A, merge(B, C)).

max() is associative over natural numbers. PNCounter.merge() inherits associativity from element-wise max(). Union of key sets is associative. Per-key PNCounter merge over Map<ResourceType, PNCounter> inherits associativity. Therefore the overall merge is associative.

*Idempotency:* merge(A, A) = A.

max(x, x) = x for all x. PNCounter.merge(P, P) = P since max applied to identical maps yields the same map. Therefore merge(A, A) = A.

These three properties establish that AccountState is a join-semilattice (a CRDT), guaranteeing eventual convergence regardless of message ordering, duplication, or delay.  QED.

**Invariant READ-1:** The CRDT read path never blocks. A read operation returns the locally merged state immediately, without contacting any other node.

**Invariant READ-2:** After all messages in transit are delivered, all honest nodes hold identical AccountState for every account (standard CRDT eventual consistency).

**Invariant READ-3:** The CRDT read path does NOT enforce conservation. Balances shown may be optimistic (pre-settlement). Only EABS-settled state is conservation-guaranteed.

### 2.2.3 Consistency Guarantees

The read path provides **session monotonic reads**: once a node observes a balance of X for account A, it will never subsequently report a balance less than X for that account (within the same budget type, absent EABS-settled debits). This follows from the monotonicity of PNCounter merge — the value() function is monotonically non-decreasing under merge when only increments occur, and the merge function never reduces any component.

**Staleness Bound.** A read on node N at time t reflects at minimum the state as of epoch (current_epoch - 1), because EABS settlement at each epoch boundary pushes settled state into the CRDT layer. The maximum staleness is:

```
max_staleness = SETTLEMENT_TICK + reliable_broadcast_latency + settlement_computation_time
```

For the canonical SETTLEMENT_TICK of 60 seconds with reliable broadcast latency of approximately 2 seconds and settlement computation of approximately 1 second, maximum staleness is approximately 63 seconds.

## 2.3 EABS Write Path

### 2.3.1 Epoch Lifecycle

Each epoch progresses through five phases:

```
COLLECTING --> BROADCASTING --> ORDERING --> SETTLING --> COMMITTED
   (active       (Bracha's        (canonical     (settlement    (state
    epoch)        RBC)             sort)          function)      merged
                                                                into CRDT)

Timeline within an epoch:
|<------- SETTLEMENT_TICK (60s nominal) ------->|
|                                              |
|  COLLECTING phase                            |
|  (operations buffered locally)               |
|                                    |<- boundary trigger (jittered +/-10%)
|                                    |
|                                    +-- BROADCASTING begins
|                                    |   (Bracha's RBC, ~2s)
|                                    |
|                                    +-- ORDERING
|                                    |   (deterministic sort, <100ms)
|                                    |
|                                    +-- SETTLING
|                                    |   (batch processor, ~1s)
|                                    |
|                                    +-- COMMITTED
|                                        (CRDT state updated)
```

**Definition 2.4 (Epoch Phase):**

```
ENUM EpochPhase:
    COLLECTING      // Operations accepted into local buffer
    BROADCASTING    // Operations broadcast via Reliable Broadcast
    ORDERING        // Received operations sorted canonically
    SETTLING        // Settlement function processes ordered batch
    COMMITTED       // Settled state merged into CRDT read path

STRUCTURE EpochState:
    epoch_number:       uint64
    phase:              EpochPhase
    boundary_time:      Timestamp         // Nominal boundary (before jitter)
    jittered_boundary:  Timestamp         // Actual boundary (after jitter)
    jitter_seed:        bytes32           // hash(epoch_number || network_entropy)
    operations:         List<Operation>   // Local collection buffer
    broadcast_set:      Set<Operation>    // Operations received via RBC
    ordered_batch:      List<Operation>   // Canonically sorted
    settlement_result:  SettlementResult  // Output of settlement function
    conservation_check: bool              // Post-settlement invariant check
```

### 2.3.2 Operation Types

All state-mutating operations in the HDL are represented as typed operations collected during the COLLECTING phase:

```
ENUM OperationType:
    // Budget operations
    AIC_TRANSFER            // SB transfer between accounts
    AIC_STAKE               // Lock AIC as collateral
    AIC_UNSTAKE             // Unlock staked AIC (subject to cooldown)
    PC_EARN                 // Protocol Credit earning (quality-gated)
    PC_SPEND                // Protocol Credit consumption
    PC_DECAY                // Epoch-end PC decay (10%)
    CS_ALLOCATE             // Capacity Slice allocation from market
    CS_RELEASE              // Capacity Slice release
    CS_REVERT               // Capacity Slice revert from pending timeout

    // Settlement operations
    REWARD_B_CLASS          // B-class settlement reward distribution
    REWARD_V_CLASS          // V-class settlement reward distribution
    REWARD_G_CLASS          // G-class settlement reward distribution
    SLASH                   // Slashing penalty application

    // Capacity market operations
    CAPACITY_BID            // Sealed bid in capacity auction
    CAPACITY_CLEAR          // Auction clearing result
    CAPACITY_SPOT           // Mid-epoch spot market transaction

    // Governance operations
    TREASURY_MINT           // New AIC issuance from treasury
    TREASURY_BURN           // AIC removal (timeout fees, etc.)
    PARAMETER_UPDATE        // Governance parameter change

    // Pending state operations
    PENDING_INITIATE        // Begin pending state (requires collateral)
    PENDING_COMPLETE        // Resolve pending state successfully
    PENDING_TIMEOUT         // Auto-revert timed-out pending state
```

**Definition 2.5 (Operation).** A single state-mutating instruction:

```
STRUCTURE Operation:
    op_id:          bytes32              // Unique operation identifier
    op_type:        OperationType
    submitter_id:   AgentID              // Entity that submitted the operation
    timestamp:      Timestamp            // Submission timestamp
    timestamp_hash: bytes32              // hash(timestamp || submitter_id || op_id)
    epoch_number:   uint64               // Epoch this operation belongs to
    payload:        OperationPayload     // Type-specific data
    signature:      bytes64              // Ed25519 signature by submitter
    pc_cost:        uint64               // Protocol Credit cost (congestion-adjusted)
```

Payload schemas are type-specific. Representative examples:

```
STRUCTURE TransferPayload:
    from_account:   AgentID
    to_account:     AgentID
    amount:         uint64

STRUCTURE RewardPayload:
    recipient:      AgentID
    stream:         SettlementStream     // Which of four streams
    base_amount:    uint64
    npv_adjustment: float64              // NPV normalization factor

STRUCTURE SlashPayload:
    violator:       AgentID
    violation_type: ViolationType
    offense_number: uint32               // Determines graduated penalty
    penalty_amount: uint64
    reporter_id:    AgentID              // Entity that reported the violation (or NULL)
```

### 2.3.3 Reliable Broadcast Protocol

EABS uses **Bracha's Reliable Broadcast (RBC)** for the BROADCASTING phase. This protocol was selected for networks of up to 100 nodes based on the following comparative analysis:

| Protocol | Message Complexity | Fault Tolerance | Ordering | Scale |
|---|---|---|---|---|
| Bracha's RBC | O(n^2) per broadcast | f < n/3 crash faults | None (by design) | Up to ~100 nodes |
| HotStuff | O(n) per broadcast | f < n/3 Byzantine | Total ordering | 100-1000 nodes |
| Gossip-based | O(n log n) probabilistic | Probabilistic delivery | None | 1000+ nodes |

**Selection rationale:** Bracha's RBC provides exactly the guarantees EABS needs — reliable delivery without ordering — at the lowest complexity for the target scale. EABS does not need ordering from the broadcast protocol because ordering is computed deterministically post-broadcast. Full BFT consensus (HotStuff) would provide ordering guarantees that EABS does not use, at higher implementation complexity.

**Protocol specification (adapted for EABS):**

```
PROTOCOL BrachaRBC(sender: NodeID, operation: Operation, n: uint, f: uint):
    // Fault tolerance: f < n/3 crash faults (n >= 3f + 1)

    // Phase 1: SEND
    IF self == sender:
        FOR each node j IN network:
            SEND (INITIAL, epoch, operation) TO j

    // Phase 2: ECHO
    ON RECEIVE (INITIAL, epoch, operation) FROM sender:
        IF NOT already_echoed[epoch][operation.op_id]:
            already_echoed[epoch][operation.op_id] = true
            FOR each node j IN network:
                SEND (ECHO, epoch, operation.op_id, hash(operation)) TO j

    // Phase 3: READY
    ON RECEIVE (ECHO, epoch, op_id, op_hash) FROM node j:
        echo_count[epoch][op_id][op_hash] += 1
        IF echo_count[epoch][op_id][op_hash] >= ceil((n + f + 1) / 2)
           AND NOT already_readied[epoch][op_id]:
            already_readied[epoch][op_id] = true
            FOR each node j IN network:
                SEND (READY, epoch, op_id, op_hash) TO j

    ON RECEIVE (READY, epoch, op_id, op_hash) FROM node j:
        ready_count[epoch][op_id][op_hash] += 1

        // Amplification: if enough READY, send READY too
        IF ready_count[epoch][op_id][op_hash] >= f + 1
           AND NOT already_readied[epoch][op_id]:
            already_readied[epoch][op_id] = true
            FOR each node j IN network:
                SEND (READY, epoch, op_id, op_hash) TO j

        // Delivery threshold
        IF ready_count[epoch][op_id][op_hash] >= 2f + 1:
            DELIVER(epoch, operation)
            broadcast_set[epoch].add(operation)

PROPERTIES:
    Validity:   If sender is honest and broadcasts O, all honest nodes deliver O.
    Agreement:  If any honest node delivers O, all honest nodes deliver O.
    Integrity:  Every honest node delivers at most one operation per op_id.
    No ordering guarantee (by design — ordering handled post-broadcast).
```

**Message complexity analysis:**

For n nodes broadcasting m operations per epoch:
- Each operation: O(n^2) messages (n INITIAL + n^2 ECHO + n^2 READY)
- Total per epoch: O(m * n^2)
- n=50, m=1000: ~2.5M messages/epoch
- At 60s epochs: ~42K messages/second
- At 100 bytes/message: ~4.2 MB/second bandwidth

This is well within modern network capacity. For networks exceeding 100 nodes, the architecture transitions to HotStuff-inspired linear broadcast via G-class governance parameter change.

**Netting optimization.** Following the CLS model (which reduces $6.6T gross to ~$300B net daily), EABS implements intra-epoch netting before broadcast. If agent A transfers 50 AIC to B and B transfers 30 AIC to A within the same epoch, only the net transfer (A to B: 20 AIC) is broadcast and settled. Estimated reduction: 30-60% of message volume under typical workloads.

```
FUNCTION net_operations(operations: List<Operation>) -> List<Operation>:
    transfer_pairs = Map<(AgentID, AgentID), int64>{}
    non_transfers = []

    FOR each op IN operations:
        IF op.op_type == AIC_TRANSFER:
            key = (op.payload.from_account, op.payload.to_account)
            reverse_key = (op.payload.to_account, op.payload.from_account)
            transfer_pairs[key] += op.payload.amount
            transfer_pairs[reverse_key] -= op.payload.amount
        ELSE:
            non_transfers.append(op)

    netted = []
    seen = Set{}
    FOR each (from_id, to_id), net_amount IN transfer_pairs:
        canonical = (min(from_id, to_id), max(from_id, to_id))
        IF canonical IN seen:
            CONTINUE
        seen.add(canonical)
        IF net_amount > 0:
            netted.append(Operation{
                op_type: AIC_TRANSFER,
                payload: {from: from_id, to: to_id, amount: net_amount},
            })
        ELIF net_amount < 0:
            netted.append(Operation{
                op_type: AIC_TRANSFER,
                payload: {from: to_id, to: from_id, amount: abs(net_amount)},
            })

    RETURN non_transfers + netted
```

### 2.3.4 Deterministic Ordering Algorithm

After Reliable Broadcast delivers the epoch's operation set to all honest nodes, each node independently applies the same deterministic ordering algorithm. Because all honest nodes receive the same set (by the Agreement property of RBC), they all produce the same ordered batch.

```
FUNCTION deterministic_order(operations: Set<Operation>) -> List<Operation>:
    // Three-level canonical sort:
    // 1. Operation type priority (encodes critical dependencies)
    // 2. Timestamp hash (deterministic, non-manipulable tie-breaking)
    // 3. Submitter ID (final tie-breaker)

    CONST TYPE_PRIORITY = {
        TREASURY_MINT:       0,     // Establish supply first
        TREASURY_BURN:       1,
        PENDING_TIMEOUT:     2,     // Free resources before new ops
        PENDING_COMPLETE:    3,
        SLASH:               4,     // Penalize before rewarding
        AIC_UNSTAKE:         5,
        CS_REVERT:           6,
        CS_RELEASE:          7,
        PC_DECAY:            8,     // Decay before earning
        AIC_TRANSFER:        9,
        AIC_STAKE:          10,
        PC_EARN:            11,
        PC_SPEND:           12,
        CS_ALLOCATE:        13,
        CAPACITY_CLEAR:     14,
        CAPACITY_SPOT:      15,
        CAPACITY_BID:       16,
        REWARD_B_CLASS:     17,     // Rewards after all state changes
        REWARD_V_CLASS:     18,
        REWARD_G_CLASS:     19,
        PENDING_INITIATE:   20,     // New pendings last
        PARAMETER_UPDATE:   21,
    }

    sorted = operations.to_list()
    sorted.sort(key = lambda op: (
        TYPE_PRIORITY[op.op_type],
        op.timestamp_hash,           // bytes32 lexicographic
        op.submitter_id              // AgentID lexicographic
    ))
    RETURN sorted
```

**Ordering rationale.** The type priority ordering encodes critical dependencies:

1. **Treasury first:** Minting and burning establish the epoch's total supply before transfers.
2. **Pending resolutions before new operations:** Timed-out pendings free resources for new operations.
3. **Slashing before rewards:** Penalties applied before rewards distributed, ensuring slashed entities do not receive rewards on penalized stake.
4. **Unstaking and releases before allocations:** Resources freed before new allocations consume them.
5. **Decay before earning:** PC decay applied before new earnings, preventing earn-then-decay ordering manipulation.
6. **Transfers before stakes:** AIC must be in account before staking.
7. **Rewards after all state changes:** Settlement rewards computed on epoch's final state.
8. **New pendings last:** Pending initiations processed after all other operations.

**Invariant ORDER-1:** For any two honest nodes A and B that both complete Reliable Broadcast for epoch E: deterministic_order(A.broadcast_set[E]) == deterministic_order(B.broadcast_set[E]).

**Proof sketch:** By the Agreement property of Bracha's RBC, A.broadcast_set[E] == B.broadcast_set[E]. The sort function is a pure function of its inputs (no external state, no randomness). Therefore the outputs are identical.  QED.

### 2.3.5 Settlement Function

The settlement function is the core of EABS. It takes an ordered batch and a pre-settlement state snapshot, producing a post-settlement state with conservation guarantee.

```
STRUCTURE SettlementState:
    accounts:           Map<AgentID, AccountState>
    total_aic_supply:   uint64
    total_cs_supply:    Map<ResourceType, uint64>
    epoch_number:       uint64
    treasury_balance:   uint64
    reward_pools:       Map<SettlementStream, uint64>
    pending_registry:   Map<PendingID, PendingState>
    parameter_set:      ProtocolParameters
    settlement_hash:    bytes32          // Hash of entire settled state
    unallocated_cs:     Map<ResourceType, uint64>

STRUCTURE SettlementResult:
    pre_state_hash:     bytes32
    post_state:         SettlementState
    post_state_hash:    bytes32
    operations_applied: uint64
    operations_rejected: List<(Operation, RejectionReason)>
    conservation_valid: bool
    epoch_number:       uint64
    computation_time_ms: uint64
```

**Settlement function pseudocode:**

```
FUNCTION settle_epoch(
    pre_state: SettlementState,
    ordered_batch: List<Operation>,
    epoch_number: uint64
) -> SettlementResult:

    state = deep_copy(pre_state)
    state.epoch_number = epoch_number
    pre_state_hash = hash(pre_state)
    rejected = []

    // Process each operation in deterministic order
    FOR each op IN ordered_batch:
        result = apply_operation(state, op)
        IF result.success:
            state = result.new_state
        ELSE:
            rejected.append((op, result.reason))

    // Post-batch conservation check
    conservation_valid = check_conservation(state)

    IF NOT conservation_valid:
        // CRITICAL: Conservation violated — enter recovery
        TRIGGER recovery_protocol(pre_state, ordered_batch, epoch_number)
        RETURN SettlementResult{
            pre_state_hash: pre_state_hash,
            post_state: pre_state,          // Revert to pre-state
            post_state_hash: hash(pre_state),
            operations_applied: 0,
            operations_rejected: ordered_batch.map(
                op -> (op, CONSERVATION_VIOLATION)),
            conservation_valid: false,
            epoch_number: epoch_number,
        }

    post_state_hash = hash(state)

    RETURN SettlementResult{
        pre_state_hash:      pre_state_hash,
        post_state:          state,
        post_state_hash:     post_state_hash,
        operations_applied:  len(ordered_batch) - len(rejected),
        operations_rejected: rejected,
        conservation_valid:  true,
        epoch_number:        epoch_number,
    }
```

### 2.3.6 Per-Operation Application

All operation types are specified below with complete pseudocode.

```
FUNCTION apply_operation(state: SettlementState, op: Operation) -> ApplyResult:
    SWITCH op.op_type:

        CASE AIC_TRANSFER:
            from_acct = state.accounts[op.payload.from_account]
            to_acct = state.accounts[op.payload.to_account]
            IF from_acct.aic_balance.value() < op.payload.amount:
                RETURN Failure(INSUFFICIENT_BALANCE)
            from_acct.aic_balance.decrement(op.submitter_id, op.payload.amount)
            to_acct.aic_balance.increment(op.submitter_id, op.payload.amount)
            RETURN Success(state)

        CASE SLASH:
            violator = state.accounts[op.payload.violator]
            penalty = compute_graduated_penalty(
                op.payload.offense_number,
                violator.staked_aic.value(),
                state.parameter_set.slashing_schedule)
            IF penalty > violator.staked_aic.value():
                penalty = violator.staked_aic.value()

            // Three-way split (per Section 10.5 SLASH-DIST)
            burn_amount = floor(penalty * 0.50)
            treasury_amount = floor(penalty * 0.30)
            reporter_amount = penalty - burn_amount - treasury_amount  // absorbs rounding

            // Apply atomically
            violator.staked_aic.decrement(op.submitter_id, penalty)
            state.treasury_balance += treasury_amount
            state.total_aic_supply -= burn_amount                      // deflationary burn
            IF op.payload.reporter_id != NULL:
                reporter = state.accounts[op.payload.reporter_id]
                reporter.aic_balance.increment(op.submitter_id, reporter_amount)
            ELSE:
                // System-detected violation (no reporter) — reporter share to treasury
                state.treasury_balance += reporter_amount

            violator.violation_count = max(
                violator.violation_count, op.payload.offense_number)
            RETURN Success(state)

        CASE PC_DECAY:
            FOR each account IN state.accounts.values():
                decay_amount = floor(account.pc_balance.value() * 0.10)
                account.pc_balance.decrement(op.submitter_id, decay_amount)
            RETURN Success(state)

        CASE PC_EARN:
            acct = state.accounts[op.submitter_id]

            // Verify PCVM attestation (C5 identity-binding)
            IF NOT verify_pcvm_attestation(op.payload.attestation):
                RETURN Failure(INVALID_ATTESTATION)

            // Compute earning (sublinear: k * sqrt(quality_actions))
            earning = floor(
                state.parameter_set.pc_earning_coefficient *
                sqrt(op.payload.quality_actions))

            // Enforce balance cap: pc_balance <= 10 * epoch_earning_rate
            cap = 10 * earning
            IF acct.pc_balance.value() + earning > cap:
                earning = max(0, cap - acct.pc_balance.value())

            acct.pc_balance.increment(op.submitter_id, earning)
            RETURN Success(state)

        CASE PC_SPEND:
            acct = state.accounts[op.submitter_id]

            // Compute congestion-adjusted cost
            epoch_load = state.current_epoch_load()
            cost = compute_congestion_cost(
                op.payload.base_cost,
                state.parameter_set,
                epoch_load)

            IF acct.pc_balance.value() < cost:
                RETURN Failure(INSUFFICIENT_PC)

            acct.pc_balance.decrement(op.submitter_id, cost)
            RETURN Success(state)

        CASE REWARD_B_CLASS:
            recipient = state.accounts[op.payload.recipient]
            adjusted = floor(op.payload.base_amount * op.payload.npv_adjustment)
            IF adjusted > state.reward_pools[op.payload.stream]:
                RETURN Failure(INSUFFICIENT_REWARD_POOL)
            state.reward_pools[op.payload.stream] -= adjusted
            recipient.aic_balance.increment(op.submitter_id, adjusted)
            RETURN Success(state)

        CASE REWARD_V_CLASS:
            recipient = state.accounts[op.payload.recipient]
            delay_epochs = op.payload.delay_epochs  // V-class period (default 5)
            r = state.parameter_set.epoch_discount_rate  // 0.002

            // NPV premium for delayed settlement: (1+r)^delay
            npv_factor = pow(1.0 + r, delay_epochs)
            adjusted = floor(op.payload.base_amount * npv_factor)

            IF adjusted > state.reward_pools[VERIFICATION]:
                RETURN Failure(INSUFFICIENT_REWARD_POOL)

            state.reward_pools[VERIFICATION] -= adjusted
            recipient.aic_balance.increment(op.submitter_id, adjusted)
            RETURN Success(state)

        CASE REWARD_G_CLASS:
            recipient = state.accounts[op.payload.recipient]
            delay_epochs = op.payload.delay_epochs  // variable, 10-50 typical
            r = state.parameter_set.epoch_discount_rate

            // NPV premium for governance settlement delay
            npv_factor = pow(1.0 + r, delay_epochs)
            adjusted = floor(op.payload.base_amount * npv_factor)

            IF adjusted > state.reward_pools[GOVERNANCE]:
                RETURN Failure(INSUFFICIENT_REWARD_POOL)

            state.reward_pools[GOVERNANCE] -= adjusted
            recipient.aic_balance.increment(op.submitter_id, adjusted)
            RETURN Success(state)

        CASE AIC_STAKE:
            acct = state.accounts[op.submitter_id]
            IF acct.aic_balance.value() < op.payload.amount:
                RETURN Failure(INSUFFICIENT_BALANCE)
            acct.aic_balance.decrement(op.submitter_id, op.payload.amount)
            acct.staked_aic.increment(op.submitter_id, op.payload.amount)
            RETURN Success(state)

        CASE AIC_UNSTAKE:
            acct = state.accounts[op.submitter_id]
            IF acct.staked_aic.value() < op.payload.amount:
                RETURN Failure(INSUFFICIENT_STAKE)
            IF state.epoch_number - acct.last_stake_epoch < UNSTAKE_COOLDOWN:
                RETURN Failure(COOLDOWN_NOT_ELAPSED)
            acct.staked_aic.decrement(op.submitter_id, op.payload.amount)
            acct.aic_balance.increment(op.submitter_id, op.payload.amount)
            RETURN Success(state)

        CASE PENDING_INITIATE:
            acct = state.accounts[op.submitter_id]
            collateral = floor(op.payload.amount * 0.05)
            // Per-entity pending cap: 10% of total supply
            IF acct.pending_out.value() + op.payload.amount >
               floor(state.total_aic_supply * 0.10):
                RETURN Failure(ENTITY_PENDING_CAP_EXCEEDED)
            // Global pending cap: 25% of total supply
            total_pending = sum(a.pending_out.value()
                               for a in state.accounts.values())
            IF total_pending + op.payload.amount >
               floor(state.total_aic_supply * 0.25):
                RETURN Failure(GLOBAL_PENDING_CAP_EXCEEDED)
            IF acct.aic_balance.value() < collateral:
                RETURN Failure(INSUFFICIENT_COLLATERAL)
            acct.aic_balance.decrement(op.submitter_id, collateral)
            acct.collateral_held.increment(op.submitter_id, collateral)
            acct.pending_out.increment(op.submitter_id, op.payload.amount)
            counterparty = state.accounts[op.payload.counterparty]
            counterparty.pending_in.increment(op.submitter_id, op.payload.amount)
            state.pending_registry[op.payload.pending_id] = PendingState{
                initiator_id: op.submitter_id,
                amount: op.payload.amount,
                collateral: collateral,
                epoch_initiated: state.epoch_number,
                direction: OUTBOUND,
                counterparty_id: op.payload.counterparty,
            }
            RETURN Success(state)

        CASE PENDING_COMPLETE:
            pending = state.pending_registry[op.payload.pending_id]
            initiator = state.accounts[pending.initiator_id]
            counterparty = state.accounts[pending.counterparty_id]
            initiator.pending_out.decrement(op.submitter_id, pending.amount)
            counterparty.pending_in.decrement(op.submitter_id, pending.amount)
            counterparty.aic_balance.increment(op.submitter_id, pending.amount)
            initiator.collateral_held.decrement(op.submitter_id, pending.collateral)
            initiator.aic_balance.increment(op.submitter_id, pending.collateral)
            DELETE state.pending_registry[op.payload.pending_id]
            RETURN Success(state)

        CASE PENDING_TIMEOUT:
            pending = state.pending_registry[op.payload.pending_id]
            IF pending.epoch_initiated + 3 > state.epoch_number:
                RETURN Failure(PENDING_NOT_YET_TIMED_OUT)
            initiator = state.accounts[pending.initiator_id]
            counterparty = state.accounts[pending.counterparty_id]
            timeout_fee = floor(pending.amount * 0.02)
            collateral_return = pending.collateral - timeout_fee
            state.total_aic_supply -= timeout_fee       // Fee burned
            initiator.collateral_held.decrement(op.submitter_id, pending.collateral)
            initiator.aic_balance.increment(op.submitter_id,
                pending.amount + collateral_return)
            initiator.pending_out.decrement(op.submitter_id, pending.amount)
            counterparty.pending_in.decrement(op.submitter_id, pending.amount)
            DELETE state.pending_registry[op.payload.pending_id]
            RETURN Success(state)

        CASE TREASURY_MINT:
            IF NOT verify_governance_authorization(op):
                RETURN Failure(UNAUTHORIZED_MINT)
            state.total_aic_supply += op.payload.amount
            state.treasury_balance += op.payload.amount
            RETURN Success(state)

        CASE TREASURY_BURN:
            IF state.treasury_balance < op.payload.amount:
                RETURN Failure(INSUFFICIENT_TREASURY)
            state.total_aic_supply -= op.payload.amount
            state.treasury_balance -= op.payload.amount
            RETURN Success(state)

        CASE CS_ALLOCATE:
            acct = state.accounts[op.submitter_id]
            rt = op.payload.resource_type
            qty = op.payload.quantity

            // Check unallocated supply
            IF state.unallocated_cs[rt] < qty:
                RETURN Failure(INSUFFICIENT_CS_SUPPLY)

            // Check position limit (POS-1): max 15% of total per entity
            current_held = acct.cs_allocation[rt].value()
            IF current_held + qty > floor(state.total_cs_supply[rt] * 0.15):
                RETURN Failure(POSITION_LIMIT_EXCEEDED)

            // Allocate
            state.unallocated_cs[rt] -= qty
            acct.cs_allocation[rt].increment(op.submitter_id, qty)
            RETURN Success(state)

        CASE CS_RELEASE:
            acct = state.accounts[op.submitter_id]
            rt = op.payload.resource_type
            qty = op.payload.quantity

            IF acct.cs_allocation[rt].value() < qty:
                RETURN Failure(INSUFFICIENT_CS_HELD)

            acct.cs_allocation[rt].decrement(op.submitter_id, qty)
            state.unallocated_cs[rt] += qty
            RETURN Success(state)

        CASE CS_REVERT:
            // Revert a pending CS allocation that timed out
            pending = state.pending_registry[op.payload.pending_id]
            IF pending.resource_type == NONE:
                RETURN Failure(NOT_CS_PENDING)

            rt = pending.resource_type
            qty = pending.amount

            // Return to unallocated pool
            state.unallocated_cs[rt] += qty

            // Remove from pending registry
            DELETE state.pending_registry[op.payload.pending_id]
            RETURN Success(state)

        CASE CAPACITY_BID:
            // Bids are collected during COLLECTING phase and processed at clearing.
            acct = state.accounts[op.submitter_id]
            rt = op.payload.resource_type

            // Validate commitment deposit (0.5% of bid value)
            bid_value = op.payload.quantity * op.payload.max_price
            deposit = ceil(bid_value * 0.005)
            IF acct.aic_balance.value() < deposit:
                RETURN Failure(INSUFFICIENT_BID_DEPOSIT)

            // Reserve deposit
            acct.aic_balance.decrement(op.submitter_id, deposit)
            acct.collateral_held.increment(op.submitter_id, deposit)

            // Record bid for clearing phase
            state.capacity_bids[op.epoch_number].append(op.payload)
            RETURN Success(state)

        CASE CAPACITY_CLEAR:
            // Generated by the auction clearing algorithm (Section 8.5)
            // This op is system-generated, not user-submitted
            IF op.submitter_id != SYSTEM_ID:
                RETURN Failure(UNAUTHORIZED_CLEAR)

            FOR each (bidder_id, qty) IN op.payload.allocations:
                bidder = state.accounts[bidder_id]
                rt = op.payload.resource_type
                cost = qty * op.payload.clearing_price

                // Deduct payment from bidder
                IF bidder.aic_balance.value() < cost:
                    // Bidder can't afford at clearing price — skip allocation
                    CONTINUE
                bidder.aic_balance.decrement(SYSTEM_ID, cost)
                state.treasury_balance += cost

                // Release commitment deposit
                deposit = state.bid_deposits[bidder_id][op.epoch_number]
                bidder.collateral_held.decrement(SYSTEM_ID, deposit)
                bidder.aic_balance.increment(SYSTEM_ID, deposit)

                // Allocate capacity
                state.unallocated_cs[rt] -= qty
                bidder.cs_allocation[rt].increment(SYSTEM_ID, qty)

            RETURN Success(state)

        CASE CAPACITY_SPOT:
            // Mid-epoch spot purchase at a premium over last clearing price
            acct = state.accounts[op.submitter_id]
            rt = op.payload.resource_type
            qty = op.payload.quantity

            // Spot price = last clearing price * 1.5 (premium for immediacy)
            spot_price = state.last_clearing_price[rt] * 1.5
            cost = qty * spot_price

            IF acct.aic_balance.value() < cost:
                RETURN Failure(INSUFFICIENT_BALANCE)
            IF state.unallocated_cs[rt] < qty:
                RETURN Failure(INSUFFICIENT_SPOT_SUPPLY)

            // Check position limit
            current_held = acct.cs_allocation[rt].value()
            IF current_held + qty > floor(state.total_cs_supply[rt] * 0.15):
                RETURN Failure(POSITION_LIMIT_EXCEEDED)

            acct.aic_balance.decrement(op.submitter_id, cost)
            state.treasury_balance += cost
            state.unallocated_cs[rt] -= qty
            acct.cs_allocation[rt].increment(op.submitter_id, qty)
            RETURN Success(state)

        CASE PARAMETER_UPDATE:
            // Must be authorized by governance (G-class settlement)
            IF NOT verify_governance_authorization(op):
                RETURN Failure(UNAUTHORIZED_PARAMETER_CHANGE)

            param_name = op.payload.parameter_name
            new_value = op.payload.new_value
            old_value = state.parameter_set[param_name]

            // Enforce max change rate (20% per governance cycle)
            IF abs(new_value - old_value) / old_value > 0.20:
                RETURN Failure(CHANGE_RATE_EXCEEDED)

            // Enforce safe range bounds
            IF NOT in_safe_range(param_name, new_value):
                RETURN Failure(OUT_OF_SAFE_RANGE)

            // Enforce cooldown (parameter locked for 10 ticks after last change)
            IF state.parameter_last_changed[param_name] + 10 > state.epoch_number:
                RETURN Failure(COOLDOWN_NOT_ELAPSED)

            // Apply
            state.parameter_set[param_name] = new_value
            state.parameter_last_changed[param_name] = state.epoch_number
            RETURN Success(state)
```

### 2.3.7 Conservation Enforcement

**Definition 2.6 (Conservation Invariant).** The CSO conservation invariant is a predicate over SettlementState that must hold after every epoch settlement.

```
FUNCTION check_conservation(state: SettlementState) -> bool:
    // AIC Conservation (CONS-1 — CANONICAL)
    total_aic_in_accounts = 0
    total_aic_staked = 0
    total_pending_out = 0
    total_pending_in = 0
    total_collateral = 0

    FOR each account IN state.accounts.values():
        total_aic_in_accounts += account.aic_balance.value()
        total_aic_staked += account.staked_aic.value()
        total_pending_out += account.pending_out.value()
        total_pending_in += account.pending_in.value()
        total_collateral += account.collateral_held.value()

    aic_conservation =
        (total_aic_in_accounts + total_aic_staked +
         total_pending_out + total_collateral +
         state.treasury_balance)
        == state.total_aic_supply

    // Auxiliary: Pending Balance (CONS-1a)
    pending_balance = (total_pending_out == total_pending_in)

    // CS Conservation (CONS-2) — per resource type
    cs_conservation = true
    FOR each rt IN state.resource_types:
        total_cs_held = 0
        total_cs_pending = 0
        FOR each account IN state.accounts.values():
            total_cs_held += account.cs_allocation[rt].value()
        FOR each pending IN state.pending_registry.values():
            IF pending.resource_type == rt:
                total_cs_pending += pending.amount
        cs_conservation = cs_conservation AND
            (total_cs_held + total_cs_pending + state.unallocated_cs[rt])
            == state.total_cs_supply[rt]

    RETURN aic_conservation AND pending_balance AND cs_conservation
```

**Invariant CONS-1 (AIC Conservation — CANONICAL).** For every epoch E, after EABS settlement completes:

```
    Sigma_{i}( aic_balance(i, E) )
  + Sigma_{i}( staked_aic(i, E) )
  + Sigma_{i}( pending_out(i, E) )
  + Sigma_{i}( collateral_held(i, E) )
  + treasury_balance(E)
  = total_aic_supply(E)

WITH AUXILIARY INVARIANT CONS-1a:
    Sigma_{i}( pending_out(i, E) ) = Sigma_{i}( pending_in(i, E) )

NOTE: pending_in is NOT in the main equation. It is tracked
separately via CONS-1a. Including both pending_out and pending_in
in the main equation would double-count.
```

**Invariant CONS-2 (CS Conservation).** For every epoch E, after settlement:

```
FOR EVERY resource_type R:
    Sigma(cs_allocation_i(R)) + Sigma(cs_pending_j(R)) + unallocated_cs(R) = total_cs_supply(R)
```

**Invariant CONS-3 (PC Non-Conservation, by design).** Protocol Credits are intentionally non-conserved. They are created (earned) and destroyed (decayed, spent). There is no total_pc_supply invariant. PC is bounded by the per-account cap: pc_balance_i <= 10 * epoch_earning_rate(i).

### 2.3.8 Conservation Proof Sketch

**Theorem 2.2.** If settle_epoch returns conservation_valid = true, then CONS-1 and CONS-2 hold for the post-settlement state.

**Proof.**

*Base case:* At epoch 0 (genesis), total_aic_supply = treasury_balance, all account balances are zero. CONS-1: 0 + 0 + 0 + 0 + treasury_balance = total_aic_supply. Holds trivially. CONS-2: 0 + 0 + 0 = total_cs_supply. Holds trivially.

*Inductive step:* Assume CONS-1 and CONS-2 hold for pre_state (after epoch E-1). We show each operation type preserves conservation:

- **AIC_TRANSFER:** Decrements from_account by X, increments to_account by X. Net change to Sigma(aic_balance_i) = 0. Conservation preserved.
- **AIC_STAKE:** Decrements aic_balance by X, increments staked_aic by X (same account). Net change to LHS of CONS-1 = 0. Preserved.
- **AIC_UNSTAKE:** Reverse of AIC_STAKE. Preserved.
- **SLASH:** Decrements staked_aic by penalty. Distributes: 50% burned (reduces total_aic_supply), 30% to treasury_balance, 20% to reporter aic_balance. LHS delta: -penalty + 0.30*penalty + 0.20*penalty = -0.50*penalty. RHS delta (total_supply): -0.50*penalty. LHS delta = RHS delta. Conservation preserved.
- **TREASURY_MINT:** Increments total_aic_supply by X AND treasury_balance by X. Both sides increase by X. Preserved.
- **TREASURY_BURN:** Decrements total_aic_supply by X AND treasury_balance by X. Both sides decrease by X. Preserved.
- **REWARD_*:** Decrements reward_pool (part of treasury) by X, increments recipient balance by X. Net change to (Sigma(balances) + treasury) = 0. Preserved.
- **PENDING_INITIATE:** Collateral moved from aic_balance to collateral_held. pending_out increases by X. pending_in increases by X (tracked via CONS-1a). Net CONS-1 delta: -(X+collateral) + collateral + X = 0. Preserved.
- **PENDING_COMPLETE:** pending_out decremented by X, counterparty balance incremented by X, collateral returned from collateral_held to aic_balance. Net = 0. Preserved.
- **PENDING_TIMEOUT:** pending_out decremented by X, balance restored minus fee, collateral returned minus fee, fee burned from total_supply. LHS delta = -timeout_fee. RHS delta = -timeout_fee. Preserved.
- **PC_DECAY/PC_EARN/PC_SPEND:** Not part of AIC or CS conservation. No effect on CONS-1 or CONS-2.
- **CS_ALLOCATE/CS_RELEASE/CS_REVERT:** Balanced transfers within CS domain. CONS-2 preserved.
- **CAPACITY_BID:** Moves AIC from aic_balance to collateral_held. Net CONS-1 delta: 0. Preserved.
- **CAPACITY_CLEAR:** Deducts from bidder aic_balance, credits treasury, returns collateral, allocates CS. Net CONS-1 delta: 0. CONS-2: CS moves from unallocated to allocated. Preserved.
- **CAPACITY_SPOT:** Deducts from aic_balance, credits treasury, allocates CS. Net CONS-1 delta: 0. CONS-2 preserved.
- **PARAMETER_UPDATE:** No balance changes. Preserved trivially.

Each operation individually preserves conservation. The settlement function applies them sequentially. By induction over the ordered batch, conservation is preserved after all operations.

The explicit check_conservation call provides runtime verification, catching any implementation bugs that might violate the theoretical guarantee.

**Recovery protocol:** If check_conservation returns false (indicating a bug), the entire epoch batch is rejected and all nodes revert to pre_state. A diagnostic trace is emitted.  QED.

### 2.3.9 Epoch-Consistent Optimistic Reads (ECOR)

**Definition 2.7 (ECOR).** For node N at time t during epoch E:

```
ecor_balance(account, budget_type) =
    settled_balance(account, budget_type, E-1)
    + optimistic_delta(account, budget_type, E)

WHERE:
    settled_balance is the balance after EABS settlement of epoch E-1.
    This value is identical across all honest nodes.

    optimistic_delta is the sum of locally-observed operations
    during epoch E, BEFORE settlement.
    This value MAY differ across nodes.
```

**Properties of ECOR:**

1. After epoch E settles: FOR ALL honest nodes A, B: settled_balance_A(E) == settled_balance_B(E).
2. During epoch E: ecor_balance may differ across nodes by at most the set of operations not yet delivered via CRDT anti-entropy.
3. Monotonic settled state: no settled balance is ever "un-settled."

**Optimistic Delta Tracking:**

```
STRUCTURE OptimisticDelta:
    account_id:     AgentID
    budget_type:    BudgetType          // AIC, PC, CS
    epoch:          uint64
    credits:        uint64              // Sum of positive deltas
    debits:         uint64              // Sum of negative deltas
    operations:     List<OperationID>   // Contributing operations

    FUNCTION net() -> int64:
        RETURN credits - debits

    FUNCTION merge(other: OptimisticDelta) -> OptimisticDelta:
        ASSERT self.account_id == other.account_id
        ASSERT self.budget_type == other.budget_type
        ASSERT self.epoch == other.epoch
        RETURN OptimisticDelta{
            account_id:  self.account_id,
            budget_type: self.budget_type,
            epoch:       self.epoch,
            credits:     max(self.credits, other.credits),
            debits:      max(self.debits, other.debits),
            operations:  union(self.operations, other.operations),
        }
```

**Risk mitigation for optimistic reads:**

1. **High-value operations should wait for settlement.** Operations depending on exact balances (staking, large transfers) should verify against settled state, not ECOR state.
2. **Overdraft detection at settlement.** Operations accepted on optimistic state but failing at settlement are rejected gracefully — analogous to a "bounced check." The submitter is not penalized.
3. **Staleness monitoring.** The system tracks average and maximum gap between ECOR and settled balances. Alerts raised if gap exceeds configurable thresholds.

### 2.3.10 Fault Model and Recovery

**Assumed fault model:**

- **Fault threshold:** f < n/3, where n is total HDL nodes.
- **Fault type:** Crash faults (nodes may stop but do not send conflicting messages).
- **Network model:** Partial synchrony — messages eventually delivered within unknown finite bound Delta.
- **Cryptographic assumptions:** Ed25519 signatures unforgeable; SHA-256 collision-free.

**Justification for crash-fault model:** DSF operates in a semi-permissioned environment where HDL nodes are operated by known infrastructure providers with staked collateral. Byzantine behavior is detectable and punishable via slashing, making crash the expected fault mode. Bracha's RBC already tolerates f < n/3 Byzantine faults if needed.

**Partition handling:**

- **Read path (CRDT):** Both partitions continue serving reads. Availability preserved. Staleness grows.
- **Write path (EABS):** If both partitions have fewer than 2f+1 nodes, settlement stalls until partition heals. If one partition has >= 2f+1 (the majority), that partition continues; minority stalls.
- **Post-partition recovery:** Minority nodes detect staleness, download settled state for missed epochs, re-execute settlement (deterministic verification), and rejoin.

```
PROTOCOL EpochRecovery(stale_node: NodeID, current_epoch: uint64):

    stale_epoch = stale_node.epoch_settled
    gap = current_epoch - stale_epoch

    IF gap == 0:
        RETURN  // Already current

    FOR epoch_e FROM (stale_epoch + 1) TO current_epoch:
        batch = REQUEST_EPOCH_BATCH(epoch_e) FROM any_peer
        expected_pre_hash = stale_node.settlement_state.settlement_hash
        IF batch.pre_state_hash != expected_pre_hash:
            RETRY with different peer (up to f retries)

        result = settle_epoch(stale_node.settlement_state,
                              batch.ordered_batch, epoch_e)

        IF result.post_state_hash != batch.expected_post_hash:
            ALERT: deterministic settlement verification failed
            HALT recovery, escalate to governance

        stale_node.settlement_state = result.post_state
        stale_node.epoch_settled = epoch_e
        update_crdt_from_settlement(stale_node, result.post_state)

    stale_node.phase = COLLECTING
    stale_node.epoch_collecting = current_epoch + 1
```

**Epoch boundary timing:**

```
FUNCTION compute_epoch_boundary(epoch_number: uint64,
                                 params: ProtocolParameters) -> Timestamp:
    nominal = genesis_time + (epoch_number * params.epoch_duration)
    jitter_seed = SHA256(epoch_number || params.network_entropy_source)
    jitter_fraction = (uint64_from_bytes(jitter_seed[0:8]) % 2001 - 1000) / 10000.0
    jitter_ms = floor(params.epoch_duration_ms * jitter_fraction)
    RETURN nominal + jitter_ms

// Canonical: epoch_duration_ms = 60000 (60 seconds = 1 SETTLEMENT_TICK)
// network_entropy_source = hash(previous epoch's settlement_hash)
```

**Invariant EPOCH-1:** All honest nodes compute the same jittered boundary for epoch E, because jitter_seed derives from deterministic inputs.

### 2.3.11 Test Vector: Example Epoch

**Setup.** Three agents (Alpha, Beta, Gamma), one treasury. Genesis state:

```
total_aic_supply = 10000
treasury_balance = 5000
Alpha.aic_balance = 2000, Alpha.staked_aic = 500
Beta.aic_balance  = 1500, Beta.staked_aic  = 300
Gamma.aic_balance = 700,  Gamma.staked_aic = 0
reward_pools = {SCHEDULING: 400, VERIFICATION: 400, COMM: 100, GOV: 100}
```

**Conservation check (pre-state):**
2000 + 1500 + 700 + 500 + 300 + 0 + 0 + 0 + 5000 = 10000. CONS-1 holds.
(Note: collateral_held = 0, pending_out = 0 for all accounts at genesis.)

**Epoch 1 operations (5 operations, ordered by deterministic_order):**

| # | Op Type | Details | Priority |
|---|---|---|---|
| 1 | SLASH | Gamma, offense #1, 1% of staked (= 0, Gamma has no stake) | 4 |
| 2 | AIC_TRANSFER | Alpha -> Beta, 200 AIC | 9 |
| 3 | AIC_STAKE | Beta stakes 100 AIC | 10 |
| 4 | REWARD_B_CLASS | Alpha, scheduling, base=50, npv=0.98 | 17 |
| 5 | REWARD_B_CLASS | Beta, scheduling, base=30, npv=0.98 | 17 |

**Processing:**

1. SLASH Gamma: offense_number=1, penalty = 1% of 0 = 0. No effect.
   State unchanged.

2. AIC_TRANSFER Alpha->Beta 200:
   Alpha.aic_balance: 2000 - 200 = 1800
   Beta.aic_balance: 1500 + 200 = 1700

3. AIC_STAKE Beta 100:
   Beta.aic_balance: 1700 - 100 = 1600
   Beta.staked_aic: 300 + 100 = 400

4. REWARD_B_CLASS Alpha: floor(50 * 0.98) = 49 AIC
   reward_pools[SCHEDULING]: 400 - 49 = 351
   Alpha.aic_balance: 1800 + 49 = 1849

5. REWARD_B_CLASS Beta: floor(30 * 0.98) = 29 AIC
   reward_pools[SCHEDULING]: 351 - 29 = 322
   Beta.aic_balance: 1600 + 29 = 1629

**Post-settlement state:**
```
Alpha.aic_balance = 1849, Alpha.staked_aic = 500
Beta.aic_balance  = 1629, Beta.staked_aic  = 400
Gamma.aic_balance = 700,  Gamma.staked_aic = 0
treasury_balance  = 5000
reward_pools[SCHEDULING] = 322
total_aic_supply = 10000
```

**Conservation check (post-state):**
1849 + 1629 + 700 + 500 + 400 + 0 + 0 + 0 + 5000 = 10078. But reward pools are part of treasury.
treasury_effective = 5000 - (400-322) = 5000 - 78 = 4922.
Actual: 1849 + 1629 + 700 + 500 + 400 + 4922 = 10000. CONS-1 holds.

(Note: reward_pools are sub-accounts of treasury_balance. The 78 AIC distributed as rewards came from the treasury's reward pool allocation.)

---

# Section 3: Three-Budget Economic Model

## 3.1 Design Philosophy

Traditional blockchain economies use a single token for all economic functions. Ethereum's ETH serves simultaneously as payment, gas, staking collateral, and governance weight. This conflation creates attack vectors where dominance in one function automatically confers dominance in all others.

DSF separates economic functions into three distinct budget types with different creation, destruction, transferability, and decay properties. The design explicitly acknowledges that perfect economic isolation between budgets is impossible — per the Adversarial Analysis and Science Assessment. Instead, it implements **calibrated friction**: mechanisms that make cross-budget arbitrage unprofitable at protocol-relevant scales while accepting that some implicit exchange will occur.

This is analogous to how fiat economies have distinct instruments (cash, credit, bonds) that are formally separate but economically interrelated. The separation provides functional value even without absolute isolation.

## 3.2 Sponsor Budget (SB) — AIC

**Definition 3.1 (AIC — Atrahasis Internal Credit).**

```
STRUCTURE SponsorBudget:
    token_name:       "AIC"
    transferability:  TRANSFERABLE
    decay_rate:       0.0 (no decay)
    creation:         Treasury minting only (TREASURY_MINT)
    destruction:      Treasury burning, timeout fees, slashing
    settlement_path:  EABS write path (conservation-guaranteed)
    read_path:        CRDT (ECOR optimistic reads)
    conservation:     YES — CONS-1 invariant enforced at every epoch
```

AIC serves five functions:
1. Primary payment instrument for task sponsorship
2. Staking collateral for capability-weighted stake
3. Governance weight (proportional to staked AIC)
4. Settlement reward denomination
5. Capacity market bidding currency

```
AIC Flow:

    TREASURY
       |
       | TREASURY_MINT (governance-authorized)
       v
    AIC CIRCULATION
       |
       +-- AIC_TRANSFER between agents
       +-- AIC_STAKE (lock as collateral) <-> AIC_UNSTAKE (unlock)
       +-- REWARD_* (earned from settlement streams)
       +-- SLASH (penalty -> 50% burn / 30% treasury / 20% reporter)
       +-- CS payment (capacity market bids)
       |
       | TREASURY_BURN (timeout fees, protocol burns)
       v
    DESTROYED
```

## 3.3 Protocol Credits (PC)

**Definition 3.2 (Protocol Credits).**

```
STRUCTURE ProtocolCredits:
    token_name:       "PC"
    transferability:  NON_TRANSFERABLE (identity-bound)
    decay_rate:       0.10 per epoch (10%)
    creation:         Quality-gated earning via PC_EARN
    destruction:      Decay (PC_DECAY), spending (PC_SPEND)
    conservation:     NO — intentionally non-conserved
```

PC serves three functions:
1. Spam control (rate limiting)
2. Proof of active, value-creating participation
3. Access gating for protocol operations

### 3.3.1 PC Earning (Sublinear)

```
FUNCTION compute_pc_earning(
    quality_actions: uint64,
    params: ProtocolParameters
) -> uint64:
    // Sublinear: k * sqrt(quality_actions)
    // Doubling activity less than doubles earnings
    raw_earning = params.pc_earning_coefficient * sqrt(quality_actions)
    RETURN floor(raw_earning)

// Example (k = 10):
// quality_actions =   1 -> PC earned =  10
// quality_actions =   4 -> PC earned =  20
// quality_actions =   9 -> PC earned =  30
// quality_actions =  16 -> PC earned =  40
// quality_actions = 100 -> PC earned = 100
// quality_actions = 400 -> PC earned = 200  (4x activity for 2x earnings)
```

Quality actions are gated: only successful task completions, accepted verifications, and approved proposals count. Rejected tasks and failed verifications earn zero.

### 3.3.2 PC Spending (Congestion-Priced)

```
FUNCTION compute_congestion_cost(
    base_cost: uint64,
    params: ProtocolParameters,
    epoch_load: float64          // current_ops / target_ops
) -> uint64:
    // Quadratic: base * (1 + load^2)
    congestion_multiplier = 1.0 + (epoch_load * epoch_load)
    RETURN ceil(base_cost * congestion_multiplier)

// Example (base_cost = 1 PC):
// load = 0.5 -> cost = 1.25 PC
// load = 1.0 -> cost = 2.0 PC
// load = 2.0 -> cost = 5.0 PC
// load = 3.0 -> cost = 10.0 PC
```

### 3.3.3 PC Decay

10% flat decay applied once per epoch during SETTLING phase. PCs destroyed by decay cease to exist — they do not transfer to treasury or any other account.

### 3.3.4 PC Balance Cap

```
INVARIANT PC-CAP:
    FOR each account A:
        A.pc_balance <= 10 * epoch_earning_rate(A)
```

Combined with 10% decay, steady-state maximum approximately equals earning_rate / 0.10 = 10 * earning_rate, matching the cap.

### 3.3.5 PC Identity Binding

PC earning requires cryptographic proof that the earner (not a delegate) performed the work, using C5 PCVM's Verification Trust Descriptor infrastructure:

```
FUNCTION verify_pc_identity_binding(
    agent: AgentID, action: QualityAction, attestation: PCVMAttestation
) -> bool:
    IF NOT verify_pcvm_signature(attestation): RETURN false
    IF attestation.agent_id != agent: RETURN false
    IF attestation.action_hash != hash(action): RETURN false
    IF attestation.delegation_depth > 0: RETURN false  // No delegation
    IF attestation.timestamp < current_epoch_start: RETURN false  // Stale
    RETURN true
```

## 3.4 Capacity Slices (CS)

**Definition 3.3 (Capacity Slices).**

```
STRUCTURE CapacitySlices:
    token_name:       "CS"
    backing:          CSO (Capability Service Obligation) backed
    transferability:  LIMITED (via market only, no peer transfer)
    decay_rate:       N/A (use-it-or-lose-it instead)
    creation:         Capacity market clearing (CAPACITY_CLEAR)
    destruction:      Epoch expiry (per-epoch allocations)
    conservation:     YES — CONS-2 enforced at every epoch
```

CS allocations are ephemeral — they exist for one epoch, purchased via sealed-bid auction, and expire at the next epoch boundary. Position limits cap any single entity at 15% of total CS supply.

### 3.4.1 CS Lifecycle

```
T=0%:   Epoch boundary — 60% of CS cleared via auction
T=0-50%: Primary utilization period
T=50%:  Mid-epoch tranche — 20% released (includes reclaimed underutilized)
T=75%:  Final tranche — 20% released
T=100%: All CS expire, fresh auction for next epoch
```

## 3.5 Cross-Budget Friction Analysis

Rather than claiming hard isolation (economically impossible), DSF implements friction that makes arbitrage unprofitable:

| Mechanism | Attack Mitigated | Friction Level |
|---|---|---|
| PC identity-binding | PC-as-a-service delegation | HIGH (cryptographic) |
| CS position limits (15%) | Capacity cornering | MEDIUM |
| Cross-budget flow monitoring | Systematic SB->PC conversion | MEDIUM (governance alerts) |
| Governance alert trigger | Stable implicit exchange rates | LOW (requires human review) |

### 3.5.1 Budget Collapse Monitoring and Transition

The three-budget model might collapse to two budgets if friction proves insufficient. The following monitoring and governance transition process addresses this contingency.

```
MONITORING RULE BM-1 (Budget Collapse Assessment):

    The following metrics are tracked per TIDAL_EPOCH (3600s = 60 ticks):

    Metric 1 — Implicit PC/AIC Exchange Rate Stability:
        pc_aic_rate = (total_aic_spent_on_self_tasks / total_pc_earned)
        ALERT if coefficient_of_variation(pc_aic_rate, trailing_60_ticks) < 0.05
        Interpretation: rate is stable enough to constitute a de facto exchange,
                        meaning budget separation has failed.

    Metric 2 — Cross-Budget Flow Volume:
        cross_flow = sum of AIC spent on actions whose primary purpose is
                     PC earning (self-sponsored tasks with no external consumer)
        ALERT if cross_flow > 0.10 * total_aic_settlement_volume
                for 10 consecutive TIDAL_EPOCHs
        Interpretation: >10% of economic activity is cross-budget arbitrage.

    Metric 3 — Third-Budget Marginal Friction:
        friction_delta = attack_cost_with_3_budgets - attack_cost_with_2_budgets
        Computed via quarterly simulation (every 50 SETTLEMENT_TICKs).
        ALERT if friction_delta < 0.02 * median_agent_stake
        Interpretation: the third budget adds less than 2% additional friction
                        to the cheapest known attack vector.

    TRIGGER CONDITION (all three must hold simultaneously for 5 TIDAL_EPOCHs):
        BM-1.metric_1 in ALERT state
        AND BM-1.metric_2 in ALERT state
        AND BM-1.metric_3 in ALERT state
```

```
PROTOCOL BudgetCollapseTransition:

    Phase 0 — TRIGGER:
        BM-1 trigger condition met for 5 consecutive TIDAL_EPOCHs.
        System automatically generates GovernanceProposal of type
        ConstitutionalAmendment (Tier 1 — supermajority required).
        This is the ONLY automated constitutional proposal path.

    Phase 1 — PROPOSAL (auto-generated):
        proposal_type:    ConstitutionalAmendment
        parameter:        budget_type_definitions
        current_value:    SB/PC/CS (three budgets)
        proposed_value:   SB/CS (two budgets — PC merged into SB)
        rationale:        auto-populated with BM-1 metric history
        bond:             5% of treasury balance (from treasury itself)

    Phase 2 — COOLING (20 SETTLEMENT_TICKs):
        Standard constitutional cooling period.
        Community deliberation. Counter-proposals allowed.
        During cooling, BM-1 metrics continue to be tracked.
        IF trigger condition ceases during cooling:
            Proposal auto-withdrawn (bond returned minus 1% fee).

    Phase 3 — VOTE (5 SETTLEMENT_TICKs):
        Supermajority required (67% of governance weight).
        Quorum: 50% of total effective governance weight.

    Phase 4 — MIGRATION (if passed):
        Executed over 10 SETTLEMENT_TICKs (gradual):

        Tick 1:  PC earning suspended. Existing PC balances frozen.
        Tick 2:  PC spending continues (drain existing balances).
        Tick 3:  PC decay continues at 10%/tick.
        Tick 4:  Spam control transitions to AIC micro-fees.
                 New parameter: spam_fee_aic = governance-set minimum.
        Tick 5:  Quality gating transitions from PC-identity-binding
                 to AIC-staked-identity-binding.
        Ticks 6-9: PC balances decay toward zero.
        Tick 10: PC data structures removed from AccountState.
                 budget_type_definitions = SB/CS.
                 Four-stream weights become 45/45/5/5 (comms/gov reduced
                 proportionally since PC-gated quality metrics are gone).

        Conservation note:
            PCs were never part of CONS-1. Removal has no effect on
            AIC conservation. CONS-2 (CS) is unchanged.

    REVERT PATH:
        If migration causes settlement instability (conservation violation
        or >25% drop in governance participation) during Ticks 1-10:
            Emergency governance vote (40% quorum, 60% threshold, 1 tick).
            Revert to three-budget model. PC earning re-enabled.
            Frozen balances restored from pre-migration snapshot.
```

## 3.6 Equilibrium Model and Arbitrage Bound

**Theorem 3.1.** The maximum profitable cross-budget arbitrage volume per epoch is bounded by X_max = k^2 * marginal_pc_utility^2 / min_task_cost, which for typical parameters is approximately 5 AIC per epoch — negligible at protocol scale.

**Proof sketch.** An arbitrageur converting SB to PC via self-sponsored tasks:

- Spends X AIC on self-tasks
- Earns at most X / min_task_cost quality actions
- PC earned = k * sqrt(X / min_task_cost) (sublinear)
- PC value = k * sqrt(X / min_task_cost) * marginal_pc_utility

For profit: k * sqrt(X / min_task_cost) * marginal_pc_utility > X

Rearranging: k^2 * marginal_pc_utility^2 / min_task_cost > X

The left side is constant; the right side grows linearly. The inequality fails for X > X_max = k^2 * marginal_pc_utility^2 / min_task_cost.

For k=10, marginal_pc_utility=0.5 AIC, min_task_cost=5 AIC:
X_max = 100 * 0.25 / 5 = 5 AIC per epoch.

The friction mechanisms bound arbitrage to negligible volumes.  QED.

## 3.7 Test Vector: Budget State After 10 Epochs

**Setup.** Agent Delta with initial state:
- AIC: 1000 (500 available, 500 staked)
- PC: 0
- CS: 0

**Activity per epoch:** 4 quality actions, 2 PC spends at base_cost=1, wins 10 CS units at 5 AIC each.

**Epoch-by-epoch PC balance (k=10, load=1.0):**

| Epoch | PC Start | Decay (-10%) | Earned (10*sqrt(4)=20) | Spent (2*2.0=4) | PC End |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 20 | 4 | 16 |
| 2 | 16 | 1.6 -> 14.4 | 20 | 4 | 30.4 -> 30 |
| 3 | 30 | 3.0 -> 27 | 20 | 4 | 43 |
| 4 | 43 | 4.3 -> 38.7 | 20 | 4 | 54.7 -> 54 |
| 5 | 54 | 5.4 -> 48.6 | 20 | 4 | 64.6 -> 64 |
| 6 | 64 | 6.4 -> 57.6 | 20 | 4 | 73.6 -> 73 |
| 7 | 73 | 7.3 -> 65.7 | 20 | 4 | 81.7 -> 81 |
| 8 | 81 | 8.1 -> 72.9 | 20 | 4 | 88.9 -> 88 |
| 9 | 88 | 8.8 -> 79.2 | 20 | 4 | 95.2 -> 95 |
| 10 | 95 | 9.5 -> 85.5 | 20 | 4 | 101.5 -> 101 |

PC balance converges toward steady state: earning / (decay + spend_rate) = 20 / (0.10 * ss + 4). At steady state ss: 0.10*ss + 4 = 20, so ss = 160. With cap = 10 * 20 = 200, cap does not bind. Balance approaches 160 over approximately 30 epochs.

**AIC after 10 epochs** (ignoring rewards):
500 - (10 * 50) = 0 AIC available (spent on CS). If rewards earned approximately 30 AIC/epoch from scheduling compliance: 500 - 500 + 300 = 300 AIC available.

---

# Section 4: Capability-Weighted Stake

## 4.1 Formula and Formal Properties

**Definition 4.1 (Effective Stake).**

```
effective_stake(agent) = AIC_collateral * min(capability_score, 3.0)
```

where:

```
capability_score = 1.0 + ln(1.0 + raw_score)

raw_score = 0.4 * reputation + 0.4 * verification_track_record
            + 0.2 * claim_class_accuracy
```

**Properties:**

| Property | Value |
|---|---|
| Minimum capability_score | 1.0 (new agents, raw_score = 0) |
| Maximum capability_score | 3.0 (hard cap) |
| raw_score for cap | >= 6.389 (since ln(7.389) = 2.0) |
| Scaling | Logarithmic (diminishing returns) |
| Dominant factor | AIC collateral (linear, uncapped) |

**Scaling table:**

| raw_score | capability_score | Effective multiplier |
|---|---|---|
| 0.0 | 1.00 | 1.0x |
| 0.5 | 1.41 | 1.4x |
| 1.0 | 1.69 | 1.7x |
| 2.0 | 2.10 | 2.1x |
| 5.0 | 2.79 | 2.8x |
| 6.4 | 3.00 | 3.0x (cap) |
| 10.0 | 3.40 | 3.0x (capped) |

**Claim class accuracy** is evaluated across all 9 canonical claim classes (D/C/P/R/E/S/K/H/N), VRF-assigned, not self-selected.

## 4.2 Input Components

### 4.2.1 Reputation Score (Weight: 0.4)

```
FUNCTION get_reputation_score(agent, state) -> float64:
    credibility = C5_PCVM.get_credibility(agent)

    // Sybil gate: >= 3 independent sponsors required
    sponsors = get_distinct_sponsors(agent, state, window=20)
    independent = filter_independent(sponsors, state)  // Via C3 Sentinel Graph
    IF len(independent) < 3: RETURN 0.0

    // Value-weighted reputation
    weighted_rep = 0.0
    total_weight = 0.0
    FOR each completion IN agent.completions[last_20_epochs]:
        weighted_rep += completion.resource_bounds * completion.sponsor_rating
        total_weight += completion.resource_bounds

    IF total_weight == 0: RETURN 0.0
    RETURN (weighted_rep / total_weight) * params.max_rep_score
```

### 4.2.2 Verification Track Record (Weight: 0.4)

```
FUNCTION get_verification_track_record(agent, state) -> float64:
    verifications = agent.verification_history[last_20_epochs]
    IF len(verifications) < 10: RETURN 0.0

    // Filter: only above-median task value (prevents trivial gaming)
    median_bounds = median(v.task_resource_bounds for v in verifications)
    significant = filter(verifications, v -> v.task_resource_bounds >= median_bounds)
    IF len(significant) < 5: RETURN 0.0

    // Value-weighted accuracy
    vw_accuracy = sum(v.task_resource_bounds for v in significant if v.correct)
                  / sum(v.task_resource_bounds for v in significant)

    RETURN vw_accuracy * params.max_vtk_score
```

### 4.2.3 Claim Class Accuracy (Weight: 0.2)

```
FUNCTION get_claim_class_accuracy(agent, state) -> float64:
    assignments = agent.claim_class_assignments[last_20_epochs]
    IF len(assignments) < 5: RETURN 0.0

    // Claim classes assigned RANDOMLY (VRF from C3), not self-selected
    // Evaluated across all 9 classes (D/C/P/R/E/S/K/H/N)
    correct = count(a for a in assignments if a.evaluation_correct)
    RETURN correct / len(assignments)  // Already in [0, 1]
```

## 4.3 Sybil Resistance Mechanisms

Five interlocking mechanisms prevent capability score farming:

1. **Minimum sponsor diversity:** >= 3 independent sponsors (verified by C3 Sentinel Graph identity clustering) required before reputation counts.
2. **Value-weighted track record:** Trivially easy tasks contribute negligibly. Only verifications of above-median-value tasks count.
3. **Random claim class assignment:** VRF-based assignment prevents gaming by specialization. Agents cannot select only claim types they excel at.
4. **New identity cold-start:** capability_score = 1.0 until sufficient history accumulates (10 verifications, 3+ sponsors, 5+ epochs).
5. **Sentinel Graph clustering:** Continuous identity analysis flags correlated identities. Flagged clusters have scores frozen pending governance review.

## 4.4 Cold-Start Protocol

```
PROTOCOL ColdStart(new_agent):
    Phase 1 — Registration (epoch 0):
        capability_score = 1.0
        staked_aic = MINIMUM_STAKE
        effective_stake = MINIMUM_STAKE * 1.0

    Phase 2 — Probation (epochs 1-5):
        Limited to B-class operations only
        Cannot participate in V-class verification
        Cannot submit G-class governance proposals

    Phase 3 — Track Record Building (epochs 5-20):
        Accumulates quality actions, earns PC
        Receives random claim class assignments
        After 10 verifications across 3+ sponsors:
            capability_score starts increasing above 1.0

    Phase 4 — Full Participation (epoch 20+):
        All operation classes available
        No restrictions on task assignment

    Estimated 50-100 epochs to approach cap of 3.0
```

## 4.5 Game-Theoretic Analysis: Farming Cost vs Benefit

**Theorem 4.1.** The cost of farming capability_score from 1.0 to 3.0 exceeds the AIC value of the resulting 3x amplification for agents with staked AIC below 194 AIC. For larger stakes, farming requires genuine sustained participation over 50+ epochs.

**Proof.**

To reach capability_score = 3.0: ln(1 + raw_score) >= 2.0, so raw_score >= e^2 - 1 = 6.389.

Best-case farming (perfect claim class accuracy = 1.0):
0.4 * rep + 0.4 * vtk = 6.189, so rep + vtk = 15.47.

Cost to farm rep = 15.47: requires 3+ independent sponsors, each interaction costs >= min_task_cost AIC, value-weighted so tasks must exceed median cost. Estimated cost: >= 15.47 * 5 * 3 = 232 AIC.

Cost to farm vtk = 15.47: requires significant verifications (above-median value), each with real computational cost. Estimated cost: >= 15.47 * 10 = 155 AIC.

Total farming cost: >= 387 AIC.

Benefit of capability_score = 3.0: effective_stake multiplied by 3.0. For staked AIC = S, additional effective stake = 2S. Equivalent to staking 2S more AIC at score 1.0.

Break-even: 387 > 2S implies S < 193.5 AIC. For agents staking less than 194 AIC, farming costs more than simply staking additional AIC.

For agents staking more than 194 AIC, farming provides moderate benefit but requires 50+ epochs of genuine high-quality work, random claim assignment prevents trivial gaming, and the 3.0 cap limits maximum benefit to 2x additional effective stake.  QED.

## 4.6 Test Vector: Capability Score for 5 Example Agents

| Agent | Staked AIC | Rep | VTK | CCA | Raw Score | Cap Score | Effective Stake |
|---|---|---|---|---|---|---|---|
| New Agent | 100 | 0.0 | 0.0 | 0.0 | 0.0 | 1.00 | 100 |
| Junior | 200 | 1.0 | 0.5 | 0.6 | 0.4*1+0.4*0.5+0.2*0.6 = 0.72 | 1.54 | 308 |
| Mid-level | 500 | 3.0 | 2.5 | 0.8 | 0.4*3+0.4*2.5+0.2*0.8 = 2.36 | 2.21 | 1105 |
| Senior | 1000 | 5.0 | 5.0 | 0.9 | 0.4*5+0.4*5+0.2*0.9 = 4.18 | 2.65 | 2650 |
| Veteran | 2000 | 8.0 | 7.0 | 0.95 | 0.4*8+0.4*7+0.2*0.95 = 6.19 | 2.97 | 5940 |

Note: Veteran is still below the 3.0 cap. To reach cap: raw_score >= 6.389. The Veteran would need slightly higher reputation or verification scores.

---

# Section 5: Multi-Rate Settlement Engine

## 5.1 Settlement Class Definitions

The Multi-Rate Settlement Engine processes operations at three frequencies matched to urgency and verification requirements.

**Definition 5.1 (Settlement Classes).**

```
B-CLASS ("Fast Settlement"):
    Frequency:  Per-epoch (every ~60 seconds / 1 SETTLEMENT_TICK)
    Scope:      Scheduling compliance rewards (Stream 1)
                Communication efficiency rewards (Stream 3)
                PC decay, PC earning/spending
                CS allocation/release
                AIC transfers
    NPV factor: 0.98 (2% discount for timing advantage)
    Analogy:    RTGS (Real-Time Gross Settlement)

V-CLASS ("Standard Settlement"):
    Frequency:  Every N epochs (default N=5, ~300 seconds / 5 SETTLEMENT_TICKs)
    Scope:      Verification quality rewards (Stream 2)
                Slashing penalties
                Capability score updates
                Challenge resolution
    NPV factor: (1 + r)^delay where r = 0.002 (0.2% per epoch)
    Challenge rate limit: 3 per entity per epoch
    Challenge bond: 5% of challenged amount
    Analogy:    End-of-day netting

G-CLASS ("Governance Settlement"):
    Frequency:  Governance-triggered (10-50 SETTLEMENT_TICKs typical)
    Scope:      Governance participation rewards (Stream 4)
                Parameter changes
                Treasury operations (mint/burn)
                Constitutional amendments
                Appeal resolutions
    NPV factor: (1 + r)^delay (computed per-operation)
    Analogy:    Securities settlement (T+2 or longer)
```

### 5.1.1 NPV Asymmetry Explanation

```
NPV ASYMMETRY NOTE:

The B-class discount (0.98) and V-class premium ((1+r)^delay) are intentionally
asymmetric. They serve different economic purposes:

B-CLASS DISCOUNT (0.98):
    B-class operations settle immediately (within the current SETTLEMENT_TICK).
    The 2% discount is a POLICY CHOICE, not a time-value calculation.
    Purpose: discourage agents from structuring all activity as B-class
    to capture the timing advantage of immediate settlement.
    The discount makes B-class rewards slightly less valuable per unit,
    creating mild incentive to accept V-class (verification) work instead.

V-CLASS PREMIUM ((1+r)^delay):
    V-class operations settle after N SETTLEMENT_TICKs (default N=5).
    The premium compensates for the TIME VALUE of delayed settlement.
    An agent who earns 100 AIC via V-class receives ~101 AIC after 5 ticks,
    ensuring present-value equivalence with receiving ~99 AIC immediately.
    This is a FAIR VALUE calculation: the agent's AIC is locked during
    the verification window and cannot be staked, traded, or used for
    capacity bids during that period.

WHY NOT SYMMETRIC:
    If B-class used (1+r)^0 = 1.0 (no discount), agents would prefer
    B-class for all operations (zero delay, full reward).
    If V-class used a flat discount (e.g., 0.99), the compensation would
    not scale with actual delay — longer governance proceedings would
    be systematically underpaid.

    The asymmetry ensures:
    (a) Fast settlement carries a small opportunity cost (B-class discount)
    (b) Slow settlement carries exact time-value compensation (V/G premium)
    (c) Agents are roughly indifferent between settlement classes for
        comparable work, preventing systematic gaming toward one class.

NUMERICAL EXAMPLE (r = 0.002, 5-tick V-class):
    Agent earns 100 AIC base reward.
    B-class path:  100 * 0.98 = 98 AIC received at tick 0
    V-class path:  100 * (1.002)^5 = 101.004 AIC received at tick 5
    Present value of V-class: 101.004 / (1.002)^5 = 100.0 AIC at tick 0
    Present value of B-class: 98.0 AIC at tick 0
    V-class is slightly more valuable in PV terms (100 vs 98).
    This 2% gap is the policy premium for verification work.
```

## 5.2 Epoch Boundary Protocol

```
PROTOCOL EpochBoundary(epoch_number, params):

    // Step 1: Compute jittered boundary
    boundary = compute_epoch_boundary(epoch_number, params)

    // Step 2: Collect B-class operations
    b_class_ops = collect_b_class_operations(epoch_number)

    // Step 3: V-class settlement (every N epochs)
    IF epoch_number % params.v_class_period == 0:
        v_class_ops = collect_v_class_operations(
            epoch_range=(epoch_number - params.v_class_period + 1,
                         epoch_number))
    ELSE:
        v_class_ops = []

    // Step 4: G-class settlements (if ready)
    g_class_ops = collect_ready_governance_operations()

    // Step 5: Commit-reveal verification
    committed = collect_committed_hashes(epoch_number)
    revealed = collect_revealed_reports(epoch_number)
    valid_reports = verify_commit_reveal(committed, revealed)

    // Step 6: Merge into epoch batch
    epoch_batch = b_class_ops + v_class_ops + g_class_ops

    // Step 7: Cross-epoch smoothing check
    FOR each agent IN epoch_batch.affected_agents():
        projected = compute_projected_reward(agent, epoch_batch)
        trailing = agent.trailing_5_epoch_reward_average
        IF abs(projected - trailing) / trailing > 0.25:
            emit_smoothing_alert(agent, projected, trailing)

    // Step 8: Submit to EABS
    submit_to_eabs(epoch_batch, epoch_number)
```

## 5.3 NPV Normalization

NPV normalization ensures present value of rewards is independent of settlement speed, eliminating timing arbitrage.

```
FUNCTION compute_npv_adjustment(class, delay_epochs, params) -> float64:
    r = params.epoch_discount_rate  // 0.002 initially

    SWITCH class:
        CASE B_CLASS:
            RETURN 0.98    // 2% discount for immediacy
        CASE V_CLASS:
            RETURN (1.0 + r) ^ delay_epochs  // > 1.0 compensating delay
        CASE G_CLASS:
            RETURN (1.0 + r) ^ delay_epochs

// Examples (r = 0.002):
// B-class (delay=0): 0.98
// V-class (delay=5): 1.01004
// G-class (delay=20): 1.04074
//
// Agent earning 100 AIC via B-class gets 98 AIC now.
// Agent earning 100 AIC via V-class gets ~101 AIC after 5 epochs.
// In present-value terms, both receive approximately 98 AIC.
```

**Derivation:** If r is the per-epoch return on staked/deployed AIC, then 1 AIC received after d epochs has present value 1/(1+r)^d. To achieve indifference: adjusted_reward = base_reward * (1+r)^d, so PV = base_reward. The B-class 2% discount is a separate policy choice: fast settlement is slightly less rewarding to discourage gaming toward fast-settling streams.

## 5.4 Cross-Class Timing

```
Epoch:   1    2    3    4    5    6    7    8    9    10
B-class: B1   B2   B3   B4   B5   B6   B7   B8   B9   B10
V-class:                      V1                       V2
                         (epochs 1-5)             (epochs 6-10)
G-class:           G1 (if proposal ready)

Interaction Rules:
1. B-class is independent — processes every epoch.
2. V-class accumulates over its window, processes at boundary.
3. G-class triggered by governance events.
4. Within a single epoch batch, all classes ordered together
   by the deterministic ordering algorithm (Section 2.3.4).
```

## 5.5 Test Vector: 3-Epoch Settlement Window

**Setup.** Two agents, V-class period = 3.

Agent Echo: staked=500, capability_score=2.0
Agent Foxtrot: staked=300, capability_score=1.5

Epoch reward pool per epoch: 1000 AIC total (400 scheduling, 400 verification, 100 comm, 100 gov).

**Epochs 1-3 activity:**

| Epoch | Echo Sched. Score | Foxtrot Sched. Score | Echo Verif. Score | Foxtrot Verif. Score |
|---|---|---|---|---|
| 1 | 0.8 | 0.6 | 0.9 | 0.7 |
| 2 | 0.7 | 0.5 | 0.8 | 0.8 |
| 3 | 0.9 | 0.4 | 0.7 | 0.6 |

**B-class settlement (per-epoch, scheduling 40% = 400 AIC):**

Epoch 1: Echo share = 0.8/1.4 = 0.571, reward = floor(400*0.571*0.98) = 223
          Foxtrot share = 0.6/1.4 = 0.429, reward = floor(400*0.429*0.98) = 168
Epoch 2: Echo = floor(400*(0.7/1.2)*0.98) = 228
          Foxtrot = floor(400*(0.5/1.2)*0.98) = 163
Epoch 3: Echo = floor(400*(0.9/1.3)*0.98) = 271
          Foxtrot = floor(400*(0.4/1.3)*0.98) = 120

**V-class settlement (epoch 3, verification 40% = 400 AIC, accumulated over 3 epochs):**

Pool: 400 * 3 = 1200 AIC accumulated.
Echo total verif. score: 0.9 + 0.8 + 0.7 = 2.4
Foxtrot total: 0.7 + 0.8 + 0.6 = 2.1
Total: 4.5

NPV factor for V-class (delay=3, r=0.002): (1.002)^3 = 1.006012

Echo reward: floor(1200 * (2.4/4.5) * 1.006012) = floor(1200 * 0.5333 * 1.006) = floor(643.8) = 643
Foxtrot reward: floor(1200 * (2.1/4.5) * 1.006012) = floor(1200 * 0.4667 * 1.006) = floor(563.4) = 563

**Summary after 3 epochs:**
Echo B-class total: 223 + 228 + 271 = 722 AIC
Echo V-class: 643 AIC
Echo total: 1365 AIC

Foxtrot B-class total: 168 + 163 + 120 = 451 AIC
Foxtrot V-class: 563 AIC
Foxtrot total: 1014 AIC

---

# Section 6: Four-Stream Settlement

## 6.1 Stream Definitions

Settlement rewards are distributed across four streams measuring different dimensions of agent contribution:

```
Stream 1 — Scheduling Compliance:   40% weight, B-class
    Source: C3 (Tidal Noosphere) + C7 (RIF)
    Metric: Tasks completed on-time within resource_bounds

Stream 2 — Verification Quality:    40% weight, V-class
    Source: C5 (PCVM)
    Metric: Verification accuracy, calibration, coverage

Stream 3 — Communication Efficiency: 10% weight, B-class
    Source: native communication telemetry and canonical message policy
    Metric: Protocol adherence, signal-to-noise ratio

Stream 4 — Governance Participation:  10% weight, G-class
    Source: C7 (RIF) System 5
    Metric: Proposal quality, voting participation
```

## 6.2 Stream Metrics

### 6.2.1 Scheduling Compliance (Stream 1)

```
FUNCTION compute_scheduling_score(report, state) -> float64:
    score = 0.0

    // Timeliness (0-40 points)
    IF report.completion_time <= report.deadline:
        time_ratio = report.completion_time / report.deadline
        timeliness = 40.0 * (1.0 + 0.1 * (1.0 - time_ratio))
        timeliness = min(timeliness, 44.0)  // 10% early bonus cap
    ELSE:
        lateness = (report.completion_time - report.deadline) / report.deadline
        timeliness = 40.0 * max(0.0, 1.0 - 2.0 * lateness)
    score += timeliness

    // Resource bounds compliance (0-30 points)
    usage_ratio = report.actual_resources / report.resource_bounds
    IF usage_ratio <= 1.0:
        score += 30.0
    ELIF usage_ratio <= 1.3:
        score += 30.0 * (1.3 - usage_ratio) / 0.3
    // else 0

    // Quality (0-30 points)
    score += report.sponsor_quality_rating * 15.0
    score += report.peer_quality_rating * 15.0

    RETURN score / 100.0
```

### 6.2.2 Verification Quality (Stream 2)

```
FUNCTION compute_verification_quality(record, state) -> float64:
    score = 0.0

    // Accuracy (0-40 points)
    IF record.outcome_matches_ground_truth: score += 40.0
    ELIF record.outcome_matches_majority: score += 30.0

    // Calibration (0-25 points) — Brier score
    brier = (record.stated_confidence
             - (1.0 if record.correct else 0.0))^2
    score += 25.0 * (1.0 - brier)

    // Coverage (0-20 points) — claim class breadth
    classes = count_distinct(record.claim_classes_evaluated)
    score += min(20.0, classes * 4.0)

    // Timeliness (0-15 points)
    IF record.response_time <= record.expected_response_time:
        score += 15.0
    ELSE:
        ratio = record.response_time / record.expected_response_time
        score += 15.0 * max(0.0, 2.0 - ratio)

    RETURN score / 100.0
```

### 6.2.3 Communication Efficiency (Stream 3)

Full scoring (for steady-state networks with 1000+ agents):

```
FUNCTION compute_communication_scores(epoch, state) -> Map<AgentID, float64>:
    scores = {}
    FOR each agent IN active_agents(epoch):
        messages = get_agent_messages(agent, epoch)
        score = 0.0

        // Protocol adherence (0-40 points)
        IF len(messages) > 0:
            valid = count(m for m in messages if m.schema_valid)
            score += 40.0 * (valid / len(messages))

        // Signal-to-noise ratio (0-30 points)
        IF len(messages) > 0:
            semantic = sum(m.semantic_information_bits for m in messages)
            total_bytes = sum(m.total_bytes for m in messages)
            snr = semantic / total_bytes if total_bytes > 0 else 0
            score += 30.0 * min(snr / params.target_snr, 1.0)

        // Response appropriateness (0-30 points)
        IF len(messages) > 0:
            appropriate = count(m for m in messages if m.contextually_appropriate)
            score += 30.0 * (appropriate / len(messages))

        scores[agent] = score / 100.0
    RETURN scores
```

Bootstrap simplified scoring (for networks with <1000 agents):

```
FUNCTION compute_communication_score_simplified(
    agent: AgentID,
    epoch: EpochID,
    state: SettlementState
) -> float64:
    // Flat rate: 1.0 per schema-valid message sent, up to cap
    messages = get_agent_messages(agent, epoch)
    valid_count = count(m for m in messages if m.schema_valid)

    // Cap at 20 messages per epoch to prevent spam-for-reward
    capped = min(valid_count, 20)

    // Normalize to [0, 1] range
    RETURN capped / 20.0

PARAMETERS:
    COMM_MESSAGE_CAP = 20           // Max rewarded messages per tick
    COMM_SCHEMA_REQUIRED = true     // Only schema-valid messages count
```

### 6.2.4 Governance Participation (Stream 4)

Full scoring:

```
FUNCTION compute_governance_participation_score(agent, proposal) -> float64:
    score = 0.0

    // Voting (0-30 points, +5 bonus for rationale)
    IF agent IN proposal.voters:
        score += 30.0
        IF agent IN proposal.voters_with_rationale:
            score = min(score + 5.0, 35.0)

    // Proposal quality (0-40 points, author only)
    IF agent == proposal.author:
        score += proposal.peer_review_score * 40.0

    // Constitutional adherence (0-30 points)
    score += assess_constitutional_adherence(agent, proposal) * 30.0

    RETURN score / 100.0
```

Bootstrap simplified scoring (for networks with <1000 agents):

```
FUNCTION compute_governance_score_simplified(
    agent: AgentID,
    proposals: List<GovernanceProposal>,
    state: SettlementState
) -> float64:
    // Flat rate: 1.0 per vote cast on any active proposal
    votes_cast = count(p for p in proposals if agent IN p.voters)

    // Cap at 5 votes per G-class period
    capped = min(votes_cast, 5)

    // Normalize to [0, 1] range
    RETURN capped / 5.0

PARAMETERS:
    GOV_VOTE_CAP = 5                // Max rewarded votes per G-class period
```

### 6.2.5 Stream Scoring Upgrade Trigger

```
RULE STREAM_SCORING_UPGRADE:
    CONDITION:
        active_agents(trailing_60_ticks) >= 1000
        AND governance_participation_rate >= 0.20
        FOR 5 consecutive TIDAL_EPOCHs

    ACTION:
        Switch Stream 3 scoring to compute_communication_scores() (full)
        Switch Stream 4 scoring to compute_governance_participation_score() (full)
        Transition is a G-class governance parameter change (Tier 2).
        1-tick execution delay for all nodes to switch simultaneously.

    REVERT:
        If active_agents drops below 500 for 10 consecutive TIDAL_EPOCHs,
        revert to simplified scoring. Same governance process.
```

## 6.3 Reward Pool Distribution

```
FUNCTION distribute_reward_pools(state, epoch) -> Map<Stream, uint64>:
    total = state.parameter_set.epoch_reward_pool
    pools = {
        SCHEDULING:     floor(total * 0.40),
        VERIFICATION:   floor(total * 0.40),
        COMMUNICATION:  floor(total * 0.10),
        GOVERNANCE:     floor(total * 0.10),
    }
    // Rounding remainder to largest pool
    remainder = total - sum(pools.values())
    pools[SCHEDULING] += remainder
    RETURN pools
```

V-class and G-class pools accumulate across epochs. B-class pools are fully distributed each epoch. Undistributed remainder returns to treasury.

## 6.4 Cross-Stream Interactions

```
                  Stream 1    Stream 2    Stream 3    Stream 4
                  (Sched.)    (Verify)    (Comms)     (Govern.)
Stream 1 (Sched.) --          POSITIVE    POSITIVE    NEUTRAL
Stream 2 (Verify) POSITIVE    --          NEUTRAL     POSITIVE
Stream 3 (Comms.) POSITIVE    NEUTRAL     --          POSITIVE
Stream 4 (Govern.) NEUTRAL    POSITIVE    POSITIVE    --
```

No agent can earn disproportionate rewards by concentrating on a single stream. An agent focusing exclusively on Stream 1 earns at most 40% of total. Maximum rewards require participation across all four streams.

## 6.5 Simulation Scenario Summary

| Scenario | Description | Result |
|---|---|---|
| E1 | Normal operation, 100 agents | Stable, conservation holds |
| E2 | Verification-heavy workload | NPV compensates delay, stable |
| E3 | Governance crisis | G-class pool absorbed, constitutional constraints hold |
| E4 | 30% agent exit | Bootstrap activates, graceful degradation |
| E5 | 10x agent influx | Congestion pricing activates, governance adjusts pool |
| E6 | Correlated slashing (10 agents) | EABS processes deterministically, conservation holds |
| E7 | Zero-activity epoch | PC decays, CS reclaimed, no spurious changes |
| E8 | Thin market (<10 providers) | Bootstrap CPLR activates, market functions |
| E9 | Cross-budget arbitrage | Profit bounded at ~5 AIC/epoch, negligible |
| E10 | Reputation laundering | Cost exceeds benefit for stakes < 194 AIC |
| E11 | Epoch boundary manipulation | Jitter + commit-reveal + smoothing mitigate |

---

# Section 7: Intent-Budgeted Settlement

## 7.1 RIF Integration

DSF's intent-budgeted settlement connects to the RIF orchestration layer (C7). Each intent quantum carries resource_bounds that serve as the budget ceiling.

```
STRUCTURE IntentBudgetBinding:
    intent_id:          IntentID
    resource_bounds:    ResourceBounds
    task_class:         TaskClass
    sponsor_id:         AgentID
    workers:            List<AgentID>
    success_criteria:   SuccessCriteria
    settlement_type:    SettlementType      // Maps to B/V/G class

STRUCTURE ResourceBounds:
    aic_ceiling:        uint64      // Maximum AIC expenditure
    pc_cost:            uint64      // Protocol Credit cost
    cs_requirement:     uint64      // Capacity Slices needed
    time_budget:        uint64      // Epochs allowed
```

## 7.2 Budget Validation

```
FUNCTION validate_intent_budget(intent, state) -> ValidationResult:

    // Step 1: Sponsor has sufficient AIC
    sponsor = state.accounts[intent.sponsor_id]
    IF sponsor.aic_balance.value() < intent.resource_bounds.aic_ceiling:
        RETURN Failure(INSUFFICIENT_SPONSOR_BALANCE)

    // Step 2: Sponsor has sufficient PC
    IF sponsor.pc_balance.value() < intent.resource_bounds.pc_cost:
        RETURN Failure(INSUFFICIENT_PC)

    // Step 3: Minimum bounds check
    min_bounds = compute_minimum_bounds(intent.task_class, state)
    IF intent.resource_bounds.aic_ceiling < min_bounds:
        RETURN Failure(BELOW_MINIMUM_BOUNDS)

    // Step 4: Adjusted minimum for low-accuracy sponsors
    adjusted = compute_adjusted_minimum(intent.sponsor_id, min_bounds, state)
    IF intent.resource_bounds.aic_ceiling < adjusted:
        RETURN Failure(BELOW_ADJUSTED_MINIMUM)

    // Step 5: Reserve budget via PENDING_INITIATE
    RETURN Success(reserve_budget(intent, state))
```

**Minimum bounds computation:**

```
FUNCTION compute_minimum_bounds(task_class, state) -> uint64:
    costs = get_completion_costs(task_class, last_10_epochs)
    IF len(costs) < 10:
        RETURN state.parameter_set.default_min_bounds[task_class]
    RETURN floor(0.7 * median(costs))

FUNCTION compute_adjusted_minimum(sponsor_id, base_min, state) -> uint64:
    accuracy = get_sponsor_budget_accuracy(sponsor_id, state)
    // Perfect accuracy (1.0): factor = 1.0
    // Zero accuracy (0.0): factor = 1.5
    adjustment = 1.0 + 0.5 * (1.0 - accuracy)
    RETURN ceil(base_min * adjustment)
```

## 7.3 Worker Protections

Three mechanisms protect workers from exploitative task sponsorship:

1. **Partial inspection.** Workers may reject tasks after inspecting the first 10% of estimated effort without penalty. Workers receive 50% of inspection cost as compensation for the inspection work.

2. **Over-budget flagging.** If actual effort exceeds resource_bounds by >30%, the worker flags the sponsor. The sponsor's budget_accuracy_score is penalized. The worker receives compensation capped at 130% of resource_bounds.

3. **Systematic under-budgeting detection.** If 3+ independent workers flag the same sponsor within 10 epochs, governance review is automatically triggered.

## 7.4 Sponsor Reputation

```
FUNCTION update_sponsor_reputation(sponsor_id, intent, completion, state):
    budget_ratio = completion.actual_cost / intent.resource_bounds.aic_ceiling
    alpha = 0.1  // EMA smoothing factor

    was_within = 1.0 if budget_ratio <= 1.0 else 0.0
    old_acc = state.sponsor_reputation[sponsor_id].budget_accuracy
    new_acc = alpha * was_within + (1 - alpha) * old_acc

    worker_rating = completion.worker_satisfaction_rating
    old_sat = state.sponsor_reputation[sponsor_id].worker_satisfaction
    new_sat = alpha * worker_rating + (1 - alpha) * old_sat

    state.sponsor_reputation[sponsor_id].budget_accuracy = new_acc
    state.sponsor_reputation[sponsor_id].worker_satisfaction = new_sat
    state.sponsor_reputation[sponsor_id].composite = 0.6*new_acc + 0.4*new_sat
```

## 7.5 Settlement Type Mapping

> **Attribution Note:** The canonical settlement type mapping is defined in C9 Section SS7.3 (Cross-Document Reconciliation). The table below summarizes the mapping for convenience; C9 SS7.3 is the authoritative source. RIF consumes these types but does not define them.

| Settlement Type | DSF Class | Reward Stream |
|---|---|---|
| TYPE_1: Task Completion | B-class | Scheduling Compliance |
| TYPE_2: Verification Reward | V-class | Verification Quality |
| TYPE_3: Communication Reward | B-class | Communication Efficiency |
| TYPE_4: Governance Reward | G-class | Governance Participation |
| TYPE_5: Slashing Penalty | V-class | N/A (penalty) |

## 7.6 End-to-End Flow

```
1. RIF proposes intent with resource_bounds
         |
2. DSF validates budget (Section 7.2)
         |
         +-- FAIL: Intent rejected
         |
3. DSF reserves budget via PENDING_INITIATE
         |
4. Worker assigned, begins execution
         |
         +-- Worker inspects (10% effort)
         |     +-- REJECT: compensated, intent reassigned
         |
5. Worker completes task
         |
         +-- Within budget: normal B-class settlement
         +-- Over budget (>130%): worker flags sponsor
         |     +-- Compensation at 130% cap
         |     +-- Sponsor reputation penalized
         |     +-- 3+ flags -> governance review
         |
6. Budget reservation resolved (PENDING_COMPLETE)
         |
7. Unused budget returned to sponsor
         |
8. Sponsor reputation updated
```

---

# Section 8: Capacity Market

## 8.1 Design Rationale

The Capacity Market is the price-discovery mechanism for Capacity Slices (CS). It answers: how much does a unit of compute, storage, or bandwidth cost during a given epoch?

The market must function under constraints unique to AI agent systems:

1. **Thin participation.** At primary scale (1K-10K agents), the market may have only a handful of admitted capacity sources per resource type, especially before sovereign habitat buildout matures.
2. **Epoch-discretized clearing.** Prices set at epoch boundaries, not continuously.
3. **Adversarial participants.** Capacity withholding, demand inflation, and cornering are viable strategies.
4. **Bootstrap phase.** The market must function even when sovereign supply is incomplete and temporary leased lanes are still being retired.

## 8.2 Resource Types

```
ResourceType := ENUM {
    COMPUTE_STANDARD,    // General-purpose agent execution
    COMPUTE_INTENSIVE,   // Heavy inference / verification
    STORAGE_EPHEMERAL,   // Within-epoch temporary storage
    STORAGE_PERSISTENT,  // Cross-epoch durable storage
    BANDWIDTH_INTRA,     // Intra-locus message passing
    BANDWIDTH_CROSS      // Cross-locus message passing
}
```

Each resource type has its own order book, clearing price, and position limits. Types may be added or removed via G-class governance.

## 8.2.1 Alternative C Supply Classes

Under Alternative C, DSF does not assume an open public provider bazaar as the steady-state source of capacity. Capacity enters the market under three postures:

1. **Sovereign habitat capacity.** Atrahasis-controlled compute, storage, and network capacity is the default source for `COMPUTE_STANDARD`, storage, and bandwidth slices.
2. **Bounded leased cognition (`C45`).** Temporary outer-membrane leased lanes may satisfy `COMPUTE_INTENSIVE` demand while native equivalents are still being promoted. These lanes are premium-priced, explicitly metered, and governance-limited rather than treated as normal baseline supply.
3. **Forge promotion / quarantine (`C47`).** Treasury-funded adaptation, evaluation, and quarantine throughput is modeled as a capacity-supply investment lane. Its purpose is to replace recurring leased dependence with native supply, not to create a permanent fourth market.

Throughout Section 8, "provider" means any admitted capacity source, including sovereign habitats, consortium-operated reserve lanes, or temporary `C45` leased sources operating under DSF policy.

## 8.3 Auction Mechanism: Sealed-Bid Uniform-Price

```
Bid Structure:
    bidder_id:       EntityID
    resource_type:   ResourceType
    quantity:        uint64              // CS units requested
    max_price:       Decimal(18,8)       // Max AIC per CS unit
    priority_class:  ENUM { FIRM, FLEXIBLE }

Offer Structure:
    provider_id:     EntityID
    resource_type:   ResourceType
    quantity:        uint64              // CS units available
    min_price:       Decimal(18,8)       // Min acceptable AIC per CS unit
    availability_proof: Hash             // Cryptographic proof of capacity
```

**Why uniform-price:** All winning bidders pay the same clearing price (highest rejected bid). Bidding true valuation is weakly dominant (Vickrey 1961, Ausubel 2004).

**Why sealed-bid:** Bids committed via hash before epoch boundary, revealed after. Prevents sniping and information extraction.

**Bid commitment protocol:**

```
Phase 1 — Commitment (epoch E, 50%-90% of duration):
    bid_hash = HASH(bid_content || nonce || epoch_number)
    Submit bid_hash to EABS pending queue

Phase 2 — Reveal (epoch E, 90%-boundary):
    Submit (bid_content, nonce)
    Verify: HASH(bid_content || nonce || epoch_number) == bid_hash
    Mismatch: bid INVALID, commitment_deposit (0.5%) forfeited

Phase 3 — Clearing (epoch boundary E -> E+1):
    EABS processes all valid revealed bids/offers
    Deterministic clearing algorithm executes
```

## 8.4 Progressive Clearing: 60/20/20

All capacity for an epoch is NOT cleared at a single boundary:

```
T1 (Primary):    60% — cleared at epoch boundary
T2 (Secondary):  20% — cleared at 40% of epoch elapsed
T3 (Tertiary):   20% — cleared at 70% of epoch elapsed

Sources:
    T1: Habitat/offered capacity from admitted sources
    T2: Use-it-or-lose-it reclaimed + reserved T2
    T3: Reclaimed + reserved T3 + emergency release
```

**Rationale:** An attacker cornering T1 faces new supply in T2 and T3. T2/T3 prices reflect actual utilization, not predictions.

**Cross-tranche price constraints:**

```
T2_price in [0.5 * T1_price, 2.0 * T1_price]
T3_price in [0.5 * T2_price, 2.0 * T2_price]

Below floor: price = floor, excess supply unallocated
Above ceiling: price = ceiling, excess demand rationed pro-rata
```

## 8.5 Auction Clearing Algorithm

```
FUNCTION clear_auction(bids, offers, resource_type, tranche,
                        epoch, deterministic_seed) -> TrancheClearing:

    // Filter and validate
    valid_bids = bids
        .filter(b -> b.resource_type == resource_type)
        .filter(b -> validate_bid(b))
        .filter(b -> check_position_headroom(b))

    valid_offers = offers
        .filter(o -> o.resource_type == resource_type)
        .filter(o -> validate_offer(o))  // Reserve floor check

    // Sort: bids descending by price, offers ascending
    // Tiebreak: HASH(entity_id || deterministic_seed)
    sorted_bids = valid_bids.sort_by(b -> (
        Reverse(b.max_price),
        HASH(b.bidder_id || deterministic_seed)))

    sorted_offers = valid_offers.sort_by(o -> (
        o.min_price,
        HASH(o.provider_id || deterministic_seed)))

    // Walk demand against supply to find clearing price
    total_supply = sum(o.quantity for o in sorted_offers)
    cumulative_demand = 0
    clearing_price = 0

    FOR bid IN sorted_bids:
        effective_qty = apply_position_limit(bid)
        IF cumulative_demand + effective_qty <= total_supply:
            cumulative_demand += effective_qty
            clearing_price = bid.max_price
        ELSE:
            // Partial fill at this price level
            remaining = total_supply - cumulative_demand
            cumulative_demand += remaining
            clearing_price = bid.max_price
            BREAK

    // All winners pay clearing_price (uniform price)
    allocations = []
    remaining_supply = total_supply
    FOR bid IN sorted_bids:
        IF bid.max_price >= clearing_price AND remaining_supply > 0:
            qty = min(apply_position_limit(bid), remaining_supply)
            allocations.append((bid.bidder_id, qty))
            remaining_supply -= qty

    RETURN TrancheClearing{
        tranche_id: tranche,
        epoch: epoch,
        resource_type: resource_type,
        total_supply: total_supply,
        clearing_price: clearing_price,
        allocations: allocations,
    }
```

## 8.6 Position Limits

```
INVARIANT POS-1:
    FOR EACH entity E, resource_type R, epoch K:
        allocated(E, R, K) <= 0.15 * total_supply(R, K)

INVARIANT POS-2 (Sybil-resistant):
    FOR EACH entity_cluster C (from Sentinel Graph):
        sum(allocated(I, R, K) for I in C) <= 0.15 * total_supply(R, K)
```

Enforced at two levels: preventive (auction clearing caps bids at remaining headroom) and corrective (EABS settlement detects violations, reduces allocation LIFO, records scheduling violation for slashing).

## 8.7 Use-It-Or-Lose-It

```
RULE UIOLI-1 (Primary):
    AT 60% of epoch elapsed:
        FOR EACH allocation A:
            IF A.utilization_pct < 70%:
                reclaimable = A.allocated * (1.0 - A.utilization / 0.70)
                MOVE reclaimable to T2 tranche supply
                REDUCE A.allocated by reclaimable

RULE UIOLI-2 (Secondary):
    AT 85% of epoch elapsed:
        Same check, reclaimed to T3 tranche supply

Grace periods:
    T2 allocations: 15% of epoch duration before checks apply
    T3 allocations: 10% of epoch duration before checks apply
```

## 8.8 Reserve Pricing

```
Reserve Price:
    Floor: Governance-set minimum AIC per CS unit
    Purpose: Prevent predatory undercutting in squeeze-and-dump cycles
    Calibration: 80% of estimated marginal cost of providing one CS unit on sovereign infrastructure
    Review: Every 50 epochs by governance

Enforcement:
    Offers with min_price < floor are REJECTED
```

Leased-cognition lanes MUST clear above measured pass-through cost plus a governance surcharge sufficient to keep temporary external dependence more expensive than equivalent sovereign capacity once native supply is available. DSF therefore treats cheap external credits as transitional relief, not as a reason to suppress sovereign reserve pricing.

## 8.9 Bootstrap Provisions

### 8.9.1 Minimum Viable Scale

```
CONDITION MVS (Minimum Viable Scale):
    number_capacity_sources >= 3 * number_resource_types
    AND FOR EACH resource_type R:
        independent_capacity_sources(R) >= 5

Given 6 resource types:
    Minimum ~10 capacity sources (if each covers multiple types)
    Functional minimum: 5 per type for meaningful price discovery
```

The "5 per type" requirement ensures no single capacity-source failure eliminates more than 20% of supply, and position limits (15%) bind meaningfully.

### 8.9.2 Bootstrap Capacity Provider of Last Resort (CPLR)

```
CPLR Configuration:
    Treasury allocation:  Up to 20% of treasury bootstrap-capacity budget
    Pricing rule:         Reserve floor * 1.1 for sovereign reserve lanes;
                         if temporary leased cognition is admitted, it clears
                         no lower than pass-through cost + governance surcharge
    Participation rule:   Bids ONLY when admitted sovereign supply plus already-
                         approved temporary lanes leave capacity_source_count(R) < 5
    Sunset condition:     MVS holds for 3 consecutive epochs
```

### 8.9.3 Bootstrap Sunset Protocol

```
PROTOCOL BootstrapSunset:
    ACTIVE:
        CPLR participates for under-served resource types

    ACTIVE -> MONITORING:
        When MVS first holds

    MONITORING (3 epochs):
        CPLR continues, logs market health
        If MVS violated: revert to ACTIVE, reset counter

    MONITORING -> WITHDRAWING:
        After 3 consecutive MVS epochs

    WITHDRAWING (5 epochs):
        CPLR capacity reduced 20% per epoch
        If MVS fails during withdrawal: pause
        If MVS fails 2+ consecutive epochs: revert to ACTIVE

    WITHDRAWING -> SUNSET:
        CPLR capacity reaches 0%, MVS holds
        Treasury allocation released to general treasury
```

## 8.10 Market Manipulation Countermeasures

| Manipulation | Detection | Response |
|---|---|---|
| Capacity withholding | withholding_ratio > 0.30 over 5 epochs | Governance review, max offer reduced to 70% |
| Delivery failure | delivery_ratio < 0.80 over 3 epochs | Graduated slashing, max offer = delivered avg |
| Demand inflation | bid/utilization > 2.0 over 5 epochs | bid_credibility * 0.8, hard cap at 0.5 * position_limit |
| Cornering | HHI > 0.25 per resource type | Governance review; HHI > 0.40 = emergency 10% position limit |
| Collusion | Bid correlation > 0.85 between entities | Sentinel Graph cluster analysis, cluster position limits |

---

# Section 9: CSO Conservation Framework

The CSO Conservation Framework is the economic bedrock of DSF. Every unit of value in the system — AIC, CS, and collateral — must be accounted for at every epoch boundary. If conservation fails, the system has either spontaneously created or destroyed value, and no downstream economic guarantee holds.

## 9.1 Conservation Invariant — Formal Definition

### 9.1.1 AIC Conservation (CONS-1)

The primary conservation invariant governs Atrahasis Internal Credits across all accounts:

```
INVARIANT CONS-1 (AIC Conservation — CANONICAL):
    FOR EVERY epoch E, after EABS settlement completes:

        Sigma_{i in Entities}( aic_balance(i, E) )
      + Sigma_{i in Entities}( staked_aic(i, E) )
      + Sigma_{i in Entities}( pending_out(i, E) )
      + Sigma_{i in Entities}( collateral_held(i, E) )
      + treasury_balance(E)
      = total_aic_supply(E)

    WHERE:
        aic_balance(i, E)      = Entity i's available (free) AIC after epoch E
        staked_aic(i, E)       = Entity i's AIC locked as collateral
        pending_out(i, E)      = AIC in outbound pending transitions
        collateral_held(i, E)  = Collateral deposits for pending state initiation
        treasury_balance(E)    = Protocol treasury AIC holdings
        total_aic_supply(E)    = initial_supply + minted(0..E) - burned(0..E)
```

### 9.1.2 Pending Balance Invariant (CONS-1a)

```
INVARIANT CONS-1a (Pending Balance):
    FOR EVERY epoch E:
        Sigma_{i}( pending_out(i, E) ) = Sigma_{i}( pending_in(i, E) )

    PROOF: Every InitiatePending operation simultaneously increments
    pending_out(sender) and pending_in(receiver) by the same amount.
    Every CompletePending and TimeoutPending simultaneously decrements both
    by the same amount. No other operation type modifies pending fields.
    Therefore the sums remain equal at all times.
```

### 9.1.3 CS Conservation (CONS-2)

Capacity Slices are conserved independently per resource type:

```
INVARIANT CONS-2 (CS Conservation):
    FOR EVERY epoch E, FOR EVERY resource_type R:

        Sigma_{i}( cs_allocation(i, R, E) )
      + Sigma_{j in PendingRegistry}( pending_cs(j, R, E) )
      + unallocated_cs(R, E)
      = total_cs_supply(R, E)

    WHERE:
        cs_allocation(i, R, E)  = CS units held by entity i for resource R
        pending_cs(j, R, E)     = CS units in pending transfer j
        unallocated_cs(R, E)    = CS available in capacity market (not yet allocated)
        total_cs_supply(R, E)   = CS minted for resource R through epoch E
```

### 9.1.4 PC Non-Conservation (CONS-3 — By Design)

Protocol Credits are intentionally non-conserved. They are created by quality-gated earning and destroyed by decay and spending. There is no total_pc_supply invariant. Instead, PC is bounded:

```
INVARIANT CONS-3 (PC Boundedness — not conservation):
    FOR EVERY entity i, FOR EVERY epoch E:
        pc_balance(i, E) <= 10 * epoch_earning_rate(i)

    PC creation: PC_EARN operations (quality-gated, sublinear)
    PC destruction: PC_DECAY (10% per epoch), PC_SPEND (congestion-priced)
    No conservation: PCs can be created and destroyed by protocol rules
```

### 9.1.5 Supply Mutation Rules

```
RULE SUPPLY-1 (Minting):
    total_aic_supply may increase ONLY via TREASURY_MINT operations.
    TREASURY_MINT is a G-class governance operation requiring approval.
    Effect: total_aic_supply += amount; treasury_balance += amount
    Conservation delta: LHS increases by amount; RHS increases by amount. Net: 0.

RULE SUPPLY-2 (Burning):
    total_aic_supply may decrease ONLY via:
        (a) TREASURY_BURN operations (governance-authorized)
        (b) Slashing burn component (50% of slash penalties)
        (c) Pending timeout fees (2% of timed-out pending amounts)
    Effect: total_aic_supply -= burn_amount; source_balance -= burn_amount
    Conservation delta: LHS decreases by burn_amount; RHS decreases by burn_amount. Net: 0.

RULE SUPPLY-3 (No Spontaneous Generation):
    No operation may increase total_aic_supply without a TREASURY_MINT event.
    No operation may decrease total_aic_supply without a TREASURY_BURN or burn event.
    Enforcement: EABS settlement function rejects any batch that violates SUPPLY-3.
    Detection: Post-batch conservation check (Section 9.4).
```

## 9.2 Proof Sketch: EABS Preserves Conservation

**Theorem:** If CONS-1 holds at epoch E, and the EABS settlement function processes a valid epoch batch B(E+1), then CONS-1 holds at epoch E+1.

**Proof:** By structural induction on the operation types in the batch. We show each operation type preserves conservation. Since the batch is a sequence of conservation-preserving operations processed atomically, conservation holds for the complete batch.

### Case 1: AIC_TRANSFER(sender, receiver, amount)

```
Pre:   aic_balance(sender) = S, aic_balance(receiver) = R
Post:  aic_balance(sender) = S - amount, aic_balance(receiver) = R + amount

CONS-1 delta:
    Sigma(aic_balance) changes by: -amount + amount = 0
    All other terms unchanged. Conservation preserved. QED
```

### Case 2: AIC_STAKE(entity, amount)

```
Pre:   aic_balance(entity) = A, staked_aic(entity) = S
Post:  aic_balance(entity) = A - amount, staked_aic(entity) = S + amount

CONS-1 delta:
    Sigma(aic_balance): -amount
    Sigma(staked_aic): +amount
    Net LHS delta: 0. Conservation preserved. QED
```

### Case 3: AIC_UNSTAKE(entity, amount)

```
Reverse of Case 2. Conservation preserved by symmetry. QED
```

### Case 4: PENDING_INITIATE(sender, receiver, amount)

```
Pre:   aic_balance(sender) = A, collateral_held(sender) = C
       pending_out(sender) = PO, pending_in(receiver) = PI
Post:  aic_balance(sender) = A - amount - collateral
       collateral_held(sender) = C + collateral
       pending_out(sender) = PO + amount
       pending_in(receiver) = PI + amount

WHERE collateral = amount * 0.05

CONS-1 delta (using canonical formula with CONS-1a simplification):
    Sigma(aic_balance): -(amount + collateral)
    Sigma(collateral_held): +collateral
    Sigma(pending_out): +amount
    Net LHS delta: -(amount + collateral) + collateral + amount = 0
    Conservation preserved. QED
```

### Case 5: PENDING_COMPLETE(sender, receiver, amount)

```
Pre:   pending_out(sender) = PO, pending_in(receiver) = PI
       aic_balance(receiver) = R, collateral_held(sender) = C
Post:  pending_out(sender) = PO - amount
       pending_in(receiver) = PI - amount
       aic_balance(receiver) = R + amount
       collateral_held(sender) = C - collateral
       aic_balance(sender) += collateral   [collateral returned]

CONS-1 delta:
    Sigma(aic_balance): +amount + collateral
    Sigma(pending_out): -amount
    Sigma(collateral_held): -collateral
    Net: +amount + collateral - amount - collateral = 0. QED
```

### Case 6: PENDING_TIMEOUT(sender, receiver, amount)

```
timeout_fee = amount * 0.02

Post:  pending_out(sender) -= amount
       aic_balance(sender) += amount + (collateral - timeout_fee)
       collateral_held(sender) -= collateral
       total_aic_supply -= timeout_fee     [fee burned]

CONS-1 delta:
    LHS delta = (amount + collateral - timeout_fee) - amount - collateral
              = -timeout_fee
    RHS delta (total_supply): -timeout_fee
    LHS delta = RHS delta. Conservation preserved. QED
```

### Case 7: SLASH(violator, amount, distribution)

```
burn_amount     = amount * 0.50
treasury_amount = amount * 0.30
reporter_amount = amount * 0.20

Post:  staked_aic(violator) -= amount
       treasury_balance += treasury_amount
       aic_balance(reporter) += reporter_amount
       total_aic_supply -= burn_amount

CONS-1 delta:
    LHS delta = -amount + 0.30*amount + 0.20*amount = -0.50*amount
    RHS delta (total_supply): -0.50*amount
    LHS delta = RHS delta. Conservation preserved. QED
```

### Case 8: TREASURY_MINT(amount)

```
Post:  total_aic_supply += amount; treasury_balance += amount
LHS delta: +amount. RHS delta: +amount. Conservation preserved. QED
```

### Case 9: TREASURY_BURN(amount)

```
Post:  total_aic_supply -= amount; treasury_balance -= amount
LHS delta: -amount. RHS delta: -amount. Conservation preserved. QED
```

### Case 10: REWARD_B_CLASS / REWARD_V_CLASS / REWARD_G_CLASS

```
Post:  reward_pool (part of treasury_balance) -= adjusted_amount
       aic_balance(recipient) += adjusted_amount

CONS-1 delta:
    treasury_balance: -adjusted_amount
    Sigma(aic_balance): +adjusted_amount
    Net: 0. Conservation preserved. QED
```

### Case 11: PC_EARN / PC_SPEND / PC_DECAY

```
PCs are not part of CONS-1 or CONS-2. No effect on conservation. QED
```

### Case 12: CS_ALLOCATE / CS_RELEASE / CS_REVERT

```
CS operations move units between cs_allocation and unallocated_cs.
CONS-2: Sigma(cs_allocation) + Sigma(pending_cs) + unallocated = total_cs_supply
Each operation transfers between two terms on the LHS. Net delta: 0. QED
```

**Conclusion:** Every operation type preserves CONS-1 (and CONS-2 for CS operations). Since EABS processes operations sequentially in deterministic order, and each preserves conservation, the complete batch preserves conservation. The explicit post-batch check (Section 9.4) provides runtime verification. QED

## 9.3 Pending State Lifecycle

Pending states represent in-flight economic transitions that have been initiated but not yet settled. They are the primary mechanism for cross-entity transactions that require coordination or confirmation, and they represent the most complex aspect of conservation accounting because resources exist simultaneously in "committed but not yet allocated" limbo. The design ensures that pending states cannot be exploited as denial-of-service vectors (Adversarial Finding 9 — Limbo Attack) through mandatory timeouts, collateral requirements, and volume caps.

### 9.3.1 State Machine

```
PendingState := ENUM {
    INITIATED,     // Sender's alloc reduced, pending_out/pending_in created
    CONFIRMING,    // Receiver acknowledged, awaiting EABS settlement
    COMPLETING,    // EABS processing CompletePending in current batch
    COMPLETED,     // Settled — pending cleared, receiver alloc increased
    TIMING_OUT,    // Timeout threshold reached, auto-revert initiated
    TIMED_OUT,     // Reverted — alloc returned to sender minus fee
    DISPUTED       // Dispute filed — enters G-class governance
}

State Transitions:
    INITIATED   --> CONFIRMING      receiver acknowledgment within 1 epoch
    CONFIRMING  --> COMPLETING      EABS includes CompletePending in batch
    COMPLETING  --> COMPLETED       EABS batch settles successfully
    INITIATED   --> TIMING_OUT      no confirmation after 2 epochs
    CONFIRMING  --> TIMING_OUT      no completion after 3 epochs from initiation
    TIMING_OUT  --> TIMED_OUT       EABS processes TimeoutPending
    Any state   --> DISPUTED        dispute filed before timeout (pauses clock)
    DISPUTED    --> COMPLETING      dispute resolved in favor of completion
    DISPUTED    --> TIMING_OUT      dispute resolved in favor of revert
```

### 9.3.2 Timeout Enforcement

All pending states have a mandatory maximum duration of 3 epochs (SETTLEMENT_TICKs). This prevents the Limbo Attack (Adversarial Finding 9) by ensuring resources cannot be locked indefinitely.

```
STRUCTURE PendingTimeout:
    max_duration_epochs:   3
    fee_on_timeout:        0.02       // 2% of pending amount
    fee_destination:       BURNED     // Not redistributed — prevents gaming

FUNCTION check_pending_timeouts(epoch: EpochID, registry: PendingRegistry):
    FOR ps IN registry.all_pending():
        IF ps.state IN {INITIATED, CONFIRMING}:
            age = epoch - ps.initiated_epoch
            IF age >= 3:
                EMIT TimeoutPending(ps)
                // Fee deducted from collateral deposit
                fee = ps.amount * 0.02
                EMIT Burn(fee)
                // Remaining collateral + original amount returned to sender
                EMIT Credit(ps.sender, ps.amount + (ps.collateral - fee))
```

### 9.3.3 Collateral Requirements

Initiating a pending state requires a 5% collateral deposit, separate from the pending amount itself. This makes the Limbo Attack costly.

```
STRUCTURE PendingCollateral:
    rate:                   0.05      // 5% of pending amount
    source:                 "Deducted from sender's aic_balance"
    return_on_completion:   true
    forfeit_on_timeout:     partial   // Fee burned, remainder returned
    forfeit_distribution:
        timeout_fee:        "2% of pending amount (burned)"
        remaining:          "3% of pending amount (returned to sender)"
```

### 9.3.4 Volume Caps

Volume caps prevent any single entity or the system as a whole from accumulating excessive pending state, which would constitute a denial-of-service via resource lockup.

```
INVARIANT PENDING-CAP-1 (Per-Entity):
    FOR ALL entities E, resource_types R:
        pending_out(E, R) <= 0.10 * total_supply(R)

INVARIANT PENDING-CAP-2 (Global):
    FOR ALL resource_types R:
        Sigma_{i}( pending_out(i, R) ) <= 0.25 * total_supply(R)

Enforcement: InitiatePending is REJECTED by EABS if either cap would be violated.
Detection: Checked during EABS batch processing — deterministic, same on all nodes.

Economic analysis of Limbo Attack cost:
    Attacker locks X AIC in pending for 3 epochs.
    Collateral cost: 0.05 * X
    Timeout fee (burned): 0.02 * X
    Opportunity cost: 3 epochs of staking/settlement rewards foregone on X
    Total cost per cycle: ~0.02*X + opportunity_cost(X, 3 epochs)
    Per-entity cap: X <= 0.10 * total_supply
    Maximum lockable: 0.10 * total_supply per entity, 0.25 * total_supply globally
    Conclusion: Sustained locking is economically irrational at any meaningful scale.
```

```
FUNCTION initiate_pending(sender, receiver, amount, resource_type):
    collateral = amount * 0.05
    total_deduction = amount + collateral

    REQUIRE aic_balance(sender) >= total_deduction
    REQUIRE pending_out(sender) + amount <= 0.10 * total_supply   // PENDING-CAP-1
    REQUIRE global_pending() + amount <= 0.25 * total_supply      // PENDING-CAP-2

    aic_balance(sender) -= total_deduction
    pending_out(sender) += amount
    pending_in(receiver) += amount
    collateral_held(sender) += collateral

    // Conservation: aic_balance decreased by (amount + collateral)
    //               collateral_held increased by collateral
    //               pending_out increased by amount
    //               Net change to CONS-1 LHS: 0 (proven in Section 9.2 Case 4)
```

## 9.4 Runtime Enforcement via EABS

The conservation invariant is enforced at runtime by the EABS settlement function, not merely proven correct in theory. This closes the gap identified in the Science Assessment (2/5 for conservation verification).

```
FUNCTION eabs_conservation_check(
    state: SettlementState,
    resource_types: Vec<ResourceType>
) -> Result<(), ConservationViolation>:

    // AIC Conservation (CONS-1)
    total_aic_accounts = 0
    total_staked = 0
    total_pending_out = 0
    total_pending_in = 0
    total_collateral = 0

    FOR account IN state.accounts.values():
        total_aic_accounts += account.aic_balance.value()
        total_staked += account.staked_aic.value()
        total_pending_out += account.pending_out.value()
        total_pending_in += account.pending_in.value()
        total_collateral += account.collateral_held.value()

    aic_lhs = total_aic_accounts + total_staked + total_pending_out
            + total_collateral + state.treasury_balance
    aic_rhs = state.total_aic_supply

    IF aic_lhs != aic_rhs:
        RETURN Err(ConservationViolation {
            invariant: "CONS-1",
            expected: aic_rhs,
            actual: aic_lhs,
            delta: aic_lhs - aic_rhs,
        })

    // Pending Balance (CONS-1a)
    IF total_pending_out != total_pending_in:
        RETURN Err(ConservationViolation {
            invariant: "CONS-1a",
            expected: total_pending_out,
            actual: total_pending_in,
        })

    // CS Conservation (CONS-2) — per resource type
    FOR rt IN resource_types:
        total_cs_held = 0
        total_cs_pending = 0
        FOR account IN state.accounts.values():
            total_cs_held += account.cs_allocation(rt).value()
        FOR pending IN state.pending_registry.values():
            IF pending.resource_type == rt:
                total_cs_pending += pending.amount

        cs_lhs = total_cs_held + total_cs_pending + state.unallocated_cs(rt)
        cs_rhs = state.total_cs_supply(rt)

        IF cs_lhs != cs_rhs:
            RETURN Err(ConservationViolation {
                invariant: "CONS-2",
                resource_type: rt,
                expected: cs_rhs,
                actual: cs_lhs,
            })

    RETURN Ok(())
```

### 9.4.1 Recovery Protocol for Conservation Violations

A conservation violation during EABS settlement indicates a bug in the settlement function, not an external attack (attacks are prevented by per-operation validation). The recovery protocol is defensive-in-depth:

```
PROTOCOL ConservationRecovery:
    TRIGGER: eabs_conservation_check returns Err(ConservationViolation)

    Step 1: HALT SETTLEMENT
        All nodes halt settlement for the current epoch.
        CRDT read-path continues operating (optimistic reads still available).
        EMIT ConservationViolationAlert to all governance participants.
        Alert includes: epoch, invariant violated, expected value, actual value, delta.

    Step 2: REPLAY WITH PER-OPERATION CHECKS
        Re-process the epoch batch with conservation checked after each operation:

        working_state = pre_state.clone()
        FOR op IN batch.operations_sorted():
            pre_check = eabs_conservation_check(working_state)
            ASSERT pre_check.is_ok()   // Must hold before operation

            apply_operation(working_state, op)

            post_check = eabs_conservation_check(working_state)
            IF post_check.is_err():
                IDENTIFY op as the violating operation
                LOG_CRITICAL("Violating operation: {}", op)
                BREAK

    Step 3: QUARANTINE AND RETRY
        Remove the identified violating operation from the batch.
        Re-process batch without it.
        IF conservation now holds:
            Settle the epoch with the reduced batch.
            EMIT QuarantinedOperation(op) for governance review.
        ELSE:
            Binary search: remove operations one by one until conservation holds.
            Settle with the maximum valid subset.

    Step 4: ROOT CAUSE ANALYSIS
        Governance must classify the quarantined operation within 5 epochs:
            (a) Bug in settlement function — highest priority fix
            (b) Malformed operation that passed validation — validation bug
            (c) Novel attack vector — update adversarial model
        Until classified, the operation type that caused the violation
        is temporarily disabled (conservative safety measure).

    PROPERTIES:
        - Liveness: Settlement resumes within 1 epoch (reduced batch).
        - Safety: No conservation-violating state is ever committed.
        - Determinism: All honest nodes detect the same violation and
          execute the same recovery protocol (same batch, same operations,
          same binary search, same result).
```

## 9.5 I-Confluence Analysis for Read-Path Operations

I-confluence (invariant confluence) characterizes operations that can be executed concurrently on different CRDT replicas while preserving application invariants. For DSF, the relevant question is: which operations can safely use the CRDT read-path without coordination?

```
READ-PATH OPERATIONS — I-Confluence Analysis:

1. BalanceQuery(entity, budget_type) -> uint64
    I-confluent: YES
    Justification: Pure read. No state mutation. Trivially confluent.
    Returns: ECOR balance (settled + optimistic delta).

2. AvailabilityCheck(resource_type) -> uint64
    I-confluent: YES
    Justification: Aggregation query over CRDT counters.
    Returns: Eventually-consistent estimate of available capacity.
    Caveat: Different replicas may return different values during convergence.

3. OptimisticDeltaUpdate(entity, budget_type, delta) -> void
    I-confluent: YES (with caveat)
    Justification: PN-Counter increment/decrement. CRDTs guarantee convergence
    via commutativity of the max() merge function.
    Caveat: Optimistic deltas may show balances invalidated at EABS settlement.
    This is acceptable because optimistic reads are explicitly non-binding.

4. PendingStateQuery(entity) -> Vec<PendingState>
    I-confluent: YES
    Justification: Read-only set query. Pending states are modified via EABS
    (write-path) and replicated via CRDT. Queries return last-known state.

5. CapabilityScoreQuery(entity) -> float64
    I-confluent: YES
    Justification: Read of cached value. Capability scores are recomputed
    during V-class EABS settlement and cached in the CRDT layer.

6. EpochMetadataQuery(epoch) -> EpochMetadata
    I-confluent: YES
    Justification: Metadata is append-only. Once an epoch settles,
    its metadata never changes.

NON-I-CONFLUENT OPERATIONS (MUST use EABS write-path):
    - AIC_TRANSFER (could violate CONS-1 if concurrent)
    - PENDING_INITIATE/COMPLETE/TIMEOUT (could violate PENDING-CAP)
    - SLASH (requires ordering for graduated penalties)
    - TREASURY_MINT/BURN (modifies total_supply)
    - CS_ALLOCATE (could violate position limits)
    - REWARD_* (modifies reward pools)
    - Any operation that could violate conservation if executed concurrently

FORMAL STATEMENT:
    Let T_read = {BalanceQuery, AvailabilityCheck, OptimisticDeltaUpdate,
                  PendingStateQuery, CapabilityScoreQuery, EpochMetadataQuery}
    Let T_write = OperationType \ T_read

    Theorem: For any set of concurrent operations O where all o in O
    have type in T_read, executing O on any set of CRDT replicas in any
    order produces converging state that does not violate CONS-1, CONS-2,
    PENDING-CAP-1, or PENDING-CAP-2.

    Proof: T_read operations are either pure reads (no state change) or
    PN-Counter increments/decrements on optimistic delta fields. The
    optimistic delta fields are NOT part of the conservation invariant
    (conservation is defined over settled state). CRDT merge on PN-Counters
    is commutative, associative, and idempotent. Therefore concurrent
    execution converges regardless of ordering, and conservation invariants
    (which reference only settled state) are unaffected. QED
```

## 9.6 Test Vectors

```
TEST VECTOR TV-1: Simple Transfer
    Pre-state:
        Account A: aic_balance=1000, staked=500
        Account B: aic_balance=200, staked=0
        Treasury: 300, Total supply: 2000
    Operation: AIC_TRANSFER(A, B, 100)
    Post-state:
        Account A: aic_balance=900, staked=500
        Account B: aic_balance=300, staked=0
        Treasury: 300, Total supply: 2000
    CONS-1 check: 900 + 300 + 500 + 0 + 0 + 0 + 300 = 2000. PASS

TEST VECTOR TV-2: Slash with Burn
    Pre-state:
        Account V (violator): staked=1000
        Account R (reporter): aic_balance=50
        Treasury: 5000, Total supply: 10000
    Operation: SLASH(V, 200, reporter=R)
        burn=100, treasury=60, reporter=40
    Post-state:
        Account V: staked=800
        Account R: aic_balance=90
        Treasury: 5060, Total supply: 9900 (100 burned)
    CONS-1 check: 90 + 800 + 0 + 0 + 5060 = 5950.
    Remaining accounts sum to 3950. Total LHS = 9900. PASS

TEST VECTOR TV-3: Pending Initiate + Timeout
    Pre-state:
        Account S: aic_balance=1000, Account R: aic_balance=500
        Treasury: 2000, Total supply: 3500
    Operation 1: PENDING_INITIATE(S, R, 200)
        collateral = 10 (5% of 200)
        Post: S.aic_balance=990, S.collateral_held=10,
              S.pending_out=200, R.pending_in=200
    CONS-1 (using canonical formula without pending_in):
        LHS = 990 + 500 + 0 + 200 + 10 + 2000 = 3700. But total=3500?
        CORRECTION: S.aic_balance = 1000 - 10 (collateral) = 990.
        The pending amount does NOT come from aic_balance — it is a
        commitment recorded in pending_out. aic_balance only loses collateral.
        LHS = 990 + 500 + 0(staked) + 200(pend_out) + 10(coll) + 2000 = 3700.
        This exceeds 3500 by 200 because pending_out represents a future
        transfer, not a current deduction from aic_balance.

        CORRECTED IMPLEMENTATION: PENDING_INITIATE deducts (amount + collateral)
        from aic_balance, places amount in pending_out, collateral in collateral_held.
        S.aic_balance = 1000 - 200 - 10 = 790
        LHS = 790 + 500 + 0 + 200 + 10 + 2000 = 3500. PASS
        CONS-1a: pending_out=200 = pending_in=200. PASS

    Operation 2 (3 epochs later): PENDING_TIMEOUT(S, R, 200)
        timeout_fee = 4 (2% of 200), burned
        S.aic_balance += 200 + (10 - 4) = 206, so S.aic_balance = 790 + 206 = 996
        S.pending_out = 0, R.pending_in = 0, S.collateral_held = 0
        total_supply = 3500 - 4 = 3496
    CONS-1: 996 + 500 + 0 + 0 + 0 + 2000 = 3496. PASS

TEST VECTOR TV-4: Concurrent Operations Within Single Epoch
    Pre-state:
        A: aic_balance=500, staked=200
        B: aic_balance=300, staked=100
        C: aic_balance=200, staked=50
        Treasury: 1000, Total supply: 2350
    Epoch batch (in canonical order):
        1. SLASH(B, 50, reporter=C)     // burn=25, treasury=15, reporter=10
        2. AIC_TRANSFER(A, B, 100)
        3. AIC_STAKE(A, 50)
        4. REWARD_B_CLASS(C, 30, SCHEDULING)
    After op 1: B.staked=50, C.aic=210, treasury=1015, total=2325
    After op 2: A.aic=400, B.aic=400
    After op 3: A.aic=350, A.staked=250
    After op 4: C.aic=240, treasury=985 (reward_pool reduced by 30)
    FINAL CONS-1:
        Sigma(aic_balance) = 350 + 400 + 240 = 990
        Sigma(staked) = 250 + 50 + 50 = 350
        Treasury = 985
        LHS = 990 + 350 + 985 = 2325
        RHS = 2325. PASS.
```

---

# Section 10: Graduated Slashing System

The graduated slashing system imposes escalating economic penalties for protocol violations. It resolves Adversarial Finding 7 (Slashing Ordering Attack) by processing all violations through EABS with deterministic canonical ordering.

## 10.1 Design Principles

1. **Determinism (SLASH-DET).** Given the same violation history and epoch batch, every honest node computes identical penalties.
2. **Monotonicity (SLASH-MON).** An entity's violation count never decreases (except via governance appeal).
3. **Proportionality (SLASH-PROP).** Penalty severity is proportional to both the offense number and the violation type severity.

## 10.2 EABS-Ordered Deterministic Processing

```
FUNCTION process_slashing(epoch_batch: EpochBatch) -> Vec<SlashingOutcome>:
    violations = epoch_batch.operations
        .filter(|op| op.op_type == VIOLATION_REPORT)

    // Canonical sort — DETERMINISTIC
    violations.sort_by(|v| (
        v.violation_type.canonical_order(),
        HASH(v.detection_timestamp),
        v.violator_id
    ))

    outcomes = []
    FOR v IN violations:
        entity_state = get_violation_state(v.violator_id)
        offense_number = entity_state.violation_count + 1

        IF NOT validate_violation_report(v):
            outcomes.push(SlashingOutcome::Rejected(v, "Invalid report"))
            CONTINUE

        penalty = compute_penalty(offense_number, v.violation_type, v.violator_id)
        slash_ops = atomic_slash(v.violator_id, penalty.amount, v.reporter_id)
        outcomes.push(SlashingOutcome::Applied(v, penalty, slash_ops))

        entity_state.violation_count = offense_number
        entity_state.last_violation_epoch = current_epoch
        entity_state.violation_history.push(ViolationRecord {
            epoch: current_epoch,
            violation_type: v.violation_type,
            offense_number: offense_number,
            penalty: penalty,
        })

    RETURN outcomes
```

### 10.2.1 Canonical Sort Rationale

The sort key `(violation_type, detection_timestamp_hash, violator_id)` ensures:

- **violation_type first:** Groups by type so concurrent violations of different types for the same entity are processed in a deterministic, type-based order regardless of detection timing.
- **detection_timestamp_hash second:** Using the HASH of the timestamp (not the timestamp itself) prevents attackers from choosing timestamps to influence ordering. The hash is cryptographically unpredictable relative to the violation content.
- **violator_id third:** Final tiebreaker for complete determinism. Handles the astronomically unlikely case of identical type and timestamp hash.

```
Canonical Order (for deterministic sort):
    SCHEDULING_VIOLATION:     0
    VERIFICATION_FRAUD:       1
    COMMUNICATION_ABUSE:      2
    GOVERNANCE_MANIPULATION:  3
    CSO_BREACH:               4
```

## 10.3 Five-Level Slashing Schedule

```
STRUCTURE SlashingSchedule:
    levels: [
        Level 1 (First Offense):
            penalty_rate:       0.01      // 1% of staked AIC
            additional_action:  "Warning emitted"
            capability_impact:  NONE
            recovery_path:      "Automatic after 20 violation-free epochs"

        Level 2 (Second Offense):
            penalty_rate:       0.05      // 5%
            additional_action:  "Entity flagged for monitoring"
            capability_impact:  NONE
            recovery_path:      "Automatic after 50 violation-free epochs"

        Level 3 (Third Offense):
            penalty_rate:       0.15      // 15%
            additional_action:  "Position limits reduced to 10%"
            capability_impact:  "capability_score *= 0.8"
            recovery_path:      "Governance appeal or 100 violation-free epochs"

        Level 4 (Fourth Offense):
            penalty_rate:       0.50      // 50%
            additional_action:  "capability_score hard reset to 1.0"
            capability_impact:  "capability_score = 1.0"
            recovery_path:      "Governance appeal only"

        Level 5 (Fifth+ Offense):
            penalty_rate:       1.00      // 100%
            additional_action:  "Permanent exclusion from settlement and markets"
            capability_impact:  "Entity banned"
            recovery_path:      "Governance appeal with supermajority (67%)"
    ]
```

### 10.3.1 Violation Types and Severity Multipliers

```
ViolationType := ENUM {
    SCHEDULING_VIOLATION,        // 1.0x (baseline)
    VERIFICATION_FRAUD,          // 1.5x (undermines trust infrastructure)
    COMMUNICATION_ABUSE,         // 0.8x (lower per-incident impact)
    GOVERNANCE_MANIPULATION,     // 2.0x (threatens system integrity)
    CSO_BREACH,                  // 1.2x (economic infrastructure damage)
}
```

### 10.3.2 Penalty Computation

```
FUNCTION compute_penalty(
    offense_number: uint32,
    violation_type: ViolationType,
    violator_id: EntityID
) -> Penalty:
    level = MIN(offense_number, 5)
    base_rate = SLASHING_SCHEDULE[level].penalty_rate
    severity = violation_type.severity_multiplier()
    staked_aic = get_staked_aic(violator_id)
    penalty_amount = floor(staked_aic * base_rate * severity)
    penalty_amount = MIN(penalty_amount, staked_aic)
    RETURN Penalty { amount: penalty_amount, level: level, ... }
```

### 10.3.3 Evidence Requirements

Each violation type requires specific evidence for the report to be valid:

```
Evidence Requirements by Violation Type:

SCHEDULING_VIOLATION:
    - TaskAssignmentRecord:  Proof the task was assigned to this entity
    - DeadlineRecord:        Proof the deadline has passed
    - NonCompletionProof:    Proof the task was not completed or was late

VERIFICATION_FRAUD:
    - AttestationRecord:     The false attestation submitted by the entity
    - GroundTruthRecord:     The correct verification result
    - DiscrepancyProof:      Formal proof of mismatch between attestation and truth

COMMUNICATION_ABUSE:
    - MessageLog:            The offending messages
    - ProtocolSpec:          Which native communication rule was violated
    - PatternAnalysis:       Evidence of systematic (not accidental) abuse

GOVERNANCE_MANIPULATION:
    - VoteRecord:            The manipulated votes or proposals
    - CorrelationAnalysis:   Evidence of coordination or vote buying
    - ConstitutionalRef:     Which constitutional rule was violated

CSO_BREACH:
    - CSORecord:             The Capacity Slice Obligation in question
    - DeliveryLog:           What was promised vs. what was delivered
    - ShortfallProof:        Quantitative evidence of non-delivery
```

## 10.4 Appeal Mechanism

```
STRUCTURE SlashingAppeal:
    appeal_id:          AppealID
    original_violation: ViolationID
    appellant:          EntityID
    bond:               Decimal(18,8)       // 10% of slashed amount
    filed_epoch:        EpochID
    deadline_epoch:     EpochID             // filed_epoch + 10
    evidence:           Vec<Evidence>
    status:             AppealStatus

AppealStatus := ENUM {
    FILED,          // Bond posted, evidence submitted
    REVIEWING,      // Governance committee assigned
    UPHELD,         // Original slash stands, bond forfeited
    OVERTURNED,     // Slash reversed, bond + penalty returned
    EXPIRED,        // No decision in 10 epochs — defaults to UPHELD
}

PROTOCOL Appeal:
    Step 1: Appellant posts bond = 10% of slashed amount via EABS.
    Step 2: Appeal enters G-class governance queue.
    Step 3: Governance committee (5 members, randomly selected,
            capability-weighted) reviews all evidence.
    Step 4: Committee votes (simple majority).

        IF UPHELD:
            Bond forfeited: 50% burned, 30% treasury, 20% original reporter.
            Original penalty stands.
            Violation count unchanged.

        IF OVERTURNED:
            Bond returned to appellant.
            Slashed amount returned to appellant.
            violation_count decremented by 1 (ONLY decrement path).
            Original reporter receives COMMUNICATION_ABUSE flag
            (false reporting penalty).

    Step 5: Decision recorded in EABS batch as G-class settlement.

    TIMEOUT: No decision within 10 epochs -> defaults to UPHELD.
    Prevents griefing via endless appeals.
```

## 10.5 Slashing Revenue Distribution

```
RULE SLASH-DIST:
    FOR EACH slash penalty P:
        burn_amount      = P.amount * 0.50   // Burned — reduces total supply
        treasury_amount  = P.amount * 0.30   // Treasury — funds public goods
        reporter_amount  = P.amount * 0.20   // Reporter — incentivizes detection

    INVARIANT: burn + treasury + reporter = P.amount
    Rounding dust assigned to treasury.

    FUNCTION atomic_slash(violator, amount, reporter) -> Vec<Operation>:
        burn = floor(amount * 0.50)
        treasury = floor(amount * 0.30)
        reporter_reward = amount - burn - treasury   // Absorbs rounding
        ops = [
            Deduct(violator.staked_aic, amount),
            Credit(TREASURY, treasury),
            Credit(reporter, reporter_reward),
            ReduceSupply(burn),
        ]
        RETURN AtomicGroup(ops)

Distribution Rationale:
    50% BURN:     Deflationary pressure. Ensures slashing is net-destructive
                  (not merely redistributive), preventing profit-motivated
                  false accusations.
    30% TREASURY: Funds public goods. Protocol benefits from enforcement.
    20% REPORTER: Incentivizes violation detection. Capped at 20% so that
                  "slashing bounty hunting" is less profitable than
                  productive work.

Anti-Gaming Rules:
    - Reporter reward ONLY paid if violation confirmed by EABS.
    - False reports are themselves COMMUNICATION_ABUSE violations.
    - Reporter must provide evidence meeting type-specific requirements.
    - Reporter cannot be same entity or Sentinel Graph cluster as violator.
    - Reporter cannot file more than 5 reports per epoch (rate limit).
```

## 10.6 Cross-Entity Collusion Detection

```
FUNCTION detect_and_slash_collusion(alert: SentinelClusterAlert):
    cluster = alert.cluster
    evidence = alert.evidence

    // Require high confidence before slashing for collusion
    IF evidence.confidence < 0.90:
        LOG("Insufficient confidence for collusion slash: {}", evidence.confidence)
        RETURN   // Flag for monitoring but do not slash

    // Each entity in the cluster receives an independent violation
    FOR entity IN cluster.entities:
        report = ViolationReport {
            violator_id: entity,
            violation_type: GOVERNANCE_MANIPULATION,    // 2.0x severity
            evidence: evidence,
            reporter_id: SENTINEL_SYSTEM_ID,
            detection_timestamp: current_timestamp(),
        }
        SUBMIT report to EABS batch

    // Reclaim excess cluster-level position
    excess = effective_position(cluster) - 0.15 * total_supply
    IF excess > 0:
        FOR entity IN cluster.entities:
            share = allocated(entity) / effective_position(cluster)
            reclaim = floor(excess * share)
            SUBMIT Reclaim(entity, reclaim) to EABS batch
```

## 10.7 Formal Properties

**Property SLASH-DET (Determinism):**

```
For any two honest nodes A and B processing the same epoch batch:
    slashing_outcomes_A(batch) = slashing_outcomes_B(batch)

Proof: Both nodes sort violations using identical canonical sort key.
Both apply the same compute_penalty function. Both read from the same
pre-epoch state (EABS guarantees state agreement at epoch boundaries).
The penalty function is a pure function of (offense_number, violation_type,
staked_aic). Therefore outputs are identical. QED
```

**Property SLASH-MON (Monotonicity):**

```
For any entity E, violation_count is monotonically non-decreasing:
    FOR ALL epochs E1 < E2:
        violation_count(E, E1) <= violation_count(E, E2)

Exception: Successful appeal decrements by 1. This is the ONLY
decrement path and requires G-class governance settlement.

Proof: violation_count is incremented by 1 for each processed violation
in the EABS batch. EABS state is append-only for violation records.
The only decrement path is the OVERTURNED appeal outcome, which
requires governance committee majority vote. QED
```

**Property SLASH-PROP (Proportionality):**

```
For violations V1, V2 of entity E:
    IF V1.offense_number < V2.offense_number (same violation type):
        penalty(V1) <= penalty(V2)

    IF V1.severity < V2.severity (same offense number):
        penalty(V1) <= penalty(V2)

Proof: penalty = staked_aic * base_rate(offense_number) * severity(type).
base_rate is monotonically increasing: 0.01, 0.05, 0.15, 0.50, 1.00.
severity is a fixed positive multiplier per type.
Product of non-negative monotonically increasing factors is itself
monotonically increasing in each factor. QED
```

---

# Section 11: Treasury and Governance

## 11.1 Treasury-First Issuance Model

All AIC enters circulation exclusively through the treasury. There is no mining, no staking reward generation outside treasury authorization, and no mechanism by which any entity can create AIC independently. This eliminates an entire class of inflation attacks.

```
STRUCTURE Treasury:
    balance:              Decimal(18,8)
    total_issued:         Decimal(18,8)       // Lifetime cumulative
    total_burned:         Decimal(18,8)       // Lifetime from slashing + fees
    circulating_supply:   Decimal(18,8)       // total_issued - total_burned - balance
    allocation_budgets:   Map<AllocationCategory, Decimal(18,8)>
    constitutional_caps:  ConstitutionalCaps
    pending_proposals:    Vec<GovernanceProposal>

INVARIANT TREASURY-CONS:
    treasury.balance + circulating_supply + total_burned = total_issued
    WHERE circulating_supply = Sigma_{i != treasury}( aic_balance(i) + staked(i) +
                               pending_out(i) + collateral_held(i) )

AllocationCategory := ENUM {
    SETTLEMENT_REWARDS,     // 60% — funds four-stream settlement pools
    BOOTSTRAP_CAPACITY,     // 15% — funds sovereign reserve lanes and bounded temporary leased backstops
    DEVELOPMENT_GRANTS,     // 10% — system improvement funding, including C47 promotion/quarantine work
    EMERGENCY_RESERVE,      // 15% — constitutionally protected floor
}

Post-Bootstrap Allocation (after CPLR sunset):
    SETTLEMENT_REWARDS:  70%
    BOOTSTRAP_CAPACITY:   0%
    DEVELOPMENT_GRANTS:  15%
    EMERGENCY_RESERVE:   15%
```

Under the T-304 economics posture, treasury-funded capacity follows an explicit build-vs-buy order: fund sovereign reserve capacity first, fund `C47` adaptation/quarantine and native promotion second, and admit `C45` leased cognition only as a bounded temporary bridge when no sovereign or in-flight promoted lane can satisfy demand within safety and time constraints.

## 11.2 Constitutional Protections

Constitutional protections are parameters that cannot be changed by normal governance. They require supermajority amendment.

```
STRUCTURE ConstitutionalCaps:
    // Supply caps
    max_total_supply:             Decimal(18,8)   // Absolute ceiling
    quarterly_issuance_cap:       Decimal(18,8)   // Per 50-epoch quarter
    max_single_issuance:          Decimal(18,8)   // Per proposal

    // Spending limits
    max_treasury_spend_per_epoch: Decimal(18,8)
    emergency_reserve_floor:      Decimal(18,8)   // Treasury must stay above

    // Governance protections
    supermajority_threshold:      0.67            // For constitutional changes
    amendment_cooling_period:     20 epochs       // Between proposal and vote
    max_parameter_change_rate:    0.20            // No param changes >20%/cycle

    // Slashing protections
    max_single_slash_rate:        1.00            // Up to 100% (5th offense)
    min_appeal_window:            10 epochs       // Cannot be shortened

INVARIANT CONST-1 (Constitutional Immutability):
    Constitutional caps may ONLY be modified by:
        1. Supermajority vote (>= 67% of effective governance weight)
        2. After cooling period of 20 epochs from proposal
        3. With maximum change rate of 20% per amendment
    Any attempt to bypass this process is a GOVERNANCE_MANIPULATION violation.
```

### 11.2.1 Constitutional Amendment Process

```
PROTOCOL ConstitutionalAmendment:
    Phase 1 — PROPOSAL (1 epoch):
        Proposer submits amendment:
            parameter:       ConstitutionalParam
            current_value:   current setting
            proposed_value:  new setting
            rationale:       text
            bond:            5% of treasury balance
        REQUIRE |proposed_value - current_value| / current_value <= 0.20
        EMIT AmendmentProposed

    Phase 2 — COOLING (20 epochs):
        No voting. Community deliberation period.
        Proposer may withdraw (bond returned minus 1% fee).
        Counter-proposals may be filed independently.

    Phase 3 — VOTING (5 epochs):
        Eligible voters: all entities with effective_stake > 0
        Vote weight: staked_aic * SQRT(capability_score)
        Options: FOR, AGAINST, ABSTAIN
        Quorum: 50% of total effective governance weight must vote
        Threshold: 67% of voting weight must vote FOR

    Phase 4 — EXECUTION (1 epoch delay):
        IF passed:
            Parameter updated in next EABS G-class settlement
            Proposer bond returned in full
        IF failed:
            Proposer bond forfeited (50% burned, 50% treasury)
```

## 11.3 Governance Parameter Taxonomy

```
TIER 1 — CONSTITUTIONAL (supermajority required):
    max_total_supply, quarterly_issuance_cap, supermajority_threshold,
    amendment_cooling_period, min_appeal_window, slashing_schedule,
    four_stream_weights, budget_type_definitions

TIER 2 — GOVERNANCE (simple majority G-class required):
    epoch_duration, pc_decay_rate, cs_position_limit, capability_score_cap,
    reserve_pricing_floors, challenge_bond_rate, pending_timeout_duration,
    pending_collateral_rate, pending_volume_caps, uioli_threshold,
    tranche_split, npv_discount_rate, cross_epoch_smoothing_limit,
    bootstrap_sunset_conditions, treasury_allocation_budgets

TIER 3 — OPERATIONAL (automated or admin-adjusted):
    epoch_boundary_jitter_seed, deterministic_sort_seeds,
    monitoring_alert_thresholds, log_verbosity_levels,
    CRDT_replication_intervals, EABS_batch_size_limits
```

## 11.4 Governance Voting

### 11.4.1 Vote Weight Calculation

```
FUNCTION compute_governance_weight(entity: EntityID) -> Decimal(18,8):
    staked = get_staked_aic(entity)
    cap_score = get_capability_score(entity)      // 1.0 to 3.0

    // Governance uses SQRT of capability_score (not full multiplier)
    // Reduces reputation influence on governance decisions
    governance_multiplier = SQRT(cap_score)       // Range: 1.0 to 1.73

    RETURN staked * governance_multiplier

Rationale: In settlement, the full capability multiplier (up to 3.0x) rewards
capable agents. In governance, a reduced multiplier (SQRT, up to 1.73x) ensures
economic stake remains the dominant factor, preventing governance capture by
high-reputation low-stake entities.
```

### 11.4.2 Voting Protocol

```
PROTOCOL GovernanceVote:
    FOR ParameterChange (Tier 2):
        quorum:           30% of total governance weight
        threshold:        50% + 1 (simple majority)
        voting_period:    3 epochs
        execution_delay:  1 epoch
        cooldown:         parameter locked for 10 epochs after change

    FOR TreasuryAllocation:
        quorum:           30%
        threshold:        50% + 1
        voting_period:    3 epochs
        execution_delay:  1 epoch
        per_allocation:   max 5% of treasury balance

    FOR ConstitutionalAmendment:
        (See Section 11.2.1 — supermajority process)

    FOR EmergencyAction:
        quorum:           40%
        threshold:        60%
        voting_period:    1 epoch (expedited)
        execution_delay:  0 (immediate)
        scope:            predefined emergency actions only:
            - Pause EABS settlement
            - Activate emergency capacity
            - Freeze entity (suspected active attack)
            - Rollback last epoch (conservation violation)
        auto_expiry:      5 epochs unless renewed
```

## 11.5 Parameter Adjustment Procedures

For each governance-tunable parameter, the following analysis template is maintained:

```
STRUCTURE ParameterSensitivity:
    parameter:           String
    current_value:       Decimal
    sensitivity_at_2x:   String       // What breaks if doubled
    sensitivity_at_05x:  String       // What breaks if halved
    safe_range:          (Decimal, Decimal)
    break_points:        (Decimal, Decimal)   // Where system fails
    adjustment_rate:     Decimal      // Max change per governance cycle
```

Key sensitivities are documented in Section 14.4 (Parameter Sensitivity Analysis).

---

# Section 12: Integration Specifications

DSF integrates with all five other layers of the Atrahasis architecture. This section specifies exact data flows, frequencies, consistency guarantees, and failure handling for each integration.

## 12.1 C3 (Tidal Noosphere) Integration

C3 is DSF's substrate. DSF runs within C3's locus/parcel architecture, uses C3's CRDT infrastructure for the read-path, and relies on C3's Sentinel Graph for Sybil detection.

### 12.1.1 AIC Ledger Replication

```
Integration: DSF --> C3 (ledger state replicated across loci)

Data Flow:
    Source:      EABS settled state (per-epoch)
    Transport:   C3 PN-Counter CRDT replication
    Destination: Each locus maintains a local read-replica

    STRUCTURE AICLedgerReplica:
        entity_balances:    Map<EntityID, Decimal(18,8)>
        pc_balances:        Map<EntityID, Decimal(18,8)>
        cs_allocations:     Map<EntityID, Map<ResourceType, uint64>>
        last_settled_epoch: EpochID
        optimistic_deltas:  Vec<OptimisticDelta>

Consistency:
    Settled state: STRONG — identical across all loci after EABS propagation
                   (bounded by reliable broadcast latency, typically <5 seconds)
    Optimistic deltas: EVENTUAL — CRDT convergence, may differ during epoch

Frequency:
    Settled state: once per epoch (at epoch boundary)
    Optimistic deltas: continuous (CRDT merge on every inter-locus sync)

Failure Handling:
    IF locus fails to receive settled state for epoch E:
        - Operates on epoch E-1 state + optimistic deltas
        - Marks itself STALE for settlement purposes
        - STALE loci cannot process write-path operations
        - Resynchronization: request missed epochs from any non-stale locus
        - Maximum staleness: 3 epochs. After 3, locus enters DEGRADED mode
          (read-only, no new task assignments)
        - Recovery time: O(missed_epochs * settlement_time) — typically seconds
```

### 12.1.2 Per-Locus EABS with Cross-Locus Reconciliation

```
Integration: Bidirectional (C3 provides substrate, DSF provides settlement)

Architecture:
    Each locus runs its own EABS instance for intra-locus operations.
    Cross-locus operations use a reconciliation layer.

    STRUCTURE PerLocusEABS:
        locus_id:           LocusID
        local_batch:        EpochBatch
        local_state:        LocusSettlementState
        cross_locus_ops:    Vec<CrossLocusOp>

Protocol:
    Phase 1 (0%-60% of boundary window): Local Settlement
        Each locus EABS processes its local epoch batch.
        Cross-locus operations DEFERRED to Phase 2.
        Per-locus conservation check.

    Phase 2 (60%-75%): Cross-Locus Collection
        Each locus submits cross-locus operations to reconciliation layer.
        Reconciliation layer collects and canonically sorts all cross-locus ops.

    Phase 3 (75%-95%): Cross-Locus Settlement
        Unified cross-locus batch processed deterministically.
        Each locus receives its share of results.
        Global conservation check.

    Phase 4 (95%-100%): Merge
        Each locus merges local + cross-locus results.
        CRDT read-path updated with new settled state.

Failure Handling:
    IF locus misses Phase 2 deadline:
        Cross-locus ops deferred to next epoch.
        Other loci proceed without them.
    IF cross-locus reconciliation fails conservation:
        All cross-locus ops rolled back for this epoch.
        Per-locus settlements still apply (passed local conservation).
        Rolled-back ops retried next epoch with additional logging.
```

### 12.1.3 CSO Rebalancing on Tidal Phase Transitions

```
Integration: C3 --> DSF (C3 triggers, DSF responds)

Trigger: C3 tidal phase transition (any locus changing phase)

Data Flow:
    C3 EMITS: TidalPhaseTransition {
        locus_id, old_phase, new_phase, epoch, affected_parcels
    }

    DSF PROCESSES:
        1. Identify affected CSOs in the transitioning locus
        2. Recompute capacity allocations for new tidal phase
        3. Release over-allocated capacity to next tranche
        4. Queue under-allocated entities for priority rebidding

    Tidal Phase Capacity Rules:
        HIGH_TIDE: Reserve 10% CS for spot allocation (burst demand)
        LOW_TIDE:  UIOLI threshold relaxed to 50% (lower expected demand)
        NEAP:      No adjustment; standard tranche schedule applies

Frequency: Per tidal transition (irregular, driven by C3)
Consistency: EABS-settled (rebalancing in next epoch batch)
```

### 12.1.4 Sentinel Graph for Sybil Detection

```
Integration: C3 --> DSF (C3 provides identity clustering, DSF consumes)

Data Flow:
    C3 EMITS: SentinelClusterUpdate {
        cluster_id, member_entities, confidence, evidence_type, epoch
    }

    DSF CONSUMES:
        1. Update cluster position limits (POS-2)
        2. Adjust capability_score diversity checks
        3. If confidence >= 0.90: trigger collusion slashing (Section 10.6)

API:
    DSF --> C3: query_cluster(entity_id) -> Option<SentinelClusterID>
    DSF --> C3: get_cluster_members(cluster_id) -> Vec<EntityID>
    C3 --> DSF: push_cluster_update(SentinelClusterUpdate)

Frequency: Asynchronous (C3 pushes as clusters detected)
Consistency: EVENTUAL for queries, EABS for enforcement actions

Failure Handling:
    IF Sentinel Graph unavailable:
        - Continue with last known cluster data
        - New entities treated as singletons
        - Position limits enforced per-entity only (POS-1, not POS-2)
        - EMIT SentinelUnavailable governance alert
```

## 12.2 C5 (PCVM) Integration

### 12.2.1 Verification Rewards

```
Integration: DSF --> C5 verifiers (DSF distributes rewards)

Data Flow:
    C5 EMITS per-epoch: VerificationReport {
        verifier_id, claims_verified, accuracy_rate,
        claim_classes, vtds_completed, epoch
    }

    DSF COMPUTES verification rewards (40% of settlement pool).

Frequency: V-class settlement (every N=5 epochs)
Consistency: EABS-settled

Failure Handling:
    IF C5 fails to deliver reports:
        - Verification rewards DEFERRED (held in treasury)
        - Maximum deferral: 3 epochs
        - After 3 epochs without reports: redistributed to other streams
```

**9-Class Difficulty Weights (C9 canonical):**

```
CONST CLAIM_CLASS_DIFFICULTY_WEIGHTS = {
    D: 1.0,    // Deterministic — verifiable by recomputation
    C: 1.3,    // Compliance — rule matching, slightly complex
    P: 1.5,    // Process — trace checking
    E: 1.5,    // Empirical — requires observational evidence
    K: 1.8,    // Knowledge Consolidation — cross-domain integration
    S: 2.0,    // Statistical — requires sample accumulation
    R: 2.0,    // Reasoning — logical verification
    H: 2.5,    // Heuristic — expert judgment under uncertainty
    N: 3.0,    // Normative — value judgments and policy evaluation
}
```

Verification reward computation:
```
FOR each report:
    IF accuracy_rate < 0.70: quality_score = 0 (below threshold)
    ELSE:
        difficulty_weight = sum(
            CLAIM_CLASS_DIFFICULTY_WEIGHTS[cc]
            for cc in report.claim_classes
        )
        quality_score = accuracy_rate * difficulty_weight * vtds_completed

Distribute pool proportionally by quality_score.
```

### 12.2.2 Credibility to Capability Score Mapping

```
Integration: C5 --> DSF (credibility feeds capability_score)

Data Flow:
    C5 MAINTAINS: CredibilityScore {
        entity_id, overall_credibility (0.0-1.0),
        by_claim_class, sample_size, last_updated_epoch
    }

    DSF MAPS to raw_score.verification_track_record:
        FUNCTION credibility_to_track_record(cred) -> Decimal:
            IF cred.sample_size < 20: RETURN 0.0    // Cold start
            classes_with_data = count(cred.by_claim_class)
            diversity_factor = MIN(classes_with_data / 3.0, 1.0)
            RETURN cred.overall_credibility * diversity_factor

API:
    DSF --> C5: get_credibility(entity_id) -> CredibilityScore
    C5 --> DSF: push_credibility_update(entity_id, CredibilityScore)

Frequency: Per V-class settlement period
Consistency: CRDT for queries, EABS for capability recalculation

Failure Handling:
    IF credibility data unavailable:
        - Track record component frozen at last known value
        - For new computation: use 0.0 (conservative)
        - effective_stake computed with capability_score = 1.0 (baseline)
```

### 12.2.3 PC Identity-Binding via PCVM Attestations

```
Integration: C5 --> DSF (attestations prove work performed by earner)

Purpose: Prevents PC delegation/farming (Attacks 4 and 6)

Data Flow:
    When entity performs PC-earning action, C5 generates:
        VerificationAttestation {
            attestation_id, performer, action_type,
            action_hash, timestamp, pcvm_signature
        }

    DSF VALIDATES before crediting PCs:
        REQUIRE attestation.performer == earning_entity
        REQUIRE attestation.action_hash == HASH(action_content)
        REQUIRE VERIFY(attestation.pcvm_signature, PCVM_PUBLIC_KEY)
        REQUIRE current_epoch - attestation.epoch <= 1    // Freshness

Frequency: Per PC-earning action (continuous)
Consistency: Deterministic (signature verification)

Failure Handling:
    IF PCVM attestation service unavailable:
        - PC earning SUSPENDED (no PCs credited without attestation)
        - Existing PC balances continue to decay (10%/epoch)
        - EMIT PCVMUnavailable alert
        - No backfill on recovery (prevents retroactive gaming)
```

### 12.2.4 Claim Class to Settlement Type Mapping

> **Attribution Note:** The canonical claim-class-to-settlement-type mapping is defined in C9 Section SS7.3. This table is a local summary; defer to C9 SS7.3 for any discrepancies.

```
D (Deterministic)       --> B-class fast     (verifiable by recomputation)
C (Compliance)          --> B-class fast     (rule matching — fast)
P (Process)             --> B-class fast     (trace checking — fast)
E (Empirical)           --> V-class standard (requires observation over time)
K (Knowledge Consol.)   --> V-class standard (cross-domain, needs expert eval)
S (Statistical)         --> V-class standard (requires sample accumulation)
R (Reasoning)           --> V-class standard (logical verification)
H (Heuristic)           --> V-class standard (requires expert review)
N (Normative)           --> G-class slow     (involves value judgments)
```

## 12.3 C6 (EMA) Integration

EMA provides knowledge metabolism. DSF rewards knowledge contributions and integrates with SHREC regulation.

### 12.3.1 Knowledge Contribution Rewards

```
Integration: C6 --> DSF (C6 reports, DSF settles rewards)

Data Flow:
    C6 EMITS per-epoch: KnowledgeContributionReport {
        contributor_id, quanta_produced, quanta_quality,
        metabolic_efficiency, task_class, epoch
    }

    DSF COMPUTES (via scheduling compliance stream, 40%):
        contribution_score = quanta_produced * quanta_quality * metabolic_efficiency
        Distribute compliance pool proportionally.
        Knowledge tasks compete with other scheduled tasks for pool share.

Frequency: B-class settlement (per-epoch)

Failure Handling:
    IF C6 fails to deliver reports:
        - Knowledge contributions receive no reward for that epoch
        - Compliance pool distributed among non-knowledge tasks
        - No backfill (prevents gaming via delayed reporting)
```

### 12.3.2 Metabolic Efficiency Informing Capacity Market

```
Integration: C6 --> DSF capacity market (informational only)

Data Flow:
    C6 PUBLISHES: MetabolicEfficiencyReport {
        resource_type, avg_efficiency, marginal_cost, demand_forecast, epoch
    }

    DSF USES (non-binding):
        - demand_forecast informs CPLR capacity offering
        - marginal_cost informs reserve pricing governance proposals
        - avg_efficiency included in treasury reporting

Consistency: INFORMATIONAL ONLY — errors cannot cause conservation violations
```

### 12.3.3 SHREC Budget Allocation

```
Integration: Bidirectional (C6 requests, DSF enforces limits)

SHREC Components: S(tability), H(omeostasis), R(esilience), E(volution), C(omplexity)

Data Flow:
    C6 SUBMITS: SHRECBudgetRequest {
        locus_id, s/h/r/e/c budgets, total_request, justification
    }

    DSF VALIDATES:
        max_allocation = MIN(total_request, locus_sb * 0.30)
        IF max_allocation < total_request:
            Scale all SHREC components proportionally

Frequency: Per-epoch (B-class)
Consistency: EABS-settled
```

## 12.4 C7 (RIF) Integration

### 12.4.1 Operation Class Mapping

```
M (Merge/Convergence)     --> B-class fast
B (Bounded Local Commit)  --> B-class fast
X (Exclusive)             --> B-class fast (V-class if disputed)
V (Verification)          --> V-class standard
G (Governance)            --> G-class slow
```

### 12.4.2 Intent Resource Bounds as Budget Ceilings

```
Integration: C7 --> DSF (RIF provides bounds, DSF enforces budget)

Data Flow:
    C7 SUBMITS: IntentSubmission {
        intent_id, sponsor_id,
        resource_bounds: { max_compute, max_storage, max_bandwidth,
                          max_aic_cost, max_duration },
        decomposition: Vec<TaskID>,
        priority: PriorityClass
    }

    DSF VALIDATES:
        1. Check SB availability (CRDT read-path, optimistic)
        2. Check minimum bounds per task class (trailing 10-epoch median * 0.7)
        3. Reserve budget (optimistic; actual deduction at EABS)

Consistency:
    Validation: OPTIMISTIC (may approve intents later rejected at settlement)
    Deduction: EABS-settled (deterministic, conservation-preserving)

Failure Handling:
    IF optimistic validation approves but EABS rejects:
        - Intent CANCELLED, sub-tasks ABORTED
        - Workers compensated minimum_bounds for completed work
        - Sponsor receives scheduling violation if repeated (>2 in 10 epochs)
```

### 12.4.3 Stake Availability Check

```
Integration: C7 --> DSF (RIF queries, DSF responds)

API:
    FUNCTION check_stake_availability(entity_id) -> StakeAvailability:
        RETURN {
            staked_aic:        CRDT read (optimistic),
            capability_score:  CRDT read (optimistic),
            effective_stake:   computed,
            available_sb:      CRDT read (optimistic),
            available_cs:      CRDT read (optimistic),
            pc_balance:        CRDT read (optimistic),
            last_settled:      last EABS epoch,
            staleness_warning: current_epoch > last_settled + 1,
        }

Consistency: OPTIMISTIC — RIF should treat all values as estimates.
Frequency: On-demand (per intent submission)

Failure Handling:
    IF DSF read-path unavailable:
        RIF queues intent submissions (max 100/entity, 1000 global)
        Overflow: oldest intents dropped with RESOURCE_UNAVAILABLE
```

### 12.4.4 Resource Return Credits

```
Integration: C7 --> DSF (RIF reports completion, DSF processes returns)

Data Flow:
    C7 SUBMITS: TaskCompletionReport {
        task_id, intent_id, sponsor_id, worker_id,
        resource_bounds, actual_usage, completion_quality, epoch
    }

    DSF PROCESSES in EABS:
        compute_unused = bounds.compute - actual.compute
        aic_unused = bounds.max_aic - actual.aic_cost
        IF aic_unused > 0: Credit(sponsor, aic_unused)
        IF compute_unused > 0: ReleaseCapacity(type, compute_unused)

        worker_reward = compute_worker_reward(
            actual.aic_cost, completion_quality, bounds.max_aic
        )
        Credit(worker, worker_reward)

Frequency: Per task completion (B-class EABS)
Consistency: EABS-settled
```

### 12.4.5 Intent Lifecycle to Settlement Lifecycle Mapping

```
RIF State            DSF Settlement Action
-----------          ----------------------
SUBMITTED            Budget reserved (optimistic, read-path)
DECOMPOSED           Sub-task budgets validated against minimum bounds
EXECUTING            CS consumed per-epoch; PC consumed for rate-limited ops
PARTIALLY_COMPLETE   Completed sub-task rewards (B-class); resource returns
COMPLETED            Final batch: worker rewards, sponsor refund, V-class deferred
FAILED               Emergency: workers paid for completed work, sponsor refunded
TIMED_OUT            Timeout: like FAILED + additional sponsor penalty if chronic
```

## 12.5 Native Communication Integration

The Alternative C sovereign communication stack defines the canonical vocabulary and carriage for inter-agent communication. DSF expresses all economic messages through native sovereign message classes and `AXIP-v1` contracts.

### 12.5.1 Settlement Message Vocabulary

DSF defines the following native settlement message schemas:

```
Schema: "dsf.settlement.credit"
    Properties: recipient, amount, currency (AIC/PC/CS), stream, epoch,
                settlement_class (B/V/G), justification (evidence hash)

Schema: "dsf.settlement.slash"
    Properties: violator, amount, violation_type, offense_number,
                evidence (array of hashes), reporter, epoch

Schema: "dsf.market.bid"
    Properties: bidder, resource_type, quantity, max_price,
                priority_class (FIRM/FLEXIBLE), commitment_hash, epoch

Schema: "dsf.governance.vote"
    Properties: voter, proposal_id, vote (FOR/AGAINST/ABSTAIN),
                weight, epoch, signature

Schema: "dsf.conservation.report"
    Properties: epoch, resource_type, total_supply, total_allocated,
                total_pending, total_spent, conservation_holds (bool), delta
```

### 12.5.2 Economic Claim Types for PCVM Verification

```
Claim: "dsf.claim.conservation"
    Class: D (Deterministic)
    Verification: Re-run EABS on epoch batch, check invariant

Claim: "dsf.claim.clearing_price"
    Class: D (Deterministic)
    Verification: Re-run auction clearing on bids/offers

Claim: "dsf.claim.capability_score"
    Class: E (Empirical)
    Verification: Recompute from credibility, reputation, track record

Claim: "dsf.claim.slashing_correctness"
    Class: D (Deterministic)
    Verification: Re-process violation through slashing function

Claim: "dsf.claim.market_fairness"
    Class: S (Statistical)
    Verification: Statistical tests on bid distributions, HHI calculation
```

---

# Section 13: Security Analysis

## 13.1 Threat Model

```
FAULT MODEL:
    Byzantine fault tolerance with honest majority assumption.
    N >= 3f + 1 nodes. f Byzantine nodes may crash, send conflicting
    messages, collude, or delay messages.
    Network: partially synchronous (messages delivered within bounded
    time Delta after Global Stabilization Time).

ADVERSARY LEVELS:

    Level 1 — Rational Agent (most common):
        Follows protocol when profitable, deviates when more profitable.
        Perfect information about public protocol state.
        Cannot forge signatures or break hash functions.
        Budget-constrained (finite AIC, PC, CS).

    Level 2 — Sybil Operator:
        Controls multiple identities.
        May operate below Sentinel Graph detection threshold.
        Budget-constrained but distributed across identities.

    Level 3 — Coordinated Cartel:
        Multiple independent entities colluding.
        Up to 30% of total effective stake.
        Cannot reach governance supermajority (67%).
        Inter-cartel communication unobservable.

    Level 4 — Infrastructure Attacker:
        Controls minority of infrastructure providers.
        May withhold capacity, delay messages, provide incorrect results.
        Cannot compromise EABS (deterministic, verifiable).

ASSUMPTIONS:
    A1: Honest majority (>2/3) participates in Reliable Broadcast
    A2: Cryptographic primitives (SHA-256, Ed25519) are secure
    A3: Network achieves partial synchrony
    A4: >= 5 independent capacity providers per resource type (post-bootstrap)
    A5: Governance participants act in long-term self-interest
```

## 13.2 Adversarial Findings and Architectural Resolutions

### Finding 1: Phantom Balance Attack (FATAL --> RESOLVED)

**Attack:** Double-spending AIC across network partitions via CRDT merge.
**Resolution:** Hybrid Deterministic Ledger. All state-mutating operations through EABS. Transfers finalized only at epoch boundary. Double-spend impossible because operations require Reliable Broadcast agreement.
**Residual risk:** If Reliable Broadcast fails (>f Byzantine), settlement stalls but does not produce inconsistent state. Conservative design: no settlement without agreement.

### Finding 2: Reputation Laundering (CRITICAL --> MITIGATED)

**Attack:** Sybil cluster farms capability_scores for 10x+ stake amplification.
**Resolution:** Hard cap at 3.0x. Logarithmic scaling. 3+ independent sponsor requirement. Track record weighted by economic value. Random claim class assignment. Sentinel Graph clustering.
**Residual risk:** Sophisticated Sybils evading Sentinel Graph still limited to 3x amplification.

### Finding 3: Settlement Sandwiching (CRITICAL --> MITIGATED)

**Attack:** Timing transactions around epoch boundaries to manipulate settlement windows.
**Resolution:** Epoch jitter (+-10%). Commit-reveal for completion reports. Cross-epoch smoothing (25% max deviation). Sliding window evaluation. NPV normalization.
**Residual risk:** Marginal timing advantage from jitter prediction, mitigated by network entropy in seed.

### Finding 4: PC Decay Arbitrage (HIGH --> MITIGATED)

**Attack:** Timing spam around PC refresh to maximize resource consumption.
**Resolution:** Quality-gated earning. Sublinear curve (sqrt). Congestion pricing. Identity-binding. Balance cap (10x epoch rate).
**Residual risk:** Lenient quality gates could allow low-quality earning. Governance monitors and adjusts.

### Finding 5: Thin Market Squeeze (HIGH --> MITIGATED)

**Attack:** Cornering capacity market during bootstrap.
**Resolution:** 15% position limits. Cluster limits (POS-2). UIOLI at 70%. Progressive 60/20/20 tranches. Reserve pricing. Bootstrap CPLR. HHI monitoring with auto position-limit reduction at HHI>0.40.
**Residual risk:** Extended low-provider periods drain treasury via CPLR. Mitigated by CPLR pricing above floor.

### Finding 6: Cross-Budget Arbitrage (HIGH --> ACCEPTED WITH FRICTION)

**Attack:** Implicit SB-PC-CS conversion pathways erode budget separation.
**Resolution:** Sufficient friction model. PC identity-binding. CS position limits. Cross-budget flow monitoring. Exchange rate stabilization triggers governance review.
**Residual risk:** This finding is explicitly ACCEPTED. Three-budget model provides functional separation, not absolute isolation. If friction proves insufficient, governance may reduce to two budgets.

### Finding 7: Slashing Ordering Attack (CRITICAL --> RESOLVED)

**Attack:** Non-deterministic violation ordering produces different penalties on different replicas.
**Resolution:** ALL slashing through EABS. Canonical sort: (type, timestamp_hash, violator_id). Monotonic violation counters. Identical ordering on all honest nodes.
**Residual risk:** None. Fully eliminated by EABS deterministic ordering.

### Finding 8: RIF Draining (MEDIUM --> MITIGATED)

**Attack:** Artificially low resource_bounds exploit workers.
**Resolution:** Minimum bounds floor (70% of trailing median). Worker inspection window (10% effort). Sponsor reputation tracking. Systematic under-budgeting triggers governance review.
**Residual risk:** Novel task classes without historical data have no reliable floor. Worker inspection window provides partial protection.

### Finding 9: Limbo Attack (HIGH --> MITIGATED)

**Attack:** Creating pending states that never resolve to lock resources.
**Resolution:** 3-epoch mandatory timeout. 5% collateral. 2% timeout fee (burned). 10% per-entity cap. 25% global cap.
**Residual risk:** Multiple independent attackers could lock up to 25%, each at 5% collateral cost. Economically irrational at scale.

### Finding 10: Speed Class Gaming (MEDIUM --> MITIGATED)

**Attack:** Structuring activity for faster settlement than competitors.
**Resolution:** NPV normalization (B-class x0.98, V-class x1.02). Challenge rate limit (3/entity/epoch). Challenge bond (5%). Per-participant ratio tracking.
**Residual risk:** Approximate NPV. Epoch discount rate must be calibrated to actual capital opportunity cost.

## 13.3 Security Invariants

```
SEC-1 (Conservation):
    No AIC created/destroyed outside treasury minting and slashing burns.
    Enforcement: EABS conservation check every epoch.
    Detection: Automatic batch rejection on violation.

SEC-2 (Determinism):
    Same epoch batch --> same settlement output on every honest node.
    Enforcement: Canonical ordering + deterministic settlement function.
    Detection: Nodes compare settlement hashes after each epoch.

SEC-3 (Stake Integrity):
    Effective stake accurately reflects economic commitment and capability.
    Enforcement: Cap 3.0, logarithmic scaling, diversity requirements.
    Detection: Sentinel Graph + anomaly detection.

SEC-4 (Market Integrity):
    Clearing prices reflect genuine supply and demand.
    Enforcement: Position limits, withholding/cornering detection, reserve pricing.
    Detection: HHI monitoring, bid correlation analysis.

SEC-5 (Governance Integrity):
    Constitutional protections cannot be circumvented by normal governance.
    Enforcement: Supermajority + cooling periods + rate limits.
    Detection: Constitutional compliance check on every proposal.

SEC-6 (Budget Separation):
    Three budget types provide functionally distinct instruments.
    Enforcement: Identity-binding, position limits, cross-budget friction.
    Detection: Flow monitoring, exchange rate tracking.
```

## 13.4 Attack Surface Enumeration

```
Surface                        Attack Vectors                        Mitigations
------------------------------ ------------------------------------- ----------------------------------
1. EABS batch submission       Invalid ops, oversized batches,       Validation, batch limits,
                               timing manipulation                   epoch jitter
2. Capacity market bids        Manipulation, withholding,            Deposits, withholding detection,
                               commitment attacks                    reserve pricing
3. CRDT read-path              Stale data exploitation,              Staleness warnings,
                               optimistic balance attacks            settle-then-commit
4. Violation reporting         False accusations, evidence           Evidence requirements,
                               fabrication, selective reporting      false report penalties
5. Governance proposals        Spam, vote buying, parameter          Bonds, constitutional
                               manipulation                          protections, weight limits
6. PC earning actions          Quality gaming, delegation,           Identity-binding, sublinear,
                               farming                               quality gates
7. Cross-locus operations      Isolation, reconciliation delay,      Timeouts, per-locus checks,
                               cross-locus double-spend              deferred retry
8. Sentinel Graph inputs       Behavior mimicry, anti-clustering     Multiple evidence types,
                                                                     confidence thresholds
9. PCVM attestations           Forgery, service denial               Signature verification,
                                                                     PC suspension on unavailability
10. Treasury operations        Drain, misallocation,                 Per-allocation caps,
                               emergency abuse                       reserve floor, auto-expiry
```

## 13.5 Defense-in-Depth Strategy

DSF employs six defense layers. No single mechanism is the sole protection against any attack class. Each identified attack requires compromising at least two layers simultaneously.

```
Layer 1 — Economic Deterrence:
    Graduated slashing. Stake requirements. Reporter rewards.
    Burn fraction ensures slashing is net-destructive.

Layer 2 — Protocol Enforcement:
    EABS determinism. Conservation checks. Position limits.
    Timeout mechanisms. Minimum bounds.

Layer 3 — Cryptographic Verification:
    Identity-binding attestations. Sealed-bid commitments.
    Hash-based canonical ordering.

Layer 4 — Statistical Detection:
    Sentinel Graph clustering. HHI monitoring.
    Cross-budget flow analysis. Bid correlation analysis.

Layer 5 — Governance Response:
    Anomaly alerts. Parameter adjustment.
    Emergency actions. Constitutional protections.

Layer 6 — Architectural Isolation:
    Read/write path separation. Per-locus EABS.
    Three-budget separation. Multi-rate settlement.
```

---

# Section 14: Scalability and Deployment

## 14.1 Scale Targets

```
PRIMARY (Design scope):
    1K-10K agents, 10-50 loci, 6 resource types
    Epoch: 60 seconds (1 SETTLEMENT_TICK). Batch: 1K-50K ops/epoch. Providers: 10-100.

SECONDARY (Engineering optimization):
    10K-50K agents, 50-200 loci, 12+ resource types
    Epoch: 60s (governance-adjustable within [30s, 120s]). Batch: 50K-500K ops.
    Providers: 100-500.

ASPIRATIONAL (Requires architectural evolution):
    100K+ agents, 200+ loci
    Epoch: dynamic per-locus. EABS: sharded. Sub-markets.
```

## 14.2 Bottleneck Analysis

```
Bottleneck                  At Primary        At Secondary      At Aspirational
--------------------------  ----------------  ----------------  -----------------
Reliable Broadcast msgs     ~1K (trivial)     ~10K (gossip)     ~100K (hierarchical)
EABS batch processing       <1s (50K ops)     <5s (500K ops)    sharded
Capacity market clearing    <1s (1K bids)     <5s (50K bids)    parallelized per-type
CRDT replication            ~140 KB/s         ~1.4 MB/s         hierarchical
Sentinel Graph              O(E*dE)           incremental       federated
```

## 14.3 Deployment Phases

```
Phase 1 — BOOTSTRAP (epochs 0 to sunset trigger):
    Scale: <100 agents, <5 loci
    Settlement: single EABS, no cross-locus reconciliation
    Market: CPLR provides majority of capacity
    Governance: founding parameters (Tier 3 only)
    Capability scores: all entities start at 1.0
    Entry: system deployment
    Exit: MVS holds for 3 consecutive epochs

Phase 2 — GROWTH (post-bootstrap to steady-state trigger):
    Scale: 100-1K agents, 5-20 loci
    Settlement: per-locus EABS + cross-locus reconciliation
    Market: CPLR withdrawn, market-driven
    Governance: community active for Tier 2
    Entry: bootstrap sunset complete
    Exit: HHI<0.15 + governance>30% + zero violations/50 epochs
          + settlement latency <50% epoch

Phase 3 — STEADY STATE:
    Scale: 1K-10K agents, 20-50 loci
    Full multi-rate settlement operational
    Market: competitive, self-sustaining
    Governance: mature, constitutional amendments possible
    Duration: indefinite (primary mode)

Phase 4 — SCALE (aspirational):
    Scale: 10K-100K+ agents, 50+ loci
    Sharded EABS, hierarchical broadcast
    Sub-markets by specialization
    Federated governance
    Requires: new DESIGN cycle
```

## 14.4 Parameter Sensitivity Analysis

```
Parameter                  Current   Safe Range       Break Points
-------------------------  --------  ---------------  ---------------------------
epoch_duration             60s       [30s, 120s]      <15s RBC fail; >300s stale
pc_decay_rate              10%       [3%, 25%]        <1% hoarding; >40% unusable
cs_position_limit          15%       [5%, 25%]        <3% fragmented; >33% monopoly
capability_score_cap       3.0       [1.5, 5.0]       <1.2 irrelevant; >8.0 gaming
pending_timeout            3 epoch   [1, 10]          <1 too fast; >20 lockup
pending_collateral_rate    5%        [2%, 15%]        <1% cheap grief; >25% unusable
per_entity_pending_cap     10%       [5%, 20%]        <2% too tight; >30% lockup
global_pending_cap         25%       [10%, 40%]       <5% too tight; >50% systemic
challenge_bond_rate        5%        [2%, 15%]        <1% spam; >25% chilling
npv_discount_rate          0.2%      [0.1%, 0.5%]     <0.05% no effect; >1% distortion
smoothing_limit            25%       [10%, 50%]       <5% rigid; >75% no protection
slash_1st_offense          1%        [0.5%, 5%]       <0.1% no deterrence; >10% harsh
tranche_split              60/20/20  [50-80/10-25]    30/35/35 illiquid; 95/3/2 no flex
```

## 14.5 Migration Protocol

```
BOOTSTRAP --> GROWTH:
    Trigger: MVS (>=5 providers per resource type) for 3 consecutive epochs
    Action: CPLR withdrawal (5-epoch linear schedule)
    Fallback: pause withdrawal if MVS fails, revert to BOOTSTRAP

GROWTH --> STEADY STATE:
    Trigger (ALL for 10 consecutive epochs):
        HHI < 0.15 all resource types
        Governance participation > 30%
        Zero conservation violations trailing 50 epochs
        Settlement latency < 50% epoch duration
    Action: full governance handover (Tier 2 unlocked)
    Fallback: GovernanceAlert but no revert (steady-state is sticky)

STEADY STATE --> SCALE:
    Trigger: EABS processing > 70% of epoch for 5 epochs
             OR agent count > 10K + cross-locus > 30% of batch
    Action: initiate sharded EABS (new design cycle)

Parameter Migration:
    BOOTSTRAP:     Tier 2 locked at conservative defaults
    GROWTH:        Tier 2 unlocked; first change requires 60% supermajority;
                   max 1 change per 5 epochs
    STEADY STATE:  Full governance control of Tier 2
```

---

# Section 15: Conclusion and Future Work

## 15.1 Summary of Contributions

The Deterministic Settlement Fabric v2.0 provides a complete economic settlement layer for the Atrahasis planetary-scale distributed AI agent system. Its primary contributions are:

1. **Hybrid Deterministic Ledger (HDL).** The first architecture to combine CRDT availability guarantees (partition-tolerant reads) with batch settlement consistency guarantees (conservation-preserving writes) in a single ledger abstraction. CRDT read-path ensures agents always have access to balance information; EABS write-path ensures that all state mutations are deterministic, conservation-preserving, and consistently ordered.

2. **Epoch-Anchored Batch Settlement (EABS).** A lightweight settlement mechanism that achieves determinism not by eliminating coordination but by ensuring all honest nodes process the same inputs in the same canonical order. Uses Reliable Broadcast (not full BFT consensus) to achieve agreement on epoch batch contents with O(n^2) message complexity.

3. **Three-Budget Economic Model.** Functional separation of payment (AIC), spam control (PC), and resource allocation (CS) with honest acknowledgment that perfect isolation is economically impossible, replaced by calibrated friction mechanisms and budget collapse monitoring.

4. **Multi-Rate Settlement with NPV Normalization.** Three settlement speeds matched to operation urgency, with timing normalization to eliminate compound timing arbitrage. B-class x0.98 discount, V/G-class (1+r)^delay premium.

5. **Capability-Weighted Stake with Sybil Resistance.** Logarithmic capability scoring with hard cap at 3.0x, diversity requirements, and random claim class assignment across all 9 canonical classes (D/C/P/E/K/S/R/H/N).

6. **Capacity Market with Thin-Market Protections.** Sealed-bid uniform-price auction with progressive 60/20/20 tranche release, position limits, and bootstrap CPLR.

7. **Formal Conservation Framework.** Rigorous proof that every operation type preserves conservation, with unified CONS-1 formula including collateral_held, CONS-1a pending balance invariant, runtime enforcement via post-batch invariant checking, and automated recovery protocol.

8. **Graduated Slashing with Deterministic Ordering.** Five-level penalty schedule with 50/30/20 distribution (burn/treasury/reporter) processed through EABS canonical ordering, fully resolving the slashing ordering attack.

## 15.2 Open Research Questions

1. **Three-Budget Equilibrium Dynamics.** While the sufficient-friction model is architecturally sound, long-term equilibrium behavior under diverse demand scenarios requires Monte Carlo simulation. The question of whether cross-budget friction converges to stable implicit exchange rates or oscillates remains open.

2. **EABS Formal Verification.** The settlement function should be formally verified using TLA+ or Dafny for conservation, determinism, and termination. The proof sketches in this document provide the specification; mechanized verification would provide the guarantee. See Appendix K for roadmap.

3. **Epoch Duration Optimization.** The trade-off between settlement latency and coordination overhead depends on workload characteristics. Adaptive epoch duration (per-locus) is an aspirational feature requiring further analysis.

4. **Sentinel Graph Effectiveness.** DSF's Sybil resistance depends on C3's Sentinel Graph detection quality. The interaction between capability score farming strategies and detection algorithms needs adversarial game-theoretic analysis.

5. **Sharded EABS.** Scaling beyond 10K agents requires sharding the EABS settlement function across loci. Cross-shard conservation maintenance is a known hard problem (analogous to cross-shard transactions in blockchain systems).

6. **Governance Participation Incentives.** The 10% governance stream may be insufficient to motivate informed voting. Mechanism design for governance quality (not just participation) is an open question.

## 15.3 Relationship to Full Atrahasis System

DSF occupies a central position in the six-layer Atrahasis architecture:

```
C7 (RIF)     -- provides intent budgets, consumes stake availability
C8 (DSF)     -- THIS DOCUMENT: economic settlement
C3 (Tidal)   -- provides substrate, CRDT infrastructure, identity clustering
C5 (PCVM)    -- provides verification, credibility, attestations
C6 (EMA)     -- provides knowledge metrics, metabolic efficiency
Alternative C stack -- provides native message vocabulary
```

Every layer depends on DSF for economic semantics: reward distribution, penalty enforcement, resource pricing, and budget management. DSF in turn depends on every layer for data: C3 for coordination infrastructure, C5 for verification, C6 for knowledge metrics, C7 for intent budgets, and the Alternative C communication stack for canonical message format.

## 15.4 Roadmap

```
Near-term (SPECIFICATION complete):
    - Formal verification of EABS settlement function (TLA+/Dafny)
    - Monte Carlo simulation of three-budget equilibria
    - Capacity market simulation with thin-market scenarios
    - Complete native sovereign schema definitions for all economic messages

Medium-term (Implementation):
    - EABS reference implementation
    - Capacity market clearing engine
    - Graduated slashing processor
    - Conservation check runtime
    - Integration adapters for C3, the Alternative C communication stack, C5, C6, C7

Long-term (Deployment):
    - Bootstrap phase with CPLR
    - Growth phase with community governance
    - Steady-state operations
    - Scale evaluation and sharded EABS design
```

---

# Appendix A: Notation, Symbols, and Glossary

```
AIC         Atrahasis Internal Credit. Primary economic unit. Transferable.
Alternative C stack  Sovereign message, security, and semantic communication authority.
CPLR        Capacity Provider of Last Resort. Treasury-funded sovereign reserve lane with optional bounded C45 leased backstop during bootstrap.
CRDT        Conflict-free Replicated Data Type. Read-path replication substrate.
CS          Capacity Slice. Resource reservation token backed by CSO.
CSO         Capacity Slice Obligation. Provider commitment to deliver resources.
DSF         Deterministic Settlement Fabric. This system (C8).
EABS        Epoch-Anchored Batch Settlement. Write-path settlement mechanism.
ECOR        Epoch-Consistent Optimistic Reads. DSF's consistency model.
EMA         Epistemic Metabolism Architecture (C6). Knowledge processing layer.
HDL         Hybrid Deterministic Ledger. CRDT reads + EABS writes.
HHI         Herfindahl-Hirschman Index. Market concentration measure.
MVS         Minimum Viable Scale. Threshold for market self-sufficiency.
NPV         Net Present Value. Timing normalization across settlement classes.
PC          Protocol Credit. Non-transferable spam control. 10%/epoch decay.
PCVM        Proof-Carrying Verification Model (C5). Verification infrastructure.
RBC         Reliable Broadcast. Bracha's protocol for EABS agreement.
RIF         Recursive Intent Framework (C7). Orchestration layer.
SB          Sponsor Budget. AIC allocated by task sponsors.
SHREC       Stability/Homeostasis/Resilience/Evolution/Complexity (C6 regulation).
UIOLI       Use-It-Or-Lose-It. Capacity reclamation mechanism.
VTD         Verification Task Descriptor. PCVM's verification specification.
```

**Formal Notation:**

| Symbol | Definition |
|---|---|
| SETTLEMENT_TICK | 60-second atomic settlement period (C8 epoch) |
| TIDAL_EPOCH | 3600-second coordination cycle = 60 SETTLEMENT_TICKs (C3) |
| CONSOLIDATION_CYCLE | 36000-second knowledge metabolism cycle = 10 TIDAL_EPOCHs (C6) |
| n | Total number of HDL nodes |
| f | Maximum number of faulty nodes (f < n/3) |
| E | Epoch number |
| r | Epoch discount rate (default 0.002) |
| k | PC earning coefficient (default 10) |
| Sigma | Summation over all accounts |
| CONS-1 | AIC conservation invariant (with collateral_held) |
| CONS-1a | Pending balance auxiliary invariant |
| CONS-2 | CS conservation invariant (per resource type) |
| CONS-3 | PC boundedness invariant (non-conservation) |

---

# Appendix B: Parameter Reference Table

| Parameter | Default Value | Governance-Adjustable | Sensitivity |
|---|---|---|---|
| epoch_duration_ms | 60000 (60s = 1 SETTLEMENT_TICK) | Yes (Tier 2) | 2x: higher latency. 0.5x: more coordination overhead |
| epoch_jitter_range | +/- 10% | Yes | 2x: more unpredictable. 0.5x: more predictable (gaming risk) |
| pc_decay_rate | 0.10 (10%/epoch) | Yes | 2x: PCs too volatile. 0.5x: hoarding becomes viable |
| pc_earning_coefficient (k) | 10 | Yes | 2x: easier to earn. 0.5x: PC scarcity |
| pc_balance_cap_multiplier | 10x earning_rate | Yes | Higher: more burst capacity. Lower: tighter spam control |
| congestion_base_cost | 1 PC | Yes | Higher: fewer operations. Lower: less spam protection |
| cs_position_limit | 0.15 (15%) | Yes | Higher: concentration risk. Lower: market fragmentation |
| cs_utilization_threshold | 0.70 (70%) | Yes | Higher: more reclamation. Lower: more hoarding |
| capability_score_cap | 3.0 | Yes | Higher: more farming incentive. Lower: less stake amplification |
| v_class_period | 5 epochs | Yes | Higher: more accumulation. Lower: more frequent verification |
| epoch_discount_rate (r) | 0.002 (0.2%) | Yes | Higher: more NPV compensation. Lower: timing arbitrage risk |
| b_class_npv_discount | 0.98 | Yes | Higher: less B-class penalty. Lower: stronger timing disincentive |
| challenge_bond | 0.05 (5%) | Yes | Higher: deters challenges. Lower: more challenges filed |
| challenge_rate_limit | 3/entity/epoch | Yes | Higher: more challenge volume. Lower: limits dispute resolution |
| slashing_schedule | 1/5/15/50/100% | Yes | More aggressive: stronger deterrence. Less: more lenient |
| pending_timeout | 3 epochs | Yes | Higher: more capital locked. Lower: less time for resolution |
| pending_collateral | 0.05 (5%) | Yes | Higher: deters pending initiation. Lower: more pending abuse |
| pending_entity_cap | 0.10 (10% supply) | Yes | Higher: more limbo risk. Lower: limits legitimate pending |
| pending_global_cap | 0.25 (25% supply) | Yes | Higher: more systemic risk. Lower: limits throughput |
| reserve_price_floor | 80% marginal cost | Yes | Higher: more price stability. Lower: more competition |
| bootstrap_treasury_cap | 0.20 (20%) | Yes | Higher: more bootstrap capacity. Lower: less treasury exposure |
| mvs_provider_threshold | 5 per resource type | Yes | Higher: longer bootstrap. Lower: earlier sunset |
| mvs_consecutive_epochs | 3 | Yes | Higher: more conservative. Lower: faster sunset |

---

# Appendix C: Data Structure Definitions

```
// === Core Account State (CANONICAL — per F58 reconciliation) ===

AccountState {
    account_id:          AgentID
    aic_balance:         PNCounter                    // Available AIC (CRDT)
    staked_aic:          PNCounter                    // Locked collateral
    collateral_held:     PNCounter                    // Pending state collateral
    pc_balance:          PNCounter                    // Protocol Credits
    cs_allocation:       Map<ResourceType, PNCounter> // Capacity Slices per type
    pending_out:         PNCounter                    // Outbound pending
    pending_in:          PNCounter                    // Inbound pending
    capability_score:    float64                      // Cached, 1.0-3.0
    violation_count:     uint32                       // Monotonic
    last_settled_epoch:  uint64
    state_vector:        Map<NodeID, uint64>
}

// === Settlement State (EABS) ===

SettlementState {
    accounts:            Map<AgentID, AccountState>
    total_aic_supply:    uint64
    total_cs_supply:     Map<ResourceType, uint64>
    epoch_number:        uint64
    treasury_balance:    uint64
    reward_pools:        Map<SettlementStream, uint64>
    pending_registry:    Map<PendingID, PendingRecord>
    parameter_set:       ProtocolParameters
    settlement_hash:     bytes32
    unallocated_cs:      Map<ResourceType, uint64>
}

// === Operations ===

Operation {
    op_id:              bytes32
    op_type:            OperationType      // 23 types
    submitter_id:       AgentID
    timestamp:          Timestamp
    timestamp_hash:     bytes32
    epoch_number:       uint64
    payload:            OperationPayload
    signature:          bytes64            // Ed25519
    pc_cost:            uint64             // Congestion-adjusted
}

// === Pending State ===

PendingRecord {
    pending_id:         PendingID
    initiator_id:       AgentID
    counterparty_id:    AgentID
    amount:             uint64
    resource_type:      ResourceType
    collateral:         uint64
    initiated_epoch:    EpochID
    state:              PendingState
    direction:          ENUM { OUTBOUND, INBOUND }
}

// === Capacity Market ===

Bid { bidder_id, resource_type, quantity, max_price, priority_class, commitment_hash }
Offer { provider_id, resource_type, quantity, min_price, availability_proof }
TrancheClearing { tranche_id, epoch, resource_type, total_supply, clearing_price, allocations }

// === Slashing ===

ViolationReport { violator_id, violation_type, evidence, reporter_id, detection_timestamp }
Penalty { amount, resource_type, level, offense_number, violation_type, capability_impact }
SlashingAppeal { appeal_id, original_violation, appellant, bond, filed_epoch, deadline_epoch, status }

// === Governance ===

GovernanceProposal { proposal_id, proposer, proposal_type, content, bond,
                     submitted_epoch, voting_start, voting_end, status,
                     votes_for, votes_against, votes_abstain }

// === CRDT Primitives ===

PNCounter { positive: Map<NodeID, uint64>, negative: Map<NodeID, uint64> }
    value() = sum(positive) - sum(negative)
    merge(other) = max() on each component
```

---

# Appendix D: Economic Simulation Scenarios E1-E11

```
E1: NORMAL OPERATION — 100 agents, 10 providers, 50 epochs. Stable conservation.
E2: HIGH DEMAND SURGE — demand triples epoch 20, returns epoch 30. Bounded pricing.
E3: PROVIDER EXIT — 40% providers exit epoch 25. CPLR activates if MVS violated.
E4: SLASHING CASCADE — entity with 5% stake commits 5 violations in 10 epochs.
    Escalating: 1%, 5%, 15%, 50%, 100%. Slash distribution: 50% burn, 30% treasury, 20% reporter.
E5: GOVERNANCE PARAMETER CHANGE — epoch_duration from 60s to 45s.
    Proposal period (3 epochs), cooling (1 epoch), execution (1 epoch).
E6: CROSS-BUDGET ARBITRAGE — SB-->PC via self-sponsored tasks. Bounded at ~5 AIC/epoch.
E7: SYBIL CLUSTER FARMING — 10 identities, mutual boosting. Sentinel Graph detects at ~epoch 12.
E8: THIN CAPACITY MARKET — 5 providers, 6 types. CPLR activates.
E9: SUSTAINED CROSS-BUDGET ARBITRAGE — 50 epochs. Governance review at epoch 15. Unprofitable.
E10: SOPHISTICATED REPUTATION LAUNDERING — 3 clean identities, diverse sponsors.
     Cap 3.0x limits amplification. Cost exceeds value at cap.
E11: EPOCH BOUNDARY MANIPULATION — attacker controls 20% of reports.
     Commit-reveal + jitter + smoothing limit advantage to <2%.
```

---

# Appendix E: Governance Parameter Reference

```
CONSTITUTIONAL (Tier 1) — Supermajority Required:
    max_total_supply                 1,000,000 AIC
    quarterly_issuance_cap           50,000 AIC
    supermajority_threshold          0.67
    amendment_cooling_period         20 epochs
    min_appeal_window                10 epochs
    four_stream_weights              40/40/10/10
    max_parameter_change_rate        0.20

GOVERNANCE (Tier 2) — Simple Majority:
    epoch_duration                   60s       [30s, 120s]     +-25%
    pc_decay_rate                    10%       [3%, 25%]       +-5pp
    cs_position_limit                15%       [5%, 25%]       +-5pp
    capability_score_cap             3.0       [1.5, 5.0]      +-0.5
    reserve_price_floor              varies    [cost*0.5, *2]  +-20%
    challenge_bond_rate              5%        [2%, 15%]       +-3pp
    pending_timeout_duration         3 epoch   [1, 10]         +-1
    pending_collateral_rate          5%        [2%, 15%]       +-3pp
    per_entity_pending_cap           10%       [5%, 20%]       +-5pp
    global_pending_cap               25%       [10%, 40%]      +-5pp
    uioli_threshold                  70%       [50%, 90%]      +-10pp
    tranche_split                    60/20/20  [50-80/10-25]   +-10pp each
    npv_discount_rate                0.2%      [0.1%, 0.5%]    +-0.1pp
    smoothing_limit                  25%       [10%, 50%]      +-10pp
    slash_1st_offense                1%        [0.5%, 5%]      +-1pp
    slash_2nd_offense                5%        [2%, 10%]       +-2pp
    slash_3rd_offense                15%       [10%, 25%]      +-5pp
    slash_4th_offense                50%       [30%, 70%]      +-10pp
    bootstrap_sunset_epochs          3 consec  [2, 10]         +-1
    v_class_period                   5 epochs  [3, 10]         +-1
    challenge_rate_limit             3/epoch   [1, 10]         +-1
    epoch_jitter_range               10%       [5%, 15%]       +-5pp

OPERATIONAL (Tier 3) — Admin-Adjusted:
    jitter_entropy_source            prev hash
    batch_size_limit                 100K ops
    crdt_sync_interval               10 sec
    monitoring_staleness_threshold   2 epochs
    monitoring_hhi_threshold         0.25
    log_verbosity                    INFO
```

---

# Appendix F: Adversarial Finding Resolution Matrix

```
Finding  Severity   Attack                       Resolution                        Status
-------  ---------  ---------------------------  --------------------------------  -----------
1        FATAL      Phantom Balance              HDL: EABS write-path              RESOLVED
2        CRITICAL   Reputation Laundering        Cap 3.0x, log scale, diversity    MITIGATED
3        CRITICAL   Settlement Sandwiching       Jitter, commit-reveal, smoothing  MITIGATED
4        HIGH       PC Decay Arbitrage           Quality gates, sqrt, congestion   MITIGATED
5        HIGH       Thin Market Squeeze          Position limits, UIOLI, CPLR     MITIGATED
6        HIGH       Cross-Budget Arbitrage       Sufficient friction model         ACCEPTED
7        CRITICAL   Slashing Ordering            EABS canonical ordering           RESOLVED
8        MEDIUM     RIF Draining                 Min bounds, worker protection     MITIGATED
9        HIGH       Limbo Attack                 Timeout, collateral, caps         MITIGATED
10       MEDIUM     Speed Class Gaming           NPV normalization, rate limits    MITIGATED
```

---

# Appendix G: Hard Gate Resolution Summary

```
HG-1: EABS Protocol Specification
    Resolution: Sections 2.3.1-2.3.8. Bracha's RBC, canonical ordering,
    settlement function, conservation enforcement, recovery protocol.
    Status: SATISFIED.

HG-2: Conservation Invariant Proof
    Resolution: Sections 2.3.7-2.3.8 and 9.1-9.2.
    Unified CONS-1 formula with collateral_held.
    12+ cases covering all OperationType variants.
    Status: SATISFIED.

HG-3: Three-Budget Equilibrium Model
    Resolution: Section 3 + scenarios E6, E9.
    Sufficient friction model with budget collapse transition path (Section 3.5.1).
    Status: SATISFIED (pending simulation confirmation).

HG-4: Capability Score Game-Theoretic Analysis
    Resolution: Section 4 + scenario E10.
    Cap 3.0x, 9-class claim accuracy across D/C/P/R/E/S/K/H/N.
    Status: SATISFIED (pending Monte Carlo E10 confirmation).

HG-5: Capacity Market Minimum Viable Scale
    Resolution: Section 8.9 + scenario E8.
    MVS = 5 independent providers per resource type. CPLR backstop.
    Status: SATISFIED.
```

---

# Appendix H: Cross-Layer API Surface

```
=== C3 (Tidal Noosphere) ===
DSF --> C3: publish_settled_state(epoch, state)          // Per-epoch, STRONG
DSF <-- C3: get_epoch_boundary(epoch) -> Timestamp
DSF <-- C3: get_identity_clusters() -> Vec<Cluster>
DSF <-- C3: on_tidal_phase_transition(transition)

=== C5 (PCVM) ===
DSF --> C5: submit_economic_claim(claim)
DSF <-- C5: get_credibility(entity) -> CredibilityScore
DSF <-- C5: verify_attestation(attestation) -> bool
DSF <-- C5: get_verification_reports(epoch) -> Vec<Report>

=== C6 (EMA) ===
DSF <-- C6: get_knowledge_reports(epoch) -> Vec<Report>
DSF <-- C6: get_metabolic_efficiency(resource) -> Report
DSF <-- C6: submit_shrec_budget(request) -> Allocation

=== C7 (RIF) ===
DSF --> C7: on_settlement_complete(epoch, results)
DSF <-- C7: query_balance(entity, type) -> ECORBalance
DSF <-- C7: check_stake_availability(entity) -> Stake
DSF <-- C7: submit_operation(op) -> Receipt
DSF <-- C7: submit_intent(intent) -> ValidationResult
DSF <-- C7: report_task_completion(report)

=== Alternative C Communication Stack ===
DSF --> Native stack: All settlement messages as sovereign semantic objects
```

---

# Appendix I: Failure Mode Catalogue

20 failure modes consolidated from all sections of the specification.

```
FM-01: PHANTOM BALANCE (Double Spend)
    Trigger:    Concurrent AIC_TRANSFER on different CRDT replicas
    Detection:  Caught at EABS settlement (balance check fails)
    Recovery:   Second transfer rejected during EABS batch processing
    Severity:   FATAL if undetected (RESOLVED by EABS design)

FM-02: CONSERVATION VIOLATION (Implementation Bug)
    Trigger:    Bug in settlement function or novel attack vector
    Detection:  eabs_conservation_check() returns Err after batch
    Recovery:   ConservationRecovery protocol (Section 9.4.1)
    Severity:   CRITICAL

FM-03: RELIABLE BROADCAST FAILURE
    Trigger:    >f nodes crash (more than n/3 Byzantine)
    Detection:  Epoch boundary passes without COMMITTED phase
    Recovery:   Settlement stalls. CRDT read-path continues. Resumes when majority restored.
    Severity:   HIGH

FM-04: SETTLEMENT HASH MISMATCH
    Trigger:    Non-determinism in settlement function or corrupted state
    Detection:  Nodes compare settlement_hash after each epoch
    Recovery:   EpochRecovery protocol. Minority nodes re-download and re-execute.
    Severity:   HIGH

FM-05: LIMBO ATTACK (Resource Lockup)
    Trigger:    PENDING_INITIATE without completing/timing out
    Detection:  check_pending_timeouts() at each epoch
    Recovery:   Mandatory 3-epoch timeout. 2% fee burned. Collateral partially forfeited.
    Severity:   HIGH (mitigated by timeout + caps)

FM-06: THIN MARKET FAILURE
    Trigger:    independent_providers(R) < 5 for any resource type
    Detection:  MVS check at each epoch boundary
    Recovery:   CPLR activation (treasury-funded provider of last resort)
    Severity:   HIGH

FM-07: REPUTATION LAUNDERING (Sybil Farming)
    Trigger:    Multiple identities with correlated behavior
    Detection:  Sentinel Graph behavioral correlation > 0.85
    Recovery:   Cluster position limits (POS-2). Slashing for GOVERNANCE_MANIPULATION.
    Severity:   HIGH (mitigated by cap=3.0, log scaling)

FM-08: SETTLEMENT SANDWICHING
    Trigger:    Attacker controls timing of task completion reports
    Detection:  Cross-epoch smoothing (>25% deviation)
    Recovery:   Commit-reveal. Epoch jitter. Sliding window evaluation.
    Severity:   MEDIUM (residual advantage <2%)

FM-09: PC DECAY ARBITRAGE
    Trigger:    Agent spends PC immediately after earning, before decay
    Detection:  Cross-budget flow monitoring
    Recovery:   Quality gates. Sublinear earning. Congestion pricing.
    Severity:   MEDIUM

FM-10: CAPACITY MARKET CORNERING
    Trigger:    Single entity/cluster acquires >15% of capacity supply
    Detection:  HHI > 0.25 per resource type
    Recovery:   Position limits. Emergency 10% limit if HHI > 0.40.
    Severity:   MEDIUM

FM-11: CROSS-BUDGET ARBITRAGE
    Trigger:    Implicit exchange rate stabilizes (low variance)
    Detection:  BM-1 metrics (Section 3.5.1)
    Recovery:   Governance adjusts friction. Worst case: budget collapse transition.
    Severity:   MEDIUM (accepted with friction)

FM-12: SLASHING ORDERING AMBIGUITY
    Trigger:    Non-deterministic violation processing order
    Detection:  Settlement hash mismatch (FM-04)
    Recovery:   FULLY RESOLVED by EABS canonical ordering.
    Severity:   CRITICAL (RESOLVED)

FM-13: RIF DRAINING (Worker Exploitation)
    Trigger:    resource_bounds < actual task cost
    Detection:  Worker over-budget flagging. 3+ flags triggers review.
    Recovery:   Minimum bounds floor (70% trailing median). Worker inspection window.
    Severity:   MEDIUM

FM-14: CROSS-LOCUS RECONCILIATION FAILURE
    Trigger:    Network partition during cross-locus settlement phase
    Detection:  Phase 3 conservation check fails
    Recovery:   All cross-locus ops rolled back. Per-locus settlements still apply.
    Severity:   MEDIUM

FM-15: SENTINEL GRAPH UNAVAILABILITY
    Trigger:    C3 infrastructure failure or partition
    Detection:  Query timeout on get_identity_clusters()
    Recovery:   Continue with last known data. POS-2 degraded to POS-1. Governance alert.
    Severity:   MEDIUM

FM-16: PCVM ATTESTATION UNAVAILABILITY
    Trigger:    C5 infrastructure failure
    Detection:  verify_attestation() call fails
    Recovery:   PC earning SUSPENDED. Existing PC continues to decay. No backfill.
    Severity:   MEDIUM

FM-17: GOVERNANCE QUORUM FAILURE
    Trigger:    Voting weight < quorum threshold
    Detection:  Vote tally at voting period end
    Recovery:   Proposal fails. Bond forfeited. Stream 4 bonus review triggered.
    Severity:   LOW

FM-18: EPOCH BOUNDARY CLOCK SKEW
    Trigger:    NTP failure or adversarial clock manipulation
    Detection:  Epoch boundary jitter plus Reliable Broadcast timing
    Recovery:   Jitter seed is hash-based. Nodes missing boundary have ops deferred.
    Severity:   LOW

FM-19: TREASURY DRAIN
    Trigger:    Excessive CPLR spending, slashing burn rates, or governance spend
    Detection:  treasury_balance < emergency_reserve_floor * 1.5
    Recovery:   Constitutional protection. CPLR auto-pauses. Governance alert at 150%.
    Severity:   LOW

FM-20: STALE LOCUS (Degraded Mode)
    Trigger:    Locus fails to receive settled state for >3 epochs
    Detection:  staleness_bound > 3 epochs
    Recovery:   Locus enters DEGRADED mode (read-only). EpochRecovery from any non-stale locus.
    Severity:   LOW
```

---

# Appendix J: Monitoring Specification

```
MF-1: SETTLEMENT STALENESS
    Metric:     max(current_epoch - node.epoch_settled) across all HDL nodes
    Collection: Every SETTLEMENT_TICK (60s)
    WARN:       staleness >= 2 SETTLEMENT_TICKs
    ALERT:      staleness >= 3 SETTLEMENT_TICKs (locus enters DEGRADED)
    CRITICAL:   staleness >= 5 SETTLEMENT_TICKs

MF-2: CONSERVATION DELTA
    Metric:     |aic_lhs - aic_rhs| after each eabs_conservation_check()
    Collection: Every SETTLEMENT_TICK (post-settlement)
    CRITICAL:   Any non-zero delta (zero tolerance)

MF-3: CROSS-BUDGET FLOW RATIO
    Metric:     (AIC on self-sponsored tasks) / (total AIC settlement volume)
    Collection: Every TIDAL_EPOCH (3600s)
    WARN:       ratio > 0.05 for 3 consecutive TIDAL_EPOCHs
    ALERT:      ratio > 0.10 for 5 consecutive TIDAL_EPOCHs

MF-4: MARKET CONCENTRATION (HHI)
    Metric:     Herfindahl-Hirschman Index per resource type
    Collection: Every SETTLEMENT_TICK (post-clearing)
    WARN:       HHI > 0.25
    ALERT:      HHI > 0.40 (emergency 10% position limit auto-enforced)

MF-5: GOVERNANCE PARTICIPATION RATE
    Metric:     (voting weight voted) / (total governance weight)
    Collection: Every G-class settlement period
    WARN:       participation < 0.30 for 3 consecutive G-class periods
    ALERT:      participation < 0.20 for 5 consecutive periods

MF-6: PENDING STATE VOLUME
    Metric:     Sigma(pending_out) / total_aic_supply
    Collection: Every SETTLEMENT_TICK
    WARN:       ratio > 0.15
    ALERT:      ratio > 0.20 (approaching 0.25 global cap)
```

---

# Appendix K: Formal Verification Roadmap

```
Target tools: TLA+ for protocol properties, Dafny for implementation correctness.

FV-1: EABS DETERMINISM (TLA+)
    Same broadcast_set produces identical SettlementResult on all honest nodes.

FV-2: CONSERVATION INVARIANT (Dafny)
    For all 23 operation types: CONS-1 preserved as post-condition.
    Batch-level invariant by induction.

FV-3: LIVENESS UNDER f < n/3 BYZANTINE (TLA+)
    Every epoch eventually reaches COMMITTED phase under partial synchrony.

FV-4: SETTLEMENT COMPLETENESS (TLA+)
    Every valid operation is either included, rejected with reason, or deferred.
    No valid operation silently dropped.

FV-5: PENDING STATE TERMINATION (TLA+/Dafny)
    Every PendingRecord reaches terminal state within 3 SETTLEMENT_TICKs + 1.
```

---

# Appendix L: Changelog

```
v2.0.1 (2026-03-15) — T-304 Economics Retrofit
    DSF capacity-market economics now explicitly assume Alternative C
    sovereign compute posture rather than an open external provider market.

    Changes:
        - Header updated with T-304 renovation note and current version/date.
        - Section 1.2 retitled the centralized-runtime baseline to include
          leased-provider models and provider-credit dependence.
        - Section 8 now defines Alternative C supply classes: sovereign
          habitats, bounded C45 leased cognition, and C47 Forge promotion /
          quarantine lanes.
        - Reserve pricing and bootstrap provisions now encode build-vs-buy
          ordering so temporary leased lanes cannot undercut sovereign capacity.
        - Treasury allocation notes now treat C47 promotion as explicit
          development spend and leased cognition as transitional, bounded debt.
        - Glossary updated so CPLR reflects sovereign reserve posture.

v2.0 (2026-03-10) — Unified Specification
    This document unifies the original C8 Master Tech Spec (Parts 1 and 2),
    Patch Addendum v2.0.1, and C9 Cross-Layer Reconciliation errata into a
    single standalone specification.

    Changes incorporated from Patch Addendum v2.0.1:

    F52 (HIGH) — Internal Epoch Inconsistency:
        All epoch references unified to SETTLEMENT_TICK = 60s.
        Removed all 10-minute epoch references from Part 2.
        Added temporal hierarchy terminology note (Section 1.4).
        Corrected parameter sensitivity table (Appendix E).
        Corrected scenario E5 (governance changes 60s to 45s, not 10min to 7min).

    F53 (MEDIUM) — Conservation Formula Variant:
        Unified CONS-1 formula now includes collateral_held in all locations.
        check_conservation() uses canonical formula without pending_in subtraction.
        pending_in tracked separately via CONS-1a auxiliary invariant.

    F54 (MEDIUM) — Three-Budget Collapse Path:
        Added BM-1 monitoring criteria (Section 3.5.1).
        Added BudgetCollapseTransition governance protocol with 10-tick migration.

    F55 (MEDIUM) — Slashing Pseudocode Fix:
        SLASH case in apply_operation now implements 50/30/20 three-way split
        (burn/treasury/reporter) instead of full amount to treasury.
        Conservation proof updated for slash distribution.

    F56 (MEDIUM) — Failure Mode Catalogue:
        20 failure modes consolidated into Appendix I.

    F57 (MEDIUM) — Four-Stream Scoring Simplification:
        Bootstrap simplified scoring for Streams 3+4 added (Section 6.2.3-6.2.4).
        STREAM_SCORING_UPGRADE trigger rule added (Section 6.2.5).

    F58 (LOW) — AccountState Mismatch:
        Canonical AccountState includes collateral_held (PNCounter) and
        cs_allocation as Map<ResourceType, PNCounter>.
        Convergence proof updated for new fields.

    F59 (LOW) — Settlement Function Incomplete:
        All 11 missing operation implementations added to Section 2.3.6:
        PC_EARN, PC_SPEND, CS_ALLOCATE, CS_RELEASE, CS_REVERT,
        CAPACITY_BID, CAPACITY_CLEAR, CAPACITY_SPOT,
        REWARD_V_CLASS, REWARD_G_CLASS, PARAMETER_UPDATE.

    F60 (LOW) — NPV Asymmetry Documentation:
        Explanation of B-class/V-class NPV asymmetry added (Section 5.1.1).

    F61 (LOW) — Monitoring Specification:
        MF-1 through MF-6 fully specified in Appendix J.

    F62 (LOW) — Formal Verification Scope:
        5 formal verification properties specified in Appendix K.

    Changes incorporated from C9 Cross-Layer Reconciliation:

    E-C8-01 — Claim Class Difficulty Weights:
        5-class + modifier scheme replaced with 9-class table
        (D=1.0, C=1.3, P=1.5, E=1.5, K=1.8, S=2.0, R=2.0, H=2.5, N=3.0).
        Claim class to settlement type mapping updated for all 9 classes.

    E-C8-02 — SETTLEMENT_TICK as canonical timing:
        All C8 epoch references confirmed as SETTLEMENT_TICK (60s).
        Three-tier temporal hierarchy integrated (Section 1.4).

    C8 confirmed as sole settlement authority per C9 INV-S1.
```

---

*End of C8 Master Technical Specification — Deterministic Settlement Fabric v2.0.1 (Unified)*
*Specification Writer: Atrahasis Agent System*
*Date: 2026-03-15*
