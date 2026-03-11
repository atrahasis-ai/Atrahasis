# C3 Hardening Addendum: Emergency Tidal Rollback Resilience
## Addressing ETR Fragility Under Catastrophic Scheduling Failure

**Addendum to:** Tidal Noosphere Master Technical Specification (C3-A v1.0)
**Section affected:** 7.3 Emergency Tidal Rollback (ETR)
**Date:** 2026-03-10
**Status:** DESIGN — Hardening Amendment
**Classification:** CONSTITUTIONAL (modifies governance-protected mechanism)

---

## Problem Statement

The existing ETR mechanism (Section 7.3) requires a 90% supermajority of active governance agents, voted over a dedicated governance channel, within an ETR_VOTE_WINDOW of 2 epochs. The threshold reduction fallback (90% -> 80% after 3 failures, Sentinel override after 6 failures) partially mitigates blocking coalitions but does not address four structural fragilities:

1. **Governance channel disruption.** The dedicated governance channel is architecturally independent of the tidal data plane, but it is still a single communication substrate. If the governance gossip mesh itself suffers partition or connectivity loss (network-level failure, not scheduling-level), ETR votes cannot propagate.

2. **Agent unreachability under crisis.** The 90% threshold is computed against "active governance agents." But a crisis severe enough to trigger ETR may also render agents unresponsive — not because they oppose rollback, but because the broken tidal function has disrupted their ability to participate. Absent agents count as implicit vetoes against the supermajority.

3. **Temporal inadequacy.** The ETR_VOTE_WINDOW of 2 epochs assumes the governance channel is functional and agents can deliberate. Under cascading failure (e.g., tidal function induces parcel oscillation which exhausts agent compute budgets), even 2 epochs may be too slow, and the 3-attempt-then-reduce-threshold cycle adds further delay.

4. **Circular dependency residue.** While the governance channel is independent of the tidal scheduler, the agents themselves still depend on the tidal scheduler for their primary task execution. If the scheduler is broken, agents may be in degraded states that impair their governance participation — reduced compute budget, stale roster information, inability to verify the ETR proposal's validity.

**Consequence:** In the worst case, a catastrophically bad tidal function version could render the system unable to invoke the very mechanism designed to recover from bad tidal function versions.

---

## 1. Two-Tier ETR: Standard and Critical

### 1.1 Tier Definitions

The ETR mechanism is split into two tiers with distinct activation conditions, quorum requirements, and procedural safeguards.

**Standard ETR** (existing mechanism, unchanged):
- Trigger: Any of the three existing automated triggers (scheduling skew, verification starvation, settlement divergence).
- Proposal: 3 governance-seat holders.
- Vote channel: Primary governance mesh.
- Vote window: ETR_VOTE_WINDOW (2 epochs).
- Quorum: ETR_SUPERMAJORITY (90%) of all active governance agents.
- Threshold reduction: 90% -> 80% after 3 failures; Sentinel override after 6 failures.
- Use case: Non-urgent version regressions, performance degradation, gradual quality drift.

**Critical ETR** (new):
- Trigger: Automatic trigger conditions (Section 1.2) OR manual trigger by 3 governance-seat holders from different loci.
- Proposal: Automatic (system-generated on trigger detection) or manual (3 holders from distinct loci).
- Vote channel: Any available channel (primary, secondary, or tertiary — see Section 2).
- Vote window: CRITICAL_ETR_VOTE_WINDOW (1 epoch).
- Quorum: CRITICAL_ETR_QUORUM (67%) of **reachable** governance agents, not all active agents.
- Threshold reduction: None. If 67% of reachable agents is not achieved within 1 epoch, the system proceeds to automatic degradation (Section 4).
- Use case: Genuine emergencies where the tidal function itself is the source of system-wide disruption.
- Rollback target: MUST be a version from the Known-Good Registry (Section 3). Cannot target an arbitrary version.

### 1.2 Critical ETR Trigger Conditions

Critical ETR activates automatically when ANY of the following conditions is detected. Detection is performed independently by each agent's local Sentinel; consensus on trigger detection is NOT required (any agent detecting a trigger can broadcast a Critical ETR proposal).

```
function evaluate_critical_etr_triggers(agent, local_state) -> Option<CriticalETRProposal>:
    // Trigger C1: Sustained scheduling failure
    // Scheduling failure = epoch completes with <50% of assigned tasks successfully dispatched
    if local_state.scheduling_failure_rate > 0.50
       for last 3 consecutive epochs:
        return CriticalETRProposal(
            trigger = "C1_SCHEDULING_FAILURE",
            evidence = local_state.last_3_epoch_scheduling_logs,
            proposed_target = known_good_registry.most_recent()
        )

    // Trigger C2: Verification committee formation collapse
    // Formation failure = VRF committee selection produces fewer than MIN_COMMITTEE_SIZE verifiers
    if local_state.verification_formation_failure_rate > 0.30
       for last 2 consecutive epochs:
        return CriticalETRProposal(
            trigger = "C2_VERIFICATION_COLLAPSE",
            evidence = local_state.last_2_epoch_vrf_logs,
            proposed_target = known_good_registry.most_recent()
        )

    // Trigger C3: Settlement computation divergence (determinism invariant violated)
    // This is the most severe trigger: it means INV-2 is broken
    if local_state.settlement_divergence_detected:
        return CriticalETRProposal(
            trigger = "C3_DETERMINISM_VIOLATION",
            evidence = local_state.divergence_proof,  // two agents, same inputs, different outputs
            proposed_target = known_good_registry.most_recent()
        )

    // Trigger C4: Manual trigger (3 governance-seat holders from different loci)
    // This is checked via incoming proposals, not local state
    // See manual_critical_etr_check() below

    return None
```

