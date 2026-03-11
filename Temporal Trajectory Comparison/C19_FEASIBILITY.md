# C19 — Temporal Trajectory Comparison — FEASIBILITY

**Invention ID:** C19
**Stage:** FEASIBILITY
**Date:** 2026-03-11
**Selected Concept:** C19-C+ (Hybrid DTW-DVC with Per-Modality Drift Decomposition)

---

# PART 1 — DOMAIN TRANSLATOR (Sub-Problem Analogies)

## Sub-Problem: Population-Mean De-Trending

**Problem:** All agents may drift in the same direction due to environmental changes (SEB task pool refresh, system updates, seasonal patterns). How do you isolate idiosyncratic drift from systematic drift without removing the signal you need?

**Analogy: Tide-Corrected Sea Level Measurement**
Oceanographers measuring long-term sea level rise must remove tidal oscillations (predictable, affecting all measurement stations equally) to detect genuine sea level trends. They use harmonic analysis to model and subtract tidal components, leaving the residual trend. Over-correction removes real signal; under-correction leaves confounding noise. The standard approach: subtract the *mean across stations* at each time point, then analyze inter-station differences.

**Application:** C19 should subtract the population-mean behavioral drift at each monthly window. This removes first-order systematic effects (equivalent to tidal removal). The residual per-agent drift is the idiosyncratic component that carries the same-origin signal. Over-correction risk: if the population is dominated by same-origin clusters, the population mean itself is biased. Mitigation: use a *trimmed mean* (remove top/bottom 10% of drift magnitudes before averaging) to resist cluster dominance.

---

## Sub-Problem: Minimum Observation Window

**Problem:** How many monthly trajectory points are needed before trajectory comparison produces reliable results? Too few = noisy comparisons, high false positive rate. Too many = long activation delay, reducing detection window.

**Analogy: Satellite Orbit Determination**
To determine a satellite's orbit, astronomers need multiple position observations over time. Three observations define the orbit uniquely (via Gauss's method), but noise requires more. In practice, 6+ observations spanning at least half the orbital period provide reliable orbit parameters. Fewer observations yield ambiguous or unstable solutions.

**Application:** Behavioral trajectories are analogous to orbits — structured paths through feature space. The RESEARCH stage's statistical power analysis showed that 6 monthly windows provide adequate power for both drift direction (cosine) and trajectory shape (DTW) comparison. C19 should require 6 monthly windows spanning 6 distinct months. This is stricter than C17's placeholder (4 windows over 6 months) but backed by the power analysis.

---

# PART 2 — COMMERCIAL VIABILITY ASSESSMENT (Early)

## Adoption Barriers

| Barrier | Severity | Mitigation |
|---------|----------|-----------|
| 6-month activation delay | LOW | Trajectory modality is supplementary; 5-modality B operates from day 1. 6-month delay is inherent to the problem (need history to compare history). |
| Compute overhead | NEGLIGIBLE | <1% addition to C17 compute budget (RESEARCH §3.2). No new infrastructure required. |
| Monthly snapshot storage | LOW | ~50 dims per modality per month per agent. At 100K agents: ~300 MB/year. Trivial. |
| Population-mean computation | LOW | One aggregation pass per month across all agents. O(n) per modality. |
| Complexity perception | MEDIUM | The hybrid DTW-DVC architecture is more complex than the C17 placeholder. Mitigated by per-modality decomposition (preserves interpretability) and the trajectory explanation format. |

## Value Proposition

The trajectory modality addresses a specific, identified attack (C17 FEASIBILITY Attack 4: Gradual Behavioral Drift) that the 5 core modalities cannot detect. Its value is defensive: it closes a gap, not opens a market. The investment is minimal (compute is negligible, storage is trivial, specification effort is the main cost) and the return is an incremental improvement in Sybil detection for long-lived agents.

---

# PART 3 — ADVERSARIAL ANALYST REPORT

## 10 Attacks on C19-C+

### Attack 1: Synchronized Update Avoidance

**Attack:** Adversary staggers Sybil agent updates by different amounts — Agent A updated in January, Agent B in April, Agent C in July — so that temporal trajectory alignment is poor. DTW warping band (2 months) is insufficient to align trajectories offset by 3+ months.

**Impact:** DTW shape comparison degrades. Drift direction comparison survives if the updates use the same training data (drift direction is the same regardless of timing).

**Defense:** The hybrid design's drift direction component (cosine on displacement vectors) is robust to arbitrary temporal offsets because it compares *cumulative* displacement direction, not per-month alignment. DTW provides supplementary shape signal but is not the sole mechanism. Also: extend the DTW band width dynamically for pairs with high drift direction similarity but low DTW similarity — this suggests misalignment, not independence.

**Verdict:** LOW — the hybrid design specifically addresses this by combining alignment-sensitive (DTW) and alignment-insensitive (direction) measures.

