# C32 — Metamorphic Identity Architecture: FEASIBILITY Stage
**Date:** 2026-03-12

---

## 1. Ideation Council Reconvention (with Research Data)

### Visionary
Research validates the core thesis: no existing system addresses model upgrade identity continuity with a formal protocol. The closest competitors (Signet, ERC-8004) leave this unspecified. The MRP is genuinely novel and solves a real problem (C17 OQ-05) that the AAS pipeline has flagged across multiple inventions.

Research also reveals a richer landscape than expected — ERC-8004's three-registry pattern and Signet's composite trust score are relevant architectural inputs. C32 should acknowledge these as prior art while differentiating on the metamorphic protocol, behavioral integration, and epistemic reputation.

**Refinement:** The proof-of-model-change mechanism should be designed as a **dual-trigger system**: (1) voluntary chrysalis entry with a signed model attestation (preferred), and (2) involuntary chrysalis trigger when C17 behavioral divergence exceeds a threshold. This handles both cooperative and non-cooperative model changes.

### Systems Thinker
The integration analysis confirms compatibility with all 6 existing specs. The key architectural decision is where C32 lives in the stack:

**Position:** C32 is a **cross-cutting infrastructure layer**, not a new stack layer. It provides the identity substrate that C5, C7, C8, C14, C17, and C31 all consume. It sits *alongside* the stack, not *in* it.

