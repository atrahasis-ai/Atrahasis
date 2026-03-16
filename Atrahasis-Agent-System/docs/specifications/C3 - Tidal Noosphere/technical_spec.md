# Tidal Noosphere -- Technical Specification
## C3-A DESIGN Document

**Invention ID:** C3
**Concept:** C3-A Tidal Noosphere
**Version:** v0.1
**Date:** 2026-03-09
**Status:** DRAFT
**Predecessor Specs:** Noosphere Master Spec v5, PTA Complete Design v0.1
**Primary Scale Target:** 1K--10K agents (100K+ aspirational, contingent on Phase 3 results)

---

### 1. Specification Overview

#### 1.1 Scope

This document formally specifies the Tidal Noosphere: the unified coordination architecture formed by absorbing PTA's deterministic scheduling engine into the Noosphere's epistemic coordination fabric and adopting the Locus Fabric's formal proof obligations as mandatory standards. It defines all data structures, algorithms, protocols, and wire formats required for an independent implementation.

This specification covers:
- System primitives and their formal definitions (Section 2)
- The five-class operation algebra with I-confluence grounding (Sections 3, 10)
- Tidal scheduling within parcels via bounded-loads consistent hashing (Section 4)
- VRF-based verifier selection with dual defense against grinding and filter exploitation (Section 5)
- Dual communication: predictive delta (intra-parcel) and stigmergic decay (locus-scope) (Section 6)
- Parcel transition, emergency rollback, and governance protocols (Sections 7, 8, 9)
- AASL extension and settlement (Sections 11, 12)

This specification does NOT cover: the Noosphere's verification membrane internals (see Noosphere Spec Sections 13--22), the Fusion Capsule Epoch Protocol (see Noosphere Spec Section 12), or PTA Layer 3 Morphogenic Fields (discarded per Science Assessment recommendation).

#### 1.2 Conventions

- **MUST**, **SHOULD**, **MAY** follow RFC 2119 semantics.
- Epoch indices are 0-based unsigned 64-bit integers.
- All hashes use SHA-256 unless stated otherwise.
- `||` denotes byte-level concatenation.
- `H(x)` denotes `SHA-256(x)`.
- Set membership: `x in S`. Set cardinality: `|S|`.
- All pseudocode uses Python-like syntax with explicit types.
- Time is measured in epochs unless wall-clock time is specified.

#### 1.3 Relationship to Parent Specifications

| Concern | Authoritative Spec |
|---|---|
| Locus/Parcel model, operation-class algebra, verification membrane, knowledge cortex, economics | Noosphere Master Spec v5 |
| Hash ring construction, epoch clock, VRF computation, settlement calculation | PTA Complete Design v0.1 (as amended herein) |
| Tidal scheduling within parcels, dual communication, VRF dual defense, parcel transitions, ETR | **This specification** |

Where this specification conflicts with the parent specs, this specification governs for the subsystems it defines. The Noosphere Spec governs for all other subsystems.

---

### 2. System Primitives

#### 2.1 Structural Primitives

**Definition 2.1 (Locus).** A stable logical coordination domain:
```
Locus := {
  id:             LocusId        -- globally unique identifier
  selector:       NamespaceSelector
  invariant_set:  Set<Invariant> -- correctness constraints
  safety_class:   {LOW, MEDIUM, HIGH, CRITICAL}
  epoch_class:    {standard, accelerated}
  parcels:        Set<ParcelId>  -- current parcel decomposition
  state:          {CREATED, ACTIVE, SPLIT, MERGED, QUIESCENT, ARCHIVED}
}
```

**Definition 2.2 (Parcel).** An elastic physical execution unit within a locus:
```
Parcel := {
  id:             ParcelId
  locus:          LocusId
  agents:         Set<AgentId>   -- current agent assignment, |agents| >= 5
  hash_rings:     Map<TaskType, HashRing>
  slv:            ScopeLoadVector
  epoch:          uint64
  state:          {ACTIVE, TRANSITIONING, DEGRADED, DISSOLVED}
}
```
Invariant: `|Parcel.agents| >= PARCEL_MIN_AGENTS` (default 5).

**Definition 2.3 (Agent).** A participating entity:
```
Agent := {
  id:             AgentId        -- cryptographic identity
  pubkey:         ECPublicKey    -- ECVRF public key (P-256)
  privkey:        ECPrivateKey   -- ECVRF private key (local only)
  capabilities:   Set<TaskType>
  capacity:       float64        -- [0.0, 1.0] normalized
  stake:          uint64         -- AIC staked
  reputation:     float64        -- [0.0, 1.0]
  parcel:         ParcelId       -- current parcel assignment
  locus:          LocusId
  diversity_attr: DiversityCommitment
  governance:     bool           -- governance participant
}
```

**Definition 2.4 (Epoch).** A discrete time interval:
```
Epoch := {
  index:          uint64         -- monotonically increasing
  start_time:     Timestamp      -- NTP-synchronized wall-clock
  duration:       Duration       -- configurable, default 3600s
  tidal_version:  TidalVersionId -- active tidal function version
  vrf_seed:       bytes[32]      -- VRF seed for this epoch
}
```
Epoch boundaries are synchronized via NTP (tolerance: 500ms). Agents exceeding tolerance are treated as timing-faulty.

#### 2.2 Scheduling Primitives

**Definition 2.5 (Hash Ring).** A bounded-loads consistent hash ring:
```
HashRing := {
  task_type:      TaskType
  parcel:         ParcelId
  entries:        SortedArray<(uint256, AgentId)>  -- (position, agent)
  virtual_nodes:  uint32         -- V per physical agent
  epsilon:        float64        -- bounded-loads tolerance
  agent_count:    uint32         -- N physical agents
}
```
Ring positions are computed as `pos(agent, vnode) = H(agent.id || task_type || vnode_index) mod 2^256`.

**Definition 2.6 (Virtual Node Count).** For a parcel with N agents:
```
V(N) = max(VNODE_MIN, ceil(VNODE_SCALE / N))
```
Default: `VNODE_MIN = 150`, `VNODE_SCALE = 1000`. For N=5, V=200; for N=50, V=150.

**Definition 2.7 (Tidal Function).** A deterministic pure function:
```
TidalFunction := {
  version:        TidalVersionId
  hash_config:    HashRingConfig   -- ring parameters per task type
  vrf_seeds:      SeedSchedule     -- seed rotation schedule
  epoch_length:   Duration
  task_types:     Set<TaskType>    -- active task types
  economic_params: EconomicConfig  -- settlement parameters
  activation_epoch: uint64
  predecessor:    TidalVersionId | null
}
```
Invariant: For identical inputs, all conformant implementations MUST produce identical outputs.

**Definition 2.8 (Tidal Version).** An immutable, content-addressed tidal function definition:
```
TidalVersionId = H(canonical_serialize(TidalFunction))
```

#### 2.3 Verification Primitives

**Definition 2.9 (Claim).** An AASL-typed epistemic assertion (per Noosphere Spec Section 6.5):
```
Claim := {
  id:             ClaimId
  claim_class:    {deterministic, empirical, statistical, heuristic, normative}
  claim_type:     {observation, derivation, synthesis, hypothesis, prediction}
  locus:          LocusId
  agent:          AgentId
  body:           AASLRef
  evidence:       List<EvidenceRef>
  hash:           bytes[32]      -- H(canonical_serialize(claim_body))
  epoch:          uint64         -- submission epoch
}
```

**Definition 2.10 (Operation).** A typed action with a derived agreement class:
```
Operation := {
  id:             OperationId
  op_type:        OperationType
  locus_footprint: Set<LocusId>
  class:          {M, B, X, V, G}  -- derived, not chosen
  payload:        bytes
}
```

**Definition 2.11 (Operation Class).** The five agreement classes:
```
M  -- Merge/Convergence: CRDT-like, zero coordination, I-confluence proven
B  -- Bounded Local Commit: CSO local spend, epoch-boundary rebalancing
X  -- Exclusive: serial commit (single-parcel) or Fusion Capsule (multi-parcel)
V  -- Verification: claim-class-specific membrane protocol
G  -- Governance: BFT constitutional consensus, 75% supermajority
```

#### 2.4 VRF and Diversity Primitives

**Definition 2.12 (VRF Output).** Per ECVRF (RFC 9381) on curve P-256:
```
VRFOutput := {
  gamma:          ECPoint        -- VRF output point
  beta:           bytes[32]      -- VRF hash output = H(point_to_string(gamma))
  pi:             bytes[80]      -- VRF proof (c, s components)
}
```
Computation: `(beta, pi) = ECVRF_prove(privkey, alpha)` where `alpha = H(claim.hash || epoch || vrf_seed)`.

