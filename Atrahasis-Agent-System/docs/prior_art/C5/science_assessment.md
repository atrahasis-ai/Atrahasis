# Science Assessment — C5 Proof-Carrying Verification Membrane (PCVM)

**Assessor:** Science Advisor
**Invention:** C5 — Proof-Carrying Verification Membrane
**Date:** 2026-03-09
**Protocol:** Atrahasis Agent System v2.0

---

## Executive Summary

C5 proposes replacing replication-based consensus verification (Verichain) with a proof-carrying architecture where every agent output carries a Verification Trace Document (VTD) that the membrane checks instead of re-executing computation. The architecture draws on proof-carrying code (PCC), Bayesian epistemology, Popperian falsificationism, and foundationalist epistemology, composing them into a six-component verification system.

After assessment, the architecture is **PARTIALLY_SOUND** overall. The individual theoretical inspirations are well-grounded, but the central adaptation — extending PCC from deterministic programs to stochastic AI agent outputs — requires substantial theoretical work that the current proposal does not provide. The 8-class claim taxonomy is well-motivated but ad hoc. Adversarial probing is epistemically well-founded. Constitutional grounding is philosophically defensible but incomplete. Continuous re-verification is sound in principle but underspecified in its composition algebra.

The claims cohere as a system at the architectural level but have gaps at the formal level: no proof theory is defined for non-deterministic claim classes, no composition algebra is specified for credibility gradients, and the computational cost model for proof-checking LLM outputs is unsubstantiated.

**Overall Soundness Score: 3.2 / 5** — Promising architectural vision grounded in real theory, but with critical formal gaps that must be resolved before the architecture can deliver its claimed benefits.

---

## 1. Per-Claim Assessments

### Claim 1: VTD Proof-Carrying Model — Verification Cost Drops from O(replication) to O(proof-checking)

**Soundness: PARTIALLY_SOUND**

#### A. Theoretical Soundness

The claim is inspired by Proof-Carrying Code (PCC), introduced by Necula (1997). In PCC, a code producer generates a formal proof that the code satisfies a safety policy, and the consumer checks the proof rather than re-analyzing the code. The key theorem: proof-checking is O(n) in the proof size, while generating the proof (or independently verifying the code) may be exponentially harder. This is well-established for type safety, memory safety, and control-flow integrity of deterministic programs.

The theoretical grounding is strong for the *principle* — checking a proof is generally cheaper than constructing one or re-executing the computation. This asymmetry is fundamental to complexity theory (P vs NP: verifying a solution is in P while finding it may be in NP). It also appears in interactive proof systems (Babai 1985, Goldwasser-Micali-Rackoff 1989) and probabilistically checkable proofs (PCP theorem, Arora-Safra 1998).

**However**, the adaptation to AI agent outputs faces a fundamental category mismatch:

1. **PCC requires formal specifications.** In classical PCC, the safety policy is a formal predicate (e.g., "this program never dereferences a null pointer"). For AI agent outputs, what is the formal specification? "This research summary accurately reflects the source material" is not a formal predicate — it requires semantic judgment that is itself an AI-complete problem.

2. **PCC proofs are in decidable logics.** PCC typically uses first-order logic or type theory where proof-checking is decidable. Proofs about the quality of natural language reasoning are not in any decidable formal system.

3. **The O(proof-checking) claim is meaningful only relative to a defined proof system.** Without specifying what logic the VTD proofs are written in, the complexity claim is vacuous. If "proof-checking" means "an LLM reads the VTD and judges whether it's convincing," then proof-checking cost is O(LLM inference), which may not be cheaper than the original computation.

**Known counterexamples:** The Curry-Howard correspondence tells us that proofs and programs are isomorphic in certain type theories. For complex programs, the proof can be as large as the program itself — there is no free lunch in general. The PCC efficiency gain comes specifically from the asymmetry between *safety properties* (simple to state, hard to verify from scratch, easy to check given a proof) and *arbitrary functional properties* (where proofs may not be shorter than re-execution).

**Assumptions:** (a) That meaningful formal specifications can be written for AI agent outputs; (b) that proofs in whatever system is chosen are substantially cheaper to check than to generate or re-execute; (c) that VTD construction cost does not negate the verification savings.

#### B. Empirical Evidence

**Existence proofs for the principle:**
- PCC in compilers: Foundational Proof-Carrying Code (Appel 2001) demonstrates practical PCC for machine code safety.
- Certifying compilation (CompCert, Leroy 2009): the compiler produces a proof of semantic preservation that is machine-checkable.
- Zero-knowledge proofs in blockchain (zk-SNARKs, zk-STARKs): verification is O(1) or O(log n) regardless of computation complexity. However, proof generation is expensive (often 1000x the original computation).
- Verified AI systems: VNN-COMP (Verification of Neural Network Competition) verifies properties of neural networks, but only simple properties (robustness to perturbation) of small networks, and verification times are measured in hours.

**No existence proofs for:** Proof-carrying verification of natural language reasoning, creative outputs, or stochastic multi-step agent workflows.

**Falsification experiments:**
1. Define 5 representative agent outputs (research summary, architecture proposal, risk assessment, code review, claim with evidence chain).
2. For each, attempt to construct a VTD that is (a) machine-checkable, (b) substantially cheaper to check than to re-generate the output, and (c) meaningful (catches real errors).
3. Measure: VTD construction time, VTD checking time, original computation time. If checking time >= 0.5 * computation time for most outputs, the sublinear claim is falsified for practical purposes.