---

### Attack 2: Decorrelated Update Strategy

**Attack:** Adversary updates Sybil agents using *different* training data / RLHF data for each agent. Agents A, B, and C are fine-tuned on disjoint datasets, causing them to drift in different directions despite sharing a base model.

**Impact:** Drift direction cosine similarity drops to near-zero. DTW shape similarity also drops. The trajectory modality produces low similarity (CLEAR), even though agents share origin.

**Defense:** This is the **intended economic deterrent**. Creating genuinely different fine-tuning pipelines for each Sybil agent multiplies the adversary's cost. The cost of maintaining separate training data pipelines is comparable to maintaining separate model architectures (the 4.0x multiplier from C17). Moreover, the 5 core modalities still detect same-origin at the base model level — agents fine-tuned differently from the same base still share base-model temporal, structural, and error signatures.

**Verdict:** LOW — this is the design working as intended. The adversary pays the cost multiplier.

---

### Attack 3: Noise Injection Into Drift

**Attack:** Adversary adds random behavioral noise at each update to obscure the drift direction. Each agent's drift is the real drift + random perturbation, making drift vectors noisy and reducing cosine similarity between same-origin pairs.

**Impact:** Drift direction similarity decreases. At sufficient noise levels, same-origin drift becomes indistinguishable from independent drift.

**Defense:**
1. **Multi-modality noise budget.** To obscure drift in all 5 modalities simultaneously, the adversary must inject substantial noise. This degrades agent performance (C5 PCVM quality monitoring detects performance degradation).
2. **Multi-month averaging.** Drift direction is computed as cumulative displacement over 6+ months. Random per-month noise averages out over the trajectory. The adversary must inject *consistent directional noise* (i.e., a fake drift direction) — which is detectable as an anomalous drift pattern.
3. **Magnitude-direction decomposition.** Compare drift *magnitude* as well as direction. Same-origin agents under noise injection show higher drift magnitude (real drift + noise) than independent agents (only real drift). Anomalously high drift magnitude triggers enhanced monitoring.

**Verdict:** MEDIUM — partially effective but noise injection adds cost and is partially defeated by multi-month averaging. Residual risk: sophisticated adversary can engineer consistent, modality-specific fake drift at significant cost.

---

### Attack 4: Mimicking Population-Mean Drift

**Attack:** Adversary ensures each Sybil agent's drift closely follows the population-mean drift vector, so that after de-trending, the idiosyncratic drift is near-zero. With zero idiosyncratic drift, there is nothing to compare.

**Impact:** Both drift direction and DTW shape comparisons yield low signal. Agents appear to drift only with the population — no idiosyncratic pattern to correlate.

**Defense:**
1. **Zero-drift is suspicious.** Agents with near-zero idiosyncratic drift over 6+ months are statistically unlikely (all agents drift idiosyncratically as their task portfolios diversify). Near-zero idiosyncratic drift should trigger a WATCH flag for drift suppression.
2. **Timing precision.** To track the population mean precisely, the adversary must observe it in near-real-time. Population-mean drift is published only quarterly (C17 Section 8.3 — quarterly anonymized statistics). The adversary must estimate monthly population drift from incomplete information.
3. **Multi-task deconfounding.** Population-mean drift varies by SEB task category. Matching the population mean across all 7 categories simultaneously is harder than matching one aggregate mean.

**Verdict:** MEDIUM — feasible in principle but requires real-time population drift intelligence that is not available to agents (information asymmetry). Near-zero drift is itself a detectable anomaly.

---

### Attack 5: Trajectory Replay (Historical Mimicry)

**Attack:** Adversary observes a legitimate independent agent's publicly known behavioral trajectory (from quarterly anonymized statistics) and engineers Sybil agents to follow similar trajectories, making them appear independently drifting.

**Impact:** Sybil agents' trajectories correlate with a legitimate agent's trajectory rather than with each other. Cross-comparison shows low Sybil-to-Sybil correlation.

**Defense:**
1. **Anonymized statistics are insufficient.** C17's quarterly statistics are aggregate, not per-agent trajectories. The adversary cannot observe individual agent trajectories (information asymmetry, C17 Section 14.4).
2. **Engineering a specific trajectory is expensive.** Even if the adversary could observe a target trajectory, steering an agent's behavioral drift to match it requires precise per-update calibration of training data — essentially solving a control problem in high-dimensional behavioral space.
3. **Sybil-to-Sybil comparison still operates.** Even if each Sybil mimics a different legitimate agent, the Sybil agents' trajectories must be *uncorrelated* — which requires genuinely different drift drivers (different training data). This is the cost multiplier again.

**Verdict:** LOW — information asymmetry and high engineering cost make trajectory replay impractical.

---

