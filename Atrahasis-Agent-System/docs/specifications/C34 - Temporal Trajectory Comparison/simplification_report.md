# C34 Simplification Report

**Invention:** C34 — Black-Start Recovery Fabric with Adversarial State Reconstruction
**Stage:** DESIGN (post-architecture review)
**Role:** Simplification Agent

---

## Summary

10 recommendations that reduce C34 from ~2,076 lines to ~1,666 lines (~20% reduction), from 19 parameters to 10, from 21 predicates to ~11, and from a 7-state FSM to a 5-state FSM — while preserving all four novel claims.

---

## Recommendations

### S1. REMOVE: Temporal Trust Gradient
- Not essential — consistent-cut algorithm never needs tiebreaking
- Saves: 3 parameters, ~20 lines
- Simpler alternative: Use raw age as ordinal preference if needed later

### S2. REPLACE: Digest History Merkle Tree → flat circular buffer
- Consumer-side verification compares digests directly, doesn't need Merkle proofs
- Saves: ~30 lines, O(log N) → O(1) per tick
- Simpler alternative: CircularBuffer<TickDigest, DIGEST_RETENTION_TICKS>

### S3. REMOVE: 7 reverse-direction synchronization predicates
- Duplicate witness verification (Part II). Reverse predicates check later-boot layers from earlier-boot consumer logs — this is exactly what Part II does post-boot.
- Reduces predicates from 21 to ~14
- Saves: ~40 lines

### S4. REMOVE: Defense system predicates (C11/C12/C13)
- Defense subsystem state already covered by host layer digests
- Reduces predicates by 3 more (total ~11 with S3)
- Saves: ~10 lines

### S5. SIMPLIFY: Predicate extensibility mechanism
- Process/governance concern, not architectural component
- Replace with sentence in INV-R4
- Saves: ~10 lines

### S6. REMOVE: PRED_C4C6_ASV
- C4 excluded from C34 scope but then included via predicate — inconsistency
- Saves: ~5 lines

### S7. SIMPLIFY: Recovery Completion Attestation → single signer (C7)
- Multi-layer signing is ceremony — C7 already verified all predicates
- Saves: ~30 lines, removes synchronization bottleneck

### S8. REDUCE: Part III → registry + stub (largest savings)
- Part III deferred to Wave 4+. Keep reference registry (novel claim), remove algorithm/termination/coverage/API (~200 lines)
- Saves: ~200 lines, 6 parameters
- Removes RECONSTRUCTING state from FSM

### S9. REMOVE: C5 VTD Hash Chain specification
- C5-internal implementation detail. C34 should specify what C5's digest must contain, not how C5 chains VTDs internally.
- Saves: ~50 lines

### S10. COLLAPSE: DETECTING + INITIALIZING → single state
- Functionally one transition. False-alarm handled as guard.
- Saves: ~15 lines, simplifies FSM from 7 to 5 states (with S8)

---

## Totals

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Lines | ~2,076 | ~1,666 | ~20% |
| Parameters | 19 | 10 | ~47% |
| Predicates | 21 | ~11 | ~48% |
| FSM states | 7 | 5 | ~29% |
| Novel claims | 4 | 4 | 0% |

## Priority Order
1. S8 (Part III stub) — largest savings
2. S3 (reverse predicates) — largest conceptual simplification
3. S9 (VTD chain) — improves cohesion
4. S2 (flat buffer) — removes unnecessary complexity
