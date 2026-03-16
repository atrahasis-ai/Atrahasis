# C34 — Black-Start Recovery Fabric: Pre-Mortem Analysis

**Invention:** C34 — Black-Start Recovery Fabric with Adversarial State Reconstruction
**Stage:** DESIGN
**Role:** Pre-Mortem Analyst (PRIMARY tier)
**Date:** 2026-03-11
**Scenario:** C34 has failed catastrophically 5 years after deployment. Work backward.

---

## Executive Summary

This analysis identifies 31 failure scenarios across five categories. The most dangerous failures are not in the recovery protocol itself — they are in the operational and integration seams where C34 touches every other layer simultaneously. The design is technically sound for the failures it anticipates, but has significant exposure to scenarios it does not model: predicate drift, partial-layer failures, recovery-triggered cascades, and attacks that exploit the recovery window itself.

The three highest-risk scenarios are:
1. **Synchronization predicate drift** (T-03) — the 21 predicates silently desynchronize from evolving C9 contracts, causing recovery to either false-pass or deadlock.
2. **Recovery-window attack** (A-01) — an adversary triggers a real or simulated multi-layer failure specifically to exploit the degraded state during recovery.
3. **Part III absence during coordinated attack** (I-05) — the Wave 4+ deferral creates a multi-year window where coordinated corruption forces full snapshot restore with massive data loss.

---

## Category 1: Technical Failure Modes

### T-01: Consistent-Cut Search Exhaustion
- **Likelihood:** MEDIUM
- **Severity:** HIGH
- **Root Cause:** The consistent-cut algorithm (SS2.2.3) searches backward tick-by-tick through MAX_CONSISTENT_CUT_SEARCH_WINDOW (default 600 ticks = 10 hours). Under sustained cross-layer inconsistency — even minor transient disagreements accumulating over time — every candidate tick may show at least one consumer-producer digest mismatch. The algorithm returns FAILED, and recovery cannot proceed.
- **Current Design Addresses:** PARTIALLY. The algorithm falls through to "use oldest available digests" (SS4.2, DETECTING->BOOTING guard), but this fallback path is underspecified. What consistent-cut is used when none is found? The design says "oldest available" but does not define how to handle the fact that those digests are also likely inconsistent.
- **Recommendation:** Specify a "best-effort cut" selection — the tick with the fewest inconsistencies — as a fallback before full snapshot restore.

### T-02: C6 Coherence Graph Merkle Root Divergence Under Concurrent Shard Updates
- **Likelihood:** MEDIUM
- **Severity:** MEDIUM
- **Root Cause:** C6's digest uses an incrementally maintained Merkle root over sharded coherence graph (SS3.2.5). During high-throughput periods, concurrent shard updates may produce non-deterministic ordering of Merkle leaf insertions across replicas. Two C6 replicas could compute different coherence_graph_hash values for the same logical state at the same tick, causing permanent consumer-side digest mismatches.
- **Current Design Addresses:** NO. The digest computation assumes the Merkle root is deterministic. The architecture specifies "sorted by shard ID" for global root computation, but does not address intra-shard leaf ordering.
- **Recommendation:** Require canonical leaf ordering within each shard (e.g., by quantum ID), and specify that digest computation is atomic with respect to shard mutations within a tick.

### T-03: Synchronization Predicate Drift
- **Likelihood:** HIGH
- **Severity:** HIGH
- **Root Cause:** The 21 synchronization predicates are derived from the C9 contract matrix at design time (SS2.2.2). The extensibility rule says new C9 contracts "automatically generate new predicates," but this generation is described as a RULE, not an implementation. In practice, predicate maintenance is a manual process that requires someone to notice a new C9 contract was added, derive the predicate, implement the check function, and deploy it to all layers. Over 5 years of evolution, predicates will silently fall out of sync with the actual C9 contract set.
- **Failure mode 1 (false pass):** A new C9 dependency exists but no predicate checks it. Recovery succeeds but layers are actually inconsistent on the unchecked dimension.
- **Failure mode 2 (deadlock):** An old predicate references a C9 contract that was deprecated or restructured. The predicate fails with UNVERIFIABLE on every recovery attempt, blocking the boot sequence.
- **Current Design Addresses:** PARTIALLY. The extensibility rule (SS2.2.2) describes the intent but not the enforcement mechanism. INV-R4 (Predicate Exhaustiveness) states the invariant but provides no runtime verification.
- **Recommendation:** Add a compile-time or startup-time exhaustiveness check that enumerates C9 contracts and verifies each has a corresponding predicate. Add a version stamp linking predicates to C9 revision.

