# T-060 Sentinel Graph — Cross-Domain Analogy Brief

**Prepared for:** Ideation Council (Round 0 Input)

---

## Analogy 1: Quorum Sensing in Bacterial Biofilms
**Source:** Microbiology — autoinducer signaling for population density detection (Vibrio fischeri, Pseudomonas aeruginosa).
**Parallel:** Each agent's behavioral telemetry = autoinducer molecules. Sybil clusters produce elevated "concentration" across multiple behavioral channels simultaneously. V. harveyi uses 3 distinct autoinducers — maps to multi-modality fusion. Biofilm spatial structure suggests locality weighting.
**Breakdown:** Bacteria want detection (cooperative); Sybil operators want evasion (adversarial). Telemetry requires active collection unlike passive diffusion.
**Design Insight:** Multi-channel threshold detection with locality weighting. Define behavioral "concentration fields" local to interaction neighborhoods. Detection fires when multiple channels simultaneously exceed threshold within a neighborhood. Sub-quadratic scaling because only local neighborhoods evaluated.

## Analogy 2: Forensic Ballistics — Striation Pattern Matching
**Source:** Forensic science — matching bullet striations to identify same-weapon origin via microscopic barrel imperfections.
**Parallel:** One operator ("barrel") controlling multiple agents ("bullets") leaves behavioral micro-patterns shared across identities. NIBIN system extracts canonical signatures and uses indexed correlation — equivalent to LSH for behavioral fingerprints. Forensics distinguishes class characteristics (gun model, shared by type) from individual characteristics (unique barrel) — maps to separating workload-induced similarity from operator-induced similarity.
**Breakdown:** Barrels don't disguise striations. Patterns are static; agent behavior evolves. No adversarial dimension.
**Design Insight:** Two-tier signature architecture: (1) compact behavioral fingerprint indexed for fast lookup, (2) explicit class vs. individual decomposition. Only individual-level deviations that cluster raise alerts. Directly addresses false-positive problem where similar workloads look correlated.

## Analogy 3: Seismograph Networks — Earthquake Triangulation
**Source:** Geophysics — distributed seismograph networks detecting earthquakes, locating epicenters, distinguishing events from noise.
**Parallel:** Thousands of sensors producing streaming data. Hierarchical trigger: per-station STA/LTA (cheap local) escalates to cross-station correlation (expensive global) only when multiple triggers cluster. Multi-consumer: same detection feeds tsunami warnings, building safety, research, insurance. Command propagation from operator to Sybil agents creates detectable timing correlations analogous to seismic wave propagation.
**Breakdown:** Earthquakes don't hide. Seismic wave physics is known; Sybil command propagation is adversarially variable. Fixed stations vs. dynamic agent populations.
**Design Insight:** Hierarchical trigger architecture — cheap per-agent anomaly detectors as first pass, expensive multi-agent correlation only on triggered clusters. Directly addresses O(V²) scaling. Also: "velocity model estimation" — inferring characteristic lag structure of operator command propagation as novel detection dimension.

## Analogy 4: Renaissance Counterpoint Rules (SURPRISING)
**Source:** Music theory — species counterpoint (Fux, Gradus ad Parnassum, 1725). Rules governing when simultaneous melodic voices maintain independence.
**Parallel:** Counterpoint defines independence: contrary/oblique motion, no parallel fifths/octaves, distinct rhythmic profiles, different registral space. Violations cause voices to perceptually fuse into one. A single operator's agents "move in parallel" — correlated timing (parallel rhythm), correlated errors (same wrong notes), correlated resources (same register). Sustained contrary motion is harder to maintain than it appears — lapses are statistically inevitable. Counterpoint also distinguishes surface independence (different notes) from deep dependence (same harmonic progression) — operators may decorrelate superficially while sharing deep structural logic.
**Breakdown:** Counterpoint rules are aesthetic conventions, not physical laws. Handles 2-6 voices, not thousands. Cultural specificity.
**Design Insight:** Define independence axioms. Instead of only looking for positive correlation evidence, define what genuinely independent agents should look like and flag violations. Inverts detection logic: "do these agents fail to exhibit expected independence?" rather than "are they suspiciously similar?" May catch sophisticated Sybils who decorrelate on obvious dimensions but fail on deeper structural ones.

## Analogy 5: Epidemiological Contact Tracing — Superspreader Identification
**Source:** Epidemiology — SARS-CoV-2/Ebola contact tracing and genomic phylogenetics for transmission tree reconstruction.
**Parallel:** Reconstruct operator-agent relationships from incomplete behavioral observations, like reconstructing who-infected-whom from symptom timing and viral genomes. Two patients from same superspreader carry similar viral genomes — two agents from same operator carry similar behavioral genomes. Tools: R0 estimation (how many agents per operator), overdispersion parameter k (heavy-tailed cluster sizes), backward tracing (from cluster to common source), phylogenetic tree construction (behavioral distance matrices).
**Breakdown:** Disease is involuntary; Sybil operation is intentional. Behavioral divergence can be engineered unlike random viral mutation. No confirmatory test equivalent.
**Design Insight:** Backward tracing and phylogenetic clustering. When suspicious behavior detected, trace backward through similarity graph to identify common source. Construct "behavioral phylogenies." Overdispersion insight: most operators control one agent — focus resources on the heavy tail.

---

## Cross-Cutting Themes

| Theme | Supporting Analogies |
|-------|---------------------|
| Locality is a scaling lever | 1 (quorum neighborhoods), 3 (triggered clusters) |
| Two-phase architecture (cheap screen → expensive correlation) | 2 (signature index), 3 (STA/LTA), 5 (case detection → tracing) |
| Inversion as detection strategy (define independence, flag violations) | 4 (counterpoint rules) |
| Signature drift is the hard sub-problem | 2 (barrel wear), 5 (viral mutation) |
| Adversarial evasion has no clean analogue | All five break down here |