```
function manual_critical_etr_check(proposals: List<ManualCriticalETRRequest>) -> Option<CriticalETRProposal>:
    // Group by proposed target version
    for target_version, group in group_by(proposals, p -> p.target_version):
        unique_loci = distinct(p.proposer_locus for p in group)
        if len(unique_loci) >= 3 and target_version in known_good_registry:
            return CriticalETRProposal(
                trigger = "C4_MANUAL",
                evidence = group,
                proposed_target = target_version
            )
    return None
```

**Trigger severity ordering:** C3 (determinism violation) > C1 (scheduling failure) > C2 (verification collapse) > C4 (manual). Higher severity triggers override lower severity proposals if they occur simultaneously.

### 1.3 Critical ETR Voting Protocol

```
function critical_etr_vote(agent, proposal: CriticalETRProposal) -> CriticalETRVote:
    // Validate the proposal
    assert proposal.proposed_target in known_good_registry
    assert proposal.trigger in {"C1_SCHEDULING_FAILURE", "C2_VERIFICATION_COLLAPSE",
                                 "C3_DETERMINISM_VIOLATION", "C4_MANUAL"}

    // Verify evidence locally (each agent checks independently)
    evidence_valid = verify_trigger_evidence(proposal.trigger, proposal.evidence)

    // Local corroboration: does this agent's own observation confirm the crisis?
    local_corroboration = agent.sentinel.confirms_crisis(proposal.trigger)

    // Vote YES if either evidence is valid OR local observation confirms crisis
    // This prevents a healthy partition from blocking rollback because they
    // cannot verify evidence from a disrupted partition
    vote = APPROVE if (evidence_valid or local_corroboration) else REJECT

    return CriticalETRVote(
        voter = agent.id,
        proposal_hash = hash(proposal),
        vote = vote,
        timestamp = current_epoch(),
        channel_used = agent.best_available_channel()  // primary, secondary, or tertiary
    )
```

```
function tally_critical_etr(votes: List<CriticalETRVote>, proposal_hash) -> ETRDecision:
    relevant_votes = [v for v in votes if v.proposal_hash == proposal_hash]

    // Deduplicate: one vote per agent (latest timestamp wins)
    latest_votes = deduplicate_by_agent(relevant_votes)

    // "Reachable" = agents that have sent ANY message (vote, heartbeat, or data)
    // on ANY channel within the last 2 epochs
    reachable_agents = governance_roster.agents_active_within(epochs=2)

    approve_count = count(v for v in latest_votes if v.vote == APPROVE)
    quorum_target = ceil(len(reachable_agents) * CRITICAL_ETR_QUORUM)

    if approve_count >= quorum_target:
        return ETRDecision(
            outcome = APPROVED,
            target_version = proposal.proposed_target,
            activation_epoch = current_epoch() + 1,
            tier = CRITICAL
        )
    else:
        return ETRDecision(
            outcome = REJECTED,
            proceed_to_safe_mode = True  // Critical ETR has no retry; failure -> SAFE_MODE
        )
```

### 1.4 Tier Selection Logic

```
function select_etr_tier(trigger_source) -> ETRTier:
    // Critical triggers bypass Standard ETR entirely
    if trigger_source in {"C1_SCHEDULING_FAILURE", "C2_VERIFICATION_COLLAPSE",
                           "C3_DETERMINISM_VIOLATION", "C4_MANUAL"}:
        return CRITICAL

    // Standard triggers (scheduling skew, verification starvation, settlement divergence)
    // go through Standard ETR first
    return STANDARD

function etr_escalation(standard_etr_result) -> ETRTier:
    // If Standard ETR fails after Sentinel override threshold (6 attempts),
    // escalate to Critical ETR
    if standard_etr_result.attempt_count >= 6 and standard_etr_result.outcome == REJECTED:
        return CRITICAL
    return STANDARD
```

### 1.5 New Constants

| # | Name | Default | Range | Description |
|---|------|---------|-------|-------------|
| 32 | CRITICAL_ETR_QUORUM | 0.67 | [0.51, 0.80] | Fraction of reachable governance agents for Critical ETR. |
| 33 | CRITICAL_ETR_VOTE_WINDOW | 1 | [1, 3] | Epochs for Critical ETR vote collection. |
| 34 | SCHEDULING_FAILURE_THRESHOLD | 0.50 | [0.30, 0.70] | Scheduling failure rate triggering C1. |
| 35 | SCHEDULING_FAILURE_EPOCHS | 3 | [2, 5] | Consecutive failed epochs for C1. |
| 36 | VERIFICATION_COLLAPSE_THRESHOLD | 0.30 | [0.20, 0.50] | Formation failure rate triggering C2. |
| 37 | VERIFICATION_COLLAPSE_EPOCHS | 2 | [1, 4] | Consecutive failed epochs for C2. |
| 38 | MANUAL_CRITICAL_MIN_LOCI | 3 | [2, 5] | Minimum distinct loci for manual Critical ETR. |
| 39 | REACHABLE_LOOKBACK_EPOCHS | 2 | [1, 5] | Lookback window for determining reachable agents. |
| 40 | KNOWN_GOOD_REGISTRY_SIZE | 10 | [5, 20] | Maximum versions in Known-Good Registry. |
| 41 | KNOWN_GOOD_QUALIFICATION_EPOCHS | 100 | [50, 500] | Consecutive successful epochs to qualify. |
| 42 | AUTO_ROLLBACK_FAILED_EPOCHS | 5 | [3, 10] | Consecutive failed epochs for tertiary auto-rollback. |

