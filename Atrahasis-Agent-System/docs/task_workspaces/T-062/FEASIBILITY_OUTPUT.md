# C34 — Black-Start Recovery Fabric: FEASIBILITY Output

**Invention:** C34 — Black-Start Recovery Fabric with Adversarial State Reconstruction
**Stage:** FEASIBILITY
**Date:** 2026-03-12

---

## Refined Scores
- **Novelty:** 3.5
- **Feasibility:** 4.0
- **Impact:** 3.5 (reduced from 4.0 — most failures handled by existing per-layer recovery)
- **Risk:** 4/10 (MEDIUM)

## Key Changes from IDEATION

1. **Authority corruption detection added.** Cross-layer witness corroboration (soft-TMR): if a majority of consumer layers disagree with the authority's recovered state, the authority is flagged and recovery falls back to the last multiply-attested snapshot.

2. **Reconstruction window made adaptive.** Triple-criteria termination: (a) coverage plateau detection, (b) compute budget exhaustion, (c) total-loss cost comparison against snapshot restore. 10-epoch hard cap retained as outer bound.

3. **Recovery coordinator placement resolved (MF-2).** Protocol specification at C9 integration level. Runtime coordinator is a C7 recovery saga. Pre-C7 boot phases (C8→C5→C3) self-coordinate via embedded synchronization predicates.

4. **Part III phased.** Adversarial reconstruction fully specified at DESIGN but flagged for Wave 4+ implementation. Parts I and II target Wave 2.

5. **Consumer-side audit trail added.** Each layer records digests of state received from other layers, creating an authority-independent verification path.

6. **Temporal trust gradient added.** Long-surviving unchallenged digests carry higher trust weight during recovery.

## Monitoring Flags Status
- **MF-1 (reference density):** PARTIALLY RESOLVED — coverage 50-90% by layer, sufficient for bounded reconstruction
- **MF-2 (coordinator placement):** RESOLVED — protocol at C9, coordinator in C7, pre-C7 self-coordinating
- **MF-3 (C5 snapshotting):** RESOLVED — VTD log + periodic snapshots, ~60ms replay
- **MF-4 (anti-entropy overhead):** RESOLVED — 0.007% of tick budget, negligible
- **MF-5 (novelty claims):** Updated — Part III has no direct precedent; claims focus on integration + adversarial resilience

## Domain Translator Sub-Problem Resolutions
1. **Authority corruption:** Soft-TMR via cross-layer witnesses + temporal trust gradient + consumer-side audit trail
2. **Reconstruction bounding:** Triple-criteria adaptive termination + 10-epoch hard cap
3. **Coordinator placement:** FEMA/NRF pattern — protocol at C9, execution in C7, pre-C7 self-coordinating

## Adversarial Analyst Assessment
- Strongest counter-argument: existing per-layer recovery handles most failure modes (partially accepted → impact reduced to 3.5)
- Boot-order and Merkle components are commodity engineering (accepted — novelty is in the integration)
- Adversarial reconstruction attack model is narrow (accepted — Part III phased to Wave 4+)
- Recommendation: do not abandon, but narrow scope → incorporated

## Commercial Viability
- Minimal overhead (0.007% always-on, rest dormant)
- Becomes blocking at C22 Wave 2 entry
- No direct revenue generation — necessary infrastructure
- Limited independent value outside AAS; scholarly contribution viable

## Remaining Risks
1. C5 snapshot implementation may be more complex than estimated
2. Synchronization predicate completeness — 10+ predicates must be exhaustive
3. Part III deferred risk — coordinated attack before Wave 4 forces full snapshot restore
4. Cross-layer witness cannot detect collusion across 4+ layers

## Design Constraints
- Digest computation ≤ 4ms/60s tick (0.007%)
- Strictly linear boot order C8→C5→C3→C7→C6
- Pre-C7 phases must self-coordinate
- Protocol spec at C9 level, not owned by any single layer
- Causal reconstruction polynomial O(R×W×N)
- Must integrate with (not replace) existing per-layer recovery mechanisms

## Recommendation
**ADVANCE to DESIGN**
