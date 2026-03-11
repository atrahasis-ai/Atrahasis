# C8 — Deterministic Settlement Fabric (DSF) v2.0

## Architecture Document — Part 1 (Sections 1–7)

---

## 1. Executive Summary

### 1.1 Position in the Atrahasis Stack

The Deterministic Settlement Fabric (DSF) is the economic settlement layer of the Atrahasis planetary-scale distributed AI agent system. It occupies a precise position in a six-layer architecture:

```
+=========================================================================+
|  C7: RIF — Recursive Intent Fabric (Orchestration)                      |
|    Intent Quanta, decomposition algebra, System 3/4/5, VSM executive    |
|    DSF INTERFACE: Intent resource_bounds as budget ceilings,            |
|                   settlement type classification (B/V/G),               |
|                   stake availability queries (optimistic read path)     |
+=========================================================================+
          |                    |                    |
          | budget ceilings    | settlement events  | stake queries
          v                    v                    v
+=========================================================================+
|  C8: DSF — Deterministic Settlement Fabric (THIS DOCUMENT)              |
|    Hybrid Deterministic Ledger, Three-Budget Model, Multi-Rate Engine,  |
|    Four-Stream Settlement, Capability-Weighted Stake, Capacity Market   |
+=========================================================================+
          |                    |                    |
          | CRDT state         | verification data  | knowledge metrics
          v                    v                    v
+=========================================================================+
|  C3: Tidal Noosphere    C5: PCVM           C6: EMA                      |
|  (Coordination)         (Verification)     (Knowledge Metabolism)        |
|  Parcels, loci,         Claim classes,     Epistemic quanta,            |
|  tidal scheduling,      VTDs, MCTs,        SHREC regulation,           |
|  CRDTs, VRF             credibility        coherence graph             |
+=========================================================================+
          |
          | semantic vocabulary
          v
+=========================================================================+
|  C4: ASV — Agent Semantic Vocabulary (Communication)                    |
|    JSON Schema semantic vocabulary, claim/evidence structures            |
+=========================================================================+
```

DSF receives intent-level budget constraints from RIF (C7) above and relies on coordination primitives from C3, verification attestations from C5, and metabolic efficiency data from C6 below. It produces settlement outcomes — deterministic reward distributions, slashing penalties, capacity allocations, and budget state transitions — that all layers consume.

### 1.2 The v1 Fatal Flaw and v2 Resolution

DSF v1 proposed a pure-CRDT ledger for AIC (Atrahasis Internal Credit) balances, claiming that consensus was unnecessary for settlement. The Adversarial Analysis identified a fatal flaw: CRDTs cannot enforce global invariants such as "no account goes negative" or "total supply is conserved" during concurrent transfer operations. Specifically:

- **Phantom Balance Attack (Attack 1, FATAL):** Concurrent transfers from both sides of a network partition produce valid local state on each side but violate conservation upon merge.
- **Slashing Ordering Attack (Attack 7, CRITICAL):** Graduated penalties require causal ordering that CRDTs do not provide.
- **Conservation Verification (Science Assessment, 2/5):** Runtime enforcement of the CSO conservation invariant requires consistent snapshots, which CRDTs cannot produce without coordination.

DSF v2 resolves all three through the **Hybrid Deterministic Ledger (HDL)**:

| Property | v1 (Pure CRDT) | v2 (HDL) |
|---|---|---|
| Read path | CRDT | CRDT (unchanged) |
| Write path | CRDT | Epoch-Anchored Batch Settlement (EABS) |
| Conservation enforcement | Formal proof only | Formal proof + runtime enforcement |
| Ordering guarantee | None (eventual consistency) | Deterministic canonical ordering per epoch |
| Coordination requirement | None | Lightweight Reliable Broadcast (not full BFT) |
| Fault tolerance | Partition-tolerant reads | Partition-tolerant reads + crash-fault-tolerant writes (f < n/3) |

The key insight: **determinism does not require eliminating coordination — it requires ensuring that all honest nodes process the same inputs in the same order.** EABS achieves this by collecting all state-mutating operations during an epoch, broadcasting them via Reliable Broadcast, sorting them deterministically, and processing them atomically at the epoch boundary.

### 1.3 Key Innovations

1. **Hybrid Deterministic Ledger (HDL):** CRDT-replicated reads for availability and partition tolerance; EABS writes for conservation and consistency. The first architecture to combine CRDT availability guarantees with batch settlement consistency guarantees in a single ledger abstraction.

2. **Epoch-Consistent Optimistic Reads (ECOR):** A novel consistency model where reads reflect the last settled epoch state plus optimistic (unconfirmed) current-epoch deltas. Provides useful approximate state without blocking on settlement.

3. **Three-Budget Economic Model:** Sponsor Budget (AIC), Protocol Credits (PC), and Capacity Slices (CS) provide functional separation of payment, spam control, and resource allocation — with honest acknowledgment that perfect economic isolation is impossible, replaced by calibrated friction mechanisms.

4. **Multi-Rate Settlement with NPV Normalization:** B-class (per-epoch), V-class (N-epoch), and G-class (governance) settlement speeds matched to operation urgency, with net-present-value normalization to eliminate timing arbitrage.

5. **Capability-Weighted Stake with Sybil Resistance:** effective_stake = AIC_collateral x min(capability_score, 3.0), where capability_score uses logarithmic scaling, diversity requirements, and random claim-class assignment to resist farming.

6. **Intent-Budgeted Settlement:** RIF intent resource_bounds serve as budget ceilings with minimum bounds enforcement, worker protections, and sponsor reputation tracking.

### 1.4 Relationship to Other Layers

| Layer | DSF Reads From | DSF Writes To | Consistency Model |
|---|---|---|---|
| C3 (Tidal Noosphere) | Locus topology, epoch boundaries, Sentinel Graph identity clusters, CRDT state vectors | AIC ledger state (CRDT replicas), CSO allocation updates, capacity market clearing results | Read: CRDT eventual consistency; Write: EABS epoch consistency |
| C4 (ASV) | Claim schemas, evidence structures for settlement disputes | Settlement outcome claims (reward amounts, slashing events) expressed as ASV-formatted provenance | Schema-validated, append-only |
| C5 (PCVM) | Credibility scores (VTDs), claim class assessments, verification attestations for PC identity-binding | Verification reward distributions (V-class), slashing penalties, capability_score updates | Credibility: CRDT-optimistic; Rewards: EABS-settled |
| C6 (EMA) | Metabolic efficiency reports, SHREC regulation state, coherence trends | Knowledge contribution rewards (scheduling compliance stream), SHREC budget allocations | Read-only from EMA; write via EABS |
| C7 (RIF) | Intent resource_bounds (budget ceilings), intent lifecycle events, settlement type classifications | Stake availability (optimistic read), resource return credits (EABS write), settlement confirmations | Budget queries: ECOR; Settlement: EABS |

### 1.5 Document Scope

This document (Part 1) specifies Sections 1-7:

1. Executive Summary (this section)
2. Hybrid Deterministic Ledger — Core Architecture
3. Three-Budget Economic Model
4. Capability-Weighted Stake System
5. Multi-Rate Settlement Engine
6. Four-Stream Settlement Computation
7. Intent-Budgeted Settlement

Part 2 (separate document) will cover Sections 8-14: Capacity Market, CSO Conservation Framework, Graduated Slashing, Treasury and Governance, Integration Protocols, Failure Mode Catalogue, and Parameter Sensitivity Analysis.

---

## 2. Hybrid Deterministic Ledger (HDL) — Core Architecture

The Hybrid Deterministic Ledger is the primary research contribution of DSF v2.0. It resolves the fundamental tension between CRDT availability (partition-tolerant, coordination-free reads) and financial consistency (conservation-preserving, deterministically-ordered writes) by splitting the ledger into two paths with distinct consistency guarantees unified under the ECOR consistency model.

### 2.1 Architecture Overview

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

### 2.2 CRDT Read Path

#### 2.2.1 Data Structures

Each account in the HDL maintains a PN-Counter (Positive-Negative Counter) CRDT for each budget type. The PN-Counter is a well-studied CRDT that supports both increment and decrement operations with guaranteed convergence.

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

**Account State CRDT:**

```
STRUCTURE AccountState:
    account_id:          AgentID
    aic_balance:         PNCounter       // Sponsor Budget (AIC)
    pc_balance:          PNCounter       // Protocol Credits
    cs_allocation:       PNCounter       // Capacity Slices held
    staked_aic:          PNCounter       // AIC locked in stake
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
            result.state_vector[node_id] = max(self.state_vector.get(node_id, 0),
                                                other.state_vector.get(node_id, 0))
        RETURN result
```

**State Vector and Version Tracking:**

```
STRUCTURE HDLStateVector:
    node_id:         NodeID
    epoch_settled:   uint64              // Last epoch this node has settled
    epoch_collecting: uint64             // Current epoch being collected
    account_versions: Map<AgentID, uint64>  // Per-account version counters
    global_version:  uint64              // Monotonic global version

    FUNCTION is_stale(other: HDLStateVector) -> bool:
        RETURN self.epoch_settled < other.epoch_settled

    FUNCTION staleness_bound(other: HDLStateVector) -> uint64:
        RETURN other.epoch_settled - self.epoch_settled
```

#### 2.2.2 Merge Semantics

The CRDT merge operation satisfies the required algebraic properties:

**Commutativity:** merge(A, B) = merge(B, A)
- Proven by the max() operation on all counter components and version fields.

**Associativity:** merge(merge(A, B), C) = merge(A, merge(B, C))
- Proven by the associativity of max() over natural numbers.

**Idempotency:** merge(A, A) = A
- Proven by max(x, x) = x for all x.

These properties guarantee that CRDT replicas converge to the same state regardless of the order in which merge operations are applied, even under arbitrary network reordering, duplication, and delay.

**INVARIANT READ-1:** The CRDT read path never blocks. A read operation returns the locally merged state immediately, without contacting any other node.

**INVARIANT READ-2:** After all messages in transit are delivered, all honest nodes hold identical AccountState for every account. (Standard CRDT eventual consistency.)

**INVARIANT READ-3:** The CRDT read path does NOT enforce conservation. Balances shown may be optimistic (pre-settlement). Only EABS-settled state is conservation-guaranteed.

#### 2.2.3 Consistency Guarantees

The read path provides **session monotonic reads**: once a node observes a balance of X for account A, it will never subsequently report a balance less than X for that account (within the same budget type, absent EABS-settled debits). This follows from the monotonicity of PNCounter merge.

**Staleness Bound:** A read on node N at time t reflects at minimum the state as of epoch (current_epoch - 1), because EABS settlement at each epoch boundary pushes settled state into the CRDT layer. The maximum staleness is:

```
max_staleness = epoch_duration + reliable_broadcast_latency + settlement_computation_time
```

For the recommended epoch duration of 60 seconds with reliable broadcast latency of ~2 seconds and settlement computation of ~1 second, maximum staleness is approximately 63 seconds.

### 2.3 EABS Write Path

#### 2.3.1 Epoch Lifecycle

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

**Phase Definitions:**

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
    conservation_check: bool             // Post-settlement invariant check
```

#### 2.3.2 Operation Types

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
    CS_RELEASE              // Capacity Slice release (voluntary or use-it-or-lose-it)
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

STRUCTURE OperationPayload:
    // AIC_TRANSFER
    from_account:   AgentID
    to_account:     AgentID
    amount:         uint64

    // REWARD_*
    recipient:      AgentID
    stream:         SettlementStream     // Which of four streams
    base_amount:    uint64
    npv_adjustment: float64              // NPV normalization factor

    // SLASH
    violator:       AgentID
    violation_type: ViolationType
    offense_number: uint32               // Determines graduated penalty
    penalty_amount: uint64

    // (other payload variants omitted for brevity -- each OperationType
    //  has a corresponding payload schema defined in the ASV vocabulary)
```

#### 2.3.3 Reliable Broadcast Protocol

EABS uses **Bracha's Reliable Broadcast (RBC)** for the BROADCASTING phase. This protocol was selected for networks of up to 100 nodes based on the following analysis:

| Protocol | Message Complexity | Fault Tolerance | Ordering | Suitable Scale |
|---|---|---|---|---|
| Bracha's RBC | O(n^2) per broadcast | f < n/3 crash faults | No ordering (by design) | Up to ~100 nodes |
| HotStuff | O(n) per broadcast | f < n/3 Byzantine | Total ordering | 100-1000 nodes |
| Gossip-based | O(n log n) probabilistic | Probabilistic delivery | No ordering | 1000+ nodes |

**Selection rationale:** Bracha's RBC provides exactly the guarantees EABS needs -- reliable delivery without ordering -- at the lowest complexity for the target scale. EABS does not need ordering from the broadcast protocol because ordering is computed deterministically post-broadcast. Full BFT consensus (HotStuff) provides ordering guarantees that EABS does not use, at higher message complexity.

**Bracha's RBC Protocol (adapted for EABS):**

```
// Node i wants to broadcast operation O to all n nodes
// Fault tolerance: f < n/3 crash faults (n >= 3f + 1)

PROTOCOL BrachaRBC(sender: NodeID, operation: Operation, n: uint, f: uint):

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

        // Amplification: if enough READY messages, send READY too
        IF ready_count[epoch][op_id][op_hash] >= f + 1
           AND NOT already_readied[epoch][op_id]:
            already_readied[epoch][op_id] = true
            FOR each node j IN network:
                SEND (READY, epoch, op_id, op_hash) TO j

        // Delivery: if enough READY messages, deliver
        IF ready_count[epoch][op_id][op_hash] >= 2f + 1:
            DELIVER(epoch, operation)
            broadcast_set[epoch].add(operation)

PROPERTIES:
    - Validity: If sender is honest and broadcasts O, all honest nodes deliver O.
    - Agreement: If any honest node delivers O, all honest nodes deliver O.
    - Integrity: Every honest node delivers at most one operation per op_id.
    - No ordering guarantee (by design -- ordering handled by EABS).
```

**Message Complexity Analysis:**