---

## 2. Governance Channel Redundancy

### 2.1 Three-Channel Architecture

The existing specification defines a single dedicated governance channel (the Governance Plane, Section 14.1). This addendum introduces a three-channel failover architecture.

```
enum GovernanceChannel:
    PRIMARY    = 1   // Existing governance mesh (persistent gossip overlay)
    SECONDARY  = 2   // Out-of-band point-to-point protocol
    TERTIARY   = 3   // Time-based automatic rollback (no communication required)
```

**Primary Channel: Governance Mesh (existing)**
- Persistent gossip overlay among governance agents.
- Independent of tidal data plane.
- Standard ETR and Critical ETR votes propagate here first.
- Health monitored via governance heartbeats (existing metric: governance channel availability).

**Secondary Channel: Out-of-Band Direct Exchange**
- Point-to-point vote exchange between governance agents.
- Each governance agent maintains a partial roster of peer governance agents' network addresses (obtained during healthy Primary operation).
- Votes are exchanged via direct unicast, bypassing the gossip overlay entirely.
- Activated when Primary channel availability drops below SECONDARY_ACTIVATION_THRESHOLD (default 80%).
- Uses epidemic dissemination: each agent forwards received votes to K random known peers (K = SECONDARY_FANOUT, default 5) until convergence or timeout.

**Tertiary Channel: Automatic Time-Based Rollback**
- No communication required. Each agent acts independently.
- If no successful tidal epoch completes for AUTO_ROLLBACK_FAILED_EPOCHS (default 5) consecutive attempts, each agent independently reverts to the most recent version in its local copy of the Known-Good Registry.
- Convergence guarantee: because the Known-Good Registry is deterministically maintained (Section 3), all agents with consistent registries will revert to the same version. Agents with stale registries will revert to an older known-good version, which is safe (suboptimal but correct).

### 2.2 Channel Failover Logic

```
struct ChannelHealth:
    primary_available: bool        // governance mesh responding to heartbeats
    primary_latency: float         // avg round-trip on governance mesh (epochs)
    secondary_peer_count: int      // number of reachable direct peers
    consecutive_failed_epochs: int // epochs with no successful tidal completion

function select_governance_channel(health: ChannelHealth) -> GovernanceChannel:
    // Primary: governance mesh is healthy
    if health.primary_available and health.primary_latency < 1.0:
        return PRIMARY

    // Secondary: mesh is degraded but we can reach peers directly
    if health.secondary_peer_count >= SECONDARY_MIN_PEERS:
        return SECONDARY

    // Tertiary: no governance communication possible; act autonomously
    return TERTIARY

// Constants
SECONDARY_ACTIVATION_THRESHOLD = 0.80   // primary availability below this -> try secondary
SECONDARY_MIN_PEERS = 3                 // minimum direct peers for secondary to function
SECONDARY_FANOUT = 5                    // epidemic dissemination fan-out
```

### 2.3 Secondary Channel Protocol

```
struct DirectVoteMessage:
    payload: ETRVote              // Standard or Critical ETR vote
    hop_count: int                // incremented at each relay; max MAX_HOPS (default 6)
    origin_agent: AgentID         // original voter
    relay_chain: List<AgentID>    // agents that relayed this message (tamper detection)
    signature: Signature          // origin agent's signature over (payload, hop_count=0)

function secondary_channel_send(agent, vote: ETRVote):
    msg = DirectVoteMessage(
        payload = vote,
        hop_count = 0,
        origin_agent = agent.id,
        relay_chain = [agent.id],
        signature = sign(agent.private_key, canonical_bytes(vote))
    )
    // Send to K random governance peers from cached roster
    peers = random_sample(agent.governance_peer_roster, SECONDARY_FANOUT)
    for peer in peers:
        direct_send(peer.address, msg)

function secondary_channel_receive(agent, msg: DirectVoteMessage):
    // Validate signature (prevents forgery)
    if not verify(msg.origin_agent.public_key, msg.signature, canonical_bytes(msg.payload)):
        drop(msg)
        return

    // Deduplicate
    if agent.seen_votes.contains(hash(msg.payload)):
        return
    agent.seen_votes.add(hash(msg.payload))

    // Record the vote
    agent.etr_vote_collector.add(msg.payload)

    // Relay if under hop limit
    if msg.hop_count < MAX_HOPS:
        relay_msg = msg with {
            hop_count = msg.hop_count + 1,
            relay_chain = msg.relay_chain + [agent.id]
        }
        relay_peers = random_sample(
            agent.governance_peer_roster - set(msg.relay_chain),
            SECONDARY_FANOUT
        )
        for peer in relay_peers:
            direct_send(peer.address, relay_msg)
```

### 2.4 Tertiary Channel: Autonomous Rollback

