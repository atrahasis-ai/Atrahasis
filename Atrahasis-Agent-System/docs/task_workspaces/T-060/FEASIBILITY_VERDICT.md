# C35 FEASIBILITY VERDICT

**Invention:** C35 — Seismographic Sentinel with PCM-Augmented Tier 2
**Task:** T-060
**Stage:** FEASIBILITY → DESIGN gate
**Date:** 2026-03-12
**Assessment Council:** Technical Feasibility Assessor, Novelty Assessor, Impact Assessor, Arbiter

---

## Inputs Considered

| Source | Role | Verdict | Key Finding |
|--------|------|---------|-------------|
| Prior Art Report | Prior Art Researcher | HIGH composite novelty | 24 findings; PCM has no direct precedent; no system combines all 6 innovations |
| Landscape Report | Landscape Analyst | Unoccupied niche | 6 gaps confirmed; ~55% novel development; LOW competitive threat; FAVORABLE timing |
| Science Assessment | Science Advisor | PARTIALLY_SOUND (3.5/5) | 8 assessments; 3 contradictions found (all addressable); no fundamental impossibilities |
| Assumption Validation | Science Advisor (Reconciliation) | RESEARCH SURVIVES | 3 contradictions, 0 fatal; novelty 3.5-4.0 confirmed; feasibility revised to 3.5-4.0 |
| Feasibility Council | Ideation Council (reconvened) | UNANIMOUS ADVANCE | All 3 contradictions resolved; 86 parameters with literature defaults; 6 new conditions |
| Domain Translator Brief | Domain Translator | 9 analogies, 3 sub-problems | Complementary filter, factor graph, gerrymandering-resistant redistricting recommended |
| Commercial Viability | Commercial Viability Assessor | CONDITIONAL_ADVANCE | $550K-$700K (8-11% of C22 budget); BUILD; 5 blocking conditions |
| Adversarial Report | Adversarial Analyst | REJECT | Composition novelty challenged; arms race futility; lean alternative proposed |

---

## Assessment Council Evaluations

### Technical Feasibility Assessment

**Score: 3.5 / 5** (Feasible with significant R&D effort; moderate-to-current technology)

The refined architecture resolves all three contradictions identified at RESEARCH:

1. **PCM → Log-linear model**: Standard ecological correction (Ovaskainen et al. 2017). Closed-form computation preserves D-1 precomputed lookup. 16 params/channel (5 main + 10 interaction + 1 intercept). Within-neighborhood restriction eliminates hidden O(V²) term.

2. **Channel fusion → Two-phase Bayesian**: Bootstrap phase retains 3-of-4 quorum (no training data needed). Transitions to 4-node Bayesian network after 50 confirmed anomalies. Well-understood methodology. 8-12 parameters.

3. **Dual-baseline → OR with confirmation window**: 3-5 epoch adaptive confirmation, dual-trigger bypass. 6 parameters. Worst-case 5-hour latency acceptable for slow-ramp threat model.

**Adversarial rebuttal on technical impossibility:** The Adversarial Analyst's strongest technical argument is the dual-baseline Pareto frontier (§3.1). The council's OR-with-confirmation design does not eliminate the trade-off but selects a specific operating point with principled justification: catch slow-ramp (OR trigger sensitivity) while filtering false positives (confirmation window specificity). The Adversarial claim of "no good solution" is overstated — what exists is a trade-off with no *dominant* solution, which is the normal state of detection theory. Every IDS in production operates on a chosen ROC point.

**Remaining technical risks:**
- PCM convergence without formal proof (MF-2: EXP-3 simulation required at DESIGN)
- Fixed-baseline reconstructibility by adversary (MF-4: Red Team at DESIGN)
- Spectral clustering adversarial hardening (MF-7: game-theoretic analysis at DESIGN)
- 86-parameter calibration burden (mitigated by literature defaults; sensitivity analysis required)

---

### Novelty Assessment

**Score: 3.5 / 5** (Novel combination of known techniques with one genuinely novel component)

**PCM is the anchor:** The Permitted Correlation Model — computing expected inter-agent correlation from structural covariates and detecting only residual anomalies — has no direct precedent in multi-agent security. The Prior Art Report surveyed 24 sources across 5 categories and found no system that performs structural-covariate correction for inter-agent correlation in an adversarial context.

