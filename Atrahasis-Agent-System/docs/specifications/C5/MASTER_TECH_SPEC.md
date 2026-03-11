# Proof-Carrying Verification Membrane (PCVM)

## Master Technical Specification

**Version:** 2.0.0
**Date:** 2026-03-10
**Invention ID:** C5
**System:** Atrahasis Agent System v2.0
**Status:** SPECIFICATION COMPLETE (Unified v2.0)
**Assessment Council Verdict:** CONDITIONAL_ADVANCE (Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10)
**Normative References:** RFC 2119, RFC 9381 (ECVRF), JSON Schema Draft 2020-12, Josang Subjective Logic (2016), RFC 3339, RFC 8032 (Ed25519), FIPS 180-4 (SHA-256), Groth16, FRI (STARK), Pedersen Commitments, Fujisaki-Suzuki 2007 (LRS)
**Supersedes:** C5 MASTER_TECH_SPEC v1.0.0, C5 PATCH_ADDENDUM v1.1, C10 Hardening Addendum (C5-relevant portions), C11 CACT v1.0.0, C12 AVAP v1.0.0
**Cross-references:** C3 (Tidal Noosphere v1.0), C4 (ASV v1.0), C8 (DSF v2.0), C9 (Reconciliation), C11 (VTD Forgery Defense / CACT v1.0 — integrated in Sections 8, 12), C12 (Collusion Defense / AVAP v1.0 — integrated in Section 13)

---

## Abstract

The Proof-Carrying Verification Membrane (PCVM) is a verification architecture for multi-agent AI systems that replaces replication-based consensus with graduated proof-carrying verification. In conventional multi-agent verification, every claim is verified by having multiple independent agents re-execute the computation and vote on agreement -- an approach that scales poorly, cannot handle non-deterministic outputs, and checks only "did I get the same answer?" rather than "is this answer well-supported?" PCVM introduces a different paradigm: every agent output carries a Verification Trace Document (VTD), a structured, machine-checkable artifact whose form and depth vary by claim class. The verification membrane checks the VTD rather than re-executing the computation.

PCVM defines nine claim classes organized into three verification tiers. Tier 1 (D-class deterministic, C-class compliance) carries machine-checkable formal proofs with genuinely sublinear verification cost (0.1x-0.35x of replication). Tier 2 (E-class empirical, S-class statistical, P-class process, R-class reasoning, K-class knowledge consolidation) carries structured evidence chains verified through completeness checking and selective adversarial probing (0.5x-1.2x of replication). Tier 3 (H-class heuristic, N-class normative) carries structured attestations verified through adversarial probing and expert committee review (1.0x-2.0x of replication -- an honest admission that these claims are harder to verify, not easier). Credibility is represented using Josang's Subjective Logic opinion tuples and propagated through claim dependency graphs. The membrane assigns claim classifications (agents propose, the membrane decides), selects adversarial probers via VRF independently of verification committees, and subjects 7% of all passed claims to random deep-audit via full replication as a deterrence mechanism.

System-level verification cost is approximately 0.83x of universal replication (a 17% reduction), calculated from the weighted cost across all nine claim classes including deep-audit overhead. This modest direct savings reflects the honest cost of Tier 3 claims (H-class and N-class), which consume 1.5x-2.0x of replication cost and constitute approximately 20% of claim volume. The deeper cost advantage emerges through downstream trust propagation: when verified claims are cited by subsequent claims, the citing claims inherit credibility without triggering re-verification of their dependencies. Under the assumption that each verified claim is cited an average of 3 times (a figure that requires empirical validation during pilot deployment), effective system cost drops to approximately 0.40x-0.60x of universal replication. The 40-60% figure is therefore a projected long-term savings contingent on citation density, not a guaranteed per-epoch reduction.

PCVM v2.0 integrates two defense-in-depth subsystems that address the CRITICAL residual risks identified in v1.0:

- **CACT (Commit-Attest-Challenge-Triangulate):** A four-mechanism VTD forgery defense that escapes the infinite trust regress by shifting verification from the evidence chain to orthogonal channels that the forger cannot control. Temporal commitment binding makes retroactive fabrication cryptographically impossible. Verifiable computation (SNARK/STARK) makes computational integrity mathematically verifiable. Knowledge interrogation tests the producing agent's generative understanding. Orthogonal verification channels require simultaneous fabrication across structurally independent systems.

- **AVAP (Anonymous Verification with Adaptive Probing):** A five-mechanism anti-collusion architecture that combines structural prevention (anonymous VRF self-selection committees, sealed commit-reveal opinions), active detection (class-stratified honeypot claims, conditional behavioral analysis), and economic deterrence (collusion deterrence payments with zero-knowledge reporting). AVAP renders collusion rings structurally difficult to form, statistically detectable within 25 epochs, and economically irrational to sustain beyond 10 epochs.

---

## Table of Contents

