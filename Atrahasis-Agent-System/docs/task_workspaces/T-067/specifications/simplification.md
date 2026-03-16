# C37 EFF Simplification Report

**Role:** Simplification Agent
**Date:** 2026-03-12
**Agent:** Enki (Claude Code)
**Question:** What is the simplest version that preserves the novel claim?

---

## Core Innovation Claim

The novel claim is: **a privacy-preserving feedback loop from post-hoc verification outcomes to population-level advisory signals, behind an explicitly non-enforcement membrane, for sovereign heterogeneous agents.**

The Advisory Membrane Pattern is the primary patent differentiator (per Prior Art Report).

## Simplification Analysis

### Component: VFL — KEEP (core)
VFL is the engine. Without it, there's nothing to publish. The three-layer privacy (k-anonymity + DP + secure aggregation) is essential for the sovereignty claim.

**Simplification opportunity:** The hierarchical Bayesian estimator (James-Stein shrinkage) adds complexity for handling rare claim classes. Could be deferred to v1.1 — simply suppress rare classes until they accumulate data.

**Recommendation:** KEEP hierarchical Bayesian. The alternative (suppressing rare classes) means H, K, N classes get no feedback for potentially months. That's 3 of 9 classes silenced. The shrinkage estimator is well-understood (20 lines of code) and the transparency flag makes it safe.

### Component: RSC — SIMPLIFY
RSC has the lowest soundness score (2.5/5). Three format types are already restricted from the original broader concept.

**Simplification opportunity:** RSC could start as a STATIC catalog — seed patterns only, no VFL-derived pattern generation in v1.0. Pattern generation from VFL data is the complex part (credibility tracking, lifecycle FSM, C6 integration). Static seed patterns are just curated documents.

**Recommendation:** REJECT this simplification. The dynamic credibility tracking is what makes RSC more than a static wiki. Without VFL-derived patterns and credibility updates, RSC is just documentation. The lifecycle FSM is inherited from C6 EMA (not new complexity) and the credibility tracking is 50 lines of subjective logic.

### Component: CABS — SIMPLIFY
CABS has three computation sources (C9 weights, C7 complexity, VFL calibration). The three-source fusion adds complexity.

**Simplification opportunity:** CABS could use ONLY C9 claim class weights in v1.0. The VFL calibration and RIF complexity scores improve accuracy but aren't needed for the MVP.

**Recommendation:** REJECT. C9 weights alone produce a fixed lookup table, not a dynamic signal. The value of CABS is that it adapts to observed verification data. Without VFL calibration, CABS is a static configuration, which could be a C23 parameter table rather than a new component.

### Component: Advisory Membrane — KEEP (core)
The membrane IS the differentiator. Cannot simplify without losing the novel claim.

**One simplification:** The C17 RSC-aware whitelist (structural fingerprint discounting) is the most complex membrane sub-component. Pre-mortem Scenario 1 ("The Invisible Cage") rates this as CRITICAL.

**Could we defer the whitelist?** NO. Without it, C17 structural similarity would flag agents following RSC patterns as behaviorally similar (potential Sybils). This would effectively punish RSC consumption, violating the membrane guarantee on day one.

### Pattern Diversity Monitoring — COULD DEFER
The convergence monitoring (HHI computation, sampling-based pairwise similarity) is a defense against Pre-mortem Scenario 2 ("Monoculture Collapse"). It's rated CRITICAL × HIGH.

**Could we defer?** Risky but possible for v1.0. Monoculture collapse takes months to develop (per pre-mortem timeline). We could deploy without convergence monitoring and add it before population-scale deployment.

**Recommendation:** KEEP. The monitoring is ~30 lines of code (sampling, pairwise similarity, threshold check). Deferring a CRITICAL mitigation for a savings of 30 lines is not a good trade.

### VFL Anomaly Detection — COULD SIMPLIFY
The dual-cadence publication (normal + anomaly-triggered) adds a chi-squared test at every TIDAL_EPOCH.

**Could we use single cadence only?** Yes, at the cost of 10-hour latency for detecting quality shifts. Pre-mortem Scenario 6 ("Feedback Freeze") rates this MEDIUM × MEDIUM.

**Recommendation:** KEEP. Chi-squared test is 15 lines. The alternative is discovering quality degradation 10 hours late.

## Removed/Deferred Items

| Item | Action | Rationale |
|------|--------|-----------|
| Multi-class RSC patterns (OQ-3) | DEFER to v1.1 | Duplicate per class is simpler and sufficient for v1.0 |
| CABS feedback damping / circuit breaker | DEFER to pre-production | Pre-mortem Scenario 3 mitigation; can be added before scale |
| CABS budget floor / Gini cap | DEFER to pre-production | Pre-mortem Scenario 5 mitigation; not needed at low population |
| VFL manipulation detection | DEFER to Wave 3 | Pre-mortem Scenario 4 mitigation; requires C12 AVAP integration |
| Fast-path VFL (TIDAL_EPOCH-rate distributional shift) | DEFER to v1.1 | Pre-mortem Scenario 6 mitigation; anomaly detection partially covers |
| `architecture_applicability` field future values | DEFER | v1.0 has only "universal" and "llm_preferred" |

## Verdict

**The architecture is already well-scoped.** The FEASIBILITY conditions drove most of the simplification (RSC format restriction, CABS range format). The pre-mortem mitigations add necessary defensive engineering, not unnecessary complexity.

**No components should be removed.** The four components (VFL, RSC, CABS, Advisory Membrane) are the minimum set that preserves the novel claim. Removing any one breaks the feedback loop or the sovereignty guarantee.

**Deferred items are appropriate deferrals** — they address pre-mortem scenarios that develop over months, not days. They should be specified as "Wave 3+" requirements in the Master Tech Spec.