**Adversarial rebuttal on novelty:** The Adversarial Analyst's prior art destruction (§2) is technically accurate on individual components — each is indeed well-known. The "composition novelty defense fails" argument (§2.7) claims the pipeline produces no emergent properties. This is **partially valid**: the three tiers operate sequentially and their combined detection is approximately the union of individual capabilities. However, the Adversarial Analyst undervalues two genuine contributions:

1. **PCM structural correction** is not "Newman 2010 in a new coat." Newman's configuration model operates on a static network with degree-sequence correction only. PCM operates on a dynamic, multi-channel network with 5+ structural covariates, streaming incremental updates, and adversarial robustness requirements. The ecological analogy (Ovaskainen) is methodological, not identical — ecological systems are not adversarial.

2. **Cross-layer integration depth**: C35's integration with 7 AAS specifications is not merely "engineering." The cluster membership API that feeds C3, C5, C6, C8, C12, C17 creates a detection substrate that no individual component provides. The Adversarial Analyst's "lean alternative" (§7) using C17 + C12 + thresholds achieves ~60-70% detection capability but cannot provide the cluster membership API, PCM-corrected residuals, or epidemiological attribution that downstream specs reference.

**Net novelty assessment:** Score of 3.5 reflects genuine novelty in PCM (4.0-4.5 individually) diluted by well-known individual components (2.0-2.5 each) in a composition that provides meaningful but not transformative emergent value.

---

### Impact Assessment

**Score: 4.0 / 5** (High internal impact — critical infrastructure for AAS platform)

C35 is referenced by 10+ existing specifications as critical infrastructure:
- C12 AVAP explicitly references "Layer 1: Sentinel Graph" as its detection substrate
- C3 scheduling, C5 verification, C8 settlement all require anomaly detection for integrity
- C14 AiBC governance, C17 MCSD Sybil defense need cluster membership data

**Without C35**, the AAS platform operates with fragmented, per-spec anomaly detection. The Commercial Viability Report estimates 60-70% detection degradation and flags a likely CRITICAL finding at Wave 4 security audit.

**The Adversarial Analyst's lean alternative** (C17 + C12 + thresholds at $50K-$100K) provides basic detection but:
- Cannot provide PCM-corrected residuals (every correlated agent pair triggers alerts)
- Cannot provide epidemiological attribution (no causal traceback)
- Cannot provide the cluster membership API (downstream specs lose their referenced interface)
- Creates technical debt that C35 would eventually need to replace

The lean alternative is appropriate as a **stopgap** if C35 is delayed, not as a permanent replacement.

---

### Arbiter Synthesis

**Risk Score: 5 / 10 (MEDIUM)**

Risk factors:
- PCM calibration uncertainty (no convergence proof): +2
- 86-parameter tuning burden: +1
- 7-spec integration complexity: +1.5
- Adversarial spectral clustering vulnerability: +1
- Mitigated by: literature defaults (-0.5), phased rollout (-0.5), existing C17/C12 infrastructure (-0.5)

**Adversarial case assessment:** The Adversarial Analyst presents a competent destruction case. The strongest arguments are:
1. **Arms race futility (§4)** — the adversary-always-adapts argument is philosophically valid but applies equally to ALL detection systems. If accepted, it would prevent building any security infrastructure. The correct response is defense-in-depth with acceptable cost, which C35 provides.
2. **Integration death march (§6)** — 12+ integration points across 7 specs is genuinely concerning. Mitigated by C9's existing contract framework and C22's wave structure, but schedule risk is real.
3. **Lean alternative (§7)** — legitimate as a stopgap. The council should treat this as the "C35 fails" fallback plan, not as a reason to reject C35.

The Adversarial case for REJECT is **not sustained**. The arguments are valid as risk factors but do not individually or collectively rise to the level of rejection. The "lean alternative" should be documented as the contingency plan.

---

## FEASIBILITY_VERDICT

### Decision: CONDITIONAL_ADVANCE

C35 advances to **DESIGN** with the following conditions:

### Blocking Conditions (must be resolved before DESIGN completion)

