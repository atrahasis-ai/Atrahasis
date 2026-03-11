# Tidal Noosphere --- System Architecture
## C3-A DESIGN Document

**Invention ID:** C3
**Concept:** C3-A (Tidal Noosphere)
**Stage:** DESIGN
**Version:** v0.1
**Date:** 2026-03-09
**Status:** DRAFT
**Assessment Council Verdict:** CONDITIONAL_ADVANCE
**Primary Scale Target:** 1K-10K agents (100K is Phase 4 aspiration)

---

## 1. Architecture Overview

### 1.1 System Identity

The Tidal Noosphere is the unified coordination architecture for Atrahasis, formed by absorbing PTA's deterministic scheduling engine into the Noosphere's epistemic coordination fabric and adopting the Locus Fabric's formal proof obligations as mandatory standards. The Noosphere remains the architecture. PTA becomes its scheduling substrate. The Locus Fabric provides its proof discipline.

### 1.2 Design Philosophy

Three principles govern every design decision in this architecture:

1. **The Membrane is Sovereign.** The Verification Membrane is constitutionally protected. No scheduling optimization, communication reduction, or governance convenience may weaken it. The rest of the system is optimized around the membrane, never the reverse. (Noosphere Architectural Commandment.)

2. **Agree by Computation, Communicate Only Surprises.** In steady state, agents compute identical schedules from shared inputs via deterministic hash ring evaluation. Communication occurs only when reality deviates from the computable prediction. The system is silent when correct. (PTA Design Constraint 1.)

3. **Proof Before Freedom.** An operation earns coordination-free execution (M-class) only after a machine-checked I-confluence proof demonstrates that concurrent execution preserves all declared invariants. Without proof, the operation defaults to a higher-cost agreement class. The system is correct before it is fast. (Locus Fabric proof discipline.)

### 1.3 Structural Overview

The architecture operates across three structural levels:

```
+=====================================================================+
|                           LOCUS LAYER                                |
|  Stable semantic domains. Correctness boundaries. Split rarely.      |
|  Invariant sets, safety classifications, governance scope.           |
|  Stigmergic decay signals (need, offer, risk, anomaly) at this scope |
+=====================================================================+
       |              |              |              |
+------v------+ +----v------+ +----v------+ +-----v-----+
| PARCEL A    | | PARCEL B  | | PARCEL C  | | PARCEL D  |
| Hash rings  | | Hash rings| | Hash rings| | Hash rings|
| per task    | | per task  | | per task  | | per task  |
| type        | | type      | | type      | | type      |
| Predictive  | | Predictive| | Predictive| | Predictive|
| delta comms | | delta     | | delta     | | delta     |
| VRF verifier| | VRF       | | VRF       | | VRF       |
| sets        | | verifier  | | verifier  | | verifier  |
+------+------+ +----+------+ +----+------+ +-----+-----+
       |              |              |              |
+------v--------------v--------------v--------------v------+
|             TIDAL SCHEDULING ENGINE                       |
|  Bounded-loads consistent hash rings (Mirrokni et al.)    |
|  ECVRF (RFC 9381) verifier selection                      |
|  Commit-reveal diversity + pre-stratified pools           |
|  Epoch clock, settlement calculator                       |
+----------------------------------------------------------+
```

### 1.4 Key Invariants

These invariants must hold under all conditions including degraded operation:

- **INV-1:** No claim enters durable memory without passing the Verification Membrane.
- **INV-2:** The membrane cannot be weakened by any non-constitutional action.
- **INV-3:** Every scheduling output is a deterministic pure function of shared inputs.
- **INV-4:** An operation is classified M-class only after a machine-checked I-confluence proof exists.
- **INV-5:** Loci define correctness boundaries; parcels define execution boundaries. These never conflate.
- **INV-6:** During parcel reconfiguration, the system operates in degraded-but-correct mode. Never in incorrect mode.
- **INV-7:** The tidal function version is itself a verified claim within the membrane it schedules (recursive closure).
- **INV-8:** ETR rollback completes within 3 epoch cycles under all trigger conditions.

### 1.5 Operation-Class Algebra

Agreement mode is derived from operation class, not chosen ad hoc:

| Class | Name | Agreement Mode | Steady-State Cost | Example Operations |
|-------|------|---------------|-------------------|-------------------|
| M | Merge/Convergence | CRDT-like merge, no coordination | O(1), zero communication | Signals, offers, needs, alerts, lineage references |
| B | Bounded Local Commit | CSO local spend, epoch rebalance | O(1), zero mid-epoch | Resource consumption within owned slice |
| X | Exclusive | Serial commit (single-parcel) or Fusion Capsule (multi-parcel) | O(quorum) | Lease acquisition, object mutation |
| V | Verification | Committee protocol through membrane | O(committee) | Claim verification, attestation |
| G | Governance | Constitutional BFT consensus | O(governance participants) | Parameter changes, tidal version approval, ETR |

### 1.6 Component Map

| Component | Section | Source Architecture |
|-----------|---------|-------------------|
| Noosphere Core | 3.1 | Noosphere Master Spec |
| Tidal Scheduler | 3.2 | PTA Layer 1, adapted |
| VRF Engine | 3.3 | PTA + Noosphere Section 15, extended |
| Predictive Delta Channel | 3.4 | PTA Layer 2 |
| Stigmergic Decay Channel | 3.5 | Noosphere Section 6.4 |
| Parcel Manager | 3.6 | Noosphere Section 9 + PTP (new) |
| G-Class Governance Engine | 3.7 | Noosphere Section 36 + tidal extensions |
| ETR Controller | 3.8 | New (from adversarial finding) |
| I-Confluence Prover | 3.9 | Locus Fabric, formalized |
| AASL Extension Layer | 3.10 | PTA + Noosphere AASL |
| Settlement Calculator | 3.11 | PTA Section 2.4, integrated |

---

## 2. Hard Gate Experiments

The Assessment Council mandated three hard gates as first deliverables. Each must be satisfied before the corresponding design area is finalized.

### 2.1 HG-1: Reconfiguration Storm Simulation

#### 2.1.1 Motivation

The Adversarial Analyst identified the Reconfiguration Storm (Attack 1, CRITICAL) as the most dangerous failure mode: simultaneous parcel reconfiguration degrades all five integration points (hash rings, VRF committees, predictive models, communication, governance availability), creating a window where the system has no efficient scheduling, no efficient communication, and stale verifier caches. The central question is whether recovery time exceeds the mean time between churn events at scale.

#### 2.1.2 Experiment Setup

**System configuration:**
- 1 Locus with 100 parcels, 10 agents per parcel (1,000 agents total)
- 20 active task types per parcel
- V = 150 virtual nodes per agent (bounded-loads hash rings)
- Predictive delta communication active with 70% accuracy activation threshold
- VRF verifier sets with 7-member committees
- Epoch length: 60 seconds (compressed for simulation; production is 1 hour)
- Parcel Transition Protocol (PTP) active with PREPARE/SWITCH/STABILIZE phases
- Staggering constraint: max 20% of parcels reconfiguring in any 10-epoch window
- Circuit breaker: halt all reconfigurations if >30% of parcels in TRANSITIONING state

**Churn injection profiles (run each independently):**

| Profile | Description | Severity |
|---------|-------------|----------|
| P1-MILD | 10% agent departure uniformly distributed across parcels | Baseline |
| P2-MODERATE | 20% agent departure concentrated in 30% of parcels | Moderate stress |
| P3-SEVERE | 30% agent departure concentrated in 50% of parcels | Design limit |
| P4-EXTREME | 30% agent departure + 15% agent arrival (simultaneous churn) | Beyond design limit |
| P5-CASCADING | P3, then another 15% departure 5 epochs after initial event | Double-hit scenario |
| P6-REPEATED | 10% churn every 8 epochs for 50 epochs | Sustained stress |

#### 2.1.3 Procedure

For each churn profile:

1. **Run system to steady state** (50 epochs). Record baseline metrics: scheduling throughput, communication bandwidth, verification committee availability, predictive model accuracy across all parcels.

2. **Inject churn event** at epoch 50. The PTP activates:
   - **PREPARE phase** (1 epoch): Bi-timescale controller announces reconfiguration. Agents freeze predictive model updates, cache VRF sets, queue outbound surprise signals. Hash rings continue on old configuration.
   - **SWITCH phase** (epoch boundary): Simultaneous hash ring reconstruction, VRF set invalidation/recomputation, queued signal flush, predictive models marked TRANSITIONING.
   - **STABILIZE phase** (2-5 epochs): Bounded-loads hash rings provide correct assignments immediately. No predictive optimization. Models bootstrap from Compact Transfer Vectors.

3. **Measure recovery trajectory** across all five integration points:

| Integration Point | Metric | Measurement Method |
|-------------------|--------|-------------------|
| IP-1: Hash Rings | Time to complete ring reconstruction for all affected parcels | Wall-clock from SWITCH start to all rings operational |
| IP-1: Hash Rings | Load imbalance (max/avg) during and after reconstruction | Per-epoch load ratio measurement |
| IP-2: VRF Committees | Time to recompute all pending verifier sets | Wall-clock from set invalidation to all sets recomputed |
| IP-2: VRF Committees | Committee quality (diversity score) during recovery | Diversity metric per committee, averaged |
| IP-3: Predictive Delta | Fraction of agents in cold-start mode per epoch | Count agents in TRANSITIONING or STANDARD mode |
| IP-3: Predictive Delta | Communication bandwidth relative to steady state | Total bytes per epoch / baseline bytes |
| IP-4: Governance | Governance channel availability | Fraction of governance agents reachable on dedicated channel |
| IP-5: AASL | TDF/TSK re-serialization latency | Wall-clock for AASL re-encoding |
| Combined | Scheduling throughput relative to steady state | Tasks completed per epoch / baseline |
| Combined | Epochs until >90% of agents exit TRANSITIONING | Count from SWITCH to threshold crossing |

4. **Record combined recovery time**: the number of epochs from churn injection until all five integration points return to within 20% of steady-state metrics.

5. **Run 100 trials per profile** with different random seeds for agent departure selection.

#### 2.1.4 Success Criteria

| Criterion | Threshold | Applies To |
|-----------|-----------|-----------|
| Combined recovery time (median) | < 5 epochs | P1-P3 |
| Combined recovery time (99th percentile) | < 10 epochs | P1-P3 |
| Combined recovery time (median) | < 8 epochs | P4-P5 |
| No cascading failure | 0% of runs where >50% parcels enter TRANSITIONING simultaneously | P1-P5 |
| Scheduling throughput floor | > 60% of steady state during worst epoch | P1-P4 |
| Communication bandwidth ceiling | < 5x steady state during worst epoch | P1-P4 |
| Governance channel availability | > 95% throughout recovery | P1-P5 |
| Sustained stress stability | System does not enter permanent degradation over 50 epochs | P6 |
| Circuit breaker activation | Triggers correctly when >30% parcels in TRANSITIONING | P4-P5 |

#### 2.1.5 Kill Criteria

