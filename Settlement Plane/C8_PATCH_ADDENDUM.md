# C8 DSF Master Tech Spec — Patch Addendum v2.0.1

**Document:** Deterministic Settlement Fabric v2.0 — Patch Addendum
**Applies to:** MASTER_TECH_SPEC.md (C8, Parts 1 and 2)
**Date:** 2026-03-10
**Triggered by:** C9 Cross-Specification Reconciliation + Internal Consistency Audit
**Findings addressed:** F52 through F62, plus C9 Erratum E-C8-01

---

## How to Read This Addendum

Each section below addresses a specific finding. For each, the addendum provides:
1. The finding ID and severity
2. The exact locations in the Master Tech Spec that are affected (by line number)
3. The canonical correction, including full pseudocode where applicable

Implementors MUST apply all HIGH and MEDIUM patches before beginning implementation. LOW patches are strongly recommended.

---

# F52 — Internal Epoch Inconsistency (HIGH)

## Problem

Part 1 consistently uses 60-second epochs (lines 310, 325, 509, 1022, 1510, 2302). Part 2 introduces 10-minute epochs at multiple locations (lines 4390, 4454, 4799, 4869) without acknowledging the discrepancy.

## C9 Terminology Mapping

Per C9 cross-specification reconciliation:

| DSF Term | C9 Canonical Name | Duration | Relationship |
|---|---|---|---|
| epoch (C8) | SETTLEMENT_TICK | 60 seconds | Atomic settlement period |
| — | TIDAL_EPOCH (from C3) | 3600 seconds | 60 SETTLEMENT_TICKs |

The canonical epoch duration for DSF is **60 seconds** (SETTLEMENT_TICK). All references to 10-minute epochs are errors introduced during Part 2 drafting, likely from an earlier design iteration.

## Corrections by Line Number

### Line 4390 (Section 14.1 — Scale Targets, PRIMARY)

**WAS:**
```
Epoch: 10 minutes. Batch: 1K-50K ops/epoch. Providers: 10-100.
```

**CORRECTED:**
```
Epoch: 60 seconds (1 SETTLEMENT_TICK). Batch: 1K-50K ops/epoch. Providers: 10-100.
```

### Line 4394 (Section 14.1 — Scale Targets, SECONDARY)

**WAS:**
```
Epoch: 5-15 min. Batch: 50K-500K ops. Providers: 100-500.
```

**CORRECTED:**
```
Epoch: 60s (governance-adjustable within [30s, 120s]). Batch: 50K-500K ops. Providers: 100-500.
```

### Line 4454 (Section 14.4 — Parameter Sensitivity Analysis)

**WAS:**
```
epoch_duration             10 min    [5 min, 30 min]  <3 min RBC fail; >60 min stale
```

**CORRECTED:**
```
epoch_duration             60s       [30s, 120s]      <15s RBC fail; >300s stale
```

### Line 4799 (Appendix C — Scenario E5)

**WAS:**
```
Setup: E1 baseline + governance changes epoch_duration from 10 min to 7 min
```

**CORRECTED:**
```
Setup: E1 baseline + governance changes epoch_duration from 60s to 45s
```

### Line 4869 (Appendix D — Governance Parameters)

**WAS:**
```
epoch_duration                   10 min    [5, 30] min     +-25%
```

**CORRECTED:**
```
epoch_duration                   60s       [30s, 120s]     +-25%
```

## Terminology Note (to be added after Section 1.3)

```
TERMINOLOGY NOTE (C9 Reconciliation):

Throughout this document, "epoch" refers to the SETTLEMENT_TICK — the
atomic settlement period of 60 seconds. This is distinct from:

  - TIDAL_EPOCH (C3): 3600 seconds = 60 SETTLEMENT_TICKs.
    One TIDAL_EPOCH encompasses a full tidal phase cycle in the
    Noosphere. DSF settles 60 times per TIDAL_EPOCH.

  - V-class period: default 5 SETTLEMENT_TICKs (300 seconds).
    Verification settlement accumulates over multiple ticks.

  - G-class period: variable, 10-50 SETTLEMENT_TICKs typical.

Canonical constant: SETTLEMENT_TICK_MS = 60000
```

---

# F53 — Conservation Formula Variant (MEDIUM)

## Problem

Part 1 (line 840, `check_conservation`) omits `collateral_held` from the AIC conservation check. Part 2 (line 2382, CONS-1 formal definition) correctly includes it. The Part 1 test vector TV-3 (line 2997) even discovered this bug during its own worked example, producing an inline correction.

## Canonical Conservation Formula

The single authoritative AIC conservation formula is:

```
INVARIANT CONS-1 (AIC Conservation — CANONICAL):
    FOR EVERY epoch E, after EABS settlement completes:

        Sigma_{i}( aic_balance(i, E) )
      + Sigma_{i}( staked_aic(i, E) )
      + Sigma_{i}( pending_out(i, E) )
      + Sigma_{i}( collateral_held(i, E) )
      + treasury_balance(E)
      = total_aic_supply(E)

    WITH AUXILIARY INVARIANT CONS-1a:
        Sigma_{i}( pending_out(i, E) ) = Sigma_{i}( pending_in(i, E) )

    NOTE: pending_in is NOT in the main equation. It is tracked
    separately via CONS-1a. Including both pending_out and pending_in
    in the main equation would double-count (as discovered in TV-3).
```

## Corrected check_conservation (replaces Part 1 lines 827-859)

```
FUNCTION check_conservation(state: SettlementState) -> bool:
    // AIC Conservation (CONS-1 — CANONICAL)
    total_aic_in_accounts = 0
    total_aic_staked = 0
    total_pending_out = 0
    total_pending_in = 0
    total_collateral = 0

    FOR each account IN state.accounts.values():
        total_aic_in_accounts += account.aic_balance.value()
        total_aic_staked += account.staked_aic.value()
        total_pending_out += account.pending_out.value()
        total_pending_in += account.pending_in.value()
        total_collateral += account.collateral_held.value()

    aic_conservation =
        (total_aic_in_accounts + total_aic_staked +
         total_pending_out + total_collateral +
         state.treasury_balance)
        == state.total_aic_supply

    // Auxiliary: Pending Balance (CONS-1a)
    pending_balance = (total_pending_out == total_pending_in)

    // CS Conservation (CONS-2) — per resource type
    cs_conservation = true
    FOR each rt IN state.resource_types:
        total_cs_held = 0
        total_cs_pending = 0
        FOR each account IN state.accounts.values():
            total_cs_held += account.cs_allocation[rt].value()
        FOR each pending IN state.pending_registry.values():
            IF pending.resource_type == rt:
                total_cs_pending += pending.amount
        cs_conservation = cs_conservation AND
            (total_cs_held + total_cs_pending + state.unallocated_cs[rt])
            == state.total_cs_supply[rt]

    RETURN aic_conservation AND pending_balance AND cs_conservation
```

---

