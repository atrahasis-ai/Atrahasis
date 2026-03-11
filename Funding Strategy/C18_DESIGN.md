# C18 --- Funding Strategy + Business Operations --- DESIGN DOCUMENT

**Invention ID:** C18
**Stage:** DESIGN
**Date:** 2026-03-11
**Concept:** C18-A+ v1.1 (Staged Portfolio Funding with W0 Pivot)
**Prior Stages:** IDEATION (C18-A+ selected), RESEARCH (landscape validated), FEASIBILITY (CONDITIONAL_ADVANCE with 12 design actions)
**Budget Target:** $10M--$12M over 30--36 months (revised per DA-01)

---

# TABLE OF CONTENTS

1. [Design Actions Traceability Matrix](#section-1)
2. [Founding Capital Strategy (DA-02, DA-12)](#section-2)
3. [Grant Application Portfolio (DA-04, DA-05)](#section-3)
4. [Compensation Architecture (DA-03, DA-06, DA-08)](#section-4)
5. [Cash Flow Model (DA-01, DA-07, DA-12)](#section-5)
6. [PBC Revenue Operations](#section-6)
7. [Pitch Deck Outline](#section-7)
8. [Legal/Regulatory Preparation (DA-08, DA-10, DA-11)](#section-8)
9. [Risk Mitigation (DA-09, DA-10)](#section-9)
10. [Simplification Agent Review](#section-10)
11. [Mid-Design Review Gate](#section-11)
12. [Formal Requirements](#section-12)

---

<a id="section-1"></a>
# SECTION 1 --- DESIGN ACTIONS TRACEABILITY MATRIX

Every design action from the FEASIBILITY verdict is resolved below. This table provides traceability from feasibility finding to design resolution.

| DA ID | Feasibility Requirement | Design Section | Status |
|-------|------------------------|----------------|--------|
| DA-01 | Revise budget to $10M--$12M; drop $8M lower bound | Sec 5 (Cash Flow Model) | RESOLVED --- $10.2M baseline, $12.1M full ramp |
| DA-02 | Model all 4 founding capital options with cash flow | Sec 2 (Founding Capital Strategy) | RESOLVED --- 4 options modeled, Option B-D hybrid recommended |
| DA-03 | Design AIC dashboard and vesting visualization | Sec 4.4 (AIC Dashboard Specification) | RESOLVED --- 6-panel dashboard specified |
| DA-04 | Grant application calendar for 6+ programs | Sec 3 (Grant Application Portfolio) | RESOLVED --- 9 programs calendared |
| DA-05 | Identify 2--3 university co-PI collaborators | Sec 3.5 (Academic Partnership Strategy) | RESOLVED --- 3 target profiles specified |
| DA-06 | ZKP hiring contingency (academic, consulting, defer) | Sec 4.6 (ZKP Hiring Contingency) | RESOLVED --- 3-tier contingency designed |
| DA-07 | Part-time CFO in Phase 1 budget ($60K--$80K/year) | Sec 5.4 (Overhead and Support) | RESOLVED --- 0.5 FTE from Month 7 |
| DA-08 | Employment tax counsel for 409A PVR ($15K--$25K) | Sec 8.3 (Employment Law) | RESOLVED --- $20K budgeted, Month -1 |
| DA-09 | CTO as first/second hire; co-leadership ramp | Sec 9.2 (Key Person Risk) | RESOLVED --- CTO is hire #1 or #2 |
| DA-10 | Key-person insurance ($3M--$5M, $5K--$8K/year) | Sec 9.2 (Key Person Risk) | RESOLVED --- $4M policy, Month 1 |
| DA-11 | Regulatory counsel FMA + SEC ($35K--$75K) | Sec 8.4 (Token Regulatory Strategy) | RESOLVED --- $50K budgeted, phased engagement |
| DA-12 | $200K ring-fenced operating reserve in founding capital | Sec 2.5 (Operating Reserve) | RESOLVED --- $200K reserve within founding capital |

---

<a id="section-2"></a>
# SECTION 2 --- FOUNDING CAPITAL STRATEGY

## 2.1 The Irreducible Constraint

The FEASIBILITY stage confirmed: nothing happens without $750K--$1M in founding capital. This section models all four options identified in DA-02, provides a decision framework, and recommends the optimal path.

**Minimum requirement:** $950K--$1.2M (revised upward from $750K--$1M per DA-12 to include $200K ring-fenced operating reserve).

## 2.2 Option A: Solo Founder Investment

**Structure:** Joshua Dunn contributes $950K--$1.2M from personal liquid assets.

| Parameter | Value |
|-----------|-------|
| Amount | $950K--$1.2M |
| Timeline to availability | Immediate (upon account transfer) |
| Legal complexity | LOW --- standard capital contribution to Stiftung |
| Governance impact | None --- Stiftung governance is independent of funding source |
| Risk concentration | EXTREME --- single individual bears 100% of Stage 0 loss risk |

**Cash Flow Projection (Option A):**

| Month | Funding In | Burn | Cumulative Spend | Cash on Hand | Runway (mo) |
|-------|-----------|------|-----------------|-------------|-------------|
| 1 | $1,000K | $95K | $95K | $905K | 9.5 |
| 2 | $0 | $95K | $190K | $810K | 8.5 |
| 3 | $0 | $95K | $285K | $715K | 7.5 |
| 4 | $0 | $130K | $415K | $585K | 4.5 |
| 5 | $0 | $130K | $545K | $455K | 3.5 |
| 6 | $0 | $130K | $675K | $325K | 2.5 * |

*Danger: runway below 3 months by Month 6 if no grant income arrives.*

**Verdict:** Option A provides maximum speed but unacceptable risk concentration. The runway drops below 3 months by Month 6 even at the high end ($1.2M founding), unless grants or other income arrive. **NOT RECOMMENDED as sole strategy.**

## 2.3 Option B: Co-Founder Capital

**Structure:** Joshua Dunn ($400K--$600K) + 1--2 co-founding partners ($250K--$500K each).

| Parameter | Value |
|-----------|-------|
| Amount | $950K--$1.5M |
| Timeline to availability | 4--8 weeks (partner identification, legal agreements, fund transfer) |
| Legal complexity | MEDIUM --- co-founder agreements, Stiftung board composition, role definition |
| Governance impact | Co-founders join Stiftung board or PBC leadership |
| Risk distribution | Shared across 2--3 individuals |

**Co-Founder Value Proposition:**

A co-founding partner contributes capital AND one of the following:
- **Technical co-founder:** Fills the CTO role (DA-09), reducing hire #1 dependency. Must have distributed systems or cryptographic protocol expertise.
- **Operations co-founder:** Fills CFO/COO function (DA-07), manages grants, compliance, and finances. Must have nonprofit or research administration experience.
- **Network co-founder:** Brings established relationships with grant-makers, AI safety community, or academic institutions (DA-05). Must be able to open doors that Joshua cannot.

**What co-founders receive:**
- Founding team recognition and Stiftung board advisory role
- AIC allocation: 0.03--0.05% of treasury (3M--5M AIC), 4-year vest with 1-year cliff
- PVR participation (same terms as senior engineers)
- No equity --- the Stiftung cannot issue equity. This must be communicated with radical honesty.

**Cash Flow Projection (Option B, $1.2M total):**

| Month | Funding In | Burn | Cash on Hand | Runway (mo) |
|-------|-----------|------|-------------|-------------|
| 1 | $1,200K | $95K | $1,105K | 11.6 |
| 3 | $0 | $95K | $915K | 9.6 |
| 6 | $0 | $130K | $525K | 4.0 |
| 9 | $500K (grant pre-finance) | $170K | $515K | 3.0 * |
| 12 | $500K (DARPA Phase 1) | $200K | $515K | 2.6 * |

*Still tight, but the higher initial capital provides critical additional months.*

**Verdict:** Option B is stronger than A but requires finding mission-aligned individuals willing to contribute $250K+ to a nonprofit with speculative returns. **RECOMMENDED if a suitable co-founder can be identified within 8 weeks.**

## 2.4 Option C: Angel Syndicate (Founding Patrons)

**Structure:** Joshua Dunn ($400K--$600K) + 5--10 "Founding Patrons" ($50K--$100K each).

| Parameter | Value |
|-----------|-------|
| Amount | $900K--$1.6M |
| Timeline to availability | 8--16 weeks (syndicate formation, legal structuring, securities compliance) |
| Legal complexity | HIGH --- must structure to avoid securities law violations |
| Governance impact | Founding Patrons receive advisory roles, not governance authority |
| Risk distribution | Broadly distributed |

**Founding Patron Program Structure:**

| Tier | Contribution | AIC Allocation | Benefits |
|------|-------------|---------------|----------|
| Founding Patron (Gold) | $100K+ | 0.01% of treasury (1M AIC) | Advisory Board seat, quarterly briefings, name on founding charter, priority ecosystem access |
| Founding Patron (Silver) | $50K--$99K | 0.005% of treasury (500K AIC) | Quarterly briefings, name on founding charter, priority ecosystem access |

**Legal Structure for Patron Program:**
- Contributions are structured as **charitable donations** to the Stiftung (not investments)
- AIC allocations are **gratitude allocations** from the Stiftung treasury (not securities)
- No promise of financial return --- AIC is explicitly described as having zero current market value
- Legal opinion required: Liechtenstein counsel confirms Stiftung can make gratitude allocations; US counsel confirms no securities offering under Howey (no expectation of profit from efforts of others, because AIC is a utility token and contributions are donations, not investments)
- Estimated legal cost: $25K--$40K for dual-jurisdiction opinion

**Critical risk:** If 3+ patrons contribute $100K+ each, this may resemble a "pooled investment" regardless of legal framing. SEC or FMA could challenge. Mitigation: limit the Founding Patron pool to 8 individuals and structure each as an independent donation, not a syndicated round.

**Verdict:** Option C provides the most resilient capital base but introduces significant legal complexity. **RECOMMENDED only if legal counsel confirms compliance.** Timeline: 12--16 weeks including legal structuring.

## 2.5 Option D: Parallel Grant Track

**Structure:** Joshua Dunn ($400K--$600K) + parallel application to Open Philanthropy or similar for pre-seed grant ($250K--$500K).

| Parameter | Value |
|-----------|-------|
| Amount | $650K--$1.1M |
| Timeline to availability | Joshua's capital: immediate. Grant: 3--6 months from application |
| Legal complexity | LOW --- standard grant application |
| Governance impact | Grant terms may include reporting requirements and milestone conditions |
| Risk distribution | Partially externalized |

**Parallel Grant Targets:**

| Program | Amount | Application Timeline | Decision Timeline | Probability |
|---------|--------|---------------------|-------------------|-------------|
| Open Philanthropy (AI safety) | $250K--$500K | Month -2 to Month 0 | 2--4 months | 25--35% |
| Survival Fund | $100K--$250K | Month -1 to Month 0 | 1--3 months | 15--25% |
| Patrick J. McGovern Foundation | $100K--$250K | Month 0 | 3--6 months | 10--20% |

**Expected value of parallel grants:** 0.25 x $375K + 0.20 x $175K + 0.15 x $175K = $94K + $35K + $26K = $155K. This is supplementary, not foundational.

**Verdict:** Option D is the safest but slowest. The grant income may arrive too late to prevent a runway crisis if Joshua's personal capital is at the lower end ($400K). **RECOMMENDED as a parallel track regardless of which primary option is chosen.**

## 2.6 Recommended Founding Capital Strategy: B+D Hybrid

**The recommended strategy combines Options B and D:**

1. **Joshua Dunn contributes $500K** (Month 0)
2. **1 co-founding partner contributes $300K--$500K** (Month 0--1)
3. **Parallel pre-seed grant application to Open Philanthropy** (submitted Month -2, decision Month 2--4)
4. **$200K ring-fenced operating reserve** (within the $800K--$1M total)

**Why B+D:**
- Total founding capital: $800K--$1.0M (before grants) or $1.05M--$1.5M (if Open Philanthropy funds)
- Risk is distributed between 2 individuals, not concentrated on 1
- The co-founder adds operational capability (CTO or COO), not just capital
- The parallel grant validates the concept externally
- If the grant is awarded, it extends runway by 3--4 months at W0 burn rates
- If the grant is not awarded, founding capital alone covers 8--10 months

**Decision Framework:**

```
IF Joshua can identify a co-founder within 8 weeks:
    → Execute Option B+D (target: $1M+ founding capital)
ELSE IF Joshua can commit $750K+ personally:
    → Execute Option A+D (higher risk, faster start)
ELSE IF Joshua can commit $500K and legal counsel approves patron structure:
    → Execute Option C+D (3-5 patrons at $50K-$100K each)
ELSE:
    → Project cannot launch. Reduce scope to solo research + grant applications.
```

**Milestone Timeline:**

| Week | Milestone |
|------|-----------|
| W-12 | Submit Open Philanthropy pre-seed application |
| W-8 | Begin co-founder search (personal network, AI safety community, distributed systems community) |
| W-4 | Co-founder identified and committed (or: decision to proceed with Option A or C) |
| W-2 | Legal agreements signed, capital transferred to PBC operating account |
| W0 | Stiftung formally established, PBC incorporated, first engineering hires begin |

---

<a id="section-3"></a>
# SECTION 3 --- GRANT APPLICATION PORTFOLIO

## 3.1 Grant Calendar (DA-04)

Nine target programs, organized by tier, with full timeline modeling.

### Tier 1: Submit Pre-W0 or During W0 (Month -2 to Month 3)

#### Grant G-01: Open Philanthropy --- AI Safety Infrastructure

| Parameter | Detail |
|-----------|--------|
| **Program** | Open Philanthropy, AI Safety & Governance |
| **Ask** | $500K--$2M |
| **Applying entity** | Stiftung (global) or PBC (US-based) |
| **Application type** | Rolling; submit concept note, invited to full proposal |
| **Alignment** | VERY HIGH --- "structural alternative to profit-driven AI labs" maps directly to OP's theory of change |
| **Success probability** | 25--35% (first-time applicant, but strong mission fit) |
| **Submit** | Month -2 (concept note) |
| **Decision** | Month 1--3 |
| **First disbursement** | Month 2--4 (lump sum or 2 tranches) |
| **Grant narrative angle** | "Pre-registered AI infrastructure experiment with kill criteria. The only AI research project designed from Day 1 as a public-benefit institution with constitutional safeguards against profit conversion. $750K buys a definitive answer within 3 months." |

#### Grant G-02: EU Horizon Europe --- AI Security and Robustness (HORIZON-CL4-2026-DIGITAL-EMERGING)

| Parameter | Detail |
|-----------|--------|
| **Program** | Horizon Europe, Cluster 4, Digital/Emerging Technologies |
| **Ask** | EUR 3--4M (consortium, Stiftung as coordinator or partner) |
| **Applying entity** | Stiftung (EEA-eligible) |
| **Application type** | Call-based; 2-stage evaluation |
| **Alignment** | HIGH --- formal verification economics (C5 PCVM), adversarial robustness (C11 CACT, C12 AVAP) |
| **Success probability** | 12--18% (competitive, but EEA diversity + novel approach boost) |
| **Submit** | Month 1--2 (Stage 1 proposal) |
| **Decision (Stage 1)** | Month 5--7 |
| **Full proposal** | Month 7--9 |
| **Decision (final)** | Month 10--13 |
| **First disbursement** | Month 12--15 (40% pre-financing at grant agreement signature) |
| **Grant narrative angle** | "Verifiable AI infrastructure: economic incentives for formal verification of AI outputs. Addresses AI Act compliance requirements for high-risk AI systems through novel verification economics." |
| **Consortium requirement** | 1--2 academic partners required. See Sec 3.5. |

#### Grant G-03: Open Philanthropy --- AI Governance Mechanisms

| Parameter | Detail |
|-----------|--------|
| **Program** | Open Philanthropy, AI Governance |
| **Ask** | $250K--$1M |
| **Applying entity** | PBC |
| **Alignment** | HIGH --- AiBC governance structure (C14), constitutional AI governance |
| **Success probability** | 20--30% (governance focus is timely post-OpenAI conversion) |
| **Submit** | Month 2 (with W0 preliminary framing) |
| **Decision** | Month 4--6 |
| **First disbursement** | Month 5--7 |
| **Grant narrative angle** | "Operational testing of the first AI governance constitution with immutable safeguards. The AiBC structure implements lessons from OpenAI's failed nonprofit governance in a legally binding framework." |

### Tier 2: Submit During W0 With Preliminary Results (Month 3--6)

#### Grant G-04: DARPA I2O BAA --- Trustworthy AI Verification

| Parameter | Detail |
|-----------|--------|
| **Program** | DARPA I2O, BAA HR001126S0001 |
| **Ask** | $1M--$3M (Phase 1: 12--18 months) |
| **Applying entity** | PBC (US entity required) |
| **Alignment** | HIGH --- C5 PCVM verification, C11 CACT anti-forgery, C12 AVAP anti-collusion |
| **Success probability** | 10--15% (highly competitive, first-time performer) |
| **Submit** | Month 4 (abstract); Month 5 (full proposal if invited) |
| **Decision** | Month 8--10 |
| **First disbursement** | Month 10--12 |
| **Grant narrative angle** | "Multi-agent verification and anti-collusion systems with pre-registered performance benchmarks. Phase 1 deliverable: empirically validated verification economics model with quantitative cost-of-attack analysis." |
| **W0 evidence** | Experiment 1 (tidal scheduling) and Experiment 2 (ZKP verification costs) results strengthen the proposal |

#### Grant G-05: Schmidt Futures --- AI Governance Infrastructure

| Parameter | Detail |
|-----------|--------|
| **Program** | Schmidt Futures, Technology & Society |
| **Ask** | $500K--$1.5M |
| **Applying entity** | Either |
| **Alignment** | HIGH --- AI governance standards, public-benefit AI |
| **Success probability** | 15--20% (invitation-based; requires warm introduction) |
| **Submit** | Month 3--4 (via introduction) |
| **Decision** | Month 6--9 |
| **First disbursement** | Month 7--10 |
| **Key dependency** | Requires a warm introduction from someone in Schmidt's network. DA-05 academic partners may provide this. |

#### Grant G-06: Patrick J. McGovern Foundation --- Responsible AI

| Parameter | Detail |
|-----------|--------|
| **Program** | McGovern Foundation, Responsible AI |
| **Ask** | $250K--$500K |
| **Applying entity** | PBC |
| **Alignment** | MEDIUM --- responsible AI, data governance |
| **Success probability** | 10--15% |
| **Submit** | Month 3 |
| **Decision** | Month 6--9 |
| **First disbursement** | Month 7--10 |

### Tier 3: Submit During W1--W2 With W0 Results (Month 6--12)

#### Grant G-07: NSF --- Distributed Systems and Formal Verification

| Parameter | Detail |
|-----------|--------|
| **Program** | NSF CISE, Distributed Computing |
| **Ask** | $500K--$2M (3 years) |
| **Applying entity** | PBC + university co-PI (required) |
| **Alignment** | MEDIUM --- C3 Tidal coordination, C7 RIF orchestration, C8 DSF settlement |
| **Success probability** | 10--15% |
| **Submit** | Month 8--10 |
| **Decision** | Month 14--18 |
| **First disbursement** | Month 16--20 |

#### Grant G-08: DOE Genesis Mission --- AI Infrastructure Challenges

| Parameter | Detail |
|-----------|--------|
| **Program** | DOE, Genesis Mission AI Grand Challenges |
| **Ask** | $5M--$10M |
| **Applying entity** | PBC |
| **Alignment** | MEDIUM --- AI infrastructure at scale |
| **Success probability** | 5--10% (large program, loosely aligned) |
| **Submit** | Month 10--12 |
| **Decision** | Month 18--24 |
| **First disbursement** | Month 20--26 |

#### Grant G-09: Ethereum Foundation ESP --- Verification Overlap

| Parameter | Detail |
|-----------|--------|
| **Program** | Ethereum Foundation, Ecosystem Support Program |
| **Ask** | $50K--$200K |
| **Applying entity** | Either |
| **Alignment** | LOW-MEDIUM --- ZKP verification, applied cryptography |
| **Success probability** | 20--30% (smaller amount, rolling, less competitive) |
| **Submit** | Month 6 |
| **Decision** | Month 8--10 |
| **First disbursement** | Month 9--11 |

## 3.2 Grant Portfolio Statistics

| Metric | Value |
|--------|-------|
| Total applications | 9 |
| Total asked | $8M--$24M |
| Expected success rate | 12--20% per application |
| Expected number funded (Year 1) | 1.3--2.2 |
| Expected total granted (Year 1) | $750K--$3M |
| Probability of zero grants (Year 1) | 15--22% |
| Probability of 2+ grants (Year 1) | 45--55% |

**Diversification principle:** No single grant represents more than 30% of the total funding plan. If any single grant fails, the project continues (with adjusted scope if necessary).

## 3.3 Grant Narrative Templates

### Template A: Philanthropic Funders (Open Philanthropy, Schmidt Futures, McGovern)

**Opening paragraph (adapt per funder):**

> The 2025 restructuring of OpenAI from nonprofit to for-profit corporation demonstrated a structural failure: no existing AI organization has governance mechanisms capable of resisting the economic pressure to abandon public-benefit missions. Atrahasis is a direct response. We are building verifiable AI infrastructure --- coordination, verification, settlement, and governance systems --- within a Liechtenstein Stiftung whose constitution immutably prohibits for-profit conversion, asset distribution to individuals, and profit extraction. This is not a policy proposal; it is running code with pre-registered experimental validation.

**Evidence section (post-W0):**

> In [Month X], we completed Wave 0 validation: four pre-registered experiments testing core architectural hypotheses. [Experiment 1] demonstrated that tidal-epoch scheduling achieves [X]% throughput improvement over static allocation in a 100-agent simulation. [Experiment 2] validated that SNARK-based claim verification costs [$X] per verification at [Y] claims/second. [Experiment 3] confirmed that [behavioral fingerprinting / knowledge synthesis] achieves [metric]. [Experiment 4] showed [result]. Full data and code are published at [repository URL].

**Ask section:**

> We request [$X] over [Y] months to fund Wave [1/2]: [specific deliverables]. This funding supports [N] engineers implementing [specific technical milestones]. Success criteria are pre-registered: [list criteria]. If criteria are not met, the project enters scope reduction per our published contingency plan.

### Template B: Government Funders (DARPA, Horizon Europe, NSF, DOE)

**Opening paragraph:**

> Current multi-agent AI systems lack trustworthy verification of outputs, coordinated resource allocation across heterogeneous providers, and formal economic settlement mechanisms. These gaps create vulnerabilities in adversarial environments: agents can forge verification credentials, collude to manipulate consensus, and extract resources without accountability. The Atrahasis architecture addresses these gaps through six integrated infrastructure layers, each specified in a formal Master Tech Spec with defined interfaces and pre-registered validation criteria.

**Technical depth section (adapt per layer):**

> C5 PCVM (Probabilistic Claim Verification Matrix) implements a verification economics model where agents post verification stakes that are slashed upon detection of fraudulent claims. The system uses SNARK proofs for computational verification and behavioral fingerprinting for semantic verification. Formal requirements: [list 5--8 key requirements from C5 spec]. Validation approach: [describe W0 Experiment 2 methodology].

**Defense relevance (DARPA-specific):**

> Multi-agent verification (C5 PCVM) and anti-collusion (C12 AVAP) directly address adversarial robustness requirements for military and intelligence applications. Behavioral fingerprinting (C17) provides agent authenticity guarantees in contested environments. The formal verification approach ensures provable correctness bounds, not just empirical confidence.

### Template C: How W0 Results Strengthen Applications

| W0 Experiment | Result Type | Grant Programs Strengthened |
|---------------|------------|---------------------------|
| Exp 1: Tidal scheduling | Throughput data, latency data, agent count scaling curves | G-02 (Horizon), G-04 (DARPA), G-07 (NSF) |
| Exp 2: ZKP verification costs | Cost-per-verification, proving time, circuit size | G-02 (Horizon), G-04 (DARPA), G-09 (Ethereum ESP) |
| Exp 3: Behavioral fingerprinting / knowledge synthesis | Detection accuracy, false positive rate, convergence speed | G-01 (OP Safety), G-04 (DARPA), G-06 (McGovern) |
| Exp 4: Settlement / economic model | Transaction throughput, settlement latency, stake economics | G-04 (DARPA), G-07 (NSF), G-08 (DOE) |

**Pre-W0 applications** (G-01, G-02, G-03) reference the experimental design and spec depth.
**Post-W0 applications** (G-04 through G-09) include quantitative results and published code.

## 3.4 Grant Timeline Visualization

```
Month:  -2  -1   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
        |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
G-01:   [SUBMIT]----[DECIDE]---[$$$]
G-02:           [---SUBMIT---]----------[S1 DECIDE]--[FULL]-----[DECIDE]---[$$$40%]
G-03:               [--SUBMIT--]----[DECIDE]---[$$$]
G-04:                           [ABSTRACT][FULL]------[DECIDE]--------[$$$]
G-05:                       [INTRO]---[SUBMIT]-------[DECIDE]---[$$$]
G-06:                           [SUBMIT]--------[DECIDE]---[$$$]
G-07:                                       [------SUBMIT------]-------[DECIDE...
G-08:                                               [------SUBMIT------]----...
G-09:                                   [SUBMIT]----[DECIDE][$$$]

W0:     |=============|
W1:                     |==================|
W2:                                         |==========================|
```

## 3.5 Academic Partnership Strategy (DA-05)

### Target Co-PI Profiles

**Profile 1: Distributed Systems / Formal Verification Faculty**
- Departments: Computer Science at ETH Zurich, TU Munich, MIT CSAIL, CMU, Imperial College London
- Expertise needed: TLA+, model checking, distributed consensus protocols
- Role: Co-PI on NSF (G-07), Horizon Europe (G-02) applications
- Value exchange: Atrahasis provides novel research problems and implementation platform; faculty provides institutional credibility, graduate students, and publication pipeline
- Target: 1 confirmed partnership by Month 3

**Profile 2: Cryptography / Zero-Knowledge Proofs Faculty**
- Departments: Applied cryptography at Stanford, UC Berkeley, Technion, ETH Zurich, University of Waterloo
- Expertise needed: SNARK/STARK systems, verification circuit design
- Role: Co-PI on DARPA (G-04), Horizon Europe (G-02); potential source of ZKP engineer hires (postdocs, PhD candidates)
- Value exchange: Novel ZKP application domain (AI verification economics); access to implementation-scale testing
- Target: 1 confirmed partnership by Month 4

**Profile 3: AI Safety / AI Governance Faculty**
- Departments: AI safety at Oxford (FHI successor), UC Berkeley (CHAI), Georgetown (CSET), Cambridge (Leverhulme Centre)
- Expertise needed: AI governance frameworks, institutional design, alignment theory
- Role: Co-PI on Open Philanthropy (G-01, G-03), Schmidt Futures (G-05); advisory board member
- Value exchange: Living laboratory for AI governance research; data on constitutional AI governance in practice
- Target: 1 confirmed partnership by Month 2

### Outreach Protocol

1. **Month -2:** Identify 6--9 specific faculty (2--3 per profile). Review recent publications for alignment.
2. **Month -1:** Send personalized introduction emails referencing their published work. Include a 2-page summary of the relevant Atrahasis specifications. Request 30-minute call.
3. **Month 0:** Conduct introductory calls. Share full specifications with interested faculty. Discuss co-PI arrangements.
4. **Month 1--2:** Formalize 2--3 partnerships. Draft joint grant proposals. Execute co-PI agreements (IP terms, publication rights, data sharing).

---

<a id="section-4"></a>
# SECTION 4 --- COMPENSATION ARCHITECTURE

## 4.1 Total Compensation Structure

Every employee receives a four-component compensation package. Each component serves a distinct motivational function.

| Component | Function | Timing | Source | Certainty |
|-----------|----------|--------|--------|-----------|
| Base salary | Living cost, market competitiveness | Monthly | PBC payroll | HIGH (guaranteed) |
| Signing bonus | Close the for-profit gap at hire | At start date | PBC operating funds | HIGH (guaranteed) |
| Wave milestone bonus | Near-term performance incentive | Upon C22 wave advancement | PBC operating funds | MEDIUM (contingent on wave success) |
| AIC allocation | Long-term speculative upside | Vests over 3 years, 1-year cliff | Stiftung treasury | LOW (speculative, no current market value) |
| Phantom Value Rights (PVR) | Bridge between cash and speculative | Paid within 2.5 months of trigger | PBC operating revenue | MEDIUM (contingent on PBC revenue and wave completion) |

## 4.2 Base Salary Schedule

Salaries are benchmarked at the 75th percentile of nonprofit technology organizations (Mozilla, Linux Foundation, Ethereum Foundation), adjusted for role scarcity.

| Role | Base Salary Range | Signing Bonus | Total Year 1 Cash (incl. est. milestone) |
|------|------------------|---------------|------------------------------------------|
| Technical Architect / CTO | $260K--$300K | $35K--$50K | $310K--$375K |
| ZKP Engineer | $220K--$260K | $30K--$40K | $265K--$325K |
| Senior Rust / Distributed Systems Engineer | $200K--$240K | $20K--$30K | $235K--$295K |
| ML/LLM Engineer | $190K--$230K | $20K--$30K | $225K--$285K |
| Protocol Engineer | $180K--$210K | $15K--$25K | $210K--$260K |
| Formal Verification (TLA+) Specialist | $190K--$230K | $20K--$30K | $225K--$285K |
| Security Engineer | $190K--$230K | $20K--$25K | $225K--$280K |
| DevOps / Infrastructure Engineer | $170K--$210K | $15K--$20K | $200K--$255K |

**Benefits package (all roles):**
- Health insurance: employer-paid premium (est. $15K--$25K/year per employee)
- 401(k) with 4% employer match
- 25 days PTO + US federal holidays
- $3K/year equipment/home office stipend
- $2K/year professional development (conferences, courses)
- Remote-first with optional co-working stipend ($250/month)

**Fully-loaded cost per engineer:** $276K/year average (base $200K + benefits $40K + payroll taxes $20K + equipment $5K + cloud allocation $6K + remote stipend $5K). Confirmed from RESEARCH stage.

## 4.3 AIC Allocation Schedule

AIC is allocated from the Stiftung treasury to employees as a long-term speculative incentive. The total employee allocation pool is 0.5% of the 10B AIC treasury (50M AIC), reserved for the first 3 years of hires.

| Role | AIC Allocation | % of Treasury | Vesting | Cliff |
|------|---------------|---------------|---------|-------|
| Founder (Joshua Dunn) | 5M AIC | 0.050% | 4 years | 1 year |
| Technical Architect / CTO | 5M AIC | 0.050% | 3 years | 1 year |
| Co-Founder (if applicable) | 3M--5M AIC | 0.030--0.050% | 4 years | 1 year |
| ZKP Engineer (W0 hire) | 2M AIC | 0.020% | 3 years | 1 year |
| Senior Engineer (W0 hire) | 1.5M AIC | 0.015% | 3 years | 1 year |
| Senior Engineer (W1 hire) | 1M AIC | 0.010% | 3 years | 1 year |
| Engineer (W2+ hire) | 500K AIC | 0.005% | 3 years | 1 year |
| Part-time CFO | 500K AIC | 0.005% | 3 years | 1 year |

**Total AIC allocated (19-person team):** ~35M--45M AIC (0.35--0.45% of treasury)
**Remaining pool for future hires:** 5M--15M AIC (0.05--0.15%)

**AIC allocation terms:**
1. AIC has zero current market value. This is stated explicitly in the allocation agreement.
2. AIC vests monthly after the 1-year cliff. Unvested AIC returns to the treasury upon departure.
3. Vested AIC is non-transferable and non-convertible until the CRF (C15 DA-01) is operational (estimated Phase 2, Month 18+).
4. Tax treatment: AIC allocation is NOT a taxable event at grant (zero fair market value). Tax liability arises only upon CRF conversion, when AIC is exchanged for fiat. This avoids the "tax on paper value" problem.
5. 83(b) election is NOT applicable (AIC is not equity in a US corporation). Allocation agreement must specify that AIC is a contractual right to a digital asset, not a property transfer.

**Notional value scenarios (for employee dashboard, not guaranteed):**

| ACI Level | Reference Price (C15 formula) | 2M AIC Value (ZKP Engineer) | 5M AIC Value (CTO) |
|-----------|------------------------------|----------------------------|---------------------|
| 0.001 (early) | ~$10 | $20M notional / 99% discount = $200K | $50M / 99% = $500K |
| 0.01 (functional system) | ~$100 | $200M notional / 95% discount = $10M | $500M / 95% = $25M |
| 0.10 (scaled system) | ~$1,000 | $2B notional / 90% discount = $200M | $5B / 90% = $500M |

*Discounts reflect illiquidity, conversion restrictions, and probability weighting. Actual realized value will vary dramatically.*

## 4.4 AIC Dashboard Specification (DA-03)

An internal web dashboard visible to all AIC holders. Six panels:

**Panel 1: My Allocation**
- Total AIC allocated
- Vested AIC (monthly calculation)
- Unvested AIC and next vesting date
- Vesting progress bar (visual)

**Panel 2: ACI Progress**
- Current ACI value (from C15 SWECV calculation or projected during pre-system phase)
- ACI history chart (monthly data points)
- ACI milestone markers (0.001, 0.01, 0.10) with projected timeline

**Panel 3: Notional Value**
- Current notional value at reference rate: Vested AIC x Reference Price
- Scenario table: notional at ACI = 0.001 / 0.01 / 0.10
- Explicit disclaimer: "Notional value is a projection based on the C15 SWECV formula. AIC has no market price and may never have market value."

**Panel 4: CRF Status**
- CRF funding level ($0 in Phase 0; target $500K--$1M in Phase 1)
- CRF conversion availability (locked / open / restricted)
- Queue position if conversion requests exist

**Panel 5: Wave Progress**
- Current wave (W0--W5)
- Wave advancement criteria status (met / in progress / not started)
- Next milestone bonus trigger

**Panel 6: PVR Status**
- PVR units held
- Current PVR trigger status (wave milestone met? PBC revenue sufficient?)
- Projected PVR payout at current trajectory

**Technical implementation:** Static web page or lightweight React app hosted on internal infrastructure. Cost: $5K--$10K to design and implement (one engineer, 1--2 weeks). Updated monthly by the financial controller.

## 4.5 Phantom Value Rights (PVR) Structure (DA-08)

### Legal Structure: Short-Term Deferral (409A-Exempt)

PVR is structured as a **short-term deferral bonus plan** to avoid IRC 409A complications:

- PVR bonuses are paid within **2.5 months of the end of the fiscal year** in which the vesting condition is met
- Vesting conditions are **objective milestones**: C22 wave advancement criteria (observable events)
- This qualifies as a "short-term deferral" exempt from 409A under Treas. Reg. 1.409A-1(b)(4)

### PVR Formula

Each employee receives PVR units at hire. PVR payout is calculated as:

```
PVR_payout = PVR_units x Wave_multiplier x PBC_revenue_factor

Where:
  PVR_units     = Granted at hire (see table below)
  Wave_multiplier = $1,000 per wave advancement (W0→W1 = $1K, W1→W2 = $1K, etc.)
  PBC_revenue_factor = MIN(1.0, PBC_quarterly_revenue / $100K)
```

The PBC_revenue_factor ensures PVR payouts only occur when the PBC has operating revenue to fund them. In Phase 0 (no revenue), the factor is 0. Once the PBC generates $100K+/quarter in revenue, the factor reaches 1.0 and PVR pays at full formula value.

**Alternative trigger (Phase 0 override):** During Phase 0 when PBC revenue is $0, PVR payouts are funded from the operating budget at 50% of formula value, provided runway exceeds 6 months. This ensures PVR has some value from Day 1.

### PVR Unit Allocation

| Role | PVR Units | Max Payout Per Wave (at full factor) | Max Total (6 waves) |
|------|-----------|-------------------------------------|----------------------|
| CTO / Technical Architect | 25 | $25,000 | $150,000 |
| ZKP Engineer | 20 | $20,000 | $120,000 |
| Senior Engineer | 15 | $15,000 | $90,000 |
| Engineer | 10 | $10,000 | $60,000 |
| Part-time CFO | 8 | $8,000 | $48,000 |

### PVR Legal Requirements

1. Written PVR plan document reviewed by employment tax counsel (DA-08, $20K budget)
2. PVR granted at hire with written allocation notice
3. Payout calculated and paid within 2.5 months of fiscal year-end in which wave advancement occurs
4. PVR is treated as ordinary income to the employee and deductible expense to the PBC
5. PVR units are forfeited upon voluntary termination (retention mechanism)
6. PVR plan is discretionary --- the PBC board (controlled by Stiftung) can amend or terminate with 90 days notice

## 4.6 ZKP Hiring Contingency (DA-06)

### Tier 1: Direct Hire (Primary)

- Post job listing on ZK-specific channels: zkjobs.com, Ethereum Foundation job board, ZK research mailing lists, academic cryptography forums
- Offer at top of range: $240K--$260K base + $40K signing bonus + 2M AIC + 20 PVR units
- Total Year 1 cash: $295K--$325K (competitive with crypto company base before equity)
- Target: hire by Month 2. If no viable candidate by Month 2, activate Tier 2.

### Tier 2: Academic Partnership (Contingency A)

- Partner with a ZKP research group (Stanford, ETH Zurich, Technion, University of Waterloo)
- Engage a postdoctoral researcher at $80K--$120K/year (academic rates) + AIC allocation
- Or: fund a PhD student's research assistantship ($40K--$60K/year) with the ZKP verification circuit as their dissertation topic
- Co-supervised by the research group PI and Atrahasis CTO
- Timeline: 4--8 weeks to formalize; researcher available Month 3--4
- Trade-off: slower ramp-up, less control, but access to cutting-edge ZKP expertise

### Tier 3: Consulting Engagement (Contingency B)

- Engage a ZKP consulting firm or independent contractor for the W0 Experiment 2 verification circuit design
- Firms: Geometry Research, Starkware consultants, independent SNARK/STARK developers
- Cost: $30K--$80K for a 2--3 month engagement to design and benchmark the verification circuit
- Trade-off: no long-term team member, but W0 Experiment 2 proceeds on schedule
- Can transition to a full-time hire if the consultant is a good fit

### Tier 4: Defer Experiment 2 (Last Resort)

- If no ZKP capability is available by Month 3, defer W0 Experiment 2 (ZKP verification economics) to W1
- W0 proceeds with 3 experiments instead of 4
- Impact: reduces W0 evidence strength for DARPA and Horizon Europe applications (which emphasize verification)
- This is acceptable --- W0 still validates 3 of 4 architectural hypotheses

**Decision timeline:**

```
Month 1: Post ZKP job listings. Begin academic outreach.
Month 2: If no direct hire candidate → activate Tier 2 (academic) AND Tier 3 (consulting)
Month 3: If neither academic nor consulting engagement secured → activate Tier 4 (defer Exp 2)
```

## 4.7 Compensation Comparison Table

| Component | Atrahasis (Year 1, Senior Eng) | FAANG (Year 1, Senior SWE) | Blockchain Startup (Year 1, Senior) |
|-----------|-------------------------------|---------------------------|-------------------------------------|
| Base salary | $200K--$240K | $200K--$300K | $180K--$250K |
| Signing bonus | $20K--$30K | $30K--$100K | $10K--$30K |
| Annual equity/token | 1.5M AIC (speculative, $0 current) | $100K--$250K RSU (liquid) | $50K--$200K tokens (partially liquid) |
| Performance bonus | $15K--$25K (wave milestone) | $20K--$60K (annual) | $0--$50K (discretionary) |
| PVR (Atrahasis-specific) | $15K per wave (up to $90K total) | N/A | N/A |
| Benefits | Full (health, 401k match, PTO, remote) | Full + perks | Varies (often limited) |
| **Total Year 1 Cash** | **$235K--$295K** | **$250K--$460K** | **$190K--$330K** |
| **Total Year 1 incl. equity** | **$235K--$295K (cash) + speculative AIC** | **$350K--$710K** | **$240K--$530K** |
| Mission premium | HIGH (founding team of public-benefit AI infrastructure) | LOW (profit-driven) | MEDIUM (varies) |
| Technical novelty | VERY HIGH (6-layer AI infrastructure, novel economics) | MEDIUM (incremental product work) | HIGH (protocol design) |

**Honest assessment:** Atrahasis Year 1 total cash ($235K--$295K for a senior engineer) is competitive with blockchain startups and 60--85% of FAANG total cash. The gap is the equity component. Atrahasis compensates with: (a) mission premium for the right candidate profile, (b) AIC speculative upside that could dramatically exceed FAANG equity IF the system succeeds, (c) founding team status and career positioning.

**Target candidate profile:** An engineer who has left or would leave a FAANG/AI lab role because of concerns about profit-driven AI development, values technical ownership (founding team, not team #47), and is willing to accept the asymmetric bet of speculative AIC upside.

---

<a id="section-5"></a>
# SECTION 5 --- CASH FLOW MODEL

## 5.1 Budget Summary (DA-01 Resolved)

**Revised total: $10.2M (baseline) to $12.1M (full ramp)**

| Category | Baseline ($10.2M) | Full Ramp ($12.1M) | Notes |
|----------|-------------------|-------------------|-------|
| Personnel | $6.8M | $8.5M | 10 avg / 14 avg engineers, 30 months |
| Signing bonuses | $180K | $350K | $20K--$40K x 6--19 hires |
| Wave milestone bonuses | $360K | $570K | $15K--$25K x 6 waves x team |
| PVR payouts | $200K | $400K | Contingent on PBC revenue |
| Cloud infrastructure | $370K | $470K | Per C22 DA-06 |
| CRF (Conversion Reserve) | $500K | $1M | Grows from Phase 2 revenue |
| Legal/regulatory/insurance | $280K | $420K | 409A ($20K), FMA/SEC ($50K), formation ($80K), ongoing ($50K/yr), insurance ($7K/yr) |
| Grant management (0.5 FTE) | $120K | $160K | Month 7 onward, $60K--$80K/year |
| Travel/conferences/recruiting | $120K | $190K | Academic outreach, hiring |
| Operating reserve (DA-12) | $200K | $200K | Ring-fenced in founding capital |
| Contingency (10%) | $1.0M | $1.2M | |
| **TOTAL** | **$10.2M** | **$12.1M** | |

## 5.2 Revenue Sources by Month

| Source | Month Available | Monthly Amount | Annual Total (Yr 1 / Yr 2 / Yr 3) |
|--------|----------------|---------------|-------------------------------------|
| Founding capital | Month 0 | One-time: $1M | $1M / $0 / $0 |
| Open Philanthropy pre-seed | Month 3--5 | One-time: $250K--$500K | $375K / $0 / $0 |
| Horizon Europe pre-finance | Month 12--15 | One-time: EUR 1.2--1.6M (~$1.3--1.7M) | $0 / $1.5M / $0 |
| Horizon Europe drawdowns | Month 15--36 | ~$80K/month | $0 / $960K / $960K |
| DARPA Phase 1 | Month 10--12 | ~$100K/month for 12 months | $300K / $900K / $0 |
| Open Phil + Schmidt (post-W0) | Month 6--10 | One-time: $500K--$1.5M | $1M / $0 / $0 |
| Consulting revenue | Month 8+ | $20K--$30K/month | $100K / $300K / $300K |
| Task marketplace | Month 20+ | $5K--$50K/month growing | $0 / $60K / $600K |
| VaaS (verification) | Month 20+ | $10K--$50K/month growing | $0 / $120K / $600K |
| Institutional membership | Month 18+ | Varies | $0 / $200K / $500K |
| **Annual Total (Expected)** | | | **$2.8M / $4.0M / $3.0M** |

## 5.3 Month-by-Month Cash Flow Projection (36 Months)

### Phase 0: Months 1--6 (Stage 0, W0)

| Month | Team | Burn | Funding In | Cash on Hand | Runway (mo) |
|-------|------|------|-----------|-------------|-------------|
| 1 | 4 | $95K | $1,000K (founding) | $905K | 9.5 |
| 2 | 5 | $105K | $0 | $800K | 7.6 |
| 3 | 6 | $115K | $0 | $685K | 6.0 |
| 4 | 6 | $125K | $375K (Open Phil pre-seed) | $935K | 7.5 |
| 5 | 6 | $130K | $0 | $805K | 6.2 |
| 6 | 6 | $130K | $0 | $675K | 5.2 * |

*Month 6 runway dips below 6 months --- this is the first stress point. W0 results should be complete. Aggressive grant follow-up and post-W0 fundraising pivot activates.*

### Phase 1: Months 7--18 (Stage 1, W1--W2)

| Month | Team | Burn | Funding In | Cash on Hand | Runway (mo) |
|-------|------|------|-----------|-------------|-------------|
| 7 | 8 | $160K | $0 | $515K | 3.2 * |
| 8 | 9 | $175K | $500K (Open Phil/Schmidt post-W0) | $840K | 4.8 * |
| 9 | 10 | $190K | $500K (Open Phil/Schmidt tranche 2) | $1,150K | 6.1 |
| 10 | 10 | $195K | $100K (DARPA Phase 1 start) | $1,055K | 5.4 * |
| 11 | 11 | $210K | $100K (DARPA) | $945K | 4.5 * |
| 12 | 11 | $215K | $100K (DARPA) + $50K (Eth ESP) | $880K | 4.1 * |
| 13 | 12 | $230K | $1,400K (Horizon Europe 40% pre-finance) | $2,050K | 8.9 |
| 14 | 12 | $235K | $100K (DARPA) | $1,915K | 8.1 |
| 15 | 13 | $250K | $100K (DARPA) + $80K (Horizon drawdown) | $1,845K | 7.4 |
| 16 | 13 | $255K | $80K (Horizon) + $20K (consulting) | $1,690K | 6.6 |
| 17 | 13 | $260K | $80K (Horizon) + $25K (consulting) | $1,535K | 5.9 * |
| 18 | 14 | $270K | $80K (Horizon) + $30K (consulting) + $100K (membership) | $1,475K | 5.5 * |

*Months 7--12 are the most dangerous period. Runway drops below 4 months at Month 12 if grants are delayed. The $200K operating reserve (DA-12) provides a 1-month buffer but does not eliminate the risk. Contingency trigger: if Cash on Hand drops below $400K (2 months burn), activate hiring freeze immediately.*

### Phase 2: Months 19--36 (Stage 2, W3--W5)

| Month | Team | Burn | Funding In | Cash on Hand | Runway (mo) |
|-------|------|------|-----------|-------------|-------------|
| 19 | 15 | $300K | $80K (Horizon) + $30K (consulting) + $20K (marketplace pilot) | $1,305K | 4.4 * |
| 20 | 15 | $305K | $80K (Horizon) + $30K (consulting) + $30K (marketplace) + $20K (VaaS) | $1,160K | 3.8 * |
| 21 | 16 | $320K | $80K (Horizon) + $500K (DARPA Phase 2) + $50K (marketplace+VaaS) | $1,470K | 4.6 * |
| 22 | 16 | $325K | $80K (Horizon) + $50K (marketplace+VaaS) | $1,275K | 3.9 * |
| 23 | 17 | $340K | $80K (Horizon) + $60K (marketplace+VaaS) + $200K (membership) | $1,275K | 3.8 * |
| 24 | 17 | $345K | $80K (Horizon) + $70K (marketplace+VaaS) + $750K (renewal grants) | $1,830K | 5.3 * |
| 25 | 17 | $350K | $80K (Horizon) + $80K (marketplace+VaaS) | $1,640K | 4.7 * |
| 26 | 18 | $360K | $80K (Horizon) + $90K (marketplace+VaaS) | $1,450K | 4.0 * |
| 27 | 18 | $365K | $80K (Horizon) + $100K (marketplace+VaaS) + $500K (grants) | $1,765K | 4.8 * |
| 28 | 18 | $365K | $100K (marketplace+VaaS) + $30K (consulting) | $1,530K | 4.2 * |
| 29 | 18 | $365K | $110K (marketplace+VaaS) + $30K (consulting) | $1,305K | 3.6 * |
| 30 | 19 | $380K | $120K (marketplace+VaaS) + $500K (membership+grants) | $1,545K | 4.1 * |
| 31 | 19 | $380K | $130K (marketplace+VaaS) + $30K (consulting) | $1,325K | 3.5 * |
| 32 | 19 | $380K | $140K (marketplace+VaaS) + $30K (consulting) | $1,115K | 2.9 * |
| 33 | 19 | $380K | $150K (marketplace+VaaS) + $750K (grants/membership renewal) | $1,635K | 4.3 * |
| 34 | 19 | $380K | $170K (marketplace+VaaS) | $1,425K | 3.8 * |
| 35 | 19 | $380K | $190K (marketplace+VaaS) | $1,235K | 3.3 * |
| 36 | 19 | $380K | $210K (marketplace+VaaS) + $250K (membership) | $1,315K | 3.5 * |

### Cash Flow Analysis

**Key observations:**

1. **Runway never exceeds 10 months.** The project operates on permanently tight margins. This is structural --- a $10M budget over 36 months with 6--19 engineers leaves no room for large reserves.

2. **There are 5 distinct danger zones** where runway drops below 4 months:
   - Month 6--7 (pre-grant, post-W0)
   - Month 10--12 (pre-Horizon disbursement)
   - Month 19--23 (Phase 2 ramp before revenue materializes)
   - Month 25--26 (between grant drawdowns)
   - Month 29--36 (transition from grants to revenue)

3. **The Horizon Europe pre-finance at Month 13 is the single most important cash event after founding capital.** If Horizon Europe is not awarded, the entire Phase 1 cash flow collapses. This is the highest-impact single grant.

4. **Revenue begins to matter at Month 24+** but does not cover burn until Month 42--48 under expected assumptions.

5. **The operating reserve ($200K) provides roughly 0.5--0.7 months of additional buffer at Phase 1--2 burn rates.** This is meaningful but not sufficient to bridge a major grant delay.

## 5.4 Expense Breakdown by Category

### Monthly Expense Composition (at steady state, Month 18)

| Category | Monthly | % of Burn |
|----------|---------|-----------|
| Payroll (14 engineers x $16.7K avg) | $233K | 86% |
| Benefits (20% of payroll) | Included above | --- |
| Cloud infrastructure | $14K | 5% |
| CFO (0.5 FTE) | $5.5K | 2% |
| Legal/compliance (amortized) | $3K | 1% |
| Insurance | $0.6K | 0.2% |
| Travel/recruiting | $3K | 1% |
| Office/remote stipends | $3.5K | 1.3% |
| Software/tools | $2K | 0.7% |
| Contingency accrual | $5K | 1.9% |
| **Total** | **$270K** | **100%** |

## 5.5 Contingency Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| **Yellow alert** | Runway < 6 months | Hiring freeze. Accelerate grant follow-up. Activate consulting revenue. Monthly board briefing. |
| **Orange alert** | Runway < 4 months | Scope reduction: defer next wave. Reduce team by 2--3 (last-in-first-out, voluntary separation preferred). Emergency fundraising sprint. |
| **Red alert** | Runway < 2 months | Emergency scope reduction to 4--5 core engineers. All non-essential spending frozen. Board emergency session. Consider bridge loan against confirmed grants. |
| **Terminal** | Runway < 1 month AND no confirmed incoming funding | Orderly wind-down. Publish all code and specifications as open source. Transfer IP to Stiftung. Notify all stakeholders. 30-day notice to employees. |

## 5.6 Scenario Analysis

### Pessimistic Scenario (25th percentile)

- Founding capital: $800K
- Grants in Year 1: $375K (only Open Philanthropy pre-seed)
- Grants in Year 2: $1.5M (one Horizon Europe)
- Revenue by Month 36: $50K/month
- **Total 36-month funding: $6.5M**
- **Outcome:** Project must reduce to 8--10 engineers by Month 12. W3--W5 delayed or simplified. Total 36-month spend: $6.5M (within available). ACI targets reduced.

### Expected Scenario (50th percentile)

- Founding capital: $1M
- Grants in Year 1: $1.9M (Open Philanthropy + DARPA start)
- Grants in Year 2: $3.5M (Horizon Europe + DARPA + Schmidt)
- Revenue by Month 36: $200K/month
- **Total 36-month funding: $10.5M**
- **Outcome:** Full team ramp (slower than ideal, reaching 19 by Month 30 instead of 24). All waves completed by Month 33. CRF funded at $500K.

### Optimistic Scenario (75th percentile)

- Founding capital: $1.2M
- Grants in Year 1: $3M (Open Philanthropy + DARPA + Schmidt)
- Grants in Year 2: $4.5M (Horizon Europe + DARPA + DOE + renewals)
- Revenue by Month 36: $500K/month
- **Total 36-month funding: $13.5M**
- **Outcome:** Full team ramp by Month 18. All waves completed by Month 27. CRF funded at $1.5M. Revenue approaching self-sustainability by Month 36.

---

<a id="section-6"></a>
# SECTION 6 --- PBC REVENUE OPERATIONS

## 6.1 Task Marketplace Launch Timeline

| Phase | Months | Milestone | Revenue |
|-------|--------|-----------|---------|
| **Pre-launch** | 1--13 | Build marketplace infrastructure as part of W1--W2 | $0 |
| **Closed alpha** | 14--16 | 3--5 invited compute providers (universities, friendly organizations). Internal testing. BRA agreements per C15 DA-02. | $0 (testing only) |
| **Closed beta** | 17--20 | 10--20 providers. Real tasks, real AIC settlement. Transaction fee: 3%. | $5K--$30K/month |
| **Open beta** | 21--27 | Public provider onboarding. Verification-as-a-Service (VaaS) launch. | $30K--$100K/month |
| **Production** | 28--36+ | Full marketplace. Enterprise integration contracts. Data licensing begins. | $100K--$500K/month |

## 6.2 Pricing Model

### Transaction Fees

| Service | Fee Structure | Expected Volume (Month 24) | Monthly Revenue |
|---------|-------------|---------------------------|-----------------|
| Compute task brokerage | 3% of task value | $500K task volume | $15K |
| Verification-as-a-Service | $0.05--$0.50 per verification | 50K verifications/month | $5K--$25K |
| Priority scheduling | 5% premium on task value | $100K priority volume | $5K |
| **Subtotal** | | | **$25K--$45K** |

### Enterprise Integration

| Service | Price | Expected Volume (Year 2--3) | Annual Revenue |
|---------|-------|---------------------------|----------------|
| Custom integration support | $50K--$200K per engagement | 2--4 engagements/year | $100K--$800K |
| Enterprise API access (annual license) | $25K--$100K/year | 3--10 licensees | $75K--$1M |
| Training/workshops | $5K--$10K per workshop | 4--8 workshops/year | $20K--$80K |

## 6.3 Provider Onboarding Strategy

### Phase 1: Seed Providers (Month 14--16)

**Target:** 3--5 providers who contribute compute in exchange for early ecosystem positioning.

| Provider Type | Approach | Value Proposition |
|---------------|----------|-------------------|
| University HPC centers | Direct outreach to academic partners (DA-05) | Research collaboration, publication, student training |
| Small cloud providers (Lambda Labs, CoreWeave) | Partnership proposal | Early integration with novel AI marketplace; competitive differentiation vs. AWS/GCP/Azure |
| Academic AI labs | Grant co-funding | Access to verified compute marketplace for their research |

**Provider onboarding requirements (per C15 DA-02):**
- Execute Bilateral Resource Agreement (BRA)
- Pass compute capability verification
- Stake minimum AIC in Settlement Plane (C8)
- Complete integration testing (API compatibility, latency requirements)

### Phase 2: Growth Providers (Month 17--27)

**Target:** 10--50 providers across Tier 1--3 compute classifications.

- Tier 1 (GPU clusters, $1M+/month capacity): 2--5 providers
- Tier 2 (mid-range GPU, $100K--$1M/month): 5--15 providers
- Tier 3 (CPU/edge compute, <$100K/month): 10--30 providers

**Onboarding funnel:**
1. Provider applies via marketplace portal
2. Technical review (compute specs, uptime history, security posture)
3. BRA negotiation and execution
4. Integration testing (2--4 weeks)
5. Staking and activation

## 6.4 Revenue Projections by Quarter

| Quarter | Task Marketplace | VaaS | Enterprise | Membership | Consulting | **Total** |
|---------|-----------------|------|-----------|------------|------------|-----------|
| Q1--Q4 (Year 1) | $0 | $0 | $0 | $0 | $0 | **$0** |
| Q5 | $0 | $0 | $0 | $0 | $30K | **$30K** |
| Q6 | $15K | $5K | $0 | $0 | $60K | **$80K** |
| Q7 | $30K | $15K | $0 | $50K | $75K | **$170K** |
| Q8 | $60K | $30K | $50K | $100K | $75K | **$315K** |
| Q9 | $100K | $50K | $100K | $75K | $50K | **$375K** |
| Q10 | $150K | $75K | $100K | $100K | $50K | **$475K** |
| Q11 | $200K | $100K | $150K | $75K | $30K | **$555K** |
| Q12 | $275K | $125K | $150K | $125K | $30K | **$705K** |

**Year 1 total revenue:** $0
**Year 2 total revenue (Q5--Q8):** $595K
**Year 3 total revenue (Q9--Q12):** $2.1M

## 6.5 Integration with C15 AIC Economics

- All marketplace transactions settle in AIC through the C8 DSF Settlement Plane
- The PBC collects transaction fees in AIC
- AIC collected as fees is either: (a) held in the PBC treasury for operational use, or (b) converted to fiat through the CRF at the current reference rate
- Provider staking follows C8 staking requirements (minimum stake per compute tier)
- Verification fees fund the C5 PCVM verification economy
- The 3% transaction fee is calibrated to fund PBC operations without making the marketplace uncompetitive vs. direct compute procurement

---

<a id="section-7"></a>
# SECTION 7 --- PITCH DECK OUTLINE

## 7.1 Target Audiences

| Audience | Primary Goal | Key Concern | Emotional Hook |
|----------|-------------|-------------|----------------|
| **AI Safety Philanthropy** (Open Philanthropy, Schmidt Futures) | Fund structural alternatives to profit-driven AI | "Is this team credible?" | OpenAI's betrayal of its nonprofit mission |
| **Government Grants** (Horizon Europe, DARPA, NSF) | Advance trustworthy AI infrastructure | "Is this technically rigorous?" | Verification and robustness are national security issues |
| **Strategic Partners** (compute providers, universities) | Position for the AI governance ecosystem | "What do I get out of this?" | Early-mover advantage in AI verification infrastructure |
| **Institutional Members** (Year 2+) | Shape AI governance standards | "Is this going to matter?" | Regulatory inevitability of AI verification requirements |

## 7.2 Deck Structure (12 slides)

### Slide 1: The Problem

**Title:** "Who Watches the AI?"

Content: AI systems making critical decisions (medical, financial, legal, military) have no trustworthy verification infrastructure. Current approaches: trust the lab that built it (conflict of interest), audit after deployment (too late), or regulate without technical mechanisms (unenforceable).

Visual: Timeline of AI failures/controversies (2023--2026) alongside growing AI deployment.

### Slide 2: The Structural Failure

**Title:** "Profit-Driven Labs Cannot Self-Govern"

Content: OpenAI (nonprofit → $500B for-profit). Anthropic ($380B valuation, investor pressure). Google DeepMind (ethics board never formed). The organizations building AI are structurally incapable of building trustworthy verification infrastructure because verification imposes costs on their business model.

Visual: OpenAI's 6 mission statement rewrites, side by side.

### Slide 3: The Solution

**Title:** "Verifiable AI Infrastructure, Public Benefit by Design"

Content: Atrahasis builds the coordination, verification, settlement, and governance layers that make any AI system accountable. Not another AI model. Not another AI lab. The infrastructure layer between AI systems and the real world.

Visual: 6-layer architecture diagram (RIF → Tidal → PCVM → EMA → DSF → ASV).

### Slide 4: How It Works (Technical Summary)

**Title:** "Six Layers, One Infrastructure"

Content: 1-sentence description of each layer. Emphasize: formal specifications (21,000 lines), 3 defense systems (forgery, collusion, poisoning), cross-layer reconciliation.

Visual: Architecture diagram with data flow arrows.

### Slide 5: Differentiation

**Title:** "Why This Is Different from OpenAI / Anthropic / Google"

| Dimension | OpenAI | Anthropic | Google | **Atrahasis** |
|-----------|--------|-----------|--------|---------------|
| Structure | For-profit PBC | For-profit PBC w/ LTBT | For-profit subsidiary | **Nonprofit Stiftung (immutable)** |
| Mission lock | None (changed 6x) | LTBT (strong but not immutable) | None | **Constitutional prohibition on conversion** |
| Verification | Self-reported | Self-reported | Self-reported | **Independent verification economics** |
| Revenue model | Product sales | Product sales | Ad-supported | **Compute marketplace + verification fees** |
| Governance | Board (captured) | LTBT (independent) | Corporate | **Stiftung + Purpose Trust Protector** |

### Slide 6: The Evidence (W0 Results)

**Title:** "We Don't Ask You to Trust Us. We Ask You to Check the Data."

Content: W0 experiment results (4 experiments, quantitative data, pre-registered kill criteria). All code published. Academic papers submitted.

Visual: Key charts from W0 experiments (throughput curves, verification costs, detection accuracy).

*Note: Pre-W0, this slide presents the experimental design and kill criteria. Post-W0, it presents results.*

### Slide 7: The Team

**Title:** "Built by Engineers, Not Executives"

Content: Founder + CTO profiles. Advisory board. Academic partners. Emphasis: deep technical credentials, not sales experience.

Visual: Team photos, institutional affiliations.

### Slide 8: The Plan (Implementation Roadmap)

**Title:** "27--36 Months, Pre-Registered Milestones"

Content: W0--W5 timeline. Each wave has defined success criteria and kill criteria. Funding gates between waves.

Visual: Gantt chart showing wave progression with milestone markers.

### Slide 9: The Business Model

**Title:** "Public Benefit, Sustainable Economics"

Content: Task marketplace (3% fee), verification-as-a-service, enterprise integration. Revenue projections by year. Path to self-sustainability by Year 3--4.

Visual: Revenue ramp chart.

### Slide 10: The Ask

**Title:** Varies by audience

- Philanthropy: "Fund the experiment. $500K--$2M for Waves 1--2."
- Government: "Trustworthy AI infrastructure research. $1M--$4M for 18 months."
- Partners: "Early ecosystem positioning. Compute credits + co-development."
- Members: "Shape AI governance standards. $100K--$250K/year."

### Slide 11: The Governance Structure

**Title:** "Built to Last, Built to Resist"

Content: Stiftung (immutable constitution) → Purpose Trust (independent Protector) → PBC (operational arm). No profit extraction. No acquisition. No conversion. Ever.

Visual: Entity structure diagram.

### Slide 12: The Opportunity

**Title:** "The Window Is Now"

Content: Post-OpenAI conversion, there is a 2--3 year window where funders, governments, and the public are receptive to structural alternatives. If Atrahasis does not exist, profit-driven labs will define AI verification standards by default.

## 7.3 Differentiation from OpenAI/Anthropic/Google Pitch

| Their pitch | Atrahasis counter |
|-------------|-------------------|
| "We'll build safe AI" | "We'll build the infrastructure that verifies whether ANY AI is safe" |
| "Trust our safety team" | "Trust the math: SNARK proofs, behavioral fingerprints, economic incentives" |
| "We need $30B" | "We need $10M and will prove it works within 3 months" |
| "We're a PBC with a trust" | "We're a Stiftung with an immutable constitution and an independent Protector" |
| "Revenue from our AI products" | "Revenue from verification of everyone's AI products" |

## 7.4 W0 Results as Evidence Package

The evidence package (prepared post-W0) includes:

1. **Technical report:** Quantitative results from 4 experiments, methodology, raw data
2. **Academic paper(s):** Submitted to relevant conferences (NSDI, SOSP, ACM CCS, IEEE S&P)
3. **Open-source repository:** All W0 code, benchmarks, and configuration files
4. **1-page executive summary:** Non-technical summary of what was validated and what it means
5. **Video demonstration:** 5-minute narrated walkthrough of key experiments and results

This package is included with every grant application, partnership proposal, and philanthropic pitch from Month 4 onward.

---

<a id="section-8"></a>
# SECTION 8 --- LEGAL AND REGULATORY PREPARATION

## 8.1 Stiftung Formation (Liechtenstein)

### Steps and Timeline

| Step | Timeline | Cost | Notes |
|------|----------|------|-------|
| 1. Engage Liechtenstein counsel | Month -3 | $5K retainer | Identify firm with Stiftung and TVTG experience |
| 2. Draft Stiftung statutes (Stiftungsurkunde) | Month -3 to -2 | $15K--$25K | Must include: immutable purpose clause, constitutional layers (C14), prohibition on profit conversion, Purpose Trust provisions |
| 3. Appoint Foundation Council | Month -2 | $0 (but ongoing council fees: $10K--$20K/year) | Minimum 2 members; 1 must be Liechtenstein-licensed trustee |
| 4. Deposit minimum capital | Month -1 | CHF 30,000 ($33K) | Minimum required by PGR Art. 552 §27 |
| 5. File with Commercial Register | Month -1 | $2K--$5K | Registration with Handelsregister |
| 6. Apply for tax exemption (public-benefit) | Month 0 | $3K--$5K | Application to Steuerverwaltung |
| 7. Notify Foundation Supervisory Authority | Month 0 | $0 | Stiftungsaufsichtsbehorde supervision for public-benefit foundations |
| 8. Establish Stiftung bank account | Month 0 | $0--$1K | Liechtenstein or Swiss bank |

**Total Stiftung formation cost:** $25K--$60K
**Total timeline:** 3 months (Month -3 to Month 0)

### Constitutional Provisions (C14 Alignment)

The Stiftung statutes must include:

1. **L0 (Immutable):** Purpose clause prohibiting for-profit conversion, asset distribution to individuals, and profit extraction. Can only be amended by unanimous Foundation Council + Purpose Trust Protector approval (effectively immutable).
2. **L1 (Structural):** Dual-entity governance (Stiftung + PBC), Foundation Council composition rules, Purpose Trust integration.
3. **L2 (Policy):** Spending caps (5% annual, 20% emergency reserve per C14), AIC treasury management rules.
4. **L3 (Operational):** Delegated to PBC within L0--L2 constraints.

## 8.2 PBC Incorporation (Delaware)

### Steps and Timeline

| Step | Timeline | Cost | Notes |
|------|----------|------|-------|
| 1. Engage Delaware counsel | Month -2 | $3K retainer | Corporate law firm with PBC experience |
| 2. Draft Certificate of Incorporation | Month -2 | $5K--$10K | Must identify specific public benefit per DGCL 362(a) |
| 3. File with DE Secretary of State | Month -1 | $300 filing fee | Standard incorporation |
| 4. Draft bylaws | Month -1 | $3K--$5K | Board composition, officer roles, Stiftung approval requirements |
| 5. Issue shares to Stiftung (via Purpose Trust) | Month -1 | $2K--$3K | 100% ownership by Stiftung through Purpose Trust |
| 6. Obtain EIN | Month -1 | $0 | IRS Form SS-4 |
| 7. Open PBC bank account | Month 0 | $0 | US bank, operational account |
| 8. State registrations (as needed) | Month 0--1 | $1K--$3K | Register in states where employees reside |

**Total PBC incorporation cost:** $15K--$25K
**Total timeline:** 2 months (Month -2 to Month 0)

**Public benefit statement:** "The development and maintenance of open, verifiable artificial intelligence infrastructure for the long-term benefit of humanity, including coordination, verification, settlement, and governance systems that ensure AI systems operate transparently, accountably, and in alignment with human values."

## 8.3 Employment Law (DA-08)

### PBC as Sole Employer

All employees are hired by the Delaware PBC. The Stiftung does not directly employ anyone. This avoids:
- Liechtenstein labor law complications
- Dual-employment jurisdictional conflicts
- Social security treaty issues

### Employment Law Compliance

| Requirement | Approach | Cost |
|-------------|----------|------|
| Employment agreements | Standard at-will agreements with IP assignment, non-disclosure, arbitration | $3K--$5K (template from counsel) |
| IRC 409A compliance (PVR) | Engage employment tax counsel to review PVR plan | $15K--$20K (DA-08) |
| AIC allocation agreements | Separate agreement from employment; specifies AIC terms, zero-value disclaimer, tax treatment | $5K--$8K (template from counsel) |
| Multi-state employment compliance | Register in each state where remote employees reside; payroll withholding per state | $1K--$3K per state |
| Benefits administration | Use PEO (Professional Employer Organization) for <20 employees: Justworks, Rippling, or TriNet | $100--$200/employee/month |
| Workers' compensation insurance | Required in all states; obtained through PEO | Included in PEO fees |

### IP Assignment

All employees sign an IP assignment agreement at hire:
- All work product created during employment is assigned to the PBC
- The PBC licenses all IP to the Stiftung under a perpetual, irrevocable license
- The Stiftung holds ultimate IP ownership (per C14 governance structure)
- Open-source code is published under the Stiftung's chosen license (to be determined; likely Apache 2.0 or similar permissive license)

## 8.4 Token Regulatory Strategy (DA-11)

### AIC Classification Approach

**Target classification:** Utility token (MiCAR Category: neither asset-referenced nor e-money)

**Regulatory engagement timeline:**

| Step | Timeline | Cost | Entity |
|------|----------|------|--------|
| 1. Engage Liechtenstein FMA counsel | Month 1 | $10K retainer | Stiftung |
| 2. Prepare AIC classification memorandum | Month 1--2 | $15K--$20K | Stiftung counsel |
| 3. Informal FMA consultation | Month 2--3 | $5K--$8K | Stiftung counsel |
| 4. Engage US securities counsel | Month 3 | $8K retainer | PBC |
| 5. Prepare US classification memorandum (Howey analysis) | Month 3--4 | $10K--$15K | PBC counsel |
| 6. File MiCAR notification (if required) | Month 12+ (when CRF approaches operation) | $10K--$20K | Stiftung |

**Total regulatory counsel cost:** $50K--$75K (phased over Month 1--12)

### Fallback if AIC Classified as Security

If SEC or FMA signals security classification:
1. Employee AIC allocations are converted to additional PVR units (cash-based, no token)
2. CRF operations are deferred to Phase 3+ pending regulatory resolution
3. The marketplace operates in fiat only during Phase 1--2
4. AIC remains an internal accounting unit (not distributed externally) until classification is resolved
5. Engage regulatory counsel to explore Regulation D (US) or MiCAR-compliant issuance pathways

## 8.5 Cayman Purpose Trust (Phase 2+)

Per C14, the Cayman Purpose Trust holds PBC shares and provides an independent Protector with authority to block L0 violations. Formation is Phase 2 (Month 18+) and is not required for Phase 0--1 operations.

**Estimated formation cost:** $30K--$50K
**Annual maintenance:** $15K--$25K (trustee fees, compliance)

---

<a id="section-9"></a>
# SECTION 9 --- RISK MITIGATION

## 9.1 Pre-Mortem Analysis: Six Failure Scenarios

### Failure Scenario 1: "The Money Never Comes" (Grant Drought)

**Scenario:** All 6 Year 1 grant applications are rejected. No philanthropic funding materializes. Founding capital ($1M) is exhausted by Month 10.

**Probability:** 15--20%

**Consequences:** Team reduced to 3--4 engineers by Month 8. W1 delayed or simplified. Loss of ZKP and ML specialists who find other opportunities.

**Mitigation plan:**
1. **Month 6 (trigger):** If zero grants awarded and no firm commitments, activate consulting bridge. Target $30K--$50K/month in distributed systems consulting.
2. **Month 8:** Reduce team to 4 core engineers (CTO + 3 senior). Place remaining engineers on unpaid leave with guaranteed rehire within 6 months.
3. **Month 9--12:** Publish W0 results aggressively. Submit to 3--4 additional grant programs. Approach venture philanthropy (Omidyar, Skoll) with W0 evidence.
4. **Month 12:** If no funding secured, transition to "hibernation mode": 2 engineers maintain specifications and codebase part-time while founder pursues full-time fundraising.

### Failure Scenario 2: "W0 Kills the Project" (Kill Criteria Triggered)

**Scenario:** One or more W0 experiments produces results that trigger C22 kill criteria. The architectural hypotheses are invalidated.

**Probability:** 10--15% (per C22 feasibility assessment)

**Consequences:** The fundraising pivot cannot happen because W0 results are negative. All downstream funding depends on positive W0 results.

**Mitigation plan:**
1. Publish negative results transparently (academic integrity and Stiftung credibility).
2. Analyze which specific hypotheses failed and whether the architecture can be revised.
3. If partial failure (1--2 experiments fail, 2--3 succeed): revise architecture, reduce scope, submit modified grant applications based on surviving hypotheses.
4. If total failure (3+ experiments fail): orderly wind-down. Return unused founding capital to contributors (pro rata). Publish all specifications as open-source contribution to the field.

### Failure Scenario 3: "Can't Hire the Team" (Talent Market Failure)

**Scenario:** After 3 months of recruiting, only 2--3 of 6 target W0 hires accept offers. ZKP and senior architecture roles remain unfilled.

**Probability:** 20--25%

**Consequences:** W0 experiments are delayed or reduced in scope. The team operates below critical mass.

**Mitigation plan:**
1. Activate DA-06 ZKP contingency (academic partnership or consulting).
2. Offer above-range compensation for unfilled critical roles (increase base by $20K--$30K, increase signing bonus to $50K).
3. Engage recruiting firm specializing in distributed systems / crypto talent ($30K--$50K retainer, success fee 15--20% of first-year salary).
4. Expand geographic search: EU-based engineers (hired through Stiftung or PBC + EOR) may accept lower base due to different cost-of-living dynamics.
5. Accept slower W0 timeline (4--5 months instead of 3) with reduced team.

### Failure Scenario 4: "Founder Burnout / Incapacity"

**Scenario:** Joshua Dunn experiences burnout, health crisis, or personal emergency that prevents active leadership for 3+ months.

**Probability:** 10--15% (over 36 months)

**Consequences:** Without the founder, institutional relationships, grant writing, and strategic direction stall. Technical work may continue under CTO but fundraising and external relations stop.

**Mitigation plan:**
1. **DA-09:** CTO is hired as first or second employee and undergoes 6-month co-leadership ramp. By Month 6, CTO can serve as operational successor.
2. **DA-10:** Key-person insurance ($4M policy) provides financial bridge during founder absence.
3. **Institutional knowledge base:** All funder contacts, grant strategies, partnership agreements, and strategic decisions documented in shared system (Notion, Confluence, or similar).
4. **Stiftung board authority:** Foundation Council can appoint acting director and continue operations.
5. **Sabbatical policy:** Founder takes 1 week off per quarter (mandatory). Board monitors for burnout indicators.

### Failure Scenario 5: "Regulatory Shutdown" (AIC Classified as Security)

**Scenario:** The SEC issues an enforcement action classifying AIC distributions as unregistered securities. The FMA requires full MiCAR authorization before any AIC activity.

**Probability:** 5--10%

**Consequences:** All AIC allocations to employees are void. CRF cannot operate. The economic model (C15) is disrupted.

**Mitigation plan:**
1. AIC allocations are converted to additional PVR units (cash-based, no regulatory risk).
2. The marketplace operates in fiat only during regulatory resolution.
3. Engage securities counsel for Regulation D exemption (US) or MiCAR-compliant issuance (EU).
4. If resolution takes 12+ months: the project continues without AIC distribution. The economic model adapts to fiat-denominated settlement. AIC becomes an internal accounting unit only.
5. Long-term: if utility-token classification is ultimately denied, explore alternative token structures (e.g., governance-only token, non-transferable credit) that may satisfy regulators.

### Failure Scenario 6: "Competitor Captures the Market" (First-Mover Disadvantage)

**Scenario:** A well-funded organization (Google, Anthropic, or a new entrant) launches a competing AI verification infrastructure before Atrahasis reaches W3. Their resources (100x+ Atrahasis budget) allow faster development and instant credibility.

**Probability:** 15--20%

**Consequences:** Atrahasis's differentiator (first public-benefit AI verification infrastructure) is undermined. Grant-makers and partners may prefer the established competitor.

**Mitigation plan:**
1. **Structural differentiation:** A for-profit competitor's verification infrastructure has a conflict of interest (they verify their own AI). Atrahasis's independent Stiftung structure is the permanent differentiator.
2. **Open-source advantage:** Publish code early. If a competitor builds proprietary infrastructure, Atrahasis becomes the open-source alternative (Red Hat vs. Windows dynamic).
3. **Interoperability:** Design the verification layer (C5 PCVM) to be compatible with multiple verification standards. Even if a competitor exists, Atrahasis can verify THEIR outputs.
4. **Niche first:** Focus on markets where independence is mandatory (government, healthcare, financial regulation) rather than competing head-to-head on enterprise adoption.

## 9.2 Key Person Risk Mitigation (DA-09, DA-10)

### CTO Hire (DA-09)

**Requirement:** The CTO must be hired as the first or second employee (Month 1--2).

**CTO Profile:**
- 10+ years in distributed systems, cryptographic protocols, or formal verification
- Experience leading teams of 5--15 engineers
- Published research or significant open-source contributions
- Alignment with Atrahasis mission (not just a job)
- Capable of serving as operational successor to Joshua Dunn

**Co-Leadership Ramp (6 months):**

| Month | CTO Responsibility | Founder Responsibility |
|-------|-------------------|----------------------|
| 1--2 | Technical deep-dive into C3--C13 specs. W0 experiment design lead. | Strategy, fundraising, hiring, grant writing |
| 3--4 | W0 execution lead. Begin representing Atrahasis in technical forums. | Grant follow-up, partner negotiations, board formation |
| 5--6 | Full technical leadership. Participate in funder meetings. | Strategic direction, external relations, board governance |
| 7+ | Operational successor. Can run the project independently for 3+ months. | Shared leadership. Founder can reduce to 50--75% involvement if needed. |

### Key-Person Insurance (DA-10)

| Parameter | Specification |
|-----------|--------------|
| Insured | Joshua Dunn |
| Policy type | Key-person life and disability insurance |
| Coverage | $4M (covers 12--18 months of operations at Phase 1 burn rate) |
| Annual premium (estimated) | $5K--$8K (varies by age, health) |
| Beneficiary | Atrahasis Stiftung (via PBC) |
| Policy start | Month 0 (before W0 launch) |
| Coverage period | Continuous, renewed annually |

## 9.3 Insurance and Legal Reserves

| Insurance / Reserve | Coverage | Annual Cost | Purpose |
|--------------------|----------|-------------|---------|
| Key-person insurance | $4M | $5K--$8K | Founder incapacity |
| Directors & Officers (D&O) insurance | $2M | $3K--$5K | Board liability |
| General liability | $1M | $1K--$2K | Standard business coverage |
| Cyber liability | $1M | $2K--$4K | Data breach, system compromise |
| Legal reserve fund | $50K (maintained) | N/A (replenished from operations) | Unexpected legal matters |
| **Total annual insurance cost** | | **$11K--$19K** | |

## 9.4 Scenario Planning Summary

| Dimension | Pessimistic (25th pct) | Expected (50th pct) | Optimistic (75th pct) |
|-----------|----------------------|--------------------|-----------------------|
| Total funding (36 mo) | $6.5M | $10.5M | $13.5M |
| Peak team size | 10 | 17 | 19 |
| W5 completion | Month 42+ (delayed) | Month 33 | Month 27 |
| Self-sustaining revenue | Month 48+ | Month 40 | Month 34 |
| CRF funded at | $0--$200K | $500K | $1.5M |
| ACI at Month 36 | 0.0001 (minimal) | 0.001 (early) | 0.005 (promising) |
| Probability of project survival at Month 36 | 55% | 80% | 95% |

---

<a id="section-10"></a>
# SECTION 10 --- SIMPLIFICATION AGENT REVIEW

## 10.1 What Can Be Removed Without Material Impact?

### Removable Without Impact

| Element | Rationale for Removal | Savings |
|---------|----------------------|---------|
| Cayman Purpose Trust (Phase 0--1) | Not needed until Phase 2 (Month 18+). Stiftung governance is sufficient for Phase 0--1. | $30K--$50K formation cost deferred |
| Institutional membership program (Year 1) | No members will join before the system exists. Design the program but defer launch to Month 18+. | $0 cost savings but removes a distraction |
| Data licensing revenue stream | Highly speculative, available only at W5+. Remove from Year 1--2 projections. | $0 (was already minimal in projections) |
| Enterprise API licensing (Year 1) | No API to license until W3+. Defer to Phase 2. | $0 |
| AIC dashboard (elaborate version) | Replace with a simple monthly spreadsheet email for Phase 0. Build dashboard in Phase 1 when there are 8+ employees. | $5K--$10K development cost deferred |

### NOT Removable (Essential)

| Element | Why It Cannot Be Removed |
|---------|-------------------------|
| Founding capital ($950K+) | Irreducible. Without it, nothing starts. |
| CTO hire (Month 1--2) | DA-09 is CRITICAL. Founder dependency must be mitigated immediately. |
| Grant applications (4+ in Year 1) | The project cannot survive on founding capital alone. Grants are the bridge to Phase 2. |
| Employment tax counsel ($20K) | PVR without 409A compliance creates personal tax liability for employees. Non-negotiable. |
| Regulatory counsel ($50K) | AIC distribution without legal opinion creates existential regulatory risk. |
| Key-person insurance ($7K/year) | Board fiduciary duty requires this. Cost is trivial relative to risk. |

## 10.2 Minimum Viable Funding Strategy

If all simplifications are applied and the budget must be minimized:

**Minimum Viable Configuration:**

| Parameter | Minimum Viable | Full Design |
|-----------|---------------|-------------|
| Founding capital | $750K (no $200K reserve) | $950K--$1.2M |
| W0 team | 3 engineers (defer ZKP to W1) | 4--6 engineers |
| W0 duration | 4 months | 3 months |
| W0 experiments | 3 (drop Experiment 2: ZKP verification) | 4 |
| Grant applications | 3 (Open Philanthropy, Horizon Europe, 1 other) | 6--9 |
| CTO hire | Month 3 (after W0, not during) | Month 1--2 |
| Legal spending | $35K (409A + minimal regulatory) | $70K--$100K |
| 36-month total budget | $7M--$9M | $10M--$12M |
| Peak team | 12--14 | 17--19 |
| W5 completion | Month 36--42 | Month 27--33 |

**Impact of minimum viable:** Slower, smaller, but still achievable. The core architecture is implemented. ZKP verification is delayed by one wave. The team peaks at 12--14 instead of 19. W5 production launch is pushed to Month 36--42.

**When to use minimum viable:** If founding capital is $750K or less, or if zero grants are awarded by Month 12.

---

<a id="section-11"></a>
# SECTION 11 --- MID-DESIGN REVIEW GATE

## 11.1 Arbiter Assessment of Design Completeness

### Design Action Resolution Audit

| DA | Status | Complete? | Notes |
|----|--------|-----------|-------|
| DA-01 | Budget revised to $10.2M--$12.1M | YES | Sec 5.1 |
| DA-02 | All 4 options modeled with cash flow | YES | Sec 2.2--2.5 |
| DA-03 | AIC dashboard specified (6 panels) | YES | Sec 4.4 |
| DA-04 | 9 grants calendared with timelines | YES | Sec 3.1--3.4 |
| DA-05 | 3 academic partner profiles specified | YES | Sec 3.5 |
| DA-06 | 4-tier ZKP contingency designed | YES | Sec 4.6 |
| DA-07 | 0.5 FTE CFO from Month 7, $60K--$80K/yr | YES | Sec 5.4 |
| DA-08 | 409A-exempt PVR structure designed | YES | Sec 4.5 |
| DA-09 | CTO as hire #1--2, 6-month ramp | YES | Sec 9.2 |
| DA-10 | $4M key-person insurance, Month 0 | YES | Sec 9.2 |
| DA-11 | $50K regulatory counsel, phased | YES | Sec 8.4 |
| DA-12 | $200K ring-fenced reserve | YES | Sec 2.5, 5.1 |

**All 12 design actions resolved.**

### Monitoring Flag Coverage

| MF | FEASIBILITY Flag | Design Coverage |
|----|-----------------|-----------------|
| MF-01 | Founding capital commitment | Sec 2 decision framework; minimum $750K confirmed as threshold |
| MF-02 | Grant success rate | Sec 3 portfolio; 15--22% zero-grant probability; Sec 9.1 Scenario 1 contingency |
| MF-03 | ZKP hire | Sec 4.6 four-tier contingency |
| MF-04 | Burn rate variance | Sec 5.5 trigger system (Yellow/Orange/Red/Terminal) |
| MF-05 | Runway threshold | Sec 5.5 trigger system with specific actions at 6/4/2/1 month thresholds |
| MF-06 | AIC regulatory | Sec 8.4 phased regulatory engagement; Sec 9.1 Scenario 5 fallback |
| MF-07 | Founder health | Sec 9.2 CTO co-leadership ramp; Sec 9.1 Scenario 4 mitigation |

**All 7 monitoring flags addressed.**

### Design Gaps Identified

1. **International hiring mechanics.** If engineers are hired outside the US, the PBC needs an Employer of Record (EOR) service. This adds $400--$800/month per international employee. The design assumes US-based hiring but should budget $10K--$20K/year for 1--3 international hires.

2. **Open-source licensing strategy.** The design references Apache 2.0 but has not analyzed IP implications for the verification layer (C5) and defense systems (C11--C13). Some components may require different licensing to prevent adversarial use while maintaining open access.

3. **Board composition.** The Stiftung requires 2+ Foundation Council members including 1 Liechtenstein-licensed trustee. The design does not specify how to identify and recruit the independent trustee. Budget $10K--$20K/year for trustee fees.

**These gaps are non-blocking for DESIGN stage completion. They should be resolved during SPECIFICATION or pre-execution.**

### Arbiter Verdict

The DESIGN document resolves all 12 feasibility design actions and addresses all 7 monitoring flags. The founding capital strategy provides a clear decision framework with recommended path (Option B+D hybrid). The cash flow model is realistic and shows the structural tightness of the budget --- this honesty is a strength, not a weakness. The compensation architecture is the strongest achievable within Stiftung constraints. The risk mitigation section covers the six most likely failure modes with specific, actionable contingency plans.

**Remaining weaknesses:**
- The cash flow model shows runway below 4 months at multiple points in the expected scenario. This is inherently fragile.
- The 15--22% probability of zero grants in Year 1 is a material risk with no complete mitigation (only contingency).
- The ZKP hiring contingency (Tier 2--4) degrades W0 evidence strength, which degrades subsequent grant success probability --- a negative feedback loop.

**Overall assessment:** The design is comprehensive, internally consistent, and honest about its constraints. It is ready for SPECIFICATION stage advancement.

---

<a id="section-12"></a>
# SECTION 12 --- FORMAL REQUIREMENTS

## 12.1 Funding Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| FR-01 | Founding capital of $950K--$1.2M must be committed before W0 launch | CRITICAL | Bank statement showing transferred funds |
| FR-02 | At least 4 grant applications submitted within 4 months of W0 launch | HIGH | Application confirmation receipts |
| FR-03 | At least 1 grant awarded within 12 months of W0 launch | HIGH | Grant agreement signed |
| FR-04 | Operating reserve of $200K maintained and ring-fenced for payroll only | HIGH | Separate bank account or accounting segregation |
| FR-05 | Runway must not drop below 2 months at any time | CRITICAL | Monthly financial reporting |
| FR-06 | No single funding source may exceed 40% of total 36-month funding | MEDIUM | Annual financial audit |

## 12.2 Compensation Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| CR-01 | Base salary benchmarked at 75th percentile nonprofit tech | HIGH | Annual compensation survey comparison |
| CR-02 | PVR plan reviewed by employment tax counsel for 409A compliance | HIGH | Legal opinion letter |
| CR-03 | AIC allocation agreements include explicit zero-value disclaimer | HIGH | Signed agreement with clause |
| CR-04 | Total employee AIC allocation must not exceed 0.5% of treasury (50M AIC) for first 3 years | MEDIUM | AIC ledger audit |
| CR-05 | Wave milestone bonuses paid within 30 days of wave advancement certification | MEDIUM | Payment records |

## 12.3 Legal/Regulatory Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| LR-01 | Stiftung statutes include immutable prohibition on profit conversion (C14 L0) | CRITICAL | Legal review of filed statutes |
| LR-02 | PBC Certificate of Incorporation identifies specific public benefit | HIGH | Filed certificate |
| LR-03 | AIC classification opinion obtained from FMA counsel before any AIC distribution | HIGH | Legal opinion letter |
| LR-04 | Key-person insurance on founder in force before W0 launch | HIGH | Insurance policy documentation |
| LR-05 | IP assignment agreements signed by all employees at hire | HIGH | Signed agreements on file |
| LR-06 | PBC biennial benefit report filed per DGCL 366 | MEDIUM | Filed report |

## 12.4 Operational Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| OR-01 | CTO or operational successor must be in place by Month 6 | HIGH | Employment agreement signed |
| OR-02 | Monthly financial reporting to Stiftung board | HIGH | Board meeting minutes |
| OR-03 | Quarterly runway projection updated and distributed to board | HIGH | Projection document |
| OR-04 | Contingency triggers (Yellow/Orange/Red/Terminal) evaluated monthly | MEDIUM | Financial controller report |
| OR-05 | W0 results published as open-source code within 30 days of W0 completion | MEDIUM | Public repository |

---

# APPENDIX A --- CONSOLIDATED BUDGET TABLE

| Category | Phase 0 (Mo 1--6) | Phase 1 (Mo 7--18) | Phase 2 (Mo 19--36) | Total |
|----------|-------------------|--------------------|--------------------|-------|
| Personnel (payroll + benefits) | $660K | $2,640K | $5,760K | $9,060K |
| Signing bonuses | $160K | $120K | $70K | $350K |
| Wave milestone bonuses | $100K | $180K | $290K | $570K |
| PVR payouts | $0 | $80K | $320K | $400K |
| Cloud infrastructure | $36K | $134K | $300K | $470K |
| CRF (Conversion Reserve) | $0 | $200K | $800K | $1,000K |
| Legal/regulatory/insurance | $135K | $115K | $170K | $420K |
| CFO (0.5 FTE) | $0 | $80K | $80K | $160K |
| Travel/recruiting | $60K | $80K | $50K | $190K |
| Operating reserve (ring-fenced) | $200K | maintained | maintained | $200K |
| **Subtotal** | **$1,351K** | **$3,629K** | **$7,840K** | **$12,820K** |
| Less: contingency already included | | | | ($720K) |
| **Target (with 10% contingency)** | | | | **$12,100K** |

*Note: This represents the "full ramp" scenario. The baseline scenario ($10.2M) reduces personnel by $2M through slower hiring.*

---

# APPENDIX B --- KEY DATES AND MILESTONES

| Date (relative to W0 launch) | Milestone | Dependency |
|------------------------------|-----------|------------|
| Month -3 | Stiftung formation begins | Joshua's commitment confirmed |
| Month -2 | PBC incorporation begins; Open Philanthropy concept note submitted | Stiftung counsel engaged |
| Month -1 | Legal entities formed; bank accounts opened; first hire offers extended | Formation complete |
| Month 0 | W0 launch; founding capital transferred; key-person insurance in force | Capital committed |
| Month 1--2 | CTO hired; 4--6 engineers onboarded; Horizon Europe Stage 1 submitted | Recruiting pipeline |
| Month 3 | W0 experiments complete; results analyzed | Team execution |
| Month 4 | W0 evidence package prepared; DARPA abstract submitted; Open Phil post-W0 proposal | W0 success |
| Month 6 | W0 published; W1 begins; post-W0 fundraising pivot | W0 results |
| Month 12 | At least 1 grant awarded (target); team at 10--11 | Grant success |
| Month 13--15 | Horizon Europe pre-finance received (if awarded) | Horizon Europe success |
| Month 18 | W2 complete; marketplace closed alpha; CRF initial funding | Technical milestones |
| Month 24 | W4 begins; marketplace open beta; revenue >$50K/month | System functional |
| Month 30 | W5 production launch target; revenue >$150K/month | Full implementation |
| Month 36 | All waves complete (expected scenario); self-sustainability assessment | Cumulative execution |

---

# APPENDIX C --- GLOSSARY OF FINANCIAL TERMS

| Term | Definition |
|------|-----------|
| **AIC** | Atrahasis Internal Currency. The native unit of account for the Atrahasis compute marketplace. 10B total supply. |
| **ACI** | Atrahasis Capability Index. A composite metric measuring the system's verification, coordination, and settlement capabilities. Drives AIC reference price via C15 SWECV formula. |
| **BRA** | Bilateral Resource Agreement. The contract between a compute provider and the Atrahasis marketplace (C15 DA-02). |
| **CRF** | Conversion Reserve Fund. A fiat reserve (target $500K--$2M) that enables AIC-to-fiat conversion at the reference rate (C15 DA-01). |
| **PVR** | Phantom Value Rights. A contractual right to a cash bonus calculated from PVR units x wave multiplier x revenue factor. 409A-exempt as short-term deferral. |
| **SWECV** | Systemic Weighted Expected Creation Value. The C15 formula for calculating AIC reference price as a function of ACI. |
| **Wave (W0--W5)** | Implementation phases defined in C22. Each wave has pre-registered success criteria and kill criteria. |
| **Runway** | Months of remaining cash at current burn rate. Calculated as: Cash on Hand / Monthly Burn Rate. |
| **Fully-loaded cost** | Total employer cost per employee including salary, benefits, payroll taxes, equipment, cloud allocation, and stipends. Estimated at $276K/year average. |

---

*End of C18 Design Document. Submitted for SPECIFICATION stage advancement.*
