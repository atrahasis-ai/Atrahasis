# C34 Research Reconciliation — Assumption Validation

**Invention:** C34 — Black-Start Recovery Fabric with Adversarial State Reconstruction
**Stage:** RESEARCH → FEASIBILITY gate
**Date:** 2026-03-12

---

## Ideation Assumption → Research Finding Mapping

### A1: Boot order C8→C5→C3→C7→C6 is correct
- **Science Advisor (F-2):** CONFIRMED (Confidence 5/5). No true circular dependency. C8's SETTLEMENT_TICK is self-timed. C5 boots in degraded mode (no VRF committees) until C3 is online.
- **Status:** VALIDATED

### A2: Per-epoch state digests enable retrospective consistent-cut without Chandy-Lamport
- **Science Advisor (F-1):** CONFIRMED with caveat (Confidence 4/5). Sound but worst-case gap is 36,000s (one CONSOLIDATION_CYCLE). All cross-layer reads must be logged in digests.
- **Design constraint:** Add requirement that all cross-layer reads are captured in epoch digests.
- **Status:** VALIDATED WITH CONSTRAINT

### A3: Merkle verification is computationally feasible at SETTLEMENT_TICK frequency
- **Science Advisor (F-7):** CONFIRMED (Confidence 5/5). ~4ms per 60s tick = 0.007% overhead.
- **MF-4 (benchmark anti-entropy overhead):** RESOLVED — overhead is negligible.
- **Status:** VALIDATED

### A4: Authority-directed reconciliation preserves invariants
- **Science Advisor (F-3):** CONDITIONALLY CONFIRMED (Confidence 3/5). Cannot detect subtle corruption of the authoritative layer itself. This is a fundamental limitation.
- **Mitigation:** Structural invariant checks + Part III causal reconstruction as cross-check.
- **Status:** VALIDATED WITH KNOWN LIMITATION

### A5: Causal reconstruction from cross-layer references is feasible
- **Science Advisor (F-4):** CONFIRMED (Confidence 4/5). Polynomial complexity O(R×W×N). NOT NP-hard. Coverage varies: C8 ~90%, C5 ~70%, C3 ~60%, C7 ~55%, C6 ~50%.
- **MF-1 (reference density):** PARTIALLY RESOLVED — coverage is sufficient for bounded reconstruction but not full reconstruction of all layers.
- **Status:** VALIDATED WITH COVERAGE BOUNDS

### A6: C5 state snapshotting is addressable
- **Science Advisor (F-6):** CONFIRMED (Confidence 4/5). VTD log is minimum durable state. Credibility opinions replayable in ~60ms with periodic snapshots. Needs VTD hash chain for tamper evidence.
- **MF-3 (C5 snapshotting blocking dependency):** RESOLVED — feasible via VTD log.
- **Status:** VALIDATED

### A7: Adversarial digest corruption is a realistic attack model
- **Science Advisor (F-5):** CONFIRMED but NARROW (Confidence 3/5). Meaningful only when digests are unsigned. Mandatory digest signing reduces attack to layer compromise (baseline threat). Still valuable as defense-in-depth.
- **Landscape Analyst:** No existing system addresses adversarial recovery infrastructure attacks.
- **Status:** VALIDATED — attack model is narrow but novel and worth addressing

### A8: No direct prior art for the combined architecture
- **Prior Art Researcher:** CONFIRMED. Part III has no direct precedent. Parts I & II have antecedents but C34's integration is novel.
- **Landscape Analyst:** Four confirmed technology gaps. Unoccupied niche.
- **MF-5 (novelty ceiling):** UPDATED — novelty may be 3.5-4.0 given Part III's lack of precedent.
- **Status:** VALIDATED

---

## Contradictions Found
- **None fatal.** The authority-directed reconciliation limitation (A4) and narrow adversarial model (A7) are acknowledged limitations, not contradictions.

## Research Questions Resolved
- MF-1: Cross-layer reference density — sufficient for bounded reconstruction (50-90% by layer)
- MF-3: C5 snapshotting — addressable via VTD log
- MF-4: Merkle overhead — negligible (0.007%)

## Research Questions Remaining
- MF-2: Recovery coordinator placement (C7 vs C9) — deferred to DESIGN
- Exact snapshot interval for C5 VTD log — deferred to DESIGN
- Whether background anti-entropy should be continuous or on-demand — Science Advisor says overhead is trivial, so continuous is viable

## Recommendation
**PROCEED TO FEASIBILITY.** All core assumptions validated. No fatal contradictions. Known limitations are bounded and mitigated.
