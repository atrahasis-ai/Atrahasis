# C19 — Temporal Trajectory Comparison — IDEATION

**Invention ID:** C19
**Stage:** IDEATION
**Date:** 2026-03-11
**Subject:** 6th behavioral modality for C17 B(a_i, a_j) — detecting correlated behavioral drift over time via temporal trajectory comparison
**Source:** C17 Assessment MF-5 ("Temporal trajectory comparison (6th modality) should be evaluated for Phase 2 inclusion"), C17 Section 11 (placeholder specification), C17 Feasibility Attack 4 (Gradual Behavioral Drift)

---

# PART 1 — PRE-IDEATION QUICK SCAN

## 1.1 Problem Statement

C17 defines B(a_i, a_j) using 5 behavioral modalities that compare agents at a *point in time*. Section 11 adds a placeholder for a 6th modality — temporal trajectory comparison — activated at Phase 2 for agents with >= 6 months history. The placeholder specifies:

- Monthly BFE snapshots as trajectory points
- DTW (Dynamic Time Warping) for trajectory distance
- Weight w_Traj = 0.14 drawn proportionally from other modalities

However, the placeholder lacks:
- **Feature extraction specification.** What exactly constitutes a "trajectory point"? Raw BFE vectors (853 dims) are too noisy for DTW.
- **DTW configuration.** Warping window, step patterns, normalization, distance function within DTW.
- **Drift detection vs. trajectory matching.** DTW finds similar *shapes* but the insight is about correlated *drift direction*. These are different problems.
- **Adversarial analysis.** How hard is it to fake independent drift trajectories?
- **Minimum observation requirements.** Is 6 months / 4 windows enough for statistical significance?

C19 fills these gaps with a complete specification of the temporal trajectory modality.

## 1.2 Quick Domain Scan

### Temporal Analysis in Behavioral Biometrics
- **Keystroke dynamics aging:** Users' typing patterns drift over time due to practice, fatigue, or hardware changes. Continuous authentication systems track these changes using sliding windows. Key finding: drift is *structured* — it follows predictable trajectories influenced by the user's underlying motor control, not random noise. Systems that model drift trajectories achieve 15-25% lower EER than static templates.
- **Gait recognition over time:** Human gait changes with age, injury, footwear. Longitudinal gait analysis shows that drift patterns cluster by individual — people whose gait changes in similar ways over time are more likely to share physical characteristics (age, body type, injury history).

### Drift Detection in Machine Learning
- **Concept drift detection:** Methods like ADWIN, DDM, and KSWIN detect when a model's performance distribution shifts. These detect *that* drift occurred, not *how* it compares across models.
- **Model update fingerprinting:** When a model is fine-tuned, its outputs change systematically. Recent work (Mitchell et al., 2023) shows that the *direction* of change in embedding space is characteristic of the fine-tuning data — models fine-tuned on similar data drift in similar directions regardless of starting point.
- **Federated learning divergence:** In federated learning, tracking how client models diverge from the global model reveals which clients share data distributions. Analogous to tracking how agents diverge from their initial behavioral profile.

### DTW Applications
- **Speech recognition:** DTW's original application. Aligns speech signals that vary in speed. Well-understood: O(n*m) complexity with Sakoe-Chiba band optimization.
- **Financial time series:** DTW compares stock price trajectories, identifying stocks that move similarly even with timing offsets. Relevant: stocks influenced by the same fundamentals drift in similar directions.
- **Medical time series:** DTW on physiological signals (EEG, ECG) identifies patients with similar condition progression. Key insight: trajectory shape similarity is more diagnostic than point-in-time similarity.
- **DTW alternatives:** Soft-DTW (differentiable relaxation), shape-based distance (SBD), time series kernels (SINK, GAK), and Frechet distance. Each has trade-offs in sensitivity, computational cost, and differentiability.

### Model Update Fingerprinting (Most Directly Relevant)
- **Training data attribution:** Methods like influence functions and data Shapley estimate which training examples most affected model outputs. When two models are updated on similar data, their behavioral shifts correlate.
- **Checkpoint comparison:** Comparing model checkpoints before and after updates reveals structured differences. Key: the *difference vector* between checkpoints is often more informative than the checkpoints themselves.
- **RLHF drift patterns:** Models fine-tuned with RLHF from the same human feedback data develop correlated behavioral shifts — similar changes in verbosity, hedging, topic avoidance. These patterns persist even when the base models differ.

---

# PART 2 — DOMAIN TRANSLATOR (5 Cross-Domain Analogies)

### Analogy 1: Plate Tectonics and Continental Drift

