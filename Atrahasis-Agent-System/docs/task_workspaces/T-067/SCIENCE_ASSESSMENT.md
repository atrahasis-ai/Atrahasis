# Science Assessment — C37 Epistemic Feedback Fabric (EFF)

**Assessor:** Science Advisor | **Date:** 2026-03-12 | **Stage:** RESEARCH
**Agent:** Enki (Claude Code)

---

## Executive Summary

**Overall Soundness Score: 3.3 / 5** — Architecturally coherent with genuine theoretical grounding in privacy and compute scaling, but with one component (RSC) lacking sufficient evidence and one component (Advisory Membrane) facing fundamental information-theoretic limits on its guarantees.

---

## 1. Per-Component Assessments

### Component 1: Verification Feedback Loop (VFL) — SOUND (4.0/5)

**Privacy-preserving aggregation:** Well-studied problem. Combination of k-anonymity floors (suppress groups < k=10) + differential privacy noise (epsilon 1.0-4.0) + secure aggregation provides defense in depth. No novel cryptography required. DP noise scales as O(1/epsilon) independent of n, meaning accuracy improves as population grows — favorable for 1K-100K agents.

**Minimum sample size:** Detecting 10% change in acceptance rate requires n >= 199 per claim class per reporting period. For rare classes (N, H, K), use hierarchical Bayesian estimation (James-Stein) to borrow strength across related classes, or longer aggregation windows.

**Signal staleness:** Per-class baseline acceptance rates change on timescales of months — reporting per CONSOLIDATION_CYCLE (10 hours) is more than frequent enough. Anomaly-triggered updates handle fast-changing signals (chi-squared test, p < 0.01).

**Key flag:** C9 shows wide variation in admission thresholds (D: 0.95, H: 0.50). VFL metrics must be calibrated per-class, not raw acceptance rates.

### Component 2: Reasoning Strategy Catalog (RSC) — PARTIALLY SOUND (2.5/5)

**Model-agnostic format:** Feasible ONLY for three pattern types:
1. Declarative task decompositions ("for R-class, check: premises, validity, support, coverage")
2. Anti-pattern descriptions ("circular evidence rejected at 3x baseline")
3. Verification checkpoint schemas (checklists)

NOT feasible for: prompt templates, chain-of-thought structures, internal representation guidance.

**Evidence that published patterns improve quality:** Strong for LLMs via RAG/few-shot (Wei et al. 2022). No evidence for symbolic agents or passive consumption. CPG literature shows 5-10% improvement in human practitioners, but agents lack the enforcement mechanisms (licensing, liability) that drive CPG adoption.

**Pattern credibility measurement:** Bayesian posterior Beta(n_success + α, n_fail + β) is well-defined. Significant risks: confounding (selection bias — better agents may self-select into pattern consumption), Goodhart's Law (gaming patterns to pass verification), survivorship bias (novel patterns lack data).

**Recommendation:** Use subjective logic opinion tuples (b, d, u, a) consistent with C6 EMA. New patterns start with high uncertainty (u >= 0.7).

**Contradiction:** The assumption that RSC serves "both neural and symbolic agents" is overstated. Must either restrict scope to LLM agents or define two pattern subtypes.

### Component 3: Budget Advisory Signals (CABS) — PARTIALLY SOUND (3.5/5)

**Literature support:** TALE-EP (ACL 2025) reduces token costs 67% while maintaining performance. Compute-optimal scaling (Snell et al. 2024) shows 4x efficiency improvement. AVA shows 20-40% cost reduction through adaptive allocation.

**Critical caveat:** "Increasing the Thinking Budget is Not All You Need" (arXiv 2512.19585) demonstrates non-monotonic budget-performance relationship. More tokens can DECREASE performance. CABS must recommend (min_sufficient, recommended, max_useful) ranges, not point estimates, and should pair budget with strategy recommendations.

**Model-agnostic budget recommendations:** Feasible via:
1. C9 claim class difficulty weights (D: 1.0, R: 2.0, H: 2.5, N: 3.0)
2. Task-extrinsic complexity from descriptions (CARD framework)
3. Historical calibration from VFL data (75th percentile of successful claims)
4. C7 RIF decomposition structural complexity

No agent internals required.

### Component 4: Advisory Membrane — PARTIALLY SOUND (3.0/5)

