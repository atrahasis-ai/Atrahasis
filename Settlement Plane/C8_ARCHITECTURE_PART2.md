# Deterministic Settlement Fabric v2.0 — Architecture Document Part 2
## Sections 8–14: Markets, Conservation, Slashing, Governance, Integration, Security, Deployment

**Invention ID:** C8
**Concept:** C8-A (Deterministic Settlement Fabric)
**Stage:** DESIGN
**Version:** v2.0
**Date:** 2026-03-10
**Status:** DRAFT — Part 2 of 2
**Depends on:** Part 1 (Sections 1–7): HDL, Three-Budget, Capability Stake, Multi-Rate, Four-Stream, Intent-Budget
**Assessment Council Verdict:** CONDITIONAL_ADVANCE (Feasibility 3/5, Novelty 4/5, Impact 4/5, Risk 6/10)
**Primary Scale Target:** 1K–10K agents (100K aspirational)

---

# Section 8: Capacity Market Architecture

## 8.1 Design Rationale

The Capacity Market is the price-discovery mechanism for Capacity Slices (CS) — the third budget in DSF's three-budget model. It answers the question: how much does a unit of compute, storage, or bandwidth cost during a given epoch? Without a functional market, resource allocation degenerates into either central planning (treasury dictates prices) or a commons tragedy (resources consumed without cost signals).

The market must function under constraints unique to the Atrahasis domain:

1. **Thin participation.** At primary scale (1K–10K agents), the market may have only dozens of active providers per resource type. Classical auction theory assumes thick markets; DSF cannot.
2. **Epoch-discretized clearing.** Prices are set at epoch boundaries (with mid-epoch tranches), not continuously. This creates intra-epoch price rigidity.
3. **Adversarial participants.** Capacity withholding, demand inflation, and cornering are all viable strategies (Attack 5 from Adversarial Report).
4. **Bootstrap phase.** The market must function even when participation is below minimum viable scale, requiring a protocol-funded backstop.

## 8.2 Market Structure

### 8.2.1 Resource Type Taxonomy

The capacity market operates independently for each resource type. Resource types are governance-defined and initially comprise:

```
ResourceType := ENUM {
    COMPUTE_STANDARD,    // General-purpose agent execution cycles
    COMPUTE_INTENSIVE,   // Heavy inference / verification workloads
    STORAGE_EPHEMERAL,   // Within-epoch temporary storage
    STORAGE_PERSISTENT,  // Cross-epoch durable storage
    BANDWIDTH_INTRA,     // Intra-locus message passing
    BANDWIDTH_CROSS      // Cross-locus message passing
}
```

Each resource type has its own order book, clearing price, and position limits. Resource types may be added or removed via G-class governance settlement.

### 8.2.2 Auction Format: Sealed-Bid Uniform-Price

```
AuctionFormat:
    type: "Sealed-bid uniform-price"
    bid_structure:
        - bidder_id: EntityID
        - resource_type: ResourceType
        - quantity: uint64          // CS units requested
        - max_price: Decimal(18,8)  // Maximum AIC per CS unit
        - priority_class: ENUM { FIRM, FLEXIBLE }
    offer_structure:
        - provider_id: EntityID
        - resource_type: ResourceType
        - quantity: uint64          // CS units available
        - min_price: Decimal(18,8)  // Minimum acceptable AIC per CS unit
        - availability_proof: Hash  // Cryptographic proof of capacity
```

**Why uniform-price:** In a uniform-price auction, all winning bidders pay the same clearing price (the highest rejected bid or lowest accepted offer, depending on convention). This is incentive-compatible for bidders — bidding one's true valuation is a weakly dominant strategy (Vickrey 1961, adapted for multi-unit by Ausubel 2004). In DSF, we use the highest-rejected-bid convention, meaning the clearing price equals the bid of the first bidder who did not receive allocation.

**Why sealed-bid:** Bids are committed via hash before the epoch boundary and revealed after. This prevents last-moment sniping and information extraction from observable bidding behavior.

### 8.2.3 Bid Commitment Protocol

```
Phase 1 — Commitment (epoch E, from 50% to 90% of epoch duration):
    bid_hash = HASH(bid_content || nonce || epoch_number)
    SUBMIT bid_hash to EABS pending queue

Phase 2 — Reveal (epoch E, from 90% to epoch boundary):
    SUBMIT (bid_content, nonce) to EABS pending queue
    VERIFY: HASH(bid_content || nonce || epoch_number) == bid_hash
    IF mismatch: bid is INVALID, bidder loses commitment_deposit

Phase 3 — Clearing (epoch boundary E → E+1):
    EABS processes all valid revealed bids/offers
    Deterministic auction clearing algorithm executes
    Results included in epoch E+1 settlement batch

commitment_deposit: 0.5% of (max_price × quantity)
    returned: on valid reveal
    slashed: on failure to reveal or hash mismatch
```

## 8.3 Progressive Clearing: 60/20/20 Tranche Release

All capacity for epoch E+1 is NOT cleared at a single epoch boundary. Instead:

```
Tranche Schedule:
    T1 (Primary):   60% of total capacity — cleared at epoch boundary E → E+1
    T2 (Secondary):  20% of total capacity — cleared at 40% of epoch E+1 elapsed
    T3 (Tertiary):   20% of total capacity — cleared at 70% of epoch E+1 elapsed

Tranche Sources:
    T1: Provider-offered capacity for the epoch
    T2: Use-it-or-lose-it reclaimed capacity (Section 8.5) + reserved T2 allocation
    T3: Use-it-or-lose-it reclaimed capacity + reserved T3 allocation + emergency release
```

**Rationale:** Progressive release mitigates the thin-market squeeze (Attack 5). An attacker who corners the T1 auction faces new supply in T2 and T3, diluting their position. It also provides price discovery refinement — T2 and T3 prices reflect actual utilization patterns observed during the epoch, not just pre-epoch predictions.

```
struct TrancheClearing {
    tranche_id:       uint8,          // 1, 2, or 3
    epoch:            EpochID,
    resource_type:    ResourceType,
    total_supply:     uint64,         // CS units available in this tranche
    clearing_price:   Decimal(18,8),  // Uniform price for this tranche
    allocations:      Vec<(EntityID, uint64)>,  // (bidder, quantity) pairs
    timestamp:        EpochTimestamp,
    deterministic_seed: Hash,         // For tiebreaking
}
```

**Cross-tranche price constraints:** To prevent extreme intra-epoch volatility, T2 and T3 clearing prices are bounded:

```
T2_price ∈ [0.5 × T1_price, 2.0 × T1_price]
T3_price ∈ [0.5 × T2_price, 2.0 × T2_price]

If market-clearing price would fall outside these bounds:
    - If below floor: set price = floor, excess supply goes unallocated (returned to providers)
    - If above ceiling: set price = ceiling, excess demand is rationed pro-rata
```

## 8.4 Position Limits and Enforcement

### 8.4.1 Position Limit Definition

```
INVARIANT POS-1: Position Limit
    FOR EACH entity E, resource_type R, epoch K:
        allocated(E, R, K) ≤ 0.15 × total_supply(R, K)

    WHERE:
        allocated(E, R, K) = Σ over all tranches T of allocation(E, R, K, T)
        total_supply(R, K) = Σ over all providers P of offered(P, R, K)
```

### 8.4.2 Enforcement Mechanism

Position limits are enforced at two levels:

**Level 1 — Auction clearing (preventive):**
```
function enforce_position_limit(bids, entity, resource_type, epoch):
    current_allocation = get_allocated(entity, resource_type, epoch)
    remaining_headroom = 0.15 * total_supply(resource_type, epoch) - current_allocation

    IF remaining_headroom <= 0:
        REJECT all bids from entity for this resource_type
        RETURN

    // Cap the entity's bid quantity at remaining headroom
    FOR bid IN bids WHERE bid.bidder_id == entity:
        bid.effective_quantity = MIN(bid.quantity, remaining_headroom)
        remaining_headroom -= bid.effective_quantity
```

**Level 2 — EABS settlement (corrective):**
If, due to a bug or race condition, an entity's allocation exceeds 15% after clearing, the EABS settlement function detects the violation and:
1. Reduces the entity's allocation to exactly 15%, removing the most recently cleared tranche allocations first (LIFO).
2. Returns excess capacity to the next tranche's available supply.
3. Records a scheduling violation for graduated slashing (Section 10).

### 8.4.3 Sybil-Resistant Position Limits

Position limits apply to economic entities, not just agent identifiers. The Sentinel Graph (from C3 Tidal Noosphere) provides identity clustering:

```
effective_position(entity_cluster) = Σ over all identities I in cluster(entity):
    allocated(I, resource_type, epoch)

INVARIANT POS-2: Cluster Position Limit
    effective_position(entity_cluster) ≤ 0.15 × total_supply
```

When the Sentinel Graph identifies a new cluster relationship, the EABS settlement function retroactively checks POS-2. If violated, excess allocations are reclaimed at the next tranche or epoch boundary.

## 8.5 Use-It-Or-Lose-It Mechanism

### 8.5.1 Utilization Monitoring

```
struct UtilizationRecord {
    entity_id:       EntityID,
    resource_type:   ResourceType,
    epoch:           EpochID,
    allocated:       uint64,         // CS units allocated
    consumed:        uint64,         // CS units actually used
    utilization_pct: Decimal(5,2),   // consumed / allocated × 100
    checkpoint_time: EpochTimestamp,  // When utilization was measured
}
```

### 8.5.2 Reclamation Rules

```
RULE UIOLI-1: Primary Reclamation
    AT 60% of epoch elapsed:
        FOR EACH allocation A:
            IF A.utilization_pct < 70%:
                reclaimable = A.allocated × (1.0 - A.utilization_pct / 70%)
                // Entity keeps a proportional share; unused fraction is reclaimed
                MOVE reclaimable CS units to T2 tranche supply
                REDUCE A.allocated by reclaimable
                EMIT UtilizationReclamation event

RULE UIOLI-2: Secondary Reclamation
    AT 85% of epoch elapsed:
        FOR EACH allocation A (post-T2 clearing):
            IF A.utilization_pct < 70%:
                reclaimable = A.allocated × (1.0 - A.utilization_pct / 70%)
                MOVE reclaimable CS units to T3 tranche supply
                REDUCE A.allocated by reclaimable
```

### 8.5.3 Grace Period for New Allocations

Allocations from T2 and T3 tranches receive a grace period before utilization checks apply:

```
grace_period(tranche) = CASE tranche OF:
    T1: no grace (full epoch to utilize)
    T2: 15% of epoch duration after T2 clearing
    T3: 10% of epoch duration after T3 clearing
```

## 8.6 Reserve Pricing Floor

```
struct ReservePrice {
    resource_type:   ResourceType,
    floor_price:     Decimal(18,8),  // Minimum AIC per CS unit
    set_by:          GovernanceProposalID,
    effective_epoch:  EpochID,
    review_interval: uint32,         // Epochs between mandatory governance review
}
```

**Purpose:** The reserve price prevents predatory undercutting in squeeze-and-dump cycles. Without a floor, a well-capitalized attacker could offer capacity below cost for several epochs (driving out competitors), then raise prices once competition is eliminated.

**Calibration:** The initial reserve price is set to 80% of the estimated marginal cost of providing one CS unit, based on infrastructure cost surveys conducted during bootstrap. Governance may adjust the floor at intervals of `review_interval` epochs (initially 50 epochs).

**Enforcement:**
```
function validate_offer(offer):
    reserve = get_reserve_price(offer.resource_type)
    IF offer.min_price < reserve.floor_price:
        REJECT offer with error BELOW_RESERVE_FLOOR
```

## 8.7 Bootstrap Provisions

### 8.7.1 Hard Gate HG-5 Resolution: Minimum Viable Scale Analysis

**Model:** The capacity market functions without protocol intervention when:

```
CONDITION MVS (Minimum Viable Scale):
    number_providers ≥ 3 × number_resource_types
    AND
    FOR EACH resource_type R:
        independent_providers(R) ≥ 5

Given initial resource_types = 6:
    Minimum total providers = MAX(3 × 6, enough for 5 per type)
    = 18 providers minimum (if each covers 1 type)
    = realistically ~10 providers if each covers multiple types
```

**Derivation:**

The "3 × resource_types" requirement ensures that no single provider controls more than 33% of any type's supply (since position limits cap at 15%, we need at least ceil(1/0.15) ≈ 7 providers per type for the limit to bind meaningfully, but 5 is the functional minimum where auction price discovery produces meaningful signals based on electricity market analogies — FERC Order 888 analysis showed minimum 5 independent generators per zone for competitive outcomes).

The "5 per resource type" requirement ensures:
- No single provider failure eliminates more than 20% of supply
- Auction clearing has enough bids for meaningful price discovery
- Position limits (15%) are binding — 5 providers × 15% = 75% max concentration by top entity

### 8.7.2 Bootstrap Capacity Provider of Last Resort (CPLR)

```
struct BootstrapCPLR {
    treasury_allocation:     Decimal(18,8),  // Max AIC from treasury (20% cap)
    capacity_offered:        Map<ResourceType, uint64>,
    pricing_rule:            "Reserve floor price × 1.1 (slightly above floor)"
    participation_rule:      "CPLR bids ONLY when provider_count(R) < 5 for any R"
    sunset_condition:        BootstrapSunsetCondition,
}

struct BootstrapSunsetCondition {
    // MVS must hold for 3 consecutive epochs
    consecutive_epochs_required: 3,
    check: |epoch| -> bool {
        FOR EACH resource_type R:
            IF independent_providers(R, epoch) < 5:
                RETURN false
        IF total_providers(epoch) < 3 * count(ResourceType):
            RETURN false
        RETURN true
    },
    // Once sunset triggers, CPLR capacity is withdrawn over 5 epochs (20% per epoch)
    withdrawal_schedule: "Linear over 5 epochs post-sunset trigger"
}
```

### 8.7.3 Bootstrap Sunset Protocol

```
PROTOCOL BootstrapSunset:
    STATE: { ACTIVE, MONITORING, WITHDRAWING, SUNSET }

    ACTIVE:
        CPLR participates in all tranches for resource types with < 5 providers
        Treasury funds capacity at reserve_floor × 1.1

    TRANSITION ACTIVE → MONITORING:
        WHEN MVS condition holds for first time

    MONITORING:
        CPLR continues participating but logs market health metrics
        Duration: 3 consecutive epochs of MVS
        IF MVS violated during monitoring: REVERT to ACTIVE, reset counter

    TRANSITION MONITORING → WITHDRAWING:
        WHEN 3 consecutive epochs of MVS observed
        EMIT BootstrapSunsetInitiated event

    WITHDRAWING:
        Epoch 1: CPLR capacity reduced to 80% of ACTIVE level
        Epoch 2: Reduced to 60%
        Epoch 3: Reduced to 40%
        Epoch 4: Reduced to 20%
        Epoch 5: Reduced to 0%
        IF at any point during withdrawal, MVS condition fails:
            PAUSE withdrawal, EMIT BootstrapSunsetPaused
            IF MVS fails for 2+ consecutive epochs: REVERT to ACTIVE

    TRANSITION WITHDRAWING → SUNSET:
        WHEN CPLR capacity reaches 0% and MVS holds
        EMIT BootstrapSunsetComplete
        Treasury allocation for CPLR is released to general treasury
```

## 8.8 Market Manipulation Countermeasures

### 8.8.1 Capacity Withholding Detection

```
struct WithholdingDetector {
    // A provider who repeatedly offers capacity then withdraws or underdelivers
    metrics_per_provider: Map<EntityID, ProviderMetrics>,
}

struct ProviderMetrics {
    advertised_capacity:  Vec<uint64>,    // Per-epoch advertised
    offered_to_auction:   Vec<uint64>,    // Per-epoch actually offered
    delivered:            Vec<uint64>,    // Per-epoch actually delivered
    withholding_ratio:    Decimal(5,4),   // (advertised - offered) / advertised
    delivery_ratio:       Decimal(5,4),   // delivered / allocated
}

RULE MW-1: Withholding Detection
    IF provider.withholding_ratio > 0.30 over trailing 5 epochs:
        FLAG provider for governance review
        REDUCE provider's maximum offer quantity to 70% of historical average
        EMIT WithholdingAlert(provider_id, withholding_ratio)

RULE MW-2: Delivery Failure
    IF provider.delivery_ratio < 0.80 over trailing 3 epochs:
        APPLY graduated slashing (Section 10) — scheduling violation class
        REDUCE provider's maximum offer quantity to delivered average
        EMIT DeliveryFailureAlert(provider_id, delivery_ratio)
```

### 8.8.2 Demand Inflation Detection

```
RULE DI-1: Demand Inflation
    // An entity that consistently bids high quantities but uses little
    IF entity.bid_quantity / entity.actual_utilization > 2.0 over trailing 5 epochs:
        entity.bid_credibility_score *= 0.8  // Reduce priority in auction clearing
        IF entity.bid_credibility_score < 0.5:
            entity.max_bid_quantity = 0.5 × position_limit  // Hard restriction
            EMIT DemandInflationAlert(entity_id)
```

### 8.8.3 Cornering Detection (Sentinel Graph Integration)

```
RULE CORN-1: Concentration Monitoring
    FOR EACH resource_type R, epoch K:
        hhi = Σ over entities E: (share(E, R, K))²
        // HHI > 0.25 indicates highly concentrated market
        IF hhi > 0.25:
            EMIT ConcentrationAlert(resource_type=R, hhi=hhi)
            TRIGGER governance review of position limits for R
        IF hhi > 0.40:
            EMERGENCY: reduce position limit for R to 10% for next epoch
            EMIT ConcentrationEmergency(resource_type=R, hhi=hhi)

    WHERE share(E, R, K) = allocated(E, R, K) / total_allocated(R, K)
```