**Domain:** Geologists track how continental plates move over millions of years. Plates that were once joined (Pangaea) drift apart, but their drift trajectories remain correlated because they share the same mantle convection currents. By comparing the direction and rate of plate movement, geologists can reconstruct which plates were once connected — even billions of years after separation.

**Structural Parallels:**
- AI agents from the same creator are like fragments of the same continental plate — initially similar, then drifting
- The "mantle convection" is the creator's update philosophy (same training data, same RLHF preferences, same fine-tuning objectives)
- Correlated drift direction reveals shared underlying forces, not just shared starting position

**Insights for C19:**
- **Direction of drift matters more than magnitude.** Two plates may drift at different speeds (different update frequencies) but in the same direction (same training data). C19 should compare drift *direction vectors*, not just trajectory shape.
- **Phase correlation is detectable even with time offsets.** Plates respond to the same mantle event at slightly different times. DTW handles this — aligning trajectories that respond to the same cause at different times.

---

### Analogy 2: Epidemiological Contact Tracing via Symptom Evolution

**Domain:** In epidemiology, when multiple patients develop the same disease, their symptom progressions follow correlated trajectories — not identical (individual variation), but structurally similar (same pathogen, same disease mechanism). Contact tracers use symptom trajectory correlation to identify common-source outbreaks vs. independent infections, even when the initial infection point is unknown.

**Structural Parallels:**
- "Symptom trajectory" = behavioral feature trajectory over time
- "Common pathogen" = common creator/training pipeline
- Independent infections produce uncorrelated symptom trajectories; common-source infections produce correlated ones
- The correlation is in the *progression pattern*, not the initial presentation

**Insights for C19:**
- **Trajectory correlation survives individual variation.** Even though each patient's symptoms vary, the underlying trajectory shape is diagnostic. Similarly, two agents from the same creator may have different absolute behavioral profiles but correlated drift trajectories.
- **Incubation period analogy.** There is a delay between infection (update) and symptom change (behavioral shift). C19 must handle temporal lag between creator's update and observable behavioral change.

---

### Analogy 3: Stellar Proper Motion in Astrometry

**Domain:** Stars in a galaxy move through space. Stars born in the same molecular cloud (stellar siblings) share a common motion vector even after dispersing across the galaxy. Astrometrists compare proper motion vectors (direction and rate of movement across the sky) to identify co-natal stellar groups. The ESA's Gaia mission uses proper motion correlation to identify stellar associations separated by hundreds of light-years.

**Structural Parallels:**
- "Proper motion" = behavioral drift direction and rate
- "Co-natal origin" = same creator
- Stars can be widely separated in current position (different behavioral profiles) but share motion vectors (correlated drift)
- Background stars (independent agents) have uncorrelated proper motions

**Insights for C19:**
- **Motion vector comparison is independent of current position.** Two agents can have very different behavioral profiles (different "positions") but correlated drift vectors. This is exactly what C19 needs — it detects correlated CHANGE, not correlated STATE.
- **Statistical significance requires sufficient baseline.** Gaia needs multiple observations over time to distinguish proper motion from measurement noise. C19 needs sufficient trajectory length (observation windows) to distinguish real correlated drift from noise.

---

### Analogy 4: Financial Portfolio Covariance (Factor Models)

**Domain:** In finance, portfolio returns are decomposed into systematic factors (market, value, momentum) and idiosyncratic noise. Two portfolios managed by the same fund manager tend to have correlated factor exposures over time — not because they hold the same stocks, but because the manager's investment philosophy applies consistent biases. Factor covariance analysis reveals common management even when portfolios appear diversified.

**Structural Parallels:**
- "Factor exposures" = behavioral modality feature values
- "Fund manager's philosophy" = creator's update/training approach
- "Systematic factors" = environmental changes that affect all agents (e.g., new task types, system updates)
- "Idiosyncratic noise" = agent-specific behavioral variation

**Insights for C19:**
- **Factor out systematic drift.** All agents may drift in the same direction due to environmental changes (new SEB tasks, system-wide updates). C19 must distinguish *systematic* drift (everyone changes) from *correlated idiosyncratic* drift (only same-origin agents change together). Factor analysis or de-trending against population mean drift is essential.
- **Covariance over time is more informative than correlation at a point.** The evolution of covariance between two agents' behavioral features over time is a richer signal than any single comparison.

---

### Analogy 5: Forensic Document Aging (Ink Chemistry Degradation)

**Domain:** Forensic document examiners date documents by analyzing how ink chemistry changes over time — volatile compounds evaporate at predictable rates. Two documents created with the same ink batch show correlated aging trajectories (same compounds, same degradation rates). Documents from different ink batches age differently. Crucially, the *rate* and *pattern* of aging reveals batch identity even when the documents are different ages.

