# C13: CRP+ — Consolidation Robustness Protocol

## ASSESSMENT REPORT

**Invention:** C13 — Consolidation Poisoning Defense
**Stage:** ASSESSMENT (Final Review)
**Date:** 2026-03-10
**Assessors:** Simplification Agent, Completeness Checker, Consistency Auditor
**Document Under Review:** MASTER_TECH_SPEC.md v1.0 (2,641 lines)

---

## 1. Simplification Assessment

### 1.1 Over-Engineering Analysis

**Question:** Is the specification over-engineered? Can any mechanisms be removed?

**Finding: Moderately complex but justified. No mechanism is removable without creating a defense gap.**

Each of the seven mechanisms addresses a distinct and identified weakness in the pre-CRP+ consolidation pipeline:

| Mechanism | Addresses | Removable? | Consequence of Removal |
|---|---|---|---|
| M1 (APRT) | No robustness testing of synthesized claims | NO | Adversary can plant load-bearing quanta undetected |
| M2 (CODS) | No calibrated dissent analysis | NO | System either penalizes genuine novelty or ignores dissent deficit |
| M3 (Purpose) | Tie-breaking in ambiguous cases | PARTIALLY | Could be folded into M2 as a sub-score. However, the 20% invocation rate and 0.15 cap already minimize its footprint. Cost of removal: loss of signal in ~20% of borderline cases. |
| M4 (VRF Selection) | Deterministic candidate selection | NO | Adversary can target specific bridges with certainty |
| M5 (Credibility Ladder) | Binary validation model | NO | No graduated trust; damage from poison is unbounded at acceptance |
| M6 (Depth Limits) | Consolidation-of-consolidation cascades | NO | Poison amplification through K->K chains |
| M7 (Immune Memory) | No institutional memory of past attacks | NO | System re-evaluates identical attack patterns from scratch each time |

**M3 is the only candidate for simplification.** It contributes a maximum of 0.15 to the combined score and is invoked conditionally. However, its LLM cost is approximately 1 call per cycle (1 of 5 candidates triggers ambiguity). The cost-benefit ratio is acceptable. Recommendation: retain but flag as the first mechanism to disable if LLM budget tightens.

**Potential simplifications within mechanisms (not removal):**

1. **M7 L3 behavioral matching** uses a three-component similarity formula (timing 0.3 + cluster 0.3 + influence 0.4). The timing component's normalization (`abs(mean_diff) / 100.0`) is somewhat arbitrary. Could simplify to two-component (cluster + influence) without significant detection loss. **Severity: LOW.**

2. **M5 domain-adaptive threshold calibration** (Section 8.6) uses sigmoid/lerp with a midpoint of 100 and steepness 0.02. This is sophisticated machinery for what amounts to a small adjustment to uncertainty floors (e.g., CORROBORATED varies between 0.25 and 0.35). A simpler two-tier system (sparse vs. dense) would achieve 90% of the effect. **Severity: LOW.**

3. **Novelty Pathway provenance deep audit** runs three statistical checks (KS test, framing similarity, M7 cross-reference). The KS test against uniform distribution for intra-epoch timing is theoretically sound but may be brittle with small sample sizes (N ~ 10-15 quanta). **Severity: LOW.**

### 1.2 Complexity Score: 7/10

The spec is complex but proportionate to the threat model. Seven mechanisms is a significant implementation surface, but each is well-scoped with clear boundaries. The Novelty Pathway adds a parallel decision track that increases conceptual complexity. The 82 formal requirements are thorough but create a substantial conformance burden.

**Complexity drivers:**
- 7 mechanisms + 1 pathway = 8 distinct subsystems
- 82 formal requirements (44 MUST)
- 8 system invariants
- 10 failure modes with recovery protocols
- 40+ configurable parameters (9 constitutional, 30+ operational)
- 3 LLM separation requirements (M2 contradiction, M3 evaluator, NP constructive probe)

### 1.3 Achievability Score: 7/10

The spec is implementable within the Atrahasis stack. Key achievability factors:

**Favorable:**
- Reuses existing infrastructure (C3 VRF, C6 embeddings, C10 layers)
- 3.7x LLM overhead is within the 5x budget with 42-72% headroom
- All algorithms are specified in pseudocode with clear data flows
- No novel cryptographic primitives (ECVRF already deployed via C3)

