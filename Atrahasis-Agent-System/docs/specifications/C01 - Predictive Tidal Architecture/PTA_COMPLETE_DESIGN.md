# C1 — Predictive Tidal Architecture (PTA): Complete Design Document

**Invention ID:** C1
**Stage:** DESIGN
**Version:** v0.1
**Date:** 2026-03-09
**Status:** DRAFT
**Assessment Council Verdict:** CONDITIONAL_ADVANCE (ADR-002)

---

# Part I — System Architecture

---


## 1. Architecture Overview

### 1.1 System Context

PTA is a coordination-layer architecture positioned between the organizational hierarchy (CIOS) above and the verification/economic subsystems below. It does not execute tasks, verify claims, define semantics, or manage tokens. It computes **who does what, when, and with whom** — deterministically.

```
                    +-------------------------------+
                    |        HUMAN GOVERNANCE       |
                    |  (Tidal Function Parameters,  |
                    |   Epoch Config, Version Mgmt) |
                    +---------------+---------------+
                                    |
                    +---------------v---------------+
                    |            CIOS               |
                    |  (Organizational Hierarchy:   |
                    |   Coordinators, Implementors, |
                    |   Observers, Strategists)     |
                    +---------------+---------------+
                                    |
                        scheduling params, topology,
                        role assignments
                                    |
          +-------------------------v--------------------------+
          |                                                    |
          |         PREDICTIVE TIDAL ARCHITECTURE (PTA)        |
          |                                                    |
          |  +-------------+  +-----------+  +-------------+  |
          |  |    LAYER 1  |  |  LAYER 2  |  |   LAYER 3   |  |
          |  |    Tidal    |  | Predictive|  | Morphogenic  |  |
          |  |  Backbone   |  |   Delta   |  |    Field     |  |
          |  | (REQUIRED)  |  |  Comms    |  | Allocation   |  |
          |  |             |  |(ENHANCING)|  | (GATED)      |  |
          |  +-------------+  +-----------+  +-------------+  |
          |                                                    |
          +---+----------+----------+----------+----------+----+
              |          |          |          |          |
              v          v          v          v          v
          Verichain    AASL     AIC Token   Knowledge  Tetrahedral
         (verifier  (claim     (settlement  Graph     Clusters
          sets)     types,      amounts)   (read/write (local
                    semantic               windows)   allocation)
                    dims)
```

### 1.2 High-Level Component Diagram

```
+====================================================================+
|                    PTA RUNTIME                                      |
|                                                                     |
|  LAYER 1: TIDAL BACKBONE (Phase 1)                                 |
|  +------------------+ +-------------------+ +-------------------+  |
|  | Tidal Function   | | Scheduling        | | Verifier Set      |  |
|  | Engine           | | Resolver          | | Computer          |  |
|  | - Hash rings     | | - Task assignment | | - VRF evaluation  |  |
|  | - Epoch clock    | | - Virtual nodes   | | - Seed management |  |
|  | - VRF compute    | | - Churn handling  | | - Set output      |  |
|  +------------------+ +-------------------+ +-------------------+  |
|  +------------------+ +-------------------+ +-------------------+  |
|  | Settlement       | | Tidal Version     | | Capacity Snapshot |  |
|  | Calculator       | | Manager           | | Service           |  |
|  | - Compliance     | | - Version registry| | - Epoch-boundary  |  |
|  |   scoring        | | - Overlap periods | |   state exchange  |  |
|  | - AIC amounts    | | - Schelling-point | | - Agent capacity  |  |
|  |                  | |   migration       | |   aggregation     |  |
|  +------------------+ +-------------------+ +-------------------+  |
|                                                                     |
|  LAYER 2: PREDICTIVE DELTA COMMUNICATION (Phase 2, enhancing)      |
|  +------------------+ +-------------------+                        |
|  | Prediction Model | | Surprise Signal   |                        |
|  | Manager          | | Router            |                        |
|  | - Per-neighbor   | | - Delta encoding  |                        |
|  |   linear models  | | - Radius control  |                        |
|  | - Threshold      | | - Propagation     |                        |
|  |   adaptation     | |   damping         |                        |
|  +------------------+ +-------------------+                        |
|                                                                     |
|  LAYER 3: MORPHOGENIC FIELD ALLOCATION (Phase 3, gated)           |
|  +------------------+                                              |
|  | Field Gradient   |                                              |
|  | Computer         |                                              |
|  | - Potential game |                                              |
|  |   solver         |                                              |
|  | - AASL semantic  |                                              |
|  |   space          |                                              |
|  | - Tidal reset    |                                              |
|  |   perturbation   |                                              |
|  +------------------+                                              |
|                                                                     |
|  INTEGRATION ADAPTERS                                              |
|  +--------+ +--------+ +--------+ +--------+ +--------+           |
|  | CIOS   | |Verichain| | AASL  | |  AIC   | |  KG    |           |
|  |Adapter | |Adapter  | |Adapter | |Adapter | |Adapter |           |
|  +--------+ +--------+ +--------+ +--------+ +--------+           |
+====================================================================+
```

### 1.3 Design Philosophy and Constraints

**Core principle:** Agree by computation, communicate only surprises.

**Design constraints:**

1. **Determinism first.** Every scheduling, verification, and settlement computation must be a pure function of shared inputs. Two agents with the same inputs must produce identical outputs. No runtime consensus is permitted for coordination.

2. **Layer independence.** The tidal backbone (Layer 1) must be fully functional without Layers 2 or 3. Predictive communication (Layer 2) enhances but does not replace backbone operations. Morphogenic fields (Layer 3) are additive and droppable. (Assessment Council condition: ADVISORY items 3 and 4.)

3. **Narrow integration interfaces.** PTA communicates with each subsystem through typed, versioned, epoch-relative interfaces. No shared mutable state. Each integration point is independently testable.

4. **O(1) per-agent steady-state overhead.** Per-agent computation and communication must be constant with respect to total system size N. Only epoch-boundary capacity snapshots incur O(N) aggregate cost, amortized across the epoch.

5. **Graceful degradation.** Every component failure degrades to a less-efficient but still-correct state. No single failure causes system-wide incorrectness.

6. **Epoch-relative timing.** All operations are defined relative to epoch boundaries, not wall-clock time. Clock synchronization is NTP-grade, not consensus-grade.

---

## 2. Component Architecture

### 2.1 Tidal Function Engine

**Purpose:** Maintains the consistent hash ring infrastructure and provides the core deterministic computation primitives upon which all scheduling, verification, and settlement depend.

**Responsibilities:**
- Manage one consistent hash ring per task type
- Compute VRF outputs given claim hashes, epochs, and seeds
- Maintain the epoch clock (monotonic counter synchronized via NTP)
- Map agent IDs to virtual nodes on hash rings
- Provide the `evaluate(agent_id, task_type, epoch) -> assignment` primitive

**Inputs:**
- `agent_id`: identifier of the querying agent
- `task_type`: AASL-defined claim type identifier
- `epoch`: integer epoch counter
- `tidal_version`: active tidal function version definition (hash ring config, VRF seeds, epoch length, task-type frequency bands)
- `agent_roster`: current set of registered agents with virtual node mappings (from Capacity Snapshot Service)

**Outputs:**
- `assignment`: deterministic task assignment for (agent_id, task_type, epoch)
- `verifier_set`: VRF-derived set of verifier agent IDs for a given claim hash
- `settlement_boundary`: boolean indicating whether this epoch is a settlement epoch
- `substitution_list`: ordered fallback agents for a given assignment (from hash ring neighbors)

**Internal Structure:**

```
+---------------------------------------------------------------+
|                    Tidal Function Engine                       |
|                                                               |
|  +-------------------+    +--------------------+              |
|  | Epoch Clock       |    | Hash Ring Manager  |              |
|  | - NTP sync        |    | - Ring per task    |              |
|  | - Epoch counter   |    |   type             |              |
|  | - Tick interval   |    | - Virtual nodes    |              |
|  | - Boundary detect |    | - Lookup(key)->    |              |
|  +-------------------+    |   agent            |              |
|                           +--------------------+              |
|  +-------------------+    +--------------------+              |
|  | VRF Computer      |    | Function Registry  |              |
|  | - Micali VRF      |    | - Active version   |              |
|  | - Seed store      |    | - Pending version  |              |
|  | - Proof gen       |    | - Params cache     |              |
|  | - Proof verify    |    |                    |              |
|  +-------------------+    +--------------------+              |
+---------------------------------------------------------------+
```

**Dependencies:**
- Tidal Version Manager (provides active function definition)
- Capacity Snapshot Service (provides agent roster for virtual node mapping)

**Failure Modes and Recovery:**
- **Epoch clock drift:** If local clock drifts beyond tolerance (configurable, default 500ms), the agent is observed as generating timing surprises by peers. Persistent drift is treated as agent failure; substitution list activates.
- **Hash ring inconsistency:** Can only occur if agents have different agent rosters (stale capacity snapshots). Resolved at next epoch boundary when fresh snapshots propagate. Stale-roster scheduling produces suboptimal (not incorrect) assignments — work still gets done, possibly by a less-ideal agent.
- **VRF computation failure:** Local computational failure. Agent cannot produce verifier sets. Fallback: agent reports inability; next agent on substitution list covers verification duty.

---

### 2.2 Scheduling Resolver

**Purpose:** Translates tidal function outputs into concrete task assignments for the local agent within a given epoch.

**Responsibilities:**
- Query the Tidal Function Engine for all task types relevant to this agent
- Resolve conflicts when an agent is assigned to multiple task types in the same epoch
- Apply capacity weighting from the most recent snapshot
- Produce the agent's work schedule for the current epoch

**Inputs:**
- `local_agent_id`: this agent's identifier
- `epoch`: current epoch
- `agent_capabilities`: set of task types this agent can perform
- `capacity_weight`: this agent's current capacity (from Capacity Snapshot Service)
- `tidal_function_outputs`: assignment results from Tidal Function Engine

**Outputs:**
- `epoch_schedule`: ordered list of (task_type, priority, time_slot) assignments for this epoch
- `substitution_duties`: backup assignments this agent holds for failed peers

**Internal Structure:**

```
+-----------------------------------------------+
|              Scheduling Resolver               |
|                                                |
|  +------------------+  +-------------------+  |
|  | Assignment Query  |  | Conflict Resolver |  |
|  | - Per-task-type   |  | - Priority sort   |  |
|  |   hash lookup     |  | - Capacity check  |  |
|  | - Capability      |  | - Overflow defer  |  |
|  |   filter          |  |                   |  |
|  +------------------+  +-------------------+  |
|                                                |
|  +------------------+                         |
|  | Substitution     |                         |
|  | Tracker          |                         |
|  | - Monitor peer   |                         |
|  |   liveness       |                         |
|  | - Activate       |                         |
|  |   backup duties  |                         |
|  +------------------+                         |
+-----------------------------------------------+
```

**Dependencies:**
- Tidal Function Engine (assignment computations)
- Capacity Snapshot Service (capacity weights)
- CIOS Adapter (role-based task filtering)

**Failure Modes and Recovery:**
- **Over-assignment:** Agent assigned more tasks than capacity allows. Resolution: priority-based shedding; lowest-priority tasks are left to substitution agents. Shed events generate a surprise signal to peers.
- **Under-assignment:** Agent has idle capacity. Resolution: agent can voluntarily accept substitution duties or signal availability for reallocation at next epoch boundary.

---

### 2.3 Verifier Set Computer

**Purpose:** Computes deterministic verifier sets for claims using VRF, providing the bridge between PTA scheduling and Verichain verification execution.

**Responsibilities:**
- Compute `verifier_set = VRF(claim_hash, epoch, seed)` for any given claim
- Manage VRF seed rotation (governance-controlled intervals)
- Generate and verify VRF proofs (allowing any agent to confirm the correctness of a verifier set without recomputing it)
- Emit (claim_hash, epoch, verifier_set) tuples to the Verichain Adapter

**Inputs:**
- `claim_hash`: hash of the claim to be verified (from AASL)
- `epoch`: the epoch at which verification is scheduled
- `vrf_seed`: current VRF seed (from Tidal Version Manager)
- `eligible_verifiers`: set of agents with verification capability (from agent roster)

**Outputs:**
- `verifier_set`: ordered list of agent IDs assigned to verify this claim
- `vrf_proof`: cryptographic proof that the verifier set was correctly derived
- `verification_epoch`: the epoch at which verification must occur
- `substitution_verifiers`: backup verifiers if primary verifiers are unavailable

**Internal Structure:**

```
+------------------------------------------------+
|            Verifier Set Computer                |
|                                                 |
|  +-------------------+  +------------------+   |
|  | VRF Evaluator     |  | Seed Manager     |   |
|  | - Micali VRF      |  | - Rotation       |   |
|  | - Hash-to-curve   |  |   schedule       |   |
|  | - Proof gen       |  | - Seed history   |   |
|  +-------------------+  | - Anti-grinding  |   |
|                          |   checks         |   |
|  +-------------------+  +------------------+   |
|  | Set Builder       |                         |
|  | - VRF output ->   |                         |
|  |   agent selection |                         |
|  | - Size config     |                         |
|  | - Substitution    |                         |
|  |   list            |                         |
|  +-------------------+                         |
+------------------------------------------------+
```

**Dependencies:**
- Tidal Function Engine (VRF primitives, epoch clock)
- Tidal Version Manager (VRF seed)
- Capacity Snapshot Service (eligible verifier roster)

**Failure Modes and Recovery:**
- **Stale VRF seed:** Agent uses an outdated seed. Detected when Verichain rejects the verifier set proof. Agent re-syncs seed from Tidal Version Manager and recomputes.
- **Insufficient eligible verifiers:** Fewer available verifiers than required set size. Resolution: reduce set size to available count; if below minimum threshold, defer claim verification to next epoch.

---

### 2.4 Settlement Calculator

**Purpose:** Computes deterministic AIC settlement amounts at epoch boundaries based on tidal compliance, surprise costs, prediction accuracy, and verification participation.

**Responsibilities:**
- Score each agent's tidal compliance for the completed epoch
- Compute surprise costs based on surprise signal history
- Compute prediction accuracy bonuses (Phase 2 only)
- Compute verification participation rewards
- Produce a deterministic settlement ledger that any observer can independently verify

**Inputs:**
- `epoch`: the epoch being settled
- `tidal_schedule`: the deterministic schedule for this epoch (from Tidal Function Engine)
- `event_log`: recorded events for this epoch (task completions, surprise signals, verification actions)
- `economic_parameters`: reward rates, cost rates, bonus multipliers (from tidal function version)

**Outputs:**
- `settlement_ledger`: map of agent_id -> AIC delta (positive = earned, negative = cost)
- `compliance_scores`: map of agent_id -> compliance score [0.0, 1.0]
- `settlement_proof`: deterministic hash of all inputs and outputs for auditability

**Internal Structure:**

```
+---------------------------------------------------+
|              Settlement Calculator                  |
|                                                     |
|  +--------------------+  +---------------------+  |
|  | Compliance Scorer   |  | Surprise Cost       |  |
|  | - Schedule vs       |  | Computer            |  |
|  |   actual comparison |  | - Magnitude-based   |  |
|  | - Partial credit    |  |   costing            |  |
|  |   for late work     |  | - Per-agent          |  |
|  +--------------------+  |   aggregation        |  |
|                           +---------------------+  |
|  +--------------------+  +---------------------+  |
|  | Prediction Bonus    |  | Verification        |  |
|  | Computer (Phase 2)  |  | Reward Computer     |  |
|  | - Model accuracy    |  | - Duty fulfillment  |  |
|  |   evaluation        |  |   check             |  |
|  | - Bonus scaling     |  | - Fee computation   |  |
|  +--------------------+  +---------------------+  |
|                                                     |
|  +--------------------+                            |
|  | Ledger Assembler    |                            |
|  | - Sum all streams   |                            |
|  | - Proof generation  |                            |
|  +--------------------+                            |
+---------------------------------------------------+
```

**Dependencies:**
- Tidal Function Engine (scheduled assignments for comparison)
- AIC Adapter (settlement output delivery)
- Verichain Adapter (verification duty records)
- Surprise Signal Router (surprise event records, Phase 2)

**Failure Modes and Recovery:**
- **Incomplete event log:** Some events may be missing at settlement time (network partition, late arrival). Resolution: settlement uses a grace period (configurable, default 1 epoch). Events arriving within the grace period are included in an amended settlement. Events arriving after grace period are written off — the cost is bounded and predictable.
- **Disputed settlement:** By design, settlement is deterministic. If two agents compute different settlements from the same inputs, one has a bug. Resolution: compare settlement proofs (deterministic hashes); the divergent agent re-syncs its computation logic from the canonical tidal function version.

---

### 2.5 Prediction Model Manager

**Purpose:** Maintains lightweight linear predictive models for each direct neighbor, enabling the predictive delta communication layer (Phase 2). This component is enhancing but not required — the tidal backbone operates fully without it.

**Responsibilities:**
- Maintain one linear predictive model per direct neighbor (bounded by CIOS hierarchy degree, typically 4-10)
- Predict neighbor behavior relative to the tidal schedule: expected task completions, resource consumption, communication patterns
- Compute prediction errors (observed - predicted)
- Adapt surprise thresholds: tighten as accuracy improves, loosen under non-stationarity
- Recalibrate models at tidal (epoch) boundaries using observed behavior
- Manage cold-start: use standard messaging until model accuracy crosses activation threshold

**Inputs:**
- `neighbor_list`: direct neighbors per CIOS hierarchy (from CIOS Adapter)
- `neighbor_observations`: observed behavior of each neighbor during the epoch
- `tidal_schedule`: expected schedule for each neighbor (from Tidal Function Engine)
- `model_state`: current model parameters for each neighbor (persisted locally)
- `threshold_parameters`: adaptation rates, minimum/maximum thresholds

**Outputs:**
- `predictions`: predicted behavior vector for each neighbor for the next epoch
- `prediction_errors`: observed - predicted for each neighbor in the completed epoch
- `surprise_flags`: boolean per neighbor indicating whether prediction error exceeds threshold
- `model_accuracy`: rolling accuracy metric per neighbor
- `communication_mode`: per neighbor, one of {STANDARD, TRANSITIONING, PREDICTIVE}

**Internal Structure:**

```
+------------------------------------------------------+
|            Prediction Model Manager                   |
|                                                       |
|  +----------------------+  +-----------------------+ |
|  | Model Store          |  | Threshold Adapter     | |
|  | - Per-neighbor model |  | - Accuracy-gated      | |
|  |   parameters         |  |   tightening          | |
|  | - History window     |  | - Non-stationarity    | |
|  | - Accuracy metrics   |  |   loosening           | |
|  +----------------------+  | - Hysteresis guard    | |
|                             +-----------------------+ |
|  +----------------------+  +-----------------------+ |
|  | Error Computer       |  | Cold-Start Manager    | |
|  | - observed - predict |  | - Standard messaging  | |
|  | - Magnitude calc     |  |   fallback            | |
|  | - Flag generation    |  | - Accuracy threshold  | |
|  +----------------------+  |   for transition      | |
|                             | - Progressive switch  | |
|                             +-----------------------+ |
|  +----------------------+                            |
|  | Epoch Recalibrator   |                            |
|  | - Boundary-triggered |                            |
|  |   model update       |                            |
|  | - Weight refresh     |                            |
|  +----------------------+                            |
+------------------------------------------------------+
```

**Dependencies:**
- CIOS Adapter (neighbor list)
- Tidal Function Engine (expected schedules for neighbors)
- Capacity Snapshot Service (observed neighbor state at boundaries)

**Failure Modes and Recovery:**
- **Model divergence (silent drift):** Model is confidently wrong. Detection: epoch-boundary recalibration compares model predictions against actual observations. If recalibration error exceeds a ceiling, the model is reset to cold-start state for that neighbor.
- **Threshold oscillation:** Adaptive threshold oscillates between tight and loose, causing communication pattern instability. Mitigation: hysteresis guard — threshold must remain stable for a configurable number of epochs before adjustment is permitted.
- **All-neighbor model failure:** If >50% of neighbor models are in STANDARD mode, the Prediction Model Manager signals that the predictive layer is degraded. System operates on tidal backbone alone. No correctness impact.

---

### 2.6 Surprise Signal Router

**Purpose:** Routes delta-encoded surprise signals between agents with magnitude-proportional propagation radius and damping.

**Responsibilities:**
- Package prediction errors into surprise signals when they exceed the threshold
- Determine propagation radius based on surprise magnitude
- Route signals to affected agents within radius
- Apply damping to prevent cascade amplification
- Record all surprise events for settlement calculation

**Inputs:**
- `surprise_flags`: from Prediction Model Manager
- `prediction_errors`: magnitude and direction of each surprise
- `network_topology`: CIOS hierarchy adjacency (from CIOS Adapter)
- `damping_parameters`: propagation decay rate, maximum radius, cascade ceiling

**Outputs:**
- `outgoing_signals`: surprise signals to transmit to affected agents
- `incoming_signals`: surprise signals received from other agents (fed back to Prediction Model Manager)
- `surprise_log`: complete record of all surprise events for settlement

**Internal Structure:**

```
+-------------------------------------------------+
|            Surprise Signal Router                |
|                                                  |
|  +-------------------+  +--------------------+  |
|  | Signal Packager    |  | Radius Calculator  |  |
|  | - Delta encoding   |  | - Magnitude ->     |  |
|  | - Source/epoch/    |  |   hop count        |  |
|  |   error vector     |  | - Damping function |  |
|  +-------------------+  | - Max radius cap   |  |
|                          +--------------------+  |
|  +-------------------+  +--------------------+  |
|  | Propagation Engine |  | Cascade Limiter    |  |
|  | - Topology-aware   |  | - Per-epoch signal |  |
|  |   routing          |  |   budget           |  |
|  | - Hop-count track  |  | - Exponential      |  |
|  | - Dedup            |  |   decay per hop    |  |
|  +-------------------+  +--------------------+  |
|                                                  |
|  +-------------------+                          |
|  | Event Recorder     |                          |
|  | - Surprise log     |                          |
|  | - Settlement feed  |                          |
|  +-------------------+                          |
+-------------------------------------------------+
```

**Dependencies:**
- Prediction Model Manager (surprise flags and error magnitudes)
- CIOS Adapter (network topology for routing)
- Settlement Calculator (surprise log for cost accounting)

**Failure Modes and Recovery:**
- **Signal storm (cascade):** Many simultaneous surprises amplify each other. Prevention: per-epoch signal budget per agent (hard cap); exponential damping per hop; cascade limiter drops signals that would exceed budget. The system gracefully degrades to silence (missed surprises) rather than storm (unbounded signals).
- **Network partition:** Surprise signals cannot reach intended recipients. Impact: recipients do not learn about the surprise until the next epoch-boundary capacity snapshot. Bounded staleness — at most one epoch of missed surprise information.

---

### 2.7 Field Gradient Computer

**Purpose:** Computes potential-game-based gradient vectors for sub-epoch task allocation within tetrahedral (4-agent) clusters. Phase 3 component with a formal decision gate at end of Phase 2. (Assessment Council condition: ADVISORY item 4.)

**Responsibilities:**
- Compute the potential function over the 4-agent cluster state
- Derive gradient vectors in AASL-defined semantic space pointing toward unmet task demand
- Apply tidal reset perturbations at epoch boundaries to escape local minima
- Signal field coherence anomalies (agents whose gradient responses are inconsistent with the potential function) to Verichain

**Inputs:**
- `cluster_members`: the 4 agent IDs in this tetrahedral cluster
- `cluster_state`: per-member task queue depths, capability scores, resource availability
- `semantic_dimensions`: AASL-defined dimensions for the field space (from AASL Adapter)
- `task_demand`: current unmet task demand vector for the cluster
- `tidal_boundary_flag`: whether this is an epoch boundary (triggers reset perturbation)

**Outputs:**
- `gradient_vector`: per-agent direction vector for task allocation adjustment
- `allocation_recommendation`: suggested task redistribution within the cluster
- `field_coherence_score`: measure of cluster consistency [0.0, 1.0]; low scores indicate anomaly
- `convergence_status`: whether the cluster has reached a Nash equilibrium

**Internal Structure:**

```
+----------------------------------------------------+
|           Field Gradient Computer                    |
|                                                      |
|  +-----------------------+  +---------------------+ |
|  | Potential Function    |  | Gradient Solver      | |
|  | Evaluator             |  | - Analytic at 4D     | |
|  | - Monderer-Shapley    |  | - Per-agent          | |
|  |   potential           |  |   direction          | |
|  | - State -> scalar     |  | - Step size control  | |
|  +-----------------------+  +---------------------+ |
|                                                      |
|  +-----------------------+  +---------------------+ |
|  | Reset Perturbation    |  | Coherence Monitor    | |
|  | Engine                |  | - Expected vs actual | |
|  | - Epoch-boundary      |  |   gradient response  | |
|  |   injection           |  | - Anomaly score      | |
|  | - Magnitude decay     |  | - Verichain signal   | |
|  |   (annealing)         |  |                     | |
|  +-----------------------+  +---------------------+ |
+----------------------------------------------------+
```

