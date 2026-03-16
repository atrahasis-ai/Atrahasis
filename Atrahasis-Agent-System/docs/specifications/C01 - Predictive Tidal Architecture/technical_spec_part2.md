# C1 — Predictive Tidal Architecture (PTA): Technical Specification — Part 2

**Invention ID:** C1
**Stage:** DESIGN
**Date:** 2026-03-09
**Status:** DRAFT
**Supplements:** Technical Specification Part 1 (Sections 1–5: Overview, Primitives, Layer 1 Tidal Backbone)

---

## 6. Predictive Delta Communication Protocol (Layer 2) — ENHANCING, NOT REQUIRED

**SCOPING NOTE:** This layer is additive. The system is fully functional with Layer 1 (Tidal Backbone) alone. Layer 2 reduces communication overhead but is not required for correct operation. All components specified in this section may be disabled without affecting scheduling correctness, settlement determinism, or verification scheduling. When Layer 2 is disabled, agents communicate via standard messaging within the tidal framework, and the settlement calculator omits the prediction bonus and surprise cost streams.

### 6.1 Per-Neighbor Prediction Model

Each agent maintains an independent linear autoregressive (AR) model for every direct neighbor. The neighbor set is bounded by the CIOS hierarchy degree (typically 4–10 neighbors).

**Model type:** Linear autoregressive model with exogenous features (ARX).

**Feature vector:** For neighbor *i* at epoch *t*, the observation vector is:

```
x_i(t) = [
    tidal_compliance_rate,        // fraction of assigned tasks completed on schedule, ∈ [0, 1]
    task_completion_time_delta,   // (actual - expected) completion time, normalized, ∈ ℝ
    resource_utilization_delta,   // (actual - expected) resource consumption, normalized, ∈ ℝ
    surprise_count_window         // count of surprise signals generated in trailing window, ∈ ℕ
]
```

Feature dimension: *d* = 4.

**Model definition:** The prediction for neighbor *i* at epoch *t+1* given observations through epoch *t* is:

```
x̂_i(t+1) = W_i(t) · x_i(t)
```

where **W_i(t)** ∈ ℝ^(d×d) is the weight matrix for neighbor *i*, updated via Recursive Least Squares (RLS).

**Update rule — Recursive Least Squares (RLS) with forgetting factor:**

Let λ ∈ (0, 1] be the forgetting factor (recommended default: λ = 0.98). Higher values weight historical data more; lower values adapt faster to non-stationarity.

Given a new observation x_i(t+1):

1. Compute prediction error:
```
e_i(t+1) = x_i(t+1) - W_i(t) · x_i(t)
```

2. Compute gain vector:
```
k_i(t+1) = P_i(t) · x_i(t) / (λ + x_i(t)ᵀ · P_i(t) · x_i(t))
```

3. Update weight matrix:
```
W_i(t+1) = W_i(t) + e_i(t+1) · k_i(t+1)ᵀ
```

4. Update covariance matrix:
```
P_i(t+1) = (1/λ) · (P_i(t) - k_i(t+1) · x_i(t)ᵀ · P_i(t))
```

**Initialization:**

```
W_i(0) = 0_(d×d)              // zero matrix (predict zero deviation)
P_i(0) = δ · I_(d×d)          // δ = 100.0 (high initial uncertainty)
```

**Computational complexity:**

| Operation | Complexity |
|---|---|
| Initialization | O(d²) |
| Per-update (steps 1–4) | O(d²) |
| Per-prediction | O(d) for matrix-vector multiply |

Since d = 4, all operations are constant-time in practice: O(16) multiplications per update, O(4) per prediction.

**Memory per neighbor:** O(d² + d) = O(20) floating-point values (16 for W, 16 for P, 4 for the last observation vector). Approximately 288 bytes per neighbor at 64-bit precision.

**Total memory for prediction models:** O(D × (d² + d)) where D is the neighbor degree. At D = 10, d = 4: approximately 2.9 KB per agent.

---

### 6.2 Adaptive Surprise Threshold

Each agent maintains an independent adaptive threshold θ_i(t) for each neighbor *i*, governing when a prediction error is large enough to constitute a "surprise" that must be communicated.

**Threshold function:** θ_i(t) ∈ [θ_min, θ_max] for neighbor *i* at epoch *t*.

**Adaptation rules:**

*Tightening* (prediction was accurate — reduce future communication):
```
If ‖e_i(t)‖₂ < θ_i(t):
    θ_i(t+1) = max(θ_min, θ_i(t) × α)
```
where α ∈ (0.9, 0.99) is the tightening rate (recommended default: α = 0.95).

*Loosening* (prediction was inaccurate — increase future communication):
```
If ‖e_i(t)‖₂ ≥ θ_i(t):
    θ_i(t+1) = min(θ_max, θ_i(t) × β)
```
where β ∈ (1.01, 1.1) is the loosening rate (recommended default: β = 1.05).

**Parameter bounds:**

| Parameter | Symbol | Default | Purpose |
|---|---|---|---|
| Minimum threshold | θ_min | 0.01 | Prevents zero-communication deadlock; ensures periodic surprise signals even with perfect predictions |
| Maximum threshold | θ_max | 10.0 | Upper bound equivalent to standard messaging (all deviations are surprises) |
| Initial threshold | θ_init | 1.0 | Starting point; agents begin with moderate sensitivity |
| Tightening rate | α | 0.95 | Per-epoch multiplicative decrease when prediction is accurate |
| Loosening rate | β | 1.05 | Per-epoch multiplicative increase when prediction is inaccurate |

**Non-stationarity detector:**

To detect regime changes where the prediction model is systematically failing, a variance-based non-stationarity detector operates alongside the threshold adapter:

```
σ²_i(t) = (1 - γ) · σ²_i(t-1) + γ · ‖e_i(t)‖₂²
```

where γ ∈ (0, 1) is the smoothing constant (recommended default: γ = 0.1).