| ID | Condition | Source | Priority |
|----|-----------|--------|----------|
| FC-1 | PCM convergence simulation: demonstrate calibration convergence within 1000 epochs for systems of 1K, 10K, and 100K agents using the log-linear model | Science Assessment SA-2, MF-2 | P0 — BLOCKING |
| FC-2 | Dual-baseline fusion specification: formally specify the OR-with-confirmation rule including confirmation window parameters, dual-trigger bypass threshold, and expected FAR/FRR at each operating point | Science Assessment SA-1, Council C-3 | P0 — BLOCKING |
| FC-3 | Red Team fixed-baseline evaluation: demonstrate whether adversary with partial observability can reconstruct fixed baseline parameters, and specify mitigation if yes | MF-4 | P1 — BLOCKING |
| FC-4 | Budget allocation: confirm $550K-$700K within C22 Wave 3-5 parallel track without displacing C11/C12/C13 | Commercial Viability CC-4 | P1 — BLOCKING |
| FC-5 | Spectral clustering adversarial analysis: game-theoretic analysis of adversary cost vs. detection benefit for NMI divergence check | MF-7 | P2 — should be resolved by mid-DESIGN review |

### Carried Conditions from Ideation

| ID | Condition | Status |
|----|-----------|--------|
| C-1 | Tier 2 emits raw + residual values (auditability) | CARRIED |
| C-2 | PCM includes "unmodeled correlation" category at reduced severity | CARRIED |
| C-3 | PCM coverage fallback to raw below 0.70 threshold | CARRIED |
| D-1 | PCM is precomputed lookup, refreshed at CONSOLIDATION_CYCLE | CARRIED (log-linear preserves this) |

### New Conditions from Feasibility

| ID | Condition | Source |
|----|-----------|--------|
| C-4 | Log-linear PCM with pairwise interaction terms (16 params/channel) | Council resolution of Contradiction C-1 |
| C-5 | Two-phase channel fusion: quorum bootstrap → Bayesian network | Council resolution of Contradiction C-2 |
| C-6 | OR-with-confirmation dual-baseline fusion (3-5 epoch adaptive window) | Council resolution of Contradiction C-3 |
| C-7 | Dual-graph NMI divergence check for spectral clustering hardening | Systems Thinker proposal, accepted by council |
| C-8 | Within-neighborhood-only PCM computation (no global pairs) | SA-6 scaling finding |
| C-9 | Lean alternative (C17 + C12 + thresholds) documented as contingency plan | Adversarial Analyst §7 |

### Active Monitoring Flags

| Flag | Status | Next Gate |
|------|--------|-----------|
| MF-2 | OPEN — PCM convergence bounds | FC-1 resolves at DESIGN |
| MF-4 | OPEN — Fixed-baseline reconstructibility | FC-3 resolves at DESIGN |
| MF-5 | NEW — PCM residual calibration bias | DESIGN |
| MF-6 | NEW — Bayesian network sample size | DESIGN |
| MF-7 | NEW — Adversarial spectral clustering game theory | FC-5 resolves at mid-DESIGN |

### Updated Scores

| Dimension | IDEATION Score | FEASIBILITY Score | Change | Justification |
|-----------|---------------|-------------------|--------|---------------|
| Novelty | 3.5-4.0 | **3.5** | Confirmed | PCM genuinely novel; composition value confirmed but not transformative |
| Feasibility | 4.0 | **3.5** | -0.5 | Log-linear PCM + Bayesian fusion + 86 parameters increase complexity |
| Impact | — | **4.0** | New | Critical infrastructure for 10+ specs; platform security depends on it |
| Risk | — | **5/10 MEDIUM** | New | PCM calibration uncertainty + integration complexity + adversarial surface |

---

## Director's Note

C35 has passed FEASIBILITY with CONDITIONAL_ADVANCE. The invention is sound, novel in its PCM contribution, and critical to AAS platform security. The Adversarial Analyst's case, while vigorous, does not sustain rejection — the arguments are valid risk factors already captured in conditions and monitoring flags.

The refined architecture (log-linear PCM, two-phase Bayesian fusion, OR-with-confirmation baselines, NMI-hardened spectral clustering) is stronger than the original IC-2+ concept. The research phase successfully identified and the council successfully resolved three design contradictions.

**Next stage: DESIGN** (Steps 19-25 per §6). The Architecture Designer should begin with FC-1 (PCM convergence simulation) as the critical-path deliverable, since all Tier 2 design decisions depend on validated PCM behavior.

**Contingency:** If FC-1 fails (PCM does not converge within 1000 epochs at scale), invoke C-9 (lean alternative) and consider whether PCM can be replaced with simpler structural correction (e.g., degree-sequence-only residual, reducing back toward Newman 2010). This would reduce novelty but preserve Tier 1 and Tier 3 value.