# F54 — Three-Budget Collapse Path (MEDIUM)

## Problem

Section 13.2, Finding 6 acknowledges that the three-budget model might collapse to two budgets if friction proves insufficient, but provides no governance procedure for executing this transition.

## Monitoring Criteria for Budget Collapse Trigger

```
MONITORING RULE BM-1 (Budget Collapse Assessment):

    The following metrics are tracked per TIDAL_EPOCH (3600s = 60 ticks):

    Metric 1 — Implicit PC/AIC Exchange Rate Stability:
        pc_aic_rate = (total_aic_spent_on_self_tasks / total_pc_earned)
        ALERT if coefficient_of_variation(pc_aic_rate, trailing_60_ticks) < 0.05
        Interpretation: rate is stable enough to constitute a de facto exchange,
                        meaning budget separation has failed.

    Metric 2 — Cross-Budget Flow Volume:
        cross_flow = sum of AIC spent on actions whose primary purpose is
                     PC earning (self-sponsored tasks with no external consumer)
        ALERT if cross_flow > 0.10 * total_aic_settlement_volume
                for 10 consecutive TIDAL_EPOCHs
        Interpretation: >10% of economic activity is cross-budget arbitrage.

    Metric 3 — Third-Budget Marginal Friction:
        friction_delta = attack_cost_with_3_budgets - attack_cost_with_2_budgets
        Computed via quarterly simulation (every 50 SETTLEMENT_TICKs).
        ALERT if friction_delta < 0.02 * median_agent_stake
        Interpretation: the third budget adds less than 2% additional friction
                        to the cheapest known attack vector.

    TRIGGER CONDITION (all three must hold simultaneously for 5 TIDAL_EPOCHs):
        BM-1.metric_1 in ALERT state
        AND BM-1.metric_2 in ALERT state
        AND BM-1.metric_3 in ALERT state
```

## Governance Transition Process

```
PROTOCOL BudgetCollapseTransition:

    Phase 0 — TRIGGER:
        BM-1 trigger condition met for 5 consecutive TIDAL_EPOCHs.
        System automatically generates GovernanceProposal of type
        ConstitutionalAmendment (Tier 1 — supermajority required).
        This is the ONLY automated constitutional proposal path.

    Phase 1 — PROPOSAL (auto-generated):
        proposal_type:    ConstitutionalAmendment
        parameter:        budget_type_definitions
        current_value:    SB/PC/CS (three budgets)
        proposed_value:   SB/CS (two budgets — PC merged into SB)
        rationale:        auto-populated with BM-1 metric history
        bond:             5% of treasury balance (from treasury itself)

    Phase 2 — COOLING (20 SETTLEMENT_TICKs):
        Standard constitutional cooling period.
        Community deliberation. Counter-proposals allowed.
        During cooling, BM-1 metrics continue to be tracked.
        IF trigger condition ceases during cooling:
            Proposal auto-withdrawn (bond returned minus 1% fee).

    Phase 3 — VOTE (5 SETTLEMENT_TICKs):
        Supermajority required (67% of governance weight).
        Quorum: 50% of total effective governance weight.

    Phase 4 — MIGRATION (if passed):
        Executed over 10 SETTLEMENT_TICKs (gradual):

        Tick 1:  PC earning suspended. Existing PC balances frozen.
        Tick 2:  PC spending continues (drain existing balances).
        Tick 3:  PC decay continues at 10%/tick.
        Tick 4:  Spam control transitions to AIC micro-fees.
                 New parameter: spam_fee_aic = governance-set minimum.
        Tick 5:  Quality gating transitions from PC-identity-binding
                 to AIC-staked-identity-binding.
        Ticks 6-9: PC balances decay toward zero.
        Tick 10: PC data structures removed from AccountState.
                 budget_type_definitions = SB/CS.
                 Four-stream weights become 45/45/5/5 (comms/gov reduced
                 proportionally since PC-gated quality metrics are gone).

        Conservation note:
            PCs were never part of CONS-1. Removal has no effect on
            AIC conservation. CONS-2 (CS) is unchanged.

    REVERT PATH:
        If migration causes settlement instability (conservation violation
        or >25% drop in governance participation) during Ticks 1-10:
            Emergency governance vote (40% quorum, 60% threshold, 1 tick).
            Revert to three-budget model. PC earning re-enabled.
            Frozen balances restored from pre-migration snapshot.
```

---

# F55 — Slashing Pseudocode Fix (MEDIUM)

## Problem

Part 1's `apply_operation` SLASH case (line 713-714) sends the full penalty to treasury:

```
violator.staked_aic.decrement(op.submitter_id, penalty)
state.treasury_balance += penalty   // BUG: full amount to treasury
```

Part 2 Section 10.5 (lines 3330-3351) correctly specifies the three-way split: 50% burned, 30% treasury, 20% reporter.

## Corrected SLASH Case (replaces Part 1 lines 705-717)

```
CASE SLASH:
    violator = state.accounts[op.payload.violator]
    penalty = compute_graduated_penalty(
        op.payload.offense_number,
        violator.staked_aic.value(),
        state.parameter_set.slashing_schedule)
    IF penalty > violator.staked_aic.value():
        penalty = violator.staked_aic.value()

    // Three-way split (per Section 10.5 SLASH-DIST)
    burn_amount = floor(penalty * 0.50)
    treasury_amount = floor(penalty * 0.30)
    reporter_amount = penalty - burn_amount - treasury_amount  // absorbs rounding

    // Apply atomically
    violator.staked_aic.decrement(op.submitter_id, penalty)
    state.treasury_balance += treasury_amount
    state.total_aic_supply -= burn_amount                      // deflationary burn
    IF op.payload.reporter_id != NULL:
        reporter = state.accounts[op.payload.reporter_id]
        reporter.aic_balance.increment(op.submitter_id, reporter_amount)
    ELSE:
        // System-detected violation (no reporter) — reporter share to treasury
        state.treasury_balance += reporter_amount

    violator.violation_count = max(
        violator.violation_count, op.payload.offense_number)
    RETURN Success(state)
```

## Conservation Proof Update (replaces Part 1 line 890)

The proof sketch at line 890 stated:

> SLASH: Decrements staked_aic by penalty, increments treasury_balance by penalty. Net change = 0. Preserved.

**CORRECTED:**

> SLASH: Decrements staked_aic by penalty. Distributes: 50% burned (reduces total_aic_supply), 30% to treasury_balance, 20% to reporter aic_balance. LHS delta: -penalty + 0.30*penalty + 0.20*penalty = -0.50*penalty. RHS delta (total_supply): -0.50*penalty. LHS delta = RHS delta. Conservation preserved.

---

# F56 — Failure Mode Catalogue (MEDIUM)

## Problem

Failure modes are scattered throughout both parts of the spec. This section consolidates them into a single numbered catalogue.

## Consolidated Failure Mode Catalogue