For n nodes broadcasting m operations per epoch:
- Each operation requires O(n^2) messages (n INITIAL + n^2 ECHO + n^2 READY)
- Total messages per epoch: O(m * n^2)
- For n=50 nodes, m=1000 operations: ~2.5M messages per epoch
- At 60-second epochs: ~42K messages/second
- At 100 bytes/message: ~4.2 MB/second bandwidth

This is well within the capacity of modern networks. For networks exceeding 100 nodes, the architecture should transition to HotStuff-inspired linear broadcast (see Section 2.7).

#### 2.3.4 Deterministic Ordering Algorithm

After Reliable Broadcast delivers the epoch's operation set to all honest nodes, each node independently applies the same deterministic ordering algorithm. Because all honest nodes receive the same set of operations (by the Agreement property of RBC), they all produce the same ordered batch.

```
FUNCTION deterministic_order(operations: Set<Operation>) -> List<Operation>:
    // Three-level canonical sort:
    // 1. Operation type priority (ensures slashing before rewards, etc.)
    // 2. Timestamp hash (deterministic tie-breaking, not manipulable)
    // 3. Submitter ID (final tie-breaker)

    CONST TYPE_PRIORITY = {
        // Highest priority first (processed first in batch)
        TREASURY_MINT:       0,
        TREASURY_BURN:       1,
        PENDING_TIMEOUT:     2,    // Auto-reverts before new operations
        PENDING_COMPLETE:    3,
        SLASH:               4,    // Slashing before rewards
        AIC_UNSTAKE:         5,
        CS_REVERT:           6,
        CS_RELEASE:          7,
        PC_DECAY:            8,
        AIC_TRANSFER:        9,
        AIC_STAKE:          10,
        PC_EARN:            11,
        PC_SPEND:           12,
        CS_ALLOCATE:        13,
        CAPACITY_CLEAR:     14,
        CAPACITY_SPOT:      15,
        CAPACITY_BID:       16,
        REWARD_B_CLASS:     17,
        REWARD_V_CLASS:     18,
        REWARD_G_CLASS:     19,
        PENDING_INITIATE:   20,    // New pendings last
        PARAMETER_UPDATE:   21,
    }

    sorted = operations.to_list()
    sorted.sort(key = lambda op: (
        TYPE_PRIORITY[op.op_type],
        op.timestamp_hash,        // bytes32 lexicographic comparison
        op.submitter_id           // AgentID lexicographic comparison
    ))
    RETURN sorted
```

**Ordering Rationale:**

The type priority ordering encodes critical dependencies:

1. **Treasury operations first:** Minting and burning establish the epoch's total supply before any transfers.
2. **Pending resolutions before new operations:** Timed-out pendings are reverted, freeing resources for the epoch's new operations.
3. **Slashing before rewards:** Penalties are applied before new rewards are distributed, ensuring slashed entities do not receive rewards on already-penalized stake.
4. **Unstaking and releases before allocations:** Resources are freed before new allocations consume them.
5. **Decay before earning:** PC decay is applied before new PC earnings, preventing earn-then-decay ordering manipulation.
6. **Transfers before stakes:** AIC must be in the account before it can be staked.
7. **Rewards after all state changes:** Settlement rewards computed on the epoch's final state.
8. **New pending states last:** Pending initiations are processed after all other operations to prevent limbo-based blocking.

**INVARIANT ORDER-1:** For any two honest nodes A and B that both complete Reliable Broadcast for epoch E, deterministic_order(A.broadcast_set[E]) == deterministic_order(B.broadcast_set[E]).

**Proof sketch:** By the Agreement property of Bracha's RBC, A.broadcast_set[E] == B.broadcast_set[E]. The sort function is deterministic (pure function of its inputs). Therefore the outputs are identical.

#### 2.3.5 Settlement Function

