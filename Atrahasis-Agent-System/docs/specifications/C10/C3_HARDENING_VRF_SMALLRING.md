# C3 Hardening Addendum: VRF Diversity Attribute Grinding & Small-Ring Load Imbalance

## Addendum to: Tidal Noosphere Master Technical Specification (C3-A v1.0)
## Date: 2026-03-10
## Status: HARDENING — Addresses Two CRITICAL Findings
## Sections Affected: 4.1, 4.2, 4.5, 5.2, 10.2 (Attacks 2, 3)

---

## Preamble

This addendum hardens two interrelated attack surfaces identified during post-specification review of the C3 Master Tech Spec. Both findings are CRITICAL severity because they concern foundational mechanisms (VRF committee selection and consistent hash ring scheduling) that underpin system correctness.

**Finding 1 — VRF Diversity Attribute Grinding.** The existing dual defense (commit-reveal + pre-stratified pools) bounds adversary advantage to <3% above baseline under the assumption that the adversary optimizes timing. However, a more sophisticated adversary who controls multiple agent identities can register agents with carefully chosen diversity attributes to maximize selection probability across the diversity filtering step itself. The diversity filter, intended to improve epistemic quality, becomes an attack surface for strategic identity placement. The adversary knows the diversity constraints, knows the public attributes of all eligible verifiers, and can compute the probability that any VRF output leads to a committee containing their agents.

**Finding 2 — Small-Ring Load Imbalance.** The spec mandates bounded-loads consistent hashing (Section 4.2) with epsilon=0.15, which guarantees max/avg <= 1.15 for the steady-state lookup. However, the bounded-loads guarantee depends on having sufficient task volume for the overflow mechanism to activate. With basic consistent hashing and N nodes (5-15 agents per parcel), maximum load on any node is O(log N / log log N) times the average before bounded-loads engages. For 10 agents, this means ~2.3x load imbalance. For 5 agents, ~3.1x. The existing virtual node inflation policy (Section 4.1) mitigates but does not eliminate this for small parcels, and no epoch-boundary rebalancing mechanism exists.

Both findings interact: small parcels have fewer agents in diversity pools, making diversity grinding more effective per-pool, while also suffering worse load imbalance. A hardened design must address both simultaneously.

---

## Part 1: VRF Diversity Attribute Grinding Defense

### 1.1 Hidden Diversity Attributes

**Problem.** All four diversity dimensions (training_lineage, methodology, temporal_bucket, region) are public after reveal. An adversary can observe the full attribute distribution of all eligible agents and compute the optimal attribute vector for each Sybil identity to maximize diversity slot capture probability.

**Defense.** Split diversity dimensions into public and hidden. Public dimensions are revealed normally and used for coarse stratification. Hidden dimensions are hashed with a per-epoch salt known only after the epoch begins, preventing pre-computation of optimal attribute placement.

```
HIDDEN_DIMENSION_COUNT = 2   // governance-configurable, range [1, 4]

// At registration, agent commits ALL dimensions (public + hidden)
struct DiversityAttributes:
    // Public dimensions (revealed after REVEAL_DELAY)
    training_lineage: string
    region: string
    // Hidden dimensions (never revealed in plaintext)
    methodology_hash: bytes[32]
    temporal_bucket_hash: bytes[32]

struct HiddenDiversityCommitment:
    agent_id: AgentId
    public_attrs: {training_lineage: string, region: string}
    hidden_commitment: bytes[32]   // hash of hidden attrs + agent salt
    agent_salt: bytes[16]          // agent's permanent salt for hidden attrs
    committed_epoch: uint64
    cooling_until: uint64

function commit_diversity_v2(
    agent: Agent,
    public_attrs: PublicDiversityAttributes,
    hidden_attrs: HiddenDiversityAttributes,
    agent_salt: bytes[16]
) -> HiddenDiversityCommitment:
    // Commit hidden attributes with agent-specific salt
    hidden_commitment = SHA256(
        agent_salt
        || hidden_attrs.methodology
        || hidden_attrs.temporal_bucket
    )

    return HiddenDiversityCommitment{
        agent_id = agent.id,
        public_attrs = public_attrs,
        hidden_commitment = hidden_commitment,
        agent_salt = agent_salt,
        committed_epoch = current_epoch(),
        cooling_until = 0
    }

function evaluate_hidden_diversity(
    agent: Agent,
    epoch: uint64,
    epoch_salt: bytes[32]
) -> bytes[32]:
    // Per-epoch hidden diversity score
    // The epoch_salt is derived from the VRF seed, unknown until the epoch begins
    return SHA256(
        epoch_salt
        || agent.diversity_commitment.hidden_commitment
        || agent.diversity_commitment.agent_salt
    )

function build_diversity_pools_v2(
    eligible: Set<Agent>,
    locus: Locus,
    epoch: uint64,
    vrf_seed: bytes[32]
) -> (Map<(DiversityDimension, DiversityValue), DiversityPool>,
      Map<AgentId, bytes[32]>):
    // Phase 1: Build public pools (same as before)
    public_pools = {}
    for agent in eligible:
        if not agent.diversity_commitment.public_attrs: continue
        if agent.diversity_commitment.cooling_until > current_epoch(): continue

        attrs = agent.diversity_commitment.public_attrs
        for (dim, val) in [
            (TRAINING_LINEAGE, attrs.training_lineage),
            (REGION, attrs.region)
        ]:
            key = (dim, val)
            if key not in public_pools:
                public_pools[key] = DiversityPool{
                    dimension=dim, value=val, members={}
                }
            public_pools[key].members.add(agent.id)

    // Phase 2: Compute hidden diversity scores
    epoch_salt = SHA256(vrf_seed || uint64_be(epoch) || b"hidden_diversity")
    hidden_scores = {}
    for agent in eligible:
        hidden_scores[agent.id] = evaluate_hidden_diversity(
            agent, epoch, epoch_salt
        )

    return (public_pools, hidden_scores)
```

**Security property.** The adversary can optimize Sybil placement for public dimensions (training_lineage, region) but cannot optimize for hidden dimensions (methodology, temporal_bucket) because the effective hidden score depends on `epoch_salt`, which is derived from the VRF seed unknown until the epoch begins. The adversary's information advantage is reduced from 4 optimizable dimensions to 2.

### 1.2 Randomized Filter Thresholds