**Structural Parallels:**
- "Ink chemistry" = model weights / training data
- "Aging trajectory" = behavioral drift over time
- Same-batch documents age the same way = same-origin agents drift the same way
- The aging *pattern* is a fingerprint even if absolute age differs

**Insights for C19:**
- **Drift rate as a fingerprint.** Not just drift direction but drift *rate* reveals origin. Agents from the same creator, updated on the same schedule, change at similar rates.
- **Environmental deconfounding.** Ink ages differently in different storage conditions (humidity, light). Similarly, agents may drift differently based on their task environment. C19 must control for task-environment effects on drift — comparing drift on controlled SEB tasks, not just organic tasks.

---

# PART 3 — IDEATION COUNCIL (3-Round Debate)

## Concept Generation

### Concept C19-A: Direct DTW on BFE Trajectory Vectors
**Description:** The straightforward approach. Monthly BFE snapshots are aggregated into trajectory vectors (reduced from 853 to ~50 dims via PCA). DTW aligns the two agents' trajectories and computes warping distance. Low DTW distance = similar trajectories = likely same origin.

**Strengths:**
- Directly implements C17 Section 11 placeholder
- DTW is well-understood, mature algorithm
- Handles temporal misalignment (agents updated at different times)

**Weaknesses:**
- DTW on raw BFE vectors may be dominated by noise
- Does not distinguish systematic drift from correlated idiosyncratic drift
- O(n*m) per pair — potentially expensive at scale
- DTW measures shape similarity, but the insight is about correlated drift *direction* — not the same thing

---

### Concept C19-B: Drift Vector Correlation (DVC)
**Description:** Instead of comparing trajectories directly, compute *drift vectors* — the change between consecutive monthly snapshots. Then compare drift vector sequences between agents using cosine similarity. Two agents whose drift vectors point in the same direction over time are likely same-origin.

**Architecture:**
1. For each agent, compute monthly BFE delta: delta_t = BFE(t) - BFE(t-1)
2. Reduce delta to a drift vector via PCA or per-modality summarization
3. For each pair, compute cosine similarity between corresponding drift vectors
4. Aggregate drift vector similarities over time using a weighted mean (recency-weighted)
5. Factor out population-mean drift to isolate idiosyncratic correlation

**Strengths:**
- Directly targets the core insight: correlated drift direction
- Simpler than DTW — linear time per pair
- Population-mean de-trending removes systematic drift
- Drift vectors are lower-dimensional than raw trajectories (change is often structured)

**Weaknesses:**
- Requires strict temporal alignment (no handling of update timing differences)
- Single-step deltas are noisy; small windows amplify noise
- Does not capture trajectory shape — only direction

---

### Concept C19-C: Hybrid DTW-DVC with Drift Decomposition
**Description:** Combines the best of both approaches. Decomposes behavioral trajectories into three components:
1. **Systematic drift** (population-level trend) — removed
2. **Idiosyncratic drift direction** (agent-specific change direction) — compared via cosine similarity
3. **Trajectory shape** (how the drift unfolds over time) — compared via constrained DTW

**Architecture:**
1. Monthly BFE snapshots reduced to 50-dim representation via per-modality PCA
2. Population-mean trajectory subtracted to isolate idiosyncratic drift
3. Drift direction computed as cumulative displacement vector
4. Trajectory shape compared via Sakoe-Chiba band-constrained DTW (window = 2 months)
5. Final distance: d_Traj = alpha * cosine(drift_dir_i, drift_dir_j) + (1-alpha) * DTW_norm(shape_i, shape_j)
6. Cross-task trajectory comparison: separate trajectories per SEB task category, with multi-task consistency gating (rho_Traj) analogous to C17's rho_m

**Strengths:**
- Addresses systematic drift deconfounding (Analogy 4)
- Captures both direction AND shape of drift
- Constrained DTW reduces computational cost and prevents pathological warpings
- Multi-task trajectory consistency (rho_Traj) inherits C17's anti-coincidence framework
- Handles temporal misalignment via DTW while capturing direction via DVC

**Weaknesses:**
- More complex than C19-A or C19-B
- Three-component decomposition requires sufficient data (more monthly windows)
- PCA reduction may lose discriminative features
- More parameters to tune (alpha, DTW window, PCA dimensions)

---

## Round 1: Initial Positions

**Advocate (for C19-C):** The hybrid approach is the right one. C19-A's pure DTW misses the core insight — it measures trajectory *shape* similarity, but the signal is about drift *direction*. C19-B captures direction but cannot handle temporal misalignment, which is critical (creators update agents on different schedules). C19-C captures both while removing the systematic drift confound that would cause false positives. The complexity is justified because this is a specialized modality that activates only at Phase 2 with 6+ months of data — we have time and data to support the more sophisticated approach.