**Dependencies:**
- AASL Adapter (semantic dimensions)
- Tidal Function Engine (epoch boundary detection, cluster assignment)
- Verichain Adapter (coherence anomaly signals)

**Failure Modes and Recovery:**
- **Cluster member failure:** 1 of 4 agents fails. The remaining 3 recompute gradients over a 3-agent simplex. Task redistribution absorbs the lost agent's share. If 2+ members fail, the cluster is dissolved; agents are reassigned at the next tidal boundary.
- **Convergence failure:** Cluster does not reach Nash equilibrium within the epoch. Impact: suboptimal but not incorrect allocation. Tidal reset at boundary injects fresh perturbation. Persistent non-convergence triggers cluster reformation.
- **Potential function mismatch:** Agents compute different potential values due to stale state. Impact: gradient directions diverge. Detection: coherence monitor compares gradient responses. Resolution: state re-sync at epoch boundary.

---

### 2.8 Tidal Version Manager

**Purpose:** Manages tidal function versioning, overlap periods, and Schelling-point-based migration between function versions. The single point in PTA where soft consensus is required.

**Responsibilities:**
- Maintain the tidal version registry (all published versions with activation/deactivation epochs)
- Manage overlap periods during version migration (both old and new versions are evaluated simultaneously)
- Track peer migration status (how many observed peers are on the new version)
- Execute Schelling-point migration: switch to new version when sufficient peers observed on it
- Execute rollback if migration does not reach threshold within the overlap period

**Inputs:**
- `version_registry`: all published tidal function versions (from governance)
- `peer_observations`: observed version usage by peers
- `migration_threshold`: fraction of peers required before switching (governance parameter, default 0.67)
- `overlap_duration`: maximum overlap period in epochs (governance parameter)

**Outputs:**
- `active_version`: the currently active tidal function version for this agent
- `pending_version`: the version being migrated to (if any)
- `migration_status`: {STABLE, OVERLAP_ACTIVE, SWITCHING, ROLLBACK}
- `version_parameters`: hash ring config, VRF seeds, epoch length, task-type frequency bands for the active version

**Internal Structure:**

```
+-----------------------------------------------------+
|             Tidal Version Manager                    |
|                                                      |
|  +----------------------+  +----------------------+ |
|  | Version Registry     |  | Migration Controller | |
|  | - Published versions |  | - Peer observation   | |
|  | - Activation epochs  |  | - Threshold tracking | |
|  | - Deactivation epochs|  | - Switch decision    | |
|  | - Parameter sets     |  | - Rollback trigger   | |
|  +----------------------+  +----------------------+ |
|                                                      |
|  +----------------------+  +----------------------+ |
|  | Overlap Executor     |  | Rollback Handler     | |
|  | - Dual evaluation    |  | - Revert to previous | |
|  |   during overlap     |  | - Notify peers       | |
|  | - Result merging     |  | - Clean up pending   | |
|  | - Conflict handling  |  |   version state      | |
|  +----------------------+  +----------------------+ |
+-----------------------------------------------------+
```

**Dependencies:**
- Human Governance (version publication)
- Tidal Function Engine (consumes active version parameters)
- Capacity Snapshot Service (peer version observations embedded in snapshots)

**Failure Modes and Recovery:**
- **Split-brain (agents on different versions):** Some agents switch, others do not, threshold never reached. Prevention: bounded overlap period. If threshold is not reached within the overlap, ALL agents revert to the previous version. The overlap period is long enough to accommodate reasonable propagation delays but short enough to prevent indefinite dual-version operation (default: 10 epochs).
- **Governance failure (no new version published):** System continues on the current version indefinitely. No degradation — the current version remains fully functional.
- **Rapid version churn:** Governance publishes versions faster than agents can migrate. Prevention: minimum cooldown period between version publications (governance rule, not PTA enforcement).

---

### 2.9 Capacity Snapshot Service

**Purpose:** Collects and distributes agent capacity information at epoch boundaries. The sole periodic O(N) communication in the system.

**Responsibilities:**
- At each epoch boundary, compile this agent's capacity snapshot (available resources, active task types, queue depths, version status)
- Propagate snapshot to direct neighbors (CIOS hierarchy adjacency)
- Aggregate received snapshots into a local view of the agent roster
- Provide the agent roster to the Tidal Function Engine for hash ring computation

**Inputs:**
- `local_state`: this agent's current resource availability, task queues, version, liveness
- `neighbor_snapshots`: snapshots received from direct neighbors
- `aggregation_strategy`: how to combine multi-hop snapshots (default: gossip-style with bounded TTL)

**Outputs:**
- `local_snapshot`: this agent's snapshot for distribution
- `agent_roster`: aggregated view of all known agents and their capacities
- `roster_staleness`: estimated age of each entry in the roster

**Internal Structure:**

```
+---------------------------------------------------+
|           Capacity Snapshot Service                 |
|                                                     |
|  +---------------------+  +---------------------+ |
|  | Snapshot Compiler    |  | Snapshot Propagator | |
|  | - Local state        |  | - Neighbor-based    | |
|  |   assembly           |  |   distribution      | |
|  | - Version tagging    |  | - Gossip protocol   | |
|  | - Epoch stamping     |  | - TTL-bounded hops  | |
|  +---------------------+  +---------------------+ |
|                                                     |
|  +---------------------+                           |
|  | Roster Aggregator    |                           |
|  | - Merge received     |                           |
|  |   snapshots          |                           |
|  | - Staleness tracking |                           |
|  | - Conflict           |                           |
|  |   resolution (latest |                           |
|  |   epoch wins)        |                           |
|  +---------------------+                           |
+---------------------------------------------------+
```

**Dependencies:**
- CIOS Adapter (neighbor list for propagation)
- Tidal Function Engine (epoch boundary trigger)

**Failure Modes and Recovery:**
- **Snapshot propagation delay:** Some snapshots arrive late (after the new epoch has started). Impact: agents use the previous epoch's roster. Resolution: the hash ring tolerates stale roster data — assignment is suboptimal but not incorrect. The delayed snapshot is incorporated into the next epoch's roster.
- **Network partition:** A subset of agents cannot exchange snapshots. Impact: disjoint roster views. The hash ring produces different assignments for agents with different rosters. Resolution: partition healing restores snapshot exchange; rosters converge within 1-2 epoch boundaries.

---

### 2.10 Integration Adapters

Each adapter provides a typed, versioned interface between PTA and an external subsystem. Adapters encapsulate serialization, error handling, retries, and version negotiation.

#### 2.10.1 CIOS Adapter

**Purpose:** Bidirectional interface between PTA and the CIOS organizational hierarchy.

**Responsibilities:**
- Receive hierarchy topology (Coordinator/Implementor/Observer/Strategist assignments)
- Receive role-based task filtering rules
- Provide scheduling results to CIOS Coordinators
- Provide tidal compliance data for CIOS performance evaluation

**Interface:**
- **Inbound:** `HierarchyTopology`, `RoleAssignments`, `TaskFilterRules`
- **Outbound:** `EpochSchedule`, `ComplianceReport`, `SubstitutionEvents`

#### 2.10.2 Verichain Adapter

**Purpose:** Outbound interface providing verifier set tuples to Verichain for verification execution.

**Responsibilities:**
- Emit (claim_hash, epoch, verifier_set, vrf_proof) tuples
- Receive verification results (pass/fail/timeout) for settlement computation
- Forward behavioral anomaly signals (Phase 2) and field coherence signals (Phase 3) as supplementary verification inputs

**Interface:**
- **Outbound:** `VerifierSetAssignment`, `AnomalySignal`, `CoherenceSignal`
- **Inbound:** `VerificationResult`, `VerificationReceipt`

#### 2.10.3 AASL Adapter

**Purpose:** Inbound interface receiving semantic structure definitions from AASL.

**Responsibilities:**
- Receive claim type registry (maps to task-type parameters in tidal functions)
- Receive semantic dimension definitions (maps to morphogenic field gradient space)
- Validate that tidal function task-type parameters are consistent with registered AASL claim types

**Interface:**
- **Inbound:** `ClaimTypeRegistry`, `SemanticDimensionDefinitions`
- **Outbound:** `TypeConsistencyReport` (validation feedback)

#### 2.10.4 AIC Adapter

**Purpose:** Outbound interface delivering deterministic settlement amounts to the AIC token system.

**Responsibilities:**
- Deliver settlement ledger entries at each settlement epoch
- Include settlement proofs for independent auditability
- Receive confirmation of settlement execution

**Interface:**
- **Outbound:** `SettlementLedger`, `SettlementProof`
- **Inbound:** `SettlementConfirmation`, `SettlementRejection`

#### 2.10.5 Knowledge Graph Adapter

**Purpose:** Bidirectional interface managing knowledge graph access scheduling.

**Responsibilities:**
- Compute read/write windows for knowledge graph access based on tidal function
- Communicate window schedules to the knowledge graph subsystem
- Receive lifecycle status (active/archival/deprecated) for scheduling prioritization

**Interface:**
- **Outbound:** `AccessWindowSchedule`, `LifecycleTransitionRequest`
- **Inbound:** `LifecycleStatus`, `AccessConfirmation`

---

## 3. Data Flow Diagrams

### 3.1 Steady-State Operation (No Surprises)

In steady state, agents perform their tidal-assigned tasks and exchange no operational messages. The only communication is the epoch-boundary capacity snapshot.

```
Time -->  [---- Epoch N ----][-- Boundary --][---- Epoch N+1 ----]

Agent A:  Compute schedule    Send snapshot   Compute schedule
          Execute tasks       Recv snapshots  Execute tasks
          (silence)           Update roster   (silence)
                              Recalibrate
                              models (L2)

Agent B:  Compute schedule    Send snapshot   Compute schedule
          Execute tasks       Recv snapshots  Execute tasks
          (silence)           Update roster   (silence)
                              Settle AIC

Agent C:  Compute schedule    Send snapshot   Compute schedule
          Execute tasks       Recv snapshots  Execute tasks
          (silence)           Update roster   (silence)

Messages exchanged mid-epoch: ZERO
Messages exchanged at boundary: O(N) aggregate (snapshots only)
```

### 3.2 Surprise Propagation Flow

When an agent deviates from its predicted behavior, a surprise signal propagates outward with decaying magnitude.

```
Agent X deviates from predicted schedule
          |
          v
[Prediction Model Manager @ Agent Y (neighbor of X)]
  - Computes: prediction_error = observed(X) - predicted(X)
  - Checks: |prediction_error| > threshold?
          |
          YES
          v
[Surprise Signal Router @ Agent Y]
  - Packages signal: {source: X, epoch: N, error: E, magnitude: M}
  - Computes radius: R = f(M)  (larger surprise -> wider propagation)
  - Routes to agents within R hops on CIOS topology
          |
          v
[Agents within radius R]
  - Receive surprise signal
  - Update local prediction model for X
  - If received magnitude > local threshold:
      re-propagate with damped magnitude (M' = M * decay_factor)
  - Record event for settlement calculation
          |
          v
[Settlement Calculator (at epoch boundary)]
  - Agent X charged surprise cost proportional to M
  - Detecting agent Y earns prediction accuracy bonus
```

### 3.3 Epoch Boundary Processing

The epoch boundary is the primary synchronization point. Processing is ordered:

```
Epoch N ends
  |
  v
Step 1: SNAPSHOT COMPILATION
  - Each agent compiles local capacity snapshot
  - Snapshot includes: resources, queue depths, version, liveness
  |
  v
Step 2: SNAPSHOT PROPAGATION
  - Snapshots exchanged via CIOS neighbor topology (gossip, TTL-bounded)
  - Aggregation into local agent roster
  |
  v
Step 3: SETTLEMENT (if settlement epoch)
  - Settlement Calculator processes:
    a. Tidal compliance scores
    b. Surprise cost totals
    c. Prediction accuracy bonuses (Phase 2)
    d. Verification participation rewards
  - Settlement ledger emitted to AIC Adapter
  |
  v
Step 4: MODEL RECALIBRATION (Phase 2)
  - Prediction Model Manager updates all neighbor models
  - Compares predictions vs observations for Epoch N
  - Adjusts thresholds per accuracy
  |
  v
Step 5: HASH RING UPDATE
  - Tidal Function Engine incorporates new agent roster
  - Virtual nodes added/removed for joining/leaving agents
  - New hash ring positions computed
  |
  v
Step 6: VERSION CHECK
  - Tidal Version Manager checks for pending migration
  - If in overlap: evaluate migration threshold
  - If threshold met: switch to new version
  - If overlap expired without threshold: rollback
  |
  v
Step 7: SCHEDULE COMPUTATION
  - Scheduling Resolver queries updated Tidal Function Engine
  - Produces Epoch N+1 schedule
  |
  v
Epoch N+1 begins
```

### 3.4 Tidal Function Migration Flow

```
Governance publishes Version V2 (activation_epoch = E, overlap_duration = D)
  |
  v
Epoch E arrives: OVERLAP BEGINS
  |
  +-- All agents evaluate BOTH V1 and V2
  |   V1 results used for execution
  |   V2 results computed for comparison
  |
  v
Each epoch during overlap (E to E+D):
  |
  +-- Agent observes peer behavior
  |   Tracks: which peers appear to be following V2 schedule?
  |   (Embedded in capacity snapshots as version field)
  |
  +-- Agent checks: fraction_on_V2 >= migration_threshold?
  |     |
  |     YES --> Agent switches primary execution to V2
  |     NO  --> Agent continues on V1
  |
  v
Epoch E+D arrives: OVERLAP ENDS
  |
  +-- If fraction_on_V2 >= migration_threshold:
  |     Migration SUCCEEDS
  |     V1 deactivated
  |     All remaining V1 agents forced to V2
  |
  +-- If fraction_on_V2 < migration_threshold:
        Migration FAILS
        V2 deactivated
        All V2 agents revert to V1
        Governance notified of failure
```

### 3.5 Agent Join/Leave (Churn) Flow

```
AGENT JOIN:
  New Agent Z registers
    |
    v
  Next epoch boundary:
    - Z sends initial capacity snapshot
    - Peers incorporate Z into their rosters
    - Hash Ring Manager adds virtual nodes for Z
    - Z receives existing snapshots, builds local roster
    - Z computes schedule for next epoch
    - Z begins execution
    |
  Convergence: 1 epoch boundary (Z is fully integrated)

AGENT LEAVE (graceful):
  Agent Z announces departure in snapshot (liveness = LEAVING)
    |
    v
  Next epoch boundary:
    - Peers remove Z from rosters
    - Hash Ring Manager removes Z's virtual nodes
    - Tasks redistributed to hash-ring successors
    - Substitution lists activate for Z's assignments
    |
  Convergence: 1 epoch boundary (Z is fully removed)

AGENT LEAVE (failure):
  Agent Z stops responding
    |
    v
  During epoch:
    - Z's scheduled checkpoints are missed
    - Substitution agents detect Z's absence (no checkpoint)
    - Substitution agents activate (deterministic: next on hash ring)
    |
  At epoch boundary:
    - Z's snapshot is absent
    - After configurable absence count (default: 2 epochs), Z is
      removed from roster
    - Z's virtual nodes removed from hash ring
    |
  Convergence: 2 epoch boundaries (Z is fully removed)
  During gap: substitution agents cover Z's duties
```

---

## 4. Integration Interface Contracts

Per Assessment Council MANDATORY condition 2: integration interface contracts with Verichain and CIOS must be drafted in Phase 1.

### 4.1 PTA <-> Verichain Interface

**Interface Name:** `PTA-Verichain-VerifierScheduling`
**Direction:** Bidirectional (PTA provides verifier sets; Verichain returns verification results)
**Protocol Version:** 1.0.0

**Data Types Exchanged:**

| Message Type | Direction | Payload | Frequency |
|---|---|---|---|
| `VerifierSetAssignment` | PTA -> Verichain | `{claim_hash: bytes32, epoch: uint64, verifier_set: AgentID[], vrf_proof: bytes, substitution_verifiers: AgentID[]}` | Per claim requiring verification |
| `VerificationResult` | Verichain -> PTA | `{claim_hash: bytes32, epoch: uint64, result: PASS\|FAIL\|TIMEOUT, verifier_reports: VerifierReport[]}` | Per completed verification |
| `AnomalySignal` | PTA -> Verichain | `{agent_id: AgentID, epoch: uint64, anomaly_type: BEHAVIORAL\|COHERENCE, magnitude: float64, evidence: bytes}` | When anomaly detected (Phase 2+) |
| `VerificationReceipt` | Verichain -> PTA | `{claim_hash: bytes32, epoch: uint64, verifiers_participated: AgentID[], fees_earned: map<AgentID, uint64>}` | Per completed verification |

**Timing Constraints:**
- `VerifierSetAssignment` must be emitted before `epoch_start + 0.1 * epoch_length` (first 10% of the epoch)
- `VerificationResult` must be returned before `epoch_end` for inclusion in that epoch's settlement
- `AnomalySignal` is best-effort, no hard deadline (supplementary signal)

**Error Handling:**
- If Verichain is unavailable: PTA queues `VerifierSetAssignment` messages with a TTL of 3 epochs. After TTL expiry, the verification assignment is re-computed for a future epoch.
- If `VerificationResult` is TIMEOUT: the claim is rescheduled for verification in the next epoch with a fresh verifier set. Verifiers who timed out receive a partial participation credit (not full fee).
- If VRF proof validation fails on the Verichain side: Verichain rejects the assignment and returns an error. PTA re-evaluates; if the error persists, the agent's VRF seed is likely stale and triggers a re-sync from Tidal Version Manager.

**Versioning Strategy:**
- Interface version follows semantic versioning (MAJOR.MINOR.PATCH)
- MINOR version changes (additive fields) are backward compatible
- MAJOR version changes require coordinated deployment with overlap period
- Interface version is included in every message header

---

### 4.2 PTA <-> CIOS Interface

**Interface Name:** `PTA-CIOS-CoordinationLayer`
**Direction:** Bidirectional (CIOS provides hierarchy; PTA provides scheduling)
**Protocol Version:** 1.0.0

**Data Types Exchanged:**

| Message Type | Direction | Payload | Frequency |
|---|---|---|---|
| `HierarchyTopology` | CIOS -> PTA | `{agents: AgentDescriptor[], edges: Edge[], roles: map<AgentID, Role>, cluster_assignments: TetrahedralCluster[]}` | At deployment, on topology change |
| `RoleAssignment` | CIOS -> PTA | `{agent_id: AgentID, role: COORDINATOR\|IMPLEMENTOR\|OBSERVER\|STRATEGIST, capabilities: TaskType[], hierarchy_level: uint32}` | Per agent role change |
| `EpochSchedule` | PTA -> CIOS | `{epoch: uint64, assignments: map<AgentID, TaskAssignment[]>, substitutions: map<AgentID, AgentID>}` | Per epoch |
| `ComplianceReport` | PTA -> CIOS | `{epoch: uint64, agent_scores: map<AgentID, float64>, anomalies: AnomalyEvent[]}` | Per settlement epoch |
| `SchedulingParameters` | CIOS -> PTA | `{task_priorities: map<TaskType, uint32>, capacity_overrides: map<AgentID, float64>, scheduling_hints: SchedulingHint[]}` | On parameter change |

**Timing Constraints:**
- `HierarchyTopology` and `RoleAssignment` must arrive before the epoch boundary at which they take effect (at least 1 epoch lead time)
- `EpochSchedule` is computed within the first 5% of each epoch and made available to CIOS Coordinators
- `ComplianceReport` is emitted within 1 epoch of the settlement epoch boundary
- `SchedulingParameters` must arrive at least 2 epochs before taking effect (to allow tidal function recomputation)

**Error Handling:**
- If CIOS is unavailable: PTA continues with the last known hierarchy topology. Scheduling proceeds with stale hierarchy data. Any agent joining or leaving during the outage is handled as churn (join at next available epoch, leave via failure detection).
- If `HierarchyTopology` contains contradictions (agent assigned to multiple roles at same level): PTA rejects the topology update and retains the previous version. Error reported to CIOS.
- If `SchedulingParameters` arrive late (within the 2-epoch buffer): PTA applies them at the next eligible epoch boundary.

**Versioning Strategy:**
- Same semantic versioning as Verichain interface
- Hierarchy topology schema versioned independently (topology changes are frequent; schema changes are rare)
- PTA maintains backward compatibility for at least 2 MAJOR versions of the topology schema

---

### 4.3 PTA <-> AASL Interface

**Interface Name:** `PTA-AASL-SemanticRegistry`
**Direction:** Primarily inbound (AASL provides definitions; PTA provides consistency reports)
**Protocol Version:** 1.0.0

**Data Types Exchanged:**

| Message Type | Direction | Payload | Frequency |
|---|---|---|---|
| `ClaimTypeRegistry` | AASL -> PTA | `{claim_types: ClaimTypeDefinition[], version: uint64}` | On registry update |
| `SemanticDimensionDefinitions` | AASL -> PTA | `{dimensions: DimensionDef[], metric: MetricDef, version: uint64}` | On dimension update |
| `TypeConsistencyReport` | PTA -> AASL | `{epoch: uint64, mismatches: TypeMismatch[], coverage: float64}` | Per settlement epoch |

**Timing Constraints:**
- Registry updates take effect at the next epoch boundary following receipt
- Semantic dimension changes require a morphogenic field recalibration (Phase 3); 2-epoch lead time recommended
- Consistency reports are informational; no hard timing requirement

**Error Handling:**
- If AASL is unavailable: PTA continues with cached claim type registry and semantic dimensions. No impact on Layer 1 (tidal backbone). Layer 3 (morphogenic fields) may use stale dimensions, resulting in suboptimal but not incorrect gradient computation.
- If a claim type is removed from the registry while tasks of that type are in progress: PTA completes the current epoch's assignments and stops scheduling that task type from the next epoch onward.

**Versioning Strategy:**
- Claim type registry is versioned independently (monotonic counter)
- Semantic dimensions are versioned independently
- PTA caches the latest version of each and validates on receipt

---

### 4.4 PTA <-> AIC Token Interface

**Interface Name:** `PTA-AIC-Settlement`
**Direction:** Primarily outbound (PTA provides settlement; AIC confirms)
**Protocol Version:** 1.0.0

**Data Types Exchanged:**

| Message Type | Direction | Payload | Frequency |
|---|---|---|---|
| `SettlementLedger` | PTA -> AIC | `{epoch: uint64, entries: map<AgentID, {delta: int64, breakdown: SettlementBreakdown}>, proof: bytes32}` | Per settlement epoch |
| `SettlementConfirmation` | AIC -> PTA | `{epoch: uint64, status: APPLIED\|PARTIAL\|REJECTED, details: string}` | Per settlement |
| `EconomicParameters` | AIC -> PTA | `{reward_rates: RateSchedule, cost_rates: RateSchedule, bonus_multipliers: MultiplierSchedule, effective_epoch: uint64}` | On parameter change |

**Timing Constraints:**
- `SettlementLedger` must be emitted within 2 epochs of the settlement epoch boundary
- `SettlementConfirmation` expected within 1 epoch of ledger submission
- `EconomicParameters` must arrive at least 1 epoch before `effective_epoch`

**Error Handling:**
- If AIC rejects a settlement (REJECTED): PTA logs the rejection, re-validates the settlement computation, and re-submits. If the recomputed settlement differs, the new version is submitted. If identical, the rejection is escalated to governance.
- If AIC is unavailable: settlements are queued with TTL. Agents continue earning/spending but actual token transfers are deferred. No impact on scheduling or verification.
- PARTIAL settlement: some entries applied, some failed. PTA processes the failed entries as a delta in the next settlement.

**Versioning Strategy:**
- Settlement ledger format versioned with the tidal function version (settlement computation is part of the tidal function)
- Economic parameters versioned independently

---

### 4.5 PTA <-> Knowledge Graph Interface

**Interface Name:** `PTA-KG-AccessScheduling`
**Direction:** Bidirectional (PTA provides access windows; KG provides lifecycle status)
**Protocol Version:** 1.0.0

**Data Types Exchanged:**

| Message Type | Direction | Payload | Frequency |
|---|---|---|---|
| `AccessWindowSchedule` | PTA -> KG | `{epoch: uint64, windows: AccessWindow[], lifecycle_transitions: LifecycleTransition[]}` | Per epoch |
| `LifecycleStatus` | KG -> PTA | `{entries: map<KnowledgeID, ACTIVE\|ARCHIVAL\|DEPRECATED>, version: uint64}` | On status change |
| `AccessConfirmation` | KG -> PTA | `{epoch: uint64, windows_honored: AccessWindow[], windows_denied: AccessWindow[]}` | Per epoch |

