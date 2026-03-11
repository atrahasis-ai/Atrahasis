# C20 — Contrastive Model Training Bias Framework — ASSESSMENT

**Invention ID:** C20
**Stage:** ASSESSMENT (Final Gate)
**Date:** 2026-03-11
**Selected Concept:** C20-A (Contrastive Model Training Bias Framework — CMTBF)

---

# PART 1 — SPECIALIST ASSESSOR REPORTS

## 1.1 Technical Feasibility Assessor

**Score: 4.0/5**

CMTBF is technically feasible using established methods. Every component maps to known, proven technology:

- **Pre-training distribution analysis:** Simpson's diversity index, chi-square distribution tests, schema validation — standard statistical methods with mature implementations.
- **Spectral signature analysis:** SVD + DBSCAN clustering — both well-understood and available in standard scientific computing libraries (scikit-learn, SciPy).
- **Influence function computation:** Kong & Chaudhuri (2022) demonstrate feasibility for contrastive learning models. For C17's MLP (~600K parameters, ~5,500 training pairs), the computation requires ~3.3 billion operations — feasible in minutes on a single GPU.
- **Per-family FPR/FNR validation:** Standard classification metrics computed on stratified subsets. No computational challenges.
- **Embedding space monitoring:** Variance and silhouette computations on 128-dimensional embeddings. Trivial overhead.

**Challenges:**
- Influence screening at Phase 3+ scale (50,000+ training pairs) may require aggressive sampling (10-20%). The approximation quality of LiSSA at low sampling rates needs empirical validation.
- Spectral signature analysis assumes poisoned data clusters in singular value space. Distributed poisoning attacks that spread uniformly across the spectrum are undetectable by this method alone. Defense depth (influence + golden holdout) provides secondary coverage.

**Assessment:** No technical risks that would block implementation. The hardest component (influence functions) has published feasibility evidence for the specific model architecture.

## 1.2 Novelty Assessor

**Score: 3.0/5 — Novel Combination of Known Techniques**

**Novel elements:**
1. **Domain-specific bias taxonomy for behavioral trace contrastive learning:** No existing framework defines the 6 bias dimensions (BD-1 through BD-6) specific to training a contrastive model on AI agent behavioral traces. The taxonomy itself is a contribution.
2. **Label traceability chain:** Requiring multi-source behavioral confirmation for positive pair labels, with provenance tracking and conflict rejection, is novel in the contrastive learning context. Existing data validation frameworks do not address adversarial label provenance.
3. **Golden holdout regression testing for feedback loop defense:** While holdout testing is standard, using a fixed golden set specifically to detect feedback loop degradation in a security-critical adversarial retraining cycle is a novel application.

**Known elements:**
- Fairness metrics (disparate impact, equalized odds) — well-established
- Spectral anomaly detection — established (Tran et al., 2018)
- Influence functions for ML — established (Koh & Liang, 2017)
- Contrastive learning fairness — established (Park et al., 2022)
- Data validation pipelines — established (TFDV, Great Expectations)

**Prior art clearance:** Park et al. (2022) is the closest prior art. C20 differentiates by: (a) operating on behavioral traces rather than image/text, (b) addressing adversarial label poisoning, (c) defining a complete 3-layer pipeline rather than a loss function modification, (d) including governance integration (TDQR, threshold governance).

**Assessment:** This is a well-executed application of known techniques to a novel domain with domain-specific contributions. Score 3 is appropriate — novel combination, not breakthrough.

## 1.3 Impact Assessor

**Score: 3.5/5 — High Impact Within C17 Scope**

**Direct impact:**
- Resolves C17 Monitoring Flag 3, removing a documented risk to Phase 2 contrastive model deployment.
- Operationalizes C17's existing bias monitoring requirements (Section 12.3) by specifying HOW to achieve per-family FPR compliance and model governance.
- Provides a concrete fallback mechanism (statistical-only B) when bias validation fails, preventing premature deployment of a biased model.

**Systemic impact:**
- The TDQR framework establishes a reusable audit pattern for any future Atrahasis ML component.
- The label traceability chain and golden holdout regression patterns can be applied to other adversarial ML settings within the system.
- The bias taxonomy provides a checklist for evaluating bias in any behavioral analysis system.

**Limitations:**
- C20 is infrastructure for C17 Phase 2 — it does not independently produce value. Its impact is bounded by C17's deployment success.
- At Phase 2 entry (~1,000 agents, 5,500 training pairs), the framework may be over-specified for the actual scale. Its full value is realized at Phase 3+ (10,000+ agents).