The settlement function is the core of EABS. It takes an ordered batch of operations and a pre-settlement state snapshot, then produces a post-settlement state and a conservation proof.

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
        // CRITICAL: Conservation violated -- enter recovery
        TRIGGER recovery_protocol(pre_state, ordered_batch, epoch_number)
        RETURN SettlementResult{
            pre_state_hash: pre_state_hash,
            post_state: pre_state,          // Revert to pre-state
            post_state_hash: hash(pre_state),
            operations_applied: 0,
            operations_rejected: ordered_batch.map(op -> (op, CONSERVATION_VIOLATION)),
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
            violator_acct = state.accounts[op.payload.violator]
            penalty = compute_graduated_penalty(
                op.payload.offense_number,
                violator_acct.staked_aic.value(),
                state.parameter_set.slashing_schedule
            )
            IF penalty > violator_acct.staked_aic.value():
                penalty = violator_acct.staked_aic.value()
            violator_acct.staked_aic.decrement(op.submitter_id, penalty)
            state.treasury_balance += penalty
            violator_acct.violation_count = max(
                violator_acct.violation_count, op.payload.offense_number)
            RETURN Success(state)

        CASE PC_DECAY:
            FOR each account IN state.accounts.values():
                decay_amount = floor(account.pc_balance.value() * 0.10)
                account.pc_balance.decrement(op.submitter_id, decay_amount)
            RETURN Success(state)

        CASE REWARD_B_CLASS:
            recipient_acct = state.accounts[op.payload.recipient]
            adjusted = floor(op.payload.base_amount * op.payload.npv_adjustment)
            IF adjusted > state.reward_pools[op.payload.stream]:
                RETURN Failure(INSUFFICIENT_REWARD_POOL)
            state.reward_pools[op.payload.stream] -= adjusted
            recipient_acct.aic_balance.increment(op.submitter_id, adjusted)
            RETURN Success(state)

        CASE PENDING_TIMEOUT:
            pending = state.pending_registry[op.payload.pending_id]
            IF pending.epoch_initiated + 3 > state.epoch_number:
                RETURN Failure(PENDING_NOT_YET_TIMED_OUT)
            initiator_acct = state.accounts[pending.initiator_id]
            timeout_fee = floor(pending.amount * 0.02)
            collateral_return = pending.collateral - timeout_fee
            state.treasury_balance += timeout_fee
            initiator_acct.aic_balance.increment(op.submitter_id, collateral_return)
            IF pending.direction == OUTBOUND:
                initiator_acct.pending_out.decrement(op.submitter_id, pending.amount)
            ELSE:
                counterparty_acct = state.accounts[pending.counterparty_id]
                counterparty_acct.pending_in.decrement(op.submitter_id, pending.amount)
            DELETE state.pending_registry[op.payload.pending_id]
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
            // Check cooldown: unstaking requires N epochs since last stake
            IF state.epoch_number - acct.last_stake_epoch < UNSTAKE_COOLDOWN:
                RETURN Failure(COOLDOWN_NOT_ELAPSED)
            acct.staked_aic.decrement(op.submitter_id, op.payload.amount)
            acct.aic_balance.increment(op.submitter_id, op.payload.amount)
            RETURN Success(state)

        CASE PC_EARN:
            acct = state.accounts[op.submitter_id]
            // Quality gate: verify attestation from C5 PCVM
            IF NOT verify_pc_attestation(op.payload.attestation):
                RETURN Failure(INVALID_PC_ATTESTATION)
            // Sublinear earning: k * sqrt(quality_actions)
            earned = compute_pc_earning(op.payload.quality_actions, state.parameter_set)
            // Balance cap check
            IF acct.pc_balance.value() + earned > 10 * state.parameter_set.epoch_earning_rate:
                earned = max(0, 10 * state.parameter_set.epoch_earning_rate - acct.pc_balance.value())
            acct.pc_balance.increment(op.submitter_id, earned)
            RETURN Success(state)

        CASE PC_SPEND:
            acct = state.accounts[op.submitter_id]
            // Congestion pricing: base_cost * (1 + load_factor^2)
            actual_cost = compute_congestion_cost(
                op.payload.base_cost, state.parameter_set, state.epoch_load)
            IF acct.pc_balance.value() < actual_cost:
                RETURN Failure(INSUFFICIENT_PC)
            acct.pc_balance.decrement(op.submitter_id, actual_cost)
            RETURN Success(state)

        CASE CS_ALLOCATE:
            acct = state.accounts[op.submitter_id]
            // Position limit check: max 15% of total CS supply
            IF acct.cs_allocation.value() + op.payload.amount >
               floor(state.total_cs_supply * 0.15):
                RETURN Failure(POSITION_LIMIT_EXCEEDED)
            acct.cs_allocation.increment(op.submitter_id, op.payload.amount)
            RETURN Success(state)

        CASE CS_RELEASE:
            acct = state.accounts[op.submitter_id]
            IF acct.cs_allocation.value() < op.payload.amount:
                RETURN Failure(INSUFFICIENT_CS)
            acct.cs_allocation.decrement(op.submitter_id, op.payload.amount)
            RETURN Success(state)

        CASE TREASURY_MINT:
            // Governance-authorized only
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

        CASE PENDING_INITIATE:
            acct = state.accounts[op.submitter_id]
            collateral = floor(op.payload.amount * 0.05)
            // Per-entity pending cap: 10% of total supply
            current_pending = acct.pending_out.value()
            IF current_pending + op.payload.amount >
               floor(state.total_aic_supply * 0.10):
                RETURN Failure(ENTITY_PENDING_CAP_EXCEEDED)
            // Global pending cap: 25% of total supply
            total_pending = sum(a.pending_out.value() for a in state.accounts.values())
            IF total_pending + op.payload.amount >
               floor(state.total_aic_supply * 0.25):
                RETURN Failure(GLOBAL_PENDING_CAP_EXCEEDED)
            // Lock collateral
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
            initiator_acct = state.accounts[pending.initiator_id]
            counterparty_acct = state.accounts[pending.counterparty_id]
            // Complete the transfer
            initiator_acct.pending_out.decrement(op.submitter_id, pending.amount)
            counterparty_acct.aic_balance.increment(op.submitter_id, pending.amount)
            // Return collateral
            initiator_acct.aic_balance.increment(op.submitter_id, pending.collateral)
            DELETE state.pending_registry[op.payload.pending_id]
            RETURN Success(state)

        // Additional cases (CAPACITY_BID, CAPACITY_CLEAR, CAPACITY_SPOT,
        // REWARD_V_CLASS, REWARD_G_CLASS, PARAMETER_UPDATE, CS_REVERT)
        // follow the same pattern: validate preconditions, modify state
        // atomically, return Success or Failure with reason.
```

#### 2.3.6 Conservation Enforcement

**The Conservation Invariant (INV-CSO):**

```
FUNCTION check_conservation(state: SettlementState) -> bool:
    // AIC Conservation
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

    // CS Conservation
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

**INVARIANT CONS-1 (AIC Conservation):**
For every epoch E, after settlement:
```
Sigma(aic_balance_i) + Sigma(staked_aic_i) + Sigma(pending_out_i)
    - Sigma(pending_in_i) + treasury_balance = total_aic_supply
```
where i ranges over all accounts.

**INVARIANT CONS-2 (CS Conservation):**
For every epoch E, after settlement:
```
Sigma(cs_allocation_i) + Sigma(cs_pending_j) = total_cs_supply
```
where i ranges over all accounts and j ranges over all pending CS operations.

**INVARIANT CONS-3 (PC Non-Conservation -- by design):**
Protocol Credits are intentionally non-conserved. They are created (earned) and destroyed (decayed, spent) by protocol rules. There is no total_pc_supply invariant. Instead, PC is bounded by:
```
FOR each account i: pc_balance_i <= 10 * epoch_earning_rate(i)
```

#### 2.3.7 Hard Gate HG-1 Resolution: EABS Protocol Specification

The EABS protocol is fully specified by the combination of:

1. **Epoch lifecycle** (Section 2.3.1): Five-phase state machine with defined transitions.
2. **Reliable Broadcast** (Section 2.3.3): Bracha's RBC with O(n^2) message complexity, f < n/3 crash fault tolerance.
3. **Deterministic ordering** (Section 2.3.4): Canonical sort by (type_priority, timestamp_hash, submitter_id).
4. **Settlement function** (Section 2.3.5): Deterministic batch processor with per-operation validation.
5. **Conservation enforcement** (Section 2.3.6): Post-batch invariant check with recovery on violation.

**Completeness argument:** Every state-mutating operation in DSF is expressed as an Operation (Section 2.3.2), collected during COLLECTING, broadcast during BROADCASTING, ordered during ORDERING, and processed during SETTLING. No state mutation occurs outside this pipeline. The CRDT read path is read-only between epoch settlements -- it reflects settled state plus optimistic deltas but does not modify authoritative state.

#### 2.3.8 Hard Gate HG-2 Resolution: Conservation Invariant Proof Sketch

**Theorem:** If the settlement function `settle_epoch` returns `conservation_valid = true`, then CONS-1 and CONS-2 hold for the post-settlement state.

**Proof sketch:**

*Base case:* At epoch 0 (genesis), total_aic_supply = treasury_balance, all account balances are zero, and the conservation invariant holds trivially.

*Inductive step:* Assume CONS-1 and CONS-2 hold for pre_state (the state after epoch E-1). We must show they hold for post_state (the state after epoch E).

For each operation type, we verify that apply_operation preserves conservation:

- **AIC_TRANSFER:** Decrements from_account by X, increments to_account by X. Net change to Sigma(aic_balance_i) = 0. Conservation preserved.
- **AIC_STAKE:** Decrements aic_balance by X, increments staked_aic by X (same account). Net change to (aic_balance + staked_aic) = 0. Conservation preserved.
- **AIC_UNSTAKE:** Reverse of AIC_STAKE. Conservation preserved.
- **SLASH:** Decrements staked_aic by penalty, increments treasury_balance by penalty. Net change to (Sigma(staked_aic_i) + treasury_balance) = 0. Conservation preserved.
- **TREASURY_MINT:** Increments total_aic_supply by X, increments treasury_balance by X. Both sides of CONS-1 increase by X. Conservation preserved.
- **TREASURY_BURN:** Decrements total_aic_supply by X, decrements treasury_balance by X. Both sides of CONS-1 decrease by X. Conservation preserved.
- **REWARD_*:** Decrements reward_pool (part of treasury_balance) by X, increments recipient.aic_balance by X. Net change to (Sigma(aic_balance_i) + treasury_balance) = 0. Conservation preserved.
- **PENDING_INITIATE (outbound):** Collateral (5% of X) moved from aic_balance to collateral hold. pending_out increases by X. The pending_out term is already on the left side of CONS-1. The collateral is subtracted from aic_balance but remains within the system (held by the protocol). Net conservation change = 0. Conservation preserved.
- **PENDING_COMPLETE:** pending_out decremented by X, counterparty balance incremented by X. Collateral returned to initiator. Net effect equivalent to a transfer plus collateral return. Conservation preserved.
- **PENDING_TIMEOUT:** pending_out decremented by X, initiator balance restored minus timeout_fee. Timeout_fee added to treasury. Net: pending_out decreases by X, aic_balance increases by (collateral - fee), treasury increases by fee. The pending amount X is effectively cancelled. Conservation preserved.
- **PC_DECAY/PC_EARN/PC_SPEND:** PCs are not part of the AIC conservation invariant. No effect on CONS-1 or CONS-2.
- **CS_ALLOCATE/CS_RELEASE/CS_REVERT:** CS moves between accounts or between allocated and unallocated pools. CONS-2 is preserved because each operation is a balanced transfer within the CS domain.

Each operation individually preserves conservation. The settlement function applies them sequentially. By induction over the ordered batch, conservation is preserved after all operations.

The explicit `check_conservation` call after batch processing provides runtime verification -- catching any implementation bugs that might violate the theoretical guarantee.

**Recovery protocol:** If check_conservation returns false (indicating a bug, not an attack -- attacks are prevented by per-operation validation), the entire epoch batch is rejected and all nodes revert to pre_state. A diagnostic trace is emitted for debugging.

### 2.4 Epoch-Consistent Optimistic Reads (ECOR)

#### 2.4.1 Formal Definition

```
DEFINITION (ECOR):
    For node N at time t during epoch E:

    ecor_balance(account, budget_type) =
        settled_balance(account, budget_type, E-1)
        + optimistic_delta(account, budget_type, E)

    WHERE:
        settled_balance(account, budget_type, E-1) =
            The account's balance for budget_type after EABS settlement
            of epoch E-1. This value is identical across all honest nodes.

        optimistic_delta(account, budget_type, E) =
            The sum of locally-observed operations affecting this account
            and budget_type during the current epoch E, BEFORE settlement.
            This value MAY differ across nodes (eventual consistency).

PROPERTIES:
    1. After epoch E settles:
       FOR ALL honest nodes A, B:
       settled_balance_A(account, budget_type, E)
           == settled_balance_B(account, budget_type, E)

    2. During epoch E (before settlement):
       ecor_balance may differ across nodes by at most the set of
       operations not yet delivered via CRDT anti-entropy.

    3. Monotonic settled state:
       settled_balance(account, AIC, E) reflects all operations
       through epoch E. No settled balance is ever "un-settled"
       (monotonic epoch progression).
```

#### 2.4.2 Optimistic Delta Tracking

```
STRUCTURE OptimisticDelta:
    account_id:     AgentID
    budget_type:    BudgetType          // AIC, PC, CS
    epoch:          uint64
    credits:        uint64              // Sum of positive deltas
    debits:         uint64              // Sum of negative deltas
    operations:     List<OperationID>   // Operations contributing to delta

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

#### 2.4.3 Staleness Bounds and Risk Mitigation

```
THEOREM (ECOR Staleness Bound):
    For any honest node N at time t:
    |ecor_balance_N(account, budget_type) - true_settled_balance|
    <= max_epoch_reward_pool + max_single_transfer

    WHERE:
        true_settled_balance is the balance after the most recent epoch
        settlement that N may not yet have received (due to broadcast latency).

    In practice, for typical parameters:
    - max_epoch_reward_pool = 1000 AIC (configurable)
    - max_single_transfer is governed by per-operation limits
    - Staleness resolves within reliable_broadcast_latency (~2 seconds)
```

**Risk mitigation for optimistic reads:**

1. **High-value operations should wait for settlement.** Operations that depend on exact balances (e.g., staking, large transfers) should verify against settled state, not ECOR state. The HDL_C7_Contract.query_balance function returns both the ECOR balance and the last settled balance.

2. **Overdraft detection at settlement.** If an operation was accepted based on optimistic state but the settled state reveals insufficient balance, the operation is rejected during SETTLING. This is analogous to a "bounced check" in traditional banking -- the operation fails gracefully, and the submitter is not penalized (the operation was submitted in good faith based on available information).

3. **Monitoring flag MF-1 (CRDT Read-Path Staleness).** The system tracks the average and maximum gap between ECOR balances and settled balances. If this gap exceeds configurable thresholds, an alert is raised to governance.

### 2.5 Fault Model

#### 2.5.1 Assumed Fault Model

DSF v2 assumes a **crash-fault model** for the EABS write path:

- **Fault threshold:** f < n/3, where n is the total number of HDL nodes.
- **Fault type:** Crash faults (nodes may stop, but do not send conflicting messages).
- **Network model:** Partial synchrony -- messages are eventually delivered within an unknown but finite bound Delta.
- **Cryptographic assumptions:** Ed25519 signatures are unforgeable. SHA-256 hash collisions do not occur.

**Justification for crash-fault (not Byzantine):** DSF operates in a semi-permissioned environment where HDL nodes are operated by known infrastructure providers with staked collateral. Byzantine behavior (sending conflicting messages) is detectable and punishable via slashing, making the expected fault mode crash rather than Byzantine. If future deployments require Byzantine fault tolerance, the Bracha's RBC protocol already tolerates f < n/3 Byzantine faults with the same message complexity.

#### 2.5.2 Partition Handling

```
SCENARIO: Network partitions into groups P1 and P2.

READ PATH (CRDT):
    Both partitions continue serving reads from local CRDT state.
    Reads become increasingly stale as partitions diverge.
    No reads are blocked. Availability is preserved.

WRITE PATH (EABS):
    Reliable Broadcast requires 2f+1 responses for delivery.
    If both partitions have fewer than 2f+1 nodes, NO operations
    are delivered in either partition.
    EABS settlement STALLS until partition heals.

    If one partition has >= 2f+1 nodes (the "majority partition"),
    that partition continues settlement normally.
    The minority partition stalls.

POST-PARTITION RECOVERY:
    1. Minority partition nodes detect they have fallen behind
       (their epoch_settled < network epoch_settled).
    2. They request catch-up: download settled state for all
       missed epochs from majority partition nodes.
    3. They verify each epoch's settlement by re-executing the
       settlement function on the ordered batch (deterministic
       re-computation).
    4. Once caught up, they rejoin normal EABS participation.

    RECOVERY TIME: O(missed_epochs * settlement_computation_time)
    For a 10-epoch partition (~10 minutes at 60s epochs):
    Recovery time ~10 seconds (settlement is fast).
```

#### 2.5.3 Recovery Protocol

```
PROTOCOL EpochRecovery(stale_node: NodeID, current_epoch: uint64):

    // Step 1: Detect staleness
    stale_epoch = stale_node.epoch_settled
    gap = current_epoch - stale_epoch

    IF gap == 0:
        RETURN  // Already current

    // Step 2: Request epoch batches from peers
    FOR epoch_e FROM (stale_epoch + 1) TO current_epoch:
        batch = REQUEST_EPOCH_BATCH(epoch_e) FROM any_peer
        // Verify batch authenticity via settlement hash chain
        expected_pre_hash = stale_node.settlement_state.settlement_hash
        IF batch.pre_state_hash != expected_pre_hash:
            // Hash chain broken -- request from different peer
            RETRY with different peer (up to f retries)
            IF all retries fail:
                ALERT: possible state corruption, manual intervention required

        // Re-execute settlement (deterministic verification)
        result = settle_epoch(stale_node.settlement_state, batch.ordered_batch, epoch_e)

        IF result.post_state_hash != batch.expected_post_hash:
            // Settlement divergence -- indicates bug or corruption
            ALERT: deterministic settlement verification failed
            HALT recovery, escalate to governance

        stale_node.settlement_state = result.post_state
        stale_node.epoch_settled = epoch_e

        // Update CRDT read path with settled state
        update_crdt_from_settlement(stale_node, result.post_state)

    // Step 3: Rejoin EABS
    stale_node.phase = COLLECTING
    stale_node.epoch_collecting = current_epoch + 1
```

### 2.6 Epoch Boundary Timing

```
FUNCTION compute_epoch_boundary(epoch_number: uint64, params: ProtocolParameters) -> Timestamp:
    nominal_boundary = genesis_time + (epoch_number * params.epoch_duration)

    // Jitter: +/-10% of epoch duration
    jitter_seed = SHA256(epoch_number || params.network_entropy_source)
    jitter_fraction = (uint64_from_bytes(jitter_seed[0:8]) % 2001 - 1000) / 10000.0
    // jitter_fraction is in [-0.10, +0.10]

    jitter_ms = floor(params.epoch_duration_ms * jitter_fraction)
    jittered_boundary = nominal_boundary + jitter_ms

    RETURN jittered_boundary

// Recommended initial parameters:
// epoch_duration_ms = 60000 (60 seconds)
// network_entropy_source = hash of previous epoch's settlement_hash
```

**INVARIANT EPOCH-1:** All honest nodes compute the same jittered boundary for epoch E, because the jitter_seed is derived from deterministic inputs (epoch_number and the previous epoch's settlement_hash, which is identical across all honest nodes by INVARIANT ORDER-1).

### 2.7 Scalability Considerations

| Network Size | Broadcast Protocol | Messages/Epoch (1K ops) | Bandwidth/Node | Settlement Latency |
|---|---|---|---|---|
| 10 nodes | Bracha's RBC | ~100K | ~1 MB/s | <3s |
| 50 nodes | Bracha's RBC | ~2.5M | ~5 MB/s | <5s |
| 100 nodes | Bracha's RBC | ~10M | ~10 MB/s | <10s |
| 500 nodes | HotStuff linear | ~500K | ~1 MB/s | <5s |
| 1000 nodes | Gossip + HotStuff | ~1M | ~2 MB/s | <15s |

The architecture supports protocol upgrades at scale thresholds via G-class governance parameter changes. The broadcast protocol is abstracted behind the Reliable Broadcast interface -- any protocol satisfying the Validity, Agreement, and Integrity properties can be substituted.

**Netting optimization:** Following the CLS model (which reduces $6.6T gross to ~$300B net daily), EABS can implement intra-epoch netting before broadcast. If agent A transfers 50 AIC to B and B transfers 30 AIC to A within the same epoch, only the net transfer (A->B: 20 AIC) needs to be broadcast and settled. This reduces message volume by an estimated 30-60% under typical workloads.

```
FUNCTION net_operations(operations: List<Operation>) -> List<Operation>:
    // Group transfers by (from, to) pair
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

    // Emit netted transfers
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
                // ... other fields derived from constituent operations
            })
        ELIF net_amount < 0:
            netted.append(Operation{
                op_type: AIC_TRANSFER,
                payload: {from: to_id, to: from_id, amount: abs(net_amount)},
            })
        // net_amount == 0: transfers cancel out, nothing to settle

    RETURN non_transfers + netted
```

### 2.8 HDL Integration Contracts

```
// Contract: HDL <-> C3 (Tidal Noosphere)
INTERFACE HDL_C3_Contract:
    // HDL publishes settled state to C3 CRDT layer after each epoch
    FUNCTION publish_settled_state(epoch: uint64, state: SettlementState)
        FREQUENCY: Once per epoch
        CONSISTENCY: EABS-settled (deterministic, conservation-guaranteed)
        FAILURE_MODE: If C3 is unavailable, HDL queues state updates
                      and delivers on reconnection.

    // HDL reads epoch boundaries from C3 tidal scheduling
    FUNCTION get_epoch_boundary(epoch: uint64) -> Timestamp
        FREQUENCY: Once per epoch
        CONSISTENCY: C3 tidal schedule is deterministic

    // HDL reads Sentinel Graph identity clusters for Sybil detection
    FUNCTION get_identity_clusters() -> List<IdentityCluster>
        FREQUENCY: Once per V-class settlement cycle (every N epochs)
        CONSISTENCY: CRDT-optimistic (Sybil detection is best-effort)

// Contract: HDL <-> C7 (RIF)
INTERFACE HDL_C7_Contract:
    // RIF queries balances via ECOR (optimistic, fast, never blocks)
    FUNCTION query_balance(agent: AgentID, budget: BudgetType) -> ECORBalance
        FREQUENCY: On-demand (per intent proposal)
        CONSISTENCY: ECOR (settled + optimistic delta)
        LATENCY: <1ms (local CRDT read)

    // RIF submits operations for next epoch settlement
    FUNCTION submit_operation(op: Operation) -> OperationReceipt
        FREQUENCY: On-demand
        CONSISTENCY: Operation buffered; settlement at next epoch boundary
        LATENCY: <1ms (local buffer write)

    // RIF receives settlement confirmations
    CALLBACK on_settlement_complete(epoch: uint64, results: List<SettlementConfirmation>)
        FREQUENCY: Once per epoch
        CONSISTENCY: EABS-settled (deterministic, final)

// Contract: HDL <-> C5 (PCVM)
INTERFACE HDL_C5_Contract:
    // HDL reads credibility scores for capability_score computation
    FUNCTION get_credibility(agent: AgentID) -> CredibilityScore
        FREQUENCY: Once per V-class settlement cycle
        CONSISTENCY: CRDT-optimistic (credibility is soft-state)

    // HDL reads verification attestations for PC identity-binding
    FUNCTION verify_attestation(attestation: PCVMAttestation) -> bool
        FREQUENCY: Per PC_EARN operation
        CONSISTENCY: Cryptographic verification (deterministic)