### T-04: VTD Hash Chain Replay Divergence
- **Likelihood:** LOW
- **Severity:** HIGH
- **Root Cause:** C5 recovery replays VTD chain entries from snapshot (SS2.6.3). The replay function calls `state.apply_vtd_credibility_update(entry)`. If the credibility update function's behavior has changed between the snapshot epoch and the recovery epoch (due to parameter updates, C11 CACT evolution, or C12 AVAP rule changes), replay produces different credibility state than the original computation. The post-replay digest will not match the expected digest, and recovery will report INCONSISTENT even though the state is logically correct.
- **Current Design Addresses:** NO. The replay procedure assumes credibility update logic is immutable across epochs.
- **Recommendation:** Version-stamp the credibility update logic and store the version in each C5OpinionSnapshot. Replay must use the logic version that was active when the VTDs were originally processed.

### T-05: Recovery Saga WAL Corruption During C7 Failure
- **Likelihood:** LOW
- **Severity:** HIGH
- **Root Cause:** The Recovery Coordinator is a C7 saga persisted via C7's WAL (SS2.3.2). But C34 recovery is triggered by multi-layer failure. If C7 is one of the failed layers, the WAL that stores the saga state may itself be corrupted. The design acknowledges C7 failover (active->passive LD) but does not address the case where both active and passive LDs have corrupted WALs — which is exactly the kind of correlated failure that triggers C34 in the first place.
- **Current Design Addresses:** PARTIALLY. SS2.3.2(4) says if C7 enters Emergency Bypass, the saga is "frozen" and pre-C7 layers self-coordinate. But the saga cannot resume from a corrupted WAL. There is no mechanism to reconstruct the saga state itself.
- **Recommendation:** Persist a minimal saga state summary in C8's HDL (which boots first and has the highest redundancy) as a backup coordination record.

### T-06: Digest History Tree Wrap-Around Collision
- **Likelihood:** LOW
- **Severity:** MEDIUM
- **Root Cause:** DigestHistoryTree uses a CircularBuffer indexed by `tick % DIGEST_RETENTION_TICKS` (SS2.1.2). If DIGEST_RETENTION_TICKS is reduced via governance parameter change while old entries still exist, the modular index wraps around and overwrites entries that are still within the logical retention window. Recovery could then reference a digest that has been overwritten by a newer tick's digest.
- **Current Design Addresses:** NO. The parameter range allows governance to reduce DIGEST_RETENTION_TICKS from 36000 down to 3600 (10x reduction), but no migration protocol is specified.
- **Recommendation:** Add a migration protocol for DIGEST_RETENTION_TICKS changes: new size takes effect only at the next CONSOLIDATION_CYCLE boundary, and old entries are pruned explicitly rather than implicitly overwritten.

### T-07: Temporal Trust Gradient Exploitation via Age Inflation
- **Likelihood:** LOW
- **Severity:** MEDIUM
- **Root Cause:** The temporal trust gradient assigns higher weight to older, unchallenged digests (SS2.1.5). An adversary who corrupts a digest and then ensures no consumer challenges it for a long period (by also corrupting consumer records or by corrupting a low-traffic layer pair) can artificially inflate the trust weight of a corrupted digest. During recovery, the consistent-cut algorithm "preferentially selects digest sets with higher aggregate temporal trust weight," meaning it will prefer the corrupted old digest over a correct recent one.
- **Current Design Addresses:** PARTIALLY. The temporal trust gradient is a heuristic, and witness verification (Part II) should catch the corruption. But if the adversary also controls the consumer-side record, witness verification will show CONSISTENT for the corrupted pair.
- **Recommendation:** Cross-reference temporal trust with witness corroboration from non-adjacent layers. A digest should not receive elevated trust if it has never been independently verified by a layer that is not its direct consumer.

---

## Category 2: Operational Failure Modes

