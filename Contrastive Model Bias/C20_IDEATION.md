# C20 — Contrastive Model Training Bias Framework — IDEATION

**Invention ID:** C20
**Stage:** IDEATION
**Date:** 2026-03-11
**Subject:** Bias detection and mitigation for C17 Phase 2 contrastive learning training data
**Source:** C17 Monitoring Flag 3: "Training data for Phase 2 contrastive model must be validated for bias."
**Normative Reference:** C17 Section 12 (Contrastive Learning Model, Phase 2+)

---

# PART 1 — PRE-IDEATION: QUICK SCAN

## Known Solutions Brief

### 1. ML Fairness and Bias Detection (General)

**Existing tools and frameworks:**
- **IBM AI Fairness 360 (AIF360):** Open-source toolkit providing 70+ fairness metrics and 10+ bias mitigation algorithms. Addresses group fairness, individual fairness, and intersectional fairness. Designed for tabular classification; not directly applicable to contrastive learning on behavioral traces.
- **Google What-If Tool / ML Fairness Indicators:** Visualization-based bias exploration for TensorFlow models. Supports threshold calibration per subgroup. Limited to classification outcomes.
- **Microsoft Fairlearn:** Fairness constraints as optimization objectives (demographic parity, equalized odds). Works at the loss function level — potentially adaptable to contrastive loss.
- **Aequitas (UChicago):** Bias audit framework for binary/multi-class classifiers. Computes disparate impact ratios across protected groups.

**Relevance to C20:** These tools assume protected demographic attributes (race, gender, age). C20's "protected groups" are model families, infrastructure types, and task categories — fundamentally different. The mathematical frameworks (disparate impact ratios, equalized odds) are transferable; the group definitions are not.

### 2. Contrastive Learning Failure Modes

**Known issues in contrastive learning literature:**
- **Representation collapse:** Encoder maps all inputs to the same embedding region, producing trivially high similarity. Detected by monitoring embedding variance. Well-understood; addressed by temperature scaling and hard negative mining.
- **Shortcut learning (Simplicity bias):** Model learns to distinguish pairs using superficial features (e.g., model family metadata) rather than genuine behavioral similarity. Robinson et al. (2021) show that hard negatives reduce shortcut learning.
- **Class imbalance in contrastive loss:** NT-Xent and supervised contrastive loss assume balanced positive/negative ratios. C17 training data has a 1:10 positive:negative ratio (500:5,000) — this skew can bias the learned embedding toward the majority class.
- **Batch composition effects:** The composition of negative pairs within each training batch affects gradient quality. Sohn (2016) shows that more negatives per positive improve embedding quality, but only if negatives are truly independent.
- **Temperature sensitivity:** The temperature parameter in contrastive loss controls the concentration of the embedding distribution. Too low: model focuses on nearest negatives (may miss distant true positives). Too high: gradients become uniform (slow convergence).

**Relevance to C20:** These are failure modes of the learning algorithm itself. C20 must address them, but its primary focus is the training data — whether the labeled pairs accurately represent the deployment distribution.

### 3. Data Validation Frameworks

**Existing approaches:**
- **TensorFlow Data Validation (TFDV):** Schema-based data validation for ML pipelines. Detects anomalies, drift, and schema violations. Works on feature distributions.
- **Great Expectations:** Data quality assertions as code. Supports distribution checks, uniqueness constraints, cross-column validation.
- **DataRobot Bias Detection:** Automated bias scanning across protected attributes during model development.
- **Slice-based evaluation (Chen et al., 2019):** Evaluate model performance on semantically meaningful data slices rather than aggregate metrics. Reveals hidden failure modes in underrepresented subgroups.

**Relevance to C20:** These frameworks provide the infrastructure for validation but not the domain-specific bias taxonomy. C20 must define WHAT to validate (which biases exist in behavioral trace training data), not just HOW to validate.

### 4. Gap Analysis

No existing framework addresses bias in contrastive learning applied to AI agent behavioral traces. The specific challenges are:

