# C5 PCVM — Assessment Report

**Invention:** C5 — Proof-Carrying Verification Membrane (PCVM)
**Document Under Review:** Master Technical Specification v1.0.0 (2026-03-10)
**Assessment Date:** 2026-03-10
**Assessors:** Simplification Agent, Completeness Reviewer
**Protocol:** Atrahasis Agent System v2.0, ASSESSMENT Stage

---

## Part 1: Simplification Agent Review

### 1.1 Overall Scores

| Metric | Score | Rationale |
|--------|-------|-----------|
| **Complexity** | **7/10** | The system has 9 components, 8 claim classes across 3 tiers, 3 Subjective Logic operators, 35+ configurable parameters, and integration contracts with 4 external systems. This is substantial but not gratuitous — each piece traces to a specific requirement. |
| **Achievability** | **5/10** | Four mandatory hard gates remain experimentally unvalidated. Subjective Logic domain transfer to epistemic claims is theoretically unproven. The 8-class taxonomy's reliability is an open question. An implementer could build the system from this spec, but whether it would actually work as designed depends on experimental outcomes that have not yet occurred. |

### 1.2 Per-Component Complexity Assessment

#### Component 1: VTD Engine (construct, validate, store VTDs)
- **Earns its complexity?** YES
- **Rationale:** The VTD common envelope + 8 class-specific proof body schemas are the core innovation. Each schema is well-motivated by the epistemic nature of the claim class. The schemas are detailed enough to implement directly from the spec.
- **Over-engineered elements:** None identified. The schemas are appropriately granular.

#### Component 2: Claim Classifier (three-way classification)
- **Earns its complexity?** YES
- **Rationale:** Three-way classification (agent suggestion + structural analysis + independent classifier) addresses the Class Downgrade attack (Attack 3). The conservatism ordering (H > N > E > S > R > P > C > D) is principled.
- **Over-engineered elements:** The structural analysis based on text markers (Section 5.3) is underspecified relative to the other two signals. It is unclear how reliable keyword-matching classification would be for distinguishing, say, E-class from S-class claims.
- **Simplification opportunity:** MEDIUM. Could start with two-way classification (agent + independent classifier) and add structural analysis later if needed.

#### Component 3: Verification Dispatcher
- **Earns its complexity?** YES
- **Rationale:** Routing claims to the correct tier-specific verifier is a straightforward dispatch pattern. The complexity is in the tier-specific protocols, not the dispatcher itself.

#### Component 4: Proof Checker (Tier 1)
- **Earns its complexity?** YES
- **Rationale:** Four proof types (RECOMPUTATION, HASH_VERIFICATION, PROOF_CERTIFICATE, PROOF_SKETCH) provide graduated verification depth for deterministic claims. This is where PCVM delivers genuine sublinear cost (0.1x-0.35x). Well-earned.

#### Component 5: Evidence Evaluator (Tier 2)
- **Earns its complexity?** PARTIALLY
- **Rationale:** The six-phase pipeline is sound (schema validation, completeness check, counter-evidence check, class-specific verification, dependency verification, adversarial probing decision). However, the E-class mandatory source verification protocol (four-level: URL accessibility, content hash, quote accuracy, contextual relevance) is ambitious. Level 4 (contextual relevance assessment) is essentially an LLM judgment call, which introduces the same non-determinism the system is trying to verify.
- **Over-engineered elements:** Level 4 source verification (contextual relevance) for E-class. The first three levels are mechanical and reliable; the fourth is a judgment that could itself require verification.
- **Simplification opportunity:** LOW-MEDIUM. Could make Level 4 optional and triggered only by adversarial probing.

#### Component 6: Attestation Reviewer (Tier 3)
- **Earns its complexity?** YES, with reservation
- **Rationale:** The Structured Disagreement Protocol (independent assessment, cross-review, synthesis, dissent recording) is well-designed for committee-based evaluation. The concern is cost: Tier 3 verification costs 1.0x-2.0x of replication. The spec is honest about this, which is commendable.
- **Reservation:** The Skeptic's critique from feasibility (Attack 9: Tier Collapse) remains relevant. For H-class and N-class, PCVM is delivering structured documentation, not proof-checking. This is valuable, but calling it a "verification membrane" overpromises.