### Attack 6: Model Architecture Switch Mid-Trajectory

**Attack:** Adversary switches an agent's underlying model architecture (e.g., GPT-4 to Llama-3) mid-trajectory, creating a discontinuity that breaks trajectory comparison. The pre-switch and post-switch trajectories are from different architectures and cannot be meaningfully compared.

**Impact:** DTW on the full trajectory produces a high distance due to the discontinuity. Drift direction comparison is disrupted.

**Defense:**
1. **Discontinuity detection.** A sudden, large behavioral shift between consecutive monthly windows (beyond 3 standard deviations of normal drift magnitude) triggers a trajectory reset. The agent's trajectory history restarts from the post-switch baseline.
2. **Post-reset reduced weight.** After a trajectory reset, the agent has insufficient history for trajectory comparison. The standard 5-modality weights apply until 6 new monthly windows accumulate. During this period, the point-in-time B comparison still operates.
3. **Frequent resets are suspicious.** An agent that resets trajectory more than once per year triggers enhanced monitoring. Legitimate model upgrades are infrequent; adversarial resets to evade trajectory comparison are frequent.
4. **Note:** C17 OQ-05 already identified this as an open question ("How should B handle agents that undergo major model upgrades?"). C19's discontinuity detection and trajectory reset protocol provides the answer.

**Verdict:** LOW — discontinuity detection with reset is a clean solution. Frequent resets are detectable and penalized.

---

### Attack 7: Slow Decorrelation (Boiling Frog)

**Attack:** Adversary starts with correlated updates (same training data for all Sybils) then gradually introduces divergence — small amounts of unique training data mixed in over time. The drift trajectories slowly decorrelate over months.

**Impact:** Initial trajectory comparison detects correlation. Over time, correlation fades. Eventually, the pair drops from WATCH to CLEAR.

**Defense:**
1. **Cumulative evidence.** Trajectory comparison retains the full 12-month rolling window. Early high-correlation windows continue contributing to the trajectory distance even as later windows decorrelate. The exponential decay weighting from C17 (half_life = 90 days) means early evidence fades — but 90 days of high correlation produces a strong WATCH/FLAG signal that triggers enhanced monitoring.
2. **WATCH persistence.** Once a pair enters WATCH, enhanced monitoring continues for 6 months (C17 Section 10.3). The adversary must sustain decorrelation for 6+ months under enhanced observation frequency.
3. **Historical record.** Even if the pair eventually drops to CLEAR, the historical WATCH record remains. A future correlation spike re-triggers WATCH with elevated suspicion.

**Verdict:** MEDIUM — boiling-frog decorrelation is a viable strategy but requires 6+ months of sustained, expensive divergent updates under enhanced monitoring. The cost is significant.

---

### Attack 8: Spurious Correlation Exploitation (False Positives)

**Attack:** Not an evasion attack but a disruption attack. Adversary identifies two legitimate independent agents that happen to have correlated trajectories (e.g., both run on the same model family, updated at similar times by different creators) and publicizes the correlation to undermine trust in the system.

**Impact:** False positive. Two legitimate agents are incorrectly flagged, creating political pressure to weaken the trajectory modality.

**Defense:**
1. **Population-mean de-trending.** The most likely source of spurious correlation (agents on the same model family drifting together after a provider update) is exactly what population-mean de-trending removes. If GPT-5 is released and all GPT agents drift similarly, the systematic drift is subtracted.
2. **Multi-task consistency gating (rho_Traj).** Spurious correlation from model-family effects should be inconsistent across SEB task categories. Genuine same-origin correlation is consistent across tasks.
3. **Weight moderation.** Trajectory weight is 0.14 (not dominant). Even a perfect false positive on trajectory alone cannot produce B >= theta_B without corroboration from the 5 core modalities.
4. **Known-independent whitelist.** C17's whitelist mechanism (Section 10.3) applies — confirmed false positives are whitelisted.

**Verdict:** LOW — multiple deconfounding mechanisms reduce false positive risk. Trajectory modality's moderate weight prevents trajectory-only false flags.

---

### Attack 9: Drift Direction Spoofing via Opposite Updates

**Attack:** Adversary updates Sybil agents in *opposite* directions — Agent A is fine-tuned toward more verbose responses while Agent B is fine-tuned toward more concise responses. Drift directions are anti-correlated (negative cosine similarity), which the system interprets as independent.

**Impact:** Drift direction cosine similarity is negative (anti-correlated). Standard interpretation: independent agents. The trajectory modality misses these Sybils.