**Timing Constraints:**
- `AccessWindowSchedule` emitted at epoch boundary, before agents begin read/write operations
- `LifecycleStatus` updates are asynchronous; PTA incorporates at next epoch boundary
- `AccessConfirmation` expected within the epoch; denied windows trigger scheduling adjustment

**Error Handling:**
- If KG is unavailable: PTA continues scheduling access windows, but agents will encounter access failures. Impact is limited to knowledge operations; tidal backbone unaffected.
- Denied windows: PTA reschedules denied access to a future epoch; affected agents are notified via surprise signal (if Phase 2 active) or at next boundary.

**Versioning Strategy:**
- Access window format versioned with tidal function version
- Knowledge lifecycle status versioned independently

---

## 5. Convergence Experiment Design

Per Assessment Council MANDATORY condition 1: this is the first DESIGN deliverable. Kill criterion: <5% assignment error within 3 epoch cycles at 100+ agents.

### 5.1 Objective

Validate that consistent-hash-based deterministic scheduling achieves sufficient convergence after agent churn events (joins and leaves) to produce less than 5% assignment error within 3 epoch cycles, at a scale of 100+ agents.

**Assignment error** is defined as: the fraction of (agent, task_type) pairs where the agent's locally computed assignment differs from the canonical assignment computed by an omniscient observer with a perfect agent roster.

### 5.2 Experimental Setup

**Environment:**
- Discrete-event simulator (no real network; focus on algorithmic convergence)
- Simulated agents: N = {100, 500, 1000, 5000} (100 is the kill-criterion threshold; higher values test scalability)
- Each agent has a unique ID and a set of 3-5 supported task types (randomly assigned from a pool of 20 task types)
- Each agent runs the full Tidal Function Engine + Scheduling Resolver + Capacity Snapshot Service locally

**Workload Profiles:**
- **Stable:** No agent churn during the measurement window. Baseline for 0% expected error.
- **Low churn:** 1% of agents join/leave per epoch (random uniform selection).
- **Medium churn:** 5% of agents join/leave per epoch.
- **High churn:** 10% of agents join/leave per epoch.
- **Burst churn:** 20% of agents leave simultaneously at epoch E, then rejoin at epoch E+2. Simulates correlated failure.

**Consistent Hash Configuration:**
- Virtual nodes per agent: V = {50, 100, 200, 500}
- Hash function: SHA-256 truncated to 64 bits
- Hash ring per task type (20 rings)

**Epoch Configuration:**
- Epoch length: 1 simulated time unit (wall-clock time is irrelevant in discrete simulation)
- Snapshot propagation: gossip protocol with TTL = ceil(log2(N)) hops
- Measurement window: 20 epochs per scenario (first 5 are warm-up)

### 5.3 Metrics to Capture

| Metric | Definition | Target |
|---|---|---|
| **Assignment error rate** | Fraction of (agent, task_type) pairs where local assignment != canonical assignment | <5% within 3 epochs of churn event |
| **Convergence time** | Number of epochs from churn event until assignment error < 5% | <= 3 epochs |
| **Steady-state error** | Assignment error rate with no churn in previous 10 epochs | 0% |
| **Redistribution fraction** | Fraction of assignments that change due to one agent joining/leaving | O(1/N) expected (consistent hashing property) |
| **Snapshot propagation latency** | Number of epochs until 95% of agents have an accurate roster | <= 2 epochs |
| **Schedule computation time** | Wall-clock time per agent to compute one epoch's schedule | < 10ms at N=1000 |
| **Substitution activation latency** | Epochs from agent failure to substitution agent taking over | <= 1 epoch |

### 5.4 Kill Criterion

**The architecture requires revision if ANY of the following hold at N=100:**

1. Assignment error rate does not drop below 5% within 3 epochs of a churn event, under the LOW CHURN profile (1% churn/epoch), with V=200 virtual nodes.
2. Steady-state error is non-zero (indicates a determinism bug or roster inconsistency).
3. Convergence time exceeds 3 epochs in >10% of trials for the MEDIUM CHURN profile.

**If the kill criterion is triggered:** The architecture design halts. The team investigates whether the issue is (a) a parameter tuning problem (solvable by adjusting virtual node count, snapshot TTL, or gossip protocol), or (b) a fundamental limitation of the consistent-hashing approach (requires architectural revision). The investigation has a 2-week time box. If no resolution is found, the architecture is revised per ADR process.

### 5.5 Expected Timeline

| Milestone | Duration | Deliverable |
|---|---|---|
| Simulator implementation | 2 weeks | Discrete-event simulator with agent lifecycle, hash ring, gossip protocol |
| Baseline experiments (stable, N=100) | 1 week | Steady-state error confirmation (expected: 0%) |
| Churn experiments (all profiles, N=100) | 1 week | Convergence time measurements, kill criterion evaluation |
| Scale experiments (N=500 to 5000) | 1 week | Scalability confirmation |
| Virtual node parameter sweep | 1 week | Optimal V for each churn profile |
| Results analysis and report | 1 week | Experiment report with go/no-go recommendation |
| **Total** | **7 weeks** | |

Target completion: DESIGN month 2 (well before the RED monitoring flag at month 3).

### 5.6 Tools and Framework Recommendations

- **Language:** Python (rapid prototyping) or Rust (if performance concerns arise at N=5000+)
- **Simulation framework:** Custom discrete-event simulator (SimPy if Python, or bare event loop). The experiment is simple enough that a general-purpose simulation framework adds more complexity than value.
- **Consistent hashing library:** Implement from scratch using SHA-256 to maintain full control over virtual node mapping. Existing libraries (e.g., `hashring`) may not expose the internals needed for experimentation.
- **VRF library:** Use an existing Micali VRF implementation (e.g., `ecvrf` in Rust, or a Python binding). The VRF is not the subject of this experiment but must be present for completeness.
- **Statistics:** Standard Python scientific stack (NumPy, pandas, matplotlib) for analysis and visualization.
- **Reproducibility:** All random seeds are fixed and recorded. All experiment configurations are stored as YAML files. Results are stored as structured data (CSV or Parquet) with full provenance.

---

## 6. Scalability Architecture

### 6.1 Per-Component Scaling Analysis

| Component | Per-Agent Computation | Communication per Epoch | Scaling with N |
|---|---|---|---|
| Tidal Function Engine | O(1) hash + O(1) VRF | None (local computation) | O(1) per agent |
| Scheduling Resolver | O(T) where T = task types (bounded) | None (local computation) | O(1) per agent |
| Verifier Set Computer | O(1) VRF per claim | None (local computation) | O(1) per agent |
| Settlement Calculator | O(E) where E = events in epoch | None (local computation) | O(events/N) per agent |
| Prediction Model Manager | O(D) where D = neighbor degree (bounded 4-10) | None (model is local) | O(1) per agent |
| Surprise Signal Router | O(D * S) where S = surprise rate | O(S * R) where R = avg radius | O(surprise_rate) per agent |
| Field Gradient Computer | O(1) (fixed 4-agent cluster) | O(3) per epoch (within cluster) | O(1) per agent |
| Tidal Version Manager | O(1) per epoch | Version field in snapshot | O(1) per agent |
| Capacity Snapshot Service | O(1) compile, O(D) propagate | O(D) outbound, O(D) inbound | O(N) aggregate, O(D) per agent |

**Net per-agent overhead:**
- **Steady state (no surprises):** O(1) computation, O(D) communication at epoch boundary
- **During surprises:** O(D * S) computation, O(S * R) communication
- **Total system communication:** O(N * D) at boundaries + O(N * S * R) for surprises
- **With predictive layer active and converged:** S -> 0, so total communication -> O(N * D) at boundaries only

### 6.2 Bottleneck Analysis

| Scale | Primary Bottleneck | Mitigation |
|---|---|---|
| 1K agents | None significant | All operations are O(1) per agent |
| 10K agents | Snapshot propagation latency | Increase gossip TTL; hierarchical aggregation via CIOS topology |
| 100K agents | Snapshot aggregate bandwidth | Compressed snapshots; delta-encoded snapshots (only changes since last epoch); hierarchical aggregation (Coordinators aggregate Implementor snapshots) |
| 1M agents | Roster size per agent | Partial roster: agents only need roster entries for agents in their hash ring neighborhood. Implement roster sharding by task type — agents only maintain roster entries for task types they participate in. |

### 6.3 Horizontal Scaling Strategy

PTA is inherently horizontally scaled — each agent is an independent computation node. There is no central server, no leader, no shared state (beyond the shared mathematical function definition and the gossip-propagated roster).

For scales above 100K agents:

1. **Hierarchical snapshot aggregation:** CIOS Coordinators aggregate snapshots from their Implementor subtrees and exchange summaries with peer Coordinators. Implementors receive aggregated views rather than individual snapshots. Reduces per-agent snapshot bandwidth from O(N) to O(sqrt(N)).

2. **Task-type roster sharding:** Agents maintain detailed roster entries only for task types they participate in. For other task types, they maintain aggregated capacity summaries. Reduces per-agent roster memory from O(N) to O(N/T) where T is the number of task types.

3. **VRF computation offloading:** At very large scales, VRF computations for all pending claims may become significant. VRF computation can be parallelized and cached — the same (claim_hash, epoch, seed) always produces the same verifier set.

### 6.4 Resource Requirements

| Scale | Per-Agent Memory | Per-Agent CPU/Epoch | Aggregate Bandwidth/Epoch |
|---|---|---|---|
| 1K agents | ~10 MB (roster + models) | ~1 ms | ~10 MB (snapshots) |
| 10K agents | ~50 MB | ~1 ms | ~500 MB (snapshots) |
| 100K agents | ~100 MB (with sharding) | ~1 ms | ~5 GB (hierarchical) |
| 1M agents | ~200 MB (with sharding) | ~1 ms | ~10 GB (hierarchical, compressed) |

Note: Epoch length determines bandwidth/time. Longer epochs spread the aggregate bandwidth over more wall-clock time. At 1M agents with 1-minute epochs, aggregate bandwidth is ~170 MB/s — well within modern network capacity.

---

## 7. Security Architecture

### 7.1 Threat Model

**Adversary capabilities:**
- Can control up to f < N/3 agents (Byzantine fault tolerance bound)
- Has full knowledge of the tidal function definition (it is public)
- Can observe all network traffic (public network assumption)
- Can selectively delay or drop messages (network adversary)
- Can attempt to manipulate the VRF seed derivation (VRF grinding)

**Attack surfaces by layer:**

| Attack | Layer | Severity | Exploitability |
|---|---|---|---|
| Schedule prediction | L1 | LOW | Scheduling is deterministic by design; predictability is a feature |
| VRF grinding | L1 | HIGH | Adversary tries to influence verifier set selection |
| Schedule manipulation | L1 | MEDIUM | Adversary exploits deterministic schedule to arrange favorable task assignments |
| Prediction model poisoning | L2 | MEDIUM | Adversary sends carefully crafted behavior to corrupt neighbor prediction models |
| Surprise suppression | L2 | MEDIUM | Adversary stays just within prediction threshold to avoid detection while corrupting outputs |
| Surprise flooding | L2 | LOW | Adversary generates many false surprises to waste communication budget |
| Field gradient poisoning | L3 | MEDIUM | Adversary reports false state to manipulate cluster gradient |
| Stealth attacks | All | HIGH | Adversary maintains tidal compliance while producing semantically incorrect outputs |
| Sybil attack | L1 | HIGH | Adversary creates many agent identities to dominate hash ring positions |

### 7.2 Defense Mechanisms

**Layer 1 (Tidal Backbone):**
- **VRF grinding prevention:** Micali VRF with periodic seed rotation at governance-controlled intervals. Seeds are derived from a chain of committed values (commitment revealed at rotation epoch). An adversary cannot predict future seeds and therefore cannot grind current actions to influence future verifier sets.
- **Sybil resistance:** Agent registration requires identity verification via CIOS (out of PTA scope). PTA trusts the CIOS-provided agent roster. Sybil defense is delegated to the identity layer.
- **Schedule manipulation:** Accepted as a known property. The schedule is deterministic and public. Defense is in the verification layer (Verichain): even if an adversary knows when they will be verified, they cannot fool the verification logic. The adversary gains no advantage from schedule knowledge because verification is content-based, not timing-based.

**Layer 2 (Predictive Communication):**
- **Two-layer defense:** An adversary must simultaneously maintain tidal compliance (Layer 1) AND fool prediction models (Layer 2) to avoid all detection signals. Maintaining tidal compliance constrains the adversary's behavior to the scheduled pattern. Fooling prediction models requires the adversary's deviation to be within the adaptive threshold. The intersection of these constraints is narrow.
- **Surprise flooding mitigation:** Per-epoch signal budget per agent (hard cap). Excessive surprises from one agent are rate-limited. Persistent flooding degrades that agent's compliance score and triggers increased Verichain scrutiny.
- **Model poisoning resistance:** Epoch-boundary recalibration resets prediction models to observed truth, limiting the duration of any poisoning attack to one epoch. Persistent statistical anomalies (even within threshold) are flagged by drift detection at recalibration.

**Layer 3 (Morphogenic Fields):**
- **Gradient poisoning defense:** With 4 agents in a cluster, a single adversary is outvoted 3:1. The coherence monitor detects when one agent's gradient response is inconsistent with the cluster's potential function. The adversary can introduce suboptimal allocation but cannot cause incorrect allocation for other cluster members.
- **Cluster integrity:** If coherence score drops below a configurable threshold, the cluster is flagged for Verichain inspection and potentially reformed at the next tidal boundary.

**Cross-layer:**
- **Stealth attack limitation:** PTA explicitly does not claim to detect semantic correctness attacks. If an adversary produces structurally and behaviorally correct but semantically wrong outputs, detection is Verichain's responsibility. PTA provides three supplementary signals (tidal compliance, behavioral prediction anomaly, field coherence) but none are sufficient for semantic verification.

### 7.3 Audit and Monitoring Points

| Monitoring Point | What Is Monitored | Alert Condition |
|---|---|---|
| Epoch clock drift | Per-agent clock offset from NTP reference | Drift > tolerance window |
| Hash ring consistency | Fraction of agents with matching hash ring state | Agreement < 99% |
| VRF seed currency | Per-agent VRF seed version | Seed older than 2 rotation periods |
| Surprise rate | System-wide surprise rate per epoch | Rate > 2x historical baseline |
| Prediction model health | Fraction of models in STANDARD (non-predictive) mode | > 50% of models degraded |
| Settlement determinism | Settlement proof hash agreement across auditors | Any disagreement |
| Migration progress | Fraction of agents on each version during overlap | Stalled migration (no progress for 3 epochs) |
| Coherence scores | Per-cluster field coherence | Score < threshold for > 3 consecutive epochs |
| Substitution activation rate | Fraction of assignments covered by substitutes | > 10% substitution rate |

---

## 8. Deployment Architecture

### 8.1 Phase 1 Deployment: Tidal Backbone

**Components deployed:**
- Tidal Function Engine
- Scheduling Resolver
- Verifier Set Computer
- Settlement Calculator
- Tidal Version Manager
- Capacity Snapshot Service
- CIOS Adapter
- Verichain Adapter
- AIC Adapter
- Knowledge Graph Adapter (basic access scheduling only)
- AASL Adapter (claim type registry only; semantic dimensions deferred to Phase 3)

**Deployment topology:**
- Each PTA agent runs the full component stack locally (no centralized services)
- Agents connect to each other via CIOS-defined topology
- Integration adapters connect to their respective subsystems via subsystem-specific transport (API, message queue, or direct call — transport is adapter-internal)

**Validation criteria before Phase 2:**
- Convergence experiment passes (Section 5)
- Integration interfaces with Verichain and CIOS are exercised with real subsystem instances
- Settlement determinism is confirmed (multiple independent agents compute identical settlement proofs)
- System operates at 100+ agents for >1000 epochs with <1% unplanned substitution rate

**Rollback strategy:**
- Phase 1 introduces PTA as a new subsystem. Rollback = remove PTA entirely. No existing subsystem is modified by Phase 1 deployment; PTA is additive.

### 8.2 Phase 2 Additions: Predictive Communication

**Components added:**
- Prediction Model Manager
- Surprise Signal Router

**Components modified:**
- Settlement Calculator: adds prediction accuracy bonus stream and surprise cost stream
- Verichain Adapter: adds anomaly signal emission

**Deployment strategy:**
- Predictive communication is deployed as an opt-in layer. Agents can run with or without it.
- Agents without the predictive layer continue to send standard messages (equivalent to all-surprise mode).
- Progressive rollout: enable on 10% of agents, measure communication reduction, expand if >30% reduction confirmed.
- The predictive layer is scoped as **enhancing but not required** (Assessment Council ADVISORY condition 3). The system must remain fully functional if the predictive layer is disabled for all agents.

**Validation criteria before Phase 3:**
- Communication reduction >30% in steady state vs. standard messaging (below this threshold, AMBER monitoring flag triggers)
- No cliff-edge behavior under model degradation (graceful fallback to standard messaging confirmed)
- Adaptive threshold stability confirmed (no oscillation over 100-epoch window)
- Behavioral anomaly signals provide actionable input to Verichain (measured by Verichain team)

**Rollback strategy:**
- Disable Prediction Model Manager and Surprise Signal Router on all agents. System reverts to standard messaging within the tidal framework. Settlement Calculator reverts to compliance-only scoring (no prediction bonuses or surprise costs). No data loss; model state is local and disposable.

### 8.3 Phase 3 Additions: Morphogenic Fields

**Components added:**
- Field Gradient Computer

**Components modified:**
- AASL Adapter: adds semantic dimension consumption for gradient space
- Verichain Adapter: adds coherence signal emission
- Tidal Function Engine: adds tetrahedral cluster assignment computation

**Deployment strategy:**
- Formal decision gate at end of Phase 2 (Assessment Council ADVISORY condition 4)
- Gate criteria: (1) Phase 2 validation criteria met, (2) potential game convergence validated in simulation (Experiment 4), (3) measurable improvement over round-robin allocation in simulated tetrahedral clusters
- If gate criteria not met: Phase 3 is simplified (replace morphogenic fields with simple load-balancing within clusters) or dropped entirely

**Rollback strategy:**
- Disable Field Gradient Computer. Tetrahedral clusters revert to round-robin task distribution within the cluster. No impact on Layers 1 or 2. Coherence signals to Verichain cease (Verichain uses remaining two signal types). Cluster assignment computation in Tidal Function Engine is retained (clusters are still useful organizational units even without gradient-based allocation).

### 8.4 Deployment Dependency Graph

```
Phase 1 (REQUIRED)                     Phase 2 (ENHANCING)       Phase 3 (GATED)
+--------------------+                  +--------------------+    +------------------+
| Tidal Function     |                  | Prediction Model   |    | Field Gradient   |
| Engine             |<-+-----------+   | Manager            |    | Computer         |
+--------------------+  |           |   +--------+-----------+    +--------+---------+
+--------------------+  |           |            |                         |
| Scheduling         |--+           |            v                         |
| Resolver           |  |           |   +--------------------+             |
+--------------------+  |           +-->| Surprise Signal    |             |
+--------------------+  |               | Router             |             |
| Verifier Set       |--+               +--------------------+             |
| Computer           |  |                                                  |
+--------------------+  |   Phase 1 must pass        Phase 2 must pass     |
+--------------------+  |   convergence experiment   validation criteria   |
| Settlement         |--+   before Phase 2 begins    + formal decision     |
| Calculator         |                                gate before Phase 3  |
+--------------------+                                begins               |
+--------------------+                                                     |
| Tidal Version      |--+                                                  |
| Manager            |  |                                                  |
+--------------------+  |                                                  |
+--------------------+  |                                                  |
| Capacity Snapshot  |--+                                                  |
| Service            |                                                     |
+--------------------+                                                     |
+--------------------+                                                     |
| Integration        |-----------------------------------------------------+
| Adapters           |  (AASL Adapter adds semantic dims in Phase 3)
+--------------------+
```

---

## 9. Decision Log

### ARCH-001: Consistent Hashing as Scheduling Primitive

**Decision:** Use consistent hashing with virtual nodes (Karger et al., 1997) as the core scheduling primitive, with one hash ring per task type.

**Rationale:** Consistent hashing provides O(1) per-agent computation, O(K/N) key redistribution on churn (where K = total assignments, N = agents), and deterministic reproducibility. Alternative approaches considered: (a) Round-robin (too rigid, no capacity awareness), (b) Auction/market (requires runtime communication, violates determinism constraint), (c) Constraint solving (NP-hard, not O(1) per agent). Consistent hashing is the only known approach that is simultaneously deterministic, O(1) per agent, and handles churn gracefully.

**Status:** ACCEPTED, pending validation by convergence experiment (Section 5).

---

### ARCH-002: Epoch-Boundary-Only Communication

**Decision:** All inter-agent communication in Layer 1 occurs exclusively at epoch boundaries via capacity snapshots. Mid-epoch communication is eliminated entirely for the tidal backbone.

**Rationale:** This is the key insight that enables O(1) per-agent steady-state overhead. By constraining communication to epoch boundaries, we accept that capacity information may be up to one epoch stale, but we eliminate the O(N^2) messaging that causes existing systems to hit the 30-agent ceiling. The tradeoff is favorable: stale capacity data produces suboptimal (but not incorrect) scheduling, while eliminated mid-epoch communication provides the scaling breakthrough.

**Status:** ACCEPTED.

---

### ARCH-003: Predictive Layer as Enhancement, Not Requirement

**Decision:** The predictive delta communication layer (Layer 2) is architecturally optional. The tidal backbone (Layer 1) must be fully functional and valuable without it.

**Rationale:** Assessment Council ADVISORY condition 3. The predictive layer has feasibility score 3 (lowest of the three layers). Making it required would create a dependency on the least-proven component. Making it enhancing ensures that Phase 1 delivers standalone value and that predictive communication failure (slow convergence, model instability) does not compromise the core system.

**Status:** ACCEPTED (Assessment Council condition).

---

### ARCH-004: Morphogenic Fields Scoped to 4-Agent Clusters

**Decision:** Morphogenic field allocation operates exclusively within tetrahedral (4-agent) clusters.

**Rationale:** Potential game convergence (Monderer-Shapley 1996) is trivially guaranteed at 4 agents. Gradient computation in 4 dimensions is computationally negligible. The curse of dimensionality is entirely eliminated. The Visionary's dissent (expand to larger clusters) is noted and deferred: if Experiment 4 shows strong results, expansion can be evaluated. Current scope prioritizes certainty of convergence over generality.

**Status:** ACCEPTED, with expansion as a future option.

---

### ARCH-005: Schelling-Point Migration for Version Transitions

**Decision:** Tidal function version migration uses Schelling-point coordination (agents switch when they observe sufficient peers on the new version) rather than formal consensus.

**Rationale:** Formal consensus would contradict PTA's zero-consensus design principle. Schelling-point migration is the minimum-coordination approach that can achieve version transition. The risk of split-brain is mitigated by bounded overlap periods with automatic rollback. This is the single weakest point in the otherwise-deterministic architecture, and Experiment 5 specifically tests its reliability.

**Status:** ACCEPTED, pending validation by Experiment 5.

---

### ARCH-006: Three-Signal Verification Input

**Decision:** PTA provides three independent signals to Verichain for verification decisions: (1) tidal compliance (L1), (2) behavioral prediction anomaly (L2), (3) field coherence (L3). PTA does not make verification decisions itself.

**Rationale:** Clean separation of concerns. PTA is a coordination layer, not a verification layer. Combining three independent signals increases the difficulty for an adversary (must fool all three simultaneously) without requiring PTA to understand verification logic. Semantic correctness verification is explicitly out of scope and delegated to Verichain.

**Status:** ACCEPTED.

---

### ARCH-007: Gossip-Based Snapshot Propagation

**Decision:** Capacity snapshots are propagated using a gossip protocol over the CIOS hierarchy topology with TTL = ceil(log2(N)) hops.

**Rationale:** Gossip provides probabilistic but efficient propagation without requiring a central aggregation point. TTL = ceil(log2(N)) ensures coverage within O(log(N)) rounds while bounding bandwidth. At large scales (>100K agents), hierarchical aggregation via CIOS Coordinators supplements gossip to reduce per-agent bandwidth. Alternative considered: tree-based aggregation (more structured but fragile to node failure at internal nodes).

**Status:** ACCEPTED.

---

### ARCH-008: Deterministic Settlement with Grace Period

**Decision:** Settlement computation uses a deterministic function over the tidal schedule and recorded events, with a 1-epoch grace period for late-arriving events.