1. **No protected attributes:** Traditional fairness frameworks require demographic groups. Agent populations have model families, infrastructure types, and task specializations — but these are not "protected" in the legal sense. The fairness criteria must be defined from first principles.
2. **Adversarial training data contamination:** Unlike typical ML bias (which arises from historical data), C17 training data can be actively poisoned by adversaries who submit mislabeled Sybil pairs. This is a security problem layered on a fairness problem.
3. **Evolving distribution:** Agent populations change over time as new model families emerge and old ones retire. Training data bias is not static — it shifts with population dynamics.
4. **Dual harm from bias:** Bias can cause false positives (legitimate agents falsely flagged as Sybils — governance harm) OR false negatives (real Sybils evading detection — security harm). The harm asymmetry is unique to Sybil detection.

**Conclusion:** C20 must build a domain-specific bias framework from first principles, borrowing mathematical tools from ML fairness but defining bias categories, detection methods, and mitigation strategies tailored to contrastive learning on behavioral trace data.

---

# PART 2 — DOMAIN TRANSLATOR BRIEF

## Round 0: Cross-Domain Analogies

**Problem statement:** When training a contrastive model to distinguish same-origin from independent-origin AI agents, what constitutes "bias" in the training data? How do we detect it? How do we mitigate it?

---

### Analogy 1: Clinical Trial Design (Biomedical Research)

**Domain:** Clinical trials test whether a drug works by comparing treatment and control groups. Bias in trial design — selection bias, allocation bias, measurement bias, attrition bias — can produce results that are statistically significant but clinically misleading. The Consolidated Standards of Reporting Trials (CONSORT) framework defines 7 categories of bias and requires explicit reporting of each.

**Structural Parallels:**
- Training pairs (same-origin / independent) are the "treatment" and "control" groups
- Selection bias: if training data over-represents agents from specific model families, the model learns "GPT-ness" rather than "same-origin-ness" — analogous to a trial that only enrolls young healthy patients
- Allocation bias: if positive pairs are generated synthetically but negative pairs come from production data, the distribution mismatch biases the boundary
- Measurement bias: if behavioral feature extraction (BFE) is systematically more precise for some agent types than others, the comparison is biased

**Where it breaks down:** Clinical trials have clear outcome measures (patient recovery). C17's "outcome" (same-origin or not) is fuzzy — two agents from the same model family may be genuinely independent.

**Design insight:** Adopt a CONSORT-like reporting framework for training data quality. Require explicit disclosure of bias sources for each training dataset version. Define a "training data quality checklist" analogous to CONSORT.

---

### Analogy 2: Jury Selection and Representativeness (Legal System)

**Domain:** The U.S. Constitution requires juries drawn from a "fair cross-section of the community." Systematic exclusion of identifiable groups (Batson v. Kentucky, 1986) produces biased verdicts. The venire (jury pool) must be representative; individual jurors may be excluded for cause, but not for group membership.

**Structural Parallels:**
- The training data is the "jury" that decides whether agent pairs are same-origin or independent
- If the training data systematically excludes certain agent types (e.g., small/rare model families), the contrastive model's "verdict" on those agents is unreliable
- Batson challenges (objecting to exclusion of a group) map to audit processes that flag underrepresented agent populations
- Peremptory challenges (removing individual datapoints) must be justified — data cleaning decisions must be documented

**Where it breaks down:** Juries make binary decisions; the contrastive model produces continuous embeddings. Jury bias affects one case; training data bias affects all future predictions.

**Design insight:** Define a "fair cross-section" requirement for training data: every agent model family with >1% population share must be represented in training pairs proportional to their population (or with documented justification for deviation). Establish an audit mechanism analogous to Batson challenges.

---

### Analogy 3: Ecological Sampling and the Observer Effect (Field Biology)

**Domain:** Ecologists studying animal populations must account for sampling bias: trap-shy species are underrepresented in capture-recapture studies; conspicuous species are over-counted in visual surveys; nocturnal species are missed in daytime sampling. The observer effect (animals change behavior when observed) further distorts data. Remedies include stratified sampling, occupancy modeling, and detection probability estimation.

**Structural Parallels:**
- Different agent architectures are "species" in the agent ecosystem
- Some agents may produce richer behavioral traces (more verbose reasoning, more detailed error messages) — making them easier to "capture" behaviorally, while others are "trap-shy" (minimal behavioral signatures)
- The SEB itself is an observation that changes behavior — agents may perform differently under evaluation than during organic tasks (the agent analog of "trap response")
- Population-level bias: if agent "species" have unequal detectability, the training data reflects detectability, not true origin