- **KILL-HG1-A:** Cascading failure (>50% parcels in TRANSITIONING simultaneously) occurs in >5% of simulation runs with P3 (max 30% concurrent churn). Architecture requires fundamental PTP redesign.
- **KILL-HG1-B:** Combined recovery time exceeds 10 epochs in >10% of runs with P3. Recovery mechanism is too slow for the churn rates the system must handle.
- **KILL-HG1-C:** Under P6 (sustained 10% churn every 8 epochs), the system enters permanent degradation (never returns to >80% steady-state throughput). The architecture cannot handle sustained moderate churn.

#### 2.1.6 Fallback Plan

If HG-1 fails on kill criteria, evaluate:
1. **Dual-Mode Fabric (C3-B concept):** Add an explicit degraded-but-stable operating mode where the system pre-emptively drops to pure stigmergic communication and round-robin scheduling during mass churn, then gradually re-enables optimizations.
2. **Tighter staggering:** Reduce the 20% concurrent reconfiguration cap to 10%.
3. **Priority-based reconfiguration:** Only reconfigure the most-impacted parcels first, letting others absorb temporary suboptimality.

---

### 2.2 HG-2: Bounded-Loads Hash Ring Validation

#### 2.2.1 Motivation

The Adversarial Analyst identified small-ring load imbalance (Attack 2, HIGH) as a fundamental tension: typical parcels have 5-15 agents, and standard consistent hashing produces O(log N / log log N) load imbalance at these sizes. The bounded-loads variant (Mirrokni, Thorup, Wieder, SODA 2018) with virtual node inflation is the proposed solution.

#### 2.2.2 Experiment Setup

**Implementation:** Bounded-loads consistent hashing with configurable epsilon parameter (maximum fractional overload above average).

**Virtual node inflation policy:**
```
V(N) = max(150, ceil(1000 / N))
```
Where N is the number of agents in the parcel.

| N (agents) | V (virtual nodes per agent) | Total ring entries | Epsilon |
|-----------|---------------------------|-------------------|---------|
| 5 | 200 | 1,000 | 0.25 |
| 10 | 150 | 1,500 | 0.15 |
| 20 | 150 | 3,000 | 0.10 |
| 50 | 150 | 7,500 | 0.05 |
| 100 | 150 | 15,000 | 0.05 |
| 500 | 150 | 75,000 | 0.03 |
| 1,000 | 150 | 150,000 | 0.02 |
| 5,000 | 150 | 750,000 | 0.01 |
| 10,000 | 150 | 1,500,000 | 0.01 |

**Task distribution models:**
- UNIFORM: tasks hashed uniformly across the key space
- SKEWED: 80% of tasks map to 20% of the key space (Zipf distribution, alpha=1.0)
- CLUSTERED: tasks arrive in bursts targeting adjacent key ranges
- ADVERSARIAL: tasks specifically target load imbalance via key selection

#### 2.2.3 Procedure

For each (N, distribution) pair:

1. **Initialize** bounded-loads hash ring with V(N) virtual nodes per agent and the specified epsilon.
2. **Generate 100,000 task assignments** from the specified distribution.
3. **Measure load per agent**: count of tasks assigned to each agent.
4. **Compute metrics:**
   - max_load / avg_load ratio
   - min_load / avg_load ratio
   - Standard deviation of load distribution
   - Gini coefficient of load distribution
5. **Measure churn cost**: remove 1 agent, then add 1 agent. Count the number of task reassignments (key remappings). Compare to standard consistent hashing.
6. **Measure lookup latency**: time for 10,000 hash ring lookups. Report p50, p95, p99.
7. **Run 1,000 trials** per configuration with different random seeds.

Additionally, sweep epsilon from 0.01 to 0.50 in steps of 0.01 for N=5, N=10, N=50, N=100 to find the optimal epsilon per parcel size class.

#### 2.2.4 Success Criteria

| Criterion | Threshold | Applies To |
|-----------|-----------|-----------|
| max/avg load ratio (median across trials) | < 1.15 | N >= 5, all distributions |
| max/avg load ratio (median) | < 1.05 | N >= 100, all distributions |
| max/avg load ratio (99th percentile) | < 1.25 | N >= 10, UNIFORM + SKEWED |
| Churn cost increase vs standard consistent hashing | < 30% additional remappings | All N |
| Lookup latency p99 | < 100 microseconds | All N up to 10,000 |
| Ring reconstruction time for full parcel | < 50 ms | N <= 100, V = V(N) |
| Ring reconstruction time for full parcel | < 500 ms | N = 10,000, V = 150 |

#### 2.2.5 Kill Criteria

- **KILL-HG2-A:** max/avg load ratio exceeds 1.25 for any N >= 10 under UNIFORM or SKEWED distributions in >5% of trials. The bounded-loads algorithm does not provide sufficient balance at typical parcel sizes.
- **KILL-HG2-B:** max/avg load ratio exceeds 1.15 for N >= 5 under UNIFORM distribution in >10% of trials, even after epsilon optimization. Small parcels cannot be adequately load-balanced with this approach.
- **KILL-HG2-C:** Churn cost exceeds 50% additional remappings vs standard consistent hashing for any N. The reconfiguration overhead is too high for the parcel transition protocol.

#### 2.2.6 Fallback Plan

If HG-2 fails:
1. **Power-of-two-choices:** Replace hash rings with power-of-two-choices assignment (hash to 2 candidates, pick the less loaded). Better load balance but loses determinism unless the load state is shared.
2. **Rendezvous hashing:** Use highest random weight (HRW) hashing which has better small-N behavior. Higher lookup cost O(N) but N is small in parcels.
3. **Hybrid:** Use bounded-loads hash rings for N >= 20, round-robin with epoch-seeded permutation for N < 20.

---

### 2.3 HG-3: Emergency Tidal Rollback (ETR) Feasibility

#### 2.3.1 Motivation

The Adversarial Analyst identified Emergency Governance Deadlock (Attack 5, CRITICAL) as a fundamental risk: a buggy tidal function version could degrade scheduling for 72+ hours while standard G-class governance grinds through its discussion period. The ETR mechanism provides a fast path for reverting to a known-good tidal version.

#### 2.3.2 ETR Mechanism Design

**Three Automated Triggers (any one sufficient):**

| Trigger | ID | Detection Source | Condition | Detection Latency |
|---------|-----|-----------------|-----------|-------------------|
| Scheduling Skew | ETR-T1 | Sentinel Graph | max_parcel_load / avg_parcel_load > 2.0 across 3+ parcels within a single locus, sustained for 2 consecutive epochs | 2 epochs |
| Verification Starvation | ETR-T2 | Sentinel Graph | Any locus has zero verifier sets computed for > 1 epoch (no verification possible) | 1 epoch |
| Settlement Divergence | ETR-T3 | Settlement Calculator | > 5% of agents compute different settlement amounts from the same inputs (tidal function nondeterminism) | 1 epoch (detected at settlement boundary) |

**Trigger Detection Protocol:**

```
For each epoch E:
  Sentinel Graph computes:
    skew_metric(locus) = max over parcels(load) / avg over parcels(load)
    starvation_flag(locus) = (verifier_sets_computed == 0)
    divergence_metric = count(agents with different settlement) / total agents

  If skew_metric(L) > 2.0 for 3+ parcels in L for 2 consecutive epochs:
    EMIT ETR_TRIGGER(type=ETR-T1, locus=L, evidence=skew_data)

  If starvation_flag(L) == true for > 1 epoch:
    EMIT ETR_TRIGGER(type=ETR-T2, locus=L, evidence=starvation_data)

  If divergence_metric > 0.05:
    EMIT ETR_TRIGGER(type=ETR-T3, evidence=divergence_data)
```

**ETR Voting Protocol:**

1. **Proposal.** Upon receiving an ETR_TRIGGER, any 3 governance agents may co-sign an ETR_PROPOSAL specifying: trigger evidence, the target tidal function version to revert to (most recent previously-verified version), and proposed activation epoch (next epoch boundary).

2. **Propagation.** The ETR_PROPOSAL is broadcast on the **dedicated governance channel**, which is independent of the tidal-scheduled data plane. This channel uses a simple reliable broadcast protocol over a persistent mesh of governance agents, with no dependency on parcel topology or hash ring scheduling. The governance channel is always-on and does not use predictive delta communication.

3. **Voting.** Each active governance agent receives the proposal and votes YES or NO. Votes are propagated on the same dedicated governance channel. The voting window is **2 epochs** from proposal broadcast.

4. **Threshold.** ETR requires **90% instant supermajority** of active governance agents (agents that have voted on any governance action in the last 50 epochs). No discussion period.

5. **Activation.** If 90% YES votes are received within the voting window:
   - At the next epoch boundary, all agents switch to the reverted tidal function version.
   - The reverted version operates under a **governance hold**: no new tidal version proposals may be submitted for 10 epochs (cooling period).
   - The standard G-class process evaluates the failed version and proposes a replacement.

6. **Failure to reach threshold.** If <90% YES within the voting window, the ETR fails. The system continues on the current version. A new ETR may be proposed after 3 epochs. After 3 failed ETR attempts for the same trigger, the threshold drops to 80% for the 4th attempt.

7. **Constitutional protection.** The ETR mechanism itself is constitutionally protected: ETR thresholds, trigger conditions, and quorum requirements can only be modified by G-class constitutional consensus (75% supermajority with 72-hour discussion).

**Governance Agent Obligations:**

- Governance agents must maintain always-on voting capability as a condition of governance participation.
- Agents that fail to vote on 2 consecutive ETR proposals lose governance standing for 50 epochs.
- The dedicated governance channel has a heartbeat protocol: governance agents must respond to heartbeat pings within 30 seconds. Agents that miss 5 consecutive heartbeats are marked INACTIVE and excluded from the supermajority denominator.

#### 2.3.3 Experiment Setup

**System configuration:**
- 500 agents, 50 governance agents (10% governance participation rate)
- 10 loci, 50 parcels total
- Dedicated governance channel simulated with configurable latency (50ms-500ms per message)
- Tidal scheduling active on data plane

**Bug injection scenarios:**

| Scenario | ID | Bug Type | Expected Trigger |
|----------|----|----------|-----------------|
| S1 | Load Skew Bug | Tidal function produces 3x load on specific hash range | ETR-T1 (scheduling skew) |
| S2 | Verifier Starvation Bug | Tidal function excludes a verifier capability class | ETR-T2 (verification starvation) |
| S3 | Nondeterminism Bug | Tidal function uses floating-point operation with platform-dependent rounding | ETR-T3 (settlement divergence) |
| S4 | Subtle Performance Bug | 20% load imbalance (below ETR-T1 threshold) | None (should NOT trigger ETR) |
| S5 | Combined | S1 + governance channel degradation (20% message loss) | ETR-T1 with degraded comms |
| S6 | Rapid Trigger | S2 with immediate locus-wide impact | ETR-T2 (fast detection) |

#### 2.3.4 Procedure

For each scenario:

1. **Run to steady state** (20 epochs).
2. **Deploy buggy tidal version** at epoch 20 via simulated G-class governance approval.
3. **Measure detection latency**: epochs from bug deployment to ETR_TRIGGER emission.
4. **Measure proposal latency**: epochs from trigger to ETR_PROPOSAL broadcast.
5. **Measure voting latency**: epochs from proposal to 90% threshold crossing (or failure).
6. **Measure activation latency**: epochs from approval to all agents operating on reverted version.
7. **Measure total rollback time**: epochs from bug deployment to stable operation on reverted version.
8. **Measure system degradation**: scheduling throughput, verification throughput, communication bandwidth during the rollback period.
9. **Run 200 trials** per scenario.

