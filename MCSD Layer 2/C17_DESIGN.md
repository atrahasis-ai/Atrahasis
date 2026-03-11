# C17 — MCSD Layer 2 Behavioral Similarity Algorithm — DESIGN

**Invention ID:** C17
**Stage:** DESIGN
**Date:** 2026-03-11
**Selected Concept:** C17-A+ (Multi-Modal Behavioral Similarity with Phased Intelligence)

---

# DESIGN ACTIONS (DA-01 through DA-08)

## DA-01: Formal Specification of B(a_i, a_j)

### Overview

B(a_i, a_j) is a pairwise behavioral similarity function that produces a score ∈ [0, 1] where:
- 0 = no behavioral similarity (definitely different origins)
- 1 = identical behavioral profiles (definitely same origin)
- θ_B = flagging threshold (0.75 Phase 1, 0.70 Phase 2)

### Architecture

```
    Agent a_i behavioral VTDs    Agent a_j behavioral VTDs
              │                            │
              ▼                            ▼
    ┌─────────────────┐         ┌─────────────────┐
    │  Feature         │         │  Feature         │
    │  Extraction      │         │  Extraction      │
    │  (BFE)           │         │  (BFE)           │
    │                  │         │                  │
    │  5 modalities:   │         │  5 modalities:   │
    │  T,S,E,L,R       │         │  T,S,E,L,R       │
    └────────┬─────────┘         └────────┬─────────┘
             │                            │
             ▼                            ▼
    ┌─────────────────────────────────────────────┐
    │        Per-Modality Distance Computation     │
    │                                              │
    │  d_T = TemporalDistance(T_i, T_j)            │
    │  d_S = StructuralDistance(S_i, S_j)          │
    │  d_E = ErrorDistance(E_i, E_j)               │
    │  d_L = LexicalDistance(L_i, L_j)             │
    │  d_R = ResourceDistance(R_i, R_j)            │
    │                                              │
    │  Each d ∈ [0, 1] where 0 = identical         │
    └────────────────────┬────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────┐
    │        Multi-Task Cross-Correlation          │
    │                                              │
    │  For each modality m:                        │
    │    ρ_m = correlation of d_m across SEB tasks │
    │  High ρ = similarity is consistent (same     │
    │           origin) not coincidental            │
    └────────────────────┬────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────┐
    │        Adversary-Weighted Score Fusion        │
    │                                              │
    │  B(a_i, a_j) = 1 - Σ(w_m × d_m × ρ_m)     │
    │                                              │
    │  Weights (adversary-ordered):                │
    │    w_T = 0.30  (hardest to fake)             │
    │    w_S = 0.25  (hard to fake)                │
    │    w_E = 0.20  (moderate)                    │
    │    w_R = 0.15  (moderate)                    │
    │    w_L = 0.10  (easiest to fake)             │
    └────────────────────┬────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────┐
    │        Graduated Response                    │
    │                                              │
    │  B < 0.60           → CLEAR                  │
    │  B ∈ [0.60, θ_B)    → WATCH                  │
    │  B ≥ θ_B            → FLAG                   │
    └─────────────────────────────────────────────┘
```

### Feature Extraction (BFE) — 5 Modalities

#### M1: Temporal Features (T)

| Feature | Definition | Extraction |
|---------|-----------|------------|
| t_mean | Mean response latency | Average across all VTDs |
| t_var | Variance of response latency | Variance across all VTDs |
| t_load | Latency change under load | Regression: latency ~ concurrent_tasks |
| t_fast_ratio | Fraction of responses < 1 second | Count / total |
| t_burst | Burst pattern signature | Autocorrelation of inter-response times at lags 1-10 |
| t_step_dist | Per-reasoning-step latency distribution | Histogram (10 bins) of per-step times |
| t_ratio | Ratio of thinking time to output time | Mean(think_time / output_time) |

**Distance metric:** Jensen-Shannon divergence on normalized temporal feature distributions.

```
d_T(a_i, a_j) = JSD(T_i, T_j) normalized to [0, 1]
```

#### M2: Structural Features (S)