If σ²_i(t) > ψ × σ²_i(t-1) for ψ > 1 (recommended default: ψ = 2.0), a non-stationarity event is declared for neighbor *i*, triggering:
1. Threshold is immediately set to θ_max (revert to full communication for this neighbor).
2. The prediction model forgetting factor λ is temporarily reduced to λ_fast = 0.90 for accelerated adaptation.
3. After the model re-converges (accuracy above a recovery threshold for η consecutive epochs, default η = 5), normal threshold adaptation resumes.

**Hysteresis guard:** To prevent oscillation, threshold adjustments are gated: after a loosening event, tightening is inhibited for a configurable cooldown period (default: 3 epochs). This prevents rapid oscillation between tight and loose thresholds when the prediction error hovers near the boundary.

---

### 6.3 Surprise Signal Specification

**Message format:**

```
SurpriseSignal {
    source_id:    AgentID   // originator of the deviation
    epoch:        uint64    // epoch in which the deviation was observed
    error_vector: float[d]  // prediction error vector (d = 4)
    magnitude:    float     // L2 norm of error_vector
    ttl:          uint8     // maximum remaining hops
    hop_count:    uint8     // hops traversed so far
}
```

**Magnitude computation:**

```
magnitude = ‖e_i(t)‖₂ = sqrt(Σ_{j=1}^{d} e_i(t)_j²)
```

A surprise signal is emitted if and only if magnitude > θ_i(t).

**Propagation radius:**

The propagation radius determines how far a surprise signal travels through the CIOS topology:

```
r = min(r_max, floor(log₂(magnitude / θ_base)))
```

where:
- θ_base is the base threshold for radius calculation (default: θ_init = 1.0)
- r_max is the maximum propagation radius (governance parameter, default: 8 hops)

This yields:
- magnitude ∈ [θ_base, 2·θ_base): r = 0 (local only, no propagation)
- magnitude ∈ [2·θ_base, 4·θ_base): r = 1 (immediate neighbors)
- magnitude ∈ [4·θ_base, 8·θ_base): r = 2
- ...and so on, logarithmically

**Damping:**

At each hop, the signal magnitude is reduced by a damping factor δ ∈ (0, 1) (default: δ = 0.7):

```
magnitude_at_hop_h = magnitude_original × δ^h
```

An intermediate agent re-propagates the signal only if the damped magnitude still exceeds its own threshold for the source agent. This naturally limits cascade propagation.

**TTL enforcement:**

```
ttl_initial = r                         // set to computed propagation radius
ttl_at_hop = ttl_initial - hop_count    // decremented at each hop
```

Signal is dropped when ttl_at_hop ≤ 0, regardless of remaining magnitude.

**Deduplication:**

Each agent maintains a deduplication cache keyed by the tuple (source_id, epoch). A signal is processed at most once per (source_id, epoch) pair. Cache entries are evicted after 2 epoch boundaries.

**Per-epoch signal budget:**

Each agent has a hard cap of B_max surprise signals it may originate per epoch (default: B_max = 50). Signals beyond this cap are dropped and logged. This prevents surprise flooding attacks and bounds worst-case communication.

---

### 6.4 Cold-Start Protocol

When a neighbor relationship is newly established (agent join, cluster reformation, or model reset), the prediction model has no history and cannot produce accurate predictions.

**Initial state:** The communication mode for the new neighbor is set to STANDARD. In STANDARD mode, all observation data is transmitted as if every observation were a surprise (equivalent to θ_i = 0).

**Transition criterion:** The neighbor communication mode transitions from STANDARD to PREDICTIVE when:

```
model_accuracy_i(t) > acc_threshold   for   consecutive_epochs_threshold consecutive epochs
```

where:
- model_accuracy_i(t) = 1 - (mean_absolute_error_i(t) / mean_observation_magnitude_i(t))
- acc_threshold = 0.7 (70% model accuracy; configurable)
- consecutive_epochs_threshold = 5 (configurable)

**Transition sequence:**

1. STANDARD: all messages sent (epochs 0 through qualification start)
2. TRANSITIONING: model accuracy is being evaluated, messages still sent in full (qualification window)
3. PREDICTIVE: only surprises sent (steady state)

Transition from STANDARD to TRANSITIONING is implicit when model_accuracy_i first exceeds acc_threshold. Transition from TRANSITIONING to PREDICTIVE occurs after consecutive_epochs_threshold consecutive epochs above acc_threshold.

**Per-neighbor independence:** Each neighbor transitions independently. Agent A may be in PREDICTIVE mode for neighbor B and STANDARD mode for neighbor C simultaneously.

**Revert criterion:** If model accuracy drops below revert_threshold = 0.5 (configurable) at any point during PREDICTIVE mode, the neighbor reverts to STANDARD mode immediately. The model may be reset to initial state (W = 0, P = δI) if the revert is triggered by a non-stationarity event.

---

### 6.5 Model Recalibration

At every epoch boundary, all prediction models undergo mandatory recalibration to prevent silent drift.

**Recalibration procedure:**

1. **Observation collection:** Gather the complete epoch's observations for each neighbor: actual tidal compliance, task completion times, resource utilization, and surprise counts.

2. **Retrospective accuracy assessment:** For each neighbor *i*, compute the epoch-level prediction accuracy:
```
epoch_accuracy_i = 1 - (1/T) · Σ_{t ∈ epoch} ‖e_i(t)‖₂ / ‖x_i(t)‖₂
```
where T is the number of observation steps within the epoch.

3. **Drift detection:** Compare the epoch-level accuracy against the running average accuracy:
```
drift_detected_i = (|epoch_accuracy_i - running_accuracy_i| > drift_threshold)
```
where drift_threshold = 0.2 (default).

4. **Conditional actions:**
   - If drift NOT detected: continue with current model parameters; update running_accuracy_i with exponential moving average.
   - If drift detected: reset the forgetting factor to λ_fast = 0.90 for the next epoch to accelerate adaptation. If drift persists for 3 consecutive epochs, fully reset the model (W = 0, P = δI) and revert to STANDARD mode.

5. **Threshold synchronization:** After recalibration, re-evaluate the threshold θ_i based on the recalibrated model's accuracy. If the model was reset, θ_i is reset to θ_init.

**Pseudocode:**

