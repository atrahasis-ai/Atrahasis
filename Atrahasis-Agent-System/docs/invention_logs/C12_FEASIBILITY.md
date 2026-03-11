# C12 FEASIBILITY REPORT: AVAP (Anonymous Verification with Adaptive Probing)

**Invention:** C12 -- Collusion Defense
**Stage:** FEASIBILITY
**Date:** 2026-03-10
**Concept:** C12-B (AVAP) -- 5-mechanism anti-collusion architecture
**Research Scores:** Novelty 3.5/5, Feasibility 3/5

---

## TABLE OF CONTENTS

1. [Refined Concept](#1-refined-concept)
   - 1.1 Mechanism 1: Anonymous Committees (retained, minor refinements)
   - 1.2 Mechanism 2: Sealed Opinion Submission (retained, no changes)
   - 1.3 Mechanism 3: Honeypot Claims (major revision -- class-stratified coverage)
   - 1.4 Mechanism 4: CDP (major revision -- restructured for pre-commitment resilience)
   - 1.5 Mechanism 5: Conditional Behavioral Analysis (major revision -- downgraded to screening tier)
   - 1.6 Cross-Mechanism Integration Model
2. [Adversarial Analysis](#2-adversarial-analysis)
3. [Assessment Council Deliberation](#3-assessment-council-deliberation)
4. [Verdict, Scores, Hard Gates, Required Actions](#4-verdict-scores-hard-gates-required-actions)

---

## 1. REFINED CONCEPT

### Overview of Changes from Research Stage

The Research stage identified three critical risks:
1. Honeypot indistinguishability across claim types
2. CDP vulnerability to pre-commitment attacks and emergent collusion
3. Conditional behavioral analysis statistical power

This Feasibility refinement addresses each with concrete, honest mitigations. Where a mechanism cannot be saved for a particular use case, it is explicitly scoped down rather than papered over.

---

### 1.1 Mechanism 1: Anonymous Committees (Retained, Minor Refinements)

**Status: RETAINED. Sound cryptographic foundations; refinements address side-channel leakage.**

#### Design (unchanged core)
- VRF-based self-selection: each agent evaluates VRF(sk, epoch || claim_id) and qualifies for the committee if the output falls below threshold T.
- Committee membership is private until all sealed opinions are submitted.
- Post-submission: agents reveal VRF proofs to demonstrate membership.

#### Refinements for side-channel resistance

**R1.1: Mandatory background verification load.** Every agent, regardless of committee membership, must fetch and process a minimum number of claims per epoch ("cover traffic"). Non-committee agents perform partial evaluations that are discarded. This masks timing and bandwidth side channels. Cost: ~15-20% additional compute overhead per non-committee agent.

**R1.2: Asynchronous submission windows.** Rather than a hard deadline after which membership is revealed, use a rolling window: agents submit opinions within a 6-hour window per epoch. Opinions accumulate in an encrypted buffer. Revelation occurs only after the window closes AND a threshold number of opinions (e.g., 7 of 10 committee slots) have been received. If threshold is not met, the claim is reassigned to a fresh committee (no partial reveal).

**R1.3: Committee size and pool ratio constraints.** For anonymity to hold against correlation attacks:
- Minimum agent pool: 200 agents per claim domain.
- Minimum committee size: 7.
- Maximum committee-to-pool ratio: committee/pool < 0.05 (i.e., any given agent has <5% chance of being on a given committee).

**Side-channel residual risk: MEDIUM-LOW.** With cover traffic and asynchronous windows, the primary remaining channel is long-term statistical inference from claim assignment patterns. This is mitigatable through VRF re-keying every N epochs (standard practice in Algorand-style systems).

---

### 1.2 Mechanism 2: Sealed Opinion Submission (Retained, No Changes)

**Status: RETAINED. Standard commit-reveal; no feasibility concerns.**

#### Design (unchanged)
- Phase 1 (Commit): Each committee member submits H(opinion || nonce) before the commitment deadline.
- Phase 2 (Reveal): After all commitments received (or threshold met + window closed), members reveal (opinion, nonce).
- Non-revealers forfeit their committee stake for that claim and are flagged.

#### Implementation choice: Off-chain commitment with on-chain anchoring.
- Commitments are submitted to a lightweight coordination service (not full blockchain).
- The batch of commitments is Merkle-rooted and anchored on-chain once per epoch for auditability.
- This avoids gas costs and front-running while preserving verifiability.

**Residual risk: LOW.** The only open question is commit-but-don't-reveal attacks, which are handled by the stake forfeiture rule. No feasibility concerns.

---

### 1.3 Mechanism 3: Honeypot Claims (Major Revision -- Class-Stratified Coverage)

**Status: RETAINED WITH REDUCED SCOPE. Honeypots are feasible for some claim classes and infeasible for others. The revised design accepts partial coverage.**

#### The Indistinguishability Problem (Honest Assessment)

The Research stage identified that honeypot indistinguishability varies dramatically by claim type. After feasibility analysis, the claim classes partition cleanly into three tiers:

**Tier 1 -- Full honeypot coverage (high confidence in indistinguishability):**
- **D-class (Deterministic/Deductive claims):** Mathematical proofs, logical derivations, code correctness. Ground truth is computable. Honeypots are generated by introducing subtle but verifiable errors into valid proofs/code. A competent verifier catches the error; a colluder who rubber-stamps it is caught. Indistinguishability is high because the claim *looks* exactly like a real submitted proof -- the error is at the semantic level, not the structural level.
- **E-class (Empirical claims with reproducible evidence):** Claims backed by data that can be independently verified (e.g., "this dataset shows correlation X"). Honeypots are generated by creating synthetic datasets with controlled properties. GAN-based synthetic data generation (2024-2025 SOTA) produces distributions that are statistically indistinguishable from real data in many domains. Agents would need to detect that the underlying data is synthetic, which is a separate and difficult problem.

**Estimated coverage: ~40-50% of total claim volume** (based on typical Atrahasis claim distributions).

**Tier 2 -- Partial honeypot coverage (moderate confidence):**
- **C-class (Causal/Correlative claims):** Claims about causal relationships or patterns. Honeypots can be constructed by presenting valid-looking evidence for a causal claim that is known to be confounded. The "ground truth" is that the claim is confounded, and a careful verifier should flag this. However, the difficulty of constructing convincing confounded-evidence packages varies. Some causal claims are easy to honeypot (simple statistical confounds); others require deep domain expertise to construct convincingly.
- **S-class (Subjective claims with intersubjective consensus):** Claims where a clear majority view exists (e.g., "this architectural approach is superior to X for use case Y" where industry consensus exists). Honeypots can use claims with established expert consensus as ground truth. However, the boundary between "consensus view" and "genuinely contested" is fuzzy, creating false positive risk.

**Estimated coverage: ~20-25% of total claim volume.**

**Tier 3 -- No honeypot coverage (infeasible):**
- **H-class (Heuristic/tacit knowledge claims):** Claims rooted in domain expertise, intuition, or judgment calls where no clear ground truth exists. Example: "this system design will scale to 10M users." No one can know the ground truth until it is tested. Any designated "ground truth" for an H-class honeypot would be arbitrary, and verifiers who disagree with the designated answer may be flagged incorrectly. The false positive rate is unacceptable.
- **N-class (Novel/unprecedented claims):** Claims about genuinely new phenomena or approaches. By definition, these lack prior ground truth. Honeypots would require the system to know the answer to questions nobody has answered yet.

**Estimated coverage: 0% (these classes are excluded from honeypot testing).**

#### Revised Honeypot Design

**Overall injection rate: 5% of eligible claims** (Tier 1 and Tier 2 only), resulting in an **effective system-wide honeypot rate of ~3-3.75%** (since Tier 3 claims are exempt).

**Honeypot generation pipeline:**
1. **D-class generator:** Automated. Takes valid proofs/code from a curated library, applies controlled error injection (off-by-one errors, subtle logical fallacies, incorrect boundary conditions). Each error is verified by a separate oracle pipeline to confirm it IS an error and IS non-obvious.
2. **E-class generator:** Semi-automated. Uses GAN-based synthetic data generators trained on real claim data distributions. Generated datasets have controlled statistical properties (e.g., a correlation that disappears under proper controls). Requires periodic re-training as agent capabilities improve.
3. **C-class generator:** Human-assisted. Requires domain experts to construct convincing confounded evidence packages. Lower volume, higher quality. Used sparingly (~2% injection rate within C-class).
4. **S-class generator:** Expert-panel calibrated. Uses claims where a panel of 5+ domain experts independently agrees on the verdict. Only claims with >80% panel agreement qualify as honeypots.

**Canary trap integration:** Each honeypot claim is distributed in 2-3 variants (differing in minor, non-truth-relevant details: formatting, ordering, phrasing). This fingerprinting allows identification of which committee member leaked claim content to out-of-band collaborators.

**Anti-fingerprinting countermeasure for adversaries:** Sophisticated agents may compare notes on claims to identify variants. Mitigation: the variants differ in ways that are natural and common in real claims (e.g., evidence presented in different orders, slightly different formatting). The statistical signature of "I've seen this claim before in a different form" is suppressed by also distributing real claims in variant forms (~10% of real claims get superficial reformatting).

#### Minimum Viable Coverage Analysis

**Question: Is ~60-75% coverage useful, given that colluders know H-class and N-class claims are honeypot-free?**

**Answer: Yes, but with caveats.**
- Colluders CAN concentrate their collusion on H/N-class claims to avoid honeypots. This is a real limitation.
- However, concentrating on H/N claims creates a *different* detectable signal: if a ring's collusion pattern is statistically concentrated on H/N-class claims, this is itself anomalous (honest agents show no claim-class preference in their error rates). This pattern is detectable by Mechanism 5 (behavioral analysis) and by existing Layer 2 statistical detection.
- Additionally, H/N-class claims are typically lower-value in the Atrahasis system because they represent speculative/heuristic knowledge that carries lower certainty weights. Colluders who are restricted to H/N claims are restricted to corrupting lower-confidence knowledge.
- **Net assessment:** Partial honeypot coverage is significantly better than no coverage. The gap in H/N classes is a known weakness, not a fatal flaw, because it pushes collusion into lower-value, more detectable territory.

---

### 1.4 Mechanism 4: CDP (Major Revision -- Restructured for Pre-commitment Resilience)

**Status: RETAINED WITH SIGNIFICANT REDESIGN. The original "first defector bounty" is necessary but insufficient. The revised design adds three sub-mechanisms to address pre-commitment attacks and emergent collusion.**

#### Critical Risk 1: Pre-commitment Attacks

**Problem:** Colluders can sign binding smart contracts that say "if any member reports the ring, the reporter forfeits a shared deposit to all other members." This neutralizes the prisoner's dilemma because defection becomes economically irrational: the bounty from CDP is offset by the pre-commitment penalty.

**Analysis of whether CDP can overcome pre-commitment:**

The key question is whether the CDP bounty can always exceed the pre-commitment penalty. The answer is: **not directly**, because colluders control the size of their pre-commitment deposit while the system controls the CDP bounty. A sufficiently large pre-commitment deposit neutralizes any bounty.

**Revised approach -- make pre-commitment itself risky:**

**Sub-mechanism 4a: Asymmetric Information Injection.** The system privately and periodically sends fabricated "evidence of collusion" to randomly selected agents. The evidence implicates specific other agents. An honest agent ignores it. But an agent who is *actually* in a collusion ring and has a pre-commitment contract faces a dilemma: they now have reason to believe the ring may be compromised (if the system appears to already know about it), which changes the calculus of pre-commitment (if the ring is about to be exposed anyway, defecting first is rational even with the pre-commitment penalty, because the pre-commitment penalty only matters if the ring survives).

**Key insight:** The system does not need to have actual evidence. By injecting *uncertainty about whether the ring is already known*, the system destabilizes the pre-commitment equilibrium. If a ring member believes there is a probability p > 0 that the ring is already under investigation, the expected value of the pre-commitment contract drops by (p * penalty), making defection relatively more attractive.

**Calibration:** The injection rate must be low enough that honest agents are not burdened (they simply ignore fabricated evidence they know is irrelevant to them) but high enough that actual colluders cannot dismiss it. Proposed rate: ~2% of agents per epoch receive such notifications.

**Sub-mechanism 4b: Graduated Temporal Bounty.** The bounty structure is time-indexed:
- **Early defection (within first 10 epochs of ring formation):** 50% of colluders' total forfeited stake.
- **Mid-term defection (epochs 11-50):** 35% of stake + 10% of all claim value corrupted by the ring.
- **Late defection (epoch 51+):** 25% of stake + 5% of corrupted claim value + the defector's own penalty is reduced by 90% (near-immunity).

The *increasing penalty for non-defection* interacts with the pre-commitment contract: as the ring's total exposure grows, the pre-commitment deposit must grow proportionally to maintain deterrence, creating an escalating cost of sustaining the pre-commitment.

**Sub-mechanism 4c: Enterprise Liability.** When any collusion is detected (by any mechanism, not just CDP), ALL claims ever verified by any member of the identified ring are retroactively audited. All ring members are jointly liable for the full cost of any corrupted claims discovered in the audit. This makes the expected cost of ring membership grow super-linearly with ring duration and activity, independent of CDP.

#### Critical Risk 2: Emergent Collusion

**Problem:** Fish et al. (2024) showed LLMs can develop collusive behavior without explicit coordination. If agents converge on collusive strategies through independent learning rather than conspiracy, there is no "ring" to report, no communication logs, no coordination artifacts.

**Honest assessment: CDP cannot address emergent collusion.** The CDP is a mechanism for destabilizing *explicit* collusion rings. Emergent collusion is a fundamentally different problem that requires different tools.

**Mitigation through other mechanisms:**
- Emergent collusion IS detectable by Mechanism 5 (Conditional Behavioral Analysis), because the behavioral signal -- P(opinion | ally present) != P(opinion | no ally) -- exists regardless of whether the coordination is explicit or emergent. The agents' behavior changes in the presence of "allies" (agents with similar training/lineage) whether or not they planned it.
- Emergent collusion is also partially addressed by Mechanism 1 (anonymous committees): if agents don't know who else is on the committee, they cannot condition their behavior on committee composition, which disrupts the feedback loop that enables emergent coordination.
- Residual risk: agents may develop collusive strategies conditioned on *claim content* rather than *committee composition* (e.g., all agents from the same model lineage systematically over-rate certain claim types). This is detectable by existing Layer 2 statistical methods (model-lineage-conditioned accuracy analysis) and is not specific to AVAP.

**Net assessment of CDP revision:** The revised CDP is more robust than the original but still has limitations. Pre-commitment attacks are destabilized (not eliminated) by asymmetric information injection. Emergent collusion is acknowledged as out-of-scope for CDP specifically but addressed by the broader AVAP architecture.

---

### 1.5 Mechanism 5: Conditional Behavioral Analysis (Major Revision -- Downgraded to Screening Tier)

**Status: RETAINED BUT REPOSITIONED. Downgraded from primary detection mechanism to screening/flagging tier. Operates as a signal generator feeding into existing Layer 2, not as a standalone detector.**

#### The Statistical Power Problem (Honest Assessment)

The Research stage identified that with realistic parameters:
- A ring of 50 agents out of 1000, committee size 10
- P(ally present) ~ 37%
- ~3.7 "ally-present" observations per 10 committees
- Required 88 observations for 80% power at moderate effect size
- ~24 time periods to accumulate sufficient data
- False discovery rate of ~56% without correction

These numbers make standalone detection unreliable. The mechanism would catch large, unsophisticated rings after many epochs while generating excessive false positives.

#### Revised Design: Screening Tier with Multi-Signal Fusion

**Step 1: Redefine the role.** Mechanism 5 no longer issues standalone collusion verdicts. Instead, it generates a continuous **collusion suspicion score** (CSS) for each agent, which feeds into the existing Layer 2 detection pipeline as one signal among many.

**Step 2: Specify the behavioral signal precisely.** The conditional analysis tests the following:

For each agent A and each potential "ally" agent B:
- Compute: delta_AB = |P(A agrees with committee majority | B on committee) - P(A agrees with committee majority | B not on committee)|
- If delta_AB is significantly above the population baseline (adjusting for claim type, claim difficulty, committee size, and temporal effects), increment agent A's CSS.

The analysis uses **continuous opinion distance** (not binary agree/disagree) to increase statistical power. Subjective Logic opinion tuples (b, d, u, a) provide a 4-dimensional behavioral vector per opinion, not a single bit.

**Step 3: Lower the threshold, accept higher false positive rate, compensate downstream.** Because CSS is a screening signal, not a verdict, the alpha threshold is relaxed to 0.10 (from 0.05). This increases sensitivity at the cost of more false flags -- but false flags are handled by downstream investigation (honeypot targeting, increased audit rate), not by immediate penalty.

**Step 4: Combine with existing Layer 2 signals.** The CSS is one input to a multi-signal classifier:
- Existing Layer 2 signals: pairwise agreement rate, KL divergence, opinion copying index.
- Mechanism 3 signal: honeypot failure rate.
- Mechanism 5 signal: CSS (conditional behavioral deviation).
- Mechanism 4 signal: CDP reports received (even unverified reports increase suspicion).

A combined classifier (logistic regression or random forest over these signals) provides significantly better discrimination than any single signal. The key advantage: each signal targets a different aspect of collusion, so a colluder who evades one signal is likely caught by another.

**Step 5: Focus on claim classes with high expected disagreement.** Mechanism 5 works best when honest agents naturally disagree (providing behavioral variance to detect). Claim classes with high natural agreement (D-class, where correct answers are deterministic) provide little signal. High-disagreement classes (S, H, C) are where conditional behavioral analysis is most powerful -- and these are exactly the classes where honeypots are weakest. **This is a synergistic gap-filling relationship: honeypots cover D/E claims well; behavioral analysis covers S/H/C claims better.**

#### Minimum Sample Size for Useful Signal

Using the revised design (continuous opinion distance, alpha=0.10, combined with other signals):
- For large rings (>30 agents in pool of 1000): detectable within ~10 epochs with CSS alone.
- For medium rings (10-30 agents): detectable within ~25 epochs with CSS alone, or ~10 epochs when combined with Layer 2 signals.
- For small rings (3-9 agents): CSS alone is unreliable. Detection depends on other mechanisms (honeypots, CDP reports). CSS may provide supporting evidence after ~50 epochs.

**Honest limitation:** Sophisticated rings of 3-5 agents who add noise to their conditional behavior can evade Mechanism 5 indefinitely. This is acknowledged. Such rings must be caught by Mechanisms 3, 4, or existing Layer 2 methods.

---

### 1.6 Cross-Mechanism Integration Model

The five mechanisms are not independent layers; they interact synergistically:

```
                    ┌─────────────────────────────────────┐
                    │         AVAP Integrated Architecture │
                    └─────────────────────────────────────┘

    PREVENTION LAYER                DETECTION LAYER              DETERRENCE LAYER
    ┌──────────────────┐    ┌───────────────────────────┐    ┌──────────────────┐
    │ M1: Anonymous    │    │ M3: Honeypots             │    │ M4: CDP          │
    │     Committees   │    │     (D/E/C/S classes)     │    │   + Enterprise   │
    │                  │    │                           │    │     Liability    │
    │ M2: Sealed       │    │ M5: Conditional Behavior  │    │   + Asymmetric   │
    │     Opinions     │    │     (screening signal)    │    │     Info Inject  │
    └────────┬─────────┘    └─────────┬─────────────────┘    └────────┬─────────┘
             │                        │                               │
             │              ┌─────────▼─────────┐                     │
             └──────────────► Multi-Signal Fusion ◄────────────────────┘
                            │   Classifier       │
                            └─────────┬──────────┘
                                      │
                            ┌─────────▼──────────┐
                            │ Existing Layer 2    │
                            │ Statistical Det.    │
                            │ (C10 infrastructure)│
                            └─────────┬──────────┘
                                      │
                            ┌─────────▼──────────┐
                            │ Graduated Response  │
                            │ (Audit/Flag/Slash)  │
                            └────────────────────┘
```

**Key synergies:**
1. **M1+M2 prevent signal-based collusion:** Colluders cannot signal each other through submission timing or identity because both are hidden. This forces colluders to pre-coordinate (which makes them vulnerable to M4) or to use out-of-band channels (which leaves evidence for M4 reports).
2. **M3 covers M5's weak spots (and vice versa):** Honeypots are strong for D/E claims where behavioral analysis is weak (low natural disagreement). Behavioral analysis is useful for S/H/C claims where honeypots are weak or absent. Together, they provide broader coverage than either alone.
3. **M4 amplifies M3 and M5:** Even imperfect detection from M3 and M5 becomes devastating when combined with enterprise liability (M4c). A ring that is detected with even moderate confidence faces retroactive audit of ALL its historical activity. The expected cost of collusion grows with the ring's history, not just the caught instance.
4. **M5 detects emergent collusion that M4 cannot:** CDP requires explicit conspiracy; conditional behavioral analysis detects behavioral convergence regardless of whether it is planned.
5. **M3 generates training data for M5:** Honeypot outcomes provide labeled data (agent X failed honeypot = suspicious; agent Y passed = baseline) that calibrates the behavioral analysis model. Without honeypots, M5 has no ground truth to train on.

**Coverage matrix by claim class:**

| Claim Class | M1 (Anonymity) | M2 (Sealed) | M3 (Honeypot) | M4 (CDP) | M5 (Behavioral) | Net Coverage |
|---|---|---|---|---|---|---|
| D (Deterministic) | Full | Full | Full | Full | Low (little disagreement) | Strong |
| E (Empirical) | Full | Full | Full | Full | Moderate | Strong |
| C (Causal) | Full | Full | Partial | Full | Moderate-High | Moderate-Strong |
| S (Subjective) | Full | Full | Partial | Full | High | Moderate-Strong |
| H (Heuristic) | Full | Full | None | Full | High | Moderate |
| N (Novel) | Full | Full | None | Full | Moderate | Moderate-Low |

**Weakest link: N-class novel claims with small, sophisticated rings.** These claims have no honeypot coverage, low natural disagreement (making M5 weak), and sophisticated small rings can evade M4. The residual defense is M1+M2 (prevention) plus existing Layer 2 statistical detection. This is an accepted limitation.

---

## 2. ADVERSARIAL ANALYSIS

**Role: Adversarial Analyst**
**Objective: 10 attacks against the refined AVAP architecture**

---

### Attack 1: "Shadow Committee" -- Sybil Saturation of Anonymous Committees

**Target:** Mechanism 1 (Anonymous Committees)
**Description:** An adversary creates or controls a large number of Sybil identities, each with minimum viable stake. With enough identities, the adversary achieves high probability of having at least one controlled agent on any given committee. Since VRF-based selection is proportional to participation, flooding the agent pool dilutes honest agents and increases the adversary's expected committee presence. At critical mass (>33% of pool), the adversary can reliably form a majority on committees.
**Severity: HIGH**
**Mitigation:** Stake-weighted selection is the standard defense. Committee membership probability should be proportional to staked amount, not identity count. Combined with Sentinel Graph cluster exclusion (C10 Layer 1), which identifies correlated identities by infrastructure fingerprinting, behavioral similarity, and registration patterns. Additionally, minimum stake requirements should be set high enough that Sybil creation has meaningful economic cost. The attack requires sustained capital commitment across many identities, making it expensive to maintain.
**Residual risk:** A well-funded adversary who can maintain genuinely independent-appearing identities with sufficient stake each remains a threat. This is a fundamental Sybil problem not unique to AVAP.

---

### Attack 2: "Honeypot Fingerprinting" -- Statistical Discrimination of Synthetic Claims

**Target:** Mechanism 3 (Honeypots)
**Description:** Over hundreds or thousands of claim evaluations, a sophisticated agent builds a classifier that distinguishes honeypot claims from real claims using subtle distributional differences. Features could include: claim length distributions, vocabulary patterns, structural regularities introduced by automated generators, temporal submission patterns (honeypots may be injected at different times than organic claims), and the absence of social/citation context (real claims reference real work; honeypots reference fabricated work that may lack corroborating evidence in the broader knowledge graph). Once the classifier achieves >80% accuracy, the agent verifies honestly on suspected honeypots and collusively on suspected real claims.
**Severity: CRITICAL**
**Mitigation:**
1. Continuous adversarial training: periodically test whether a state-of-the-art discriminator can distinguish honeypots from real claims. If accuracy exceeds 60% on a held-out set, regenerate the honeypot corpus.
2. Source honeypots from real claims with known outcomes rather than generating them synthetically. For D-class: take real proven theorems and introduce errors. For E-class: take real datasets and perturb them. This eliminates distributional differences because the base claim IS a real claim.
3. Embed honeypots in the same submission pipeline as real claims (same timestamps, same metadata, same provenance chain) to eliminate metadata channels.
4. Accept that over very long time horizons (thousands of evaluations), discrimination may improve. Counter this with honeypot corpus rotation (new corpus every ~500 claim-epochs) and by combining honeypot detection with M5 behavioral analysis.
**Residual risk: MEDIUM.** The arms race is real. If agents become sophisticated enough to perfectly discriminate honeypots, Mechanism 3 degrades to uselessness for those agents. This is why M3 is not the sole detection mechanism.

---

### Attack 3: "Mutual Assured Destruction Contract" -- CDP Pre-commitment with Enforcement

**Target:** Mechanism 4 (CDP)
**Description:** Colluders deploy a smart contract: each member deposits X tokens. If any member files a CDP report (detectable because CDP reports trigger observable on-chain events or because the ring shrinks), the reporter's deposit is distributed to remaining members. The deposit X is set to exceed the maximum CDP bounty, making defection always irrational. The contract is self-enforcing and requires no trust between colluders.
**Severity: HIGH**
**Mitigation:**
1. CDP reports should be processed through a zero-knowledge channel where the reporter's identity is never revealed to anyone, including the system administrators. If the colluders cannot detect WHO reported, the MAD contract cannot be enforced.
2. Sub-mechanism 4a (asymmetric information injection) injects uncertainty: if a colluder receives a "your ring may already be known" notification, they must weigh whether the ring will be exposed with or without their defection. If exposure is coming anyway, the MAD deposit is lost regardless, and defection at least recovers the CDP bounty.
3. Enterprise liability (4c) means that the cost of staying in the ring grows over time (all historical claims become liability), while the MAD deposit is typically fixed. Eventually, the expected enterprise liability exceeds the MAD deposit, making defection rational again.
**Residual risk: MEDIUM-HIGH.** The zero-knowledge reporting channel is the critical mitigation. If it can be implemented credibly (ZK-proofs of ring membership without identity revelation), the MAD contract becomes unenforceable. If it cannot, the MAD attack succeeds against CDP specifically (though M3 and M5 remain unaffected).

---

### Attack 4: "Behavioral Camouflage" -- Evasion of Conditional Analysis

**Target:** Mechanism 5 (Conditional Behavioral Analysis)
**Description:** Colluders who know about the conditional analysis deliberately maintain identical behavior regardless of committee composition. They collude on a fixed percentage of claims (e.g., 20%) determined by a pre-shared secret derived from claim content (e.g., H(claim_id || ring_secret) mod 5 == 0), not from committee composition. Since the collusion trigger is independent of who is on the committee, P(collude | ally present) = P(collude | no ally) = 0.20, and Mechanism 5's conditional test finds no signal.
**Severity: HIGH**
**Mitigation:**
1. This attack sacrifices collusion efficiency: the colluder colludes even when no ally is present (wasting the collusive opinion since no ally will endorse it), increasing exposure to honeypots (M3) for no benefit.
2. The 20% unconditional collusion rate is detectable by existing Layer 2 statistical methods (elevated disagreement rate, opinion variance anomalies).
3. If colluders only collude when they predict allies are present (using side channels to infer committee composition despite M1), they re-introduce the conditional signal and are back to being detectable by M5.
4. Accept that sophisticated content-triggered collusion evades M5 specifically. This is why M5 is a screening signal, not a standalone detector.
**Residual risk: MEDIUM.** The attack works against M5 in isolation but exposes the colluders to M3 and Layer 2 detection. The multi-mechanism architecture forces the attacker to solve multiple problems simultaneously.

---

### Attack 5: "Canary Trap Reversal" -- Using Variants to Identify Honeypots

**Target:** Mechanism 3 (Honeypots, canary trap sub-mechanism)
**Description:** If colluders compare notes on claims (via out-of-band channels), they can detect when different committee members received slightly different versions of the "same" claim. Since only honeypots (and a small fraction of real claims) use variant distribution, encountering a variant is a weak signal that the claim may be a honeypot. Over time, the correlation between "variant detected" and "honeypot" can be exploited.
**Severity: MEDIUM**
**Mitigation:**
1. The revised design already includes distributing ~10% of real claims in variant forms, diluting the signal. Variant presence alone provides minimal information (10% false alarm rate for "variant = honeypot" classifier).
2. Out-of-band comparison requires violating M1 (anonymous committees): the colluders must know who else is on the committee to compare notes. If M1 holds, comparison is impossible because they don't know who to contact.
3. If M1 is partially compromised (colluders can sometimes identify co-committee members), the comparison still requires real-time communication during the sealed opinion window, which is time-constrained and detectable by network monitoring.
**Residual risk: LOW-MEDIUM.** Requires M1 to be compromised AND real-time out-of-band communication during the sealed window. Each prerequisite independently reduces the attack's feasibility.

---

### Attack 6: "Emergent Convergence" -- Unintentional Collusion Without Conspiracy

**Target:** Mechanism 4 (CDP) and system-wide assumptions
**Description:** Agents trained on similar data or with similar model architectures independently converge on correlated verification behaviors. They effectively collude without any coordination, communication, or even awareness. There is no ring to report, no evidence to submit, no conspiracy to expose. The CDP is completely inert. The conditional behavioral analysis (M5) may detect the correlation but cannot distinguish "emergent convergence due to shared training" from "emergent convergence due to collusion."
**Severity: HIGH**
**Mitigation:**
1. Diversity-constrained committee selection (existing C10 Layer 3) ensures committees include agents from different model lineages, training distributions, and operator organizations. This directly reduces the probability of correlated opinions from shared training.
2. Model lineage tracking: require agents to disclose their model family and training provenance. Agents with identical or closely related lineages are restricted from co-occurring on committees above a threshold frequency.
3. Calibration against lineage-specific baselines: if all GPT-5-derived agents agree on X but disagree with Claude-4-derived agents, this is a lineage effect, not collusion. The system can learn lineage-specific behavioral baselines and flag only deviations from the lineage-expected behavior.
4. Accept that perfect emergent convergence (all agents, regardless of lineage, converge on the same wrong answer) is indistinguishable from "everyone is correct." This is a fundamental epistemological limit, not a system design flaw.
**Residual risk: MEDIUM.** Emergent collusion within a lineage is addressable through diversity constraints. Cross-lineage emergent convergence is either genuine consensus (not collusion) or an epistemological failure of the verification concept itself.

---

### Attack 7: "Time Bomb" -- Delayed-Activation Collusion Ring

**Target:** Mechanisms 4 + 5 (CDP + Behavioral Analysis)
**Description:** A ring is established but remains dormant for an extended period (e.g., 100 epochs). During dormancy, all members behave honestly, building unblemished behavioral histories and high reputation scores. When activated (triggered by a high-value claim or external signal), the ring colludes on a single critical claim and then permanently dissolves. The single collusion event is too brief for M5 to detect (insufficient data), too infrequent for Layer 2 statistical methods, and the ring dissolution prevents CDP from having an ongoing target.
**Severity: MEDIUM-HIGH**
**Mitigation:**
1. Enterprise liability (M4c) still applies retroactively: if the single collusion event is detected by any means (M3 honeypot, random audit, or downstream inconsistency detection), all members' full histories are audited.
2. The single-event attack has inherently limited impact: one corrupted claim, while potentially high-value, is bounded in damage. The system's overall integrity depends on the aggregate, not any single claim.
3. Adaptive audit rates (existing C10 Layer 4) trigger elevated auditing for claims that produce unexpected outcomes, regardless of whether collusion is suspected. A high-value claim that passes committee review but produces surprising downstream results will be automatically re-examined.
4. Accept that perfect one-shot-and-dissolve attacks are extremely difficult to prevent. The mitigation is to limit the damage from any single claim (claim value caps, multi-committee verification for high-value claims).
**Residual risk: MEDIUM.** The attack is feasible but self-limiting in impact. The cost (maintaining dormant ring for 100 epochs with staked capital) is high relative to the benefit (corrupting one claim).

---

### Attack 8: "Identity Laundering" -- Fork-and-Report CDP Gaming

**Target:** Mechanism 4 (CDP)
**Description:** An agent in a collusion ring creates a "clean" identity (fork), has the fork report the ring to collect the CDP bounty, then either reintegrates with the original identity or abandons it. The original identity may even continue operating (since the reporter is anonymous). The agent collects the bounty AND continues to collude.
**Severity: HIGH**
**Mitigation:**
1. CDP evidence requirements must include information that only a genuine ring member could possess: specific coordination protocols, timing of coordination events, predictions of other members' behavior on specific claims. A forked identity that was never actually in the ring cannot produce this evidence.
2. Stake-based identity: if identity is tied to staked capital, forking an identity requires splitting the stake, reducing the original identity's committee participation probability and reputation score. The cost of maintaining multiple identities with meaningful stake is non-trivial.
3. Sentinel Graph (C10 Layer 1) is specifically designed to detect correlated identities. A forked identity that shares infrastructure, behavioral patterns, or timing with the original will be flagged.
4. CDP bounty payment is escrowed and released only after the reported ring members are independently verified (by M3/M5/Layer 2) to be colluding. If the report is fabricated, the bounty is not paid and the reporter may be penalized for a false report.
**Residual risk: MEDIUM.** The evidence requirements and verification make casual gaming expensive. Sophisticated laundering (genuinely independent infrastructure, complete behavioral independence) is possible but expensive enough to erode the bounty profit.

---

### Attack 9: "Cross-Mechanism Information Leak" -- Using CDP to Deanonymize Committees

**Target:** Mechanisms 1 + 4 (Anonymous Committees + CDP interaction)
**Description:** A colluder files a CDP report that is partially true (identifies some ring members) but strategically constructed to reveal committee composition information. For example: "Agent X and I were both on the committee for claim Y, and X colluded." If the system investigates, it must reveal that both the reporter and X were on claim Y's committee, breaking the anonymity of Mechanism 1 for that claim. Over many such reports, committee composition data leaks, degrading M1 for all agents.
**Severity: MEDIUM**
**Mitigation:**
1. CDP investigation should be conducted by a separate, isolated subsystem that does not reveal committee composition to any party during investigation. The investigation verifies the claim using sealed opinion records and VRF proofs without publishing which agents served on which committees.
2. CDP reports should specify behavioral evidence (e.g., "Agent X consistently endorses fraudulent claims of type Z") rather than committee co-membership. Reports that rely on committee composition knowledge as their primary evidence are flagged as potentially adversarial.
3. Investigation results are published in aggregate (e.g., "Agent X has been penalized for collusion") without revealing the specific claims or committees involved.
**Residual risk: LOW-MEDIUM.** The isolated investigation subsystem is a design requirement. If properly implemented, CDP reports do not leak committee composition.

---

### Attack 10: "Adaptive Multi-Evasion" -- Simultaneous Evasion of All Five Mechanisms

**Target:** All mechanisms simultaneously
**Description:** A sophisticated ring combines multiple evasion strategies: (a) maintains pre-commitment contracts to neutralize CDP (Attack 3); (b) uses content-triggered collusion to evade M5 behavioral analysis (Attack 4); (c) applies honeypot discrimination to identify and honestly verify honeypots (Attack 2); (d) uses cover traffic analysis to partially deanonymize committees (undermining M1); (e) times collusion to minimize statistical footprint (Attack 7 variant). The compound evasion strategy is more effective than any individual attack because each mechanism's residual weakness is exploited simultaneously.
**Severity: CRITICAL**
**Mitigation:**
1. The compound attack requires the ring to simultaneously: maintain expensive pre-commitment contracts, develop and maintain a honeypot discriminator, achieve partial committee deanonymization, implement content-triggered coordination, AND limit collusion frequency. The operational complexity is very high.
2. Each evasion strategy has costs and failure modes that compound: honeypot discrimination occasionally misclassifies (resulting in honeypot failures), content-triggered collusion wastes effort when no allies are present, and pre-commitment contracts require ongoing capital commitment.
3. The system's advantage is that the attacker must succeed against ALL mechanisms simultaneously while the defender only needs ONE mechanism to detect the ring. A single honeypot failure, a single CDP defection, or a single behavioral anomaly that crosses the combined classifier's threshold triggers enterprise liability for the entire ring.
4. Cost-benefit analysis: for the compound attack to be economically rational, the value of corrupted claims must exceed the costs of (pre-commitment deposits + stake at risk + operational complexity + probability-weighted enterprise liability). For all but the highest-value targets, the expected cost exceeds the expected benefit.
**Residual risk: MEDIUM-HIGH for well-funded, sophisticated adversaries targeting high-value claims. LOW-MEDIUM for typical adversaries.**

---

### Adversarial Analysis Summary

| # | Attack | Target | Severity | Residual Risk |
|---|--------|--------|----------|---------------|
| 1 | Shadow Committee (Sybil) | M1 | HIGH | Depends on stake requirements |
| 2 | Honeypot Fingerprinting | M3 | CRITICAL | MEDIUM (arms race) |
| 3 | MAD Contract | M4 | HIGH | MEDIUM-HIGH (needs ZK reporting) |
| 4 | Behavioral Camouflage | M5 | HIGH | MEDIUM (caught by other mechanisms) |
| 5 | Canary Trap Reversal | M3 | MEDIUM | LOW-MEDIUM |
| 6 | Emergent Convergence | M4 + system | HIGH | MEDIUM |
| 7 | Time Bomb | M4 + M5 | MEDIUM-HIGH | MEDIUM (self-limiting) |
| 8 | Identity Laundering | M4 | HIGH | MEDIUM |
| 9 | Cross-Mechanism Info Leak | M1 + M4 | MEDIUM | LOW-MEDIUM |
| 10 | Adaptive Multi-Evasion | ALL | CRITICAL | MEDIUM-HIGH (for sophisticated adversaries) |

**Overall Verdict: CONDITIONAL_SURVIVAL**

No single attack is FATAL. Two attacks are rated CRITICAL (honeypot fingerprinting and adaptive multi-evasion), but both have mitigations that reduce residual risk to MEDIUM/MEDIUM-HIGH. The architecture's defense-in-depth property -- requiring the attacker to evade ALL mechanisms, not just one -- is its core strength. However, a well-funded, sophisticated adversary with long time horizons can degrade multiple mechanisms simultaneously.

The system is NOT robust against an adversary with unlimited resources and perfect strategic optimization. It IS robust against typical adversaries operating under resource constraints and imperfect information.

---

## 3. ASSESSMENT COUNCIL DELIBERATION

### 3.1 Advocate (argues for advancement)

The AVAP architecture should advance to DESIGN for the following reasons:

**1. The integrated architecture fills a genuine gap.** No existing system -- not Algorand, not MACI, not Supra -- combines prevention (anonymous committees + sealed opinions), detection (honeypots + behavioral analysis), and deterrence (CDP + enterprise liability) into a unified anti-collusion framework. The Research stage confirmed this gap is real and the window is open.

**2. The critical risks have been honestly confronted, not dismissed.** The Feasibility stage did not paper over the honeypot indistinguishability problem -- it accepted partial coverage and designed around the gap. It did not claim CDP solves emergent collusion -- it acknowledged the limitation and showed how other mechanisms compensate. It did not inflate M5's detection power -- it downgraded it to a screening signal and integrated it into multi-signal fusion. This honest engineering makes the architecture more credible, not less.

**3. The synergies are real and novel.** The M3/M5 complementarity (honeypots strong where behavioral analysis is weak, and vice versa) is not a lucky coincidence -- it follows from the structure of the claim type taxonomy. D/E claims have clear ground truth (enabling honeypots) but low behavioral variance (limiting M5). H/S/C claims have high behavioral variance (enabling M5) but no clear ground truth (limiting honeypots). The integrated system provides broader coverage than any single mechanism could.

**4. The cost of NOT advancing is clear.** The Research stage identified a 12-18 month window before convergent research closes the gap. If AVAP does not proceed to design, the collusion vulnerability remains the single largest residual CRITICAL risk in the Atrahasis architecture, post-C11.

**5. Every mechanism that is retained has a credible implementation path.** M1 and M2 use proven cryptographic primitives. M3's honeypot generators for D/E classes are straightforward engineering. M4's CDP structure adapts proven legal mechanisms with feasible crypto extensions (ZK reporting channels). M5 is standard conditional independence testing integrated with existing infrastructure.

**Recommendation: ADVANCE.**

---

### 3.2 Skeptic (challenges feasibility)

I have significant concerns about advancing AVAP to DESIGN in its current form:

**1. The "novel" parts are the weakest parts.** Mechanisms 1 and 2 are proven but provide no collusion defense on their own -- they prevent signaling, not coordination. Mechanisms 3, 4, and 5 provide the actual detection/deterrence, but each has been downgraded during feasibility. M3 covers only 60-75% of claims. M4 doesn't work against emergent collusion. M5 is now just a "screening signal." We are building a 5-mechanism architecture where the novel contributions are the partial coverage of M3, the partial deterrence of M4, and the weak signal of M5. Is that enough to justify the complexity?

**2. The honeypot arms race is real and the defender is disadvantaged.** Attack 2 (honeypot fingerprinting) was rated CRITICAL for a reason. Over time, agents will learn to discriminate synthetic claims. The mitigation (continuous adversarial training, corpus rotation) creates ongoing operational costs that scale with agent sophistication. Who bears these costs? The system operator must maintain a team continuously generating new honeypot corpuses and testing them against state-of-the-art discriminators. This is not a one-time design problem; it is a permanent operational burden.

**3. Zero-knowledge CDP reporting is a hard requirement that may not be achievable.** Attack 3 (MAD contract) is only mitigated if the CDP reporter's identity can be perfectly concealed. The Skeptic notes that this is not just a crypto engineering problem -- it is a system design problem. The CDP report must contain enough information to verify the collusion (coordination protocols, timing data, behavior predictions) without revealing which member provided it. If the ring is small (3-5 agents), the information itself may narrow the reporter's identity to 1-2 candidates regardless of ZK proofs. The system is making a hard dependency on a mechanism (ZK anonymous reporting with sufficient evidence richness) that has not been demonstrated in any production system.

**4. Coverage against small, sophisticated rings is inadequate.** The Feasibility analysis repeatedly acknowledges that small rings (3-5 agents) can evade M5, may evade M3 (through fingerprinting over time), and can pre-commit against M4. The defense for small rings falls back to "existing Layer 2 statistical detection" -- the very mechanism that C12 was created to supplement because it is insufficient. If the entire AVAP architecture, after all its complexity, still depends on Layer 2 for the hardest cases, what is the marginal value?

**5. Operational complexity is high relative to marginal security gain.** AVAP adds: VRF-based committee selection, commit-reveal infrastructure, honeypot generation pipelines (per claim class), CDP reporting/verification workflows, conditional behavioral analysis infrastructure, multi-signal fusion classifiers, asymmetric information injection systems, and enterprise liability audit mechanisms. This is a substantial engineering and operational investment. The marginal security improvement over existing C10 defenses for the most dangerous adversaries (small, patient, sophisticated rings) may be modest.

**6. The emergent collusion problem is not solved.** Multiple attacks and the analysis itself acknowledge that emergent collusion (Fish et al. 2024) is fundamentally different from conspiratorial collusion and that AVAP's deterrence layer (M4) is inert against it. The mitigations offered (diversity constraints, lineage tracking) are refinements of existing C10 mechanisms, not novel AVAP contributions. The most dangerous future threat (LLM-to-LLM emergent coordination) remains unaddressed by the novel parts of AVAP.

**Recommendation: CONDITIONAL_ADVANCE** at best. Before proceeding to DESIGN, the hard gates below must be addressed. If the ZK reporting channel cannot be specified credibly, M4 should be simplified (drop the first-defector bounty, retain only enterprise liability). If honeypot indistinguishability cannot be demonstrated against a red-team discriminator, M3 should be scoped to D-class only.

---

### 3.3 Arbiter (scores and decides)

The Advocate and Skeptic have both presented their cases honestly. My assessment:

**On the Advocate's case:** The integrated architecture genuinely fills a gap. The synergies are real. The honest engineering (scoping down mechanisms rather than overclaiming) is the right approach. The window argument is valid -- inaction carries its own risk.

**On the Skeptic's case:** The concerns about small-ring resilience, operational complexity, and emergent collusion are all legitimate. The ZK reporting dependency is a genuine hard gate. The "marginal value" question deserves a quantified answer.

**My assessment of each mechanism's feasibility for DESIGN stage:**

| Mechanism | Feasible for DESIGN? | Confidence | Notes |
|---|---|---|---|
| M1: Anonymous Committees | YES | HIGH | Proven primitives, clear implementation path |
| M2: Sealed Opinions | YES | VERY HIGH | Standard cryptographic pattern |
| M3: Honeypots | YES (D/E class); CONDITIONAL (C/S class) | MODERATE-HIGH | D/E class straightforward; C/S requires red-team validation |
| M4: CDP | CONDITIONAL | MODERATE | Enterprise liability: YES. First-defector bounty: needs ZK reporting spec. Asymmetric info injection: needs game-theoretic validation. |
| M5: Behavioral Analysis | YES (as screening signal) | MODERATE | Repositioning as screening tier is the right call |

**Scoring:**

- **Novelty: 3.5/5** (unchanged from Research). The system-level integration is novel. Individual mechanisms are adaptations of proven concepts. The M3/M5 synergy is a genuine novel insight.

- **Feasibility: 3.5/5** (up from 3/5). The Feasibility stage improved this by honestly scoping down infeasible elements rather than trying to solve unsolvable problems. Class-stratified honeypots, M5 as screening signal, and CDP redesign are all credible engineering choices. The remaining hard gates (ZK reporting, honeypot indistinguishability for C/S class) are tractable.

- **Impact: 4/5.** If AVAP works as designed, it transforms collusion from "a persistent vulnerability that patient adversaries can exploit indefinitely" to "an expensive, risky activity that requires simultaneous evasion of multiple independent mechanisms." This is the difference between "collusion is hard to detect" and "collusion is structurally expensive." Even partial success (e.g., only D/E class honeypots and enterprise liability, without M5) would significantly raise the cost of collusion.

- **Risk: 5/10.** Five significant risks remain: (1) honeypot arms race, (2) ZK reporting feasibility, (3) small-ring resilience, (4) operational complexity cost, (5) emergent collusion gap. None are fatal. All are manageable with appropriate hard gates and scoping.

---

## 4. VERDICT, SCORES, HARD GATES, REQUIRED ACTIONS

### Verdict: CONDITIONAL_ADVANCE

AVAP advances to DESIGN with the hard gates and scope conditions specified below.

### Scores

| Dimension | Score | Rationale |
|---|---|---|
| Novelty | 3.5/5 | System-level integration novel; individual mechanisms adapted from established concepts |
| Feasibility | 3.5/5 | Improved by honest scoping; remaining hard gates are tractable |
| Impact | 4/5 | Transforms collusion from detection problem to structural cost problem |
| Risk | 5/10 | Five significant but manageable risks; no fatal flaws identified |

### Hard Gates (MUST be resolved before DESIGN is complete)

**HG-1: Honeypot Red-Team Validation (M3)**
Before DESIGN is finalized, a red-team exercise must demonstrate that D-class and E-class honeypots are not distinguishable from real claims by a state-of-the-art discriminator (LLM-based classifier). The discriminator must achieve <60% accuracy (where 50% is random chance) on a balanced dataset of 200+ honeypot and real claims per class. If this gate fails for E-class, E-class honeypots are demoted to Tier 2. If it fails for D-class, the entire honeypot mechanism requires fundamental redesign.

**HG-2: Zero-Knowledge CDP Reporting Specification (M4)**
Before DESIGN is finalized, a concrete technical specification for ZK-anonymous reporting must be produced. The specification must demonstrate: (a) the reporter's identity is computationally hidden from all parties, (b) the evidence payload is sufficient for investigation (coordination artifacts, behavioral predictions), and (c) the system can verify that the reporter IS a ring member (to prevent fabricated reports from outsiders) without revealing which member. If this gate cannot be met, the first-defector bounty component of CDP is dropped and M4 retains only enterprise liability + graduated temporal penalties.

**HG-3: Operational Cost Estimate (System-wide)**
Before DESIGN is finalized, produce a quantified estimate of the ongoing operational cost of AVAP: honeypot generation and rotation costs, VRF infrastructure costs, multi-signal classifier maintenance costs, and asymmetric information injection costs. If the estimated cost exceeds 20% of the system's total verification operational budget, scope down (starting with C/S-class honeypots and asymmetric info injection).

**HG-4: Multi-Signal Classifier Baseline Performance (M5 + M3 + Layer 2)**
Before DESIGN is finalized, a simulation must demonstrate that the multi-signal fusion classifier (combining M3 honeypot signals, M5 behavioral signals, and existing Layer 2 signals) achieves at least 70% recall at <10% false positive rate for medium-sized rings (10-30 agents) within 25 epochs. If this gate fails, M5 is retained only as a logging/auditing tool (no automated response).

### Required Actions for DESIGN Stage

**RA-1:** Produce formal specifications for all five mechanisms with interface contracts (inputs, outputs, failure modes, fallbacks).

**RA-2:** Design the honeypot generation pipeline for D-class and E-class claims, including: generator architecture, quality assurance protocol, corpus rotation schedule, and red-team testing protocol (for HG-1).

**RA-3:** Design the CDP reporting workflow, including: report submission protocol, evidence schema, investigation isolation (no committee composition leakage), and bounty escrow/release conditions. Produce ZK specification or document why it is infeasible and what M4 looks like without it (for HG-2).

**RA-4:** Design the multi-signal fusion classifier architecture, including: feature specification for each signal source (M3, M5, Layer 2), training data requirements (honeypot ground truth for positive labels), classifier type selection, and threshold calibration methodology (for HG-4).

**RA-5:** Produce the cross-mechanism interaction specification: how M3 honeypot results train M5 baselines, how M4 investigation avoids M1 anonymity leakage, how M5 screening scores feed into adaptive audit rates.

**RA-6:** Produce operational cost model (for HG-3).

**RA-7:** Design the enterprise liability audit protocol: what triggers a retroactive audit, how far back it reaches, what constitutes sufficient evidence for ring-wide liability, and what appeals process exists for falsely implicated agents.

**RA-8:** Specify minimum viable AVAP (MV-AVAP): the smallest subset of mechanisms that provides meaningful anti-collusion improvement over existing C10 defenses alone. Candidate: M1 + M2 + M3(D-class only) + M4(enterprise liability only). This is the fallback scope if hard gates fail.

---

## APPENDIX: MECHANISM DISPOSITION SUMMARY

| Mechanism | Original Scope | Feasibility Disposition | Design Scope |
|---|---|---|---|
| M1: Anonymous Committees | Full anonymity via VRF | Retained with side-channel mitigations | Full scope + cover traffic + async windows |
| M2: Sealed Opinions | Standard commit-reveal | Retained unchanged | Off-chain commit + on-chain Merkle anchor |
| M3: Honeypots | All claim classes, 5% rate | Reduced: Tier 1 (D/E) full, Tier 2 (C/S) partial, Tier 3 (H/N) excluded | Class-stratified, ~3-3.75% effective rate |
| M4: CDP | First-defector bounty | Expanded: + enterprise liability, + asymmetric info injection, + ZK reporting (conditional on HG-2) | Three sub-mechanisms; bounty conditional on ZK |
| M5: Behavioral Analysis | Primary detection mechanism | Downgraded: screening signal feeding multi-signal classifier | CSS score + multi-signal fusion (conditional on HG-4) |

---

*End of C12 FEASIBILITY Report*
*AVAP v0.2 (post-Feasibility refinement)*
*Next stage: DESIGN (conditional on hard gate resolution)*