### 8.8.4 Cross-Entity Collusion Detection

```
RULE COLL-1: Coordinated Bidding Detection
    // Uses Sentinel Graph identity clustering from C3
    FOR EACH pair of entities (E1, E2) NOT in same known cluster:
        bid_correlation = pearson(E1.bid_prices, E2.bid_prices, trailing_20_epochs)
        quantity_correlation = pearson(E1.bid_quantities, E2.bid_quantities, trailing_20_epochs)

        IF bid_correlation > 0.85 AND quantity_correlation > 0.85:
            SUBMIT to Sentinel Graph for cluster analysis
            IF confirmed as likely same economic entity:
                APPLY cluster position limits (POS-2)
                EMIT CollusionAlert(E1, E2, bid_correlation, quantity_correlation)
```

## 8.9 Price Discovery and Equilibrium Properties

### 8.9.1 Auction Clearing Algorithm

```
function clear_auction(
    bids: Vec<Bid>,
    offers: Vec<Offer>,
    resource_type: ResourceType,
    tranche: TrancheID,
    epoch: EpochID,
    deterministic_seed: Hash
) -> TrancheClearing:

    // Step 1: Filter and validate
    valid_bids = bids
        .filter(|b| b.resource_type == resource_type)
        .filter(|b| validate_bid(b))           // Check commitment hash, deposit, etc.
        .filter(|b| check_position_headroom(b)) // Position limit enforcement

    valid_offers = offers
        .filter(|o| o.resource_type == resource_type)
        .filter(|o| validate_offer(o))         // Check availability proof, reserve floor

    // Step 2: Sort bids descending by max_price, offers ascending by min_price
    // Tiebreaking: HASH(entity_id || deterministic_seed) — deterministic, unpredictable
    sorted_bids = valid_bids.sort_by(|b| (
        Reverse(b.max_price),
        HASH(b.bidder_id || deterministic_seed)
    ))

    sorted_offers = valid_offers.sort_by(|o| (
        o.min_price,
        HASH(o.provider_id || deterministic_seed)
    ))

    // Step 3: Determine total supply for this tranche
    total_supply = sorted_offers.sum(|o| o.quantity)

    // Step 4: Walk demand curve (descending price) against supply curve (ascending price)
    cumulative_demand = 0
    cumulative_supply = 0
    clearing_price = 0

    demand_curve = []  // (cumulative_quantity, price) pairs
    FOR bid IN sorted_bids:
        effective_qty = apply_position_limit(bid)
        cumulative_demand += effective_qty
        demand_curve.push((cumulative_demand, bid.max_price))

    supply_curve = []  // (cumulative_quantity, price) pairs
    FOR offer IN sorted_offers:
        cumulative_supply += offer.quantity
        supply_curve.push((cumulative_supply, offer.min_price))

    // Step 5: Find intersection — clearing price and quantity
    // The clearing price is the price at which supply meets demand
    cleared_quantity = 0
    clearing_price = 0

    supply_idx = 0
    demand_idx = 0
    remaining_supply = 0
    remaining_demand = 0

    // Sweep algorithm: match demand tranches against supply tranches
    WHILE supply_idx < supply_curve.len() AND demand_idx < demand_curve.len():
        current_supply_price = sorted_offers[supply_idx].min_price
        current_demand_price = sorted_bids[demand_idx].max_price

        IF current_demand_price < current_supply_price:
            BREAK  // No more mutually acceptable trades

        // Match at the marginal price
        available_supply = sorted_offers[supply_idx].quantity - remaining_supply_consumed
        available_demand = apply_position_limit(sorted_bids[demand_idx]) - remaining_demand_filled

        matched = MIN(available_supply, available_demand)
        cleared_quantity += matched
        clearing_price = current_supply_price  // Uniform price = marginal supply price

        // Advance cursors
        IF matched == available_supply:
            supply_idx += 1
            remaining_supply_consumed = 0
        ELSE:
            remaining_supply_consumed += matched

        IF matched == available_demand:
            demand_idx += 1
            remaining_demand_filled = 0
        ELSE:
            remaining_demand_filled += matched

    // Step 6: Apply cross-tranche price bounds
    IF tranche > 1:
        prev_price = get_tranche_clearing_price(tranche - 1, resource_type, epoch)
        clearing_price = CLAMP(clearing_price, 0.5 * prev_price, 2.0 * prev_price)

    // Step 7: Build allocation list
    allocations = []
    remaining_cleared = cleared_quantity
    FOR bid IN sorted_bids:
        IF remaining_cleared <= 0: BREAK
        IF bid.max_price < clearing_price: BREAK

        alloc_qty = MIN(apply_position_limit(bid), remaining_cleared)
        allocations.push((bid.bidder_id, alloc_qty))
        remaining_cleared -= alloc_qty

    // Step 8: Handle FIRM vs FLEXIBLE priority
    // FIRM bids that didn't clear are queued for T2/T3 with priority
    uncleared_firm = sorted_bids
        .filter(|b| b.priority_class == FIRM AND b NOT IN allocations)
    QUEUE uncleared_firm for next tranche with 1.05× price premium willingness

    RETURN TrancheClearing {
        tranche_id: tranche,
        epoch: epoch,
        resource_type: resource_type,
        total_supply: total_supply,
        clearing_price: clearing_price,
        allocations: allocations,
        timestamp: current_epoch_timestamp(),
        deterministic_seed: deterministic_seed,
    }
```

### 8.9.2 Equilibrium Properties

**Property EQ-1: Individual Rationality.** No bidder pays more than their stated maximum. No provider receives less than their stated minimum. (Guaranteed by the clearing algorithm — only mutually acceptable trades execute.)

**Property EQ-2: Uniform Pricing.** All winning bidders for a given tranche and resource type pay the same clearing price. (Guaranteed by the uniform-price rule.)

**Property EQ-3: Weak Incentive Compatibility.** Bidding one's true valuation is a weakly dominant strategy for bidders (standard result for uniform-price auctions). Providers may have incentive to shade offers upward (supply reduction), which is mitigated by position limits and withholding detection.

**Property EQ-4: Price Convergence.** Under stationary demand and supply, clearing prices converge to marginal cost of provision within O(log(epochs)) epochs. (Standard competitive equilibrium result, contingent on sufficient market thickness — at least 5 providers per type.)

**Property EQ-5: Progressive Stability.** The 60/20/20 tranche structure with cross-tranche price bounds ensures that intra-epoch price volatility is bounded by a factor of 4× (2× per tranche transition, two transitions). Empirically, electricity day-ahead vs. real-time spreads average 15–25% with similar structures.

## 8.10 Integration with CSO Framework

```
CSO-Market Integration Contract:

1. CSO CREATION:
    - New CSOs are registered with the capacity market as potential supply sources
    - CSO capacity = Σ over resources R of provider_capacity(R)
    - CSO lifecycle state must be ACTIVE for provider to offer capacity

2. CSO REBALANCING (triggered by tidal phase transitions in C3):
    - When a locus transitions tidal phase, CSO allocations may shift
    - Shifted capacity is released to the next tranche's supply pool
    - Entities holding shifted CSOs receive priority rebidding rights in next tranche

3. SETTLEMENT FLOW:
    - Auction clearing prices determine CS expenditure per entity per epoch
    - CS expenditure is settled via EABS in the B-class (fast) settlement stream
    - Provider revenue = clearing_price × allocated_quantity, settled B-class
    - Bidder cost = clearing_price × received_quantity, deducted from SB

4. CAPACITY PROVING:
    - Providers must submit availability_proofs with offers
    - availability_proof = cryptographic attestation that resources exist and are uncommitted
    - Proof format: PCVM verification attestation (C5 integration)
    - Invalid proofs → scheduling violation → graduated slashing
```

---

# Section 9: CSO Conservation Framework

## 9.1 Conservation Invariant — Formal Statement

The CSO Conservation Invariant is the economic bedrock of DSF. If it fails, the system has either created or destroyed value — both unacceptable.

```
INVARIANT CSO-CONS (Conservation):
    ∀ epoch E, ∀ resource_type R:
        Σ_{i ∈ entities} alloc(i, R, E)
      + Σ_{i ∈ entities} pending_out(i, R, E)
      - Σ_{i ∈ entities} pending_in(i, R, E)
      + spent(R, E)
      = total_supply(R, E)

    WHERE:
        alloc(i, R, E)        = CS units currently allocated to entity i
        pending_out(i, R, E)  = CS units entity i has committed to transfer out (not yet received)
        pending_in(i, R, E)   = CS units entity i is expecting to receive (not yet allocated)
        spent(R, E)           = CS units consumed (irrecoverable) during or before epoch E
        total_supply(R, E)    = total CS units in existence for resource type R
                              = initial_supply(R) + minted(R, 0..E) - burned(R, 0..E)
```

### 9.1.1 Supply Mutation Rules

```
RULE SUPPLY-1: Minting
    total_supply may increase ONLY via treasury-authorized minting
    Minting is a G-class governance operation
    minted(R, E) enters as pending_in to the treasury entity
    Conservation holds: total_supply increases, pending_in increases by same amount

RULE SUPPLY-2: Burning
    total_supply may decrease ONLY via:
        (a) Slashing-triggered burns (Section 10)
        (b) Governance-authorized burns
    burned(R, E) removes from spent
    Conservation holds: total_supply decreases, spent decreases by same amount

RULE SUPPLY-3: No Spontaneous Generation
    No operation may increase total_supply without a corresponding minting event
    No operation may decrease total_supply without a corresponding burning event
    This is enforced by EABS — the settlement function rejects batches that violate SUPPLY-3
```

## 9.2 Formal Proof Sketch: EABS Preserves Conservation

**Theorem:** If CSO-CONS holds at epoch E, and the EABS settlement function processes a valid epoch batch B(E+1), then CSO-CONS holds at epoch E+1.

**Proof sketch (by case analysis on operation types in the batch):**

The epoch batch B(E+1) contains operations of the following types. We show each preserves conservation:

**Case 1: Transfer(sender, receiver, amount, resource_type)**

```
Pre-state:  alloc(sender) = S, alloc(receiver) = R
Operation:  alloc(sender) -= amount, alloc(receiver) += amount
Post-state: alloc(sender) = S - amount, alloc(receiver) = R + amount

Conservation delta: (S - amount) + (R + amount) = S + R = unchanged
∴ Σ alloc unchanged. No other terms affected. CSO-CONS preserved. ∎
```

**Case 2: InitiatePending(sender, receiver, amount, resource_type)**

```
Pre-state:  alloc(sender) = S, pending_out(sender) = PO, pending_in(receiver) = PI
Operation:  alloc(sender) -= amount
            pending_out(sender) += amount
            pending_in(receiver) += amount
Post-state: alloc(sender) = S - amount
            pending_out(sender) = PO + amount
            pending_in(receiver) = PI + amount

Conservation delta:
    Σ alloc changes by: -amount
    Σ pending_out changes by: +amount
    Σ pending_in changes by: +amount

    Net: (Σ alloc - amount) + (Σ pending_out + amount) - (Σ pending_in + amount) + spent
       = Σ alloc + Σ pending_out - Σ pending_in + spent - amount + amount - amount + amount

Wait — let me be precise:

    New_LHS = (Σ alloc - amount) + (Σ pending_out + amount) - (Σ pending_in + amount) + spent
            = Σ alloc - amount + Σ pending_out + amount - Σ pending_in - amount + spent
            = Σ alloc + Σ pending_out - Σ pending_in + spent - amount

This does NOT preserve conservation naively. The issue is that pending_in is subtracted.

CORRECTION: The invariant accounts for this correctly. When sender's alloc decreases by amount
and pending_out increases by amount, from the sender side: alloc goes down, pending_out goes up
— net change to (alloc + pending_out) = 0. From the receiver side: pending_in goes up — net
change to (-pending_in) = -amount. But NO — the receiver hasn't received anything yet. The
invariant must account for the fact that pending_in represents FUTURE allocation.

REVISED INVARIANT INTERPRETATION:
    Σ alloc + Σ pending_out - Σ pending_in + spent = total_supply

    Think of it as: allocated + in-transit - expected-arrivals + consumed = total

    pending_out = resources that have LEFT an allocation but not yet ARRIVED
    pending_in = resources that are EXPECTED to arrive but haven't yet

    For a transfer in-flight: sender's alloc decreased, sender's pending_out increased (net 0
    for sender). Receiver's pending_in increased. So:

    Σ alloc changes: -amount
    Σ pending_out changes: +amount
    -Σ pending_in changes: -amount

    Net: -amount + amount - amount = -amount ≠ 0

This reveals that the invariant as stated has a sign issue for in-flight transfers.

CORRECTED INVARIANT:
    Σ alloc + Σ in_transit + spent = total_supply

    WHERE in_transit(R, E) = Σ pending_out = Σ pending_in (these must be equal globally)

    ADDITIONAL INVARIANT: Σ pending_out = Σ pending_in (every outbound has a matching inbound)
```

**Revised Conservation Invariant:**

```
INVARIANT CSO-CONS-REVISED:
    ∀ epoch E, ∀ resource_type R:
        Σ_{i} alloc(i, R, E) + Σ_{i} pending_out(i, R, E) + spent(R, E) = total_supply(R, E)

    SUPPORTING INVARIANT CSO-BALANCE:
        Σ_{i} pending_out(i, R, E) = Σ_{i} pending_in(i, R, E)
        (Every outbound pending has a matching inbound pending)
```

**Proof resumption with corrected invariant:**

**Case 2 (revised): InitiatePending(sender, receiver, amount, resource_type)**

```
Pre-state:  alloc(sender) = S, pending_out(sender) = PO_s, pending_in(receiver) = PI_r
Operation:  alloc(sender) -= amount
            pending_out(sender) += amount
            pending_in(receiver) += amount

CSO-CONS-REVISED delta:
    Σ alloc changes: -amount
    Σ pending_out changes: +amount
    Net: -amount + amount = 0. ✓

CSO-BALANCE delta:
    Σ pending_out changes: +amount
    Σ pending_in changes: +amount
    Net: 0. ✓
∴ Both invariants preserved. ∎
```

**Case 3: CompletePending(sender, receiver, amount, resource_type)**

```
Pre-state:  pending_out(sender) = PO_s, pending_in(receiver) = PI_r, alloc(receiver) = R
Operation:  pending_out(sender) -= amount
            pending_in(receiver) -= amount
            alloc(receiver) += amount

CSO-CONS-REVISED delta:
    Σ alloc changes: +amount
    Σ pending_out changes: -amount
    Net: +amount - amount = 0. ✓

CSO-BALANCE delta:
    Σ pending_out changes: -amount
    Σ pending_in changes: -amount
    Net: 0. ✓
∴ Both invariants preserved. ∎
```

**Case 4: Consume(entity, amount, resource_type)**

```
Pre-state:  alloc(entity) = A, spent = SP
Operation:  alloc(entity) -= amount
            spent += amount

CSO-CONS-REVISED delta:
    Σ alloc changes: -amount
    spent changes: +amount
    Net: 0. ✓
∴ Conservation preserved. ∎
```

**Case 5: TimeoutPending(sender, receiver, amount, resource_type)**

```
Pre-state:  pending_out(sender) = PO_s, pending_in(receiver) = PI_r, alloc(sender) = S
Operation:  pending_out(sender) -= amount
            pending_in(receiver) -= amount
            alloc(sender) += amount  // Return to sender
            // Timeout fee applied separately as a Consume operation

CSO-CONS-REVISED delta:
    Σ alloc changes: +amount
    Σ pending_out changes: -amount
    Net: 0. ✓

CSO-BALANCE delta:
    Σ pending_out changes: -amount
    Σ pending_in changes: -amount
    Net: 0. ✓
∴ Conservation preserved. ∎
```

**Case 6: Slash(entity, amount, resource_type, redistribution)**

```
Pre-state:  alloc(entity) = A
Operation:  alloc(entity) -= amount
            // 50% burned: spent += 0.5 × amount, total_supply -= 0.5 × amount
            // 30% to treasury: alloc(treasury) += 0.3 × amount
            // 20% to reporter: alloc(reporter) += 0.2 × amount

CSO-CONS-REVISED delta:
    Σ alloc: -amount + 0.3×amount + 0.2×amount = -0.5×amount
    spent: +0.5×amount (from burn)
    total_supply: -0.5×amount (from burn — both sides reduce)

    LHS delta: -0.5×amount + 0.5×amount = 0
    RHS delta: -0.5×amount

    Wait: the burn means spent increases AND total_supply decreases.

    Burn operation: remove from existence
        total_supply -= burn_amount
        The burned amount does NOT go to spent — it ceases to exist.

REVISED Case 6:
    alloc(entity) -= amount
    alloc(treasury) += 0.3 × amount
    alloc(reporter) += 0.2 × amount
    total_supply -= 0.5 × amount     // burn

    CSO-CONS-REVISED:
        Σ alloc changes: -amount + 0.3×amount + 0.2×amount = -0.5×amount
        total_supply changes: -0.5×amount
        LHS delta: -0.5×amount
        RHS delta: -0.5×amount
        Net: 0. ✓
∴ Conservation preserved. ∎
```

**Case 7: Mint(treasury, amount, resource_type)**

```
Operation:  alloc(treasury) += amount
            total_supply += amount

CSO-CONS-REVISED:
    Σ alloc changes: +amount
    total_supply changes: +amount
    LHS delta: +amount
    RHS delta: +amount
    Net: 0. ✓
∴ Conservation preserved. ∎
```