#### Component 7: Adversarial Probing System
- **Earns its complexity?** YES
- **Rationale:** Five probe types matched to claim classes, VRF-based prober selection independent of committees, generative probe components, meta-probing for inoculation detection. This is one of PCVM's most novel contributions and is well-specified.
- **Over-engineered elements:** The meta-probe for pre-fabrication detection (suspicion score > 0.70) is conceptually valuable but operationally vague. How does one reliably detect that a response is "suspiciously convenient"? This is itself an LLM judgment.

#### Component 8: Credibility Engine (Subjective Logic)
- **Earns its complexity?** PARTIALLY
- **Rationale:** Subjective Logic opinion tuples (b, d, u, a) are a principled improvement over binary pass/fail. The three composition operators (conjunction, discounting, cumulative fusion) are well-defined with correct mathematical formulations — test vectors verify correctly. However, this is an unvalidated domain transfer: Subjective Logic was designed for trust networks, not epistemic claim verification. The spec acknowledges this (Open Question Q3).
- **Over-engineered elements:** The cyclic dependency handling with iterative dampening (alpha=0.85, epsilon=0.001) is theoretically sound but may be solving a problem that rarely occurs in practice. Dependency graphs in knowledge systems are typically acyclic.
- **Simplification opportunity:** LOW. The cyclic handler is a sensible fallback even if rarely triggered.

#### Component 9: Knowledge Admission Gate
- **Earns its complexity?** YES
- **Rationale:** MCT issuance, BDL persistence, contradiction handling, and re-verification scheduling are all necessary for integration with the Knowledge Cortex. The contradiction handling (both claims persist, contradiction edge recorded) is particularly well-designed — it avoids premature resolution.

### 1.3 Specific Findings

| # | Finding | Severity | Component |
|---|---------|----------|-----------|
| F1 | **Abstract claims 40-60% cost reduction, but Section 12.2 calculates 17% before trust propagation.** The 40-60% figure depends on downstream trust propagation (verified claims cited 3x on average avoid re-verification), which is an unvalidated assumption. The abstract should lead with the conservative 17% figure. | **HIGH** | Scalability Analysis |
| F2 | **C3 Tidal Noosphere specifies 5 claim classes; C5 specifies 8.** The expansion from 5 (Deterministic, Empirical, Statistical, Heuristic, Normative) to 8 (adding Process, Reasoning, Compliance) is justified by the epistemic matrix but creates an integration inconsistency. The C3 spec's verification membrane section will need updating. | **MEDIUM** | Claim Classification |
| F3 | **C4 ASV epistemic_class enum does not match C5 claim classes.** ASV uses: observation, correlation, causation, inference, prediction, prescription. PCVM uses: D, E, S, H, N, P, R, C. Section 10.5 specifies a mapping (CLM->Claim, PRV->VTD dependencies, MCT->VRF token) but does not specify how ASV epistemic_class maps to PCVM claim class. | **MEDIUM** | ASV Interface |
| F4 | **Structural classification (Section 5.3) is underspecified.** The pseudocode references `CLASSIFICATION_SIGNATURES[cls]` with `markers` and `exclusion` fields but does not define what these markers are for any of the 8 classes. An implementer cannot build the structural classifier without this information. | **HIGH** | Claim Classifier |
| F5 | **E-class source verification Level 4 (contextual relevance) introduces circular verification.** Assessing whether a source is contextually relevant to a claim requires the same kind of judgment the system is verifying. This creates a verification regress. | **MEDIUM** | Evidence Evaluator |
| F6 | **The "most conservative class" ordering (H > N > E > S > R > P > C > D) conflates conservatism with cost.** H-class is "most conservative" because it has the highest verification cost, but a claim misclassified as H that is actually D would receive weaker verification (attestation review instead of proof checking). Conservative should mean "strongest verification," not "most expensive." | **HIGH** | Claim Classifier |
| F7 | **Probe budget is measured in "tokens" (Section 7.5) but the spec does not define what a token is in this context.** Is this LLM tokens? Compute tokens? AIC tokens? The budgeting system cannot be implemented without this definition. | **MEDIUM** | Adversarial Probing |
| F8 | **Deep-audit statistical guarantee claims >99% detection within 65 epochs, but this assumes independent audits per epoch.** If an agent submits only one forged claim, the 7% rate means 0.07 probability per epoch. The math is correct (1-0.93^65 = 0.9911). But if an agent submits many claims per epoch, forged claims may be diluted by legitimate claims, and the detection probability per claim may be lower if there is a per-epoch cap on audits. | **LOW** | Deep-Audit |
| F9 | **35+ configurable parameters may create a parameter explosion for operators.** The spec does not specify default configurations or parameter profiles for different deployment scales. | **LOW** | Configuration |
| F10 | **The MCT schema includes `cls_id` as a required field but this identifier format is never defined.** The VTD has `vtd_id` with a defined pattern; the MCT has `mct_id` with a defined pattern; but `cls_id` has no pattern constraint. | **LOW** | Knowledge Admission |
| F11 | **The spec references "V-class operation pathway" (Section 10.1) from the Tidal Noosphere but does not define what V-class operations are.** An implementer would need to cross-reference the C3 spec. | **LOW** | Integration |
| F12 | **The cost model (Section 12.1) conflates VTD construction cost (borne by the producing agent) with VTD checking cost (borne by verifiers).** The "Total vs. Replication" column adds these, but they are paid by different actors. System-level cost analysis should separate producer and verifier costs.** | **MEDIUM** | Scalability |

