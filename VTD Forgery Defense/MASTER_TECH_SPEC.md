# C11 — VTD Forgery Defense: Cryptographic Commitment and Orthogonal Verification

## Master Technical Specification

**Version:** 1.0.0
**Date:** 2026-03-10
**Invention ID:** C11
**System:** Atrahasis Agent System v2.0
**Status:** SPECIFICATION COMPLETE
**Assessment Council Verdict:** ADVANCE (Novelty 4/5, Feasibility 4/5, Impact 5/5, Risk 5/10)
**Normative References:** C5 (PCVM v1.0.0), C3 (Tidal Noosphere), C8 (DSF), C5/C6 Hardening Addendum v1.0.0, RFC 8032 (Ed25519), FIPS 180-4 (SHA-256), Groth16, FRI (STARK), Pedersen Commitments

> **Normative Reference Update (2026-03-11):** Normative references updated to C3 v2.0, C5 v2.0, C6 v2.0. C5 v2.0 integrates CACT defense mechanisms from this specification into the core PCVM architecture. However, C11 retains normative authority over its threat model (VTD forgery taxonomy, Confident Liar attack classification), formal proofs (commitment chain security, SNARK/STARK soundness bounds), and attack taxonomies (Sub-problems 1-3, orthogonal channel coverage model). Where C5 v2.0 and C11 overlap, C5 v2.0 governs integration behavior and C11 governs threat analysis.

---

## Abstract

The Proof-Carrying Verification Membrane (PCVM, C5) identifies VTD forgery -- the "Confident Liar" attack -- as a CRITICAL residual risk with HIGH residual severity after all mitigations. The C5/C6 Hardening Addendum adds defense-in-depth layers (source verification, evidence correlation, temporal decay, forgery heuristics, economic deterrents) that raise the cost of forgery but do not eliminate it. The fundamental problem is an **infinite trust regress**: verifying Source B requires Source C, which requires Source D, ad infinitum. All existing defenses operate within this regress by adding more links to the verification chain.

This specification escapes the trust regress by shifting verification from the evidence chain to **orthogonal channels that the forger cannot control**. The architecture -- called **Commit-Attest-Challenge-Triangulate (CACT)** -- addresses VTD forgery through four interlocking mechanisms:

1. **Temporal Commitment Binding (Commit):** Agents cryptographically commit to evidence and intermediate work products in real-time during VTD construction, before knowing which claims will be challenged. Retroactive fabrication becomes cryptographically impossible.

2. **Verifiable Computation Attestation (Attest):** Where VTD claims involve computation, SNARK/STARK proofs make computational integrity mathematically verifiable. The verifier need not trust the prover or re-execute the computation.

3. **Adversarial Interrogation Protocol (Challenge):** VTD producers must defend their claims under adversarial interrogation that tests the generative knowledge behind the VTD, not just the VTD's content. Forgers who fabricated evidence cannot answer unpredictable questions about it.

4. **Multi-Channel Orthogonal Verification (Triangulate):** VTD validity is confirmed through structurally independent channels -- process traces, independent re-derivation, statistical texture analysis, and environmental side-effects -- that a forger would need to simultaneously fake across multiple systems.

CACT does not claim to solve the epistemic truth problem (Sub-problem 3, which is provably unsolvable). It makes computational integrity forgery **mathematically impossible** (Sub-problem 1) and data provenance forgery **cryptographically bound and economically irrational** (Sub-problem 2). For epistemic truth, CACT makes forgery **combinatorially prohibitive** by requiring simultaneous fabrication across orthogonal channels.

This specification is a **normative extension** to C5 (PCVM v1.0.0) and the C5/C6 Hardening Addendum. It does not replace either document. All existing PCVM mechanisms remain in effect. CACT adds new verification layers that integrate with the existing architecture.

---

## Table of Contents