**Conclusion of proof sketch:** Every operation type in the EABS batch preserves CSO-CONS-REVISED and CSO-BALANCE. Since the batch is a sequence of such operations, and conservation is preserved by each, it is preserved by the batch. Since EABS processes batches atomically (all-or-nothing per epoch), conservation holds at every epoch boundary. ∎

## 9.3 Pending State Lifecycle

```
PendingState := ENUM {
    INITIATED,    // Sender's alloc reduced, pending_out/pending_in created
    CONFIRMING,   // Receiver has acknowledged, awaiting EABS settlement
    COMPLETING,   // EABS has processed CompletePending in current batch
    COMPLETED,    // Fully settled — pending cleared, receiver's alloc increased
    TIMING_OUT,   // Timeout threshold reached, auto-revert initiated
    TIMED_OUT,    // Reverted — alloc returned to sender minus fee
    DISPUTED      // Dispute filed — enters G-class governance
}

Lifecycle:
    INITIATED → CONFIRMING     (receiver acknowledgment within 1 epoch)
    CONFIRMING → COMPLETING    (EABS includes CompletePending in batch)
    COMPLETING → COMPLETED     (EABS batch settles successfully)
    INITIATED → TIMING_OUT     (no confirmation after 2 epochs)
    CONFIRMING → TIMING_OUT    (no completion after 3 epochs from initiation)
    TIMING_OUT → TIMED_OUT     (EABS processes TimeoutPending)
    Any → DISPUTED             (dispute filed before timeout — pauses timeout clock)
    DISPUTED → COMPLETING      (dispute resolved in favor of completion)
    DISPUTED → TIMING_OUT      (dispute resolved in favor of revert)
```

### 9.3.1 Timeout Enforcement

```
struct PendingTimeout {
    max_duration_epochs: 3,
    fee_on_timeout: Decimal(5,4),     // 2% of pending amount
    fee_destination: "BURNED",         // Not redistributed — prevents gaming
}

function check_pending_timeouts(epoch: EpochID, pending_states: Vec<PendingState>):
    FOR ps IN pending_states:
        IF ps.state IN {INITIATED, CONFIRMING}:
            age = epoch - ps.initiated_epoch
            IF age >= 3:
                EMIT TimeoutPending(ps.sender, ps.receiver, ps.amount, ps.resource_type)
                fee = ps.amount × 0.02
                // Fee comes from the collateral deposit, not the pending amount
                EMIT Consume(ps.sender, fee, ps.resource_type)  // Burn the fee
                // Remaining collateral returned with the pending amount
```

### 9.3.2 Collateral Requirements

```
struct PendingCollateral {
    rate: Decimal(5,4),               // 5% of pending amount
    source: "Deducted from sender's alloc at InitiatePending"
    return_on_completion: true,
    forfeit_on_timeout: true,
    forfeit_distribution: {
        timeout_fee: "2% of pending amount (burned)",
        remaining_collateral: "3% of pending amount (returned to sender)"
    }
}

// Collateral is SEPARATE from the pending amount itself
function initiate_pending(sender, receiver, amount, resource_type):
    collateral = amount × 0.05
    total_deduction = amount + collateral

    REQUIRE alloc(sender, resource_type) >= total_deduction

    alloc(sender) -= total_deduction
    pending_out(sender) += amount
    pending_in(receiver) += amount
    collateral_held(sender) += collateral

    // Conservation check:
    // Σ alloc decreased by (amount + collateral)
    // Σ pending_out increased by amount
    // collateral_held is a sub-category of alloc for conservation purposes
    // Net: alloc decreased by amount (collateral still counted in alloc-equivalent)
    //       pending_out increased by amount → net 0. ✓

    // IMPLEMENTATION NOTE: collateral_held is tracked as a separate field but
    // counts toward Σ alloc for conservation purposes. It is "frozen alloc."
```

### 9.3.3 Volume Caps

```
INVARIANT PENDING-CAP-1: Per-Entity Pending Cap
    ∀ entity E, ∀ resource_type R:
        pending_out(E, R) ≤ 0.10 × total_supply(R)

INVARIANT PENDING-CAP-2: Global Pending Cap
    ∀ resource_type R:
        Σ_{i} pending_out(i, R) ≤ 0.25 × total_supply(R)

Enforcement:
    InitiatePending is REJECTED if either cap would be violated.
    Checked in EABS batch processing — deterministic, same result on all nodes.
```

## 9.4 Runtime Enforcement via EABS

```
function eabs_settle_epoch(epoch: EpochID, batch: EpochBatch) -> Result<EpochState, ConservationViolation>:

    // Snapshot pre-state
    pre_state = get_settled_state(epoch - 1)

    // Process batch operations in canonical order
    working_state = pre_state.clone()
    FOR op IN batch.operations_sorted():  // Canonical sort: (op_type, timestamp_hash, submitter_id)
        result = apply_operation(working_state, op)
        IF result.is_err():
            LOG("Operation rejected: {}", op, result.err())
            CONTINUE  // Skip invalid operations, don't halt batch

    // Post-batch conservation check
    FOR resource_type IN ResourceType.ALL:
        lhs = sum_alloc(working_state, resource_type)
            + sum_pending_out(working_state, resource_type)
            + working_state.spent(resource_type)
        rhs = working_state.total_supply(resource_type)

        IF lhs != rhs:
            // CONSERVATION VIOLATION — this should never happen if all operations
            // are correctly implemented. If it does, it indicates a bug.
            LOG_CRITICAL("Conservation violation detected! LHS={}, RHS={}, delta={}", lhs, rhs, lhs-rhs)
            RETURN Err(ConservationViolation {
                epoch: epoch,
                resource_type: resource_type,
                expected: rhs,
                actual: lhs,
                delta: lhs - rhs,
            })

    // Conservation holds — commit the epoch
    RETURN Ok(working_state)
```

### 9.4.1 Recovery Protocol on Conservation Violation

```
PROTOCOL ConservationRecovery:
    TRIGGER: EABS settlement function returns ConservationViolation

    Step 1: HALT
        All nodes halt settlement for current epoch
        CRDT read-path continues (optimistic reads still available)
        EMIT ConservationViolationAlert to all governance participants

    Step 2: REPLAY WITH LOGGING
        Re-process the epoch batch with per-operation conservation checks:
        FOR op IN batch.operations_sorted():
            pre_check = compute_conservation(working_state)
            apply_operation(working_state, op)
            post_check = compute_conservation(working_state)
            IF pre_check.holds AND NOT post_check.holds:
                IDENTIFY op as the violating operation
                LOG_CRITICAL("Violating operation identified: {}", op)
                BREAK

    Step 3: QUARANTINE
        Remove the violating operation from the batch
        Re-process the batch without it
        IF conservation now holds:
            Settle the epoch with the reduced batch
            EMIT QuarantinedOperation(op) for governance review
        ELSE:
            Remove operations one-by-one (binary search) until conservation holds
            Settle with maximum valid subset

    Step 4: ROOT CAUSE
        The quarantined operation(s) indicate either:
        (a) A bug in the settlement function (highest priority fix)
        (b) A malformed operation that passed validation (validation bug)
        (c) A novel attack vector (update adversarial model)
        Governance must classify and address within 5 epochs
```

## 9.5 I-Confluence Analysis for Read-Path Operations

The CRDT read-path supports the following operations. We analyze each for I-confluence (the property that concurrent execution on different replicas converges to the same state without coordination):

```
READ-PATH OPERATIONS:

1. BalanceQuery(entity, resource_type) → uint64
   I-confluent: YES
   Proof: Read-only operation. No state mutation. Trivially confluent.

2. AvailabilityCheck(resource_type) → uint64
   I-confluent: YES
   Proof: Aggregation query over CRDT state. Returns eventually-consistent
   result. Different replicas may return different values during convergence
   but each individual read is consistent with that replica's state.

3. OptimisticDelta(entity, resource_type, delta) → void
   I-confluent: YES (with caveat)
   Proof: PN-Counter increment/decrement. CRDTs guarantee convergence via
   commutativity. CAVEAT: optimistic deltas may show balances that are
   invalidated at EABS settlement. This is acceptable because optimistic
   reads are explicitly non-binding (Section 2.1 of Part 1).

4. PendingStateQuery(entity) → Vec<PendingState>
   I-confluent: YES
   Proof: Read-only set query. Pending states are added via EABS (write-path)
   and replicated via CRDT. Queries return the last-known replicated set.

NON-I-CONFLUENT OPERATIONS (must go through EABS):
   - Transfer, InitiatePending, CompletePending, TimeoutPending
   - Slash, Mint, Burn
   - Any operation that could violate conservation if executed concurrently
```

## 9.6 Interaction with Slashing

Slashing and conservation must interact atomically — a slash that removes value from one entity must simultaneously redistribute it (to treasury, reporter) or burn it, within the same EABS batch operation.

```
function atomic_slash(
    violator: EntityID,
    amount: Decimal(18,8),
    resource_type: ResourceType,
    reporter: EntityID
) -> Vec<Operation>:
    // Generate a set of operations that are processed atomically in EABS
    ops = []

    burn_amount = amount × 0.50
    treasury_amount = amount × 0.30
    reporter_amount = amount × 0.20

    // Verify: burn + treasury + reporter = amount (no rounding loss)
    remainder = amount - burn_amount - treasury_amount - reporter_amount
    treasury_amount += remainder  // Any rounding dust goes to treasury

    ops.push(Deduct(violator, amount, resource_type))
    ops.push(Credit(TREASURY_ENTITY, treasury_amount, resource_type))
    ops.push(Credit(reporter, reporter_amount, resource_type))
    ops.push(ReduceSupply(burn_amount, resource_type))  // Burn

    // These operations are tagged as ATOMIC_GROUP — EABS processes all or none
    RETURN AtomicGroup(ops)
```

## 9.7 CSO Lifecycle State Machine

```
CSO_State := ENUM {
    PROPOSED,    // CSO creation submitted, awaiting governance approval
    ACTIVE,      // CSO is live, capacity available in market
    RELEASING,   // CSO is winding down, no new allocations, existing honored
    RELEASED,    // CSO fully wound down, all capacity returned
    SUSPENDED    // CSO suspended due to violation, capacity frozen
}

Transitions:
    PROPOSED → ACTIVE       (G-class governance approval + provider deposit)
    PROPOSED → RELEASED     (G-class governance rejection)
    ACTIVE → RELEASING      (Provider-initiated wind-down OR governance-triggered)
    ACTIVE → SUSPENDED      (Violation detected — capacity frozen pending resolution)
    RELEASING → RELEASED    (All outstanding allocations expired or returned)
    SUSPENDED → ACTIVE      (Governance appeal successful)
    SUSPENDED → RELEASING   (Governance confirms violation — forced wind-down)

struct CSO {
    id:               CSOID,
    provider:         EntityID,
    resource_type:    ResourceType,
    total_capacity:   uint64,
    allocated:        uint64,
    state:            CSO_State,
    created_epoch:    EpochID,
    deposit:          Decimal(18,8),    // Provider's good-faith deposit
    deposit_rate:     Decimal(5,4),     // 10% of capacity value
    violations:       uint32,
    last_state_change: EpochID,
}

INVARIANT CSO-ALLOC:
    ∀ CSO c: c.allocated ≤ c.total_capacity
    ∀ CSO c WHERE c.state == RELEASING: c.allocated monotonically decreasing
    ∀ CSO c WHERE c.state == SUSPENDED: c.allocated frozen (no new allocations, no releases)
```

---

# Section 10: Graduated Slashing System

## 10.1 Design Principles

The slashing system enforces accountability by imposing escalating economic penalties for protocol violations. It must satisfy three properties:

1. **Determinism.** Given the same violation history, every node computes the same penalty. (Required by EABS.)
2. **Monotonicity.** An entity's violation count never decreases (except via governance appeal). Penalties escalate with history.
3. **Proportionality.** Penalty severity matches violation severity and frequency. First-time minor violations receive warnings; repeated or severe violations receive escalating economic consequences.

## 10.2 EABS Processing

All slashing is processed through EABS with deterministic ordering, resolving Attack 7 (Slashing Ordering Attack) from the Adversarial Report.

```
function process_slashing(epoch_batch: EpochBatch) -> Vec<SlashingOutcome>:
    // Step 1: Extract all violation reports from the batch
    violations = epoch_batch.operations
        .filter(|op| op.type == ViolationReport)

    // Step 2: Canonical sort — DETERMINISTIC
    violations.sort_by(|v| (
        v.violation_type.canonical_order(),    // Primary: violation type enum order
        HASH(v.detection_timestamp),           // Secondary: hash of timestamp (not timestamp itself)
        v.violator_id                          // Tertiary: entity ID
    ))

    // Step 3: Process in order, updating violation counts as we go
    outcomes = []
    FOR v IN violations:
        entity_state = get_violation_state(v.violator_id)

        // Determine offense number (monotonic counter)
        offense_number = entity_state.violation_count + 1

        // Validate the violation report
        IF NOT validate_violation(v):
            outcomes.push(SlashingOutcome::Rejected(v, "Invalid violation report"))
            CONTINUE

        // Determine penalty based on schedule
        penalty = compute_penalty(offense_number, v.violation_type, v.violator_id)

        // Apply penalty atomically
        slash_ops = atomic_slash(v.violator_id, penalty.amount, penalty.resource_type, v.reporter_id)
        outcomes.push(SlashingOutcome::Applied(v, penalty, slash_ops))

        // Update violation state
        entity_state.violation_count = offense_number
        entity_state.last_violation_epoch = current_epoch
        entity_state.violation_history.push(ViolationRecord {
            epoch: current_epoch,
            type: v.violation_type,
            offense_number: offense_number,
            penalty: penalty,
        })

    RETURN outcomes
```

### 10.2.1 Canonical Sort Rationale

The sort key `(violation_type, detection_timestamp_hash, violator_id)` is chosen to ensure:

- **violation_type first:** Groups violations by type, ensuring that if an entity has multiple concurrent violations of different types, the ordering is deterministic regardless of detection order.
- **detection_timestamp_hash second:** Uses the HASH of the timestamp, not the timestamp itself. This prevents an attacker from choosing timestamps to influence ordering. The hash is effectively random relative to the violation content.
- **violator_id third:** Final tiebreaker for determinism. Two violations of the same type with the same timestamp hash (astronomically unlikely but must be handled) are ordered by entity ID.

## 10.3 Slashing Schedule

```
struct SlashingSchedule {
    offenses: [
        SlashLevel {
            offense_number: 1,
            penalty_rate: 0.01,         // 1% of staked AIC
            additional_action: "Warning emitted to entity",
            capability_impact: NONE,
        },
        SlashLevel {
            offense_number: 2,
            penalty_rate: 0.05,         // 5%
            additional_action: "Entity flagged for monitoring",
            capability_impact: NONE,
        },
        SlashLevel {
            offense_number: 3,
            penalty_rate: 0.15,         // 15%
            additional_action: "Entity's position limits reduced to 10%",
            capability_impact: "capability_score *= 0.8",
        },
        SlashLevel {
            offense_number: 4,
            penalty_rate: 0.50,         // 50%
            additional_action: "Capability score reset to 1.0",
            capability_impact: "capability_score = 1.0 (hard reset)",
        },
        SlashLevel {
            offense_number: 5,
            penalty_rate: 1.00,         // 100%
            additional_action: "Permanent exclusion (governance appeal possible)",
            capability_impact: "Entity banned from all markets and settlement",
        },
    ]
}
```

### 10.3.1 Penalty Computation

```
function compute_penalty(
    offense_number: uint32,
    violation_type: ViolationType,
    violator_id: EntityID
) -> Penalty:

    // Base penalty from schedule
    schedule_level = MIN(offense_number, 5)  // Cap at level 5
    base_rate = SLASHING_SCHEDULE[schedule_level].penalty_rate

    // Violation type severity multiplier
    severity = violation_type.severity_multiplier()
    // scheduling_violation: 1.0x
    // verification_fraud: 1.5x
    // communication_abuse: 0.8x
    // governance_manipulation: 2.0x
    // cso_breach: 1.2x

    // Compute penalty amount
    staked_aic = get_staked_aic(violator_id)
    penalty_amount = staked_aic × base_rate × severity

    // Cap: penalty cannot exceed entity's total staked AIC
    penalty_amount = MIN(penalty_amount, staked_aic)

    // Additional actions
    additional = SLASHING_SCHEDULE[schedule_level].additional_action
    capability_impact = SLASHING_SCHEDULE[schedule_level].capability_impact

    RETURN Penalty {
        amount: penalty_amount,
        resource_type: AIC,
        additional_action: additional,
        capability_impact: capability_impact,
        offense_number: offense_number,
        violation_type: violation_type,
    }
```

## 10.4 Violation Types