### O-01: 21-Predicate Maintenance Burden
- **Likelihood:** HIGH
- **Severity:** MEDIUM
- **Root Cause:** 21 synchronization predicates (24 with defense system predicates) must be kept correct, tested, and updated in lockstep with every change to C9 contracts or to any layer's state schema. Each predicate is a function `fn(SourceState, ConsumerDigest) -> PredicateResult` that must be implemented in every layer that uses it. Over 5 years, predicate rot is virtually certain: changes to a layer's internal state representation break predicates that reference fields by name, and the break is not detected until the next actual recovery event.
- **Current Design Addresses:** NO. There is no predicate testing framework, no integration test suite, and no runtime health check that validates predicates are still functional.
- **Recommendation:** Require periodic (e.g., monthly) simulated recovery exercises that execute all predicates against synthetic state. Alert if any predicate returns UNVERIFIABLE.

### O-02: Recovery Has Never Been Tested in Production
- **Likelihood:** HIGH
- **Severity:** HIGH
- **Root Cause:** C34's recovery components are dormant during normal operation (design principle #3). If no multi-layer failure occurs for years, the recovery path is entirely untested in production conditions. Bit rot in dormant code is a well-documented phenomenon. When a real multi-layer failure finally occurs, the recovery path discovers bugs that were introduced by layer evolution but never caught because recovery was never exercised.
- **Current Design Addresses:** NO. The design specifies no chaos engineering, no planned recovery drills, no canary recovery tests.
- **Recommendation:** Mandate periodic recovery drills (at minimum in staging environments, ideally controlled drills in production with limited blast radius). C22 implementation planning should include recovery drill cadence.

### O-03: C5 Opinion Snapshot Storage Growth
- **Likelihood:** MEDIUM
- **Severity:** LOW
- **Root Cause:** C5 opinion snapshots are ~10 MB per snapshot at 10,000 agents (SS2.6.2). At 100,000 agents (plausible at 5-year scale), snapshots grow to ~100 MB each. With SNAPSHOT_RETENTION_EPOCHS=10, that is 1 GB of snapshot storage per C5 node. With 100 retained (max governance range), it reaches 10 GB. Not catastrophic, but creates operational pressure to reduce retention, which reduces recovery depth.
- **Current Design Addresses:** PARTIALLY. The parameter range allows governance to manage retention. But the tension between storage cost and recovery depth is not explicitly analyzed.
- **Recommendation:** Add snapshot compression or delta-encoded snapshots. Store only full snapshots at wider intervals (e.g., every 10 TIDAL_EPOCHS) with deltas in between.

### O-04: Parameter Misconfiguration Cascade
- **Likelihood:** MEDIUM
- **Severity:** HIGH
- **Root Cause:** C34 has 19 configurable parameters (SS5) across 5 categories. Many interact non-obviously. Example: if FAILURE_DETECTION_WINDOW is set too low (2 ticks = 2 minutes) while SELF_COORD_TIMEOUT is set high (60 ticks = 60 minutes), the system triggers recovery faster than layers can self-coordinate, causing every recovery to timeout. Another example: RECOVERY_SAGA_TIMEOUT (600 ticks = 10 hours) may be shorter than the actual time needed to replay a large C5 VTD chain if the chain has grown to millions of entries.
- **Current Design Addresses:** NO. Parameters are specified with ranges but no constraint relationships between them.
- **Recommendation:** Define parameter constraint invariants (e.g., RECOVERY_SAGA_TIMEOUT > SELF_COORD_TIMEOUT * len(BOOT_ORDER)). Validate constraints at configuration time.

### O-05: Governance Escalation Black Hole
- **Likelihood:** MEDIUM
- **Severity:** HIGH
- **Root Cause:** Multiple failure paths terminate with "escalate to governance" (SS2.3.1 FAILED state, SS2.3.3 self-coordination HALT, SS2.4.3 authority override with no multiply-attested snapshot). But C34 does not specify what governance does, how fast it responds, or what the system state is while waiting. If governance is slow (days/weeks for a committee decision), the system is in FAILED recovery state with multiple layers degraded. No automated fallback is specified for the case where governance does not respond within a reasonable time.
- **Current Design Addresses:** NO. Governance escalation is treated as a terminal state with no further specification.
- **Recommendation:** Define automated degraded-operation modes for the case where governance has not responded within N ticks. At minimum, allow per-layer independent recovery to proceed even if cross-layer recovery has failed.

---

## Category 3: Market/Adoption Failure Modes

