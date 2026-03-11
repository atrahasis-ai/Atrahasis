# C9 — Cross-Document Reconciliation: Inconsistency Inventory

**Stage:** IDEATION
**Date:** 2026-03-10
**Role:** Synthesis Engineer + Domain Translator

---

## 1. Executive Summary

A comprehensive cross-layer scan of all 6 Master Tech Specs (C3, C4, C5, C6, C7, C8) reveals **4 HIGH-severity**, **3 MEDIUM-severity**, and **4 LOW-severity** inconsistencies. No CRITICAL (system-breaking) inconsistencies exist — the architecture is fundamentally sound — but the HIGH findings require resolution before any implementation begins.

---

## 2. Inconsistency Inventory

### INC-01 — EPOCH DURATION CONFLICT [HIGH]

**Layers:** C3, C5, C8
**Nature:** The three layers that define concrete epoch durations use incompatible values.

| Layer | Value | Location |
|-------|-------|----------|
| C3 | 3600s (1 hour), configurable [60s, 86400s] | Line 623, Line 2228 |
| C5 | "1-hour tidal epoch clock" (T+0 to T+60min) | Line 1046 |
| C8 | 60s (60000ms), no configurable range stated | Line 325, Line 1022, Line 2302 |

**Impact:** C8's settlement cycles, staleness bounds, and throughput benchmarks are all calibrated to 60s epochs. C3's entire parameter table, diversity cooling (50 epochs = 50 hours at 3600s vs 50 minutes at 60s), and settlement rates assume 3600s. C5's verification window (T+0 to T+50min) is meaningless with 60s epochs.

**Root Cause:** C8 was designed after C3 and optimized for settlement throughput. C3 was designed for coordination at planetary scale where 1-hour epochs reduce overhead. Neither spec acknowledges the other's timing.

---

### INC-02 — CLAIM CLASS "C" SEMANTIC COLLISION [HIGH]

**Layers:** C5, C6
**Nature:** Both specs use "C-class" but with completely different meanings.

| Layer | C-class Meaning | Definition |
|-------|-----------------|------------|
| C5 | **Compliance** | "A claim that a system, process, or output conforms to a specified regulation, standard, or constitutional parameter." (Line 447) |
| C6 | **Consolidation** | "From dreaming" — consolidation outputs from EMA's dreaming process (Line 478, Line 2031) |

**Impact:** C6's mapping table (Line 469-478) maps "C (Consolidation)" as an EMA type, but C5's canonical taxonomy defines C as Compliance. C6 submits dreaming outputs to PCVM "as C-class claims" (Line 568), but PCVM would interpret these as Compliance claims and apply Compliance verification (formal proof tier), which is wrong for consolidation outputs.

**Root Cause:** C6 co-opted the letter "C" for its novel consolidation concept without checking C5's existing assignment.

---

### INC-03 — C4 COMPLETE ISOLATION FROM STACK [HIGH]

**Layers:** C4 vs. all others
**Nature:** C4 (ASV) contains ZERO references to any layer in the architecture stack (C3, C5, C6, C7, C8). It defines 6 epistemic classes that share no mapping with C5's 8 canonical claim classes.

| C4 Epistemic Classes | C5 Claim Classes |
|---------------------|-----------------|
| observation | D (Deterministic), E (Empirical) |
| correlation | S (Statistical) |
| causation | (no direct mapping) |
| inference | R (Reasoning), H (Heuristic) |
| prediction | (no direct mapping) |
| prescription | N (Normative) |

**Impact:** C6 says "AASL messages are converted to VTD drafts" (Line 1312) and C7 says "RIF uses ASV claim schemas" (Line 157), but C4 has no conversion logic, no claim class mapping, and no integration contracts. Any implementation would have to invent this mapping.

**Root Cause:** C4 was designed as a transport-agnostic vocabulary layer positioned against A2A/MCP, not as an integrated component of the Atrahasis stack.

---

### INC-04 — C8 CLAIM CLASS SUBSET MISMATCH [HIGH]

**Layers:** C5, C8
**Nature:** C8 maps only 5 claim classes (D/E/S/H/N) to difficulty weights (Lines 3837-3841), and treats P/R/C as "modifiers" rather than claim classes.

| C5 Class | C8 Treatment |
|----------|-------------|
| D (Deterministic) | Difficulty weight 1.0 |
| E (Empirical) | Difficulty weight 1.5 |
| S (Statistical) | Difficulty weight 2.0 |
| H (Heuristic) | Difficulty weight 2.5 |
| N (Normative) | Difficulty weight 3.0 |
| P (Process) | **Treated as modifier** (x1.0) |
| R (Reasoning) | **Treated as modifier** (x0.7) |
| C (Compliance) | **Treated as modifier** (x1.3) |

**Impact:** C5's P/R/C are full claim classes with their own verification tiers, admission thresholds, and Subjective Logic parameters. C8 treating them as multipliers loses the class-specific settlement logic. A P-class claim should settle differently from a D-class claim modified by "P".

**Root Cause:** C8's author interpreted C5's 8-class taxonomy as 5 base classes + 3 modifiers, possibly misreading "P (Primary), R (Replication), C (Challenge)" as claim assessment modifiers rather than the actual C5 definitions of "P (Process), R (Reasoning), C (Compliance)".

---

### INC-05 — C3 BACKWARD ISOLATION [MEDIUM]

**Layers:** C3 vs. all others
**Nature:** C3 references only predecessor specs (Noosphere Master Spec v5, PTA, Locus Fabric). It has no references to C4, C5, C6, C7, or C8. Other layers reference C3 extensively.