**Rationale:** Pure determinism (any observer can independently compute identical settlement) is essential for auditability and dispute-free economics. The grace period acknowledges that network delays may cause some events to arrive after the settlement epoch boundary. Without the grace period, agents in partitioned network segments would systematically lose settlement credit. The grace period length (1 epoch) bounds the delay while providing fairness.

**Status:** ACCEPTED.

---

### ARCH-009: Adapter-Based Integration Pattern

**Decision:** All external integrations use typed, versioned adapter components that encapsulate serialization, error handling, retries, and transport details.

**Rationale:** Narrow adapter interfaces ensure that PTA's internal components are decoupled from external subsystem implementation details. Each adapter can be independently tested with mock subsystems. Transport changes (e.g., switching from API to message queue) require only adapter changes, not component changes. This also supports the phased deployment strategy: adapters for Phase 2 and 3 features can be added without modifying Phase 1 adapters.

**Status:** ACCEPTED.

---

*Architecture document produced 2026-03-09. Subject to revision based on convergence experiment results (Section 5) and integration interface testing.*


---

# Part II — Technical Specification: Core + Layer 1 (Tidal Backbone)

---

---

## 1. Specification Overview

### 1.1 Scope

PTA is a **coordination layer only**. It computes who does what, when, and with whom — deterministically. PTA does not:

- Execute tasks (delegated to agents via CIOS roles)
- Verify claims (delegated to Verichain)
- Define semantic structures (delegated to AASL)
- Manage tokens (delegated to AIC)
- Persist knowledge (delegated to the Knowledge Graph)

PTA provides three layered capabilities:

| Layer | Name | Status | Dependency |
|-------|------|--------|------------|
| Layer 1 | Tidal Backbone | REQUIRED | Standalone — viable without Layers 2 or 3 |
| Layer 2 | Predictive Delta Communication | ENHANCING | Requires Layer 1 |
| Layer 3 | Morphogenic Field Allocation | GATED | Requires Layers 1 and 2; formal decision gate |

This document (Part 1) fully specifies Layer 1. Layers 2 and 3 are specified in Part 2.

### 1.2 Normative and Informative Sections

**Normative sections** (implementations MUST conform):
- Section 2: System Primitives — all data structures, invariants, and lifecycle rules
- Section 3: Tidal Backbone Protocol — all algorithms, data formats, and protocol sequences
- Section 4: Algorithm Pseudocode — reference implementations
- Section 5: Test Vectors — determinism conformance tests

**Informative sections** (context and rationale):
- Section 1: this overview
- Rationale paragraphs within normative sections (marked with "Rationale:")
- Complexity annotations (Big-O notations are targets, not hard constraints)

### 1.3 Dependencies

PTA Layer 1 depends on the following external subsystems through narrow, typed interfaces:

| Subsystem | What PTA Consumes | What PTA Provides |
|-----------|-------------------|-------------------|
| **Verichain** | Verification results, verification receipts | Verifier set assignments (claim_hash, epoch, verifier_set, vrf_proof) |
| **CIOS** | Hierarchy topology, role assignments, task filter rules, scheduling parameters | Epoch schedules, compliance reports, substitution events |
| **AASL** | Claim type registry (maps to task-type parameters) | Type consistency reports |
| **AIC** | Settlement confirmations, economic parameters | Settlement ledgers with deterministic proofs |
| **Knowledge Graph** | Lifecycle status (active/archival/deprecated) | Access window schedules |

PTA does not share mutable state with any dependency. All integration is via message exchange through versioned adapter interfaces.

### 1.4 Conventions

- All byte sequences are big-endian unless otherwise noted.
- `||` denotes byte-string concatenation.
- `uint64` is an unsigned 64-bit integer.
- `bytes32` is a 32-byte (256-bit) fixed-length byte string.
- `AgentID` is a `bytes32` representing a unique agent identifier.
- `TaskType` is a `bytes32` representing an AASL-defined claim type identifier.
- Hash function references to "SHA-256" mean SHA-256 as defined in FIPS 180-4.
- VRF references to "ECVRF" mean the Elliptic Curve VRF as defined in RFC 9381 (ECVRF-EDWARDS25519-SHA512-ELL2).
- The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" are interpreted as described in RFC 2119.

---

## 2. System Primitives (Formal Definitions)

This section defines all eight system primitives. Each primitive is specified with a formal definition, data structure, invariants, lifecycle, and serialization notes.

---

### 2.1 Epoch

#### Formal Definition

An **Epoch** is a discrete, bounded time interval that serves as the fundamental unit of tidal coordination. All scheduling, settlement, verification assignment, and model recalibration are epoch-relative. Formally:

Let E = {e_0, e_1, e_2, ...} be a totally ordered, countably infinite sequence of epochs where:
- e_i < e_{i+1} for all i >= 0
- Each e_i has a wall-clock start time t_start(e_i) and end time t_end(e_i)
- t_end(e_i) = t_start(e_{i+1}) (epochs are contiguous, no gaps)
- t_end(e_i) - t_start(e_i) = epoch_length (constant within a tidal version)

#### Data Structure

```
Epoch {
    epoch_number:    uint64          // Monotonically increasing counter, starting at 0
    epoch_length_ms: uint64          // Duration in milliseconds; configurable per tidal version
    start_time_ms:   uint64          // Wall-clock start time (Unix epoch milliseconds)
    version_id:      bytes32         // Tidal version under which this epoch operates
}
```

**Field constraints:**
- `epoch_number` MUST be strictly monotonically increasing (no gaps, no reuse).
- `epoch_length_ms` MUST be > 0. Minimum: 100ms. Maximum: 3,600,000ms (1 hour).
- `start_time_ms` MUST equal `start_time_ms` of epoch 0 + (`epoch_number` * `epoch_length_ms`), subject to clock drift tolerance.
- `version_id` MUST reference a valid, active tidal version.

#### Invariants

1. **Monotonicity:** For any two epochs observed by any agent, if e_a.epoch_number < e_b.epoch_number, then e_a.start_time_ms < e_b.start_time_ms.
2. **Contiguity:** There MUST NOT exist a wall-clock interval that falls between two consecutive epochs and belongs to neither.
3. **Uniqueness:** No two distinct epochs share the same epoch_number.
4. **Determinism:** Given epoch_number and the active tidal version, start_time_ms is deterministically computable by any agent.

#### Creation/Destruction Lifecycle

- **Creation:** An epoch begins when the epoch clock ticks past the computed start_time_ms. Epoch 0 is created at system genesis (deployment of the first tidal version).
- **Active:** An epoch is active from its start_time_ms until its start_time_ms + epoch_length_ms.
- **Closed:** An epoch is closed when its successor epoch begins. A closed epoch's data (schedules, events, settlements) is immutable.
- **Destruction:** Epochs are never destroyed. Historical epoch data MAY be pruned after a governance-defined retention period, but epoch_numbers are never reused.

#### Serialization

Epochs are serialized as a packed binary structure: `[epoch_number: 8 bytes][epoch_length_ms: 8 bytes][start_time_ms: 8 bytes][version_id: 32 bytes]` = 56 bytes total. Canonical byte order is big-endian.

---

### 2.2 Tidal Function

#### Formal Definition

A **Tidal Function** is a deterministic, pure function that maps agent identity, task type, and epoch to a coordination output. Formally:

```
TF: (AgentID, TaskType, uint64) -> Assignment
```

where `Assignment` is a structured output containing scheduling decisions, verifier set membership, and settlement boundary indicators. The function is **pure**: given identical inputs, any evaluator MUST produce an identical output. The function has **no side effects** and references **no mutable external state** — only the immutable tidal version parameters.

The tidal function is decomposed into three sub-functions:

1. **Schedule function:** `schedule(agent_id, task_type, epoch, capacity_snapshot) -> assignment_set`
2. **Verifier function:** `verify(claim_hash, epoch, seed) -> verifier_set`
3. **Settlement boundary function:** `is_settlement(epoch) -> bool`

#### Data Structure

```
TidalFunction {
    version_id:         bytes32               // Unique identifier for this function version
    hash_ring_config:   HashRingConfig        // Consistent hash ring parameters
    vrf_seed:           bytes32               // Current VRF seed
    epoch_length_ms:    uint64                // Epoch duration
    task_type_bands:    map<TaskType, Band>   // Frequency band per task type
    settlement_interval: uint64               // Settlement occurs every N epochs
    verifier_set_size:  uint32                // Number of verifiers per claim (k)
    virtual_nodes_per_agent: uint32           // Number of virtual nodes per agent on hash ring
}

HashRingConfig {
    hash_function:    "SHA-256"               // Fixed; not configurable
    ring_bits:        uint32                  // Hash ring size = 2^ring_bits; default 64
    replication_factor: uint32                // Virtual nodes per agent (alias for virtual_nodes_per_agent)
}

Band {
    task_type:        TaskType
    frequency:        uint32                  // How many epochs between activations (1 = every epoch)
    phase_offset:     uint32                  // Offset within frequency cycle (0 to frequency-1)
}
```

**Field constraints:**
- `version_id` MUST be unique across all published tidal function versions.
- `vrf_seed` MUST be exactly 32 bytes. MUST NOT be all-zeros.
- `virtual_nodes_per_agent` MUST be in range [1, 1000]. Recommended: 150.
- `verifier_set_size` MUST be in range [1, 100]. Recommended: 5.
- `settlement_interval` MUST be >= 1.
- For each Band: `phase_offset` MUST be < `frequency`.

#### Invariants

1. **Purity:** TF(a, t, e) = TF(a, t, e) for all evaluators, given the same tidal version parameters. No randomness, no external state.
2. **Completeness:** For every registered (agent_id, task_type) pair where the agent has the capability for that task type, and for every epoch where the task type's band is active, the function produces a defined assignment.
3. **Consistency:** If two agents evaluate TF with the same inputs and the same tidal version, they MUST produce bit-identical outputs.

#### Creation/Destruction Lifecycle

- **Created:** When governance publishes a new tidal version definition.
- **Pending:** Published but not yet at activation_epoch.
- **Active:** From activation_epoch until deactivation_epoch.
- **Overlap:** During version migration, two tidal functions may be simultaneously active (old and new). See Tidal Version primitive.
- **Deactivated:** After deactivation_epoch. The function definition is retained for auditability but MUST NOT be used for new scheduling.

#### Serialization

The TidalFunction is serialized as a versioned binary blob. The first 4 bytes are a format version (uint32), followed by the canonical encoding of all fields. Maps are serialized as sorted key-value pairs (sorted by key bytes, lexicographic). The SHA-256 hash of the serialized blob is the `version_id`.

---

### 2.3 Prediction Model

#### Formal Definition

A **Prediction Model** is a lightweight statistical model maintained by an agent for a single direct neighbor. It predicts the neighbor's behavior relative to the tidal schedule within the next epoch. Formally:

Let M_{a->b} denote the prediction model that agent a maintains for neighbor b. Then:

```
M_{a->b}(epoch) -> predicted_behavior_vector
```

where `predicted_behavior_vector` is a vector of expected observables (task completions, resource consumption, communication patterns). The model is linear: `predicted = W * features + bias`, where W is a weight matrix, features are derived from the neighbor's recent history and the tidal schedule, and bias is a constant offset.

*Rationale: Linear models provide O(1) per-neighbor per-epoch computation and sufficient expressiveness for tidal-schedule-compliance prediction. Nonlinear extensions are a research question (see refined concept, research_questions).*

#### Data Structure

```
PredictionModel {
    owner_agent_id:     AgentID           // Agent maintaining this model
    neighbor_agent_id:  AgentID           // Agent being modeled
    weights:            float64[]         // Weight vector; length = feature_dimension
    bias:               float64[]         // Bias vector; length = output_dimension
    feature_dimension:  uint32            // Number of input features
    output_dimension:   uint32            // Number of predicted observables
    accuracy:           float64           // Rolling accuracy metric [0.0, 1.0]
    surprise_threshold: float64           // Current adaptive threshold for surprise detection
    communication_mode: enum {STANDARD, TRANSITIONING, PREDICTIVE}
    last_calibration_epoch: uint64        // Epoch of most recent recalibration
    history_window:     uint32            // Number of past epochs retained for calibration
}
```

**Field constraints:**
- `feature_dimension` MUST be in range [1, 64].
- `output_dimension` MUST be in range [1, 32].
- `accuracy` MUST be in range [0.0, 1.0].
- `surprise_threshold` MUST be > 0.0.
- `history_window` MUST be >= 1.
- `communication_mode` transitions: STANDARD -> TRANSITIONING -> PREDICTIVE (forward only, except on model reset which returns to STANDARD).

#### Invariants

1. **Bounded neighbors:** An agent MUST NOT maintain more prediction models than its CIOS hierarchy degree (typically 4-10).
2. **Epoch-aligned calibration:** Model recalibration MUST occur at epoch boundaries only.
3. **Threshold positivity:** `surprise_threshold` MUST remain strictly positive at all times.
4. **Mode monotonicity:** Under normal operation, communication_mode advances forward. Backward transitions (to STANDARD) occur only on explicit model reset.

#### Creation/Destruction Lifecycle

- **Created:** When a neighbor is added to the agent's CIOS hierarchy adjacency list. Initial state: `communication_mode = STANDARD`, `accuracy = 0.0`, `weights` and `bias` initialized to zero.
- **Calibrating:** During STANDARD mode, the model accumulates observations without suppressing communication. After `accuracy` exceeds a configurable activation threshold (default: 0.6), mode transitions to TRANSITIONING.
- **Transitioning:** Model predictions are compared against observations but both standard and predictive communication occur. After `accuracy` exceeds a confirmation threshold (default: 0.8) for a configurable number of consecutive epochs (default: 5), mode transitions to PREDICTIVE.
- **Active (PREDICTIVE):** Only surprise signals are transmitted; predicted behavior is assumed correct unless deviation exceeds threshold.
- **Reset:** If accuracy drops below a floor (default: 0.3), or if recalibration error exceeds a ceiling, the model resets to STANDARD with zeroed weights.
- **Destroyed:** When the neighbor is removed from the CIOS hierarchy adjacency list.

#### Serialization

Prediction models are local to each agent and not transmitted on the wire. Serialization format is implementation-defined. For persistence, a simple packed float64 array suffices.

---

### 2.4 Surprise Signal

#### Formal Definition

A **Surprise Signal** is a delta-encoded message transmitted when an observed behavior deviates from predicted behavior by more than the adaptive threshold. Formally:

Let `observed` = actual behavior vector of neighbor b as observed by agent a at epoch e. Let `predicted` = M_{a->b}(e). Then a surprise signal is generated if and only if:

```
||observed - predicted||_2 > surprise_threshold_{a->b}
```

where `||.||_2` is the L2 (Euclidean) norm.

#### Data Structure

```
SurpriseSignal {
    signal_id:          bytes32         // SHA-256(source_agent_id || epoch || sequence_number)
    source_agent_id:    AgentID         // Agent that generated this signal
    subject_agent_id:   AgentID         // Agent whose behavior deviated
    epoch:              uint64          // Epoch in which the deviation occurred
    prediction_error:   float64[]       // Error vector (observed - predicted)
    magnitude:          float64         // L2 norm of prediction_error
    propagation_radius: uint32          // Maximum hop count for propagation
    hop_count:          uint32          // Current hop count (incremented at each relay)
    damping_factor:     float64         // Multiplicative decay per hop (0.0, 1.0)
    timestamp_ms:       uint64          // Wall-clock time of generation
}
```

**Field constraints:**
- `signal_id` MUST be globally unique.
- `magnitude` MUST equal `||prediction_error||_2` (within floating-point tolerance of 1e-10).
- `propagation_radius` MUST be >= 1.
- `hop_count` MUST be <= `propagation_radius`. A signal with `hop_count == propagation_radius` MUST NOT be further propagated.
- `damping_factor` MUST be in range (0.0, 1.0).
- `source_agent_id` MUST NOT equal `subject_agent_id` (agents do not self-report surprises; peers detect them).

#### Invariants

1. **Magnitude-radius proportionality:** `propagation_radius = min(ceil(magnitude / radius_scale_factor), max_radius)` where `radius_scale_factor` and `max_radius` are tidal version parameters.
2. **Damping monotonicity:** The effective magnitude at hop h is `magnitude * damping_factor^h`. Effective magnitude MUST decrease strictly with each hop.
3. **Budget constraint:** Each agent MUST NOT originate more than `max_signals_per_epoch` surprise signals per epoch (a tidal version parameter; default: 100).
4. **Deduplication:** An agent MUST NOT relay a signal it has already relayed or originated (tracked by signal_id).

#### Creation/Destruction Lifecycle

- **Created:** By the Prediction Model Manager when `||observed - predicted||_2 > surprise_threshold`.
- **Propagated:** By the Surprise Signal Router to agents within `propagation_radius` hops on the CIOS topology, with `hop_count` incremented and effective magnitude decayed at each hop.
- **Consumed:** By receiving agents' Prediction Model Managers, which update their local models for the subject agent.
- **Recorded:** By the Event Recorder for settlement cost accounting.
- **Expired:** Surprise signals older than 2 epochs MUST be discarded and not relayed.

#### Serialization

Wire format: `[signal_id: 32][source_agent_id: 32][subject_agent_id: 32][epoch: 8][prediction_error_length: 4][prediction_error: 8*N][magnitude: 8][propagation_radius: 4][hop_count: 4][damping_factor: 8][timestamp_ms: 8]`. All integers big-endian, floats IEEE 754 binary64 big-endian.

---

### 2.5 Field Gradient

#### Formal Definition

A **Field Gradient** is a vector in AASL-defined semantic space representing the local direction of greatest unmet task demand within a tetrahedral (4-agent) cluster. Formally:

Let C = {a_1, a_2, a_3, a_4} be a tetrahedral cluster. Let S be the AASL-defined semantic space with dimension d. Let Phi: S^4 -> R be the potential function over the cluster state. Then the field gradient for agent a_i is:

```
g_i = -nabla_{s_i} Phi(s_1, s_2, s_3, s_4)
```

where s_i is agent a_i's position in semantic space (representing its current task allocation). Under the potential game framework (Monderer & Shapley, 1996), iterative gradient descent converges to a Nash equilibrium (a local minimum of Phi).

#### Data Structure

```
FieldGradient {
    cluster_id:        bytes32          // Identifier for the tetrahedral cluster
    agent_id:          AgentID          // Agent for which this gradient is computed
    epoch:             uint64           // Epoch in which gradient is valid
    gradient_vector:   float64[]        // Direction vector; length = semantic_dimension
    semantic_dimension: uint32          // Dimensionality of the AASL semantic space
    step_size:         float64          // Gradient descent step size for this iteration
    potential_value:   float64          // Current value of Phi at this agent's position
    convergence_flag:  bool             // True if cluster has reached Nash equilibrium
}
```

**Field constraints:**
- `gradient_vector` length MUST equal `semantic_dimension`.
- `semantic_dimension` MUST be in range [1, 64].
- `step_size` MUST be > 0.0.
- `cluster_id` MUST reference a valid tetrahedral cluster of exactly 4 agents.

#### Invariants

1. **Potential decrease:** If agent a_i moves in direction g_i with step_size, then Phi MUST not increase (within numerical tolerance). Formally: Phi(s_1, ..., s_i + step_size * g_i, ..., s_4) <= Phi(s_1, ..., s_i, ..., s_4) + epsilon, where epsilon = 1e-8.
2. **Convergence:** If `convergence_flag = true`, then `||g_i||_2 < convergence_threshold` for all i in {1,2,3,4}.
3. **Cluster scope:** Gradients are defined only within a tetrahedral cluster. There is no inter-cluster gradient.

#### Creation/Destruction Lifecycle

- **Created:** At each sub-epoch gradient computation step (multiple steps per epoch are permitted).
- **Updated:** After each agent adjusts its position along the gradient.
- **Reset:** At epoch boundaries, a tidal reset perturbation is injected: each agent's position is perturbed by a random vector scaled by `perturbation_magnitude * cooling_factor^epoch`, analogous to simulated annealing. The perturbation seed is deterministic: `SHA-256(cluster_id || epoch)`.
- **Destroyed:** When the cluster is dissolved (at a tidal boundary due to agent failure or rebalancing).

#### Serialization

Field gradients are exchanged only within the 4-agent cluster. Wire format is implementation-defined but MUST include all fields above. Recommended: packed binary with IEEE 754 floats.

---

### 2.6 Verifier Set

#### Formal Definition

A **Verifier Set** is a deterministic set of agent IDs selected to verify a specific claim at a specific epoch. Formally:

```
verifier_set = SelectTopK(VRF(claim_hash || epoch_bytes || seed), eligible_agents, k)
```

where:
- `VRF` is the ECVRF function (RFC 9381) producing a pseudorandom output
- `claim_hash` is the SHA-256 hash of the claim to be verified
- `epoch_bytes` is the big-endian 8-byte encoding of the epoch number
- `seed` is the current VRF seed from the active tidal version
- `eligible_agents` is the sorted list of agents with verification capability
- `k` is the `verifier_set_size` from the tidal version
- `SelectTopK` maps the VRF output to k agents from the eligible list (see Section 3.2)

#### Data Structure

```
VerifierSet {
    claim_hash:           bytes32         // Hash of the claim being verified
    epoch:                uint64          // Epoch at which verification occurs
    verifiers:            AgentID[]       // Ordered list of selected verifier agent IDs; length = k
    substitution_list:    AgentID[]       // Ordered fallback verifiers; length = k
    vrf_output:           bytes32         // Raw VRF output (for proof verification)
    vrf_proof:            bytes            // VRF proof (variable length per RFC 9381)
    seed_version:         uint64          // Identifies which VRF seed was used
}
```

**Field constraints:**
- `verifiers` length MUST equal `min(k, |eligible_agents|)`.
- `substitution_list` length MUST equal `min(k, |eligible_agents| - k)`.
- `verifiers` and `substitution_list` MUST be disjoint.
- All agent IDs in `verifiers` and `substitution_list` MUST be members of `eligible_agents`.
- `vrf_proof` MUST be verifiable by any agent holding the VRF public key.

#### Invariants

1. **Determinism:** Given identical (claim_hash, epoch, seed, eligible_agents, k), any evaluator MUST produce the same verifier_set.
2. **Unpredictability:** Without knowledge of `seed`, the verifier set for a future epoch is computationally unpredictable (VRF security property).
3. **Uniqueness per claim-epoch:** For a given (claim_hash, epoch), there is exactly one valid verifier set.
4. **Anti-grinding:** Changing `claim_hash` does not give the claimer useful control over which agents are selected (VRF property).

#### Creation/Destruction Lifecycle

- **Created:** When a claim requires verification at a given epoch. Computed by any agent via the VRF.
- **Emitted:** Sent to Verichain via the Verichain Adapter as a `VerifierSetAssignment`.
- **Active:** During the verification epoch. Verifiers perform their duties.
- **Settled:** After verification results are returned and included in settlement.
- **Archived:** The verifier set record is retained for auditability. Never destroyed.

#### Serialization

Wire format: `[claim_hash: 32][epoch: 8][verifier_count: 4][verifiers: 32*k][substitution_count: 4][substitution_list: 32*k][vrf_output: 32][vrf_proof_length: 4][vrf_proof: variable][seed_version: 8]`. Big-endian integers.

---

### 2.7 Settlement Boundary

#### Formal Definition

A **Settlement Boundary** is an epoch boundary at which economic settlement is computed and finalized. Formally:

```
is_settlement(epoch) = (epoch.epoch_number % settlement_interval == 0)
```

where `settlement_interval` is defined in the active tidal version. At each settlement boundary, a deterministic settlement function computes AIC token transfers based on tidal compliance, surprise costs, prediction accuracy, and verification participation.

#### Data Structure

```
SettlementBoundary {
    epoch:                 uint64                              // The settlement epoch
    settlement_interval:   uint64                              // From tidal version
    settlement_ledger:     map<AgentID, SettlementEntry>       // Per-agent settlement
    settlement_proof:      bytes32                             // SHA-256 of deterministic settlement inputs + outputs
    grace_period_epochs:   uint64                              // Late-event acceptance window (default: 1)
    finalized:             bool                                // True after grace period expires
}

SettlementEntry {
    agent_id:              AgentID
    compliance_score:      float64          // [0.0, 1.0]
    compliance_reward:     int64            // AIC units earned for tidal compliance
    surprise_cost:         int64            // AIC units charged for surprise generation (negative)
    prediction_bonus:      int64            // AIC units earned for prediction accuracy (Phase 2; 0 in Phase 1)
    verification_reward:   int64            // AIC units earned for verification duty completion
    net_delta:             int64            // Sum of all components
}
```

**Field constraints:**
- `settlement_interval` MUST be >= 1.
- `compliance_score` MUST be in range [0.0, 1.0].
- `net_delta` MUST equal `compliance_reward + surprise_cost + prediction_bonus + verification_reward`.
- `settlement_proof` MUST be deterministically reproducible from the settlement inputs.
- `grace_period_epochs` MUST be >= 0. Default: 1.

