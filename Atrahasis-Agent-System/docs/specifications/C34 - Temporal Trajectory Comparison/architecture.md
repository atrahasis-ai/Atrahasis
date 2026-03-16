# C34 — Black-Start Recovery Fabric with Adversarial State Reconstruction

## System Architecture Document

**Version:** 1.0.0
**Date:** 2026-03-11
**Invention ID:** C34
**Stage:** DESIGN
**Role:** Architecture Designer (PRIMARY tier)
**Status:** DESIGN — Architecture Complete
**Normative References:** C9 Cross-Layer Reconciliation v2.0, C3 Tidal Noosphere v2.0, C5 PCVM v2.0, C6 EMA v2.0, C7 RIF v2.0, C8 DSF v2.0, C31 CAT v1.0, RFC 2119, FIPS 180-4 (SHA-256)
**Implementation Target:** Parts I + II in C22 Wave 2; Part III in Wave 4+

---

## Abstract

C34 specifies a cross-layer recovery protocol for the five stateful layers of the Atrahasis Agent System (C3 coordination, C5 verification, C6 knowledge, C7 orchestration, C8 settlement). It addresses a gap that no individual layer's recovery mechanism covers: correlated multi-layer failure requiring coordinated restart with mutual state consistency verification.

The architecture consists of three integrated parts. **Part I (Black-Start Boot Sequence)** defines a dependency-ordered recovery protocol (C8->C5->C3->C7->C6) with per-tick state digests, synchronization predicates derived exhaustively from C9 integration contracts, and retrospective consistent-cut computation. **Part II (Recovery Witness Verification)** adds post-recovery Merkle verification between adjacent layers, cross-layer witness corroboration, and authority-directed reconciliation per the C9 hierarchy. **Part III (Adversarial Reconstruction Fallback)** provides a declarative cross-layer reference registry and causal traversal algorithm for reconstructing corrupted state from surviving cross-layer references, with adaptive triple-criteria termination and polynomial complexity O(R x W x N).

