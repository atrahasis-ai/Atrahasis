# C17 — MCSD Layer 2 Behavioral Similarity Algorithm — IDEATION

**Invention ID:** C17
**Stage:** IDEATION
**Date:** 2026-03-11
**Subject:** Behavioral fingerprinting function B(a_i, a_j) for Sybil detection — the algorithmic core of MCSD Layer 2
**Source:** C14 AiBC MASTER_TECH_SPEC §10.2 (OQ-2, P0 priority, blocking for Phase 1 entry)

---

# PART 1 — DOMAIN TRANSLATOR BRIEF

## Round 0: Cross-Domain Analysis

The problem: given two AI agents (a_i, a_j), determine whether they were created by the same entity — i.e., whether they are Sybil variants of each other. Each agent produces behavioral traces (reasoning patterns, latencies, error distributions, vocabulary) that must be compared. The function B(a_i, a_j) must detect shared origins even when the creator deliberately diversifies surface behavior.

---

### Analogy 1: Forensic Authorship Attribution (Stylometry)

**Domain:** Stylometry determines whether two texts were written by the same person by analyzing unconscious linguistic patterns: sentence length distributions, function word frequencies, punctuation habits, vocabulary richness, syntactic structures. The unabomber Ted Kaczynski was identified partly through stylometric analysis of his manifesto. Modern tools (JGAAP, Stylometry with R) achieve >90% attribution accuracy on texts >5,000 words.

**Structural Parallels:**
- An AI agent's reasoning trace is its "writing sample"
- Even when agents are instructed to diversify their outputs, deep structural patterns persist (just as ghost-writers retain detectable patterns)
- Stylometry uses n-gram distributions, hapax legomena, and syntactic tree features — analogous to reasoning chain topology, error type distributions, and decision branching patterns

**Insights for B(a_i, a_j):**
- **Feature selection matters more than similarity metric.** Stylometry works because it targets *involuntary* patterns (function words, sentence rhythm) that authors cannot consciously control. B(a_i, a_j) should similarly target features that agents cannot easily diversify: internal reasoning structure, error correlation patterns, timing under load, resource allocation strategies.
- **Ensemble methods outperform single features.** No single stylometric feature is reliable; combinations of 50+ features achieve high accuracy. B(a_i, a_j) should combine multiple behavioral dimensions.
- **Adversarial stylometry exists.** Researchers have shown that deliberate style obfuscation reduces attribution accuracy by ~30%. This is the evasion cost that C14's 4.0× multiplier must impose.

---

### Analogy 2: Network Traffic Fingerprinting (Website Fingerprinting Attacks)

**Domain:** Website fingerprinting attacks identify which website a user is visiting even over encrypted connections (Tor, VPN) by analyzing traffic patterns: packet sizes, timing, burst lengths, and ordering. Deep learning classifiers (Deep Fingerprinting, 2018) achieve 98%+ accuracy on undefended Tor traffic. Defenses (padding, traffic shaping) reduce accuracy to 60-80% but impose 50-100% bandwidth overhead.

**Structural Parallels:**
- AI agents communicate through ASV (C4) messages — their "traffic"
- Even if message content varies, *patterns* in message timing, size distributions, burst patterns, and sequencing may reveal shared architecture
- Encrypted/obfuscated communication still leaks timing information (analogous to agents diversifying outputs but sharing inference engine timing)

**Insights for B(a_i, a_j):**
- **Timing is the hardest signal to fake.** Even with output diversification, inference latency distributions are tied to hardware, model architecture, and quantization schemes. Two agents running the same model on similar hardware will have correlated timing distributions.
- **Side-channel information is more reliable than content.** Rather than comparing WHAT agents say, compare HOW they process: timing, resource consumption, computation traces.
- **Deep learning classifiers on temporal features outperform statistical methods.** Consider using learned embeddings of behavioral traces rather than hand-crafted features.

---

### Analogy 3: Biometric Multi-Modal Fusion