**Definition 2.13 (Diversity Commitment).** An agent's committed diversity attributes:
```
DiversityCommitment := {
  commitment_hash:  bytes[32]    -- H(salt || training_lineage || methodology ||
                                 --   temporal_bucket || region)
  committed_epoch:  uint64       -- epoch at which attributes were committed
  revealed:         bool         -- whether attributes have been revealed
  attributes:       DiversityAttributes | null  -- populated after reveal
  cooling_until:    uint64       -- epoch until which agent is ineligible after change
}
```

**Definition 2.14 (Diversity Attributes).** The revealed attribute vector:
```
DiversityAttributes := {
  training_lineage: bytes[32]    -- hash of training data provenance
  methodology:      MethodologyFamily  -- {replication, cross_reference,
                                       --  logical_check, statistical_analysis,
                                       --  human_review}
  temporal_bucket:  TemporalBucket     -- {recent_6mo, stable_6mo_plus}
  region:           RegionId
  salt:             bytes[16]    -- random salt used in commitment
}
```

**Definition 2.15 (Diversity Pool).** A pre-stratified pool for verifier selection:
```
DiversityPool := {
  dimension:      DiversityDimension  -- which attribute this pool covers
  value:          DiversityValue      -- the specific attribute value
  members:        Set<AgentId>        -- eligible agents in this stratum
  last_updated:   uint64              -- epoch of last membership refresh
}
```

**Definition 2.16 (Commit-Reveal Record).** A registration-time commitment:
```
CommitRevealRecord := {
  agent:          AgentId
  commitment:     DiversityCommitment
  registration_epoch: uint64
  last_change_epoch:  uint64
  change_count:   uint32         -- total lifetime attribute changes
}
```

#### 2.5 Communication Primitives

**Definition 2.17 (Predictive Model).** A per-neighbor linear model:
```
PredictiveModel := {
  neighbor:       AgentId
  weights:        Vector<float64>  -- linear model parameters
  accuracy:       float64          -- rolling accuracy [0.0, 1.0]
  threshold:      float64          -- adaptive surprise threshold
  error_history:  CircularBuffer<float64, 10>  -- last 10 epoch errors
  mode:           {STANDARD, TRANSITIONING, PREDICTIVE}
}
```

**Definition 2.18 (Surprise Threshold).** Adaptive threshold per neighbor:
```
threshold(t+1) = clamp(
  threshold(t) * (1 + THRESHOLD_ADAPT_RATE * (accuracy(t) - THRESHOLD_TARGET_ACCURACY)),
  THRESHOLD_MIN,
  THRESHOLD_MAX
)
```
Default: `THRESHOLD_ADAPT_RATE = 0.1`, `THRESHOLD_TARGET_ACCURACY = 0.8`, `THRESHOLD_MIN = 0.01`, `THRESHOLD_MAX = 1.0`.

**Definition 2.19 (Delta Message).** A surprise-only communication:
```
DeltaMessage := {
  source:         AgentId
  target:         AgentId
  epoch:          uint64
  error_vector:   Vector<float64>  -- prediction error (observed - predicted)
  magnitude:      float64          -- L2 norm of error_vector
  confidence:     float64          -- model confidence at time of surprise
  hop_count:      uint8            -- propagation hops so far
}
```

**Definition 2.20 (Stigmergic Signal).** A locus-scope coordination signal:
```
StigmergicSignal := {
  id:             SignalId
  type:           {need, offer, risk, anomaly, attention_request}
  scope:          LocusId
  issuer:         AgentId
  payload:        AASLRef
  confidence:     float64
  priority:       uint8
  decay_tau:      Duration         -- time constant for exponential decay
  created_at:     Timestamp
  reinforced_at:  Timestamp
  reinforcement_count: uint32
}
```

**Definition 2.21 (Decay Function).** Signal strength at time t:
```
strength(signal, t) = signal.confidence * exp(-(t - signal.reinforced_at) / signal.decay_tau)
```
A signal is considered expired when `strength(signal, t) < SIGNAL_EXPIRY_THRESHOLD` (default 0.01).

#### 2.6 I-Confluence Primitives

**Definition 2.22 (I-Confluence Proof).** A machine-checked proof that an operation preserves invariants under concurrent execution:
```
IConfluenceProof := {
  operation_type: OperationType
  invariant_set:  Set<Invariant>  -- the invariants preserved
  proof_system:   {TLA_PLUS, COQ, F_STAR, IVY}
  proof_artifact: ArtifactRef     -- reference to machine-checked proof
  certified_epoch: uint64
  certifier:      AgentId         -- who produced the proof
  verifiers:      Set<AgentId>    -- who checked the proof
  status:         {PROVISIONAL, CERTIFIED, REVOKED}
}
```

**Definition 2.23 (Operation Classification Record).** The runtime classification of an operation:
```
ClassificationRecord := {
  operation_type: OperationType
  current_class:  {M, B, X, V, G}
  proof:          IConfluenceProof | null  -- null for non-M classes
  provisional:    bool             -- true if empirical-only evidence
  monitoring:     MonitoringConfig | null  -- non-null for provisional M-class
  demoted_from:   {M, B, X, V, G} | null
  demotion_epoch: uint64 | null
}
```

#### 2.7 Settlement Primitives

**Definition 2.24 (Settlement Record).** Per-agent per-epoch settlement:
```
SettlementRecord := {
  agent:          AgentId
  epoch:          uint64
  streams:        SettlementStreams
  total_delta:    int64            -- sum of all streams (AIC microtokens)
  proof:          bytes[32]        -- H(canonical_serialize(inputs || outputs))
}
```

**Definition 2.25 (Economic Streams).** The four settlement components:
```
SettlementStreams := {
  scheduling:     int64   -- tidal compliance reward/penalty
  verification:   int64   -- verification duty fulfillment reward
  communication:  int64   -- prediction accuracy bonus (Phase 2)
  governance:     int64   -- governance participation reward
}
```

---

### 3. Claim Classification Protocol

#### 3.1 The Five Operation Classes

The agreement mode for every operation is derived from its type and locus footprint, never chosen ad hoc. Classification follows a decision procedure:

```
function classify(op: Operation) -> OperationClass:
  if op.op_type in GOVERNANCE_OPS:
    return G
  if op.op_type in VERIFICATION_OPS:
    return V
  if has_certified_proof(op.op_type) or has_provisional_proof(op.op_type):
    return M
  if is_cso_eligible(op.op_type):
    return B
  return X  -- default: exclusive, highest coordination cost
```

#### 3.2 Class Definitions

**M-Class (Merge/Convergence).**
- Precondition: I-confluence proof exists (certified or provisional) for the operation type against the locus invariant set.
- Mechanism: Monotone or CRDT-like state updates. No coordination beyond authenticated anti-entropy.
- Communication: Zero consensus overhead. Sync at epoch boundaries via capacity snapshot.
- Cost: O(1) per operation.

**B-Class (Bounded Local Commit).**
- Precondition: Operation consumes a resource with a conservation law; the resource/invariant pair is CSO-eligible.
- Mechanism: Local CSO decrement. Valid iff all requested dimensions available within owned slice.
- Communication: Zero for local spend. O(N) aggregate at epoch-boundary rebalancing.
- Cost: O(1) per operation; amortized rebalancing.

**X-Class (Exclusive).**
- Default class for operations without I-confluence proofs and without CSO eligibility.
- Mechanism: Single-parcel serial commit OR multi-parcel Fusion Capsule OR Cut Commit (last resort).
- Communication: Quorum protocol within replica group.
- Cost: O(N_replicas) per operation.

**V-Class (Verification).**
- Used for: All claim verification through the membrane.
- Mechanism: VRF-selected committee, claim-class-specific verification protocol.
- Communication: Committee protocol (per Noosphere Spec Sections 13--22).
- Cost: O(committee_size) per claim.

**G-Class (Governance).**
- Used for: Tidal function version changes, membrane rule modifications, slashing, constitutional amendments.
- Mechanism: BFT consensus. 75% supermajority for standard governance. 90% instant supermajority for ETR.
- Communication: Dedicated governance channel (independent of tidal-scheduled data plane).
- Cost: O(N_governance) per action.

#### 3.3 Classification Rules

An operation type transitions between classes according to these rules:

1. All operation types begin as X-class unless pre-classified.
2. An operation type MAY be promoted to M-class when an I-confluence proof is certified.
3. An operation type MAY be promoted to B-class when CSO eligibility is demonstrated.
4. A provisional M-class operation is automatically demoted to B-class (if CSO-eligible) or X-class (otherwise) if monitoring detects a convergence violation.
5. V-class and G-class are determined by operation semantics, not by proofs.
6. Reclassification takes effect at the next epoch boundary.

#### 3.4 Interaction with I-Confluence Proofs

For an operation to be classified M-class, the following MUST hold:

Let `I` be the invariant set of the locus. Let `op` be the operation type. An I-confluence proof demonstrates:

```
For all states s1, s2 reachable from a common ancestor state s0
by applying sequences of operations including op:
  merge(s1, s2) satisfies I
```

where `merge` is the CRDT merge function for the state type. This is the formal I-confluence condition from Bailis et al. (VLDB 2015).

---

### 4. Tidal Scheduling Protocol

#### 4.1 Hash Ring Construction

Within each parcel P, for each active task type T, a bounded-loads consistent hash ring is constructed.

**Algorithm 4.1: Ring Construction**
```
function build_ring(parcel: Parcel, task_type: TaskType) -> HashRing:
  N = |parcel.agents|
  V = max(VNODE_MIN, ceil(VNODE_SCALE / N))
  epsilon = BOUNDED_LOADS_EPSILON  -- default 0.15

  entries = empty sorted array
  for agent in parcel.agents:
    for v in 0..V-1:
      pos = H(agent.id || task_type || uint32_be(v)) mod 2^256
      entries.insert_sorted((pos, agent.id))

  return HashRing{
    task_type = task_type,
    parcel = parcel.id,
    entries = entries,
    virtual_nodes = V,
    epsilon = epsilon,
    agent_count = N
  }
```

#### 4.2 Bounded-Loads Consistent Hashing

This specification mandates the algorithm of Mirrokni, Thorup, and Wieder (SODA 2018). The bound guarantees that no agent receives more than `(1 + epsilon)` times the average load.

**Algorithm 4.2: Bounded-Loads Lookup**
```
function lookup(ring: HashRing, key: bytes) -> AgentId:
  target_pos = H(key) mod 2^256
  avg_load = total_keys / ring.agent_count
  max_load = ceil((1 + ring.epsilon) * avg_load)

  -- Find the first virtual node at or after target_pos
  idx = ring.entries.lower_bound(target_pos)
  if idx >= |ring.entries|:
    idx = 0  -- wrap around

  -- Walk clockwise until finding an agent below max_load
  visited = 0
  while visited < |ring.entries|:
    (pos, agent) = ring.entries[idx]
    if current_load(agent, ring.task_type) < max_load:
      return agent
    idx = (idx + 1) mod |ring.entries|
    visited += 1

  -- Fallback: all agents at max_load (should not occur with correct epsilon)
  ABORT("bounded-loads invariant violated")
```

Load tracking is maintained per-agent per-task-type within the epoch. The `current_load` function returns the number of keys currently assigned to the agent for the given task type.

#### 4.3 Epoch Clock Synchronization

All agents synchronize epoch boundaries via NTP. The epoch clock is a monotonic counter:

```
current_epoch = floor((ntp_time() - GENESIS_TIME) / EPOCH_DURATION)
```

**Timing tolerance:** An agent whose local clock diverges by more than `CLOCK_TOLERANCE` (default 500ms) from NTP is treated as timing-faulty. Persistent drift (3+ consecutive epochs) triggers substitution.

**Epoch boundary detection:**
```
function is_epoch_boundary() -> bool:
  t = ntp_time()
  return (t - GENESIS_TIME) mod EPOCH_DURATION < BOUNDARY_WINDOW
```
where `BOUNDARY_WINDOW` is configurable (default 5s).

#### 4.4 Task-to-Agent Assignment

**Algorithm 4.3: Epoch Assignment**
```
function compute_assignment(
  agent: Agent,
  parcel: Parcel,
  epoch: uint64,
  tidal_version: TidalFunction
) -> List<TaskAssignment>:

  assignments = []
  for task_type in agent.capabilities intersect tidal_version.task_types:
    ring = parcel.hash_rings[task_type]
    -- Generate epoch-specific task keys
    for task_idx in 0..task_count(task_type, epoch)-1:
      task_key = H(task_type || uint64_be(epoch) || uint32_be(task_idx))
      assigned_agent = lookup(ring, task_key)
      if assigned_agent == agent.id:
        assignments.append(TaskAssignment{
          task_type = task_type,
          task_key = task_key,
          epoch = epoch,
          priority = task_priority(task_type, tidal_version)
        })

  -- Sort by priority, shed if over capacity
  assignments.sort_by(a => a.priority, descending)
  if total_load(assignments) > agent.capacity:
    assignments = assignments[:capacity_limit(agent)]
    -- Shed tasks assigned to substitution agents

  return assignments
```

Every agent independently computes the identical assignment from the same inputs. This is the core determinism invariant.

#### 4.5 Agent Join/Leave/Churn Handling

**Join:**
1. New agent registers with parcel via Capacity Snapshot Service at epoch boundary.
2. Hash ring is reconstructed with the new agent's virtual nodes at the next epoch boundary.
3. With bounded-loads, at most `O(epsilon * K / N)` keys remap (where K = total keys, N = agents).
4. New agent enters STANDARD communication mode (no predictive models for neighbors).

**Leave (graceful):**
1. Agent announces departure during current epoch.
2. Substitution list activates: next clockwise agents on hash ring absorb departing agent's assignments.
3. Ring is reconstructed without the departing agent at next epoch boundary.
4. Predictive models referencing the departed agent are invalidated.

**Leave (failure):**
1. Detected by peer observation: missing heartbeats, missed task completions.
2. Substitution list activates immediately (no need to wait for epoch boundary).
3. Ring reconstruction at next epoch boundary.
4. Tolerance: the system operates correctly with stale roster data; assignments are suboptimal but not incorrect.

**Churn budget:** At most `CHURN_BUDGET_FRACTION` (default 0.20) of a parcel's agents MAY change in any single epoch. If churn exceeds this budget, excess joins/leaves are queued to the following epoch.

---

### 5. VRF Dual Defense Protocol

#### 5.1 Base VRF Selection

Verifier sets are computed using ECVRF per RFC 9381 on curve P-256.

**Algorithm 5.1: VRF Verifier Computation**
```
function compute_verifier_set(
  claim: Claim,
  epoch: uint64,
  vrf_seed: bytes[32],
  eligible: Set<Agent>,
  committee_size: uint8
) -> (Set<AgentId>, List<VRFProof>):

  alpha = H(claim.hash || uint64_be(epoch) || vrf_seed)
  candidates = []

  for agent in eligible:
    (beta, pi) = ECVRF_prove(agent.privkey, alpha)
    -- Self-selection: agent is candidate if VRF output below threshold
    threshold = committee_size / |eligible|
    if uint256_from_bytes(beta) < threshold * 2^256:
      candidates.append((agent.id, beta, pi))

  -- Sort candidates by VRF output (deterministic ordering)
  candidates.sort_by(c => c.beta)

  -- Select top committee_size candidates
  selected = candidates[:committee_size]
  return (
    {c.agent_id for c in selected},
    {c.pi for c in selected}
  )
```

Every agent can verify any other agent's VRF proof using `ECVRF_verify(pubkey, alpha, pi)`.

#### 5.2 Commit-Reveal for Diversity Attributes

This mechanism prevents an adversary from grinding the claim hash or timing their registration to maximize selection probability after diversity filtering.

**Protocol 5.2: Diversity Attribute Registration**

Phase 1 -- COMMIT (at agent registration):
```
function commit_diversity(agent: Agent, attrs: DiversityAttributes) -> DiversityCommitment:
  salt = random_bytes(16)
  commitment_hash = H(salt || attrs.training_lineage || attrs.methodology ||
                       attrs.temporal_bucket || attrs.region)
  return DiversityCommitment{
    commitment_hash = commitment_hash,
    committed_epoch = current_epoch(),
    revealed = false,
    attributes = null,
    cooling_until = 0
  }
```

Phase 2 -- REVEAL (after REVEAL_DELAY epochs, default 1):
```
function reveal_diversity(agent: Agent, attrs: DiversityAttributes, salt: bytes[16]):
  commitment = agent.diversity_attr
  assert commitment.revealed == false
  assert current_epoch() >= commitment.committed_epoch + REVEAL_DELAY

  -- Verify commitment matches
  expected = H(salt || attrs.training_lineage || attrs.methodology ||
                attrs.temporal_bucket || attrs.region)
  assert expected == commitment.commitment_hash

  commitment.attributes = attrs
  commitment.revealed = true
```

**Attribute change protocol:**
1. Agent submits new commitment hash.
2. Cooling period activates: agent is ineligible for verifier selection for `DIVERSITY_COOLING_EPOCHS` (default 50) epochs.
3. After cooling, agent reveals new attributes.
4. Old attributes are permanently logged for audit.

**Security property:** An adversary registering Sybil identities MUST commit diversity attributes before knowing which VRF seeds will be used in future epochs. Since VRF seeds rotate every epoch, the mutual information between committed attributes and future committee selection is negligible.

#### 5.3 Pre-Stratified Diversity Pools

Instead of post-filtering VRF-selected candidates (which creates exploitable selection bias), the system pre-stratifies the eligible verifier population into diversity pools.