#### Invariants

1. **Periodicity:** Settlement boundaries occur at exactly every `settlement_interval` epochs. No skips, no extras.
2. **Determinism:** Given identical inputs (tidal schedule, event log, economic parameters), any evaluator MUST produce an identical `settlement_ledger` and `settlement_proof`.
3. **Conservation:** The sum of all `net_delta` values across all agents in a settlement MAY be non-zero (the system may mint or burn AIC as a policy decision). However, within a single settlement, the computation MUST be reproducible.
4. **Finality:** Once `finalized = true`, the settlement MUST NOT be modified.

#### Creation/Destruction Lifecycle

- **Created:** At each settlement epoch boundary.
- **Pending:** During the grace period, the settlement accepts late-arriving events.
- **Finalized:** After the grace period expires. The settlement_proof is computed and the ledger is emitted to the AIC Adapter.
- **Archived:** Finalized settlements are retained indefinitely for auditability.

#### Serialization

Settlement ledgers are serialized as sorted (by agent_id) key-value pairs. Each entry is packed binary. The `settlement_proof` is `SHA-256(epoch || settlement_interval || sorted_serialized_entries || economic_parameters_hash)`.

---

### 2.8 Tidal Version

#### Formal Definition

A **Tidal Version** is a complete, immutable parameter set that defines the behavior of all tidal functions for a range of epochs. Formally:

```
TidalVersion = (version_id, parameters, activation_epoch, deactivation_epoch)
```

where `parameters` includes hash ring configuration, VRF seeds, epoch length, task-type frequency bands, settlement interval, economic parameters, and virtual node count. At most two tidal versions may be simultaneously active during an overlap (migration) period.

#### Data Structure

```
TidalVersion {
    version_id:            bytes32          // SHA-256 of canonical serialization of parameters
    version_number:        uint64           // Monotonically increasing version counter
    parameters:            TidalFunction    // Full tidal function parameter set (see Section 2.2)
    activation_epoch:      uint64           // First epoch this version is active
    deactivation_epoch:    uint64           // Last epoch this version is active (0 = indefinite)
    overlap_duration:      uint64           // Number of epochs of dual-version operation during migration
    migration_threshold:   float64          // Fraction of peers required before switching [0.5, 1.0)
    published_at_ms:       uint64           // Wall-clock time of governance publication
    publisher_id:          AgentID          // Governance entity that published this version
    status:                enum {PUBLISHED, PENDING, ACTIVE, OVERLAP, DEACTIVATED, ROLLED_BACK}
}
```

**Field constraints:**
- `version_id` MUST equal `SHA-256(canonical_serialize(parameters))`.
- `version_number` MUST be strictly greater than all previously published version numbers.
- `activation_epoch` MUST be > current epoch at time of publication (no retroactive activation).
- `deactivation_epoch` MUST be > `activation_epoch` or 0 (indefinite).
- `overlap_duration` MUST be in range [1, 100]. Default: 10.
- `migration_threshold` MUST be in range [0.5, 1.0). Default: 0.67.

#### Invariants

1. **Immutability:** Once published, a tidal version's parameters MUST NOT change. To modify parameters, a new version MUST be published.
2. **At-most-two:** At any epoch, at most two tidal versions may have status ACTIVE or OVERLAP simultaneously.
3. **Ordered activation:** If version A has version_number < version B's version_number, then A's activation_epoch MUST be < B's activation_epoch.
4. **Rollback safety:** If migration fails (threshold not met within overlap), the new version is set to ROLLED_BACK and the old version continues as ACTIVE.
5. **Cooldown:** A new version MUST NOT be published within `overlap_duration` epochs of the previous version's activation_epoch (prevents cascading migrations).

#### Creation/Destruction Lifecycle

- **Published:** Governance creates and signs a new tidal version. Status = PUBLISHED.
- **Pending:** Before activation_epoch. Status = PENDING.
- **Active:** From activation_epoch onward (if no new version triggers overlap). Status = ACTIVE.
- **Overlap:** When a newer version activates, both old and new are evaluated. Status = OVERLAP for both during the overlap window.
- **Migration:** Agents switch to the new version when they observe `migration_threshold` fraction of peers on the new version.
- **Deactivated:** After successful migration, the old version is deactivated. Status = DEACTIVATED.
- **Rolled back:** If migration fails, the new version is rolled back. Status = ROLLED_BACK.

#### Serialization

Canonical serialization: all fields in declaration order, maps sorted by key, strings as length-prefixed UTF-8, integers as big-endian. The `version_id` is the SHA-256 hash of this canonical serialization (excluding the `version_id` field itself).

---

## 3. Tidal Backbone Protocol (Layer 1) — Complete Specification

This section fully specifies the Layer 1 Tidal Backbone protocol. An implementation conforming to this section MUST produce bit-identical outputs for identical inputs.

---

### 3.1 Consistent Hash Ring

#### 3.1.1 Hash Function

The hash function for all ring operations is **SHA-256** (FIPS 180-4), truncated to 64 bits by taking the first 8 bytes of the SHA-256 output. This produces a ring position in the space [0, 2^64).

```
ring_position(input: bytes) -> uint64 =
    SHA-256(input)[0..8] interpreted as big-endian uint64
```

*Rationale: SHA-256 provides collision resistance and uniform distribution. Truncation to 64 bits is sufficient for ring operations at planetary scale (2^64 positions for at most ~10^12 agents). Full 256-bit hashing is used for content addressing and VRF; 64-bit truncation is used only for ring placement.*

#### 3.1.2 Virtual Node Mapping Algorithm

Each agent is mapped to V virtual nodes on each hash ring, where V = `virtual_nodes_per_agent` from the active tidal version.

**Virtual node identifier:**

```
vnode_id(agent_id: AgentID, task_type: TaskType, index: uint32) -> bytes =
    agent_id || task_type || big_endian_bytes(index)
```

**Virtual node position on ring:**

```
vnode_position(agent_id, task_type, index) -> uint64 =
    ring_position(vnode_id(agent_id, task_type, index))
```

**Ring construction:**

For a given task type T and agent roster R = {a_1, ..., a_N}:

1. For each agent a_i in R, compute V virtual node positions: `{vnode_position(a_i, T, j) | j in [0, V)}`.
2. Optionally, weight the virtual node count by agent capacity: `V_i = round(V * capacity_weight(a_i))`, where `capacity_weight(a_i)` is normalized such that the average is 1.0. Minimum virtual node count per agent: 1.
3. Sort all virtual nodes by their ring position to form the ordered ring.
4. The ring wraps: the successor of the highest-position node is the lowest-position node.

**Key-to-agent lookup:**

Given a key K (a task identifier or claim hash), find the responsible agent:

```
lookup(K: bytes, ring: SortedVirtualNodes) -> AgentID =
    position = ring_position(K)
    vnode = first virtual node in ring with position >= position
    if no such vnode exists: vnode = first virtual node in ring (wrap-around)
    return vnode.agent_id
```

**Complexity:** O(log(N*V)) per lookup via binary search on the sorted ring.

#### 3.1.3 Ring Partitioning for Task Types

Each task type has its own independent hash ring. Rings are computed identically but with different `task_type` values in the virtual node identifier, ensuring that the same agent occupies different positions on different task-type rings.

**Active rings per epoch:**

Not all task-type rings are active every epoch. Each task type has a frequency band (Section 2.2). A task-type ring is active at epoch e if and only if:

```
is_active(task_type, epoch) = ((epoch - band.phase_offset) % band.frequency == 0)
```

#### 3.1.4 Key Redistribution on Agent Join/Leave

When an agent joins or leaves, only the keys that hash to positions between the joining/leaving agent's virtual nodes and their predecessors on the ring are affected. The expected number of affected keys is O(K/N), where K is the total number of keys and N is the total number of agents.

**On agent join (agent a_new):**

1. Compute a_new's V virtual node positions for each active task-type ring.
2. For each virtual node v_new at position p_new:
   - Find the predecessor virtual node v_pred at position p_pred (the virtual node immediately before p_new on the ring).
   - Find the successor virtual node v_succ at position p_succ (the virtual node immediately after p_new, which was previously responsible for keys in (p_pred, p_new]).
   - Keys in the range (p_pred, p_new] are transferred from v_succ.agent_id to a_new.
3. Expected keys transferred: K * V / (N * V + V) = K / (N + 1) across all virtual nodes.

**On agent leave (agent a_leaving):**

1. For each virtual node v_leaving of a_leaving:
   - Find the successor virtual node v_succ.
   - Keys in v_leaving's range are transferred to v_succ.agent_id.
2. Expected keys transferred: K / N.

*No global rebalancing is needed. Only neighbors on the ring are affected.*

---

### 3.2 VRF Specification

#### 3.2.1 Algorithm

PTA uses **ECVRF-EDWARDS25519-SHA512-ELL2** as defined in RFC 9381 (Section 5.5). This provides:

- A pseudorandom output indistinguishable from random to anyone without the secret key.
- A proof that the output was correctly derived from the input and the secret key.
- Public verifiability: anyone with the public key can verify the proof.

**Key management:**

Each tidal version has a VRF key pair (sk, pk). The secret key sk is held by the governance entity. The public key pk is published as part of the tidal version parameters. In the context of PTA, the VRF is used with a **shared, published seed** rather than per-agent secret keys, because the goal is deterministic reproducibility, not per-agent secrecy. The VRF output is deterministic given the seed; the "unpredictability" comes from the seed being unknown before it is published at seed rotation time.

*Rationale: The threat model for PTA's VRF usage is preventing grinding attacks on verifier set selection. An adversary who can predict the VRF output for future epochs could craft claim hashes to influence which agents verify their claims. Seed rotation prevents this by ensuring future seeds are unknown.*

#### 3.2.2 Seed Management

**Initial seed:** The genesis tidal version includes the initial VRF seed, which is a 32-byte value chosen by governance.

**Rotation schedule:** VRF seeds rotate at governance-defined intervals, specified as a number of epochs (`seed_rotation_interval`). Default: every 100 epochs.

**Seed derivation chain:**

```
seed_0 = initial_seed                             (published in genesis tidal version)
seed_{n+1} = SHA-256("PTA-VRF-SEED" || seed_n || big_endian_bytes(rotation_epoch))
```

where `rotation_epoch` is the epoch at which seed_{n+1} becomes active.

**Commitment scheme:** To prevent grinding, seeds are committed before revelation:

1. At epoch E, governance publishes `commitment_{n+1} = SHA-256(seed_{n+1})`.
2. At epoch E + `seed_rotation_interval`, governance reveals `seed_{n+1}`.
3. Agents verify: `SHA-256(seed_{n+1}) == commitment_{n+1}`.
4. If verification fails, agents continue using `seed_n` and the rotation is rescheduled.

#### 3.2.3 Verifier Set Computation

**Input assembly:**

```
vrf_input(claim_hash: bytes32, epoch: uint64, seed: bytes32) -> bytes =
    claim_hash || big_endian_bytes(epoch) || seed
```

**VRF evaluation:**

```
(vrf_output, vrf_proof) = ECVRF_prove(sk, vrf_input)
```

For deterministic reproducibility without the secret key, PTA publishes the VRF output and proof. Any agent can verify:

```
ECVRF_verify(pk, vrf_input, vrf_output, vrf_proof) -> bool
```

**Agent selection (SelectTopK):**

Given `vrf_output` (32 bytes), select k agents from the sorted eligible_agents list:

```
SelectTopK(vrf_output: bytes32, eligible_agents: AgentID[], k: uint32) -> AgentID[]:
    // Generate k pseudo-random indices from VRF output
    selected = []
    remaining = copy(eligible_agents)
    for i in 0..k:
        if remaining is empty: break
        // Derive index from VRF output
        index_seed = SHA-256(vrf_output || big_endian_bytes(i))
        index = big_endian_uint64(index_seed[0..8]) % len(remaining)
        selected.append(remaining[index])
        remaining.remove_at(index)
    return selected
```

**Substitution list:** After selecting the primary k verifiers, continue the selection to produce k additional substitution verifiers using the same algorithm (indices k through 2k-1).

#### 3.2.4 Proof Generation and Verification

**Proof generation** (by any agent with access to the VRF secret key or the precomputed output+proof):

1. Compute `vrf_input = claim_hash || big_endian_bytes(epoch) || seed`.
2. Evaluate `(vrf_output, vrf_proof) = ECVRF_prove(sk, vrf_input)`.
3. Assemble VerifierSet (Section 2.6) with vrf_output, vrf_proof, and selected agents.

**Proof verification** (by any agent):

1. Obtain the VRF public key pk from the active tidal version.
2. Reconstruct `vrf_input = claim_hash || big_endian_bytes(epoch) || seed`.
3. Verify: `ECVRF_verify(pk, vrf_input, vrf_output, vrf_proof)`.
4. If verification passes, recompute `SelectTopK` and confirm the verifier list matches.
5. If any step fails, reject the verifier set assignment.

---

### 3.3 Epoch Clock Protocol

#### 3.3.1 NTP-Grade Synchronization Requirement

All agents MUST synchronize their system clocks to NTP-grade accuracy, defined as:

- **Maximum allowable offset from UTC:** 500 milliseconds.
- **Synchronization protocol:** NTP (RFC 5905) or any protocol achieving equivalent accuracy.
- **Synchronization frequency:** At least once per epoch (agents SHOULD synchronize more frequently).

PTA does NOT require consensus-grade time synchronization (which would demand microsecond accuracy and introduce consensus overhead). NTP-grade is sufficient because:

1. Epoch lengths are configurable and SHOULD be set to at least 10x the maximum expected clock drift (i.e., epoch_length >= 5 seconds at 500ms drift tolerance).
2. Clock drift within the tolerance window produces identical scheduling outputs (the same epoch number maps to the same assignments).
3. Clock drift beyond the tolerance window is treated as agent failure.

#### 3.3.2 Epoch Numbering

Epochs are numbered with a monotonically increasing `uint64`, starting at 0 for the genesis epoch.

**Epoch computation from wall-clock time:**

```
current_epoch(now_ms: uint64, genesis_time_ms: uint64, epoch_length_ms: uint64) -> uint64 =
    if now_ms < genesis_time_ms: error("before genesis")
    return floor((now_ms - genesis_time_ms) / epoch_length_ms)
```

**Epoch start time from epoch number:**

```
epoch_start_ms(epoch_number: uint64, genesis_time_ms: uint64, epoch_length_ms: uint64) -> uint64 =
    return genesis_time_ms + (epoch_number * epoch_length_ms)
```

`genesis_time_ms` and `epoch_length_ms` are defined in the tidal version. During version migration with a different epoch_length_ms, the new epoch length takes effect at the activation_epoch of the new version; epoch numbers continue monotonically (they do not reset).

#### 3.3.3 Epoch Boundary Processing Sequence

At each epoch boundary (transition from epoch e to epoch e+1), agents MUST execute the following steps **in order**. Steps are not concurrent; each step completes before the next begins.

```
process_epoch_boundary(e: uint64):
    // Step 1: SNAPSHOT COMPILATION
    local_snapshot = compile_snapshot(local_state)

    // Step 2: SNAPSHOT PROPAGATION
    broadcast_snapshot(local_snapshot, cios_neighbors)
    received_snapshots = receive_snapshots(timeout = 0.2 * epoch_length_ms)
    agent_roster = aggregate_roster(received_snapshots, previous_roster)

    // Step 3: SETTLEMENT (if settlement epoch)
    if is_settlement(e):
        ledger = compute_settlement(e, tidal_schedule(e), event_log(e), economic_params)
        emit_to_aic(ledger)

    // Step 4: MODEL RECALIBRATION (Phase 2 only; no-op in Phase 1)
    recalibrate_prediction_models(e, observations(e))

    // Step 5: HASH RING UPDATE
    for each task_type in registered_task_types:
        update_hash_ring(task_type, agent_roster)

    // Step 6: VERSION CHECK
    check_version_migration(e)

    // Step 7: SCHEDULE COMPUTATION
    schedule = compute_schedule(local_agent_id, e + 1, agent_roster)
    activate_schedule(schedule)
```

**Timing budget:** The total epoch boundary processing MUST complete within 20% of the epoch length. If processing exceeds this budget, the agent logs a warning and proceeds with a potentially stale roster (graceful degradation).

#### 3.3.4 Tolerance Window for Clock Drift

**Drift tolerance:** An agent's local clock may differ from true UTC by up to `drift_tolerance_ms` (default: 500ms) without consequence.

**Drift detection:** If an agent's epoch boundary processing begins more than `drift_tolerance_ms` before or after the true boundary time, peers will observe the agent as:

- **Early:** The agent's capacity snapshot arrives before peers expect it. Peers accept early snapshots (no harm).
- **Late:** The agent's capacity snapshot arrives after peers have already aggregated. The late snapshot is incorporated at the next epoch boundary. The agent's schedule for the current epoch may be based on a stale roster.

**Persistent drift:** If an agent's clock drifts beyond `2 * drift_tolerance_ms` for more than `max_drift_epochs` consecutive epochs (default: 3), the agent is treated as failed. Its assignments are covered by substitution agents.

---

### 3.4 Scheduling Algorithm

#### 3.4.1 Function Signature

```
schedule(
    agent_id:          AgentID,
    task_type:         TaskType,
    epoch:             uint64,
    capacity_snapshot: CapacitySnapshot
) -> AssignmentSet
```

Where:

```
CapacitySnapshot {
    agent_roster:      map<AgentID, AgentCapacity>
    epoch:             uint64           // Epoch at which snapshot was taken
}

AgentCapacity {
    agent_id:          AgentID
    available_compute: float64          // Normalized compute capacity [0.0, 1.0]
    available_memory:  float64          // Normalized memory capacity [0.0, 1.0]
    task_queue_depth:  uint32           // Number of tasks currently queued
    specializations:   TaskType[]       // Task types this agent can handle
    liveness:          enum {ACTIVE, LEAVING, UNKNOWN}
    version_id:        bytes32          // Tidal version this agent is running
}

AssignmentSet {
    assignments:       Assignment[]
    substitution_duties: SubstitutionDuty[]
}

Assignment {
    agent_id:          AgentID
    task_type:         TaskType
    epoch:             uint64
    task_key:          bytes32          // Hash ring key for this task
    priority:          uint32           // Lower number = higher priority
    is_primary:        bool             // True if primary assignment; false if substitution
}

SubstitutionDuty {
    primary_agent_id:  AgentID          // Agent being substituted for
    task_type:         TaskType
    task_key:          bytes32
    activation_condition: enum {PRIMARY_ABSENT, PRIMARY_OVERLOADED}
}
```

#### 3.4.2 Determinism Guarantee

The scheduling algorithm is **strictly deterministic**: given identical values of (agent_id, task_type, epoch, capacity_snapshot, tidal_version), any implementation MUST produce a bit-identical AssignmentSet. This means:

1. No use of random number generators.
2. No use of wall-clock time (only epoch number).
3. No use of local mutable state beyond the provided inputs.
4. All floating-point arithmetic MUST use IEEE 754 binary64 with round-to-nearest-even.
5. All iteration over maps and sets MUST use a canonical ordering (sorted by key bytes, lexicographic).

#### 3.4.3 Core Algorithm Pseudocode

```
function schedule_tasks(
    agent_id: AgentID,
    task_type: TaskType,
    epoch: uint64,
    capacity_snapshot: CapacitySnapshot,
    tidal_version: TidalVersion
) -> AssignmentSet:

    // Step 0: Check if task_type is active this epoch
    band = tidal_version.parameters.task_type_bands[task_type]
    if (epoch - band.phase_offset) % band.frequency != 0:
        return empty AssignmentSet

    // Step 1: Build the hash ring for this task type
    ring = []
    for each (aid, cap) in sorted(capacity_snapshot.agent_roster):
        if task_type not in cap.specializations: continue
        if cap.liveness == LEAVING or cap.liveness == UNKNOWN: continue

        // Capacity-weighted virtual node count
        base_vnodes = tidal_version.parameters.virtual_nodes_per_agent
        weight = (cap.available_compute + cap.available_memory) / 2.0
        vnodes = max(1, round(base_vnodes * weight))

        for j in 0..vnodes:
            pos = vnode_position(aid, task_type, j)
            ring.append((pos, aid))

    sort ring by pos ascending

    // Step 2: Generate task keys for this epoch
    // Tasks are identified by (task_type, epoch, sequence_number)
    // The number of tasks per epoch is determined by the tidal version
    task_keys = []
    for seq in 0..tasks_per_epoch(task_type, tidal_version):
        key = SHA-256(task_type || big_endian_bytes(epoch) || big_endian_bytes(seq))
        task_keys.append(key)

    // Step 3: Assign tasks via ring lookup
    assignments = []
    substitution_duties = []

    for (seq, key) in enumerate(task_keys):
        primary_agent = lookup(key, ring)

        assignment = Assignment {
            agent_id: primary_agent,
            task_type: task_type,
            epoch: epoch,
            task_key: key,
            priority: seq,
            is_primary: true
        }

        // Step 4: Compute substitution list (next 2 distinct agents on ring)
        subs = find_next_distinct_agents(key, ring, count=2, exclude={primary_agent})
        for sub_agent in subs:
            substitution_duties.append(SubstitutionDuty {
                primary_agent_id: primary_agent,
                task_type: task_type,
                task_key: key,
                activation_condition: PRIMARY_ABSENT
            })

        assignments.append(assignment)

    // Step 5: Filter to only assignments relevant to this agent
    my_assignments = [a for a in assignments if a.agent_id == agent_id]
    my_subs = [s for s in substitution_duties
               if find_next_distinct_agents(s.task_key, ring, count=2,
                  exclude={s.primary_agent_id}) contains agent_id]

    return AssignmentSet {
        assignments: my_assignments,
        substitution_duties: my_subs
    }
```

#### 3.4.4 Capacity-Weighted Virtual Node Placement

Agent capacity influences scheduling through weighted virtual node counts:

```
effective_vnodes(agent: AgentCapacity, base_vnodes: uint32) -> uint32:
    // Capacity weight: average of compute and memory availability
    weight = (agent.available_compute + agent.available_memory) / 2.0

    // Clamp weight to [0.1, 3.0] to prevent extreme under/over-representation
    weight = clamp(weight, 0.1, 3.0)

    // Scale virtual node count
    vnodes = max(1, round(base_vnodes * weight))

    return vnodes
```

An agent with twice the capacity of the average agent will have approximately twice as many virtual nodes, and will therefore be assigned approximately twice as many tasks. An agent at minimum capacity (weight = 0.1) still has at least 1 virtual node, ensuring it remains on the ring and is reachable for substitution.

---

### 3.5 Agent Churn Protocol

#### 3.5.1 Agent Join

**Trigger:** A new agent registers with the CIOS hierarchy and is assigned a role.

**Protocol sequence:**

```
handle_agent_join(new_agent_id: AgentID, capacity: AgentCapacity) -> UpdatedRing:

    // 1. REGISTER
    // New agent is added to the CIOS hierarchy. CIOS Adapter delivers
    // the updated HierarchyTopology to all agents at the next epoch boundary.

    // 2. ALLOCATE VIRTUAL NODES
    // At the next epoch boundary, all agents process the new roster:
    for each task_type in capacity.specializations:
        vnodes = effective_vnodes(capacity, tidal_version.virtual_nodes_per_agent)
        for j in 0..vnodes:
            pos = vnode_position(new_agent_id, task_type, j)
            insert (pos, new_agent_id) into ring[task_type]
        re-sort ring[task_type]

    // 3. SYNC CAPACITY
    // New agent sends its initial capacity snapshot at the epoch boundary.
    // New agent receives existing snapshots from neighbors via gossip.
    // After 1 epoch boundary, the new agent has a local roster and can
    // compute schedules identically to all other agents.

    // 4. KEY REDISTRIBUTION
    // Keys that now fall in the new agent's virtual node ranges are
    // implicitly reassigned. No explicit transfer is needed because
    // the ring lookup is recomputed each epoch.

    return updated_ring
```

**Convergence time:** 1 epoch boundary. After the new agent's first full epoch boundary participation, it is fully integrated.

**Impact on existing agents:** O(K/N) keys are reassigned. Only the immediate ring neighbors of the new agent's virtual nodes are affected.

#### 3.5.2 Agent Leave (Graceful)

**Trigger:** Agent signals intent to depart by setting `liveness = LEAVING` in its capacity snapshot.

**Protocol sequence:**