### 1.4 Verdict

**APPROVE WITH RECOMMENDATIONS**

The Master Tech Spec demonstrates genuine architectural rigor. The graduated VTD model is intellectually honest, the Subjective Logic formalization is mathematically correct, the adversarial probing system is novel and well-specified, and the security analysis frankly acknowledges residual risks. The spec earns most of its complexity.

However, three findings require attention before implementation:

1. **F1 (HIGH):** The cost reduction claim in the abstract (40-60%) should be qualified as dependent on trust propagation assumptions, with the conservative 17% figure presented as the validated baseline.

2. **F4 (HIGH):** The structural classification signatures must be defined for all 8 classes, or the three-way classification protocol must be redesigned as two-way.

3. **F6 (HIGH):** The conservatism ordering must be reconsidered. When all three classifiers disagree, the resolution should favor the class with the STRONGEST verification requirements (lowest tier number), not the most expensive verification cost. The current ordering could result in deterministic claims being verified as heuristic attestations, which would be weaker verification.

### 1.5 Recommendations for Simplification

1. **Consider starting with 5 claim classes** (matching C3) and adding P, R, C classes in a later phase if the base system proves stable. The 8-class taxonomy is the single largest source of complexity and its reliability is an unvalidated hard gate (GATE-2).

2. **Make Level 4 E-class source verification (contextual relevance) a SHOULD, not a MUST.** The first three levels provide mechanical verification; the fourth introduces judgment that complicates the verification model.

3. **Define a "minimal viable PCVM" profile** that implements only Tier 1 (D, C classes) with proof checking. This provides immediate value and a fallback if Tier 2/3 VTDs fail the hard gates.

4. **Reduce configurable parameters** by establishing 3 deployment profiles (Pilot, Production, Planetary) with pre-set parameter values, rather than exposing 35+ individual knobs.

---

## Part 2: Completeness and Consistency Assessment

### 2.1 Completeness: 4/5

**Claim Class Coverage:**
- All 8 claim classes (D, E, S, H, N, P, R, C) are fully specified with: formal definitions (Section 5.2), VTD proof body JSON schemas (Appendix A), verification protocols (Section 6), and admission thresholds (Section 9.1). **COMPLETE.**

**Verification Protocol Coverage:**
- Tier 1 protocol: Fully specified with pseudocode for 4 proof types. **COMPLETE.**
- Tier 2 protocol: Six-phase pipeline specified. E-class source verification detailed. S-class, P-class, R-class verification described but with less algorithmic detail than E-class. **MOSTLY COMPLETE.**
- Tier 3 protocol: Structured Disagreement Protocol specified. **COMPLETE.**
- Deep-Audit: VRF selection, audit procedure, statistical guarantees specified. **COMPLETE.**