**Where it breaks down:** Animals are not adversarial (mostly). AI agent operators may deliberately manipulate behavioral traces to game the detection system.

**Design insight:** Model agent "detectability" per model family. If BFE produces weaker features for some agent types, the contrastive model will be biased against (or toward) those types. Measure and compensate for per-family feature richness before training.

---

### Analogy 4: Calibration of Scientific Instruments (Metrology)

**Domain:** In metrology, every measurement instrument has systematic bias (offset, scale factor, nonlinearity) that must be characterized and corrected before the instrument's readings are trustworthy. Calibration uses reference standards of known value. Recalibration is required periodically because instruments drift. The metrological traceability chain ensures that every measurement can be traced back to a primary standard.

**Structural Parallels:**
- The contrastive model is a "measurement instrument" for behavioral similarity
- Training data is the "calibration standard" — if the standard is biased, the instrument reads incorrectly
- The model "drifts" over time as the agent population evolves — periodic recalibration (retraining) is required
- Traceability: every training pair should be traceable to its confirmation method (how was "same-origin" or "independent" determined?)

**Where it breaks down:** Physical instruments have well-defined error models (Gaussian noise, linear drift). ML models have complex, high-dimensional error surfaces.

**Design insight:** Establish a "traceability chain" for training labels. Every positive pair must have a documented confirmation method (synthetic generation from known model, Layer 1 economic confirmation, Layer 3/4 detection). Every negative pair must have documented independence evidence. Reject training pairs with unverifiable labels.

---

### Analogy 5: Adversarial Machine Learning and Data Poisoning (Cybersecurity)

**Deliberately surprising analogy.**

**Domain:** Data poisoning attacks inject malicious training examples to manipulate a model's behavior at test time. Targeted poisoning (Shafahi et al., 2018) can cause a classifier to misclassify a specific test input by adding carefully crafted training examples that "pull" the decision boundary. Clean-label attacks (Zhu et al., 2019) achieve this without changing labels — only feature perturbation.

**Structural Parallels:**
- An adversary who controls Sybil agents knows which pairs are same-origin
- If the adversary's Sybils contribute to training data (via Layer 1/2/3/4 detections or red team exercises), the adversary can selectively mislabel pairs
- Clean-label poisoning: adversary creates genuinely independent-looking agents that are actually same-origin, submitting them as negative pairs — this "stretches" the negative cluster to encompass same-origin signatures
- Even without mislabeling: adversary's Sybil behavioral patterns in training data create "blind spots" — the model learns that those specific evasion patterns are "normal"

**Where it breaks down:** Traditional data poisoning targets specific test inputs. C17 adversaries want to evade detection for any future Sybil pair — a more diffuse goal.

**Design insight:** The training pipeline is itself an attack surface. C20 must include adversarial data validation: statistical tests for anomalous training pair distributions, provenance verification for all training labels, and holdout-based influence analysis (does removing a subset of training pairs significantly change model behavior?).

---

# PART 3 — IDEATION COUNCIL (3-Round Debate)

## Round 0: Context Absorption

Council members have read:
- PRE-IDEATION quick scan (ML fairness gaps, contrastive learning failure modes, data validation frameworks)
- Domain Translator cross-domain analogies (clinical trials, jury selection, ecological sampling, instrument calibration, data poisoning)
- C17 Section 12 (Phase 2 contrastive model architecture and training data strategy)
- C17 Monitoring Flag 3 context

---

## Round 1: Independent Positions

### Visionary

**Position: Comprehensive Bias Validation Pipeline (CBVP)**

The contrastive model's training data is not just a dataset — it is a policy instrument. Every labeled pair encodes a judgment about what "same-origin" means. Bias in this data directly translates to governance injustice (false accusations) or security failure (missed Sybils). We need a framework that treats training data quality as a first-class governance concern.

**Concept: Six-Dimensional Bias Taxonomy + Validation Pipeline**

I propose a framework organized around 6 bias dimensions, each with a detection method and mitigation strategy:

1. **Infrastructure Bias** — agents on similar hardware produce similar behavioral traces regardless of origin. Detection: measure BFE feature variance attributable to infrastructure vs. origin. Mitigation: infrastructure-conditional normalization (subtract infrastructure-specific baselines before training).

2. **Model Family Bias** — training data dominated by a few model families (GPT, Claude, Llama). Detection: population representation analysis (chi-square test of family distribution in training data vs. deployment population). Mitigation: stratified sampling + synthetic minority pair generation.

3. **Task Bias** — SEB tasks over-represent certain categories (e.g., coding tasks vs. creative tasks). Detection: per-category F1 score decomposition. Mitigation: category-balanced SEB selection + task-category-stratified validation splits.

4. **Temporal Bias** — training data from one time period may not generalize to another (model evolution, infrastructure changes). Detection: temporal holdout validation (train on months 1-12, validate on months 13-18). Mitigation: rolling retraining with recency weighting.

5. **Population Bias** — training data from a small early-phase population may not represent large-scale deployment. Detection: representation gap analysis (which agent types exist in deployment but not in training?). Mitigation: active learning — prioritize data collection for underrepresented agent types.

6. **Adversarial Bias (Data Poisoning)** — adversary deliberately mislabels or manipulates training pairs. Detection: influence analysis (which training pairs most affect model predictions?), label consistency checks (cross-validate labels against independent evidence). Mitigation: provenance verification, anomaly detection on training pair feature distributions.

**Engagement with Domain Translator analogies:**
The clinical trial analogy is the most powerful. Just as CONSORT requires explicit reporting of 7 bias categories, I propose a Training Data Quality Report (TDQR) that must accompany every model version. The TDQR documents: population composition, label provenance, temporal coverage, task coverage, known biases, and mitigation actions taken. No model deployment without an approved TDQR.

### Systems Thinker

**Position: Layered Validation Architecture**

The Visionary's 6-dimension taxonomy is sound, but the engineering architecture matters as much as the taxonomy. I propose a 3-layer validation pipeline:

**Layer 1 — Pre-Training Validation (Data Quality Gate)**
- Schema validation: every training pair conforms to the Behavioral VTD schema (C17 Section 8.2)
- Label provenance verification: every label has a documented source (synthetic, L1 confirmed, L2 statistical, L3/4 detection, red team)
- Distribution checks: model family distribution, infrastructure distribution, task distribution, temporal distribution
- Anomaly detection: flag training pairs with extreme feature values or unusual label-feature combinations
- Output: Data Quality Score (DQS) in [0, 1]. Training proceeds only if DQS >= 0.80.

**Layer 2 — Intra-Training Monitoring (Training Quality Gate)**
- Embedding space monitoring: track embedding variance, cluster structure, and separation metrics during training
- Per-subgroup loss decomposition: ensure loss converges uniformly across model families, not just in aggregate
- Gradient attribution: monitor which features the model relies on most — flag if infrastructure-correlated features dominate
- Shortcut detection: periodically test whether the model can be "fooled" by swapping infrastructure metadata while preserving behavioral features
- Output: Training Quality Score (TQS) in [0, 1]. Training aborted if TQS < 0.70 at any checkpoint.

**Layer 3 — Post-Training Validation (Deployment Gate)**
- Held-out validation per model family: FPR and FNR must not exceed 2x aggregate for any family with >1% population share
- Temporal holdout: model must achieve AUROC >= 0.93 on data from a time period not in training
- Adversarial probe: red team submits synthetic poisoned data and measures model vulnerability
- Population simulation: test model on synthetic population matching projected Phase 2+ distribution
- Output: Deployment Readiness Score (DRS) in [0, 1]. Deployment proceeds only if DRS >= 0.90.

**Integration with C17:** This 3-layer pipeline sits between C17 Section 12.2 (training data strategy) and Section 12.3 (model governance). It operationalizes the existing "AUROC >= 0.95" and "per-family FPR <= 2x aggregate FPR" requirements by specifying HOW to achieve them.

### Critic

**Position: Scope Risks and Prior Art Concerns**

**Prior art concern:** The combination of bias detection + mitigation for ML training data is well-explored (AIF360, Fairlearn, TFDV). C20 risks being a routine application of known techniques to a specific dataset. Novelty score could be as low as 2 if the framework is merely "AIF360 applied to contrastive learning."

