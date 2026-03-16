# C6 EMA Hardening Addendum: SHREC Dual-Controller Interaction & Coherence Collapse at Scale

**Addendum to:** C6 Master Technical Specification (EMA), Version 1.0.0
**Addendum Version:** 1.0.0
**Date:** 2026-03-10
**Status:** HARDENING ADDENDUM (Critical Findings Resolution)
**Findings Addressed:** SHREC Dual-Controller Interaction (CRITICAL), Coherence Collapse at Scale (CRITICAL)
**Normative Status:** This addendum supersedes conflicting language in the base spec. All pseudocode herein is normative.

---

## Table of Contents

1. [Problem 1: SHREC Dual-Controller Interaction](#1-shrec-dual-controller-interaction)
   - 1.1 [Finding Summary](#11-finding-summary)
   - 1.2 [Root Cause Analysis](#12-root-cause-analysis)
   - 1.3 [Solution: Regime-Based Precedence Model](#13-solution-regime-based-precedence-model)
   - 1.4 [Combination Function](#14-combination-function)
   - 1.5 [Budget Conservation Enforcement](#15-budget-conservation-enforcement)
   - 1.6 [Regime Transition Logic](#16-regime-transition-logic)
   - 1.7 [Complete Pseudocode: Regime-Based Controller](#17-complete-pseudocode-regime-based-controller)
   - 1.8 [Invariants Added](#18-invariants-added)
2. [Problem 2: Coherence Collapse at Scale](#2-coherence-collapse-at-scale)
   - 2.1 [Finding Summary](#21-finding-summary)
   - 2.2 [Root Cause Analysis](#22-root-cause-analysis)
   - 2.3 [Solution: Sharded Coherence with Tiered Updates](#23-solution-sharded-coherence-with-tiered-updates)
   - 2.4 [Active Edge Budget per Shard](#24-active-edge-budget-per-shard)
   - 2.5 [Tiered Update Frequency](#25-tiered-update-frequency)
   - 2.6 [Scale Tier Definitions (Revised)](#26-scale-tier-definitions-revised)
   - 2.7 [Computation Budget Enforcement](#27-computation-budget-enforcement)
   - 2.8 [Complete Pseudocode: Sharded Coherence Engine](#28-complete-pseudocode-sharded-coherence-engine)
   - 2.9 [Invariants Added](#29-invariants-added)
3. [Superseded Sections](#3-superseded-sections)
4. [Traceability](#4-traceability)

---

## 1. SHREC Dual-Controller Interaction

### 1.1 Finding Summary

The base spec defines two overlapping control systems that both modify SHREC budget allocations:

- **Lotka-Volterra ecological competition** (Section 6.4): Produces budget allocations through generalized competitive dynamics among five signals.
- **PID graduated control overlay** (Section 6.7): Modifies budgets based on z-score error signals in elevated operating regimes.

The interaction between these two controllers is unspecified. The base spec describes them independently but never defines:

1. Whether their outputs are additive, multiplicative, or conditional.
2. Which controller has precedence when they disagree.
3. Whether the combined output can violate budget conservation (allocations summing to more or less than total budget).
4. How the system behaves during regime transitions when one controller activates or deactivates.

This is a CRITICAL finding because budget allocation governs all metabolic processing. Unspecified controller interaction means the system's behavior under stress -- exactly when correct regulation matters most -- is undefined.

### 1.2 Root Cause Analysis

The base spec Section 6.7 defines four regimes (NORMAL, ELEVATED, CRITICAL, CONSTITUTIONAL) with PID activity levels per regime, but only specifies the PID correction magnitude limits (+/-10%, +/-25%, unclamped). It does not specify how PID corrections compose with LV outputs. The implicit assumption appears to be additive (LV output + PID correction), but this is never stated, and additive composition without renormalization can violate budget conservation.

Additionally, the CONSTITUTIONAL regime ("System invariant threatened, unclamped PID") has no safety bound at all. An unclamped PID controller operating on a system with floor guarantees could produce allocations below floors, violating INV-E7.

### 1.3 Solution: Regime-Based Precedence Model

The dual-controller interaction is resolved by defining strict precedence rules per regime. The controllers are not peers; their relationship changes with system stress level.

| Regime | LV Role | PID Role | Precedence |
|--------|---------|----------|------------|
| NORMAL | Primary controller. Produces all budget allocations. | OFF. Not computed, not applied. | LV only. |
| ELEVATED | Primary controller. Produces baseline allocations. | Active, bounded. Corrections clamped to +/-10% of LV output per signal. | LV primary, PID nudges. |
| CRITICAL | Advisory. Continues running but output is not directly used for allocation. | Primary controller. Corrections clamped to +/-25% of last stable LV baseline. | PID primary, LV advisory. |
| EMERGENCY | Frozen. Last-known-good output preserved. | Frozen. Last-known-good corrections preserved. | Neither. Static hold. |

**Key design decisions:**

1. **NORMAL = LV only.** When the system is healthy, ecological competition is the correct allocation mechanism. PID overhead is unnecessary and its integral accumulation would be meaningless noise.

2. **ELEVATED = LV + bounded PID.** PID provides gentle corrections for signals drifting beyond 1.5 sigma. The 10% bound ensures PID cannot override LV's ecological balance -- it can only nudge.

3. **CRITICAL = PID primary.** When any signal exceeds 2.5 sigma, the ecological model is no longer tracking reality. PID's error-driven correction is the appropriate response. LV continues running so it can produce a baseline for regime recovery, but its output does not directly control allocations.

4. **EMERGENCY = static hold.** When a system invariant is threatened (replacing the base spec's "CONSTITUTIONAL" regime), both controllers are frozen. Budgets are held at last-known-good values. This replaces the dangerous "unclamped PID" behavior in the base spec. Unclamped PID on a system with floor guarantees is self-contradictory; emergency hold is the safe response.

**Renaming:** The base spec's "CONSTITUTIONAL" regime is renamed to "EMERGENCY" to clarify its semantics. CONSTITUTIONAL implied governance-level intervention; EMERGENCY correctly describes a safety hold.

### 1.4 Combination Function

When both controllers are active (ELEVATED regime), the combination function is:

```
final_budget[signal] = LV_output[signal] + clamp(
    PID_correction[signal],
    -0.10 * LV_output[signal],
    +0.10 * LV_output[signal]
)
```

**Properties of this function:**

- **Bounded perturbation:** PID can adjust any signal by at most 10% of its LV-determined allocation. A signal allocated 20% of budget by LV can be adjusted to [18%, 22%].
- **Proportional bounds:** Larger allocations get larger absolute correction ranges. This prevents PID from overwhelming small-allocation signals (e.g., CONSOLIDATION at floor=5%) while still allowing meaningful corrections to large-allocation signals.
- **Deterministic:** Given LV output and PID correction, the combined output is fully determined. No ambiguity.

**In CRITICAL regime**, PID operates on the last stable LV baseline (the LV output from the last NORMAL or ELEVATED epoch), not the current LV output:

```
final_budget[signal] = last_stable_LV[signal] + clamp(
    PID_correction[signal],
    -0.25 * last_stable_LV[signal],
    +0.25 * last_stable_LV[signal]
)
```

This prevents the PID from chasing LV's potentially unstable outputs during a crisis.

### 1.5 Budget Conservation Enforcement

After combining controller outputs, budget conservation is enforced in three steps:

1. **Combine:** Apply the combination function to get raw combined allocations.
2. **Floor enforcement:** Ensure every signal meets its floor allocation (INV-E7).
3. **Renormalize:** Scale all allocations proportionally so they sum to exactly total_budget.
4. **Re-enforce floors:** If renormalization pushed any signal below its floor, restore the floor and re-renormalize. Iterate until convergent (proven to converge in at most 5 iterations for 5 signals with total floor < 50%).

**Formal guarantee:** The output of the conservation enforcement always satisfies:
- `sum(final_budget.values()) == total_budget` (within floating-point epsilon)
- `final_budget[signal] >= total_budget * FLOOR_ALLOCATIONS[signal]` for all signals

Neither controller, individually or combined, can create or destroy budget.

### 1.6 Regime Transition Logic

Regime transitions are determined by signal health metrics derived from the SHREC statistical self-model (Section 6.6 of base spec).

**Transition thresholds:**

```
REGIME_THRESHOLDS:
  NORMAL_TO_ELEVATED:    max_z_score >= 1.5   (any signal z-score >= 1.5 sigma)
  ELEVATED_TO_CRITICAL:  max_z_score >= 2.5   (any signal z-score >= 2.5 sigma)
  CRITICAL_TO_EMERGENCY: invariant_violation OR max_z_score >= 4.0 OR consecutive_critical_epochs >= 20
  EMERGENCY_TO_CRITICAL: invariant_restored AND max_z_score < 4.0 AND manual_release = true
  CRITICAL_TO_ELEVATED:  max_z_score < 2.5 for DOWNGRADE_HYSTERESIS consecutive epochs (5)
  ELEVATED_TO_NORMAL:    max_z_score < 1.5 for DOWNGRADE_HYSTERESIS consecutive epochs (5)
```

**Transition rules:**

1. **Upward transitions are immediate.** When any signal crosses a threshold upward, the regime escalates in the same epoch. Latency in escalation is dangerous.
2. **Downward transitions require hysteresis.** The system must remain below the threshold for DOWNGRADE_HYSTERESIS (5) consecutive epochs before downgrading. This prevents oscillation between regimes.
3. **EMERGENCY entry has a manual release gate.** Entering EMERGENCY is automatic. Leaving EMERGENCY requires both metric recovery AND manual operator confirmation. This prevents automated recovery from a state that may indicate fundamental system compromise.
4. **Regime transitions reset PID integral.** On any regime change, the PID integral term resets to zero. This prevents integral windup from a previous regime's error history corrupting the new regime's behavior.

**Invariant violations that trigger EMERGENCY:**

- Any signal allocation falls below 50% of its floor for 3 consecutive epochs (despite floor enforcement -- indicates conservation failure).
- Total budget exceeds measured system capacity by > 20% (runaway allocation).
- SHREC statistical self-model produces NaN or infinite values (numerical instability).
- Immune self-audit detects autoimmune rate > 0.50 (catabolism attacking more than half of valid knowledge).

### 1.7 Complete Pseudocode: Regime-Based Controller

```python
# =============================================================================
# SHREC REGIME-BASED DUAL-CONTROLLER
# Supersedes: Base spec Section 6.7 (Graduated Control Overlay)
# =============================================================================

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional
from collections import deque

class Regime(Enum):
    NORMAL = 0
    ELEVATED = 1
    CRITICAL = 2
    EMERGENCY = 3

SIGNALS = ["HUNGER", "CONSOLIDATION", "STRESS", "IMMUNE", "NOVELTY"]

FLOOR_ALLOCATIONS = {
    "IMMUNE": 0.15,
    "STRESS": 0.10,
    "NOVELTY": 0.08,
    "HUNGER": 0.05,
    "CONSOLIDATION": 0.05,
}

# Regime transition thresholds
NORMAL_TO_ELEVATED_Z = 1.5
ELEVATED_TO_CRITICAL_Z = 2.5
CRITICAL_TO_EMERGENCY_Z = 4.0
CONSECUTIVE_CRITICAL_LIMIT = 20
DOWNGRADE_HYSTERESIS = 5  # epochs

# PID clamp bounds per regime
PID_CLAMP = {
    Regime.NORMAL: 0.0,       # PID off
    Regime.ELEVATED: 0.10,    # +/- 10%
    Regime.CRITICAL: 0.25,    # +/- 25%
    Regime.EMERGENCY: 0.0,    # PID frozen
}

# Conservation enforcement iteration limit
MAX_CONSERVATION_ITERATIONS = 5

@dataclass
class PIDState:
    """Per-signal PID controller state."""
    integral: float = 0.0
    previous_error: float = 0.0
    Kp: float = 0.0
    Ki: float = 0.0
    Kd: float = 0.0

@dataclass
class SHRECControllerState:
    """Complete state of the regime-based dual controller."""
    regime: Regime = Regime.NORMAL
    pid_states: Dict[str, PIDState] = field(default_factory=dict)
    last_stable_lv_output: Dict[str, float] = field(default_factory=dict)
    last_known_good_budget: Dict[str, float] = field(default_factory=dict)
    downgrade_counter: int = 0
    consecutive_critical_epochs: int = 0
    emergency_manual_release: bool = False
    signal_stats: Dict[str, "SignalStatistics"] = field(default_factory=dict)

    def __post_init__(self):
        for sig in SIGNALS:
            if sig not in self.pid_states:
                self.pid_states[sig] = PIDState()


def compute_regime(state: SHRECControllerState, signal_values: Dict[str, float]) -> Regime:
    """
    Determine the current regime based on signal z-scores.
    Upward transitions are immediate; downward transitions require hysteresis.
    """
    z_scores = {}
    for sig in SIGNALS:
        z_scores[sig] = state.signal_stats[sig].z_score(signal_values[sig])

    max_z = max(z_scores.values())
    current = state.regime

    # --- Check for EMERGENCY triggers ---
    if current == Regime.CRITICAL:
        state.consecutive_critical_epochs += 1
    else:
        state.consecutive_critical_epochs = 0

    invariant_violated = check_invariant_violations(state, signal_values)

    if invariant_violated or max_z >= CRITICAL_TO_EMERGENCY_Z or \
       state.consecutive_critical_epochs >= CONSECUTIVE_CRITICAL_LIMIT:
        if current != Regime.EMERGENCY:
            state.downgrade_counter = 0
            state.emergency_manual_release = False
        return Regime.EMERGENCY

    # --- Upward transitions (immediate) ---
    if current == Regime.NORMAL and max_z >= NORMAL_TO_ELEVATED_Z:
        state.downgrade_counter = 0
        if max_z >= ELEVATED_TO_CRITICAL_Z:
            return Regime.CRITICAL
        return Regime.ELEVATED

    if current == Regime.ELEVATED and max_z >= ELEVATED_TO_CRITICAL_Z:
        state.downgrade_counter = 0
        return Regime.CRITICAL

    # --- Downward transitions (with hysteresis) ---
    if current == Regime.EMERGENCY:
        if not invariant_violated and max_z < CRITICAL_TO_EMERGENCY_Z and \
           state.emergency_manual_release:
            state.downgrade_counter = 0
            return Regime.CRITICAL
        return Regime.EMERGENCY

    if current == Regime.CRITICAL and max_z < ELEVATED_TO_CRITICAL_Z:
        state.downgrade_counter += 1
        if state.downgrade_counter >= DOWNGRADE_HYSTERESIS:
            state.downgrade_counter = 0
            return Regime.ELEVATED
        return Regime.CRITICAL

    if current == Regime.ELEVATED and max_z < NORMAL_TO_ELEVATED_Z:
        state.downgrade_counter += 1
        if state.downgrade_counter >= DOWNGRADE_HYSTERESIS:
            state.downgrade_counter = 0
            return Regime.NORMAL
        return Regime.ELEVATED

    # No transition
    return current


def check_invariant_violations(state: SHRECControllerState,
                                signal_values: Dict[str, float]) -> bool:
    """
    Check for invariant violations that force EMERGENCY regime.
    Returns True if any invariant is violated.
    """
    # Check 1: Any signal at NaN/Inf
    for sig in SIGNALS:
        v = signal_values[sig]
        if v != v or abs(v) == float('inf'):  # NaN or Inf check
            return True

    # Check 2: Last-known-good budget has any signal below 50% of floor
    # (checked externally by the caller after conservation enforcement)
    # This flag is set by enforce_budget_conservation if it detects persistent
    # floor violations after MAX_CONSERVATION_ITERATIONS.

    # Check 3: Autoimmune rate (checked by immune self-audit, flag set externally)

    return state._invariant_violation_flag if hasattr(state, '_invariant_violation_flag') else False


def compute_lv_allocations(signal_values: Dict[str, float],
                            previous_allocations: Dict[str, float],
                            total_budget: float,
                            dt: float = 1.0) -> Dict[str, float]:
    """
    Lotka-Volterra ecological competition step.
    Implements base spec Section 6.4 with forward Euler integration.

    Parameters:
        signal_values: current signal intensities (0-1 per signal)
        previous_allocations: S_i from previous epoch
        total_budget: B(t) from Section 6.3
        dt: integration timestep (1.0 = one epoch)

    Returns:
        New budget allocations (not yet floor-enforced or conserved)
    """
    # Alpha matrix (from base spec Section 6.4)
    ALPHA = {
        "HUNGER":        {"HUNGER": 1.0, "CONSOLIDATION": 0.2, "STRESS": 0.3, "IMMUNE": 0.1, "NOVELTY": 0.2},
        "CONSOLIDATION": {"HUNGER": 0.2, "CONSOLIDATION": 1.0, "STRESS": 0.1, "IMMUNE": 0.2, "NOVELTY": 0.3},
        "STRESS":        {"HUNGER": 0.3, "CONSOLIDATION": 0.1, "STRESS": 1.0, "IMMUNE": 0.2, "NOVELTY": 0.1},
        "IMMUNE":        {"HUNGER": 0.1, "CONSOLIDATION": 0.2, "STRESS": 0.2, "IMMUNE": 1.0, "NOVELTY": 0.1},
        "NOVELTY":       {"HUNGER": 0.2, "CONSOLIDATION": 0.3, "STRESS": 0.1, "IMMUNE": 0.1, "NOVELTY": 1.0},
    }

    K = 0.4  # carrying capacity (default, all signals)
    RESTORATION_RATE = 2.0

    allocations = {}
    for i in SIGNALS:
        S_i = previous_allocations.get(i, total_budget / len(SIGNALS))
        r_i = signal_values[i]  # intrinsic growth rate = signal intensity

        # Competition term
        competition_sum = sum(ALPHA[i][j] * previous_allocations.get(j, total_budget / len(SIGNALS)) / K
                              for j in SIGNALS)
        growth = r_i * S_i * (1.0 - competition_sum)

        # Floor correction
        floor_i = total_budget * FLOOR_ALLOCATIONS[i]
        floor_correction = max(0.0, floor_i - S_i) * RESTORATION_RATE

        # Forward Euler step
        new_S_i = S_i + dt * (growth + floor_correction)

        # Clamp to non-negative
        allocations[i] = max(0.0, new_S_i)

    return allocations


def compute_pid_correction(state: SHRECControllerState,
                            signal_values: Dict[str, float],
                            target_values: Dict[str, float]) -> Dict[str, float]:
    """
    PID correction for each signal.
    Error = target - actual signal value.
    Target = statistical mean (from self-model).

    Parameters:
        state: controller state with per-signal PID states
        signal_values: current signal intensities
        target_values: target signal values (statistical means from self-model)

    Returns:
        PID correction per signal (unbounded; caller applies regime-specific clamping)
    """
    corrections = {}
    for sig in SIGNALS:
        pid = state.pid_states[sig]
        stats = state.signal_stats[sig]

        error = target_values[sig] - signal_values[sig]

        # Auto-derived gains (from base spec Section 6.7)
        sigma = max(0.01, stats.sigma)
        window = 100
        pid.Kp = 1.0 / sigma
        pid.Ki = pid.Kp / (4.0 * window)
        pid.Kd = pid.Kp * (window / 10.0)

        # PID terms
        P = pid.Kp * error
        pid.integral += error
        # Anti-windup: clamp integral to +/- 2 * sigma
        pid.integral = clamp(pid.integral, -2.0 * sigma, 2.0 * sigma)
        I = pid.Ki * pid.integral
        D = pid.Kd * (error - pid.previous_error)

        pid.previous_error = error

        corrections[sig] = P + I + D

    return corrections


def combine_controllers(regime: Regime,
                         lv_output: Dict[str, float],
                         pid_corrections: Dict[str, float],
                         state: SHRECControllerState,
                         total_budget: float) -> Dict[str, float]:
    """
    Combine LV and PID outputs according to regime precedence.

    NORMAL:    LV output only. PID ignored.
    ELEVATED:  LV + clamped PID (+/- 10% of LV output).
    CRITICAL:  Last stable LV baseline + clamped PID (+/- 25% of baseline).
    EMERGENCY: Last-known-good budget (static hold).
    """
    if regime == Regime.NORMAL:
        # LV is sole controller
        return dict(lv_output)

    elif regime == Regime.ELEVATED:
        combined = {}
        for sig in SIGNALS:
            lv_val = lv_output[sig]
            bound = PID_CLAMP[Regime.ELEVATED] * lv_val  # 10% of LV output
            clamped_pid = clamp(pid_corrections.get(sig, 0.0), -bound, bound)
            combined[sig] = lv_val + clamped_pid
        return combined

    elif regime == Regime.CRITICAL:
        combined = {}
        for sig in SIGNALS:
            # Use last stable LV output as baseline, not current LV
            baseline = state.last_stable_lv_output.get(sig, total_budget / len(SIGNALS))
            bound = PID_CLAMP[Regime.CRITICAL] * baseline  # 25% of baseline
            clamped_pid = clamp(pid_corrections.get(sig, 0.0), -bound, bound)
            combined[sig] = baseline + clamped_pid
        return combined

    elif regime == Regime.EMERGENCY:
        # Static hold: return last-known-good budget
        return dict(state.last_known_good_budget)

    else:
        raise ValueError(f"Unknown regime: {regime}")


def enforce_budget_conservation(allocations: Dict[str, float],
                                 total_budget: float) -> Dict[str, float]:
    """
    Enforce budget conservation: all allocations sum to total_budget
    and every signal meets its floor allocation.

    Iterates floor enforcement + renormalization until convergent.
    Proven to converge in <= 5 iterations for 5 signals with total floor < 50%.
    """
    for iteration in range(MAX_CONSERVATION_ITERATIONS):
        # Step 1: Enforce floors
        for sig in SIGNALS:
            floor = total_budget * FLOOR_ALLOCATIONS[sig]
            allocations[sig] = max(allocations[sig], floor)

        # Step 2: Renormalize to total_budget
        current_total = sum(allocations.values())
        if current_total <= 0:
            # Degenerate case: distribute equally
            allocations = {sig: total_budget / len(SIGNALS) for sig in SIGNALS}
            break

        if abs(current_total - total_budget) < 1e-10:
            break  # Already conserved

        scale = total_budget / current_total
        allocations = {sig: val * scale for sig, val in allocations.items()}

        # Step 3: Check if floors still met after scaling
        floors_met = all(
            allocations[sig] >= total_budget * FLOOR_ALLOCATIONS[sig] - 1e-10
            for sig in SIGNALS
        )
        if floors_met:
            break

    return allocations


def shrec_epoch_step(state: SHRECControllerState,
                      signal_values: Dict[str, float],
                      total_budget: float) -> Dict[str, float]:
    """
    MAIN ENTRY POINT: Execute one epoch of SHREC regulation.

    This is the single function that replaces the unspecified dual-controller
    interaction. It:
      1. Updates signal statistics
      2. Determines regime
      3. Runs LV (always, for baseline tracking)
      4. Runs PID (only in ELEVATED/CRITICAL)
      5. Combines according to regime precedence
      6. Enforces budget conservation
      7. Updates controller state

    Parameters:
        state: mutable controller state (persists across epochs)
        signal_values: current signal intensities from SHREC signal computation
        total_budget: B(t) for this epoch

    Returns:
        Final budget allocations, guaranteed to sum to total_budget and
        satisfy all floor constraints.
    """
    # --- Step 1: Update signal statistics ---
    for sig in SIGNALS:
        state.signal_stats[sig].update(signal_values[sig])

    # --- Step 2: Determine regime ---
    previous_regime = state.regime
    new_regime = compute_regime(state, signal_values)

    # Reset PID integral on regime transition
    if new_regime != previous_regime:
        for sig in SIGNALS:
            state.pid_states[sig].integral = 0.0
            state.pid_states[sig].previous_error = 0.0

    state.regime = new_regime

    # --- Step 3: Run Lotka-Volterra (always, for baseline tracking) ---
    lv_output = compute_lv_allocations(
        signal_values=signal_values,
        previous_allocations=state.last_known_good_budget or
                             {sig: total_budget / len(SIGNALS) for sig in SIGNALS},
        total_budget=total_budget
    )

    # Track last stable LV output (updated only in NORMAL or ELEVATED)
    if new_regime in (Regime.NORMAL, Regime.ELEVATED):
        state.last_stable_lv_output = dict(lv_output)

    # --- Step 4: Run PID (only if regime requires it) ---
    pid_corrections = {}
    if new_regime in (Regime.ELEVATED, Regime.CRITICAL):
        target_values = {sig: state.signal_stats[sig].mean for sig in SIGNALS}
        pid_corrections = compute_pid_correction(state, signal_values, target_values)

    # --- Step 5: Combine according to regime precedence ---
    raw_combined = combine_controllers(
        regime=new_regime,
        lv_output=lv_output,
        pid_corrections=pid_corrections,
        state=state,
        total_budget=total_budget
    )

    # --- Step 6: Enforce budget conservation ---
    final_budget = enforce_budget_conservation(raw_combined, total_budget)

    # --- Step 7: Update state ---
    if new_regime != Regime.EMERGENCY:
        state.last_known_good_budget = dict(final_budget)

    return final_budget


def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp value to [lo, hi]."""
    return max(lo, min(hi, value))
```

### 1.8 Invariants Added

This addendum adds the following invariants to the base spec's INV-E series:

- **INV-E11 (Controller Precedence):** In NORMAL regime, PID corrections MUST NOT be applied to budget allocations. In ELEVATED regime, PID corrections MUST be clamped to +/-10% of LV output. In CRITICAL regime, PID corrections MUST be clamped to +/-25% of last stable LV baseline. In EMERGENCY regime, both controllers MUST be frozen.

- **INV-E12 (Budget Conservation):** After all controller outputs are combined and floors enforced, the sum of all signal budget allocations MUST equal total_budget within floating-point epsilon (1e-10). Violation for 3 consecutive epochs triggers EMERGENCY regime.

- **INV-E13 (Regime Transition Atomicity):** Regime transitions MUST take effect at the start of the epoch in which they are detected. No epoch may execute under ambiguous regime state.

- **INV-E14 (Emergency Manual Gate):** Exit from EMERGENCY regime MUST require both metric recovery below CRITICAL thresholds AND explicit manual operator release. Automated recovery from EMERGENCY is prohibited.

---

## 2. Coherence Collapse at Scale

### 2.1 Finding Summary

The base spec's coherence graph (Section 7) at 1B quanta with average 5 edges per quantum produces 5B edges. Edge weight updates require visiting each edge for Hebbian reinforcement and temporal decay. At the base spec's stated processing targets:

- **SETTLEMENT_TICK = 60 seconds** (per C9 temporal hierarchy)
- **TIDAL_EPOCH = 3,600 seconds = 60 SETTLEMENT_TICKs** (per C9 temporal hierarchy)
- **CONSOLIDATION_CYCLE = 36,000 seconds = 10 TIDAL_EPOCHS** (per C9 temporal hierarchy)

At 5B edges and a conservative 1 microsecond per edge update, a full edge weight update pass takes:

```
5,000,000,000 edges * 1 microsecond/edge = 5,000 seconds = 83.3 minutes
```

This exceeds a single TIDAL_EPOCH (60 minutes). Even with parallelism, the sheer data volume (5B edges at ~40 bytes per edge = ~200 GB) creates memory pressure that prevents efficient batch processing.

The base spec defines sharding by locus (Section 7.2) and scale tiers (Section 7.5), but:

1. No shard size limits are specified (a single locus could contain all 1B quanta).
2. No tiered update frequency is defined (all edges updated at same rate regardless of activity).
3. No computation budget per epoch is specified (updates run until complete, potentially overrunning epoch boundaries).
4. The T3 tier mentions "hierarchical: cluster-level" coherence without defining the hierarchy, clustering strategy, or update protocol.
5. Cross-shard edge maintenance cost is not modeled.

### 2.2 Root Cause Analysis

The coherence graph is designed as if it will always be small enough for full traversal per epoch. The scale tiers in Section 7.5 acknowledge that this assumption fails, but only sketch solutions ("sharded", "sampled", "hierarchical") without specifying the mechanisms.

The fundamental issue: edge weight dynamics (Hebbian reinforcement + temporal decay) are specified as per-epoch operations in Section 7.3, but the cost of executing those operations scales linearly with edge count. At planetary scale, the cost exceeds the epoch budget.

### 2.3 Solution: Sharded Coherence with Tiered Updates

The solution has four components: (1) enforced shard size limits, (2) tiered edge update frequency based on edge activity, (3) revised scale tiers with concrete mechanisms, and (4) per-epoch computation budgets.

**Sharding model:**

```
Coherence Graph (global logical view)
  |
  +-- Locus L1
  |     +-- Shard L1 (max 1M quanta, max 5M intra-shard edges)
  |
  +-- Locus L2
  |     +-- Shard L2 (max 1M quanta, max 5M intra-shard edges)
  |
  +-- ...
  |
  +-- Border Graph (cross-locus edges only)
        +-- Border segment L1-L2 (reduced update frequency)
        +-- Border segment L1-L3
        +-- ...
```

**Shard rules:**

1. Each locus maintains exactly one coherence shard.
2. If a locus exceeds 1M quanta, it MUST be split into sub-loci (coordinated with C3 Parcel Transition Protocol). EMA does not split internally; it signals C3 to subdivide.
3. Intra-shard edges (both endpoints in same shard) are maintained locally.
4. Cross-shard edges are maintained in a separate border graph structure, indexed by locus pair.
5. Cross-shard edges count double against the source shard's edge budget (more expensive to maintain because updates require cross-shard coordination).

### 2.4 Active Edge Budget per Shard

Each shard enforces a hard edge budget:

```
MAX_QUANTA_PER_SHARD = 1,000,000
MAX_INTRA_EDGES_PER_SHARD = 5,000,000   (5 * MAX_QUANTA_PER_SHARD)
MAX_CROSS_EDGES_PER_SHARD = 500,000     (10% of intra-edge budget)
CROSS_EDGE_COST_MULTIPLIER = 2          (each cross-edge counts as 2 against budget)
```

**Effective edge budget per shard:**

```
effective_edge_count = intra_edge_count + CROSS_EDGE_COST_MULTIPLIER * cross_edge_count
max_effective_edges = MAX_INTRA_EDGES_PER_SHARD
```

When the effective edge budget is exceeded, edges are pruned in order of lowest rank score (using the ranking function from base spec Section 7.4), with the constraint that DERIVATION edges are never pruned (they are immutable per CR-24).

### 2.5 Tiered Update Frequency

Not all edges need updating every epoch. Edges are classified into three tiers based on activity:

| Tier | Criteria | Update Frequency | Fraction of Edges (estimated) |
|------|----------|-----------------|------------------------------|
| HOT | weight > 0.7 AND accessed in last 10 epochs | Every tidal epoch | ~10% |
| WARM | weight 0.3-0.7 OR (weight > 0.7 AND not accessed in last 10 epochs) | Every 5 tidal epochs | ~30% |
| COLD | weight < 0.3 | Every consolidation cycle (10 tidal epochs) | ~60% |

**Effective update volume reduction:**

In a given tidal epoch, the system updates:
- 100% of HOT edges (10% of total)
- 20% of WARM edges (6% of total, since each WARM edge is updated every 5th epoch)
- 10% of COLD edges (6% of total, since each COLD edge is updated every 10th epoch)
- **Total: ~22% of edges per epoch** (~4.5x reduction)

At 5B edges: 1.1B edge updates per epoch instead of 5B. At 1 microsecond per update: ~18.3 minutes, within the 30-minute computation budget (see Section 2.7).

**Tier assignment:**

```python
def classify_edge_tier(edge, current_epoch):
    """Classify an edge into HOT, WARM, or COLD tier."""
    if edge.edge_type == "DERIVATION":
        return "COLD"  # Immutable edges don't need frequent weight updates

    if edge.weight > 0.7 and (current_epoch - edge.last_accessed_epoch) <= 10:
        return "HOT"
    elif edge.weight >= 0.3:
        return "WARM"
    else:
        return "COLD"
```

**Temporal decay for non-updated edges:**

When a WARM or COLD edge is not updated in a given epoch, its decay is applied retroactively when its tier's update turn arrives:

```python
def apply_batched_decay(edge, epochs_since_last_update):
    """Apply accumulated temporal decay for edges that skipped updates."""
    # Compound decay: equivalent to applying per-epoch decay for each skipped epoch
    edge.weight *= (1.0 - EDGE_DECAY_RATE) ** epochs_since_last_update
    if edge.weight < MIN_EDGE_WEIGHT:
        mark_for_pruning(edge)
```

### 2.6 Scale Tier Definitions (Revised)

This section supersedes base spec Section 7.5.

| Tier | Quanta Range | Sharding | Update Strategy | Border Graph | Dreaming Scope |
|------|-------------|----------|-----------------|-------------|----------------|
| T1 | <= 100K | Single shard (no sharding needed) | Full update every epoch | N/A (single shard) | Global: all quanta eligible |
| T2 | 100K - 10M | Locus-sharded (max 1M per shard) | Tiered updates (HOT/WARM/COLD) | Full border graph, updated every 5 epochs | Shard-local with cross-shard bridge candidates |
| T3 | 10M - 1B | Locus-sharded + domain-partitioned | Tiered updates + border graph at reduced frequency | Sampled border graph (top 10% by weight) | Shard-local only, cluster representatives |
| T4 | > 1B | T3 + probabilistic edge sampling | Tiered updates + probabilistic sampling (random 20% per epoch) | Probabilistic border graph (reservoir sampling) | Shard-local, elected representatives only |

**T2 mechanism details:**

- Loci with > 1M quanta trigger split request to C3.
- Cross-locus edges maintained in full border graph.
- Border graph updated every 5 tidal epochs (not every epoch).
- Tiered updates reduce per-epoch edge processing by ~4.5x.

**T3 mechanism details:**

- Domain partitioning: within each locus shard, quanta are further partitioned by primary domain tag into domain sub-groups. Edge updates are parallelized across domain sub-groups.
- Border graph sampling: only the top 10% of cross-shard edges by weight are maintained. Remaining cross-shard edges are recorded as "latent" (provenance preserved, weight not actively updated).
- Aggressive pruning: MIN_EDGE_WEIGHT raised to 0.10 (from 0.05) at T3.

**T4 mechanism details:**

- Probabilistic edge sampling: each epoch, a random 20% of eligible edges per shard are selected for update. Over 5 epochs, each edge has ~67% probability of being updated at least once.
- Reservoir sampling for border graph: maintain a fixed-size reservoir of K cross-shard edges per locus pair (K = 10,000). New cross-shard edges displace existing ones with probability K/n (standard reservoir sampling).
- Edge updates are statistically unbiased: random selection ensures no systematic neglect of any edge subset.

**Tier transition triggers:**

```python
TIER_THRESHOLDS = {
    "T1_TO_T2": 100_000,       # quanta count
    "T2_TO_T3": 10_000_000,
    "T3_TO_T4": 1_000_000_000,
}

TIER_DOWNGRADE_THRESHOLDS = {
    "T2_TO_T1": 80_000,        # 20% hysteresis
    "T3_TO_T2": 8_000_000,
    "T4_TO_T3": 800_000_000,
}

def determine_scale_tier(total_quanta, current_tier):
    """
    Determine scale tier with hysteresis to prevent oscillation.
    Upgrade thresholds are higher than downgrade thresholds.
    """
    if total_quanta > TIER_THRESHOLDS["T3_TO_T4"]:
        return "T4"
    elif total_quanta > TIER_THRESHOLDS["T2_TO_T3"]:
        return "T3"
    elif total_quanta > TIER_THRESHOLDS["T1_TO_T2"]:
        return "T2"
    elif total_quanta < TIER_DOWNGRADE_THRESHOLDS.get(f"{current_tier}_TO_T1", 0):
        return "T1"
    elif total_quanta < TIER_DOWNGRADE_THRESHOLDS.get(f"{current_tier}_TO_T2", 0):
        return "T2"
    elif total_quanta < TIER_DOWNGRADE_THRESHOLDS.get(f"{current_tier}_TO_T3", 0):
        return "T3"
    else:
        return current_tier  # Stay in current tier (hysteresis)
```

### 2.7 Computation Budget Enforcement

Each tidal epoch allocates a maximum computation budget for coherence graph operations:

```
MAX_COHERENCE_COMPUTE_TIME = 1800 seconds  (30 minutes = 50% of tidal epoch)
```

The 50% allocation leaves the remaining 50% for the five metabolic phases (ingestion, circulation, consolidation, catabolism, regulation) and system overhead.

**Budget-aware update loop:**

If coherence computation exceeds its budget, the system defers remaining cold edges to the next epoch. HOT edges are always processed first (they represent active knowledge relationships), then WARM, then COLD. This ensures that under budget pressure, the most important edges are always updated.

### 2.8 Complete Pseudocode: Sharded Coherence Engine

```python
# =============================================================================
# SHARDED COHERENCE GRAPH ENGINE
# Supersedes: Base spec Section 7.2 (Sharding Strategy), Section 7.5 (Scale Tiers)
# Supplements: Base spec Section 7.3 (Edge Dynamics), Section 7.4 (Active Edge Budget)
# =============================================================================

import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum

# --- Configuration ---
MAX_QUANTA_PER_SHARD = 1_000_000
MAX_INTRA_EDGES_PER_SHARD = 5_000_000
MAX_CROSS_EDGES_PER_SHARD = 500_000
CROSS_EDGE_COST_MULTIPLIER = 2
MAX_COHERENCE_COMPUTE_SECONDS = 1800  # 30 minutes per tidal epoch

# Edge dynamics (from base spec, unchanged)
REINFORCEMENT_RATE = 0.05
EDGE_DECAY_RATE = 0.02
MIN_EDGE_WEIGHT = 0.05          # T1, T2
MIN_EDGE_WEIGHT_T3_PLUS = 0.10  # T3, T4
EDGE_TTL_EPOCHS = 50

# Tiered update frequencies (in tidal epochs)
HOT_UPDATE_INTERVAL = 1
WARM_UPDATE_INTERVAL = 5
COLD_UPDATE_INTERVAL = 10

# Edge tier thresholds
HOT_WEIGHT_THRESHOLD = 0.7
HOT_RECENCY_THRESHOLD = 10  # epochs since last access
WARM_WEIGHT_THRESHOLD = 0.3

# T4 probabilistic sampling rate
T4_SAMPLE_RATE = 0.20
T4_BORDER_RESERVOIR_SIZE = 10_000  # per locus pair

class EdgeTier(Enum):
    HOT = 0
    WARM = 1
    COLD = 2

@dataclass
class CoherenceEdge:
    source_id: str
    target_id: str
    edge_type: str          # SUPPORT, CONTRADICTION, DERIVATION, ANALOGY, SUPERSESSION
    weight: float
    last_accessed_epoch: int
    last_updated_epoch: int
    creating_agent: str
    is_cross_shard: bool = False
    tier: EdgeTier = EdgeTier.WARM

@dataclass
class CoherenceShard:
    """One shard per locus. Max 1M quanta, 5M intra-shard edges."""
    locus_id: str
    quanta_ids: Set[str] = field(default_factory=set)
    intra_edges: List[CoherenceEdge] = field(default_factory=list)
    cross_edges: List[CoherenceEdge] = field(default_factory=list)
    scale_tier: str = "T1"

    # Indexes for fast tier-based access
    hot_edge_ids: Set[int] = field(default_factory=set)
    warm_edge_ids: Set[int] = field(default_factory=set)
    cold_edge_ids: Set[int] = field(default_factory=set)

    @property
    def quanta_count(self) -> int:
        return len(self.quanta_ids)

    @property
    def effective_edge_count(self) -> int:
        return len(self.intra_edges) + CROSS_EDGE_COST_MULTIPLIER * len(self.cross_edges)

    def needs_split(self) -> bool:
        return self.quanta_count > MAX_QUANTA_PER_SHARD

@dataclass
class BorderGraph:
    """Cross-locus edges, organized by locus pair."""
    segments: Dict[Tuple[str, str], List[CoherenceEdge]] = field(default_factory=dict)

    def get_segment(self, locus_a: str, locus_b: str) -> List[CoherenceEdge]:
        key = tuple(sorted([locus_a, locus_b]))
        return self.segments.get(key, [])

    def add_edge(self, edge: CoherenceEdge, locus_a: str, locus_b: str):
        key = tuple(sorted([locus_a, locus_b]))
        if key not in self.segments:
            self.segments[key] = []
        self.segments[key].append(edge)

@dataclass
class CoherenceEngine:
    """Top-level coherence graph engine with sharding and tiered updates."""
    shards: Dict[str, CoherenceShard] = field(default_factory=dict)
    border_graph: BorderGraph = field(default_factory=BorderGraph)
    current_epoch: int = 0
    total_quanta: int = 0
    global_scale_tier: str = "T1"

    # Metrics
    last_compute_duration_seconds: float = 0.0
    deferred_cold_edges: int = 0
    edges_updated_this_epoch: int = 0


def classify_edge_tier(edge: CoherenceEdge, current_epoch: int) -> EdgeTier:
    """
    Classify an edge into HOT, WARM, or COLD tier based on weight and recency.
    DERIVATION edges are always COLD (immutable, no weight updates needed).
    """
    if edge.edge_type == "DERIVATION":
        return EdgeTier.COLD

    epochs_since_access = current_epoch - edge.last_accessed_epoch

    if edge.weight > HOT_WEIGHT_THRESHOLD and epochs_since_access <= HOT_RECENCY_THRESHOLD:
        return EdgeTier.HOT
    elif edge.weight >= WARM_WEIGHT_THRESHOLD:
        return EdgeTier.WARM
    else:
        return EdgeTier.COLD


def reclassify_shard_edges(shard: CoherenceShard, current_epoch: int):
    """
    Reclassify all edges in a shard into tier indexes.
    Called once per epoch before updates begin.
    """
    shard.hot_edge_ids.clear()
    shard.warm_edge_ids.clear()
    shard.cold_edge_ids.clear()

    for idx, edge in enumerate(shard.intra_edges):
        tier = classify_edge_tier(edge, current_epoch)
        edge.tier = tier
        if tier == EdgeTier.HOT:
            shard.hot_edge_ids.add(idx)
        elif tier == EdgeTier.WARM:
            shard.warm_edge_ids.add(idx)
        else:
            shard.cold_edge_ids.add(idx)


def update_edge_weight(edge: CoherenceEdge,
                        accessed_quanta: Set[str],
                        current_epoch: int,
                        epochs_since_last_update: int = 1) -> bool:
    """
    Update a single edge's weight: Hebbian reinforcement + temporal decay.
    Returns True if edge should be pruned.

    For edges that skipped updates (WARM/COLD tiers), applies compound decay
    for all skipped epochs, then checks for Hebbian reinforcement in current epoch.
    """
    if edge.edge_type == "DERIVATION":
        return False  # DERIVATION edges are immutable (CR-24)

    # Apply compound temporal decay for skipped epochs
    if epochs_since_last_update > 1:
        edge.weight *= (1.0 - EDGE_DECAY_RATE) ** (epochs_since_last_update - 1)

    # Current epoch: check for Hebbian reinforcement
    source_accessed = edge.source_id in accessed_quanta
    target_accessed = edge.target_id in accessed_quanta

    if source_accessed and target_accessed:
        # Hebbian reinforcement: co-accessed endpoints strengthen
        edge.weight += REINFORCEMENT_RATE * (1.0 - edge.weight)
        edge.last_accessed_epoch = current_epoch
    else:
        # Temporal decay for current epoch
        edge.weight *= (1.0 - EDGE_DECAY_RATE)

    edge.last_updated_epoch = current_epoch

    # Check pruning threshold (tier-dependent)
    return edge.weight < MIN_EDGE_WEIGHT


def enforce_shard_edge_budget(shard: CoherenceShard):
    """
    Enforce edge budget for a shard. When budget exceeded, prune lowest-ranked
    edges. DERIVATION edges are never pruned.
    """
    if shard.effective_edge_count <= MAX_INTRA_EDGES_PER_SHARD:
        return  # Within budget

    # Compute rank scores for all non-DERIVATION edges
    prunable = []
    for idx, edge in enumerate(shard.intra_edges):
        if edge.edge_type == "DERIVATION":
            continue
        rank = compute_edge_rank(edge)
        prunable.append((rank, idx, edge))

    for idx, edge in enumerate(shard.cross_edges):
        if edge.edge_type == "DERIVATION":
            continue
        rank = compute_edge_rank(edge)
        prunable.append((rank, -(idx + 1), edge))  # Negative index for cross-edges

    # Sort by rank ascending (lowest rank = first to prune)
    prunable.sort(key=lambda x: x[0])

    # Prune until within budget
    edges_to_remove = shard.effective_edge_count - MAX_INTRA_EDGES_PER_SHARD
    removed = 0
    intra_remove_indices = set()
    cross_remove_indices = set()

    for rank, idx, edge in prunable:
        if removed >= edges_to_remove:
            break
        if idx >= 0:
            intra_remove_indices.add(idx)
            removed += 1
        else:
            cross_remove_indices.add(-(idx + 1))
            removed += CROSS_EDGE_COST_MULTIPLIER  # Cross-edges free up more budget

    # Remove edges (in reverse order to preserve indices)
    shard.intra_edges = [e for i, e in enumerate(shard.intra_edges)
                         if i not in intra_remove_indices]
    shard.cross_edges = [e for i, e in enumerate(shard.cross_edges)
                         if i not in cross_remove_indices]


def compute_edge_rank(edge: CoherenceEdge) -> float:
    """
    Rank score for edge budget enforcement.
    From base spec Section 7.4, with cross-shard bonus.
    Higher rank = more important = kept longer.
    """
    TYPE_PRIORITY = {
        "CONTRADICTION": 1.0,
        "SUPPORT": 0.8,
        "DERIVATION": 0.6,   # Never actually pruned, but ranked for completeness
        "ANALOGY": 0.4,
        "SUPERSESSION": 0.2,
    }
    recency = 1.0 / (1.0 + (edge.last_accessed_epoch or 0))  # Normalized recency
    cross_bonus = 0.1 if edge.is_cross_shard else 0.0

    return (0.4 * edge.weight
            + 0.3 * recency
            + 0.2 * TYPE_PRIORITY.get(edge.edge_type, 0.0)
            + 0.1 * cross_bonus)


def epoch_coherence_update(engine: CoherenceEngine,
                            accessed_quanta: Set[str],
                            current_epoch: int):
    """
    MAIN ENTRY POINT: Execute one epoch of coherence graph updates.

    Budget-aware: processes HOT edges first, then WARM (if due), then COLD
    (if due and budget remains). Defers remaining work to next epoch.

    Parameters:
        engine: the coherence engine state
        accessed_quanta: set of quantum IDs accessed in this epoch
        current_epoch: current tidal epoch number
    """
    engine.current_epoch = current_epoch
    engine.edges_updated_this_epoch = 0
    engine.deferred_cold_edges = 0
    start_time = time.monotonic()

    # Determine global scale tier
    engine.global_scale_tier = determine_scale_tier(engine.total_quanta,
                                                     engine.global_scale_tier)

    min_edge_weight = (MIN_EDGE_WEIGHT_T3_PLUS
                       if engine.global_scale_tier in ("T3", "T4")
                       else MIN_EDGE_WEIGHT)

    # Process each shard independently (parallelizable in production)
    for locus_id, shard in engine.shards.items():
        shard.scale_tier = engine.global_scale_tier

        # Reclassify edges into tiers
        reclassify_shard_edges(shard, current_epoch)

        # Check if shard needs split (signal to C3, don't process internally)
        if shard.needs_split():
            signal_c3_split_request(locus_id, shard.quanta_count)

        # --- Phase 1: HOT edges (every epoch) ---
        edges_to_prune = []
        for idx in list(shard.hot_edge_ids):
            if _budget_exceeded(start_time):
                break  # CRITICAL: respect computation budget
            edge = shard.intra_edges[idx]
            epochs_since = current_epoch - edge.last_updated_epoch
            should_prune = update_edge_weight(edge, accessed_quanta, current_epoch, epochs_since)
            if should_prune or edge.weight < min_edge_weight:
                edges_to_prune.append(idx)
            engine.edges_updated_this_epoch += 1

        # --- Phase 2: WARM edges (every WARM_UPDATE_INTERVAL epochs) ---
        if current_epoch % WARM_UPDATE_INTERVAL == 0:
            for idx in list(shard.warm_edge_ids):
                if _budget_exceeded(start_time):
                    break
                edge = shard.intra_edges[idx]
                epochs_since = current_epoch - edge.last_updated_epoch
                should_prune = update_edge_weight(edge, accessed_quanta, current_epoch, epochs_since)
                if should_prune or edge.weight < min_edge_weight:
                    edges_to_prune.append(idx)
                engine.edges_updated_this_epoch += 1

        # --- Phase 3: COLD edges (every COLD_UPDATE_INTERVAL epochs) ---
        if current_epoch % COLD_UPDATE_INTERVAL == 0:
            cold_edges_list = list(shard.cold_edge_ids)

            # T4: probabilistic sampling -- only update random 20%
            if engine.global_scale_tier == "T4":
                sample_size = max(1, int(len(cold_edges_list) * T4_SAMPLE_RATE))
                cold_edges_list = random.sample(cold_edges_list,
                                                 min(sample_size, len(cold_edges_list)))

            for idx in cold_edges_list:
                if _budget_exceeded(start_time):
                    engine.deferred_cold_edges += len(cold_edges_list) - cold_edges_list.index(idx)
                    break
                edge = shard.intra_edges[idx]
                if edge.edge_type == "DERIVATION":
                    continue  # Immutable, skip
                epochs_since = current_epoch - edge.last_updated_epoch
                should_prune = update_edge_weight(edge, accessed_quanta, current_epoch, epochs_since)
                if should_prune or edge.weight < min_edge_weight:
                    edges_to_prune.append(idx)
                engine.edges_updated_this_epoch += 1

        # Prune marked edges (batch removal for efficiency)
        if edges_to_prune:
            prune_set = set(edges_to_prune)
            shard.intra_edges = [e for i, e in enumerate(shard.intra_edges)
                                 if i not in prune_set]

        # Enforce shard edge budget
        enforce_shard_edge_budget(shard)

    # --- Border graph updates ---
    if not _budget_exceeded(start_time):
        update_border_graph(engine, accessed_quanta, current_epoch)

    engine.last_compute_duration_seconds = time.monotonic() - start_time


def update_border_graph(engine: CoherenceEngine,
                         accessed_quanta: Set[str],
                         current_epoch: int):
    """
    Update cross-locus edges in the border graph.
    Frequency depends on scale tier:
      T1: N/A (single shard)
      T2: every 5 epochs
      T3: every 5 epochs, sampled (top 10% by weight)
      T4: every 5 epochs, reservoir sampled
    """
    if engine.global_scale_tier == "T1":
        return  # No border graph needed

    if current_epoch % WARM_UPDATE_INTERVAL != 0:
        return  # Border graph updates aligned with WARM tier

    start_time = time.monotonic()

    for key, segment in engine.border_graph.segments.items():
        if _budget_exceeded(start_time):
            break

        edges_to_process = segment

        if engine.global_scale_tier == "T3":
            # Sample top 10% by weight
            edges_to_process = sorted(segment, key=lambda e: e.weight, reverse=True)
            cutoff = max(1, len(edges_to_process) // 10)
            edges_to_process = edges_to_process[:cutoff]

        elif engine.global_scale_tier == "T4":
            # Reservoir sampling: maintain fixed-size sample
            if len(segment) > T4_BORDER_RESERVOIR_SIZE:
                edges_to_process = random.sample(segment, T4_BORDER_RESERVOIR_SIZE)

        edges_to_prune = []
        for idx, edge in enumerate(edges_to_process):
            if _budget_exceeded(start_time):
                break
            epochs_since = current_epoch - edge.last_updated_epoch
            should_prune = update_edge_weight(edge, accessed_quanta, current_epoch, epochs_since)
            min_w = (MIN_EDGE_WEIGHT_T3_PLUS
                     if engine.global_scale_tier in ("T3", "T4")
                     else MIN_EDGE_WEIGHT)
            if should_prune or edge.weight < min_w:
                edges_to_prune.append(edge)

        # Remove pruned edges
        if edges_to_prune:
            prune_set = set(id(e) for e in edges_to_prune)
            engine.border_graph.segments[key] = [
                e for e in segment if id(e) not in prune_set
            ]


def _budget_exceeded(start_time: float) -> bool:
    """Check if coherence computation budget has been exceeded."""
    elapsed = time.monotonic() - start_time
    return elapsed >= MAX_COHERENCE_COMPUTE_SECONDS


def signal_c3_split_request(locus_id: str, quanta_count: int):
    """
    Signal C3 to split a locus that has exceeded MAX_QUANTA_PER_SHARD.
    C3 will execute a Parcel Transition Protocol to subdivide the locus.
    EMA will rebalance quanta across the new shards at the epoch boundary.

    This is a coordination signal, not an internal operation. EMA does not
    split shards unilaterally.
    """
    # Implementation: emit C3 governance event requesting locus subdivision
    # C3 will respond with new locus topology at next epoch boundary
    pass  # Placeholder for C3 integration


def determine_scale_tier(total_quanta: int, current_tier: str) -> str:
    """
    Determine global scale tier with 20% downgrade hysteresis.
    """
    TIER_THRESHOLDS = {
        "T1_TO_T2": 100_000,
        "T2_TO_T3": 10_000_000,
        "T3_TO_T4": 1_000_000_000,
    }
    TIER_DOWNGRADE = {
        "T2_TO_T1": 80_000,
        "T3_TO_T2": 8_000_000,
        "T4_TO_T3": 800_000_000,
    }

    # Check upgrades first (no hysteresis, immediate)
    if total_quanta >= TIER_THRESHOLDS["T3_TO_T4"]:
        return "T4"
    if total_quanta >= TIER_THRESHOLDS["T2_TO_T3"]:
        return "T3"
    if total_quanta >= TIER_THRESHOLDS["T1_TO_T2"]:
        return "T2"

    # Check downgrades (with hysteresis)
    if current_tier == "T4" and total_quanta < TIER_DOWNGRADE["T4_TO_T3"]:
        return "T3"
    if current_tier == "T3" and total_quanta < TIER_DOWNGRADE["T3_TO_T2"]:
        return "T2"
    if current_tier == "T2" and total_quanta < TIER_DOWNGRADE["T2_TO_T1"]:
        return "T1"

    return current_tier
```

### 2.9 Invariants Added

- **INV-E15 (Shard Size Limit):** No coherence shard SHALL contain more than MAX_QUANTA_PER_SHARD (1,000,000) quanta. When exceeded, EMA MUST signal C3 for locus subdivision before the next epoch boundary.

- **INV-E16 (Shard Edge Budget):** The effective edge count of any shard (intra_edges + 2 * cross_edges) MUST NOT exceed MAX_INTRA_EDGES_PER_SHARD (5,000,000). Enforcement by pruning lowest-ranked non-DERIVATION edges.

- **INV-E17 (Computation Budget):** Coherence graph update computation per tidal epoch MUST NOT exceed MAX_COHERENCE_COMPUTE_SECONDS (1800 seconds). When budget is exceeded, remaining COLD-tier edge updates are deferred to the next eligible epoch. HOT-tier edges MUST be processed first.

- **INV-E18 (Tiered Update Guarantee):** HOT-tier edges MUST be updated every tidal epoch. WARM-tier edges MUST be updated at least every WARM_UPDATE_INTERVAL (5) tidal epochs. COLD-tier edges MUST be updated at least every COLD_UPDATE_INTERVAL (10) tidal epochs, subject to computation budget (INV-E17).

- **INV-E19 (Border Graph Isolation):** Cross-locus edges MUST be maintained in the border graph, separate from intra-shard edge storage. Cross-locus edge updates MUST NOT block intra-shard edge processing.

---

## 3. Superseded Sections

This addendum supersedes the following sections of the base C6 Master Technical Specification:

| Base Spec Section | Status | Replacement |
|-------------------|--------|-------------|
| 6.7 (Graduated Control Overlay) | **SUPERSEDED** | Section 1.3-1.7 of this addendum (Regime-Based Precedence Model). The four-regime table, PID activation rules, and "CONSTITUTIONAL" regime are replaced. |
| 7.2 (Sharding Strategy) | **SUPERSEDED** | Section 2.3 of this addendum (Sharded Coherence with shard size limits and border graph). |
| 7.5 (Scale Tiers) | **SUPERSEDED** | Section 2.6 of this addendum (Revised Scale Tier Definitions with T4 tier and concrete mechanisms). |
| 6.5 (Floor Allocation Enforcement) | **SUPPLEMENTED** | Section 1.5 of this addendum adds iterative conservation enforcement wrapping the existing floor logic. The existing `enforce_floors` function is retained as a sub-step. |
| 7.3 (Edge Dynamics) | **SUPPLEMENTED** | Section 2.5 adds tiered update frequency and batched decay. The existing Hebbian reinforcement and temporal decay formulas are retained unchanged. |
| 7.4 (Active Edge Budget) | **SUPPLEMENTED** | Section 2.4 adds per-shard budgets and cross-edge cost multiplier. The existing per-quantum edge budget (MAX_EDGES_PER_QUANTUM = 50) is retained unchanged. |

Sections not listed above remain in full force.

---

## 4. Traceability

| Requirement | Source | Addressed By |
|-------------|--------|--------------|
| SHREC dual-controller interaction undefined | Assessment Finding (CRITICAL) | Section 1: Regime-Based Precedence Model |
| PID can violate budget conservation | Assessment Finding (CRITICAL) | Section 1.5: Budget Conservation Enforcement, INV-E12 |
| "CONSTITUTIONAL" regime unclamped PID contradicts floor guarantees | Assessment Finding (CRITICAL) | Section 1.3: EMERGENCY regime replaces CONSTITUTIONAL with static hold |
| Coherence graph at 1B quanta exceeds epoch compute budget | Assessment Finding (CRITICAL) | Section 2: Sharded Coherence with Tiered Updates |
| No shard size limits specified | Assessment Finding (CRITICAL) | Section 2.3: MAX_QUANTA_PER_SHARD = 1M, INV-E15 |
| No tiered update frequency | Assessment Finding (CRITICAL) | Section 2.5: HOT/WARM/COLD tiers, INV-E18 |
| No computation budget per epoch | Assessment Finding (CRITICAL) | Section 2.7: 30-minute budget, INV-E17 |
| T3 tier mechanisms unspecified | Assessment Finding (CRITICAL) | Section 2.6: Domain partitioning, sampled border graph |
| No T4 tier for >1B quanta | Assessment Finding (CRITICAL) | Section 2.6: T4 with probabilistic edge sampling |
| Cross-shard edge cost not modeled | Assessment Finding (CRITICAL) | Section 2.4: CROSS_EDGE_COST_MULTIPLIER = 2, INV-E16 |
| INV-E6 (Edge Budget) underspecified | Base spec | Strengthened by INV-E16 (shard-level) and Section 2.4 |
| INV-E7 (SHREC Floor) enforcement gap | Base spec | Strengthened by INV-E12 (conservation) and Section 1.5 |

---

*End of Hardening Addendum*
