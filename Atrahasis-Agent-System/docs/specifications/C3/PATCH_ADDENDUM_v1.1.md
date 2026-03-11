# C3 Tidal Noosphere — Patch Addendum PA-C3-01
## Engineering Findings F4, F5, F6, F15, F16, F18 + Errata E-C3-01, E-C3-02, E-C3-03

**Applies to:** MASTER_TECH_SPEC.md v1.0 (C3-A)
**Date:** 2026-03-10
**Status:** ADDENDUM — supplements but does not replace the base spec
**Scope:** MEDIUM-severity engineering fixes only. CRITICAL items (reconfiguration storm, VRF grinding amplification, small-ring imbalance root cause, emergency rollback race conditions, cross-integration cascade) are deferred to Hardening Pass HP-C3-01.

---

## Table of Contents

- [PA-F4: VRF Path Simplification for Early Phases](#pa-f4-vrf-path-simplification-for-early-phases)
- [PA-F5: PTP Clarification](#pa-f5-ptp-clarification)
- [PA-F6: Deployment Profiles](#pa-f6-deployment-profiles)
- [PA-F15: In-Flight Surprise Signals During Reconfiguration](#pa-f15-in-flight-surprise-signals-during-reconfiguration)
- [PA-F16: Threshold Calibration Coupling](#pa-f16-threshold-calibration-coupling)
- [PA-F18: AASL Type Retirement](#pa-f18-aasl-type-retirement)
- [Errata: E-C3-01, E-C3-02, E-C3-03](#errata)

---

## PA-F4: VRF Path Simplification for Early Phases

**Finding:** The VRF dual-defense mechanism (Section 5.2) specifies commit-reveal + pre-stratified diversity post-filtering for all deployment phases. At fewer than 100 agents, this is overbuilt: the attack surface is small (all agents are known participants in a permissioned development environment), grinding is unprofitable (the reward from biasing a 7-member committee drawn from 50 agents is negligible relative to the effort), and the diversity pools are too small for meaningful stratification (a pool with 3 agents cannot provide genuine diversity — the spec itself acknowledges this in Section 11.1).

**Resolution:** Replace the single VRF protocol with a phased deployment that adds defensive layers as the attack surface grows.

### F4.1 Phase Definitions and Transition Triggers

```
enum VRFPhase { SIMPLE, COMMITTED, FULL_DUAL_DEFENSE }

function determine_vrf_phase(locus: Locus) -> VRFPhase:
  agent_count = count_eligible_verifiers(locus)

  if agent_count < VRF_PHASE2_THRESHOLD:        // default 100
    return SIMPLE
  elif agent_count < VRF_PHASE3_THRESHOLD:       // default 1000
    return COMMITTED
  else:
    return FULL_DUAL_DEFENSE
```

**Transition triggers:**

| Transition | Trigger | Activation | Rollback |
|---|---|---|---|
| SIMPLE -> COMMITTED | `eligible_verifiers(locus) >= VRF_PHASE2_THRESHOLD` for 3 consecutive epochs | Next epoch boundary after 3rd consecutive qualifying epoch | Auto-rollback to SIMPLE if count drops below `VRF_PHASE2_THRESHOLD - HYSTERESIS_BAND` (default 10) for 3 consecutive epochs |
| COMMITTED -> FULL_DUAL_DEFENSE | `eligible_verifiers(locus) >= VRF_PHASE3_THRESHOLD` for 5 consecutive epochs | Next epoch boundary after 5th consecutive qualifying epoch | Auto-rollback to COMMITTED if count drops below `VRF_PHASE3_THRESHOLD - HYSTERESIS_BAND` (default 50) for 5 consecutive epochs |

**Hysteresis rationale:** The 3-epoch / 5-epoch sustain requirements and the downward hysteresis band prevent oscillation when agent counts hover near thresholds. Without hysteresis, a locus at 99-101 agents would flip between SIMPLE and COMMITTED every epoch, invalidating cached VRF state each time.

```
// New configurable constants (add to Appendix B)
// #42: VRF_PHASE2_THRESHOLD     default: 100    range: [50, 500]
// #43: VRF_PHASE3_THRESHOLD     default: 1000   range: [500, 5000]
// #44: VRF_HYSTERESIS_BAND      default: 10     range: [5, 50]
// #45: VRF_PHASE2_SUSTAIN       default: 3      range: [1, 10]  epochs
// #46: VRF_PHASE3_SUSTAIN       default: 5      range: [2, 15]  epochs
```

### F4.2 Phase 1 Algorithm: SIMPLE VRF Selection

Phase 1 uses direct ECVRF self-selection with no commit-reveal overhead and no diversity post-filtering. The committee is formed purely from VRF sortition output.

```
function select_verifiers_simple(
  claim: Claim,
  epoch: uint64,
  vrf_seed: bytes[32],
  eligible: Set<Agent>,
  committee_size: uint8         // default 7
) -> (Set<AgentId>, List<VRFProof>):

  // Step 1: Compute VRF input from claim + epoch + seed
  alpha = SHA256(claim.hash || uint64_be(epoch) || vrf_seed)

  // Step 2: Each eligible agent evaluates VRF
  candidates = []
  for agent in eligible:
    (beta, pi) = ECVRF_prove(agent.privkey, alpha)

    // Self-selection: candidate if output below threshold
    selection_threshold = (committee_size * SELECTION_OVERSAMPLING) / |eligible|
    // SELECTION_OVERSAMPLING = 2.0 — sample 2x committee_size candidates
    // to handle agents that are offline or over-capacity
    if uint256_from_bytes(beta) < floor(selection_threshold * 2^256):
      candidates.append((agent.id, beta, pi))

  // Step 3: Sort by VRF output (deterministic, verifiable ordering)
  candidates.sort_by(c => c.beta)

  // Step 4: Take top committee_size candidates — no diversity filter
  selected = candidates[:committee_size]

  // Step 5: Fallback if fewer candidates than committee_size
  if |selected| < MIN_COMMITTEE_SIZE:    // MIN_COMMITTEE_SIZE = 3
    // Expand threshold by 2x and retry once
    expanded_candidates = []
    for agent in eligible:
      if agent.id in {s.agent_id for s in selected}: continue
      (beta, pi) = ECVRF_prove(agent.privkey, alpha || bytes("fallback"))
      expanded_candidates.append((agent.id, beta, pi))
    expanded_candidates.sort_by(c => c.beta)
    selected.extend(expanded_candidates[:committee_size - |selected|])

  return ({c[0] for c in selected}, {c[2] for c in selected})
```

**Why this is safe at <=100 agents:**

1. **Known participants.** In a <=100-agent network (Phase 1 development), all agents are registered participants with known identities. Sybil attacks require physical onboarding, not just key generation.
2. **Committee is discoverable anyway.** At 50 agents with committee_size=7, an agent has a 14% base probability of being selected. With only 50 possible committee members, the committee composition is not meaningfully secret — the VRF adds verifiability but the secrecy value is minimal.
3. **Grinding is unprofitable.** To bias a committee at N=50, an adversary would need to control multiple identities and resubmit claims across epochs. With claim commitment still enforced (the 1-epoch delay from Section 5.2.2 is retained in all phases — it costs nothing and prevents the simplest shopping attack), the adversary gains at most one extra attempt per epoch.
4. **No diversity pool starvation.** At N=20, a 4-dimensional diversity requirement with committee_size=7 often cannot be satisfied — pools have 2-3 members each, and mandatory diversity slots consume all committee positions, leaving no room for VRF randomness. Removing the diversity filter at this scale actually improves committee randomness.

**What Phase 1 retains from the base spec:**
- ECVRF (RFC 9381) on P-256 — the cryptographic primitive is unchanged
- VRF seed rotation per epoch — unpredictability is maintained
- Claim commitment with 1-epoch delay — prevents committee shopping at zero cost
- Verifiable proofs — any agent can verify committee membership

**What Phase 1 removes:**
- Commit-reveal diversity protocol (Section 5.2.2) — no diversity attributes committed or revealed
- Pre-stratified diversity pools (Section 5.2.3) — no pool construction or maintenance
- DIVERSITY_COOLING_EPOCHS enforcement — no diversity attribute changes to cool
- Diversity-weighted committee composition — pure VRF ranking

### F4.3 Phase 2 Algorithm: COMMITTED

Phase 2 adds commit-reveal for claim hashes and agent diversity attributes. It does NOT add diversity post-filtering.

```
function select_verifiers_committed(
  claim: Claim,
  epoch: uint64,
  vrf_seed: bytes[32],
  eligible: Set<Agent>,
  committee_size: uint8
) -> (Set<AgentId>, List<VRFProof>):

  // Precondition: claim.hash was committed >= 1 epoch ago (retained from Phase 1)
  assert claim.committed_epoch <= epoch - REVEAL_DELAY

  // Precondition: all eligible agents have revealed diversity attributes
  // (agents that have not completed commit-reveal are excluded from eligible set)
  eligible_revealed = {a for a in eligible
                       if a.diversity_attr.revealed
                       and a.diversity_attr.cooling_until <= epoch}

  // VRF selection identical to SIMPLE, but drawn from eligible_revealed
  alpha = SHA256(claim.hash || uint64_be(epoch) || vrf_seed)
  candidates = []
  for agent in eligible_revealed:
    (beta, pi) = ECVRF_prove(agent.privkey, alpha)
    selection_threshold = (committee_size * SELECTION_OVERSAMPLING) / |eligible_revealed|
    if uint256_from_bytes(beta) < floor(selection_threshold * 2^256):
      candidates.append((agent.id, beta, pi))

  candidates.sort_by(c => c.beta)
  selected = candidates[:committee_size]

  // Same fallback as SIMPLE if under MIN_COMMITTEE_SIZE
  if |selected| < MIN_COMMITTEE_SIZE:
    expanded_candidates = []
    for agent in eligible_revealed:
      if agent.id in {s[0] for s in selected}: continue
      (beta, pi) = ECVRF_prove(agent.privkey, alpha || bytes("fallback"))
      expanded_candidates.append((agent.id, beta, pi))
    expanded_candidates.sort_by(c => c.beta)
    selected.extend(expanded_candidates[:committee_size - |selected|])

  return ({c[0] for c in selected}, {c[2] for c in selected})
```

**What Phase 2 adds over Phase 1:**
- Diversity attribute commit-reveal is enforced — agents must commit before eligibility
- DIVERSITY_COOLING_EPOCHS applies — attribute changes incur cooling penalty
- Commit-reveal prevents timing-based grinding (adversary cannot optimize attributes after seeing VRF seeds)

**What Phase 2 still omits:**
- Pre-stratified diversity pools
- Diversity-weighted slot allocation

**Rationale:** At 100-1000 agents, grinding becomes profitable because committee influence is worth more AIC, and the identity pool is large enough that Sybil registration is harder to detect manually. Commit-reveal forces attribute commitment before VRF seeds are known, eliminating the primary grinding vector. Diversity post-filtering is still unnecessary because pool sizes at N=500 are marginal (10-30 agents per stratum) and the added complexity is not justified until strategic identity placement across strata becomes viable.

### F4.4 Phase 3: FULL_DUAL_DEFENSE

Phase 3 (1000+ agents) uses the complete `select_diverse_verifiers()` algorithm as specified in Section 5.2.4 of the base spec, without modification. At this scale, diversity pools have sufficient membership for meaningful stratification, and the adversary's ability to place identities strategically across strata justifies the post-filter defense.

### F4.5 Conformance Amendment

Replace MUST requirement #3 (Section 12.3) with:

> **MUST (revised #3):** Implement ECVRF per RFC 9381 on curve P-256 for all VRF computations. The VRF phase (SIMPLE, COMMITTED, FULL_DUAL_DEFENSE) MUST correspond to the eligible verifier count per Section PA-F4. Implementations MAY skip directly to a higher phase (e.g., deploy with COMMITTED even at <=100 agents) but MUST NOT use a lower phase than the agent count requires.

Replace MUST requirement #10 with:

> **MUST (revised #10):** Enforce the DIVERSITY_COOLING_EPOCHS cooling period for diversity attribute changes in VRF phases COMMITTED and FULL_DUAL_DEFENSE. Phase SIMPLE does not require diversity attribute registration.

---

## PA-F5: PTP Clarification

**Finding:** The Parcel Transition Protocol (Section 7.4) is described as a "three-phase protocol" with phases PREPARE, SWITCH, and STABILIZE. However, STABILIZE is not a protocol phase in the same sense as PREPARE and SWITCH. PREPARE and SWITCH have defined entry conditions, state transitions, and completion criteria that agents execute as part of a coordinated protocol. STABILIZE is a grace period during which agents independently warm up predictive models and refresh VRF caches — there is no coordinated state transition, no completion signal, and agents individually exit TRANSITIONING state as their models converge. Calling it a "phase" creates a false impression of protocol complexity and implies a coordination step that does not exist.

**Resolution:** Rename and restructure. The PTP is a 2-phase protocol followed by a convergence period.

### F5.1 Clarified Protocol Summary

```
PARCEL TRANSITION PROTOCOL (PTP) — Clarified Structure
=======================================================

PHASE 1: PREPARE (exactly 1 epoch)
  Entry:    Bi-timescale controller issues reconfiguration directive
  Actions:  - Freeze parcel membership roster for affected parcels
            - Snapshot current parcel state (agent set, hash ring config,
              SLV, VRF pool membership)
            - Freeze predictive model adaptation (models still predict,
              but weights are not updated — prevents learning on
              soon-to-be-invalid topology)
            - Cache current VRF verifier sets for in-progress verifications
            - Enter communication buffer mode: queue outbound surprise
              signals rather than emitting them (prevents signals to
              agents who will be in a different parcel next epoch)
            - Hash rings continue operating on the pre-reconfiguration
              topology
  Exit:     Next epoch boundary

PHASE 2: MIGRATE (at epoch boundary, atomic)
  Entry:    Epoch boundary following PREPARE
  Actions:  - Reconstruct hash rings for new parcel topology
              (agents removed/added per the reconfiguration directive)
            - Transfer state:
                * Predictive models for agents leaving: serialize to CTV
                  (Compact Transfer Vector, max 1KB per agent)
                * Predictive models for agents arriving: bootstrap from
                  incoming CTV via bootstrap_model()
            - Rebuild VRF eligible sets from new parcel rosters
            - Flush queued surprise signals:
                * Signals to agents still in the same parcel: deliver
                * Signals to agents now in a different parcel: discard
                  with log (see PA-F15)
            - Mark all predictive models as TRANSITIONING
  Atomicity: All agents have identical inputs (reconfiguration directive
             received during PREPARE + deterministic roster). Same inputs
             + deterministic functions = identical outputs. No consensus
             required.
  Exit:     All state transfers complete (bounded by CTV serialization
            time, typically <500ms for parcels of 50 agents)

CONVERGENCE PERIOD: STABILIZE (2-5 epochs, NOT a protocol phase)
  Entry:    Immediately following MIGRATE completion
  Nature:   This is a grace period, not a coordinated protocol phase.
            Agents independently warm up their predictive models on the
            new topology. There is no coordinated entry/exit, no
            state machine transition, and no completion signal.
  Expected behavior:
            - Agents operate with correct hash ring assignments
              (immediate from MIGRATE)
            - Communication uses standard messaging (no predictive
              optimization — predictions are unreliable during warm-up)
            - Models bootstrap from PCT transfer vectors and converge
              via normal observation
            - VRF caches are populated as new verification cycles
              execute on the new roster
  Completion criterion (per-agent, not per-parcel):
            Agent exits TRANSITIONING when model accuracy >=
            ACTIVATION_THRESHOLD (0.7) for 3 consecutive observation
            windows
  Performance during convergence:
            - Scheduling: fully correct (hash rings are rebuilt)
            - Communication: elevated bandwidth (standard messaging
              instead of predictive delta)
            - Verification: fully correct (VRF operates on new roster)
            - Expected bandwidth overhead: 2-5x steady-state, declining
              as models converge
  Parcel exits convergence when:
            >90% of agents have individually exited TRANSITIONING state
```

### F5.2 Naming Amendment

Throughout the base spec, replace references to "3-phase protocol (PREPARE/SWITCH/STABILIZE)" with "2-phase protocol (PREPARE/MIGRATE) + STABILIZE convergence period."

Specifically:
- Section 2.2, Component #6: "Bi-timescale controller, 2-phase Parcel Transition Protocol + convergence period"
- Section 7.4, heading: "Parcel Transition Protocol (2-phase + convergence)"
- Section 7.4, Phase 2 heading: Rename from "SWITCH" to "MIGRATE" (reflects the actual action: state transfer and ring rebuild, not a binary switch)
- Section 7.4, Phase 3 heading: Rename from "STABILIZE" to "Convergence Period: STABILIZE" and add note: "This is a grace period, not a protocol phase."
- Section 10.2, Attack 1 description: "PTP's 2-phase PREPARE/MIGRATE protocol with STABILIZE convergence period"
- Appendix E, GATE-1 row: Same language update

### F5.3 PTP State Machine (new)

```
ParcelState transitions under PTP:

  ACTIVE ---[reconfig directive]--> PREPARING
    |                                   |
    |                            [epoch boundary]
    |                                   |
    |                                   v
    |                              MIGRATING
    |                                   |
    |                            [state transfer
    |                             complete]
    |                                   |
    |                                   v
    |                              CONVERGING
    |                                   |
    |                            [>90% agents
    |                             exit TRANSITIONING]
    |                                   |
    +<----------------------------------+
                 ACTIVE

  Guard: ACTIVE -> PREPARING requires:
    - parcel not in CONVERGING (must finish previous convergence)
    - locus reconfiguration fraction < 20%
    - minimum RECONFIG_MIN_INTERVAL epochs since last PREPARING entry
```

---

## PA-F6: Deployment Profiles

**Finding:** The base spec defines approximately 46 configurable constants (Appendix B, #1-#41, plus implicit constants scattered through the text) but provides only a single default value per parameter. Operators deploying a dev/test cluster at 20 agents face the same parameter file as a production deployment at 5,000 agents. Many defaults are tuned for the Phase 3 target (1K-10K agents) and are inappropriate for smaller deployments — for example, DIVERSITY_COOLING_EPOCHS=50 in a 20-agent dev cluster means a diversity attribute change locks an agent out of verification for 50 hours, which is absurd for development iteration.

**Resolution:** Define three deployment profiles (T1, T2, T3) with concrete parameter values for the 20 most critical parameters.

### F6.1 Profile Definitions

| Profile | Name | Agents | Parcels | Loci | Use Case |
|---------|------|--------|---------|------|----------|
| **T1** | Dev/Test | 10-50 | 1-3 per locus | 1-3 | Local development, CI testing, algorithm validation |
| **T2** | Production Small | 50-500 | 5-20 per locus | 5-50 | Initial production deployment, Phase 2 operations |
| **T3** | Production Large | 500-10,000 | 50+ per locus | 50-500 | Phase 3 primary target, full-scale production |

### F6.2 Critical Parameter Table

| # | Parameter | T1 (Dev/Test) | T2 (Prod Small) | T3 (Prod Large) | Rationale for T1/T2 deviations |
|---|-----------|---------------|-----------------|-----------------|-------------------------------|
| 1 | **EPOCH_DURATION** | 300s (5 min) | 1800s (30 min) | 3600s (1 hr) | T1: fast iteration, see effects quickly. T2: production but lower overhead from shorter boundaries. |
| 2 | **BOUNDARY_WINDOW** | 2s | 3s | 5s | T1: fewer agents, gossip converges in <1s. T2: 500 agents converge in ~2s. |
| 3 | **CLOCK_TOLERANCE** | 2000ms | 1000ms | 500ms | T1: dev machines have worse NTP; relaxed to avoid false timing faults. |
| 4 | **PARCEL_MIN_AGENTS** | 3 | 5 | 5 | T1: allows testing with very small parcels. Load variance is accepted for dev. |
| 5 | **VNODE_MIN** | 100 | 150 | 150 | T1: fewer agents = fewer ring entries needed; speeds ring rebuild. |
| 6 | **VNODE_SCALE** | 500 | 1000 | 1000 | T1: V(5) = max(100, 500/5) = 100 instead of 200; adequate for dev. |
| 7 | **BOUNDED_LOADS_EPSILON** | 0.25 | 0.15 | 0.15 | T1: relaxed balance tolerance reduces churn cost during rapid dev changes. |
| 8 | **COMMITTEE_SIZE** | 3 | 5 | 7 | T1: 7-member committee from 20 agents is 35% of the network — too large. T2: 5 balances diversity and overhead. |
| 9 | **DIVERSITY_COOLING_EPOCHS** | 5 | 25 | 50 | T1: 5 epochs * 5 min = 25 min cooldown, reasonable for dev iteration. T2: 25 * 30 min = 12.5 hr, sufficient grinding deterrent. |
| 10 | **REVEAL_DELAY** | 1 | 1 | 1 | Same across all tiers; 1 epoch is the minimum for claim commitment. |
| 11 | **CHURN_BUDGET_FRACTION** | 0.50 | 0.30 | 0.20 | T1: dev clusters have high agent turnover; allow 50% churn per epoch. T2: more stable but still relaxed. |
| 12 | **RECONFIG_MIN_INTERVAL** | 3 | 5 | 10 | T1: fast reconfiguration for testing PTP. T2: moderate interval. |
| 13 | **LEARNING_RATE** | 0.05 | 0.02 | 0.01 | T1: faster model convergence for short-lived dev sessions. T2: moderate adaptation speed. |
| 14 | **THRESHOLD_TARGET_ACCURACY** | 0.6 | 0.7 | 0.8 | T1: lower accuracy target because dev environments are noisy. |
| 15 | **SIGNAL_BUDGET** | 100 | 75 | 50 | T1: higher budget because dev environments produce more surprises; avoids signal drops obscuring bugs. |
| 16 | **ETR_VOTE_WINDOW** | 1 | 2 | 2 | T1: 1 epoch vote window for rapid ETR testing. |
| 17 | **ETR_SUPERMAJORITY** | 0.75 | 0.85 | 0.90 | T1: lower threshold because governance is a small group (5-15 agents) — 90% of 10 = 9, one absence blocks ETR. T2: slightly relaxed for same reason. |
| 18 | **GOVERNANCE_DISCUSSION_PERIOD** | 1h | 24h | 72h (HIGH) / 24h (LOW) | T1: 1 hour for dev iteration. T2: 24 hours — production but faster governance cycle. |
| 19 | **VRF_PHASE** (from PA-F4) | SIMPLE | COMMITTED | FULL_DUAL_DEFENSE | Per PA-F4 phase boundaries. T2 may be SIMPLE or COMMITTED depending on agent count. |
| 20 | **PROMOTION_THRESHOLD** | 1 | 2 | 3 | T1: immediate anomaly promotion for dev visibility. T2: reduced to catch issues faster. |

### F6.3 Profile Selection and Override

```
function load_deployment_profile(profile: {T1, T2, T3}) -> ParameterSet:
  params = PROFILE_DEFAULTS[profile]

  // Individual overrides are permitted within valid ranges
  for (key, value) in environment_overrides():
    range = PARAMETER_RANGES[key]
    assert range.min <= value <= range.max,
      "Override {key}={value} outside valid range [{range.min}, {range.max}]"
    params[key] = value

  // Cross-parameter validation
  assert params.COMMITTEE_SIZE <= params.PARCEL_MIN_AGENTS,
    "COMMITTEE_SIZE must not exceed PARCEL_MIN_AGENTS"
  assert params.BOUNDARY_WINDOW < params.EPOCH_DURATION * 0.05,
    "BOUNDARY_WINDOW should be <5% of EPOCH_DURATION"
  assert params.ETR_VOTE_WINDOW * params.EPOCH_DURATION <= 7200,
    "ETR total vote time should not exceed 2 hours"

  return params
```

**Profile auto-detection (SHOULD, not MUST):** Implementations SHOULD auto-detect the appropriate profile from the locus agent count at genesis, falling back to T2 if ambiguous. Operators MAY override to a higher profile (T1 cluster running T2 parameters) but MUST NOT override to a lower profile than the agent count warrants.

### F6.4 Conformance Amendment

Add SHOULD requirement #8 (Section 12.3):

> **SHOULD (#8):** Provide pre-configured deployment profiles for T1 (Dev/Test), T2 (Production Small), and T3 (Production Large) per Section PA-F6. Operators SHOULD select the profile matching their deployment scale. Individual parameter overrides are permitted within the valid ranges specified in Appendix B.

---

## PA-F15: In-Flight Surprise Signals During Reconfiguration

**Finding:** The base spec does not define what happens to surprise signals (SRP messages) that are in transit when parcel boundaries change during PTP MIGRATE. A surprise signal emitted by agent A targeting agent B during the epoch before MIGRATE may arrive after B has been reassigned to a different parcel. The signal references a predictive model that no longer exists (A's model of B was reset during MIGRATE), making the signal semantically meaningless to the receiving parcel. Without a defined behavior, implementations may crash, silently drop signals, or misroute them.

**Resolution:** Define explicit routing rules for three cases: in-flight signals, new parcel member cold-start, and the transition acceptance window.

### F15.1 In-Flight Signal Routing During MIGRATE

```
function route_inflight_signal(
  signal: SurpriseSignal,
  current_topology: ParcelTopology,
  previous_topology: ParcelTopology
) -> RoutingDecision:

  dest_agent = signal.target

  // Case 1: Destination agent is in the same parcel as before
  //   (either the agent did not move, or the agent moved to the
  //    same parcel as the signal's source)
  if dest_agent in current_topology.parcel_of(signal.source).agents:
    return DELIVER_TO_ORIGINAL_DESTINATION
    // The predictive model may have been reset, but the signal still
    // carries useful information (the error vector) that the new model
    // can incorporate as an initial observation.

  // Case 2: Destination agent is in the network but in a different parcel
  if dest_agent in current_topology.all_agents():
    return DELIVER_TO_ORIGINAL_DESTINATION
    // Signal is delivered to the agent at its new parcel location.
    // The receiving agent's model for the source (if any) is in
    // TRANSITIONING state. The signal is logged as a "pre-migration
    // observation" but does NOT update model weights.
    // Rationale: the signal reflects pre-reconfiguration behavior
    // and is stale, but delivering it allows the agent to be aware
    // that a deviation was detected before the topology change.

  // Case 3: Destination agent has left the network entirely
  if dest_agent not in current_topology.all_agents():
    log_discard(signal,
      reason="DESTINATION_AGENT_DEPARTED",
      epoch=signal.epoch,
      source=signal.source,
      target=dest_agent,
      magnitude=signal.magnitude)
    return DROP_WITH_LOGGED_DISCARD
    // The signal is dropped. No retry, no redirect. The log entry
    // enables post-hoc analysis of lost signals during reconfiguration.
```

### F15.2 Cold-Start Surprise Burst for New Parcel Members

When an agent joins a parcel (either via initial registration or parcel reassignment during MIGRATE), it lacks context about the parcel's recent surprise history. A new member making scheduling decisions without knowing that the parcel has been experiencing elevated surprise rates may misinterpret normal-but-elevated behavior as anomalous, or fail to detect genuinely anomalous behavior because its baseline is wrong.

```
function send_cold_start_burst(
  new_agent: AgentId,
  parcel: Parcel,
  signal_aggregator: ParcelSignalAggregator
):

  // The parcel's signal aggregator maintains rolling statistics
  // for the last COLD_START_LOOKBACK (default 3) epochs
  lookback = min(COLD_START_LOOKBACK, parcel.age_epochs)

  burst = ColdStartBurst{
    target: new_agent,
    parcel: parcel.id,
    epoch_range: (current_epoch() - lookback, current_epoch()),
    signal_summaries: []
  }

  for signal_type in active_signal_types(parcel):
    summary = SignalTypeSummary{
      type: signal_type,
      mean_magnitude: signal_aggregator.rolling_mean(
        signal_type, lookback),
      max_magnitude: signal_aggregator.rolling_max(
        signal_type, lookback),
      signal_count: signal_aggregator.rolling_count(
        signal_type, lookback),
      mean_accuracy: signal_aggregator.rolling_mean_accuracy(
        signal_type, lookback)
    }
    burst.signal_summaries.append(summary)

  // Deliver as a single message, max 512 bytes
  // (3 epochs * ~7 signal types * ~18 bytes per summary = ~378 bytes)
  send(new_agent, burst)


function incorporate_cold_start_burst(
  agent: Agent,
  burst: ColdStartBurst
):
  for summary in burst.signal_summaries:
    // Initialize predictive model baselines from the burst
    agent.signal_baseline[summary.type] = SignalBaseline{
      expected_magnitude: summary.mean_magnitude,
      expected_frequency: summary.signal_count / burst.epoch_count(),
      confidence: 0.5    // low confidence — this is secondhand data
    }

  // The agent uses these baselines for COLD_START_LOOKBACK epochs,
  // then transitions to its own observations
  agent.cold_start_expiry = current_epoch() + COLD_START_LOOKBACK
```

**New constant:** `COLD_START_LOOKBACK` — default 3, range [1, 10]. Number of epochs of historical surprise data sent to new parcel members.

### F15.3 Transition Acceptance Window

During reconfiguration, there is an ambiguity period where signals may be addressed to agents at their old parcel location. Rather than requiring instant cutover (which is impossible in an asynchronous network), the system accepts signals addressed to either the old or new parcel boundary for a limited transition period.

```
// Duration: TRANSITION_ACCEPTANCE_EPOCHS (default 2) tidal epochs
// after MIGRATE completes

function is_valid_signal_destination(
  signal: SurpriseSignal,
  agent: AgentId,
  epoch: uint64,
  parcel: Parcel
) -> bool:

  // Normal case: agent is in this parcel
  if agent in parcel.agents:
    return true

  // Transition case: agent WAS in this parcel within the acceptance window
  if parcel.migrate_epoch is not null:
    epochs_since_migrate = epoch - parcel.migrate_epoch
    if epochs_since_migrate <= TRANSITION_ACCEPTANCE_EPOCHS:
      if agent in parcel.pre_migrate_agents:
        // Accept the signal, forward to agent's current parcel
        forward_to_current_parcel(signal, agent)
        return true

  return false
```

**New constant:** `TRANSITION_ACCEPTANCE_EPOCHS` — default 2, range [1, 5]. Number of epochs after MIGRATE during which both old and new parcel boundaries are accepted for signal routing.

**Interaction with PTP STABILIZE convergence:** The transition acceptance window overlaps with the STABILIZE convergence period (2-5 epochs). This is intentional — signals routed via the old boundary during convergence are forwarded to the correct current location, preventing signal loss during the period of highest routing ambiguity.

---

## PA-F16: Threshold Calibration Coupling

**Finding:** The base spec identifies the pathological interaction between PTA surprise thresholds and Noosphere SLV thresholds (Section 6.4, Attack 11) and specifies that surprise rate becomes the 7th SLV dimension. However, it does not define the quantitative relationship between the per-agent `surprise_threshold` and the locus-level `SLV_threshold`. These thresholds are calibrated independently, meaning an operator can set `surprise_threshold = 0.01` (very sensitive, many surprises generated) while `SLV_threshold = 10.0` (very insensitive, SLV never triggers), creating a system that floods parcels with surprise signals but never acts on them at the locus level. Conversely, `surprise_threshold = 1.0` + `SLV_threshold = 0.1` triggers locus-level responses without the surprise signal information needed to diagnose the cause.

**Resolution:** Define a coupling function that maintains a fixed ratio between the two thresholds, with governance-controlled override.

### F16.1 Coupling Function

```
// The SLV threshold is a locus-level aggregate of per-agent surprise.
// Because it aggregates across multiple agents and multiple signal types,
// it should be LESS sensitive than any individual agent's surprise
// threshold. The default ratio is 2x: SLV fires when the aggregate
// surprise is twice the level that would trigger individual surprise
// signals.

SLV_SURPRISE_RATIO = 2.0     // default, range [1.5, 5.0]
                               // configurable constant #48

function compute_slv_threshold(surprise_threshold: float64) -> float64:
  return surprise_threshold * SLV_SURPRISE_RATIO

// The SLV's 7th dimension (surprise rate) threshold:
SLV_surprise_dimension_threshold = compute_slv_threshold(
  mean(threshold_B for all models B in parcel)
)
```

### F16.2 Auto-Adjustment on Governance Change

When `surprise_threshold` is modified via governance (G-class parameter change), the SLV threshold auto-adjusts to maintain the configured ratio:

```
function on_surprise_threshold_change(
  new_surprise_threshold: float64,
  governance_action: GovernanceAction
):
  // Validate the new threshold is within range
  assert THRESHOLD_MIN <= new_surprise_threshold <= THRESHOLD_MAX

  // Auto-adjust SLV surprise dimension threshold
  new_slv_threshold = compute_slv_threshold(new_surprise_threshold)

  // Apply at next epoch boundary (consistent with all parameter changes)
  schedule_parameter_update(
    epoch = next_epoch_boundary(),
    updates = {
      "surprise_threshold_base": new_surprise_threshold,
      "slv_surprise_threshold": new_slv_threshold
    },
    source = governance_action.id
  )

  // Log the coupled change for audit
  log_coupled_threshold_change(
    governance_action = governance_action.id,
    old_surprise = get_current("surprise_threshold_base"),
    new_surprise = new_surprise_threshold,
    old_slv = get_current("slv_surprise_threshold"),
    new_slv = new_slv_threshold,
    ratio = SLV_SURPRISE_RATIO
  )
```

### F16.3 Override Mechanism

The ratio can be decoupled via explicit G-class governance action. This is intentional — there may be legitimate operational reasons to set a non-default ratio (e.g., during a known reconfiguration period, the SLV threshold might be temporarily raised to 3x to avoid false positives).

```
function decouple_slv_threshold(
  explicit_slv_threshold: float64,
  governance_action: GovernanceAction
):
  // This REQUIRES explicit G-class governance — auto-adjustment
  // cannot be silently disabled
  assert governance_action.class == G
  assert governance_action.approved == true

  schedule_parameter_update(
    epoch = next_epoch_boundary(),
    updates = {
      "slv_surprise_threshold": explicit_slv_threshold,
      "slv_threshold_decoupled": true,
      "slv_threshold_decouple_expiry": current_epoch() +
        governance_action.duration_epochs    // MUST have an expiry
    },
    source = governance_action.id
  )

  // After expiry, ratio-coupled behavior automatically resumes
```

### F16.4 Interaction with Adaptive Threshold

The per-agent adaptive threshold (Definition 2.18) operates independently of the coupling function. Each agent's `threshold_B(e)` adapts based on local model accuracy. The SLV threshold tracks the mean of all per-agent thresholds in the parcel, not a single global value:

```
function update_slv_surprise_threshold(parcel: Parcel, epoch: uint64):
  if get_current("slv_threshold_decoupled"):
    if epoch >= get_current("slv_threshold_decouple_expiry"):
      set("slv_threshold_decoupled", false)    // re-engage coupling
    else:
      return    // decoupled, do not auto-adjust

  // Compute mean surprise threshold across all agents in parcel
  agent_thresholds = []
  for agent in parcel.agents:
    for model in agent.models.values():
      agent_thresholds.append(model.threshold)

  mean_threshold = mean(agent_thresholds)

  // Apply ratio
  parcel.slv.dimension_thresholds[SURPRISE_RATE] =
    mean_threshold * SLV_SURPRISE_RATIO
```

**New constants:**
```
// #48: SLV_SURPRISE_RATIO        default: 2.0    range: [1.5, 5.0]
```

---

## PA-F18: AASL Type Retirement

**Finding:** The base spec defines 27 AASL types (23 existing + 4 new in C3) but provides no mechanism for retiring types that are no longer in use. Over time, the type namespace will accumulate dead types — types that no agent sends or processes but that implementations must still recognize (per the forward-compatibility rule: "agents that do not understand new types MUST ignore them"). Without a retirement mechanism, the type system grows monotonically, increasing parser complexity and test surface indefinitely.

**Resolution:** Define a lifecycle for AASL type retirement with governance guardrails.

### F18.1 Type Activity Tracking

```
TypeActivityRecord := {
  type_token:         AASLTypeToken
  last_active_epoch:  uint64       // last epoch where a message of this type
                                    // was sent by any agent in any locus
  inactive_epochs:    uint64       // consecutive epochs with zero messages
  total_messages:     uint64       // lifetime message count
  state:              {ACTIVE, INACTIVE, PROPOSED_RETIREMENT,
                       RETIRED, RESERVED}
}

function update_type_activity(type_token: AASLTypeToken, epoch: uint64):
  record = get_type_activity(type_token)

  messages_this_epoch = count_messages(type_token, epoch, scope=ALL_LOCI)

  if messages_this_epoch > 0:
    record.last_active_epoch = epoch
    record.inactive_epochs = 0
    record.total_messages += messages_this_epoch
    if record.state == INACTIVE:
      record.state = ACTIVE     // reactivated
  else:
    record.inactive_epochs += 1
    if record.inactive_epochs >= TYPE_INACTIVE_THRESHOLD:   // default 100
      record.state = INACTIVE
```

### F18.2 Retirement Protocol

```
function propose_type_retirement(
  type_token: AASLTypeToken,
  proposer: AgentId
) -> RetirementProposal:

  record = get_type_activity(type_token)

  // Precondition: type must be INACTIVE
  assert record.state == INACTIVE,
    "Cannot retire ACTIVE type"

  // Precondition: type must have been inactive for the full threshold
  assert record.inactive_epochs >= TYPE_INACTIVE_THRESHOLD,
    "Type has not been inactive for {} epochs".format(TYPE_INACTIVE_THRESHOLD)

  // Precondition: type must not be a core protocol type
  assert type_token not in CORE_PROTOCOL_TYPES,
    "Core protocol types (CLM, CLS, MCT, SIG, TDF, TSK, SRP, STL) " +
    "cannot be retired"

  return RetirementProposal{
    type_token: type_token,
    proposer: proposer,
    proposed_epoch: current_epoch(),
    vote_class: G,                        // G-class governance
    required_supermajority: 0.75,         // 75% supermajority
    discussion_period: GOVERNANCE_DISCUSSION_PERIOD,
    inactive_since: current_epoch() - record.inactive_epochs,
    total_lifetime_messages: record.total_messages
  }
```

### F18.3 Retirement Execution

```
function execute_type_retirement(
  proposal: RetirementProposal,
  vote_result: GovernanceVoteResult
):
  assert vote_result.approved == true
  assert vote_result.approval_fraction >= 0.75

  record = get_type_activity(proposal.type_token)

  // Final check: type has not been reactivated during voting period
  if record.state != INACTIVE:
    log_retirement_cancelled(proposal, reason="TYPE_REACTIVATED_DURING_VOTE")
    return

  // Retire the type
  record.state = RETIRED

  // The type ID is RESERVED — never reused for a different type
  // This prevents semantic confusion if old messages with the retired
  // type token are encountered in logs or archives
  reserve_type_id(proposal.type_token)

  // Activation: at next epoch boundary
  schedule_retirement_activation(
    epoch = next_epoch_boundary(),
    type_token = proposal.type_token
  )

  log_type_retirement(
    type_token = proposal.type_token,
    retired_epoch = next_epoch_boundary(),
    lifetime_messages = record.total_messages,
    inactive_epochs = record.inactive_epochs,
    governance_ref = vote_result.id
  )
```

### F18.4 Retired Type Behavior

```
function handle_message_with_retired_type(
  message: AASLMessage,
  type_token: AASLTypeToken
) -> IngestionDecision:

  record = get_type_activity(type_token)

  if record.state == RETIRED:
    // Reject at ingestion — do not process, do not forward
    return REJECT(
      reason = "RETIRED_TYPE",
      type_token = type_token,
      retired_epoch = record.retired_epoch,
      message_id = message.id
    )

  // RESERVED types (IDs of previously retired types) are also rejected
  if record.state == RESERVED:
    return REJECT(
      reason = "RESERVED_TYPE_ID",
      type_token = type_token
    )

  return ACCEPT
```

### F18.5 Active Type Cap

```
MAX_ACTIVE_TYPES = 50          // default, configurable constant #49

function register_new_type(type_def: AASLTypeDefinition) -> bool:
  active_count = count_types(state=ACTIVE)

  if active_count >= MAX_ACTIVE_TYPES:
    // Exceeding the cap requires explicit G-class governance approval
    // This prevents unchecked type proliferation
    assert type_def.governance_approval is not null,
      "Active type count ({}) at cap ({}). " +
      "G-class governance approval required to exceed.".format(
        active_count, MAX_ACTIVE_TYPES)
    assert type_def.governance_approval.approved == true
    assert type_def.governance_approval.approval_fraction >= 0.75

  register(type_def)
  return true
```

### F18.6 New Constants

```
// #49: TYPE_INACTIVE_THRESHOLD    default: 100    range: [50, 500]   epochs
// #50: MAX_ACTIVE_TYPES           default: 50     range: [30, 100]
```

### F18.7 Conformance Amendment

Add SHOULD requirement #9 (Section 12.3):

> **SHOULD (#9):** Implement AASL type activity tracking and retirement per Section PA-F18. Implementations that do not implement retirement MUST still reject messages with type tokens marked RETIRED in the canonical type registry.

---

## Errata

### E-C3-01: Extended Claim Class Enum

**Location:** Definition 2.9 (Appendix A), Section 5.1 claim class table

**Change:** Extend the `claim_class` enum from 5 values to 9 values:

```
// BEFORE (base spec Definition 2.9):
claim_class: {deterministic, empirical, statistical, heuristic, normative}

// AFTER:
claim_class: {
  deterministic,              // Recomputation-verifiable (math proofs, algo outputs)
  empirical,                  // Replication + cross-reference (experiments, observations)
  statistical,                // Distribution analysis + methodology audit
  heuristic,                  // Contestable Reliance Membrane (model predictions)
  normative,                  // Governance review + constitutional compliance
  process,                    // [NEW] Procedural correctness claims (C9)
  reasoning,                  // [NEW] Logical inference chain claims (C9)
  compliance,                 // [NEW] Regulatory/policy adherence claims (C9)
  knowledge_consolidation     // [NEW] Synthesis of existing verified claims (C9)
}
```

**Rationale:** C9 canonical hierarchy identifies four additional claim classes required for full-spectrum epistemic coordination. Process claims verify that a procedure was followed correctly (e.g., "this audit followed the 7-step protocol"). Reasoning claims verify logical inference chains (e.g., "given premises A, B, C, conclusion D follows"). Compliance claims verify adherence to external rules or internal policy. Knowledge consolidation claims verify that a synthesis accurately represents its source claims.

**Impact:** The Section 5.1 claim class table gains four rows. The `classify_claim()` function (Section 3.2) is unchanged — the new classes affect verification pathways (V-class), not operation classification.

### E-C3-02: Verification Pathways for P/R/C/K Classes

**Location:** Section 5.1, claim class table

**Addition:** Append to the claim class table:

| Claim Class | Verification Pathway | Example |
|---|---|---|
| Process | Procedure trace audit + step-completeness check | "Verification followed the 5-step membrane protocol" |
| Reasoning | Logical inference validation + premise verification | "From axioms A1-A3, theorem T follows by modus ponens" |
| Compliance | Rule-set matching + exception enumeration | "This settlement computation satisfies AIC conservation law" |
| Knowledge Consolidation | Source claim cross-reference + coverage audit + contradiction check | "Claims C1-C7 collectively establish finding F" |

**Verification depth by class:**

```
// Process claims: verify that each step in the declared procedure
// was executed, in order, with the declared inputs and outputs.
// Committee size: same as deterministic (recomputation-like).
function verify_process_claim(claim: Claim, committee: Set<AgentId>):
  trace = claim.evidence[0]    // procedure execution trace
  procedure = resolve_procedure(claim.body.procedure_ref)
  for step in procedure.steps:
    assert step.id in trace.executed_steps,
      "Step {} not found in execution trace".format(step.id)
    assert trace.step_order(step.id) == step.sequence,
      "Step {} executed out of order".format(step.id)
    assert trace.step_inputs(step.id) conform_to step.input_schema
    assert trace.step_outputs(step.id) conform_to step.output_schema
  return VERIFIED

// Reasoning claims: verify logical validity of the inference chain.
// Premises must themselves be verified claims in the knowledge graph.
function verify_reasoning_claim(claim: Claim, committee: Set<AgentId>):
  chain = claim.evidence[0]    // inference chain
  for premise in chain.premises:
    assert is_verified_claim(premise.claim_ref),
      "Premise {} is not a verified claim".format(premise.claim_ref)
  for step in chain.inference_steps:
    assert step.rule in VALID_INFERENCE_RULES,
      "Inference rule {} not recognized".format(step.rule)
    assert step.conclusion follows_from (step.premises, step.rule),
      "Inference step {} is invalid".format(step.id)
  return VERIFIED

// Compliance claims: verify against a declared rule set.
function verify_compliance_claim(claim: Claim, committee: Set<AgentId>):
  rule_set = resolve_rule_set(claim.body.rule_set_ref)
  subject = claim.body.subject_ref
  for rule in rule_set.rules:
    result = evaluate_rule(rule, subject)
    if not result.satisfied:
      // Check if a declared exception applies
      if result.exception in claim.body.declared_exceptions:
        continue    // exception acknowledged
      return REJECTED("Rule {} violated without declared exception".format(rule.id))
  return VERIFIED

// Knowledge consolidation claims: verify that synthesis is
// faithful to source claims.
function verify_consolidation_claim(claim: Claim, committee: Set<AgentId>):
  source_claims = [resolve_claim(ref) for ref in claim.evidence]
  synthesis = claim.body

  // 1. All source claims must be verified
  for sc in source_claims:
    assert is_verified_claim(sc.id),
      "Source claim {} is not verified".format(sc.id)

  // 2. Coverage: synthesis must reference all source claims
  referenced = extract_claim_references(synthesis)
  unreferenced = {sc.id for sc in source_claims} - referenced
  assert |unreferenced| == 0,
    "Synthesis does not reference source claims: {}".format(unreferenced)

  // 3. Contradiction check: no source claims contradict each other
  for (a, b) in pairs(source_claims):
    assert not contradicts(a, b),
      "Source claims {} and {} contradict".format(a.id, b.id)

  return VERIFIED
```

### E-C3-03: Epoch Duration Cross-Specification Alignment

**Location:** Section 4.3 (Epoch Management), Appendix B (#4)

**Addition:** Append the following note after the EPOCH_DURATION definition in Section 4.3:

> **Cross-specification note:** C3's `EPOCH_DURATION` (default 3600s) is equivalent to `TIDAL_EPOCH` in the C9 canonical time hierarchy. The relationship to C8's Settlement Plane is: `1 TIDAL_EPOCH = 60 SETTLEMENT_TICKs` (where each SETTLEMENT_TICK = 60s in C8's default configuration). Implementations integrating C3 with C8/C9 MUST maintain this ratio: `EPOCH_DURATION = SETTLEMENT_TICK_DURATION * TICKS_PER_TIDAL_EPOCH`. If EPOCH_DURATION is modified via governance, SETTLEMENT_TICK_DURATION adjusts proportionally to maintain the 60:1 ratio, unless explicitly decoupled by G-class governance action with documented rationale.

```
// Cross-spec time hierarchy:
//   C8 SETTLEMENT_TICK   =  60s  (base unit)
//   C3 TIDAL_EPOCH       = 3600s = 60 SETTLEMENT_TICKs
//   C9 TIDAL_EPOCH       = 3600s (same as C3, by definition)
//
// Coupling invariant:
//   EPOCH_DURATION == SETTLEMENT_TICK_DURATION * TICKS_PER_TIDAL_EPOCH
//   where TICKS_PER_TIDAL_EPOCH = 60 (default)

TICKS_PER_TIDAL_EPOCH = 60    // configurable constant #51, range [10, 120]
```

---

## Summary of New Configurable Constants

| # | Parameter | Default | Range | Source |
|---|-----------|---------|-------|--------|
| 42 | VRF_PHASE2_THRESHOLD | 100 | [50, 500] | PA-F4 |
| 43 | VRF_PHASE3_THRESHOLD | 1000 | [500, 5000] | PA-F4 |
| 44 | VRF_HYSTERESIS_BAND | 10 | [5, 50] | PA-F4 |
| 45 | VRF_PHASE2_SUSTAIN | 3 | [1, 10] epochs | PA-F4 |
| 46 | VRF_PHASE3_SUSTAIN | 5 | [2, 15] epochs | PA-F4 |
| 47 | COLD_START_LOOKBACK | 3 | [1, 10] epochs | PA-F15 |
| 48 | SLV_SURPRISE_RATIO | 2.0 | [1.5, 5.0] | PA-F16 |
| 49 | TYPE_INACTIVE_THRESHOLD | 100 | [50, 500] epochs | PA-F18 |
| 50 | MAX_ACTIVE_TYPES | 50 | [30, 100] | PA-F18 |
| 51 | TICKS_PER_TIDAL_EPOCH | 60 | [10, 120] | E-C3-03 |
| 52 | TRANSITION_ACCEPTANCE_EPOCHS | 2 | [1, 5] epochs | PA-F15 |
| 53 | SELECTION_OVERSAMPLING | 2.0 | [1.5, 4.0] | PA-F4 |

## Summary of Conformance Amendments

| Requirement | Change | Source |
|---|---|---|
| MUST #3 (revised) | VRF phase must match agent count per PA-F4 | PA-F4 |
| MUST #10 (revised) | Diversity cooling only in COMMITTED and FULL_DUAL_DEFENSE phases | PA-F4 |
| SHOULD #8 (new) | Provide T1/T2/T3 deployment profiles | PA-F6 |
| SHOULD #9 (new) | Implement AASL type retirement; MUST reject RETIRED types | PA-F18 |

## Summary of Definition Amendments

| Definition | Change | Source |
|---|---|---|
| 2.9 (Claim) | claim_class enum extended with process, reasoning, compliance, knowledge_consolidation | E-C3-01 |
| New: VRFPhase | enum {SIMPLE, COMMITTED, FULL_DUAL_DEFENSE} | PA-F4 |
| New: TypeActivityRecord | Type lifecycle tracking structure | PA-F18 |
| New: ColdStartBurst | Signal history summary for new parcel members | PA-F15 |

---

*End of Patch Addendum PA-C3-01*

*This addendum supplements MASTER_TECH_SPEC.md v1.0 (C3-A). All pseudocode uses the same conventions as the base spec (Python-like syntax, explicit type annotations, RFC 2119 keywords). Constants numbered #42-#53 extend Appendix B. New definitions extend Appendix A.*