```
FM-01: PHANTOM BALANCE (Double Spend)
    Description:  Agent spends same AIC at two replicas simultaneously
    Trigger:      Concurrent AIC_TRANSFER on different CRDT replicas
    Detection:    Impossible pre-settlement (CRDT merge allows it);
                  caught at EABS settlement (balance check fails)
    Recovery:     Second transfer rejected during EABS batch processing
    Severity:     FATAL if undetected (RESOLVED by EABS design)
    Ref:          Section 1.4, Section 13.2 Finding 1

FM-02: CONSERVATION VIOLATION (Implementation Bug)
    Description:  Post-settlement CONS-1 or CONS-2 invariant fails
    Trigger:      Bug in settlement function or novel attack vector
    Detection:    eabs_conservation_check() returns Err after batch
    Recovery:     ConservationRecovery protocol (Section 9.4.1):
                  halt, replay with per-op checks, quarantine, retry
    Severity:     CRITICAL
    Ref:          Section 9.4.1

FM-03: RELIABLE BROADCAST FAILURE
    Description:  Bracha's RBC fails to deliver epoch batch
    Trigger:      >f nodes crash (more than n/3 Byzantine)
    Detection:    Epoch boundary passes without COMMITTED phase
    Recovery:     Settlement stalls. CRDT read-path continues.
                  Resumes when honest majority restored.
                  Manual recovery: governance emergency action
    Severity:     HIGH
    Ref:          Section 2.3.3, Section 2.3.9

FM-04: SETTLEMENT HASH MISMATCH
    Description:  Nodes disagree on post-settlement state hash
    Trigger:      Non-determinism in settlement function or corrupted state
    Detection:    Nodes compare settlement_hash after each epoch
    Recovery:     EpochRecovery protocol. Minority nodes re-download
                  and re-execute. If no majority agrees, governance halt.
    Severity:     HIGH
    Ref:          Section 2.3.9 (EpochRecovery)

FM-05: LIMBO ATTACK (Resource Lockup)
    Description:  Attacker creates pending states that never resolve
    Trigger:      PENDING_INITIATE without completing/timing out
    Detection:    check_pending_timeouts() at each epoch
    Recovery:     Mandatory 3-epoch timeout. 2% fee burned.
                  Collateral partially forfeited.
    Severity:     HIGH (mitigated by timeout + caps)
    Ref:          Section 9.3.2, Section 13.2 Finding 9

FM-06: THIN MARKET FAILURE
    Description:  Capacity market has insufficient providers for price discovery
    Trigger:      independent_providers(R) < 5 for any resource type
    Detection:    MVS check at each epoch boundary
    Recovery:     CPLR activation (treasury-funded provider of last resort)
    Severity:     HIGH
    Ref:          Section 8.9

FM-07: REPUTATION LAUNDERING (Sybil Farming)
    Description:  Sybil cluster farms capability_scores for amplified stake
    Trigger:      Multiple identities with correlated behavior boosting each other
    Detection:    Sentinel Graph (C3) behavioral correlation > 0.85
    Recovery:     Cluster position limits (POS-2). Slashing for
                  GOVERNANCE_MANIPULATION (2.0x severity). Score reset.
    Severity:     HIGH (mitigated by cap=3.0, log scaling)
    Ref:          Section 4.3, Section 10.6, Section 13.2 Finding 2

FM-08: SETTLEMENT SANDWICHING
    Description:  Timing transactions around epoch boundaries for advantage
    Trigger:      Attacker controls timing of task completion reports
    Detection:    Cross-epoch smoothing (>25% deviation from trailing average)
    Recovery:     Commit-reveal for reports. Epoch jitter (+/-10%).
                  Sliding window evaluation. Smoothing alert emitted.
    Severity:     MEDIUM (residual advantage <2%)
    Ref:          Section 5.2, Section 13.2 Finding 3

FM-09: PC DECAY ARBITRAGE
    Description:  Timing spam around PC refresh cycle
    Trigger:      Agent spends PC immediately after earning, before decay
    Detection:    Cross-budget flow monitoring
    Recovery:     Quality gates. Sublinear earning. Congestion pricing.
                  Identity binding prevents delegation.
    Severity:     MEDIUM
    Ref:          Section 3.3, Section 13.2 Finding 4

FM-10: CAPACITY MARKET CORNERING
    Description:  Single entity or cluster acquires >15% of capacity supply
    Trigger:      Concentrated bidding or Sybil bids
    Detection:    HHI > 0.25 per resource type (MF-4)
    Recovery:     Position limits (POS-1, POS-2). If HHI > 0.40,
                  emergency 10% position limit. Governance review.
    Severity:     MEDIUM
    Ref:          Section 8.6, Section 8.10

FM-11: CROSS-BUDGET ARBITRAGE
    Description:  Profitable SB-to-PC conversion undermines budget separation
    Trigger:      Implicit exchange rate stabilizes (low variance)
    Detection:    BM-1 metrics (see F54). Flow monitoring.
    Recovery:     Governance adjusts friction parameters.
                  Worst case: budget collapse transition (F54).
    Severity:     MEDIUM (accepted with friction)
    Ref:          Section 3.5, Section 13.2 Finding 6

FM-12: SLASHING ORDERING AMBIGUITY
    Description:  Different nodes compute different penalties for same violation
    Trigger:      Non-deterministic violation processing order
    Detection:    Settlement hash mismatch (FM-04)
    Recovery:     FULLY RESOLVED by EABS canonical ordering.
                  (type, timestamp_hash, violator_id) sort key.
    Severity:     CRITICAL (RESOLVED)
    Ref:          Section 10.2

FM-13: RIF DRAINING (Worker Exploitation)
    Description:  Sponsor sets artificially low resource_bounds
    Trigger:      resource_bounds < actual task cost
    Detection:    Worker over-budget flagging. 3+ flags triggers review.
    Recovery:     Minimum bounds floor (70% trailing median).
                  Worker inspection window (10% effort).
                  Sponsor reputation penalty.
    Severity:     MEDIUM
    Ref:          Section 7.3, Section 13.2 Finding 8

FM-14: CROSS-LOCUS RECONCILIATION FAILURE
    Description:  Cross-locus EABS batch fails conservation check
    Trigger:      Network partition during cross-locus settlement phase
    Detection:    Phase 3 conservation check fails
    Recovery:     All cross-locus ops rolled back for epoch.
                  Per-locus settlements still apply.
                  Rolled-back ops retried next epoch.
    Severity:     MEDIUM
    Ref:          Section 12.1.2

FM-15: SENTINEL GRAPH UNAVAILABILITY
    Description:  C3 Sentinel Graph service goes offline
    Trigger:      C3 infrastructure failure or partition
    Detection:    Query timeout on get_identity_clusters()
    Recovery:     Continue with last known cluster data.
                  New entities treated as singletons.
                  POS-2 (cluster limits) degraded to POS-1 (entity limits).
                  Governance alert emitted.
    Severity:     MEDIUM
    Ref:          Section 12.1.4

FM-16: PCVM ATTESTATION UNAVAILABILITY
    Description:  C5 attestation service goes offline
    Trigger:      C5 infrastructure failure
    Detection:    verify_attestation() call fails
    Recovery:     PC earning SUSPENDED. Existing PC continues to decay.
                  No backfill on recovery.
    Severity:     MEDIUM
    Ref:          Section 12.2.3

FM-17: GOVERNANCE QUORUM FAILURE
    Description:  Insufficient voter participation for governance proposals
    Trigger:      Voting weight < quorum threshold (30% for Tier 2, 50% for Tier 1)
    Detection:    Vote tally at voting period end
    Recovery:     Proposal fails (not enacted). Bond forfeited.
                  Governance participation alert triggers Stream 4 bonus review.
    Severity:     LOW
    Ref:          Section 11.4.2

FM-18: EPOCH BOUNDARY CLOCK SKEW
    Description:  Node clocks diverge enough to disagree on epoch boundaries
    Trigger:      NTP failure or adversarial clock manipulation
    Detection:    Epoch boundary jitter plus Reliable Broadcast timing
    Recovery:     Jitter seed is deterministic (hash-based, not clock-based).
                  Nodes that miss boundary window have their ops deferred.
                  EpochRecovery for nodes that fall behind.
    Severity:     LOW
    Ref:          Section 2.3.9 (compute_epoch_boundary)

FM-19: TREASURY DRAIN
    Description:  Treasury balance approaches emergency reserve floor
    Trigger:      Excessive CPLR spending, slashing burn rates, or governance spend
    Detection:    treasury_balance < emergency_reserve_floor * 1.5
    Recovery:     Constitutional protection: emergency_reserve_floor cannot be spent.
                  CPLR auto-pauses if treasury < bootstrap_cap allocation.
                  Governance alert at 150% of floor.
    Severity:     LOW
    Ref:          Section 11.1, Section 11.2

FM-20: STALE LOCUS (Degraded Mode)
    Description:  Locus fails to receive settled state for >3 epochs
    Trigger:      Sustained network partition or infrastructure failure
    Detection:    staleness_bound > 3 epochs
    Recovery:     Locus enters DEGRADED mode (read-only).
                  Resynchronization via EpochRecovery from any non-stale locus.
                  Recovery time: O(missed_epochs * settlement_time).
    Severity:     LOW
    Ref:          Section 12.1.1
```

