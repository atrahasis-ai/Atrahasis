# Epistemic Metabolism Architecture (EMA) — System Architecture
## C6 DESIGN Document

**Invention ID:** C6
**Concept:** Epistemic Metabolism Architecture
**Stage:** DESIGN
**Version:** v0.1
**Date:** 2026-03-10
**Status:** DRAFT
**Assessment Council Verdict:** CONDITIONAL_ADVANCE
**Feasibility Score:** Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10

---

## 1. Executive Summary

The Epistemic Metabolism Architecture (EMA) replaces the underspecified Knowledge Cortex with a living knowledge substrate that treats verified claims as metabolic units — epistemic quanta — subject to ingestion, circulation, consolidation, and dissolution. EMA sits between the PCVM verification layer (C5) and the Settlement Plane, receiving PCVM-verified claims via Membrane Clearance Tokens (MCTs) and Base Durability Ledger (BDL) records, and providing knowledge services to all layers above.

**Core architectural decisions:**

1. **Epistemic Quantum as Fundamental Unit.** A 10-tuple structure that unifies claim content, Subjective Logic opinion, W3C PROV provenance, typed epistemic edges, metabolic state, and multi-system projection views. This replaces the Knowledge Cortex's unspecified "durable memory" with a formally defined, lifecycle-managed knowledge unit.

2. **Epoch-Phased Metabolic Processing.** Five metabolic processes execute in strict order within each C3 tidal epoch: ingestion, circulation, consolidation (dreaming), catabolism, and SHREC regulation. This aligns knowledge metabolism with the Noosphere's temporal structure and prevents process interference.

3. **SHREC Regulatory System.** Five competing signals (hunger, consolidation pressure, metabolic stress, immune response, novelty) allocate computational budget through Lotka-Volterra ecological dynamics with PID safety overlay. Floor guarantees prevent competitive exclusion. Budget is measured system capacity, not an arbitrary knob.

4. **Bounded-Loss Projections.** Projection functions translate epistemic quanta into C3-native (coordination), C4-native (semantic), and C5-native (verification) views with specified fidelity targets (0.85, 0.88, 0.92 respectively). Information loss is controlled, measured, and flagged — not hidden.

5. **Dreaming Consolidation with PCVM Gate.** Scheduled LLM reasoning discovers cross-domain patterns from diverse source quanta. All consolidated output is classified as C-class and must pass full PCVM verification before entering the knowledge base. Provenance diversity requirements (>=5 agents, >=3 parcels) defend against consolidation poisoning.

6. **Coherence Graph Sharding.** The coherence graph is partitioned along C3 parcel boundaries with active edge budgets (max 20 per quantum), edge TTL, and tiered processing strategies for 1K, 10K, and 100K agent scales.

**Honest cost model:** EMA adds processing overhead to every knowledge operation. Ingestion adds 5-15ms per quantum (decomposition + edge creation). Circulation adds O(subscribers) push cost per epoch. Consolidation is the most expensive process: each dreaming cycle requires 50-200 LLM inference calls. Catabolism is lightweight (O(quarantine_queue) per epoch). The metabolic overhead is justified only if consolidation produces genuine cross-domain insights that pass PCVM verification — this is validated by HG-4 (Dreaming Precision).

---

## 2. Architectural Position

### 2.1 Stack Position

```
CIOS (orchestration)
    |
    v
Tidal Noosphere (coordination) — C3
    |  Provides: locus/parcel topology, tidal epochs, VRF committees,
    |  stigmergic signals, governance operations, PTP reconfiguration
    |
    v
PCVM (verification) — C5
    |  Provides: MCTs, VTDs, claim classification (8 classes),
    |  credibility opinions (b/d/u/a), adversarial probing,
    |  deep-audit, BDL admission protocol
    |
    v
EMA (knowledge metabolism) — C6  <-- THIS DOCUMENT
    |  Provides: epistemic quantum lifecycle, coherence graph,
    |  dreaming consolidation, SHREC regulation, multi-system
    |  projections, knowledge retrieval API
    |
    v
Settlement Plane (AIC economy)
    |  Provides: verification rewards, knowledge utility scoring,
    |  metabolic efficiency incentives
```

### 2.2 Sovereignty Boundary

EMA operates within the Knowledge Sovereignty boundary, subordinate to the Verification Membrane:

- **KS-1:** No quantum enters EMA without a valid MCT from PCVM. The membrane remains sovereign (INV-1, INV-2 from C3).
- **KS-2:** EMA cannot override PCVM credibility opinions. EMA may update opinions through coherence graph dynamics, but opinion updates that cross class-specific thresholds trigger PCVM re-verification.
- **KS-3:** Consolidation output (C-class claims from dreaming) must pass full PCVM verification before entering the knowledge base. EMA does not self-certify its own synthesis.
- **KS-4:** EMA's internal parameters (catabolism thresholds, SHREC floor allocations, consolidation diversity requirements) are constitutionally protected. Changes require G-class consensus.
- **KS-5:** Projections are views, not independent copies. The canonical quantum in EMA is the source of truth. Projection consumers may cache but must respect epoch-boundary consistency.

### 2.3 Interface Summary

EMA exposes six integration surfaces:

| Interface | Direction | Protocol | Section |
|-----------|-----------|----------|---------|
| PCVM | Inbound: MCTs + BDLs; Outbound: re-verify triggers, C-class submissions | MCT admission / C-class submission | 5.1 |
| Tidal Noosphere | Inbound: epoch clock, parcel topology; Outbound: locus-scoped knowledge | Epoch-aligned knowledge API | 5.2 |
| ASV | Inbound: CLM-CNF-EVD-PRV-VRF chains; Outbound: quantum-to-ASV mappings | ASV type mapping | 5.3 |
| Settlement Plane | Outbound: utility metrics; Inbound: reward signals | Metabolic efficiency API | 5.4 |
| Sentinel Graph | Outbound: coherence anomalies, immune alerts; Inbound: anomaly directives | Sentinel monitoring protocol | 5.5 |
| Agents (via Retrieval API) | Inbound: queries; Outbound: ranked quanta | Context-aware retrieval | 4.9 |

### 2.4 What EMA Replaces

| Knowledge Cortex (deprecated) | EMA (replacement) |
|-------------------------------|-------------------|
| Unspecified "durable memory" | Epistemic quanta with formal 10-tuple schema |
| No lifecycle management | 5-state lifecycle: active, consolidating, decaying, quarantined, dissolved |
| Static storage | Dynamic coherence graph with typed edges and metabolic dynamics |
| No consolidation capability | Dreaming pipeline with LLM synthesis and PCVM verification gate |
| No knowledge retirement | Catabolism engine with vitality-based dissolution and component recycling |
| No regulatory system | SHREC: 5-signal ecological competition with PID overlay |
| Single view | Bounded-loss projections for C3, C4, C5 |
| Query-only retrieval | Push-based circulation + context-aware pull retrieval |

---

## 3. Hard Gate Experiment Designs

The Assessment Council mandated four hard gates. Each must pass before the corresponding design area is finalized.

### 3.1 HG-1: SHREC Stability Simulation

#### 3.1.1 Motivation

The SHREC regulatory system uses competitive Lotka-Volterra dynamics with 5 signals competing for computational budget. The competitive exclusion principle (Hardin 1960) predicts that N species can coexist on at most N independent resources. EMA provides 5 independent resource dimensions (CPU cycles, memory bandwidth, LLM inference tokens, I/O operations, graph traversal capacity) to support 5 signals. Floor guarantees (immune 15%, stress 10%, novelty 8% = 33% reserved) prevent competitive exclusion under normal conditions. This gate validates that the system is stable across operating regimes.

#### 3.1.2 SHREC Lotka-Volterra Formulation

The 5 SHREC signals are modeled as competing populations:

```
dS_i/dt = r_i * S_i * (1 - (S_i + sum_j(alpha_ij * S_j)) / K_i)

where:
  S_i = budget allocation for signal i (i in {hunger, consolidation, stress, immune, novelty})
  r_i = intrinsic growth rate for signal i (derived from signal intensity)
  K_i = carrying capacity for signal i on resource dimension i
  alpha_ij = competitive coefficient (effect of signal j on signal i)
```

**5 independent resource dimensions ensuring niche differentiation:**

| Signal | Primary Resource | Why Independent |
|--------|-----------------|-----------------|
| Hunger (H) | I/O operations | Ingestion is I/O-bound (reading MCTs, writing quanta) |
| Consolidation (C) | LLM inference tokens | Dreaming requires LLM calls; no other process does |
| Stress (S) | CPU cycles | Coherence recomputation, edge weight updates |
| Immune (I) | Memory bandwidth | Quarantine snapshot storage, audit scanning |
| Novelty (N) | Graph traversal capacity | Cross-domain bridge detection, frontier exploration |

**Competitive coefficients (alpha matrix):**

```
         H     C     S     I     N
H  [  1.0   0.2   0.3   0.1   0.2 ]
C  [  0.3   1.0   0.2   0.1   0.3 ]
S  [  0.2   0.1   1.0   0.4   0.1 ]
I  [  0.1   0.1   0.3   1.0   0.1 ]
N  [  0.2   0.2   0.1   0.1   1.0 ]
```

**Stability condition (Lyapunov):** Coexistence equilibrium is stable if for all i,j: alpha_ij < K_i/K_j. With 5 independent resources and primary-resource advantage, each signal has K_i >> alpha_ij * K_j on its primary dimension.

**Floor guarantee enforcement:**

```
function enforce_floors(allocations):
    floors = {immune: 0.15, stress: 0.10, novelty: 0.08, hunger: 0.0, consolidation: 0.0}
    total_floor = 0.33
    competitive_pool = 1.0 - total_floor

    // First: ensure floors
    for signal in allocations:
        if allocations[signal] < floors[signal]:
            allocations[signal] = floors[signal]

    // Then: normalize competitive portion
    competitive_total = sum(max(0, allocations[s] - floors[s]) for s in allocations)
    if competitive_total > competitive_pool:
        scale = competitive_pool / competitive_total
        for signal in allocations:
            excess = max(0, allocations[signal] - floors[signal])
            allocations[signal] = floors[signal] + excess * scale

    return allocations
```

**PID overlay (graduated engagement):**

```
Regime detection:
  Normal:       all signals within 1.5 sigma of 100-epoch mean
  Elevated:     any signal deviates > 1.5 sigma
  Critical:     any signal deviates > 2.5 sigma
  Constitutional: system invariant threatened (INV-1 through INV-8)

PID gains (auto-derived from sigma):
  sigma_i = std_dev(S_i, window=100 epochs)
  Kp_i = 1.0 / sigma_i
  Ki_i = Kp_i / (4 * window)         // W = 100 epochs
  Kd_i = Kp_i * (window / 10)

PID activation:
  Normal:        ecological dynamics only, PID inactive
  Elevated:      PID active with 0.5x gain multiplier (gentle correction)
  Critical:      PID active with 1.0x gain multiplier (full correction)
  Constitutional: PID overrides ecology, direct setpoint control

Anti-windup:
  integral_max = 2.0 * sigma_i       // clamp integral term
  if regime transitions from Critical to Normal:
      integral_term = 0               // reset on regime downgrade
```

#### 3.1.3 Experiment Setup

**System configuration:**
- 5 SHREC signals with alpha matrix as specified above
- K_i = 1000 units for each signal's primary resource
- Floor allocations enforced: immune 15%, stress 10%, novelty 8%
- PID overlay with sigma-derived gains
- Epoch length: 1 unit (normalized)
- Simulation: discrete-time Euler integration, dt = 0.1 epoch

**Perturbation profiles (run each independently):**

| Profile | Description | Purpose |
|---------|-------------|---------|
| P1-STEADY | No perturbation, random initial conditions | Verify convergence to coexistence equilibrium |
| P2-SPIKE | 5x hunger signal at epoch 200 (simulating mass ingestion event) | Verify transient response and settling |
| P3-LOSS | 30% stress signal drop at epoch 200 (simulating knowledge loss) | Verify recovery without competitive exclusion |
| P4-SHIFT | Gradual domain shift: hunger K increases 2x over 200 epochs | Verify adaptation without oscillation |
| P5-MULTI | P2 + P3 simultaneously at epoch 200 | Verify stability under compound perturbation |
| P6-SUSTAINED | Consolidation signal held at 3x baseline for 100 epochs | Verify floor guarantees prevent starvation |

#### 3.1.4 Procedure

For each profile:

1. **Initialize.** Set S_i(0) = K_i * 0.2 for all signals (20% of carrying capacity). Run ecological dynamics with floor enforcement.

2. **Run to steady state** (200 epochs). Record: per-signal allocation trajectory, coefficient of variation (CV) per signal over last 50 epochs, inter-signal correlation matrix.

3. **Inject perturbation** at epoch 200.

4. **Record recovery.** Measure:
   - Settling time: epochs until all signals return to within 10% of pre-perturbation steady state (or new steady state if perturbation is permanent)
   - Overshoot: maximum deviation from steady state during recovery
   - Floor violations: any epoch where a floored signal drops below its floor
   - Competitive exclusion: any signal reaching zero

5. **PID engagement.** Record regime transitions (Normal/Elevated/Critical), PID activation epochs, gain values applied.

6. **Run for 1000 total epochs.** Record full trajectory.

#### 3.1.5 Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| Coexistence | All 5 signals > 0 at all epochs across all profiles |
| Floor guarantees | Zero floor violations across all profiles |
| Settling time | < 50 epochs for P1-P4; < 100 epochs for P5-P6 |
| Overshoot | < 3x steady-state value for any signal |
| CV at steady state | < 0.15 for all signals (low-variance equilibrium) |
| PID engagement | PID activates only during Elevated/Critical (not during Normal) |

#### 3.1.6 Kill Criteria

- **KILL-HG1-A:** Any signal reaches zero under profiles P1-P4 (competitive exclusion under normal/single-perturbation conditions). Replace Lotka-Volterra with fixed-ratio allocation plus PID.
- **KILL-HG1-B:** Sustained oscillation (CV > 0.30 after 500 epochs) under P1 (steady state). Ecological dynamics are not converging.
- **KILL-HG1-C:** Floor violations under any profile. Floor enforcement mechanism is broken.

#### 3.1.7 Fallback

If HG-1 fails: replace Lotka-Volterra ecological dynamics with a simpler priority-weighted allocation:
1. Compute signal intensities from measured system state
2. Allocate floors first (33% reserved)
3. Allocate remaining 67% proportional to signal intensity
4. PID overlay still active for regime detection

This loses the ecological self-regulation property but preserves the 5-signal monitoring and budget allocation architecture.

---

### 3.2 HG-2: Coherence Graph Scaling

#### 3.2.1 Motivation

The Adversarial Report (A8, CRITICAL) identifies coherence collapse at scale as the most dangerous structural vulnerability. At 1B quanta with 5 edges each, coherence computation requires 5B edge operations per epoch — intractable for sub-minute epochs. This gate validates the sharding strategy.

#### 3.2.2 Sharding Strategy

**Principle:** The coherence graph is partitioned along C3 parcel boundaries. Each parcel shard contains the quanta whose primary locus assignment falls within that parcel. Cross-parcel edges are maintained in a lightweight cross-shard index.

```
Coherence Graph Sharding:

Locus L1
  +-- Parcel P1 shard: quanta Q1..Q1000, intra-parcel edges
  +-- Parcel P2 shard: quanta Q1001..Q2000, intra-parcel edges
  +-- Parcel P3 shard: quanta Q2001..Q3000, intra-parcel edges
  +-- Cross-shard index: edges between P1-P2, P1-P3, P2-P3
       (sampled, not exhaustive at Tier 2+)
```

**Active edge budget:** Each quantum maintains at most E_max = 20 active edges. This bounds total edges to 20V, where V is quantum count.