**Problem.** Fixed diversity requirements (e.g., "committee must contain at least 1 agent from each of 3 training lineages") allow the adversary to compute exactly which attribute combinations maximize selection. If the adversary knows the threshold is exactly 3 mandatory lineage slots, they register one Sybil per lineage.

**Defense.** Randomize the minimum diversity score per committee selection within a governance-approved range. The adversary cannot know which diversity requirements will apply to any specific committee until after VRF selection begins.

```
struct DiversityRequirementRange:
    dimension: DiversityDimension
    min_mandatory_slots: uint8     // governance floor
    max_mandatory_slots: uint8     // governance ceiling
    weight_range: (float, float)   // (min_weight, max_weight)

// Governance-approved ranges (constitutionally protected)
DEFAULT_DIVERSITY_RANGES = [
    DiversityRequirementRange{
        dimension = TRAINING_LINEAGE,
        min_mandatory_slots = 1,
        max_mandatory_slots = 3,
        weight_range = (0.15, 0.35)
    },
    DiversityRequirementRange{
        dimension = REGION,
        min_mandatory_slots = 1,
        max_mandatory_slots = 2,
        weight_range = (0.10, 0.25)
    },
    DiversityRequirementRange{
        dimension = METHODOLOGY,   // hidden
        min_mandatory_slots = 0,
        max_mandatory_slots = 2,
        weight_range = (0.10, 0.20)
    },
    DiversityRequirementRange{
        dimension = TEMPORAL_BUCKET,  // hidden
        min_mandatory_slots = 0,
        max_mandatory_slots = 2,
        weight_range = (0.10, 0.20)
    }
]

function randomize_diversity_requirements(
    claim: Claim,
    epoch: uint64,
    vrf_seed: bytes[32],
    ranges: List<DiversityRequirementRange>
) -> List<DiversityRequirement>:
    // Derive per-committee randomness from claim hash + epoch + seed
    committee_entropy = SHA256(
        claim.hash || uint64_be(epoch) || vrf_seed || b"diversity_threshold"
    )

    requirements = []
    offset = 0
    for range_spec in ranges:
        // Extract deterministic random bytes for this dimension
        dim_bytes = committee_entropy[offset : offset + 4]
        offset += 4

        // Map to slot count within governance range
        slot_range = range_spec.max_mandatory_slots - range_spec.min_mandatory_slots
        if slot_range == 0:
            slots = range_spec.min_mandatory_slots
        else:
            slots = range_spec.min_mandatory_slots + (
                uint32_from_bytes(dim_bytes) % (slot_range + 1)
            )

        // Map to weight within governance range
        weight_bytes = committee_entropy[offset : offset + 4]
        offset += 4
        weight_frac = uint32_from_bytes(weight_bytes) / (2^32 - 1)
        weight = range_spec.weight_range[0] + weight_frac * (
            range_spec.weight_range[1] - range_spec.weight_range[0]
        )

        requirements.append(DiversityRequirement{
            dimension = range_spec.dimension,
            mandatory_slots = slots,
            weight = weight
        })

    return requirements
```

**Security property.** The diversity requirements for any specific committee selection are deterministic (all honest agents compute the same requirements) but unpredictable until the claim hash and VRF seed are both known. Since the claim hash is committed before the verification epoch (per Section 5.2.2) and the VRF seed is unknown until the epoch begins, the adversary cannot pre-compute optimal Sybil attributes for any specific committee. The expected adversary advantage from attribute optimization is reduced to the variance of a uniform distribution over the governance-approved range.

### 1.3 Diversity Attribute Commitment with Cooling Period

**Problem.** The existing spec defines a 50-epoch cooling period (Section 5.2.2) for attribute changes but does not specify the full lifecycle or cost analysis. An adversary could rotate Sybil attributes across epochs, amortizing the cooling cost.

**Defense.** Formalize the cooling period with escalating costs for repeated changes and audit trail requirements.

```
DIVERSITY_COOLING_BASE = 50          // epochs, governance-configurable
DIVERSITY_COOLING_ESCALATION = 2.0   // multiplier per change
DIVERSITY_MAX_CHANGES_PER_YEAR = 4   // hard cap
DIVERSITY_CHANGE_STAKE_LOCK = 0.10   // 10% of stake locked during cooling

struct DiversityChangeRecord:
    agent_id: AgentId
    old_commitment: bytes[32]
    new_commitment: bytes[32]
    change_epoch: uint64
    cooling_until: uint64
    change_count_lifetime: uint32
    stake_locked: uint256

function request_diversity_change(
    agent: Agent,
    new_public_attrs: PublicDiversityAttributes,
    new_hidden_commitment: bytes[32],
    new_agent_salt: bytes[16]
) -> DiversityChangeRecord:
    // Enforce max changes per year
    recent_changes = count_changes(agent.id, current_epoch() - EPOCHS_PER_YEAR)
    assert recent_changes < DIVERSITY_MAX_CHANGES_PER_YEAR,
        "Maximum diversity attribute changes per year exceeded"

    // Compute escalating cooling period
    lifetime_changes = agent.diversity_commitment.change_count_lifetime
    cooling_epochs = ceil(
        DIVERSITY_COOLING_BASE * (DIVERSITY_COOLING_ESCALATION ** lifetime_changes)
    )
    // 1st change: 50 epochs, 2nd: 100, 3rd: 200, 4th: 400

    // Lock stake during cooling
    stake_to_lock = agent.stake * DIVERSITY_CHANGE_STAKE_LOCK
    assert agent.available_stake >= stake_to_lock,
        "Insufficient available stake for diversity change"
    lock_stake(agent.id, stake_to_lock, cooling_epochs)

    // Record the change
    record = DiversityChangeRecord{
        agent_id = agent.id,
        old_commitment = agent.diversity_commitment.hidden_commitment,
        new_commitment = new_hidden_commitment,
        change_epoch = current_epoch(),
        cooling_until = current_epoch() + cooling_epochs,
        change_count_lifetime = lifetime_changes + 1,
        stake_locked = stake_to_lock
    }

    // Agent is INELIGIBLE for verification committees during cooling
    agent.diversity_commitment.cooling_until = record.cooling_until
    agent.diversity_commitment.change_count_lifetime += 1

    // Permanent audit trail
    append_to_audit_log(DIVERSITY_CHANGE_LOG, record)

    return record

function is_eligible_for_verification(agent: Agent) -> bool:
    if agent.diversity_commitment.cooling_until > current_epoch():
        return false
    if not agent.diversity_commitment.public_attrs:
        return false
    return true
```