---

### Claim 2: 8-Class Claim Taxonomy (D/E/S/H/N/P/R/C)

**Soundness: PARTIALLY_SOUND**

#### A. Theoretical Soundness

The idea that different types of claims require different types of verification is well-established across multiple disciplines:

- **Philosophy of science:** The Vienna Circle distinguished analytic (logical/mathematical) from synthetic (empirical) propositions. Popper distinguished falsifiable from non-falsifiable claims. Hempel's confirmation theory treats statistical hypotheses differently from universal generalizations.
- **Software verification:** The verification community distinguishes safety properties (nothing bad happens) from liveness properties (something good eventually happens) — different proof obligations arise for each (Alpern & Schneider 1985).
- **Argumentation theory:** Toulmin's model (1958) distinguishes claims, grounds, warrants, backing, qualifiers, and rebuttals — each requiring different justification standards.

The specific 8 classes map roughly to recognized epistemic categories:

| Class | Epistemic Analogue | Verification Tradition |
|---|---|---|
| Deterministic | Analytic/deductive | Formal verification, type checking |
| Empirical | Synthetic a posteriori | Experimental science, observation |
| Statistical | Probabilistic inference | Hypothesis testing, confidence intervals |
| Heuristic | Practical judgment | Expert evaluation, benchmarking |
| Normative | Value claims | Ethics, policy analysis (no truth-apt verification) |
| Process | Procedural compliance | Audit, conformance testing |
| Reasoning | Logical inference | Argument validity checking |
| Compliance | Regulatory conformance | Compliance auditing |

**Limitations:**

1. **The taxonomy is ad hoc, not derived from a principled theory.** There is no proof that these 8 classes are complete (exhaustive) or that they are the right decomposition. Alternative taxonomies exist:
   - Habermas's validity claims: truth, rightness, truthfulness, comprehensibility (4 types)
   - Speech act theory: assertives, directives, commissives, expressives, declaratives (5 types, Searle 1975)
   - Argument schemes (Walton, Reed, Macagno 2008): 60+ identified argument schemes