**Integration Interfaces:**
- Tidal Noosphere interface: Specified with epoch alignment, committee sizes, MQI response tiers. **COMPLETE.**
- Knowledge Cortex interface: Admission flow and query interface described. **MOSTLY COMPLETE** (no formal API schema).
- Settlement Plane interface: Quality weighting described. **ADEQUATE.**
- Sentinel Graph interface: MQI metrics listed. **COMPLETE.**
- ASV interface: Token mapping described. **INCOMPLETE** (no epistemic_class mapping, see F3).

**Gaps That Would Block Implementation:**
1. Classification signatures (F4) — blocks structural classifier implementation.
2. ASV epistemic_class to PCVM claim class mapping — blocks C4 integration.
3. Bootstrap protocol details — acknowledged as Open Question Q6.
4. S-class, P-class, R-class verification algorithms less detailed than E-class and D-class.

### 2.2 Consistency: 4/5

**Data Structure Consistency:**
- VTD common envelope schema is internally consistent. All required fields are defined.
- All 8 class-specific proof body schemas conform to the common envelope's `proof_body` field.
- MCT schema is consistent with VTD schema (references vtd_id, claim_id).
- The `cls_id` field in MCT is not defined elsewhere — minor inconsistency (F10).

**Protocol Flow Consistency:**
- Classification protocol (Section 5.3) correctly references INV-M2.
- Verification dispatch correctly routes by tier.
- Deep-audit protocol correctly references VRF selection and independent committees (INV-M3).
- Adversarial probing correctly references independent prober selection (INV-M3).
- The conservatism ordering issue (F6) creates a logical inconsistency between "conservative" and "strongest verification."

**Terminology Consistency:**
- "VTD" used consistently throughout (Verification Trace Document).
- "MCT" used consistently (Membrane Credibility Token).
- "CLS" (Classification Seal) is referenced in conformance requirements (D.1.14) but its schema is never defined. Minor gap.
- Claim class identifiers (D, E, S, H, N, P, R, C) used consistently.
- Opinion tuple notation (b, d, u, a) used consistently with Josang's conventions.

**Cross-Reference Resolution:**
- All section cross-references resolve correctly.
- INV-M1 through INV-M7 referenced consistently.
- Appendix F traceability matrix correctly maps feasibility conditions to spec sections.

**Inconsistency: Section 12.2 cost model vs. Abstract claim.**
- Abstract claims "40-60% system-level cost reduction."
- Section 12.2 calculates 0.83x (17% savings) before trust propagation.
- Section 12.2 then claims "0.40x-0.60x with downstream trust propagation" — this makes the abstract claim 40-60% cost reduction, but the propagation assumption is unvalidated.

### 2.3 Implementation Readiness: 4/5

**Algorithm Specification:**
- Subjective Logic operators: Fully specified with formulas, pseudocode, and test vectors. Verified correct. **EXCELLENT.**
- D-class verification: Fully specified with pseudocode for all 4 proof types. **EXCELLENT.**
- E-class source verification: Four-level protocol with pseudocode. **GOOD.**
- Classification protocol: Three-way protocol with pseudocode. Missing: classification signature definitions. **GOOD minus gap.**
- Credibility propagation: DAG (topological sort) and cyclic (dampening) both specified. **GOOD.**
- Deep-audit selection: VRF-based with citation weighting. Pseudocode provided. **GOOD.**
- Adversarial prober selection: VRF-based with exclusion rules. Pseudocode provided. **GOOD.**

**Edge Cases:**
- Cyclic dependency graphs: Handled via dampening algorithm with convergence guarantee.
- All-disagree classification: Resolved via conservatism ordering (though ordering is questionable, F6).
- Dogmatic opinions in fusion: Handled via weighted average fallback.
- Bootstrap (no existing verified claims): Acknowledged; seed claims proposed; details deferred (Q6).
- VTD exceeds size limit: Must decompose into sub-claims.

**Failure Modes:**
- Credibility convergence failure: Sentinel Graph alert.
- Deep-audit discrepancy: Agent investigation, cascade re-verification.
- Source URL 404: archive.org fallback specified.
- Committee cannot reach threshold: Not explicitly addressed. (Minor gap.)