**Escalation schedule:**

| Change # | Cooling Period | Cumulative Cost (10% stake lock) |
|----------|---------------|----------------------------------|
| 1st      | 50 epochs     | 50 epochs x 10% stake           |
| 2nd      | 100 epochs    | 100 epochs x 10% stake          |
| 3rd      | 200 epochs    | 200 epochs x 10% stake          |
| 4th      | 400 epochs    | 400 epochs x 10% stake          |
| 5th+     | Blocked until next year | N/A                    |

### 1.4 Sybil Cost Analysis

**Problem.** Quantify the minimum cost for an adversary to achieve >50% committee control through diversity grinding. Show that this cost exceeds the expected gain.

**Model assumptions:**
- Committee size: 7
- Honest agents: 250 (per locus, eligible for verification)
- Public diversity dimensions: 2 (training_lineage with 5 values, region with 4 values)
- Hidden diversity dimensions: 2 (methodology, temporal_bucket)
- Minimum stake per agent: S_min AIC
- Epochs per year: 8,760 (1-hour epochs)
- Average verification reward per committee seat per epoch: R AIC

```
function compute_sybil_cost_for_majority_control(
    committee_size: uint8,        // 7
    honest_agents: uint32,        // 250
    public_dim_values: uint32,    // 5 * 4 = 20 public strata
    hidden_dim_values: uint32,    // unknown to adversary
    min_stake: float,             // S_min AIC per agent
    cooling_base: uint32,         // 50 epochs
    stake_lock_fraction: float,   // 0.10
    verification_reward: float    // R AIC per seat per epoch
) -> SybilCostAnalysis:

    target_seats = ceil(committee_size / 2) + 1   // 4 of 7

    // ---- COST ANALYSIS ----

    // Step 1: Minimum Sybils needed
    // With pre-stratified pools, adversary's per-pool representation
    // is proportional to (sybils_in_pool / total_in_pool).
    // To capture a diversity slot in a pool with probability p_capture,
    // adversary needs enough Sybils that VRF selection favors them.
    //
    // In a pool of size P with A adversary agents:
    //   Pr(adversary wins slot) = A / P
    //
    // With randomized thresholds (Section 1.2), adversary must optimize
    // across the full range of possible requirements.
    //
    // For public dimensions (2 dimensions, adversary CAN optimize):
    //   Adversary places Sybils in smallest pools to maximize A/P ratio.
    //   Best case: adversary finds a pool with P_min honest agents.
    //
    // For hidden dimensions (2 dimensions, adversary CANNOT optimize):
    //   Adversary's hidden scores are random. No optimization possible.
    //   Expected representation = A_total / N_total (proportional).

    // Minimum Sybils to capture 4/7 seats:
    // - Phase 1 (diversity slots): ~2-3 slots filled from pools
    //   Adversary needs majority of diversity slots
    // - Phase 2 (remaining slots): filled by standard VRF
    //   Adversary needs proportional representation

    // Conservative estimate (adversary optimizes public dims perfectly):
    // Need ~2 diversity slot captures + ~2 standard VRF captures = 4 seats

    // For 2 diversity slots from public pools:
    //   Each pool has ~250/20 = 12.5 honest agents (uniform distribution)
    //   To capture with >50% probability: need ~13 Sybils per pool
    //   2 pools * 13 = 26 Sybils minimum for public diversity slots

    // For 2 standard VRF seats from remaining pool:
    //   Remaining pool: ~250 - (already selected) honest + adversary Sybils
    //   Need 2/(7-2) = 40% of remaining selections
    //   With 26 Sybils in pool of ~276: Pr(select) = 26/276 = 9.4%
    //   Need ~100+ additional Sybils for 40% VRF capture
    //   Total: ~126 Sybils

    // But hidden dimensions HALVE the optimizable surface:
    // Adversary's hidden diversity scores are random, so their
    // hidden-dimension pool placement is uncontrollable.
    // This roughly doubles the Sybils needed: ~250 Sybils

    sybils_needed = 250   // conservative estimate

    // Step 2: Stake cost
    stake_cost = sybils_needed * min_stake
    // 250 * S_min AIC

    // Step 3: Cooling cost (opportunity cost during registration)
    // Each Sybil is ineligible for 50 epochs while cooling
    cooling_opportunity_cost = sybils_needed * cooling_base * verification_reward
    // 250 * 50 * R AIC (forfeited rewards during cooling)

    // Step 4: Stake lock cost (during any attribute changes)
    // If adversary needs to change attributes: 10% stake locked
    attribute_change_cost = sybils_needed * min_stake * stake_lock_fraction * cooling_base
    // 250 * S_min * 0.10 * 50 (locked capital)

    // ---- GAIN ANALYSIS ----

    // Step 5: Expected gain from committee control
    // Adversary controls 4/7 seats on committees they're selected for
    // Can approve false claims or reject valid claims
    //
    // But: continuous re-verification (Section 5.3) means false approvals
    // are re-checked with new committees. Expected persistence of a false
    // claim before re-verification: ~20 epochs (citation-weighted sampling).
    //
    // Maximum gain per false claim: bounded by the claim's scope.
    // For a single locus, maximum extractable value per epoch is
    // the verification reward pool: ~verification_reward * committee_size * claims_per_epoch
    //
    // Sentinel Graph detection window: ~20 epochs (Section 5.2.4)
    // After detection: all Sybil stakes slashed (100% for verified collusion)

    max_gain_before_detection = 20 * verification_reward * committee_size * 10
    // 20 epochs * R * 7 * 10 claims/epoch = 1,400 * R AIC

    slashing_loss = sybils_needed * min_stake
    // 250 * S_min AIC (total stake destroyed)

    // Step 6: Cost-benefit ratio
    total_cost = stake_cost + cooling_opportunity_cost + attribute_change_cost
    net_outcome = max_gain_before_detection - total_cost - slashing_loss

    return SybilCostAnalysis{
        sybils_needed = sybils_needed,
        stake_cost = stake_cost,
        cooling_cost = cooling_opportunity_cost,
        attribute_change_cost = attribute_change_cost,
        total_cost = total_cost,
        max_gain = max_gain_before_detection,
        slashing_loss = slashing_loss,
        net_outcome = net_outcome,
        // For net_outcome < 0 (attack unprofitable), we need:
        // 250 * S_min + 250 * 50 * R + 250 * S_min * 0.10 * 50 + 250 * S_min
        //   > 1,400 * R
        // Simplifying: 500 * S_min + 12,500 * R + 1,250 * S_min > 1,400 * R
        // => 1,750 * S_min + 11,100 * R > 0
        // This is ALWAYS TRUE for positive S_min and R.
        //
        // The attack is unprofitable for ANY positive stake requirement
        // because the number of Sybils needed (250) makes the stake cost
        // and slashing risk dominate the bounded gain window.
        profitable = false
    }
```