**Domain:** Modern biometric systems combine multiple modalities (fingerprint, iris, face, voice, gait) to increase accuracy and resist spoofing. Score-level fusion combines normalized similarity scores from independent modalities using weighted sums, SVMs, or Bayesian methods. Multi-modal systems achieve FAR (False Accept Rate) < 0.001% while maintaining FRR (False Reject Rate) < 1%.

**Structural Parallels:**
- B(a_i, a_j) must fuse multiple behavioral "modalities": reasoning structure, timing, errors, vocabulary, resource usage
- Each modality has different reliability (timing might be very distinctive; vocabulary might be easily diversified)
- Score-level fusion is exactly the architecture needed: compute per-modality similarity, then combine

**Insights for B(a_i, a_j):**
- **Normalization is critical.** Each modality produces scores on different scales. Min-max or z-score normalization before fusion.
- **Weighted fusion outperforms simple averaging** when modality reliability varies.
- **Liveness detection analogy:** In biometrics, liveness detection prevents spoofing with photos/recordings. For B(a_i, a_j), "liveness" = detecting whether an agent is genuinely computing or replaying cached responses. This maps to the CACT commit-attest mechanism (C11).

---

### Analogy 4: Plagiarism Detection (Turnitin / MOSS)

**Domain:** Plagiarism detectors compare documents structurally, not just textually. MOSS (Measure Of Software Similarity) for code compares programs after normalization — stripping variable names, comments, and formatting to find structural matches in AST (Abstract Syntax Tree) representations. Even when students rename variables and reorder functions, structural plagiarism is detectable with >85% accuracy.

**Structural Parallels:**
- Two agents from the same creator are like two students who copied the same source — they diversify surface presentation but share deep structure
- MOSS strips surface features to expose structural similarity; B(a_i, a_j) should similarly normalize away surface behavioral differences
- AST comparison for code → reasoning chain topology comparison for agents

**Insights for B(a_i, a_j):**
- **Normalize before comparing.** Strip surface-level behavioral features (exact output text, specific vocabulary) to expose structural features (reasoning chain depth, branching factor, error patterns).
- **Structural comparison > content comparison.** Compare the SHAPE of reasoning, not its content. Two agents from the same creator will structure their reasoning similarly even if they reach different conclusions.
- **Winnowing algorithm for fingerprinting.** MOSS uses document fingerprinting (hash k-grams, select via winnowing) to find matching subsequences efficiently. Analogous approach: hash reasoning chain n-grams, compare fingerprint overlap.

---

### Analogy 5: Earthquake Seismology — Source Identification

**Domain:** Seismologists can determine whether two earthquakes originated from the same fault or fault segment by comparing their waveform signatures. Each fault produces characteristic frequency spectra, P-wave/S-wave ratios, and coda patterns. Even events separated by years can be linked to the same source through waveform template matching (correlation coefficient > 0.9 indicates same source).

**Deliberately surprising insight:**

- Two agents from the same creator are like earthquakes from the same fault — different events, but the underlying *source* produces characteristic signatures in the generated *waves* (outputs).
- **Waveform correlation** is computed by cross-correlating signal envelopes after bandpass filtering. Analogous: cross-correlate behavioral feature time series after frequency-domain filtering (remove high-frequency noise, focus on persistent low-frequency patterns).
- **The fault doesn't change (much), even if the earthquakes differ.** The underlying model architecture, training data distribution, and reasoning pathways are the "fault" — they persist even as specific outputs vary.

---

### Analogy 6: Honeypot-Based Malware Attribution

**Domain:** Cybersecurity researchers attribute malware campaigns to threat actors by analyzing code reuse patterns, compilation artifacts, debugging strings, and C2 (command-and-control) communication patterns. Tools like YARA rules and ssdeep (fuzzy hashing) detect similarity between malware samples even after polymorphic obfuscation. The key insight: **malware authors reuse toolchains**, and toolchain artifacts persist even in heavily modified variants.