```
function recalibrate_models(epoch_observations: Map<AgentID, Observation[]>) -> Map<AgentID, Model>:
    for each neighbor_id, observations in epoch_observations:
        model = get_model(neighbor_id)

        // Step 2: Retrospective accuracy
        total_error = 0.0
        total_magnitude = 0.0
        for obs in observations:
            predicted = model.predict(obs.previous_state)
            error = obs.actual - predicted
            total_error += norm(error)
            total_magnitude += norm(obs.actual)

        epoch_accuracy = 1.0 - (total_error / max(total_magnitude, EPSILON))

        // Step 3: Drift detection
        drift_magnitude = abs(epoch_accuracy - model.running_accuracy)

        if drift_magnitude > DRIFT_THRESHOLD:
            model.consecutive_drift_count += 1
            if model.consecutive_drift_count >= 3:
                // Full reset
                model.W = zeros(d, d)
                model.P = DELTA * identity(d)
                model.communication_mode = STANDARD
                model.threshold = THETA_INIT
                model.consecutive_drift_count = 0
            else:
                // Accelerated adaptation
                model.lambda = LAMBDA_FAST
        else:
            model.consecutive_drift_count = 0
            model.lambda = LAMBDA_DEFAULT

        // Step 5: Update running accuracy
        model.running_accuracy = (1 - ACCURACY_EMA_ALPHA) * model.running_accuracy
                                 + ACCURACY_EMA_ALPHA * epoch_accuracy

        // Re-evaluate threshold
        if model.communication_mode == STANDARD:
            model.threshold = THETA_INIT

        store_model(neighbor_id, model)

    return all_models
```

---

### 6.6 Algorithm Pseudocode (Layer 2)

#### 6.6.1 update_prediction_model

```
function update_prediction_model(
    neighbor_id: AgentID,
    observation: float[d]
) -> Model:
    model = get_model(neighbor_id)
    x = model.last_observation              // x_i(t)

    if x is null:
        // First observation — store and return
        model.last_observation = observation
        return model

    // Step 1: Prediction error
    prediction = model.W · x
    e = observation - prediction             // e_i(t+1)

    // Step 2: Gain vector (RLS)
    Px = model.P · x
    denominator = model.lambda + dot(x, Px)
    k = Px / denominator                     // k_i(t+1)

    // Step 3: Update weights
    model.W = model.W + outer(e, k)          // W_i(t+1)

    // Step 4: Update covariance
    model.P = (1 / model.lambda) * (model.P - outer(k, dot(x, model.P)))

    // Housekeeping
    model.last_observation = observation
    model.last_error = e
    model.error_magnitude = norm(e)

    // Update accuracy tracker
    obs_magnitude = norm(observation)
    if obs_magnitude > EPSILON:
        step_accuracy = 1.0 - (model.error_magnitude / obs_magnitude)
    else:
        step_accuracy = 1.0
    model.accuracy_ema = (1 - ACCURACY_STEP_ALPHA) * model.accuracy_ema
                         + ACCURACY_STEP_ALPHA * step_accuracy

    // Update non-stationarity detector
    model.error_variance = (1 - GAMMA) * model.error_variance
                           + GAMMA * model.error_magnitude^2

    return model
```

#### 6.6.2 compute_surprise

```
function compute_surprise(
    observation: float[d],
    prediction: float[d],
    threshold: float,
    source_id: AgentID,
    epoch: uint64
) -> SurpriseSignal | null:
    error_vector = observation - prediction
    magnitude = norm(error_vector)

    if magnitude <= threshold:
        return null                          // No surprise — silence

    radius = min(R_MAX, floor(log2(magnitude / THETA_BASE)))
    radius = max(0, radius)

    return SurpriseSignal {
        source_id:    source_id,
        epoch:        epoch,
        error_vector: error_vector,
        magnitude:    magnitude,
        ttl:          radius,
        hop_count:    0
    }
```

#### 6.6.3 propagate_surprise

```
function propagate_surprise(
    signal: SurpriseSignal,
    neighbors: AgentID[]
) -> SurpriseSignal[]:
    // Check deduplication
    dedup_key = (signal.source_id, signal.epoch)
    if dedup_key in dedup_cache:
        return []
    dedup_cache.insert(dedup_key)

    // Check TTL
    if signal.ttl <= 0:
        return []

    // Check per-epoch signal budget
    if signals_originated_this_epoch >= B_MAX and signal.hop_count == 0:
        log_warning("Signal budget exceeded, dropping outbound surprise")
        return []

    forwarded = []
    for neighbor in neighbors:
        // Apply damping
        damped_magnitude = signal.magnitude * DELTA_DAMPING ^ signal.hop_count

        // Only forward if damped magnitude exceeds neighbor's threshold
        neighbor_threshold = get_threshold_for_source(neighbor, signal.source_id)
        if damped_magnitude > neighbor_threshold:
            forwarded_signal = SurpriseSignal {
                source_id:    signal.source_id,
                epoch:        signal.epoch,
                error_vector: signal.error_vector * (damped_magnitude / signal.magnitude),
                magnitude:    damped_magnitude,
                ttl:          signal.ttl - 1,
                hop_count:    signal.hop_count + 1
            }
            send_to(neighbor, forwarded_signal)
            forwarded.append(forwarded_signal)

    // Record for settlement
    record_surprise_event(signal)

    return forwarded
```

#### 6.6.4 recalibrate_models

See Section 6.5 for the complete recalibration pseudocode. The function signature is:

```
function recalibrate_models(
    epoch_observations: Map<AgentID, Observation[]>
) -> Map<AgentID, Model>
```

This function is invoked at Step 4 of the Epoch Boundary Processing sequence (architecture document Section 3.3).

---

## 7. Morphogenic Field Protocol (Layer 3) — DECISION GATE AT PHASE 2 END