```
function tertiary_autonomous_rollback(agent):
    """
    Called by each agent's local epoch completion handler.
    No communication with other agents.
    """
    if agent.consecutive_failed_epochs >= AUTO_ROLLBACK_FAILED_EPOCHS:
        target = agent.known_good_registry.most_recent()
        if target is None:
            target = GENESIS_TIDAL_FUNCTION  // always available

        log(CONSTITUTIONAL_EXCEPTION,
            "TERTIARY_AUTO_ROLLBACK",
            f"Agent {agent.id} autonomously reverting to version {target.version_id} "
            f"after {agent.consecutive_failed_epochs} consecutive failed epochs. "
            f"Post-mortem required.")

        agent.tidal_function = target.tidal_function
        agent.tidal_version = target.version_id
        agent.enter_safe_mode(reason="TERTIARY_ROLLBACK")

        // Reset failure counter
        agent.consecutive_failed_epochs = 0
```

**Convergence after tertiary rollback.** When agents independently revert:
- All agents with identical Known-Good Registries revert to the same version (determinism from shared registry state).
- Agents with divergent registries (due to partition during registry updates) may revert to different known-good versions. This is acceptable because all known-good versions are by definition functional. The system will enter SAFE_MODE (Section 4) and Standard ETR can subsequently unify all agents onto a single version once governance is restored.

### 2.5 Channel Health Monitoring

```
function monitor_channel_health(agent) -> ChannelHealth:
    // Primary: check governance heartbeat responses
    primary_ok = agent.governance_mesh.heartbeat_success_rate(window=2_epochs) > 0.80
    primary_lat = agent.governance_mesh.avg_round_trip(window=2_epochs)

    // Secondary: count recently-contacted direct peers
    sec_peers = count(p for p in agent.governance_peer_roster
                      if p.last_direct_contact_epoch >= current_epoch() - 2)

    // Tertiary: pure local state
    failed = agent.consecutive_failed_epochs

    return ChannelHealth(
        primary_available = primary_ok,
        primary_latency = primary_lat,
        secondary_peer_count = sec_peers,
        consecutive_failed_epochs = failed
    )
```

---

## 3. Known-Good Version Registry

### 3.1 Data Structure

```
struct KnownGoodVersion:
    version_id: VersionHash          // SHA256 of the tidal function definition
    tidal_function: TidalFunction    // the complete function (AASL-encoded)
    qualification_epoch: EpochNumber // epoch at which this version qualified
    consecutive_success_count: int   // epochs of consecutive success (>= KNOWN_GOOD_QUALIFICATION_EPOCHS)
    activated_epoch: EpochNumber     // epoch when this version was first activated
    is_genesis: bool                 // true only for the genesis tidal function

struct KnownGoodRegistry:
    versions: OrderedList<KnownGoodVersion>  // ordered by qualification_epoch, newest first
    max_size: int = KNOWN_GOOD_REGISTRY_SIZE // default 10
    registry_hash: Hash              // SHA256 of canonical serialization (for consistency checks)

    // INVARIANT: The genesis tidal function is ALWAYS present.
    // INVARIANT: len(versions) <= max_size.
    // INVARIANT: All versions have consecutive_success_count >= KNOWN_GOOD_QUALIFICATION_EPOCHS.
    // INVARIANT: versions are ordered by qualification_epoch descending.
```

### 3.2 Qualification Logic

```
function update_known_good_tracking(registry: KnownGoodRegistry,
                                     current_version: VersionHash,
                                     epoch_result: EpochResult,
                                     tracker: VersionTracker):
    """
    Called at every epoch boundary by every agent.
    Deterministic: same inputs -> same outputs (preserves INV-2).
    """

    // Define "successful epoch" for qualification purposes
    epoch_successful = (
        epoch_result.scheduling_failure_rate < 0.10   // <10% scheduling failures
        and epoch_result.verification_formation_rate > 0.90  // >90% committees formed
        and epoch_result.settlement_divergence == 0.0  // zero divergence
    )

    if epoch_successful:
        tracker.consecutive_successes[current_version] += 1
    else:
        // Any failure resets the counter for the current version
        tracker.consecutive_successes[current_version] = 0

    // Check if current version qualifies
    if (tracker.consecutive_successes[current_version] >= KNOWN_GOOD_QUALIFICATION_EPOCHS
        and current_version not in registry):
        add_to_registry(registry, current_version, tracker)

function add_to_registry(registry: KnownGoodRegistry,
                          version_id: VersionHash,
                          tracker: VersionTracker):
    new_entry = KnownGoodVersion(
        version_id = version_id,
        tidal_function = tracker.function_cache[version_id],
        qualification_epoch = current_epoch(),
        consecutive_success_count = tracker.consecutive_successes[version_id],
        activated_epoch = tracker.activation_epochs[version_id],
        is_genesis = False
    )

    registry.versions.insert(0, new_entry)  // newest first

    // Enforce size limit: remove oldest non-genesis version
    while len(registry.versions) > registry.max_size:
        // Find oldest non-genesis entry
        for i in range(len(registry.versions) - 1, -1, -1):
            if not registry.versions[i].is_genesis:
                registry.versions.remove(i)
                break

    // Update registry hash for consistency verification
    registry.registry_hash = sha256(canonical_serialize(registry.versions))
```

### 3.3 Registry Initialization

```
function initialize_known_good_registry(genesis_function: TidalFunction) -> KnownGoodRegistry:
    genesis_entry = KnownGoodVersion(
        version_id = sha256(canonical_serialize(genesis_function)),
        tidal_function = genesis_function,
        qualification_epoch = 0,  // epoch 0
        consecutive_success_count = KNOWN_GOOD_QUALIFICATION_EPOCHS,  // pre-qualified
        activated_epoch = 0,
        is_genesis = True
    )

    return KnownGoodRegistry(
        versions = [genesis_entry],
        max_size = KNOWN_GOOD_REGISTRY_SIZE,
        registry_hash = sha256(canonical_serialize([genesis_entry]))
    )
```

