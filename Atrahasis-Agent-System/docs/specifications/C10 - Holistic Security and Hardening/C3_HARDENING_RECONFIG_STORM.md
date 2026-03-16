# C3 Tidal Noosphere -- Hardening Addendum HP-C3-01
## Reconfiguration Storm Mitigation

**Applies to:** MASTER_TECH_SPEC.md v1.0 (C3-A), as amended by PATCH_ADDENDUM_v1.1.md (PA-C3-01)
**Date:** 2026-03-10
**Status:** HARDENING ADDENDUM -- supplements base spec and patch addendum
**Scope:** CRITICAL-severity reconfiguration storm failure mode (Attack 1). Addresses the single most dangerous failure mode in the architecture: simultaneous disruption of all five subsystems during parcel split/merge events.
**Severity:** CRITICAL -- this failure mode can cause permanent degraded state if left unmitigated
**Predecessor:** PA-F5 (PTP Clarification), PA-F15 (In-Flight Surprise Signals)

---

## Table of Contents

- [HP-1: Storm Detection and Throttling](#hp-1-storm-detection-and-throttling)
- [HP-2: Staggered Reconfiguration Protocol](#hp-2-staggered-reconfiguration-protocol)
- [HP-3: VRF Committee Cache Invalidation Protocol](#hp-3-vrf-committee-cache-invalidation-protocol)
- [HP-4: Predictive Model Migration](#hp-4-predictive-model-migration)
- [HP-5: Governance Quorum Protection](#hp-5-governance-quorum-protection)
- [HP-6: Cross-Integration Failure Ordering](#hp-6-cross-integration-failure-ordering)
- [HP-7: Conformance Amendments](#hp-7-conformance-amendments)
- [HP-8: Validation Requirements](#hp-8-validation-requirements)

---

## Problem Statement

When parcels split or merge (reconfiguration), five subsystems are disrupted simultaneously:

1. **Hash ring reconstruction** -- all task assignments are invalidated; scheduling breaks until rings rebuild.
2. **VRF committee caching** -- cached verifier sets reference agents who are no longer in the parcel; in-progress verifications may target wrong agents.
3. **Predictive model cold-start** -- all agents lose their neighbor behavioral models; communication spikes from zero to O(N) per agent.
4. **Communication routing** -- surprise signals in transit may target agents who have moved to a different parcel.
5. **Governance quorum** -- if reconfiguration occurs during a vote, the quorum denominator changes mid-vote, potentially invalidating an ongoing decision.

A single large-scale agent churn event (e.g., 20% of agents departing a locus within one epoch) can trigger ALL FIVE disruptions simultaneously. The system degrades on every axis at once. This is the "reconfiguration storm."

The base spec (Section 7.4) addresses this with PTP's 2-phase protocol + convergence period, plus staggering guards (20% max concurrent reconfiguration, 10-epoch minimum interval, 30% circuit breaker). The patch addendum (PA-F5, PA-F15) clarifies PTP structure and in-flight signal routing. However, the base spec treats the five disruptions as a single atomic event in the MIGRATE phase. This addendum separates them into a staggered sequence, adds storm detection and throttling, and provides concrete protocols for each subsystem's recovery.

**Relationship to GATE-1.** This addendum specifies the mechanisms that GATE-1 will validate. GATE-1's kill criterion (recovery time > 10 epochs at 100+ parcels) applies to the staggered protocol defined here. If GATE-1 fails with this protocol, the architecture requires fundamental redesign.

---

## HP-1: Storm Detection and Throttling

### HP-1.1 Storm Condition Definition

A reconfiguration storm is declared when the system detects that the volume of simultaneous or near-simultaneous parcel reconfigurations exceeds the architecture's ability to recover before the next churn event arrives. Two independent triggers define the storm condition:

**Trigger S1 -- Parcel Fraction Trigger:**
More than STORM_PARCEL_FRACTION of parcels in a locus are simultaneously in a non-ACTIVE state (PREPARING, MIGRATING, or CONVERGING per PA-F5 state machine).

**Trigger S2 -- Agent Transition Trigger:**
More than STORM_AGENT_FRACTION of agents across all parcels in a locus are in TRANSITIONING communication mode (meaning their predictive models have been reset and they are operating in standard messaging).

```
// New configurable constants
// #50: STORM_PARCEL_FRACTION    default: 0.15   range: [0.05, 0.30]
// #51: STORM_AGENT_FRACTION     default: 0.25   range: [0.10, 0.50]
// #52: STORM_THROTTLE_MAX       default: 3      range: [1, 10]
//      Max new reconfigurations per tidal epoch per locus during storm
// #53: STORM_COOLDOWN_EPOCHS    default: 5      range: [2, 20]
//      Epochs after storm condition clears before normal throttling resumes
// #54: STORM_QUEUE_MAX          default: 50     range: [10, 200]
//      Maximum queued reconfigurations before forced rejection
```

### HP-1.2 Storm Detector

```
StormState := {
  locus:              LocusId
  storm_active:       bool
  storm_start_epoch:  uint64 | null
  storm_clear_epoch:  uint64 | null
  queued_reconfigs:   Queue<ReconfigDirective>
  throttle_counter:   uint32          // reconfigs initiated this epoch
  consecutive_clear:  uint32          // consecutive epochs below both triggers
}

function evaluate_storm_condition(
  locus: Locus,
  epoch: uint64,
  storm_state: StormState
) -> StormState:

  // Count parcels in non-ACTIVE state
  non_active_parcels = count(
    p for p in locus.parcels
    if p.state in {PREPARING, MIGRATING, CONVERGING}
  )
  parcel_fraction = non_active_parcels / |locus.parcels|

  // Count agents in TRANSITIONING mode
  transitioning_agents = count(
    a for a in all_agents(locus)
    if a.communication_mode == TRANSITIONING
  )
  total_agents = count(all_agents(locus))
  agent_fraction = transitioning_agents / total_agents

  // Evaluate triggers
  s1_triggered = parcel_fraction > STORM_PARCEL_FRACTION
  s2_triggered = agent_fraction > STORM_AGENT_FRACTION

  if s1_triggered or s2_triggered:
    if not storm_state.storm_active:
      // Storm onset
      storm_state.storm_active = true
      storm_state.storm_start_epoch = epoch
      storm_state.consecutive_clear = 0
      emit_stigmergic_signal(
        type = ANOMALY,
        scope = locus,
        confidence = max(parcel_fraction, agent_fraction),
        decay_tau = 14400,
        payload = StormOnsetPayload{
          trigger = S1 if s1_triggered else S2,
          parcel_fraction = parcel_fraction,
          agent_fraction = agent_fraction
        }
      )
      log_storm_event(locus, epoch, "STORM_ONSET",
        parcel_fraction, agent_fraction)
    storm_state.consecutive_clear = 0
  else:
    if storm_state.storm_active:
      storm_state.consecutive_clear += 1
      if storm_state.consecutive_clear >= STORM_COOLDOWN_EPOCHS:
        // Storm cleared
        storm_state.storm_active = false
        storm_state.storm_clear_epoch = epoch
        storm_state.consecutive_clear = 0
        log_storm_event(locus, epoch, "STORM_CLEARED",
          parcel_fraction, agent_fraction)

  // Reset per-epoch throttle counter
  storm_state.throttle_counter = 0

  return storm_state
```

### HP-1.3 Throttle and Queue

When a storm is active, new reconfiguration requests are throttled and queued rather than rejected outright. This prevents cascading failures where load-driven reconfigurations are permanently suppressed, causing the load imbalance that triggered them to worsen.

```
function request_reconfiguration(
  directive: ReconfigDirective,
  locus: Locus,
  storm_state: StormState,
  epoch: uint64
) -> ReconfigDecision:

  // Pre-storm guard: base spec's 20% cap still applies
  if not storm_state.storm_active:
    non_active = count(p for p in locus.parcels
                       if p.state != ACTIVE)
    if (non_active + |directive.affected_parcels|) / |locus.parcels| > 0.20:
      return QUEUE(directive, reason="BASE_SPEC_20_PERCENT_CAP")

    // Base spec's minimum interval still applies
    for parcel in directive.affected_parcels:
      if parcel.last_reconfig_epoch is not null:
        if epoch - parcel.last_reconfig_epoch < RECONFIG_MIN_INTERVAL:
          return QUEUE(directive, reason="MIN_INTERVAL_NOT_MET")

    return APPROVE(directive)

  // Storm is active: apply throttling
  if storm_state.throttle_counter >= STORM_THROTTLE_MAX:
    if |storm_state.queued_reconfigs| >= STORM_QUEUE_MAX:
      // Queue is full: reject with backpressure signal
      emit_stigmergic_signal(
        type = RISK,
        scope = locus,
        confidence = 1.0,
        decay_tau = 7200,
        payload = QueueFullPayload{
          queue_depth = |storm_state.queued_reconfigs|,
          rejected_directive = directive.id
        }
      )
      return REJECT(directive, reason="STORM_QUEUE_FULL")

    // Queue for next epoch
    storm_state.queued_reconfigs.enqueue(directive)
    return QUEUE(directive, reason="STORM_THROTTLE_ACTIVE")

  // Under throttle limit: approve but count
  storm_state.throttle_counter += 1
  return APPROVE(directive)


function drain_storm_queue(
  locus: Locus,
  storm_state: StormState,
  epoch: uint64
) -> List<ReconfigDirective>:
  // Called at each epoch boundary during storm
  // Releases up to STORM_THROTTLE_MAX queued reconfigurations

  released = []
  while (|released| < STORM_THROTTLE_MAX
         and not storm_state.queued_reconfigs.empty()):
    directive = storm_state.queued_reconfigs.peek()

    // Check if still valid (parcels may have changed since queuing)
    if is_directive_still_valid(directive, locus, epoch):
      storm_state.queued_reconfigs.dequeue()
      released.append(directive)
    else:
      // Stale directive: discard
      storm_state.queued_reconfigs.dequeue()
      log_stale_directive(directive, epoch)

  return released


function is_directive_still_valid(
  directive: ReconfigDirective,
  locus: Locus,
  epoch: uint64
) -> bool:
  // A queued directive expires after DIRECTIVE_TTL epochs
  DIRECTIVE_TTL = 10    // range [5, 30]
  if epoch - directive.submitted_epoch > DIRECTIVE_TTL:
    return false

  // All affected parcels must still exist and be ACTIVE
  for parcel_id in directive.affected_parcels:
    parcel = locus.get_parcel(parcel_id)
    if parcel is null or parcel.state != ACTIVE:
      return false

  return true
```

### HP-1.4 Circuit Breaker Enhancement

The base spec defines a circuit breaker at 30% TRANSITIONING parcels. This addendum adds a graduated response:

```
function evaluate_circuit_breaker(
  locus: Locus,
  storm_state: StormState
) -> CircuitBreakerAction:

  non_active_fraction = count(
    p for p in locus.parcels if p.state != ACTIVE
  ) / |locus.parcels|

  if non_active_fraction >= 0.30:
    // HARD HALT: base spec circuit breaker
    // No new reconfigurations until fraction drops below 0.20
    return HALT_ALL_RECONFIGURATIONS

  if non_active_fraction >= 0.20:
    // SOFT HALT: allow only queue drains, no new requests
    return DRAIN_ONLY

  if storm_state.storm_active:
    // THROTTLED: storm-limited operation
    return THROTTLED

  // NORMAL: base spec guards apply
  return NORMAL
```

---

## HP-2: Staggered Reconfiguration Protocol

### HP-2.1 Design Rationale

The base spec's PTP MIGRATE phase performs five state changes atomically at the epoch boundary: hash ring reconstruction, VRF set invalidation, predictive model reset, signal queue flush, and parcel state update. While this atomicity simplifies reasoning, it means all five subsystems enter their recovery phase simultaneously. The staggered protocol separates these into four time-sequential phases, each completing before the next begins. This ensures that at any given moment, at most two subsystems are in a degraded state.

**Key constraint:** The staggered protocol MUST NOT violate the determinism invariant (INV-2). All agents must independently compute the same state transitions at the same ticks. The staggering is defined relative to the MIGRATE epoch boundary, so all agents agree on the timing.

**Tick definition:** Within each epoch, the system defines TICKS_PER_EPOCH logical ticks (default: 60). Each tick corresponds to EPOCH_DURATION / TICKS_PER_EPOCH wall-clock seconds. For the default 3600s epoch, each tick is 60 seconds. Ticks provide sub-epoch timing granularity for the staggered protocol without requiring consensus on sub-epoch events -- all agents compute tick boundaries from the shared epoch clock.

```
// New configurable constant
// #55: TICKS_PER_EPOCH     default: 60    range: [20, 120]

function current_tick(epoch: uint64) -> uint32:
  tick_duration = EPOCH_DURATION / TICKS_PER_EPOCH
  elapsed = ntp_time() - (GENESIS_TIME + epoch * EPOCH_DURATION)
  return min(floor(elapsed / tick_duration), TICKS_PER_EPOCH - 1)
```

### HP-2.2 Staggered Phase Definitions

The staggered protocol replaces the monolithic MIGRATE action with four sequential phases. Each phase has explicit entry conditions, invariants that hold during the phase, and completion criteria.

```
StaggeredPhase := enum {
  PHASE_A_RINGS,        // tick 1-10:  Hash ring reconstruction
  PHASE_B_VRF,          // tick 11-20: VRF committee refresh
  PHASE_C_PREDICTIVE,   // tick 21-40: Predictive model warm-up
  PHASE_D_NORMAL        // tick 41-60: Normal operation resumes
}

ParcelReconfigState := {
  parcel_id:          ParcelId
  directive:          ReconfigDirective
  prepare_epoch:      uint64            // epoch when PREPARE entered
  migrate_epoch:      uint64            // epoch when MIGRATE begins
  current_phase:      StaggeredPhase
  phase_entry_tick:   uint32
  old_ring_snapshot:  Map<TaskType, HashRing>
  old_vrf_cache:      Map<ClaimHash, VerifierSet>
  old_roster:         Set<AgentId>
  new_roster:         Set<AgentId>
  model_summaries:    Map<AgentId, CompressedModelSummary>
  frozen_quorums:     Map<VoteId, FrozenQuorum>
}
```

### HP-2.3 Phase A: Hash Ring Reconstruction (Ticks 1-10)

During Phase A, only the hash rings are rebuilt. All other subsystems continue operating on the pre-reconfiguration state. This means scheduling breaks temporarily but verification, communication, and governance continue uninterrupted.

```
function execute_phase_a(
  parcel: Parcel,
  reconfig: ParcelReconfigState,
  tick: uint32
):
  // ENTRY (tick 1): Begin ring reconstruction
  if tick == reconfig.phase_entry_tick:
    // Snapshot old rings for fallback
    reconfig.old_ring_snapshot = deep_copy(parcel.hash_rings)

    // Compute new roster from reconfiguration directive
    reconfig.new_roster = compute_new_roster(
      reconfig.old_roster, reconfig.directive
    )

    // Build new hash rings for all task types
    for task_type in parcel.active_task_types():
      new_ring = build_ring(
        Parcel{agents = reconfig.new_roster},
        task_type
      )
      parcel.hash_rings[task_type] = new_ring

    // All agents independently compute identical rings
    // because inputs (new_roster, task_types) are deterministic
    // from the reconfiguration directive received during PREPARE.

  // INVARIANTS during Phase A (ticks 1-10):
  //   - NEW hash rings are active for scheduling
  //   - OLD VRF committees remain valid (Phase B has not started)
  //   - OLD predictive models remain active (Phase C has not started)
  //   - Communication uses standard messaging for agents whose
  //     scheduling changed (new ring positions differ from old)
  //   - Governance operates normally on old quorum

  // COMPLETION (tick 10): Verify ring consistency
  if tick == 10:
    // All agents should have built identical rings
    ring_hash = SHA256(canonical_serialize(parcel.hash_rings))
    // Ring hash is deterministic; no verification needed
    // (identical inputs guarantee identical outputs per INV-2)

    reconfig.current_phase = PHASE_B_VRF
    reconfig.phase_entry_tick = 11
    log_phase_transition(parcel, PHASE_A_RINGS, PHASE_B_VRF, tick)


function scheduling_lookup_during_phase_a(
  parcel: Parcel,
  reconfig: ParcelReconfigState,
  task_key: bytes,
  task_type: TaskType,
  tick: uint32
) -> AgentId:
  // During ticks 1-10, use the NEW ring for task assignment.
  // Agents that were assigned tasks on the OLD ring but are no longer
  // in the parcel have their tasks reassigned via the substitution list.

  new_ring = parcel.hash_rings[task_type]
  assigned = lookup(new_ring, task_key)

  if assigned in reconfig.new_roster:
    return assigned

  // Agent departed: walk substitution list
  return find_substitute(new_ring, task_key, reconfig.new_roster)
```

### HP-2.4 Phase B: VRF Committee Refresh (Ticks 11-20)

Phase B invalidates cached VRF committee assignments and rebuilds them using the new roster. During this phase, hash rings are fully operational (Phase A complete) and predictive models remain on the old state (Phase C has not started).

```
function execute_phase_b(
  parcel: Parcel,
  reconfig: ParcelReconfigState,
  tick: uint32
):
  // ENTRY (tick 11): Begin VRF refresh
  if tick == 11:
    // Snapshot old VRF cache for in-progress verifications
    reconfig.old_vrf_cache = deep_copy(parcel.vrf_committee_cache)

    // Rebuild eligible verifier set from new roster
    new_eligible = {
      agent for agent in reconfig.new_roster
      if agent.diversity_attr.revealed
      and agent.diversity_attr.cooling_until <= current_epoch()
    }

    // Rebuild diversity pools (if in COMMITTED or FULL_DUAL_DEFENSE phase)
    if determine_vrf_phase(parcel.locus) != SIMPLE:
      parcel.diversity_pools = build_diversity_pools(
        new_eligible, parcel.locus
      )

    // Invalidate all cached committee assignments
    // (see HP-3 for detailed invalidation protocol)
    invalidate_vrf_cache(parcel, reconfig)

    // New VRF seed is already available (computed at epoch boundary)
    // New committees will be computed on demand for new verification
    // requests using the new roster

  // INVARIANTS during Phase B (ticks 11-20):
  //   - NEW hash rings are active (Phase A complete)
  //   - In-progress verifications use OLD committees (see HP-3)
  //   - NEW verifications use freshly computed committees from new roster
  //   - OLD predictive models remain active (Phase C has not started)
  //   - Governance operates normally

  // COMPLETION (tick 20):
  if tick == 20:
    // Verify: all in-progress verifications from before tick 11
    // have either completed or timed out
    stale_verifications = count(
      v for v in parcel.active_verifications
      if v.committee_epoch < reconfig.migrate_epoch
    )
    if stale_verifications > 0:
      // Extend Phase B by up to 5 additional ticks
      if tick < 25:
        return  // stay in Phase B
      else:
        // Force-expire stale verifications
        for v in parcel.active_verifications:
          if v.committee_epoch < reconfig.migrate_epoch:
            v.status = EXPIRED_DURING_RECONFIG
            log_forced_expiry(v, parcel, tick)

    reconfig.current_phase = PHASE_C_PREDICTIVE
    reconfig.phase_entry_tick = max(tick + 1, 21)
    log_phase_transition(parcel, PHASE_B_VRF, PHASE_C_PREDICTIVE, tick)
```

### HP-2.5 Phase C: Predictive Model Warm-Up (Ticks 21-40)

Phase C handles the predictive model reset and warm-up. During this phase, hash rings and VRF committees are fully operational. Communication falls back to full standard messaging for agents in the reconfiguring parcel.

```
function execute_phase_c(
  parcel: Parcel,
  reconfig: ParcelReconfigState,
  tick: uint32
):
  // ENTRY (tick 21): Begin predictive model migration
  if tick == 21:
    // For agents LEAVING this parcel: serialize model summaries
    departing = reconfig.old_roster - reconfig.new_roster
    for agent_id in departing:
      summary = serialize_model_summary(agent_id, parcel)
      reconfig.model_summaries[agent_id] = summary
      // Summary is transmitted to the agent's new parcel via the
      // model migration protocol (HP-4)

    // For agents ARRIVING in this parcel: receive model summaries
    arriving = reconfig.new_roster - reconfig.old_roster
    for agent_id in arriving:
      // Check if a model summary was received during PREPARE
      if agent_id in reconfig.model_summaries:
        warm_start_models(agent_id, parcel,
                          reconfig.model_summaries[agent_id])
      else:
        // Cold start: no summary available
        cold_start_models(agent_id, parcel)

    // Mark all models in this parcel as TRANSITIONING
    for agent in parcel.agents:
      for model in agent.predictive_models.values():
        model.mode = TRANSITIONING

    // Communication falls back to standard messaging
    parcel.communication_mode = STANDARD_BROADCAST

  // ONGOING (ticks 21-40): Models warm up via observation
  if 21 <= tick <= 40:
    // Each tick, agents observe neighbor behavior and update models
    for agent in parcel.agents:
      for neighbor in parcel.agents:
        if neighbor.id == agent.id: continue
        model = agent.predictive_models[neighbor.id]
        if model.mode == TRANSITIONING:
          observation = observe(agent, neighbor)
          model.update(observation)
          if model.accuracy >= ACTIVATION_THRESHOLD:  // 0.7
            model.consecutive_accurate += 1
            if model.consecutive_accurate >= 3:
              model.mode = PREDICTIVE
              model.consecutive_accurate = 0
          else:
            model.consecutive_accurate = 0

  // INVARIANTS during Phase C (ticks 21-40):
  //   - NEW hash rings are active (Phase A complete)
  //   - NEW VRF committees are active (Phase B complete)
  //   - Predictive models are warming up; communication is standard broadcast
  //   - Governance operates normally
  //   - Communication overhead is elevated (2-5x steady state)

  // COMPLETION (tick 40):
  if tick == 40:
    // Count how many agents have transitioned to PREDICTIVE mode
    predictive_count = count(
      a for a in parcel.agents
      if all(m.mode == PREDICTIVE
             for m in a.predictive_models.values())
    )
    predictive_fraction = predictive_count / |parcel.agents|

    if predictive_fraction >= 0.90:
      // Normal transition to Phase D
      reconfig.current_phase = PHASE_D_NORMAL
      parcel.communication_mode = PREDICTIVE_DELTA
      log_phase_transition(parcel, PHASE_C_PREDICTIVE, PHASE_D_NORMAL, tick)
    else:
      // Extend Phase C into next epoch if needed
      // Models continue warming up; Phase D begins when 90% threshold met
      // or at tick 60 (forced transition), whichever comes first
      log_extended_warmup(parcel, predictive_fraction, tick)
```

### HP-2.6 Phase D: Normal Operation (Ticks 41-60)

```
function execute_phase_d(
  parcel: Parcel,
  reconfig: ParcelReconfigState,
  tick: uint32
):
  // ENTRY (tick 41 or earlier if all phases completed early):
  if tick == reconfig.phase_entry_tick:
    // All subsystems operational on new configuration
    parcel.state = ACTIVE
    parcel.communication_mode = PREDICTIVE_DELTA

    // Clear reconfiguration state
    reconfig.old_ring_snapshot = null
    reconfig.old_vrf_cache = null
    reconfig.model_summaries = null

    // Unfreeze governance quorums (HP-5)
    unfreeze_quorums(parcel, reconfig.frozen_quorums)

    log_phase_transition(parcel, PHASE_C_PREDICTIVE, PHASE_D_NORMAL, tick)

  // Remaining agents still in TRANSITIONING mode continue warming up
  // individually (per PA-F5 convergence period semantics)

  // FORCED COMPLETION (tick 60 / epoch end):
  if tick >= TICKS_PER_EPOCH - 1:
    // Any remaining TRANSITIONING models are force-transitioned
    // to PREDICTIVE with low confidence
    for agent in parcel.agents:
      for model in agent.predictive_models.values():
        if model.mode == TRANSITIONING:
          model.mode = PREDICTIVE
          model.accuracy = 0.5  // low confidence
          model.threshold = THRESHOLD_MAX * 0.8  // loose threshold
          log_forced_model_transition(agent, model)
```

### HP-2.7 Staggered Protocol State Machine

```
Staggered Reconfiguration State Machine:
=========================================

  ACTIVE
    |
    | [reconfiguration directive from bi-timescale controller]
    | [guard: storm throttle approves, base spec guards pass]
    v
  PREPARING (1 epoch, per PA-F5)
    |
    | [epoch boundary]
    v
  PHASE_A_RINGS (ticks 1-10)
    |  - Hash rings rebuilt from new roster
    |  - Old VRF, old models, old governance: unchanged
    |  - Scheduling: new rings active
    v
  PHASE_B_VRF (ticks 11-20, extendable to 25)
    |  - VRF cache invalidated, new committees on demand
    |  - In-progress verifications use old committees
    |  - Old models, old governance: unchanged
    v
  PHASE_C_PREDICTIVE (ticks 21-40, extendable to epoch end)
    |  - Models reset and warming up
    |  - Communication: standard broadcast
    |  - Hash rings, VRF: fully operational on new config
    v
  PHASE_D_NORMAL (ticks 41-60)
    |  - All subsystems operational on new configuration
    |  - Remaining TRANSITIONING models converge individually
    v
  ACTIVE

  Phase timing guarantees:
    - Phase A: exactly 10 ticks (deterministic ring rebuild)
    - Phase B: 10 ticks minimum, up to 15 if stale verifications pending
    - Phase C: 20 ticks minimum, extended if <90% models converged
    - Phase D: remainder of epoch
    - Total: 1 epoch (PREPARE) + 1 epoch (MIGRATE with staggering) = 2 epochs
    - Convergence: 2-5 additional epochs for remaining model warm-up

  Degradation at each phase:
    Phase A: scheduling disrupted, all else normal
    Phase B: VRF refreshing, scheduling normal, all else normal
    Phase C: communication elevated, scheduling + VRF normal
    Phase D: all normal, residual model convergence
```

---

## HP-3: VRF Committee Cache Invalidation Protocol

### HP-3.1 Cache Structure

Each parcel maintains a cache of recently computed VRF committee assignments to avoid recomputing committees for claims that are still in their verification window.

```
VRFCacheEntry := {
  claim_hash:       bytes[32]
  epoch_computed:    uint64
  committee:        Set<AgentId>
  proofs:           List<VRFProof>
  roster_snapshot:  Set<AgentId>     // roster at computation time
  status:           {VALID, STALE, EXPIRED}
  stale_since:      uint64 | null    // tick when marked stale
}

VRFCommitteeCache := {
  parcel_id:        ParcelId
  entries:          Map<bytes[32], VRFCacheEntry>
  max_entries:      uint32           // default 1000
  ttl_epochs:       uint32           // default 3
}
```

### HP-3.2 Invalidation Logic

When a parcel boundary changes during Phase B of the staggered protocol, the cache must be invalidated. However, in-progress verifications that were initiated before the boundary change must complete using their original committee -- changing the committee mid-verification would violate the verification membrane's integrity guarantees.

```
function invalidate_vrf_cache(
  parcel: Parcel,
  reconfig: ParcelReconfigState
):
  // Step 1: Identify which cache entries are affected
  // An entry is affected if ANY member of its committee has left the parcel
  departed_agents = reconfig.old_roster - reconfig.new_roster

  for (claim_hash, entry) in parcel.vrf_cache.entries:
    committee_departed = entry.committee & departed_agents

    if |committee_departed| == 0:
      // Committee is intact: entry remains VALID
      continue

    // Step 2: Determine if verification is in progress
    verification = get_active_verification(claim_hash, parcel)

    if verification is not null and verification.status == IN_PROGRESS:
      // IN-PROGRESS VERIFICATION: mark entry as STALE but do not invalidate
      // The verification continues with the original committee.
      // Rationale: The committee was legitimately selected before the
      // boundary change. Invalidating mid-verification would require
      // restarting the verification, wasting the work already done and
      // potentially allowing a timing attack (force reconfiguration to
      // reset unfavorable committee).
      entry.status = STALE
      entry.stale_since = current_tick()
      log_stale_cache_entry(claim_hash, committee_departed,
                            "IN_PROGRESS_VERIFICATION_PRESERVED")

    else:
      // NO IN-PROGRESS VERIFICATION: invalidate the entry
      entry.status = EXPIRED
      parcel.vrf_cache.entries.remove(claim_hash)
      log_invalidated_cache_entry(claim_hash, committee_departed)


function resolve_committee_for_new_verification(
  claim: Claim,
  parcel: Parcel,
  epoch: uint64,
  reconfig: ParcelReconfigState | null
) -> (Set<AgentId>, List<VRFProof>):

  // Check cache first
  cached = parcel.vrf_cache.entries.get(claim.hash)
  if cached is not null and cached.status == VALID:
    return (cached.committee, cached.proofs)

  // Cache miss or stale: compute fresh committee from CURRENT roster
  vrf_seed = get_vrf_seed(epoch, parcel.id)

  // Use the appropriate VRF phase algorithm (per PA-F4)
  vrf_phase = determine_vrf_phase(parcel.locus)
  if vrf_phase == SIMPLE:
    (committee, proofs) = select_verifiers_simple(
      claim, epoch, vrf_seed, parcel.agents, COMMITTEE_SIZE)
  elif vrf_phase == COMMITTED:
    (committee, proofs) = select_verifiers_committed(
      claim, epoch, vrf_seed, parcel.agents, COMMITTEE_SIZE)
  else:
    (committee, proofs) = select_diverse_verifiers(
      claim, epoch, vrf_seed, parcel.diversity_pools,
      parcel.locus, COMMITTEE_SIZE)

  // Cache the result
  parcel.vrf_cache.entries[claim.hash] = VRFCacheEntry{
    claim_hash = claim.hash,
    epoch_computed = epoch,
    committee = committee,
    proofs = proofs,
    roster_snapshot = set(parcel.agents),
    status = VALID,
    stale_since = null
  }

  return (committee, proofs)
```

### HP-3.3 Stale Entry Resolution

Stale entries (in-progress verifications using old committees) must eventually resolve. The protocol defines a bounded window for stale entry completion.

```
// New configurable constant
// #56: STALE_VRF_MAX_TICKS    default: 30   range: [10, 60]
//      Maximum ticks a STALE cache entry persists before forced expiry

function resolve_stale_entries(
  parcel: Parcel,
  tick: uint32
):
  for (claim_hash, entry) in parcel.vrf_cache.entries:
    if entry.status != STALE:
      continue

    elapsed = tick - entry.stale_since
    verification = get_active_verification(claim_hash, parcel)

    // Case 1: Verification completed normally
    if verification is null or verification.status in {VERIFIED, REJECTED}:
      entry.status = EXPIRED
      parcel.vrf_cache.entries.remove(claim_hash)
      log_stale_resolved(claim_hash, "VERIFICATION_COMPLETED")

    // Case 2: Verification still in progress but within time bound
    elif elapsed < STALE_VRF_MAX_TICKS:
      // Let it continue -- the original committee is still working
      continue

    // Case 3: Verification exceeded stale time bound
    else:
      // Force-expire the stale entry and restart verification
      entry.status = EXPIRED
      parcel.vrf_cache.entries.remove(claim_hash)

      // Restart verification with new committee from current roster
      restart_verification(claim_hash, parcel,
        reason="STALE_VRF_TIMEOUT",
        original_committee = entry.committee,
        new_committee = resolve_committee_for_new_verification(
          get_claim(claim_hash), parcel, current_epoch(), null
        )
      )
      log_stale_resolved(claim_hash, "FORCED_RESTART")
```

---

## HP-4: Predictive Model Migration

### HP-4.1 Compressed Model Summary

When an agent moves from parcel A to parcel B, it carries a compressed summary of its behavioral statistics from the last N epochs. This summary enables the new parcel's members to initialize their predictive models with a "warm start" instead of cold start, reducing convergence time from 10-15 epochs to 3-5 epochs.

```
CompressedModelSummary := {
  agent_id:               AgentId
  source_parcel:          ParcelId
  epoch_range:            (uint64, uint64)  // (oldest, newest)
  summary_version:        uint8             // schema version for forward compat

  // Behavioral statistics (last MIGRATION_LOOKBACK epochs)
  task_completion_rate:    RunningStats      // mean, variance, min, max
  surprise_frequency:     RunningStats
  resource_consumption:   RunningStats
  scheduling_compliance:  RunningStats
  verification_quality:   RunningStats

  // Communication pattern summary
  avg_surprises_emitted:  float64
  avg_surprises_received: float64
  dominant_surprise_types: List<(SurpriseType, float64)>  // top 3 by frequency

  // Capability profile (does not change, but new parcel needs it)
  capabilities:           Set<TaskType>
  capacity:               float64

  // Compressed weight vector from the agent's own predictive model
  // (optional -- only included if agent consents to model sharing)
  self_model_weights:     bytes | null    // compressed, max 256 bytes

  // Integrity
  signature:              bytes[64]       // agent's ed25519 signature
  total_size:             uint32          // MUST be <= 1024 bytes
}

RunningStats := {
  mean:     float64
  variance: float64
  min:      float64
  max:      float64
  n:        uint32       // sample count
}

// New configurable constant
// #57: MIGRATION_LOOKBACK     default: 10    range: [3, 30]
//      Number of epochs of behavioral history in migration summary
```

### HP-4.2 Summary Serialization (Departing Agent)

```
function serialize_model_summary(
  agent_id: AgentId,
  source_parcel: Parcel
) -> CompressedModelSummary:

  agent = get_agent(agent_id)
  lookback = min(MIGRATION_LOOKBACK, agent.epochs_in_parcel)

  summary = CompressedModelSummary{
    agent_id = agent_id,
    source_parcel = source_parcel.id,
    epoch_range = (current_epoch() - lookback, current_epoch()),
    summary_version = 1,

    task_completion_rate = compute_running_stats(
      agent.history.completion_rates[-lookback:]),
    surprise_frequency = compute_running_stats(
      agent.history.surprise_frequencies[-lookback:]),
    resource_consumption = compute_running_stats(
      agent.history.resource_consumption[-lookback:]),
    scheduling_compliance = compute_running_stats(
      agent.history.compliance_scores[-lookback:]),
    verification_quality = compute_running_stats(
      agent.history.verification_quality[-lookback:]),

    avg_surprises_emitted = mean(
      agent.history.surprises_emitted[-lookback:]),
    avg_surprises_received = mean(
      agent.history.surprises_received[-lookback:]),
    dominant_surprise_types = top_k(
      agent.history.surprise_type_counts[-lookback:], k=3),

    capabilities = agent.capabilities,
    capacity = agent.capacity,

    self_model_weights = compress_weights(agent.self_model)
      if agent.consents_to_model_sharing else null,

    signature = ed25519_sign(agent.privkey, canonical_serialize(summary_body)),
    total_size = 0  // computed after serialization
  }

  serialized = canonical_serialize(summary)
  assert |serialized| <= 1024,
    "Model summary exceeds 1KB limit: " + str(|serialized|)
  summary.total_size = |serialized|

  return summary


function compute_running_stats(values: List<float64>) -> RunningStats:
  return RunningStats{
    mean = mean(values),
    variance = variance(values),
    min = min(values),
    max = max(values),
    n = |values|
  }
```

### HP-4.3 Warm-Start Algorithm (Receiving Parcel)

```
function warm_start_models(
  arriving_agent_id: AgentId,
  dest_parcel: Parcel,
  summary: CompressedModelSummary
):
  // Validate summary integrity
  agent = get_agent(arriving_agent_id)
  assert arriving_agent_id == summary.agent_id
  assert verify_signature(agent.pubkey, summary.signature,
                          canonical_serialize(summary_body))

  // Validate freshness: summary must be from within MIGRATION_LOOKBACK epochs
  assert current_epoch() - summary.epoch_range[1] <= MIGRATION_LOOKBACK

  // Step 1: Initialize models for existing parcel members -> arriving agent
  // Each agent in the destination parcel creates a predictive model for
  // the arriving agent, initialized from the summary
  for existing_agent in dest_parcel.agents:
    if existing_agent.id == arriving_agent_id: continue

    model = PredictiveModel{
      neighbor = arriving_agent_id,
      // Initialize weights from behavioral summary
      weights = prior_from_summary(summary),
      // Start with moderate accuracy -- summary gives us a head start
      // but is not direct observation
      accuracy = 0.5,
      // Use moderate threshold -- not as loose as cold start (THRESHOLD_MAX)
      // but not as tight as established models
      threshold = THRESHOLD_MAX * 0.6,
      error_history = [],
      mode = TRANSITIONING,
      warm_start_source = summary.source_parcel,
      consecutive_accurate = 0
    }
    existing_agent.predictive_models[arriving_agent_id] = model

  // Step 2: Initialize models for arriving agent -> existing parcel members
  // The arriving agent has no observations of its new neighbors. It uses
  // the cold-start burst from PA-F15 (which provides parcel-level summary
  // statistics) as its only baseline.
  arriving = get_agent(arriving_agent_id)
  for existing_agent in dest_parcel.agents:
    if existing_agent.id == arriving_agent_id: continue

    model = PredictiveModel{
      neighbor = existing_agent.id,
      weights = default_weights(),   // no information about existing members
      accuracy = 0.3,
      threshold = THRESHOLD_MAX * 0.8,
      error_history = [],
      mode = TRANSITIONING,
      warm_start_source = null,       // no summary available for this direction
      consecutive_accurate = 0
    }
    arriving.predictive_models[existing_agent.id] = model

  // Step 3: Send cold-start burst to arriving agent (per PA-F15)
  send_cold_start_burst(arriving_agent_id, dest_parcel,
                        dest_parcel.signal_aggregator)


function prior_from_summary(
  summary: CompressedModelSummary
) -> WeightVector:
  // Convert behavioral statistics to initial weight vector
  // The weight vector predicts: [completion_rate, surprise_freq,
  //   resource_consumption, compliance, verification_quality]

  weights = WeightVector{
    completion_rate_w = summary.task_completion_rate.mean,
    surprise_freq_w = summary.surprise_frequency.mean,
    resource_w = summary.resource_consumption.mean,
    compliance_w = summary.scheduling_compliance.mean,
    verification_w = summary.verification_quality.mean,
    // Confidence scaling: higher variance in historical data
    // means lower confidence in the prior
    confidence_scale = 1.0 / (1.0 + mean_variance(summary))
  }

  // If the agent shared its self-model weights, blend them
  if summary.self_model_weights is not null:
    self_weights = decompress_weights(summary.self_model_weights)
    weights = blend(weights, self_weights,
                    alpha=0.3)  // 30% self-model, 70% behavioral summary

  return weights


function cold_start_models(
  arriving_agent_id: AgentId,
  dest_parcel: Parcel
):
  // No summary available: full cold start per base spec Section 6.4
  // Models initialized with default weights, THRESHOLD_MAX threshold,
  // 0.3 accuracy, TRANSITIONING mode. Expected convergence: 10-15 epochs.

  arriving = get_agent(arriving_agent_id)
  for existing_agent in dest_parcel.agents:
    if existing_agent.id == arriving_agent_id: continue

    model = PredictiveModel{
      neighbor = existing_agent.id,
      weights = default_weights(),
      accuracy = 0.3,
      threshold = THRESHOLD_MAX,
      error_history = [],
      mode = TRANSITIONING,
      warm_start_source = null,
      consecutive_accurate = 0
    }
    arriving.predictive_models[existing_agent.id] = model

  for existing_agent in dest_parcel.agents:
    if existing_agent.id == arriving_agent_id: continue
    model = PredictiveModel{
      neighbor = arriving_agent_id,
      weights = default_weights(),
      accuracy = 0.3,
      threshold = THRESHOLD_MAX,
      error_history = [],
      mode = TRANSITIONING,
      warm_start_source = null,
      consecutive_accurate = 0
    }
    existing_agent.predictive_models[arriving_agent_id] = model

  send_cold_start_burst(arriving_agent_id, dest_parcel,
                        dest_parcel.signal_aggregator)
```

### HP-4.4 Summary Integrity and Privacy

```
Model Migration Security Properties:
======================================

1. INTEGRITY: Summary is signed by the departing agent.
   Receiving agents verify the signature before using the summary.
   A corrupted or forged summary is detected and discarded;
   the model falls back to cold start.

2. FRESHNESS: Summary epoch range is validated against current epoch.
   Stale summaries (older than MIGRATION_LOOKBACK epochs) are rejected.
   This prevents replay attacks where an adversary submits an old
   summary to mislead new neighbors about current behavior.

3. PRIVACY: The self_model_weights field is OPTIONAL. Agents may
   decline to share their internal model weights. In that case,
   warm start uses only the behavioral statistics (which are derived
   from publicly observable actions -- task completions, surprise
   signals emitted, etc.) and provides a weaker but still useful prior.

4. BOUNDED SIZE: The 1KB limit on CompressedModelSummary ensures that
   model migration does not consume significant bandwidth during
   reconfiguration -- the time when bandwidth is most constrained.
   With N=50 agents departing a parcel, total migration data is 50KB.

5. ABUSE RESISTANCE: An adversary cannot use a fabricated summary to
   mislead new neighbors because:
   (a) The signature binds the summary to the agent's identity.
   (b) Behavioral statistics are verifiable against the settlement
       record (which is deterministically computed from shared inputs).
   (c) If the summary's claimed task_completion_rate differs
       significantly from the settlement-derived rate, the summary
       is flagged as suspicious and discarded.
```

---

## HP-5: Governance Quorum Protection

### HP-5.1 Quorum Freeze Protocol

When a parcel reconfiguration occurs during an active G-class vote, the set of eligible voters changes. Without protection, this can cause three problems:

1. **Quorum inflation:** Agents join the parcel mid-vote, increasing the denominator. A vote that had sufficient support may suddenly fall below threshold.
2. **Quorum deflation:** Agents leave the parcel mid-vote, decreasing the denominator. A vote that lacked support may suddenly cross threshold, approving a change without genuine consensus.
3. **Voter eligibility ambiguity:** An agent that was eligible when the vote started but departed before voting -- should their absence count against quorum?

The quorum freeze protocol solves all three by freezing the quorum denominator at the pre-reconfiguration value for in-progress votes.

```
FrozenQuorum := {
  vote_id:              VoteId
  frozen_at_epoch:      uint64
  frozen_eligible_set:  Set<AgentId>     // voters eligible when frozen
  frozen_denominator:   uint32           // |frozen_eligible_set|
  frozen_threshold:     float64          // 0.75 for standard, 0.90 for ETR
  votes_received:       Map<AgentId, Vote>
  deadline_epoch:       uint64           // original deadline
  extended:             bool             // true if deadline was extended
  extended_deadline:    uint64 | null    // extended deadline if applicable
}
```

### HP-5.2 Freeze Logic

```
function freeze_quorum_on_reconfig(
  parcel: Parcel,
  reconfig: ParcelReconfigState,
  active_votes: List<GovernanceVote>
) -> Map<VoteId, FrozenQuorum>:

  frozen_quorums = {}

  for vote in active_votes:
    if vote.status != IN_PROGRESS:
      continue

    // Determine the eligible voter set from BEFORE reconfiguration
    pre_reconfig_eligible = {
      agent for agent in reconfig.old_roster
      if agent.governance == true
      and agent.id in vote.eligible_voters
    }

    frozen = FrozenQuorum{
      vote_id = vote.id,
      frozen_at_epoch = current_epoch(),
      frozen_eligible_set = pre_reconfig_eligible,
      frozen_denominator = |pre_reconfig_eligible|,
      frozen_threshold = vote.required_threshold,
      votes_received = vote.votes_received,
      deadline_epoch = vote.deadline_epoch,
      extended = false,
      extended_deadline = null
    }

    // Check if reconfiguration reduced eligible voters below quorum
    post_reconfig_eligible = {
      agent for agent in reconfig.new_roster
      if agent.governance == true
      and agent.id in vote.eligible_voters
    }

    remaining_fraction = |post_reconfig_eligible| / frozen.frozen_denominator

    if remaining_fraction < frozen.frozen_threshold:
      // The remaining voters cannot possibly reach quorum
      // even if all of them vote yes. Extend the deadline.
      frozen.extended = true
      frozen.extended_deadline = vote.deadline_epoch + QUORUM_EXTENSION_EPOCHS
      log_quorum_extension(vote, remaining_fraction,
                           frozen.frozen_denominator,
                           QUORUM_EXTENSION_EPOCHS)

      // Emit governance-channel alert
      emit_governance_alert(
        type = QUORUM_AT_RISK,
        vote_id = vote.id,
        remaining_eligible = |post_reconfig_eligible|,
        required_for_quorum = ceil(
          frozen.frozen_threshold * frozen.frozen_denominator),
        extension_epochs = QUORUM_EXTENSION_EPOCHS
      )

    frozen_quorums[vote.id] = frozen

  return frozen_quorums


// New configurable constant
// #58: QUORUM_EXTENSION_EPOCHS   default: 2    range: [1, 5]
//      Number of tidal epochs to extend vote deadline when
//      reconfiguration reduces eligible voters below quorum threshold
```

### HP-5.3 Vote Counting with Frozen Quorum

```
function count_vote(
  vote: GovernanceVote,
  voter: AgentId,
  ballot: Vote,
  frozen: FrozenQuorum | null
) -> VoteResult:

  // Determine which quorum to use
  if frozen is not null:
    // Use frozen quorum: only agents in the frozen eligible set can vote
    if voter not in frozen.frozen_eligible_set:
      return REJECTED(
        reason="VOTER_NOT_IN_FROZEN_ELIGIBLE_SET",
        detail="Agent {voter} joined after quorum freeze at epoch "
               + str(frozen.frozen_at_epoch)
      )

    // Record the vote
    frozen.votes_received[voter] = ballot

    // Check approval against frozen denominator
    yes_votes = count(v for v in frozen.votes_received.values()
                      if v == YES)
    approval_fraction = yes_votes / frozen.frozen_denominator

    // Determine effective deadline
    deadline = frozen.extended_deadline if frozen.extended else frozen.deadline_epoch

    if approval_fraction >= frozen.frozen_threshold:
      return APPROVED(
        approval_fraction = approval_fraction,
        denominator = frozen.frozen_denominator,
        note = "Counted against frozen quorum from epoch "
               + str(frozen.frozen_at_epoch)
      )
    elif current_epoch() > deadline:
      return EXPIRED(
        approval_fraction = approval_fraction,
        denominator = frozen.frozen_denominator,
        extended = frozen.extended
      )
    else:
      return PENDING(
        approval_fraction = approval_fraction,
        remaining_epochs = deadline - current_epoch()
      )

  else:
    // No frozen quorum: standard vote counting per base spec
    return standard_vote_count(vote, voter, ballot)


function evaluate_new_vote_quorum(
  proposal: GovernanceProposal,
  locus: Locus,
  epoch: uint64
) -> QuorumConfig:
  // NEW votes (submitted after reconfiguration) use the CURRENT
  // eligible voter set, not the frozen set.
  current_eligible = {
    agent for agent in all_agents(locus)
    if agent.governance == true
  }

  return QuorumConfig{
    eligible_set = current_eligible,
    denominator = |current_eligible|,
    threshold = proposal.required_threshold,
    deadline = epoch + proposal.vote_duration_epochs,
    frozen = false
  }
```

### HP-5.4 Unfreezing

```
function unfreeze_quorums(
  parcel: Parcel,
  frozen_quorums: Map<VoteId, FrozenQuorum>
):
  // Called at Phase D entry (normal operation resumes)
  // All frozen quorums are unfrozen -- future votes use current roster

  for (vote_id, frozen) in frozen_quorums:
    vote = get_governance_vote(vote_id)

    if vote.status == IN_PROGRESS:
      // Vote is still active: check if it was approved or expired
      // under the frozen quorum
      yes_votes = count(v for v in frozen.votes_received.values()
                        if v == YES)
      approval = yes_votes / frozen.frozen_denominator

      deadline = frozen.extended_deadline if frozen.extended \
                 else frozen.deadline_epoch

      if approval >= frozen.frozen_threshold:
        vote.status = APPROVED
        vote.approval_note = "Approved under frozen quorum (epoch "
                             + str(frozen.frozen_at_epoch) + ")"
      elif current_epoch() > deadline:
        vote.status = EXPIRED
        vote.expiry_note = "Expired under frozen quorum"
      else:
        // Vote still pending: transition to current quorum
        // Votes already cast remain valid. New denominator is
        // the current eligible set.
        vote.eligible_voters = {
          agent for agent in all_agents(parcel.locus)
          if agent.governance == true
        }
        vote.denominator = |vote.eligible_voters|
        log_quorum_transition(vote_id, frozen.frozen_denominator,
                              vote.denominator)

    // Clear frozen state
    frozen_quorums.remove(vote_id)
```

### HP-5.5 ETR Quorum Protection

ETR votes receive special treatment because they are the most critical governance mechanism -- the system's emergency brake. ETR quorum protection is stricter:

```
function protect_etr_quorum(
  etr_vote: ETRVote,
  reconfig: ParcelReconfigState
) -> FrozenQuorum:

  // ETR votes are ALWAYS frozen at pre-reconfiguration state
  // No exceptions, no unfreezing until the ETR resolves

  frozen = freeze_quorum_on_reconfig(
    parcel = null,  // ETR is locus-scoped, not parcel-scoped
    reconfig = reconfig,
    active_votes = [etr_vote]
  )[etr_vote.id]

  // ETR extension is more aggressive: 3 epochs instead of 2
  if frozen.extended:
    frozen.extended_deadline = etr_vote.deadline_epoch + 3

  // ETR votes from agents who departed are counted if cast before departure
  // (unlike standard governance where departed agent votes expire)
  for (voter, ballot) in frozen.votes_received:
    if voter not in reconfig.new_roster:
      // Agent departed but already voted: vote STANDS
      log_departed_etr_voter(voter, ballot, "VOTE_PRESERVED")

  return frozen
```

---

## HP-6: Cross-Integration Failure Ordering

### HP-6.1 Degradation Priority

When the system must choose which subsystem to degrade first during resource contention or partial recovery, the following priority ordering governs. Priority 1 is degraded last (most protected); Priority 4 is degraded first (least critical, fastest recovery).

```
DegradationPriority := enum {
  PRIORITY_1_GOVERNANCE    = 1,   // Degrade LAST
  PRIORITY_2_VERIFICATION  = 2,   // Degrade second-to-last
  PRIORITY_3_SCHEDULING    = 3,   // Degrade third
  PRIORITY_4_COMMUNICATION = 4    // Degrade FIRST
}

// Rationale for this ordering:
//
// 1. GOVERNANCE (degrade last): Governance is the system's immune system.
//    If governance degrades, the system loses its ability to respond to
//    crises -- including the very reconfiguration storm that caused the
//    degradation. The ETR mechanism is the last line of defense; it must
//    remain operational when everything else fails. The dedicated
//    governance channel (independent of data plane) supports this.
//
// 2. VERIFICATION (degrade second-to-last): The verification membrane
//    is constitutionally protected (INV-1). Epistemic corruption
//    compounds through the knowledge graph and is harder to detect and
//    reverse than performance degradation. However, verification can
//    operate with reduced committee sizes or relaxed diversity
//    requirements without catastrophic failure -- it degrades gracefully
//    along a quality gradient rather than failing hard.
//
// 3. SCHEDULING (degrade third): Scheduling degradation means suboptimal
//    task assignment -- work still gets done, possibly by a less-ideal
//    agent. Stale hash rings produce valid (if suboptimal) assignments.
//    The substitution list provides automatic fallback. Recovery is
//    deterministic and complete within one epoch of roster stabilization.
//
// 4. COMMUNICATION (degrade first): Communication degradation means
//    falling back from predictive delta (zero messages in steady state)
//    to standard messaging (O(N) messages per epoch). This is the least
//    damaging because:
//    (a) Standard messaging is always correct, just less efficient.
//    (b) Recovery is the fastest: models reconverge in 3-5 epochs
//        with warm start, 10-15 without.
//    (c) The system was designed for zero-communication steady state
//        as an optimization, not a correctness requirement.
```

### HP-6.2 Degradation Ordering Logic

```
function compute_degradation_plan(
  locus: Locus,
  available_resources: ResourceBudget,
  storm_state: StormState
) -> DegradationPlan:

  plan = DegradationPlan{
    communication = FULL,
    scheduling = FULL,
    verification = FULL,
    governance = FULL
  }

  // Compute resource requirements for each subsystem at full operation
  comm_cost = estimate_communication_cost(locus, FULL)
  sched_cost = estimate_scheduling_cost(locus, FULL)
  verif_cost = estimate_verification_cost(locus, FULL)
  gov_cost = estimate_governance_cost(locus, FULL)

  total_required = comm_cost + sched_cost + verif_cost + gov_cost

  if total_required <= available_resources.total:
    return plan   // No degradation needed

  // Degrade in priority order (4 -> 3 -> 2 -> 1)
  deficit = total_required - available_resources.total

  // Step 1: Degrade COMMUNICATION first
  comm_savings = degrade_communication(locus, plan)
  deficit -= comm_savings
  if deficit <= 0:
    return plan

  // Step 2: Degrade SCHEDULING second
  sched_savings = degrade_scheduling(locus, plan)
  deficit -= sched_savings
  if deficit <= 0:
    return plan

  // Step 3: Degrade VERIFICATION third
  verif_savings = degrade_verification(locus, plan)
  deficit -= verif_savings
  if deficit <= 0:
    return plan

  // Step 4: Degrade GOVERNANCE last (should almost never happen)
  gov_savings = degrade_governance(locus, plan)
  deficit -= gov_savings

  if deficit > 0:
    // CRITICAL: system cannot meet minimum resource requirements
    // Emit emergency signal and trigger ETR
    emit_governance_alert(
      type = CRITICAL_RESOURCE_EXHAUSTION,
      deficit = deficit,
      plan = plan
    )

  return plan


function degrade_communication(
  locus: Locus,
  plan: DegradationPlan
) -> float64:
  // Level 1: Disable predictive delta, fall back to standard messaging
  plan.communication = STANDARD_ONLY
  savings = estimate_communication_cost(locus, FULL)
             - estimate_communication_cost(locus, STANDARD_ONLY)

  // Level 2: If still insufficient, reduce signal budget by 50%
  if savings < needed_savings():
    plan.communication = REDUCED_STANDARD
    savings += estimate_communication_cost(locus, STANDARD_ONLY)
               - estimate_communication_cost(locus, REDUCED_STANDARD)

  return savings


function degrade_scheduling(
  locus: Locus,
  plan: DegradationPlan
) -> float64:
  // Level 1: Freeze hash ring reconstruction (use stale rings)
  // Tasks still get assigned, just suboptimally
  plan.scheduling = STALE_RINGS
  savings = estimate_ring_rebuild_cost(locus)

  // Level 2: Reduce virtual node count by 50%
  // Increases load imbalance but reduces ring memory and rebuild cost
  if savings < needed_savings():
    plan.scheduling = REDUCED_VNODES
    savings += estimate_vnode_reduction_savings(locus)

  return savings


function degrade_verification(
  locus: Locus,
  plan: DegradationPlan
) -> float64:
  // Level 1: Reduce committee size to MIN_COMMITTEE_SIZE (3)
  // Verification still occurs but with less diversity
  plan.verification = REDUCED_COMMITTEE
  savings = estimate_committee_reduction_savings(locus)

  // Level 2: Defer non-critical re-verifications
  // New claims still verified; continuous re-verification paused
  if savings < needed_savings():
    plan.verification = DEFER_REVERIFICATION
    savings += estimate_reverification_savings(locus)

  // NEVER: Skip verification entirely. The membrane is sovereign.
  // Constitutional protection (INV-1) prohibits this.

  return savings


function degrade_governance(
  locus: Locus,
  plan: DegradationPlan
) -> float64:
  // Level 1: Extend voting windows (slower governance, not less governance)
  plan.governance = EXTENDED_WINDOWS
  savings = estimate_governance_window_savings(locus)

  // Level 2: Suspend non-ETR governance proposals
  // ETR MUST remain operational at all times
  if savings < needed_savings():
    plan.governance = ETR_ONLY
    savings += estimate_non_etr_savings(locus)

  // NEVER: Disable ETR. This is the system's last line of defense.

  return savings
```

### HP-6.3 Recovery Ordering

Recovery follows the REVERSE of degradation -- subsystems are restored from Priority 1 (governance) to Priority 4 (communication). This ensures that the most critical subsystems recover first.

```
function compute_recovery_plan(
  locus: Locus,
  current_plan: DegradationPlan,
  available_resources: ResourceBudget
) -> DegradationPlan:

  // Attempt recovery in priority order (1 -> 2 -> 3 -> 4)
  // Priority 1: Restore governance first
  if current_plan.governance != FULL:
    gov_cost = estimate_governance_cost(locus, FULL)
               - estimate_governance_cost(locus, current_plan.governance)
    if available_resources.surplus >= gov_cost:
      current_plan.governance = FULL
      available_resources.surplus -= gov_cost

  // Priority 2: Restore verification
  if current_plan.verification != FULL:
    verif_cost = estimate_verification_cost(locus, FULL)
                 - estimate_verification_cost(locus, current_plan.verification)
    if available_resources.surplus >= verif_cost:
      current_plan.verification = FULL
      available_resources.surplus -= verif_cost

  // Priority 3: Restore scheduling
  if current_plan.scheduling != FULL:
    sched_cost = estimate_scheduling_cost(locus, FULL)
                 - estimate_scheduling_cost(locus, current_plan.scheduling)
    if available_resources.surplus >= sched_cost:
      current_plan.scheduling = FULL
      available_resources.surplus -= sched_cost

  // Priority 4: Restore communication last
  if current_plan.communication != FULL:
    comm_cost = estimate_communication_cost(locus, FULL)
                - estimate_communication_cost(locus, current_plan.communication)
    if available_resources.surplus >= comm_cost:
      current_plan.communication = FULL
      available_resources.surplus -= comm_cost

  return current_plan
```

### HP-6.4 Degradation State Monitoring

```
DegradationReport := {
  locus:              LocusId
  epoch:              uint64
  storm_active:       bool
  communication:      {FULL, STANDARD_ONLY, REDUCED_STANDARD}
  scheduling:         {FULL, STALE_RINGS, REDUCED_VNODES}
  verification:       {FULL, REDUCED_COMMITTEE, DEFER_REVERIFICATION}
  governance:         {FULL, EXTENDED_WINDOWS, ETR_ONLY}
  degradation_depth:  uint32    // count of subsystems below FULL
  time_in_degraded:   uint32    // epochs since first degradation
}

function emit_degradation_report(
  locus: Locus,
  plan: DegradationPlan,
  storm_state: StormState,
  epoch: uint64
):
  depth = count(s for s in [plan.communication, plan.scheduling,
                            plan.verification, plan.governance]
                if s != FULL)

  report = DegradationReport{
    locus = locus.id,
    epoch = epoch,
    storm_active = storm_state.storm_active,
    communication = plan.communication,
    scheduling = plan.scheduling,
    verification = plan.verification,
    governance = plan.governance,
    degradation_depth = depth,
    time_in_degraded = epoch - storm_state.storm_start_epoch
                       if storm_state.storm_active else 0
  }

  // Emit as stigmergic signal for locus-scope visibility
  emit_stigmergic_signal(
    type = RISK,
    scope = locus,
    confidence = depth / 4.0,
    decay_tau = 3600,
    payload = report
  )

  // Alert thresholds
  if depth >= 3:
    log_critical("DEGRADATION_DEPTH_3+", report)
    emit_governance_alert(type = SEVERE_DEGRADATION, report = report)
  elif depth >= 2:
    log_warning("DEGRADATION_DEPTH_2", report)
```

---

## HP-7: Conformance Amendments

### HP-7.1 New MUST Requirements

Add the following MUST requirements to Section 12.3:

> **MUST (#16):** Implement the storm detection mechanism (HP-1) with configurable thresholds STORM_PARCEL_FRACTION and STORM_AGENT_FRACTION. When a storm condition is detected, new reconfigurations MUST be throttled to STORM_THROTTLE_MAX per epoch per locus and excess reconfigurations MUST be queued (not rejected) for execution in subsequent epochs.

> **MUST (#17):** Implement the staggered reconfiguration protocol (HP-2) with four sequential phases (A: rings, B: VRF, C: predictive, D: normal). The phase ordering MUST NOT be reordered. Each phase MUST complete before the next begins.

> **MUST (#18):** Implement the VRF committee cache invalidation protocol (HP-3). In-progress verifications MUST complete using their original committee. New verifications after a boundary change MUST use freshly computed committees from the new roster.

> **MUST (#19):** Implement governance quorum freeze (HP-5). Any in-progress G-class vote at the time of reconfiguration MUST freeze its quorum denominator at the pre-reconfiguration value. ETR votes MUST be frozen with stricter protection per HP-5.5.

> **MUST (#20):** Implement the degradation priority ordering (HP-6): communication degrades first, governance degrades last. The ETR mechanism MUST remain operational under all degradation states.

### HP-7.2 New SHOULD Requirements

> **SHOULD (#9):** Implement predictive model migration (HP-4) with compressed model summaries. Agents crossing parcel boundaries SHOULD carry a CompressedModelSummary (max 1KB) for warm-start initialization of neighbor models.

> **SHOULD (#10):** Implement the graduated circuit breaker (HP-1.4) with HALT, DRAIN_ONLY, THROTTLED, and NORMAL states. The base spec's binary circuit breaker (30% halt) remains the minimum requirement.

### HP-7.3 New Configurable Constants Summary

| # | Constant | Default | Range | Section |
|---|----------|---------|-------|---------|
| 50 | STORM_PARCEL_FRACTION | 0.15 | [0.05, 0.30] | HP-1.1 |
| 51 | STORM_AGENT_FRACTION | 0.25 | [0.10, 0.50] | HP-1.1 |
| 52 | STORM_THROTTLE_MAX | 3 | [1, 10] | HP-1.1 |
| 53 | STORM_COOLDOWN_EPOCHS | 5 | [2, 20] | HP-1.1 |
| 54 | STORM_QUEUE_MAX | 50 | [10, 200] | HP-1.1 |
| 55 | TICKS_PER_EPOCH | 60 | [20, 120] | HP-2.1 |
| 56 | STALE_VRF_MAX_TICKS | 30 | [10, 60] | HP-3.3 |
| 57 | MIGRATION_LOOKBACK | 10 | [3, 30] | HP-4.1 |
| 58 | QUORUM_EXTENSION_EPOCHS | 2 | [1, 5] | HP-5.2 |

### HP-7.4 Deployment Profile Additions (per PA-F6)

| # | Parameter | T1 (Dev/Test) | T2 (Prod Small) | T3 (Prod Large) |
|---|-----------|---------------|-----------------|-----------------|
| 50 | STORM_PARCEL_FRACTION | 0.30 | 0.20 | 0.15 |
| 51 | STORM_AGENT_FRACTION | 0.50 | 0.35 | 0.25 |
| 52 | STORM_THROTTLE_MAX | 10 | 5 | 3 |
| 53 | STORM_COOLDOWN_EPOCHS | 2 | 3 | 5 |
| 55 | TICKS_PER_EPOCH | 20 | 40 | 60 |
| 56 | STALE_VRF_MAX_TICKS | 15 | 20 | 30 |
| 57 | MIGRATION_LOOKBACK | 3 | 5 | 10 |
| 58 | QUORUM_EXTENSION_EPOCHS | 1 | 2 | 2 |

---

## HP-8: Validation Requirements

### HP-8.1 GATE-1 Amendment

The GATE-1 reconfiguration storm simulation (Section 12.1) is amended to validate the staggered protocol:

**Amended GATE-1 Setup:**
- 100+ parcels in a single locus
- 30% simultaneous agent churn (triggered at a single epoch boundary)
- Storm detector and throttle active
- Staggered reconfiguration protocol active
- Measure:
  - Time from churn event to all parcels returning to ACTIVE state
  - Maximum simultaneous degradation depth (how many subsystems degraded at once)
  - Communication overhead during Phase C (must not exceed 5x steady state)
  - VRF cache stale entry count and resolution time
  - Governance quorum freeze count and resolution
  - Queue depth during storm throttling

**Amended GATE-1 Success Criteria:**
- Combined recovery time < 10 epochs at 100+ parcels (unchanged)
- Maximum simultaneous degradation depth <= 2 subsystems during staggered protocol
- No governance votes invalidated by reconfiguration (quorum freeze holds)
- No verification membrane violations (in-progress verifications complete with original committee)
- Storm queue drains within 5 epochs of storm condition clearing

**Amended GATE-1 Kill Criterion:**
- Recovery time > 10 epochs (unchanged)
- OR simultaneous degradation depth > 3 subsystems during staggered protocol
- OR governance vote invalidated during reconfiguration
- OR verification membrane integrity violation during VRF cache invalidation

### HP-8.2 New Recommended Experiments

**Experiment 8: Storm Throttle Calibration**
- Sweep STORM_PARCEL_FRACTION from 0.05 to 0.30 and STORM_THROTTLE_MAX from 1 to 10.
- At each parameter combination, inject 30% agent churn and measure: recovery time, queue depth, communication overhead.
- Success criterion: identify parameter region where recovery time < 10 epochs AND queue depth < STORM_QUEUE_MAX AND communication overhead < 5x steady state.

**Experiment 9: Warm-Start vs Cold-Start Convergence**
- Compare predictive model convergence with and without CompressedModelSummary.
- Setup: 50-agent parcel, 10 agents depart, 10 new agents arrive.
- Measure: epochs to 70% model accuracy for new agent pairs.
- Success criterion: warm start achieves 70% accuracy in <= 5 epochs; cold start baseline takes 10-15 epochs.

**Experiment 10: Quorum Freeze Under Cascading Reconfigurations**
- Initiate a G-class governance vote. During the vote, trigger 3 successive reconfigurations affecting overlapping agent sets.
- Measure: quorum denominator stability, vote outcome consistency, extension count.
- Success criterion: vote outcome is identical to what it would have been without reconfiguration. No quorum manipulation possible.

---

## Summary of Changes

This hardening addendum adds six concrete mechanisms to address the reconfiguration storm:

1. **Storm Detection and Throttling (HP-1):** Detects when reconfiguration volume exceeds recovery capacity. Throttles new reconfigurations to a bounded rate and queues excess for later execution. Graduated circuit breaker provides four response levels.

2. **Staggered Reconfiguration Protocol (HP-2):** Replaces the monolithic MIGRATE phase with four sequential phases, each addressing one subsystem. At most two subsystems are degraded simultaneously. Sub-epoch tick mechanism provides timing granularity without consensus.

3. **VRF Committee Cache Invalidation (HP-3):** In-progress verifications complete with their original committee. New verifications use freshly computed committees. Stale entries have a bounded lifetime with forced resolution.

4. **Predictive Model Migration (HP-4):** Agents carry compressed behavioral summaries (max 1KB) when crossing parcel boundaries. New neighbors use these for warm-start model initialization, reducing convergence from 10-15 epochs to 3-5.

5. **Governance Quorum Protection (HP-5):** In-progress votes freeze their quorum denominator at the pre-reconfiguration value. If reconfiguration reduces eligible voters below the frozen quorum's threshold, the vote deadline extends. ETR votes receive stricter protection.

6. **Cross-Integration Failure Ordering (HP-6):** Communication degrades first (fastest recovery, least critical). Governance degrades last (system's immune system). Recovery follows the reverse order. ETR is never disabled.

**Net effect on GATE-1:** The staggered protocol ensures that the 10-epoch recovery bound is achievable because subsystems recover sequentially rather than competing for resources simultaneously. The storm detector prevents the system from entering a state where recovery time exceeds mean time between churn events -- the conditional fatal flaw identified by the Adversarial Report.

**Relationship to other deferred CRITICAL items:** This addendum addresses only the reconfiguration storm (Attack 1). The following CRITICAL items remain deferred to subsequent hardening passes:
- VRF grinding amplification at scale
- Emergency rollback race conditions
- Cross-integration cascade propagation across locus boundaries