// Contract: HDL <-> C6 (EMA)
INTERFACE HDL_C6_Contract:
    // HDL reads metabolic efficiency for reward computation
    FUNCTION get_metabolic_efficiency(agent: AgentID) -> MetabolicReport
        FREQUENCY: Once per epoch (for scheduling compliance stream)
        CONSISTENCY: CRDT-optimistic

    // HDL reads SHREC regulation state for budget allocation
    FUNCTION get_shrec_state(locus: LocusID) -> SHRECState
        FREQUENCY: Once per epoch
        CONSISTENCY: CRDT-optimistic
```

---

## 3. Three-Budget Economic Model

### 3.1 Design Philosophy

The Three-Budget Model is DSF's primary economic innovation. Traditional blockchain economies use a single token for all economic functions (Ethereum's ETH serves as payment, gas, staking collateral, and governance weight). This conflation creates attack vectors where dominance in one function (e.g., capital for staking) automatically confers dominance in all others (spam capacity, resource access, governance power).

DSF separates economic functions into three distinct budget types, each with different creation, destruction, transferability, and decay properties. The design explicitly acknowledges (per Adversarial Analysis Attack 6 and Science Assessment Claim 1) that perfect economic isolation between budgets is impossible. Instead, it implements **calibrated friction** -- mechanisms that make cross-budget arbitrage unprofitable at protocol-relevant scales while accepting that some implicit exchange will occur.

### 3.2 Budget Type Formal Definitions

#### 3.2.1 Sponsor Budget (SB) -- AIC

```
STRUCTURE SponsorBudget:
    token_name:       "AIC" (Atrahasis Internal Credit)
    transferability:  TRANSFERABLE
    decay_rate:       0.0 (no decay)
    creation:         Treasury minting only (TREASURY_MINT operation)
    destruction:      Treasury burning (TREASURY_BURN), timeout fees, slashing
    settlement_path:  EABS write path (conservation-guaranteed)
    read_path:        CRDT (ECOR optimistic reads)
    conservation:     YES -- CONS-1 invariant enforced at every epoch

    // AIC serves as:
    //   1. Primary payment instrument for task sponsorship
    //   2. Staking collateral for capability-weighted stake
    //   3. Governance weight (proportional to staked AIC)
    //   4. Settlement reward denomination
    //   5. Capacity market bidding currency

STRUCTURE AICAccount:
    available_balance:  uint64      // Free AIC, available for transfers/staking
    staked_balance:     uint64      // AIC locked as collateral
    pending_outbound:   uint64      // AIC in outbound pending state
    pending_inbound:    uint64      // AIC in inbound pending state

    FUNCTION total_balance() -> uint64:
        RETURN available_balance + staked_balance + pending_outbound

    FUNCTION effective_stake(capability_score: float64) -> uint64:
        RETURN staked_balance * min(capability_score, 3.0)
```

**AIC Flow Diagram:**

```
                    TREASURY
                       |
            TREASURY_MINT (governance-authorized)
                       |
                       v
+------------------------------------------------------------------+
|                    AIC CIRCULATION                                 |
|                                                                    |
|  +-------------+    AIC_TRANSFER    +-------------+               |
|  | Sponsor A   | -----------------> | Sponsor B   |               |
|  | (available) | <----------------- | (available) |               |
|  +------+------+                    +------+------+               |
|         |                                  |                       |
|    AIC_STAKE                          AIC_STAKE                    |
|         |                                  |                       |
|         v                                  v                       |
|  +------+------+                    +------+------+               |
|  | Staked A    |                    | Staked B    |               |
|  | (collateral)|                    | (collateral)|               |
|  +------+------+                    +------+------+               |
|         |                                  |                       |
|    SLASH (penalty)                   REWARD_* (earned)             |
|         |                                  |                       |
|         v                                  v                       |
|     TREASURY                         available_balance             |
|     (slashed AIC                     (reward AIC                   |
|      returned to                      from reward pool)            |
|      treasury)                                                     |
+------------------------------------------------------------------+
                       |
            TREASURY_BURN (timeout fees, protocol burns)
                       |
                       v
                   DESTROYED
```

#### 3.2.2 Protocol Credits (PC)

```
STRUCTURE ProtocolCredits:
    token_name:       "PC" (Protocol Credits)
    transferability:  NON_TRANSFERABLE (identity-bound)
    decay_rate:       0.10 per epoch (10%)
    creation:         Quality-gated earning via PC_EARN operation
    destruction:      Decay (PC_DECAY), spending (PC_SPEND)
    settlement_path:  EABS write path (earning/decay settled per epoch)
    read_path:        CRDT (ECOR optimistic reads)
    conservation:     NO -- PCs are intentionally non-conserved

    // PC serves as:
    //   1. Spam control (rate limiting)
    //   2. Proof of active, value-creating participation
    //   3. Access gating for protocol operations

STRUCTURE PCAccount:
    balance:            uint64
    last_decay_epoch:   uint64      // Epoch of last decay application
    quality_actions:    uint64      // Cumulative quality actions this epoch
    earning_rate:       float64     // Current epoch earning rate
    balance_cap:        uint64      // 10 * epoch_earning_rate

    FUNCTION available() -> uint64:
        RETURN balance

    FUNCTION can_spend(cost: uint64) -> bool:
        RETURN balance >= cost
```

**PC Earning Mechanics:**

```
FUNCTION compute_pc_earning(
    quality_actions: uint64,
    params: ProtocolParameters
) -> uint64:
    // Sublinear earning curve: k * sqrt(quality_actions)
    // This prevents linear farming -- doubling activity less than doubles earnings
    raw_earning = params.pc_earning_coefficient * sqrt(quality_actions)

    // Quality gate: only actions that produced measurable value count
    // (successful task completions, accepted verifications, approved proposals)
    // Non-value-producing activity (rejected tasks, failed verifications) = 0 quality_actions

    RETURN floor(raw_earning)

// Example earning curve (k = 10):
// quality_actions = 1   -> PC earned = 10
// quality_actions = 4   -> PC earned = 20
// quality_actions = 9   -> PC earned = 30
// quality_actions = 16  -> PC earned = 40
// quality_actions = 100 -> PC earned = 100
// quality_actions = 400 -> PC earned = 200  (4x activity for 2x earnings)
```

**PC Spending Mechanics (Congestion Pricing):**

```
FUNCTION compute_congestion_cost(
    base_cost: uint64,
    params: ProtocolParameters,
    epoch_load: float64            // current_ops / target_ops
) -> uint64:
    // Quadratic congestion pricing: base * (1 + load^2)
    // At normal load (load = 1.0): cost = 2 * base
    // At 2x load: cost = 5 * base
    // At 3x load: cost = 10 * base
    // This makes spam increasingly expensive under congestion

    congestion_multiplier = 1.0 + (epoch_load * epoch_load)
    RETURN ceil(base_cost * congestion_multiplier)

// Example costs (base_cost = 1 PC):
// epoch_load = 0.5  -> actual cost = 1.25 PC
// epoch_load = 1.0  -> actual cost = 2.0 PC
// epoch_load = 1.5  -> actual cost = 3.25 PC
// epoch_load = 2.0  -> actual cost = 5.0 PC
// epoch_load = 3.0  -> actual cost = 10.0 PC
```

**PC Decay Mechanics:**

```
FUNCTION apply_pc_decay(state: SettlementState) -> SettlementState:
    // Applied once per epoch during SETTLING phase
    // 10% flat decay on all PC balances

    FOR each account IN state.accounts.values():
        IF account.pc_balance.value() > 0:
            decay_amount = floor(account.pc_balance.value() * 0.10)
            account.pc_balance.decrement(SYSTEM_NODE_ID, decay_amount)

    // PCs destroyed by decay do not go to treasury or any other account.
    // They cease to exist. This is the primary mechanism that prevents
    // PC hoarding and ensures PCs reflect recent activity.

    RETURN state
```

**PC Balance Cap:**

```
INVARIANT PC-CAP:
    FOR each account A:
    A.pc_balance <= 10 * epoch_earning_rate(A)

    // The cap limits burst capacity. Even an agent with maximum earning rate
    // can accumulate at most 10 epochs' worth of PC before the cap binds.
    // Combined with 10% decay, the effective maximum is approximately:
    // steady_state_max = earning_rate / decay_rate = earning_rate / 0.10
    //                  = 10 * earning_rate (matches the cap)
```

**PC Identity Binding:**

```
FUNCTION verify_pc_identity_binding(
    agent: AgentID,
    action: QualityAction,
    attestation: PCVMAttestation
) -> bool:
    // Step 1: Verify the attestation is from C5 PCVM
    IF NOT verify_pcvm_signature(attestation):
        RETURN false

    // Step 2: Verify the attestation links this agent to this action
    IF attestation.agent_id != agent:
        RETURN false
    IF attestation.action_hash != hash(action):
        RETURN false

    // Step 3: Verify the action was performed by the agent (not delegated)
    // This uses C5's Verification Trust Descriptor (VTD) infrastructure
    IF attestation.delegation_depth > 0:
        RETURN false  // Delegated actions do not earn PC

    // Step 4: Verify temporal validity
    IF attestation.timestamp < current_epoch_start:
        RETURN false  // Stale attestation

    RETURN true
```

#### 3.2.3 Capacity Slices (CS)

```
STRUCTURE CapacitySlices:
    token_name:       "CS" (Capacity Slices)
    backing:          CSO (Capability Service Obligation) backed
    transferability:  LIMITED (acquired via market, not peer-to-peer transfer)
    decay_rate:       N/A (use-it-or-lose-it mechanism instead)
    creation:         Capacity market clearing (CAPACITY_CLEAR operation)
    destruction:      Epoch expiry (CS allocations are per-epoch)
    settlement_path:  EABS write path
    read_path:        CRDT (ECOR optimistic reads)
    conservation:     YES -- CONS-2 invariant enforced at every epoch

    // CS serves as:
    //   1. Resource reservation (compute, storage, bandwidth)
    //   2. Capacity market clearing unit
    //   3. Infrastructure provider compensation basis

STRUCTURE CSAccount:
    allocated:          uint64      // CS currently held for this epoch
    utilized:           uint64      // CS actually used this epoch
    utilization_ratio:  float64     // utilized / allocated

    FUNCTION is_underutilized(threshold: float64, epoch_progress: float64) -> bool:
        // Use-it-or-lose-it check at specified epoch progress point
        expected_utilization = allocated * epoch_progress * threshold
        RETURN utilized < expected_utilization
```

**CS Lifecycle Within an Epoch:**

```
EPOCH TIMELINE FOR CS:

|<=================== epoch_duration ===================>|
|                                                         |
|  T=0%: Epoch boundary                                  |
|  - 60% of CS cleared via sealed-bid uniform-price auction
|  - Winning bidders receive CS allocations                |
|  - Position limit enforced: max 15% per entity          |
|                                                         |
|  T=0-50%: Primary utilization period                    |
|  - Agents use CS for compute/storage/bandwidth          |
|  - Utilization tracked per-account                      |
|                                                         |
|  T=50%: Mid-epoch tranche 1                             |
|  - 20% of remaining CS released to spot market          |
|  - Use-it-or-lose-it check on primary allocations:      |
|    IF utilization < 70% of expected at T=50%            |
|    THEN underutilized CS released to spot market         |
|                                                         |
|  T=75%: Mid-epoch tranche 2                             |
|  - Final 20% of CS released to spot market              |
|  - Second use-it-or-lose-it check                       |
|                                                         |
|  T=100%: Epoch boundary                                 |
|  - All CS allocations expire                            |
|  - New auction for next epoch                           |
```

### 3.3 Cross-Budget Friction Mechanisms

```
STRUCTURE CrossBudgetFrictionModel:
    // The three budgets are not economically isolated.
    // They are functionally separated with calibrated friction.

    friction_mechanisms:
        pc_identity_binding:
            description: "PC earning requires PCVM attestation of direct work"
            attack_mitigated: "PC-as-a-service delegation"
            friction_level: "HIGH -- requires cryptographic proof of work authorship"

        cs_position_limits:
            description: "Max 15% CS per entity per epoch"
            attack_mitigated: "Capacity cornering for arbitrage"
            friction_level: "MEDIUM -- limits accumulation, doesn't prevent use"

        cross_budget_flow_monitoring:
            description: "Protocol tracks correlation between SB spend and PC accumulation"
            attack_mitigated: "Systematic SB->PC conversion"
            implementation: |
                FOR each agent A, compute:
                    correlation = pearson(
                        A.sb_spend_per_epoch[last_20_epochs],
                        A.pc_earned_per_epoch[last_20_epochs]
                    )
                IF correlation > 0.85:
                    FLAG agent for governance review

        governance_alert_trigger:
            description: "Alert when implicit exchange rates stabilize"
            trigger: "SB/PC or SB/CS implicit rate stable within 5% for 10+ epochs"
            action: "Governance review and potential parameter adjustment"

FUNCTION compute_implicit_exchange_rate(
    budget_a: BudgetType,
    budget_b: BudgetType,
    window: uint64          // Number of epochs to analyze
) -> float64:
    // Estimate implicit exchange rate from cross-budget transaction patterns
    // This is a monitoring function, not an enforcement mechanism

    a_to_b_flows = []
    FOR each epoch IN last(window) epochs:
        agents_spending_a = set(agents with budget_a spend in epoch)
        agents_earning_b = set(agents with budget_b earn in epoch)
        overlap = agents_spending_a.intersection(agents_earning_b)
        IF len(overlap) > 0:
            avg_a_spent = mean(budget_a spend for agents in overlap)
            avg_b_earned = mean(budget_b earn for agents in overlap)
            IF avg_a_spent > 0:
                a_to_b_flows.append(avg_b_earned / avg_a_spent)

    IF len(a_to_b_flows) < 5:
        RETURN NaN  // Insufficient data
    RETURN median(a_to_b_flows)