```
ViolationType := ENUM {
    SCHEDULING_VIOLATION,       // Failed to execute assigned tasks, missed deadlines
    VERIFICATION_FRAUD,         // Submitted false verification attestations
    COMMUNICATION_ABUSE,        // Spam, protocol violations, ASV non-compliance
    GOVERNANCE_MANIPULATION,    // Vote buying, proposal spam, constitutional violation
    CSO_BREACH,                 // Capacity non-delivery, conservation violation attempt
}

impl ViolationType {
    function severity_multiplier(self) -> Decimal(3,2):
        MATCH self:
            SCHEDULING_VIOLATION    => 1.0   // Baseline
            VERIFICATION_FRAUD      => 1.5   // Undermines trust infrastructure
            COMMUNICATION_ABUSE     => 0.8   // Lower impact per incident
            GOVERNANCE_MANIPULATION => 2.0   // Threatens system integrity
            CSO_BREACH              => 1.2   // Economic infrastructure damage

    function canonical_order(self) -> uint8:
        MATCH self:
            SCHEDULING_VIOLATION    => 0
            VERIFICATION_FRAUD      => 1
            COMMUNICATION_ABUSE     => 2
            GOVERNANCE_MANIPULATION => 3
            CSO_BREACH              => 4

    function evidence_requirements(self) -> Vec<EvidenceType>:
        MATCH self:
            SCHEDULING_VIOLATION => [
                TaskAssignmentRecord,   // Proof task was assigned
                DeadlineRecord,         // Proof deadline passed
                NonCompletionProof,     // Proof task was not completed
            ]
            VERIFICATION_FRAUD => [
                AttestationRecord,      // The false attestation
                GroundTruthRecord,      // What the correct result was
                DiscrepancyProof,       // Formal proof of mismatch
            ]
            COMMUNICATION_ABUSE => [
                MessageLog,             // The abusive messages
                ProtocolSpec,           // Which protocol rule was violated
                PatternAnalysis,        // Evidence of systematic abuse
            ]
            GOVERNANCE_MANIPULATION => [
                VoteRecord,             // The manipulated votes
                CorrelationAnalysis,    // Evidence of coordination
                ConstitutionalReference, // Which constitutional rule was violated
            ]
            CSO_BREACH => [
                CSORecord,              // The CSO in question
                DeliveryLog,            // What was supposed to be delivered
                ShortfallProof,         // Evidence of non-delivery
            ]
}
```

## 10.5 Appeal Mechanism

```
struct SlashingAppeal {
    appeal_id:          AppealID,
    original_violation: ViolationID,
    appellant:          EntityID,
    bond:               Decimal(18,8),    // 10% of slashed amount
    filed_epoch:        EpochID,
    deadline_epoch:     EpochID,          // filed_epoch + 10
    evidence:           Vec<Evidence>,
    status:             AppealStatus,
}

AppealStatus := ENUM {
    FILED,        // Bond posted, evidence submitted
    REVIEWING,    // Governance committee assigned
    UPHELD,       // Original slash stands, bond forfeited
    OVERTURNED,   // Slash reversed, bond returned, penalty returned
    EXPIRED,      // No decision within 10 epochs — defaults to UPHELD
}

PROTOCOL Appeal:
    Step 1: Appellant posts bond = 10% of slashed amount via EABS
    Step 2: Appeal enters G-class governance queue
    Step 3: Governance committee (randomly selected, 5 members, capability-weighted) reviews evidence
    Step 4: Committee votes (simple majority)
        IF UPHELD:
            Bond forfeited (50% burned, 30% treasury, 20% original reporter)
            Original penalty stands
        IF OVERTURNED:
            Bond returned to appellant
            Slashed amount returned to appellant
            Violation count decremented by 1
            Reporter loses reporter_reward and receives a COMMUNICATION_ABUSE violation flag
    Step 5: Decision recorded in EABS batch as G-class settlement

    TIMEOUT: If no decision within 10 epochs, appeal defaults to UPHELD
             (prevents griefing via endless appeals)
```

## 10.6 Slashing Revenue Distribution

```
RULE SLASH-DIST: Slashing Revenue Distribution
    FOR EACH slash penalty P:
        burn_amount     = P.amount × 0.50    // Burned — reduces total supply
        treasury_amount = P.amount × 0.30    // Treasury — funds public goods
        reporter_amount = P.amount × 0.20    // Reporter — incentivizes detection

    INVARIANT: burn_amount + treasury_amount + reporter_amount = P.amount
    (Rounding dust assigned to treasury)

Distribution Rationale:
    50% BURN: Deflationary pressure. Prevents slashing from being merely redistributive
              (which could incentivize false accusations for profit). The burn ensures that
              slashing is net-destructive to the system's token supply, creating a real
              economic cost for violations.

    30% TREASURY: Funds public goods (bootstrap capacity, development grants, emergency
                  reserve). Ensures the protocol benefits from enforcement.

    20% REPORTER: Incentivizes violation detection. Without reporter rewards, rational
                  agents have no incentive to spend effort detecting and reporting violations.
                  Capped at 20% to prevent "slashing bounty hunting" from becoming more
                  profitable than productive work.

Anti-Gaming:
    Reporter reward is ONLY paid if the violation is confirmed by EABS processing.
    False reports are themselves a COMMUNICATION_ABUSE violation.
    Reporter must post evidence meeting the violation type's evidence_requirements.
    Reporter cannot be the same entity (or in the same Sentinel Graph cluster) as the violator.
```

## 10.7 Cross-Entity Slashing for Collusion

```
struct CollusionSlash {
    cluster_id:      SentinelClusterID,
    entities:        Vec<EntityID>,
    evidence_source: "Sentinel Graph analysis from C3",
    violation_type:  GOVERNANCE_MANIPULATION,  // Collusion is a governance violation
    penalty_model:   "Joint and several — each entity slashed for full cluster penalty"
}

function detect_and_slash_collusion(sentinel_alert: SentinelClusterAlert):
    cluster = sentinel_alert.cluster
    evidence = sentinel_alert.evidence

    // Verify the cluster represents actual collusion, not coincidence
    IF evidence.confidence < 0.90:
        RETURN  // Insufficient confidence — do not slash

    // Compute cluster-level violation
    // If the cluster as a whole violated position limits (POS-2), each member is liable
    FOR entity IN cluster.entities:
        // Each entity's offense count increments independently
        report = ViolationReport {
            violator_id: entity,
            violation_type: GOVERNANCE_MANIPULATION,
            evidence: evidence,
            reporter_id: SENTINEL_SYSTEM_ID,  // System-generated report
            detection_timestamp: current_timestamp(),
        }
        SUBMIT report to EABS batch

    // Additionally: cluster position limit enforcement
    // Excess capacity allocated to the cluster is reclaimed
    excess = effective_position(cluster) - 0.15 × total_supply
    IF excess > 0:
        // Reclaim pro-rata from cluster members
        FOR entity IN cluster.entities:
            entity_share = allocated(entity) / effective_position(cluster)
            reclaim_amount = excess × entity_share
            SUBMIT Reclaim(entity, reclaim_amount) to EABS batch
```

## 10.8 Formal Properties

**Property SLASH-DET (Determinism):**
For any two honest nodes A and B processing the same epoch batch:
```
slashing_outcomes_A(batch) = slashing_outcomes_B(batch)
```
*Proof:* Both nodes sort violations using the same canonical sort key. Both apply the same penalty function. Both read from the same pre-epoch state (EABS guarantees state agreement at epoch boundaries). Therefore outputs are identical. ∎

**Property SLASH-MON (Monotonicity):**
For any entity E, violation_count(E) is monotonically non-decreasing across epochs:
```
∀ epochs E1 < E2: violation_count(E, E1) ≤ violation_count(E, E2)
```
*Exception:* Successful appeal decrements by 1. This is the ONLY decrement path, and it requires G-class governance settlement.
*Proof:* violation_count is incremented in EABS processing and never decremented except by appeal. EABS is append-only for violation state. ∎

**Property SLASH-PROP (Proportionality):**
```
∀ violations V1, V2 of entity E:
    IF V1.offense_number < V2.offense_number:
        penalty(V1) ≤ penalty(V2)  (for same violation type)

    IF V1.violation_type.severity < V2.violation_type.severity:
        penalty(V1) ≤ penalty(V2)  (for same offense number)
```
*Proof:* penalty = staked_aic × base_rate(offense_number) × severity(violation_type). base_rate is monotonically increasing in offense_number. severity is a fixed multiplier per type. Product preserves monotonicity in each factor. ∎

---

# Section 11: Treasury and Governance

## 11.1 Treasury-First Issuance Model

All AIC enters circulation through the treasury. There is no mining, no staking reward generation outside treasury authorization, and no mechanism by which any entity can create AIC. This design eliminates an entire class of inflation attacks and ensures that all economic activity is traceable to governance-authorized issuance.

```
struct Treasury {
    balance:              Decimal(18,8),
    total_issued:         Decimal(18,8),    // Lifetime cumulative issuance
    total_burned:         Decimal(18,8),    // Lifetime cumulative burns (from slashing)
    circulating_supply:   Decimal(18,8),    // total_issued - total_burned - balance
    allocation_budgets:   Map<AllocationCategory, Decimal(18,8)>,
    constitutional_caps:  ConstitutionalCaps,
    pending_proposals:    Vec<GovernanceProposal>,
}

INVARIANT TREASURY-CONS:
    treasury.balance + circulating_supply + total_burned = total_issued
    WHERE circulating_supply = Σ_{i ∈ all_entities, i ≠ treasury} alloc(i, AIC)
```

### 11.1.1 Issuance Protocol

```
PROTOCOL Issuance:
    TRIGGER: G-class governance proposal approved

    Step 1: Governance proposal specifies:
        - amount: Decimal(18,8)         // AIC to mint
        - category: AllocationCategory  // Purpose
        - schedule: IssuanceSchedule    // Immediate or vesting

    Step 2: Constitutional cap check
        IF total_issued + amount > constitutional_caps.max_total_supply:
            REJECT "Would exceed maximum total supply cap"
        IF amount > constitutional_caps.max_single_issuance:
            REJECT "Exceeds single-issuance cap"
        IF issuance_this_quarter + amount > constitutional_caps.quarterly_cap:
            REJECT "Would exceed quarterly issuance cap"

    Step 3: Mint to treasury
        treasury.balance += amount
        treasury.total_issued += amount
        treasury.allocation_budgets[category] += amount

    Step 4: Distribution (per schedule)
        IF schedule == IMMEDIATE:
            Distribute per allocation rules in next EABS batch
        IF schedule == VESTING:
            Create vesting schedule with linear unlock over specified epochs
```

## 11.2 Constitutional Protections

Constitutional protections are parameters that CANNOT be changed by normal governance. They require a supermajority constitutional amendment process.

```
struct ConstitutionalCaps {
    // Supply caps
    max_total_supply:        Decimal(18,8),  // Absolute ceiling on total AIC ever issued
    quarterly_issuance_cap:  Decimal(18,8),  // Max new AIC per governance quarter (50 epochs)
    max_single_issuance:     Decimal(18,8),  // Max AIC in a single governance proposal

    // Spending limits
    max_treasury_spend_per_epoch: Decimal(18,8),  // Treasury cannot disburse more per epoch
    emergency_reserve_floor:      Decimal(18,8),  // Treasury balance must stay above this

    // Governance protections
    supermajority_threshold:  Decimal(3,2),  // 0.67 — required for constitutional changes
    amendment_cooling_period: uint32,         // 20 epochs between amendment proposal and vote
    max_parameter_change_rate: Decimal(3,2), // 0.20 — no parameter can change by >20% per governance cycle

    // Slashing protections
    max_single_slash_rate:    Decimal(3,2),  // 1.00 — can slash up to 100% (5th offense)
    min_appeal_window:        uint32,         // 10 epochs — cannot be shortened
}

INVARIANT CONST-1: Constitutional Immutability
    Constitutional caps may ONLY be modified by:
        1. Supermajority vote (≥ 67% of effective stake)
        2. After a cooling period of 20 epochs from proposal
        3. With a maximum change rate of 20% per amendment
    Any attempt to modify constitutional caps outside this process is a
    GOVERNANCE_MANIPULATION violation → immediate slashing.
```

### 11.2.1 Constitutional Amendment Process

```
PROTOCOL ConstitutionalAmendment:
    Phase 1 — PROPOSAL (1 epoch):
        Proposer submits amendment with:
            - parameter: ConstitutionalParam
            - current_value: current setting
            - proposed_value: new setting
            - rationale: text
            - bond: 5% of treasury balance (significant commitment)
        REQUIRE |proposed_value - current_value| / current_value ≤ 0.20
        EMIT AmendmentProposed event

    Phase 2 — COOLING (20 epochs):
        No voting occurs. Community deliberation period.
        Proposer may withdraw (bond returned minus 1% fee).
        Counter-proposals may be filed (each with own bond).

    Phase 3 — VOTING (5 epochs):
        Eligible voters: all entities with effective_stake > 0
        Vote weight: effective_stake (AIC_collateral × capability_score)
        Options: FOR, AGAINST, ABSTAIN (abstain does not count toward quorum)
        Quorum: 50% of total effective stake must vote
        Threshold: 67% of voting stake must vote FOR

    Phase 4 — EXECUTION (1 epoch delay):
        IF passed:
            Parameter updated in next EABS G-class settlement
            Proposer bond returned in full
            EMIT AmendmentRatified event
        IF failed:
            Proposer bond forfeited (50% burned, 50% treasury)
            EMIT AmendmentRejected event
```

## 11.3 Governance Parameter Taxonomy

Parameters are classified into three tiers based on their impact and the process required to change them:

```
TIER 1 — CONSTITUTIONAL (supermajority amendment required):
    max_total_supply
    quarterly_issuance_cap
    supermajority_threshold
    amendment_cooling_period
    min_appeal_window
    slashing_schedule (offense thresholds)
    four_stream_weights (40/40/10/10 split)
    budget_type_definitions (SB/PC/CS existence and purpose)

TIER 2 — GOVERNANCE (simple majority G-class required):
    epoch_duration
    pc_decay_rate (currently 10%)
    cs_position_limit (currently 15%)
    capability_score_cap (currently 3.0)
    reserve_pricing_floors
    challenge_bond_rate (currently 5%)
    pending_timeout_duration (currently 3 epochs)
    pending_collateral_rate (currently 5%)
    pending_volume_caps (currently 10% per-entity, 25% global)
    use_it_or_lose_it_threshold (currently 70%)
    tranche_split (currently 60/20/20)
    npv_discount_rate (currently 0.2% per epoch)
    cross_epoch_smoothing_limit (currently 25%)
    bootstrap_sunset_conditions
    treasury_allocation_budgets

TIER 3 — OPERATIONAL (automated or admin-adjusted):
    epoch_boundary_jitter_seed
    deterministic_sort_tiebreak_seeds
    monitoring_alert_thresholds
    log_verbosity_levels
    CRDT_replication_intervals
    EABS_batch_size_limits
```

## 11.4 Treasury Allocation Categories

```
AllocationCategory := ENUM {
    SETTLEMENT_REWARDS,    // Funds the four-stream settlement pools
    BOOTSTRAP_CAPACITY,    // Funds the CPLR during bootstrap phase
    DEVELOPMENT_GRANTS,    // Funds development of system improvements
    EMERGENCY_RESERVE,     // Buffer for unexpected system needs
}

struct AllocationPolicy {
    target_split: {
        SETTLEMENT_REWARDS: 0.60,   // 60% of treasury disbursements
        BOOTSTRAP_CAPACITY: 0.15,   // 15% (decreases as bootstrap sunsets)
        DEVELOPMENT_GRANTS: 0.10,   // 10%
        EMERGENCY_RESERVE:  0.15,   // 15% (minimum floor — constitutionally protected)
    },

    // Settlement rewards sub-allocation follows four-stream weights:
    settlement_sub_split: {
        scheduling_compliance:    0.40,
        verification_quality:     0.40,
        communication_efficiency: 0.10,
        governance_participation:  0.10,
    },

    adjustment_rules: {
        // BOOTSTRAP_CAPACITY allocation automatically reduces as bootstrap sunsets
        // Freed allocation shifts to SETTLEMENT_REWARDS
        post_bootstrap: {
            SETTLEMENT_REWARDS: 0.70,
            BOOTSTRAP_CAPACITY: 0.00,
            DEVELOPMENT_GRANTS: 0.15,
            EMERGENCY_RESERVE:  0.15,
        }
    }
}
```

## 11.5 Governance Voting

### 11.5.1 Vote Weight Calculation

```
function compute_vote_weight(entity: EntityID) -> Decimal(18,8):
    staked_aic = get_staked_aic(entity)
    cap_score = get_capability_score(entity)  // 1.0 to 3.0

    // Vote weight = staked AIC × capability multiplier
    // Capability multiplier is SQRT of capability_score for governance
    // (reduced from full multiplier to limit reputation influence on governance)
    governance_multiplier = SQRT(cap_score)  // Range: 1.0 to 1.73

    RETURN staked_aic × governance_multiplier
```

**Rationale for SQRT:** In settlement (Section 4 of Part 1), the full capability_score multiplier (up to 3.0) applies because settlement rewards should favor capable agents. In governance, a reduced multiplier (SQRT, up to 1.73) is used because governance should be more stake-weighted — the entities with the most economic skin in the game should have proportionally more say in parameter decisions, and reputation amplification should be bounded to prevent governance capture by high-reputation, low-stake entities.

### 11.5.2 Voting Protocol

```
PROTOCOL GovernanceVote:
    proposal_types: [ParameterChange, TreasuryAllocation, ConstitutionalAmendment, EmergencyAction]

    FOR ParameterChange:
        quorum: 30% of total effective governance weight
        threshold: 50% + 1 of voting weight (simple majority)
        voting_period: 3 epochs
        execution_delay: 1 epoch
        cooldown: parameter cannot be changed again for 10 epochs

    FOR TreasuryAllocation:
        quorum: 30% of total effective governance weight
        threshold: 50% + 1
        voting_period: 3 epochs
        execution_delay: 1 epoch
        per_allocation_cap: 5% of treasury balance

    FOR ConstitutionalAmendment:
        (See Section 11.2.1 — supermajority process)

    FOR EmergencyAction:
        quorum: 40% of total effective governance weight
        threshold: 60% of voting weight
        voting_period: 1 epoch (expedited)
        execution_delay: 0 (immediate)
        scope: limited to predefined emergency actions:
            - Pause settlement (halt EABS processing)
            - Activate emergency capacity (treasury-funded)
            - Freeze entity (suspected active attack)
            - Rollback last epoch (if conservation violation detected)
        auto_expiry: emergency actions expire after 5 epochs unless renewed
```