### M-01: Recovery Infrastructure Perceived as Unnecessary Until It Is Not
- **Likelihood:** HIGH
- **Severity:** MEDIUM
- **Root Cause:** C34 is pure infrastructure with zero visible value during normal operation. The always-on cost (0.007%) is negligible, but the implementation cost (every layer must implement C34LayerInterface, maintain digest computation, store consumer logs) is substantial. If the AAS never experiences a multi-layer failure in its first 3 years, there will be persistent pressure to deprioritize C34 maintenance, skip recovery drills, and defer Part III implementation indefinitely.
- **Current Design Addresses:** NO. This is a human/organizational risk, not a technical one, but it directly affects C34's operational readiness.
- **Recommendation:** Frame C34's always-on digest computation as a system health monitoring tool (not just recovery infrastructure). Publish digest consistency metrics as an operational dashboard. This creates ongoing visible value.

### M-02: Part III Never Implemented
- **Likelihood:** HIGH
- **Severity:** MEDIUM
- **Root Cause:** Part III (Adversarial Reconstruction) is deferred to Wave 4+. The API contracts are forward-compatible (no-ops in Wave 2), but the actual reconstruction logic — causal traversal, triple-criteria termination, LayerReconstructionProvider implementations — requires significant development effort. If Wave 4 is deprioritized or if the AAS never reaches Wave 4 scale, Part III remains a specification without implementation. The system's adversarial resilience stays at the "full snapshot restore" level indefinitely.
- **Current Design Addresses:** YES, explicitly. The design acknowledges this risk (MF-2) and specifies the degraded-mode path. But acknowledging a risk is not the same as mitigating it.
- **Recommendation:** Identify a minimal Part III subset (e.g., reconstruction for C8 only, which has ~90% coverage) that could be implemented in Wave 2 or 3 as a proof-of-concept and incremental value delivery.

### M-03: External Auditors Cannot Verify Recovery Correctness
- **Likelihood:** MEDIUM
- **Severity:** LOW
- **Root Cause:** The RecoveryCompletionAttestation (SS2.4.4) is signed by all five layers, but verification requires access to all five layers' Merkle trees, digest histories, and consumer logs. An external auditor (regulator, partner, academic reviewer) cannot independently verify that a recovery was correct without deep access to internal state. This limits C34's value as a trust mechanism.
- **Current Design Addresses:** NO. Attestations are self-referential (signed by the same system that recovered).
- **Recommendation:** Publish attestation hashes to an external append-only log (or blockchain) so external parties can at least verify temporal ordering and non-repudiation, even if they cannot verify content.

---

## Category 4: Adversarial Failure Modes

### A-01: Recovery-Window Attack (Highest Priority Adversarial Scenario)
- **Likelihood:** MEDIUM
- **Severity:** HIGH
- **Root Cause:** C34 recovery takes between 5 minutes (C8 ROSC) and 3+ hours (C6 ROSC). During this window, the system is in a degraded state: layers are booting sequentially, witness verification has not completed, and the Recovery Coordinator saga may not yet be active (pre-C7 phases). An adversary who can trigger or simulate a multi-layer failure can then exploit the recovery window to: (a) inject corrupted state during layer boot before witness verification catches it; (b) manipulate the pre-C7 self-coordination protocol (UDP multicast is unauthenticated at the network layer); (c) submit transactions to layers that have booted but not yet been verified, creating "post-recovery" state that is accepted as legitimate.
- **Current Design Addresses:** PARTIALLY. LayerReadyAnnouncement messages are signed with Ed25519 (SS2.3.3), which prevents impersonation. But the design does not specify whether layers accept new operations during recovery or only after attestation is complete.
- **Recommendation:** Specify that all layers operate in read-only mode (no new state mutations except recovery operations) from DETECTING until VERIFIED->NORMAL transition. This is the equivalent of a system-wide SAFE_MODE during recovery.

### A-02: Consumer-Side Digest Poisoning
- **Likelihood:** LOW
- **Severity:** HIGH
- **Root Cause:** Consumer-side audit trails (SS2.1.4) are the foundation of witness verification. If an adversary compromises a consumer layer's storage, they can retroactively modify consumer-side digests to match a corrupted producer's state. When witness verification runs, the corrupted consumer record agrees with the corrupted producer, showing CONSISTENT. The corroboration assessment then sees this as corroborating evidence.
- **Current Design Addresses:** PARTIALLY. Digests are signed by the producing layer (Ed25519), so a consumer cannot forge a digest. But the consumer controls the `received_at` timestamp and the `verified` flag, and — critically — the consumer controls which digests it stores and which it "loses." A consumer that selectively drops digests for certain ticks can force UNVERIFIABLE results for those ticks, steering the consistent-cut algorithm toward a tick where the adversary has planted consistent-but-corrupted digests.
- **Recommendation:** Add a cross-consumer consistency check: if consumer C_a has digest D for producer P at tick T, but consumer C_b does not, and both C_a and C_b should have received it (per the dependency map), flag the missing digest as suspicious.

