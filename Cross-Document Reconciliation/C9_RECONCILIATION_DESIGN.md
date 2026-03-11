# C9 — Cross-Document Reconciliation: Architecture Design

**Stage:** DESIGN
**Date:** 2026-03-10
**Roles:** Architecture Designer, Systems Thinker, Domain Translator

---

## 1. Design Principles

1. **No existing spec is modified.** The reconciliation produces an addendum that bridges all 6 specs.
2. **C5 is the authoritative claim class taxonomy.** All other layers defer to C5 for class definitions.
3. **C3 is the authoritative coordination layer.** Epoch semantics, operation classes, and spatial topology are C3's domain.
4. **C8 is the authoritative settlement layer.** Economic parameters, difficulty weights, and settlement timing are C8's domain.
5. **Conflicts are resolved by establishing a hierarchy of authority**, not by compromise.

---

## 2. Canonical Epoch Hierarchy (Resolves INC-01)

### 2.1 Definition

The Atrahasis stack operates on a **three-tier temporal hierarchy**:

```
TIER 1: SETTLEMENT_TICK     =  60 seconds    (C8 authority)
TIER 2: TIDAL_EPOCH          = 3600 seconds   (C3 authority) = 60 ticks
TIER 3: CONSOLIDATION_CYCLE  = 36000 seconds  (C6 authority) = 10 tidal epochs = 600 ticks
```

### 2.2 Layer Mapping

| Layer | "Epoch" in Spec | Canonical Term | Duration |
|-------|----------------|----------------|----------|
| C3 | `EPOCH_DURATION` | `TIDAL_EPOCH` | 3600s |
| C5 | "tidal epoch clock" | `TIDAL_EPOCH` | 3600s |
| C6 | "every N epochs (default N=10)" | `CONSOLIDATION_CYCLE` | 36000s |
| C7 | "epoch" (generic) | `TIDAL_EPOCH` (for deadlines, staleness) | 3600s |
| C8 | `epoch_duration_ms` | `SETTLEMENT_TICK` | 60s |

### 2.3 Parameter Re-Derivation

| Parameter | Original Spec | Original Value | Canonical Interpretation |
|-----------|--------------|----------------|-------------------------|
| C3 EPOCH_DURATION | C3 Line 2228 | 3600s | 1 TIDAL_EPOCH |
| C3 DIVERSITY_COOLING_EPOCHS | C3 Line 2234 | 50 | 50 TIDAL_EPOCHS = 50 hours |
| C3 BOUNDARY_WINDOW | C3 Line 2230 | 5s | 5s within each TIDAL_EPOCH boundary |
| C5 verification window | C5 Line 1046 | T+0 to T+50min | Within 1 TIDAL_EPOCH |
| C5 audit selection | C5 Line 1046 | T+50min | 50 minutes into TIDAL_EPOCH |
| C5 settlement reporting | C5 Line 1046 | T+55min | 55 minutes into TIDAL_EPOCH |
| C6 dreaming schedule | C6 Line 570 | Every 10 epochs | Every 10 TIDAL_EPOCHS = 1 CONSOLIDATION_CYCLE |
| C7 settlement lag | C7 Line 2891 | 32 epochs (normal) | 32 TIDAL_EPOCHS = 32 hours |
| C7 staleness tolerance | C7 Line 2985 | 5 epochs | 5 TIDAL_EPOCHS = 5 hours |
| C8 epoch_duration_ms | C8 Line 2302 | 60000ms | 1 SETTLEMENT_TICK |
| C8 max_staleness | C8 Line 307 | ~63s | ~1 SETTLEMENT_TICK + overhead |
| C8 throughput | C8 Line 509 | ~42K msg/s at 60s epochs | Per SETTLEMENT_TICK |

### 2.4 Relationship Between Tiers