1. [Introduction and Motivation](#1-introduction-and-motivation)
2. [Background and Related Work](#2-background-and-related-work)
3. [Architectural Overview](#3-architectural-overview)
4. [The Graduated VTD Model](#4-the-graduated-vtd-model)
5. [Claim Classification System](#5-claim-classification-system)
6. [Verification Protocols](#6-verification-protocols)
7. [Adversarial Probing System](#7-adversarial-probing-system)
8. [CACT: Commit-Attest-Challenge-Triangulate](#8-cact-commit-attest-challenge-triangulate)
9. [Credibility Engine](#9-credibility-engine)
10. [Knowledge Admission](#10-knowledge-admission)
11. [Integration Architecture](#11-integration-architecture)
12. [Defense in Depth: VTD Forgery](#12-defense-in-depth-vtd-forgery)
13. [Defense in Depth: Collusion](#13-defense-in-depth-collusion)
14. [Security Analysis](#14-security-analysis)
15. [Scalability Analysis](#15-scalability-analysis)
16. [Open Design Questions](#16-open-design-questions)
17. [Conclusion](#17-conclusion)
- [Appendix A: Complete VTD JSON Schemas](#appendix-a-complete-vtd-json-schemas)
- [Appendix B: Subjective Logic Operator Definitions](#appendix-b-subjective-logic-operator-definitions)
- [Appendix C: Configurable Parameters Table](#appendix-c-configurable-parameters-table)
- [Appendix D: Conformance Requirements](#appendix-d-conformance-requirements)
- [Appendix E: Test Vectors](#appendix-e-test-vectors)
- [Appendix F: Traceability Matrix](#appendix-f-traceability-matrix)
- [Appendix G: CACT Parameters and Test Vectors](#appendix-g-cact-parameters-and-test-vectors)
- [Appendix H: AVAP Parameters](#appendix-h-avap-parameters)
- [Appendix I: Glossary](#appendix-i-glossary)
- [Changelog](#changelog)

---

## 1. Introduction and Motivation

### 1.1 Why Verification Matters for Planetary AI Coordination

As multi-agent AI systems scale from tens to thousands of cooperating agents, the question of output trustworthiness becomes architecturally critical. A single agent can produce valuable analysis, but a planetary-scale coordination fabric -- where agents across diverse domains contribute knowledge to a shared canonical graph -- requires a principled answer to the question: "Why should any agent trust what another agent claims?"

The naive answer is social trust: agents learn to trust each other through repeated interaction. But social trust does not scale, cannot be audited, and provides no defense against sophisticated adversarial behavior. The engineering answer is verification: a systematic mechanism that evaluates every claim before it enters durable shared memory.

The Tidal Noosphere [1] is a coordination fabric designed for planetary-scale multi-agent AI cooperation. It provides governance (constitutional protections, VRF-based committee selection, tidal epoch scheduling) but delegates the question of HOW verification executes to a Verification Membrane -- a sovereignty-protected subsystem through which all claims must pass before entering the canonical knowledge graph. PCVM is that membrane.

### 1.2 The Problem with Replication-Based Consensus

The Tidal Noosphere's predecessor verification layer, Verichain, used replication-based consensus: multiple agents independently re-execute the computation that produced a claim, compare their results, and vote on agreement. This approach has three fundamental limitations:

**Cost.** Replication requires O(n) compute where n is the number of verifiers. For a 5-member verification committee, every claim costs 5x the original computation. At Noosphere scale (1,000-100,000 agents producing thousands of claims per epoch), this is prohibitively expensive.

**Non-determinism.** Large language model outputs are non-deterministic. Two runs of the same prompt produce different text. Replication-based consensus assumes deterministic computation -- "I ran the same program and got the same answer" -- which is structurally incompatible with LLM-based agents. Verichain was designed for an era of deterministic computation that no longer exists.

**Depth.** Replication checks "did I get the same answer?" but not "is this answer well-supported?" Two independent agents can produce the same incorrect claim -- both hallucinate the same false citation, both make the same logical error -- and replication reports consensus. Agreement is not truth.

### 1.3 The Proof-Carrying Alternative

PCVM replaces replication with proof-carrying verification: instead of re-executing computations, the membrane requires every agent output to carry a Verification Trace Document (VTD) -- a structured evidence package that provides machine-checkable support for the claim. The membrane evaluates the VTD rather than re-executing the computation.

The key insight that makes this work is that not all claims are equal. A deterministic hash computation can be verified by checking a proof certificate in sublinear time. An empirical claim about GPT-4's benchmark performance can be verified by checking cited sources and cross-references. A heuristic architectural recommendation can only be verified by evaluating whether alternatives were genuinely considered and whether the reasoning is sound. These are fundamentally different verification tasks that require different proof obligations.

PCVM embraces this heterogeneity through a graduated VTD model with three verification tiers matched to nine claim classes. The result is a verification architecture that provides genuine sublinear verification for decidable claims, structured evidence evaluation for empirical and reasoning claims, and honest acknowledgment that judgment-based claims cost more to verify than to replicate -- with the compensating benefit of producing richer verification metadata and enabling downstream trust propagation.

### 1.4 Defense in Depth: CACT and AVAP

PCVM v1.0 identified two CRITICAL residual risks with HIGH severity: VTD forgery (the "Confident Liar" attack) and mutual endorsement collusion. These risks are fundamental to any peer-verification system. PCVM v2.0 integrates two defense-in-depth subsystems that reduce these risks from HIGH to MEDIUM-LOW:

**CACT (Commit-Attest-Challenge-Triangulate)** addresses VTD forgery by escaping the infinite trust regress. Rather than adding more links to the evidence verification chain, CACT shifts verification to orthogonal channels: temporal commitments that bind evidence before claim construction, verifiable computation proofs (SNARK/STARK) for computational claims, adversarial knowledge interrogation that tests the producer's generative understanding, and multi-channel orthogonal verification that requires simultaneous fabrication across structurally independent systems. A sophisticated forger's detection probability rises from 0.434 (base PCVM) to 0.611 (with CACT).

**AVAP (Anonymous Verification with Adaptive Probing)** addresses collusion by combining structural prevention, active detection, and economic deterrence. Anonymous VRF self-selection with cover traffic prevents colluders from identifying allies. Sealed commit-reveal opinions prevent real-time opinion signaling. Honeypot claims with known ground truth catch blanket coordination strategies. Conditional behavioral analysis detects selective collusion through pairwise mutual information. Collusion deterrence payments create economic incentives for ring defection. Together with the C10 4-layer defense-in-depth, AVAP forms a 6-layer system that renders collusion statistically detectable within 25 epochs and economically irrational to sustain beyond 10 epochs.

---

## 2. Background and Related Work

### 2.1 Proof-Carrying Code

The conceptual ancestor of PCVM is Necula's Proof-Carrying Code (PCC) [2], which introduced the idea that untrusted code can be made trustworthy by attaching a machine-checkable proof of safety. The code producer constructs a proof that the code satisfies a safety policy; the code consumer checks the proof (which is cheaper than analyzing the code) and, if the proof validates, runs the code without further verification.

PCVM extends this concept from programs to agent outputs. Where PCC proves "this program satisfies memory safety," PCVM proves "this claim is supported by adequate evidence, correct reasoning, or proper process." The extension is non-trivial: PCC operates over decidable properties of deterministic programs, while PCVM must handle undecidable properties of non-deterministic agent outputs. PCVM's graduated model (formal proofs for decidable claims, structured evidence for undecidable claims) is an honest acknowledgment of this fundamental difference.

### 2.2 AI Output Verification

Several systems address AI output verification, though none produce persistent, structured proof artifacts:

**FactScore** [3] decomposes LLM-generated text into atomic facts and checks each fact against a knowledge source. FactScore produces a numerical score but not a structured verification artifact. The verification is ephemeral (not stored) and does not compose across claims.

**SAFE (Search-Augmented Factuality Evaluator)** [4] uses an LLM to verify claims by searching for supporting or contradicting evidence. SAFE produces a factuality score but does not create a machine-checkable proof artifact.

**Chain-of-Verification (CoVe)** [5] has an LLM generate verification questions about its own output, answer them independently, and revise the output accordingly. CoVe is a self-correction mechanism, not an external verification layer.

**CLOVER** [6] provides closed-loop verifiable code generation where an LLM generates code with an attached test suite that verifies correctness. CLOVER is limited to code generation and produces verification artifacts (test suites) only for code.

PCVM differs from all of these in three ways: (1) VTDs are persistent, machine-checkable artifacts stored alongside the claims they support; (2) VTDs are class-specific, with different proof obligations for different types of claims; and (3) verification is performed by an external membrane with adversarial probing, not by the producing agent itself.

### 2.3 Epistemic Claim Taxonomies

PCVM's nine-class claim taxonomy draws on several epistemic classification frameworks:

**GRADE (Grading of Recommendations Assessment, Development and Evaluation)** [7] classifies evidence quality in medical literature as High, Moderate, Low, or Very Low. PCVM's tier system is analogous but more granular and domain-general.

**ECO (Evidence and Conclusion Ontology)** [8] provides an ontology for relating evidence to conclusions in biomedical literature. PCVM's VTD dependency model (claims referencing other claims as premises or evidence) is structurally similar.

**W3C PROV** [9] is a standard for representing provenance -- the history of how data was produced. PCVM's VTD captures provenance as part of the verification trace, extending W3C PROV with claim-class-specific proof obligations.

No prior system combines epistemic classification with differential proof obligations: the idea that the type of knowledge claim determines what constitutes adequate proof is novel to PCVM.

### 2.4 Multi-Agent Verification Landscape

The multi-agent verification landscape bifurcates into two camps:

**Trust-the-LLM systems** (LangGraph, CrewAI, AutoGen, OpenAI Swarm) rely on prompting, guardrails, and post-hoc observability. None produce structured per-output verification artifacts.

**Verify-the-computation systems** (EZKL, Modulus Labs, Giza, Ritual) use zero-knowledge proofs to verify that a specific ML model was executed correctly on specific inputs. These prove computational integrity -- "this model ran correctly" -- but not semantic correctness -- "the output is factually accurate and well-supported."

PCVM occupies the unexploited architectural niche between these two camps: verifying that the semantic content of an agent's output is well-supported, correctly reasoned, and adequately evidenced.

The closest partial competitors are Truebit (cryptographic transcripts of agent decisions, approximately 30% overlap), Monte Carlo Agent Observability (input/output trust contracts, approximately 25% overlap), and Ritual Infernet (verifiable inference oracles, approximately 20% overlap). No existing system combines structured proof artifacts, an epistemic claim taxonomy, adversarial probing, and constitutional protections for membrane parameters.

### 2.5 Verifiable Computation and Anti-Forgery

CACT draws on research in verifiable computation and anti-forgery systems:

**SNARKs (Succinct Non-interactive Arguments of Knowledge)** [11] allow a prover to convince a verifier that a computation was performed correctly, with verification cost sublinear in the computation size. PCVM uses Groth16 for D-class computational claims where proof size and verification time are critical.

**STARKs (Scalable Transparent Arguments of Knowledge)** [12] provide similar guarantees without a trusted setup, using hash-based commitments (FRI protocol). PCVM uses STARKs for computational claims where transparency is preferred over proof compactness.

**Temporal Commitment Schemes** based on Pedersen commitments bind evidence to timestamps before claim construction, making retroactive fabrication cryptographically impossible without breaking the discrete logarithm assumption.

**Costly Signaling Theory** from evolutionary biology and economics provides the theoretical basis for Knowledge Interrogation probes: if demonstrating knowledge of fabricated evidence is cheaper than possessing genuine knowledge, the signaling protocol has failed. CACT's interrogation protocol is designed so that answering unpredictable questions about genuinely gathered evidence is significantly cheaper than fabricating consistent answers about invented evidence.

### 2.6 Anti-Collusion Mechanisms

AVAP draws on research in mechanism design, anonymous voting, and collusion resistance:

**VRF Self-Selection** extends the Algorand consensus model where agents privately evaluate their eligibility rather than having a coordinator assign roles. This eliminates the coordinator as a target for collusion intelligence.

**Commit-Reveal Protocols** from sealed-bid auctions prevent participants from conditioning their bids on others' bids. AVAP applies this to Subjective Logic opinions: agents commit to opinion hashes before seeing any other agent's commitment.

**Honeypot Systems** from cybersecurity deploy known-false targets to detect adversarial behavior. AVAP's class-stratified honeypot claims extend this to epistemic verification: synthetic claims with known ground truth are injected indistinguishably into the verification pipeline.

**Linkable Ring Signatures** (Fujisaki-Suzuki 2007) enable anonymous but non-duplicable reporting, used in AVAP's collusion deterrence mechanism for zero-knowledge defector reports.

### 2.7 The Tidal Noosphere Context

PCVM operates within the Tidal Noosphere coordination fabric [1], which provides:

- **Governance:** Constitutional protections, G-class consensus for parameter changes, sovereignty boundaries.
- **Committee Selection:** VRF-based (ECVRF on P-256, RFC 9381) committee selection with pre-stratified diversity pools and commit-reveal dual defense.
- **Epoch Scheduling:** Tidal epoch clock (1-hour default, NTP-synchronized) for scheduling verification rounds.
- **Sentinel Graph:** Anomaly detection system that monitors system health and triggers defensive responses.
- **Settlement Plane:** Economic incentive layer (C8 DSF) that rewards honest verification and penalizes fraudulent behavior, including slashing for detected forgery and collusion.

PCVM is the verification execution engine within this governance framework. The Noosphere determines WHAT gets verified (all claims entering durable memory), WHO verifies (VRF-selected committees), and WHEN verification occurs (tidal epoch scheduling). PCVM determines HOW verification executes.

---

## 3. Architectural Overview

### 3.1 Stack Position

PCVM occupies the verification layer between the Tidal Noosphere (coordination) and the Knowledge Cortex (persistent memory):

```
CIOS (orchestration)
    |
    v
Tidal Noosphere (coordination)
    |  Provides: VRF dual defense, constitutional protections,
    |  MQI drift detection, Sentinel Graph, V-class algebra,
    |  tidal epoch scheduling, settlement integration
    |
    v
PCVM (verification) <-- THIS DOCUMENT
    |  Provides: VTD generation/checking, claim classification,
    |  tier-specific verification, credibility composition,
    |  adversarial probing, deep-audit, knowledge admission,
    |  CACT forgery defense, AVAP collusion defense
    |
    v
Knowledge Cortex (persistent memory)
    |  Provides: BDL persistence, re-verification triggers,
    |  dependency graph, knowledge evolution
    |
    v
Settlement Plane (AIC economy)
       Provides: verification rewards, quality scoring,
       economic incentives for honest verification,
       slashing for forgery/collusion (C8 DSF)
```

### 3.2 Design Principles and Invariants

Seven formal invariants govern PCVM's behavior:

**INV-M1 (Membrane Sovereignty).** No claim enters the canonical knowledge graph without passing through PCVM. This invariant is constitutionally protected.

**INV-M2 (Classification Independence).** The membrane assigns final claim classifications. Producing agents propose; the membrane decides. No agent may self-certify its own claim classification.

**INV-M3 (Verifier Independence).** VTD verification is performed by VRF-selected committees. No agent may verify its own claims. Adversarial probers are selected independently of verification committees.

**INV-M4 (Class-Specific Trust).** Agent credibility is tracked per claim class. An agent's credibility in class K does not transfer to class K' where K != K'.

**INV-M5 (Deep-Audit Deterrence).** A configurable percentage (default 7%) of all passed VTDs are re-verified via full replication. Selection is VRF-based and unpredictable.

**INV-M6 (Credibility Monotonicity).** Composition of opinions via conjunction never increases belief beyond the minimum of the composed beliefs. Discounting never increases belief beyond the discounter's trust level.

**INV-M7 (VTD Immutability).** Once a VTD is submitted and sealed, its contents MUST NOT be modified. Corrections require a new VTD with an explicit supersedes reference.

### 3.3 Component Map

PCVM consists of nine components, extended with CACT and AVAP integration points:

```
+------------------------------------------------------------------+
|                         PCVM MEMBRANE                             |
|                                                                   |
|  +----------------+    +------------------+    +---------------+  |
|  | VTD Engine     |    | Claim Classifier |    | Verification  |  |
|  | (construct,    |--->| (3-way classify, |--->| Dispatcher    |  |
|  |  validate,     |    |  seal, appeal)   |    | (route by     |  |
|  |  store VTDs,   |    |                  |    |  tier/stakes) |  |
|  |  CACT commit   |    |                  |    |               |  |
|  |  chain mgmt)   |    |                  |    |               |  |
|  +----------------+    +------------------+    +-------+-------+  |
|                                                        |          |
|  +------+  +-----------+  +-----------+  +-------+    |          |
|  | Proof|  | Evidence  |  |Attestation|  | Adver-|    |          |
|  |Checker| | Evaluator |  | Reviewer  |  | sarial|<---+          |
|  |(Tier1,| | (Tier 2,  |  | (Tier 3,  |  |Prober |              |
|  | SNARK/|  | CACT OVC)|  | sealed    |  |(+KI   |              |
|  | STARK)|  |          |  | opinions) |  | probe)|              |
|  +---+--+  +-----+-----+  +-----+-----+  +---+---+              |
|      |           |               |            |                   |
|      +-----------+-------+-------+------------+                   |
|                          |                                        |
|              +-----------v-----------+    +-------------------+   |
|              | Credibility Engine    |    | Deep-Audit        |   |
|              | (Subjective Logic,    |    | Subsystem         |   |
|              |  propagation, decay,  |    | (VRF selection,   |   |
|              |  OVC adjustments)     |    |  full replication, |   |
|              +-----------+-----------+    |  stratified       |   |
|                          |               |  sampling)         |   |
|              +-----------v-----------+    +-------------------+   |
|              | Knowledge Admission   |                            |
|              | Gate (MCT issuance,   |                            |
|              |  BDL persistence,     |                            |
|              |  contradiction check) |                            |
|              +-----------------------+                            |
|                                                                   |
|  +---------------------------+  +----------------------------+    |
|  | CACT Subsystem            |  | AVAP Subsystem             |    |
|  | (commitment chains,       |  | (anonymous committees,     |    |
|  |  VC proofs, KI probes,    |  |  sealed opinions,          |    |
|  |  orthogonal channels,     |  |  honeypot claims,          |    |
|  |  OVC scoring)             |  |  deterrence payments,      |    |
|  +---------------------------+  |  behavioral analysis)      |    |
|                                 +----------------------------+    |
+------------------------------------------------------------------+
```

### 3.4 What PCVM Replaces

| Verichain (deprecated) | PCVM (replacement) |
|------------------------|-------------------|
| Replication-based consensus | VTD proof-checking + evidence evaluation |
| Binary pass/fail | Credibility opinion tuple (b, d, u, a) |
| O(replication) for all claims | Variable cost by claim class |
| Untyped claims | 9-class typed claims with class-specific VTDs |
| Verification result stored as boolean | VTD stored permanently for audit and re-verification |
| No adversarial component | Selective adversarial probing + random deep-audit |
| No credibility propagation | Subjective Logic composition through dependency graphs |
| No forgery defense | CACT: commitment binding + verifiable computation + orthogonal verification |
| No collusion defense | AVAP: anonymous committees + sealed opinions + honeypots + deterrence |

---

## 4. The Graduated VTD Model

### 4.1 Design Rationale

The original PCVM proposal claimed universal proof-checking across all claim classes. Adversarial analysis and scientific review revealed this to be untenable: formal proof-checking works for decidable, deterministic computations but cannot be meaningfully applied to heuristic judgments or normative claims. The graduated VTD model is the honest architectural response.

Three verification tiers are matched to nine claim classes based on a principled epistemic status x verification modality matrix (Section 5). Each tier defines different proof obligations, verification mechanisms, and cost profiles.

### 4.2 Tier 1: Formal Proofs (D-class, C-class)

**Applicable claims:** Deterministic computations (D-class) and regulatory compliance checks (C-class).

**Proof obligation:** Machine-checkable proof that the claimed result follows from the stated inputs via the stated algorithm. For D-class claims involving computation, SNARK/STARK proofs (via CACT) provide mathematical verification of computational integrity with soundness error ~2^-128.

**Verification mechanism:** Proof certificate checking, computation trace spot-checking, rule matching against a finite requirement set, or SNARK/STARK proof verification.

**Cost:** 0.1x-0.35x of replication. This is where PCVM delivers genuine sublinear verification. The verifier checks the proof without re-executing the computation.

**D-class VTD** carries: algorithm identifier, input hashes, output hash, proof type (recomputation, hash verification, proof certificate, proof sketch, SNARK_PROOF, or STARK_PROOF), and optional computation trace with sampled intermediate steps. When SNARK_PROOF or STARK_PROOF is used, the VTD also carries the CACT verifiable computation attestation.

**C-class VTD** carries: regulation reference, requirement mapping (each requirement mapped to evidence), gap analysis, compliance status, and constitutional parameter checks.

**Verification result:** Binary opinion for D-class -- w = (1, 0, 0, 0.5) if verified, w = (0, 1, 0, 0.5) if falsified. Near-binary for C-class, with belief proportional to the compliance rate.

### 4.3 Tier 2: Structured Evidence (E-class, S-class, P-class, R-class, K-class)

**Applicable claims:** Empirical observations (E-class), statistical inferences (S-class), process conformance (P-class), logical reasoning (R-class), and knowledge consolidation (K-class).

**Proof obligation:** Structured evidence chain linking the claim to verifiable sources, valid methodology, proper process, sound logic, or diverse provenance with traceable synthesis.

**Verification mechanism:** Source verification, methodology audit, process trace conformance checking, logical validity assessment, provenance diversity checking, plus selective adversarial probing for high-stakes or low-credibility claims. CACT orthogonal verification channels (process traces, statistical texture, environmental side-effects) provide additional verification depth.

**Cost:** 0.35x-1.2x of replication. The cost advantage is moderate and comes primarily from structured evaluation rather than re-execution. For E-class claims with mandatory source verification (enhanced per C10 hardening), cost approaches replication. The compensating value is richer verification metadata.

**E-class VTD** carries: source citations with URLs, content hashes, and quoted text; cross-references between sources; an evidence chain linking claim to sources; and observation conditions.

**S-class VTD** carries: dataset metadata (sample size, sampling method, data hash); methodology (test type, software, pre-registration); results (test statistic, p-value, confidence interval, effect size); and assumption checks.

**P-class VTD** carries: process specification reference; step-by-step execution log with timestamps; deviation records with justifications; and conformance summary.

**R-class VTD** carries: premises with support types (verified claim, axiom, assumption, empirical); inference steps with named rules (modus ponens, hypothetical syllogism, etc.); assumption declarations; and logical validity assessment with fallacy checks.

**K-class VTD** carries: source quanta references (minimum 5 from at least 5 agents and 3 parcels, no single agent contributing >30%); synthesis chain with reasoning and reconciliation notes; falsification statement with testable conditions; voting record with 3-pass protocol; and provenance summary.

### 4.4 Tier 3: Structured Attestations (H-class, N-class)

**Applicable claims:** Heuristic judgments and expert recommendations (H-class), and normative/ethical claims (N-class).

**Proof obligation:** Structured attestation demonstrating that alternatives were genuinely considered, uncertainty is acknowledged, and the claim is constitutionally aligned.

**Verification mechanism:** MANDATORY adversarial probing plus expert committee review with structured disagreement protocol. Under AVAP, committee opinions are submitted via sealed commit-reveal protocol to prevent real-time signaling.

**Cost:** 1.0x-2.0x of replication. This is an honest admission: Tier 3 claims are harder to verify, not easier. The value proposition for Tier 3 is not cost reduction but quality improvement -- structured deliberation produces richer verification metadata, and adversarial probing exposes weaknesses that replication would miss.

**H-class VTD** carries: alternatives considered (minimum 2 genuinely evaluated); evaluation criteria with weights; evaluation matrix (each alternative against each criterion); precedents cited; stated confidence level; declared uncertainty sources; boundary conditions; and failure modes.

**N-class VTD** carries: value framework (ethical theory invoked with justification); constitutional parameter references with alignment assessments; stakeholder analysis (impact on each affected group); alternative normative positions considered; and dissent record.

### 4.5 VTD Common Envelope

Every VTD, regardless of claim class, conforms to a common envelope schema that carries identity, provenance, and structural metadata. The class-specific proof evidence is carried in the `proof_body` field.

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-envelope.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "VTD Common Envelope",
  "type": "object",
  "required": [
    "vtd_id", "claim_id", "claim_text", "suggested_class",
    "assigned_class", "tier", "producing_agent", "epoch",
    "locus", "timestamp", "proof_body", "dependencies",
    "counter_evidence", "vtd_hash", "agent_signature"
  ],
  "properties": {
    "vtd_id": {
      "type": "string",
      "pattern": "^vtd:clm:[^:]+:[0-9]+:[a-f0-9]{8}:[0-9]+$"
    },
    "claim_id": {
      "type": "string",
      "pattern": "^clm:[^:]+:[0-9]+:[a-f0-9]{8}$"
    },
    "claim_text": {
      "type": "string", "minLength": 1, "maxLength": 10000
    },
    "suggested_class": {
      "type": "string",
      "enum": ["D", "E", "S", "H", "N", "P", "R", "C", "K"]
    },
    "assigned_class": {
      "type": ["string", "null"],
      "enum": ["D", "E", "S", "H", "N", "P", "R", "C", "K", null]
    },
    "secondary_classes": {
      "type": "array",
      "items": { "type": "string", "enum": ["D","E","S","H","N","P","R","C","K"] },
      "default": []
    },
    "tier": {
      "type": ["string", "null"],
      "enum": ["FORMAL_PROOF", "STRUCTURED_EVIDENCE", "STRUCTURED_ATTESTATION", null]
    },
    "producing_agent": { "type": "string" },
    "epoch": { "type": "integer", "minimum": 0 },
    "locus": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "proof_body": { "type": "object" },
    "secondary_proof_bodies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["class", "body"],
        "properties": {
          "class": { "type": "string" },
          "body": { "type": "object" }
        }
      },
      "default": []
    },
    "cact_extension": {
      "type": "object",
      "description": "CACT commitment chain and orthogonal verification data. See Section 8.",
      "properties": {
        "commitment_chain": {
          "type": "object",
          "required": ["chain_id", "commitments", "chain_hash"],
          "properties": {
            "chain_id": { "type": "string", "pattern": "^cact:chain:[a-f0-9]{16}$" },
            "commitments": {
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "object",
                "required": ["commitment_id", "timestamp", "commitment_hash", "commitment_type"],
                "properties": {
                  "commitment_id": { "type": "string" },
                  "timestamp": { "type": "string", "format": "date-time" },
                  "commitment_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
                  "commitment_type": {
                    "type": "string",
                    "enum": ["EVIDENCE_GATHER", "INTERMEDIATE_RESULT", "ANALYSIS_STEP",
                             "SOURCE_RETRIEVAL", "METHODOLOGY_SELECTION", "DRAFT_CONCLUSION"]
                  },
                  "revealed_content_hash": { "type": ["string", "null"] },
                  "pedersen_params": {
                    "type": "object",
                    "properties": {
                      "generator": { "type": "string" },
                      "blinding_factor_hash": { "type": "string" }
                    }
                  }
                }
              }
            },
            "chain_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
            "temporal_span": {
              "type": "object",
              "properties": {
                "first_commitment": { "type": "string", "format": "date-time" },
                "last_commitment": { "type": "string", "format": "date-time" },
                "vtd_submission": { "type": "string", "format": "date-time" }
              }
            }
          }
        },
        "vc_attestation": {
          "type": "object",
          "description": "Verifiable computation proof (D-class, computational S-class)",
          "properties": {
            "proof_system": { "type": "string", "enum": ["GROTH16", "PLONK", "STARK_FRI", "NONE"] },
            "circuit_id": { "type": "string" },
            "proof_bytes": { "type": "string", "contentEncoding": "base64" },
            "public_inputs_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
            "verification_key_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
          }
        },
        "orthogonal_channels": {
          "type": "object",
          "properties": {
            "process_trace": { "type": "object" },
            "statistical_texture": { "type": "object" },
            "environmental_side_effects": { "type": "object" }
          }
        },
        "ovc_score": {
          "type": ["number", "null"],
          "minimum": 0, "maximum": 1,
          "description": "Orthogonal Verification Coverage score computed post-verification"
        }
      }
    },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["claim_id", "relationship"],
        "properties": {
          "claim_id": { "type": "string" },
          "relationship": {
            "type": "string",
            "enum": ["PREMISE", "EVIDENCE", "PROCESS_INPUT",
                     "CONSTITUTIONAL_AXIOM", "EXTERNAL_SOURCE"]
          },
          "required_credibility": {
            "type": "number", "minimum": 0, "maximum": 1, "default": 0.6
          }
        }
      }
    },
    "counter_evidence": {
      "type": "object",
      "required": ["considered"],
      "properties": {
        "considered": { "type": "boolean" },
        "items": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["description", "disposition"],
            "properties": {
              "description": { "type": "string" },
              "source": { "type": "string" },
              "disposition": {
                "type": "string",
                "enum": ["REFUTED", "ACKNOWLEDGED_LIMITATION",
                         "SCOPE_EXCLUSION", "UNRESOLVED"]
              },
              "refutation": { "type": "string" }
            }
          },
          "default": []
        }
      }
    },
    "supersedes": { "type": ["string", "null"], "default": null },
    "vtd_size_bytes": { "type": "integer" },
    "vtd_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "agent_signature": { "type": "string" }
  },
  "additionalProperties": false
}
```

**VTD Size Limits per Class:**

| Class | Max Size | Rationale |
|-------|----------|-----------|
| D | 10 KB | Computation traces are compact |
| C | 50 KB | Compliance mappings may be lengthy |
| E | 50 KB | Source citations with quotes |
| S | 30 KB | Statistical metadata is structured |
| P | 100 KB | Process logs can be detailed |
| R | 30 KB | Reasoning chains are bounded |
| K | 75 KB | Source quanta refs + synthesis chain can be substantial |
| H | 100 KB | Alternatives analysis can be extensive |
| N | 100 KB | Stakeholder analysis can be extensive |

Claims exceeding size limits MUST be decomposed into smaller sub-claims, each with its own VTD.

---

## 5. Claim Classification System

### 5.1 The Epistemic Status x Verification Modality Matrix

The nine claim classes are not arbitrary categories. They are derived from a principled two-dimensional matrix crossing epistemic status (what kind of knowledge the claim represents) with verification modality (how the claim can be checked):

| | REPLAY | EVIDENCE | LOGIC | ALIGNMENT |
|---|---|---|---|---|
| **COMPUTED** | D (primary) | | | C |
| **OBSERVED** | | E (primary) | | |
| **INFERRED** | | S | R (primary) | |
| **SYNTHESIZED** | | K (primary) | K | |
| **JUDGED** | | | | H, N |

P (Process) is cross-cutting: it applies to the production process of any claim regardless of epistemic status. K (Knowledge Consolidation) spans EVIDENCE and LOGIC modalities because it synthesizes across sources and requires reasoning chain validation.

### 5.2 Formal Class Definitions

**D-class (Deterministic).** A claim whose truth value is decidable by deterministic computation. The claim's correctness can be verified by replaying the computation on the stated inputs or, when available, by checking a SNARK/STARK proof of computational integrity. Examples: hash computations, sorting results, mathematical calculations. Tier: FORMAL_PROOF.

**C-class (Compliance).** A claim that a system, process, or output conforms to a specified regulation, standard, or constitutional parameter. Verification reduces to matching against a finite rule set. Examples: EU AI Act Article 11 compliance, constitutional parameter satisfaction. Tier: FORMAL_PROOF.

**E-class (Empirical).** A claim derived from observation or measurement of external phenomena. Verification requires checking cited sources, cross-referencing, and assessing source reliability. Enhanced source verification (C10 hardening) mandates independent retrieval and support assessment. Examples: benchmark scores, market data, experimental results. Tier: STRUCTURED_EVIDENCE.

**S-class (Statistical).** A claim derived from statistical analysis of data. Verification requires checking methodology, sample adequacy, test appropriateness, and conclusion validity. Examples: load balancing efficiency measurements, performance comparisons. Tier: STRUCTURED_EVIDENCE.

**P-class (Process).** A claim that a specified process was followed during the production of another claim. Verification checks execution traces against the declared process specification, including CACT process trace consistency checks. Examples: research protocol adherence, pipeline stage execution. Tier: STRUCTURED_EVIDENCE.

**R-class (Reasoning).** A claim derived from logical inference over premises. Verification checks logical validity, premise support, and assumption disclosure. Examples: architectural arguments, I-confluence proofs. Tier: STRUCTURED_EVIDENCE.

**K-class (Knowledge Consolidation).** A claim that synthesizes information from multiple source quanta contributed by multiple agents into a consolidated knowledge artifact. The synthesis must demonstrate provenance diversity (no single agent or parcel dominates), a traceable reasoning chain from sources to conclusion, and a falsification statement articulating what evidence would refute the consolidation. Verification checks provenance diversity, reasoning chain validity, falsification statement quality, and cross-domain coherence. Examples: literature synthesis across agent contributions, architectural pattern consolidation, cross-domain risk assessment. Tier: STRUCTURED_EVIDENCE.

**H-class (Heuristic).** A claim derived from expert judgment, model prediction, or pragmatic assessment. Verification checks that alternatives were considered, criteria are appropriate, and no known contradictions exist. Examples: technology recommendations, architectural decisions. Tier: STRUCTURED_ATTESTATION.

**N-class (Normative).** A claim about values, ethics, or policy that invokes a normative framework. Verification checks constitutional alignment, stakeholder coverage, and framework application consistency. Normative claims are verified for consistency and completeness, not for truth. Examples: ethical guidelines, governance policies. Tier: STRUCTURED_ATTESTATION.

### 5.3 Classification Signatures

The `CLASSIFICATION_SIGNATURES` dictionary defines structural text patterns for each class. Each signature contains marker patterns (matched against claim text and VTD `proof_body` field names) and exclusion patterns. Pattern matching uses case-insensitive substring or regex matching.

```python
# Each signature has:
#   markers:   list of (pattern, weight) tuples. A pattern match contributes
#              its weight toward the class score. Patterns are regex.
#   exclusion: list of patterns. ANY match disqualifies this class (score = 0).
#
# count_matching_markers() returns sum of weights for matched marker patterns.
# max_possible_score() returns sum of all possible weights (for normalization).

CLASSIFICATION_SIGNATURES = {

    "D": ClassificationSignature(
        markers=[
            (r"\b(comput|calculat|hash|sort|encrypt|decrypt|deterministic)\b", 1.0),
            (r"\b(algorithm|function|output\s+equals?|result\s+is)\b", 0.8),
            (r"\b(SHA-?\d+|MD5|AES|RSA|CRC)\b", 1.0),
            (r"\b(recomput|replay|reproduce|identical)\b", 0.7),
            (r"\b(given\s+input|for\s+input|on\s+input)\b", 0.6),
            # VTD structural: proof_body has computation + inputs + output fields
            (r"__vtd_has_field:computation", 1.0),
            (r"__vtd_has_field:proof_type", 0.8),
        ],
        exclusion=[
            r"\b(recommend|should|ought|ethic|moral|stakeholder)\b",
            r"\b(heuristic|judgment|opinion|believe|estimate|approximate)\b",
            r"\b(survey|sample|population|p-value|confidence\s+interval)\b",
            r"\b(observed|measured|experiment|benchmark\s+score)\b",
        ]
    ),

    "E": ClassificationSignature(
        markers=[
            (r"\b(observed|measured|recorded|reported|found\s+that)\b", 1.0),
            (r"\b(benchmark|experiment|study\s+shows?|data\s+shows?)\b", 1.0),
            (r"\b(source|citation|according\s+to|per\s+\w+\s+report)\b", 0.8),
            (r"\b(empirical|evidence|finding|result)\b", 0.7),
            (r"\b(score[ds]?\s+\d|achieve[ds]?\s+\d|percent|rate\s+of)\b", 0.8),
            (r"\b(as\s+of\s+\d{4}|in\s+\d{4}|published)\b", 0.6),
            # VTD structural: proof_body has sources + evidence_chain
            (r"__vtd_has_field:sources", 1.0),
            (r"__vtd_has_field:evidence_chain", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of|sort\s+of\s+\[|given\s+input)\b",
            r"\b(p-value|confidence\s+interval|regression|hypothesis\s+test)\b",
            r"\b(should|ought|recommend|ethic|normative)\b",
        ]
    ),

    "S": ClassificationSignature(
        markers=[
            (r"\b(statistic|p-value|confidence\s+interval|significance)\b", 1.0),
            (r"\b(sample\s+size|population|regression|correlation)\b", 1.0),
            (r"\b(hypothesis|null|alternative\s+hypothesis|test\s+shows?)\b", 0.9),
            (r"\b(mean|median|standard\s+deviation|variance|effect\s+size)\b", 0.8),
            (r"\b(chi-squared|t-test|ANOVA|Mann-Whitney|Wilcoxon)\b", 1.0),
            (r"\b(dataset|n\s*=\s*\d+|sampling)\b", 0.7),
            # VTD structural: proof_body has dataset + methodology + results
            (r"__vtd_has_field:dataset", 1.0),
            (r"__vtd_has_field:methodology", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash|encrypt)\b",
            r"\b(should|ought|recommend|ethic|normative)\b",
            r"\b(process\s+was\s+followed|step\s+\d+\s+executed)\b",
        ]
    ),

    "P": ClassificationSignature(
        markers=[
            (r"\b(process|procedure|protocol|pipeline|workflow)\b", 1.0),
            (r"\b(step\s+\d+|phase\s+\d+|stage\s+\d+)\b", 0.9),
            (r"\b(followed|executed|completed|adhered\s+to)\b", 0.8),
            (r"\b(conformance|compliance\s+with\s+process|deviat)\b", 0.9),
            (r"\b(log|trace|timestamp|audit\s+trail)\b", 0.7),
            (r"\b(specification\s+\w+\s+was|per\s+SOP|per\s+spec)\b", 0.8),
            # VTD structural: proof_body has process_spec + steps
            (r"__vtd_has_field:process_spec", 1.0),
            (r"__vtd_has_field:steps", 0.9),
            (r"__vtd_has_field:conformance_summary", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of)\b",
            r"\b(ethic|moral|normative|stakeholder)\b",
            r"\b(recommend|suggest|best\s+practice)\b",
        ]
    ),

    "R": ClassificationSignature(
        markers=[
            (r"\b(therefore|hence|thus|it\s+follows|because|since)\b", 0.9),
            (r"\b(premise|conclusion|argument|infer|deduc|induc)\b", 1.0),
            (r"\b(modus\s+ponens|syllogism|contrapositive|reductio)\b", 1.0),
            (r"\b(if\s+.+then|implies|entails|necessitates)\b", 0.8),
            (r"\b(logical|valid|sound|fallacy|assumption)\b", 0.8),
            (r"\b(proof\s+by|derive|establish\s+that)\b", 0.7),
            # VTD structural: proof_body has premises + inferences
            (r"__vtd_has_field:premises", 1.0),
            (r"__vtd_has_field:inferences", 1.0),
            (r"__vtd_has_field:logical_assessment", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of|encrypt)\b",
            r"\b(ethic|moral|normative|stakeholder)\b",
            r"\b(p-value|sample\s+size|regression)\b",
            r"\b(recommend|suggest|best\s+practice|trade-?off)\b",
        ]
    ),

    "K": ClassificationSignature(
        markers=[
            (r"\b(synthesiz|consolidat|integrat|unif|merg)\b", 1.0),
            (r"\b(across\s+(agents?|domains?|sources?|parcels?))\b", 1.0),
            (r"\b(knowledge\s+(graph|base|synthesis|consolidation))\b", 1.0),
            (r"\b(provenance|multi-agent|cross-domain)\b", 0.9),
            (r"\b(source\s+quant(a|um)|contributing\s+agent)\b", 0.8),
            (r"\b(falsification|refut|reconcil)\b", 0.7),
            # VTD structural: proof_body has source_quanta + synthesis_chain
            (r"__vtd_has_field:source_quanta", 1.0),
            (r"__vtd_has_field:synthesis_chain", 1.0),
            (r"__vtd_has_field:falsification_statement", 0.9),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of|encrypt)\b",
            r"\b(ethic|moral|normative|stakeholder)\b",
            r"\b(recommend|suggest|best\s+practice)\b",
            r"\b(p-value|sample\s+size|hypothesis\s+test)\b",
        ]
    ),

    "C": ClassificationSignature(
        markers=[
            (r"\b(comply|compliance|compliant|conform)\b", 1.0),
            (r"\b(regulation|regulatory|Article\s+\d+|Section\s+\d+)\b", 1.0),
            (r"\b(EU\s+AI\s+Act|GDPR|NIST|ISO\s+\d+|SOC\s+\d)\b", 1.0),
            (r"\b(requirement\s+\w+\s+(met|satisfied)|satisfies)\b", 0.9),
            (r"\b(audit|gap\s+analysis|remediation)\b", 0.7),
            (r"\b(constitutional\s+parameter|CONST-\d+)\b", 0.8),
            # VTD structural: proof_body has regulation + requirements
            (r"__vtd_has_field:regulation", 1.0),
            (r"__vtd_has_field:requirements", 0.9),
            (r"__vtd_has_field:compliance_status", 0.8),
        ],
        exclusion=[
            r"\b(recommend|suggest|best\s+practice|heuristic)\b",
            r"\b(ethic|moral|normative\s+framework)\b",
            r"\b(p-value|sample\s+size|hypothesis\s+test)\b",
            r"\b(observed|measured|benchmark\s+score)\b",
        ]
    ),

    "H": ClassificationSignature(
        markers=[
            (r"\b(recommend|suggest|advise|best\s+practice)\b", 1.0),
            (r"\b(heuristic|judgment|expert\s+opinion|pragmatic)\b", 1.0),
            (r"\b(trade-?off|alternative|option|weigh|criterion)\b", 0.9),
            (r"\b(architecture\s+decision|design\s+choice|approach)\b", 0.8),
            (r"\b(prefer|favor|better\s+suited|most\s+appropriate)\b", 0.8),
            (r"\b(confidence|uncertain|risk|failure\s+mode)\b", 0.6),
            # VTD structural: proof_body has alternatives + criteria + evaluation
            (r"__vtd_has_field:alternatives", 1.0),
            (r"__vtd_has_field:criteria", 0.8),
            (r"__vtd_has_field:evaluation", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of|sort\s+of\s+\[)\b",
            r"\b(ethic|moral|normative|value\s+framework|stakeholder\s+impact)\b",
            r"\b(regulation|compliance|Article\s+\d+)\b",
        ]
    ),

    "N": ClassificationSignature(
        markers=[
            (r"\b(ethic|moral|normative|value|principle)\b", 1.0),
            (r"\b(should|ought|right|wrong|fair|just|equitable)\b", 0.9),
            (r"\b(stakeholder|impact\s+on|affected\s+part(y|ies))\b", 0.8),
            (r"\b(constitutional|governance|policy|guideline)\b", 0.8),
            (r"\b(deontolog|consequential|virtue\s+ethic|care\s+ethic)\b", 1.0),
            (r"\b(consent|autonomy|transparency|accountability)\b", 0.7),
            # VTD structural: proof_body has value_framework + stakeholder_analysis
            (r"__vtd_has_field:value_framework", 1.0),
            (r"__vtd_has_field:stakeholder_analysis", 0.9),
            (r"__vtd_has_field:constitutional_refs", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash|comput\w+\s+result)\b",
            r"\b(p-value|sample\s+size|regression)\b",
            r"\b(benchmark\s+score|measured|experiment)\b",
        ]
    ),
}
```

### Matching Functions

```python
def count_matching_markers(claim_text: str, vtd: VTD, markers: list) -> float:
    """Returns sum of weights for markers that match claim text or VTD structure."""
    score = 0.0
    for pattern, weight in markers:
        if pattern.startswith("__vtd_has_field:"):
            field_name = pattern.split(":")[1]
            if hasattr(vtd.proof_body, field_name) and \
               getattr(vtd.proof_body, field_name) is not None:
                score += weight
        else:
            if re.search(pattern, claim_text, re.IGNORECASE):
                score += weight
    return score

def max_possible_score(markers: list) -> float:
    """Returns sum of all weights (normalization denominator)."""
    return sum(weight for _, weight in markers)
```

### 5.4 Membrane-Assigned Classification Protocol

Classification is membrane-assigned (INV-M2): the producing agent proposes a class, but the membrane makes the final determination through a three-way protocol:

```python
def classify_claim(claim: Claim, vtd: VTD) -> ClassificationResult:
    # Step 1: Agent's suggested classification (already in VTD)
    agent_suggestion = vtd.suggested_class

    # Step 2: Structural analysis against classification signatures
    structural_scores = {}
    for cls in ClaimClass:
        sig = CLASSIFICATION_SIGNATURES[cls]
        # Check exclusions first
        excluded = False
        for excl_pattern in sig.exclusion:
            if re.search(excl_pattern, claim.text, re.IGNORECASE):
                excluded = True
                break
        if excluded:
            structural_scores[cls] = 0.0
        else:
            matched = count_matching_markers(claim.text, vtd, sig.markers)
            structural_scores[cls] = matched / max_possible_score(sig.markers)
    structural_class = max(structural_scores, key=structural_scores.get)

    # Step 3: VRF-selected independent classifier
    classifier_agent = select_independent_classifier(claim, current_epoch())
    independent_class = classifier_agent.classify(claim).classification

    # Step 4: Three-way agreement
    all_three = [agent_suggestion, structural_class, independent_class]
    if all_three[0] == all_three[1] == all_three[2]:
        assigned_class = all_three[0]
        seal_type = "UNANIMOUS"
    elif len(set(all_three)) == 2:
        majority = Counter(all_three).most_common(1)[0][0]
        assigned_class = majority
        seal_type = "MAJORITY"
    else:
        assigned_class = most_conservative_class(all_three)
        seal_type = "CONSERVATIVE"

    return ClassificationResult(assigned_class, seal_type, ...)
```

The **most conservative class** is selected when all three classification inputs disagree. Per C9 reconciliation, the conservatism ordering is:

**H > N > K > E > S > R > P > C > D**

"Most conservative" means "requires the most rigorous verification," not "most expensive." The ordering reflects verification rigor -- the degree to which mechanical checking is insufficient and human judgment, empirical grounding, or structured reasoning is required:

- **H, N (highest rigor):** These classes require human expert judgment that cannot be reduced to algorithmic checking. H-class demands evaluation of whether alternatives were genuinely considered and whether criteria are appropriate -- judgments that resist formalization. N-class demands assessment of constitutional alignment and stakeholder impact -- inherently value-laden evaluations. Defaulting a disputed claim to H or N forces the most thorough verification pathway.

- **K (high rigor):** Knowledge Consolidation claims synthesize across multiple source quanta and agents. Verification must confirm provenance diversity and reasoning chain validity -- checks that require cross-referencing multiple knowledge artifacts, not just evaluating a single evidence chain.

- **E, S (moderate rigor):** These classes require empirical evidence that can be partially checked mechanically (source verification, arithmetic recomputation) but ultimately depend on assessing source reliability and methodological soundness -- judgments that go beyond formal proof.

- **R, P (structured rigor):** These classes admit structured checking: logical validity for R-class, trace conformance for P-class. While not fully decidable (soundness requires premise evaluation), the verification steps are well-defined and largely mechanical.

- **C, D (lowest rigor, formally decidable):** These classes can be mechanically verified. D-class through computation replay, C-class through rule matching against a finite requirement set. Defaulting a disputed claim to C or D would be insufficiently rigorous for any claim that might actually require judgment or evidence.

Note that this ordering intentionally diverges from cost ordering. H-class verification (2.0x) is more expensive than E-class (0.8x), but the conservatism ordering is not about cost -- it is about the consequence of under-verifying. A heuristic claim verified only at D-class rigor would pass without any assessment of alternatives or uncertainty, producing a dangerously overconfident result. The ordering ensures that ambiguous claims receive enough scrutiny.

```python
CONSERVATISM_ORDER = {
    "H": 8, "N": 7, "K": 6, "E": 5, "S": 4, "R": 3, "P": 2, "C": 1, "D": 0
}

def most_conservative_class(classes: list) -> str:
    """Return the class requiring the most rigorous verification."""
    return max(classes, key=lambda c: CONSERVATISM_ORDER[c])
```

### 5.5 Multi-Class Claims

A claim MAY occupy multiple positions in the epistemic matrix. When it does:

1. The primary classification determines the VTD envelope type and strongest proof obligation.
2. Secondary classifications impose additional proof obligations via VTD extension sections.
3. The VTD MUST satisfy ALL applicable proof obligations (union of requirements).
4. The credibility score is the MINIMUM across all applicable class credibilities:

```
credibility(claim) = min(E(w_K) for K in claim.classes)
```

### 5.6 Anti-Gaming Defenses

**Problem:** An agent could deliberately misclassify a claim to a class with weaker proof obligations (e.g., classifying an empirical claim as heuristic to avoid source verification requirements).

**Defense 1: Membrane-assigned classification.** The membrane, not the agent, makes the final classification decision. Three independent classification signals provide defense-in-depth.

**Defense 2: Class downgrade detection.** Agents with downgrade rate > 30% (consistently proposing lower-tier classes than the membrane assigns) receive a credibility penalty of 0.10.

**Defense 3: Re-classification at audit.** During deep-audit (Section 6.4), claims are re-classified by an independent classifier. If the audit classification disagrees with the original, the verification result is invalidated.

---

## 6. Verification Protocols

### 6.1 Tier 1: Proof Checking Protocol

Tier 1 verification applies to D-class and C-class claims. Verification is mechanical and sublinear relative to recomputation.

**D-class verification** proceeds through six proof types (the original four plus SNARK_PROOF and STARK_PROOF from CACT):

```python
def verify_d_class(vtd: VTD, committee: Set[AgentId]) -> VerificationResult:
    body = vtd.proof_body

    if body.proof_type == "RECOMPUTATION":
        recomputed_hash = recompute(body.computation, body.inputs)
        if recomputed_hash == body.output.value_hash:
            return VerificationResult(status="VERIFIED",
                opinion=Opinion(b=1, d=0, u=0, a=0.5))
        else:
            return VerificationResult(status="FALSIFIED",
                opinion=Opinion(b=0, d=1, u=0, a=0.5))

    elif body.proof_type == "HASH_VERIFICATION":
        actual_hash = SHA256(canonical_serialize(body.output.value))
        if actual_hash == body.output.value_hash:
            return VerificationResult(status="VERIFIED",
                opinion=Opinion(b=1, d=0, u=0, a=0.5))

    elif body.proof_type == "PROOF_CERTIFICATE":
        check_result = run_proof_checker(cert.format, cert.certificate_uri)
        if check_result.valid:
            return VerificationResult(status="VERIFIED",
                opinion=Opinion(b=1, d=0, u=0, a=0.5))

    elif body.proof_type == "PROOF_SKETCH":
        # Spot-check random intermediate steps (not all)
        for step in body.trace.key_steps:
            if not recompute_step(step.input, step.operation) == step.output:
                return VerificationResult(status="FALSIFIED", ...)
        return VerificationResult(status="VERIFIED",
            opinion=Opinion(b=0.95, d=0, u=0.05, a=0.5))

    elif body.proof_type in ("SNARK_PROOF", "STARK_PROOF"):
        # CACT verifiable computation -- see Section 8.3.2
        vc_result = verify_vc_proof(vtd)
        if vc_result.valid:
            return VerificationResult(status="VERIFIED",
                opinion=Opinion(b=1, d=0, u=0, a=0.5))
        else:
            return VerificationResult(status="FALSIFIED",
                opinion=Opinion(b=0, d=1, u=0, a=0.5))
```

**C-class verification** checks each regulatory requirement against provided evidence, verifying completeness and accuracy of the compliance mapping. Committee agreement threshold is 80% (not unanimous, unlike D-class).

**Performance:** D-class verification cost is approximately 0.01x-0.11x of replication. C-class verification cost is approximately 0.15x-0.35x of replication.

### 6.2 Tier 2: Evidence Evaluation Protocol

Tier 2 verification applies to E-class, S-class, P-class, R-class, and K-class claims. It follows a seven-phase pipeline (extended from six in v1.0 to include CACT orthogonal verification):

1. **Schema validation** -- VTD conforms to class-specific schema.
2. **Completeness check** -- All required evidence fields populated.
3. **Counter-evidence check** -- Tier 2 MUST have a counter-evidence section.
4. **Class-specific evidence verification** -- Source checking (E), methodology audit (S), trace conformance (P), logical validity (R), provenance diversity + synthesis chain (K).
5. **CACT commitment chain verification** -- If present, verify temporal commitments (Section 8.3.1).
6. **Dependency verification** -- Claims this VTD depends on have adequate credibility.
7. **Adversarial probing decision** -- Probe if claim is high-stakes, agent has low credibility, or random selection triggers.

**E-class mandatory source verification (enhanced per C10 hardening):**

```python
def verify_source(source, probe_mode=False):
    """
    Verify an E-class source citation.

    Levels 1-3 run during routine verification.
    Level 4 runs ONLY when probe_mode=True (triggered by adversarial probing).

    Args:
        source: Source citation from VTD proof_body.sources
        probe_mode: If True, include Level 4 contextual relevance check.
                    Set to True only during adversarial probing, not routine
                    verification, to avoid verification regress.
    """
    result = SourceVerificationResult()

    # Level 1: URL accessibility (with archive.org fallback)
    response = fetch(source.url, timeout=10_000)
    if not response.accessible:
        response = fetch("https://web.archive.org/web/" + source.url)
    result.accessible = response.accessible
    if not result.accessible:
        result.verdict = "INACCESSIBLE"
        return result

    # Level 2: Content hash comparison
    current_hash = SHA256(response.body)
    result.content_unchanged = (current_hash == source.content_hash)
    if not result.content_unchanged:
        result.content_drift = True  # Flag but do not fail; content may
                                      # have been updated legitimately

    # Level 3: Quote accuracy (fuzzy match, threshold 0.9)
    result.quote_found = fuzzy_match(source.quoted_text, response.body,
                                      threshold=0.9)
    if not result.quote_found:
        result.verdict = "QUOTE_NOT_FOUND"
        return result

    # Level 4: Contextual relevance -- OPTIONAL, probe-triggered only
    if probe_mode:
        result.relevance = assess_relevance(
            source.relevance_justification, response.body)
        if result.relevance.score < 0.5:
            result.verdict = "IRRELEVANT_SOURCE"
            return result

    result.verdict = "VERIFIED"
    return result
```

**E-class independent source verification (C10 hardening, mandatory):**

```python
def verify_sources_eclass(vtd, verifier_id, epoch):
    """
    Mandatory independent source verification for E-class VTDs.
    The verifier MUST independently fetch at least one cited source
    and confirm the claim matches the source content.
    """
    sources = vtd.proof_body.sources
    evidence_chain = vtd.proof_body.evidence_chain

    # Always verify the PRIMARY source (highest weight in evidence chain).
    # Randomly verify one additional source (VRF-selected).
    primary_source = select_primary_source(sources, evidence_chain)
    additional_source = vrf_select_source(
        sources, exclude=[primary_source.source_id],
        seed=SHA256(b"SRC_VERIFY" + vtd.vtd_id.encode() +
                    verifier_id.encode() + uint64_be(epoch))
    )

    targets = [primary_source]
    if additional_source is not None:
        targets.append(additional_source)

    verdicts = []
    for source in targets:
        verdict = independently_verify_source(source, vtd)
        verdicts.append(verdict)

    return SourceVerificationResult(
        verdicts=verdicts,
        overall=aggregate_source_verdicts(verdicts)
    )
```

**Conformance requirement (CR-H1):** For E-class VTDs, every verifier on the committee MUST execute `verify_sources_eclass()` and include the `SourceVerificationResult` in their verification opinion. A verifier that skips source verification MUST have their opinion discounted by 50%.

**Cross-verifier evidence correlation (C10 hardening):**

When multiple verifiers independently check the same E-class claim, their source verification results are compared before fusion. This detects single-point-of-failure evidence and rewards genuine independence.

```python
def correlate_verifier_evidence(verifier_results, vtd):
    """
    Compare independently-gathered evidence across verifiers.

    Signal interpretation:
    - Different sources agreeing -> HIGH confidence (genuine independence)
    - Same source, same conclusion -> MEDIUM confidence (single-point-of-failure)
    - Different sources disagreeing -> FLAG for investigation
    - Same source, different conclusions -> CRITICAL FLAG (interpretation error)
    """
    source_matrix = build_source_usage_matrix(verifier_results)
    independence_score = compute_evidence_independence(source_matrix)
    agreement_score = compute_cross_verifier_agreement(source_matrix)

    if independence_score > 0.7 and agreement_score > 0.8:
        return EvidenceCorrelation(strength="HIGH", boost=0.05)
    elif independence_score < 0.3:
        return EvidenceCorrelation(strength="LOW", penalty=0.10,
            note="Single-point-of-failure: all verifiers used same source")
    elif agreement_score < 0.5:
        return EvidenceCorrelation(strength="CONFLICT", penalty=0.20,
            note="Verifiers disagree on source interpretation")
    else:
        return EvidenceCorrelation(strength="MEDIUM", boost=0.0)

def apply_evidence_correlation(base_opinion, correlation):
    """Adjust opinion based on evidence correlation analysis."""
    if correlation.boost > 0:
        adjusted_b = min(1.0, base_opinion.b + correlation.boost)
        adjusted_u = max(0.0, base_opinion.u - correlation.boost)
    elif correlation.penalty > 0:
        adjusted_b = max(0.0, base_opinion.b - correlation.penalty)
        adjusted_u = min(1.0, base_opinion.u + correlation.penalty)
    else:
        return base_opinion
    return normalize(Opinion(adjusted_b, base_opinion.d, adjusted_u, base_opinion.a))
```

**S-class verification** checks: test appropriateness for the data and hypotheses, assumption validity, arithmetic verification (recompute test statistic from summary statistics), and conclusion validity relative to results.

**P-class verification** checks: process specification exists and is registered, all required steps present, temporal ordering is valid, deviations are justified. CACT process trace consistency checks (Section 8.3.4) provide additional assurance.

**R-class verification** checks: logical validity of each inference step, premise support (verified claims or declared assumptions), assumption disclosure completeness, and derivability of conclusion from premises.

**K-class verification** follows a six-step protocol:

```python
def verify_k_class(vtd: VTD, committee: Set[AgentId],
                    epoch: EpochNum) -> VerificationResult:
    body = vtd.proof_body
    checks = []

    # --- Step 1: Provenance Diversity Check ---
    unique_agents = set(sq.contributing_agent for sq in body.source_quanta)
    unique_parcels = set(sq.parcel_id for sq in body.source_quanta)

    if len(unique_agents) < 5:
        return VerificationResult(
            status="REJECTED",
            reason="Insufficient agent diversity: need >=5, got " +
                   str(len(unique_agents)),
            opinion=Opinion(b=0, d=0.8, u=0.2, a=0.6))

    if len(unique_parcels) < 3:
        return VerificationResult(
            status="REJECTED",
            reason="Insufficient parcel diversity: need >=3, got " +
                   str(len(unique_parcels)),
            opinion=Opinion(b=0, d=0.8, u=0.2, a=0.6))

    # Check max agent share
    agent_counts = Counter(sq.contributing_agent for sq in body.source_quanta)
    total_quanta = len(body.source_quanta)
    max_share = max(agent_counts.values()) / total_quanta
    if max_share > 0.30:
        return VerificationResult(
            status="REJECTED",
            reason=f"Agent concentration too high: {max_share:.0%} > 30%",
            opinion=Opinion(b=0, d=0.7, u=0.3, a=0.6))

    # Verify declared provenance matches actual
    if body.provenance_summary.total_agents != len(unique_agents):
        checks.append(("provenance_mismatch", -0.15))
    if body.provenance_summary.total_parcels != len(unique_parcels):
        checks.append(("provenance_mismatch", -0.15))
    if body.provenance_summary.max_agent_share < max_share - 0.01:
        checks.append(("provenance_understated", -0.20))

    # Verify each source quantum exists and has adequate credibility
    for sq in body.source_quanta:
        source_opinion = lookup_claim_credibility(sq.claim_id)
        if source_opinion is None:
            checks.append(("missing_source_" + sq.claim_id, -0.10))
        elif expected_probability(source_opinion) < 0.50:
            checks.append(("low_cred_source_" + sq.claim_id, -0.05))

    provenance_score = max(0.0, 1.0 + sum(p for _, p in checks))

    # --- Step 2: Reasoning Chain Validity ---
    valid_quanta_ids = set(sq.claim_id for sq in body.source_quanta)
    chain_score = 1.0

    for step in body.synthesis_chain:
        for qid in step.input_quanta:
            if qid not in valid_quanta_ids:
                chain_score -= 0.15  # References non-existent source
        if len(step.reasoning.strip()) < 50:
            chain_score -= 0.10  # Too terse to evaluate
        if len(step.input_quanta) > 1 and not step.reconciliation_notes:
            chain_score -= 0.05  # Multi-source step without reconciliation
        valid_quanta_ids.add(step.step_id)

    chain_score = max(0.0, chain_score)

    # --- Step 3: Falsification Statement Quality ---
    falsification_score = 1.0
    if not body.falsification_statement.statement or \
       len(body.falsification_statement.statement.strip()) < 30:
        falsification_score -= 0.40
    if len(body.falsification_statement.conditions) < 1:
        falsification_score -= 0.30
    has_invalidating = any(
        c.impact == "INVALIDATES"
        for c in body.falsification_statement.conditions
    )
    if not has_invalidating:
        falsification_score -= 0.20
    if not body.falsification_statement.testable:
        falsification_score -= 0.15
    falsification_score = max(0.0, falsification_score)

    # --- Step 4: Cross-Domain Coherence Assessment ---
    coherence_opinions = []
    for member in committee:
        member_opinion = member.assess_k_class_coherence(
            source_quanta=body.source_quanta,
            synthesis_chain=body.synthesis_chain,
            falsification=body.falsification_statement,
            voting_record=body.voting_record
        )
        coherence_opinions.append(member_opinion)
    coherence_fused = cumulative_fusion_all(coherence_opinions)

    # --- Step 5: Voting Record Validation ---
    voting_penalty = 0.0
    if len(body.voting_record.passes) < 3:
        voting_penalty = 0.20
    for pass_record in body.voting_record.passes:
        if len(pass_record.voters) < 3:
            voting_penalty += 0.05

    # --- Step 6: Compose Final Opinion ---
    mechanical_score = (
        0.30 * provenance_score +
        0.30 * chain_score +
        0.20 * falsification_score +
        0.20 * (1.0 - voting_penalty)
    )
    mechanical_opinion = Opinion(
        b=mechanical_score * 0.8,
        d=(1.0 - mechanical_score) * 0.6,
        u=1.0 - mechanical_score * 0.8 - (1.0 - mechanical_score) * 0.6,
        a=0.6  # K-class base rate
    )
    mechanical_opinion = normalize(mechanical_opinion)
    combined = conjunction(mechanical_opinion, coherence_fused)

    return VerificationResult(
        status="VERIFIED" if expected_probability(combined) >= 0.70
               else "REJECTED",
        opinion=combined
    )
```

### 6.3 Tier 3: Attestation Review + Adversarial Probing Protocol

Tier 3 verification applies to H-class and N-class claims. Adversarial probing is MANDATORY for all Tier 3 claims. Under AVAP (Section 13), committee opinions are submitted via sealed commit-reveal protocol.

```python
def verify_tier3(vtd: VTD, committee: Set[AgentId], epoch: EpochNum):
    # Phase 1-2: Schema and completeness validation
    # Phase 3: Counter-evidence (MUST have items, not just considered=true)
    if not vtd.counter_evidence.considered or len(vtd.counter_evidence.items) == 0:
        suspicion_penalty = 0.15  # No counter-evidence for Tier 3 is suspicious

    # Phase 4: Class-specific structural checks
    # H-class: >= 2 genuine alternatives, criteria weights sum to 1.0,
    #          complete evaluation matrix, calibrated confidence
    # N-class: constitutional references, stakeholder analysis,
    #          alternative positions, framework justification

    # Phase 5: CACT commitment chain verification (if present)
    if vtd.cact_extension and vtd.cact_extension.commitment_chain:
        cact_result = verify_cact_commitments(vtd)
        # Adjust opinion based on commitment chain validity

    # Phase 6: MANDATORY adversarial probing
    probe_result = invoke_adversarial_probing(vtd, epoch)

    # Phase 7: Expert committee evaluation with structured disagreement
    # Under AVAP: sealed commit-reveal for opinions
    committee_opinions = [evaluate_attestation(m, vtd, probe_result)
                          for m in committee]
    fused = cumulative_fusion_all(committee_opinions)

    # Phase 8: Merge probe results into final opinion
    final = merge_probe_result_opinion(fused, probe_result)
```

**Structured Disagreement Protocol** for Tier 3 committees:

1. Independent assessment (parallel): Each member reviews VTD independently.
2. Cross-review (sequential): Each member reviews one other member's assessment.
3. Synthesis: Cumulative fusion of individual opinions weighted by cross-review agreement.
4. Dissent recording: Dissenting opinions preserved; later validation increases dissenter's credibility.

### 6.4 Cross-Tier: Deep-Audit Protocol

The deep-audit protocol randomly selects 7% (default) of passed VTDs for full-replication re-verification. Selection is VRF-based and unpredictable.

**Stratified sampling** (enhanced per C10 analysis) ensures coverage across strata:

```python
def select_for_deep_audit_stratified(passed_claims, epoch,
                                      audit_rate=0.07):
    """
    Stratified deep-audit selection. Guarantees minimum coverage per
    stratum while maintaining the overall audit rate.
    """
    audit_seed = SHA256(b"DEEP_AUDIT" + uint64_be(epoch) + vrf_seed(epoch))

    # Phase 1: Stratify claims
    agent_strata = group_by(passed_claims, key=lambda c: c.producing_agent)
    domain_strata = group_by(passed_claims, key=lambda c: c.locus[:2])

    # Phase 2: Mandatory stratum coverage
    mandatory = set()
    for agent, claims in agent_strata.items():
        if len(claims) >= 3:
            stratum_hash = SHA256(audit_seed + agent.encode())
            idx = uint256_from_bytes(stratum_hash) % len(claims)
            mandatory.add(claims[idx].claim_id)

    for domain, claims in domain_strata.items():
        if len(claims) >= 5:
            stratum_hash = SHA256(audit_seed + domain.encode())
            idx = uint256_from_bytes(stratum_hash) % len(claims)
            mandatory.add(claims[idx].claim_id)

    # Phase 3: Fill remaining audit budget with random selection
    target_count = max(len(mandatory),
                       int(audit_rate * len(passed_claims)))
    remaining_budget = target_count - len(mandatory)

    remaining_claims = [c for c in passed_claims
                        if c.claim_id not in mandatory]
    random_selected = set()
    for claim in remaining_claims:
        if len(random_selected) >= remaining_budget:
            break
        selection_hash = SHA256(audit_seed + claim.claim_id.encode())
        effective_rate = audit_rate * (1 + log2(1 + claim.citation_count))
        if uint256_from_bytes(selection_hash) < int(effective_rate * 2**256):
            random_selected.add(claim.claim_id)

    return mandatory | random_selected
```

**Citation-weighted bias:** Heavily cited claims have higher effective audit rates. A claim with C citations has its rate multiplied by (1 + log2(1 + C)).

**Correlated claim caveat.** The detection probability formula P(detected within T epochs) = 1 - (1 - r)^T assumes independent claim quality. This assumption breaks when claims are correlated -- for example, when a single agent produces many claims in the same epoch, or when multiple agents submit claims about the same knowledge domain using shared source material. Stratified sampling ensures that a coordinated attack targeting a single domain or executed by a single agent cannot evade audit through statistical luck. The stratification dimensions are:

1. **Agent stratum:** Claims from the same producing agent are grouped. At least one claim per agent-epoch pair with >= 3 claims SHOULD be audited.
2. **Domain stratum:** Claims within the same knowledge locus (first two path segments) are grouped. At least one claim per locus-epoch pair with >= 5 claims SHOULD be audited.
3. **Dependency stratum:** Claims sharing >= 2 common dependencies are grouped. At least one claim per dependency cluster SHOULD be audited.

**Audit procedure:**
1. Select independent audit committee (no overlap with original verifiers or probers).
2. Each auditor independently evaluates the claim via full replication.
3. Fuse auditor opinions via cumulative fusion.
4. Compare audit credibility with original verification credibility.
5. If discrepancy exceeds threshold (0.25): credibility downgrade, agent investigation, cascade re-verification of agent's recent claims, Sentinel Graph alert.

**Statistical guarantees:** At 7% audit rate, a forged claim has a >99% probability of being audited within 65 epochs (approximately 65 hours at 1-hour epochs). The formula: P(detected within T epochs) = 1 - (1 - r)^T.

---

## 7. Adversarial Probing System

### 7.1 Probe Types and Strategies

Adversarial probing supplements formal verification for Tier 2 and Tier 3 claims. Six probe types test claims from different angles (five original plus KI from CACT):

| Probe Type | ID | Description |
|-----------|-----|-------------|
| Counterexample Search | CX | Construct specific counterexamples to the claim |
| Assumption Exposure | AE | Identify unstated assumptions the claim relies on |
| Source Challenge | SC | Verify cited sources actually support the claim |
| Logical Fallacy Detection | LF | Check for common reasoning errors |
| Boundary Probing | BP | Test claim at edge cases and boundary conditions |
| Knowledge Interrogation | KI | Direct questioning of producing agent about content they should know if VTD is genuine (CACT) |

Probe type selection is class-specific:

| Class | Probe Types |
|-------|-------------|
| E | CX, SC, AE |
| S | CX, LF, AE, BP |
| P | AE, BP |
| R | CX, LF, AE |
| K | CX, AE, SC |
| H | CX, AE, BP, LF |
| N | AE, LF, BP |

KI probes are applied across all classes when CACT is active and the claim has verifiable sources. See Section 8.3.3 for the full KI protocol.

### 7.2 Prober Selection

Probers are selected via VRF independently of verification committees. A prober MUST NOT be the producing agent, MUST NOT be on the verification committee, and SHOULD be from a different diversity pool than the committee majority.

```python
def select_adversarial_probers(claim, epoch, verification_committee):
    # Different VRF domain separator ensures independence
    alpha = SHA256(b"ADVERSARIAL_PROBE" + claim.hash + uint64_be(epoch)
                   + vrf_seed(epoch))
    excluded = {claim.producing_agent} | verification_committee
    eligible = get_eligible_probers(claim.locus, exclude=excluded)
    # Sort by VRF output, select top N
    # Tier 2: 1 prober (when triggered). Tier 3: 2 probers (always).
```

### 7.3 Probe Execution and Evaluation

Each probe includes:
- A base strategy from the probe strategy library.
- A generative component: dynamically generated probe questions using a VRF-derived seed. This defends against the Inoculation Attack (Attack 4), where agents pre-fabricate responses to anticipated probe strategies.
- A meta-probe: checks whether VTD responses appear pre-fabricated (suspiciously precise matches to anticipated attack patterns).

**Probe result aggregation:**

| Finding | Overall Verdict |
|---------|----------------|
| Any CRITICAL severity or confirmed counterexample | FALSIFIED |
| Any HIGH severity or plausible counterexample | WEAKENED |
| All findings NO_ISSUE | SURVIVED |
| Meta-probe detects inoculation + SURVIVED | WEAKENED (downgrade) |

**Impact on credibility opinion:**
- FALSIFIED: opinion set to (b=0, d=0.9, u=0.1, a).
- WEAKENED: belief reduced by 30%, transferred to uncertainty.
- SURVIVED: belief boosted by 0.05 (probe survival is positive evidence).

### 7.4 Anti-Inoculation Measures

The Inoculation Attack (Attack 4) occurs when an agent pre-fabricates responses to anticipated probe strategies. PCVM defends through:

1. **Generative probe component:** Probes include dynamically generated questions not drawn from any fixed library.
2. **Strategy opacity:** Probe strategies use VRF-derived seeds unknown to the producing agent.
3. **Meta-probing:** A secondary check evaluates whether VTD responses to probe questions appear suspiciously convenient (pre-fabricated suspicion score > 0.70 triggers downgrade).

### 7.5 Probing Budget Allocation

**1 probe token = 1 AIC (Atrahasis Intelligence Coin).**

A probe token represents the cost of one atomic verification operation performed by a prober. The Settlement Plane denominates all PCVM costs in AIC; probe budgets are denominated in the same unit to enable direct cost accounting.

**Probe Operation Costs:**

| Operation | AIC Cost | Description |
|-----------|----------|-------------|
| Source fetch + hash check | 2 AIC | HTTP GET + SHA-256 comparison |
| Quote fuzzy match | 3 AIC | Substring matching with threshold |
| Contextual relevance assessment (Level 4) | 15 AIC | Semantic analysis of source-claim relationship |
| Counterexample generation (CX) | 25 AIC | Generate and evaluate a specific counterexample |
| Assumption exposure (AE) | 20 AIC | Identify and articulate unstated assumption |
| Logical fallacy check (LF) | 15 AIC | Check one inference step for named fallacies |
| Boundary probe (BP) | 20 AIC | Construct and evaluate one edge case |
| Knowledge interrogation (KI) | 30 AIC | Generate and evaluate one KI question set |
| Meta-probe (inoculation check) | 10 AIC | Assess whether VTD responses appear pre-fabricated |

**Base Budgets by Class:**

| Class | Base Budget (AIC) |
|-------|-------------------|
| E | 500 |
| S | 400 |
| P | 200 |
| R | 400 |
| K | 600 |
| H | 800 |
| N | 700 |

```python
def compute_probe_budget(claim_class: str, risk_level: str,
                         agent_credibility: float) -> int:
    """
    Compute total probe budget in AIC.

    Returns:
        Budget in AIC (1 AIC = 1 probe token). This is the maximum
        the prober may spend on verification operations for this claim.
        Unspent budget is not charged to the Settlement Plane.
    """
    BASE_BUDGETS_AIC = {
        "E": 500, "S": 400, "P": 200, "R": 400,
        "H": 800, "N": 700, "K": 600
    }
    RISK_MULTIPLIERS = {
        "LOW": 0.5, "MEDIUM": 1.0, "HIGH": 2.0, "CRITICAL": 3.0
    }
    base = BASE_BUDGETS_AIC[claim_class]
    risk_factor = RISK_MULTIPLIERS[risk_level]
    # Low-credibility agents get more probing (range 1.0 to 2.0)
    credibility_factor = 2.0 - min(max(agent_credibility, 0.0), 1.0)
    raw_budget = base * risk_factor * credibility_factor
    return min(int(raw_budget), 5000)  # 5000 AIC hard cap
```

**Settlement Integration:**
- Probe budget is **reserved** from the Settlement Plane when probing is initiated.
- Only **actually spent** AIC is charged. If a prober spends 300 AIC of a 500 AIC budget, the remaining 200 AIC is released.
- The producing agent bears 0% of probe cost (probing is a system verification cost).
- Probe costs are distributed across verification committee members' epoch settlement as a shared system expense.
- Probers who find confirmed errors (FALSIFIED or WEAKENED verdict) receive a quality bonus of 10% of the spent budget from the Settlement Plane's verification reward pool.

---

## 8. CACT: Commit-Attest-Challenge-Triangulate

CACT is the primary VTD forgery defense subsystem. It escapes the infinite trust regress -- where verifying Source B requires Source C, which requires Source D -- by shifting verification from the evidence chain to orthogonal channels that the forger cannot control.

### 8.1 Architecture

CACT addresses VTD forgery through four interlocking mechanisms:

1. **Temporal Commitment Binding (Commit):** Agents cryptographically commit to evidence and intermediate work products in real-time during VTD construction, before knowing which claims will be challenged. Retroactive fabrication becomes cryptographically impossible without breaking SHA-256 or the discrete logarithm assumption (Pedersen commitments).

2. **Verifiable Computation Attestation (Attest):** Where VTD claims involve computation, SNARK/STARK proofs make computational integrity mathematically verifiable with soundness error ~2^-128 (Groth16/PLONK) or ~2^-80 (STARK/FRI). The verifier need not trust the prover or re-execute the computation.

3. **Adversarial Interrogation Protocol (Challenge):** VTD producers must defend their claims under Knowledge Interrogation (KI) probing that tests the generative knowledge behind the VTD, not just the VTD's content. Three question categories -- factual recall, cross-reference consistency, negative knowledge -- are generated dynamically from independently retrieved source content.

4. **Multi-Channel Orthogonal Verification (Triangulate):** VTD validity is confirmed through structurally independent channels -- process traces, environmental side-effects -- that a forger would need to simultaneously fake across multiple systems.

### 8.2 CACT Applicability by Claim Class

| Class | Commitment Chain | Verifiable Computation | Knowledge Interrogation | Process Trace | Environmental Audit |
|-------|:---:|:---:|:---:|:---:|:---:|
| D | REQUIRED | REQUIRED (SNARK/STARK) | Optional | Optional | Optional |
| C | Recommended | N/A | Optional | Optional | N/A |
| E | Recommended | N/A | REQUIRED | Recommended | Recommended |
| S | Recommended | Optional | Recommended | Recommended | Optional |
| P | Recommended | N/A | Optional | REQUIRED | Optional |
| R | Optional | N/A | Optional | Optional | N/A |
| K | Recommended | N/A | Recommended | Recommended | Optional |
| H | Optional | N/A | Recommended | Optional | N/A |
| N | Optional | N/A | Optional | Optional | N/A |

### 8.3 Verification Protocols

#### 8.3.1 Commitment Chain Verification (Phase 0)

Commitment chain verification is the first phase of CACT-extended verification, executed before class-specific verification. The commitment chain is a sequential, hash-linked log of evidence commitments made during VTD construction. Each commitment records an evidence hash, a blinded purpose hash, and a timestamp, linked to the previous commitment via hash chaining.

The full `verify_commitment_chain()` and `verify_cact_commitments()` algorithms verify structural integrity (sequential numbering, hash linking, temporal ordering, rate limiting, chain hash, agent signature) and semantic validity (purpose reveals match committed hashes, evidence cited in VTD appears in chain, all commitments precede VTD submission).

**Credibility adjustments based on commitment verification:**
- Binding ratio >= 0.90: +0.05 credibility boost (well-committed evidence)
- Binding ratio 0.50-0.90: no adjustment
- Binding ratio < 0.50: -0.10 credibility penalty, flag LOW_COMMITMENT_COVERAGE
- CACT extension absent (non-D-class): credibility capped at 0.70

#### 8.3.2 Verifiable Computation Verification (D-class, S-class)

For D-class VTDs with proof_type SNARK_PROOF or STARK_PROOF, the verifier checks the zero-knowledge proof without re-executing the computation. The protocol retrieves the verification key for the declared circuit, confirms the key hash matches, verifies the proof against public inputs, and cross-checks that public inputs appear in the commitment chain (preventing fabricated-input attacks).

Supported proof systems: Groth16, PLONK, STARK/FRI, Nova.

**Soundness bounds:** Groth16/PLONK: ~2^-128. STARK/FRI: ~2^-80 (larger but post-quantum secure).

#### 8.3.3 Knowledge Interrogation (KI) Protocol

The KI probe type tests whether the producing agent possesses the generative knowledge required to honestly produce the VTD. Three question categories are generated dynamically using VRF-derived seeds:

- **Q1 (Factual Recall):** Specific values, names, dates from cited sources.
- **Q2 (Cross-Reference Consistency):** Relationships between multiple sources.
- **Q3 (Negative Knowledge):** What the sources explicitly do NOT claim.

Questions are generated from independently retrieved source content, not from the VTD itself. This prevents the forger from pre-computing answers.

**KI Verdicts:**
- Accuracy >= 0.80 (KI_PASS_THRESHOLD): SURVIVED, +0.05 credibility
- Accuracy 0.50-0.80 (KI_MARGINAL_THRESHOLD): WEAKENED, -0.10 credibility
- Accuracy < 0.50: FAILED, -0.30 credibility

#### 8.3.4 Process Trace Consistency

Process trace analysis checks whether the VTD's construction process is consistent with how genuine VTDs are produced. Five checks (P1-P5): temporal plausibility, activity sequence plausibility, resource consumption consistency, source retrieval timing vs. commitment chain, and draft revision patterns.

**Credibility adjustments:**
- Consistency score > 0.8: +0.05 credibility boost
- Consistency score < 0.5: -0.10 credibility penalty
- Process trace absent: credibility capped at 0.75

#### 8.3.5 Environmental Side-Effect Audit

Environmental audit checks external system records for evidence consistent with the agent's claimed activities: source access logs (E1), API call records (E2), and computational resource records (E3). The membrane queries external systems directly, not through the agent. VRF selects which external systems to audit.

### 8.4 Orthogonal Verification Coverage (OVC) Score

The OVC score measures how many independent verification channels provided usable signals. It is computed as a weighted mean of four channel scores:

```python
def compute_ovc_score(commitment_result, ki_result,
                       process_result, env_result):
    """
    OVC = weighted mean of channel scores.
    Weights: commitment=0.30, KI=0.25, process=0.20, env=0.25
    Score range: [0.0, 1.0]
    """
    channel_scores = []

    # Channel 1: Commitment chain
    if commitment_result.status == "VERIFIED":
        channel_scores.append(min(1.0, commitment_result.binding_ratio))
    else:
        channel_scores.append(0.0)

    # Channel 2: Knowledge interrogation
    if ki_result.status == "SURVIVED":
        channel_scores.append(ki_result.accuracy)
    elif ki_result.status == "NOT_APPLICABLE":
        channel_scores.append(0.5)  # Neutral
    else:
        channel_scores.append(0.0)

    # Channel 3: Process trace
    if process_result.status == "CHECKED":
        channel_scores.append(process_result.consistency_score)
    else:
        channel_scores.append(0.0)

    # Channel 4: Environmental audit
    if env_result.status == "CHECKED":
        channel_scores.append(env_result.environmental_score)
    else:
        channel_scores.append(0.5)  # Neutral

    weights = [0.30, 0.25, 0.20, 0.25]
    return clamp(sum(w * s for w, s in zip(weights, channel_scores)), 0.0, 1.0)
```

### 8.5 CACT Credibility Integration

CACT results feed into the Credibility Engine (Section 9) via an OVC-based belief cap:

```python
def apply_cact_credibility_adjustments(base_opinion, ovc_score,
    commitment_result, ki_result, process_result, env_result, vtd):
    """
    Apply CACT credibility adjustments. Called AFTER standard PCVM
    verification and BEFORE knowledge admission.
    """
    opinion = copy(base_opinion)

    # Step 1: OVC-based belief cap
    # OVC_MIN_CAP = 0.50, OVC_MAX_CAP = 0.95
    ovc_belief_cap = 0.50 + ovc_score * 0.45
    if opinion.b > ovc_belief_cap:
        excess = opinion.b - ovc_belief_cap
        opinion.b = ovc_belief_cap
        opinion.u += excess  # Excess belief becomes uncertainty

    # Step 2: Channel-specific adjustments (additive)
    adjustments = [
        commitment_result.credibility_boost,
        ki_result.credibility_adjustment,
        process_result.credibility_adjustment,
        env_result.credibility_adjustment
    ]
    total_adjustment = sum(a for a in adjustments if a is not None)
    total_adjustment = clamp(total_adjustment, -0.30, 0.15)

    if total_adjustment > 0:
        opinion.b = min(opinion.b + total_adjustment, ovc_belief_cap)
        opinion.u = max(0, opinion.u - total_adjustment)
    elif total_adjustment < 0:
        opinion.b = max(0, opinion.b + total_adjustment)
        opinion.u = min(1, opinion.u - total_adjustment)

    return normalize(opinion)
```

### 8.6 Detection Probability Analysis

CACT raises the combined detection probability for sophisticated forgers:

| Forger Type | Base PCVM Detection | With CACT Detection |
|-------------|:---:|:---:|
| Naive (fabricated URLs) | 0.95 | 0.99 |
| Moderate (real sources, misrepresented) | 0.60 | 0.78 |
| Sophisticated (consistent fabrication) | 0.434 | 0.611 |
| Perfect (all channels faked) | 0.07 (deep-audit only) | 0.15 |

The improvement for sophisticated forgers (0.434 -> 0.611) comes from requiring simultaneous fabrication across orthogonal channels. A forger who can fake an evidence chain may not be able to simultaneously fake temporal commitments (requires pre-planning before knowing what will be challenged), KI responses (requires generative knowledge of fabricated sources), process traces (requires consistent construction timing), and environmental side-effects (requires control of external systems).

---

## 9. Credibility Engine

### 9.1 Subjective Logic Foundations

PCVM uses Josang's Subjective Logic [10] to represent epistemic uncertainty about claim credibility. An opinion tuple w = (b, d, u, a) represents belief about a binary proposition:

- **b** (belief): evidence in favor, b >= 0
- **d** (disbelief): evidence against, d >= 0
- **u** (uncertainty): lack of evidence, u >= 0
- **a** (base rate): prior probability absent evidence, a in [0, 1]
- **Constraint:** b + d + u = 1

The **expected probability** (credibility score): E(w) = b + a * u

Key reference opinions:
- Vacuous (total ignorance): w = (0, 0, 1, 0.5)
- Dogmatic belief: w = (1, 0, 0, a)
- Dogmatic disbelief: w = (0, 1, 0, a)

### 9.2 Opinion Initialization per Claim Class

Each claim class has initialization strategies reflecting the nature of the knowledge:

| Class | Verified Opinion | Initial Opinion | Decay Model | Base Rate |
|-------|-----------------|-----------------|-------------|-----------|
| D | (1.0, 0, 0, 0.5) | (0, 0, 1, 0.5) | None (proofs do not expire) | 0.5 |
| C | (1.0, 0, 0, 0.5) | (0, 0, 1, 0.5) | On regulation change | 0.5 |
| E | Full tuple | (0, 0, 1, 0.5) | Half-life (180 days default) | 0.5 |
| S | Full tuple | (0, 0, 1, 0.5) | On new data availability | 0.5 |
| P | (1.0, 0, 0, 0.5) | (0, 0, 1, 0.5) | On process spec change | 0.5 |
| R | Full tuple | (0, 0, 1, 0.5) | On premise change | 0.5 |
| K | Full tuple | (0, 0, 1, 0.6) | Half-life (270 days) + on source credibility change | 0.6 |
| H | Full tuple | (0, 0, 1, 0.7) | Half-life (180 days) | 0.7 |
| N | Full tuple | (0, 0, 1, 0.5) | On constitutional amendment | 0.5 |

Note: H-class has a higher base rate (a=0.7) reflecting the inherently uncertain nature of heuristic claims. K-class base rate (a=0.6) is between the default 0.5 and H-class 0.7, reflecting moderate prior probability of consolidation soundness.

### 9.3 Composition Operators

Three primary operators compose opinions through dependency chains.

**Conjunction (AND).** Used when a conclusion requires both premise A and premise B. From Josang (2016), Definition 12.1:

```python
def conjunction(w_A, w_B):
    b_C = w_A.b * w_B.b
    d_C = w_A.d + w_B.d - w_A.d * w_B.d
    u_C = w_A.b * w_B.u + w_A.u * w_B.b + w_A.u * w_B.u
    a_C = w_A.a * w_B.a
    return normalize(b_C, d_C, u_C, a_C)
```

Property (INV-M6): conjunction(w_A, w_B).b <= min(w_A.b, w_B.b). Belief never increases through conjunction.

**Discounting (Transitive Trust).** Used when agent X reports opinion w_A, and we have trust w_X in agent X. From Josang (2016), Definition 14.2:

```python
def discounting(w_trust, w_claim):
    b = w_trust.b * w_claim.b
    d = w_trust.b * w_claim.d
    u = w_trust.d + w_trust.u + w_trust.b * w_claim.u
    a = w_claim.a
    return Opinion(b, d, u, a)
```

Property: If w_trust.b = 0, then discounted.b = 0 and discounted.u = 1. Complete distrust yields complete uncertainty.

**Cumulative Fusion (Consensus).** Used when two independent agents report opinions about the same claim. From Josang (2016), Definition 12.6:

```python
def cumulative_fusion(w_A, w_B):
    if w_A.u == 0 and w_B.u == 0:
        return weighted_average(w_A, w_B, gamma=0.5)
    denom = w_A.u + w_B.u - w_A.u * w_B.u
    b = (w_A.b * w_B.u + w_B.b * w_A.u) / denom
    d = (w_A.d * w_B.u + w_B.d * w_A.u) / denom
    u = (w_A.u * w_B.u) / denom
    a = (w_A.a * w_B.u + w_B.a * w_A.u) / (w_A.u + w_B.u)
    return normalize(b, d, u, a)
```

Property: cumulative_fusion(w_A, w_B).u <= min(w_A.u, w_B.u). Uncertainty never increases through consensus of independent opinions.

### 9.4 Evidence Belief Cap with Temporal Decay (C10 Hardening)

Evidence-based claims have a maximum belief (evidence belief cap) that decays over time to prevent overconfidence in aging evidence:

```python
def compute_max_belief_from_sources(vtd, current_epoch):
    """
    Compute the maximum belief justified by the VTD's evidence quality.

    For E-class and S-class claims, belief is capped by source quality
    and freshness. This prevents a strong initial opinion from persisting
    after evidence becomes stale.
    """
    if vtd.assigned_class not in ("E", "S", "K"):
        return 1.0  # No evidence-based cap for non-empirical classes

    source_quality = assess_aggregate_source_quality(vtd)
    age_days = (current_epoch - vtd.epoch) * EPOCH_DURATION_HOURS / 24

    if vtd.assigned_class == "E":
        half_life = E_CLASS_HALF_LIFE_DAYS  # 180
    elif vtd.assigned_class == "K":
        half_life = K_CLASS_HALF_LIFE_DAYS  # 270
    else:
        half_life = 365  # S-class default

    decay_factor = 0.5 ** (age_days / half_life)
    return source_quality * decay_factor

def enforce_evidence_belief_cap(opinion, max_belief):
    """Cap belief at the evidence-justified maximum."""
    if opinion.b > max_belief:
        excess = opinion.b - max_belief
        return Opinion(
            b=max_belief,
            d=opinion.d,
            u=opinion.u + excess,
            a=opinion.a
        )
    return opinion
```

### 9.5 Forgery Detection Heuristics (C10 Hardening)

Four signals contribute to a forgery suspicion score:

```python
def compute_forgery_suspicion_score(vtd, agent_history, epoch):
    """
    Compute a composite forgery suspicion score from four independent
    heuristic signals.

    H1: Unusually high VTD production rate
    H2: Source verifiability ratio (what % of sources can be independently verified)
    H3: Deep-audit discrepancy history
    H4: Citation pattern anomalies (citing non-existent or low-credibility claims)
    """
    scores = []

    # H1: Production rate anomaly
    recent_vtds = count_recent_vtds(vtd.producing_agent, lookback_epochs=50)
    rate_z_score = (recent_vtds - MEAN_PRODUCTION_RATE) / STD_PRODUCTION_RATE
    if rate_z_score > 2.0:
        scores.append(("H1_RATE", min(1.0, rate_z_score / 5.0)))

    # H2: Source verifiability
    if hasattr(vtd.proof_body, 'sources') and vtd.proof_body.sources:
        verifiable = sum(1 for s in vtd.proof_body.sources
                        if s.source_type in ("PEER_REVIEWED_PAPER", "OFFICIAL_REPORT",
                                             "DATABASE", "VERIFIED_CLAIM"))
        ratio = verifiable / len(vtd.proof_body.sources)
        if ratio < 0.5:
            scores.append(("H2_VERIFIABILITY", 1.0 - ratio))

    # H3: Audit discrepancy history
    discrepancy_rate = get_audit_discrepancy_rate(vtd.producing_agent)
    if discrepancy_rate > AUDIT_DISCREPANCY_THRESHOLD:  # 0.15
        scores.append(("H3_AUDIT", discrepancy_rate))

    # H4: Citation pattern anomalies
    citation_anomaly = check_citation_patterns(vtd)
    if citation_anomaly > 0.3:
        scores.append(("H4_CITATION", citation_anomaly))

    if not scores:
        return 0.0

    # Weighted combination
    total = sum(s for _, s in scores) / len(scores)
    return clamp(total, 0.0, 1.0)
```

When forgery suspicion score exceeds 0.50, escalation triggers: increased probe rate, mandatory deep-audit, Sentinel Graph alert, and potential C8 DSF slashing investigation.

### 9.6 Propagation Through Knowledge Graph

Credibility propagates through the claim dependency graph. For DAGs, a single-pass topological sort suffices (O(|edges|)):

```python
def propagate_credibility(claims, opinions, agent_trust, graph):
    if graph.has_cycles():
        return propagate_with_dampening(claims, opinions, agent_trust, graph)

    for claim_id in graph.topological_sort():
        # Step 1: Discount by class-specific agent trust (INV-M4)
        trust = agent_trust.get((claim.agent_id, claim.class),
                                default_trust)
        discounted = discounting(trust, base_opinion)

        # Step 2: Conjoin with dependencies
        for dep in graph.get_dependencies(claim_id):
            dep_opinion = result[dep.claim_id]
            discounted = conjunction(discounted, dep_opinion)

        result[claim_id] = discounted
```

### 9.7 Cycle Handling

For cyclic dependency graphs, PCVM applies iterative dampening analogous to PageRank:

```python
def propagate_with_dampening(claims, opinions, agent_trust, graph):
    alpha = 0.85  # dampening factor
    epsilon = 0.001  # convergence threshold
    max_iter = 100

    current = {c: discounting(trust, base) for c in claims}

    for iteration in range(max_iter):
        next_opinions = {}
        max_delta = 0.0
        for claim_id in claims:
            composed = current[claim_id]
            for dep in graph.get_dependencies(claim_id):
                composed = conjunction(composed, current[dep.claim_id])
            dampened = Opinion(
                b = alpha * composed.b + (1-alpha) * base.b,
                d = alpha * composed.d + (1-alpha) * base.d,
                u = alpha * composed.u + (1-alpha) * base.u,
                a = composed.a
            )
            dampened = normalize(dampened)
            next_opinions[claim_id] = dampened
            delta = abs(dampened.E() - current[claim_id].E())
            max_delta = max(max_delta, delta)

        current = next_opinions
        if max_delta < epsilon:
            return current  # Converged

    emit_sentinel_alert("CREDIBILITY_CONVERGENCE_FAILURE", ...)
    return current
```

Convergence is guaranteed within ceil(log(epsilon) / log(alpha)) iterations. For alpha=0.85, epsilon=0.001: max 44 iterations.

### 9.8 Decay and Re-Verification Triggers

Credibility decays over time according to class-specific rules:

- **D-class:** No decay. Deterministic proofs are timeless.
- **E-class:** Half-life decay (180 days default, configurable 90-365). Belief transfers to uncertainty.
- **S-class:** Triggered by new data availability. Uncertainty increases by 0.3.
- **P-class:** Triggered by process specification changes. Full reset to uncertainty.
- **R-class:** Triggered by premise credibility changes exceeding 0.2.
- **K-class:** Half-life decay (270 days). Also triggered when any source quantum's credibility drops below 0.50 or when more than 20% of source quanta have been superseded.
- **H-class:** Half-life decay (180 days).
- **N-class:** Triggered by constitutional amendments.
- **C-class:** Triggered by regulation changes.

When a claim's expected probability decays below 0.5, it is automatically queued for re-verification.

---

## 10. Knowledge Admission

### 10.1 VTD Verification to MCT Issuance

When a VTD passes verification, the membrane issues a Membrane Credibility Token (MCT) -- a signed attestation that the claim has been verified and admitted to the canonical knowledge graph.

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/mct.schema.json",
  "title": "Membrane Credibility Token",
  "type": "object",
  "required": [
    "mct_id", "claim_id", "vtd_id", "cls_id",
    "assigned_class", "tier", "credibility_opinion",
    "verification_committee", "verification_epoch",
    "admission_timestamp", "mct_hash", "membrane_signature"
  ],
  "properties": {
    "mct_id": { "type": "string", "pattern": "^mct:[a-f0-9]{16}$" },
    "claim_id": { "type": "string" },
    "vtd_id": { "type": "string" },
    "cls_id": {
      "type": "string",
      "pattern": "^mct:[DESHNPRCK]:[0-9]+:[a-f0-9]{8}:[0-9]+$",
      "description": "Classification ID: mct:<class>:<epoch>:<committee_hash>:<nonce>"
    },
    "assigned_class": { "type": "string", "enum": ["D","E","S","H","N","P","R","C","K"] },
    "tier": { "type": "string", "enum": ["FORMAL_PROOF","STRUCTURED_EVIDENCE","STRUCTURED_ATTESTATION"] },
    "credibility_opinion": {
      "type": "object",
      "required": ["b", "d", "u", "a"],
      "properties": {
        "b": { "type": "number", "minimum": 0, "maximum": 1 },
        "d": { "type": "number", "minimum": 0, "maximum": 1 },
        "u": { "type": "number", "minimum": 0, "maximum": 1 },
        "a": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "credibility_score": { "type": "number", "minimum": 0, "maximum": 1 },
    "ovc_score": { "type": ["number", "null"], "minimum": 0, "maximum": 1 },
    "verification_committee": { "type": "array", "items": { "type": "string" } },
    "adversarial_probers": { "type": "array", "items": { "type": "string" } },
    "probe_survival": { "type": ["string", "null"], "enum": ["SURVIVED","WEAKENED","NOT_PROBED",null] },
    "ki_result": { "type": ["string", "null"], "enum": ["SURVIVED","WEAKENED","FAILED","NOT_APPLICABLE",null] },
    "verification_epoch": { "type": "integer", "minimum": 0 },
    "admission_timestamp": { "type": "string", "format": "date-time" },
    "decay_policy": { "type": "string" },
    "next_reverification_epoch": { "type": ["integer", "null"] },
    "mct_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "membrane_signature": { "type": "string" }
  }
}
```

**cls_id construction:**

```python
def generate_cls_id(assigned_class: str, epoch: int,
                     committee: Set[AgentId],
                     epoch_counter: AtomicCounter) -> str:
    sorted_ids = sorted(committee)
    committee_hash = SHA256("|".join(sorted_ids).encode())[:8]  # first 8 hex
    nonce = epoch_counter.increment()
    return f"mct:{assigned_class}:{epoch}:{committee_hash}:{nonce}"
```

**Admission thresholds** vary by class:

| Class | Threshold | Rationale |
|-------|-----------|-----------|
| D | 0.95 | Deterministic claims should be near-certain |
| C | 0.90 | Compliance claims require high confidence |
| P | 0.80 | Process conformance should be high-confidence |
| R | 0.75 | Logical reasoning should be high-confidence |
| K | 0.70 | Consolidation requires higher confidence than raw empirical claims |
| S | 0.65 | Statistical claims slightly higher than empirical |
| E | 0.60 | Empirical claims tolerate moderate uncertainty |
| H | 0.50 | Heuristic claims accept significant uncertainty |
| N | 0.50 | Normative claims verified for consistency, not truth |

### 10.2 MCT to BDL Persistence

Admitted claims persist to the Bounded Durability Layer (BDL) of the Knowledge Cortex. The BDL record includes: claim content, assigned class, credibility opinion, OVC score, VTD reference, MCT reference, producing agent, locus, admission epoch, dependencies, decay policy, and re-verification schedule.

### 10.3 Contradiction Handling

When a new claim is admitted, the membrane checks for contradictions with existing claims:

1. Query Knowledge Cortex for semantically related claims (similarity threshold 0.7).
2. Assess semantic contradiction (score > 0.8 indicates contradiction).
3. Both claims persist -- contradiction does not block admission.
4. Contradiction edge recorded in the knowledge graph.
5. If new claim has higher credibility, queue existing claim for re-verification.
6. Sentinel Graph alerted for monitoring.

This design ensures that the knowledge graph accurately represents disagreement rather than forcing premature resolution.

### 10.4 Re-Verification Scheduling

The Knowledge Cortex triggers re-verification when:

1. A dependency's credibility drops below threshold.
2. A contradiction is discovered with a newly admitted claim.
3. Credibility decay crosses the re-verification threshold (0.5).
4. Deep-audit reveals systematic issues with the producer.
5. External events invalidate a class of claims (regulation change, new data).

Re-verification priority is citation-weighted: claims with more dependents are re-verified first. Maximum 100 re-verifications per epoch to prevent resource exhaustion.

---

## 11. Integration Architecture

### 11.1 Tidal Noosphere Interface

PCVM integrates with the Tidal Noosphere through the V-class operation pathway:

```
Noosphere                              PCVM
--------                              ----
1. Agent submits claim with
   proposed class
2. Noosphere schedules verification
   for epoch E+1 (1-epoch delay)
3. VRF Engine selects committee -----> 4. PCVM receives claim +
   from pre-stratified pools              committee + epoch context
   (AVAP: self-selection mode)        5. Classifier assigns class
                                      6. VTD Engine constructs VTD
                                         (CACT: commitment chain)
                                      7. Dispatcher routes to tier
                                      8. Verification executes
                                         (CACT: orthogonal channels)
                                      9. Credibility composed
                                         (CACT: OVC adjustments)
                                     10. Admission decision
11. Noosphere receives <-------------- MCT or Rejection
    MCT or Rejection
12. MCT -> Knowledge Cortex
    Rejection -> Agent notification
    MQI metrics -> Sentinel Graph
```

**Epoch alignment:** PCVM operates on the Noosphere's 1-hour tidal epoch (TIDAL_EPOCH = 3,600s) clock. Verification window: T+0 to T+50min. Audit selection: T+50min. Settlement reporting: T+55min. Epoch close: T+60min. For the canonical intra-tidal-epoch timeline and its relationship to SETTLEMENT_TICK (60s) and CONSOLIDATION_CYCLE (36,000s), see C9 Section SS3.3.

**Committee sizes by tier:**
- Tier 1 (FORMAL_PROOF): 3 members
- Tier 2 (STRUCTURED_EVIDENCE): 5 members
- Tier 3 (STRUCTURED_ATTESTATION): 7 members

> **AVAP Override (C9 errata E-C12-02):** When AVAP (Section 13) is active, per-class committee sizes are overridden to MIN=7, DEFAULT=10 to ensure sufficient anonymity set size for VRF self-selection. The tier defaults above apply only when AVAP is inactive.

**MQI Response Tiers:**

| Condition | PCVM Response |
|-----------|---------------|
| Conservative (1 metric degraded) | Increase probe rate 50%, reduce admission thresholds by 0.05 |
| Alert (3+ metrics degraded) | Probe ALL claims, increase deep-audit to 15% |
| Lockdown (sustained degradation) | Halt new admissions, re-verify 100 most recent claims |

### 11.2 Knowledge Cortex Interface

PCVM is the sole gateway for claims entering the Knowledge Cortex (INV-M1).

**Admission flow:** PCVM sends BDL records (claim + MCT + VTD reference + dependency edges + OVC score). Knowledge Cortex returns acknowledgment with conflict information.

**Query interface:** PCVM reads dependency graphs and claim credibilities for propagation. PCVM writes credibility updates, contradiction edges, and supersession records.

### 11.3 Settlement Plane Interface

PCVM reports verification quality to the Settlement Plane (C8 DSF). Verification quality is weighted at 40% of total settlement score. Economic incentives align stakeholders:

| Actor | Incentive | Mechanism |
|-------|-----------|-----------|
| Producer | Accurate claims with complete VTDs | Quality score affects 40% of settlement |
| Verifier | Thorough verification | Endorsing audit-failed claims reduces score |
| Prober | Find genuine errors | Confirmed probe findings earn quality bonus |
| Forger | Avoid detection | Slashing: 3x verification cost on detected forgery (C8) |
| Colluder | Avoid detection | Slashing: 5x committee cost on detected collusion (C8) |

**Economic deterrent integration (C10 hardening):**

```python
def verify_economic_deterrent(vtd, agent_id, epoch):
    """
    Check that economic deterrents are properly configured for this agent.
    Extends C5 Section 11.2 Attack 1 defense with C8 DSF slashing.
    """
    stake = get_agent_stake(agent_id)
    min_stake = compute_minimum_stake(vtd.assigned_class)

    if stake < min_stake:
        return DeterrentResult(
            sufficient=False,
            reason=f"Stake {stake} below minimum {min_stake} for {vtd.assigned_class}-class"
        )

    # Compute expected loss from forgery detection
    detection_prob = get_class_detection_probability(vtd.assigned_class)
    slash_amount = compute_slash_amount(vtd.assigned_class, stake)
    expected_loss = detection_prob * slash_amount

    return DeterrentResult(
        sufficient=True,
        expected_loss=expected_loss,
        detection_probability=detection_prob,
        slash_amount=slash_amount
    )
```

### 11.4 Sentinel Graph Interface

PCVM feeds the Sentinel Graph with MQI metrics at each epoch boundary:

- VTD rejection rate
- Classification override rate
- Adversarial probe trigger rate and detection rate
- Deep-audit failure rate
- Credibility distribution histogram
- Pairwise endorsement correlation (for collusion detection)
- OVC score distribution (CACT)
- Commitment chain coverage statistics (CACT)
- Honeypot failure rates (AVAP)

The Sentinel Graph responds with alerts: collusion detection triggers increased audit rates and exclusion of suspicious agent pairs from shared committees. Sybil cluster detection triggers agent suspension.

### 11.5 ASV (C4) Interface

PCVM consumes ASV semantic tokens (CLM, EVD, PRV) and produces ASV verification tokens (VRF). The mapping:

- ASV CLM token -> PCVM Claim (content, proposed class, agent ID)
- ASV PRV chain -> VTD dependencies (terminal nodes must resolve to verified claims or constitutional axioms)
- PCVM MCT -> ASV VRF token (verification status, Subjective Logic opinion, epoch, VTD reference)

---

## 12. Defense in Depth: VTD Forgery

This section consolidates all VTD forgery defenses from C10 hardening and CACT (C11) into a unified multi-layer defense architecture.

### 12.1 The Forgery Threat

VTD forgery -- the "Confident Liar" attack -- occurs when a sophisticated forger produces structurally valid VTDs with fabricated or misrepresented evidence. The VTD has correct format, citations, and reasoning chains, but the underlying evidence is false. The fundamental challenge is an infinite trust regress: verifying Source B requires Source C, ad infinitum.

### 12.2 Defense Layers

PCVM v2.0 deploys nine defense layers against VTD forgery:

| Layer | Mechanism | Source | What It Catches |
|-------|-----------|--------|-----------------|
| L1 | Mandatory source verification | C10 CR-H1 | Fabricated URLs, misquoted sources |
| L2 | Cross-verifier evidence correlation | C10 CR-H2 | Single-point-of-failure evidence |
| L3 | Evidence belief cap with temporal decay | C10 CR-H3 | Overconfidence in aging evidence |
| L4 | Forgery suspicion heuristics (H1-H4) | C10 CR-H4 | Production rate anomalies, verification history |
| L5 | Economic deterrents (C8 slashing) | C10 CR-H5 | Rational adversaries (makes forgery unprofitable) |
| L6 | Temporal commitment binding | CACT | Retroactive evidence fabrication |
| L7 | Verifiable computation (SNARK/STARK) | CACT | Computational integrity forgery |
| L8 | Knowledge interrogation | CACT | Fabricators lacking generative knowledge |
| L9 | Orthogonal verification channels | CACT | Fabricators who cannot fake process + environment |

### 12.3 Combined Detection Probability

| Forger Sophistication | Base PCVM | + C10 Hardening | + CACT (Full) |
|----------------------|:---------:|:---------------:|:-------------:|
| Naive (fabricated URLs) | 0.85 | 0.95 | 0.99 |
| Moderate (real sources, misrepresented) | 0.45 | 0.60 | 0.78 |
| Sophisticated (consistent fabrication) | 0.25 | 0.434 | 0.611 |
| Perfect (all channels faked) | 0.07 | 0.07 | 0.15 |

### 12.4 Forgery Escalation Protocol

When forgery suspicion score exceeds 0.50:

```python
def handle_forgery_escalation(agent_id, suspicion_score, vtd, epoch):
    """Handle escalating forgery suspicion."""
    if suspicion_score >= 0.80:
        # Level 3: Strong suspicion
        # Immediate: quarantine VTD, mandatory deep-audit
        quarantine_vtd(vtd.vtd_id)
        schedule_deep_audit(vtd.claim_id, priority="CRITICAL")
        # Cascade: re-verify agent's last 50 claims
        cascade_reverification(agent_id, count=50)
        # Alert Sentinel Graph
        sentinel_alert("FORGERY_STRONG", agent_id, suspicion_score)
        # Initiate C8 slashing investigation
        initiate_slashing_investigation(agent_id, evidence=vtd)

    elif suspicion_score >= 0.65:
        # Level 2: Moderate suspicion
        schedule_deep_audit(vtd.claim_id, priority="HIGH")
        cascade_reverification(agent_id, count=20)
        sentinel_alert("FORGERY_MODERATE", agent_id, suspicion_score)

    elif suspicion_score >= 0.50:
        # Level 1: Elevated suspicion
        increase_probe_rate(agent_id, multiplier=2.0)
        schedule_deep_audit(vtd.claim_id, priority="MEDIUM")
        sentinel_alert("FORGERY_ELEVATED", agent_id, suspicion_score)
```

---

## 13. Defense in Depth: Collusion

This section consolidates all collusion defenses from C10 hardening and AVAP (C12) into a unified multi-layer defense architecture.

### 13.1 The Collusion Threat

Collusion occurs when two or more agents coordinate their verification opinions to manipulate fused credibility scores. A collusion ring can inflate credibility of fabricated claims, suppress valid claims, extract economic value through C8 DSF manipulation, and undermine epistemic integrity by corrupting the knowledge graph's credibility surface.

### 13.2 Defense Layers

PCVM v2.0 deploys ten defense layers against collusion, organized as reactive detection (C10) plus proactive prevention/deterrence (AVAP):

**C10 Reactive Detection (4 layers):**

| Layer | Mechanism | CR | What It Catches |
|-------|-----------|-----|-----------------|
| L1 | Sentinel Graph cluster exclusion | CR-H6 | Sybil attacks, identity correlation |
| L2 | Statistical collusion detection (S1/S2/S3) | CR-H7 | Agreement anomalies, opinion copying |
| L3 | Diversity-constrained committees | CR-H8 | Homogeneous rings (same model, same region) |
| L4 | Adaptive audit for unanimous committees | CR-H9 | Suspiciously unanimous complex-claim verdicts |

**AVAP Proactive Prevention (5 layers):**

| Layer | Mechanism | Type | What It Catches |
|-------|-----------|------|-----------------|
| M1 | Anonymous VRF self-selection committees | Prevention | Real-time coordination (colluders cannot identify allies) |
| M2 | Sealed commit-reveal opinions | Prevention | Opinion signaling, opinion copying |
| M3 | Class-stratified honeypot claims | Detection | Blanket coordination strategies (ground-truth probes) |
| M4 | Collusion deterrence payments | Deterrence | Rational colluders (creates incentives for ring defection) |
| M5 | Conditional behavioral analysis | Detection | Selective collusion (opinion shifts when allies present) |

### 13.3 AVAP Mechanism Details

#### 13.3.1 M1: Anonymous Committees

Agents privately evaluate their VRF self-selection eligibility rather than being publicly assigned by a coordinator. Assignment tokens are encrypted. Mandatory cover traffic prevents colluders from identifying allies through network analysis.

**Anonymity timeline:** Agent learns own assignment at T+0. Identity revealed to membrane only during opinion submission. Full committee roster revealed only after all opinions are sealed. This eliminates the coordination window.

#### 13.3.2 M2: Sealed Opinion Submission

Two-phase commit-reveal protocol for Subjective Logic opinions:

1. **Commit phase:** Each committee member submits `commitment = SHA256(opinion_tuple || nonce)`.
2. **Reveal phase:** After all commitments received, each member reveals `(opinion_tuple, nonce)`.
3. **Non-reveal handling:** Agents who commit but do not reveal receive a credibility penalty (0.15) and their commitment is excluded from fusion.

Sealed opinions are transparent to cumulative fusion (REQ-M2-012): the fusion operation receives revealed opinions and operates identically to unsealed fusion. The sealing mechanism prevents real-time signaling, not the mathematical operation.

#### 13.3.3 M3: Honeypot Claims

Synthetic verification tasks with known ground truth, injected indistinguishably into the verification pipeline:

| Class Coverage | Status | Generator Type |
|---------------|--------|---------------|
| D-class | Full | Deterministic computation with known answer |
| E-class | Full | Empirical claim with planted sources (verifiable ground truth) |
| C-class | Partial | Compliance check with known requirements |
| S-class | Partial | Statistical claim with known dataset |
| H-class | Excluded | Cannot generate ground-truth heuristic judgments |
| N-class | Excluded | Cannot generate ground-truth normative claims |
| K-class | Excluded | Cannot generate ground-truth consolidations |

Honeypot injection rate: 3-5% of verification pipeline volume. Canary-trap variant generation enables leak identification: each potential colluder sees a slightly different honeypot variant.

#### 13.3.4 M4: Collusion Deterrence Payments

Three sub-mechanisms create economic incentives for ring defection:

1. **Asymmetric information injection:** The membrane injects private information into each committee member's verification context, making pre-commitment contracts fragile (members cannot verify whether allies received the same information).

2. **Graduated temporal bounties:** Ring defectors who report collusion receive escalating bounties: 2x base reward at epoch 1, scaling to 10x at epoch 50+. Early defection is more profitable than sustained collusion.

3. **Enterprise liability with retroactive audit cascades:** When collusion is detected, all claims verified by the ring are retroactively audited. The economic cost of remediation exceeds the benefit of collusion by design.

#### 13.3.5 M5: Conditional Behavioral Analysis

Continuous screening via pairwise conditional mutual information: does Agent A's opinion distribution change depending on whether Agent B is on the committee?

This catches selective collusion -- rings that coordinate only when allies are present -- which evades simple agreement-rate analysis.

### 13.4 Combined Collusion Detection Timeline

| Detection Window | Mechanism | Ring Detected |
|-----------------|-----------|--------------|
| Real-time (epoch 0) | M3 honeypot failure | Blanket coordination |
| 5-10 epochs | M5 conditional MI screening | Selective coordination |
| 10-25 epochs | L2 statistical detection (S1/S2/S3) | Any persistent pattern |
| Ongoing | L4 adaptive audit + M4 deterrence | Rational defection incentives |

Under AVAP + C10, a sophisticated ring that spans diversity categories, colludes selectively, and adds noise is detectable with >90% probability within 25 epochs and becomes economically irrational to sustain beyond 10 epochs.

---

## 14. Security Analysis

### 14.1 Threat Model

PCVM assumes the Tidal Noosphere's threat model with PCVM-specific extensions. The system tolerates up to f < 1/3 Byzantine agents within verification committees. Adversarial capabilities range from producing structurally valid VTDs with fabricated evidence (single agent) to coordinated collusion rings (multi-agent).

### 14.2 Attack Resistance

**Attack 1: VTD Forgery (CRITICAL).** An agent produces a high-quality VTD containing fabricated evidence chains. Defense depth: (1) mandatory source verification catches fabricated URLs and quotes (CR-H1); (2) cross-verifier evidence correlation detects single-point-of-failure evidence (CR-H2); (3) evidence belief cap with temporal decay prevents overconfidence (CR-H3); (4) forgery suspicion heuristics flag anomalous patterns (CR-H4); (5) economic deterrents via C8 slashing make forgery unprofitable (CR-H5); (6) CACT temporal commitment binding prevents retroactive fabrication; (7) CACT verifiable computation prevents computational integrity forgery; (8) CACT knowledge interrogation tests generative knowledge; (9) CACT orthogonal channels require multi-system fabrication. **Residual risk: MEDIUM.** A sophisticated forger remains possible but detection probability rises to 0.611 (from 0.434 pre-CACT), and economic deterrents make sustained forgery irrational.

**Attack 2: Strategic Omission (HIGH).** An agent produces a valid VTD that omits unfavorable evidence. Defense: mandatory counter-evidence section for Tier 2 and 3; adversarial probing includes counter-evidence search; claims with no counter-evidence receive credibility penalty (0.05-0.15). **Residual risk: MEDIUM.**

**Attack 3: Class Downgrade (HIGH).** Agent misclassifies claims for weaker proof obligations. Defense: three-way membrane-assigned classification (INV-M2); downgrade rate monitoring (penalty at >30%); re-classification at audit. **Residual risk: MEDIUM.**

**Attack 4: Probe Inoculation (HIGH).** Agent pre-fabricates responses to anticipated probe strategies. Defense: dynamic generative probe component; strategy opacity via VRF seeds; meta-probing for pre-fabrication detection; CACT knowledge interrogation with dynamically generated questions from independently retrieved content. **Residual risk: MEDIUM.**

**Attack 5: Reputation Laundering (MEDIUM).** Agent builds D-class credibility, exploits for H-class claims. Defense: class-specific credibility (INV-M4). D-class trust does not transfer to H-class. **Residual risk: LOW.**

**Attack 6: Constitutional Exploitation (MEDIUM).** Agent satisfies letter but not spirit of constitutional parameters. Defense: intent annotations; adversarial "constitutional spirit" checks; case law mechanism. **Residual risk: MEDIUM.**

**Attack 7: VTD Explosion (MEDIUM).** Agent submits massive VTDs to overwhelm verification. Defense: per-class size limits; per-agent resource budgets; priority queue. **Residual risk: LOW-MEDIUM.**

**Attack 8: Mutual Endorsement / Collusion (CRITICAL).** Colluding verifiers endorse each other's claims. Defense: (C10) Sentinel Graph cluster exclusion (CR-H6), statistical collusion detection (CR-H7), diversity-constrained committees (CR-H8), adaptive audit for unanimous committees (CR-H9); (AVAP) anonymous VRF self-selection committees (M1), sealed commit-reveal opinions (M2), honeypot claims (M3), collusion deterrence payments (M4), conditional behavioral analysis (M5). **Residual risk: MEDIUM-LOW.** Detectable within 25 epochs, economically irrational beyond 10 epochs.

**Attack 9: Tier Collapse (HIGH, strategic).** Argument that PCVM for H/N classes is documentation, not verification. Defense: unified architecture enables cross-class credibility composition; membrane sovereignty requires single checkpoint; engineering simplicity of one system vs. three. **Residual risk: MEDIUM.**

**Attack 10: Bootstrap Problem (MEDIUM).** First VTDs have no verified claims to cite. Defense: seed 100-500 ground-truth claims (default 200); accept higher uncertainty during bootstrap; fall back to replication for high-stakes claims; 2x deep-audit rate during first 100 epochs. **Residual risk: LOW.**

### 14.3 Trust Assumptions

1. The Tidal Noosphere's VRF engine is correctly implemented (RFC 9381).
2. SHA-256 and Ed25519 are cryptographically secure.
3. At least 2/3 of agents in any verification committee are honest.
4. The Sentinel Graph's statistical detection operates with sufficient lookback window.
5. External sources (URLs) are accessible and have not been retroactively modified to match fabricated citations (archive.org fallback partially mitigates).
6. The discrete logarithm assumption holds (for Pedersen commitments in CACT).
7. SNARK/STARK proof systems maintain their soundness properties.
8. Cover traffic in AVAP M1 is indistinguishable from genuine assignment traffic.

### 14.4 Residual Risks

The two CRITICAL attacks have been reduced from HIGH residual risk to MEDIUM and MEDIUM-LOW respectively:

1. **VTD Forgery:** Residual risk reduced from HIGH to MEDIUM. CACT's orthogonal channels raise the detection probability from 0.434 to 0.611 for sophisticated forgers. Economic deterrents (C8 slashing) make sustained forgery irrational. The fundamental limitation remains: epistemic truth is provably unsolvable, and a sufficiently sophisticated forger who controls external systems can still evade detection.

2. **Collusion:** Residual risk reduced from HIGH to MEDIUM-LOW. AVAP's structural prevention (anonymous committees, sealed opinions) eliminates real-time coordination. Active detection (honeypots, behavioral analysis) catches blanket and selective strategies within 25 epochs. Economic deterrence (defector bounties, retroactive audits) makes sustained collusion unprofitable.

---

## 15. Scalability Analysis

### 15.1 Cost Model per Claim Class (Producer vs. Verifier)

| Class | Producer Cost (VTD construction) | Verifier Cost (per member) | Total Verifier Cost (full committee) | Total System Cost vs. Replication |
|-------|----------------------------------|----------------------------|--------------------------------------|-----------------------------------|
| D | 0.05x | 0.017x | 0.05x (3 members) | 0.10x |
| C | 0.15x | 0.067x | 0.20x (3 members) | 0.35x |
| E | 0.30x | 0.10x | 0.50x (5 members) | 0.80x |
| S | 0.20x | 0.06x | 0.30x (5 members) | 0.50x |
| P | 0.15x | 0.04x | 0.20x (5 members) | 0.35x |
| R | 0.20x | 0.08x | 0.40x (5 members) | 0.60x |
| K | 0.25x | 0.10x | 0.50x (5 members) | 0.75x |
| H | 0.50x | 0.214x | 1.50x (7 members) | 2.00x |
| N | 0.40x | 0.157x | 1.10x (7 members) | 1.50x |

Notes:
- "x" = cost of one full replication by one agent.
- Producer Cost is the marginal cost of constructing the VTD beyond producing the claim itself.
- Total System Cost = Producer Cost + Total Verifier Cost (producer constructs VTD once).

```python
def producer_cost(claim_class: str) -> float:
    """Cost to the producing agent for VTD construction."""
    PRODUCER_COSTS = {
        "D": 0.05, "C": 0.15, "E": 0.30, "S": 0.20,
        "P": 0.15, "R": 0.20, "H": 0.50, "N": 0.40, "K": 0.25
    }
    return PRODUCER_COSTS[claim_class]

def verifier_cost_per_member(claim_class: str) -> float:
    """Cost to ONE verification committee member for VTD checking."""
    VERIFIER_COSTS_TOTAL = {
        "D": 0.05, "C": 0.20, "E": 0.50, "S": 0.30,
        "P": 0.20, "R": 0.40, "H": 1.50, "N": 1.10, "K": 0.50
    }
    COMMITTEE_SIZES = {
        "D": 3, "C": 3, "E": 5, "S": 5,
        "P": 5, "R": 5, "H": 7, "N": 7, "K": 5
    }
    return VERIFIER_COSTS_TOTAL[claim_class] / COMMITTEE_SIZES[claim_class]

def total_system_cost(claim_class: str) -> float:
    """Total system cost for verifying one claim."""
    pc = producer_cost(claim_class)
    VERIFIER_COSTS_TOTAL = {
        "D": 0.05, "C": 0.20, "E": 0.50, "S": 0.30,
        "P": 0.20, "R": 0.40, "H": 1.50, "N": 1.10, "K": 0.50
    }
    return pc + VERIFIER_COSTS_TOTAL[claim_class]
```

**Settlement Plane Cost Attribution:**

| Cost Component | Borne By | Settlement Mechanism |
|---------------|----------|---------------------|
| VTD Construction | Producing agent | Deducted from producer's epoch budget; offset by quality score rewards |
| VTD Checking | Each committee member | Compensated from verification reward pool (per-claim payment) |
| Adversarial Probing | System (shared) | Distributed across committee members' epoch settlement |
| Deep-Audit | System (shared) | Funded from deep-audit reserve (2% of total epoch AIC) |
| CACT overhead | System (shared) | ~5-10% additional verification cost |
| AVAP overhead | System (shared) | ~15-20% additional verification cost (within budget) |

### 15.2 System-Level Cost Projection

Assuming a representative claim distribution (D: 15%, E: 20%, S: 10%, H: 15%, N: 5%, P: 15%, R: 10%, C: 5%, K: 5%), the weighted average verification cost is:

```
0.15 * 0.10 + 0.20 * 0.80 + 0.10 * 0.50 + 0.15 * 2.00 +
0.05 * 1.50 + 0.15 * 0.35 + 0.10 * 0.60 + 0.05 * 0.35 + 0.05 * 0.75
= 0.015 + 0.16 + 0.05 + 0.30 + 0.075 + 0.0525 + 0.06 + 0.0175 + 0.0375
= 0.7675x of replication cost
```

Adding deep-audit overhead (7% of claims re-verified at full cost): 0.7675 + 0.07 = 0.8375x. Rounding: approximately 0.83x.

**Net savings: approximately 17% over universal replication.** The savings are modest because Tier 3 claims (20% of volume) cost more than replication. The system-level value proposition rests on:

1. Cost reduction for Tier 1 and Tier 2 claims (75% of volume, average ~0.50x cost).
2. Quality improvement for all tiers (richer verification metadata, adversarial probing, credibility propagation, CACT orthogonal verification).
3. Downstream trust propagation: verified claims do not need re-verification when cited by subsequent claims, amortizing verification cost over the citation graph.

With downstream trust propagation factored in (verified claims cited an average of 3 times each avoid 3x re-verification), effective system cost drops to approximately 0.40x-0.60x of universal replication. This figure requires empirical validation of citation density assumptions.

### 15.3 Scale Targets

| Scale | Agents | Claims/Epoch | Verification Capacity | Key Bottleneck |
|-------|--------|-------------|----------------------|----------------|
| Pilot | 1K | 500 | 50 verifiers | Committee diversity |
| Production | 10K | 5,000 | 500 verifiers | Credibility propagation latency |
| Planetary | 100K | 50,000 | 5,000 verifiers | Sentinel Graph correlation analysis |

At 100K agents: deep-audit processes approximately 3,500 claims/epoch (7% of 50K). Credibility propagation runs over a dependency graph of approximately 5M claims. The dampening-based propagation algorithm (Section 9.7) is O(|edges| * iterations_to_convergence) which, for a graph with average degree 3 and max 44 iterations, is approximately O(15M * 44) = O(660M) operations -- manageable with parallelization.

---

## 16. Open Design Questions

**Q1: Formal proof theory for non-deterministic claims.** PCVM's VTD model for Tier 2 and Tier 3 classes is novel and unproven. The four hard gate experiments must validate that VTDs provide genuine verification value beyond documentation. Kill criterion: VTD checking achieves < 80% error detection rate at < 50% replication cost for fewer than 4 of 9 classes.

**Q2: Claim taxonomy stability.** The 9-class taxonomy must be reliably classifiable. Kill criterion: Fleiss' kappa < 0.60 across 5 classifiers on 200 claims. Fallback: simplify to 5 classes (merge H+N, merge E+S, keep D, P/C, R/K).

**Q3: Credibility composition domain transfer.** Subjective Logic was designed for trust in multi-agent communication, not for epistemic claim verification. The claim-class adaptations are novel modifications whose correctness properties are not guaranteed. Kill criterion: propagation does not converge within 100 iterations, or cascade > 0.3 at distance > 3.

**Q4: Adversarial probing effectiveness.** The probing system's ability to detect subtle and adversarial errors must be validated, including KI probe effectiveness against LLMs. Kill criterion: VTD+probing F1 < 0.80 or cost > 2x replication.

**Q5: Unified vs. split architecture.** Comparative analysis mandated: unified membrane vs. three separate systems. If the split architecture is more than 30% simpler with less than 10% capability loss, the split is preferred.

**Q6: Bootstrap protocol details.** The cold-start procedure requires specification. The system provides minimal verification value during bootstrap.

**Q7: CACT complexity budget.** CACT adds significant complexity (commitment chains, SNARK/STARK infrastructure, KI probes, orthogonal channels). The benefit must justify the attack surface increase. Kill criterion: CACT overhead > 25% of verification cost with < 15% improvement in detection probability.

**Q8: AVAP anonymity guarantees.** VRF self-selection anonymity depends on cover traffic indistinguishability. If cover traffic is distinguishable from genuine traffic, colluders can identify committee members. Kill criterion: committee identification probability > 0.20 with cover traffic active.

---

## 17. Conclusion

PCVM replaces replication-based consensus with a graduated proof-carrying architecture that matches verification depth to claim type. The system provides genuine sublinear verification for deterministic claims (Tier 1, 0.1x-0.35x cost), structured evidence evaluation for empirical and reasoning claims (Tier 2, 0.35x-1.2x cost), and quality-improving attestation review for judgment-based claims (Tier 3, 1.0x-2.0x cost).

The system-level direct cost reduction of 17% (0.83x of replication) is modest. With downstream trust propagation -- contingent on empirical validation of citation density assumptions -- projected savings reach 40-60%. The value proposition is therefore not primarily cost but quality: VTDs produce richer verification metadata than binary pass/fail, credibility opinions propagate through knowledge graphs to give downstream consumers calibrated confidence, and adversarial probing exposes weaknesses that replication-based consensus would miss.

PCVM v2.0 addresses the two CRITICAL residual risks from v1.0:

**VTD Forgery** is defended by nine layers: mandatory source verification, cross-verifier evidence correlation, evidence belief caps, forgery heuristics, economic deterrents, CACT temporal commitment binding, verifiable computation, knowledge interrogation, and orthogonal verification channels. The sophisticated forger detection probability rises from 0.434 to 0.611. The residual risk is reduced from HIGH to MEDIUM.

**Collusion** is defended by nine layers: Sentinel Graph cluster exclusion, statistical detection, diversity-constrained committees, adaptive audit, AVAP anonymous committees, sealed opinions, honeypot claims, deterrence payments, and conditional behavioral analysis. Collusion is detectable within 25 epochs and economically irrational beyond 10 epochs. The residual risk is reduced from HIGH to MEDIUM-LOW.

The architecture is honest about its limitations. Tier 3 claims cost more to verify than to replicate. The proof theory for non-deterministic claims is novel and unproven. Epistemic truth forgery remains provably unsolvable. The 9-class taxonomy's reliability and the credibility algebra's domain transfer are subject to experimental validation through mandatory hard gates. CACT and AVAP add complexity that must justify its cost through measurable improvement in detection probabilities.

Despite these limitations, PCVM fills a genuine architectural gap: the Tidal Noosphere requires a verification membrane that handles non-deterministic agent outputs, and PCVM is the only candidate that has been through a full research pipeline. No existing system combines per-output structured proof artifacts, an epistemic claim taxonomy, adversarial probing, governance-integrated constitutional protections, orthogonal forgery defense, and structural collusion prevention. The regulatory window (EU AI Act enforcement August 2026, NIST AI Agent Standards launching) creates a market opportunity for structured verification artifacts that PCVM's VTD format is positioned to address.

---

## Appendix A: Complete VTD JSON Schemas

### A.1 D-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-d-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "D-class Proof Body",
  "description": "Deterministic computation proof. Tier 1: FORMAL_PROOF.",
  "type": "object",
  "required": ["computation", "inputs", "output", "proof_type"],
  "properties": {
    "proof_type": {
      "type": "string",
      "enum": ["RECOMPUTATION", "HASH_VERIFICATION", "PROOF_CERTIFICATE",
               "PROOF_SKETCH", "SNARK_PROOF", "STARK_PROOF"]
    },
    "computation": {
      "type": "object",
      "required": ["algorithm", "version"],
      "properties": {
        "algorithm": { "type": "string" },
        "version": { "type": "string" },
        "determinism_declaration": {
          "type": "string",
          "enum": ["FULLY_DETERMINISTIC", "DETERMINISTIC_GIVEN_SEED",
                   "DETERMINISTIC_MODULO_PRECISION"]
        },
        "seed": { "type": "string" }
      }
    },
    "inputs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "value_hash"],
        "properties": {
          "name": { "type": "string" },
          "value_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
          "value": {},
          "size_bytes": { "type": "integer" }
        }
      }
    },
    "output": {
      "type": "object",
      "required": ["value_hash"],
      "properties": {
        "value_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "value": {},
        "size_bytes": { "type": "integer" }
      }
    },
    "trace": {
      "type": "object",
      "properties": {
        "key_steps": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["step_index", "operation", "intermediate_hash"],
            "properties": {
              "step_index": { "type": "integer" },
              "operation": { "type": "string" },
              "intermediate_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
            }
          }
        },
        "total_steps": { "type": "integer" }
      }
    },
    "proof_certificate": {
      "type": "object",
      "properties": {
        "format": { "type": "string", "enum": ["COQ_PROOF","TLA_PROOF","ISABELLE_PROOF","CUSTOM_CERT"] },
        "certificate_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "certificate_uri": { "type": "string", "format": "uri" },
        "checker_version": { "type": "string" }
      }
    }
  },
  "additionalProperties": false
}
```

### A.2 E-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-e-class.schema.json",
  "title": "E-class Proof Body",
  "description": "Empirical evidence package. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": ["sources", "cross_references", "evidence_chain"],
  "properties": {
    "sources": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["source_id", "source_type", "retrieval_timestamp", "relevance_justification"],
        "properties": {
          "source_id": { "type": "string" },
          "source_type": { "type": "string", "enum": ["PEER_REVIEWED_PAPER","PREPRINT","OFFICIAL_REPORT","DATABASE","WEB_PAGE","API_RESPONSE","VERIFIED_CLAIM","OBSERVATION_RECORD"] },
          "uri": { "type": "string", "format": "uri" },
          "retrieval_timestamp": { "type": "string", "format": "date-time" },
          "content_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
          "quoted_text": { "type": "string", "maxLength": 2000 },
          "quote_context": { "type": "string" },
          "relevance_justification": { "type": "string" },
          "reliability_assessment": { "type": "string", "enum": ["HIGH","MEDIUM","LOW","UNKNOWN"] }
        }
      }
    },
    "cross_references": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source_id", "confirms"],
        "properties": {
          "source_id": { "type": "string" },
          "confirms": { "type": "boolean" },
          "partial": { "type": "boolean", "default": false },
          "note": { "type": "string" }
        }
      }
    },
    "evidence_chain": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["sub_claim", "supporting_sources"],
        "properties": {
          "sub_claim": { "type": "string" },
          "supporting_sources": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
          "strength": { "type": "string", "enum": ["STRONG","MODERATE","WEAK"] }
        }
      }
    },
    "observation_conditions": {
      "type": "object",
      "properties": {
        "temporal_range": { "type": "object", "properties": { "start": { "type": "string", "format": "date-time" }, "end": { "type": "string", "format": "date-time" } } },
        "methodology": { "type": "string" },
        "instruments": { "type": "array", "items": { "type": "string" } }
      }
    }
  },
  "additionalProperties": false
}
```

### A.3 S-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-s-class.schema.json",
  "title": "S-class Proof Body",
  "description": "Statistical evidence package. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": ["dataset", "methodology", "results", "assumptions"],
  "properties": {
    "dataset": {
      "type": "object",
      "required": ["sample_size", "source_description"],
      "properties": {
        "sample_size": { "type": "integer", "minimum": 1 },
        "population_description": { "type": "string" },
        "source_description": { "type": "string" },
        "sampling_method": { "type": "string", "enum": ["RANDOM","STRATIFIED","CONVENIENCE","CENSUS","SYSTEMATIC","CLUSTER"] },
        "data_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "data_uri": { "type": "string", "format": "uri" },
        "collection_period": { "type": "object", "properties": { "start": { "type": "string", "format": "date-time" }, "end": { "type": "string", "format": "date-time" } } }
      }
    },
    "methodology": {
      "type": "object",
      "required": ["test_type"],
      "properties": {
        "test_type": { "type": "string" },
        "software": { "type": "string" },
        "software_version": { "type": "string" },
        "pre_registration": { "type": "object", "properties": { "registered": { "type": "boolean" }, "registry_uri": { "type": "string", "format": "uri" } } },
        "corrections": { "type": "array", "items": { "type": "string" } }
      }
    },
    "results": {
      "type": "object",
      "required": ["test_statistic", "conclusion"],
      "properties": {
        "test_statistic": { "type": "object", "required": ["name", "value"], "properties": { "name": { "type": "string" }, "value": { "type": "number" }, "degrees_of_freedom": { "type": "number" } } },
        "p_value": { "type": "number", "minimum": 0, "maximum": 1 },
        "confidence_interval": { "type": "object", "properties": { "level": { "type": "number" }, "lower": { "type": "number" }, "upper": { "type": "number" } } },
        "effect_size": { "type": "object", "properties": { "metric": { "type": "string" }, "value": { "type": "number" }, "interpretation": { "type": "string", "enum": ["NEGLIGIBLE","SMALL","MEDIUM","LARGE"] } } },
        "conclusion": { "type": "string" }
      }
    },
    "assumptions": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["assumption", "check_result"],
        "properties": {
          "assumption": { "type": "string" },
          "check_method": { "type": "string" },
          "check_result": { "type": "string", "enum": ["SATISFIED","APPROXIMATELY_SATISFIED","VIOLATED","NOT_TESTABLE"] },
          "note": { "type": "string" }
        }
      }
    },
    "power_analysis": {
      "type": "object",
      "properties": {
        "target_power": { "type": "number" },
        "achieved_power": { "type": "number" },
        "minimum_detectable_effect": { "type": "number" }
      }
    }
  },
  "additionalProperties": false
}
```

### A.4 P-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-p-class.schema.json",
  "title": "P-class Proof Body",
  "description": "Process trace evidence. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": ["process_spec", "steps", "conformance_summary"],
  "properties": {
    "process_spec": {
      "type": "object",
      "required": ["spec_id", "spec_version"],
      "properties": {
        "spec_id": { "type": "string" },
        "spec_version": { "type": "string" },
        "spec_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "required_steps": { "type": "array", "items": { "type": "string" } }
      }
    },
    "steps": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["step_id", "step_name", "started", "completed", "status"],
        "properties": {
          "step_id": { "type": "string" },
          "step_name": { "type": "string" },
          "started": { "type": "string", "format": "date-time" },
          "completed": { "type": "string", "format": "date-time" },
          "status": { "type": "string", "enum": ["COMPLETED","SKIPPED","FAILED","PARTIAL"] },
          "inputs": { "type": "array", "items": { "type": "object", "properties": { "name": { "type": "string" }, "value_hash": { "type": "string" }, "source": { "type": "string" } } } },
          "outputs": { "type": "array", "items": { "type": "object", "properties": { "name": { "type": "string" }, "value_hash": { "type": "string" } } } },
          "tools_invoked": { "type": "array", "items": { "type": "object", "properties": { "tool_id": { "type": "string" }, "invocation_hash": { "type": "string" } } } },
          "prerequisites_met": { "type": "array", "items": { "type": "object", "properties": { "prerequisite": { "type": "string" }, "satisfied": { "type": "boolean" }, "evidence": { "type": "string" } } } }
        }
      }
    },
    "deviations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step_id", "deviation_type", "justification"],
        "properties": {
          "step_id": { "type": "string" },
          "deviation_type": { "type": "string", "enum": ["SKIPPED","REORDERED","MODIFIED","ADDED"] },
          "justification": { "type": "string" },
          "approved_by": { "type": "string" }
        }
      },
      "default": []
    },
    "conformance_summary": {
      "type": "object",
      "required": ["total_required", "completed", "skipped", "failed"],
      "properties": {
        "total_required": { "type": "integer" },
        "completed": { "type": "integer" },
        "skipped": { "type": "integer" },
        "failed": { "type": "integer" },
        "conformance_rate": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  },
  "additionalProperties": false
}
```

### A.5 R-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-r-class.schema.json",
  "title": "R-class Proof Body",
  "description": "Reasoning chain evidence. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": ["premises", "inferences", "assumptions", "logical_assessment"],
  "properties": {
    "premises": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["premise_id", "content", "support_type"],
        "properties": {
          "premise_id": { "type": "string" },
          "content": { "type": "string" },
          "support_type": { "type": "string", "enum": ["VERIFIED_CLAIM","AXIOM","ASSUMPTION","EMPIRICAL","DEFINITION"] },
          "support_ref": { "type": "string" },
          "support_credibility": { "type": "number", "minimum": 0, "maximum": 1 }
        }
      }
    },
    "inferences": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["from_premises", "rule", "yields"],
        "properties": {
          "from_premises": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
          "rule": { "type": "string" },
          "rule_type": { "type": "string", "enum": ["DEDUCTIVE","INDUCTIVE","ABDUCTIVE","ANALOGICAL"] },
          "yields": { "type": "string" },
          "yields_id": { "type": "string" }
        }
      }
    },
    "assumptions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["assumption", "necessity"],
        "properties": {
          "assumption": { "type": "string" },
          "necessity": { "type": "string", "enum": ["ESSENTIAL","SIMPLIFYING","CONVENTIONAL"] },
          "justification": { "type": "string" },
          "violation_consequence": { "type": "string" }
        }
      }
    },
    "logical_assessment": {
      "type": "object",
      "required": ["validity"],
      "properties": {
        "validity": { "type": "string", "enum": ["VALID","VALID_IF_ASSUMPTIONS_HOLD","PROBABILISTICALLY_VALID","INVALID"] },
        "soundness_notes": { "type": "string" },
        "known_fallacies_checked": {
          "type": "array",
          "items": { "type": "object", "properties": { "fallacy": { "type": "string" }, "present": { "type": "boolean" }, "note": { "type": "string" } } }
        }
      }
    }
  },
  "additionalProperties": false
}
```

### A.6 C-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-c-class.schema.json",
  "title": "C-class Proof Body",
  "description": "Compliance proof package. Tier 1: FORMAL_PROOF.",
  "type": "object",
  "required": ["regulation", "requirements", "compliance_status"],
  "properties": {
    "regulation": {
      "type": "object",
      "required": ["regulation_id", "title"],
      "properties": {
        "regulation_id": { "type": "string" },
        "title": { "type": "string" },
        "version": { "type": "string" },
        "effective_date": { "type": "string", "format": "date" },
        "jurisdiction": { "type": "string" },
        "uri": { "type": "string", "format": "uri" }
      }
    },
    "requirements": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["requirement_id", "requirement_text", "evidence_type", "evidence"],
        "properties": {
          "requirement_id": { "type": "string" },
          "requirement_text": { "type": "string" },
          "applicability": { "type": "string", "enum": ["APPLICABLE","NOT_APPLICABLE","PARTIALLY_APPLICABLE"] },
          "evidence_type": { "type": "string", "enum": ["DOCUMENT","PROCESS_LOG","TEST_RESULT","ATTESTATION","CONFIGURATION"] },
          "evidence": {
            "type": "object",
            "required": ["description"],
            "properties": {
              "description": { "type": "string" },
              "reference": { "type": "string" },
              "reference_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
              "verified_date": { "type": "string", "format": "date-time" }
            }
          },
          "status": { "type": "string", "enum": ["COMPLIANT","NON_COMPLIANT","PARTIALLY_COMPLIANT","NOT_ASSESSED"] }
        }
      }
    },
    "gaps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["requirement_id", "gap_description", "remediation_plan"],
        "properties": {
          "requirement_id": { "type": "string" },
          "gap_description": { "type": "string" },
          "severity": { "type": "string", "enum": ["CRITICAL","HIGH","MEDIUM","LOW"] },
          "remediation_plan": { "type": "string" },
          "remediation_deadline": { "type": "string", "format": "date" }
        }
      },
      "default": []
    },
    "compliance_status": {
      "type": "object",
      "required": ["overall_status", "last_reviewed"],
      "properties": {
        "overall_status": { "type": "string", "enum": ["FULLY_COMPLIANT","PARTIALLY_COMPLIANT","NON_COMPLIANT"] },
        "compliant_count": { "type": "integer" },
        "total_requirements": { "type": "integer" },
        "last_reviewed": { "type": "string", "format": "date-time" },
        "next_review": { "type": "string", "format": "date-time" }
      }
    },
    "constitutional_parameters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "parameter_id": { "type": "string", "pattern": "^CONST-[0-9]{3,4}$" },
          "satisfied": { "type": "boolean" },
          "evidence_ref": { "type": "string" }
        }
      }
    }
  },
  "additionalProperties": false
}
```

### A.7 H-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-h-class.schema.json",
  "title": "H-class Proof Body",
  "description": "Heuristic attestation package. Tier 3: STRUCTURED_ATTESTATION.",
  "type": "object",
  "required": ["alternatives", "criteria", "evaluation", "confidence", "uncertainty_sources"],
  "properties": {
    "alternatives": {
      "type": "array", "minItems": 2,
      "items": {
        "type": "object",
        "required": ["name", "description"],
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "genuinely_considered": { "type": "boolean", "default": true }
        }
      }
    },
    "criteria": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "weight"],
        "properties": {
          "name": { "type": "string" },
          "weight": { "type": "number", "minimum": 0, "maximum": 1 },
          "justification": { "type": "string" }
        }
      }
    },
    "evaluation": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["alternative", "criterion", "score", "rationale"],
        "properties": {
          "alternative": { "type": "string" },
          "criterion": { "type": "string" },
          "score": { "type": "number", "minimum": 0, "maximum": 1 },
          "rationale": { "type": "string" }
        }
      }
    },
    "precedents": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["description", "relevance"],
        "properties": {
          "description": { "type": "string" },
          "source": { "type": "string" },
          "outcome": { "type": "string" },
          "relevance": { "type": "string" },
          "similarity_score": { "type": "number", "minimum": 0, "maximum": 1 }
        }
      }
    },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "uncertainty_sources": { "type": "array", "minItems": 1, "items": { "type": "string" } },
    "boundary_conditions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["condition", "effect"],
        "properties": {
          "condition": { "type": "string" },
          "effect": { "type": "string", "enum": ["INVALIDATES","WEAKENS","MODIFIES","IRRELEVANT"] }
        }
      }
    },
    "failure_modes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["mode", "likelihood", "impact"],
        "properties": {
          "mode": { "type": "string" },
          "likelihood": { "type": "string", "enum": ["HIGH","MEDIUM","LOW"] },
          "impact": { "type": "string", "enum": ["HIGH","MEDIUM","LOW"] },
          "mitigation": { "type": "string" }
        }
      }
    },
    "model_info": {
      "type": "object",
      "properties": {
        "model_id": { "type": "string" },
        "training_data_relevance": { "type": "string" },
        "known_biases": { "type": "array", "items": { "type": "string" } }
      }
    }
  },
  "additionalProperties": false
}
```

### A.8 N-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-n-class.schema.json",
  "title": "N-class Proof Body",
  "description": "Normative attestation package. Tier 3: STRUCTURED_ATTESTATION.",
  "type": "object",
  "required": ["value_framework", "constitutional_refs", "stakeholder_analysis", "alternatives"],
  "properties": {
    "value_framework": {
      "type": "object",
      "required": ["framework_type", "principles"],
      "properties": {
        "framework_type": {
          "type": "string",
          "enum": ["DEONTOLOGICAL","CONSEQUENTIALIST","VIRTUE_ETHICS","CARE_ETHICS","CONTRACTUALIST","PLURALIST","CONSTITUTIONAL"]
        },
        "principles": {
          "type": "array", "minItems": 1,
          "items": {
            "type": "object",
            "required": ["principle", "application"],
            "properties": {
              "principle": { "type": "string" },
              "source": { "type": "string" },
              "application": { "type": "string" }
            }
          }
        },
        "framework_justification": { "type": "string" }
      }
    },
    "constitutional_refs": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["parameter_id", "alignment"],
        "properties": {
          "parameter_id": { "type": "string", "pattern": "^CONST-[0-9]{3,4}$" },
          "parameter_text": { "type": "string" },
          "parameter_intent": { "type": "string" },
          "alignment": { "type": "string", "enum": ["SUPPORTS","CONSISTENT","NEUTRAL","TENSION","CONFLICTS"] },
          "alignment_argument": { "type": "string" }
        }
      }
    },
    "stakeholder_analysis": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["stakeholder_group", "impact", "impact_description"],
        "properties": {
          "stakeholder_group": { "type": "string" },
          "impact": { "type": "string", "enum": ["POSITIVE","NEGATIVE","NEUTRAL","MIXED"] },
          "impact_description": { "type": "string" },
          "mitigation": { "type": "string" }
        }
      }
    },
    "alternatives": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["position", "counter_argument"],
        "properties": {
          "position": { "type": "string" },
          "counter_argument": { "type": "string" },
          "framework_used": { "type": "string" }
        }
      }
    },
    "dissent_record": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "dissenting_position": { "type": "string" },
          "dissenting_agent": { "type": "string" },
          "resolution": { "type": "string" }
        }
      }
    }
  },
  "additionalProperties": false
}
```