## 11.6 Parameter Adjustment Procedures with Sensitivity Analysis

For each Tier 2 governance-tunable parameter, the following template applies:

```
struct ParameterSensitivity {
    parameter:          String,
    current_value:      Decimal,
    sensitivity_at_2x:  String,    // What breaks if parameter doubles
    sensitivity_at_05x: String,    // What breaks if parameter halves
    safe_range:         (Decimal, Decimal),  // Min, Max before system instability
    adjustment_rate:    Decimal,   // Max change per governance cycle
}
```

### Key Parameter Sensitivities:

```
Parameter: epoch_duration
    Current: governance-set (target: 10 minutes for 1K agents)
    At 2x (20 min): Settlement latency doubles. Capital efficiency drops.
                     Capacity market clearing becomes stale. Acceptable for low activity.
    At 0.5x (5 min): EABS batch overhead increases. Reliable broadcast may not
                      complete within epoch. Risk of epoch-skip failures.
    Safe range: [5 min, 30 min] for 1K agents
    Adjustment rate: ±25% per governance cycle

Parameter: pc_decay_rate
    Current: 10% per epoch
    At 2x (20%): Aggressive decay. Agents must constantly earn PCs. May throttle
                  legitimate low-activity agents. Stronger spam protection.
    At 0.5x (5%): Slow decay. PC accumulation possible. Burst capacity increases.
                   Spam protection weakened. PC hoarding becomes viable.
    Safe range: [3%, 25%] per epoch
    Adjustment rate: ±5 percentage points per governance cycle

Parameter: cs_position_limit
    Current: 15%
    At 2x (30%): Market concentration increases. Cornering becomes easier.
                  Only need ~4 colluding entities to control majority.
    At 0.5x (7.5%): Market fragmentation. May prevent efficient large-scale
                     resource allocation. Increases transaction count.
    Safe range: [5%, 25%]
    Adjustment rate: ±5 percentage points per governance cycle

Parameter: capability_score_cap
    Current: 3.0
    At 2x (6.0): Reputation becomes dominant over AIC collateral. Reputation
                  laundering becomes 2x more profitable. Security model weakens.
    At 0.5x (1.5): Capability differences almost irrelevant. Reduces incentive
                    for quality work. System becomes pure stake-weighted.
    Safe range: [1.5, 5.0]
    Adjustment rate: ±0.5 per governance cycle

Parameter: slashing rates (1st offense)
    Current: 1%
    At 2x (2%): Slightly harsher. May deter marginal participants who fear
                 accidental violations. Stronger deterrence.
    At 0.5x (0.5%): Weak deterrence. Cost of violation may be below cost of compliance.
                      Rational agents may choose to violate and absorb the penalty.
    Safe range: [0.5%, 5%] for 1st offense
    Adjustment rate: ±1 percentage point per governance cycle
```

## 11.7 G-Class Settlement for Governance Decisions

```
function settle_governance(epoch: EpochID, governance_batch: Vec<GovernanceDecision>):
    FOR decision IN governance_batch:
        MATCH decision.type:
            ParameterChange(param, new_value):
                // Validate: parameter is Tier 2, change within adjustment_rate
                REQUIRE param.tier == 2
                REQUIRE |new_value - param.current| / param.current <= param.adjustment_rate
                // Apply at next epoch boundary
                SCHEDULE param.set(new_value) AT epoch + 1
                EMIT ParameterChanged(param, old_value, new_value, epoch + 1)

            TreasuryAllocation(category, amount):
                REQUIRE amount <= treasury.balance × 0.05
                REQUIRE treasury.balance - amount >= constitutional_caps.emergency_reserve_floor
                treasury.allocation_budgets[category] += amount
                treasury.balance -= amount
                EMIT TreasuryAllocated(category, amount, epoch)

            ConstitutionalAmendment(param, new_value):
                // Already validated by amendment process (Section 11.2.1)
                param.set(new_value)
                EMIT ConstitutionalAmended(param, old_value, new_value, epoch)

            EmergencyAction(action):
                EXECUTE action
                SCHEDULE action.expiry AT epoch + 5
                EMIT EmergencyActivated(action, epoch, expiry=epoch+5)
```

---

# Section 12: Integration Contracts

This section specifies the exact data flows, frequencies, consistency guarantees, failure handling, and API surfaces for DSF's integration with each upstream and downstream layer.

## 12.1 C3 (Tidal Noosphere) Integration

The Tidal Noosphere is DSF's substrate — DSF runs within the Noosphere's locus/parcel architecture. This is the deepest integration.

### 12.1.1 AIC Ledger Maintenance

```
Integration: AIC Ledger Replication
    Direction: DSF → C3 (ledger state replicated across loci)
    Mechanism: CRDT read-path replication via C3's CRDT infrastructure

    Data Flow:
        Source: DSF EABS settled state (per-epoch)
        Transport: C3 PN-Counter CRDT replication
        Destination: Each locus maintains a local read-replica of AIC balances

    struct AICLedgerReplica {
        entity_balances:   Map<EntityID, Decimal(18,8)>,  // AIC balances
        pc_balances:       Map<EntityID, Decimal(18,8)>,  // Protocol Credit balances
        cs_allocations:    Map<EntityID, Map<ResourceType, uint64>>,  // CS allocations
        last_settled_epoch: EpochID,
        optimistic_deltas:  Vec<OptimisticDelta>,  // Current-epoch uncommitted changes
    }

    Consistency Guarantee:
        - Settled state (last_settled_epoch): STRONG — identical across all loci after
          EABS settlement propagation (bounded by reliable broadcast latency)
        - Optimistic deltas: EVENTUAL — CRDT convergence, may differ across loci during epoch

    Frequency:
        - EABS settled state: once per epoch (at epoch boundary)
        - Optimistic deltas: continuous (CRDT merge on every inter-locus sync)

    Failure Handling:
        IF a locus fails to receive EABS settled state for epoch E:
            - Locus operates on last known settled state (epoch E-1) + optimistic deltas
            - Locus marks itself as STALE for settlement purposes
            - STALE loci cannot process write-path operations until resynchronized
            - Resynchronization: request settled state for missed epochs from any non-stale locus
            - Maximum staleness tolerance: 3 epochs. After 3 epochs stale, locus enters
              DEGRADED mode (read-only, no new task assignments)
```

### 12.1.2 Deterministic Settlement: Per-Locus with Cross-Locus Reconciliation

```
Integration: EABS Settlement Execution
    Direction: Bidirectional (C3 provides substrate, DSF provides settlement logic)

    Architecture:
        Each locus runs its own EABS instance for intra-locus operations.
        Cross-locus operations (transfers between entities in different loci)
        are processed by a cross-locus reconciliation layer.

    struct PerLocusEABS {
        locus_id:          LocusID,
        epoch_batch:       EpochBatch,       // Operations originating in this locus
        local_state:       LocusSettlementState,
        cross_locus_ops:   Vec<CrossLocusOp>,  // Operations requiring multi-locus settlement
    }

    struct CrossLocusReconciliation {
        epoch:             EpochID,
        participating_loci: Vec<LocusID>,
        cross_locus_batch:  Vec<CrossLocusOp>,
        reconciliation_result: ReconciliationState,
    }

    Protocol:
        Phase 1 — Local Settlement (within each locus):
            Each locus EABS processes its local epoch batch
            Cross-locus operations are DEFERRED to Phase 2
            Local conservation invariant checked (per-locus)

        Phase 2 — Cross-Locus Collection:
            Each locus submits its cross-locus operations to the reconciliation layer
            Reconciliation layer collects all cross-locus operations into a single batch
            Canonical sort applied to the unified cross-locus batch

        Phase 3 — Cross-Locus Settlement:
            Unified cross-locus batch processed deterministically
            Each locus receives its share of the results
            Cross-locus conservation invariant checked (global)

        Phase 4 — Merge:
            Each locus merges local settlement results with cross-locus results
            Final per-locus state = local_result ⊕ cross_locus_result
            CRDT read-path updated with new settled state

    Timing:
        Phase 1: 0% to 60% of epoch boundary processing window
        Phase 2: 60% to 75%
        Phase 3: 75% to 95%
        Phase 4: 95% to 100%

    Failure Handling:
        IF a locus fails to submit cross-locus operations by Phase 2 deadline:
            - That locus's cross-locus operations are DEFERRED to next epoch
            - Other loci proceed without them
            - Deferred operations are marked with original epoch for ordering
        IF cross-locus reconciliation fails conservation check:
            - All cross-locus operations for this epoch are ROLLED BACK
            - Per-locus settlements still apply (they passed local conservation)
            - Rolled-back operations are retried next epoch with additional logging
```

### 12.1.3 CSO Rebalancing on Tidal Phase Transitions

```
Integration: Tidal Phase → CSO Rebalancing
    Direction: C3 → DSF (C3 triggers, DSF responds)

    Trigger: C3 tidal phase transition (any locus changing tidal phase)

    Data Flow:
        C3 EMITS TidalPhaseTransition {
            locus_id:     LocusID,
            old_phase:    TidalPhase,    // e.g., HIGH_TIDE, LOW_TIDE, NEAP
            new_phase:    TidalPhase,
            epoch:        EpochID,
            affected_parcels: Vec<ParcelID>,
        }

        DSF RECEIVES and processes:
            1. Identify all CSOs affected by the locus transition
            2. Recompute capacity allocations based on new tidal phase
            3. Release over-allocated capacity to next tranche
            4. Queue under-allocated entities for priority rebidding

    struct CSO_Rebalancing {
        trigger:           TidalPhaseTransition,
        affected_csos:     Vec<CSOID>,
        capacity_released: Map<ResourceType, uint64>,
        priority_rebids:   Vec<(EntityID, ResourceType, uint64)>,
    }

    Tidal Phase → Capacity Adjustment Rules:
        HIGH_TIDE (high activity):
            Capacity demand increases. Reserve 10% of available CS for
            spot allocation to handle burst demand.

        LOW_TIDE (low activity):
            Capacity demand decreases. Excess allocations eligible for
            early release. Use-it-or-lose-it threshold relaxed to 50%.

        NEAP (transition):
            No adjustment. Existing allocations continue.
            New allocations processed at standard tranche schedule.

    Frequency: Per tidal phase transition (irregular, driven by C3 tidal function)

    Consistency Guarantee: EABS-settled (rebalancing processed in next epoch batch)
```

### 12.1.4 Sentinel Graph Integration for Sybil Detection

```
Integration: Sentinel Graph → Capability Score / Position Limits
    Direction: C3 → DSF (C3 provides identity clustering, DSF consumes)

    Data Flow:
        C3 Sentinel Graph EMITS:
            SentinelClusterUpdate {
                cluster_id:     SentinelClusterID,
                member_entities: Vec<EntityID>,
                confidence:      Decimal(3,2),     // 0.00 to 1.00
                evidence_type:   EvidenceType,      // BEHAVIORAL, NETWORK, TEMPORAL
                epoch:           EpochID,
            }

        DSF CONSUMES:
            1. Update cluster position limits (POS-2)
            2. Adjust capability_score inputs (reputation diversity check)
            3. If confidence ≥ 0.90: trigger collusion slashing (Section 10.7)

    API Surface:
        DSF → C3: query_cluster(entity_id) → Option<SentinelClusterID>
        DSF → C3: get_cluster_members(cluster_id) → Vec<EntityID>
        C3 → DSF: push_cluster_update(SentinelClusterUpdate)

    Frequency: Asynchronous (C3 pushes updates as clusters are detected/updated)

    Consistency Guarantee: EVENTUAL (CRDT read-path for queries, EABS for enforcement)

    Failure Handling:
        IF Sentinel Graph is unavailable:
            - DSF continues with last known cluster data
            - New entities are treated as singletons (no cluster relationships)
            - Position limits enforced per-entity only (POS-1, not POS-2)
            - EMIT SentinelUnavailable alert to governance
```

## 12.2 C5 (PCVM) Integration

PCVM provides the verification infrastructure that DSF's capability scoring and reward distribution depend on.

### 12.2.1 Verification Rewards

```
Integration: Verification Quality Rewards
    Direction: DSF → C5 verifiers (DSF distributes, C5 verifiers receive)

    Mechanism:
        Treasury funds the verification quality stream (40% of settlement rewards).
        Rewards distributed based on PCVM verification outcomes.

    Data Flow:
        C5 EMITS per-epoch:
            VerificationReport {
                verifier_id:     EntityID,
                claims_verified: uint32,
                accuracy_rate:   Decimal(5,4),
                claim_classes:   Vec<ClaimClass>,    // D/E/S/H/N + P/R/C
                vtds_completed:  uint32,             // Verification Task Descriptors
                epoch:           EpochID,
            }

        DSF PROCESSES:
            1. Aggregate VerificationReports for the epoch
            2. Compute per-verifier quality scores
            3. Distribute verification stream rewards proportionally

    Reward Computation:
        function compute_verification_rewards(
            reports: Vec<VerificationReport>,
            pool: Decimal(18,8)  // Total AIC in verification stream for this epoch
        ) -> Vec<(EntityID, Decimal(18,8))>:

            // Quality score per verifier
            FOR report IN reports:
                // Weight by claim difficulty (higher claim classes → higher weight)
                difficulty_weight = report.claim_classes.map(|c| c.difficulty_weight()).sum()
                // Weight by accuracy (must exceed 70% threshold to receive any reward)
                IF report.accuracy_rate < 0.70:
                    quality_score = 0  // Below threshold — no reward
                ELSE:
                    quality_score = report.accuracy_rate × difficulty_weight × report.vtds_completed

            // Normalize and distribute
            total_quality = Σ quality_scores
            FOR (verifier, score) IN quality_scores:
                reward = pool × (score / total_quality)
                EMIT SettlementCredit(verifier, reward, VERIFICATION_QUALITY)

    Claim Class Difficulty Weights:
        D (Deterministic):  1.0  // Easiest to verify
        E (Empirical):      1.5
        S (Statistical):    2.0
        H (Heuristic):      2.5
        N (Normative):      3.0  // Hardest to verify
        // Modifier: P (Primary) ×1.0, R (Replication) ×0.7, C (Challenge) ×1.3

    Frequency: V-class settlement (every N epochs, default N=5)

    Consistency Guarantee: EABS-settled (verification rewards are write-path operations)

    Failure Handling:
        IF C5 fails to deliver VerificationReports for an epoch:
            - Verification stream rewards for that epoch are DEFERRED (held in treasury)
            - Deferred rewards distributed in the next epoch with valid reports
            - Maximum deferral: 3 epochs. After 3 epochs without reports, rewards are
              redistributed to other streams proportionally
```

### 12.2.2 Credibility → Capability Score Mapping

```
Integration: PCVM Credibility → DSF Capability Score
    Direction: C5 → DSF (C5 provides credibility, DSF consumes for staking)

    Data Flow:
        C5 MAINTAINS per-entity credibility scores:
            CredibilityScore {
                entity_id:            EntityID,
                overall_credibility:  Decimal(5,4),  // 0.0 to 1.0
                by_claim_class:       Map<ClaimClass, Decimal(5,4)>,
                sample_size:          uint32,         // Number of verified claims
                last_updated_epoch:   EpochID,
            }

        DSF MAPS credibility to raw_score.verification_track_record:
            function credibility_to_track_record(cred: CredibilityScore) -> Decimal(5,4):
                // Only count if sufficient sample size
                IF cred.sample_size < 20:
                    RETURN 0.0  // Cold start — no track record credit

                // Weight by claim class diversity
                classes_with_data = cred.by_claim_class.keys().len()
                diversity_factor = MIN(classes_with_data / 3.0, 1.0)  // Need ≥3 classes

                // Base score from overall credibility
                base = cred.overall_credibility

                // Discount for low-value verification (only count high-value)
                // This mapping is the integration point — DSF trusts C5's credibility score
                RETURN base × diversity_factor

    API Surface:
        DSF → C5: get_credibility(entity_id) → CredibilityScore
        C5 → DSF: push_credibility_update(entity_id, CredibilityScore) [per epoch]

    Frequency: Updated per V-class settlement period (every N epochs)

    Consistency Guarantee: CRDT read-path for queries (optimistic), EABS for capability score recalculation

    Failure Handling:
        IF credibility data unavailable:
            - Entity's verification_track_record component frozen at last known value
            - capability_score recalculation skips this component (uses 0.0)
            - Entity's effective_stake computed with capability_score = 1.0 (baseline)
```

### 12.2.3 PC Identity-Binding via PCVM Attestations