**Counter-argument to Visionary:**
- 6 dimensions may be over-specified for the initial Phase 2 deployment. At Phase 2 entry, the agent population is ~1,000 (C14 phased deployment). With 500 positive and 5,000 negative pairs, the training data is small enough for manual review. Is a fully automated bias detection pipeline justified at this scale?
- Infrastructure bias mitigation via "conditional normalization" is risky — you might normalize away genuine same-origin signals that happen to correlate with infrastructure. The cure could be worse than the disease.

**Counter-argument to Systems Thinker:**
- The 3-layer validation architecture with 3 quality scores (DQS, TQS, DRS) introduces bureaucratic overhead that may delay Phase 2 deployment. C17 already has a deployment gate (AUROC >= 0.95). Adding two more gates creates a system that may never approve deployment.
- Gradient attribution during training is expensive and may not provide actionable information for a 3-layer MLP. It is more useful for deep networks with complex feature hierarchies.

**Analogy breakdown analysis (per Critic mandate):**

1. **Clinical trial analogy:** Breaks down because clinical trials have pre-registered protocols and external review boards. C20's "TDQR" has no external review — AiSIA reviews its own training data quality. This is a fox-guarding-henhouse problem.

2. **Jury selection analogy:** Breaks down because jurors are individuals making decisions; training data points are statistical inputs to gradient descent. The legal notion of "fair cross-section" does not have a rigorous mathematical definition in the embedding space context.

3. **Ecological sampling analogy:** Most productive analogy. The concept of "detectability" varying across agent types is a real and underappreciated risk. However, the analogy's remedy (occupancy modeling) assumes stable populations — agent populations are dynamic and adversarial.

4. **Instrument calibration analogy:** Sound but banal — all ML models need calibration. Does not contribute novel insight beyond "validate your model."

5. **Data poisoning analogy:** Critical insight. The training pipeline IS an attack surface. However, the Visionary's proposed mitigation (influence analysis) is computationally expensive for contrastive learning and may not scale to quarterly retraining. Simpler provenance-based filtering may be more practical.

**Key concern:** The real risk is not sophisticated bias — it is the simpler problem of model family dominance. If Phase 0-1 data is 80% GPT-based agents, the contrastive model will learn "GPT behavioral signature" rather than "same-origin behavioral signature." This single bias type accounts for the majority of the risk. C20 should focus on this before building an elaborate 6-dimension framework.

---

## Round 2: Challenge

### Systems Thinker challenges Visionary:

The 6-dimension taxonomy is comprehensive but risks over-engineering at the cost of deployment speed. I suggest a phased approach: implement dimensions 1-3 (infrastructure, model family, task) at Phase 2 entry, and add dimensions 4-6 (temporal, population, adversarial) at Phase 2+. This aligns with C17's own phased deployment philosophy.

Also: infrastructure bias mitigation via conditional normalization could strip away genuine signals. I propose a weaker remedy: infrastructure-aware stratification (ensure training pairs span diverse infrastructure combinations) rather than normalization (subtract infrastructure baselines).

### Critic challenges both:

The Critic's central challenge: is C20 a genuine invention or a quality assurance checklist? A bias taxonomy + validation pipeline is good engineering practice, not novel technology. The novelty must come from the specific bias types unique to behavioral trace contrastive learning (model family bias, adversarial label poisoning) and the detection methods tailored to them.

Also: the 3-layer validation architecture (Systems Thinker) creates coupling between training and deployment pipelines that may introduce fragility. If the DQS gate rejects training data, what happens? Does Phase 2 deployment delay indefinitely? There must be a fallback plan.

---

## Round 3: Synthesis

### Visionary responds:

I accept the Critic's point about scope. The 6-dimension taxonomy is the intellectual framework, but implementation should be phased. I also accept the Systems Thinker's concern about conditional normalization — infrastructure-aware stratification is safer.

On novelty: the Critic is right that individual bias detection techniques are known. The novelty is in (a) the domain-specific taxonomy for behavioral trace training data, (b) the adversarial label poisoning defense integrated into the training pipeline, and (c) the traceability chain for training labels. No existing framework addresses these together.

**Mark:** AGREE with phased implementation. CONDITIONAL on retaining all 6 dimensions in the specification (even if later phases).