**Test Vectors:**
- 8 test vectors provided (TV-D-001, TV-E-001, TV-SL-001 through TV-SL-003, TV-DA-001, TV-CLS-001, TV-DECAY-001).
- Mathematical test vectors (TV-SL-001, TV-SL-002, TV-SL-003) verified correct by independent calculation.
- Deep-audit probability test vector (TV-DA-001) verified correct.
- Credibility decay test vector (TV-DECAY-001) verified correct.
- **Adequacy:** GOOD. Test vectors cover the core mathematical operations. Additional vectors needed for: multi-class claims, contradictions, and adversarial probing outcomes.

### 2.4 Cross-Document Consistency

**C3 Tidal Noosphere Alignment:**
- C3 specifies 5 claim classes; C5 specifies 8. The expansion is justified by C5's epistemic matrix but creates a versioning issue. C3's verification membrane section references only 5 classes and does not mention P-class, R-class, or C-class. **INCONSISTENCY — MEDIUM severity.** Requires either updating C3 or documenting that C5 supersedes C3's claim taxonomy.
- C3 specifies VRF dual defense (commit-reveal + pre-stratified pools). C5 references VRF committee selection and pre-stratified diversity pools, consistent with C3. **CONSISTENT.**
- C3 specifies constitutional protection for the verification membrane (INV-1). C5's INV-M1 aligns with this. **CONSISTENT.**
- C3 specifies tidal epoch clock (1-hour default). C5's epoch alignment (Section 10.1) matches. **CONSISTENT.**
- C3 specifies Sentinel Graph for anomaly detection. C5's MQI metrics feed into Sentinel Graph. **CONSISTENT.**
- C3 specifies a 4-step classification protocol; C5 specifies a 3-way protocol (step 4 "seal" is a result, not a separate classification input). **MINOR DIFFERENCE,** but functionally equivalent.
- C3 references "Verichain" as the verification execution engine. C5 replaces Verichain. **CONSISTENT with the stated purpose of C5.**

**C4 ASV Alignment:**
- C4 defines 6 epistemic classes: observation, correlation, causation, inference, prediction, prescription.
- C5 defines 8 claim classes: D, E, S, H, N, P, R, C.
- Section 10.5 specifies the mapping: ASV CLM -> PCVM Claim, ASV PRV -> VTD dependencies, PCVM MCT -> ASV VRF token. However, the epistemic_class-to-claim-class mapping is NOT specified. This is a real gap. **INCONSISTENCY — MEDIUM severity.**
- Plausible mapping (not in spec): observation->E, correlation->S, causation->R, inference->R, prediction->H, prescription->N. But this loses D, P, C classes entirely and conflates correlation/causation/inference in ways that may not hold.
- C4's VRF token has `verification_result` (enum: verified, disputed, refuted, insufficient_evidence) and `confidence_in_verification` (numeric). C5's MCT has a full opinion tuple (b, d, u, a) and a credibility_score. The mapping is lossy: MCT's opinion tuple carries more information than VRF's verification_result enum. **MINOR INCONSISTENCY** — the ASV VRF token may need extending.

**Feasibility Conditions:**
- GATE-1 (VTD Feasibility): Addressed in Sections 4, 6 with complete VTD schemas and verification protocols. Experimental validation still required. **SPEC COMPLETE; VALIDATION PENDING.**
- GATE-2 (Classification Reliability): Three-way protocol specified (Section 5.3). Fleiss' kappa threshold specified. Classification signatures missing. **MOSTLY COMPLETE.**
- GATE-3 (Credibility Propagation): Dampening algorithm with convergence guarantees specified (Section 8.5). 500-claim graph experiment parameters defined. **SPEC COMPLETE; VALIDATION PENDING.**
- GATE-4 (Probing Effectiveness): Five probe types, selection, execution, evaluation all specified (Section 7). **SPEC COMPLETE; VALIDATION PENDING.**
- REQ-1 (Source Verification): Four-level protocol specified (Section 6.2). **COMPLETE.**
- REQ-2 (Membrane Classification): INV-M2 with three-way protocol (Section 5.3). **COMPLETE.**
- REQ-3 (Class-Specific Credibility): INV-M4 with per-class tracking (Section 8.2). **COMPLETE.**
- REQ-4 (Deep-Audit Protocol): VRF selection at 7% with citation weighting (Section 6.4). **COMPLETE.**
- REQ-5 (Unified vs. Split): Deferred as Open Question Q5. **INCOMPLETE — as expected at this stage.**

