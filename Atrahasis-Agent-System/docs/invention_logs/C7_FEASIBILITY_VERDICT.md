# C7 Feasibility Verdict — Recursive Intent Fabric (RIF)

**Date:** 2026-03-10
**Council:** Advocate, Skeptic, Arbiter
**Decision:** CONDITIONAL_ADVANCE

## Scores

| Criterion | Score |
|-----------|-------|
| Novelty | 4 |
| Feasibility | 3 |
| Impact | 4 |
| Risk | 6/10 (MEDIUM-HIGH) |

## Council Positions

**Advocate:** Genuine gap in landscape validated by Google's own scaling research. Graduated sovereignty resolves fatal flaw. 6 novelty gaps survive scrutiny. 12-18mo window sufficient. Recommends advance.

**Skeptic:** Three concerns: (1) graduated sovereignty is governance-gated override, not true sovereignty — novelty should be 3 not 4; (2) ≥80% locality assumption unvalidated; (3) implementation complexity is multi-year program, feasibility is optimistic at 3.

**Arbiter:** Advocate's case stronger. Graduated sovereignty is more rigorous than blanket claim it replaced. Locality monitorable. Complexity reflected in feasibility 3. Recommends CONDITIONAL_ADVANCE.

## Hard Gates (Must Pass Before SPECIFICATION)

1. **Decomposition Algebra Formal Proof** — TLA+ or Alloy model demonstrating:
   - Termination guarantee for all well-formed intent trees
   - Cycle-freedom under context-dependent decomposition
   - Resource bound preservation across decomposition levels

2. **Locality Ratio Validation** — Analysis on realistic intent distributions showing:
   - ≥80% locus-local under normal operation
   - Graceful degradation profile when ratio drops below 80%
   - Global Executive throughput model under varying cross-locus ratios

3. **Sovereignty Relaxation Safety** — Formal proof that:
   - Governance-gated override cannot cascade into permanent sovereignty loss
   - Automatic reversion is guaranteed (lease expiry cannot be indefinitely extended)
   - Constitutional tier protections are mathematically inviolable

4. **Locus Failover Latency** — Demonstrate:
   - Standby promotion within 1 epoch boundary
   - Zero intent state loss during failover
   - Emergency bypass mode functional for critical intents

## Required Actions

1. Define decomposition algebra rules: which operation classes decompose into which, composition rules, forbidden decomposition paths
2. Specify System 3 ↔ System 4 communication protocol formally (not just separation)
3. Define intent admission control criteria with formal security properties
4. Specify compensation protocols for partial decomposition failure (saga-style rollback)

## Monitoring Flags

| Flag | Level | Condition |
|------|-------|-----------|
| Cross-locus ratio | RED | >20% cross-locus intents sustained >10 epochs |
| Decomposition depth | AMBER | Average depth >3 levels sustained |
| System 4 proposal rate | AMBER | >1 proposal per cool-down period attempted |
| Intent GC backlog | AMBER | DISSOLVED intent count >10x active intent count |
| Sovereignty relaxation frequency | RED | >2 relaxation events per 100 epochs |
| Locus failover count | AMBER | >1 failover per 50 epochs per locus |

## Key Refinements Applied

1. Graduated sovereignty model (3-tier: constitutional/operational/coordination)
2. Domain-Scoped State Plane replacing "thin stateless infrastructure"
3. Locus fault tolerance (active-passive + emergency bypass)
4. Intent Admission Control gate
5. System 5 = G-class governance (explicit VSM mapping)
6. Oscillation dampening (cool-down + similarity detection + stability gating)
7. Decomposition budget (time + compute) alongside max_depth
8. Sub-linear scaling bounded: requires ≥80% locus-local
9. Vector clocks for causal ordering under partition