**Direct enforcement:** Feasible via standard information flow control — data segregation, formal labels (ADVISORY_PRIVATE), microservice isolation. C17/C35 components cannot access advisory consumption records. Straightforward.

**Side-channel risks:**
- **Timing:** LOW risk. RSC lookup latency (~50-200ms) lost in LLM inference noise (seconds-minutes).
- **Structural:** HIGH risk. Agents following RSC patterns produce similar reasoning structures. C17 structural modality (w=0.25) may detect this as shared origin. **Mitigation required:** C17 must maintain RSC-synchronized whitelist; discount structural similarity matching published patterns.
- **Resource:** LOW risk. Catalog lookups too small to distinguish from normal activity.
- **Quality inference:** FUNDAMENTAL LIMITATION. Agents consuming effective signals outperform non-consumers. C35 can detect this performance gap without knowing the cause.

**Voluntariness paradox:** If advisory signals are effective, they create performance gaps that constitute implicit market pressure to adopt. The membrane prevents surveillance-based enforcement but cannot prevent performance-based self-selection. This is a property of ALL effective advisory systems (medical CPGs face the same dynamic). The specification should acknowledge this explicitly rather than claiming complete voluntariness.

---

## 2. Assumption Validation Table

| Assumption | Evidence | Verdict |
|---|---|---|
| Privacy-preserving aggregation is feasible | DP, secure aggregation, FL literature | **VALIDATED** |
| Population-level signals useful for individual reasoning | CPG literature (5-10% improvement); RAG/few-shot for LLMs | **PARTIALLY VALIDATED** |
| Reasoning patterns can be model-agnostic | Feasible for declarative decompositions only | **PARTIALLY VALIDATED** |
| Publishing patterns improves reasoning quality | Strong for LLMs via RAG; no evidence for symbolic agents | **PARTIALLY VALIDATED** |
| Budget allocation improves reasoning quality | TALE, AVA, Snell et al. | **VALIDATED** (non-monotonic) |
| Budget recommendations without agent internals | CARD, C9 weights, historical calibration | **VALIDATED** |
| Advisory Membrane prevents enforcement | Direct: yes. Side channels: structural risk. Quality inference: fundamental limit | **PARTIALLY VALIDATED** |
| Advisory signals remain truly voluntary | Cannot prevent performance-based self-selection | **NEEDS DESIGN WORK** |

---

## 3. Falsification Experiments

1. **VFL Privacy-Utility:** DP with epsilon=2.0 on 10K synthetic VTDs across 9 classes. Falsified if MAE > 5% or power to detect 10% drop < 0.70.
2. **RSC Effectiveness:** A/B cohort test (RSC access vs. no access). Falsified if no significant improvement in >= 5/9 claim classes.
3. **CABS Budget-Performance:** Compare fixed vs. CABS-recommended vs. unlimited budgets on 200 tasks. Falsified if CABS doesn't achieve 90% of unlimited quality at 50% cost.
4. **Membrane Side-Channel:** 50 consuming + 50 non-consuming agents. Falsified if classifier predicts consumption from C17 features with AUC > 0.65.

---

## 4. Key Risks

| Risk | Severity | Mitigation |
|---|---|---|
| VFL insufficient sample for rare classes | MEDIUM | Hierarchical Bayesian; longer windows; suppress n < 10 |
| RSC ineffective for non-LLM agents | HIGH | Restrict v1.0 to declarative patterns; label by architecture |
| CABS wrong budget (non-monotonic) | MEDIUM | Range recommendations; strategy + budget pairs |
| Membrane structural side-channel via C17 | HIGH | RSC-aware baseline adjustment in C17 |
| Advisory becomes de facto mandatory | LOW-MEDIUM | Acknowledge paradox; ensure membrane prevents surveillance-based enforcement |
| VFL Goodhart's Law | MEDIUM | Inherited from C5; flag for C5 v3.0 |

---

## 5. Recommendations for FEASIBILITY

1. Restrict RSC v1.0 to declarative decompositions, anti-patterns, and checklists
2. Specify minimum sample sizes per claim class; use hierarchical Bayesian models
3. CABS: (min_sufficient, recommended, max_useful) triples, not point estimates
4. C17 must maintain RSC-synchronized whitelist for structural similarity discounting
5. Acknowledge voluntariness paradox explicitly in specification