**Challenging:**
- Three separate LLM instances required (consolidation, contradiction assessment, evaluator)
- Immune memory GC must run every epoch (performance-sensitive)
- Full leave-one-out APRT for N3 claims scales linearly with quanta count
- Domain-adaptive calibration requires per-domain density tracking
- 40+ parameters to tune, with complex interactions

### 1.4 Verdict: APPROVE WITH RECOMMENDATIONS

The specification is well-engineered for its threat model. No mechanism should be removed. Minor simplifications are possible within M5 (domain-adaptive thresholds) and M7 (L3 behavioral similarity) but are not blocking.

---

## 2. Completeness Check

### 2.1 Mechanism Coverage

| Mechanism | Fully Specified? | Sections | Notes |
|---|---|---|---|
| M1 (APRT) | YES | 4.1-4.6 | Two tiers, three cases, enhanced mode, pseudocode |
| M2 (CODS) | YES | 5.1-5.5 | Three-step pipeline, novelty classification, dissent search, calibration |
| M3 (Purpose) | YES | 6.1-6.4 | Invocation conditions, scoring algorithm, cap enforcement |
| M4 (VRF Selection) | YES | 7.1-7.6 | Seed construction, selection formula, anti-starvation, cost analysis |
| M5 (Credibility Ladder) | YES | 8.1-8.7 | 5 rungs, promotion/demotion protocols, domain-adaptive calibration, C10 integration |
| M6 (Depth Limits) | YES | 9.1-9.4 | Input weights, enforcement point, sandboxed K->K, lifecycle |
| M7 (Immune Memory) | YES | 10.1-10.5 | Three-level signatures, matching algorithm, enhanced scrutiny, memory management |
| Novelty Pathway | YES | 11.1-11.5 | Entry criteria, 4 scrutiny tests, combined decision, exit conditions |

**All 7 mechanisms and the Novelty Pathway are fully specified.** Each has purpose, integration point, algorithm, pseudocode, and formal requirements.

### 2.2 Hard Gate Coverage

| Invariant | Verified? | Verification Protocol |
|---|---|---|
| INV-CRP1 (VRF Unpredictability) | YES | Appendix B.1 |
| INV-CRP2 (APRT Completeness) | YES | Appendix B.2 |
| INV-CRP3 (CODS Calibration) | YES | Defined in Section 5.5, enforced by REQ-M2-012 |
| INV-CRP4 (Credibility Monotonicity) | YES | Promotion/demotion protocols in Sections 8.4-8.5 |
| INV-CRP5 (Depth Enforcement) | YES | Appendix B.3 |
| INV-CRP6 (Immune Memory Bounded) | YES | Appendix B.4 |
| INV-CRP7 (Novelty Pathway Isolation) | YES | Appendix B.5 |
| INV-CRP8 (M3 Cap) | YES | Appendix B.6 |

**All 8 invariants have verification protocols.** INV-CRP3 and INV-CRP4 are verified through their mechanism definitions rather than dedicated appendix protocols; this is acceptable since they are enforced by code logic rather than external verification.

### 2.3 Cross-Reference Coverage

| Referenced Spec | Cross-References Present? | Key Integration Points |
|---|---|---|
| C3 (Tidal Noosphere) | YES | VRF seeds (Section 7.2, 7.6), epoch clock (throughout), parcel topology (M5 promotion), G-class governance (Section 13.1) |
| C5 (PCVM) | YES | PCVM verification gate (Section 3.1, 3.2), Bayesian opinion fusion (M5 uncertainty floors) |
| C6 (EMA) | YES | Dreaming pipeline (Section 1.1, 3.1), Three-Pass LLM Synthesis (Section 4.2), consolidation phase wrapping (Section 3.1), coherence graph (M2), catabolism/regulation piggyback (Section 3.1) |
| C8 (DSF) | PARTIAL | Listed in normative references but no explicit mechanism integration points cited in the body. C8 (DSF v2.0) handles data sovereignty; CRP+ does not directly interact with sovereignty boundaries. |
| C9 | NOT LISTED | C9 is mentioned in the assessment task but NOT in the spec's normative references. If C9 exists and is relevant, this is a gap. |
| C10 (Hardening Addenda) | YES | 5-layer defense-in-depth (Section 1.2, 2.3), Layer 1-5 integration (Sections 3.1, 12.3), Sentinel Graph clusters (Section 11.2), cascade (Section 8.5) |
| C11 (CACT) | YES | Listed in normative references and stack diagram (Section 3.1). CACT collusion defense is a prerequisite layer. |
| C12 (AVAP) | YES | Listed in normative references and stack diagram (Section 3.1). AVAP collusion defense is a prerequisite layer. |