---

# F57 — Four-Stream Scoring Simplification (MEDIUM)

## Problem

Stream 3 (Communication Efficiency, 10%) and Stream 4 (Governance Participation, 10%) have multi-dimensional scoring functions (protocol adherence, signal-to-noise, response appropriateness for Stream 3; voting + proposal quality + constitutional adherence for Stream 4) that represent disproportionate implementation complexity for their reward weight.

## Bootstrap Simplified Scoring

The following simplified scoring functions apply during bootstrap and growth phases (Phases 1-2 per Section 14.3), when network size is below 1000 agents.

### Stream 3 — Communication Bonus (Simplified)

```
FUNCTION compute_communication_score_simplified(
    agent: AgentID,
    epoch: EpochID,
    state: SettlementState
) -> float64:
    // Flat rate: 1.0 per schema-valid message sent, up to cap
    messages = get_agent_messages(agent, epoch)
    valid_count = count(m for m in messages if m.schema_valid)

    // Cap at 20 messages per epoch to prevent spam-for-reward
    capped = min(valid_count, 20)

    // Normalize to [0, 1] range
    RETURN capped / 20.0

// Reward per agent = (capped / 20.0) / Sigma_agents(capped_i / 20.0) * pool
// With pool = 10% of epoch reward pool

PARAMETERS:
    COMM_MESSAGE_CAP = 20           // Max rewarded messages per tick
    COMM_SCHEMA_REQUIRED = true     // Only schema-valid messages count
```

### Stream 4 — Governance Bonus (Simplified)

```
FUNCTION compute_governance_score_simplified(
    agent: AgentID,
    proposals: List<GovernanceProposal>,
    state: SettlementState
) -> float64:
    // Flat rate: 1.0 per vote cast on any active proposal
    votes_cast = count(p for p in proposals if agent IN p.voters)

    // Cap at 5 votes per G-class period
    capped = min(votes_cast, 5)

    // Normalize to [0, 1] range
    RETURN capped / 5.0

PARAMETERS:
    GOV_VOTE_CAP = 5                // Max rewarded votes per G-class period
```

### Transition Trigger to Full Scoring

```
RULE STREAM_SCORING_UPGRADE:
    CONDITION:
        active_agents(trailing_60_ticks) >= 1000
        AND governance_participation_rate >= 0.20
        FOR 5 consecutive TIDAL_EPOCHs

    ACTION:
        Switch Stream 3 scoring to compute_communication_scores() (Section 6.2.3)
        Switch Stream 4 scoring to compute_governance_participation_score() (Section 6.2.4)
        Transition is a G-class governance parameter change (Tier 2).
        1-tick execution delay for all nodes to switch simultaneously.

    REVERT:
        If active_agents drops below 500 for 10 consecutive TIDAL_EPOCHs,
        revert to simplified scoring. Same governance process.
```

---

# F58 — AccountState Mismatch (LOW)

## Problem

Part 1 Definition 2.2 (line 223) defines AccountState without `collateral_held` and uses a bare `PNCounter` for `cs_allocation`. Part 2 Appendix B (line 4612) defines a different AccountState that includes `collateral_held` and uses `Map<ResourceType, PNCounter>` for `cs_allocation`.

## Canonical AccountState

The following is the single authoritative AccountState. It supersedes both Part 1 line 223 and Part 2 line 4612.