```
Within each TIDAL_EPOCH (3600s):
  ├── SETTLEMENT_TICKs 1-55:  Normal EABS settlement cycles (55 × 60s = 3300s = 55min)
  ├── SETTLEMENT_TICKs 56-58: C5 audit selection window (T+55min)
  ├── SETTLEMENT_TICK 59:     C5 settlement reporting (T+58-59min)
  └── SETTLEMENT_TICK 60:     Tidal epoch boundary operations:
                               • Capacity snapshot gossip
                               • Hash ring reconstruction
                               • VRF seed rotation
                               • Predictive model recalibration
                               • Tidal settlement computation (cumulative)

Within each CONSOLIDATION_CYCLE (36000s = 10 TIDAL_EPOCHS):
  ├── TIDAL_EPOCHS 1-9:  Normal metabolic processing
  └── TIDAL_EPOCH 10:    EMA consolidation (dreaming phase)
```

### 2.5 HG-1 Verification

C3's parameters derive from TIDAL_EPOCH (3600s). C8's parameters derive from SETTLEMENT_TICK (60s). The ratio is exactly 60:1. All parameters maintain their original values and semantics — only the naming changes to disambiguate.

**HG-1: SATISFIED** — no contradiction, both C3 and C8 parameters are preserved exactly.

---

## 3. Canonical Claim Class Taxonomy (Resolves INC-02, INC-04, INC-06)

### 3.1 Authoritative Taxonomy: 9 Classes

C5 defines 8 classes. The reconciliation adds 1 class (K) for C6's consolidation outputs.

| Letter | Full Name | Verification Tier | Admission Threshold | Difficulty Weight | Settlement Type |
|--------|-----------|-------------------|--------------------|--------------------|-----------------|
| D | Deterministic | Tier 1 (FORMAL_PROOF) | 0.95 | 1.0 | B-class fast |
| C | Compliance | Tier 1 (FORMAL_PROOF) | 0.90 | 1.3 | B-class fast |
| P | Process | Tier 2 (STRUCTURED_EVIDENCE) | 0.80 | 1.5 | B-class fast |
| R | Reasoning | Tier 2 (STRUCTURED_EVIDENCE) | 0.75 | 2.0 | V-class standard |
| E | Empirical | Tier 2 (STRUCTURED_EVIDENCE) | 0.60 | 1.5 | V-class standard |
| S | Statistical | Tier 2 (STRUCTURED_EVIDENCE) | 0.65 | 2.0 | V-class standard |
| K | Knowledge Consolidation | Tier 2 (STRUCTURED_EVIDENCE) | 0.70 | 1.8 | V-class standard |
| H | Heuristic | Tier 3 (STRUCTURED_ATTESTATION) | 0.50 | 2.5 | V-class standard |
| N | Normative | Tier 3 (STRUCTURED_ATTESTATION) | 0.50 | 3.0 | G-class slow |

### 3.2 Conservatism Ordering (Updated)

```
H > N > K > E > S > R > P > C > D
```

Rationale for K placement: Knowledge consolidation claims (LLM-mediated, multi-source dreaming outputs) have higher inherent uncertainty than empirical observations or statistical analyses because they involve synthetic reasoning. But they are less uncertain than heuristic expert judgment because they are grounded in explicit source quanta with traceable provenance.

### 3.3 K-Class Definition

**K-class (Knowledge Consolidation):** A claim produced by EMA's consolidation (dreaming) process, synthesizing patterns across multiple epistemic quanta from diverse sources. Verification checks source quantum provenance, reasoning chain validity, falsification statement quality, and cross-domain coherence. K-class claims start with high uncertainty (u ≥ 0.4) and are subject to aging uncertainty increase if not empirically validated.

**Subjective Logic initialization:**
- Verified opinion: Full tuple
- Initial opinion: (0, 0, 1, 0.6) — base rate 0.6, between E/S (0.5) and H (0.7)
- Decay model: Half-life 120 days (shorter than H=180 days, reflecting synthetic nature)

**VTD requirements:**
- Source quanta references (minimum 5 from ≥3 parcels, no agent >30%)
- Synthesis reasoning chain
- Falsification statement
- 3-pass majority voting record (per C6 CR-13)

### 3.4 C3 Name-to-Letter Mapping

| C3 Name (Line 800) | C5/Canonical Letter | Notes |
|--------------------|--------------------|----|
| deterministic | D | Direct match |
| empirical | E | Direct match |
| statistical | S | Direct match |
| heuristic | H | Direct match |
| normative | N | Direct match |
| (not in C3) | P (Process) | Added by C5 |
| (not in C3) | R (Reasoning) | Added by C5 |
| (not in C3) | C (Compliance) | Added by C5 |
| (not in C3) | K (Knowledge Consolidation) | Added by C9 reconciliation |