**SCOPING NOTE:** This layer carries a formal decision gate. Implementation proceeds only if Phase 2 evaluation confirms net value over simple load-balancing heuristics within tetrahedral clusters. The gate criteria are: (1) Phase 2 validation criteria are met, (2) potential game convergence is validated in simulation (per Experiment 4 in the refined concept), (3) measurable improvement over round-robin allocation is demonstrated in simulated tetrahedral clusters. If the gate criteria are not met, Layer 3 is either simplified to a static load-balancing rule within clusters or dropped entirely. Layers 1 and 2 are unaffected by the gate outcome.

### 7.1 Potential Game Framework

Layer 3 models sub-epoch task allocation within tetrahedral (4-agent) clusters as a potential game, guaranteeing convergence to Nash equilibrium.

**Definitions:**

Let *C* = {a₁, a₂, a₃, a₄} be a tetrahedral cluster of 4 agents.

Let *K* be the number of available task types within the cluster. Each agent *i* maintains a strategy vector:

```
s_i ∈ Δ^K    (the K-dimensional simplex)
```

where s_i[k] represents the fraction of agent *i*'s capacity allocated to task type *k*, subject to:

```
Σ_{k=1}^{K} s_i[k] = 1,    s_i[k] ≥ 0    ∀k
```

The joint strategy profile is **s** = (s₁, s₂, s₃, s₄).

**Potential function:**

Define the global potential function Φ: S → ℝ over the cluster state space *S* = (Δ^K)⁴:

```
Φ(s) = Σ_{k=1}^{K} [ D_k · log(Σ_{i=1}^{4} c_i · s_i[k] + ε) - μ · Σ_{i=1}^{4} (s_i[k] - 1/K)² ]
```

where:
- D_k ∈ ℝ≥0 is the demand weight for task type *k* (derived from task queue depths and AASL semantic urgency)
- c_i ∈ ℝ>0 is agent *i*'s capability score for the cluster's task mix (from the capacity snapshot)
- ε > 0 is a small constant to prevent log(0) (default: ε = 10⁻⁶)
- μ ≥ 0 is a regularization coefficient penalizing extreme specialization (default: μ = 0.1)

The first term drives agents to collectively cover demand proportionally to its weight. The logarithmic form ensures diminishing returns from additional allocation to well-served task types. The second term provides regularization, preventing degenerate strategies where one agent handles all of one task type.

**Potential game property:**

Define agent *i*'s local cost function:

```
J_i(s_i, s_{-i}) = -Σ_{k=1}^{K} [ D_k · c_i · s_i[k] / (Σ_{j=1}^{4} c_j · s_j[k] + ε) ] + μ · Σ_{k=1}^{K} (s_i[k] - 1/K)²
```

This is the negative marginal contribution of agent *i* to the log-capacity terms, plus the regularization cost. By construction:

```
Φ(s_i', s_{-i}) - Φ(s_i, s_{-i}) corresponds to J_i(s_i, s_{-i}) - J_i(s_i', s_{-i})
```

in the sense that any unilateral improvement by agent *i* (reducing J_i) also improves Φ. This satisfies the Monderer-Shapley potential game condition (Monderer & Shapley, "Potential Games," *Games and Economic Behavior*, 1996).

**Convergence guarantee:**

By the finite improvement property of potential games (Monderer & Shapley 1996), any sequence of best-response updates by individual agents converges to a Nash equilibrium, which is a local maximum of Φ. Since the strategy space is compact (each s_i lies on the K-simplex) and Φ is continuous, convergence is guaranteed.

**Convergence bound at 4-agent scale:**

With 4 agents and K task types (typically K ≤ 10), the strategy space is (Δ^K)⁴. Best-response updates with a gradient step converge within O(K / η) iterations, where η is the step size. At K = 10 and η = 0.1, this is approximately 100 gradient steps. Since each step is O(K) computation for 4 agents, total convergence cost is O(K² × 4) = O(400) floating-point operations — trivially fast, achievable within sub-epoch timescales.

---

### 7.2 Field Gradient Computation

**Input:**
- AASL semantic dimensions d_sem (defines the task type space K)
- Local task queue state: q_i[k] = queue depth for task type *k* at agent *i*
- Capability vector: c_i[k] = agent *i*'s efficiency for task type *k* (from AASL capability registry)
- Cluster state **s** = (s₁, s₂, s₃, s₄): current allocation strategies of all cluster members

**Demand vector computation:**

```
D_k = Σ_{i=1}^{4} q_i[k] · w_k
```

where w_k is the AASL-defined semantic urgency weight for task type *k*.

**Gradient computation:**

The gradient of Φ with respect to agent *i*'s strategy is:

```
∂Φ/∂s_i[k] = D_k · c_i / (Σ_{j=1}^{4} c_j · s_j[k] + ε) - 2μ · (s_i[k] - 1/K)
```

The full gradient vector for agent *i* is:

```
∇Φ_i = [∂Φ/∂s_i[1], ∂Φ/∂s_i[2], ..., ∂Φ/∂s_i[K]]
```

**Update rule:**

Agent *i* updates its strategy by gradient ascent on Φ (equivalently, gradient descent on J_i):

```
s_i(t+1) = Proj_Δ( s_i(t) + η · ∇Φ_i )
```

where:
- η > 0 is the step size (default: η = 0.1)
- Proj_Δ is the projection onto the K-simplex, ensuring s_i(t+1) remains a valid probability distribution

**Simplex projection** (Duchi et al. 2008):

Given an unconstrained update vector *v*, project onto Δ^K:

```
function project_simplex(v: float[K]) -> float[K]:
    sort v in descending order → v_sorted
    find ρ = max { j ∈ {1..K} : v_sorted[j] - (1/j)(Σ_{r=1}^{j} v_sorted[r] - 1) > 0 }
    τ = (1/ρ)(Σ_{r=1}^{ρ} v_sorted[r] - 1)
    return max(v - τ, 0)   // element-wise
```

**Output:** The gradient vector ∇Φ_i tells agent *i* which task types are under-served relative to demand, weighted by the agent's capability. Following the gradient increases the cluster's overall allocation efficiency.

---

### 7.3 Tidal Reset Perturbation

At each epoch boundary, a random perturbation is injected into each agent's strategy to escape local minima of the potential function. This mechanism is analogous to simulated annealing.

**Perturbation injection:**

