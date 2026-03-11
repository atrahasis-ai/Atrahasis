# C31 Design: Crystallographic Adaptive Topology (CAT)
## Design Council Output

**Invention ID:** C31
**Stage:** DESIGN (Stage 4)
**Date:** 2026-03-11
**Concept:** C31-C — Crystallographic Adaptive Topology (CAT): Deterministic Affinity Neighborhoods (DANs) of 3-5 agents within C3 parcels
**Ideation Verdict:** SELECTED (8-0 unanimous, 6 conditions)
**Research Verdict:** HYBRID CONFIRMED (confidence 4/5)
**Feasibility Verdict:** ADVANCE (10 conditions: 6 Ideation + 4 Feasibility)

---

## Table of Contents

- [1. Executive Summary](#1-executive-summary)
- [2. Architecture Design](#2-architecture-design)
  - [2.1 DAN Formation Algorithm](#21-dan-formation-algorithm)
  - [2.2 Capability Score Derivation](#22-capability-score-derivation)
  - [2.3 Role Assignment Algorithm](#23-role-assignment-algorithm)
  - [2.4 DAN Lifecycle](#24-dan-lifecycle)
  - [2.5 Overlapping DAN Coverage Model](#25-overlapping-dan-coverage-model)
  - [2.6 Crystal Structure Definition](#26-crystal-structure-definition)
  - [2.7 DAN Diversity Monitoring](#27-dan-diversity-monitoring)
  - [2.8 Integration Points](#28-integration-points)
- [3. Communication Design](#3-communication-design)
  - [3.1 Predictive Delta Channel](#31-predictive-delta-channel)
  - [3.2 Stigmergic Decay Channel](#32-stigmergic-decay-channel)
  - [3.3 DAN-Aware Gossip Efficiency](#33-dan-aware-gossip-efficiency)
- [4. Parameter Design](#4-parameter-design)
- [5. Pre-Mortem Analysis](#5-pre-mortem-analysis)
- [6. Simplification Review](#6-simplification-review)
- [7. Heritage Documentation](#7-heritage-documentation)
- [8. Condition Traceability](#8-condition-traceability)
- [Appendix A: DAN Formation Pseudocode](#appendix-a-dan-formation-pseudocode)
- [Appendix B: Capability Score Derivation Pseudocode](#appendix-b-capability-score-derivation-pseudocode)
- [Appendix C: Role Assignment Pseudocode](#appendix-c-role-assignment-pseudocode)
- [Appendix D: Affinity Weight Annealing Pseudocode](#appendix-d-affinity-weight-annealing-pseudocode)

---

## 1. Executive Summary

This document presents the full Design specification for C31 — Crystallographic Adaptive Topology (CAT). CAT introduces Deterministic Affinity Neighborhoods (DANs), small groups of 3-5 agents within C3 parcels, computed deterministically from hash ring adjacency and integer-valued capability profiles derived from PCVM credibility data and tidal history. DANs provide intra-parcel organizational structure: role differentiation (Coordinator, Executor, Verifier Liaison), affinity-weighted predictive models, and an optional coherence settlement bonus. The entire mechanism is optional (DAN_ENABLED=false by default) and degrades gracefully to standard C3 behavior when disabled.

**Design deliverables in this document:**

1. **Architecture Design** (Section 2) — Complete DAN formation algorithm, integer-only capability score derivation, role assignment, lifecycle management, overlapping coverage, crystal structure, diversity monitoring, and integration contracts with C3, C5, C6, C7, and C8.
2. **Communication Design** (Section 3) — How DANs interact with C3's Predictive Delta Channel, Stigmergic Decay Channel, and gossip mechanisms.
3. **Parameter Design** (Section 4) — All 12 tunable parameters with defaults, governance ranges, and rationale.
4. **Pre-Mortem Analysis** (Section 5) — Five failure scenarios with mitigations.
5. **Simplification Review** (Section 6) — Complexity audit with verdict.
6. **Heritage Documentation** (Section 7) — Lineage from Trinity/Tetrahedral/Lattice through CAT.

**Key design decisions:**

- All capability scores are integers in range [0, 1000] (FC-1: no floating-point in DAN computation path).
- Tie-breaking is by agent ID lexicographic comparison (deterministic, manipulation-resistant).
- Capability derivation includes a diversity factor penalizing single-claim-class gaming (FC-2).
- DAN diversity monitoring flags DANs where all members have below-median PCVM credibility (FC-3).
- Implementation deferred to Phase 2; Phase 1 deploys with DAN_ENABLED=false (FC-4).
- DAN_SIZE is a minimum target, not a maximum; a DAN may contain up to 5 agents regardless of safety class.
- DANs are computed per task type per parcel; agents may participate in multiple DANs up to DAN_MEMBERSHIP_CAP.

---

## 2. Architecture Design

### 2.1 DAN Formation Algorithm

The DAN formation algorithm is the core of CAT. It computes, for each active task type within a parcel, a set of non-overlapping DANs that partition the parcel's agents into groups of 3-5. The algorithm is deterministic: given identical inputs, any conformant implementation MUST produce identical DANs.

#### 2.1.1 Inputs

All inputs are shared state available to every agent in the parcel at epoch boundary:

| Input | Source | Update Frequency |
|-------|--------|-----------------|
| `hash_ring[task_type]` | C3 Section 4.1 — bounded-loads consistent hash ring for the task type | Rebuilt at TIDAL_EPOCH boundary |
| `agent_roster` | C3 capacity snapshot — list of all agents in the parcel | Published at TIDAL_EPOCH boundary |
| `safety_class` | Locus governance property — LOW, MEDIUM, HIGH, CRITICAL | Stable across epochs (G-class change only) |
| `epoch_number` | C9 three-tier hierarchy — current TIDAL_EPOCH | Increments every 3,600 seconds |
| `capability_vectors` | CAT capability pipeline (Section 2.2) — integer vectors per agent | Computed at TIDAL_EPOCH boundary |
| `DAN_ENABLED` | Global configuration parameter | Governance-controlled |

#### 2.1.2 DAN Size Determination

DAN size is determined by the locus safety class:

| Safety Class | Base DAN Size | Rationale |
|-------------|:---:|-----------|
| LOW | 3 | Minimum viable group: Coordinator + Executor + Verifier Liaison |
| MEDIUM | 4 | Standard group: Coordinator + 2 Executors + Verifier Liaison |
| HIGH | 4 | Same as MEDIUM (verified task quality more important than group size) |
| CRITICAL | 5 | Maximum group: Coordinator + 2 Executors + Verifier Liaison + Knowledge Accessor |

The base DAN size is a target minimum. The actual DAN size may vary:
- **Minimum:** 3 (below this, no meaningful role differentiation; degenerate DAN is prohibited)
- **Maximum:** 5 (above this, coordination overhead exceeds the small-group benefit per Hackman/Steiner research)
- If the remaining agents in the parcel after forming full DANs number fewer than 3, those agents are absorbed into the last DAN (which may reach size 5).
- A parcel of exactly 5 agents with safety class MEDIUM forms a single DAN of 5 (not a DAN of 4 + 1 orphan).

#### 2.1.3 Algorithm: DAN Partition

The DAN partition algorithm takes the hash ring for a specific task type and partitions the parcel's agents into DANs.

**Step 1: Extract ring ordering.** Sort all agents in the parcel by their primary virtual node position on the hash ring for `task_type`, ascending (clockwise). This produces a deterministic ordered list `ring_order[0..N-1]`.

For agents with multiple virtual nodes, use the virtual node with the lowest hash value as the primary position. This ensures each agent appears exactly once in the ordering.

**Step 2: Compute DAN count.** `dan_count = max(1, floor(N / base_dan_size))` where N is the parcel agent count.

**Step 3: Partition agents into DANs.** Distribute agents from `ring_order` into `dan_count` DANs using a round-robin-then-fill strategy:

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

This produces DANs that differ in size by at most 1. The first `remainder` DANs get one extra agent.

**Step 4: Validate DAN sizes.** If any DAN has fewer than 3 members (possible only when N < 3 * dan_count, which the floor computation in Step 2 prevents), merge it into the adjacent DAN. Post-validation guarantee: every DAN has 3, 4, or 5 members.

**Step 5: Record DAN membership.** For each DAN, record the member list and the anchor agent (the member whose primary virtual node position is closest to position 0 on the ring; deterministic tiebreaker: lowest agent ID).

**Determinism proof:** Step 1 uses SHA256 hash positions (deterministic) with ties broken by agent ID (deterministic). Steps 2-4 use only integer arithmetic on the ordered list. Step 5 uses the same deterministic ordering. The entire computation uses no floating-point, no randomness, and no external state beyond the declared inputs. Two conformant implementations with identical inputs MUST produce identical results.

**Complexity:** O(N log N) for Step 1 (sorting by hash position), O(N) for Steps 2-5. Total: O(N log N) per task type, O(T * N log N) per parcel per epoch. At design targets (N=10, T=20): ~2,000 operations. Negligible.

#### 2.1.4 Multi-Task-Type DAN Computation

The algorithm above runs independently for each active task type in the parcel. Agent A may be in DAN_alpha for task type T1 and DAN_beta for task type T2, with different DAN partners each time (because the hash rings for T1 and T2 produce different orderings).

An agent's total DAN membership count across all task types is bounded by `DAN_MEMBERSHIP_CAP` (default: 5). When a parcel has more than `DAN_MEMBERSHIP_CAP` active task types:

**Task type clustering:** Group task types by hash proximity on a meta-ring (a hash ring whose keys are task type identifiers). Task types within the same meta-ring segment share a single DAN computation. The meta-ring has `DAN_MEMBERSHIP_CAP` segments. This guarantees that no agent participates in more than `DAN_MEMBERSHIP_CAP` distinct DANs.

The meta-ring is constructed identically to C3's task-type hash rings, using SHA256(task_type_id) as the hash function. Segments are divided by `DAN_MEMBERSHIP_CAP` evenly-spaced partition points. Task types hashing to the same segment share one DAN computation (using the combined agent set from all covered task types).

### 2.2 Capability Score Derivation

Capability scores quantify each agent's proficiency across five dimensions. They are derived from PCVM verification history and tidal scheduling history — never self-reported (IC-2). All scores are integers in range [0, 1000] (FC-1).

#### 2.2.1 Five Capability Dimensions

| Dimension | Code | Data Source | Measures |
|-----------|------|-------------|----------|
| Compute Throughput | COMP | C3 tidal history | Task completion rate and efficiency |
| Verification Liaison | VLSN | C5 PCVM VTD history | VTD submission acceptance rate with diversity |
| Knowledge Access | KACC | C6 EMA metrics (Phase 2) | Knowledge retrieval quality and relevance |
| Reasoning Depth | RDEP | C5 PCVM credibility engine | Credibility for R-class and H-class claims |
| Memory Bandwidth | MBND | C6 EMA metrics (Phase 2) | Consolidation throughput and reliability |

**Phase 1 availability:** COMP, VLSN, and RDEP are derivable from data already collected by C3 and C5. KACC and MBND require C6 EMA to expose interaction quality metrics (not currently available). Phase 1 deploys with 3 of 5 dimensions; KACC and MBND default to 500 (midpoint) until C6 metrics are available.

#### 2.2.2 Derivation Functions (Integer-Only)

All intermediate computations use integer arithmetic. Division rounds toward zero. The `normalize_to_1000` function maps a ratio to [0, 1000]:

```
function normalize_to_1000(numerator: uint64, denominator: uint64) -> uint16:
    if denominator == 0: return 500  // default when no data
    return min(1000, (numerator * 1000) / denominator)
```

**COMP — Compute Throughput:**

```
function derive_COMP(
    agent_id: AgentId,
    tidal_history: TidalHistory,
    window: uint32 = 10  // TIDAL_EPOCHs
) -> uint16:
    assigned = tidal_history.tasks_assigned(agent_id, window)
    completed = tidal_history.tasks_completed(agent_id, window)
    return normalize_to_1000(completed, assigned)
```

**VLSN — Verification Liaison (with diversity factor, FC-2):**

```
function derive_VLSN(
    agent_id: AgentId,
    pcvm_history: PCVMHistory,
    window: uint32 = 10
) -> uint16:
    submissions = pcvm_history.vtd_submissions(agent_id, window)
    accepted = pcvm_history.vtd_accepted(agent_id, window)

    // Base acceptance rate [0, 1000]
    acceptance_rate = normalize_to_1000(accepted, submissions)

    // Diversity factor: count of distinct claim classes covered [1..9]
    // 9 canonical classes: D/C/P/R/E/S/K/H/N
    classes_covered = pcvm_history.distinct_claim_classes(agent_id, window)
    // diversity_factor maps [1..9] to [333..1000]
    // Formula: 333 + (667 * (classes_covered - 1)) / 8
    diversity_factor = 333 + (667 * (classes_covered - 1)) / 8

    // Combined score: (acceptance_rate * diversity_factor) / 1000
    return (acceptance_rate * diversity_factor) / 1000
```

The diversity factor (FC-2) ensures that an agent covering only 1 claim class scores at most 333/1000 (33.3%) of its raw acceptance rate. An agent covering all 9 classes retains its full score. This prevents single-class gaming.

**RDEP — Reasoning Depth:**

```
function derive_RDEP(
    agent_id: AgentId,
    pcvm_history: PCVMHistory,
    window: uint32 = 10
) -> uint16:
    // PCVM credibility for R-class and H-class claims
    // Josang opinion tuple: (belief, disbelief, uncertainty, base_rate)
    opinion = pcvm_history.credibility(agent_id, ['R', 'H'])
    // belief is in [0.0, 1.0]; convert to integer [0, 1000]
    // Use fixed-point: belief is stored as uint16 in [0, 1000] by PCVM
    return opinion.belief_fixed_point
```

Note: PCVM credibility scores are already computed and stored by C5. The only requirement is that C5 expose a fixed-point integer representation (belief * 1000, truncated). If C5 currently stores floating-point beliefs, this requires a one-line conversion at the C5 interface boundary. The DAN computation path itself never touches floating-point.

**KACC — Knowledge Access (Phase 2, requires C6 metrics):**

```
function derive_KACC(
    agent_id: AgentId,
    ema_metrics: EMAMetrics,  // Not available in Phase 1
    window: uint32 = 10
) -> uint16:
    if not ema_metrics.available():
        return 500  // Default: midpoint
    retrievals = ema_metrics.retrieval_count(agent_id, window)
    relevant = ema_metrics.retrieval_relevant_count(agent_id, window)
    return normalize_to_1000(relevant, retrievals)
```

**MBND — Memory Bandwidth (Phase 2, requires C6 metrics):**

```
function derive_MBND(
    agent_id: AgentId,
    ema_metrics: EMAMetrics,  // Not available in Phase 1
    window: uint32 = 10
) -> uint16:
    if not ema_metrics.available():
        return 500  // Default: midpoint
    consolidations_attempted = ema_metrics.consolidation_attempts(agent_id, window)
    consolidations_succeeded = ema_metrics.consolidation_successes(agent_id, window)
    return normalize_to_1000(consolidations_succeeded, consolidations_attempted)
```

#### 2.2.3 Capability Vector Assembly

```
function derive_capability_vector(
    agent_id: AgentId,
    tidal_history: TidalHistory,
    pcvm_history: PCVMHistory,
    ema_metrics: Optional[EMAMetrics],
    window: uint32 = CAPABILITY_WINDOW_EPOCHS
) -> CapabilityVector:
    return CapabilityVector(
        COMP = derive_COMP(agent_id, tidal_history, window),
        VLSN = derive_VLSN(agent_id, pcvm_history, window),
        RDEP = derive_RDEP(agent_id, pcvm_history, window),
        KACC = derive_KACC(agent_id, ema_metrics, window),
        MBND = derive_MBND(agent_id, ema_metrics, window)
    )
```

**Publication:** Each agent computes its own capability vector at epoch boundary and includes it in the C3 capacity snapshot. The vector is 5 x 16-bit unsigned integers = 10 bytes per agent. For verification, any agent can independently recompute any other agent's capability vector from the shared PCVM and tidal history — the derivation is deterministic.

**Staleness:** Capability vectors reflect the trailing `CAPABILITY_WINDOW_EPOCHS` (default 10) epochs. New agents (with fewer than 10 epochs of history) receive default scores of 500 on all dimensions. This prevents new agents from being excluded from roles due to zero history.

### 2.3 Role Assignment Algorithm

Once a DAN's members are determined (Section 2.1), roles are assigned based on capability scores. Role assignment is deterministic with integer-only comparisons and agent-ID tiebreaking.

#### 2.3.1 Role Definitions

| Role | Count per DAN | Primary Capability | Description |
|------|:---:|------|-------------|
| Coordinator | 1 | COMP | Highest compute throughput. Serves as DAN anchor for RIF PE routing. Distributes tasks to DAN members. |
| Verifier Liaison | 1 | VLSN | Prepares VTDs for claims produced by DAN members. Formats metadata, assembles evidence, submits to verification membrane. Does NOT evaluate claims or participate in VRF selection. |
| Knowledge Accessor | 0-1 | KACC | Present only in DANs of size >= 4 with KACC data available. Preferred EMA interaction point. Maintains DAN-local artifact cache. |
| Executor | 1+ | (remaining) | Remaining DAN members. Execute tasks assigned by Coordinator. |

**Critical constraint (IC-3, from Feasibility Section 3.2):** The Verifier Liaison role is an operational formatting role, NOT a verification role. The Verifier Liaison:
- DOES prepare and submit VTDs to the verification membrane
- DOES track verification status and relay membrane certificates to the DAN
- Does NOT evaluate claims
- Does NOT participate in VRF committee selection for claims it submits
- Does NOT have knowledge of VRF committee composition
- Has NO influence over verification outcomes

This distinction MUST be preserved in all documentation and implementation. DAN roles and VRF committee membership are fully orthogonal systems.

#### 2.3.2 Assignment Algorithm

```
function assign_roles(dan_members: List[AgentId], capabilities: Map[AgentId, CapabilityVector]) -> Map[AgentId, Role]:
    assignments = {}
    remaining = copy(dan_members)

    // Step 1: Assign Coordinator (highest COMP)
    coordinator = select_best(remaining, capabilities, dimension=COMP)
    assignments[coordinator] = COORDINATOR
    remaining.remove(coordinator)

    // Step 2: Assign Verifier Liaison (highest VLSN among remaining)
    verifier = select_best(remaining, capabilities, dimension=VLSN)
    assignments[verifier] = VERIFIER_LIAISON
    remaining.remove(verifier)

    // Step 3: Assign Knowledge Accessor if DAN size >= 4 and KACC data available
    if len(dan_members) >= 4 and kacc_data_available():
        ka = select_best(remaining, capabilities, dimension=KACC)
        assignments[ka] = KNOWLEDGE_ACCESSOR
        remaining.remove(ka)

    // Step 4: All remaining members are Executors
    for agent in remaining:
        assignments[agent] = EXECUTOR

    return assignments

function select_best(candidates: List[AgentId], capabilities: Map[AgentId, CapabilityVector], dimension: Dimension) -> AgentId:
    // Sort by capability score descending, then by agent_id ascending (tiebreaker)
    // Uses stable sort; agent_id comparison is lexicographic on 256-bit identifiers
    best = candidates[0]
    for agent in candidates[1:]:
        score_agent = capabilities[agent][dimension]
        score_best = capabilities[best][dimension]
        if score_agent > score_best:
            best = agent
        elif score_agent == score_best and agent < best:  // lexicographic agent ID
            best = agent
    return best
```

**Determinism guarantee:** `select_best` compares integer scores and breaks ties by agent ID lexicographic ordering. Agent IDs are 256-bit cryptographic hashes, not agent-chosen, making the tiebreaker manipulation-resistant. The algorithm is O(DAN_SIZE) per role, O(DAN_SIZE * ROLES) = O(DAN_SIZE^2) total, which is O(1) since DAN_SIZE <= 5.

#### 2.3.3 Role Stability

Roles are recomputed at every epoch boundary from current capability vectors and current DAN membership. Roles may change between epochs if:
- An agent's capability scores change (gradual, over CAPABILITY_WINDOW_EPOCHS)
- DAN membership changes (due to parcel reconfiguration or agent churn)
- A new agent with higher scores joins the DAN

Role instability (frequent role switching) is naturally dampened by the 10-epoch sliding window for capability derivation. Scores change slowly, so role assignments are semi-stable.

### 2.4 DAN Lifecycle

#### 2.4.1 Formation

DANs are formed (or reformed) at TIDAL_EPOCH boundaries, synchronized with C3 hash ring reconstruction. The timeline within an epoch boundary:

```
T+0ms:    C3 hash ring reconstruction begins
T+Xms:    Hash rings complete (X varies by parcel size, typically <100ms)
T+Xms:    Capability vectors computed from PCVM/tidal history
T+X+1ms:  DAN partition algorithm runs for each active task type
T+X+2ms:  Role assignment runs for each DAN
T+X+3ms:  Affinity weights updated in predictive models
T+X+4ms:  DAN membership and roles published in capacity snapshot
```

Total DAN computation time at design targets (N=10, T=20): < 5ms. This adds < 5% overhead to the epoch boundary processing.

#### 2.4.2 Steady-State Operation

Between epoch boundaries, DANs are stable. No DAN recomputation occurs mid-epoch. Agents use their DAN membership and role assignments to:
- Route tasks within the DAN via the Coordinator
- Prepare VTDs via the Verifier Liaison
- Access knowledge via the Knowledge Accessor (optimization hint)
- Weight predictive models by DAN affinity (Section 3.1)

#### 2.4.3 Dissolution and Reform on Churn

When an agent departs mid-epoch (crash, voluntary leave, eviction):

1. **Detection:** Remaining DAN members detect absence via C3's existing heartbeat timeout mechanism. No new detection mechanism is needed.
2. **Interim operation:** The DAN operates with DAN_SIZE - 1 members. If the departed agent held a role:
   - Coordinator departs: the DAN member with the next-highest COMP score inherits the Coordinator role for the remainder of the epoch. This is computable locally from the capability vectors already published in the capacity snapshot.
   - Verifier Liaison departs: VTD preparation falls back to any DAN member (or the producing agent itself, which is the current non-DAN behavior).
   - Knowledge Accessor departs: EMA queries are made directly by each agent (current non-DAN behavior).
   - Executor departs: tasks are reassigned via C3's existing `TSK.substitutions` mechanism.
3. **Epoch boundary reform:** At the next epoch boundary, the hash ring is rebuilt (existing C3 mechanism), and DANs are recomputed from the new ring state. The departed agent is absent from the roster; new DANs reflect the current parcel membership.

When an agent joins mid-epoch:

1. The new agent is not added to any DAN until the next epoch boundary (DANs are epoch-stable).
2. The new agent operates without DAN affiliation for the remainder of the epoch, using standard C3 scheduling (uniform predictive weights).
3. At the next epoch boundary, the agent is incorporated into the hash ring and DAN computation.

#### 2.4.4 Parcel Split and Merge

When C3's bi-timescale controller triggers a parcel split or merge:

- **Split:** Two new parcels are formed, each with its own hash rings. DANs are recomputed independently in each new parcel. Former DAN partners may end up in different parcels — their DAN relationship dissolves cleanly.
- **Merge:** A single larger parcel is formed. DANs are recomputed for the combined agent set. New DANs may contain agents from both former parcels.

In both cases, affinity weights enter the annealing phase (Section 3.1) for new DAN partnerships. This is the primary transient cost of reconfiguration, and the primary benefit CAT provides: structured re-learning that prioritizes intra-DAN convergence.

### 2.5 Overlapping DAN Coverage Model

Because DANs are computed per task type, a single agent may belong to different DANs for different task types. This creates an overlapping coverage structure:

```
Agent A4 memberships:
  Task type task.compute:   DAN_alpha (with A2, A7, A9)     Role: EXECUTOR
  Task type task.verify:    DAN_beta  (with A1, A6)          Role: COORDINATOR
  Task type task.knowledge: DAN_gamma (with A3, A5, A8, A0)  Role: KNOWLEDGE_ACCESSOR
```

The overlap creates implicit bonds between DANs — agents that share members can exchange information through those shared members without explicit inter-DAN communication.

**Coverage guarantee:** Every agent in the parcel belongs to at least one DAN for each active task type (guaranteed by the partition algorithm). No agent is unaffiliated unless the parcel has fewer than 3 agents (which violates C3's minimum parcel size of 5, so this cannot occur).

**Membership cap enforcement:** If an agent would belong to more than `DAN_MEMBERSHIP_CAP` DANs (because the parcel has more than `DAN_MEMBERSHIP_CAP` active task types), the task type clustering mechanism (Section 2.1.4) ensures the cap is respected.

### 2.6 Crystal Structure Definition

The crystal structure is the emergent topology formed by DANs and their inter-DAN bonds within a parcel. It is defined for monitoring and analysis purposes; it is not operationally critical.

#### 2.6.1 Definitions

**Node:** A DAN (not an individual agent). Each DAN is a node in the crystal graph.

**Bond:** Two DANs share a bond if and only if they share at least one member agent. The bond weight is the count of shared agents.

**Crystal graph:** G = (V, E) where V = set of all DANs in the parcel, E = set of bonds. This is an undirected weighted graph.

#### 2.6.2 Crystal Classification

| Classification | Condition | Interpretation |
|---------------|-----------|----------------|
| ISOLATED | No bonds (single task type, or disjoint DAN memberships) | DANs operate independently; no inter-DAN information flow |
| SPARSE | Average bond weight < 1.5 | Few shared agents; limited inter-DAN coupling |
| CONNECTED | Crystal graph is connected and average bond weight in [1.5, 3.0] | Normal operating state; information flows through shared members |
| DENSE | Average bond weight > 3.0 or crystal graph is complete | Many shared agents; high inter-DAN coupling (typically T >> DAN count) |

Crystal classification is logged at each epoch boundary for monitoring. Classification changes (e.g., CONNECTED -> SPARSE after agent churn) are noted but do not trigger any automated response. Classification informs human operators about parcel health, not system behavior.

#### 2.6.3 Crystal Metrics (Monitoring Only)

| Metric | Formula | Purpose |
|--------|---------|---------|
| `crystal_density` | `2 * |E| / (|V| * (|V| - 1))` | Graph density; 0 = isolated, 1 = complete |
| `crystal_diameter` | Longest shortest path in G | Information propagation bound |
| `max_agent_centrality` | Max over agents of DAN membership count | Identifies information chokepoints |
| `min_dan_credibility` | Min over DANs of average member credibility | Identifies potentially weak DANs |

These metrics are published in the parcel's epoch summary for operational visibility. They do not affect scheduling, settlement, or any other mechanism.

### 2.7 DAN Diversity Monitoring

Per FC-3, the system monitors DAN composition to detect potentially compromised or weak DANs.

#### 2.7.1 Credibility Floor Check

At each epoch boundary, after DAN computation:

```
function check_dan_diversity(
    dan: DAN,
    capabilities: Map[AgentId, CapabilityVector],
    parcel_median_credibility: uint16
) -> DiversityAlert:
    // Compute average RDEP (reasoning depth / credibility proxy) for DAN members
    dan_avg_rdep = sum(capabilities[m].RDEP for m in dan.members) / len(dan.members)

    if dan_avg_rdep < parcel_median_credibility:
        return DiversityAlert(
            dan_id = dan.id,
            alert_type = BELOW_MEDIAN_CREDIBILITY,
            dan_avg = dan_avg_rdep,
            parcel_median = parcel_median_credibility,
            severity = LOW
        )
    return None
```

The `parcel_median_credibility` is the median RDEP score across all agents in the parcel. DANs where every member is below this median are flagged.

#### 2.7.2 Alert Handling

DAN diversity alerts are:
1. Logged in the parcel's epoch summary
2. Counted in a rolling 10-epoch window
3. If the same DAN triggers alerts for `DAN_DIVERSITY_ALERT_THRESHOLD` (default: 3) consecutive epochs, the alert severity escalates to MEDIUM and is reported to the Locus Decomposer (C7 LD) for potential investigation

DAN diversity alerts do NOT automatically dissolve or restructure DANs. Restructuring is a human/governance decision. The monitoring mechanism provides visibility, not enforcement.

#### 2.7.3 Sybil Clustering Detection

Beyond credibility checks, the monitoring system flags DANs where:
- All members joined the parcel within the same epoch (potential coordinated Sybil entry)
- All members have capability vectors within Euclidean distance < `DAN_SYBIL_DISTANCE_THRESHOLD` (default: 50, meaning all scores differ by less than ~50/1000 on average — suspiciously homogeneous)

These checks are heuristic. False positives are expected (legitimate agents may have similar profiles). The alerts serve as input to human review, not automated enforcement.

### 2.8 Integration Points

#### 2.8.1 C3 Tidal Noosphere Integration

**New section (proposed C3 Section 4.11): Deterministic Affinity Neighborhoods.**

Content: DAN formation algorithm (Section 2.1 of this document), DAN lifecycle (Section 2.4), edge case handling. Purely additive — no existing C3 section is removed or structurally modified.

**Modified section (C3 Section 6.2): Predictive Delta Channel.**

The affinity weight modification replaces uniform prediction weights with DAN-aware weights when DAN_ENABLED=true. See Section 3.1 of this document for full specification.

**New section (proposed C3 Section 4.12): Heritage Documentation.**

Content: Section 7 of this document (Heritage Documentation). Documentation only; no mechanism change.

**New parameters (C3 Appendix B):**

All 12 parameters from Section 4 of this document.

**Hash ring interaction:** DANs are computed AFTER hash rings are constructed. The hash ring construction algorithm (C3 Sections 4.1-4.2) is completely unchanged. DANs are a post-processing layer that reads hash ring state but does not modify it.

**Bi-timescale controller interaction:** The bi-timescale controller operates on SLV (Scope Load Vector) metrics. DANs do not modify SLV computation. Controller split/merge decisions are unaffected. DANs recompute after any controller action.

#### 2.8.2 C5 PCVM Integration

**Isolation guarantee (IC-3):** VRF committee selection (C5 Sections 5.2-5.6) takes as input: VRF seed, agent public keys, diversity attributes, and claim hash. None of these include DAN membership, DAN role, or crystal structure. DAN structure is invisible to VRF selection by construction. No C5 modification is needed.

**Clarification note (proposed C5 Section 11 addition):**

> "The DAN Verifier Liaison role (C31 CAT) is an operational formatting role within the task execution layer. It prepares and submits Verification Trace Documents but does not evaluate claims, does not participate in VRF committee selection for claims it submits, and has no access to committee composition. DAN structure is fully orthogonal to PCVM verification. VRF committee selection MUST NOT incorporate DAN membership or DAN role as inputs."

**Data dependency:** CAT reads from C5 (PCVM credibility scores for capability derivation) but does not write to C5 or modify any C5 mechanism.

#### 2.8.3 C6 EMA Integration

**Optimization note (proposed C6 metabolic interface addition):**

> "When CAT (C31) is enabled, the DAN Knowledge Accessor role serves as the preferred EMA interaction point within each DAN. This is an optimization hint: any agent MAY invoke EMA APIs directly. The Knowledge Accessor maintains a DAN-local artifact cache to reduce redundant queries from DAN members working on related tasks."

**Metrics interface (Phase 2 requirement):** C6 must expose two metrics for full capability vector derivation:
1. `retrieval_relevant_count(agent_id, window)` — count of EMA retrievals rated as relevant by the consuming process
2. `consolidation_successes(agent_id, window)` — count of successful knowledge consolidation operations

These are simple counters on existing EMA operations. Until available, KACC and MBND default to 500.

#### 2.8.4 C7 RIF Integration

**PE extension (proposed C7 Section 10.4 modification):**

When DAN_ENABLED=true and an intent specifies `dan_routing=true`, the Parcel Executor routes the leaf intent to the appropriate DAN member based on role:

| Intent Requirement | DAN Routing Target |
|---|---|
| General compute | Coordinator (who distributes to Executors) |
| VTD preparation | Verifier Liaison |
| Knowledge retrieval | Knowledge Accessor (if present; else any Executor) |
| No specific role | Coordinator |

The PE computes the target DAN deterministically (same algorithm as Section 2.1) and selects the appropriate member. The DAN is NOT a new decomposition tier — it is a routing optimization within the existing PE level. The LD is unaware of DAN structure.

**Backward compatibility:** Intents that do not specify `dan_routing=true` use the current direct-to-agent routing. The `dan_routing` constraint is optional per-intent.

#### 2.8.5 C8 DSF Integration

**DAN Coherence Bonus (optional, disabled by default):**

```
function compute_dan_coherence_bonus(
    agent_id: AgentId,
    dan_membership_history: List[(EpochId, DAN_Id, List[AgentId])],
    base_reward: uint64  // AIC in smallest unit
) -> uint64:
    if not DAN_COHERENCE_BONUS_ENABLED:
        return 0

    // Count consecutive epochs where this agent's DAN had
    // identical membership (same agents, same roles)
    consecutive = 0
    current_epoch_dan = dan_membership_history[latest]
    for epoch in reverse(dan_membership_history):
        if epoch.dan_id == current_epoch_dan.dan_id and
           epoch.members == current_epoch_dan.members:
            consecutive += 1
        else:
            break

    // Linear ramp: 0% at epoch 0, DAN_COHERENCE_BONUS_MAX at RAMP epochs
    // Integer arithmetic: bonus = base * MAX_BPS * min(consecutive, RAMP) / (RAMP * 10000)
    // where MAX_BPS = DAN_COHERENCE_BONUS_MAX in basis points (default 500 = 5%)
    ramp_factor = min(consecutive, DAN_COHERENCE_BONUS_RAMP_EPOCHS)
    bonus = (base_reward * DAN_COHERENCE_BONUS_MAX_BPS * ramp_factor) /
            (DAN_COHERENCE_BONUS_RAMP_EPOCHS * 10000)

    return bonus
```

**Settlement integration:** The bonus is computed by the Settlement Calculator (C8 Component 11) and added to the agent's per-epoch settlement record. The deterministic computation uses DAN membership history, which is derivable from hash ring state at each epoch.

**Governance gate:** DAN_COHERENCE_BONUS_ENABLED can only be set to `true` via G-class governance vote. It cannot be enabled by operational configuration.

**Circuit breaker:** If the Gini coefficient of coherence bonuses across all agents in a locus exceeds `DAN_COHERENCE_GINI_LIMIT` (default: 0.40), the bonus is automatically disabled for the next CONSOLIDATION_CYCLE (36,000 seconds) and a governance alert is raised.

---

## 3. Communication Design

### 3.1 Predictive Delta Channel

C3's Predictive Delta Channel is the primary steady-state communication mechanism. Each agent maintains predictive models of other agents' behavior. When a prediction is correct, no message is sent (zero communication). When a prediction is incorrect, a surprise delta is sent.

#### 3.1.1 Affinity-Weighted Prediction

CAT modifies the prediction weight function. The weight determines how much computational effort an agent invests in maintaining its predictive model of another agent:

```
function prediction_weight(agent_A: AgentId, agent_B: AgentId, task_type: TaskType) -> uint16:
    // Returns weight in [0, 1000] (1000 = full weight, 0 = no prediction)

    if not DAN_ENABLED:
        return 1000  // Uniform weight: exact current C3 behavior

    dan_A = get_dan(agent_A, task_type)
    dan_B = get_dan(agent_B, task_type)

    if dan_A == dan_B:
        // Same DAN for this task type
        return AFFINITY_WEIGHT_INTRA_DAN  // default: 1000

    if share_any_dan(agent_A, agent_B):
        // Different DANs for this task type, but share a DAN for some other task type
        return AFFINITY_WEIGHT_CROSS_DAN_BONDED  // default: 700

    // Same parcel, no shared DAN membership
    return AFFINITY_WEIGHT_CROSS_DAN  // default: 300
```

**Interpretation:** Agents invest full predictive effort in DAN partners (weight 1000), moderate effort in agents bonded through other task types (weight 700), and reduced effort in unaffiliated parcel members (weight 300). Weight 300 (not 0) ensures that predictions are still maintained for all parcel members — DANs prioritize, not partition.

**Effect on communication:** In steady state, prediction accuracy is higher for DAN partners (more effort invested), so fewer surprise deltas are sent within DANs. Inter-DAN surprises are more frequent (less prediction effort) but lower priority. The total communication volume is approximately the same; the distribution is restructured.

**Effect on reconfiguration:** During reconfiguration (parcel split, merge, agent churn), the system must re-learn predictive models. With DANs, intra-DAN re-learning is prioritized (weight 1000), allowing small-group convergence in 1-2 epochs while inter-DAN convergence continues at reduced priority over 3-5 epochs. This is the primary predicted benefit of CAT: structured re-learning that reduces peak transient communication.

#### 3.1.2 Affinity Weight Annealing

When DANs change (at epoch boundary), affinity weights do not jump instantaneously. They anneal over `AFFINITY_RAMP_EPOCHS` (default: 3) to prevent oscillation:

```
function annealed_weight(
    target_weight: uint16,
    previous_weight: uint16,
    epochs_since_change: uint32
) -> uint16:
    if epochs_since_change >= AFFINITY_RAMP_EPOCHS:
        return target_weight  // Ramp complete

    // Linear interpolation using integer arithmetic
    // weight = previous + (target - previous) * epochs / RAMP
    delta = target_weight - previous_weight  // may be negative (use signed)
    return previous_weight + (delta * epochs_since_change) / AFFINITY_RAMP_EPOCHS
```

**Monotonicity constraint:** For newly formed DANs (new intra-DAN partners), `target_weight >= previous_weight`, so the ramp is monotonically increasing. For dissolved DANs (former partners now in different DANs), `target_weight <= previous_weight`, so the ramp is monotonically decreasing. This prevents oscillation — weights never reverse direction during a ramp.

**Interaction with storm detection:** C3's surprise storm detection (Section 4.9 in C3 v2.0) operates on absolute surprise counts per agent per epoch. Affinity weights affect prediction accuracy but not the storm detection threshold. An agent generating excessive surprises triggers storm detection regardless of DAN structure. No modification to storm detection is needed.

### 3.2 Stigmergic Decay Channel

C3's Stigmergic Decay Channel implements signal persistence: signals (task demands, capability advertisements, load metrics) are written to the shared stigmergic field and decay over time unless reinforced. This is C3 Invariant INV-5.

**DAN interaction with stigmergic signals:** DANs do not modify the stigmergic decay mechanism. Signals are parcel-scoped (not DAN-scoped), and their decay rates are unchanged.

However, DAN structure provides routing context for stigmergic signals:

1. **Signal amplification within DANs:** When a DAN member writes a signal (e.g., "high load on task type T"), other DAN members for the same task type are the most likely to benefit from that signal. The affinity-weighted prediction mechanism naturally amplifies this: DAN partners invest more prediction effort, so they detect and respond to DAN-mate signals faster than non-DAN agents.

2. **Cross-DAN signal propagation via bonds:** Crystal bonds (shared members between DANs) serve as natural conduits for signal propagation across DANs. An agent in DAN_alpha and DAN_beta can relay demand signals between the two task types without explicit cross-DAN communication — simply by being in both DANs and having its behavior predicted by members of both.

3. **No new stigmergic mechanism:** CAT does not add DAN-scoped stigmergic fields, DAN-specific decay rates, or DAN-level signal aggregation. The existing parcel-level stigmergic mechanism is sufficient. DAN structure influences signal relevance implicitly through prediction weights, not through new stigmergic infrastructure.

### 3.3 DAN-Aware Gossip Efficiency

C3 uses epidemic gossip for capacity snapshots and epoch synchronization. Currently, gossip targets are selected uniformly at random from the parcel.

**DAN-aware gossip optimization (optional, monitoring-only in Phase 2):**

When DAN_ENABLED=true, gossip propagation can be monitored for DAN-alignment:
- Track whether gossip naturally converges faster within DANs (expected, since DAN members are hash-ring-adjacent and likely to gossip with each other)
- Track whether crystal bonds accelerate cross-DAN gossip convergence
- Measure gossip rounds to full parcel convergence with and without DAN structure

**Design decision: no gossip modification.** CAT does not modify the gossip protocol. The existing uniform random gossip is well-understood and has proven convergence guarantees. DAN-aware gossip targeting (preferring DAN partners) could reduce convergence time but introduces risk of gossip partitioning if DAN structure is poorly connected. The monitoring data from Phase 2 will inform whether DAN-aware gossip is warranted in Phase 3.

---

## 4. Parameter Design

### 4.1 Complete Parameter Table

| # | Parameter | Type | Default | Range | Governance | Rationale |
|---|-----------|------|---------|-------|------------|-----------|
| P-1 | `DAN_ENABLED` | bool | `false` | {true, false} | G-class | Master switch. When false, all DAN computation is skipped and the system behaves identically to C3 without CAT. (IC-1) |
| P-2 | `DAN_SIZE_LOW` | uint8 | 3 | [3, 5] | G-class | Base DAN size for LOW safety class loci. |
| P-3 | `DAN_SIZE_MEDIUM` | uint8 | 4 | [3, 5] | G-class | Base DAN size for MEDIUM safety class loci. |
| P-4 | `DAN_SIZE_HIGH` | uint8 | 4 | [3, 5] | G-class | Base DAN size for HIGH safety class loci. |
| P-5 | `DAN_SIZE_CRITICAL` | uint8 | 5 | [3, 5] | G-class | Base DAN size for CRITICAL safety class loci. |
| P-6 | `DAN_MEMBERSHIP_CAP` | uint8 | 5 | [3, 10] | G-class | Maximum DANs an agent may belong to simultaneously. Controls task type clustering threshold. |
| P-7 | `AFFINITY_WEIGHT_INTRA_DAN` | uint16 | 1000 | [500, 1000] | Operational | Prediction weight for agents in the same DAN for the same task type. |
| P-8 | `AFFINITY_WEIGHT_CROSS_DAN_BONDED` | uint16 | 700 | [300, 1000] | Operational | Prediction weight for agents sharing a DAN bond (same DAN for a different task type). |
| P-9 | `AFFINITY_WEIGHT_CROSS_DAN` | uint16 | 300 | [100, 700] | Operational | Prediction weight for agents in the same parcel with no shared DAN. |
| P-10 | `AFFINITY_RAMP_EPOCHS` | uint8 | 3 | [1, 10] | Operational | Number of epochs for affinity weight annealing after DAN change. |
| P-11 | `CAPABILITY_WINDOW_EPOCHS` | uint8 | 10 | [5, 50] | Operational | Trailing window (in TIDAL_EPOCHs) for capability score derivation. |
| P-12 | `DAN_COHERENCE_BONUS_ENABLED` | bool | `false` | {true, false} | G-class | Enables the DAN coherence settlement bonus. Requires separate G-class vote even when DAN_ENABLED=true. |
| P-13 | `DAN_COHERENCE_BONUS_MAX_BPS` | uint16 | 500 | [100, 500] | G-class | Maximum coherence bonus in basis points (500 = 5% of base reward). (IC-4) |
| P-14 | `DAN_COHERENCE_BONUS_RAMP_EPOCHS` | uint8 | 5 | [3, 20] | G-class | Epochs of DAN stability required for full coherence bonus. |
| P-15 | `DAN_COHERENCE_GINI_LIMIT` | uint16 | 400 | [200, 600] | G-class | Maximum Gini coefficient (x1000) for coherence bonus distribution. Circuit breaker triggers above this. |
| P-16 | `DAN_DIVERSITY_ALERT_THRESHOLD` | uint8 | 3 | [2, 10] | Operational | Consecutive epochs of below-median DAN credibility before escalation to MEDIUM severity. |
| P-17 | `DAN_SYBIL_DISTANCE_THRESHOLD` | uint16 | 50 | [10, 200] | Operational | Euclidean distance threshold for Sybil clustering detection in capability space. |

### 4.2 Parameter Interaction Constraints

1. `AFFINITY_WEIGHT_INTRA_DAN >= AFFINITY_WEIGHT_CROSS_DAN_BONDED >= AFFINITY_WEIGHT_CROSS_DAN` — weights must be monotonically decreasing by affinity distance. If a governance vote sets values violating this constraint, the system uses: intra = max(all three), bonded = median, cross = min(all three).

2. `DAN_COHERENCE_BONUS_ENABLED` requires `DAN_ENABLED=true`. Setting `DAN_COHERENCE_BONUS_ENABLED=true` while `DAN_ENABLED=false` is a no-op (bonus computation is skipped because no DANs exist).

3. `DAN_SIZE_*` parameters must all be >= 3 and <= 5. Values outside [3, 5] are clamped to the nearest boundary.

4. When `DAN_ENABLED` transitions from `false` to `true`, all affinity weights start at 1000 (uniform) and anneal toward their target values over `AFFINITY_RAMP_EPOCHS`. This prevents a sudden discontinuity in prediction behavior.

---

## 5. Pre-Mortem Analysis

Five failure scenarios, each analyzed as if it has already occurred.

### 5.1 Failure: Non-Determinism Bug in DAN Computation

**Scenario:** Two implementations of the DAN formation algorithm produce different DANs for the same inputs. Agent A believes it is in DAN_alpha; Agent B believes A is in DAN_beta. Predictive models diverge. Task routing fails silently. Surprise messages spike.

**Root cause analysis:**
- Floating-point arithmetic in capability score derivation (different IEEE 754 rounding across platforms)
- Unstable sort in hash ring ordering (equal hash positions sorted differently)
- Different interpretations of "primary virtual node" for agents with multiple virtual nodes

**Mitigation:**
- FC-1 mandates integer-only scores. No floating-point enters the DAN computation path.
- Stable sort is mandated; ties broken by agent ID (256-bit, collision probability negligible).
- Primary virtual node is defined as the virtual node with the numerically lowest hash value (unambiguous for distinct SHA256 outputs).
- **Validation requirement:** The Master Tech Spec includes a determinism test suite: 10 canonical inputs with expected outputs. Any implementation must produce byte-identical results for all 10 test cases.

**Severity if unmitigated:** CRITICAL — silent correctness violation across the parcel.
**Severity after mitigation:** NEGLIGIBLE — specification discipline eliminates the root causes.

### 5.2 Failure: Capability Vector Pipeline Produces Stale or Garbage Data

**Scenario:** The PCVM history or tidal history database is corrupted, unavailable, or severely delayed. Capability vectors contain stale data (reflecting agent state from 20+ epochs ago) or default values (500 on all dimensions). Role assignments become meaningless — Coordinator role is assigned to a low-throughput agent because its COMP score is stale-high.

**Root cause analysis:**
- PCVM history database connectivity loss
- Tidal history log rotation deletes data within the CAPABILITY_WINDOW_EPOCHS window
- Clock skew causes the capability derivation pipeline to read the wrong epoch range

**Mitigation:**
- Each capability vector includes a `freshness_epoch` field indicating the most recent epoch of input data. If `freshness_epoch < current_epoch - 2`, the vector is considered stale and replaced with the default (500 on all dimensions).
- When all agents in a DAN have default vectors, role assignment becomes position-based (first agent = Coordinator, second = Verifier Liaison, etc.) — equivalent to C31-B's simpler model. This is deterministic and functional, just not capability-optimized.
- The system logs a MEDIUM-severity alert when more than 50% of agents in a parcel have stale capability vectors.

**Severity if unmitigated:** MEDIUM — misassigned roles reduce DAN effectiveness but do not violate correctness.
**Severity after mitigation:** LOW — graceful degradation to position-based assignment.

### 5.3 Failure: DAN Coherence Bonus Creates Unintended Wealth Concentration

**Scenario:** A small number of agents in stable, high-performing DANs accumulate coherence bonuses over many epochs. Other agents in frequently reconfigured parcels (high-churn loci, rapidly growing task types) never earn coherence bonuses. Over 100+ epochs, the wealth gap becomes significant, creating a two-class system: "established" agents with high cumulative rewards and "migrant" agents with low cumulative rewards.

**Root cause analysis:**
- The 5% cap applies per-epoch, but compounds over time
- Stable DANs correlate with stable, well-resourced loci (rich get richer)
- High-churn loci are also the loci most in need of agent retention (poor get poorer)

**Mitigation:**
- The Gini circuit breaker (P-15, default 0.40) detects wealth concentration and disables the bonus automatically.
- The bonus is disabled by default (P-12) and requires a separate G-class governance vote to enable — governance can choose not to enable it.
- The 5% cap (P-13) limits per-epoch accumulation. Over 100 epochs, the maximum total coherence bonus is 5% * 100 = 500% of a single epoch's base reward. Compared to the 100 * 100% = 10,000% base reward over the same period, the coherence bonus is 5% of total earnings — significant but not dominant.
- **Additional safeguard:** The coherence bonus resets to zero when an agent's parcel is reconfigured (split/merge). This prevents indefinite accumulation and ensures the bonus tracks DAN stability, not agent tenure.

**Severity if unmitigated:** MEDIUM — economic distortion without the circuit breaker.
**Severity after mitigation:** LOW — capped, monitored, and circuit-breaker-protected.

### 5.4 Failure: Crystal Structure Becomes Pathologically Dense

**Scenario:** A parcel with 8 agents and 40 active task types (T >> N) produces 40 DANs per the partition algorithm. Every agent is in every DAN. The crystal is trivially DENSE (complete graph). Affinity weights become meaningless — every agent pair is in the same DAN for multiple task types, so all weights are AFFINITY_WEIGHT_INTRA_DAN (1000). The system effectively has uniform weights, which is the non-DAN behavior. DANs exist but provide no structural benefit.

**Root cause analysis:**
- Task type clustering (Section 2.1.4) should prevent this, but if DAN_MEMBERSHIP_CAP is set too high (e.g., 10) and the parcel has 12 task types, clustering is insufficient
- Small parcels with many task types are a natural degenerate case

**Mitigation:**
- DAN_MEMBERSHIP_CAP (default: 5) limits each agent to 5 DAN memberships. Task types beyond 5 are clustered, reducing the effective DAN count.
- The crystal classification system (Section 2.6) detects DENSE crystals and logs them. If DENSE classification persists for more than 5 consecutive epochs, an operational advisory recommends reducing active task types or increasing parcel size.
- **No corrective action is needed.** A DENSE crystal degrades to uniform-weight behavior, which is the current C3 model. The system does not perform worse than baseline — it simply does not benefit from DAN structure in this configuration.

**Severity if unmitigated:** LOW — performance matches baseline (no degradation, no benefit).
**Severity after mitigation:** NEGLIGIBLE — detected and documented.

### 5.5 Failure: DAN-Aware Routing in RIF PE Causes Task Starvation

**Scenario:** The Parcel Executor routes a task to a DAN's Coordinator via dan_routing=true. The Coordinator is overloaded (already processing maximum concurrent tasks). The Coordinator queues the task. The Coordinator's queue grows unboundedly because tasks keep arriving via DAN routing, but the Coordinator cannot distribute them fast enough. Meanwhile, Executors in the DAN are idle because they receive tasks only through the Coordinator, not directly from the hash ring.

**Root cause analysis:**
- The DAN Coordinator is a routing optimization, not a mandatory funnel
- If the PE treats DAN routing as the only path, the Coordinator becomes a bottleneck
- The original C31-B concept was rejected partly for this coordinator bottleneck problem

**Mitigation:**
- DAN routing is OPTIONAL per-intent (`dan_routing` flag). The PE falls back to direct agent routing when:
  - `dan_routing` is not set (default)
  - The target DAN's Coordinator has exceeded its task queue threshold
  - The task has a deadline that the Coordinator's queue cannot meet
- The Coordinator does not queue tasks — it performs immediate deterministic distribution. The Coordinator inspects the task, determines which Executor has the best capability match, and routes it in the same processing step. There is no Coordinator-side queue.
- If the Coordinator is unreachable, the PE falls back to direct routing (existing C3 behavior). This is the standard graceful degradation: DAN routing fails -> direct routing succeeds.

**Severity if unmitigated:** HIGH — task starvation in the DAN.
**Severity after mitigation:** NEGLIGIBLE — immediate distribution + fallback eliminates the bottleneck.

---

## 6. Simplification Review

*Prepared by the Simplification Agent role. This section reviews the Design for unnecessary complexity.*

### 6.1 Complexity Audit

| Component | Lines (est.) | Necessary? | Verdict |
|-----------|:---:|:-:|:-:|
| DAN formation algorithm | ~120 | YES — core mechanism, deterministic partition | KEEP |
| Capability score derivation (5 dimensions) | ~100 | PARTIAL — 3 of 5 dimensions are derivable in Phase 1; the 2 C6-dependent dimensions add specification weight for deferred functionality | SIMPLIFY: specify 3 dimensions now, reserve 2 as "Phase 2 extensions" with interface stubs |
| Role assignment (4 roles) | ~60 | YES — role differentiation is the primary structural benefit | KEEP |
| DAN lifecycle | ~50 | YES — essential for correctness during churn | KEEP |
| Crystal structure definition | ~60 | MARGINAL — monitoring-only, provides no operational benefit | KEEP with caveat: label as INFORMATIONAL, not NORMATIVE |
| Crystal metrics | ~30 | LOW — four monitoring metrics with no automated response | SIMPLIFY: reduce to 2 metrics (crystal_density, min_dan_credibility); drop crystal_diameter and max_agent_centrality |
| DAN diversity monitoring | ~50 | YES — required by FC-3 | KEEP |
| Sybil clustering detection | ~30 | MARGINAL — heuristic with expected false positives | KEEP with caveat: label as ADVISORY, not NORMATIVE |
| Affinity weight annealing | ~40 | YES — prevents oscillation during transitions | KEEP |
| DAN coherence bonus | ~50 | LOW — disabled by default, requires G-class vote, provides speculative benefit | KEEP as specified but label OPTIONAL EXTENSION |
| Coherence Gini circuit breaker | ~20 | YES (given bonus exists) — prevents wealth concentration | KEEP |
| Task type clustering | ~40 | YES — prevents degenerate T >> N case | KEEP |
| Heritage documentation | ~60 | YES — required by IC-5 | KEEP |

### 6.2 Simplification Recommendations

1. **Reduce crystal metrics from 4 to 2.** `crystal_diameter` and `max_agent_centrality` require graph traversal algorithms that add implementation complexity for pure monitoring value. Retain `crystal_density` (simple formula) and `min_dan_credibility` (simple aggregation). Defer the graph metrics to Phase 3 if monitoring data shows they would be useful.

2. **Defer KACC and MBND capability dimensions.** Specify the derivation formulas (as done in Section 2.2) but mark them as "Phase 2 extension — not computed until C6 exposes required metrics interface." The DAN computation algorithm treats them as constant 500 until activated. This reduces Phase 1 implementation from 5 derivation functions to 3.

3. **Label crystal structure as INFORMATIONAL.** The crystal graph, classification, and remaining metrics are for human operational visibility only. No algorithm, no parameter, and no mechanism depends on crystal classification. Mark the entire Section 2.6 as INFORMATIONAL to prevent implementors from treating it as normative.

4. **Label Sybil clustering detection as ADVISORY.** The heuristic flags are input to human review with expected false positives. Mark as ADVISORY to prevent implementors from building automated responses.

### 6.3 Simplification Verdict

**ACCEPTABLE.** The Design is well-scoped for an optional additive mechanism. The primary complexity (DAN formation + capability derivation + role assignment + affinity weighting) is the minimum viable set for the intended benefit. The secondary complexity (crystal metrics, coherence bonus, Sybil detection) is correctly labeled as optional/monitoring/advisory.

Applying the four simplification recommendations above reduces estimated specification lines from ~710 to ~640 and estimated implementation LOC from ~530 to ~440. These are modest reductions, confirming that the design does not have large pockets of unnecessary complexity.

**One concern:** The 17 parameters (Section 4) are a large parameter surface for an optional mechanism. However, 8 of 17 are disabled-by-default (the coherence bonus family) or informational (the monitoring thresholds). The operationally active parameter count when DAN_ENABLED=true is 9, which is comparable to other AAS subsystems.

**Final verdict: PASS.** The Design is approved without mandatory simplification. The four recommendations above are SUGGESTED, not REQUIRED — the Design Council may accept or reject them.

**Design Council response:** Recommendations 1, 2, 3, and 4 are ACCEPTED. Crystal metrics are reduced to 2. KACC and MBND are marked as Phase 2 extensions. Crystal structure is INFORMATIONAL. Sybil detection is ADVISORY.

---

## 7. Heritage Documentation

### 7.1 Lineage

The Atrahasis agent organizational topology has evolved through five conceptual stages:

| Stage | Model | Era | Key Property |
|-------|-------|-----|-------------|
| 1 | **Trinity (K3)** | Pre-AAS concept | 3 agents: reasoning, verification, coordination. Full-mesh triangle. Minimum viable cooperating unit. |
| 2 | **Tetrahedral Cluster (K4)** | Pre-AAS Noosphere spec | Trinity + memory access node. Complete graph (4 vertices, 6 edges). Built-in verification and knowledge access per cell. Fixed N=4. |
| 3 | **Lattice** | Pre-AAS Noosphere spec | Interconnected tetrahedra sharing coordination nodes. Fractal self-similarity. Small-world network. Static topology. |
| 4 | **Elastic Parcels** | AAS C3 v2.0 | Hash ring-based elastic groups. No intra-parcel structure. Deterministic O(1) scheduling. Minimum 5 agents. Variable size. |
| 5 | **Crystallographic Adaptive Topology (CAT)** | AAS C31 | DANs of 3-5 within elastic parcels. Deterministic formation. Capability-based roles. Affinity-weighted prediction. Optional layer. |

### 7.2 What CAT Preserves from the Tetrahedral Model

| Property | Tetrahedral Model | CAT Realization |
|----------|------------------|-----------------|
| **Small-group structure** | Fixed K4 (4 agents) | Elastic 3-5 agents, safety-class-determined |
| **Role differentiation** | Coordinator, Executor, Verification Liaison, Memory Liaison | Coordinator, Executor(s), Verifier Liaison, Knowledge Accessor |
| **Built-in verification liaison** | Verification node in every cell | Verifier Liaison role in every DAN (formatting only — not evaluation) |
| **Memory/knowledge access** | Memory liaison node in every cell | Knowledge Accessor role (DAN size >= 4) |
| **Fault tolerance through redundancy** | K4 complete graph: every node reaches every other | DAN full-mesh communication within 3-5 agents |
| **Fractal scaling** | Tetrahedra -> Lattice -> Planetary | DAN -> Crystal -> Parcel -> Locus -> Network |

### 7.3 What CAT Improves Over the Tetrahedral Model

| Limitation of Tetrahedral Model | CAT Improvement |
|-------------------------------|-----------------|
| **Fixed N=4** creates remainder problem (13 agents = 3 cells + 1 orphan) | Elastic 3-5 sizing: round-robin-then-fill eliminates orphans |
| **Static lattice** topology requires manual configuration at scale | Deterministic formation from hash ring state: zero configuration |
| **Position-based roles** (role = ring position mod 4) ignore agent capability | Capability-based roles derived from PCVM history |
| **Dedicated memory node** wastes 25% of cell capacity on memory liaison | Knowledge Accessor is an optimization hint, not an exclusive role |
| **Embedded verification** creates verification capture risk | Verifier Liaison is formatting only; verification is via independent VRF committees |
| **Always-on** structure cannot be disabled when not beneficial | Optional by default (DAN_ENABLED=false); zero cost when disabled |

### 7.4 What CAT Drops from the Tetrahedral Model

| Dropped Property | Rationale |
|-----------------|-----------|
| **Static lattice connectivity** (tetrahedra sharing coordination nodes in a fixed graph) | Replaced by dynamic crystal bonds (shared members between task-type DANs). Bonds emerge from overlapping DAN membership, not from pre-wired lattice topology. Dynamic bonds adapt to task type distribution; static lattice cannot. |
| **Dedicated memory node** (1 of 4 agents is exclusively a memory liaison) | AAS C6 EMA provides a formal metabolic interface accessible by any agent. Dedicating 25% of a cell to memory access is wasteful. The Knowledge Accessor role is an optimization hint, not an exclusive assignment. |
| **Self-similar branching ratio** (K3 -> K4 -> lattice with consistent ~4x ratio) | CAT's branching is data-driven: DAN size depends on safety class, DAN count depends on parcel size, crystal density depends on task type count. This is more adaptive but less aesthetically regular. |
| **Tetrahedral motif as identity** (the tetrahedron as the system's visual/conceptual signature) | Acknowledged as historically significant. The DAN of 4 agents in MEDIUM safety class IS a tetrahedron (4 nodes, full-mesh communication). The motif is preserved as a special case, not as the universal form. |

### 7.5 Tetrahedral Motif Acknowledgment

The Atrahasis system's original identity was built around the tetrahedral motif: four cooperating agents forming a complete graph, scaling through lattice repetition. This was a powerful conceptual model that guided early design toward small-group coherence, role complementarity, and fractal scaling.

CAT does not reject the tetrahedral motif. It generalizes it:

- A DAN of 4 in a MEDIUM-safety locus IS a tetrahedral cell (K4).
- A DAN of 3 in a LOW-safety locus IS a trinity (K3).
- A DAN of 5 in a CRITICAL-safety locus extends the tetrahedron to K5.
- The crystal bond structure IS a lattice — but a dynamic, adaptive one rather than a static, pre-wired one.

The tetrahedral motif is the seed from which CAT grew. CAT generalizes the fixed seed into an adaptive growth pattern — preserving the structural insight (small complementary groups are the unit of cooperation) while removing the rigidity (fixed size, static connectivity, always-on) that prevented deployment within the elastic AAS architecture.

The lineage is: Trinity -> Tetrahedron -> Lattice -> DAN -> Crystal -> Parcel -> Locus -> Network.

---

## 8. Condition Traceability

All 10 conditions from Ideation and Feasibility are traced to their realization in this Design:

### 8.1 Ideation Conditions

| # | Condition | Section | Realization |
|---|-----------|---------|-------------|
| IC-1 | Optional by default (DAN_ENABLED=false in Phase 1-2) | 4.1, P-1 | DAN_ENABLED defaults to false. All DAN computation is skipped when false. System behavior is identical to C3 without CAT. |
| IC-2 | Capability vectors from PCVM history, not self-reported | 2.2 | Five-dimensional capability vector derived from C5 PCVM credibility + C3 tidal history. No self-reporting. |
| IC-3 | VRF isolation (DAN structure invisible to VRF committees) | 2.8.2 | VRF selection inputs do not include DAN data. Isolation holds by construction. Verifier Liaison role clarification added. |
| IC-4 | Settlement bonus capped at 5% of base reward | 2.8.5, P-13 | DAN_COHERENCE_BONUS_MAX_BPS = 500 (5%). Range capped at [100, 500]. |
| IC-5 | Heritage documentation tracing intellectual lineage | 7 | Full heritage section: lineage table, preserved/improved/dropped analysis, tetrahedral motif acknowledgment. |
| IC-6 | Empirical validation gate for Phase 3 enablement | 4.1 (P-1 note), 5.2 | DAN_ENABLED requires G-class governance vote. Phase 3 enablement contingent on Phase 2 simulation results showing >20% transient communication reduction. |

### 8.2 Feasibility Conditions

| # | Condition | Section | Realization |
|---|-----------|---------|-------------|
| FC-1 | Integer-only capability scores, stable sort, agent-ID tiebreaker, no floating-point | 2.1, 2.2, 2.3 | All scores uint16 [0, 1000]. normalize_to_1000 uses integer division. Stable sort with agent ID tiebreaker. No floating-point in DAN computation path. |
| FC-2 | Diversity factor in capability derivation | 2.2.2 (VLSN) | VLSN derivation includes diversity_factor penalizing single-claim-class gaming. Factor maps [1..9] classes to [333..1000] multiplier. |
| FC-3 | DAN diversity monitoring for below-median credibility | 2.7 | Credibility floor check at each epoch. Consecutive alerts escalate severity. Sybil clustering detection added as advisory. |
| FC-4 | Implementation deferred to Phase 2 | 1, 4.1 (P-1) | DAN_ENABLED=false by default. Phase 1 deploys without DANs. Specification is complete; implementation begins in Phase 2. |

---

## Appendix A: DAN Formation Pseudocode

```
// Complete DAN formation for one task type in one parcel
// All operations are deterministic; no randomness, no floating-point

function form_dans(
    parcel_id: ParcelId,
    task_type: TaskType,
    agent_roster: List[AgentId],      // All agents in the parcel
    hash_ring: HashRing,              // Bounded-loads consistent hash ring for task_type
    safety_class: SafetyClass,        // LOW | MEDIUM | HIGH | CRITICAL
    capabilities: Map[AgentId, CapabilityVector]
) -> List[DAN]:

    if not DAN_ENABLED:
        return []   // No DANs when disabled

    N = len(agent_roster)
    if N < 3:
        return []   // Cannot form a DAN with fewer than 3 agents

    // Step 1: Determine base DAN size from safety class
    base_size = match safety_class:
        LOW:      DAN_SIZE_LOW       // default 3
        MEDIUM:   DAN_SIZE_MEDIUM    // default 4
        HIGH:     DAN_SIZE_HIGH      // default 4
        CRITICAL: DAN_SIZE_CRITICAL  // default 5

    // Step 2: Extract ring ordering
    // For each agent, find their primary virtual node (lowest hash value)
    // Sort agents by primary virtual node position, ascending
    ring_order = sort(agent_roster, key = lambda a: min_vnode_hash(hash_ring, a))
    // Tiebreaker: if two agents have identical min_vnode_hash (negligible probability
    // with SHA256), sort by agent_id ascending
    ring_order = stable_sort(ring_order, key = lambda a: (min_vnode_hash(hash_ring, a), a))

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
            // Merge with previous DAN (should not occur with correct dan_count)
            dans[len(dans) - 1].members.extend(members)
            continue

        // Step 5: Assign roles
        roles = assign_roles(members, capabilities)

        // Step 6: Determine anchor (member with lowest primary vnode hash;
        //         tiebreak by lowest agent_id)
        anchor = members[0]   // Already sorted by vnode hash

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

## Appendix B: Capability Score Derivation Pseudocode

```
// Complete capability vector derivation for one agent
// All arithmetic is integer-only; no floating-point

function derive_capability_vector(
    agent_id: AgentId,
    tidal_history: TidalHistory,
    pcvm_history: PCVMHistory,
    ema_metrics: Optional[EMAMetrics],
    window: uint32 = CAPABILITY_WINDOW_EPOCHS   // default 10
) -> CapabilityVector:

    // --- COMP: Compute Throughput ---
    assigned = tidal_history.tasks_assigned(agent_id, window)
    completed = tidal_history.tasks_completed(agent_id, window)
    COMP = normalize_to_1000(completed, assigned)

    // --- VLSN: Verification Liaison (with diversity factor) ---
    submissions = pcvm_history.vtd_submissions(agent_id, window)
    accepted = pcvm_history.vtd_accepted(agent_id, window)
    acceptance_rate = normalize_to_1000(accepted, submissions)

    classes_covered = pcvm_history.distinct_claim_classes(agent_id, window)
    // classes_covered in [0, 9]; if 0, treat as 1 (minimum)
    classes_covered = max(1, classes_covered)
    diversity_factor = 333 + (667 * (classes_covered - 1)) / 8
    VLSN = (acceptance_rate * diversity_factor) / 1000

    // --- RDEP: Reasoning Depth ---
    // PCVM stores belief as fixed-point uint16 in [0, 1000]
    opinion = pcvm_history.credibility(agent_id, claim_classes=['R', 'H'])
    RDEP = opinion.belief_fixed_point   // Already uint16 [0, 1000]

    // --- KACC: Knowledge Access (Phase 2) ---
    if ema_metrics is not None and ema_metrics.available():
        retrievals = ema_metrics.retrieval_count(agent_id, window)
        relevant = ema_metrics.retrieval_relevant_count(agent_id, window)
        KACC = normalize_to_1000(relevant, retrievals)
    else:
        KACC = 500   // Default midpoint

    // --- MBND: Memory Bandwidth (Phase 2) ---
    if ema_metrics is not None and ema_metrics.available():
        attempts = ema_metrics.consolidation_attempts(agent_id, window)
        successes = ema_metrics.consolidation_successes(agent_id, window)
        MBND = normalize_to_1000(successes, attempts)
    else:
        MBND = 500   // Default midpoint

    // --- Freshness check ---
    freshness = tidal_history.most_recent_epoch(agent_id)
    if current_epoch() - freshness > 2:
        // Stale data: return default vector
        return CapabilityVector(500, 500, 500, 500, 500, freshness_epoch=freshness)

    return CapabilityVector(COMP, VLSN, RDEP, KACC, MBND, freshness_epoch=freshness)


function normalize_to_1000(numerator: uint64, denominator: uint64) -> uint16:
    if denominator == 0:
        return 500   // No data: midpoint default
    result = (numerator * 1000) / denominator   // Integer division
    return min(1000, result)
```

---

## Appendix C: Role Assignment Pseudocode

```
// Complete role assignment for one DAN
// Deterministic: integer comparisons + agent-ID tiebreaker

function assign_roles(
    members: List[AgentId],
    capabilities: Map[AgentId, CapabilityVector]
) -> Map[AgentId, Role]:

    assignments = {}
    remaining = list(members)   // Copy

    // 1. Coordinator: highest COMP score
    coord = select_best(remaining, capabilities, COMP)
    assignments[coord] = COORDINATOR
    remaining.remove(coord)

    // 2. Verifier Liaison: highest VLSN score among remaining
    vl = select_best(remaining, capabilities, VLSN)
    assignments[vl] = VERIFIER_LIAISON
    remaining.remove(vl)

    // 3. Knowledge Accessor: highest KACC among remaining, if DAN >= 4 and KACC available
    if len(members) >= 4 and kacc_available():
        ka = select_best(remaining, capabilities, KACC)
        assignments[ka] = KNOWLEDGE_ACCESSOR
        remaining.remove(ka)

    // 4. All remaining are Executors
    for agent in remaining:
        assignments[agent] = EXECUTOR

    return assignments


function select_best(
    candidates: List[AgentId],
    capabilities: Map[AgentId, CapabilityVector],
    dimension: Dimension
) -> AgentId:
    // Find candidate with highest score on dimension
    // Tiebreaker: lowest agent_id (lexicographic on 256-bit identifier)

    best = candidates[0]
    best_score = capabilities[best][dimension]

    for agent in candidates[1:]:
        score = capabilities[agent][dimension]
        if score > best_score:
            best = agent
            best_score = score
        elif score == best_score and agent < best:
            best = agent
            // best_score unchanged (tied)

    return best


function kacc_available() -> bool:
    // Returns true if C6 EMA metrics interface is available
    // Phase 1: returns false
    // Phase 2+: returns true if EMA exposes retrieval_relevant_count
    return ema_metrics_interface_enabled()
```

---

## Appendix D: Affinity Weight Annealing Pseudocode

```
// Affinity weight calculation with annealing
// Prevents discontinuities when DANs change at epoch boundaries

function compute_affinity_weight(
    agent_A: AgentId,
    agent_B: AgentId,
    task_type: TaskType,
    dan_index: DANIndex,              // Current epoch's DAN memberships
    previous_weight: uint16,          // Last epoch's weight for this pair
    epochs_since_dan_change: uint32   // Epochs since A and B's DAN relationship changed
) -> uint16:

    if not DAN_ENABLED:
        return 1000   // Uniform: exact C3 behavior

    // Determine target weight
    dan_A = dan_index.get_dan(agent_A, task_type)
    dan_B = dan_index.get_dan(agent_B, task_type)

    if dan_A is not None and dan_A == dan_B:
        target = AFFINITY_WEIGHT_INTRA_DAN          // default 1000
    elif dan_index.share_any_dan(agent_A, agent_B):
        target = AFFINITY_WEIGHT_CROSS_DAN_BONDED   // default 700
    else:
        target = AFFINITY_WEIGHT_CROSS_DAN           // default 300

    // Apply annealing
    if epochs_since_dan_change >= AFFINITY_RAMP_EPOCHS:
        return target   // Ramp complete

    // Linear interpolation (integer arithmetic)
    // delta may be negative (weight decreasing for dissolved DAN partnerships)
    delta = (target as int32) - (previous_weight as int32)
    annealed = previous_weight + (delta * epochs_since_dan_change) / AFFINITY_RAMP_EPOCHS
    return clamp(annealed, 0, 1000) as uint16


// On DAN_ENABLED transition from false to true:
// All previous_weight values are initialized to 1000 (uniform)
// epochs_since_dan_change is set to 0 for all pairs
// Weights anneal from 1000 toward their DAN-determined targets
```

---

*Design prepared by the Design Council for C31 — Crystallographic Adaptive Topology (CAT).*
*Design date: 2026-03-11*
*Conditions honored: 10 of 10 (6 Ideation + 4 Feasibility)*
*Simplification review: PASS (4 recommendations accepted)*
*Heritage documentation: Complete (Trinity -> Tetrahedron -> Lattice -> DAN -> Crystal lineage)*
*Next stage: SPECIFICATION (Stage 5) — produce Master Tech Spec addendum*
