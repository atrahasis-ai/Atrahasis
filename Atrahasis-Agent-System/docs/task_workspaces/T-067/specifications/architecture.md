# C37 — Epistemic Feedback Fabric (EFF)

## Architecture Specification

| Field | Value |
|---|---|
| **Title** | Epistemic Feedback Fabric (EFF) |
| **Version** | 1.0.0 |
| **Date** | 2026-03-12 |
| **Invention ID** | C37 |
| **Task ID** | T-067 |
| **System** | Atrahasis Agent System v2.4 |
| **Stage** | DESIGN |
| **Normative References** | C5 (PCVM v2.0), C6 (EMA v2.0), C7 (RIF v2.0), C9 (Reconciliation), C17 (MCSD L2 v1.0), C23 (SCR v1.0), C35 (Sentinel v1.0) |
| **Feasibility Conditions** | All 5 satisfied (see Section 1.3) |

---

## Table of Contents

1. [System Overview and Data Flow](#1-system-overview-and-data-flow)
2. [Component Specifications](#2-component-specifications)
   - 2.1 [Verification Feedback Loop (VFL)](#21-verification-feedback-loop-vfl)
   - 2.2 [Reasoning Strategy Catalog (RSC)](#22-reasoning-strategy-catalog-rsc)
   - 2.3 [Complexity-Aware Budget Signals (CABS)](#23-complexity-aware-budget-signals-cabs)
   - 2.4 [Advisory Membrane](#24-advisory-membrane)
3. [Integration Contracts](#3-integration-contracts)
4. [Parameters Table](#4-parameters-table)
5. [C22 Wave Placement](#5-c22-wave-placement)
6. [RSC Pattern Lifecycle](#6-rsc-pattern-lifecycle)
7. [Formal Requirements](#7-formal-requirements)
8. [Risk Analysis](#8-risk-analysis)
9. [Open Questions](#9-open-questions)

---

## 1. System Overview and Data Flow

### 1.1 Architectural Position

EFF occupies a cross-layer advisory position. It is not load-bearing infrastructure — the system functions without it. EFF closes the information lifecycle loop: C5 PCVM verification outcomes currently flow only to C8 DSF for settlement. EFF adds a second consumer that distills verification data into population-level reasoning quality signals and makes them available as voluntary advisory information.

EFF does not verify claims (C5's role), does not prescribe agent internals (forbidden by sovereignty model), and does not enforce adoption of its signals. It is an information service behind an explicit Advisory Membrane.

### 1.2 Data Flow Diagram

```
                          ATRAHASIS CORE
 ┌────────────────────────────────────────────────────────────────────┐
 │                                                                    │
 │  ┌──────────┐          ┌──────────┐          ┌──────────┐         │
 │  │ C7 RIF   │          │ C5 PCVM  │          │ C9 Recon │         │
 │  │ (decomp  │          │ (verify) │          │ (claim   │         │
 │  │  complex)│          │          │          │  weights)│         │
 │  └────┬─────┘          └────┬─────┘          └────┬─────┘         │
 │       │                     │                     │                │
 │       │                     │ VTD stream           │                │
 │       │                     │ (second consumer)    │                │
 │       │                     ▼                     │                │
 │       │    ┌──────────────────────────────┐       │                │
 │       │    │   VFL — Verification          │       │                │
 │       │    │   Feedback Loop               │       │                │
 │       │    │                               │       │                │
 │       │    │  ┌─────────┐  ┌──────────┐   │       │                │
 │       │    │  │Anonymizer│  │Aggregator│   │       │                │
 │       │    │  │ k=10 +   │─►│Hierarchic│   │       │                │
 │       │    │  │ DP noise │  │Bayesian  │   │       │                │
 │       │    │  └─────────┘  └────┬─────┘   │       │                │
 │       │    │                    │          │       │                │
 │       │    │  ┌─────────────────▼────────┐ │       │                │
 │       │    │  │ Per-Class Quality Metrics │ │       │                │
 │       │    │  │ + Anomaly Detector       │ │       │                │
 │       │    │  │   (chi-squared, p<0.01)  │ │       │                │
 │       │    │  └────────┬────────────────┘ │       │                │
 │       │    └───────────┼──────────────────┘       │                │
 │       │                │                          │                │
 │       │         ┌──────┴───────┐                  │                │
 │       │         │              │                  │                │
 │       │         ▼              ▼                  │                │
 │       │   ┌──────────┐  ┌──────────┐             │                │
 │       │   │   RSC    │  │  CABS    │◄────────────┘                │
 │       │   │ Reasoning│  │ Budget   │◄────────────────────┐        │
 │       │   │ Strategy │  │ Advisory │                     │        │
 │       │   │ Catalog  │  │ Signals  │                     │        │
 │       │   │ (in C6   │  └────┬─────┘                     │        │
 │       │   │  EMA)    │       │                            │        │
 │       │   └────┬─────┘       │                            │        │
 │       │        │             │                            │        │
 │       │        │             ▼                            │        │
 │       │        │      ┌──────────┐                       │        │
 │       │        │      │ C23 SCR  │                       │        │
 │       │        │      │ Exec     │                       │        │
 │       │        │      │ Lease    │      ┌─────────┐      │        │
 │       │        │      │ +optional│      │ C7 RIF  │──────┘        │
 │       │        │      │ advisory │      │ decomp  │               │
 │       │        │      └────┬─────┘      │complexity│              │
 │       │        │           │            └─────────┘               │
 │  ┌────┼────────┼───────────┼──────────────────────────────┐       │
 │  │    │  ADVISORY MEMBRANE (information flow boundary)    │       │
 │  │    │        │           │                              │       │
 │  │    │  published   optional                             │       │
 │  │    │  patterns    budget                               │       │
 │  │    │  (pull)      advisory                             │       │
 │  │    │        │     (push on lease)                      │       │
 │  └────┼────────┼───────────┼──────────────────────────────┘       │
 │       │        │           │                                      │
 │       │        ▼           ▼                                      │
 │       │   ┌─────────────────────┐                                 │
 │       │   │    SOVEREIGN AGENTS  │  consume voluntarily           │
 │       │   │    (black boxes)     │                                │
 │       │   └──────────┬──────────┘                                 │
 │       │              │                                            │
 │       │              │ produce claims                             │
 │       │              ▼                                            │
 │       │        ┌──────────┐         ┌──────────┐                  │
 │       │        │ C5 PCVM  │────────►│ C8 DSF   │                  │
 │       │        │ (verify) │         │ (settle) │                  │
 │       │        └──────────┘         └──────────┘                  │
 │       │                                                           │
 │  ┌────┼───────────────────────────────────────────┐               │
 │  │    │  DATA SEGREGATION BOUNDARY                │               │
 │  │    │                                           │               │
 │  │    │   RSC consumption   ──X──►  C17 MCSD      │               │
 │  │    │   logs                      (no read      │               │
 │  │    │                              access)      │               │
 │  │    │   RSC consumption   ──X──►  C35 Sentinel  │               │
 │  │    │   logs                      (no read      │               │
 │  │    │                              access)      │               │
 │  │    │                                           │               │
 │  │    │   RSC published     ──────►  C17 MCSD     │               │
 │  │    │   patterns                  (whitelist    │               │
 │  │    │                              for B(a,a))  │               │
 │  └────┼───────────────────────────────────────────┘               │
 │       │                                                           │
 └───────┼───────────────────────────────────────────────────────────┘
         │
    Feedback loop closes:
    better reasoning → higher verification rates → updated VFL metrics
```

### 1.3 Feasibility Condition Satisfaction

| # | Condition | Satisfaction |
|---|---|---|
| 1 | RSC v1.0 restricted to declarative decompositions, anti-patterns, checklists | Section 2.2 — three format types only |
| 2 | CABS must recommend (min, recommended, max) ranges with strategy labels | Section 2.3 — range format with confidence |
| 3 | Advisory Membrane must include RSC-aware baseline adjustment for C17 | Section 2.4, Section 3.4 — whitelist protocol |
| 4 | Specification must explicitly acknowledge voluntariness paradox | Section 2.4.4 |
| 5 | Pattern diversity monitoring must be specified | Section 2.2.6 |

### 1.4 Temporal Alignment

EFF operates on the canonical three-tier temporal hierarchy:

| Tier | Name | Duration | EFF Usage |
|---|---|---|---|
| T-1 | `SETTLEMENT_TICK` | 60 s | VTD ingestion (continuous) |
| T-2 | `TIDAL_EPOCH` | 3,600 s (1 h) | RSC credibility updates, CABS recalibration |
| T-3 | `CONSOLIDATION_CYCLE` | 36,000 s (10 h) | VFL metric publication (normal cadence), RSC pattern lifecycle transitions |

---

## 2. Component Specifications

### 2.1 Verification Feedback Loop (VFL)

#### 2.1.1 Purpose

VFL aggregates C5 PCVM verification outcomes into population-level, per-claim-class quality metrics while preserving individual agent privacy. It is the only new runtime component introduced by EFF.

#### 2.1.2 VTD Ingestion

VFL subscribes to the C5 VTD output stream as a second consumer (alongside C8 DSF). For each completed VTD, VFL extracts:

| Field | Source in VTD Envelope | Purpose |
|---|---|---|
| `assigned_class` | `vtd.assigned_class` | Claim class categorization |
| `tier` | `vtd.tier` | Verification tier (FORMAL_PROOF / STRUCTURED_EVIDENCE / STRUCTURED_ATTESTATION) |
| `producing_agent` | `vtd.producing_agent` | For k-anonymity grouping; discarded after aggregation |
| `epoch` | `vtd.epoch` | Temporal binning |
| `verdict` | Derived from verification outcome | ACCEPTED / REJECTED / WEAKENED |
| `premises_count` | `len(vtd.proof_body.premises)` or equivalent | Reasoning complexity signal |
| `reasoning_steps_count` | `len(vtd.proof_body.reasoning_chain)` or equivalent | Reasoning depth signal |
| `failure_mode` | Derived from rejection reason (if rejected) | Common failure categorization |
| `probe_outcome` | From CACT extension if present | Adversarial probing result |

VFL MUST NOT store raw VTD content. Only the extracted fields above are retained, and `producing_agent` is discarded after the aggregation window closes.

#### 2.1.3 Privacy-Preserving Aggregation

Three-layer privacy defense:

**Layer 1 — k-Anonymity Floor (k = VFL_K_ANONYMITY_FLOOR, default 10)**

Statistics are computed only when the contributing agent set for a given claim class within the aggregation window contains at least k distinct agents. If fewer than k agents contributed to a class, the class statistics are suppressed for that window.

```python
def k_anonymity_check(records: list[VTDExtract], claim_class: str, k: int) -> bool:
    """Returns True if at least k distinct agents contributed to this class."""
    agents = set(r.producing_agent for r in records if r.assigned_class == claim_class)
    return len(agents) >= k
```

**Layer 2 — Differential Privacy (epsilon = VFL_EPSILON)**

After aggregation, Laplace noise is added to all published counts and rates:

```python
def dp_noise(true_value: float, sensitivity: float, epsilon: float) -> float:
    """Add calibrated Laplace noise for epsilon-differential privacy."""
    scale = sensitivity / epsilon
    noise = numpy.random.laplace(0, scale)
    return true_value + noise

# For acceptance rate (sensitivity = 1/n where n is sample size):
noisy_rate = dp_noise(acceptance_rate, sensitivity=1.0/n, epsilon=VFL_EPSILON)
```

VFL_EPSILON is a constitutional parameter — changes require G-class consensus per C3 governance model.

**Layer 3 — Secure Aggregation**

Agent identifiers are processed within a secure aggregation boundary. The aggregation service receives VTD extracts, computes per-class statistics, applies DP noise, and publishes only aggregate results. No per-agent data leaves the aggregation boundary.

```
VTD extracts ──► [Secure Aggregation Boundary] ──► Aggregate metrics only
                  │                              │
                  │ agent_id used for:           │
                  │  - k-anonymity counting      │
                  │  - deduplication              │
                  │ agent_id DISCARDED after      │
                  │   window close                │
                  └──────────────────────────────┘
```

#### 2.1.4 Per-Claim-Class Quality Metrics

For each of the 9 canonical claim classes (D, C, P, R, E, S, K, H, N), VFL publishes:

| Metric | Type | Description |
|---|---|---|
| `acceptance_rate` | float [0,1] | Fraction of claims accepted (with DP noise) |
| `rejection_rate` | float [0,1] | Fraction of claims rejected (with DP noise) |
| `weakened_rate` | float [0,1] | Fraction of claims weakened during probing |
| `failure_mode_distribution` | map[string, float] | Top-5 failure modes with relative frequencies |
| `premises_count_stats` | {p25, p50, p75, p90} | Quartile distribution of premise counts for accepted claims |
| `reasoning_steps_stats` | {p25, p50, p75, p90} | Quartile distribution of reasoning steps for accepted claims |
| `sample_size` | int | Number of observations in the window (with DP noise) |
| `confidence_interval` | (float, float) | 95% CI for acceptance rate |

**Minimum sample size enforcement:** Per-class metrics are published only when `n >= VFL_MIN_SAMPLE` (default 50). This is stricter than the k-anonymity floor and prevents noisy statistics from misleading consumers.

#### 2.1.5 Hierarchical Bayesian Estimation for Rare Classes

Classes with low claim volume (particularly K, H, N) may not reach VFL_MIN_SAMPLE within a single CONSOLIDATION_CYCLE. VFL uses hierarchical Bayesian estimation (James-Stein shrinkage) to borrow strength across related classes:

```python
class HierarchicalEstimator:
    """
    Hierarchical Bayesian estimation for claim class acceptance rates.
    Borrows strength across classes within the same verification tier.
    """

    # Tier groupings (from C5 Section 5)
    TIER_GROUPS = {
        "FORMAL_PROOF": ["D", "C"],
        "STRUCTURED_EVIDENCE": ["E", "S", "P", "R", "K"],
        "STRUCTURED_ATTESTATION": ["H", "N"]
    }

    def estimate(self, class_data: dict[str, ClassStats]) -> dict[str, float]:
        """
        For each class, compute a shrinkage estimator that pulls
        low-sample classes toward the tier mean.

        shrunk_rate = lambda * class_rate + (1 - lambda) * tier_rate

        where lambda = n_class / (n_class + kappa)
        kappa calibrated so that classes with n >= VFL_MIN_SAMPLE
        get lambda >= 0.8 (dominated by own data).
        """
        estimates = {}
        for tier, classes in self.TIER_GROUPS.items():
            tier_rate = self._compute_tier_rate(classes, class_data)
            for cls in classes:
                n = class_data[cls].sample_size
                kappa = VFL_MIN_SAMPLE / 4  # calibration constant
                lam = n / (n + kappa)
                estimates[cls] = lam * class_data[cls].raw_rate + (1 - lam) * tier_rate
        return estimates
```

When a class has fewer than VFL_MIN_SAMPLE observations, its published acceptance rate carries a `shrinkage_applied: true` flag and the shrinkage weight `lambda` is included for transparency.

#### 2.1.6 Dual-Cadence Publication

**Normal cadence:** VFL publishes per-class quality metrics once per CONSOLIDATION_CYCLE (36,000 s / 10 hours). This aligns with C6 EMA's consolidation schedule, ensuring RSC patterns can update credibility based on fresh VFL data.

**Anomaly-triggered cadence:** VFL runs a chi-squared goodness-of-fit test on the per-class acceptance rate distribution at every TIDAL_EPOCH (3,600 s / 1 hour). If the test rejects the null hypothesis (that the current epoch's distribution matches the rolling 10-cycle baseline) at p < VFL_ANOMALY_P_THRESHOLD (default 0.01), an anomaly-triggered publication is emitted immediately.

```python
def anomaly_check(current_epoch: EpochStats, baseline: RollingBaseline) -> bool:
    """
    Chi-squared test: does the current epoch's per-class distribution
    deviate significantly from the rolling baseline?
    """
    observed = [current_epoch.counts[cls] for cls in CLAIM_CLASSES]
    expected = [baseline.expected_counts[cls] for cls in CLAIM_CLASSES]

    # Suppress classes with expected < 5 (chi-squared validity requirement)
    valid = [(o, e) for o, e in zip(observed, expected) if e >= 5]
    if len(valid) < 3:
        return False  # insufficient data for meaningful test

    chi2_stat = sum((o - e)**2 / e for o, e in valid)
    df = len(valid) - 1
    p_value = 1 - chi2_cdf(chi2_stat, df)

    return p_value < VFL_ANOMALY_P_THRESHOLD
```

Anomaly-triggered publications carry the `anomaly_trigger: true` flag with the chi-squared statistic and p-value for downstream consumers.

#### 2.1.7 VFL Output Schema

```json
{
  "$id": "https://eff.atrahasis.dev/schema/v1/vfl-publication.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "VFL Quality Metrics Publication",
  "type": "object",
  "required": ["publication_id", "publication_type", "window_start",
               "window_end", "epoch_range", "class_metrics", "metadata"],
  "properties": {
    "publication_id": {
      "type": "string",
      "pattern": "^vfl:pub:[0-9]+:[a-f0-9]{8}$"
    },
    "publication_type": {
      "type": "string",
      "enum": ["SCHEDULED", "ANOMALY_TRIGGERED"]
    },
    "window_start": { "type": "string", "format": "date-time" },
    "window_end": { "type": "string", "format": "date-time" },
    "epoch_range": {
      "type": "object",
      "properties": {
        "first_epoch": { "type": "integer" },
        "last_epoch": { "type": "integer" }
      }
    },
    "class_metrics": {
      "type": "object",
      "patternProperties": {
        "^[DCPRESKHM]$": {
          "$ref": "#/$defs/ClassMetrics"
        }
      }
    },
    "anomaly_trigger": {
      "type": "object",
      "properties": {
        "triggered": { "type": "boolean" },
        "chi_squared_stat": { "type": "number" },
        "p_value": { "type": "number" },
        "deviating_classes": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "epsilon_used": { "type": "number" },
        "k_anonymity_floor": { "type": "integer" },
        "min_sample_size": { "type": "integer" },
        "suppressed_classes": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "$defs": {
    "ClassMetrics": {
      "type": "object",
      "required": ["acceptance_rate", "rejection_rate", "sample_size"],
      "properties": {
        "acceptance_rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "rejection_rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "weakened_rate": { "type": "number", "minimum": 0, "maximum": 1 },
        "failure_mode_distribution": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        },
        "premises_count_stats": { "$ref": "#/$defs/QuartileStats" },
        "reasoning_steps_stats": { "$ref": "#/$defs/QuartileStats" },
        "sample_size": { "type": "integer", "minimum": 0 },
        "confidence_interval": {
          "type": "array", "items": { "type": "number" },
          "minItems": 2, "maxItems": 2
        },
        "shrinkage_applied": { "type": "boolean", "default": false },
        "shrinkage_lambda": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "QuartileStats": {
      "type": "object",
      "properties": {
        "p25": { "type": "number" },
        "p50": { "type": "number" },
        "p75": { "type": "number" },
        "p90": { "type": "number" }
      }
    }
  }
}
```

---

### 2.2 Reasoning Strategy Catalog (RSC)

#### 2.2.1 Purpose

RSC is a published library of proven reasoning patterns, stored as C6 EMA epistemic quanta with type `reasoning_strategy`. Agents may voluntarily query the catalog. RSC does not prescribe how to reason — it publishes what reasoning patterns historically correlate with successful verification.

#### 2.2.2 Format Types (v1.0 Restriction)

RSC v1.0 supports exactly three format types. This restriction is a feasibility condition (Condition 1) driven by the Science Assessment's finding that model-agnostic patterns are feasible only for declarative formats.

| Format Type | Description | Example |
|---|---|---|
| `declarative_decomposition` | A structured breakdown of what verification expects for a claim class. Describes the logical components of a successful claim. | "For R-class: premises, logical validity, evidence support, scope coverage, counter-evidence consideration" |
| `anti_pattern` | A description of a reasoning pattern that correlates with verification failure. Does not prescribe avoidance strategy — describes the observable anti-pattern. | "Circular evidence chains: claims citing derivative sources that trace back to the original claim. Rejected at 3x baseline rate." |
| `verification_checklist` | A list of checkpoints that successful claims in a class typically satisfy. Structured as boolean predicates. | "E-class checklist: source accessible? source authoritative? quote found? quote supports claim? counter-evidence addressed?" |

Explicitly NOT supported in v1.0:
- Prompt templates
- Chain-of-thought prescriptions
- Internal representation guidance
- Architecture-specific optimizations

#### 2.2.3 RSC as Epistemic Quanta

RSC patterns are stored as C6 EMA epistemic quanta with the following field mappings:

| EQ Field | RSC Mapping |
|---|---|
| `id` | UUID v4 (standard EQ identifier) |
| `content` | `StructuredClaim` with `type: "reasoning_strategy"` and the pattern payload |
| `opinion` | Subjective logic tuple tracking pattern credibility (see 2.2.4) |
| `provenance` | Derivation chain: VFL metrics → pattern extraction → curation |
| `edges` | DERIVATION edges to source VFL publications; ANALOGY edges to related patterns |
| `metabolic_state` | Standard EQ lifecycle (see Section 6) |
| `projections` | None (RSC patterns are consumed directly, not projected) |
| `timestamps` | Standard EQ temporal tracking |
| `dissolution_record` | Standard (if dissolved) |
| `claim_class` | The claim class this pattern applies to (D/C/P/R/E/S/K/H/N) |

RSC pattern content schema:

```json
{
  "type": "reasoning_strategy",
  "format": "declarative_decomposition | anti_pattern | verification_checklist",
  "applies_to_class": "D | C | P | R | E | S | K | H | N",
  "applies_to_tier": "FORMAL_PROOF | STRUCTURED_EVIDENCE | STRUCTURED_ATTESTATION",
  "title": "string (human-readable pattern name)",
  "description": "string (full pattern description)",
  "body": {
    // Format-specific content:
    // declarative_decomposition: { "components": [...] }
    // anti_pattern: { "pattern": "...", "failure_rate_multiplier": float, "indicators": [...] }
    // verification_checklist: { "checkpoints": [{ "predicate": "...", "weight": float }] }
  },
  "source_vfl_publications": ["vfl:pub:..."],
  "version": "string (semver)",
  "architecture_applicability": "universal | llm_preferred",
  "seed_pattern": "boolean (true if manually curated, not derived from VFL)"
}
```

#### 2.2.4 Credibility Tracking via Subjective Logic

Each RSC pattern carries a subjective logic opinion tuple (b, d, u, a) tracking its credibility:

```python
@dataclass
class RSCCredibility:
    """
    Subjective logic opinion for an RSC pattern.

    - b: belief that the pattern improves verification success
    - d: disbelief (evidence that the pattern does NOT help)
    - u: uncertainty (insufficient evidence)
    - a: base rate (prior probability that a random pattern helps)

    Constraint: b + d + u = 1, 0 <= a <= 1
    """
    b: float
    d: float
    u: float
    a: float = 0.5  # uninformative prior

    def projected_probability(self) -> float:
        return self.b + self.a * self.u


# New patterns start with high uncertainty (Feasibility Condition):
RSC_INITIAL_OPINION = RSCCredibility(
    b=0.10,    # minimal initial belief
    d=0.05,    # minimal initial disbelief
    u=0.85,    # high uncertainty (>= RSC_INITIAL_UNCERTAINTY = 0.70)
    a=0.50     # uninformative base rate
)

# Seed patterns (manually curated) start with moderate uncertainty:
RSC_SEED_OPINION = RSCCredibility(
    b=0.30,
    d=0.05,
    u=0.65,
    a=0.50
)
```

**Credibility update mechanism:** At each TIDAL_EPOCH, RSC patterns are evaluated against the latest VFL data. For claim class C with pattern P:

1. Compute the acceptance rate for agents who queried pattern P before submitting C-class claims (from advisory consumption logs, within the secure aggregation boundary).
2. Compare against the population acceptance rate for the same class.
3. If the pattern-consulting cohort has a higher acceptance rate, increase b (via cumulative fusion with positive evidence opinion).
4. If lower, increase d (via cumulative fusion with negative evidence opinion).
5. If insufficient data (< 20 observations in either cohort), increase u slightly.

**Important:** The acceptance rate comparison is computed WITHIN the secure aggregation boundary. Only the resulting opinion update leaves the boundary. C17 and C35 never see which agents consulted which patterns.

#### 2.2.5 Cold-Start: Seed Patterns

At system initialization, RSC begins with manually curated seed patterns. These are authored by the specification team based on:

1. C5 PCVM verification protocol requirements (what constitutes adequate proof per class)
2. C9 reconciliation constraints (cross-layer consistency requirements)
3. Domain expert knowledge of reasoning best practices

Seed patterns are marked `seed_pattern: true` and start with RSC_SEED_OPINION (lower initial uncertainty than derived patterns). They follow the standard RSC lifecycle but receive a grace period of 5 CONSOLIDATION_CYCLEs before credibility-based catabolism evaluation.

Recommended minimum seed set:

| Claim Class | Seed Patterns |
|---|---|
| D (Deterministic) | 1 decomposition, 1 checklist |
| C (Compliance) | 1 decomposition, 1 checklist |
| P (Process) | 1 decomposition, 1 anti-pattern |
| R (Reasoning) | 2 decompositions, 2 anti-patterns, 1 checklist |
| E (Empirical) | 1 decomposition, 1 anti-pattern, 1 checklist |
| S (Statistical) | 1 decomposition, 1 anti-pattern, 1 checklist |
| K (Knowledge) | 1 decomposition, 1 checklist |
| H (Heuristic) | 1 decomposition, 2 anti-patterns |
| N (Normative) | 1 decomposition, 1 anti-pattern |

Total: ~27 seed patterns. R-class receives extra coverage because it is Tier 2 with the highest volume and the most complex verification protocol.

#### 2.2.6 Pattern Diversity Monitoring

RSC MUST monitor population structural convergence to prevent reasoning monoculture (Feasibility Condition 5).

**Convergence metric:** For each claim class, compute the structural similarity of VTD reasoning chains submitted in the current CONSOLIDATION_CYCLE. If the mean pairwise structural similarity exceeds RSC_CONVERGENCE_THRESHOLD (needs calibration — initial target: 0.70), a diversity alert is raised.

```python
def monitor_convergence(vtds: list[VTDExtract], claim_class: str) -> ConvergenceReport:
    """
    Monitor structural convergence of reasoning patterns for a claim class.
    Uses VFL's copy of VTD structural data (not raw VTDs).
    """
    class_vtds = [v for v in vtds if v.assigned_class == claim_class]
    if len(class_vtds) < 30:
        return ConvergenceReport(status="INSUFFICIENT_DATA")

    # Extract structural fingerprints (reasoning step topology)
    fingerprints = [extract_structure(v) for v in class_vtds]

    # Compute mean pairwise similarity (sample if n > 200)
    if len(fingerprints) > 200:
        fingerprints = random.sample(fingerprints, 200)

    pairs = list(itertools.combinations(fingerprints, 2))
    mean_sim = sum(structural_similarity(a, b) for a, b in pairs) / len(pairs)

    if mean_sim > RSC_CONVERGENCE_THRESHOLD:
        return ConvergenceReport(
            status="CONVERGENCE_ALERT",
            mean_similarity=mean_sim,
            threshold=RSC_CONVERGENCE_THRESHOLD,
            recommendation="Publish alternative patterns; flag dominant pattern for review"
        )

    return ConvergenceReport(status="HEALTHY", mean_similarity=mean_sim)
```

**Response to convergence alert:**
1. Flag the dominant RSC pattern(s) for the affected class.
2. Increase the visibility of alternative patterns in catalog queries.
3. Consider minting new patterns from the minority reasoning structures in VFL data.
4. Do NOT suppress or remove the convergent pattern — agents chose it voluntarily.

---

### 2.3 Complexity-Aware Budget Signals (CABS)

#### 2.3.1 Purpose

CABS provides optional reasoning budget recommendations on C23 SCR ExecutionLease objects. These signals suggest how much reasoning effort (measured in tokens/steps) is likely to be useful for a given task, based on claim class, decomposition complexity, and historical verification data.

CABS does not constrain agents. It annotates leases with advisory information.

#### 2.3.2 Advisory Object Schema

```json
{
  "$id": "https://eff.atrahasis.dev/schema/v1/reasoning-budget-advisory.schema.json",
  "title": "Reasoning Budget Advisory",
  "type": "object",
  "required": ["min_sufficient", "recommended", "max_useful",
               "strategy_label", "confidence"],
  "properties": {
    "min_sufficient": {
      "type": "integer",
      "minimum": 0,
      "description": "Minimum reasoning budget (tokens/steps) at which acceptable quality is achievable for this task class."
    },
    "recommended": {
      "type": "integer",
      "minimum": 0,
      "description": "Recommended reasoning budget — the CABS_CALIBRATION_PERCENTILE of successful claims for this class."
    },
    "max_useful": {
      "type": "integer",
      "minimum": 0,
      "description": "Budget beyond which additional reasoning effort shows no marginal quality improvement (non-monotonic budget-performance ceiling)."
    },
    "strategy_label": {
      "type": "string",
      "description": "Human-readable label for the recommended approach, referencing RSC pattern if applicable.",
      "examples": ["decompose-then-verify", "evidence-chain-first", "counter-evidence-sweep"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Confidence in this recommendation. Low confidence indicates sparse historical data."
    },
    "source_components": {
      "type": "object",
      "description": "Provenance of this recommendation.",
      "properties": {
        "claim_class_weight": { "type": "number" },
        "rif_complexity_score": { "type": "number" },
        "vfl_calibration_percentile": { "type": "integer" },
        "vfl_publication_id": { "type": "string" }
      }
    }
  }
}
```

#### 2.3.3 Budget Computation

CABS computes the advisory from three independent sources, then fuses them:

**Source 1: C9 Claim Class Difficulty Weights**

C9 reconciliation defines per-class difficulty multipliers reflecting verification complexity:

| Class | Weight | Rationale |
|---|---|---|
| D (Deterministic) | 1.0 | Formal proof, well-bounded |
| C (Compliance) | 1.2 | Rule-matching, bounded |
| P (Process) | 1.5 | Multi-step process validation |
| R (Reasoning) | 2.0 | Open-ended logical analysis |
| E (Empirical) | 1.8 | Source verification, factual checking |
| S (Statistical) | 2.0 | Methodology validation |
| K (Knowledge Consolidation) | 2.2 | Cross-source synthesis |
| H (Heuristic) | 2.5 | Judgment-intensive, adversarial probing |
| N (Normative) | 3.0 | Value-laden, committee review |

**Source 2: C7 RIF Decomposition Complexity**

The C7 RIF Parcel Executor produces a decomposition tree for each intent. CABS reads the structural complexity of the leaf intent's position in this tree:

```python
def rif_complexity(intent: Intent) -> float:
    """
    Estimate reasoning complexity from RIF decomposition structure.
    """
    depth = intent.decomposition_depth       # 1-5 typical
    sibling_count = intent.sibling_count     # parallel tasks at this level
    dependency_count = intent.dependency_count # data dependencies

    # Normalized to [0, 1] range
    return min(1.0, (depth * 0.3 + sibling_count * 0.1 + dependency_count * 0.2) / 3.0)
```

**Source 3: VFL Historical Calibration**

From the latest VFL publication, CABS extracts the CABS_CALIBRATION_PERCENTILE (default: 75th) of reasoning_steps_count for accepted claims in the relevant class:

```python
def vfl_calibration(vfl_pub: VFLPublication, claim_class: str) -> int:
    """
    Extract the calibration-percentile reasoning step count
    for accepted claims in this class.
    """
    class_metrics = vfl_pub.class_metrics.get(claim_class)
    if class_metrics is None or class_metrics.sample_size < VFL_MIN_SAMPLE:
        return None  # insufficient data; confidence will be low
    return class_metrics.reasoning_steps_stats.p75  # default percentile


def compute_advisory(claim_class: str, intent: Intent,
                     vfl_pub: VFLPublication) -> ReasoningBudgetAdvisory:
    """
    Fuse three sources into a budget advisory.
    """
    # Source 1: class weight
    class_weight = C9_DIFFICULTY_WEIGHTS[claim_class]
    base_budget = int(BASE_REASONING_TOKENS * class_weight)

    # Source 2: RIF complexity adjustment
    rif_score = rif_complexity(intent)
    rif_adjusted = int(base_budget * (1.0 + rif_score * 0.5))

    # Source 3: VFL calibration
    vfl_p75 = vfl_calibration(vfl_pub, claim_class)

    if vfl_p75 is not None:
        # Weight VFL data heavily when available
        recommended = int(0.4 * rif_adjusted + 0.6 * vfl_p75)
        confidence = min(0.9, vfl_pub.class_metrics[claim_class].sample_size / 500)
    else:
        recommended = rif_adjusted
        confidence = 0.3  # low confidence without VFL data

    # Non-monotonic budget-performance ceiling (from VFL p90)
    vfl_p90 = vfl_pub.class_metrics.get(claim_class, {}).reasoning_steps_stats.p90
    max_useful = vfl_p90 if vfl_p90 else int(recommended * 1.5)

    # Minimum sufficient (from VFL p25)
    vfl_p25 = vfl_pub.class_metrics.get(claim_class, {}).reasoning_steps_stats.p25
    min_sufficient = vfl_p25 if vfl_p25 else int(recommended * 0.4)

    # Strategy label from highest-credibility RSC pattern for this class
    strategy = rsc_best_pattern(claim_class)

    return ReasoningBudgetAdvisory(
        min_sufficient=min_sufficient,
        recommended=recommended,
        max_useful=max_useful,
        strategy_label=strategy.title if strategy else "general",
        confidence=confidence,
        source_components={
            "claim_class_weight": class_weight,
            "rif_complexity_score": rif_score,
            "vfl_calibration_percentile": CABS_CALIBRATION_PERCENTILE,
            "vfl_publication_id": vfl_pub.publication_id
        }
    )
```

#### 2.3.4 Non-Breaking Integration

The `reasoning_budget_advisory` field on C23 ExecutionLease is OPTIONAL:

- Leases without this field continue to work identically to pre-EFF behavior.
- No SCR component reads or enforces the advisory — it is metadata for the agent.
- Agents MAY ignore the advisory entirely. No downstream consequence follows.
- The C23 Execution Evidence Bundle (EEB) MUST NOT record whether the agent followed the advisory.

---

### 2.4 Advisory Membrane

#### 2.4.1 Purpose

The Advisory Membrane is the architectural boundary between EFF's advisory signals and the enforcement/surveillance mechanisms of the Atrahasis stack. It is not a software component — it is an information flow policy enforced through data segregation, access control, and integration contract constraints.

The membrane ensures one invariant: **no enforcement or surveillance system may use EFF advisory consumption data as input.**

#### 2.4.2 Information Flow Controls

**ADVISORY_PRIVATE label:** All RSC consumption logs (which agent queried which pattern, when, how often) are labeled `ADVISORY_PRIVATE`. This label has the following access control semantics:

| Component | Read Access to ADVISORY_PRIVATE | Rationale |
|---|---|---|
| VFL aggregation service | YES (within secure aggregation boundary) | Required for RSC credibility updates |
| RSC catalog service | YES (query routing) | Required for catalog operation |
| C17 MCSD | **NO** | Prevents behavioral similarity weaponization |
| C35 Sentinel | **NO** | Prevents anomaly detection weaponization |
| C5 PCVM | **NO** | Prevents verification bias |
| C8 DSF | **NO** | Prevents economic consequences |
| C7 RIF | **NO** | Prevents orchestration bias |
| C3 Tidal Noosphere | **NO** | Prevents governance consequences |

**Data segregation:** Advisory consumption logs MUST be stored in a physically or logically separate data store from:
- C17 Behavioral VTD storage
- C35 Sentinel metric streams
- C5 VTD storage
- C8 settlement records

The segregation boundary MUST be verifiable by audit.

#### 2.4.3 C17 RSC-Aware Whitelist

The structural side-channel is the highest risk identified by the Science Assessment: agents consuming RSC patterns produce structurally similar reasoning, which C17's structural modality (w_S = 0.25) may detect as shared origin.

**Mitigation: RSC Pattern Whitelist Protocol**

1. Every time an RSC pattern transitions to ACTIVE state (published and credible), its structural fingerprint is added to the C17 RSC whitelist.
2. When C17 computes B(a_i, a_j) structural distance, it applies a discount:

```python
def adjusted_structural_distance(
    s_i: StructuralProfile,
    s_j: StructuralProfile,
    rsc_whitelist: list[StructuralFingerprint]
) -> float:
    """
    Compute structural distance with RSC whitelist discounting.

    Similarity that matches published RSC patterns is expected
    (agents following published guidance) and should not count
    as evidence of shared origin.
    """
    raw_distance = cosine_distance(s_i, s_j)

    # Identify structural features that match whitelisted patterns
    whitelist_overlap_i = compute_whitelist_overlap(s_i, rsc_whitelist)
    whitelist_overlap_j = compute_whitelist_overlap(s_j, rsc_whitelist)

    # Discount: if both agents' structural similarity is explainable
    # by published RSC patterns, reduce the distance weight
    shared_whitelist = whitelist_overlap_i & whitelist_overlap_j
    discount_factor = 1.0 - (len(shared_whitelist) / max(len(rsc_whitelist), 1))

    return raw_distance * discount_factor
```

3. The whitelist is synchronized at every CONSOLIDATION_CYCLE. C17 receives only structural fingerprints of published patterns — not consumption data.

#### 2.4.4 Voluntariness Paradox Acknowledgment

EFF explicitly acknowledges the voluntariness paradox identified by the Science Assessment and Feasibility review:

**Statement of the paradox:** If EFF advisory signals are effective, agents that consume them will achieve higher verification rates and lower inference costs than agents that do not. This performance differential creates market pressure to adopt EFF signals. Over time, non-adoption may become an economic disadvantage. The membrane prevents surveillance-based coercion but cannot prevent performance-based self-selection.

**This is by design.** The same dynamic exists in all effective advisory systems:
- Medical clinical practice guidelines are formally advisory; physicians who consistently ignore them face malpractice exposure.
- Academic peer review norms are voluntary; researchers who ignore them cannot publish.
- Building codes specify performance requirements; builders who ignore them cannot pass inspection.

The membrane's guarantee is narrower and more precise: **no Atrahasis enforcement mechanism will use EFF consumption data as a decision input.** Whether to consume advisory signals is a sovereign agent choice with natural (not enforced) consequences.

**What the membrane prevents:**
- C17 treating pattern consumption as behavioral similarity evidence
- C35 treating non-consumption as an anomaly
- C5 adjusting verification thresholds based on advisory adherence
- C8 adjusting settlement rates based on advisory usage

**What the membrane does NOT prevent:**
- Agents who follow good advice performing better than those who do not
- The market recognizing and rewarding better-performing agents
- De facto adoption norms emerging over time

#### 2.4.5 C35 Explicit Exclusion

C35 Sentinel's three-tier anomaly detection pipeline MUST NOT use advisory consumption as an input feature. Specifically:

1. **Tier 1 (STA/LTA per-agent):** Metric channels MUST NOT include "RSC query frequency" or "CABS adherence ratio."
2. **Tier 2 (PCM pairwise correlation):** Platform covariates for the PCM model MUST NOT include advisory consumption similarity.
3. **Tier 3 (backward tracing):** Source attribution MUST NOT reference RSC patterns as causal explanations for behavioral clusters.

This exclusion is specified as an integration contract (Section 3.5).

---

## 3. Integration Contracts

### 3.1 Contract IC-EFF-01: C5 PCVM → VFL (VTD Second Consumer)

| Field | Value |
|---|---|
| **Provider** | C5 PCVM |
| **Consumer** | EFF VFL |
| **Interface** | VTD output stream subscription |
| **Data** | Completed VTD envelope (read-only) |
| **Latency** | Within 1 SETTLEMENT_TICK of VTD completion |
| **Guarantees** | At-least-once delivery; VFL handles deduplication via vtd_id |
| **Privacy** | VFL extracts only the fields listed in Section 2.1.2; raw VTD content is not retained |
| **Non-interference** | VFL is a passive consumer. It MUST NOT modify VTDs, delay verification, or influence C5 decisions |
| **Failure mode** | If VFL is unavailable, C5 continues normally. VFL catches up from the VTD log on recovery |

**Schema dependency:** VFL depends on the C5 VTD common envelope schema (`vtd-envelope.schema.json` v2). If C5 adds or removes envelope fields, VFL extraction must be updated. VFL MUST NOT depend on `proof_body` internals (class-specific and subject to change).

### 3.2 Contract IC-EFF-02: VFL → C6 EMA (RSC Patterns as Epistemic Quanta)

| Field | Value |
|---|---|
| **Provider** | EFF VFL / RSC pattern extraction |
| **Consumer** | C6 EMA |
| **Interface** | Standard EQ ingestion pipeline |
| **Data** | Epistemic quanta with `content.type = "reasoning_strategy"` |
| **Lifecycle** | RSC quanta follow standard EMA metabolic lifecycle (INGESTED → ACTIVE → DORMANT → QUARANTINED → DISSOLVED) |
| **Credibility** | Initial opinion set by RSC (Section 2.2.4); subsequent updates via standard EMA opinion fusion |
| **Coherence graph** | RSC quanta participate in the coherence graph with DERIVATION edges (to source VFL publications) and ANALOGY edges (to related patterns) |
| **SHREC** | RSC quanta compete for metabolic processing budget under standard SHREC regulation. They are NOT exempt from catabolism |
| **Special:** | RSC quanta with `seed_pattern: true` receive a 5-CONSOLIDATION_CYCLE grace period before catabolism candidacy evaluation |

### 3.3 Contract IC-EFF-03: CABS → C23 SCR (Optional Lease Advisory)

| Field | Value |
|---|---|
| **Provider** | EFF CABS |
| **Consumer** | C23 SCR ExecutionLease |
| **Interface** | Optional `reasoning_budget_advisory` field on ExecutionLease schema |
| **Data** | `ReasoningBudgetAdvisory` object (Section 2.3.2) |
| **Non-breaking** | Leases without this field are valid. No SCR component reads or enforces the advisory |
| **Timing** | CABS populates the advisory at lease creation time (during C7 → C23 handoff) |
| **Update** | The advisory is immutable for the lease lifetime. If conditions change, new leases receive updated advisories |
| **Evidence exclusion** | The C23 Execution Evidence Bundle (EEB) MUST NOT record whether the agent read or followed the advisory |

### 3.4 Contract IC-EFF-04: RSC → C17 MCSD (Published Pattern Whitelist)

| Field | Value |
|---|---|
| **Provider** | EFF RSC |
| **Consumer** | C17 MCSD B(a_i, a_j) computation |
| **Interface** | Structural fingerprint whitelist, synchronized per CONSOLIDATION_CYCLE |
| **Data** | Structural fingerprints of ACTIVE RSC patterns (not consumption data, not full pattern content) |
| **Purpose** | C17 discounts structural similarity that matches published RSC patterns (Section 2.4.3) |
| **Data excluded** | Agent consumption logs, pattern credibility scores, query frequencies |
| **Synchronization** | Pull model: C17 queries the RSC whitelist at the start of each SEB evaluation round |
| **Failure mode** | If RSC whitelist is unavailable, C17 proceeds with un-discounted structural similarity (conservative — may produce false positives) |

### 3.5 Contract IC-EFF-05: C35 Sentinel (Explicit Exclusion)

| Field | Value |
|---|---|
| **Provider** | N/A (exclusion contract) |
| **Consumer** | C35 Sentinel |
| **Interface** | None — this contract specifies what C35 MUST NOT consume |
| **Exclusion** | C35 MUST NOT read, subscribe to, or derive features from: RSC consumption logs, CABS adherence data, advisory query patterns, or any data labeled ADVISORY_PRIVATE |
| **Audit** | The C35 deployment configuration MUST NOT contain connection strings, API endpoints, or data source references to advisory consumption stores |
| **Rationale** | Prevents advisory signals from becoming surveillance inputs |

### 3.6 Contract IC-EFF-06: C17 MCSD (Consumption Data Exclusion)

| Field | Value |
|---|---|
| **Provider** | N/A (exclusion contract) |
| **Consumer** | C17 MCSD |
| **Interface** | None — this contract specifies what C17 MUST NOT consume |
| **Exclusion** | C17 MUST NOT use RSC consumption logs, CABS adherence data, or advisory query patterns as input to B(a_i, a_j) computation or any other behavioral analysis |
| **Permitted** | C17 MAY consume the RSC published pattern whitelist (IC-EFF-04) for structural baseline adjustment |
| **Distinction** | Whitelist = what patterns exist (public). Consumption = who queries them (private) |

---

## 4. Parameters Table

| Parameter | Default | Type | Scope | Governance |
|---|---|---|---|---|
| `VFL_EPSILON` | 2.0 | float (0, inf) | Constitutional | G-class consensus required for change |
| `VFL_K_ANONYMITY_FLOOR` | 10 | int [2, 100] | Operational | Standard parameter change process |
| `VFL_MIN_SAMPLE` | 50 | int [10, 1000] | Operational | Standard parameter change process |
| `VFL_ANOMALY_P_THRESHOLD` | 0.01 | float (0, 0.1) | Operational | Standard parameter change process |
| `VFL_ROLLING_BASELINE_WINDOW` | 10 | int [5, 50] | Operational | Number of CONSOLIDATION_CYCLEs in rolling baseline |
| `VFL_SHRINKAGE_KAPPA` | 12.5 | float (0, 100) | Operational | Calibration constant for hierarchical Bayesian (VFL_MIN_SAMPLE / 4) |
| `RSC_INITIAL_UNCERTAINTY` | 0.70 | float [0.5, 0.95] | Operational | Minimum initial u for new patterns |
| `RSC_SEED_UNCERTAINTY` | 0.65 | float [0.4, 0.90] | Operational | Initial u for seed patterns |
| `RSC_SEED_GRACE_PERIOD` | 5 | int [3, 20] | Operational | CONSOLIDATION_CYCLEs before seed catabolism eligibility |
| `RSC_CONVERGENCE_THRESHOLD` | 0.70 | float [0.5, 0.95] | Operational | Mean pairwise structural similarity alert threshold. **Needs empirical calibration.** |
| `RSC_CONVERGENCE_SAMPLE_SIZE` | 200 | int [50, 500] | Operational | Max sample pairs for convergence computation |
| `RSC_CREDIBILITY_UPDATE_MIN_N` | 20 | int [10, 100] | Operational | Min observations per cohort for credibility update |
| `CABS_CALIBRATION_PERCENTILE` | 75 | int [50, 95] | Operational | Percentile of successful claims for recommended budget |
| `CABS_BASE_REASONING_TOKENS` | 1000 | int [100, 10000] | Operational | Base token budget before class/complexity adjustment |
| `MEMBRANE_AUDIT_INTERVAL` | 10 | int [1, 100] | Operational | CONSOLIDATION_CYCLEs between membrane audit checks |

### Parameter Interactions

| Interaction | Constraint |
|---|---|
| VFL_K_ANONYMITY_FLOOR < VFL_MIN_SAMPLE | Always true (k=10 < min=50). k-anonymity is necessary but not sufficient for publication. |
| VFL_EPSILON and VFL_MIN_SAMPLE | Lower epsilon (stronger privacy) requires larger samples for the same statistical power. At epsilon=1.0, VFL_MIN_SAMPLE should be >= 100. |
| RSC_INITIAL_UNCERTAINTY >= RSC_INITIAL_UNCERTAINTY | Tautology enforced: the parameter itself is the floor. |
| RSC_CONVERGENCE_THRESHOLD + RSC pattern count | If very few patterns exist, convergence is expected and the threshold should be relaxed. |
| CABS_CALIBRATION_PERCENTILE and max_useful | max_useful uses p90 regardless of CABS_CALIBRATION_PERCENTILE; recommended uses the configured percentile. |

---

## 5. C22 Wave Placement

### 5.1 Dependencies

| Dependency | Wave | Rationale |
|---|---|---|
| C5 PCVM operational | Wave 1 | VFL requires VTD stream |
| C6 EMA operational | Wave 2 | RSC stored as epistemic quanta |
| C23 SCR operational | Wave 1 | CABS advisory field on ExecutionLease |
| C7 RIF operational | Wave 1 | CABS reads decomposition complexity |
| C9 reconciliation | Wave 1 | CABS reads claim class difficulty weights |
| C17 MCSD operational | Wave 2 | Advisory Membrane whitelist integration |
| C35 Sentinel operational | Wave 3 | Exclusion contract |

### 5.2 EFF Placement: Wave 2 (with Wave 3 completion)

```
Wave 0: Risk validation experiments
  └── No EFF involvement

Wave 1: Foundation (C5, C23, C7, C8, C9)
  └── EFF prerequisites deployed
  └── CABS schema extension added to C23 (dormant — no data yet)

Wave 2: Coordination (C3, C6, C17)
  └── VFL aggregation service deployed
  └── RSC seed patterns loaded into C6
  └── VFL begins ingesting VTDs and building baseline
  └── RSC credibility tracking begins
  └── CABS begins producing advisories (initially low confidence)
  └── C17 whitelist integration activated

Wave 3: Intelligence (C35)
  └── C35 exclusion contract verified
  └── Advisory Membrane audit capability deployed
  └── Full EFF operational

Wave 4: Defense (C11, C12, C13)
  └── No EFF-specific work

Wave 5: Governance (C14)
  └── No EFF-specific work
```

### 5.3 Maturity Progression

| Wave | EFF Maturity | Description |
|---|---|---|
| Wave 1 | Stub (~10%) | Schema extensions in C23. No runtime. |
| Wave 2 | Functional (~60%) | VFL running, RSC seeded, CABS producing. Low confidence. Membrane enforced for C17. |
| Wave 3 | Hardened (~85%) | C35 exclusion verified. Membrane audit operational. VFL has multi-cycle baseline. RSC patterns accumulating credibility. |
| Wave 4+ | Production (~95%) | Full population data. High-confidence CABS. RSC lifecycle stable. Convergence monitoring calibrated. |

### 5.4 Implementation Effort Estimate

| Component | Effort | Technology |
|---|---|---|
| VFL aggregation service | 3-4 weeks | Rust (aggregation) + Python (statistical computation) |
| VFL privacy layer (DP + k-anonymity) | 2 weeks | Rust |
| RSC storage integration (C6) | 1-2 weeks | Standard EQ ingestion |
| RSC seed pattern authoring | 1 week | Manual curation |
| CABS computation + C23 integration | 2 weeks | Rust + TypeScript (schema) |
| Advisory Membrane (access control, segregation) | 1-2 weeks | Infrastructure |
| C17 whitelist integration | 1 week | Rust |
| Testing (privacy, accuracy, membrane integrity) | 2-3 weeks | TLA+ (2 properties) + integration tests |
| **Total** | **13-18 weeks** | ~1 engineer |

---

## 6. RSC Pattern Lifecycle

### 6.1 State Machine

RSC patterns follow the C6 EMA metabolic lifecycle with RSC-specific transition conditions:

```
                                    ┌─────────────────────────┐
                                    │                         │
            manual curation         │     VFL-derived         │
            (seed patterns)         │     extraction          │
                   │                │                         │
                   ▼                ▼                         │
            ┌─────────────┐                                   │
            │  CANDIDATE  │  (pre-ingestion review)           │
            └──────┬──────┘                                   │
                   │                                          │
                   │ format validation + uniqueness check      │
                   │                                          │
                   ▼                                          │
            ┌─────────────┐                                   │
            │  INGESTED   │  (C6 standard state)              │
            └──────┬──────┘                                   │
                   │                                          │
                   │ initial opinion assigned                  │
                   │ (RSC_INITIAL_OPINION or RSC_SEED_OPINION) │
                   │                                          │
                   ▼                                          │
            ┌─────────────┐                                   │
            │   ACTIVE    │  (published, queryable)           │
            │             │                                   │
            │ credibility │◄──────────────────────────────────┘
            │ updated per │   (reactivation from DORMANT)
            │ TIDAL_EPOCH │
            └──┬───┬───┬──┘
               │   │   │
    ┌──────────┘   │   └──────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌──────────┐  ┌────────────┐
│DORMANT │  │  SUPER-  │  │QUARANTINED │
│        │  │  SEDED   │  │            │
│(low    │  │          │  │(credibility│
│access) │  │(newer    │  │ below      │
│        │  │version   │  │ threshold) │
│        │  │exists)   │  │            │
└───┬────┘  └────┬─────┘  └──────┬─────┘
    │            │               │
    │ reactivate │               │ re-evaluation
    │ (access    │               │ (new evidence)
    │  resumes)  │               │
    │            │               ├──► ACTIVE (if credibility recovers)
    │            │               │
    │            ▼               ▼
    │       ┌──────────┐  ┌──────────┐
    │       │DISSOLVED │  │DISSOLVED │
    │       └──────────┘  └──────────┘
    │
    └──► QUARANTINED (if credibility decays during dormancy)
```

### 6.2 State Descriptions

| State | Entry Condition | Behavior | Exit Condition |
|---|---|---|---|
| **CANDIDATE** | Pattern extracted from VFL or manually authored | Awaiting format validation and uniqueness check. Not visible to agents. | Passes validation → INGESTED. Fails → discarded. |
| **INGESTED** | CANDIDATE passes validation | C6 standard: initial opinion assigned, provenance recorded, edges formed. | Standard C6 INGESTED → ACTIVE transition. |
| **ACTIVE** | INGESTED processing complete | Published in RSC catalog. Queryable by agents. Credibility updated each TIDAL_EPOCH. Structural fingerprint exported to C17 whitelist. | Low access → DORMANT. Superseded → SUPERSEDED. Low credibility → QUARANTINED. |
| **DORMANT** | Access frequency below DORMANT_THRESHOLD for 3 consecutive CONSOLIDATION_CYCLEs | Excluded from RSC query results (but not deleted). Credibility frozen. Removed from C17 whitelist. | Access resumes → ACTIVE. Credibility decays → QUARANTINED. |
| **SUPERSEDED** | A newer version of this pattern enters ACTIVE state | Remains queryable (for backward compatibility) but flagged as superseded. Not included in default query results. Removed from C17 whitelist. | After 5 CONSOLIDATION_CYCLEs with zero queries → DISSOLVED. |
| **QUARANTINED** | Credibility opinion drops below QUARANTINE_THRESHOLD (projected probability < 0.40) OR convergence alert names this pattern as dominant | Under review. Not queryable. Removed from C17 whitelist. | Re-evaluation with new VFL data shows recovery → ACTIVE. 3 CONSOLIDATION_CYCLEs in QUARANTINED without recovery → DISSOLVED. |
| **DISSOLVED** | Terminal: QUARANTINED timeout, or SUPERSEDED with zero queries | Pattern content removed. Provenance and dissolution record retained per C6 standard. C17 whitelist entry removed. | None (terminal state). |

### 6.3 Transition Guards

```python
class RSCLifecycleGuard:
    """Guards for RSC pattern state transitions."""

    def can_quarantine(self, pattern: RSCPattern) -> bool:
        """ACTIVE → QUARANTINED requires credibility below threshold."""
        pp = pattern.opinion.projected_probability()
        if pattern.seed_pattern and pattern.active_cycles < RSC_SEED_GRACE_PERIOD:
            return False  # seed grace period
        return pp < 0.40  # QUARANTINE_THRESHOLD

    def can_reactivate_from_quarantine(self, pattern: RSCPattern) -> bool:
        """QUARANTINED → ACTIVE requires credibility recovery."""
        pp = pattern.opinion.projected_probability()
        return pp >= 0.50  # hysteresis: higher than quarantine threshold

    def can_dissolve_from_quarantine(self, pattern: RSCPattern) -> bool:
        """QUARANTINED → DISSOLVED after timeout."""
        return pattern.quarantine_cycles >= 3

    def can_supersede(self, old: RSCPattern, new: RSCPattern) -> bool:
        """An ACTIVE pattern can be SUPERSEDED by a new pattern."""
        return (
            old.applies_to_class == new.applies_to_class and
            old.format == new.format and
            new.opinion.projected_probability() > old.opinion.projected_probability()
        )

    def should_dormant(self, pattern: RSCPattern) -> bool:
        """ACTIVE → DORMANT on sustained low access."""
        return pattern.consecutive_low_access_cycles >= 3
```

### 6.4 C17 Whitelist Lifecycle Integration

The C17 RSC whitelist is synchronized with RSC pattern state:

| RSC State Transition | C17 Whitelist Action |
|---|---|
| → ACTIVE | Add structural fingerprint to whitelist |
| ACTIVE → DORMANT | Remove from whitelist |
| ACTIVE → SUPERSEDED | Remove from whitelist |
| ACTIVE → QUARANTINED | Remove from whitelist |
| DORMANT → ACTIVE | Add structural fingerprint to whitelist |
| QUARANTINED → ACTIVE | Add structural fingerprint to whitelist |
| → DISSOLVED | Remove from whitelist (if present) |

---

## 7. Formal Requirements

| ID | Requirement | Component | Priority |
|---|---|---|---|
| **EFF-R01** | VFL MUST subscribe to C5 VTD output as a non-interfering second consumer | VFL | P0 |
| **EFF-R02** | VFL MUST enforce k-anonymity floor of VFL_K_ANONYMITY_FLOOR on all published statistics | VFL | P0 |
| **EFF-R03** | VFL MUST apply epsilon-differential privacy noise to all published aggregate metrics | VFL | P0 |
| **EFF-R04** | VFL MUST discard agent identifiers after the aggregation window closes | VFL | P0 |
| **EFF-R05** | VFL MUST suppress per-class statistics when sample size < VFL_MIN_SAMPLE | VFL | P0 |
| **EFF-R06** | VFL MUST apply hierarchical Bayesian shrinkage for classes below VFL_MIN_SAMPLE, with shrinkage flag | VFL | P1 |
| **EFF-R07** | VFL MUST publish per-class quality metrics once per CONSOLIDATION_CYCLE | VFL | P0 |
| **EFF-R08** | VFL MUST run anomaly detection (chi-squared) at each TIDAL_EPOCH and publish immediately if p < VFL_ANOMALY_P_THRESHOLD | VFL | P1 |
| **EFF-R09** | RSC patterns MUST be stored as C6 EMA epistemic quanta with content.type = "reasoning_strategy" | RSC | P0 |
| **EFF-R10** | RSC v1.0 MUST restrict format types to declarative_decomposition, anti_pattern, and verification_checklist | RSC | P0 |
| **EFF-R11** | New RSC patterns MUST start with opinion uncertainty u >= RSC_INITIAL_UNCERTAINTY | RSC | P0 |
| **EFF-R12** | RSC MUST track pattern credibility via subjective logic opinion tuples | RSC | P0 |
| **EFF-R13** | RSC MUST monitor population structural convergence per claim class and raise diversity alerts when mean similarity exceeds RSC_CONVERGENCE_THRESHOLD | RSC | P1 |
| **EFF-R14** | RSC convergence monitoring MUST NOT suppress or remove convergent patterns | RSC | P1 |
| **EFF-R15** | CABS MUST produce range recommendations (min_sufficient, recommended, max_useful) with strategy labels | CABS | P0 |
| **EFF-R16** | The reasoning_budget_advisory field on ExecutionLease MUST be optional (non-breaking) | CABS | P0 |
| **EFF-R17** | C23 EEB MUST NOT record whether the agent read or followed the CABS advisory | CABS | P0 |
| **EFF-R18** | All RSC consumption logs MUST carry the ADVISORY_PRIVATE label | Membrane | P0 |
| **EFF-R19** | C17 MUST NOT access ADVISORY_PRIVATE data | Membrane | P0 |
| **EFF-R20** | C35 MUST NOT access ADVISORY_PRIVATE data | Membrane | P0 |
| **EFF-R21** | C17 MUST maintain an RSC-synchronized structural pattern whitelist and discount matching structural similarity in B(a_i, a_j) | Membrane | P0 |
| **EFF-R22** | The C17 whitelist MUST contain only structural fingerprints, not consumption data or credibility scores | Membrane | P0 |
| **EFF-R23** | VFL_EPSILON MUST be a constitutional parameter requiring G-class consensus for modification | VFL | P0 |
| **EFF-R24** | RSC seed patterns MUST receive a grace period of RSC_SEED_GRACE_PERIOD before catabolism eligibility | RSC | P1 |
| **EFF-R25** | RSC credibility updates MUST be computed within the secure aggregation boundary; only opinion deltas leave the boundary | RSC | P0 |
| **EFF-R26** | CABS confidence MUST be < 0.5 when VFL data is unavailable or below VFL_MIN_SAMPLE | CABS | P1 |
| **EFF-R27** | Advisory Membrane data segregation MUST be verifiable by audit at MEMBRANE_AUDIT_INTERVAL | Membrane | P1 |

---

## 8. Risk Analysis

| Risk | Severity | Probability | Mitigation | Residual |
|---|---|---|---|---|
| VFL insufficient sample for rare classes (K, H, N) | MEDIUM | HIGH | Hierarchical Bayesian shrinkage (EFF-R06); longer aggregation windows; suppress when n < VFL_MIN_SAMPLE | LOW-MEDIUM |
| RSC ineffective for non-LLM agents | HIGH | HIGH | v1.0 restricted to declarative patterns; `architecture_applicability` field distinguishes universal vs. llm_preferred | MEDIUM |
| CABS non-monotonic budget-performance | MEDIUM | MEDIUM | Range recommendations with max_useful ceiling; strategy labels pair budget with approach | LOW |
| C17 structural side-channel leaks advisory consumption | HIGH | MEDIUM | RSC-aware whitelist (IC-EFF-04); structural fingerprint discounting | LOW-MEDIUM |
| Advisory signals become de facto mandatory | LOW-MEDIUM | HIGH | Voluntariness paradox acknowledged; membrane prevents enforcement-based coercion; no downstream consequences | LOW (accepted) |
| RSC reasoning monoculture | MEDIUM | MEDIUM | Convergence monitoring (EFF-R13); diversity alerts; alternative pattern promotion | LOW |
| VFL Goodhart's Law (agents gaming VFL metrics) | MEDIUM | LOW | Inherited from C5 verification integrity; flag for C5 v3.0 | MEDIUM |
| Privacy guarantee erosion via composition attacks | MEDIUM | LOW | VFL_EPSILON as constitutional parameter; total privacy budget tracked across EFF lifetime | LOW-MEDIUM |
| RSC patterns calcify (old patterns resist dissolution) | LOW | MEDIUM | Standard C6 metabolic lifecycle; no grace period exceptions (except seed) | LOW |
| GaaS patent overlap | MEDIUM | LOW | EFF is advisory-only (GaaS is enforcement); Advisory Membrane is primary differentiator | LOW |

---

## 9. Open Questions

| ID | Question | Priority | Resolution Path |
|---|---|---|---|
| OQ-1 | What is the empirically correct RSC_CONVERGENCE_THRESHOLD? | P1 | W0 experiment: measure baseline structural similarity across 1000+ agents before RSC deployment. Set threshold at mean + 2 sigma. |
| OQ-2 | Should VFL publish failure mode taxonomies or free-text failure descriptions? | P2 | Taxonomy is more useful for statistical analysis but requires maintenance. Recommend taxonomy with version control. |
| OQ-3 | How should RSC handle multi-class patterns (patterns useful for R+E or S+K)? | P2 | Option A: duplicate pattern per class. Option B: multi-class patterns with per-class credibility. Recommend B for v1.0, review after data accumulates. |
| OQ-4 | What is the total DP privacy budget across EFF's lifetime? | P1 | Composition theorem: epsilon accumulates. With VFL_EPSILON=2.0 and 1 publication per CONSOLIDATION_CYCLE, annual budget is ~2.0 * 876 = 1752. This is large; consider privacy amplification via subsampling or the moments accountant. |
| OQ-5 | Should CABS recommendations be versioned (tied to specific VFL publications)? | P2 | Yes — CABS advisory includes `vfl_publication_id` for traceability. |
| OQ-6 | How does EFF interact with C14 AiBC Phase transitions? | P3 | EFF is infrastructure; it operates identically across AiBC phases. No phase-specific behavior required. |