### A.9 K-class Proof Body

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v2/vtd-k-class.schema.json",
  "title": "K-class Proof Body",
  "description": "Knowledge Consolidation evidence. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": [
    "source_quanta", "synthesis_chain", "falsification_statement",
    "voting_record", "provenance_summary"
  ],
  "properties": {
    "source_quanta": {
      "type": "array",
      "minItems": 5,
      "items": {
        "type": "object",
        "required": ["claim_id", "contributing_agent", "parcel_id",
                      "domain", "contribution_summary"],
        "properties": {
          "claim_id": { "type": "string" },
          "contributing_agent": { "type": "string" },
          "parcel_id": { "type": "string" },
          "domain": { "type": "string" },
          "contribution_summary": { "type": "string", "maxLength": 500 },
          "credibility_at_synthesis": {
            "type": "number", "minimum": 0, "maximum": 1
          }
        }
      }
    },
    "provenance_summary": {
      "type": "object",
      "required": ["total_agents", "total_parcels", "max_agent_share"],
      "properties": {
        "total_agents": { "type": "integer", "minimum": 5 },
        "total_parcels": { "type": "integer", "minimum": 3 },
        "max_agent_share": {
          "type": "number", "minimum": 0, "maximum": 0.30
        },
        "domain_coverage": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "synthesis_chain": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["step_id", "input_quanta", "reasoning", "output"],
        "properties": {
          "step_id": { "type": "string" },
          "input_quanta": {
            "type": "array", "items": { "type": "string" }, "minItems": 1
          },
          "reasoning": { "type": "string" },
          "reconciliation_notes": { "type": "string" },
          "output": { "type": "string" }
        }
      }
    },
    "falsification_statement": {
      "type": "object",
      "required": ["statement", "conditions"],
      "properties": {
        "statement": { "type": "string" },
        "conditions": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": ["condition", "impact"],
            "properties": {
              "condition": { "type": "string" },
              "impact": {
                "type": "string",
                "enum": ["INVALIDATES", "WEAKENS", "NARROWS_SCOPE"]
              }
            }
          }
        },
        "testable": { "type": "boolean", "default": true }
      }
    },
    "voting_record": {
      "type": "object",
      "required": ["passes"],
      "properties": {
        "passes": {
          "type": "array",
          "minItems": 3,
          "maxItems": 3,
          "items": {
            "type": "object",
            "required": ["pass_number", "voters", "outcome"],
            "properties": {
              "pass_number": { "type": "integer", "minimum": 1, "maximum": 3 },
              "voters": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": ["agent_id", "vote"],
                  "properties": {
                    "agent_id": { "type": "string" },
                    "vote": {
                      "type": "string",
                      "enum": ["APPROVE", "REJECT", "ABSTAIN", "REQUEST_REVISION"]
                    },
                    "rationale": { "type": "string" }
                  }
                }
              },
              "outcome": {
                "type": "string",
                "enum": ["PASSED", "FAILED", "REVISED"]
              }
            }
          }
        }
      }
    }
  },
  "additionalProperties": false
}
```

---

## Appendix B: Subjective Logic Operator Definitions

### B.1 Conjunction

```
w_C = w_A AND w_B
b_C = b_A * b_B
d_C = d_A + d_B - d_A * d_B
u_C = b_A * u_B + u_A * b_B + u_A * u_B
a_C = a_A * a_B
```

Reference: Josang (2016), Definition 12.1.

### B.2 Discounting

```
w_disc = w_trust : w_claim
b_disc = b_trust * b_claim
d_disc = b_trust * d_claim
u_disc = d_trust + u_trust + b_trust * u_claim
a_disc = a_claim
```

Reference: Josang (2016), Definition 14.2.

### B.3 Cumulative Fusion

```
When u_A > 0 and u_B > 0:
  k = u_A + u_B - u_A * u_B
  b_f = (b_A * u_B + b_B * u_A) / k
  d_f = (d_A * u_B + d_B * u_A) / k
  u_f = (u_A * u_B) / k
  a_f = (a_A * u_B + a_B * u_A) / (u_A + u_B)

