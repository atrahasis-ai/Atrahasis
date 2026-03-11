# Science Assessment — C6 Epistemic Metabolism Architecture (EMA)

**Assessor:** Science Advisor
**Invention:** C6 — Epistemic Metabolism Architecture
**Date:** 2026-03-10
**Protocol:** Atrahasis Agent System v2.0

---

## Executive Summary

C6 proposes replacing the underspecified Knowledge Cortex with an Epistemic Metabolism Architecture (EMA) that treats knowledge as a living metabolic process. Knowledge units ("epistemic quanta") are ingested, circulated through a coherence graph, consolidated during "dreaming" phases, and catabolized when they lose coherence or relevance. A SHREC regulatory system combining ecological budget competition with graduated PID control governs metabolic rates. Multi-ontology projection functions allow different subsystems (C3/C4/C5) to view the same knowledge in native formats.

After assessment, the architecture is **PARTIALLY_SOUND** overall. The metabolic metaphor is generative but risks over-commitment — it produces useful architectural heuristics (decay, consolidation, circulation) but does not constitute a formal theory that makes falsifiable predictions distinguishing it from alternative knowledge management architectures. The strongest components are knowledge catabolism (well-grounded in garbage collection theory and information lifecycle management) and the SHREC regulatory system (well-grounded in control theory, though the biological analogy is looser than claimed). The weakest components are the dreaming consolidation claim (dependent on unproven LLM capabilities for reliable cross-domain synthesis) and the bidirectional projection claim (which faces fundamental information-theoretic barriers).

The claims cohere as a system at the metaphorical level but have gaps at the formal level: no information-theoretic analysis of projection loss, no convergence proof for SHREC dynamics, no empirical basis for LLM consolidation reliability, and no formal definition of "epistemic quantum" that would distinguish it from existing knowledge representation formalisms.

**Overall Soundness Score: 3.0 / 5** — Creative architectural vision that synthesizes real theoretical traditions, but the metabolic framing is more metaphorical than formal, and several claims require substantial theoretical and empirical work to substantiate.

---

## 1. Per-Claim Assessments

### Claim 1: Knowledge as Metabolic Process

**Soundness: PARTIALLY_SOUND**

#### A. Theoretical Soundness

The idea that knowledge should be treated as a dynamic, living process rather than static storage draws on several legitimate theoretical traditions:

1. **Autopoiesis (Maturana & Varela, 1980).** Living systems continuously produce and replace their own components. The metabolic metaphor maps: ingestion = knowledge acquisition, circulation = knowledge distribution, anabolism = knowledge construction (combining simpler units into complex understanding), catabolism = knowledge decomposition (breaking down outdated structures, recycling components). Autopoiesis specifically predicts that a knowledge system must be *operationally closed* — its knowledge-maintenance processes must themselves be describable within the system. EMA appears to satisfy this if SHREC signals are themselves epistemic quanta.

2. **Enactivism (Varela, Thompson & Rosch, 1991).** Knowledge is not representation of a pre-given world but is enacted through interaction. This supports treating knowledge as process rather than storage. However, enactivism also implies that knowledge cannot be separated from the agent that enacts it — a challenge for a shared knowledge substrate serving multiple subsystems.

3. **Knowledge lifecycle management (Nonaka & Takeuchi, 1995; Wiig, 1993).** The SECI model (Socialization, Externalization, Combination, Internalization) treats knowledge as undergoing phase transitions. The metabolic model can be seen as a refinement: SECI's four modes map roughly to ingestion (externalization), circulation (socialization), anabolism (combination), and catabolism (a phase SECI lacks — knowledge retirement).

4. **Garbage collection and memory management (McCarthy, 1960; Wilson, 1992).** Computer science has long treated memory as requiring active management — allocation, reference counting, garbage collection, compaction. Catabolism is essentially garbage collection with semantic awareness.

**However, the critical question is whether the metabolic framing is more than a metaphor:**

- **Predictive power test.** A genuine metabolic theory should predict specific phenomena that a non-metabolic architecture would not predict. For example: (a) metabolic rate should correlate with system health in a specific, measurable way; (b) "metabolic diseases" (analogues to diabetes, autoimmune disorders) should be identifiable failure modes with specific signatures; (c) homeostatic setpoints should exist and be derivable from system parameters. If these predictions are not falsifiable, the metabolic framing is heuristic, not theoretical.

- **The metabolism metaphor over-determines the architecture.** Biological metabolism has features that may be architectural liabilities if taken literally: metabolic pathways are highly conserved (resistant to change), metabolic diseases cascade (a single enzyme deficiency can be lethal), and metabolic regulation involves hundreds of interacting feedback loops. The proposal must specify which features of metabolism are load-bearing and which are decorative.

- **Alternative framings produce similar architectures.** An "information ecosystem" metaphor (knowledge as organisms in an ecology) or a "knowledge market" metaphor (knowledge as goods with supply and demand) would produce many of the same architectural features (lifecycle, competition, decay, consolidation) without committing to the specific metabolic vocabulary. The metabolic framing must justify itself against these alternatives.

**Assumptions:** (a) That the four metabolic phases (ingestion, circulation, anabolism, catabolism) are exhaustive — what about excretion (deliberate export)? Secretion (controlled release of processed knowledge)? (b) That metabolic rate is a meaningful scalar — biological metabolism is not a single rate but thousands of coupled rates. (c) That homeostasis is the right regulatory target — many knowledge systems benefit from punctuated equilibrium rather than homeostasis.

#### B. Empirical Evidence