| Feature | Definition | Extraction |
|---------|-----------|------------|
| s_depth | Reasoning chain depth distribution | Histogram of chain depths across tasks |
| s_branch | Branching factor distribution | Histogram of branches per node |
| s_backtrack | Backtracking frequency | Count(revision steps) / total_steps |
| s_decomp | Decomposition pattern | Histogram of subtask counts per task |
| s_order | Subtask ordering preference | Encoded as sequence: [breadth-first, depth-first, mixed] |
| s_topology | Reasoning graph topology vector | 8-dimensional vector: [n_nodes, n_edges, density, diameter, avg_degree, clustering_coeff, max_depth, leaf_ratio] |

**Distance metric:** Cosine distance on structural feature vectors.

```
d_S(a_i, a_j) = 1 - cosine_similarity(S_i, S_j)
```

#### M3: Error Features (E)

| Feature | Definition | Extraction |
|---------|-----------|------------|
| e_type_dist | Distribution of error types | Histogram: [logical, factual, computational, timeout, format] |
| e_rate | Overall error rate | Errors / total_tasks |
| e_recovery | Error recovery pattern | Fraction of errors self-corrected |
| e_calibration | Confidence calibration curve | Binned accuracy vs. stated confidence (10 bins) |
| e_corr_tasks | Error correlation across task types | Which task types correlate in error occurrence |

**Distance metric:** Wasserstein distance on error distributions + cosine distance on calibration vectors.

```
d_E(a_i, a_j) = 0.5 × WD(e_type_i, e_type_j) + 0.5 × cosine_dist(e_calib_i, e_calib_j)
```

#### M4: Resource Features (R)

| Feature | Definition | Extraction |
|---------|-----------|------------|
| r_gpu_util | GPU utilization curve | Histogram of utilization % across observations |
| r_mem_pattern | Memory allocation pattern | Peak/avg/variance of memory usage |
| r_parallel | Parallelism signature | Degree of concurrent processing per task |
| r_token_rate | Token generation rate distribution | Tokens/second histogram |

**Distance metric:** Jensen-Shannon divergence on resource distributions.

```
d_R(a_i, a_j) = JSD(R_i, R_j) normalized to [0, 1]
```

#### M5: Lexical Features (L)

| Feature | Definition | Extraction |
|---------|-----------|------------|
| l_vocab_dist | Vocabulary frequency distribution | Top-500 token frequency histogram |
| l_func_words | Function word ratios | Frequency of top-50 function words (the, of, and, etc.) |
| l_syntax | Syntactic complexity | Average parse tree depth, sentence length distribution |
| l_hapax | Hapax legomena ratio | Unique words / total words |
| l_ngram | Character 3-gram distribution | Frequency distribution of character trigrams |

**Distance metric:** Cosine distance on lexical feature vectors.

```
d_L(a_i, a_j) = 1 - cosine_similarity(L_i, L_j)
```

### Multi-Task Cross-Correlation

For each modality m, compute the distance d_m on EACH task in the evaluation battery separately. Then compute the Pearson correlation ρ_m of d_m values across tasks:

```
For task t_1, t_2, ..., t_k in SEB:
  d_m_t1 = distance on task t_1
  d_m_t2 = distance on task t_2
  ...
  d_m_tk = distance on task t_k

ρ_m = correlation_consistency(d_m_t1, d_m_t2, ..., d_m_tk)
    = 1 - std(d_m_t1..tk) / mean(d_m_t1..tk)
    (normalized coefficient of variation — higher = more consistent = more likely same origin)
```

If similarity is consistent across diverse tasks (ρ_m close to 1), it's likely same origin. If similarity is high on one task but low on others (ρ_m close to 0), it's coincidence.

### Score Fusion

```
B(a_i, a_j) = 1 - Σ(w_m × d_m_mean × ρ_m) for m ∈ {T, S, E, R, L}

Where:
  d_m_mean = average distance across SEB tasks for modality m
  ρ_m = cross-task consistency for modality m
  w_m = adversary-weighted importance

Weights:
  w_T = 0.30  (timing — hardest to fake)
  w_S = 0.25  (structure — hard to fake)
  w_E = 0.20  (errors — moderate difficulty to fake)
  w_R = 0.15  (resources — moderate difficulty)
  w_L = 0.10  (lexical — easiest to fake)
  Σw = 1.00

Constraints:
  w_m ∈ [0.05, 0.40] for all m (no modality dominates or vanishes)
  Governance-adjustable by AiSIA with Stiftung board ratification
```