```
s_i_perturbed = Proj_Δ( s_i + ε_i )
```

where ε_i ~ N(0, σ²I_K), a K-dimensional Gaussian with isotropic covariance.

**Annealing schedule for σ:**

```
σ(epoch) = max(σ_min, σ_initial × decay_rate^stability_count)
```

where:
- σ_initial = 0.3 (initial perturbation magnitude; configurable)
- σ_min = 0.01 (floor to ensure non-zero exploration; configurable)
- decay_rate = 0.9 (per-stable-epoch decay; configurable)
- stability_count = number of consecutive epochs where the cluster reached Nash equilibrium (convergence_status = true)

**Behavior:**
- When the cluster is new or recently reformed: σ is large, providing broad exploration.
- As the cluster stabilizes: σ decreases, refining the allocation toward the best-known equilibrium.
- If the cluster is dissolved and reformed (e.g., due to member failure), stability_count resets to 0 and σ returns to σ_initial.

**Purpose:** Without perturbation, the potential game may converge to a suboptimal local maximum of Φ. Tidal reset perturbations provide a mechanism analogous to temperature in simulated annealing: early epochs explore broadly, later epochs exploit the best-found equilibrium. The tidal boundary is a natural synchronization point — all cluster members apply perturbation simultaneously, maintaining cluster coherence.

---

### 7.4 Cluster Management Protocol

**Tetrahedron formation:**

At each tidal boundary where cluster formation is required (initial deployment, member failure requiring reformation, or governance-triggered restructuring), the Tidal Function Engine assigns agents to tetrahedral clusters.

Assignment criteria:
1. **Capability complementarity:** Prefer clusters where the union of member capabilities covers the broadest range of task types. Formally, maximize |∪_{i ∈ C} TaskTypes(i)| across clusters.
2. **Topological proximity:** Prefer clusters where members are close on the CIOS topology (minimizes intra-cluster communication latency).
3. **Load balance:** Equalize aggregate capacity across clusters.

The assignment is deterministic: given the agent roster and their capabilities, any agent can independently compute the same cluster assignments using a stable sorting algorithm over (capability_coverage, topology_distance, capacity) tuples mapped through the consistent hash ring.

**State sharing within cluster:**

Each cluster member broadcasts its local state to the other 3 members at every gradient update step:

```
ClusterStateMessage {
    agent_id:       AgentID
    epoch:          uint64
    step:           uint32          // gradient step number within epoch
    queue_depths:   float[K]        // task queue depths per type
    current_strategy: float[K]      // current allocation strategy
    capability_scores: float[K]     // per-type capability
}
```

Communication within a cluster is bounded: 3 messages per agent per gradient step, with each message of size O(K). At K = 10 and 100 gradient steps per epoch, this is 300 messages per agent per epoch — a small constant independent of total system size N.

**Dissolution triggers:**

A tetrahedral cluster is dissolved when:
- 2 or more members fail within a single epoch (detected by absence of cluster state messages for > 50% of gradient steps)
- Coherence score falls below the dissolution threshold (default: 0.3) for 3 consecutive epochs
- Governance explicitly disbands the cluster

**Reformation protocol:**

1. At the next tidal boundary following dissolution, surviving agents are placed into a reformation pool.
2. The Tidal Function Engine computes new cluster assignments from the pool plus any unassigned agents.
3. New clusters begin in cold-start state (stability_count = 0, σ = σ_initial).
4. Any in-progress work by the dissolved cluster continues under tidal backbone scheduling (Layer 1); only the intra-cluster allocation optimization is interrupted.

**Degraded operation (3-agent cluster):**

When exactly 1 member fails, the remaining 3 agents continue operating as a reduced cluster:
- The potential function is recomputed over 3 agents instead of 4.
- The failed agent's capacity share is redistributed via gradient rebalancing.
- The reduced cluster operates until the next tidal boundary, at which point it either receives a replacement member or is dissolved and reformed.

---

### 7.5 Algorithm Pseudocode (Layer 3)

#### 7.5.1 compute_field_gradient

```
function compute_field_gradient(
    cluster_state: ClusterState,
    aasl_dimensions: SemanticDimensions
) -> Map<AgentID, float[K]>:
    K = aasl_dimensions.task_type_count
    members = cluster_state.members                  // list of 4 (or 3) agents

    // Compute demand vector
    D = zeros(K)
    for agent in members:
        for k in 0..K:
            D[k] += cluster_state.queue_depth[agent][k] * aasl_dimensions.urgency_weight[k]

    gradients = {}
    for agent_i in members:
        grad = zeros(K)
        for k in 0..K:
            // Total capability-weighted allocation to task type k
            total_alloc = EPSILON
            for agent_j in members:
                total_alloc += cluster_state.capability[agent_j][k]
                               * cluster_state.strategy[agent_j][k]

            // Gradient component
            grad[k] = D[k] * cluster_state.capability[agent_i][k] / total_alloc
                      - 2 * MU * (cluster_state.strategy[agent_i][k] - 1.0 / K)

        gradients[agent_i] = grad

    return gradients
```

#### 7.5.2 update_allocation

```
function update_allocation(
    current_strategy: float[K],
    gradient: float[K],
    step_size: float
) -> float[K]:
    // Gradient ascent step
    unconstrained = current_strategy + step_size * gradient

    // Project onto simplex
    new_strategy = project_simplex(unconstrained)

    return new_strategy
```

#### 7.5.3 apply_tidal_perturbation

```
function apply_tidal_perturbation(
    strategy: float[K],
    epoch: uint64,
    stability_count: uint32
) -> float[K]:
    // Compute annealing sigma
    sigma = max(SIGMA_MIN, SIGMA_INITIAL * DECAY_RATE ^ stability_count)

    // Generate perturbation (deterministic given epoch + agent_id as seed)
    rng = seeded_rng(hash(epoch, agent_id))
    perturbation = rng.normal(mean=0, std=sigma, size=K)

    // Apply and project
    perturbed = strategy + perturbation
    perturbed = project_simplex(perturbed)

    return perturbed
```

