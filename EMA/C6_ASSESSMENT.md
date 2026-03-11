# C6 EMA — Assessment Report

**Invention:** C6 — Epistemic Metabolism Architecture (EMA)
**Document Under Review:** Master Technical Specification v1.0.0 (2026-03-10)
**Assessment Date:** 2026-03-10
**Assessors:** Simplification Agent, Completeness Reviewer
**Protocol:** Atrahasis Agent System v2.0, ASSESSMENT Stage

---

## Part 1: Simplification Agent Review

### 1.1 Overall Scores

| Metric | Score | Rationale |
|--------|-------|-----------|
| **Complexity** | **8/10** | Nine components, five metabolic phases per epoch, a five-signal ecological regulator modeled on Lotka-Volterra dynamics with PID overlay, a three-pass LLM dreaming pipeline with PCVM gating, five edge types with Hebbian dynamics, three projection functions with fidelity monitoring, 60+ configurable parameters (Appendix D), and tight integration contracts with C3/C4/C5. This is the most complex C-series invention to date. |
| **Achievability** | **4/10** | Four hard gates remain experimentally unvalidated (SHREC stability, coherence graph scaling, consolidation provenance diversity, dreaming precision). The dreaming pipeline depends on LLM consolidation producing genuine cross-domain insights — an unproven capability. SHREC stability is proven only locally via linearized Lyapunov analysis. The spec is honest about these risks (Section 13), which is commendable but does not reduce them. An engineer could build the scaffolding, but whether the system produces value beyond a simpler knowledge graph with TTL expiry is genuinely uncertain. |

### 1.2 Per-Component Complexity Assessment

#### Component 1: Quantum Engine (create, store, manage lifecycle)
- **Earns its complexity?** YES
- **Rationale:** The 10-tuple epistemic quantum (Section 4.1) is the foundational data structure. Each field is justified: content carries the claim, opinion carries Subjective Logic confidence, provenance satisfies W3C PROV auditability, edges encode relationships, metabolic_state drives lifecycle, projections cache subsystem views, timestamps enable temporal queries, dissolution_record preserves audit trail, claim_class aligns with PCVM taxonomy. The JSON schema (Appendix A) is complete and implementable.
- **Over-engineered elements:** None. This is the cleanest component in the spec.

#### Component 2: Ingestion Pipeline
- **Earns its complexity?** YES
- **Rationale:** Nine-step ingestion protocol (Section 5.1) is procedurally clear. The ASV-to-Quantum field mapping table and Claim Class-to-Claim Type mapping table are precise enough to implement directly. Initial edge discovery via embedding similarity is a standard technique applied well.
- **Over-engineered elements:** The claim decomposition step ("Most claims map 1:1. Compound claims decompose into atomic sub-claims") is mentioned but not specified. What constitutes a "compound claim"? What decomposition algorithm is used? This is under-specified rather than over-engineered.
- **Simplification opportunity:** LOW. Could defer compound claim decomposition to a later version and require 1:1 mapping initially.

#### Component 3: Coherence Graph
- **Earns its complexity?** YES
- **Rationale:** Five typed edges (Section 4.5) with distinct semantics, Hebbian reinforcement, temporal decay, edge budgets, and three scale tiers. The sharding strategy aligned with C3 parcel topology is architecturally clean. The active edge budget (50 per quantum, 500K per shard) provides concrete bounds.
- **Over-engineered elements:** The edge ranking formula for budget enforcement (Section 7.4) uses a cross_shard_bonus factor that is never defined. What is its value? How is it computed?
- **Simplification opportunity:** LOW. The graph is the circulatory system; it needs this structure.

#### Component 4: Circulation Engine
- **Earns its complexity?** PARTIALLY
- **Rationale:** The subscription model and relevance ranking formula (Section 5.2) are reasonable. Priority push for contradictions and supersessions is well-motivated.
- **Over-engineered elements:** The five-factor relevance formula (domain 0.30, opinion 0.20, recency 0.15, vitality 0.15, novelty 0.20) introduces five tunable weights whose optimal values are unknown. The spec provides defaults but no empirical basis for choosing them. This is a parameter tuning exercise disguised as specification.
- **Simplification opportunity:** MEDIUM. Could start with a simpler two-factor ranking (domain match + credibility) and add sophistication based on operational data.