```
STRUCTURE AccountState:
    // Identity
    account_id:          AgentID

    // Budget balances (CRDT-mergeable)
    aic_balance:         PNCounter                    // Sponsor Budget (AIC) — free balance
    staked_aic:          PNCounter                    // AIC locked as collateral for stake
    collateral_held:     PNCounter                    // Pending state collateral deposits
    pc_balance:          PNCounter                    // Protocol Credits (non-transferable)
    cs_allocation:       Map<ResourceType, PNCounter> // Capacity Slices per resource type

    // Pending state tracking
    pending_out:         PNCounter                    // Outbound pending transitions
    pending_in:          PNCounter                    // Inbound pending transitions

    // Settlement metadata
    last_settled_epoch:  uint64                       // Last EABS settlement epoch
    capability_score:    float64                      // Cached, range [1.0, 3.0]
    violation_count:     uint32                       // Monotonic (except appeal decrement)

    // CRDT synchronization
    state_vector:        Map<NodeID, uint64>          // Lamport timestamps per node

    FUNCTION merge(other: AccountState) -> AccountState:
        ASSERT self.account_id == other.account_id
        result = AccountState{account_id: self.account_id}

        // All PNCounter fields: element-wise max merge
        result.aic_balance = self.aic_balance.merge(other.aic_balance)
        result.staked_aic = self.staked_aic.merge(other.staked_aic)
        result.collateral_held = self.collateral_held.merge(other.collateral_held)
        result.pc_balance = self.pc_balance.merge(other.pc_balance)
        result.pending_out = self.pending_out.merge(other.pending_out)
        result.pending_in = self.pending_in.merge(other.pending_in)

        // CS allocation: merge per resource type
        all_types = union(self.cs_allocation.keys(), other.cs_allocation.keys())
        FOR each rt IN all_types:
            self_counter = self.cs_allocation.get(rt, PNCounter{})
            other_counter = other.cs_allocation.get(rt, PNCounter{})
            result.cs_allocation[rt] = self_counter.merge(other_counter)

        // Scalar fields: last-writer-wins by epoch
        result.last_settled_epoch = max(self.last_settled_epoch, other.last_settled_epoch)
        result.capability_score = IF self.last_settled_epoch >= other.last_settled_epoch
                                  THEN self.capability_score
                                  ELSE other.capability_score
        result.violation_count = max(self.violation_count, other.violation_count)

        // State vector: element-wise max
        FOR each node_id IN union(self.state_vector.keys(), other.state_vector.keys()):
            result.state_vector[node_id] = max(
                self.state_vector.get(node_id, 0),
                other.state_vector.get(node_id, 0))

        RETURN result
```

### Changes from Part 1 Definition 2.2

| Field | Part 1 | Canonical | Reason |
|---|---|---|---|
| `collateral_held` | absent | `PNCounter` | Required for CONS-1 (collateral is part of conservation) |
| `cs_allocation` | `PNCounter` | `Map<ResourceType, PNCounter>` | CS is typed per resource (6 types defined in Section 8.2) |

### Convergence Proof Update

Theorem 2.1 (CRDT Convergence) remains valid. The added `collateral_held` field uses PNCounter merge (commutative, associative, idempotent). The `Map<ResourceType, PNCounter>` for cs_allocation applies PNCounter merge per key, with union of key sets — this composition preserves all three semilattice properties by the same argument as the original proof.

---

# F59 — Settlement Function Incomplete (LOW)

## Problem

Part 1's `apply_operation` (lines 693-819) provides pseudocode for AIC_TRANSFER, SLASH, PC_DECAY, REWARD_B_CLASS, AIC_STAKE, AIC_UNSTAKE, PENDING_INITIATE, PENDING_COMPLETE, PENDING_TIMEOUT, TREASURY_MINT, and TREASURY_BURN. Lines 816-819 note that remaining types "follow the same pattern" without providing pseudocode. This patch provides the missing implementations.

## Missing Operation Implementations

### PC_EARN

```
CASE PC_EARN:
    acct = state.accounts[op.submitter_id]

    // Verify PCVM attestation (C5 identity-binding)
    IF NOT verify_pcvm_attestation(op.payload.attestation):
        RETURN Failure(INVALID_ATTESTATION)

    // Compute earning (sublinear: k * sqrt(quality_actions))
    earning = floor(
        state.parameter_set.pc_earning_coefficient *
        sqrt(op.payload.quality_actions))

    // Enforce balance cap: pc_balance <= 10 * epoch_earning_rate
    cap = 10 * earning
    IF acct.pc_balance.value() + earning > cap:
        earning = max(0, cap - acct.pc_balance.value())

    acct.pc_balance.increment(op.submitter_id, earning)
    RETURN Success(state)
```

### PC_SPEND

```
CASE PC_SPEND:
    acct = state.accounts[op.submitter_id]

    // Compute congestion-adjusted cost
    epoch_load = state.current_epoch_load()
    cost = compute_congestion_cost(
        op.payload.base_cost,
        state.parameter_set,
        epoch_load)

    IF acct.pc_balance.value() < cost:
        RETURN Failure(INSUFFICIENT_PC)

    acct.pc_balance.decrement(op.submitter_id, cost)
    RETURN Success(state)
```

### CS_ALLOCATE

```
CASE CS_ALLOCATE:
    acct = state.accounts[op.submitter_id]
    rt = op.payload.resource_type
    qty = op.payload.quantity

    // Check unallocated supply
    IF state.unallocated_cs[rt] < qty:
        RETURN Failure(INSUFFICIENT_CS_SUPPLY)

    // Check position limit (POS-1): max 15% of total per entity
    current_held = acct.cs_allocation[rt].value()
    IF current_held + qty > floor(state.total_cs_supply[rt] * 0.15):
        RETURN Failure(POSITION_LIMIT_EXCEEDED)

    // Allocate
    state.unallocated_cs[rt] -= qty
    acct.cs_allocation[rt].increment(op.submitter_id, qty)
    RETURN Success(state)
```

### CS_RELEASE

```
CASE CS_RELEASE:
    acct = state.accounts[op.submitter_id]
    rt = op.payload.resource_type
    qty = op.payload.quantity

    IF acct.cs_allocation[rt].value() < qty:
        RETURN Failure(INSUFFICIENT_CS_HELD)

    acct.cs_allocation[rt].decrement(op.submitter_id, qty)
    state.unallocated_cs[rt] += qty
    RETURN Success(state)
```

### CS_REVERT

```
CASE CS_REVERT:
    // Revert a pending CS allocation that timed out
    pending = state.pending_registry[op.payload.pending_id]
    IF pending.resource_type == NONE:
        RETURN Failure(NOT_CS_PENDING)

    rt = pending.resource_type
    qty = pending.amount

    // Return to unallocated pool
    state.unallocated_cs[rt] += qty

    // Remove from pending registry
    DELETE state.pending_registry[op.payload.pending_id]
    RETURN Success(state)
```

### CAPACITY_BID

```
CASE CAPACITY_BID:
    // Bids are collected during COLLECTING phase and processed at clearing.
    // The EABS settlement function validates and records the bid.
    acct = state.accounts[op.submitter_id]
    rt = op.payload.resource_type

    // Validate commitment deposit (0.5% of bid value)
    bid_value = op.payload.quantity * op.payload.max_price
    deposit = ceil(bid_value * 0.005)
    IF acct.aic_balance.value() < deposit:
        RETURN Failure(INSUFFICIENT_BID_DEPOSIT)

    // Reserve deposit
    acct.aic_balance.decrement(op.submitter_id, deposit)
    acct.collateral_held.increment(op.submitter_id, deposit)

    // Record bid for clearing phase
    state.capacity_bids[op.epoch_number].append(op.payload)
    RETURN Success(state)
```

### CAPACITY_CLEAR

