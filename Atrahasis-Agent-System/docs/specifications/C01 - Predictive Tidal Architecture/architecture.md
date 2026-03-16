# C1 — Predictive Tidal Architecture (PTA): System Architecture

**Invention ID:** C1
**Stage:** DESIGN
**Date:** 2026-03-09
**Status:** DRAFT
**Assessment Council Verdict:** CONDITIONAL_ADVANCE (ADR-002)

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