When u_A = 0 and u_B = 0 (both dogmatic):
  b_f = (b_A + b_B) / 2
  d_f = (d_A + d_B) / 2
  u_f = 0
  a_f = (a_A + a_B) / 2
```

Reference: Josang (2016), Definition 12.6.

### B.4 Expected Probability

```
E(w) = b + a * u
```

### B.5 Credibility Propagation (DAG)

Single-pass topological sort: for each claim in topological order, discount by class-specific agent trust, then conjoin with all dependency opinions.

### B.6 Credibility Propagation (Cyclic)

Iterative dampening with alpha = 0.85, epsilon = 0.001, max iterations = 100. Convergence guaranteed within ceil(log(epsilon) / log(alpha)) = 44 iterations.

---

## Appendix C: Configurable Parameters Table

| Parameter | Default | Range | Governance |
|-----------|---------|-------|------------|
| DEEP_AUDIT_RATE | 0.07 | [0.01, 0.25] | G-class |
| MIN_AUDITS_PER_EPOCH | 5 | [1, 50] | G-class |
| AUDIT_COMMITTEE_SIZE | 5 | [3, 11] | G-class |
| AUDIT_AGREEMENT_THRESHOLD | 0.15 | [0.05, 0.30] | G-class |
| AUDIT_SIGNIFICANT_DROP | 0.25 | [0.10, 0.50] | G-class |
| AUDIT_LOOKBACK | 50 epochs | [10, 200] | Operational |
| COMMITTEE_SIZE_TIER1 | 3 | [3, 7] | G-class |
| COMMITTEE_SIZE_TIER2 | 5 | [3, 11] | G-class |
| COMMITTEE_SIZE_TIER3 | 7 | [5, 15] | G-class |
| PROBERS_TIER2 | 1 | [0, 3] | G-class |
| PROBERS_TIER3 | 2 | [1, 5] | G-class |
| DAMPENING_FACTOR | 0.85 | [0.70, 0.95] | Operational |
| CONVERGENCE_EPSILON | 0.001 | [0.0001, 0.01] | Operational |
| CONVERGENCE_MAX_ITER | 100 | [20, 500] | Operational |
| REVERIFICATION_THRESHOLD | 0.50 | [0.30, 0.70] | G-class |
| PREMISE_CHANGE_THRESHOLD | 0.20 | [0.10, 0.40] | Operational |
| TIER3_ACCEPT_THRESHOLD | 0.60 | [0.50, 0.80] | G-class |
| TIER3_WEAK_THRESHOLD | 0.40 | [0.30, 0.60] | G-class |
| RANDOM_PROBE_RATE | 0.10 | [0.05, 0.30] | G-class |
| PROBE_CREDIBILITY_THRESHOLD | 0.50 | [0.30, 0.70] | Operational |
| PROBE_SURVIVAL_BOOST | 0.05 | [0.01, 0.10] | Operational |
| SUSPICION_PENALTY_NO_COUNTER_EVIDENCE | 0.15 | [0.05, 0.30] | Operational |
| INOCULATION_THRESHOLD | 0.70 | [0.50, 0.90] | Operational |
| MAX_PROBE_BUDGET | 5000 AIC | [1000, 20000] | Operational |
| APPEAL_RATE_LIMIT | 0.05 | [0.01, 0.15] | G-class |
| SOURCE_FRESHNESS_DAYS | varies | [30, 730] | Operational |
| CONTRADICTION_SIMILARITY_THRESHOLD | 0.70 | [0.50, 0.90] | Operational |
| CONTRADICTION_THRESHOLD | 0.80 | [0.60, 0.95] | Operational |
| MAX_REVERIFICATIONS_PER_EPOCH | 100 | [10, 1000] | Operational |
| MQI_REJECTION_THRESHOLD | 0.30 | [0.10, 0.50] | G-class |
| MQI_AUDIT_DISCREPANCY_THRESHOLD | 0.15 | [0.05, 0.30] | G-class |
| COLLUSION_LOOKBACK_EPOCHS | 50 | [20, 200] | Operational |
| COLLUSION_ENDORSEMENT_THRESHOLD | 0.95 | [0.85, 1.00] | Operational |
| DIVERSITY_COOLING_EPOCHS | 50 | [10, 100] | G-class |
| E_CLASS_HALF_LIFE_DAYS | 180 | [90, 365] | Operational |
| H_CLASS_HALF_LIFE_DAYS | 180 | [90, 365] | Operational |
| K_CLASS_HALF_LIFE_DAYS | 270 | [120, 540] | Operational |
| FUZZY_MATCH_THRESHOLD | 0.90 | [0.80, 0.98] | Operational |
| SOURCE_FETCH_TIMEOUT_MS | 10000 | [5000, 30000] | Operational |
| CLASSIFICATION_MAJORITY_COUNT | 2 | [2, 3] | G-class |
| DOWNGRADE_RATE_PENALTY_THRESHOLD | 0.30 | [0.15, 0.50] | Operational |
| DOWNGRADE_RATE_PENALTY_AMOUNT | 0.10 | [0.05, 0.25] | Operational |
| CITATION_AUDIT_LOG_BASE | 2 | [2, 10] | Operational |
| BOOTSTRAP_SEED_CLAIMS | 200 | [100, 500] | G-class |
| BOOTSTRAP_AUDIT_MULTIPLIER | 2.0 | [1.5, 4.0] | Operational |
| K_CLASS_ADMISSION_THRESHOLD | 0.70 | [0.60, 0.85] | G-class |
| K_CLASS_SOURCE_CRED_FLOOR | 0.50 | [0.30, 0.70] | Operational |
| K_CLASS_MAX_AGENT_SHARE | 0.30 | [0.15, 0.50] | G-class |

**Governance levels:**
- **G-class (Constitutional):** 75% BFT supermajority + 72-hour discussion. Directly affects membrane sovereignty.
- **Operational:** Modifiable by feedback controller within bounds or by simple majority.

---

## Appendix D: Conformance Requirements

### D.1 MUST Requirements (25)

1. Validate all VTDs against the common envelope schema before processing.
2. Validate VTD proof_body against the class-specific schema.
3. Enforce VTD size limits per class.
4. Implement three-way classification protocol (INV-M2).
5. Apply most conservative class when all three classification inputs disagree (conservatism ordering H>N>K>E>S>R>P>C>D).
6. Select verification committees via VRF (RFC 9381).
7. NOT allow an agent to verify its own claims (INV-M3).
8. NOT allow adversarial probers to overlap with verification committee (INV-M3).
9. Track agent credibility per claim class (INV-M4).
10. Perform mandatory source verification for E-class claims (CR-H1).
11. Invoke adversarial probing for all Tier 3 claims.
12. Implement deep-audit protocol with VRF-based selection (INV-M5).
13. Handle deep-audit failures: credibility downgrade, agent investigation, cascade, alert.
14. Issue a Classification Seal (CLS) for every classified claim.
15. Issue a Membrane Credibility Token (MCT) for every admitted claim.
16. Perform contradiction checking before knowledge admission.
17. Preserve constraint b + d + u = 1 in all Subjective Logic operations.
18. Report MQI metrics to Sentinel Graph at each epoch boundary.
19. Enforce G-class parameters modifiable only through constitutional consensus.
20. NOT modify a VTD after submission and sealing (INV-M7).
21. Apply Sentinel Graph cluster exclusion in committee selection (CR-H6).
22. Run collusion detection every 10 epochs for qualifying agent pairs (CR-H7).
23. Record committee diversity score for every verification event (CR-H8).
24. Compute adaptive audit rate for every passed claim (CR-H9).
25. Include "K" in all claim class enumerations.

### D.2 SHOULD Requirements (12)

1. Implement citation-weighted deep-audit selection.
2. Include generative component in adversarial probe strategies.
3. Implement meta-probing for pre-fabricated response detection.
4. Implement collusion detection via pairwise endorsement correlation.
5. Require counter-evidence sections with items for Tier 3 claims.
6. Schedule re-verification based on class-specific decay policies.
7. Support multi-class claims with secondary proof bodies.
8. Provide ASV-compatible output for external interoperability.
9. Implement CACT commitment chain verification for all claim classes.
10. Implement CACT knowledge interrogation for E-class claims.
11. Implement AVAP sealed commit-reveal opinion submission.
12. Implement stratified deep-audit sampling.

### D.3 MAY Requirements (7)

1. Implement alternative proof certificate formats beyond the six specified.
2. Adjust operational parameters within valid ranges without G-class consensus.
3. Implement bootstrap protocol with seed claims.
4. Implement constitutional intent annotations for N-class verification.
5. Implement extended classification appeal protocol.
6. Implement AVAP honeypot claims for D-class and E-class.
7. Implement AVAP collusion deterrence payments.

### D.4 CACT Conformance Requirements (12)

CR-CACT-1: Commitment chains MUST be structurally validated before acceptance.
CR-CACT-2: Commitment timestamps MUST precede VTD submission timestamp.
CR-CACT-3: Purpose reveals MUST hash to committed purpose hashes.
CR-CACT-4: D-class VTDs MUST include CACT commitment chains.
CR-CACT-5: SNARK/STARK proofs MUST be verified against registered circuit verification keys.
CR-CACT-6: KI probe questions MUST be generated from independently retrieved content.
CR-CACT-7: Process trace consistency checks MUST include all five P1-P5 checks.
CR-CACT-8: Environmental audit MUST query external systems directly, not through the agent.
CR-CACT-9: OVC score MUST be computed and recorded for every CACT-verified claim.
CR-CACT-10: OVC-based belief cap MUST be applied before knowledge admission.
CR-CACT-11: Commitment chain rate limit MUST be enforced (default: 100 per epoch).
CR-CACT-12: Evidence binding ratio MUST be recorded in verification metadata.

---

## Appendix E: Test Vectors

### E.1 D-class Hash Verification (TV-D-001)

```json
{
  "test_id": "TV-D-001",
  "claim_text": "SHA-256('hello world') = b94d27b9...",
  "vtd": {
    "proof_body": {
      "proof_type": "HASH_VERIFICATION",
      "computation": { "algorithm": "SHA-256", "version": "FIPS-180-4" },
      "inputs": [{ "name": "message", "value": "hello world" }],
      "output": { "value": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9" }
    }
  },
  "expected_classification": "D",
  "expected_status": "VERIFIED",
  "expected_opinion": { "b": 1.0, "d": 0.0, "u": 0.0, "a": 0.5 }
}
```

### E.2 E-class Source Verification Failure (TV-E-001)

Claim: "GPT-4 achieves 86.4% on MMLU" with source URL returning 404. Expected: FALSIFIED, b_max = 0.1.

### E.3 Subjective Logic Conjunction (TV-SL-001)

```
Input A: (b=0.7, d=0.1, u=0.2, a=0.5)
Input B: (b=0.8, d=0.0, u=0.2, a=0.5)
Expected: (b=0.56, d=0.10, u=0.34, a=0.25)
E = 0.56 + 0.25 * 0.34 = 0.645
```

### E.4 Cumulative Fusion (TV-SL-002)

```
Input A: (b=0.6, d=0.1, u=0.3, a=0.5)
Input B: (b=0.5, d=0.2, u=0.3, a=0.5)
denom = 0.3 + 0.3 - 0.09 = 0.51
Expected: (b=0.6471, d=0.1765, u=0.1765, a=0.5)
E = 0.6471 + 0.5 * 0.1765 = 0.7353
```

### E.5 Trust Discounting (TV-SL-003)

```
Trust: (b=0.9, d=0.0, u=0.1, a=0.5)
Claim: (b=0.8, d=0.1, u=0.1, a=0.5)
Expected: (b=0.72, d=0.09, u=0.19, a=0.5)
E = 0.72 + 0.5 * 0.19 = 0.815
```

### E.6 Deep-Audit Detection Probability (TV-DA-001)

```
Audit rate: 0.07
P(detected within 10 epochs) = 1 - 0.93^10 = 0.516
P(detected within 50 epochs) = 1 - 0.93^50 = 0.971
P(detected within 100 epochs) = 1 - 0.93^100 = 0.9993
```

### E.7 Classification Disagreement (TV-CLS-001)

Agent suggests E, structural analysis yields S, independent classifier yields H. Full disagreement: resolve to most conservative (H). Seal type: CONSERVATIVE. Tier: STRUCTURED_ATTESTATION.

### E.8 Credibility Decay (TV-DECAY-001)

E-class claim, initial (b=0.8, d=0.05, u=0.15, a=0.5), half-life 180 days, age 180 days. Decay factor = 0.5. Expected: (b=0.4, d=0.05, u=0.55, a=0.5). E = 0.4 + 0.5 * 0.55 = 0.675. Above re-verification threshold (0.5).

### E.9 CACT Commitment Chain Validation (TV-CACT-001)

Valid chain with 5 commitments, binding ratio 0.90. Expected: OVC channel 1 score = 0.90, credibility boost = +0.05.

### E.10 KI Probe Verdict (TV-KI-001)

Agent answers 4/5 questions correctly (accuracy = 0.80). Expected: SURVIVED, credibility adjustment = +0.05.

---

## Appendix F: Traceability Matrix

| Feasibility Condition | Spec Section | Status |
|----------------------|-------------|--------|
| GATE-1: VTD Feasibility | Sections 4, 6 | VTD schemas and verification protocols specified |
| GATE-2: Classification Reliability | Section 5 | Three-way classification protocol with 9 classes specified |
| GATE-3: Credibility Propagation | Section 9 | Dampening algorithm with convergence guarantees |
| GATE-4: Probing Effectiveness | Section 7 | Six probe types (including KI) with budget allocation |
| REQ-1: Source Verification | Section 6.2 (E-class) | Enhanced source verification with independent retrieval |
| REQ-2: Membrane Classification | Section 5.4 | INV-M2 with three-way protocol |
| REQ-3: Class-Specific Credibility | Section 9.2 | INV-M4 with per-class opinion tracking |
| REQ-4: Deep-Audit Protocol | Section 6.4 | VRF selection at 7% with stratified sampling |
| REQ-5: Unified vs. Split Validation | Section 16 (Q5) | Open design question requiring comparative analysis |
| REC-1: Bootstrap Protocol | Sections 14.2, 16 (Q6) | Bootstrap security specified; details open |
| REC-2: Constitutional Parameters | Appendix C | 47 parameters with governance levels |
| REC-3: VTD Size Limits | Section 4.5 | Per-class limits specified (9 classes) |
| CACT-1: Forgery Defense | Sections 8, 12 | 9-layer defense-in-depth specified |
| AVAP-1: Collusion Defense | Section 13 | 9-layer defense-in-depth specified |

---

## Appendix G: CACT Parameters and Test Vectors

### G.1 CACT Configurable Parameters

| Parameter | Default | Range | Governance |
|-----------|---------|-------|------------|
| CACT_ABSENT_CREDIBILITY_CAP | 0.70 | [0.50, 0.90] | Operational |
| OVC_MIN_CAP | 0.50 | [0.30, 0.70] | G-class |
| OVC_MAX_CAP | 0.95 | [0.80, 1.00] | G-class |
| MAX_COMMITMENTS_PER_EPOCH | 100 | [20, 500] | Operational |
| KI_CORRECT_THRESHOLD | 0.70 | [0.50, 0.90] | Operational |
| KI_PASS_THRESHOLD | 0.80 | [0.60, 0.95] | Operational |
| KI_MARGINAL_THRESHOLD | 0.50 | [0.30, 0.70] | Operational |
| KI_TIMEOUT_MS | 30000 | [10000, 60000] | Operational |
| PROCESS_TRACE_ABSENT_CAP | 0.75 | [0.50, 0.90] | Operational |
| SOURCE_SUPPORT_THRESHOLD | 0.40 | [0.20, 0.70] | Operational |
| COMMITMENT_CHAIN_WEIGHTS | [0.30, 0.25, 0.20, 0.25] | -- | G-class |
| MIN_TEMPORAL_SPAN_SECONDS | 60 | [10, 600] | Operational |
| FORGERY_ESCALATION_THRESHOLD | 0.50 | [0.30, 0.70] | Operational |

### G.2 CACT Test Vectors

(Refer to C11 Appendix B for 5 detailed test vectors covering commitment chain validation, SNARK verification, KI interrogation, process trace consistency, and OVC score computation.)

---

## Appendix H: AVAP Parameters

| Parameter | Default | Range | Governance |
|-----------|---------|-------|------------|
| AVAP_COVER_TRAFFIC_RATIO | 3.0 | [2.0, 5.0] | Operational |
| AVAP_COMMIT_TIMEOUT_MS | 15000 | [5000, 30000] | Operational |
| AVAP_REVEAL_TIMEOUT_MS | 10000 | [5000, 20000] | Operational |
| AVAP_NON_REVEAL_PENALTY | 0.15 | [0.05, 0.30] | Operational |
| AVAP_HONEYPOT_INJECTION_RATE | 0.04 | [0.02, 0.10] | G-class |
| AVAP_DEFECTOR_BOUNTY_BASE | 2.0x | [1.5x, 5.0x] | G-class |
| AVAP_DEFECTOR_BOUNTY_MAX | 10.0x | [5.0x, 20.0x] | G-class |
| AVAP_CMI_LOOKBACK_EPOCHS | 100 | [50, 300] | Operational |
| AVAP_CMI_THRESHOLD | 0.15 | [0.05, 0.30] | Operational |
| AVAP_OVERHEAD_BUDGET | 0.20 | [0.10, 0.30] | G-class |
| MIN_COMMITTEE_ANONYMITY_WINDOW_MS | 30000 | [10000, 60000] | Operational |

---

## Appendix I: Glossary

| Term | Definition |
|------|-----------|
| AIC | Atrahasis Intelligence Credit -- unit of economic value in the Settlement Plane |
| ASV | Atrahasis Semantic Vocabulary (C4) -- structured vocabulary for AI communication |
| AVAP | Anonymous Verification with Adaptive Probing -- 5-mechanism anti-collusion subsystem |
| BDL | Bounded Durability Layer -- persistence layer of the Knowledge Cortex |
| BFT | Byzantine Fault Tolerance |
| CACT | Commit-Attest-Challenge-Triangulate -- 4-mechanism VTD forgery defense subsystem |
| CIOS | Core Intelligence Operating System -- top-level orchestration layer |
| CLS | Classification Seal -- signed attestation of claim classification |
| CLM | Claim token (ASV type) |
| CMI | Conditional Mutual Information -- statistical measure for detecting selective collusion |
| D/E/S/H/N/P/R/C/K | The nine PCVM claim classes |
| DSF | Distributed Settlement Fabric (C8) -- economic incentive and slashing system |
| ECVRF | Elliptic Curve Verifiable Random Function (RFC 9381) |
| EVD | Evidence token (ASV type) |
| FRI | Fast Reed-Solomon Interactive Oracle Proof -- STARK verification protocol |
| KI | Knowledge Interrogation -- CACT probe type testing generative knowledge |
| LRS | Linkable Ring Signature -- used in AVAP for anonymous defector reporting |
| MCT | Membrane Credibility Token -- signed attestation of claim admission |
| MQI | Membrane Quality Index -- health metrics for the Sentinel Graph |
| OVC | Orthogonal Verification Coverage -- multi-channel verification depth score |
| PCVM | Proof-Carrying Verification Membrane |
| PRV | Provenance token (ASV type) |
| SNARK | Succinct Non-interactive Argument of Knowledge |
| STARK | Scalable Transparent Argument of Knowledge |
| TIDAL_EPOCH | The 3,600-second (1-hour) scheduling cycle inherited from C3 (Tidal Noosphere). Distinguished from SETTLEMENT_TICK (60s, C8) and CONSOLIDATION_CYCLE (36,000s, C6). All unqualified uses of "epoch" in this specification refer to TIDAL_EPOCH unless explicitly stated otherwise. See C9 Section SS3.3 for the canonical three-tier epoch hierarchy. |
| VRF | Verifiable Random Function |
| VTD | Verification Trace Document -- structured proof artifact |

---

## References

[1] Tidal Noosphere: Coordination Fabric for Planetary AI Cooperation. Atrahasis Agent System C3 Master Tech Spec, 2026.

[2] G. C. Necula, "Proof-Carrying Code," in Proceedings of the 24th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL), 1997, pp. 106-119.

[3] S. Min, K. Krishna, X. Lyu, M. Lewis, W. Yih, P. Koh, M. Iyyer, L. Zettlemoyer, H. Hajishirzi, "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation," in Proceedings of EMNLP, 2023.

[4] D. Wei, S. Wang, N. Cheng, J. Xi, Y. Qi, Z. Ren, Y. Su, "Long-form Factuality in Large Language Models," arXiv:2403.18802, 2024.

[5] S. Dhuliawala, M. Komeili, J. Xu, R. Raileanu, X. Li, A. Celikyilmaz, J. Weston, "Chain-of-Verification Reduces Hallucination in Large Language Models," arXiv:2309.11495, 2023.

[6] J. Yang et al., "CLOVER: Closed-Loop Verifiable Code Generation," arXiv:2310.17110, 2023.

[7] G. H. Guyatt, A. D. Oxman, G. E. Vist, R. Kunz, Y. Falck-Ytter, P. Alonso-Coello, H. J. Schunemann, "GRADE: an emerging consensus on rating quality of evidence and strength of recommendations," BMJ, vol. 336, no. 7650, pp. 924-926, 2008.

[8] M. Brush, K. Shefchek, M. Haendel, "SEPIO: A Semantic Model for the Integration and Analysis of Scientific Evidence," in ICBO, 2016.

[9] L. Moreau, P. Missier, "PROV-DM: The PROV Data Model," W3C Recommendation, 2013.

[10] A. Josang, "Subjective Logic: A Formalism for Reasoning Under Uncertainty," Springer, 2016.

[11] J. Groth, "On the Size of Pairing-Based Non-interactive Arguments," in EUROCRYPT, 2016.

[12] E. Ben-Sasson, I. Bentov, Y. Horesh, M. Riabzev, "Scalable, Transparent, and Post-Quantum Secure Computational Integrity," IACR Cryptology ePrint Archive, 2018.

---

## Changelog

### v2.0.0 (2026-03-10) — Unified Specification

**Supersedes:** C5 MASTER_TECH_SPEC v1.0.0, C5 PATCH_ADDENDUM v1.1, C10 Hardening Addendum (C5 portions), C11 CACT v1.0.0, C12 AVAP v1.0.0

**Major changes:**

1. **9-class taxonomy:** Added K-class (Knowledge Consolidation) per C9 reconciliation. Updated all enumerations, schemas, tables, and protocols to include K-class. (Source: PA-F29)

2. **Corrected cost claims:** Abstract and Conclusion now lead with 17% direct savings (0.83x), qualifying the 40-60% figure as projected contingent on citation density. (Source: PA-F19)

3. **Classification signatures defined:** Complete CLASSIFICATION_SIGNATURES dictionary with markers and exclusions for all 9 classes. (Source: PA-F20)

4. **Conservatism ordering updated:** H>N>K>E>S>R>P>C>D with detailed rationale explaining rigor-based (not cost-based) ordering. (Source: PA-F21)

5. **Source verification fixed:** Level 4 (contextual relevance) made probe-triggered only, avoiding verification regress. (Source: PA-F22)

6. **Probe budget defined:** 1 token = 1 AIC, with operation cost table and K-class budget. (Source: PA-F23)

7. **Cost model separated:** Producer vs. verifier costs with K-class. (Source: PA-F24)

8. **K-class verification protocol:** Complete 6-step protocol with VTD schema, committee parameters, and verification pseudocode. (Source: PA-F29)

9. **Parameter defaults:** 14 critical parameters defined with ranges and governance levels. (Source: PA-F30)

10. **cls_id format defined:** mct:<class>:<epoch>:<committee_hash>:<nonce>. (Source: PA-F31)

11. **Deep-audit stratified sampling:** Stratification by agent, domain, and dependency cluster. (Source: PA-F32)

12. **C10 hardening integrated:** Mandatory source verification (CR-H1), cross-verifier evidence correlation (CR-H2), evidence belief cap (CR-H3), forgery heuristics (CR-H4), economic deterrents (CR-H5), Sentinel Graph cluster exclusion (CR-H6), statistical collusion detection (CR-H7), diversity-constrained committees (CR-H8), adaptive audit rates (CR-H9).

13. **CACT integrated (new Section 8):** Temporal commitment binding, verifiable computation (SNARK/STARK), knowledge interrogation (KI probe type), orthogonal verification channels (process traces, environmental side-effects), OVC scoring, credibility integration. VTD envelope extended with cact_extension field. D-class proof types extended with SNARK_PROOF and STARK_PROOF.

14. **AVAP integrated (new Section 13):** Anonymous VRF self-selection committees (M1), sealed commit-reveal opinions (M2), honeypot claims (M3), collusion deterrence payments (M4), conditional behavioral analysis (M5).

15. **Defense-in-depth sections added:** Section 12 (VTD Forgery: 9 defense layers) and Section 13 (Collusion: 9 defense layers) consolidate all defenses.

16. **Security analysis updated:** VTD forgery residual risk reduced from HIGH to MEDIUM. Collusion residual risk reduced from HIGH to MEDIUM-LOW. Detection probability tables updated.

17. **New appendices:** Appendix G (CACT parameters), Appendix H (AVAP parameters), expanded glossary (Appendix I).

### v1.0.0 (2026-03-10) — Original Specification

Initial PCVM specification with 8 claim classes, 3 verification tiers, 7 invariants, 5 probe types, Subjective Logic credibility engine, and knowledge admission protocol.

---

*Master Technical Specification v2.0.0 completed 2026-03-10. Unified rewrite integrating C5 v1.0.0, C5 Patch Addendum v1.1, C10 Hardening (C5 portions), C11 CACT v1.0.0, and C12 AVAP v1.0.0. Specification Writer, Atrahasis Agent System v2.0.*
*Protocol: Specification Stage, C5 Proof-Carrying Verification Membrane.*