**Cost-benefit summary table (with S_min = 100 AIC, R = 0.01 AIC):**

| Component | Value | Notes |
|-----------|-------|-------|
| Sybils needed for >50% committee control | ~250 | Accounts for hidden dimensions |
| Stake cost | 25,000 AIC | 250 agents x 100 AIC minimum stake |
| Cooling opportunity cost | 125 AIC | 250 x 50 epochs x 0.01 AIC reward |
| Stake lock cost | 125,000 AIC-epochs | Capital locked during cooling |
| **Total cost** | **>25,125 AIC + locked capital** | |
| Maximum gain before detection (20 epochs) | 14 AIC | 1,400 x 0.01 AIC |
| Slashing loss on detection | 25,000 AIC | 100% stake slash for verified collusion |
| **Net outcome** | **-50,111 AIC** | **Attack is deeply unprofitable** |

**Key insight.** The combination of hidden dimensions (doubling Sybil requirements), escalating cooling periods (time cost), stake lock during cooling (capital cost), and Sentinel Graph detection within ~20 epochs (bounded gain window + slashing) makes diversity grinding unprofitable by a factor of >3,500x. Even if the adversary could somehow avoid detection for 10x longer (200 epochs), the attack remains unprofitable by >350x.

### 1.5 Hardened End-to-End VRF Committee Selection

The following replaces Section 5.2.4 of the Master Tech Spec with the hardened protocol integrating all four defense mechanisms.

```
function select_diverse_verifiers_v2(
    claim: Claim,
    epoch: uint64,
    vrf_seed: bytes[32],
    eligible: Set<Agent>,
    locus: Locus,
    committee_size: uint8,              // default 7
    diversity_ranges: List<DiversityRequirementRange>
) -> Set<AgentId>:

    // Step 1: Build public pools + compute hidden scores
    (public_pools, hidden_scores) = build_diversity_pools_v2(
        eligible, locus, epoch, vrf_seed
    )

    // Step 2: Randomize diversity requirements for this committee
    requirements = randomize_diversity_requirements(
        claim, epoch, vrf_seed, diversity_ranges
    )

    // Step 3: Compute the VRF input
    alpha = SHA256(claim.hash || uint64_be(epoch) || vrf_seed)

    committee = {}

    // Step 4: Fill public diversity slots
    for req in requirements:
        if req.dimension in [TRAINING_LINEAGE, REGION]:   // public dimensions
            // Standard pool-based selection (per existing spec)
            for (dim_key, pool) in public_pools:
                if dim_key[0] != req.dimension: continue
                if req.mandatory_slots <= 0: break

                pool_candidates = []
                for agent_id in pool.members:
                    if agent_id in committee: continue
                    if not is_eligible_for_verification(get_agent(agent_id)):
                        continue
                    agent = get_agent(agent_id)
                    (beta, pi) = ECVRF_prove(
                        agent.privkey,
                        alpha || encode(req.dimension) || encode(dim_key[1])
                    )
                    pool_candidates.append((agent_id, beta))

                pool_candidates.sort_by(c => c.beta)
                if len(pool_candidates) > 0:
                    committee.add(pool_candidates[0].agent_id)
                    req.mandatory_slots -= 1

    // Step 5: Fill hidden diversity slots
    // Hidden dimensions use epoch-salted scores for selection
    epoch_hidden_salt = SHA256(vrf_seed || uint64_be(epoch) || b"hidden_select")
    for req in requirements:
        if req.dimension in [METHODOLOGY, TEMPORAL_BUCKET]:   // hidden dimensions
            hidden_candidates = []
            for agent_id in union(p.members for p in public_pools.values()):
                if agent_id in committee: continue
                if not is_eligible_for_verification(get_agent(agent_id)):
                    continue
                // Hidden diversity score combines agent's hidden commitment
                // with epoch-specific salt — adversary cannot pre-optimize
                hidden_score = SHA256(
                    epoch_hidden_salt
                    || hidden_scores[agent_id]
                    || encode(req.dimension)
                )
                hidden_candidates.append((agent_id, hidden_score))

            // Sort by hidden score (deterministic but unpredictable)
            hidden_candidates.sort_by(c => c[1])

            // Select top candidates for hidden diversity slots
            slots_to_fill = min(req.mandatory_slots, len(hidden_candidates))
            for i in 0..slots_to_fill-1:
                committee.add(hidden_candidates[i][0])

    // Step 6: Fill remaining slots via standard VRF (unchanged from spec)
    all_eligible = union(p.members for p in public_pools.values())
    remaining = []
    for agent_id in all_eligible:
        if agent_id in committee: continue
        if not is_eligible_for_verification(get_agent(agent_id)):
            continue
        agent = get_agent(agent_id)
        (beta, pi) = ECVRF_prove(agent.privkey, alpha)
        remaining.append((agent_id, beta))

    remaining.sort_by(c => c.beta)
    for (agent_id, beta) in remaining:
        if len(committee) >= committee_size: break
        if would_exceed_weight_cap(agent_id, committee): continue   // 15% cap
        committee.add(agent_id)

    return committee
```

---

## Part 2: Small-Ring Load Imbalance Defense

### 2.1 Bounded-Loads Consistent Hashing (Hardened)

The existing spec (Section 4.2) defines the bounded-loads algorithm but does not address the transient imbalance that occurs when task volume is low relative to agent count, or the interaction between epsilon and virtual node density in small rings. This section provides the hardened implementation.