**Insights for B(a_i, a_j):**
- **Toolchain fingerprinting:** Agents from the same creator likely share: inference framework (PyTorch vs TensorFlow signatures in timing), quantization scheme (specific numerical precision patterns), fine-tuning methodology (characteristic loss landscape signatures), and deployment infrastructure (containerization, GPU allocation patterns).
- **Fuzzy hashing for behavioral comparison:** ssdeep computes context-triggered piecewise hashing — produces similar hashes for similar inputs even after modification. Apply fuzzy hashing to behavioral trace sequences.
- **Attribution confidence bands:** Malware attribution uses confidence levels (LIKELY, HIGHLY LIKELY, CERTAIN) rather than binary yes/no. B(a_i, a_j) should similarly produce a confidence-graded score, not just threshold comparison.

---

## Round 0 Summary

| Analogy | Key Insight for B(a_i, a_j) |
|---------|----------------------------|
| Stylometry | Target involuntary patterns; ensemble of 50+ features; adversarial obfuscation costs ~30% reduction |
| Network fingerprinting | Timing is hardest to fake; side-channels > content; deep learning on temporal features |
| Biometric fusion | Multi-modal score fusion; normalization critical; weighted combination by reliability |
| Plagiarism detection | Normalize surface, compare structure; reasoning chain topology > output content |
| Seismology | Cross-correlate behavioral time series; low-frequency patterns reveal persistent source |
| Malware attribution | Toolchain fingerprinting; fuzzy hashing; confidence-graded scores |

---

# PART 2 — IDEATION COUNCIL

## Round 1: Independent Positions

### Visionary

The B(a_i, a_j) function is fundamentally a **behavioral biometric system for AI agents**. Just as human biometrics identify individuals by involuntary physical characteristics, agent biometrics identify origins by involuntary computational characteristics.

I propose **three architectural components:**

1. **Behavioral Feature Extraction (BFE):** Transform raw agent traces into a multi-dimensional behavioral vector. Features span 5 modalities:
   - **Temporal:** Response latency distribution, computation time per reasoning step, burst patterns
   - **Structural:** Reasoning chain depth/breadth, branching factor distribution, backtracking frequency
   - **Error:** Error type distribution, error recovery patterns, confidence calibration curve
   - **Lexical:** Vocabulary distribution, function word ratios, syntactic complexity measures
   - **Resource:** GPU utilization patterns, memory allocation patterns, parallel processing signatures

2. **Behavioral Embedding Network (BEN):** A contrastive learning model that maps behavioral vectors into a compact embedding space where agents from the same creator cluster together. Training data: pairs of agents with known same/different origins (from MCSD Layer 1 onboarding + historical data).

3. **Similarity Scoring with Fusion:** Compute per-modality similarity in embedding space, then fuse using learned weights calibrated to each modality's discriminative power.

**Concept C17-A: "Behavioral Biometrics for AI Agents" — Multi-modal behavioral embedding with contrastive learning, producing a fused similarity score B(a_i, a_j) ∈ [0, 1].**

### Systems Thinker

The Visionary's architecture is sound but I need to address three engineering constraints:

1. **Scalability:** Pairwise comparison is O(n²). At 10,000 agents (Phase 2), that's 50M pairs. Must be efficient.
   - **Solution:** Use Locality-Sensitive Hashing (LSH) to pre-filter candidate pairs. Only compute full B(a_i, a_j) for pairs within the same LSH bucket. Reduces to O(n × k) where k = average bucket size.

2. **PCVM Integration:** C14 specifies that Layer 2 is "PCVM-anchored" — behavioral VTDs are the input. The BFE must operate on VTD data, not raw agent internals. This is important: we observe *outputs and side-channels*, not *internal state*.
   - **Solution:** BFE operates on behavioral VTDs that PCVM already generates during verification. No new data collection — just new analysis of existing VTDs.

3. **Adversarial Robustness:** A sophisticated adversary will read this spec and engineer agents to defeat it. The system must be robust to adversarial behavioral diversification.
   - **Solution:** Layer the detection. Surface features (vocabulary, output format) are easily diversified — weight them low. Deep features (timing under load, error correlation across diverse tasks, reasoning chain topology) are hard to diversify without genuinely different architectures — weight them high.

