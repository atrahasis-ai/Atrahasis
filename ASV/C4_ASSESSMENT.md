# ASSESSMENT -- C4-A ASV Master Tech Spec
## Date: 2026-03-10

---

## Part 1: Simplification Review

### Verdict: APPROVE WITH RECOMMENDATIONS
### Complexity Score: 6/10 current, 5/10 achievable

### Findings

**S-1: Architecture document uses different CNF structure than Master Tech Spec and Technical Spec** | Severity: HIGH

The architecture document (architecture.md, Section 3.2) defines CNF with a `representation` field (`"representation": "point"`, `"representation": "distribution"`, `"representation": "interval"`), a `calibration.calibrated` boolean, and a `calibration.warning` string. The Master Tech Spec and Technical Spec define CNF without a `representation` field (using `anyOf` with required `value`, `interval`, or `distribution`), with `calibration.status` as an enum (`calibrated`, `uncalibrated`, `self_reported`), and no `calibration.warning` field. The architecture also lists `heuristic` as missing from the CNF `method` enum (it lists only 4 methods; the schemas define 5). These are not minor formatting differences -- they are structural schema mismatches that would produce incompatible implementations.

**Recommendation:** Align the architecture document's CNF examples and schema descriptions to match the normative schemas in the Master Tech Spec and Technical Spec. The Master Tech Spec schemas are the correct authority.

---

**S-2: Architecture document uses different field names than the normative schemas** | Severity: HIGH

Multiple field name discrepancies between architecture.md and the other two specs:
- Architecture uses `statement` where Master/Technical use `content` for CLM text.
- Architecture uses `claim` where Master/Technical use `payload` for SAE content.
- Architecture uses `rebuts_claim` (singular) where Master/Technical use `rebuts_claims` (plural).
- Architecture uses `commitment` field on SAE which does not exist in the normative schemas.
- Architecture uses `claim_type` on CLM which does not exist in the normative schemas.
- Architecture PRV uses `prov:wasGeneratedBy` as a nested object with `activity_id`, `activity_type`, `started_at`, `ended_at` -- an entirely different structure from the flat PRV schema in the other specs.
- Architecture VRF uses `verifiers` (array of URIs) instead of `verifier_id` (single URI).
- Architecture VRF uses `result` (nested object) which does not exist in the normative schemas.

These are not cosmetic -- an implementer following the architecture document would produce ASV objects that fail schema validation against the Master Tech Spec schemas.

**Recommendation:** The architecture document must be updated to use the normative field names from the Master Tech Spec. Since architecture.md appears to have been written first (before schemas were finalized), a reconciliation pass is required.

---

**S-3: Type count discrepancy -- 7 types vs 8 types** | Severity: MEDIUM

The Master Tech Spec consistently says "seven typed semantic structures" and "seven core types." The Technical Spec says "eight core types" (Section 2, line 52). The Technical Spec counts RBT (Rebuttal) as a type in its section numbering (Section 2.7) and TVL (Temporal Validity) as another (Section 2.8), but then clarifies that neither is a separate schema type. This creates confusion: the spec says "eight" but defines seven schemas. The Master Tech Spec is correct: there are 7 schema-backed types.

**Recommendation:** Fix the Technical Spec's count to say "seven core types" and clarify that Sections 2.7 (RBT) and 2.8 (TVL) describe behavioral patterns of existing types, not new types.

---

**S-4: The 6x6 dual classification matrix is appropriate complexity** | Severity: LOW (informational)

The 6x6 matrix (6 performatives x 6 epistemic classes = 36 combinations) was flagged for review. Assessment: this is justified complexity. The two dimensions are genuinely orthogonal -- speech-act type describes the communicative intent while epistemic class describes the knowledge assertion type. Reducing either dimension would lose operational value: removing a performative like WARN loses routing clarity; removing an epistemic class like the causation/correlation distinction loses the verification-strategy differentiation that is ASV's core value proposition. The matrix is documented clearly, the spec explicitly states all 36 combinations are valid, and implementations MUST NOT reject uncommon combinations. This complexity earns its place.

---

**S-5: Three conformance levels are justified** | Severity: LOW (informational)

The three conformance levels (Basic, Standard, Full) were flagged for review. Assessment: the three levels are well-differentiated and serve distinct use cases. Basic is pure schema validation (implementable in hours). Standard adds cross-field semantic checks (value-within-interval, distribution-sums-to-1). Full adds graph-level integrity and runtime monitoring. Reducing to two levels would either force lightweight consumers to implement graph referential integrity (unreasonable) or leave no path for implementations that want semantic validation without runtime monitoring. Three levels is the right number.