### Systems Thinker responds:

I agree with the Critic that the 3-layer architecture needs a fallback. If DQS < 0.80, the fallback is: (1) document the specific bias, (2) apply targeted mitigation, (3) recompute DQS. If DQS cannot be raised to 0.80, Phase 2 contrastive model deployment delays and C17 continues with statistical-only B(a_i, a_j). This is not a failure — it is the correct conservative outcome.

On gradient attribution: I withdraw this from the initial specification. The MLP is too shallow for meaningful gradient attribution. Replace with simpler feature importance via permutation.

**Mark:** AGREE on phased implementation. AGREE on fallback to statistical-only B.

### Critic responds:

Satisfied with the phased approach and fallback plan. Remaining concern: adversarial label poisoning detection needs a concrete mechanism, not just "influence analysis." I propose a simpler approach: require that every positive pair label be confirmed by at least 2 independent detection layers (e.g., both L1 economic evidence AND L2 statistical B >= threshold). This is the metrology "traceability chain" made operational.

**Mark:** CONDITIONAL — the framework is ADVANCE-worthy only if adversarial bias detection has a concrete, implementable mechanism (not just a category name).

---

## IDEATION COUNCIL OUTPUT

```yaml
IDEATION_COUNCIL_OUTPUT:
  domain: "ML bias detection for contrastive learning on AI behavioral traces"
  generated_at: "2026-03-11T00:00:00Z"
  consensus_level: "MAJORITY"
  concepts:
    - concept_id: "C20-A"
      title: "Contrastive Model Training Bias Framework (CMTBF)"
      summary: "Six-dimensional bias taxonomy (infrastructure, model family, task, temporal, population, adversarial) with a 3-layer validation pipeline (pre-training, intra-training, post-training) for C17 Phase 2 contrastive learning. Phased implementation: dimensions 1-3 at Phase 2 entry, dimensions 4-6 at Phase 2+. Includes Training Data Quality Report (TDQR), label traceability chain, and fallback to statistical-only B(a_i, a_j) if validation fails."
      novelty_score: 3
      feasibility_score: 4
      key_innovation: "Domain-specific bias taxonomy for behavioral trace contrastive learning, with adversarial label poisoning defense and multi-layer label traceability"
      technical_approach: "Pre-training distribution analysis + intra-training embedding monitoring + post-training per-subgroup validation. Adversarial bias detection via multi-source label confirmation and influence function analysis."
      potential_applications:
        - "C17 Phase 2 contrastive model training validation"
        - "Reusable framework for any future Atrahasis ML component"
        - "Template for bias auditing in security-critical contrastive learning"
      known_risks:
        - "Over-engineering may delay Phase 2 deployment"
        - "Infrastructure bias mitigation may strip genuine signals"
        - "Adversarial label poisoning detection may be computationally expensive"
      prior_art_concerns:
        - "Individual bias detection techniques are well-known (AIF360, Fairlearn)"
        - "Novelty depends on domain-specific taxonomy, not individual methods"
      research_questions:
        - "What is the empirical model family distribution in Phase 0-1 data?"
        - "How computationally expensive is influence function analysis for a 3-layer MLP?"
        - "What is the minimum training data size for reliable per-family validation?"
        - "Can adversarial label poisoning be detected without influence functions?"
      hitl_required: true
  recommended_concept: "C20-A"
  dissent_record:
    - point: "Framework may be over-engineered for Phase 2 scale (~1,000 agents)"
      minority: "Critic"
      monitoring_flag: "Validate that framework complexity is proportional to population size. Consider streamlined version for initial deployment."
    - point: "Conditional normalization for infrastructure bias may strip genuine signals"
      minority: "Critic + Systems Thinker"
      monitoring_flag: "Use stratification (not normalization) for infrastructure bias at Phase 2 entry. Revisit normalization at Phase 3."
    - point: "Adversarial bias detection needs concrete mechanism, not just taxonomy entry"
      minority: "Critic"
      monitoring_flag: "Training data for Phase 2 contrastive model must be validated for bias — specifically, multi-source label confirmation must be specified as a concrete algorithm."
```

---

**HITL Gate:** Concept C20-A selected for advancement to RESEARCH.

**End of IDEATION.**