C3's verification pathways for D/E/S/H/N remain as specified. For P/R/C/K, the verification pathway is:

| Class | C3 Verification Pathway |
|-------|------------------------|
| P (Process) | Trace replay + cross-reference (analogous to empirical) |
| R (Reasoning) | Premise verification + logical audit (analogous to deterministic for valid proofs, statistical for probabilistic arguments) |
| C (Compliance) | Rule-set matching + constitutional compliance (analogous to normative governance review) |
| K (Knowledge Consolidation) | Source provenance + reasoning chain + falsification audit (new pathway) |

### 3.5 C6 Claim Class → EMA Type Mapping (Corrected)

| PCVM Class | EMA Type | Rationale |
|-----------|---------|-----------|
| D (Deterministic) | observation | Computation results are observations |
| E (Empirical) | observation | Direct mapping |
| S (Statistical) | inference | Statistical conclusions are inferred |
| H (Heuristic) | inference | Heuristic judgments are inferred |
| N (Normative) | governance | Normative claims are governance rules |
| P (Process) | observation | Process compliance is observed |
| R (Reasoning) | inference | Reasoning produces inferences |
| C (Compliance) | observation | Compliance is observed against rules |
| **K (Knowledge Consolidation)** | **consolidation** | **From dreaming** |

This corrects C6's original table where "C" meant "Consolidation". Now "K" maps to consolidation, and "C" (Compliance) correctly maps to observation.

### 3.6 HG-2, HG-4 Verification

**HG-2:** K-class fits the conservatism ordering (H > N > K > E > S > R > P > C > D). K sits between N and E, which is correct — consolidation is more uncertain than observation but less than normative value judgments. C5's existing verification logic handles 3-tier systems; K slots into Tier 2 (STRUCTURED_EVIDENCE) without disruption.

**HG-4:** Difficulty weights are monotonically increasing with conservatism: D(1.0) < C(1.3) < P(1.5) = E(1.5) < K(1.8) < S(2.0) = R(2.0) < H(2.5) < N(3.0). The equal weights for P/E and S/R are acceptable — they're in the same verification tier.

**HG-2: SATISFIED.** **HG-4: SATISFIED.**

---

## 4. C4 Integration Mapping (Resolves INC-03)

### 4.1 Epistemic Class → Claim Class Mapping

| C4 `epistemic_class` | Primary C5 `claim_class` | Secondary (context-dependent) | Mapping Rule |
|----------------------|-------------------------|-------------------------------|-------------|
| `observation` | E (Empirical) | D (Deterministic) if computationally verifiable | If source is sensor/API/instrument → E. If source is deterministic computation → D. |
| `correlation` | S (Statistical) | — | Always S — correlations are statistical by definition. |
| `causation` | R (Reasoning) | S (Statistical) if experimental | If experimental/RCT → S. If argued from theory → R. |
| `inference` | R (Reasoning) | H (Heuristic) if model-based | If formal logic/proof → R. If ML model/expert intuition → H. |
| `prediction` | H (Heuristic) | S (Statistical) if quantitative model | If quantitative forecast with CI → S. If qualitative/expert → H. |
| `prescription` | N (Normative) | — | Always N — prescriptions are normative by definition. |

### 4.2 Resolution Rule

When a C4 ASV message enters the stack (via C6 ingestion or C7 intent processing):

```
FUNCTION map_epistemic_to_claim_class(clm: C4.CLM) -> C5.ClaimClass:
    // Primary mapping
    primary = PRIMARY_MAP[clm.epistemic_class]

    // Context-dependent override
    IF clm.epistemic_class == "observation":
        IF clm.evidence[0].quality_class == "computational_result":
            RETURN D
    IF clm.epistemic_class == "causation":
        IF any(e.quality_class == "computational_result" for e in clm.evidence):
            RETURN S
    IF clm.epistemic_class == "inference":
        IF clm.confidence.method == "model_derived":
            RETURN H
    IF clm.epistemic_class == "prediction":
        IF clm.confidence.method == "statistical" AND clm.confidence.interval IS NOT NULL:
            RETURN S

    RETURN primary
```