### 2.4 Missing Elements

| # | Element | Severity | Notes |
|---|---|---|---|
| 1 | C8 (DSF) body integration | LOW | Listed in normative references but no body text describes how CRP+ respects DSF sovereignty boundaries. Should specify that immune memory signatures do not cross sovereignty domains, or explicitly state no interaction. |
| 2 | C9 cross-reference | INFO | C9 is mentioned in the assessment task but absent from the spec. If C9 is a valid spec (e.g., Settlement Plane), the relationship should be documented or the omission explained. |
| 3 | Monitoring/observability specification | LOW | Section 15 describes failure detection via monitoring but does not specify the metrics, alerting thresholds, or dashboard requirements. Acceptable for a theoretical spec but would need elaboration for implementation. |
| 4 | Migration path from C10 Layer 5 binary model | LOW | Section 8.7 states M5 replaces C10 Layer 5 binary model and retains the data structure, but does not specify how existing PENDING_VALIDATION/VALIDATED quanta are migrated to the 5-rung system. |

### 2.5 Completeness Score: 4/5

The spec is substantially complete. All mechanisms, invariants, and most cross-references are present. The C8 body-level integration gap and migration path omission are minor. The C9 question depends on whether C9 exists and is relevant.

---

## 3. Consistency Audit

### 3.1 Internal Consistency

**3.1.1 Mechanism Interaction Check**

| Pair | Consistent? | Notes |
|---|---|---|
| M1 + M2 | YES | M1 produces robustness_score consumed by combined scoring. M2 produces cods_score consumed by combined scoring. No overlap or contradiction. |
| M1 + M7 | YES | M7 L2 match triggers enhanced APRT. Enhanced APRT is a well-defined mode of M1 (Section 4.6). |
| M2 + NP | YES | N3 classification routes to Novelty Pathway per REQ-M2-011. Novelty Pathway receives its own enhanced APRT. CODS score is recorded but not used in NP decision. |
| M3 + combined scoring | YES | M3 is additive (not weighted) and hard-capped at 0.15. Weights (0.35+0.25+0.25+0.15) sum to 1.00 excluding M3. Maximum combined suspicion is 1.15. |
| M4 + M1 | YES | VRF selection occurs before synthesis; APRT occurs after synthesis. No interaction. |
| M5 + M6 | YES | M6 uses M5 rung to determine consolidation eligibility. Rung 0-1 excluded, rung 2 at 0.50 weight, rung 3-4 at full weight. Consistent with M5 rung definitions. |
| M5 + NP quarantine | YES | Quarantined N3 claims are PROVISIONAL (rung 1) with quarantine_flag. REQ-M5-005 blocks promotion during quarantine. REQ-NP-009 disables fast-track. No contradiction. |
| M7 + NP entry | YES | NP entry criterion 4 requires no L2/L3 immune match. N3 claims that match immune memory follow the standard path per REQ-NP-001/002. |

**3.1.2 Parameter Consistency**

| Check | Result | Notes |
|---|---|---|
| Combined scoring weights sum | PASS | 0.35 + 0.25 + 0.25 + 0.15 = 1.00 (REQ-INT-001) |
| ACCEPT_THRESHOLD < REJECT_THRESHOLD | PASS | 0.35 < 0.60 (REQ-CFG-002) |
| M3 cap consistent across sections | PASS | 0.15 in Sections 2.1, 6.3, 12.1, 13.2 |
| PROVISIONAL influence weight consistent | PASS | 0.25 in Sections 2.2, 8.2, 8.3, 13.1 |
| N3 dissent weight consistent | PASS | 0.1 in Sections 5.5, 13.2 |
| STABILITY_THRESHOLD consistent | PASS | 0.70 in Sections 4.4.1, 11.3.1, 13.1, 15 |
| VRF_SELECTION_RATE consistent | PASS | 0.10 in Sections 7.3, 7.5, 13.1 |
| Quarantine cycles consistent | PASS | 5 standard, 10 extended in Sections 11.3.3, 11.4, 13.1 |

**3.1.3 Potential Internal Tension (not contradiction)**