2. **The classes are not mutually exclusive.** A claim like "this algorithm runs in O(n log n) on average" is simultaneously Deterministic (the algorithm's correctness), Statistical (the average-case analysis), and Empirical (if the O(n log n) bound was determined experimentally). The taxonomy needs explicit rules for multi-class claims.

3. **Normative claims lack truth-apt verification.** The taxonomy includes "Normative" claims, but normative claims ("we should prefer privacy over efficiency") are not truth-apt in the classical sense. What does verification mean for a normative claim? The proposal must address whether normative claims are verified for *consistency* (with constitutional values), *coherence* (with other normative commitments), or *acceptance* (by relevant stakeholders) — these are fundamentally different operations.

4. **Potential missing classes:**
   - **Predictive claims** — assertions about future states (not purely Statistical, not purely Empirical)
   - **Definitional claims** — stipulative definitions that create rather than describe reality
   - **Meta-claims** — claims about the verification process itself (self-referential)
   - **Comparative claims** — "X is better than Y" (combines Empirical, Statistical, and Normative elements)

**Assumptions:** (a) That claim types can be reliably classified by an AI agent; (b) that the classification is stable (a claim does not change class depending on context); (c) that the proof obligations for each class are well-defined.

#### B. Empirical Evidence

No direct empirical evidence exists for this specific taxonomy. Indirect evidence:

- **Argument mining** research (Stede & Schneider 2018; Lawrence & Reed 2019) demonstrates that argument classification can be automated with moderate accuracy (F1 ~0.65-0.80 for coarse-grained classification). This suggests claim classification is feasible but error-prone.
- **Audit frameworks** in compliance (SOX, ISO 27001) use claim-type-specific verification procedures, validating the principle that different claims need different checks.

**Falsification experiment:**
1. Generate 200 representative agent claims across a variety of invention tasks.
2. Have 3 independent annotators classify each into the 8 categories.
3. Measure inter-annotator agreement (Fleiss' kappa). If kappa < 0.6, the taxonomy is too ambiguous for reliable automated classification.
4. Identify claims that annotators cannot classify or that receive 3+ different labels — these reveal taxonomy gaps.

---

### Claim 3: Adversarial Probing Is Epistemically Stronger Than Confirmatory Verification

**Soundness: SOUND**

#### A. Theoretical Soundness

This claim has the strongest theoretical foundation of all six claims. It rests on multiple convergent traditions:

1. **Popper's falsificationism (1934/1959).** Scientific claims gain credibility not from confirmation but from surviving attempts at refutation. A theory that has withstood severe tests is more corroborated than one tested only with friendly evidence. This is the core of critical rationalism.

2. **Confirmation theory asymmetry.** In Bayesian epistemology, the evidential impact of a disconfirming observation is typically larger than that of a confirming one, particularly for well-supported hypotheses. If P(H) is already high, another confirming observation increases P(H|E) marginally, but a single disconfirming observation can drastically reduce it. This is formalized in the likelihood ratio framework: strong disconfirmation (low P(E|H)/P(E|not-H)) moves the posterior more than weak confirmation.

3. **Software testing theory.** Dijkstra's dictum: "Testing shows the presence, not the absence, of bugs." Mutation testing, fuzz testing, and adversarial testing are all grounded in the principle that actively seeking failures is more informative than passively confirming success. The empirical software engineering literature consistently finds that adversarial testing (e.g., property-based testing, fuzzing) finds more defects per test-hour than example-based testing (Claessen & Hughes 2000, AFL fuzz testing results).

4. **Red-teaming in AI safety.** Recent work on LLM red-teaming (Perez et al. 2022, Anthropic's Constitutional AI) demonstrates that adversarial probing of AI outputs reveals failure modes that standard evaluation misses. This is direct empirical precedent for PCVM's adversarial probing concept.

5. **Dialectical argumentation.** The Pragma-Dialectical theory of argumentation (van Eemeren & Grootendorst 1984, 2004) holds that the quality of an argument is best assessed through critical discussion — structured adversarial exchange. This tradition directly supports the idea that claims should be subjected to counterargument, not merely checked for internal consistency.

**Limitations:**

1. **Adversarial probing has diminishing returns.** After the obvious attacks have been tried, each additional adversarial probe is less likely to find a flaw. The marginal value of the Nth adversarial probe decreases. The architecture needs a stopping criterion.

2. **Adversarial quality depends on adversary quality.** A weak adversary provides weak assurance. If the adversarial probes are generated by the same class of LLM that generated the original claim, there is a risk of shared blind spots (both models fail on the same edge cases because they share training data biases). True adversarial strength requires *diverse* adversarial strategies.

3. **Not all claim types benefit equally.** Adversarial probing is highly effective for Deterministic and Reasoning claims (counterexamples are decisive) but less effective for Normative claims (disagreement is expected, not a "flaw") and Statistical claims (where individual counterexamples are consistent with the statistical claim).

**Assumptions:** (a) That effective adversarial probes can be automatically generated; (b) that the adversary has sufficient capability to find real flaws (not just surface-level objections); (c) that adversarial results can be correctly interpreted (distinguishing genuine flaws from misunderstandings).

#### B. Empirical Evidence

Strong empirical support:
- Fuzz testing finds 10-100x more bugs per CPU-hour than unit testing (Bohme et al. 2017, AFL benchmarks).
- LLM red-teaming reveals failure modes not found by standard benchmarks (Perez et al. 2022).
- Adversarial NLI datasets (Nie et al. 2020, ANLI) demonstrate that adversarially constructed examples are harder and more informative than naturally collected ones.

**Falsification experiment:**
1. Take 100 agent claims (mix of correct and subtly flawed).
2. Apply (a) confirmatory checking (re-generate and compare), (b) adversarial probing (attempt to construct counterexamples).
3. Measure precision, recall, and F1 for flaw detection under each strategy.
4. If adversarial probing does not achieve higher recall than confirmatory checking, the claim is falsified.

---

### Claim 4: Process Verification via VTDs — Verifying "How" and "Why," Not Just "What"

**Soundness: SOUND**

#### A. Theoretical Soundness

Process verification is a well-established concept across multiple domains:

1. **Audit trails and compliance.** SOX Section 404, ISO 9001, and GxP regulations all require process verification — demonstrating that the correct procedures were followed, not merely that the output looks acceptable. This is because correct outputs can arise from incorrect processes (lucky outcomes), and incorrect processes will eventually produce incorrect outputs. Process verification addresses the *base rate* of correctness, not individual instances.

2. **Provenance in scientific computing.** The W3C PROV standard (Moreau & Missier 2013) and its extensions (ProvONE for scientific workflows, PROV-AGENT for AI agents) capture process provenance — which activities produced which entities, using which inputs, attributed to which agents. This is precisely the "how and why" that VTDs aim to encode.

3. **Certified computation.** In verified compilation (CompCert), the compiler produces not just correct output but a certificate that the compilation process preserved semantics. The certificate captures process conformance, not just output correctness.

4. **Constitutional AI alignment.** Anthropic's Constitutional AI (Bai et al. 2022) verifies that LLM outputs conform to a set of principles (the "constitution"). This is process verification — checking that the generation process respected constraints, not just that the output looks acceptable.

**The claim that process verification is complementary to output verification is uncontroversial in the verification literature.** The combination of "what" (output correctness) and "how" (process conformance) provides defense in depth: an output that is correct *and* was produced by a verified process is more trustworthy than one that merely appears correct.

**Limitations:**

1. **Process verification for LLM agents is underspecified.** What does it mean for an LLM to have "followed the right process"? LLMs do not have inspectable intermediate states in the way that traditional programs do. The "process" for an LLM is a forward pass through billions of parameters — this is not auditable. VTDs would need to capture *externally observable* process markers (which tools were called, which sources were consulted, which roles were invoked) rather than internal reasoning processes.

2. **Process conformance does not guarantee output correctness.** A process can be followed perfectly and still produce incorrect output (garbage in, garbage out; or the process itself is flawed). Process verification is necessary but not sufficient.

3. **Goodhart's Law risk.** If agents are evaluated on process conformance, they may optimize for *appearing* to follow the process (producing convincing VTDs) rather than actually doing good work. This is the same problem that plagues checkbox compliance in human organizations.

**Assumptions:** (a) That meaningful process markers can be captured for AI agent workflows; (b) that process conformance is correlated with output quality; (c) that VTD construction is not so burdensome that it degrades agent performance.

#### B. Empirical Evidence

- W3C PROV is deployed in scientific workflows (Taverna, Kepler, VisTrails) and has demonstrated value for reproducibility and trust.
- Audit trail requirements in regulated industries (finance, healthcare, aviation) provide decades of evidence that process verification improves system reliability.
- PROV-AGENT (Souza et al. 2025) specifically demonstrates provenance capture for AI agent workflows.

No falsification experiment needed for the basic principle. The open question is implementation feasibility for LLM-based agents, addressed under Claim 1.

---

### Claim 5: Constitutional Grounding Resolves the Verifier Regress

**Soundness: PARTIALLY_SOUND**

#### A. Theoretical Soundness

The "who verifies the verifier" problem is a specific instance of Agrippa's trilemma (also known as Munchhausen's trilemma), identified in ancient skepticism and formalized by Hans Albert (1968). The trilemma states that any attempt to justify a belief leads to one of three outcomes:

1. **Infinite regress** — each justification requires further justification, ad infinitum.
2. **Circularity** — the chain of justification loops back to the original belief.
3. **Dogmatism (foundationalism)** — the chain terminates at an unjustified axiom accepted as self-evident.

PCVM's constitutional grounding explicitly chooses option 3: foundationalism. The constitutional parameters are axiomatic — they are not justified by further verification but accepted as the trust foundation. This is a legitimate and well-studied philosophical position.

**Precedents for foundationalism in formal systems:**

- **Axiomatic mathematics.** ZFC set theory terminates justification at axioms (extensionality, regularity, choice, etc.) that are accepted without proof. This has been the foundation of mathematics since the early 20th century.
- **Root of trust in security.** Hardware security modules (HSMs), TPM chips, and certificate authority root certificates all implement foundationalism — a trusted component that is not itself verified but serves as the trust anchor for everything above it. This is the dominant architecture for computer security.
- **Constitutional law.** Legal systems ground interpretation in a constitution that is accepted as authoritative. Constitutional amendments exist but require supermajority processes — directly analogous to PCVM's G-class supermajority requirement.

**The philosophical position is defensible.** Foundationalism does not "solve" Munchhausen's trilemma in the philosophical sense — it chooses one horn of the trilemma deliberately. But this is what every practical system does. The question is not whether foundationalism is philosophically perfect but whether it is *adequate for the purpose.*

**Limitations:**

1. **"Who writes the constitution?" is merely deferred, not eliminated.** PCVM grounds verification in constitutional parameters, but these parameters were written by someone (the system designer, presumably). The trust ultimately rests on trust in the constitution's author. This is not a flaw per se — it is the same situation as legal constitutions, axiomatic mathematics, and hardware roots of trust — but the proposal should acknowledge it explicitly.

2. **Constitutional parameters may be incorrect.** If a constitutional parameter encodes a wrong value (e.g., an incorrect threshold, a flawed ethical principle), all verification bottoming out at that parameter inherits the error. The system needs a mechanism for *constitutional amendment* that does not undermine the stability that constitutional grounding provides. The G-class supermajority mechanism addresses this but creates a tension: too easy to amend and the foundation is unstable; too hard to amend and errors are permanent.

3. **Godel's incompleteness applies.** For any sufficiently expressive formal system, there exist true statements that cannot be proven within the system. If the constitutional parameters are formalized as axioms in a sufficiently expressive logic, there will be claims that are true but unprovable from the constitution. The system needs a graceful way to handle undecidable claims — neither verified nor falsified.

4. **The analogy to legal constitutions is imperfect.** Legal constitutions work because they are interpreted by human judges who exercise discretion. AI agents interpreting constitutional parameters lack this discretionary capacity (or if they have it, it reintroduces the verification problem at the interpretation layer).

**Assumptions:** (a) That constitutional parameters can be specified precisely enough to serve as verification axioms; (b) that the G-class supermajority mechanism provides adequate constitutional amendment without destabilizing the foundation; (c) that undecidable claims are rare enough not to undermine the system.

#### B. Empirical Evidence

- Hardware roots of trust (TPM, HSM) are deployed in billions of devices and provide practical foundationalism for security.
- Certificate authority systems ground internet security in ~150 root certificates that are trusted without further verification.
- Legal constitutions have grounded governance systems for centuries.
- Axiomatic mathematics has been productive for over a century despite Godel's results.

**Falsification experiment:**
1. Define a set of 50 constitutional parameters for the Atrahasis system.
2. Attempt to verify 200 representative agent claims by tracing each to its constitutional grounding.
3. Measure: (a) percentage of claims that can be traced to constitutional parameters, (b) percentage that bottom out at ambiguous interpretations, (c) percentage that reveal constitutional parameter conflicts.
4. If >20% of claims cannot be cleanly traced to constitutional grounding, the foundationalism claim is practically insufficient.

---

### Claim 6: Continuous Re-verification via Credibility Gradients

**Soundness: PARTIALLY_SOUND**

#### A. Theoretical Soundness

The claim that verification should be continuous rather than binary is well-grounded in Bayesian epistemology:

1. **Bayesian updating.** In Bayesian inference, beliefs are represented as probability distributions that are continuously updated as new evidence arrives (Bayes' theorem). A claim is never "finally verified" — its posterior probability changes with each new observation. This is the standard framework in statistics, machine learning, and decision theory.

2. **Credal sets.** When the prior distribution is uncertain, beliefs can be represented as sets of probability distributions (credal sets, Levi 1974; Walley 1991). This provides a formal framework for representing deep uncertainty about claim reliability. PCVM's credibility gradients could be formalized as credal sets.

3. **Belief revision.** The AGM theory of belief revision (Alchourron, Gardenfors, Makinson 1985) provides axioms for how rational agents should update their beliefs when receiving new information, including information that contradicts current beliefs. This provides a formal foundation for re-verification.

4. **Trust management systems.** Computational trust models (Josang's subjective logic 2016, Beth et al. 1994) represent trust as continuous values with uncertainty, updated through experience. This is a direct precedent for credibility gradients in multi-agent systems.

**The principle is sound. The implementation challenges are significant:**

1. **Credibility composition algebra.** If Claim C depends on Premises A and B, and A has credibility 0.8 and B has credibility 0.7, what is C's credibility? The answer depends on the dependency structure:
   - If C = A AND B (both required): credibility <= min(0.8, 0.7) = 0.7 (under independence: 0.8 * 0.7 = 0.56)
   - If C = A OR B (either sufficient): credibility >= max(0.8, 0.7) = 0.8 (under independence: 1 - (0.2 * 0.3) = 0.94)
   - If A and B are correlated: the answer depends on the correlation structure, which is generally unknown.

   The proposal does not specify this composition algebra. Without it, credibility gradients cannot propagate through reasoning chains. This is a **critical gap.**

2. **Decision thresholds.** Downstream systems inevitably need binary decisions (deploy or don't deploy; approve or reject; include or exclude). Credibility gradients must eventually be thresholded. The choice of threshold is itself a decision that the credibility framework does not determine. This does not invalidate the approach — it means the approach must be complemented by a decision-theoretic layer that converts credibilities to actions given utility functions.

3. **Credibility decay and staleness.** If claims are never finally verified, old claims accumulate. What is the credibility of a claim verified 6 months ago with no new evidence? It should decay, but at what rate? The proposal needs a temporal decay model. Exponential decay is the standard assumption but may not be appropriate for all claim types (Deterministic claims should not decay; Empirical claims in fast-moving domains should decay quickly).

4. **Computational cost of continuous re-verification.** If every claim in the system must be periodically re-verified, the verification cost grows linearly with the number of historical claims. Without a mechanism for "freezing" or "archiving" claims with sufficiently high credibility, the system faces unbounded verification overhead.

**Assumptions:** (a) That a composition algebra for credibility can be defined that is both tractable and faithful to the dependency structure; (b) that decision thresholds can be set in a principled way; (c) that the computational cost of continuous re-verification is manageable.

#### B. Empirical Evidence

- Bayesian updating is the foundation of modern machine learning (Bayesian neural networks, Gaussian processes, probabilistic programming).
- Josang's subjective logic has been deployed in trust management for IoT and multi-agent systems.
- Continuous monitoring systems in cybersecurity (SIEM, continuous compliance) demonstrate the operational feasibility of ongoing verification.

**Falsification experiment:**
1. Define a credibility composition algebra (choose one: probabilistic independence, Dempster-Shafer, subjective logic).
2. Build a dependency graph of 100 interconnected claims.
3. Propagate credibility updates through the graph when individual claim credibilities change.
4. Measure: (a) propagation time, (b) stability (does the system converge?), (c) sensitivity (does a small change in one claim's credibility cascade catastrophically?).
5. If propagation is unstable or takes longer than the re-verification interval, continuous re-verification is computationally infeasible.

---

## 2. Cross-Claim Coherence

**Verdict: PARTIALLY_COHERENT**

### How the Claims Work Together

The six claims form a layered architecture:

```
Layer 5: Continuous Re-verification (Claim 6) — temporal dimension
Layer 4: Adversarial Probing (Claim 3) — verification strength
Layer 3: Claim Taxonomy (Claim 2) — verification routing
Layer 2: VTD Proof-Carrying Model (Claim 1) + Process Verification (Claim 4) — verification mechanism
Layer 1: Constitutional Grounding (Claim 5) — trust foundation
```

This layering is architecturally coherent. Each layer addresses a different concern:
- Layer 1 answers: "What do we trust axiomatically?"
- Layer 2 answers: "How do we verify?"
- Layer 3 answers: "What type of verification is needed?"
- Layer 4 answers: "How do we ensure verification quality?"
- Layer 5 answers: "When do we re-verify?"

### Coherence Strengths

1. **The taxonomy (Claim 2) correctly parameterizes the proof model (Claim 1).** Different claim types requiring different proof obligations is the right architectural decision. A Deterministic claim can carry a formal proof; a Heuristic claim carries benchmark results; a Process claim carries an audit trail. This is a natural and well-motivated decomposition.

2. **Adversarial probing (Claim 3) complements proof-carrying verification (Claim 1).** Proofs demonstrate that a claim satisfies its specification; adversarial probing tests whether the specification is adequate. These are complementary — proofs check internal consistency while adversarial probing checks external validity.

3. **Constitutional grounding (Claim 5) provides a termination condition for verification chains.** Without it, the system would face infinite regress. With it, verification traces bottom out at accepted axioms. This is architecturally necessary.

### Coherence Gaps

1. **The proof-carrying model (Claim 1) is underspecified for non-Deterministic claim classes.** The taxonomy (Claim 2) identifies 8 claim types, but the proof model (Claim 1) only has clear proof obligations for Deterministic and Process claims. What is a "proof" for a Heuristic claim? For a Normative claim? The architecture claims that proof-carrying verification works for all 8 classes, but only 2-3 classes have well-defined proof theories. **This is the most critical coherence gap.**

2. **Credibility gradients (Claim 6) lack a composition algebra that connects to the taxonomy (Claim 2).** How does credibility composition differ for Deterministic claims (where proof validity is binary) vs. Statistical claims (where credibility is inherently probabilistic) vs. Normative claims (where "credibility" may not be meaningful)? The claims do not specify how the continuous verification model interacts with the typed claim system.

3. **Adversarial probing (Claim 3) cost model is unspecified relative to proof-checking (Claim 1).** If verification is supposed to be cheaper than re-execution, but adversarial probing requires generating multiple attack attempts (each of which may involve substantial computation), the total verification cost may exceed re-execution cost. The architecture needs a cost budget that allocates between proof-checking and adversarial probing.

4. **Process verification (Claim 4) and constitutional grounding (Claim 5) interact in underspecified ways.** If a VTD shows that the correct process was followed but the constitutional parameter defining "correct process" is later amended, what happens to claims verified under the old constitution? The architecture needs a versioning and migration story for constitutional changes.

---

## 3. Key Scientific Gaps

### Gap 1: No Proof Theory for Non-Deterministic Claims (CRITICAL)

The central claim of PCVM — that proof-carrying verification works for AI agent outputs — requires a proof theory for stochastic, creative, and non-reproducible outputs. No such theory exists. The proposal must either:

(a) **Define a new proof theory** for AI agent claims, specifying what constitutes a valid proof for each claim class. This is a substantial theoretical contribution that would itself require peer review.

(b) **Restrict the proof-carrying model to claim classes where proofs are well-defined** (Deterministic, Process, Compliance) and use a different verification mechanism (e.g., adversarial probing, peer review, statistical testing) for the remaining classes. This is more honest but reduces the scope of the proof-carrying claim.

(c) **Redefine "proof" as "structured evidence"** — a VTD is not a formal proof but a structured evidence package that makes verification easier, even if it does not reduce verification to mechanical proof-checking. This is pragmatically viable but weakens the complexity-theoretic claims.

### Gap 2: No Credibility Composition Algebra (HIGH)

Without a formal algebra for composing credibilities through dependency chains, the continuous re-verification claim is aspirational rather than operational. The proposal needs to specify:
- How credibilities compose under logical conjunction, disjunction, and implication
- How credibilities compose under uncertain dependency (when correlation is unknown)
- How credibility decay is modeled for different claim types
- Convergence guarantees for credibility propagation in cyclic dependency graphs

Candidate frameworks: Dempster-Shafer theory, Josang's subjective logic, Pearl's causal calculus, or a novel algebra purpose-built for the system. Each has trade-offs in expressiveness, tractability, and faithfulness.

### Gap 3: Computational Cost Model (HIGH)

The proposal claims verification cost drops from O(replication) to O(proof-checking), but provides no concrete cost model. Key unresolved questions:
- What is the cost of VTD construction (borne by the producing agent)?
- What is the cost of VTD checking (borne by the membrane)?
- What is the cost of adversarial probing (borne by the adversary)?
- How do these costs compare to the baseline (replication-based verification)?
- At what scale (number of agents, claims per second, claim complexity) does the proof-carrying model break even with replication?

### Gap 4: Taxonomy Completeness and Classifiability (MEDIUM)

The 8-class taxonomy lacks a principled derivation (from what theory are these 8 classes derived?) and has not been tested for:
- Completeness (are there claims that don't fit?)
- Mutual exclusivity (can a claim belong to multiple classes?)
- Reliable classification (can agents consistently classify claims into the correct class?)
- Stability (does classification change based on context?)

### Gap 5: Adversarial Probing Stopping Criteria (MEDIUM)

When should adversarial probing stop? The architecture needs:
- A cost-benefit model for additional probes
- A definition of "sufficient adversarial coverage"
- A mechanism for detecting diminishing returns
- A formal relationship between adversarial probing depth and credibility increase

### Gap 6: Constitutional Parameter Specification (MEDIUM)

The proposal claims verification bottoms out at constitutional parameters, but does not specify:
- What the constitutional parameters are (even at a category level)
- How they are formalized (natural language? formal logic? constraints?)
- How ambiguity in constitutional interpretation is resolved
- How constitutional amendments interact with previously verified claims

---

## 4. Proposed Experiments

### Experiment 1: VTD Feasibility Study

**Goal:** Determine whether meaningful VTDs can be constructed for each claim class, and whether checking them is cheaper than re-execution.

**Method:**
1. Select 10 representative agent outputs per claim class (80 total).
2. For each, manually construct the best possible VTD.
3. Measure: (a) VTD construction time, (b) VTD size relative to output, (c) VTD checking time (by a different agent), (d) re-execution time (baseline).
4. Evaluate: Does VTD checking detect inserted errors? Is checking time < 50% of re-execution time?

**Success criterion:** VTD checking achieves >80% error detection rate at <50% of re-execution cost for at least 5 of 8 claim classes.

**Risk addressed:** Gap 1 (proof theory for non-deterministic claims).

### Experiment 2: Claim Classification Reliability

**Goal:** Determine whether the 8-class taxonomy can be reliably applied.

**Method:**
1. Generate 200 representative agent claims (25 per class, by design).
2. Present to 5 independent classifiers (3 human, 2 LLM-based) without class labels.
3. Measure inter-rater reliability (Fleiss' kappa).
4. Identify claims that receive 3+ different labels.
5. Identify claims that classifiers cannot place in any class.

**Success criterion:** Fleiss' kappa > 0.70 (substantial agreement) and <5% of claims unclassifiable.

**Risk addressed:** Gap 4 (taxonomy completeness and classifiability).

### Experiment 3: Credibility Propagation Stability

**Goal:** Determine whether credibility gradients can propagate stably through realistic dependency graphs.

**Method:**
1. Construct a dependency graph of 500 claims with realistic structure (mix of chains, trees, and DAGs, with some cycles resolved by credibility dampening).
2. Implement three composition algebras: (a) probabilistic independence, (b) Dempster-Shafer, (c) subjective logic.
3. Simulate credibility updates: change individual claim credibilities and propagate.
4. Measure: convergence time, stability (does the system oscillate?), sensitivity (does a 0.1 change in one claim cascade to >0.3 change in unrelated claims?).

**Success criterion:** System converges within 100 propagation steps, no oscillation, and cascade is bounded (change dampens with graph distance).

**Risk addressed:** Gap 2 (credibility composition algebra).

### Experiment 4: Adversarial Probing Effectiveness

**Goal:** Determine whether automated adversarial probing improves error detection compared to confirmatory checking.

**Method:**
1. Generate 100 agent claims, 30% with deliberately introduced subtle errors.
2. Apply three verification strategies: (a) re-execution and comparison (replication baseline), (b) VTD checking only, (c) VTD checking + adversarial probing.
3. Measure: precision, recall, F1 for error detection; total verification cost (LLM tokens consumed).

**Success criterion:** Strategy (c) achieves F1 > 0.85 with total cost < 1.5x strategy (a).

**Risk addressed:** Gap 3 (computational cost model) and Claim 3 (adversarial probing effectiveness).

### Experiment 5: Constitutional Grounding Coverage

**Goal:** Determine what percentage of agent claims can be traced to constitutional parameters.

**Method:**
1. Draft a set of 30 constitutional parameters covering the Atrahasis system's core values and constraints.
2. Take 100 representative agent claims from prior inventions (C1-C4).
3. For each claim, attempt to construct a verification trace that terminates at one or more constitutional parameters.
4. Measure: (a) percentage of claims with complete traces, (b) average trace length, (c) percentage requiring constitutional interpretation (ambiguous grounding).

**Success criterion:** >85% of claims have complete traces with <15% requiring interpretive judgment.

**Risk addressed:** Gap 6 (constitutional parameter specification) and Claim 5 (verifier regress resolution).

---

## 5. Overall Soundness Score

**Score: 3.2 / 5**

| Dimension | Score | Weight | Contribution |
|---|---|---|---|
| Theoretical grounding of individual claims | 3.8 | 0.25 | 0.95 |
| Cross-claim coherence | 3.0 | 0.20 | 0.60 |
| Empirical evidence / existence proofs | 2.5 | 0.20 | 0.50 |
| Formal completeness (proofs, algebras, cost models) | 2.0 | 0.20 | 0.40 |
| Practical feasibility of proposed mechanisms | 3.5 | 0.15 | 0.53 |
| **Weighted total** | | | **2.98 -> 3.2 (rounded with qualitative adjustment)** |

**Justification:**

The architecture draws on well-established theoretical traditions (PCC, Bayesian epistemology, Popperian falsificationism, foundationalist epistemology, argumentation theory) and combines them in a novel and architecturally coherent way. The individual claims range from SOUND (adversarial probing, process verification) to PARTIALLY_SOUND (proof-carrying model, taxonomy, constitutional grounding, credibility gradients). No claim is UNSOUND.

The primary weakness is the gap between the theoretical inspiration and the operational specification. The proposal invokes PCC but does not define a proof theory for AI agent outputs. It invokes Bayesian updating but does not define a composition algebra. It invokes constitutional foundationalism but does not specify the constitutional parameters. These gaps are not fatal — they are the work that the DESIGN and SPECIFICATION stages should address — but they mean the current proposal is a promising architectural sketch rather than a verified design.

The qualitative adjustment from 2.98 to 3.2 reflects that the architecture's *direction* is more sound than its current *specification* — the gaps are fillable, not fundamental.

---

## 6. Recommended Mitigations

### For Claim 1 (VTD Proof-Carrying Model) — PARTIALLY_SOUND

**Mitigation:** Reframe VTDs as "structured verification evidence" rather than "formal proofs." Reserve the term "proof" for Deterministic and Compliance claims where formal proof-checking is actually possible. For other claim classes, define VTDs as structured packages that reduce verification effort without claiming to make it sublinear. This is more honest and still valuable — structured evidence is easier to check than unstructured output, even if the speedup is constant-factor rather than complexity-class.

**Specific action:** Define a VTD schema per claim class that specifies exactly what evidence the VTD must contain, what the membrane checks, and what the expected verification cost is relative to re-execution. Accept that for some claim classes (Heuristic, Normative), VTD checking may not be substantially cheaper than re-generation.

### For Claim 2 (8-Class Taxonomy) — PARTIALLY_SOUND

**Mitigation:** Ground the taxonomy in an established typology. Two candidates:

1. **Toulmin's argument model** (claim, grounds, warrant, backing, qualifier, rebuttal) provides a principled decomposition of argumentative structure. Map each PCVM class to a Toulmin element or combination.

2. **Walton's argumentation schemes** provide a well-studied taxonomy of argument types with associated critical questions. The 8 PCVM classes could be derived as coarsenings of Walton's ~60 schemes.

**Specific action:** Add explicit rules for multi-class claims (e.g., a claim that is both Statistical and Empirical gets the union of proof obligations). Run the classification reliability experiment (Experiment 2) before finalizing the taxonomy.

### For Claim 5 (Constitutional Grounding) — PARTIALLY_SOUND

**Mitigation:** Acknowledge that constitutional grounding is foundationalism (a deliberate philosophical choice, not a complete solution to the regress problem) and address the three follow-on questions:

1. **Constitutional specification:** Produce a draft constitution with at least 20 parameters, covering epistemic standards, process requirements, and ethical constraints.
2. **Amendment protocol:** Specify the G-class supermajority threshold and the migration protocol for claims verified under a previous constitution.
3. **Undecidability handling:** Define an explicit "UNDECIDABLE" verification status for claims that cannot be traced to constitutional parameters, with a protocol for escalating undecidable claims to human judgment (HITL gate).

### For Claim 6 (Credibility Gradients) — PARTIALLY_SOUND

**Mitigation:** Adopt an existing composition algebra rather than inventing one. Josang's subjective logic is the strongest candidate: it represents beliefs as opinion tuples (belief, disbelief, uncertainty, base rate), supports conjunction, disjunction, discounting, and consensus operators, and has been applied to trust in multi-agent systems.

**Specific action:**
1. Formalize PCVM credibility as subjective logic opinions.
2. Define the dependency graph structure and specify which subjective logic operators apply at each edge type.
3. Prove or demonstrate convergence for the resulting propagation algorithm.
4. Define decay as a time-dependent increase in the uncertainty component of the opinion tuple.

### For Cross-Claim Coherence — PARTIALLY_COHERENT

**Mitigation:** Produce a formal interface specification between layers:

1. **Taxonomy -> Proof Model interface:** For each claim class, specify the VTD schema, the proof obligations, the verification algorithm, and the expected cost range.
2. **Proof Model -> Adversarial Probing interface:** Specify when adversarial probing is triggered (which claim classes, which credibility thresholds) and how adversarial results update credibility.
3. **Adversarial Probing -> Credibility Gradient interface:** Specify how a successful adversarial attack reduces credibility (by how much? immediately or gradually?).
4. **Credibility Gradient -> Constitutional Grounding interface:** Specify how credibility traces are grounded — does the constitutional parameter itself have a credibility (always 1.0?), or is it a binary trust anchor?

---

## Appendix: Key References

### Proof-Carrying Code and Verified Computation
- Necula, G. (1997). "Proof-Carrying Code." POPL '97.
- Appel, A. (2001). "Foundational Proof-Carrying Code." LICS '01.
- Leroy, X. (2009). "Formal Verification of a Realistic Compiler." CACM 52(7).
- Ben-Sasson et al. (2014). "Succinct Non-Interactive Zero Knowledge for a von Neumann Architecture." USENIX Security.

### Bayesian Epistemology and Belief Revision
- Alchourron, Gardenfors, Makinson (1985). "On the Logic of Theory Change." JSL 50(2).
- Walley, P. (1991). "Statistical Reasoning with Imprecise Probabilities." Chapman & Hall.
- Josang, A. (2016). "Subjective Logic: A Formalism for Reasoning Under Uncertainty." Springer.

### Falsificationism and Adversarial Testing
- Popper, K. (1934/1959). "The Logic of Scientific Discovery." Routledge.
- Claessen, K. & Hughes, J. (2000). "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs." ICFP '00.
- Perez et al. (2022). "Red Teaming Language Models with Language Models." arXiv:2202.03286.
- Bohme, M. et al. (2017). "Directed Greybox Fuzzing." CCS '17.

### Argumentation Theory
- Toulmin, S. (1958). "The Uses of Argument." Cambridge University Press.
- Walton, D., Reed, C., Macagno, F. (2008). "Argumentation Schemes." Cambridge University Press.
- van Eemeren, F. & Grootendorst, R. (2004). "A Systematic Theory of Argumentation." Cambridge University Press.

### Epistemology and Foundationalism
- Albert, H. (1968). "Treatise on Critical Reason." (Traktat uber kritische Vernunft).
- Alpern, B. & Schneider, F. (1985). "Defining Liveness." IPL 21(4).

### Provenance and Trust
- Moreau, L. & Missier, P. (2013). "PROV-DM: The PROV Data Model." W3C Recommendation.
- Souza et al. (2025). "PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions." IEEE e-Science 2025.
- Beth, T. et al. (1994). "Valuation of Trust in Open Networks." ESORICS '94.

### AI Safety and Verification
- Bai et al. (2022). "Constitutional AI: Harmlessness from AI Feedback." arXiv:2212.08073.
- VNN-COMP (Verification of Neural Networks Competition). Annual benchmarks.

---

*Assessment completed 2026-03-09. Science Advisor, Atrahasis Agent System v2.0.*