**Existence proofs for knowledge-as-process:**
- Wikipedia's editorial ecosystem treats knowledge as continuously maintained, with processes analogous to ingestion (article creation), circulation (cross-linking), anabolism (article merging, synthesis), and catabolism (deletion, archiving). Wikipedia's success suggests the process model is viable at scale.
- Biological neural networks: memory consolidation (sleep-dependent, Diekelmann & Born 2010), synaptic pruning (Huttenlocher 1979), and memory reconsolidation (Nader, Schafe & LeDoux 2000) all treat memory as metabolic.
- Organizational knowledge management: Nonaka's knowledge-creating company demonstrates that treating knowledge as process rather than asset improves innovation outcomes.

**No existence proofs for:** A software system that implements the full metabolic cycle with measurable homeostatic regulation and demonstrates superiority over conventional knowledge management.

**Falsification experiments:**
1. Implement a minimal metabolic knowledge system and a matched non-metabolic baseline (standard knowledge graph with TTL-based expiry and periodic re-indexing). Measure: knowledge retrieval quality over time, staleness rate, storage growth, and response to sudden knowledge influx or invalidation. If the metabolic system does not outperform the baseline on at least 2 of 4 metrics, the metabolic framing does not justify its complexity.
2. Test homeostatic prediction: perturb the system (inject large amounts of contradictory knowledge) and measure recovery time. A metabolic system should exhibit characteristic recovery dynamics (overshoot, settling time) predictable from SHREC parameters. If recovery is unpredictable from parameters, the regulatory model is not doing useful work.

---

### Claim 2: Epistemic Quanta with Multi-Ontology Projection

**Soundness: PARTIALLY_SOUND**

#### A. Theoretical Soundness

The idea of a unified internal representation that can be projected into different views is well-established:

1. **Category theory and functors.** A functor F: C -> D maps objects and morphisms from category C to category D while preserving composition and identity. If epistemic quanta form a category and each ontological frame is a category, then projection functions are functors. Bidirectionality requires the functors to be part of an adjunction (left adjoint / right adjoint pair), which is a well-studied structure. **Crucially, adjunctions do not require bijectivity** — the round-trip F followed by its adjoint G gives a unit/counit transformation that is generally not the identity. This means information loss is the norm, not the exception.

2. **Database view theory (ANSI/SPARC, 1975).** The three-schema architecture (conceptual, logical, external) has the same structure: one internal representation, multiple external views. View update theory (Bancilhon & Spyratos, 1981; Dayal & Bernstein, 1982) demonstrates that view updates are generally not uniquely translatable back to base relations — the "view update problem." This is a formal result, not an engineering limitation.

3. **Ontology alignment (Euzenat & Shvaiko, 2007).** The ontology matching community has decades of work on translating between ontological representations. Key finding: fully automatic, lossless alignment between independently developed ontologies is not achievable in general. Precision-recall tradeoffs are fundamental.

4. **Information theory.** If two ontological frames have different information capacities (different numbers of distinguishable states), then by the data processing inequality, the lower-capacity frame cannot represent all distinctions made in the higher-capacity frame. Bidirectional lossless projection requires the frames to be informationally isomorphic, which is a very strong condition unlikely to hold between, say, a graph-based frame (C3 Tidal Noosphere) and a proof-carrying frame (C5 PCVM).

**The formal conditions for bidirectional projection without information loss are:**
- The projection functions must form a Galois connection (monotone, with F(G(x)) >= x and G(F(y)) <= y), or more strongly, an isomorphism.
- The ontological frames must be expressively equivalent (same information capacity).
- The internal representation must be at least as expressive as the most expressive external frame.

**These conditions are unlikely to hold in practice** between C3 (coordination topology), C4 (semantic vocabulary), and C5 (verification claims). Each frame captures aspects the others do not: C3 captures spatial/temporal coordination context, C4 captures semantic structure, C5 captures epistemic confidence and verification status.

**A more honest claim:** Projection functions can translate between frames with *controlled, measurable* information loss, and round-trip projections satisfy specified fidelity bounds. This is achievable and still valuable.

**Counterexamples:**
- The RDF/OWL ecosystem attempted universal knowledge representation with ontology mapping. After 20+ years, fully automated lossless interoperability between independently developed ontologies remains unsolved (Ontology Alignment Evaluation Initiative, OAEI, annual results).
- Google's Knowledge Graph and Wikidata use different internal representations and maintain separate schemas rather than projecting from a unified internal form — suggesting that in practice, the unified representation approach does not scale.

#### B. Empirical Evidence

**Existence proofs for the approach:**
- Protocol Buffers / Avro / Thrift: schema-based serialization formats that project between language-specific representations. These work because the domain is narrow (structured data types) and the projections are well-defined. Knowledge representation is far richer.
- GraphQL: projects a unified data graph into query-specific views. The projections are one-directional (read-only) by default; mutations require explicit schema alignment.
- CycL / SUMO: upper ontologies that attempt to provide a unified conceptual framework from which domain ontologies can be derived. Partial success in narrow domains; no demonstrated success for cross-domain knowledge at scale.

**No existence proofs for:** Bidirectional, lossless projection of general knowledge between fundamentally different representational frameworks (graph-based, proof-based, semantic-vocabulary-based).

**Falsification experiments:**
1. Define 20 representative epistemic quanta spanning all 8 claim classes from C5. For each, implement projection into C3 format (parcel/epoch context), C4 format (ASV semantic representation), and C5 format (VTD with credibility). Measure round-trip fidelity: project to each frame and back, compute semantic similarity to original. If mean fidelity < 0.8 for any pair of frames, the "without translation loss" claim is falsified.
2. Identify the information-theoretic capacity of each ontological frame (count distinguishable states for a fixed quantum). If capacities differ by more than 2x between frames, bidirectional lossless projection is impossible by data processing inequality — the claim must be weakened.

---

### Claim 3: Dreaming Consolidation

**Soundness: PARTIALLY_SOUND**

#### A. Theoretical Soundness

The "dreaming" consolidation concept draws on:

1. **Sleep-dependent memory consolidation (Diekelmann & Born, 2010; Walker & Stickgold, 2004).** During sleep, the brain replays experiences, consolidates declarative memories (hippocampus to neocortex transfer), and integrates new knowledge with existing schemas. REM sleep in particular is associated with creative problem-solving (Wagner et al., 2004) and insight (Cai et al., 2009). The neuroscience is well-established.

2. **Analogical reasoning and structure mapping (Gentner, 1983; Hofstadter & Sander, 2013).** Cross-domain pattern discovery requires finding structural correspondences between different knowledge domains. Structure Mapping Theory (SMT) provides a formal account: analogy maps relational structure (not surface features) from a source to a target domain. This is computationally expensive (mapping is NP-hard in general, Veale & Keane, 1997) but tractable with heuristics.

3. **Scientific discovery as search (Langley et al., 1987; BACON, EUREKA).** Automated discovery systems have found scientific laws by searching for patterns in data. However, these systems work on numerical data with well-defined variables, not on heterogeneous natural-language knowledge claims.

**The critical question is whether LLMs can reliably perform this consolidation:**

- **LLMs as analogical reasoners.** Recent work (Webb et al., 2023; Mitchell & Krakauer, 2023) shows LLMs can perform analogical reasoning on standardized tests, but performance degrades significantly on novel analogies outside training distribution. Cross-domain synthesis requires precisely this kind of novel analogy.

- **Hallucination risk.** The consolidation process — "synthesize general principles from specific claims" — is exactly the kind of task where LLMs hallucinate. A system that generates plausible-sounding but false general principles and injects them into the knowledge base could be actively harmful. The proposal must specify how consolidated outputs are verified before integration.

- **Confirmation bias.** LLMs tend to find patterns that confirm common associations in their training data. A consolidation process might systematically "discover" well-known cross-domain analogies (everything is like evolution, everything is like a market) while missing genuinely novel connections.

- **Reproducibility.** LLM outputs are stochastic. Two dreaming cycles over the same knowledge may produce different consolidations. The system must specify whether consolidation outputs are deterministic (temperature 0, which reduces creativity), stochastic (which requires a voting/consensus mechanism), or somehow constrained to be reproducible.

**Comparison to existing systems:**
- Google DeepMind's AlphaFold consolidates structural biology knowledge but does so through learned neural representations, not explicit reasoning. The dreaming claim is more ambitious: explicit, interpretable principle extraction.
- IBM Watson's "discovery" capabilities search for patterns in literature but rely on co-occurrence statistics, not deep analogical reasoning. Results are suggestive, not reliable.

**Assumptions:** (a) That LLMs can reliably distinguish genuine cross-domain patterns from superficial similarities; (b) that the rate of valuable discoveries exceeds the rate of harmful hallucinations; (c) that the computational cost of periodic LLM-based reasoning is justified by the value of discoveries; (d) that discovered principles can be verified before integration.

#### B. Empirical Evidence

**Existence proofs:**
- Sleep-dependent consolidation in biological neural networks is empirically established (thousands of studies, see Walker 2017 for review).
- Automated scientific discovery: BACON discovered Kepler's third law, Ohm's law from numerical data (Langley et al., 1987). DENDRAL discovered organic chemistry rules (Buchanan & Feigenbaum, 1978). These are genuine existence proofs but in very narrow, well-structured domains.
- LLM-based literature review: systems like Semantic Scholar, Elicit, and consensus.app use LLMs to synthesize findings across papers. These sometimes find genuine patterns but frequently produce overconfident or incorrect syntheses.

**No existence proofs for:** Reliable, unsupervised LLM-based discovery of cross-domain principles from a heterogeneous knowledge base, with error rates low enough for autonomous integration.

**Falsification experiments:**
1. Assemble 100 knowledge claims from 5 domains (20 per domain). Manually identify 10 genuine cross-domain patterns and 10 plausible but false ones (controls). Run the dreaming consolidation process. Measure: precision (what fraction of discovered "principles" are genuine), recall (what fraction of genuine patterns are found), and hallucination rate (fraction of outputs that are neither genuine nor control patterns but fabricated). If precision < 0.6 or hallucination rate > 0.2, the claim that dreaming produces "emergent understanding" is undermined — it produces emergent noise.
2. Run the same dreaming process 5 times on the same knowledge base. Measure consistency: Jaccard similarity of discovered principles across runs. If Jaccard < 0.5, the process is too stochastic for reliable knowledge base integration.
3. Compare dreaming consolidation against a baseline: human-curated cross-domain synthesis by a domain expert given the same 100 claims. If LLM consolidation precision is less than 50% of human precision, the approach needs significant guardrails.

---

### Claim 4: SHREC Regulatory System

**Soundness: PARTIALLY_SOUND**

This is the most technically substantive claim, with several sub-claims that warrant individual assessment.

#### Sub-claim 4a: Budget Competition as Lotka-Volterra Dynamics

**Soundness: PARTIALLY_SOUND**

**Theoretical grounding:** Lotka-Volterra equations model predator-prey and competitive dynamics in ecology. The classic competitive Lotka-Volterra model (two species competing for shared resources) has well-characterized behavior:

- Two stable equilibria (one species dominates) and one unstable coexistence equilibrium (for 2 species)
- With N species: competitive exclusion principle predicts at most K species coexist on K resources (Hardin, 1960; Levin, 1970)
- Coexistence requires niche differentiation — each species must be limited by a different resource

**Applicability to knowledge signals:** The four SHREC signals (presumably: Saturation, Hunger, Renewal, Elimination — or similar) compete for computational budget. The Lotka-Volterra analogy holds if:

1. **Signals consume a shared, finite resource (budget).** This is architecturally enforceable. SOUND.
2. **Signal interactions are pairwise and continuous.** Lotka-Volterra assumes continuous, deterministic dynamics. Knowledge processing is discrete and stochastic. The continuous approximation is valid only if the number of knowledge operations per time step is large (law of large numbers). For a small system processing 10 quanta/epoch, the dynamics will be highly stochastic and Lotka-Volterra predictions will be unreliable. PARTIALLY_SOUND — depends on scale.
3. **Interaction coefficients are constant.** In ecology, alpha_ij (the competitive effect of species j on species i) is assumed constant. In a knowledge system, the interaction between signals changes as the knowledge base evolves. This is a significant deviation — Lotka-Volterra with time-varying coefficients is a much harder system with fewer guarantees. PARTIALLY_SOUND.
4. **No higher-order interactions.** Standard Lotka-Volterra is pairwise. If SHREC signals interact in triples or higher (e.g., the effect of hunger on elimination depends on the level of saturation), the dynamics are not Lotka-Volterra and standard results do not apply. UNKNOWN — depends on implementation.

**Key concern:** The competitive exclusion principle implies that in steady state, the number of coexisting signals cannot exceed the number of independent limiting resources. If there is only one resource (computational budget), only ONE signal should dominate at equilibrium. To maintain all four signals active requires either: (a) four independent resources (e.g., CPU, memory, I/O, LLM calls), (b) frequency-dependent selection (signals become more competitive when rare), or (c) environmental fluctuation that prevents equilibrium. The proposal must address this.

#### Sub-claim 4b: Sigma-Derived PID Gains (Ziegler-Nichols Adaptation)

**Soundness: PARTIALLY_SOUND**

**Theoretical grounding:** PID control is the most widely used control strategy in industrial applications. Ziegler-Nichols tuning (1942) provides heuristic rules for setting PID gains based on the system's step response or ultimate gain/period. The method is well-established but known to produce:

- Aggressive tuning (25% overshoot by design)
- Poor performance for systems with long dead times
- Instability for systems with time-varying dynamics

**Adaptation to sigma-based gains:** Using the standard deviation (sigma) of a signal as the basis for PID gains is non-standard. The logic is presumably: high sigma indicates high variability, requiring stronger control action. This is reasonable as a heuristic but lacks formal justification:

1. **Sigma measures variability, not system dynamics.** Ziegler-Nichols derives gains from the system's dynamic response (rise time, settling time, ultimate period). Sigma captures statistical spread but not the causal structure of the system. A system with high sigma due to measurement noise requires *weaker* control (to avoid amplifying noise), while high sigma due to genuine disturbances requires *stronger* control. Sigma alone cannot distinguish these cases.

2. **PID assumes a linear, time-invariant plant.** Knowledge metabolism is neither linear nor time-invariant. PID control of nonlinear systems can work locally (around an operating point) but may fail globally. The proposal's claim that PID is a "safety net" rather than the primary controller is wise — but the safety net must not destabilize the primary controller (ecological competition). The interaction between the two control layers needs stability analysis.

3. **Integral windup.** If the PID controller has an integral term, long periods where the error is non-zero (common during knowledge regime transitions) will cause integral windup, producing large corrective actions when the system finally responds. Anti-windup mechanisms are well-understood but must be explicitly specified.

**The claim that this requires "minimal tuning (7 parameter categories vs dozens for pure adaptive)" is reasonable** — PID has 3 gains per loop, and pre-computing them from sigma reduces ongoing tuning. But the comparison to "dozens for pure adaptive" is a strawman — many adaptive controllers also have few parameters (e.g., Model Reference Adaptive Control has 2-4 parameters per loop).

#### Sub-claim 4c: Bayesian Priors for Cold Start

**Soundness: SOUND**

**Theoretical grounding:** Using Bayesian priors to initialize system parameters when no data is available is standard practice in machine learning and control theory:

- Empirical Bayes (Robbins, 1956): use marginal distribution of data to estimate priors
- Conjugate priors (Raiffa & Schlaifer, 1961): choose priors that produce analytically tractable posteriors
- Informative priors from domain knowledge (Gelman et al., 2013): encode known constraints

For SHREC, reasonable priors could encode: (a) expected knowledge ingestion rate based on system capacity; (b) expected contradiction rate based on domain characteristics; (c) expected staleness rate based on domain volatility. These are defensible initial estimates.

**One concern:** The quality of cold-start priors depends entirely on the quality of the domain model used to set them. If priors are poorly calibrated (e.g., assuming a static domain when the system operates in a rapidly evolving one), the system will behave poorly until enough data accumulates to overwhelm the priors. The proposal should specify: (a) how priors are set, (b) how quickly they are overridden by data, and (c) what happens if priors are badly wrong (graceful degradation or catastrophic failure).

#### Sub-claim 4d: Change-Point Detection for Scale Transitions

**Soundness: SOUND**

**Theoretical grounding:** Change-point detection is a well-established field:

- CUSUM (Page, 1954): cumulative sum control charts for detecting shifts in mean
- Bayesian Online Changepoint Detection (Adams & MacKay, 2007): principled Bayesian framework
- PELT (Killick, Fearnhead & Eckley, 2012): efficient algorithm for multiple change-point detection

The idea that a knowledge system will undergo regime changes (e.g., when the number of agents doubles, when a new domain is added, when the system is federating with another instance) is architecturally sound. Detecting these transitions and adjusting regulatory parameters accordingly is good engineering.

**Concerns:** (a) What parameters are adjusted at change points? If SHREC gains are recomputed, the system may oscillate during transitions. (b) False positive change-point detection could trigger unnecessary parameter changes, destabilizing an otherwise stable system. The detection threshold is a tunable parameter that itself needs tuning — this is the recursive tuning problem.

#### Sub-claim 4e: Immune Self-Audit Against Autoimmune Pathology

**Soundness: PARTIALLY_SOUND**

**Theoretical grounding:** The biological immune system distinguishes self from non-self, but autoimmune diseases occur when this distinction fails. Artificial Immune Systems (AIS, de Castro & Timmis, 2002) are an established computational paradigm:

- Negative selection algorithm (Forrest et al., 1994): generate detectors that match non-self but not self
- Clonal selection (de Castro & Von Zuben, 2002): adaptive immune response through selection and mutation
- Danger theory (Aickelin & Cayzer, 2002): immune response triggered by danger signals, not just non-self

**The autoimmune pathology concern is valid and important:** If the catabolic process (knowledge elimination) becomes overly aggressive, it could destroy valid knowledge — the system attacks itself. This is a real failure mode.

**However, the immune metaphor introduces more complexity than needed.** The core requirement is: "don't delete valid knowledge." This can be addressed more directly through:
- Soft deletion with undo windows
- Quorum requirements for catabolism
- Coherence threshold validation before deletion

Framing this as "immune self-audit" adds vocabulary without adding formal precision. The critical question is whether the immune framing provides detection mechanisms that simpler approaches would miss.

#### Overall SHREC Assessment

**Soundness: PARTIALLY_SOUND**

The SHREC system combines well-grounded components (Bayesian priors, change-point detection, PID control) with a looser biological analogy (Lotka-Volterra competition, immune self-audit). The ecological competition as primary controller is the most novel and least proven component. The key risk is emergent instability from the interaction between ecological dynamics and PID overlay — this interaction needs formal stability analysis (e.g., Lyapunov stability, describing function analysis for the nonlinear/linear combination).

---

### Claim 5: Coherence Graph as Circulatory System

**Soundness: PARTIALLY_SOUND**

#### A. Theoretical Soundness

The coherence graph with typed edges (support, contradiction, derivation, analogy, supersession) draws on:

1. **Coherentism (BonJour, 1985; Thagard, 2000).** Knowledge is justified not by foundational axioms but by mutual coherence among beliefs. Thagard's ECHO model computes explanatory coherence using constraint satisfaction over a graph of propositions connected by explanation and contradiction relations. This is directly relevant — EMA's coherence graph is essentially a Thagard-style coherence network with richer edge types.

2. **Argumentation frameworks (Dung, 1995).** Abstract argumentation frameworks model arguments and attack relations. Preferred, stable, grounded, and complete extensions define different ways to resolve conflicts. The contradiction and support edges in EMA's coherence graph correspond to attack and support relations in bipolar argumentation frameworks (Cayrol & Lagasquie-Schiex, 2005).

3. **Truth Maintenance Systems (Doyle, 1979; de Kleer, 1986).** TMS tracks dependencies between beliefs and propagates revisions when beliefs change. JTMS (Justification-based TMS) and ATMS (Assumption-based TMS) are well-studied. EMA's derivation edges serve a similar function to JTMS justifications.

**The key distinction claimed — "knowledge circulates to where it's needed" vs. "knowledge is retrieved by query" — requires scrutiny:**

- **Push vs. pull knowledge delivery.** In a pull model (standard query), consumers request knowledge when they need it. In a push model (circulation), the system proactively delivers knowledge based on relevance signals. Push models exist: publish-subscribe systems (Eugster et al., 2003), recommendation engines, and active databases with triggers. The efficiency of push vs. pull depends on the ratio of (knowledge produced) to (knowledge consumed per consumer). If many consumers need the same knowledge, push is more efficient. If each consumer needs different knowledge, pull is more efficient.

- **"Guided by metabolic signals" is underspecified.** What determines where knowledge circulates? If it's relevance to active tasks, this is just a recommendation engine. If it's structural position in the coherence graph (e.g., contradictions are pushed to resolution agents, support edges are pushed to dependent claims), this is more like a constraint propagation system. The proposal must specify the circulation algorithm.

**How does this differ from a standard knowledge graph with inference?**

A knowledge graph (e.g., Neo4j with inference rules, or an RDF store with RDFS/OWL reasoning) has:
- Typed edges (similar to support, derivation)
- Inference rules (similar to analogy, derivation propagation)
- Query capabilities
- Some systems support triggers (similar to push-based circulation)

The meaningful distinction, if any, is:
1. **Metabolic edge dynamics.** EMA edges have metabolic properties — they weaken with disuse, strengthen with confirmation, and can be catabolized. Standard knowledge graphs have static edges unless explicitly updated. This is a real difference, analogous to Hebbian learning ("neurons that fire together wire together").
2. **Contradiction as first-class type.** Most knowledge graphs treat contradictions as errors to be resolved. EMA treats contradiction as a normal metabolic state — the system can hold contradictory knowledge and use metabolic processes to resolve it over time. This is similar to paraconsistent logic (da Costa, 1974) and defeasible reasoning (Nute, 1994).
3. **Supersession.** The explicit modeling of knowledge replacement (A supersedes B) is not standard in knowledge graphs but is present in version control systems and temporal databases.

**Assessment:** The coherence graph is a real extension beyond standard knowledge graphs, but the "circulatory system" framing overstates the novelty. The most valuable features — dynamic edge weights, first-class contradiction, supersession — can be described without the circulatory metaphor and would benefit from formal specifications independent of it.

#### B. Empirical Evidence

**Existence proofs:**
- Thagard's ECHO: demonstrates coherence-based reasoning over modest-scale networks (tens to hundreds of propositions). No evidence of scaling to thousands or millions.
- TMS systems: scale to thousands of propositions in practice but become slow with dense dependency graphs.
- Knowledge graphs in industry (Google, Amazon, LinkedIn): scale to billions of edges but with simple edge types and no coherence computation.
- Publish-subscribe systems (Kafka, Pulsar): demonstrate push-based information delivery at massive scale, but without semantic coherence computation.

**No existence proofs for:** A knowledge graph with dynamic edge weights, coherence-based circulation, and metabolic regulation operating at the scale required for a multi-agent AI system.