**Adversarial Findings:**
All 10 attacks from the Adversarial Report are addressed in Section 11.2 with specific defenses and honest residual risk assessments. The two CRITICAL attacks (VTD Forgery, Collusion) retain HIGH residual risk, which is honestly acknowledged. **CONSISTENT with adversarial report.**

### 2.5 Specific Issues

| # | Issue | Severity | Category |
|---|-------|----------|----------|
| I1 | Abstract's 40-60% cost claim is misleading; raw calculation yields 17% savings | HIGH | Consistency |
| I2 | C3 specifies 5 claim classes, C5 specifies 8 — no reconciliation documented | MEDIUM | Cross-Document |
| I3 | ASV epistemic_class to PCVM claim class mapping undefined | MEDIUM | Cross-Document |
| I4 | Classification signatures (markers/exclusions) undefined for all 8 classes | HIGH | Completeness |
| I5 | CLS (Classification Seal) schema never defined despite being a MUST requirement | MEDIUM | Completeness |
| I6 | Conservatism ordering may weaken verification for misclassified deterministic claims | HIGH | Consistency |
| I7 | Bootstrap protocol (Q6) remains an open question with minimal specification | LOW | Completeness |
| I8 | Committee failure to reach agreement threshold not specified | LOW | Completeness |
| I9 | "Compute tokens" unit for probe budgets undefined | MEDIUM | Completeness |
| I10 | MCT `cls_id` format pattern not specified | LOW | Consistency |
| I11 | S-class, P-class, R-class verification algorithms less detailed than D-class and E-class | LOW | Completeness |

---

## Final Assessment

### Overall Verdict: APPROVE WITH RECOMMENDATIONS

The C5 PCVM Master Tech Spec is a rigorous, technically honest specification that represents a genuine architectural contribution. It successfully navigates the tension between ambition (replacing replication-based consensus) and honesty (admitting that Tier 3 claims cost more to verify, that two critical attacks retain high residual risk, and that four hard gates require experimental validation).

**Strengths:**
1. The graduated VTD model is the right architecture — it matches verification depth to epistemic claim type rather than pretending all claims can be proof-checked.
2. The Subjective Logic formalization is mathematically correct (independently verified) and provides a principled improvement over binary pass/fail.
3. The adversarial probing system is novel and well-specified — no comparable system exists.
4. The security analysis is commendably honest about what PCVM cannot solve.
5. Eight complete JSON schemas for class-specific VTDs provide direct implementation guidance.
6. The conformance requirements (20 MUST, 8 SHOULD, 5 MAY) are well-structured and traceable.

**Weaknesses:**
1. The headline cost reduction claim (40-60%) depends on an unvalidated trust propagation assumption. The honest number is 17%.
2. Three high-severity issues (F1, F4, F6) should be addressed before implementation begins.
3. Cross-document consistency with C3 (5 vs. 8 classes) and C4 (epistemic_class mapping) requires reconciliation.
4. Four hard gates remain experimentally unvalidated — the system's core value proposition is contingent on their outcomes.

**Final Scores:**

| Dimension | Score |
|-----------|-------|
| Complexity | 7/10 |
| Achievability | 5/10 |
| Completeness | 4/5 |
| Consistency | 4/5 |
| Implementation Readiness | 4/5 |

**Pipeline Status:** C5 PCVM — ASSESSMENT COMPLETE. The specification is approved for the conclusion of the invention pipeline with the recommendations above noted for any future implementation effort.

---

*Assessment completed 2026-03-10. Simplification Agent and Completeness Reviewer, Atrahasis Agent System v2.0.*
*Protocol: Assessment Stage, C5 Proof-Carrying Verification Membrane.*