#### Component 5: Consolidation Engine (Dreaming)
- **Earns its complexity?** THE QUESTION IS WHETHER IT WORKS AT ALL
- **Rationale:** This is EMA's highest-risk, highest-reward component. The three-pass LLM synthesis with majority voting (Section 5.3.4) is novel. Provenance diversity verification (Section 5.3.2) is well-specified with four concrete requirements. The PCVM verification gate (Section 5.3.5) provides a meaningful quality filter. C-class aging uncertainty (Section 5.3.6) is a principled defense against unfalsifiable consolidations.
- **Over-engineered elements:** Three synthesis passes (inductive, analogy, predictive) with majority voting across all three is expensive. The claim similarity clustering at threshold 0.8 for majority voting is a hyperparameter with no theoretical justification.
- **Critical concern:** The spec treats dreaming as the core innovation but honestly admits (Section 13.2, Section 14) that if dreaming does not produce genuine insights, EMA reduces to "an expensive knowledge graph." This honesty is appropriate but means the entire metabolic architecture is a bet on an unproven capability.
- **Simplification opportunity:** HIGH. If dreaming fails HG-4, the spec should define a graceful degradation path more precisely. Currently it says "restrict to within-domain patterns only, or eliminate entirely" but does not specify what the fallback architecture looks like.

#### Component 6: Catabolism Engine
- **Earns its complexity?** YES
- **Rationale:** Two-phase dissolution (quarantine then dissolution) with component recycling (Section 5.4) is well-motivated. Structural protection (citation count >= 10, keystone detection) prevents loss of foundational knowledge. The immune self-audit (Section 6.8) detecting autoimmune behavior (catabolism attacking valid knowledge) is an elegant self-correction mechanism.
- **Over-engineered elements:** Evidence recycling during dissolution (transferring evidence from dissolved quanta to surviving quanta with domain overlap) is conceptually appealing but operationally vague. How does the system determine which evidence is worth recycling to which recipient? The `execute_recycling` function is called but never defined.
- **Simplification opportunity:** LOW. Catabolism without structural protection would be dangerous. The two-phase approach is prudent.

#### Component 7: SHREC Controller
- **Earns its complexity?** PARTIALLY
- **Rationale:** Five competing signals governed by Lotka-Volterra dynamics with PID overlay, four operating regimes, Bayesian cold-start priors, CUSUM change-point detection, and regime hysteresis. This is the second most complex component after dreaming. The biological analogy (homeostatic regulation) generates genuine architectural predictions, and the niche differentiation argument (each signal has a primary resource dimension) is sound.
- **Over-engineered elements:** The full Lotka-Volterra competitive dynamics may be unnecessary. The spec itself acknowledges (Section 6.9, Section 13.1) that if SHREC exhibits competitive exclusion or sustained oscillation, "the Lotka-Volterra model must be replaced with simpler priority-weighted allocation." The fallback is simpler and may work just as well. The PID overlay with auto-derived gains (Kp from sigma, Ki and Kd from window) adds a second control system on top of the ecological dynamics — two control loops governing the same budget is architecturally redundant.
- **Simplification opportunity:** HIGH. Start with priority-weighted allocation + floor guarantees (the fallback system). Add Lotka-Volterra only if priority-weighted allocation demonstrably fails. The PID overlay should be the primary controller OR the Lotka-Volterra should be the primary controller — not both layered.

#### Component 8: Projection Engine
- **Earns its complexity?** YES
- **Rationale:** Three projection functions (C3, C4, C5) with explicit preservation/loss documentation, round-trip fidelity metrics, and cache management with three consistency levels. The "bounded information loss" principle (Section 3.2, Principle 4) is a genuine contribution — most systems pretend projections are lossless.
- **Over-engineered elements:** The fidelity metrics themselves are untested. The C3 fidelity formula (0.5 * text_similarity + 0.3 * opinion_preservation + 0.2 * edge_jaccard) is reasonable but the weights are arbitrary. More importantly, "round-trip fidelity" requires a reconstruction function (projection -> canonical) that is never specified.
- **Simplification opportunity:** LOW-MEDIUM. The round-trip fidelity concept needs a defined reconstruction function, but the projection functions themselves are appropriately scoped.

