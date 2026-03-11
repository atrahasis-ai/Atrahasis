# EMA Master Tech Spec -- Patch Addendum v1.1

**Applies to:** C6 MASTER_TECH_SPEC.md v1.0.0 (2026-03-10)
**Patch version:** 1.1.0
**Date:** 2026-03-10
**Status:** ADDENDUM (normative corrections and missing definitions)

This addendum provides corrections and missing definitions identified during cross-system reconciliation (C9). All pseudocode in this document is normative and supersedes the corresponding sections in v1.0.0 where conflicts exist.

---

## Table of Contents

- [PA-1: F34 -- LV Signal Multiplication Ordering Fix](#pa-1-f34----lv-signal-multiplication-ordering-fix)
- [PA-2: F35 -- execute_recycling Definition](#pa-2-f35----execute_recycling-definition)
- [PA-3: F36 -- Reconstruction Functions](#pa-3-f36----reconstruction-functions)
- [PA-4: F39 -- cross_shard_bonus Definition](#pa-4-f39----cross_shard_bonus-definition)
- [PA-5: F40 -- Compound Claim Decomposition](#pa-5-f40----compound-claim-decomposition)
- [PA-6: F41 -- Parameter Deployment Profiles](#pa-6-f41----parameter-deployment-profiles)
- [PA-7: F42 -- Vitality Multiplicative Composition Rationale and Floor](#pa-7-f42----vitality-multiplicative-composition-rationale-and-floor)
- [PA-8: F43 -- TV-6 Rejection Behavior Correction](#pa-8-f43----tv-6-rejection-behavior-correction)
- [PA-9: F44 -- PCVM Outage Degraded Mode](#pa-9-f44----pcvm-outage-degraded-mode)
- [PA-10: F45 -- Dreaming Temperature Rationale](#pa-10-f45----dreaming-temperature-rationale)
- [PA-11: F46 -- Immune Self-Audit Lookback Window](#pa-11-f46----immune-self-audit-lookback-window)
- [PA-12: Claim Class Mapping Correction (C9 Reconciliation)](#pa-12-claim-class-mapping-correction-c9-reconciliation)

---

## PA-1: F34 -- LV Signal Multiplication Ordering Fix

**Severity:** HIGH
**Affects:** Appendix C, Section C.2 (Discrete-Time Implementation)

### Problem

In the v1.0.0 Lotka-Volterra discrete-time step (Appendix C.2), the signal intensity multiplier `dS *= signals[name]` is applied AFTER the floor correction term. When `signals[name]` is zero (signal has no intensity), the entire delta including the floor correction is multiplied to zero. This prevents floor recovery for any signal with zero intensity, violating INV-E7 (SHREC Floor Guarantee).

### Corrected Pseudocode

**Replaces:** Appendix C.2 `lotka_volterra_step` in its entirety.

```python
def lotka_volterra_step(current_shares, signals, params):
    """
    Discrete-time Lotka-Volterra competitive step with correct ordering.

    Critical fix: signal intensity modulates ONLY the competitive dynamics term.
    Floor correction is applied AFTER signal multiplication so that floor
    recovery is never suppressed by zero-intensity signals.
    """
    new_shares = {}
    for i, name in enumerate(SIGNAL_NAMES):
        S_i = current_shares[name]
        r_i = params.growth_rates[name]
        K_i = params.carrying_capacities[name]  # default: 0.4

        # Step 1: Compute competitive dynamics
        competition = sum(
            params.alpha[name][other] * current_shares[other] / K_i
            for other in SIGNAL_NAMES
        )
        dS_competitive = r_i * S_i * (1.0 - competition)

        # Step 2: Apply signal intensity ONLY to the competitive term.
        # Zero-intensity signal zeroes competitive growth but does NOT
        # suppress floor correction.
        dS_competitive *= signals[name]

        # Step 3: Floor correction applied AFTER signal multiplication.
        # This guarantees floor recovery regardless of signal intensity.
        floor = FLOOR_ALLOCATIONS[name]
        floor_correction = 0.0
        if (S_i + dS_competitive * DT) < floor:
            floor_correction = (floor - S_i) * FLOOR_RESTORATION_RATE

        # Step 4: Combine
        dS = dS_competitive + floor_correction
        new_shares[name] = max(0.0, S_i + dS * DT)

    # Normalize to sum to 1.0
    total = sum(new_shares.values())
    if total > 0:
        return {s: v / total for s, v in new_shares.items()}
    else:
        # Fallback: equal shares (should never occur with floor corrections)
        equal = 1.0 / len(SIGNAL_NAMES)
        return {s: equal for s in SIGNAL_NAMES}
```

### Verification

With this fix, TV-3 (SHREC Floor Enforcement) holds even when four signals have intensity zero: the floor correction drives each zero-intensity signal back toward its floor allocation independently of the competitive dynamics term.

---

## PA-2: F35 -- execute_recycling Definition

**Severity:** HIGH (blocks implementation)
**Affects:** Section 5.4.3 (Two-Phase Dissolution)

### Problem

`execute_recycling(q)` is called in `execute_dissolution` (Section 5.4.3) but is never defined anywhere in the specification.

### Definition

```python
@dataclass
class RecyclingTransfer:
    """Record of a single evidence transfer during dissolution."""
    evidence_item: Evidence           # The evidence being transferred
    source_quantum_id: str            # The dissolving quantum
    recipient_quantum_id: str         # The receiving quantum
    new_edge_type: str                # "DERIVATION" or "CONTRADICTION"
    new_edge_weight: float            # original_weight * dissolution_confidence
    provenance_chain: List[str]       # Full chain: original source -> ... -> dissolving -> recipient

@dataclass
class RecyclingResult:
    """Output of the recycling process."""
    transfers: List[RecyclingTransfer]    # Evidence successfully transferred
    archived: List[ArchivedEvidence]      # Evidence archived (no suitable recipient)
    recycled_to: List[str]                # Recipient quantum IDs (for dissolution record)
    eliminated: List[dict]                # Evidence items that were eliminated


def execute_recycling(q: EpistemicQuantum) -> RecyclingResult:
    """
    Recycle evidence and edge connections from a dissolving quantum to
    surviving quanta. Called during dissolution (Section 5.4.3).

    Input:
        q: The dissolving quantum (state = QUARANTINED, about to become DISSOLVED).
           Must have: q.content.evidence, q.edges, q.opinion

    Algorithm:
        1. For each evidence item, find the best surviving recipient.
        2. Transfer evidence via new DERIVATION edges (or CONTRADICTION if contradictory).
        3. Archive orphaned evidence with full provenance chain.

    Output:
        RecyclingResult with transfers performed and archived items.
    """
    transfers = []
    archived = []
    eliminated = []

    # Dissolution confidence: how much trust we place in the dissolving
    # quantum's evidence connections. Derived from the quantum's final
    # credibility, discounted because it is being dissolved.
    dissolution_confidence = max(
        0.1,
        (q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty) * 0.5
    )

    shard = get_shard(q.shard_id)

    for evidence_item in (q.content.evidence or []):
        # Step 1: Find candidate recipients.
        # Candidates are ACTIVE quanta that share domain overlap with
        # the dissolving quantum and have existing edges to it.
        candidates = []
        for edge in q.edges:
            neighbor = get_quantum(edge.target_id)
            if neighbor is None:
                continue
            if neighbor.metabolic_state.phase not in ("ACTIVE", "CONSOLIDATING"):
                continue
            if neighbor.id == q.id:
                continue

            # Score by: edge weight to dissolving quantum * domain overlap
            domain_overlap = len(
                set(neighbor.content.domain_tags) & set(q.content.domain_tags)
            ) / max(1, len(q.content.domain_tags))

            score = edge.weight * (0.6 + 0.4 * domain_overlap)
            candidates.append((neighbor, edge, score))

        # Sort by score descending; take top MAX_RECYCLING_RECIPIENTS (5)
        candidates.sort(key=lambda c: c[2], reverse=True)
        candidates = candidates[:MAX_RECYCLING_RECIPIENTS]

        if not candidates:
            # Step 3: No suitable recipient -- archive with provenance chain.
            archived.append(ArchivedEvidence(
                evidence_item=evidence_item,
                source_quantum_id=q.id,
                source_quantum_hash=sha256(serialize(q.content)) if q.content else "dissolved",
                provenance_chain=build_provenance_chain(q, evidence_item),
                archived_at_epoch=current_epoch(),
                dissolution_confidence=dissolution_confidence
            ))
            continue

        # Step 2: Transfer to the best recipient.
        best_recipient, best_edge, best_score = candidates[0]
        transfer_weight = best_edge.weight * dissolution_confidence

        # Step 2a: Check for contradiction.
        # If the evidence contradicts the recipient quantum (detected by
        # existing CONTRADICTION edge or semantic opposition), create a
        # CONTRADICTION edge instead of DERIVATION.
        is_contradictory = _check_contradiction(evidence_item, best_recipient, q)

        if is_contradictory:
            edge_type = "CONTRADICTION"
            # Contradiction edges are lower weight to avoid weaponizing
            # dissolution as an attack vector.
            transfer_weight *= 0.5
        else:
            edge_type = "DERIVATION"

        # Create the transfer edge from dissolving quantum to recipient.
        # DERIVATION edges record that the recipient now inherits this
        # evidence lineage. The edge points from q -> recipient
        # (recipient is derived-from the evidence that q carried).
        create_edge(
            source=q,
            target=best_recipient,
            edge_type=edge_type,
            weight=clamp(transfer_weight, MIN_EDGE_WEIGHT, 1.0),
            metadata={
                "recycled_from": q.id,
                "evidence_type": evidence_item.evidence_type,
                "original_edge_weight": best_edge.weight,
                "dissolution_confidence": dissolution_confidence
            }
        )

        # Update recipient citation count if DERIVATION
        if edge_type == "DERIVATION":
            best_recipient.citation_count += 1

        transfers.append(RecyclingTransfer(
            evidence_item=evidence_item,
            source_quantum_id=q.id,
            recipient_quantum_id=best_recipient.id,
            new_edge_type=edge_type,
            new_edge_weight=transfer_weight,
            provenance_chain=build_provenance_chain(q, evidence_item)
                           + [best_recipient.id]
        ))

    return RecyclingResult(
        transfers=transfers,
        archived=archived,
        recycled_to=list(set(t.recipient_quantum_id for t in transfers)),
        eliminated=[
            {"evidence_hash": sha256(serialize(a.evidence_item)), "reason": "no_recipient"}
            for a in archived
        ]
    )


def _check_contradiction(
    evidence_item: Evidence,
    recipient: EpistemicQuantum,
    dissolving: EpistemicQuantum
) -> bool:
    """
    Determine whether transferring evidence_item to recipient would
    introduce a contradiction.

    Returns True if:
      1. There is an existing CONTRADICTION edge between dissolving and
         recipient with weight >= 0.5, OR
      2. The evidence directly opposes the recipient's claim (detected
         by negative cosine similarity below -CONTRADICTION_SIMILARITY_THRESHOLD).
    """
    # Check 1: Existing contradiction edge
    for edge in dissolving.edges:
        if (edge.target_id == recipient.id
                and edge.edge_type == "CONTRADICTION"
                and edge.weight >= 0.5):
            return True

    # Check 2: Semantic opposition between evidence and recipient
    if evidence_item.source_quantum_id:
        source_q = get_quantum(evidence_item.source_quantum_id)
        if source_q and source_q.content:
            sim = cosine_similarity(
                compute_embedding(source_q.content.claim_text),
                compute_embedding(recipient.content.claim_text)
            )
            if sim < -CONTRADICTION_SIMILARITY_THRESHOLD:  # -0.6
                return True

    return False


def build_provenance_chain(
    q: EpistemicQuantum,
    evidence_item: Evidence
) -> List[str]:
    """
    Build the full provenance chain for an evidence item being recycled.
    Traces back through DERIVATION edges to find the original sources.
    """
    chain = []

    # Start with the evidence's own source
    if evidence_item.source_quantum_id:
        chain.append(evidence_item.source_quantum_id)

    # Add the dissolving quantum's own derivation chain
    chain.extend(q.provenance.derived_from or [])

    # Add the dissolving quantum itself
    chain.append(q.id)

    return chain
```

### Integration

The call site in `execute_dissolution` (Section 5.4.3, line `recycling_result = execute_recycling(q)`) requires no change. The returned `RecyclingResult` is compatible with the existing `DissolutionRecord` fields `recycled_to` and `eliminated_evidence`.

---

## PA-3: F36 -- Reconstruction Functions

**Severity:** HIGH (blocks implementation)
**Affects:** Section 8 (Projection Engine), INV-E8 (Projection Fidelity)

### Problem

Round-trip fidelity (INV-E8) requires reconstruction from each projection back to the canonical form. Forward projection functions are defined (Sections 8.2-8.4) but no reconstruction (inverse) functions exist. Without reconstruction, fidelity cannot be measured.

### Definitions

```python
@dataclass
class ReconstructionResult:
    """Result of reconstructing a canonical quantum from a projection."""
    quantum: EpistemicQuantum    # Best-effort canonical form
    fidelity_score: float        # [0, 1] measuring information preserved
    loss_report: List[str]       # Human-readable list of information that could not be recovered
    reconstruction_source: str   # "c3", "c4", or "c5"


def reconstruct_from_c3(c3_proj: C3Projection) -> ReconstructionResult:
    """
    Reconstruct a canonical EpistemicQuantum from a Tidal Noosphere
    parcel view (C3 projection).

    C3 projections lose:
      - Full SL opinion (collapsed to scalar relevance_score)
      - Uncertainty quantification
      - Evidence array details
      - Metabolic state
      - Analogy and derivation edges outside parcel scope
      - SHREC signal associations

    Reconstruction strategy:
      - Claim text: recover from claim_summary (may be truncated at 200 chars)
      - Opinion: reverse-engineer from scalar relevance_score using default base_rate
      - Edges: recover SUPPORT/CONTRADICTION counts but not targets or weights
      - Provenance: not recoverable (set to reconstruction stub)
      - Metabolic state: default to ACTIVE (actual state was lost)
    """
    losses = []
    q = EpistemicQuantum()

    # ID: preserved
    q.id = c3_proj.quantum_id

    # Content: claim_summary may be truncated
    q.content = TypedContent(
        claim_text=c3_proj.claim_summary,  # may be truncated to 200 chars
        claim_type="observation",          # cannot recover original type from C3
        domain_tags=c3_proj.domain_tags,
        evidence=[]                        # evidence array lost in C3 projection
    )
    if len(c3_proj.claim_summary) >= 200:
        losses.append("claim_text likely truncated at 200 characters")
    losses.append("claim_type defaulted to 'observation' (original type lost)")
    losses.append("evidence array not recoverable from C3 projection")

    # Opinion: reverse from scalar relevance_score = b + a * u
    # With only one equation and three unknowns (b, d, u) plus a,
    # we assume default base_rate a=0.5 and maximum uncertainty consistent
    # with the observed relevance_score.
    relevance = c3_proj.relevance_score
    a = 0.5  # default base_rate assumption
    # relevance = b + 0.5 * u, and b + d + u = 1
    # Maximize u (most honest about reconstruction uncertainty):
    # b = relevance - 0.5 * u => substitute into b + d + u = 1
    # (relevance - 0.5u) + d + u = 1 => d = 1 - relevance - 0.5u
    # d >= 0 => u <= 2 * (1 - relevance)
    # b >= 0 => u <= 2 * relevance
    u_max = min(2.0 * (1.0 - relevance), 2.0 * relevance, 1.0)
    # Use 80% of max uncertainty to reflect reconstruction loss
    u = u_max * 0.8
    b = max(0.0, relevance - a * u)
    d = max(0.0, 1.0 - b - u)
    # Renormalize
    total = b + d + u
    if total > 0:
        b, d, u = b / total, d / total, u / total

    q.opinion = SubjectiveLogicOpinion(belief=b, disbelief=d, uncertainty=u, base_rate=a)
    losses.append("SL opinion reconstructed from scalar; uncertainty is estimated")

    # Edges: we know counts but not targets or weights
    q.edges = []
    # Create placeholder edges (no target IDs available)
    losses.append(
        f"edge structure lost: only counts recovered "
        f"(support={c3_proj.edge_summary.support_count}, "
        f"contradiction={c3_proj.edge_summary.contradiction_count})"
    )

    # Provenance: not recoverable
    q.provenance = W3C_PROV_Record(
        generating_agent="reconstruction:c3",
        generating_activity="external_import",
        generation_time=current_timestamp(),
        generation_epoch=0,  # unknown
        derived_from=[c3_proj.quantum_id],
        method="c3_reconstruction"
    )
    losses.append("provenance not recoverable from C3 projection")

    # Metabolic state: not recoverable, default to ACTIVE
    q.metabolic_state = MetabolicState(phase="ACTIVE", vitality=0.5)
    losses.append("metabolic state defaulted to ACTIVE with vitality=0.5")

    # Shard: recoverable from parcel
    q.shard_id = c3_proj.parcel

    # Fidelity score computation
    # text: 1.0 if not truncated, 0.7 if truncated
    text_fidelity = 0.7 if len(c3_proj.claim_summary) >= 200 else 1.0
    # opinion: ~0.5 (scalar to tuple reconstruction is lossy)
    opinion_fidelity = 0.5
    # edges: 0.2 (counts only, no structure)
    edge_fidelity = 0.2

    fidelity = 0.5 * text_fidelity + 0.3 * opinion_fidelity + 0.2 * edge_fidelity

    return ReconstructionResult(
        quantum=q,
        fidelity_score=round(fidelity, 4),
        loss_report=losses,
        reconstruction_source="c3"
    )


def reconstruct_from_c4(c4_proj: C4Projection) -> ReconstructionResult:
    """
    Reconstruct a canonical EpistemicQuantum from an ASV token chain
    (C4 projection).

    C4 projections lose:
      - Coherence graph position (edge targets and weights)
      - Metabolic state (vitality, phase, circulation count)
      - SHREC signal associations

    C4 preserves:
      - Full CLM-CNF-EVD-PRV-VRF chain
      - Full SL opinion tuple
      - Epistemic class and claim type
      - Evidence references
      - Provenance agent

    Reconstruction strategy:
      - This is the second-highest fidelity reconstruction.
      - Claim text, opinion, evidence, provenance all recoverable.
      - Edges and metabolic state are not recoverable.
    """
    losses = []
    q = EpistemicQuantum()

    # ID: preserved in the token chain
    q.id = c4_proj.quantum_id

    # Content: fully recoverable from CLM token
    q.content = TypedContent(
        claim_text=c4_proj.clm.statement,
        claim_type=map_class_to_type(c4_proj.epistemic_class),
        domain_tags=c4_proj.domain_tags if hasattr(c4_proj, 'domain_tags') else [],
        evidence=[
            Evidence(
                source_quantum_id=evd.source_id,
                external_reference=evd.external_ref,
                evidence_type=evd.evidence_type,
                weight=evd.weight
            )
            for evd in c4_proj.evd_chain
        ]
    )
    if not hasattr(c4_proj, 'domain_tags') or not c4_proj.domain_tags:
        losses.append("domain_tags not present in C4 projection; defaulted to empty")

    # Opinion: fully preserved (C4/AASL natively supports SL)
    q.opinion = SubjectiveLogicOpinion(
        belief=c4_proj.cnf.belief,
        disbelief=c4_proj.cnf.disbelief,
        uncertainty=c4_proj.cnf.uncertainty,
        base_rate=c4_proj.cnf.base_rate
    )
    # No loss on opinion

    # Provenance: recoverable from PRV token
    q.provenance = W3C_PROV_Record(
        generating_agent=c4_proj.prv.agent_id,
        generating_activity=c4_proj.prv.activity or "ingestion",
        generation_time=c4_proj.prv.timestamp,
        generation_epoch=c4_proj.prv.epoch if hasattr(c4_proj.prv, 'epoch') else 0,
        derived_from=c4_proj.prv.derived_from or [],
        method=c4_proj.prv.method,
        source_vtd_id=c4_proj.vrf.vtd_id if hasattr(c4_proj, 'vrf') else None
    )

    # Edges: NOT recoverable from C4
    q.edges = []
    losses.append("coherence graph edges not recoverable from C4 projection")

    # Metabolic state: NOT recoverable
    q.metabolic_state = MetabolicState(phase="ACTIVE", vitality=0.5)
    losses.append("metabolic state not recoverable; defaulted to ACTIVE with vitality=0.5")

    # Claim class
    q.claim_class = c4_proj.epistemic_class

    # Fidelity score computation
    text_fidelity = 1.0           # full text preserved
    opinion_fidelity = 1.0        # full SL tuple preserved
    type_fidelity = 1.0           # class preserved
    edge_fidelity = 0.0           # edges completely lost
    provenance_fidelity = 0.9     # mostly preserved, epoch may be missing

    # Using C4 fidelity metric weights: 0.4 text + 0.4 opinion + 0.2 type
    # But for round-trip we also need to account for edge loss.
    # Adjusted: 0.3 text + 0.3 opinion + 0.2 type + 0.1 edges + 0.1 provenance
    fidelity = (0.3 * text_fidelity + 0.3 * opinion_fidelity
                + 0.2 * type_fidelity + 0.1 * edge_fidelity
                + 0.1 * provenance_fidelity)

    return ReconstructionResult(
        quantum=q,
        fidelity_score=round(fidelity, 4),
        loss_report=losses,
        reconstruction_source="c4"
    )


def reconstruct_from_c5(c5_proj: C5Projection) -> ReconstructionResult:
    """
    Reconstruct a canonical EpistemicQuantum from a PCVM verification
    view (C5 projection).

    C5 projections lose:
      - ANALOGY edges
      - Vitality and circulation metadata
      - Metabolic phase
      - Consolidation history

    C5 preserves:
      - Full SL opinion
      - Claim class
      - Full W3C PROV provenance
      - Evidence array
      - VTD/MCT references
      - SUPPORT, CONTRADICTION, DERIVATION edges

    Reconstruction strategy:
      - Highest fidelity reconstruction. Most fields recoverable.
      - Only analogy edges and metabolic metadata are lost.
    """
    losses = []
    q = EpistemicQuantum()

    # ID: preserved
    q.id = c5_proj.quantum_id

    # Content: fully recoverable
    q.content = TypedContent(
        claim_text=c5_proj.claim_text,
        claim_type=map_class_to_type(c5_proj.claim_class),
        domain_tags=c5_proj.domain_tags if hasattr(c5_proj, 'domain_tags') else [],
        evidence=c5_proj.evidence  # fully preserved
    )

    # Opinion: fully preserved
    q.opinion = SubjectiveLogicOpinion(
        belief=c5_proj.opinion.belief,
        disbelief=c5_proj.opinion.disbelief,
        uncertainty=c5_proj.opinion.uncertainty,
        base_rate=c5_proj.opinion.base_rate
    )

    # Provenance: fully preserved
    q.provenance = c5_proj.provenance  # W3C PROV record preserved in C5

    # Edges: SUPPORT, CONTRADICTION, DERIVATION preserved; ANALOGY and SUPERSESSION lost
    q.edges = [
        edge for edge in c5_proj.edges
        if edge.edge_type in ("SUPPORT", "CONTRADICTION", "DERIVATION")
    ]
    analogy_count = c5_proj.analogy_edge_count if hasattr(c5_proj, 'analogy_edge_count') else 0
    supersession_count = c5_proj.supersession_edge_count if hasattr(c5_proj, 'supersession_edge_count') else 0
    if analogy_count > 0 or supersession_count > 0:
        losses.append(
            f"ANALOGY edges ({analogy_count}) and SUPERSESSION edges "
            f"({supersession_count}) not recoverable from C5 projection"
        )

    # Metabolic state: NOT recoverable
    q.metabolic_state = MetabolicState(phase="ACTIVE", vitality=0.5)
    losses.append("metabolic state (phase, vitality, circulation_count) not recoverable")

    # Claim class: preserved
    q.claim_class = c5_proj.claim_class

    # Timestamps: partially recoverable
    q.timestamps = TemporalRecord(
        created_at=c5_proj.provenance.generation_time,
        last_verified=c5_proj.last_verified if hasattr(c5_proj, 'last_verified') else None
    )
    losses.append("last_circulated, last_accessed, decay_start timestamps not recoverable")

    # Fidelity score computation
    # Using C5 fidelity metric: 0.3 text + 0.3 opinion + 0.2 provenance + 0.2 evidence
    text_fidelity = 1.0
    opinion_fidelity = 1.0
    provenance_fidelity = 1.0
    evidence_fidelity = 1.0

    # Adjust for edge loss: analogy edges are a small fraction typically
    total_original_edges = len(q.edges) + analogy_count + supersession_count
    if total_original_edges > 0:
        edge_preservation = len(q.edges) / total_original_edges
    else:
        edge_preservation = 1.0

    # Composite fidelity including edge preservation penalty
    fidelity = (0.3 * text_fidelity + 0.3 * opinion_fidelity
                + 0.2 * provenance_fidelity + 0.15 * evidence_fidelity
                + 0.05 * edge_preservation)

    return ReconstructionResult(
        quantum=q,
        fidelity_score=round(fidelity, 4),
        loss_report=losses,
        reconstruction_source="c5"
    )
```

### Fidelity Measurement Protocol

Round-trip fidelity for each projection is now computed as:

```python
def measure_round_trip_fidelity(quantum: EpistemicQuantum, target: str) -> float:
    """Measure round-trip fidelity: project then reconstruct."""
    if target == "c3":
        projected = project_to_c3(quantum)
        result = reconstruct_from_c3(projected)
    elif target == "c4":
        projected = project_to_c4(quantum)
        result = reconstruct_from_c4(projected)
    elif target == "c5":
        projected = project_to_c5(quantum)
        result = reconstruct_from_c5(projected)
    else:
        raise ValueError(f"Unknown projection target: {target}")

    # Compare reconstructed quantum to original
    return compute_fidelity(quantum, result.quantum, target)
```

### Expected Fidelity Ranges

| Projection | Forward Loss | Reconstruction Fidelity | Meets Target? |
|-----------|-------------|------------------------|---------------|
| C3 | Opinion collapsed, edges lost, metabolic state lost | 0.55 - 0.75 | Below 0.85 target (expected; C3 round-trip is inherently lossy) |
| C4 | Edges lost, metabolic state lost | 0.82 - 0.90 | Near 0.88 target |
| C5 | ANALOGY/SUPERSESSION edges lost, metabolic state lost | 0.90 - 0.97 | Meets 0.92 target |

**Note on C3 round-trip:** The C3 fidelity target of 0.85 applies to the *forward projection* (how well the C3 view represents the canonical quantum for C3 consumers), not to round-trip reconstruction. C3 round-trip will always be lower because the scalar-to-opinion reversal is lossy by construction.

---

## PA-4: F39 -- cross_shard_bonus Definition

**Severity:** MEDIUM
**Affects:** Section 7.4 (Active Edge Budget)

### Problem

`edge.cross_shard_bonus` is used in edge budget ranking (Section 7.4) but never defined.

### Definition

```python
def compute_cross_shard_bonus(edge: EpistemicEdge, source_quantum: EpistemicQuantum) -> float:
    """
    Compute cross-shard bonus for edge budget ranking.

    Purpose: Cross-shard edges are more valuable for global coherence
    because they connect knowledge across different spatial partitions
    (C3 loci/parcels). Losing a cross-shard edge is more damaging than
    losing an intra-shard edge, because cross-shard edges are harder
    to re-discover (they require cross-shard similarity scanning).

    Applied in: Section 7.4 enforce_edge_budget, as the 0.1-weighted
    term in rank_score computation.

    Returns:
        0.2 if source and target are in different shards
        0.0 if source and target are in the same shard
    """
    target_quantum = get_quantum(edge.target_id)
    if target_quantum is None:
        return 0.0

    if source_quantum.shard_id != target_quantum.shard_id:
        return CROSS_SHARD_BONUS  # 0.2
    else:
        return 0.0

# New configurable parameter
CROSS_SHARD_BONUS = 0.2  # Range: [0.0, 0.5], Section 7.4
```

### Updated Edge Budget Ranking

The `enforce_edge_budget` function in Section 7.4 is clarified (no change to logic, only to `cross_shard_bonus` which was previously undefined):

```python
def enforce_edge_budget(quantum, E_max=50):
    if len(quantum.edges) <= E_max:
        return
    for edge in quantum.edges:
        edge.cross_shard_bonus = compute_cross_shard_bonus(edge, quantum)
        edge.rank_score = (
            0.4 * edge.weight
            + 0.3 * edge.recency_score
            + 0.2 * edge.type_priority
            + 0.1 * edge.cross_shard_bonus
        )
    quantum.edges.sort(by=rank_score, descending=True)
    quantum.active_edges = quantum.edges[:E_max]
    quantum.archived_edges = quantum.edges[E_max:]
```

### Parameter Addition

Add to Appendix D.2 (Edge Parameters):

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| CROSS_SHARD_BONUS | 0.2 | [0.0, 0.5] | 7.4 |

---

## PA-5: F40 -- Compound Claim Decomposition

**Severity:** MEDIUM
**Affects:** Section 5.1 (Phase 1: Ingestion)

### Problem

`decompose_claim` is called in the ingestion protocol (Section 5.1) with the comment "Most claims map 1:1. Compound claims decompose into atomic sub-claims." The decomposition algorithm is not defined.

### Definition

```python
def decompose_claim(
    claim: VerifiedClaim,
    mct: MembranceClearanceToken
) -> List[EpistemicQuantum]:
    """
    Decompose a verified claim into one or more atomic epistemic quanta.

    Definition: A compound claim contains multiple independent assertive
    statements. These are detected by:
      1. Conjunction parsing: claim contains coordinating conjunctions
         (and, also, furthermore, additionally, moreover) joining
         independent clauses that each make a distinct assertion.
      2. claim_count field: if the PCVM VTD indicates claim_count > 1.
      3. Multi-sentence assertion: multiple sentences each containing
         a distinct predication.

    Atomic sub-claims: A claim is atomic if it makes exactly one assertive
    statement about one subject with one predicate. Atomic claims cannot
    be further decomposed without losing their assertive content.
    """
    # Step 1: Detect whether the claim is compound
    sub_statements = _extract_sub_claims(claim.statement)

    if len(sub_statements) <= 1:
        # Simple (atomic) claim -- return single quantum
        q = EpistemicQuantum()
        q.id = generate_quantum_id(claim)
        q.content = TypedContent(
            claim_text=claim.statement,
            claim_type=map_class_to_type(mct.assigned_class),
            domain_tags=extract_domain_tags(claim),
            evidence=claim.evidence or []
        )
        q.claim_class = mct.assigned_class
        return [q]

    # Step 2: Decompose into atomic sub-claims
    quanta = []
    for i, sub_statement in enumerate(sub_statements):
        q = EpistemicQuantum()

        # Each sub-claim gets its own ID with a decomposition suffix
        q.id = generate_quantum_id(claim, suffix=f":d{i}")

        q.content = TypedContent(
            claim_text=sub_statement,
            claim_type=map_class_to_type(mct.assigned_class),
            domain_tags=extract_domain_tags_for_subclaim(sub_statement, claim),
            evidence=claim.evidence or []  # all sub-claims inherit full evidence
        )

        # Sub-claims inherit the parent's claim class
        q.claim_class = mct.assigned_class

        # Provenance: inherits parent provenance with decomposition step added
        q.provenance = W3C_PROV_Record(
            generating_agent=claim.provenance.agent_id,
            generating_activity="ingestion",
            generation_time=current_timestamp(),
            generation_epoch=current_epoch(),
            derived_from=[claim.id],
            method="compound_claim_decomposition",
            attribution_chain=claim.provenance.attribution_chain + [
                AttributionStep(
                    agent_id="ema:ingestion_pipeline",
                    role="decomposer",
                    timestamp=current_timestamp()
                )
            ]
        )

        # Each sub-claim gets independent classification through PCVM.
        # However, for ingestion efficiency the parent MCT covers all
        # sub-claims. Independent verification happens post-ingestion
        # if any sub-claim's credibility diverges from the parent.
        q.opinion = map_pcvm_opinion(mct.opinion)

        quanta.append(q)

    # Step 3: Create DERIVATION edges between sub-claims and implicit
    # SUPPORT edges (sub-claims from the same compound claim are
    # initially assumed to support each other).
    for i in range(len(quanta)):
        for j in range(i + 1, len(quanta)):
            # Mutual support: sub-claims from same compound claim
            create_edge(quanta[i], quanta[j], "SUPPORT",
                        weight=DECOMPOSITION_SIBLING_WEIGHT)  # 0.3

    return quanta


def _extract_sub_claims(statement: str) -> List[str]:
    """
    Extract atomic sub-claims from a compound statement.

    Uses conjunction-based splitting and sentence boundary detection.
    Each extracted sub-claim is a self-contained assertive statement.
    """
    # Strategy 1: Split on coordinating conjunctions joining independent clauses
    CONJUNCTION_PATTERNS = [
        r',\s*and\s+',           # ", and"
        r';\s*',                  # semicolons separating independent clauses
        r',\s*also\s+',          # ", also"
        r'\.\s*Furthermore,?\s+', # "Furthermore,"
        r'\.\s*Additionally,?\s+', # "Additionally,"
        r'\.\s*Moreover,?\s+',   # "Moreover,"
    ]

    candidates = [statement]
    for pattern in CONJUNCTION_PATTERNS:
        new_candidates = []
        for candidate in candidates:
            parts = re.split(pattern, candidate)
            new_candidates.extend(parts)
        candidates = new_candidates

    # Filter: each sub-claim must be a meaningful assertion
    # (at least 10 characters, contains a verb-like structure)
    sub_claims = []
    for candidate in candidates:
        candidate = candidate.strip()
        if len(candidate) >= 10 and _is_assertive(candidate):
            sub_claims.append(candidate)

    # If splitting produced only 1 result, the claim is atomic
    if len(sub_claims) <= 1:
        return [statement]

    return sub_claims


def _is_assertive(text: str) -> bool:
    """
    Heuristic check that a text fragment is an assertive statement
    (not a dangling clause fragment).

    Returns True if the text appears to be a complete assertion.
    """
    # Must contain at least one word that looks like a verb/predicate
    # This is a heuristic; full NLP parsing is not required at this stage
    words = text.split()
    if len(words) < 3:
        return False
    # Check for subject-verb structure (at minimum)
    return True  # conservative: accept anything with 3+ words


# New configurable parameter
DECOMPOSITION_SIBLING_WEIGHT = 0.3  # Range: [0.1, 0.6], Section 5.1
```

---

## PA-6: F41 -- Parameter Deployment Profiles

**Severity:** MEDIUM
**Affects:** Appendix D (Configurable Parameters Table)

### Problem

All parameters in Appendix D have single default values. No guidance exists for adapting parameters to different deployment scales. The scale tiers (Section 7.5) define coherence modes but not parameter adjustments.

### Deployment Profiles

Three deployment profiles are defined. Implementations SHOULD select a profile at deployment time and MAY override individual parameters within a profile.

| # | Parameter | Section | T1 (Dev/Test, 10-100 agents) | T2 (Prod Small, 100-1000 agents) | T3 (Prod Large, 1000+ agents) |
|---|-----------|---------|------------------------------|----------------------------------|-------------------------------|
| 1 | DECAY_THRESHOLD | 4.3 | 0.20 | 0.30 | 0.35 |
| 2 | QUARANTINE_THRESHOLD | 4.3 | 0.10 | 0.15 | 0.18 |
| 3 | MAX_QUARANTINE_EPOCHS | 4.3 | 20 | 100 | 200 |
| 4 | BASE_DECAY_RATE | 4.4 | 0.01 | 0.005 | 0.003 |
| 5 | MAX_EDGES_PER_QUANTUM | 7.4 | 100 | 50 | 30 |
| 6 | MAX_EDGES_PER_SHARD | 7.4 | 1,000,000 | 500,000 | 200,000 |
| 7 | MIN_CLUSTER_SIZE | 5.3.1 | 3 | 5 | 7 |
| 8 | MIN_INDEPENDENT_AGENTS | 5.3.2 | 3 | 5 | 8 |
| 9 | MIN_INDEPENDENT_PARCELS | 5.3.2 | 2 | 3 | 4 |
| 10 | CONSOLIDATION_LOCK_TTL | 5.3.3 | 10 | 5 | 3 |
| 11 | SYNTHESIS_TEMPERATURE | 5.3.4 | 0.5 | 0.3 | 0.3 |
| 12 | STRUCTURAL_PROTECTION_THRESHOLD | 5.4.2 | 5 | 10 | 20 |
| 13 | IMMUNE_AUDIT_INTERVAL | 6.8 | 10 | 50 | 100 |
| 14 | BUDGET_SAFETY_MARGIN | 6.3 | 0.05 | 0.15 | 0.25 |
| 15 | EDGE_DISCOVERY_THRESHOLD | 5.1 | 0.3 | 0.4 | 0.5 |

### Profile Rationale

**T1 (Development/Testing, 10-100 agents):**
- Lower decay/quarantine thresholds: preserve more quanta for debugging and inspection.
- Higher edge limits: full graph visibility is more important than memory savings.
- Relaxed diversity requirements (3 agents, 2 parcels): small deployments cannot satisfy strict diversity.
- Higher synthesis temperature: more exploratory consolidation for testing dreaming.
- Lower structural protection: fewer quanta exist, so lower citation counts are meaningful.
- Frequent immune audit: rapid feedback on catabolism behavior during development.

**T2 (Production Small, 100-1000 agents):**
- Standard defaults from v1.0.0. This is the baseline the spec was designed for.
- Balanced trade-off between knowledge preservation and resource efficiency.

**T3 (Production Large, 1000+ agents):**
- Tighter edge budgets: memory pressure requires aggressive edge pruning.
- Higher diversity requirements: large populations can satisfy stricter thresholds.
- Shorter consolidation lock TTL: more contention requires faster lock release.
- Higher structural protection: in large graphs, citation count 10 is relatively low.
- Larger safety margin: larger systems have more variance in throughput.
- Higher edge discovery threshold: reduces initial edge creation to manage graph density.

---

## PA-7: F42 -- Vitality Multiplicative Composition Rationale and Floor

**Severity:** MEDIUM
**Affects:** Section 4.4 (Vitality Computation)

### Design Rationale

The vitality computation in Section 4.4 uses multiplicative composition:

```
vitality = base_decay * access_recency * support_factor
           * (1.0 - contradiction_factor) * credibility
           * (1.0 - supersession_penalty)
```

**This is intentional.** Multiplicative composition enforces the invariant that ALL health factors must be non-zero for a quantum to remain viable. A single catastrophic factor (e.g., full supersession, zero credibility) drives vitality toward zero regardless of other factors. This models the biological principle that an organism cannot compensate for total organ failure in one system by having excellent health in another.

The alternative (additive/weighted-average composition) would allow a quantum with zero credibility but high access recency to maintain moderate vitality. This is semantically wrong: a quantum with zero credibility has no epistemic value regardless of how often it is accessed.

### Minimum Floor

However, multiplicative composition creates a failure mode: a single factor momentarily reaching zero (e.g., credibility drops to 0.0 due to a transient opinion update) causes immediate vitality collapse, which may trigger irreversible catabolism before the factor recovers. To prevent this:

**Correction to Section 4.4 -- add vitality floor and grace period:**

```python
def compute_vitality(q: EpistemicQuantum, epoch: EpochNum) -> float:
    # [... existing computation unchanged through line 372 ...]

    # Composite (multiplicative -- all factors must be healthy)
    raw_vitality = (base_decay * access_recency * support_factor
                    * (1.0 - contradiction_factor) * credibility
                    * (1.0 - supersession_penalty))

    # PA-7 FIX: Apply minimum vitality floor.
    # Prevents instant catabolism from a single transient zero factor.
    vitality = max(raw_vitality, VITALITY_FLOOR)  # 0.05

    return clamp(vitality, 0.0, 1.0)


# Grace period logic in catabolism phase:
def evaluate_catabolism_candidate(q: EpistemicQuantum, epoch: EpochNum) -> bool:
    """
    Check whether a quantum should enter catabolism.
    Quanta at the vitality floor enter a grace period before dissolution.
    """
    vitality = compute_vitality(q, epoch)

    if vitality <= VITALITY_FLOOR:
        # Quantum is at the floor. Check grace period.
        if q.metabolic_state.floor_entry_epoch is None:
            # First epoch at floor -- start grace period
            q.metabolic_state.floor_entry_epoch = epoch
            return False  # Not yet a catabolism candidate

        grace_elapsed = epoch - q.metabolic_state.floor_entry_epoch
        if grace_elapsed < VITALITY_GRACE_PERIOD:  # 5 tidal epochs
            return False  # Still in grace period

        # Grace period expired -- proceed with normal catabolism evaluation
        return True

    else:
        # Above floor -- reset grace period tracker
        q.metabolic_state.floor_entry_epoch = None
        # Normal catabolism threshold check
        return vitality < DECAY_THRESHOLD
```

### New Parameters

Add to Appendix D.1 (Metabolic State Parameters):

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| VITALITY_FLOOR | 0.05 | [0.01, 0.10] | 4.4 |
| VITALITY_GRACE_PERIOD | 5 | [2, 20] | 4.4 |

### Schema Addition

Add to Appendix A, under `metabolic_state.properties`:

```json
"floor_entry_epoch": {
    "oneOf": [{ "type": "null" }, { "type": "integer", "minimum": 0 }],
    "default": null,
    "description": "Epoch when vitality first hit VITALITY_FLOOR. Null if above floor."
}
```

---

## PA-8: F43 -- TV-6 Rejection Behavior Correction

**Severity:** MEDIUM
**Affects:** Appendix F, Test Vector TV-6 (Section F.6)

### Problem

TV-6 states that edges 4-5 are "rejected" when the per-agent contradiction cap is exceeded. This is under-specified and inconsistent with the principle that contradictions should always be recorded (even at reduced influence) to maintain provenance completeness (INV-E9).

### Corrected Behavior

When a new contradiction edge would cause an agent's total contradiction weight against a target quantum to exceed MAX_AGENT_CONTRADICTION_WEIGHT (0.3, INV-E10), the system does NOT reject the edge. Instead:

1. The edge IS created, but at reduced weight.
2. The reduced weight is computed as: `remaining_budget / pending_edge_count`, where `remaining_budget = MAX_AGENT_CONTRADICTION_WEIGHT - current_accumulated_weight`.
3. A WARN-level signal is emitted to the Sentinel Graph.

```python
def create_contradiction_edge_with_cap(
    source: EpistemicQuantum,
    target: EpistemicQuantum,
    proposed_weight: float,
    creating_agent: str
) -> EpistemicEdge:
    """
    Create a contradiction edge respecting the per-agent cap (INV-E10).

    If the proposed weight would exceed the cap, the edge is created
    at reduced weight rather than rejected.
    """
    # Compute current accumulated weight for this agent against this target
    current_weight = sum(
        e.weight for e in target.edges
        if e.edge_type == "CONTRADICTION"
        and e.creating_agent == creating_agent
    )

    remaining_budget = MAX_AGENT_CONTRADICTION_WEIGHT - current_weight

    if remaining_budget <= 0.0:
        # Agent has fully exhausted contradiction budget for this target.
        # Create edge at minimum weight to preserve provenance record.
        capped_weight = MIN_EDGE_WEIGHT  # 0.05
        sentinel.emit_warning(
            "CONTRADICTION_CAP_EXCEEDED",
            agent=creating_agent,
            target=target.id,
            proposed=proposed_weight,
            actual=capped_weight,
            message=f"Agent {creating_agent} contradiction budget exhausted "
                    f"for target {target.id}. Edge created at minimum weight."
        )
    elif proposed_weight > remaining_budget:
        # Partial budget remaining -- cap to remaining budget
        capped_weight = remaining_budget
        sentinel.emit_warning(
            "CONTRADICTION_CAP_REDUCED",
            agent=creating_agent,
            target=target.id,
            proposed=proposed_weight,
            actual=capped_weight,
            message=f"Agent {creating_agent} contradiction weight reduced "
                    f"from {proposed_weight:.2f} to {capped_weight:.2f} "
                    f"(remaining budget: {remaining_budget:.2f})."
        )
    else:
        # Within budget -- use proposed weight
        capped_weight = proposed_weight

    edge = create_edge(
        source=source,
        target=target,
        edge_type="CONTRADICTION",
        weight=capped_weight,
        creating_agent=creating_agent
    )

    return edge
```

### Corrected TV-6

**Input:** Agent creates 5 contradiction edges (proposed weight 0.1 each) to target quantum.

**Expected:**
- Edge 1: created at weight 0.1 (cumulative: 0.1)
- Edge 2: created at weight 0.1 (cumulative: 0.2)
- Edge 3: created at weight 0.1 (cumulative: 0.3 = cap)
- Edge 4: created at weight 0.05 (minimum weight; remaining budget 0.0; WARN emitted)
- Edge 5: created at weight 0.05 (minimum weight; remaining budget 0.0; WARN emitted)

All 5 edges exist in the coherence graph. The agent's total effective contradiction weight is capped at 0.3 for vitality computation (per Section 4.4), but the additional edges at minimum weight preserve the provenance record that the agent attempted further contradiction.

---

## PA-9: F44 -- PCVM Outage Degraded Mode

**Severity:** LOW
**Affects:** Section 10.1 (PCVM Interface)

### Problem

No behavior is defined for when PCVM is unreachable. Since PCVM is a mandatory gate for ingestion (INV-E2) and consolidation (CR-14), an outage blocks both processes entirely.

### Degraded Mode Specification

```python
class PCVMDegradedMode:
    """
    Degraded-mode behavior when PCVM is unreachable.

    Detection: PCVM health check fails for PCVM_OUTAGE_DETECTION_EPOCHS
    consecutive epochs (default: 3).

    Recovery: PCVM health check succeeds. Drain queued items FIFO.
    """

    # Configuration
    MAX_QUEUE_DEPTH_PER_LOCUS = 1000   # Range: [100, 10000]
    PCVM_OUTAGE_DETECTION_EPOCHS = 3   # Range: [1, 10]
    PCVM_RECOVERY_DRAIN_RATE = 50      # Claims per epoch during recovery

    def on_pcvm_outage_detected(self, state):
        """Called when PCVM is confirmed unreachable."""
        state.pcvm_status = "DEGRADED"
        sentinel.emit_alert(
            "PCVM_OUTAGE",
            severity="HIGH",
            message="PCVM unreachable. Entering degraded mode."
        )

    def handle_ingestion_degraded(self, claim, mct_pending, locus):
        """
        Ingestion during PCVM outage.

        Behavior: Queue incoming claims. Do NOT create quanta (INV-E2
        prohibits ACTIVE state without PCVM verification).
        """
        queue = self.ingestion_queues[locus]

        if len(queue) >= self.MAX_QUEUE_DEPTH_PER_LOCUS:
            # Queue full -- apply backpressure
            sentinel.emit_warning(
                "INGESTION_QUEUE_FULL",
                locus=locus,
                depth=len(queue),
                message=f"Locus {locus} ingestion queue at capacity. "
                        f"Claims will be dropped until PCVM recovers."
            )
            return REJECTED("ingestion_queue_full")

        queue.append(QueuedClaim(
            claim=claim,
            queued_at_epoch=current_epoch(),
            locus=locus
        ))
        return QUEUED

    def handle_consolidation_degraded(self, state):
        """
        Consolidation during PCVM outage.

        Behavior: Pause dreaming entirely. K-class claims cannot be
        submitted without PCVM verification (CR-14). Consolidation
        candidates are still identified and cached for when PCVM
        recovers, but no LLM synthesis is executed.
        """
        state.dreaming_paused = True
        # Cache candidate sets for post-recovery processing
        candidates = identify_consolidation_candidates(state.shard, current_epoch())
        state.deferred_consolidation_candidates.extend(candidates)

    def handle_existing_quanta_degraded(self, state):
        """
        Existing quanta during PCVM outage.

        Behavior: Continue metabolic lifecycle (circulation, edge
        dynamics, catabolism evaluation) but with FROZEN credibility
        scores. No opinion updates are permitted because opinion
        changes may require re-verification.

        Specifically:
          - Circulation: continues normally
          - Edge dynamics: Hebbian reinforcement and decay continue
          - Catabolism: continues using last-known vitality scores
          - Opinions: FROZEN at pre-outage values
          - Re-verification triggers: queued, not executed
        """
        for q in state.all_active_quanta():
            q.metabolic_state.opinion_frozen = True

    def on_pcvm_recovery(self, state):
        """
        Called when PCVM becomes reachable again.

        Recovery protocol:
          1. Unfreeze opinions on all quanta
          2. Drain ingestion queue FIFO at controlled rate
          3. Process deferred consolidation candidates
          4. Resume normal operations
        """
        state.pcvm_status = "HEALTHY"

        # Step 1: Unfreeze opinions
        for q in state.all_active_quanta():
            q.metabolic_state.opinion_frozen = False

        # Step 2: Drain ingestion queue FIFO
        for locus, queue in self.ingestion_queues.items():
            # Process at controlled rate to avoid ingestion spike
            batch_size = min(
                self.PCVM_RECOVERY_DRAIN_RATE,
                len(queue)
            )
            for _ in range(batch_size):
                queued_claim = queue.popleft()  # FIFO order
                # Submit to PCVM for verification, then ingest normally
                result = pcvm.submit_for_verification(
                    construct_vtd(queued_claim.claim)
                )
                if result.admitted:
                    ingest(result.claim, result.mct, result.vtd_ref, result.bdl)

            # Remaining items stay in queue for next epoch's drain cycle

        # Step 3: Resume dreaming with deferred candidates
        state.dreaming_paused = False
        # Deferred candidates will be picked up in the next
        # consolidation phase

        sentinel.emit_alert(
            "PCVM_RECOVERED",
            severity="INFO",
            message=f"PCVM recovered. Draining {sum(len(q) for q in self.ingestion_queues.values())} "
                    f"queued claims."
        )
```

### New Parameters

Add to Appendix D:

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| MAX_QUEUE_DEPTH_PER_LOCUS | 1000 | [100, 10000] | 10.1 |
| PCVM_OUTAGE_DETECTION_EPOCHS | 3 | [1, 10] | 10.1 |
| PCVM_RECOVERY_DRAIN_RATE | 50 | [10, 500] | 10.1 |

---

## PA-10: F45 -- Dreaming Temperature Rationale

**Severity:** LOW
**Affects:** Section 5.3.4 (Three-Pass LLM Synthesis)

### Problem

SYNTHESIS_TEMPERATURE is set to 0.3 with no rationale. The Appendix D range goes up to 0.7, but no guidance is given on why 0.3 was chosen or how temperature affects dreaming quality.

### Rationale and Two-Temperature Design

**Why 0.3 for synthesis:** Temperature 0.3 produces conservative, high-probability token sequences. For consolidation, this is correct: the synthesis step is making epistemic claims that will be submitted to PCVM for verification. High temperature (0.7+) increases hallucination risk -- the LLM generates plausible-sounding but unsupported cross-domain patterns. At 0.3, the LLM favors patterns strongly supported by the input context, reducing false positives.

**However, 0.3 alone misses creative connections.** The strongest cross-domain insights often require exploratory reasoning that low temperature suppresses. A two-temperature approach balances creativity with reliability:

### Corrected Three-Pass LLM Synthesis

**Replaces:** Section 5.3.4 `execute_llm_synthesis`.

```python
# Temperature configuration
EXPLORATION_TEMPERATURE = 0.7    # Range: [0.5, 0.9], higher = more creative
SYNTHESIS_TEMPERATURE = 0.3      # Range: [0.1, 0.5], lower = more conservative

def execute_llm_synthesis(candidate, session_id):
    """
    Two-temperature three-pass synthesis.

    Phase A (Exploration, T=0.7): Generate diverse candidate patterns.
    Phase B (Synthesis, T=0.3): Filter and refine candidates.

    The exploration pass generates candidates that the synthesis pass
    would never produce on its own. The synthesis pass filters out
    hallucinations that the exploration pass inevitably introduces.
    """
    context = prepare_synthesis_context(candidate.quanta)

    # ---- Phase A: Exploration (temperature = 0.7) ----
    # Goal: generate diverse candidate patterns, accepting higher noise

    # Pass 0: Inductive generalization (exploratory)
    explore_0 = llm_inference(
        prompt_inductive(context),
        temperature=EXPLORATION_TEMPERATURE,
        max_tokens=2048
    )

    # Pass 1: Cross-domain pattern detection (exploratory)
    explore_1 = llm_inference(
        prompt_analogy(context),
        temperature=EXPLORATION_TEMPERATURE,
        max_tokens=2048
    )

    # Pass 2: Predictive synthesis (exploratory)
    explore_2 = llm_inference(
        prompt_predictive(context),
        temperature=EXPLORATION_TEMPERATURE,
        max_tokens=2048
    )

    # Collect all exploration candidates
    exploration_claims = parse_all([explore_0, explore_1, explore_2])

    # ---- Phase B: Synthesis filter (temperature = 0.3) ----
    # Goal: validate exploration candidates with conservative reasoning

    # Present exploration candidates to the LLM at low temperature
    # and ask: "Which of these patterns are well-supported by the evidence?"
    filter_prompt = construct_filter_prompt(
        context=context,
        candidates=exploration_claims
    )
    filter_result = llm_inference(
        filter_prompt,
        temperature=SYNTHESIS_TEMPERATURE,
        max_tokens=2048
    )

    # Parse which candidates survived the conservative filter
    filtered_claims = parse_filter_result(filter_result, exploration_claims)

    # ---- Majority voting across exploration passes ----
    # Cluster similar claims and require presence in >= 2 of 3 exploration passes
    clusters = cluster_by_similarity(filtered_claims, threshold=0.8)
    confirmed = [
        select_representative(c) for c in clusters
        if count_distinct_passes(c) >= MAJORITY_THRESHOLD  # 2
    ]

    # Final deduplication against existing active quanta
    return [c for c in confirmed if not is_duplicate(c, candidate.shard)]
```

### New Parameters

Add to Appendix D.3 (Consolidation Parameters):

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| EXPLORATION_TEMPERATURE | 0.7 | [0.5, 0.9] | 5.3.4 |

**Note:** SYNTHESIS_TEMPERATURE (0.3) remains as defined. The two temperatures serve complementary roles. Neither should be adjusted independently without understanding the trade-off: raising SYNTHESIS_TEMPERATURE increases false positive rate; lowering EXPLORATION_TEMPERATURE reduces novel pattern discovery.

---

## PA-11: F46 -- Immune Self-Audit Lookback Window

**Severity:** LOW
**Affects:** Section 6.8 (Immune Self-Audit)

### Problem

`recently_quarantined` and `recently_dissolved` are referenced in the immune self-audit (Section 6.8) but "recently" is not defined.

### Definition

```python
# Lookback window for immune self-audit
IMMUNE_AUDIT_LOOKBACK_EPOCHS = 5  # Range: [2, 20]

def get_recently_quarantined(state, epoch) -> List[EpistemicQuantum]:
    """
    Return quanta that entered QUARANTINE state within the last
    IMMUNE_AUDIT_LOOKBACK_EPOCHS tidal epochs.

    "Recently quarantined" = quanta whose metabolic state transitioned
    to QUARANTINED at any epoch E where:
        (epoch - IMMUNE_AUDIT_LOOKBACK_EPOCHS) <= E <= epoch
    """
    cutoff = epoch - IMMUNE_AUDIT_LOOKBACK_EPOCHS
    return [
        q for q in state.all_quarantined_quanta()
        if q.metabolic_state.quarantine_entry_epoch is not None
        and q.metabolic_state.quarantine_entry_epoch >= cutoff
    ]


def get_recently_dissolved(state, epoch) -> List[EpistemicQuantum]:
    """
    Return quanta that were dissolved within the last
    IMMUNE_AUDIT_LOOKBACK_EPOCHS tidal epochs.

    "Recently dissolved" = quanta whose dissolution_record.dissolved_at_epoch
    falls within the lookback window.
    """
    cutoff = epoch - IMMUNE_AUDIT_LOOKBACK_EPOCHS
    return [
        q for q in state.all_dissolved_quanta()
        if q.dissolution_record is not None
        and q.dissolution_record.dissolved_at_epoch >= cutoff
    ]
```

### Corrected Immune Self-Audit

**Replaces:** the `recently_quarantined` and `recently_dissolved` references in Section 6.8:

```python
def execute_immune_self_audit(state, epoch):
    # Sample 10% of quanta quarantined in the last 5 tidal epochs
    recently_quarantined = get_recently_quarantined(state, epoch)
    sample = random_sample(recently_quarantined, rate=0.10)

    # [... remainder of audit logic unchanged ...]

    # Under-detection check: sample recently dissolved quanta
    recently_dissolved = get_recently_dissolved(state, epoch)
    dissolved_sample = random_sample(recently_dissolved, rate=0.10)

    # [... remainder unchanged ...]
```

### New Parameters

Add to Appendix D.5 (SHREC Parameters):

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| IMMUNE_AUDIT_LOOKBACK_EPOCHS | 5 | [2, 20] | 6.8 |

### Schema Addition

Add to Appendix A, under `metabolic_state.properties`:

```json
"quarantine_entry_epoch": {
    "oneOf": [{ "type": "null" }, { "type": "integer", "minimum": 0 }],
    "default": null,
    "description": "Epoch when quantum entered QUARANTINED state. Null if not quarantined."
}
```

---

## PA-12: Claim Class Mapping Correction (C9 Reconciliation)

**Severity:** HIGH (cross-system inconsistency)
**Affects:** Section 5.1 (Claim Class to Claim Type Mapping table)

### Problem

The v1.0.0 mapping table maps PCVM class "C" to EMA type "consolidation" with the label "C (Consolidation)." However, per C9 cross-system reconciliation:

1. PCVM class "C" is **Compliance**, not Consolidation. Compliance claims observe whether agents or processes conform to governance rules.
2. Consolidation outputs from EMA's dreaming pipeline should use PCVM class "K" (Knowledge Consolidation), which is the dedicated class for dreaming outputs.

The v1.0.0 spec conflates these two classes, causing consolidation outputs to be misclassified as compliance claims in PCVM.

### Corrected Mapping Table

**Replaces:** "Claim Class to Claim Type Mapping" table in Section 5.1.

| PCVM Class | EMA Type | Rationale |
|-----------|---------|-----------|
| D (Deterministic) | observation | Computation results are observations |
| E (Empirical) | observation | Direct mapping |
| S (Statistical) | inference | Statistical conclusions are inferred |
| H (Heuristic) | inference | Heuristic judgments are inferred |
| N (Normative) | governance | Normative claims are governance rules |
| P (Process) | observation | Process compliance is observed |
| R (Reasoning) | inference | Reasoning produces inferences |
| **C (Compliance)** | **observation** | **Compliance is observed against rules** |
| **K (Knowledge Consolidation)** | **consolidation** | **From dreaming** |

### Affected References

The following sections reference "C-class" when they mean consolidation outputs. These MUST be read as "K-class" post-patch:

1. **Section 5.3.5** (`construct_c_class_vtd`): should be `construct_k_class_vtd`. The VTD is K-class, not C-class.
2. **Section 5.3.5** ("C-class claims start with high uncertainty"): should read "K-class claims start with high uncertainty (>= 0.4)."
3. **Section 5.3.6** (`q.claim_class != "C"`): should be `q.claim_class != "K"`.
4. **Section 5.3.6** (`q.content.claim_type != "consolidation"`): unchanged (still correct).
5. **Section 10.1** ("C-class submission"): should read "K-class submission."
6. **Section 10.1** ("C-class VTDs"): should read "K-class VTDs."
7. **Appendix A** (`claim_class` enum): add "K" to the enum: `["D", "E", "S", "H", "N", "P", "R", "C", "K"]`.
8. **Appendix H** (Glossary, "Claim Class"): update to list 9 classes including K.
9. **TV-4** (Appendix F.4): "claim_class='C'" should be "claim_class='K'".

### Schema Correction

In Appendix A, replace:

```json
"claim_class": { "type": "string", "enum": ["D", "E", "S", "H", "N", "P", "R", "C"] }
```

With:

```json
"claim_class": { "type": "string", "enum": ["D", "E", "S", "H", "N", "P", "R", "C", "K"] }
```

---

## Summary of New Parameters Introduced

| Parameter | Default | Introduced By |
|-----------|---------|---------------|
| CROSS_SHARD_BONUS | 0.2 | PA-4 (F39) |
| DECOMPOSITION_SIBLING_WEIGHT | 0.3 | PA-5 (F40) |
| VITALITY_FLOOR | 0.05 | PA-7 (F42) |
| VITALITY_GRACE_PERIOD | 5 epochs | PA-7 (F42) |
| EXPLORATION_TEMPERATURE | 0.7 | PA-10 (F45) |
| IMMUNE_AUDIT_LOOKBACK_EPOCHS | 5 epochs | PA-11 (F46) |
| MAX_QUEUE_DEPTH_PER_LOCUS | 1000 | PA-9 (F44) |
| PCVM_OUTAGE_DETECTION_EPOCHS | 3 | PA-9 (F44) |
| PCVM_RECOVERY_DRAIN_RATE | 50 | PA-9 (F44) |

## Summary of Schema Additions

| Field | Location | Introduced By |
|-------|----------|---------------|
| `metabolic_state.floor_entry_epoch` | Appendix A | PA-7 (F42) |
| `metabolic_state.quarantine_entry_epoch` | Appendix A | PA-11 (F46) |
| `metabolic_state.opinion_frozen` | Appendix A | PA-9 (F44) |
| `claim_class` enum: add "K" | Appendix A | PA-12 |

---

*Patch Addendum v1.1.0 -- produced under Atrahasis Agent System v2.0 protocol.*
*Applies to: C6 EMA Master Tech Spec v1.0.0.*
*Status: NORMATIVE ADDENDUM.*