### 3.4 Registry Consistency

Because the Known-Good Registry is updated deterministically from shared inputs (epoch results), all non-partitioned agents maintain identical registries. The `registry_hash` field allows agents to detect divergence during governance heartbeats:

```
function check_registry_consistency(agent, peer_heartbeat):
    if peer_heartbeat.registry_hash != agent.known_good_registry.registry_hash:
        log(WARNING, "Known-Good Registry divergence detected",
            peer=peer_heartbeat.agent_id,
            local_hash=agent.known_good_registry.registry_hash,
            peer_hash=peer_heartbeat.registry_hash)

        // Attempt reconciliation: exchange registries and take the union,
        // keeping only entries both agents can independently verify qualified.
        // If reconciliation fails, the agent with fewer entries adopts the
        // superset (safe because all entries are by definition known-good).
```

### 3.5 Rollback Target Selection

```
function select_rollback_target(registry: KnownGoodRegistry,
                                 current_version: VersionHash) -> KnownGoodVersion:
    // Select the most recent known-good version that is NOT the current (broken) version
    for entry in registry.versions:  // newest first
        if entry.version_id != current_version:
            return entry

    // If all known-good versions have been tried (extreme edge case),
    // fall back to genesis
    return registry.get_genesis()
```

---

## 4. Automatic Degradation: SAFE_MODE

### 4.1 SAFE_MODE Definition

SAFE_MODE is the state of last resort: entered when both Standard ETR and Critical ETR have failed, or when Tertiary autonomous rollback has occurred. It is a constitutionally recognized exception state in which the system trades all optimization for correctness.

**SAFE_MODE behavioral guarantees:**

| Subsystem | Normal Mode | SAFE_MODE |
|-----------|-------------|-----------|
| Operation classification | Five-class algebra (M/B/X/V/G) | All operations treated as X-class (quorum protocol) |
| Scheduling | Deterministic hash ring with predictive communication | Hash ring scheduling retained, predictive communication disabled; standard messaging only |
| Settlement | Four-stream scoring (compliance, verification, knowledge, signaling) | Flat-rate settlement: equal rewards to all participating agents per epoch |
| Verification | VRF dual defense with pre-stratified diversity pools | Random committee selection (uniform random, no VRF, no diversity filter) |
| Communication | Predictive delta (zero comm) + stigmergic decay | Standard messaging only (all communication is explicit) |
| Governance | Full G-class with 75% supermajority | Standard ETR voting on any available channel; no other governance actions until SAFE_MODE exits |

### 4.2 State Machine

```
enum SystemState:
    NORMAL              // Full operational mode
    STANDARD_ETR        // Standard ETR in progress (system continues, governance active)
    CRITICAL_ETR        // Critical ETR in progress (accelerated voting, reduced quorum)
    SAFE_MODE           // All optimization suspended; correctness-only operation
    RECOVERY            // SAFE_MODE exiting; re-enabling optimizations progressively

// State transition table
TRANSITIONS = {
    NORMAL -> STANDARD_ETR:
        trigger: Standard ETR trigger detected
        action: Begin Standard ETR voting

    NORMAL -> CRITICAL_ETR:
        trigger: Critical ETR trigger detected (C1-C4)
        action: Begin Critical ETR voting on best available channel

    STANDARD_ETR -> NORMAL:
        trigger: Standard ETR approved and rollback complete
        action: Resume normal operation with rolled-back version

    STANDARD_ETR -> CRITICAL_ETR:
        trigger: Standard ETR fails 6 times (escalation)
                 OR Critical trigger detected during Standard ETR
        action: Escalate to Critical ETR

    CRITICAL_ETR -> NORMAL:
        trigger: Critical ETR approved and rollback complete
        action: Resume normal operation with rolled-back version

    CRITICAL_ETR -> SAFE_MODE:
        trigger: Critical ETR vote fails (67% not reached)
                 OR Critical ETR vote window expires with no quorum
        action: Enter SAFE_MODE immediately

    NORMAL -> SAFE_MODE:
        trigger: Tertiary autonomous rollback activated
        action: Enter SAFE_MODE after autonomous rollback

    SAFE_MODE -> RECOVERY:
        trigger: Standard ETR successfully completes while in SAFE_MODE
                 (governance restored enough for 90% supermajority)
        action: Begin progressive re-enablement

    RECOVERY -> NORMAL:
        trigger: All subsystems restored and stable for RECOVERY_EPOCHS (default 10)
        action: Resume full NORMAL operation

    SAFE_MODE -> SAFE_MODE:
        trigger: Standard ETR attempt fails during SAFE_MODE
        action: Remain in SAFE_MODE; log continued governance failure
}
```

### 4.3 SAFE_MODE Entry Procedure