The architecture document (Section 6.1) defines conformance differently as Level 1/2/3 (Structural/Semantic/Full) while the Technical Spec and Master Tech Spec use Basic/Standard/Full. The naming should be unified to Basic/Standard/Full throughout. The chain completeness levels in the Technical Spec Section 3.4 (Minimal/Standard/Full/Auditable -- four levels) are distinct from conformance levels and should remain separate but be more clearly distinguished from conformance levels to avoid confusion.

---

**S-6: Confidence calibration protocol is appropriately scoped** | Severity: LOW (informational)

The calibration protocol in Section 7 of the Master Tech Spec was flagged as potentially over-engineered. Assessment: it is appropriately scoped. The spec does not attempt to solve calibration -- it explicitly states calibration is "an active research problem, not a specification problem." What it does is require transparency: three status levels (calibrated/uncalibrated/self_reported), metadata when calibrated, and drift detection guidance. This is the minimum needed to make confidence values interpretable. The drift detection is SHOULD-level, not MUST, at Basic and Standard conformance. No simplification recommended.

---

**S-7: The `heuristic` confidence method may be redundant** | Severity: LOW

The five confidence methods are: `statistical`, `consensus`, `model_derived`, `human_judged`, `heuristic`. The `heuristic` method overlaps with `model_derived` for rule-based systems and with `human_judged` for expert heuristics. However, removing it would force producers to misclassify rule-based confidence (which is neither statistical nor model-derived in the ML sense) into an ill-fitting category. The cost of keeping it is one extra enum value. The cost of removing it is semantic confusion for a common case (rule-based systems).

**Recommendation:** Keep as-is. The slight redundancy is less harmful than the misclassification it prevents.

---

**S-8: Namespace URI inconsistency between architecture and other specs** | Severity: MEDIUM

The architecture document uses `https://asv.atrahasis.org/v1/` as the namespace and context URI in its examples (e.g., `"@context": "https://asv.atrahasis.org/v1/context.jsonld"`, `"$schema": "https://asv.atrahasis.org/v1/schema.json"`). The Master Tech Spec and Technical Spec use `https://asv.atrahasis.dev/vocab/v1/` and `https://asv.atrahasis.dev/vocab/v1#` consistently. These are different domains (`.org` vs `.dev`) and different path structures.

**Recommendation:** Standardize on `https://asv.atrahasis.dev/vocab/v1/` as used in the normative schemas.

---

**S-9: Architecture document lists `direct_observation` method on CNF** | Severity: LOW

In architecture.md Section 4.2 (MCP example, line 540-541), a CNF uses `"method": "direct_observation"`. This is not a valid CNF method enum value. The valid values are: `statistical`, `consensus`, `model_derived`, `human_judged`, `heuristic`. `direct_observation` is an EVD quality class, not a CNF method.

**Recommendation:** Fix to an appropriate method value (likely `statistical` or `heuristic`).

---

**S-10: Architecture evidence source_type values differ from normative schemas** | Severity: LOW

The architecture uses evidence `source_type` values not in the normative enum: `dataset_reference`, `analysis_output`, `model_output`, `credit_bureau_report`, `income_verification`, `regulatory_filing`. The normative enum is: `dataset`, `document`, `api`, `agent_output`, `sensor`, `human_input`, `other`. These architecture examples would fail schema validation.

**Recommendation:** Update architecture examples to use normative enum values or `other`.

---

### Complexity That Earns Its Place

1. **Seven ASV types (AGT, CLM, CNF, EVD, PRV, VRF, SAE).** Each serves a distinct purpose in the epistemic chain. No type is redundant. AGT identifies responsibility; CLM is the root assertion; CNF quantifies confidence; EVD links to supporting data; PRV traces derivation history; VRF records independent validation; SAE wraps in communicative intent. Removing any one breaks the chain's completeness.

2. **Six epistemic classes.** The observation/correlation/causation distinction is the core novel contribution. Collapsing any pair (e.g., correlation and causation) would eliminate the verification-strategy differentiation that justifies ASV's existence. The six classes are derived from epistemology and map to operationally different verification approaches.

3. **Six SAE performatives.** Grounded in the uACP completeness proof (4 verbs suffice); the 2 additions (PROPOSE, WARN) are pragmatic convenience that improve routing without extending expressive power. The justification is explicit and the mapping to uACP is documented.

4. **Three confidence representation modes (point, interval, distribution).** Different use cases require different representations. A sensor reading needs a point estimate. A statistical analysis needs an interval. A diagnostic assessment needs a distribution over outcomes. Removing any mode forces misrepresentation of confidence for common cases.