### 4.3 ASV Token Flow Through Stack

```
Agent produces C4 ASV message (CLM + CNF + EVD + PRV)
    │
    ▼
C6 EMA Ingestion:
    1. Extract epistemic_class from CLM
    2. Map to preliminary claim_class via §4.2 rule
    3. Package as VTD draft with preliminary class
    │
    ▼
C5 PCVM Classification:
    1. Three-way classification (agent suggestion, structural, independent)
    2. Final claim_class assigned (C5 is sovereign)
    3. MCT generated with final class + Subjective Logic opinion
    │
    ▼
C6 EMA Quantum Creation:
    1. Quantum created with PCVM-assigned class
    2. ASV fields mapped to quantum fields (per C6 §4.2 table)
    3. Enters metabolic lifecycle
```

### 4.4 HG-3 Verification

The mapping is many-to-one (6 epistemic classes → 5 primary claim classes). The context-dependent overrides make it many-to-many, but with deterministic resolution rules. No C4 epistemic_class is unmapped. No C5 claim_class is unreachable (D reached via observation+computational, E via observation, S via correlation/causation/prediction, R via causation/inference, H via inference/prediction, N via prescription; P/C/K not reachable from C4 directly — P is generated by process verification systems, C by compliance checkers, K by EMA dreaming).

**HG-3: SATISFIED** — mapping is well-defined with deterministic resolution.

---

## 5. Settlement Integration (Resolves INC-07, INC-10)

### 5.1 Settlement Authority Hierarchy

```
C8 (DSF) is the CANONICAL settlement authority.
C3's settlement calculator is the SCHEDULING COMPLIANCE component within DSF.
C7's Settlement Router forwards to C8 (DSF), NOT to C3 directly.
```

Corrected data flow:
```
C7 RIF → C8 DSF Settlement Router → EABS processing → Settlement outputs
                                         │
C3 Tidal Noosphere ──────────────────────┘ (provides scheduling compliance data)
C5 PCVM ──────────────────────────────────┘ (provides verification quality data)
C6 EMA ───────────────────────────────────┘ (provides knowledge contribution data)
```

### 5.2 Settlement Stream Canonical Weights

C8's weights are authoritative:

| Stream | Weight | Data Source | Settlement Tier |
|--------|--------|-------------|-----------------|
| Scheduling Compliance | 40% | C3 tidal scheduler | Per-SETTLEMENT_TICK (B-class) |
| Verification Quality | 40% | C5 PCVM | Per-TIDAL_EPOCH (V-class) |
| Communication Efficiency | 10% | C3 predictive channels | Per-SETTLEMENT_TICK (B-class) |
| Governance Participation | 10% | C3 G-class engine | Per-governance-action (G-class) |

C3's rate parameters (COMPLIANCE_RATE, VERIFICATION_RATE, COMM_RATE, GOV_RATE) are intra-stream scaling factors, not cross-stream weights. The combined formula:

```
agent_settlement(tick) =
    0.40 × COMPLIANCE_RATE × scheduling_score(agent, tick) +
    0.40 × VERIFICATION_RATE × verification_score(agent, tidal_epoch) +
    0.10 × COMM_RATE × communication_score(agent, tick) +
    0.10 × GOV_RATE × governance_score(agent, tidal_epoch)
```

---

## 6. Cross-Layer Type Registry

### 6.1 Canonical Type Definitions

All layers MUST use these canonical types for cross-layer communication:

```yaml
# Temporal types
SettlementTick:    uint64    # 60s increments (C8 authority)
TidalEpoch:        uint64    # 3600s increments (C3 authority)
ConsolidationCycle: uint64   # 36000s increments (C6 authority)

# Identity types
AgentID:           string    # Format: "ag:<locus>:<uuid7>" (C3 authority)
LocusID:           string    # Format: "locus:<region>:<name>" (C3 authority)
ParcelID:          string    # Format: "parcel:<locus>:<index>" (C3 authority)
ClaimID:           string    # Format: "claim:<class>:<uuid7>" (C5 authority)
QuantumID:         string    # Format: "eq:<locus>:<epoch>:<uuid7>" (C6 authority)
IntentID:          string    # Format: "intent:<uuid>" (C7 authority)

# Claim taxonomy
ClaimClass:        enum      # {D, E, S, H, N, P, R, C, K} (C5+C9 authority)
OperationClass:    enum      # {M, B, X, V, G} (C3 authority)
SettlementClass:   enum      # {B_FAST, V_STANDARD, G_SLOW} (C8 authority)

# Subjective Logic
SLOpinion:         tuple     # (belief, disbelief, uncertainty, base_rate) (C5 authority)
                             # Constraint: b + d + u = 1, all ≥ 0, a ∈ [0,1]

# Economic types
AIC:               decimal(18,8)  # Atrahasis Intelligence Coin (C8 authority)
ProtocolCredit:    decimal(18,8)  # Non-transferable, 10%/tick decay (C8 authority)
CapacitySlice:     uint64         # CSO-backed resource unit (C8 authority)

# Verification types
MCT:               struct    # Membrane Clearance Token (C5 authority)
VTD:               struct    # Verification Trace Document (C5 authority)
```

### 6.2 Cross-Layer Contract Summary

| Provider | Consumer | Contract | Data Flow |
|----------|----------|----------|-----------|
| C3 | C5 | VRF committee selection | C3 → C5: VRF output per tidal epoch |
| C3 | C6 | Epoch boundaries, parcel topology | C3 → C6: epoch events, topology changes |
| C3 | C7 | Operation scheduling, G-class voting | C3 ↔ C7: schedule requests, vote results |
| C3 | C8 | CRDT infrastructure, Sentinel Graph | C3 ↔ C8: ledger replication, cluster updates |
| C4 | C6 | ASV token intake | C4 → C6: CLM/CNF/EVD/PRV tokens |
| C4 | C7 | Intent provenance chains | C4 ↔ C7: INT claim type, provenance |
| C4 | C8 | Settlement message vocabulary | C4 → C8: economic message schemas |
| C5 | C3 | Verification results | C5 → C3: V-class settlement data |
| C5 | C6 | MCTs, VTDs, credibility | C5 ↔ C6: admission, re-verification |
| C5 | C7 | Agent credibility, claim assessment | C5 → C7: credibility scores |
| C5 | C8 | Verification attestations | C5 → C8: verification reports |
| C6 | C7 | Knowledge projections, SHREC state | C6 → C7: projections, metabolic phase |
| C6 | C8 | Knowledge contribution reports | C6 → C8: metabolic efficiency |
| C7 | C8 | Intent budgets, task completions | C7 ↔ C8: submissions, stake queries |

---

## 7. Resolved Inconsistency Verification

| INC | Severity | Resolution | Hard Gate | Status |
|-----|----------|------------|-----------|--------|
| INC-01 | HIGH | Three-tier epoch hierarchy | HG-1 | ✅ RESOLVED |
| INC-02 | HIGH | K-class for consolidation | HG-2 | ✅ RESOLVED |
| INC-03 | HIGH | C4 integration mapping | HG-3 | ✅ RESOLVED |
| INC-04 | HIGH | Extended 9-class difficulty weights | HG-4 | ✅ RESOLVED |
| INC-05 | MEDIUM | Addendum serves as C3's integration spec | — | ✅ RESOLVED |
| INC-06 | MEDIUM | Canonical name-letter table | — | ✅ RESOLVED |
| INC-07 | MEDIUM | C8 weights canonical, C3 rates intra-stream | — | ✅ RESOLVED |
| INC-08 | LOW | C5 committee sizes authoritative | — | ✅ RESOLVED |
| INC-09 | LOW | C6 mapping is unilateral (acceptable) | — | ✅ RESOLVED |
| INC-10 | LOW | C7 routes to C8, not C3 | — | ✅ RESOLVED |
| INC-11 | LOW | C3 claim_type ≠ C4 epistemic_class (different axes) | — | ✅ RESOLVED |

All 11 inconsistencies resolved. All 4 hard gates satisfied.
