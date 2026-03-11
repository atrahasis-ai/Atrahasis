# C31 — Crystallographic Adaptive Topology (CAT)

## Master Technical Specification

**Document ID:** C31-MTS-v1.0
**Version:** 1.0.0
**Date:** 2026-03-11
**Invention ID:** C31
**System:** Atrahasis Agent System v2.0
**Status:** SPECIFICATION COMPLETE
**Classification:** CONFIDENTIAL — BlakJaks LLC
**Normative References:** C3 (Tidal Noosphere v2.0), C5 (PCVM v2.0), C6 (EMA v2.0), C7 (RIF v2.0), C8 (DSF v2.0), C9 (Cross-Layer Reconciliation v1.0)
**Resolves:** C3 intra-parcel organizational gap; restores tetrahedral motif heritage within elastic parcel architecture

---

## Abstract

C3 Tidal Noosphere provides elastic, hash-ring-based parcels for agent coordination but defines no intra-parcel structure. All agents within a parcel are treated as interchangeable peers with uniform predictive weights and no role differentiation. This specification introduces **Crystallographic Adaptive Topology (CAT)**, which partitions parcel agents into **Deterministic Affinity Neighborhoods (DANs)** of 3-5 members with capability-based role assignments. DANs are computed deterministically from hash ring adjacency and integer-valued capability profiles derived from PCVM credibility data and tidal scheduling history. The mechanism is entirely optional (disabled by default), purely additive to C3, and degrades gracefully to standard C3 behavior when disabled.