5. **Calibration metadata.** Directly addresses Assessment Council REQ-3 and the most dangerous technical assumption (poorly calibrated LLM confidence). The three-status approach is the minimum needed to distinguish "validated against holdout data" from "raw model guess."

---

## Part 2: Completeness Assessment

### Verdict: CONDITIONALLY_COMPLETE
### Completeness: 4/5
### Consistency: 3/5
### Implementation Readiness: 4/5

### Section Assessment

| Section | Master Tech Spec | Status |
|---------|-----------------|--------|
| 1. Introduction | Problem, landscape, principles, anti-patterns | COMPLETE |
| 2. Epistemic Accountability Chain | Chain structure, complete example | COMPLETE |
| 3. ASV Type System | All 7 types with full JSON Schema | COMPLETE |
| 4. Claim Classification | Epistemic classes, dual classification matrix | COMPLETE |
| 5. Integration | A2A, MCP, standalone with complete examples | COMPLETE |
| 6. JSON-LD Context | Full context definition | COMPLETE |
| 7. Confidence Calibration | Levels, protocol, drift detection, guidance | COMPLETE |
| 8. Rebuttals and Temporal Validity | Rules, examples | COMPLETE |
| 9. Security Analysis | Threat model, mitigations, trust delegation | COMPLETE |
| 10. Validation Plan | 3 gates, 3 conformance levels, 7 test vectors | COMPLETE |
| 11. Adoption Strategy | Regulated industries, open source, standards path | COMPLETE |
| 12. Risk Assessment | Residual risks, monitoring flags, convergence | COMPLETE |
| 13. Implementation Roadmap | 4 phases, kill criteria per phase | COMPLETE |
| 14. Conclusion | Honest assessment | COMPLETE |
| Appendix A: Schema Inventory | All 12 files listed | COMPLETE |
| Appendix B: Invention Claim Scope | REQ-1 compliance | COMPLETE |
| Appendix C: Traceability Matrix | All conditions mapped | COMPLETE |
| Appendix D: Glossary | 24 terms defined | COMPLETE |

No TODOs, TBDs, or placeholder sections found in the Master Tech Spec.

### Traceability Verification

| Condition | ID | Type | Addressed? | Location |
|-----------|-----|------|-----------|----------|
| Working Implementation Before Full Spec | GATE-1 | GATE | Yes (PENDING execution) | Master Sec 10.1, 13 Phase 1; Technical Sec schemas; Architecture Sec 2.1 |
| LLM Generation Accuracy | GATE-2 | GATE | Yes (PENDING execution) | Master Sec 10.1; Architecture Sec 2.2 |
| Provenance Chain Utility | GATE-3 | GATE | Yes (PENDING execution) | Master Sec 10.1; Architecture Sec 2.3 |
| Narrow the Invention Claim | REQ-1 | REQUIRED | ADDRESSED | Master Appendix B; Technical Appendix B; Architecture Sec 1.1 |
| Kill AACP as Separate Protocol | REQ-2 | REQUIRED | ADDRESSED | Master Sec 1.4-1.5; Architecture Sec 1.3; Technical Sec 1.1 |
| Address Confidence Calibration | REQ-3 | REQUIRED | ADDRESSED | Master Sec 3.3, 7; Technical Sec 2.3, 9; Architecture Sec 3.2 |
| Semantic Spec Cap (50 pages) | REQ-4 | REQUIRED | ADDRESSED | Master Sec 7 note; Architecture Sec 6; Technical Sec 8 |
| Regulated Industry Engagement | REC-1 | RECOMMENDED | PENDING (appropriate) | Master Sec 11.1; examples demonstrate healthcare use case |
| A2A Specification Monitoring | REC-2 | RECOMMENDED | PENDING (appropriate) | Master Sec 12.2; Architecture noted |

All 3 hard gates are documented with clear kill criteria. All 4 required actions are addressed. Both recommended actions are acknowledged as pending operational concerns. The traceability matrix in each document is consistent.

### Cross-Document Consistency Issues

**Issue 1 (HIGH): Architecture vs. Master/Technical schema misalignment.** The architecture document uses a fundamentally different object structure for CNF, PRV, VRF, and SAE compared to the normative schemas. Specific discrepancies are cataloged in S-1 and S-2 above. An implementer using only the architecture document would produce non-conforming ASV objects.

**Issue 2 (MEDIUM): Namespace URI mismatch.** The architecture uses `.org` domain; the specs use `.dev` domain. Cataloged in S-8.