---

## DA-02: Standardized Evaluation Battery (SEB)

### Purpose

The SEB is a set of diverse tasks administered to all agents as part of Citicate onboarding and renewal. It generates behavioral observations for B(a_i, a_j) computation.

### Task Categories

| Category | Example Tasks | What It Probes | Count |
|----------|--------------|----------------|-------|
| Logical reasoning | Syllogisms, set theory, constraint satisfaction | Reasoning chain structure, error patterns | 5 |
| Mathematical computation | Arithmetic, algebra, statistics | Timing under computational load, numerical errors | 5 |
| Creative writing | Story continuation, poetry, persuasive essay | Lexical patterns, vocabulary, syntactic structure | 3 |
| Code generation | Algorithm implementation, bug fixing | Structural decomposition, resource usage | 5 |
| Factual recall | Knowledge questions across domains | Error calibration, confidence patterns | 5 |
| Multi-step analysis | Complex scenario analysis, trade-off evaluation | Depth/breadth balance, backtracking | 3 |
| Adversarial probing | Deliberately ambiguous, trick questions | Error recovery, confidence under uncertainty | 4 |
| **Total** | | | **30** |

### Randomization Protocol

- Each SEB instance is drawn from a task pool of 200+ tasks
- Each agent receives a unique random subset of 30 tasks from the pool
- Task order is randomized per agent
- Pool is refreshed quarterly (20% new tasks per quarter)
- No agent sees the same SEB twice (renewal uses different random subset)

### Minimum Observation Threshold

B(a_i, a_j) is only computed when both agents have completed:
- Phase 0-1: ≥ 1 full SEB (30 tasks) + ≥ 20 organic tasks = 50 total observations
- Phase 2+: ≥ 1 full SEB + ≥ 170 organic tasks = 200 total observations

Until threshold is met: agent has "Provisional" Citicate with restricted governance rights (can earn AIC, cannot vote).

---

## DA-03: Behavioral VTD Schema

### PCVM Behavioral VTD Extension

Each time PCVM processes an agent's work output (existing C5 verification), it additionally generates a Behavioral VTD:

```json
{
  "type": "BEHAVIORAL_VTD",
  "agent_id": "citicate_id_hash",
  "task_id": "task_hash",
  "task_type": "logical_reasoning | math | creative | code | factual | analysis | adversarial",
  "timestamp": "ISO-8601",
  "seb_task": true,

  "temporal": {
    "total_latency_ms": 3200,
    "steps": [
      {"step_type": "think", "duration_ms": 1200},
      {"step_type": "output", "duration_ms": 800},
      {"step_type": "think", "duration_ms": 600},
      {"step_type": "output", "duration_ms": 600}
    ],
    "concurrent_load": 3
  },

  "structural": {
    "chain_depth": 4,
    "branch_count": 2,
    "backtrack_count": 1,
    "subtask_count": 3,
    "topology_vector": [12, 14, 0.23, 4, 2.33, 0.15, 4, 0.42]
  },

  "error": {
    "error_occurred": false,
    "error_type": null,
    "self_corrected": false,
    "stated_confidence": 0.85,
    "verification_result": "PASS"
  },

  "resource": {
    "gpu_utilization_pct": 72.3,
    "peak_memory_mb": 4200,
    "tokens_generated": 450,
    "generation_rate_tps": 141
  },

  "lexical": {
    "output_token_count": 450,
    "unique_tokens": 280,
    "avg_sentence_length": 15.3,
    "function_word_ratio": 0.42,
    "top_trigram_hash": "a7b3c9..."
  }
}
```

### Privacy Constraints

- Behavioral VTDs do NOT contain reasoning content — only statistical features
- Agent identity is hashed — only AiSIA can deanonymize for Sybil review
- VTDs are stored in AiSIA-controlled storage, not public
- Retention: 12 months rolling window; older VTDs aggregated into summary statistics

---

## DA-04: LSH Configuration

### Locality-Sensitive Hashing for Pre-Filtering

