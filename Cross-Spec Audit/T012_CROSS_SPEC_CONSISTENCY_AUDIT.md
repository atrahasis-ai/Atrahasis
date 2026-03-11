# T-012: Cross-Spec Consistency Audit

**Date:** 2026-03-11
**Scope:** All 19 Master Tech Specs (C3-C22) + C9 reconciliation addendum
**Status:** COMPLETE
**Methodology:** Parallel 4-agent systematic scan across architecture layers, defense systems, governance/economics, and implementation specs

---

## Executive Summary

**Total findings: 35** (5 CRITICAL, 9 HIGH, 13 MEDIUM, 8 LOW)

The 5 v2.0 core architecture specs (C3, C5, C6, C7, C8) are largely consistent with each other and with C9. The most significant inconsistencies are:

1. **Version reference staleness** — C11/C12/C13 (defense specs) reference C3/C5/C6 v1.0 while v2.0 exists and claims to supersede them
2. **Budget/timeline mismatch** — C18 ($10M-$12M, 30-36mo) vs C22 ($5.4M-$8.8M, 21-30mo)
3. **K-class aging rate parameter conflict** — C3 and C6 specify different values
4. **C14 economic model outdated** — Still references CCU model superseded by C15 ACI
5. **C12 claim class misidentification** — C-class labeled "Causal" instead of "Compliance"

No findings represent unfixable architectural contradictions. All are reconcilable through targeted errata.

---

## CRITICAL Findings (5)

### CR-01: K-Class Aging Rate Units Mismatch
**Specs:** C3 (line ~1298) vs C6 (line ~285)
**Issue:** C3 states `KNOWLEDGE_AGING_RATE = 0.02 per CONSOLIDATION_CYCLE`. C6 states `K-class aging rate = 0.005 per TIDAL_EPOCH`. These are dimensionally incompatible: 0.02/36000s ≠ 0.005/3600s. C9 canonical value is `0.005 per TIDAL_EPOCH`.
**Impact:** K-class credibility decay calculations would differ between C3 and C6 implementations.
**Fix:** Correct C3 to `0.005 per TIDAL_EPOCH` (or equivalently `0.05 per CONSOLIDATION_CYCLE`) to match C6 and C9.

### CR-02: Budget Range Mismatch — C18 vs C22
**Specs:** C18 (line ~12) vs C22 (line ~21)
**Issue:** C18 specifies $10M-$12M total budget over 30-36 months. C22 specifies $5.4M-$8.8M (with contingency: $6.5M-$9.1M). Gap of $1.6M-$4.6M unexplained.
**Root cause:** C22 appears to budget engineering-only costs; C18 includes legal, admin, overhead, founder compensation, contingency. Neither spec explicitly documents the scope boundary.
**Impact:** Implementation teams and funders would see contradictory cost projections.
**Fix:** Add explicit scope statement to both specs. C22 should note "engineering delivery costs only; see C18 for fully-loaded budget." C18 should include a reconciliation table mapping its categories to C22 wave costs.

### CR-03: Timeline Mismatch — C18 vs C22
**Specs:** C18 (line ~12) vs C22 (lines ~19, 60)
**Issue:** C18 specifies 30-36 months. C22 specifies 21-30 months for the 6-wave implementation. C18's minimum exceeds C22's midpoint.
**Root cause:** C22 measures engineering delivery. C18 measures from founding capital to revenue sustainability, which includes pre-W0 entity formation (3 months) and post-W5 operational ramp.
**Impact:** Stakeholders cannot determine which timeline to plan against.
**Fix:** Clarify that C22's 21-30 months covers W0-W5 engineering delivery only; C18's 30-36 months covers the full lifecycle from entity formation through operational sustainability. Add timeline reconciliation diagram to both specs.

### CR-04: Defense Specs Reference Outdated v1.0 Core Specs
**Specs:** C11 (line ~11), C12 (line ~10), C13 (line ~10)
**Issue:** All three defense specs list normative references to C3 v1.0, C5 v1.0, C6 v1.0. Canonical versions are all v2.0 (2026-03-10). Meanwhile, C5 v2.0 claims to "supersede" C11 and C12; C6 v2.0 claims to "supersede" C13.
**Impact:** Ambiguity about authoritative source. An implementer reading C11 alone would reference deprecated spec versions. The supersession relationship creates dual-documentation confusion.
**Fix:** Two options:
  - **(A) Preferred:** Mark C11/C12/C13 as "Reference Architecture v1.0 — integrated into C5/C6 v2.0." Add deprecation headers. Update normative references to v2.0 for anyone reading the standalone docs.
  - **(B) Alternative:** Remove "Supersedes C11/C12/C13" from C5/C6 headers. Instead state "Integrates C11/C12/C13 mechanisms." Keep all as current documents.