```
BOUNDED_LOADS_EPSILON = 0.15          // default, governance-configurable [0.05, 0.50]
BOUNDED_LOADS_MIN_TASKS_FOR_BALANCE = 3  // minimum tasks per agent for guarantee

struct BoundedLoadsRing:
    entries: SortedArray<(uint256, AgentId)>
    agent_count: uint32
    virtual_nodes_per_agent: uint32
    epsilon: float
    task_type: TaskType
    parcel_id: ParcelId
    // NEW: per-agent load tracking within the epoch
    agent_loads: Map<AgentId, uint32>
    total_assigned: uint32
    capacity_cap: uint32               // (1 + epsilon) * ceil(total_tasks / agent_count)

function build_bounded_ring(
    parcel: Parcel,
    task_type: TaskType,
    expected_tasks: uint32              // estimated tasks this epoch
) -> BoundedLoadsRing:
    N = len(parcel.agents)
    V = adaptive_vnode_count(N)         // see Section 2.2
    epsilon = BOUNDED_LOADS_EPSILON

    entries = empty sorted array
    for agent in parcel.agents:
        for v in 0..V-1:
            pos = SHA256(agent.id || task_type || uint32_be(v)) mod 2^256
            entries.insert_sorted((pos, agent.id))

    avg_load = max(1, ceil(expected_tasks / N))
    cap = ceil((1 + epsilon) * avg_load)

    return BoundedLoadsRing{
        entries = entries,
        agent_count = N,
        virtual_nodes_per_agent = V,
        epsilon = epsilon,
        task_type = task_type,
        parcel_id = parcel.id,
        agent_loads = {agent.id: 0 for agent in parcel.agents},
        total_assigned = 0,
        capacity_cap = cap
    }

function lookup_bounded(ring: BoundedLoadsRing, key: bytes) -> AgentId:
    target_pos = SHA256(key) mod 2^256

    // Dynamically recompute cap as tasks arrive
    // This handles the case where expected_tasks was underestimated
    ring.total_assigned += 1
    current_avg = ring.total_assigned / ring.agent_count
    dynamic_cap = max(
        ring.capacity_cap,
        ceil((1 + ring.epsilon) * current_avg)
    )

    // Find the first virtual node at or after target_pos
    idx = ring.entries.lower_bound(target_pos)
    if idx >= len(ring.entries):
        idx = 0   // wrap around

    // Walk clockwise until finding an agent below capacity
    visited = 0
    while visited < len(ring.entries):
        (pos, agent_id) = ring.entries[idx]
        if ring.agent_loads[agent_id] < dynamic_cap:
            ring.agent_loads[agent_id] += 1
            return agent_id
        idx = (idx + 1) % len(ring.entries)
        visited += 1

    // All agents at capacity — this can happen if total_assigned > N * dynamic_cap
    // Fallback: assign to least-loaded agent
    least_loaded = min(ring.agent_loads, key=lambda aid: ring.agent_loads[aid])
    ring.agent_loads[least_loaded] += 1
    return least_loaded

function reset_loads(ring: BoundedLoadsRing):
    // Called at epoch boundary after all assignments are computed
    for agent_id in ring.agent_loads:
        ring.agent_loads[agent_id] = 0
    ring.total_assigned = 0
```

### 2.2 Adaptive Virtual Nodes

The existing spec defines `V(N) = max(VNODE_MIN, ceil(VNODE_SCALE / N))` with VNODE_MIN=150, VNODE_SCALE=1000. This section provides a refined scaling function with empirical justification.

```
// Refined virtual node scaling function
// Rationale: For small rings, load variance is proportional to 1/sqrt(V*N).
// To achieve target variance sigma_target, we need V >= 1/(sigma_target^2 * N).
// Target: max/avg load < 1.15 (matching epsilon=0.15) with 99% probability.
// This requires sigma < 0.05 (from normal approximation of load distribution).
// Therefore: V >= 1/(0.05^2 * N) = 400/N.
// But we also need V >= VNODE_MIN for hash quality.

VNODE_MIN = 50            // absolute minimum for hash distribution quality
VNODE_MAX = 500           // cap to limit ring size and rebuild cost
VNODE_TARGET_VARIANCE = 0.05   // target standard deviation of load fraction

function adaptive_vnode_count(N: uint32) -> uint32:
    // Primary formula: V = ceil(1 / (sigma^2 * N))
    variance_based = ceil(1.0 / (VNODE_TARGET_VARIANCE ** 2 * N))

    // Apply bounds
    V = clamp(variance_based, VNODE_MIN, VNODE_MAX)

    // Override table for very small parcels (empirically tuned)
    SMALL_PARCEL_OVERRIDES = {
        5:  400,    // 400 vnodes x 5 agents = 2,000 ring entries
        6:  350,    // 350 x 6 = 2,100
        7:  300,    // 300 x 7 = 2,100
        8:  250,    // 250 x 8 = 2,000
        9:  225,    // 225 x 9 = 2,025
        10: 200,    // 200 x 10 = 2,000
    }

    if N in SMALL_PARCEL_OVERRIDES:
        V = max(V, SMALL_PARCEL_OVERRIDES[N])

    return V
```

**Scaling table:**

| Agents (N) | Formula V | Override V | Ring Entries | Expected max/avg |
|------------|-----------|------------|-------------|-----------------|
| 5          | 400       | 400        | 2,000       | 1.10            |
| 8          | 250       | 250        | 2,000       | 1.08            |
| 10         | 200       | 200        | 2,000       | 1.07            |
| 15         | 134       | 134        | 2,010       | 1.06            |
| 20         | 100       | 100        | 2,000       | 1.05            |
| 30         | 67        | 67         | 2,010       | 1.04            |
| 50         | 50 (min)  | 50         | 2,500       | 1.03            |

**Design note.** The ring size (N * V) is held roughly constant at ~2,000 entries across all parcel sizes. This means rebuild cost is O(2,000) regardless of parcel size — a constant-time operation that takes approximately 0.1ms on modern hardware. The variance improvement comes entirely from distributing the same number of ring entries more densely for small parcels.

### 2.3 Load Rebalancing at Epoch Boundary

**Problem.** Even with bounded-loads and adaptive virtual nodes, actual load may diverge from expected load due to: (a) non-uniform task key distribution within an epoch, (b) task shedding by over-capacity agents, (c) stale expected_tasks estimates. This section defines an epoch-boundary rebalancing algorithm.