## 1.4 Specification Completeness Assessor

**Score: 4.0/5 — Complete with Minor Gaps**

**Complete:**
- Bias taxonomy: all 6 dimensions defined with detection methods, mitigation strategies, and implementation phasing
- Layer 1 (Pre-Training): schema, label provenance, distribution analysis, anomaly detection, DQS formula
- Layer 2 (Intra-Training): embedding monitoring, per-family loss, TQS formula
- Layer 3 (Post-Training): per-family FPR/FNR, temporal holdout, golden holdout, adversarial probe, DRS formula
- TDQR: structure specified, retention requirements, governance integration
- Integration with C17: pipeline positioning, requirement operationalization
- Adversarial defenses: 10 attacks analyzed with defenses and residual risk
- Parameters: 15 governance-controlled parameters with ranges
- Formal requirements: 20 functional + 4 non-functional requirements

**Minor gaps:**
- No specification for how model family is determined when agents do not self-report (metadata field allows UNKNOWN). The framework assumes model family labels are available but does not specify a family inference algorithm.
- No specification for the adversarial probe creation process — who creates the 50 synthetic adversarial pairs, and how is their diversity ensured? This is an operational detail but affects test quality.
- The interaction between C20's golden holdout AUROC >= 0.95 and C17's FR-17 AUROC >= 0.95 on the held-out validation set is not explicitly reconciled — are these the same test or different? They should be different (golden holdout is fixed; FR-17 validation set rotates with training data).
- No specification for how DQS component weights (0.25, 0.25, 0.20, 0.20, 0.10) were determined or whether they should be governance-adjustable.

**Assessment:** Specification is sufficient for implementation. Gaps are operational details that can be resolved during integration without architectural changes. The golden holdout vs. FR-17 distinction should be clarified in a future addendum.

## 1.5 Commercial Viability Assessor

**Score: 3.5/5 — Viable as Internal Infrastructure**

C20 is not revenue-generating. It is a quality assurance framework that protects the integrity of C17's Phase 2 contrastive model.

**Cost analysis:**
- Development: 2-3 person-months of ML engineering
- Per-retraining-cycle: 8 GPU-hours maximum (influence screening is the main cost)
- TDQR production: 1 person-day per quarter
- Annual red team targeting validation pipeline: included in C17's existing red team budget

**Value protection:**
- A biased contrastive model would produce either: (a) false positive governance harm (innocent agents flagged), triggering Constitutional Tribunal challenges costing far more than C20's overhead, or (b) false negative security harm (Sybils evading detection), undermining MCSD Layer 2's entire purpose.
- C20's cost is negligible compared to the governance and security costs of deploying a biased model.

**Adoption:** Mandatory internal infrastructure — no adoption barrier.

---

# PART 2 — ADVERSARIAL ANALYST FINAL REPORT

## The Case for Abandonment

**Prior art destruction:** Park et al. (2022) "Fairness-aware Contrastive Learning" already provides the mathematical framework for subgroup-fair contrastive learning. C20's per-family FPR/FNR validation and loss decomposition are direct applications of this prior art. The label traceability chain and golden holdout are sound engineering practices, not novel inventions. C20 is competent engineering, not invention.

**Technical concern:** The influence function screening (the most technically sophisticated component) may not provide actionable information at Phase 2 scale. With 5,500 training pairs and a 3-layer MLP, the model is simple enough that standard validation metrics (AUROC, per-family FPR) already capture most quality issues. Influence functions add complexity without proportional benefit at this scale. Their value emerges only at Phase 3+ (50,000+ pairs), by which time the framework may need redesign anyway.

**Commercial concern:** C20 adds validation overhead to a process that may already be adequately gated by C17's existing requirements (AUROC >= 0.95, per-family FPR <= 2x, automatic rollback). The incremental value of C20 over C17's built-in governance is uncertain.

**The case:** C20 is a reasonable quality assurance framework, but it is over-specified for Phase 2 and under-novel for a standalone invention. It would be better integrated as an addendum to C17 (a "Section 12.5: Training Data Validation Protocol") rather than a separate Master Tech Spec.

**Counter to the case:** The Adversarial Analyst's argument treats C20 as overkill because C17 already has some bias monitoring. But C17's monitoring is limited to 2 checks (AUROC >= 0.95 and per-family FPR <= 2x). C20 provides the complete framework that makes these checks meaningful: the label provenance chain, the distribution analysis, the golden holdout regression, and the TDQR audit trail. Without C20, C17's bias monitoring is a pair of metrics without a methodology. Furthermore, the adversarial bias dimension (BD-6) — including the label traceability chain and spectral/influence analysis — addresses a genuine attack surface that C17 does not consider at all.