**Defense:**
1. **Use absolute cosine similarity.** Anti-correlated drift (cosine ~ -1.0) is as suspicious as positively correlated drift (cosine ~ +1.0). Independent agents have cosine ~ 0. Change the distance function: d_direction = 1 - |cosine_similarity(drift_i, drift_j)|. This treats both correlated and anti-correlated drift as indicators of shared origin.
2. **Rationale:** Truly independent agents should have uncorrelated drift (cosine ~ 0 with noise). Any strong correlation — positive OR negative — suggests a shared cause. Anti-correlated drift is actually more suspicious than uncorrelated drift, because it suggests deliberate opposition (a coordinating force).

**Verdict:** LOW — using absolute cosine similarity is a simple, principled fix that turns this attack into a detection signal.

---

### Attack 10: Trajectory Length Inequality Exploitation

**Attack:** Adversary registers Sybil agents at different times (Agent A at month 0, Agent B at month 6, Agent C at month 12). When comparing A-B at month 12, Agent A has 12 months of history but Agent B has only 6 months. The comparison uses only the overlapping 6-month window, reducing statistical power.

**Impact:** Reduced comparison window means higher variance in trajectory distance estimates. False negative rate increases.

**Defense:**
1. **Overlap-window comparison.** DTW and drift direction are computed only over the overlapping time window when both agents have observations. This is correct behavior — the comparison is valid but lower-power.
2. **Minimum overlap requirement.** Trajectory comparison activates only when the overlapping window contains >= 6 monthly snapshots. If overlap is shorter, trajectory modality is disabled for that pair and standard 5-modality weights apply.
3. **Staggered registration as signal.** If multiple agents from the same origin stagger registration to minimize overlapping trajectory windows, this pattern itself is detectable by AiSIA (registration timing anomaly monitoring). Layer 3 social graph analysis can flag coordinated staggered registration.

**Verdict:** LOW — minimum overlap requirement ensures adequate power. Staggered registration is a Layer 3/4 detection target.

---

### Adversarial Analyst Verdict

**ADVANCE.** 10 attacks tested; 0 fatal, 0 HIGH, 3 MEDIUM, 7 LOW. The trajectory modality is defensible because:
- The hybrid DTW + drift direction design provides complementary signals (shape and direction)
- Population-mean de-trending removes the primary false positive source (model-family systematic drift)
- Information asymmetry (agents cannot see individual trajectories or population drift in real-time) prevents calibration attacks
- The trajectory modality's moderate weight (0.14) ensures it supplements but does not dominate the 5 core modalities
- Multiple attacks (2, 5, 10) reduce to the existing 4.0x cost multiplier — the design reinforces rather than undermines C17's economic deterrent

---

# PART 4 — FEASIBILITY VERDICT

```json
{
  "type": "ASSESSMENT_COUNCIL_VERDICT",
  "invention_id": "C19",
  "stage": "FEASIBILITY",
  "decision": "ADVANCE",
  "novelty_score": 3.0,
  "feasibility_score": 4.5,
  "impact_score": 3.5,
  "risk_score": 3,
  "risk_level": "LOW-MEDIUM",
  "required_actions": [
    "DA-01: Per-modality monthly snapshot extraction specification — what features are aggregated, how",
    "DA-02: Population-mean drift computation and subtraction — trimmed mean specification, computation cadence",
    "DA-03: DTW configuration — Sakoe-Chiba band width, step pattern, per-modality point distance function, normalization to [0,1]",
    "DA-04: Drift direction vector specification — cumulative vs. per-month, absolute cosine similarity",
    "DA-05: Direction-shape fusion formula — alpha = 0.6/0.4 validation, per-modality aggregation",
    "DA-06: Multi-task trajectory consistency (rho_Traj) specification",
    "DA-07: Updated 6-modality weight allocation with governance constraints",
    "DA-08: Discontinuity detection and trajectory reset protocol",
    "DA-09: Trajectory explanation format for WATCH/FLAG reports",
    "DA-10: Integration specification — how C19 modifies C17 MTS Section 11"
  ],
  "monitoring_flags": [
    "MF-1: Empirical false positive rate of trajectory modality in isolation (Phase 2 shadow period)",
    "MF-2: Population-mean drift magnitude — if systematically large, de-trending removes too much signal",
    "MF-3: DTW band width (2 months) adequacy — may need widening if staggered updates are common"
  ],
  "pivot_direction": null,
  "rationale": "C19-C+ is technically sound, computationally negligible, and addresses a specific identified gap in C17 (Attack 4: Gradual Behavioral Drift). The hybrid DTW-DVC architecture with per-modality decomposition is well-grounded in established techniques. Risk is LOW-MEDIUM (3/10) — lower than C17 itself because C19 is an incremental extension. 10 adversarial attacks produced 0 fatal, 0 HIGH, 3 MEDIUM, 7 LOW. ADVANCE to DESIGN."
}
```

---

**End of FEASIBILITY Stage**

**Status:** FEASIBILITY COMPLETE — ADVANCE with 10 design actions
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Temporal Trajectory Comparison\C19_FEASIBILITY.md`