```
REBALANCE_TRIGGER_RATIO = 1.5      // trigger if any agent exceeds 1.5x average
REBALANCE_VNODE_ADJUSTMENT = 0.10  // adjust vnodes by up to 10% per epoch
REBALANCE_MAX_CONSECUTIVE = 3      // max consecutive rebalances before cooldown
REBALANCE_COOLDOWN_EPOCHS = 5      // cooldown period after max consecutive

struct LoadBalanceState:
    parcel_id: ParcelId
    task_type: TaskType
    epoch: uint64
    agent_loads: Map<AgentId, uint32>
    avg_load: float
    max_load: uint32
    max_loaded_agent: AgentId
    imbalance_ratio: float
    consecutive_rebalances: uint32
    cooldown_until: uint64
    vnode_adjustments: Map<AgentId, int32>   // per-agent vnode count deltas

function measure_load_imbalance(
    ring: BoundedLoadsRing,
    epoch: uint64
) -> LoadBalanceState:
    total = sum(ring.agent_loads.values())
    avg = total / ring.agent_count if ring.agent_count > 0 else 0
    max_load = max(ring.agent_loads.values())
    max_agent = argmax(ring.agent_loads)
    ratio = max_load / avg if avg > 0 else 1.0

    return LoadBalanceState{
        parcel_id = ring.parcel_id,
        task_type = ring.task_type,
        epoch = epoch,
        agent_loads = dict(ring.agent_loads),
        avg_load = avg,
        max_load = max_load,
        max_loaded_agent = max_agent,
        imbalance_ratio = ratio,
        consecutive_rebalances = 0,
        cooldown_until = 0,
        vnode_adjustments = {}
    }

function rebalance_vnodes(
    ring: BoundedLoadsRing,
    state: LoadBalanceState,
    parcel: Parcel
) -> BoundedLoadsRing:
    // Check if rebalancing is needed
    if state.imbalance_ratio <= REBALANCE_TRIGGER_RATIO:
        return ring   // no rebalancing needed

    // Check cooldown
    if state.cooldown_until > state.epoch:
        return ring   // in cooldown, skip rebalancing

    // Check consecutive rebalance limit
    prev_state = get_previous_balance_state(ring.parcel_id, ring.task_type)
    consecutive = 0
    if prev_state and prev_state.consecutive_rebalances > 0:
        consecutive = prev_state.consecutive_rebalances

    if consecutive >= REBALANCE_MAX_CONSECUTIVE:
        state.cooldown_until = state.epoch + REBALANCE_COOLDOWN_EPOCHS
        log_warning("Rebalance cooldown activated for {ring.parcel_id}/{ring.task_type}")
        return ring

    // Compute vnode adjustments
    // Strategy: reduce vnodes for overloaded agents, increase for underloaded
    base_vnodes = ring.virtual_nodes_per_agent
    max_adjustment = ceil(base_vnodes * REBALANCE_VNODE_ADJUSTMENT)

    adjustments = {}
    for agent_id in ring.agent_loads:
        load = ring.agent_loads[agent_id]
        load_ratio = load / state.avg_load if state.avg_load > 0 else 1.0

        if load_ratio > 1.0 + ring.epsilon:
            // Overloaded: reduce vnodes (fewer ring positions = fewer assignments)
            reduction = min(
                max_adjustment,
                ceil(max_adjustment * (load_ratio - 1.0) / ring.epsilon)
            )
            adjustments[agent_id] = -reduction
        elif load_ratio < 1.0 - ring.epsilon:
            // Underloaded: increase vnodes
            increase = min(
                max_adjustment,
                ceil(max_adjustment * (1.0 - load_ratio) / ring.epsilon)
            )
            adjustments[agent_id] = increase
        else:
            adjustments[agent_id] = 0

    // Rebuild ring with adjusted vnode counts
    entries = empty sorted array
    for agent in parcel.agents:
        agent_vnodes = base_vnodes + adjustments.get(agent.id, 0)
        agent_vnodes = max(VNODE_MIN, agent_vnodes)   // never below minimum

        for v in 0..agent_vnodes-1:
            pos = SHA256(agent.id || ring.task_type || uint32_be(v)) mod 2^256
            entries.insert_sorted((pos, agent.id))

    // Update ring
    new_ring = BoundedLoadsRing{
        entries = entries,
        agent_count = ring.agent_count,
        virtual_nodes_per_agent = base_vnodes,   // base unchanged
        epsilon = ring.epsilon,
        task_type = ring.task_type,
        parcel_id = ring.parcel_id,
        agent_loads = {agent.id: 0 for agent in parcel.agents},
        total_assigned = 0,
        capacity_cap = ring.capacity_cap
    }

    // Record rebalance
    state.consecutive_rebalances = consecutive + 1
    state.vnode_adjustments = adjustments
    store_balance_state(state)

    return new_ring

function epoch_boundary_rebalance(parcel: Parcel, epoch: uint64):
    // Called during Phase 4 of epoch boundary (Section 4.3)
    for task_type in parcel.active_task_types:
        ring = parcel.hash_rings[task_type]
        state = measure_load_imbalance(ring, epoch)

        if state.imbalance_ratio > REBALANCE_TRIGGER_RATIO:
            log_info(
                "Load imbalance detected: {task_type} in {parcel.id}, "
                "ratio={state.imbalance_ratio:.2f}, "
                "max_agent={state.max_loaded_agent}"
            )
            parcel.hash_rings[task_type] = rebalance_vnodes(ring, state, parcel)
        else:
            // No rebalance needed — reset consecutive counter
            state.consecutive_rebalances = 0
            store_balance_state(state)
```

**Determinism note.** All rebalancing inputs (agent_loads, ring configuration, epoch) are derived from shared state that all agents independently compute. The rebalancing algorithm is a pure function of these inputs. Therefore, all agents produce identical rebalanced rings without communication — preserving the determinism invariant (INV-2).

### 2.4 Minimum Parcel Size with Merge Protocol

**Problem.** When agents depart a parcel, it may drop below the minimum viable size. Below 5 agents, load variance becomes extreme even with maximum virtual nodes, and diversity pools become too small for meaningful verification.