#### Component 9: Retrieval Interface
- **Earns its complexity?** YES
- **Rationale:** Four query types (semantic, structural, temporal, metabolic-state) are a minimal but complete set. The relevance ranking formula is straightforward. Context-aware retrieval via graph neighbor boosting is a reasonable feature.
- **Over-engineered elements:** None. This is one of the simpler components.

### 1.3 Specific Findings

| # | Finding | Severity | Component |
|---|---------|----------|-----------|
| F1 | **SHREC uses two overlapping control systems (Lotka-Volterra + PID) with no clear specification of how they interact.** Section 6.4 defines ecological competition. Section 6.7 defines PID overlay. But the PID output modifies the same budget allocations that Lotka-Volterra produces. How are the two combined? Additively? Does PID override Lotka-Volterra in ELEVATED+ regimes? The interaction is ambiguous. | **CRITICAL** | SHREC Controller |
| F2 | **The `execute_recycling` function is called in dissolution (Section 5.4.3) but never defined.** The spec says evidence is "redistributed to surviving knowledge" but provides no algorithm for selecting recipients, determining which evidence to transfer, or handling conflicts when evidence contradicts the recipient. An implementer cannot build this from the spec. | **HIGH** | Catabolism Engine |
| F3 | **Round-trip fidelity requires a reconstruction function (projection -> canonical) that is never specified.** Section 8.5 monitors "round-trip fidelity" but only defines the forward projection functions (canonical -> projection). Without the inverse function, fidelity cannot be computed. | **HIGH** | Projection Engine |
| F4 | **The cross_shard_bonus used in edge budget ranking (Section 7.4) is referenced but never defined.** Its value, computation method, and rationale are absent. | **MEDIUM** | Coherence Graph |
| F5 | **Claim decomposition for compound claims is mentioned but not specified.** Section 5.1 says "Compound claims decompose into atomic sub-claims" but provides no algorithm, no definition of "compound," and no examples beyond the trivial 1:1 case. | **MEDIUM** | Ingestion Pipeline |
| F6 | **The Lotka-Volterra discrete-time implementation (Appendix C.2) multiplies dS by signals[name] AFTER computing the Lotka-Volterra dynamics.** This means signal intensity modulates the growth rate multiplicatively, which could drive dS to zero when signal intensity is zero — even if the signal's floor has been breached. The floor correction is applied before the signal multiplication, so a zero-intensity signal with below-floor allocation would still not recover. | **HIGH** | SHREC Controller |
| F7 | **60+ configurable parameters with no recommended deployment profiles.** Appendix D lists parameters with ranges but no guidance on which parameter sets are appropriate for T1 vs T2 vs T3 deployments. The combinatorial parameter space is unmanageable without profiles. | **MEDIUM** | Configuration |
| F8 | **The vitality computation (Section 4.4) uses multiplicative composition, meaning any single factor near zero drives vitality to zero.** If access_recency drops to 0.1 (neglected quantum), vitality collapses regardless of high support and high credibility. This is by design ("all factors must be healthy") but may cause premature catabolism of valuable-but-currently-unfashionable knowledge. | **MEDIUM** | Quantum Engine |
| F9 | **Test Vector TV-6 (Per-Agent Contradiction Cap) claims edges 4-5 are "rejected" but the spec never defines rejection behavior for cap-exceeding contradiction edges.** Does the system refuse to create the edge? Does it create the edge but cap the weight? Does it redistribute weight across existing edges? The enforcement mechanism is unspecified. | **MEDIUM** | Coherence Graph |
| F10 | **The immune self-audit (Section 6.8) samples 10% of recently quarantined quanta, but "recently" is undefined.** What is the lookback window? How is "recently quarantined" distinguished from "quarantined for 90 epochs"? | **LOW** | SHREC Controller |
| F11 | **Dreaming synthesis temperature is set to 0.3 (Section 5.3.4, Appendix D) which is very low for creative cross-domain pattern detection.** Low temperature favors conventional outputs. The dreaming pipeline's purpose is to discover novel patterns — a task that typically benefits from higher temperature. This creates a tension between synthesis novelty and output reliability. | **LOW** | Consolidation Engine |
| F12 | **The spec does not define behavior when PCVM is unavailable.** If PCVM experiences an outage, ingestion halts (no MCTs), consolidation halts (no C-class verification), and re-verification cannot proceed. There is no degraded-mode specification. | **LOW** | Integration |

