# Deterministic Settlement Fabric v2.0 — Master Technical Specification

## Part 1 of 2: Core Architecture and Economic Model

**Invention ID:** C8
**System:** Atrahasis Planetary-Scale Distributed AI Agent System
**Stage:** SPECIFICATION
**Version:** 2.0
**Date:** 2026-03-10
**Classification:** Whitepaper — Self-Contained Technical Specification
**Target Audience:** Systems architects, distributed systems researchers, mechanism designers
**Scope:** Sections 1-8 of 16 (Part 2 covers Sections 9-16)

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
Appendix A: Notation and Symbols
Appendix B: Parameter Reference Table

---

# Section 1: Introduction and Motivation

## 1.1 The Problem: Economic Settlement for Autonomous AI Agent Systems

Planetary-scale AI agent systems — networks of thousands to hundreds of thousands of autonomous agents performing distributed computation, verification, and coordination — require an economic substrate. Without one, there is no mechanism to:

- **Allocate scarce resources** (compute, storage, bandwidth) among competing agents with heterogeneous capabilities and demands.
- **Incentivize quality** in task execution and verification, where the outputs are epistemic (knowledge claims, inference results) rather than deterministically checkable.
- **Punish defection** when agents submit fraudulent work, free-ride on others' verification, or attempt to monopolize shared infrastructure.
- **Prevent spam** in open or semi-open networks where the cost of generating plausible-looking agent messages is near zero.
- **Coordinate at scale** without centralized orchestration that creates single points of failure and trust concentration.

The Atrahasis system is one such network. It comprises six architectural layers:

```
Layer 6: RIF — Recursive Intent Fabric (Orchestration)          C7
Layer 5: Tidal Noosphere (Coordination, CRDT state, topology)   C3
Layer 4: PCVM — Probabilistic Claim Verification Machine        C5
Layer 3: EMA — Epistemic Metabolism Architecture                 C6
Layer 2: DSF — Deterministic Settlement Fabric (THIS DOCUMENT)   C8
Layer 1: ASV — Agent Semantic Vocabulary (Communication)         C4
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

### 1.2.2 Centralized Billing (Cloud Provider Models)

Centralized billing (AWS-style metered usage, internal accounting databases) provides low latency and simplicity but creates:

- **Single point of failure and trust.** A centralized billing authority can arbitrarily modify balances, deny service, or extract rents. For an autonomous agent system, this reintroduces the principal-agent problem that decentralization was meant to solve.
- **No verifiable conservation.** Without distributed verification, there is no guarantee that the total economic supply is conserved. The billing authority can inflate or deflate at will.
- **No credible commitment.** Slashing penalties and staking mechanisms require credible commitment — the guarantee that penalties will be enforced even if the penalized party controls infrastructure. Centralized systems cannot provide this against the operator.

### 1.2.3 No Economy (Pure Coordination)

Some multi-agent frameworks (AutoGPT, CrewAI, LangGraph) operate without internal economics, relying on external funding (user-provided API keys) and centralized orchestration. This works for small-scale, short-lived agent teams but cannot support:

- **Persistent agent populations** that must sustain themselves economically across unbounded time horizons.
- **Adversarial environments** where agents have incentives to defect, free-ride, or manipulate.
- **Resource allocation** at scale, where thousands of agents compete for finite compute and bandwidth.

## 1.3 DSF's Position: CLS-Meets-IOTA for AI Agents

DSF draws architectural inspiration from two domains:

**From traditional clearing systems (CLS, ACH, SWIFT):** The insight that settlement does not require real-time consensus. CLS settles $6.6 trillion daily in foreign exchange using multilateral netting and batch processing, reducing gross settlement by ~96%. ACH processes 80 million transactions daily in the United States using same-day and next-day batch windows. DSF adopts this batch settlement paradigm: operations are collected during epochs and settled atomically at epoch boundaries.

**From IOTA 2.0 (Mana, congestion control):** The insight that economic functions should be separated into distinct instruments. IOTA 2.0 separates its native token (value transfer) from Mana (congestion control and access). DSF extends this to a three-budget model: Sponsor Budget (payment), Protocol Credits (spam control), and Capacity Slices (resource allocation).

The synthesis — **batch settlement with multi-budget separation, purpose-built for AI agent workloads** — is DSF's core architectural contribution.

## 1.4 The v1 Fatal Flaw and v2 Resolution

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

## 1.5 Document Roadmap

This document (Part 1) specifies the core architecture and economic model:

- **Section 2** specifies the Hybrid Deterministic Ledger — the primary technical contribution. It includes CRDT read-path data structures with merge proofs, the complete EABS write-path protocol (five phases, Bracha's Reliable Broadcast, deterministic ordering, settlement function), the ECOR consistency model, fault model, conservation enforcement with proof sketch, and test vectors.

- **Section 3** defines the Three-Budget Economic Model: Sponsor Budget (AIC), Protocol Credits (PC), and Capacity Slices (CS), with lifecycle mechanics, cross-budget friction analysis, and equilibrium proofs.

- **Section 4** specifies the Capability-Weighted Stake system: formula derivation, input components, Sybil resistance, cold-start protocol, and game-theoretic analysis.

- **Section 5** details the Multi-Rate Settlement Engine: B/V/G settlement classes, epoch boundary protocol, NPV normalization, and cross-class timing.

- **Section 6** covers the Four-Stream Settlement computation: stream metrics, reward distribution, cross-stream interactions, and simulation scenarios.

- **Section 7** specifies Intent-Budgeted Settlement: RIF integration, budget mechanics, worker protections, and settlement type mapping.

- **Section 8** defines the Capacity Market: sealed-bid uniform-price auction, progressive clearing, position limits, bootstrap provisions, and minimum viable scale analysis.

Part 2 (separate document) covers CSO Conservation Framework, Graduated Slashing, Treasury and Governance, Integration Protocols, Failure Mode Catalogue, and Parameter Sensitivity Analysis.

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
    account_id:          AgentID
    aic_balance:         PNCounter       // Sponsor Budget (AIC)
    pc_balance:          PNCounter       // Protocol Credits
    cs_allocation:       PNCounter       // Capacity Slices held
    staked_aic:          PNCounter       // AIC locked as collateral
    pending_out:         PNCounter       // Outbound pending transfers
    pending_in:          PNCounter       // Inbound pending transfers
    last_settled_epoch:  uint64          // Epoch of last EABS settlement
    capability_score:    float64         // Cached from last V-class settlement
    violation_count:     uint32          // Monotonic slashing counter
    state_vector:        Map<NodeID, uint64>  // Lamport timestamps per node

    FUNCTION merge(other: AccountState) -> AccountState:
        ASSERT self.account_id == other.account_id
        result = AccountState{account_id: self.account_id}
        result.aic_balance = self.aic_balance.merge(other.aic_balance)
        result.pc_balance = self.pc_balance.merge(other.pc_balance)
        result.cs_allocation = self.cs_allocation.merge(other.cs_allocation)
        result.staked_aic = self.staked_aic.merge(other.staked_aic)
        result.pending_out = self.pending_out.merge(other.pending_out)
        result.pending_in = self.pending_in.merge(other.pending_in)
        result.last_settled_epoch = max(self.last_settled_epoch, other.last_settled_epoch)
        result.capability_score = IF self.last_settled_epoch >= other.last_settled_epoch
                                  THEN self.capability_score
                                  ELSE other.capability_score
        result.violation_count = max(self.violation_count, other.violation_count)
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

Every component of the merge function uses either max() or PNCounter.merge(), both of which are commutative. For max(x, y) = max(y, x) trivially. For PNCounter.merge(), commutativity follows from the commutativity of max() applied element-wise to the positive and negative maps. The union() of key sets is commutative. Therefore the overall merge is commutative.

*Associativity:* merge(merge(A, B), C) = merge(A, merge(B, C)).

max() is associative over natural numbers. PNCounter.merge() inherits associativity from element-wise max(). Union of key sets is associative. Therefore the overall merge is associative.

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
max_staleness = epoch_duration + reliable_broadcast_latency + settlement_computation_time
```

For the recommended epoch duration of 60 seconds with reliable broadcast latency of approximately 2 seconds and settlement computation of approximately 1 second, maximum staleness is approximately 63 seconds.

## 2.3 EABS Write Path

### 2.3.1 Epoch Lifecycle

Each epoch progresses through five phases:

```
COLLECTING --> BROADCASTING --> ORDERING --> SETTLING --> COMMITTED
   (active       (Bracha's        (canonical     (settlement    (state
    epoch)        RBC)             sort)          function)      merged
                                                                into CRDT)

Timeline within an epoch:
|<------- epoch_duration (60s nominal) ------->|
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
    total_cs_supply:    uint64
    epoch_number:       uint64
    treasury_balance:   uint64
    reward_pools:       Map<SettlementStream, uint64>
    pending_registry:   Map<PendingID, PendingState>
    parameter_set:      ProtocolParameters
    settlement_hash:    bytes32          // Hash of entire settled state

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

**Per-operation application (representative cases):**

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
            violator.staked_aic.decrement(op.submitter_id, penalty)
            state.treasury_balance += penalty
            violator.violation_count = max(
                violator.violation_count, op.payload.offense_number)
            RETURN Success(state)

        CASE PC_DECAY:
            FOR each account IN state.accounts.values():
                decay_amount = floor(account.pc_balance.value() * 0.10)
                account.pc_balance.decrement(op.submitter_id, decay_amount)
            RETURN Success(state)

        CASE REWARD_B_CLASS:
            recipient = state.accounts[op.payload.recipient]
            adjusted = floor(op.payload.base_amount * op.payload.npv_adjustment)
            IF adjusted > state.reward_pools[op.payload.stream]:
                RETURN Failure(INSUFFICIENT_REWARD_POOL)
            state.reward_pools[op.payload.stream] -= adjusted
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
            acct.pending_out.increment(op.submitter_id, op.payload.amount)
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
            counterparty.aic_balance.increment(op.submitter_id, pending.amount)
            initiator.aic_balance.increment(op.submitter_id, pending.collateral)
            DELETE state.pending_registry[op.payload.pending_id]
            RETURN Success(state)

        CASE PENDING_TIMEOUT:
            pending = state.pending_registry[op.payload.pending_id]
            IF pending.epoch_initiated + 3 > state.epoch_number:
                RETURN Failure(PENDING_NOT_YET_TIMED_OUT)
            initiator = state.accounts[pending.initiator_id]
            timeout_fee = floor(pending.amount * 0.02)
            collateral_return = pending.collateral - timeout_fee
            state.treasury_balance += timeout_fee
            initiator.aic_balance.increment(op.submitter_id, collateral_return)
            initiator.pending_out.decrement(op.submitter_id, pending.amount)
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

        // PC_EARN, PC_SPEND, CS_ALLOCATE, CS_RELEASE, CS_REVERT,
        // CAPACITY_BID, CAPACITY_CLEAR, CAPACITY_SPOT, REWARD_V_CLASS,
        // REWARD_G_CLASS, PARAMETER_UPDATE follow the same pattern:
        // validate preconditions, modify state atomically, return result.
```

### 2.3.6 Conservation Enforcement

**Definition 2.6 (Conservation Invariant).** The CSO conservation invariant is a predicate over SettlementState that must hold after every epoch settlement.

```
FUNCTION check_conservation(state: SettlementState) -> bool:
    // AIC Conservation (INV-CONS-1)
    total_aic_in_accounts = 0
    total_aic_staked = 0
    total_pending_out = 0
    total_pending_in = 0

    FOR each account IN state.accounts.values():
        total_aic_in_accounts += account.aic_balance.value()
        total_aic_staked += account.staked_aic.value()
        total_pending_out += account.pending_out.value()
        total_pending_in += account.pending_in.value()

    aic_conservation =
        (total_aic_in_accounts + total_aic_staked +
         total_pending_out - total_pending_in +
         state.treasury_balance)
        == state.total_aic_supply

    // CS Conservation (INV-CONS-2)
    total_cs_held = 0
    total_cs_pending = 0
    FOR each account IN state.accounts.values():
        total_cs_held += account.cs_allocation.value()
    FOR each pending IN state.pending_registry.values():
        IF pending.budget_type == CS:
            total_cs_pending += pending.amount

    cs_conservation =
        (total_cs_held + total_cs_pending)
        == state.total_cs_supply

    RETURN aic_conservation AND cs_conservation
```

**Invariant CONS-1 (AIC Conservation).** For every epoch E, after settlement:

```
Sigma(aic_balance_i) + Sigma(staked_aic_i) + Sigma(pending_out_i)
    - Sigma(pending_in_i) + treasury_balance = total_aic_supply
```

**Invariant CONS-2 (CS Conservation).** For every epoch E, after settlement:

```
Sigma(cs_allocation_i) + Sigma(cs_pending_j) = total_cs_supply
```

**Invariant CONS-3 (PC Non-Conservation, by design).** Protocol Credits are intentionally non-conserved. They are created (earned) and destroyed (decayed, spent). There is no total_pc_supply invariant. PC is bounded by the per-account cap: pc_balance_i <= 10 * epoch_earning_rate(i).

### 2.3.7 Conservation Proof Sketch

**Theorem 2.2.** If settle_epoch returns conservation_valid = true, then CONS-1 and CONS-2 hold for the post-settlement state.

**Proof.**

*Base case:* At epoch 0 (genesis), total_aic_supply = treasury_balance, all account balances are zero. CONS-1: 0 + 0 + 0 - 0 + treasury_balance = total_aic_supply. Holds trivially. CONS-2: 0 + 0 = 0 = total_cs_supply. Holds trivially.

*Inductive step:* Assume CONS-1 and CONS-2 hold for pre_state (after epoch E-1). We show each operation type preserves conservation:

- **AIC_TRANSFER:** Decrements from_account by X, increments to_account by X. Net change to Sigma(aic_balance_i) = 0. Conservation preserved.
- **AIC_STAKE:** Decrements aic_balance by X, increments staked_aic by X (same account). Net change to LHS of CONS-1 = 0. Preserved.
- **AIC_UNSTAKE:** Reverse of AIC_STAKE. Preserved.
- **SLASH:** Decrements staked_aic by penalty, increments treasury_balance by penalty. Net change = 0. Preserved.
- **TREASURY_MINT:** Increments total_aic_supply by X AND treasury_balance by X. Both sides increase by X. Preserved.
- **TREASURY_BURN:** Decrements total_aic_supply by X AND treasury_balance by X. Both sides decrease by X. Preserved.
- **REWARD_*:** Decrements reward_pool (part of treasury) by X, increments recipient balance by X. Net change to (Sigma(balances) + treasury) = 0. Preserved.
- **PENDING_INITIATE:** Collateral moved from aic_balance to protocol hold. pending_out increases by X. Net conservation change = 0. Preserved.
- **PENDING_COMPLETE:** pending_out decremented by X, counterparty balance incremented by X, collateral returned. Net equivalent to transfer + collateral return. Preserved.
- **PENDING_TIMEOUT:** pending_out decremented by X, balance restored minus fee, fee to treasury. Net = 0. Preserved.
- **PC_DECAY/PC_EARN/PC_SPEND:** Not part of AIC or CS conservation. No effect on CONS-1 or CONS-2.
- **CS_ALLOCATE/CS_RELEASE/CS_REVERT:** Balanced transfers within CS domain. CONS-2 preserved.

Each operation individually preserves conservation. The settlement function applies them sequentially. By induction over the ordered batch, conservation is preserved after all operations.

The explicit check_conservation call provides runtime verification, catching any implementation bugs that might violate the theoretical guarantee.

**Recovery protocol:** If check_conservation returns false (indicating a bug), the entire epoch batch is rejected and all nodes revert to pre_state. A diagnostic trace is emitted.  QED.

### 2.3.8 Epoch-Consistent Optimistic Reads (ECOR)

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

### 2.3.9 Fault Model and Recovery

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