```
Integration: PCVM Attestations → Protocol Credit Identity Binding
    Direction: C5 → DSF (C5 provides attestations that prove work was performed by earner)

    Purpose: Prevents PC delegation/farming (Attack 4 and Attack 6 mitigations)

    Data Flow:
        When an entity performs a PC-earning action (task completion, verification):
            C5 generates a VerificationAttestation:
                attestation_id:    AttestationID,
                performer:         EntityID,
                action_type:       ActionType,
                action_hash:       Hash,        // Hash of the action content
                timestamp:         EpochTimestamp,
                pcvm_signature:    Signature,   // PCVM's attestation that performer did the work

        DSF VALIDATES attestation before crediting PCs:
            function validate_pc_earning(action: PCEarningAction, attestation: VerificationAttestation) -> bool:
                // Check attestation matches action
                REQUIRE attestation.performer == action.entity_id
                REQUIRE attestation.action_hash == HASH(action.content)
                // Verify PCVM signature
                REQUIRE VERIFY(attestation.pcvm_signature, PCVM_PUBLIC_KEY)
                // Check freshness (attestation must be from current or previous epoch)
                REQUIRE current_epoch - attestation.timestamp.epoch <= 1
                RETURN true

    Frequency: Per PC-earning action (continuous)

    Consistency Guarantee: Attestation verification is deterministic (signature check).
                           PC credit is EABS-settled.

    Failure Handling:
        IF PCVM attestation service unavailable:
            - PC earning is SUSPENDED (no PCs credited without attestation)
            - Existing PC balances continue to decay (10% per epoch)
            - EMIT PCVMUnavailable alert
            - Resume when attestation service recovers (backfill for missed epochs NOT allowed)
```

### 12.2.4 Claim Class → Settlement Type Mapping

```
Integration: PCVM Claim Classes → DSF Settlement Types
    Direction: Mapping specification (bidirectional understanding)

    Mapping:
        Claim Class → Settlement Type:
            D (Deterministic) → B-class (fast)
                Deterministic claims can be verified quickly; rewards settle per-epoch.

            E (Empirical) → V-class (standard)
                Empirical claims require observation over time; rewards settle every N epochs.

            S (Statistical) → V-class (standard)
                Statistical claims require sample accumulation; V-class settlement.

            H (Heuristic) → V-class (standard)
                Heuristic claims require expert review; V-class settlement.

            N (Normative) → G-class (slow)
                Normative claims involve value judgments; governance-speed settlement.

        Claim Modifier → Settlement Adjustment:
            P (Primary)     → Standard settlement timing
            R (Replication) → Same timing as original claim
            C (Challenge)   → V-class minimum (challenges always need review time)
                              Challenge bond (5%) applies regardless of claim class
```

## 12.3 C6 (EMA) Integration

EMA provides knowledge metabolism — DSF must reward knowledge contributions and integrate with SHREC regulation.

### 12.3.1 Knowledge Contribution Rewards

```
Integration: EMA Knowledge Tasks → Scheduling Compliance Stream
    Direction: C6 → DSF (C6 reports knowledge task outcomes, DSF settles rewards)

    Data Flow:
        C6 EMITS per-epoch:
            KnowledgeContributionReport {
                contributor_id:     EntityID,
                quanta_produced:    uint32,      // Epistemic quanta generated
                quanta_quality:     Decimal(5,4), // SHREC quality assessment
                metabolic_efficiency: Decimal(5,4), // Resource efficiency
                task_class:         TaskClass,
                epoch:              EpochID,
            }

        DSF PROCESSES:
            Knowledge contributions are settled via the scheduling compliance stream (40%).
            Quality-weighted contribution scores determine share of the compliance pool.

    function compute_knowledge_rewards(
        reports: Vec<KnowledgeContributionReport>,
        compliance_pool: Decimal(18,8)
    ) -> Vec<(EntityID, Decimal(18,8))>:

        FOR report IN reports:
            // Score = quantity × quality × efficiency
            contribution_score = report.quanta_produced
                               × report.quanta_quality
                               × report.metabolic_efficiency

        total_score = Σ contribution_scores
        FOR (contributor, score) IN contribution_scores:
            reward = compliance_pool × (score / total_score)
            // Note: compliance pool is shared with non-knowledge scheduling tasks
            // Knowledge tasks compete with other scheduled tasks for this pool
            EMIT SettlementCredit(contributor, reward, SCHEDULING_COMPLIANCE)

    Frequency: B-class settlement (per-epoch)

    Failure Handling:
        IF C6 fails to deliver reports:
            - Knowledge contributions for that epoch receive no reward
            - Compliance pool distributed among other scheduled tasks
            - No backfill (prevents gaming via delayed reporting)
```

### 12.3.2 Metabolic Efficiency → Capacity Market Pricing

```
Integration: EMA Metabolic Efficiency → Capacity Market Information
    Direction: C6 → DSF capacity market (informational, not binding)

    Data Flow:
        C6 PUBLISHES aggregate metabolic efficiency metrics:
            MetabolicEfficiencyReport {
                resource_type:    ResourceType,
                avg_efficiency:   Decimal(5,4),  // Across all knowledge tasks
                marginal_cost:    Decimal(18,8), // Estimated marginal cost per quanta
                demand_forecast:  Decimal(18,8), // Expected demand for next epoch
                epoch:            EpochID,
            }

        DSF Capacity Market USES:
            - demand_forecast informs CPLR capacity offering decisions
            - marginal_cost informs reserve pricing floor governance proposals
            - avg_efficiency used in treasury reporting

    Consistency Guarantee: INFORMATIONAL ONLY — not used in settlement computation.
                           Errors in metabolic reports cannot cause conservation violations.

    Frequency: Per-epoch (published with EABS settlement results)
```

### 12.3.3 SHREC Budget Allocation via Intent-Budgeted Settlement

```
Integration: EMA SHREC Regulation → DSF Intent Budgets
    Direction: Bidirectional (C6 requests budgets, DSF enforces limits)

    SHREC Components:
        S (Stability):  Budget for maintaining existing knowledge quality
        H (Homeostasis): Budget for system equilibrium maintenance
        R (Resilience):  Budget for recovery from knowledge degradation
        E (Evolution):   Budget for new knowledge generation
        C (Complexity):  Budget for managing knowledge interconnections

    Data Flow:
        C6 SUBMITS per-epoch SHREC budget request:
            SHRECBudgetRequest {
                locus_id:       LocusID,
                s_budget:       Decimal(18,8),
                h_budget:       Decimal(18,8),
                r_budget:       Decimal(18,8),
                e_budget:       Decimal(18,8),
                c_budget:       Decimal(18,8),
                total_request:  Decimal(18,8),
                justification:  Hash,  // Reference to SHREC analysis document
            }

        DSF VALIDATES and ALLOCATES:
            function process_shrec_budget(request: SHRECBudgetRequest) -> SHRECBudgetAllocation:
                // Check against locus's SB (Sponsor Budget) availability
                locus_sb = get_sponsor_budget(request.locus_id)
                max_allocation = MIN(request.total_request, locus_sb × 0.30)
                // SHREC cannot consume more than 30% of a locus's sponsor budget

                // Allocate proportionally if capped
                IF max_allocation < request.total_request:
                    scale_factor = max_allocation / request.total_request
                    RETURN SHRECBudgetAllocation {
                        s: request.s_budget × scale_factor,
                        h: request.h_budget × scale_factor,
                        r: request.r_budget × scale_factor,
                        e: request.e_budget × scale_factor,
                        c: request.c_budget × scale_factor,
                    }
                ELSE:
                    RETURN SHRECBudgetAllocation from request (full allocation)

    Frequency: Per-epoch (B-class settlement)
    Consistency Guarantee: EABS-settled (budget allocations are write-path operations)
```

## 12.4 C7 (RIF) Integration

RIF is the orchestration layer — it decomposes high-level intents into executable tasks. DSF must account for intent costs, check stake availability, and process resource return credits.

### 12.4.1 Intent Cost Accounting: Operation Class Mapping

```
Integration: RIF Operation Classes → DSF Settlement Types
    Direction: Specification (shared understanding)

    RIF defines 5 operation classes. Each maps to a DSF settlement type:

    M (Merge/Convergence) → B-class fast settlement
        Cost model: Near-zero marginal cost. PCs consumed for rate limiting.
        Settlement: PC deduction settled per-epoch.
        Typical operations: Signal propagation, CRDT merges, status updates.

    B (Bounded Local Commit) → B-class fast settlement
        Cost model: CS consumption proportional to resource usage.
        Settlement: CS deduction and provider payment per-epoch.
        Typical operations: Task execution within allocated capacity.

    X (Exclusive) → B-class fast settlement (with V-class for disputes)
        Cost model: CS consumption + priority premium.
        Settlement: Standard per-epoch. If disputed, deferred to V-class.
        Typical operations: Lease acquisition, exclusive resource access.

    V (Verification) → V-class standard settlement
        Cost model: Verification effort funded from treasury (not intent budget).
        Settlement: Verifier rewards distributed every N epochs.
        Typical operations: Claim verification, attestation generation.

    G (Governance) → G-class slow settlement
        Cost model: Governance participation rewarded from governance stream.
        Settlement: Slow, governance-triggered.
        Typical operations: Parameter votes, constitutional amendments.
```

### 12.4.2 Intent Resource Bounds → Settlement Budget Ceiling

```
Integration: RIF Intent resource_bounds → DSF Task Budget
    Direction: C7 → DSF (RIF provides bounds, DSF enforces budget)

    Data Flow:
        C7 SUBMITS Intent with resource_bounds:
            IntentSubmission {
                intent_id:        IntentID,
                sponsor_id:       EntityID,
                resource_bounds: {
                    max_compute:     uint64,       // CS units of compute
                    max_storage:     uint64,       // CS units of storage
                    max_bandwidth:   uint64,       // CS units of bandwidth
                    max_aic_cost:    Decimal(18,8), // AIC budget ceiling
                    max_duration:    uint32,        // Epochs until timeout
                },
                decomposition:    Vec<TaskID>,     // Decomposed sub-tasks
                priority:         PriorityClass,
            }

        DSF VALIDATES:
            function validate_intent_budget(intent: IntentSubmission) -> Result<(), BudgetError>:
                sponsor = get_entity(intent.sponsor_id)

                // Check SB availability (optimistic — via CRDT read-path)
                IF sponsor.sb_balance < intent.resource_bounds.max_aic_cost:
                    RETURN Err(InsufficientSponsorBudget)

                // Check minimum bounds (Section 6 of Part 1)
                FOR task IN intent.decomposition:
                    min = get_minimum_bounds(task.task_class)
                    IF task.resource_bounds < min:
                        RETURN Err(BelowMinimumBounds(task.task_class, min))

                // Reserve budget (optimistic — actual deduction at EABS settlement)
                RESERVE intent.resource_bounds.max_aic_cost FROM sponsor.sb_balance
                RETURN Ok(())

    Consistency Guarantee:
        Budget validation: OPTIMISTIC (CRDT read-path) — may approve intents that are
        later rejected at EABS settlement if optimistic balance was stale.
        Budget deduction: EABS-settled — deterministic, conservation-preserving.

    Failure Handling:
        IF optimistic validation approves but EABS settlement rejects (insufficient funds):
            - Intent is CANCELLED
            - All sub-tasks are ABORTED
            - Workers who completed work before cancellation receive minimum_bounds compensation
              from the sponsor's remaining balance (worker protection — Section 6 of Part 1)
            - Sponsor receives a scheduling violation if this occurs repeatedly (>2 times in 10 epochs)
```

### 12.4.3 Stake Availability Check

```
Integration: RIF Stake Check → DSF HDL Read-Path
    Direction: C7 → DSF (RIF queries, DSF responds)

    API Surface:
        function check_stake_availability(entity_id: EntityID) -> StakeAvailability:
            RETURN StakeAvailability {
                staked_aic:       get_staked_aic(entity_id),           // CRDT read (optimistic)
                capability_score: get_capability_score(entity_id),     // CRDT read (optimistic)
                effective_stake:  compute_effective_stake(entity_id),   // Computed
                available_sb:     get_sb_balance(entity_id),           // CRDT read (optimistic)
                available_cs:     get_cs_allocations(entity_id),       // CRDT read (optimistic)
                pc_balance:       get_pc_balance(entity_id),           // CRDT read (optimistic)
                last_settled:     get_last_settled_epoch(),            // Epoch of last EABS settlement
                staleness_warning: current_epoch > last_settled + 1,   // Flag if data may be stale
            }

    Consistency Guarantee: OPTIMISTIC (CRDT read-path)
        RIF should treat all values as estimates. Binding settlement occurs via EABS.
        If staleness_warning is true, RIF should add safety margins to resource estimates.

    Frequency: On-demand (per intent submission and task assignment)

    Failure Handling:
        IF DSF read-path unavailable:
            - RIF queues intent submissions until DSF is available
            - Maximum queue: 100 intents per entity, 1000 globally
            - Queue overflow: oldest intents dropped with RESOURCE_UNAVAILABLE error
```

### 12.4.4 Resource Return Credits

```
Integration: Task Completion → Resource Return Credits
    Direction: C7 → DSF (RIF reports completion, DSF processes returns)

    When a task completes using fewer resources than budgeted, the difference is returned:

    Data Flow:
        C7 SUBMITS per-task:
            TaskCompletionReport {
                task_id:          TaskID,
                intent_id:        IntentID,
                sponsor_id:       EntityID,
                worker_id:        EntityID,
                resource_bounds:  ResourceBounds,    // Original budget
                actual_usage:     ResourceUsage,     // What was actually consumed
                completion_quality: Decimal(5,4),    // Quality assessment (0.0 to 1.0)
                epoch:            EpochID,
            }

        DSF PROCESSES in EABS batch:
            function process_resource_return(report: TaskCompletionReport):
                // Compute unused resources
                compute_unused = report.resource_bounds.max_compute - report.actual_usage.compute
                storage_unused = report.resource_bounds.max_storage - report.actual_usage.storage
                bandwidth_unused = report.resource_bounds.max_bandwidth - report.actual_usage.bandwidth
                aic_unused = report.resource_bounds.max_aic_cost - report.actual_usage.aic_cost

                // Return unused AIC to sponsor's SB
                IF aic_unused > 0:
                    EMIT Credit(report.sponsor_id, aic_unused, AIC)

                // Return unused CS to market (available in next tranche)
                IF compute_unused > 0:
                    EMIT ReleaseCapacity(COMPUTE_STANDARD, compute_unused)
                // ... similarly for storage and bandwidth

                // Compute worker reward based on quality and actual usage
                worker_reward = compute_worker_reward(
                    report.actual_usage.aic_cost,
                    report.completion_quality,
                    report.resource_bounds.max_aic_cost
                )
                EMIT Credit(report.worker_id, worker_reward, AIC)

    Frequency: Per-task completion (processed in B-class EABS settlement)

    Consistency Guarantee: EABS-settled (all credits and debits are write-path operations)
```

### 12.4.5 Intent Lifecycle → Settlement Lifecycle Mapping

```
RIF Intent Lifecycle          DSF Settlement Lifecycle
─────────────────────         ────────────────────────
SUBMITTED                →    Budget reserved (optimistic, read-path)
DECOMPOSED               →    Sub-task budgets validated against minimum bounds
EXECUTING                →    CS consumed per-epoch (B-class settlement)
                               PC consumed for rate-limited operations
PARTIALLY_COMPLETE       →    Completed sub-task rewards settled (B-class)
                               Resource returns for completed sub-tasks
COMPLETED                →    Final settlement batch:
                               - Worker rewards (B-class)
                               - Sponsor refund for unused budget (B-class)
                               - Verification rewards (V-class, deferred)
                               - Quality assessment recorded for capability scores
FAILED                   →    Emergency settlement:
                               - Workers compensated for completed work
                               - Sponsor refunded remaining budget
                               - Failure recorded for sponsor reputation
TIMED_OUT                →    Timeout settlement:
                               - Similar to FAILED
                               - Additional timeout penalty for sponsor if chronic
```

## 12.5 C4 (ASV) Integration

ASV defines the semantic vocabulary for inter-agent communication. DSF must express economic messages in ASV format and define economic claim types.

### 12.5.1 Settlement Messages in ASV Vocabulary

```
Integration: DSF Settlement Messages → ASV Format
    Direction: DSF → C4 (DSF produces messages in ASV vocabulary)

    DSF defines the following ASV message schemas for settlement-related communication:

    ASV Schema: "dsf.settlement.credit"
        {
            "$schema": "https://atrahasis.org/asv/v1/schema",
            "type": "dsf.settlement.credit",
            "properties": {
                "recipient":     { "type": "entity_id" },
                "amount":        { "type": "decimal", "precision": 18, "scale": 8 },
                "currency":      { "enum": ["AIC", "PC", "CS"] },
                "stream":        { "enum": ["SCHEDULING", "VERIFICATION", "COMMUNICATION", "GOVERNANCE"] },
                "epoch":         { "type": "epoch_id" },
                "settlement_class": { "enum": ["B", "V", "G"] },
                "justification": { "type": "hash" }  // Reference to evidence
            }
        }

    ASV Schema: "dsf.settlement.slash"
        {
            "$schema": "https://atrahasis.org/asv/v1/schema",
            "type": "dsf.settlement.slash",
            "properties": {
                "violator":       { "type": "entity_id" },
                "amount":         { "type": "decimal" },
                "violation_type": { "enum": ["SCHEDULING", "VERIFICATION_FRAUD", "COMMUNICATION_ABUSE", "GOVERNANCE_MANIPULATION", "CSO_BREACH"] },
                "offense_number": { "type": "uint32" },
                "evidence":       { "type": "array", "items": { "type": "hash" } },
                "reporter":       { "type": "entity_id" },
                "epoch":          { "type": "epoch_id" }
            }
        }

    ASV Schema: "dsf.market.bid"
        {
            "$schema": "https://atrahasis.org/asv/v1/schema",
            "type": "dsf.market.bid",
            "properties": {
                "bidder":          { "type": "entity_id" },
                "resource_type":   { "enum": ["COMPUTE_STANDARD", "COMPUTE_INTENSIVE", "STORAGE_EPHEMERAL", "STORAGE_PERSISTENT", "BANDWIDTH_INTRA", "BANDWIDTH_CROSS"] },
                "quantity":        { "type": "uint64" },
                "max_price":       { "type": "decimal" },
                "priority_class":  { "enum": ["FIRM", "FLEXIBLE"] },
                "commitment_hash": { "type": "hash" },
                "epoch":           { "type": "epoch_id" }
            }
        }

    ASV Schema: "dsf.governance.vote"
        {
            "$schema": "https://atrahasis.org/asv/v1/schema",
            "type": "dsf.governance.vote",
            "properties": {
                "voter":         { "type": "entity_id" },
                "proposal_id":   { "type": "proposal_id" },
                "vote":          { "enum": ["FOR", "AGAINST", "ABSTAIN"] },
                "weight":        { "type": "decimal" },
                "epoch":         { "type": "epoch_id" },
                "signature":     { "type": "signature" }
            }
        }

    ASV Schema: "dsf.conservation.report"
        {
            "$schema": "https://atrahasis.org/asv/v1/schema",
            "type": "dsf.conservation.report",
            "properties": {
                "epoch":            { "type": "epoch_id" },
                "resource_type":    { "type": "resource_type" },
                "total_supply":     { "type": "decimal" },
                "total_allocated":  { "type": "decimal" },
                "total_pending":    { "type": "decimal" },
                "total_spent":      { "type": "decimal" },
                "conservation_holds": { "type": "boolean" },
                "delta":            { "type": "decimal" }  // Should be 0
            }
        }

    Frequency: Per relevant event (settlement credits per-epoch, slashing per-violation, etc.)

    Consistency Guarantee: Messages are generated from EABS-settled state (authoritative).
```