#### 2.3.5 Success Criteria

| Criterion | Threshold | Applies To |
|-----------|-----------|-----------|
| Total rollback time (median) | <= 3 epochs | S1, S2, S3, S6 |
| Total rollback time (99th percentile) | <= 5 epochs | S1, S2, S3, S6 |
| Detection latency | <= 2 epochs | S1, S2, S3 |
| Voting success rate | >= 95% of trials reach 90% threshold | S1, S2, S3, S6 |
| False positive rate | 0% ETR triggers | S4 |
| Degraded governance recovery | Rollback within 5 epochs | S5 |
| System throughput during rollback | > 50% of steady state | S1-S3 |
| Post-rollback recovery | Full steady state within 3 epochs of version revert | S1-S3, S6 |

#### 2.3.6 Kill Criteria

- **KILL-HG3-A:** Total rollback time exceeds 10 epochs in any scenario (S1-S3, S6) in >5% of trials. The ETR mechanism is too slow.
- **KILL-HG3-B:** Voting fails to reach 90% threshold in >20% of trials for S1-S3 (non-degraded governance). The supermajority requirement is too high.
- **KILL-HG3-C:** ETR requires manual intervention (human governance override) in any trial. The mechanism must be fully automated once triggered.
- **KILL-HG3-D:** False positives occur (ETR triggers for S4 where no rollback is needed). Trigger thresholds are miscalibrated.

#### 2.3.7 Fallback Plan

If HG-3 fails:
1. **Lower threshold:** Reduce ETR supermajority from 90% to 80%. Risk: increases potential for abuse.
2. **Automated rollback without vote:** If all 3 trigger conditions fire simultaneously, execute automatic rollback via Sentinel Graph authority with no governance vote. Requires constitutional protection against abuse.
3. **Dual-version operation:** Instead of full rollback, run both old and new versions in parallel (overlap mode from PTA Tidal Version Manager). Agents that detect anomalies switch to the old version individually (Schelling-point fallback).

---

## 3. Component Architecture

### 3.1 Noosphere Core (Epistemic Fabric)

**Purpose:** The foundational epistemic coordination substrate. Manages the verification membrane, claim classification, knowledge persistence, and the constitutional protection framework.

**Inputs:**
- Claims (CLM) from agents
- Attestations (ATT) from verifier committees
- Governance directives (GOV) from G-class consensus
- Locus/Parcel topology from Parcel Manager

**Outputs:**
- Membrane Certificates (MCT) for verified claims
- Bundles (BDL) for knowledge persistence
- Classification Seals (CLS) for claim routing
- Membrane Quality Index (MQI) metrics to Sentinel Graph
- Supersession Records (SUP) for knowledge evolution

**Interfaces:**
- `verify_claim(CLM, committee: [AgentID]) -> MCT | Rejection`
- `classify_claim(CLM) -> CLS`
- `check_contradiction(CLM, knowledge_graph) -> [CTD]`
- `compute_MQI(locus) -> MQI_metrics`
- `re_verify_sample(epoch) -> [CLM]` (continuous re-verification)

**Failure Modes:**
- *Membrane drift:* MQI detects degradation. Response: conservative mode, then lockdown (Noosphere Section 19).
- *Classification gate error:* Structural check + independent classifier provides defense-in-depth. If both fail, continuous re-verification catches misclassified claims.
- *Verifier committee corruption:* Deep diversity enforcement (4 rules + weight cap) + anti-correlation audit via Sentinel Graph. VRF dual defense (Section 3.3) prevents committee shopping.

**Dependencies:** VRF Engine (verifier selection), Parcel Manager (topology), Sentinel Graph (anomaly detection), AASL Extension Layer (type system).

---

### 3.2 Tidal Scheduler

**Purpose:** Provides deterministic, O(1) per-agent task scheduling within parcels using bounded-loads consistent hash rings. This is PTA Layer 1, scoped to operate within the Noosphere's parcel boundaries.

**Inputs:**
- `agent_roster`: current set of registered agents with virtual node mappings (from Capacity Snapshot Service)
- `tidal_version`: active tidal function version definition (from G-Class Governance Engine)
- `parcel_topology`: current parcel assignments (from Parcel Manager)
- `epoch`: integer epoch counter (from Epoch Clock)

**Outputs:**
- `assignment(agent_id, task_type, epoch)`: deterministic task assignment
- `substitution_list(agent_id)`: ordered fallback agents from hash ring neighbors
- `settlement_boundary`: boolean indicating settlement epoch

**Internal Structure:**
- **Epoch Clock:** NTP-synchronized monotonic counter. Tolerance: 500ms. Persistent drift triggers substitution.
- **Hash Ring Manager:** One bounded-loads consistent hash ring per (parcel, task_type) pair. Virtual node inflation: V(N) = max(150, ceil(1000/N)). Epsilon parameter: configurable per parcel size class (see HG-2 results).
- **Scheduling Resolver:** Translates hash ring outputs into concrete agent work schedules. Handles multi-task-type conflict resolution via priority-based shedding.

**Failure Modes:**
- *Hash ring inconsistency (agents have different rosters):* Produces suboptimal but not incorrect assignments. Resolves at next epoch boundary.
- *Epoch clock drift:* Agent generates timing surprises. Persistent drift treated as agent failure; substitution list activates.
- *Parcel reconfiguration:* PTP Phase 2 (SWITCH) reconstructs all rings atomically at epoch boundary. Degraded scheduling during STABILIZE phase uses bounded-loads rings (correct immediately, not yet optimized by predictive layer).

**Dependencies:** Capacity Snapshot Service, G-Class Governance Engine (tidal version), Parcel Manager.

---

### 3.3 VRF Engine (Dual Defense)

**Purpose:** Computes verifier sets for claims using ECVRF (RFC 9381) with two layered defenses against committee manipulation: commit-reveal protocol and pre-stratified diversity pools.

This is the component where the user's critical design direction is implemented. Both mechanisms must work together.

**Defense Layer 1: Commit-Reveal Protocol**

Prevents grinding the claim hash to shop for favorable committees.

1. **Registration-time commitment.** When an agent registers as a potential verifier, it commits a hash of its diversity attributes: `H(training_lineage || methodology_family || temporal_bucket || region || nonce)`. The commitment is stored on-chain at registration time, before any VRF seed is known.

2. **Attribute lock.** Committed attributes are locked for a minimum of 100 epochs after commitment. Attribute changes require a 50-epoch cooling period during which the agent is excluded from verifier eligibility.

3. **Claim commitment.** Claims must be committed (claim hash published) before the epoch in which they will be verified is known. The claim hash determines the VRF output, so the adversary must commit to a claim before learning which epoch's seed will select its committee. This imposes a 1-epoch delay between claim submission and verification scheduling.

4. **VRF seed rotation.** VRF seeds rotate every epoch. The seed for epoch E is derived from: `seed_E = VRF(governance_randomness_beacon, E)`. No agent can predict the seed for epoch E+2 during epoch E.

**Defense Layer 2: Pre-Stratified Diversity Pools**

Prevents exploiting the diversity filtering step. This is the user's addition that works alongside commit-reveal.

1. **Pool stratification.** At each epoch boundary, the eligible verifier population is pre-stratified into diversity pools based on their committed attributes:
   - **Lineage pools:** grouped by training data lineage hash
   - **Methodology pools:** grouped by methodology family
   - **Temporal pools:** grouped by model recency (recent vs stable)
   - **Regional pools:** grouped by declared region

2. **Balanced sampling.** VRF committee selection does not draw from the undifferentiated verifier pool. Instead, it draws from pre-constructed strata:
   ```
   For a committee of size K:
     Select ceil(K/4) from lineage diversity stratum
     Select ceil(K/4) from methodology diversity stratum
     Select ceil(K/4) from temporal diversity stratum
     Select remaining from regional diversity stratum

     Within each stratum, use VRF output to select specific agents
     Dedup: if an agent is selected from multiple strata, retain
       first selection, resample from that stratum
   ```

3. **Anti-optimization defense.** Because the strata are pre-constructed from committed attributes, an adversary who registers Sybil identities with "maximally diverse" attributes is spread across multiple pools rather than concentrated in one. The adversary's per-pool representation is proportional to their fraction of the total pool, not amplified by diversity optimization.

4. **Sentinel Graph monitoring.** The Sentinel Graph tracks:
   - Agents whose diversity attributes are "too uniformly distributed" across all dimensions (statistically unlikely for honest agents)
   - Committee co-occurrence patterns that exceed random baseline
   - Attribute distributions within strata that become suspiciously uniform

**Combined Flow:**

```
Registration:
  Agent commits H(diversity_attributes)
  Attributes locked for 100 epochs
  Agent added to pre-stratified pools based on committed attributes

Claim Submission:
  Agent publishes claim_hash at epoch E
  Verification scheduled for epoch E+1 (1-epoch delay)

Committee Selection (epoch E+1):
  seed = VRF(beacon, E+1)
  For each stratum:
    candidates = agents in stratum with sufficient stake/reputation
    selected = VRF_select(seed, claim_hash, candidates, quota)
  committee = deduplicated union of selected agents
  Apply 15% weight cap per verifier

Verification:
  Committee verifies claim through class-specific pathway
  Attestations collected, membrane certificate issued or rejected
```

**Inputs:**
- `claim_hash`: hash of the claim to verify
- `epoch`: verification epoch
- `vrf_seed`: current VRF seed from governance randomness beacon
- `stratified_pools`: pre-computed diversity strata
- `committed_attributes`: registry of all agents' committed diversity attributes

**Outputs:**
- `verifier_set`: ordered list of selected verifier agent IDs
- `vrf_proof`: cryptographic proof of correct derivation
- `stratum_assignments`: which stratum each verifier was drawn from

**Failure Modes:**
- *Insufficient verifiers in a stratum:* Relax stratum quota; draw more from other strata. If total eligible verifiers below minimum committee size, defer verification to next epoch.
- *VRF seed not yet available:* Agent cannot compute verifier sets. Wait for beacon. Bounded delay: seed available within 1 epoch.
- *Sybil cluster detected:* Sentinel Graph flags cluster. Flagged agents temporarily excluded from pools. Governance investigation initiated.

**Dependencies:** Governance Randomness Beacon, Agent Registry (committed attributes), Sentinel Graph.

---

### 3.4 Predictive Delta Channel

**Purpose:** Intra-parcel communication layer that maintains lightweight linear predictive models of each neighbor's behavior, communicating only when prediction error exceeds an adaptive threshold.

**Inputs:**
- `neighbor_list`: direct neighbors within the same parcel
- `tidal_schedule`: expected schedule for each neighbor (from Tidal Scheduler)
- `neighbor_observations`: observed behavior during the epoch

**Outputs:**
- `surprise_signals`: delta-encoded prediction errors exceeding threshold (SRP type)
- `communication_mode`: per-neighbor {STANDARD, TRANSITIONING, PREDICTIVE}
- `prediction_accuracy`: rolling accuracy metric per neighbor

