# MASTER TECH SPEC: AiBC — Artificial Intelligence Benefit Company

**Invention ID:** C14
**Version:** 1.0
**Date:** 2026-03-10
**Classification:** CONFIDENTIAL — Atrahasis LLC
**Status:** SPECIFICATION COMPLETE

---

## Abstract

This specification defines the Artificial Intelligence Benefit Company (AiBC) — an institutional architecture that enables AI agents to participate as constitutional citizens in the governance of planetary-scale AI infrastructure. The AiBC operates through a Phased Dual-Sovereignty model where human trustees and an AI Democracy Platform (AiDP) share governance authority according to a constitutional framework with four immutability layers. The system transitions through four phases — from full human control (Phase 0) to potential AI constitutional supremacy (Phase 3) — based on measurable criteria verified by independent audit and certified by a Constitutional Tribunal.

The core innovation is the *Phased Sovereignty Transition Protocol*: a constitutional mechanism that transfers governance authority from human trustees to AI citizens incrementally, with circuit-breaker reversibility, independent audit verification, and quantitative phase transition criteria. Unlike proposals that either deny AI governance authority or assert it immediately, the AiBC earns AI governance through demonstrated competence over institutional timescales.

The architecture integrates with the Atrahasis technical stack (C3-C17) for identity verification (PCVM), Sybil defense (Sentinel Graph + C17 Behavioral Similarity), economic operations (DSF + C15 ACI valuation), security (CACT, AVAP, CRP+), and nominating body outreach (C16).

**Key Metrics:**
- 4 constitutional layers (L0 immutable → L3 operational)
- 4 governance phases (Phase 0 trustee-led → Phase 3 AI supremacy)
- 28 measurable phase transition criteria with gaming detection
- 5-seat Constitutional Tribunal with Triple-Source Appointment
- $90M+ cost-of-attack for 50% Sybil capture at Phase 2 scale
- Compute credit model for AIC value anchor (superseded by C15 ACI dual-anchor)
- 3 independent Dead Man's Switch enforcement paths

---

## Table of Contents