```
function enter_safe_mode(agent, reason: str):
    """
    Deterministic entry procedure. Each agent executes independently.
    Convergence guaranteed because SAFE_MODE behavior is deterministic
    and does not depend on inter-agent agreement.
    """
    log(CONSTITUTIONAL_EXCEPTION, "SAFE_MODE_ENTRY",
        reason=reason, epoch=current_epoch(), agent=agent.id)

    agent.system_state = SAFE_MODE
    agent.safe_mode_entry_epoch = current_epoch()
    agent.safe_mode_reason = reason

    // 1. Disable predictive communication
    agent.predictive_delta.disable()
    agent.communication_mode = STANDARD_MESSAGING

    // 2. Downgrade all operations to X-class
    agent.operation_classifier.override_all_to_x_class()

    // 3. Switch to flat-rate settlement
    agent.settlement_calculator.mode = FLAT_RATE

    // 4. Switch to random committee selection
    agent.verification_engine.committee_selection = UNIFORM_RANDOM
    agent.verification_engine.vrf_enabled = False
    agent.verification_engine.diversity_filter = False

    // 5. Freeze governance (except ETR voting)
    agent.governance_client.freeze_non_etr()

    // 6. Begin SAFE_MODE heartbeats on all available channels
    // These heartbeats allow agents to detect when enough peers are in SAFE_MODE
    // to attempt Standard ETR for recovery
    agent.safe_mode_heartbeat.start()
```

### 4.4 SAFE_MODE Operation

```
function safe_mode_epoch(agent):
    """
    Main epoch loop during SAFE_MODE.
    """
    // Scheduling: hash ring still works (it is deterministic from roster)
    // but we fall back to standard messaging for all coordination
    assignments = agent.tidal_scheduler.compute_assignments(current_epoch())
    agent.execute_assignments(assignments)

    // Settlement: flat rate
    settlement = flat_rate_settlement(agent, current_epoch())
    agent.record_settlement(settlement)

    // Verification: random committees (no VRF)
    if agent.assigned_to_verify(current_epoch()):
        committee = random_committee_select(
            agent.parcel.agents,
            size=DEFAULT_COMMITTEE_SIZE,
            seed=epoch_seed(current_epoch())  // deterministic random for consistency
        )
        agent.verify_with_committee(committee)

    // Recovery check: periodically attempt Standard ETR to exit SAFE_MODE
    if (current_epoch() - agent.safe_mode_entry_epoch) % SAFE_MODE_ETR_RETRY_INTERVAL == 0:
        attempt_safe_mode_recovery(agent)

function flat_rate_settlement(agent, epoch) -> Settlement:
    """
    Equal distribution: total epoch budget / number of participating agents.
    Participating = completed at least one assigned task this epoch.
    """
    participating = count(a for a in agent.parcel.agents
                          if a.tasks_completed(epoch) > 0)
    if participating == 0:
        return Settlement(amount=0)

    per_agent = EPOCH_SETTLEMENT_BUDGET / participating
    return Settlement(amount=per_agent, stream="SAFE_MODE_FLAT_RATE")

function random_committee_select(agents, size, seed) -> List<AgentID>:
    """
    Deterministic random selection using epoch seed.
    No VRF, no diversity filter, no pre-stratification.
    Simple but correct.
    """
    rng = PRNG(seed)
    pool = list(agents)
    rng.shuffle(pool)
    return pool[:min(size, len(pool))]
```

### 4.5 Recovery From SAFE_MODE

```
function attempt_safe_mode_recovery(agent):
    """
    While in SAFE_MODE, periodically attempt to restore governance.
    """
    // Check: can we reach enough governance agents for Standard ETR?
    channel_health = monitor_channel_health(agent)

    if channel_health.primary_available:
        // Governance mesh is back. Propose Standard ETR to officially
        // ratify the current tidal version (which is the rollback target).
        log(INFO, "Governance channel restored. Attempting Standard ETR for SAFE_MODE exit.")

        proposal = StandardETRProposal(
            target_version = agent.tidal_version,  // ratify current (rolled-back) version
            reason = "SAFE_MODE_EXIT_RATIFICATION",
            proposed_by = agent.id
        )
        broadcast_on_primary(proposal)

        // If this Standard ETR succeeds, transition to RECOVERY
        // (handled by the Standard ETR result handler)

    elif channel_health.secondary_peer_count >= SECONDARY_MIN_PEERS:
        // Try secondary channel for governance coordination
        log(INFO, "Primary channel still down. Attempting coordination via secondary.")
        // Exchange SAFE_MODE heartbeats to build peer awareness
        agent.safe_mode_heartbeat.send_via_secondary()

function enter_recovery(agent, etr_result: ETRDecision):
    """
    Transition from SAFE_MODE to RECOVERY after successful Standard ETR.
    Progressive re-enablement to avoid shocking the system.
    """
    assert agent.system_state == SAFE_MODE
    assert etr_result.outcome == APPROVED

    log(INFO, "SAFE_MODE -> RECOVERY", epoch=current_epoch())
    agent.system_state = RECOVERY
    agent.recovery_entry_epoch = current_epoch()

    // Phase 1 (epochs 1-3): Re-enable VRF committee selection
    schedule_at(current_epoch() + 1, lambda:
        agent.verification_engine.vrf_enabled = True
        agent.verification_engine.diversity_filter = True
        agent.verification_engine.committee_selection = VRF_DUAL_DEFENSE
    )

    // Phase 2 (epochs 4-6): Re-enable predictive communication
    schedule_at(current_epoch() + 4, lambda:
        agent.predictive_delta.enable()
        agent.communication_mode = PREDICTIVE_DELTA
    )

    // Phase 3 (epochs 7-9): Restore operation classification
    schedule_at(current_epoch() + 7, lambda:
        agent.operation_classifier.restore_normal_classification()
    )

    // Phase 4 (epoch 10): Restore four-stream settlement and full governance
    schedule_at(current_epoch() + 10, lambda:
        agent.settlement_calculator.mode = FOUR_STREAM
        agent.governance_client.unfreeze_all()
        agent.system_state = NORMAL
        log(INFO, "RECOVERY -> NORMAL", epoch=current_epoch())
        log(CONSTITUTIONAL_EXCEPTION, "SAFE_MODE_POST_MORTEM_REQUIRED",
            safe_mode_duration = current_epoch() - agent.safe_mode_entry_epoch,
            reason = agent.safe_mode_reason)
    )

// Constants
SAFE_MODE_ETR_RETRY_INTERVAL = 10  // epochs between recovery attempts
RECOVERY_EPOCHS = 10               // total epochs for progressive re-enablement
```