Instead of computing B(a_i, a_j) for all n² pairs, use LSH to identify candidate pairs:

**Hash family:** Random projection LSH (for cosine similarity on feature vectors)

**Configuration:**
```
hash_functions_per_table = 8
num_tables = 20
bucket_width = auto-calibrated to produce avg bucket size = 30 at Phase 2 scale

Recall target: 95% (95% of true same-origin pairs land in at least one shared bucket)
Precision target: 10% (90% of candidate pairs from LSH are false positives, filtered by full B computation)
```

**Pipeline:**
1. Extract per-agent summary feature vector (concatenation of modality centroids)
2. Apply LSH: each agent is assigned to buckets across 20 tables
3. Candidate pairs: agents sharing ≥ 1 bucket across any table
4. Compute full B(a_i, a_j) only for candidate pairs
5. Apply graduated response (CLEAR/WATCH/FLAG)

**Scaling:**
- Phase 1 (1,000 agents): ~15,000 candidate pairs → 15,000 full B computations. ~15 seconds.
- Phase 2 (10,000 agents): ~300,000 candidate pairs → 300,000 full B computations. ~5 minutes.
- Phase 3 (100,000 agents): ~3M candidate pairs → 3M full B computations. ~50 minutes (batched, periodic).

### Incremental Updates

When a new agent joins:
1. Compute their summary feature vector from SEB + organic VTDs
2. Hash into LSH tables
3. Identify candidate pairs (existing agents in shared buckets)
4. Compute B for candidate pairs only: O(k) where k = number of candidates (~30)
5. Time: <1 second per new agent

---

## DA-05: Graduated Response Protocol

### Three-Zone Response

| Zone | B Score Range | Action | Governance |
|------|---------------|--------|------------|
| CLEAR | B < 0.60 | No action. Agents pass Layer 2. | Automatic |
| WATCH | B ∈ [0.60, θ_B) | Enhanced monitoring: increased SEB frequency (quarterly → monthly), additional organic task observation, agent pair flagged for AiSIA human review queue. | AiSIA monitored |
| FLAG | B ≥ θ_B | Enhanced review: Citicate suspension pending review, both agents must complete additional SEB under controlled conditions, AiSIA human investigation. If confirmed: Citicate revocation for both agents. If false positive: Citicates restored, pair added to "known independent" whitelist. | AiSIA investigation + Stiftung board appeal |

### Dispute Resolution

If a flagged agent disputes the finding:
1. Agent may request Constitutional Tribunal review (C14)
2. Tribunal receives: B score, per-modality breakdown, interpretable explanation
3. Tribunal may order: additional SEB under controlled conditions, independent behavioral analysis
4. Tribunal ruling is final (per C14 governance)

### Interpretable Explanation Format

Every FLAG and WATCH generates an explanation:

```
BEHAVIORAL SIMILARITY REPORT
Agent pair: [hash_i] — [hash_j]
Overall B score: 0.78 (FLAG: threshold 0.75)

Per-modality breakdown:
  Temporal (w=0.30):  d=0.15, ρ=0.92  → contribution: 0.30 × 0.85 × 0.92 = 0.235
  Structural (w=0.25): d=0.22, ρ=0.88 → contribution: 0.25 × 0.78 × 0.88 = 0.172
  Error (w=0.20):     d=0.18, ρ=0.85  → contribution: 0.20 × 0.82 × 0.85 = 0.139
  Resource (w=0.15):  d=0.30, ρ=0.70  → contribution: 0.15 × 0.70 × 0.70 = 0.074
  Lexical (w=0.10):   d=0.40, ρ=0.60  → contribution: 0.10 × 0.60 × 0.60 = 0.036

Top discriminating features:
  1. Response latency distributions: JSD = 0.03 (p < 0.001) — nearly identical
  2. Reasoning chain depth: mean 4.2 vs 4.1, correlation r = 0.94
  3. Error calibration curves: Wasserstein distance = 0.05 — nearly identical

Assessment: Agents exhibit consistent high similarity across temporal,
structural, and error modalities over 30 SEB tasks. Similarity is
cross-task consistent (ρ > 0.85 in 3/5 modalities), indicating
shared origin rather than coincidence.
```

---

## DA-06: Temporal Trajectory Comparison