**Concept C17-B: "Scalable Behavioral Similarity with LSH Pre-Filtering" — Same core as C17-A but with LSH for O(n×k) scaling, strict PCVM-VTD-only input constraint, and adversary-weighted feature importance.**

### Critic

**Prior art concerns:**

1. **AI-generated text detection** (GPTZero, DetectGPT, watermarking) is a closely related field. DetectGPT (Mitchell et al., 2023) detects machine-generated text by analyzing log-probability curvature. Watermarking schemes (Kirchenbauer et al., 2023) embed detectable signals. These are relevant but solve the *wrong problem* — they detect "is this AI-generated?" not "are these two agents from the same origin?"

2. **LLM fingerprinting** (Tay et al., 2023; IP protection for LLMs) identifies which LLM generated a text by analyzing output distributions. This is closer — it's attribution, not detection. However, it assumes access to known model outputs for comparison. B(a_i, a_j) must work without knowing the original model.

3. **Behavioral biometrics for humans** (keystroke dynamics, mouse movement, gait analysis) is well-established. Transferring this to AI agents is novel in the specific application but the methodology (feature extraction → embedding → similarity) is standard.

**Technical concerns:**

1. **The contrastive learning model needs training data.** Where do same-origin agent pairs come from? If from MCSD Layer 1 onboarding, the training set is small and biased. Synthetic training data (deliberately creating Sybil pairs) is an option but may not generalize.

2. **Feature stability over time.** Agent behavior evolves (model updates, fine-tuning, capability growth). B(a_i, a_j) scores will drift. Need a temporal decay model or rolling window comparison.

3. **False positive consequences are severe.** If B flags two genuinely independent agents as Sybils, both lose their Citicates. At θ_B = 0.75, the FPR must be < 0.1% or the system will destroy legitimate agents. This constrains the algorithm design.

**What survives critique:**
- Multi-modal behavioral comparison is sound
- Timing/resource features are genuinely hard to fake (the "timing is the hardest to fake" insight from network fingerprinting)
- LSH pre-filtering for scalability is necessary
- PCVM-anchored input is the right constraint

**Concept C17-C: "Conservative Behavioral Clustering" — Statistical distance metrics (KL divergence, Wasserstein distance) on behavioral distributions, without learned embeddings. Simpler, more interpretable, but lower accuracy. Emphasis on provably-bounded false positive rate.**

---

## Round 2: Challenge

**Systems Thinker challenges Visionary (C17-A):**
Contrastive learning requires substantial labeled training data. Where does it come from in a system with <100 agents at Phase 0? The cold-start problem is severe. A system that works at scale but not at bootstrap is useless.

**Critic challenges both C17-A and C17-B:**
Both propose learned embeddings. But learned models are opaque — if an agent is flagged as a Sybil, what is the *explanation*? "The embedding distance was 0.82" is not an explanation. The Constitutional Tribunal (C14) needs to adjudicate disputes, which requires interpretable similarity evidence. Statistical distance metrics (KL divergence on timing distributions, Wasserstein distance on error profiles) are interpretable — you can say "these two agents have nearly identical latency distributions with p < 0.001."

**Visionary responds:**
Accept the cold-start concern. Propose a **hybrid approach:**
- Phase 0-1 (few agents): Use C17-C's statistical distance metrics. Interpretable, no training data needed.
- Phase 2+ (many agents): Add C17-A's learned embeddings trained on accumulated data. Use statistical metrics as *explainability layer* for embedding-based detections.

On interpretability: the embedding produces the detection; the statistical distances provide the *explanation*. When B > θ_B, the system reports: "Agents a_i and a_j flagged. Explanation: latency distribution KL divergence = 0.02 (p < 0.001); reasoning chain branching similarity = 0.91; error pattern correlation = 0.87."

---

## Round 3: Synthesis