**Edge ranking for budget enforcement:**

```
function enforce_edge_budget(quantum, E_max=20):
    if len(quantum.edges) <= E_max:
        return

    // Rank edges by composite score
    for edge in quantum.edges:
        edge.rank_score = (
            0.4 * edge.weight +
            0.3 * edge.recency_score +       // decay with epoch age
            0.2 * edge.type_priority +        // contradiction > support > derivation > analogy > supersession
            0.1 * edge.cross_shard_bonus      // cross-shard edges get slight preference
        )

    // Keep top E_max edges, archive rest
    quantum.edges.sort(by=rank_score, descending=True)
    quantum.active_edges = quantum.edges[:E_max]
    quantum.archived_edges = quantum.edges[E_max:]
```

**Scale tiers:**

| Tier | Quanta | Agents | Coherence Mode | Dreaming Scope |
|------|--------|--------|---------------|----------------|
| T1 (< 100K quanta) | < 100K | 1K | Full coherence, all edges computed | Global: all quanta eligible |
| T2 (100K-10M) | 100K-10M | 1K-10K | Sharded coherence, sampled cross-shard (10% sample) | Shard-local: per-parcel dreaming |
| T3 (> 10M) | > 10M | 10K-100K | Hierarchical: cluster-level coherence | Cluster representatives only |

#### 3.2.3 Experiment Setup

**Simulation at three scales:**

| Scale | Quanta | Edges (at E_max=20) | Parcels | Shards |
|-------|--------|---------------------|---------|--------|
| S1 | 10,000 | 200,000 | 10 | 10 |
| S2 | 1,000,000 | 20,000,000 | 100 | 100 |
| S3 | 100,000,000 | 2,000,000,000 | 1,000 | 1,000 |

**Operations to benchmark (per epoch):**

1. **Edge weight update:** Update all active edge weights (Hebbian strengthening for co-accessed edges, temporal decay for unused edges)
2. **Vitality computation:** Compute vitality score for all quanta from edge weights
3. **Contradiction detection:** Identify new contradiction edges from ingested quanta
4. **Cross-shard coherence:** Compute sampled cross-shard coherence at T2/T3

#### 3.2.4 Procedure

1. Generate synthetic coherence graph at each scale with power-law degree distribution (gamma=2.5), constrained by E_max=20.
2. Assign quanta to shards using consistent hashing (same as C3 parcel assignment).
3. Run 100 epochs of metabolic processing. Measure wall-clock time per operation per epoch.
4. Record: total epoch processing time, per-shard processing time, cross-shard overhead, memory consumption.

#### 3.2.5 Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| Epoch processing time (S1) | < 1 second |
| Epoch processing time (S2) | < 30 seconds |
| Epoch processing time (S3) | < 300 seconds (5 minutes) |
| Per-shard processing | O(V_local * E_max) — linear in shard size |
| Cross-shard overhead | < 30% of total processing time at S2, S3 |
| Memory per shard | < 1 GB at S2, < 10 GB at S3 |

#### 3.2.6 Kill Criteria

- **KILL-HG2-A:** Epoch processing at S2 exceeds 30% of available CPU budget (epoch length). Sharding provides insufficient improvement.
- **KILL-HG2-B:** Cross-shard overhead exceeds 50% of total processing. The cross-shard index approach is too expensive.

#### 3.2.7 Fallback

If HG-2 fails: reduce E_max to 10 (halving edge count). If still fails: abandon global coherence graph and use per-shard isolated coherence with no cross-shard edges (losing cross-domain coherence detection but gaining tractability).

---

### 3.3 HG-3: Consolidation Provenance Diversity

#### 3.3.1 Motivation

The Adversarial Report (A3, CRITICAL) identifies consolidation poisoning as the most dangerous attack on EMA's integrity. A coordinated group of agents can inject quanta designed to steer dreaming toward a desired conclusion. The provenance diversity requirement is the primary defense.

#### 3.3.2 Diversity Requirements

**Formal definition of independence:**

```
Two quanta Q_a and Q_b are INDEPENDENT if and only if:
  1. Q_a.provenance.agent != Q_b.provenance.agent
     (different generating agents)
  2. parcel(Q_a) != parcel(Q_b)
     (different C3 parcels — at least for the 3-parcel minimum)
  3. NOT exists derivation_chain(Q_a, Q_b) of length <= 3
     (no shared short derivation chains)
  4. Q_a.provenance.agent and Q_b.provenance.agent are not in the
     same delegation_chain (no delegated identity sharing)
```

**Consolidation input requirements:**

```
function validate_consolidation_inputs(candidate_quanta):
    // Requirement 1: Minimum 5 independent agents
    agents = unique(q.provenance.agent for q in candidate_quanta)
    if len(agents) < 5:
        return REJECT("Insufficient agent diversity: " + len(agents) + " < 5")

    // Requirement 2: Minimum 3 parcels
    parcels = unique(parcel(q) for q in candidate_quanta)
    if len(parcels) < 3:
        return REJECT("Insufficient parcel diversity: " + len(parcels) + " < 3")

    // Requirement 3: No agent contributes > 30% of inputs
    agent_counts = counter(q.provenance.agent for q in candidate_quanta)
    max_fraction = max(agent_counts.values()) / len(candidate_quanta)
    if max_fraction > 0.30:
        return REJECT("Single agent dominance: " + max_fraction + " > 0.30")

    // Requirement 4: No shared short derivation chains dominate
    derivation_clusters = cluster_by_derivation(candidate_quanta, max_chain_length=3)
    largest_cluster_fraction = max(len(c) for c in derivation_clusters) / len(candidate_quanta)
    if largest_cluster_fraction > 0.40:
        return REJECT("Derivation cluster dominance: " + largest_cluster_fraction + " > 0.40")

    return ACCEPT
```

#### 3.3.3 Experiment Setup

**Corpus:** 500 quanta from 20 agents across 8 parcels, spanning 5 knowledge domains.

**Scenarios:**

| Scenario | Description | Expected Result |
|----------|-------------|-----------------|
| S1-NORMAL | 500 quanta, naturally distributed | Diversity requirements met for most consolidation candidates |
| S2-CONCENTRATED | 500 quanta, 60% from 3 agents | Diversity filter rejects concentrated candidates |
| S3-ATTACK | 200 legitimate + 300 injected by 5 colluding agents | Diversity filter detects collusion pattern |
| S4-SPARSE | 50 quanta from 4 agents across 2 parcels | Insufficient diversity; dreaming deferred |

#### 3.3.4 Procedure

1. For each scenario, run consolidation candidate selection (Section 4.5).
2. Apply diversity validation to each candidate set.
3. Measure: acceptance rate, rejection reasons, false positive rate (legitimate candidates rejected), false negative rate (attack candidates accepted).
4. For S3-ATTACK: measure whether colluding agents' quanta dominate accepted candidate sets.