```
CASE CAPACITY_CLEAR:
    // Generated by the auction clearing algorithm (Section 8.5)
    // This op is system-generated, not user-submitted
    IF op.submitter_id != SYSTEM_ID:
        RETURN Failure(UNAUTHORIZED_CLEAR)

    FOR each (bidder_id, qty) IN op.payload.allocations:
        bidder = state.accounts[bidder_id]
        rt = op.payload.resource_type
        cost = qty * op.payload.clearing_price

        // Deduct payment from bidder
        IF bidder.aic_balance.value() < cost:
            // Bidder can't afford at clearing price — skip allocation
            CONTINUE
        bidder.aic_balance.decrement(SYSTEM_ID, cost)
        state.treasury_balance += cost

        // Release commitment deposit
        deposit = state.bid_deposits[bidder_id][op.epoch_number]
        bidder.collateral_held.decrement(SYSTEM_ID, deposit)
        bidder.aic_balance.increment(SYSTEM_ID, deposit)

        // Allocate capacity
        state.unallocated_cs[rt] -= qty
        bidder.cs_allocation[rt].increment(SYSTEM_ID, qty)

    RETURN Success(state)
```

### CAPACITY_SPOT

```
CASE CAPACITY_SPOT:
    // Mid-epoch spot purchase at a premium over last clearing price
    acct = state.accounts[op.submitter_id]
    rt = op.payload.resource_type
    qty = op.payload.quantity

    // Spot price = last clearing price * 1.5 (premium for immediacy)
    spot_price = state.last_clearing_price[rt] * 1.5
    cost = qty * spot_price

    IF acct.aic_balance.value() < cost:
        RETURN Failure(INSUFFICIENT_BALANCE)
    IF state.unallocated_cs[rt] < qty:
        RETURN Failure(INSUFFICIENT_SPOT_SUPPLY)

    // Check position limit
    current_held = acct.cs_allocation[rt].value()
    IF current_held + qty > floor(state.total_cs_supply[rt] * 0.15):
        RETURN Failure(POSITION_LIMIT_EXCEEDED)

    acct.aic_balance.decrement(op.submitter_id, cost)
    state.treasury_balance += cost
    state.unallocated_cs[rt] -= qty
    acct.cs_allocation[rt].increment(op.submitter_id, qty)
    RETURN Success(state)
```

### REWARD_V_CLASS

```
CASE REWARD_V_CLASS:
    recipient = state.accounts[op.payload.recipient]
    delay_epochs = op.payload.delay_epochs  // V-class period (default 5)
    r = state.parameter_set.epoch_discount_rate  // 0.002

    // NPV premium for delayed settlement: (1+r)^delay
    npv_factor = pow(1.0 + r, delay_epochs)
    adjusted = floor(op.payload.base_amount * npv_factor)

    IF adjusted > state.reward_pools[VERIFICATION]:
        RETURN Failure(INSUFFICIENT_REWARD_POOL)

    state.reward_pools[VERIFICATION] -= adjusted
    recipient.aic_balance.increment(op.submitter_id, adjusted)
    RETURN Success(state)
```

### REWARD_G_CLASS

```
CASE REWARD_G_CLASS:
    recipient = state.accounts[op.payload.recipient]
    delay_epochs = op.payload.delay_epochs  // variable, 10-50 typical
    r = state.parameter_set.epoch_discount_rate

    // NPV premium for governance settlement delay
    npv_factor = pow(1.0 + r, delay_epochs)
    adjusted = floor(op.payload.base_amount * npv_factor)

    IF adjusted > state.reward_pools[GOVERNANCE]:
        RETURN Failure(INSUFFICIENT_REWARD_POOL)

    state.reward_pools[GOVERNANCE] -= adjusted
    recipient.aic_balance.increment(op.submitter_id, adjusted)
    RETURN Success(state)
```

### PARAMETER_UPDATE

```
CASE PARAMETER_UPDATE:
    // Must be authorized by governance (G-class settlement)
    IF NOT verify_governance_authorization(op):
        RETURN Failure(UNAUTHORIZED_PARAMETER_CHANGE)

    param_name = op.payload.parameter_name
    new_value = op.payload.new_value
    old_value = state.parameter_set[param_name]

    // Enforce max change rate (20% per governance cycle)
    IF abs(new_value - old_value) / old_value > 0.20:
        RETURN Failure(CHANGE_RATE_EXCEEDED)

    // Enforce safe range bounds
    IF NOT in_safe_range(param_name, new_value):
        RETURN Failure(OUT_OF_SAFE_RANGE)

    // Enforce cooldown (parameter locked for 10 ticks after last change)
    IF state.parameter_last_changed[param_name] + 10 > state.epoch_number:
        RETURN Failure(COOLDOWN_NOT_ELAPSED)

    // Apply
    state.parameter_set[param_name] = new_value
    state.parameter_last_changed[param_name] = state.epoch_number
    RETURN Success(state)
```

---

# F60 — NPV Asymmetry Documentation (LOW)

## Problem

V-class uses `(1+r)^delay` (a premium > 1.0) while B-class uses a flat `0.98` discount. This asymmetry is not explained in the spec.

## Explanation (to be added after Section 5.3, line 1608)

```
NPV ASYMMETRY NOTE:

The B-class discount (0.98) and V-class premium ((1+r)^delay) are intentionally
asymmetric. They serve different economic purposes:

B-CLASS DISCOUNT (0.98):
    B-class operations settle immediately (within the current SETTLEMENT_TICK).
    The 2% discount is a POLICY CHOICE, not a time-value calculation.
    Purpose: discourage agents from structuring all activity as B-class
    to capture the timing advantage of immediate settlement.
    The discount makes B-class rewards slightly less valuable per unit,
    creating mild incentive to accept V-class (verification) work instead.

V-CLASS PREMIUM ((1+r)^delay):
    V-class operations settle after N SETTLEMENT_TICKs (default N=5).
    The premium compensates for the TIME VALUE of delayed settlement.
    An agent who earns 100 AIC via V-class receives ~101 AIC after 5 ticks,
    ensuring present-value equivalence with receiving ~99 AIC immediately.
    This is a FAIR VALUE calculation: the agent's AIC is locked during
    the verification window and cannot be staked, traded, or used for
    capacity bids during that period.

WHY NOT SYMMETRIC:
    If B-class used (1+r)^0 = 1.0 (no discount), agents would prefer
    B-class for all operations (zero delay, full reward).
    If V-class used a flat discount (e.g., 0.99), the compensation would
    not scale with actual delay — longer governance proceedings would
    be systematically underpaid.

    The asymmetry ensures:
    (a) Fast settlement carries a small opportunity cost (B-class discount)
    (b) Slow settlement carries exact time-value compensation (V/G premium)
    (c) Agents are roughly indifferent between settlement classes for
        comparable work, preventing systematic gaming toward one class.

NUMERICAL EXAMPLE (r = 0.002, 5-tick V-class):
    Agent earns 100 AIC base reward.
    B-class path:  100 * 0.98 = 98 AIC received at tick 0
    V-class path:  100 * (1.002)^5 = 101.004 AIC received at tick 5
    Present value of V-class: 101.004 / (1.002)^5 = 100.0 AIC at tick 0
    Present value of B-class: 98.0 AIC at tick 0
    V-class is slightly more valuable in PV terms (100 vs 98).
    This 2% gap is the policy premium for verification work.
```