### A-03: Authority-Override Quorum Manipulation
- **Likelihood:** LOW
- **Severity:** HIGH
- **Root Cause:** The authority-override quorum for C8 and C3 requires unanimity of consumers (2/2) to flag (SS2.4.2). But C8 has only 2 consumers (C5, C3). If an adversary compromises one of them, the adversary can (a) prevent a legitimate C8 flag by keeping one consumer "consistent," or (b) force a false C8 flag by corrupting one consumer and manipulating the other. The small quorum size makes C8 authority override either too hard to trigger (both consumers must disagree) or too easy to manipulate (only 2 votes needed).
- **Current Design Addresses:** YES, intentionally. The design notes "C8 is settlement authority — high bar to override" as the rationale. This is a conscious trade-off: settlement integrity is valued over recovery flexibility. But the consequence is that a subtle C8 corruption that only one consumer detects will never trigger an override.
- **Recommendation:** Accept as designed trade-off, but add a governance notification when a single consumer disagrees with C8 (even if unanimity is not reached). This creates a manual investigation trigger for the case where one consumer is right and the other is compromised.

### A-04: Digest Computation Timing Side-Channel
- **Likelihood:** LOW
- **Severity:** LOW
- **Root Cause:** Each layer's digest computation has a 4ms budget (INV-R7). An adversary observing digest computation timing can infer information about layer state (e.g., C6's coherence graph size from the time taken to compute its Merkle root). This is a minor information leak, not a direct attack vector.
- **Current Design Addresses:** NO, but severity is low.
- **Recommendation:** Note as residual risk. If constant-time digest computation is needed, it can be added as a hardening measure.

### A-05: Fake Multi-Layer Failure Injection
- **Likelihood:** MEDIUM
- **Severity:** MEDIUM
- **Root Cause:** C34 triggers when ">=2 layers report DEGRADED or UNREACHABLE within FAILURE_DETECTION_WINDOW" (SS4.2). The design does not specify who detects layer failure or how. If the detection mechanism relies on health checks that can be spoofed (e.g., by blocking health-check traffic between specific layers), an adversary can trigger C34 recovery unnecessarily. Each unnecessary recovery incurs downtime (minutes to hours) and creates attack windows (see A-01).
- **Current Design Addresses:** NO. The failure detection mechanism is not specified — it is assumed to be an existing capability of the layers.
- **Recommendation:** Require corroborated failure detection: a layer is considered DEGRADED only if N independent monitors agree. Define the failure detection interface as part of C34's specification, not as an external assumption.

### A-06: Reconstruction Engine as Oracle
- **Likelihood:** LOW
- **Severity:** MEDIUM
- **Root Cause:** Part III's causal traversal algorithm (SS2.5.2) follows cross-layer references from corrupted entities outward through surviving layers. An adversary who knows the reference registry (it is declarative and static) can predict exactly which entities will be queried during reconstruction and pre-corrupt them. The reference registry is effectively a roadmap for a targeted multi-layer corruption attack.
- **Current Design Addresses:** NO. The reference registry is specified as a static declarative structure. Its contents are visible to anyone with access to the C34 specification.
- **Recommendation:** Add randomization to traversal order (not just following references deterministically). Consider making the reference registry partially dynamic (e.g., including runtime-discovered references alongside declared ones).

---

## Category 5: Integration Failure Modes

### I-01: C3 CRDT Replication Failure Blocks Digest Distribution
- **Likelihood:** MEDIUM
- **Severity:** HIGH
- **Root Cause:** Digest broadcasting piggybacks on C3's CRDT replication (SS2.1.3, "no new network protocol"). If C3's CRDT replication fails or degrades (network partition, C3 in SAFE_MODE, CRDT convergence delays), digest distribution stops. Consumer-side logs stop receiving updates. Over time, the gap between last-received consumer digest and current tick grows. When recovery is needed, consumer logs are stale and consistent-cut computation fails.
- **Current Design Addresses:** PARTIALLY. The pre-C7 self-coordination protocol (SS2.3.3) lists "direct peer-to-peer UDP multicast" as a fallback for C3 unavailability. But this fallback is only specified for recovery-time LayerReadyAnnouncement messages, not for normal-operation digest distribution.
- **Recommendation:** Specify a fallback digest distribution mechanism for normal operation (not just recovery). Even a simple periodic direct exchange between layer pairs would prevent consumer-log staleness during C3 degradation.