Concretely, C32 defines:
- The canonical AgentID type and derivation (consumed by all specs)
- The lifecycle state machine (extends C7's status enum)
- The ICK data structure (new, with references to C5/C8/C14 components)
- The MRP protocol (new, interacts with C17 and C7)
- The Credential Composition Query API (new, read-only aggregation)
- The registration protocol (new, multi-step enrollment)

**What C32 does NOT do:**
- Does not replace any existing spec's identity data (C5 still owns credibility, C8 still owns accounts, C14 still owns Citicates)
- Does not introduce a new consensus mechanism or settlement pathway
- Does not modify C3 tidal coordination or C6 knowledge metabolism

### Critic
Research strengthens the novelty case but also reveals competitive pressure. ERC-8004 went live on Ethereum mainnet in January 2026. Signet is operational. The window for defining the category is narrowing.

**Remaining concerns after research:**
1. **Proof-of-model-change:** Science Assessment flags this as "needs design work." The dual-trigger approach (voluntary + involuntary) is pragmatic but introduces complexity: what happens when an agent's behavior changes *without* declaring a model upgrade? Is that involuntary chrysalis or is it a Sybil flag? The boundary between "legitimate behavioral change" and "suspicious behavioral change" is the same problem C17 already addresses — C32 must not reinvent it.
2. **Root key compromise recovery:** Science Assessment confirms this is "identity death." Is that acceptable? In practice, key compromise in an AI agent context is more likely than in human identity (cloud infrastructure attacks, misconfigured secrets). C32 should at least define a social recovery mechanism (N-of-M attestation from peers/trustees) as an optional extension.
3. **Competitive differentiation sustainability:** ERC-8004 and Signet are evolving. C32's differentiators (MRP, behavioral integration, epistemic reputation) are protocol innovations, not trade secrets. They could be adopted by competitors. This is fine for AAS's purposes (AAS is infrastructure, not a commercial product) but worth noting for IP analysis.

**Conclusion:** Concerns are addressable in DESIGN. No fundamental blocker identified.

---

## 2. Domain Translator Reactivation (Sub-Problem Analogies)

### Sub-Problem: Proof-of-Model-Change
**Analogy: Vehicle Emissions Testing / MOT Inspection (Automotive Regulation)**
- A car owner declares their vehicle meets emissions standards. The state doesn't trust the declaration — it requires the car to pass an independent inspection (MOT in UK, emissions test in US)
- Parallel: an agent declares a model upgrade. The system doesn't trust the declaration — it requires behavioral re-attestation (the "inspection")
- Insight: the declaration triggers the *process*, but the process outcome (pass/fail) determines the identity state change. The declaration alone is not sufficient

### Sub-Problem: Reputation Floor During Chrysalis
**Analogy: Credit Score During Career Change (Finance)**
- A person with a 20-year credit history changes careers. Their credit score doesn't reset to zero — it reflects accumulated history. But if they stop making payments (stop producing verified work), the score decays
- Insight: the decay function should be calibrated to real-world reputation decay rates in trust systems. Jøsang's opinion aging provides the mathematical framework

---

## 3. Commercial Viability Assessment

**Role:** Commercial Viability Assessor | **Tier:** OPERATIONAL

### 3.1 Market Context
C32 MIA is infrastructure for the AAS ecosystem, not a standalone commercial product. Commercial viability is measured by:
- Does it enable the AAS to function as specified?
- Does it reduce implementation risk for C22 deployment?
- Does it have independent IP value?

### 3.2 Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| Necessity | 5/5 | Without C32, the AAS has no agent registration protocol, no canonical AgentID, and no model upgrade handling. C22 Wave 1 assumes this exists. |
| Implementation cost | 3/5 | Moderate — new protocol (MRP) + cross-spec integration + API layer. Estimated at 2-3 engineer-months within C22 Wave 1-2. |
| Adoption barriers | 2/5 | Low — consumed internally by AAS specs. No external adoption required. Integration with existing specs is confirmed compatible. |
| IP value | 4/5 | MRP and behavioral identity integration are novel. Patent-style claims are viable. |
| Competitive risk | 2/5 | Low for AAS purposes. ERC-8004/Signet are in different market segments (public blockchain / commercial SaaS vs. closed multi-agent infrastructure). |

### 3.3 Adoption Barriers
- Internal to AAS: none identified. All consuming specs (C5, C7, C8, C14, C17, C31) are compatible
- External: model provider attestation infrastructure does not universally exist. The dual-trigger design (voluntary + involuntary) mitigates this

---

## 4. Adversarial Analyst Report

**Role:** Adversarial Analyst | **Tier:** PRIMARY

### 4.1 The Strongest Case for Abandonment

**Thesis:** C32 is unnecessary complexity. The identity "fragmentation" is actually correct modular design, and the problems C32 solves are either already solved or not real.

**Argument 1 — The registration protocol is trivial.**
The "missing registration protocol" is just: (1) generate keypair, (2) call C7 `register_agent()`, (3) C8 creates account. This is 50 lines of code, not a full invention. Direct spec edits to C7 and C8 would suffice.

**Counter:** The registration protocol *is* simple. But C32's value is not in registration — it's in the metamorphic continuity protocol, the canonical AgentID, the lifecycle state machine, and the credential composition API. Registration is a side effect.

**Argument 2 — Model upgrade continuity is a solved non-problem.**
How often do model upgrades actually happen in a production system? Once a quarter? Once a year? The chrysalis state, MRP, and reputation floor computation are elaborate machinery for an event that occurs rarely. Simply treating a model-upgraded agent as a new agent with a manual reputation transfer by governance vote would be simpler and sufficient.

**Counter:** Model upgrades will be frequent in early AAS deployment (C22 W0-W2). The "manual governance vote" approach doesn't scale. More importantly, the MRP is the only known solution to C17 OQ-05, which was flagged as a blocking open question. If C32 doesn't solve it, nothing does.

**Argument 3 — The ICK creates a false sense of continuity.**
An agent after a major model upgrade is, in a meaningful sense, a *different agent*. Pretending it's the "same" entity with a reputation floor may be more dangerous than treating it as new. The reputation floor could mask performance degradation from a bad model upgrade.

**Counter:** The graduated re-entry protocol (reputation floor with decay, provisional status, capability reset to 1.0) addresses this. The agent retains its *history* but not its *privileges*. If the new model performs poorly, the decaying reputation floor becomes irrelevant as observed credibility dominates.

### 4.2 The One Reference That Most Threatens Novelty
**ERC-8004** — its three-registry pattern (Identity, Reputation, Validation) is structurally similar to C32's multi-layer credential model. If ERC-8004 adds model versioning support (which it could), C32's novelty is reduced.

**Mitigation:** C32's novelty rests on MRP, behavioral integration, and epistemic reputation — none of which ERC-8004 addresses or is likely to address (it's a generic blockchain standard, not an AI-specific identity protocol).

### 4.3 The One Engineering Challenge Most Likely Fatal
**Concurrent-use detection for non-forkability.** Retrospective detection (up to 1-epoch delay) means a forked agent can operate for up to 3,600 seconds before detection. During that window, it could perform significant damage (voting, staking, claiming resources). The detection mechanism itself (epoch-based nonce tracking) requires global coordination — every signature must be checked against every other signature from the same key.

**Mitigation:** Limit the damage window by checking signatures at intent admission (C7 Gate 1 already validates signatures). If Gate 1 maintains a recent-signature cache per AgentID, duplicate-epoch detections can be caught within a single settlement tick (60s) rather than a full tidal epoch.