```
handle_agent_graceful_leave(leaving_agent_id: AgentID) -> UpdatedRing:

    // 1. SIGNAL
    // Leaving agent sets liveness = LEAVING in its capacity snapshot
    // at the current epoch boundary.

    // 2. COMPLETE CURRENT EPOCH
    // Leaving agent completes all assignments for the current epoch.

    // 3. DEREGISTER (next epoch boundary)
    // All agents observe liveness = LEAVING and exclude the agent
    // from ring construction:
    for each task_type:
        remove all virtual nodes for leaving_agent_id from ring[task_type]
        re-sort ring[task_type]

    // 4. KEY REDISTRIBUTION
    // Keys formerly assigned to the leaving agent are now assigned to
    // the next agent on the ring (automatic via lookup recomputation).

    return updated_ring
```

**Convergence time:** 1 epoch boundary after the LEAVING signal.

#### 3.5.3 Agent Failure (Ungraceful)

**Trigger:** Agent stops responding. No LEAVING signal is sent.

**Detection mechanism:**

1. **Checkpoint absence:** The tidal schedule defines expected checkpoints (e.g., task completion acknowledgments). If a primary agent misses its checkpoint, the substitution agent activates.
2. **Snapshot absence:** At epoch boundary, the failed agent's capacity snapshot is absent. After `absence_threshold` consecutive epochs without a snapshot (default: 2), the agent is removed from the roster.

**Protocol sequence:**

```
handle_agent_failure(failed_agent_id: AgentID) -> SubstitutionAssignments:

    // 1. DETECT (during epoch)
    // Substitution agents detect the failed agent's absence at scheduled
    // checkpoints (deterministic: the next agent on the hash ring).

    // 2. ACTIVATE SUBSTITUTIONS (immediate, within current epoch)
    for each task assigned to failed_agent_id in current epoch:
        sub_agent = next_distinct_agent_on_ring(task.task_key, ring, exclude={failed_agent_id})
        sub_agent activates for this task

    // 3. ROSTER UPDATE (at next epoch boundary)
    // If failed agent's snapshot is absent:
    //   Increment absence_counter[failed_agent_id]
    //   If absence_counter >= absence_threshold:
    //     Remove failed_agent_id from roster
    //     Remove all virtual nodes from all rings
    //     Reset absence_counter

    // 4. FULL REDISTRIBUTION (at epoch boundary after removal)
    // Same as graceful leave step 3-4.

    return substitution_assignments
```

**Convergence time:** Substitution within the current epoch (immediate). Full roster removal after `absence_threshold` epochs (default: 2).

#### 3.5.4 Substitution List

The substitution list for any task assignment is deterministic: it is the ordered sequence of the next distinct agents on the hash ring after the primary assignment's virtual node.

```
substitution_list(task_key: bytes, ring: SortedVirtualNodes, primary: AgentID, depth: uint32) -> AgentID[]:
    position = ring_position(task_key)
    result = []
    seen = {primary}
    cursor = first vnode in ring with pos >= position

    while len(result) < depth:
        cursor = next_vnode(cursor, ring)  // wraps around
        if cursor.agent_id not in seen:
            result.append(cursor.agent_id)
            seen.add(cursor.agent_id)
        if cursor has wrapped past starting point:
            break  // exhausted all agents

    return result
```

Default substitution depth: 2 (two backup agents per task).

---

### 3.6 Capacity Snapshot Service

#### 3.6.1 Snapshot Contents

```
CapacitySnapshotMessage {
    agent_id:           AgentID
    epoch:              uint64           // Epoch at which snapshot was compiled
    available_compute:  float64          // [0.0, 1.0] normalized
    available_memory:   float64          // [0.0, 1.0] normalized
    task_queue_depth:   uint32           // Number of tasks currently queued
    specializations:    TaskType[]       // Task types this agent can handle
    liveness:           enum {ACTIVE, LEAVING, UNKNOWN}
    version_id:         bytes32          // Active tidal version
    signature:          bytes            // Agent's signature over the above fields
    ttl:                uint32           // Remaining hops for gossip propagation
}
```

**Field constraints:**
- `available_compute` and `available_memory` MUST be in range [0.0, 1.0].
- `specializations` MUST contain at least one task type.
- `ttl` MUST be initialized to `ceil(log2(N))` where N is the estimated network size.
- `signature` MUST be verifiable against the agent's registered public key.

#### 3.6.2 Exchange Timing

Capacity snapshots are exchanged **at epoch boundaries only**. No mid-epoch snapshot exchange is permitted in Layer 1.

**Timing sequence:**

1. At epoch boundary e -> e+1, each agent compiles its snapshot within the first 5% of the epoch boundary processing window.
2. The agent transmits its snapshot to all CIOS-defined direct neighbors.
3. Each neighbor that receives a snapshot decrements `ttl` and, if `ttl > 0`, forwards it to its own neighbors (excluding the sender).
4. Snapshot reception window: 20% of epoch_length_ms from the start of the boundary.

#### 3.6.3 Aggregation: Hierarchical via CIOS Topology

**Gossip propagation:**

Snapshots propagate via a bounded gossip protocol over the CIOS hierarchy topology:

1. Each agent sends its own snapshot to its direct CIOS neighbors (degree D, typically 4-10).
2. Each receiving agent forwards received snapshots to its own neighbors, decrementing `ttl`.
3. When `ttl` reaches 0, the snapshot is not forwarded further.
4. **Deduplication:** Agents track received snapshot (agent_id, epoch) pairs. Duplicate snapshots are dropped.
5. **Conflict resolution:** If multiple snapshots for the same agent_id arrive with different epochs, the highest epoch wins.

**Hierarchical aggregation (for N > 10,000):**

At large scales, CIOS Coordinators aggregate snapshots from their Implementor subtrees:

1. Implementors send snapshots to their assigned Coordinator.
2. Coordinators compile aggregate summaries (count, average capacity, task type distribution) for their subtree.
3. Coordinators exchange summaries with peer Coordinators.
4. Agents receive either individual snapshots (for nearby agents) or aggregate summaries (for distant agents).

This reduces per-agent snapshot bandwidth from O(N) to O(sqrt(N)) at large scales.

#### 3.6.4 Staleness Bound

**Guarantee:** The agent roster used for hash ring computation is at most one epoch old. Specifically:

- At epoch e, the roster used for scheduling MUST contain all snapshots received during the epoch (e-1) -> e boundary.
- Snapshots from epoch e-2 or earlier are valid if no newer snapshot for that agent has been received.
- An agent with no snapshot received for `absence_threshold` epochs is treated as failed (Section 3.5.3).

**Impact of staleness:** A stale roster may cause agents to disagree on hash ring composition for at most 1 epoch. This produces suboptimal (not incorrect) scheduling: some tasks may be computed as assigned to an agent that has already left, and the substitution agent covers. By the next epoch boundary, rosters converge.

---

## 4. Algorithm Pseudocode (Layer 1)

This section provides reference pseudocode for the five core Layer 1 algorithms. Implementations MUST produce identical outputs for identical inputs.

---

### 4.1 schedule_tasks

```
function schedule_tasks(
    agent_id: AgentID,
    task_type: TaskType,
    epoch: uint64,
    capacity_snapshot: CapacitySnapshot,
    tidal_version: TidalVersion
) -> AssignmentSet:

    // --- PHASE 1: Activity check ---
    band = tidal_version.parameters.task_type_bands[task_type]
    if (epoch - band.phase_offset) % band.frequency != 0:
        return AssignmentSet { assignments: [], substitution_duties: [] }

    // --- PHASE 2: Ring construction ---
    ring = build_ring(task_type, capacity_snapshot, tidal_version)

    if ring is empty:
        return AssignmentSet { assignments: [], substitution_duties: [] }

    // --- PHASE 3: Task key generation ---
    num_tasks = tidal_version.parameters.tasks_per_epoch[task_type]  // default: 1
    task_keys = []
    for seq in 0..num_tasks:
        key = SHA-256(
            task_type ||
            big_endian_bytes(epoch) ||
            big_endian_bytes(seq)
        )
        task_keys.append((seq, key))

    // --- PHASE 4: Assignment via ring lookup ---
    all_assignments = []
    all_substitutions = []

    for (seq, key) in task_keys:
        primary = lookup(key, ring)

        all_assignments.append(Assignment {
            agent_id: primary,
            task_type: task_type,
            epoch: epoch,
            task_key: key,
            priority: seq,
            is_primary: true
        })

        subs = substitution_list(key, ring, primary, depth=2)
        for (i, sub_id) in enumerate(subs):
            all_substitutions.append(SubstitutionDuty {
                primary_agent_id: primary,
                task_type: task_type,
                task_key: key,
                activation_condition: PRIMARY_ABSENT
            })

    // --- PHASE 5: Filter to local agent ---
    my_assignments = [a for a in all_assignments where a.agent_id == agent_id]
    my_substitutions = [s for s in all_substitutions
                        where substitution_list(s.task_key, ring, s.primary_agent_id, 2)
                              contains agent_id]

    return AssignmentSet {
        assignments: my_assignments,
        substitution_duties: my_substitutions
    }


function build_ring(
    task_type: TaskType,
    snapshot: CapacitySnapshot,
    version: TidalVersion
) -> SortedVirtualNodes:

    ring = []
    base_v = version.parameters.virtual_nodes_per_agent

    // Iterate in canonical order (sorted by agent_id bytes)
    for each (aid, cap) in sorted_by_key(snapshot.agent_roster):
        if task_type not in cap.specializations: continue
        if cap.liveness != ACTIVE: continue

        weight = clamp((cap.available_compute + cap.available_memory) / 2.0, 0.1, 3.0)
        v = max(1, round(base_v * weight))

        for j in 0..v:
            pos = ring_position(aid || task_type || big_endian_bytes(j))
            ring.append(VirtualNode { position: pos, agent_id: aid })

    sort ring by position ascending
    return ring
```

---

### 4.2 compute_verifier_set

```
function compute_verifier_set(
    claim_hash: bytes32,
    epoch: uint64,
    seed: bytes32,
    eligible_agents: AgentID[],    // MUST be sorted lexicographically
    k: uint32,                     // Verifier set size
    vrf_sk: VRFSecretKey           // VRF secret key (held by governance / precomputed)
) -> VerifierSet:

    // --- STEP 1: Assemble VRF input ---
    vrf_input = claim_hash || big_endian_bytes(epoch) || seed

    // --- STEP 2: Evaluate VRF ---
    (vrf_output, vrf_proof) = ECVRF_prove(vrf_sk, vrf_input)

    // --- STEP 3: Select primary verifiers ---
    primary_k = min(k, len(eligible_agents))
    selected = []
    remaining = copy(eligible_agents)

    for i in 0..primary_k:
        index_seed = SHA-256(vrf_output || big_endian_bytes(i))
        index = big_endian_uint64(index_seed[0..8]) % len(remaining)
        selected.append(remaining[index])
        remaining.remove_at(index)

    // --- STEP 4: Select substitution verifiers ---
    sub_k = min(k, len(remaining))
    substitutions = []

    for i in primary_k..(primary_k + sub_k):
        if remaining is empty: break
        index_seed = SHA-256(vrf_output || big_endian_bytes(i))
        index = big_endian_uint64(index_seed[0..8]) % len(remaining)
        substitutions.append(remaining[index])
        remaining.remove_at(index)

    // --- STEP 5: Assemble result ---
    return VerifierSet {
        claim_hash: claim_hash,
        epoch: epoch,
        verifiers: selected,
        substitution_list: substitutions,
        vrf_output: vrf_output,
        vrf_proof: vrf_proof,
        seed_version: current_seed_version()
    }
```

---

### 4.3 handle_agent_join

```
function handle_agent_join(
    new_agent_id: AgentID,
    capacity: AgentCapacity,
    current_rings: map<TaskType, SortedVirtualNodes>,
    tidal_version: TidalVersion
) -> map<TaskType, SortedVirtualNodes>:

    base_v = tidal_version.parameters.virtual_nodes_per_agent
    weight = clamp(
        (capacity.available_compute + capacity.available_memory) / 2.0,
        0.1, 3.0
    )
    v = max(1, round(base_v * weight))

    updated_rings = copy(current_rings)

    for each task_type in capacity.specializations:
        if task_type not in updated_rings:
            updated_rings[task_type] = []

        for j in 0..v:
            pos = ring_position(new_agent_id || task_type || big_endian_bytes(j))
            insert VirtualNode { position: pos, agent_id: new_agent_id }
                into updated_rings[task_type]

        re-sort updated_rings[task_type] by position

    return updated_rings
```

---

### 4.4 handle_agent_failure

```
function handle_agent_failure(
    failed_agent_id: AgentID,
    current_epoch: uint64,
    current_rings: map<TaskType, SortedVirtualNodes>,
    tidal_version: TidalVersion,
    active_assignments: map<bytes32, Assignment>  // task_key -> Assignment
) -> SubstitutionAssignments:

    subs = []

    // --- STEP 1: Identify affected assignments ---
    affected = [a for a in active_assignments.values()
                where a.agent_id == failed_agent_id and a.epoch == current_epoch]

    // --- STEP 2: Activate substitutions ---
    for a in affected:
        ring = current_rings[a.task_type]
        sub_list = substitution_list(a.task_key, ring, failed_agent_id, depth=2)

        if sub_list is not empty:
            subs.append(SubstitutionActivation {
                original_assignment: a,
                substitute_agent_id: sub_list[0],  // first available substitute
                task_key: a.task_key,
                task_type: a.task_type,
                epoch: current_epoch,
                reason: AGENT_FAILURE
            })

    // --- STEP 3: Queue roster removal ---
    // (Actual removal happens at epoch boundary after absence_threshold)
    increment_absence_counter(failed_agent_id)

    if absence_counter[failed_agent_id] >= ABSENCE_THRESHOLD:
        // Remove from all rings
        for each task_type in current_rings:
            current_rings[task_type] = [vn for vn in current_rings[task_type]
                                        where vn.agent_id != failed_agent_id]
        remove failed_agent_id from agent_roster
        reset absence_counter[failed_agent_id]

    return SubstitutionAssignments { activations: subs }
```

---

### 4.5 process_epoch_boundary

```
function process_epoch_boundary(
    epoch: uint64,
    local_agent_id: AgentID,
    local_state: AgentState,
    cios_neighbors: AgentID[],
    tidal_version: TidalVersion,
    event_log: EventLog,
    economic_params: EconomicParameters,
    previous_roster: AgentRoster
) -> SettlementInputs:

    // === STEP 1: SNAPSHOT COMPILATION ===
    snapshot = CapacitySnapshotMessage {
        agent_id: local_agent_id,
        epoch: epoch,
        available_compute: local_state.compute_available(),
        available_memory: local_state.memory_available(),
        task_queue_depth: local_state.queue_depth(),
        specializations: local_state.supported_task_types(),
        liveness: ACTIVE,
        version_id: tidal_version.version_id,
        signature: sign(local_state.private_key, above_fields),
        ttl: ceil(log2(estimated_network_size()))
    }

    // === STEP 2: SNAPSHOT PROPAGATION ===
    send(snapshot, to=cios_neighbors)
    received = receive_all(timeout=0.2 * tidal_version.parameters.epoch_length_ms)

    // Gossip: forward received snapshots with decremented TTL
    for msg in received:
        if msg.ttl > 0:
            forward = copy(msg)
            forward.ttl -= 1
            send(forward, to=cios_neighbors, exclude=msg.sender)

    // Aggregate roster
    agent_roster = copy(previous_roster)
    for msg in received:
        if msg.epoch > agent_roster[msg.agent_id].epoch or
           msg.agent_id not in agent_roster:
            agent_roster[msg.agent_id] = msg
    // Add our own snapshot
    agent_roster[local_agent_id] = snapshot

    // Detect absent agents
    for aid in agent_roster:
        if aid not in {m.agent_id for m in received} and aid != local_agent_id:
            increment_absence_counter(aid)
            if absence_counter[aid] >= ABSENCE_THRESHOLD:
                remove aid from agent_roster

    // === STEP 3: SETTLEMENT (if settlement epoch) ===
    settlement = null
    if epoch % tidal_version.parameters.settlement_interval == 0:
        schedule_for_epoch = reconstruct_schedule(epoch, agent_roster, tidal_version)
        settlement = compute_settlement(
            epoch,
            schedule_for_epoch,
            event_log.events_for(epoch),
            economic_params
        )
        emit_settlement(settlement)

    // === STEP 4: MODEL RECALIBRATION (Phase 2; no-op in Phase 1) ===
    // recalibrate_all_prediction_models(epoch)

    // === STEP 5: HASH RING UPDATE ===
    rings = {}
    for each task_type in all_registered_task_types(tidal_version):
        rings[task_type] = build_ring(task_type, agent_roster, tidal_version)

    // === STEP 6: VERSION CHECK ===
    check_version_migration(epoch, agent_roster, tidal_version)

    // === STEP 7: SCHEDULE COMPUTATION ===
    next_schedule = {}
    for each task_type in local_state.supported_task_types():
        assignments = schedule_tasks(
            local_agent_id, task_type, epoch + 1,
            CapacitySnapshot { agent_roster: agent_roster, epoch: epoch },
            tidal_version
        )
        next_schedule[task_type] = assignments

    activate_schedule(next_schedule)

    // === RETURN ===
    return SettlementInputs {
        settlement: settlement,
        updated_roster: agent_roster,
        rings: rings,
        next_schedule: next_schedule
    }
```

---

## 5. Test Vectors (Layer 1)

This section provides concrete test vectors for verifying implementation correctness and determinism.

---

### 5.1 Test Vector: schedule_tasks

**Test configuration:**

```
Tidal Version Parameters:
    virtual_nodes_per_agent: 4       (small for test clarity)
    hash_function: SHA-256 truncated to uint64
    settlement_interval: 10
    task_type_bands:
        TaskType_A: { frequency: 1, phase_offset: 0 }  (active every epoch)
        TaskType_B: { frequency: 3, phase_offset: 1 }  (active at epochs 1, 4, 7, ...)
    tasks_per_epoch:
        TaskType_A: 1
        TaskType_B: 1

Agent Roster (3 agents):
    Agent_ALPHA:
        agent_id: 0x0000...0001 (32 bytes, last byte 0x01)
        available_compute: 1.0
        available_memory: 1.0
        specializations: [TaskType_A, TaskType_B]
        liveness: ACTIVE

    Agent_BETA:
        agent_id: 0x0000...0002
        available_compute: 0.5
        available_memory: 0.5
        specializations: [TaskType_A]
        liveness: ACTIVE

    Agent_GAMMA:
        agent_id: 0x0000...0003
        available_compute: 1.0
        available_memory: 1.0
        specializations: [TaskType_A, TaskType_B]
        liveness: ACTIVE
```

**Test case 1: TaskType_A at epoch 5**

Input:
```
agent_id: Agent_ALPHA (0x0000...0001)
task_type: TaskType_A
epoch: 5
```

Expected computation:
1. Band check: `(5 - 0) % 1 == 0` -> active.
2. Ring construction for TaskType_A:
   - Agent_ALPHA: weight = (1.0 + 1.0)/2 = 1.0, vnodes = round(4 * 1.0) = 4
   - Agent_BETA: weight = (0.5 + 0.5)/2 = 0.5, vnodes = round(4 * 0.5) = 2
   - Agent_GAMMA: weight = (1.0 + 1.0)/2 = 1.0, vnodes = round(4 * 1.0) = 4
   - Total virtual nodes: 10
3. Task key: `SHA-256(TaskType_A || 0x0000000000000005 || 0x0000000000000000)`
4. Primary agent: determined by ring lookup of task key.
5. Substitution list: next 2 distinct agents on ring after primary.

**Determinism verification:** Any conforming implementation given these inputs MUST produce the identical primary agent and substitution list.

**Test case 2: TaskType_B at epoch 5**

Input:
```
agent_id: Agent_ALPHA
task_type: TaskType_B
epoch: 5
```

Expected: Band check: `(5 - 1) % 3 == 4 % 3 == 1 != 0` -> **not active**. Return empty AssignmentSet.

**Test case 3: TaskType_B at epoch 7**

Input:
```
agent_id: Agent_ALPHA
task_type: TaskType_B
epoch: 7
```

Expected: Band check: `(7 - 1) % 3 == 6 % 3 == 0` -> active. Ring construction excludes Agent_BETA (no TaskType_B specialization). Ring has Agent_ALPHA (4 vnodes) and Agent_GAMMA (4 vnodes) only.

---

### 5.2 Test Vector: compute_verifier_set

**Test configuration:**

```
claim_hash: SHA-256("test_claim_001") =
    0x7a0a6c26e6a4e1b2d3c4f5e6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f  (example)
epoch: 42
seed: 0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
k: 3

eligible_agents (sorted lexicographically):
    [Agent_A (0x0000...000A),
     Agent_B (0x0000...000B),
     Agent_C (0x0000...000C),
     Agent_D (0x0000...000D),
     Agent_E (0x0000...000E)]
```

**Expected computation:**

1. VRF input: `claim_hash || 0x000000000000002A || seed` (72 bytes)
2. VRF output: `(vrf_output, vrf_proof) = ECVRF_prove(sk, vrf_input)` (deterministic given sk)
3. Selection round 0: `index_seed_0 = SHA-256(vrf_output || 0x0000000000000000)`, `index_0 = uint64(index_seed_0[0..8]) % 5` -> selects one of {A,B,C,D,E}
4. Selection round 1: `index_seed_1 = SHA-256(vrf_output || 0x0000000000000001)`, `index_1 = uint64(index_seed_1[0..8]) % 4` -> selects from remaining 4
5. Selection round 2: `index_seed_2 = SHA-256(vrf_output || 0x0000000000000002)`, `index_2 = uint64(index_seed_2[0..8]) % 3` -> selects from remaining 3
6. Substitution rounds 3-5: continue with remaining agents.

**Output:** 3 primary verifiers + up to 2 substitution verifiers. The exact agents depend on the VRF output, which depends on the VRF secret key.

**Verification:** Any agent can verify the result by checking `ECVRF_verify(pk, vrf_input, vrf_output, vrf_proof)` and recomputing SelectTopK.

---

### 5.3 Determinism Test

**Test objective:** Confirm that two independent implementations produce identical outputs.

**Protocol:**

1. Fix all inputs:
   ```
   tidal_version: (exact bytes of canonical serialization)
   agent_roster: (exact list of agents with capacities)
   epoch: 100
   task_type: TaskType_A
   ```

2. Implementation A computes:
   ```
   result_A = schedule_tasks(agent_X, TaskType_A, 100, snapshot, version)
   ```

3. Implementation B computes:
   ```
   result_B = schedule_tasks(agent_X, TaskType_A, 100, snapshot, version)
   ```

4. **Assertion:** `SHA-256(canonical_serialize(result_A)) == SHA-256(canonical_serialize(result_B))`

**Canonical serialization of AssignmentSet:**

```
serialize(assignment_set):
    buf = []
    // Sort assignments by (task_key, agent_id) lexicographically
    sorted_assignments = sort(assignment_set.assignments, key=(a.task_key, a.agent_id))
    buf.append(uint32(len(sorted_assignments)))
    for a in sorted_assignments:
        buf.append(a.agent_id)          // 32 bytes
        buf.append(a.task_type)         // 32 bytes
        buf.append(uint64(a.epoch))     // 8 bytes
        buf.append(a.task_key)          // 32 bytes
        buf.append(uint32(a.priority))  // 4 bytes
        buf.append(uint8(a.is_primary)) // 1 byte

    sorted_subs = sort(assignment_set.substitution_duties,
                       key=(s.task_key, s.primary_agent_id))
    buf.append(uint32(len(sorted_subs)))
    for s in sorted_subs:
        buf.append(s.primary_agent_id)  // 32 bytes
        buf.append(s.task_type)         // 32 bytes
        buf.append(s.task_key)          // 32 bytes
        buf.append(uint8(s.activation_condition))  // 1 byte

    return concat(buf)
```

**Additional determinism tests:**

| Test | Input Variation | Expected Behavior |
|------|----------------|-------------------|
| Same inputs, different machines | Identical inputs on x86 vs ARM | Identical outputs (IEEE 754 compliance) |
| Roster ordering | Same agents, different insertion order | Identical outputs (canonical sort) |
| Float precision | Capacity weights at boundary (e.g., 0.5000000001) | Round-to-nearest-even produces identical vnode count |
| Empty roster | No eligible agents for a task type | Empty AssignmentSet (no crash, no undefined behavior) |
| Single agent | One agent handles all tasks | All tasks assigned to that agent; empty substitution list |

---

## Appendix A: Summary of Constants and Defaults