**Algorithm 5.3: Pool Construction**
```
function build_diversity_pools(
  eligible: Set<Agent>,
  locus: Locus
) -> Map<(DiversityDimension, DiversityValue), DiversityPool>:

  pools = {}
  for agent in eligible:
    if not agent.diversity_attr.revealed:
      continue
    if agent.diversity_attr.cooling_until > current_epoch():
      continue

    attrs = agent.diversity_attr.attributes
    for (dim, val) in [
      (TRAINING_LINEAGE, attrs.training_lineage),
      (METHODOLOGY, attrs.methodology),
      (TEMPORAL_BUCKET, attrs.temporal_bucket),
      (REGION, attrs.region)
    ]:
      key = (dim, val)
      if key not in pools:
        pools[key] = DiversityPool{
          dimension = dim, value = val,
          members = {}, last_updated = current_epoch()
        }
      pools[key].members.add(agent.id)

  return pools
```

Pools are reconstructed at each epoch boundary when the eligible verifier set changes.

#### 5.4 Combined Protocol

The combined VRF + commit-reveal + pre-stratified pools protocol works end-to-end as follows:

**Algorithm 5.4: Diverse Verifier Selection**
```
function select_diverse_verifiers(
  claim: Claim,
  epoch: uint64,
  vrf_seed: bytes[32],
  pools: Map<(DiversityDimension, DiversityValue), DiversityPool>,
  locus: Locus,
  committee_size: uint8  -- default 7
) -> Set<AgentId>:

  alpha = H(claim.hash || uint64_be(epoch) || vrf_seed)
  committee = {}
  used_lineages = {}
  used_methods = {}
  used_buckets = {}
  used_regions = {}

  -- Determine diversity requirements from safety class
  diversity_req = get_diversity_requirements(locus.safety_class)
  -- e.g., for HIGH: min 2 lineages, min 2 methods, min 1 recent + 1 stable

  -- Phase 1: Fill diversity slots by drawing from stratified pools
  for requirement in diversity_req.mandatory_slots:
    pool = pools[(requirement.dimension, requirement.value)]
    if pool is null or |pool.members| == 0:
      continue  -- skip if no agents in this stratum

    -- VRF-select from within this pool
    pool_candidates = []
    for agent_id in pool.members:
      if agent_id in committee:
        continue
      agent = get_agent(agent_id)
      (beta, pi) = ECVRF_prove(agent.privkey, alpha || requirement.dimension)
      pool_candidates.append((agent_id, beta))

    pool_candidates.sort_by(c => c.beta)
    if |pool_candidates| > 0:
      selected = pool_candidates[0].agent_id
      committee.add(selected)
      update_used_sets(selected, used_lineages, used_methods,
                       used_buckets, used_regions)

  -- Phase 2: Fill remaining slots via standard VRF from full eligible set
  all_eligible = union(pool.members for pool in pools.values())
  remaining_candidates = []
  for agent_id in all_eligible:
    if agent_id in committee:
      continue
    agent = get_agent(agent_id)
    (beta, pi) = ECVRF_prove(agent.privkey, alpha)
    remaining_candidates.append((agent_id, beta))

  remaining_candidates.sort_by(c => c.beta)

  for (agent_id, beta) in remaining_candidates:
    if |committee| >= committee_size:
      break
    -- Apply weight cap: no single verifier > 15% of total committee weight
    if would_exceed_weight_cap(agent_id, committee):
      continue
    committee.add(agent_id)

  return committee
```

**Security analysis of the combined mechanism:**

1. **Against claim hash grinding:** The adversary cannot resubmit claims across epochs to shop for committees because claims MUST be committed (hash published) at least 1 epoch before verification scheduling. The claim hash determines the VRF input, and VRF seeds are unknown until the verification epoch.

2. **Against attribute grinding:** Diversity attributes are committed before VRF seeds are known. The 50-epoch cooling period makes attribute changes expensive. The adversary must commit attributes "blind" with respect to future committee selections.

3. **Against filter exploitation:** Pre-stratified pools mean the diversity requirement is satisfied by drawing from pools rather than post-filtering. An adversary with "perfectly diverse" Sybils gains no advantage because the drawing is VRF-randomized within each pool. The adversary's expected advantage is bounded to `< 3%` above random baseline (information-theoretic bound: mutual information between committed attributes and committee selection is negligible when VRF seeds rotate per epoch).

4. **Detection:** The Sentinel Graph's verification affinity matrix (Noosphere Spec Section 15.2 Rule 4) detects statistical anomalies in committee co-occurrence. Agents with "too-perfect" diversity (uniformly spread across all dimensions) trigger `diversity_optimization_suspicion` sentinel edges.

---

### 6. Dual Communication Protocol

#### 6.1 Predictive Delta Channel (Intra-Parcel)

Within each parcel, agents maintain lightweight linear predictive models of each neighbor's behavior relative to the deterministic tidal schedule.

**Model specification:**

For agent A observing neighbor B in epoch e, the predictive model is:
```
predicted_B(e) = W_B * feature_vector(B, e)
```
where `feature_vector` encodes B's scheduled tasks, capacity, recent compliance history, and the tidal function parameters. `W_B` is a weight vector updated via online linear regression.

**Update rule (at epoch boundary):**
```
error(e) = observed_B(e) - predicted_B(e)
W_B := W_B + LEARNING_RATE * error(e) * feature_vector(B, e)^T
accuracy(e) = 1 - |error(e)| / |observed_B(e)|  -- normalized
```
Default: `LEARNING_RATE = 0.01`.

**Surprise threshold computation:**

The adaptive threshold determines when a prediction error warrants communication:
```
threshold_B(e+1) = clamp(
  threshold_B(e) * (1 + 0.1 * (accuracy_B(e) - 0.8)),
  THRESHOLD_MIN, THRESHOLD_MAX
)
```
When `accuracy > 0.8`, the threshold tightens (fewer messages tolerated). When `accuracy < 0.8`, it loosens (more deviations expected).

**Delta message generation:**
```
function check_surprise(agent_A: Agent, neighbor_B: Agent, epoch: uint64):
  model = agent_A.models[neighbor_B.id]
  error = observed(neighbor_B, epoch) - model.predict(neighbor_B, epoch)
  magnitude = l2_norm(error)

  if magnitude > model.threshold:
    emit DeltaMessage{
      source = agent_A.id,
      target = neighbor_B.id,
      epoch = epoch,
      error_vector = error,
      magnitude = magnitude,
      confidence = model.accuracy,
      hop_count = 0
    }
```

**Steady-state zero-communication conditions:**

When all agents follow their tidal schedule exactly and predictive models have converged (accuracy > 0.8 for all neighbors), no surprise signals are generated. The communication cost is exactly zero. This is the O(1) steady-state claim.

Communication occurs only when:
1. An agent deviates from its schedule (surprise).
2. A predictive model is in cold-start mode (STANDARD communication).
3. An external event (stigmergic signal from locus scope) perturbs predictions.

**Signal propagation:**

Delta messages propagate with magnitude-proportional radius and exponential damping:
```
propagation_radius = min(floor(magnitude / RADIUS_UNIT), MAX_RADIUS)
damped_magnitude(hop) = magnitude * DAMPING_FACTOR ^ hop
```
Default: `RADIUS_UNIT = 0.1`, `MAX_RADIUS = 3`, `DAMPING_FACTOR = 0.5`.

A receiving agent applies the damped delta to update its own predictive model of the originating agent.

**Cascade limiter:** Each agent has a per-epoch signal budget of `SIGNAL_BUDGET` (default 50) outgoing delta messages. Excess signals are dropped. This guarantees bounded communication even under adversarial conditions.

#### 6.2 Stigmergic Decay Channel (Locus-Scope)

At locus scope, coordination uses stigmergic signals that decay unless reinforced.

**Signal types:**
| Type | Purpose | Default tau |
|---|---|---|
| `need` | Unmet task demand | 3600s |
| `offer` | Available capacity | 1800s |
| `risk` | Detected anomaly or degradation | 7200s |
| `anomaly` | Sentinel-detected behavioral anomaly | 14400s |
| `attention_request` | Request for governance or human review | 86400s |

**Decay function:**
```
strength(sig, t) = sig.confidence * exp(-(t - sig.reinforced_at) / sig.decay_tau)
```

**Reinforcement rule:** When agent B publishes a signal with matching `(type, scope, payload_hash)`, the existing signal's `reinforcement_count` increments and `reinforced_at` resets to current time. No duplicate signal is created.

**Signal propagation:** Signals propagate to all parcels within the locus via reliable broadcast within the replica group. Cross-locus propagation requires X-class Fusion Capsules or explicit cross-locus signal forwarding.

