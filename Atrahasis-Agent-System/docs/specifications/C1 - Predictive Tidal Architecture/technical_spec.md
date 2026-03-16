# C1 — Predictive Tidal Architecture (PTA): Technical Specification

**Invention ID:** C1
**Stage:** DESIGN
**Version:** v0.1
**Date:** 2026-03-09
**Status:** DRAFT
**Scope:** Part 1 — Specification Overview, System Primitives, Layer 1 (Tidal Backbone)

> **Note:** Part 2 (Layers 2-3, economic settlement, version management) follows in a subsequent section.

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