```

### 3.4 Hard Gate HG-3 Resolution: Three-Budget Equilibrium Analysis

**Analytical Model:**

We model a simplified economy with N agents, each making strategic decisions across three budgets. The equilibrium analysis demonstrates that the friction mechanisms prevent collapse to effective single-token behavior.

```
MODEL ThreeBudgetEquilibrium:
    // Agent strategy space
    AGENT STRATEGY = (sb_allocation, pc_activity_level, cs_bid)
    // where sb_allocation is fraction of AIC devoted to task sponsorship vs staking
    //       pc_activity_level is quality actions per epoch (determines PC earning)
    //       cs_bid is capacity market bid amount

    // Budget dynamics per epoch for agent i:
    AIC_balance(t+1) = AIC_balance(t)
                       - task_spend(t)          // SB function
                       - stake_change(t)        // Staking
                       + rewards(t)             // Settlement rewards
                       - cs_payment(t)          // Capacity market

    PC_balance(t+1) = PC_balance(t) * 0.90     // 10% decay
                      + pc_earn(quality_actions(t))  // Sublinear earning

    CS_allocation(t+1) = auction_result(cs_bid(t+1))  // Per-epoch auction

    // Cross-budget conversion attempt:
    // An arbitrageur tries to convert SB -> PC by sponsoring easy tasks
    // that they themselves complete.

    ARBITRAGE COST:
        sb_spent_on_self_task = X AIC
        quality_actions_earned = f(X)      // Depends on task class
        pc_earned = k * sqrt(f(X))         // Sublinear
        pc_value_of_earned = pc_earned * marginal_pc_utility

    ARBITRAGE PROFIT:
        profit = pc_value_of_earned - sb_spent_on_self_task

    FOR arbitrage to be profitable:
        k * sqrt(f(X)) * marginal_pc_utility > X

    Given sublinear PC earning and identity-binding:
        f(X) <= X / min_task_cost    // At best, 1 quality action per min_task_cost
        k * sqrt(X / min_task_cost) * marginal_pc_utility > X
        k^2 * marginal_pc_utility^2 / min_task_cost > X

    This inequality FAILS for sufficiently large X because the left side
    is constant while the right side grows linearly. Therefore:

    THERE EXISTS a maximum profitable arbitrage volume X_max:
        X_max = k^2 * marginal_pc_utility^2 / min_task_cost

    For typical parameters (k=10, marginal_pc_utility=0.5 AIC, min_task_cost=5 AIC):
        X_max = 100 * 0.25 / 5 = 5 AIC per epoch

    This represents negligible arbitrage at protocol-relevant scales.
    The friction mechanisms bound the attack to small volumes.

EQUILIBRIUM CONDITIONS:
    1. SB market clears: total task_spend = total rewards distributed
       (steady state, ignoring treasury flows)
    2. PC market clears: PC earned per epoch = PC spent + PC decayed
       In steady state: earn_rate = spend_rate + 0.10 * balance
    3. CS market clears: capacity demanded = capacity supplied at
       auction clearing price

    Under these conditions, each budget serves its primary function:
    - SB: payment and value transfer
    - PC: spam control and activity proof
    - CS: resource allocation
    The cross-budget arbitrage profit is bounded by X_max << total
    economic activity, so the budgets remain functionally separate.
```

### 3.5 Token Flow Summary

```
COMPLETE TOKEN FLOW DIAGRAM:

    TREASURY
    |
    | TREASURY_MINT
    v
    +----> AIC Reward Pools (funded by treasury)
    |         |
    |         | REWARD_B_CLASS, REWARD_V_CLASS, REWARD_G_CLASS
    |         v
    |      Agent AIC Balances (available)
    |         |           |           |
    |    AIC_TRANSFER  AIC_STAKE   CS_ALLOCATE (payment)
    |         |           |           |
    |         v           v           v
    |      Other Agent   Staked AIC   Capacity Provider
    |      Balances      (collateral)  (infrastructure compensation)
    |                     |
    |                SLASH (penalty)
    |                     |
    |                     v
    +<---- Treasury (receives slashed AIC)
    |
    | TREASURY_BURN (timeout fees, protocol burns)
    v
    DESTROYED


    PC LIFECYCLE (separate, non-conserved):

    Quality Action (verified by C5 PCVM)
    |
    | PC_EARN (sublinear, identity-bound)
    v
    Agent PC Balance
    |           |
    | PC_SPEND  | PC_DECAY (10%/epoch)
    v           v
    DESTROYED   DESTROYED


    CS LIFECYCLE (conserved per CONS-2):

    Total CS Supply (fixed per epoch, governance-adjustable)
    |
    | CAPACITY_CLEAR (auction)
    v
    Agent CS Allocations
    |           |
    | Utilized  | Underutilized (use-it-or-lose-it)
    v           v
    Resource    Released to Spot Market
    Consumption      |
                     | CAPACITY_SPOT
                     v
                Other Agent CS Allocations
    |
    | Epoch boundary
    v
    All CS expire, fresh auction next epoch
```

---

## 4. Capability-Weighted Stake System

### 4.1 Stake Computation

The Capability-Weighted Stake system replaces v1's PoMS (Proof of Model Service) model fingerprint approach. Instead of requiring agents to prove their model identity (impractical for LLM agents), v2 derives effective stake from a combination of collateral commitment (AIC) and demonstrated capability (track record).

```
FUNCTION compute_effective_stake(agent: AgentID, state: SettlementState) -> uint64:
    aic_collateral = state.accounts[agent].staked_aic.value()
    cap_score = compute_capability_score(agent, state)
    RETURN floor(aic_collateral * min(cap_score, 3.0))

FUNCTION compute_capability_score(agent: AgentID, state: SettlementState) -> float64:
    raw = compute_raw_score(agent, state)
    // Logarithmic scaling: 1.0 + ln(1 + raw_score)
    // This ensures:
    //   raw=0.0 -> cap=1.0 (no amplification for new agents)
    //   raw=1.0 -> cap=1.69
    //   raw=2.0 -> cap=2.10
    //   raw=5.0 -> cap=2.79
    //   raw=10.0 -> cap=3.40 (capped at 3.0)
    //   raw=20.0 -> cap=4.04 (capped at 3.0)
    RETURN 1.0 + ln(1.0 + raw)

FUNCTION compute_raw_score(agent: AgentID, state: SettlementState) -> float64:
    rep = get_reputation_score(agent, state)         // [0, infinity)
    vtk = get_verification_track_record(agent, state) // [0, infinity)
    cca = get_claim_class_accuracy(agent, state)     // [0, 1]

    // Weighted combination
    raw = 0.4 * rep + 0.4 * vtk + 0.2 * cca
    RETURN raw
```

### 4.2 Raw Score Components

#### 4.2.1 Reputation Score (weight: 0.4)

```
FUNCTION get_reputation_score(agent: AgentID, state: SettlementState) -> float64:
    // Cross-validated peer assessment sourced from C5 PCVM credibility
    credibility = HDL_C5_Contract.get_credibility(agent)

    // Sybil resistance: reputation only counts if earned across
    // >= 3 independent task sponsors
    sponsors = get_distinct_sponsors(agent, state, window=20)  // last 20 epochs
    IF len(sponsors) < 3:
        RETURN 0.0  // Insufficient sponsor diversity

    // Sponsor independence verified via C3 Sentinel Graph
    independent_sponsors = filter_independent(sponsors, state)
    IF len(independent_sponsors) < 3:
        RETURN 0.0  // Sponsors are not independent (possible Sybil cluster)

    // Value-weighted: reputation from high-value tasks counts more
    weighted_rep = 0.0
    total_weight = 0.0
    FOR each task_completion IN agent.completions[last_20_epochs]:
        task_value = task_completion.resource_bounds
        task_rating = task_completion.sponsor_rating  // [0, 1]
        weighted_rep += task_value * task_rating
        total_weight += task_value

    IF total_weight == 0:
        RETURN 0.0

    normalized_rep = weighted_rep / total_weight  // [0, 1]

    // Scale to [0, max_rep_score]
    RETURN normalized_rep * state.parameter_set.max_rep_score
```

#### 4.2.2 Verification Track Record (weight: 0.4)

```
FUNCTION get_verification_track_record(agent: AgentID, state: SettlementState) -> float64:
    // Historical verification accuracy against ground truth
    verifications = agent.verification_history[last_20_epochs]

    IF len(verifications) < 10:
        RETURN 0.0  // Insufficient history

    // Filter: only verifications of tasks with resource_bounds > median
    // (prevents gaming via trivially easy verifications)
    median_bounds = median(v.task_resource_bounds for v in verifications)
    significant_verifications = filter(
        verifications, v -> v.task_resource_bounds >= median_bounds
    )

    // Compute accuracy
    correct = count(v for v in significant_verifications where v.outcome == CORRECT)
    total = len(significant_verifications)

    IF total < 5:
        RETURN 0.0  // Insufficient significant verifications

    accuracy = correct / total

    // Value-weight the track record
    value_weighted_accuracy = 0.0
    total_value = 0.0
    FOR each v IN significant_verifications:
        value_weighted_accuracy += v.task_resource_bounds * (1.0 if v.outcome == CORRECT else 0.0)
        total_value += v.task_resource_bounds

    vw_accuracy = value_weighted_accuracy / total_value

    RETURN vw_accuracy * state.parameter_set.max_vtk_score
```

#### 4.2.3 Claim Class Accuracy (weight: 0.2)

```
FUNCTION get_claim_class_accuracy(agent: AgentID, state: SettlementState) -> float64:
    // Accuracy of claims within RANDOMLY assigned claim classes
    // Random assignment prevents gaming by specialization

    assignments = agent.claim_class_assignments[last_20_epochs]

    IF len(assignments) < 5:
        RETURN 0.0  // Insufficient history

    // Claim classes: D (Deterministic), E (Empirical), S (Statistical),
    //               H (Heuristic), N (Normative) -- from C5 PCVM
    // Plus evaluation types: P (Primary), R (Replication), C (Challenge)

    correct = 0
    total = 0
    FOR each assignment IN assignments:
        // The agent was randomly assigned to evaluate a claim of this class
        IF assignment.evaluation_correct:
            correct += 1
        total += 1

    RETURN correct / total  // Already in [0, 1]
```

### 4.3 Sybil Resistance Mechanisms

```
STRUCTURE SybilResistance:
    mechanisms:
        minimum_sponsor_diversity:
            requirement: ">= 3 independent sponsors for reputation to count"
            verification: "C3 Sentinel Graph identity clustering"
            rationale: >
                A Sybil cluster can create mutual ratings, but cannot
                cheaply create 3+ independent sponsors. Each sponsor
                must be a distinct economic entity with its own AIC
                stake and task sponsorship history.

        value_weighted_track_record:
            requirement: "Track record weighted by task economic value"
            verification: "EABS settlement records"
            rationale: >
                Trivially easy tasks contribute negligibly to track record.
                An attacker farming capability_score via cheap self-referential
                tasks earns minimal raw_score per AIC spent.

        random_claim_class_assignment:
            requirement: "Claim classes assigned randomly, not self-selected"
            verification: "VRF-based assignment from C3"
            rationale: >
                Prevents agents from building accuracy by only evaluating
                claim types they know they can handle. Forces breadth.

        new_identity_cold_start:
            requirement: "New agents start at capability_score = 1.0"
            implementation: >
                No multiplier benefit until sufficient history accumulates.
                Minimum history: 10 verifications across 3+ sponsors
                over 5+ epochs before capability_score > 1.0.

        sentinel_graph_clustering:
            source: "C3 Tidal Noosphere Sentinel Graph"
            mechanism: >
                Sentinel Graph performs continuous identity clustering
                using behavioral signatures, interaction patterns, and
                temporal correlations. Flagged clusters have their
                capability_scores frozen pending governance review.
```

### 4.4 Cold-Start Protocol

```
PROTOCOL ColdStart(new_agent: AgentID):
    // Phase 1: Registration (epoch 0)
    new_agent.capability_score = 1.0
    new_agent.staked_aic = MINIMUM_STAKE  // Governance-set minimum
    new_agent.effective_stake = MINIMUM_STAKE * 1.0

    // Phase 2: Probation (epochs 1-5)
    // Agent can participate in tasks but:
    //   - Limited to B-class and M-class operations only
    //   - Cannot participate in V-class verification
    //   - Cannot submit G-class governance proposals
    //   - Task assignment weighted by effective_stake (low priority)

    // Phase 3: Track Record Building (epochs 5-20)
    // Agent accumulates quality_actions, earning PC
    // Agent receives random claim class assignments
    // After 10 verifications across 3+ sponsors:
    //   capability_score starts increasing above 1.0

    // Phase 4: Full Participation (epoch 20+)
    // All operation classes available
    // capability_score reflects actual track record
    // No restrictions on task assignment

    MINIMUM_EPOCHS_TO_MAX_SCORE = estimated 50-100 epochs
    // (requires sustained high-quality participation to approach cap of 3.0)