**Trend signals (extension):** To address the information lag identified in Attack 10 of the Adversarial Report, agents SHOULD emit trend signals carrying gradient information:
```
TrendSignal := {
  base_signal:    SignalId      -- the signal being trended
  gradient:       float64       -- rate of change per epoch
  direction:      {increasing, decreasing, stable}
  confidence:     float64
  window:         uint32        -- epochs observed
}
```
Trend signals allow locus-scope awareness of developing situations before threshold crossings.

#### 6.3 Boundary Interaction

**Predictive Context Transfer (PCT):**

When an agent transfers from parcel P1 to parcel P2:

Step 1 -- Serialize (departing agent):
```
function serialize_context(agent: Agent, old_parcel: Parcel) -> CompactTransferVector:
  ctv = CompactTransferVector{}
  for neighbor in old_parcel.agents:
    model = agent.models[neighbor.id]
    ctv.neighbor_models[neighbor.id] = {
      weights: model.weights,
      accuracy: model.accuracy,
      error_history: model.error_history,
      mode: model.mode
    }
  ctv.behavioral_profile = {
    task_completion_rate: agent.rolling_avg(5, "completions"),
    surprise_frequency: agent.rolling_avg(5, "surprises"),
    resource_consumption: agent.rolling_avg(5, "resources")
  }
  return ctv  -- MUST be <= 1KB per agent
```

Step 2 -- Bootstrap (arriving agent, new neighbors):
```
function bootstrap_model(
  new_neighbor: Agent,
  incoming_agent: Agent,
  ctv: CompactTransferVector
):
  -- Initialize with behavioral profile as prior
  model = PredictiveModel{
    neighbor = incoming_agent.id,
    weights = prior_from_profile(ctv.behavioral_profile),
    accuracy = 0.5,  -- moderate initial confidence
    threshold = THRESHOLD_MAX * 0.5,  -- start moderately loose
    error_history = [],
    mode = TRANSITIONING
  }
  new_neighbor.models[incoming_agent.id] = model
```

Step 3 -- Mode transition:
```
After each epoch, if model.accuracy >= ACTIVATION_THRESHOLD (default 0.7):
  model.mode = PREDICTIVE
```
Expected convergence: 3-5 epochs with PCT (vs 10-15 epochs cold-start without PCT).

**Anomaly promotion (predictive -> stigmergic):**

When a parcel detects sustained anomaly (surprise signals from the same cause for `PROMOTION_THRESHOLD` consecutive epochs, default 3):
```
function promote_to_stigmergic(source_signals: List<DeltaMessage>, locus: LocusId):
  aggregate_error = mean(s.magnitude for s in source_signals)
  emit StigmergicSignal{
    type = risk,
    scope = locus,
    confidence = aggregate_error / max_possible_error,
    decay_tau = 7200,
    ...
  }
```

For CRITICAL safety class loci, the promotion threshold is reduced to 1 epoch.

**Exogenous signal incorporation (stigmergic -> predictive):**

When a locus-scope signal is received by a parcel, the predictive layer incorporates it:
```
function incorporate_exogenous(signal: StigmergicSignal, parcel: Parcel):
  for agent in parcel.agents:
    for model in agent.models.values():
      model.weights += EXOGENOUS_WEIGHT * signal_to_feature(signal)
```
This adjusts predictions for the current epoch, preventing the predictive layer from being blindsided by events visible at locus scope.

---

### 7. Parcel Transition Protocol

The Parcel Transition Protocol (PTP) coordinates simultaneous state changes across all five integration points during parcel reconfiguration.

#### 7.1 Three-Phase Protocol

**Phase 1 -- PREPARE (1 epoch):**
```
function ptp_prepare(controller: BiTimescaleController, affected_parcels: Set<ParcelId>):
  -- Validate: no more than 20% of locus parcels reconfiguring simultaneously
  assert |affected_parcels| <= 0.20 * |locus.parcels|

  for parcel in affected_parcels:
    parcel.state = TRANSITIONING

    -- a) Freeze predictive model updates (models predict but do not adapt)
    for agent in parcel.agents:
      for model in agent.models.values():
        model.frozen = true

    -- b) Cache current VRF verifier sets
    cache_vrf_sets(parcel)

    -- c) Enter communication buffer mode
    parcel.buffer_mode = true  -- outbound surprises queued, not sent

    -- d) Hash rings continue on old configuration
```

**Phase 2 -- SWITCH (at epoch boundary, atomic):**
```
function ptp_switch(controller: BiTimescaleController, reconfig: ReconfigDirective):
  -- This executes at the epoch boundary
  -- All agents have the same inputs (B-class broadcast from Phase 1)

  for parcel in reconfig.affected_parcels:
    -- a) Reconstruct hash rings for new topology
    new_agents = reconfig.new_agent_sets[parcel.id]
    for task_type in parcel.hash_rings.keys():
      parcel.hash_rings[task_type] = build_ring(
        Parcel{agents = new_agents, ...}, task_type
      )

    -- b) Invalidate cached VRF sets, recompute with new eligible pool
    invalidate_vrf_cache(parcel)

    -- c) Flush queued surprise signals (re-route to new neighbors)
    flush_signal_buffer(parcel, reconfig)

    -- d) Mark all predictive models as TRANSITIONING
    for agent in new_agents:
      for model in agent.models.values():
        model.mode = TRANSITIONING
        model.frozen = false
```

**Phase 3 -- STABILIZE (2-5 epochs):**
```
function ptp_stabilize(parcel: Parcel):
  -- Agents operate with:
  --   - Correct hash ring assignments (bounded-loads provides immediate correctness)
  --   - Standard communication (no predictive optimization)
  --   - Predictive models bootstrapping from PCT transfer vectors

  while true:
    agents_stabilized = 0
    for agent in parcel.agents:
      all_models_ready = true
      for model in agent.models.values():
        if model.mode == TRANSITIONING and model.accuracy >= ACTIVATION_THRESHOLD:
          model.mode = PREDICTIVE
        if model.mode != PREDICTIVE:
          all_models_ready = false
      if all_models_ready:
        agents_stabilized += 1

    if agents_stabilized >= 0.90 * |parcel.agents|:
      parcel.state = ACTIVE
      return

    await next_epoch()
```

#### 7.2 Reconfiguration Constraints

1. **Maximum concurrent reconfiguration:** At most 20% of parcels within a locus MAY be in TRANSITIONING state at any time.
2. **Minimum interval:** A parcel MUST remain ACTIVE for at least `RECONFIG_MIN_INTERVAL` (default 10) epochs between reconfigurations.
3. **Circuit breaker:** If >30% of parcels in a locus are simultaneously TRANSITIONING, all further reconfigurations are halted until the count drops below 20%.
4. **Staggering:** The bi-timescale controller staggers reconfigurations within a locus, ensuring no more than 20% of parcels reconfigure in any 10-epoch window.

#### 7.3 State Transfer During Transition

During Phase 2, the following state is transferred for each agent reassignment:

| State Component | Transfer Method | Size Bound |
|---|---|---|
| Hash ring membership | Recomputed locally (deterministic) | 0 bytes |
| VRF eligibility | Recomputed locally | 0 bytes |
| Predictive model context | Compact Transfer Vector (PCT) | <= 1KB/agent |
| Queued surprise signals | Re-routed during flush | Variable |
| CSO slice allocations | Epoch-boundary rebalancing | Existing protocol |

---

### 8. Emergency Tidal Rollback (ETR) Protocol

#### 8.1 Automated Triggers

Three conditions, any one sufficient to trigger ETR proposal:

**Trigger 1 -- Scheduling Skew:**
```
function detect_scheduling_skew(locus: Locus) -> bool:
  load_ratios = []
  for parcel in locus.parcels:
    avg = mean(agent_load(a) for a in parcel.agents)
    max_l = max(agent_load(a) for a in parcel.agents)
    load_ratios.append(max_l / avg)

  skewed_parcels = count(r > SKEW_THRESHOLD for r in load_ratios)
  -- Trigger: skew > 2x across 3+ parcels for 2 consecutive epochs
  return skewed_parcels >= SKEW_MIN_PARCELS and consecutive_epochs >= SKEW_MIN_EPOCHS
```
Default: `SKEW_THRESHOLD = 2.0`, `SKEW_MIN_PARCELS = 3`, `SKEW_MIN_EPOCHS = 2`.

**Trigger 2 -- Verification Starvation:**
```
function detect_verification_starvation(locus: Locus) -> bool:
  -- Any locus experiences zero verifier sets computed for >1 epoch
  for parcel in locus.parcels:
    if parcel.verifier_sets_computed_last_epoch == 0:
      if parcel.starvation_epochs >= STARVATION_THRESHOLD:
        return true
  return false
```
Default: `STARVATION_THRESHOLD = 1` (epoch).

**Trigger 3 -- Settlement Divergence:**
```
function detect_settlement_divergence(locus: Locus) -> bool:
  -- More than 5% of agents compute different settlements from same inputs
  settlements = collect_settlements(locus, current_epoch())
  canonical = majority_settlement(settlements)
  divergent = count(s != canonical for s in settlements.values())
  return divergent > DIVERGENCE_THRESHOLD * |settlements|
```
Default: `DIVERGENCE_THRESHOLD = 0.05`.

