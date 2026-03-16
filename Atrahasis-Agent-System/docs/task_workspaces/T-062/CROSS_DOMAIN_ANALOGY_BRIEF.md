# Cross-Domain Analogy Brief: T-062 Recovery & State Assurance

**Task:** T-062 — Recovery & State Assurance
**Role:** Domain Translator
**Date:** 2026-03-11
**Purpose:** Round 0 input for Ideation Council. Raw analogical material only — no invention concepts proposed.

---

## Problem Fingerprint

The Atrahasis system has 6 architectural layers, each with independent recovery mechanisms:

| Layer | Recovery Mechanism | Temporal Grain |
|-------|-------------------|----------------|
| C3 (Coordination) | Two-tier ETR rollback, three-channel governance failover, SAFE_MODE state machine | TIDAL_EPOCH (3600s) |
| C5 (Verification) | Bootstrap seed claims, committee diversity relaxation, credibility decay | Per-claim |
| C6 (Knowledge) | Opinion freezing during PCVM outage, quarantine/dissolution lifecycle, queue drain on recovery | CONSOLIDATION_CYCLE (36000s) |
| C7 (Orchestration) | Saga-pattern compensation, ISR CRDT replication, WAL replay for settlement router | Per-intent-tree |
| C8 (Settlement) | Deterministic EABS replay, conservation violation binary search, epoch-by-epoch catch-up | SETTLEMENT_TICK (60s) |
| C4 (Communication) | Degraded first / recovered first (C10 HP-6 priority 4) | Message-level |

**The gap:** No mechanism for consistent cross-layer snapshots, coordinated recovery ordering across layers, state reconstruction from partial data when multiple layers fail simultaneously, or cross-layer verification that recovery succeeded. C10 HP-6 provides intra-C3 degradation priority but does not extend to inter-layer recovery sequencing.

**Structural signature of the problem:**
- Multiple subsystems with different temporal grains (60s / 3600s / 36000s)
- Each subsystem has internal consistency guarantees but no cross-system consistency point
- Causal dependencies flow in multiple directions (C8 settles what C7 orchestrates, C5 verifies what C6 metabolizes, C3 coordinates everything)
- Recovery must preserve sovereignty (each layer "owns" its state)

---

## Analogy 1: Mammalian Autonomic Recovery After Cardiac Arrest (Physiology)

### Source Domain

When a mammalian heart stops and is restarted (e.g., via defibrillation), the body does not recover all systems simultaneously. There is a strict physiological recovery ordering:

1. **Cardiac rhythm** (electrical pacing restored first)
2. **Hemodynamic stability** (blood pressure, perfusion)
3. **Respiratory function** (gas exchange)
4. **Renal function** (filtration, electrolyte balance — hours to days)
5. **Neurological function** (consciousness — minutes to days)
6. **Higher cognition** (memory, executive function — last, if at all)

Each organ system has its own internal recovery trajectory, but the sequence is constrained by dependency: the brain cannot recover without perfusion, perfusion requires cardiac output, etc. Clinicians monitor recovery through "end-organ markers" — creatinine for kidneys, lactate clearance for perfusion, GCS for neurology — not through a single unified metric.

### Structural Parallel

- **Layered recovery with strict ordering** maps directly to the cross-layer recovery sequencing problem. C8 (settlement = "heartbeat") must recover before C7 (orchestration = "circulation") can resume meaningful work. C6 (knowledge metabolism = "higher cognition") recovers last because it operates on the longest timescale and depends on all lower layers.
- **End-organ markers** suggest that cross-layer recovery verification should use per-layer health indicators rather than attempting a single "system recovered" predicate.
- **The concept of "return of spontaneous circulation" (ROSC)** — a minimal viability threshold that is far below full health but indicates the system can sustain itself — maps to a "minimum viable recovery" state distinct from full operational status.

### Where It Breaks Down

- Biological systems have massive redundancy (two kidneys, bilateral blood supply to brain). Atrahasis layers are not redundant with each other — they are functionally distinct.
- Biological recovery ordering is hardwired by physics (no blood flow = no oxygen = no function). Atrahasis layer dependencies are more configurable and context-dependent.
- Medicine accepts permanent partial loss (e.g., some brain damage after arrest). Atrahasis requires deterministic, complete state reconstruction.