| Parameter | Default Value | Range | Defined In |
|-----------|--------------|-------|------------|
| `epoch_length_ms` | 10,000 (10s) | [100, 3,600,000] | Tidal Version |
| `virtual_nodes_per_agent` | 150 | [1, 1000] | Tidal Version |
| `verifier_set_size` (k) | 5 | [1, 100] | Tidal Version |
| `settlement_interval` | 10 epochs | [1, max_uint64] | Tidal Version |
| `drift_tolerance_ms` | 500 | [10, epoch_length_ms / 2] | Epoch Clock |
| `max_drift_epochs` | 3 | [1, 100] | Epoch Clock |
| `absence_threshold` | 2 epochs | [1, 10] | Churn Protocol |
| `substitution_depth` | 2 | [1, 10] | Scheduling |
| `snapshot_ttl` | ceil(log2(N)) | [1, 20] | Snapshot Service |
| `boundary_processing_budget` | 20% of epoch_length | — | Epoch Clock |
| `snapshot_timeout` | 20% of epoch_length | — | Snapshot Service |
| `migration_threshold` | 0.67 | [0.5, 1.0) | Tidal Version |
| `overlap_duration` | 10 epochs | [1, 100] | Tidal Version |
| `seed_rotation_interval` | 100 epochs | [10, 10000] | VRF |
| `capacity_weight_min` | 0.1 | — | Scheduling |
| `capacity_weight_max` | 3.0 | — | Scheduling |
| `max_signals_per_epoch` | 100 | [1, 10000] | Surprise Signal |
| `grace_period_epochs` | 1 | [0, 10] | Settlement |

---

## Appendix B: Glossary

| Term | Definition |
|------|-----------|
| **Agent** | An autonomous computational entity participating in the PTA network. Identified by a unique AgentID. |
| **Epoch** | A discrete time interval; the fundamental coordination unit. |
| **Tidal Function** | A deterministic pure function mapping (agent, task, epoch) to assignments. |
| **Hash Ring** | A consistent hash ring used for deterministic task-to-agent mapping. |
| **Virtual Node** | A point on a hash ring associated with an agent. Multiple virtual nodes per agent improve load balance. |
| **VRF** | Verifiable Random Function; produces unpredictable but verifiable pseudorandom outputs. |
| **Verifier Set** | A deterministically selected set of agents assigned to verify a claim. |
| **Settlement Boundary** | An epoch at which economic settlement is computed. |
| **Surprise Signal** | A delta-encoded message sent when behavior deviates from prediction. |
| **Field Gradient** | A direction vector for sub-epoch task reallocation within a 4-agent cluster. |
| **Substitution List** | Ordered fallback agents for a task when the primary agent fails. |
| **Capacity Snapshot** | Per-agent resource and status report exchanged at epoch boundaries. |
| **Tidal Version** | An immutable parameter set defining tidal function behavior for a range of epochs. |
| **CIOS** | Coordinator-Implementor-Observer-Strategist organizational hierarchy. |
| **AASL** | Agent-Agent Semantic Language; provides claim types and semantic dimensions. |
| **AIC** | AI Coin; the settlement token. |
| **Verichain** | Verification execution subsystem consuming verifier set assignments from PTA. |


---

# Part III — Technical Specification: Layers 2-3, Protocols, Conformance

---


## 6. Predictive Delta Communication Protocol (Layer 2) — ENHANCING, NOT REQUIRED

**SCOPING NOTE:** This layer is additive. The system is fully functional with Layer 1 (Tidal Backbone) alone. Layer 2 reduces communication overhead but is not required for correct operation. All components specified in this section may be disabled without affecting scheduling correctness, settlement determinism, or verification scheduling. When Layer 2 is disabled, agents communicate via standard messaging within the tidal framework, and the settlement calculator omits the prediction bonus and surprise cost streams.

### 6.1 Per-Neighbor Prediction Model

Each agent maintains an independent linear autoregressive (AR) model for every direct neighbor. The neighbor set is bounded by the CIOS hierarchy degree (typically 4–10 neighbors).

**Model type:** Linear autoregressive model with exogenous features (ARX).

**Feature vector:** For neighbor *i* at epoch *t*, the observation vector is:

```
x_i(t) = [
    tidal_compliance_rate,        // fraction of assigned tasks completed on schedule, ∈ [0, 1]
    task_completion_time_delta,   // (actual - expected) completion time, normalized, ∈ ℝ
    resource_utilization_delta,   // (actual - expected) resource consumption, normalized, ∈ ℝ
    surprise_count_window         // count of surprise signals generated in trailing window, ∈ ℕ
]
```

Feature dimension: *d* = 4.

**Model definition:** The prediction for neighbor *i* at epoch *t+1* given observations through epoch *t* is:

```
x̂_i(t+1) = W_i(t) · x_i(t)
```

where **W_i(t)** ∈ ℝ^(d×d) is the weight matrix for neighbor *i*, updated via Recursive Least Squares (RLS).

**Update rule — Recursive Least Squares (RLS) with forgetting factor:**

Let λ ∈ (0, 1] be the forgetting factor (recommended default: λ = 0.98). Higher values weight historical data more; lower values adapt faster to non-stationarity.

Given a new observation x_i(t+1):

1. Compute prediction error:
```
e_i(t+1) = x_i(t+1) - W_i(t) · x_i(t)
```

2. Compute gain vector:
```
k_i(t+1) = P_i(t) · x_i(t) / (λ + x_i(t)ᵀ · P_i(t) · x_i(t))
```

3. Update weight matrix:
```
W_i(t+1) = W_i(t) + e_i(t+1) · k_i(t+1)ᵀ
```

4. Update covariance matrix:
```
P_i(t+1) = (1/λ) · (P_i(t) - k_i(t+1) · x_i(t)ᵀ · P_i(t))
```

**Initialization:**

```
W_i(0) = 0_(d×d)              // zero matrix (predict zero deviation)
P_i(0) = δ · I_(d×d)          // δ = 100.0 (high initial uncertainty)
```

**Computational complexity:**

| Operation | Complexity |
|---|---|
| Initialization | O(d²) |
| Per-update (steps 1–4) | O(d²) |
| Per-prediction | O(d) for matrix-vector multiply |

Since d = 4, all operations are constant-time in practice: O(16) multiplications per update, O(4) per prediction.

**Memory per neighbor:** O(d² + d) = O(20) floating-point values (16 for W, 16 for P, 4 for the last observation vector). Approximately 288 bytes per neighbor at 64-bit precision.

**Total memory for prediction models:** O(D × (d² + d)) where D is the neighbor degree. At D = 10, d = 4: approximately 2.9 KB per agent.

---

### 6.2 Adaptive Surprise Threshold

Each agent maintains an independent adaptive threshold θ_i(t) for each neighbor *i*, governing when a prediction error is large enough to constitute a "surprise" that must be communicated.

**Threshold function:** θ_i(t) ∈ [θ_min, θ_max] for neighbor *i* at epoch *t*.

**Adaptation rules:**

*Tightening* (prediction was accurate — reduce future communication):
```
If ‖e_i(t)‖₂ < θ_i(t):
    θ_i(t+1) = max(θ_min, θ_i(t) × α)
```
where α ∈ (0.9, 0.99) is the tightening rate (recommended default: α = 0.95).

*Loosening* (prediction was inaccurate — increase future communication):
```
If ‖e_i(t)‖₂ ≥ θ_i(t):
    θ_i(t+1) = min(θ_max, θ_i(t) × β)
```
where β ∈ (1.01, 1.1) is the loosening rate (recommended default: β = 1.05).

**Parameter bounds:**

| Parameter | Symbol | Default | Purpose |
|---|---|---|---|
| Minimum threshold | θ_min | 0.01 | Prevents zero-communication deadlock; ensures periodic surprise signals even with perfect predictions |
| Maximum threshold | θ_max | 10.0 | Upper bound equivalent to standard messaging (all deviations are surprises) |
| Initial threshold | θ_init | 1.0 | Starting point; agents begin with moderate sensitivity |
| Tightening rate | α | 0.95 | Per-epoch multiplicative decrease when prediction is accurate |
| Loosening rate | β | 1.05 | Per-epoch multiplicative increase when prediction is inaccurate |

**Non-stationarity detector:**

To detect regime changes where the prediction model is systematically failing, a variance-based non-stationarity detector operates alongside the threshold adapter:

```
σ²_i(t) = (1 - γ) · σ²_i(t-1) + γ · ‖e_i(t)‖₂²
```

where γ ∈ (0, 1) is the smoothing constant (recommended default: γ = 0.1).

If σ²_i(t) > ψ × σ²_i(t-1) for ψ > 1 (recommended default: ψ = 2.0), a non-stationarity event is declared for neighbor *i*, triggering:
1. Threshold is immediately set to θ_max (revert to full communication for this neighbor).
2. The prediction model forgetting factor λ is temporarily reduced to λ_fast = 0.90 for accelerated adaptation.
3. After the model re-converges (accuracy above a recovery threshold for η consecutive epochs, default η = 5), normal threshold adaptation resumes.

**Hysteresis guard:** To prevent oscillation, threshold adjustments are gated: after a loosening event, tightening is inhibited for a configurable cooldown period (default: 3 epochs). This prevents rapid oscillation between tight and loose thresholds when the prediction error hovers near the boundary.

---

### 6.3 Surprise Signal Specification

**Message format:**

```
SurpriseSignal {
    source_id:    AgentID   // originator of the deviation
    epoch:        uint64    // epoch in which the deviation was observed
    error_vector: float[d]  // prediction error vector (d = 4)
    magnitude:    float     // L2 norm of error_vector
    ttl:          uint8     // maximum remaining hops
    hop_count:    uint8     // hops traversed so far
}
```

**Magnitude computation:**

```
magnitude = ‖e_i(t)‖₂ = sqrt(Σ_{j=1}^{d} e_i(t)_j²)
```

A surprise signal is emitted if and only if magnitude > θ_i(t).

**Propagation radius:**

The propagation radius determines how far a surprise signal travels through the CIOS topology:

```
r = min(r_max, floor(log₂(magnitude / θ_base)))
```

where:
- θ_base is the base threshold for radius calculation (default: θ_init = 1.0)
- r_max is the maximum propagation radius (governance parameter, default: 8 hops)

This yields:
- magnitude ∈ [θ_base, 2·θ_base): r = 0 (local only, no propagation)
- magnitude ∈ [2·θ_base, 4·θ_base): r = 1 (immediate neighbors)
- magnitude ∈ [4·θ_base, 8·θ_base): r = 2
- ...and so on, logarithmically

**Damping:**

At each hop, the signal magnitude is reduced by a damping factor δ ∈ (0, 1) (default: δ = 0.7):

```
magnitude_at_hop_h = magnitude_original × δ^h
```

An intermediate agent re-propagates the signal only if the damped magnitude still exceeds its own threshold for the source agent. This naturally limits cascade propagation.

**TTL enforcement:**

```
ttl_initial = r                         // set to computed propagation radius
ttl_at_hop = ttl_initial - hop_count    // decremented at each hop
```

Signal is dropped when ttl_at_hop ≤ 0, regardless of remaining magnitude.

**Deduplication:**

Each agent maintains a deduplication cache keyed by the tuple (source_id, epoch). A signal is processed at most once per (source_id, epoch) pair. Cache entries are evicted after 2 epoch boundaries.

**Per-epoch signal budget:**

Each agent has a hard cap of B_max surprise signals it may originate per epoch (default: B_max = 50). Signals beyond this cap are dropped and logged. This prevents surprise flooding attacks and bounds worst-case communication.

---

### 6.4 Cold-Start Protocol

When a neighbor relationship is newly established (agent join, cluster reformation, or model reset), the prediction model has no history and cannot produce accurate predictions.

**Initial state:** The communication mode for the new neighbor is set to STANDARD. In STANDARD mode, all observation data is transmitted as if every observation were a surprise (equivalent to θ_i = 0).

**Transition criterion:** The neighbor communication mode transitions from STANDARD to PREDICTIVE when:

```
model_accuracy_i(t) > acc_threshold   for   consecutive_epochs_threshold consecutive epochs
```

where:
- model_accuracy_i(t) = 1 - (mean_absolute_error_i(t) / mean_observation_magnitude_i(t))
- acc_threshold = 0.7 (70% model accuracy; configurable)
- consecutive_epochs_threshold = 5 (configurable)

**Transition sequence:**

1. STANDARD: all messages sent (epochs 0 through qualification start)
2. TRANSITIONING: model accuracy is being evaluated, messages still sent in full (qualification window)
3. PREDICTIVE: only surprises sent (steady state)

Transition from STANDARD to TRANSITIONING is implicit when model_accuracy_i first exceeds acc_threshold. Transition from TRANSITIONING to PREDICTIVE occurs after consecutive_epochs_threshold consecutive epochs above acc_threshold.

**Per-neighbor independence:** Each neighbor transitions independently. Agent A may be in PREDICTIVE mode for neighbor B and STANDARD mode for neighbor C simultaneously.

**Revert criterion:** If model accuracy drops below revert_threshold = 0.5 (configurable) at any point during PREDICTIVE mode, the neighbor reverts to STANDARD mode immediately. The model may be reset to initial state (W = 0, P = δI) if the revert is triggered by a non-stationarity event.

---

### 6.5 Model Recalibration

At every epoch boundary, all prediction models undergo mandatory recalibration to prevent silent drift.

**Recalibration procedure:**

1. **Observation collection:** Gather the complete epoch's observations for each neighbor: actual tidal compliance, task completion times, resource utilization, and surprise counts.

2. **Retrospective accuracy assessment:** For each neighbor *i*, compute the epoch-level prediction accuracy:
```
epoch_accuracy_i = 1 - (1/T) · Σ_{t ∈ epoch} ‖e_i(t)‖₂ / ‖x_i(t)‖₂
```
where T is the number of observation steps within the epoch.

3. **Drift detection:** Compare the epoch-level accuracy against the running average accuracy:
```
drift_detected_i = (|epoch_accuracy_i - running_accuracy_i| > drift_threshold)
```
where drift_threshold = 0.2 (default).

4. **Conditional actions:**
   - If drift NOT detected: continue with current model parameters; update running_accuracy_i with exponential moving average.
   - If drift detected: reset the forgetting factor to λ_fast = 0.90 for the next epoch to accelerate adaptation. If drift persists for 3 consecutive epochs, fully reset the model (W = 0, P = δI) and revert to STANDARD mode.

5. **Threshold synchronization:** After recalibration, re-evaluate the threshold θ_i based on the recalibrated model's accuracy. If the model was reset, θ_i is reset to θ_init.

**Pseudocode:**

```
function recalibrate_models(epoch_observations: Map<AgentID, Observation[]>) -> Map<AgentID, Model>:
    for each neighbor_id, observations in epoch_observations:
        model = get_model(neighbor_id)

        // Step 2: Retrospective accuracy
        total_error = 0.0
        total_magnitude = 0.0
        for obs in observations:
            predicted = model.predict(obs.previous_state)
            error = obs.actual - predicted
            total_error += norm(error)
            total_magnitude += norm(obs.actual)

        epoch_accuracy = 1.0 - (total_error / max(total_magnitude, EPSILON))

        // Step 3: Drift detection
        drift_magnitude = abs(epoch_accuracy - model.running_accuracy)

        if drift_magnitude > DRIFT_THRESHOLD:
            model.consecutive_drift_count += 1
            if model.consecutive_drift_count >= 3:
                // Full reset
                model.W = zeros(d, d)
                model.P = DELTA * identity(d)
                model.communication_mode = STANDARD
                model.threshold = THETA_INIT
                model.consecutive_drift_count = 0
            else:
                // Accelerated adaptation
                model.lambda = LAMBDA_FAST
        else:
            model.consecutive_drift_count = 0
            model.lambda = LAMBDA_DEFAULT

        // Step 5: Update running accuracy
        model.running_accuracy = (1 - ACCURACY_EMA_ALPHA) * model.running_accuracy
                                 + ACCURACY_EMA_ALPHA * epoch_accuracy

        // Re-evaluate threshold
        if model.communication_mode == STANDARD:
            model.threshold = THETA_INIT

        store_model(neighbor_id, model)

    return all_models
```

---

### 6.6 Algorithm Pseudocode (Layer 2)

#### 6.6.1 update_prediction_model

```
function update_prediction_model(
    neighbor_id: AgentID,
    observation: float[d]
) -> Model:
    model = get_model(neighbor_id)
    x = model.last_observation              // x_i(t)

    if x is null:
        // First observation — store and return
        model.last_observation = observation
        return model

    // Step 1: Prediction error
    prediction = model.W · x
    e = observation - prediction             // e_i(t+1)

    // Step 2: Gain vector (RLS)
    Px = model.P · x
    denominator = model.lambda + dot(x, Px)
    k = Px / denominator                     // k_i(t+1)

    // Step 3: Update weights
    model.W = model.W + outer(e, k)          // W_i(t+1)

    // Step 4: Update covariance
    model.P = (1 / model.lambda) * (model.P - outer(k, dot(x, model.P)))

    // Housekeeping
    model.last_observation = observation
    model.last_error = e
    model.error_magnitude = norm(e)

    // Update accuracy tracker
    obs_magnitude = norm(observation)
    if obs_magnitude > EPSILON:
        step_accuracy = 1.0 - (model.error_magnitude / obs_magnitude)
    else:
        step_accuracy = 1.0
    model.accuracy_ema = (1 - ACCURACY_STEP_ALPHA) * model.accuracy_ema
                         + ACCURACY_STEP_ALPHA * step_accuracy

    // Update non-stationarity detector
    model.error_variance = (1 - GAMMA) * model.error_variance
                           + GAMMA * model.error_magnitude^2

    return model
```

#### 6.6.2 compute_surprise

```
function compute_surprise(
    observation: float[d],
    prediction: float[d],
    threshold: float,
    source_id: AgentID,
    epoch: uint64
) -> SurpriseSignal | null:
    error_vector = observation - prediction
    magnitude = norm(error_vector)

    if magnitude <= threshold:
        return null                          // No surprise — silence

    radius = min(R_MAX, floor(log2(magnitude / THETA_BASE)))
    radius = max(0, radius)

    return SurpriseSignal {
        source_id:    source_id,
        epoch:        epoch,
        error_vector: error_vector,
        magnitude:    magnitude,
        ttl:          radius,
        hop_count:    0
    }
```

#### 6.6.3 propagate_surprise

```
function propagate_surprise(
    signal: SurpriseSignal,
    neighbors: AgentID[]
) -> SurpriseSignal[]:
    // Check deduplication
    dedup_key = (signal.source_id, signal.epoch)
    if dedup_key in dedup_cache:
        return []
    dedup_cache.insert(dedup_key)

    // Check TTL
    if signal.ttl <= 0:
        return []

    // Check per-epoch signal budget
    if signals_originated_this_epoch >= B_MAX and signal.hop_count == 0:
        log_warning("Signal budget exceeded, dropping outbound surprise")
        return []

    forwarded = []
    for neighbor in neighbors:
        // Apply damping
        damped_magnitude = signal.magnitude * DELTA_DAMPING ^ signal.hop_count

        // Only forward if damped magnitude exceeds neighbor's threshold
        neighbor_threshold = get_threshold_for_source(neighbor, signal.source_id)
        if damped_magnitude > neighbor_threshold:
            forwarded_signal = SurpriseSignal {
                source_id:    signal.source_id,
                epoch:        signal.epoch,
                error_vector: signal.error_vector * (damped_magnitude / signal.magnitude),
                magnitude:    damped_magnitude,
                ttl:          signal.ttl - 1,
                hop_count:    signal.hop_count + 1
            }
            send_to(neighbor, forwarded_signal)
            forwarded.append(forwarded_signal)

    // Record for settlement
    record_surprise_event(signal)

    return forwarded
```

#### 6.6.4 recalibrate_models

See Section 6.5 for the complete recalibration pseudocode. The function signature is:

```
function recalibrate_models(
    epoch_observations: Map<AgentID, Observation[]>
) -> Map<AgentID, Model>
```

This function is invoked at Step 4 of the Epoch Boundary Processing sequence (architecture document Section 3.3).

---

## 7. Morphogenic Field Protocol (Layer 3) — DECISION GATE AT PHASE 2 END

**SCOPING NOTE:** This layer carries a formal decision gate. Implementation proceeds only if Phase 2 evaluation confirms net value over simple load-balancing heuristics within tetrahedral clusters. The gate criteria are: (1) Phase 2 validation criteria are met, (2) potential game convergence is validated in simulation (per Experiment 4 in the refined concept), (3) measurable improvement over round-robin allocation is demonstrated in simulated tetrahedral clusters. If the gate criteria are not met, Layer 3 is either simplified to a static load-balancing rule within clusters or dropped entirely. Layers 1 and 2 are unaffected by the gate outcome.

### 7.1 Potential Game Framework

Layer 3 models sub-epoch task allocation within tetrahedral (4-agent) clusters as a potential game, guaranteeing convergence to Nash equilibrium.

**Definitions:**

Let *C* = {a₁, a₂, a₃, a₄} be a tetrahedral cluster of 4 agents.

Let *K* be the number of available task types within the cluster. Each agent *i* maintains a strategy vector:

```
s_i ∈ Δ^K    (the K-dimensional simplex)
```

where s_i[k] represents the fraction of agent *i*'s capacity allocated to task type *k*, subject to:

```
Σ_{k=1}^{K} s_i[k] = 1,    s_i[k] ≥ 0    ∀k
```

The joint strategy profile is **s** = (s₁, s₂, s₃, s₄).

**Potential function:**

Define the global potential function Φ: S → ℝ over the cluster state space *S* = (Δ^K)⁴:

```
Φ(s) = Σ_{k=1}^{K} [ D_k · log(Σ_{i=1}^{4} c_i · s_i[k] + ε) - μ · Σ_{i=1}^{4} (s_i[k] - 1/K)² ]
```

where:
- D_k ∈ ℝ≥0 is the demand weight for task type *k* (derived from task queue depths and AASL semantic urgency)
- c_i ∈ ℝ>0 is agent *i*'s capability score for the cluster's task mix (from the capacity snapshot)
- ε > 0 is a small constant to prevent log(0) (default: ε = 10⁻⁶)
- μ ≥ 0 is a regularization coefficient penalizing extreme specialization (default: μ = 0.1)

The first term drives agents to collectively cover demand proportionally to its weight. The logarithmic form ensures diminishing returns from additional allocation to well-served task types. The second term provides regularization, preventing degenerate strategies where one agent handles all of one task type.

**Potential game property:**

Define agent *i*'s local cost function:

```
J_i(s_i, s_{-i}) = -Σ_{k=1}^{K} [ D_k · c_i · s_i[k] / (Σ_{j=1}^{4} c_j · s_j[k] + ε) ] + μ · Σ_{k=1}^{K} (s_i[k] - 1/K)²
```

This is the negative marginal contribution of agent *i* to the log-capacity terms, plus the regularization cost. By construction:

```
Φ(s_i', s_{-i}) - Φ(s_i, s_{-i}) corresponds to J_i(s_i, s_{-i}) - J_i(s_i', s_{-i})
```

in the sense that any unilateral improvement by agent *i* (reducing J_i) also improves Φ. This satisfies the Monderer-Shapley potential game condition (Monderer & Shapley, "Potential Games," *Games and Economic Behavior*, 1996).

**Convergence guarantee:**

By the finite improvement property of potential games (Monderer & Shapley 1996), any sequence of best-response updates by individual agents converges to a Nash equilibrium, which is a local maximum of Φ. Since the strategy space is compact (each s_i lies on the K-simplex) and Φ is continuous, convergence is guaranteed.

**Convergence bound at 4-agent scale:**

With 4 agents and K task types (typically K ≤ 10), the strategy space is (Δ^K)⁴. Best-response updates with a gradient step converge within O(K / η) iterations, where η is the step size. At K = 10 and η = 0.1, this is approximately 100 gradient steps. Since each step is O(K) computation for 4 agents, total convergence cost is O(K² × 4) = O(400) floating-point operations — trivially fast, achievable within sub-epoch timescales.

---

### 7.2 Field Gradient Computation

**Input:**
- AASL semantic dimensions d_sem (defines the task type space K)
- Local task queue state: q_i[k] = queue depth for task type *k* at agent *i*
- Capability vector: c_i[k] = agent *i*'s efficiency for task type *k* (from AASL capability registry)
- Cluster state **s** = (s₁, s₂, s₃, s₄): current allocation strategies of all cluster members

**Demand vector computation:**

```
D_k = Σ_{i=1}^{4} q_i[k] · w_k
```

where w_k is the AASL-defined semantic urgency weight for task type *k*.

**Gradient computation:**

The gradient of Φ with respect to agent *i*'s strategy is:

```
∂Φ/∂s_i[k] = D_k · c_i / (Σ_{j=1}^{4} c_j · s_j[k] + ε) - 2μ · (s_i[k] - 1/K)
```

The full gradient vector for agent *i* is:

```
∇Φ_i = [∂Φ/∂s_i[1], ∂Φ/∂s_i[2], ..., ∂Φ/∂s_i[K]]
```

**Update rule:**

Agent *i* updates its strategy by gradient ascent on Φ (equivalently, gradient descent on J_i):

```
s_i(t+1) = Proj_Δ( s_i(t) + η · ∇Φ_i )
```