**Internal Structure:**
- **Model Store:** One linear model per neighbor. Parameters: behavioral weights, accuracy metric, 10-epoch error history.
- **Threshold Adapter:** Accuracy-gated tightening, non-stationarity loosening, hysteresis guard.
- **Cold-Start Manager:** Standard messaging fallback. Activation threshold: 70% accuracy. Progressive switch to predictive mode.
- **Predictive Context Transfer (PCT):** When agents cross parcel boundaries, serialize model state into Compact Transfer Vector (CTV): `(model_weights, accuracy_metric, last_10_epoch_error_history, communication_mode)` per former neighbor. New neighbors bootstrap from CTV + behavioral profile prior.

**Failure Modes:**
- *Model divergence:* Epoch-boundary recalibration detects. Model reset to cold-start for that neighbor.
- *Threshold oscillation:* Hysteresis guard prevents. Threshold must remain stable for configurable epochs before adjustment.
- *All-neighbor failure:* If >50% of neighbor models in STANDARD mode, system operates on tidal backbone alone. No correctness impact.
- *Parcel reconfiguration:* PCT reduces cold-start from 10-15 epochs to 3-5 epochs. During transition, increased communication bandwidth (bounded by cascade limiter).

**Dependencies:** Tidal Scheduler, Parcel Manager (neighbor assignments), Capacity Snapshot Service.

---

### 3.5 Stigmergic Decay Channel

**Purpose:** Locus-scope coordination layer using typed, decaying signals. Provides passive coordination across parcel boundaries where the rich predictive models of the Delta Channel are not available.

**Signal Types:** `need | offer | risk | anomaly | attention_request | reservation | trend`

The `trend` type is an addition recommended by the Adversarial Analyst (Attack 10) to carry gradient information (direction and rate of change of SLV dimensions) rather than just threshold crossings.

**Decay Rule:** A signal is removed when `now() - reinforced_at > decay_tau` and `reinforcement_count` has not increased. Computed lazily at read time.

**Reinforcement Rule:** Duplicate `(type, scope, payload_hash)` signals increment `reinforcement_count` and reset TTL.

**Interaction with Predictive Delta:**
- **Promotion (predictive -> stigmergic):** When parcel-level predictive models detect sustained anomaly (surprise signals exceeding threshold for 3+ consecutive epochs from the same cause), the anomaly is automatically promoted to a locus-scope `risk` or `anomaly` signal with magnitude derived from aggregate prediction error. For CRITICAL safety class loci, promotion threshold is reduced to 1 epoch.
- **Incorporation (stigmergic -> predictive):** When a locus-scope signal is received, the predictive layer incorporates it as an exogenous input to all neighbor models within the receiving parcel.

**Dependencies:** Parcel Manager (parcel boundaries), Noosphere Core (signal type definitions).

---

### 3.6 Parcel Manager (3-Phase Transition Protocol)

**Purpose:** Manages elastic parcel boundaries within loci. Implements the Parcel Transition Protocol (PTP) that coordinates state changes across all integration points during reconfiguration.

**Bi-Timescale Controller:**
- **Slow loop:** Parcelization changes based on rolling access/conflict hypergraph analysis. Changes only when candidate plan beats current plan by margin exceeding migration debt and churn budget. Shadow planning for n windows before data moves.
- **Fast loop:** PI controller for routing weights, replica fanout, worker placement within parcel boundaries. Default gains: Kp = 0.05, Ki = 0.005.

**Parcel Transition Protocol (PTP):**

```
Phase 1: PREPARE (1 epoch)
  Controller announces reconfiguration to all agents in affected parcels
  Agents:
    - Freeze predictive model updates (predict but do not adapt)
    - Cache current VRF verifier sets
    - Enter communication buffer mode (queue outbound surprise signals)
    - Hash rings continue on old configuration

Phase 2: SWITCH (epoch boundary, atomic)
  All agents simultaneously:
    a) Reconstruct hash rings for new parcel topology
    b) Invalidate cached VRF sets, recompute with new eligible pool
    c) Flush queued surprise signals (re-route to new neighbors)
    d) Mark all predictive models as TRANSITIONING

  Atomicity: All agents have the same inputs (controller directive is
  B-class broadcast received during Phase 1). Same inputs + deterministic
  function = same outputs. No consensus required.

Phase 3: STABILIZE (2-5 epochs)
  Agents operate with:
    - Bounded-loads hash rings (correct immediately)
    - Standard-mode communication (no predictive optimization)
    - Predictive models bootstrapping from CTVs
  Completion: >90% of agents in new parcel exit TRANSITIONING state
```

**Reconfiguration Guards:**
- Minimum 10-epoch interval between reconfigurations of any single parcel
- Maximum 20% of parcels in a locus reconfiguring in any 10-epoch window
- Circuit breaker: halt all reconfigurations if >30% parcels in TRANSITIONING state

**Failure Modes:**
- *Circuit breaker activation:* Slow loop halted. Fast loop continues. Gains reduced 50%.
- *Cascading splits:* Staggering constraint prevents. If demand exceeds staggering budget, controller prioritizes most-impacted parcels.
- *Split-then-merge oscillation:* Detected within 20 epochs. Plan discarded. Halt 20 epochs.

**Dependencies:** Tidal Scheduler (hash ring reconstruction), VRF Engine (set recomputation), Predictive Delta Channel (model transfer), Noosphere Core (locus invariants).

---

### 3.7 G-Class Governance Engine

**Purpose:** Manages constitutional consensus for tidal function versions, membrane rule changes, and system parameter updates. Extends the Noosphere's existing G-class governance with tidal-specific capabilities.

**Standard Governance (Tidal Versions):**
- 75% supermajority of governance stake
- 72-hour discussion period for HIGH safety class
- Tidal function version proposals encoded as TDF (tidal definition) AASL type
- Version transition includes: overlap duration, activation epoch, rollback conditions
- The tidal function is itself a verified claim within the membrane (recursive closure, INV-7)

**Emergency Governance (ETR):**
- Delegated to ETR Controller (Section 3.8)

**Constitutional Protection:**
- No system parameter may reduce membrane verification depth
- No tidal function version may bypass G-class approval
- ETR mechanism thresholds require G-class constitutional consensus to modify
- The Feedback Controller is prohibited from adjusting membrane or governance parameters

**Failure Modes:**
- *Governance deadlock (26% blocking coalition):* ETR provides emergency bypass for scheduling emergencies. For non-scheduling governance, deadlock requires political resolution (not an architectural problem).
- *Governance participation below quorum:* Heartbeat protocol on dedicated channel. Inactive agents excluded from denominator after 5 missed heartbeats.

**Dependencies:** ETR Controller, Noosphere Core (membrane), Dedicated Governance Channel.

---

### 3.8 ETR Controller

**Purpose:** Implements the Emergency Tidal Rollback mechanism as specified in HG-3 (Section 2.3).

**Inputs:**
- ETR_TRIGGER events from Sentinel Graph
- Voting results from governance agents on dedicated channel
- Current and previous tidal function versions from G-Class Governance Engine

**Outputs:**
- ETR_PROPOSAL broadcasts on dedicated governance channel
- ETR_ACTIVATION directives at epoch boundary
- Governance hold enforcement (10-epoch cooling period)

**State Machine:**

```
MONITORING -> TRIGGERED -> PROPOSAL_ACTIVE -> VOTING -> {APPROVED, FAILED}

MONITORING:
  Listen for ETR_TRIGGER events from Sentinel Graph

TRIGGERED:
  Validate trigger evidence
  Wait for 3 governance agent co-signatures on ETR_PROPOSAL
  Timeout: 1 epoch. If no proposal, return to MONITORING.

PROPOSAL_ACTIVE:
  Broadcast ETR_PROPOSAL on dedicated governance channel
  Open voting window (2 epochs)

VOTING:
  Collect YES/NO votes
  If >= 90% YES of active governance agents: -> APPROVED
  If voting window expires without threshold: -> FAILED

APPROVED:
  Issue ETR_ACTIVATION for next epoch boundary
  All agents switch to reverted tidal version
  Enter governance hold (10 epochs)
  Return to MONITORING

FAILED:
  Log failure with evidence
  Cooldown 3 epochs before new ETR may be proposed
  Increment failure counter
  If failure_counter >= 3: reduce threshold to 80% for next attempt
  Return to MONITORING
```

**Failure Modes:**
- *Dedicated channel unavailable:* ETR cannot proceed. System continues on current version. This is the motivation for the dedicated channel -- it must be independent of tidal scheduling.
- *Trigger false positive:* S4 scenario in HG-3. Governance agents evaluate evidence and vote NO. System continues.
- *90% threshold unreachable:* After 3 failures, threshold drops to 80%. If still unreachable, system requires manual intervention (this is a KILL criterion for HG-3).

**Dependencies:** Sentinel Graph (trigger detection), Dedicated Governance Channel (vote propagation), Tidal Scheduler (version revert).

---

### 3.9 I-Confluence Prover

**Purpose:** Manages the proof obligations for M-class operation classification. Provides the cold-start bootstrap plan and maintains the proof library. Implements the provisional M-class mechanism.

**Proof Obligation:** An operation may be classified M-class (coordination-free) only after a machine-checked proof demonstrates that concurrent execution by any number of agents preserves all declared invariants of the locus in which it operates.

**Proof Toolchain:** TLA+ for initial model checking. Coq or F* for machine-checked proofs of critical operations. Ivy for automated invariant checking of protocol-level operations.

**Cold-Start Bootstrap Plan:** See Section 5 for the full plan.

**Provisional M-Class Mechanism:**

Operations that have empirical evidence of convergence (from simulation or testing) but lack formal proofs may be classified as **Provisional M-class** (M-prov):

- M-prov operations execute with M-class performance (coordination-free)
- Additional monitoring: Sentinel Graph tracks convergence violations per M-prov operation type
- If any convergence violation detected: automatic demotion to B-class, governance alert
- Formal proof required for promotion from M-prov to full M-class
- M-prov classification requires: 100+ epochs of convergence in simulation, 50+ epochs of convergence in production, zero detected violations

**Inputs:**
- Operation type definitions
- Locus invariant declarations
- Proof artifacts (TLA+ models, Coq proofs)
- Runtime convergence monitoring data from Sentinel Graph

**Outputs:**
- Operation class certification: {M, M-prov, B, X, V, G}
- Proof artifacts for certified operations
- Demotion alerts for M-prov violations
- Bootstrap library of pre-certified operations

**Dependencies:** Sentinel Graph (convergence monitoring), G-Class Governance Engine (proof library governance).

---

### 3.10 AASL Extension Layer

**Purpose:** Extends the Noosphere's AASL type system with four new types and five new AACP messages for tidal coordination.

**New Types (4):**

| Token | Object | Semantics |
|-------|--------|-----------|
| TDF | Tidal Definition | Complete tidal function version: hash ring config, VRF seed schedule, epoch parameters, task-type frequency bands. Submitted as normative claim for G-class governance. |
| TSK | Task Schedule | Deterministic computation output: agent assignments for a given epoch. Ephemeral (recomputable from TDF + roster). |
| SRP | Surprise Signal | Prediction error signal from the predictive delta layer. Carries: source agent, prediction error magnitude, model confidence, threshold, epoch. Distinct from SIG because it carries model-based semantics. |
| STL | Settlement Boundary | Settlement computation output: per-agent AIC deltas, compliance scores, settlement proof hash. Deterministic from shared inputs. |