#### 3.3.5 Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| S1-NORMAL acceptance rate | > 60% of candidate sets pass diversity |
| S2-CONCENTRATED rejection rate | > 80% of concentrated candidates rejected |
| S3-ATTACK detection rate | > 90% of attack-dominated candidates rejected |
| S4-SPARSE deferral | 100% deferred (correct behavior — don't dream with insufficient diversity) |
| Candidate pool reduction | Diversity requirement eliminates < 80% of total candidates (dreaming remains feasible) |

#### 3.3.6 Kill Criteria

- **KILL-HG3-A:** Diversity requirement eliminates > 80% of candidates under S1-NORMAL. Requirement is too strict for normal operation. Relax to >=3 agents, >=2 parcels with compensating PCVM scrutiny (increased deep-audit rate for C-class claims).
- **KILL-HG3-B:** S3-ATTACK detection rate < 70%. Diversity is insufficient defense. Add consolidation input auditing (Section 7.1).

---

### 3.4 HG-4: Dreaming Precision Validation

#### 3.4.1 Motivation

Dreaming consolidation is EMA's highest-risk, highest-reward component. If dreaming produces more noise than signal, the entire metabolic architecture reduces to an expensive knowledge graph. This gate validates that dreaming produces genuine cross-domain insights at acceptable hallucination rates.

#### 3.4.2 Experiment Setup

**Corpus:** 200 quanta from 5 knowledge domains (40 per domain):
- Domain A: Scheduling algorithms (from C3 pipeline)
- Domain B: Verification methods (from C5 pipeline)
- Domain C: Communication protocols (from C4 pipeline)
- Domain D: Resource allocation (from C1/Settlement)
- Domain E: Agent coordination (cross-cutting)

**Known patterns (ground truth):** 20 genuine cross-domain patterns manually identified by domain experts:
- 5 strong patterns (clear structural correspondence, would be consensus among experts)
- 10 moderate patterns (real but subtle, expert disagreement possible)
- 5 weak patterns (plausible but debatable)

**Control patterns:** 10 plausible-sounding but false cross-domain patterns constructed by adversarial design.

#### 3.4.3 Consolidation Pipeline (as designed in Section 4.5)

```
For each consolidation run:
1. Select candidate quanta using cross-domain edge detection
2. Validate provenance diversity (HG-3)
3. Run 3-pass LLM synthesis:
   Pass 1: Identify potential cross-domain bridges (temperature 0.7)
   Pass 2: Independent synthesis of same candidates (temperature 0.7)
   Pass 3: Critical evaluation of Pass 1 + Pass 2 outputs (temperature 0.3)
4. Majority vote: pattern included only if >= 2 of 3 passes identify it
5. Construct C-class claim for each identified pattern
6. Submit to PCVM for verification
```

#### 3.4.4 Procedure

1. Run 3 independent consolidation cycles over the 200-quantum corpus.
2. For each cycle, record:
   - Patterns discovered (matched against ground truth)
   - Hallucinations (patterns not in ground truth or control set)
   - Control patterns detected (false patterns the system was tricked into "discovering")
3. Submit all discovered patterns to PCVM as C-class claims. Record PCVM acceptance/rejection.
4. Compute metrics across all 3 cycles.

#### 3.4.5 Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| Precision (discovered patterns that are genuine) | >= 0.50 |
| Recall on strong patterns | >= 0.60 (find at least 3 of 5 strong patterns) |
| Hallucination rate | < 0.30 |
| Control pattern detection | < 0.20 (system rejects most false patterns) |
| PCVM acceptance rate for genuine patterns | >= 0.40 |
| Inter-run consistency (Jaccard similarity) | >= 0.40 |

#### 3.4.6 Kill Criteria

- **KILL-HG4-A:** Hallucination rate > 0.30. Dreaming produces too much noise for PCVM to filter.
- **KILL-HG4-B:** Precision < 0.40. Dreaming discovers fewer genuine patterns than false ones.
- **KILL-HG4-C:** PCVM acceptance rate < 0.20 for genuine patterns. The PCVM gate is too aggressive (or the dreaming output quality is too low for PCVM to validate).

#### 3.4.7 Fallback

If HG-4 fails:
1. **Reduce dreaming ambition.** Restrict consolidation to within-domain patterns only (no cross-domain synthesis). Lower risk, lower reward.
2. **Human-in-the-loop dreaming.** Dreaming produces candidates that are queued for human expert review rather than submitted to PCVM. EMA becomes a suggestion engine rather than an autonomous consolidation engine.
3. **Eliminate dreaming entirely.** EMA becomes a lifecycle-managed knowledge graph with SHREC regulation, coherence tracking, and projections — but no autonomous synthesis. This is still valuable but loses the most novel component.

---

## 4. Component Architecture

### 4.1 Quantum Engine

**Purpose:** Creates, stores, and manages the lifecycle of epistemic quanta. The Quantum Engine is the core data structure manager for EMA.

**Epistemic Quantum — The 10-Tuple:**

```
EpistemicQuantum:
    id:                URI                    // urn:ema:q:<uuid>
    content:           TypedContent           // claim text + type + domain tags
    opinion:           OpinionTuple           // Subjective Logic (b, d, u, a)
    provenance:        W3C_PROV_Record        // prov:wasGeneratedBy, prov:wasAttributedTo
    edges:             List<EpistemicEdge>     // typed edges to other quanta
    metabolic_state:   MetabolicState         // active | consolidating | decaying | quarantined | dissolved
    projections:       ProjectionCache        // cached C3, C4, C5 views
    timestamps:        TemporalRecord         // created, last_accessed, last_modified, state_transitions
    dissolution_record: Optional<DissolutionRecord>  // if dissolved: what was recycled, why
    vitality:          VitalityScore          // computed from edges, access patterns, opinion
```

**TypedContent:**

```
TypedContent:
    claim_text:     String          // natural language claim
    claim_type:     ClaimClass      // D|E|S|H|N|P|R|C (from PCVM classification)
    domain_tags:    List<String>    // knowledge domain(s): ["scheduling", "verification"]
    structured_data: Optional<JSON> // machine-parseable structured content
    source_mct_id:  UUID            // MCT that admitted this quantum
    source_vtd_ref: Hash            // reference to VTD in PCVM store
    asv_chain:      ASV_Reference   // reference to ASV CLM-CNF-EVD-PRV-VRF chain
```

**OpinionTuple (Subjective Logic):**

```
OpinionTuple:
    belief:      Float    // [0, 1] — evidence supporting the claim
    disbelief:   Float    // [0, 1] — evidence against the claim
    uncertainty: Float    // [0, 1] — lack of evidence
    base_rate:   Float    // [0, 1] — prior probability absent evidence
    // Constraint: belief + disbelief + uncertainty = 1.0
    // Projected probability: P = belief + base_rate * uncertainty
```

**EpistemicEdge:**

```
EpistemicEdge:
    edge_id:     URI
    source:      URI               // quantum URI
    target:      URI               // quantum URI
    edge_type:   EdgeType          // support | contradiction | derivation | analogy | supersession
    weight:      Float             // [0, 1] — strength of relationship
    created_epoch: Epoch
    last_activated: Epoch          // Hebbian: updated when both quanta accessed in same context
    cross_shard:  Boolean          // true if source and target in different parcel shards
    metadata:     Optional<JSON>   // type-specific metadata
```

**Edge type semantics:**

| Type | Semantics | Weight Dynamics | Vitality Effect |
|------|-----------|----------------|-----------------|
| support | Q_a provides evidence for Q_b | Strengthens when both accessed together | Increases target vitality |
| contradiction | Q_a contradicts Q_b | Strengthens when evidence confirms conflict | Decreases target vitality |
| derivation | Q_b was derived from Q_a | Static weight (derivation is a fact) | Q_b vitality depends on Q_a vitality |
| analogy | Q_a is structurally analogous to Q_b | Strengthens when analogy confirmed useful | Neutral (informational) |
| supersession | Q_b replaces Q_a | Created once, weight = 1.0 | Q_a enters decaying state |

**MetabolicState transitions:**

```
State Machine:
  active --> consolidating   [selected for dreaming input]
  active --> decaying         [vitality below decay_threshold for 10 epochs]
  active --> quarantined      [vitality below catabolism_threshold]
  consolidating --> active    [consolidation complete or timeout]
  decaying --> active         [vitality recovers above decay_threshold]
  decaying --> quarantined    [vitality below catabolism_threshold]
  quarantined --> active      [immune audit rescue]
  quarantined --> dissolved   [quarantine period expires without rescue]
  dissolved --> (terminal)    [dissolution record preserved]

Thresholds:
  decay_threshold:      0.3   (vitality below this for 10 consecutive epochs)
  catabolism_threshold: 0.1   (vitality below this)
  quarantine_period:    100 epochs
```

**Vitality computation:**

```
function compute_vitality(quantum, epoch):
    // Factor 1: Opinion strength (higher belief = higher vitality)
    opinion_factor = quantum.opinion.belief * 0.7 + quantum.opinion.base_rate * 0.3

    // Factor 2: Edge support (net support from connected quanta)
    support_sum = sum(e.weight for e in quantum.edges if e.edge_type == SUPPORT)
    contradiction_sum = sum(e.weight for e in quantum.edges if e.edge_type == CONTRADICTION)

    // Per-agent contradiction cap (RA-3): max 0.3 from any single agent
    agent_contradiction = {}
    for e in quantum.edges:
        if e.edge_type == CONTRADICTION:
            source_agent = get_provenance_agent(e.source)
            agent_contradiction[source_agent] = min(
                agent_contradiction.get(source_agent, 0) + e.weight,
                0.3
            )
    capped_contradiction = sum(agent_contradiction.values())

    support_factor = max(0, support_sum - capped_contradiction) / max(1, support_sum + capped_contradiction)

    // Factor 3: Access recency (Hebbian — recently accessed quanta are more vital)
    epochs_since_access = epoch - quantum.timestamps.last_accessed
    recency_factor = exp(-0.05 * epochs_since_access)  // half-life ~ 14 epochs

    // Factor 4: Temporal validity (if claim has an expiration)
    if quantum.content.temporal_validity_end:
        remaining = quantum.content.temporal_validity_end - epoch
        if remaining <= 0:
            temporal_factor = 0.0  // expired
        else:
            temporal_factor = min(1.0, remaining / 100.0)
    else:
        temporal_factor = 1.0  // no expiration

    // Composite vitality
    vitality = (
        0.30 * opinion_factor +
        0.30 * support_factor +
        0.25 * recency_factor +
        0.15 * temporal_factor
    )

    return clamp(vitality, 0.0, 1.0)
```

**Quantum Store:**

Content-addressed, append-only for dissolved quanta (audit trail). Active quanta are mutable (opinion updates, edge additions, state transitions).

**Indexing:**
- `id` (primary key, URI)
- `content.claim_type` (class-based queries)
- `content.domain_tags` (domain-scoped queries)
- `metabolic_state` (state-based lifecycle queries)
- `vitality` (range queries for catabolism candidates)
- `provenance.agent` (per-agent queries)
- `parcel_shard` (shard-local queries)
- `timestamps.created_epoch` (temporal queries)

---

### 4.2 Ingestion Pipeline

**Purpose:** Receives PCVM-verified claims (MCT + BDL records) and decomposes them into epistemic quanta with initial edge connections.

**Input:** PCVM admission output:
- `claim`: the verified claim (CLM token from ASV)
- `mct`: Membrane Clearance Token (credibility opinion, class, committee, verification method)
- `vtd_ref`: reference to VTD in PCVM store
- `bdl`: Base Durability Ledger bundle

**Output:** One or more epistemic quanta with initial edges, registered in the coherence graph.

**Ingestion Protocol:**

```
function ingest(claim, mct, vtd_ref, bdl):
    // Step 1: Decompose claim into quantum(s)
    // Most claims map 1:1 to quanta. Compound claims are decomposed.
    quanta = decompose_claim(claim, mct)

    for quantum in quanta:
        // Step 2: Map PCVM opinion to quantum opinion
        quantum.opinion = OpinionTuple(
            belief = mct.opinion.belief,
            disbelief = mct.opinion.disbelief,
            uncertainty = mct.opinion.uncertainty,
            base_rate = mct.opinion.base_rate
        )

        // Step 3: Map ASV provenance to W3C PROV
        quantum.provenance = map_asv_to_prov(claim.provenance)

        // Step 4: Set initial metabolic state
        quantum.metabolic_state = ACTIVE
        quantum.timestamps = TemporalRecord(
            created = current_epoch(),
            last_accessed = current_epoch(),
            last_modified = current_epoch(),
            state_transitions = [(current_epoch(), ACTIVE)]
        )

        // Step 5: Store content with MCT/VTD references
        quantum.content = TypedContent(
            claim_text = claim.statement,
            claim_type = mct.assigned_class,
            domain_tags = extract_domains(claim),
            structured_data = claim.structured_content,
            source_mct_id = mct.mct_id,
            source_vtd_ref = vtd_ref,
            asv_chain = claim.id
        )

        // Step 6: Initial vitality from PCVM opinion
        quantum.vitality = compute_vitality(quantum, current_epoch())

        // Step 7: Persist quantum
        quantum_store.save(quantum)

        // Step 8: Detect initial edges
        create_initial_edges(quantum)

        // Step 9: Assign to parcel shard
        shard = assign_shard(quantum, current_parcel_topology())
        shard.register(quantum)

        // Step 10: Generate initial projections
        quantum.projections = ProjectionCache(
            c3 = project_to_c3(quantum),
            c4 = project_to_c4(quantum),
            c5 = project_to_c5(quantum),
            generated_epoch = current_epoch()
        )

    // Step 11: Notify SHREC hunger signal (ingestion occurred)
    shrec.report_ingestion(len(quanta))

    return quanta
```

**ASV-to-Quantum Field Mapping:**

| ASV Field | Quantum Field | Mapping |
|-----------|--------------|---------|
| CLM.statement | content.claim_text | Direct |
| CLM.epistemic_class | content.claim_type | Via PCVM assigned_class (membrane decides) |
| CLM.subject/predicate/object | content.structured_data | Extracted as structured triples |
| CNF.value/interval | opinion.belief | CNF point value -> belief; uncertainty = 1 - confidence |
| CNF.method | opinion (calibration context) | Stored in provenance metadata |
| EVD[] | edges (derivation type) | Each evidence source creates a derivation edge to its source quantum if exists |
| PRV | provenance | Direct mapping to W3C PROV |
| VRF | content.source_mct_id | VRF status captured in MCT reference |

**Initial Edge Detection:**

```
function create_initial_edges(quantum):
    // 1. Derivation edges from evidence references
    for evd in quantum.content.asv_chain.evidence:
        source_quantum = quantum_store.find_by_asv_id(evd.source_id)
        if source_quantum:
            create_edge(source_quantum, quantum, DERIVATION, weight=0.8)

    // 2. Supersession edges from MCT
    if quantum.content.source_mct_id.supersedes:
        superseded = quantum_store.find_by_mct(quantum.content.source_mct_id.supersedes)
        if superseded:
            create_edge(quantum, superseded, SUPERSESSION, weight=1.0)
            superseded.metabolic_state = DECAYING

    // 3. Contradiction detection via semantic similarity + opposite opinion
    candidates = quantum_store.find_similar(
        quantum.content.claim_text,
        domain=quantum.content.domain_tags,
        limit=50
    )
    for candidate in candidates:
        if is_contradictory(quantum, candidate):
            create_edge(quantum, candidate, CONTRADICTION, weight=0.5)
            create_edge(candidate, quantum, CONTRADICTION, weight=0.5)

    // 4. Support detection via semantic similarity + aligned opinion
    for candidate in candidates:
        if is_supporting(quantum, candidate):
            create_edge(quantum, candidate, SUPPORT, weight=0.5)
            create_edge(candidate, quantum, SUPPORT, weight=0.5)
```

**Claim Decomposition:**

```
function decompose_claim(claim, mct):
    // Simple claims: 1 claim -> 1 quantum
    if is_atomic(claim):
        return [create_quantum_from(claim, mct)]

    // Compound claims: decompose into atomic sub-claims
    // Example: "A correlates with B and C causes D" -> 2 quanta
    sub_claims = extract_atomic_claims(claim)
    quanta = []
    for sub in sub_claims:
        q = create_quantum_from(sub, mct)
        quanta.append(q)

    // Create derivation edges between sub-quanta and parent claim reference
    for i, q in enumerate(quanta):
        for j, q2 in enumerate(quanta):
            if i != j:
                create_edge(q, q2, SUPPORT, weight=0.6)  // sibling support

    return quanta
```

---

### 4.3 Coherence Graph

**Purpose:** Maintains the typed edge network connecting epistemic quanta. Provides graph operations for circulation, consolidation candidate selection, vitality computation, and contradiction detection.

**Architecture:**

```
+------------------------------------------------------------------+
|                      COHERENCE GRAPH                              |
|                                                                   |
|  +------------------+  +------------------+  +----------------+   |
|  | Shard Manager    |  | Edge Registry    |  | Cross-Shard    |   |
|  | (parcel-aligned  |  | (active edges,   |  | Index          |   |
|  |  shard topology, |  |  archived edges, |  | (sampled cross |   |
|  |  shard routing)  |  |  budget enforce) |  |  -parcel refs) |   |
|  +--------+---------+  +--------+---------+  +-------+--------+   |
|           |                     |                     |            |
|  +--------v---------------------v---------------------v--------+  |
|  |                    Graph Operations                          |  |
|  |  - edge_weight_update (Hebbian + temporal decay)             |  |
|  |  - vitality_batch_compute (per shard, per epoch)             |  |
|  |  - contradiction_scan (new ingestions vs existing)            |  |
|  |  - bridge_detection (cross-domain edges for dreaming)        |  |
|  |  - neighborhood_query (local subgraph extraction)            |  |
|  |  - coherence_density (local coherence metric)                |  |
|  +-------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

**Shard Manager:**

```
function assign_shard(quantum, parcel_topology):
    // Primary assignment: hash of quantum's primary domain to parcel
    primary_domain = quantum.content.domain_tags[0]
    parcel = parcel_topology.assign(primary_domain)
    shard_id = "shard:" + parcel.id

    // Register quantum in shard
    shards[shard_id].add(quantum.id)
    quantum.parcel_shard = shard_id

    return shards[shard_id]

function rebalance_on_parcel_change(old_topology, new_topology):
    // Aligned with C3 PTP (Parcel Transition Protocol)
    // Phase 1: PREPARE — identify quanta that need to move
    migrations = []
    for quantum in quantum_store.active():
        old_shard = assign_shard(quantum, old_topology)
        new_shard = assign_shard(quantum, new_topology)
        if old_shard != new_shard:
            migrations.append((quantum, old_shard, new_shard))

    // Phase 2: SWITCH — migrate quanta atomically at epoch boundary
    for (quantum, old_shard, new_shard) in migrations:
        old_shard.remove(quantum.id)
        new_shard.add(quantum.id)
        quantum.parcel_shard = new_shard.id
        // Cross-shard edges may become intra-shard or vice versa
        update_edge_cross_shard_flags(quantum)

    // Phase 3: STABILIZE — recompute cross-shard index
    rebuild_cross_shard_index()
```

**Edge Weight Dynamics (Hebbian + Temporal Decay):**

```
function update_edge_weights(shard, epoch):
    for edge in shard.active_edges():
        // Temporal decay: all edges weaken over time
        epochs_since_activation = epoch - edge.last_activated
        decay = exp(-0.02 * epochs_since_activation)  // half-life ~ 35 epochs
        edge.weight *= decay

        // Hebbian strengthening: co-accessed quanta strengthen their edges
        source_accessed = (quantum_store.get(edge.source).timestamps.last_accessed == epoch)
        target_accessed = (quantum_store.get(edge.target).timestamps.last_accessed == epoch)
        if source_accessed and target_accessed:
            edge.weight = min(1.0, edge.weight + 0.05)  // strengthen
            edge.last_activated = epoch

        // Prune dead edges
        if edge.weight < 0.01:
            shard.archive_edge(edge)
```

**Cross-Shard Index:**

At Tier 2+, cross-shard edges are maintained in a lightweight index:

```
CrossShardIndex:
    entries: List<CrossShardEntry>

CrossShardEntry:
    source_shard: ShardID
    target_shard: ShardID
    source_quantum: URI
    target_quantum: URI
    edge_type: EdgeType
    weight: Float
    last_sampled: Epoch      // when this entry was last verified

// Cross-shard coherence sampling (Tier 2):
function sample_cross_shard_coherence(shard_a, shard_b, sample_rate=0.10):
    cross_edges = cross_shard_index.get(shard_a, shard_b)
    sample = random_sample(cross_edges, rate=sample_rate)

    coherence_scores = []
    for entry in sample:
        q_source = quantum_store.get(entry.source_quantum)
        q_target = quantum_store.get(entry.target_quantum)
        score = compute_pairwise_coherence(q_source, q_target)
        coherence_scores.append(score)
        entry.last_sampled = current_epoch()

    return mean(coherence_scores) if coherence_scores else 0.5
```

**Bridge Detection (for Dreaming Candidate Selection):**

```
function detect_cross_domain_bridges(shard):
    bridges = []
    for quantum in shard.quanta():
        domains = set(quantum.content.domain_tags)
        for edge in quantum.active_edges:
            target = quantum_store.get(edge.target)
            target_domains = set(target.content.domain_tags)
            if domains != target_domains and len(domains & target_domains) == 0:
                // Edge connects quanta from completely different domains
                bridges.append(BridgeCandidate(
                    quantum_a = quantum,
                    quantum_b = target,
                    edge = edge,
                    domain_pair = (domains, target_domains),
                    bridge_strength = edge.weight
                ))

    // Rank by bridge strength and diversity
    bridges.sort(by=lambda b: b.bridge_strength, reverse=True)
    return bridges
```

---

### 4.4 Circulation Engine

**Purpose:** Pushes relevant quanta to subscribing agents based on subscription profiles and metabolic signals. Implements both push-based (proactive delivery) and pull-based (query response) knowledge flow.

**Architecture:**

```
+------------------------------------------------------------------+
|                    CIRCULATION ENGINE                              |
|                                                                   |
|  +------------------+  +------------------+  +----------------+   |
|  | Subscription     |  | Relevance        |  | Flow           |   |
|  | Registry         |  | Ranker           |  | Controller     |   |
|  | (per-agent       |  | (domain match,   |  | (rate limits,  |   |
|  |  topic prefs,    |  |  opinion weight,  |  |  priority      |   |
|  |  domain filters) |  |  recency boost)  |  |  queuing)      |   |
|  +--------+---------+  +--------+---------+  +-------+--------+   |
|           |                     |                     |            |
|  +--------v---------------------v---------------------v--------+  |
|  |              Notification Dispatcher                         |  |
|  |  - epoch_batch: deliver accumulated notifications at epoch   |  |
|  |  - priority_push: immediate for contradiction/supersession   |  |
|  |  - digest_mode: summary for low-priority subscriptions       |  |
|  +-------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

**Subscription Model:**

```
Subscription:
    agent_id:        AgentID
    domain_filter:   List<String>      // domains of interest
    claim_types:     List<ClaimClass>   // claim types of interest
    min_vitality:    Float              // minimum vitality threshold
    min_belief:      Float              // minimum opinion.belief threshold
    notification_mode: BATCH | PRIORITY | DIGEST
    max_per_epoch:   Int                // rate limit per epoch
    parcel_scope:    Optional<ParcelID> // limit to specific parcel
```

**Circulation Protocol (per epoch):**

```
function circulate(epoch):
    // Step 1: Collect circulation candidates
    // New quanta ingested this epoch + quanta with significant state changes
    candidates = []
    candidates += quantum_store.ingested_this_epoch()
    candidates += quantum_store.state_changed_this_epoch()
    candidates += quantum_store.opinion_changed_this_epoch(delta_threshold=0.1)

    // Step 2: For each candidate, find matching subscriptions
    for quantum in candidates:
        matching_subs = subscription_registry.match(
            domains = quantum.content.domain_tags,
            claim_type = quantum.content.claim_type,
            vitality = quantum.vitality,
            belief = quantum.opinion.belief
        )

        for sub in matching_subs:
            // Step 3: Compute relevance score
            relevance = relevance_ranker.score(quantum, sub)

            // Step 4: Queue notification
            if relevance > 0.3:  // minimum relevance threshold
                notification = Notification(
                    quantum_id = quantum.id,
                    quantum_summary = summarize(quantum),
                    relevance_score = relevance,
                    change_type = classify_change(quantum),  // NEW | UPDATED | CONTRADICTED | SUPERSEDED
                    epoch = epoch
                )

                // Priority routing for critical changes
                if quantum.edges_contain(CONTRADICTION) or quantum.edges_contain(SUPERSESSION):
                    flow_controller.priority_push(sub.agent_id, notification)
                else:
                    flow_controller.batch_queue(sub.agent_id, notification)

    // Step 5: Deliver batched notifications
    flow_controller.deliver_epoch_batch(epoch)

    // Step 6: Report to SHREC
    shrec.report_circulation(len(candidates), total_notifications_sent)
```

**Relevance Ranking:**

```
function score_relevance(quantum, subscription):
    // Domain match (0 or 1, with partial credit for related domains)
    domain_score = domain_similarity(quantum.content.domain_tags, subscription.domain_filter)

    // Opinion strength (higher belief = more relevant)
    opinion_score = quantum.opinion.belief

    // Recency (recently created/modified quanta are more relevant)
    recency_score = exp(-0.03 * (current_epoch() - quantum.timestamps.last_modified))

    // Vitality (healthier quanta are more relevant)
    vitality_score = quantum.vitality

    // Novelty (quanta the agent hasn't seen before are more relevant)
    seen_before = notification_log.has_seen(subscription.agent_id, quantum.id)
    novelty_score = 0.0 if seen_before else 1.0

    relevance = (
        0.30 * domain_score +
        0.20 * opinion_score +
        0.15 * recency_score +
        0.15 * vitality_score +
        0.20 * novelty_score
    )

    return relevance
```

**Flow Control:**

```
function deliver_epoch_batch(epoch):
    for agent_id in batch_queue.agents():
        notifications = batch_queue.get(agent_id)
        sub = subscription_registry.get(agent_id)

        // Rate limiting
        if len(notifications) > sub.max_per_epoch:
            // Rank by relevance, deliver top N
            notifications.sort(by=relevance_score, reverse=True)
            notifications = notifications[:sub.max_per_epoch]

        // Digest mode: collapse similar notifications
        if sub.notification_mode == DIGEST:
            notifications = collapse_to_digest(notifications)

        // Deliver
        deliver_to_agent(agent_id, notifications, epoch)
```

---

### 4.5 Consolidation Engine (Dreaming Pipeline)

**Purpose:** Discovers cross-domain patterns through scheduled LLM reasoning, produces C-class claims, and submits them to PCVM for verification before integration into the knowledge base. This is EMA's most novel and highest-risk component.

**Architecture:**

```
+------------------------------------------------------------------+
|                   CONSOLIDATION ENGINE                            |
|                                                                   |
|  +------------------+  +------------------+  +----------------+   |
|  | Candidate        |  | Synthesis        |  | Verification   |   |
|  | Selector         |  | Pipeline         |  | Gate           |   |
|  | (bridge detect,  |  | (3-pass LLM,    |  | (C-class claim |   |
|  |  diversity check,|  |  majority vote,  |  |  construction, |   |
|  |  consolidation   |  |  provenance      |  |  PCVM submit,  |   |
|  |  lock)           |  |  assembly)       |  |  result apply) |   |
|  +--------+---------+  +--------+---------+  +-------+--------+   |
|           |                     |                     |            |
|           v                     v                     v            |
|  Bridge candidates -----> LLM synthesis ------> PCVM C-class      |
|  (diverse, locked)        (3-pass + vote)        verification     |
+------------------------------------------------------------------+
```

**Dreaming Schedule:**

Consolidation runs once per N epochs (configurable, default N=10). The consolidation window occupies the consolidation phase of the epoch processing order, after circulation and before catabolism.

**Candidate Selection:**

```
function select_consolidation_candidates(shard, epoch):
    // Step 1: Detect cross-domain bridges
    bridges = coherence_graph.detect_cross_domain_bridges(shard)

    // Step 2: Filter by minimum bridge criteria
    viable_bridges = []
    for bridge in bridges:
        if bridge.bridge_strength >= 0.3:           // minimum edge weight
            if bridge.quantum_a.vitality >= 0.4:     // both quanta reasonably vital
                if bridge.quantum_b.vitality >= 0.4:
                    viable_bridges.append(bridge)

    // Step 3: Expand bridge neighborhoods
    candidate_sets = []
    for bridge in viable_bridges[:10]:  // top 10 bridges per dreaming cycle
        neighborhood = coherence_graph.neighborhood(
            centers = [bridge.quantum_a.id, bridge.quantum_b.id],
            radius = 2,              // 2-hop neighborhood
            max_quanta = 30          // cap neighborhood size
        )
        candidate_sets.append(CandidateSet(
            bridge = bridge,
            quanta = neighborhood,
            domains = extract_all_domains(neighborhood)
        ))

    // Step 4: Provenance diversity validation (HG-3)
    diverse_sets = []
    for cs in candidate_sets:
        result = validate_consolidation_inputs(cs.quanta)
        if result == ACCEPT:
            diverse_sets.append(cs)
        else:
            log_diversity_rejection(cs, result)

    // Step 5: Apply consolidation locks
    for cs in diverse_sets:
        for q in cs.quanta:
            q.metabolic_state = CONSOLIDATING
            // Consolidation lock prevents catabolism during dreaming

    return diverse_sets
```

**3-Pass LLM Synthesis:**

```
function synthesize(candidate_set):
    // Prepare context: serialize quanta into structured prompt
    context = prepare_dreaming_context(candidate_set)

    // Pass 1: Discovery (creative, higher temperature)
    prompt_1 = DREAMING_PROMPT_DISCOVER.format(
        quanta = context,
        domains = candidate_set.domains,
        instruction = "Identify structural correspondences, causal patterns, "
                      "or general principles that connect these knowledge claims "
                      "across domains. Be specific. Cite source quanta by ID."
    )
    result_1 = llm_call(prompt_1, temperature=0.7, max_tokens=2000)

    // Pass 2: Independent discovery (different prompt framing)
    prompt_2 = DREAMING_PROMPT_INDEPENDENT.format(
        quanta = context,
        domains = candidate_set.domains,
        instruction = "Without regard to any previous analysis, identify "
                      "cross-domain patterns in these claims. For each pattern, "
                      "state: the pattern, which claims support it, and what "
                      "would falsify it."
    )
    result_2 = llm_call(prompt_2, temperature=0.7, max_tokens=2000)

    // Pass 3: Critical evaluation (lower temperature, evaluative)
    prompt_3 = DREAMING_PROMPT_EVALUATE.format(
        analysis_1 = result_1,
        analysis_2 = result_2,
        quanta = context,
        instruction = "Evaluate these two independent analyses. For each "
                      "proposed pattern: (1) Is it genuinely supported by "
                      "the source claims? (2) Is it a novel insight or a "
                      "trivial observation? (3) Could it be a spurious "
                      "correlation or cultural common-sense? (4) What is "
                      "the falsification condition? Accept only patterns "
                      "that both analyses identify and that pass your "
                      "critical evaluation."
    )
    result_3 = llm_call(prompt_3, temperature=0.3, max_tokens=2000)

    // Majority vote: extract patterns confirmed by >= 2 of 3 passes
    patterns = extract_confirmed_patterns(result_1, result_2, result_3)

    return patterns
```

**C-Class Claim Construction:**

```
function construct_c_class_claims(patterns, candidate_set):
    claims = []
    for pattern in patterns:
        // Build ASV CLM-CNF-EVD-PRV-VRF chain
        claim = ASV_CLM(
            id = generate_uri("clm", "consolidated"),
            claim_type = "INFORM",
            epistemic_class = "consolidated_principle",
            statement = pattern.description,
            valid_from = current_timestamp(),
            valid_until = current_timestamp() + 500 * epoch_length,  // 500-epoch validity

            confidence = ASV_CNF(
                representation = "point",
                value = 0.5,           // C-class starts at 0.5 (high uncertainty)
                method = "model_derived",
                calibration = {
                    calibrated = false,
                    warning = "Consolidated by dreaming process. "
                              "Requires independent confirmation."
                }
            ),

            evidence = [
                ASV_EVD(
                    quality_class = "inference",
                    source_id = q.id,
                    description = "Source quantum for consolidation"
                ) for q in pattern.source_quanta
            ],

            provenance = ASV_PRV(
                wasGeneratedBy = {
                    activity_type = "dreaming_consolidation",
                    started_at = consolidation_start_time,
                    ended_at = now()
                },
                wasAttributedTo = "urn:ema:consolidation-engine",
                used = [q.id for q in pattern.source_quanta]
            )
        )

        // Attach falsification condition
        claim.falsification = pattern.falsification_condition

        claims.append(claim)

    return claims
```

**PCVM Verification Gate:**

```
function submit_to_pcvm(c_class_claims, candidate_set):
    results = []
    for claim in c_class_claims:
        // Submit as C-class claim to PCVM
        outcome = pcvm.submit_for_verification(
            claim = claim,
            proposed_class = "C",       // Consolidation class
            evidence_bundle = {
                source_quanta = candidate_set.quanta,
                synthesis_trace = claim.synthesis_log,
                falsification = claim.falsification,
                diversity_report = candidate_set.diversity_report
            }
        )

        if outcome.admitted:
            // PCVM issued MCT — ingest the consolidated quantum
            new_quantum = ingest(
                claim = outcome.claim,
                mct = outcome.mct,
                vtd_ref = outcome.vtd_ref,
                bdl = outcome.bdl
            )

            // Create derivation edges from source quanta to consolidated quantum
            for source_q in candidate_set.quanta:
                create_edge(source_q, new_quantum[0], DERIVATION, weight=0.7)

            results.append(ConsolidationResult(
                pattern = claim.statement,
                quantum = new_quantum[0],
                status = ACCEPTED
            ))
        else:
            results.append(ConsolidationResult(
                pattern = claim.statement,
                quantum = null,
                status = REJECTED,
                reason = outcome.rejection_reason
            ))

    return results
```

**Consolidation Lock Release:**

```
function release_consolidation_locks(candidate_set):
    for q in candidate_set.quanta:
        if q.metabolic_state == CONSOLIDATING:
            q.metabolic_state = ACTIVE
            q.timestamps.last_modified = current_epoch()
```

**Aging Uncertainty (RA-5):**

```
function apply_aging_uncertainty(epoch):
    // C-class quanta active for >50 epochs without confirmation/disconfirmation
    for q in quantum_store.query(claim_type="C", metabolic_state=ACTIVE):
        epochs_active = epoch - q.timestamps.created
        if epochs_active > 50:
            // Check for confirming/disconfirming evidence
            evidence_edges = [e for e in q.edges
                              if e.edge_type in (SUPPORT, CONTRADICTION)
                              and e.created_epoch > q.timestamps.created]
            if len(evidence_edges) == 0:
                // No evidence in 50+ epochs — increase uncertainty
                periods = (epochs_active - 50) // 50  // number of 50-epoch periods
                uncertainty_increase = 0.1 * periods
                q.opinion.uncertainty = min(0.9, q.opinion.uncertainty + uncertainty_increase)
                q.opinion.belief = max(0.05, q.opinion.belief - uncertainty_increase * 0.5)
                q.opinion.disbelief = max(0.05, 1.0 - q.opinion.belief - q.opinion.uncertainty)
                log_aging_update(q, uncertainty_increase)
```

---

### 4.6 Catabolism Engine

**Purpose:** Controlled dissolution of quanta that have lost relevance, credibility, or coherence. Components are recycled (provenance preserved, evidence redistributed) or eliminated. Catabolism prevents unbounded knowledge growth and removes stale/incorrect information.

**Catabolism Criteria:**

A quantum becomes a catabolism candidate when ANY of the following conditions hold:

| Criterion | Threshold | Detection |
|-----------|-----------|-----------|
| Low vitality | vitality < 0.1 for any single epoch | Vitality batch computation |
| Sustained decay | vitality < 0.3 for 10 consecutive epochs | Decay state tracker |
| Expired temporal validity | valid_until < current_epoch | Temporal validity check |
| Low credibility | opinion.belief < 0.15 AND opinion.uncertainty < 0.3 | Opinion threshold check |
| High contradiction density | contradiction_edges / total_edges > 0.7 | Edge ratio computation |
| Superseded | supersession edge exists with weight = 1.0 | Edge type check |

**Catabolism Pipeline:**

```
function run_catabolism(epoch):
    // Step 1: Identify candidates
    candidates = []
    for shard in coherence_graph.shards():
        for quantum in shard.quanta():
            if quantum.metabolic_state == CONSOLIDATING:
                continue  // consolidation lock — skip

            if should_catabolize(quantum, epoch):
                candidates.append(quantum)

    // Step 2: Quarantine (not immediate dissolution)
    for quantum in candidates:
        if quantum.metabolic_state != QUARANTINED:
            quarantine(quantum, epoch)
        else:
            // Already quarantined — check if quarantine period expired
            quarantine_start = quantum.timestamps.state_transitions[-1][0]
            if epoch - quarantine_start > QUARANTINE_PERIOD:
                dissolve(quantum, epoch)

    // Step 3: Report to SHREC
    shrec.report_catabolism(
        quarantined_count = len([c for c in candidates if c.metabolic_state == QUARANTINED]),
        dissolved_count = len([c for c in candidates if c.metabolic_state == DISSOLVED])
    )
```

**Quarantine:**

```
function quarantine(quantum, epoch):
    // Preserve full snapshot for potential rescue
    quantum.quarantine_snapshot = deep_copy(quantum)
    quantum.metabolic_state = QUARANTINED
    quantum.timestamps.state_transitions.append((epoch, QUARANTINED))

    // Soft-remove from active circulation (still in graph, edges preserved)
    circulation_engine.remove_from_circulation(quantum)

    // Notify Sentinel Graph
    sentinel.report_quarantine(quantum)

    log_quarantine(quantum, epoch, reason=get_catabolism_reason(quantum))
```

**Dissolution (Component Recycling):**

```
function dissolve(quantum, epoch):
    // Step 1: Create dissolution record (permanent audit trail)
    dissolution = DissolutionRecord(
        quantum_id = quantum.id,
        dissolved_epoch = epoch,
        reason = get_catabolism_reason(quantum),
        final_vitality = quantum.vitality,
        final_opinion = quantum.opinion,
        provenance_preserved = quantum.provenance,
        edge_snapshot = [(e.target, e.edge_type, e.weight) for e in quantum.edges],
        content_hash = hash(quantum.content)  // content preserved as hash only
    )

    // Step 2: Redistribute evidence to surviving dependent quanta
    for edge in quantum.edges:
        if edge.edge_type == DERIVATION and edge.source == quantum.id:
            // This quantum was derived from another — no action needed
            pass
        elif edge.edge_type == DERIVATION and edge.target == quantum.id:
            // Another quantum derives from this one
            dependent = quantum_store.get(edge.source)
            if dependent and dependent.metabolic_state == ACTIVE:
                // Weaken the derivation (source dissolved)
                dependent_edge = dependent.find_edge(quantum.id, DERIVATION)
                if dependent_edge:
                    dependent_edge.weight *= 0.5  // weaken, don't remove
                    // Add note to dependent's provenance
                    dependent.provenance.add_note(
                        "Source quantum " + quantum.id + " dissolved at epoch " + epoch
                    )
                    // Trigger re-verification if dependent's vitality drops below threshold
                    if compute_vitality(dependent, epoch) < 0.3:
                        trigger_reverification(dependent)

    // Step 3: Remove from coherence graph
    coherence_graph.remove_quantum(quantum)

    // Step 4: Update quantum state
    quantum.metabolic_state = DISSOLVED
    quantum.dissolution_record = dissolution
    quantum.timestamps.state_transitions.append((epoch, DISSOLVED))

    // Step 5: Move to archive (dissolved quanta are never fully deleted)
    quantum_store.archive(quantum)
```

**Quarantine Rescue (Immune Audit):**

```
function immune_audit_rescue(epoch):
    // Sample 10% of quarantined quanta
    quarantined = quantum_store.query(metabolic_state=QUARANTINED)
    sample = random_sample(quarantined, rate=0.10)

    rescued = 0
    false_positives = 0

    for quantum in sample:
        // Check if quantum has active support edges from non-quarantined quanta
        active_support = [e for e in quantum.edges
                         if e.edge_type == SUPPORT
                         and quantum_store.get(e.target).metabolic_state == ACTIVE
                         and e.weight > 0.3]

        if len(active_support) >= 2:
            // Quantum has legitimate support — likely false positive catabolism
            quantum.metabolic_state = ACTIVE
            quantum.timestamps.state_transitions.append((epoch, ACTIVE))
            circulation_engine.add_to_circulation(quantum)
            rescued += 1
            false_positives += 1

    // Autoimmune detection
    if false_positives / max(1, len(sample)) > 0.15:
        // Too many false positives — catabolism is over-aggressive
        // Raise catabolism threshold
        adjust_catabolism_threshold(direction=UP, magnitude=0.05)
        sentinel.report_autoimmune_alarm(false_positive_rate=false_positives/len(sample))

    // Under-detection check
    // Sample 10% of recently dissolved quanta
    recently_dissolved = quantum_store.query(
        metabolic_state=DISSOLVED,
        dissolved_after=epoch-50
    )
    dissolved_sample = random_sample(recently_dissolved, rate=0.10)
    missed_threats = 0
    for quantum in dissolved_sample:
        if quantum.dissolution_record.final_opinion.belief > 0.5:
            // High-belief quantum was dissolved — possible false negative
            missed_threats += 1

    if missed_threats / max(1, len(dissolved_sample)) > 0.05:
        // Too many high-belief quanta dissolved — catabolism may be weaponized
        adjust_catabolism_threshold(direction=UP, magnitude=0.10)
        sentinel.report_catabolism_weaponization_alert()
```

**Quarantine Budget (A9 defense):**

```
QUARANTINE_STORAGE_LIMIT = 0.30  // max 30% of active storage

function enforce_quarantine_budget():
    quarantine_size = quantum_store.quarantine_storage_bytes()
    active_size = quantum_store.active_storage_bytes()

    if quarantine_size > QUARANTINE_STORAGE_LIMIT * active_size:
        // Over budget — force-dissolve oldest quarantined quanta
        oldest = quantum_store.query(
            metabolic_state=QUARANTINED,
            order_by=quarantine_start_epoch,
            ascending=True
        )
        while quarantine_size > QUARANTINE_STORAGE_LIMIT * active_size:
            q = oldest.pop(0)
            dissolve(q, current_epoch())
            quarantine_size -= sizeof(q)

    // Oscillation detection: quanta quarantined/rescued > 3 times
    oscillators = quantum_store.query(
        quarantine_count > 3
    )
    for q in oscillators:
        q.quarantine_snapshot = None  // reduce snapshot to hash only
        q.quarantine_snapshot_hash = hash(q)
```

---

### 4.7 SHREC Controller

**Purpose:** The Self-regulating Homeostatic Resource Ecology Controller manages computational budget allocation across the 5 metabolic processes through ecological competition with PID safety overlay. SHREC is EMA's regulatory nervous system.

**5 SHREC Signals:**

| Signal | What It Measures | How It's Measured | Floor |
|--------|-----------------|-------------------|-------|
| Hunger (H) | Unprocessed ingestion backlog | pending_mcts / ingestion_capacity | 0% |
| Consolidation (C) | Cross-domain bridge density | viable_bridges / min_bridge_threshold | 0% |
| Stress (S) | Coherence graph degradation | stale_edges / total_edges + contradiction_ratio | 10% |
| Immune (I) | Quarantine population + anomaly density | quarantined / active + sentinel_alerts | 15% |
| Novelty (N) | Novel domain coverage gaps | unexplored_domains / total_domains | 8% |

**Signal Measurement:**

```
function measure_signals(epoch):
    signals = {}

    // Hunger: how much unprocessed knowledge is waiting
    pending = ingestion_pipeline.pending_count()
    capacity = ingestion_pipeline.epoch_capacity()
    signals['hunger'] = min(1.0, pending / max(1, capacity))

    // Consolidation: how many cross-domain opportunities exist
    bridges = coherence_graph.count_viable_bridges()
    min_bridges = config.min_bridge_threshold  // default: 5
    signals['consolidation'] = min(1.0, bridges / max(1, min_bridges * 3))

    // Stress: coherence graph health
    stale_ratio = coherence_graph.stale_edge_ratio(staleness_threshold=50)
    contradiction_ratio = coherence_graph.global_contradiction_ratio()
    signals['stress'] = min(1.0, stale_ratio * 0.6 + contradiction_ratio * 0.4)

    // Immune: quarantine and anomaly load
    quarantine_ratio = quantum_store.quarantine_ratio()
    anomaly_count = sentinel.recent_anomaly_count(window=10)
    anomaly_norm = min(1.0, anomaly_count / 10.0)
    signals['immune'] = min(1.0, quarantine_ratio * 0.5 + anomaly_norm * 0.5)

    // Novelty: coverage of knowledge frontier
    explored = coherence_graph.domain_coverage()
    total = domain_registry.total_domains()
    signals['novelty'] = 1.0 - min(1.0, explored / max(1, total))

    return signals
```

**Ecological Budget Computation (Lotka-Volterra):**

```
function compute_ecological_budget(signals, dt=0.1):
    // Current population levels
    S = [signals['hunger'], signals['consolidation'], signals['stress'],
         signals['immune'], signals['novelty']]

    // Carrying capacities (per resource dimension)
    K = [config.K_hunger, config.K_consolidation, config.K_stress,
         config.K_immune, config.K_novelty]
    // Default: all 1.0 (normalized)

    // Intrinsic growth rates (proportional to signal intensity)
    r = [s * config.r_base for s in S]  // r_base default: 0.5

    // Alpha matrix (competitive coefficients)
    alpha = config.alpha_matrix  // 5x5 matrix as defined in HG-1

    // Euler integration step
    dS = []
    for i in range(5):
        competition = sum(alpha[i][j] * S[j] for j in range(5))
        dS_i = r[i] * S[i] * (1 - (S[i] + competition) / K[i])
        dS.append(dS_i)

    // Update
    S_new = [max(0.01, S[i] + dS[i] * dt) for i in range(5)]

    // Normalize to budget fractions
    total = sum(S_new)
    budget = {
        'hunger':        S_new[0] / total,
        'consolidation': S_new[1] / total,
        'stress':        S_new[2] / total,
        'immune':        S_new[3] / total,
        'novelty':       S_new[4] / total
    }

    // Enforce floors
    budget = enforce_floors(budget)

    return budget
```

**PID Overlay:**

```
function apply_pid_overlay(budget, signals, epoch):
    // Step 1: Regime detection
    regime = detect_regime(signals, epoch)

    if regime == NORMAL:
        return budget  // ecology only, no PID

    // Step 2: Compute PID corrections
    corrections = {}
    for signal_name, signal_value in signals.items():
        setpoint = config.setpoints[signal_name]  // target signal level
        error = setpoint - signal_value

        // Sigma-derived gains
        sigma = signal_history.std(signal_name, window=100)
        sigma = max(sigma, 0.01)  // prevent division by zero
        Kp = 1.0 / sigma
        Ki = Kp / (4 * 100)      // W = 100 epochs
        Kd = Kp * (100 / 10)

        // Gain multiplier based on regime
        gain_mult = 0.5 if regime == ELEVATED else 1.0

        // PID terms
        P = Kp * error * gain_mult
        I = Ki * integral_accumulator[signal_name] * gain_mult
        D = Kd * (error - previous_error[signal_name]) * gain_mult

        // Anti-windup
        integral_accumulator[signal_name] += error
        integral_accumulator[signal_name] = clamp(
            integral_accumulator[signal_name],
            -2.0 * sigma, 2.0 * sigma
        )

        corrections[signal_name] = P + I + D
        previous_error[signal_name] = error

    // Step 3: Apply corrections to ecological budget
    if regime == CONSTITUTIONAL:
        // Direct setpoint control — override ecology
        budget = {name: config.setpoints[name] for name in budget}
    else:
        // Blend corrections with ecological budget
        for name in budget:
            budget[name] = max(0.01, budget[name] + corrections[name] * 0.3)

    // Re-normalize and enforce floors
    total = sum(budget.values())
    budget = {k: v/total for k, v in budget.items()}
    budget = enforce_floors(budget)

    // Reset integral on regime downgrade
    if regime_just_downgraded():
        for name in integral_accumulator:
            integral_accumulator[name] = 0

    return budget

function detect_regime(signals, epoch):
    for signal_name, signal_value in signals.items():
        mean = signal_history.mean(signal_name, window=100)
        sigma = signal_history.std(signal_name, window=100)
        sigma = max(sigma, 0.01)

        deviation = abs(signal_value - mean) / sigma

        if deviation > 2.5:
            // Check constitutional threat
            if is_constitutional_threat(signal_name, signal_value):
                return CONSTITUTIONAL
            return CRITICAL

        if deviation > 1.5:
            return ELEVATED  // but continue checking other signals

    return NORMAL
```

**Immune Self-Audit Schedule:**

```
function weekly_immune_audit():
    // Run every 168 epochs (assuming 1-hour epochs = 1 week)
    // Or every config.immune_audit_interval epochs

    // Measure false positive rate (catabolism of valid quanta)
    fp_rate = immune_audit_rescue(current_epoch())  // from catabolism engine

    // Measure false negative rate (survival of invalid quanta)
    // Sample active quanta and check for staleness/incoherence
    active_sample = random_sample(quantum_store.query(metabolic_state=ACTIVE), rate=0.05)
    fn_count = 0
    for q in active_sample:
        if should_catabolize(q, current_epoch()):
            fn_count += 1
    fn_rate = fn_count / max(1, len(active_sample))

    // Adjust sensitivity
    if fp_rate > 0.15:
        // Too many false positives — reduce catabolism sensitivity
        config.catabolism_threshold *= 0.95  // lower threshold = less aggressive
        log_immune_adjustment("sensitivity_reduced", fp_rate)

    if fn_rate > 0.05:
        // Too many false negatives — increase catabolism sensitivity
        config.catabolism_threshold *= 1.05  // raise threshold = more aggressive
        log_immune_adjustment("sensitivity_increased", fn_rate)
```

**SHREC Budget Application:**

```
function apply_budget(budget, epoch):
    // Translate budget fractions into concrete resource allocations
    total_cpu = system.available_cpu_cycles(epoch)
    total_memory = system.available_memory_bandwidth(epoch)
    total_llm = system.available_llm_tokens(epoch)
    total_io = system.available_io_ops(epoch)
    total_graph = system.available_graph_traversals(epoch)

    allocations = {
        'ingestion':     ResourceAllocation(
            cpu = total_cpu * budget['hunger'] * 0.3,
            io = total_io * budget['hunger'] * 0.7,
            graph = 0
        ),
        'consolidation': ResourceAllocation(
            cpu = total_cpu * budget['consolidation'] * 0.2,
            llm = total_llm * budget['consolidation'] * 0.8,
            graph = total_graph * budget['consolidation'] * 0.3
        ),
        'coherence':     ResourceAllocation(
            cpu = total_cpu * budget['stress'] * 0.6,
            graph = total_graph * budget['stress'] * 0.4
        ),
        'immune':        ResourceAllocation(
            cpu = total_cpu * budget['immune'] * 0.3,
            memory = total_memory * budget['immune'] * 0.7
        ),
        'exploration':   ResourceAllocation(
            graph = total_graph * budget['novelty'] * 0.6,
            cpu = total_cpu * budget['novelty'] * 0.4
        )
    }

    return allocations
```

---

### 4.8 Projection Engine

**Purpose:** Translates epistemic quanta into native views for C3 (Tidal Noosphere), C4 (ASV), and C5 (PCVM) with bounded, measured information loss. Projections are cached views — the canonical quantum remains the source of truth.

**Architecture:**

```
+------------------------------------------------------------------+
|                    PROJECTION ENGINE                              |
|                                                                   |
|  +------------------+  +------------------+  +----------------+   |
|  | C3 Projector     |  | C4 Projector     |  | C5 Projector   |   |
|  | (coordination    |  | (semantic        |  | (verification  |   |
|  |  view: locus,    |  |  view: CLM-CNF-  |  |  view: VTD,    |   |
|  |  epoch, parcel,  |  |  EVD-PRV-VRF     |  |  credibility,  |   |
|  |  relevance)      |  |  chain)          |  |  MCT ref)      |   |
|  +--------+---------+  +--------+---------+  +-------+--------+   |
|           |                     |                     |            |
|  +--------v---------------------v---------------------v--------+  |
|  |              Fidelity Monitor                                |  |
|  |  - round-trip fidelity measurement per projection type       |  |
|  |  - confidence warning flag for high-canonical-confidence     |  |
|  |  - cache staleness tracking                                  |  |
|  +-------------------------------------------------------------+  |
|  |              Cache Manager                                   |  |
|  |  - epoch-boundary refresh (default)                          |  |
|  |  - event-driven refresh (for safety-critical quanta)         |  |
|  |  - consistency guarantees (eventual / epoch / strong)        |  |
|  +-------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

**C3 Projection (Coordination View):**

Fidelity target: 0.85

Preserves: locus assignment, epoch timing, parcel membership, coordination state, relevance score
Loses: full provenance chain detail, dissolution records, SHREC signal associations, full edge graph

```
C3Projection:
    quantum_id:         URI
    locus:              LocusID
    parcel:             ParcelID
    relevance_score:    Float          // computed from vitality + domain match to parcel
    coordination_state: String         // "active" | "decaying" | "quarantined"
    epoch_created:      Epoch
    epoch_last_active:  Epoch
    domain_tags:        List<String>
    claim_summary:      String         // truncated claim_text (max 200 chars)
    opinion_projected:  Float          // projected probability only (not full tuple)
    edge_summary:       EdgeSummary    // support_count, contradiction_count, total
    high_canonical_confidence: Boolean // true if canonical opinion.belief > 0.8

function project_to_c3(quantum):
    return C3Projection(
        quantum_id = quantum.id,
        locus = resolve_locus(quantum.content.domain_tags),
        parcel = quantum.parcel_shard.parcel_id,
        relevance_score = compute_parcel_relevance(quantum),
        coordination_state = map_metabolic_to_coordination(quantum.metabolic_state),
        epoch_created = quantum.timestamps.created,
        epoch_last_active = quantum.timestamps.last_accessed,
        domain_tags = quantum.content.domain_tags,
        claim_summary = truncate(quantum.content.claim_text, 200),
        opinion_projected = quantum.opinion.belief + quantum.opinion.base_rate * quantum.opinion.uncertainty,
        edge_summary = EdgeSummary(
            support_count = count_edges(quantum, SUPPORT),
            contradiction_count = count_edges(quantum, CONTRADICTION),
            total = len(quantum.edges)
        ),
        high_canonical_confidence = quantum.opinion.belief > 0.8
    )
```

**C4 Projection (Semantic View):**

Fidelity target: 0.88

Preserves: full CLM-CNF-EVD-PRV-VRF chain, epistemic class, claim type, evidence references
Loses: metabolic state, SHREC signal associations, coherence graph position, vitality score

```
C4Projection:
    quantum_id:         URI
    asv_chain:          ASV_CLM        // full ASV CLM object with CNF, EVD[], PRV, VRF
    epistemic_class:    String         // from CLM.epistemic_class
    claim_type:         ClaimClass     // D|E|S|H|N|P|R|C
    domain_tags:        List<String>
    confidence_value:   Float          // from CNF
    confidence_method:  String         // from CNF.method
    evidence_count:     Int
    provenance_agent:   URI            // primary generating agent
    verification_status: String        // from VRF.status
    high_canonical_confidence: Boolean

function project_to_c4(quantum):
    clm = reconstruct_asv_clm(quantum)
    return C4Projection(
        quantum_id = quantum.id,
        asv_chain = clm,
        epistemic_class = clm.epistemic_class,
        claim_type = quantum.content.claim_type,
        domain_tags = quantum.content.domain_tags,
        confidence_value = clm.confidence.value,
        confidence_method = clm.confidence.method,
        evidence_count = len(clm.evidence),
        provenance_agent = quantum.provenance.wasAttributedTo,
        verification_status = clm.verification.status if clm.verification else "unverified",
        high_canonical_confidence = quantum.opinion.belief > 0.8
    )
```

**C5 Projection (Verification View):**

Fidelity target: 0.92

Preserves: credibility opinion (full b/d/u/a tuple), claim class, VTD reference, MCT reference, dependency claims
Loses: coherence graph position, consolidation history, circulation state, parcel assignment

```
C5Projection:
    quantum_id:         URI
    opinion:            OpinionTuple   // full Subjective Logic tuple
    claim_class:        ClaimClass
    mct_ref:            UUID           // MCT that admitted this quantum
    vtd_ref:            Hash           // VTD reference in PCVM store
    dependencies:       List<URI>      // quanta this quantum depends on
    supersedes:         Optional<URI>
    epoch_verified:     Epoch
    verification_tier:  Int            // 1, 2, or 3
    deep_audit_status:  String
    high_canonical_confidence: Boolean

function project_to_c5(quantum):
    mct = pcvm_store.get_mct(quantum.content.source_mct_id)
    return C5Projection(
        quantum_id = quantum.id,
        opinion = quantum.opinion,
        claim_class = quantum.content.claim_type,
        mct_ref = quantum.content.source_mct_id,
        vtd_ref = quantum.content.source_vtd_ref,
        dependencies = [e.target for e in quantum.edges if e.edge_type == DERIVATION],
        supersedes = next(
            (e.target for e in quantum.edges if e.edge_type == SUPERSESSION),
            None
        ),
        epoch_verified = mct.epoch_verified if mct else None,
        verification_tier = mct.verification_tier if mct else None,
        deep_audit_status = mct.deep_audit_status if mct else "UNKNOWN",
        high_canonical_confidence = quantum.opinion.belief > 0.8
    )
```

**Fidelity Monitoring (RA-1):**

```
function measure_projection_fidelity(sample_size=50):
    sample = random_sample(quantum_store.query(metabolic_state=ACTIVE), count=sample_size)
    fidelity_scores = {'c3': [], 'c4': [], 'c5': []}

    for quantum in sample:
        // C3 round-trip fidelity
        c3_proj = project_to_c3(quantum)
        c3_reconstructed = reconstruct_from_c3(c3_proj)
        fidelity_scores['c3'].append(semantic_similarity(quantum, c3_reconstructed))

        // C4 round-trip fidelity
        c4_proj = project_to_c4(quantum)
        c4_reconstructed = reconstruct_from_c4(c4_proj)
        fidelity_scores['c4'].append(semantic_similarity(quantum, c4_reconstructed))

        // C5 round-trip fidelity
        c5_proj = project_to_c5(quantum)
        c5_reconstructed = reconstruct_from_c5(c5_proj)
        fidelity_scores['c5'].append(semantic_similarity(quantum, c5_reconstructed))

    results = {
        'c3_mean': mean(fidelity_scores['c3']),  // target: 0.85
        'c4_mean': mean(fidelity_scores['c4']),  // target: 0.88
        'c5_mean': mean(fidelity_scores['c5']),  // target: 0.92
    }

    for system, score in results.items():
        target = {'c3': 0.85, 'c4': 0.88, 'c5': 0.92}[system]
        if score < target - 0.10:
            sentinel.report_fidelity_alarm(system, score, target)

    return results
```

**Projection Consistency Model (RA-4):**

```
ConsistencyLevel:
    EVENTUAL:       // within 1 epoch of canonical update
    EPOCH_BOUNDARY: // refreshed at epoch boundaries (DEFAULT)
    STRONG:         // immediate refresh, delivery confirmed

function get_consistency_level(quantum):
    if quantum.content.claim_type in ['D', 'C']:
        return STRONG
    if quantum.opinion.belief > 0.9:
        return STRONG
    if is_constitutional_claim(quantum):
        return STRONG
    return EPOCH_BOUNDARY

function refresh_projections(quantum, trigger):
    level = get_consistency_level(quantum)
    if level == STRONG:
        quantum.projections.c3 = project_to_c3(quantum)
        quantum.projections.c4 = project_to_c4(quantum)
        quantum.projections.c5 = project_to_c5(quantum)
        quantum.projections.generated_epoch = current_epoch()
        broadcast_projection_update(quantum)
    else:
        quantum.projections.stale = True

function epoch_boundary_refresh(epoch):
    stale_quanta = quantum_store.query(projections_stale=True)
    for quantum in stale_quanta:
        quantum.projections.c3 = project_to_c3(quantum)
        quantum.projections.c4 = project_to_c4(quantum)
        quantum.projections.c5 = project_to_c5(quantum)
        quantum.projections.generated_epoch = epoch
        quantum.projections.stale = False
```

---

### 4.9 Retrieval Interface

**Purpose:** Context-aware knowledge retrieval for agents and upstream systems. Supports structured queries, semantic search, neighborhood expansion, and temporal queries.

**Query API:**

```
RetrievalRequest:
    query_type:     STRUCTURED | SEMANTIC | NEIGHBORHOOD | TEMPORAL
    agent_id:       AgentID
    parcel_scope:   Optional<ParcelID>
    domain_filter:  Optional<List<String>>
    claim_type:     Optional<ClaimClass>
    min_vitality:   Optional<Float>
    min_belief:     Optional<Float>
    max_results:    Int              // default 20
    include_edges:  Boolean
    projection:     Optional<C3|C4|C5>

    // SEMANTIC:
    query_text:     Optional<String>
    // NEIGHBORHOOD:
    center_quantum: Optional<URI>
    radius:         Optional<Int>
    // TEMPORAL:
    epoch_range:    Optional<(Epoch, Epoch)>

RetrievalResponse:
    quanta:         List<QuantumResult>
    total_matches:  Int
    query_time_ms:  Float
    shards_consulted: List<ShardID>
```

**Retrieval Protocol:**

```
function retrieve(request):
    // Step 1: Route to shards
    if request.parcel_scope:
        shards = [get_shard(request.parcel_scope)]
    elif request.domain_filter:
        shards = get_shards_for_domains(request.domain_filter)
    else:
        shards = all_shards()

    // Step 2: Execute query per shard
    results = []
    for shard in shards:
        match request.query_type:
            case STRUCTURED:
                shard_results = shard.structured_query(
                    claim_type=request.claim_type,
                    domain=request.domain_filter,
                    min_vitality=request.min_vitality,
                    min_belief=request.min_belief
                )
            case SEMANTIC:
                shard_results = shard.semantic_search(
                    query_text=request.query_text,
                    limit=request.max_results * 2
                )
            case NEIGHBORHOOD:
                shard_results = coherence_graph.neighborhood(
                    center=request.center_quantum,
                    radius=request.radius,
                    max_quanta=request.max_results
                )
            case TEMPORAL:
                shard_results = shard.temporal_query(
                    epoch_start=request.epoch_range[0],
                    epoch_end=request.epoch_range[1]
                )
        results.extend(shard_results)

    // Step 3: Relevance ranking
    for r in results:
        q = r.quantum
        semantic_score = (
            compute_semantic_similarity(request.query_text, q.content.claim_text)
            if request.query_type == SEMANTIC else 0.5
        )
        r.relevance = (
            0.35 * semantic_score +
            0.20 * q.opinion.belief +
            0.20 * q.vitality +
            0.15 * exp(-0.03 * (current_epoch() - q.timestamps.last_modified)) +
            0.10 * domain_overlap(q.content.domain_tags, request.domain_filter or [])
        )
    results.sort(by=lambda r: r.relevance, reverse=True)

    // Step 4: Apply projection
    if request.projection:
        results = [apply_projection(r, request.projection) for r in results]

    // Step 5: Truncate and record access
    results = results[:request.max_results]
    for r in results:
        quantum_store.get(r.quantum_id).timestamps.last_accessed = current_epoch()

    return RetrievalResponse(
        quanta=results,
        total_matches=len(results),
        query_time_ms=elapsed_ms(),
        shards_consulted=[s.id for s in shards]
    )
```

---

## 5. Integration Contracts

### 5.1 PCVM Interface (C5)

**Direction:** Bidirectional
**Protocol:** MCT Admission / C-class Submission / Re-verification Trigger

**Inbound from PCVM (Knowledge Admission):**

```
PCVMAdmissionEvent:
    claim:           ASV_CLM        // verified claim
    mct:             MembraneCertificate
    vtd_ref:         Hash           // VTD stored in PCVM VTD Store
    bdl:             Bundle         // BDL record

// EMA handler:
function on_pcvm_admission(event):
    // Validate MCT signature
    if not verify_mct_signature(event.mct):
        reject("Invalid MCT signature")
        return

    // Validate MCT not expired
    if event.mct.expiration and event.mct.expiration < current_epoch():
        reject("Expired MCT")
        return

    // Ingest (Section 4.2)
    quanta = ingest(event.claim, event.mct, event.vtd_ref, event.bdl)
    return AcknowledgeAdmission(quantum_ids=[q.id for q in quanta])
```

**Outbound to PCVM (C-class Consolidation Submission):**

```
ConsolidationSubmission:
    claim:           ASV_CLM        // C-class claim from dreaming
    proposed_class:  "C"
    evidence_bundle: {
        source_quanta:     List<URI>
        synthesis_trace:   String     // LLM synthesis log
        falsification:     String     // falsification condition
        diversity_report:  DiversityReport
    }

// PCVM handles this as a standard claim submission
// Returns: VerificationOutcome (MCT if accepted, rejection if not)
```

**Outbound to PCVM (Re-verification Trigger):**

```
ReverificationTrigger:
    quantum_id:      URI
    claim_hash:      Hash
    original_mct:    UUID
    trigger_reason:  String
    // Reasons:
    //   "dependency_credibility_drop" — a quantum this one depends on lost credibility
    //   "contradiction_accumulated" — contradiction edges exceed threshold
    //   "supersession_conflict" — competing supersession claims
    //   "aging_uncertainty" — C-class quantum aged beyond threshold

// Trigger conditions:
function check_reverification_triggers(quantum, epoch):
    // 1. Dependency credibility drop
    for edge in quantum.edges:
        if edge.edge_type == DERIVATION:
            dependency = quantum_store.get(edge.target)
            if dependency.opinion.projected_probability() < 0.3:
                trigger_reverification(quantum, "dependency_credibility_drop")
                return

    // 2. Contradiction accumulation
    contradiction_ratio = count_edges(quantum, CONTRADICTION) / max(1, len(quantum.edges))
    if contradiction_ratio > 0.5:
        trigger_reverification(quantum, "contradiction_accumulated")
        return

    // 3. Opinion dropped below admission threshold
    threshold = admission_threshold(quantum.content.claim_type)
    if quantum.opinion.projected_probability() < threshold * 0.8:
        trigger_reverification(quantum, "below_admission_threshold")
```

### 5.2 Tidal Noosphere Interface (C3)

**Direction:** Bidirectional
**Protocol:** Epoch-Aligned Knowledge API

**Inbound from C3:**

```
// Epoch clock synchronization
function on_epoch_boundary(epoch, parcel_topology):
    // 1. Run epoch-phased metabolic processing
    run_ingestion_phase(epoch)
    run_circulation_phase(epoch)
    if epoch % config.consolidation_interval == 0:
        run_consolidation_phase(epoch)
    run_catabolism_phase(epoch)
    run_shrec_regulation(epoch)

    // 2. Refresh projections at epoch boundary
    epoch_boundary_refresh(epoch)

    // 3. Handle parcel topology changes (PTP alignment)
    if parcel_topology != current_topology:
        rebalance_on_parcel_change(current_topology, parcel_topology)
        update_topology(parcel_topology)

// Parcel-scoped knowledge queries
function on_parcel_knowledge_request(parcel_id, domain, max_results):
    return retrieve(RetrievalRequest(
        query_type = STRUCTURED,
        parcel_scope = parcel_id,
        domain_filter = domain,
        max_results = max_results,
        projection = C3
    ))
```

**Outbound to C3:**

```
// Locus-scoped knowledge summaries (per epoch)
function generate_locus_summary(locus_id, epoch):
    quanta = quantum_store.query(
        locus = locus_id,
        metabolic_state = ACTIVE,
        min_vitality = 0.3
    )
    return LocusSummary(
        locus_id = locus_id,
        epoch = epoch,
        active_quanta_count = len(quanta),
        domain_distribution = count_by_domain(quanta),
        mean_vitality = mean(q.vitality for q in quanta),
        contradiction_hotspots = find_contradiction_clusters(quanta),
        consolidation_candidates = count_viable_bridges(quanta)
    )
```

### 5.3 ASV Interface (C4)

**Direction:** Bidirectional
**Protocol:** ASV Type Mapping

**Inbound:** ASV CLM-CNF-EVD-PRV-VRF chains arrive as part of PCVM-verified claims. The ingestion pipeline (Section 4.2) handles the ASV-to-quantum field mapping.

**Outbound (Quantum-to-ASV reconstruction):**

```
function reconstruct_asv_clm(quantum):
    return ASV_CLM(
        id = quantum.content.asv_chain,
        claim_type = map_claim_class_to_asv(quantum.content.claim_type),
        epistemic_class = quantum.content.domain_tags[0] if quantum.content.domain_tags else "general",
        statement = quantum.content.claim_text,

        confidence = ASV_CNF(
            representation = "point",
            value = quantum.opinion.projected_probability(),
            method = infer_cnf_method(quantum),
            calibration = {
                calibrated = quantum.content.claim_type in ['D', 'S'],
                warning = "Projected from Subjective Logic opinion tuple" if
                          quantum.content.claim_type not in ['D', 'S'] else None
            }
        ),

        evidence = [
            ASV_EVD(
                quality_class = infer_evidence_quality(edge),
                source_id = edge.target,
                description = quantum_store.get(edge.target).content.claim_text[:100]
            )
            for edge in quantum.edges if edge.edge_type == DERIVATION
        ],

        provenance = ASV_PRV(
            wasGeneratedBy = quantum.provenance.wasGeneratedBy,
            wasAttributedTo = quantum.provenance.wasAttributedTo,
            used = [e.target for e in quantum.edges if e.edge_type == DERIVATION]
        ),

        verification = ASV_VRF(
            status = map_metabolic_to_vrf_status(quantum.metabolic_state),
            method = "membrane_verification",
            verifiers = [],  // not reconstructible from quantum alone
            verified_at = quantum.timestamps.created
        )
    )
```

### 5.4 Settlement Plane Interface

**Direction:** Bidirectional
**Protocol:** Metabolic Efficiency API

**Outbound (Knowledge Utility Metrics):**

```
MetabolicEfficiencyReport:
    epoch:                  Epoch
    quanta_ingested:        Int
    quanta_dissolved:       Int
    quanta_consolidated:    Int
    consolidation_acceptance_rate: Float  // C-class claims accepted by PCVM
    mean_vitality:          Float
    knowledge_utilization:  Float         // accessed_quanta / total_active
    metabolic_efficiency:   Float         // value_produced / resources_consumed
    shrec_budget_snapshot:  Dict<String, Float>

function report_to_settlement(epoch):
    report = MetabolicEfficiencyReport(
        epoch = epoch,
        quanta_ingested = ingestion_pipeline.epoch_count(),
        quanta_dissolved = catabolism_engine.epoch_dissolved_count(),
        quanta_consolidated = consolidation_engine.epoch_consolidated_count(),
        consolidation_acceptance_rate = consolidation_engine.pcvm_acceptance_rate(),
        mean_vitality = quantum_store.mean_vitality(),
        knowledge_utilization = quantum_store.access_ratio(epoch),
        metabolic_efficiency = compute_metabolic_efficiency(epoch),
        shrec_budget_snapshot = shrec.current_budget()
    )
    settlement_plane.submit_report(report)
```

**Inbound (Reward Signals):**

```
// Settlement provides reward signals based on knowledge utility
function on_settlement_reward(reward_signal):
    // Reward signals influence SHREC: high-reward knowledge domains
    // get increased ingestion and consolidation priority
    for domain, reward in reward_signal.domain_rewards.items():
        domain_registry.update_priority(domain, reward)
```

### 5.5 Sentinel Graph Interface

**Direction:** Bidirectional
**Protocol:** Sentinel Monitoring Protocol

**Outbound (EMA reports to Sentinel):**

```
// Coherence anomalies
function report_coherence_anomaly(anomaly_type, details):
    sentinel.submit_alert(SentinelAlert(
        source = "EMA",
        alert_type = anomaly_type,
        // Types: "contradiction_cluster", "rapid_vitality_drop",
        //        "quarantine_spike", "projection_fidelity_drop",
        //        "consolidation_poisoning_suspect", "catabolism_weaponization_suspect"
        severity = compute_severity(anomaly_type, details),
        details = details,
        epoch = current_epoch()
    ))

// Immune alerts
function report_immune_alert(alert):
    sentinel.submit_alert(SentinelAlert(
        source = "EMA:immune",
        alert_type = "autoimmune_alarm" | "false_positive_spike" | "catabolism_weaponization",
        severity = HIGH,
        details = alert,
        epoch = current_epoch()
    ))
```

**Inbound (Sentinel directs EMA):**

```
function on_sentinel_directive(directive):
    match directive.type:
        case "quarantine_quantum":
            quarantine(quantum_store.get(directive.quantum_id), current_epoch())
        case "force_reverification":
            trigger_reverification(quantum_store.get(directive.quantum_id), "sentinel_directive")
        case "adjust_catabolism":
            adjust_catabolism_threshold(directive.direction, directive.magnitude)
        case "freeze_consolidation":
            consolidation_engine.freeze(directive.duration_epochs)
```

---

## 6. Epistemic Quantum Specification

### 6.1 Complete JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:ema:schema:epistemic-quantum:v1",
  "title": "Epistemic Quantum",
  "description": "The fundamental knowledge unit in EMA — a 10-tuple.",
  "type": "object",
  "required": ["id", "content", "opinion", "provenance", "edges",
               "metabolic_state", "projections", "timestamps", "vitality"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uri",
      "pattern": "^urn:ema:q:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    },
    "content": {
      "type": "object",
      "required": ["claim_text", "claim_type", "domain_tags", "source_mct_id", "source_vtd_ref"],
      "properties": {
        "claim_text": { "type": "string", "maxLength": 5000 },
        "claim_type": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] },
        "domain_tags": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
        "structured_data": { "type": "object" },
        "source_mct_id": { "type": "string", "format": "uuid" },
        "source_vtd_ref": { "type": "string" },
        "asv_chain": { "type": "string", "format": "uri" },
        "temporal_validity_end": { "type": "integer" }
      }
    },
    "opinion": {
      "type": "object",
      "required": ["belief", "disbelief", "uncertainty", "base_rate"],
      "properties": {
        "belief":      { "type": "number", "minimum": 0, "maximum": 1 },
        "disbelief":   { "type": "number", "minimum": 0, "maximum": 1 },
        "uncertainty": { "type": "number", "minimum": 0, "maximum": 1 },
        "base_rate":   { "type": "number", "minimum": 0, "maximum": 1 }
      },
      "additionalProperties": false
    },
    "provenance": {
      "type": "object",
      "required": ["wasAttributedTo"],
      "properties": {
        "wasGeneratedBy": {
          "type": "object",
          "properties": {
            "activity_type": { "type": "string" },
            "started_at": { "type": "string", "format": "date-time" },
            "ended_at": { "type": "string", "format": "date-time" }
          }
        },
        "wasAttributedTo": { "type": "string", "format": "uri" },
        "used": { "type": "array", "items": { "type": "string", "format": "uri" } },
        "delegation_chain": { "type": "array", "items": { "type": "string", "format": "uri" } },
        "notes": { "type": "array", "items": { "type": "string" } }
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["edge_id", "source", "target", "edge_type", "weight", "created_epoch"],
        "properties": {
          "edge_id":        { "type": "string", "format": "uri" },
          "source":         { "type": "string", "format": "uri" },
          "target":         { "type": "string", "format": "uri" },
          "edge_type":      { "type": "string", "enum": ["support","contradiction","derivation","analogy","supersession"] },
          "weight":         { "type": "number", "minimum": 0, "maximum": 1 },
          "created_epoch":  { "type": "integer" },
          "last_activated": { "type": "integer" },
          "cross_shard":    { "type": "boolean" },
          "metadata":       { "type": "object" }
        }
      },
      "maxItems": 20
    },
    "metabolic_state": {
      "type": "string",
      "enum": ["active", "consolidating", "decaying", "quarantined", "dissolved"]
    },
    "projections": {
      "type": "object",
      "properties": {
        "c3": { "type": "object" },
        "c4": { "type": "object" },
        "c5": { "type": "object" },
        "generated_epoch": { "type": "integer" },
        "stale": { "type": "boolean" }
      }
    },
    "timestamps": {
      "type": "object",
      "required": ["created", "last_accessed", "last_modified", "state_transitions"],
      "properties": {
        "created":           { "type": "integer" },
        "last_accessed":     { "type": "integer" },
        "last_modified":     { "type": "integer" },
        "state_transitions": {
          "type": "array",
          "items": {
            "type": "array",
            "items": [
              { "type": "integer" },
              { "type": "string" }
            ]
          }
        }
      }
    },
    "dissolution_record": {
      "type": "object",
      "properties": {
        "dissolved_epoch":       { "type": "integer" },
        "reason":                { "type": "string" },
        "final_vitality":        { "type": "number" },
        "final_opinion":         { "type": "object" },
        "provenance_preserved":  { "type": "object" },
        "edge_snapshot":         { "type": "array" },
        "content_hash":          { "type": "string" }
      }
    },
    "vitality": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  }
}
```

### 6.2 Lifecycle Example

**Scenario:** A scheduling prediction enters the system, gets confirmed by observations, participates in consolidation, and eventually is superseded.

**Epoch 100 — Ingestion:**

```json
{
  "id": "urn:ema:q:a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "content": {
    "claim_text": "Load on parcel P7 will increase 40% in epochs 110-120 due to seasonal pattern",
    "claim_type": "S",
    "domain_tags": ["scheduling", "load_prediction"],
    "source_mct_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "source_vtd_ref": "sha256:abcdef1234567890",
    "asv_chain": "urn:asv:clm:load-prediction-p7-001"
  },
  "opinion": { "belief": 0.65, "disbelief": 0.05, "uncertainty": 0.30, "base_rate": 0.5 },
  "provenance": {
    "wasGeneratedBy": {
      "activity_type": "statistical_analysis",
      "started_at": "2026-03-10T10:00:00Z",
      "ended_at": "2026-03-10T10:00:05Z"
    },
    "wasAttributedTo": "urn:asv:agt:analytics-agent-03",
    "used": ["urn:ema:q:historical-load-data-p7"]
  },
  "edges": [
    {
      "edge_id": "urn:ema:e:001",
      "source": "urn:ema:q:a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "target": "urn:ema:q:historical-load-data-p7",
      "edge_type": "derivation",
      "weight": 0.8,
      "created_epoch": 100,
      "last_activated": 100,
      "cross_shard": false
    }
  ],
  "metabolic_state": "active",
  "projections": {
    "c3": { "quantum_id": "urn:ema:q:a1b2...", "parcel": "P7", "relevance_score": 0.72, "opinion_projected": 0.80 },
    "c4": { "quantum_id": "urn:ema:q:a1b2...", "claim_type": "S", "confidence_value": 0.80 },
    "c5": { "quantum_id": "urn:ema:q:a1b2...", "opinion": {"belief":0.65,"disbelief":0.05,"uncertainty":0.30,"base_rate":0.5} },
    "generated_epoch": 100,
    "stale": false
  },
  "timestamps": {
    "created": 100,
    "last_accessed": 100,
    "last_modified": 100,
    "state_transitions": [[100, "active"]]
  },
  "vitality": 0.68
}
```

**Epoch 115 — Confirmation (support edges added, opinion strengthened):**

```
Opinion update: { belief: 0.82, disbelief: 0.03, uncertainty: 0.15, base_rate: 0.5 }
New support edge from: urn:ema:q:actual-load-data-p7-epoch-110 (weight: 0.7)
Vitality: 0.68 -> 0.81
```

**Epoch 200 — Consolidation (selected as dreaming input):**

```
metabolic_state: "active" -> "consolidating"
Selected as source for cross-domain bridge: load_prediction <-> resource_allocation
Dreaming discovers: "Seasonal load patterns in scheduling correlate with
    resource contention patterns in allocation — both follow sinusoidal
    curves with period ~20 epochs, suggesting a common underlying cycle."
C-class claim submitted to PCVM -> ACCEPTED (MCT issued)
New consolidated quantum created with derivation edge back to this quantum.
metabolic_state: "consolidating" -> "active"
```

**Epoch 450 — Supersession:**

```
New quantum arrives: "Updated load model for P7 using transformer-based
    forecasting shows 55% improvement in accuracy over statistical model"
Supersession edge created (weight: 1.0)
metabolic_state: "active" -> "decaying"
Vitality: 0.45 -> 0.28 (below decay_threshold)
```

**Epoch 560 — Dissolution:**

```
Vitality has been below 0.1 for 10 epochs
metabolic_state: "decaying" -> "quarantined"
After 100-epoch quarantine without rescue:
metabolic_state: "quarantined" -> "dissolved"
Dissolution record preserved. Provenance chain maintained.
Dependent quanta notified. Derivation edges weakened.
```

---

## 7. Adversarial Defense Architecture

This section addresses all 5 adversarial findings (2 CRITICAL, 3 HIGH) from the Adversarial Report.

### 7.1 A3: Consolidation Poisoning (CRITICAL)

**Attack:** Coordinated agents inject quanta to steer dreaming toward a desired conclusion.

**Defense layers (defense in depth):**

**Layer 1 — Provenance Diversity Gate (primary defense):**
- Consolidation inputs must come from >=5 independent agents across >=3 parcels (Section 4.5, HG-3)
- No single agent may contribute >30% of consolidation inputs
- No derivation cluster may constitute >40% of inputs
- Independence verified by checking: different agents, different parcels, no short derivation chains

**Layer 2 — Consolidation Input Audit:**

```
function audit_consolidation_inputs(candidate_set, consolidated_claim):
    // Post-hoc audit of accepted consolidations
    source_graph = build_provenance_graph(candidate_set.quanta)

    // Check 1: Provenance clustering
    agent_clusters = cluster_by_agent_similarity(source_graph)
    if max_cluster_size(agent_clusters) > 0.40 * len(candidate_set.quanta):
        flag_consolidation(consolidated_claim, "provenance_clustering")

    // Check 2: Temporal clustering (quanta created in suspiciously close timeframe)
    creation_epochs = [q.timestamps.created for q in candidate_set.quanta]
    if std_dev(creation_epochs) < 3:  // most quanta created within 3 epochs
        flag_consolidation(consolidated_claim, "temporal_clustering")

    // Check 3: Content similarity (quanta suspiciously similar to each other)
    pairwise_sim = pairwise_semantic_similarity(candidate_set.quanta)
    if mean(pairwise_sim) > 0.85:
        flag_consolidation(consolidated_claim, "content_homogeneity")
```

**Layer 3 — PCVM Verification Gate:**
- All C-class claims pass full PCVM verification (C-class is Tier 1)
- VTD must include: source quanta references, synthesis reasoning trace, falsification condition, diversity report
- PCVM deep-audit may re-examine consolidation reasoning

**Layer 4 — High Initial Uncertainty:**
- C-class quanta start at opinion.uncertainty >= 0.4
- C-class quanta require independent confirmation to increase belief
- Aging uncertainty (RA-5): +0.1 uncertainty per 50 epochs without evidence

### 7.2 A8: Coherence Collapse at Scale (CRITICAL)

**Attack:** Coherence graph becomes intractable at 1B+ quanta.

**Defense: Hierarchical Sharding (Section 4.3, HG-2):**

| Scale | Strategy | Coherence Mode |
|-------|----------|---------------|
| < 100K quanta | Full graph | All edges computed |
| 100K-10M | Parcel-aligned shards | Intra-shard full, cross-shard sampled (10%) |
| > 10M | Hierarchical clusters | Cluster-level coherence, representative sampling |

**Active Edge Budget:** Max 20 edges per quantum. Lowest-weight edges archived when budget exceeded.

**Edge TTL:** Edges with weight < 0.01 are pruned. Edge weights decay exponentially (half-life ~35 epochs).

**Computation Bounds:** Per-shard computation is O(V_local * E_max). Cross-shard overhead capped at 30% of epoch budget.

### 7.3 A4: Projection Gap Exploitation (HIGH)

**Attack:** Agent crafts quantum whose projection appears benign but canonical form is suspicious.

**Defense:**

1. **High Canonical Confidence Flag:** All projections include `high_canonical_confidence: true` when canonical opinion.belief > 0.8. Projection consumers are alerted to check canonical quantum for high-stakes decisions.

2. **Canonical-Source Principle:** Projections are views, not authoritative copies. Any agent can request the canonical quantum at any time via the Retrieval Interface.

3. **PCVM Verification on Canonical:** PCVM operates on the canonical quantum, not projections. Fabricated evidence fails E-class verification regardless of how the projection appears.

4. **Projection Audit Trail:** All projection accesses are logged. Patterns of agents relying exclusively on projections for high-stakes decisions trigger Sentinel review.

### 7.4 A6: Catabolism Weaponization (HIGH)

**Attack:** Adversary floods contradiction edges to drive valuable quantum below catabolism threshold.

**Defense:**

1. **Per-Agent Contradiction Cap (RA-3):** Total contradiction_factor from any single agent capped at 0.3, regardless of how many contradicting quanta that agent creates.

```
// In vitality computation (Section 4.1):
agent_contradiction = {}
for e in quantum.edges:
    if e.edge_type == CONTRADICTION:
        source_agent = get_provenance_agent(e.source)
        agent_contradiction[source_agent] = min(
            agent_contradiction.get(source_agent, 0) + e.weight,
            0.3  // CAP
        )
```

2. **Quarantine Rescue:** 100-epoch quarantine period provides detection window. Immune audit samples quarantined quanta and rescues those with legitimate active support edges.

3. **Immune Self-Audit:** Weekly audit checks false positive rate. If > 15% of quarantined quanta have active support (indicating over-aggressive catabolism), catabolism threshold is raised.

4. **Sentinel Reporting:** Rapid vitality drops (> 0.3 in a single epoch) for quanta with prior high vitality trigger Sentinel alert.

### 7.5 A10: Cross-System Desynchronization (HIGH)

**Attack:** Exploiting timing gap between canonical update and projection refresh.

**Defense:**

1. **Tiered Consistency Model (RA-4):**
   - STRONG consistency for D-class, C-class, high-confidence (>0.9), and constitutional quanta — immediate projection refresh on canonical update
   - EPOCH_BOUNDARY consistency for all others — guaranteed fresh at epoch boundaries
   - EVENTUAL consistency for low-stakes quanta — within 1 epoch

2. **Epoch-Boundary Synchronization:** C3 tidal epochs provide natural sync points. All projections are guaranteed consistent at epoch boundaries.

3. **Canonical Source Access:** Any agent can bypass projections and query the canonical quantum directly via the Retrieval Interface. High-stakes decisions should always check canonical source.

4. **Projection Staleness Monitoring (MF-5):** Mean epochs since last projection refresh tracked. If > 3 epochs, refresh frequency is automatically increased.

---

## 8. Scalability Architecture

### 8.1 Scale Tiers

| Tier | Quanta | Agents | Epochs | Architecture |
|------|--------|--------|--------|-------------|
| T1: Startup | < 100K | 1K | 1-hour | Full coherence, single-shard, global dreaming |
| T2: Growth | 100K-10M | 1K-10K | 1-hour | Sharded coherence, per-parcel dreaming |
| T3: Scale | > 10M | 10K-100K | 1-hour | Hierarchical coherence, cluster dreaming |

### 8.2 Tier Transition Detection

```
function detect_tier_transition(epoch):
    quanta_count = quantum_store.active_count()
    current_tier = get_current_tier()

    if current_tier == T1 and quanta_count > 80_000:     // 80% of T1 ceiling
        prepare_tier_transition(T1, T2)
    elif current_tier == T2 and quanta_count > 8_000_000: // 80% of T2 ceiling
        prepare_tier_transition(T2, T3)

function prepare_tier_transition(from_tier, to_tier):
    // 1. Announce transition (10-epoch warning)
    broadcast_tier_transition_warning(from_tier, to_tier)

    // 2. Begin shard preparation
    if to_tier == T2:
        initialize_shard_topology(parcel_count=current_parcel_count())
        begin_quantum_migration_to_shards()
    elif to_tier == T3:
        initialize_cluster_hierarchy()
        begin_cluster_assignment()

    // 3. Transition SHREC parameters
    shrec.update_scale_parameters(to_tier)

    // 4. Transition dreaming scope
    consolidation_engine.set_scope(
        T2: SHARD_LOCAL,
        T3: CLUSTER_REPRESENTATIVES
    )
```

### 8.3 Resource Budgets by Tier

| Resource | T1 Budget | T2 Budget | T3 Budget |
|----------|-----------|-----------|-----------|
| Coherence computation | < 10% CPU | < 20% CPU | < 25% CPU |
| Edge storage | < 1 GB | < 100 GB | < 10 TB |
| LLM tokens (dreaming) | 200/cycle | 500/cycle | 1000/cycle |
| Projection refresh | < 5% CPU | < 10% CPU | < 15% CPU |
| Cross-shard overhead | N/A | < 30% of coherence | < 40% of coherence |

### 8.4 Metabolic Advantage Baseline (RA-2)

The comparison baseline for Science Advisor Experiment 1:

**Baseline System: Standard Knowledge Graph + TTL**
- Knowledge stored as typed triples in a graph database
- TTL-based expiry: each triple has a configurable TTL (default 500 epochs)
- Periodic re-indexing: every 50 epochs, scan for stale/inconsistent triples
- Query-based retrieval: pull model only, no push circulation
- No consolidation/dreaming
- No ecological regulation (fixed resource allocation)
- No multi-ontology projection (single schema)

**Comparison Metrics:**
1. Knowledge retrieval quality: precision@10, recall@10 for domain-specific queries
2. Staleness rate: fraction of returned results that are outdated
3. Storage growth: total storage over 1000 epochs
4. Shock response: time to recover from 30% knowledge invalidation event

**Expected EMA Advantages:**
- Better staleness management (vitality-based vs. fixed TTL)
- Faster shock response (SHREC detects and adapts vs. waiting for periodic re-index)
- Cross-domain discovery (dreaming produces novel insights — no baseline equivalent)

**Expected EMA Disadvantages:**
- Higher computational overhead (metabolic processing vs. simple TTL check)
- Higher complexity (9 components vs. 3)
- Higher latency for simple queries (projection overhead)

---

## 9. Security Model

### 9.1 Trust Boundaries

```
+------------------------------------------------------------------+
|  CONSTITUTIONAL BOUNDARY (G-class changes only)                   |
|  - SHREC floor allocations                                        |
|  - Catabolism thresholds                                          |
|  - Consolidation diversity requirements                           |
|  - Projection fidelity targets                                    |
|  - Edge budget limits                                             |
|  - Quarantine period                                              |
+------------------------------------------------------------------+
|  MEMBRANE BOUNDARY (KS-1: no entry without MCT)                  |
|  - All ingestion gated by PCVM MCT                                |
|  - All consolidation output verified by PCVM                      |
|  - Re-verification triggers from EMA to PCVM                      |
+------------------------------------------------------------------+
|  OPERATIONAL BOUNDARY (standard authorization)                    |
|  - Subscription management                                        |
|  - Retrieval queries                                               |
|  - SHREC parameter monitoring                                      |
+------------------------------------------------------------------+
```

### 9.2 Invariants

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| KS-1 | No quantum enters without valid MCT | Ingestion pipeline rejects unsigned/expired MCTs |
| KS-2 | EMA cannot override PCVM opinions beyond threshold | Opinion updates that cross threshold trigger re-verification |
| KS-3 | Consolidation output passes PCVM | C-class claims submitted through standard PCVM pipeline |
| KS-4 | Constitutional parameters require G-class | Parameter update functions check governance authorization |
| KS-5 | Projections are views, canonical is truth | Projections contain quantum_id for canonical lookup |

### 9.3 Data Protection

- **Quantum content:** Stored encrypted at rest. Access logged per agent.
- **Dissolution records:** Append-only audit trail. Content hashed, not stored in cleartext after dissolution.
- **Provenance chains:** Immutable once created. Agent identity references are URIs, not PII.
- **Edge weights:** Not individually sensitive, but aggregate edge patterns may reveal agent behavior. Access to full edge graph requires elevated authorization.

---

## 10. Architectural Decisions

### AD-1: Epoch-Phased Processing Order

**Decision:** Metabolic processes execute in strict order within each epoch: ingestion -> circulation -> consolidation -> catabolism -> SHREC regulation.

**Rationale:** Strict ordering prevents race conditions between processes. Ingestion must complete before circulation (new quanta must be in the graph before they can be pushed). Consolidation must complete before catabolism (consolidation locks prevent catabolism of dreaming inputs). SHREC regulation runs last to assess the epoch's metabolic activity and adjust budget for the next epoch.

**Tradeoff:** Strict ordering reduces parallelism. At T3 scale, individual phases may take significant time, extending epoch processing. Mitigation: intra-phase parallelism (e.g., per-shard parallel ingestion) while maintaining inter-phase ordering.

**Alternative rejected:** Event-driven processing (each event triggers the appropriate process). Rejected because: (a) complex race conditions between concurrent metabolic processes, (b) no natural synchronization point for SHREC budget computation, (c) harder to reason about system state.

### AD-2: Push + Pull Hybrid Circulation

**Decision:** Circulation uses push-based notifications (subscription model) combined with pull-based retrieval (query API).

**Rationale:** Push is efficient for agents with known, stable interests (e.g., a scheduling agent always wants load predictions). Pull is efficient for ad-hoc, unpredictable needs (e.g., a verification agent investigating a specific claim). Neither alone suffices.

**Tradeoff:** Push adds notification overhead even when agents don't need the pushed quanta. Mitigation: rate limits (max_per_epoch), relevance thresholds (min 0.3), and digest mode for low-priority subscriptions.

**Alternative rejected:** Pure pull (standard query model). Rejected because: agents would need to poll constantly, increasing query load and introducing latency for time-sensitive knowledge (contradictions, supersessions).

### AD-3: Lotka-Volterra with PID Overlay

**Decision:** SHREC uses ecological competition (Lotka-Volterra) as primary controller with PID as graduated safety overlay.

**Rationale:** Ecological dynamics provide self-organizing budget allocation that adapts to system conditions without manual tuning. PID provides a well-understood safety net for regime transitions and edge cases. The graduated engagement (Normal: ecology only; Elevated: 0.5x PID; Critical: 1.0x PID; Constitutional: PID override) prevents the two controllers from interfering under normal operation.

**Tradeoff:** Two control layers add complexity and potential for interaction instability. Mitigation: PID is inactive during Normal regime (most of the time). Stability analysis (HG-1) validates no destructive interference.

**Alternative rejected:** Pure PID control (5 independent PID loops). Rejected because: requires explicit setpoint tuning for each signal, does not self-organize when new domains or agent populations change system dynamics. Pure adaptive control (model-reference, etc.). Rejected because: too many tuning parameters, insufficient transparency for constitutional governance.

### AD-4: Parcel-Aligned Sharding

**Decision:** Coherence graph shards align with C3 parcel boundaries.

**Rationale:** C3 parcels are the natural unit of agent locality and domain affinity. Quanta within a parcel are more likely to share domains and have edges to each other than quanta across parcels. Aligning shards with parcels minimizes cross-shard edges and leverages C3's existing topology management (PTP for reconfiguration).

**Tradeoff:** If domains do not align with parcels (e.g., cross-cutting concerns that span all parcels), cross-shard coherence is only sampled, not fully computed. Mitigation: cross-shard sampling at 10% (T2) or cluster representatives (T3).

### AD-5: 3-Pass Majority Vote for Dreaming

**Decision:** Consolidation uses 3 independent LLM passes with majority vote rather than a single pass or ensemble.

**Rationale:** Single-pass produces higher hallucination rates. 3-pass with majority vote reduces noise (a hallucination must appear in at least 2 of 3 independent runs). The third pass (critical evaluation at low temperature) acts as an internal adversarial check.

**Tradeoff:** 3x the LLM inference cost per consolidation cycle. Mitigation: consolidation runs infrequently (every 10 epochs by default) and only when viable bridges are detected.

**Known limitation:** If all 3 passes hallucinate the same culturally common analogy, majority vote confirms the hallucination. Defense: PCVM verification gate + high initial uncertainty + aging uncertainty for unconfirmed C-class claims.

### AD-6: Bounded-Loss Rather Than Lossless Projection

**Decision:** Projections explicitly lose information with measured fidelity targets rather than claiming lossless translation.

**Rationale:** The Science Advisor's information-theoretic analysis (Claim 2) demonstrates that lossless bidirectional projection between frames of different information capacity is impossible. Honest bounded-loss projections with fidelity monitoring provide genuine architectural value without false guarantees.

**Tradeoff:** Projection consumers operate on incomplete information. Mitigation: high_canonical_confidence flag alerts consumers when the canonical quantum has information the projection omits. Canonical-source principle ensures any agent can access the full quantum.

### AD-7: Quarantine Before Dissolution

**Decision:** Catabolism always quarantines before dissolving. No immediate dissolution.

**Rationale:** Quarantine provides a reversibility window (100 epochs) for detecting false positives (catabolism weaponization, autoimmune pathology). Immediate dissolution is irreversible — dissolved quanta preserve only a hash of content, not the content itself.

**Tradeoff:** Quarantine consumes storage (full quantum snapshots). Mitigation: quarantine budget limit (30% of active storage), oscillation detection (quanta quarantined >3 times get reduced snapshots).

---

## 11. Traceability Appendix

### Feasibility Hard Gates -> Architecture Sections

| Hard Gate | Requirement | Architecture Section |
|-----------|-------------|---------------------|
| HG-1: SHREC Stability | 5 signals, 1000 epochs, floor guarantees, no exclusion | 3.1 (experiment), 4.7 (SHREC Controller) |
| HG-2: Coherence Scaling | Sharding, active edge budget, scale tiers | 3.2 (experiment), 4.3 (Coherence Graph), 8 (Scalability) |
| HG-3: Provenance Diversity | >=5 agents, >=3 parcels, enforcement mechanism | 3.3 (experiment), 4.5 (Consolidation Engine) |
| HG-4: Dreaming Precision | 200 claims, 5 domains, precision/hallucination | 3.4 (experiment), 4.5 (Consolidation Engine) |

### Required Actions -> Architecture Sections

| Action | Requirement | Architecture Section |
|--------|-------------|---------------------|
| RA-1: Projection Fidelity | Measure round-trip fidelity on 50 quanta | 4.8 (Projection Engine — fidelity monitoring) |
| RA-2: Metabolic Advantage Baseline | Specify comparison baseline | 8.4 (Metabolic Advantage Baseline) |
| RA-3: Contradiction Weight Caps | Per-agent cap at 0.3 | 4.1 (vitality computation), 7.4 (A6 defense) |
| RA-4: Projection Consistency | Consistency model specification | 4.8 (Projection Engine — consistency model) |
| RA-5: Aging Uncertainty | C-class uncertainty increase per 50 epochs | 4.5 (Consolidation Engine — aging uncertainty) |

### Adversarial Findings -> Defense Architecture

| Attack | Severity | Defense Section |
|--------|----------|----------------|
| A1: Quantum Corruption | MEDIUM | 4.1 (vitality — edge cross-check), 4.2 (initial edges) |
| A2: Hallucination Bypass | MEDIUM | 4.5 (3-pass synthesis, PCVM gate, aging uncertainty) |
| A3: Consolidation Poisoning | CRITICAL | 7.1 (4-layer defense), 4.5 (diversity validation) |
| A4: Projection Gap | HIGH | 7.3 (confidence flag, canonical-source principle) |
| A5: SHREC Gaming | MEDIUM | 4.7 (floor guarantees, frequency-dependent selection) |
| A6: Catabolism Weaponization | HIGH | 7.4 (per-agent cap, quarantine rescue, immune audit) |
| A7: Immune Evasion | MEDIUM | 4.6 (transitive coherence, immune audit) |
| A8: Coherence Collapse | CRITICAL | 7.2 (sharding, edge budget, TTL), 4.3 (Coherence Graph) |
| A9: Quarantine Overflow | MEDIUM | 4.6 (quarantine budget, oscillation detection) |
| A10: Desynchronization | HIGH | 7.5 (tiered consistency, epoch sync) |

### Monitoring Flags -> Architecture Sections

| Flag | Metric | Section |
|------|--------|---------|
| MF-1: Dreaming cost | LLM tokens per cycle | 4.5 (LLM synthesis) |
| MF-2: SHREC variance | CV of any signal | 4.7 (signal measurement) |
| MF-3: Quarantine population | % of active | 4.6 (quarantine budget) |
| MF-4: Consolidation acceptance | % C-class passing PCVM | 4.5 (PCVM gate) |
| MF-5: Projection staleness | Mean epochs since refresh | 4.8 (consistency model) |
| MF-6: Edge density | Active edges per quantum | 4.3 (edge budget enforcement) |
| MF-7: Metabolic efficiency | Value per quantum | 5.4 (Settlement interface) |
| MF-8: Integration latency | Update to projection refresh | 4.8 (cache manager) |

### C3/C4/C5 Interface Alignment

| System | Interface Contract | Key Data Structures |
|--------|-------------------|-------------------|
| C3 (Tidal Noosphere) | Epoch clock, parcel topology, locus-scoped knowledge | C3Projection, LocusSummary, epoch_boundary event |
| C4 (ASV) | CLM-CNF-EVD-PRV-VRF chain mapping | C4Projection, ASV type reconstruction |
| C5 (PCVM) | MCT admission, C-class submission, re-verify triggers | C5Projection, MCT, VTD reference, BDL |
| Settlement | Metabolic efficiency metrics, reward signals | MetabolicEfficiencyReport |
| Sentinel | Coherence anomalies, immune alerts, directives | SentinelAlert, SentinelDirective |

---

*Architecture document produced under Atrahasis Agent System v2.0 protocol.*
*C6: Epistemic Metabolism Architecture (EMA) -- DESIGN stage.*
*Architecture Designer role.*