**Skeptic (against C19-C, for C19-B):** C19-C is over-engineered for a 6th modality with w=0.14. The trajectory modality is a *supplement* to the 5 core modalities, not a replacement. C19-B's drift vector correlation captures the most valuable signal (correlated direction) at much lower complexity. The temporal misalignment problem is overstated — most creators update all their agents simultaneously. The population-mean de-trending from C19-B is the critical innovation; DTW adds complexity without proportionate detection gain.

**Arbiter:** Both sides agree on population-mean de-trending — that is non-negotiable. The debate is whether DTW shape comparison adds enough value to justify its complexity. Key question: how common is temporal misalignment (staggered updates) in practice?

## Round 2: Evidence and Rebuttal

**Advocate:** Temporal misalignment IS common because agents may be updated independently even by the same creator. Consider: a creator fine-tunes Agent A in January and Agent B in March using the same RLHF data. Both drift in the same direction, but with a 2-month lag. C19-B's strict alignment would miss this. DTW catches it. Moreover, the constrained DTW with a 2-month window is computationally cheap — O(n * w) where w=2, so effectively linear. The marginal complexity over C19-B is small.

**Skeptic:** Fair point on staggered updates. But I remain concerned about the PCA reduction. Reducing 853 dims to 50 loses information. Counter-proposal: use C19-C's architecture but with per-modality drift comparison instead of PCA. Compare drift vectors within each modality separately (temporal drift, structural drift, etc.), then fuse per-modality trajectory distances using existing C17 weights. This is more interpretable AND avoids the PCA information loss.

**Arbiter:** The Skeptic's counter-proposal is sound. Per-modality trajectory comparison preserves interpretability and aligns with C17's existing architecture. Adopt C19-C's three-component decomposition but with per-modality drift decomposition instead of PCA-reduced combined vectors.

## Round 3: Convergence

**Consensus concept — C19-C+ (Hybrid DTW-DVC with Per-Modality Drift Decomposition):**

1. For each of the 5 existing modalities, compute monthly feature snapshots
2. Subtract population-mean trajectory per modality to isolate idiosyncratic drift
3. For each modality, compute:
   - **Drift direction:** cosine similarity of cumulative displacement vectors
   - **Trajectory shape:** band-constrained DTW distance (window = 2 months) on idiosyncratic trajectory
4. Fuse direction and shape: d_Traj_m = 0.6 * drift_direction_distance + 0.4 * DTW_shape_distance
5. Aggregate across modalities using C17 adversary weights: d_Traj = Sum(w_m * d_Traj_m)
6. Apply multi-task trajectory consistency gating (rho_Traj) using per-SEB-category trajectories

This preserves:
- Population-mean de-trending (from Analogy 4 / C19-B)
- Temporal misalignment handling (from C19-A / DTW)
- Per-modality interpretability (from C17 architecture)
- Multi-task consistency (from C17's rho_m framework)

---

# PART 4 — CONCEPT SELECTION

```json
{
  "type": "IDEATION_RESULT",
  "invention_id": "C19",
  "stage": "IDEATION",
  "selected_concept": "C19-C+",
  "concept_name": "Hybrid DTW-DVC with Per-Modality Drift Decomposition",
  "description": "A 6th behavioral modality that detects correlated behavioral drift over time. Decomposes per-modality trajectories into systematic (population) and idiosyncratic (agent-specific) components, then compares idiosyncratic drift via both direction correlation and band-constrained DTW shape similarity, with multi-task consistency gating.",
  "key_innovations": [
    "Population-mean de-trending to isolate idiosyncratic drift from environmental changes",
    "Dual drift comparison: direction (cosine) + shape (constrained DTW)",
    "Per-modality trajectory decomposition preserving C17 interpretability architecture",
    "Multi-task trajectory consistency (rho_Traj) extending C17's anti-coincidence framework"
  ],
  "design_actions_identified": [
    "Specify per-modality monthly snapshot extraction from Behavioral VTDs",
    "Specify population-mean trajectory computation and subtraction",
    "Specify DTW configuration: step pattern, Sakoe-Chiba band width, normalization",
    "Specify drift direction vector computation and cosine comparison",
    "Determine minimum observation windows for statistical significance",
    "Define updated 6-modality weight allocation",
    "Adversarial analysis: how to fake independent drift trajectories"
  ],
  "decision": "ADVANCE to RESEARCH"
}
```

---

**End of IDEATION Stage**

**Status:** IDEATION COMPLETE — C19-C+ selected, ADVANCE to RESEARCH
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Temporal Trajectory Comparison\C19_IDEATION.md`