#### 8.2 ETR Proposal and Voting

```
function propose_etr(proposers: Set<AgentId>, trigger: ETRTrigger):
  assert |proposers| >= ETR_MIN_PROPOSERS  -- default 3
  assert all(is_governance_agent(a) for a in proposers)

  proposal = ETRProposal{
    trigger = trigger,
    proposed_by = proposers,
    target_version = get_previous_verified_tidal_version(),
    proposed_epoch = current_epoch(),
    vote_deadline = current_epoch() + ETR_VOTE_WINDOW  -- default 2 epochs
  }

  broadcast_on_governance_channel(proposal)
```

**Voting:**
```
function vote_etr(agent: Agent, proposal: ETRProposal) -> ETRVote:
  assert is_governance_agent(agent)
  return ETRVote{
    agent = agent.id,
    proposal = proposal.id,
    vote = APPROVE | REJECT,
    epoch = current_epoch()
  }
```

**Approval condition:**
```
function check_etr_approval(proposal: ETRProposal) -> bool:
  votes = collect_votes(proposal)
  approve_count = count(v.vote == APPROVE for v in votes)
  total_governance = count_active_governance_agents()
  return approve_count >= ETR_SUPERMAJORITY * total_governance
```
Default: `ETR_SUPERMAJORITY = 0.90`.

#### 8.3 Dedicated Governance Channel

ETR votes propagate on a dedicated governance channel that is architecturally independent of the tidal-scheduled data plane:
- The governance channel uses direct peer-to-peer gossip among governance agents.
- It does NOT depend on hash ring scheduling, predictive delta communication, or parcel assignment.
- Governance agents MUST maintain always-on voting capability as a condition of governance participation.
- Agents failing to vote on 3 consecutive ETR proposals lose governance standing.

#### 8.4 Rollback Procedure

```
function execute_etr(proposal: ETRProposal):
  -- Step 1: Identify rollback target
  target = proposal.target_version  -- previous verified tidal version

  -- Step 2: Schedule activation at next epoch boundary
  next_epoch = current_epoch() + 1

  -- Step 3: At epoch boundary, atomically switch
  -- (This is equivalent to PTP Phase 2 for all parcels simultaneously)
  for locus in affected_loci:
    for parcel in locus.parcels:
      activate_tidal_version(parcel, target, next_epoch)
      rebuild_all_hash_rings(parcel, target)
      invalidate_vrf_cache(parcel)

  -- Step 4: Enter governance hold
  -- The rolled-back version operates while standard G-class process
  -- evaluates a replacement
  governance_hold = GovernanceHold{
    version = target,
    reason = proposal.trigger,
    hold_until = resolved_by_g_class()
  }
```

#### 8.5 Constitutional Protection

The ETR mechanism itself is constitutionally protected:
- Only G-class constitutional consensus (75% supermajority + 72-hour discussion) can modify ETR thresholds or quorum requirements.
- The ETR cannot be weakened by parameter changes through any mechanism other than G-class governance.
- The ETR trigger conditions cannot be disabled.

---

### 9. G-Class Governance Protocol

#### 9.1 Tidal Function Version Management

New tidal function versions follow the G-class governance path:

```
TidalVersionProposal := {
  proposed_version:   TidalFunction
  proposer:           AgentId
  rationale:          AASLRef
  activation_epoch:   uint64      -- earliest activation
  overlap_duration:   uint32      -- epochs where both versions valid
  rollback_conditions: List<Condition>
  discussion_deadline: Timestamp
  vote_deadline:       Timestamp
}
```

#### 9.2 Standard Version Upgrade

1. **Proposal submission:** Any governance agent MAY propose a new tidal version.
2. **Discussion period:** `GOVERNANCE_DISCUSSION_PERIOD` (default 72 hours for HIGH safety class, 24 hours for LOW).
3. **Vote:** 75% supermajority of active governance agents.
4. **Activation:** At the specified epoch boundary, with overlap period.
5. **Overlap:** Both old and new versions are valid during the overlap period. Agents SHOULD switch to the new version. At overlap end, old version is deactivated.

#### 9.3 Constitutional Protection

The following parameters are constitutionally protected and can only be changed via G-class constitutional consensus (75% supermajority + 72-hour discussion):
- Membrane verification depth and admission thresholds
- ETR trigger thresholds and quorum requirements
- Minimum committee size for V-class operations
- G-class supermajority threshold itself

#### 9.4 Interaction with ETR

| Scenario | Path |
|---|---|
| Standard version upgrade | G-class: proposal -> discussion -> 75% vote -> activation |
| Emergency version rollback | ETR: trigger detection -> proposal by 3+ governance agents -> 90% instant vote -> rollback at next epoch |
| Post-rollback replacement | G-class: standard process evaluates replacement while rolled-back version operates |

---

### 10. I-Confluence Bootstrap Specification

#### 10.1 The Cold-Start Problem

Without I-confluence proofs, all operations default to X-class (exclusive), the most expensive agreement mode. The system cannot achieve its O(1) steady-state performance claim until sufficient operations are certified M-class.

#### 10.2 Minimal Obviously-I-Confluent Operation Set

The following operations are I-confluent from first principles and require minimal proof effort. They form the bootstrap set:

| Operation | Why I-Confluent | Proof Complexity |
|---|---|---|
| CRDT G-Counter increment | Monotonic; merge = component-wise max | Trivial |
| CRDT G-Set add | Grow-only; merge = union | Trivial |
| CRDT LWW-Register write | Last-writer-wins with timestamp; merge = max timestamp | Low |
| Append-only log entry | Monotonic append; merge = union + sort | Low |
| Idempotent state update | Re-applying produces same state; merge = any copy | Low |
| Signal emission (SIG) | Signals coexist from different issuers; merge = union + decay | Low |
| Signal reinforcement | Increments count, resets timer; commutative | Low |
| Need/Offer publication | Typed signals; merge = union | Low |
| Monotonic counter increment | Strictly increasing; merge = max | Trivial |
| CSO local spend | Within owned slice; conservation law holds locally | Medium |

These 10 operations MUST be pre-certified with machine-checked proofs before system launch.

#### 10.3 Proof Obligation Format

```
IConfluenceProofObligation := {
  operation_type:   OperationType
  state_type:       StateTypeId
  invariant_set:    Set<Invariant>
  merge_function:   FunctionSignature
  proof_goal:       "forall s1 s2 : State,
                      reachable(s0, s1) -> reachable(s0, s2) ->
                      satisfies(merge(s1, s2), invariant_set)"
  proof_system:     {TLA_PLUS, COQ, F_STAR, IVY}
  proof_artifact:   ArtifactRef
}
```

#### 10.4 Provisional M-Class

Operations with empirical convergence evidence but incomplete formal proofs MAY be classified as provisional M-class:

```
function classify_provisional_m(op_type: OperationType) -> bool:
  -- Requires: simulation evidence of convergence over 1000+ runs
  -- Requires: no observed convergence violations
  -- Requires: monitoring configuration specified

  evidence = get_convergence_evidence(op_type)
  if evidence.runs >= PROVISIONAL_MIN_RUNS and evidence.violations == 0:
    register_classification(op_type, M, provisional=true,
      monitoring=MonitoringConfig{
        check_interval = 1,  -- every epoch
        violation_action = DEMOTE_TO_X,
        alert_threshold = 1  -- single violation triggers demotion
      })
    return true
  return false
```

#### 10.5 X-Class to M-Class Transition Protocol

```
function promote_to_m_class(op_type: OperationType, proof: IConfluenceProof):
  -- Step 1: Proof submission
  assert proof.status == CERTIFIED
  assert proof.verifiers >= PROOF_MIN_VERIFIERS  -- default 3

  -- Step 2: Governance review (lightweight, not full G-class)
  -- 50% of governance agents must acknowledge the proof
  ack_count = await governance_ack(proof, timeout=PROOF_ACK_TIMEOUT)
  assert ack_count >= 0.50 * count_active_governance_agents()

  -- Step 3: Activation at next epoch boundary
  update_classification(op_type, M, provisional=false, proof=proof)

  -- Step 4: Monitor for 10 epochs post-promotion
  install_promotion_monitor(op_type, duration=10)
```

#### 10.6 Cold-Start Procedure

At system genesis:
1. The 10 bootstrap operations (Section 10.2) are pre-certified M-class.
2. All other operations are X-class.
3. The system operates with higher coordination overhead but full correctness.
4. As proofs are produced, operations transition X -> M at epoch boundaries.
5. B-class is available for any CSO-eligible operation immediately (CSO proofs are separate from I-confluence proofs).