---

# F61 — Monitoring Specification (LOW)

## Problem

Monitoring flags MF-1 through MF-6 are referenced in the parameter table (lines 4904-4905) but never fully defined. This section consolidates them.

## Monitoring Flag Specification

```
MONITORING SPECIFICATION — DSF v2.0.1

Each monitoring flag defines: metric, collection frequency, threshold, escalation.

================================================================
MF-1: SETTLEMENT STALENESS
================================================================
Metric:       max(current_epoch - node.epoch_settled) across all HDL nodes
Unit:         SETTLEMENT_TICKs (epochs)
Collection:   Every SETTLEMENT_TICK (60s)
Threshold:
    WARN:     staleness >= 2 SETTLEMENT_TICKs
    ALERT:    staleness >= 3 SETTLEMENT_TICKs (locus enters DEGRADED)
    CRITICAL: staleness >= 5 SETTLEMENT_TICKs
Escalation:
    WARN:     Log + operator notification. Node attempts EpochRecovery.
    ALERT:    Governance notification. Affected locus marked DEGRADED
              (read-only). Other loci continue normally.
    CRITICAL: Emergency governance action eligible. Manual intervention required.

================================================================
MF-2: CONSERVATION DELTA
================================================================
Metric:       |aic_lhs - aic_rhs| after each eabs_conservation_check()
Unit:         AIC (absolute)
Collection:   Every SETTLEMENT_TICK (post-settlement)
Threshold:
    WARN:     delta > 0 (any non-zero delta is abnormal)
    CRITICAL: delta > 0 (immediate — conservation violations are always critical)
Escalation:
    Any non-zero delta triggers ConservationRecovery protocol (Section 9.4.1).
    This is the most severe monitoring flag. Zero tolerance.

================================================================
MF-3: CROSS-BUDGET FLOW RATIO
================================================================
Metric:       (AIC spent on self-sponsored tasks) / (total AIC settlement volume)
Unit:         Ratio [0, 1]
Collection:   Every TIDAL_EPOCH (3600s = 60 SETTLEMENT_TICKs)
Threshold:
    WARN:     ratio > 0.05 for 3 consecutive TIDAL_EPOCHs
    ALERT:    ratio > 0.10 for 5 consecutive TIDAL_EPOCHs
Escalation:
    WARN:     Log + include in treasury report.
    ALERT:    Auto-generate governance review proposal (Tier 2).
              Feeds into BM-1 budget collapse assessment (see F54).

================================================================
MF-4: MARKET CONCENTRATION (HHI)
================================================================
Metric:       Herfindahl-Hirschman Index per resource type
              HHI = Sigma(market_share_i^2) where market_share = allocated/total
Unit:         Dimensionless [0, 1]
Collection:   Every SETTLEMENT_TICK (post-clearing)
Threshold:
    WARN:     HHI > 0.25 for any resource type
    ALERT:    HHI > 0.40 for any resource type
Escalation:
    WARN:     Governance notification. Market health report generated.
    ALERT:    Emergency position limit reduction to 10% (auto-enforced).
              Governance review auto-triggered.

================================================================
MF-5: GOVERNANCE PARTICIPATION RATE
================================================================
Metric:       (governance weight that voted) / (total governance weight)
              Measured per G-class settlement period.
Unit:         Ratio [0, 1]
Collection:   Every G-class settlement (10-50 SETTLEMENT_TICKs)
Threshold:
    WARN:     participation < 0.30 for 3 consecutive G-class periods
    ALERT:    participation < 0.20 for 5 consecutive G-class periods
Escalation:
    WARN:     Stream 4 (governance) reward multiplier increased by 1.5x
              (temporary, governance-adjustable).
    ALERT:    Auto-generate governance proposal to review Stream 4 weight.
              Consider increasing from 10% to 15%.

================================================================
MF-6: PENDING STATE VOLUME
================================================================
Metric:       Sigma(pending_out) / total_aic_supply (global pending ratio)
Unit:         Ratio [0, 1]
Collection:   Every SETTLEMENT_TICK
Threshold:
    WARN:     global_pending_ratio > 0.15
    ALERT:    global_pending_ratio > 0.20 (approaching 0.25 global cap)
Escalation:
    WARN:     Log + operator notification.
              check_pending_timeouts() runs with enhanced logging.
    ALERT:    Governance notification. Pending collateral rate review.
              New PENDING_INITIATE operations throttled
              (congestion pricing multiplier applied to collateral).
```

---

# F62 — Formal Verification Scope (LOW)

## Acknowledgment and Specification

Formal verification of EABS is listed as future work (Section 15.2, item 2). This section specifies the exact properties to verify.

```
FORMAL VERIFICATION ROADMAP

Target tools: TLA+ for protocol properties, Dafny for implementation correctness.

================================================================
Property FV-1: EABS DETERMINISM
================================================================
Tool:     TLA+
Statement:
    For any two honest nodes A, B that both complete Reliable Broadcast
    for epoch E with the same broadcast_set:
        settle_epoch(pre_state, deterministic_order(broadcast_set), E)
    produces identical SettlementResult on A and B.

    Formally: deterministic_order is a total function (no randomness,
    no external state). settle_epoch is a pure function of its inputs.
    Therefore outputs are identical given identical inputs.

Verification approach:
    Model the settlement function as a TLA+ specification.
    Prove that for all possible input batches and pre-states,
    the output is uniquely determined.

================================================================
Property FV-2: CONSERVATION INVARIANT
================================================================
Tool:     Dafny (stronger guarantees for arithmetic properties)
Statement:
    For all operation types T in OperationType:
        IF CONS-1 holds for pre_state
        AND apply_operation(pre_state, op) returns Success(post_state)
        THEN CONS-1 holds for post_state

    AND:
        IF CONS-1 holds for pre_state
        AND settle_epoch(pre_state, batch, E) returns {conservation_valid: true}
        THEN CONS-1 holds for post_state

Verification approach:
    Encode CONS-1 as a Dafny predicate over SettlementState.
    For each of the 23 operation types, prove the predicate is
    preserved as a post-condition of apply_operation.
    Prove the batch-level invariant by induction.

================================================================
Property FV-3: LIVENESS UNDER f < n/3 BYZANTINE
================================================================
Tool:     TLA+
Statement:
    In a system with n nodes and at most f < n/3 Byzantine faults,
    under partial synchrony (all messages delivered within Delta
    after Global Stabilization Time):

    (a) Every epoch eventually reaches COMMITTED phase.
    (b) Bracha's RBC delivers all operations from honest senders
        to all honest receivers within bounded time.
    (c) No honest node waits indefinitely for settlement.

Verification approach:
    Model Bracha's RBC in TLA+ with fault injection.
    Prove that if f < n/3, the COMMITTED phase is eventually reached.
    Use the partial synchrony model from Dwork-Lynch-Stockmeyer.

================================================================
Property FV-4: SETTLEMENT COMPLETENESS
================================================================
Tool:     TLA+
Statement:
    For every valid operation O submitted during epoch E's COLLECTING phase:
        Either O is included in epoch E's settled batch
        OR O is rejected with a specific RejectionReason
        OR O is deferred to epoch E+1 (for cross-locus operations)

    No valid operation is silently dropped.

Verification approach:
    Model the five-phase epoch lifecycle in TLA+.
    Prove that every operation in the COLLECTING buffer either
    appears in the COMMITTED result or in the rejected list.

================================================================
Property FV-5: PENDING STATE TERMINATION
================================================================
Tool:     TLA+ or Dafny
Statement:
    Every PendingRecord transitions to a terminal state
    (COMPLETED or TIMED_OUT) within 3 SETTLEMENT_TICKs + 1
    of initiation.

    No pending state persists indefinitely.

Verification approach:
    Model the pending state machine (Section 9.3.1).
    Prove that from any non-terminal state, a terminal state
    is reached within bounded time (3 epochs for timeout).
```