The always-on overhead is bounded at 0.007% of the 60-second SETTLEMENT_TICK budget (<=4ms per tick for digest computation). Recovery components are dormant during normal operation. The protocol is specified at C9 level — it is not owned by any single layer but defines obligations each layer must fulfill.

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Component Specifications](#2-component-specifications)
   - [2.1 State Digest Engine](#21-state-digest-engine)
   - [2.2 Recovery Protocol](#22-recovery-protocol)
   - [2.3 Recovery Coordinator](#23-recovery-coordinator)
   - [2.4 Witness Verification Engine](#24-witness-verification-engine)
   - [2.5 Adversarial Reconstruction Engine](#25-adversarial-reconstruction-engine)
   - [2.6 C5 VTD Snapshot Protocol](#26-c5-vtd-snapshot-protocol)
3. [Cross-Layer Integration](#3-cross-layer-integration)
4. [State Machine](#4-state-machine)
5. [Parameters Table](#5-parameters-table)
6. [Formal Properties](#6-formal-properties)

---

## 1. System Architecture Overview

### 1.1 Architectural Position

C34 is a **cross-cutting recovery infrastructure** — not a new layer in the AAS stack, but a protocol specified at C9 integration level that imposes obligations on all five stateful layers. C4 (ASV) is excluded because it is a stateless vocabulary specification. C31 (CAT) is optionally included when DAN_ENABLED=true.

```
┌──────────────────────────────────────────────────────────────────────┐
│                        AAS Architecture Stack                        │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │               C34 Recovery Fabric (C9-level protocol)           │ │
│  │                                                                  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │ │
│  │  │ State Digest │  │  Recovery    │  │ Witness Verification │  │ │
│  │  │ Engine       │  │  Coordinator │  │ Engine               │  │ │
│  │  │ (always-on)  │  │  (dormant)   │  │ (dormant)            │  │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │ │
│  │         │                 │                      │              │ │
│  │  ┌──────┴─────────────────┴──────────────────────┴──────────┐  │ │
│  │  │            Adversarial Reconstruction Engine              │  │ │
│  │  │            (dormant; Wave 4+ implementation)              │  │ │
│  │  └──────────────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                              │                                       │
│         ┌────────────────────┼────────────────────┐                  │
│         │ digest()           │ boot()              │ verify()         │
│         ▼                    ▼                     ▼                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ C8 DSF   │  │ C5 PCVM  │  │ C3 Tidal │  │ C7 RIF   │  │ C6 EMA ││
│  │ (Layer 2)│  │ (Layer 4)│  │ (Layer 5)│  │ (Layer 6)│  │(Layer 3)││
│  │          │  │          │  │          │  │          │  │         ││
│  │ EABS     │  │ VTD log  │  │ ETR/     │  │ WAL/     │  │ SHREC/  ││
│  │ state    │  │ opinion  │  │ SAFE_MODE│  │ failover │  │ quarant.││
│  │ hashing  │  │ snapshot │  │ KG Reg   │  │ ISR      │  │ opinion ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └────────┘│
│                                                                      │
│  Boot Order:  C8 ──► C5 ──► C3 ──► C7 ──► C6                       │
│  (settlement)  (verification) (coordination) (orchestration) (knowledge)│
└──────────────────────────────────────────────────────────────────────┘
```

### 1.2 Design Principles

1. **Integration, not replacement.** C34 augments each layer's existing recovery mechanisms. C8's EpochRecovery, C3's ETR/SAFE_MODE, C7's WAL/failover, C6's quarantine — all remain operational. C34 adds the cross-layer coordination they lack.

2. **Protocol at C9, execution distributed.** The protocol is defined at C9 integration level. Each layer implements its C34 obligations locally. No central recovery service exists.

3. **Always-on is cheap; recovery is expensive.** Digest computation runs at every tick (<=4ms). All other C34 machinery is dormant during normal operation.

4. **Consumer-side audit.** Each layer records digests of state it *receives* from other layers, not just its own state. This creates authority-independent verification paths without circular dependencies (producers do not digest consumer attestations).

5. **Authority hierarchy preserved.** Per C9: C5 is sovereign over claims, C8 is sovereign over settlement. C34 recovery respects this — it never overrides an authority's state from consumer-side data alone.

### 1.3 Data Flow: Normal Operation (Digest Computation)

During normal operation, the only active C34 component is the State Digest Engine, which runs at every SETTLEMENT_TICK boundary.

```
Every SETTLEMENT_TICK (60s):

  C8 DSF                     C5 PCVM                   C3 Tidal
  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
  │ 1. Compute       │       │ 1. Compute       │       │ 1. Compute       │
  │    settlement    │       │    VTD chain     │       │    scheduling    │
  │    state digest  │       │    digest        │       │    state digest  │
  │                  │       │                  │       │                  │
  │ 2. Broadcast     │       │ 2. Broadcast     │       │ 2. Broadcast     │
  │    signed digest │       │    signed digest │       │    signed digest │
  └────────┬─────────┘       └────────┬─────────┘       └────────┬─────────┘
           │                          │                           │
           ▼                          ▼                           ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                    Digest Broadcast Channel                            │
  │  (piggybacks on C3 CRDT replication; no new network protocol)         │
  └────────┬──────────────────┬───────────────────────┬───────────────────┘
           │                  │                       │
           ▼                  ▼                       ▼
  Consumer-side recording: each layer stores digests received from others.
  C5 stores: {C8_digest[tick], C3_digest[tick]}
  C3 stores: {C8_digest[tick], C5_digest[tick]}
  C7 stores: {C3_digest[tick], C5_digest[tick], C8_digest[tick]}
  C6 stores: {C5_digest[tick], C7_digest[tick], C3_digest[tick]}
  C8 stores: {C5_digest[tick], C3_digest[tick]}
```

### 1.4 Data Flow: Recovery (Boot Sequence + Verification)

When a multi-layer failure is detected, the recovery flow proceeds in strict linear order.

```
TRIGGER: Multi-layer failure detected
         (>=2 layers report DEGRADED or UNREACHABLE within FAILURE_DETECTION_WINDOW)

Phase 1: BLACK-START BOOT (C8 → C5 → C3 → C7 → C6)
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  Step 1: C8 (settlement)     ◄── Self-coordinating (pre-C7)             │
│    • EpochRecovery from last settled state                               │
│    • Compute post_state_hash                                             │
│    • Emit C8_READY(settlement_hash, epoch)                               │
│    • Gate: PRED_C8_READY                                                 │
│                                                                          │
│  Step 2: C5 (verification)   ◄── Self-coordinating (pre-C7)             │
│    • Load VTD snapshot + replay hash chain from C5 snapshot epoch        │
│    • Verify: consumer-side C8 digest matches C8_READY.settlement_hash    │
│    • Emit C5_READY(vtd_chain_hash, credibility_state_hash, epoch)        │
│    • Gate: PRED_C5_READY ∧ PRED_C8_CONSISTENT                           │
│                                                                          │
│  Step 3: C3 (coordination)   ◄── Self-coordinating (pre-C7)             │
│    • ETR / SAFE_MODE / Known-Good Registry recovery (existing)           │
│    • Verify: C8 digest, C5 digest from consumer-side trail               │
│    • Emit C3_READY(topology_hash, vrf_state_hash, epoch)                 │
│    • Gate: PRED_C3_READY ∧ PRED_C8_CONSISTENT ∧ PRED_C5_CONSISTENT      │
│                                                                          │
│  Step 4: C7 (orchestration)  ◄── C7 Recovery Coordinator takes over      │
│    • WAL replay + ISR reconciliation (existing)                          │
│    • Verify: C3, C5, C8 digests from consumer-side trail                 │
│    • Emit C7_READY(isr_hash, saga_state_hash, epoch)                     │
│    • Gate: PRED_C7_READY ∧ all upstream CONSISTENT predicates            │
│                                                                          │
│  Step 5: C6 (knowledge)      ◄── C7 Recovery Coordinator orchestrates    │
│    • Opinion freeze + queue drain + quarantine (existing)                 │
│    • Verify: C5, C7, C3 digests from consumer-side trail                 │
│    • Emit C6_READY(coherence_hash, shrec_state_hash, epoch)              │
│    • Gate: PRED_C6_READY ∧ all upstream CONSISTENT predicates            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

Phase 2: WITNESS VERIFICATION
┌──────────────────────────────────────────────────────────────────────────┐
│  For each adjacent layer pair (L_i, L_j):                                │
│    • L_i sends its state Merkle proof for shared data to L_j             │
│    • L_j verifies proof against its consumer-side digest                  │
│    • Result: CONSISTENT | INCONSISTENT                                    │
│                                                                          │
│  Cross-layer corroboration:                                              │
│    • If majority of consumer layers disagree with authority's state →     │
│      authority FLAGGED, fall back to last multiply-attested snapshot      │
│    • Authority-directed reconciliation: C5 for claims, C8 for settlement │
│                                                                          │
│  Recovery Completion Attestation:                                        │
│    • Signed tuple: (C8_hash, C5_hash, C3_hash, C7_hash, C6_hash, epoch) │
│    • All layers must sign before NORMAL state transition                  │
└──────────────────────────────────────────────────────────────────────────┘

Phase 3: ADVERSARIAL RECONSTRUCTION (if needed, Wave 4+)
┌──────────────────────────────────────────────────────────────────────────┐
│  Activated only if Phase 2 identifies unrecoverable state corruption     │
│    • Traverse cross-layer reference registry                             │
│    • Reconstruct missing state from consumer-side references             │
│    • Triple-criteria termination: coverage plateau, budget, comparison    │
│    • 10-epoch hard cap                                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 State Digest Engine (Always-On)

The State Digest Engine computes per-layer state digests at every SETTLEMENT_TICK boundary. It is the only C34 component that runs during normal operation.

#### 2.1.1 What Is Digested Per Layer Per Tick

Each layer digests a well-defined subset of its state that captures cross-layer-relevant state changes:

| Layer | Digested State | Rationale |
|-------|---------------|-----------|
| **C8 DSF** | `SHA-256(settlement_hash ‖ epoch_number ‖ total_aic_supply ‖ conservation_valid)` | settlement_hash already computed by EABS (zero additional cost); total_aic_supply and conservation_valid are canary values |
| **C5 PCVM** | `SHA-256(vtd_chain_tip ‖ credibility_snapshot_hash ‖ pending_claims_count ‖ opinion_count)` | vtd_chain_tip is the VTD hash chain head (see SS2.6); credibility_snapshot_hash summarizes aggregate credibility state |
| **C3 Tidal** | `SHA-256(topology_version ‖ hash_ring_hash ‖ vrf_seed ‖ safe_mode_state ‖ known_good_registry_hash)` | Captures scheduling state, VRF entropy, and emergency state |
| **C7 RIF** | `SHA-256(isr_crdt_hash ‖ active_saga_count ‖ wal_tip ‖ pe_roster_hash)` | ISR CRDT hash captures intent state; WAL tip captures durability frontier |
| **C6 EMA** | `SHA-256(coherence_graph_hash ‖ shrec_regime ‖ active_quanta_count ‖ quarantine_count ‖ consolidation_epoch)` | Coherence graph hash is sharded Merkle root; SHREC regime captures metabolic state |

**Performance budget:** Each layer's digest computation MUST complete within DIGEST_BUDGET_MS (default 4ms). The C8 settlement_hash is already computed by EABS, so C8's marginal cost is effectively zero (only the additional concatenation and SHA-256 of 4 values). For C6, the coherence_graph_hash uses an incrementally maintained Merkle root over the sharded coherence graph — not recomputed from scratch each tick.

#### 2.1.2 Merkle Tree Structure

Each layer maintains a **Digest History Tree** — a Merkle tree indexed by tick number, enabling efficient proof of any historical digest.

```
STRUCTURE DigestHistoryTree:
    // Binary Merkle tree over sequential tick digests
    // Leaves: individual tick digests
    // Height: ceil(log2(DIGEST_RETENTION_TICKS))

    root:           bytes32
    leaves:         CircularBuffer<TickDigest, DIGEST_RETENTION_TICKS>
    tree_nodes:     Array<bytes32>    // internal nodes, level-indexed

    FUNCTION append(tick: uint64, digest: bytes32):
        leaf_index = tick % DIGEST_RETENTION_TICKS
        leaves[leaf_index] = TickDigest { tick: tick, digest: digest }
        recompute_path(leaf_index)  // O(log N) hash recomputations

    FUNCTION prove(tick: uint64) -> MerkleProof:
        // Returns sibling hashes from leaf to root
        leaf_index = tick % DIGEST_RETENTION_TICKS
        RETURN extract_proof_path(leaf_index)

    FUNCTION verify(tick: uint64, digest: bytes32, proof: MerkleProof) -> bool:
        computed_root = compute_root_from_proof(digest, proof)
        RETURN computed_root == root

STRUCTURE TickDigest:
    tick:       uint64
    digest:     bytes32
    signature:  Ed25519Sig    // signed by layer's identity key
    timestamp:  uint64        // wall-clock time of computation
```

**Retention policy:** DIGEST_RETENTION_TICKS = 36000 (one CONSOLIDATION_CYCLE = 600 ticks x 60 = 36000 seconds, storing one digest per tick). At 32 bytes per digest + 64 bytes signature + 16 bytes metadata = 112 bytes per tick, total storage per layer is ~3.8 MB. Pruning occurs at CONSOLIDATION_CYCLE boundaries.

#### 2.1.3 Storage Location and Redundancy

| Layer | Primary Storage | Redundancy Mechanism |
|-------|----------------|---------------------|
| C8 DSF | Appended to HDL node state (alongside settlement_hash) | HDL replication across all settlement nodes (>=2f+1 copies) |
| C5 PCVM | Dedicated digest log, co-located with VTD store | Replicated via C5's existing storage redundancy |
| C3 Tidal | Embedded in epoch-boundary CRDT state | CRDT replication ensures all nodes hold digests |
| C7 RIF | Appended to WAL | WAL is synchronously replicated to passive LD (active-passive replication) |
| C6 EMA | Dedicated digest log per shard | Sharded coherence graph replication |

**Cross-layer digest replication:** Each layer's signed digests are broadcast to all other layers via C3's CRDT replication infrastructure (piggyback — no new protocol). Each layer maintains a `ConsumerDigestLog` of digests received from other layers.

#### 2.1.4 Consumer-Side Audit Trail Format

Each layer maintains a log of digests received from layers it depends on:

```
STRUCTURE ConsumerDigestLog:
    // Per-source-layer circular buffer of received digests
    entries: Map<LayerID, CircularBuffer<ReceivedDigest, DIGEST_RETENTION_TICKS>>

STRUCTURE ReceivedDigest:
    source_layer:   LayerID         // which layer produced this digest
    tick:           uint64          // which tick
    digest:         bytes32         // the digest value
    signature:      Ed25519Sig      // source layer's signature
    received_at:    uint64          // wall-clock time of receipt
    verified:       bool            // signature verified on receipt

ENUM LayerID:
    C3_TIDAL
    C5_PCVM
    C6_EMA
    C7_RIF
    C8_DSF
```

**Dependency map for consumer-side recording** (derived from C9 contract matrix, Section 9.1):

| Consumer Layer | Records Digests From | Rationale (C9 contracts) |
|---------------|---------------------|--------------------------|
| C8 DSF | C5, C3 | C8 receives verification reports from C5, CRDT infra from C3 |
| C5 PCVM | C8, C3, C6 | C5 receives settlement feedback from C8, VRF from C3, K-class VTDs from C6 |
| C3 Tidal | C8, C5 | C3 receives settlement data from C8, verification results from C5 |
| C7 RIF | C3, C5, C8 | C7 receives scheduling from C3, credibility from C5, stake queries from C8 |
| C6 EMA | C5, C7, C3 | C6 receives MCTs/VTDs from C5, knowledge projections via C7, epoch boundary from C3 |

**Acyclicity guarantee:** Consumer-side recording is strictly unidirectional — a layer records what it *receives*, never what it *sends*. This prevents circular dependencies: L_i's digest is computed from L_i's own state, not from L_j's recording of L_i's state.

#### 2.1.5 Temporal Trust Gradient

Digests that have survived unchallenged for longer periods carry higher trust weight during recovery:

```
FUNCTION temporal_trust_weight(digest: TickDigest, current_tick: uint64) -> float:
    age_ticks = current_tick - digest.tick
    IF age_ticks <= 0:
        RETURN TRUST_WEIGHT_MIN     // 0.1 — just-computed digest

    // Logarithmic trust accumulation, capped
    raw_weight = TRUST_WEIGHT_MIN + TRUST_GROWTH_RATE * ln(1 + age_ticks)
    RETURN min(raw_weight, TRUST_WEIGHT_MAX)    // cap at 1.0

// During recovery, the consistent-cut algorithm preferentially selects
// digest sets with higher aggregate temporal trust weight.
```

### 2.2 Recovery Protocol (C9-Level Specification)

#### 2.2.1 Boot Order DAG

The boot order is a strict linear DAG derived from layer dependencies:

```
C8 (settlement) ──► C5 (verification) ──► C3 (coordination) ──► C7 (orchestration) ──► C6 (knowledge)

Justification:
  C8 first: Settlement state is the economic ground truth. All other layers
            depend on settlement being consistent before they can verify
            their own state against economic reality. C8 has no cross-layer
            dependencies for its own recovery (EpochRecovery is self-contained).

  C5 second: Verification state (credibility, VTD chains) depends on
             settlement being correct (C5 → C8 for attestation settlement).
             C5 does NOT depend on C3 for its own recovery (VRF is used
             for committee selection during normal operation, not recovery).

  C3 third:  Coordination state (topology, hash rings) depends on both
             settlement (C3 ↔ C8 for CRDT infrastructure) and verification
             (C3 ↔ C5 for verification result integration). C3's ETR/SAFE_MODE
             is self-contained but requires settlement and verification to
             be consistent before exiting SAFE_MODE.

  C7 fourth: Orchestration depends on scheduling (C3), credibility (C5),
             and settlement (C8). C7 is also the Recovery Coordinator for
             Phase 4-5. C7 cannot coordinate recovery of layers it depends on.

  C6 last:   Knowledge metabolism depends on verification (C5 for claim
             classification), coordination (C3 for epoch boundaries), and
             orchestration (C7 for knowledge projections). C6 has the
             lowest recovery coverage (~50%) and highest acceptable data loss.
```

**Formal dependency declarations:**

```
STRUCTURE BootDependency:
    layer:              LayerID
    depends_on:         List<LayerID>
    self_coordinating:  bool        // true for pre-C7 layers
    rosc_definition:    ROSCSpec    // minimum viable recovery state

CONST BOOT_ORDER: List<BootDependency> = [
    BootDependency {
        layer: C8_DSF,
        depends_on: [],
        self_coordinating: true,
        rosc_definition: ROSC_C8
    },
    BootDependency {
        layer: C5_PCVM,
        depends_on: [C8_DSF],
        self_coordinating: true,
        rosc_definition: ROSC_C5
    },
    BootDependency {
        layer: C3_TIDAL,
        depends_on: [C8_DSF, C5_PCVM],
        self_coordinating: true,
        rosc_definition: ROSC_C3
    },
    BootDependency {
        layer: C7_RIF,
        depends_on: [C8_DSF, C5_PCVM, C3_TIDAL],
        self_coordinating: false,       // C7 IS the coordinator
        rosc_definition: ROSC_C7
    },
    BootDependency {
        layer: C6_EMA,
        depends_on: [C5_PCVM, C3_TIDAL, C7_RIF],
        self_coordinating: false,       // coordinated by C7
        rosc_definition: ROSC_C6
    },
]
```

#### 2.2.2 Synchronization Predicates

Synchronization predicates gate each layer's recovery. They are derived **exhaustively** from the C9 integration contract directory (SS9.2, 9.3). Every bidirectional contract in the C9 matrix generates at least one predicate.

**Predicate derivation methodology:** For each entry in the C9 contract matrix where layer L_i has a dependency on layer L_j (`<-` or `<->`), a synchronization predicate is generated that asserts L_j's recovered state is consistent with L_i's consumer-side record of L_j's state.

```
// Master predicate type
STRUCTURE SynchronizationPredicate:
    name:           string
    source_layer:   LayerID         // layer whose state is being checked
    consumer_layer: LayerID         // layer that holds the consumer-side record
    contract_ref:   string          // C9 contract reference (e.g., "C5 -> C8")
    check_function: fn(SourceState, ConsumerDigest) -> PredicateResult

ENUM PredicateResult:
    SATISFIED           // source state matches consumer record
    VIOLATED_MINOR      // minor divergence within tolerance
    VIOLATED_MAJOR      // major divergence, requires reconciliation
    UNVERIFIABLE        // consumer record missing or corrupted
```

**Complete predicate table** (21 predicates derived from C9 contract matrix):

**C8 Recovery (Step 1) — 0 upstream predicates:**

| ID | Predicate | Gate | Source |
|----|-----------|------|--------|
| PRED_C8_READY | C8 EpochRecovery completed, settlement_hash computed | C8 internal | C8 EABS |

**C5 Recovery (Step 2) — 2 upstream predicates:**

| ID | Predicate | Gate | Source |
|----|-----------|------|--------|
| PRED_C5_READY | C5 VTD snapshot loaded, hash chain replayed to tip | C5 internal | C5 VTD log |
| PRED_C8C5_SETTLEMENT | C5's consumer-side C8 digest at recovery tick matches C8_READY.settlement_hash | C8 → C5 | C9 SS9.2: "C5 -> C8: Verification reports, credibility scores, attestations" |

**C3 Recovery (Step 3) — 4 upstream predicates:**

| ID | Predicate | Gate | Source |
|----|-----------|------|--------|
| PRED_C3_READY | C3 ETR/SAFE_MODE recovery complete, topology and VRF state reconstructed | C3 internal | C3 SAFE_MODE FSM |
| PRED_C8C3_CRDT | C3's consumer-side C8 digest matches C8_READY.settlement_hash | C8 → C3 | C9 SS9.2: "C3 <-> C8: C3 provides CRDT infrastructure" |
| PRED_C5C3_VERIFICATION | C3's consumer-side C5 digest matches C5_READY.vtd_chain_hash | C5 → C3 | C9 SS9.2: "C5 -> C3: Verification results" |
| PRED_C3C5_VRF | C5's consumer-side C3 digest matches C3_READY.vrf_state_hash | C3 → C5 | C9 SS9.2: "C3 -> C5: VRF output per tidal epoch" |

**C7 Recovery (Step 4) — 6 upstream predicates:**

| ID | Predicate | Gate | Source |
|----|-----------|------|--------|
| PRED_C7_READY | C7 WAL replayed, ISR reconciled, PE roster rebuilt | C7 internal | C7 WAL/failover |
| PRED_C3C7_SCHEDULING | C7's consumer-side C3 digest matches C3_READY.topology_hash | C3 → C7 | C9 SS9.2: "C3 <-> C7: scheduling, G-class, VRF, topology" |
| PRED_C5C7_CREDIBILITY | C7's consumer-side C5 digest matches C5_READY.credibility_state_hash | C5 → C7 | C9 SS9.2: "C5 -> C7: Agent credibility scores" |
| PRED_C8C7_STAKE | C7's consumer-side C8 digest matches C8_READY.settlement_hash | C8 → C7 | C9 SS9.2: "C7 <-> C8: stake availability queries" |
| PRED_C7C3_INTENTS | C3's consumer-side C7 digest matches C7_READY.isr_hash | C7 → C3 | C9 SS9.2: "C7 submits leaf intents" |
| PRED_C7C8_BUDGETS | C8's consumer-side C7 digest matches C7_READY.saga_state_hash | C7 → C8 | C9 SS9.2: "C7 submits intent budgets, task completions" |

**C6 Recovery (Step 5) — 9 upstream predicates:**

| ID | Predicate | Gate | Source |
|----|-----------|------|--------|
| PRED_C6_READY | C6 opinion freeze + queue drain complete, coherence graph loaded | C6 internal | C6 SHREC |
| PRED_C5C6_CLAIMS | C6's consumer-side C5 digest matches C5_READY.vtd_chain_hash | C5 → C6 | C9 SS9.2: "C5 <-> C6: MCTs, VTDs, claim classification" |
| PRED_C7C6_PROJECTIONS | C6's consumer-side C7 digest matches C7_READY.isr_hash | C7 → C6 | C9 SS9.2: "C6 -> C7: Knowledge projections" |
| PRED_C3C6_EPOCH | C6's consumer-side C3 digest matches C3_READY.topology_hash | C3 → C6 | C9 SS9.2: "C3 -> C6: Epoch boundary notifications" |
| PRED_C6C5_KCLASS | C5's consumer-side C6 digest matches C6_READY.coherence_hash | C6 → C5 | C9 SS9.2: "C6 submits K-class VTDs" |
| PRED_C6C7_KNOWLEDGE | C7's consumer-side C6 digest matches C6_READY.shrec_state_hash | C6 → C7 | C9 SS9.2: "C6 -> C7: Knowledge projections, SHREC state" |
| PRED_C6C8_METABOLIC | C8's consumer-side C6 digest matches C6_READY.coherence_hash | C6 → C8 | C9 SS9.2: "C6 -> C8: Knowledge contribution reports" |
| PRED_C6C3_SUMMARIES | C3's consumer-side C6 digest matches C6_READY.coherence_hash | C6 → C3 | C9 SS9.2: "C6 -> C3: Locus-scoped knowledge summaries" |
| PRED_C4C6_ASV | C6's stored C4 schema version matches expected (stateless check) | C4 → C6 | C9 SS9.2: "C4 -> C6: ASV tokens" |

**Defense system predicates (conditional — only when defense layers are active):**

| ID | Predicate | Gate | Source |
|----|-----------|------|--------|
| PRED_C11_CACT | C5's CACT extension state consistent with C5 recovery | C11 ↔ C5 | C9 SS9.3.1 |
| PRED_C12_AVAP | C3's AVAP VRF state consistent with C3 recovery; C5's sealed opinion state consistent | C12 ↔ C3/C5 | C9 SS9.3.2 |
| PRED_C13_CRP | C6's CRP+ immune memory consistent with C6 recovery | C13 ↔ C6 | C9 SS9.3.3 |

**Extensibility mechanism (MF-3):** New C9 contracts added after DESIGN automatically generate new predicates via the following rule:

```
RULE PredicateGeneration:
    FOR each new contract entry (L_i, L_j, direction) added to C9 SS9:
        IF direction IN {<-, <->}:  // L_i depends on L_j
            GENERATE predicate PRED_{L_j}{L_i}_{contract_name}
            ADD to L_i's recovery gate
            LOG: "New synchronization predicate generated for {L_i} <- {L_j}"
```

#### 2.2.3 Consistent-Cut Algorithm

A consistent cut is a set of per-layer state snapshots such that no layer's snapshot references state from another layer that is *newer* than that layer's snapshot. C34 computes consistent cuts **retrospectively** from stored digests.

```
FUNCTION compute_consistent_cut(
    target_tick: uint64,
    digest_logs: Map<LayerID, DigestHistoryTree>,
    consumer_logs: Map<LayerID, ConsumerDigestLog>
) -> ConsistentCut:

    // Step 1: Find the most recent tick at or before target_tick where
    //         all layers have digests
    candidate_tick = target_tick
    WHILE candidate_tick > (target_tick - MAX_CONSISTENT_CUT_SEARCH_WINDOW):
        all_present = true
        FOR each layer IN [C8, C5, C3, C7, C6]:
            IF NOT digest_logs[layer].has(candidate_tick):
                all_present = false
                BREAK
        IF all_present:
            BREAK
        candidate_tick -= 1

    IF NOT all_present:
        RETURN ConsistentCut.FAILED(reason="No tick with all digests in window")

    // Step 2: Verify mutual consistency at candidate_tick
    //         For each consumer-producer pair, check that the consumer's
    //         recorded producer digest matches the producer's own digest
    inconsistencies = []
    FOR each (consumer, producer) IN CONSUMER_PRODUCER_PAIRS:
        consumer_record = consumer_logs[consumer].get(producer, candidate_tick)
        producer_digest = digest_logs[producer].get(candidate_tick)

        IF consumer_record IS NULL:
            // Consumer missing this record — tolerable if within
            // DIGEST_LOSS_TOLERANCE (max 5 consecutive missing)
            CONTINUE
        IF consumer_record.digest != producer_digest.digest:
            inconsistencies.append(Inconsistency {
                consumer: consumer,
                producer: producer,
                tick: candidate_tick,
                consumer_value: consumer_record.digest,
                producer_value: producer_digest.digest
            })

    IF len(inconsistencies) == 0:
        // Step 3: Consistent cut found
        cut = ConsistentCut {
            tick: candidate_tick,
            digests: { layer: digest_logs[layer].get(candidate_tick)
                       FOR layer IN [C8, C5, C3, C7, C6] },
            trust_weight: sum(temporal_trust_weight(d, target_tick)
                              FOR d IN cut.digests.values()),
            status: CONSISTENT
        }
        RETURN cut

    ELSE:
        // Inconsistency at this tick — try earlier tick
        candidate_tick -= 1
        GOTO Step 1 (WHILE loop continues)

STRUCTURE ConsistentCut:
    tick:           uint64
    digests:        Map<LayerID, TickDigest>
    trust_weight:   float           // aggregate temporal trust
    status:         CONSISTENT | FAILED
    inconsistencies: List<Inconsistency>   // empty if CONSISTENT
```

**Worst-case consistent-cut gap:** One CONSOLIDATION_CYCLE (36,000 seconds = 600 ticks). This occurs when C6's coherence_graph_hash only changes at CONSOLIDATION_CYCLE boundaries. For C8 settlement (where AIC balances are at stake), the gap is much shorter — C8's settlement_hash changes every tick. **MF-5 resolution:** The 36,000-second gap applies only to C6 state. C8 settlement state has a worst-case gap of 1 tick (60 seconds) because EABS settles every tick. C5 state has a worst-case gap of 1 TIDAL_EPOCH (3600 seconds) because opinion snapshots are taken at TIDAL_EPOCH boundaries. For settlement recovery, the relevant consistent-cut gap is the C8 gap (60 seconds), not the C6 gap.

#### 2.2.4 ROSC (Reduced Operational State Configuration) Per Layer

ROSC defines the minimum viable recovered state for each layer — the state sufficient to resume accepting new operations, even if historical state is incomplete.

```
STRUCTURE ROSCSpec:
    layer:              LayerID
    required_state:     List<string>     // what MUST be recovered
    optional_state:     List<string>     // what MAY be recovered (best-effort)
    acceptable_loss:    string           // what CAN be lost permanently
    recovery_time_target: Duration       // target recovery duration

CONST ROSC_C8: ROSCSpec = {
    layer: C8_DSF,
    required_state: [
        "settlement_hash (current epoch)",
        "all AccountState records (balances, stakes, collateral)",
        "total_aic_supply",
        "reward_pools",
        "pending_registry (active pending operations)",
    ],
    optional_state: [
        "historical settlement results (previous epochs)",
        "operation rejection logs",
    ],
    acceptable_loss: "Computation timing metrics. Historical rejection reasons.",
    recovery_time_target: Duration.ticks(5)    // 5 SETTLEMENT_TICKs = 5 minutes
}

CONST ROSC_C5: ROSCSpec = {
    layer: C5_PCVM,
    required_state: [
        "VTD hash chain (complete, unbroken)",
        "current credibility state per agent (overall + per-class)",
        "pending claim queue",
        "CACT commitment chain state",
    ],
    optional_state: [
        "historical VTDs older than DIGEST_RETENTION_TICKS",
        "deep-audit logs",
        "AVAP sealed opinion history",
    ],
    acceptable_loss: "Individual VTD content for closed claims older than retention. "
                     "Adversarial probing statistics (can be recomputed).",
    recovery_time_target: Duration.ticks(10)   // 10 SETTLEMENT_TICKs = 10 minutes
}

CONST ROSC_C3: ROSCSpec = {
    layer: C3_TIDAL,
    required_state: [
        "current topology (loci, parcels, agent assignments)",
        "hash ring state per parcel",
        "VRF seed (current epoch)",
        "Known-Good Registry",
        "SAFE_MODE state machine state",
    ],
    optional_state: [
        "predictive model coefficients (can be cold-started)",
        "stigmergic decay values (will regenerate)",
        "historical capacity snapshots",
    ],
    acceptable_loss: "Predictive communication model (retrains in ~10 epochs). "
                     "Stigmergic signals (regenerate naturally).",
    recovery_time_target: Duration.ticks(10)   // 10 ticks = 10 minutes
}

CONST ROSC_C7: ROSCSpec = {
    layer: C7_RIF,
    required_state: [
        "ISR CRDT state (all non-COMPLETED, non-DISSOLVED intents)",
        "active saga state (all in-flight recovery/compensation sagas)",
        "PE roster (which agents are assigned to which loci)",
        "WAL (from last checkpoint to current)",
    ],
    optional_state: [
        "completed intent history",
        "decomposition cache",
        "System 4 horizon scan state",
    ],
    acceptable_loss: "Completed intent archive. Decomposition cache (rebuilt on demand). "
                     "System 4 predictive state (re-scans within 1 CONSOLIDATION_CYCLE).",
    recovery_time_target: Duration.epochs(1)   // 1 TIDAL_EPOCH = 1 hour
}

CONST ROSC_C6: ROSCSpec = {
    layer: C6_EMA,
    required_state: [
        "coherence graph structure (sharded, active quanta only)",
        "SHREC controller state (current regime, allocations)",
        "quarantine queue (quanta under review)",
        "CRP+ immune memory (L1 + L2 signatures)",
    ],
    optional_state: [
        "historical vitality scores",
        "circulation analytics",
        "dreaming pipeline work-in-progress",
    ],
    acceptable_loss: "In-progress consolidation (dreaming restarts at next cycle). "
                     "Vitality history (can be recomputed from coherence graph). "
                     "~50% of C6 state is reconstructible from C5 claim records + "
                     "C7 knowledge projections; remaining ~50% (internal coherence "
                     "metadata, catabolism history) is unrecoverable — MF-4 acknowledged.",
    recovery_time_target: Duration.epochs(3)   // 3 TIDAL_EPOCHS = 3 hours
}
```

### 2.3 Recovery Coordinator (C7 Component)

#### 2.3.1 Recovery Saga State Machine

The Recovery Coordinator is a C7 recovery saga — a durable workflow that survives C7 restarts via WAL persistence. It becomes active only during cross-layer recovery.

```
STRUCTURE RecoverySaga:
    saga_id:            SagaID
    state:              RecoverySagaState
    boot_progress:      Map<LayerID, LayerBootState>
    consistent_cut:     ConsistentCut?
    witness_results:    Map<(LayerID, LayerID), WitnessResult>
    completion_attestation: RecoveryCompletionAttestation?
    started_at:         uint64          // tick when saga started
    timeout_tick:       uint64          // hard deadline

ENUM RecoverySagaState:
    INITIALIZING        // saga created, gathering failure information
    BOOTING_C8          // C8 recovery in progress
    BOOTING_C5          // C5 recovery in progress
    BOOTING_C3          // C3 recovery in progress
    BOOTING_C7_SELF     // C7 self-recovery (WAL replay, ISR reconciliation)
    BOOTING_C6          // C6 recovery in progress
    VERIFYING           // witness verification in progress
    RECONSTRUCTING      // Part III adversarial reconstruction (Wave 4+)
    COMPLETING          // all layers verified, assembling attestation
    COMPLETED           // recovery complete, system returning to NORMAL
    FAILED              // recovery failed, escalating to governance

ENUM LayerBootState:
    PENDING             // not yet started
    IN_PROGRESS         // recovery underway
    READY               // layer reports READY
    VERIFIED            // layer passed witness verification
    FAILED              // layer recovery failed
    RECONSTRUCTED       // layer state reconstructed from cross-layer refs

// Saga transitions
FUNCTION advance_saga(saga: RecoverySaga, event: RecoveryEvent):
    MATCH saga.state:
        INITIALIZING:
            IF event == C8_READY:
                saga.boot_progress[C8_DSF] = READY
                saga.state = BOOTING_C5
                signal_layer(C5_PCVM, START_RECOVERY, saga.consistent_cut)

        BOOTING_C5:
            IF event == C5_READY AND check_predicates(C5_PCVM, saga):
                saga.boot_progress[C5_PCVM] = READY
                saga.state = BOOTING_C3
                signal_layer(C3_TIDAL, START_RECOVERY, saga.consistent_cut)

        BOOTING_C3:
            IF event == C3_READY AND check_predicates(C3_TIDAL, saga):
                saga.boot_progress[C3_TIDAL] = READY
                saga.state = BOOTING_C7_SELF
                // C7 self-recovery begins here

        BOOTING_C7_SELF:
            IF event == C7_READY AND check_predicates(C7_RIF, saga):
                saga.boot_progress[C7_RIF] = READY
                saga.state = BOOTING_C6
                signal_layer(C6_EMA, START_RECOVERY, saga.consistent_cut)

        BOOTING_C6:
            IF event == C6_READY AND check_predicates(C6_EMA, saga):
                saga.boot_progress[C6_EMA] = READY
                saga.state = VERIFYING
                initiate_witness_verification(saga)

        VERIFYING:
            IF all_witnesses_complete(saga):
                IF all_witnesses_consistent(saga):
                    saga.state = COMPLETING
                ELSE IF reconstruction_possible(saga):
                    saga.state = RECONSTRUCTING     // Wave 4+ only
                ELSE:
                    saga.state = FAILED
                    escalate_to_governance(saga)

        RECONSTRUCTING:
            IF event == RECONSTRUCTION_COMPLETE:
                saga.state = COMPLETING
            IF event == RECONSTRUCTION_FAILED:
                saga.state = FAILED

        COMPLETING:
            attestation = build_completion_attestation(saga)
            IF all_layers_signed(attestation):
                saga.completion_attestation = attestation
                saga.state = COMPLETED
                // System transitions from RECOVERY to NORMAL

    // Timeout check (every tick)
    IF current_tick() > saga.timeout_tick:
        saga.state = FAILED
        escalate_to_governance(saga)
```

#### 2.3.2 Interaction with C7's Existing Failover Infrastructure

The Recovery Coordinator integrates with C7's existing active-passive LD failover:

1. **WAL persistence:** The RecoverySaga state is written to C7's WAL. If C7 crashes during recovery, the passive LD replays the WAL and resumes the saga from the last persisted state.

2. **ISR interaction:** The RecoverySaga is registered in the ISR CRDT as a special `SYSTEM_RECOVERY` intent type. This ensures it survives ISR reconciliation during C7 failover.

3. **GE routing:** During recovery, the Global Engine (GE) routes all recovery-related messages to the designated Recovery Coordinator LD. If that LD fails, another LD takes over via the standard failover protocol plus WAL replay of the saga.

4. **Emergency bypass interaction:** If C7 enters Emergency Bypass (SS10.6.3 — both active and passive LD unavailable), the Recovery Coordinator saga is frozen. Pre-C7 layers (C8, C5, C3) continue their self-coordinating recovery. When C7 is restored, the saga resumes from its WAL-persisted state.

#### 2.3.3 Pre-C7 Self-Coordination Mechanism

Layers C8, C5, and C3 recover before C7 is available and therefore cannot rely on C7's orchestration. Self-coordination uses a simple broadcast protocol:

```
PROTOCOL PreC7SelfCoordination:
    // Uses C3 CRDT broadcast when C3 is available;
    // falls back to direct peer-to-peer when C3 is unavailable.

    MESSAGE LayerReadyAnnouncement:
        layer:          LayerID
        state_digest:   bytes32
        epoch:          uint64
        rosc_status:    ROSCStatus
        signature:      Ed25519Sig      // signed by layer's identity key

    // Each pre-C7 layer:
    // 1. Performs its own recovery (existing mechanisms)
    // 2. Checks synchronization predicates against consumer-side digest log
    // 3. Broadcasts LayerReadyAnnouncement
    // 4. Waits for upstream layer announcements before proceeding

    FUNCTION self_coordinate(layer: LayerID, boot_deps: List<LayerID>):
        // Step 1: Perform layer-specific recovery
        layer.recover()

        // Step 2: Wait for upstream layers
        FOR each dep IN boot_deps:
            announcement = await_announcement(dep, timeout=SELF_COORD_TIMEOUT)
            IF announcement IS NULL:
                HALT: "Upstream layer {dep} did not announce READY within timeout"
                escalate_to_manual_recovery()
                RETURN

            // Step 3: Verify synchronization predicate
            predicate_result = check_predicate(layer, dep, announcement)
            IF predicate_result == VIOLATED_MAJOR:
                HALT: "Synchronization predicate failed: {layer} <- {dep}"
                escalate_to_governance()
                RETURN

        // Step 4: Announce readiness
        broadcast(LayerReadyAnnouncement {
            layer: layer,
            state_digest: layer.compute_digest(),
            epoch: layer.current_epoch(),
            rosc_status: layer.rosc_status(),
            signature: layer.sign(...)
        })

    // Communication channel priority:
    // 1. C3 CRDT broadcast (if C3 is already READY)
    // 2. Direct peer-to-peer UDP multicast (fallback)
    // 3. HDL gossip (C8 can piggyback on HDL node communication)
```

### 2.4 Witness Verification Engine (Part II)

#### 2.4.1 Merkle Comparison Protocol

After all layers have booted, the Witness Verification Engine verifies mutual consistency between all adjacent layer pairs.

```
PROTOCOL MerkleWitnessVerification:
    // For each layer pair (L_i, L_j) with a C9 contract:

    FUNCTION verify_pair(
        source: LayerID,        // authority for this data
        consumer: LayerID,      // consumer of this data
        recovery_tick: uint64
    ) -> WitnessResult:

        // Step 1: Source provides Merkle proof for its state at recovery_tick
        source_digest = source.get_digest(recovery_tick)
        source_proof = source.get_merkle_proof(recovery_tick)

        // Step 2: Consumer checks against its recorded digest
        consumer_record = consumer.get_consumer_digest(source, recovery_tick)

        IF consumer_record IS NULL:
            // Consumer didn't record this digest — check nearest available
            nearest = consumer.get_nearest_consumer_digest(source, recovery_tick,
                                                            MAX_DIGEST_SKIP)
            IF nearest IS NULL:
                RETURN WitnessResult.UNVERIFIABLE
            consumer_record = nearest

        // Step 3: Compare
        IF source_digest.digest == consumer_record.digest:
            // Step 4: Verify Merkle proof is valid
            IF source.verify_merkle_proof(recovery_tick, source_proof):
                RETURN WitnessResult.CONSISTENT
            ELSE:
                RETURN WitnessResult.PROOF_INVALID

        ELSE:
            RETURN WitnessResult.INCONSISTENT(
                source_value = source_digest.digest,
                consumer_value = consumer_record.digest,
                divergence_tick = find_divergence_tick(source, consumer, recovery_tick)
            )

STRUCTURE WitnessResult:
    status:         CONSISTENT | INCONSISTENT | UNVERIFIABLE | PROOF_INVALID
    source_layer:   LayerID
    consumer_layer: LayerID
    tick:           uint64
    details:        string?
    divergence_tick: uint64?     // tick where digests first diverged
```

#### 2.4.2 Cross-Layer Witness Corroboration Rules

When a layer's recovered state is disputed, corroboration across multiple consumer layers determines the outcome.

```
STRUCTURE CorroborationAssessment:
    authority_layer:    LayerID
    consumer_results:   Map<LayerID, WitnessResult>
    verdict:            CORROBORATED | FLAGGED | INCONCLUSIVE

FUNCTION assess_corroboration(
    authority: LayerID,
    witness_results: Map<(LayerID, LayerID), WitnessResult>
) -> CorroborationAssessment:

    // Collect all witness results where this layer is the source
    consumer_results = {}
    FOR each ((source, consumer), result) IN witness_results:
        IF source == authority:
            consumer_results[consumer] = result

    // Count verdicts
    consistent_count = count(r FOR r IN consumer_results.values()
                             IF r.status == CONSISTENT)
    inconsistent_count = count(r FOR r IN consumer_results.values()
                               IF r.status == INCONSISTENT)
    total_verifiable = consistent_count + inconsistent_count

    IF total_verifiable == 0:
        RETURN CorroborationAssessment {
            authority_layer: authority,
            consumer_results: consumer_results,
            verdict: INCONCLUSIVE
        }

    // Corroboration threshold: strict majority of verifiable consumers
    // must agree with the authority
    IF inconsistent_count > consistent_count:
        // Majority of consumers DISAGREE with authority
        RETURN CorroborationAssessment {
            authority_layer: authority,
            consumer_results: consumer_results,
            verdict: FLAGGED
        }
    ELSE:
        RETURN CorroborationAssessment {
            authority_layer: authority,
            consumer_results: consumer_results,
            verdict: CORROBORATED
        }
```

**Corroboration thresholds per layer:**

| Authority Layer | Number of Consumers | Flagging Threshold | Rationale |
|----------------|--------------------|--------------------|-----------|
| C8 DSF | 2 (C5, C3) | Both disagree (2/2) | C8 is settlement authority — high bar to override |
| C5 PCVM | 3 (C8, C3, C6) | >=2 disagree (2/3) | C5 is verification authority — standard majority |
| C3 Tidal | 2 (C8, C5) | Both disagree (2/2) | C3 state is broadly shared — high bar |
| C7 RIF | 3 (C3, C5, C8) | >=2 disagree (2/3) | Standard majority |
| C6 EMA | 3 (C5, C7, C3) | >=2 disagree (2/3) | Standard majority; C6 has lowest recovery coverage |

#### 2.4.3 Authority-Override Quorum

When a layer is FLAGGED by corroboration assessment, the authority-override protocol activates:

```
PROTOCOL AuthorityOverride:
    // Activated when assess_corroboration returns FLAGGED

    FUNCTION handle_flagged_authority(
        assessment: CorroborationAssessment,
        saga: RecoverySaga
    ):
        flagged_layer = assessment.authority_layer

        // Step 1: Determine reconciliation authority (per C9 hierarchy)
        reconciliation_authority = MATCH flagged_layer:
            C5_PCVM => C5_PCVM     // C5 is its own claims authority (INV-C1)
            C8_DSF  => C8_DSF      // C8 is its own settlement authority (INV-S1)
            C3_TIDAL => C3_TIDAL   // C3 is coordination authority
            C7_RIF  => C7_RIF      // C7 is orchestration authority
            C6_EMA  => C6_EMA      // C6 is knowledge authority

        // Step 2: Fall back to last multiply-attested snapshot
        //   A multiply-attested snapshot is a tick where ALL consumers
        //   agreed with the authority (all witness results CONSISTENT)
        fallback_tick = find_last_multiply_attested_tick(
            flagged_layer,
            saga.witness_results,
            search_window = DIGEST_RETENTION_TICKS
        )

        IF fallback_tick IS NOT NULL:
            // Step 3: Roll back authority to multiply-attested state
            flagged_layer.rollback_to_tick(fallback_tick)
            // Step 4: Replay from fallback_tick to current
            flagged_layer.replay_from(fallback_tick)
            // Step 5: Re-run witness verification for this layer
            re_verify(flagged_layer, saga)
        ELSE:
            // No multiply-attested snapshot found — escalate
            IF PART_III_ENABLED:
                saga.state = RECONSTRUCTING
                initiate_reconstruction(flagged_layer, saga)
            ELSE:
                // Pre-Wave 4: full snapshot restore (degraded mode — MF-2)
                flagged_layer.restore_from_full_snapshot()
                saga.state = VERIFYING
                re_verify(flagged_layer, saga)
```

#### 2.4.4 Recovery Completion Attestation Format

```
STRUCTURE RecoveryCompletionAttestation:
    // Signed by all five layers; constitutes proof of successful recovery
    saga_id:            SagaID
    recovery_tick:      uint64          // tick at which recovery completed
    consistent_cut_tick: uint64         // tick of the consistent cut used
    layer_digests:      Map<LayerID, bytes32>  // post-recovery digest per layer
    layer_signatures:   Map<LayerID, Ed25519Sig>  // each layer signs the full tuple
    witness_summary:    WitnessSummary
    reconstruction_used: bool           // true if Part III was invoked
    duration_ticks:     uint64          // how long recovery took
    attestation_hash:   bytes32         // SHA-256 of all fields above

STRUCTURE WitnessSummary:
    total_pairs_verified:   uint32
    consistent_pairs:       uint32
    inconsistent_pairs:     uint32
    unverifiable_pairs:     uint32
    flagged_layers:         List<LayerID>
    override_applied:       bool

// Attestation validity
FUNCTION is_valid_attestation(att: RecoveryCompletionAttestation) -> bool:
    // All five layers must have signed
    FOR each layer IN [C8_DSF, C5_PCVM, C3_TIDAL, C7_RIF, C6_EMA]:
        IF layer NOT IN att.layer_signatures:
            RETURN false
        IF NOT verify_signature(att.attestation_hash, att.layer_signatures[layer], layer.pubkey):
            RETURN false

    // Consistent cut tick must precede recovery tick
    IF att.consistent_cut_tick > att.recovery_tick:
        RETURN false

    RETURN true
```

### 2.5 Adversarial Reconstruction Engine (Part III)

**Implementation phase:** Wave 4+ (Parts I and II are Wave 2). Part III is fully specified here for forward-compatibility but is not implemented until adversarial threat models are validated by operational experience.

**Degraded-mode path (MF-2):** Before Wave 4, if witness verification identifies unrecoverable state corruption, the system falls back to full snapshot restore. This is explicitly specified as the pre-Part-III degraded path.

#### 2.5.1 Declarative Cross-Layer Reference Registry

Each layer declares all outbound references it holds to other layers' state. This registry enables causal traversal during reconstruction.

```
STRUCTURE CrossLayerReference:
    source_layer:       LayerID         // layer holding the reference
    source_entity:      string          // entity type in source layer
    source_id:          bytes32         // entity identifier
    target_layer:       LayerID         // layer being referenced
    target_entity:      string          // entity type in target layer
    target_id:          bytes32         // entity identifier
    reference_type:     ReferenceType   // nature of the reference
    cardinality:        SINGULAR | PLURAL  // one-to-one or one-to-many
    criticality:        REQUIRED | OPTIONAL // is source invalid without target?

ENUM ReferenceType:
    SETTLEMENT_REF      // reference to C8 settlement state
    CREDIBILITY_REF     // reference to C5 credibility score
    CLAIM_REF           // reference to C5 claim/VTD
    TOPOLOGY_REF        // reference to C3 topology/parcel
    VRF_REF             // reference to C3 VRF output
    INTENT_REF          // reference to C7 intent state
    KNOWLEDGE_REF       // reference to C6 epistemic quantum
    SCHEDULE_REF        // reference to C3 scheduling assignment
    BUDGET_REF          // reference to C8 budget allocation
```

**Complete reference registry** (derived from C9 contracts):

| Source Layer | Source Entity | Target Layer | Target Entity | Type | Criticality |
|-------------|--------------|-------------|--------------|------|-------------|
| C5 | VerificationReport | C8 | SettlementEntry | SETTLEMENT_REF | REQUIRED |
| C5 | VTD | C3 | VRFOutput | VRF_REF | OPTIONAL |
| C5 | CredibilityScore | C8 | AccountState.capability_score | SETTLEMENT_REF | REQUIRED |
| C3 | HashRing | C8 | AccountState.staked_aic | SETTLEMENT_REF | REQUIRED |
| C3 | ParcelAssignment | C5 | VRFOutput | VRF_REF | REQUIRED |
| C3 | EpochBoundary | C6 | SHRECState | KNOWLEDGE_REF | OPTIONAL |
| C7 | IntentState | C3 | ScheduleAssignment | SCHEDULE_REF | REQUIRED |
| C7 | IntentBudget | C8 | BudgetAllocation | BUDGET_REF | REQUIRED |
| C7 | AgentAssignment | C5 | CredibilityScore | CREDIBILITY_REF | REQUIRED |
| C6 | EpistemicQuantum | C5 | ClaimClassification | CLAIM_REF | REQUIRED |
| C6 | KClassVTD | C5 | VTDChain | CLAIM_REF | REQUIRED |
| C6 | KnowledgeProjection | C7 | IntentState | INTENT_REF | OPTIONAL |
| C6 | ConsolidationCandidate | C3 | VRFOutput (CRP+ M4) | VRF_REF | REQUIRED |
| C8 | SettlementResult | C5 | VerificationReport | CLAIM_REF | OPTIONAL |
| C8 | CapacityBid | C3 | ResourceSnapshot | TOPOLOGY_REF | OPTIONAL |

#### 2.5.2 Causal Traversal Algorithm

```
FUNCTION reconstruct_layer(
    target_layer: LayerID,
    corrupted_entities: Set<bytes32>,
    reference_registry: List<CrossLayerReference>,
    surviving_layers: Map<LayerID, LayerState>
) -> ReconstructionResult:

    // Phase 1: Identify all inbound references TO the corrupted entities
    inbound_refs = []
    FOR each ref IN reference_registry:
        IF ref.target_layer == target_layer
           AND ref.target_id IN corrupted_entities:
            inbound_refs.append(ref)

    // Phase 2: Identify all outbound references FROM the corrupted entities
    //          that point to surviving layers
    outbound_refs = []
    FOR each ref IN reference_registry:
        IF ref.source_layer == target_layer
           AND ref.source_id IN corrupted_entities
           AND ref.target_layer IN surviving_layers:
            outbound_refs.append(ref)

    // Phase 3: Causal traversal — reconstruct from surviving references
    reconstructed = {}
    work_queue = Queue(outbound_refs)
    visited = Set()
    iteration = 0

    WHILE NOT work_queue.empty() AND iteration < RECONSTRUCTION_MAX_ITERATIONS:
        ref = work_queue.dequeue()
        IF ref IN visited:
            CONTINUE
        visited.add(ref)
        iteration += 1

        // Attempt to reconstruct the source entity from the target
        target_state = surviving_layers[ref.target_layer].get(ref.target_id)
        IF target_state IS NOT NULL:
            partial = target_layer.reconstruct_from_reference(
                ref.source_id, ref, target_state)
            IF partial IS NOT NULL:
                reconstructed[ref.source_id] = merge(
                    reconstructed.get(ref.source_id), partial)

        // Follow transitive references from the target
        transitive_refs = find_references_from(ref.target_layer, ref.target_id,
                                                reference_registry)
        FOR each tref IN transitive_refs:
            IF tref NOT IN visited:
                work_queue.enqueue(tref)

    // Phase 4: Coverage assessment
    total_corrupted = len(corrupted_entities)
    fully_reconstructed = count(e FOR e IN corrupted_entities
                                IF e IN reconstructed
                                   AND reconstructed[e].is_complete())
    partially_reconstructed = count(e FOR e IN corrupted_entities
                                     IF e IN reconstructed
                                        AND NOT reconstructed[e].is_complete())

    RETURN ReconstructionResult {
        target_layer: target_layer,
        fully_reconstructed: fully_reconstructed,
        partially_reconstructed: partially_reconstructed,
        unrecoverable: total_corrupted - fully_reconstructed - partially_reconstructed,
        coverage: fully_reconstructed / total_corrupted,
        iterations: iteration,
        reconstructed_state: reconstructed
    }
```

**Complexity analysis:** O(R x W x N) where R = number of cross-layer references traversed, W = width of transitive reference graph (bounded by the maximum fan-out of any single entity's references), N = depth of traversal (bounded by RECONSTRUCTION_MAX_ITERATIONS). In practice, R is bounded by the reference registry size (~15 reference types x average entity count), W is bounded by the maximum reference fan-out (~10 for C7 intents), and N is bounded at 10 epochs of state.

#### 2.5.3 Triple-Criteria Termination Logic

```
FUNCTION should_terminate_reconstruction(
    result: ReconstructionResult,
    budget: ReconstructionBudget,
    previous_results: List<ReconstructionResult>
) -> (bool, TerminationReason):

    // Criterion 1: Coverage plateau
    //   If the last PLATEAU_WINDOW iterations improved coverage by less
    //   than PLATEAU_THRESHOLD, further reconstruction is unlikely to help
    IF len(previous_results) >= PLATEAU_WINDOW:
        recent_improvement = result.coverage - previous_results[-PLATEAU_WINDOW].coverage
        IF recent_improvement < PLATEAU_THRESHOLD:
            RETURN (true, COVERAGE_PLATEAU)

    // Criterion 2: Compute budget exhaustion
    //   Total reconstruction compute time must not exceed budget
    IF budget.elapsed_ticks >= budget.max_ticks:
        RETURN (true, BUDGET_EXHAUSTED)
    IF budget.iterations_used >= budget.max_iterations:
        RETURN (true, ITERATION_LIMIT)

    // Criterion 3: Total-loss comparison
    //   If reconstruction coverage is worse than what a full snapshot
    //   restore would provide, abandon reconstruction and snapshot-restore
    snapshot_coverage = estimate_snapshot_coverage(result.target_layer)
    IF result.coverage < snapshot_coverage * SNAPSHOT_ADVANTAGE_RATIO:
        RETURN (true, SNAPSHOT_PREFERRED)

    // Hard cap: 10 epochs regardless of other criteria
    IF budget.elapsed_ticks >= RECONSTRUCTION_HARD_CAP_TICKS:
        RETURN (true, HARD_CAP)

    RETURN (false, NONE)

STRUCTURE ReconstructionBudget:
    max_ticks:          uint64      // default: RECONSTRUCTION_HARD_CAP_TICKS
    max_iterations:     uint64      // default: RECONSTRUCTION_MAX_ITERATIONS
    elapsed_ticks:      uint64
    iterations_used:    uint64
```

#### 2.5.4 Coverage Estimation Per Layer

Based on the reference registry density and cross-layer reference availability:

| Layer | Estimated Reconstruction Coverage | Basis |
|-------|----------------------------------|-------|
| C8 DSF | ~90% | Most C8 state is deterministically replayable from EABS batches; AccountState reconstructible from surviving peers via EpochRecovery |
| C5 PCVM | ~75% | VTD chain reconstructible from VTD snapshots; credibility state partially reconstructible from C8 settlement records + C6 claim references |
| C3 Tidal | ~85% | Topology and hash ring deterministically derivable from agent roster; VRF seed deterministic from previous epoch; Known-Good Registry is small and replicable |
| C7 RIF | ~70% | Active intent state reconstructible from C3 scheduling records + C8 budget records; WAL replay covers most; completed intent history unrecoverable |
| C6 EMA | ~50% | Coherence graph structure partially reconstructible from C5 claim graph; SHREC regime reconstructible from current metrics; internal coherence metadata, catabolism history, vitality scores unrecoverable. This is the documented acceptable loss (MF-4). |

#### 2.5.5 API Contracts for Forward-Compatibility

Part III's API contracts are defined here so Parts I and II can be implemented without breaking changes when Part III arrives.

```
// Forward-compatible API: implemented as no-ops in Wave 2, activated in Wave 4+

INTERFACE ReconstructionEngine:
    // Called by RecoverySaga when witness verification identifies corruption
    FUNCTION initiate_reconstruction(
        target_layer: LayerID,
        corrupted_entities: Set<bytes32>,
        consistent_cut: ConsistentCut,
        budget: ReconstructionBudget
    ) -> ReconstructionHandle

    // Poll reconstruction progress
    FUNCTION get_progress(handle: ReconstructionHandle) -> ReconstructionResult

    // Cancel reconstruction (e.g., if governance intervenes)
    FUNCTION cancel(handle: ReconstructionHandle) -> void

    // Check if Part III is enabled
    FUNCTION is_enabled() -> bool
        // Wave 2: returns false
        // Wave 4+: returns PART_III_ENABLED config value

INTERFACE LayerReconstructionProvider:
    // Each layer implements this to declare its references and
    // provide reconstruction logic

    FUNCTION get_outbound_references() -> List<CrossLayerReference>
    FUNCTION get_inbound_references() -> List<CrossLayerReference>

    FUNCTION reconstruct_from_reference(
        entity_id: bytes32,
        reference: CrossLayerReference,
        target_state: bytes          // state from the referenced layer
    ) -> PartialReconstruction?

    FUNCTION merge_reconstructions(
        entity_id: bytes32,
        partials: List<PartialReconstruction>
    ) -> ReconstructedEntity?

STRUCTURE PartialReconstruction:
    entity_id:      bytes32
    layer:          LayerID
    fields:         Map<string, bytes>  // which fields were reconstructed
    confidence:     float               // 0.0-1.0, how confident the reconstruction is
    source_ref:     CrossLayerReference // which reference provided this data

STRUCTURE ReconstructedEntity:
    entity_id:      bytes32
    layer:          LayerID
    full_state:     bytes               // reconstructed state
    is_complete:    bool                // all required fields present?
    confidence:     float               // aggregate confidence
    sources:        List<CrossLayerReference>  // provenance
```

### 2.6 C5 VTD Snapshot Protocol

C5 PCVM currently maintains VTD chains but has no state snapshot mechanism (identified as a gap in feasibility). This section specifies the VTD hash chain and periodic snapshot protocol that C34 requires from C5.

#### 2.6.1 VTD Hash Chain Specification

The VTD hash chain is a cryptographic chain linking every VTD processed by C5 in causal order:

```
STRUCTURE VTDHashChainEntry:
    sequence_number:    uint64          // monotonically increasing
    vtd_hash:           bytes32         // SHA-256 of the VTD content
    claim_class:        ClaimClass      // D/C/P/R/E/S/K/H/N
    agent_id:           bytes32         // producing agent
    tick:               uint64          // settlement tick when processed
    previous_chain_hash: bytes32        // hash of previous entry (chain link)
    chain_hash:         bytes32         // SHA-256(sequence ‖ vtd_hash ‖ claim_class
                                        //          ‖ agent_id ‖ tick ‖ previous_chain_hash)

// Chain construction
FUNCTION append_to_vtd_chain(
    chain: VTDHashChain,
    vtd: VTD,
    tick: uint64
) -> VTDHashChainEntry:
    entry = VTDHashChainEntry {
        sequence_number: chain.tip.sequence_number + 1,
        vtd_hash: SHA256(vtd.serialize()),
        claim_class: vtd.claim_class,
        agent_id: vtd.agent_id,
        tick: tick,
        previous_chain_hash: chain.tip.chain_hash,
        chain_hash: SHA256(
            entry.sequence_number ‖ entry.vtd_hash ‖ entry.claim_class
            ‖ entry.agent_id ‖ entry.tick ‖ entry.previous_chain_hash
        )
    }
    chain.entries.append(entry)
    chain.tip = entry
    RETURN entry

// Chain verification
FUNCTION verify_vtd_chain(chain: VTDHashChain) -> bool:
    FOR i FROM 1 TO len(chain.entries) - 1:
        entry = chain.entries[i]
        prev = chain.entries[i - 1]
        expected_hash = SHA256(
            entry.sequence_number ‖ entry.vtd_hash ‖ entry.claim_class
            ‖ entry.agent_id ‖ entry.tick ‖ prev.chain_hash
        )
        IF entry.chain_hash != expected_hash:
            RETURN false
        IF entry.previous_chain_hash != prev.chain_hash:
            RETURN false
    RETURN true
```

#### 2.6.2 Opinion Snapshot Format and Interval

C5 takes periodic snapshots of its credibility state at TIDAL_EPOCH boundaries:

```
STRUCTURE C5OpinionSnapshot:
    epoch:                  uint64          // TIDAL_EPOCH number
    tick:                   uint64          // SETTLEMENT_TICK at snapshot
    vtd_chain_tip:          bytes32         // chain_hash of last VTD at snapshot
    vtd_chain_sequence:     uint64          // sequence_number at snapshot

    // Aggregate credibility state
    agent_credibilities:    Map<AgentID, AgentCredibilityState>
    claim_class_stats:      Map<ClaimClass, ClassStatistics>

    // CACT state (if C11 active)
    cact_commitment_tips:   Map<AgentID, bytes32>   // per-agent commitment chain tips

    // Snapshot integrity
    snapshot_hash:          bytes32         // SHA-256 of all above fields
    signature:              Ed25519Sig      // C5's signature over snapshot_hash

STRUCTURE AgentCredibilityState:
    agent_id:               AgentID
    overall_credibility:    OpinionTuple    // (belief, disbelief, uncertainty)
    per_class_credibility:  Map<ClaimClass, OpinionTuple>
    sample_size:            uint64
    last_update_tick:       uint64

STRUCTURE ClassStatistics:
    claim_class:            ClaimClass
    total_claims:           uint64
    verified_claims:        uint64
    deep_audited_claims:    uint64
    average_credibility:    float

// Snapshot interval: every TIDAL_EPOCH boundary (every 60 ticks)
// Storage: retained for SNAPSHOT_RETENTION_EPOCHS TIDAL_EPOCHS
// Size estimate: ~1 KB per agent x 10,000 agents = ~10 MB per snapshot
//                x 10 snapshots retained = ~100 MB total
```

#### 2.6.3 Replay Procedure

To recover C5 state from a snapshot:

```
FUNCTION replay_c5_from_snapshot(
    snapshot: C5OpinionSnapshot,
    vtd_chain: VTDHashChain,
    target_tick: uint64
) -> C5RecoveryResult:

    // Step 1: Load snapshot state
    state = C5State.from_snapshot(snapshot)
    start_sequence = snapshot.vtd_chain_sequence

    // Step 2: Verify chain continuity from snapshot to current
    IF vtd_chain.entries[start_sequence].chain_hash != snapshot.vtd_chain_tip:
        RETURN C5RecoveryResult.CHAIN_BREAK(
            expected = snapshot.vtd_chain_tip,
            actual = vtd_chain.entries[start_sequence].chain_hash
        )

    // Step 3: Replay VTD chain entries from snapshot to target
    replayed = 0
    FOR each entry IN vtd_chain.entries[start_sequence + 1 ..]:
        IF entry.tick > target_tick:
            BREAK

        // Apply credibility update from this VTD
        state.apply_vtd_credibility_update(entry)
        replayed += 1

    // Step 4: Verify replay result against expected digest
    replay_digest = state.compute_digest()

    RETURN C5RecoveryResult {
        status: SUCCESS,
        state: state,
        replay_digest: replay_digest,
        entries_replayed: replayed,
        replay_time_ms: elapsed(),
        snapshot_epoch: snapshot.epoch,
        target_tick: target_tick
    }

// Expected replay time: ~1ms per 1000 VTD entries
// At peak load (~100 VTDs per tick, 60 ticks per epoch):
//   Worst-case replay from epoch boundary: 6000 entries = ~6ms
//   Worst-case replay from last snapshot (10 epochs): 60000 entries = ~60ms
```

---

## 3. Cross-Layer Integration

### 3.1 How C34 Extends C9 Integration Contracts

C34 adds the following entries to the C9 Integration Contract Directory (SS9):

```
## 9.4 Recovery Fabric Contracts (C34)

C34 defines cross-cutting recovery obligations for all stateful layers.
Unlike defense systems (C11-C13), C34 is not a cross-cutting instrument
but a cross-cutting protocol — it specifies interfaces that each layer
must implement, not a subsystem that instruments existing pipelines.

### 9.4.1 Always-On Obligations (Normal Operation)

Every stateful layer (C3, C5, C6, C7, C8) MUST:
  1. Compute its state digest at every SETTLEMENT_TICK boundary
  2. Sign the digest with its layer identity key
  3. Broadcast the signed digest via C3 CRDT replication
  4. Record signed digests received from all layers it depends on
     (per the consumer dependency map in SS2.1.4)
  5. Maintain a DigestHistoryTree for DIGEST_RETENTION_TICKS ticks
  6. Maintain a ConsumerDigestLog for DIGEST_RETENTION_TICKS ticks

### 9.4.2 Recovery Obligations

Every stateful layer MUST:
  1. Implement a ROSC (Reduced Operational State Configuration)
  2. Implement synchronization predicate checks for all upstream layers
  3. Respond to LayerReadyAnnouncement messages during pre-C7 recovery
  4. Participate in witness verification (provide Merkle proofs on request)
  5. Sign the RecoveryCompletionAttestation when verification succeeds
  6. Implement LayerReconstructionProvider interface (no-op until Wave 4+)

### 9.4.3 Authority Hierarchy Preservation

C34 recovery MUST NOT override:
  - C5's sovereignty over claim classification (INV-C1)
  - C8's sovereignty over settlement (INV-S1)
  - C3's sovereignty over spatial coordination
  - C6's sovereignty over knowledge metabolism
  - C7's sovereignty over intent orchestration

Recovery reconciliation is authority-directed:
  - Claims discrepancies: resolved by C5 (source of truth)
  - Settlement discrepancies: resolved by C8 (source of truth)
  - All other discrepancies: resolved by the authoritative layer per C9 SS1.3
```

### 3.2 Per-Layer C34 Implementation Obligations

#### 3.2.1 C8 DSF Obligations

```
// C8 additions for C34 support

// 1. Digest computation — marginal cost ~0ms (settlement_hash already exists)
FUNCTION c32_compute_digest(state: SettlementState) -> bytes32:
    RETURN SHA256(
        state.settlement_hash
        ‖ uint64_to_bytes(state.epoch_number)
        ‖ uint64_to_bytes(state.total_aic_supply)
        ‖ bool_to_byte(state.conservation_valid)
    )

// 2. Recovery interface — wraps existing EpochRecovery
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C8RecoveryResult:
    target_epoch = consistent_cut.tick / TICKS_PER_TIDAL_EPOCH
    // Use existing EpochRecovery protocol
    result = EpochRecovery(self.node_id, target_epoch)
    IF result.success:
        broadcast(LayerReadyAnnouncement {
            layer: C8_DSF,
            state_digest: c32_compute_digest(self.state),
            epoch: self.state.epoch_number,
            rosc_status: READY
        })
    RETURN result

// 3. No new C8 data structures required — DigestHistoryTree and
//    ConsumerDigestLog are appended to HDL node state
```

#### 3.2.2 C5 PCVM Obligations

```
// C5 additions for C34 support

// 1. VTD hash chain (new — SS2.6.1)
//    Integrated into existing VTD processing pipeline
//    Cost: 1 SHA-256 per VTD processed (~0.001ms)

// 2. Opinion snapshots (new — SS2.6.2)
//    Taken at TIDAL_EPOCH boundaries
//    Cost: ~10ms per snapshot (serialize agent credibilities)

// 3. Digest computation
FUNCTION c32_compute_digest(state: C5State) -> bytes32:
    RETURN SHA256(
        state.vtd_chain.tip.chain_hash
        ‖ state.credibility_snapshot_hash()
        ‖ uint64_to_bytes(state.pending_claims.count())
        ‖ uint64_to_bytes(state.opinion_count)
    )

// 4. Recovery interface
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C5RecoveryResult:
    // Find nearest snapshot before consistent_cut tick
    snapshot = find_nearest_snapshot(consistent_cut.tick)
    // Replay VTD chain from snapshot
    result = replay_c5_from_snapshot(snapshot, self.vtd_chain, consistent_cut.tick)
    // Verify C8 consistency
    c8_digest = self.consumer_log.get(C8_DSF, consistent_cut.tick)
    IF c8_digest IS NOT NULL:
        // Check predicate PRED_C8C5_SETTLEMENT
        // (verified during predicate check in boot sequence)
        PASS
    broadcast(LayerReadyAnnouncement { ... })
    RETURN result
```

#### 3.2.3 C3 Tidal Obligations

```
// C3 additions for C34 support

// 1. Digest computation
FUNCTION c32_compute_digest(state: C3State) -> bytes32:
    RETURN SHA256(
        uint64_to_bytes(state.topology_version)
        ‖ state.hash_ring_hash()
        ‖ state.vrf_seed
        ‖ uint8_to_byte(state.safe_mode_state)
        ‖ state.known_good_registry.registry_hash
    )

// 2. Recovery interface — wraps existing ETR/SAFE_MODE
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C3RecoveryResult:
    // If in SAFE_MODE, C3 is already in a safe state
    IF self.state.safe_mode_state == SAFE_MODE:
        // SAFE_MODE guarantees correctness; C34 just verifies consistency
        PASS
    ELSE:
        // Reconstruct topology from known-good registry + agent roster
        self.reconstruct_topology(consistent_cut.tick)
        // Reconstruct VRF seed deterministically
        self.recompute_vrf_seed(consistent_cut.tick)

    broadcast(LayerReadyAnnouncement { ... })
    RETURN C3RecoveryResult { ... }

// 3. CRDT broadcast for digest distribution
//    C34 digests piggyback on existing C3 CRDT replication
//    No new broadcast protocol required
```

#### 3.2.4 C7 RIF Obligations

```
// C7 additions for C34 support

// 1. Digest computation
FUNCTION c32_compute_digest(state: C7State) -> bytes32:
    RETURN SHA256(
        state.isr_crdt.hash()
        ‖ uint64_to_bytes(state.active_saga_count)
        ‖ state.wal.tip_hash()
        ‖ state.pe_roster.hash()
    )

// 2. Recovery Coordinator — new C7 component (SS2.3)
//    The RecoverySaga is a specialized saga type added to C7's
//    existing saga infrastructure

// 3. WAL persistence of RecoverySaga state
//    RecoverySaga state transitions are WAL-logged like all other
//    C7 state mutations

// 4. Recovery interface — wraps existing WAL replay + ISR reconciliation
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C7RecoveryResult:
    // Replay WAL from last checkpoint
    wal_result = self.replay_wal()
    // Reconcile ISR state with PEs
    isr_result = self.reconcile_isr()
    // Verify upstream layer consistency
    // (handled by RecoverySaga predicate checks)
    RETURN C7RecoveryResult { ... }
```

#### 3.2.5 C6 EMA Obligations

```
// C6 additions for C34 support

// 1. Digest computation — uses incrementally maintained Merkle root
FUNCTION c32_compute_digest(state: C6State) -> bytes32:
    RETURN SHA256(
        state.coherence_graph.merkle_root()
        ‖ uint8_to_byte(state.shrec_controller.current_regime)
        ‖ uint64_to_bytes(state.active_quanta_count)
        ‖ uint64_to_bytes(state.quarantine_queue.count())
        ‖ uint64_to_bytes(state.last_consolidation_epoch)
    )

// 2. Incremental Merkle root for coherence graph
//    The coherence graph is already sharded (INV-E15 through INV-E19).
//    Each shard maintains a local Merkle root. The global Merkle root
//    is SHA-256 of the concatenation of shard roots (sorted by shard ID).
//    Update cost: O(log Q) per quantum change where Q = quanta per shard.
//    Total digest cost per tick: O(S * log Q) where S = number of shards.
//    At S=10, Q=100,000: ~0.3ms per tick — well within 4ms budget.

// 3. Recovery interface — wraps existing opinion freeze + queue drain
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C6RecoveryResult:
    // Freeze opinions (existing mechanism)
    self.freeze_opinions()
    // Drain in-progress queues (existing mechanism)
    self.drain_queues()
    // Apply quarantine to in-progress consolidation (existing 3-epoch window)
    self.quarantine_in_progress()
    // Rebuild coherence graph from surviving shards
    self.rebuild_coherence_graph()
    // Restore SHREC controller from last known regime
    self.restore_shrec()

    // Note: ~50% of C6 state may be unrecoverable (MF-4)
    // Internal coherence metadata, catabolism history, vitality scores
    // are acceptable losses. Coherence graph structure is partially
    // reconstructible from C5 claim records.

    RETURN C6RecoveryResult { ... }
```

### 3.3 Interface Definitions

#### 3.3.1 APIs

```
// C34 Recovery Fabric API — implemented by each layer

INTERFACE C34LayerInterface:
    // Always-on (normal operation)
    FUNCTION compute_digest() -> bytes32
    FUNCTION get_digest(tick: uint64) -> TickDigest?
    FUNCTION get_merkle_proof(tick: uint64) -> MerkleProof?
    FUNCTION get_consumer_digest(source: LayerID, tick: uint64) -> ReceivedDigest?
    FUNCTION get_nearest_consumer_digest(source: LayerID, tick: uint64,
                                          max_skip: uint64) -> ReceivedDigest?

    // Recovery
    FUNCTION recover(consistent_cut: ConsistentCut) -> LayerRecoveryResult
    FUNCTION check_predicate(predicate_id: string, upstream_state: bytes32) -> PredicateResult
    FUNCTION rollback_to_tick(tick: uint64) -> bool
    FUNCTION sign_attestation(attestation_hash: bytes32) -> Ed25519Sig

    // Part III (forward-compatible, no-op in Wave 2)
    FUNCTION get_outbound_references() -> List<CrossLayerReference>
    FUNCTION get_inbound_references() -> List<CrossLayerReference>
    FUNCTION reconstruct_from_reference(entity_id: bytes32, ref: CrossLayerReference,
                                         target_state: bytes) -> PartialReconstruction?

// C34 Recovery Coordinator API — implemented by C7 only

INTERFACE C34RecoveryCoordinator:
    FUNCTION initiate_recovery(trigger: RecoveryTrigger) -> SagaID
    FUNCTION get_recovery_status(saga_id: SagaID) -> RecoverySagaState
    FUNCTION cancel_recovery(saga_id: SagaID) -> void
    FUNCTION get_completion_attestation(saga_id: SagaID) -> RecoveryCompletionAttestation?
```

#### 3.3.2 Events

```
// Events emitted by C34 components

EVENT DigestComputed:
    layer:      LayerID
    tick:       uint64
    digest:     bytes32
    signature:  Ed25519Sig

EVENT RecoveryInitiated:
    saga_id:    SagaID
    trigger:    RecoveryTrigger
    tick:       uint64
    affected_layers: List<LayerID>

EVENT LayerRecoveryStarted:
    saga_id:    SagaID
    layer:      LayerID
    tick:       uint64

EVENT LayerRecoveryComplete:
    saga_id:    SagaID
    layer:      LayerID
    tick:       uint64
    digest:     bytes32
    rosc_status: ROSCStatus

EVENT PredicateChecked:
    saga_id:    SagaID
    predicate:  string
    result:     PredicateResult
    source:     LayerID
    consumer:   LayerID

EVENT WitnessVerificationComplete:
    saga_id:    SagaID
    source:     LayerID
    consumer:   LayerID
    result:     WitnessResult

EVENT RecoveryComplete:
    saga_id:    SagaID
    tick:       uint64
    attestation: RecoveryCompletionAttestation

EVENT RecoveryFailed:
    saga_id:    SagaID
    tick:       uint64
    reason:     string
    escalation: GOVERNANCE | MANUAL | SNAPSHOT_RESTORE
```

#### 3.3.3 Data Structures Summary

| Structure | Defined In | Used By | Cardinality |
|-----------|-----------|---------|-------------|
| TickDigest | SS2.1.2 | All layers | 1 per layer per tick |
| DigestHistoryTree | SS2.1.2 | All layers | 1 per layer |
| ConsumerDigestLog | SS2.1.4 | All layers | 1 per layer |
| ReceivedDigest | SS2.1.4 | All layers | N per layer (from each dependency) |
| ConsistentCut | SS2.2.3 | Recovery Coordinator | 1 per recovery event |
| ROSCSpec | SS2.2.4 | All layers | 1 per layer (static) |
| RecoverySaga | SS2.3.1 | C7 RIF | 1 per recovery event |
| WitnessResult | SS2.4.1 | Witness Verification Engine | 1 per layer pair per verification |
| RecoveryCompletionAttestation | SS2.4.4 | All layers | 1 per successful recovery |
| CrossLayerReference | SS2.5.1 | Reconstruction Engine | N per layer (static registry) |
| VTDHashChainEntry | SS2.6.1 | C5 PCVM | 1 per VTD processed |
| C5OpinionSnapshot | SS2.6.2 | C5 PCVM | 1 per TIDAL_EPOCH |

---

## 4. State Machine

### 4.1 System-Level Recovery State Machine

```
ENUM SystemRecoveryState:
    NORMAL              // All layers operational, digest engine running
    DETECTING           // Multi-layer failure detected, assessing scope
    BOOTING             // Black-start boot sequence in progress
    VERIFYING           // Witness verification in progress
    RECONSTRUCTING      // Part III adversarial reconstruction (Wave 4+)
    VERIFIED            // All witnesses consistent, assembling attestation
    NORMAL              // Recovery complete (returns to NORMAL)

// Note: This state machine is ORTHOGONAL to C3's SAFE_MODE state machine.
// C3 may be in SAFE_MODE independently of C34 recovery state.
// If C3 is in SAFE_MODE when C34 recovery begins, C34 does not exit
// C3's SAFE_MODE — that requires separate Standard ETR governance vote.
```

### 4.2 State Transitions

```
NORMAL → DETECTING:
    Guard:  multi_layer_failure_detected()
            (>=2 layers report DEGRADED or UNREACHABLE within
             FAILURE_DETECTION_WINDOW ticks)
    Action: create RecoverySaga
            compute consistent_cut from digest history
            identify affected layers

DETECTING → BOOTING:
    Guard:  consistent_cut computed successfully
            OR no consistent cut found (will use oldest available digests)
    Action: initiate C8 recovery (Step 1)
            saga.state = BOOTING_C8

DETECTING → NORMAL:
    Guard:  false alarm — affected layers self-recovered before saga started
    Action: cancel saga, log false alarm

BOOTING → BOOTING:
    Guard:  current boot step complete, next step pending
    Action: advance to next layer in boot order
            (internal sub-transitions: BOOTING_C8 → BOOTING_C5 → ... → BOOTING_C6)

BOOTING → VERIFYING:
    Guard:  all 5 layers report READY
            all synchronization predicates SATISFIED
    Action: initiate witness verification for all layer pairs

BOOTING → FAILED:
    Guard:  any layer recovery FAILED
            OR any synchronization predicate VIOLATED_MAJOR
            OR saga timeout exceeded
    Action: escalate to governance
            attempt per-layer snapshot restore as fallback

VERIFYING → VERIFIED:
    Guard:  all witness pairs CONSISTENT
            OR flagged layers successfully overridden (authority fallback)
    Action: build RecoveryCompletionAttestation
            request signatures from all layers

VERIFYING → RECONSTRUCTING:
    Guard:  witness verification identifies unrecoverable corruption
            AND PART_III_ENABLED
    Action: initiate causal reconstruction for corrupted layers

VERIFYING → FAILED:
    Guard:  witness verification identifies unrecoverable corruption
            AND NOT PART_III_ENABLED
    Action: fall back to full snapshot restore (degraded mode — MF-2)
            OR escalate to governance

RECONSTRUCTING → VERIFIED:
    Guard:  reconstruction complete
            coverage exceeds RECONSTRUCTION_MIN_COVERAGE
    Action: re-run witness verification on reconstructed state

RECONSTRUCTING → FAILED:
    Guard:  reconstruction terminated (any termination criterion)
            AND coverage below RECONSTRUCTION_MIN_COVERAGE
    Action: fall back to full snapshot restore
            escalate to governance

VERIFIED → NORMAL:
    Guard:  RecoveryCompletionAttestation signed by all 5 layers
    Action: transition system to NORMAL
            log attestation
            emit RecoveryComplete event
            resume normal digest computation
```

### 4.3 State Transition Diagram

```
                    multi-layer failure
           ┌──────────────────────────────┐
           │                              ▼
        NORMAL                       DETECTING
           ▲                         /        \
           │                false   /          \ consistent cut
           │               alarm   /            \ computed
           │                      ▼              ▼
           │                   NORMAL          BOOTING
           │                                  /      \
           │                   all READY     /        \ layer FAILED
           │                   + predicates /          \ or timeout
           │                              ▼            ▼
           │                          VERIFYING      FAILED
           │                         /    |    \        ▲
           │            consistent  /     |     \      │
           │                       /      |      \     │
           │                      ▼       │       ▼    │
           │                  VERIFIED    │   RECONSTRUCTING
           │                      │       │       │    │
           │      all signed      │       │       │    │
           │                      │       │   coverage │
           │                      ▼       │   < min   │
           └──────────────────NORMAL      └───────────┘
```

---

## 5. Parameters Table

### 5.1 Always-On Parameters (State Digest Engine)

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| DIGEST_BUDGET_MS | 4 | 1-10 | OPERATIONAL | Maximum time per layer for digest computation per tick |
| DIGEST_RETENTION_TICKS | 36000 | 3600-108000 | GOVERNANCE | Number of ticks of digest history retained (default = 1 CONSOLIDATION_CYCLE) |
| TRUST_WEIGHT_MIN | 0.1 | 0.01-0.5 | OPERATIONAL | Minimum temporal trust weight for fresh digests |
| TRUST_WEIGHT_MAX | 1.0 | 0.5-1.0 | OPERATIONAL | Maximum temporal trust weight for aged digests |
| TRUST_GROWTH_RATE | 0.1 | 0.01-0.5 | OPERATIONAL | Logarithmic growth rate for temporal trust |
| DIGEST_LOSS_TOLERANCE | 5 | 1-10 | OPERATIONAL | Maximum consecutive missing consumer digests before alert |

### 5.2 Recovery Protocol Parameters

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| FAILURE_DETECTION_WINDOW | 5 | 2-15 | OPERATIONAL | Ticks within which >=2 layer failures trigger C34 recovery |
| MAX_CONSISTENT_CUT_SEARCH_WINDOW | 600 | 60-3600 | GOVERNANCE | Maximum ticks to search backward for consistent cut |
| SELF_COORD_TIMEOUT | 30 | 10-60 | OPERATIONAL | Ticks to wait for upstream LayerReadyAnnouncement (pre-C7) |
| RECOVERY_SAGA_TIMEOUT | 600 | 120-1800 | GOVERNANCE | Maximum ticks for entire recovery saga before FAILED |
| MAX_DIGEST_SKIP | 5 | 1-10 | OPERATIONAL | Maximum tick gap when searching for nearest consumer digest |

### 5.3 Witness Verification Parameters

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| WITNESS_TIMEOUT | 10 | 5-30 | OPERATIONAL | Ticks allowed for each witness verification pair |
| AUTHORITY_OVERRIDE_SEARCH_WINDOW | 3600 | 600-36000 | GOVERNANCE | Ticks to search for multiply-attested snapshot on override |

### 5.4 Part III (Reconstruction) Parameters

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| PART_III_ENABLED | false | true/false | GOVERNANCE | Enable adversarial reconstruction (Wave 4+) |
| RECONSTRUCTION_MAX_ITERATIONS | 100000 | 10000-1000000 | GOVERNANCE | Maximum traversal iterations |
| RECONSTRUCTION_HARD_CAP_TICKS | 6000 | 600-36000 | GOVERNANCE | Hard cap: 10 TIDAL_EPOCHS = 10 hours |
| PLATEAU_WINDOW | 5 | 3-10 | OPERATIONAL | Iterations to check for coverage plateau |
| PLATEAU_THRESHOLD | 0.001 | 0.0001-0.01 | OPERATIONAL | Minimum improvement to avoid plateau termination |
| SNAPSHOT_ADVANTAGE_RATIO | 0.8 | 0.5-1.0 | OPERATIONAL | If reconstruction coverage < snapshot_coverage * this, prefer snapshot |
| RECONSTRUCTION_MIN_COVERAGE | 0.6 | 0.3-0.9 | GOVERNANCE | Minimum coverage to accept reconstruction result |

### 5.5 C5 Snapshot Parameters

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| SNAPSHOT_INTERVAL | 60 | 30-120 | OPERATIONAL | Ticks between C5 opinion snapshots (default = 1 TIDAL_EPOCH) |
| SNAPSHOT_RETENTION_EPOCHS | 10 | 5-100 | GOVERNANCE | TIDAL_EPOCHS of C5 snapshots retained |

---

## 6. Formal Properties

### 6.1 Invariants

**INV-R1 (Digest Completeness).** At every SETTLEMENT_TICK boundary, every operational stateful layer MUST have computed and signed a state digest. If a layer fails to produce a digest for DIGEST_LOSS_TOLERANCE consecutive ticks, it is considered DEGRADED.

**INV-R2 (Consumer-Side Acyclicity).** Consumer-side digest recording is strictly unidirectional. Layer L_i's digest is computed exclusively from L_i's own state. No layer's digest computation may depend on another layer's recording of its digest. This prevents circular dependencies.

**INV-R3 (Boot Order Monotonicity).** During recovery, layers boot in strict order C8 -> C5 -> C3 -> C7 -> C6. No layer may begin recovery before all layers preceding it in the boot order have reported READY and satisfied their synchronization predicates.

**INV-R4 (Predicate Exhaustiveness).** The set of synchronization predicates is exhaustive with respect to the C9 integration contract directory. For every bidirectional or consumer relationship in the C9 contract matrix, at least one synchronization predicate exists. New C9 contracts automatically generate new predicates (SS2.2.2 extensibility rule).

**INV-R5 (Authority Preservation).** C34 recovery MUST NOT override the authoritative layer's state with consumer-side data unless the authority-override quorum is reached (strict majority of verifiable consumers disagree with authority). Even then, the authority is rolled back to its own historical state (a multiply-attested snapshot), not replaced with consumer-derived state.

**INV-R6 (Attestation Completeness).** A RecoveryCompletionAttestation is valid if and only if all five stateful layers have signed it. Recovery is not considered complete until a valid attestation exists.

**INV-R7 (Digest Budget).** Digest computation per layer MUST NOT exceed DIGEST_BUDGET_MS milliseconds. If a layer's digest computation consistently exceeds this budget, the layer MUST simplify its digest (e.g., reduce Merkle depth) rather than violate the timing constraint.

**INV-R8 (Conservation Through Recovery).** C8's CONS-1 invariant (AIC conservation) MUST hold at all times, including during and after recovery. If recovery produces a C8 state that violates CONS-1, the recovery MUST be rejected and C8 MUST fall back to its own ConservationRecovery protocol.

### 6.2 Safety Properties

**SAFE-1 (No Phantom State).** Recovery MUST NOT introduce state that did not exist before the failure. A recovered layer's state at tick T must be derivable from the layer's state at some tick T' <= T, plus deterministic replay of operations between T' and T.

**SAFE-2 (No Settlement Divergence).** After recovery, all C8 HDL nodes MUST agree on the same settlement_hash. If any node's post-recovery settlement_hash differs, EpochRecovery is re-triggered for that node.

**SAFE-3 (No Credential Inflation).** Recovery MUST NOT increase any agent's credibility score beyond its pre-failure value. If C5 state is reconstructed, credibility scores are capped at the values in the most recent consistent C5 opinion snapshot.

**SAFE-4 (No Boot Order Violation).** It is impossible for a later-boot layer to reach READY state before an earlier-boot layer. The self-coordination protocol and saga state machine enforce this through await_announcement blocking.

**SAFE-5 (No Circular Recovery).** Recovery of layer L_i MUST NOT depend on layer L_j if L_j's boot order is later than L_i's. The boot dependency DAG is acyclic by construction.

**SAFE-6 (No Silent Data Corruption).** If adversarial state corruption occurs and is not detected by witness verification, the system MUST NOT silently operate on corrupted state. The temporal trust gradient ensures that recently-computed digests are treated with lower trust, and any digest inconsistency triggers investigation.

### 6.3 Liveness Properties

**LIVE-1 (Recovery Termination).** Every initiated recovery saga MUST terminate within RECOVERY_SAGA_TIMEOUT ticks, either with a valid RecoveryCompletionAttestation (success) or a FAILED state with governance escalation.

**LIVE-2 (Reconstruction Termination).** Every initiated adversarial reconstruction MUST terminate via one of the three criteria (coverage plateau, budget exhaustion, snapshot comparison) or the 10-epoch hard cap. Infinite reconstruction is impossible.

**LIVE-3 (Digest Availability).** Under the assumption that at least one node per layer survives a failure, at least one copy of every digest within DIGEST_RETENTION_TICKS is available for recovery.

**LIVE-4 (Predicate Resolution).** Every synchronization predicate evaluation MUST produce a result (SATISFIED, VIOLATED_MINOR, VIOLATED_MAJOR, or UNVERIFIABLE) within SELF_COORD_TIMEOUT ticks. No predicate evaluation may block indefinitely.

**LIVE-5 (Progressive Recovery).** If full cross-layer recovery fails, the system MUST degrade to per-layer recovery (each layer's existing mechanisms). Per-layer recovery is always available as a fallback — C34 adds coordination but never removes the per-layer safety net.

**LIVE-6 (Eventual Consistency).** After a successful recovery (valid attestation), all layers MUST reach a mutually consistent state within 1 TIDAL_EPOCH. "Mutually consistent" means all synchronization predicates evaluate to SATISFIED.

---

## Appendix A: Predicate-to-C9-Contract Traceability Matrix

| Predicate ID | C9 Contract | C9 Section | Direction | Layer Pair |
|-------------|-------------|------------|-----------|------------|
| PRED_C8_READY | (internal) | — | — | C8 self |
| PRED_C5_READY | (internal) | — | — | C5 self |
| PRED_C8C5_SETTLEMENT | "C5 -> C8: Verification reports" | SS9.2 | C8 → C5 | C8, C5 |
| PRED_C3_READY | (internal) | — | — | C3 self |
| PRED_C8C3_CRDT | "C3 <-> C8: CRDT infrastructure" | SS9.2 | C8 → C3 | C8, C3 |
| PRED_C5C3_VERIFICATION | "C5 -> C3: Verification results" | SS9.2 | C5 → C3 | C5, C3 |
| PRED_C3C5_VRF | "C3 -> C5: VRF output per tidal epoch" | SS9.2 | C3 → C5 | C3, C5 |
| PRED_C7_READY | (internal) | — | — | C7 self |
| PRED_C3C7_SCHEDULING | "C3 <-> C7: scheduling, topology" | SS9.2 | C3 → C7 | C3, C7 |
| PRED_C5C7_CREDIBILITY | "C5 -> C7: Agent credibility" | SS9.2 | C5 → C7 | C5, C7 |
| PRED_C8C7_STAKE | "C7 <-> C8: stake queries" | SS9.2 | C8 → C7 | C8, C7 |
| PRED_C7C3_INTENTS | "C7 submits leaf intents" | SS9.2 | C7 → C3 | C7, C3 |
| PRED_C7C8_BUDGETS | "C7 submits intent budgets" | SS9.2 | C7 → C8 | C7, C8 |
| PRED_C6_READY | (internal) | — | — | C6 self |
| PRED_C5C6_CLAIMS | "C5 <-> C6: MCTs, VTDs, classification" | SS9.2 | C5 → C6 | C5, C6 |
| PRED_C7C6_PROJECTIONS | "C6 -> C7: Knowledge projections" | SS9.2 | C7 → C6 | C7, C6 |
| PRED_C3C6_EPOCH | "C3 -> C6: Epoch boundary notifications" | SS9.2 | C3 → C6 | C3, C6 |
| PRED_C6C5_KCLASS | "C6 submits K-class VTDs" | SS9.2 | C6 → C5 | C6, C5 |
| PRED_C6C7_KNOWLEDGE | "C6 -> C7: Knowledge projections" | SS9.2 | C6 → C7 | C6, C7 |
| PRED_C6C8_METABOLIC | "C6 -> C8: Contribution reports" | SS9.2 | C6 → C8 | C6, C8 |
| PRED_C6C3_SUMMARIES | "C6 -> C3: Knowledge summaries" | SS9.2 | C6 → C3 | C6, C3 |
| PRED_C11_CACT | "C11 <-> C5: CACT extension" | SS9.3.1 | C11 ↔ C5 | C11, C5 |
| PRED_C12_AVAP | "C12 <-> C3/C5: AVAP VRF/opinions" | SS9.3.2 | C12 ↔ C3/C5 | C12, C3/C5 |
| PRED_C13_CRP | "C13 <-> C6: CRP+ immune memory" | SS9.3.3 | C13 ↔ C6 | C13, C6 |

## Appendix B: Monitoring Flag Resolutions

| Flag | Status | Resolution |
|------|--------|------------|
| MF-1 (Authority-directed reconciliation) | ADDRESSED | Authority-override quorum defined (SS2.4.3). Detectable corruption classes: any corruption that produces digest inconsistency with majority of consumers. Undetectable: collusion across 4+ layers (acknowledged in feasibility as residual risk). |
| MF-2 (Part III deferral) | ADDRESSED | Explicit degraded-mode path specified (SS2.4.3): pre-Wave-4, unrecoverable corruption triggers full snapshot restore. PART_III_ENABLED parameter gates activation. |
| MF-3 (Predicate extensibility) | ADDRESSED | Extensibility rule in SS2.2.2: new C9 contracts automatically generate predicates. Predicate generation is mechanical, not design-time. |
| MF-4 (C6 reconstruction coverage ~50%) | ADDRESSED | Unrecoverable C6 state documented in ROSC_C6 (SS2.2.4): internal coherence metadata, catabolism history, vitality scores. Acceptable loss bounds: coherence graph structure recoverable from C5 claims; SHREC regime recoverable from current metrics; dreaming pipeline restarts at next CONSOLIDATION_CYCLE. |
| MF-5 (36,000s consistent-cut gap) | ADDRESSED | Gap analysis in SS2.2.3: 36,000s gap applies only to C6 state. C8 settlement gap is 60s (1 tick). C5 verification gap is 3,600s (1 TIDAL_EPOCH). For settlement recovery, the relevant gap is 60s. |

## Appendix C: Glossary

| Term | Definition |
|------|-----------|
| Black-start | Recovery from a state where multiple layers are simultaneously unavailable, analogous to power grid black-start procedures |
| Consistent cut | A set of per-layer state snapshots where no snapshot references state newer than any other snapshot in the set |
| Consumer-side audit trail | Digests recorded by consuming layers of state received from producing layers |
| Digest | SHA-256 hash of a well-defined subset of a layer's state, computed at SETTLEMENT_TICK boundaries |
| DigestHistoryTree | Binary Merkle tree indexed by tick number, storing a layer's own digest history |
| Multiply-attested snapshot | A tick at which all consumer layers' recorded digests agree with the producer layer's own digest |
| ROSC | Reduced Operational State Configuration — minimum viable recovered state for a layer |
| Recovery Completion Attestation | Signed tuple of all verified-consistent layer digests, constituting proof of successful recovery |
| Synchronization predicate | A boolean condition that must hold before a layer can proceed with recovery, gating cross-layer consistency |
| Temporal trust gradient | Higher trust weight assigned to digests that have survived unchallenged for longer periods |
| Witness verification | Post-recovery Merkle comparison between adjacent layers to verify mutual consistency |

---

*End of C34 Architecture Document*