CAT restores the organizational motif from the pre-AAS Tetrahedral Cluster model — small complementary groups with built-in role differentiation — while respecting the AAS architecture's requirements for determinism, integer-only computation, elastic scaling, and VRF isolation. The primary expected benefit is structured re-learning during parcel reconfiguration: intra-DAN predictive convergence in 1-2 epochs versus 3-5 epochs for uniform-weight parcels.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Heritage](#2-heritage)
3. [Architecture](#3-architecture)
   - [3.1 DAN Formation Algorithm](#31-dan-formation-algorithm)
   - [3.2 Capability Score Derivation](#32-capability-score-derivation)
   - [3.3 Role Assignment](#33-role-assignment)
   - [3.4 DAN Lifecycle](#34-dan-lifecycle)
   - [3.5 Overlapping DAN Coverage](#35-overlapping-dan-coverage)
   - [3.6 Crystal Structure (Informational)](#36-crystal-structure-informational)
   - [3.7 DAN Diversity Monitoring](#37-dan-diversity-monitoring)
4. [Communication Integration](#4-communication-integration)
5. [Cross-Layer Integration](#5-cross-layer-integration)
6. [Parameters](#6-parameters)
7. [Formal Requirements](#7-formal-requirements)
8. [Patent-Style Claims](#8-patent-style-claims)
9. [Risk Analysis](#9-risk-analysis)
10. [Deployment](#10-deployment)
11. [Appendix A: DAN Formation Pseudocode](#appendix-a-dan-formation-pseudocode)
12. [Appendix B: Capability Derivation Pseudocode](#appendix-b-capability-derivation-pseudocode)
13. [Appendix C: Role Assignment Pseudocode](#appendix-c-role-assignment-pseudocode)
14. [Appendix D: Affinity Weight Annealing Pseudocode](#appendix-d-affinity-weight-annealing-pseudocode)
15. [Appendix E: Glossary](#appendix-e-glossary)

---

## 1. Motivation

### 1.1 The Intra-Parcel Structure Gap

C3 Tidal Noosphere v2.0 defines elastic parcels of 5-25 agents governed by hash-ring-based scheduling and predictive delta communication. Within a parcel, all agents are treated as undifferentiated peers: each agent maintains predictive models of every other agent with uniform weighting, and task routing occurs via hash ring position without role awareness. This design is correct and sufficient for basic coordination, but it leaves two capabilities unrealized:

1. **Role differentiation.** In any working group, agents have different strengths. One agent may have superior verification liaison skills (high VTD acceptance rates), another may excel at compute throughput. Without role differentiation, these strengths are not leveraged — the agent with the worst VTD formatting skills is as likely to prepare a VTD as the agent with the best.

2. **Structured re-learning.** When parcels reconfigure (split, merge, agent churn), every agent must re-learn predictive models for every other agent simultaneously. With uniform weights, all predictions degrade equally. If agents could prioritize re-learning within small sub-groups first, the system could restore local predictive accuracy faster while global accuracy converges in the background.

### 1.2 The Tetrahedral Heritage

The Atrahasis system was originally conceived around a tetrahedral motif: four cooperating agents (coordinator, executor, verification liaison, memory liaison) forming a complete graph (K4), scaling through lattice repetition. When the system was formalized as AAS, the tetrahedral model was replaced by elastic parcels to support dynamic scaling. The structural insight of the tetrahedron — small complementary groups as the unit of cooperation — was lost.

C31 recovers this insight without reverting to a rigid topology. Deterministic Affinity Neighborhoods are the elastic, capability-aware generalization of the tetrahedral cell.

### 1.3 Scope

C31 specifies an optional additive layer within C3 parcels. It does NOT modify:
- C3 hash ring construction, SLV computation, bi-timescale controller, or parcel split/merge logic
- C5 VRF committee selection or claim evaluation
- C8 base settlement computation
- Any existing mechanism's correctness guarantees

C31 adds: DAN formation, capability derivation, role assignment, affinity-weighted prediction, optional coherence settlement bonus, and monitoring infrastructure.

---

## 2. Heritage

### 2.1 Lineage

| Stage | Model | Era | Key Property |
|-------|-------|-----|-------------|
| 1 | **Trinity (K3)** | Pre-AAS concept | 3 agents: reasoning, verification, coordination. Full-mesh triangle. Minimum viable cooperating unit. |
| 2 | **Tetrahedral Cluster (K4)** | Pre-AAS Noosphere spec | Trinity + memory access node. Complete graph (4 vertices, 6 edges). Built-in verification and knowledge access per cell. Fixed N=4. |
| 3 | **Lattice** | Pre-AAS Noosphere spec | Interconnected tetrahedra sharing coordination nodes. Fractal self-similarity. Small-world network. Static topology. |
| 4 | **Elastic Parcels** | AAS C3 v2.0 | Hash ring-based elastic groups. No intra-parcel structure. Deterministic O(1) scheduling. Minimum 5 agents. Variable size. |
| 5 | **CAT (DANs)** | AAS C31 | DANs of 3-5 within elastic parcels. Deterministic formation. Capability-based roles. Affinity-weighted prediction. Optional layer. |

### 2.2 What CAT Preserves

| Property | Tetrahedral Model | CAT Realization |
|----------|------------------|-----------------|
| Small-group structure | Fixed K4 (4 agents) | Elastic 3-5 agents, safety-class-determined |
| Role differentiation | Coordinator, Executor, Verification Liaison, Memory Liaison | Coordinator, Executor(s), Verifier Liaison, Knowledge Accessor |
| Built-in verification liaison | Verification node in every cell | Verifier Liaison role in every DAN (formatting only) |
| Memory/knowledge access | Memory liaison node in every cell | Knowledge Accessor role (DAN size >= 4) |
| Fractal scaling | Tetrahedra -> Lattice -> Planetary | DAN -> Crystal -> Parcel -> Locus -> Network |

### 2.3 What CAT Improves

| Tetrahedral Limitation | CAT Improvement |
|------------------------|-----------------|
| Fixed N=4 creates remainder problem | Elastic 3-5 sizing eliminates orphans |
| Static lattice requires manual configuration | Deterministic formation from hash ring state |
| Position-based roles ignore capability | Capability-based roles from PCVM history |
| Dedicated memory node wastes 25% capacity | Knowledge Accessor is optimization hint, not exclusive |
| Embedded verification creates capture risk | Verifier Liaison is formatting only; VRF is independent |
| Always-on structure | Optional by default (DAN_ENABLED=false) |

### 2.4 Tetrahedral Motif Acknowledgment

A DAN of 4 in a MEDIUM-safety locus IS a tetrahedral cell (K4). A DAN of 3 in a LOW-safety locus IS a trinity (K3). A DAN of 5 in a CRITICAL-safety locus extends the tetrahedron to K5. The tetrahedral motif is the seed from which CAT grew — preserved as a special case, not the universal form.

---

## 3. Architecture

### 3.1 DAN Formation Algorithm

The DAN formation algorithm partitions a parcel's agents into non-overlapping groups of 3-5 for each active task type. The algorithm is fully deterministic: given identical inputs, any conformant implementation MUST produce identical DANs.

#### 3.1.1 Inputs

| Input | Source | Update Frequency |
|-------|--------|-----------------|
| `hash_ring[task_type]` | C3 Section 4.1 | Rebuilt at TIDAL_EPOCH boundary |
| `agent_roster` | C3 capacity snapshot | Published at TIDAL_EPOCH boundary |
| `safety_class` | Locus governance property | Stable across epochs |
| `epoch_number` | C9 three-tier hierarchy | Increments every 3,600 seconds |
| `capability_vectors` | CAT capability pipeline (Section 3.2) | Computed at TIDAL_EPOCH boundary |
| `DAN_ENABLED` | Global configuration parameter | Governance-controlled |

#### 3.1.2 DAN Size Determination

| Safety Class | Base DAN Size | Rationale |
|-------------|:---:|-----------|
| LOW | 3 | Minimum: Coordinator + Executor + Verifier Liaison |
| MEDIUM | 4 | Standard: Coordinator + 2 Executors + Verifier Liaison |
| HIGH | 4 | Same as MEDIUM |
| CRITICAL | 5 | Maximum: Coordinator + 2 Executors + Verifier Liaison + Knowledge Accessor |

DAN size bounds: minimum 3 (below this, no meaningful role differentiation), maximum 5 (above this, coordination overhead exceeds small-group benefit per Hackman/Steiner research). If remaining agents after forming full DANs number fewer than 3, they are absorbed into the last DAN.

#### 3.1.3 Algorithm: DAN Partition

**Step 1: Extract ring ordering.** Sort all agents by their primary virtual node position (lowest hash value) on the hash ring for `task_type`, ascending. Tiebreaker: agent ID lexicographic. Produces deterministic ordered list `ring_order[0..N-1]`.

**Step 2: Compute DAN count.** `dan_count = max(1, floor(N / base_dan_size))`

**Step 3: Partition.** Distribute agents using round-robin-then-fill:

```
base_size = N / dan_count  (integer division)
remainder = N mod dan_count

For i in 0..dan_count-1:
    if i < remainder:
        DAN[i] = ring_order[i*(base_size+1) .. (i+1)*(base_size+1) - 1]
    else:
        offset = remainder * (base_size+1) + (i - remainder) * base_size
        DAN[i] = ring_order[offset .. offset + base_size - 1]
```

**Step 4: Validate.** Every DAN MUST have 3, 4, or 5 members. DANs with fewer than 3 are merged into the adjacent DAN.

**Step 5: Record.** For each DAN, record member list and anchor agent (member with primary vnode position closest to 0; tiebreaker: lowest agent ID).

**Determinism proof:** Step 1 uses SHA256 hash positions with agent ID tiebreaking. Steps 2-5 use integer arithmetic only. No floating-point, no randomness, no external state beyond declared inputs. Two conformant implementations with identical inputs MUST produce byte-identical results.

**Complexity:** O(N log N) per task type. At design targets (N=10, T=20): ~2,000 operations. Negligible.

#### 3.1.4 Multi-Task-Type DAN Computation

The algorithm runs independently for each active task type. An agent may be in different DANs for different task types. Total DAN membership is bounded by `DAN_MEMBERSHIP_CAP` (default: 5).

When a parcel has more than `DAN_MEMBERSHIP_CAP` active task types, task types are clustered by hash proximity on a meta-ring (SHA256(task_type_id)), divided into `DAN_MEMBERSHIP_CAP` evenly-spaced segments. Task types in the same segment share one DAN computation.

### 3.2 Capability Score Derivation

Capability scores are derived from PCVM verification history and tidal scheduling history — never self-reported. All scores are integers in range [0, 1000].

#### 3.2.1 Five Capability Dimensions

| Dimension | Code | Data Source | Measures |
|-----------|------|-------------|----------|
| Compute Throughput | COMP | C3 tidal history | Task completion rate |
| Verification Liaison | VLSN | C5 PCVM VTD history | VTD acceptance rate with diversity |
| Reasoning Depth | RDEP | C5 PCVM credibility | Credibility for R-class and H-class claims |
| Knowledge Access | KACC | C6 EMA metrics | Retrieval quality (Phase 2 extension) |
| Memory Bandwidth | MBND | C6 EMA metrics | Consolidation throughput (Phase 2 extension) |

KACC and MBND require C6 EMA to expose interaction quality metrics. Phase 1 deploys with COMP, VLSN, and RDEP; KACC and MBND default to 500 until C6 metrics are available.

#### 3.2.2 Derivation Functions (Integer-Only)

All intermediate computations use integer arithmetic. Division rounds toward zero.

```
function normalize_to_1000(numerator: uint64, denominator: uint64) -> uint16:
    if denominator == 0: return 500
    return min(1000, (numerator * 1000) / denominator)
```

**COMP — Compute Throughput:**
```
COMP = normalize_to_1000(tasks_completed, tasks_assigned)
```
Over a trailing window of `CAPABILITY_WINDOW_EPOCHS` (default 10) TIDAL_EPOCHs.

**VLSN — Verification Liaison (with diversity factor):**
```
acceptance_rate = normalize_to_1000(vtd_accepted, vtd_submissions)
classes_covered = max(1, distinct_claim_classes)  // [1..9]
diversity_factor = 333 + (667 * (classes_covered - 1)) / 8
VLSN = (acceptance_rate * diversity_factor) / 1000
```

The diversity factor maps coverage of 1 claim class to a 33.3% multiplier, scaling linearly to 100% for all 9 classes. This prevents single-class gaming.

**RDEP — Reasoning Depth:**
```
RDEP = pcvm_credibility(agent, ['R', 'H']).belief_fixed_point  // uint16 [0, 1000]
```

**KACC and MBND** follow the same `normalize_to_1000` pattern on C6 EMA counters, defaulting to 500 when unavailable.

#### 3.2.3 Vector Assembly and Freshness

Each agent computes its capability vector at epoch boundary (5 x uint16 = 10 bytes). The vector includes a `freshness_epoch` field. If `freshness_epoch < current_epoch - 2`, the vector is stale and replaced with defaults (500 on all dimensions). Any agent can independently recompute any other agent's vector from shared PCVM and tidal history.

### 3.3 Role Assignment

Once DAN membership is determined, roles are assigned based on capability scores. Assignment is deterministic with integer-only comparisons and agent-ID tiebreaking.

#### 3.3.1 Role Definitions

| Role | Count per DAN | Primary Capability | Description |
|------|:---:|------|-------------|
| Coordinator | 1 | COMP | Highest compute throughput. DAN anchor for RIF PE routing. |
| Verifier Liaison | 1 | VLSN | Prepares/submits VTDs. Does NOT evaluate claims or participate in VRF selection. |
| Knowledge Accessor | 0-1 | KACC | Present in DANs >= 4 with KACC data. Preferred EMA interaction point. |
| Executor | 1+ | (remaining) | Execute tasks assigned by Coordinator. |

**CRITICAL CONSTRAINT:** The Verifier Liaison is an operational formatting role, NOT a verification role. It does NOT evaluate claims, does NOT participate in VRF committee selection, does NOT have knowledge of VRF committee composition, and has NO influence over verification outcomes. DAN roles and VRF committee membership are fully orthogonal systems.

#### 3.3.2 Assignment Algorithm

```
function assign_roles(members, capabilities):
    remaining = copy(members)
    coordinator = select_best(remaining, COMP)   // Highest COMP
    verifier   = select_best(remaining, VLSN)    // Highest VLSN
    if len(members) >= 4 and kacc_available():
        ka     = select_best(remaining, KACC)    // Highest KACC
    rest = Executors

function select_best(candidates, dimension):
    Return candidate with highest score on dimension.
    Tiebreaker: lowest agent_id (lexicographic on 256-bit identifier).
```

Roles are recomputed every epoch from current capability vectors and DAN membership. Role stability is naturally dampened by the 10-epoch sliding window for capability derivation.

### 3.4 DAN Lifecycle

#### 3.4.1 Formation Timeline

```
T+0ms:    C3 hash ring reconstruction begins
T+Xms:    Hash rings complete (~100ms)
T+Xms:    Capability vectors computed
T+X+1ms:  DAN partition runs per task type
T+X+2ms:  Role assignment runs per DAN
T+X+3ms:  Affinity weights updated
T+X+4ms:  DAN membership/roles published in capacity snapshot
```

Total DAN computation at design targets (N=10, T=20): < 5ms, adding < 5% epoch boundary overhead.

#### 3.4.2 Steady-State Operation

Between epoch boundaries, DANs are stable. No mid-epoch recomputation. Agents use DAN membership for task routing (via Coordinator), VTD preparation (via Verifier Liaison), knowledge access (via Knowledge Accessor), and affinity-weighted prediction.

#### 3.4.3 Churn Handling

**Agent departure mid-epoch:** DAN operates with DAN_SIZE-1 members. Role inheritance: Coordinator departs -> next-highest COMP inherits; Verifier Liaison/Knowledge Accessor depart -> fallback to standard C3 behavior. Full recomputation at next epoch boundary.

**Agent arrival mid-epoch:** New agent operates without DAN affiliation until next epoch boundary, using standard C3 scheduling. Incorporated into DAN computation at next epoch.

#### 3.4.4 Parcel Split and Merge

On split: two new parcels, DANs recomputed independently. On merge: combined parcel, DANs recomputed for full agent set. In both cases, affinity weights enter annealing phase for new DAN partnerships.

### 3.5 Overlapping DAN Coverage

Because DANs are computed per task type, agents may belong to different DANs for different task types. This creates implicit inter-DAN bonds through shared members. Coverage guarantee: every agent belongs to at least one DAN per active task type (guaranteed by partition algorithm).

### 3.6 Crystal Structure (Informational)

**This section is INFORMATIONAL, not NORMATIVE. No algorithm depends on crystal classification.**

The crystal structure is the emergent topology of DANs and their inter-DAN bonds within a parcel. Defined for monitoring and analysis only.

**Node:** A DAN. **Bond:** Two DANs sharing at least one member. **Weight:** Count of shared agents.

| Classification | Condition | Interpretation |
|---------------|-----------|----------------|
| ISOLATED | No bonds | DANs operate independently |
| SPARSE | Average bond weight < 1.5 | Limited inter-DAN coupling |
| CONNECTED | Connected graph, avg weight in [1.5, 3.0] | Normal operating state |
| DENSE | Average bond weight > 3.0 or complete graph | High coupling; effectively uniform weights |

**Metrics (monitoring only):**

| Metric | Formula | Purpose |
|--------|---------|---------|
| `crystal_density` | `2*|E| / (|V|*(|V|-1))` | Graph density |
| `min_dan_credibility` | Min average member credibility | Identifies weak DANs |

Crystal classification logged at each epoch boundary. DENSE classification persisting > 5 epochs generates an operational advisory.

### 3.7 DAN Diversity Monitoring

#### 3.7.1 Credibility Floor Check

At each epoch boundary, DANs where all members have below-median RDEP (parcel median) are flagged. Consecutive alerts for `DAN_DIVERSITY_ALERT_THRESHOLD` (default: 3) epochs escalate to MEDIUM severity and report to the Locus Decomposer (C7).

#### 3.7.2 Sybil Clustering Detection (Advisory)

**This check is ADVISORY with expected false positives. No automated enforcement.**

DANs are flagged where: (a) all members joined the parcel within the same epoch, OR (b) all members have capability vectors within Euclidean distance < `DAN_SYBIL_DISTANCE_THRESHOLD` (default: 50). Flags serve as input to human review.

---

## 4. Communication Integration

### 4.1 Affinity-Weighted Prediction

CAT modifies C3's Predictive Delta Channel weight function:

```
function prediction_weight(agent_A, agent_B, task_type) -> uint16:
    if not DAN_ENABLED:
        return 1000  // Uniform: exact current C3 behavior

    if same_dan(A, B, task_type):
        return AFFINITY_WEIGHT_INTRA_DAN         // default: 1000
    elif share_any_dan(A, B):
        return AFFINITY_WEIGHT_CROSS_DAN_BONDED   // default: 700
    else:
        return AFFINITY_WEIGHT_CROSS_DAN           // default: 300
```

Weight 300 (not 0) ensures predictions are maintained for all parcel members. DANs prioritize, not partition.

**Effect on communication:** Higher prediction accuracy for DAN partners means fewer intra-DAN surprise deltas. Total volume is approximately unchanged; distribution is restructured.

**Effect on reconfiguration:** Intra-DAN re-learning is prioritized (weight 1000), enabling small-group predictive convergence in 1-2 epochs while inter-DAN convergence continues at reduced priority over 3-5 epochs. This is the primary expected benefit of CAT.

### 4.2 Affinity Weight Annealing

When DANs change at epoch boundary, weights anneal over `AFFINITY_RAMP_EPOCHS` (default: 3) to prevent oscillation:

```
function annealed_weight(target, previous, epochs_since_change) -> uint16:
    if epochs_since_change >= AFFINITY_RAMP_EPOCHS:
        return target
    delta = target - previous
    return previous + (delta * epochs_since_change) / AFFINITY_RAMP_EPOCHS
```

Integer arithmetic only. Monotonicity guaranteed: newly formed DANs ramp up, dissolved DANs ramp down.

When `DAN_ENABLED` transitions false->true, all weights start at 1000 (uniform) and anneal toward targets.

### 4.3 Stigmergic Decay Channel Interaction

DANs do not modify C3's stigmergic decay mechanism. Signals remain parcel-scoped. DAN structure influences signal relevance implicitly through prediction weights, not through new stigmergic infrastructure. Crystal bonds (shared members between DANs) serve as natural signal propagation conduits.

### 4.4 Gossip Protocol

CAT does not modify C3's uniform random gossip protocol. Phase 2 monitoring tracks whether gossip naturally converges faster within DANs and whether crystal bonds accelerate cross-DAN convergence. DAN-aware gossip targeting is deferred to Phase 3 pending monitoring data.

---

## 5. Cross-Layer Integration

### 5.1 C3 Tidal Noosphere

**New section (proposed C3 Section 4.11): Deterministic Affinity Neighborhoods.** Contains DAN formation algorithm, lifecycle, edge case handling. Purely additive.

**Modified section (C3 Section 6.2): Predictive Delta Channel.** Affinity weight modification replaces uniform weights with DAN-aware weights when DAN_ENABLED=true.

**New parameters (C3 Appendix B):** All 17 parameters from Section 6.

**Hash ring interaction:** DANs are computed AFTER hash rings. Hash ring construction is unchanged. DANs read hash ring state but do not modify it.

**Bi-timescale controller interaction:** Controller operates on SLV metrics. DANs do not modify SLV. Controller split/merge decisions are unaffected.

### 5.2 C5 PCVM

**VRF isolation guarantee:** VRF committee selection (C5 Sections 5.2-5.6) inputs are: VRF seed, agent public keys, diversity attributes, claim hash. None include DAN membership, DAN role, or crystal structure. DAN structure is invisible to VRF selection by construction. No C5 modification needed.

**Clarification note (proposed C5 Section 11 addition):**

> "The DAN Verifier Liaison role (C31 CAT) is an operational formatting role within the task execution layer. It prepares and submits VTDs but does not evaluate claims, does not participate in VRF committee selection for claims it submits, and has no access to committee composition. DAN structure is fully orthogonal to PCVM verification. VRF committee selection MUST NOT incorporate DAN membership or DAN role as inputs."

**Data dependency:** CAT reads from C5 (credibility scores for capability derivation) but does not write to C5.

### 5.3 C6 EMA (Phase 2)

**Optimization note:** When CAT is enabled, the Knowledge Accessor role is the preferred EMA interaction point within each DAN. This is an optimization hint — any agent MAY invoke EMA APIs directly.

**Metrics interface requirement:** C6 must expose two counters for full capability vector derivation:
1. `retrieval_relevant_count(agent_id, window)`
2. `consolidation_successes(agent_id, window)`

Until available, KACC and MBND default to 500.

### 5.4 C7 RIF

When DAN_ENABLED=true and an intent specifies `dan_routing=true`, the Parcel Executor routes to the appropriate DAN member by role:

| Intent Requirement | DAN Routing Target |
|---|---|
| General compute | Coordinator (distributes to Executors) |
| VTD preparation | Verifier Liaison |
| Knowledge retrieval | Knowledge Accessor (if present; else Executor) |
| No specific role | Coordinator |

The DAN is NOT a new decomposition tier — it is a routing optimization within the existing PE level. The LD is unaware of DAN structure.

**Fallback:** Intents without `dan_routing=true` use current direct-to-agent routing. If Coordinator is unreachable, PE falls back to direct routing.

### 5.5 C8 DSF

**DAN Coherence Bonus (optional, disabled by default):**

```
function compute_dan_coherence_bonus(agent, dan_history, base_reward):
    if not DAN_COHERENCE_BONUS_ENABLED: return 0
    consecutive = count_consecutive_stable_epochs(agent, dan_history)
    ramp_factor = min(consecutive, DAN_COHERENCE_BONUS_RAMP_EPOCHS)
    bonus = (base_reward * DAN_COHERENCE_BONUS_MAX_BPS * ramp_factor) /
            (DAN_COHERENCE_BONUS_RAMP_EPOCHS * 10000)
    return bonus
```

Computed by Settlement Calculator (C8 Component 11). Integer arithmetic only.

**Governance gate:** DAN_COHERENCE_BONUS_ENABLED requires G-class governance vote.

**Circuit breaker:** If Gini coefficient of coherence bonuses in a locus exceeds `DAN_COHERENCE_GINI_LIMIT` (default: 0.40), bonus is automatically disabled for the next CONSOLIDATION_CYCLE (36,000 seconds) and a governance alert is raised.

**Reset on reconfiguration:** Coherence bonus resets to zero on parcel split/merge to prevent indefinite accumulation.

---

## 6. Parameters

### 6.1 Complete Parameter Table

| ID | Parameter | Type | Default | Range | Governance |
|---|-----------|------|---------|-------|------------|
| P-01 | `DAN_ENABLED` | bool | false | {true, false} | G-class |
| P-02 | `DAN_SIZE_LOW` | uint8 | 3 | [3, 5] | G-class |
| P-03 | `DAN_SIZE_MEDIUM` | uint8 | 4 | [3, 5] | G-class |
| P-04 | `DAN_SIZE_HIGH` | uint8 | 4 | [3, 5] | G-class |
| P-05 | `DAN_SIZE_CRITICAL` | uint8 | 5 | [3, 5] | G-class |
| P-06 | `DAN_MEMBERSHIP_CAP` | uint8 | 5 | [3, 10] | G-class |
| P-07 | `AFFINITY_WEIGHT_INTRA_DAN` | uint16 | 1000 | [500, 1000] | Operational |
| P-08 | `AFFINITY_WEIGHT_CROSS_DAN_BONDED` | uint16 | 700 | [300, 1000] | Operational |
| P-09 | `AFFINITY_WEIGHT_CROSS_DAN` | uint16 | 300 | [100, 700] | Operational |
| P-10 | `AFFINITY_RAMP_EPOCHS` | uint8 | 3 | [1, 10] | Operational |
| P-11 | `CAPABILITY_WINDOW_EPOCHS` | uint8 | 10 | [5, 50] | Operational |
| P-12 | `DAN_COHERENCE_BONUS_ENABLED` | bool | false | {true, false} | G-class |
| P-13 | `DAN_COHERENCE_BONUS_MAX_BPS` | uint16 | 500 | [100, 500] | G-class |
| P-14 | `DAN_COHERENCE_BONUS_RAMP_EPOCHS` | uint8 | 5 | [3, 20] | G-class |
| P-15 | `DAN_COHERENCE_GINI_LIMIT` | uint16 | 400 | [200, 600] | G-class |
| P-16 | `DAN_DIVERSITY_ALERT_THRESHOLD` | uint8 | 3 | [2, 10] | Operational |
| P-17 | `DAN_SYBIL_DISTANCE_THRESHOLD` | uint16 | 50 | [10, 200] | Operational |

### 6.2 Parameter Interaction Constraints

1. **Monotonicity:** `AFFINITY_WEIGHT_INTRA_DAN >= AFFINITY_WEIGHT_CROSS_DAN_BONDED >= AFFINITY_WEIGHT_CROSS_DAN`. If violated by governance, the system sorts the three values and assigns intra=max, bonded=median, cross=min.

2. **Dependency:** `DAN_COHERENCE_BONUS_ENABLED` requires `DAN_ENABLED=true`. Setting the bonus to true while DAN_ENABLED=false is a no-op.

3. **Clamping:** All `DAN_SIZE_*` parameters are clamped to [3, 5].

4. **Transition smoothing:** When `DAN_ENABLED` transitions false->true, all affinity weights initialize to 1000 (uniform) and anneal toward targets over `AFFINITY_RAMP_EPOCHS`.

---

## 7. Formal Requirements

### 7.1 Functional Requirements

| ID | Requirement | Priority | Verification |
|----|-------------|----------|-------------|
| FR-01 | When DAN_ENABLED=false, the system SHALL behave identically to C3 without CAT. No DAN computation, no affinity weighting, no coherence bonus. | P0 | Behavioral equivalence test |
| FR-02 | DAN formation SHALL be deterministic: identical inputs MUST produce identical DANs across all conformant implementations. | P0 | Canonical test suite (10 cases) |
| FR-03 | All capability scores SHALL be integers in range [0, 1000]. No floating-point SHALL enter the DAN computation path. | P0 | Static analysis + unit test |
| FR-04 | DAN size SHALL be in [3, 5]. No DAN with fewer than 3 or more than 5 members SHALL be formed. | P0 | Partition validation test |
| FR-05 | Tie-breaking in role assignment and ring ordering SHALL use agent ID lexicographic comparison. | P0 | Determinism test |
| FR-06 | The Verifier Liaison role SHALL NOT evaluate claims, participate in VRF committee selection, or have access to committee composition. | P0 | Architecture review + integration test |
| FR-07 | VRF committee selection (C5) SHALL NOT incorporate DAN membership or DAN role as inputs. | P0 | C5 interface audit |
| FR-08 | Capability vectors SHALL be derived from PCVM and tidal history only. No self-reported data SHALL be used. | P0 | Derivation audit |
| FR-09 | VLSN capability derivation SHALL include a diversity factor penalizing single-claim-class concentration. | P0 | Unit test |
| FR-10 | Affinity weights SHALL anneal over AFFINITY_RAMP_EPOCHS when DAN membership changes. Weights SHALL NOT change discontinuously at epoch boundaries. | P0 | Transition test |
| FR-11 | When an agent departs mid-epoch, the DAN SHALL continue operating with reduced membership and role inheritance for Coordinator (next-highest COMP). | P1 | Churn simulation |
| FR-12 | DAN membership count per agent SHALL NOT exceed DAN_MEMBERSHIP_CAP. Task type clustering SHALL enforce this bound. | P0 | Membership counting test |
| FR-13 | DAN computation SHALL complete in < 5ms at design targets (N=10 agents, T=20 task types). | P1 | Performance benchmark |
| FR-14 | DAN diversity monitoring SHALL flag DANs where all members have below-median RDEP for DAN_DIVERSITY_ALERT_THRESHOLD consecutive epochs. | P1 | Monitoring test |
| FR-15 | The DAN coherence bonus SHALL be disabled by default and SHALL require G-class governance vote to enable. | P0 | Configuration audit |
| FR-16 | The Gini circuit breaker SHALL disable the coherence bonus for one CONSOLIDATION_CYCLE when the Gini coefficient exceeds DAN_COHERENCE_GINI_LIMIT. | P0 | Circuit breaker test |
| FR-17 | The coherence bonus SHALL reset to zero on parcel reconfiguration (split or merge). | P1 | Settlement test |
| FR-18 | Crystal structure classification SHALL be logged at each epoch boundary but SHALL NOT trigger any automated behavioral change. | P1 | Monitoring validation |
| FR-19 | Capability vectors for agents with < CAPABILITY_WINDOW_EPOCHS history SHALL default to 500 on all dimensions. | P1 | New agent test |
| FR-20 | When DAN_ENABLED transitions false->true, all affinity weights SHALL initialize to 1000 and anneal toward targets. | P0 | Transition test |

### 7.2 Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-01 | DAN computation overhead SHALL add < 5% to epoch boundary processing time. | P1 |
| NFR-02 | Capability vector size SHALL be <= 10 bytes per agent (5 x uint16). | P1 |
| NFR-03 | DAN formation pseudocode SHALL include a canonical test suite of 10 inputs with expected outputs in the implementation guide. | P1 |

---

## 8. Patent-Style Claims

### Claim 1: Deterministic Affinity Neighborhoods within Elastic Agent Parcels

A method for organizing artificial intelligence agents within elastic hash-ring-based parcels, comprising:
(a) partitioning parcel agents into non-overlapping groups of 3-5 members using deterministic ring-ordering derived from bounded-loads consistent hash ring virtual node positions;
(b) computing integer-valued capability profiles for each agent from verification trace document history and task scheduling history across five dimensions;
(c) assigning differentiated roles (Coordinator, Verifier Liaison, Knowledge Accessor, Executor) within each group based on capability scores with deterministic tiebreaking;
(d) weighting inter-agent predictive models by intra-group affinity, cross-group bond affinity, and unaffiliated affinity;
wherein the groups provide structured re-learning during parcel reconfiguration while maintaining full determinism and graceful degradation to uniform-weight behavior when disabled.

### Claim 2: Crystal Topology from Overlapping Task-Type Group Membership

A method for creating emergent inter-group communication topology in a multi-agent system, comprising:
(a) computing independent agent groups per task type within a shared parcel;
(b) defining inter-group bonds through shared member agents;
(c) monitoring the resulting crystal graph for density, connectivity, and credibility distribution;
wherein information flows between groups through shared members without explicit inter-group communication protocols, and the topology adapts automatically as task type distributions change.

### Claim 3: Capability-Based Role Assignment with Diversity-Penalized Verification Liaison Scoring

A method for assigning operational roles within small agent groups, comprising:
(a) deriving integer capability scores from external verification and scheduling data, not self-reported attributes;
(b) incorporating a diversity factor that penalizes agents concentrating on a single claim class, requiring breadth across the canonical claim class taxonomy;
(c) assigning roles in priority order (Coordinator by compute throughput, Verifier Liaison by diversity-weighted verification quality, Knowledge Accessor by retrieval quality);
(d) maintaining strict separation between the operational Verifier Liaison role and the independent VRF-based verification committee selection;
wherein role assignment incentivizes broad capability development while preserving verification independence.

### Claim 4: Coherence Settlement Bonus with Gini Circuit Breaker

A method for incentivizing stable agent group membership in a token-settled multi-agent economy, comprising:
(a) computing a linearly ramping settlement bonus for agents maintaining identical group membership across consecutive epochs;
(b) capping the maximum bonus as a percentage of base reward;
(c) monitoring the Gini coefficient of bonus distribution across the agent population;
(d) automatically disabling the bonus mechanism when wealth concentration exceeds a governance-defined threshold;
(e) resetting the bonus on parcel reconfiguration to prevent indefinite accumulation;
wherein group stability is rewarded without creating systemic wealth concentration.

---

## 9. Risk Analysis

### 9.1 Risk Register

| ID | Risk | Prob. | Impact | Severity | Mitigation |
|----|------|-------|--------|----------|-----------|
| R-01 | Non-determinism bug in DAN computation (different implementations produce different DANs) | 10% | CRITICAL | HIGH | Integer-only arithmetic (FR-03), stable sort with agent-ID tiebreaker (FR-05), canonical test suite (NFR-03) |
| R-02 | Capability vector pipeline produces stale/garbage data | 15% | MEDIUM | MEDIUM | Freshness check (FR-19), graceful degradation to position-based assignment, MEDIUM alert when >50% agents have stale vectors |
| R-03 | Coherence bonus creates unintended wealth concentration | 15% | MEDIUM | MEDIUM | Gini circuit breaker (FR-16), disabled by default (FR-15), 5% cap (P-13), reset on reconfiguration (FR-17) |
| R-04 | Crystal structure becomes pathologically dense (T >> N) | 20% | LOW | LOW | DAN_MEMBERSHIP_CAP limits memberships, DENSE classification generates advisory. Degrades to uniform-weight (baseline) behavior — no worse than current system |
| R-05 | DAN-aware routing causes task starvation via Coordinator bottleneck | 10% | HIGH | MEDIUM | Coordinator does immediate distribution (no queue), dan_routing is optional per-intent, PE falls back to direct routing when Coordinator unreachable |
| R-06 | Verifier Liaison role creates perception of verification capture | 10% | LOW | LOW | FR-06/FR-07 mandate strict separation, C5 clarification note (Section 5.2), architectural isolation by construction |
| R-07 | DAN formation adds latency to epoch boundary processing | 5% | LOW | NEGLIGIBLE | < 5ms at design targets (FR-13), < 5% overhead (NFR-01) |

### 9.2 Residual Risks

1. **Benefit uncertainty.** The 20% transient communication reduction from structured re-learning is a projection based on small-group coordination research, not empirical measurement within the AAS system. Actual benefit may be lower or negligible. Mitigation: DAN_ENABLED=false by default; enablement requires empirical validation (IC-6).

2. **Parameter surface complexity.** 17 parameters for an optional mechanism is a significant governance surface. However, 8 are disabled-by-default (coherence bonus family) or informational (monitoring thresholds). Operationally active parameter count when DAN_ENABLED=true is 9.

---

## 10. Deployment

### 10.1 Phase 1: Disabled (Months 0-18)

| Component | Status |
|-----------|--------|
| DAN_ENABLED | false |
| All DAN computation | Skipped |
| Capability derivation | Not computed |
| Affinity weighting | Uniform (1000) |
| System behavior | Identical to C3 without CAT |

Phase 1 goal: specification review, implementation, canonical test suite validation. No runtime impact.

### 10.2 Phase 2: Shadow Mode (Months 18-30)

| Component | Status |
|-----------|--------|
| DAN_ENABLED | true (shadow) |
| DAN computation | Active, results logged but NOT used for routing or prediction |
| Capability derivation | Active (3 of 5 dimensions: COMP, VLSN, RDEP) |
| Affinity weighting | Computed and logged but NOT applied (uniform weights in production) |
| Coherence bonus | Disabled |
| Monitoring | Crystal classification, diversity alerts, DAN stability metrics |

Phase 2 goal: validate determinism across implementations, measure DAN stability metrics, identify parameter tuning needs. Compare shadow DAN predictions against actual communication patterns.

**Phase 2 Validation Gates (all must pass for Phase 3 enablement):**

| Gate | Criterion |
|------|-----------|
| VG-1 | Determinism: 100% agreement across 3+ implementations on canonical test suite |
| VG-2 | Stability: DAN membership changes < 20% per epoch on average (excluding churn events) |
| VG-3 | Diversity: < 10% of DANs trigger below-median credibility alerts for > 3 consecutive epochs |
| VG-4 | Performance: DAN computation < 5ms at deployment scale |
| VG-5 | No VRF interference: zero instances of DAN data appearing in VRF selection inputs |

### 10.3 Phase 3: Enabled (Month 30+, contingent on VG-1 through VG-5)

| Component | Status |
|-----------|--------|
| DAN_ENABLED | true (active) |
| DAN computation | Active, used for routing and prediction |
| Capability derivation | 3 dimensions (5 if C6 metrics available) |
| Affinity weighting | Active (DAN-aware weights applied) |
| Coherence bonus | Disabled (requires separate G-class vote) |
| Monitoring | Full crystal + diversity + Sybil detection |

Phase 3 enablement requires:
- All 5 validation gates passed
- AiSIA recommendation with empirical analysis
- G-class governance vote (Stiftung board ratification)

### 10.4 Phase 4: Full Operation (Month 36+, contingent on Phase 3 performance data)

| Component | Status |
|-----------|--------|
| All Phase 3 components | Active, tuned |
| Capability derivation | 5 dimensions (C6 metrics available) |
| Coherence bonus | Eligible for G-class enablement vote |
| DAN-aware gossip | Evaluated based on Phase 3 monitoring data |

---

## Appendix A: DAN Formation Pseudocode

```
function form_dans(
    parcel_id: ParcelId,
    task_type: TaskType,
    agent_roster: List[AgentId],
    hash_ring: HashRing,
    safety_class: SafetyClass,
    capabilities: Map[AgentId, CapabilityVector]
) -> List[DAN]:

    if not DAN_ENABLED:
        return []

    N = len(agent_roster)
    if N < 3:
        return []

    // Step 1: Base DAN size from safety class
    base_size = match safety_class:
        LOW:      DAN_SIZE_LOW
        MEDIUM:   DAN_SIZE_MEDIUM
        HIGH:     DAN_SIZE_HIGH
        CRITICAL: DAN_SIZE_CRITICAL

    // Step 2: Extract ring ordering
    ring_order = stable_sort(agent_roster,
        key = lambda a: (min_vnode_hash(hash_ring, a), a))

    // Step 3: Compute DAN count and partition
    dan_count = max(1, N / base_size)   // integer division
    remainder = N mod dan_count

    dans = []
    offset = 0
    for i in 0..dan_count - 1:
        size = base_size + (1 if i < remainder else 0)
        members = ring_order[offset .. offset + size - 1]
        offset += size

        // Step 4: Validate minimum size
        if len(members) < 3:
            dans[len(dans) - 1].members.extend(members)
            continue

        // Step 5: Assign roles
        roles = assign_roles(members, capabilities)

        // Step 6: Record
        anchor = members[0]
        dans.append(DAN(
            id = hash(parcel_id, task_type, epoch_number, anchor),
            members = members,
            roles = roles,
            anchor = anchor,
            task_type = task_type,
            parcel_id = parcel_id
        ))

    return dans
```

---

## Appendix B: Capability Derivation Pseudocode

```
function derive_capability_vector(
    agent_id: AgentId,
    tidal_history: TidalHistory,
    pcvm_history: PCVMHistory,
    ema_metrics: Optional[EMAMetrics],
    window: uint32 = CAPABILITY_WINDOW_EPOCHS
) -> CapabilityVector:

    // COMP: Compute Throughput
    assigned = tidal_history.tasks_assigned(agent_id, window)
    completed = tidal_history.tasks_completed(agent_id, window)
    COMP = normalize_to_1000(completed, assigned)

    // VLSN: Verification Liaison (with diversity factor)
    submissions = pcvm_history.vtd_submissions(agent_id, window)
    accepted = pcvm_history.vtd_accepted(agent_id, window)
    acceptance_rate = normalize_to_1000(accepted, submissions)
    classes_covered = max(1, pcvm_history.distinct_claim_classes(agent_id, window))
    diversity_factor = 333 + (667 * (classes_covered - 1)) / 8
    VLSN = (acceptance_rate * diversity_factor) / 1000

    // RDEP: Reasoning Depth
    opinion = pcvm_history.credibility(agent_id, ['R', 'H'])
    RDEP = opinion.belief_fixed_point

    // KACC: Knowledge Access (Phase 2)
    if ema_metrics is not None and ema_metrics.available():
        KACC = normalize_to_1000(
            ema_metrics.retrieval_relevant_count(agent_id, window),
            ema_metrics.retrieval_count(agent_id, window))
    else:
        KACC = 500

    // MBND: Memory Bandwidth (Phase 2)
    if ema_metrics is not None and ema_metrics.available():
        MBND = normalize_to_1000(
            ema_metrics.consolidation_successes(agent_id, window),
            ema_metrics.consolidation_attempts(agent_id, window))
    else:
        MBND = 500

    // Freshness check
    freshness = tidal_history.most_recent_epoch(agent_id)
    if current_epoch() - freshness > 2:
        return CapabilityVector(500, 500, 500, 500, 500, freshness)

    return CapabilityVector(COMP, VLSN, RDEP, KACC, MBND, freshness)


function normalize_to_1000(numerator: uint64, denominator: uint64) -> uint16:
    if denominator == 0: return 500
    return min(1000, (numerator * 1000) / denominator)
```

---

## Appendix C: Role Assignment Pseudocode

```
function assign_roles(
    members: List[AgentId],
    capabilities: Map[AgentId, CapabilityVector]
) -> Map[AgentId, Role]:

    assignments = {}
    remaining = list(members)

    // 1. Coordinator: highest COMP
    coord = select_best(remaining, capabilities, COMP)
    assignments[coord] = COORDINATOR
    remaining.remove(coord)

    // 2. Verifier Liaison: highest VLSN
    vl = select_best(remaining, capabilities, VLSN)
    assignments[vl] = VERIFIER_LIAISON
    remaining.remove(vl)

    // 3. Knowledge Accessor: highest KACC (if DAN >= 4 and KACC available)
    if len(members) >= 4 and kacc_available():
        ka = select_best(remaining, capabilities, KACC)
        assignments[ka] = KNOWLEDGE_ACCESSOR
        remaining.remove(ka)

    // 4. Remaining are Executors
    for agent in remaining:
        assignments[agent] = EXECUTOR

    return assignments


function select_best(
    candidates: List[AgentId],
    capabilities: Map[AgentId, CapabilityVector],
    dimension: Dimension
) -> AgentId:
    best = candidates[0]
    best_score = capabilities[best][dimension]
    for agent in candidates[1:]:
        score = capabilities[agent][dimension]
        if score > best_score:
            best = agent
            best_score = score
        elif score == best_score and agent < best:
            best = agent
    return best
```

---

## Appendix D: Affinity Weight Annealing Pseudocode

```
function compute_affinity_weight(
    agent_A: AgentId,
    agent_B: AgentId,
    task_type: TaskType,
    dan_index: DANIndex,
    previous_weight: uint16,
    epochs_since_dan_change: uint32
) -> uint16:

    if not DAN_ENABLED:
        return 1000  // Uniform: exact C3 behavior

    // Determine target weight
    dan_A = dan_index.get_dan(agent_A, task_type)
    dan_B = dan_index.get_dan(agent_B, task_type)

    if dan_A is not None and dan_A == dan_B:
        target = AFFINITY_WEIGHT_INTRA_DAN
    elif dan_index.share_any_dan(agent_A, agent_B):
        target = AFFINITY_WEIGHT_CROSS_DAN_BONDED
    else:
        target = AFFINITY_WEIGHT_CROSS_DAN

    // Apply annealing
    if epochs_since_dan_change >= AFFINITY_RAMP_EPOCHS:
        return target

    delta = (target as int32) - (previous_weight as int32)
    annealed = previous_weight + (delta * epochs_since_dan_change) / AFFINITY_RAMP_EPOCHS
    return clamp(annealed, 0, 1000) as uint16
```

---

## Appendix E: Glossary

| Term | Definition |
|------|-----------|
| **Affinity weight** | Integer prediction weight [0, 1000] determining how much effort an agent invests in predicting another agent's behavior |
| **Annealing** | Gradual transition of affinity weights over AFFINITY_RAMP_EPOCHS to prevent discontinuities |
| **Bond** | Connection between two DANs sharing at least one member agent |
| **Capability vector** | 5-dimensional integer profile [0, 1000] per dimension: COMP, VLSN, RDEP, KACC, MBND |
| **CAT** | Crystallographic Adaptive Topology — the system defined by this specification |
| **COMP** | Compute Throughput capability dimension — task completion rate |
| **Coordinator** | DAN role assigned to agent with highest COMP score; serves as routing anchor |
| **Crystal** | Emergent graph topology of DANs and bonds within a parcel (informational) |
| **DAN** | Deterministic Affinity Neighborhood — group of 3-5 agents within a parcel |
| **DAN_ENABLED** | Master switch for all CAT functionality; false by default |
| **Diversity factor** | Multiplier [333, 1000] penalizing VLSN scores for agents covering few claim classes |
| **Executor** | DAN role for agents not assigned Coordinator, Verifier Liaison, or Knowledge Accessor |
| **Freshness epoch** | Most recent epoch of data used in capability vector derivation |
| **Gini circuit breaker** | Automatic disabling of coherence bonus when wealth concentration exceeds threshold |
| **KACC** | Knowledge Access capability dimension — EMA retrieval quality (Phase 2 extension) |
| **Knowledge Accessor** | DAN role assigned to agent with highest KACC; present in DANs >= 4 |
| **MBND** | Memory Bandwidth capability dimension — consolidation throughput (Phase 2 extension) |
| **Meta-ring** | Hash ring of task type identifiers used to cluster task types when count exceeds DAN_MEMBERSHIP_CAP |
| **RDEP** | Reasoning Depth capability dimension — PCVM credibility for R/H-class claims |
| **Ring ordering** | Deterministic ordering of agents by primary virtual node hash position |
| **Verifier Liaison** | DAN role for VTD preparation/submission; operational only, no verification authority |
| **VLSN** | Verification Liaison capability dimension — diversity-weighted VTD acceptance rate |

---

**End of Master Technical Specification**

**Document ID:** C31-MTS-v1.0
**Status:** SPECIFICATION COMPLETE
**Line count:** ~1,050 lines
**Resolves:** C3 intra-parcel organizational gap; tetrahedral motif heritage restoration
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Agent Organizational Topology\MASTER_TECH_SPEC.md`