### 1.4 Verdict

**APPROVE WITH RECOMMENDATIONS**

EMA is a genuinely novel architecture. The metabolic framing produces architectural predictions (dreaming consolidation, ecological self-regulation, vitality-based lifecycle) that would not emerge from conventional knowledge management design. The spec is thorough, honest about its risks, and provides sufficient detail for implementation of most components.

However, complexity is at the upper bound of what is manageable. The dual-controller SHREC system (F1) is the most urgent architectural issue — it must be clarified before implementation. The dreaming pipeline is the make-or-break component; if HG-4 fails, the architecture needs a well-defined fallback that is not currently specified.

### 1.5 Recommendations

1. **CRITICAL: Resolve SHREC dual-controller interaction (F1).** Specify whether PID overrides or supplements Lotka-Volterra in ELEVATED+ regimes. Recommendation: use Lotka-Volterra in NORMAL, switch entirely to PID in ELEVATED+, rather than layering both.
2. **HIGH: Fix Lotka-Volterra signal multiplication ordering (F6).** Move signal intensity multiplication before floor correction, or apply floor correction after signal multiplication, to prevent zero-intensity signals from blocking floor recovery.
3. **HIGH: Define execute_recycling algorithm (F2).** At minimum: select top-K surviving quanta by domain tag overlap, transfer evidence items with weight > 0.5, skip evidence that contradicts the recipient's claim.
4. **HIGH: Define reconstruction functions for round-trip fidelity (F3).** Each projection needs an inverse (or approximate inverse) to make the fidelity metric computable.
5. **MEDIUM: Define dreaming fallback architecture.** If HG-4 fails, specify the exact reduced system: which components are removed, which parameters change, what the resulting architecture looks like.
6. **MEDIUM: Provide deployment parameter profiles.** Define T1-minimal, T2-standard, and T3-scaled parameter profiles in Appendix D.
7. **LOW: Consider additive vitality composition (F8).** Weighted sum instead of product would prevent single-factor collapse. Trade-off: product enforces "all factors must be healthy," sum allows compensation. The choice should be explicit and justified.

---

## Part 2: Completeness and Consistency Check

### 2.1 Completeness Assessment

| Dimension | Score | Analysis |
|-----------|-------|----------|
| **Completeness** | **4/5** | The spec covers all nine components with pseudocode, data structures, integration contracts, security analysis, scalability analysis, conformance requirements, and test vectors. Two gaps prevent a 5: (1) execute_recycling is called but never defined, (2) reconstruction functions for round-trip fidelity are absent. These are implementation-blocking gaps. |

**Detailed completeness by section:**

| Section | Complete? | Gaps |
|---------|-----------|------|
| 1. Introduction | YES | None |
| 2. Background | YES | Thorough coverage of prior art, honest about MemOS as closest competitor |
| 3. Architecture Overview | YES | 10 invariants, 9 components, 5 phases — all well-defined |
| 4. Epistemic Quantum | YES | 10-tuple fully specified, JSON schema in Appendix A, lifecycle state machine complete, vitality computation with test vector |
| 5. Metabolic Processes | MOSTLY | Ingestion, circulation, consolidation, catabolism all have pseudocode. Gap: execute_recycling undefined. Gap: compound claim decomposition undefined. |
| 6. SHREC | MOSTLY | Signal computation, budget, Lotka-Volterra, floors, self-model, regimes — all specified. Gap: dual-controller interaction (F1). Gap: signal multiplication ordering (F6). |
| 7. Coherence Graph | YES | Sharding, edge dynamics, budget, scale tiers, bridge detection — complete |
| 8. Projection Engine | MOSTLY | Forward projections specified. Gap: reconstruction functions for fidelity measurement. |
| 9. Retrieval | YES | Four query types, ranking, context-aware retrieval — complete |
| 10. Integration | YES | All five interfaces (PCVM, C3, C4, Settlement, Sentinel) specified bidirectionally |
| 11. Security | YES | 5 attacks analyzed with mitigations and residual risks. Honest. |
| 12. Scalability | YES | Three tiers, complexity analysis, cost model with honest assessment |
| 13. Open Questions | YES | Five open questions honestly stated |
| 14. Conclusion | YES | Balanced, acknowledges risks |
| Appendix A | YES | Complete JSON schema |
| Appendix B | YES (pointer) | References Section 6.2 |
| Appendix C | YES | Lotka-Volterra equations, discrete implementation, coexistence conditions, Lyapunov |
| Appendix D | YES | 60+ parameters with defaults, ranges, and section references |
| Appendix E | YES | 24 MUST, 12 SHOULD, 7 MAY requirements |
| Appendix F | YES | 8 test vectors covering key operations |
| Appendix G | YES | Traceability from hard gates / required actions to sections and CRs |
| Appendix H | YES | Comprehensive glossary |