### CR-05: C12 Claim Class Misidentification
**Spec:** C12 (line ~716)
**Issue:** C12's honeypot injection table defines C-class as "Causal." Canonical definition (C5 v2.0, C9): C-class = "Compliance" (regulatory conformance claims).
**Impact:** Honeypot generation for C-class claims would target wrong evidence types. Verification rigor assignment affected.
**Fix:** Correct C12 honeypot table: C-class = "Compliance", not "Causal." Update honeypot generation approach accordingly (compliance evidence vs. causal evidence).

---

## HIGH Findings (9)

### HI-01: C14 References Deprecated CCU Economic Model
**Specs:** C14 (lines ~788-789) vs C15 (line ~151)
**Issue:** C14 defines `1 AIC = 1 CCU = 1 GPU-hour`. C15 explicitly supersedes this with dual-anchor valuation (ACI + NIV). C14 has not been updated.
**Fix:** C14 should reference C15 for AIC valuation. Add note: "CCU model in §X.X is superseded by C15 ACI-based valuation."

### HI-02: Deprecated Verichain/CIOS in C3 Dependency Table
**Spec:** C3 (lines ~2685-2686)
**Issue:** C3 v2.0 phased implementation plan lists "Verichain Consensus Algorithm" and "CIOS Organizational Hierarchy" as Phase 1 dependencies. Both are replaced (by C5 PCVM and C7 RIF respectively).
**Fix:** Replace with "PCVM (C5) Verification Membrane" and "RIF (C7) Recursive Intent Fabric."

### HI-03: C6 Missing Conservatism Ordering Statement
**Spec:** C6
**Issue:** C3 and C5 both correctly state the canonical conservatism ordering `H > N > K > E > S > R > P > C > D` per C9. C6 does not state it anywhere despite being the primary consumer of K-class claims.
**Fix:** Add explicit conservatism ordering to C6 with citation to C9 SS4.2 and INV-C2.

### HI-04: C3 K-Class Source Requirements Understated
**Spec:** C3 (line ~1296) vs C5/C9
**Issue:** C3 states K-class VTDs require "evidence from at least 3 independent sources." C5/C9 canonical requirement is "minimum 5 from at least 5 agents and 3 parcels, no single agent >30%."
**Fix:** Update C3 to match C5/C9 canonical requirement.

### HI-05: C12 Missing P-Class and R-Class Honeypot Coverage
**Spec:** C12 (lines ~714-720)
**Issue:** C12's class-stratified honeypot table covers D, E, C, S, H, N, K — but omits P-class (Process) and R-class (Reasoning). These two claim classes have no defined honeypot injection rates.
**Fix:** Add P-class and R-class to the honeypot table. Suggested: P-class Tier 2 Partial (2%, like C/S), R-class Tier 2 Partial (2%).

### HI-06: C14 Missing C15-C17 Integration References
**Spec:** C14 (line ~17)
**Issue:** C14 states integration with "C3-C13" but does not reference C15 (AIC economics that supersedes its own CCU model), C17 (MCSD Layer 2 that resolves its OQ-2), or C16 (outreach package that addresses its OC-3).
**Fix:** Add integration references to C15, C17, C16 in C14's cross-reference section.

### HI-07: C14 G-Class Governance Ops Not Mapped to DSF Settlement Streams
**Specs:** C14 vs C8
**Issue:** C14 defines governance operations (G-GOV-01 through G-GOV-08) but does not specify which C8 settlement stream (B/V/G-class) they use or how they interleave with C8 capacity budgets.
**Fix:** Add settlement stream mapping table to C14: all governance operations should map to G-class settlement (variable 10-50 SETTLEMENT_TICKs per C8).

### HI-08: C22 Budget Lacks Non-Engineering Cost Breakdown
**Spec:** C22 (lines ~21, 69, 947)
**Issue:** C22 provides only engineering delivery costs ($5.4M-$8.8M) and cloud infrastructure ($410K). No breakdown of legal, admin, overhead, contingency, or founder compensation — all of which C18 includes in the $10M-$12M fully-loaded figure.
**Fix:** Add explicit scope statement and reconciliation table mapping C22 wave costs to C18 fully-loaded categories.

### HI-09: CCU Supersession Transition Plan Missing
**Specs:** C15 vs C14
**Issue:** C15 states CCU is "superseded" but does not specify: which C14 sections reference CCU, whether CCU is deprecated in all contexts, or whether a transition plan is needed for Phase 0-1 where both models might coexist.
**Fix:** Add CCU deprecation section to C15 listing all C14 CCU references and their ACI replacements.

---

## MEDIUM Findings (13)

### ME-01: C6 Missing K-Class Extended Lifecycle Documentation
**Spec:** C6
**Issue:** C9 v2.0 introduced 5-rung credibility ladder (SPECULATIVE/PROVISIONAL/CORROBORATED/ESTABLISHED/CANONICAL) for K-class with depth limits per C13 CRP+. C6 does not document rung definitions or enforcement.
**Fix:** Add K-class credibility rung section to C6 referencing C9 SS4.6 and C13.