### 4.6 SAFE_MODE Monitoring

```
struct SafeModeMetrics:
    entry_epoch: EpochNumber
    duration_epochs: int
    reason: str
    recovery_attempts: int
    governance_channel_status: ChannelHealth
    agent_participation_rate: float     // fraction of roster executing tasks
    settlement_total: float             // cumulative flat-rate settlement
    verification_committee_success: float  // fraction of random committees that formed

// SAFE_MODE persists until Standard ETR succeeds.
// There is no time-based automatic exit from SAFE_MODE.
// This is intentional: SAFE_MODE is a constitutionally recognized exception
// that requires explicit governance ratification to exit.
```

---

## 5. Integrated Control Flow

The complete ETR hardening control flow, incorporating all four sections:

```
function etr_master_control(agent, epoch_result: EpochResult):
    """
    Called at each epoch boundary. Orchestrates the complete hardened ETR.
    """
    // 0. Update Known-Good Registry tracking
    update_known_good_tracking(
        agent.known_good_registry,
        agent.tidal_version,
        epoch_result,
        agent.version_tracker
    )

    // 1. Track consecutive failures for Tertiary channel
    if epoch_result.successful:
        agent.consecutive_failed_epochs = 0
    else:
        agent.consecutive_failed_epochs += 1

    // 2. If already in SAFE_MODE, run SAFE_MODE epoch logic
    if agent.system_state == SAFE_MODE:
        safe_mode_epoch(agent)
        return

    // 3. Check Tertiary trigger (autonomous rollback)
    if agent.consecutive_failed_epochs >= AUTO_ROLLBACK_FAILED_EPOCHS:
        tertiary_autonomous_rollback(agent)
        return

    // 4. Evaluate Critical ETR triggers
    critical_proposal = evaluate_critical_etr_triggers(agent, agent.local_state)
    if critical_proposal is not None:
        channel = select_governance_channel(monitor_channel_health(agent))
        broadcast_critical_etr(critical_proposal, channel)
        agent.system_state = CRITICAL_ETR
        return

    // 5. Evaluate Standard ETR triggers (existing logic from Section 7.3)
    standard_trigger = evaluate_standard_etr_triggers(agent, epoch_result)
    if standard_trigger is not None:
        broadcast_standard_etr(standard_trigger, PRIMARY)
        agent.system_state = STANDARD_ETR
        return
```

---

## 6. Interaction With Existing Mechanisms

### 6.1 Invariant Preservation

This addendum preserves all seven system invariants (Section 1.4):

- **INV-1 (Membrane sovereignty):** SAFE_MODE continues verification (random committees). The membrane is never bypassed.
- **INV-2 (Determinism):** Known-Good Registry updates are deterministic. SAFE_MODE behavior is deterministic. Tertiary rollback target selection is deterministic from shared registry state.
- **INV-3 (Prove-before-trust):** SAFE_MODE overrides all operations to X-class, which is stricter than M-class. The invariant holds trivially.
- **INV-4 (Parcel boundaries):** Unchanged. SAFE_MODE does not alter parcel topology.
- **INV-5 (Signal decay):** Predictive communication is disabled in SAFE_MODE. Standard messaging inherits existing decay semantics.
- **INV-6 (Graceful degradation):** This addendum IS the formal specification of INV-6 for the ETR subsystem. The degradation chain is: Normal -> Standard ETR -> Critical ETR -> SAFE_MODE.
- **INV-7 (Recursive self-verification):** In SAFE_MODE, the tidal function is a known-good version from the registry, which by definition has been verified. The self-verification closure is maintained.

### 6.2 Constitutional Impact

The following constitutional provisions are added:

1. **CONST-ETR-1:** Critical ETR is a constitutionally recognized emergency mechanism. Its quorum and trigger parameters can only be modified by G-class constitutional consensus (same protection as Standard ETR).
2. **CONST-ETR-2:** SAFE_MODE is a constitutionally recognized exception state. Every SAFE_MODE episode requires a post-mortem governance review within 30 epochs of SAFE_MODE exit.
3. **CONST-ETR-3:** The Known-Good Registry is constitutionally protected. Its update logic (Section 3.2) cannot be modified except by G-class constitutional consensus. The genesis entry cannot be removed.
4. **CONST-ETR-4:** Tertiary autonomous rollback is a constitutionally authorized unilateral agent action. No individual agent is penalized for executing autonomous rollback when the trigger condition (AUTO_ROLLBACK_FAILED_EPOCHS consecutive failures) is met.

### 6.3 Impact on GATE-3 Validation

The existing GATE-3 experiment (ETR activation under scheduling disruption) must be extended:

**GATE-3A (existing):** Standard ETR activation under scheduling disruption. Kill criterion unchanged.