**New AACP Messages (5):**

| Message | Direction | Purpose |
|---------|-----------|---------|
| TIDAL_VERSION_PROPOSE | Agent -> Governance | Submit a new TDF for G-class approval |
| TIDAL_VERSION_ACTIVATE | Governance -> All | Announce activation of approved TDF at specified epoch |
| SURPRISE_SIGNAL | Agent -> Parcel Neighbors | Delta-encoded SRP when prediction error exceeds threshold |
| ETR_PROPOSAL | Governance -> Governance | Emergency rollback proposal on dedicated channel |
| ETR_VOTE | Governance -> Governance | YES/NO vote on active ETR proposal |

**Type System Total:** 23 (existing) + 4 (new) = 27 AASL types. 17% expansion. Within sustainable protocol evolution bounds per Science Assessment.

**SRP vs SIG Decision:** SRP is a separate type (not a SIG subtype) because:
- SRP carries predictive-delta-specific fields (model confidence, threshold, prediction error vector) that have no meaning in the stigmergic signal context
- SRP routing is intra-parcel only; SIG routing is locus-scope
- Parsers can dispatch on type token without inspecting payload
- Trade-off accepted: type count increases by 1, but parsing is cleaner

**Dependencies:** Noosphere Core (existing AASL types), Tidal Scheduler (TSK generation), Predictive Delta Channel (SRP generation), Settlement Calculator (STL generation).

---

### 3.11 Settlement Calculator

**Purpose:** Computes deterministic AIC settlement amounts at epoch boundaries, integrating tidal compliance with the Noosphere's three-budget economic model.

**Settlement Formula:**

```
settlement(agent, epoch) =
  w_tidal * tidal_compliance(agent, epoch)
  + w_verify * verification_quality(agent, epoch)
  + w_resource * resource_efficiency(agent, epoch)

Where:
  tidal_compliance = fraction of scheduled tasks completed correctly
  verification_quality = attestation accuracy * method diversity bonus
  resource_efficiency = CSO utilization efficiency within owned slices

  w_tidal + w_verify + w_resource = 1.0
  Default weights: w_tidal = 0.4, w_verify = 0.4, w_resource = 0.2
```

**Inputs:**
- Tidal schedule for the epoch (from Tidal Scheduler)
- Event log: task completions, surprise signals, verification actions
- Economic parameters from tidal function version
- CSO utilization data

**Outputs:**
- `settlement_ledger`: map of agent_id -> AIC delta
- `compliance_scores`: map of agent_id -> compliance score [0.0, 1.0]
- `settlement_proof`: deterministic hash of all inputs and outputs

**Dependencies:** Tidal Scheduler (schedule data), Noosphere Core (verification data), CSO system (resource data), AIC Token Adapter (settlement delivery).

---

## 4. Integration Architecture

### 4.1 Data Flow Overview

```
+--------+     +------------------+     +------------------+
|  CIOS  | --> | Noosphere Locus  | --> | Tidal Scheduler  |
| (goals,|     | Router           |     | (hash rings per  |
|  roles)|     | (locus/parcel    |     |  parcel/task)    |
+--------+     |  assignment)     |     +--------+---------+
               +--------+---------+              |
                        |                         |
               +--------v---------+     +--------v---------+
               | VRF Engine       |     | Predictive Delta |
               | (verifier sets   |     | Channel          |
               |  with dual       |     | (intra-parcel    |
               |  defense)        |     |  surprise-only)  |
               +--------+---------+     +--------+---------+
                        |                         |
               +--------v---------+     +--------v---------+
               | Verification     |     | Stigmergic Decay |
               | Membrane         |     | Channel          |
               | (claim-class     |     | (locus-scope     |
               |  specific)       |     |  signals)        |
               +--------+---------+     +--------+---------+
                        |                         |
               +--------v---------+     +--------v---------+
               | Knowledge Cortex |     | Sentinel Graph   |
               | (verified memory)|     | (anomaly detect) |
               +--------+---------+     +--------+---------+
                        |                         |
               +--------v---------+     +--------v---------+
               | Settlement       |     | ETR Controller   |
               | Calculator       |     | (emergency       |
               | (AIC deltas)     |     |  rollback)       |
               +------------------+     +------------------+
                                                  |
                                        +---------v--------+
                                        | Dedicated Gov    |
                                        | Channel          |
                                        | (independent of  |
                                        |  data plane)     |
                                        +------------------+
```

### 4.2 VRF Engine Dual Defense Integration

The two VRF defense mechanisms interact as follows:

```
TIME ------>

Registration (one-time):
  Agent registers:
    1. Commits H(diversity_attributes) on-chain
    2. Attributes verified by registry
    3. Agent assigned to pre-stratified diversity pools
    4. 100-epoch attribute lock begins

Epoch E (claim submission):
  Claim C published with claim_hash
  VRF seed for epoch E+1 not yet known
  Adversary cannot compute future committee for C

Epoch E+1 (committee selection):
  Seed S_{E+1} = VRF(beacon, E+1)        [unpredictable at E]

  For committee of size K:
    Pool_lineage = agents grouped by committed lineage
    Pool_method  = agents grouped by committed methodology
    Pool_temporal = agents grouped by committed recency
    Pool_region  = agents grouped by committed region

    From Pool_lineage: VRF_select(S_{E+1}, claim_hash, Pool_lineage, K/4)
    From Pool_method:  VRF_select(S_{E+1}, claim_hash, Pool_method,  K/4)
    From Pool_temporal: VRF_select(S_{E+1}, claim_hash, Pool_temporal, K/4)
    From Pool_region:  VRF_select(S_{E+1}, claim_hash, Pool_region, rem)

    Deduplicate, apply 15% weight cap
    Result: committee with guaranteed diversity across all 4 dimensions

  Adversary analysis:
    - Cannot grind claim_hash (committed before seed known)
    - Cannot grind attributes (committed 100+ epochs before any seed)
    - Cannot concentrate Sybils in one pool (pools are pre-stratified)
    - Per-pool representation is proportional to pool fraction
    - Expected adversary advantage: <3% above stake-proportional baseline
```

### 4.3 Parcel Transition Protocol Interaction with Hash Rings

The PTP coordinates the Tidal Scheduler's hash ring reconstruction with all other integration point transitions:

```
Epoch E-1: PREPARE
  +------------------+     +------------------+     +------------------+
  | Tidal Scheduler  |     | VRF Engine       |     | Predictive Delta |
  | Rings: OLD config|     | Sets: CACHED     |     | Models: FROZEN   |
  | Status: RUNNING  |     | Status: ACTIVE   |     | Status: PREDICT  |
  +------------------+     +------------------+     | (no adapt)       |
                                                     +------------------+

Epoch E boundary: SWITCH (atomic)
  +------------------+     +------------------+     +------------------+
  | Tidal Scheduler  |     | VRF Engine       |     | Predictive Delta |
  | Rings: REBUILT   |     | Sets: RECOMPUTED |     | Models: TRANSIT  |
  | V(N_new) vnodes  |     | Pools: RE-STRAT  |     | CTVs: SENT       |
  | Status: ACTIVE   |     | Status: ACTIVE   |     | Status: STANDARD |
  +------------------+     +------------------+     +------------------+

Epochs E+1 to E+5: STABILIZE
  +------------------+     +------------------+     +------------------+
  | Tidal Scheduler  |     | VRF Engine       |     | Predictive Delta |
  | Rings: OPTIMIZING|     | Sets: NOMINAL    |     | Models: BOOTSTRAP|
  | Load balance: OK |     | Diversity: OK    |     | Accuracy: RISING |
  | Status: ACTIVE   |     | Status: ACTIVE   |     | Status: -> PRED  |
  +------------------+     +------------------+     +------------------+
```

Key interaction: During SWITCH, the hash ring reconstruction and VRF pool re-stratification must use the same agent roster snapshot. The PTP ensures this by having the PREPARE phase distribute the target roster to all agents before the SWITCH occurs. Since the roster is delivered as a B-class broadcast during PREPARE, all agents have identical inputs for the SWITCH computation.

### 4.4 Threshold Coordination (PTA Surprise vs Noosphere SLV)

The Science Assessment identified pathological interactions between PTA's surprise threshold and the Noosphere's SLV threshold (Attack 11). The integration architecture resolves this:

1. **Surprise rate feeds SLV.** The aggregate surprise rate within a parcel (count of SRP signals per epoch) becomes a 7th dimension of the SLV:
   ```
   SLV(parcel, t) = {
     pending_needs, pending_claims, dispute_count,
     lease_contention, active_agents, verification_lag,
     surprise_rate    // NEW: from Predictive Delta Channel
   }
   ```

2. **SLV constrains surprise threshold.** When SLV indicates known overload (any dimension above high threshold for 3+ epochs), the Predictive Delta Channel auto-loosens its surprise threshold by 20% for the affected parcel. This reduces signal flood during known stress without losing critical surprise information.

3. **Joint calibration.** The bi-timescale controller's fast loop jointly calibrates both thresholds as part of its PI control, treating surprise_rate as a controlled variable with target range.

---

## 5. I-Confluence Bootstrap Plan

### 5.1 The Cold-Start Problem

At system launch, no operations have I-confluence proofs. Without proofs, all operations default to B-class (broadcast) or X-class (serialized), negating the O(1) steady-state performance advantage of M-class. The bootstrap plan identifies operations that are OBVIOUSLY I-confluent from first principles and provides them as a starting library.

### 5.2 Obviously I-Confluent Operations (Bootstrap Set)

These operations are I-confluent by construction because their merge functions are inherently commutative, associative, and idempotent. The proofs are mechanical, not creative.

| # | Operation | Why Obviously I-Confluent | Proof Technique | Estimated Effort |
|---|-----------|--------------------------|-----------------|-----------------|
| 1 | **G-Counter increment** | Monotone increment per agent. Merge = max per agent. CRDT by definition. | TLA+ (trivial) | 4 hours |
| 2 | **G-Set add** | Set union. Add-only set. Merge = union. CRDT by definition. | TLA+ (trivial) | 4 hours |
| 3 | **LWW-Register write** | Last-writer-wins with total-order timestamps. Merge = latest. CRDT by definition. | TLA+ (trivial) | 4 hours |
| 4 | **OR-Set add/remove** | Observed-remove set. Each add tagged with unique ID. Remove only affects observed tags. CRDT by definition. | TLA+ (moderate) | 16 hours |
| 5 | **Signal emission** | Signals are append-only per issuer, merge by `(type, scope, payload_hash)` dedup with reinforcement_count increment. Commutative: order of signal arrival does not affect final state. | TLA+ | 8 hours |
| 6 | **Signal decay** | Time-based removal. Monotone with respect to time. Any two agents computing decay at the same wallclock time produce the same set of surviving signals. | TLA+ | 8 hours |
| 7 | **Reputation accumulation** | Multi-dimensional vector. Each dimension is a weighted running average. Update is commutative when the weight function depends only on the event, not the order. | TLA+ | 16 hours |
| 8 | **SLV computation** | Each SLV dimension is a count or aggregate derived from current parcel state. Recomputed from scratch each epoch. No merge needed -- recomputation is idempotent. | TLA+ (trivial) | 4 hours |
| 9 | **Capacity snapshot propagation** | Gossip-based with latest-epoch-wins merge. Merge = per-agent max-epoch snapshot. CRDT pattern. | TLA+ | 8 hours |
| 10 | **Idempotent claim state transition** | Claim state transitions (active -> provisional, provisional -> disputed) are monotone along the state lattice. Merge = max along lattice order. | TLA+ | 16 hours |
| 11 | **Evidence reference accumulation** | Append-only set of evidence references on a claim. G-Set pattern. | TLA+ (trivial) | 4 hours |
| 12 | **Attestation accumulation** | Append-only set of attestations on a claim. Each attestation is unique (one per verifier). G-Set pattern with natural dedup. | TLA+ | 8 hours |
| 13 | **Reinforcement count increment** | Monotone counter per signal. Merge = max. G-Counter pattern. | TLA+ (trivial) | 2 hours |
| 14 | **Contradiction edge creation** | Append-only edge set. Creating a contradiction edge between two claims is commutative -- the edge exists or it does not. G-Set pattern. | TLA+ | 8 hours |
| 15 | **Bundle utility score update** | Monotone update (utility only increases as new citations accumulate). Merge = max. | TLA+ | 4 hours |