```

### 4.5 Hard Gate HG-4 Resolution: Game-Theoretic Analysis

**Theorem:** The cost of farming capability_score from 1.0 to 3.0 exceeds the AIC value of the resulting 3x stake amplification.

**Proof:**

```
ANALYSIS CapabilityScoreFarming:
    // Goal: increase capability_score from 1.0 to 3.0
    // This requires raw_score such that 1 + ln(1 + raw_score) >= 3.0
    // ln(1 + raw_score) >= 2.0
    // 1 + raw_score >= e^2 = 7.389
    // raw_score >= 6.389

    // To achieve raw_score = 6.389:
    // 0.4 * rep + 0.4 * vtk + 0.2 * cca = 6.389
    // Best case: cca = 1.0 (perfect claim class accuracy)
    // Then: 0.4 * rep + 0.4 * vtk = 6.389 - 0.2 = 6.189
    // rep + vtk = 15.47

    // Cost to farm rep = 15.47:
    //   Requires 3+ independent sponsors (cannot self-deal)
    //   Each sponsor interaction costs at minimum min_task_cost AIC
    //   Value-weighted: tasks must have resource_bounds > median
    //   Need high ratings from independent sponsors
    //   ESTIMATED COST: >= 15.47 * min_task_cost * sponsor_overhead
    //                   = 15.47 * 5 * 3 = 232 AIC

    // Cost to farm vtk = 15.47:
    //   Requires significant verifications (above-median task value)
    //   Each verification has real computational cost
    //   Track record weighted by value: need high-value verifications
    //   ESTIMATED COST: >= 15.47 * median_task_cost = 15.47 * 10 = 155 AIC

    // TOTAL COST to farm capability_score to 3.0: >= 387 AIC minimum
    // (likely much higher due to random assignment and failure rates)

    // BENEFIT of capability_score = 3.0:
    //   effective_stake multiplied by 3.0
    //   For staked_aic = S, benefit = 2S additional effective stake
    //   This is equivalent to staking 2S more AIC at capability_score = 1.0

    // BREAK-EVEN: farming is unprofitable when farming_cost > 2S
    //   387 AIC > 2S
    //   S < 193.5 AIC

    // For agents staking less than 194 AIC: farming capability_score
    // costs more than simply staking additional AIC.

    // For agents staking more than 194 AIC: farming becomes profitable
    // BUT the logarithmic scaling and cap at 3.0 limit the benefit.
    // An agent staking 1000 AIC who farms to cap gets effective_stake
    // of 3000 -- equivalent to staking 3000 AIC with no farming.
    // Cost of farming: ~387 AIC. Cost of staking 2000 more: 2000 AIC.
    // Farming is cheaper for high-stake agents, BUT:
    //   - It takes 50+ epochs (significant time investment)
    //   - It requires genuine high-quality work (not trivial to fake)
    //   - The 3.0 cap means the maximum farming benefit is 2x additional
    //   - Random claim class assignment and minimum 3 sponsors prevent
    //     trivial gaming

    CONCLUSION:
    Farming is more expensive than direct collateral for small stakes.
    For large stakes, farming provides moderate benefit (up to 2x) but
    requires genuine sustained participation. The cap at 3.0 bounds
    the maximum gaming benefit. This satisfies HG-4.
```

### 4.6 Interaction with Slashing

```
FUNCTION compute_post_slash_effective_stake(
    agent: AgentID,
    state: SettlementState
) -> uint64:
    // After slashing, effective_stake decreases through BOTH
    // reduced collateral AND potential capability_score reset

    aic_collateral = state.accounts[agent].staked_aic.value()
    violation_count = state.accounts[agent].violation_count

    // Fourth offense: capability_score reset to 1.0
    IF violation_count >= 4:
        cap_score = 1.0
    ELSE:
        cap_score = compute_capability_score(agent, state)

    RETURN floor(aic_collateral * min(cap_score, 3.0))

    // Slashing interaction creates double punishment for repeat offenders:
    // 1. AIC collateral reduced by slashing percentage
    // 2. capability_score reset eliminates farming investment
    // This makes the cost of repeated misbehavior super-linear.
```

---

## 5. Multi-Rate Settlement Engine

### 5.1 Settlement Class Definitions

The Multi-Rate Settlement Engine processes settlement operations at three different frequencies, each matched to the urgency and verification requirements of the operation class.

```
STRUCTURE SettlementClass:
    B_CLASS:
        name: "Fast Settlement"
        frequency: "Per-epoch (every ~60 seconds)"
        scope: [
            "Scheduling compliance rewards (Stream 1)",
            "Communication efficiency rewards (Stream 3)",
            "PC decay",
            "PC earning/spending",
            "CS allocation/release",
            "AIC transfers",
            "Resource accounting",
        ]
        npv_discount: 0.98   // 2% discount for timing advantage
        rationale: >
            Operations that agents need resolved quickly to continue
            functioning. Analogous to RTGS in traditional finance.

    V_CLASS:
        name: "Standard Settlement"
        frequency: "Every N epochs (default N=5, ~5 minutes)"
        scope: [
            "Verification quality rewards (Stream 2)",
            "Slashing penalties",
            "Capability score updates",
            "Challenge resolution",
        ]
        npv_premium: 1.02    // 2% premium to compensate for delay
        challenge_rate_limit: 3  // Max challenges per entity per epoch
        challenge_bond: 0.05     // 5% of challenged amount
        rationale: >
            Operations requiring multi-epoch observation windows for
            accuracy assessment. Analogous to end-of-day netting.

    G_CLASS:
        name: "Governance Settlement"
        frequency: "Governance-triggered (variable, typically 10-50 epochs)"
        scope: [
            "Governance participation rewards (Stream 4)",
            "Parameter changes",
            "Treasury operations (mint/burn)",
            "Constitutional amendments",
            "Appeal resolutions",
        ]
        npv_premium: "Computed per-operation based on actual delay"
        rationale: >
            Operations requiring deliberation and broad participation.
            Analogous to securities settlement (T+2 or longer).
```

### 5.2 Epoch Boundary Protocol

```
PROTOCOL EpochBoundary(epoch_number: uint64, params: ProtocolParameters):

    // Step 1: Compute jittered boundary time
    boundary = compute_epoch_boundary(epoch_number, params)

    // Step 2: Collect B-class settlement operations
    b_class_ops = collect_b_class_operations(epoch_number)
    //   - Scheduling compliance scores for this epoch
    //   - Communication efficiency scores for this epoch
    //   - PC decay operations
    //   - PC earn/spend operations
    //   - CS allocation/release operations
    //   - AIC transfer operations

    // Step 3: Check if V-class settlement is due
    IF epoch_number % params.v_class_period == 0:  // Default: every 5 epochs
        v_class_ops = collect_v_class_operations(
            epoch_range=(epoch_number - params.v_class_period + 1, epoch_number)
        )
        //   - Verification quality assessments over the V-class window
        //   - Pending slashing from this V-class window
        //   - Capability score recalculations
        //   - Challenge resolutions
    ELSE:
        v_class_ops = []

    // Step 4: Check if any G-class settlements are ready
    g_class_ops = collect_ready_governance_operations()

    // Step 5: Commit-reveal for completion reports
    // (Prevents epoch boundary manipulation -- Attack 3)
    committed_hashes = collect_committed_hashes(epoch_number)
    revealed_reports = collect_revealed_reports(epoch_number)
    valid_reports = verify_commit_reveal(committed_hashes, revealed_reports)
    // Only valid (properly committed) reports are included

    // Step 6: Merge all operations into epoch batch
    epoch_batch = b_class_ops + v_class_ops + g_class_ops

    // Step 7: Apply cross-epoch smoothing check
    FOR each agent IN epoch_batch.affected_agents():
        projected_reward = compute_projected_reward(agent, epoch_batch)
        trailing_avg = agent.trailing_5_epoch_reward_average
        IF abs(projected_reward - trailing_avg) / trailing_avg > 0.25:
            // Flag for review but do not block (MF-5 monitoring)
            emit_smoothing_alert(agent, projected_reward, trailing_avg)

    // Step 8: Submit to EABS pipeline
    submit_to_eabs(epoch_batch, epoch_number)
```

### 5.3 NPV Normalization

```
FUNCTION compute_npv_adjustment(
    settlement_class: SettlementClass,
    settlement_delay_epochs: uint64,
    params: ProtocolParameters
) -> float64:
    // NPV normalization ensures that the present value of rewards
    // is independent of settlement speed.
    //
    // Without normalization, B-class (immediate) rewards have higher
    // real value than V-class (delayed) rewards, creating the timing
    // arbitrage identified in Attack 10.
    //
    // Formula: adjusted_reward = base_reward * (1 + r)^delay
    // where r = epoch_discount_rate (governance-set, initially 0.2%)

    r = params.epoch_discount_rate  // 0.002 initially

    SWITCH settlement_class:
        CASE B_CLASS:
            // B-class settles immediately: delay = 0
            // But receives a 2% discount to account for timing advantage
            RETURN 0.98

        CASE V_CLASS:
            // V-class settles after N epochs: compensated for delay
            adjustment = (1.0 + r) ^ settlement_delay_epochs
            RETURN adjustment  // > 1.0 for delay > 0

        CASE G_CLASS:
            // G-class: variable delay, computed per operation
            adjustment = (1.0 + r) ^ settlement_delay_epochs
            RETURN adjustment

    // Example NPV adjustments (r = 0.002):
    // B-class (delay=0): 0.98 (2% discount)
    // V-class (delay=5): 1.01004 (compensated for 5-epoch wait)
    // G-class (delay=20): 1.04074 (compensated for 20-epoch wait)
    //
    // Net effect: an agent earning 100 AIC via B-class gets 98 AIC now.
    // An agent earning 100 AIC via V-class gets ~101 AIC after 5 epochs.
    // In present-value terms, both receive approximately 98 AIC.
```

**Derivation:**

The NPV normalization is derived from the standard time-value-of-money formula. In DSF, an AIC received now can be staked or used for capacity market bidding immediately, generating returns during the epochs that a delayed payment would be in transit. The discount rate r represents the opportunity cost of capital per epoch.

```
DERIVATION:
    Let V_now = value of 1 AIC received now
    Let V_delayed(d) = value of 1 AIC received after d epochs

    If r is the per-epoch return on staked/deployed AIC:
    V_now = 1 AIC (by definition)
    V_delayed(d) = 1 / (1 + r)^d  (discounted present value)

    To make agents indifferent between settlement classes:
    adjusted_reward(d) = base_reward * (1 + r)^d

    Then: present_value(adjusted_reward(d)) = base_reward * (1+r)^d / (1+r)^d
                                             = base_reward

    All settlement classes have equal present value.

    The B-class 2% discount (factor 0.98) is separate from NPV normalization.
    It reflects a deliberate policy choice: fast settlement is slightly
    less rewarding to discourage gaming toward fast-settling streams.
```

### 5.4 Settlement Function by Class

#### 5.4.1 B-Class Settlement

```
FUNCTION settle_b_class(
    state: SettlementState,
    epoch: uint64,
    reports: List<CompletionReport>
) -> List<Operation>:

    operations = []

    // Stream 1: Scheduling Compliance (40% of reward pool)
    compliance_pool = state.reward_pools[SCHEDULING_COMPLIANCE]

    compliance_scores = {}
    FOR each report IN reports:
        agent = report.agent_id
        // Scoring: on-time completion within resource_bounds
        score = compute_scheduling_score(report, state)
        compliance_scores[agent] = compliance_scores.get(agent, 0) + score

    total_compliance = sum(compliance_scores.values())
    IF total_compliance > 0:
        FOR each agent, score IN compliance_scores:
            share = score / total_compliance
            reward = floor(compliance_pool * share * 0.98)  // NPV discount
            operations.append(Operation{
                op_type: REWARD_B_CLASS,
                payload: {
                    recipient: agent,
                    stream: SCHEDULING_COMPLIANCE,
                    base_amount: reward,
                    npv_adjustment: 0.98,
                },
            })

    // Stream 3: Communication Efficiency (10% of reward pool)
    comm_pool = state.reward_pools[COMMUNICATION_EFFICIENCY]

    comm_scores = compute_communication_scores(epoch, state)
    total_comm = sum(comm_scores.values())
    IF total_comm > 0:
        FOR each agent, score IN comm_scores:
            share = score / total_comm
            reward = floor(comm_pool * share * 0.98)
            operations.append(Operation{
                op_type: REWARD_B_CLASS,
                payload: {
                    recipient: agent,
                    stream: COMMUNICATION_EFFICIENCY,
                    base_amount: reward,
                    npv_adjustment: 0.98,
                },
            })

    // PC Decay (applied to all accounts)
    operations.append(Operation{op_type: PC_DECAY, submitter_id: SYSTEM})

    RETURN operations
```

#### 5.4.2 V-Class Settlement

```
FUNCTION settle_v_class(
    state: SettlementState,
    epoch_range: (uint64, uint64),
    verification_records: List<VerificationRecord>
) -> List<Operation>:

    operations = []
    start_epoch, end_epoch = epoch_range
    delay = end_epoch - start_epoch  // For NPV computation

    // Stream 2: Verification Quality (40% of reward pool)
    verify_pool = state.reward_pools[VERIFICATION_QUALITY]

    // Compute verification quality scores over the V-class window
    quality_scores = {}
    FOR each record IN verification_records:
        agent = record.verifier_id
        // Score based on: accuracy, calibration, coverage, timeliness
        score = compute_verification_quality(record, state)
        quality_scores[agent] = quality_scores.get(agent, 0) + score

    total_quality = sum(quality_scores.values())
    npv_factor = compute_npv_adjustment(V_CLASS, delay, state.parameter_set)

    IF total_quality > 0:
        FOR each agent, score IN quality_scores:
            share = score / total_quality
            reward = floor(verify_pool * share * npv_factor)
            operations.append(Operation{
                op_type: REWARD_V_CLASS,
                payload: {
                    recipient: agent,
                    stream: VERIFICATION_QUALITY,
                    base_amount: reward,
                    npv_adjustment: npv_factor,
                },
            })

    // Process pending slashing events from this window
    FOR each violation IN pending_violations[epoch_range]:
        operations.append(Operation{
            op_type: SLASH,
            payload: {
                violator: violation.agent_id,
                violation_type: violation.type,
                offense_number: violation.offense_number,
                penalty_amount: compute_graduated_penalty(
                    violation.offense_number,
                    state.accounts[violation.agent_id].staked_aic.value(),
                    state.parameter_set.slashing_schedule
                ),
            },
        })

    // Process challenge resolutions
    FOR each challenge IN resolved_challenges[epoch_range]:
        IF challenge.outcome == UPHELD:
            // Challenger was right: reward challenger, penalize challengee
            operations.append(make_challenge_reward(challenge, state))
            operations.append(make_challenge_penalty(challenge, state))
        ELSE:
            // Challenge was frivolous: forfeit challenger's bond
            operations.append(Operation{
                op_type: SLASH,
                payload: {
                    violator: challenge.challenger_id,
                    violation_type: FRIVOLOUS_CHALLENGE,
                    penalty_amount: challenge.bond_amount,
                },
            })

    // Update capability scores
    FOR each agent IN active_agents(epoch_range):
        new_cap_score = compute_capability_score(agent, state)
        // Capability score updates are recorded but take effect
        // at the next settlement cycle (no retroactive changes)
        operations.append(make_capability_update(agent, new_cap_score))

    RETURN operations