where:
- η > 0 is the step size (default: η = 0.1)
- Proj_Δ is the projection onto the K-simplex, ensuring s_i(t+1) remains a valid probability distribution

**Simplex projection** (Duchi et al. 2008):

Given an unconstrained update vector *v*, project onto Δ^K:

```
function project_simplex(v: float[K]) -> float[K]:
    sort v in descending order → v_sorted
    find ρ = max { j ∈ {1..K} : v_sorted[j] - (1/j)(Σ_{r=1}^{j} v_sorted[r] - 1) > 0 }
    τ = (1/ρ)(Σ_{r=1}^{ρ} v_sorted[r] - 1)
    return max(v - τ, 0)   // element-wise
```

**Output:** The gradient vector ∇Φ_i tells agent *i* which task types are under-served relative to demand, weighted by the agent's capability. Following the gradient increases the cluster's overall allocation efficiency.

---

### 7.3 Tidal Reset Perturbation

At each epoch boundary, a random perturbation is injected into each agent's strategy to escape local minima of the potential function. This mechanism is analogous to simulated annealing.

**Perturbation injection:**

```
s_i_perturbed = Proj_Δ( s_i + ε_i )
```

where ε_i ~ N(0, σ²I_K), a K-dimensional Gaussian with isotropic covariance.

**Annealing schedule for σ:**

```
σ(epoch) = max(σ_min, σ_initial × decay_rate^stability_count)
```

where:
- σ_initial = 0.3 (initial perturbation magnitude; configurable)
- σ_min = 0.01 (floor to ensure non-zero exploration; configurable)
- decay_rate = 0.9 (per-stable-epoch decay; configurable)
- stability_count = number of consecutive epochs where the cluster reached Nash equilibrium (convergence_status = true)

**Behavior:**
- When the cluster is new or recently reformed: σ is large, providing broad exploration.
- As the cluster stabilizes: σ decreases, refining the allocation toward the best-known equilibrium.
- If the cluster is dissolved and reformed (e.g., due to member failure), stability_count resets to 0 and σ returns to σ_initial.

**Purpose:** Without perturbation, the potential game may converge to a suboptimal local maximum of Φ. Tidal reset perturbations provide a mechanism analogous to temperature in simulated annealing: early epochs explore broadly, later epochs exploit the best-found equilibrium. The tidal boundary is a natural synchronization point — all cluster members apply perturbation simultaneously, maintaining cluster coherence.

---

### 7.4 Cluster Management Protocol

**Tetrahedron formation:**

At each tidal boundary where cluster formation is required (initial deployment, member failure requiring reformation, or governance-triggered restructuring), the Tidal Function Engine assigns agents to tetrahedral clusters.

Assignment criteria:
1. **Capability complementarity:** Prefer clusters where the union of member capabilities covers the broadest range of task types. Formally, maximize |∪_{i ∈ C} TaskTypes(i)| across clusters.
2. **Topological proximity:** Prefer clusters where members are close on the CIOS topology (minimizes intra-cluster communication latency).
3. **Load balance:** Equalize aggregate capacity across clusters.

The assignment is deterministic: given the agent roster and their capabilities, any agent can independently compute the same cluster assignments using a stable sorting algorithm over (capability_coverage, topology_distance, capacity) tuples mapped through the consistent hash ring.

**State sharing within cluster:**

Each cluster member broadcasts its local state to the other 3 members at every gradient update step:

```
ClusterStateMessage {
    agent_id:       AgentID
    epoch:          uint64
    step:           uint32          // gradient step number within epoch
    queue_depths:   float[K]        // task queue depths per type
    current_strategy: float[K]      // current allocation strategy
    capability_scores: float[K]     // per-type capability
}
```

Communication within a cluster is bounded: 3 messages per agent per gradient step, with each message of size O(K). At K = 10 and 100 gradient steps per epoch, this is 300 messages per agent per epoch — a small constant independent of total system size N.

**Dissolution triggers:**

A tetrahedral cluster is dissolved when:
- 2 or more members fail within a single epoch (detected by absence of cluster state messages for > 50% of gradient steps)
- Coherence score falls below the dissolution threshold (default: 0.3) for 3 consecutive epochs
- Governance explicitly disbands the cluster

**Reformation protocol:**

1. At the next tidal boundary following dissolution, surviving agents are placed into a reformation pool.
2. The Tidal Function Engine computes new cluster assignments from the pool plus any unassigned agents.
3. New clusters begin in cold-start state (stability_count = 0, σ = σ_initial).
4. Any in-progress work by the dissolved cluster continues under tidal backbone scheduling (Layer 1); only the intra-cluster allocation optimization is interrupted.

**Degraded operation (3-agent cluster):**

When exactly 1 member fails, the remaining 3 agents continue operating as a reduced cluster:
- The potential function is recomputed over 3 agents instead of 4.
- The failed agent's capacity share is redistributed via gradient rebalancing.
- The reduced cluster operates until the next tidal boundary, at which point it either receives a replacement member or is dissolved and reformed.

---

### 7.5 Algorithm Pseudocode (Layer 3)

#### 7.5.1 compute_field_gradient

```
function compute_field_gradient(
    cluster_state: ClusterState,
    aasl_dimensions: SemanticDimensions
) -> Map<AgentID, float[K]>:
    K = aasl_dimensions.task_type_count
    members = cluster_state.members                  // list of 4 (or 3) agents

    // Compute demand vector
    D = zeros(K)
    for agent in members:
        for k in 0..K:
            D[k] += cluster_state.queue_depth[agent][k] * aasl_dimensions.urgency_weight[k]

    gradients = {}
    for agent_i in members:
        grad = zeros(K)
        for k in 0..K:
            // Total capability-weighted allocation to task type k
            total_alloc = EPSILON
            for agent_j in members:
                total_alloc += cluster_state.capability[agent_j][k]
                               * cluster_state.strategy[agent_j][k]

            // Gradient component
            grad[k] = D[k] * cluster_state.capability[agent_i][k] / total_alloc
                      - 2 * MU * (cluster_state.strategy[agent_i][k] - 1.0 / K)

        gradients[agent_i] = grad

    return gradients
```

#### 7.5.2 update_allocation

```
function update_allocation(
    current_strategy: float[K],
    gradient: float[K],
    step_size: float
) -> float[K]:
    // Gradient ascent step
    unconstrained = current_strategy + step_size * gradient

    // Project onto simplex
    new_strategy = project_simplex(unconstrained)

    return new_strategy
```

#### 7.5.3 apply_tidal_perturbation

```
function apply_tidal_perturbation(
    strategy: float[K],
    epoch: uint64,
    stability_count: uint32
) -> float[K]:
    // Compute annealing sigma
    sigma = max(SIGMA_MIN, SIGMA_INITIAL * DECAY_RATE ^ stability_count)

    // Generate perturbation (deterministic given epoch + agent_id as seed)
    rng = seeded_rng(hash(epoch, agent_id))
    perturbation = rng.normal(mean=0, std=sigma, size=K)

    // Apply and project
    perturbed = strategy + perturbation
    perturbed = project_simplex(perturbed)

    return perturbed
```

**Note on determinism:** The perturbation uses a deterministic PRNG seeded with hash(epoch, agent_id). Given the same epoch and agent_id, any implementation produces the same perturbation vector. This preserves PTA's determinism property — cluster allocation is reproducible from shared inputs.

---

## 8. Economic Settlement Protocol

### 8.1 Settlement Timing

Settlement computation occurs at designated epoch boundaries. Not every epoch boundary is a settlement boundary; settlement frequency is a governance parameter defined in the TidalVersion (default: every epoch).

The settlement is a pure function:

```
settlement_ledger = settle(tidal_schedule, event_log, model_accuracy_records, economic_parameters)
```

Given identical inputs, any agent or auditor independently computes an identical settlement ledger.

### 8.2 Settlement Streams

The net settlement for agent *a* at settlement epoch *e* is:

```
net_settlement(a, e) = compliance_reward(a, e)
                     - surprise_cost(a, e)
                     + prediction_bonus(a, e)
                     + verification_reward(a, e)
```

#### 8.2.1 Compliance Reward

```
compliance_reward(a, e) = R_base × compliance_score(a, e)
```

where:
- R_base ∈ ℝ>0 is the base reward rate (AIC tokens per epoch; field of TidalVersion)
- compliance_score(a, e) ∈ [0, 1] measures agent *a*'s adherence to the tidal schedule in epoch *e*

Compliance score computation:

```
compliance_score(a, e) = (tasks_completed_on_time(a, e) + 0.5 × tasks_completed_late(a, e))
                         / tasks_assigned(a, e)
```

where:
- tasks_completed_on_time: assignments completed within the epoch they were scheduled
- tasks_completed_late: assignments completed in the epoch immediately following (grace period)
- tasks_assigned: total assignments from the tidal schedule for agent *a* in epoch *e*

If tasks_assigned = 0 (agent had no assignments), compliance_score = 1.0 (neutral).

#### 8.2.2 Surprise Cost

```
surprise_cost(a, e) = R_surprise × total_surprise_magnitude(a, e)
```

where:
- R_surprise ∈ ℝ≥0 is the surprise cost rate (AIC tokens per unit magnitude; field of TidalVersion)
- total_surprise_magnitude(a, e) = Σ over all surprise signals originated by agent *a* in epoch *e* of their magnitude values

This incentivizes predictable behavior. Agents that deviate from expectations pay a cost proportional to the magnitude of their deviation.

When Layer 2 is inactive (no prediction models), surprise_cost = 0 for all agents.

#### 8.2.3 Prediction Bonus

```
prediction_bonus(a, e) = R_prediction × avg_model_accuracy(a, e)
```

where:
- R_prediction ∈ ℝ≥0 is the prediction bonus rate (AIC tokens per unit accuracy; field of TidalVersion)
- avg_model_accuracy(a, e) = (1/|N(a)|) × Σ_{i ∈ N(a)} model_accuracy_a_i(e)
- N(a) is the set of agent *a*'s direct neighbors
- model_accuracy_a_i(e) is agent *a*'s prediction model accuracy for neighbor *i* in epoch *e*

This incentivizes agents to maintain accurate prediction models of their neighbors, which reduces system-wide communication overhead.

When Layer 2 is inactive, prediction_bonus = 0 for all agents.

#### 8.2.4 Verification Reward

```
verification_reward(a, e) = R_verify × verification_participation(a, e)
```

where:
- R_verify ∈ ℝ≥0 is the verification fee rate (AIC tokens per verification duty; field of TidalVersion)
- verification_participation(a, e) = count of verification duties fulfilled by agent *a* in epoch *e*, as reported by Verichain via VerificationReceipt messages

Agents that fulfill their VRF-assigned verification duties earn fees. Agents that fail to fulfill verification duties (timeout or absence) earn 0 for those duties and may incur a compliance score penalty (verification non-fulfillment counts as an incomplete assignment).

### 8.3 Determinism Guarantee

The settlement computation is deterministic if and only if all inputs are identical:

| Input | Source | Determinism property |
|---|---|---|
| tidal_schedule | Tidal Function Engine | Deterministic by construction (pure function of version + roster + epoch) |
| event_log | Local observation + received surprise signals | Eventual consistency within grace period; settlement waits for grace period |
| model_accuracy_records | Prediction Model Manager | Deterministic given identical observation sequences |
| economic_parameters | TidalVersion | Deterministic; updated only at version boundaries |

**Grace period:** Settlement computation is deferred by grace_period epochs (default: 1) after the settlement epoch boundary to allow late-arriving events to be incorporated. Events arriving after the grace period are excluded from that epoch's settlement and cannot be retroactively applied.

**Settlement proof:** After computation, a deterministic hash is generated over all inputs and the resulting ledger:

```
settlement_proof = SHA-256(
    canonical_serialize(tidal_schedule) ||
    canonical_serialize(event_log) ||
    canonical_serialize(model_accuracy_records) ||
    canonical_serialize(economic_parameters) ||
    canonical_serialize(settlement_ledger)
)
```

Any auditor with the same inputs can verify the proof by recomputing the settlement.

### 8.4 Parameter Governance

All economic parameters (R_base, R_surprise, R_prediction, R_verify) are fields of the TidalVersion data structure. They are updated only at version boundaries, never mid-version. This ensures that all agents within a version compute settlements using identical rates.

Rate changes follow the tidal version migration protocol (Section 9): proposed in a new version, evaluated during the overlap period, and activated only upon successful migration.

---

## 9. Tidal Version Management Protocol

### 9.1 Version Lifecycle

A TidalVersion progresses through five states:

```
PROPOSED → PUBLISHED → OVERLAP → ACTIVE → DEPRECATED
```

**State definitions:**

| State | Description |
|---|---|
| PROPOSED | Version definition submitted by governance; not yet visible to agents |
| PUBLISHED | Version definition distributed to all agents; evaluation may begin but no execution |
| OVERLAP | Both the current ACTIVE version and this version are evaluated simultaneously |
| ACTIVE | This version is the primary execution version for the system |
| DEPRECATED | This version has been superseded; retained for audit trail only |

### 9.2 State Transitions

```
PROPOSED --[governance approval]--> PUBLISHED
PUBLISHED --[activation_epoch reached]--> OVERLAP
OVERLAP --[migration_threshold met]--> ACTIVE (previous version → DEPRECATED)
OVERLAP --[overlap_duration expired without threshold]--> (this version discarded; previous remains ACTIVE)
ACTIVE --[new version enters OVERLAP]--> (remains ACTIVE until new version reaches ACTIVE)
ACTIVE --[governance deprecation]--> DEPRECATED
```

**Transition triggers:**

| Transition | Trigger | Authority |
|---|---|---|
| PROPOSED → PUBLISHED | Governance approval | Human governance |
| PUBLISHED → OVERLAP | Current epoch ≥ activation_epoch | Automatic (deterministic) |
| OVERLAP → ACTIVE | observed_fraction_on_new ≥ migration_threshold | Per-agent Schelling point decision |
| OVERLAP → discarded | Current epoch ≥ activation_epoch + overlap_duration AND observed_fraction_on_new < migration_threshold | Automatic (deterministic) |
| ACTIVE → DEPRECATED | New version reaches ACTIVE state | Automatic |

### 9.3 Overlap Period

**Duration:** Governance parameter overlap_duration (default: 10 epochs). This is the maximum time agents have to migrate to the new version.

**Dual evaluation:** During the overlap period, each agent computes assignments under both the current ACTIVE version and the OVERLAP version:

```
schedule_current = evaluate(agent_id, task_types, epoch, active_version)
schedule_new     = evaluate(agent_id, task_types, epoch, overlap_version)
```

The agent executes schedule_current while computing schedule_new for comparison. This allows agents to observe whether the new version produces acceptable assignments before switching.

**Migration signal (Schelling point dynamics):**

Each agent independently decides when to switch its primary execution to the new version. The decision rule is:

```
if fraction_of_observed_peers_on_new_version ≥ migration_threshold:
    switch_to_new_version()
```

where:
- migration_threshold ∈ (0.5, 1.0) (governance parameter, default: 0.67)
- The fraction is computed from the version field embedded in capacity snapshots received at epoch boundaries

This creates a Schelling-point coordination game: agents switch when they believe enough peers have switched. The migration threshold ensures that a supermajority is on the new version before any individual agent commits.

**Early adopter incentive:** Agents that switch early (within the first 25% of the overlap period) and the migration succeeds receive a small bonus in the first settlement under the new version. This accelerates convergence to the Schelling point.

### 9.4 Rollback

If migration does not reach migration_threshold within overlap_duration epochs:

1. The overlap version is discarded (state: never reaches ACTIVE).
2. All agents that switched to the new version revert to the previous ACTIVE version.
3. Reversion is deterministic: at epoch activation_epoch + overlap_duration, the overlap version ceases to exist. Agents must be on the previous ACTIVE version by this epoch.
4. Work performed under the new version during the overlap is settled using the economic parameters of the new version (the work was valid under the version it was performed against).
5. Governance is notified of the migration failure for analysis.

### 9.5 Version Data Structure

```
TidalVersion {
    version_id:           uint64        // monotonically increasing identifier
    hash_ring_config: {
        virtual_nodes_per_agent: uint32 // number of virtual nodes per agent
        hash_function:           string // hash algorithm identifier (e.g., "SHA-256-TRUNC-64")
        ring_count:              uint32 // number of hash rings (one per task type)
    }
    vrf_seeds: {
        current_seed:        bytes32    // active VRF seed
        rotation_interval:   uint64     // epochs between seed rotations
        seed_commitment:     bytes32    // commitment to next seed (anti-grinding)
    }
    epoch_length:            uint64     // epoch duration in milliseconds
    task_type_bands: [                  // frequency bands for task types
        {
            task_type:       string     // AASL claim type identifier
            frequency_band:  string     // HIGH | MEDIUM | LOW | BATCH
            priority:        uint32     // scheduling priority within band
        }
    ]
    activation_epoch:        uint64     // epoch at which OVERLAP begins
    deactivation_epoch:      uint64     // epoch at which DEPRECATED (set when superseded)
    economic_parameters: {
        base_reward_rate:       float64 // R_base
        surprise_cost_rate:     float64 // R_surprise
        prediction_bonus_rate:  float64 // R_prediction
        verification_fee_rate:  float64 // R_verify
        settlement_frequency:   uint32  // settle every N epochs
        grace_period:           uint32  // epochs to wait for late events
    }
    migration_parameters: {
        overlap_duration:       uint32  // epochs
        migration_threshold:    float64 // fraction of peers required
        early_adopter_window:   uint32  // epochs (first N of overlap for bonus)
        early_adopter_bonus:    float64 // AIC bonus amount
    }
}
```

The version is immutable once published: no field may be modified after the PUBLISHED state transition. New parameters require a new version.

---

## 10. Conformance and Verification

### 10.1 Determinism Conformance

The foundational property of PTA is determinism: two independent implementations given identical inputs must produce identical outputs for all Layer 1 computations and all settlement computations.

**Determinism test:**

Given a reference input set R = (agent_roster, task_types, epoch_sequence, event_log, tidal_version), two implementations A and B must satisfy:

```
∀ inputs ∈ R:
    schedule_A(inputs) == schedule_B(inputs)
    verifier_set_A(inputs) == verifier_set_B(inputs)
    settlement_A(inputs) == settlement_B(inputs)
```

Equality is bitwise for integer outputs and within ε = 10⁻¹² for floating-point outputs (to accommodate IEEE 754 rounding differences across platforms).

**Reference input generation:**

The conformance test suite includes a deterministic reference input generator that produces:
- 10 agent rosters of varying sizes (10, 100, 1000 agents)
- 5 tidal version configurations with varying parameters
- 20-epoch event logs with known surprise events, verification results, and churn events
- Expected outputs for each input set, generated by the reference implementation

### 10.2 Layer 1 Conformance — MINIMUM REQUIRED

Layer 1 conformance is the minimum requirement for PTA compliance. An implementation is Layer 1 conformant if and only if it passes all of the following:

| Test Category | Tests | Requirement |
|---|---|---|
| Hash ring determinism | Given (agent_roster, task_type, epoch, version), the computed assignment matches the reference output | 100% match |
| VRF correctness | Given (claim_hash, epoch, seed), the computed verifier set matches the reference output; VRF proof verifies | 100% match |
| Epoch clock correctness | Epoch boundaries are detected at the correct wall-clock times within NTP tolerance | Within ±tolerance |
| Settlement determinism | Given (schedule, event_log, parameters), the computed settlement matches the reference output | 100% match (within ε for floats) |
| Substitution correctness | Given an agent failure, the substitution agent matches the hash ring successor | 100% match |
| Version migration | Given a migration scenario, the agent switches or rolls back at the correct epoch | 100% match |
| Capacity snapshot protocol | Snapshots are compiled, propagated, and aggregated correctly per the gossip protocol | Functional test pass |

### 10.3 Layer 2 Conformance — OPTIONAL ENHANCEMENT

Layer 2 conformance is optional. An implementation may omit Layer 2 entirely and remain PTA-compliant (operating in standard messaging mode).

If Layer 2 is implemented, conformance requires:

| Test Category | Tests | Requirement |
|---|---|---|
| RLS model correctness | Given an observation sequence, the model parameters after N updates match the reference output | Within ε for floats |
| Threshold adaptation | Given an error sequence, the threshold trajectory matches the reference output | Within ε |
| Surprise signal format | Generated surprise signals match the specified message format | Structural match |
| Propagation radius | Given a magnitude and θ_base, the computed radius matches floor(log₂(magnitude/θ_base)) | 100% match |
| Damping | Signal magnitude at hop *h* matches magnitude × δ^h | Within ε |
| Cold-start protocol | Transition from STANDARD to PREDICTIVE occurs at the correct epoch given the accuracy trajectory | 100% match |
| Deduplication | Duplicate (source_id, epoch) signals are processed at most once | Functional test pass |
| Signal budget | No more than B_max signals originated per agent per epoch | Hard limit verified |

### 10.4 Layer 3 Conformance — OPTIONAL ENHANCEMENT (PENDING DECISION GATE)

Layer 3 conformance is optional and pending the Phase 2 decision gate. An implementation may omit Layer 3 entirely.

If Layer 3 is implemented, conformance requires:

| Test Category | Tests | Requirement |
|---|---|---|
| Potential function evaluation | Given (cluster_state, demand_vector, parameters), Φ(s) matches the reference output | Within ε |
| Gradient computation | Given (cluster_state, AASL dimensions), the gradient vector matches the reference output | Within ε |
| Simplex projection | Given an unconstrained vector, the simplex projection matches the reference output | Within ε |
| Strategy update | Given (strategy, gradient, step_size), the updated strategy matches the reference output | Within ε |
| Tidal perturbation determinism | Given (epoch, agent_id, stability_count), the perturbation vector matches the reference output | 100% match (deterministic PRNG) |
| Cluster formation | Given (agent_roster, capabilities), the cluster assignment matches the reference output | 100% match |
| Cluster dissolution | Dissolution triggered correctly when 2+ members fail | Functional test pass |
| Convergence detection | Nash equilibrium correctly detected when gradient magnitudes fall below convergence threshold | Functional test pass |

### 10.5 Test Suite Outline

#### 10.5.1 Unit Tests (per algorithm)

| Component | Unit Tests |
|---|---|
| Consistent hash ring | Ring construction, lookup, virtual node mapping, add/remove agent, key redistribution fraction |
| VRF computation | Evaluate, prove, verify, seed rotation, determinism across calls |
| RLS model (Layer 2) | Initialization, single update, convergence on synthetic data, forgetting factor effect |
| Threshold adaptation (Layer 2) | Tightening, loosening, floor/ceiling enforcement, hysteresis guard, non-stationarity detection |
| Surprise signal (Layer 2) | Magnitude computation, radius calculation, damping, deduplication, budget enforcement |
| Potential function (Layer 3) | Evaluation at known states, gradient correctness via finite differences, simplex projection |
| Settlement calculator | Each stream independently (compliance, surprise cost, prediction bonus, verification reward), net computation, proof generation |
| Version manager | State transitions, overlap dual evaluation, migration threshold check, rollback trigger |

#### 10.5.2 Integration Tests (per data flow)

| Data Flow | Integration Test |
|---|---|
| Epoch boundary processing | Full boundary sequence (snapshot → settlement → recalibration → hash ring update → version check → schedule) produces correct outputs |
| Surprise propagation | Surprise generated at agent A propagates correctly through B and C with proper damping, dedup, and budget |
| Cold-start to predictive transition | Agent begins in STANDARD mode, model trains, transitions to PREDICTIVE at correct epoch |
| Cluster gradient convergence | 4-agent cluster converges to Nash equilibrium within expected iteration count |
| Version migration end-to-end | New version published → overlap → sufficient agents switch → migration succeeds → old version deprecated |
| Version rollback end-to-end | New version published → overlap → insufficient agents switch → rollback → all agents on previous version |
| Settlement with all streams | Epoch with compliance events, surprises, prediction data, and verification results produces correct net settlement |

#### 10.5.3 End-to-End Determinism Tests

| Test | Description |
|---|---|
| Two-implementation agreement | Run the reference implementation and the implementation-under-test with identical inputs for 100 epochs; verify bitwise-identical outputs at every epoch boundary |
| Replay determinism | Record all inputs for a 100-epoch run; replay the inputs and verify identical outputs |
| Cross-platform determinism | Run the same implementation on two platforms (e.g., Linux x86_64 and Linux aarch64); verify outputs match within floating-point ε |
| Churn determinism | Inject identical churn sequences into two instances; verify identical schedule and settlement outputs after convergence |
| Adversarial determinism | Inject identical adversarial behavior into two instances; verify identical surprise signals, settlement costs, and anomaly signals |

---

*End of Technical Specification Part 2.*

*Part 1 covers: System overview, primitives, Layer 1 (Tidal Backbone) protocol specification, core data structures, and the Tidal Function family definition.*