### I-02: C9 Contract Evolution Breaks INV-R4
- **Likelihood:** HIGH
- **Severity:** HIGH
- **Root Cause:** INV-R4 (Predicate Exhaustiveness) requires that every C9 contract has a corresponding predicate. But C9 is a living document that will evolve over 5 years. New inventions (C33+) may add new cross-layer contracts. Existing contracts may be restructured. The predicate-to-contract traceability matrix (Appendix A) becomes outdated. This is the same failure as T-03 but viewed from the integration perspective: the dependency is on C9 stability, which is not guaranteed.
- **Current Design Addresses:** PARTIALLY (extensibility rule in SS2.2.2). But the rule is descriptive, not enforced.
- **Recommendation:** Add a C9 revision field to the C34 parameter set. At system startup, C34 verifies that its predicate set matches the declared C9 revision. Mismatch triggers a WARNING that blocks recovery (but not normal operation).

### I-03: C7 Emergency Bypass Leaves Recovery Orphaned
- **Likelihood:** LOW
- **Severity:** HIGH
- **Root Cause:** If C7 enters Emergency Bypass (both active and passive LD unavailable), the recovery saga is frozen (SS2.3.2(4)). Pre-C7 layers continue self-coordinating. But C6 (which boots after C7) cannot boot at all — it requires C7 coordination. The system is stuck: C8, C5, C3 are recovered but C7 and C6 are not. The system is in a partial recovery state with no coordinator to advance it. LIVE-5 (Progressive Recovery) says per-layer recovery is "always available as a fallback," but C6 cannot perform per-layer recovery without C7 for knowledge projections.
- **Current Design Addresses:** PARTIALLY. LIVE-5 asserts per-layer fallback but does not verify it for all layers. C6's per-layer recovery (opinion freeze, queue drain, quarantine) does not require C7 — but the C34 boot order makes C6 wait for C7 regardless.
- **Recommendation:** Specify a degraded C6 recovery path that can proceed without C7 coordination, accepting reduced recovery quality (e.g., skip knowledge projection verification, accept C6 at whatever state it can self-recover to).

### I-04: C31 (CAT) Optional Inclusion Creates Untested Path
- **Likelihood:** MEDIUM
- **Severity:** MEDIUM
- **Root Cause:** C34 optionally includes C31 when DAN_ENABLED=true (SS1.1). The defense system predicates (PRED_C11_CACT, PRED_C12_AVAP, PRED_C13_CRP) are conditional. This creates 2^4 = 16 possible predicate configurations (each of C11, C12, C13, C31 enabled or disabled). In practice, only 1-2 configurations will be tested. The remaining configurations may have predicate interactions that cause recovery to fail in untested ways.
- **Current Design Addresses:** NO. The conditional predicates are specified but the combinatorial testing burden is not acknowledged.
- **Recommendation:** Restrict supported configurations to a small set (e.g., "all defense systems off" and "all defense systems on") and reject intermediate configurations at startup. Alternatively, test all 16 combinations as part of recovery drill validation.

### I-05: Part III Absence During Pre-Wave-4 Coordinated Attack
- **Likelihood:** MEDIUM
- **Severity:** HIGH
- **Root Cause:** Part III is deferred to Wave 4+ (SS2.5). Before Wave 4, any unrecoverable state corruption forces full snapshot restore (SS2.4.3 degraded-mode path). A full snapshot restore loses all state between the snapshot and the failure — potentially hours or days of AIC transactions, verification results, knowledge consolidation, and intent orchestration. A coordinated adversary who knows Part III is not implemented can deliberately corrupt state in a way that passes witness verification (by also corrupting consumer records — see A-02) and then trigger a situation where the corruption is discovered too late. The system must snapshot-restore, losing significant operational state.
- **Current Design Addresses:** YES, explicitly acknowledged as MF-2 residual risk. The design accepts this trade-off.
- **Recommendation:** Accelerate a minimal Part III implementation for the highest-value layer (C8, ~90% reconstruction coverage). Even partial adversarial reconstruction for settlement state significantly reduces the blast radius of a pre-Wave-4 attack.