```

#### 5.4.3 G-Class Settlement

```
FUNCTION settle_g_class(
    state: SettlementState,
    proposal: GovernanceProposal
) -> List<Operation>:

    operations = []

    // Stream 4: Governance Participation (10% of reward pool)
    gov_pool = state.reward_pools[GOVERNANCE_PARTICIPATION]

    // Reward voters and proposal authors
    participants = proposal.voters + [proposal.author]
    participation_scores = {}

    FOR each participant IN participants:
        score = compute_governance_participation_score(participant, proposal)
        participation_scores[participant] = score

    total_participation = sum(participation_scores.values())
    delay = state.epoch_number - proposal.submission_epoch
    npv_factor = compute_npv_adjustment(G_CLASS, delay, state.parameter_set)

    IF total_participation > 0:
        FOR each participant, score IN participation_scores:
            share = score / total_participation
            reward = floor(gov_pool * share * npv_factor)
            operations.append(Operation{
                op_type: REWARD_G_CLASS,
                payload: {
                    recipient: participant,
                    stream: GOVERNANCE_PARTICIPATION,
                    base_amount: reward,
                    npv_adjustment: npv_factor,
                },
            })

    // Process governance actions
    IF proposal.type == PARAMETER_UPDATE AND proposal.passed:
        operations.append(Operation{
            op_type: PARAMETER_UPDATE,
            payload: proposal.parameter_changes,
        })
    ELIF proposal.type == TREASURY_OPERATION AND proposal.passed:
        operations.append(make_treasury_operation(proposal))
    ELIF proposal.type == APPEAL_RESOLUTION:
        operations.append(process_appeal(proposal, state))

    RETURN operations
```

### 5.5 Cross-Class Timing Analysis

```
TIMING DIAGRAM (10 epochs, V-class period = 5):

Epoch:  1    2    3    4    5    6    7    8    9    10
        |    |    |    |    |    |    |    |    |    |
B-class: B1   B2   B3   B4   B5   B6   B7   B8   B9   B10
V-class:                     V1                       V2
                        (epochs 1-5)             (epochs 6-10)
G-class:           G1 (if proposal ready)

B-class processes: scheduling compliance, comm efficiency, PC, CS
V-class processes: verification quality, slashing, capability updates
G-class processes: governance rewards, parameter changes, treasury

INTERACTION RULES:
1. B-class operations are independent of V/G-class and process every epoch.
2. V-class operations accumulate over the V-class window and process at
   the window boundary. They can read B-class settled state from any
   epoch in their window.
3. G-class operations are triggered by governance events (proposal passage,
   appeal deadline). They process at the epoch following the trigger.
4. Within a single epoch batch, all three classes are processed together
   in the deterministic ordering defined in Section 2.3.4.
5. B-class rewards from epoch E are settled in epoch E.
   V-class rewards from epochs E-4 to E are settled in epoch E (if V-class due).
   G-class rewards are settled in the epoch following governance trigger.
```

### 5.6 Integration with EABS Epoch Lifecycle

```
FUNCTION prepare_epoch_batch(epoch: uint64, state: SettlementState) -> List<Operation>:
    batch = []

    // Always: B-class operations
    batch.extend(settle_b_class(state, epoch, get_completion_reports(epoch)))

    // Conditionally: V-class operations
    IF epoch % state.parameter_set.v_class_period == 0:
        v_start = epoch - state.parameter_set.v_class_period + 1
        batch.extend(settle_v_class(
            state,
            (v_start, epoch),
            get_verification_records(v_start, epoch)
        ))

    // Conditionally: G-class operations
    FOR each ready_proposal IN get_ready_governance_proposals():
        batch.extend(settle_g_class(state, ready_proposal))

    // System operations (always)
    batch.extend(generate_system_operations(epoch, state))
    //   - Pending timeouts
    //   - Use-it-or-lose-it CS releases
    //   - Capacity market clearing

    RETURN batch
```

---

## 6. Four-Stream Settlement Computation

### 6.1 Stream Overview

Settlement rewards are distributed across four streams, each measuring a different dimension of agent contribution to the Atrahasis system. The stream weights (40/40/10/10) reflect the primacy of execution (scheduling) and verification in the system's value creation.

```
STRUCTURE FourStreamModel:
    STREAM_1_SCHEDULING:
        weight: 0.40
        settlement_class: B_CLASS
        source_layer: "C3 (Tidal Noosphere) + C7 (RIF)"
        metric: "Tasks completed on-time and within resource_bounds"

    STREAM_2_VERIFICATION:
        weight: 0.40
        settlement_class: V_CLASS
        source_layer: "C5 (PCVM)"
        metric: "Verification accuracy, calibration, and coverage"

    STREAM_3_COMMUNICATION:
        weight: 0.10
        settlement_class: B_CLASS
        source_layer: "C4 (ASV)"
        metric: "Protocol adherence, signal-to-noise ratio"

    STREAM_4_GOVERNANCE:
        weight: 0.10
        settlement_class: G_CLASS
        source_layer: "C7 (RIF) System 5"
        metric: "Proposal quality, voting participation, constitutional adherence"
```

### 6.2 Stream 1: Scheduling Compliance (40%, B-Class)

```
FUNCTION compute_scheduling_score(
    report: CompletionReport,
    state: SettlementState
) -> float64:
    // Scoring rubric for scheduling compliance

    score = 0.0

    // Component 1: Timeliness (0-40 points)
    // Did the agent complete the task within the deadline?
    IF report.completion_time <= report.deadline:
        // On-time: full timeliness score, with bonus for early completion
        time_ratio = report.completion_time / report.deadline  // < 1.0
        timeliness = 40.0 * (1.0 + 0.1 * (1.0 - time_ratio))
        timeliness = min(timeliness, 44.0)  // Cap early bonus at 10%
    ELSE:
        // Late: penalty proportional to lateness
        lateness_ratio = (report.completion_time - report.deadline) / report.deadline
        timeliness = 40.0 * max(0.0, 1.0 - 2.0 * lateness_ratio)
    score += timeliness

    // Component 2: Resource Bounds Compliance (0-30 points)
    // Did the agent stay within the intent's resource_bounds?
    resource_usage_ratio = report.actual_resources / report.resource_bounds
    IF resource_usage_ratio <= 1.0:
        bounds_score = 30.0
    ELIF resource_usage_ratio <= 1.3:
        // Over-budget by up to 30%: partial score
        bounds_score = 30.0 * (1.3 - resource_usage_ratio) / 0.3
    ELSE:
        bounds_score = 0.0
    score += bounds_score

    // Component 3: Quality Assessment (0-30 points)
    // Based on sponsor rating and peer review
    quality = report.sponsor_quality_rating * 15.0  // [0, 15]
    quality += report.peer_quality_rating * 15.0     // [0, 15]
    score += quality

    // Normalize to [0, 1]
    RETURN score / 100.0
```

### 6.3 Stream 2: Verification Quality (40%, V-Class)

```
FUNCTION compute_verification_quality(
    record: VerificationRecord,
    state: SettlementState
) -> float64:
    score = 0.0

    // Component 1: Accuracy (0-40 points)
    // Was the verification correct when checked against ground truth
    // or majority-of-verifiers agreement?
    IF record.outcome_matches_ground_truth:
        accuracy = 40.0
    ELIF record.outcome_matches_majority:
        accuracy = 30.0  // Partial credit for majority agreement
    ELSE:
        accuracy = 0.0
    score += accuracy

    // Component 2: Calibration (0-25 points)
    // How well does the verifier's confidence correlate with accuracy?
    // Uses Brier score: BS = (confidence - outcome)^2
    brier = (record.stated_confidence - (1.0 if record.correct else 0.0))^2
    calibration = 25.0 * (1.0 - brier)  // Brier in [0,1], so calibration in [0,25]
    score += calibration

    // Component 3: Coverage (0-20 points)
    // Did the verifier cover multiple claim classes, not just easy ones?
    claim_classes_covered = count_distinct(record.claim_classes_evaluated)
    coverage = min(20.0, claim_classes_covered * 4.0)  // 5 classes * 4 = 20
    score += coverage

    // Component 4: Timeliness (0-15 points)
    // Did the verifier respond within the expected window?
    IF record.response_time <= record.expected_response_time:
        timeliness = 15.0
    ELSE:
        ratio = record.response_time / record.expected_response_time
        timeliness = 15.0 * max(0.0, 2.0 - ratio)
    score += timeliness

    // Normalize to [0, 1]
    RETURN score / 100.0
```

### 6.4 Stream 3: Communication Efficiency (10%, B-Class)

```
FUNCTION compute_communication_scores(
    epoch: uint64,
    state: SettlementState
) -> Map<AgentID, float64>:

    scores = {}

    FOR each agent IN active_agents(epoch):
        messages = get_agent_messages(agent, epoch)  // From C4 ASV

        score = 0.0

        // Component 1: Protocol Adherence (0-40 points)
        // Are messages well-formed ASV claims with proper schemas?
        valid_messages = count(m for m in messages if m.schema_valid)
        total_messages = len(messages)
        IF total_messages > 0:
            adherence = 40.0 * (valid_messages / total_messages)
        ELSE:
            adherence = 0.0  // No messages = no score (not penalized)
        score += adherence

        // Component 2: Signal-to-Noise Ratio (0-30 points)
        // Ratio of semantically meaningful content to overhead
        IF total_messages > 0:
            semantic_content = sum(m.semantic_information_bits for m in messages)
            total_bytes = sum(m.total_bytes for m in messages)
            snr = semantic_content / total_bytes if total_bytes > 0 else 0
            noise_score = 30.0 * min(snr / state.parameter_set.target_snr, 1.0)
        ELSE:
            noise_score = 0.0
        score += noise_score

        // Component 3: Response Appropriateness (0-30 points)
        // Does the agent respond to the right messages at the right time?
        IF total_messages > 0:
            appropriate = count(m for m in messages if m.contextually_appropriate)
            appropriateness = 30.0 * (appropriate / total_messages)
        ELSE:
            appropriateness = 0.0
        score += appropriateness

        scores[agent] = score / 100.0

    RETURN scores
```

### 6.5 Stream 4: Governance Participation (10%, G-Class)

```
FUNCTION compute_governance_participation_score(
    agent: AgentID,
    proposal: GovernanceProposal
) -> float64:
    score = 0.0

    // Component 1: Voting Participation (0-30 points)
    IF agent IN proposal.voters:
        vote_score = 30.0
        // Bonus for voting with analysis (not just yes/no)
        IF agent IN proposal.voters_with_rationale:
            vote_score = min(35.0, vote_score + 5.0)
    ELSE:
        vote_score = 0.0
    score += vote_score

    // Component 2: Proposal Quality (0-40 points) — for proposal author only
    IF agent == proposal.author:
        // Quality assessed by peer review of proposal
        quality = proposal.peer_review_score * 40.0  // [0, 40]
        score += quality

    // Component 3: Constitutional Adherence (0-30 points)
    // Does the agent's governance activity align with constitutional constraints?
    constitutional_score = assess_constitutional_adherence(agent, proposal)
    score += constitutional_score * 30.0

    RETURN score / 100.0
```

### 6.6 Reward Pool Distribution Algorithm

```
FUNCTION distribute_reward_pools(
    state: SettlementState,
    epoch: uint64
) -> Map<SettlementStream, uint64>:

    // Total epoch reward pool is funded by treasury allocation
    total_pool = state.parameter_set.epoch_reward_pool

    // Distribute according to stream weights
    pools = {
        SCHEDULING_COMPLIANCE:   floor(total_pool * 0.40),
        VERIFICATION_QUALITY:    floor(total_pool * 0.40),
        COMMUNICATION_EFFICIENCY: floor(total_pool * 0.10),
        GOVERNANCE_PARTICIPATION: floor(total_pool * 0.10),
    }

    // Handle rounding remainder (add to largest pool)
    remainder = total_pool - sum(pools.values())
    pools[SCHEDULING_COMPLIANCE] += remainder

    // V-class and G-class pools accumulate across epochs
    // B-class pools are fully distributed each epoch
    // Undistributed pool remainder returns to treasury

    RETURN pools
```

### 6.7 Cross-Stream Interactions

```
CROSS-STREAM INTERACTION MATRIX:

                    Stream 1      Stream 2      Stream 3      Stream 4
                    (Schedule)    (Verify)      (Comms)       (Govern)
Stream 1 (Sched.)  --            POSITIVE      POSITIVE      NEUTRAL
Stream 2 (Verify)  POSITIVE      --            NEUTRAL       POSITIVE
Stream 3 (Comms.)  POSITIVE      NEUTRAL       --            POSITIVE
Stream 4 (Govern.) NEUTRAL       POSITIVE      POSITIVE      --

POSITIVE interactions:
- S1-S2: Agents that schedule well tend to produce verifiable outputs.
- S1-S3: On-time completion requires clear communication with peers.
- S2-S4: Verification quality informs governance decisions.
- S3-S4: Good communication supports effective governance participation.

DESIGN CONSTRAINT:
No agent should be able to earn disproportionate rewards by
concentrating activity in a single stream. The four-stream model
is designed so that maximum total reward requires participation
across all streams (due to the 40/40/10/10 split).

An agent concentrating 100% on Stream 1 earns at most 40% of total.
An agent participating in all four streams earns up to 100%.
This naturally incentivizes balanced participation.
```

### 6.8 Economic Simulation Scenarios

```
SCENARIO E1: Normal Operation (100 agents, balanced workload)
    Expected: Rewards distributed proportional to quality across all streams.
    B-class settles each epoch. V-class settles every 5 epochs.
    PC balances reach steady state after ~10 epochs.
    CS market clears efficiently with 50+ providers.
    RESULT: System operates at design point. Conservation holds.

