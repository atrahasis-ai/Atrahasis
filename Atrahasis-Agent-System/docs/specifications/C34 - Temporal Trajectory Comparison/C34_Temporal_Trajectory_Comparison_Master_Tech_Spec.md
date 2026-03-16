# C34 — Black-Start Recovery Fabric with Adversarial State Reconstruction

## Master Technical Specification

**Version:** 1.0.0
**Date:** 2026-03-11
**Invention ID:** C34
**System:** Atrahasis Agent System v2.0
**Status:** SPECIFICATION COMPLETE
**Assessment Council Scores:** Novelty 3.5/5, Feasibility 4.0/5, Impact 3.5/5, Risk 4/10 (MEDIUM)
**Normative References:** C9 Cross-Layer Reconciliation v2.0, C3 Tidal Noosphere v2.0, C5 PCVM v2.0, C6 EMA v2.0, C7 RIF v2.0, C8 DSF v2.0, C31 CAT v1.0, RFC 8032 (Ed25519), FIPS 180-4 (SHA-256)
**Implementation Target:** Parts I + II in C22 Wave 2; Part III stub in Wave 2, full implementation in Wave 4+

---

## Abstract

The Atrahasis Agent System comprises five stateful layers (C8 settlement, C5 verification, C3 coordination, C7 orchestration, C6 knowledge) with rich cross-layer dependencies governed by the C9 integration contract matrix. Each layer has its own recovery mechanism -- C8's EpochRecovery, C3's ETR/SAFE_MODE, C7's WAL/failover, C6's quarantine -- but none addresses **correlated multi-layer failure** requiring coordinated restart with mutual state consistency verification. C34 fills this gap.

The Black-Start Recovery Fabric is a cross-cutting protocol specified at C9 integration level. It consists of three parts. **Part I (Black-Start Boot Sequence)** defines a dependency-ordered recovery protocol (C8 -> C5 -> C3 -> C7 -> C6) with per-tick state digests stored in flat circular buffers, consumer-side audit trails, synchronization predicates derived exhaustively from C9 contracts with formal predicate contract binding, consistent-cut computation, and recovery window isolation. **Part II (Recovery Witness Verification)** adds post-recovery cross-layer Merkle comparison, witness corroboration with authority-directed reconciliation, and multi-layer signed recovery completion attestation. **Part III (Adversarial Reconstruction)** specifies a declarative cross-layer reference registry for future causal state reconstruction, deployed as a registry with stub interface in Wave 2.

The always-on overhead is bounded at 0.007% of the 60-second SETTLEMENT_TICK budget (<=4ms per tick per layer for digest computation). All other C34 machinery is dormant during normal operation. The protocol mandates quarterly recovery drills to prevent dormancy-induced bit rot.