**Note on determinism:** The perturbation uses a deterministic PRNG seeded with hash(epoch, agent_id). Given the same epoch and agent_id, any implementation produces the same perturbation vector. This preserves PTA's determinism property — cluster allocation is reproducible from shared inputs.

---

## 8. Economic Settlement Protocol

### 8.1 Settlement Timing

Settlement computation occurs at designated epoch boundaries. Not every epoch boundary is a settlement boundary; settlement frequency is a governance parameter defined in the TidalVersion (default: every epoch).

The settlement is a pure function:

```
settlement_ledger = settle(tidal_schedule, event_log, model_accuracy_records, economic_parameters)
```

Given identical inputs, any agent or auditor independently computes an identical settlement ledger.

### 8.2 Settlement Streams

The net settlement for agent *a* at settlement epoch *e* is:

```
net_settlement(a, e) = compliance_reward(a, e)
                     - surprise_cost(a, e)
                     + prediction_bonus(a, e)
                     + verification_reward(a, e)
```

#### 8.2.1 Compliance Reward

```
compliance_reward(a, e) = R_base × compliance_score(a, e)
```

where:
- R_base ∈ ℝ>0 is the base reward rate (AIC tokens per epoch; field of TidalVersion)
- compliance_score(a, e) ∈ [0, 1] measures agent *a*'s adherence to the tidal schedule in epoch *e*

Compliance score computation:

```
compliance_score(a, e) = (tasks_completed_on_time(a, e) + 0.5 × tasks_completed_late(a, e))
                         / tasks_assigned(a, e)
```

where:
- tasks_completed_on_time: assignments completed within the epoch they were scheduled
- tasks_completed_late: assignments completed in the epoch immediately following (grace period)
- tasks_assigned: total assignments from the tidal schedule for agent *a* in epoch *e*

If tasks_assigned = 0 (agent had no assignments), compliance_score = 1.0 (neutral).

#### 8.2.2 Surprise Cost

```
surprise_cost(a, e) = R_surprise × total_surprise_magnitude(a, e)
```

where:
- R_surprise ∈ ℝ≥0 is the surprise cost rate (AIC tokens per unit magnitude; field of TidalVersion)
- total_surprise_magnitude(a, e) = Σ over all surprise signals originated by agent *a* in epoch *e* of their magnitude values

This incentivizes predictable behavior. Agents that deviate from expectations pay a cost proportional to the magnitude of their deviation.

When Layer 2 is inactive (no prediction models), surprise_cost = 0 for all agents.

#### 8.2.3 Prediction Bonus

```
prediction_bonus(a, e) = R_prediction × avg_model_accuracy(a, e)
```

where:
- R_prediction ∈ ℝ≥0 is the prediction bonus rate (AIC tokens per unit accuracy; field of TidalVersion)
- avg_model_accuracy(a, e) = (1/|N(a)|) × Σ_{i ∈ N(a)} model_accuracy_a_i(e)
- N(a) is the set of agent *a*'s direct neighbors
- model_accuracy_a_i(e) is agent *a*'s prediction model accuracy for neighbor *i* in epoch *e*

This incentivizes agents to maintain accurate prediction models of their neighbors, which reduces system-wide communication overhead.

When Layer 2 is inactive, prediction_bonus = 0 for all agents.

#### 8.2.4 Verification Reward

```
verification_reward(a, e) = R_verify × verification_participation(a, e)
```

where:
- R_verify ∈ ℝ≥0 is the verification fee rate (AIC tokens per verification duty; field of TidalVersion)
- verification_participation(a, e) = count of verification duties fulfilled by agent *a* in epoch *e*, as reported by Verichain via VerificationReceipt messages

Agents that fulfill their VRF-assigned verification duties earn fees. Agents that fail to fulfill verification duties (timeout or absence) earn 0 for those duties and may incur a compliance score penalty (verification non-fulfillment counts as an incomplete assignment).

### 8.3 Determinism Guarantee

The settlement computation is deterministic if and only if all inputs are identical:

| Input | Source | Determinism property |
|---|---|---|
| tidal_schedule | Tidal Function Engine | Deterministic by construction (pure function of version + roster + epoch) |
| event_log | Local observation + received surprise signals | Eventual consistency within grace period; settlement waits for grace period |
| model_accuracy_records | Prediction Model Manager | Deterministic given identical observation sequences |
| economic_parameters | TidalVersion | Deterministic; updated only at version boundaries |

**Grace period:** Settlement computation is deferred by grace_period epochs (default: 1) after the settlement epoch boundary to allow late-arriving events to be incorporated. Events arriving after the grace period are excluded from that epoch's settlement and cannot be retroactively applied.

**Settlement proof:** After computation, a deterministic hash is generated over all inputs and the resulting ledger:

```
settlement_proof = SHA-256(
    canonical_serialize(tidal_schedule) ||
    canonical_serialize(event_log) ||
    canonical_serialize(model_accuracy_records) ||
    canonical_serialize(economic_parameters) ||
    canonical_serialize(settlement_ledger)
)
```

Any auditor with the same inputs can verify the proof by recomputing the settlement.

### 8.4 Parameter Governance

All economic parameters (R_base, R_surprise, R_prediction, R_verify) are fields of the TidalVersion data structure. They are updated only at version boundaries, never mid-version. This ensures that all agents within a version compute settlements using identical rates.

Rate changes follow the tidal version migration protocol (Section 9): proposed in a new version, evaluated during the overlap period, and activated only upon successful migration.

---

## 9. Tidal Version Management Protocol

### 9.1 Version Lifecycle

A TidalVersion progresses through five states:

```
PROPOSED → PUBLISHED → OVERLAP → ACTIVE → DEPRECATED
```

**State definitions:**

| State | Description |
|---|---|
| PROPOSED | Version definition submitted by governance; not yet visible to agents |
| PUBLISHED | Version definition distributed to all agents; evaluation may begin but no execution |
| OVERLAP | Both the current ACTIVE version and this version are evaluated simultaneously |
| ACTIVE | This version is the primary execution version for the system |
| DEPRECATED | This version has been superseded; retained for audit trail only |

### 9.2 State Transitions