**Impact:** C3's integration contracts (Section 7, Lines 1254-1303) describe internal cross-integration (hash rings, VRF, communication, governance, AASL extension) but not inter-layer contracts. This means all integration specifications are unilateral — defined only by the consuming layer.

**Resolution Difficulty:** LOW — C3 doesn't need to be modified. The consuming layers define the contracts. But a reconciliation addendum should confirm that C3's exported interfaces match what consumers expect.

---

### INC-06 — CLAIM CLASS NAME vs. LETTER INCONSISTENCY [MEDIUM]

**Layers:** C3, C5
**Nature:** C3 uses full names (deterministic, empirical, statistical, heuristic, normative). C5 uses single letters (D/E/S/H/N/P/R/C). The 5-to-8 expansion is unacknowledged.

| C3 Name | C5 Letter | Match? |
|---------|-----------|--------|
| deterministic | D | Yes |
| empirical | E | Yes |
| statistical | S | Yes |
| heuristic | H | Yes |
| normative | N | Yes |
| (none) | P (Process) | C3 missing |
| (none) | R (Reasoning) | C3 missing |
| (none) | C (Compliance) | C3 missing |

**Impact:** C3's verification pathways (Line 800-808) don't cover P/R/C classes. Any P/R/C claim entering the Noosphere would have no defined verification pathway in C3.

---

### INC-07 — SETTLEMENT STREAM WEIGHT ASYMMETRY [MEDIUM]

**Layers:** C3, C8
**Nature:** C3 defines four settlement streams with rate parameters but no percentage weights. C8 defines the same four streams with specific weights: 40/40/10/10.

| Stream | C3 Rate Parameter | C8 Weight |
|--------|-------------------|-----------|
| Scheduling Compliance | COMPLIANCE_RATE = 0.001 AIC/unit | 40% |
| Verification Quality | VERIFICATION_RATE = 0.002 AIC/unit | 40% |
| Communication Efficiency | COMM_RATE = 0.0005 AIC/unit | 10% |
| Governance Participation | GOV_RATE = 0.003 AIC/unit | 10% |

**Impact:** The rate ratios in C3 (1:2:0.5:3) don't match C8's percentage weights (4:4:1:1). Under C3, governance has the highest rate; under C8, it's 10%.

---

### INC-08 — C5 VERIFICATION COMMITTEE SIZES UNCONFIRMED BY C3 [LOW]

**Layers:** C3, C5
**Nature:** C5 defines committee sizes (Tier 1: 3, Tier 2: 5, Tier 3: 7) at Line 1048-1051. C3's VRF engine doesn't specify committee sizes per verification tier.

**Impact:** Minor — C5 is the authoritative source for verification parameters.

---

### INC-09 — C6 PROJECTION TARGETS REFERENCE NON-EXISTENT C4 INTERFACE [LOW]

**Layers:** C4, C6
**Nature:** C6 defines projection fidelity targets for C4 (0.88) and maps ASV fields to quantum fields (Lines 458-465), but C4 has no awareness of EMA or projection interfaces.

**Impact:** Low — C6 defines the mapping unilaterally, and C4's JSON Schema is stable enough to map against.

---

### INC-10 — C7 SETTLEMENT ROUTER REFERENCES C3 LEDGER, NOT C8 [LOW]

**Layers:** C7, C8
**Nature:** C7's Settlement Router "forwards all intent-related transactions to the C3 settlement ledger" (Line 3028-3050). But C8 (DSF) is the actual settlement layer. C7 should reference C8, not C3.

**Impact:** Architectural confusion — C3 has a settlement calculator component (Component #11), but C8/DSF is the canonical settlement layer.

---

### INC-11 — C3 CLAIM TYPE vs. C5 CLAIM CLASS ORTHOGONALITY [LOW]

**Layers:** C3, C5
**Nature:** C3 defines `claim_type: {observation, derivation, synthesis, hypothesis, prediction}` as orthogonal to `claim_class`. C4 defines `epistemic_class: {observation, correlation, causation, inference, prediction, prescription}`. These overlap (observation, prediction appear in both) but serve different purposes.

**Impact:** Naming collision risk. C3's `claim_type` and C4's `epistemic_class` share terms but mean different things.

---

## 3. Reconciliation Concept

**Approach:** Produce a **Cross-Layer Reconciliation Addendum** — a single canonical document that:

1. **Establishes C5 as the authoritative claim class taxonomy** (8 classes, D/E/S/H/N/P/R/C)
2. **Resolves INC-02** by renaming C6's consolidation output class (proposal: "K-class" for Knowledge consolidation, or submit as C-class Compliance with a specific sub-type)
3. **Resolves INC-01** by establishing a canonical epoch duration with layer-specific sub-epoch timing
4. **Resolves INC-03** by adding a C4 Integration Appendix that maps epistemic_class → claim_class
5. **Resolves INC-04** by extending C8's difficulty weights to all 8 classes
6. **Produces canonical cross-layer type definitions** that all specs can reference

This addendum does NOT modify the existing Master Tech Specs — it serves as the integration specification that bridges them.

---

## 4. Council Vote

| Role | Vote | Rationale |
|------|------|-----------|
| Synthesis Engineer | APPROVE | All inconsistencies are resolvable without architectural redesign |
| Domain Translator | APPROVE | C4 isolation is the hardest problem but solvable with a mapping appendix |
| Systems Thinker | APPROVE | Epoch duration requires a principled choice, not a compromise |
| Critic | APPROVE WITH CAVEAT | INC-02 (C-class collision) could cascade if not handled carefully |

**Decision:** PROCEED to RESEARCH synthesis and FEASIBILITY assessment.