---

# PART 3 — ASSESSMENT COUNCIL

## 3.1 Advocate

C20 resolves a documented monitoring flag (C17 MF-3) with a comprehensive, implementable framework. The 6-dimension bias taxonomy is domain-specific and not available from any existing tool or framework. The label traceability chain directly addresses the training pipeline as an attack surface — a genuine security concern that C17 acknowledges but does not solve. The phased deployment aligns with C17's own phasing. The fallback mechanism (statistical-only B) ensures that C20 can never make things worse — it only gates deployment of improvements.

## 3.2 Skeptic

The Adversarial Analyst's point about specification as addendum vs. standalone MTS has merit. C20 is tightly coupled to C17 Section 12 and has no independent existence. Novelty score 3 is accurate — this is competent application of known techniques, not a breakthrough. The influence function component may be over-engineered for Phase 2 scale.

However: the Skeptic acknowledges that (a) the bias taxonomy is a genuine contribution, (b) the adversarial defenses address real attack vectors, and (c) the TDQR audit framework has systemic value beyond C17. The framework is worth specifying even if individual components are not novel.

## 3.3 Arbiter

**Verdict:** ADVANCE

C20 adequately resolves C17 Monitoring Flag 3. The framework is technically sound, implementable with proven components, and appropriately scoped. The novelty is at the "novel combination" level (score 3), which is appropriate for a validation framework. The phased deployment and fallback mechanisms demonstrate engineering maturity.

**Operational conditions:**
1. Clarify the distinction between C20's golden holdout AUROC test and C17 FR-17's held-out validation AUROC test in a future addendum or C17 patch.
2. Influence function screening is RECOMMENDED but not REQUIRED at Phase 2 entry (mandatory at Phase 2+).
3. DQS component weights (0.25/0.25/0.20/0.20/0.10) should be marked as governance-adjustable parameters.
4. Model family inference method (when agents do not self-report) should be specified in a future addendum or deferred to operational AiSIA protocol.
5. Adversarial probe creation process should be documented as an AiSIA operational procedure.

---

## Assessment Council Verdict

```json
{
  "type": "ASSESSMENT_COUNCIL_VERDICT",
  "invention_id": "C20",
  "stage": "ASSESSMENT",
  "decision": "ADVANCE",
  "novelty_score": 3,
  "feasibility_score": 4,
  "impact_score": 3.5,
  "risk_score": 4,
  "risk_level": "MEDIUM",
  "required_actions": [
    "Clarify golden holdout AUROC vs. C17 FR-17 AUROC distinction",
    "Mark DQS component weights as governance-adjustable parameters",
    "Document model family inference method for UNKNOWN-family agents",
    "Document adversarial probe creation process as AiSIA operational procedure"
  ],
  "monitoring_flags": [
    "Influence function screening may not provide proportional value at Phase 2 scale (5,500 pairs) — validate empirically",
    "Clean-label poisoning remains a residual risk with no complete defense",
    "Small-family validation gap (families with < 50 pairs) limits individual fairness guarantees"
  ],
  "pivot_direction": null,
  "rationale": "CMTBF is a sound, implementable framework that resolves C17 Monitoring Flag 3. It provides domain-specific bias detection and mitigation for contrastive learning on AI behavioral traces, with adversarial defenses against training data poisoning. Novelty is at the 'novel combination' level — individual techniques are known but the domain-specific taxonomy, label traceability chain, and integrated 3-layer validation pipeline are not covered by any existing framework. Phased deployment and automatic fallback to statistical-only B ensure the framework cannot degrade C17's existing capabilities."
}
```

---

**End of ASSESSMENT.**

**PIPELINE COMPLETE.**

**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Contrastive Model Bias\`
**Files produced:**
1. `C20_IDEATION.md` — PRE-IDEATION + Domain Translator + Ideation Council
2. `C20_RESEARCH_REPORT.md` — Prior art + Science assessment
3. `C20_FEASIBILITY.md` — Sub-problem analogies + Adversarial Analyst (10 attacks) + Feasibility verdict
4. `C20_DESIGN.md` — Architecture + Pre-Mortem + Simplification
5. `MASTER_TECH_SPEC.md` — C20-MTS-v1.0 (~560 lines)
6. `C20_ASSESSMENT.md` — 5 assessors + Adversarial Analyst + Assessment Council verdict
