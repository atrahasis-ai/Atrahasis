# C31 Feasibility Assessment: Crystallographic Adaptive Topology (CAT)
## Feasibility Council Report

**Invention ID:** C31
**Stage:** FEASIBILITY (Stage 3)
**Date:** 2026-03-11
**Concept Under Review:** C31-C — Crystallographic Adaptive Topology (CAT): Deterministic Affinity Neighborhoods (DANs) of 3-5 agents within C3 parcels
**Ideation Verdict:** SELECTED (8-0 unanimous, with 6 conditions)
**Research Verdict:** HYBRID CONFIRMED (confidence 4/5, cross-domain convergence)

---

## Table of Contents

- [1. Executive Summary](#1-executive-summary)
- [2. Technical Feasibility](#2-technical-feasibility)
  - [2.1 Deterministic DAN Computation](#21-deterministic-dan-computation)
  - [2.2 C3 Invariant Compliance](#22-c3-invariant-compliance)
  - [2.3 Overhead Analysis](#23-overhead-analysis)
  - [2.4 Edge Cases and Degeneracies](#24-edge-cases-and-degeneracies)
  - [2.5 Capability Vector Derivation Pipeline](#25-capability-vector-derivation-pipeline)
  - [2.6 Technical Feasibility Verdict](#26-technical-feasibility-verdict)
- [3. Integration Feasibility](#3-integration-feasibility)
  - [3.1 C3 Tidal Noosphere Integration](#31-c3-tidal-noosphere-integration)
  - [3.2 C5 PCVM Integration: DANs vs. VRF Committees](#32-c5-pcvm-integration-dans-vs-vrf-committees)
  - [3.3 C7 RIF Integration: Parcel Executor Extension](#33-c7-rif-integration-parcel-executor-extension)
  - [3.4 C8 DSF Integration: DAN Coherence Bonus](#34-c8-dsf-integration-dan-coherence-bonus)
  - [3.5 C6 EMA Integration](#35-c6-ema-integration)
  - [3.6 C9 Cross-Layer Constraints](#36-c9-cross-layer-constraints)
  - [3.7 Integration Feasibility Verdict](#37-integration-feasibility-verdict)
- [4. Adversarial Analysis (Counter-Report)](#4-adversarial-analysis-counter-report)
  - [4.1 Attack Vector: Hash Ring Position Manipulation](#41-attack-vector-hash-ring-position-manipulation)
  - [4.2 Attack Vector: Capability Vector Gaming](#42-attack-vector-capability-vector-gaming)
  - [4.3 Attack Vector: DAN Role Information Leakage](#43-attack-vector-dan-role-information-leakage)
  - [4.4 Attack Vector: DAN Composition Steering](#44-attack-vector-dan-composition-steering)
  - [4.5 Attack Vector: Crystal Structure Reconnaissance](#45-attack-vector-crystal-structure-reconnaissance)
  - [4.6 Attack Vector: Coherence Bonus Exploitation](#46-attack-vector-coherence-bonus-exploitation)
  - [4.7 Attack Vector: Affinity Weight Manipulation](#47-attack-vector-affinity-weight-manipulation)
  - [4.8 Adversarial Analysis Summary](#48-adversarial-analysis-summary)
- [5. Complexity Assessment](#5-complexity-assessment)
  - [5.1 Specification Complexity](#51-specification-complexity)
  - [5.2 Implementation Complexity](#52-implementation-complexity)
  - [5.3 Cognitive Complexity](#53-cognitive-complexity)
  - [5.4 Testing Complexity](#54-testing-complexity)
  - [5.5 Complexity Budget Analysis](#55-complexity-budget-analysis)
- [6. Risk Assessment](#6-risk-assessment)
  - [6.1 Risk Register](#61-risk-register)
  - [6.2 Scoring](#62-scoring)
- [7. Verdict](#7-verdict)
  - [7.1 Decision](#71-decision)
  - [7.2 Conditions for Advancement](#72-conditions-for-advancement)
  - [7.3 Specification Directives](#73-specification-directives)
- [Appendix A: DAN Computation Walkthrough](#appendix-a-dan-computation-walkthrough)
- [Appendix B: Overhead Budget Calculation](#appendix-b-overhead-budget-calculation)
- [Appendix C: Attack Tree Summary](#appendix-c-attack-tree-summary)

---

## 1. Executive Summary

The Feasibility Council has assessed C31-C (Crystallographic Adaptive Topology / CAT) across five dimensions: technical feasibility, integration feasibility, adversarial resistance, complexity cost, and overall risk.

**Findings:**

1. **Technical feasibility is CONFIRMED.** DAN computation is deterministic, O(N) per epoch per task type, and preserves all seven C3 invariants. The algorithm uses only operations already present in the C3 stack (hash ring lookup, clockwise traversal, deterministic sorting). The capability vector derivation from PCVM history is feasible but requires a new pipeline that does not currently exist.

2. **Integration feasibility is CONFIRMED with one critical constraint.** CAT integrates cleanly with C3 (additive section), C6 (clarification), C7 (PE extension), and C8 (optional parameter). The critical constraint is C5 PCVM isolation: DAN structure MUST be invisible to VRF committee selection. This is achievable because VRF selection already operates on locus-scope agent pools, not parcel-internal structure. DANs and VRF committees serve fundamentally different purposes (task execution vs. claim verification) and operate at different scopes (intra-parcel vs. locus-wide).

3. **Adversarial resistance is ADEQUATE.** Seven attack vectors were analyzed. Three have negligible risk (position manipulation, crystal reconnaissance, affinity weight manipulation). Two have LOW risk with existing mitigations (capability gaming via PCVM derivation, coherence bonus exploitation via 5% cap). Two have MEDIUM risk requiring specification-time mitigation (DAN composition steering via Sybil agents, role information leakage to colluders). No attack vector reaches HIGH severity.

4. **Complexity cost is MODERATE and bounded.** CAT adds approximately 350-400 specification lines across 5 specs, one new algorithm (DAN computation), one coefficient change (affinity weighting), and one optional settlement parameter. The optional-by-default design means implementations that do not enable DANs bear zero additional runtime complexity. The primary complexity cost is cognitive — engineers must understand the DAN/crystal model even if they disable it.

5. **Overall risk is MEDIUM (5/10).** The design is sound, the integration is clean, and the adversarial surface is manageable. The primary risks are: (a) unproven behavior at scale (no simulation data), (b) capability vector pipeline is new unspecified infrastructure, and (c) the benefit (transient communication reduction) is speculative until empirically validated.

**Verdict: ADVANCE to DESIGN (Stage 4)** with conditions.

---

## 2. Technical Feasibility

### 2.1 Deterministic DAN Computation

The DAN computation algorithm proposed in C31 Ideation has the following properties that make it technically feasible:

**Inputs (all shared state):**
- Hash ring for the task type (deterministic per C3 Section 4.1)
- Agent roster for the parcel (broadcast at epoch boundaries via capacity snapshot)
- Safety class of the locus (stable across epochs, governance-controlled)
- Epoch number (shared global clock per C9 three-tier hierarchy)
- Agent capability vectors (derived from PCVM history, published at epoch boundaries)

**Algorithm steps and determinism analysis:**

| Step | Operation | Deterministic? | Justification |
|------|-----------|:-:|---------------|
| 1. Find primary assignee | Hash ring lookup | Yes | SHA256 is deterministic; bounded-loads lookup is deterministic given same ring state and same load counters |
| 2. Determine DAN size | Match on safety class | Yes | Safety class is a locus property, identical for all agents in the parcel |
| 3. Select candidates | Clockwise ring traversal | Yes | Ring ordering is deterministic from construction |
| 4. Capability-aware filtering | Greedy coverage maximization | Yes | Requires deterministic tie-breaking (see below) |
| 5. Role assignment | Capability score ranking | Yes | Requires deterministic tie-breaking (see below) |

**Critical requirement: deterministic tie-breaking.** Steps 4 and 5 involve maximization operations where ties are possible. Two agents may have identical capability scores for the same role. The algorithm MUST specify a deterministic tie-breaking rule. We recommend: break ties by agent ID (lexicographic comparison of 256-bit identifiers). This is a stable, deterministic, manipulation-resistant tiebreaker because agent IDs are cryptographic hashes, not agent-chosen.

**Theorem verification (DAN determinism):** The proof sketch from Ideation is valid. All inputs are shared state. All operations are deterministic. The only gap is the tie-breaking rule, which is a specification detail, not a feasibility blocker. With the agent-ID tiebreaker added, the algorithm is fully deterministic. Two conformant implementations with identical inputs MUST produce identical DAN structures.

**Computational complexity:**

For a parcel with N agents and T active task types:
- Per task type: O(N) to build the ring (already done by C3), O(DAN_SIZE * 2) = O(1) for candidate selection, O(DAN_SIZE^2) = O(1) for role assignment
- Total per epoch: O(T) DAN computations, each O(1) after ring construction
- Since ring construction is O(N * V) where V is virtual nodes per agent (already paid by C3), the marginal cost of DAN computation is O(T) per epoch per parcel

At the design target (10,000 agents, ~1,000 parcels of ~10 agents each, ~20 task types per parcel):
- DAN computations per epoch: 1,000 parcels * 20 task types = 20,000
- Each computation: ~10 operations (2*DAN_SIZE candidate lookups + role assignments)
- Total: ~200,000 operations per epoch (every 3,600 seconds)
- This is negligible — approximately 56 operations per second system-wide

### 2.2 C3 Invariant Compliance

CAT must preserve all seven C3 invariants or fail feasibility. Analysis:

| Invariant | Description | CAT Compliance | Analysis |
|-----------|-------------|:-:|----------|
| INV-1 | Verification membrane is constitutionally protected | PASS | DANs do not touch the verification membrane. The VERIFY_LIAISON role is an operational formatting role, not a verification role. VRF committee selection is isolated from DAN structure. |
| INV-2 | Determinism: identical inputs produce identical outputs | PASS | DAN computation is deterministic (Section 2.1). Affinity weighting is a deterministic coefficient applied to predictive models. All DAN-related state is derived from shared inputs. |
| INV-3 | Only I-confluence-proven operations execute coordination-free | PASS | DANs do not modify the operation-class algebra. M/B/X/V/G classification is unchanged. DAN-internal task distribution follows the same class rules. |
| INV-4 | Parcels are correctness boundaries | PASS | DANs exist entirely within parcels. DAN membership never crosses parcel boundaries. Cross-parcel operations still require X-class Fusion Capsules. |
| INV-5 | Signals decay unless reinforced | PASS | DANs do not modify the stigmergic decay channel. Affinity weighting affects intra-parcel predictive delta only. |
| INV-6 | Graceful degradation | PASS | When DANs are disabled (DAN_ENABLED = false or all affinity weights = 1.0), the system reverts to the current C3 model. DAN failure (e.g., capability vector pipeline unavailable) degrades to uniform-weight prediction, which is the current behavior. |
| INV-7 | Tidal function is itself a verified claim | PASS | DANs are derived from the tidal function outputs (hash ring assignments). The tidal function itself is unchanged. DAN computation is a post-processing layer on top of tidal scheduling, not a modification to it. |

**Verdict: All seven invariants preserved.** CAT is a strict superset of C3's current behavior — it can only add, never subtract.

### 2.3 Overhead Analysis

**Computational overhead (per epoch boundary):**

| Component | Current C3 | With CAT | Delta |
|-----------|-----------|----------|-------|
| Hash ring construction | O(N * V * T) per parcel | O(N * V * T) per parcel | 0 (unchanged) |
| Task assignment | O(1) per task | O(1) per task | 0 (unchanged) |
| DAN computation | 0 | O(T) per parcel | +O(T) per parcel |
| Predictive model maintenance | O(N) models per agent | O(N) models per agent (different weights) | 0 (coefficient change only) |
| Capacity snapshot | O(N) per parcel | O(N) per parcel + capability vectors | +O(N * C) where C = capability dimensions |

The dominant new cost is publishing capability vectors in the capacity snapshot. If each agent has C=5 capability dimensions (COMPUTE, VERIFY_LIAISON, KNOWLEDGE_ACCESS, MEMORY_BANDWIDTH, REASONING_DEPTH), each represented as a 32-bit float, the per-agent overhead is 20 bytes. For a parcel of 10 agents, this is 200 bytes per epoch — negligible relative to the capacity snapshot's existing content.

**Communication overhead (steady state):**

| Component | Current C3 | With CAT | Delta |
|-----------|-----------|----------|-------|
| Intra-parcel predictive delta | O(1) per agent (zero when predictions correct) | O(1) per agent (zero when predictions correct) | 0 — affinity weights change prediction ACCURACY, not message count |
| Inter-DAN communication | N/A | 0 (no new channel) | 0 |
| DAN lifecycle signals | N/A | 0 (DANs are computed, not signaled) | 0 |

**Communication overhead (transient — reconfiguration):**

This is where CAT is predicted to provide benefit. During parcel reconfiguration:

| Component | Current C3 | With CAT (predicted) |
|-----------|-----------|---------------------|
| Predictive model re-learning | All N*(N-1) models re-learn simultaneously | High-priority: intra-DAN models (DAN_SIZE * (DAN_SIZE-1) per DAN). Low-priority: inter-DAN models (lazy re-learning) |
| Communication burst duration | 3-5 epochs for full convergence | 1-2 epochs for intra-DAN convergence; 3-5 epochs for inter-DAN convergence |
| Peak message rate | O(N^2) surprise messages | O(DAN_SIZE^2) surprise messages per DAN + O(1) inter-DAN |

**Expected transient communication reduction:** For a parcel of 12 agents reconfiguring:
- Current: 132 model pairs re-learning simultaneously
- With CAT: 3 DANs of 4 agents = 36 high-priority model pairs + 96 low-priority pairs (deferred)
- Peak burst reduction: approximately 70% (36 vs. 132 simultaneous high-priority re-learning events)

This estimate is speculative and MUST be validated empirically (Ideation Condition 6).

### 2.4 Edge Cases and Degeneracies

**Edge case 1: Minimum parcel (5 agents).**
- With safety class LOW: 1 DAN of 3 + 1 DAN of 2 (degenerate) OR 1 DAN of 3 + 2 unaffiliated agents
- Recommended: minimum DAN size is 3. A parcel of 5 with safety LOW forms 1 DAN of 3 covering the primary task type; remaining 2 agents participate in DANs for secondary task types only. If only 1 task type exists, a single DAN of 5 forms (safety class override: LOW permits DAN_SIZE=3 but does not prohibit larger).
- **Resolution: specify that DAN_SIZE is a minimum, not a maximum.** A DAN of 5 in a parcel of 5 is acceptable.

**Edge case 2: Parcel with 1 task type.**
- All agents are on the same hash ring. DAN computation produces ceil(N / base_size) DANs with no overlapping agents (since there is only one ring to draw from).
- Crystal structure is trivially SPARSE (no bonds between DANs because there is only one task type per DAN).
- This degeneracy is harmless — the DAN provides role differentiation and affinity weighting within the group, even without cross-DAN bonds.

**Edge case 3: Parcel with more task types than agents (T >> N).**
- Every agent participates in T DANs (one per task type). This is the DENSE crystal.
- Maximum DAN membership per agent: T. If T=50 and N=10, each agent is in ~50 DANs.
- Ideation specified a cap of 5 DANs per agent, with excess task types sharing DANs. This cap needs careful specification: which task types share DANs? Proposed: group task types by hash proximity on a meta-ring, forming "task type clusters" that share a single DAN.
- **Resolution: specify DAN_MEMBERSHIP_CAP (default 5) and task-type clustering algorithm for overflow.**

**Edge case 4: All agents have identical capability vectors.**
- Role assignment by capability score produces ties for every role.
- Tie-breaking by agent ID ensures deterministic assignment, but role assignment becomes effectively random (determined by cryptographic ID, not by capability).
- This is the correct behavior: when agents are homogeneous, role assignment is arbitrary. The system degrades gracefully to position-based assignment (similar to C31-B, but without its other drawbacks).

**Edge case 5: Agent churn during an epoch.**
- An agent joins or leaves mid-epoch. The hash ring is not rebuilt until the next epoch boundary. DANs are also not recomputed until the next epoch boundary.
- During the interim: the departed agent's DAN partners detect absence via heartbeat timeout (existing C3 mechanism). Tasks are reassigned via the TSK.substitutions list (existing C3 mechanism). The DAN is "incomplete" until epoch boundary, operating with DAN_SIZE - 1 members.
- **Resolution: no new mechanism needed.** Existing C3 churn handling covers this case. DANs recompute at epoch boundary along with hash rings.

### 2.5 Capability Vector Derivation Pipeline

The Ideation Council mandated (Condition 2) that capability vectors MUST be derived from PCVM verification history, not self-reported. This requires a new pipeline:

**Inputs (from existing systems):**
- C5 PCVM credibility engine: maintains per-agent credibility scores (Josang opinion tuples) across claim classes
- C5 verification history: records of claims produced, verification outcomes, deep audit results
- C3 tidal scheduler: records of tasks completed, latency, resource consumption

**Derivation algorithm (proposed):**

```
function derive_capability_vector(
    agent_id: AgentId,
    pcvm_history: PCVMHistory,
    tidal_history: TidalHistory,
    window: uint32 = 10  // TIDAL_EPOCHs
) -> CapabilityVector:

    # COMPUTE: normalized throughput of completed tasks
    compute_score = tidal_history.tasks_completed(agent_id, window) /
                    tidal_history.tasks_assigned(agent_id, window)

    # VERIFY_LIAISON: success rate of VTD submissions (not verification itself)
    vtd_submissions = pcvm_history.vtd_submissions(agent_id, window)
    vtd_accepted = pcvm_history.vtd_accepted(agent_id, window)
    verify_liaison_score = vtd_accepted / max(1, vtd_submissions)

    # KNOWLEDGE_ACCESS: frequency and quality of EMA interactions
    # (requires C6 EMA to expose interaction metrics)
    knowledge_score = ema_history.retrieval_quality(agent_id, window)

    # REASONING_DEPTH: credibility score for R-class and H-class claims
    reasoning_score = pcvm_history.credibility(agent_id, ['R', 'H']).belief

    # MEMORY_BANDWIDTH: throughput of knowledge consolidation operations
    memory_score = ema_history.consolidation_throughput(agent_id, window)

    return CapabilityVector(
        compute = normalize(compute_score),
        verify_liaison = normalize(verify_liaison_score),
        knowledge_access = normalize(knowledge_score),
        reasoning_depth = normalize(reasoning_score),
        memory_bandwidth = normalize(memory_score)
    )
```

**Feasibility assessment of the pipeline:**
- COMPUTE and VERIFY_LIAISON scores can be derived from data already collected by C3 and C5. No new instrumentation needed.
- KNOWLEDGE_ACCESS and MEMORY_BANDWIDTH require C6 EMA to expose interaction quality metrics. C6 does not currently expose these. This is a minor C6 enhancement (adding metrics counters to existing operations).
- REASONING_DEPTH uses PCVM credibility scores that already exist per-agent.
- The pipeline runs once per epoch at epoch boundary, producing a 5-dimensional float vector per agent. Cost: O(1) per agent per epoch (aggregating pre-computed metrics).

**Gap: C6 EMA metrics.** The KNOWLEDGE_ACCESS and MEMORY_BANDWIDTH dimensions require C6 to instrument its metabolic interface. This is not a feasibility blocker — the pipeline can launch with 3 dimensions (COMPUTE, VERIFY_LIAISON, REASONING_DEPTH) and add the C6 dimensions when available. Partial capability vectors still enable meaningful role assignment.

### 2.6 Technical Feasibility Verdict

**FEASIBLE.** The DAN computation is deterministic, O(T) marginal cost per epoch, preserves all C3 invariants, handles all identified edge cases, and the capability pipeline is constructible from existing data. Two gaps remain:
1. Tie-breaking rule must be specified (trivial: agent ID lexicographic comparison)
2. C6 EMA metrics interface needed for 2 of 5 capability dimensions (deferrable)

---

## 3. Integration Feasibility

### 3.1 C3 Tidal Noosphere Integration

**Changes required:**

| Section | Change Type | Description | Risk |
|---------|-------------|-------------|------|
| New 4.11 | Addition | DAN computation algorithm, crystal structure definition, DAN_ENABLED configuration, edge case handling | LOW — purely additive |
| 6.2 | Modification | Replace uniform prediction weights with affinity-weighted prediction. When DAN_ENABLED=false, all weights=1.0 (current behavior). | LOW — coefficient change |
| New 4.12 | Addition | Heritage section tracing Trinity -> Tetrahedron -> Lattice -> DAN -> Crystal -> Locus -> Network | NONE — documentation only |
| Appendix B | Addition | New parameters: DAN_ENABLED, DAN_MEMBERSHIP_CAP, AFFINITY_WEIGHT_INTRA_DAN, AFFINITY_WEIGHT_CROSS_DAN, AFFINITY_RAMP_EPOCHS | LOW — configurable constants |

**Hash ring interaction:** DANs are computed AFTER hash rings are constructed. The hash ring construction algorithm (C3 Section 4.1-4.2) is completely unchanged. DANs are a post-processing layer that reads hash ring state but does not modify it. This clean separation means CAT cannot introduce regressions in tidal scheduling.

**Predictive delta interaction:** The affinity weight change in Section 6.2 replaces:
```
// Current C3: uniform weight for all parcel members
prediction_weight(A, B) = 1.0  // for all A, B in same parcel
```
with:
```
// CAT-enabled: DAN-aware weighting
prediction_weight(A, B) = match:
    DAN_ENABLED == false:               1.0    // exact current behavior
    same DAN, same task type:           AFFINITY_WEIGHT_INTRA_DAN    // default 1.0
    same DAN, different task type:      0.7
    same parcel, no shared DAN:         AFFINITY_WEIGHT_CROSS_DAN    // default 0.3
    different parcel:                   0.0    // unchanged
```

When DAN_ENABLED=false, the function returns 1.0 for all same-parcel pairs — identical to current behavior. The change is guaranteed to be backward-compatible.

**Parcel reconfiguration interaction:** When a parcel splits, merges, or an agent joins/leaves:
1. Hash rings are reconstructed (existing C3 mechanism)
2. DANs are recomputed from new ring state (new step, deterministic)
3. Affinity weights are updated for new DAN memberships
4. Predictive models enter annealing phase for new DAN partners (3-epoch ramp)

Step 2-4 add latency to epoch boundary processing. Estimated additional time: <10ms for a parcel of 25 agents with 20 task types (20 DAN computations of ~100 operations each). This is negligible relative to hash ring reconstruction time.

**Bi-timescale controller interaction:** The bi-timescale controller (C3 Parcel Manager) operates on SLV (Scope Load Vector) metrics. DANs do not modify the SLV computation. The controller's split/merge decisions are unaffected. DANs simply recompute after any controller action.

### 3.2 C5 PCVM Integration: DANs vs. VRF Committees

This is the most critical integration point. DANs and VRF committees are both "small groups of agents" but serve fundamentally different purposes:

| Property | DAN | VRF Committee |
|----------|-----|---------------|
| Purpose | Task execution coordination | Claim verification |
| Scope | Intra-parcel | Locus-wide (potentially cross-parcel) |
| Formation | Deterministic from hash ring | VRF sortition with diversity filtering |
| Persistence | Semi-persistent (stable across epochs if ring stable) | Ephemeral (formed per-claim, dissolved after verification) |
| Size | 3-5 (safety-class-dependent) | 5-9 (claim-class-dependent, default 7) |
| Role basis | Capability vectors | VRF randomness + diversity pools |
| Anonymity | Fully transparent (all agents compute identical DANs) | Anonymous (VRF self-selection, AVAP cover traffic) |

**The critical isolation requirement:** VRF committee selection (C5 Section 5.2-5.6) takes as input:
1. VRF seed (epoch-derived)
2. Agent public keys
3. Diversity attributes (hidden per C3 Section 5.3)
4. Claim hash

None of these inputs include DAN membership, DAN role, or crystal structure. Therefore, DAN structure is already invisible to VRF selection by construction. No modification to C5 is needed to achieve isolation — it is the default state.

**The VERIFY_LIAISON role clarification:** The DAN's VERIFY_LIAISON role MUST be clearly distinguished from PCVM verification:

> **VERIFY_LIAISON (DAN role):** Prepares Verification Trace Documents (VTDs) for claims produced by DAN members. Formats claim metadata, assembles evidence chains, and submits to the verification membrane. Tracks verification status and relays membrane certificates back to the DAN. Does NOT evaluate claims, does NOT participate in VRF committee selection for claims it submits, and does NOT have access to committee composition.

This clarification should be added as a note to C5 Section 11 (Integration Architecture).

**Risk assessment: verification capture.** C31-A (Simplification Agent) raised the concern that persistent DAN membership could lead to verification capture — DAN members becoming sympathetic to each other's claims. This risk is mitigated by three structural properties:
1. VRF committee members are drawn from the locus population (100+ agents), not from the producing DAN (3-5 agents). The probability of a DAN-mate being on the verification committee is DAN_SIZE / LOCUS_AGENTS, typically < 5%.
2. AVAP anonymous selection means the producer does not know who is on the committee.
3. The VERIFY_LIAISON only formats and submits — it cannot influence verification outcomes.

**Residual risk: LOW.** No new verification capture pathway is created by DANs.

### 3.3 C7 RIF Integration: Parcel Executor Extension

The C7 RIF decomposition hierarchy is currently: Global Executive (GE) -> Locus Decomposer (LD) -> Parcel Executor (PE).

With CAT, the PE gains an additional routing option. Currently, PE maps leaf intents directly to individual agents via `c3.schedule_operation()`. With DANs enabled, PE can optionally route leaf intents to DAN anchors, which distribute work within the DAN based on role assignments.

**Proposed extension to PE (C7 Section 10.4):**

```
function pe_execute_intent(leaf: IntentQuantum, agent: AgentRecord):
    if DAN_ENABLED and leaf.constraints.dan_routing:
        // Find the DAN that covers this task type for this agent
        dan = compute_dan(
            ring = get_ring(agent.parcel_id, leaf.task_type),
            task_hash = hash(leaf.intent_id),
            agent_roster = get_roster(agent.parcel_id),
            safety_class = get_safety_class(agent.locus_id),
            epoch = current_epoch()
        )
        // Route to the best-fit DAN member by role
        target_agent = dan.member_for_role(leaf.required_role)
        c3_op = map_intent_to_c3_operation(leaf)
        result = c3.schedule_operation(
            operation = c3_op,
            agent_id = target_agent,
            parcel_id = agent.parcel_id,
            deadline = leaf.constraints.deadline_epoch,
            priority = leaf.constraints.priority
        )
    else:
        // Current behavior (unchanged)
        c3_op = map_intent_to_c3_operation(leaf)
        result = c3.schedule_operation(
            operation = c3_op,
            agent_id = agent.agent_id,
            parcel_id = agent.parcel_id,
            deadline = leaf.constraints.deadline_epoch,
            priority = leaf.constraints.priority
        )
    // ... remainder unchanged
```

**Key design decision:** DAN routing in RIF is OPTIONAL per-intent (`leaf.constraints.dan_routing`). Intents that do not specify DAN routing use the current direct-to-agent path. This preserves backward compatibility and allows intents to opt into DAN-aware scheduling when beneficial.

**Hierarchy change:** The hierarchy does NOT gain a fourth level. The DAN anchor is not a new decomposition tier — it is a routing optimization within the existing PE level. The PE still receives leaf intents from the LD and reports results back to the LD. The internal routing to DAN members is transparent to the LD.

**Risk: PE complexity increase.** The PE gains a conditional branch (DAN routing vs. direct routing). This is a minor complexity increase — one `if/else` in the execution path. The DAN computation is deterministic and fast (O(1) per intent after ring lookup).

### 3.4 C8 DSF Integration: DAN Coherence Bonus

The Ideation Council proposed an optional DAN coherence bonus: agents that remain in stable DANs for multiple consecutive epochs receive a small settlement bonus reflecting the value of deep predictive model convergence.

**Proposed mechanism:**

```
DAN_COHERENCE_BONUS_ENABLED = false       // off by default
DAN_COHERENCE_BONUS_MAX = 0.05            // 5% of base reward (Ideation Condition 4)
DAN_COHERENCE_BONUS_RAMP_EPOCHS = 5       // epochs to reach full bonus

function compute_dan_coherence_bonus(
    agent_id: AgentId,
    dan_history: List[(EpochId, DAN)],
    base_reward: AIC
) -> AIC:
    if not DAN_COHERENCE_BONUS_ENABLED:
        return 0

    // Count consecutive epochs in same DAN (same members, same roles)
    consecutive = count_consecutive_stable_epochs(agent_id, dan_history)

    // Linear ramp from 0% to MAX over RAMP epochs
    bonus_fraction = min(
        DAN_COHERENCE_BONUS_MAX,
        DAN_COHERENCE_BONUS_MAX * (consecutive / DAN_COHERENCE_BONUS_RAMP_EPOCHS)
    )

    return base_reward * bonus_fraction
```

**Integration with C8 settlement function:** The coherence bonus is computed by the Settlement Calculator (C3 Component 11) and added to the agent's per-epoch settlement record. The deterministic computation uses DAN membership history, which is derivable from hash ring state at each epoch — no new on-chain data is required.

**Perverse incentive analysis (per Ideation Condition 4):**

| Perverse Incentive | Mitigation |
|--------------------|------------|
| Agents avoid parcel reconfiguration to preserve DAN stability | 5% cap means the maximum forgone reward from reconfiguration is 5% of base — far less than the efficiency gain from proper load balancing |
| Agents collude to maintain stable DANs | DAN stability is a function of hash ring stability, not agent behavior. Agents cannot control who their DAN partners are without controlling hash ring positions (which requires Sybil attacks — already mitigated by C8 staking) |
| Agents game the "consecutive stable epochs" counter | The counter is deterministically computable from hash ring state. No self-reporting. |

**Verdict: Safe at 5% cap.** The coherence bonus is too small to distort behavior but large enough to create a measurable preference for stability (all else equal). Disabled by default; enabled only when empirical data supports it.

### 3.5 C6 EMA Integration

The DAN's KNOWLEDGE_ACCESS role formalizes a currently-unspecified interaction: which agent in a parcel mediates knowledge retrieval from EMA's metabolic interface?

Currently, C6 EMA does not specify which agent performs knowledge operations within a parcel. Any agent can invoke EMA's retrieval, consolidation, and persistence APIs. With DANs, the KNOWLEDGE_ACCESS role designates a preferred agent for these operations within each DAN:

- The KNOWLEDGE_ACCESS agent maintains a warm cache of recently accessed artifacts for the DAN's task type
- Other DAN members route knowledge requests through the KNOWLEDGE_ACCESS agent (when co-located) rather than independently querying EMA
- This reduces redundant EMA queries from DAN members working on related tasks

**Change to C6:** Add a note to C6's metabolic interface specification:

> "When CAT (C31) is enabled, the DAN KNOWLEDGE_ACCESS role serves as the preferred EMA interaction point within each DAN. This is an optimization hint, not a hard constraint: any agent MAY invoke EMA APIs directly. The KNOWLEDGE_ACCESS role reduces redundant queries by maintaining a DAN-local artifact cache."

**Risk: LOW.** This is an optimization hint, not a structural dependency. If the KNOWLEDGE_ACCESS agent fails, other DAN members invoke EMA directly — existing behavior.

### 3.6 C9 Cross-Layer Constraints

C9 established the canonical cross-layer integration constraints. CAT must comply with:

| C9 Constraint | CAT Compliance |
|---------------|:-:|
| C5 is sole claim class authority | PASS — DANs do not classify claims |
| C8 is sole settlement authority | PASS — DAN coherence bonus is computed by C8 settlement calculator |
| 9 canonical claim classes (D/C/P/R/E/S/K/H/N) | PASS — DANs do not modify claim classes |
| Three-tier epoch hierarchy (60s/3600s/36000s) | PASS — DANs recompute at TIDAL_EPOCH boundaries |
| C4 epistemic_class maps to C5 claim_class deterministically | PASS — DANs are orthogonal to this mapping |

**No C9 violations detected.**

### 3.7 Integration Feasibility Verdict

**FEASIBLE.** CAT integrates cleanly with all five existing spec layers. The changes are:
- C3: +1 new section, +1 modified section, +5 new parameters (all additive)
- C5: +1 clarification note (no mechanism change)
- C6: +1 optimization note (no mechanism change)
- C7: +1 conditional branch in PE (backward-compatible)
- C8: +1 optional parameter, +1 bonus computation function (disabled by default)
- C9: no changes needed

Total cross-spec changes: ~350-400 lines. No existing mechanism is removed or modified in a non-backward-compatible way.

---

## 4. Adversarial Analysis (Counter-Report)

*Prepared by the Adversarial Analyst role. This section is a counter-report that assumes a sophisticated adversary with full knowledge of the CAT specification.*

### 4.1 Attack Vector: Hash Ring Position Manipulation

**Attack:** An adversary generates agent IDs whose SHA256 hashes place them adjacent to a target agent on the hash ring, ensuring they are selected as DAN partners.

**Difficulty:** SHA256 is collision-resistant. Finding an ID that hashes to a specific ring position requires brute-force search over 2^256 possibilities. Finding an ID that hashes to a position NEAR a target requires searching until the hash falls within a window of size W around the target. For a ring with N agents, the average inter-agent distance is 2^256/N. To guarantee adjacency, the attacker needs to find an ID within distance 2^256/(N*V) of the target (where V = virtual nodes per agent). At N=10, V=200, this is 2^256/2000 — still astronomically large.

**Additional barrier:** C8 DSF requires agents to stake AIC to participate. Creating multiple Sybil agents requires proportional economic investment.

**Severity: NEGLIGIBLE.** Hash ring position manipulation is computationally infeasible. This attack vector exists in the current C3 model (for task assignment manipulation) and is already mitigated by SHA256 pre-image resistance.

### 4.2 Attack Vector: Capability Vector Gaming

**Attack:** An adversary misreports or manipulates capability vectors to be assigned preferred DAN roles (e.g., KNOWLEDGE_ACCESS for data exfiltration, or VERIFY_LIAISON for claim manipulation).

**Difficulty:** Capability vectors are derived from PCVM verification history (Ideation Condition 2), not self-reported. To game the COMPUTE score, an agent must actually complete tasks at high throughput (verified by C3 tidal scheduler). To game the VERIFY_LIAISON score, an agent must submit VTDs that pass membrane verification. To game the REASONING_DEPTH score, an agent must produce R-class and H-class claims that pass PCVM credibility evaluation.

**Residual attack surface:** An agent could strategically choose WHICH tasks to accept and WHICH claims to produce to inflate specific capability dimensions. For example, an agent could exclusively produce simple D-class claims (high acceptance rate) to inflate its VERIFY_LIAISON score, then use the role to format VTDs in a way that subtly introduces bias.

**Mitigation:** The capability derivation function should use a balanced score that weights both volume and diversity:
```
verify_liaison_score = (vtd_accepted / max(1, vtd_submissions)) *
                       diversity_factor(claim_classes_covered)
```
This penalizes agents that game a single claim class.

**Severity: LOW.** The attack requires sustained effort over multiple epochs, produces only a role preference (not a privilege), and the role itself has no special powers (VERIFY_LIAISON cannot influence verification outcomes).

### 4.3 Attack Vector: DAN Role Information Leakage

**Attack:** DAN structure is fully transparent — all agents compute identical DANs. An adversary knows exactly which agents are in which DANs and which roles they hold. This information could be exploited by a collusion ring to:
1. Identify which agent will format VTDs (the VERIFY_LIAISON) and target it for social engineering
2. Identify which agent accesses knowledge (KNOWLEDGE_ACCESS) and feed it poisoned data
3. Map the crystal bond structure to identify information chokepoints

**Analysis:** This is a genuine information leakage that does not exist in the current C3 model (where all agents are undifferentiated). However, the leaked information is LIMITED:
- DAN roles are operational hints, not security-critical permissions
- VTD formatting is transparent (the VTD format is standardized per C5)
- Knowledge access is not exclusive (any agent can query EMA)
- Crystal structure does not reveal anything about VRF committee composition (which is the actual security-sensitive structure)

**Comparison to baseline:** In the current C3 model, hash ring positions are also transparent — an adversary can compute which agent handles which tasks. DAN role information is a marginal increase in transparency, not a qualitative change.

**Severity: MEDIUM.** The information leakage is real but its exploitability is limited. The most concerning scenario is collusion ring coordination: colluders can identify which DAN roles their co-conspirators hold and coordinate claim formatting accordingly. Mitigation: the AVAP anonymous committee selection (C12) ensures that even if colluders know DAN roles, they cannot identify who will verify their claims.

### 4.4 Attack Vector: DAN Composition Steering

**Attack:** An adversary with multiple Sybil agents in the same parcel attempts to concentrate them in the same DAN, creating a "captured DAN" where all members are adversary-controlled.

**Difficulty:** DAN membership is determined by hash ring adjacency. To place K Sybil agents in the same DAN, the adversary needs K agents with adjacent hash positions. For K=3 (minimum DAN size), this requires 3 agents in the same 3/N fraction of the ring.

**Probability analysis:** For a parcel with N agents, if an adversary controls F of them (F < N/3 per Byzantine assumption), the probability that a randomly formed DAN of size S contains >=S adversary-controlled agents is:
```
P(captured DAN) = C(F, S) * C(N-F, 0) / C(N, S)
```
For N=12, F=3, S=4: P = 0 (F < S, impossible to capture a 4-agent DAN with only 3 adversarial agents).
For N=12, F=4, S=3: P = C(4,3)*C(8,0)/C(12,3) = 4/220 = 0.018 (1.8%).

However, this assumes random placement. With hash ring adjacency, the probability depends on whether the adversary's agents cluster. Since SHA256 distributes agents pseudo-randomly, the adversary cannot control clustering without brute-forcing hash positions (see Section 4.1).

**Additional barrier:** Capturing a DAN provides limited advantage. The captured DAN can produce claims, but verification still goes through the VRF membrane (independent of DAN structure). The captured DAN can at most produce a higher volume of low-quality claims, which the 7% random deep audit and CACT mechanisms will detect.

**Severity: MEDIUM.** The attack is statistically improbable and provides limited advantage, but the scenario of Sybil agents coincidentally clustering in a DAN is non-zero and should be monitored. Recommendation: add a DAN diversity check that flags DANs where all members have below-median credibility scores.

### 4.5 Attack Vector: Crystal Structure Reconnaissance

**Attack:** An adversary maps the entire crystal structure (all DANs, all bonds, all roles) to identify structural vulnerabilities — e.g., agents that serve as bonds between many DANs (high betweenness centrality) and whose failure would fragment the crystal.

**Analysis:** Crystal structure is deterministically computable by any agent, so this "attack" requires no special access. However, targeting high-centrality agents for denial-of-service attacks could degrade information flow within the parcel.

**Mitigation:** Crystal fragmentation is a performance concern, not a correctness concern. If high-centrality agents fail, DANs recompute at the next epoch boundary. Information flow degrades to the current C3 model (no crystal, uniform prediction weights) until annealing completes. The graceful degradation property means crystal fragmentation cannot cause data loss or correctness violations.

**Severity: NEGLIGIBLE.** Crystal structure is public information, targeted agent failure causes only temporary performance degradation, and the system degrades to current C3 behavior.

### 4.6 Attack Vector: Coherence Bonus Exploitation

**Attack:** An adversary maintains stable DAN membership across many epochs to accumulate the maximum coherence bonus (5% of base reward), while doing minimal useful work.

**Analysis:** The coherence bonus is additive to the base reward, which is itself dependent on task completion and verification success. An agent doing "minimal useful work" earns a low base reward. 5% of a low base reward is negligible. The attack is self-defeating: to earn a meaningful bonus, the agent must earn a meaningful base reward, which requires doing meaningful work.

**Quantitative example:** Base reward for an active agent: ~10 AIC/epoch. Coherence bonus: 0.5 AIC/epoch (5% * 10). An idle agent's base reward: ~0 AIC/epoch. Idle coherence bonus: ~0 AIC/epoch (5% * 0). The bonus provides no incentive for idleness.

**Severity: LOW.** The 5% cap (Ideation Condition 4) makes this attack economically irrational.

### 4.7 Attack Vector: Affinity Weight Manipulation

**Attack:** An adversary attempts to exploit the affinity-weighted prediction to inject false surprise signals. If the adversary knows that its DAN partner has a high affinity weight (1.0), it can generate behavior that deviates from the partner's prediction, triggering a surprise response that wastes communication bandwidth.

**Analysis:** This is a variant of the existing surprise flooding attack (C3 Section 10.2). In the current model, any agent can generate surprises for any parcel member. With CAT, intra-DAN surprises have higher priority (weight 1.0 vs. 0.3), so adversary-generated surprises from within a DAN consume more predictive model update bandwidth than inter-DAN surprises.

**Mitigation:** C3's existing surprise throttling (Section 4.9, storm detection) applies to DAN-internal surprises as well. An agent generating excessive surprises triggers storm detection regardless of whether the surprises are intra-DAN or inter-DAN. Additionally, the PCVM credibility engine (C5) penalizes agents whose behavior is consistently unpredictable (high surprise rate correlates with low credibility).

**Severity: NEGLIGIBLE.** Existing mitigations cover this attack. The affinity weight amplifies the signal but not the agent's ability to generate it.

### 4.8 Adversarial Analysis Summary

| # | Attack Vector | Severity | Mitigation Status |
|---|---------------|----------|-------------------|
| 1 | Hash ring position manipulation | NEGLIGIBLE | SHA256 pre-image resistance + C8 staking |
| 2 | Capability vector gaming | LOW | PCVM-derived capabilities + diversity weighting |
| 3 | DAN role information leakage | MEDIUM | AVAP anonymous committees; roles are hints not privileges |
| 4 | DAN composition steering | MEDIUM | SHA256 randomization + Sybil cost; add DAN diversity monitoring |
| 5 | Crystal structure reconnaissance | NEGLIGIBLE | Public info; graceful degradation to C3 baseline |
| 6 | Coherence bonus exploitation | LOW | 5% cap; bonus scales with base reward (no free lunch) |
| 7 | Affinity weight manipulation | NEGLIGIBLE | Existing surprise throttling + credibility penalties |

**Overall adversarial assessment: ADEQUATE.** No HIGH or CRITICAL attack vectors identified. Two MEDIUM vectors require specification-time mitigations (DAN diversity monitoring, clear documentation that roles are non-privileged hints). The adversarial surface of CAT is comparable to the current C3 model — DAN structure reveals slightly more information about agent relationships, but this information is not security-sensitive because verification (the actual trust-bearing mechanism) operates independently.

**Mandatory specification requirements from adversarial analysis:**
1. DAN diversity monitoring: flag DANs where all members have credibility below PCVM median
2. VERIFY_LIAISON role documentation must include explicit prohibition on any influence over VRF selection
3. Capability derivation must include diversity factor to prevent single-class gaming

---

## 5. Complexity Assessment

### 5.1 Specification Complexity

**New specification content:**

| Spec | New Content | Lines (est.) | Complexity |
|------|------------|:---:|:-:|
| C3 Section 4.11 | DAN computation algorithm, crystal structure, edge cases | 180-220 | MEDIUM |
| C3 Section 6.2 mod | Affinity-weighted prediction coefficients | 25-35 | LOW |
| C3 Heritage section | Intellectual lineage documentation | 40-60 | LOW |
| C3 Appendix B additions | 5 new configurable parameters | 15-20 | LOW |
| C5 clarification note | VERIFY_LIAISON is not a verifier | 10-15 | LOW |
| C6 integration note | KNOWLEDGE_ACCESS optimization hint | 15-20 | LOW |
| C7 Section 10.4 mod | Optional DAN routing in PE | 30-40 | LOW |
| C8 settlement addition | DAN coherence bonus function | 25-35 | LOW |
| **Total** | | **340-445** | **MODERATE** |

### 5.2 Implementation Complexity

**New code modules:**

| Module | Purpose | Est. Size | Dependencies |
|--------|---------|:-:|:-:|
| DAN Computation Engine | compute_dan(), assign_roles_by_capability() | ~200 LOC | Hash ring, agent roster, capability vectors |
| Capability Derivation Pipeline | derive_capability_vector() | ~150 LOC | PCVM history, tidal history, EMA metrics |
| Affinity Weight Calculator | prediction_weight() | ~30 LOC | DAN membership index |
| Crystal Structure Analyzer | classify_crystal(), compute_bonds() | ~100 LOC | DAN index (optional, for monitoring/debugging) |
| DAN Coherence Bonus | compute_dan_coherence_bonus() | ~50 LOC | DAN history, settlement calculator |
| **Total** | | **~530 LOC** | |

**Comparison to existing codebase:** The C3 specification alone is 3,503 lines. The total AAS specification across 5 Master Tech Specs is 21,166 lines. Adding ~400 specification lines (1.9% increase) and ~530 implementation LOC is a modest addition.

### 5.3 Cognitive Complexity

This is the most significant cost. Engineers working on the AAS must understand:

**Without CAT:** Locus -> Parcel -> Hash Ring -> Agent. Three-level hierarchy. Agent assignment is purely hash-ring-based. All agents in a parcel are equivalent.

**With CAT:** Locus -> Parcel -> Hash Ring -> DAN -> Agent. Conceptually four levels (though DAN is not a decomposition tier in the RIF sense). Agents have DAN-assigned roles. Predictive models have non-uniform weights. Crystal structure provides emergent small-world topology.

**Cognitive cost mitigation:**
1. CAT is OPTIONAL. Engineers can fully understand and implement C3 without DANs. DANs are an enhancement layer with a clean on/off switch.
2. When disabled, no DANs exist. There is no "ghost DAN" state or partial DAN behavior.
3. The DAN concept maps to a familiar mental model: "your closest work partners for this task type." This is intuitive even for engineers unfamiliar with crystallographic terminology.

**Cognitive complexity rating: MODERATE.** The crystal/crystallographic terminology is potentially intimidating but the underlying concept (affinity groups of 3-5 hash ring neighbors with capability-based roles) is straightforward.

### 5.4 Testing Complexity

**New test requirements:**

| Test Category | Tests Needed | Complexity |
|---------------|:---:|:-:|
| DAN determinism | Verify identical DANs from identical inputs across implementations | LOW |
| DAN edge cases | Minimum parcel, single task type, T >> N, identical capabilities | MEDIUM |
| Invariant preservation | Verify all 7 C3 invariants hold with DANs enabled | MEDIUM |
| Affinity weight behavior | Verify prediction convergence with non-uniform weights | MEDIUM |
| Capability derivation | Verify correct pipeline from PCVM/tidal history | MEDIUM |
| DAN-disabled equivalence | Verify exact behavioral match with current C3 when disabled | LOW |
| Adversarial tests | Sybil clustering, capability gaming, surprise flooding | HIGH |
| Integration tests | C3+C5 isolation, C7 PE routing, C8 bonus calculation | MEDIUM |
| Performance tests | DAN computation overhead at scale, annealing convergence | HIGH |

**Total estimated testing effort:** 160-240 person-hours. This is comparable to a mid-size hardening pass (C10 was ~200 person-hours for 49 fixes).

### 5.5 Complexity Budget Analysis

**The question:** Given the AAS's existing complexity (21,166 specification lines, 5 Master Tech Specs, 13 completed invention cycles), is the marginal complexity of CAT justified?

**Arguments for:**
1. CAT fills a documented architectural gap (C31 Research Report Section 11, Gap G-1: "No intra-parcel structure"). The gap is rated HIGH severity.
2. The complexity is bounded and optional. Disabling DANs eliminates all runtime complexity.
3. The per-spec changes are small (largest addition: ~220 lines to C3).
4. The concept is conceptually orthogonal to existing mechanisms — it does not interleave with hash ring construction, VRF selection, or settlement computation.

**Arguments against:**
1. The AAS has never been implemented. Adding complexity to an unimplemented system increases the distance to first deployment.
2. The primary benefit (transient communication reduction) is speculative.
3. The capability derivation pipeline requires new infrastructure (C6 metrics interface).
4. The "optional" argument cuts both ways: if it is truly optional, maybe it should be deferred until after Phase 1 deployment proves the gap is real.

**Council assessment:** The complexity is justified because (a) the gap is real (documented in Research with cross-domain evidence), (b) the complexity is bounded and optional, (c) specifying CAT now preserves the design option even if implementation is deferred to Phase 2, and (d) the specification cost (~400 lines, 1.9% increase) is modest relative to the insight gained.

However, the council recommends that **implementation** of CAT be deferred to Phase 2. Phase 1 should deploy with DAN_ENABLED=false. The specification should be complete in the Master Tech Spec, but the implementation priority should be below core C3 mechanisms.

---

## 6. Risk Assessment

### 6.1 Risk Register

| # | Risk | Likelihood | Impact | Severity | Mitigation |
|---|------|:-:|:-:|:-:|-----------|
| R-1 | DAN computation introduces non-determinism due to implementation-dependent floating-point or sorting behavior | LOW | CRITICAL | MEDIUM | Specify: integer-only capability scores, stable sort with agent-ID tiebreaker, no floating-point in DAN computation path |
| R-2 | Capability vector pipeline from PCVM history proves too expensive or too stale | MEDIUM | LOW | LOW | Degrade to uniform capabilities (all agents score 1.0 on all dimensions); DAN roles become position-based (equivalent to C31-B but with variable size) |
| R-3 | Affinity weighting causes predictive model divergence in edge cases (oscillating weights during rapid DAN reconfiguration) | LOW | MEDIUM | LOW | Specify monotonic annealing: weights only increase during ramp-up, never decrease mid-ramp; add AFFINITY_RAMP_EPOCHS minimum (3) |
| R-4 | DAN coherence bonus creates perverse incentives not anticipated by the 5% cap analysis | LOW | MEDIUM | LOW | Disabled by default; requires explicit governance vote (G-class) to enable; includes automatic circuit breaker if Gini coefficient of coherence bonuses exceeds 0.4 |
| R-5 | Crystal structure at scale (10,000 agents) exhibits emergent pathological properties (e.g., bifurcation, oscillation between DENSE and SPARSE) | MEDIUM | MEDIUM | MEDIUM | Empirical validation gate (Ideation Condition 6): DANs are not enabled by default until Phase 2 simulation confirms benign crystal behavior |
| R-6 | The "optional layer" argument leads to indefinite deferral — DANs are specified but never enabled | MEDIUM | LOW | LOW | Specify explicit empirical gates: if Phase 2 shows >20% transient communication reduction, DANs become default-enabled in Phase 3 |
| R-7 | Adversarial DAN composition steering via Sybil agents in small parcels | LOW | MEDIUM | LOW | DAN diversity monitoring (Section 4.4); minimum parcel size already mitigates (5 agents, requiring >1 Sybil to control a DAN of 3) |
| R-8 | C6 EMA metrics interface never gets implemented, leaving 2/5 capability dimensions permanently unavailable | MEDIUM | LOW | LOW | System functions with 3/5 dimensions; add C6 metrics to Phase 2 implementation plan |

### 6.2 Scoring

| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| **Novelty** | **3/5** | DAN concept is a synthesis of consistent hashing neighborhoods + capability-aware role assignment + affinity-weighted prediction. The individual components are known; the combination within an epistemic coordination fabric is novel but not groundbreaking. The "coordination crystal" framing is conceptually appealing but adds no technical novelty beyond DANs + bonds. Downgraded from Ideation's 4/5 because the crystal structure's emergent properties are unproven. |
| **Feasibility** | **4/5** | DAN computation is deterministic, O(T) marginal cost, preserves all invariants. Integration is clean across all 5 specs. Capability pipeline is constructible from existing data (with C6 gap). Implementation is ~530 LOC. Upgraded from Ideation's 3/5 because detailed analysis confirms no technical blockers. |
| **Impact** | **3/5** | Primary impact: recovers lost small-group coherence property. Secondary impact: reduces transient communication during reconfiguration (speculative, requires empirical validation). Tertiary impact: enables future DAN-aware optimizations (caching, scheduling). Downgraded from Ideation's 4/5 because the primary benefit is speculative and the system already works without DANs. The "organizational legibility" argument, while conceptually valid, provides no measurable performance gain. |
| **Risk** | **5/10** | MEDIUM. No HIGH-severity risks. Two MEDIUM risks (R-1: non-determinism, R-5: emergent crystal pathology). Both are mitigatable with specification discipline and empirical validation. The optional-by-default design caps downside risk. |

---

## 7. Verdict

### 7.1 Decision

**ADVANCE to DESIGN (Stage 4).**

**Justification:** CAT is technically sound, integrates cleanly with the existing AAS stack, introduces no HIGH-severity adversarial vulnerabilities, and its complexity cost is bounded by the optional-by-default design. The primary uncertainty — whether DANs provide measurable transient communication improvement — is an empirical question that can only be answered after specification and simulation, not before.

The Feasibility Council finds that:

1. The research report's conclusion that "hybrid is correct" is strongly supported. Every production distributed system uses fixed-size groups within elastic structures. C3 is an anomaly in lacking this.

2. CAT's design is superior to C31-B (rigid tetrahedral cells) because it avoids the coordinator bottleneck, remainder problem, and position-based role assignment.

3. The graceful degradation property (DAN_ENABLED=false reverts exactly to current C3) eliminates the risk of CAT making the system worse. The design is monotonically beneficial or neutral.

4. The specification should be written now, with implementation deferred to Phase 2. This preserves the design option while focusing Phase 1 engineering on core C3 mechanisms.

### 7.2 Conditions for Advancement

All six Ideation conditions are confirmed. The Feasibility Council adds four additional conditions:

**From Ideation (confirmed):**

| # | Condition | Status |
|---|-----------|--------|
| IC-1 | OPTIONAL by default (DAN_ENABLED=false in Phase 1-2) | CONFIRMED |
| IC-2 | Capability vectors from PCVM history, not self-reported | CONFIRMED — pipeline specified in Section 2.5 |
| IC-3 | VRF isolation (DAN structure invisible to VRF committees) | CONFIRMED — isolation holds by construction (Section 3.2) |
| IC-4 | Settlement bonus capped at 5% of base reward | CONFIRMED — analysis shows 5% is safe (Section 3.4) |
| IC-5 | Heritage documentation tracing intellectual lineage | CONFIRMED |
| IC-6 | Empirical validation gate for Phase 3 enablement | CONFIRMED |

**From Feasibility (new):**

| # | Condition | Rationale |
|---|-----------|-----------|
| FC-1 | DAN computation MUST use integer-only capability scores with stable sort and agent-ID tiebreaker. No floating-point in the DAN computation path. | Prevents non-determinism from IEEE 754 rounding differences across implementations (Risk R-1) |
| FC-2 | Capability derivation MUST include a diversity factor that penalizes single-claim-class gaming. | Prevents capability vector gaming (Section 4.2) |
| FC-3 | The Design specification MUST include a DAN diversity monitoring mechanism that flags DANs where all members have below-median PCVM credibility scores. | Mitigates DAN composition steering (Section 4.4) |
| FC-4 | Implementation MUST be deferred to Phase 2. Phase 1 deploys with DAN_ENABLED=false. The specification is complete in the Master Tech Spec but implementation priority is below core C3 mechanisms. | Focuses Phase 1 engineering on proven mechanisms; CAT implementation begins only when core C3 is validated |

### 7.3 Specification Directives

The Design stage MUST produce a Master Tech Spec addendum (or C3 v3.0 section) covering:

1. **DAN Computation Algorithm** — complete, deterministic, with integer-only scores, stable sort, agent-ID tiebreaker, and all edge cases from Section 2.4
2. **Capability Vector Derivation Pipeline** — formal specification with 5 dimensions, diversity factor, epoch-boundary computation, and graceful degradation to 3 dimensions when C6 metrics are unavailable
3. **Affinity-Weighted Prediction** — coefficient specification, annealing protocol (monotonic ramp over AFFINITY_RAMP_EPOCHS), and interaction with C3 storm detection
4. **Crystal Structure Definition** — formal definition of bonds and lattice type (for monitoring/analysis; not operationally critical)
5. **DAN Coherence Bonus** — settlement integration, G-class governance gate, circuit breaker specification
6. **DAN Diversity Monitoring** — credibility-based flagging mechanism
7. **Heritage Section** — Trinity -> Tetrahedron -> Lattice -> DAN -> Crystal -> Locus -> Network lineage
8. **Integration Contracts** — formal interface specifications for C5 (isolation proof), C6 (metrics), C7 (PE extension), C8 (bonus)
9. **Configurable Parameters** — DAN_ENABLED, DAN_MEMBERSHIP_CAP, AFFINITY_WEIGHT_INTRA_DAN, AFFINITY_WEIGHT_CROSS_DAN, AFFINITY_RAMP_EPOCHS, DAN_COHERENCE_BONUS_ENABLED, DAN_COHERENCE_BONUS_MAX, DAN_COHERENCE_BONUS_RAMP_EPOCHS
10. **Validation Plan** — empirical gates for Phase 2 enablement, specific experiments (DAN vs. no-DAN transient communication measurement, crystal stability at scale, capability gaming resistance)

---

## Appendix A: DAN Computation Walkthrough

**Scenario:** Parcel P with 10 agents (A0-A9) on a hash ring for task type `task.compute`, safety class MEDIUM (DAN_SIZE=4).

**Step 1:** A task arrives with hash H. Hash ring lookup (bounded-loads) assigns the task to agent A3 (closest clockwise).

**Step 2:** DAN_SIZE = 4 (MEDIUM safety class).

**Step 3:** Clockwise neighbors of A3 on the ring: A7, A1, A5, A9, A0, A6, A2, A8 (ordered by ring distance from A3's position). Select first 8 candidates (2 * DAN_SIZE).

**Step 4:** Capability-aware selection:
```
Required capabilities: {COMPUTE, VERIFY_LIAISON, KNOWLEDGE_ACCESS}

A3 (primary): capabilities = {COMPUTE: 850, VERIFY_LIAISON: 400, KNOWLEDGE_ACCESS: 600}
  covered = {COMPUTE}  (highest score)

A7 (candidate 1): capabilities = {COMPUTE: 500, VERIFY_LIAISON: 900, KNOWLEDGE_ACCESS: 300}
  new_coverage = {VERIFY_LIAISON}  -> SELECT
  covered = {COMPUTE, VERIFY_LIAISON}

A1 (candidate 2): capabilities = {COMPUTE: 700, VERIFY_LIAISON: 300, KNOWLEDGE_ACCESS: 200}
  new_coverage = {}  -> SELECT (need at least 3 members)
  covered = {COMPUTE, VERIFY_LIAISON}

A5 (candidate 3): capabilities = {COMPUTE: 400, VERIFY_LIAISON: 200, KNOWLEDGE_ACCESS: 800}
  new_coverage = {KNOWLEDGE_ACCESS}  -> SELECT
  covered = {COMPUTE, VERIFY_LIAISON, KNOWLEDGE_ACCESS}

DAN_SIZE=4 reached. Stop.
```

**Step 5:** Role assignment by capability score:
```
COMPUTE role:           A3 (score 850 > A1:700 > A7:500 > A5:400)
VERIFY_LIAISON role:    A7 (score 900 > A3:400 > A1:300 > A5:200)
KNOWLEDGE_ACCESS role:  A5 (score 800 > A3:600 > A7:300 > A1:200)
EXECUTOR role:          A1 (remaining member)
```

**Result:** DAN = {A3: COMPUTE, A7: VERIFY_LIAISON, A5: KNOWLEDGE_ACCESS, A1: EXECUTOR}, anchor = A3.

**Every agent in parcel P independently computes this same DAN structure.** No messages exchanged.

---

## Appendix B: Overhead Budget Calculation

**Target:** 10,000 agents, 1,000 parcels, 10 agents/parcel, 20 task types/parcel.

| Component | Per Parcel/Epoch | System-Wide/Epoch | Per Second |
|-----------|:---:|:---:|:---:|
| DAN computations | 20 (1 per task type) | 20,000 | 5.6 |
| Operations per DAN computation | ~10 (ring lookup + candidate scan + role assignment) | 200,000 | 55.6 |
| Capability vector publication | 10 * 20 bytes = 200 bytes | 200 KB | 0.056 KB/s |
| Affinity weight lookups | 20 * 10 = 200 (per agent, per epoch) | 2,000,000 | 555.6 |

**Total marginal compute:** ~200,000 simple operations + 2,000,000 hash table lookups per epoch (every 3,600 seconds). This is approximately 0.1% of a single modern CPU core's capacity. **Negligible.**

**Total marginal bandwidth:** 200 KB per epoch for capability vectors. Current capacity snapshot (C3) exchanges approximately 1-10 MB per epoch. **0.2-2% increase. Negligible.**

---

## Appendix C: Attack Tree Summary

```
GOAL: Compromise CAT to gain unfair advantage
|
+-- [1] Control DAN composition
|   +-- [1a] Manipulate hash ring position (INFEASIBLE: SHA256 pre-image)
|   +-- [1b] Sybil agents in same parcel (LOW: C8 staking cost + random distribution)
|   +-- [1c] Manipulate capability vectors (LOW: PCVM-derived + diversity factor)
|
+-- [2] Exploit DAN role information
|   +-- [2a] Target VERIFY_LIAISON for VTD manipulation (LOW: VTD format is standardized)
|   +-- [2b] Target KNOWLEDGE_ACCESS for data poisoning (LOW: EMA access is non-exclusive)
|   +-- [2c] Map crystal for DoS targeting (NEGLIGIBLE: graceful degradation to C3)
|
+-- [3] Exploit economic mechanisms
|   +-- [3a] Farm coherence bonus without work (NEGLIGIBLE: bonus scales with base reward)
|   +-- [3b] Prevent reconfiguration to preserve bonus (NEGLIGIBLE: 5% cap < efficiency gain)
|
+-- [4] Exploit communication mechanisms
|   +-- [4a] Abuse affinity weights for surprise flooding (NEGLIGIBLE: existing storm detection)
|   +-- [4b] Manipulate annealing to delay convergence (LOW: monotonic ramp prevents oscillation)

Maximum achievable adversary advantage: MARGINAL
Required investment for meaningful attack: DISPROPORTIONATE to gain
Comparison to current C3 attack surface: COMPARABLE (no qualitative degradation)
```

---

*Feasibility Assessment prepared by the Feasibility Council for C31 — Agent Organizational Topology / Crystallographic Adaptive Topology (CAT).*
*Assessment date: 2026-03-11*
*Council decision: ADVANCE to DESIGN (Stage 4) with 10 conditions (6 from Ideation, 4 from Feasibility)*
*Next stage: DESIGN — produce Master Tech Spec addendum with complete DAN specification*