### Design Insight

Recovery should be staged with explicit "ROSC-equivalent" checkpoints at each layer, and the system should distinguish between "layer is alive" (minimal function) and "layer is healthy" (full function). Verification should use per-layer health predicates composed into a recovery progress vector, not a single boolean.

---

## Analogy 2: Git Rebase Across Divergent Branches (Version Control)

### Source Domain

When a developer rebases a feature branch onto a main branch that has diverged significantly, git must:

1. Identify the common ancestor (the last consistent state)
2. Replay each commit from the feature branch on top of the new base
3. Detect and resolve conflicts at each step
4. Verify the result (tests pass, build succeeds)

If conflicts arise mid-rebase, the process pauses. The developer resolves the conflict, marks it resolved, and continues. The key property: each commit is replayed individually and verified, not applied as a bulk diff.

### Structural Parallel

- **Common ancestor = cross-layer snapshot.** The recovery problem requires finding the last point where all layers agreed — the "common ancestor" of 6 divergent state histories.
- **Sequential replay with per-step verification** maps to replaying state transitions layer by layer, verifying cross-layer invariants after each step rather than only at the end.
- **Conflict detection** maps to detecting cross-layer inconsistencies that arose during the failure window (e.g., C7 orchestrated intents that C8 never settled, or C5 verified claims that C6 never metabolized).
- **The `--abort` option** (abandon the rebase and return to pre-rebase state) maps to the need for a recovery-of-recovery mechanism when state reconstruction itself fails.

### Where It Breaks Down

- Git operates on immutable snapshots (commits). Atrahasis layers have mutable state that evolves continuously.
- Git rebase is single-threaded and deterministic. Atrahasis recovery may need to handle concurrent partial recoveries across layers.
- Git conflicts are syntactic (overlapping text edits). Cross-layer conflicts are semantic (violated invariants across different data models).

### Design Insight

Cross-layer recovery should identify a "common ancestor epoch" — the latest SETTLEMENT_TICK at which all 6 layers had mutually consistent state — and replay forward from there, checking cross-layer invariants at each epoch boundary. This reframes the problem from "how do we snapshot 6 layers simultaneously" to "how do we find the latest epoch where all layers were consistent, and replay from there."

---

## Analogy 3: Blackout Restoration in Electrical Power Grids (Power Systems Engineering)

### Source Domain

After a total grid blackout, power restoration follows a well-studied protocol called "black start":

1. **Black-start units** — small generators (often hydro or gas turbines) that can start without external power — energize first.
2. **Cranking paths** — transmission lines from black-start units to large generators — are energized next.
3. **Large generators** are started sequentially, each synchronized to the existing island before connecting.
4. **Load is restored incrementally** — not all at once, to prevent frequency collapse.
5. **Islands are interconnected** — separate recovered regions are synchronized and coupled only when their frequencies and voltages match within tolerance.

The critical constraint: connecting two unsynchronized islands causes a fault that can crash both. The grid must verify synchronization (frequency, phase angle, voltage) at the boundary before closing the tie switch.

### Structural Parallel

- **Black-start units** map to whichever Atrahasis layer can bootstrap independently without depending on other layers. C8's deterministic EABS replay is a strong candidate: it can reconstruct settlement state from its WAL without needing C3, C5, C6, or C7 to be operational.
- **Incremental load restoration** maps to gradually re-enabling cross-layer interactions rather than flipping everything on simultaneously.
- **Island synchronization before interconnection** is the most directly useful concept: when C3 and C8 have both recovered independently, they must verify mutual consistency (are C3's capacity snapshots consistent with C8's staked balances?) before resuming cross-layer operations.
- **Frequency as a universal health signal** — all grid participants implicitly communicate system stress through frequency deviation. This suggests a lightweight cross-layer health signal.

### Where It Breaks Down