// Recommended: epoch_duration_ms = 60000 (60 seconds)
// network_entropy_source = hash(previous epoch's settlement_hash)
```

**Invariant EPOCH-1:** All honest nodes compute the same jittered boundary for epoch E, because jitter_seed derives from deterministic inputs.

### 2.3.10 Test Vector: Example Epoch

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
2000 + 1500 + 700 + 500 + 300 + 0 + 0 - 0 + 5000 = 10000. CONS-1 holds.

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
1849 + 1629 + 700 + 500 + 400 + 0 + 0 - 0 + 5000
= 10078. But reward pools are part of treasury.
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
       +-- SLASH (penalty -> treasury)
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
    Frequency:  Per-epoch (every ~60 seconds)
    Scope:      Scheduling compliance rewards (Stream 1)
                Communication efficiency rewards (Stream 3)
                PC decay, PC earning/spending
                CS allocation/release
                AIC transfers
    NPV factor: 0.98 (2% discount for timing advantage)
    Analogy:    RTGS (Real-Time Gross Settlement)

V-CLASS ("Standard Settlement"):
    Frequency:  Every N epochs (default N=5, ~5 minutes)
    Scope:      Verification quality rewards (Stream 2)
                Slashing penalties
                Capability score updates
                Challenge resolution
    NPV factor: (1 + r)^delay where r = 0.002 (0.2% per epoch)
    Challenge rate limit: 3 per entity per epoch
    Challenge bond: 5% of challenged amount
    Analogy:    End-of-day netting

G-CLASS ("Governance Settlement"):
    Frequency:  Governance-triggered (10-50 epochs typical)
    Scope:      Governance participation rewards (Stream 4)
                Parameter changes
                Treasury operations (mint/burn)
                Constitutional amendments
                Appeal resolutions
    NPV factor: (1 + r)^delay (computed per-operation)
    Analogy:    Securities settlement (T+2 or longer)
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
    Source: C4 (ASV)
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

### 6.2.4 Governance Participation (Stream 4)

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

| RIF Settlement Type | DSF Class | Reward Stream |
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

1. **Thin participation.** At primary scale (1K-10K agents), the market may have only dozens of providers per resource type.
2. **Epoch-discretized clearing.** Prices set at epoch boundaries, not continuously.
3. **Adversarial participants.** Capacity withholding, demand inflation, and cornering are viable strategies.
4. **Bootstrap phase.** The market must function even below minimum viable scale.

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
    T1: Provider-offered capacity
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
    // Standard supply-demand intersection algorithm
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
    Calibration: 80% of estimated marginal cost of providing one CS unit
    Review: Every 50 epochs by governance

Enforcement:
    Offers with min_price < floor are REJECTED
```

## 8.9 Bootstrap Provisions

### 8.9.1 Minimum Viable Scale

```
CONDITION MVS (Minimum Viable Scale):
    number_providers >= 3 * number_resource_types
    AND FOR EACH resource_type R:
        independent_providers(R) >= 5

Given 6 resource types:
    Minimum ~10 providers (if each covers multiple types)
    Functional minimum: 5 per type for meaningful price discovery
```

The "5 per type" requirement ensures no single provider failure eliminates more than 20% of supply, and position limits (15%) bind meaningfully.

### 8.9.2 Bootstrap Capacity Provider of Last Resort (CPLR)

```
CPLR Configuration:
    Treasury allocation:  Up to 20% of treasury
    Pricing rule:         Reserve floor * 1.1 (slightly above floor)
    Participation rule:   Bids ONLY when provider_count(R) < 5
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

# Appendix A: Notation and Symbols

| Symbol | Definition |
|---|---|
| AIC | Atrahasis Internal Credit (primary token) |
| PC | Protocol Credits (spam control token) |
| CS | Capacity Slices (resource allocation token) |
| HDL | Hybrid Deterministic Ledger |
| EABS | Epoch-Anchored Batch Settlement |
| ECOR | Epoch-Consistent Optimistic Reads |
| RBC | Reliable Broadcast (Bracha's protocol) |
| CSO | Capability Service Obligation |
| n | Total number of HDL nodes |
| f | Maximum number of faulty nodes (f < n/3) |
| E | Epoch number |
| r | Epoch discount rate (default 0.002) |
| k | PC earning coefficient (default 10) |
| Sigma | Summation over all accounts |
| CONS-1 | AIC conservation invariant |
| CONS-2 | CS conservation invariant |

---

# Appendix B: Parameter Reference Table

| Parameter | Default Value | Governance-Adjustable | Sensitivity |
|---|---|---|---|
| epoch_duration_ms | 60000 (60s) | Yes | 2x: higher latency, larger batches. 0.5x: more coordination overhead |
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

*End of Part 1 (Sections 1-8). Part 2 continues with CSO Conservation Framework, Graduated Slashing, Treasury and Governance, Integration Protocols, Failure Mode Catalogue, and Parameter Sensitivity Analysis.*
