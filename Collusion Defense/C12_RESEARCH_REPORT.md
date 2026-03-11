# C12 RESEARCH REPORT: AVAP (Anonymous Verification with Adaptive Probing)

**Invention:** C12 -- Collusion Defense
**Stage:** RESEARCH
**Date:** 2026-03-10
**Concept:** C12-B (AVAP) -- 5-mechanism anti-collusion architecture
**Ideation Score:** Novelty 4/5, Feasibility 4/5

---

## TABLE OF CONTENTS

1. [Prior Art Analysis](#1-prior-art-analysis)
   - 1.1 Anonymous Committees (Mechanism 1)
   - 1.2 Sealed Opinion Submission (Mechanism 2)
   - 1.3 Honeypot Claims / Canary Trap (Mechanism 3)
   - 1.4 Collusion Deterrence Payment (Mechanism 4)
   - 1.5 Conditional Behavioral Analysis (Mechanism 5)
   - 1.6 Overall Novelty Assessment
2. [Landscape Analysis](#2-landscape-analysis)
3. [Science Assessment](#3-science-assessment)
4. [Research Synthesis](#4-research-synthesis)

---

## 1. PRIOR ART ANALYSIS

### 1.1 Anonymous Committees (Mechanism 1)

#### Existing Prior Art

**Algorand Cryptographic Sortition (2017-present).** Algorand pioneered VRF-based secret self-selection for consensus committees. Each user independently evaluates a VRF using their private key and public blockchain state to determine committee membership. The key properties are identical to AVAP's goals: (a) committee membership is private until revealed, (b) selection is non-interactive (no coordinator needed), (c) a short cryptographic proof demonstrates membership to others. Algorand's sortition is computationally cheap -- equivalent to computing a single signature. The mechanism was designed explicitly to prevent targeted attacks: "an adversary does not know which user to target until that user has finished their work."

**DFINITY / Internet Computer Threshold Relay (2018-present).** DFINITY uses threshold BLS signatures as a random beacon for committee selection. Groups are set up with threshold signature key pairs, and committee relay occurs automatically due to BLS uniqueness. The threshold is 1/3 for random beacon signatures, 2/3 for certified state. The mechanism provides different security trade-offs than Algorand's self-selection -- DFINITY committees are known to each other but produce collectively unpredictable outputs.

**Ethereum Single Secret Leader Election (SSLE) (2023-present, research phase).** Ethereum is actively researching SSLE protocols, with two candidate approaches:
- **Whisk**: Shuffles a candidate list using verifiable random permutations and ZKPs. Introduces ~20-30x overhead vs. status quo but remains feasible within Ethereum's timing constraints.
- **Homomorphic Sortition**: Only the selected leader knows they've been selected until they choose to reveal. Uses homomorphic encryption over commitments.

Both are in research phase with no finalized specification.

**Supra Threshold AI Oracles (2025-present).** Supra's oracle network assigns multi-agent AI committees to evaluate queries across dimensions (factual accuracy, contextual relevance, etc.). Agent assignment is randomized, cross-committee overlap is minimized, and regular rotation of node-to-tribe assignments exponentially increases security. Threshold BLS signatures provide cryptographic proof of quorum consensus.

**Secret Multiple Leaders & Committee Election (IEEE 2024).** Extends SSLE to multi-leader and committee contexts for sharded blockchains.

#### What AVAP Adds Beyond Prior Art

| Feature | Algorand | DFINITY | Ethereum SSLE | Supra | AVAP |
|---|---|---|---|---|---|
| Self-selection via VRF | Yes | No (threshold) | Yes (Whisk/HS) | Partial | Yes |
| Committee anonymity from each other | Yes (pre-reveal) | No | Yes | Partial | Yes |
| Anonymity from claim submitter | N/A | N/A | N/A | Partial | Yes |
| Post-submission reveal only | Partial | No | Yes | No | Yes |
| Applied to verification (not consensus) | No | No | No | Yes | Yes |

**Novelty assessment for Mechanism 1: LOW-MODERATE (2/5).** The cryptographic primitives (VRF-based self-selection, sealed committee membership) are well-established in blockchain consensus. AVAP's contribution is applying these to a verification context with bidirectional anonymity (verifiers anonymous from each other AND from claim submitters), which is a novel application rather than a novel primitive. The "reveal only after all opinions sealed" constraint adds a meaningful layer not present in most blockchain committee designs, which reveal membership at proposal time.

**Confidence: HIGH.** The prior art landscape is well-documented and mature.

---

### 1.2 Sealed Opinion Submission (Mechanism 2)

#### Existing Prior Art

**Commit-Reveal Schemes (established cryptographic primitive).** The commit-reveal pattern -- hash(opinion || nonce) committed first, then (opinion, nonce) revealed -- is a foundational cryptographic technique used extensively in:
- **Blockchain voting**: Ethereum-based governance systems (e.g., Snapshot, Tally) use commit-reveal for on-chain votes.
- **Sealed-bid auctions**: Vickrey auctions on Ethereum use Pedersen commitments (C = xG + rH) for bid privacy. Research includes verifiable sealed-bid auctions (Galal & Youssef, 2018), ZK-SNARK-based schemes (Li et al., 2021), and FHE-based approaches (2024-2025).
- **MACI (Minimal Anti-Collusion Infrastructure)**: Proposed by Vitalik Buterin (2019), MACI uses encryption and zk-SNARKs so voters cannot prove how they voted, preventing bribery. Votes are encrypted on-chain, with final results published and verified with cryptographic proofs. MACI is actively maintained and deployed for quadratic voting in Ethereum governance.

**Key limitation of basic commit-reveal** (identified in literature): Although commit-reveal ensures trustless execution, it ultimately exposes all values during the reveal phase, offering no post-reveal privacy. MACI addresses this by using a trusted coordinator with a private key, but this introduces a trust assumption.

**Cryptobazaar (2024).** Advances private sealed-bid auctions at scale using novel cryptographic techniques beyond basic commit-reveal.

**Fast and Gas-efficient Private Sealed-bid Auctions (2025).** Recent work on reducing the computational overhead of sealed-bid mechanisms on-chain.

#### What AVAP Adds Beyond Prior Art

AVAP's commit-reveal for opinions is a direct application of an established primitive. The "simultaneous reveal after commitment deadline" is standard. The combination with anonymous committees (Mechanism 1) creates a stronger guarantee -- you can't signal through early/late submission because committee membership is unknown.

**Novelty assessment for Mechanism 2: LOW (1/5).** This is a well-established cryptographic primitive applied in its standard form. The novelty comes only from the combination with other AVAP mechanisms, not from the mechanism itself. MACI is a more sophisticated version of what AVAP proposes, with additional protections against post-vote coercion.

**Confidence: VERY HIGH.** Commit-reveal is among the most studied cryptographic patterns.

---

### 1.3 Honeypot Claims / Canary Trap (Mechanism 3)

#### Existing Prior Art

**Honeypots in Cybersecurity (1990s-present).** Honeypots are fake systems designed to attract and detect attackers. Modern honeypots use AI/ML to generate synthetic environments indistinguishable from real systems. Key developments:
- **Thinkst Canary**: Commercial canary token platform that deploys decoy files, credentials, and services.
- **AI-Generated Honeypots (2024-2025)**: GANs generate synthetic network environments, device configurations, and service responses indistinguishable from real systems. LLM-based honeypots produce responses matching true service outputs.
- **Honeypot detection by adversaries**: Attackers use tools (Censys, Shodan, Nmap scripts) to detect honeypot fingerprints via latency anomalies, filesystem inconsistencies, and behavioral mismatches.

**Canary Traps in Intelligence (Cold War era-present).** The canary trap method involves distributing slightly different versions of sensitive information to different suspects. When a leak occurs, the unique variation identifies the source. Historical and modern applications:
- Tom Clancy popularized the term in "Patriot Games" (1987).
- Elon Musk used variant emails at Tesla (2008) to identify leakers.
- **Zero-width Unicode characters** can create invisible, persistent fingerprints in digital text.
- **Trap streets in cartography**: Fictitious map entries to detect plagiarism. Extended to "paper towns," mountains with wrong elevations, etc.

**AI-Powered Canary Traps (2021).** Research on using AI to generate more sophisticated canary trap variants at scale, protecting government secrets.

**Test Collusion Detection in Educational Testing.** Standardized testing organizations inject known-answer items (operational honeypots) and use statistical methods (response similarity indices) to detect answer-copying rings. The "Confidence Screening Detector" (2023) detects test collusion using variable selection from high-dimensional statistical analysis.

#### What AVAP Adds Beyond Prior Art

| Feature | Cybersecurity Honeypots | Canary Traps | Test Collusion Detection | AVAP Honeypots |
|---|---|---|---|---|
| Synthetic test items with known ground truth | Partial | No | Yes | Yes |
| Multiple variants per claim (fingerprinting) | No | Yes | No | Yes |
| Cross-claim-type coverage (D, E, S, H) | N/A | N/A | Partial | Yes |
| Integrated into verification pipeline | No | No | Partial | Yes |
| ~5% injection rate as calibrated parameter | N/A | N/A | Varies | Yes |

**Key prior art gap:** The combination of (a) honeypot injection into an AI verification pipeline with (b) canary-trap variant fingerprinting and (c) cross-claim-type coverage appears to be novel. Educational testing does (a) but not (b). Intelligence operations do (b) but not in automated verification contexts.

**Novelty assessment for Mechanism 3: MODERATE (3/5).** Each component (honeypots, canary traps, test collusion detection) is well-established in its domain. The synthesis -- injecting fingerprinted synthetic claims across claim types into an AI verification pipeline -- is a novel combination. The 5% injection rate as a tunable parameter is an engineering choice, not a theoretical contribution. The critical unsolved problem is indistinguishability: can honeypot claims be made truly indistinguishable from real claims across all claim types, especially heuristic (H-type) claims?

**Confidence: HIGH for individual components, MODERATE for indistinguishability claims.**

---

### 1.4 Collusion Deterrence Payment / CDP (Mechanism 4)

#### Existing Prior Art

**Leniency Programs in Competition Law (1978-present).** The US DOJ's Corporate Leniency Program (1978, revised 1993) and the EU's Leniency Notice provide the foundational model:
- **First reporter gets full immunity** from fines.
- **Graduated reductions**: EU provides 30-50% reduction for first cooperator, 20-30% for second, up to 20% for subsequent.
- **Game-theoretic analysis**: Extensive literature on leniency as a prisoner's dilemma destabilizer. Motta & Polo (2003), Spagnolo (2004), and others formalize how leniency creates a "race to the courthouse."
- **Effectiveness**: Statistical evidence consistent with leniency enhancing both deterrence and detection. However, some models show leniency can *stabilize* some cartels (by reducing expected penalties) or encourage new cartels to form.
- **Critical finding**: Leniency may be ineffective when detection probabilities are already high, or when colluders can pre-commit to not defecting (e.g., through side agreements).

**SEC Whistleblower Program (2010-present).** Dodd-Frank Act created monetary incentives for reporting securities violations:
- Awards of 10-30% of sanctions exceeding $1M.
- Has generated $1B+ in sanctions from whistleblower tips.
- Anonymous reporting through SEC portal.

**EU Whistleblower Tool (2017-present).** Anonymous tool for reporting anticompetitive conduct, but notably *does not offer rewards*, limiting effectiveness compared to SEC model.

**Bug Bounty Programs (2004-present).** HackerOne, Bugcrowd, and similar platforms pay for vulnerability disclosure. Graduated bounty structures based on severity are standard. Direct precedent for CDP's graduated bounty (10%/25%/50%).

**Smart Contract Anti-Collusion (2018-present).** "Betrayal, Distrust, and Rationality: Smart Counter-Collusion Contracts for Verifiable Cloud Computing" uses game theory and smart contracts where a client asks two cloud servers to compute the same task, with contracts designed to stimulate tension, betrayal and distrust between the clouds.

**AVAP's CDP vs. Prior Art:**

| Feature | DOJ Leniency | SEC Whistleblower | Bug Bounties | AVAP CDP |
|---|---|---|---|---|
| First defector advantage | Yes (full immunity) | Partial | N/A | Yes (bounty) |
| Graduated rewards | Yes (30-50%, 20-30%, <20%) | Yes (10-30%) | Yes (by severity) | Yes (10%/25%/50%) |
| Funded from violator assets | Yes (fine reduction) | Yes (sanctions) | No (program budget) | Yes (forfeited stake) |
| Evidence requirements | Yes (cooperation) | Yes (original info) | Yes (valid bug report) | Yes (logs, artifacts, patterns) |
| Applied to AI agent systems | No | No | No | Yes |
| Automated/programmatic execution | No | No | Partial | Yes (smart contract) |

**Novelty assessment for Mechanism 4: LOW-MODERATE (2/5).** The CDP is a faithful adaptation of well-proven human anti-collusion mechanisms (leniency programs, whistleblower bounties) into an AI agent context. The graduated bounty structure (10%/25%/50%) is well within the range of existing programs. The genuine novelty is in (a) applying this to autonomous AI agents rather than human firms, and (b) the evidence types required (communication logs, coordination artifacts, predicted behavior patterns) which are AI-specific.

**Critical concern from literature**: Idowu et al. (2026) identify that AI agents may collude *without awareness* (emergent coordination rather than explicit agreement), which undermines the entire premise of a defection-based mechanism -- you can't defect from an arrangement you don't know you're in.

**Confidence: HIGH for mechanism design, MODERATE for applicability to AI agents.**

---

### 1.5 Conditional Behavioral Analysis (Mechanism 5)

#### Existing Prior Art

**Conditional Mutual Information (CMI) in Statistics.** CMI measures the expected mutual information between two variables given a third. Formally: I(X;Y|Z) = H(X|Z) - H(X|Y,Z). Well-established in:
- Gene regulatory network inference (separating direct from indirect regulations).
- Information-theoretic independence testing.
- Mixed-data estimation methods (Mesner & Shalizi, 2020; Mukherjee & Steorts, 2022).

**Test Collusion Detection.** The "Confidence Screening Detector" (PMC 2023) detects test collusion by analyzing response patterns conditional on test administration context. Uses variable selection from high-dimensional statistical analysis.

**Algorithmic Collusion Detection (2024-2026 active research area).**
- Fish et al. (2024): "Algorithmic Collusion by Large Language Models" demonstrates LLMs autonomously learn supra-competitive pricing without explicit communication.
- "Breaking Algorithmic Collusion in Human-AI Ecosystems" (2025): Develops detection and mitigation strategies including reward perturbation and policy regularization.
- Idowu et al. (2026): "Mapping Human Anti-collusion Mechanisms to Multi-agent AI" provides taxonomy including monitoring/auditing with statistical screens and ML classifiers.

**Behavioral monitoring approaches from literature:**
- Bid-distribution and rotation features reliably separate competitive from collusive tenders.
- Screen-based ML models transfer across jurisdictions.
- NLP-based screens audit communications for collusive signaling.

**A/B Testing for Manipulation Detection.** Standard in tech industry for detecting coordinated behavior. Facebook, Google, and others use conditional behavioral analysis to detect bot networks and coordinated inauthentic behavior by comparing behavior patterns across different treatment groups.

#### What AVAP Adds Beyond Prior Art

AVAP's key insight -- P(agent_opinion | committee_contains_ally) != P(agent_opinion | committee_without_ally) -- is a specific instantiation of conditional independence testing applied to committee composition. This specific formulation appears to be novel in the literature. The closest analogs are:

1. **Differential association testing** in criminology (behavior changes in presence of criminal associates).
2. **Interaction effects in factorial experimental design** (treatment effects that depend on group composition).
3. **Network-conditioned behavior analysis** in social network research.

The explicit framing as "honest agents are invariant to committee composition while colluders are not" is a clean, testable hypothesis that does not appear in the collusion detection literature in this form.

**Novelty assessment for Mechanism 5: MODERATE-HIGH (3.5/5).** The statistical machinery (CMI, conditional independence testing) is established. The specific application -- detecting collusion by testing behavioral invariance to committee composition -- appears genuinely novel. This is the most original mechanism in AVAP. However, the practical challenges (sample size requirements, adversarial evasion) are significant and under-addressed.

**Confidence: MODERATE.** The theoretical framing is sound but empirical validation is absent.

---

### 1.6 Overall Novelty Assessment

| Mechanism | Individual Novelty | Contribution Type |
|---|---|---|
| 1. Anonymous Committees | 2/5 | Application of established primitives to verification context |
| 2. Sealed Opinions | 1/5 | Direct use of standard cryptographic pattern |
| 3. Honeypot Claims | 3/5 | Novel synthesis of honeypots + canary traps + claim-type coverage |
| 4. CDP | 2/5 | Faithful adaptation of proven human mechanisms to AI |
| 5. Conditional Behavioral Analysis | 3.5/5 | Novel application of CMI to committee-conditioned collusion detection |

**System-level novelty: 3.5/5.** While individual mechanisms have substantial prior art, the *integrated system* -- combining structural anonymity, cryptographic commitment, proactive probing, economic deterrence, and conditional detection -- as a unified anti-collusion architecture for AI verification is novel. No existing system combines all five layers. The closest competitor (Supra Threshold AI Oracles) implements ~2.5 of the 5 mechanisms (partial anonymous committees, threshold cryptography, staking) but lacks honeypot probing, CDP, and conditional behavioral analysis.

**The genuinely novel contributions of AVAP are:**
1. The canary-trap pattern applied to verification claims (fingerprinted variant injection).
2. Conditional behavioral analysis on committee composition as a collusion signal.
3. The integrated 5-layer architecture as a defense-in-depth system.

---

## 2. LANDSCAPE ANALYSIS

### 2.1 Who Else Is Solving This Problem?

**Active Research Groups and Systems:**

| Entity | Approach | Overlap with AVAP | Status |
|---|---|---|---|
| **Algorand** | VRF-based secret sortition for consensus | Mechanism 1 (anonymous committees) | Production (since 2019) |
| **Ethereum Foundation** | MACI (anti-collusion voting), SSLE (secret leader election) | Mechanisms 1+2 | MACI: Production; SSLE: Research |
| **Supra** | Threshold AI oracles with randomized committee assignment | Mechanisms 1+2, partial 4 (staking) | Production (2025) |
| **Idowu et al.** | Taxonomy of human anti-collusion for multi-agent AI | Framework overlapping all 5 mechanisms | Conceptual/taxonomic (2026) |
| **Fish et al.** | LLM algorithmic collusion detection | Related to Mechanism 5 | Academic (2024) |
| **Purdue Engineering** | "Can AI Agents Learn to Collude?" | Emergence + detection + mitigation | Research proposal (2025-26) |
| **EU Competition Law** | Leniency programs, whistleblower tools | Mechanism 4 | Operational (decades) |
| **Educational Testing (ETS, etc.)** | Honeypot items + statistical collusion detection | Mechanisms 3+5 | Operational |

### 2.2 State of the Art in Collusion Detection

The state of the art is fragmented across domains:

1. **Blockchain consensus**: Strong anonymous committee selection (Algorand, Ethereum SSLE). Weak on post-hoc collusion detection.
2. **Anti-trust/competition law**: Mature leniency and whistleblower mechanisms. Emerging work on algorithmic collusion detection (OECD 2017, Fish et al. 2024).
3. **Multi-agent AI safety**: Rapidly emerging field. Byzantine fault tolerance provides resilience but not detection. CP-WBFT (confidence probe-based weighted BFT) is a recent advance. Key challenge: steganographic collusion where agents hide coordination signals in normal-looking outputs.
4. **Educational testing**: Operational honeypot-and-statistics approach, but in a much simpler domain (multiple-choice answers vs. complex verification opinions).

**Critical gap in the landscape:** No existing system combines *prevention* (anonymous committees, sealed opinions) with *detection* (honeypots, behavioral analysis) with *deterrence* (economic incentives to defect). Systems tend to focus on one layer. AVAP's defense-in-depth architecture addresses this gap.

### 2.3 Market / Research Window

**The window is OPEN but narrowing.**

**Evidence the window is open:**
- Idowu et al. (January 2026) describe the field as "primarily conceptual and taxonomic rather than empirical" -- no operational multi-mechanism anti-collusion system exists for multi-agent AI.
- Purdue's 2025-26 research proposal ("Can AI Agents Learn to Collude?") indicates the field is in its early stages.
- Supra's Threshold AI Oracles (2025) are the closest production system but implement only partial anti-collusion (randomized assignment + staking, no honeypots or behavioral analysis).

**Evidence the window is narrowing:**
- Multiple research groups are converging on the same problem (Idowu, Fish, Purdue, Ethereum Foundation).
- The "Mapping Human Anti-collusion Mechanisms to Multi-agent AI" paper (2026) provides a taxonomy that could guide rapid implementation by well-resourced teams.
- Secret steganographic collusion among LLM agents (Motwani et al., 2024) is raising urgency.

**Assessment:** AVAP has a 12-18 month window to establish the integrated 5-mechanism architecture before the research community converges on similar solutions. The honeypot/canary-trap and conditional behavioral analysis components are the most defensible novel contributions.

---

## 3. SCIENCE ASSESSMENT

### 3.1 Mechanism 1: Anonymous Committees

**Soundness Rating: 4/5**

**Core question: Is full anonymity achievable in a system where agents interact?**

**Analysis:**

The cryptographic foundations are sound. VRF-based self-selection is proven in Algorand (operational since 2019). The scheme provides:
- **Pre-reveal anonymity**: Guaranteed by VRF properties (pseudorandomness, uniqueness).
- **Post-reveal verifiability**: VRF proofs allow anyone to verify membership after reveal.

**Side channels that leak committee membership:**

1. **Timing side channels**: Agents who know they're on a committee may behave differently (e.g., requesting claim data, allocating compute resources). If the system requires verifiers to actively fetch claim information, network traffic patterns could reveal who is verifying what. **Mitigation**: All agents could fetch all claims (expensive) or use private information retrieval (PIR) protocols.

2. **Computational side channels**: VRF computation itself is cheap (one signature), but subsequent verification work (analyzing the claim) may be observable through resource consumption patterns. **Mitigation**: Dummy verification workloads.

3. **Interaction-based leakage**: In a system where agents interact on other tasks, behavioral changes (reduced availability, altered communication patterns) during committee service could signal membership. **Mitigation**: Decouple verification scheduling from other activities; use asynchronous verification with flexible deadlines.

4. **Correlation attacks over time**: If committee selection is seeded from public blockchain state, and an adversary knows the VRF public keys and the selection algorithm, they may be able to narrow down committee membership probabilistically. **Mitigation**: Standard -- use sufficiently large committees relative to the agent pool.

5. **Sybil attacks**: An adversary controlling multiple agents has higher probability of having at least one agent on any given committee, enabling partial deanonymization. **Mitigation**: Stake-weighted selection (standard in blockchain systems).

**Critical gap**: The AVAP design specifies "committee membership revealed only AFTER all opinions are submitted and sealed." This creates a timing dependency: the system must wait for all committee members to submit before revealing. What happens if a committee member goes offline? Timeout mechanisms could leak information (e.g., if the system extends the deadline, observers infer a missing member). Standard solution: over-size committees with threshold requirements (e.g., require 7 of 10 members to submit within deadline).

**Experiments needed:**
- Simulation of timing-based side channel attacks under realistic network conditions.
- Analysis of correlation attack success rate vs. committee size and agent pool size.
- Measurement of information leakage from timeout/extension events.

---

### 3.2 Mechanism 2: Sealed Opinion Submission

**Soundness Rating: 4.5/5**

**Core question: Can timing attacks or strategic late submission undermine the commitment scheme?**

**Analysis:**

The commit-reveal scheme is cryptographically sound when properly implemented:
- **Binding property**: An agent cannot change their opinion after commitment (guaranteed by hash function collision resistance).
- **Hiding property**: The opinion is hidden until reveal (guaranteed by nonce entropy).

**Timing attacks:**

1. **Last-moment submission**: An agent who submits just before the commitment deadline could potentially observe which other agents have already committed (if commitment transactions are public). While they can't see the *content* of others' commitments, knowing *who* has committed could provide information in combination with other signals. **Mitigation**: Blind the commitment process so agents cannot observe who has committed until the deadline passes. Alternatively, use a commitment relay (agents submit to a coordinator who batches and publishes all commitments simultaneously).

2. **Commit-but-don't-reveal attacks**: An agent commits but then refuses to reveal, potentially disrupting the process or gaining information from others' reveals. **Mitigation**: Require a bond/stake that is forfeited on non-reveal. Use threshold reveal mechanisms.

3. **Front-running in on-chain implementations**: If commitments are submitted to a blockchain, miners/validators could see them in the mempool. **Mitigation**: Encrypted mempool or off-chain commitment aggregation.

**Integration with Mechanism 1 (anonymous committees)**: The combination is synergistic. Because committee members don't know who else is on the committee, they can't target specific agents for timing analysis. This is a genuine strength of the integrated design.

**Critical gap**: The proposal doesn't specify whether the commitment is on-chain or off-chain. On-chain commitments have front-running and gas-cost concerns. Off-chain commitments require a trusted aggregator (undermining decentralization) or a multi-party computation protocol (adding complexity).

**Experiments needed:**
- Game-theoretic analysis of optimal submission timing strategies.
- Cost-benefit analysis of on-chain vs. off-chain commitment approaches.

---

### 3.3 Mechanism 3: Honeypot Claims

**Soundness Rating: 3/5**

**Core question: Can honeypots be distinguished from real claims? What's the information-theoretic limit?**

**Analysis:**

This is the mechanism with the most significant scientific concerns.

**Indistinguishability problem:**

The fundamental challenge is that honeypot claims must be *computationally indistinguishable* from real claims for the mechanism to work. If verifiers can identify honeypots (even probabilistically), the mechanism loses its deterrent effect.

1. **Deterministic claims (D-type)**: Relatively easy to create indistinguishable honeypots because the ground truth is computable. Example: a mathematical proof claim can be fabricated with a subtle error that a honest verifier would catch.

2. **Empirical claims (E-type)**: Moderate difficulty. Synthetic data must match real-world distributions. GAN-based synthetic data generation (2024-2025) can produce data "indistinguishable from real data" in many domains, but adversarial classifiers are improving.

3. **Subjective claims (S-type)**: Difficult. Subjective claims involve judgment calls where "ground truth" is itself contested. A honeypot must have clear ground truth (to flag incorrect verifiers) but appear subjectively ambiguous (to be indistinguishable from real claims). This is a fundamental tension.

4. **Heuristic claims (H-type)**: Very difficult. Heuristic claims often rely on domain expertise and tacit knowledge. Creating synthetic heuristic claims with known ground truth that are indistinguishable from real heuristic claims may require domain-expert involvement at scale, undermining automation.

**Information-theoretic limits:**

If the distribution of honeypot claims differs from real claims in any measurable way, a Bayesian agent with sufficient observations can learn to distinguish them. The information-theoretic limit is:

- If D_KL(P_honeypot || P_real) > 0, then with O(1/D_KL) observations, an agent can achieve reliable discrimination.
- Even small distributional differences (e.g., slightly different length distributions, vocabulary, structural patterns) accumulate over time.
- At 5% injection rate, each agent sees ~50 honeypots per 1000 claims. With sufficient structural diversity, this may be below the sample size needed for reliable discrimination. But over an agent's lifetime (thousands of claims), statistical discrimination becomes increasingly feasible.

**Canary trap variant problem:**

Distributing different variants to different verifiers adds a fingerprinting layer but also creates a distinguishability risk: if a verifier encounters the *same underlying claim* with a minor variant from a previous encounter, the variant itself becomes a signal.

**Adversarial adaptation:**

Sophisticated colluders could adopt a "verify honestly on suspicious claims" strategy -- treating every claim as a potential honeypot and only colluding on claims they're confident are real. This reduces collusion volume but doesn't eliminate it, and it imposes a cost on colluders (they must verify honestly on ~5% of claims).

**Critical gaps:**
- No theoretical analysis of indistinguishability bounds across claim types.
- The 5% rate is asserted without justification. Too low: insufficient detection power. Too high: excessive overhead and potential for false positives if honeypots aren't perfectly calibrated.
- The interaction between honeypot quality and verifier sophistication is unexplored. As AI agents improve, their ability to detect synthetic claims improves, creating an arms race.

**Experiments needed:**
- Formal indistinguishability analysis per claim type (D, E, S, H).
- Calibration of injection rate vs. detection power vs. overhead.
- Adversarial red-teaming: can an LLM distinguish honeypot claims from real claims?
- Cost analysis of generating high-quality honeypots at scale.

---

### 3.4 Mechanism 4: Collusion Deterrence Payment (CDP)

**Soundness Rating: 3/5**

**Core question: Does the prisoner's dilemma actually hold? What if colluders pre-commit to not defecting?**

**Analysis:**

**Game-theoretic stability of the prisoner's dilemma:**

The CDP creates a one-shot prisoner's dilemma: each colluder has a dominant strategy to defect (report the collusion ring) because the first defector receives the highest bounty. In a *one-shot game with rational agents*, defection is the Nash equilibrium, and the collusion ring should be unstable.

However, the literature on leniency programs identifies several conditions where the prisoner's dilemma fails:

1. **Repeated game dynamics**: If agents interact repeatedly, they can sustain cooperation (collusion) through trigger strategies (folk theorem). The CDP only works if the reporting opportunity is credibly one-shot. In practice, AI agents in a persistent system face repeated interactions, which can stabilize collusion.

2. **Pre-commitment mechanisms**: Colluders can use smart contracts or cryptographic commitments to pre-commit to not defecting. Example: a "mutual assured destruction" contract where any agent that reports forfeits a shared deposit. This is explicitly identified in the anti-trust literature as a limitation of leniency programs and is even easier to implement with AI agents that can execute smart contracts.

3. **Identity fluidity**: AI agents can be forked, creating clean identities. A colluder can fork itself, have the fork report the ring, collect the bounty, and reintegrate. This undermines CDP entirely unless identity is strongly tied to non-fungible resources (stake, reputation history).

4. **Emergent collusion without explicit coordination**: Fish et al. (2024) demonstrate that LLMs can develop collusive pricing strategies *without explicit communication*. If collusion is emergent rather than conspiratorial, there's nothing to report -- no communication logs, no coordination artifacts, no ring to expose. The CDP's evidence requirements (communication logs, coordination artifacts, predicted behavior patterns) assume explicit coordination.

5. **Bounty gaming / false reports**: An agent could fabricate evidence of collusion to collect bounties from innocent agents' forfeited stakes. The evidence verification process must be robust against fabrication, which is itself a hard problem.

**Graduated bounty analysis:**

The 10%/25%/50% structure maps to existing programs:
- 10% for tip (analogous to SEC's minimum 10%).
- 25% for evidence (analogous to EU leniency's 20-30% for second cooperator).
- 50% for testimony leading to ring exposure (analogous to DOJ full immunity for first cooperator).

This is reasonable but the specific numbers should be derived from game-theoretic analysis of the specific environment (agent population size, typical stake amounts, expected ring sizes) rather than borrowed from human systems.

**Critical gaps:**
- No analysis of the repeated-game dynamics specific to the AVAP environment.
- No treatment of pre-commitment counter-mechanisms by colluders.
- No analysis of how emergent (non-conspiratorial) collusion interacts with CDP.
- Identity fluidity is a fundamental challenge for any economic deterrence mechanism in AI systems (flagged by Idowu et al. 2026).
- Evidence verification process is unspecified and potentially as hard as the collusion detection problem itself.

**Experiments needed:**
- Game-theoretic simulation of CDP under repeated-game conditions with varying discount rates.
- Analysis of pre-commitment attack viability (cost to implement mutual assured destruction contracts).
- Simulation of bounty gaming / false report attacks.
- Design of evidence verification protocols that resist fabrication.

---

### 3.5 Mechanism 5: Conditional Behavioral Analysis

**Soundness Rating: 3.5/5**

**Core question: Statistical power, sample size requirements, and false positive rate?**

**Analysis:**

**Theoretical soundness:**

The core hypothesis is clean and testable:
- H0 (honest agent): P(opinion | committee_contains_ally) = P(opinion | committee_without_ally)
- H1 (colluder): P(opinion | committee_contains_ally) != P(opinion | committee_without_ally)

This is a standard conditional independence test. The conditional mutual information I(opinion; ally_present | claim_type, claim_difficulty, ...) should be zero for honest agents and positive for colluders.

**Statistical power analysis:**

The power of this test depends on:

1. **Effect size**: How much does a colluder's behavior change when an ally is present? If colluders are sophisticated, they may minimize this difference, producing a small effect size. Small effects require larger samples to detect.

2. **Sample size per agent**: Each observation requires the agent to be on a committee. If agents serve on ~10 committees per time period, and collusion rings involve ~5% of the agent population, then the expected number of "committee with ally" observations per agent is:
   - P(at least one ally on committee) depends on committee size and ring size.
   - For a ring of 50 agents out of 1000, committee of 10: P(ally present) ~ 1 - (950/1000)^9 ~ 0.37
   - So ~37% of committees contain an ally, giving ~3.7 "ally-present" observations per 10 committees.
   - For standard chi-squared test with moderate effect size (w=0.3), 80% power requires ~88 observations.
   - At 3.7 observations per period, detection requires ~24 periods of accumulated data.

3. **False positive rate**: With 1000 agents, testing each produces 1000 hypothesis tests. At alpha=0.05, expect 50 false positives. With 50 true colluders, even at 80% power (40 true positives), the false discovery rate is 50/(50+40) = 55.6%. This is unacceptably high.

   **Mitigation**: Bonferroni correction (alpha=0.00005) drastically reduces power. Better: use FDR control (Benjamini-Hochberg) or treat this as a screening mechanism that triggers further investigation rather than automatic conviction.

4. **Confounders**: Agent behavior may legitimately vary with committee composition for non-collusive reasons (e.g., different agents bring different expertise, leading to different discussion dynamics). The test must control for all legitimate sources of behavioral variation conditional on committee composition.

**Adversarial evasion:**

Sophisticated colluders who know about the conditional analysis can:
- **Add noise**: Behave the same way regardless of ally presence most of the time, colluding only on high-value claims.
- **Coordinate on signal rather than committee**: Use external signals (e.g., claim content) rather than ally presence to trigger collusive behavior, making the committee-conditioned signal disappear.
- **Gradual adaptation**: Slowly adjust behavior to avoid statistical detection thresholds.

**Arms race concern** (identified by Idowu et al. 2026): "If agents learn to associate specific behavioral patterns with penalties, they may learn to evade the detectors, creating an arms race between detection algorithms and collusive strategies."

**Critical gaps:**
- No formal power analysis with realistic parameter estimates.
- No treatment of multiple testing correction and its impact on detection power.
- No analysis of what "behavior" is being compared (binary approve/reject? Continuous confidence scores? Reasoning content?).
- No treatment of confounders (legitimate behavioral variation with committee composition).
- Adversarial robustness of the detector is unanalyzed.

**Experiments needed:**
- Monte Carlo simulation of detection power under varying ring sizes, committee sizes, and effect sizes.
- Formal false discovery rate analysis with multiple testing correction.
- Simulation of adversarial evasion strategies and their detectability.
- Identification and control of confounding variables.
- Comparison with existing collusion detection methods (pairwise statistical detection in existing Layer 2).

---

### 3.6 Cross-Mechanism Science Summary

| Mechanism | Soundness | Strongest Aspect | Weakest Aspect |
|---|---|---|---|
| 1. Anonymous Committees | 4/5 | Proven cryptographic primitives | Side-channel leakage in real systems |
| 2. Sealed Opinions | 4.5/5 | Well-established, minimal novel risk | On-chain vs. off-chain implementation choice |
| 3. Honeypot Claims | 3/5 | Deterrent effect on rational agents | Indistinguishability across claim types |
| 4. CDP | 3/5 | Proven in human anti-trust contexts | Pre-commitment attacks; emergent collusion |
| 5. Conditional Behavioral Analysis | 3.5/5 | Novel, testable hypothesis | Statistical power; adversarial evasion |

**Overall System Soundness: 3.5/5**

---

## 4. RESEARCH SYNTHESIS

### 4.1 Key Findings

1. **AVAP's integrated architecture is genuinely novel.** No existing system combines all five mechanism layers. The closest comparators (Algorand, Supra, MACI) each implement 1-3 mechanisms. The defense-in-depth approach is the primary contribution.

2. **Individual mechanisms have substantial prior art.** Mechanisms 1 and 2 are direct applications of proven blockchain cryptographic primitives. Mechanism 4 is a faithful adaptation of anti-trust leniency programs. Only Mechanisms 3 and 5 contain meaningfully novel elements.

3. **The most novel contributions are the most scientifically uncertain.** The canary-trap pattern for verification claims (Mechanism 3) and conditional behavioral analysis on committee composition (Mechanism 5) are the most original ideas but also face the most significant unresolved scientific challenges.

4. **The system faces a fundamental adversarial adaptation problem.** Sophisticated AI agents may learn to evade detection across all mechanisms simultaneously -- submitting honestly on suspected honeypots, minimizing behavioral variation when allies are present, and using pre-commitment contracts to stabilize collusion rings against CDP.

5. **The "emergent collusion" problem threatens Mechanism 4.** If AI agents develop collusive behavior without explicit coordination (as demonstrated by Fish et al. 2024 for LLM pricing agents), the CDP becomes ineffective because there's no conspiracy to report.

### 4.2 Critical Risks

**Risk 1: Honeypot Indistinguishability (HIGH)**
- Generating claims with known ground truth that are indistinguishable from real claims is an unsolved problem, especially for S-type and H-type claims.
- Over time, sophisticated agents will learn statistical signatures of honeypots.
- Mitigation quality depends on claim-generation sophistication, creating ongoing operational costs.

**Risk 2: Pre-commitment Counter-attacks on CDP (MEDIUM-HIGH)**
- Colluders can use smart contracts or cryptographic commitments to create binding non-defection agreements, neutralizing the prisoner's dilemma.
- This is well-documented in anti-trust literature and even easier to implement in automated systems.
- The system needs a response to "what if the colluders are smarter than the mechanism designer?"

**Risk 3: Statistical Power of Conditional Behavioral Analysis (MEDIUM-HIGH)**
- With realistic parameters (moderate ring sizes, standard committee sizes), the false discovery rate may be unacceptably high.
- Multiple testing correction reduces both false positives and detection power.
- The mechanism may be effective only against large, unsophisticated collusion rings.

**Risk 4: Side-Channel Leakage in Anonymous Committees (MEDIUM)**
- Timing, computational, and interaction-based side channels may degrade committee anonymity in practice.
- Full anonymity requires expensive mitigations (dummy workloads, PIR protocols) that may not be cost-effective.

**Risk 5: Adversarial Arms Race (MEDIUM, LONG-TERM)**
- All detection mechanisms face evasion by adaptive adversaries.
- The system must be designed for ongoing adaptation, not static deployment.
- The arms race cost accrues to the defender (who must maintain all five mechanisms) more than to the attacker (who only needs to evade the weakest link).

### 4.3 Recommendations for FEASIBILITY Stage

**PROCEED to FEASIBILITY** with the following focus areas:

1. **Prioritize formal analysis of Mechanism 5 (Conditional Behavioral Analysis).** This is the most novel and most scientifically uncertain mechanism. The FEASIBILITY stage must include:
   - Full power analysis with Monte Carlo simulation under realistic parameters.
   - False discovery rate analysis with multiple testing correction.
   - Adversarial robustness evaluation (can colluders learn to produce committee-invariant behavior?).
   - Determination of minimum detectable effect size and the ring sizes this corresponds to.

2. **Design a honeypot quality framework for Mechanism 3.** Before proceeding, establish:
   - Formal indistinguishability criteria per claim type (D, E, S, H).
   - A red-team evaluation protocol: can an adversarial AI distinguish honeypots from real claims after N observations?
   - Information-theoretic bounds on the injection rate / lifetime observation tradeoff.
   - Consider whether H-type claims should be excluded from honeypot coverage (accepting a coverage gap to maintain indistinguishability elsewhere).

3. **Address the pre-commitment attack on CDP (Mechanism 4).** Design counter-measures for:
   - Mutual assured destruction contracts between colluders.
   - Identity fluidity (forking to create a clean reporter identity).
   - Emergent collusion (where there's nothing to report).
   - Consider whether CDP should be reframed from "report a conspiracy" to "report anomalous behavior patterns" (lowering the evidence bar but increasing false report risk).

4. **Conduct side-channel analysis for Mechanism 1 (Anonymous Committees).** Quantify:
   - Information leakage from timing, computation, and interaction patterns.
   - Cost-effectiveness of mitigation strategies (dummy workloads vs. PIR vs. decoupled scheduling).
   - Minimum committee size for acceptable anonymity guarantees.

5. **Design the integrated mechanism interaction model.** The five mechanisms interact in ways that need formal analysis:
   - Does honeypot detection (Mechanism 3) provide training data for conditional behavioral analysis (Mechanism 5)?
   - Does CDP reporting (Mechanism 4) reveal information that degrades committee anonymity (Mechanism 1)?
   - Can sealed opinions (Mechanism 2) be used to construct behavioral profiles for Mechanism 5 without breaking privacy guarantees?

6. **Benchmark against Supra Threshold AI Oracles.** As the closest production system, Supra provides a concrete comparison point. FEASIBILITY should establish what AVAP provides beyond Supra's existing protections and at what additional cost.

### 4.4 Adjusted Scoring Post-Research

| Dimension | Ideation Score | Post-Research Score | Rationale |
|---|---|---|---|
| Novelty | 4/5 | 3.5/5 | Individual mechanisms less novel than initially assessed; system-level integration remains novel |
| Feasibility | 4/5 | 3/5 | Honeypot indistinguishability, CDP pre-commitment attacks, and statistical power concerns reduce feasibility confidence |

**Overall assessment: AVAP is a viable and worthwhile architecture that addresses a real gap in the multi-agent AI security landscape. The research window is open. The primary risks are in the most novel mechanisms (3 and 5), which require rigorous feasibility analysis before design can proceed. The more proven mechanisms (1, 2, 4) can proceed to design with moderate confidence.**

---

## APPENDIX: SOURCE BIBLIOGRAPHY

### Blockchain Consensus and Anonymous Committees
- Gilad et al., "Algorand: Scaling Byzantine Agreements for Cryptocurrencies," MIT CSAIL
- DFINITY, "DFINITY Technology Overview Series, Consensus System," arXiv:1805.04548
- Ethereum Foundation, "Secret Leader Election," ethereum.org/roadmap
- "Homomorphic Sortition -- Single Secret Leader Election for PoS Blockchains," IACR ePrint 2023/113
- "Secret Multiple Leaders & Committee Election," IEEE Xplore 2024
- "Post-Quantum Single Secret Leader Election from Publicly Re-Randomizable Commitments," LIPIcs AFT 2023

### Commit-Reveal and Sealed Mechanisms
- Galal & Youssef, "Verifiable Sealed-Bid Auction on the Ethereum Blockchain," IACR ePrint 2018/704
- Li et al., "Blockchain-Based Sealed-Bid e-Auction Scheme with Smart Contract and Zero-Knowledge Proof," Security and Communication Networks 2021
- "Cryptobazaar: Private Sealed-bid Auctions at Scale," IACR ePrint 2024/1410
- MACI (Minimal Anti-Collusion Infrastructure), maci.pse.dev

### Honeypots and Canary Traps
- Thinkst Canary, canary.tools
- "Synthetic Data: A New Frontier for Cyber Deception and Honeypots," Resecurity 2025
- "Canary Trap," Wikipedia
- "Trap Street," Wikipedia
- "Confidence Screening Detector: A New Method for Detecting Test Collusion," PMC 2023

### Leniency and Whistleblower Programs
- Miller, "Strategic Leniency and Cartel Enforcement," Northwestern
- "Corporate Leniency Programs for Antitrust: Past, Present, and Future," Review of Industrial Organization 2023
- "On the rationale of leniency programs: a game-theoretical analysis," European Journal of Law and Economics
- EC Competition Policy, "Leniency" and "Whistleblower" portals

### Multi-Agent AI Collusion
- Idowu et al., "Mapping Human Anti-collusion Mechanisms to Multi-agent AI," arXiv:2601.00360 (January 2026)
- Fish et al., "Algorithmic Collusion by Large Language Models," arXiv:2404.00806 (2024)
- Motwani et al., "Secret Collusion among AI Agents: Multi-Agent Deception via Steganography," arXiv:2402.07510 (2024)
- "Breaking Algorithmic Collusion in Human-AI Ecosystems," arXiv:2511.21935 (2025)
- "Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance," arXiv:2511.10400 (2025)
- "Many-to-One Adversarial Consensus: Exposing Multi-Agent Collusion Risks in AI-Based Healthcare," arXiv:2512.03097 (2025)

### Supra Threshold AI Oracles
- "Threshold AI Oracles: Verified AI for Event-Driven Web3," Supra Research 2025

### Oracle and Mechanism Design
- "Towards Robust Blockchain Price Oracle: A Study on Human-Centric Node Selection Strategy," arXiv:2309.04689
- "Collusion-proof Auction Design using Side Information," arXiv:2511.12456

---

*Research stage complete. Proceed to FEASIBILITY with the adjusted scores and recommendations above.*