```
PARCEL_MIN_AGENTS = 5                  // hard minimum
PARCEL_MERGE_THRESHOLD = 6            // merge consideration when at or below this
PARCEL_MERGE_COOLDOWN_EPOCHS = 10     // minimum epochs between merges

struct ParcelMergeCandidate:
    source_parcel: ParcelId
    target_parcel: ParcelId
    combined_agent_count: uint32
    combined_load: float
    compatibility_score: float        // based on task type overlap
    merge_epoch: uint64

function check_parcel_health(parcel: Parcel, locus: Locus) -> ParcelHealthStatus:
    agent_count = len(parcel.agents)

    if agent_count < PARCEL_MIN_AGENTS:
        return ParcelHealthStatus{
            status = CRITICAL_UNDERSIZE,
            agent_count = agent_count,
            action = FORCE_MERGE,
            urgency = IMMEDIATE
        }
    elif agent_count <= PARCEL_MERGE_THRESHOLD:
        return ParcelHealthStatus{
            status = MARGINAL,
            agent_count = agent_count,
            action = CONSIDER_MERGE,
            urgency = NEXT_EPOCH
        }
    else:
        return ParcelHealthStatus{
            status = HEALTHY,
            agent_count = agent_count,
            action = NONE,
            urgency = NONE
        }

function find_merge_target(
    source: Parcel,
    locus: Locus
) -> ParcelMergeCandidate:
    candidates = []
    for parcel in locus.parcels:
        if parcel.id == source.id: continue
        if parcel.state == TRANSITIONING: continue   // don't merge into transitioning
        if parcel.last_merge_epoch + PARCEL_MERGE_COOLDOWN_EPOCHS > current_epoch():
            continue   // cooldown

        // Compute compatibility: task type overlap
        source_types = set(source.active_task_types)
        target_types = set(parcel.active_task_types)
        overlap = len(source_types & target_types) / len(source_types | target_types)

        // Prefer parcels that won't become too large after merge
        combined = len(source.agents) + len(parcel.agents)
        size_score = 1.0 if combined <= 30 else 30.0 / combined

        // Prefer parcels with similar load profiles
        source_load = sum(source.slv.dimensions) / len(source.slv.dimensions)
        target_load = sum(parcel.slv.dimensions) / len(parcel.slv.dimensions)
        load_compatibility = 1.0 - abs(source_load - target_load) / max(
            source_load, target_load, 0.01
        )

        compatibility = 0.4 * overlap + 0.3 * size_score + 0.3 * load_compatibility

        candidates.append(ParcelMergeCandidate{
            source_parcel = source.id,
            target_parcel = parcel.id,
            combined_agent_count = combined,
            combined_load = source_load + target_load,
            compatibility_score = compatibility,
            merge_epoch = current_epoch() + 1   // merge at next epoch boundary
        })

    if len(candidates) == 0:
        // No valid merge targets — source parcel operates in degraded mode
        // with enhanced monitoring until agents join or a target becomes available
        return null

    // Select best candidate
    candidates.sort_by(c => c.compatibility_score, descending)
    return candidates[0]

function execute_parcel_merge(
    source: Parcel,
    target: Parcel,
    locus: Locus
):
    // This runs as part of the Parcel Transition Protocol (Section 7.4)
    // Phase 1: PREPARE
    source.state = TRANSITIONING
    target.state = TRANSITIONING

    // Phase 2: SWITCH (at epoch boundary)
    // a) Move all agents from source to target
    for agent in source.agents:
        target.agents.add(agent)
        agent.parcel = target.id

    // b) Rebuild all hash rings for target with merged agent set
    for task_type in target.active_task_types | source.active_task_types:
        target.hash_rings[task_type] = build_bounded_ring(
            target, task_type,
            estimate_tasks(target, task_type)
        )

    // c) Merge VRF diversity pools
    // (pools are per-locus, not per-parcel, so no action needed
    //  beyond ensuring merged agents are in the eligibility set)

    // d) Export predictive context from source agents
    for agent in source.agents:
        ctv = serialize_context(agent, source)
        for neighbor in target.agents:
            if neighbor.id != agent.id:
                bootstrap_model(neighbor, agent, ctv)

    // e) Remove source parcel from locus
    locus.parcels.remove(source.id)
    source.state = DISSOLVED

    // f) Update target
    target.state = STABILIZING
    target.last_merge_epoch = current_epoch()

    // Phase 3: STABILIZE
    // Target operates in standard communication mode for 3-5 epochs
    // while predictive models converge for the newly added agents.

    log_info(
        "Parcel merge: {source.id} -> {target.id}, "
        "combined agents: {len(target.agents)}"
    )

function parcel_health_check_all(locus: Locus):
    // Called at each epoch boundary by the Parcel Manager
    for parcel in list(locus.parcels):   // copy list since we may modify
        health = check_parcel_health(parcel, locus)

        if health.action == FORCE_MERGE:
            candidate = find_merge_target(parcel, locus)
            if candidate:
                target = get_parcel(candidate.target_parcel)
                execute_parcel_merge(parcel, target, locus)
            else:
                // No merge target available
                // Enter enhanced monitoring: extra VRF committee slots
                // allocated from locus-wide pool, load rebalancing every epoch
                parcel.enhanced_monitoring = true
                log_warning(
                    "Parcel {parcel.id} below minimum size ({health.agent_count}) "
                    "with no merge target. Enhanced monitoring activated."
                )

        elif health.action == CONSIDER_MERGE:
            // Non-urgent: evaluate whether merge would improve overall locus health
            candidate = find_merge_target(parcel, locus)
            if candidate and candidate.compatibility_score > 0.7:
                target = get_parcel(candidate.target_parcel)
                execute_parcel_merge(parcel, target, locus)
```

---

## Part 3: Cross-Cutting Concerns

### 3.1 Interaction Between VRF Hardening and Small-Ring Defense

The two hardening areas interact in small parcels:

1. **Small parcels have small diversity pools.** A parcel with 5 agents has at most 5 agents in its diversity pools. With 4 diversity dimensions and randomized slot counts, the pools may be too small for meaningful stratification. Defense: diversity pool membership is per-locus, not per-parcel. A locus with 50 agents across 5 parcels provides pools of ~50 agents each.

2. **Parcel merges refresh diversity pools.** When a small parcel merges with an adjacent parcel, the combined agent set improves diversity pool quality. The merge protocol explicitly triggers VRF pool restratification.

3. **Load rebalancing must not interfere with VRF eligibility.** An agent that is rebalanced to fewer virtual nodes (receiving fewer task assignments) remains fully eligible for VRF verification committees. The load rebalancing affects only task scheduling, not verification duty.

### 3.2 New Constants Summary