### ME-02: C5 "Epoch" Not Explicitly Mapped to TIDAL_EPOCH
**Spec:** C5
**Issue:** C5 uses "epoch" throughout without clarifying it means TIDAL_EPOCH (3600s). Could be confused with SETTLEMENT_TICK (60s).
**Fix:** Add disambiguation statement in C5 introduction per C9 SS3.4.

### ME-03: C3 Stale AASL/AACP References
**Spec:** C3 (technical_spec.md lines ~27, 157, 165)
**Issue:** References to AASL remain in C3 technical spec. AASL is the predecessor to C4 ASV.
**Fix:** Clarify AASL as the base layer; add note that C4 ASV is the canonical communication vocabulary.

### ME-04: C8/C7 Settlement Type Mapping Terminology
**Specs:** C8 (line ~2515), C7
**Issue:** C8 table header suggests RIF defines settlement types, but the canonical mapping (claim class → settlement type) lives in C9 SS7.3 with C8 implementing it.
**Fix:** Add clarifying text in C8 attributing the mapping to C9 canon.

### ME-05: C5 AVAP Committee Size Override Not Documented
**Spec:** C5
**Issue:** C9 errata E-C12-02 specifies AVAP overrides C5's per-class committee sizes (MIN=7, DEFAULT=10) when active. C5 doesn't mention this.
**Fix:** Add AVAP override note after C5's committee size table.

### ME-06: C11 Uses Deprecated "8+1" Claim Class Notation
**Spec:** C11 (line ~80)
**Issue:** Uses "8+1 claim class system" instead of "9-class taxonomy."
**Fix:** Replace with "9 canonical claim classes (D/C/P/R/E/S/K/H/N)."

### ME-07: C11 Missing Canonical Temporal Hierarchy References
**Spec:** C11
**Issue:** C11 makes no reference to SETTLEMENT_TICK/TIDAL_EPOCH/CONSOLIDATION_CYCLE despite timing-sensitive operations (60-second KI response window).
**Fix:** Add temporal hierarchy mapping in C11 introduction.

### ME-08: C13 Non-Canonical Parameter Naming
**Spec:** C13 (line ~1417)
**Issue:** Uses `CONSOLIDATION_CYCLE_EPOCHS` instead of canonical `EPOCHS_PER_CONSOLIDATION_CYCLE` (10).
**Fix:** Normalize parameter naming per C3/C9 conventions.

### ME-09: Defense Contract Matrix Not Mapped in C11-C13
**Specs:** C9 (lines ~926, 1213) vs C11/C12/C13
**Issue:** C9 defines a 9x9 defense contract matrix with 5 invariants (INV-D1 through INV-D5). C11/C12/C13 do not document compliance with this matrix.
**Fix:** Add defense invariant compliance section to each defense spec.

### ME-10: C17/C19 Modality Weight Redistribution Incomplete
**Specs:** C17 vs C19 (Section 19)
**Issue:** C19 lists required modifications to C17 but marks several as "Update" rather than "Replacement." Whether C17 has been updated to reflect C19's 6-modality weight redistribution is unclear.
**Fix:** Verify C17 includes trajectory modality placeholder; add C19 integration appendix.

### ME-11: Phase 0/1/2 Timing Inconsistencies Across C17/C19/C20/C21
**Specs:** C17, C19, C20, C21
**Issue:** "Phase 0/1/2" used interchangeably with "Month X" timelines across specs. C19 activates at "Phase 2" requiring 6 months pre-accumulation; C20 says "month 18"; C21 says "Phase 1." No unified phase-to-month mapping.
**Fix:** Create unified phase timeline mapping and add to C22 or C9.

### ME-12: FPR Parameter Numbering Inconsistency
**Specs:** C17 vs C21
**Issue:** C21 references "C17 P-21 — Constitutional" for FPR_hard_limit (0.1%) but also labels it P-01 internally. Parameter numbering not aligned.
**Fix:** Verify C17 P-21 definition; ensure C21 cross-references match.

### ME-13: C16 Nominating Body Count/Structure Underdocumented
**Spec:** C16
**Issue:** C16 requires "≥2 signed agreements (1 per category)" but doesn't explicitly define how "category" maps to tribunal seats, or whether multiple NB can share a seat.
**Fix:** Add explicit mapping: Category A (AI Governance) → Seat 3 primary; Category B (Law) → Seat 3 alternate/rotation. Minimum 2 NB = 1 per category.

---

## LOW Findings (8)

### LO-01: C3 AVAP Logic Attribution
C3 references AVAP committee formation logic that should be attributed to C12.

