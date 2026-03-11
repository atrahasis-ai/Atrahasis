# C19 — Temporal Trajectory Comparison — ASSESSMENT

**Invention ID:** C19
**Stage:** ASSESSMENT (Final Gate)
**Date:** 2026-03-11
**Selected Concept:** C19-C+ (Hybrid DTW-DVC with Per-Modality Drift Decomposition)

---

# PART 1 — SPECIALIST ASSESSOR REPORTS

## 1.1 Technical Feasibility Assessor

**Score: 4.5/5**

C19 is highly feasible. Every component is built from established techniques:

- **Monthly snapshot extraction:** Arithmetic mean of BFE vectors already computed by C17. No new feature extraction. O(n) per agent per month.
- **Population-mean de-trending:** Trimmed mean, a standard robust statistic. O(n) per month across agents.
- **Drift direction comparison:** Cosine similarity on difference vectors — first-year linear algebra.
- **DTW with Sakoe-Chiba band:** 46-year-old algorithm with mature implementations in every scientific computing library (scipy, tslearn, dtw-python). Banded variant is O(n*w) — effectively linear.
- **Multi-task consistency (rho_Traj):** Coefficient of variation — basic descriptive statistics.

The only technical concern is the per-task-category trajectory data sparsity (Pre-Mortem F-03). Some categories may have too few VTDs per month for reliable per-category snapshots. The minimum 2-VTD-per-category and 3-of-7 category requirements are conservative solutions. This is a data availability issue, not a technical one.

Computational cost is negligible: < 1% addition to C17's compute budget (validated in RESEARCH Section 3.2 with concrete estimates). No new infrastructure is required — C19 runs within AiSIA's existing B computation pipeline.

**Assessment:** No technical risks. This is the most straightforward invention in the AAS pipeline — a clean extension to an existing system using established methods.

## 1.2 Novelty Assessor

**Score: 3.0/5 — Novel Application of Known Techniques**

**Novel elements:**
1. **Population-mean de-trending for Sybil detection.** Subtracting systematic environmental drift to isolate idiosyncratic agent-level drift correlation is not found in any prior Sybil detection system or behavioral biometric system.
2. **Dual drift comparison (direction + shape).** Combining cosine similarity on displacement vectors with DTW on trajectory shape addresses two orthogonal aspects of drift correlation — a design choice not present in prior time series comparison literature (which typically uses one or the other).
3. **Absolute cosine similarity for anti-correlated drift detection.** The insight that anti-correlated drift is as suspicious as correlated drift (both indicate a shared cause) is novel in the behavioral fingerprinting context.
4. **Multi-task trajectory consistency.** Extending cross-task consistency gating from point-in-time to longitudinal comparison.

**Known elements:**
- DTW (1978), Sakoe-Chiba band (1978)
- Cosine similarity on difference vectors (standard)
- Trimmed mean (standard robust statistics)
- Concept drift detection (ADWIN, DDM — established ML monitoring)
- Factor model de-trending (established in finance)

**Prior art clearance:** No existing system performs population-de-trended, multi-modal temporal trajectory comparison for AI agent Sybil detection. Individual components are well-established. The novelty is in the combination and application.

**Score justification:** 3.0 (not 3.5) because C19 is an incremental extension to C17 rather than a new system. The core innovation (correlated drift reveals shared origin) was already identified in C17 FEASIBILITY Attack 4 — C19 operationalizes it.

## 1.3 Impact Assessor

**Score: 3.5/5 — Moderate-High Impact Within Architecture**

**Direct impact:**
- Closes the gradual behavioral drift gap identified in C17 FEASIBILITY Attack 4
- Resolves C17 OQ-05 (model upgrade handling) via discontinuity detection
- Adds a genuinely orthogonal detection signal — trajectory correlation provides information that point-in-time comparison cannot

**Impact boundary:**
- The trajectory modality activates only at Phase 2 (month 18+) for agents with 6+ months history. It provides no value in Phase 0-1.
- Weight is moderate (0.14) — trajectory alone cannot produce a FLAG. It contributes to but does not dominate the B score.
- Detection value depends on the assumption that same-origin agents receive correlated updates. If an adversary uses decorrelated updates, trajectory adds nothing (but costs the adversary).

**Systemic impact:**
- The population-mean de-trending framework is a reusable infrastructure component. If future AAS inventions need to compare agent behavioral changes over time (e.g., quality monitoring, capability tracking), the MBS + de-trending pipeline is available.
- Discontinuity detection provides the first formal mechanism for handling model architecture changes in the AAS system — relevant beyond Sybil detection.