**Falsification experiments:**
1. Compare knowledge delivery effectiveness: build a coherence graph with push-based circulation and a standard knowledge graph with pull-based queries. Measure: time-to-relevant-knowledge for agents performing tasks. If pull-based retrieval with a good query mechanism matches or outperforms push-based circulation, the circulatory model does not justify its complexity.
2. Test contradiction resolution: insert 50 contradictions into the coherence graph and measure how many are detected and resolved by metabolic processes vs. requiring explicit intervention. If < 30% are resolved automatically, the claim that contradiction handling is "continuous metabolic activity" is not substantiated.

---

### Claim 6: Knowledge Catabolism

**Soundness: SOUND**

#### A. Theoretical Soundness

Knowledge catabolism — controlled dissolution of knowledge that has lost coherence or relevance, with recycling of components — is the best-grounded claim in the proposal.

1. **Information lifecycle management (ILM).** Enterprise data management has long recognized that data has a lifecycle: creation, active use, archival, and destruction (Tannenbaum, 2001). Retention policies, data classification, and automated archival are standard practice. Catabolism is ILM with semantic awareness.

2. **Garbage collection (GC).** Tracing GC (mark-and-sweep, Jones & Lins, 1996) identifies unreachable objects and reclaims their memory. Catabolism identifies "unreachable" or "low-coherence" knowledge and reclaims representational capacity. The analogy is precise:
   - Mark phase = coherence assessment (which quanta are still referenced/supported?)
   - Sweep phase = catabolism (dissolve unreferenced quanta)
   - Compaction = knowledge consolidation (merge remaining fragments)

3. **Forgetting in machine learning.** Catastrophic forgetting (McCloskey & Cohen, 1989; French, 1999) is a well-studied problem — neural networks forget old knowledge when learning new. Elastic Weight Consolidation (Kirkpatrick et al., 2017) and progressive neural networks (Rusu et al., 2016) address this. EMA's catabolism is *intentional* forgetting — removing knowledge that should be forgotten — which is the complement of the continual learning problem.

4. **Controlled demolition.** The key innovation is *recycling*: when a knowledge quantum is catabolized, its constituent evidence is redistributed to other quanta that can use it, and its provenance is preserved in a dissolution record. This is analogous to organ donation — the body dies but the organs live on. This is well-motivated: evidence that supported a now-invalid conclusion may still support other conclusions.

**Reversibility concern:** The question asks whether catabolism is reversible if the system makes a mistake. This depends on implementation:

- **Full reversibility** (undo catabolism, reconstruct the original quantum): Requires the dissolution record to contain enough information to reconstruct the quantum. This is achievable if the dissolution record stores the full quantum content (essentially a "recycle bin"). Storage cost: O(total catabolized content).
- **Partial reversibility** (recover constituent evidence but not the quantum's structure): Requires only that evidence redistribution is traceable. Less storage-intensive but cannot reconstruct the original synthesis.
- **Irreversibility** (catabolized content is gone): Unacceptable for a safety-critical system. The proposal must specify which level of reversibility is provided.

**Safety guarantees should include:**
- Quarantine period before final dissolution (analogous to "trash" in file systems)
- Quorum or threshold requirements (e.g., catabolism of a quantum supported by >3 other quanta requires confirmation)
- Immune check (sub-claim 4e): verify the quantum is genuinely invalid, not just temporarily low-coherence
- Dissolution audit log (provenance preservation)

#### B. Empirical Evidence

**Existence proofs:**
- Git: version control provides full reversibility of deletions through history
- Database soft-deletion: marking records as deleted without physical removal
- Email trash/archive: quarantine period before permanent deletion
- Biological apoptosis: programmed cell death with recycling of cellular components
- Wikipedia deletion: articles are not destroyed but moved to a deletion log with full content preserved

**These are strong existence proofs** — the pattern of "controlled deletion with recycling and reversibility" is well-established in both biology and engineering.

**Falsification experiments:**
1. Operate the system with and without catabolism for an extended period (simulated time). Measure knowledge graph size, query performance, and answer quality. Without catabolism, the graph should grow unboundedly and query performance should degrade. With catabolism, both should stabilize. If catabolism does not improve answer quality while controlling graph size, the mechanism is unnecessary.
2. Test error recovery: deliberately catabolize 10 valid quanta and attempt recovery. Measure recovery fidelity (semantic similarity to original) and time. If recovery fidelity < 0.9 or recovery is not possible within quarantine period, the safety guarantee is insufficient.

---

## 2. Cross-Claim Coherence Assessment

### 2.1 Internal Consistency

The six claims form a coherent narrative: epistemic quanta (Claim 2) are the substrate that undergoes metabolic processing (Claim 1); the coherence graph (Claim 5) is the medium through which quanta circulate; dreaming (Claim 3) is the anabolic process; catabolism (Claim 6) is the catabolic process; and SHREC (Claim 4) regulates all of it.

**Coherence strengths:**
- The metabolic metaphor provides a unified vocabulary for describing knowledge lifecycle operations that would otherwise be ad hoc (decay, consolidation, elimination, circulation).
- SHREC regulation naturally connects to all other components — ingestion rate (Claim 1), circulation priority (Claim 5), consolidation scheduling (Claim 3), and catabolism threshold (Claim 6).
- The coherence graph (Claim 5) provides the substrate that SHREC (Claim 4) monitors and that catabolism (Claim 6) operates on.

**Coherence weaknesses:**
1. **Claim 2 (projection) is somewhat orthogonal.** Multi-ontology projection is about interoperability with external subsystems (C3/C4/C5), not about internal metabolism. It could be removed or added without affecting the metabolic architecture. This suggests it is a separate concern that has been folded into the metabolic narrative for aesthetic rather than structural reasons.

2. **Claim 3 (dreaming) depends on Claim 4 (SHREC) for scheduling, but SHREC has no model of dreaming cost.** Dreaming consolidation is the most expensive metabolic process (it requires LLM inference). If SHREC treats it as just another budget competitor, the dreaming cycle may be starved by cheaper processes (ingestion, catabolism). The system needs a "basal metabolic rate" concept — a minimum guaranteed allocation for each process — which is not obviously part of the Lotka-Volterra competition model (where a weak competitor goes extinct).

3. **Tension between Claim 5 (push-based circulation) and Claim 2 (projection).** If knowledge circulates proactively, it must be projected into the recipient's ontological frame at delivery time. This means projection is not a one-time operation but a continuous cost proportional to circulation volume. The proposal must account for this in the SHREC budget model.

4. **Claim 6 (catabolism) and Claim 3 (dreaming) can conflict.** Dreaming may discover value in knowledge that catabolism has marked for elimination. The temporal ordering matters: does the dreaming cycle see knowledge that is in the catabolism queue? If yes, dreaming may "rescue" doomed knowledge. If no, the system may catabolize knowledge that dreaming would have found valuable. This needs explicit specification.

### 2.2 Cross-Claim Rating

**Cross-claim coherence: MOSTLY_COHERENT** — The claims form a plausible system but have unresolved interactions (dreaming/catabolism ordering, projection cost in circulation, competitive exclusion of expensive processes).

---

## 3. Key Scientific Gaps

### Gap 1: Formal Definition of Epistemic Quantum
The proposal does not provide a formal definition of what an epistemic quantum *is*. Without this, claims about projection, circulation, and catabolism are informal. Is it a proposition? A structured argument? A claim with evidence and confidence? A point in a vector space? The formal properties of the system depend entirely on this definition.

**Severity: HIGH** — This is foundational. Without it, the architecture cannot be formally analyzed.

### Gap 2: Information-Theoretic Analysis of Projection
No analysis of what information is preserved or lost during projection between ontological frames. Without this, the "without translation loss" claim is unsubstantiated.

**Severity: HIGH** — This determines whether Claim 2 is achievable or requires weakening.

### Gap 3: LLM Consolidation Reliability
No evidence or analysis of LLM reliability for cross-domain pattern discovery. The hallucination rate of consolidation determines whether dreaming is beneficial or harmful.

**Severity: HIGH** — This determines whether Claim 3 is safe to implement.

### Gap 4: SHREC Stability Analysis
No formal stability analysis of the combined ecological + PID control system. Interactions between the two control layers could produce oscillation, deadlock, or competitive exclusion.

**Severity: MEDIUM-HIGH** — The system may work in practice (many control systems work without formal stability proofs) but failures could be difficult to diagnose.

### Gap 5: Competitive Exclusion in Budget Competition
The Lotka-Volterra analogy predicts that with a single limiting resource, only one signal should dominate. The proposal must explain how all four SHREC signals coexist.

**Severity: MEDIUM** — This may be solvable (multiple resources, frequency-dependent selection) but needs explicit treatment.

### Gap 6: Scale Characterization
At what scale (number of quanta, number of agents, rate of ingestion) do the metabolic dynamics become meaningful? For small systems (100 quanta), standard knowledge management may suffice. For large systems (1M quanta), the overhead of metabolic regulation must be justified.

**Severity: MEDIUM** — Determines the practical utility of the architecture.

### Gap 7: Catabolism Reversibility Specification
The level of reversibility (full, partial, irreversible) is not specified. This is a critical safety property.

**Severity: MEDIUM** — Straightforward to specify but must be done before implementation.

---

## 4. Proposed Experiments

### Experiment 1: Metabolic Advantage Test
**Objective:** Determine whether the metabolic architecture outperforms a non-metabolic baseline.
**Design:** Implement two knowledge management systems — EMA (metabolic) and a baseline (standard knowledge graph with TTL expiry, periodic re-indexing, and query-based retrieval). Populate both with the same stream of knowledge claims over simulated time (10,000 claims, including 10% contradictions, 5% supersessions, 20% that become stale). Measure:
- Retrieval precision/recall at t = 1000, 5000, 10000
- Storage growth rate
- Staleness rate (fraction of active knowledge that is outdated)
- Contradiction resolution rate
**Success criterion:** EMA outperforms baseline on >= 3 of 4 metrics.
**Estimated effort:** 4-6 weeks.

### Experiment 2: Projection Fidelity Test
**Objective:** Quantify information loss in multi-ontology projection.
**Design:** Define 50 epistemic quanta spanning different claim types. Implement projection functions for 3 ontological frames (C3-coordination, C4-semantic, C5-verification). For each quantum, compute: (a) forward projection fidelity, (b) round-trip fidelity (project and back), (c) cross-frame consistency (project to A, then to B vs. project directly to B).
**Success criterion:** Mean round-trip fidelity > 0.85 for all frame pairs. Cross-frame consistency > 0.90.
**Estimated effort:** 2-3 weeks.

### Experiment 3: Dreaming Precision Test
**Objective:** Measure the reliability of LLM-based knowledge consolidation.
**Design:** Curate 200 claims from 5 domains with 20 known cross-domain patterns (ground truth established by domain experts). Run dreaming consolidation 5 times. Measure: precision, recall, hallucination rate, inter-run consistency.
**Success criterion:** Precision > 0.6, recall > 0.3, hallucination rate < 0.15, inter-run Jaccard > 0.5.
**Kill criterion:** Hallucination rate > 0.3 or precision < 0.4 (dreaming produces more noise than signal).
**Estimated effort:** 3-4 weeks.

### Experiment 4: SHREC Stability Test
**Objective:** Verify that the combined ecological + PID system is stable under normal and perturbed conditions.
**Design:** Simulate SHREC dynamics over 1000 epochs with: (a) steady-state input, (b) sudden 5x input spike, (c) sudden loss of 30% of knowledge base, (d) gradual domain shift. Measure: signal convergence time, overshoot magnitude, oscillation frequency, competitive exclusion (does any signal go to zero?).
**Success criterion:** All signals remain positive (no competitive exclusion). Settling time < 50 epochs after perturbation. No sustained oscillation.
**Estimated effort:** 2-3 weeks.

### Experiment 5: Catabolism Safety Test
**Objective:** Verify that catabolism is safely reversible and does not destroy valuable knowledge.
**Design:** Operate the system for 500 epochs, allowing catabolism to run naturally. Then: (a) identify 20 catabolized quanta, (b) attempt recovery from dissolution records, (c) evaluate whether any catabolized quanta were subsequently needed. Measure: recovery fidelity, false positive catabolism rate (valuable knowledge destroyed), storage overhead of dissolution records.
**Success criterion:** Recovery fidelity > 0.95. False positive catabolism rate < 5%. Dissolution record overhead < 30% of active storage.
**Estimated effort:** 2-3 weeks.

---

## 5. Recommended Mitigations

### Mitigation 1: Formalize the Epistemic Quantum
Define the epistemic quantum as a formal structure: (claim: string, evidence: set[reference], confidence: [0,1], provenance: lineage, coherence_edges: set[typed_edge], metabolic_state: enum, created_at: timestamp, last_circulated: timestamp). This makes all other claims testable.

### Mitigation 2: Weaken the Projection Claim
Replace "without translation loss" with "with bounded, measurable translation loss." Define a fidelity metric and specify minimum fidelity thresholds for each frame pair. Accept that some information exists only in certain frames.

### Mitigation 3: Gate Dreaming Output Through Verification
Do not inject dreaming consolidation outputs directly into the knowledge base. Instead, treat them as hypotheses that must pass through the C5 PCVM verification membrane before integration. This turns the hallucination risk from a system-level threat into a quality control problem.

### Mitigation 4: Ensure Multi-Resource Budget
Design the SHREC budget to have at least 4 independent resource dimensions (e.g., CPU cycles, LLM inference tokens, storage I/O, graph traversal operations). This provides the niche differentiation needed to prevent competitive exclusion in the Lotka-Volterra dynamics.

### Mitigation 5: Specify Catabolism Reversibility as Quarantine-Then-Dissolve
Implement a two-phase catabolism: (1) quarantine — quantum is removed from active circulation but fully preserved, retrievable for a configurable period (default: 100 epochs); (2) dissolution — after quarantine, the quantum is dissolved with components recycled and provenance archived. Allow manual rescue from quarantine.

### Mitigation 6: Add Metabolic Health Metrics
Define concrete, measurable health metrics that the metabolic framing predicts: (a) metabolic rate = quanta processed per epoch, (b) metabolic efficiency = value generated per quantum processed, (c) metabolic balance = ratio of anabolism to catabolism, (d) circulatory health = mean time-to-relevant-delivery. If these metrics are not predictive of system performance, the metabolic framing is not earning its keep.

### Mitigation 7: Formal Stability Analysis for SHREC
Before implementation, conduct a linearized stability analysis of the combined ecological + PID system around the intended operating point. Compute eigenvalues of the Jacobian. If any have positive real parts, the system is locally unstable and requires re-tuning. Use Lyapunov functions for global stability guarantees if possible.

---

## 6. Overall Assessment

| Claim | Rating | Confidence |
|---|---|---|
| 1. Knowledge as Metabolic Process | PARTIALLY_SOUND | Medium |
| 2. Epistemic Quanta with Multi-Ontology Projection | PARTIALLY_SOUND | Medium-High |
| 3. Dreaming Consolidation | PARTIALLY_SOUND | Medium-Low |
| 4. SHREC Regulatory System (overall) | PARTIALLY_SOUND | Medium |
| 4a. Budget Competition / Lotka-Volterra | PARTIALLY_SOUND | Medium |
| 4b. Sigma-Derived PID Gains | PARTIALLY_SOUND | Medium |
| 4c. Bayesian Priors for Cold Start | SOUND | High |
| 4d. Change-Point Detection | SOUND | High |
| 4e. Immune Self-Audit | PARTIALLY_SOUND | Medium-Low |
| 5. Coherence Graph as Circulatory System | PARTIALLY_SOUND | Medium |
| 6. Knowledge Catabolism | SOUND | High |
| **Cross-Claim Coherence** | **MOSTLY_COHERENT** | Medium |

**Overall Soundness Score: 3.0 / 5**

The Epistemic Metabolism Architecture is a creative and ambitious design that synthesizes legitimate theoretical traditions (autopoiesis, coherentism, control theory, information lifecycle management, garbage collection) into a unified architectural vision. The metabolic framing is generative — it produces architectural features (decay, consolidation, circulation, regulation) that are individually well-motivated. However, the framing remains more metaphorical than formal: it does not make quantitative predictions that distinguish it from alternative architectures, and several claims (projection losslessness, dreaming reliability, Lotka-Volterra applicability) require weakening or additional formal work.

The strongest components are knowledge catabolism (Claim 6: well-grounded, clearly implementable, addresses a real problem) and the SHREC regulatory primitives (Bayesian priors, change-point detection: standard, well-established). The weakest component is dreaming consolidation (Claim 3: dependent on unproven LLM capabilities, highest risk of producing harm through hallucination).

The architecture is viable if: (a) the epistemic quantum is formally defined, (b) the projection claim is weakened to "bounded loss," (c) dreaming output is gated through verification, (d) SHREC stability is formally analyzed, and (e) catabolism reversibility is explicitly specified. With these mitigations, the architecture would merit a score of 3.5-4.0 / 5.

---

*Assessment conducted under Atrahasis Agent System v2.0 protocol. All theoretical references are to published, peer-reviewed work or established textbooks. No empirical claims are made without citing existence proofs or noting their absence.*