Four novel contributions: (1) dependency-ordered cross-layer recovery with semantic synchronization predicates, not just health checks; (2) authority-directed reconciliation with cross-layer witness corroboration; (3) adversarial state reconstruction via declarative reference registry; (4) consumer-side audit trail as an authority-independent verification path.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Part I: Black-Start Boot Sequence](#3-part-i-black-start-boot-sequence)
   - [3.1 State Digest Engine](#31-state-digest-engine)
   - [3.2 Consumer-Side Audit Trail](#32-consumer-side-audit-trail)
   - [3.3 Boot Order DAG](#33-boot-order-dag)
   - [3.4 Synchronization Predicates](#34-synchronization-predicates)
   - [3.5 Predicate Contract Binding](#35-predicate-contract-binding)
   - [3.6 Consistent-Cut Algorithm](#36-consistent-cut-algorithm)
   - [3.7 ROSC Definitions](#37-rosc-definitions)
   - [3.8 Recovery Window Isolation](#38-recovery-window-isolation)
4. [Part II: Recovery Witness Verification](#4-part-ii-recovery-witness-verification)
   - [4.1 Merkle Comparison Protocol](#41-merkle-comparison-protocol)
   - [4.2 Cross-Layer Witness Corroboration](#42-cross-layer-witness-corroboration)
   - [4.3 Authority-Directed Reconciliation](#43-authority-directed-reconciliation)
   - [4.4 Recovery Completion Attestation](#44-recovery-completion-attestation)
5. [Part III: Adversarial Reconstruction (Registry + Stub)](#5-part-iii-adversarial-reconstruction-registry--stub)
   - [5.1 Declarative Cross-Layer Reference Registry](#51-declarative-cross-layer-reference-registry)
   - [5.2 Stub Interface Specification](#52-stub-interface-specification)
   - [5.3 Degraded Recovery Guarantees](#53-degraded-recovery-guarantees)
6. [Recovery State Machine](#6-recovery-state-machine)
7. [Recovery Coordinator](#7-recovery-coordinator)
   - [7.1 C7 Recovery Saga](#71-c7-recovery-saga)
   - [7.2 Pre-C7 Self-Coordination](#72-pre-c7-self-coordination)
8. [Recovery Drill Interface](#8-recovery-drill-interface)
9. [Cross-Layer Integration](#9-cross-layer-integration)
   - [9.1 C9 Contract Extensions](#91-c9-contract-extensions)
   - [9.2 Per-Layer Obligations](#92-per-layer-obligations)
   - [9.3 Interfaces and Events](#93-interfaces-and-events)
10. [Parameters](#10-parameters)
11. [Formal Properties](#11-formal-properties)
12. [Patent-Style Claims](#12-patent-style-claims)
13. [Comparison with Existing Approaches](#13-comparison-with-existing-approaches)
14. [Risk Analysis and Open Questions](#14-risk-analysis-and-open-questions)
15. [Appendices](#15-appendices)
    - [Appendix A: Predicate Registry](#appendix-a-predicate-registry)
    - [Appendix B: Reference Registry](#appendix-b-reference-registry)
    - [Appendix C: Glossary](#appendix-c-glossary)

---

## 1. Introduction

### 1.1 Problem Statement

The Atrahasis Agent System is a multi-layer architecture where settlement (C8), verification (C5), coordination (C3), orchestration (C7), and knowledge metabolism (C6) each maintain independent state with cross-layer dependencies. The C9 integration contract matrix defines how these layers interact: C5 reads settlement state from C8, C7 reads scheduling from C3, C6 reads claim classifications from C5, and so on.

Each layer has its own recovery mechanism designed for single-layer failures:

- **C8 DSF:** EpochRecovery protocol restores settlement state from HDL replicas
- **C5 PCVM:** VTD chain replay from snapshots (newly specified by C34)
- **C3 Tidal:** ETR governance vote and SAFE_MODE fallback
- **C7 RIF:** WAL replay with active-passive LD failover
- **C6 EMA:** Opinion freeze, queue drain, quarantine with 3-epoch window

These mechanisms work well for isolated failures. They do not handle the case where two or more layers fail simultaneously -- a correlated failure that corrupts the cross-layer consistency guarantees that each layer's recovery assumes. When C5 recovers, it checks its credibility state against settlement data from C8. But if C8 also failed and recovered to a different epoch boundary, C5's consistency check against C8 is comparing against a moving target. Neither layer can verify the other without knowing which recovery point the other chose.

### 1.2 What Is Missing

No existing AAS mechanism provides:

1. **Coordinated recovery ordering.** There is no defined sequence for restarting layers that respects their mutual dependencies. If C7 starts recovery before C3, it will attempt to read scheduling data from a layer that is not yet consistent.

2. **Cross-layer consistency verification.** Each layer can verify its own state internally, but no mechanism verifies that layer A's recovered state is consistent with layer B's recovered state across the C9 contract matrix.

3. **Consumer-side audit.** During normal operation, no layer records digests of state it receives from other layers. When a dispute arises about what C8's settlement hash was at tick T, the only source of truth is C8 itself -- there is no independent witness.

4. **Adversarial reconstruction.** If state corruption is detected post-recovery, there is no mechanism to reconstruct the corrupted state from cross-layer references. The only option is full snapshot restore, which loses all state between the snapshot and the failure.

### 1.3 Scope

C34 covers the five stateful layers: C8 DSF, C5 PCVM, C3 Tidal Noosphere, C7 RIF, and C6 EMA. C4 (ASV) is excluded because it is a stateless vocabulary specification. C31 (CAT) is optionally included when DAN_ENABLED=true but is not part of the core recovery protocol.

C34 is not a new layer. It is a **cross-cutting protocol** specified at C9 integration level that defines obligations each layer must fulfill. No central recovery service exists. The protocol is executed in distributed fashion by the layers themselves, with C7 serving as recovery coordinator once it has booted.

### 1.4 Analogy: Power Grid Black-Start

The term "black-start" comes from power grid engineering. When a large-scale blackout takes down multiple generating stations simultaneously, you cannot simply "turn everything back on" -- each generator needs power to start, creating a bootstrapping problem. The solution is a defined restart sequence starting from generators that can self-start (e.g., hydroelectric, diesel), then using those to energize progressively larger generators, then verifying frequency synchronization before connecting to the grid.

C34 applies this same pattern to the AAS:
- **Self-starting generators** = C8 (settlement), which has no cross-layer dependencies for its own recovery
- **Progressive energization** = boot order C8 -> C5 -> C3 -> C7 -> C6, each layer verified before the next starts
- **Frequency synchronization** = synchronization predicates that verify cross-layer state consistency
- **Grid connection** = the recovery completion attestation that transitions the system back to normal operation

The analogy breaks down in one important way: power grid black-start assumes honest equipment. C34 must also consider adversarial corruption -- a generator that claims to be at the right frequency but is actually sabotaged. This is why C34 adds consumer-side audit trails and witness verification: independent measurements that do not trust the generator's own instruments.

### 1.5 Design Principles

1. **Integration, not replacement.** C34 augments each layer's existing recovery mechanisms. All per-layer recovery protocols remain operational and serve as fallbacks.

2. **Protocol at C9, execution distributed.** The protocol is defined at C9 integration level. Each layer implements its C34 obligations locally.

3. **Always-on is cheap; recovery is expensive.** Digest computation runs at every tick (<=4ms). All other C34 machinery is dormant during normal operation.

4. **Consumer-side audit.** Each layer records digests of state it *receives* from other layers, creating authority-independent verification paths.

5. **Authority hierarchy preserved.** Per C9: C5 is sovereign over claims, C8 is sovereign over settlement. C34 never overrides an authority's state from consumer-side data alone.

6. **Recovery window isolation.** No operational input is accepted from system entry until recovery reaches VERIFIED state. The recovery window is a controlled environment.

7. **Drill or decay.** Recovery paths that are never exercised will rot. Periodic recovery drills are mandatory, not optional.

---

## 2. Architecture Overview

### 2.1 Architectural Position

C34 occupies the C9 integration plane -- the same level as the cross-layer reconciliation contracts it extends. It is not a layer in the AAS stack but a protocol that spans all five stateful layers.

```
+----------------------------------------------------------------------+
|                        AAS Architecture Stack                         |
|                                                                       |
|  +------------------------------------------------------------------+|
|  |               C34 Recovery Fabric (C9-level protocol)             ||
|  |                                                                    ||
|  |  +----------------+  +----------------+  +----------------------+ ||
|  |  | State Digest   |  | Recovery       |  | Witness Verification | ||
|  |  | Engine         |  | Coordinator    |  | Engine               | ||
|  |  | (always-on)    |  | (dormant)      |  | (dormant)            | ||
|  |  +-------+--------+  +-------+--------+  +---------+-----------+  ||
|  |          |                    |                      |             ||
|  |  +-------+--------------------+----------------------+---------+  ||
|  |  |      Adversarial Reconstruction Registry + Stub             |  ||
|  |  |      (dormant; full implementation Wave 4+)                 |  ||
|  |  +------------------------------------------------------------+  ||
|  +------------------------------------------------------------------+|
|                              |                                        |
|         +--------------------+--------------------+                   |
|         | digest()           | boot()             | verify()          |
|         v                    v                    v                   |
|  +----------+  +----------+  +----------+  +----------+  +--------+ |
|  | C8 DSF   |  | C5 PCVM  |  | C3 Tidal |  | C7 RIF   |  | C6 EMA | |
|  +----------+  +----------+  +----------+  +----------+  +--------+ |
|                                                                       |
|  Boot Order:  C8 --> C5 --> C3 --> C7 --> C6                         |
+----------------------------------------------------------------------+
```

### 2.2 Component Summary

| Component | Activation | Description |
|-----------|-----------|-------------|
| **State Digest Engine** | Always-on | Computes per-layer state digests at every SETTLEMENT_TICK boundary. Stores digests in flat circular buffers. Broadcasts via C3 CRDT replication. |
| **Consumer-Side Audit Trail** | Always-on | Each layer records signed digests received from layers it depends on. Authority-independent verification path. |
| **Recovery Coordinator** | Dormant | C7 recovery saga that orchestrates the boot sequence. Pre-C7 layers self-coordinate via signed broadcast. |
| **Witness Verification Engine** | Dormant | Post-recovery Merkle comparison between adjacent layer pairs. Cross-layer corroboration and authority-directed reconciliation. |
| **Adversarial Reconstruction Registry** | Dormant | Declarative cross-layer reference registry. Stub interface for Wave 2; full causal traversal implementation in Wave 4+. |
| **Recovery Drill Controller** | Periodic | Controlled recovery trigger for quarterly drill exercises. |

### 2.3 Data Flow: Normal Operation

During normal operation, only the State Digest Engine and Consumer-Side Audit Trail are active.

```
Every SETTLEMENT_TICK (60s):

  Each layer L_i:
    1. Compute state digest = SHA-256(layer-specific state fields)
    2. Sign digest with layer identity key (Ed25519)
    3. Store in local circular buffer (DigestHistory)
    4. Broadcast signed digest via C3 CRDT replication

  Each consumer layer L_j (for each producer L_i it depends on):
    1. Receive signed digest from L_i
    2. Verify Ed25519 signature
    3. Store in ConsumerDigestLog[L_i][tick]
```

**Overhead:** <=4ms per layer per tick for digest computation (0.007% of the 60-second SETTLEMENT_TICK budget). Digest broadcast piggybacks on C3 CRDT replication -- no new network protocol.

### 2.4 Data Flow: Recovery

When a multi-layer failure is detected, recovery proceeds in three phases:

```
TRIGGER: >=2 layers DEGRADED or UNREACHABLE within FAILURE_DETECTION_WINDOW

Phase 1: BLACK-START BOOT (C8 -> C5 -> C3 -> C7 -> C6)
  - Recovery window isolation: all operational input rejected
  - Sequential layer recovery with synchronization predicate gates
  - Pre-C7 layers self-coordinate; C7 coordinates C6

Phase 2: WITNESS VERIFICATION
  - Cross-layer Merkle comparison for all adjacent pairs
  - Corroboration assessment with authority-directed reconciliation
  - Multi-layer signed recovery completion attestation

Phase 3: ADVERSARIAL RECONSTRUCTION (Wave 4+ only)
  - Activated only if Phase 2 identifies unrecoverable corruption
  - Traverses cross-layer reference registry
  - Pre-Wave 4: falls back to full snapshot restore
```

---

## 3. Part I: Black-Start Boot Sequence

### 3.1 State Digest Engine

The State Digest Engine is the only C34 component that runs during normal operation. It produces the raw material -- signed, timestamped state digests -- that all other C34 components consume.

#### 3.1.1 Per-Layer Digest Definitions

Each layer digests a well-defined subset of its state that captures cross-layer-relevant state changes. The digest input is deterministic: given the same layer state at the same tick, the digest is identical.

| Layer | Digest Input | Computation |
|-------|-------------|-------------|
| **C8 DSF** | `settlement_hash \|\| epoch_number \|\| total_aic_supply \|\| conservation_valid` | SHA-256. `settlement_hash` already computed by EABS; marginal cost ~0ms. |
| **C5 PCVM** | `vtd_chain_tip \|\| credibility_snapshot_hash \|\| pending_claims_count \|\| opinion_count` | SHA-256. `vtd_chain_tip` is the VTD hash chain head (Section 3.1.3). |
| **C3 Tidal** | `topology_version \|\| hash_ring_hash \|\| vrf_seed \|\| safe_mode_state \|\| known_good_registry_hash` | SHA-256. Captures scheduling, VRF entropy, emergency state. |
| **C7 RIF** | `isr_crdt_hash \|\| active_saga_count \|\| wal_tip \|\| pe_roster_hash` | SHA-256. ISR CRDT hash captures intent state; WAL tip captures durability frontier. |
| **C6 EMA** | `coherence_graph_hash \|\| shrec_regime \|\| active_quanta_count \|\| quarantine_count \|\| consolidation_epoch` | SHA-256. `coherence_graph_hash` uses incrementally maintained Merkle root over sharded coherence graph (O(S * log Q) per tick where S=shards, Q=quanta/shard; ~0.3ms at S=10, Q=100K). |

**Performance invariant (INV-R7):** Each layer's digest computation MUST complete within DIGEST_BUDGET_MS (default 4ms). If a layer's digest consistently exceeds this budget, the layer MUST simplify its digest computation rather than violate the timing constraint.

#### 3.1.2 Digest History Storage

Each layer stores its own digest history in a flat circular buffer indexed by tick number.

```
STRUCTURE DigestHistory:
    buffer:     CircularBuffer<TickDigest, DIGEST_RETENTION_TICKS>

    FUNCTION store(tick: uint64, digest: bytes32, signature: Ed25519Sig):
        index = tick % DIGEST_RETENTION_TICKS
        buffer[index] = TickDigest {
            tick: tick,
            digest: digest,
            signature: signature,
            timestamp: wall_clock_now()
        }

    FUNCTION get(tick: uint64) -> TickDigest?:
        index = tick % DIGEST_RETENTION_TICKS
        entry = buffer[index]
        IF entry IS NOT NULL AND entry.tick == tick:
            RETURN entry
        RETURN NULL     // overwritten or never stored

    FUNCTION has(tick: uint64) -> bool:
        RETURN get(tick) IS NOT NULL

STRUCTURE TickDigest:
    tick:       uint64
    digest:     bytes32
    signature:  Ed25519Sig      // signed by layer's identity key
    timestamp:  uint64          // wall-clock time of computation
```

**Design note (S2):** The architecture originally specified a binary Merkle tree for digest history. This was replaced with a flat circular buffer because consumer-side verification compares digests directly and does not need Merkle proofs over the digest history itself. The Part II Merkle comparison protocol (Section 4.1) uses separate per-layer Merkle proofs over the layer's actual state, not over the digest buffer.

**Retention policy:** DIGEST_RETENTION_TICKS = 36000 (one CONSOLIDATION_CYCLE). At 32 bytes digest + 64 bytes signature + 16 bytes metadata = 112 bytes per tick, total storage per layer is ~3.8 MB. Buffer wraps at CONSOLIDATION_CYCLE boundaries.

**Wrap-around safety:** When DIGEST_RETENTION_TICKS is reduced via governance parameter change, the new size takes effect only at the next CONSOLIDATION_CYCLE boundary. Old entries are pruned explicitly rather than implicitly overwritten, preventing the collision scenario where a governance-reduced buffer overwrites entries still within the logical retention window.

```
FUNCTION handle_retention_change(
    old_retention: uint64,
    new_retention: uint64,
    buffer: DigestHistory
):
    IF new_retention >= old_retention:
        // Expansion: no migration needed, new slots initialize to NULL
        buffer.resize(new_retention)
        RETURN

    // Contraction: defer to next CONSOLIDATION_CYCLE boundary
    buffer.pending_resize = new_retention
    buffer.resize_at_tick = next_consolidation_boundary()
    LOG("DigestHistory resize from {} to {} scheduled at tick {}",
        old_retention, new_retention, buffer.resize_at_tick)
```

#### 3.1.3 VTD Hash Chain (C5 Obligation)

C5 PCVM does not natively maintain a hash chain over its VTD processing. C34 requires C5 to maintain a cryptographic chain linking every VTD processed in causal order, providing C5's digest with a verifiable chain tip.

```
STRUCTURE VTDHashChainEntry:
    sequence_number:     uint64
    vtd_hash:            bytes32         // SHA-256 of VTD content
    claim_class:         ClaimClass      // D/C/P/R/E/S/K/H/N
    agent_id:            bytes32
    tick:                uint64
    previous_chain_hash: bytes32
    chain_hash:          bytes32         // SHA-256(sequence || vtd_hash ||
                                        //   claim_class || agent_id ||
                                        //   tick || previous_chain_hash)
```

C34 specifies **what** C5's digest must contain (the chain tip hash) and **what properties** the chain must satisfy (append-only, hash-linked, unbroken). C34 does not specify the internal implementation of C5's hash chain storage -- that is a C5-internal concern per design principle #2.

**C5 opinion snapshots:** C5 takes periodic snapshots of its credibility state at TIDAL_EPOCH boundaries (every 60 ticks). Each snapshot captures agent credibility state, claim class statistics, and the VTD chain tip at the snapshot moment. Snapshots are retained for SNAPSHOT_RETENTION_EPOCHS TIDAL_EPOCHS (default 10). Size estimate: ~1 KB per agent x 10,000 agents = ~10 MB per snapshot x 10 retained = ~100 MB total. See Section 3.7 (ROSC_C5) for how snapshots are used during recovery.

#### 3.1.4 Digest Broadcast and Redundancy

Signed digests are broadcast to all other layers via C3's CRDT replication infrastructure. No new network protocol is introduced.

| Layer | Primary Digest Storage | Redundancy |
|-------|----------------------|------------|
| C8 DSF | Appended to HDL node state | HDL replication (>=2f+1 copies) |
| C5 PCVM | Dedicated digest log, co-located with VTD store | C5 storage redundancy |
| C3 Tidal | Embedded in epoch-boundary CRDT state | CRDT replication across all nodes |
| C7 RIF | Appended to WAL | WAL replicated to passive LD |
| C6 EMA | Dedicated digest log per shard | Sharded coherence graph replication |

**Fallback digest distribution (addressing pre-mortem I-01):** If C3 CRDT replication degrades during normal operation, layers fall back to direct peer-to-peer digest exchange at TIDAL_EPOCH boundaries (every 3600s). This is coarser than per-tick distribution but prevents consumer-log staleness during C3 degradation. The fallback uses the same LayerReadyAnnouncement message format (Section 7.2) repurposed for periodic health exchange.

### 3.2 Consumer-Side Audit Trail

Each layer maintains a log of digests received from layers it depends on. This creates verification paths that are independent of the producing layer's own claims about its state.

```
STRUCTURE ConsumerDigestLog:
    entries: Map<LayerID, CircularBuffer<ReceivedDigest, DIGEST_RETENTION_TICKS>>

STRUCTURE ReceivedDigest:
    source_layer:   LayerID
    tick:           uint64
    digest:         bytes32
    signature:      Ed25519Sig      // source layer's signature (verified on receipt)
    received_at:    uint64          // wall-clock time of receipt
    verified:       bool            // signature verified on receipt

ENUM LayerID:
    C3_TIDAL
    C5_PCVM
    C6_EMA
    C7_RIF
    C8_DSF
```

**Consumer-producer dependency map** (derived from C9 contract matrix, Section 9.1):

| Consumer Layer | Records Digests From | Rationale (C9 Contracts) |
|---------------|---------------------|--------------------------|
| C8 DSF | C5, C3 | Verification reports from C5; CRDT infra from C3 |
| C5 PCVM | C8, C3, C6 | Settlement feedback from C8; VRF from C3; K-class VTDs from C6 |
| C3 Tidal | C8, C5 | Settlement data from C8; verification results from C5 |
| C7 RIF | C3, C5, C8 | Scheduling from C3; credibility from C5; stake queries from C8 |
| C6 EMA | C5, C7, C3 | MCTs/VTDs from C5; knowledge projections via C7; epoch boundary from C3 |

**Acyclicity guarantee (INV-R2):** Consumer-side recording is strictly unidirectional. Layer L_i's digest is computed from L_i's own state, never from L_j's recording of L_i's state. This prevents circular dependencies.

**Signature verification on receipt:** When a consumer receives a digest from a producer, it verifies the Ed25519 signature immediately. The `verified` flag is set at receipt time. A consumer cannot forge a producer's digest because it cannot produce a valid Ed25519 signature for the producer's identity key. However, a consumer controls the `received_at` timestamp and the `verified` flag, and can selectively drop digests for certain ticks -- this is addressed by the cross-consumer consistency check in Part II (Section 4.2).

### 3.3 Boot Order DAG

The boot order is a strict linear DAG derived from layer dependencies. No circular dependency exists.

```
C8 (settlement) --> C5 (verification) --> C3 (coordination) --> C7 (orchestration) --> C6 (knowledge)
```

**Justification:**

- **C8 first:** Settlement state is economic ground truth. All other layers depend on settlement being consistent before they can verify their own state. C8's EpochRecovery is self-contained -- no cross-layer dependencies for its own recovery.

- **C5 second:** Verification state (credibility, VTD chains) depends on settlement being correct (C5 -> C8 for attestation settlement). C5 does NOT depend on C3 for recovery (VRF is for committee selection during normal operation, not recovery).

- **C3 third:** Coordination state (topology, hash rings) depends on both settlement (C3 <-> C8 for CRDT infrastructure) and verification (C3 <-> C5 for verification result integration). C3's ETR/SAFE_MODE is self-contained but requires settlement and verification consistency before exiting SAFE_MODE.

- **C7 fourth:** Orchestration depends on scheduling (C3), credibility (C5), and settlement (C8). C7 is also the Recovery Coordinator for Steps 4-5. C7 cannot coordinate recovery of layers it depends on.

- **C6 last:** Knowledge metabolism depends on verification (C5 for claim classification), coordination (C3 for epoch boundaries), and orchestration (C7 for knowledge projections). C6 has the lowest recovery coverage (~50%) and highest acceptable data loss.

**Formal boot dependency declarations:**

```
STRUCTURE BootDependency:
    layer:              LayerID
    depends_on:         List<LayerID>
    self_coordinating:  bool        // true for pre-C7 layers (Steps 1-3)
    rosc_definition:    ROSCSpec

CONST BOOT_ORDER: List<BootDependency> = [
    { layer: C8_DSF,   depends_on: [],                        self_coordinating: true  },
    { layer: C5_PCVM,  depends_on: [C8_DSF],                  self_coordinating: true  },
    { layer: C3_TIDAL, depends_on: [C8_DSF, C5_PCVM],         self_coordinating: true  },
    { layer: C7_RIF,   depends_on: [C8_DSF, C5_PCVM, C3_TIDAL], self_coordinating: false },
    { layer: C6_EMA,   depends_on: [C5_PCVM, C3_TIDAL, C7_RIF], self_coordinating: false },
]
```

### 3.4 Synchronization Predicates

Synchronization predicates gate each layer's recovery. They assert that a recovering layer's state is consistent with the already-recovered states of its upstream layers, as witnessed by the recovering layer's own consumer-side digest log. Predicates are derived **exhaustively** from the C9 integration contract directory.

**Design note (S3, S4, S6):** The architecture originally specified 21 predicates including 7 reverse-direction predicates, 3 defense system predicates, and 1 C4-related predicate. Reverse-direction predicates (checking later-boot layers from earlier-boot consumer logs) duplicate what Part II witness verification already does post-boot. Defense system predicates (C11/C12/C13) are already covered by their host layer's digest. The C4 predicate was inconsistent with C4's exclusion from C34 scope. After simplification, ~14 forward-direction predicates remain, covering all C9 contract relationships relevant to boot-time consistency.

#### 3.4.1 Predicate Structure

```
STRUCTURE SynchronizationPredicate:
    id:             string              // unique identifier (e.g., "PRED_C8C5_SETTLEMENT")
    source_layer:   LayerID             // layer whose state is being checked
    consumer_layer: LayerID             // layer holding the consumer-side record
    contract_ref:   C9ContractRef       // formal C9 contract reference (PM-1)
    contract_version: string            // C9 revision tag (PM-1)
    check_function: fn(SourceState, ConsumerDigest) -> PredicateResult
    validation_tests: List<TestRef>     // PM-1: associated predicate validation tests

STRUCTURE C9ContractRef:
    section:        string              // e.g., "SS9.2"
    clause:         string              // e.g., "C5 -> C8: Verification reports"
    c9_revision:    string              // e.g., "v2.0.3"

ENUM PredicateResult:
    SATISFIED           // source state matches consumer record
    VIOLATED_MINOR      // minor divergence within tolerance
    VIOLATED_MAJOR      // major divergence, requires reconciliation
    UNVERIFIABLE        // consumer record missing or corrupted
```

#### 3.4.2 Predicate Table

**C8 Recovery (Step 1) -- 1 internal predicate, 0 upstream:**

| ID | Predicate | Source |
|----|-----------|--------|
| PRED_C8_READY | C8 EpochRecovery completed, `settlement_hash` computed | C8 EABS (internal) |

**C5 Recovery (Step 2) -- 1 internal + 1 upstream predicate:**

| ID | Predicate | Source |
|----|-----------|--------|
| PRED_C5_READY | C5 VTD snapshot loaded, hash chain replayed to tip | C5 VTD log (internal) |
| PRED_C8C5_SETTLEMENT | C5's consumer-side C8 digest at recovery tick matches C8_READY.settlement_hash | C9 SS9.2: "C5 -> C8" |

**C3 Recovery (Step 3) -- 1 internal + 2 upstream predicates:**

| ID | Predicate | Source |
|----|-----------|--------|
| PRED_C3_READY | C3 ETR/SAFE_MODE recovery complete, topology + VRF state reconstructed | C3 SAFE_MODE FSM (internal) |
| PRED_C8C3_CRDT | C3's consumer-side C8 digest matches C8_READY.settlement_hash | C9 SS9.2: "C3 <-> C8" |
| PRED_C5C3_VERIFICATION | C3's consumer-side C5 digest matches C5_READY.vtd_chain_hash | C9 SS9.2: "C5 -> C3" |

**C7 Recovery (Step 4) -- 1 internal + 3 upstream predicates:**

| ID | Predicate | Source |
|----|-----------|--------|
| PRED_C7_READY | C7 WAL replayed, ISR reconciled, PE roster rebuilt | C7 WAL/failover (internal) |
| PRED_C3C7_SCHEDULING | C7's consumer-side C3 digest matches C3_READY.topology_hash | C9 SS9.2: "C3 <-> C7" |
| PRED_C5C7_CREDIBILITY | C7's consumer-side C5 digest matches C5_READY.credibility_state_hash | C9 SS9.2: "C5 -> C7" |
| PRED_C8C7_STAKE | C7's consumer-side C8 digest matches C8_READY.settlement_hash | C9 SS9.2: "C7 <-> C8" |

**C6 Recovery (Step 5) -- 1 internal + 3 upstream predicates:**

| ID | Predicate | Source |
|----|-----------|--------|
| PRED_C6_READY | C6 opinion freeze + queue drain complete, coherence graph loaded | C6 SHREC (internal) |
| PRED_C5C6_CLAIMS | C6's consumer-side C5 digest matches C5_READY.vtd_chain_hash | C9 SS9.2: "C5 <-> C6" |
| PRED_C7C6_PROJECTIONS | C6's consumer-side C7 digest matches C7_READY.isr_hash | C9 SS9.2: "C6 -> C7" |
| PRED_C3C6_EPOCH | C6's consumer-side C3 digest matches C3_READY.topology_hash | C9 SS9.2: "C3 -> C6" |

**Total: 14 predicates (5 internal + 9 cross-layer).**

#### 3.4.3 Predicate Extensibility

New C9 contracts added after DESIGN automatically require new predicates via the following rule:

```
RULE PredicateGeneration:
    FOR each new contract entry (L_i, L_j, direction) added to C9:
        IF direction IN {<-, <->}:
            GENERATE predicate PRED_{L_j}{L_i}_{contract_name}
            ADD to L_i's recovery gate
            REGISTER in Predicate Contract Binding (Section 3.5)
            LOG: "New synchronization predicate required for {L_i} <- {L_j}"
```

This is a governance rule enforced through the Predicate Contract Binding mechanism, not an automatic runtime mechanism. Each new predicate must be implemented, tested, and registered before it takes effect.

### 3.5 Predicate Contract Binding (PM-1)

The highest-risk finding from pre-mortem analysis is **synchronization predicate drift** (T-03): predicates silently desynchronizing from evolving C9 contracts over time. Predicate Contract Binding is a formal registry that makes this failure detectable rather than silent.

#### 3.5.1 Binding Registry

```
STRUCTURE PredicateContractBinding:
    predicate_id:       string
    c9_contract_ref:    C9ContractRef       // section, clause, revision
    predicate_version:  string              // version of the predicate implementation
    validation_tests:   List<TestSpec>      // tests that verify predicate correctness
    last_validated:     uint64              // tick of last successful validation
    status:             ACTIVE | STALE | DEPRECATED

STRUCTURE TestSpec:
    test_id:            string
    description:        string
    test_type:          UNIT | INTEGRATION | DRILL
    expected_result:    PredicateResult
```

#### 3.5.2 C9 Revision Check

At system startup, C34 verifies that its predicate set matches the declared C9 revision:

```
FUNCTION verify_predicate_exhaustiveness(
    predicates: List<PredicateContractBinding>,
    c9_contracts: C9ContractDirectory
) -> ExhaustivenessResult:

    // Step 1: Check that every C9 contract has a predicate
    uncovered = []
    FOR each contract IN c9_contracts.stateful_layer_contracts():
        IF NOT exists(p IN predicates WHERE p.c9_contract_ref.clause == contract.clause):
            uncovered.append(contract)

    // Step 2: Check that every predicate references a valid C9 contract
    orphaned = []
    FOR each predicate IN predicates:
        IF NOT c9_contracts.has(predicate.c9_contract_ref):
            orphaned.append(predicate)
            predicate.status = STALE

    // Step 3: Check version alignment
    mismatched = []
    FOR each predicate IN predicates:
        IF predicate.c9_contract_ref.c9_revision != c9_contracts.current_revision:
            mismatched.append(predicate)

    IF len(uncovered) > 0 OR len(orphaned) > 0:
        EMIT WARNING("Predicate exhaustiveness check failed",
                     uncovered=uncovered, orphaned=orphaned)
        // WARNING blocks recovery but does NOT block normal operation

    RETURN ExhaustivenessResult {
        exhaustive: len(uncovered) == 0 AND len(orphaned) == 0,
        uncovered: uncovered,
        orphaned: orphaned,
        mismatched: mismatched
    }
```

#### 3.5.3 C9 Amendment Trigger

When C9 is amended (new contracts added, existing contracts modified or deprecated), the Predicate Contract Binding mechanism triggers revalidation:

1. All predicates referencing modified contracts are marked STALE
2. A governance notification is emitted listing STALE predicates
3. STALE predicates must be re-implemented, re-tested, and re-registered before the next recovery drill
4. Recovery drills fail if any STALE predicates exist (Section 8)

### 3.6 Consistent-Cut Algorithm

A consistent cut is a set of per-layer state snapshots such that no layer's snapshot references state from another layer that is *newer* than that layer's snapshot. C34 computes consistent cuts **retrospectively** from stored digests.

```
FUNCTION compute_consistent_cut(
    target_tick: uint64,
    digest_histories: Map<LayerID, DigestHistory>,
    consumer_logs: Map<LayerID, ConsumerDigestLog>
) -> ConsistentCut:

    // Step 1: Find the most recent tick at or before target_tick
    //         where all layers have digests
    candidate_tick = target_tick
    best_effort_tick = NULL
    best_effort_inconsistencies = INFINITY

    WHILE candidate_tick > (target_tick - MAX_CONSISTENT_CUT_SEARCH_WINDOW):
        // Check all layers have digests at this tick
        all_present = true
        FOR each layer IN [C8, C5, C3, C7, C6]:
            IF NOT digest_histories[layer].has(candidate_tick):
                all_present = false
                BREAK

        IF NOT all_present:
            candidate_tick -= 1
            CONTINUE

        // Step 2: Verify mutual consistency at candidate_tick
        inconsistencies = []
        FOR each (consumer, producer) IN CONSUMER_PRODUCER_PAIRS:
            consumer_record = consumer_logs[consumer].get(producer, candidate_tick)
            producer_digest = digest_histories[producer].get(candidate_tick)

            IF consumer_record IS NULL:
                CONTINUE       // tolerable within DIGEST_LOSS_TOLERANCE
            IF consumer_record.digest != producer_digest.digest:
                inconsistencies.append(Inconsistency {
                    consumer: consumer, producer: producer,
                    tick: candidate_tick
                })

        IF len(inconsistencies) == 0:
            // Consistent cut found
            RETURN ConsistentCut {
                tick: candidate_tick,
                digests: { layer: digest_histories[layer].get(candidate_tick)
                           FOR layer IN [C8, C5, C3, C7, C6] },
                status: CONSISTENT
            }

        // Track best-effort candidate (addressing pre-mortem T-01)
        IF len(inconsistencies) < best_effort_inconsistencies:
            best_effort_tick = candidate_tick
            best_effort_inconsistencies = len(inconsistencies)

        candidate_tick -= 1

    // No perfect cut found -- use best-effort (fewest inconsistencies)
    IF best_effort_tick IS NOT NULL:
        RETURN ConsistentCut {
            tick: best_effort_tick,
            digests: { layer: digest_histories[layer].get(best_effort_tick)
                       FOR layer IN [C8, C5, C3, C7, C6] },
            status: BEST_EFFORT,
            inconsistency_count: best_effort_inconsistencies
        }

    // Complete failure
    RETURN ConsistentCut.FAILED(reason="No tick with all digests in search window")

STRUCTURE ConsistentCut:
    tick:                uint64
    digests:             Map<LayerID, TickDigest>
    status:              CONSISTENT | BEST_EFFORT | FAILED
    inconsistency_count: uint32             // 0 if CONSISTENT
```

**Design note (S1):** The architecture originally included a temporal trust gradient that assigned higher weight to older digests during consistent-cut selection. This was removed because the consistent-cut algorithm never needs tiebreaking -- it selects the most recent consistent tick, which is deterministic. If multiple ticks are equally consistent, the most recent one is chosen.

**Worst-case consistent-cut gap:** One CONSOLIDATION_CYCLE (36,000 seconds = 600 ticks) for C6 state, because C6's `coherence_graph_hash` only changes at CONSOLIDATION_CYCLE boundaries. For settlement recovery, the relevant gap is 1 tick (60 seconds) because C8's `settlement_hash` changes every tick. For verification, 1 TIDAL_EPOCH (3600 seconds).

### 3.7 ROSC Definitions

ROSC (Reduced Operational State Configuration) defines the minimum viable recovered state for each layer -- the state sufficient to resume accepting new operations, even if historical state is incomplete.

#### 3.7.1 ROSC_C8 (Settlement)

```
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
    acceptable_loss:
        "Computation timing metrics. Historical rejection reasons.",
    recovery_time_target: Duration.ticks(5)    // 5 minutes
}
```

#### 3.7.2 ROSC_C5 (Verification)

```
CONST ROSC_C5: ROSCSpec = {
    layer: C5_PCVM,
    required_state: [
        "VTD hash chain (complete, unbroken)",
        "current credibility state per agent (overall + per-class)",
        "pending claim queue",
        "CACT commitment chain state (if C11 active)",
    ],
    optional_state: [
        "historical VTDs older than DIGEST_RETENTION_TICKS",
        "deep-audit logs",
        "AVAP sealed opinion history (if C12 active)",
    ],
    acceptable_loss:
        "Individual VTD content for closed claims older than retention. "
        "Adversarial probing statistics (can be recomputed).",
    recovery_time_target: Duration.ticks(10)   // 10 minutes
}
```

**C5 recovery procedure:**

```
FUNCTION recover_c5(consistent_cut: ConsistentCut) -> C5RecoveryResult:
    // Step 1: Find nearest snapshot before consistent-cut tick
    snapshot = find_nearest_snapshot(consistent_cut.tick)
    IF snapshot IS NULL:
        RETURN C5RecoveryResult.FAILED("No snapshot available")

    // Step 2: Load snapshot state
    state = C5State.from_snapshot(snapshot)
    start_sequence = snapshot.vtd_chain_sequence

    // Step 3: Verify chain continuity from snapshot to current
    IF vtd_chain.entries[start_sequence].chain_hash != snapshot.vtd_chain_tip:
        RETURN C5RecoveryResult.CHAIN_BREAK(
            expected = snapshot.vtd_chain_tip,
            actual = vtd_chain.entries[start_sequence].chain_hash
        )

    // Step 4: Replay VTD chain entries from snapshot to target tick
    replayed = 0
    FOR each entry IN vtd_chain.entries[start_sequence + 1 ..]:
        IF entry.tick > consistent_cut.tick:
            BREAK
        state.apply_vtd_credibility_update(entry)
        replayed += 1

    // Step 5: Verify replay result against expected digest
    replay_digest = state.compute_digest()

    // Step 6: Check C8 consistency predicate
    c8_consumer_digest = consumer_log.get(C8_DSF, consistent_cut.tick)
    IF c8_consumer_digest IS NOT NULL:
        IF c8_consumer_digest.digest != consistent_cut.digests[C8_DSF].digest:
            RETURN C5RecoveryResult.PREDICATE_FAILED("PRED_C8C5_SETTLEMENT")

    RETURN C5RecoveryResult {
        status: SUCCESS,
        state: state,
        replay_digest: replay_digest,
        entries_replayed: replayed,
        snapshot_epoch: snapshot.epoch,
        target_tick: consistent_cut.tick
    }
```

Expected replay time: ~1ms per 1000 VTD entries. At peak load (~100 VTDs per tick, 60 ticks per epoch): worst-case replay from epoch boundary is 6,000 entries = ~6ms. Worst-case replay from last snapshot (10 epochs): 60,000 entries = ~60ms.

#### 3.7.3 ROSC_C3 (Coordination)

```
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
    acceptable_loss:
        "Predictive communication model (retrains in ~10 epochs). "
        "Stigmergic signals (regenerate naturally).",
    recovery_time_target: Duration.ticks(10)   // 10 minutes
}
```

**C3/SAFE_MODE interaction:** C3_READY in C34 context means "C3 has recovered its state and satisfies synchronization predicates," independent of SAFE_MODE status. C34 recovery succeeds even if C3 remains in SAFE_MODE. SAFE_MODE exit requires a separate Standard ETR governance vote and is not gated by C34.

#### 3.7.4 ROSC_C7 (Orchestration)

```
CONST ROSC_C7: ROSCSpec = {
    layer: C7_RIF,
    required_state: [
        "ISR CRDT state (all non-COMPLETED, non-DISSOLVED intents)",
        "active saga state (all in-flight sagas)",
        "PE roster (agent-to-locus assignments)",
        "WAL (from last checkpoint to current)",
    ],
    optional_state: [
        "completed intent history",
        "decomposition cache",
        "System 4 horizon scan state",
    ],
    acceptable_loss:
        "Completed intent archive. Decomposition cache (rebuilt on demand). "
        "System 4 predictive state (re-scans within 1 CONSOLIDATION_CYCLE).",
    recovery_time_target: Duration.epochs(1)   // 1 hour
}
```

#### 3.7.5 ROSC_C6 (Knowledge)

```
CONST ROSC_C6: ROSCSpec = {
    layer: C6_EMA,
    required_state: [
        "coherence graph structure (sharded, active quanta only)",
        "SHREC controller state (current regime, allocations)",
        "quarantine queue (quanta under review)",
        "CRP+ immune memory (L1 + L2 signatures, if C13 active)",
    ],
    optional_state: [
        "historical vitality scores",
        "circulation analytics",
        "dreaming pipeline work-in-progress",
    ],
    acceptable_loss:
        "In-progress consolidation (dreaming restarts at next cycle). "
        "Vitality history (can be recomputed from coherence graph). "
        "~50% of C6 state is reconstructible from C5 claim records + "
        "C7 knowledge projections; remaining ~50% (internal coherence "
        "metadata, catabolism history) is unrecoverable.",
    recovery_time_target: Duration.epochs(3)   // 3 hours
}
```

**Degraded C6 recovery without C7 (addressing pre-mortem I-03):** If C7 is in Emergency Bypass (both active and passive LD unavailable), C6 can perform degraded self-recovery: opinion freeze, queue drain, quarantine, and coherence graph rebuild from surviving shards. Knowledge projection verification is skipped. C6 accepts its self-recovered state with reduced confidence. This is acceptable degraded operation -- C6 already has the lowest recovery coverage and highest acceptable data loss.

### 3.8 Recovery Window Isolation (PM-2)

Recovery Window Isolation addresses the pre-mortem finding A-01 (recovery-window attack): an adversary who triggers or exploits a multi-layer failure to inject corrupted state during the recovery window.

**Requirement:** All layers operate in **read-only mode** from the moment C34 recovery is initiated (DETECTING state) until the RecoveryCompletionAttestation is signed and the system transitions to NORMAL. During recovery window isolation:

1. **No new operational state mutations** are accepted. All operational input (new VTDs, new intents, new settlement operations, new knowledge quanta) is rejected with a `SYSTEM_RECOVERING` error.

2. **Only recovery operations** are permitted: layer boot, digest verification, predicate checks, witness verification, attestation signing.

3. **Queued input** during recovery is held in a bounded input buffer per layer (max RECOVERY_INPUT_BUFFER_SIZE operations). When the buffer is full, further input is dropped. After recovery completes, buffered input is processed in submission order.

```
FUNCTION recovery_input_guard(layer: LayerID, operation: Operation) -> GuardResult:
    IF system_recovery_state != NORMAL:
        IF operation.type IN RECOVERY_OPERATIONS:
            RETURN PERMIT
        ELSE:
            layer.input_buffer.enqueue(operation)
            IF layer.input_buffer.is_full():
                RETURN REJECT("SYSTEM_RECOVERING: input buffer full")
            RETURN DEFERRED("SYSTEM_RECOVERING: queued for post-recovery")
    RETURN PERMIT
```

**State guard enforcement:** Each layer's C34LayerInterface implementation MUST include the recovery input guard. The guard is checked before any state-mutating operation. This is enforced by INV-R9 (Section 11).

---

## 4. Part II: Recovery Witness Verification

Part II activates after all five layers have booted (Phase 1 complete). Its purpose is to verify that the recovered layers are mutually consistent -- that the cross-layer state relationships defined by C9 contracts actually hold in the recovered state, not just in the individual layers' self-assessments.

### 4.1 Merkle Comparison Protocol

For each adjacent layer pair with a C9 contract, the source layer (authority) provides a Merkle proof over its recovered state, and the consumer layer verifies it against its consumer-side digest.

```
FUNCTION verify_witness_pair(
    source: LayerID,
    consumer: LayerID,
    recovery_tick: uint64
) -> WitnessResult:

    // Step 1: Source provides its digest and Merkle proof at recovery_tick
    source_digest = source.get_digest(recovery_tick)
    source_proof = source.get_merkle_proof(recovery_tick)

    // Step 2: Consumer retrieves its recorded digest of this source
    consumer_record = consumer.get_consumer_digest(source, recovery_tick)

    IF consumer_record IS NULL:
        // Try nearest available within MAX_DIGEST_SKIP
        nearest = consumer.get_nearest_consumer_digest(
            source, recovery_tick, MAX_DIGEST_SKIP)
        IF nearest IS NULL:
            RETURN WitnessResult {
                status: UNVERIFIABLE,
                source_layer: source,
                consumer_layer: consumer,
                tick: recovery_tick
            }
        consumer_record = nearest

    // Step 3: Compare digests
    IF source_digest.digest == consumer_record.digest:
        // Step 4: Verify Merkle proof validity
        IF source.verify_merkle_proof(recovery_tick, source_proof):
            RETURN WitnessResult { status: CONSISTENT, ... }
        ELSE:
            RETURN WitnessResult { status: PROOF_INVALID, ... }
    ELSE:
        RETURN WitnessResult {
            status: INCONSISTENT,
            source_layer: source,
            consumer_layer: consumer,
            tick: recovery_tick,
            divergence_tick: find_divergence_tick(source, consumer, recovery_tick)
        }

STRUCTURE WitnessResult:
    status:          CONSISTENT | INCONSISTENT | UNVERIFIABLE | PROOF_INVALID
    source_layer:    LayerID
    consumer_layer:  LayerID
    tick:            uint64
    divergence_tick: uint64?         // tick where digests first diverged
```

**Divergence tick detection:** When an inconsistency is found, the `find_divergence_tick` function binary-searches backward through the digest history to find the earliest tick where the producer's digest and consumer's record diverged. This identifies the approximate time of corruption.

```
FUNCTION find_divergence_tick(
    source: LayerID,
    consumer: LayerID,
    recovery_tick: uint64
) -> uint64:
    // Binary search for earliest divergence within retention window
    lo = max(0, recovery_tick - DIGEST_RETENTION_TICKS)
    hi = recovery_tick
    earliest_divergence = recovery_tick

    WHILE lo <= hi:
        mid = (lo + hi) / 2
        source_digest = source.get_digest(mid)
        consumer_record = consumer.get_consumer_digest(source, mid)

        IF source_digest IS NULL OR consumer_record IS NULL:
            // Gap in history -- cannot determine; narrow search
            lo = mid + 1
            CONTINUE

        IF source_digest.digest != consumer_record.digest:
            earliest_divergence = mid
            hi = mid - 1       // search for even earlier divergence
        ELSE:
            lo = mid + 1       // consistent here; divergence is later

    RETURN earliest_divergence
```

**Layer pairs verified:** All pairs (L_i, L_j) where L_j is in L_i's consumer dependency map (Section 3.2). Total: 12 directed pairs.

| Source (Authority) | Consumer | C9 Contract Direction |
|-------------------|----------|----------------------|
| C8 | C5 | C8 -> C5 (settlement feedback) |
| C8 | C3 | C8 -> C3 (CRDT infra) |
| C5 | C8 | C5 -> C8 (verification reports) |
| C5 | C3 | C5 -> C3 (verification results) |
| C5 | C6 | C5 -> C6 (MCTs, VTDs, classification) |
| C3 | C8 | C3 -> C8 (CRDT infra) |
| C3 | C5 | C3 -> C5 (VRF output) |
| C3 | C7 | C3 -> C7 (scheduling, topology) |
| C3 | C6 | C3 -> C6 (epoch boundary) |
| C7 | C3 | C7 -> C3 (leaf intents) |
| C7 | C8 | C7 -> C8 (intent budgets) |
| C7 | C6 | C7 -> C6 (knowledge projections) |

### 4.2 Cross-Layer Witness Corroboration

When a layer's recovered state is disputed (at least one consumer reports INCONSISTENT), corroboration across multiple consumer layers determines the outcome.

```
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
        RETURN CorroborationAssessment { verdict: INCONCLUSIVE }

    // Flagging threshold: strict majority of verifiable consumers disagree
    IF inconsistent_count > consistent_count:
        RETURN CorroborationAssessment { verdict: FLAGGED }
    ELSE:
        RETURN CorroborationAssessment { verdict: CORROBORATED }
```

**Corroboration thresholds per layer:**

| Authority Layer | Consumers | Flagging Threshold | Rationale |
|----------------|-----------|-------------------|-----------|
| C8 DSF | 2 (C5, C3) | Both disagree (2/2) | Settlement authority -- highest bar to override |
| C5 PCVM | 3 (C8, C3, C6) | >=2 disagree (2/3) | Verification authority -- standard majority |
| C3 Tidal | 2 (C8, C5) | Both disagree (2/2) | Coordination authority -- high bar |
| C7 RIF | 3 (C3, C5, C8) | >=2 disagree (2/3) | Standard majority |
| C6 EMA | 3 (C5, C7, C3) | >=2 disagree (2/3) | Standard majority; lowest recovery coverage |

**Cross-consumer consistency check (addressing pre-mortem A-02):** If consumer C_a has a digest for producer P at tick T but consumer C_b does not (and both should have received it per the dependency map), the missing digest is flagged as suspicious. This limits an adversary's ability to selectively drop consumer-side digests to steer the consistent-cut algorithm.

**Single-consumer disagreement notification (addressing pre-mortem A-03):** When a single consumer disagrees with an authority but the flagging threshold is not reached (e.g., 1/2 consumers disagree with C8), a governance notification is emitted. This creates a manual investigation trigger without blocking recovery.

### 4.3 Authority-Directed Reconciliation

When a layer is FLAGGED by corroboration assessment, the authority-directed reconciliation protocol activates. Per C9 hierarchy and INV-R5 (Authority Preservation), recovery reconciliation is always directed by the authoritative layer.

```
FUNCTION handle_flagged_authority(
    assessment: CorroborationAssessment,
    saga: RecoverySaga
):
    flagged_layer = assessment.authority_layer

    // Step 1: Each layer is its own authority (per C9 SS1.3)
    //   C5: sovereign over claims (INV-C1)
    //   C8: sovereign over settlement (INV-S1)
    //   C3: sovereign over coordination
    //   C7: sovereign over orchestration
    //   C6: sovereign over knowledge metabolism

    // Step 2: Fall back to last multiply-attested snapshot
    //   A multiply-attested snapshot is a tick where ALL consumers
    //   agreed with the authority (all witness results CONSISTENT)
    fallback_tick = find_last_multiply_attested_tick(
        flagged_layer,
        saga.witness_results,
        search_window = AUTHORITY_OVERRIDE_SEARCH_WINDOW
    )

    IF fallback_tick IS NOT NULL:
        // Step 3: Roll back authority to multiply-attested state
        flagged_layer.rollback_to_tick(fallback_tick)

        // Step 4: Replay from fallback_tick to recovery_tick
        flagged_layer.replay_from(fallback_tick)

        // Step 5: Re-verify this layer
        re_verify(flagged_layer, saga)

    ELSE:
        // No multiply-attested snapshot found
        IF reconstruction_engine.is_enabled():
            // Wave 4+: attempt adversarial reconstruction
            saga.state = RECONSTRUCTING
            initiate_reconstruction(flagged_layer, saga)
        ELSE:
            // Pre-Wave 4: full snapshot restore (degraded mode)
            flagged_layer.restore_from_full_snapshot()
            re_verify(flagged_layer, saga)
```

**Conditional soundness:** Authority-directed reconciliation is conditionally sound -- it preserves authority sovereignty (INV-R5) but depends on the authority's historical state being correct. An adversary who corrupts both the authority's current state AND its historical snapshots can defeat the reconciliation. This is mitigated by: (a) cross-layer witnesses limiting the time window for undetected corruption; (b) Part III reconstruction (Wave 4+) providing an alternative path; (c) the multiply-attested snapshot requirement ensuring at least some historical state was corroborated.

### 4.4 Recovery Completion Attestation

Recovery is not complete until all five layers have verified consistency and signed a joint attestation. This is the multi-layer signed attestation kept from simplification S7 because recovery is the point of maximum system vulnerability -- ceremony is justified.

```
STRUCTURE RecoveryCompletionAttestation:
    saga_id:             SagaID
    recovery_tick:       uint64
    consistent_cut_tick: uint64
    layer_digests:       Map<LayerID, bytes32>
    layer_signatures:    Map<LayerID, Ed25519Sig>
    witness_summary:     WitnessSummary
    reconstruction_used: bool
    duration_ticks:      uint64
    drill_mode:          bool            // true if this was a recovery drill
    attestation_hash:    bytes32         // SHA-256 of all fields above

STRUCTURE WitnessSummary:
    total_pairs_verified:   uint32
    consistent_pairs:       uint32
    inconsistent_pairs:     uint32
    unverifiable_pairs:     uint32
    flagged_layers:         List<LayerID>
    override_applied:       bool

FUNCTION is_valid_attestation(att: RecoveryCompletionAttestation) -> bool:
    // All five layers must have signed
    FOR each layer IN [C8_DSF, C5_PCVM, C3_TIDAL, C7_RIF, C6_EMA]:
        IF layer NOT IN att.layer_signatures:
            RETURN false
        IF NOT verify_signature(att.attestation_hash,
                                att.layer_signatures[layer],
                                layer.pubkey):
            RETURN false

    // Consistent cut tick must precede or equal recovery tick
    IF att.consistent_cut_tick > att.recovery_tick:
        RETURN false

    RETURN true
```

**Why multi-layer signing matters here:** At recovery completion, the system is transitioning from a degraded state back to normal operation. A single-signer attestation (e.g., C7 alone) would mean that a compromised C7 could declare recovery complete while other layers remain inconsistent. Multi-layer signing ensures that each layer independently verifies and attests to the consistency of the recovered state. The additional synchronization cost (collecting 5 signatures) is negligible compared to the recovery duration.

**Attestation archival:** Valid attestations are stored in C8's HDL (the most resilient storage in the system) as an append-only audit trail. This allows post-hoc analysis of recovery events and provides evidence for governance review.

---

## 5. Part III: Adversarial Reconstruction (Registry + Stub)

### 5.1 Declarative Cross-Layer Reference Registry

Part III's core contribution is the **declarative cross-layer reference registry** -- a static catalog of all cross-layer state references in the AAS. Even without the full reconstruction algorithm (deferred to Wave 4+), the registry has independent value: it documents exactly what state relationships exist between layers, enabling manual reconstruction and future automated tooling.

#### 5.1.1 Reference Structure

```
STRUCTURE CrossLayerReference:
    source_layer:       LayerID
    source_entity:      string          // entity type in source layer
    target_layer:       LayerID
    target_entity:      string          // entity type in target layer
    reference_type:     ReferenceType
    cardinality:        SINGULAR | PLURAL
    criticality:        REQUIRED | OPTIONAL

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

#### 5.1.2 Complete Reference Registry

The following 15 cross-layer references are derived from the C9 contract matrix. Each entry documents a specific state relationship that could be traversed during causal reconstruction.

| # | Source Layer | Source Entity | Target Layer | Target Entity | Type | Criticality |
|---|-------------|--------------|-------------|--------------|------|-------------|
| 1 | C5 | VerificationReport | C8 | SettlementEntry | SETTLEMENT_REF | REQUIRED |
| 2 | C5 | VTD | C3 | VRFOutput | VRF_REF | OPTIONAL |
| 3 | C5 | CredibilityScore | C8 | AccountState.capability_score | SETTLEMENT_REF | REQUIRED |
| 4 | C3 | HashRing | C8 | AccountState.staked_aic | SETTLEMENT_REF | REQUIRED |
| 5 | C3 | ParcelAssignment | C5 | VRFOutput | VRF_REF | REQUIRED |
| 6 | C3 | EpochBoundary | C6 | SHRECState | KNOWLEDGE_REF | OPTIONAL |
| 7 | C7 | IntentState | C3 | ScheduleAssignment | SCHEDULE_REF | REQUIRED |
| 8 | C7 | IntentBudget | C8 | BudgetAllocation | BUDGET_REF | REQUIRED |
| 9 | C7 | AgentAssignment | C5 | CredibilityScore | CREDIBILITY_REF | REQUIRED |
| 10 | C6 | EpistemicQuantum | C5 | ClaimClassification | CLAIM_REF | REQUIRED |
| 11 | C6 | KClassVTD | C5 | VTDChain | CLAIM_REF | REQUIRED |
| 12 | C6 | KnowledgeProjection | C7 | IntentState | INTENT_REF | OPTIONAL |
| 13 | C6 | ConsolidationCandidate | C3 | VRFOutput (CRP+ M4) | VRF_REF | REQUIRED |
| 14 | C8 | SettlementResult | C5 | VerificationReport | CLAIM_REF | OPTIONAL |
| 15 | C8 | CapacityBid | C3 | ResourceSnapshot | TOPOLOGY_REF | OPTIONAL |

**Coverage estimation per layer** (based on reference density):

| Layer | Estimated Reconstruction Coverage | Basis |
|-------|----------------------------------|-------|
| C8 DSF | ~90% | Deterministically replayable from EABS batches |
| C5 PCVM | ~75% | VTD chain from snapshots; credibility partially from C8 + C6 |
| C3 Tidal | ~85% | Topology deterministic from agent roster; VRF seed deterministic |
| C7 RIF | ~70% | Active intents from C3 scheduling + C8 budgets; WAL replay |
| C6 EMA | ~50% | Coherence graph partially from C5 claims; internal metadata unrecoverable |

### 5.2 Stub Interface Specification

Part III is deployed as a registry + stub in Wave 2. The stub provides the API surface that Parts I and II use to query Part III availability, ensuring forward-compatibility when the full implementation arrives in Wave 4+.

```
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

    // Cancel reconstruction
    FUNCTION cancel(handle: ReconstructionHandle) -> void

    // Check if Part III is enabled
    FUNCTION is_enabled() -> bool

INTERFACE LayerReconstructionProvider:
    // Each layer implements to declare references and provide reconstruction
    FUNCTION get_outbound_references() -> List<CrossLayerReference>
    FUNCTION get_inbound_references() -> List<CrossLayerReference>
    FUNCTION reconstruct_from_reference(
        entity_id: bytes32,
        reference: CrossLayerReference,
        target_state: bytes
    ) -> PartialReconstruction?
    FUNCTION merge_reconstructions(
        entity_id: bytes32,
        partials: List<PartialReconstruction>
    ) -> ReconstructedEntity?
```

**Wave 2 stub behavior:**

| Method | Stub Return |
|--------|------------|
| `is_enabled()` | `false` |
| `initiate_reconstruction()` | Returns handle with status UNSUPPORTED |
| `get_progress()` | Returns `ReconstructionResult { status: UNSUPPORTED }` |
| `cancel()` | No-op |
| `get_outbound_references()` | Returns from static registry (Section 5.1.2) |
| `get_inbound_references()` | Returns from static registry (Section 5.1.2) |
| `reconstruct_from_reference()` | Returns NULL |
| `merge_reconstructions()` | Returns NULL |

The reference query methods (`get_outbound_references`, `get_inbound_references`) are functional even in the stub -- they return data from the static registry. This enables manual reconstruction workflows and tooling development before Wave 4.

### 5.3 Degraded Recovery Guarantees (PM-4)

Before Part III is fully implemented (Wave 4+), the system operates in degraded recovery mode when witness verification identifies unrecoverable state corruption. This section documents exactly what guarantees hold and what is lost.

#### 5.3.1 What Works Without Part III

1. **Single-layer corruption with multiply-attested history:** If only one layer's state is corrupted and a multiply-attested snapshot exists within AUTHORITY_OVERRIDE_SEARCH_WINDOW, the authority-directed reconciliation protocol (Section 4.3) restores the layer to its last corroborated state and replays forward. No data loss beyond the gap between the snapshot and the failure.

2. **Multi-layer corruption where each layer's own recovery works:** If each corrupted layer can independently recover to a consistent state via its own mechanisms (C8 EpochRecovery, C7 WAL replay, etc.), C34 adds cross-layer consistency verification but the actual recovery is performed by existing mechanisms. Part III is not needed.

3. **Full snapshot restore:** If neither of the above applies, each corrupted layer falls back to its most recent full snapshot. Data between the snapshot and the failure is lost. This is the worst-case degraded path.

#### 5.3.2 What Is Lost Without Part III

1. **Adversarial state reconstruction:** The ability to reconstruct corrupted state from surviving cross-layer references. Without Part III, corrupted state that cannot be recovered by the layer's own mechanisms is lost.

2. **Targeted corruption recovery:** Part III can reconstruct specific corrupted entities without affecting the rest of the layer's state. Without it, corruption triggers a full-layer snapshot restore, which is coarser-grained.

3. **Coverage beyond ~50% for C6:** C6 has the lowest self-recovery coverage. Part III's causal traversal from C5 claims and C7 knowledge projections would raise C6's effective coverage. Without Part III, C6's ~50% self-recovery coverage is the ceiling.

#### 5.3.3 Risk Profile Without Part III

**Pre-Wave 4 adversarial exposure:** A coordinated adversary who corrupts state in a way that passes Part II witness verification (by also corrupting consumer-side records -- see pre-mortem A-02) can force a full snapshot restore when the corruption is eventually discovered, losing significant operational state. This is an accepted residual risk. Mitigation: cross-consumer consistency checks (Section 4.2) limit the adversary's ability to corrupt consumer records undetected.

---

## 6. Recovery State Machine

### 6.1 States

The system-level recovery state machine has 5 states after simplification (S10: DETECTING + INITIALIZING collapsed into single state; S8: RECONSTRUCTING removed from FSM since Part III is a stub).

```
ENUM SystemRecoveryState:
    NORMAL          // All layers operational, digest engine running
    DETECTING       // Multi-layer failure detected, computing consistent cut,
                    //   creating RecoverySaga (S10: merged with INITIALIZING)
    BOOTING         // Black-start boot sequence in progress
    VERIFYING       // Witness verification in progress
    VERIFIED        // All witnesses consistent, attestation being signed
```

The RECONSTRUCTING state exists conceptually within the RecoverySaga (Section 7.1) when Part III is enabled in Wave 4+, but it is not a top-level FSM state. The saga handles reconstruction internally and transitions to VERIFIED or FAILED.

### 6.2 State Transitions

```
NORMAL -> DETECTING:
    Guard:  >=2 layers report DEGRADED or UNREACHABLE
            within FAILURE_DETECTION_WINDOW ticks
    Action: Activate recovery window isolation (PM-2)
            Create RecoverySaga
            Compute consistent cut from digest history

DETECTING -> NORMAL:
    Guard:  False alarm -- affected layers self-recovered
            before saga started boot sequence
    Action: Cancel saga
            Deactivate recovery window isolation
            Log false alarm event

DETECTING -> BOOTING:
    Guard:  Consistent cut computed (CONSISTENT or BEST_EFFORT)
            OR no consistent cut found (use oldest available digests)
    Action: Initiate C8 recovery (Step 1)

BOOTING -> BOOTING:
    Guard:  Current boot step complete and predicates satisfied;
            next step pending
    Action: Advance to next layer in boot order
            (sub-transitions: C8 -> C5 -> C3 -> C7 -> C6)

BOOTING -> VERIFYING:
    Guard:  All 5 layers report READY
            All synchronization predicates SATISFIED
    Action: Initiate witness verification for all layer pairs

BOOTING -> DETECTING:
    Guard:  Any layer recovery FAILED
            OR any predicate VIOLATED_MAJOR
            OR saga timeout exceeded
    Action: Escalate to governance
            Attempt per-layer snapshot restore as fallback
            Log failure details

VERIFYING -> VERIFIED:
    Guard:  All witness pairs CONSISTENT
            OR flagged layers successfully reconciled
    Action: Build RecoveryCompletionAttestation
            Request signatures from all layers

VERIFYING -> DETECTING:
    Guard:  Witness verification identifies unrecoverable corruption
            AND (NOT Part III enabled OR Part III reconstruction failed)
    Action: Fall back to full snapshot restore (degraded mode)
            OR escalate to governance

VERIFIED -> NORMAL:
    Guard:  RecoveryCompletionAttestation signed by all 5 layers
    Action: Deactivate recovery window isolation
            Process buffered input (Section 3.8)
            Log attestation to C8 HDL
            Emit RecoveryComplete event
            Resume normal digest computation
```

**Note on FAILED terminal state:** The architecture does not include an explicit FAILED state in the FSM. Recovery failure transitions back to DETECTING with governance escalation. This avoids the governance escalation black hole (pre-mortem O-05) by allowing automated degraded-operation fallbacks:

1. If governance does not respond within GOVERNANCE_ESCALATION_TIMEOUT, each layer enters per-layer independent recovery (LIVE-5).
2. Per-layer recovery produces a partial restoration that allows basic operations even without full cross-layer consistency.
3. A subsequent C34 recovery attempt can be initiated once governance responds or conditions change.

### 6.3 State Transition Diagram

```
                    multi-layer failure
           +------------------------------+
           |                              v
        NORMAL                       DETECTING
           ^                         /        \
           |                false   /          \ consistent cut
           |               alarm   /            \ computed
           |                      /              \
           |                     v                v
           |                  (return           BOOTING
           |                   to NORMAL)      /      \
           |                                  /        \
           |                   all READY     /          \ FAILED /
           |                   + predicates /            \ timeout
           |                              v              v
           |                          VERIFYING     (escalate +
           |                         /          \    fallback to
           |            consistent  /            \   DETECTING)
           |                       /              \
           |                      v                v
           |                  VERIFIED         (escalate +
           |                      |             fallback to
           |      all signed      |             DETECTING)
           |                      v
           +-------------------NORMAL
```

---

## 7. Recovery Coordinator

### 7.1 C7 Recovery Saga

The Recovery Coordinator is a C7 recovery saga -- a durable workflow that survives C7 restarts via WAL persistence. It becomes active only during cross-layer recovery.

#### 7.1.1 Saga Structure

```
STRUCTURE RecoverySaga:
    saga_id:             SagaID
    state:               RecoverySagaState
    boot_progress:       Map<LayerID, LayerBootState>
    consistent_cut:      ConsistentCut?
    witness_results:     Map<(LayerID, LayerID), WitnessResult>
    completion_attestation: RecoveryCompletionAttestation?
    started_at:          uint64
    timeout_tick:        uint64
    drill_mode:          bool            // true if drill (Section 8)

ENUM RecoverySagaState:
    INITIALIZING
    BOOTING_C8
    BOOTING_C5
    BOOTING_C3
    BOOTING_C7_SELF
    BOOTING_C6
    VERIFYING
    COMPLETING
    COMPLETED
    FAILED

ENUM LayerBootState:
    PENDING
    IN_PROGRESS
    READY
    VERIFIED
    FAILED
```

#### 7.1.2 Saga Transitions

```
FUNCTION advance_saga(saga: RecoverySaga, event: RecoveryEvent):
    MATCH saga.state:
        INITIALIZING:
            compute consistent cut
            IF consistent_cut computed:
                saga.state = BOOTING_C8
                signal_layer(C8_DSF, START_RECOVERY, saga.consistent_cut)

        BOOTING_C8:
            IF event == C8_READY:
                saga.boot_progress[C8_DSF] = READY
                saga.state = BOOTING_C5
                signal_layer(C5_PCVM, START_RECOVERY, saga.consistent_cut)

        BOOTING_C5:
            IF event == C5_READY AND check_predicates(C5_PCVM):
                saga.boot_progress[C5_PCVM] = READY
                saga.state = BOOTING_C3
                signal_layer(C3_TIDAL, START_RECOVERY, saga.consistent_cut)

        BOOTING_C3:
            IF event == C3_READY AND check_predicates(C3_TIDAL):
                saga.boot_progress[C3_TIDAL] = READY
                saga.state = BOOTING_C7_SELF
                // C7 self-recovery begins

        BOOTING_C7_SELF:
            IF event == C7_READY AND check_predicates(C7_RIF):
                saga.boot_progress[C7_RIF] = READY
                saga.state = BOOTING_C6
                signal_layer(C6_EMA, START_RECOVERY, saga.consistent_cut)

        BOOTING_C6:
            IF event == C6_READY AND check_predicates(C6_EMA):
                saga.boot_progress[C6_EMA] = READY
                saga.state = VERIFYING
                initiate_witness_verification(saga)

        VERIFYING:
            IF all_witnesses_complete(saga):
                IF all_witnesses_consistent_or_reconciled(saga):
                    saga.state = COMPLETING
                ELSE:
                    saga.state = FAILED
                    escalate_to_governance(saga)

        COMPLETING:
            attestation = build_completion_attestation(saga)
            IF all_layers_signed(attestation):
                saga.completion_attestation = attestation
                saga.state = COMPLETED

    // Timeout check (every tick)
    IF current_tick() > saga.timeout_tick:
        saga.state = FAILED
        escalate_to_governance(saga)
```

#### 7.1.3 C7 Integration

The RecoverySaga integrates with C7's existing infrastructure:

1. **WAL persistence:** Saga state is written to C7's WAL. If C7 crashes during recovery, the passive LD replays the WAL and resumes the saga.

2. **ISR registration:** The saga is registered in the ISR CRDT as a `SYSTEM_RECOVERY` intent type, ensuring it survives ISR reconciliation during C7 failover.

3. **GE routing:** During recovery, the Global Engine routes recovery messages to the designated Recovery Coordinator LD.

4. **Emergency bypass:** If C7 enters Emergency Bypass (both active and passive LD unavailable), the saga is frozen. Pre-C7 layers continue self-coordinating. When C7 is restored, the saga resumes from its WAL-persisted state.

**Saga state backup in C8 HDL (addressing pre-mortem T-05):** A minimal saga state summary (saga_id, current state, boot_progress map, started_at) is persisted in C8's HDL alongside the recovery attestation archive. If C7's WAL is corrupted during recovery, the C8-backed summary provides enough information to reconstruct the saga's progress and resume from the last completed boot step rather than restarting from scratch.

### 7.2 Pre-C7 Self-Coordination

Layers C8, C5, and C3 recover before C7 is available. They use a signed broadcast protocol for coordination.

```
PROTOCOL PreC7SelfCoordination:

    MESSAGE LayerReadyAnnouncement:
        layer:          LayerID
        state_digest:   bytes32
        epoch:          uint64
        rosc_status:    ROSCStatus
        signature:      Ed25519Sig

    FUNCTION self_coordinate(layer: LayerID, boot_deps: List<LayerID>):
        // Step 1: Perform layer-specific recovery
        layer.recover()

        // Step 2: Wait for upstream layers
        FOR each dep IN boot_deps:
            announcement = await_announcement(dep, timeout=SELF_COORD_TIMEOUT)
            IF announcement IS NULL:
                HALT: "Upstream layer {dep} did not announce READY"
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
    //   1. C3 CRDT broadcast (if C3 is already READY -- only for C7/C6)
    //   2. Direct peer-to-peer UDP multicast
    //   3. HDL gossip (C8 piggybacks on HDL node communication)
```

**Message authentication:** LayerReadyAnnouncement messages are signed with Ed25519 by the announcing layer's identity key. Recipients verify the signature before acting on the announcement. This prevents impersonation during the recovery window (addressing pre-mortem A-01).

**Pre-C7 communication specification:** The pre-C7 communication path uses UDP multicast on a well-known multicast group address configured at deployment. Message format is the serialized LayerReadyAnnouncement with a 4-byte length prefix. Retry: 3 attempts with 10-second intervals. If all channels fail, the layer enters HALT and escalates to manual recovery.

```
STRUCTURE PreC7Message:
    magic:          uint32          // 0x43333252 ("C34R")
    version:        uint8           // protocol version (1)
    length:         uint32          // payload length in bytes
    payload:        LayerReadyAnnouncement  // serialized
    checksum:       uint32          // CRC-32 of payload

// Communication channel priority:
//   1. C3 CRDT broadcast (only if C3 is already READY)
//   2. Direct peer-to-peer UDP multicast
//        Group: configured at deployment (e.g., 239.32.32.1:5332)
//        TTL: 1 (same subnet)
//        Retry: 3 attempts, 10-second intervals
//   3. HDL gossip (C8 piggybacks on HDL node communication)
//        Available from Step 1 since C8 boots first
//        C5 and C3 nodes may not be HDL participants;
//        they receive via UDP multicast fallback

// What happens when all channels fail:
//   Layer enters HALT state
//   Emits RecoveryFailed event with escalation=MANUAL
//   Governance notification with channel failure diagnostics
//   Manual operator intervention required (provide network path)
```

### 7.3 Failure Detection

C34 recovery is triggered when multiple layers fail within a short window. The failure detection mechanism relies on the always-on digest engine: if a layer fails to produce a digest for DIGEST_LOSS_TOLERANCE consecutive ticks, it is classified DEGRADED.

```
FUNCTION detect_multi_layer_failure(
    digest_histories: Map<LayerID, DigestHistory>,
    current_tick: uint64
) -> FailureDetection?:

    degraded_layers = []
    FOR each layer IN [C8, C5, C3, C7, C6]:
        consecutive_missing = 0
        FOR tick FROM current_tick DOWNTO (current_tick - FAILURE_DETECTION_WINDOW):
            IF NOT digest_histories[layer].has(tick):
                consecutive_missing += 1
            ELSE:
                BREAK

        IF consecutive_missing >= DIGEST_LOSS_TOLERANCE:
            degraded_layers.append(layer)

    IF len(degraded_layers) >= 2:
        RETURN FailureDetection {
            tick: current_tick,
            degraded_layers: degraded_layers,
            window: FAILURE_DETECTION_WINDOW
        }

    RETURN NULL     // no multi-layer failure detected

STRUCTURE FailureDetection:
    tick:               uint64
    degraded_layers:    List<LayerID>
    window:             uint64
```

**Corroborated failure detection (addressing pre-mortem A-05):** A layer is classified DEGRADED only if its digest absence is observed by at least 2 independent monitors (other layers that record its consumer-side digest). A single monitor reporting absence could be due to network partition between the monitor and the layer, not actual layer failure. The requirement for 2+ monitors reduces the risk of fake failure injection by an adversary blocking health-check traffic to a single monitor.

```
FUNCTION corroborate_failure(
    layer: LayerID,
    consumer_logs: Map<LayerID, ConsumerDigestLog>,
    current_tick: uint64
) -> bool:
    // Count how many consumers are missing this layer's digest
    consumers = CONSUMER_DEPENDENCY_MAP.consumers_of(layer)
    absent_count = 0
    FOR each consumer IN consumers:
        IF consumer_logs[consumer].get(layer, current_tick) IS NULL:
            absent_count += 1

    // Require at least 2 independent consumers to observe absence
    RETURN absent_count >= min(2, len(consumers))
```

### 7.4 Recovery Walk-Through: End-to-End Example

This section traces through a complete recovery scenario to illustrate how all components interact.

**Scenario:** At tick 100,000, both C5 (verification) and C7 (orchestration) become UNREACHABLE due to a correlated infrastructure failure. C8, C3, and C6 are still running but detect the absence.

**Phase 0: Detection (ticks 100,000 - 100,005)**

1. Tick 100,001: C8 notices C5's digest is missing from consumer log. C3 also notices.
2. Tick 100,003: C8 notices C7's digest is missing. C3 notices C7's digest missing.
3. Tick 100,005: FAILURE_DETECTION_WINDOW (5 ticks) reached. Two layers (C5, C7) have DIGEST_LOSS_TOLERANCE (5) consecutive missing digests corroborated by 2+ consumers.
4. System transitions NORMAL -> DETECTING.
5. Recovery Window Isolation activates: all 5 layers enter read-only mode.

**Phase 1: Consistent Cut (tick 100,005)**

6. Consistent-cut algorithm searches backward from tick 100,000.
7. At tick 99,998, all 5 layers have digests and all consumer-producer pairs are consistent.
8. ConsistentCut { tick: 99998, status: CONSISTENT } computed.

**Phase 2: Boot Sequence (ticks 100,005 - 100,020)**

9. **Step 1 (C8):** C8 is already running but re-verifies its state against consistent cut. PRED_C8_READY satisfied. C8 broadcasts LayerReadyAnnouncement via HDL gossip.

10. **Step 2 (C5):** C5 loads nearest OpinionSnapshot (tick 99,960 = epoch boundary). Replays VTD chain entries 99,961-99,998 (~38 entries at moderate load). Verifies consumer-side C8 digest at tick 99,998 matches C8_READY.settlement_hash. PRED_C5_READY and PRED_C8C5_SETTLEMENT satisfied. C5 broadcasts LayerReadyAnnouncement via UDP multicast.

11. **Step 3 (C3):** C3 is already running. Re-verifies topology state. Checks PRED_C8C3_CRDT and PRED_C5C3_VERIFICATION against consumer logs. Both satisfied. C3 broadcasts LayerReadyAnnouncement via CRDT.

12. **Step 4 (C7):** C7 Recovery Coordinator takes over. C7 replays WAL from last checkpoint. ISR reconciliation with PEs. Checks PRED_C3C7_SCHEDULING, PRED_C5C7_CREDIBILITY, PRED_C8C7_STAKE. All satisfied. C7 enters READY.

13. **Step 5 (C6):** C7 signals C6 to recover. C6 freezes opinions, drains queues, quarantines in-progress consolidation. Checks PRED_C5C6_CLAIMS, PRED_C7C6_PROJECTIONS, PRED_C3C6_EPOCH. All satisfied. C6 enters READY.

**Phase 3: Witness Verification (ticks 100,020 - 100,025)**

14. Witness verification runs for all 12 directed layer pairs.
15. All pairs return CONSISTENT (because the failure was an infrastructure outage, not state corruption).

**Phase 4: Attestation (tick 100,025)**

16. RecoveryCompletionAttestation built with all 5 layer digests at tick 99,998.
17. All 5 layers sign the attestation.
18. Attestation archived in C8 HDL.
19. System transitions VERIFIED -> NORMAL.
20. Recovery Window Isolation deactivated. Buffered input (from ticks 100,005-100,025) processed.

**Total recovery time:** ~20 ticks = ~20 minutes. Well within RECOVERY_SAGA_TIMEOUT (600 ticks = 10 hours).

---

## 8. Recovery Drill Interface (PM-3)

Recovery drills address the highest operational risk identified in pre-mortem analysis: the dormancy problem (O-02). Recovery code that is never exercised will rot. C34 mandates periodic controlled recovery exercises.

### 8.1 Drill Trigger

```
STRUCTURE RecoveryDrill:
    drill_id:           DrillID
    trigger_type:       SCHEDULED | MANUAL | GOVERNANCE
    scope:              FULL | PARTIAL
    affected_layers:    List<LayerID>       // FULL = all 5; PARTIAL = subset
    sandbox_mode:       bool                // if true, do not mutate real state
    started_at:         uint64
    result:             DrillResult?

FUNCTION initiate_drill(trigger: DrillTrigger) -> DrillID:
    // Step 1: Verify no active recovery in progress
    IF system_recovery_state != NORMAL:
        RETURN ERROR("Cannot drill during active recovery")

    // Step 2: Verify predicate exhaustiveness (PM-1)
    exhaustiveness = verify_predicate_exhaustiveness(...)
    IF NOT exhaustiveness.exhaustive:
        RETURN ERROR("Predicate exhaustiveness check failed: " +
                     exhaustiveness.uncovered + " / " + exhaustiveness.orphaned)

    // Step 3: Create drill-mode RecoverySaga
    saga = RecoverySaga {
        drill_mode: true,
        ...
    }

    // Step 4: Execute recovery protocol in sandbox mode
    //   - Digest histories and consumer logs are read (not written)
    //   - Layer recovery is simulated (not executed)
    //   - Witness verification runs against current live state
    //   - Predicates are fully evaluated
    //   - Attestation is generated with drill_mode=true

    RETURN drill.drill_id
```

### 8.2 Drill Cadence and Requirements

| Parameter | Value | Governance |
|-----------|-------|------------|
| Minimum drill frequency | Quarterly (every 90 days) | GOVERNANCE |
| Maximum time since last drill | 180 days (after which WARNING is emitted) | GOVERNANCE |
| Drill result retention | 10 most recent results | OPERATIONAL |

### 8.3 Drill Result Record

```
STRUCTURE DrillResult:
    drill_id:               DrillID
    timestamp:              uint64
    scope:                  FULL | PARTIAL
    predicate_results:      Map<string, PredicateResult>
    witness_results:        Map<(LayerID, LayerID), WitnessResult>
    consistent_cut_found:   bool
    consistent_cut_tick:    uint64?
    attestation_valid:      bool
    duration_ticks:         uint64
    anomalies:              List<DrillAnomaly>
    overall_result:         PASS | FAIL | DEGRADED

STRUCTURE DrillAnomaly:
    category:       PREDICATE_STALE | DIGEST_MISSING | WITNESS_FAIL |
                    PERFORMANCE_EXCEEDED | EXHAUSTIVENESS_GAP
    description:    string
    severity:       LOW | MEDIUM | HIGH
```

**Drill failure escalation:** If a drill returns FAIL, a governance notification is emitted with the full drill result. The notification includes specific remediation guidance (e.g., "PRED_C3C7_SCHEDULING is STALE: C9 contract SS9.2 was amended in revision v2.1.0 but predicate has not been updated"). Drill failures do not block normal operation but DO block recovery -- if a real failure occurs while the most recent drill result is FAIL, the recovery proceeds but the governance notification includes a warning that recovery correctness is degraded.

---

## 9. Cross-Layer Integration

### 9.1 C9 Contract Extensions

C34 adds the following section to the C9 Integration Contract Directory:

```
## C9 Section 9.4: Recovery Fabric Contracts (C34)

C34 defines cross-cutting recovery obligations for all stateful layers.
Unlike defense systems (C11-C13), C34 is not a cross-cutting instrument
but a cross-cutting protocol -- it specifies interfaces that each layer
must implement, not a subsystem that instruments existing pipelines.

### 9.4.1 Always-On Obligations (Normal Operation)

Every stateful layer (C3, C5, C6, C7, C8) MUST:
  1. Compute its state digest at every SETTLEMENT_TICK boundary (INV-R1)
  2. Sign the digest with its layer identity key (Ed25519)
  3. Broadcast the signed digest via C3 CRDT replication
  4. Record signed digests received from dependency layers (Section 3.2)
  5. Maintain a DigestHistory buffer for DIGEST_RETENTION_TICKS ticks
  6. Maintain a ConsumerDigestLog for DIGEST_RETENTION_TICKS ticks

### 9.4.2 Recovery Obligations

Every stateful layer MUST:
  1. Implement a ROSC (Reduced Operational State Configuration)
  2. Implement synchronization predicate checks for all upstream layers
  3. Respond to LayerReadyAnnouncement messages during pre-C7 recovery
  4. Participate in witness verification (provide Merkle proofs on request)
  5. Sign the RecoveryCompletionAttestation when verification succeeds
  6. Implement the recovery input guard (PM-2, Section 3.8)
  7. Implement LayerReconstructionProvider interface (stub until Wave 4+)

### 9.4.3 Authority Hierarchy Preservation

C34 recovery MUST NOT override:
  - C5's sovereignty over claim classification (INV-C1)
  - C8's sovereignty over settlement (INV-S1)
  - C3's sovereignty over spatial coordination
  - C6's sovereignty over knowledge metabolism
  - C7's sovereignty over intent orchestration

Recovery reconciliation is authority-directed per C9 SS1.3.
```

### 9.2 Per-Layer Obligations

#### 9.2.1 C8 DSF

```
// Digest computation -- marginal cost ~0ms (settlement_hash already exists)
FUNCTION c32_compute_digest(state: SettlementState) -> bytes32:
    RETURN SHA256(
        state.settlement_hash
        || uint64_to_bytes(state.epoch_number)
        || uint64_to_bytes(state.total_aic_supply)
        || bool_to_byte(state.conservation_valid)
    )

// Recovery -- wraps existing EpochRecovery
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C8RecoveryResult:
    target_epoch = consistent_cut.tick / TICKS_PER_TIDAL_EPOCH
    result = EpochRecovery(self.node_id, target_epoch)
    IF result.success:
        broadcast(LayerReadyAnnouncement { layer: C8_DSF, ... })
    RETURN result

// Storage: DigestHistory and ConsumerDigestLog appended to HDL node state
// Additional: saga state backup (Section 7.1.3)
// Additional: attestation archive (Section 4.4)
```

#### 9.2.2 C5 PCVM

```
// Digest computation
FUNCTION c32_compute_digest(state: C5State) -> bytes32:
    RETURN SHA256(
        state.vtd_chain.tip.chain_hash
        || state.credibility_snapshot_hash()
        || uint64_to_bytes(state.pending_claims.count())
        || uint64_to_bytes(state.opinion_count)
    )

// Recovery -- VTD snapshot + replay
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C5RecoveryResult:
    snapshot = find_nearest_snapshot(consistent_cut.tick)
    result = replay_c5_from_snapshot(snapshot, self.vtd_chain, consistent_cut.tick)
    broadcast(LayerReadyAnnouncement { layer: C5_PCVM, ... })
    RETURN result

// New obligations:
//   - VTD hash chain maintenance (Section 3.1.3)
//   - Periodic opinion snapshots at TIDAL_EPOCH boundaries
```

#### 9.2.3 C3 Tidal

```
// Digest computation
FUNCTION c32_compute_digest(state: C3State) -> bytes32:
    RETURN SHA256(
        uint64_to_bytes(state.topology_version)
        || state.hash_ring_hash()
        || state.vrf_seed
        || uint8_to_byte(state.safe_mode_state)
        || state.known_good_registry.registry_hash
    )

// Recovery -- wraps existing ETR/SAFE_MODE
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C3RecoveryResult:
    IF self.state.safe_mode_state == SAFE_MODE:
        // SAFE_MODE guarantees correctness
        PASS
    ELSE:
        self.reconstruct_topology(consistent_cut.tick)
        self.recompute_vrf_seed(consistent_cut.tick)
    broadcast(LayerReadyAnnouncement { layer: C3_TIDAL, ... })
    RETURN C3RecoveryResult { ... }

// Digest broadcast: piggybacks on existing CRDT replication
```

#### 9.2.4 C7 RIF

```
// Digest computation
FUNCTION c32_compute_digest(state: C7State) -> bytes32:
    RETURN SHA256(
        state.isr_crdt.hash()
        || uint64_to_bytes(state.active_saga_count)
        || state.wal.tip_hash()
        || state.pe_roster.hash()
    )

// Recovery -- wraps existing WAL replay + ISR reconciliation
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C7RecoveryResult:
    wal_result = self.replay_wal()
    isr_result = self.reconcile_isr()
    RETURN C7RecoveryResult { ... }

// New obligations:
//   - RecoverySaga implementation (Section 7.1)
//   - Recovery Coordinator role
//   - Saga state backup to C8 HDL
```

#### 9.2.5 C6 EMA

```
// Digest computation -- incrementally maintained Merkle root
FUNCTION c32_compute_digest(state: C6State) -> bytes32:
    RETURN SHA256(
        state.coherence_graph.merkle_root()
        || uint8_to_byte(state.shrec_controller.current_regime)
        || uint64_to_bytes(state.active_quanta_count)
        || uint64_to_bytes(state.quarantine_queue.count())
        || uint64_to_bytes(state.last_consolidation_epoch)
    )

// Recovery -- wraps existing opinion freeze + queue drain
FUNCTION c32_recover(consistent_cut: ConsistentCut) -> C6RecoveryResult:
    self.freeze_opinions()
    self.drain_queues()
    self.quarantine_in_progress()
    self.rebuild_coherence_graph()
    self.restore_shrec()
    // ~50% unrecoverable (internal metadata, catabolism history)
    RETURN C6RecoveryResult { ... }

// Degraded recovery without C7:
//   Skip knowledge projection verification
//   Accept self-recovered state with reduced confidence
```

### 9.3 Interfaces and Events

#### 9.3.1 C34 Layer Interface

```
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
    FUNCTION check_predicate(predicate_id: string,
                             upstream_state: bytes32) -> PredicateResult
    FUNCTION rollback_to_tick(tick: uint64) -> bool
    FUNCTION sign_attestation(attestation_hash: bytes32) -> Ed25519Sig
    FUNCTION recovery_input_guard(operation: Operation) -> GuardResult

    // Part III (forward-compatible, stub in Wave 2)
    FUNCTION get_outbound_references() -> List<CrossLayerReference>
    FUNCTION get_inbound_references() -> List<CrossLayerReference>
    FUNCTION reconstruct_from_reference(entity_id: bytes32,
        ref: CrossLayerReference, target_state: bytes) -> PartialReconstruction?
```

#### 9.3.2 C34 Recovery Coordinator Interface

```
INTERFACE C34RecoveryCoordinator:
    FUNCTION initiate_recovery(trigger: RecoveryTrigger) -> SagaID
    FUNCTION initiate_drill(trigger: DrillTrigger) -> DrillID
    FUNCTION get_recovery_status(saga_id: SagaID) -> RecoverySagaState
    FUNCTION cancel_recovery(saga_id: SagaID) -> void
    FUNCTION get_completion_attestation(saga_id: SagaID) ->
        RecoveryCompletionAttestation?
```

#### 9.3.3 Events

```
EVENT DigestComputed:
    layer: LayerID, tick: uint64, digest: bytes32, signature: Ed25519Sig

EVENT RecoveryInitiated:
    saga_id: SagaID, trigger: RecoveryTrigger, tick: uint64,
    affected_layers: List<LayerID>

EVENT LayerRecoveryStarted:
    saga_id: SagaID, layer: LayerID, tick: uint64

EVENT LayerRecoveryComplete:
    saga_id: SagaID, layer: LayerID, tick: uint64,
    digest: bytes32, rosc_status: ROSCStatus

EVENT PredicateChecked:
    saga_id: SagaID, predicate: string, result: PredicateResult,
    source: LayerID, consumer: LayerID

EVENT WitnessVerificationComplete:
    saga_id: SagaID, source: LayerID, consumer: LayerID, result: WitnessResult

EVENT RecoveryComplete:
    saga_id: SagaID, tick: uint64, attestation: RecoveryCompletionAttestation

EVENT RecoveryFailed:
    saga_id: SagaID, tick: uint64, reason: string,
    escalation: GOVERNANCE | MANUAL | SNAPSHOT_RESTORE

EVENT DrillComplete:
    drill_id: DrillID, result: DrillResult

EVENT PredicateStale:
    predicate_id: string, c9_revision_expected: string,
    c9_revision_current: string

EVENT RecoveryWindowActivated:
    tick: uint64, saga_id: SagaID

EVENT RecoveryWindowDeactivated:
    tick: uint64, saga_id: SagaID, buffered_operations: uint64

EVENT GovernanceEscalation:
    saga_id: SagaID, tick: uint64, reason: string,
    timeout_tick: uint64
```

#### 9.3.4 Data Structures Summary

| Structure | Defined In | Used By | Cardinality | Size Estimate |
|-----------|-----------|---------|-------------|---------------|
| TickDigest | SS3.1.2 | All layers | 1 per layer per tick | 112 bytes |
| DigestHistory | SS3.1.2 | All layers | 1 per layer | ~3.8 MB |
| ConsumerDigestLog | SS3.2 | All layers | 1 per layer | ~3.8 MB per dependency |
| ReceivedDigest | SS3.2 | All layers | N per layer | 112 bytes |
| ConsistentCut | SS3.6 | Recovery Coordinator | 1 per recovery | ~600 bytes |
| ROSCSpec | SS3.7 | All layers | 1 per layer (static) | ~500 bytes |
| SynchronizationPredicate | SS3.4 | All layers | 14 total (static) | ~200 bytes each |
| PredicateContractBinding | SS3.5 | All layers | 14 total | ~500 bytes each |
| RecoverySaga | SS7.1 | C7 RIF | 1 per recovery | ~2 KB |
| WitnessResult | SS4.1 | Witness Engine | 1 per pair per verification | ~200 bytes |
| CorroborationAssessment | SS4.2 | Witness Engine | 1 per layer per verification | ~300 bytes |
| RecoveryCompletionAttestation | SS4.4 | All layers | 1 per successful recovery | ~1 KB |
| CrossLayerReference | SS5.1 | Reconstruction Engine | 15 total (static) | ~200 bytes each |
| VTDHashChainEntry | SS3.1.3 | C5 PCVM | 1 per VTD | ~112 bytes |
| C5OpinionSnapshot | SS3.7.2 | C5 PCVM | 1 per TIDAL_EPOCH | ~10 MB |
| DrillResult | SS8.3 | Recovery Drill Controller | 1 per drill | ~5 KB |
| FailureDetection | SS7.3 | Recovery Coordinator | 1 per detection | ~100 bytes |

#### 9.3.5 Error Codes

```
ENUM C34ErrorCode:
    // Detection errors
    E_NO_CONSISTENT_CUT          // No consistent cut found in search window
    E_FALSE_ALARM                // Layers self-recovered before boot started

    // Boot errors
    E_LAYER_RECOVERY_FAILED      // A layer's own recovery mechanism failed
    E_PREDICATE_VIOLATED         // Synchronization predicate VIOLATED_MAJOR
    E_PREDICATE_UNVERIFIABLE     // Consumer record missing for predicate check
    E_UPSTREAM_TIMEOUT           // Upstream layer did not announce READY in time
    E_SAGA_TIMEOUT               // Recovery saga exceeded RECOVERY_SAGA_TIMEOUT

    // Witness errors
    E_WITNESS_INCONSISTENT       // Producer-consumer digest mismatch
    E_WITNESS_PROOF_INVALID      // Merkle proof verification failed
    E_WITNESS_TIMEOUT            // Witness verification timed out
    E_AUTHORITY_FLAGGED          // Majority of consumers disagree with authority
    E_NO_ATTESTED_SNAPSHOT       // No multiply-attested snapshot found for override

    // Attestation errors
    E_ATTESTATION_UNSIGNED       // Not all layers signed the attestation
    E_ATTESTATION_INVALID        // Attestation hash verification failed

    // Drill errors
    E_DRILL_DURING_RECOVERY      // Cannot drill while recovery is active
    E_PREDICATES_STALE           // Stale predicates block drill execution
    E_DRILL_OVERDUE              // Drill staleness threshold exceeded

    // Recovery window errors
    E_SYSTEM_RECOVERING          // Operational input rejected during recovery
    E_INPUT_BUFFER_FULL          // Recovery input buffer capacity exceeded

    // Governance errors
    E_GOVERNANCE_TIMEOUT         // Governance did not respond in time
```

---

## 10. Parameters

### 10.1 Always-On Parameters (State Digest Engine)

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| DIGEST_BUDGET_MS | 4 | 1-10 | OPERATIONAL | Max time per layer for digest computation per tick |
| DIGEST_RETENTION_TICKS | 36000 | 3600-108000 | CONSTITUTIONAL | Ticks of digest history retained (1 CONSOLIDATION_CYCLE) |
| DIGEST_LOSS_TOLERANCE | 5 | 1-10 | OPERATIONAL | Max consecutive missing consumer digests before DEGRADED alert |

### 10.2 Recovery Protocol Parameters

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| FAILURE_DETECTION_WINDOW | 5 | 2-15 | OPERATIONAL | Ticks within which >=2 layer failures trigger recovery |
| MAX_CONSISTENT_CUT_SEARCH_WINDOW | 600 | 60-3600 | CONSTITUTIONAL | Max ticks to search backward for consistent cut |
| SELF_COORD_TIMEOUT | 30 | 10-60 | OPERATIONAL | Ticks to wait for upstream LayerReadyAnnouncement |
| RECOVERY_SAGA_TIMEOUT | 600 | 120-1800 | CONSTITUTIONAL | Max ticks for entire recovery saga |
| MAX_DIGEST_SKIP | 5 | 1-10 | OPERATIONAL | Max tick gap when searching for nearest consumer digest |
| RECOVERY_INPUT_BUFFER_SIZE | 10000 | 1000-100000 | OPERATIONAL | Max operations buffered per layer during recovery |
| GOVERNANCE_ESCALATION_TIMEOUT | 60 | 30-300 | CONSTITUTIONAL | Ticks before automated fallback if governance unresponsive |

### 10.3 Witness Verification Parameters

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| WITNESS_TIMEOUT | 10 | 5-30 | OPERATIONAL | Ticks allowed for each witness verification pair |
| AUTHORITY_OVERRIDE_SEARCH_WINDOW | 3600 | 600-36000 | CONSTITUTIONAL | Ticks to search for multiply-attested snapshot on override |

### 10.4 Part III Parameters (Wave 4+)

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| PART_III_ENABLED | false | true/false | CONSTITUTIONAL | Enable adversarial reconstruction |

### 10.5 C5 Snapshot Parameters

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| SNAPSHOT_INTERVAL | 60 | 30-120 | OPERATIONAL | Ticks between C5 opinion snapshots (1 TIDAL_EPOCH) |
| SNAPSHOT_RETENTION_EPOCHS | 10 | 5-100 | CONSTITUTIONAL | TIDAL_EPOCHS of C5 snapshots retained |

### 10.6 Recovery Drill Parameters

| Parameter | Default | Range | Governance | Description |
|-----------|---------|-------|------------|-------------|
| DRILL_MIN_INTERVAL_DAYS | 90 | 30-180 | CONSTITUTIONAL | Minimum days between required drills |
| DRILL_MAX_STALENESS_DAYS | 180 | 90-365 | CONSTITUTIONAL | Days since last drill before WARNING |
| DRILL_RESULT_RETENTION | 10 | 5-50 | OPERATIONAL | Number of drill results retained |

### 10.7 Parameter Constraint Invariants

The following constraints must hold between parameters. They are validated at configuration time and on any parameter change. Violation prevents the parameter change from taking effect.

```
CONSTRAINT PC-1: RECOVERY_SAGA_TIMEOUT > SELF_COORD_TIMEOUT * len(BOOT_ORDER)
    // Saga must have enough time for all layers to self-coordinate
    // Default check: 600 > 30 * 5 = 150  (satisfied)

CONSTRAINT PC-2: MAX_CONSISTENT_CUT_SEARCH_WINDOW <= DIGEST_RETENTION_TICKS
    // Cannot search beyond what is retained
    // Default check: 600 <= 36000  (satisfied)

CONSTRAINT PC-3: FAILURE_DETECTION_WINDOW < SELF_COORD_TIMEOUT
    // Detection must complete before coordination times out
    // Default check: 5 < 30  (satisfied)

CONSTRAINT PC-4: AUTHORITY_OVERRIDE_SEARCH_WINDOW <= DIGEST_RETENTION_TICKS
    // Cannot search for attested snapshots beyond retention
    // Default check: 3600 <= 36000  (satisfied)

CONSTRAINT PC-5: SNAPSHOT_INTERVAL * SNAPSHOT_RETENTION_EPOCHS >=
                 MAX_CONSISTENT_CUT_SEARCH_WINDOW
    // C5 snapshots must cover the consistent-cut search window
    // Default check: 60 * 10 = 600 >= 600  (satisfied)
```

**Total: 16 parameters** (reduced from 19 in the architecture via simplifications S1, S8).

---

## 11. Formal Properties

### 11.1 Invariants

**INV-R1 (Digest Completeness).** At every SETTLEMENT_TICK boundary, every operational stateful layer MUST have computed and signed a state digest. If a layer fails to produce a digest for DIGEST_LOSS_TOLERANCE consecutive ticks, it is classified DEGRADED.

**INV-R2 (Consumer-Side Acyclicity).** Consumer-side digest recording is strictly unidirectional. Layer L_i's digest is computed exclusively from L_i's own state. No layer's digest computation may depend on another layer's recording of its digest.

**INV-R3 (Boot Order Monotonicity).** During recovery, layers boot in strict order C8 -> C5 -> C3 -> C7 -> C6. No layer may begin recovery before all layers preceding it in the boot order have reported READY and satisfied their synchronization predicates.

**INV-R4 (Predicate Exhaustiveness).** The set of synchronization predicates is exhaustive with respect to the C9 integration contract directory. For every consumer relationship in the C9 contract matrix, at least one synchronization predicate exists. Predicate Contract Binding (Section 3.5) enforces this at startup and on C9 amendment.

**INV-R5 (Authority Preservation).** C34 recovery MUST NOT override the authoritative layer's state with consumer-side data unless the authority-override quorum is reached. Even then, the authority is rolled back to its own historical state (a multiply-attested snapshot), not replaced with consumer-derived state.

**INV-R6 (Attestation Completeness).** A RecoveryCompletionAttestation is valid if and only if all five stateful layers have signed it. Recovery is not considered complete until a valid attestation exists.

**INV-R7 (Digest Budget).** Digest computation per layer MUST NOT exceed DIGEST_BUDGET_MS milliseconds.

**INV-R8 (Conservation Through Recovery).** C8's CONS-1 invariant (AIC conservation) MUST hold at all times, including during and after recovery. If recovery produces a C8 state that violates CONS-1, the recovery MUST be rejected and C8 MUST fall back to its own ConservationRecovery protocol.

**INV-R9 (Recovery Window Isolation).** From the moment C34 recovery is initiated until the RecoveryCompletionAttestation is signed, no layer may accept operational state mutations. Only recovery operations are permitted.

### 11.2 Safety Properties

**SAFE-1 (No Phantom State).** Recovery MUST NOT introduce state that did not exist before the failure. A recovered layer's state at tick T must be derivable from the layer's state at some tick T' <= T, plus deterministic replay of operations between T' and T.

**SAFE-2 (No Settlement Divergence).** After recovery, all C8 HDL nodes MUST agree on the same `settlement_hash`. If any node's post-recovery `settlement_hash` differs, EpochRecovery is re-triggered for that node.

**SAFE-3 (No Credential Inflation).** Recovery MUST NOT increase any agent's credibility score beyond its pre-failure value. If C5 state is reconstructed, credibility scores are capped at the values in the most recent consistent C5 opinion snapshot.

**SAFE-4 (No Boot Order Violation).** It is impossible for a later-boot layer to reach READY state before an earlier-boot layer. The self-coordination protocol and saga state machine enforce this through `await_announcement` blocking.

**SAFE-5 (No Circular Recovery).** Recovery of layer L_i MUST NOT depend on layer L_j if L_j's boot order is later than L_i's. The boot dependency DAG is acyclic by construction.

**SAFE-6 (No Undetected State Corruption).** If adversarial state corruption occurs, it MUST be detectable through either: (a) digest inconsistency between producer and consumer at the corrupted tick, or (b) witness verification inconsistency post-recovery. Corruption that evades both detection paths requires the adversary to compromise both the producer and a majority of its consumers simultaneously.

### 11.3 Liveness Properties

**LIVE-1 (Recovery Termination).** Every initiated recovery saga MUST terminate within RECOVERY_SAGA_TIMEOUT ticks, either with a valid RecoveryCompletionAttestation (success) or a FAILED state with governance escalation and automated fallback.

**LIVE-2 (Digest Availability).** Under the assumption that at least one node per layer survives a failure, at least one copy of every digest within DIGEST_RETENTION_TICKS is available for recovery.

**LIVE-3 (Predicate Resolution).** Every synchronization predicate evaluation MUST produce a result (SATISFIED, VIOLATED_MINOR, VIOLATED_MAJOR, or UNVERIFIABLE) within SELF_COORD_TIMEOUT ticks. No predicate evaluation may block indefinitely.

**LIVE-4 (Progressive Recovery).** If full cross-layer recovery fails, the system MUST degrade to per-layer recovery (each layer's existing mechanisms). Per-layer recovery is always available as a fallback.

**LIVE-5 (Eventual Consistency).** After a successful recovery (valid attestation), all layers MUST reach a mutually consistent state within 1 TIDAL_EPOCH. "Mutually consistent" means all synchronization predicates evaluate to SATISFIED.

**LIVE-6 (Governance Timeout Fallback).** If governance does not respond to an escalation within GOVERNANCE_ESCALATION_TIMEOUT, the system MUST proceed with per-layer independent recovery rather than waiting indefinitely.

### 11.4 TLA+ Sketch

The following properties are candidates for formal verification in TLA+ during C22 Wave 2 implementation. Each is bounded to the 2-person-year TLA+ budget specified in C22.

```
---- MODULE C34Recovery ----
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS Layers, BootOrder, ConsumerMap

VARIABLES
    systemState,        \* NORMAL | DETECTING | BOOTING | VERIFYING | VERIFIED
    layerState,         \* [Layers -> {PENDING, IN_PROGRESS, READY, VERIFIED, FAILED}]
    bootIndex,          \* index into BootOrder (0..4)
    predicatesOK,       \* [Layers -> BOOLEAN]
    witnessesOK,        \* [Layers x Layers -> BOOLEAN]
    attestationSigned   \* [Layers -> BOOLEAN]

\* Property 1: Boot Order Monotonicity
BootOrderMonotonicity ==
    \A i, j \in 1..Len(BootOrder) :
        i < j =>
            layerState[BootOrder[j]] \in {PENDING} \/
            layerState[BootOrder[i]] \in {READY, VERIFIED}

\* Property 2: No Phantom State
\* (Expressed as: READY implies predicates satisfied)
NoPhantomState ==
    \A l \in Layers :
        layerState[l] = READY => predicatesOK[l]

\* Property 3: Authority Preservation
\* (Expressed as: VERIFIED state derived only from layer's own history)

\* Property 4: Recovery Termination
\* (Bounded by RECOVERY_SAGA_TIMEOUT -- fairness assumption)

\* Property 5: Recovery Window Isolation
\* (Expressed as: no operational mutations while systemState /= NORMAL)
RecoveryIsolation ==
    systemState /= "NORMAL" => \A l \in Layers : \* no mutations accepted
====
```

**TLA+ scope:** Properties 1 (Boot Order Monotonicity) and 2 (No Phantom State) are prioritized for formal verification. Properties 3-5 are candidates if budget permits. The 2-person-year cap (from C22) limits the verification to the FSM and boot sequence; witness verification and Part III are too complex for the budget.

### 11.5 Data Integrity Chain

The following diagram shows how cryptographic integrity flows through C34's data structures, from digest computation through to the final attestation.

```
Layer State (L_i at tick T)
    |
    v
SHA-256 digest computation (INV-R7: <= 4ms)
    |
    v
TickDigest { tick=T, digest=d, signature=Ed25519(d, L_i.privkey) }
    |
    +---> DigestHistory[L_i][T % RETENTION]   (local storage)
    |
    +---> Broadcast via C3 CRDT
              |
              v
         ReceivedDigest at consumer L_j
         { source=L_i, tick=T, digest=d, signature=sig, verified=true }
              |
              v
         ConsumerDigestLog[L_j][L_i][T % RETENTION]
              |
              v  (during recovery)
         SynchronizationPredicate check:
             d == L_i_READY.state_digest ?
              |
              v  (during witness verification)
         WitnessResult { source=L_i, consumer=L_j, status=CONSISTENT }
              |
              v
         CorroborationAssessment for L_i across all consumers
              |
              v
         RecoveryCompletionAttestation
         { layer_digests, layer_signatures[all 5], attestation_hash }
              |
              v
         Archived in C8 HDL (highest-resilience storage)
```

Each step in this chain is verifiable:
- TickDigest: Ed25519 signature proves L_i produced this digest
- ReceivedDigest: signature verified on receipt (cannot be forged by consumer)
- Predicate check: deterministic comparison of two values
- WitnessResult: Merkle proof verifies source state; consumer digest provides independent witness
- Attestation: 5 Ed25519 signatures over SHA-256 of all layer digests

---

## 12. Patent-Style Claims

### Claim 1: Dependency-Ordered Cross-Layer Recovery with Semantic Synchronization Predicates

A method for recovering a multi-layer distributed system from correlated failure, comprising:

(a) computing a dependency-ordered boot sequence (C8 -> C5 -> C3 -> C7 -> C6) based on the system's cross-layer contract matrix, such that each layer recovers only after all layers it depends on have been verified;

(b) gating each layer's recovery completion on synchronization predicates that verify semantic state consistency -- not merely health or availability -- between the recovering layer's consumer-side audit trail and the upstream layer's declared recovered state;

(c) deriving synchronization predicates exhaustively and mechanically from the system's integration contract directory, with formal contract binding that detects predicate drift when contracts evolve;

(d) enforcing recovery window isolation that rejects all operational input from system entry until cross-layer consistency is verified;

wherein the predicates verify not that upstream layers are *available* but that the recovering layer's recorded view of upstream state is *consistent* with the upstream layer's post-recovery state.

### Claim 2: Authority-Directed Reconciliation with Cross-Layer Witness Corroboration

A method for resolving cross-layer state inconsistencies discovered during multi-layer recovery, comprising:

(a) performing pairwise Merkle comparison between each authority layer and its consumer layers after boot completion;

(b) assessing corroboration by counting how many consumer layers' recorded digests agree or disagree with the authority's declared state;

(c) flagging an authority layer only when a strict majority of its verifiable consumers disagree with its state;

(d) reconciling a flagged authority by rolling it back to its own most recent multiply-attested snapshot (a historical state where all consumers agreed), rather than replacing its state with consumer-derived data;

wherein authority sovereignty is preserved -- no layer's state is overridden by external data, only by its own historical data that was previously corroborated by multiple independent witnesses.

### Claim 3: Consumer-Side Audit Trail as Independent Verification Path

A method for creating authority-independent verification of cross-layer state in a distributed system, comprising:

(a) each layer computing a cryptographic digest (SHA-256) of its cross-layer-relevant state at fixed time intervals (SETTLEMENT_TICK boundaries);

(b) each layer signing its digest with its identity key (Ed25519) and broadcasting to all other layers;

(c) each consumer layer recording the signed digests it receives from producer layers in a local audit trail, with signature verification on receipt;

(d) during recovery, using the consumer-side audit trail to verify that a producing layer's recovered state matches what consumers recorded during normal operation, without requiring the producing layer to be trusted;

wherein the audit trail is strictly acyclic (no layer's digest depends on another layer's recording of it), preventing circular verification dependencies while creating N-1 independent witnesses for each layer's state history.

### Claim 4: Declarative Cross-Layer Reference Registry for State Reconstruction

A system for enabling adversarial state reconstruction in a multi-layer architecture, comprising:

(a) a declarative reference registry cataloging all cross-layer state relationships (15 reference types across 5 layers), including source entity, target entity, reference type, cardinality, and criticality;

(b) a stub interface specification that enables forward-compatible integration with a full causal traversal reconstruction engine without requiring the engine to be implemented;

(c) per-layer coverage estimation based on reference density, enabling informed decisions about reconstruction feasibility versus full snapshot restore;

wherein the registry has independent value for manual reconstruction, tooling development, and architectural documentation even before automated reconstruction is implemented.

---

## 13. Comparison with Existing Approaches

### 13.1 Kubernetes Health Checks and Liveness Probes

Kubernetes uses health checks (liveness, readiness, startup probes) to determine when a container is healthy enough to receive traffic. These are **availability** checks: "is the service responding?" C34's synchronization predicates are **consistency** checks: "is the service's state consistent with its upstream dependencies?" A Kubernetes pod can pass all health checks while returning stale data that is inconsistent with other services. C34 detects this inconsistency.

Kubernetes also lacks coordinated multi-service recovery ordering. Services restart independently and rely on retry/backoff to converge. C34's boot order DAG ensures that a recovering service does not read from a dependency that has not yet recovered.

### 13.2 ARIES (Algorithm for Recovery and Isolation Exploiting Semantics)

ARIES is the standard database recovery algorithm: WAL-based, with redo/undo passes to restore a single database to a consistent state. C7's WAL replay is an ARIES-style mechanism. C34 extends this concept to **cross-database consistency**: after each "database" (layer) has performed its own ARIES-style recovery, C34 verifies that the recovered databases are mutually consistent with respect to their cross-database contracts.

ARIES operates within a single trust domain. C34 adds adversarial considerations: the consumer-side audit trail and witness corroboration detect corruption that ARIES would not, because ARIES trusts the WAL.

### 13.3 Chandy-Lamport Distributed Snapshots

The Chandy-Lamport algorithm computes consistent global snapshots of a distributed system by recording channel state. C34's consistent-cut algorithm is conceptually similar but operates **retrospectively** on stored digests rather than initiating a coordinated snapshot. This is because C34 must work when the system has already failed -- it cannot initiate a coordinated snapshot protocol when layers are down.

Chandy-Lamport also assumes reliable channels, which C34 does not. C34's consumer-side audit trail tolerates missing digests (DIGEST_LOSS_TOLERANCE) and BEST_EFFORT consistent cuts.

### 13.4 Erlang/OTP Supervision Trees

Erlang's supervision trees define restart strategies for process hierarchies: one-for-one, one-for-all, rest-for-one. C34's boot order DAG is analogous to a rest-for-one strategy with additional consistency verification. The key difference is that Erlang supervisors restart processes (stateless recovery), while C34 coordinates stateful recovery with cross-process consistency verification.

Erlang's "let it crash" philosophy assumes that restarting a process from a known good state is cheap and fast. In the AAS, restarting a layer is expensive (minutes to hours) and may involve replaying significant state history. C34's always-on digest computation makes the "known good state" readily available without requiring frequent full checkpoints.

### 13.5 Raft/Paxos Consensus Recovery

Raft and Paxos handle recovery within a single replicated state machine: a failed node rejoins by replaying the leader's log. This is analogous to C7's WAL replay for a single layer. C34 differs in three ways:

1. **Multiple heterogeneous state machines.** The AAS has five independent state machines (layers) with different state schemas, different recovery mechanisms, and cross-state-machine invariants. Raft handles replicas of one state machine; C34 handles coordination between five different state machines.

2. **No single leader.** Raft has a leader that is the source of truth. In the AAS, each layer is its own authority (C9 sovereignty). C34 must coordinate recovery without a global leader, using the dependency DAG to impose ordering.

3. **Adversarial model.** Raft assumes crash-fault tolerance (honest but potentially unavailable nodes). C34 assumes Byzantine-adjacent faults: layers may have corrupted state that passes internal consistency checks. The consumer-side audit trail and witness corroboration detect this class of fault.

### 13.6 Saga Pattern (Microservices)

The saga pattern (Garcia-Molina and Salem, 1987) coordinates long-running transactions across multiple services through a sequence of local transactions with compensating actions. C34's Recovery Coordinator is a saga -- it orchestrates a sequence of per-layer recoveries with defined failure handlers.

The key difference: a traditional saga's compensating actions undo partial work. C34's "compensating action" for a failed layer recovery is not to undo the recovery but to fall back to a more conservative recovery strategy (full snapshot restore). There is no undo in C34's boot sequence -- once a layer reports READY, it stays READY. The boot order DAG ensures that undoing an earlier layer would invalidate all later layers, which is why C34 uses progressive fallback rather than compensation.

### 13.7 Two-Phase Commit (2PC)

The RecoveryCompletionAttestation signing resembles a 2PC commit protocol: Phase 1 is "prepare" (all layers agree state is consistent), Phase 2 is "commit" (all layers sign the attestation). However, C34 does not use 2PC's blocking protocol. If one layer refuses to sign, C34 does not block -- it escalates to governance. This is because C34 operates in a failure scenario where blocking would be catastrophic: the system is already degraded and cannot afford to wait indefinitely for a potentially failed layer to respond.

### 13.8 Summary

| Approach | Scope | Consistency Check | Adversarial Model | Boot Ordering | Authority Model |
|----------|-------|-------------------|-------------------|---------------|-----------------|
| Kubernetes | Availability | Health probe (boolean) | None | None | Centralized (etcd) |
| ARIES | Single database | WAL redo/undo | None | N/A | Single authority |
| Chandy-Lamport | Distributed snapshot | Channel recording (proactive) | None | None | Symmetric |
| Erlang/OTP | Process hierarchy | None (stateless restart) | None | Supervision tree | Hierarchical |
| Raft/Paxos | Replicated state machine | Log replay | Crash-fault | Leader election | Single leader |
| Saga pattern | Microservices | Local transaction + compensate | None | Sequence DAG | Per-service |
| 2PC | Distributed transaction | Vote + commit | None | None | Coordinator |
| **C34** | **Cross-layer state** | **Retrospective digest + witness** | **Consumer-side audit** | **Dependency DAG** | **Per-layer sovereignty** |

**C34's distinctive contribution** is the combination of (a) semantic cross-layer consistency verification (not just "is it up?" but "is its state consistent with what other layers recorded?"), (b) consumer-side audit trails that create authority-independent verification paths, and (c) authority-directed reconciliation that respects each layer's sovereignty while still detecting cross-layer corruption. No existing approach combines all three.

---

## 14. Risk Analysis and Open Questions

### 14.1 Addressed Risks

| ID | Risk | Mitigation | Residual |
|----|------|-----------|----------|
| T-03 | Predicate drift | PM-1: Predicate Contract Binding with C9 revision check | STALE predicates detectable at startup; enforcement depends on governance discipline |
| A-01 | Recovery-window attack | PM-2: Recovery Window Isolation (read-only mode) | Adversary cannot inject state during recovery; buffered input processed post-recovery |
| O-02 | Recovery never tested | PM-3: Quarterly drill mandate | Drill failures generate governance alerts; enforcement depends on operational discipline |
| T-01 | Consistent-cut exhaustion | Best-effort cut selection (fewest inconsistencies) | Best-effort cut may have residual inconsistencies requiring witness verification reconciliation |
| O-05 | Governance escalation black hole | GOVERNANCE_ESCALATION_TIMEOUT with automated fallback | Per-layer independent recovery proceeds if governance is slow |
| O-04 | Parameter misconfiguration | PC-1 through PC-5 constraint invariants | Constraints are necessary conditions, not sufficient; unexpected interactions possible |
| I-01 | C3 degradation blocks digests | Fallback peer-to-peer digest exchange at TIDAL_EPOCH | Coarser granularity (3600s vs 60s); acceptable for digest availability |
| I-03 | C7 Emergency Bypass orphans C6 | Degraded C6 self-recovery without C7 | Reduced recovery confidence; knowledge projection verification skipped |
| T-05 | Saga WAL corruption | Minimal saga state backup in C8 HDL | Backup is summary only; full saga state requires C7 WAL |

### 14.2 Accepted Residual Risks

| ID | Risk | Rationale for Acceptance |
|----|------|------------------------|
| I-05 | Part III absence during coordinated attack | Pre-Wave 4, unrecoverable corruption forces full snapshot restore. Accepted because: (a) snapshot restore is functional, just lossy; (b) cross-consumer consistency checks (Section 4.2) limit adversary's ability to corrupt consumer records; (c) Part III will address this in Wave 4+ |
| A-03 | Authority-override quorum manipulation | C8 requires unanimity (2/2) to flag; one compromised consumer prevents flagging. Accepted because: (a) settlement integrity requires high override bar; (b) single-consumer disagreement notification creates manual investigation trigger |
| A-04 | Digest computation timing side-channel | 4ms digest budget reveals minor information about layer state size. LOW severity; constant-time computation can be added as a hardening measure if needed |
| M-02 | Part III never implemented | Organizational risk. Mitigated by: (a) registry has independent value; (b) stub interface prevents API breakage; (c) degraded recovery is explicitly documented |

### 14.3 Threat Model Summary

C34 operates in an environment where layers may be corrupted (not just unavailable). The following table summarizes detection capabilities by attack type:

| Attack Type | Detection Mechanism | Detection Probability | Notes |
|-------------|--------------------|-----------------------|-------|
| Accidental single-layer corruption | Digest inconsistency (consumer vs producer) | HIGH (~95%) | Detected at next tick if digest covers corrupted state |
| Accidental multi-layer corruption | Consistent-cut failure + witness verification | HIGH (~90%) | Multiple independent witnesses |
| Adversarial single-layer corruption (no consumer compromise) | Consumer-side audit trail | HIGH (~95%) | Adversary cannot forge Ed25519-signed digests |
| Adversarial corruption of producer + 1 consumer | Witness corroboration (majority rule) | MEDIUM (~70%) | Depends on remaining consumers' coverage |
| Adversarial corruption of producer + majority of consumers | Authority-override quorum | LOW (~30%) | Requires 2/2 for C8/C3 or 2/3 for others |
| Full collusion (producer + all consumers) | Undetectable by C34 | NONE | Acknowledged residual; requires 4+ compromised layers |

**Fundamental limitation:** With only 2-3 consumers per layer, the quorum sizes are too small for robust Byzantine fault tolerance. C34's witness corroboration is effective against accidental corruption and unsophisticated adversaries but cannot withstand a coordinated attack compromising 3+ layers. This is an inherent architectural constraint of a 5-layer system, not a C34 design flaw. The mitigation path is through the defense systems (C11 CACT, C12 AVAP, C13 CRP+) that detect sophisticated adversaries at the individual-agent level before they can compromise whole layers.

### 14.4 Performance Impact Analysis

| Component | Normal Operation Cost | Recovery Cost | Storage Cost |
|-----------|----------------------|---------------|--------------|
| Digest computation | <=4ms/tick/layer (0.007%) | Same | -- |
| Digest storage | -- | -- | ~3.8 MB/layer (DigestHistory) |
| Consumer-side audit trail | ~0.1ms/tick/layer (receive + store) | Read-intensive during consistent-cut search | ~3.8 MB * deps/layer (ConsumerDigestLog) |
| VTD hash chain (C5 only) | ~0.001ms/VTD (1 SHA-256) | Replay: ~1ms/1000 entries | ~112 bytes/VTD |
| C5 opinion snapshots | ~10ms/TIDAL_EPOCH (every 3600s) | Load + replay | ~100 MB total (10 snapshots) |
| Digest broadcast | Piggyback on C3 CRDT (~0ms marginal) | N/A | -- |
| Recovery Coordinator (C7) | 0 (dormant) | WAL-logged saga execution | Saga state in WAL |
| Witness verification | 0 (dormant) | ~4ms/pair x 12 pairs = ~48ms total | -- |
| Part III registry | 0 (static data) | 0 (stub in Wave 2) | ~2 KB (15 reference entries) |

**Total always-on overhead:** <=4.1ms/tick/layer for digest + consumer recording + VTD chain. At 60,000ms per tick, this is 0.0068%. Storage: ~20 MB per layer (digest + consumer logs) + ~100 MB for C5 snapshots = ~200 MB total across all layers.

### 14.5 Open Questions

**OQ-1 (Correlated failure probability).** What is the realistic probability of correlated multi-layer failure? If it is extremely rare (once per decade), the operational investment in C34 maintenance may not be justified. If it is moderately likely (once per year), C34 is clearly worth the investment. This question should be informed by operational experience in Wave 1-2. The always-on digest computation serves as a health monitoring tool regardless, providing visible value even without recovery events.

**OQ-2 (Optimal consistent-cut granularity).** The current consistent-cut algorithm searches at tick granularity (60s). For C6, which only changes at CONSOLIDATION_CYCLE boundaries (36000s), searching at tick granularity is wasteful. A tiered search (first at CONSOLIDATION_CYCLE, then TIDAL_EPOCH, then tick) might be more efficient. Deferred to implementation.

**OQ-3 (External attestation publication).** Should RecoveryCompletionAttestations be published to an external append-only log for third-party verifiability? This would increase trust but introduces an external dependency. Deferred to governance.

**OQ-4 (C5 replay logic versioning).** If C5's credibility update logic changes between a snapshot epoch and the recovery epoch (due to parameter updates, C11 CACT evolution, or C12 AVAP rule changes), replaying VTD chain entries produces different credibility state than the original computation. The post-replay digest will not match. Mitigation: version-stamp the credibility update logic and store the version in each C5OpinionSnapshot. Replay must use the logic version active when VTDs were originally processed. This is a C5-internal concern but C34 should declare the requirement.

**OQ-5 (Minimal Part III for C8).** C8 has ~90% reconstruction coverage due to deterministic replayability. A minimal Part III implementation covering C8 only could be delivered in Wave 2-3, providing the highest-value reconstruction capability at the lowest implementation cost. This would reduce the blast radius of pre-Wave-4 adversarial attacks (pre-mortem I-05).

**OQ-6 (Recovery drill scope in production).** Recovery drills in staging environments verify code paths but not production data shapes. Full drills in production carry risk (recovery window isolation blocks operations). Possible approach: sandbox-mode drills that read production state but do not mutate it, verifying that predicates and consistent cuts work against real data without actual recovery. Specified in Section 8.1 as `sandbox_mode: true`.

### 14.6 C22 Implementation Mapping

C34 maps to C22's wave structure as follows:

| C22 Wave | C34 Components | Maturity Target | Dependencies |
|----------|---------------|----------------|--------------|
| **Wave 1** (Foundation) | DigestHistory buffer, ConsumerDigestLog storage | Stub (~20%) | C8 HDL, C3 CRDT |
| **Wave 2** (Coordination) | State Digest Engine (always-on), Consumer-side audit trail, Boot order DAG, Synchronization predicates, Consistent-cut algorithm, Witness verification, Recovery Coordinator saga, Recovery completion attestation, Predicate contract binding, Recovery window isolation, Recovery drill interface, Part III registry + stub | Functional (~60%) | C7 WAL/saga infrastructure, C5 VTD chain, C3 CRDT broadcast |
| **Wave 3** (Intelligence) | -- | Hardened (~90%) | Recovery drill results inform hardening |
| **Wave 4** (Defense) | Part III full implementation: causal traversal algorithm, triple-criteria termination, LayerReconstructionProvider per layer | Functional (~60%) | Defense systems (C11/C12/C13) operational |
| **Wave 5** (Governance) | External attestation publication (if OQ-3 resolved), governance integration for escalation handling | Production (~100%) | Governance infrastructure |

**Critical path items for Wave 2:**
1. C5 VTD hash chain implementation (C5-internal, but C34-required)
2. C5 opinion snapshot mechanism (new C5 capability)
3. C7 RecoverySaga integration into existing saga infrastructure
4. Per-layer C34LayerInterface implementation (all 5 layers)
5. Predicate validation test suite (14 predicates x unit + integration tests)

**W0 risk validation relevance:** C22's W0 behavioral fingerprinting experiment (for C17 MCSD) shares infrastructure with C34's digest computation -- both require per-tick state hashing across layers. W0 results on hashing performance will inform whether the 4ms DIGEST_BUDGET_MS is achievable in practice.

---

## 15. Appendices

### Appendix A: Predicate Registry

Complete predicate-to-C9-contract traceability matrix.

| # | Predicate ID | C9 Contract | C9 Section | Direction | Layer Pair | Boot Step |
|---|-------------|-------------|------------|-----------|------------|-----------|
| 1 | PRED_C8_READY | (internal) | -- | -- | C8 self | 1 |
| 2 | PRED_C5_READY | (internal) | -- | -- | C5 self | 2 |
| 3 | PRED_C8C5_SETTLEMENT | "C5 -> C8: Verification reports" | SS9.2 | C8 -> C5 | C8, C5 | 2 |
| 4 | PRED_C3_READY | (internal) | -- | -- | C3 self | 3 |
| 5 | PRED_C8C3_CRDT | "C3 <-> C8: CRDT infrastructure" | SS9.2 | C8 -> C3 | C8, C3 | 3 |
| 6 | PRED_C5C3_VERIFICATION | "C5 -> C3: Verification results" | SS9.2 | C5 -> C3 | C5, C3 | 3 |
| 7 | PRED_C7_READY | (internal) | -- | -- | C7 self | 4 |
| 8 | PRED_C3C7_SCHEDULING | "C3 <-> C7: scheduling, topology" | SS9.2 | C3 -> C7 | C3, C7 | 4 |
| 9 | PRED_C5C7_CREDIBILITY | "C5 -> C7: Agent credibility" | SS9.2 | C5 -> C7 | C5, C7 | 4 |
| 10 | PRED_C8C7_STAKE | "C7 <-> C8: stake queries" | SS9.2 | C8 -> C7 | C8, C7 | 4 |
| 11 | PRED_C6_READY | (internal) | -- | -- | C6 self | 5 |
| 12 | PRED_C5C6_CLAIMS | "C5 <-> C6: MCTs, VTDs, classification" | SS9.2 | C5 -> C6 | C5, C6 | 5 |
| 13 | PRED_C7C6_PROJECTIONS | "C6 -> C7: Knowledge projections" | SS9.2 | C7 -> C6 | C7, C6 | 5 |
| 14 | PRED_C3C6_EPOCH | "C3 -> C6: Epoch boundary notifications" | SS9.2 | C3 -> C6 | C3, C6 | 5 |

**Note:** The original architecture specified 21 predicates. After accepted simplifications (S3: remove 7 reverse-direction predicates; S4: remove 3 defense system predicates; S6: remove PRED_C4C6_ASV), 14 predicates remain. The reverse-direction predicates are covered by Part II witness verification. Defense system predicates are covered by their host layer's digest. See Simplification Report for full justification.

### Appendix B: Reference Registry

Complete cross-layer reference registry for Part III. See Section 5.1.2 for the table. Each reference type maps to a specific field or entity relationship in the source and target layers' specifications:

| Ref # | Source Spec Section | Target Spec Section | Notes |
|-------|--------------------|--------------------|-------|
| 1 | C5 SS4.7 (verification reports) | C8 SS4.3 (settlement entries) | Every settlement requires verification |
| 2 | C5 SS4.5 (VTD envelope) | C3 SS5.2 (VRF output) | VRF for committee selection; optional |
| 3 | C5 SS6.1 (credibility scores) | C8 SS4.1 (account state) | Credibility maps to capability score |
| 4 | C3 SS5.1 (hash ring) | C8 SS4.1 (staked AIC) | Ring membership from stake |
| 5 | C3 SS5.3 (parcel assignment) | C5 SS5.2 (VRF) | VRF determines assignment |
| 6 | C3 SS3.4 (epoch boundary) | C6 SS4.1 (SHREC state) | Epoch triggers SHREC transitions |
| 7 | C7 SS4.2 (intent state) | C3 SS5.4 (schedule assignment) | Intents scheduled by C3 |
| 8 | C7 SS4.3 (intent budget) | C8 SS4.4 (budget allocation) | Budget from settlement |
| 9 | C7 SS4.5 (agent assignment) | C5 SS6.1 (credibility) | Assignment considers credibility |
| 10 | C6 SS4.2 (epistemic quantum) | C5 SS4.6 (claim classification) | Quanta classified by C5 |
| 11 | C6 SS4.3 (K-class VTD) | C5 SS4.5 (VTD chain) | K-class submitted to C5 |
| 12 | C6 SS4.4 (knowledge projection) | C7 SS4.2 (intent state) | Projections inform intents |
| 13 | C6 SS4.5 (consolidation candidate) | C3 SS5.2 (VRF, CRP+ M4) | CRP+ uses VRF for randomization |
| 14 | C8 SS4.3 (settlement result) | C5 SS4.7 (verification report) | Settlement references verification |
| 15 | C8 SS4.5 (capacity bid) | C3 SS5.5 (resource snapshot) | Bids reference capacity |

### Appendix C: Glossary

| Term | Definition |
|------|-----------|
| **Black-start** | Recovery from a state where multiple layers are simultaneously unavailable, analogous to power grid black-start procedures. |
| **Consistent cut** | A set of per-layer state snapshots where no snapshot references state newer than any other snapshot in the set. |
| **Consumer-side audit trail** | Digests recorded by consuming layers of state received from producing layers, creating authority-independent verification paths. |
| **Digest** | SHA-256 hash of a well-defined subset of a layer's state, computed at SETTLEMENT_TICK boundaries. |
| **DigestHistory** | Flat circular buffer storing a layer's own digest history, indexed by tick modulo DIGEST_RETENTION_TICKS. |
| **Multiply-attested snapshot** | A tick at which all consumer layers' recorded digests agree with the producer layer's own digest -- a historical point of confirmed cross-layer consistency. |
| **Predicate Contract Binding** | Formal registry linking each synchronization predicate to its C9 contract source, version, and validation tests, enabling detection of predicate drift. |
| **Recovery Completion Attestation** | Signed tuple of all verified-consistent layer digests from all five layers, constituting cryptographic proof of successful recovery. |
| **Recovery Drill** | A controlled, periodic exercise of the recovery protocol against live system state, designed to detect dormancy-induced bit rot before a real failure occurs. |
| **Recovery Window Isolation** | The state guard that rejects all operational input from system entry until recovery reaches VERIFIED state, preventing adversarial exploitation of the recovery window. |
| **ROSC** | Reduced Operational State Configuration -- minimum viable recovered state for a layer, sufficient to resume operations even if historical state is incomplete. |
| **Synchronization predicate** | A boolean condition derived from a C9 contract that must hold before a layer can proceed with recovery, gating semantic cross-layer consistency. |
| **Witness verification** | Post-recovery Merkle comparison between adjacent layers to verify mutual consistency, providing independent corroboration of each layer's recovered state. |

### Appendix D: Conformance Requirements

A C34-conformant implementation MUST satisfy the following requirements. Each requirement traces to a specific section.

| Req ID | Requirement | Section | Priority |
|--------|------------|---------|----------|
| REQ-01 | Each stateful layer MUST compute a state digest at every SETTLEMENT_TICK boundary | SS3.1 | P0 |
| REQ-02 | Digest computation MUST complete within DIGEST_BUDGET_MS | SS3.1.1 | P0 |
| REQ-03 | Each layer MUST sign its digest with Ed25519 | SS3.1.2 | P0 |
| REQ-04 | Each layer MUST store digest history in a circular buffer of DIGEST_RETENTION_TICKS | SS3.1.2 | P0 |
| REQ-05 | Each layer MUST record signed digests from dependency layers | SS3.2 | P0 |
| REQ-06 | Consumer-side recording MUST be acyclic (INV-R2) | SS3.2 | P0 |
| REQ-07 | Boot order MUST follow C8->C5->C3->C7->C6 | SS3.3 | P0 |
| REQ-08 | Each layer's recovery MUST be gated by synchronization predicates | SS3.4 | P0 |
| REQ-09 | Predicate contract binding registry MUST be maintained | SS3.5 | P0 |
| REQ-10 | Predicate exhaustiveness MUST be verified at startup | SS3.5.2 | P0 |
| REQ-11 | Consistent-cut algorithm MUST support best-effort fallback | SS3.6 | P1 |
| REQ-12 | Each layer MUST define and implement a ROSC | SS3.7 | P0 |
| REQ-13 | Recovery window isolation MUST reject operational input | SS3.8 | P0 |
| REQ-14 | Witness verification MUST run for all adjacent layer pairs | SS4.1 | P0 |
| REQ-15 | Corroboration assessment MUST use per-layer flagging thresholds | SS4.2 | P0 |
| REQ-16 | Authority-directed reconciliation MUST use multiply-attested snapshots | SS4.3 | P0 |
| REQ-17 | Recovery completion attestation MUST be signed by all 5 layers | SS4.4 | P0 |
| REQ-18 | Part III reference registry MUST be deployed (even as stub) | SS5.1 | P1 |
| REQ-19 | Recovery state machine MUST implement all 5 states | SS6.1 | P0 |
| REQ-20 | C7 MUST implement RecoverySaga with WAL persistence | SS7.1 | P0 |
| REQ-21 | Pre-C7 layers MUST implement self-coordination protocol | SS7.2 | P0 |
| REQ-22 | Failure detection MUST require 2+ corroborating observers | SS7.3 | P1 |
| REQ-23 | Recovery drills MUST be supported with minimum quarterly cadence | SS8 | P1 |
| REQ-24 | Parameter constraint invariants (PC-1 to PC-5) MUST be validated | SS10.7 | P0 |
| REQ-25 | Conservation invariant (CONS-1) MUST hold through recovery | SS11.1 | P0 |
| REQ-26 | Governance escalation timeout MUST have automated fallback | SS11.3 | P1 |
| REQ-27 | C5 MUST implement VTD hash chain for digest computation | SS3.1.3 | P0 |
| REQ-28 | C5 MUST implement periodic opinion snapshots | SS3.7.2 | P0 |
| REQ-29 | C8 MUST store saga state backup and attestation archive | SS7.1.3 | P1 |
| REQ-30 | C6 MUST support degraded self-recovery without C7 | SS3.7.5 | P1 |
| REQ-31 | Digest broadcast MUST include fallback for C3 degradation | SS3.1.4 | P1 |
| REQ-32 | Each layer MUST implement C34LayerInterface | SS9.3.1 | P0 |
| REQ-33 | Attestation MUST be archived in C8 HDL | SS4.4 | P1 |
| REQ-34 | C5 MUST version-stamp credibility update logic in OpinionSnapshot headers; VTD replay MUST use the logic version active when VTDs were originally processed | SS3.7 | P0 |
| REQ-35 | C6 coherence graph Merkle root MUST use canonical leaf ordering within each shard (sorted by quantum ID); digest computation MUST be atomic with respect to shard mutations within a tick | SS3.1 | P0 |

**Priority classification:**
- **P0 (MUST):** Required for C34 to function. Blocks Wave 2 completion.
- **P1 (SHOULD):** Required for full operational readiness. May be delivered in Wave 2 or early Wave 3.

### Appendix E: Monitoring Flag Resolutions

| Flag | Status | Resolution |
|------|--------|------------|
| MF-1 (Authority-directed reconciliation soundness) | ADDRESSED | Authority-override quorum defined (SS4.3). Conditional soundness: effective against accidental corruption, mitigated by cross-layer witnesses for adversarial. Detectable corruption: any producing digest inconsistency with majority of consumers. Undetectable: collusion across 4+ layers (feasibility-acknowledged residual). |
| MF-2 (Part III deferral) | ADDRESSED | Explicit degraded-mode path specified (SS5.3): pre-Wave 4, unrecoverable corruption triggers full snapshot restore. PART_III_ENABLED parameter gates activation. Registry deployed as stub in Wave 2 for forward-compatibility. |
| MF-3 (Predicate extensibility) | ADDRESSED | PM-1 Predicate Contract Binding (SS3.5): formal registry with C9 revision tracking, validation tests, amendment-triggered revalidation. Exhaustiveness verified at startup. |
| MF-4 (C6 reconstruction coverage ~50%) | ADDRESSED | Unrecoverable C6 state documented in ROSC_C6 (SS3.7.5). Acceptable loss bounds: coherence graph structure recoverable from C5 claims; SHREC regime from current metrics; dreaming pipeline restarts at next CONSOLIDATION_CYCLE. |
| MF-5 (36,000s consistent-cut gap) | ADDRESSED | Gap analysis in SS3.6: 36,000s applies only to C6 state. C8 settlement gap is 60s. C5 verification gap is 3,600s. For settlement recovery, the relevant gap is 60s. |

### Appendix F: Pre-Mortem Findings Integration

The following table maps pre-mortem findings to their resolution in this specification.

| Pre-Mortem ID | Finding | Resolution | Section |
|---------------|---------|-----------|---------|
| T-01 | Consistent-cut search exhaustion | Best-effort cut selection (fewest inconsistencies) | SS3.6 |
| T-03 | Synchronization predicate drift | PM-1: Predicate Contract Binding | SS3.5 |
| T-05 | Recovery saga WAL corruption | Saga state backup in C8 HDL | SS7.1.3 |
| T-06 | Digest history wrap-around collision | Deferred resize to CONSOLIDATION_CYCLE boundary | SS3.1.2 |
| O-01 | Predicate maintenance burden | Reduced to 14 predicates; validation test framework | SS3.4, SS3.5 |
| O-02 | Recovery never tested in production | PM-3: Mandatory quarterly drills | SS8 |
| O-04 | Parameter misconfiguration cascade | PC-1 through PC-5 constraint invariants | SS10.7 |
| O-05 | Governance escalation black hole | GOVERNANCE_ESCALATION_TIMEOUT with automated fallback | SS6.2, SS11.3 |
| A-01 | Recovery-window attack | PM-2: Recovery Window Isolation (read-only mode) | SS3.8 |
| A-02 | Consumer-side digest poisoning | Cross-consumer consistency check | SS4.2 |
| A-03 | Authority-override quorum manipulation | Single-consumer disagreement notification | SS4.2 |
| A-05 | Fake multi-layer failure injection | Corroborated failure detection (2+ observers) | SS7.3 |
| I-01 | C3 CRDT failure blocks digests | Fallback peer-to-peer digest exchange | SS3.1.4 |
| I-02 | C9 contract evolution breaks INV-R4 | C9 revision check at startup | SS3.5.2 |
| I-03 | C7 Emergency Bypass orphans C6 | Degraded C6 self-recovery without C7 | SS3.7.5 |
| I-07 | C34/C3 SAFE_MODE circular dependency | C3_READY independent of SAFE_MODE | SS3.7.3 |

---

*End of C34 Master Technical Specification*