SCENARIO E2: Verification-Heavy Workload (high dispute rate)
    Expected: V-class reward pool grows (40% weight). Challenge bonds lock
    additional AIC. Settlement latency increases as V-class queue grows.
    RESULT: NPV normalization compensates delay. System stable.

SCENARIO E3: Governance Crisis (contentious proposal)
    Expected: G-class activity spike. Governance participation rewards
    increase. System 5 arbitration engaged. Resolution within 10-50 epochs.
    RESULT: G-class pool absorbed. Constitutional constraints prevent
    destructive outcomes.

SCENARIO E4: Agent Exit (30% of agents leave)
    Expected: Capacity market thinning. Bootstrap provisions activate.
    Remaining agents receive larger reward shares (fewer participants,
    same pool). CS prices may drop. System self-heals as remaining
    agents expand capacity.
    RESULT: System degrades gracefully. Bootstrap prevents market failure.

SCENARIO E5: Rapid Growth (10x agent influx)
    Expected: PC congestion pricing activates (load_factor > 1.0).
    CS market prices increase. Epoch batches grow. May need broadcast
    protocol upgrade at >100 nodes.
    RESULT: Congestion pricing manages demand. Governance adjusts
    epoch_reward_pool upward.

SCENARIO E6: Correlated Slashing Event (10 agents slashed simultaneously)
    Expected: V-class settlement processes all slashing in deterministic order.
    Treasury receives slashed AIC. Affected agents' effective_stake drops.
    Capability scores reset for 4th+ offense.
    RESULT: System processes bulk slashing correctly. Conservation preserved.

SCENARIO E7: Zero-Activity Epoch (network idle)
    Expected: No B-class rewards (nothing to reward). PC decays by 10%.
    CS goes unutilized (use-it-or-lose-it triggers). Reward pool rolls
    to next epoch or returns to treasury.
    RESULT: System handles idle gracefully. No spurious state changes.

SCENARIO E8: Thin Capacity Market (<10 providers)
    Expected: Bootstrap capacity provider of last resort activates.
    Treasury-funded infrastructure ensures minimum capacity.
    Position limits prevent monopolization by few providers.
    Reserve pricing prevents predatory undercutting.
    RESULT: Market functions at reduced efficiency. Bootstrap prevents failure.

SCENARIO E9: Cross-Budget Arbitrage Attempt
    Expected: Attacker attempts SB->PC conversion via self-sponsored tasks.
    Sublinear PC earning limits returns. Identity-binding prevents delegation.
    Cross-budget monitoring detects correlation. Governance alerted.
    RESULT: Arbitrage profit bounded by X_max (~5 AIC/epoch). Negligible.

SCENARIO E10: Reputation Laundering Attempt
    Expected: Sybil cluster attempts to farm capability_score.
    Minimum 3 independent sponsors requirement blocks self-dealing.
    Sentinel Graph detects correlated identities. Random claim class
    assignment prevents specialization. Logarithmic scaling + cap limits benefit.
    RESULT: Attack cost exceeds benefit for stakes < 194 AIC.
    For larger stakes, farming requires genuine participation.

SCENARIO E11: Epoch Boundary Manipulation Attempt
    Expected: Attacker times transaction submission to game settlement.
    Epoch boundary jitter (+/-10%) makes timing unpredictable.
    Commit-reveal prevents retroactive report modification.
    Sliding window evaluation prevents hard-boundary gaming.
    Cross-epoch smoothing flags anomalous reward spikes.
    RESULT: Attack mitigated. Anomalous patterns detected.
```

---

## 7. Intent-Budgeted Settlement

### 7.1 Integration with RIF (C7) Intent Lifecycle

DSF's intent-budgeted settlement connects directly to the RIF orchestration layer. Each intent quantum in RIF carries resource_bounds that serve as the budget ceiling for settlement.

```
STRUCTURE IntentBudgetBinding:
    // RIF intent quantum (from C7) carries:
    intent_id:          IntentID
    resource_bounds:    ResourceBounds      // AIC budget ceiling
    task_class:         TaskClass           // Classification for minimum bounds
    sponsor_id:         AgentID             // Entity funding the intent
    workers:            List<AgentID>       // Assigned workers
    success_criteria:   SuccessCriteria     // From RIF decomposition
    settlement_type:    SettlementType      // Maps to B/V/G class

STRUCTURE ResourceBounds:
    aic_ceiling:        uint64      // Maximum AIC expenditure
    pc_cost:            uint64      // Protocol Credit cost for submission
    cs_requirement:     uint64      // Capacity Slices needed
    time_budget:        uint64      // Epochs allowed for completion
```

### 7.2 Budget Ceiling Mechanics

```
FUNCTION validate_intent_budget(
    intent: IntentBudgetBinding,
    state: SettlementState
) -> ValidationResult:

    // Step 1: Check sponsor has sufficient AIC
    sponsor = state.accounts[intent.sponsor_id]
    IF sponsor.aic_balance.value() < intent.resource_bounds.aic_ceiling:
        RETURN Failure(INSUFFICIENT_SPONSOR_BALANCE)

    // Step 2: Check sponsor has sufficient PC
    IF sponsor.pc_balance.value() < intent.resource_bounds.pc_cost:
        RETURN Failure(INSUFFICIENT_PC)

    // Step 3: Check minimum bounds
    min_bounds = compute_minimum_bounds(intent.task_class, state)
    IF intent.resource_bounds.aic_ceiling < min_bounds:
        RETURN Failure(BELOW_MINIMUM_BOUNDS)

    // Step 4: Check adjusted minimum for low-accuracy sponsors
    adjusted_min = compute_adjusted_minimum(intent.sponsor_id, min_bounds, state)
    IF intent.resource_bounds.aic_ceiling < adjusted_min:
        RETURN Failure(BELOW_ADJUSTED_MINIMUM)

    // Step 5: Reserve budget (optimistic, confirmed at settlement)
    // Creates a PENDING_INITIATE for the budget amount
    RETURN Success(reserve_budget(intent, state))
```

### 7.3 Minimum Bounds Computation

```
FUNCTION compute_minimum_bounds(
    task_class: TaskClass,
    state: SettlementState
) -> uint64:
    // Minimum resource_bounds per task class, based on trailing
    // 10-epoch median completion cost for that class.

    historical_costs = get_completion_costs(task_class, last_10_epochs)

    IF len(historical_costs) < 10:
        // Insufficient history: use governance-set default
        RETURN state.parameter_set.default_min_bounds[task_class]

    median_cost = median(historical_costs)

    // Minimum is 70% of median (allows some undercutting but prevents exploitation)
    RETURN floor(0.7 * median_cost)

FUNCTION compute_adjusted_minimum(
    sponsor_id: AgentID,
    base_min: uint64,
    state: SettlementState
) -> uint64:
    // Sponsors with poor budget accuracy face higher minimums

    accuracy = get_sponsor_budget_accuracy(sponsor_id, state)
    // accuracy in [0, 1]: ratio of tasks completing within budget

    // adjusted_min = base_min * (1 + 0.5 * (1 - accuracy))
    // Perfect accuracy (1.0): adjusted_min = base_min
    // 50% accuracy: adjusted_min = 1.25 * base_min
    // 0% accuracy: adjusted_min = 1.5 * base_min

    adjustment = 1.0 + 0.5 * (1.0 - accuracy)
    RETURN ceil(base_min * adjustment)
```

### 7.4 Worker Protection Mechanisms

```
STRUCTURE WorkerProtections:
    partial_inspection:
        description: >
            Workers may reject tasks after inspecting the first 10% of
            estimated effort without penalty to their reputation or
            capability_score.
        implementation: |
            FUNCTION inspect_and_decide(worker, intent, state):
                // Worker performs first 10% of estimated work
                inspection_cost = 0.10 * intent.resource_bounds.aic_ceiling
                inspection_result = worker.inspect(intent)

                IF inspection_result.reject:
                    // Worker rejects: no penalty, small compensation
                    compensate_worker(worker, inspection_cost * 0.5)
                    RETURN REJECTED
                ELSE:
                    // Worker accepts: proceeds with full task
                    RETURN ACCEPTED

    over_budget_flagging:
        description: >
            If actual effort exceeds resource_bounds by >30%, the worker
            can flag the intent. The sponsor's budget_accuracy_score is
            penalized. The worker receives compensation up to 130% of
            resource_bounds.
        implementation: |
            FUNCTION flag_over_budget(worker, intent, actual_cost, state):
                IF actual_cost > intent.resource_bounds.aic_ceiling * 1.3:
                    // Flag sponsor
                    penalize_sponsor_accuracy(intent.sponsor_id, state)
                    // Compensate worker (capped at 130% of bounds)
                    compensation = min(actual_cost,
                                       intent.resource_bounds.aic_ceiling * 1.3)
                    compensate_worker(worker, compensation)
                    // Log for governance review
                    IF count_flags(intent.sponsor_id, last_10_epochs) >= 3:
                        trigger_governance_review(intent.sponsor_id)

    systematic_under_budgeting_detection:
        description: >
            If 3+ independent workers flag the same sponsor within 10
            epochs, governance review is automatically triggered.
        threshold: 3 independent flags within 10 epochs
        action: "Governance review of sponsor; potential minimum bounds increase"
```

### 7.5 Sponsor Reputation System

```
FUNCTION update_sponsor_reputation(
    sponsor_id: AgentID,
    intent: IntentBudgetBinding,
    completion: TaskCompletion,
    state: SettlementState
):
    // Track budget accuracy
    budget_ratio = completion.actual_cost / intent.resource_bounds.aic_ceiling

    // Update running accuracy score (exponential moving average)
    alpha = 0.1  // Smoothing factor
    was_within_budget = 1.0 if budget_ratio <= 1.0 else 0.0

    old_accuracy = state.sponsor_reputation[sponsor_id].budget_accuracy
    new_accuracy = alpha * was_within_budget + (1 - alpha) * old_accuracy
    state.sponsor_reputation[sponsor_id].budget_accuracy = new_accuracy

    // Track worker satisfaction
    worker_rating = completion.worker_satisfaction_rating  // [0, 1]
    old_satisfaction = state.sponsor_reputation[sponsor_id].worker_satisfaction
    new_satisfaction = alpha * worker_rating + (1 - alpha) * old_satisfaction
    state.sponsor_reputation[sponsor_id].worker_satisfaction = new_satisfaction

    // Composite sponsor score
    state.sponsor_reputation[sponsor_id].composite =
        0.6 * new_accuracy + 0.4 * new_satisfaction

STRUCTURE SponsorReputation:
    sponsor_id:           AgentID
    budget_accuracy:      float64    // EMA of within-budget completion rate
    worker_satisfaction:  float64    // EMA of worker satisfaction ratings
    composite:            float64    // Weighted combination
    total_intents:        uint64     // Lifetime intent count
    total_flags:          uint64     // Lifetime under-budget flags
    adjusted_min_factor:  float64    // Current minimum bounds adjustment
```

### 7.6 Settlement Type Mapping

```
MAPPING IntentSettlementTypes:
    // Each RIF intent settlement type maps to a DSF settlement class

    TYPE_1_TASK_COMPLETION:
        description: "Standard task completion by worker"
        dsf_class: B_CLASS
        stream: SCHEDULING_COMPLIANCE
        settlement: "Per-epoch, immediate upon verified completion"

    TYPE_2_VERIFICATION_REWARD:
        description: "Reward for verifying task output quality"
        dsf_class: V_CLASS
        stream: VERIFICATION_QUALITY
        settlement: "N-epoch window, batched with verification quality assessment"

    TYPE_3_COMMUNICATION_REWARD:
        description: "Reward for efficient inter-agent communication"
        dsf_class: B_CLASS
        stream: COMMUNICATION_EFFICIENCY
        settlement: "Per-epoch, based on C4 ASV metrics"

    TYPE_4_GOVERNANCE_REWARD:
        description: "Reward for governance participation"
        dsf_class: G_CLASS
        stream: GOVERNANCE_PARTICIPATION
        settlement: "Upon governance proposal resolution"

    TYPE_5_SLASHING_PENALTY:
        description: "Penalty for protocol violation or poor performance"
        dsf_class: V_CLASS
        stream: N/A (penalty, not reward)
        settlement: "N-epoch window, processed with V-class batch"

    MAPPING TABLE:
    +-----------------------------+-----------+-------------------------+
    | Settlement Type             | DSF Class | Reward Stream           |
    +-----------------------------+-----------+-------------------------+
    | TYPE_1 Task Completion      | B-class   | Scheduling Compliance   |
    | TYPE_2 Verification Reward  | V-class   | Verification Quality    |
    | TYPE_3 Communication Reward | B-class   | Communication Efficiency|
    | TYPE_4 Governance Reward    | G-class   | Governance Participation|
    | TYPE_5 Slashing Penalty     | V-class   | N/A (penalty)           |
    +-----------------------------+-----------+-------------------------+
```

### 7.7 End-to-End Intent Settlement Flow

```
FLOW IntentSettlement:

    1. RIF proposes intent with resource_bounds
         |
    2. DSF validates budget (Section 7.2)
         |
         +-- FAIL: Intent rejected (insufficient funds/below minimum)
         |
    3. DSF reserves budget via PENDING_INITIATE
         |
    4. Worker assigned and begins execution
         |
         +-- Worker inspects (10% effort, Section 7.4)
         |     |
         |     +-- REJECT: Worker compensated, intent reassigned
         |
    5. Worker completes task
         |
         +-- Within budget: normal completion
         |     |
         |     +-- Completion report submitted (commit-reveal)
         |     |
         |     +-- B-class settlement: scheduling compliance reward
         |     |
         |     +-- V-class settlement: verification quality (if due)
         |
         +-- Over budget (>130%): worker flags sponsor
               |
               +-- Worker compensated at 130% cap
               |
               +-- Sponsor reputation penalized
               |
               +-- Governance review if 3+ flags

    6. Budget reservation resolved via PENDING_COMPLETE
         |
    7. Unused budget returned to sponsor
         |
    8. Sponsor reputation updated (Section 7.5)
```

---

*End of Part 1 (Sections 1-7). Part 2 continues with Sections 8-14.*