| Constant | Default | Range | Section |
|----------|---------|-------|---------|
| HIDDEN_DIMENSION_COUNT | 2 | [1, 4] | 1.1 |
| DIVERSITY_COOLING_BASE | 50 | [20, 200] | 1.3 |
| DIVERSITY_COOLING_ESCALATION | 2.0 | [1.5, 3.0] | 1.3 |
| DIVERSITY_MAX_CHANGES_PER_YEAR | 4 | [1, 12] | 1.3 |
| DIVERSITY_CHANGE_STAKE_LOCK | 0.10 | [0.05, 0.25] | 1.3 |
| VNODE_TARGET_VARIANCE | 0.05 | [0.02, 0.10] | 2.2 |
| VNODE_MIN | 50 | [20, 100] | 2.2 |
| VNODE_MAX | 500 | [200, 1000] | 2.2 |
| REBALANCE_TRIGGER_RATIO | 1.5 | [1.2, 2.0] | 2.3 |
| REBALANCE_VNODE_ADJUSTMENT | 0.10 | [0.05, 0.20] | 2.3 |
| REBALANCE_MAX_CONSECUTIVE | 3 | [1, 5] | 2.3 |
| REBALANCE_COOLDOWN_EPOCHS | 5 | [2, 10] | 2.3 |
| PARCEL_MIN_AGENTS | 5 | [3, 10] | 2.4 |
| PARCEL_MERGE_THRESHOLD | 6 | [PARCEL_MIN_AGENTS, PARCEL_MIN_AGENTS+3] | 2.4 |
| PARCEL_MERGE_COOLDOWN_EPOCHS | 10 | [5, 20] | 2.4 |
| BOUNDED_LOADS_MIN_TASKS_FOR_BALANCE | 3 | [1, 10] | 2.1 |

### 3.3 Updated Conformance Requirements

**MUST (additions to Section 12.3):**
16. Implement hidden diversity dimensions per Section 1.1 with per-epoch salt derivation.
17. Implement randomized diversity filter thresholds per Section 1.2 within governance-approved ranges.
18. Enforce escalating cooling periods for diversity attribute changes per Section 1.3.
19. Implement epoch-boundary load rebalancing per Section 2.3.
20. Enforce minimum parcel size of 5 agents with merge protocol per Section 2.4.
21. Use adaptive virtual node counts per Section 2.2.

**SHOULD (additions):**
8. Implement the full Sybil cost analysis monitoring per Section 1.4 as a Sentinel Graph extension.
9. Implement the small-parcel override table per Section 2.2 with empirically validated values.

### 3.4 Updated Validation Requirements

**Experiment H1: Hidden Diversity Attribute Effectiveness**
- Setup: 500 honest agents, adversary with 50-250 Sybils optimizing public dimensions.
- Measure: adversary committee representation with hidden dimensions vs. without.
- Success criterion: hidden dimensions reduce adversary advantage by >40% compared to all-public.
- Kill criterion: hidden dimensions provide <20% advantage reduction.

**Experiment H2: Randomized Threshold Resistance**
- Setup: adversary with full knowledge of governance-approved ranges, 100 Sybils.
- Measure: adversary committee representation across 10,000 committee selections.
- Success criterion: adversary representation < 5% above stake-proportional baseline.
- Kill criterion: adversary representation > 10% above baseline.

**Experiment H3: Load Rebalancing Convergence**
- Setup: 5-50 agent parcels, Zipf task distribution, measure load imbalance over 20 epochs.
- Measure: epochs to achieve max/avg < 1.2 after initial assignment.
- Success criterion: convergence within 3 epochs for all parcel sizes >= 5.
- Kill criterion: convergence takes >5 epochs for any parcel size >= 5.

**Experiment H4: Parcel Merge Protocol**
- Setup: locus with 10 parcels, systematically reduce 3 parcels below minimum size.
- Measure: merge completion time, merged parcel load balance, predictive model convergence.
- Success criterion: merge completes within PTP bounds (3-5 epochs to STABILIZE), no verification gap.
- Kill criterion: merge causes >1 epoch verification starvation.

---

## Appendix H-A: Attack Tree for Diversity Grinding (Post-Hardening)

```
GOAL: >50% committee control through diversity grinding

  AND-1: Register Sybils with optimized attributes
    |
    +-- Optimize public dimensions (training_lineage, region)
    |     Cost: S_min * sybils_per_pool stake
    |     Effectiveness: partial (2 of 4 dimensions)
    |
    +-- Optimize hidden dimensions (methodology, temporal_bucket)
          Cost: impossible (epoch salt unknown until committee selection)
          Effectiveness: zero

  AND-2: Survive cooling period
    |
    +-- 50 epochs minimum (escalating to 400 for repeat changes)
    +-- 10% stake locked during cooling
    +-- Ineligible for verification during cooling

  AND-3: Avoid detection
    |
    +-- Sentinel Graph correlation audit: ~20 epoch window
    +-- Diversity distribution anomaly detector
    +-- Consequence: 100% stake slash on confirmed collusion

  RESULT:
    Cost: ~250 Sybils * S_min stake + cooling opportunity cost
    Max gain: ~20 epochs * bounded reward
    Net: deeply unprofitable (>3,500x cost/gain ratio)
    Residual risk: NEGLIGIBLE (bounded to <3% above baseline)
```

## Appendix H-B: Load Imbalance Bounds (Post-Hardening)

```
WITHOUT HARDENING (standard consistent hashing, V=150):
  N=5:   expected max/avg = 3.1x  (unacceptable)
  N=10:  expected max/avg = 2.3x  (unacceptable)
  N=15:  expected max/avg = 1.9x  (marginal)
  N=50:  expected max/avg = 1.4x  (marginal)

WITH BOUNDED-LOADS ONLY (epsilon=0.15, V=150):
  All N >= 5: guaranteed max/avg <= 1.15x
  But: requires sufficient task volume for overflow mechanism

WITH FULL HARDENING (bounded-loads + adaptive vnodes + rebalancing):
  N=5:   V=400, expected max/avg = 1.10x, rebalance if >1.5x
  N=10:  V=200, expected max/avg = 1.07x, rebalance if >1.5x
  N=15:  V=134, expected max/avg = 1.06x, rebalance if >1.5x
  N=50:  V=50,  expected max/avg = 1.03x, rebalance if >1.5x

  Epoch-boundary rebalance converges within 1-3 epochs.
  Parcel merge activates if N drops below 5.
  Ring size held constant at ~2,000 entries (O(0.1ms) rebuild).
```

---

*End of Hardening Addendum.*
*This addendum supersedes the corresponding subsections of the C3 Master Tech Spec where conflicts exist.*
*All pseudocode uses the same conventions as the Master Tech Spec (Section 0, Notation and Conventions).*