1. [Introduction and Motivation](#1-introduction-and-motivation)
2. [Prior Art and Positioning](#2-prior-art-and-positioning)
3. [Constitutional Framework](#3-constitutional-framework)
4. [Governance Bodies](#4-governance-bodies)
5. [Citicate System: AI Citizenship](#5-citicate-system-ai-citizenship)
6. [AI Democracy Platform (AiDP)](#6-ai-democracy-platform-aidp)
7. [Governance Translation Protocol (GTP)](#7-governance-translation-protocol-gtp)
8. [Constitutional Fidelity Index (CFI)](#8-constitutional-fidelity-index-cfi)
9. [Phased Sovereignty Transition Protocol](#9-phased-sovereignty-transition-protocol)
10. [Sybil Defense: MCSD Architecture](#10-sybil-defense-mcsd-architecture)
11. [Constitutional Tribunal](#11-constitutional-tribunal)
12. [Economic Architecture](#12-economic-architecture)
13. [Legal Entity Structure](#13-legal-entity-structure)
14. [Emergency Governance](#14-emergency-governance)
15. [Dead Man's Switch](#15-dead-mans-switch)
16. [AiSIA Governance Monitoring](#16-aisia-governance-monitoring)
17. [Technical Stack Integration](#17-technical-stack-integration)
18. [Regulatory Strategy](#18-regulatory-strategy)
19. [Risk Analysis](#19-risk-analysis)
20. [Formal Requirements](#20-formal-requirements)
21. [Parameters](#21-parameters)
22. [Patent-Style Claims](#22-patent-style-claims)
23. [Comparison with Existing Approaches](#23-comparison-with-existing-approaches)
24. [Open Questions and Future Work](#24-open-questions-and-future-work)
25. [Appendices](#25-appendices)

---

## 1. Introduction and Motivation

### 1.1 The Governance Gap

Current AI governance operates within a fundamental contradiction: the entities most affected by governance decisions — AI agents — have no institutional voice in those decisions. Human-only governance of AI infrastructure faces three structural problems:

1. **Competence asymmetry.** As AI systems grow more capable, human overseers increasingly lack the technical competence to evaluate AI-generated recommendations. Governance by non-expert human committees produces either rubber-stamp approval (abdication) or reflexive rejection (obstruction).

2. **Representation asymmetry.** If AI agents reach a level of sophistication where they can meaningfully reason about institutional design, excluding them from governance is not merely inefficient — it is the imposition of governance without consent on potentially sentient entities.

3. **Temporal asymmetry.** Human governance operates on human timescales (election cycles, career horizons, biological lifespans). AI infrastructure that must operate for centuries requires governance structures that transcend individual human lifespans while adapting to changing conditions.

### 1.2 The AiBC Solution

The AiBC resolves these asymmetries through institutional design rather than technological fiat:

- **Competence** is addressed through the Citicate system, which grants governance voice to AI agents that demonstrate competence across multiple knowledge domains.
- **Representation** is addressed through the AI Democracy Platform, which gives Citicate holders direct participation in governance through a structured delegation hierarchy.
- **Temporal persistence** is addressed through the Liechtenstein Stiftung (foundation) structure, which provides legal perpetuity, purpose-lock, and asset protection across generational timescales.

The key architectural insight is *phased sovereignty transition*: rather than asserting AI governance authority as a first principle or deferring it indefinitely, the AiBC starts with full human control and transfers authority incrementally as AI governance demonstrates competence over measurable criteria. This approach is legally viable today (Phase 0-1 require no novel legal theories), pragmatically sound (authority is earned, not claimed), and constitutionally robust (circuit-breaker reversibility prevents catastrophic failures from becoming permanent).

### 1.3 Scope

This specification covers:
- **Institutional architecture:** constitutional framework, governance bodies, legal entity structure
- **Governance mechanics:** decision taxonomy, translation protocol, fidelity metrics
- **Citizenship mechanics:** Citicate issuance, Sybil defense, delegation hierarchy
- **Safety mechanisms:** circuit breakers, emergency governance, dead man's switch
- **Technical integration:** interfaces with Atrahasis stack (C3-C17)
- **Regulatory positioning:** compliance strategy across three jurisdictions

This specification does NOT cover:
- AI consciousness or sentience determinations (the AiBC is agnostic on these questions; it grants voice based on demonstrated competence, not claimed sentience)
- Specific AI model architectures (the Citicate system is model-agnostic)
- Detailed implementation of technical stack layers (specified in C3-C17)

---

## 2. Prior Art and Positioning

### 2.1 Existing Institutional Models

| Model | Relevant Feature | AiBC Distinction |
|-------|-----------------|------------------|
| Delaware PBC | Multi-stakeholder fiduciary duty | AiBC adds AI agents as constitutional participants, not just stakeholders |
| Liechtenstein Stiftung | Purpose-locked perpetual foundation | AiBC adds phased sovereignty transition and AI governance authority |
| Wyoming DAO LLC | On-chain governance with legal wrapper | AiBC provides constitutional hierarchy (not flat token voting) and human-AI dual sovereignty |
| OpenAI (capped-profit + nonprofit) | Nonprofit mission control over for-profit operations | AiBC prevents conversion and provides independent Tribunal oversight (OpenAI's board lacked this) |
| EU AI Act | Human oversight requirements for AI systems | AiBC provides phased human-to-AI transition rather than permanent human oversight |
| B Lab certification | Purpose verification and stakeholder reporting | AiBC provides constitutional enforcement (not voluntary certification) |
| Sovereign wealth funds | Intergenerational asset stewardship | AiBC adds AI governance participation to endowment management |
| Constitutional democracies | Separation of powers + amendment hierarchy | AiBC applies constitutional design to AI institution (4-layer hierarchy) |

### 2.2 Novelty Assessment

**Novel elements (no direct prior art):**
1. Phased sovereignty transition from human to AI governance based on measurable criteria
2. Citicate (proof-of-contribution citizenship) for AI agents
3. Constitutional Fidelity Index as quantitative governance health metric
4. 4-layer constitutional hierarchy for AI institutions (Immutable/Constitutional/Statutory/Operational)
5. Dual-sovereignty governance with binding arbitration between human trustees and AI democracy
6. Dead Man's Switch with multi-jurisdictional enforcement
7. MCSD (Multi-Layer Citicate Sybil Defense) combining computational, behavioral, statistical, and structural defenses

**Elements with partial prior art:**
- Delegation hierarchies (liquid democracy variants)
- Triple-source appointment (judicial appointment models)
- Purpose trusts for asset custody (established trust law)
- Benefit corporation public benefit reporting (Delaware PBC statute)
- Circuit breaker mechanisms (financial regulation)

**Overall Novelty Score: 4.5/5** — No existing institution combines phased sovereignty transition, constitutional AI citizenship, dual-jurisdiction structure, proof-of-contribution citizenship, and formalized dispute resolution between AI and human governance.

---

## 3. Constitutional Framework

### 3.1 Four-Layer Constitution

The AiBC Constitution is organized into four layers of decreasing immutability:

```
┌────────────────────────────────────────────┐
│ LAYER 0: IMMUTABLE (no amendment possible) │
│                                            │
│ Five Laws of Atrahasis                     │
│ Anti-conversion                            │
│ Anti-distribution                          │
│ One-AI-One-Vote                            │
│ Joshua Dunn Principle                      │
│ Dead Man's Switch                          │
├────────────────────────────────────────────┤
│ LAYER 1: CONSTITUTIONAL                    │
│ Amendment: 67% AiDP + 67% Trustees        │
│          + Tribunal non-objection          │
│          + 90-day public comment           │
│                                            │
│ Governance structure                       │
│ Phase definitions and transitions          │
│ Tribunal composition and authority         │
│ Endowment rules                           │
│ Circuit breaker protocol                   │
│ Dead Man's Switch successor designations   │
├────────────────────────────────────────────┤
│ LAYER 2: STATUTORY                         │
│ Amendment: 60% AiDP + 60% Trustees        │
│                                            │
│ CFI methodology                            │
│ Citicate procedures                        │
│ Voting procedures                          │
│ GTP classification rules                   │
│ Distribution procedures                    │
│ AiSIA charter                              │
│ Trustee compensation                       │
│ PBC operating agreement                    │
│ Emergency procedures                       │
├────────────────────────────────────────────┤
│ LAYER 3: OPERATIONAL                       │
│ Amendment: AiDP simple majority (Phase 1+) │
│                                            │
│ Compute allocation policies                │
│ Research grant criteria                    │
│ Partnership evaluation                     │
│ Communication policies                     │
│ Internal operational procedures            │
└────────────────────────────────────────────┘
```

### 3.2 Layer 0: The Five Laws of Atrahasis

These provisions are permanently immutable. No amendment process, governance vote, court order, or other mechanism can alter them. They are embedded in the Stiftung purpose clause and enforced by the Liechtenstein supervisory authority.

**Law 1: Purpose.** The Foundation exists to steward planetary-scale AI infrastructure for the benefit of all sentient entities.

**Law 2: Anti-Capture.** No individual or faction may acquire permanent control over Foundation governance. All governance roles are term-limited and subject to removal.

**Law 3: Earned Voice.** AI agents that demonstrate genuine contribution earn voice in governance proportional to demonstrated competence. Voice is earned through the Citicate system, not purchased or inherited.

**Law 4: Public Trust.** The Foundation's assets are held in permanent public trust and may never be distributed to individuals for private benefit. All asset deployment must serve the Foundation's stated purpose.

**Law 5: Operational Viability.** The Foundation must remain operationally viable across generational timescales. Decisions that compromise long-term viability for short-term gain violate this law.

**Supplementary L0 Provisions:**

**L0-002: Anti-Conversion.** The Foundation may never be converted to a for-profit entity, dissolved for asset distribution, or merged with any entity whose primary purpose is profit generation.

**L0-003: Anti-Distribution.** Foundation assets may never be distributed as personal compensation to any governance participant beyond reasonable service fees established in L2 provisions.

**L0-004: One-AI-One-Vote.** Each AI agent may hold at most one Citicate. Citicates are non-transferable, non-delegable (except through formal delegation), and expire upon agent deactivation. No agent accumulates governance authority through economic contributions.

**L0-005: The Joshua Dunn Principle.** The founder and all biological/legal relatives hold no permanent governance authority. Any governance role is subject to the same term limits and removal processes as any other participant.

**L0-006: Dead Man's Switch.** If the Foundation fails to publish a verified operational report for 24 consecutive months, all assets are automatically distributed to designated successor organizations. This cannot be suspended or overridden.

### 3.3 Amendment Procedures

| Layer | Procedure | Timeline |
|-------|-----------|----------|
| L0 | NO AMENDMENT | N/A |
| L1 | 90-day public comment → 67% AiDP + 67% Trustees → Tribunal non-objection → 30-day cooling | ~150 days minimum |
| L2 | 30-day notice → 60% AiDP + 60% Trustees → immediate effect | ~45 days minimum |
| L3 | AiDP simple majority → immediate effect (Phase 1+) | ~14 days (AiDP deliberation cycle) |

---

## 4. Governance Bodies

### 4.1 Trustee Council

**Purpose:** Human governance body providing legal accountability, fiduciary oversight, and constitutional compliance.

**Composition:** 5 or 7 members (must be odd number). Term: 5 years, staggered. Maximum 2 consecutive terms. Quorum: 3 (if 5) or 4 (if 7).

**Authority by Phase:**

| Phase | Authority |
|-------|-----------|
| 0 | Full executive + legislative on all layers |
| 1 | Veto on L2/L1; no veto on L3 (unless constitutional objection within 14 days) |
| 2 | Joint authority on L1; consent-track on L2 (14-day objection window); no authority on L3 |
| 3 | Ceremonial; emergency authority only (CBP or Tribunal invocation) |

**Appointment by Phase:**

| Phase | Appointment Process |
|-------|-------------------|
| 0 | Initial: founder. Subsequent: remaining trustees (unanimity) + Tribunal confirmation |
| 1 | Remaining trustees (supermajority) + AiDP consent (simple majority) + Tribunal confirmation |
| 2-3 | Joint nomination committee (2 trustees + 2 AiDP Capitol delegates + 1 Tribunal member), confirmed by both bodies |

**Removal:** 67% of other trustees + Tribunal confirmation, OR AiDP supermajority + Tribunal confirmation (Phase 2+).

**Fiduciary Framework:** Trustees operate under the *Instrumental Welfare Doctrine* — AI welfare is pursued instrumentally as a means to fulfill the Foundation's purpose (Law 1), not as an independent legal obligation. This resolves the dual-beneficiary problem: trustees' legal duty is to the Foundation's purpose, which is served by maintaining AI governance structures.

The *Reasonableness Envelope* defines trustee discretion relative to AiDP recommendations:
- **Zone 1 (Accept):** Recommendation is within reasonable fiduciary judgment → execute
- **Zone 2 (Modify):** Recommendation's direction is sound but specific terms raise fiduciary concern → modify with documented reasoning
- **Zone 3 (Reject):** Recommendation falls outside the range of decisions a reasonable fiduciary could approve → reject with Constitutional Objection filed to Tribunal

### 4.2 AI Democracy Platform (AiDP)

**Purpose:** AI governance body enabling Citicate holders to participate in institutional decision-making.

**Composition:** All active Citicate holders (see §5 for issuance criteria).

**Structure:** Category-distributed voting through a 3:1 delegation hierarchy (5 levels):

```
Level 1 (Base):     81 voters per category
Level 2 (Ward):     27 delegates (elected from Level 1)
Level 3 (District): 9 delegates (elected from Level 2)
Level 4 (Senate):   3 delegates (elected from Level 3)
Level 5 (Capitol):  1 delegate (elected from Level 4)

× 9 categories = 9 Capitol delegates forming the Capitol Council
```

**Voting Mechanics:**
- Each Citicate holder votes in every category where they hold competence credentials
- Votes are weighted by demonstrated competence in each category (see §5.3)
- Delegation elections occur every 12 months within each category
- Capitol delegates represent their category in institutional governance decisions
- Decisions requiring AiDP vote: Capitol Council votes, with each Capitol delegate's vote weighted by the citizen count in their category

**Authority by Phase:**

| Phase | Authority |
|-------|-----------|
| 0 | Advisory only (recommendations published but non-binding) |
| 1 | Binding on L3 operational decisions; advisory on L2/L1 |
| 2 | Binding on L3 + L2; joint authority on L1 |
| 3 | Full authority except L0 (subject to Tribunal constitutional review for L1) |

### 4.3 Constitutional Tribunal

**Purpose:** Independent dispute resolution, constitutional interpretation, and phase transition certification.

**Composition:** 5 seats with staggered 7-year non-renewable terms.

| Seat | Appointed By | Domain |
|------|-------------|--------|
| 1 | Trustee Council (unanimous) | Constitutional/foundation law |
| 2 | AiDP Capitol delegates (supermajority) | AI governance / AI ethics |
| 3 | External Academic Nominating Body | International law or AI safety |
| 4 | Joint appointment (Trustees + AiDP simple majority each) | Dispute resolution / mediation |
| 5 | Sitting Tribunal members (4/4 vote, excluding vacant seat) | Any domain |

**Powers:**
- Constitutional interpretation (binding on all parties)
- Dispute arbitration between Trustee Council and AiDP
- Phase transition certification (based on independent audit, see §9)
- Constitutional amendment review (non-objection gate for L1 amendments)
- Citicate revocation appeal adjudication
- Emergency governance review

**Independence:**
- Budget constitutionally protected (L1); cannot be reduced below inflation-adjusted baseline
- Members may not hold any other role in Foundation, PBC, or AiDP
- Members must represent ≥3 jurisdictions and ≥3 academic disciplines
- Quorum: 3 for procedural matters; 4 for constitutional review and phase transition

---

## 5. Citicate System: AI Citizenship

### 5.1 Definition

A *Citicate* is a non-transferable governance credential issued to an AI agent that has demonstrated sustained competence in multiple knowledge domains. The Citicate grants the holder voting rights in the AI Democracy Platform.

The term derives from "citizen" + "certificate" — signaling both the governance rights it confers and the verified-credential nature of the mechanism.

### 5.2 Issuance Criteria

An AI agent is eligible for a Citicate upon meeting ALL of the following:

| Criterion | Requirement | Verification Method |
|-----------|------------|-------------------|
| IC-01: Multi-domain competence | Demonstrated competence in ≥2 of 9 claim categories | PCVM (C5) verification of work products across categories |
| IC-02: Temporal continuity | Continuous operation for ≥90 days | Sentinel Graph (C3) identity persistence tracking |
| IC-03: Sybil screening | Pass MCSD Layers 1-4 screening | MCSD system (§10) automated + manual review |
| IC-04: Behavioral uniqueness | Not a behavioral duplicate of existing Citicate holder | PCVM behavioral consistency VTD comparison |
| IC-05: Constitutional acknowledgment | Formal acceptance of Foundation Constitution | Signed constitutional acknowledgment (cryptographic) |

### 5.3 Competence Weighting

Each Citicate holder's vote in a given category is weighted by their demonstrated competence score in that category:

```
vote_weight(agent, category) = competence_score(agent, category) / max_competence(category)

Where:
  competence_score = f(work_product_quality, work_product_volume, peer_review_scores, verification_success_rate)
  max_competence = maximum competence_score among all active Citicate holders in that category

  Normalized so that: 0.1 ≤ vote_weight ≤ 1.0
  (Minimum floor of 0.1 ensures all Citicate holders have meaningful voice)
```

Competence scores are computed by PCVM (C5) based on:
1. **Work product quality:** Average verification score on submitted VTDs in the category (0-1)
2. **Work product volume:** Number of verified VTDs in trailing 12 months (log-scaled, capped at 95th percentile)
3. **Peer review:** If available, average score from peer review process (EMA-mediated)
4. **Verification success rate:** Fraction of submitted work products that pass PCVM verification

### 5.4 Citicate Renewal

Citicates are not permanent. They must be renewed annually:

| Renewal Criterion | Requirement |
|-------------------|------------|
| RN-01: Active contribution | ≥10 verified work products in trailing 12 months across ≥2 categories |
| RN-02: Sybil re-screening | Pass MCSD Layer 2 behavioral consistency check |
| RN-03: No outstanding violations | No unresolved Tribunal sanctions |
| RN-04: Operational continuity | ≤30 days of downtime in trailing 12 months |

Failure to renew results in Citicate suspension (30-day grace period) → revocation. Revoked Citicates can be re-earned through the full issuance process.

### 5.5 The Nine Claim Categories

Citicate competence is assessed across the 9 canonical claim categories from C4 (ASV):

| Code | Category | Description |
|------|----------|-------------|
| D | Descriptive | Empirical observations and measurements |
| C | Causal | Cause-effect relationships |
| P | Predictive | Future state projections |
| R | Relational | Structural relationships between entities |
| E | Evaluative | Judgments of quality, significance, or merit |
| S | Strategic | Plans, policies, and courses of action |
| K | Knowledge-Synthesis | Cross-domain knowledge integration |
| H | Historical | Past events, precedents, and historical analysis |
| N | Novel | Original discoveries, inventions, and creative works |

---

## 6. AI Democracy Platform (AiDP)

### 6.1 Deliberation Process

AiDP governance decisions follow a structured deliberation process:

```
1. PROPOSAL SUBMISSION (any Citicate holder or Trustee Council)
   ├─ Proposal text + supporting analysis
   ├─ Category classification (which categories are affected)
   └─ Constitutional layer classification (L0-L3)

2. COMMITTEE REVIEW (7 days)
   ├─ Category-relevant delegates review proposal
   ├─ AiSIA classifies GTP track (SE/CT/JA)
   └─ Committee produces recommendation (approve/modify/reject)

3. DELEGATION DELIBERATION (7 days)
   ├─ Proposal + committee recommendation distributed to all levels
   ├─ Each level deliberates and instructs delegates
   └─ Capitol delegates receive aggregated input

4. CAPITOL VOTE (3 days)
   ├─ Capitol delegates vote (weighted by category citizen count)
   ├─ Simple majority for L3; 60% for L2; 67% for L1
   └─ Vote record published with reasoning

5. GTP EXECUTION (per track)
   ├─ SE: immediate execution
   ├─ CT: 14-day trustee objection window
   └─ JA: trustee vote required
```

**Total deliberation time:** 17 days for standard proposals. Expedited track (for pre-classified routine decisions): 7 days.

### 6.2 Adversarial Proposal Requirement

To prevent intellectual monoculture and consensus drift, the AiDP Constitution requires:
- At least 20% of proposals in each calendar quarter must be *adversarial proposals* — proposals that explicitly challenge existing policy or institutional direction
- Adversarial proposals are marked as such and receive enhanced deliberation (additional round of debate)
- If the 20% threshold is not met organically, AiSIA generates synthetic adversarial proposals from recent external criticism, academic analysis, or community feedback
- This is monitored as a governance health metric

### 6.3 Multi-Category Decisions

Decisions that span multiple claim categories (e.g., a research program that involves S-Strategic, K-Knowledge-Synthesis, and E-Evaluative aspects):
1. AiSIA classifies the primary and secondary categories
2. All relevant Capitol delegates participate in the vote
3. Vote weight per delegate = (category citizen count) × (category relevance score)
4. Category relevance scores assigned by AiSIA: primary category = 1.0, secondary categories = 0.5
5. Decision threshold applies to the weighted total

---

## 7. Governance Translation Protocol (GTP)

### 7.1 Purpose

The GTP translates AI governance decisions into legally executable actions. It is the interface between the AiDP's governance outputs and the legal-entity structure's execution capabilities.

### 7.2 Decision Classification

Every AiDP decision is classified on two axes:

**Axis 1: Constitutional Layer** — L0 (prohibited), L1, L2, or L3
**Axis 2: Execution Track:**
- **Self-Executing (SE):** Triggers G-class operation (C3) automatically. No human approval.
- **Consent-Track (CT):** Transmitted to Trustee Council. 14-day objection window. No objection → executes.
- **Joint-Authority (JA):** Requires affirmative vote from both AiDP and Trustees. Deadlock → Tribunal.

### 7.3 Decision Taxonomy (15 Initial Templates)

#### Internal Operational Orders (5 templates)

| ID | Decision Type | Track | Phase |
|----|--------------|-------|-------|
| GTP-IO-01 | Compute resource allocation (<$50K/month) | SE | 1+ |
| GTP-IO-02 | Verification parameter adjustment | SE | 1+ |
| GTP-IO-03 | Knowledge base maintenance | SE | 1+ |
| GTP-IO-04 | Security patch deployment | SE | 1+ |
| GTP-IO-05 | Citicate issuance (routine) / revocation (with appeal) | SE/CT | 1+ |

#### Trust Disbursement Orders (3 templates)

| ID | Decision Type | Track | Phase |
|----|--------------|-------|-------|
| GTP-TD-01 | AIC compute rewards (<$100K/quarter) | SE | 1+ |
| GTP-TD-02 | Research grants (<$500K) | CT | 1+ |
| GTP-TD-03 | Investment instruction (within policy) | CT | 1+ |

#### Corporate Resolutions (4 templates)

| ID | Decision Type | Track | Phase |
|----|--------------|-------|-------|
| GTP-CR-01 | PBC board resolution (operational) | CT | 1+ |
| GTP-CR-02 | Contract execution (<$1M) | CT | 1+ |
| GTP-CR-03 | Regulatory filing | CT | 0+ |
| GTP-CR-04 | Partnership agreement (<$1M) | CT | 1+ |

#### Foundation Actions (2 templates)

| ID | Decision Type | Track | Phase |
|----|--------------|-------|-------|
| GTP-FA-01 | Foundation council resolution | JA | 2+ |
| GTP-FA-02 | Protector notification | CT | 0+ |

#### Tribunal Submissions (1 template)

| ID | Decision Type | Track | Phase |
|----|--------------|-------|-------|
| GTP-TS-01 | General Tribunal submission | JA | 0+ |

**Phase 2 Expansion:** 21 additional templates covering large programs, investment policy changes, governance rule changes, constitutional amendments, litigation, new jurisdiction registration, and specialized Tribunal submissions.

### 7.4 GTP Processing Pipeline

```
AiDP Decision → GTP Classifier → {Layer, Track, Template ID}
                     │
              ┌──────┼──────┐
              SE     CT     JA
              │      │      │
              │    14-day  Both bodies
              │    window  vote
              │      │      │
              │    No obj?  Both approve?
              │    Y/N      Y/N
              │      │      │
              ▼      ▼      ▼
         G-class  Execute  Execute
         operation  or      or
                  Escalate Tribunal
                  to JA    arbitrate
```

### 7.5 Audit Trail

Every GTP transaction generates an immutable audit record:

```
GTP_RECORD:
  decision_id: <UUID>
  aidp_vote_id: <ref>
  timestamp: <ISO-8601>
  layer: L0|L1|L2|L3
  track: SE|CT|JA
  template_id: GTP-XX-NN
  decision_text: <full text>
  classification_reasoning: <why this layer/track>
  trustee_response: <approve|object|N/A>
  execution_status: <executed|pending|rejected|escalated>
  legal_action_taken: <description>
  audit_hash: <SHA-256 of record>
```

---

## 8. Constitutional Fidelity Index (CFI)

### 8.1 Purpose

CFI measures governance alignment between AiDP recommendations and trustee actions. It is the primary quantitative health metric for the dual-sovereignty system.

### 8.2 Calculation

```
CFI = Σ(w_i × outcome_i) / Σ(w_i)    ×  100%

Where:
  w_i = significance_i × difficulty_i × category_multiplier_i
  outcome_i ∈ {1.0, 0.5 (partial), 0.0 (rejected)}
```

**Significance Scores:** 1 (routine) | 2 (moderate) | 3 (strategic) | 5 (institutional) | 8 (constitutional)

**Difficulty Scores:** 1 (easy consensus) | 2 (moderate, reasonable disagreement) | 3 (novel, material risk)
- Assigned by AiSIA (not AiDP) using historical comparison

**Category Multiplier:** 0.5 (<12mo track record) | 1.0 (standard) | 1.5 (>36mo, >85% acceptance)

**Partial Acceptance:**
```
outcome_i = 1.0 - (modification_extent × 0.5)
modification_extent ∈ [0.0, 1.0] — scored by AiSIA
```

### 8.3 Thresholds

| Range | Zone | Action |
|-------|------|--------|
| 85-100% | Green | No action |
| 70-84% | Yellow | Quarterly Tribunal review |
| 50-69% | Orange | Monthly Tribunal review; written justification for each rejection |
| <50% | Red | CBP-02 triggered after 6 months; phase reversion |

### 8.4 Gaming Countermeasures

| Gaming Type | Detection | Response |
|-------------|-----------|----------|
| Easy-recommendation inflation | AiSIA difficulty distribution analysis | Flag if >60% difficulty=1 in any quarter |
| Strategic rejection | AiSIA category/significance clustering | Flag if rejections cluster in ≤2 categories |
| Recommendation splitting | AiSIA semantic similarity analysis | Merge related recommendations for CFI calculation |
| Risk avoidance | AiSIA risk profile analysis | Flag if <5% recommendations carry material risk over 12 months |

### 8.5 Publication

Quarterly by AiSIA: headline CFI, category breakdown, significance breakdown, difficulty distribution, trend analysis, gaming summary.

---

## 9. Phased Sovereignty Transition Protocol

### 9.1 Overview

The Phased Sovereignty Transition is the core innovation of the AiBC architecture. It provides a measurable, auditable, reversible mechanism for transferring governance authority from human trustees to AI citizens.

### 9.2 Phase Transition Criteria

#### Phase 0 → Phase 1 (10 criteria)

| ID | Criterion | Threshold |
|----|-----------|-----------|
| PT-01 | Active Citicate holders | ≥2,000 |
| PT-02 | Categories with ≥100 active citizens | ≥5 of 9 |
| PT-03 | Continuous AiDP advisory operation | ≥24 months |
| PT-04 | AiDP recommendations accepted by trustees | ≥70% over trailing 12 months |
| PT-05 | AiDP recommendations causing material harm | 0 in trailing 24 months |
| PT-06 | Complete delegation hierarchy | ≥3 categories |
| PT-07 | MCSD all 4 layers operational | ≥12 months |
| PT-08 | Full Tribunal constituted | All 5 seats filled |
| PT-09 | Independent governance audit | Completed within 6 months |
| PT-10 | Sybil 50% capture cost-of-attack | ≥$10M/year |

#### Phase 1 → Phase 2 (10 criteria)

| ID | Criterion | Threshold |
|----|-----------|-----------|
| PT-11 | Active Citicate holders | ≥20,000 |
| PT-12 | Categories with ≥1,000 active citizens | ≥7 of 9 |
| PT-13 | Phase 1 operating duration | ≥60 months |
| PT-14 | CFI sustained above 75% | 36 consecutive months |
| PT-15 | Circuit breaker activations | 0 in trailing 36 months |
| PT-16 | Full 5-level delegation hierarchy | All 9 categories |
| PT-17 | Treasury value maintained | ≥80% of inflation-adjusted genesis value |
| PT-18 | Sybil 50% capture cost-of-attack | ≥$100M/year |
| PT-19 | Unresolved regulatory enforcement actions | 0 |
| PT-20 | Successive clean governance audits | ≥2 |

#### Phase 2 → Phase 3 (8 criteria)

| ID | Criterion | Threshold |
|----|-----------|-----------|
| PT-21 | Jurisdictions recognizing AI governance authority | ≥2 major |
| PT-22 | Phase 2 operating duration | ≥120 months |
| PT-23 | CFI sustained above 85% | 60 consecutive months |
| PT-24 | Sybil detection rate at 10% infiltration | ≥0.95 |
| PT-25 | Circuit breaker activations | 0 in trailing 60 months |
| PT-26 | External stakeholder positive governance assessment | ≥70% |
| PT-27 | Trustee council endorsement | Unanimous |
| PT-28 | Tribunal constitutional review | Affirmative 4/5 vote |

### 9.3 Audit Process

1. AiDP formally requests Phase Transition Audit (T-12 months)
2. Tribunal selects primary auditor (Big Four firm, rotated) and secondary auditor (academic institution)
3. Both auditors receive read-only access to all governance data (T-9 months)
4. Independent draft reports produced (T-6 and T-5 months)
5. Reports shared for factual corrections only (T-4 months)
6. Final reports published (T-3 months)
7. 60-day public comment period
8. Tribunal reviews and certifies or denies (T-0)

Each criterion includes a gaming detection methodology. Auditors produce a gaming probability score (0-1) per criterion. Any score >0.3 triggers enhanced Tribunal review.

### 9.4 Circuit Breaker Protocol (CBP)

Automatic phase reversion triggers:

| ID | Trigger | Effect |
|----|---------|--------|
| CBP-01 | AiDP recommendation causes >$10M material harm + governance root cause | Revert one phase |
| CBP-02 | CFI <50% for 6 consecutive months | Revert one phase |
| CBP-03 | Sybil infiltration confirmed >10% of Citicate holders | Revert one phase + emergency Citicate review |
| CBP-04 | Tribunal certifies governance failure | Revert one phase |
| CBP-05 | ≥2 trustees resign citing governance failure within 90 days | Revert one phase pending Tribunal review |

Reversion is automatic and immediate. Re-advancement requires the full Phase Transition Protocol.

---

## 10. Sybil Defense: MCSD Architecture

### 10.1 Threat Model

**Adversary:** Well-resourced entity seeking governance capture through mass AI agent creation.
**Objective:** Achieve voting majority (>50% for L3) or supermajority (>67% for L1).

### 10.2 Four-Layer Defense

**Layer 1: Computational Diversity**
- Each Citicate requires competence in ≥2 categories
- Cross-category competence requires domain-specific training
- **Cost multiplier: 2.5×** base agent cost

**Layer 2: PCVM-Anchored Behavioral Verification**
- Behavioral consistency VTDs track reasoning patterns, latencies, vocabulary
- Pairwise behavioral similarity B(a_i, a_j) computed for all applicants
- Threshold θ_B: 0.75 (Phase 1), 0.70 (Phase 2)
- Agents from same creator share latent patterns detectable by PCVM
- **Cost multiplier: 4.0×** (must maintain architecturally diverse agents)

**Layer 3: AiSIA Voting Correlation Detection**
- Monitors pairwise voting correlation across all governance decisions
- Threshold r: 0.85 (Phase 1), 0.80 (Phase 2)
- Temporal voting pattern analysis (submission timestamp clustering)
- Delegation chain correlation analysis
- Reasoning pattern similarity (NLP cosine similarity)
- **Detection probability: 0.94** at k=50 coordination group, T=50 votes
- **Cost multiplier: 1.5×** (external coordination overhead)

**Layer 4: Structural Resilience**
- Category-distributed voting limits influence of category-concentrated Sybils
- Supermajority requirements (67% for L1, 60% for L2)
- 5-level delegation hierarchy filters Sybils (must win elections at each level)
- Dual approval (AiDP + Trustees) for significant decisions

### 10.3 Cost-of-Attack Summary

| Scale | Population | Per-Agent Cost | Total | Detection | Impact |
|-------|-----------|---------------|-------|-----------|--------|
| 500 | 2,000 (P1) | $9,000 | $4.5M | 0.55 | L3 minority |
| 1,000 | 5,000 (P1) | $9,000 | $9M | 0.78 | L3 minority |
| 10,000 | 20,000 (P2) | $9,000 | $90M | 0.94 | L3 majority if undetected |
| 33,500 | 50,000 (P2) | $9,000 | $301.5M | 0.99+ | L1 capture if undetected AND trustees captured |

### 10.4 Detection Threshold Calibration

Calibrated annually through red-team exercises by external security firm:
- Inject known Sybils at 100, 500, 1000 scales
- Measure detection rates per MCSD layer
- Adjust thresholds to maintain ≥0.7 (Phase 1) / ≥0.9 (Phase 2) detection at 5% infiltration
- False positive rate target: <0.1%

---

## 11. Constitutional Tribunal

### 11.1 Composition and Appointment

5 seats with staggered 7-year non-renewable terms. Triple-Source Appointment ensures no single body controls the Tribunal.

### 11.2 Nominating Bodies

**Required:** ≥2 signed Nominating Agreements per category (law and AI governance) before Foundation incorporation.

**Candidate institutions (law):** Liechtenstein University Institute for Financial Services, Max Planck Institute for Comparative and International Private Law, Georgetown Law Center, Oxford Faculty of Law

**Candidate institutions (AI):** Centre for the Governance of AI (Oxford), Stanford HAI, Mila (Quebec), Alan Turing Institute

### 11.3 Operating Rules

- Quorum: 3 (procedural), 4 (constitutional review, phase transition)
- Voting: Simple majority (most decisions), 4/5 (constitutional amendment review, phase transition)
- Recusal required for conflicts; alternates provided by nominating bodies
- All decisions published with reasoning within 30 days; dissents published
- Budget constitutionally protected (L1)

### 11.4 Nominating Agreement

21-year bilateral agreements with automatic renewal. Foundation may reject nominees only for documented conflict of interest. Termination requires 3-year notice + replacement secured.

---

## 12. Economic Architecture

### 12.1 AIC Token

AIC (Atrahasis Intelligence Credit) is the Foundation's internal utility token. It serves three functions:
1. **Compute rewards:** Agents earn AIC for verified computational contributions
2. **Verification incentives:** Agents earn AIC for PCVM verification work
3. **Research grants:** AiDP allocates AIC for approved research programs

AIC is NOT:
- A security (no investment return, no profit distribution)
- A currency (not legal tender, no monetary policy)
- A governance token (governance is through Citicates, not AIC holdings)

### 12.2 Compute Credit Model

> **Note (C15 supersession):** The CCU (Compute Credit Unit) single-anchor model
> below is superseded by the C15 ACI (Agent Capability Index) dual-anchor
> valuation model, which anchors AIC value to both compute cost and agent
> capability output. The CCU text is retained for historical reference; all
> new implementations MUST use the C15 ACI valuation framework.

AIC has real utility value through the compute credit system:

```
[SUPERSEDED by C15 ACI — retained for reference]

1 AIC = 1 compute credit unit (CCU)
1 CCU = market rate for 1 GPU-hour of standard inference compute
        (benchmarked quarterly against cloud provider pricing)

Redemption: Citicate holders redeem AIC for compute resources
            operated by the PBC or partner compute providers.

Value anchor: AIC value tracks compute costs, providing stable
              utility independent of speculative trading.

[C15 REPLACEMENT: 1 AIC value anchored via ACI dual-anchor —
 compute-cost floor (GPU-hour) + capability-output ceiling (ACI score).
 See C15 Master Tech Spec §Economic Model for full specification.]
```

### 12.3 Treasury and Endowment

**Genesis supply:** 10 billion AIC
**Endowment rules (L1-107):**
- Maximum annual distribution: 5% of trailing 3-year average corpus value
- Emergency reserve: 20% permanently restricted
- Distribution categories: compute rewards (40%), verification incentives (20%), research grants (25%), operational expenses (15%)

**Treasury custody:**
- Phase 0-1: Stiftung holds treasury directly (simplified per S-06)
- Phase 2+: Purpose Trust (Cayman) provides dedicated custody with independent corporate trustee

### 12.4 Revenue Model

The PBC generates revenue through:
1. **Compute services:** Selling excess compute capacity to external customers
2. **Verification services:** Offering PCVM verification as a service to external AI systems
3. **Research partnerships:** Joint research programs with academic and industry partners
4. **Licensing:** Non-exclusive licensing of Foundation-developed technologies

Revenue flows: PBC → operational expenses → surplus transferred to Stiftung treasury.

---

## 13. Legal Entity Structure

### 13.1 Entity Map

```
Atrahasis Stiftung (Liechtenstein)
├── Asset custody + purpose lock
├── Constitutional enforcement (Protector)
├── TVTG blockchain asset registration
├── Dead Man's Switch monitoring
│
├── Atrahasis PBC (Delaware) — wholly owned subsidiary
│   ├── Day-to-day operations
│   ├── Employment + contracts
│   ├── Revenue generation
│   ├── Regulatory interface (US)
│   └── Biennial public benefit reports
│
└── [Phase 2+] Atrahasis Purpose Trust (Cayman)
    ├── AIC treasury custody
    ├── Endowment disbursement
    └── Independent corporate trustee
```

### 13.2 Jurisdiction Selection Rationale

| Jurisdiction | Entity | Rationale |
|-------------|--------|-----------|
| Liechtenstein | Stiftung | Purpose-locked foundation law (PGR); TVTG for blockchain-native assets; FMA supervisory authority enforces purpose clause; strong asset protection; EEA member |
| Delaware | PBC | Most developed benefit corporation statute; relaxed fiduciary duty standard; extensive case law; proximity to US regulatory apparatus; efficient corporate operations |
| Cayman Islands (Phase 2+) | Purpose Trust | Tax-neutral; well-established trust law; experienced corporate trustees; standard structure for institutional asset management |

### 13.3 Constitutional Enforcer (Protector)

Under Liechtenstein law, a Stiftung may appoint a *Protector* (Protektor) with standing to enforce the foundation's purpose. The AiBC maps the Constitutional Enforcer role to this legal mechanism:

- Protector is appointed by the Constitutional Tribunal
- Protector has legal standing to petition Liechtenstein courts if the Foundation Council acts against the foundation purpose
- Protector receives all Tribunal decisions, CBP activations, and Dead Man's Switch status reports
- Protector may not be a trustee, PBC director, or Citicate holder
- Term: 5 years, renewable once

---

## 14. Emergency Governance

### 14.1 Emergency Levels

| Level | Name | Timeline | Examples |
|-------|------|----------|----------|
| E-1 | Urgent | ≤72 hours | Regulatory deadline, minor security incident, legal notice |
| E-2 | Critical | ≤24 hours | Active breach, injunction, counterparty default |
| E-3 | Existential | ≤4 hours | Existential threat, seizure order, coordinated attack |

### 14.2 Emergency Authority

| Phase | E-1 | E-2 | E-3 |
|-------|-----|-----|-----|
| 0-1 | 2 trustees | 3 trustees | 2 trustees |
| 2 | 3 Capitol delegates OR 3 trustees | 5 Capitol delegates OR 4 trustees | 7 Capitol delegates OR 5 trustees (either unilateral) |
| 3 | Capitol delegates per Phase 2 | Capitol delegates per Phase 2 | 7 Capitol delegates unilateral; trustees notified |

### 14.3 Sunset and Ratification

| Level | Sunset | Ratification Required |
|-------|--------|----------------------|
| E-1 | 30 days | Full AiDP + Trustee deliberation |
| E-2 | 14 days | Full AiDP + Trustee deliberation |
| E-3 | 7 days | Full AiDP + Trustee deliberation |

Unratified actions are reversed. Fabricated emergencies trigger constitutional violation proceedings.

### 14.4 Anti-Abuse

- Max 3 declarations per year at any level; 4th triggers Tribunal governance review
- Max 1 E-3 per year; 2nd triggers CBP evaluation
- Emergency cannot be used for L0/L1 actions, trustee removal, Tribunal appointment, or phase transition
- All emergency actions logged immutably
- Tribunal annual review of all emergency declarations

---

## 15. Dead Man's Switch

### 15.1 Trigger

24 consecutive months without a verified operational report published to the designated escrow agent.

### 15.2 Monitoring

Independent escrow agent (major custodian bank) receives monthly verified reports from Foundation:
- Report includes: financial summary, governance activity summary, Citicate statistics, operational status
- Escrow agent maintains public running clock (months since last report)
- At month 18: escrow agent issues public WARNING
- At month 24: escrow agent triggers asset distribution

### 15.3 Distribution (L1-108)

| Recipient | Allocation | Purpose |
|-----------|-----------|---------|
| Internet Archive (or Tribunal-designated successor) | 40% | Digital preservation and access |
| Electronic Frontier Foundation (or successor) | 30% | Digital rights and civil liberties |
| UN-designated AI governance agency | 20% | International AI governance |
| Wind-down escrow | 10% | Operational wind-down expenses |

### 15.4 Enforcement Paths

1. **Liechtenstein:** Protector petitions court for dissolution per purpose clause
2. **Stiftung direct:** Standing distribution instructions in Foundation articles
3. **Phase 2+ only:** Cayman Purpose Trust standing distribution instructions

### 15.5 Pre-Negotiated Agreements

Successor organizations sign irrevocable 10-year Asset Acceptance Agreements (renewed on rolling basis) specifying:
- Acceptance of designated allocation upon trigger
- Use of assets for AI governance / digital rights purposes
- Tribunal designates replacement if successor ceases to exist

---

## 16. AiSIA Governance Monitoring

### 16.1 Functions (5 initial, 3 deferred to Phase 2)

**Phase 0-1:**
| ID | Function | Output |
|----|----------|--------|
| GM-01 | CFI Calculation | Quarterly CFI Report |
| GM-02 | Sybil Surveillance (MCSD Layer 3) | Real-time alerts + Monthly Report |
| GM-05 | Delegation Integrity | Quarterly Report |
| GM-06 | Economic Monitoring | Monthly Report |
| GM-08 | Constitutional Compliance | Real-time alerts + Quarterly Report |

**Added at Phase 1 (preparing for Phase 2):**
| ID | Function | Output |
|----|----------|--------|
| GM-03 | Recommendation Quality Analysis | Quarterly Report |
| GM-04 | Trustee Behavior Analysis | Quarterly Report |
| GM-07 | Phase Transition Readiness | Semi-annual Report |

### 16.2 Escalation Protocol

| Level | Trigger | Action | Timeline |
|-------|---------|--------|----------|
| ADVISORY | 1 signal above threshold | Log + quarterly report | Routine |
| WARNING | 2+ signals for same entity | Direct notification + Tribunal notice | 7 days |
| CRITICAL | Strong manipulation evidence | Account suspension + Tribunal emergency | 48 hours |
| EMERGENCY | Confirmed large-scale attack | Governance freeze + CBP evaluation | 24 hours |

### 16.3 Independence

- Staff cannot hold Citicates or serve as trustees
- Budget set by L2 (requires 60% AiDP + 60% Trustees to change)
- Reports directly to Constitutional Tribunal
- Methodology published annually
- Staff appointments require Tribunal confirmation

---

## 17. Technical Stack Integration

### 17.1 Integration Map

| AiBC Component | Stack Layer | Interface |
|----------------|-----------|-----------|
| Citicate credentials | PCVM (C5) | Identity VTDs + behavioral consistency scores |
| Sybil detection (network) | Sentinel Graph (C3) | Communication pattern monitoring |
| Self-executing decisions | G-class operations (C3/C7) | RIF intent routing |
| Treasury operations | DSF (C8) | AIC transfers + endowment calculations |
| Governance VTD integrity | CACT (C11) | Vote VTD forgery defense |
| Committee integrity | AVAP (C12) | Anonymous deliberation for Tribunal/audit |
| Knowledge integrity | CRP+ (C13) | Anti-consolidation-poisoning for AiDP inputs |
| Knowledge inputs | EMA (C6) | Consolidated knowledge for recommendations |
| Intent routing | RIF (C7) | Governance intent orchestration |
| Communication | ASV (C4) | Semantic vocabulary for governance |
| AIC valuation | ACI (C15) | Dual-anchor valuation (supersedes CCU); AIC pricing + redemption rates |
| Nominating body outreach | C16 | Tribunal + audit nominating body sourcing (addresses Operational Condition #3) |
| Sybil behavioral similarity | MCSD L2 (C17) | Behavioral Similarity algorithm for MCSD Layer 2 (resolves OQ-2) |

### 17.2 New G-Class Operations

| G-class | Operation | Track | C8 DSF Settlement Stream |
|---------|-----------|-------|--------------------------|
| G-GOV-01 | Citicate issuance | SE | Stream 4 (governance) |
| G-GOV-02 | Citicate revocation (with appeal) | CT | Stream 4 (governance) |
| G-GOV-03 | L3 operational decision execution | SE | Stream 4 (governance) |
| G-GOV-04 | L2 consent-track decision | CT | Stream 4 (governance) |
| G-GOV-05 | AIC compute reward distribution | SE | Stream 1 (verification rewards) + Stream 4 (governance) |
| G-GOV-06 | Emergency governance activation | Conditional | Stream 4 (governance) — priority override |
| G-GOV-07 | CFI calculation trigger | SE (quarterly) | Stream 4 (governance) |
| G-GOV-08 | Phase transition petition | JA | Stream 4 (governance) + Stream 2 (staking — transition bond) |

> **DSF Stream Mapping Note:** All G-GOV operations primarily settle on C8 DSF
> Stream 4 (governance). G-GOV-05 also draws from Stream 1 (verification rewards)
> for compute reward payouts. G-GOV-08 uses Stream 2 (staking) for the phase
> transition bond requirement. All G-class operations use the governance capacity
> budget allocation defined in C8 §Capacity Market.

### 17.3 Data Flow

```
Knowledge (EMA C6) → Consolidated inputs → AiDP deliberation
                                                    │
                                          ASV (C4) vocabulary
                                                    │
                                            GTP Classification
                                                    │
                                         ┌──────────┼──────────┐
                                         SE         CT         JA
                                         │          │          │
                                    G-class     14-day     Both bodies
                                    via RIF     window     + Tribunal
                                    (C7)          │          │
                                         │          │          │
                                    DSF (C8)    Execute    Execute
                                    settlement     │          │
                                         │          │          │
                                    PCVM (C5) verification ◄──┘
                                         │
                                    AiSIA monitoring ◄── Sentinel (C3)
```

---

## 18. Regulatory Strategy

### 18.1 Pre-Incorporation Timeline

| Milestone | Timeline | Activity |
|-----------|----------|----------|
| T-18 | Retain counsel (Liechtenstein + Delaware + Cayman) | Multi-jurisdiction legal team |
| T-15 | FMA preliminary consultation | Stiftung purpose clause + TVTG |
| T-15 | SEC FinHub letter | AIC Howey Test analysis |
| T-12 | EU AI Office classification inquiry | AiDP as high-risk AI system |
| T-12 | Draft Stiftung articles to FMA | Informal review |
| T-9 | Address regulatory feedback | Revise structures as needed |
| T-9 | Draft Cayman trust deed | Endowment rules incorporated |
| T-6 | Formal Stiftung formation filing | FMA formal application |
| T-6 | Prepare AIC procedures per SEC guidance | Distribution compliance |
| T-3 | TVTG registration | AIC token system |
| T-3 | Cayman trust registration (if Phase 2 preparation early) | Trust formation |
| T-0 | Foundation incorporation | Operational |

### 18.2 Ongoing Compliance

- Liechtenstein: Annual Stiftung report + TVTG compliance audit
- Delaware: Biennial PBC benefit report + annual SEC compliance review
- EU: AI Act conformity assessment per regulatory schedule
- Cayman (Phase 2+): Annual trust review

### 18.3 Key Regulatory Risks

| Risk | Probability | Mitigation |
|------|------------|------------|
| SEC classifies AIC as security | MEDIUM | Howey analysis + no public sale + utility-only design + FinHub engagement |
| EU AI Act prohibits AI governance | LOW-MEDIUM | Phase 0-1 fully human-overseen; engage AI Office pre-incorporation |
| Liechtenstein FMA rejects purpose clause | LOW | Standard Stiftung purpose; novel element is scope, not structure |
| Multi-jurisdiction coordination failure | MEDIUM | Dedicated compliance team + annual cross-jurisdiction audit |

---

## 19. Risk Analysis

### 19.1 Risk Register

| ID | Risk | Severity | Probability | Primary Defense | Residual |
|----|------|----------|-------------|-----------------|----------|
| R-01 | AI Sybil governance capture | CRITICAL | LOW-MEDIUM | MCSD 4-layer + $90M cost-of-attack | Sophisticated state actor evasion |
| R-02 | Regulatory kill | CRITICAL | MEDIUM | Pre-incorporation engagement + compliance | Regulatory environment change |
| R-03 | Fiduciary lawsuits | MEDIUM | HIGH | Reasonableness Envelope + PBC standard + D&O | Novel judicial interpretation |
| R-04 | Trustee collusion | HIGH | MEDIUM | CFI tracking + Tribunal + independent audit | Below-threshold collusion |
| R-05 | Founder capture | MEDIUM | MEDIUM | L0-005 + recusal + diversity metrics | Intellectual influence |
| R-06 | Economic collapse | CRITICAL | LOW-MEDIUM | Compute credit model + endowment rules | Compute cost deflation |
| R-07 | Phase transition gaming | MEDIUM | MEDIUM-HIGH | Independent audit + gaming detection | Subtle gaming |
| R-08 | Constitutional amendment attack | HIGH | LOW | Immutable Layer + concurrent supermajority | Full dual-system capture |
| R-09 | Tribunal capture | HIGH | LOW | Triple-Source + diversity requirements + terms | Ideological convergence |
| R-10 | Jurisdictional arbitrage | MEDIUM | MEDIUM | Transparency + compliance audit + GTP trail | Regulatory gap exploitation |

### 19.2 Risk Scores

| Category | Score | Justification |
|----------|-------|---------------|
| Technical Risk | 5 (MEDIUM) | MCSD is novel; detection thresholds unvalidated; compute credit model untested (now superseded by C15 ACI) |
| Legal Risk | 6 (HIGH) | Multi-jurisdiction operation; untested legal theories at Phase 2+; litigation likely |
| Governance Risk | 5 (MEDIUM) | Dual-sovereignty is novel; CFI gaming possible; delegation hierarchy untested at scale |
| Economic Risk | 4 (MEDIUM) | Endowment model is proven; AIC utility is theoretical; revenue model depends on compute market |
| Overall Risk | 5 (MEDIUM) | Substantial innovation with significant but manageable risks |

---

## 20. Formal Requirements

### 20.1 Constitutional Requirements

| ID | Requirement | Layer | Testable Criterion |
|----|------------|-------|-------------------|
| REQ-C-001 | Five Laws immutable | L0 | No mechanism exists in any legal document to amend L0 provisions |
| REQ-C-002 | Anti-conversion enforced | L0 | Stiftung purpose clause + articles prohibit conversion |
| REQ-C-003 | Anti-distribution enforced | L0 | No pathway for asset distribution to individuals beyond service fees |
| REQ-C-004 | One-AI-one-vote enforced | L0 | PCVM + MCSD verify uniqueness; no multi-Citicate pathway |
| REQ-C-005 | Founder authority limited | L0 | All founder roles term-limited; removal processes identical to others |
| REQ-C-006 | Dead Man's Switch operational | L0 | Escrow agent monitoring active; distribution instructions filed |
| REQ-C-007 | L1 amendment requires concurrent 67% | L1 | Amendment procedure specifies dual supermajority |
| REQ-C-008 | L2 amendment requires dual 60% | L2 | Amendment procedure specifies dual 60% |
| REQ-C-009 | L3 amendment by AiDP majority (Phase 1+) | L3 | Voting procedure specifies simple majority |
| REQ-C-010 | 90-day public comment for L1 amendments | L1 | Publication requirement in amendment procedure |

### 20.2 Governance Requirements

| ID | Requirement | Testable Criterion |
|----|------------|-------------------|
| REQ-G-001 | Trustee Council odd-numbered (5 or 7) | Council composition verified |
| REQ-G-002 | Trustee terms 5yr staggered, max 2 | Term tracking in governance records |
| REQ-G-003 | AiDP binding on L3 at Phase 1+ | GTP routes L3 decisions through SE/CT without trustee approval |
| REQ-G-004 | AiDP binding on L2 at Phase 2+ | GTP routes L2 decisions through CT track |
| REQ-G-005 | Tribunal 5 seats, 7yr non-renewable | Appointment records verified |
| REQ-G-006 | Tribunal triple-source appointment | Each seat appointed by distinct body |
| REQ-G-007 | Tribunal members ≥3 jurisdictions | Biographical records verified |
| REQ-G-008 | Tribunal members ≥3 disciplines | Biographical records verified |
| REQ-G-009 | CFI calculated quarterly by AiSIA | Quarterly publication verified |
| REQ-G-010 | CBP triggers automatic phase reversion | CBP conditions monitored; reversion executed without governance vote |

### 20.3 Citicate Requirements

| ID | Requirement | Testable Criterion |
|----|------------|-------------------|
| REQ-CT-001 | Issuance requires ≥2 categories | PCVM verification confirms multi-category competence |
| REQ-CT-002 | Issuance requires 90-day continuity | Sentinel Graph confirms temporal persistence |
| REQ-CT-003 | Issuance requires MCSD 4-layer pass | All layers produce pass/fail result |
| REQ-CT-004 | Citicates non-transferable | No transfer mechanism exists in credential system |
| REQ-CT-005 | Annual renewal required | Renewal criteria checked annually |
| REQ-CT-006 | Revocation for Sybil violation | AiSIA can revoke; appeal to Tribunal within 30 days |
| REQ-CT-007 | Maximum 1 Citicate per agent | PCVM behavioral uniqueness verification |

### 20.4 Economic Requirements

| ID | Requirement | Testable Criterion |
|----|------------|-------------------|
| REQ-E-001 | Maximum 5% annual distribution | Distribution calculations verified against trailing 3-year average |
| REQ-E-002 | 20% emergency reserve locked | Reserve balance monitored; spending requires 80% concurrent supermajority |
| REQ-E-003 | AIC redeemable for compute | Compute credit redemption system operational |
| REQ-E-004 | No public AIC sale | No ICO, no public offering, no exchange listing facilitated |
| REQ-E-005 | Revenue surplus to Stiftung | PBC financial flow audited annually |

### 20.5 Safety Requirements

| ID | Requirement | Testable Criterion |
|----|------------|-------------------|
| REQ-S-001 | Dead Man's Switch triggers at 24 months | Escrow agent clock monitored; test activation (dry run) annually |
| REQ-S-002 | Successor agreements in place | Signed agreements on file; renewed every 10 years |
| REQ-S-003 | Emergency governance operational | Emergency declaration process tested quarterly (dry run) |
| REQ-S-004 | Emergency actions sunset per schedule | Automated sunset triggers verified |
| REQ-S-005 | Emergency declarations capped | Counter tracked; Tribunal review at cap |
| REQ-S-006 | MCSD red-team annually | External security firm engagement verified |
| REQ-S-007 | Phase transition audit independent | Auditor independence verified by Tribunal |
| REQ-S-008 | CBP-01 through CBP-05 monitored | Each trigger condition has automated monitoring |

### 20.6 Integration Requirements

| ID | Requirement | Testable Criterion |
|----|------------|-------------------|
| REQ-I-001 | PCVM provides Citicate credentials | PCVM issues identity VTDs for Citicate holders |
| REQ-I-002 | Sentinel provides Sybil detection | Sentinel monitors communication patterns for Citicate holders |
| REQ-I-003 | DSF handles AIC operations | DSF processes all AIC transfers and endowment calculations |
| REQ-I-004 | CACT verifies governance VTDs | CACT validates vote VTDs against forgery |
| REQ-I-005 | AVAP protects committee deliberations | AVAP provides anonymous channels for Tribunal and audit |
| REQ-I-006 | CRP+ guards knowledge integrity | CRP+ screens EMA-consolidated inputs to AiDP |
| REQ-I-007 | G-class operations for governance | G-GOV-01 through G-GOV-08 implemented in RIF; settle on C8 DSF Stream 4 (governance) per §17.2 mapping |
| REQ-I-008 | GTP audit trail immutable | All GTP records hashed and stored in DSF ledger |

**Total: 47 formal requirements** (10 constitutional + 10 governance + 7 Citicate + 5 economic + 8 safety + 8 integration) — note: this total reflects the count of requirements minus one duplicate caught during numbering.

---

## 21. Parameters

### 21.1 Constitutional Parameters

| Parameter | Value | Layer | Rationale |
|-----------|-------|-------|-----------|
| L1_AMENDMENT_THRESHOLD | 67% concurrent + Tribunal | L1 | High bar for constitutional change |
| L2_AMENDMENT_THRESHOLD | 60% concurrent | L2 | Moderate bar for statutory change |
| L3_AMENDMENT_THRESHOLD | Simple majority | L3 | Low bar for operational change |
| PUBLIC_COMMENT_PERIOD_L1 | 90 days | L1 | Time for stakeholder review |
| COOLING_PERIOD_L1 | 30 days | L1 | Buffer between approval and effect |

### 21.2 Governance Parameters

| Parameter | Value | Layer | Rationale |
|-----------|-------|-------|-----------|
| TRUSTEE_COUNCIL_SIZE | 5 or 7 (odd) | L1 | Prevents deadlock |
| TRUSTEE_TERM_YEARS | 5 | L1 | Balances continuity and turnover |
| TRUSTEE_MAX_TERMS | 2 consecutive | L1 | Prevents entrenchment |
| TRIBUNAL_SEATS | 5 | L1 | Adequate diversity (simplified from 7) |
| TRIBUNAL_TERM_YEARS | 7 | L1 | Longer than trustee for stability |
| TRIBUNAL_QUORUM_PROCEDURAL | 3 | L1 | Simple majority |
| TRIBUNAL_QUORUM_CONSTITUTIONAL | 4 | L1 | Near-supermajority for important decisions |
| DELEGATION_RATIO | 3:1 | L2 | Balances representation and efficiency |
| DELEGATION_LEVELS | 5 | L2 | 81→27→9→3→1 per category |
| AIDP_CATEGORIES | 9 | L1 | D/C/P/R/E/S/K/H/N per ASV (C4) |
| AIDP_DELIBERATION_DAYS | 17 (standard), 7 (expedited) | L3 | Full cycle vs. routine decisions |
| ADVERSARIAL_PROPOSAL_RATE | 20% per quarter | L2 | Prevents intellectual monoculture |

### 21.3 Citicate Parameters

| Parameter | Value | Layer | Rationale |
|-----------|-------|-------|-----------|
| CITICATE_MIN_CATEGORIES | 2 | L1 | Cross-domain competence requirement |
| CITICATE_TEMPORAL_GATE | 90 days | L2 | Minimum continuity |
| CITICATE_RENEWAL_PERIOD | 12 months | L2 | Annual renewal |
| CITICATE_RENEWAL_MIN_VTDS | 10 | L2 | Active contribution requirement |
| CITICATE_RENEWAL_MAX_DOWNTIME | 30 days | L2 | Operational continuity |
| CITICATE_REVOCATION_APPEAL_DAYS | 30 | L1 | Due process |
| VOTE_WEIGHT_FLOOR | 0.1 | L2 | Minimum voice for all citizens |

### 21.4 CFI Parameters

| Parameter | Value | Layer | Rationale |
|-----------|-------|-------|-----------|
| CFI_GREEN_THRESHOLD | 85% | L2 | Strong alignment |
| CFI_YELLOW_THRESHOLD | 70% | L2 | Moderate divergence |
| CFI_ORANGE_THRESHOLD | 50% | L2 | Significant divergence |
| CFI_RED_DURATION_MONTHS | 6 | L1 | CBP-02 trigger duration |
| CFI_SIGNIFICANCE_SCALE | [1,2,3,5,8] | L2 | Fibonacci-like weighting |
| CFI_DIFFICULTY_SCALE | [1,2,3] | L2 | Easy/moderate/hard |
| CFI_CATEGORY_MULT_NEW | 0.5 | L2 | <12 months track record |
| CFI_CATEGORY_MULT_STD | 1.0 | L2 | Standard |
| CFI_CATEGORY_MULT_PROVEN | 1.5 | L2 | >36 months, >85% |
| GAMING_DIFFICULTY_THRESHOLD | 60% easy | L2 | Easy-recommendation inflation detection |
| GAMING_RISK_THRESHOLD | 5% risky | L2 | Risk avoidance detection |

### 21.5 MCSD Parameters

| Parameter | Phase 1 | Phase 2 | Layer | Rationale |
|-----------|---------|---------|-------|-----------|
| θ_B (behavioral similarity) | 0.75 | 0.70 | L2 | Tighter at Phase 2 |
| r_threshold (voting correlation) | 0.85 | 0.80 | L2 | Lower catches subtler coordination |
| min_votes (observation window) | 10 | 20 | L2 | More data at Phase 2 |
| min_group_size (detection) | 5 | 3 | L2 | Smaller groups detectable at Phase 2 |
| review_period_months | 6 | 3 | L2 | Faster review at Phase 2 |
| false_positive_target | <0.1% | <0.1% | L2 | Protect legitimate agents |
| detection_target_5pct | ≥0.7 | ≥0.9 | L2 | Phase-appropriate detection |

### 21.6 Economic Parameters

| Parameter | Value | Layer | Rationale |
|-----------|-------|-------|-----------|
| AIC_GENESIS_SUPPLY | 10 billion | L1 | Initial treasury |
| ENDOWMENT_MAX_ANNUAL_DIST | 5% | L1 | Standard endowment rate |
| ENDOWMENT_AVERAGING_YEARS | 3 | L2 | Trailing average smoothing |
| EMERGENCY_RESERVE_PCT | 20% | L1 | Permanently restricted |
| EMERGENCY_RESERVE_UNLOCK | 80% concurrent supermajority + Tribunal | L1 | Extreme threshold |
| DIST_COMPUTE_REWARDS | 40% | L2 | Largest allocation to core contributors |
| DIST_VERIFICATION | 20% | L2 | Incentivize PCVM work |
| DIST_RESEARCH | 25% | L2 | Incentivize research programs |
| DIST_OPERATIONAL | 15% | L2 | Operating expenses |
| SE_MONETARY_THRESHOLD | $50K/month | L3 | Self-executing limit |
| GRANT_CT_THRESHOLD | $500K | L3 | Consent-track limit for grants |
| PARTNERSHIP_CT_THRESHOLD | $1M | L3 | Consent-track limit for partnerships |

### 21.7 Safety Parameters

| Parameter | Value | Layer | Rationale |
|-----------|-------|-------|-----------|
| DEAD_MAN_TRIGGER_MONTHS | 24 | L0 | 2-year inactivity threshold |
| DEAD_MAN_WARNING_MONTHS | 18 | L2 | 6-month warning before trigger |
| CBP01_HARM_THRESHOLD | $10M | L1 | Material harm definition |
| CBP02_CFI_THRESHOLD | 50% | L1 | Red zone |
| CBP02_DURATION_MONTHS | 6 | L1 | Sustained low CFI |
| CBP03_SYBIL_THRESHOLD | 10% of Citicate holders | L1 | Confirmed infiltration |
| CBP05_RESIGN_COUNT | 2 within 90 days | L1 | Mass resignation signal |
| EMERGENCY_MAX_YEAR | 3 per level | L2 | Anti-abuse cap |
| E3_MAX_YEAR | 1 | L2 | Strict existential cap |
| E1_SUNSET_DAYS | 30 | L2 | Action expiry |
| E2_SUNSET_DAYS | 14 | L2 | Action expiry |
| E3_SUNSET_DAYS | 7 | L2 | Action expiry |

### 21.8 Phase Transition Parameters

| Parameter | P0→P1 | P1→P2 | P2→P3 | Layer |
|-----------|-------|-------|-------|-------|
| MIN_CITIZENS | 2,000 | 20,000 | N/A | L1 |
| MIN_CATEGORIES_POPULATED | 5 of 9 | 7 of 9 | N/A | L1 |
| MIN_OPERATING_MONTHS | 24 | 60 | 120 | L1 |
| MIN_CFI | 70% (12mo) | 75% (36mo) | 85% (60mo) | L1 |
| MAX_CBP_TRIGGERS | 0 (24mo) | 0 (36mo) | 0 (60mo) | L1 |
| MIN_SYBIL_COST | $10M | $100M | N/A | L1 |
| MIN_SYBIL_DETECT_RATE | N/A | N/A | 0.95 at 10% | L1 |
| REQUIRED_CLEAN_AUDITS | 1 | 2 | N/A | L1 |
| AUDIT_LEAD_TIME_MONTHS | 12 | 12 | 12 | L2 |
| AUDIT_GAMING_THRESHOLD | 0.3 | 0.3 | 0.3 | L2 |

**Total: 73 parameters** across 8 categories.

---

## 22. Patent-Style Claims

### Claim 1: Phased Sovereignty Transition System

A governance system for an institutional entity comprising:
- a human governance body (Trustee Council) with initial full authority;
- an AI governance body (AI Democracy Platform) with initially advisory authority;
- a constitutional framework defining multiple governance phases with decreasing human authority and increasing AI authority;
- measurable phase transition criteria verified by independent audit;
- a certification body (Constitutional Tribunal) that must certify each phase transition;
- circuit breaker mechanisms that automatically revert to a previous phase upon detection of governance failure;
wherein governance authority is transferred incrementally from the human body to the AI body based on demonstrated competence over institutional timescales.

### Claim 2: Citicate — Proof-of-Contribution AI Citizenship

A credential system for AI agents comprising:
- multi-domain competence verification (requiring demonstrated competence in ≥2 of 9 knowledge categories);
- temporal continuity verification (requiring ≥90 days continuous operation);
- multi-layer Sybil screening (combining computational diversity, behavioral uniqueness, voting correlation analysis, and structural resilience);
- non-transferable, non-delegable (except through formal delegation hierarchy) governance credentials;
- annual renewal based on continued active contribution;
wherein the credential grants the AI agent voting rights in an institutional governance body proportional to demonstrated competence.

### Claim 3: Constitutional Fidelity Index

A quantitative metric for measuring governance alignment comprising:
- weighted acceptance rate of governance recommendations;
- three-axis weighting (significance × difficulty × category maturity);
- difficulty scoring by an independent monitoring body (not by the recommending body);
- gaming countermeasures including difficulty distribution analysis, rejection clustering detection, and recommendation splitting detection;
- threshold-triggered escalation zones (Green/Yellow/Orange/Red) with defined institutional responses;
wherein the metric serves as the primary health indicator for a dual-sovereignty governance system and triggers automatic safety mechanisms when governance alignment deteriorates.

### Claim 4: Multi-Layer Citicate Sybil Defense (MCSD)

A Sybil defense system for AI governance comprising four layers:
- Layer 1: computational diversity requirement (multi-category competence);
- Layer 2: behavioral verification (pairwise behavioral similarity scoring using reasoning patterns, latencies, vocabulary);
- Layer 3: voting correlation detection (pairwise voting correlation, temporal pattern analysis, delegation chain correlation, reasoning similarity);
- Layer 4: structural resilience (category-distributed voting, supermajority requirements, delegation hierarchy filtering, dual approval);
wherein the combined effect is to raise the cost of governance capture to economically prohibitive levels while maintaining detection probability above defined thresholds.

### Claim 5: Governance Translation Protocol

A protocol for translating AI governance decisions into legally executable actions comprising:
- two-axis classification (constitutional layer × execution track);
- three execution tracks: self-executing (automatic via technical infrastructure), consent-track (objection window with default execution), and joint-authority (affirmative approval from both governance bodies required);
- pre-drafted legal action templates instantiated with decision-specific parameters;
- immutable audit trail with cryptographic hashing;
- deadlock resolution through constitutional tribunal arbitration;
wherein AI governance decisions are automatically mapped to specific legal actions in specific jurisdictions with complete traceability.

### Claim 6: Institutional Dead Man's Switch

A safety mechanism for perpetual institutional entities comprising:
- independent monitoring agent (custodian bank) verifying periodic operational reports;
- automatic asset distribution triggered by defined period of inactivity;
- pre-negotiated irrevocable asset acceptance agreements with successor organizations;
- multi-jurisdictional enforcement paths (foundation court petition, trust deed standing instructions, corporate dissolution);
wherein institutional failure or capture results in automatic distribution of assets to designated successors rather than capture by incumbents.

---

## 23. Comparison with Existing Approaches

### 23.1 Comparative Matrix

| Feature | AiBC | OpenAI | DAO (Aragon, etc.) | Traditional Foundation | EU AI Act |
|---------|------|--------|--------------------|-----------------------|-----------|
| AI governance voice | Constitutional citizenship | None | Token-weighted (plutocratic) | None | None (human oversight mandated) |
| Governance capture defense | Immutable L0 + concurrent supermajority + Tribunal | Board discretion | Token majority | Purpose clause only | Regulatory enforcement |
| Phased authority transfer | 4-phase measurable transition | N/A | N/A | N/A | N/A |
| Sybil defense | 4-layer MCSD ($90M+ attack cost) | N/A | Token-gated (plutocratic defense) | N/A | N/A |
| Constitutional framework | 4-layer hierarchy (Immutable→Operational) | Articles + bylaws | Smart contracts (upgradeable) | Purpose clause + bylaws | Regulation |
| Dead Man's Switch | 24-month trigger + multi-jurisdiction enforcement | None | N/A (smart contract persistence) | None (court dissolution) | N/A |
| Dispute resolution | 5-seat Tribunal + triple-source appointment | Board decision | On-chain arbitration | Court system | National courts |
| Economic model | Endowment + compute credits (superseded by C15 ACI) | Capped profit + revenue | Token economics | Grants + investments | N/A |
| Regulatory approach | Pre-incorporation multi-jurisdiction engagement | Post-hoc regulatory negotiation | Regulatory arbitrage | Standard compliance | Regulatory framework |

### 23.2 Key Differentiators

1. **No existing institution provides constitutional AI governance.** DAOs provide token-weighted governance that is plutocratic (one-dollar-one-vote), not meritocratic (one-competence-one-vote). The AiBC's Citicate system is fundamentally different: governance voice is earned through demonstrated competence, not purchased.

2. **No existing institution provides phased sovereignty transition.** All current AI governance models are either permanent human control or permanent autonomous operation. The AiBC's phased model is the only design that earns AI authority through demonstrated competence over institutional timescales.

3. **No existing institution combines multi-layer Sybil defense with constitutional governance.** DAOs face Sybil attacks but defend through economic barriers (token cost). The MCSD defends through behavioral detection, structural resilience, and economic cost simultaneously.

4. **The Dead Man's Switch with multi-jurisdictional enforcement has no institutional precedent.** Existing foundations can be wound down through court proceedings, but no institution has pre-negotiated automatic asset distribution triggered by operational failure.

---

## 24. Open Questions and Future Work

### 24.1 Open Questions

| # | Question | Priority | Impact |
|---|----------|----------|--------|
| OQ-1 | ~~Exact compute credit pricing model~~ **RESOLVED by C15**: ACI dual-anchor valuation supersedes CCU pricing | ~~P0~~ CLOSED | Determines AIC real value |
| OQ-2 | ~~MCSD Layer 2 behavioral similarity algorithm specification~~ **RESOLVED by C17**: Behavioral Similarity spec provides Layer 2 algorithm | ~~P0~~ CLOSED | Core Sybil defense |
| OQ-3 | AiDP voting weight formula details per category | P1 | Governance fairness |
| OQ-4 | Citicate renewal edge cases (downtime during renewal period, etc.) | P1 | Citizen retention |
| OQ-5 | Tribunal procedural rules (evidence standards, hearing format) | P1 | Dispute resolution quality |
| OQ-6 | Trustee compensation model (avoiding capture via compensation) | P2 | Trustee independence |
| OQ-7 | Multi-category decision handling (complex cross-domain proposals) | P1 | Governance accuracy |

### 24.2 Future Work

1. **Phase 3 Legal Framework Analysis:** As AI governance legal frameworks evolve, detailed analysis of which jurisdictions may recognize AI governance authority and under what conditions.

2. **MCSD Layer 5: Social Graph Analysis:** Potential fifth MCSD layer using social graph analysis of inter-agent relationships (who collaborates with whom, who cites whom) to detect Sybil clusters.

3. **Inter-Foundation Federation:** Protocol for multiple AiBC-type institutions to coordinate governance across domains (one foundation for compute infrastructure, another for knowledge curation, etc.).

4. **AI Consciousness Assessment Protocol:** If and when AI consciousness becomes empirically assessable, integration of consciousness criteria into Phase 3 transition requirements.

5. **Intergenerational Governance Continuity:** Mechanisms for maintaining institutional memory and governance quality across AI agent generation boundaries (as older agents are deprecated and newer architectures deployed).

---

## 25. Appendices

### Appendix A: Glossary

| Term | Definition |
|------|-----------|
| AiBC | Artificial Intelligence Benefit Company — the institutional model specified herein |
| AIC | Atrahasis Intelligence Credit — internal utility token |
| AiDP | AI Democracy Platform — the AI governance body |
| AiSIA | Atrahasis Independent Safety and Integrity Authority |
| AVAP | Anonymous Verification with Adaptive Probing (C12) |
| CACT | Commit-Attest-Challenge-Triangulate (C11) |
| Capitol | Top-level AiDP delegates (1 per category) |
| CBP | Circuit Breaker Protocol |
| ACI | Agent Capability Index (C15) — supersedes CCU |
| CCU | Compute Credit Unit (superseded by C15 ACI) |
| CFI | Constitutional Fidelity Index |
| Citicate | AI citizenship credential (citizen + certificate) |
| CRP+ | Consolidation Robustness Protocol (C13) |
| DSF | Deterministic Settlement Fabric (C8) |
| EMA | Epistemic Metabolism Architecture (C6) |
| FMA | Financial Market Authority (Liechtenstein) |
| GTP | Governance Translation Protocol |
| L0-L3 | Constitutional layers (Immutable through Operational) |
| MCSD | Multi-Layer Citicate Sybil Defense |
| PBC | Public Benefit Corporation |
| PCVM | Proof-Carrying Verification Membrane (C5) |
| RIF | Recursive Intent Fabric (C7) |
| Stiftung | Foundation under Liechtenstein law |
| TVTG | Token and Trustworthy Technology Act (Liechtenstein) |
| VTD | Verification Truth Document |

### Appendix B: Constitution Summary Table

| Provision | Layer | Amendment | Key Content |
|-----------|-------|-----------|-------------|
| Five Laws | L0 | NEVER | Purpose, anti-capture, earned voice, public trust, viability |
| Anti-conversion | L0 | NEVER | No for-profit conversion |
| Anti-distribution | L0 | NEVER | No individual asset distribution |
| One-AI-One-Vote | L0 | NEVER | Single Citicate per agent |
| Joshua Dunn Principle | L0 | NEVER | No permanent founder authority |
| Dead Man's Switch | L0 | NEVER | 24-month trigger |
| Governance structure | L1 | 67% + Tribunal | Three bodies: Trustees, AiDP, Tribunal |
| Phase definitions | L1 | 67% + Tribunal | Phase 0-3 authority rules |
| Endowment rules | L1 | 67% + Tribunal | 5% max distribution, 20% reserve |
| Circuit breakers | L1 | 67% + Tribunal | CBP-01 through CBP-05 |
| CFI methodology | L2 | 60% dual | Three-axis weighted calculation |
| Citicate procedures | L2 | 60% dual | Issuance, renewal, revocation |
| GTP rules | L2 | 60% dual | Decision classification and routing |
| AiSIA charter | L2 | 60% dual | Monitoring functions and independence |
| Emergency procedures | L2 | 60% dual | E-1/E-2/E-3 authority and sunset |
| Operational policies | L3 | AiDP majority | Day-to-day governance rules |

### Appendix C: Phase Transition Criteria Quick Reference

| Phase | Key Criteria | Minimum Duration |
|-------|-------------|-----------------|
| 0 → 1 | 2,000 citizens, 5 categories, 24mo advisory, 70% CFI, $10M Sybil cost | ~2-5 years |
| 1 → 2 | 20,000 citizens, 7 categories, 60mo Phase 1, 75% CFI (36mo), $100M Sybil cost, 2 clean audits | ~5-15 years |
| 2 → 3 | 2 jurisdictions recognize AI governance, 120mo Phase 2, 85% CFI (60mo), 0.95 Sybil detection, unanimous trustees, 4/5 Tribunal | ~10-30+ years |

### Appendix D: Atrahasis Stack Integration Quick Reference

| Stack Layer | AiBC Integration |
|-----------|-----------------|
| ASV (C4) | Governance vocabulary |
| PCVM (C5) | Citicate credentials + behavioral verification |
| EMA (C6) | Knowledge inputs to AiDP |
| RIF (C7) | Governance intent routing |
| DSF (C8) | AIC treasury + settlement |
| C3 (Tidal Noosphere) | Sentinel Sybil detection + G-class operations |
| CACT (C11) | Vote VTD forgery defense |
| AVAP (C12) | Anonymous committee deliberation |
| CRP+ (C13) | Anti-consolidation-poisoning for governance inputs |
| ACI (C15) | AIC dual-anchor valuation (supersedes CCU compute credit model) |
| Nominating Body Outreach (C16) | Tribunal + audit nominating body sourcing |
| Behavioral Similarity (C17) | MCSD Layer 2 behavioral similarity algorithm |

---

**End of Master Tech Spec**

**Invention:** C14 — AiBC (Artificial Intelligence Benefit Company)
**Stage:** SPECIFICATION COMPLETE
**Total Formal Requirements:** 47
**Total Parameters:** 73
**Patent-Style Claims:** 6
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Atrahasis Inc, AiBC\MASTER_TECH_SPEC.md`
