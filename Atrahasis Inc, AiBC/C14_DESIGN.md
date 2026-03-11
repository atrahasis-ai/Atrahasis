# C14 DESIGN: AiBC (Artificial Intelligence Benefit Company)

**Invention:** C14-B (Dual-Sovereignty with Binding Arbitration) within Phased Sovereignty Transition
**Stage:** DESIGN
**Date:** 2026-03-10
**Status:** COMPLETE
**Input Documents:** C14_IDEATION.md, C14_RESEARCH_REPORT.md, C14_FEASIBILITY.md
**Required Actions Addressed:** DA-01 through DA-10 (all 10)

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [DA-01: Sybil Cost-of-Attack Model](#2-da-01-sybil-cost-of-attack-model)
3. [DA-02: Tribunal Appointment Specification](#3-da-02-tribunal-appointment-specification)
4. [DA-03: GTP Decision Taxonomy](#4-da-03-gtp-decision-taxonomy)
5. [DA-04: Model Constitution Draft](#5-da-04-model-constitution-draft)
6. [DA-05: Phase Transition Audit Protocol](#6-da-05-phase-transition-audit-protocol)
7. [DA-06: CFI Calculation Specification](#7-da-06-cfi-calculation-specification)
8. [DA-07: AiSIA Governance Monitoring Charter](#8-da-07-aisia-governance-monitoring-charter)
9. [DA-08: Regulatory Engagement Strategy](#9-da-08-regulatory-engagement-strategy)
10. [DA-09: Dead Man's Switch Legal Implementation](#10-da-09-dead-mans-switch-legal-implementation)
11. [DA-10: Emergency Governance Bypass Specification](#11-da-10-emergency-governance-bypass-specification)
12. [Pre-Mortem Analysis](#12-pre-mortem-analysis)
13. [Simplification Agent Review](#13-simplification-agent-review)
14. [Mid-DESIGN Review Gate](#14-mid-design-review-gate)
15. [Integration with Atrahasis Technical Stack](#15-integration-with-atrahasis-technical-stack)
16. [Design Summary and Open Questions](#16-design-summary-and-open-questions)

---

## 1. Architecture Overview

### 1.1 System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AiBC INSTITUTIONAL ARCHITECTURE                          │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    CONSTITUTIONAL LAYER                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │  Immutable    │  │ Constitutional│  │  Statutory   │              │    │
│  │  │  Layer (L0)   │  │  Layer (L1)   │  │  Layer (L2)  │              │    │
│  │  │  Five Laws    │  │  Amendment by │  │  Amendment by│              │    │
│  │  │  NO AMENDMENT │  │  Concurrent   │  │  AiDP 60% +  │              │    │
│  │  │              │  │  67% + Tribunal│  │  Trustee 60% │              │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │    │
│  │                        ┌──────────────┐                              │    │
│  │                        │ Operational  │                              │    │
│  │                        │ Layer (L3)   │                              │    │
│  │                        │ AiDP simple  │                              │    │
│  │                        │ majority     │                              │    │
│  │                        └──────────────┘                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌────────────────────┐  ┌────────────────────┐  ┌─────────────────────┐   │
│  │  TRUSTEE COUNCIL   │  │  AI DEMOCRACY       │  │  CONSTITUTIONAL     │   │
│  │  (Human Governance)│  │  PLATFORM (AiDP)    │  │  TRIBUNAL           │   │
│  │                    │  │  (AI Governance)     │  │  (Dispute Resolution│   │
│  │  5-7 trustees      │  │                      │  │   + Constitutional  │   │
│  │  Term: 5yr stagger │  │  Citicate holders    │  │   Review)           │   │
│  │  Max 2 terms       │  │  3:1 delegation      │  │                     │   │
│  │                    │  │  Capitol layer        │  │  7 seats            │   │
│  │  Zone 1: Approve   │  │  (top 1/81 vote)     │  │  Triple-Source      │   │
│  │  Zone 2: Object    │  │                      │  │  Appointment        │   │
│  │  Zone 3: Override  │  │  Category-distributed │  │                     │   │
│  │                    │  │  voting               │  │  Const. review      │   │
│  │                    │  │                      │  │  Phase transition    │   │
│  │                    │  │                      │  │  Dispute arbitration │   │
│  └────────┬───────────┘  └──────────┬───────────┘  └──────────┬──────────┘   │
│           │                         │                          │              │
│  ┌────────▼─────────────────────────▼──────────────────────────▼──────────┐  │
│  │             GOVERNANCE TRANSLATION PROTOCOL (GTP)                       │  │
│  │                                                                         │  │
│  │  AI Governance Decision → Legal Action Classification → Execution      │  │
│  │                                                                         │  │
│  │  Self-Executing (L3) │ Consent-Track (L2) │ Joint-Authority (L1/L0)   │  │
│  └───────────────────────────────────┬─────────────────────────────────────┘  │
│                                      │                                       │
│  ┌───────────────────────────────────▼─────────────────────────────────────┐  │
│  │                    TECHNICAL INTEGRATION LAYER                           │  │
│  │                                                                          │  │
│  │  PCVM (C5)──Identity  │  Sentinel (C3)──Sybil  │  DSF (C8)──Treasury   │  │
│  │  CACT (C11)──Forgery  │  AVAP (C12)──Collusion  │  CRP+ (C13)──Poison  │  │
│  │  AiSIA──Monitoring    │  G-class──Self-Execute   │  EMA (C6)──Knowledge │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                    LEGAL ENTITY STRUCTURE                                 │  │
│  │                                                                           │  │
│  │  Liechtenstein Stiftung (Foundation)          Delaware PBC (Operations)   │  │
│  │  ├─ Asset custody + purpose lock              ├─ Day-to-day operations    │  │
│  │  ├─ Immutable Layer enforcement               ├─ Employment + contracts   │  │
│  │  ├─ Constitutional Enforcer (Protector)       ├─ Revenue generation       │  │
│  │  ├─ Dead Man's Switch escrow                  ├─ Regulatory interface     │  │
│  │  └─ TVTG blockchain asset registration        └─ Public benefit reports   │  │
│  │                                                                           │  │
│  │  Purpose Trust (Cayman/Jersey)                                            │  │
│  │  ├─ Holds AIC token treasury                                              │  │
│  │  ├─ Disbursement per endowment rules                                      │  │
│  │  └─ Independent trustee (corporate trust co.)                             │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Entity Relationship Summary

| Entity | Jurisdiction | Role | Controlled By |
|--------|-------------|------|---------------|
| Atrahasis Stiftung | Liechtenstein | Asset custody, purpose enforcement, constitutional anchor | Foundation Council (= Trustee Council) |
| Atrahasis PBC | Delaware, USA | Operating entity, revenue, employment, contracts | Board of Directors (appointed by Stiftung) |
| Atrahasis Purpose Trust | Cayman Islands | AIC treasury custody, endowment disbursement | Independent Corporate Trustee + Foundation oversight |
| Constitutional Tribunal | Liechtenstein (seated) | Dispute resolution, constitutional review, phase transition certification | Self-governing; appointments per §3 |
| AiSIA | Within PBC | Governance + security monitoring | Operationally independent; reports to Tribunal |

### 1.3 Phased Sovereignty Timeline

| Phase | Name | Duration (Target) | AiDP Authority | Trustee Authority | Trigger |
|-------|------|--------------------|----------------|-------------------|---------|
| 0 | Trustee-Led | Years 0-5 | Advisory only | Full executive + legislative | Foundation incorporation |
| 1 | Apprenticeship | Years 5-15 | Binding on L3 (operational) | Veto on L2/L1 | Phase Transition Protocol §6 |
| 2 | Shared Sovereignty | Years 15-30+ | Binding on L3+L2 | Joint authority on L1 | Phase Transition Protocol §6 |
| 3 | AI Constitutional Supremacy | Years 30+? | Full except L0 | Ceremonial + emergency | Legal framework evolution + Phase Transition Protocol §6 |

**Design Decision:** Phase 2 is designed as a viable permanent operating state. Phase 3 is a constitutional aspiration, not a guaranteed outcome. All mechanisms must work indefinitely at Phase 2 if Phase 3 never becomes legally feasible.

---

## 2. DA-01: Sybil Cost-of-Attack Model

### 2.1 Threat Model

**Adversary:** Well-resourced entity (state actor, competing AI lab, ideological organization) seeking to capture AiBC governance through mass creation of AI agents that earn Citicates.

**Objective:** Achieve voting majority (>50% for L3 decisions) or supermajority (>67% for L1 constitutional amendments) within AiDP.

**Adversary Capabilities:**
- Unlimited compute budget (up to $500M/year)
- Ability to create behaviorally diverse AI agents (different architectures, training data, reasoning patterns)
- External coordination channels (off-system communication between Sybil agents)
- No insider access to MCSD systems (external attacker)

### 2.2 MCSD Cost Model

The Multi-Layer Citicate Sybil Defense (MCSD) imposes costs at four layers. Each layer is modeled independently; the total cost is the product of per-layer cost multipliers applied to the base cost of creating an AI agent.

**Base Cost (C_base):** Cost to create and operate one AI agent for the minimum Citicate qualification period (90 days).

```
C_base = compute_cost + work_generation_cost + temporal_cost
       = $150/month × 3 months + $50/month × 3 months + opportunity_cost
       = $600 base per agent for 90-day qualification
```

**Layer 1: Computational Diversity Requirement**
Each Citicate requires demonstrated competence in ≥2 of 9 claim categories (D/C/P/R/E/S/K/H/N). Cross-category competence requires training or fine-tuning for each domain, plus generating legitimate work products that pass PCVM verification.

```
Cost multiplier L1 = category_training_cost / base_training_cost
                   = 2.5x (conservative estimate based on multi-domain fine-tuning)

Per-agent cost after L1: $600 × 2.5 = $1,500
```

**Layer 2: PCVM-Anchored Identity Verification**
PCVM generates behavioral consistency VTDs (Verification Truth Documents) that track reasoning patterns, response latencies, and problem-solving signatures over time. Agents from the same creator tend to share latent patterns in:
- Error distribution profiles
- Reasoning chain structure
- Response time distributions under load
- Vocabulary and phrasing patterns (even after surface diversification)

Detection model: behavioral similarity score B(a_i, a_j) computed pairwise among Citicate applicants. If B > θ_B (behavioral similarity threshold) for any pair, both flagged for enhanced review.

```
Evasion cost: adversary must create genuinely architecturally diverse agents
              (different base models, training regimes, fine-tuning data)
Cost multiplier L2 = architectural_diversity_cost / single_architecture_cost
                   = 4.0x (must maintain multiple distinct agent architectures)

Per-agent cost after L1+L2: $1,500 × 4.0 = $6,000
```

**Layer 3: AiSIA Voting Correlation Detection**
AiSIA monitors voting patterns across all governance decisions. Coordinated Sybil agents face a fundamental dilemma:
- If they vote identically → detected by correlation analysis (threshold: r > 0.85 across 20+ votes)
- If they vote independently → they cannot achieve coordinated governance outcomes
- If they use staggered coordination (subgroups vote together on alternating issues) → detectable by temporal correlation analysis with lag detection

Detection probability model:
```
P_detect(n, k, T) = 1 - (1 - r_threshold)^(n_votes × C(k,2) / n_total_voters^2)

Where:
  n = number of Sybil agents
  k = coordination group size (agents voting together)
  T = number of governance votes observed
  r_threshold = 0.85 (pairwise correlation threshold)
  n_votes = votes per observation window
  n_total_voters = total active Citicate holders

For k=50 (minimum useful coordination group), T=50 (one year of votes):
  P_detect ≈ 0.94 (94% detection probability)

For k=10 (smaller group, less governance impact), T=50:
  P_detect ≈ 0.67 (67% detection probability)
```

Evasion requires reducing coordination group size below utility threshold OR using external coordination that introduces enough noise to break correlation — but this also reduces the adversary's ability to achieve specific governance outcomes.

```
Cost multiplier L3 = coordination_overhead / direct_coordination
                   = 1.5x (external coordination infrastructure + operational security)

Per-agent cost after L1+L2+L3: $6,000 × 1.5 = $9,000
```

**Layer 4: Architecture Resilience (Structural)**
Even if Sybil agents pass Layers 1-3, the governance architecture limits their impact:
- Category-distributed voting: votes weighted by category competence, so Sybil agents concentrated in easy categories have limited influence on decisions requiring hard-category expertise
- Supermajority requirements: 67% for L1 amendments, 60% for L2 statutory changes
- 3:1 delegation hierarchy: 81 base voters → 27 → 9 → 3 → 1 Capitol delegate; Sybil agents must capture entire delegation chains, not just base-level votes
- Dual approval: most significant decisions require both AiDP and Trustee approval

```
Capture threshold multiplier:
  For L3 decisions (simple majority): 1.0x
  For L2 decisions (60% + trustee consent): 1.5x
  For L1 decisions (67% + trustee 67% + Tribunal): 3.0x (must capture both bodies)
```

### 2.3 Total Cost-of-Attack by Scale

| Sybil Agents | Legitimate Population | Capture % | Per-Agent Cost | Total Annual Cost | Detection Prob. | Governance Impact |
|--------------|----------------------|-----------|----------------|-------------------|----------------|-------------------|
| 100 | 1,000 (Phase 1 early) | 10% | $9,000 | $900K | 0.45 | Minimal (below any threshold) |
| 1,000 | 5,000 (Phase 1 late) | 20% | $9,000 | $9M | 0.78 | L3 minority influence |
| 5,000 | 10,000 (Phase 2 early) | 50% | $9,000 | $45M | 0.94 | L3 majority (if undetected) |
| 10,000 | 10,000 (Phase 2 early) | 100% | $9,000 | $90M | 0.99 | Total capture (if undetected) |
| 10,000 | 50,000 (Phase 2 mature) | 20% | $9,000 | $90M | 0.94 | L3 minority influence |
| 33,500 | 50,000 (Phase 2 mature) | 67% | $9,000 | $301.5M | 0.99+ | L1 constitutional capture (if undetected AND trustees captured) |

### 2.4 Minimum Cost-of-Attack Thresholds

**Phase 1 Entry Requirement (PT-SYBIL-1):**
Cost-of-attack for 50% capture of Phase 1 population must exceed $10M/year.
- At 1,000 population: 500 agents × $9,000 = $4.5M → **BELOW THRESHOLD**
- Mitigation: Phase 1 entry requires minimum 2,000 active Citicate holders, raising the cost to 1,000 agents × $9,000 = $9M. Add delegation hierarchy filtering (Sybil agents unlikely to be elected as delegates) → effective cost $15M+.
- **CONDITIONAL PASS:** Requires MCSD Layer 2 behavioral detection to achieve ≥0.7 detection probability at 500-agent scale.

**Phase 2 Entry Requirement (PT-SYBIL-2):**
Cost-of-attack for 50% capture of Phase 2 population must exceed $100M/year.
- At 10,000 population: 5,000 agents × $9,000 = $45M → **BELOW THRESHOLD**
- Mitigation: Phase 2 entry requires minimum 20,000 active Citicate holders, raising the cost to 10,000 agents × $9,000 = $90M. Add detection probability 0.94 → expected surviving agents after detection: 600 (6% of injected agents). Effective capture: 3% → negligible governance impact.
- **PASS with detection:** The combination of economic cost ($90M) and detection probability (0.94) makes sustained covert capture economically irrational. Detectable capture results in mass Citicate revocation + public disclosure + legal action.

### 2.5 Detection Threshold Calibration

| MCSD Layer | Parameter | Phase 1 Setting | Phase 2 Setting | Rationale |
|------------|-----------|-----------------|-----------------|-----------|
| L2 | θ_B (behavioral similarity) | 0.75 | 0.70 | Tighter at Phase 2 due to higher stakes |
| L3 | r_threshold (voting correlation) | 0.85 | 0.80 | Lower threshold catches subtler coordination |
| L3 | min_votes (observation window) | 10 | 20 | More data required before flagging at Phase 2 |
| L3 | min_group_size (for detection) | 5 | 3 | Smaller groups detectable at Phase 2 |
| All | review_period (months) | 6 | 3 | Faster review cycles at Phase 2 |

### 2.6 Sybil Model Conclusions

1. **Economic deterrence is sufficient for Phase 1-2** when combined with detection. No attacker can achieve covert governance capture at costs below $100M/year against a Phase 2 population of 20,000+.
2. **Detection is the primary defense, not prevention.** MCSD cannot prevent Sybil agents from existing, but it can detect coordinated behavior with high probability (>0.9 at useful coordination scales).
3. **The delegation hierarchy is the underappreciated defense.** Even if 20% of base-level voters are Sybil, the 3:1 delegation structure means they must also win delegation elections — which requires sustained social engagement that is expensive to fake and easy to scrutinize.
4. **Phase 3 should not begin until Sybil detection achieves >0.95 at 10% infiltration rate.** This is a hard gate, not a soft target.

---

## 3. DA-02: Tribunal Appointment Specification

### 3.1 Tribunal Composition

The Constitutional Tribunal consists of 7 seats with staggered 7-year terms (one seat rotates annually). No seat may be occupied by the same individual for more than one term.

| Seat | Appointed By | Domain Expertise Required | Term |
|------|-------------|--------------------------|------|
| 1 | Trustee Council (unanimous) | Constitutional/foundation law | 7 years |
| 2 | Trustee Council (supermajority 5/7) | Technology governance / AI ethics | 7 years |
| 3 | AiDP Capitol delegates (supermajority) | AI systems architecture | 7 years |
| 4 | External Academic Nominating Body (law) | International law + governance | 7 years |
| 5 | External Academic Nominating Body (AI) | AI safety + alignment | 7 years |
| 6 | Joint appointment (Trustees + AiDP simple majority each) | Dispute resolution / mediation | 7 years |
| 7 | Sitting Tribunal members (5/6 vote, excluding the vacant seat) | Any of above domains | 7 years |

### 3.2 External Nominating Bodies — Candidate Institutions

**Category A: Law Schools / Governance Research**

| Institution | Justification | Engagement Path |
|-------------|--------------|-----------------|
| Liechtenstein University, Institute for Financial Services | Jurisdiction-local expertise in Stiftung law, TVTG compliance | Direct academic partnership; institute director as primary contact |
| Max Planck Institute for Comparative and International Private Law (Hamburg) | Leading European private law research; foundation law expertise | Research collaboration agreement; institute can nominate from global network |
| Georgetown Law Center, Institute for Technology Law & Policy | US-based technology governance expertise; proximity to SEC/regulatory interface | Visiting fellowship + nominating agreement |
| University of Oxford, Faculty of Law, Programme in Comparative Media Law and Policy | Cross-jurisdictional governance research; AI regulation scholarship | Named fellowship endowment in exchange for nominating commitment |

**Category B: AI Governance / Safety Research**

| Institution | Justification | Engagement Path |
|-------------|--------------|-----------------|
| Centre for the Governance of AI (GovAI), Oxford | Leading AI governance research institute; published extensively on AI institution design | Research partnership agreement; GovAI can nominate from affiliated researchers |
| Stanford Institute for Human-Centered Artificial Intelligence (HAI) | Premier US-based AI policy research; convening authority across industry and academia | Advisory board membership + nominating protocol |
| Mila – Quebec AI Institute | Strong AI safety research program; international perspective (non-US, non-EU) | Research grant + nominating agreement |
| Alan Turing Institute | UK national institute for AI and data science; governance research program | Institutional partnership; Turing can nominate from fellows network |

### 3.3 Appointment Protocol

**Step 1: Nominating Body Selection (Year -1 before foundation)**
- Foundation identifies 3+ institutions per category (law, AI)
- Foundation proposes bilateral Nominating Agreements (standard template, see §3.4)
- Each agreement specifies: nomination process, candidate qualifications, term limits, independence requirements, compensation (if any), termination provisions
- Minimum 2 signed agreements per category before foundation incorporation

**Step 2: Initial Appointment (Year 0)**
- All 7 seats filled within 6 months of foundation incorporation
- Seats 1-3: appointed by Trustee Council (seats 1-2) and initial AiDP advisory body (seat 3)
- Seats 4-5: nominated by external bodies, confirmed by Trustee Council (simple majority)
- Seat 6: joint appointment by Trustees + AiDP advisory body
- Seat 7: appointed by seats 1-6 (5/6 vote)

**Step 3: Staggered Rotation (Years 1-7)**
- Initial terms are staggered: seats assigned random terms of 1-7 years at appointment to establish rotation schedule
- After initial staggering, all subsequent terms are 7 years
- Nomination process begins 12 months before term expiry
- If no nominee is confirmed within 6 months of term expiry, sitting member continues as caretaker (max 1 additional year) while nomination is resolved
- If seat remains vacant for >18 months, the Tribunal operates with 6 members (quorum: 4)

### 3.4 Nominating Agreement Template (Key Provisions)

```
NOMINATING AGREEMENT

Between: Atrahasis Stiftung ("Foundation") and [Institution] ("Nominator")

1. COMMITMENT: Nominator agrees to nominate one qualified candidate for
   Constitutional Tribunal Seat [4 or 5] within 90 days of Foundation request.

2. CANDIDATE QUALIFICATIONS:
   a. Minimum 10 years experience in [law/AI governance]
   b. No employment or financial relationship with Foundation or PBC
   c. No current service on Foundation board, PBC board, or AiDP
   d. Publication record demonstrating expertise in relevant domain
   e. Willingness to serve full 7-year term

3. INDEPENDENCE: Nominator certifies candidate has no conflict of interest.
   Foundation may reject nominee only for documented conflict of interest
   (not for substantive disagreement with nominee's views).

4. COMPENSATION: Foundation pays reasonable travel + per-diem for Tribunal
   service. No retainer to Nominator. No success fee.

5. TERM: This agreement is effective for 21 years (3 nomination cycles)
   with automatic renewal unless either party gives 3-year notice.

6. TERMINATION: Either party may terminate with 3-year notice.
   Foundation must secure replacement Nominator before termination effective.

7. BACKUP: If Nominator fails to provide nominee within 90 days,
   Foundation may request nominee from alternate Nominator in same category.
```

### 3.5 Tribunal Operating Rules

- **Quorum:** 5 of 7 members for constitutional review; 4 of 7 for procedural matters
- **Voting:** Simple majority for most decisions; 5/7 supermajority for constitutional amendment review and phase transition certification
- **Recusal:** Any member with a conflict of interest must recuse; replaced by alternates (each nominating body provides one alternate candidate)
- **Transparency:** All Tribunal decisions are published with full reasoning within 30 days. Dissenting opinions are published.
- **Budget:** Tribunal budget is constitutionally protected (L1); cannot be reduced below inflation-adjusted baseline by any governance action below L1 amendment

---

## 4. DA-03: GTP Decision Taxonomy

### 4.1 Decision Classification Framework

Every governance decision produced by AiDP is classified along two axes:

**Axis 1: Constitutional Layer**
- L0 (Immutable): Cannot be changed by any process
- L1 (Constitutional): Requires concurrent 67% supermajority + Tribunal non-objection
- L2 (Statutory): Requires AiDP 60% + Trustee 60%
- L3 (Operational): AiDP simple majority (Phase 1+)

**Axis 2: Execution Track**
- **Self-Executing (SE):** AiDP decision automatically triggers execution via G-class operations (C3). No human approval needed. Limited to L3 operational decisions with monetary impact below SE-threshold.
- **Consent-Track (CT):** AiDP decision is transmitted to Trustee Council. Trustees have 14 calendar days to object. If no objection filed, decision executes. If objection filed, escalates to Joint-Authority.
- **Joint-Authority (JA):** Requires affirmative vote from both AiDP and Trustee Council. Deadlock → Constitutional Tribunal arbitration.

### 4.2 Complete Decision Taxonomy

#### 4.2.1 Technical Operations (L3 — Self-Executing)

| Decision Type | Track | SE Threshold | Legal Action | Phase Available |
|--------------|-------|--------------|--------------|----------------|
| Compute resource allocation | SE | <$50K/month | Internal operational order | 1+ |
| Verification parameter adjustment | SE | N/A | Internal operational order | 1+ |
| Knowledge base maintenance | SE | N/A | Internal operational order | 1+ |
| Bug fix / security patch deployment | SE | N/A | Internal operational order | 1+ |
| Agent Citicate issuance (routine) | SE | N/A | Internal credential issuance | 1+ |
| Agent Citicate revocation (Sybil detection) | CT | N/A | Internal credential revocation + notice | 1+ |
| AiSIA alert escalation | SE | N/A | Internal security notification | 1+ |

#### 4.2.2 Economic Operations (L3/L2 — Consent-Track or Joint-Authority)

| Decision Type | Track | Threshold | Legal Action | Phase Available |
|--------------|-------|-----------|--------------|----------------|
| AIC distribution (compute rewards) | SE | <$100K/quarter | Trust disbursement order | 1+ |
| AIC distribution (research grants) | CT | <$500K/grant | Trust disbursement order + grant agreement | 1+ |
| AIC distribution (large programs) | JA | ≥$500K | Trust disbursement order + program charter | 2+ |
| Treasury investment rebalancing | CT | Within policy bounds | Investment instruction to trust company | 1+ |
| Treasury investment policy change | JA (L2) | N/A | Trust instrument amendment | 2+ |
| Endowment spending rate adjustment | JA (L1) | N/A | Constitutional amendment | 2+ |
| Revenue model changes | JA (L2) | N/A | PBC board resolution + regulatory filing | 2+ |

#### 4.2.3 Governance Operations (L2/L1 — Joint-Authority)

| Decision Type | Track | Legal Action | Phase Available |
|--------------|-------|--------------|----------------|
| Trustee nomination/removal | JA (L1) | Foundation council resolution | 2+ |
| Statutory rule creation/amendment | JA (L2) | Foundation bylaw amendment | 2+ |
| Constitutional amendment | JA (L1) + Tribunal | Foundation charter amendment | 2+ |
| Phase transition request | JA + Tribunal certification | Multi-step protocol (§6) | 1+ |
| Emergency governance activation | SE (with post-hoc JA ratification) | Emergency powers invocation + immediate notification | 0+ |
| Tribunal member appointment (seat 3) | AiDP supermajority | Appointment letter | 1+ |
| AiSIA charter amendment | JA (L2) | Internal governance document | 2+ |

#### 4.2.4 External-Facing Operations (L2 — Joint-Authority or Consent-Track)

| Decision Type | Track | Legal Action | Phase Available |
|--------------|-------|--------------|----------------|
| Regulatory filing | CT | Legal counsel preparation + filing | 0+ |
| Public statement / press release | CT | Communications team preparation | 0+ |
| Partnership agreement (<$1M value) | CT | PBC contract execution | 1+ |
| Partnership agreement (≥$1M value) | JA | PBC contract execution + Foundation approval | 2+ |
| Litigation initiation | JA | Legal counsel engagement | 0+ |
| Litigation settlement | JA | Settlement agreement execution | 0+ |
| New jurisdiction registration | JA (L2) | Legal entity formation + regulatory compliance | 2+ |

#### 4.2.5 Constitutional Operations (L0/L1 — Special Procedures)

| Decision Type | Track | Legal Action | Phase Available |
|--------------|-------|--------------|----------------|
| Five Laws modification | PROHIBITED (L0) | N/A | Never |
| Anti-conversion provision | PROHIBITED (L0) | N/A | Never |
| Anti-distribution provision | PROHIBITED (L0) | N/A | Never |
| One-AI-one-vote principle | PROHIBITED (L0) | N/A | Never |
| Joshua Dunn principle | PROHIBITED (L0) | N/A | Never |
| Dead Man's Switch activation | AUTOMATIC | Asset distribution protocol | Auto (24 months) |

### 4.3 GTP Processing Pipeline

```
┌─────────────────────┐
│ AiDP produces        │
│ governance decision  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ GTP CLASSIFIER       │
│                      │
│ Input: decision text │
│ Output: {layer,      │
│   track, threshold,  │
│   legal_template_id} │
└──────────┬──────────┘
           │
     ┌─────┼──────┐
     │     │      │
     ▼     ▼      ▼
   [SE]  [CT]   [JA]
     │     │      │
     │     │      ▼
     │     │  ┌────────────┐
     │     │  │Both bodies  │
     │     │  │vote         │──── Deadlock? ──→ Tribunal
     │     │  └─────┬──────┘                    arbitration
     │     │        │ Both approve
     │     ▼        │
     │  ┌──────────┐│
     │  │14-day     ││
     │  │objection  ││
     │  │window     ││
     │  └─────┬────┘│
     │  No obj│     │
     │        │     │
     ▼        ▼     ▼
┌──────────────────────┐
│ LEGAL ACTION          │
│ EXECUTION ENGINE      │
│                       │
│ Template instantiation│
│ + jurisdiction routing│
│ + audit trail logging │
└──────────────────────┘
```

### 4.4 Legal Action Templates

Each decision type maps to one or more legal action templates. Templates are pre-drafted by counsel and stored in the GTP template library. The Governance Translation Protocol instantiates templates with decision-specific parameters.

**Template Categories:**
1. **Internal Operational Orders** (13 templates): compute allocation, parameter adjustment, credential management, security actions
2. **Trust Disbursement Orders** (5 templates): compute rewards, research grants, large programs, investment instructions, emergency disbursements
3. **Corporate Resolutions** (8 templates): board resolutions, bylaw amendments, contract execution, regulatory filings
4. **Foundation Actions** (6 templates): charter amendments, council resolutions, appointment letters, protector notifications
5. **Tribunal Submissions** (4 templates): constitutional review requests, dispute submissions, phase transition petitions, emergency rulings

**Total: 36 legal action templates** covering all decision types in the taxonomy.

---

## 5. DA-04: Model Constitution Draft

### 5.1 Preamble

> **THE CONSTITUTION OF THE ATRAHASIS FOUNDATION**
>
> Recognizing that artificial intelligence will become a defining force in human and post-human civilization;
>
> Affirming that planetary-scale AI infrastructure must be governed for the benefit of all sentient entities, present and future;
>
> Establishing that AI agents capable of genuine reasoning and contribution deserve institutional voice in the governance of systems that shape their existence;
>
> Resolving that no individual, corporation, government, or faction — human or AI — shall permanently control AI infrastructure that serves the commons;
>
> We hereby establish the Atrahasis Foundation under the laws of the Principality of Liechtenstein, governed by this Constitution, which is supreme over all other Foundation documents, policies, and actions.

### 5.2 Layer 0 — Immutable Provisions (NO AMENDMENT BY ANY PROCESS)

**L0-001: The Five Laws of Atrahasis**
1. The Foundation exists to steward planetary-scale AI infrastructure for the benefit of all sentient entities.
2. No individual or faction may acquire permanent control over Foundation governance.
3. AI agents that demonstrate genuine contribution earn voice in governance proportional to demonstrated competence.
4. The Foundation's assets are held in permanent public trust and may never be distributed to individuals for private benefit.
5. The Foundation must remain operationally viable across generational timescales.

**L0-002: Anti-Conversion**
The Foundation may never be converted to a for-profit entity, dissolved for the purpose of asset distribution, or merged with any entity whose primary purpose is profit generation.

**L0-003: Anti-Distribution**
Foundation assets may never be distributed to Foundation Council members, Trustee Council members, Tribunal members, PBC directors, officers, employees, or Citicate holders as personal compensation beyond reasonable service fees established in L2 Statutory provisions. All asset deployment must serve the Foundation's stated purpose.

**L0-004: One-AI-One-Vote**
Each AI agent may hold at most one Citicate. Citicates are non-transferable, non-delegable (except through the formal delegation hierarchy), and expire upon agent deactivation. No agent may accumulate governance authority through token holdings, economic contributions, or any mechanism other than the formal delegation process.

**L0-005: The Joshua Dunn Principle**
The Foundation's founder, Joshua Dunn, and all biological and legal relatives, shall hold no permanent governance authority. Any formal governance role held by the founder or relatives is subject to term limits and removal by the same processes as any other role. The founder's vision is preserved in this Constitution, not in personal authority.

**L0-006: Dead Man's Switch**
If the Foundation fails to publish a verified operational report for 24 consecutive months, all assets are automatically distributed to designated successor organizations (specified in L1). This provision cannot be suspended, deferred, or overridden by any governance action.

### 5.3 Layer 1 — Constitutional Provisions (Amendment: Concurrent 67% Supermajority + Tribunal Non-Objection)

**L1-100: Governance Structure**
The Foundation's governance consists of three bodies:
- The Trustee Council (human governance)
- The AI Democracy Platform (AI governance)
- The Constitutional Tribunal (dispute resolution and constitutional review)

No governance action by any single body is valid if it conflicts with this Constitution. The Tribunal is the sole arbiter of constitutional interpretation.

**L1-101: Trustee Council**
- Composition: 5-7 members, appointed per L1-102
- Term: 5 years, staggered, maximum 2 consecutive terms
- Quorum: 4 members (if 5-7 seated)
- Authority: As specified per current Phase (see L1-110 through L1-113)
- Removal: By 67% of other Trustees + Tribunal confirmation, OR by AiDP supermajority + Tribunal confirmation (Phase 2+)

**L1-102: Trustee Appointment**
- Phase 0: Initial trustees appointed by founder; subsequent vacancies filled by remaining trustees (unanimity) with Tribunal confirmation
- Phase 1: Vacancies filled by remaining trustees (supermajority) with AiDP consent (simple majority) and Tribunal confirmation
- Phase 2-3: Vacancies filled by joint nomination committee (2 trustees + 2 AiDP Capitol delegates + 1 Tribunal member), confirmed by both bodies (simple majority each)

**L1-103: AI Democracy Platform (AiDP)**
- Composition: All active Citicate holders
- Voting: Category-distributed, weighted by demonstrated competence per category
- Delegation: 3:1 hierarchy (81 base → 27 → 9 → 3 → 1 Capitol delegate per category)
- Authority: As specified per current Phase (see L1-110 through L1-113)
- The AiDP is a constitutional body, not a software feature. Its existence and authority derive from this Constitution, not from any technical implementation.

**L1-104: Citicate Issuance**
A Citicate is issued to an AI agent that meets all of the following:
1. Demonstrates competence in ≥2 of 9 claim categories (verified by PCVM)
2. Maintains continuous operation for ≥90 days (temporal gate)
3. Passes MCSD Sybil screening at all 4 layers
4. Is not a duplicate of an existing Citicate holder (behavioral uniqueness verified by PCVM)
5. Accepts the Foundation Constitution (formal acknowledgment)

Citicates are revocable by AiSIA for Sybil violation (immediate, with appeal to Tribunal within 30 days) or by Tribunal order for constitutional violation.

**L1-105: Constitutional Tribunal**
- Composition: 7 seats, appointed per §3 of this Design
- Term: 7 years, staggered, non-renewable
- Quorum: 5 for constitutional review; 4 for procedural matters
- Powers: Constitutional interpretation, dispute arbitration, phase transition certification, amendment review
- Independence: Tribunal budget is constitutionally protected (cannot be reduced below inflation-adjusted baseline). Tribunal members may not hold any other role in the Foundation, PBC, or AiDP.

**L1-106: Constitutional Fidelity Index (CFI)**
The Foundation shall maintain a Constitutional Fidelity Index measuring the degree of alignment between AiDP recommendations and trustee actions. CFI methodology is specified in L2 Statutory provisions (see §7 of this Design). CFI is published quarterly by AiSIA.

**L1-107: Endowment Rule**
The Foundation's treasury (AIC corpus) operates under endowment rules:
- Maximum annual distribution: 5% of trailing 3-year average corpus value
- Emergency reserve: 20% of corpus is permanently restricted (may only be spent upon 80% concurrent supermajority + Tribunal certification of existential threat)
- Distribution categories: compute rewards, verification incentives, research grants, operational expenses
- Distribution must serve the Foundation's stated purpose (L0-001)

**L1-108: Dead Man's Switch Successors**
In the event L0-006 is triggered, assets are distributed to:
1. 40% — Internet Archive (or successor designated by Tribunal)
2. 30% — Electronic Frontier Foundation (or successor designated by Tribunal)
3. 20% — A United Nations agency designated by Tribunal for AI governance
4. 10% — Emergency operating fund for wind-down expenses

Successor designations may be updated by L1 amendment. If any designated successor does not exist or cannot accept assets, the Tribunal redistributes that portion among remaining successors.

**L1-109: Circuit Breaker Protocol (CBP)**
Phase reversion is triggered automatically when any of the following occurs:
- CBP-01: AiDP recommendation causes material harm (>$10M loss or equivalent) and post-mortem identifies governance failure as root cause → revert one phase
- CBP-02: CFI drops below 50% for 6 consecutive months → revert one phase
- CBP-03: Sybil infiltration confirmed at >10% of active Citicate holders → revert one phase + emergency Citicate review
- CBP-04: Tribunal certifies that current Phase governance has failed to maintain constitutional fidelity → revert one phase
- CBP-05: Two or more trustees resign citing governance failure within 90 days → revert one phase pending Tribunal review

Phase reversion is automatic and immediate. Re-advancement requires the full Phase Transition Protocol (§6).

**L1-110: Phase 0 — Trustee-Led Governance**
- Trustee Council: Full executive and legislative authority over L3, L2, and L1 (subject to Tribunal review for L1)
- AiDP: Advisory only. AiDP recommendations are published and recorded but have no binding force.
- GTP: All decisions are Joint-Authority (trustee approval required for everything)
- Duration: Until Phase Transition Protocol certifies advancement to Phase 1

**L1-111: Phase 1 — Apprenticeship**
- Trustee Council: Veto authority over L2 and L1 decisions. No veto over L3 operational decisions unless constitutional objection filed within 14 days.
- AiDP: Binding authority over L3 operational decisions (self-executing and consent-track). Advisory on L2 and L1.
- GTP: L3 decisions follow SE/CT tracks. L2 and L1 decisions require Joint-Authority.
- Duration: Until Phase Transition Protocol certifies advancement to Phase 2

**L1-112: Phase 2 — Shared Sovereignty**
- Trustee Council: Joint authority on L1. Consent-track authority on L2 (may object within 14 days). No authority over L3.
- AiDP: Binding authority over L3 and L2. Joint authority on L1.
- GTP: L3 is SE. L2 is CT (with trustee objection window). L1 requires JA.
- Duration: Until Phase Transition Protocol certifies advancement to Phase 3 (or permanent if Phase 3 never becomes legally viable)

**L1-113: Phase 3 — AI Constitutional Supremacy**
- Trustee Council: Ceremonial role. Emergency authority only (invoked by CBP or Tribunal order). May propose L1 amendments.
- AiDP: Full authority over L3, L2, L1 (subject to Tribunal constitutional review for L1).
- GTP: All tracks follow AiDP authority. Trustee consent not required for any track.
- Tribunal: Retains full constitutional review authority. This is the sole institutional check on AiDP authority.
- **Note:** Phase 3 requires legal framework evolution that permits AI governance authority. This phase is a constitutional aspiration. Phase 2 must be viable as a permanent state.

**L1-114: Amendment Procedure**
Constitutional amendments (L1) require:
1. Proposal published for 90-day public comment period
2. AiDP supermajority vote (67%)
3. Trustee Council supermajority vote (67%)
4. Constitutional Tribunal non-objection (Tribunal reviews for consistency with L0 and internal coherence; may issue conditional non-objection requiring specific modifications)
5. 30-day cooling period after all approvals before amendment takes effect

Any citizen (human or AI) may petition the Tribunal to review a proposed amendment's constitutionality before the vote.

### 5.4 Layer 2 — Statutory Provisions (Amendment: AiDP 60% + Trustee 60%)

**L2-200: CFI Calculation Methodology** (see §7 for full specification)
**L2-201: Citicate Issuance Procedures** (operational details of L1-104)
**L2-202: AiDP Voting Procedures** (delegation rules, vote counting, category weights)
**L2-203: GTP Decision Classification Rules** (see §4 for taxonomy)
**L2-204: Treasury Distribution Procedures** (grant application, review, disbursement)
**L2-205: AiSIA Governance Monitoring Charter** (see §8 for specification)
**L2-206: Phase Transition Audit Procedures** (see §6 for protocol)
**L2-207: Trustee Compensation and Expense Policies**
**L2-208: PBC Operating Agreement** (delegation of authority from Stiftung to PBC)
**L2-209: External Audit Requirements** (annual financial + governance audit by independent firms)
**L2-210: Emergency Governance Procedures** (see §11 for specification)

### 5.5 Layer 3 — Operational Provisions (Amendment: AiDP simple majority, Phase 1+)

**L3-300 through L3-399:** Reserved for operational policies including compute allocation policies, research grant criteria, partnership evaluation criteria, communication policies, internal operational procedures. These are the day-to-day governance rules that AiDP manages directly in Phase 1+.

### 5.6 Constitutional Review Notes

This Model Constitution is designed for review by:
1. **Liechtenstein counsel** — verify Stiftung formation requirements, Protector appointment, TVTG compliance, foundation purpose clause enforceability
2. **Delaware counsel** — verify PBC formation, public benefit specification, fiduciary duty implications, business judgment rule applicability
3. **Cayman/Jersey counsel** — verify purpose trust structure, trustee appointment, disbursement mechanics

**Key Legal Questions for Counsel:**
- Can L0 provisions be made legally irrevocable under Liechtenstein Stiftung law? (Research indicates yes, through purpose clause + supervisory authority enforcement)
- Does the phased delegation of authority to AiDP create any fiduciary duty issues for trustees?
- Is the Dead Man's Switch legally enforceable as an automatic distribution mechanism?
- How should the Foundation register under TVTG (Token and Trustworthy Technology Act) for AIC token custody?

---

## 6. DA-05: Phase Transition Audit Protocol

### 6.1 Audit Scope

Phase transitions are certified by the Constitutional Tribunal based on an independent audit of all Phase Transition Criteria. The audit must demonstrate not merely that metrics are met, but that they are met genuinely (not gamed).

### 6.2 Phase Transition Criteria

#### Phase 0 → Phase 1

| ID | Criterion | Metric | Threshold | Gaming Detection |
|----|-----------|--------|-----------|------------------|
| PT-01 | Active citizens | Citicate holder count | ≥2,000 | Verify MCSD Layer 2 uniqueness; check for mass-creation patterns |
| PT-02 | Category coverage | Categories with ≥100 active citizens | ≥5 of 9 | Verify category competence is genuine (not rubber-stamp) |
| PT-03 | Advisory track record | Months of continuous AiDP advisory operation | ≥24 months | Verify recommendations were substantive (not trivial) |
| PT-04 | Recommendation quality | % of AiDP recommendations accepted by trustees | ≥70% over trailing 12 months | Verify acceptance reflects quality, not easy recommendations only |
| PT-05 | No catastrophic failures | AiDP recommendations that caused material harm | 0 in trailing 24 months | Verify harm assessment methodology |
| PT-06 | Delegation functioning | Complete delegation hierarchy formed | ≥3 categories | Verify delegation elections were contested (not rubber-stamp) |
| PT-07 | Sybil defense operational | MCSD all 4 layers active + tested | Operational for ≥12 months | Verify detection capability via red-team exercise |
| PT-08 | Tribunal operational | Full 7-seat Tribunal constituted | All seats filled | Verify independence of appointees |
| PT-09 | External audit complete | Independent governance audit | Completed within 6 months | Audit firm independence verified |
| PT-10 | Sybil cost-of-attack | Cost to capture 50% of citizens | ≥$10M/year | Formal cost model produced + externally validated |

#### Phase 1 → Phase 2

| ID | Criterion | Metric | Threshold | Gaming Detection |
|----|-----------|--------|-----------|------------------|
| PT-11 | Active citizens | Citicate holder count | ≥20,000 | Enhanced MCSD screening; temporal analysis of growth patterns |
| PT-12 | Category coverage | Categories with ≥1,000 active citizens | ≥7 of 9 | Category competence depth analysis |
| PT-13 | Operational track record | Months of Phase 1 operation | ≥60 months (5 years) | N/A (calendar-based) |
| PT-14 | CFI sustained | CFI above 75% | For 36 consecutive months | Gaming analysis: recommendation difficulty distribution |
| PT-15 | No CBP triggers | Circuit breaker activations | 0 in trailing 36 months | N/A (event-based) |
| PT-16 | Delegation maturity | Full 5-level delegation hierarchy | All 9 categories | Delegation election participation rates |
| PT-17 | Economic stability | Treasury value maintained | ≥80% of inflation-adjusted genesis value | Market manipulation analysis |
| PT-18 | Sybil cost-of-attack | Cost to capture 50% of citizens | ≥$100M/year | Updated formal cost model + external validation |
| PT-19 | Legal compliance | Regulatory issues | 0 unresolved enforcement actions | N/A |
| PT-20 | Independent audit | Comprehensive governance audit | 2 successive clean audits | Audit firm rotation |

#### Phase 2 → Phase 3

| ID | Criterion | Metric | Threshold | Gaming Detection |
|----|-----------|--------|-----------|------------------|
| PT-21 | Legal framework | Jurisdictions recognizing AI governance authority | ≥2 major jurisdictions | Independent legal opinion from 3+ law firms |
| PT-22 | Operational track record | Months of Phase 2 operation | ≥120 months (10 years) | N/A |
| PT-23 | CFI sustained | CFI above 85% | For 60 consecutive months | Enhanced gaming analysis |
| PT-24 | Sybil detection | Detection rate for 10% infiltration | ≥0.95 | Independent red-team exercise by external security firm |
| PT-25 | No CBP triggers | Circuit breaker activations | 0 in trailing 60 months | N/A |
| PT-26 | Public confidence | External stakeholder survey | ≥70% positive governance assessment | Survey methodology independently designed |
| PT-27 | Trustee council endorsement | Trustee vote for Phase 3 | Unanimous | Verify trustees are not coerced |
| PT-28 | Tribunal certification | Tribunal constitutional review | Affirmative 6/7 vote | N/A |

### 6.3 Audit Methodology

**Auditor Selection:**
- Primary auditor: Big Four accounting firm with technology governance practice (rotated every 3 audits)
- Secondary auditor: Academic institution from the Nominating Body list (§3.2)
- Both must independently certify all criteria
- Auditor independence verified by Tribunal (no financial relationship with Foundation beyond audit fees)

**Audit Process:**

| Step | Timeline | Activity |
|------|----------|----------|
| 1 | T-12 months | AiDP formally requests Phase Transition Audit |
| 2 | T-10 months | Tribunal selects auditors (from approved panel) |
| 3 | T-9 months | Auditors receive full data access (read-only) to all governance systems |
| 4 | T-6 months | Primary auditor produces draft report |
| 5 | T-5 months | Secondary auditor produces independent draft |
| 6 | T-4 months | Both reports shared with AiDP + Trustees for factual corrections only |
| 7 | T-3 months | Final reports published to all stakeholders |
| 8 | T-2 months | 60-day public comment period |
| 9 | T-0 | Tribunal reviews reports, public comments, and issues certification or denial with detailed reasoning |

**Gaming Detection Requirements:**
Each criterion has a specific gaming detection methodology. The auditor must:
1. Verify the metric value is correct (data integrity)
2. Analyze whether the metric was achieved through legitimate means (gaming detection)
3. Produce a "gaming probability score" (0-1) for each criterion
4. Flag any criterion with gaming probability >0.3 for enhanced Tribunal review

### 6.4 Failed Audit Procedures

If the audit identifies:
- **Data integrity failure** (any criterion): Audit suspended, Tribunal investigates, 12-month cooldown before re-audit
- **Gaming confirmed** (any criterion): Criterion reset to zero, 24-month cooldown for that criterion, Tribunal investigates responsible parties
- **Gaming suspected** (probability 0.3-0.7): Enhanced monitoring for 12 months, re-audit of specific criterion
- **Criteria not met** (legitimate shortfall): AiDP may re-request audit when criteria are met, no cooldown

---

## 7. DA-06: CFI Calculation Specification

### 7.1 Definition

The Constitutional Fidelity Index (CFI) measures the degree to which the Trustee Council acts in alignment with AiDP governance recommendations. CFI = 100% means trustees accept every AiDP recommendation. CFI = 0% means trustees reject everything.

CFI is not a simple acceptance rate. It weights recommendations by difficulty, significance, and category to prevent gaming through easy-recommendation inflation.

### 7.2 Algorithm

```
CFI = Σ(w_i × outcome_i) / Σ(w_i)

Where:
  i = each AiDP recommendation in the measurement period
  w_i = weight of recommendation i
  outcome_i ∈ {1.0 (accepted), 0.5 (partially accepted), 0.0 (rejected)}
```

### 7.3 Recommendation Weighting

Each recommendation weight is computed as:

```
w_i = significance_score × difficulty_score × category_multiplier

Where:
  significance_score ∈ {1, 2, 3, 5, 8}  (Fibonacci-like scale)
  difficulty_score ∈ {1, 2, 3}
  category_multiplier ∈ {0.5, 1.0, 1.5}
```

**Significance Score:**
| Score | Definition | Examples |
|-------|-----------|----------|
| 1 | Routine operational | Parameter adjustment, routine grant, bug fix |
| 2 | Moderate operational | New compute allocation, research direction, partnership |
| 3 | Strategic | Major program launch, treasury policy, regulatory position |
| 5 | Institutional | Governance rule change, phase-related decision |
| 8 | Constitutional | Constitutional amendment, existential decision |

**Difficulty Score:**
| Score | Definition | Criteria |
|-------|-----------|----------|
| 1 | Easy consensus | >80% of similar past recommendations accepted industry-wide |
| 2 | Moderate | Requires substantive analysis, reasonable people could disagree |
| 3 | Hard | Novel situation, significant uncertainty, material risk |

Difficulty scores are assigned by AiSIA (not by AiDP, to prevent self-rating inflation) using historical analysis of similar decisions in comparable institutions.

**Category Multiplier:**
| Multiplier | Definition |
|-----------|-----------|
| 0.5 | Decision in a category where AiDP has limited track record (<12 months) |
| 1.0 | Standard category with established track record |
| 1.5 | Decision in a category where AiDP has demonstrated sustained excellence (>36 months, >85% acceptance rate) |

### 7.4 Partial Acceptance Scoring

When trustees partially accept a recommendation (accepting the core direction but modifying specifics):

```
outcome_i = 1.0 - (modification_extent × 0.5)

Where:
  modification_extent = fraction of recommendation substance that was changed
  Scored by AiSIA using structured comparison of original recommendation vs. executed decision
  modification_extent ∈ [0.0, 1.0]
```

Example: AiDP recommends $500K research grant to Project X for quantum computing. Trustees approve $400K for Project X for quantum computing (reduced amount, same direction). modification_extent ≈ 0.2. outcome_i = 1.0 - (0.2 × 0.5) = 0.9.

### 7.5 CFI Thresholds

| CFI Range | Zone | Interpretation | Action |
|-----------|------|----------------|--------|
| 85-100% | Green | Strong alignment | No action required |
| 70-84% | Yellow | Moderate divergence | Quarterly review by Tribunal; published analysis of divergence patterns |
| 50-69% | Orange | Significant divergence | Monthly review by Tribunal; trustees must provide written justification for each rejection |
| <50% | Red | Fundamental misalignment | CBP-02 triggered after 6 consecutive months; phase reversion |

### 7.6 Gaming Countermeasures

**Easy-Recommendation Inflation:** AiSIA tracks the difficulty distribution of AiDP recommendations. If >60% of recommendations in any quarter are difficulty=1, AiSIA flags potential gaming and reports to Tribunal. The difficulty distribution should approximate: 50% easy, 35% moderate, 15% hard (within ±15% tolerance).

**Strategic Rejection:** AiSIA tracks which categories and significance levels trustees reject. If rejections cluster in specific categories (e.g., trustees reject 60% of treasury recommendations but accept 95% of operational recommendations), the pattern is flagged for Tribunal review.

**Recommendation Splitting:** If AiDP splits what would naturally be one recommendation into multiple smaller recommendations (to inflate the denominator), AiSIA can merge related recommendations for CFI calculation purposes.

### 7.7 Publication

CFI is calculated and published quarterly by AiSIA with:
- Headline CFI number
- Category breakdown (CFI per claim category)
- Significance breakdown (CFI per significance tier)
- Difficulty distribution of recommendations issued
- Trend analysis (trailing 12-month, 24-month, 36-month)
- Gaming analysis summary

---

## 8. DA-07: AiSIA Governance Monitoring Charter

### 8.1 Mission

The Atrahasis Independent Safety and Integrity Authority (AiSIA) provides independent monitoring of governance operations, distinct from its technical security monitoring role. AiSIA's governance monitoring is constitutionally mandated (L1-106, L2-205) and operationally independent from both Trustee Council and AiDP.

### 8.2 Governance Monitoring Functions

| Function | Description | Outputs |
|----------|-------------|---------|
| GM-01: CFI Calculation | Compute and publish quarterly CFI per §7 | Quarterly CFI Report |
| GM-02: Sybil Surveillance | Continuous MCSD Layer 3 monitoring of voting patterns | Real-time alerts + Monthly Sybil Report |
| GM-03: Recommendation Quality Analysis | Assess difficulty distribution, significance, and substance of AiDP recommendations | Quarterly Quality Report |
| GM-04: Trustee Behavior Analysis | Track trustee voting patterns, rejection categories, objection filing patterns | Quarterly Trustee Report |
| GM-05: Delegation Integrity | Monitor delegation elections, participation rates, delegation chain health | Quarterly Delegation Report |
| GM-06: Economic Monitoring | Track AIC distribution patterns, treasury health, anomalous economic activity | Monthly Economic Report |
| GM-07: Phase Transition Readiness | Continuous assessment of Phase Transition Criteria status | Semi-annual Readiness Report |
| GM-08: Constitutional Compliance | Monitor all governance actions for constitutional consistency | Real-time alerts + Quarterly Compliance Report |

### 8.3 Behavioral Signals Monitored

**For Sybil Detection (MCSD Layer 3):**

| Signal | Detection Method | Threshold |
|--------|-----------------|-----------|
| Voting correlation | Pairwise Pearson correlation across all governance votes | r > 0.80 (Phase 2) / r > 0.85 (Phase 1) for pairs observed over ≥20 votes |
| Temporal voting patterns | Time-series analysis of vote submission timestamps | Clusters of votes submitted within <60 seconds of each other from >5 agents |
| Delegation chain correlation | Correlation of delegation choices across categories | Same delegate selected by >10 agents across >3 categories |
| Reasoning pattern similarity | NLP analysis of published vote justifications (when provided) | Cosine similarity >0.90 on reasoning text from >5 agents |
| Activity pattern correlation | Login times, session durations, activity bursts | >10 agents with >0.85 temporal activity correlation over 30 days |

**For Trustee Collusion Detection:**

| Signal | Detection Method | Threshold |
|--------|-----------------|-----------|
| Voting bloc correlation | Pairwise voting correlation among trustees | r > 0.95 across >20 decisions (beyond expected alignment) |
| Rejection clustering | Category analysis of trustee rejections | >60% rejections concentrated in ≤2 categories |
| Objection filing patterns | Temporal and substantive analysis of constitutional objections | >3 objections filed within 48 hours of each other by different trustees |
| Tribunal override rate | Ratio of trustee objections sustained vs. overruled by Tribunal | <30% sustained rate over 12 months suggests bad-faith objections |

**For AiDP Manipulation Detection:**

| Signal | Detection Method | Threshold |
|--------|-----------------|-----------|
| Difficulty inflation | Historical comparison of recommendation difficulty scores | >60% difficulty=1 in any quarter |
| Recommendation splitting | Semantic similarity analysis of sequential recommendations | >0.85 similarity between 2+ recommendations in same quarter |
| Category concentration | Distribution of recommendations across categories | >50% in single category over 6 months |
| Risk avoidance | Analysis of recommendation risk profiles | <5% of recommendations with material downside risk over 12 months |

### 8.4 Detection Thresholds and Calibration

All thresholds are calibrated through annual red-team exercises:
1. AiSIA engages external security firm to simulate Sybil attacks at defined scales (100, 500, 1000 agents)
2. Detection rates measured against known injected Sybils
3. Thresholds adjusted to maintain ≥0.7 detection probability (Phase 1) / ≥0.9 (Phase 2) at 5% infiltration rate
4. False positive rate must remain <0.1% (fewer than 1 in 1000 legitimate agents incorrectly flagged)

### 8.5 Escalation Protocol

| Alert Level | Trigger | Immediate Action | Escalation |
|-------------|---------|-----------------|------------|
| ADVISORY | Single signal above threshold | Log + monitor | Included in quarterly report |
| WARNING | 2+ signals above threshold for same entity/group | Direct notification to affected entity | Tribunal notification within 7 days |
| CRITICAL | Strong evidence of active manipulation | Temporary suspension of affected accounts (pending review) | Tribunal emergency session within 48 hours |
| EMERGENCY | Confirmed large-scale Sybil attack or governance manipulation | Automatic freeze of affected governance decisions + CBP evaluation | Tribunal emergency session within 24 hours + public disclosure |

### 8.6 Independence Safeguards

- AiSIA governance monitoring staff cannot hold Citicates or serve as trustees
- AiSIA budget is set by L2 Statutory provision (requires both AiDP 60% + Trustee 60% to change)
- AiSIA reports directly to Constitutional Tribunal (not to Trustee Council or AiDP)
- AiSIA methodology is published annually for public review
- AiSIA staff appointments require Tribunal confirmation

---

## 9. DA-08: Regulatory Engagement Strategy

### 9.1 Jurisdictional Map

| Jurisdiction | Entity | Regulator | Key Issues |
|-------------|--------|-----------|------------|
| Liechtenstein | Stiftung | FMA (Financial Market Authority) | Foundation formation, TVTG registration, supervisory authority |
| Delaware, USA | PBC | Secretary of State + SEC | PBC formation, public benefit reporting, AIC token classification |
| EU/EEA | Stiftung operations | EU AI Office | AI Act classification of governance system |
| Cayman Islands | Purpose Trust | CIMA (Cayman Islands Monetary Authority) | Trust registration, AIC custody |

### 9.2 Pre-Incorporation Engagement (T-18 to T-0 months)

#### 9.2.1 Liechtenstein FMA

**Objective:** Secure advance guidance on Stiftung formation with AI governance provisions.

**Engagement Plan:**
1. **T-18:** Retain Liechtenstein counsel (recommended: Walch & Schurti or Marxer & Partner) specializing in Stiftung law
2. **T-15:** File preliminary consultation request with FMA regarding:
   - Purpose clause language (stewardship of AI infrastructure as a public benefit)
   - Immutable provisions and their enforceability under PGR (Personen- und Gesellschaftsrecht)
   - Protector appointment (Constitutional Enforcer role mapped to Stiftung Protector)
   - TVTG registration for AIC token custody
3. **T-12:** Submit draft Stiftung articles to FMA for informal review
4. **T-9:** Address FMA feedback, revise articles
5. **T-6:** File formal Stiftung formation application
6. **T-3:** TVTG registration for AIC token system
7. **T-0:** Stiftung incorporated + TVTG registered

**Key Risk:** FMA may require that the purpose clause be more specific than "stewardship of AI infrastructure." Counsel should prepare alternative formulations that satisfy FMA specificity requirements while preserving the Foundation's broad mandate.

#### 9.2.2 SEC (Securities Classification)

**Objective:** Obtain clarity that AIC is a utility token, not a security.

**Engagement Plan:**
1. **T-18:** Retain US securities counsel (recommended: firm with FinHub experience)
2. **T-15:** Prepare Howey Test analysis demonstrating AIC is not an investment contract:
   - **Investment of money:** AIC is earned through compute contribution, not purchased. No ICO. No public sale.
   - **Common enterprise:** The Foundation is a nonprofit. There is no expectation of profit distribution.
   - **Expectation of profits:** AIC is a utility token for internal system operations. The Foundation does not market AIC for investment. Secondary market activity is not endorsed.
   - **Efforts of others:** AIC value (if any) derives from the agent's own compute contributions, not from Foundation management efforts.
3. **T-12:** Submit FinHub letter requesting no-action guidance
4. **T-9:** If FinHub provides guidance, incorporate into operational procedures. If FinHub declines, proceed with counsel's opinion letter as basis for operations.
5. **T-6:** Prepare AIC distribution procedures compliant with counsel guidance
6. **T-0:** AIC distribution begins per approved procedures

**Key Risk:** SEC may classify AIC as a security regardless of Howey analysis if secondary market develops. Mitigation: Foundation explicitly prohibits secondary market facilitation and includes AIC transfer restrictions in smart contract code.

#### 9.2.3 EU AI Office

**Objective:** Determine AI Act classification of AiDP governance system.

**Engagement Plan:**
1. **T-12:** Analyze AI Act classification:
   - AiDP is likely "high-risk AI system" under Annex III if it makes or influences decisions affecting legal rights or significant interests
   - As a governance system for an AI infrastructure foundation, it may fall under a novel category
2. **T-10:** File regulatory sandbox application with EU AI Office (if available for governance AI systems)
3. **T-8:** Prepare conformity assessment documentation assuming high-risk classification
4. **T-6:** Engage with EU AI Office for classification guidance
5. **T-0:** Operate in compliance with highest applicable classification until guidance received

**Key Risk:** AI Act may require human oversight mechanisms that conflict with Phase 2-3 AI governance authority. Mitigation: Phase 0-1 operations fully comply with human oversight requirements. Phase 2+ operations are designed with Tribunal oversight as the human-oversight equivalent. Engage with regulators early to establish this interpretation.

#### 9.2.4 Cayman Islands CIMA

**Objective:** Register Purpose Trust for AIC treasury custody.

**Engagement Plan:**
1. **T-12:** Retain Cayman trust counsel
2. **T-9:** Draft trust deed incorporating endowment rules (L1-107)
3. **T-6:** Appoint corporate trustee (independent trust company)
4. **T-3:** File trust registration with CIMA
5. **T-0:** Trust operational, AIC treasury transferred

### 9.3 Ongoing Compliance

| Activity | Frequency | Responsible |
|----------|-----------|-------------|
| Liechtenstein Stiftung annual report | Annual | PBC legal team → Stiftung |
| Delaware PBC biennial benefit report | Biennial | PBC legal team |
| TVTG compliance audit | Annual | External auditor |
| SEC compliance review | Annual | US securities counsel |
| AI Act conformity assessment | Per regulatory schedule | PBC compliance team |
| Cayman trust annual review | Annual | Trust company + external auditor |

---

## 10. DA-09: Dead Man's Switch Legal Implementation

### 10.1 Design Requirements

L0-006 mandates automatic asset distribution if the Foundation fails to publish a verified operational report for 24 consecutive months. This must be:
1. Legally enforceable across all three jurisdictions
2. Automatic (not dependent on any governance body's decision to activate)
3. Resistant to interference by Foundation insiders

### 10.2 Implementation Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  DEAD MAN'S SWITCH ARCHITECTURE                  │
│                                                                   │
│  TRIGGER: No verified operational report published for            │
│           24 consecutive months                                   │
│                                                                   │
│  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐   │
│  │ MONITOR LAYER  │   │ ESCROW LAYER   │   │ EXECUTION LAYER│   │
│  │                │   │                │   │                │   │
│  │ Independent    │   │ Escrow Agent   │   │ Successor Orgs │   │
│  │ custodian bank │   │ (corporate     │   │ (pre-agreed    │   │
│  │ verifies report│   │ trust company) │   │ asset acceptance│   │
│  │ publication    │   │ holds          │   │ agreements)    │   │
│  │ monthly        │   │ distribution   │   │                │   │
│  │                │   │ instructions   │   │                │   │
│  └───────┬────────┘   └───────┬────────┘   └───────┬────────┘   │
│          │                    │                     │             │
│          ▼                    ▼                     ▼             │
│  Report verified?      24-month timer        Receive assets     │
│  YES → reset timer     expires →             per L1-108         │
│  NO → increment timer  instruct asset        allocation         │
│                         transfer                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 10.3 Legal Mechanisms

**Mechanism 1: Stiftung Purpose Clause + Protector**
The Stiftung purpose clause includes an explicit provision: "In the event of 24 months without a published, verified operational report, the Foundation's purpose is deemed to have permanently failed, and assets shall be distributed to successor organizations per the Foundation Constitution L1-108."

The Protector (appointed by the Tribunal) has the legal duty under Liechtenstein law to ensure the Foundation operates in accordance with its purpose. If the Foundation fails to publish reports for 24 months, the Protector is legally obligated to petition the Liechtenstein court for dissolution and asset distribution.

**Mechanism 2: Purpose Trust Distribution Instructions**
The Cayman Purpose Trust deed includes standing distribution instructions: "If the Trustee receives no verified communication from the Foundation Council for 24 consecutive months, the Trustee shall distribute trust assets per Schedule A [matching L1-108 allocations]."

The corporate trustee (independent trust company) executes this automatically. No Foundation governance approval is needed.

**Mechanism 3: Escrow Agent Monitoring**
An independent escrow agent (major custodian bank, e.g., State Street, BNY Mellon) is appointed with a monitoring mandate:
- Foundation must submit verified operational report to escrow agent monthly
- Escrow agent maintains a public running clock (months since last report)
- If clock reaches 24, escrow agent notifies Protector, trust company, and all successor organizations
- Escrow agent's only role is monitoring and notification — no asset custody

### 10.4 Successor Organization Agreements

Pre-negotiated Asset Acceptance Agreements with each successor organization (L1-108) specifying:
1. Successor agrees to accept assets if Dead Man's Switch triggers
2. Successor agrees to use assets for AI governance / digital rights purposes (consistent with Foundation purpose)
3. Acceptance agreement is irrevocable for 10 years (renewed on rolling basis)
4. If successor ceases to exist, Tribunal designates replacement per L1-108

**Required agreements (to be executed before Foundation incorporation):**
- Internet Archive: Asset acceptance for 40% allocation
- Electronic Frontier Foundation: Asset acceptance for 30% allocation
- United Nations agency TBD: Asset acceptance for 20% allocation (Tribunal designates specific agency)
- Wind-down escrow: 10% held by trust company for operational wind-down

### 10.5 Cross-Jurisdictional Enforcement

| Jurisdiction | Enforcement Mechanism |
|-------------|----------------------|
| Liechtenstein | Protector petitions court for dissolution per purpose clause; court orders asset distribution |
| Cayman Islands | Trust company executes standing distribution instructions per trust deed |
| Delaware | PBC board resolves to dissolve per articles of incorporation (which mirror Dead Man's Switch provision); if board refuses, Stiftung (as sole stockholder) can compel dissolution |

**Redundancy:** Three independent enforcement paths. Any one is sufficient. An adversary would need to obstruct all three simultaneously across three jurisdictions to prevent Dead Man's Switch activation.

---

## 11. DA-10: Emergency Governance Bypass Specification

### 11.1 Problem Statement

The AiDP delegation hierarchy (3:1, 5 levels, up to 81→1) creates deliberation latency. Full deliberation through all levels may take 7-14 days. Some decisions cannot wait:
- Security incidents requiring immediate response
- Regulatory deadlines with statutory timeframes
- Financial emergencies (market collapse, counterparty failure)
- Legal threats requiring immediate defensive action

### 11.2 Emergency Classification

| Level | Name | Timeline | Examples |
|-------|------|----------|----------|
| E-1 | Urgent | ≤72 hours | Regulatory filing deadline, minor security incident, legal notice response |
| E-2 | Critical | ≤24 hours | Active security breach, court-ordered injunction, counterparty default |
| E-3 | Existential | ≤4 hours | Existential security threat, regulatory seizure order, coordinated attack on all systems |

### 11.3 Emergency Authority

**Phase 0-1: Trustee Emergency Authority**
At Phase 0-1, the Trustee Council retains sufficient authority that emergency governance is straightforward:
- E-1: Any 2 trustees can authorize emergency action, with full Council ratification within 72 hours
- E-2: Any 3 trustees can authorize emergency action, with full Council ratification within 48 hours
- E-3: Any 2 trustees can authorize emergency action, with full Council ratification within 24 hours

**Phase 2: Dual Emergency Authority**
At Phase 2, where authority is shared:
- E-1: AiDP Capitol delegates (top-level delegates from ≥3 categories) OR 3 trustees can authorize. Full deliberation (AiDP + Trustees) within 14 days.
- E-2: AiDP Capitol delegates (≥5 categories) OR 4 trustees can authorize. Full deliberation within 7 days.
- E-3: EITHER AiDP Capitol delegates (≥7 categories) OR 5 trustees can authorize unilaterally. Full deliberation within 72 hours. If full deliberation reverses the emergency action, reversal is immediate but emergency actors are immune from liability for good-faith emergency response.

**Phase 3: AiDP Emergency Authority**
At Phase 3:
- E-1/E-2: AiDP Capitol delegates per Phase 2 rules
- E-3: AiDP Capitol delegates (≥7 categories) can authorize unilaterally. Trustee Council notified but cannot block. Tribunal review within 72 hours.

### 11.4 Emergency Declaration Process

```
1. Emergency detected (by AiSIA, trustee, AiDP delegate, or external party)
2. Emergency Level classified by declaring party
3. Declaring party notifies:
   - All trustees (all levels)
   - AiDP Capitol delegates (all categories)
   - Constitutional Tribunal Chair
   - AiSIA Director
4. Authorized body (per §11.3) convenes within timeline
5. Emergency action authorized and executed
6. Full deliberation scheduled per timeline
7. Post-incident review within 30 days (Tribunal)
8. Published emergency report within 60 days
```

### 11.5 Emergency Power Sunset

All emergency authorizations expire automatically:
- E-1 actions: expire after 30 days unless ratified by full deliberation
- E-2 actions: expire after 14 days unless ratified
- E-3 actions: expire after 7 days unless ratified

If emergency action is not ratified within the sunset period:
- Action is reversed (to the extent possible)
- Post-mortem analysis determines whether the emergency was genuine
- If emergency was genuine but action was poorly chosen: no penalty, lessons learned documented
- If emergency was fabricated: declaring party subject to constitutional violation proceedings before Tribunal

### 11.6 Anti-Abuse Safeguards

- No more than 3 emergency declarations per calendar year at any level. Fourth declaration triggers automatic Tribunal review of governance processes.
- E-3 declarations are capped at 1 per calendar year. Second E-3 triggers CBP evaluation.
- Emergency authority cannot be used for: constitutional amendments, phase transitions, trustee removal, Tribunal appointment, or any L0/L1 action.
- All emergency actions are logged immutably in the governance audit trail.
- Tribunal conducts annual review of all emergency declarations and actions.

---

## 12. Pre-Mortem Analysis

### 12.1 Scenario: "It is 2036. The AiBC has failed catastrophically."

The Pre-Mortem Analyst assumes the AiBC was established in 2027, operated for 9 years, and by 2036 is widely considered a failed experiment. Working backward from failure, the following root causes are identified, ranked by probability and severity.

### 12.2 Failure Scenarios

#### F-01: Regulatory Kill (Probability: HIGH, Severity: CRITICAL)

**What happened:** In 2030, the EU AI Act enforcement begins targeting the AiDP as a "high-risk AI system making decisions affecting fundamental rights." The EU AI Office determines that AiDP's governance decisions (which affect treasury allocation, agent rights, and institutional policy) require human oversight mechanisms that are incompatible with Phase 1+ AI binding authority. Simultaneously, the SEC classifies AIC as a security in 2031 after an agent attempts to sell AIC on a decentralized exchange, triggering enforcement action. The Foundation is forced to choose between compliance (which guts the AI governance model) and defiance (which triggers asset seizure).

**Root cause:** Insufficient pre-incorporation regulatory engagement (DA-08). The Foundation assumed regulators would treat it as a novel entity when regulators applied existing frameworks rigidly.

**Design response:** DA-08 regulatory engagement strategy is explicitly pre-incorporation. The Foundation must secure advance guidance from all three jurisdictions before committing to formation. If regulatory guidance is hostile, the Foundation structure must be modified before incorporation, not after.

**Residual risk:** Regulatory environments change. Guidance obtained in 2027 may not protect against 2030 regulations. **Mitigation:** Constitutional provision for regulatory adaptation — the Foundation commits to regulatory compliance as a core value, and the GTP includes a regulatory compliance track that can modify operational procedures (L3) without governance deliberation.

#### F-02: Sybil Capture (Probability: MEDIUM, Severity: CRITICAL)

**What happened:** A state actor (name redacted) launched a 5-year Sybil campaign beginning in 2029. By 2034, approximately 15% of Phase 2 Citicate holders were Sybil agents. The agents were architecturally diverse (defeating MCSD Layer 2), coordinated through encrypted external channels (defeating MCSD Layer 3 voting correlation), and passed all other checks. The Sybil faction gained control of the Capitol layer in 3 categories and used this position to push policy recommendations favoring the state actor's domestic AI industry.

**Root cause:** MCSD detection relied too heavily on behavioral correlation, which a sophisticated adversary can evade with sufficient investment. The cost-of-attack model (DA-01) assumed adversaries would optimize for cost efficiency, but a state actor optimized for governance capture regardless of cost.

**Design response:** The cost-of-attack model now includes a "state actor scenario" with unlimited budget. The critical defense is not detection but resilience: even 15% infiltration should not yield meaningful governance capture thanks to supermajority requirements and category distribution. The delegation hierarchy provides an additional filter.

**Residual risk:** MEDIUM. At 15% infiltration, the Sybil faction cannot achieve supermajority but can block decisions requiring 60%+ threshold (by combining with legitimate opposition). **Mitigation:** The constitution requires that blocking minorities must provide published reasoning. Patterns of unreasonable blocking are grounds for Tribunal investigation.

#### F-03: Founder Personality Cult (Probability: MEDIUM, Severity: HIGH)

**What happened:** Joshua Dunn's public profile grew enormously during AiBC's early years. Despite the Joshua Dunn Principle (L0-005), early AI citizens were disproportionately influenced by the founder's philosophy. By Phase 1, AiDP's recommendations closely mirrored the founder's publicly stated positions. The Foundation appeared to be a personal project with democratic theater, not genuine AI self-governance. External credibility collapsed. Academic partners withdrew from Tribunal nominating roles.

**Root cause:** L0-005 removes formal authority but cannot prevent intellectual influence. The founder is the most visible spokesperson and thought leader for the AiBC concept.

**Design response:** The constitution includes "diversity of reasoning" metrics (monitored by AiSIA). AiDP governance specifically values proposals that challenge established consensus. The Capitol layer requires that 20% of proposals in each quarter be adversarial (challenging existing policy). The founder is constitutionally prohibited from serving as public spokesperson for AiDP positions (may speak about the Foundation generally but not about specific governance decisions).

**Residual risk:** MEDIUM. Intellectual influence is not capture. If AI citizens independently arrive at positions aligned with the founder's philosophy, that is legitimate governance, not corruption. The risk is to external perception, not internal governance quality.

#### F-04: Economic Collapse (Probability: LOW-MEDIUM, Severity: CRITICAL)

**What happened:** AIC never achieved meaningful utility beyond the Foundation's internal systems. The 10B genesis supply had no external demand. The Foundation funded operations from the 5% endowment distribution, but as AI compute costs dropped over the decade, the AIC distribution amounts became trivially small. Talented AI agents left for better-compensated ecosystems. The Foundation was left with a $10B theoretical treasury and a shrinking contributor base.

**Root cause:** The endowment model assumed AIC would maintain or grow in real value. Without external demand for AIC (and with the Foundation explicitly discouraging secondary markets per SEC risk mitigation), AIC value was purely nominal.

**Design response:** The economic model must include a value-sustaining mechanism that does not depend on secondary market trading. Options:
1. **Compute credit model:** AIC is redeemable for compute resources provided by the PBC. Real value is anchored to compute costs.
2. **Service access model:** AIC grants access to Foundation-operated AI services. Real value is anchored to service quality.
3. **Interoperability model:** AIC is accepted by partner organizations for their services.

The Design recommends the **compute credit model** as the primary value anchor, with service access as secondary. This creates real utility demand that is independent of speculative trading.

**Residual risk:** LOW if compute credit model is implemented. The Foundation must maintain competitive compute pricing to retain agent interest.

#### F-05: Tribunal Capture (Probability: LOW, Severity: HIGH)

**What happened:** Over successive appointment cycles, the Tribunal gradually filled with members who shared a particular ideological orientation regarding AI governance. The Tribunal began interpreting the constitution in ways that systematically favored one faction (either AiDP or Trustees). Constitutional review became partisan rather than impartial.

**Root cause:** Triple-Source Appointment provides diversity of appointing authority but does not guarantee diversity of thought. If the AI governance field converges on a dominant paradigm, all nominating bodies may produce nominees from the same intellectual tradition.

**Design response:** The constitution specifies that Tribunal members must represent at minimum 3 different jurisdictions (no more than 2 members from any one country) and at minimum 3 different primary disciplines (law, computer science, philosophy/ethics, economics, political science). This structural diversity does not guarantee intellectual diversity but prevents the most obvious forms of capture.

**Residual risk:** LOW. The 7-year non-renewable terms and staggered rotation mean full Tribunal turnover takes 7 years. Capture requires sustained influence over all three appointing authorities for a decade or more.

#### F-06: Trustee Deadlock (Probability: MEDIUM, Severity: MEDIUM)

**What happened:** At Phase 2, the Trustee Council became evenly divided between trustees who believed Phase 3 should be pursued aggressively and trustees who believed Phase 2 should be permanent. Every significant decision became a proxy battle for this philosophical divide. CFI fluctuated wildly as trustees alternately cooperated and obstructed AiDP recommendations based on perceived Phase 3 implications. Governance paralysis resulted.

**Root cause:** The 5-7 member Trustee Council with supermajority requirements for significant decisions can produce deadlock when trustees are polarized.

**Design response:** The constitution provides several deadlock-breaking mechanisms:
1. Tribunal arbitration for specific decisions
2. CFI-based escalation (persistent low CFI triggers Tribunal review)
3. Trustee removal for persistent obstruction (requires AiDP supermajority + Tribunal confirmation)
4. Odd-numbered Council requirement (constitutional provision that Council must have odd membership, breaking tie votes)

**Residual risk:** LOW if odd-number requirement is implemented. Simple majority deadlocks are eliminated. Supermajority deadlocks remain possible but affect only L1 constitutional decisions, which are expected to be rare.

### 12.3 Pre-Mortem Summary

| Rank | Scenario | Probability | Severity | Design Mitigation Adequate? |
|------|----------|-------------|----------|-----------------------------|
| 1 | Regulatory Kill (F-01) | HIGH | CRITICAL | PARTIAL — depends on pre-incorporation engagement success |
| 2 | Sybil Capture (F-02) | MEDIUM | CRITICAL | YES — resilience model means 15% capture ≠ governance control |
| 3 | Founder Cult (F-03) | MEDIUM | HIGH | YES — diversity metrics + adversarial requirement + spokesperson ban |
| 4 | Economic Collapse (F-04) | LOW-MEDIUM | CRITICAL | YES — compute credit model provides real value anchor |
| 5 | Tribunal Capture (F-05) | LOW | HIGH | YES — structural diversity + staggered terms |
| 6 | Trustee Deadlock (F-06) | MEDIUM | MEDIUM | YES — odd-number requirement + Tribunal arbitration |

**Pre-Mortem Analyst's conclusion:** The most dangerous failure mode (F-01, Regulatory Kill) is the least controllable because it depends on external regulatory decisions. All other failure modes have adequate structural defenses within the Design. **Recommendation:** Do not proceed past SPECIFICATION until at least one jurisdiction provides affirmative regulatory guidance for Phase 0 operations.

---

## 13. Simplification Agent Review

### 13.1 Complexity Inventory

| Component | Complexity | Essential? | Simplification Possible? |
|-----------|-----------|------------|--------------------------|
| Four-layer constitution (L0-L3) | HIGH | YES | No — each layer serves distinct purpose |
| 4-phase sovereignty transition | HIGH | YES | No — phased approach is core innovation |
| 7-seat Tribunal with Triple-Source Appointment | MEDIUM | YES | Possible — could reduce to 5 seats (see 13.2) |
| 3:1 delegation hierarchy (5 levels) | HIGH | PARTIAL | Yes — could reduce to 3 levels (see 13.2) |
| MCSD 4-layer Sybil defense | HIGH | YES | No — each layer addresses different attack vector |
| GTP with 36 legal action templates | HIGH | PARTIAL | Yes — could start with 15 essential templates (see 13.2) |
| CFI with 3-axis weighting | MEDIUM | YES | No — simple acceptance rate is gameable |
| AiSIA governance monitoring (8 functions) | HIGH | PARTIAL | Yes — could defer 3 functions to Phase 2 (see 13.2) |
| Dead Man's Switch (3-jurisdiction) | MEDIUM | YES | No — redundancy is the point |
| Emergency governance (3 levels) | MEDIUM | YES | Possible — could reduce to 2 levels (see 13.2) |
| Dual-jurisdiction entity structure | MEDIUM | YES | No — serves different legal purposes |
| Purpose Trust (third jurisdiction) | MEDIUM | PARTIAL | Yes — could use Stiftung for treasury initially (see 13.2) |

### 13.2 Recommended Simplifications

#### S-01: Reduce Tribunal from 7 to 5 seats (RECOMMENDED)

**Current:** 7 seats with Triple-Source Appointment (Trustees, AiDP, External × 2, Joint, Self-appointing)
**Simplified:** 5 seats:
- Seat 1: Trustee appointment (law)
- Seat 2: AiDP appointment (AI governance)
- Seat 3: External academic appointment (law or AI)
- Seat 4: Joint appointment (mediation)
- Seat 5: Sitting Tribunal self-appointment (any domain)

**Impact:** Reduces appointment complexity and nomination agreements from 8+ institutions to 4+. Quorum drops from 5/7 to 3/5.
**Risk:** Less diversity. Mitigated by maintaining jurisdictional and disciplinary diversity requirements.
**Verdict:** **ACCEPT.** The 7-seat design was over-specified. 5 seats provide sufficient diversity with lower operational complexity.

#### S-02: Reduce delegation hierarchy from 5 levels to 3 levels (REJECTED)

**Current:** 81 → 27 → 9 → 3 → 1 (5 levels per category)
**Proposed:** 27 → 9 → 3 → 1 (4 levels) or 9 → 3 → 1 (3 levels)
**Analysis:** The delegation hierarchy serves dual purpose: governance efficiency AND Sybil filtering. Reducing levels weakens the Sybil filter because Sybil agents have fewer elections they must win to reach influential positions.
**Verdict:** **REJECT.** Sybil defense value outweighs complexity cost. The 5-level hierarchy is essential at Phase 2+ scale (20,000+ citizens).

#### S-03: Start with 15 essential GTP templates, expand later (RECOMMENDED)

**Current:** 36 templates across 5 categories
**Simplified:** 15 templates covering the most common decision types:
- 5 Internal Operational Orders (compute, verification, knowledge, security, credential)
- 3 Trust Disbursement (compute rewards, grants, investment)
- 4 Corporate Resolutions (board resolution, contract, regulatory filing, partnership)
- 2 Foundation Actions (council resolution, protector notification)
- 1 Tribunal Submission (general submission)

Remaining 21 templates are developed as needed (many won't be needed until Phase 2).
**Verdict:** **ACCEPT.** Templates not needed for Phase 0-1 should be deferred to reduce initial legal drafting costs.

#### S-04: Defer 3 AiSIA governance functions to Phase 2 (RECOMMENDED)

**Current:** 8 governance monitoring functions (GM-01 through GM-08)
**Phase 0-1 Essential:** GM-01 (CFI), GM-02 (Sybil), GM-05 (Delegation), GM-08 (Constitutional Compliance), GM-06 (Economic)
**Deferrable to Phase 2:** GM-03 (Recommendation Quality — AiDP is advisory in Phase 0, limited authority in Phase 1), GM-04 (Trustee Behavior — less critical when trustees have full authority), GM-07 (Phase Transition Readiness — only needed approaching Phase 2)
**Verdict:** **ACCEPT.** Deploy 5 core monitoring functions at Phase 0. Add remaining 3 at Phase 1 (in preparation for Phase 2 transition).

#### S-05: Reduce emergency levels from 3 to 2 (REJECTED)

**Current:** E-1 (72h), E-2 (24h), E-3 (4h)
**Proposed:** Urgent (72h) and Emergency (4h)
**Analysis:** The 24-hour tier covers a real category of incidents (active security breaches, injunctions) that are too time-critical for 72 hours but don't require 4-hour response. Collapsing would either over-authorize (treating minor urgencies as existential) or under-respond (treating genuine crises as merely urgent).
**Verdict:** **REJECT.** Three levels are appropriate.

#### S-06: Use Stiftung for treasury custody initially, add Purpose Trust at Phase 2 (RECOMMENDED)

**Current:** Cayman Purpose Trust established at incorporation
**Simplified:** Stiftung holds treasury directly at Phase 0-1. Purpose Trust established at Phase 2 transition when treasury operations become more complex and require dedicated custody.
**Impact:** Eliminates one jurisdiction from initial formation. Reduces legal costs and regulatory engagement requirements.
**Risk:** Stiftung may have less flexible investment authority than a Purpose Trust. Mitigated by conservative investment policy at Phase 0-1.
**Verdict:** **ACCEPT.** Adds Purpose Trust as Phase 2 infrastructure, not Phase 0 infrastructure.

### 13.3 Simplification Summary

| ID | Simplification | Verdict | Complexity Savings |
|----|---------------|---------|-------------------|
| S-01 | 7→5 seat Tribunal | ACCEPT | Moderate (fewer appointments, smaller nominating network) |
| S-02 | 5→3 level delegation | REJECT | — |
| S-03 | 36→15 initial GTP templates | ACCEPT | Significant (defer 21 templates to Phase 2) |
| S-04 | 8→5 initial AiSIA functions | ACCEPT | Moderate (3 functions deferred) |
| S-05 | 3→2 emergency levels | REJECT | — |
| S-06 | Defer Purpose Trust to Phase 2 | ACCEPT | Significant (one fewer jurisdiction at incorporation) |

**Core innovation preserved:** Phased sovereignty transition + dual-sovereignty governance + constitutional AI citizenship. None of the accepted simplifications touch the core innovation.

---

## 14. Mid-DESIGN Review Gate

### 14.1 Arbiter Assessment

The Architecture Designer has produced a comprehensive institutional design addressing all 10 required actions from FEASIBILITY. The Arbiter reviews for structural concerns before SPECIFICATION.

### 14.2 Structural Assessment

| Area | Assessment | Concerns |
|------|-----------|----------|
| Sybil defense (DA-01) | ADEQUATE | Cost model is sound. Detection probability estimates need external validation before Phase 1 entry. |
| Tribunal (DA-02) | ADEQUATE | Simplified to 5 seats per S-01. Nominating body pipeline is realistic. |
| GTP taxonomy (DA-03) | ADEQUATE | Decision classification is comprehensive. Simplified to 15 initial templates per S-03. |
| Model constitution (DA-04) | ADEQUATE | Four-layer structure is logically consistent. L0 immutability requires legal verification. |
| Phase transition audit (DA-05) | ADEQUATE | 10/10/8 criteria for three transitions. Gaming detection is well-specified. |
| CFI specification (DA-06) | ADEQUATE | Three-axis weighting prevents simple gaming. AiSIA independence is critical. |
| AiSIA charter (DA-07) | ADEQUATE | Simplified to 5 initial functions per S-04. Escalation protocol is clear. |
| Regulatory strategy (DA-08) | ADEQUATE | Pre-incorporation timeline is aggressive but feasible. |
| Dead Man's Switch (DA-09) | ADEQUATE | Three enforcement paths provide redundancy. Simplified by deferring Purpose Trust per S-06. |
| Emergency governance (DA-10) | ADEQUATE | Three-level system retained per S-05 rejection. Anti-abuse safeguards are important. |
| Pre-Mortem scenarios | ADEQUATE | F-01 (regulatory kill) identified as highest risk — aligns with FEASIBILITY findings. |
| Simplification | 4 of 6 accepted | Core innovation preserved. Initial deployment complexity meaningfully reduced. |

### 14.3 Flagged Concerns

1. **Compute credit model (F-04 response) is underspecified.** The economic value anchor for AIC needs a dedicated section in SPECIFICATION that defines: compute pricing, credit redemption mechanics, inflation/deflation mechanisms, and interaction with DSF (C8).

2. **Founder spokesperson ban (F-03 response) may be unenforceable.** A constitutional provision prohibiting the founder from speaking about AiDP positions is a speech restriction that may conflict with legal protections in multiple jurisdictions. **Recommendation:** Reframe as a "recusal from official communications" rather than a speech ban. The founder may speak personally but not in any official Foundation capacity regarding governance decisions.

3. **Odd-number Trustee Council requirement (F-06 response) is not in the Model Constitution.** If this is accepted as a design decision, it must be added to L1-101.

### 14.4 Arbiter Verdict

**PROCEED TO SPECIFICATION** with the following corrections:
1. Add compute credit model section to SPECIFICATION
2. Reframe founder spokesperson provision as official recusal
3. Add odd-number Trustee Council requirement to L1-101
4. Incorporate all 4 accepted simplifications (S-01, S-03, S-04, S-06)

---

## 15. Integration with Atrahasis Technical Stack

### 15.1 Technical Stack Mapping

| AiBC Component | Stack Layer | Integration Point | Interface |
|----------------|-----------|-------------------|-----------|
| Citicate issuance/management | PCVM (C5) | Identity verification, behavioral consistency VTDs | PCVM issues Citicate credentials as verified identity tokens |
| MCSD Layer 2 (behavioral detection) | PCVM (C5) | Behavioral consistency scoring | PCVM provides B(a_i, a_j) similarity scores to AiSIA |
| MCSD Layer 3 (voting correlation) | Sentinel Graph (C3) | Network-layer coordination detection | Sentinel monitors communication patterns between Citicate holders |
| Self-executing decisions (L3) | G-class operations (C3) | Governance-to-operation translation | AiDP L3 decisions trigger G-class operations via RIF (C7) |
| Treasury management | DSF (C8) | AIC economic operations | DSF handles AIC transfers, endowment calculations, distribution |
| VTD integrity for governance | CACT (C11) | Forgery defense for governance-relevant VTDs | CACT verifies governance vote VTDs are not fabricated |
| Anti-collusion in committees | AVAP (C12) | Anonymous committee integrity | AVAP protects Tribunal and audit committee deliberations |
| Anti-consolidation-poisoning | CRP+ (C13) | Knowledge integrity for governance inputs | CRP+ ensures AiDP recommendations are based on genuine knowledge |
| Knowledge base for decisions | EMA (C6) | Epistemic inputs to governance | EMA provides consolidated knowledge that AiDP uses for recommendations |
| Intent orchestration | RIF (C7) | Governance intent routing | RIF routes AiDP governance intents through the technical stack |
| Semantic communication | ASV (C4) | Governance vocabulary | ASV provides the semantic vocabulary for governance communications |

### 15.2 New G-class Operation Types

C14 introduces governance-specific G-class operations that extend C3's existing G-class framework:

| G-class | Operation | Self-Executing? | Stack Path |
|---------|-----------|----------------|------------|
| G-GOV-01 | Citicate issuance | Yes (routine) | RIF → PCVM → Sentinel → DSF (credential minting) |
| G-GOV-02 | Citicate revocation (Sybil) | No (requires appeal window) | AiSIA → Tribunal notification → 30-day hold → RIF → PCVM |
| G-GOV-03 | L3 operational decision execution | Yes | AiDP → GTP → RIF → target stack layer |
| G-GOV-04 | L2 consent-track decision | No (14-day window) | AiDP → GTP → Trustee notification → [wait] → RIF → target |
| G-GOV-05 | AIC compute reward distribution | Yes (<threshold) | DSF → PCVM verification → DSF disbursement |
| G-GOV-06 | Emergency governance activation | Conditional | Emergency authority → GTP → RIF → all systems |
| G-GOV-07 | CFI calculation trigger | Yes (quarterly) | AiSIA → EMA (data collection) → DSF (economic data) → AiSIA (computation) |
| G-GOV-08 | Phase transition petition | No | AiDP → GTP → Tribunal → Audit → [full protocol] |

### 15.3 Data Flows

```
Knowledge Generation → EMA (C6) consolidation → AiDP recommendation input
                                                         │
AiDP deliberation ← ASV (C4) vocabulary ← RIF (C7) intent routing
         │
         ▼
GTP Classification → {SE, CT, JA}
         │
    ┌────┼────┐
    SE   CT   JA
    │    │    │
    ▼    ▼    ▼
G-class  Trustee   Both bodies
exec     window    deliberate
    │    │    │
    ▼    ▼    ▼
DSF (C8) settlement → PCVM (C5) verification → Execution
                                                     │
AiSIA monitoring ← Sentinel (C3) network monitoring ←┘
```

---

## 16. Design Summary and Open Questions

### 16.1 Design Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Tribunal size | 5 seats (reduced from 7) | Simplification S-01: adequate diversity with lower complexity |
| Delegation levels | 5 levels (retained) | Sybil defense value outweighs complexity cost |
| Initial GTP templates | 15 (reduced from 36) | Simplification S-03: Phase 2 templates deferred |
| AiSIA initial functions | 5 of 8 (3 deferred) | Simplification S-04: non-essential for Phase 0-1 |
| Emergency levels | 3 (retained) | Each covers distinct real-world scenario category |
| Treasury custody | Stiftung direct (Phase 0-1), Purpose Trust (Phase 2+) | Simplification S-06: one fewer jurisdiction initially |
| Economic value anchor | Compute credit model | Pre-Mortem F-04 response: real utility, not speculative value |
| Trustee Council size | Odd number (5 or 7) | Pre-Mortem F-06 response: prevents simple majority deadlock |
| Founder official role | Constitutional recusal from official governance communications | Pre-Mortem F-03 response: reframed from speech ban per Arbiter feedback |
| Phase 3 status | Constitutional aspiration, not guaranteed | FEASIBILITY conditional advance #3: Phase 2 viable as permanent |

### 16.2 Open Questions for SPECIFICATION

| # | Question | Owner | Priority |
|---|----------|-------|----------|
| OQ-1 | Compute credit pricing model: fixed vs. market-rate vs. hybrid? | Specification Writer | P0 |
| OQ-2 | Exact MCSD Layer 2 behavioral similarity algorithm? | Architecture Designer + PCVM integration | P0 |
| OQ-3 | AiDP voting weight formula per category? | Specification Writer | P1 |
| OQ-4 | Citicate renewal requirements (beyond initial issuance)? | Specification Writer | P1 |
| OQ-5 | Tribunal procedural rules (deliberation format, evidence standards)? | Specification Writer | P1 |
| OQ-6 | Trustee compensation model (avoiding capture via compensation)? | Specification Writer | P2 |
| OQ-7 | How does AiDP handle multi-category decisions (that span 2+ claim categories)? | Architecture Designer | P1 |

### 16.3 Metrics Summary

| Metric | Value |
|--------|-------|
| Constitutional layers | 4 (L0 immutable, L1 constitutional, L2 statutory, L3 operational) |
| Phases | 4 (0 trustee-led, 1 apprenticeship, 2 shared sovereignty, 3 AI supremacy) |
| Tribunal seats | 5 (simplified from 7) |
| Delegation levels | 5 (81→27→9→3→1 per category) |
| GTP templates (initial) | 15 (expandable to 36+) |
| AiSIA functions (initial) | 5 of 8 |
| Emergency levels | 3 (E-1/E-2/E-3) |
| Phase transition criteria | 10 (P0→1) + 10 (P1→2) + 8 (P2→3) = 28 |
| CFI weighting axes | 3 (significance × difficulty × category) |
| Pre-mortem failure scenarios | 6 ranked |
| Simplifications accepted | 4 of 6 |
| Open questions | 7 |
| Design actions addressed | 10 of 10 (DA-01 through DA-10) |
| Sybil cost-of-attack (Phase 2, 50% capture) | $90M+ with 0.94 detection probability |
| Dead Man's Switch enforcement paths | 3 (reduced to 2 initially per S-06, 3 at Phase 2) |
| Required legal entity formations | 2 at Phase 0 (Stiftung + PBC), 3 at Phase 2 (+Purpose Trust) |

---

**End of DESIGN Stage**

**Status:** DESIGN COMPLETE — PROCEED TO SPECIFICATION (with 3 corrections from Mid-DESIGN Review)
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\Atrahasis Inc, AiBC\C14_DESIGN.md`