1. **Enhanced APRT double-invocation for N3 on immune match.** Section 4.6 states enhanced APRT triggers for L2 immune matches. Section 11.2 entry criterion 4 states N3 claims with L2/L3 immune match do NOT enter the Novelty Pathway. Therefore, a N3 claim with L2 match gets enhanced APRT via the immune memory path (standard track) but not the Novelty Pathway's enhanced APRT. This is consistent but subtle — the two enhanced APRT paths are the same algorithm, triggered by different conditions. **No contradiction.**

2. **REQ-M2-004 vs. REQ-M2-005 interaction.** REQ-M2-004 says the most-novel feature determines the tier. REQ-M2-005 says N3 requires ALL THREE conditions. The pseudocode in Section 14.3 resolves this correctly: N3 is checked first with its triple-AND, then N1 with its OR conditions, then N2 as the default. The "most-novel-feature" rule in REQ-M2-004 applies to N1/N2 discrimination, not N3 entry. The wording of REQ-M2-004 could be clearer, but the pseudocode is correct. **Minor wording ambiguity, not a contradiction.**

3. **M5 uncertainty floor adjustment in Section 14.5.** The pseudocode adjusts `q.opinion.belief` when enforcing uncertainty floors: `q.opinion.belief = max(0.01, q.opinion.belief - deficit)`. This modifies the belief component without specifying how disbelief is affected, only calling `normalize_opinion()`. The Subjective Logic normalization (belief + disbelief + uncertainty = 1) is implicit. **Technically correct but could be more explicit about SL normalization.**

### 3.2 Cross-Spec Consistency

| Cross-Spec Issue | Severity | Notes |
|---|---|---|
| C3 VRF reuse | CONSISTENT | CRP+ uses C3 ECVRF with domain separator prefix "CRP_CONSOLIDATION_SELECT". This follows C3's VRF separation pattern. |
| C5 PCVM gate position | CONSISTENT | PCVM verification gate is after CRP+ accept decision, before M5 rung assignment (Section 3.2). This matches C6's existing pipeline where PCVM verifies after synthesis. |
| C6 Three-Pass Synthesis | CONSISTENT | CRP+ does not modify the synthesis itself; it wraps it with pre- and post-synthesis checks. |
| C10 5-layer integration | CONSISTENT | Section 2.3 clearly maps each CRP+ mechanism to its C10 layer relationship (UNCHANGED/EXTENDED). No C10 layer is removed or contradicted. |
| C10 Layer 5 replacement | CONSISTENT | M5 replaces the binary model with a graduated system. The `EmpiricalValidationQueue` data structure is retained (REQ-M5-013). |
| C10 Sentinel Graph | CONSISTENT | CRP+ references Sentinel Graph clusters for source diversity (NP entry criterion 3) and corroboration independence (M5 promotion). This matches C10's cluster definitions. |
| C11/C12 collusion defense | CONSISTENT | CRP+ is positioned below C11/C12 in the stack (Section 3.1). It does not modify or duplicate their functions. The separate-LLM requirements (M2, M3, NP) are CRP+-specific and do not conflict with C11/C12 collusion detection. |

**No cross-spec contradictions found.**

### 3.3 Consistency Scores

- **Internal consistency: 5/5** — No contradictions. One minor wording ambiguity (REQ-M2-004) is resolved by pseudocode. All parameters are consistent across sections.
- **Cross-spec consistency: 5/5** — All cross-references to C3, C5, C6, C10, C11, C12 are consistent. No conflicts detected. C8 is underspecified but not contradicted.

---

## 4. Findings Summary

| # | Severity | Category | Finding |
|---|---|---|---|
| F1 | LOW | Completeness | C8 (DSF) listed in normative references but no body-level integration described. Should clarify whether immune memory signatures respect sovereignty boundaries. |
| F2 | INFO | Completeness | C9 absent from spec. Verify whether C9 is relevant; if so, add cross-reference. |
| F3 | LOW | Completeness | No migration path specified for existing C10 Layer 5 PENDING_VALIDATION/VALIDATED quanta to M5 5-rung system. |
| F4 | LOW | Simplification | M5 domain-adaptive threshold calibration (sigmoid/lerp) is more sophisticated than necessary. A two-tier sparse/dense system would suffice. |
| F5 | LOW | Simplification | M7 L3 behavioral timing component uses arbitrary normalization (division by 100). Consider replacing with a more principled normalization. |
| F6 | INFO | Clarity | REQ-M2-004 wording ("most-novel-feature rule") could be misread as applying to N3. Pseudocode is correct; consider rewording the requirement text. |
| F7 | INFO | Clarity | M5 uncertainty floor enforcement pseudocode (Section 14.5) implicitly relies on SL normalization. Could add explicit comment. |
| F8 | LOW | Completeness | Monitoring thresholds (rejection rate, N3 classification rate, immune match rate) mentioned in failure modes but not formally specified as operational requirements. |

