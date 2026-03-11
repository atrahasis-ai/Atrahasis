# C7 Science Assessment — Recursive Intent Fabric (RIF)

**Date:** 2026-03-10
**Advisor:** Science Advisor
**Overall Soundness: 3.5/5**

## Claim Assessment Summary

| # | Claim | Score | Verdict |
|---|-------|-------|---------|
| 1 | Intent as First-Class Metabolic Object | 4/5 | SOUND |
| 2 | Recursive Decomposition Scales Sub-Linearly | 3/5 | PARTIALLY_SOUND |
| 3 | System 3/System 4 Prevents Executive Oscillation | 4/5 | SOUND |
| 4 | Sovereignty-Preserving Without Performance Loss | 3/5 | PARTIALLY_SOUND |
| 5 | Formal Decomposition Algebra Guarantees Termination | 4/5 | SOUND (with caveats) |
| 6 | Anticipatory Planning via Read-Only Projections | 3/5 | PARTIALLY_SOUND |

## Critical Scientific Gaps (Pre-DESIGN)

### Gap 1: Sovereignty Enforcement Boundary (CRITICAL)
Tension between hierarchical coordination (Claim 2) and sovereignty preservation (Claim 4). Must precisely define: Can the orchestrator withhold resources? Quarantine? Redirect traffic? Each is a soft override. Need formal specification of "cannot override."

### Gap 2: Locality Assumption Quantification (HIGH)
Sub-linear scaling (Claim 2) depends on fraction of intents that are locus-local. Must estimate from realistic workload models. Is there a tipping point where Global Executive becomes bottleneck?

### Gap 3: Resource Composition Rules (HIGH)
Decomposition algebra (Claim 5) needs explicit resource aggregation semantics. Additive resources (compute) vs shared resources (bandwidth) have different composition rules. Without this, resource bound preservation is aspirational.

### Gap 4: System 5 Specification (HIGH)
Architecture lacks explicit System 5 (identity/policy). Who resolves System 3 vs System 4 conflicts? Who prevents mission drift? Must either include System 5 or explain why it's unnecessary. Note: G-class governance likely serves as System 5 but this must be made explicit.

### Gap 5: Failure Escalation Protocol (MEDIUM)
What happens when a subsystem fails non-self-correctably? "It never happens" is not acceptable at planetary scale. Need defined escalation path that respects sovereignty but enables recovery.

### Gap 6: Projection Staleness Bounds (MEDIUM)
Anticipatory planning (Claim 6) needs maximum acceptable projection lag specification. Determines whether read-only approach is sufficient for intended planning horizons.

## Cross-Claim Coherence

### Coherent
- Claims 1+5: Intent objects provide substrate for decomposition algebra
- Claims 2+3: Hierarchy maps onto System 3/4 separation
- Claims 3+6: Anticipatory planning realizes System 4's strategic function

### Tensions
1. **Sovereignty vs Hierarchy (Claims 4 vs 2):** Hierarchies impose structure on subordinates. Need to distinguish coordination (assigning intents to willing loci) from override (forcing internal behavior change).
2. **Formal Guarantees vs Autonomy (Claims 5 vs 4):** Algebra guarantees apply to decomposition *plan*, not *execution*. Autonomous agents may not complete assigned intents.
3. **Anticipatory vs Formal (Claims 6 vs 5):** Speculative intents from System 4 may be canceled — algebra must handle this.

## Recommended Experiments

1. **Comparative simulation:** Intent lifecycle vs task queues vs workflow DAGs — measure failure recovery, observability, overhead
2. **Locality ratio sweep:** Vary locus-local fraction (50%-99%), measure coordination overhead and Global Executive load
3. **Oscillation detection:** Unified executive vs System 3/4 separation under load
4. **Fault injection:** Sovereignty-preserving vs override-capable coordination across failure classes
5. **TLA+ model check:** Decomposition algebra termination and cycle-freedom proof
6. **Projection sufficiency:** Planning quality with varying projection staleness levels

## Recommendation

**Proceed to DESIGN with conditions.** Theoretical foundations are strong. Six gaps must be addressed as explicit design constraints, not left as implicit assumptions. Most critical: sovereignty/hierarchy tension (Gap 1).