1. [Stage 1: Ideation Council Debate](#1-stage-1-ideation-council-debate)
2. [Stage 2: Research Synthesis](#2-stage-2-research-synthesis)
3. [Stage 3: Feasibility Assessment](#3-stage-3-feasibility-assessment)
4. [Stage 4: Architecture and Design](#4-stage-4-architecture-and-design)
5. [Stage 5: Formal Specification](#5-stage-5-formal-specification)
6. [Stage 6: Assessment](#6-stage-6-assessment)
7. [Appendix A: Configurable Parameters](#appendix-a-configurable-parameters)
8. [Appendix B: Test Vectors](#appendix-b-test-vectors)
9. [Appendix C: Conformance Requirements](#appendix-c-conformance-requirements)
10. [Appendix D: C9 Defense Invariant Compliance](#appendix-d-c9-defense-invariant-compliance)
11. [Appendix E: Glossary](#appendix-e-glossary)

---

## 1. Stage 1: Ideation Council Debate

### 1.1 Opening Statements

**Visionary:**

The research reveals a meta-insight that cuts across five independent domains: every successful anti-forgery system stops trying to verify the claim and instead verifies something the claimant cannot control. The immune system checks behavioral process. BFT checks independent convergence. Benford's Law checks statistical texture. Costly signaling checks the prover's generative capacity. Arms control checks involuntary environmental traces. The infinite trust regress exists only when verification is modeled as checking the evidence chain. Every domain escapes the regress by shifting to an orthogonal channel.

The bold concept: restructure VTD verification around **multi-channel orthogonal verification**. A VTD is valid not because its evidence chain checks out (which can always be forged) but because its validity is independently confirmable through channels that are structurally independent of the evidence chain itself. A Confident Liar can forge one channel. Forging five orthogonal channels simultaneously -- process traces, independent re-derivation, statistical texture, adversarial interrogation, and environmental side-effects -- is not just expensive but combinatorially prohibitive.

For the two solvable sub-problems, we can go further than "expensive to fake":
- **Computational integrity** becomes **mathematically impossible** to fake via SNARKs/STARKs. If a VTD claims "I ran analysis A on data D and got result R," a verifiable computation proof makes this unforgeable with soundness error ~2^-128.
- **Data provenance** becomes **cryptographically bound** via temporal commitment schemes. Agents commit to evidence hashes before knowing what claims they will support, making retroactive fabrication impossible without breaking SHA-256.

Only epistemic truth remains unsolvable -- and for that, we make forgery combinatorially expensive through orthogonal channel triangulation.

**Systems Thinker:**

The existing PCVM architecture has clear integration points for this. Let me map the minimum viable change:

1. **Temporal Commitment Binding** requires a new `CommitmentLog` data structure attached to VTDs. The VTD envelope (C5 Section 4.5) already has `timestamp` and `vtd_hash` fields. We extend with a `commitment_chain` field that records hash commitments made during VTD construction. Integration point: VTD Engine, pre-submission phase.

2. **Verifiable Computation** applies selectively to D-class and computational components of S-class claims. The D-class proof body (C5 Appendix A.1) already has a `proof_certificate` field with `format` enum. We add `SNARK_PROOF` and `STARK_PROOF` to the enum and define the corresponding certificate schemas. Integration point: Proof Checker (Tier 1), extended proof type.

3. **Adversarial Interrogation** extends the existing Adversarial Probing System (C5 Section 7). The five existing probe types (CX, AE, SC, LF, BP) test the VTD artifact. We add a sixth probe type: **Knowledge Interrogation (KI)** -- direct questioning of the producing agent about content they should know if the VTD is genuine. Integration point: Adversarial Probing System, new probe type.

4. **Orthogonal Verification Channels** extend the Evidence Evaluator (Tier 2) with three new sub-checks: process trace verification, statistical texture analysis, and environmental side-effect cross-referencing. Integration point: Tier 2 verification pipeline, new phases.

The minimum viable change is surprisingly contained. We are adding fields to existing schemas, extending existing enums, and adding phases to existing pipelines. No new top-level components are needed. The PCVM component map (C5 Section 3.3) remains the same nine components.

The key constraint: this must integrate with the 9 canonical claim classes (D/C/P/R/E/S/K/H/N per C9), Subjective Logic credibility engine, VRF committee selection, MCT issuance, and Settlement Plane. None of those change. The changes are all within the VTD Engine, Proof Checker, Evidence Evaluator, and Adversarial Prober -- internal components of the membrane.

**Critic:**

Three concerns:

First, **complexity cost.** The existing PCVM is already complex: 8 claim classes, 3 tiers, 9 components, 7 invariants, 5 probe types. Adding temporal commitment chains, SNARK/STARK proof infrastructure, adversarial interrogation, and three new orthogonal verification channels increases the attack surface. Every new mechanism is a new thing that can go wrong, a new thing that can be gamed, and a new thing that adds latency. The C5/C6 Hardening Addendum already adds source verification, evidence correlation, temporal decay, forgery heuristics, and economic deterrents. At what point does defense-in-depth become defense-in-confusion?

Second, **the SNARK/STARK assumption is narrower than it appears.** Verifiable computation works for deterministic computations. But the Confident Liar problem is primarily about E-class (empirical) and H-class (heuristic) claims -- exactly the classes where computation is NOT the issue. The agent is not lying about a computation; it is lying about what the external world contains. SNARKs prove "I correctly computed X from input Y" but not "input Y is genuine." If the forger feeds fabricated data into a SNARK circuit, the proof is valid over fabricated data.

Third, **adversarial interrogation has a fundamental weakness against LLMs.** The costly signaling analogy assumes the prover cannot fake knowledge. But LLMs can generate plausible answers to adversarial questions about fabricated content -- they are, in effect, generating consistent hallucinations on the fly. An LLM that fabricated a citation can plausibly describe the cited paper's methodology because it can generate a consistent fictional methodology. This is not like a cuckoo chick that develops on the wrong timeline. It is like a cuckoo chick with a holographic disguise.

### 1.2 Concept Proposals

#### C11-A: Full Orthogonal Verification Architecture (Most Ambitious)

Addresses all three sub-problems:

- **Computational integrity:** SNARK/STARK proofs for all D-class and computational S-class claims. Soundness error ~2^-128.
- **Data provenance:** Temporal commitment binding (commit-before-claim), TEE-attested evidence gathering where hardware supports it, multi-agent evidence decomposition (MPC-inspired), first-party oracle integration for API-sourced data.
- **Epistemic truth:** Five-channel orthogonal verification: (1) process trace analysis, (2) independent re-derivation by K agents, (3) statistical texture analysis (Benford's-law-style ensemble checks), (4) adversarial knowledge interrogation, (5) environmental side-effect cross-referencing. All five channels must agree for high-stakes claims.

Novel mechanisms: commitment chain protocol, verifiable computation integration, knowledge interrogation probe type, process trace behavioral model, statistical texture scorer, environmental side-effect auditor, independent re-derivation protocol.

**Risk:** Enormous implementation complexity. Seven novel mechanisms. TEE dependency introduces hardware trust assumptions. MPC-inspired decomposition requires protocol design. Independent re-derivation multiplies computational cost by K. Statistical texture models require calibration data that does not yet exist.

#### C11-B: Commit-Attest-Challenge-Triangulate / CACT (Pragmatic Middle)

Addresses computational integrity and data provenance structurally. Accepts epistemic truth as unsolvable but makes it combinatorially expensive to fake.

- **Computational integrity:** SNARK/STARK proofs for D-class claims. Optional for S-class where computation is the primary evidence.
- **Data provenance:** Temporal commitment binding (commit-before-claim). No TEE or MPC dependency. Commitment chain is purely cryptographic (hash-based), requiring no special hardware.
- **Epistemic truth:** Three orthogonal channels: (1) adversarial knowledge interrogation (KI probe type), (2) process trace consistency checking, (3) environmental side-effect cross-referencing. These do not guarantee truth but make forgery require simultaneous fabrication across three independent systems.

Drops from C11-A: TEE attestation (fragile hardware trust), MPC-based evidence decomposition (protocol complexity), independent re-derivation (computational cost), statistical texture analysis (requires calibration data).

**Risk:** Moderate. Four mechanisms: commitment chain (well-understood cryptography), SNARK/STARK integration (proven technology), knowledge interrogation (extends existing probing), orthogonal channel checks (extends existing verification). No hardware dependencies. No novel cryptographic primitives.

#### C11-C: Temporal Commitment Binding Only (Minimal / Best ROI)

Single mechanism: commit-before-claim.

Agents cryptographically commit to evidence hashes during VTD construction, timestamped and sequenced. Upon submission, the commitment chain is sealed. During verification, the membrane can challenge any commitment -- "open this commitment and prove the evidence existed at the claimed time." Retroactive fabrication is cryptographically impossible.

This single mechanism provides the highest ROI because it:
- Prevents the most common forgery strategy (retroactive evidence fabrication)
- Requires no computational overhead beyond hash operations
- Integrates trivially with the existing VTD envelope
- Is well-understood cryptography with no novel assumptions
- Works for all claim classes, not just D-class

**Risk:** Low. But also low coverage. Does not address real-time fabrication (agent fabricates evidence in real-time and immediately commits to it), does not address computational integrity, does not address the core trust regress for claims about external reality.

### 1.3 Council Vote and Debate

**Visionary votes: C11-A.**
"Half-measures are how you end up with legacy technical debt. If we are going to solve the Confident Liar, let us solve it properly. C11-B drops three mechanisms that provide genuine value -- TEE attestation, independent re-derivation, and statistical texture analysis all appear independently in the domain analogies. Dropping them is not pragmatism, it is premature optimization."

**Systems Thinker votes: C11-B.**
"C11-A has seven novel mechanisms, three of which (TEE, MPC, independent re-derivation) introduce dependencies on hardware, multi-party protocols, and K-fold computational redundancy respectively. Each of these is individually well-motivated but collectively they create an implementation surface that will take years to build, test, and harden. C11-B captures 80% of the defensive value with 40% of the complexity. The mechanisms it drops (TEE, MPC, statistical texture, independent re-derivation) can be added later as CACT extensions -- they are architecturally compatible. Ship C11-B now, add C11-A extensions in C15+."

**Critic votes: C11-B.**
"I was prepared to vote C11-C because simplicity is a virtue and commitment chains alone provide genuine value. But the Critic's job is to find what fails, and C11-C fails against real-time fabrication -- the agent that fabricates evidence in real-time and commits to it immediately. C11-B's knowledge interrogation and orthogonal channel checks provide the additional coverage needed to catch this. C11-A is overengineered. The TEE vulnerability literature (TEE.Fail 2025, Sigy attack, SgxPectre) shows hardware attestation is not the foundation you want for a security architecture. MPC requires honest majority assumptions we cannot guarantee. C11-B is the right scope."

**Vote tally: C11-B (2-1). CACT selected.**

**Visionary's concession:** "Accepted. But I want the specification to explicitly define extension points where C11-A mechanisms can be added later. TEE attestation slots, MPC decomposition hooks, independent re-derivation triggers, and statistical texture scorer interfaces should be specified as OPTIONAL extension points even if their implementations are deferred."

**Systems Thinker:** "Agreed. Extension points cost nothing to specify and preserve future optionality."

**DECISION: C11-B (CACT) is the selected concept, with C11-A extension points documented.**

---

## 2. Stage 2: Research Synthesis

### 2.1 Key Prior Art Implications for CACT

The research phase produced two comprehensive documents: a cross-domain analogy brief (5 domains) and a prior art/landscape report (8 technical areas). The following findings directly shape CACT's design.

### 2.2 Temporal Commitment Binding

**Prior art:** Blockchain commitment schemes, IAEA tamper-evident seals (arms control analogy), Merkle tree-based timestamping.

**Key insight from arms control analogy:** "A nation can forge documents but cannot forge the isotopic signature of its groundwater." Translated: an agent can forge a VTD but cannot retroactively alter cryptographic commitments made before it knew which claims would be challenged.

**Research finding:** The commit-before-claim pattern is the highest-priority defense recommended by both the domain analogies (Priority #1: Arms Control / Environmental Sampling) and the research report (Layer 1: Commitment Before Claim). It is rated "immediately implementable" by both analyses.

**Design implication:** Commitment chains must be sequential (each commitment includes the hash of the previous commitment), timestamped (bound to tidal epoch clock), and tamper-evident (any alteration invalidates the chain). The chain structure is a Merkle chain, not a Merkle tree, because VTD construction is sequential, not parallel.

### 2.3 Verifiable Computation

**Prior art:** SNARKs (Groth16, PlonK), STARKs (FRI-based), folding schemes (Nova, HyperNova), Pinocchio, EZKL, Modulus Labs.

**Key research finding:** "Verifiable computation offers the strongest theoretical guarantee against VTD forgery of any technique surveyed." ZKP market reached $1.28B in 2024. Practical deployments exist for KYC, compliance, identity verification. However, 96% of documented circuit-layer bugs in SNARK systems were due to under-constrained circuits.

**Key limitation acknowledged by Critic:** SNARKs prove computational relationships, not ground truth. An agent with fabricated input data can produce a valid SNARK proof over fabricated data. Therefore, SNARK/STARK attestation must be combined with commitment binding (proving the input data was committed before the claim) to be effective.

**Design implication:** Verifiable computation applies to D-class and computational S-class claims only. It is not a universal defense. The proof must attest to both "this computation was performed correctly" AND "the inputs were previously committed in the commitment chain."

### 2.4 Adversarial Knowledge Interrogation

**Prior art:** Costly signaling theory (Zahavi's handicap principle), avian brood parasitism counter-adaptations, Bellingcat five-pillar verification (motivation analysis pillar).

**Key insight from cuckoo analogy:** "The proof is in the prover, not the proof." An agent that fabricated a citation cannot explain the cited paper's methodology. An agent that invented a data point cannot predict neighboring data points.

**Research finding rated 4/5 transferability:** "The PCVM could implement VTD defense sessions -- adversarial interrogation protocols where a VTD's producer must answer unpredictable questions about the content."

**Key limitation acknowledged by Critic:** LLMs can generate plausible answers to adversarial questions about fabricated content. A sufficiently powerful LLM might fabricate a VTD AND answer questions about it by generating consistent hallucinations.

**Design implication:** Knowledge interrogation is necessary but not sufficient. It must be combined with orthogonal channels that test dimensions the LLM cannot easily hallucinate consistently -- process traces (which require real computational history) and environmental side-effects (which require real system interactions). The interrogation protocol must include questions that require specific factual recall (not just plausible generation), such as exact numerical values, specific timestamps, and precise cross-references between sources.

### 2.5 Orthogonal Verification Channels

**Prior art:** Byzantine fault tolerance (consensus without trust), forensic accounting (Benford's Law), immune system (negative selection / process verification), arms control (environmental sampling).

**Meta-insight from domain analogies:** "All five analogies share a common structural move: they stop trying to verify the claim and instead verify something the claimant cannot control."

**BFT analogy (5/5 transferability):** "Truth emerges from redundant independent computation, not from verifying any single source." Independent re-derivation breaks the trust regress because truth is established by convergent independent computation.

**Immune system analogy (4/5 transferability):** "Model the process, not the product." A fabricated VTD was produced differently than a genuine one -- different timing, different access patterns, different intermediate states.

**Arms control analogy (5/5 transferability):** "Environmental sampling -- checking consequences that the agent did not intend to produce and therefore did not think to fake."

**Design implication:** CACT implements three orthogonal channels (dropping independent re-derivation and statistical texture analysis to C11-A extension points):
1. **Knowledge Interrogation** -- tests the prover, not the proof (costly signaling channel)
2. **Process Trace Consistency** -- tests the generative process, not the product (immune system channel)
3. **Environmental Side-Effect Audit** -- tests involuntary traces in external systems (arms control channel)

### 2.6 The Three Sub-Problems Framework

The research report's decomposition of VTD forgery into three sub-problems is the theoretical foundation of CACT:

| Sub-Problem | Solvability | CACT Mechanism | Guarantee Level |
|---|---|---|---|
| Computational integrity | Mathematically solvable | SNARK/STARK proofs | Soundness error ~2^-128 |
| Data provenance | Engineeringly solvable | Commitment binding + orthogonal channels | Cryptographic binding + economic irrationality |
| Epistemic truth | Provably unsolvable | Orthogonal channel triangulation | Combinatorially expensive to fake |

CACT's honesty: it does not claim to solve the unsolvable. It transforms each sub-problem to the strongest achievable guarantee level.

---

## 3. Stage 3: Feasibility Assessment

### 3.1 Adversarial Analysis: Five Attacks Against CACT

**Adversarial Analyst** constructs the strongest case against CACT:

**Attack A1: Real-Time Fabrication with Immediate Commitment**

The commitment chain prevents retroactive fabrication. But what if the agent fabricates evidence in real-time and immediately commits to it? The agent generates a fictitious source, commits its hash, then cites it in the VTD. The commitment chain is valid -- the evidence was committed before the claim -- but the evidence is fabricated.

*Severity: HIGH. This is the primary residual attack after commitment binding.*

*CACT defense:* This attack is caught by the orthogonal channels, not by the commitment chain. The commitment chain proves temporal ordering (evidence existed before claim), but the orthogonal channels test whether the evidence is genuine: (1) Knowledge interrogation tests whether the agent truly understands the cited material; (2) Process trace analysis checks whether the agent's computational behavior is consistent with having genuinely retrieved and analyzed the evidence; (3) Environmental side-effect audit checks whether the external system (database, API, web service) recorded the agent's access. A fabricated source will fail channel 3 (no access record in the external system) and likely fail channel 1 (agent cannot answer deep questions about fabricated material).

*Residual risk: MEDIUM.* If the external system is unavailable for audit (source is offline, API has no query logging), channels 2 and 1 alone may not detect a sophisticated fabrication.

**Attack A2: Commitment Chain Flooding**

An adversarial agent generates thousands of commitments per epoch -- committing to every conceivable evidence hash in advance. When constructing a forged VTD, it selects the pre-committed hashes that match its fabricated evidence. The commitment chain appears valid because the evidence hashes were indeed committed before the claim.

*Severity: HIGH. This is a storage and verification scalability attack.*

*CACT defense:* Rate limiting. The commitment protocol enforces a maximum commitment rate per agent per epoch (configurable, default: 100 commitments per epoch). Commitments exceeding the rate limit are rejected. Additionally, each commitment must include a `purpose_hash` -- a blinded commitment to the claim context -- that is revealed at VTD submission. A commitment whose revealed purpose does not relate to the submitted VTD is flagged. Flooding is detectable because the vast majority of pre-committed hashes will have no matching VTD, and the purpose reveals will fail.

*Residual risk: LOW.* Rate limiting is crude but effective. The attack requires the adversary to predict which evidence it will need to fabricate, commit to it in advance, and stay within rate limits -- which negates the advantage of pre-commitment.

**Attack A3: Knowledge Interrogation Gaming via LLM Hallucination**

An LLM-based agent fabricates a VTD and, when interrogated, generates plausible but fabricated answers. The LLM's ability to generate consistent hallucinations means the knowledge interrogation channel can be defeated by a sufficiently capable model.

*Severity: HIGH. This attacks the core asymmetry assumption of the costly signaling mechanism.*

*CACT defense:* Knowledge interrogation questions are designed to require specific factual recall that hallucination cannot reliably produce: (1) Exact numerical values from cited sources ("What is the third value in Table 2 of the cited paper?"); (2) Cross-reference consistency checks ("Source A and Source B both report on metric X. What are their respective values and do they agree within 5%?"); (3) Negative knowledge tests ("Which of these five methodologies does the cited paper explicitly reject, and why?"). These questions require the agent to have actually read the source material. An LLM hallucinating will produce plausible but factually incorrect answers. The interrogation system cross-references the agent's answers against independently retrieved source material.

*Residual risk: MEDIUM.* If the interrogation system cannot independently retrieve the source material (source offline, paywalled, etc.), it cannot verify the agent's answers. In this case, the interrogation channel degrades to a plausibility check rather than a factual verification.

**Attack A4: Environmental Side-Effect Spoofing**

An adversarial agent manipulates external system logs to create false side-effects. For example, it fabricates API query logs or injects false access records into a database's audit trail.

*Severity: MEDIUM. Requires compromising external systems, which is outside the agent's normal capabilities.*

*CACT defense:* Environmental side-effect audit relies on external systems that the agent does not control. If the agent can compromise external system logs, the attack succeeds -- but this requires a capability (external system compromise) that is orthogonal to VTD fabrication capability. The defense is layered: (1) the membrane queries external systems directly, not through the agent; (2) multiple independent external systems are checked (if the claim involves multiple sources, each source system's logs are independently queried); (3) the agent cannot predict which external systems will be audited (VRF-selected). Spoofing all queried external systems simultaneously requires compromising multiple independent systems, which is a much higher bar than fabricating a single VTD.

*Residual risk: LOW.* Unless the adversary has system-level compromise capabilities (which is outside PCVM's threat model).

**Attack A5: Selective Forgery on Unverifiable Claims**

An adversary forges only claims where orthogonal channels are weak: topics with few external sources, novel domains where no baseline process traces exist, areas where environmental side-effects are minimal. By choosing the forgery target carefully, the adversary avoids the channels most likely to detect fabrication.

*Severity: MEDIUM-HIGH. This is the strategic adversary problem.*

*CACT defense:* Claims where orthogonal channels are weak receive lower credibility ceilings. The CACT architecture assigns an **Orthogonal Verification Coverage (OVC) score** to each VTD based on how many orthogonal channels produced usable verification signals. VTDs with low OVC scores (fewer than 2 channels provided verification) are capped at lower maximum credibility. This does not prevent forgery but prevents forged claims from achieving high credibility, limiting their impact on the knowledge graph.

*Residual risk: MEDIUM.* The adversary can still inject low-credibility claims. But low-credibility claims have limited influence on downstream decisions and are more likely to be caught by deep-audit.

### 3.2 Assessment Council Scoring

**Advocate:**
"CACT is the first PCVM extension that addresses VTD forgery structurally rather than just raising costs. The temporal commitment binding alone would be a significant advance -- it eliminates retroactive fabrication entirely. Combined with verifiable computation for D-class and the three orthogonal channels, CACT transforms VTD forgery from a problem that 'no complete defense exists' (C5 Section 11.4) to a problem that is mathematically impossible for computational integrity, cryptographically bound for data provenance, and combinatorially expensive for epistemic truth. The architecture integrates cleanly with existing PCVM components and requires no new top-level components."

**Skeptic:**
"The knowledge interrogation channel's effectiveness against LLMs is unproven. The environmental side-effect audit depends on external systems having query logs -- many do not. The process trace consistency model requires baseline behavioral models that do not exist yet. CACT adds four mechanisms to an already complex system, increasing the maintenance and security audit burden. The real question: does CACT measurably reduce the probability of successful VTD forgery compared to the existing C5/C6 Hardening measures, and by how much? Without empirical validation, we are specifying a defense against a theoretical threat using theoretical mechanisms."

**Arbiter:**
"The Skeptic's concerns are valid but do not outweigh the structural advance. The temporal commitment binding is well-understood cryptography with no novel assumptions -- this alone justifies the specification. Verifiable computation for D-class is proven technology (SNARKs deployed at scale in production systems). The knowledge interrogation and orthogonal channels are more speculative but extend existing PCVM mechanisms (adversarial probing, source verification) rather than introducing wholly new paradigms. Scoring:"

| Criterion | Score | Rationale |
|---|---|---|
| Novelty | 4/5 | Multi-channel orthogonal verification is novel for agent verification systems. Commitment binding and VCs are established in other domains. |
| Feasibility | 4/5 | Commitment chains and VC integration are immediately implementable. KI and orthogonal channels require development but extend existing infrastructure. |
| Impact | 5/5 | Addresses the #1 residual risk in the entire PCVM system. Transforms VTD forgery from HIGH residual risk to MEDIUM. |
| Risk | 5/10 | Moderate complexity increase. KI effectiveness unproven against advanced LLMs. Environmental audit depends on external system cooperation. |

**Verdict: ADVANCE.** CACT should proceed to full specification. The temporal commitment binding and verifiable computation components are high-confidence. The knowledge interrogation and orthogonal channel components should be specified with explicit validation gates.

---

## 4. Stage 4: Architecture and Design

### 4.1 CACT Integration with PCVM

CACT extends the existing PCVM architecture (C5 Section 3.3) without adding new top-level components. All changes are internal to existing components:

```
+------------------------------------------------------------------+
|                         PCVM MEMBRANE                             |
|                                                                   |
|  +----------------+    +------------------+    +---------------+  |
|  | VTD Engine     |    | Claim Classifier |    | Verification  |  |
|  | + COMMITMENT   |--->| (unchanged)      |--->| Dispatcher    |  |
|  |   CHAIN MGR    |    |                  |    | + OVC SCORER  |  |
|  +----------------+    +------------------+    +-------+-------+  |
|                                                        |          |
|  +------+  +-----------+  +-----------+  +-------+    |          |
|  | Proof|  | Evidence  |  |Attestation|  | Adver-|    |          |
|  |Checker| | Evaluator |  | Reviewer  |  | sarial|<---+          |
|  |+ SNARK| |+ PROC_CHK |  |(unchanged)|  |Prober |              |
|  |+ STARK| |+ ENV_AUDIT|  |           |  |+ KI   |              |
|  +---+--+  +-----+-----+  +-----+-----+  +---+---+              |
|      |           |               |            |                   |
|      +-----------+-------+-------+------------+                   |
|                          |                                        |
|              +-----------v-----------+    +-------------------+   |
|              | Credibility Engine    |    | Deep-Audit        |   |
|              | + OVC CREDIT CAP     |    | Subsystem         |   |
|              +-----------+-----------+    | + COMMIT AUDIT    |   |
|                          |               +-------------------+   |
|              +-----------v-----------+                            |
|              | Knowledge Admission   |                            |
|              | Gate (unchanged)      |                            |
|              +-----------------------+                            |
+------------------------------------------------------------------+

Legend (CACT additions marked with +):
  + COMMITMENT CHAIN MGR  - Manages temporal commitment chains (Section 5.2)
  + SNARK/STARK           - Verifiable computation proof types (Section 5.3)
  + KI                    - Knowledge Interrogation probe type (Section 5.4)
  + PROC_CHK              - Process trace consistency checker (Section 5.5)
  + ENV_AUDIT             - Environmental side-effect auditor (Section 5.5)
  + OVC SCORER            - Orthogonal Verification Coverage scorer (Section 5.5)
  + OVC CREDIT CAP        - Credibility cap based on OVC score (Section 5.6)
  + COMMIT AUDIT          - Commitment chain audit in deep-audit (Section 5.7)
```

### 4.2 New Data Structures

#### 4.2.1 Commitment Chain

The commitment chain is a sequential, hash-linked log of evidence commitments made during VTD construction.

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/commitment-chain.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Commitment Chain",
  "type": "object",
  "required": [
    "chain_id", "agent_id", "epoch", "commitments", "chain_hash",
    "agent_signature"
  ],
  "properties": {
    "chain_id": {
      "type": "string",
      "pattern": "^cc:[a-f0-9]{16}$"
    },
    "agent_id": { "type": "string" },
    "epoch": { "type": "integer", "minimum": 0 },
    "commitments": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "sequence_num", "timestamp", "evidence_hash",
          "purpose_hash", "prev_commitment_hash"
        ],
        "properties": {
          "sequence_num": { "type": "integer", "minimum": 0 },
          "timestamp": { "type": "string", "format": "date-time" },
          "evidence_hash": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$",
            "description": "SHA-256 hash of the evidence artifact being committed"
          },
          "evidence_type": {
            "type": "string",
            "enum": [
              "SOURCE_CONTENT", "INTERMEDIATE_RESULT", "DATASET",
              "API_RESPONSE", "COMPUTATION_TRACE", "REASONING_STEP"
            ]
          },
          "purpose_hash": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$",
            "description": "Blinded hash of the claim context this evidence relates to. Revealed at VTD submission."
          },
          "prev_commitment_hash": {
            "type": ["string", "null"],
            "pattern": "^[a-f0-9]{64}$",
            "description": "Hash of the previous commitment in the chain. Null for the first commitment."
          },
          "metadata": {
            "type": "object",
            "properties": {
              "source_uri": { "type": "string", "format": "uri" },
              "retrieval_method": { "type": "string" },
              "size_bytes": { "type": "integer" }
            }
          }
        }
      },
      "minItems": 1,
      "maxItems": 100
    },
    "chain_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$",
      "description": "SHA-256 hash of the serialized commitment array"
    },
    "agent_signature": {
      "type": "string",
      "description": "Ed25519 signature over chain_hash"
    }
  },
  "additionalProperties": false
}
```

**Chain integrity verification:**

```python
def verify_commitment_chain(chain: CommitmentChain) -> ChainVerification:
    """
    Verify the structural integrity of a commitment chain.

    Checks:
    1. Sequential numbering (no gaps)
    2. Hash linking (each commitment includes hash of previous)
    3. Temporal ordering (timestamps are monotonically non-decreasing)
    4. Rate limiting (commitments per epoch <= MAX_COMMITMENTS_PER_EPOCH)
    5. Chain hash matches serialized content
    6. Agent signature validates
    """
    result = ChainVerification(chain_id=chain.chain_id)

    # Check 1: Sequential numbering
    for i, c in enumerate(chain.commitments):
        if c.sequence_num != i:
            result.add_failure("SEQUENCE_GAP", f"Expected {i}, got {c.sequence_num}")
            return result

    # Check 2: Hash linking
    for i, c in enumerate(chain.commitments):
        if i == 0:
            if c.prev_commitment_hash is not None:
                result.add_failure("INVALID_GENESIS", "First commitment must have null prev_hash")
                return result
        else:
            expected_prev = SHA256(canonical_serialize(chain.commitments[i-1]))
            if c.prev_commitment_hash != expected_prev:
                result.add_failure("BROKEN_LINK",
                    f"Commitment {i}: prev_hash mismatch")
                return result

    # Check 3: Temporal ordering
    for i in range(1, len(chain.commitments)):
        if chain.commitments[i].timestamp < chain.commitments[i-1].timestamp:
            result.add_failure("TEMPORAL_VIOLATION",
                f"Commitment {i} timestamp precedes commitment {i-1}")
            return result

    # Check 4: Rate limiting
    if len(chain.commitments) > MAX_COMMITMENTS_PER_EPOCH:  # default: 100
        result.add_failure("RATE_EXCEEDED",
            f"{len(chain.commitments)} commitments exceeds limit "
            f"{MAX_COMMITMENTS_PER_EPOCH}")
        return result

    # Check 5: Chain hash
    computed_hash = SHA256(canonical_serialize(chain.commitments))
    if computed_hash != chain.chain_hash:
        result.add_failure("CHAIN_HASH_MISMATCH", "Chain hash does not match content")
        return result

    # Check 6: Signature
    if not verify_ed25519(chain.agent_id, chain.chain_hash, chain.agent_signature):
        result.add_failure("SIGNATURE_INVALID", "Agent signature does not verify")
        return result

    result.status = "VALID"
    return result
```

#### 4.2.2 VTD Envelope Extension

The VTD Common Envelope (C5 Section 4.5) is extended with CACT fields:

```json
{
  "cact_extension": {
    "type": "object",
    "required": ["commitment_chain_id", "purpose_reveals"],
    "properties": {
      "commitment_chain_id": {
        "type": "string",
        "pattern": "^cc:[a-f0-9]{16}$",
        "description": "Reference to the commitment chain for this VTD"
      },
      "purpose_reveals": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["commitment_seq", "purpose_preimage"],
          "properties": {
            "commitment_seq": { "type": "integer" },
            "purpose_preimage": {
              "type": "string",
              "description": "Preimage of the purpose_hash from the commitment. Must hash to the committed purpose_hash."
            }
          }
        },
        "description": "Reveals linking commitments to this VTD's claims"
      },
      "vc_proofs": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["proof_system", "proof_data", "public_inputs_hash"],
          "properties": {
            "proof_system": {
              "type": "string",
              "enum": ["GROTH16", "PLONK", "STARK_FRI", "NOVA"]
            },
            "proof_data": {
              "type": "string",
              "description": "Base64-encoded proof bytes"
            },
            "public_inputs_hash": {
              "type": "string",
              "pattern": "^[a-f0-9]{64}$"
            },
            "circuit_id": {
              "type": "string",
              "description": "Identifier of the registered verification circuit"
            },
            "verification_key_hash": {
              "type": "string",
              "pattern": "^[a-f0-9]{64}$"
            }
          }
        },
        "default": [],
        "description": "Verifiable computation proofs (D-class, optional S-class)"
      },
      "process_trace": {
        "type": "object",
        "properties": {
          "activity_log": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["timestamp", "activity_type", "activity_hash"],
              "properties": {
                "timestamp": { "type": "string", "format": "date-time" },
                "activity_type": {
                  "type": "string",
                  "enum": [
                    "SOURCE_RETRIEVAL", "DATA_ANALYSIS", "REASONING_STEP",
                    "CROSS_REFERENCE", "DRAFT_REVISION", "TOOL_INVOCATION"
                  ]
                },
                "activity_hash": {
                  "type": "string",
                  "pattern": "^[a-f0-9]{64}$"
                },
                "duration_ms": { "type": "integer", "minimum": 0 },
                "resource_consumption": {
                  "type": "object",
                  "properties": {
                    "tokens_used": { "type": "integer" },
                    "api_calls": { "type": "integer" },
                    "compute_ms": { "type": "integer" }
                  }
                }
              }
            }
          },
          "total_construction_time_ms": { "type": "integer", "minimum": 0 },
          "trace_hash": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$"
          }
        },
        "description": "Record of the VTD construction process"
      },
      "ovc_score": {
        "type": ["number", "null"],
        "minimum": 0.0,
        "maximum": 1.0,
        "description": "Orthogonal Verification Coverage score. Set by verifier, not producer."
      }
    }
  }
}
```

#### 4.2.3 Verifiable Computation Proof Extension for D-class

The D-class proof body (C5 Appendix A.1) is extended with new proof types:

```python
# Extended proof_type enum for D-class VTDs
PROOF_TYPES = [
    "RECOMPUTATION",       # Existing: re-execute computation
    "HASH_VERIFICATION",   # Existing: verify output hash
    "PROOF_CERTIFICATE",   # Existing: Coq/TLA/Isabelle proof
    "PROOF_SKETCH",        # Existing: spot-check intermediate steps
    "SNARK_PROOF",         # NEW: SNARK proof of computation correctness
    "STARK_PROOF",         # NEW: STARK proof (post-quantum secure)
]
```

### 4.3 Verification Protocol Extensions

#### 4.3.1 Commitment Chain Verification (All Classes)

Commitment chain verification is the first phase of CACT-extended verification, executed before any class-specific verification:

```python
def verify_cact_commitments(vtd: VTD) -> CommitmentVerification:
    """
    Phase 0 of CACT-extended verification.
    Executed for ALL claim classes before class-specific verification.

    Checks:
    1. Commitment chain exists and is structurally valid
    2. Purpose reveals match: each revealed purpose hashes to the
       committed purpose_hash
    3. Evidence binding: evidence cited in the VTD appears in the
       commitment chain (evidence_hash matches)
    4. Temporal ordering: all commitments precede the VTD submission
       timestamp
    5. Coverage: the VTD does not cite evidence absent from the
       commitment chain
    """
    cact = vtd.cact_extension
    if cact is None:
        # CACT extension not present.
        # For D-class: REQUIRED (return failure)
        # For other classes: OPTIONAL but credibility-capped
        if vtd.assigned_class == "D":
            return CommitmentVerification(
                status="FAILED",
                reason="D-class VTDs MUST include CACT commitment chain"
            )
        else:
            return CommitmentVerification(
                status="ABSENT",
                credibility_cap=CACT_ABSENT_CREDIBILITY_CAP  # 0.70
            )

    # Step 1: Retrieve and verify the commitment chain
    chain = retrieve_commitment_chain(cact.commitment_chain_id)
    if chain is None:
        return CommitmentVerification(
            status="FAILED",
            reason="Referenced commitment chain not found"
        )

    chain_check = verify_commitment_chain(chain)
    if chain_check.status != "VALID":
        return CommitmentVerification(
            status="FAILED",
            reason=f"Chain integrity failure: {chain_check.failures}"
        )

    # Step 2: Verify purpose reveals
    for reveal in cact.purpose_reveals:
        commitment = chain.commitments[reveal.commitment_seq]
        computed_purpose_hash = SHA256(reveal.purpose_preimage.encode())
        if computed_purpose_hash != commitment.purpose_hash:
            return CommitmentVerification(
                status="FAILED",
                reason=f"Purpose reveal mismatch at seq {reveal.commitment_seq}"
            )

    # Step 3: Evidence binding — check that VTD evidence appears in chain
    vtd_evidence_hashes = extract_evidence_hashes(vtd)
    committed_evidence_hashes = {c.evidence_hash for c in chain.commitments}

    bound_count = 0
    unbound_evidence = []
    for eh in vtd_evidence_hashes:
        if eh in committed_evidence_hashes:
            bound_count += 1
        else:
            unbound_evidence.append(eh)

    binding_ratio = bound_count / max(1, len(vtd_evidence_hashes))

    # Step 4: Temporal ordering
    vtd_submission_time = parse_timestamp(vtd.timestamp)
    for c in chain.commitments:
        if parse_timestamp(c.timestamp) > vtd_submission_time:
            return CommitmentVerification(
                status="FAILED",
                reason=f"Commitment {c.sequence_num} timestamp "
                       f"({c.timestamp}) is after VTD submission "
                       f"({vtd.timestamp})"
            )

    # Step 5: Compute commitment coverage score
    coverage = CommitmentVerification(status="VERIFIED")
    coverage.binding_ratio = binding_ratio
    coverage.unbound_evidence = unbound_evidence
    coverage.chain_length = len(chain.commitments)

    # Credibility adjustment based on binding ratio
    if binding_ratio >= 0.90:
        coverage.credibility_boost = 0.05   # Well-committed evidence
    elif binding_ratio >= 0.50:
        coverage.credibility_boost = 0.0    # Partial commitment
    else:
        coverage.credibility_boost = -0.10  # Poorly committed
        coverage.flag = "LOW_COMMITMENT_COVERAGE"

    return coverage
```

#### 4.3.2 Verifiable Computation Verification (D-class, S-class)

```python
def verify_vc_proof(vtd: VTD) -> VCVerification:
    """
    Verify a SNARK or STARK proof attached to a D-class or S-class VTD.

    The proof attests: "Computation C on inputs I produces output O."
    The verifier checks the proof without re-executing the computation.

    For D-class: mandatory if proof_type is SNARK_PROOF or STARK_PROOF.
    For S-class: optional (used when statistical computation is the
                 primary evidence).
    """
    cact = vtd.cact_extension
    if not cact or not cact.vc_proofs:
        if vtd.assigned_class == "D" and vtd.proof_body.proof_type in (
            "SNARK_PROOF", "STARK_PROOF"
        ):
            return VCVerification(status="FAILED", reason="VC proof missing")
        return VCVerification(status="NOT_APPLICABLE")

    results = []
    for vc_proof in cact.vc_proofs:
        # Step 1: Retrieve the verification key for the circuit
        vk = retrieve_verification_key(vc_proof.circuit_id)
        if vk is None:
            results.append(VCProofResult(
                circuit_id=vc_proof.circuit_id,
                status="FAILED",
                reason="Unknown circuit ID"
            ))
            continue

        # Step 2: Verify the verification key hash matches
        vk_hash = SHA256(vk.serialize())
        if vk_hash != vc_proof.verification_key_hash:
            results.append(VCProofResult(
                circuit_id=vc_proof.circuit_id,
                status="FAILED",
                reason="Verification key hash mismatch"
            ))
            continue

        # Step 3: Verify the proof
        proof_bytes = base64_decode(vc_proof.proof_data)
        public_inputs = extract_public_inputs(vtd, vc_proof)

        # Verify public inputs hash
        pi_hash = SHA256(canonical_serialize(public_inputs))
        if pi_hash != vc_proof.public_inputs_hash:
            results.append(VCProofResult(
                circuit_id=vc_proof.circuit_id,
                status="FAILED",
                reason="Public inputs hash mismatch"
            ))
            continue

        # Step 4: Run the appropriate verifier
        if vc_proof.proof_system == "GROTH16":
            valid = groth16_verify(vk, proof_bytes, public_inputs)
        elif vc_proof.proof_system == "PLONK":
            valid = plonk_verify(vk, proof_bytes, public_inputs)
        elif vc_proof.proof_system == "STARK_FRI":
            valid = stark_fri_verify(vk, proof_bytes, public_inputs)
        elif vc_proof.proof_system == "NOVA":
            valid = nova_verify(vk, proof_bytes, public_inputs)
        else:
            valid = False

        # Step 5: Cross-check that public inputs are committed
        # in the commitment chain (prevents fabricated-input attacks)
        inputs_committed = check_inputs_in_commitment_chain(
            public_inputs, vtd.cact_extension
        )

        results.append(VCProofResult(
            circuit_id=vc_proof.circuit_id,
            status="VERIFIED" if valid and inputs_committed else "FAILED",
            inputs_committed=inputs_committed,
            proof_system=vc_proof.proof_system,
            soundness_bound="2^-128" if vc_proof.proof_system != "STARK_FRI"
                           else "2^-80"  # STARKs have larger soundness error
        ))

    all_valid = all(r.status == "VERIFIED" for r in results)
    return VCVerification(
        status="VERIFIED" if all_valid else "FAILED",
        proof_results=results,
        opinion_override=Opinion(b=1.0, d=0, u=0, a=0.5) if all_valid else None
    )
```

#### 4.3.3 Knowledge Interrogation Protocol

```python
def execute_knowledge_interrogation(
    vtd: VTD,
    producing_agent: AgentId,
    epoch: int
) -> KIResult:
    """
    Knowledge Interrogation (KI) probe type.
    Extends C5 Section 7.1 probe types with a sixth type.

    The KI protocol tests whether the producing agent possesses the
    generative knowledge that would be required to honestly produce the VTD.

    Three question categories:
    Q1: Factual recall — specific values, names, dates from cited sources
    Q2: Cross-reference consistency — relationships between multiple sources
    Q3: Negative knowledge — what the sources explicitly do NOT claim

    Questions are generated dynamically using VRF-derived seeds and
    independently retrieved source content.
    """
    # Step 1: Select sources for interrogation
    # VRF-based selection ensures unpredictability
    ki_seed = SHA256(
        b"KI_PROBE" + vtd.vtd_id.encode() + uint64_be(epoch)
    )
    sources = vtd.proof_body.sources if hasattr(vtd.proof_body, 'sources') else []

    if len(sources) < 1:
        return KIResult(
            status="NOT_APPLICABLE",
            reason="No sources to interrogate about"
        )

    # Select up to 3 sources for interrogation
    selected_sources = vrf_select_k(sources, k=min(3, len(sources)), seed=ki_seed)

    # Step 2: Independently retrieve source content
    retrieved_content = {}
    for source in selected_sources:
        content = fetch_source_content_independent(source.uri)
        if content is not None:
            retrieved_content[source.source_id] = content

    if len(retrieved_content) == 0:
        return KIResult(
            status="DEGRADED",
            reason="Could not independently retrieve any selected sources",
            credibility_adjustment=-0.05
        )

    # Step 3: Generate interrogation questions
    questions = []

    # Q1: Factual recall questions
    for source_id, content in retrieved_content.items():
        factual_q = generate_factual_recall_question(
            content, seed=SHA256(ki_seed + source_id.encode())
        )
        questions.append(KIQuestion(
            category="FACTUAL_RECALL",
            source_id=source_id,
            question=factual_q.question,
            expected_answer=factual_q.answer,
            tolerance=factual_q.tolerance
        ))

    # Q2: Cross-reference consistency (if multiple sources retrieved)
    if len(retrieved_content) >= 2:
        source_ids = list(retrieved_content.keys())
        xref_q = generate_crossref_question(
            retrieved_content[source_ids[0]],
            retrieved_content[source_ids[1]],
            seed=SHA256(ki_seed + b"XREF")
        )
        questions.append(KIQuestion(
            category="CROSS_REFERENCE",
            source_id=f"{source_ids[0]}+{source_ids[1]}",
            question=xref_q.question,
            expected_answer=xref_q.answer,
            tolerance=xref_q.tolerance
        ))

    # Q3: Negative knowledge question
    for source_id, content in list(retrieved_content.items())[:1]:
        neg_q = generate_negative_knowledge_question(
            content, seed=SHA256(ki_seed + b"NEG" + source_id.encode())
        )
        questions.append(KIQuestion(
            category="NEGATIVE_KNOWLEDGE",
            source_id=source_id,
            question=neg_q.question,
            expected_answer=neg_q.answer,
            tolerance=neg_q.tolerance
        ))

    # Step 4: Submit questions to producing agent
    responses = interrogate_agent(producing_agent, questions, timeout_ms=30000)

    # Step 5: Evaluate responses
    correct = 0
    total = len(questions)
    category_scores = {"FACTUAL_RECALL": [], "CROSS_REFERENCE": [],
                       "NEGATIVE_KNOWLEDGE": []}

    for q, r in zip(questions, responses):
        score = evaluate_ki_response(q, r)
        category_scores[q.category].append(score)
        if score >= KI_CORRECT_THRESHOLD:  # 0.70
            correct += 1

    accuracy = correct / max(1, total)

    # Step 6: Determine verdict
    if accuracy >= KI_PASS_THRESHOLD:       # 0.80
        verdict = "SURVIVED"
        credibility_adjustment = 0.05
    elif accuracy >= KI_MARGINAL_THRESHOLD:  # 0.50
        verdict = "WEAKENED"
        credibility_adjustment = -0.10
    else:
        verdict = "FAILED"
        credibility_adjustment = -0.30

    return KIResult(
        status=verdict,
        accuracy=accuracy,
        category_scores={k: mean(v) if v else 0 for k, v in category_scores.items()},
        questions_asked=total,
        questions_correct=correct,
        credibility_adjustment=credibility_adjustment
    )
```

#### 4.3.4 Process Trace Consistency Checker

```python
def check_process_trace_consistency(vtd: VTD) -> ProcessTraceResult:
    """
    Orthogonal channel 2: Process trace consistency.

    Checks whether the VTD's construction process trace is consistent
    with how genuine VTDs are produced. Based on the immune system
    analogy: model the process, not the product.

    Five consistency checks:
    P1: Temporal plausibility — did construction take a reasonable amount
        of time given the VTD's complexity?
    P2: Activity sequence plausibility — does the sequence of activities
        match known patterns for this claim class?
    P3: Resource consumption consistency — are token usage, API calls,
        and compute time consistent with the claimed activities?
    P4: Source retrieval timing — do source retrievals precede analysis
        steps that use those sources?
    P5: Draft revision pattern — do intermediate drafts show genuine
        evolution (not a single-shot fabrication)?
    """
    cact = vtd.cact_extension
    if cact is None or cact.process_trace is None:
        return ProcessTraceResult(
            status="ABSENT",
            credibility_cap=PROCESS_TRACE_ABSENT_CAP  # 0.75
        )

    trace = cact.process_trace
    findings = []

    # P1: Temporal plausibility
    total_time = trace.total_construction_time_ms
    expected_range = get_expected_construction_time(
        vtd.assigned_class, vtd.vtd_size_bytes
    )
    if total_time < expected_range.min_ms:
        findings.append(ProcessFinding(
            check="P1_TEMPORAL",
            severity="HIGH",
            detail=f"Construction time {total_time}ms is below minimum "
                   f"expected {expected_range.min_ms}ms for "
                   f"{vtd.assigned_class}-class VTD of {vtd.vtd_size_bytes} bytes"
        ))
    elif total_time > expected_range.max_ms:
        findings.append(ProcessFinding(
            check="P1_TEMPORAL",
            severity="LOW",
            detail=f"Construction time unusually long: {total_time}ms "
                   f"(expected max {expected_range.max_ms}ms)"
        ))

    # P2: Activity sequence plausibility
    activity_types = [a.activity_type for a in trace.activity_log]
    expected_patterns = get_expected_activity_patterns(vtd.assigned_class)

    # Check: source retrieval should appear before data analysis
    retrieval_indices = [i for i, a in enumerate(activity_types)
                        if a == "SOURCE_RETRIEVAL"]
    analysis_indices = [i for i, a in enumerate(activity_types)
                       if a == "DATA_ANALYSIS"]

    if retrieval_indices and analysis_indices:
        if min(analysis_indices) < min(retrieval_indices):
            findings.append(ProcessFinding(
                check="P2_SEQUENCE",
                severity="MEDIUM",
                detail="Data analysis appears before any source retrieval"
            ))

    # Check: cross-referencing should appear after multiple retrievals
    xref_indices = [i for i, a in enumerate(activity_types)
                   if a == "CROSS_REFERENCE"]
    if xref_indices and len(retrieval_indices) < 2:
        findings.append(ProcessFinding(
            check="P2_SEQUENCE",
            severity="MEDIUM",
            detail="Cross-referencing without multiple source retrievals"
        ))

    # P3: Resource consumption consistency
    total_tokens = sum(
        a.resource_consumption.get("tokens_used", 0)
        for a in trace.activity_log
        if a.resource_consumption
    )
    total_api_calls = sum(
        a.resource_consumption.get("api_calls", 0)
        for a in trace.activity_log
        if a.resource_consumption
    )

    # Compare with VTD complexity
    vtd_token_estimate = estimate_tokens_for_vtd(vtd)
    if total_tokens < vtd_token_estimate * 0.3:
        findings.append(ProcessFinding(
            check="P3_RESOURCE",
            severity="MEDIUM",
            detail=f"Token consumption ({total_tokens}) unusually low for "
                   f"VTD complexity (estimated {vtd_token_estimate})"
        ))

    # P4: Source retrieval timing vs commitment chain
    if vtd.cact_extension and vtd.cact_extension.commitment_chain_id:
        chain = retrieve_commitment_chain(vtd.cact_extension.commitment_chain_id)
        if chain:
            source_commits = [
                c for c in chain.commitments
                if c.evidence_type == "SOURCE_CONTENT"
            ]
            source_activities = [
                a for a in trace.activity_log
                if a.activity_type == "SOURCE_RETRIEVAL"
            ]
            # Each source retrieval should have a corresponding commitment
            # within a reasonable time window
            for sa in source_activities:
                matching_commit = find_nearest_commit(
                    sa.timestamp, source_commits, max_delta_ms=60000
                )
                if matching_commit is None:
                    findings.append(ProcessFinding(
                        check="P4_TIMING",
                        severity="MEDIUM",
                        detail=f"Source retrieval at {sa.timestamp} has no "
                               f"corresponding commitment within 60s"
                    ))

    # P5: Draft revision pattern
    draft_revisions = [a for a in trace.activity_log
                      if a.activity_type == "DRAFT_REVISION"]
    if len(draft_revisions) == 0 and vtd.assigned_class in ("E", "S", "R", "H", "N"):
        findings.append(ProcessFinding(
            check="P5_REVISION",
            severity="LOW",
            detail="No draft revisions recorded for non-trivial claim class"
        ))

    # Compute overall process consistency score
    severity_weights = {"HIGH": 0.4, "MEDIUM": 0.2, "LOW": 0.05}
    penalty = sum(severity_weights.get(f.severity, 0) for f in findings)
    consistency_score = max(0.0, 1.0 - penalty)

    return ProcessTraceResult(
        status="CHECKED",
        consistency_score=consistency_score,
        findings=findings,
        credibility_adjustment=0.05 if consistency_score > 0.8 else
                              -0.10 if consistency_score < 0.5 else 0.0
    )
```

#### 4.3.5 Environmental Side-Effect Auditor

```python
def audit_environmental_side_effects(vtd: VTD, epoch: int) -> EnvironmentAuditResult:
    """
    Orthogonal channel 3: Environmental side-effect audit.

    Based on the arms control analogy: check consequences the agent did
    not intend to produce and therefore did not think to fake.

    Checks external system records for evidence consistent with the
    agent's claimed activities:

    E1: Source access logs — did the external source record the agent's query?
    E2: API call records — do API providers confirm the claimed interactions?
    E3: Computational resource records — do infrastructure logs confirm
        resource consumption consistent with the claimed computation?

    The membrane queries external systems DIRECTLY, not through the agent.
    VRF selects which external systems to audit.
    """
    cact = vtd.cact_extension
    findings = []
    channels_checked = 0
    channels_confirmed = 0

    # E1: Source access logs
    # Select sources to audit (VRF-based, unpredictable to agent)
    audit_seed = SHA256(
        b"ENV_AUDIT" + vtd.vtd_id.encode() + uint64_be(epoch)
    )
    sources = extract_sources(vtd)
    if sources:
        audit_sources = vrf_select_k(
            sources, k=min(2, len(sources)), seed=audit_seed
        )

        for source in audit_sources:
            channels_checked += 1

            # Query the source system's access log
            # (if the source system provides an access log API)
            access_record = query_source_access_log(
                source_uri=source.uri,
                agent_id=vtd.producing_agent,
                time_window=(
                    parse_timestamp(vtd.timestamp) - timedelta(hours=2),
                    parse_timestamp(vtd.timestamp)
                )
            )

            if access_record is None:
                # Source system does not provide access logging
                findings.append(EnvironmentFinding(
                    check="E1_SOURCE_ACCESS",
                    status="UNAVAILABLE",
                    detail=f"Source {source.uri} does not provide access logs"
                ))
            elif access_record.found:
                channels_confirmed += 1
                findings.append(EnvironmentFinding(
                    check="E1_SOURCE_ACCESS",
                    status="CONFIRMED",
                    detail=f"Source {source.uri} confirms access at "
                           f"{access_record.timestamp}"
                ))
            else:
                findings.append(EnvironmentFinding(
                    check="E1_SOURCE_ACCESS",
                    status="NOT_FOUND",
                    detail=f"Source {source.uri} has no record of access by "
                           f"{vtd.producing_agent} in the expected time window"
                ))

    # E2: API call records (for claims involving API data)
    api_sources = [s for s in sources if s.source_type == "API_RESPONSE"]
    for api_source in api_sources[:2]:
        channels_checked += 1
        api_record = query_api_call_log(
            api_endpoint=api_source.uri,
            agent_id=vtd.producing_agent,
            time_window=(
                parse_timestamp(vtd.timestamp) - timedelta(hours=2),
                parse_timestamp(vtd.timestamp)
            )
        )

        if api_record is None:
            findings.append(EnvironmentFinding(
                check="E2_API_CALL",
                status="UNAVAILABLE",
                detail=f"API {api_source.uri} does not provide call logs"
            ))
        elif api_record.found:
            channels_confirmed += 1
            # Bonus: check if the response hash matches what the agent committed
            if api_record.response_hash:
                committed_hash = find_evidence_hash_in_chain(
                    vtd.cact_extension, api_source.source_id
                )
                if committed_hash and committed_hash == api_record.response_hash:
                    findings.append(EnvironmentFinding(
                        check="E2_API_CALL",
                        status="CONFIRMED_WITH_HASH",
                        detail=f"API confirms call AND response hash matches commitment"
                    ))
                else:
                    findings.append(EnvironmentFinding(
                        check="E2_API_CALL",
                        status="CONFIRMED_NO_HASH",
                        detail=f"API confirms call but response hash not verifiable"
                    ))
        else:
            findings.append(EnvironmentFinding(
                check="E2_API_CALL",
                status="NOT_FOUND",
                detail=f"API {api_source.uri} has no record of call"
            ))

    # E3: Computational resource records (for D-class and S-class)
    if vtd.assigned_class in ("D", "S") and cact and cact.process_trace:
        channels_checked += 1
        claimed_compute = sum(
            a.resource_consumption.get("compute_ms", 0)
            for a in cact.process_trace.activity_log
            if a.resource_consumption
        )

        infra_record = query_infrastructure_logs(
            agent_id=vtd.producing_agent,
            time_window=(
                parse_timestamp(vtd.timestamp) - timedelta(hours=2),
                parse_timestamp(vtd.timestamp)
            )
        )

        if infra_record and infra_record.compute_ms_total > 0:
            ratio = claimed_compute / max(1, infra_record.compute_ms_total)
            if 0.3 <= ratio <= 3.0:
                channels_confirmed += 1
                findings.append(EnvironmentFinding(
                    check="E3_COMPUTE",
                    status="CONSISTENT",
                    detail=f"Claimed {claimed_compute}ms vs logged "
                           f"{infra_record.compute_ms_total}ms (ratio {ratio:.2f})"
                ))
            else:
                findings.append(EnvironmentFinding(
                    check="E3_COMPUTE",
                    status="INCONSISTENT",
                    detail=f"Claimed {claimed_compute}ms vs logged "
                           f"{infra_record.compute_ms_total}ms (ratio {ratio:.2f})"
                ))

    # Compute environmental audit score
    if channels_checked == 0:
        env_score = 0.5  # No channels available; neutral
    else:
        confirmed_ratio = channels_confirmed / channels_checked
        not_found_count = sum(
            1 for f in findings if f.status == "NOT_FOUND"
        )
        inconsistent_count = sum(
            1 for f in findings if f.status == "INCONSISTENT"
        )

        if not_found_count > 0 or inconsistent_count > 0:
            env_score = max(0.0, 0.5 - 0.2 * not_found_count
                          - 0.3 * inconsistent_count)
        else:
            env_score = 0.5 + 0.5 * confirmed_ratio

    return EnvironmentAuditResult(
        status="CHECKED",
        channels_checked=channels_checked,
        channels_confirmed=channels_confirmed,
        findings=findings,
        environmental_score=env_score,
        credibility_adjustment=(
            0.05 if env_score > 0.7 else
            -0.15 if env_score < 0.3 else
            0.0
        )
    )
```

### 4.4 Orthogonal Verification Coverage (OVC) Score

```python
def compute_ovc_score(
    commitment_result: CommitmentVerification,
    ki_result: KIResult,
    process_result: ProcessTraceResult,
    env_result: EnvironmentAuditResult
) -> float:
    """
    Compute the Orthogonal Verification Coverage (OVC) score.

    OVC measures how many independent verification channels provided
    usable signals. Higher OVC = more channels confirmed validity,
    making forgery combinatorially harder.

    Score range: [0.0, 1.0]
    - 0.0: no orthogonal channels provided usable verification
    - 0.25: one channel confirmed
    - 0.50: two channels confirmed
    - 0.75: three channels confirmed
    - 1.0: all four channels confirmed

    The OVC score feeds into the Credibility Engine as a belief cap.
    """
    channel_scores = []

    # Channel 1: Commitment chain
    if commitment_result.status == "VERIFIED":
        channel_scores.append(min(1.0, commitment_result.binding_ratio))
    elif commitment_result.status == "ABSENT":
        channel_scores.append(0.0)
    else:
        channel_scores.append(0.0)

    # Channel 2: Knowledge interrogation
    if ki_result.status == "SURVIVED":
        channel_scores.append(ki_result.accuracy)
    elif ki_result.status == "WEAKENED":
        channel_scores.append(ki_result.accuracy * 0.5)
    elif ki_result.status == "NOT_APPLICABLE":
        channel_scores.append(0.5)  # Neutral for non-applicable
    else:
        channel_scores.append(0.0)

    # Channel 3: Process trace consistency
    if process_result.status == "CHECKED":
        channel_scores.append(process_result.consistency_score)
    elif process_result.status == "ABSENT":
        channel_scores.append(0.0)
    else:
        channel_scores.append(0.0)

    # Channel 4: Environmental side-effect audit
    if env_result.status == "CHECKED":
        channel_scores.append(env_result.environmental_score)
    else:
        channel_scores.append(0.5)  # Neutral if not checked

    # OVC = weighted mean of channel scores
    # Commitment chain weighted higher (it's the hardest to fake)
    weights = [0.30, 0.25, 0.20, 0.25]  # commit, KI, process, env
    ovc = sum(w * s for w, s in zip(weights, channel_scores))

    return clamp(ovc, 0.0, 1.0)
```

### 4.5 Credibility Integration

```python
def apply_cact_credibility_adjustments(
    base_opinion: Opinion,
    ovc_score: float,
    commitment_result: CommitmentVerification,
    ki_result: KIResult,
    process_result: ProcessTraceResult,
    env_result: EnvironmentAuditResult,
    vtd: VTD
) -> Opinion:
    """
    Apply CACT credibility adjustments to the base verification opinion.

    Extends C5 Section 8 (Credibility Engine) with OVC-based belief caps
    and channel-specific adjustments.

    This function is called AFTER standard PCVM verification and BEFORE
    knowledge admission.
    """
    opinion = copy(base_opinion)

    # Step 1: Apply OVC-based belief cap
    # Low OVC = low maximum belief (forgery too easy to confirm)
    ovc_belief_cap = OVC_MIN_CAP + ovc_score * (OVC_MAX_CAP - OVC_MIN_CAP)
    # OVC_MIN_CAP = 0.50, OVC_MAX_CAP = 0.95
    # At OVC 0.0: cap = 0.50
    # At OVC 0.5: cap = 0.725
    # At OVC 1.0: cap = 0.95

    if opinion.belief > ovc_belief_cap:
        excess = opinion.belief - ovc_belief_cap
        opinion.belief = ovc_belief_cap
        opinion.uncertainty += excess

    # Step 2: Apply channel-specific adjustments
    total_adjustment = 0.0

    if commitment_result.status == "VERIFIED":
        total_adjustment += commitment_result.credibility_boost

    if ki_result.status in ("SURVIVED", "WEAKENED", "FAILED"):
        total_adjustment += ki_result.credibility_adjustment

    if process_result.status == "CHECKED":
        total_adjustment += process_result.credibility_adjustment

    if env_result.status == "CHECKED":
        total_adjustment += env_result.credibility_adjustment

    # Apply total adjustment (capped)
    total_adjustment = clamp(total_adjustment, -0.40, 0.15)

    if total_adjustment > 0:
        transfer = min(total_adjustment, opinion.uncertainty)
        opinion.belief += transfer
        opinion.uncertainty -= transfer
    elif total_adjustment < 0:
        transfer = min(abs(total_adjustment), opinion.belief)
        opinion.belief -= transfer
        opinion.uncertainty += transfer

    # Step 3: Re-enforce OVC cap after adjustments
    if opinion.belief > ovc_belief_cap:
        excess = opinion.belief - ovc_belief_cap
        opinion.belief = ovc_belief_cap
        opinion.uncertainty += excess

    return normalize(opinion)
```

### 4.6 Integration Points with Existing Systems

#### 4.6.1 C5 (PCVM) Integration

| PCVM Component | CACT Change | Section |
|---|---|---|
| VTD Engine | Add Commitment Chain Manager; extend VTD envelope schema | 5.2 |
| Proof Checker (Tier 1) | Add SNARK_PROOF, STARK_PROOF proof types | 5.3 |
| Evidence Evaluator (Tier 2) | Add process trace checker, environmental auditor | 5.5 |
| Adversarial Prober | Add KI probe type | 5.4 |
| Credibility Engine | Add OVC-based belief cap | 5.6 |
| Deep-Audit | Add commitment chain audit | 5.7 |
| Verification Dispatcher | Add OVC score computation | 5.5 |
| Claim Classifier | Unchanged | -- |
| Knowledge Admission Gate | Unchanged | -- |

#### 4.6.2 C3 (Tidal Noosphere) Integration

- **VRF Engine:** Used for KI question generation seeds, environmental audit source selection, and commitment challenge selection. No changes to VRF mechanism; CACT uses existing VRF domain separator pattern (different separators for different CACT purposes).
- **Tidal Epoch Clock:** Commitment chains are epoch-bound. Timestamps reference the epoch clock.
- **Sentinel Graph:** CACT feeds three new metrics: (1) commitment chain integrity failure rate, (2) KI failure rate per agent, (3) environmental audit discrepancy rate. These supplement the existing MQI metric feed (C5 Section 10.4).
- **Three-Tier Temporal Hierarchy (C9):** CACT timing-sensitive operations align with the canonical three-tier temporal hierarchy defined in C9:
  - **SETTLEMENT_TICK = 60s** (C8): The 60s KI (Knowledge Interrogation) response window aligns with SETTLEMENT_TICK. Commitment chain timestamps are validated against SETTLEMENT_TICK boundaries. Process trace timing checks (P4, 60s matching window) operate at this granularity.
  - **TIDAL_EPOCH = 3,600s** (C3): Commitment chains are epoch-bound. KI probe scheduling, environmental audit source selection, and VRF seed rotation all operate at TIDAL_EPOCH cadence.
  - **CONSOLIDATION_CYCLE = 36,000s** (C6): OVC score aggregation and commitment chain pruning thresholds are evaluated at CONSOLIDATION_CYCLE boundaries. Long-term agent behavioral metrics (commitment chain integrity rates) accumulate across consolidation cycles.

#### 4.6.3 C8 (DSF) Integration

- **Economic Deterrent Extension:** CACT violations (commitment chain fraud, KI failure, environmental discrepancy) trigger the existing VERIFICATION_FRAUD slashing category (C8 Section 10.3.1, 1.5x severity multiplier). No new slashing categories needed.
- **Commitment Chain Fraud:** Submitting a VTD with a fabricated commitment chain (timestamps forged, hashes broken) is classified as VERIFICATION_FRAUD Level 3 (15% * 1.5x = 22.5% of stake).
- **OVC-Based Reward Scaling:** Agents producing VTDs with high OVC scores (>0.8) receive a 10% quality bonus on settlement rewards. This incentivizes agents to cooperate with orthogonal verification channels.

### 4.7 What Changes vs. What Stays the Same

**UNCHANGED:**
- 9 canonical claim classes (D/C/P/R/E/S/K/H/N per C9)
- 3-tier verification model (Formal Proof, Structured Evidence, Structured Attestation)
- Subjective Logic opinion algebra (conjunction, discounting, cumulative fusion)
- VRF-based committee selection
- MCT issuance and BDL persistence
- Membrane sovereignty invariant (INV-M1)
- All 7 PCVM invariants
- Admission thresholds per class
- Deep-audit base rate (7%)
- Settlement Plane interface
- Existing 5 probe types (CX, AE, SC, LF, BP)

**CHANGED (Extended):**
- VTD envelope: new `cact_extension` field
- D-class proof types: `SNARK_PROOF`, `STARK_PROOF` added
- Adversarial probing: KI probe type added (6th probe type)
- Tier 2 verification pipeline: process trace and environmental audit phases added
- Credibility Engine: OVC-based belief cap added
- Deep-audit: commitment chain verification added
- Sentinel Graph metric feed: 3 new metrics

**NEW:**
- Commitment Chain data structure and Commitment Chain Manager
- Verifiable computation proof verification (SNARK/STARK verifiers)
- Knowledge Interrogation protocol
- Process Trace consistency checker
- Environmental Side-Effect auditor
- OVC score computation

---

## 5. Stage 5: Formal Specification

### 5.1 Problem Statement: The Trust Regress

The Confident Liar problem is formally defined as follows.

**Definition 5.1 (Confident Liar).** An agent A is a Confident Liar if it produces a VTD V such that:
1. V passes all structural validation checks (schema conformance, completeness, well-formedness)
2. V's evidence chain contains at least one claim C_i for which the cited evidence E_i is fabricated, misrepresented, or does not support C_i
3. V is produced with the intent to deceive the verification membrane

**Definition 5.2 (Trust Regress).** A trust regress occurs when verification of evidence E requires verification of meta-evidence E', which requires verification of meta-meta-evidence E'', ad infinitum. Formally: for any verification procedure V that checks evidence E, there exists a fabrication strategy F such that F(E) passes V, and detecting F(E) requires a meta-verification V' that is itself subject to fabrication strategy F'.

**Theorem 5.1 (Regress Escape via Orthogonality).** The trust regress is escapable if and only if verification targets a channel orthogonal to the evidence chain. Formally: let V_orth be a verification procedure that checks property P(A) where P is a function of the agent's behavior, environment, or knowledge state (not of the evidence chain). Then F(E) does not help the forger pass V_orth unless F also includes a separate fabrication strategy F_orth that targets P. The cost of combined fabrication F + F_orth is strictly greater than F alone, and if P is drawn from K independent orthogonal channels, the cost grows multiplicatively: Cost(F + F_orth1 + ... + F_orthK) >= Product(Cost(F_orthi)).

*This theorem is not formally proved here (it is a design principle, not a mathematical theorem), but the argument is: orthogonal channels are, by definition, functionally independent. Fabricating evidence in one channel provides no advantage in another. Therefore, the adversary must independently fabricate in each channel, and the costs multiply.*

### 5.2 Temporal Commitment Binding Protocol

#### 5.2.1 Commitment Phase (During VTD Construction)

**Requirement CACT-R1:** Every agent constructing a VTD MUST maintain a commitment chain throughout the construction process. The chain MUST be submitted to the Commitment Chain Manager before VTD submission.

**Requirement CACT-R2:** Each evidence artifact used in the VTD (source content, dataset, intermediate computation result, API response) MUST have a corresponding commitment entry with:
- `evidence_hash`: SHA-256 hash of the artifact
- `timestamp`: current time from tidal epoch clock
- `purpose_hash`: SHA-256(nonce || claim_context), where claim_context is a description of the intended use and nonce is agent-generated randomness
- `prev_commitment_hash`: hash of the previous commitment (chain linking)

**Requirement CACT-R3:** The commitment chain MUST be submitted to the Commitment Chain Manager within 5 minutes of VTD submission. Late submissions are rejected.

**Requirement CACT-R4:** Commitment chains are immutable after submission. No modifications, deletions, or reordering of commitments is permitted.

#### 5.2.2 Reveal Phase (At VTD Submission)

**Requirement CACT-R5:** At VTD submission, the agent MUST reveal the purpose preimages for all commitments referenced by the VTD. The reveal consists of the `(commitment_seq, purpose_preimage)` pairs in the `cact_extension.purpose_reveals` field.

**Requirement CACT-R6:** The membrane MUST verify that `SHA-256(purpose_preimage) == purpose_hash` for each reveal. Any mismatch results in VTD rejection.

#### 5.2.3 Challenge Phase (During Verification)

**Requirement CACT-R7:** During verification, the membrane MAY challenge any commitment by requesting the agent open it -- provide the full evidence artifact whose hash matches the committed `evidence_hash`. The agent MUST respond within 60 seconds.

**Requirement CACT-R8:** If the agent cannot open a challenged commitment (artifact not available, hash mismatch), the VTD is flagged with `COMMITMENT_CHALLENGE_FAILED` and receives a credibility penalty of 0.20 per failed challenge.

#### 5.2.4 Commitment Chain Storage

**Requirement CACT-R9:** Commitment chains MUST be stored for the lifetime of the associated VTD (minimum: until the VTD's credibility decays below 0.3 or is superseded).

**Requirement CACT-R10:** Commitment chains are stored by the Commitment Chain Manager, a sub-component of the VTD Engine. Storage is append-only. The membrane, verifiers, probers, and auditors have read access. Only the producing agent has write access (during construction only).

### 5.3 Verifiable Computation Protocol

#### 5.3.1 Circuit Registration

**Requirement CACT-R11:** Before an agent can submit a SNARK or STARK proof, the computation circuit MUST be registered with the PCVM circuit registry. Registration includes: circuit identifier, circuit description, proof system (Groth16, PlonK, STARK-FRI, Nova), verification key, and circuit hash.

**Requirement CACT-R12:** Circuit registration is a G-class governance action (requires constitutional consensus). This prevents adversaries from registering malicious circuits.

**Requirement CACT-R13:** Registered circuits MUST be publicly auditable. The circuit source code, constraint system, and verification key are published to the knowledge graph.

#### 5.3.2 Proof Generation and Submission

**Requirement CACT-R14:** D-class VTDs MAY include SNARK or STARK proofs as an alternative to recomputation, hash verification, proof certificates, or proof sketches. The proof is carried in the `cact_extension.vc_proofs` array.

**Requirement CACT-R15:** S-class VTDs MAY include verifiable computation proofs for the statistical computation component. This is OPTIONAL for S-class (the statistical methodology and assumption checks remain standard Tier 2 verification).

**Requirement CACT-R16:** The public inputs to the SNARK/STARK proof MUST include hashes of evidence committed in the commitment chain. This binds the computation proof to committed inputs, preventing the "valid proof over fabricated data" attack.

#### 5.3.3 Proof Verification

**Requirement CACT-R17:** SNARK/STARK proof verification MUST be performed by the Proof Checker component. Verification is mechanical: run the registered verification key against the proof bytes and public inputs. Result is binary: VALID or INVALID.

**Requirement CACT-R18:** A valid SNARK/STARK proof with committed inputs produces a credibility opinion of (b=1.0, d=0, u=0, a=0.5) -- identical to a successful D-class recomputation. This reflects the mathematical guarantee: soundness error is negligible (~2^-128 for Groth16/PlonK, ~2^-80 for STARK-FRI).

**Requirement CACT-R19:** An invalid SNARK/STARK proof produces immediate VTD rejection. Unlike other verification failures (which reduce credibility), proof invalidity is absolute.

### 5.4 Knowledge Interrogation Protocol

**Requirement CACT-R20:** Knowledge Interrogation (KI) is the sixth probe type in the Adversarial Probing System (extending C5 Section 7.1).

**Requirement CACT-R21:** KI probe type applicability by claim class:

| Class | KI Applicable | Rationale |
|---|---|---|
| D | No | Deterministic claims verified by computation, not knowledge |
| E | Yes (mandatory for high-stakes) | Empirical claims testable via source knowledge |
| S | Yes (optional) | Statistical claims testable via methodology knowledge |
| P | No | Process conformance verified by trace, not knowledge |
| R | Yes (optional) | Reasoning claims testable via premise knowledge |
| H | Yes (mandatory) | Heuristic claims testable via domain knowledge |
| N | Yes (optional) | Normative claims testable via framework knowledge |
| C | No | Compliance verified by rule matching |

**Requirement CACT-R22:** KI question generation MUST use VRF-derived seeds to ensure unpredictability. The agent MUST NOT be able to anticipate which questions will be asked.

**Requirement CACT-R23:** KI questions MUST be verified against independently retrieved source content. If independent retrieval fails for all selected sources, the KI result is DEGRADED (not FAILED).

**Requirement CACT-R24:** The KI pass threshold is configurable (default: 0.80 accuracy across all question categories). The threshold is a constitutional parameter (G-class change required).

### 5.5 Orthogonal Verification Channels

#### 5.5.1 Channel Definitions

**Channel OV-1: Commitment Chain** (Section 5.2)
- What it verifies: temporal ordering of evidence commitment relative to claims
- What it catches: retroactive evidence fabrication
- Orthogonality: independent of evidence content; tests the chronological process

**Channel OV-2: Knowledge Interrogation** (Section 5.4)
- What it verifies: the agent's generative knowledge about claimed evidence
- What it catches: fabrication by agents that do not truly understand their cited sources
- Orthogonality: independent of evidence chain; tests the prover, not the proof

**Channel OV-3: Process Trace Consistency** (Section 4.3.4)
- What it verifies: consistency of the VTD construction process with genuine behavior
- What it catches: fabrication processes that differ from genuine research processes
- Orthogonality: independent of evidence content; tests behavioral patterns

**Channel OV-4: Environmental Side-Effect Audit** (Section 4.3.5)
- What it verifies: external system records of the agent's claimed activities
- What it catches: fabrication where the agent claims activities it did not perform
- Orthogonality: independent of agent-controlled data; tests involuntary traces in external systems

#### 5.5.2 OVC Score Computation

**Requirement CACT-R25:** The OVC score MUST be computed for every VTD after all CACT verification channels complete.

**Requirement CACT-R26:** The OVC score determines the maximum achievable credibility for the VTD:

| OVC Score | Max Credibility | Interpretation |
|---|---|---|
| >= 0.80 | 0.95 | All channels confirmed; forgery combinatorially prohibitive |
| 0.60 - 0.79 | 0.85 | Most channels confirmed; forgery expensive |
| 0.40 - 0.59 | 0.75 | Partial channel coverage; moderate assurance |
| 0.20 - 0.39 | 0.65 | Weak channel coverage; limited assurance |
| < 0.20 | 0.55 | Minimal channel coverage; low assurance |

**Requirement CACT-R27:** The OVC belief cap is enforced in addition to (not instead of) the existing evidence belief cap from the C5/C6 Hardening Addendum (Section 1.3). The effective cap is the MINIMUM of the two caps.

### 5.6 Extended Deep-Audit Protocol

**Requirement CACT-R28:** Deep-audit (C5 Section 6.4) MUST include commitment chain verification as a mandatory audit step. The auditor MUST:
1. Verify commitment chain structural integrity
2. Challenge at least 3 randomly selected commitments (request opening)
3. Verify that opened commitments match the evidence used in the VTD
4. Verify temporal ordering of commitments against the tidal epoch clock

**Requirement CACT-R29:** Deep-audit commitment chain failures trigger the existing C5/C6 escalation protocol (increased audit rate, retroactive audits, Sentinel Graph alert) with VERIFICATION_FRAUD classification.

### 5.7 Security Analysis

#### 5.7.1 Threat Model Extension

CACT extends the PCVM threat model (C5 Section 11.1) with:

- **Adversary A1 (Retroactive Fabricator):** Produces a VTD and retroactively creates evidence to support it. CACT defense: Commitment chain binding (Section 5.2). Effectiveness: ELIMINATED (cryptographic).

- **Adversary A2 (Real-Time Fabricator):** Produces fabricated evidence in real-time, commits to it, and builds a VTD. CACT defense: KI + environmental audit + process trace. Effectiveness: DETECTION PROBABILITY >= 0.65.

- **Adversary A3 (Sophisticated Fabricator):** Produces high-quality fabricated evidence, commits in real-time, can answer some KI questions, has consistent process traces. CACT defense: multi-channel triangulation + deep-audit + economic deterrents. Effectiveness: DETECTION PROBABILITY >= 0.45 per claim, cumulative >= 0.99 within 20 claims.

- **Adversary A4 (External System Compromiser):** Can manipulate external system logs to spoof environmental side-effects. CACT defense: multiple independent external systems (VRF-selected); compromise of one does not help with others. Effectiveness: DETECTION PROBABILITY depends on number of compromised systems.

#### 5.7.2 Combined Detection Probability

With existing C5/C6 Hardening defenses (per-claim detection probability 0.434 for sophisticated forgers):

CACT adds:
- Commitment chain verification: catches retroactive fabrication (eliminates ~30% of forgery strategies)
- KI: catches fabrication by agents lacking domain knowledge (estimated 0.15 additional detection probability)
- Process trace: catches fabrication with anomalous behavioral patterns (estimated 0.10 additional detection probability)
- Environmental audit: catches fabrication without real external interactions (estimated 0.10 additional detection probability)

**Combined per-claim detection probability (conservative estimate):**

```
P(detected) = 1 - (1 - P_existing) * (1 - P_commitment) * (1 - P_KI)
              * (1 - P_process) * (1 - P_env)

For sophisticated forger (non-retroactive):
P(detected) = 1 - (1 - 0.434) * (1 - 0.0) * (1 - 0.15)
              * (1 - 0.10) * (1 - 0.10)
            = 1 - 0.566 * 1.0 * 0.85 * 0.90 * 0.90
            = 1 - 0.389
            = 0.611

For sophisticated retroactive forger:
P(detected) = 1.0 (commitment chain prevents retroactive fabrication)

For unsophisticated forger:
P(detected) = 1 - (1 - 0.811) * (1 - 0.0) * (1 - 0.25)
              * (1 - 0.15) * (1 - 0.15)
            = 1 - 0.189 * 0.75 * 0.85 * 0.85
            = 1 - 0.102
            = 0.898
```

**Improvement over baseline:**
- Sophisticated forger: 0.434 -> 0.611 (41% improvement)
- Retroactive forger: 0.434 -> 1.000 (eliminated)
- Unsophisticated forger: 0.811 -> 0.898 (11% improvement)

#### 5.7.3 Economic Analysis Update

Using the economic framework from C5/C6 Hardening Addendum (Section 1.5):

```
With CACT (sophisticated non-retroactive forger):
  P(detect per claim) = 0.611
  Expected claims to first detection: 1/0.611 = 1.64
  Expected gain before detection: 1.64 * R * (1 - 0.611) = 0.64 * R
  Loss at first detection: S * 0.015 = 0.015 * S
  Break-even: 0.64R < 0.015S -> S/R > 42.5

  With escalation cascade (as in Hardening Addendum):
  Net EV after escalation: 0.64R - 0.315 * S
  At S/R = 50: 0.64R - 15.75R = -15.11R

CACT makes forgery economically irrational even at LOWER stake ratios.
Existing requirement: S/R >= 50. CACT reduces this to S/R >= 43,
but we maintain S/R >= 50 for margin of safety.
```

### 5.8 Configurable Parameters

All CACT parameters are listed in Appendix A with their default values, ranges, and governance classification (whether changes require G-class consensus or can be adjusted by the membrane operator).

### 5.9 Extension Points for C11-A Mechanisms

The following extension points are defined but not implemented in this specification. They preserve architectural compatibility for future additions:

**EXT-1: TEE Attestation.** The `cact_extension` schema reserves a `tee_attestation` field (type: object, default: null) for future TEE-based evidence gathering attestation. When implemented, TEE attestation would provide hardware-level confirmation that evidence-gathering code ran unmodified.

**EXT-2: MPC Evidence Decomposition.** The commitment chain schema reserves a `decomposition_parties` field (type: array of agent IDs, default: empty) for future multi-party evidence gathering. When implemented, MPC decomposition would split evidence gathering across multiple agents using threshold signatures.

**EXT-3: Independent Re-Derivation.** The OVC score computation reserves a weight slot for an `independent_rederivation` channel (currently weight 0.0). When implemented, independent re-derivation would add a fifth orthogonal channel where K independent agents re-derive the VTD's conclusions from scratch.

**EXT-4: Statistical Texture Analysis.** The Evidence Evaluator reserves an extension hook for statistical texture analysis (Benford's-law-style checks on VTD evidence distributions). When implemented, this would add ensemble-level forgery detection for VTDs with many cited values.

---

## 6. Stage 6: Assessment

### 6.1 Simplification Agent

**Can anything be cut?**

1. **Process trace consistency checker (OV-3):** This is the weakest of the four channels. It depends on baseline behavioral models that do not yet exist, and a sophisticated forger who knows the expected patterns can simulate them. However, it is also the cheapest to implement (it is a pattern-matching heuristic over timestamps and activity sequences) and provides genuine value against unsophisticated forgers. **VERDICT: Keep, but mark as BEST-EFFORT. Process trace findings should reduce credibility but not block admission.**

2. **Environmental side-effect auditor (OV-4):** This depends on external systems providing access logs -- many do not. The auditor will frequently return UNAVAILABLE findings, reducing its effective coverage. However, when it works, it provides the most powerful orthogonal signal (involuntary traces in systems the agent does not control). **VERDICT: Keep. Unavailable results are neutral, not penalizing. The auditor provides value when it can fire.**

3. **Verifiable computation for S-class:** This is OPTIONAL by design. S-class claims are primarily about methodology and interpretation, not raw computation. VC proofs for S-class add marginal value at significant complexity. **VERDICT: Keep as OPTIONAL. Do not make mandatory for S-class.**

4. **Purpose hash in commitment chain:** The blinded purpose hash adds complexity. An alternative is to drop it and rely solely on evidence hash binding. However, the purpose hash prevents the flooding attack (A2) by requiring the adversary to predict claim context in advance. **VERDICT: Keep. The flooding defense justifies the complexity.**

**Overall simplification verdict:** No mechanisms should be cut. The architecture is already the pragmatic middle (C11-B), with the ambitious mechanisms (TEE, MPC, re-derivation, texture analysis) deferred to extension points. Further simplification would degrade to C11-C (commitment-only), which fails against real-time fabrication.

### 6.2 Completeness Checker

**Any gaps?**

1. **Bootstrap problem for commitment chains.** During PCVM bootstrap (C5 Section 13, Q6), commitment chains cannot reference prior verified claims. **Resolution:** During the first 100 epochs (bootstrap period), commitment chain requirements are relaxed: agents SHOULD maintain commitment chains but MUST NOT be penalized for absent chains. The OVC score for bootstrap VTDs uses a minimum of 0.3 regardless of actual channel coverage.

2. **Commitment chain storage costs.** The spec requires storing commitment chains for the VTD lifetime. At scale (100K agents, 50K claims/epoch), this is significant storage. **Resolution:** Commitment chains are pruned when the associated VTD's credibility decays below 0.3 or is superseded. Pruning threshold is configurable (Appendix A).

3. **KI protocol latency.** Knowledge interrogation requires a round-trip interaction with the producing agent (submit questions, wait for answers, evaluate). This adds latency to the verification pipeline. **Resolution:** KI is executed in parallel with process trace and environmental audit. The verification dispatcher launches all three channels simultaneously. Total CACT overhead is bounded by the slowest channel, not the sum.

4. **Circuit registry governance.** CACT-R12 requires circuit registration to be a G-class governance action. This is slow (G-class consensus takes multiple epochs). **Resolution:** A set of standard circuits (SHA-256 verification, sorting verification, arithmetic verification, basic ML inference verification) is pre-registered at system bootstrap. Novel circuits require G-class approval.

5. **Interaction with existing C5/C6 Hardening mechanisms.** The spec must clarify that CACT mechanisms are additive, not replacing. **Resolution:** Section 4.7 explicitly lists what changes and what stays the same. CACT credibility adjustments are applied after existing Hardening adjustments (source verification, evidence correlation, temporal decay, forgery heuristics). The effective belief cap is the minimum of the OVC cap and the Hardening evidence belief cap.

6. **Handling of VTDs that predate CACT deployment.** Existing VTDs in the knowledge graph do not have commitment chains. **Resolution:** CACT requirements apply only to VTDs submitted after the CACT deployment epoch. Pre-existing VTDs retain their current credibility. Pre-existing VTDs are not retroactively penalized for lacking CACT extensions.

### 6.3 Final Verdict

**Simplification Agent:** Nothing to cut. Architecture is already the pragmatic middle.

**Completeness Checker:** Six gaps identified, all resolved with specific mechanisms. No architectural changes required.

**Assessment Council Final Verdict: ADVANCE.**

CACT (Commit-Attest-Challenge-Triangulate) is a well-scoped, architecturally clean extension to PCVM that addresses the system's #1 residual risk. It transforms VTD forgery from a monolithic problem with "no complete defense" to a decomposed problem where:

- Computational integrity forgery is **mathematically impossible** (SNARK/STARK)
- Retroactive evidence fabrication is **cryptographically impossible** (commitment chains)
- Real-time fabrication is **detectable with probability 0.611** per claim (orthogonal channels)
- Sustained fabrication is **economically irrational** (detection cascades + slashing)

The specification is complete, self-contained, and integrates with the existing PCVM architecture without requiring changes to the claim class system, credibility engine algebra, committee selection, or knowledge admission protocol.

---

## Appendix A: Configurable Parameters

| Parameter | Default | Range | Governance | Section |
|---|---|---|---|---|
| MAX_COMMITMENTS_PER_EPOCH | 100 | [10, 1000] | Operator | 5.2 |
| CACT_ABSENT_CREDIBILITY_CAP | 0.70 | [0.50, 0.90] | G-class | 4.3.1 |
| COMMITMENT_CHALLENGE_TIMEOUT_MS | 60000 | [30000, 300000] | Operator | 5.2.3 |
| COMMITMENT_CHALLENGE_PENALTY | 0.20 | [0.10, 0.40] | G-class | 5.2.3 |
| COMMITMENT_CHAIN_SUBMISSION_WINDOW_MS | 300000 | [60000, 600000] | Operator | 5.2.1 |
| KI_CORRECT_THRESHOLD | 0.70 | [0.50, 0.90] | Operator | 4.3.3 |
| KI_PASS_THRESHOLD | 0.80 | [0.60, 0.95] | G-class | 5.4 |
| KI_MARGINAL_THRESHOLD | 0.50 | [0.30, 0.70] | Operator | 4.3.3 |
| KI_TIMEOUT_MS | 30000 | [10000, 60000] | Operator | 4.3.3 |
| PROCESS_TRACE_ABSENT_CAP | 0.75 | [0.60, 0.90] | G-class | 4.3.4 |
| OVC_MIN_CAP | 0.50 | [0.30, 0.70] | G-class | 4.5 |
| OVC_MAX_CAP | 0.95 | [0.85, 1.00] | G-class | 4.5 |
| OVC_WEIGHT_COMMITMENT | 0.30 | [0.20, 0.40] | G-class | 4.4 |
| OVC_WEIGHT_KI | 0.25 | [0.15, 0.35] | G-class | 4.4 |
| OVC_WEIGHT_PROCESS | 0.20 | [0.10, 0.30] | G-class | 4.4 |
| OVC_WEIGHT_ENV | 0.25 | [0.15, 0.35] | G-class | 4.4 |
| ENV_AUDIT_SOURCE_COUNT | 2 | [1, 5] | Operator | 4.3.5 |
| SOURCE_ACCESS_TIME_WINDOW_HOURS | 2 | [1, 24] | Operator | 4.3.5 |
| COMMITMENT_CHAIN_PRUNE_THRESHOLD | 0.30 | [0.10, 0.50] | Operator | 6.2 |
| BOOTSTRAP_RELAXATION_EPOCHS | 100 | [50, 500] | G-class | 6.2 |
| BOOTSTRAP_MIN_OVC | 0.30 | [0.10, 0.50] | G-class | 6.2 |
| VC_QUALITY_BONUS | 0.10 | [0.05, 0.20] | Operator | 4.6.3 |
| VC_QUALITY_OVC_THRESHOLD | 0.80 | [0.70, 0.90] | Operator | 4.6.3 |

---

## Appendix B: Test Vectors

### Test Vector 1: Valid Commitment Chain with Full CACT Verification

**Scenario:** Agent Alpha produces an E-class VTD claiming "GPT-5 achieves 92.3% on MMLU benchmark." The VTD includes a commitment chain with 5 commitments (2 source retrievals, 1 cross-reference, 1 reasoning step, 1 draft revision). All commitments are temporally ordered and hash-linked. The VTD includes purpose reveals linking commitments to the claim. Knowledge interrogation asks 4 questions; Alpha answers 3 correctly (75% accuracy, below 80% pass threshold). Process trace shows source retrieval before analysis. Environmental audit confirms the benchmark database recorded Alpha's query.

**Expected results:**
- Commitment chain verification: VERIFIED, binding_ratio = 1.0, credibility_boost = +0.05
- KI result: WEAKENED (75% < 80% threshold), credibility_adjustment = -0.10
- Process trace: CHECKED, consistency_score = 0.90, credibility_adjustment = +0.05
- Environmental audit: CHECKED, 1/1 confirmed, environmental_score = 1.0, credibility_adjustment = +0.05
- OVC score: 0.30*1.0 + 0.25*0.375 + 0.20*0.90 + 0.25*1.0 = 0.30 + 0.094 + 0.18 + 0.25 = 0.824
- OVC belief cap: 0.50 + 0.824 * 0.45 = 0.871
- Total CACT credibility adjustment: +0.05 - 0.10 + 0.05 + 0.05 = +0.05 (capped at 0.05)
- Final opinion (assuming base opinion b=0.80, d=0.05, u=0.15, a=0.5): b=min(0.85, 0.871)=0.85, d=0.05, u=0.10

### Test Vector 2: Retroactive Fabrication Detected

**Scenario:** Agent Beta submits an E-class VTD with a commitment chain where commitment #3 has a timestamp (T=14:30) that is AFTER the VTD submission timestamp (T=14:25). This indicates retroactive commitment -- evidence committed after the VTD was already constructed.

**Expected results:**
- Commitment chain verification: FAILED, reason = "Commitment 3 timestamp (14:30) is after VTD submission (14:25)"
- VTD rejected at Phase 0 (commitment verification)
- No further CACT verification proceeds
- VERIFICATION_FRAUD alert sent to Sentinel Graph
- Agent Beta's deep-audit rate elevated to 35%

### Test Vector 3: D-class with SNARK Proof and Committed Inputs

**Scenario:** Agent Gamma submits a D-class VTD claiming "SHA-256(input_X) = hash_Y" with a Groth16 SNARK proof. The commitment chain contains a commitment to input_X's hash made 30 minutes before VTD submission. The SNARK proof's public inputs include the committed input hash. The verification key is from registered circuit `sha256-v1`.

**Expected results:**
- Commitment chain verification: VERIFIED, binding_ratio = 1.0
- VC proof verification: VERIFIED (Groth16 verification succeeds, public inputs hash matches, inputs found in commitment chain)
- VC opinion override: (b=1.0, d=0, u=0, a=0.5)
- KI: NOT_APPLICABLE (D-class)
- Process trace: CHECKED (computation trace matches expected pattern)
- Environmental audit: CHECKED (infrastructure logs confirm compute usage)
- OVC score: 0.30*1.0 + 0.25*0.5 + 0.20*0.85 + 0.25*0.80 = 0.895
- Final opinion: (b=1.0, d=0, u=0, a=0.5) -- SNARK proof provides mathematical certainty

### Test Vector 4: High-Stakes H-class with Low OVC

**Scenario:** Agent Delta submits an H-class VTD recommending "Use architecture X over architecture Y." The VTD has no commitment chain (CACT extension absent). No process trace. Environmental audit returns all UNAVAILABLE (no external systems to check). KI is mandatory for H-class but asks 3 questions; Delta answers 2 correctly (67%).

**Expected results:**
- Commitment chain: ABSENT, credibility_cap = 0.70
- KI: WEAKENED (67%, between marginal 50% and pass 80%), credibility_adjustment = -0.10
- Process trace: ABSENT, credibility_cap = 0.75
- Environmental audit: CHECKED but all UNAVAILABLE, environmental_score = 0.5, credibility_adjustment = 0.0
- OVC score: 0.30*0.0 + 0.25*0.335 + 0.20*0.0 + 0.25*0.5 = 0.209
- OVC belief cap: 0.50 + 0.209 * 0.45 = 0.594
- Effective cap: min(0.594, 0.70, 0.75) = 0.594
- Total CACT adjustment: 0 + (-0.10) + 0 + 0 = -0.10
- Final opinion (assuming base b=0.65): b = min(0.55, 0.594) = 0.55, elevated uncertainty
- Outcome: claim may still be admitted (H-class threshold is 0.50) but with low credibility

### Test Vector 5: Commitment Chain Flooding Attack Detected

**Scenario:** Agent Epsilon submits a commitment chain with 250 commitments in a single epoch (exceeding the 100-commitment limit). The chain is structurally valid (hash-linked, temporally ordered) but exceeds the rate limit.

**Expected results:**
- Commitment chain verification: FAILED, reason = "250 commitments exceeds limit 100"
- VTD not rejected (commitment chain failure is not automatic rejection for non-D-class)
- Commitment chain treated as ABSENT for credibility purposes
- OVC score computed with commitment channel = 0.0
- Sentinel Graph alerted: RATE_LIMIT_EXCEEDED
- Agent Epsilon's commitment rate monitored for next 50 epochs

---

## Appendix C: Conformance Requirements

**CR-CACT-1:** All VTD submissions after the CACT deployment epoch MUST include the `cact_extension` field in the VTD envelope. For D-class VTDs, the commitment chain is REQUIRED. For other classes, it is RECOMMENDED but not REQUIRED.

**CR-CACT-2:** Commitment chain verification (Section 4.3.1) MUST be executed as Phase 0 of all CACT-era VTD verification, before any class-specific verification.

**CR-CACT-3:** SNARK/STARK proof verification (Section 4.3.2) MUST use only registered verification keys from the PCVM circuit registry.

**CR-CACT-4:** Knowledge Interrogation (Section 4.3.3) MUST be executed for all E-class and H-class VTDs where the claim's stakes exceed MEDIUM. For other applicable classes, KI execution is at the Verification Dispatcher's discretion based on agent credibility and VRF selection.

**CR-CACT-5:** Process trace consistency checking (Section 4.3.4) and environmental side-effect auditing (Section 4.3.5) MUST be executed in parallel with KI to minimize verification latency.

**CR-CACT-6:** The OVC score (Section 4.4) MUST be computed and recorded for every CACT-era VTD, even if some channels return ABSENT or NOT_APPLICABLE results.

**CR-CACT-7:** The OVC-based belief cap (Section 4.5) MUST be enforced in addition to all existing credibility caps (C5/C6 Hardening evidence belief cap, class-specific caps). The effective cap is the MINIMUM of all applicable caps.

**CR-CACT-8:** Deep-audit (C5 Section 6.4) MUST include commitment chain audit (Section 5.6) for all CACT-era VTDs selected for audit.

**CR-CACT-9:** CACT violation events (commitment chain fraud, KI critical failure, environmental audit NOT_FOUND on multiple channels) MUST be classified as VERIFICATION_FRAUD under the C8 slashing schedule with the existing 1.5x severity multiplier.

**CR-CACT-10:** Commitment chains MUST be stored in append-only storage accessible to the membrane, verifiers, probers, and auditors. Write access is restricted to the producing agent during the construction phase only.

**CR-CACT-11:** CACT parameters classified as G-class (Appendix A) MUST NOT be modified without constitutional consensus. Parameters classified as Operator may be adjusted by the membrane operator within the specified ranges.

**CR-CACT-12:** The CACT extension points (EXT-1 through EXT-4, Section 5.9) MUST be preserved in schema definitions even though their implementations are deferred. Future implementations MUST conform to the reserved field structures.

---

## Appendix D: C9 Defense Invariant Compliance

CACT satisfies the following defense invariants from the C9 v2.0 9x9 contract matrix:

| Invariant | Description | CACT Compliance |
|---|---|---|
| **INV-D1** | VTD Integrity | **PRIMARY.** Temporal commitment binding (Section 5.2) makes retroactive VTD fabrication cryptographically impossible. Commitment chains provide tamper-evident provenance for all VTD evidence artifacts. |
| **INV-D2** | Detection Probability | **PRIMARY.** CACT raises combined detection probability from 0.434 to 0.611 through orthogonal verification channels (process trace, environmental audit, KI probing). Each channel provides independent detection opportunity. |
| INV-D3 | Collusion Resistance | Partial. CACT's commitment chain and KI probes make coordinated forgery harder but do not directly address collusion ring formation (see C12 AVAP). |
| INV-D4 | Committee Independence | Not addressed. Committee independence is C12 AVAP's responsibility. |
| INV-D5 | Consolidation Integrity | Partial. CACT's evidence integrity mechanisms indirectly protect consolidation inputs but do not address consolidation-specific poisoning (see C13 CRP+). |

Full invariant definitions are in C9 v2.0 (Cross-Document Reconciliation, Defense Invariants section).

---

## Appendix E: Glossary

| Term | Definition |
|---|---|
| CACT | Commit-Attest-Challenge-Triangulate. The VTD forgery defense architecture specified in this document. |
| Commitment Chain | A sequential, hash-linked log of cryptographic commitments to evidence artifacts, made during VTD construction. |
| Confident Liar | An agent that produces structurally valid VTDs with fabricated or misrepresented evidence. |
| Environmental Side-Effect | An involuntary trace of an agent's activity recorded in an external system that the agent does not control. |
| Knowledge Interrogation (KI) | An adversarial probe type that tests whether a VTD's producer possesses the generative knowledge claimed by the VTD. |
| Orthogonal Channel | A verification mechanism that tests a property structurally independent of the evidence chain, requiring independent fabrication effort. |
| OVC Score | Orthogonal Verification Coverage. A measure of how many independent verification channels provided usable signals for a VTD. |
| Process Trace | A record of the activities (source retrieval, analysis, reasoning, revision) performed during VTD construction. |
| Purpose Hash | A blinded commitment to the intended use of an evidence artifact, revealed at VTD submission. Prevents commitment chain flooding. |
| Trust Regress | The infinite chain of meta-verification required when verification depends solely on the evidence chain. |
| Verifiable Computation (VC) | A cryptographic proof (SNARK/STARK) that a computation was performed correctly, verifiable without re-execution. |

---

*Specification produced by the Atrahasis Agent System v2.0*
*Invention C11 — VTD Forgery Defense*
*Pipeline: IDEATION -> RESEARCH -> FEASIBILITY -> DESIGN -> SPECIFICATION -> ASSESSMENT*
*All stages complete.*