### 12.5.2 Economic Claim Types for PCVM Verification

```
Integration: DSF Economic Claims → C5 PCVM for Verification
    Direction: DSF → C5 (DSF submits economic claims, C5 verifies)

    Economic claims that require PCVM verification:

    Claim Type: "dsf.claim.conservation"
        Class: D (Deterministic) — verifiable by re-computation
        Content: Conservation invariant holds for epoch E, resource type R
        Verification: Re-run EABS settlement function on the epoch batch
                      and check that LHS = RHS of conservation equation
        VTD: { recompute_settlement(epoch, batch) → check_conservation() }

    Claim Type: "dsf.claim.clearing_price"
        Class: D (Deterministic) — verifiable by re-running auction
        Content: Clearing price for resource R, tranche T, epoch E = P
        Verification: Re-run auction clearing algorithm on sealed bids/offers
        VTD: { recompute_auction(bids, offers, resource, tranche, epoch) → check_price() }

    Claim Type: "dsf.claim.capability_score"
        Class: E (Empirical) — depends on historical data
        Content: Entity X has capability_score Y as of epoch E
        Verification: Recompute from credibility scores, reputation, track record
        VTD: { gather_inputs(entity, epoch) → compute_capability_score() → compare(Y) }

    Claim Type: "dsf.claim.slashing_correctness"
        Class: D (Deterministic) — verifiable by re-processing
        Content: Entity X was correctly slashed amount Y for violation Z
        Verification: Re-process violation through slashing function
        VTD: { replay_slashing(violation, entity_state) → check_penalty(Y) }

    Claim Type: "dsf.claim.market_fairness"
        Class: S (Statistical) — requires statistical analysis
        Content: Capacity market for resource R shows no manipulation indicators
        Verification: Statistical tests on bid/offer distributions, HHI calculation
        VTD: { analyze_market_data(resource, epoch_range) → statistical_tests() }
```

---

# Section 13: Security Analysis

## 13.1 Adversarial Findings and Architectural Resolutions

This section documents all 10 adversarial findings from the Adversarial Report and traces each to its architectural resolution in DSF v2.0.

### Finding 1: Phantom Balance Attack (FATAL → RESOLVED)

**Original severity:** FATAL
**Attack:** Exploiting CRDT partition tolerance to double-spend AIC across network partitions.
**Root cause:** Pure-CRDT ledger cannot enforce global invariants (conservation) without coordination.

**Resolution:** Hybrid Deterministic Ledger (HDL) — Section 2 of Part 1.
- Read-path remains CRDT (fast, partition-tolerant)
- All state-mutating operations processed through EABS write-path
- EABS provides deterministic ordering and conservation enforcement
- Reliable Broadcast ensures all honest nodes process the same epoch batch
- Double-spend is impossible: transfers are only finalized at epoch boundary via EABS

**Verification:** Conservation invariant checked at every epoch boundary (Section 9.4). If violated, epoch batch is rejected and recovery protocol activates.

**Residual risk:** EABS depends on Reliable Broadcast. If Reliable Broadcast fails (e.g., more than f Byzantine nodes in a 3f+1 system), epoch batch agreement may fail. This degrades to delayed settlement, NOT double-spend — conservative design means no settlement occurs without agreement, rather than inconsistent settlement.

### Finding 2: Reputation Laundering (CRITICAL → MITIGATED)

**Original severity:** CRITICAL
**Attack:** Sybil cluster farms cheap capability_scores for stake amplification.

**Resolution:** Capability-Weighted Stake redesign — Section 4 of Part 1.
- Hard cap at 3.0× multiplier (limits amplification from 10× to 3×)
- Logarithmic scaling: capability_score = 1.0 + ln(1 + raw_score)
- Minimum 3 independent sponsor interactions for reputation to count
- Verification track record weighted by task economic value (trivial tasks contribute negligibly)
- Random claim class assignment (prevents specialization gaming)
- Sentinel Graph identity clustering (C3) flags correlated identities

**Verification:** HG-4 (Hard Gate 4) requires formal game-theoretic analysis showing cost of farming capability_score from 1.0 to 3.0 exceeds the AIC value of 3× amplification.

**Residual risk:** Sophisticated Sybil operations that evade Sentinel Graph detection. Mitigated by the hard cap — even perfect farming yields only 3× amplification, which means the attacker still needs substantial AIC collateral.

### Finding 3: Settlement Sandwiching (CRITICAL → MITIGATED)

**Original severity:** CRITICAL
**Attack:** Timing transactions around epoch boundaries to manipulate settlement windows.

**Resolution:** Multi-rate settlement timing controls — Section 5 of Part 1.
- Epoch boundary jitter: ±10% of epoch duration (random, unpredictable)
- Commit-reveal for completion reports (hash before boundary, reveal after)
- Cross-epoch smoothing: no participant's reward can deviate >25% from trailing 5-epoch average
- Sliding window evaluation: task contribution assessed over window centered on completion, not epoch assignment
- NPV normalization across settlement speeds (eliminates timing arbitrage)

**Verification:** Economic simulation scenario E11 (epoch boundary manipulation) must demonstrate that v2 protections reduce attacker profit to below cost of attack.

**Residual risk:** Attackers with precise network timing information may still gain marginal advantage from jitter prediction. Mitigated by using network entropy in jitter seed (unpredictable to any single entity).

### Finding 4: PC Decay Arbitrage (HIGH → MITIGATED)

**Original severity:** HIGH
**Attack:** Timing spam activity around PC refresh to maximize resource consumption.

**Resolution:** Protocol Credit redesign — Section 3 of Part 1.
- Quality-gated earning: PCs only refreshed for actions producing measurable value
- Sublinear earning curve: PC_earned = k × sqrt(quality_actions) — prevents linear farming
- Congestion-dynamic pricing: cost per action scales with network load (1 + load_factor²)
- Identity-bound attestation via PCVM (C5) — prevents delegation
- Balance cap: max PC = 10 × epoch_earning_rate — limits burst capacity

**Verification:** Under the sublinear curve, doubling activity yields only √2 ≈ 1.41× more PCs. Combined with congestion pricing, the cost of high-volume spam activity scales superlinearly while PC earning scales sublinearly.

**Residual risk:** If quality gates are too lenient, low-quality actions may still earn PCs. Governance should monitor PC earning patterns and adjust quality thresholds.

### Finding 5: Thin Market Squeeze (HIGH → MITIGATED)

**Original severity:** HIGH
**Attack:** Cornering the capacity market during bootstrap with few participants.

**Resolution:** Capacity market protections — Section 8 of this document.
- Position limits: 15% max per entity per resource type
- Cluster position limits (POS-2) via Sentinel Graph
- Use-it-or-lose-it: 70% utilization threshold, reclamation at 60% of epoch
- Progressive 60/20/20 tranche release
- Reserve pricing floor (governance-set)
- Bootstrap CPLR (treasury-funded capacity provider of last resort)
- HHI monitoring with automatic position limit reduction at HHI > 0.40

**Verification:** HG-5 (Hard Gate 5) requires minimum viable scale analysis. Section 8.7 provides the analysis: market functions when ≥5 independent providers per resource type, with CPLR backstop until this condition holds for 3 consecutive epochs.

**Residual risk:** If fewer than 5 providers exist per resource type for an extended period, the CPLR must continue operating, creating treasury drain. Mitigated by CPLR pricing at reserve_floor × 1.1 (slightly above floor), which incentivizes private providers to enter.

### Finding 6: Cross-Budget Arbitrage (HIGH → ACCEPTED WITH FRICTION)

**Original severity:** HIGH
**Attack:** Implicit conversion pathways between SB, PC, and CS erode budget separation.

**Resolution:** Sufficient friction model — Section 3 of Part 1.
- Explicit acknowledgment that perfect budget isolation is economically impossible
- PC identity-binding prevents delegation
- CS position limits prevent accumulation for arbitrage
- Cross-budget flow monitoring with governance alerts
- Implicit exchange rate stabilization triggers governance review

**Verification:** HG-3 (Hard Gate 3) requires quantitative economic model demonstrating stable equilibrium under realistic demand. If model shows collapse to single-token behavior, design must either strengthen friction or honestly reduce to fewer budgets.

**Residual risk:** This is the one finding that is explicitly ACCEPTED rather than fully resolved. The three-budget model provides functional separation, not absolute isolation. If friction mechanisms prove insufficient, governance may reduce to a two-budget model (transferable AIC + non-transferable PC).

### Finding 7: Slashing Ordering Attack (CRITICAL → RESOLVED)

**Original severity:** CRITICAL
**Attack:** Exploiting non-deterministic violation ordering in CRDT-based slashing.

**Resolution:** EABS-ordered slashing — Section 10 of this document.
- ALL slashing processed through EABS write-path (not CRDTs)
- Canonical sort: (violation_type, detection_timestamp_hash, violator_id)
- Violation counts maintained as monotonic counters in EABS state
- All honest nodes process identical violation ordering → identical penalties

**Verification:** Property SLASH-DET (Section 10.8) — formal determinism proof.

**Residual risk:** None. This attack is fully eliminated by EABS. The canonical sort is deterministic by construction.

### Finding 8: RIF Draining (MEDIUM → MITIGATED)

**Original severity:** MEDIUM
**Attack:** Submitting intents with artificially low resource_bounds to exploit workers.

**Resolution:** Intent-budget protections — Section 7 of Part 1.
- Minimum resource_bounds floor based on trailing 10-epoch median completion cost
- Worker inspection window: may reject after 10% effort without penalty
- Sponsor reputation tracking with budget_accuracy_score
- Systematic under-budgeting triggers governance review

**Verification:** Workers can estimate expected effort from task class and historical data. If resource_bounds are below 70% of median completion cost (the minimum floor), the intent is rejected by the protocol.

**Residual risk:** Novel task classes without historical data have no reliable minimum bounds. During the bootstrap of a new task class, workers bear more risk. Mitigated by the worker inspection window.

### Finding 9: Limbo Attack (HIGH → MITIGATED)

**Original severity:** HIGH
**Attack:** Creating pending states that never resolve, locking resources indefinitely.

**Resolution:** Pending state protections — Section 9.3 of this document.
- Mandatory 3-epoch timeout on all pending states
- 5% collateral requirement for initiating pending states
- 2% timeout fee burned on expiry (non-redistributive — prevents gaming)
- Per-entity cap: max 10% of total_supply in pending
- Global cap: max 25% of total_supply in pending

**Verification:** At worst, an attacker can lock 10% of supply for 3 epochs (their per-entity cap), at a cost of 5% collateral. The effective cost is 2% of the locked amount (timeout fee) per 3-epoch cycle, making sustained locking economically irrational.

**Residual risk:** Multiple independent attackers could collectively lock up to 25% (global cap). At scale, this requires many attackers each posting 5% collateral. The cost is significant.

### Finding 10: Speed Class Gaming (MEDIUM → MITIGATED)

**Original severity:** MEDIUM
**Attack:** Structuring activity to settle faster than competitors, gaining compound timing advantage.

**Resolution:** Timing normalization — Section 5 of Part 1.
- NPV normalization: B-class rewards × 0.98, V-class rewards × 1.02
- Challenge rate limit: max 3 V-class challenges per entity per epoch
- Challenge bond: 5% of challenged amount, forfeited if frivolous
- Per-participant fast-to-slow ratio tracking with outlier detection

**Verification:** NPV normalization ensures that the present value of rewards is approximately equal regardless of settlement speed. An entity receiving 100 AIC in B-class gets 98 AIC; an entity receiving 100 AIC in V-class gets 102 AIC. Over time, these differences compound to equalize timing advantage.

**Residual risk:** NPV normalization is approximate. The epoch_discount_rate (0.2% per epoch) must be calibrated to actual opportunity cost of capital in the system. If miscalibrated, residual timing arbitrage exists but is bounded by the normalization parameters.

## 13.2 Threat Model

```
THREAT MODEL:

Fault Model: Byzantine fault tolerance with honest majority assumption
    - System tolerates up to f Byzantine nodes where N ≥ 3f + 1
    - Byzantine nodes may: crash, send conflicting messages, collude, delay messages
    - Network: partially synchronous (messages delivered within bounded time Δ after GST)

Adversary Capabilities:
    Level 1 — Rational Agent (most common):
        - Follows protocol when profitable, deviates when deviation is more profitable
        - Has perfect information about public protocol state
        - Cannot forge cryptographic signatures or break hash functions
        - Budget-constrained (finite AIC, PC, CS)

    Level 2 — Sybil Operator:
        - Controls multiple agent identities
        - May operate Sybil cluster below Sentinel Graph detection threshold
        - Budget-constrained but can distribute across identities

    Level 3 — Coordinated Cartel:
        - Multiple independent economic entities colluding
        - May control up to 30% of total effective stake
        - Cannot control governance supermajority (67%)
        - Communication between cartel members is unobservable

    Level 4 — Infrastructure Attacker:
        - Controls a minority of infrastructure providers
        - May withhold capacity, delay messages, or provide incorrect results
        - Cannot compromise the EABS settlement function (deterministic, verifiable)

Assumptions:
    A1: Honest majority of nodes (>2/3) participate in Reliable Broadcast
    A2: Cryptographic primitives (hash functions, signatures) are secure
    A3: Network achieves partial synchrony (messages eventually delivered)
    A4: At least 5 independent capacity providers per resource type (after bootstrap)
    A5: Governance participants act in long-term self-interest
```

## 13.3 Security Invariants and Enforcement

```
SECURITY INVARIANTS:

SEC-1: Conservation
    "No AIC is created or destroyed outside of treasury minting and slashing burns."
    Enforcement: EABS conservation check at every epoch boundary (Section 9.4)
    Detection: Automatic — EABS rejects batches that violate conservation
    Recovery: ConservationRecovery protocol (Section 9.4.1)

SEC-2: Determinism
    "Given the same epoch batch, every honest node produces the same settlement output."
    Enforcement: EABS processes canonically-ordered batches with deterministic functions
    Detection: Nodes compare settlement hashes after each epoch
    Recovery: Divergent nodes resynchronize from authoritative majority state

SEC-3: Stake Integrity
    "An entity's effective stake accurately reflects its economic commitment and capability."
    Enforcement: Capability score cap (3.0), logarithmic scaling, diversity requirements
    Detection: Sentinel Graph clustering, capability score anomaly detection
    Recovery: Graduated slashing for detected manipulation

SEC-4: Market Integrity
    "Capacity market clearing prices reflect genuine supply and demand."
    Enforcement: Position limits, withholding detection, cornering detection, reserve pricing
    Detection: HHI monitoring, bid correlation analysis, utilization tracking
    Recovery: Emergency position limit reduction, governance review

SEC-5: Governance Integrity
    "Constitutional protections cannot be circumvented by normal governance."
    Enforcement: Supermajority requirements, cooling periods, amendment rate limits
    Detection: Constitutional compliance check on every governance proposal
    Recovery: Invalid governance actions are automatically rejected by EABS

SEC-6: Budget Separation
    "The three budget types provide functionally distinct economic instruments."
    Enforcement: Identity-binding (PC), position limits (CS), cross-budget friction
    Detection: Cross-budget flow monitoring, implicit exchange rate tracking
    Recovery: Governance alert and potential budget model revision
```

## 13.4 Attack Surface Enumeration