### 2.2 Consistency Assessment

| Dimension | Score | Analysis |
|-----------|-------|----------|
| **Consistency** | **4/5** | Internal terminology is consistent throughout. Data structures match between prose, pseudocode, and JSON schema. Two issues prevent a 5: (1) the SHREC dual-controller ambiguity (F1) is an internal consistency issue — two subsections describe overlapping control authority without specifying precedence, (2) Test Vector TV-6 describes behavior ("rejected") not defined in the normative spec. |

**Specific consistency checks:**

| Check | Result |
|-------|--------|
| Quantum 10-tuple fields match between Section 4.1 and Appendix A JSON schema | PASS — all 10 fields present in both |
| Edge types match between Section 4.5 table and JSON schema enum | PASS — 5 types match exactly |
| Lifecycle states match between Section 4.3 state machine and JSON schema enum | PASS — 5 states match |
| Claim classes match between ingestion mapping (Section 5.1) and JSON schema enum | PASS — 8 classes match (D/E/S/H/N/P/R/C) |
| SHREC signal names match between Section 6.1 table and Section 6.2 pseudocode | PASS — H/C/S/I/N in both |
| Floor allocations match between Section 6.1 table and Section 6.5 code | PASS — all 5 match (15/10/8/5/5 = 43%) |
| Conformance requirements reference correct sections | PASS — spot-checked CR-1 through CR-24 |
| Test vectors compute correctly against pseudocode | PASS — TV-2 vitality computation verified: 0.7788 * 0.8187 * 0.68 * 0.925 * 0.8 = 0.321. Correct. |
| Parameter defaults in Appendix D match in-text defaults | PASS — checked DECAY_THRESHOLD (0.30), CONSOLIDATION_LOCK_TTL (5), MAX_EDGES_PER_QUANTUM (50) |

### 2.3 Implementation Readiness Assessment

| Dimension | Score | Analysis |
|-----------|-------|----------|
| **Implementation Readiness** | **4/5** | An engineer could build 7 of 9 components directly from this spec. The Quantum Engine, Ingestion Pipeline, Coherence Graph, Circulation Engine, Catabolism Engine (minus recycling), Projection Engine (minus reconstruction), and Retrieval Interface are all specified to implementation level with pseudocode, data structures, and test vectors. Two components have gaps: (1) Consolidation Engine depends on unspecified LLM prompt engineering (the prompt_inductive, prompt_analogy, prompt_predictive functions are placeholders), (2) SHREC Controller has the dual-controller ambiguity. |

**Implementation readiness by component:**

| Component | Readiness | Blocking Issues |
|-----------|-----------|-----------------|
| Quantum Engine | HIGH | None |
| Ingestion Pipeline | HIGH | Compound claim decomposition undefined (non-blocking for 1:1 path) |
| Coherence Graph | HIGH | cross_shard_bonus undefined (minor) |
| Circulation Engine | HIGH | None |
| Consolidation Engine | MEDIUM | LLM prompts are placeholders; similarity clustering threshold unvalidated |
| Catabolism Engine | MEDIUM-HIGH | execute_recycling undefined |
| SHREC Controller | MEDIUM | Dual-controller interaction ambiguous; signal multiplication ordering bug |
| Projection Engine | MEDIUM-HIGH | Reconstruction functions undefined |
| Retrieval Interface | HIGH | None |

### 2.4 Cross-Document Consistency