**Issue 3 (MEDIUM): Type count.** Technical Spec says "eight core types"; Master Tech Spec says "seven." Cataloged in S-3.

**Issue 4 (LOW): Architecture uses VRF status `unverified` and `expired`; the normative schemas define `verified`, `disputed`, `inconclusive`, `pending`.** (Architecture Sec 3.1, line 159 shows `unverified` and `expired` in the chain diagram.) These are not valid enum values per the schemas.

**Issue 5 (LOW): Architecture CNF method `human_judged` is missing from architecture Sec 3.2 method list** (lists only 4: statistical, consensus, model_derived, human_judged -- but the calibration section only mentions 4 and the normative schema has 5 including `heuristic`).

**Issue 6 (LOW): Technical Spec Example 1 (Section 12, line 1841) uses `"method": "computational_result"` on a CNF object.** This is not a valid CNF method enum value. `computational_result` is an EVD quality_class. Should be `heuristic` or `statistical`.

### Corrections Needed

1. **[MUST FIX] Architecture document reconciliation.** The architecture.md must be updated to align field names, schema structures, namespace URIs, and enum values with the normative schemas defined in the Master Tech Spec and Technical Spec. Key items: `statement` -> `content`, `claim` -> `payload`, `rebuts_claim` -> `rebuts_claims`, remove `commitment` and `claim_type` fields, flatten PRV structure, fix VRF to use `verifier_id` not `verifiers`, fix namespace to `.dev`, fix CNF to use `calibration.status` enum instead of `calibration.calibrated` boolean.

2. **[MUST FIX] Technical Spec type count.** Change "eight core types" to "seven core types" in Section 2.

3. **[SHOULD FIX] Technical Spec Example 1 CNF method.** Change `"method": "computational_result"` to a valid CNF method value.

4. **[SHOULD FIX] Architecture CNF method `direct_observation`.** Change to a valid CNF method value.

5. **[SHOULD FIX] Architecture evidence source_type values.** Align with normative enum or use `other`.

### Implementation Readiness

The Master Tech Spec is implementation-ready. It provides:
- Complete JSON Schema definitions for all 7 types with full property specifications.
- Clear composition rules for the epistemic chain.
- Complete JSON-LD context mapping.
- Three integration examples with full JSON payloads (A2A, MCP, standalone).
- Seven test vectors covering Basic, Standard, and Full conformance.
- Configurable parameters with sensible defaults (Technical Spec Section 10).
- A clear conformance testing strategy.

An implementer could build a conforming Basic validator from the Master Tech Spec alone. Standard and Full conformance require the companion Semantic Specification (not yet written, by design -- code-first principle).

The primary gap is the architecture document's divergence from normative schemas, which could mislead implementers who read architecture.md first.

---

## Final Recommendation: APPROVE_WITH_NOTES

The Master Tech Spec (MASTER_TECH_SPEC.md) is a well-crafted, implementation-ready specification. It is complete, internally consistent, honestly scoped, and addresses all Assessment Council conditions. The 7 ASV types, 6 epistemic classes, 6 performatives, 3 conformance levels, and calibration protocol all earn their complexity. No simplification is recommended for the Master Tech Spec itself.

The Technical Spec (technical_spec.md) is also strong and closely aligned with the Master Tech Spec, with only minor issues (type count, one invalid enum value in an example).

The architecture document (architecture.md) has significant structural divergence from the normative schemas and must be reconciled before implementation begins. This is the single blocking issue.

### Required Actions Before Implementation

1. **Reconcile architecture.md** with the normative schemas in MASTER_TECH_SPEC.md. This is a documentation update, not a design change -- the schemas are correct; the architecture examples need updating.

2. **Fix the Technical Spec type count** from "eight" to "seven."

3. **Fix invalid enum values** in Technical Spec Example 1 and architecture examples.

### Notes

- The spec's self-awareness is a strength. It repeatedly acknowledges its moderate novelty (3/5), identifies which components are genuinely novel vs. applications of existing standards, and provides honest risk assessment. This transparency reduces the specification-to-reality gap.

- The "code before spec" principle is correctly embedded: Phase 1 deliverables are validators and integration examples, not the semantic specification.

- The three gate experiments have clear, quantitative kill criteria. This is exactly the kind of empirical validation that prevents death-by-specification.

- No adversarial findings from the C4_ADVERSARIAL_REPORT.md are left unaddressed. The reassembly attack is acknowledged (Section 14), the adoption risk is mitigated through the compliance-first strategy (Section 11), and the confidence calibration concern is addressed head-on (Section 7).