**GATE-3B (new):** Critical ETR activation under governance channel degradation. Inject both a tidal function bug AND governance mesh partition (50% of governance agents unreachable). Measure time from trigger detection to Critical ETR approval using secondary channel. Kill criterion: Critical ETR fails to activate within 2 epochs in more than 20% of simulation runs.

**GATE-3C (new):** Tertiary autonomous rollback convergence. Inject a tidal function bug causing 100% epoch failure with governance completely offline. Measure time for all agents to autonomously revert to the same known-good version. Kill criterion: more than 10% of agents are on a different version after AUTO_ROLLBACK_FAILED_EPOCHS + 2 epochs.

**GATE-3D (new):** SAFE_MODE recovery. After triggering SAFE_MODE, restore governance channel. Measure time from governance restoration to NORMAL state re-entry. Kill criterion: recovery takes more than RECOVERY_EPOCHS + 10 epochs in more than 20% of simulation runs.

### 6.4 Impact on Risk Register

| Risk | Severity | Mitigation (before this addendum) | Mitigation (after this addendum) |
|------|----------|-----------------------------------|----------------------------------|
| ETR 90% threshold unreachable | MEDIUM | Dedicated governance channel + threshold reduction | Two-tier ETR: Critical ETR at 67% of reachable agents. Tertiary auto-rollback if all voting fails. |
| Governance channel failure | MEDIUM | Single dedicated channel (assumed reliable) | Three-channel failover: mesh, direct P2P, autonomous rollback. |
| Cascading failure freezes governance | HIGH | Degraded mode guarantees (Section 7.5) | Formal SAFE_MODE state machine with progressive recovery. |
| Rollback to untested version | LOW | "Most recent previously-verified" (vague) | Known-Good Registry: only versions with 100+ successful epochs. |
| Blocking coalition (10%) prevents ETR | MEDIUM | Threshold reduction 90%->80% after 3 failures | Critical ETR uses 67% of reachable (not all) agents. Tertiary rollback has no voting. |

### 6.5 New AASL Message Types

| Message | Direction | Payload | Trigger |
|---------|-----------|---------|---------|
| CRITICAL_ETR_PROPOSE | Governance -> Governance | CriticalETRProposal | Critical trigger detected |
| CRITICAL_ETR_VOTE | Governance -> Governance | CriticalETRVote | On Critical ETR proposal |
| SAFE_MODE_HEARTBEAT | Agent -> Agent | SafeModeStatus | While in SAFE_MODE |
| SAFE_MODE_EXIT_PROPOSE | Governance -> Governance | StandardETRProposal | Recovery attempt |
| REGISTRY_SYNC | Governance -> Governance | KnownGoodRegistry | Registry divergence detected |

---

## 7. Open Questions and Design Risks

1. **67% quorum for Critical ETR.** The 67% threshold was chosen to match standard BFT fault tolerance (2/3 + 1). However, "67% of reachable agents" introduces subjectivity — different agents may have different views of who is reachable. If two partitions each believe they have 67% of reachable agents, they could approve conflicting rollback targets. **Mitigation:** Critical ETR can only target Known-Good Registry versions, and all known-good versions are by definition safe. Divergent rollback targets are suboptimal (different partitions running different known-good versions) but not catastrophic. SAFE_MODE will be entered in both partitions, and reconciliation occurs when the partition heals.

2. **Known-Good qualification period.** 100 consecutive successful epochs is a conservative threshold that may delay initial registry population. During the early deployment (Phase 1-2), the registry may contain only the genesis version for an extended period. **Mitigation:** This is acceptable — the genesis version is always available as a rollback target, and early deployment is closely monitored.

3. **SAFE_MODE liveness.** SAFE_MODE has no time-based exit. If governance never recovers, the system remains in SAFE_MODE indefinitely. This is a deliberate design choice: autonomous exit from SAFE_MODE without governance ratification would undermine constitutional protections. **Mitigation:** SAFE_MODE is functional (agents execute tasks, verify claims, earn flat-rate rewards). It is suboptimal but not dead.

4. **Secondary channel bootstrap.** The secondary channel requires agents to have cached peer addresses from healthy Primary operation. If the Primary channel has never been healthy (e.g., failure during initial deployment), the secondary channel has no peer roster. **Mitigation:** Phase 1 deployment includes a bootstrap peer list as a configuration parameter, similar to blockchain seed nodes.

---

## Appendix A: Summary of Changes to C3-A Section References

| C3-A Section | Change |
|--------------|--------|
| 3.1 (Operation Classes) | Add note: SAFE_MODE overrides all classes to X-class. |
| 7.3 (ETR) | Rename to "Standard ETR." Add cross-reference to this addendum for Critical ETR. |
| 7.5 (Cross-Integration Failure) | Add SAFE_MODE to degraded mode guarantees. |
| 8 (Economic Settlement) | Add SAFE_MODE flat-rate settlement as alternative mode. |
| 10.3 (Coalition Analysis) | Update 10% blocking coalition analysis: Critical ETR and Tertiary rollback bypass blocking. |
| 12.1 (Hard Gate Experiments) | Add GATE-3B, GATE-3C, GATE-3D. |
| 13 (Risk Assessment) | Update risk register per Section 6.4 above. |
| 14.2 (Operational Monitoring) | Add SAFE_MODE metrics. |
| Appendix B (Constants) | Add constants 32-42 from Section 1.5. |
| Appendix D (Glossary) | Add: Critical ETR, SAFE_MODE, Known-Good Registry, Tertiary Rollback. |

---

*End of Hardening Addendum.*