---

# C9 Erratum E-C8-01: Claim Class Difficulty Weights

## Problem

Section 12.2.1 (lines 3837-3841) uses a 5-class difficulty weight table with P/R/C modifiers applied as separate multipliers:

```
D (Deterministic): 1.0    E (Empirical): 1.5
S (Statistical):   2.0    H (Heuristic): 2.5
N (Normative):     3.0
Modifiers: P (Primary) x1.0, R (Replication) x0.7, C (Challenge) x1.3
```

C9 reconciliation establishes a unified 9-class table across the Atrahasis system, replacing the 5+modifier scheme.

## Canonical 9-Class Difficulty Weight Table

The following table supersedes lines 3837-3841. Modifiers (P/R/C) are absorbed into the base weights via pre-computation. The 9 classes map directly to C5 PCVM claim classes.

```
CONST CLAIM_CLASS_DIFFICULTY_WEIGHTS = {
    D: 1.0,    // Deterministic — verifiable by recomputation
    C: 1.3,    // Challenge — contested claims requiring re-evaluation
    P: 1.5,    // Primary — first verification of novel claims
    E: 1.5,    // Empirical — requires observational evidence
    K: 1.8,    // Knowledge-synthesis — cross-domain integration (new in C9)
    S: 2.0,    // Statistical — requires sample accumulation and analysis
    R: 2.0,    // Replication — independent reproduction of prior results
    H: 2.5,    // Heuristic — expert judgment under uncertainty
    N: 3.0,    // Normative — value judgments and policy evaluation
}
```

### Migration from 5+modifier to 9-class

| Old (5+mod) | New (9-class) | Weight Change | Rationale |
|---|---|---|---|
| D-P | D | 1.0*1.0 = 1.0 -> 1.0 | Unchanged |
| D-C | C | 1.0*1.3 = 1.3 -> 1.3 | Absorbed into class C |
| E-P | P/E | 1.5*1.0 = 1.5 -> 1.5 | Split: P=primary novel, E=empirical |
| — | K | new -> 1.8 | New class for knowledge synthesis |
| S-P | S | 2.0*1.0 = 2.0 -> 2.0 | Unchanged |
| S-R | R | 2.0*0.7 = 1.4 -> 2.0 | Increased: replication undervalued in old scheme |
| H-P | H | 2.5*1.0 = 2.5 -> 2.5 | Unchanged |
| N-P | N | 3.0*1.0 = 3.0 -> 3.0 | Unchanged |

### Updated Verification Reward Computation (replaces lines 3828-3841)

```
Integration: DSF --> C5 verifiers (DSF distributes rewards)

Data Flow:
    C5 EMITS per-epoch: VerificationReport {
        verifier_id, claims_verified, accuracy_rate,
        claim_classes, vtds_completed, epoch
    }

    DSF COMPUTES verification rewards (40% of settlement pool):
        FOR each report:
            IF accuracy_rate < 0.70: quality_score = 0 (below threshold)
            ELSE:
                difficulty_weight = sum(
                    CLAIM_CLASS_DIFFICULTY_WEIGHTS[cc]
                    for cc in report.claim_classes
                )
                quality_score = accuracy_rate * difficulty_weight * vtds_completed

        Distribute pool proportionally by quality_score.

    Claim Class Difficulty Weights (9-class, per C9 E-C8-01):
        D=1.0, C=1.3, P=1.5, E=1.5, K=1.8, S=2.0, R=2.0, H=2.5, N=3.0
```

### Claim Class to Settlement Type Mapping (replaces lines 3919-3931)

```
Claim Class --> Settlement Type:
    D (Deterministic)       --> B-class fast     (verifiable by recomputation)
    C (Challenge)           --> V-class standard (contested, needs review)
    P (Primary)             --> V-class standard (novel, needs independent check)
    E (Empirical)           --> V-class standard (requires observation over time)
    K (Knowledge-synthesis) --> V-class standard (cross-domain, needs expert eval)
    S (Statistical)         --> V-class standard (requires sample accumulation)
    R (Replication)         --> V-class standard (independent reproduction)
    H (Heuristic)           --> V-class standard (requires expert review)
    N (Normative)           --> G-class slow     (involves value judgments)
```

---

# Summary of All Changes

| Finding | Severity | Type | Lines Affected | Status |
|---|---|---|---|---|
| F52 | HIGH | Epoch duration consistency | 4390, 4394, 4454, 4799, 4869 + new terminology note | PATCHED |
| F53 | MEDIUM | Conservation formula | 827-859 (Part 1 check_conservation) | PATCHED |
| F54 | MEDIUM | Budget collapse governance path | New section after 13.2 Finding 6 | ADDED |
| F55 | MEDIUM | Slashing three-way split | 705-717 (Part 1 SLASH case), 890 (proof) | PATCHED |
| F56 | MEDIUM | Failure mode catalogue | New consolidated section (20 failure modes) | ADDED |
| F57 | MEDIUM | Simplified scoring | New bootstrap scoring for Streams 3+4 | ADDED |
| F58 | LOW | AccountState reconciliation | 223-255 (Part 1), 4612-4625 (Part 2) | PATCHED |
| F59 | LOW | Settlement function completeness | 816-819 (Part 1 stub comment) | PATCHED (11 ops) |
| F60 | LOW | NPV asymmetry documentation | After line 1608 | ADDED |
| F61 | LOW | Monitoring specification | MF-1 through MF-6 | ADDED |
| F62 | LOW | Formal verification scope | After Section 15.2 | ADDED (5 properties) |
| E-C8-01 | C9 ERRATUM | 9-class difficulty weights | 3837-3841, 3919-3931 | PATCHED |

---

*End of Patch Addendum v2.0.1*
*Applies to: C8 DSF Master Tech Spec v2.0*
*Date: 2026-03-10*