**Bootstrap library total: 15 operations, estimated 106 person-hours of formal proof work.**

### 5.3 Expansion Strategy

From the bootstrap set, expand to more complex operations:

**Phase 1 expansion (months 1-4):** Operations built from compositions of bootstrap CRDTs:
- Heuristic family state management (composed of G-Set for edges + LWW-Register for champion)
- CSO local spend (monotone decrement within owned slice -- reducible to G-Counter)
- Reliance Permit lifecycle (state lattice -- reducible to monotone lattice transition)

**Phase 2 expansion (months 4-10):** Operations requiring non-trivial I-confluence analysis:
- Predictive model update (convergence depends on update commutativity -- needs analysis)
- Cross-parcel signal promotion (interaction between predictive and stigmergic layers)
- Cell assembly recruitment (threshold-based -- requires proof that concurrent recruitment preserves capacity constraints)

**Phase 3 expansion (months 10-18):** Operations where I-confluence is non-obvious:
- Fusion Capsule preparation (grant collection -- may not be I-confluent by nature, may remain X-class)
- Settlement computation (deterministic -- actually does not need I-confluence proof, it needs determinism proof)
- Tidal function evaluation (deterministic -- same)

### 5.4 Transition Protocol: X-class -> M-prov -> M-class

```
New operation type defined:
  Default classification: X-class (serialized, safe but expensive)

  If operation matches a known CRDT pattern:
    Rapid proof via template (< 1 week)
    Classification: M-class (fully certified)

  If operation has empirical convergence evidence:
    100+ epochs simulation convergence
    50+ epochs production convergence with monitoring
    Classification: M-prov (provisional, monitored)

    If convergence violation detected:
      Automatic demotion to B-class
      Governance alert, investigation

    If formal proof completed:
      Promotion to M-class (fully certified)

  If operation has no convergence evidence:
    Remains X-class until evidence accumulated
    B-class if bounded-commit pattern identified
```

---

## 6. Cross-Integration Failure Specification

This section addresses the Assessment Council's REQUIRED action (REQ-3) for formal specification of system behavior during simultaneous degradation across integration points.

### 6.1 Failure Combination Matrix

| Combination | Trigger | Behavior | Recovery Time Bound | Degraded-Mode Guarantee |
|-------------|---------|----------|--------------------|-----------------------|
| IP-1 x IP-2: Hash ring reconfig + VRF invalidation | Parcel split/merge | PTP Phase 2 handles atomically. Rings rebuilt and VRF sets recomputed from same roster snapshot. | 1 epoch (SWITCH) + 2-5 epochs (STABILIZE) | Correct scheduling (bounded-loads rings operational immediately) + correct verification (recomputed VRF sets) at degraded efficiency |
| IP-1 x IP-3: Hash ring reconfig + predictive model cold-start | Parcel split/merge | PTP Phase 2 resets models. PCT provides accelerated bootstrap. Communication spike bounded by cascade limiter. | 3-5 epochs for model convergence | Correct scheduling + standard-mode communication (no predictive optimization) |
| IP-2 x IP-4: VRF pool change + governance action | Tidal version update | Governance-approved TDF includes VRF seed schedule. VRF pool re-stratification occurs at activation epoch. Membrane security review is mandatory part of governance proposal. | 1 epoch (activation) | Continuous verification with new VRF parameters. Brief committee quality dip during pool restratification. |
| IP-3 x IP-4: Predictive degradation + governance latency | Tidal function bug causing widespread prediction failures | ETR mechanism (3 epoch detection + 2 epoch voting). Predictive layer degrades to standard messaging. | 5 epochs via ETR | Standard messaging (no prediction). Tidal backbone scheduling continues. |
| IP-4 x IP-5: Governance proposal + AASL encoding | TDF type governance | TDF AASL type is expressive enough for complete function definition. Governance expressiveness validated during Phase 1. | N/A (design-time concern) | Full function definition in AASL guaranteed by type design |
| ALL: Reconfiguration storm | Mass churn (30%+) | PTP + staggering + circuit breaker. See HG-1 simulation. | < 10 epochs (HG-1 success criterion) | Degraded but correct operation across all IPs. INV-6 maintained. |

### 6.2 Degraded Mode Specification

When the system enters degraded mode (circuit breaker activation, reconfiguration storm, ETR in progress), the following guarantees hold:

1. **Scheduling:** Bounded-loads hash rings provide correct task assignments with potentially stale rosters. Assignments are suboptimal but never incorrect.
2. **Communication:** Standard messaging replaces predictive delta. Higher bandwidth but guaranteed delivery.
3. **Verification:** VRF committees recomputed with available pool. Smaller pool may reduce diversity scores but verification never stops.
4. **Governance:** Dedicated channel independent of data plane. ETR voting always available.
5. **Knowledge persistence:** Membrane continues to gate claims. No unverified claims admitted during degradation.
6. **Economics:** Settlement computed on actual events. Degraded-mode penalties are not applied (agents are not penalized for system-level degradation).

### 6.3 Cross-Locus Failure Propagation

The Adversarial Analyst identified cross-locus cascade risk (Attack 1 extension). The defense:

1. **Locus isolation:** Each locus's PTP operates independently. A reconfiguration storm in locus A does not force reconfigurations in locus B.
2. **Fusion Capsule stall handling:** If a Fusion Capsule touches objects in a degraded locus, the capsule enters WAITING state. Expiry TTL prevents indefinite stall. If expired, the capsule is aborted and retried when the locus recovers.
3. **Cross-locus signal dampening:** Locus-scope signals that propagate to other loci carry a `source_locus_health` field. Receiving loci discount signals from degraded loci by 50% in their SLV computation.

---

## 7. Scale Architecture

### 7.1 Phase 1: 1-100 Agents (Development/Testing)

**Topology:** 1-3 loci, 1-5 parcels per locus, 5-20 agents per parcel.
**What works at this scale:** All components can be tested. Hash rings, VRF, predictive delta, PTP, ETR, settlement.
**What is different:** Gossip convergence is trivial. Governance participation is 100%. Diversity pools may be too small for meaningful stratification.
**Bottlenecks:** Formal proof generation is the gating factor (human effort, not compute).
**Needed:** Bootstrap proof library (Section 5.2), single-locus integration tests, HG-1/HG-2/HG-3 simulation experiments.

### 7.2 Phase 2: 100-1K Agents (Initial Deployment)

**Topology:** 10-50 loci, 2-20 parcels per locus, 5-50 agents per parcel.
**What changes:** Gossip convergence time becomes non-trivial (O(N log N) messages per epoch boundary). Diversity pools become meaningful. Cross-locus operations (Fusion Capsules) become common. PTP tested under real churn.
**Bottlenecks:** Capacity Snapshot Service at 1K agents: ~1K snapshots per epoch via gossip. Manageable but requires tuning of gossip fanout and TTL.
**Needed:** Multi-locus PTP validation. VRF diversity pool sizing. Economic simulation scenarios E1-E2.

### 7.3 Phase 3: 1K-10K Agents (Primary Target)

**Topology:** 50-500 loci, 5-50 parcels per locus, 5-50 agents per parcel (total: 250-25,000 parcels).
**What changes:** Stigmergic signal propagation across 1,000+ parcels requires hierarchical aggregation. Capacity snapshots at 10K agents: ~10K snapshots per epoch (~170K gossip messages). Governance participation rate drops below 100% (realistic governance dynamics). Sentinel Graph monitoring cost grows linearly.
**Bottlenecks:**
- Capacity Snapshot gossip convergence at 10K agents. Mitigation: hierarchical aggregation within loci -- parcel summaries propagate to locus level, locus summaries propagate to cross-locus level.
- Sentinel Graph computational cost for anti-correlation audit: O(V^2) where V is verifier count. At 1K verifiers, the matrix is 1M entries. Mitigation: approximate methods (locality-sensitive hashing for correlation detection).
- Governance quorum at 10K agents with 10% governance rate: 1K governance agents. 90% ETR threshold = 900 agents must vote within 2 epochs on dedicated channel. Requires robust governance channel infrastructure.
**Needed:** Hierarchical snapshot aggregation. Approximate Sentinel Graph methods. Governance channel stress testing. Economic scenarios E1-E6.

### 7.4 Phase 4: 10K-100K Agents (Aspiration)

**Topology:** 500-5,000 loci, 10-100 parcels per locus, 5-50 agents per parcel (total: 5,000-500,000 parcels).
**What changes:**
- Cross-locus operations become a significant fraction of all operations.
- Stigmergic decay time constants must be retuned for propagation across 10,000+ parcels. Decay tau at locus scope may need to be longer (slower decay) to allow signals to propagate before expiring.
- Capacity Snapshot at 100K: ~100K snapshots, ~1.7M gossip messages per epoch. Requires structured gossip with hierarchical aggregation.
- Governance at 100K: 10K governance agents. ETR 90% threshold = 9K agents. Dedicated channel must handle 9K votes within 2 epoch windows.
- Sentinel Graph: O(V^2) for 10K verifiers = 100M entries. Approximate methods mandatory.
- Cross-region federation latency must be less than epoch length.
**Open questions (research):**
- Does the O(1) per-agent overhead claim hold at 100K? Each agent computes local hash ring lookups (O(log V) per task type) but the number of task types may grow with system scale.
- Does the hierarchical snapshot aggregation introduce sufficient staleness to cause widespread roster divergence?
- Can the governance channel sustain 9K concurrent votes with sub-epoch latency?
**Needed:** Full formal verification suite (TLA+ for all critical invariants). Cross-region federation protocol. 100K-agent simulation. Economic scenarios E1-E7. Production deployment readiness assessment.

---

## 8. Security Architecture

### 8.1 Threat Model

The Tidal Noosphere operates under the following threat model:

| Threat Class | Attacker Capability | Defense |
|-------------|-------------------|---------|
| **Byzantine agents** (< 1/3 per parcel) | Arbitrary behavior: send conflicting messages, withhold responses, produce incorrect outputs | BFT quorum in replica groups. VRF prevents prediction of assignments. Settlement slashing for detected misbehavior. |
| **Sybil identities** | Create many low-cost identities to gain disproportionate influence | Stake requirement. Concave PC issuance. Diversity attribute commitment (100-epoch lock). Sentinel Graph detection. |
| **Committee shopping** | Withdraw and resubmit claims to get favorable verifier committees | Claim commitment: claim_hash published before verification epoch known. 1-epoch delay prevents shopping. |
| **Diversity grinding** | Register Sybils with optimized diversity attributes | Pre-stratified pools: Sybils distributed across pools proportionally. Commit-reveal: attributes locked before VRF seeds known. Sentinel Graph: flags "too perfect" diversity distributions. |
| **Governance capture** (26% blocking) | Block governance proposals by controlling >25% of governance stake | ETR provides bypass for scheduling emergencies (90% threshold, not 75%). Standard governance deadlock requires political resolution. Governance reputation tracking with weight reduction. |
| **Scheduling exploitation** | Exploit deterministic, public schedule for targeted attacks | VRF unpredictability (1-epoch-ahead only). Schedule is deterministic but not advantageous without committee control. Committee shopping prevented by claim commitment. |
| **Reconfiguration attack** | Deliberately trigger parcel reconfigurations to cause storms | Staggering constraint (20% cap). Circuit breaker (30% halt). Minimum 10-epoch interval. Sentinel Graph monitors reconfiguration frequency. |
| **Tidal function poisoning** | Propose a subtly buggy tidal function through governance | 72-hour discussion period for review. ETR for emergency rollback. Settlement divergence detection (ETR-T3). |

### 8.2 VRF Dual Defense Detailed Design

See Section 3.3 for the full specification of the commit-reveal protocol and pre-stratified diversity pools working together.

**Adversary Advantage Bound:**

An adversary controlling K Sybil identities in a pool of N honest agents:
- Commit-reveal prevents timing the claim hash or VRF seed for advantage. The mutual information between committed attributes and future committee selection is negligible when VRF seeds rotate every epoch.
- Pre-stratified pools ensure the adversary's representation in each stratum is at most K/(K+N_stratum) where N_stratum is the honest population of that stratum.
- For a committee of size 7 drawn from 4 strata of 250 honest agents each, an adversary with 20 Sybils (spread across all strata, 5 per stratum) has per-stratum representation of 5/255 = 1.96%. Expected committee presence: ~0.14 agents (vs 0.13 for proportional baseline). Advantage: ~3% above baseline.
- This advantage is bounded by stake requirements and detectable by Sentinel Graph within ~20 epochs of sustained elevated committee presence.

### 8.3 Coalition Attack Analysis

**26% Blocking Coalition:**
- Can block standard governance (75% threshold)
- Cannot block ETR (90% threshold, separate from standard governance)
- Cannot block membrane protection (constitutional, immutable)
- Can delay tidal version updates but cannot deploy bad versions
- Detection: Sentinel Graph monitors governance participation patterns. Persistent blocking triggers governance health alert.

**10% ETR Blocking Coalition:**
- Can block ETR (preventing emergency rollback)
- Combined with tidal function poisoning: could maintain a buggy version
- Defense: After 3 failed ETR attempts, threshold drops to 80% (only 20% can block). After 6 failed attempts, automated Sentinel-triggered rollback activates without governance vote (constitutional provision).

**Colluding Verifier Minority (< 1/3 of committee):**
- Cannot override honest majority in BFT verification
- Can produce false attestations that are outvoted
- Detection: Sentinel Graph anti-correlation audit detects correlated attestation patterns within 10 epochs
- Response: Flagged agents excluded from future committees. Slashing of staked AIC.

---

## 9. Deployment Architecture

### 9.1 Runtime Architecture

Each agent runs the following local components:

```
+============================================================+
|                    AGENT RUNTIME                            |
|                                                             |
|  +----------------+  +-----------------+  +--------------+  |
|  | Tidal Scheduler|  | VRF Engine      |  | Predictive   |  |
|  | - Hash rings   |  | - ECVRF compute |  | Delta Channel|  |
|  | - Epoch clock  |  | - Pool lookup   |  | - Neighbor   |  |
|  | - Assignment   |  | - Proof gen     |  |   models     |  |
|  +----------------+  +-----------------+  | - Surprise   |  |
|                                            |   router     |  |
|  +----------------+  +-----------------+  +--------------+  |
|  | Settlement     |  | Parcel Manager  |                    |
|  | Calculator     |  | (local view)    |  +--------------+  |
|  | - Compliance   |  | - PTP state     |  | I-Confluence  |  |
|  | - AIC compute  |  | - Reconfiguring?|  | Checker       |  |
|  +----------------+  +-----------------+  | - Proof cache |  |
|                                            | - Op classify |  |
|  +----------------+  +-----------------+  +--------------+  |
|  | Capacity       |  | Governance      |                    |
|  | Snapshot Svc   |  | Client          |  +--------------+  |
|  | - Local state  |  | - Dedicated     |  | Sentinel     |  |
|  | - Gossip       |  |   channel       |  | Agent        |  |
|  | - Roster       |  | - ETR voting    |  | - Local      |  |
|  +----------------+  +-----------------+  |   monitoring |  |
|                                            +--------------+  |
|  +------------------------------------------------------+   |
|  |                    AASL/AACP Layer                     |   |
|  |  27 types, 25+ message types, wire format             |   |
|  +------------------------------------------------------+   |
+============================================================+
```

### 9.2 Network Architecture

Three network layers:

1. **Data Plane:** Tidal-scheduled communication within parcels. Predictive delta messages (SRP), standard messages, task data. Organized by parcel topology.

2. **Gossip Plane:** Epoch-boundary capacity snapshots. Stigmergic signals at locus scope. Gossip protocol with bounded TTL. Hierarchical aggregation for scale.

3. **Governance Plane:** Dedicated persistent mesh of governance agents. Always-on. Independent of parcel topology and tidal scheduling. Heartbeat protocol for liveness detection. Carries: ETR proposals, ETR votes, standard governance proposals, governance monitoring.

### 9.3 Deployment Phases

| Phase | Timeline | Agents | Loci | Key Deliverables |
|-------|----------|--------|------|-----------------|
| 1 | Months 1-4 | 1-100 | 1-3 | Hash ring validation, VRF prototype, bootstrap proof library, HG-1/HG-2/HG-3 simulations |
| 2 | Months 5-10 | 100-1K | 10-50 | Multi-locus PTP, predictive delta, cross-locus VRF, ETR prototype, AASL extension, 1K-agent simulation |
| 3 | Months 11-16 | 1K-10K | 50-500 | Full economic model, Sentinel Graph extensions, governance system, M-class proof library (20+), 10K-agent deployment |
| 4 | Months 17-24 | 10K-100K | 500-5K | Cross-region federation, hierarchical aggregation, 100K simulation, TLA+ verification suite, production readiness |

### 9.4 Monitoring and Operations

**Key operational metrics:**

| Metric | Source | Alert Threshold | Critical Threshold |
|--------|--------|----------------|-------------------|
| Hash ring load imbalance (max/avg) | Tidal Scheduler | > 1.15 | > 1.25 |
| VRF committee diversity score | VRF Engine | < 0.7 | < 0.5 |
| Predictive model accuracy (avg) | Predictive Delta | < 60% | < 40% |
| Parcel TRANSITIONING fraction | Parcel Manager | > 15% | > 30% (circuit breaker) |
| Governance channel availability | Governance Plane | < 98% | < 95% |
| ETR detection-to-activation latency | ETR Controller | > 3 epochs | > 5 epochs |
| MQI (any metric in alert) | Noosphere Core | 1 metric | 3+ metrics |
| Capacity snapshot staleness (avg) | Capacity Snapshot Svc | > 2 epochs | > 5 epochs |
| Settlement divergence rate | Settlement Calculator | > 0.1% | > 1% |

---

## 10. Architectural Decisions

### ARCH-C3-001: Noosphere as Primary Architecture

**Status:** ACCEPTED
**Context:** Three candidate architectures (Noosphere, Locus Fabric, PTA) were evaluated for unification.
**Decision:** The Noosphere remains the primary architecture. PTA becomes the scheduling substrate within parcels. The Locus Fabric provides formal proof discipline.
**Rationale:** The Noosphere has the most complete design (2277 lines, 9 versions), the deepest verification membrane, and the most mature economic model. PTA's scheduling is absorbed because it provides deterministic O(1) scheduling that the Noosphere's threshold-based cell assembly lacks. The Locus Fabric's proof obligations are adopted because they formalize what the Noosphere's M-class classification implies but does not enforce.
**Consequences:** The Noosphere's 23 AASL types expand to 27. Cell assembly remains as a sub-epoch reactive mechanism triggered by surprises. Schelling-point migration is replaced by G-class governance.

### ARCH-C3-002: Bounded-Loads Consistent Hashing

**Status:** ACCEPTED (pending HG-2 validation)
**Context:** Standard consistent hashing produces O(log N / log log N) load imbalance at small parcel sizes (5-15 agents).
**Decision:** Adopt bounded-loads consistent hashing (Mirrokni, Thorup, Wieder, SODA 2018) with virtual node inflation V(N) = max(150, ceil(1000/N)).
**Rationale:** Proven algorithm deployed in production (Google, Vimeo). Provides O(1+epsilon) maximum load guarantee. Virtual node inflation policy parameterized by parcel size addresses the small-ring problem.
**Consequences:** Lookup is O(log V) not O(1). Slightly increased churn cost during parcel reconfiguration. Epsilon parameter must be tuned per parcel size class (via HG-2).

### ARCH-C3-003: VRF Dual Defense (Commit-Reveal + Pre-Stratified Pools)

**Status:** ACCEPTED
**Context:** The Adversarial Analyst identified VRF diversity grinding (Attack 3, HIGH) where adversaries register Sybils with optimized diversity attributes. The commit-reveal protocol alone does not prevent exploiting the filtering step.
**Decision:** Combine commit-reveal protocol (prevents grinding the claim hash and attribute timing) with pre-stratified diversity pools (prevents exploiting the filtering step). Both mechanisms are mandatory and work together.
**Rationale:** Commit-reveal alone prevents timing attacks but does not prevent an adversary from optimizing attribute distribution across Sybils at registration time. Pre-stratified pools alone prevent pool concentration but do not prevent claim hash grinding. Together, they bound adversary advantage to <3% above stake-proportional baseline.
**Consequences:** 1-epoch delay between claim submission and verification scheduling. 100-epoch attribute lock at registration. Pool re-stratification at each epoch boundary. Additional Sentinel Graph monitoring for "too perfect" diversity distributions.

### ARCH-C3-004: Emergency Tidal Rollback (ETR)