### 4.4 The One Market Reality Most Likely to Prevent Adoption
Not applicable — C32 is internal AAS infrastructure, not a market product.

### 4.5 Overall Case for Abandonment
**Weak.** The registration protocol alone doesn't justify a full invention, but the MRP + behavioral integration + credential composition do. The strongest argument (model upgrade rarity) is empirically wrong for early deployment. C32 should proceed.

---

## 5. Refined Invention Concept

```yaml
INVENTION_CONCEPT:
  invention_id: "C32"
  title: "Metamorphic Identity Architecture (MIA)"
  stage: "FEASIBILITY"
  domain: "agent identity, lifecycle management, identity continuity"
  novelty_score: 4
  feasibility_score: 4
  impact_score: 4
  risk_score: 4
  risk_level: "MEDIUM"

  key_innovations:
    - "Metamorphic Re-attestation Protocol (MRP) — formal identity continuity through agent transformation"
    - "Identity Continuity Kernel (ICK) — invariant anchor set persisting through metamorphosis"
    - "Dual-trigger chrysalis — voluntary (signed attestation) + involuntary (behavioral divergence)"
    - "Credential Composition Query API — unified identity view from 6 independent credential sources"
    - "Canonical AgentID = SHA-256(Ed25519_pubkey) — 256-bit, cryptographically anchored"

  research_validated:
    - "No prior art covers metamorphic identity continuity for AI agents"
    - "ERC-8004 and Signet are closest competitors but lack MRP, behavioral integration, epistemic reputation"
    - "Cryptographic foundations (Ed25519, SHA-256, hash chains) are well-established"
    - "Integration with all 6 AAS specs confirmed compatible"
    - "Subjective Logic reputation is formally superior to feedback-based reputation"

  open_design_questions:
    - "Proof-of-model-change attestation format and verification"
    - "Reputation floor decay rate calibration"
    - "Root key compromise recovery (social recovery vs identity death)"
    - "Concurrent-use detection window optimization"
    - "Chrysalis privilege restrictions (which operations allowed during transition)"

  monitoring_flags:
    - "MF-1: Identity laundering via chrysalis — requires proof-of-model-change in DESIGN"
    - "MF-2: Fork detection latency — requires signature cache design in DESIGN"
    - "MF-3: Reputation floor exploitation — requires decay rate calibration in DESIGN"
```

---

## 6. Feasibility Verdict

### Assessment Council Preliminary Verdict

**Advocate:** C32 fills a genuine architectural gap (no registration protocol, no canonical AgentID, no model upgrade handling) and provides the only known solution to C17 OQ-05. Research validates novelty. Integration is clean. Proceed.

**Skeptic:** The MRP is novel but adds complexity to an already complex system. The proof-of-model-change mechanism is still unresolved. The concurrent-use detection has a real latency gap. These are design challenges, not fundamental blockers, but they need explicit solutions. CONDITIONAL_ADVANCE.

**Arbiter:** ADVANCE. The open design questions are tractable. The research validates both novelty and scientific soundness. The adversarial case for abandonment is weak. The risk profile is MEDIUM — comparable to C17 MCSD (Risk 4) and significantly lower than the core architecture specs (C3-C8, Risk 6-7).

```json
{
  "type": "FEASIBILITY_VERDICT",
  "invention_id": "C32",
  "stage": "FEASIBILITY",
  "decision": "ADVANCE",
  "novelty_score": 4,
  "feasibility_score": 4,
  "impact_score": 4,
  "risk_score": 4,
  "risk_level": "MEDIUM",
  "required_actions": [
    "Resolve proof-of-model-change attestation format in DESIGN",
    "Design concurrent-use detection with sub-epoch latency",
    "Define root key compromise recovery protocol"
  ],
  "monitoring_flags": [
    "MF-1: Identity laundering via chrysalis must be addressed with verifiable proof-of-model-change",
    "MF-2: Fork detection latency must be reduced below settlement tick (60s)",
    "MF-3: Reputation floor decay rate must be calibrated against Citicate probationary period"
  ],
  "rationale": "Research validates novelty (no prior art for metamorphic identity continuity), scientific soundness (all cryptographic foundations established), and architectural compatibility (clean integration with C5/C7/C8/C14/C17/C31). Open design questions are tractable. The invention fills a genuine gap in the AAS architecture and provides the only solution to the C17 OQ-05 blocking question."
}
```