**Finding counts by severity:**
- CRITICAL: 0
- HIGH: 0
- LOW: 5
- INFO: 3

---

## 5. Final Verdict

### APPROVE

C13 CRP+ is a well-structured, internally consistent, and substantially complete specification. It addresses a genuine and clearly articulated threat (consolidation poisoning) with a proportionate 7-mechanism defense architecture. The spec demonstrates strong design discipline:

- Defense-in-depth philosophy maintained throughout
- Novelty Pathway solves the central tension (hardening vs. discovery) with calibrated skepticism
- 82 formal requirements with clear MUST/SHOULD/MAY classification
- 10 failure modes with recovery protocols
- Detailed adversary cost analysis (30x multiplication)
- Performance budget with 42-72% headroom

No critical or high-severity findings. The five LOW findings are implementation-level concerns that do not affect the spec's validity. The three INFO findings are documentation improvements.

---

## 6. Scores

| Dimension | Score | Scale | Notes |
|---|---|---|---|
| **Complexity** | 7/10 | 1=trivial, 10=impenetrable | 7 mechanisms + pathway is substantial but each is well-bounded. 82 requirements create conformance overhead. |
| **Achievability** | 7/10 | 1=impossible, 10=trivial | Reuses existing infrastructure. 3.7x LLM overhead is manageable. Multi-LLM separation and 40+ parameters are the main implementation challenges. |
| **Completeness** | 4/5 | 1=skeletal, 5=exhaustive | All mechanisms fully specified. Minor gaps in C8 integration, migration path, and monitoring formalization. |
| **Internal Consistency** | 5/5 | 1=contradictory, 5=airtight | No contradictions. Parameters consistent across all sections. Pseudocode matches prose. |
| **Cross-Spec Consistency** | 5/5 | 1=conflicting, 5=harmonized | Clean integration with C3, C5, C6, C10, C11, C12. No conflicts. C8 underspecified but not contradicted. |
| **Simplification Verdict** | APPROVE WITH RECOMMENDATIONS | | No mechanism removable. Minor simplifications possible within M5 and M7. |
| **Overall Verdict** | **APPROVE** | | Spec is ready for the Atrahasis system catalog. |

---

## 7. Recommendations

### 7.1 Pre-Catalog (address before archiving)

None required. All findings are LOW/INFO and do not block approval.

### 7.2 Implementation-Phase Recommendations

1. **Add C8 sovereignty note.** Clarify in a future revision whether immune memory signatures are shard-local (respecting DSF sovereignty boundaries) or may be shared across sovereignty domains for campaign detection. Current spec implies shard-local (Section 10.5 references per-shard limits) which is likely correct.

2. **Define migration protocol.** Before deploying M5 over existing C10 Layer 5, specify how PENDING_VALIDATION maps to PROVISIONAL and VALIDATED maps to CORROBORATED (or ESTABLISHED, depending on corroboration history).

3. **Simplify M5 domain-adaptive thresholds.** Consider replacing the sigmoid/lerp formulation with a two-tier system (sparse: < 50 quanta, dense: >= 50 quanta) during initial deployment. Graduate to sigmoid/lerp if tuning data justifies the complexity.

4. **Baseline LLM stochasticity.** Before deploying APRT, run the "re-synthesis consistency check" described in FM-10 to establish baseline variability and calibrate STABILITY_THRESHOLD accordingly.

5. **Clarify REQ-M2-004 wording.** Amend to: "When the three novelty features (domain_overlap, precedent_count, semantic_distance) individually classify to different N1/N2 tiers, the MOST NOVEL tier among them determines the classification. N3 classification follows its own triple-AND rule (REQ-M2-005) and is not subject to the most-novel-feature rule."

---

*Assessment complete. C13 CRP+ is APPROVED for the Atrahasis system catalog.*

*Assessed by: Simplification Agent, Completeness Checker, Consistency Auditor*
*Date: 2026-03-10*