### I-06: HDL Gossip Fallback (Pre-C7/Pre-C3) Is Underspecified
- **Likelihood:** LOW
- **Severity:** MEDIUM
- **Root Cause:** Pre-C7 self-coordination lists three communication channels in priority order: C3 CRDT broadcast, direct peer-to-peer UDP multicast, HDL gossip (SS2.3.3). But C8 boots first (before C3), so C3 CRDT is unavailable. The actual communication path for C8's LayerReadyAnnouncement is either UDP multicast or HDL gossip. Neither is specified with enough detail: what multicast group? What serialization? What happens if UDP multicast is blocked by network policy? HDL gossip is described as "C8 can piggyback on HDL node communication" but the HDL gossip protocol is a C8 internal mechanism — C5 and C3 may not be HDL participants.
- **Current Design Addresses:** NO. The fallback channels are listed but not specified to implementation level.
- **Recommendation:** Fully specify the pre-C7 communication protocol, including message format, transport, retry semantics, and what happens when all channels fail.

### I-07: Circular Dependency Between C34 Recovery and C3 SAFE_MODE
- **Likelihood:** LOW
- **Severity:** MEDIUM
- **Root Cause:** C34 notes that its state machine is "orthogonal" to C3's SAFE_MODE (SS4.1). But if C3 is in SAFE_MODE when C34 recovery starts, C3's recovery (Step 3) may complete but C3 remains in SAFE_MODE. SAFE_MODE exit requires a "Standard ETR governance vote" (per C3 spec). Meanwhile, C34 expects C3 to emit C3_READY. Can C3 be both READY (for C34 purposes) and in SAFE_MODE (for C3 purposes)? If yes, the system resumes with C3 in a degraded scheduling state. If no, recovery blocks on governance — creating the same governance escalation black hole as O-05.
- **Current Design Addresses:** PARTIALLY. SS4.1 acknowledges the orthogonality but does not specify the interaction rules.
- **Recommendation:** Explicitly define: C3_READY in C34 context means "C3 has recovered its state and satisfies synchronization predicates," independent of SAFE_MODE status. C34 recovery succeeds even if C3 remains in SAFE_MODE. Document this as acceptable degraded operation.

---

## Ranked Summary Table

| Rank | ID | Scenario | Likelihood | Severity | Addressed? |
|------|-----|----------|-----------|----------|-----------|
| 1 | T-03 | Synchronization predicate drift | HIGH | HIGH | PARTIALLY |
| 2 | A-01 | Recovery-window attack | MEDIUM | HIGH | PARTIALLY |
| 3 | I-05 | Part III absence during coordinated attack | MEDIUM | HIGH | YES (accepted risk) |
| 4 | O-02 | Recovery never tested in production | HIGH | HIGH | NO |
| 5 | I-02 | C9 contract evolution breaks INV-R4 | HIGH | HIGH | PARTIALLY |
| 6 | O-05 | Governance escalation black hole | MEDIUM | HIGH | NO |
| 7 | T-01 | Consistent-cut search exhaustion | MEDIUM | HIGH | PARTIALLY |
| 8 | O-04 | Parameter misconfiguration cascade | MEDIUM | HIGH | NO |
| 9 | I-01 | C3 CRDT failure blocks digest distribution | MEDIUM | HIGH | PARTIALLY |
| 10 | T-05 | Recovery saga WAL corruption | LOW | HIGH | PARTIALLY |
| 11 | I-03 | C7 Emergency Bypass leaves recovery orphaned | LOW | HIGH | PARTIALLY |
| 12 | A-02 | Consumer-side digest poisoning | LOW | HIGH | PARTIALLY |
| 13 | A-03 | Authority-override quorum manipulation | LOW | HIGH | YES (trade-off) |
| 14 | T-04 | VTD hash chain replay divergence | LOW | HIGH | NO |
| 15 | O-01 | 21-predicate maintenance burden | HIGH | MEDIUM | NO |
| 16 | M-01 | Recovery perceived as unnecessary | HIGH | MEDIUM | NO |
| 17 | M-02 | Part III never implemented | HIGH | MEDIUM | YES (acknowledged) |
| 18 | A-05 | Fake multi-layer failure injection | MEDIUM | MEDIUM | NO |
| 19 | I-04 | C31/defense system config combinatorics | MEDIUM | MEDIUM | NO |
| 20 | T-02 | C6 Merkle root non-determinism | MEDIUM | MEDIUM | NO |
| 21 | I-07 | C34/C3 SAFE_MODE circular dependency | LOW | MEDIUM | PARTIALLY |
| 22 | T-06 | Digest history wrap-around collision | LOW | MEDIUM | NO |
| 23 | T-07 | Temporal trust gradient exploitation | LOW | MEDIUM | PARTIALLY |
| 24 | I-06 | Pre-C7 communication underspecified | LOW | MEDIUM | NO |
| 25 | A-06 | Reconstruction engine as oracle | LOW | MEDIUM | NO |
| 26 | O-03 | C5 snapshot storage growth | MEDIUM | LOW | PARTIALLY |
| 27 | M-03 | External auditors cannot verify recovery | MEDIUM | LOW | NO |
| 28 | A-04 | Digest computation timing side-channel | LOW | LOW | NO |