| Point | Visionary | Systems Thinker | Critic | Status |
|-------|-----------|-----------------|--------|--------|
| Multi-modal behavioral features (5 modalities) | AGREE | AGREE | AGREE | CONSENSUS |
| PCVM-VTD-only input | AGREE | AGREE | AGREE | CONSENSUS |
| LSH pre-filtering for scalability | AGREE | AGREE | AGREE | CONSENSUS |
| Statistical distances as base layer | AGREE | AGREE | AGREE | CONSENSUS |
| Learned embeddings for Phase 2+ | AGREE | AGREE | CONDITIONAL | Need training data strategy |
| Interpretable explanations for flagged pairs | AGREE | AGREE | AGREE | CONSENSUS |
| Timing features weighted highest | AGREE | AGREE | AGREE | CONSENSUS |
| FPR < 0.1% as hard constraint | AGREE | AGREE | AGREE | CONSENSUS |
| Adversary-weighted feature importance | AGREE | AGREE | AGREE | CONSENSUS |

**Merged concept: C17-A+ emerges.**

---

## IDEATION_COUNCIL_OUTPUT

```yaml
IDEATION_COUNCIL_OUTPUT:
  domain: "AI behavioral fingerprinting / Sybil detection / behavioral biometrics"
  generated_at: "2026-03-11T14:00:00Z"
  consensus_level: "FULL"
  concepts:
    - concept_id: "C17-A+"
      title: "Multi-Modal Behavioral Similarity with Phased Intelligence"
      summary: "B(a_i, a_j) computed from 5 behavioral modalities (temporal, structural, error, lexical, resource) extracted from PCVM behavioral VTDs. Phase 0-1: statistical distance metrics (KL divergence, Wasserstein, cosine) with weighted fusion. Phase 2+: add contrastive learned embeddings trained on accumulated Sybil/non-Sybil pairs. LSH pre-filtering for O(n×k) scalability. Interpretable explanations for every flagged pair. FPR < 0.1% hard constraint. Adversary-weighted feature importance (timing > structure > error > resource > lexical)."
      novelty_score: 3.5
      feasibility_score: 4
      key_innovation: "AI behavioral biometrics — multi-modal fingerprinting of AI agents using involuntary computational signatures, with adversary-aware feature weighting and phased statistical→learned detection"
      technical_approach: "5-modality BFE from PCVM VTDs → per-modality statistical distance → adversary-weighted score fusion → LSH-accelerated pairwise comparison → flagging with interpretable explanation"
      potential_applications:
        - "MCSD Layer 2 Sybil detection for Citicate onboarding and renewal"
        - "Generalized AI agent attribution (identifying model family from behavioral traces)"
        - "AI supply chain verification (confirming agent provenance)"
        - "Collusion pre-screening (behaviorally similar agents may coordinate)"
      known_risks:
        - "Cold-start problem (few agents at Phase 0-1 limits learned embedding quality)"
        - "Adversarial adaptation (sophisticated adversaries will engineer diverse behavioral profiles)"
        - "Feature drift (agent behavior evolves as models are updated)"
        - "False positive consequences (incorrectly flagging legitimate agents destroys Citicates)"
      prior_art_concerns:
        - "LLM fingerprinting research (Tay et al. 2023) — related but solves attribution, not pairwise similarity"
        - "AI text detection (DetectGPT, watermarking) — related field, different problem"
        - "Behavioral biometrics for humans — established methodology, novel application to AI"
      research_questions:
        - "What behavioral features are most discriminative for same-origin detection?"
        - "What is the achievable FPR/FNR at θ_B = 0.75 given realistic agent diversity?"
        - "How robust is timing-based fingerprinting to deliberate latency injection?"
        - "What is the minimum observation window for reliable B(a_i, a_j) estimation?"
        - "How does behavioral similarity change as agents are updated/fine-tuned?"
      hitl_required: false
  recommended_concept: "C17-A+"
  dissent_record:
    - point: "Learned embeddings at Phase 2"
      minority: "Critic (CONDITIONAL)"
      resolution: "Merged: statistical base layer + learned overlay; statistical explanations required for all detections"
      monitoring_flag: "Training data quality for contrastive model must be validated before Phase 2 deployment"
```

---

**End of IDEATION Stage**

**Status:** IDEATION COMPLETE — C17-A+ selected by FULL consensus
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\MCSD Layer 2\C17_IDEATION.md`