```
ATTACK SURFACE:

1. EABS Epoch Batch Submission
    Entry point: Reliable Broadcast message submission
    Attack vectors: Invalid operations, oversized batches, timing manipulation
    Mitigations: Operation validation, batch size limits, epoch jitter

2. Capacity Market Bid/Offer Submission
    Entry point: Sealed-bid commitment protocol
    Attack vectors: Bid manipulation, offer withholding, commitment hash attacks
    Mitigations: Commitment deposits, withholding detection, reserve pricing

3. CRDT Read-Path
    Entry point: Balance queries, availability checks
    Attack vectors: Stale data exploitation, optimistic balance attacks
    Mitigations: Staleness warnings, optimistic-then-settled validation

4. Violation Reporting
    Entry point: ViolationReport submission to EABS batch
    Attack vectors: False accusations, evidence fabrication, selective reporting
    Mitigations: Evidence requirements, false report penalties, reporter ≠ violator check

5. Governance Proposal Submission
    Entry point: G-class governance channel
    Attack vectors: Proposal spam, vote buying, parameter manipulation
    Mitigations: Proposal bonds, constitutional protections, voting weight limits

6. PC Earning Actions
    Entry point: Task completion / verification reports
    Attack vectors: Quality gaming, delegation, farming
    Mitigations: Identity-binding attestation, sublinear earning, quality gates

7. Cross-Locus Operations
    Entry point: Cross-locus reconciliation protocol
    Attack vectors: Locus isolation, reconciliation delay, cross-locus double-spend
    Mitigations: Timeout on cross-locus operations, per-locus conservation checks

8. Sentinel Graph Inputs
    Entry point: Behavioral data fed to identity clustering
    Attack vectors: Behavior mimicry, anti-clustering strategies
    Mitigations: Multiple evidence types (behavioral, network, temporal), confidence thresholds

9. PCVM Attestation Service
    Entry point: Verification attestation API
    Attack vectors: Attestation forgery, service denial
    Mitigations: Cryptographic signature verification, PC earning suspension on unavailability

10. Treasury Operations
    Entry point: G-class governance proposals for treasury allocation
    Attack vectors: Treasury drain, misallocation, emergency action abuse
    Mitigations: Per-allocation caps, reserve floor, emergency action auto-expiry
```

## 13.5 Defense-in-Depth Strategy

DSF employs a layered defense strategy where no single mechanism is the sole protection against any attack class:

```
DEFENSE LAYERS:

Layer 1 — Economic Deterrence:
    Graduated slashing makes violations costly.
    Stake requirements ensure attackers have skin in the game.
    Reporter rewards incentivize detection.
    Burn fraction ensures slashing is net-destructive (not merely redistributive).

Layer 2 — Protocol Enforcement:
    EABS deterministic processing eliminates ordering ambiguity.
    Conservation checks reject invalid state transitions.
    Position limits bound concentration.
    Timeout mechanisms prevent indefinite resource locking.

Layer 3 — Cryptographic Verification:
    Identity-binding attestations via PCVM prevent delegation.
    Sealed-bid commitments prevent information extraction.
    Hash-based canonical ordering is manipulation-resistant.

Layer 4 — Statistical Detection:
    Sentinel Graph identity clustering detects Sybils.
    HHI monitoring detects market concentration.
    Cross-budget flow analysis detects implicit arbitrage.
    Bid correlation analysis detects coordinated manipulation.

Layer 5 — Governance Response:
    Governance alerts for anomalous patterns.
    Parameter adjustment for emerging threats.
    Emergency actions for active attacks.
    Constitutional protections for long-term stability.

Layer 6 — Architectural Isolation:
    Read-path / write-path separation limits attack surface.
    Per-locus EABS limits blast radius of any single compromise.
    Three-budget separation requires multi-vector attacks.
    Multi-rate settlement prevents single-point timing attacks.

Each identified attack requires compromising at least 2 defense layers simultaneously.
No attack compromises more than 1 defense layer via a single vulnerability.
```

---

# Section 14: Scalability and Deployment

## 14.1 Scale Targets

```
SCALE TARGETS:

Primary Target (DESIGN scope):
    1K–10K agents
    10–50 loci
    100–500 parcels
    6 resource types
    Epoch duration: 10 minutes
    EABS batch size: 1K–50K operations per epoch
    Capacity market: 10–100 providers

Secondary Target (engineering optimization):
    10K–50K agents
    50–200 loci
    500–2000 parcels
    12+ resource types
    Epoch duration: 5–15 minutes (governance-tuned)
    EABS batch size: 50K–500K operations per epoch
    Capacity market: 100–500 providers

Aspirational Target (Phase 4, requires architectural evolution):
    100K+ agents
    200+ loci
    2000+ parcels
    Epoch duration: dynamic (per-locus)
    EABS: potentially sharded by locus
    Capacity market: 500+ providers with sub-markets
```

## 14.2 Per-Locus vs Cross-Locus Settlement

```
SETTLEMENT ARCHITECTURE AT SCALE:

At Primary Target (1K–10K agents):
    - Single EABS instance processes all operations
    - Cross-locus reconciliation is lightweight (few cross-locus operations)
    - Reliable Broadcast runs across all nodes
    - Message complexity: O(N) per epoch where N = number of nodes

At Secondary Target (10K–50K agents):
    - Per-locus EABS instances for intra-locus operations
    - Cross-locus reconciliation layer for inter-locus operations
    - Reliable Broadcast per locus (O(N_locus) messages)
    - Cross-locus Reliable Broadcast among locus leaders (O(L) messages, L = number of loci)
    - Total message complexity: O(max(N_locus)) + O(L) per epoch

At Aspirational Target (100K+ agents):
    - Fully sharded EABS (each locus independently settles)
    - Cross-locus settlement becomes its own protocol layer
    - Conservation invariant maintained per-shard with periodic global reconciliation
    - Epoch duration may vary by locus (faster for high-activity, slower for low-activity)
    - Capacity market segmented by geography/specialization

SCALING BOTTLENECK ANALYSIS:

Bottleneck 1: Reliable Broadcast Message Count
    At N nodes: O(N) messages per epoch for Bracha's RBC (O(N²) bits total)
    At 1K nodes: ~1K messages — trivial
    At 10K nodes: ~10K messages — manageable with gossip optimization
    At 100K nodes: ~100K messages — requires hierarchical broadcast

Bottleneck 2: EABS Batch Processing Time
    Settlement function is deterministic and can be optimized:
    - Operation validation: O(1) per operation
    - Conservation check: O(|entities|) per resource type
    - Total: O(|batch| + |entities| × |resource_types|)
    At 50K operations, 10K entities, 6 resource types: ~110K operations
    Estimated processing time: <1 second on modern hardware

Bottleneck 3: Capacity Market Clearing
    Auction clearing: O(B log B + S log S) where B = bids, S = offers
    At 1K bids, 100 offers: ~10K operations — trivial
    At 50K bids, 500 offers: ~500K operations — <1 second
    At 500K bids, 5K offers: ~10M operations — potentially 5-10 seconds
    Mitigation: Per-resource-type clearing can be parallelized

Bottleneck 4: CRDT Read-Path Replication
    PN-Counter replication: O(N) state size per counter
    At 10K entities × 3 budget types × 6 resource types: ~180K counters
    Replication message size: ~180K × 8 bytes = ~1.4 MB per sync
    At 10-second sync interval: ~140 KB/s bandwidth — trivial

Bottleneck 5: Sentinel Graph Processing
    Identity clustering: O(E²) in worst case where E = entities
    At 10K entities: ~100M comparisons — requires efficient algorithm
    Mitigation: Incremental clustering (only re-evaluate changed relationships)
    Realistic complexity with incremental updates: O(E × ΔE) per epoch
```

## 14.3 Deployment Phases

```
DEPLOYMENT PHASE PLAN:

Phase 1 — BOOTSTRAP (Epochs 0 – sunset trigger):
    Scale: <100 agents, <5 loci
    Settlement: Single EABS instance, no cross-locus reconciliation
    Capacity market: CPLR provides majority of capacity
    Governance: Founding parameters set by design team (Tier 3 only)
    Treasury: Initial minting per constitutional caps
    Capability scores: All entities start at 1.0
    Monitoring: All 6 monitoring flags (MF-1 through MF-6) active

    Entry criteria: System deployment
    Exit criteria: MVS condition holds for 3 consecutive epochs (Section 8.7)

Phase 2 — GROWTH (Post-bootstrap sunset – steady state trigger):
    Scale: 100–1K agents, 5–20 loci
    Settlement: Per-locus EABS with cross-locus reconciliation
    Capacity market: CPLR withdrawn, market-driven pricing
    Governance: Community governance active for Tier 2 parameters
    Treasury: Regular issuance per governance-approved schedules
    Capability scores: Differentiated based on accumulated track records
    Monitoring: Focus on market thickness, governance participation

    Entry criteria: Bootstrap sunset complete
    Exit criteria:
        - HHI < 0.15 for all resource types for 10 consecutive epochs
        - Governance participation rate > 30% for 10 consecutive epochs
        - No conservation violations for 50 consecutive epochs
        - Median epoch settlement latency < 50% of epoch duration

Phase 3 — STEADY STATE:
    Scale: 1K–10K agents, 20–50 loci
    Settlement: Fully operational multi-rate settlement
    Capacity market: Competitive, self-sustaining
    Governance: Mature community governance, constitutional amendments possible
    Treasury: Self-sustaining via settlement stream funding
    Full system operational

    Entry criteria: Growth phase exit criteria met
    Duration: Indefinite (primary operational mode)

Phase 4 — SCALE (aspirational):
    Scale: 10K–100K agents, 50+ loci
    Settlement: Sharded EABS, hierarchical Reliable Broadcast
    Capacity market: Sub-markets by specialization
    Governance: Federated governance (per-locus + global)
    Requires: Architectural evolution beyond current DESIGN scope
```

## 14.4 Parameter Sensitivity Analysis Summary

```
PARAMETER SENSITIVITY TABLE:

Parameter                 | Current | Safe Low | Safe High | Break Low        | Break High
─────────────────────────┼─────────┼──────────┼───────────┼──────────────────┼─────────────────
epoch_duration            | 10 min  | 5 min    | 30 min    | <3 min (RBC fail)| >60 min (stale)
pc_decay_rate             | 10%     | 3%       | 25%       | <1% (hoarding)   | >40% (unusable)
cs_position_limit         | 15%     | 5%       | 25%       | <3% (fragmented) | >33% (monopoly)
capability_score_cap      | 3.0     | 1.5      | 5.0       | <1.2 (irrelevant)| >8.0 (gaming)
pending_timeout           | 3 epoch | 1 epoch  | 10 epoch  | <1 (too fast)    | >20 (lockup)
pending_collateral_rate   | 5%      | 2%       | 15%       | <1% (cheap grief)| >25% (unusable)
per_entity_pending_cap    | 10%     | 5%       | 20%       | <2% (too tight)  | >30% (lockup)
global_pending_cap        | 25%     | 10%      | 40%       | <5% (too tight)  | >50% (systemic)
challenge_bond_rate       | 5%      | 2%       | 15%       | <1% (spam)       | >25% (chilling)
npv_discount_rate         | 0.2%    | 0.1%     | 0.5%      | <0.05% (no effect)| >1% (distortion)
smoothing_limit           | 25%     | 10%      | 50%       | <5% (rigid)      | >75% (no protect)
slash_1st_offense         | 1%      | 0.5%     | 5%        | <0.1% (no deter) | >10% (harsh)
tranche_split             | 60/20/20| 50/25/25 | 80/10/10  | 30/35/35 (illiq) | 95/3/2 (no flex)
bootstrap_sunset_epochs   | 3 consec| 2 consec | 10 consec | 1 (premature)    | 20 (delayed)
```

## 14.5 Migration Path from Bootstrap to Steady-State

```
MIGRATION PROTOCOL:

Quantitative Triggers:
    BOOTSTRAP → GROWTH:
        Trigger: MVS (≥5 providers per resource type) for 3 consecutive epochs
        Action: Begin CPLR withdrawal (5-epoch linear schedule)
        Fallback: If MVS fails during withdrawal, pause and revert to BOOTSTRAP

    GROWTH → STEADY STATE:
        Trigger: ALL of the following for 10 consecutive epochs:
            - HHI < 0.15 for all resource types
            - Governance participation > 30%
            - Zero conservation violations for trailing 50 epochs
            - Settlement latency < 50% of epoch duration
        Action: Full governance handover (Tier 2 parameters unlocked for community governance)
        Fallback: If any trigger fails post-transition, EMIT GovernanceAlert but do NOT revert
                  (steady-state is sticky — avoids oscillation)

    STEADY STATE → SCALE:
        Trigger: Sustained demand exceeding EABS single-instance capacity
            - EABS batch processing time > 70% of epoch duration for 5 consecutive epochs
            - OR agent count > 10K with cross-locus operations > 30% of batch
        Action: Initiate architectural evolution (sharded EABS)
        Scope: Beyond current DESIGN — requires new DESIGN cycle

Parameter Migration:
    During BOOTSTRAP:
        All Tier 2 parameters set to conservative defaults (documented in this section)
        Governance cannot modify Tier 2 parameters (locked to prevent premature tuning)

    During GROWTH:
        Tier 2 parameters unlocked for governance adjustment
        First adjustment requires 60% supermajority (higher than normal 50%+1)
        Subsequent adjustments at normal threshold
        Maximum 1 parameter change per 5 epochs (prevents cascading instability)

    During STEADY STATE:
        Full governance control of Tier 2 parameters
        Constitutional protections (Tier 1) always apply
        No rate limit on parameter changes (governance responsibility)
```

## 14.6 Deployment Checklist

```
PRE-DEPLOYMENT REQUIREMENTS:

[  ] EABS settlement function formally verified (conservation, determinism, termination)
[  ] Reliable Broadcast protocol selected and implemented (Bracha's RBC for primary scale)
[  ] Capacity market auction clearing algorithm implemented and tested
[  ] Graduated slashing system implemented with canonical ordering
[  ] Conservation invariant runtime check implemented and tested
[  ] CRDT read-path replication operational across test loci
[  ] Sentinel Graph integration tested (Sybil detection → position limit enforcement)
[  ] PCVM integration tested (attestations → PC identity-binding)
[  ] Treasury initialized with constitutional caps
[  ] Bootstrap CPLR funded and operational
[  ] All 6 monitoring flags (MF-1 through MF-6) instrumented
[  ] Governance voting interface operational
[  ] Economic simulation scenarios E1-E11 executed and documented
[  ] Hard Gates HG-1 through HG-5 satisfied
[  ] Required Actions RA-1 through RA-6 completed

POST-DEPLOYMENT MONITORING (first 50 epochs):

[  ] Conservation invariant holds every epoch (SEC-1)
[  ] Settlement determinism verified across nodes (SEC-2)
[  ] CRDT read-path staleness within acceptable bounds (MF-1)
[  ] Reliable Broadcast completing within epoch (MF-2)
[  ] Capacity market clearing with meaningful price discovery
[  ] No false-positive slashing events
[  ] PC earning/decay reaching equilibrium
[  ] Cross-locus reconciliation completing within Phase 3 window
[  ] Treasury balance above emergency reserve floor
[  ] Governance participation rate tracking
```

---

# Appendix A: Invariant Summary

For reference, all invariants defined across Sections 8–14:

```
CSO-CONS-REVISED:  Σ alloc + Σ pending_out + spent = total_supply (per resource type, per epoch)
CSO-BALANCE:       Σ pending_out = Σ pending_in (globally)
TREASURY-CONS:     treasury.balance + circulating_supply + total_burned = total_issued
POS-1:             allocated(entity, R, K) ≤ 0.15 × total_supply(R, K)
POS-2:             effective_position(cluster) ≤ 0.15 × total_supply
PENDING-CAP-1:     pending_out(entity, R) ≤ 0.10 × total_supply(R)
PENDING-CAP-2:     Σ pending_out(i, R) ≤ 0.25 × total_supply(R)
CSO-ALLOC:         cso.allocated ≤ cso.total_capacity
CONST-1:           Constitutional caps modifiable only via supermajority amendment
SUPPLY-3:          No spontaneous generation or destruction of supply
SLASH-DET:         Deterministic slashing — same batch → same outcomes
SLASH-MON:         Violation count monotonically non-decreasing (except appeal)
SLASH-PROP:        Penalty proportional to offense number and violation severity
EQ-1:              Individual rationality in auctions
EQ-2:              Uniform pricing within tranches
SEC-1 through SEC-6: Security invariants (conservation, determinism, stake, market, governance, budget)
```

---

# Appendix B: Glossary

```
AIC         — Atrahasis Internal Credit. Primary economic unit. Transferable.
ASV         — AI Semantic Vocabulary (C4). Communication protocol.
CPLR        — Capacity Provider of Last Resort. Treasury-funded bootstrap entity.
CRDT        — Conflict-free Replicated Data Type. Used for read-path replication.
CS          — Capacity Slice. Resource reservation token. CSO-backed.
CSO         — Capacity Slice Obligation. Provider's commitment to deliver resources.
DSF         — Deterministic Settlement Fabric. This system (C8).
EABS        — Epoch-Anchored Batch Settlement. Write-path settlement mechanism.
ECOR        — Epoch-Consistent Optimistic Reads. DSF's consistency model.
EMA         — Epistemic Metabolism Architecture (C6). Knowledge processing layer.
HDL         — Hybrid Deterministic Ledger. CRDT reads + EABS writes.
HHI         — Herfindahl-Hirschman Index. Market concentration measure.
MVS         — Minimum Viable Scale. Threshold for market self-sufficiency.
NPV         — Net Present Value. Used for timing normalization across settlement classes.
PC          — Protocol Credit. Non-transferable spam control token. 10%/epoch decay.
PCVM        — Proof-Carrying Verification Model (C5). Verification infrastructure.
RIF         — Recursive Intent Framework (C7). Orchestration layer.
SB          — Sponsor Budget. AIC allocated by task sponsors.
SHREC       — Stability, Homeostasis, Resilience, Evolution, Complexity. EMA regulation.
VTD         — Verification Task Descriptor. PCVM's verification specification format.
```

---

*End of C8 Architecture Document — Part 2 (Sections 8–14)*
*DSF v2.0 — Deterministic Settlement Fabric*
*Date: 2026-03-10*