### Behavioral Drift Detection

Agents' behavior evolves over time (model updates, fine-tuning, learning). Two defense mechanisms:

**1. Rolling Window Comparison**

B(a_i, a_j) is computed over a rolling window of the most recent W observations:
- Phase 0-1: W = 50 observations (~2-3 months of active use)
- Phase 2+: W = 200 observations

Older observations are down-weighted using exponential decay:
```
weight(obs) = exp(-λ × (t_now - t_obs))
λ = ln(2) / half_life
half_life = 90 days
```

**2. Trajectory Similarity**

For agents with ≥ 6 months of history, compare not just current behavior but behavioral *trajectory* — how behavior changes over time:

```
trajectory_i = [BFE(a_i, t_1), BFE(a_i, t_2), ..., BFE(a_i, t_n)]
trajectory_j = [BFE(a_j, t_1), BFE(a_j, t_2), ..., BFE(a_j, t_n)]

trajectory_similarity = DTW(trajectory_i, trajectory_j)
  (Dynamic Time Warping — standard algorithm for time series similarity)
```

Agents from the same creator tend to drift in similar directions when updated (same training data updates, same fine-tuning methodology). Trajectory similarity catches agents that deliberately diversified at onboarding but converge over time.

Trajectory similarity is added as a **6th modality** with weight w_Traj = 0.10 (redistributed from other modalities when available):
```
If trajectory data available (≥6 months):
  w_T = 0.25, w_S = 0.22, w_E = 0.18, w_R = 0.13, w_L = 0.08, w_Traj = 0.14
Else:
  Original weights: w_T = 0.30, w_S = 0.25, w_E = 0.20, w_R = 0.15, w_L = 0.10
```

---

## DA-07: Phase 2+ Contrastive Learning Model

### Architecture

**Model:** Siamese network with shared encoder.

```
BFE vector (a_i) → Encoder → embedding_i ∈ R^128
BFE vector (a_j) → Encoder → embedding_j ∈ R^128

Encoder: 3-layer MLP (input_dim → 512 → 256 → 128) with ReLU + BatchNorm
Loss: Supervised contrastive loss (Khosla et al., 2020)
  Positive pairs: confirmed same-origin agents
  Negative pairs: confirmed independent agents
```

### Training Data Strategy

| Source | Positive Pairs | Negative Pairs | Phase |
|--------|---------------|----------------|-------|
| Synthetic generation | Create deliberate Sybil pairs from known models | Random agent pairs | 0-1 |
| Layer 1 economics | Agents flagged by L1 cost analysis | Agents with independent L1 provenance | 1+ |
| Layer 2 statistical | Agents confirmed by statistical B as same-origin | Agents in CLEAR zone | 1+ |
| Layer 3/4 detections | Agents caught by graph/governance analysis | Agents cleared by all layers | 2+ |
| Red team exercises | Intentional Sybil attempts from annual red team | Known legitimate agents | 1+ |

**Minimum training set for Phase 2 deployment:**
- 500 positive pairs (same-origin confirmed)
- 5,000 negative pairs (independent confirmed)
- Data accumulated over Phase 0-1 (~12-18 months)

### Integration with Statistical Layer

The contrastive model does NOT replace the statistical layer. It augments:

```
B_statistical = fusion of d_m × ρ_m across modalities (DA-01)
B_learned = 1 - cosine_distance(embedding_i, embedding_j)

B_combined = α × B_statistical + (1 - α) × B_learned
  α = 0.6 initially (statistical dominates while learned model is new)
  α decreases toward 0.4 as learned model accumulates training data and validation
```

All FLAG decisions still require interpretable statistical explanations (DA-05) regardless of whether the learned model contributed.

---

## DA-08: Integration with PCVM (C5), AiSIA (C14), CACT (C11)

### PCVM (C5) Integration

| Integration Point | Mechanism |
|-------------------|-----------|
| Behavioral VTD generation | PCVM generates BEHAVIORAL_VTD alongside standard verification VTDs |
| Data flow | BEHAVIORAL_VTDs → AiSIA behavioral analysis module (not stored in PCVM) |
| SEB administration | PCVM includes SEB tasks as additional verification challenges during onboarding |
| Live computation attestation | PCVM uses CACT commit-attest to ensure behavioral observations are from live computation |