**Score justification:** 3.5 (not 4.0) because the trajectory modality is supplementary and Phase 2-only. It does not fill a blocking gap (C17 was approved without it). Its value is incremental improvement in detection of a specific, sophisticated attack.

## 1.4 Specification Completeness Assessor

**Score: 4.5/5 — Highly Complete**

**Complete:**
- Full algorithm specification: snapshot extraction, de-trending, direction comparison, DTW configuration, fusion, multi-task consistency (Sections 3-8)
- B formula integration with explicit weight tables and activation/deactivation logic (Section 9)
- Discontinuity detection and trajectory reset protocol (Section 10)
- Drift anomaly detection (suppression + magnitude) (Section 11)
- Trajectory explanation format for WATCH/FLAG reports (Section 12)
- Phased deployment with shadow mode and activation criteria (Section 13)
- 10 anti-gaming defenses (Section 14)
- 18 functional requirements + 4 non-functional requirements (Section 15)
- 14 governed parameters with ranges (Section 16)
- 3 patent-style claims (Section 17)
- Risk register with 6 risks (Section 18)
- Complete C17 modification summary (Section 19)

**Minor gaps:**
1. No explicit specification of how trajectory data feeds into the Phase 2 contrastive model training. The MTS mentions d_Traj and rho_Traj as input dimensions but does not specify training pair generation from trajectory data.
2. The interaction between trajectory comparison and the known-independent whitelist (C17 Section 10.3) is not explicitly addressed — are whitelisted pairs excluded from trajectory comparison, or only from FLAG decisions?
3. No formal specification of the model-family-specific de-trending fallback mentioned in Risk C19-R-01. This is described as a mitigation but not specified.

**Assessment:** These gaps are operational details that can be resolved during integration. The specification is more than sufficient for Phase 2 implementation.

## 1.5 Commercial Viability Assessor

**Score: 4.0/5 — Viable as Infrastructure Extension**

C19 is not a revenue-generating invention. It is a defensive infrastructure extension to C17 that incrementally improves Sybil detection for long-lived agents. Its commercial viability is measured by cost-effectiveness.

**Cost analysis:**
- Compute: < 1% addition to C17 budget. Negligible.
- Storage: ~8 GB at Phase 3 for 24-month MBS retention. Negligible.
- Engineering: Primary cost is implementation and integration with C17. Estimated at < 0.5 FTE for initial implementation, negligible ongoing maintenance (MBS extraction and trajectory comparison are automated).

**Value proposition:**
- Closes a specific attack vector at minimal cost
- Reusable infrastructure (MBS pipeline, de-trending framework)
- No adoption barriers beyond C17 (no new data collection, no new agent obligations)