- Power grids have a single universal coupling variable (frequency). Atrahasis layers couple through multiple distinct interfaces (claims, settlements, epochs, opinions, intents) with no single "frequency equivalent."
- Grid restoration is fundamentally about analog synchronization. Atrahasis recovery is about discrete state consistency.
- Power grids tolerate brief transients during reconnection. Atrahasis's conservation invariants (C8 CSO) are strict — no transient violations allowed.

### Design Insight

Recovery should use an "island and reconnect" pattern: each layer recovers independently into a self-consistent state, then layers are reconnected pairwise with explicit synchronization checks at each interface. The reconnection order should follow the causal dependency graph. A cross-layer "frequency equivalent" — perhaps a monotonic recovery-epoch counter — could serve as a lightweight synchronization signal.

---

## Analogy 4: Archaeological Stratigraphy and Site Reconstruction (Archaeology)

### Source Domain — Deliberately Surprising

When an archaeological site is partially destroyed (by later construction, erosion, or looting), archaeologists must reconstruct the site's history from incomplete evidence across multiple strata (layers). The key methods:

1. **Harris Matrix** — a directed acyclic graph of stratigraphic relationships (layer A was deposited before layer B, which was cut by feature C). This provides relative chronology even when absolute dates are missing.
2. **Cross-dating via artifacts** — if stratum X at Site 1 contains the same pottery type as stratum Y at Site 2, they are contemporaneous. Artifacts that appear in multiple contexts serve as synchronization markers.
3. **Terminus post quem / terminus ante quem** — a layer cannot be older than its newest artifact (TPQ) and cannot be younger than the oldest thing that sits on top of it (TAQ). This bounds the temporal uncertainty.
4. **Reconstruction from partial evidence** — archaeologists routinely reconstruct site layouts from 10-30% surviving evidence by exploiting structural regularities (walls have corners, floors are flat, hearths are central).

### Structural Parallel

- **Harris Matrix** maps to the causal dependency graph across Atrahasis layers. Even without timestamps, the causal ordering of cross-layer events (intent created -> claim submitted -> claim verified -> settlement processed) provides a DAG that constrains valid recovery states.
- **Cross-dating via artifacts** maps to cross-layer correlation markers. A settlement record in C8 that references a claim_id from C5 serves as a synchronization artifact — both layers must agree on its existence and properties.
- **TPQ/TAQ bounding** maps to using known-good events to bound the uncertainty window. If C8 successfully settled epoch N, then all claims referenced in epoch N's batch must have been verified by C5 before epoch N. This constrains C5's minimum recovery state.
- **Reconstruction from partial evidence** maps to the case where some layer's state is partially corrupted. If C6's knowledge quanta are partially lost, the surviving quanta plus C5's verification records plus C7's intent history can constrain what the missing quanta must have contained.

### Where It Breaks Down

- Archaeology is forensic (retrospective). Atrahasis recovery is operational (the system must resume functioning).
- Archaeological reconstruction tolerates uncertainty ("this is probably a granary"). Atrahasis state must be deterministically exact.
- Archaeological strata are genuinely immutable (deposited once). Atrahasis state is continuously mutated.

### Design Insight

The system should maintain "cross-layer correlation markers" — events that are recorded in multiple layers and can serve as synchronization points during recovery. The causal DAG across layers (not just within layers) should be an explicit, queryable data structure so that recovery can use Harris-Matrix-style reasoning to determine the latest mutually consistent state. Recovery from partial data is feasible if cross-layer references are sufficiently dense to constrain the missing state.

---

## Analogy 5: Quorum-Based Distributed Database Recovery with Read Repair (Distributed Systems — Dynamo/Cassandra)

### Source Domain

In Dynamo-style databases (Cassandra, Riak), data is replicated across N nodes. When a node fails and recovers:

1. **Hinted handoff** — writes intended for the failed node are stored temporarily on other nodes and forwarded when it recovers (short outages).
2. **Read repair** — when a read detects that replicas disagree, the system reconciles on the fly using vector clocks or last-write-wins, then propagates the repaired value.
3. **Anti-entropy repair** — periodic full-scan comparison using Merkle trees. Nodes exchange tree roots; if they match, the subtrees are consistent. If they differ, they recurse to find the specific divergent keys and reconcile.
4. **Consistency is eventual** — the system operates continuously during recovery. It does not stop-the-world to repair.