```
PROPOSED --[governance approval]--> PUBLISHED
PUBLISHED --[activation_epoch reached]--> OVERLAP
OVERLAP --[migration_threshold met]--> ACTIVE (previous version → DEPRECATED)
OVERLAP --[overlap_duration expired without threshold]--> (this version discarded; previous remains ACTIVE)
ACTIVE --[new version enters OVERLAP]--> (remains ACTIVE until new version reaches ACTIVE)
ACTIVE --[governance deprecation]--> DEPRECATED
```

**Transition triggers:**

| Transition | Trigger | Authority |
|---|---|---|
| PROPOSED → PUBLISHED | Governance approval | Human governance |
| PUBLISHED → OVERLAP | Current epoch ≥ activation_epoch | Automatic (deterministic) |
| OVERLAP → ACTIVE | observed_fraction_on_new ≥ migration_threshold | Per-agent Schelling point decision |
| OVERLAP → discarded | Current epoch ≥ activation_epoch + overlap_duration AND observed_fraction_on_new < migration_threshold | Automatic (deterministic) |
| ACTIVE → DEPRECATED | New version reaches ACTIVE state | Automatic |

### 9.3 Overlap Period

**Duration:** Governance parameter overlap_duration (default: 10 epochs). This is the maximum time agents have to migrate to the new version.

**Dual evaluation:** During the overlap period, each agent computes assignments under both the current ACTIVE version and the OVERLAP version:

```
schedule_current = evaluate(agent_id, task_types, epoch, active_version)
schedule_new     = evaluate(agent_id, task_types, epoch, overlap_version)
```

The agent executes schedule_current while computing schedule_new for comparison. This allows agents to observe whether the new version produces acceptable assignments before switching.

**Migration signal (Schelling point dynamics):**

Each agent independently decides when to switch its primary execution to the new version. The decision rule is:

```
if fraction_of_observed_peers_on_new_version ≥ migration_threshold:
    switch_to_new_version()
```

where:
- migration_threshold ∈ (0.5, 1.0) (governance parameter, default: 0.67)
- The fraction is computed from the version field embedded in capacity snapshots received at epoch boundaries

This creates a Schelling-point coordination game: agents switch when they believe enough peers have switched. The migration threshold ensures that a supermajority is on the new version before any individual agent commits.

**Early adopter incentive:** Agents that switch early (within the first 25% of the overlap period) and the migration succeeds receive a small bonus in the first settlement under the new version. This accelerates convergence to the Schelling point.

### 9.4 Rollback

If migration does not reach migration_threshold within overlap_duration epochs:

1. The overlap version is discarded (state: never reaches ACTIVE).
2. All agents that switched to the new version revert to the previous ACTIVE version.
3. Reversion is deterministic: at epoch activation_epoch + overlap_duration, the overlap version ceases to exist. Agents must be on the previous ACTIVE version by this epoch.
4. Work performed under the new version during the overlap is settled using the economic parameters of the new version (the work was valid under the version it was performed against).
5. Governance is notified of the migration failure for analysis.

### 9.5 Version Data Structure

```
TidalVersion {
    version_id:           uint64        // monotonically increasing identifier
    hash_ring_config: {
        virtual_nodes_per_agent: uint32 // number of virtual nodes per agent
        hash_function:           string // hash algorithm identifier (e.g., "SHA-256-TRUNC-64")
        ring_count:              uint32 // number of hash rings (one per task type)
    }
    vrf_seeds: {
        current_seed:        bytes32    // active VRF seed
        rotation_interval:   uint64     // epochs between seed rotations
        seed_commitment:     bytes32    // commitment to next seed (anti-grinding)
    }
    epoch_length:            uint64     // epoch duration in milliseconds
    task_type_bands: [                  // frequency bands for task types
        {
            task_type:       string     // AASL claim type identifier
            frequency_band:  string     // HIGH | MEDIUM | LOW | BATCH
            priority:        uint32     // scheduling priority within band
        }
    ]
    activation_epoch:        uint64     // epoch at which OVERLAP begins
    deactivation_epoch:      uint64     // epoch at which DEPRECATED (set when superseded)
    economic_parameters: {
        base_reward_rate:       float64 // R_base
        surprise_cost_rate:     float64 // R_surprise
        prediction_bonus_rate:  float64 // R_prediction
        verification_fee_rate:  float64 // R_verify
        settlement_frequency:   uint32  // settle every N epochs
        grace_period:           uint32  // epochs to wait for late events
    }
    migration_parameters: {
        overlap_duration:       uint32  // epochs
        migration_threshold:    float64 // fraction of peers required
        early_adopter_window:   uint32  // epochs (first N of overlap for bonus)
        early_adopter_bonus:    float64 // AIC bonus amount
    }
}
```

The version is immutable once published: no field may be modified after the PUBLISHED state transition. New parameters require a new version.

---

## 10. Conformance and Verification

### 10.1 Determinism Conformance

The foundational property of PTA is determinism: two independent implementations given identical inputs must produce identical outputs for all Layer 1 computations and all settlement computations.

**Determinism test:**

Given a reference input set R = (agent_roster, task_types, epoch_sequence, event_log, tidal_version), two implementations A and B must satisfy:

```
∀ inputs ∈ R:
    schedule_A(inputs) == schedule_B(inputs)
    verifier_set_A(inputs) == verifier_set_B(inputs)
    settlement_A(inputs) == settlement_B(inputs)
```

Equality is bitwise for integer outputs and within ε = 10⁻¹² for floating-point outputs (to accommodate IEEE 754 rounding differences across platforms).

**Reference input generation:**

The conformance test suite includes a deterministic reference input generator that produces:
- 10 agent rosters of varying sizes (10, 100, 1000 agents)
- 5 tidal version configurations with varying parameters
- 20-epoch event logs with known surprise events, verification results, and churn events
- Expected outputs for each input set, generated by the reference implementation

### 10.2 Layer 1 Conformance — MINIMUM REQUIRED

Layer 1 conformance is the minimum requirement for PTA compliance. An implementation is Layer 1 conformant if and only if it passes all of the following:

| Test Category | Tests | Requirement |
|---|---|---|
| Hash ring determinism | Given (agent_roster, task_type, epoch, version), the computed assignment matches the reference output | 100% match |
| VRF correctness | Given (claim_hash, epoch, seed), the computed verifier set matches the reference output; VRF proof verifies | 100% match |
| Epoch clock correctness | Epoch boundaries are detected at the correct wall-clock times within NTP tolerance | Within ±tolerance |
| Settlement determinism | Given (schedule, event_log, parameters), the computed settlement matches the reference output | 100% match (within ε for floats) |
| Substitution correctness | Given an agent failure, the substitution agent matches the hash ring successor | 100% match |
| Version migration | Given a migration scenario, the agent switches or rolls back at the correct epoch | 100% match |
| Capacity snapshot protocol | Snapshots are compiled, propagated, and aggregated correctly per the gossip protocol | Functional test pass |

### 10.3 Layer 2 Conformance — OPTIONAL ENHANCEMENT

Layer 2 conformance is optional. An implementation may omit Layer 2 entirely and remain PTA-compliant (operating in standard messaging mode).

If Layer 2 is implemented, conformance requires:

| Test Category | Tests | Requirement |
|---|---|---|
| RLS model correctness | Given an observation sequence, the model parameters after N updates match the reference output | Within ε for floats |
| Threshold adaptation | Given an error sequence, the threshold trajectory matches the reference output | Within ε |
| Surprise signal format | Generated surprise signals match the specified message format | Structural match |
| Propagation radius | Given a magnitude and θ_base, the computed radius matches floor(log₂(magnitude/θ_base)) | 100% match |
| Damping | Signal magnitude at hop *h* matches magnitude × δ^h | Within ε |
| Cold-start protocol | Transition from STANDARD to PREDICTIVE occurs at the correct epoch given the accuracy trajectory | 100% match |
| Deduplication | Duplicate (source_id, epoch) signals are processed at most once | Functional test pass |
| Signal budget | No more than B_max signals originated per agent per epoch | Hard limit verified |

### 10.4 Layer 3 Conformance — OPTIONAL ENHANCEMENT (PENDING DECISION GATE)

Layer 3 conformance is optional and pending the Phase 2 decision gate. An implementation may omit Layer 3 entirely.

If Layer 3 is implemented, conformance requires:

| Test Category | Tests | Requirement |
|---|---|---|
| Potential function evaluation | Given (cluster_state, demand_vector, parameters), Φ(s) matches the reference output | Within ε |
| Gradient computation | Given (cluster_state, AASL dimensions), the gradient vector matches the reference output | Within ε |
| Simplex projection | Given an unconstrained vector, the simplex projection matches the reference output | Within ε |
| Strategy update | Given (strategy, gradient, step_size), the updated strategy matches the reference output | Within ε |
| Tidal perturbation determinism | Given (epoch, agent_id, stability_count), the perturbation vector matches the reference output | 100% match (deterministic PRNG) |
| Cluster formation | Given (agent_roster, capabilities), the cluster assignment matches the reference output | 100% match |
| Cluster dissolution | Dissolution triggered correctly when 2+ members fail | Functional test pass |
| Convergence detection | Nash equilibrium correctly detected when gradient magnitudes fall below convergence threshold | Functional test pass |

### 10.5 Test Suite Outline

#### 10.5.1 Unit Tests (per algorithm)

| Component | Unit Tests |
|---|---|
| Consistent hash ring | Ring construction, lookup, virtual node mapping, add/remove agent, key redistribution fraction |
| VRF computation | Evaluate, prove, verify, seed rotation, determinism across calls |
| RLS model (Layer 2) | Initialization, single update, convergence on synthetic data, forgetting factor effect |
| Threshold adaptation (Layer 2) | Tightening, loosening, floor/ceiling enforcement, hysteresis guard, non-stationarity detection |
| Surprise signal (Layer 2) | Magnitude computation, radius calculation, damping, deduplication, budget enforcement |
| Potential function (Layer 3) | Evaluation at known states, gradient correctness via finite differences, simplex projection |
| Settlement calculator | Each stream independently (compliance, surprise cost, prediction bonus, verification reward), net computation, proof generation |
| Version manager | State transitions, overlap dual evaluation, migration threshold check, rollback trigger |

#### 10.5.2 Integration Tests (per data flow)

| Data Flow | Integration Test |
|---|---|
| Epoch boundary processing | Full boundary sequence (snapshot → settlement → recalibration → hash ring update → version check → schedule) produces correct outputs |
| Surprise propagation | Surprise generated at agent A propagates correctly through B and C with proper damping, dedup, and budget |
| Cold-start to predictive transition | Agent begins in STANDARD mode, model trains, transitions to PREDICTIVE at correct epoch |
| Cluster gradient convergence | 4-agent cluster converges to Nash equilibrium within expected iteration count |
| Version migration end-to-end | New version published → overlap → sufficient agents switch → migration succeeds → old version deprecated |
| Version rollback end-to-end | New version published → overlap → insufficient agents switch → rollback → all agents on previous version |
| Settlement with all streams | Epoch with compliance events, surprises, prediction data, and verification results produces correct net settlement |

#### 10.5.3 End-to-End Determinism Tests

| Test | Description |
|---|---|
| Two-implementation agreement | Run the reference implementation and the implementation-under-test with identical inputs for 100 epochs; verify bitwise-identical outputs at every epoch boundary |
| Replay determinism | Record all inputs for a 100-epoch run; replay the inputs and verify identical outputs |
| Cross-platform determinism | Run the same implementation on two platforms (e.g., Linux x86_64 and Linux aarch64); verify outputs match within floating-point ε |
| Churn determinism | Inject identical churn sequences into two instances; verify identical schedule and settlement outputs after convergence |
| Adversarial determinism | Inject identical adversarial behavior into two instances; verify identical surprise signals, settlement costs, and anomaly signals |

---

*End of Technical Specification Part 2.*

*Part 1 covers: System overview, primitives, Layer 1 (Tidal Backbone) protocol specification, core data structures, and the Tidal Function family definition.*