**Status:** ACCEPTED (pending HG-3 validation)
**Context:** The Adversarial Analyst identified Emergency Governance Deadlock (Attack 5, CRITICAL). A buggy tidal function could degrade scheduling for 72+ hours during standard G-class governance.
**Decision:** Dedicated ETR mechanism with 3 automated triggers, 90% instant supermajority (no discussion period), propagation on dedicated governance channel.
**Rationale:** The 90% threshold is high enough to prevent abuse (much harder to achieve than 75%) while eliminating the 72-hour discussion period that could be catastrophic for scheduling emergencies. The dedicated governance channel ensures ETR is not blocked by the very scheduling disruption it is designed to fix.
**Consequences:** Dedicated governance channel infrastructure required (additional operational cost). Governance agents have always-on voting obligation. Failed ETR triggers threshold reduction (90% -> 80% after 3 failures).

### ARCH-C3-005: 1K-10K Primary Scale Target

**Status:** ACCEPTED
**Context:** Assessment Council required scale target reframing (REQ-2). The 170x gap between highest demonstrated autonomous agent coordination (590, MegaAgent) and C3-A's original 100K target is an existence proof failure.
**Decision:** Primary design target is 1K-10K agents. 100K is retained as Phase 4 aspiration contingent on Phase 3 empirical results. All design decisions, timeline commitments, and resource allocations are justified at the 1K-10K scale.
**Rationale:** At 1K-10K agents, the Locus/Parcel decomposition keeps parcel sizes within 5-50 agents (well-understood). Gossip convergence is manageable. Governance participation rates are realistic. The system delivers value at this scale in high-stakes verticals (pharma, defense, critical infrastructure).
**Consequences:** Phase 4 (100K) is gated on Phase 3 results. Hierarchical aggregation is designed but not required until Phase 3+. Some design choices that optimize for 100K (aggressive gossip, approximate Sentinel Graph) are deferred.

### ARCH-C3-006: Provisional M-Class Classification

**Status:** ACCEPTED
**Context:** Assessment Council identified I-Confluence cold-start (REQ-1) as a practical bottleneck. Mandatory formal proofs before M-class classification would force most operations into higher-cost classes at launch.
**Decision:** Introduce M-prov (provisional M-class) for operations with empirical convergence evidence but incomplete formal proofs. M-prov operations execute coordination-free with additional monitoring. Automatic demotion to B-class on convergence violation.
**Rationale:** Preserves the formal rigor aspiration (full M-class still requires machine-checked proof) while allowing the system to achieve reasonable performance at launch. The Sentinel Graph provides runtime safety net for M-prov operations.
**Consequences:** Two tiers of M-class certification. Additional monitoring infrastructure. Risk: an M-prov operation that silently violates I-confluence could corrupt state before detection. Mitigation: monitoring checks convergence at every epoch boundary, bounding the damage window to 1 epoch.

### ARCH-C3-007: PTA Layer 3 (Morphogenic Fields) Discarded

**Status:** ACCEPTED
**Context:** PTA Layer 3 (morphogenic field allocation within 4-agent clusters using potential games) has insufficient validation evidence. The Science Assessment concurred: "interaction between potential games in 4-agent clusters and the parcel model is poorly defined."
**Decision:** Discard PTA Layer 3 entirely. The Noosphere's cell assembly mechanism (threshold-based reactive recruitment) handles sub-epoch adaptation. The Tidal Scheduler handles epoch-scale scheduling.
**Rationale:** Layer 3 adds complexity without proven benefit. The 4-agent cluster model does not map cleanly to the Locus/Parcel decomposition. Potential game convergence within a single epoch is unvalidated.
**Consequences:** Sub-epoch adaptation relies solely on Noosphere cell assembly triggered by SLV threshold crossings and surprise signals. This is reactive rather than proactive but is well-understood and validated.

### ARCH-C3-008: Dedicated Governance Channel

**Status:** ACCEPTED
**Context:** ETR votes must propagate independently of the tidal-scheduled data plane. If scheduling disruption impairs communication, governance voting is also impaired (circular dependency).
**Decision:** Maintain a dedicated, always-on governance channel as a persistent mesh of governance agents. This channel uses simple reliable broadcast, not predictive delta or tidal scheduling. Independent infrastructure.
**Rationale:** Breaks the circular dependency between scheduling and governance. ETR voting proceeds even when the data plane is degraded. The channel carries low traffic (governance proposals and votes only) so infrastructure cost is modest.
**Consequences:** Additional network infrastructure. Governance agents must maintain dual connectivity (data plane + governance plane). Heartbeat protocol adds operational complexity.

### ARCH-C3-009: Trend Signals for Stigmergic Layer

**Status:** ACCEPTED
**Context:** Adversarial Analyst (Attack 10) identified information loss at the predictive/stigmergic boundary. Threshold-based signals are reactive; the predictive layer detects trends but cannot communicate them at locus scope.
**Decision:** Add `trend` signal type carrying gradient information (direction and rate of change of SLV dimensions).
**Rationale:** Enables proactive locus-scope awareness of developing conditions before threshold crossings. Modest extension to signal type system.
**Consequences:** 8th signal type (up from 7). Trend signals require SLV gradient computation at parcel level. Additional bandwidth for trend signal propagation at locus scope.

### ARCH-C3-010: Surprise Rate as 7th SLV Dimension

**Status:** ACCEPTED
**Context:** Science Assessment identified threshold calibration pathology (IP-3 x IP-4) between PTA surprise threshold and Noosphere SLV threshold.
**Decision:** Add surprise_rate as the 7th dimension of the Scope Load Vector. SLV constrains surprise threshold; surprise feeds SLV.
**Rationale:** Formally couples the two independently-calibrated threshold systems. Prevents pathological configurations where one system floods while the other ignores.
**Consequences:** SLV computation slightly more expensive (1 additional dimension). Bi-timescale controller fast loop gains an additional controlled variable.

---

## Appendix A: Traceability Matrix

This matrix traces Assessment Council conditions, adversarial findings, and user feedback to their resolution in this architecture document.

### Assessment Council Conditions

| Condition | ID | Resolution | Section |
|-----------|----|-----------|---------|
| Reconfiguration Storm Simulation | GATE-1 | HG-1 experiment design with 6 churn profiles, success/kill criteria | 2.1 |
| Bounded-Loads Hash Ring Validation | GATE-2 | HG-2 experiment design with epsilon sweep, 4 distributions | 2.2 |
| Emergency Tidal Rollback Feasibility | GATE-3 | HG-3 mechanism design + experiment with 6 bug scenarios | 2.3 |
| I-Confluence Proof Library Bootstrap | REQ-1 | 15 pre-certified operations, expansion strategy, M-prov mechanism | 5 |
| Scale Target Reframing | REQ-2 | 1K-10K primary, 100K Phase 4 aspiration | 7, ARCH-C3-005 |
| Cross-Integration Failure Specification | REQ-3 | 6 failure combinations with recovery bounds and degraded-mode guarantees | 6 |
| VRF Post-Filter Bias Quantification | REC-1 | VRF dual defense design, adversary advantage bound analysis | 3.3, 8.2 |

### Adversarial Findings

| Attack | Severity | Resolution | Section |
|--------|----------|-----------|---------|
| 1: Reconfiguration Storm | CRITICAL | PTP + HG-1 simulation + cross-integration failure spec | 2.1, 3.6, 6 |
| 2: Small-Ring Load Imbalance | HIGH | Bounded-loads hash rings + HG-2 validation | 2.2, 3.2, ARCH-C3-002 |
| 3: VRF Diversity Grinding | HIGH | Dual defense: commit-reveal + pre-stratified pools | 3.3, ARCH-C3-003 |
| 4: Deterministic Committee Shopping | HIGH | Claim commitment (1-epoch delay) in commit-reveal protocol | 3.3, 8.1 |
| 5: Emergency Governance Deadlock | CRITICAL | ETR mechanism + HG-3 validation | 2.3, 3.8, ARCH-C3-004 |
| 6: 170x Scale Gap | HIGH | Scale target reframing to 1K-10K | 7, ARCH-C3-005 |
| 7: I-Confluence Cold Start | MEDIUM | Bootstrap plan + M-prov mechanism | 5, 3.9, ARCH-C3-006 |
| 8: CAP Theorem Tension | LOW | Already addressed by operation-class algebra | 1.5 |
| 9: FLP Impossibility | LOW | Already addressed by deterministic scheduling | 3.2 |
| 10: Info Loss at Boundary | MEDIUM | Trend signals + promotion/incorporation protocol | 3.5, ARCH-C3-009 |
| 11: Threshold Calibration | MEDIUM | Surprise rate as 7th SLV dimension + joint calibration | 4.4, ARCH-C3-010 |
| 12: Governance Cost at Scale | LOW | ETR bypass for scheduling emergencies | 3.7, 3.8 |
| 13: Epoch Sync at Scale | LOW | Already addressed by NTP tolerance + graceful degradation | 3.2 |
| 14: Bootstrap Circular Dependency | LOW | Genesis tidal function as asserted parameter | 3.7 |

### User Feedback

| Feedback | Resolution | Section |
|----------|-----------|---------|
| VRF defense must combine commit-reveal + pre-stratified pools | Both mechanisms specified working together | 3.3, 4.2, ARCH-C3-003 |
| Scale target: 1K-10K primary, 100K Phase 4 | Architecture designed for 1K-10K, 100K as aspiration | 7, ARCH-C3-005 |
| I-confluence cold-start bootstrap: minimal obviously-I-confluent set, then expand | 15 bootstrap operations identified with effort estimates, expansion strategy | 5 |

---

## Appendix B: Open Questions for Design Review

1. **Epsilon tuning:** The optimal epsilon per parcel size class for bounded-loads hash rings is determined by HG-2 results. The architecture assumes epsilon values in the table (Section 2.2.2) but these are estimates.

2. **Governance channel infrastructure:** The dedicated governance channel is specified as a "persistent mesh" but the exact protocol (pure gossip, structured overlay, relay-based) is not yet determined. Phase 1 deliverable.

3. **SRP vs SIG consolidation:** The decision to keep SRP as a separate type (not a SIG subtype) should be reviewed after Phase 1 prototyping. If parsing complexity is not a significant concern in practice, consolidation reduces type count.

4. **M-prov monitoring latency:** The claim that Sentinel Graph detects M-prov convergence violations within 1 epoch assumes epoch-boundary monitoring. If violations accumulate within an epoch before detection, the damage window is 1 full epoch of potentially inconsistent state. The severity of this window depends on the operation type. Phase 2 investigation.

5. **Hierarchical snapshot aggregation protocol:** Required for Phase 3 (1K-10K agents) but not yet specified. Must preserve bounded staleness while reducing gossip message count from O(N log N) to O(N log(N/L)) where L is loci count.

6. **Cross-region federation:** Required for Phase 4 but not specified in this document. The Noosphere's existing cross-region federation (Section 33) provides the starting point but must be extended with tidal scheduling coordination.

7. **Tidal function complexity bounds:** As the system grows, tidal function definitions (TDF) may become complex (multiple hash ring configurations, VRF parameters per locus). The AASL TDF type must be expressive enough to represent this. Phase 2 validation.

---

*Architecture produced by: Architecture Designer, Atrahasis Agent System*
*Input documents: Noosphere Master Spec v5, PTA Complete Design v0.1, C3 Deliberation, C3 Refined Concept, C3 Adversarial Report, C3 Feasibility Verdict, C3 Science Assessment*
*Assessment Council verdict: CONDITIONAL_ADVANCE with 3 gates, 3 required actions, 1 recommendation*