### Structural Parallel

- **Each Atrahasis layer as a "replica" of the system's overall state** — each layer holds a projection of the global state (C8 sees economics, C5 sees epistemic quality, C6 sees knowledge structure). They are not replicas of the same data, but they are projections that must be mutually consistent — analogous to materialized views in a database.
- **Merkle-tree anti-entropy** maps to a cross-layer consistency check. Each layer could compute a digest of its state at each epoch boundary. Cross-layer Merkle comparison would rapidly identify which epoch and which data diverged.
- **Read repair** maps to lazy, on-demand cross-layer consistency correction. When a cross-layer operation (e.g., C7 requesting C5 verification of a claim) detects an inconsistency, it triggers localized repair rather than a full system reconciliation.
- **Hinted handoff** maps to buffering cross-layer messages during partial outage (C6's queue with MAX_QUEUE_DEPTH_PER_LOCUS is already a form of this).

### Where It Breaks Down

- Dynamo replicas hold the same data. Atrahasis layers hold structurally different data with semantic coupling. "Last-write-wins" has no meaning across layers.
- Dynamo's consistency model is eventually consistent, which tolerates stale reads. Atrahasis's conservation invariants (C8 CSO) require strict consistency — you cannot "eventually" have the right AIC balance.
- Dynamo reconciliation is symmetric (any replica can be authoritative). Atrahasis has clear authority boundaries (C5 is sole claim authority, C8 is sole settlement authority per C9).

### Design Insight

Per-epoch Merkle digests at each layer boundary would enable rapid identification of the divergence point during recovery, reducing the problem from "compare all state across all layers" to "binary search for the epoch where digests diverged." The authority asymmetry is actually an advantage: unlike Dynamo, there is no ambiguity about which layer's version of a cross-layer fact is canonical. Recovery should exploit this by always reconciling toward the authoritative layer's state.

---

## Summary Matrix

| Analogy | Domain | Key Concept for T-062 | Surprise Factor |
|---------|--------|----------------------|-----------------|
| 1. Cardiac Arrest Recovery | Physiology | Strict recovery ordering, per-organ health markers, ROSC threshold | Low |
| 2. Git Rebase | Version Control | Common ancestor identification, sequential replay with per-step verification | Low |
| 3. Grid Black Start | Power Engineering | Island-and-reconnect, synchronization check before coupling, black-start bootstrap | Medium |
| 4. Archaeological Stratigraphy | Archaeology | Cross-layer correlation markers, causal DAG for bounding, reconstruction from partial evidence | High |
| 5. Dynamo Anti-Entropy | Distributed Systems | Merkle-tree divergence detection, authority-directed reconciliation, lazy read repair | Low |

## Cross-Cutting Themes

Three structural themes emerge across all five analogies:

1. **Recovery ordering is not optional.** Every domain enforces a sequence: heartbeat before perfusion, black-start before load, ancestor before replay. The Atrahasis recovery ordering must be explicit and must follow the causal dependency graph across layers.

2. **Cross-boundary synchronization checks before reconnection.** No domain reconnects subsystems blindly. Power grids check frequency match. Git checks for conflicts. Dynamo compares Merkle roots. Atrahasis needs explicit pairwise consistency predicates at each cross-layer interface.

3. **Partial reconstruction is feasible if cross-references are dense.** Archaeology and Dynamo both demonstrate that full state preservation is not necessary for recovery — sufficient cross-referencing between subsystems allows reconstruction of missing state. The existing cross-layer references in Atrahasis (claim_ids in settlements, intent_ids in claims, epoch numbers everywhere) may already provide enough correlation density for partial state reconstruction.

---

*This brief provides raw analogical material for the Ideation Council. It does not propose invention concepts, architectures, or solutions. The council should evaluate which structural parallels are load-bearing and which are decorative before advancing to concept formation.*