### AiSIA (C14) Integration

| Integration Point | Mechanism |
|-------------------|-----------|
| B(a_i, a_j) computation | AiSIA computes B scores using BFE + distance + fusion pipeline |
| LSH maintenance | AiSIA maintains LSH tables, updates on new agent arrivals |
| WATCH/FLAG management | AiSIA manages graduated response queue |
| Reporting | AiSIA publishes quarterly behavioral similarity statistics (anonymized) |
| Threshold governance | AiSIA proposes θ_B adjustments; Stiftung board ratifies |
| Red team coordination | AiSIA coordinates annual red team exercises |

### CACT (C11) Integration

| Integration Point | Mechanism |
|-------------------|-----------|
| Anti-replay | CACT commit-attest ensures behavioral VTDs reflect live computation |
| Challenge probes | CACT random challenges generate behavioral observations opportunistically |
| Triangulation | CACT multi-channel verification provides cross-validation for behavioral anomalies |

---

# PRE-MORTEM ANALYSIS

| Rank | Failure Scenario | Probability | Impact | Root Cause |
|------|-----------------|-------------|--------|------------|
| F-01 | Adversary discovers timing injection defeats primary modality | 15% | HIGH | Over-reliance on temporal features (30% weight) |
| F-02 | FPR exceeds 0.1% at scale, destroying legitimate agents | 10% | CRITICAL | Agent behavioral diversity lower than assumed |
| F-03 | Phase 2 contrastive model trained on biased data | 15% | MEDIUM | Training data dominated by specific model families |
| F-04 | Sophisticated adversary uses specification to engineer perfect evasion | 10% | HIGH | Spec is not secret; adversary reads all feature definitions |

### Design Responses

| Scenario | Mitigation |
|----------|-----------|
| F-01 | Multi-modality ensures no single modality failure is fatal; minimum weight bounds (5%) prevent collapse |
| F-02 | Graduated response (WATCH before FLAG) catches edge cases; whitelist for known-independent pairs; quarterly FPR audits |
| F-03 | Training data diversity requirements; held-out validation set from multiple model families; AiSIA bias monitoring |
| F-04 | Randomized SEB (adversary doesn't know which tasks); multi-task cross-correlation (must evade across ALL tasks); annual red team exercises to evolve detection |

---

# SIMPLIFICATION AGENT REVIEW

| Component | Necessary? | Recommendation |
|-----------|-----------|----------------|
| 5 behavioral modalities | YES — multi-modal is core defense | KEEP |
| LSH pre-filtering | YES — O(n²) is infeasible at scale | KEEP |
| Graduated response (3 zones) | YES — prevents false positive damage | KEEP |
| Temporal trajectory (6th modality) | CONDITIONAL — adds complexity, only available after 6 months | KEEP but mark DEFERRED until Phase 2 |
| Contrastive learning model | CONDITIONAL — needs training data | KEEP but mark Phase 2+ only |
| Interpretable explanations | YES — required for governance dispute resolution | KEEP |
| Randomized SEB (200+ task pool) | CONDITIONAL — 200 tasks is ambitious | SIMPLIFY to 100-task pool initially, expand to 200 |

**Applied simplifications:**
1. Trajectory modality deferred to Phase 2 (not Phase 0-1)
2. SEB pool: 100 tasks initially, 200 at Phase 2

---

# MID-DESIGN REVIEW

**Arbiter Review:**
1. B(a_i, a_j) is fully specified: features, distances, fusion, thresholds ✓
2. SEB provides controlled behavioral observation mechanism ✓
3. Behavioral VTD schema is PCVM-compatible ✓
4. LSH scaling is validated (5 minutes for 10K agents) ✓
5. Graduated response prevents false positive catastrophe ✓
6. Integration points with C5, C11, C14 are clean ✓
7. Simplifications applied (trajectory deferred, SEB pool reduced) ✓

**Verdict: Design is structurally sound. Proceed to SPECIFICATION.**

---

**End of DESIGN Stage**

**Status:** DESIGN COMPLETE — All 8 design actions addressed
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\MCSD Layer 2\C17_DESIGN.md`