**Score justification:** 4.0 (higher than C17's 3.5) because C19 has lower cost and cleaner integration than C17 itself. It is a focused, low-cost extension.

---

# PART 2 — ADVERSARIAL ANALYST (Final Report)

The FEASIBILITY stage tested 10 attacks comprehensively. Results: 0 fatal, 0 HIGH, 3 MEDIUM, 7 LOW. The DESIGN stage addressed all findings.

**Remaining concerns after DESIGN:**

| # | Concern | Severity | Status |
|---|---------|----------|--------|
| AA-1 | Noise injection into drift (Attack 3, MEDIUM) | LOW-MEDIUM | Mitigated by multi-month averaging, drift magnitude anomaly detection, and PCVM quality monitoring. Residual: sophisticated adversary can inject modality-specific noise at significant cost. |
| AA-2 | Population-mean drift mimicry (Attack 4, MEDIUM) | LOW-MEDIUM | Mitigated by drift suppression detection, quarterly-only publication of population statistics, per-task-category deconfounding. Residual: adversary with real-time population intelligence (unlikely given info asymmetry) could match population mean. |
| AA-3 | Boiling-frog decorrelation (Attack 7, MEDIUM) | MEDIUM | Partially mitigated by rolling window and WATCH persistence. Residual: patient adversary (12+ months of sustained decorrelation) can exit detection. This is an inherent limitation of finite-memory longitudinal comparison, not a C19 design flaw. |

**New concerns identified during DESIGN/SPECIFICATION:**

| # | Concern | Severity | Status |
|---|---------|----------|--------|
| AA-4 | Homogeneous population de-trending failure (Pre-Mortem F-01) | LOW-MEDIUM | If > 80% of agents share 2-3 model families, population mean captures most drift, leaving little idiosyncratic signal. Mitigation: monitor idiosyncratic/total ratio; model-family-specific de-trending fallback. |
| AA-5 | Trajectory modality as false-positive amplifier | LOW | A legitimate agent pair with coincidentally correlated drift (same model family, updated at similar times by different creators) could see B increase from borderline-WATCH to FLAG. Mitigation: trajectory weight (0.14) is too low to push B above theta_B alone; multi-task consistency gating suppresses coincidental single-category correlation. |

**Adversarial Analyst Verdict:** No new fatal or HIGH-severity concerns beyond FEASIBILITY. The trajectory modality is a sound defensive addition that raises the bar for gradual-drift evasion at negligible cost. **ADVANCE.**

---

# PART 3 — ASSESSMENT COUNCIL

## 3.1 Advocate

C19 is the simplest, most cost-effective invention in the AAS pipeline. It fills a specific, identified gap (C17 Attack 4) using established techniques (DTW, cosine similarity, trimmed means) at negligible computational cost (< 1% of C17 budget). The specification is clean, well-integrated with C17, and resolves an open question (OQ-05) that C17 left unaddressed.

Key merits:
- **Orthogonal signal.** Trajectory correlation provides information that point-in-time comparison fundamentally cannot. Two agents with different current profiles but correlated drift are invisible to C17 but visible to C19.
- **Population-mean de-trending is essential.** Without it, model-family systematic drift would produce massive false positives. C19's trimmed-mean approach is simple, effective, and reusable.
- **The hybrid direction + shape design is principled.** Direction captures the core insight; DTW handles temporal misalignment. Neither alone is sufficient.
- **Discontinuity detection is a bonus.** C17 OQ-05 had no answer. C19 provides one: detect, split, reset. Clean.
- **No new burden on agents.** C19 uses data already collected by C17 (Behavioral VTDs). No new SEB tasks, no new data collection, no new agent obligations.

C19 should be approved. It improves the defense with minimal cost and risk.

## 3.2 Skeptic

C19 is competent but three concerns deserve acknowledgment:

1. **The core assumption is unvalidated.** C19 rests on the claim that "agents from the same creator tend to drift in similar directions when updated." This is plausible but has no empirical evidence in the AI agent domain. If creators update agents with different task-specific fine-tuning, drift could be uncorrelated even for same-origin agents. The trajectory modality would then add noise (false negatives) without improving detection.

2. **Phase 2 activation delay limits value.** The trajectory modality provides no value until Phase 2 (month 18+), and then only for agents with 6+ months of history. In practice, this means trajectory comparison is useful only for agents that have been in the system for 24+ months. If an adversary operates Sybils for < 2 years, trajectory never activates.

3. **DTW may be unnecessary complexity.** The DESIGN stage acknowledged that drift direction alone might achieve similar detection rates. The DTW component adds configuration complexity (step pattern, band width, normalization, missing data handling) for uncertain marginal benefit. The specification wisely includes a governance mechanism to disable DTW, but perhaps it should start disabled (direction-only) and enable DTW only if empirical data shows it adds value.

These concerns are not blocking. C19 is a Phase 2 extension with moderate weight — its downside is limited.

## 3.3 Arbiter

The Advocate's case is strong. C19 is a focused, low-cost extension that addresses an identified gap. The Skeptic raises legitimate concerns, none of which are architectural:

1. **Unvalidated assumption:** Valid. This is inherent to any pre-deployment specification. The shadow deployment period (Phase 2, months 18-24) explicitly validates the assumption before active deployment. If correlated drift is not observed in shadow data, the trajectory modality is not activated.

2. **Activation delay:** Correct, and by design. The trajectory modality is supplementary — it adds value for long-lived agents, which are the most valuable (longest governance participation, highest AIC stake). Short-lived Sybils are better caught by point-in-time comparison and Layer 1 economics.

3. **DTW complexity:** The Skeptic's suggestion to start direction-only is reasonable but the specification already includes the governance mechanism to disable DTW (Section 7.3). Starting with the hybrid and disabling DTW if it underperforms is safer than starting without DTW and missing temporal misalignment effects during the critical Phase 2 validation period. The marginal complexity is small.

**Verdict:**

```json
{
  "type": "ASSESSMENT_COUNCIL_VERDICT",
  "invention_id": "C19",
  "stage": "ASSESSMENT",
  "decision": "APPROVE",
  "scores": {
    "technical_feasibility": 4.5,
    "novelty": 3.0,
    "impact": 3.5,
    "specification_completeness": 4.5,
    "commercial_viability": 4.0,
    "weighted_average": 3.9
  },
  "risk_score": 3,
  "risk_level": "LOW-MEDIUM",
  "monitoring_flags": [
    "MF-1: Validate correlated-drift assumption during Phase 2 shadow period. If < 30% of known same-origin pairs show trajectory cosine > 0.5, do not activate trajectory modality.",
    "MF-2: Monitor population-mean de-trending effectiveness. If idiosyncratic drift magnitude < 20% of total drift for > 50% of agents, evaluate model-family-specific de-trending.",
    "MF-3: Evaluate DTW marginal value during shadow period. If DTW adds < 5% AUROC improvement over direction-only, set beta=1.0 via governance.",
    "MF-4: Monitor trajectory false positive rate in isolation. Target: < 0.05% FPR for trajectory modality alone."
  ],
  "operational_conditions": [
    "OC-1: Shadow deployment (trajectory computed but not contributing to B) MUST precede active deployment by >= 6 months.",
    "OC-2: Activation requires AiSIA recommendation with empirical analysis + Stiftung board ratification."
  ],
  "pivot_direction": null,
  "rationale": "C19 is a focused, technically sound extension to C17 that adds a genuinely orthogonal detection signal (correlated behavioral drift over time) at negligible cost. The hybrid DTW-DVC architecture with population-mean de-trending is well-grounded in established techniques. Risk is LOW-MEDIUM (3/10) — the lowest in the AAS pipeline — because the trajectory modality is supplementary (w=0.14), Phase 2-only, and has a mandatory shadow period before activation. The 10-attack adversarial analysis produced 0 fatal, 0 HIGH vulnerabilities. Two operational conditions ensure empirical validation before deployment. APPROVE."
}
```

---

# PART 4 — PIPELINE SUMMARY

## Pipeline Results

| Stage | Date | Verdict | Key Output |
|-------|------|---------|------------|
| IDEATION | 2026-03-11 | 3 concepts generated, C19-C+ selected | Hybrid DTW-DVC with per-modality drift decomposition |
| RESEARCH | 2026-03-11 | DTW validated, novelty 3.0 | DTW appropriate with hybrid; computational cost negligible |
| FEASIBILITY | 2026-03-11 | ADVANCE (clean) | Risk 3/10 LOW-MEDIUM. 10 attacks: 0 fatal, 0 HIGH, 3 MEDIUM, 7 LOW |
| DESIGN | 2026-03-11 | 10 design actions completed | Full specification: MBS, de-trending, DTW config, direction comparison, fusion, rho_Traj |
| SPECIFICATION | 2026-03-11 | C19-MTS-v1.0 (~600 lines) | Complete temporal trajectory modality specification |
| **ASSESSMENT** | **2026-03-11** | **APPROVE** | **Scores: TF 4.5, N 3.0, I 3.5, SC 4.5, CV 4.0. Risk 3/10. 4 monitoring flags, 2 operational conditions.** |

## What C19 Adds to the Architecture

| Component | Before C19 | After C19 |
|-----------|-----------|-----------|
| C17 Section 11 | 0.5-page placeholder: "DTW on monthly BFE snapshots" | Full specification: hybrid DTW-DVC, population de-trending, multi-task consistency, discontinuity detection |
| C17 B formula (Phase 2) | 5 modalities, w_Traj=0.14 placeholder | 6 modalities, w_Traj=0.14 validated, complete fusion formula |
| C17 OQ-05 | OPEN: "How to handle model upgrades?" | **RESOLVED**: Discontinuity detection + trajectory reset |
| C17 MF-5 | OPEN: "Evaluate trajectory for Phase 2" | **RESOLVED**: Full evaluation, specification, and approval |
| Detection coverage | Point-in-time behavioral similarity | + Longitudinal correlated drift detection |
| Data pipeline | Behavioral VTDs (12-month retention) | + Monthly Behavioral Snapshots (24-month retention) |

## Remaining Open Questions

| ID | Question | Priority | Owner |
|----|----------|----------|-------|
| C19-OQ-1 | Empirical validation of correlated-drift assumption (do same-origin agents actually drift together?) | P0 | AiSIA (Phase 2 shadow) |
| C19-OQ-2 | Model-family-specific de-trending specification (fallback if population is too homogeneous) | P2 | AiSIA |
| C19-OQ-3 | Trajectory data integration into contrastive model training pipeline | P2 | AiSIA ML team |

---

**End of ASSESSMENT Stage**

**Status:** ASSESSMENT COMPLETE — PIPELINE COMPLETE
**Decision:** APPROVE with 4 monitoring flags and 2 operational conditions
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Temporal Trajectory Comparison\C19_ASSESSMENT.md`