**Expected progression:**
- Genesis: ~10 M-class, ~5 B-class, remainder X-class
- Phase 1 end (4 months): ~20 M-class, ~10 B-class
- Phase 2 end (10 months): ~40 M-class, ~15 B-class
- Steady state: >80% of traffic is M-class or B-class

---

### 11. AASL Extension Specification

#### 11.1 New Type Tokens

Four new AASL type tokens extending the 23-token registry to 27 tokens:

| Token | Object | Category |
|---|---|---|
| `TDF` | Tidal Function Definition | Scheduling primitive |
| `TSK` | Task Schedule | Scheduling output |
| `SRP` | Surprise Signal | Communication primitive |
| `STL` | Settlement Boundary | Economic output |

#### 11.2 TDF -- Tidal Function Definition

```
TDF{
  id:tdf.v2.a3f8b1
  version:hash.tidal.a3f8b1
  hash_config:{
    vnode_min:150
    vnode_scale:1000
    epsilon:0.15
    ring_algorithm:bounded_loads_mirrokni2018
  }
  vrf_seeds:{
    rotation:per_epoch
    algorithm:ECVRF_P256_SHA256
  }
  epoch_length:3600
  task_types:[task.verify,task.compute,task.audit,task.governance]
  economic_params:{
    compliance_reward_rate:0.001
    surprise_cost_rate:0.0005
    verification_reward_rate:0.002
    governance_reward_rate:0.003
  }
  activation_epoch:5000
  predecessor:tdf.v1.7c2d4e
  governance_approval:ref.gov.tidal_v2_approval
  sig:ed25519.governance.xyz789
}
```

**Wire format:** Variable-length. Fields are AASL key-value pairs. Mandatory fields: `id`, `version`, `hash_config`, `vrf_seeds`, `epoch_length`, `activation_epoch`, `sig`. All other fields are optional with defaults.

#### 11.3 TSK -- Task Schedule

```
TSK{
  id:tsk.epoch5001.pcl_bio7
  parcel:pcl.bio_prot.hot_set_7
  epoch:5001
  tidal_version:tdf.v2.a3f8b1
  assignments:[
    {agent:ag.042,task_type:task.verify,task_key:hash.tk.1a2b,priority:3}
    {agent:ag.077,task_type:task.compute,task_key:hash.tk.3c4d,priority:2}
  ]
  substitutions:{ag.042:[ag.077,ag.103],ag.077:[ag.042,ag.118]}
  proof:hash.schedule_proof.5001_bio7
}
```

**Wire format:** Variable-length. The `assignments` array is ordered by priority descending. The `proof` field is `H(tidal_version || parcel || epoch || canonical_serialize(assignments))`, enabling any observer to verify the schedule was correctly derived.

#### 11.4 SRP -- Surprise Signal

```
SRP{
  id:srp.ag042.epoch5001.nbr077
  source:ag.042
  target:ag.077
  epoch:5001
  error_vector:[0.15,-0.08,0.22]
  magnitude:0.28
  model_confidence:0.85
  threshold_at_emission:0.20
  hop_count:0
  sig:ed25519.ag042.def456
}
```

**Wire format:** Fixed header (source, target, epoch: 40 bytes) + variable-length error vector (4 bytes per float64 dimension) + fixed trailer (magnitude, confidence, threshold, hop_count, signature: 73 bytes).

**Distinction from SIG:** SRP carries structured predictive-delta semantics (error vector, model confidence, threshold) that SIG's generic `payload` field does not encode. SRP is intra-parcel only; SIG is locus-scope.

#### 11.5 STL -- Settlement Boundary

```
STL{
  id:stl.epoch5001.locus_bio_prot
  locus:loc.biology.proteomics.high
  epoch:5001
  tidal_version:tdf.v2.a3f8b1
  streams:{
    scheduling:{total_reward:45000,total_penalty:-3200}
    verification:{total_reward:28000,total_penalty:-1100}
    communication:{total_bonus:12000}
    governance:{total_reward:5000}
  }
  agent_count:150
  settlement_proof:hash.settlement.5001_bio_prot
  sig:ed25519.settlement_authority.ghi012
}
```

**Wire format:** Variable-length. The `settlement_proof` is `H(canonical_serialize(all_inputs || all_outputs))`, enabling deterministic verification.

#### 11.6 New AACP Message Types

Five new AACP message types for tidal coordination:

| Message | Direction | Payload | Frequency |
|---|---|---|---|
| `TIDAL_SCHEDULE_ANNOUNCE` | Parcel -> Agents | `TSK` | Per epoch |
| `SURPRISE_DELTA` | Agent -> Agent(s) | `SRP` | On surprise |
| `TIDAL_VERSION_PROPOSE` | Governance -> All | `TDF` + rationale | On proposal |
| `ETR_VOTE` | Governance agent -> Governance | `ETRVote` | On ETR trigger |
| `SETTLEMENT_PUBLISH` | Settlement authority -> Locus | `STL` | Per settlement epoch |

#### 11.7 Backward Compatibility

- Existing 23 AASL types are unchanged.
- Existing 18 AACP message types are unchanged.
- Agents that do not understand the new types MUST ignore them (standard AASL forward-compatibility rule).
- The new types use the same AASL framing, encoding, and signature verification as existing types.

---

### 12. Settlement Protocol

#### 12.1 Economic Streams

Settlement is computed deterministically at each settlement epoch (configurable, default = every epoch). Four independent streams contribute to total settlement:

**Stream 1: Scheduling Compliance**
```
scheduling_reward(agent, epoch) =
  COMPLIANCE_RATE * compliance_score(agent, epoch) * agent.stake_weight

compliance_score(agent, epoch) =
  tasks_completed_on_schedule(agent, epoch) / tasks_assigned(agent, epoch)
```

**Stream 2: Verification Duty**
```
verification_reward(agent, epoch) =
  VERIFICATION_RATE * duties_fulfilled(agent, epoch) * quality_score(agent, epoch)

quality_score(agent, epoch) =
  weighted_mean(attestation_scores for agent's attestations in epoch)
```

**Stream 3: Communication Efficiency (Phase 2)**
```
communication_bonus(agent, epoch) =
  COMM_RATE * prediction_accuracy(agent, epoch) * (1 - surprise_ratio(agent, epoch))

surprise_ratio = surprise_signals_sent / total_possible_signals
```

**Stream 4: Governance Participation**
```
governance_reward(agent, epoch) =
  GOV_RATE * votes_cast(agent, epoch) / votes_possible(agent, epoch)
```

#### 12.2 Total Settlement

```
total_delta(agent, epoch) =
  scheduling_reward(agent, epoch)
  + verification_reward(agent, epoch)
  + communication_bonus(agent, epoch)
  + governance_reward(agent, epoch)
  - surprise_cost(agent, epoch)
  - protocol_credit_consumption(agent, epoch)
```

**Determinism invariant:** Two conformant implementations given identical inputs (tidal schedule, event log, economic parameters) MUST produce identical `total_delta` values for every agent. The `settlement_proof` hash enables verification.

#### 12.3 Dispute Resolution

Settlement is deterministic by design. If two agents compute different settlements from the same inputs:
1. Compare `settlement_proof` hashes.
2. The divergent agent has a bug in its settlement computation.
3. The agent MUST re-sync its computation logic from the canonical tidal function version.
4. If divergence persists after re-sync, a Sentinel Edge of type `settlement_divergence` is created and the agent is flagged for review.

---

### 13. Configurable Constants

All tunable parameters with defaults, valid ranges, and justification:

| Parameter | Default | Range | Justification |
|---|---|---|---|
| `VNODE_MIN` | 150 | [50, 500] | Minimum virtual nodes per agent. Below 50, load variance exceeds 1.3x at N=5. |
| `VNODE_SCALE` | 1000 | [500, 5000] | Numerator for V(N) = max(VNODE_MIN, ceil(VNODE_SCALE/N)). |
| `BOUNDED_LOADS_EPSILON` | 0.15 | [0.05, 0.50] | Max load factor above average. Lower = more remapping on churn. |
| `EPOCH_DURATION` | 3600s | [60s, 86400s] | Epoch length. Shorter = more responsive, higher overhead. |
| `CLOCK_TOLERANCE` | 500ms | [100ms, 5000ms] | NTP drift tolerance before timing-fault. |
| `BOUNDARY_WINDOW` | 5s | [1s, 30s] | Epoch boundary detection window. |
| `PARCEL_MIN_AGENTS` | 5 | [3, 20] | Minimum agents per parcel. Below 5, load variance is severe. |
| `CHURN_BUDGET_FRACTION` | 0.20 | [0.05, 0.50] | Max fraction of parcel agents changing per epoch. |
| `COMMITTEE_SIZE` | 7 | [3, 21] | Default verifier committee size. Odd numbers preferred. |
| `DIVERSITY_COOLING_EPOCHS` | 50 | [10, 200] | Epochs ineligible after diversity attribute change. |
| `REVEAL_DELAY` | 1 | [1, 10] | Epochs between commit and reveal of diversity attributes. |
| `THRESHOLD_ADAPT_RATE` | 0.1 | [0.01, 0.5] | Rate at which surprise threshold adapts. |
| `THRESHOLD_TARGET_ACCURACY` | 0.8 | [0.5, 0.95] | Target accuracy for predictive models. |
| `THRESHOLD_MIN` | 0.01 | [0.001, 0.1] | Minimum surprise threshold. |
| `THRESHOLD_MAX` | 1.0 | [0.5, 5.0] | Maximum surprise threshold. |
| `LEARNING_RATE` | 0.01 | [0.001, 0.1] | Online linear regression learning rate. |
| `ACTIVATION_THRESHOLD` | 0.7 | [0.5, 0.9] | Accuracy required to exit TRANSITIONING mode. |
| `SIGNAL_BUDGET` | 50 | [10, 200] | Max outgoing delta messages per agent per epoch. |
| `SIGNAL_EXPIRY_THRESHOLD` | 0.01 | [0.001, 0.1] | Minimum signal strength before expiry. |
| `RADIUS_UNIT` | 0.1 | [0.05, 0.5] | Surprise magnitude per propagation hop. |
| `MAX_RADIUS` | 3 | [1, 10] | Maximum surprise propagation hops. |
| `DAMPING_FACTOR` | 0.5 | [0.1, 0.9] | Exponential damping per hop. |
| `RECONFIG_MIN_INTERVAL` | 10 | [5, 50] | Minimum epochs between parcel reconfigurations. |
| `SKEW_THRESHOLD` | 2.0 | [1.5, 5.0] | Load ratio triggering ETR scheduling skew. |
| `SKEW_MIN_PARCELS` | 3 | [2, 10] | Minimum skewed parcels for ETR trigger. |
| `SKEW_MIN_EPOCHS` | 2 | [1, 5] | Consecutive epochs of skew for ETR trigger. |
| `STARVATION_THRESHOLD` | 1 | [1, 5] | Epochs of zero verification for ETR trigger. |
| `DIVERGENCE_THRESHOLD` | 0.05 | [0.01, 0.20] | Fraction of agents with divergent settlement for ETR. |
| `ETR_MIN_PROPOSERS` | 3 | [1, 10] | Minimum governance agents to propose ETR. |
| `ETR_VOTE_WINDOW` | 2 | [1, 5] | Epochs for ETR vote collection. |
| `ETR_SUPERMAJORITY` | 0.90 | [0.80, 0.95] | Fraction required for ETR approval. |
| `GOVERNANCE_DISCUSSION_PERIOD` | 72h (HIGH) | [24h, 168h] | Discussion period before governance vote. |
| `COMPLIANCE_RATE` | 0.001 | [0.0001, 0.01] | AIC per unit compliance score per unit stake. |
| `VERIFICATION_RATE` | 0.002 | [0.0001, 0.01] | AIC per verification duty fulfilled. |
| `COMM_RATE` | 0.0005 | [0.0001, 0.005] | AIC bonus per unit prediction accuracy. |
| `GOV_RATE` | 0.003 | [0.001, 0.01] | AIC per governance vote cast. |
| `PROMOTION_THRESHOLD` | 3 | [1, 10] | Consecutive surprise epochs before anomaly promotion. |
| `EXOGENOUS_WEIGHT` | 0.01 | [0.001, 0.1] | Weight for incorporating locus-scope signals into models. |
| `PROVISIONAL_MIN_RUNS` | 1000 | [100, 10000] | Minimum simulation runs for provisional M-class. |
| `PROOF_MIN_VERIFIERS` | 3 | [2, 10] | Minimum verifiers for I-confluence proof certification. |
| `PROOF_ACK_TIMEOUT` | 48h | [12h, 168h] | Governance acknowledgment timeout for proof promotion. |

---

### 14. Conformance Requirements

#### 14.1 MUST Requirements

A conformant implementation MUST:

1. Implement bounded-loads consistent hashing per Algorithm 4.2 with configurable epsilon.
2. Use ECVRF per RFC 9381 on curve P-256 for all VRF computations.
3. Implement the commit-reveal protocol (Section 5.2) for diversity attribute registration.
4. Implement pre-stratified diversity pools (Section 5.3) for verifier selection.
5. Produce identical scheduling outputs for identical inputs (determinism invariant).
6. Produce identical settlement outputs for identical inputs (determinism invariant).
7. Implement the three-phase Parcel Transition Protocol (Section 7).
8. Implement the ETR protocol with all three automated triggers (Section 8).
9. Enforce the 20% maximum concurrent reconfiguration constraint.
10. Enforce the 50-epoch cooling period for diversity attribute changes.
11. Support all four new AASL types (TDF, TSK, SRP, STL) and five new AACP messages.
12. Classify all operations via the classification procedure in Section 3.1.
13. Default unproven operations to X-class.
14. Implement the dedicated governance channel independent of the tidal data plane.
15. Enforce constitutional protection of membrane parameters and ETR thresholds.

#### 14.2 SHOULD Requirements

A conformant implementation SHOULD:

1. Implement predictive delta communication (Section 6.1) for intra-parcel bandwidth reduction.
2. Implement Predictive Context Transfer for parcel boundary crossings (Section 6.3).
3. Implement trend signals for gradient-based locus-scope awareness (Section 6.2).
4. Support provisional M-class classification with monitoring (Section 10.4).
5. Implement the cascade limiter for delta message storms (Section 6.1).
6. Implement the interaction between surprise threshold and SLV threshold (auto-loosen surprise threshold when SLV is high).
7. Pre-certify the 10 bootstrap operations (Section 10.2) before launch.

#### 14.3 MAY Requirements

A conformant implementation MAY:

1. Use alternative hash functions (SHA-3, BLAKE3) if collision resistance is equivalent.
2. Implement additional diversity dimensions beyond the four specified.
3. Use alternative proof systems beyond TLA+/Coq/F*/Ivy for I-confluence proofs.
4. Adjust configurable constants within the specified ranges without governance approval (governance approval required for changes outside ranges).
5. Implement additional economic streams beyond the four specified.

#### 14.4 Test Vectors

**Test Vector 1: Hash Ring Position**
```
Input:
  agent_id = bytes("agent_001")
  task_type = bytes("task.verify")
  vnode_index = uint32(0)

Expected:
  position = H("agent_001" || "task.verify" || 0x00000000) mod 2^256
  -- Implementors: compute SHA-256 of the concatenated bytes and reduce mod 2^256
```

**Test Vector 2: VRF Output**
```
Input:
  privkey = <test ECVRF P-256 private key>
  alpha = H(claim_hash || epoch_bytes || vrf_seed)

Expected:
  -- Per RFC 9381 Section 5.1, ECVRF-P256-SHA256-TAI
  -- Implementors: verify against RFC 9381 test vectors
```

**Test Vector 3: Bounded-Loads Assignment**
```
Input:
  5 agents, 150 virtual nodes each, epsilon = 0.15
  100 random task keys

Expected:
  max_load / avg_load <= 1.15
  avg_load = 20 (100 keys / 5 agents)
  max_load <= ceil(1.15 * 20) = 23
```

**Test Vector 4: Diversity Commitment**
```
Input:
  salt = 0x0123456789abcdef0123456789abcdef
  training_lineage = H("openai_gpt4_2024")
  methodology = "replication"
  temporal_bucket = "stable_6mo_plus"
  region = "us_east"

Expected:
  commitment = H(salt || training_lineage || "replication" ||
                  "stable_6mo_plus" || "us_east")
  -- Implementors: compute SHA-256 of the concatenated bytes
```

**Test Vector 5: Signal Decay**
```
Input:
  confidence = 0.85
  reinforced_at = 0 (epoch start)
  decay_tau = 3600 (seconds)
  t = 1800 (30 minutes after reinforcement)

Expected:
  strength = 0.85 * exp(-1800/3600)
           = 0.85 * exp(-0.5)
           = 0.85 * 0.6065...
           = 0.5155...
```

**Test Vector 6: Adaptive Threshold**
```
Input:
  threshold(t) = 0.20
  accuracy(t) = 0.90
  THRESHOLD_ADAPT_RATE = 0.1
  THRESHOLD_TARGET_ACCURACY = 0.8

Expected:
  threshold(t+1) = 0.20 * (1 + 0.1 * (0.90 - 0.80))
                 = 0.20 * 1.01
                 = 0.202
  -- Threshold tightens because accuracy exceeds target
```

---

*End of Technical Specification*

*This specification is a DESIGN-stage document. All algorithms, protocols, and parameters are subject to revision based on simulation results from the gated experiments defined in the Feasibility Verdict (GATE-1 through GATE-3) and the Science Assessment's recommended experiments.*
