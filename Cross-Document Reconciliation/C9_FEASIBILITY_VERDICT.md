# C9 — Cross-Document Reconciliation: Feasibility Verdict

**Stage:** FEASIBILITY
**Date:** 2026-03-10
**Roles:** Assessment Council (Advocate, Skeptic, Arbiter)

---

## 1. Feasibility Assessment

### Advocate Position

All 11 inconsistencies are resolvable without architectural redesign. The architecture is fundamentally sound — every layer serves its intended purpose, and the inter-layer contracts defined by C6/C7/C8 are detailed and mostly consistent. The inconsistencies are specification-level gaps, not design-level contradictions.

Key argument: The 6-layer stack was designed incrementally (C3 first, C8 last). Each later layer was written with knowledge of earlier layers, creating a natural forward-referencing pattern. The reconciliation task is to add the missing backward references and resolve the handful of naming/parameter conflicts.

### Skeptic Position

INC-01 (epoch duration) is not a simple parameter change. C3's entire timing model (3600s epochs, 5s boundary windows, 50-epoch cooling = 50 hours) is calibrated for planetary-scale coordination with low overhead. C8's 60s epochs are calibrated for settlement throughput. You cannot simply pick one — the choice has cascading effects on:
- C5's verification windows (50 minutes of a 60-minute epoch)
- C6's consolidation schedule (every 10 epochs — 10 hours at C3 rates, 10 minutes at C8 rates)
- C7's intent deadlines and settlement lag (32 epochs = 32 hours vs 32 minutes)

INC-02 (C-class collision) could be dangerous if the resolution introduces a 9th class that C5's conservatism ordering doesn't account for.

### Arbiter Verdict

**FEASIBLE — CONDITIONAL_ADVANCE**

The reconciliation is feasible but requires careful design. The Skeptic's concern about epoch duration is valid — the reconciliation document must propose a principled resolution, not just pick a number.

---

## 2. Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Novelty | 2 | Reconciliation is engineering, not invention |
| Feasibility | 4 | All conflicts are resolvable |
| Impact | 5 | Without reconciliation, implementation is blocked |
| Risk | 4/10 (MEDIUM-LOW) | Low risk of introducing new problems |

---

## 3. Resolution Strategy per Inconsistency

### INC-01 — EPOCH DURATION [HIGH] → RESOLVABLE

**Resolution:** Adopt a **multi-rate epoch hierarchy**.