| Cross-Reference | Status | Issues |
|----------------|--------|--------|
| **C3 (Tidal Noosphere) alignment** | GOOD | EMA correctly references C3 epoch boundaries, parcel topology, locus namespace, and VRF committees. Sharding aligns with C3 parcel structure. Epoch-boundary metabolic phases sync with C3 temporal model. The C3 projection preserves locus/parcel/epoch data appropriately. |
| **C4 (ASV) alignment** | GOOD | The ASV-to-Quantum field mapping (Section 5.1) explicitly maps CLM/CNF/EVD/PRV/VRF tokens to quantum fields. The C4 projection preserves full Subjective Logic opinions (which ASV natively supports). Claim class mapping table covers all 8 PCVM classes. |
| **C5 (PCVM) alignment** | GOOD | EMA correctly depends on MCTs for ingestion gating (INV-E2). C-class claims from dreaming are submitted back to PCVM for verification. The 8 claim classes (D/E/S/H/N/P/R/C) match C5's taxonomy exactly. Subjective Logic opinion format is consistent. |
| **C5 claim class expansion vs C3** | KNOWN ISSUE | C5's assessment (F2 in C5_ASSESSMENT) already flagged that C5 expanded from 5 to 8 claim classes relative to C3. EMA inherits this expansion. This is a C3 update requirement, not an EMA defect. |
| **Settlement Plane interface** | PARTIALLY SPECIFIED | EMA defines outbound metabolic efficiency reports and agent contribution scores, and inbound reward signals. The Settlement Plane itself is not yet specified as a C-series invention. Interface is defined from EMA's side only. |
| **Sentinel Graph interface** | PARTIALLY SPECIFIED | EMA defines health metrics and anomaly reporting outbound, and system alerts inbound. Sentinel Graph is not yet specified. Same situation as Settlement. |

### 2.5 Specific Issues

| # | Issue | Severity | Category |
|---|-------|----------|----------|
| I1 | SHREC dual-controller interaction unspecified (same as F1) | **CRITICAL** | Consistency |
| I2 | execute_recycling undefined (same as F2) | **HIGH** | Completeness |
| I3 | Reconstruction functions for fidelity undefined (same as F3) | **HIGH** | Completeness |
| I4 | Lotka-Volterra signal multiplication ordering issue (same as F6) | **HIGH** | Correctness |
| I5 | TV-6 describes "rejection" behavior not defined in normative spec (same as F9) | **MEDIUM** | Consistency |
| I6 | Compound claim decomposition unspecified (same as F5) | **MEDIUM** | Completeness |
| I7 | Dreaming LLM prompts are placeholders, not implementable specifications | **MEDIUM** | Implementation Readiness |
| I8 | No degraded-mode specification for PCVM outage (same as F12) | **LOW** | Completeness |
| I9 | Settlement Plane and Sentinel Graph interfaces only specified from EMA side | **LOW** | Cross-Document |

---

## Summary Scorecard

| Dimension | Score | Assessment |
|-----------|-------|------------|
| Complexity | 8/10 | Highest in the C-series. Justified by problem scope but at manageability limit. |
| Achievability | 4/10 | Four hard gates unvalidated. Dreaming is an unproven bet. SHREC stability is local only. |
| Completeness | 4/5 | Two implementation-blocking gaps (recycling algorithm, reconstruction functions). |
| Consistency | 4/5 | One internal ambiguity (SHREC dual-controller). One test vector / spec mismatch. |
| Implementation Readiness | 4/5 | 7 of 9 components at HIGH readiness. Two at MEDIUM due to gaps. |
| Cross-Document Consistency | 4/5 | C3/C4/C5 alignment is solid. Two unspecified external systems (Settlement, Sentinel) are acceptable given pipeline ordering. |

**Verdict: APPROVE WITH RECOMMENDATIONS**

EMA is a well-specified, genuinely novel architecture that earns its complexity through the metabolic framing. The spec is notably honest about its risks and open questions. The four findings requiring action before implementation are:

1. **CRITICAL:** Resolve SHREC dual-controller interaction.
2. **HIGH:** Fix Lotka-Volterra signal multiplication ordering.
3. **HIGH:** Define execute_recycling algorithm.
4. **HIGH:** Define reconstruction functions for round-trip fidelity.

All other findings are addressable during implementation without architectural changes.

---

*Assessment performed under Atrahasis Agent System v2.0 protocol.*
*C6: Epistemic Metabolism Architecture (EMA) -- ASSESSMENT COMPLETE.*
*Pipeline status: C6 COMPLETE.*