### LO-02: C5 Missing Verification Window Cross-Reference to C9 SS3.3
C5's verification timing should reference C9 intra-tidal-epoch timeline.

### LO-03: C4 Version Number Still Shows v1.0
C4 header says v1.0 despite v2.0 content (Appendix F addition).

### LO-04: C5 Cross-References Section Incomplete
C5 v2.0 integrates C11/C12 but cross-references don't list them explicitly.

### LO-05: C6/C13 Supersession Relationship Ambiguous
C6 "supersedes" C13 but C13 has no deprecation notice.

### LO-06: C15 ACI Data Source Definitions Partially Vague
C15 references "HDL telemetry" from C8 without expanding the acronym.

### LO-07: K-Class Terminology Migration Not Referenced in C15
C15 uses "K-class" without noting the C6/C9 relabeling history.

### LO-08: C12 Multi-Signal Fusion Reference Vague
C12 mentions "Multi-Signal Fusion replaces per-signal thresholds" without clear integration with C6 SHREC.

---

## Findings Summary

| Severity | Count | Key Themes |
|----------|-------|-----------|
| CRITICAL | 5 | Parameter conflict (1), budget/timeline mismatch (2), version staleness (1), claim class error (1) |
| HIGH | 9 | Deprecated references (3), missing integration docs (3), missing coverage (2), missing transition plan (1) |
| MEDIUM | 13 | Missing documentation (4), terminology (3), parameter naming (2), integration gaps (4) |
| LOW | 8 | Documentation clarity, cross-references, version numbers |

### By Spec (findings touching that spec)

| Spec | CRIT | HIGH | MED | LOW | Total |
|------|------|------|-----|-----|-------|
| C3 | 1 | 2 | 1 | 1 | 5 |
| C4 | — | — | — | 1 | 1 |
| C5 | — | — | 2 | 2 | 4 |
| C6 | 1* | 1 | 1 | 1 | 4 |
| C7 | — | — | 1 | — | 1 |
| C8 | — | — | 1 | — | 1 |
| C9 | — | — | 1 | — | 1 |
| C11 | 1* | — | 3 | — | 4 |
| C12 | 1 | 1 | — | 1 | 3 |
| C13 | 1* | — | 2 | 1 | 4 |
| C14 | — | 3 | — | — | 3 |
| C15 | — | 1 | — | 2 | 3 |
| C16 | — | — | 1 | — | 1 |
| C17 | — | — | 2 | — | 2 |
| C18 | 2* | 1* | — | — | 3 |
| C19 | — | — | 1 | — | 1 |
| C20 | — | — | 1* | — | 1 |
| C21 | — | — | 2* | — | 2 |
| C22 | 2* | 1 | — | — | 3 |

*Asterisk: finding shared with another spec*

---

## Recommended Fix Prioritization

### Batch 1 — CRITICAL (fix before any implementation)
1. **CR-01:** Correct C3 K-class aging rate to 0.005/TIDAL_EPOCH
2. **CR-02/CR-03:** Add budget/timeline scope reconciliation to C18 and C22
3. **CR-04:** Add deprecation headers to C11/C12/C13; update normative references to v2.0
4. **CR-05:** Fix C12 C-class definition from "Causal" to "Compliance"

### Batch 2 — HIGH (fix before W1 implementation)
5. HI-01/HI-09: Update C14 CCU references to C15 ACI; add transition plan
6. HI-02: Remove Verichain/CIOS from C3 dependency table
7. HI-03: Add conservatism ordering to C6
8. HI-04: Fix C3 K-class source requirements
9. HI-05: Add P/R-class honeypot coverage to C12
10. HI-06/HI-07: Update C14 cross-references and settlement stream mapping
11. HI-08: Add scope statement to C22 budget section

### Batch 3 — MEDIUM (fix during W1-W2)
12-24. Documentation clarifications, parameter naming, terminology normalization, integration gap closures

### Batch 4 — LOW (fix opportunistically)
25-32. Cross-reference additions, version number corrections, cosmetic fixes

---

## Assessment

**Overall architecture health: SOUND.** The 5 v2.0 core specs (C3/C5/C6/C7/C8) are well-reconciled with each other per C9. The primary consistency issues are:

1. **Temporal gap between v2.0 rewrites and post-v2.0 specs** — C11/C12/C13 were written before v2.0 rewrites and their references became stale when v2.0 claimed supersession.

2. **Scope ambiguity between C18/C22** — Budget and timeline differences are explainable by scope difference (engineering vs fully-loaded) but this is not documented.

3. **Parameter propagation lag** — When C9/C15 changed canonical values or models, not all downstream specs were updated (C3 aging rate, C14 CCU).

None of these represent architectural contradictions. All are fixable through targeted errata without redesign.

---

*Audit complete. 35 findings across 19 specifications. 0 unfixable architectural conflicts.*