- **Base epoch (tick):** 60s (C8's value) — the settlement and EABS cycle
- **Coordination epoch (tidal cycle):** 3600s = 60 ticks — C3's EPOCH_DURATION
- **C5 verification window:** operates within tidal cycles (T+0 to T+50min remains valid)
- **C6 consolidation:** every 10 tidal cycles (10 hours) or configurable

This preserves both specs' intent. C3's "epoch" becomes the tidal cycle. C8's "epoch" becomes the settlement tick. All parameters re-derive from the hierarchy:
- C3 DIVERSITY_COOLING_EPOCHS = 50 tidal cycles = 50 hours ✓
- C8 staleness = 63 seconds (1 tick + overhead) ✓
- C5 verification window = 50 minutes of a 60-minute tidal cycle ✓

**Canonical terms:**
- `SETTLEMENT_TICK` = 60s (C8 operations)
- `TIDAL_EPOCH` = 3600s = 60 ticks (C3 coordination)
- All existing specs' "epoch" mapped to the appropriate tier

### INC-02 — C-CLASS COLLISION [HIGH] → RESOLVABLE

**Resolution:** C5's C-class (Compliance) is canonical. C6's consolidation outputs should be submitted as a **new class or sub-type**.

**Option A (Preferred):** Add K-class (Knowledge Consolidation) as a 9th claim class.
- Conservatism ordering becomes: H > N > E > S > R > P > C > K > D
- K-class sits between C (Compliance) and D (Deterministic) because consolidation outputs CAN be computationally verified (check sources, check reasoning chain)
- Admission threshold: 0.85 (between C=0.90 and P=0.80)
- Verification tier: STRUCTURED_EVIDENCE (Tier 2)
- C6 already defines the VTD submission protocol; just relabel from "C-class" to "K-class"

**Option B:** Keep 8 classes, submit consolidations as R-class (Reasoning) since consolidation IS reasoning over premises.
- Pro: No new class needed
- Con: Loses the ability to treat consolidation outputs differently from general reasoning

**Recommendation:** Option A. The consolidation process is sufficiently distinct (LLM-mediated, multi-source, dreaming-phase) to warrant its own class.

### INC-03 — C4 ISOLATION [HIGH] → RESOLVABLE

**Resolution:** Add a **C4 Integration Appendix** to the reconciliation document.

Contents:
1. **Epistemic class → Claim class mapping:**
   | C4 epistemic_class | C5 claim_class | Rationale |
   |-------------------|---------------|-----------|
   | observation | E (Empirical) | Direct observations |
   | correlation | S (Statistical) | Statistical associations |
   | causation | R (Reasoning) | Causal claims require reasoning |
   | inference | R (Reasoning) or H (Heuristic) | Depends on formality |
   | prediction | H (Heuristic) | Forward-looking, inherently uncertain |
   | prescription | N (Normative) | Normative recommendations |

2. **ASV token → PCVM intake mapping** (how CLM/EVD/PRV/VRF tokens enter the verification membrane)
3. **ASV extensions for stack integration** (INT claim type from C7, settlement claim type from C8)

C4 itself doesn't need modification — the mapping lives in the reconciliation addendum.

### INC-04 — C8 CLAIM CLASS SUBSET [HIGH] → RESOLVABLE

**Resolution:** Extend C8's difficulty weight table to all 8 (or 9 with K-class) claim classes.

| Class | Difficulty Weight | Settlement Type | Rationale |
|-------|------------------|-----------------|-----------|
| D (Deterministic) | 1.0 | B-class fast | Recomputation |
| K (Knowledge Consolidation) | 1.2 | V-class standard | Reasoning verification |
| C (Compliance) | 1.3 | B-class fast | Rule matching |
| P (Process) | 1.5 | B-class fast | Trace checking |
| E (Empirical) | 1.5 | V-class standard | Observation over time |
| S (Statistical) | 2.0 | V-class standard | Sample accumulation |
| R (Reasoning) | 2.2 | V-class standard | Logical verification |
| H (Heuristic) | 2.5 | V-class standard | Expert review |
| N (Normative) | 3.0 | G-class slow | Value judgments |

Remove the P/R/C "modifiers" — they were a misinterpretation.

### INC-05 — C3 BACKWARD ISOLATION [MEDIUM] → RESOLVED BY ADDENDUM

The reconciliation addendum serves as C3's integration spec. No C3 modification needed.

### INC-06 — NAME vs. LETTER [MEDIUM] → RESOLVED BY CANONICAL TABLE

The reconciliation addendum establishes the canonical name-letter-tier mapping table that all specs reference.

### INC-07 — SETTLEMENT WEIGHT ASYMMETRY [MEDIUM] → RESOLVABLE

**Resolution:** C8's weights (40/40/10/10) are canonical — C8 is the settlement authority. C3's rates become per-tick rates within the settlement tick, and the stream weights from C8 govern the overall allocation. The reconciliation addendum specifies:

- C3's rate parameters apply within each stream's allocation
- C8's percentage weights govern cross-stream allocation
- Combined: `agent_reward = Σ(stream_weight × stream_rate × agent_score)`

### INC-08 through INC-11 [LOW] → RESOLVED BY ADDENDUM

All resolved by the canonical reference tables in the reconciliation addendum.

---

## 4. Hard Gates

| Gate | Criterion | Status |
|------|-----------|--------|
| HG-1 | Epoch hierarchy must be derivable from both C3 and C8 parameters without contradiction | DESIGN |
| HG-2 | K-class (if adopted) must fit C5's conservatism ordering without breaking existing verification logic | DESIGN |
| HG-3 | C4 epistemic_class → C5 claim_class mapping must be bijective or explicitly many-to-one with clear rules | DESIGN |
| HG-4 | Extended C8 difficulty weights must preserve the monotonicity property (harder classes = higher weights) | DESIGN |

---

## 5. Verdict

**CONDITIONAL_ADVANCE** to DESIGN.

All 4 HIGH inconsistencies have viable resolution strategies. The reconciliation addendum approach (single document bridging all specs) is architecturally clean — it doesn't modify existing specs, instead providing the missing integration layer.

Risk: 4/10 (MEDIUM-LOW). The main risk is epoch duration cascading effects, mitigated by the multi-rate hierarchy approach.