---

## Cross-Cutting Themes

### Theme 1: The Dormancy Problem
Scenarios O-02, O-01, M-01, and T-03 all stem from the same root cause: C34's recovery path is dormant code that will rot. The design's conscious choice to minimize always-on overhead (principle #3) creates a system that is cheap to run but expensive to trust. Every system that has ever relied on dormant recovery code has eventually discovered that the recovery code did not work when needed. The design team must either accept this risk explicitly or invest in active recovery testing.

### Theme 2: The Specification-Implementation Gap
T-03, I-02, I-06, and O-04 all reflect the gap between C34's specification-level completeness and the operational reality of maintaining it. The specification is thorough — 21 predicates, 15 reference types, 19 parameters — but each of these is a maintenance obligation that must survive 5 years of system evolution. The extensibility rule (SS2.2.2) is necessary but not sufficient.

### Theme 3: The Recovery-During-Failure Paradox
T-05, I-03, A-01, and I-01 all reflect the fundamental paradox of C34: it is a recovery system that is most needed when the system is most broken. The components it depends on for recovery (C3 CRDT broadcast, C7 WAL, C7 saga infrastructure) are themselves failure candidates. The design addresses this with fallback mechanisms (pre-C7 self-coordination, per-layer recovery), but the fallbacks are less well-specified than the primary path.

### Theme 4: Small Quorum Vulnerability
A-03 and the corroboration thresholds generally reflect a fundamental constraint: with only 2-3 consumers per layer, the quorum sizes are too small for robust Byzantine fault tolerance. This is an inherent architectural constraint of a 5-layer system, not a C34 design flaw. But the consequence is that C34's witness corroboration provides weak adversarial guarantees — it is effective against accidental corruption but not against a sophisticated adversary who compromises 2+ layers.

---

## Recommendations for Design Team

### Must Address (Severity HIGH, unaddressed or partially addressed)
1. **Add recovery drill specification** (O-02) — define periodic simulated recovery exercises
2. **Add predicate exhaustiveness runtime check** (T-03, I-02) — verify predicates match C9 revision at startup
3. **Specify read-only mode during recovery** (A-01) — no new state mutations between DETECTING and NORMAL
4. **Define automated degraded-operation for governance timeout** (O-05) — do not let recovery hang indefinitely
5. **Add parameter constraint validation** (O-04) — define and enforce inter-parameter invariants
6. **Specify fallback digest distribution** (I-01) — do not depend solely on C3 CRDT for normal-operation digests

### Should Address (Severity MEDIUM-HIGH, design improvement)
7. **Add best-effort consistent-cut selection** (T-01) — do not fail when no perfect cut exists
8. **Specify C5 replay logic versioning** (T-04) — version-stamp credibility update logic in snapshots
9. **Backup saga state in C8 HDL** (T-05) — minimal recovery coordination state in the most resilient layer
10. **Define C6 degraded recovery without C7** (I-03) — allow C6 to self-recover when C7 is unavailable

### May Dismiss (Acknowledged residual risk)
11. A-03 (authority-override quorum) — conscious trade-off, but add single-consumer-disagreement notification
12. I-05 (Part III absence) — accepted risk, but consider minimal C8-only Part III in Wave 2-3
13. A-04 (timing side-channel) — low severity, note as residual
14. O-03 (snapshot storage growth) — manageable via parameter governance

---

*End of Pre-Mortem Analysis*
