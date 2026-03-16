# C18-MTS --- Staged Portfolio Funding with W0 Pivot

## Master Tech Spec

**Document ID:** C18-MTS-v1.0.1
**Invention ID:** C18
**Title:** Staged Portfolio Funding with W0 Pivot
**Status:** SPECIFICATION
**Date:** 2026-03-15
**Author:** Atrahasis Agent System (Specification Writer)
**Prior Stages:** IDEATION (C18-A+ selected), RESEARCH (landscape validated), FEASIBILITY (CONDITIONAL_ADVANCE, 12 DAs), DESIGN (all 12 DAs resolved)
**Budget Target:** $11.3M--$15.7M over 30--36 months
**Team:** 6 engineers (W0) scaling to 19 (W5)
**Legal Structure:** Liechtenstein Stiftung + Delaware PBC + Cayman Purpose Trust (Phase 2+)

### Version History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | 2026-03-11 | Initial Master Tech Spec |
| v1.0.1 | 2026-03-15 | T-304 cost-model rewrite for Alternative C sovereign compute, leased cognition, and Forge adaptation economics |

---

# 1. Executive Summary

This document specifies the funding strategy, business operations, compensation architecture, and revenue model for the Atrahasis implementation — a $11.3M--$15.7M program to build a mission-locked sovereign intelligence institution through a nonprofit Liechtenstein Stiftung and its operational Delaware PBC subsidiary.

**The Posture: Closed Capability, Open Accountability**
In accordance with the Mission-Locked Sovereignty Doctrine, Atrahasis will NOT publish its core models, recursive algorithms, or un-sanitized internal traces as open source. We publish rigorous safety audits, ZKP compliance proofs, and verifiable governance signals. The highest-capability intelligence remains strictly internal.

**Key numbers:**

- **Total budget:** $11.3M (baseline) to $15.7M (full ramp)
- **Founding capital required:** $950K-$1.25M (irreducible constraint)
- **Team:** 4–6 engineers at W0, scaling to 17–19 by W5
- **Funding stages:** Stage 0 ($950K-$1.25M, founding capital), Stage 1 ($2.5M-$4.5M, grants + sovereign-compute partnerships), Stage 2 ($6M-$9.5M, Foundry Licensing + Enterprise Bounded Services + strategic stewardship renewals)
- **Revenue model:** Atrahasis does not run an open public task marketplace. Revenue is generated via:
  1. **Foundry Patent Licensing:** Major corporations petition the Foundry for R&D breakthroughs. Atrahasis solves them internally, patents them, and ethically licenses them for significant fiat payouts.
  2. **Enterprise Bounded Services:** Selling safe, non-recursive, bounded capabilities to B2B clients.

The revised cost model assumes the Alternative C operating posture: native `AACP/AASL` implementation, `C45`-governed leased cognition where temporarily unavoidable, and a financed `C47` Cross-Compilation Forge lane for native model adaptation and quarantine rather than low-cost adapter-era cloud assumptions.

The strategy's central innovation is the **W0 Pivot**: raise minimum founding capital to run three months of pre-registered validation experiments (C22 Wave 0), then use quantitative results as the primary evidence for all subsequent fundraising. This transforms a speculative whitepaper pitch into an evidence-based infrastructure proposal.

---

# 2. Motivation

## 2.1 The Funding Problem

Atrahasis is a nonprofit building AGI infrastructure. This creates a structural funding paradox: the organizations with the most capital to invest in AI (venture capital firms, tech conglomerates) expect equity returns that a Stiftung cannot provide. The organizations most aligned with Atrahasis's mission (foundations, governments, philanthropies) operate at funding scales 100--1000x smaller than for-profit AI investment.

To illustrate: Anthropic raised $30B as a for-profit PBC. Atrahasis needs roughly $11M--$16M as a nonprofit Stiftung. The 3000x difference reflects the for-profit premium --- not a 3000x difference in ambition or technical scope.

## 2.2 The OpenAI Lesson

OpenAI's 2015--2025 trajectory --- from 501(c)(3) nonprofit to $500B for-profit PBC --- is the canonical failure mode. The nonprofit had no constitutional prohibition on for-profit conversion. When infrastructure costs reached $115B and investors demanded returns, the board voted to restructure. The foundation retained 26% equity in the entity it created, but the mission had been rewritten six times.

Atrahasis's C14 immutable layer (constitutional prohibition on profit conversion, asset distribution, and profit extraction, enforced by a Cayman Purpose Trust Protector) is the structural firewall OpenAI lacked. But this firewall makes fundraising harder. C18 is the strategy for funding an immovable nonprofit in a for-profit funding landscape.

## 2.3 Why a Formal Strategy Is Required

Without a formal funding strategy, the project faces:

1. **Cash flow death.** Engineering payroll at $95K--$380K/month cannot tolerate even a single month of funding disruption.
2. **Talent loss.** Elite distributed systems and ZKP engineers command $200K--$300K+ in the for-profit market. Without a coherent compensation architecture, hires will not accept or will not stay.
3. **Grant timing mismatch.** Government grants take 6--18 months from application to disbursement. Without cash flow planning, the project runs out of money waiting for awarded funds.
4. **Credibility gap.** Funders evaluating a speculative AI infrastructure project need to see financial discipline alongside technical ambition.

---

# 3. Legal Entity Architecture

## 3.1 Three-Entity Structure

The Atrahasis legal structure comprises three entities with distinct roles, established per C14 (AiBC governance specification):

```
+---------------------------+
|  Liechtenstein Stiftung   |  IP ownership, mission custody, AIC treasury,
|  (nonprofit foundation)   |  constitutional governance (L0--L2)
+---------------------------+
            |
            | funds via grants/service agreements
            | owns 100% equity (via Purpose Trust)
            v
+---------------------------+
|  Delaware PBC             |  Employs all staff, generates revenue,
|  (public benefit corp)    |  runs Foundry/enterprise ops, pays salaries
+---------------------------+
            ^
            | holds PBC shares, independent Protector
            |
+---------------------------+
|  Cayman Purpose Trust     |  Blocks L0 violations, independent oversight
|  (Phase 2+, Month 18+)   |  Cannot be influenced by founder or board
+---------------------------+
```

## 3.2 Stiftung (Liechtenstein)

**Governing law:** Art. 522 et seq., Persons and Companies Act (PGR)
**Minimum capital:** CHF 30,000 ($33K)
**Supervision:** Stiftungsaufsichtsbehorde (Foundation Supervisory Authority)
**Tax:** 12.5% flat rate; tax exemption available for public-benefit foundations

**Responsibilities:**
- Holds all intellectual property (licensed to PBC under perpetual irrevocable license)
- Manages the 10B AIC treasury per C14 spending constraints (5% annual cap, 20% emergency reserve)
- Receives all PBC profits (no individual distribution)
- Maintains constitutional governance (L0 immutable, L1 structural, L2 policy layers)
- Issues AIC allocations to employees as Stiftung treasury distributions (not equity)

**Formation steps and costs:**

| Step | Timeline | Cost |
|------|----------|------|
| Engage Liechtenstein counsel | Month -3 | $5K retainer |
| Draft Stiftung statutes (Stiftungsurkunde) | Month -3 to -2 | $15K--$25K |
| Appoint Foundation Council (min 2 members, 1 Liechtenstein trustee) | Month -2 | $10K--$20K/year ongoing |
| Deposit minimum capital | Month -1 | CHF 30,000 ($33K) |
| File with Commercial Register (Handelsregister) | Month -1 | $2K--$5K |
| Apply for tax exemption | Month 0 | $3K--$5K |
| **Total** | **3 months** | **$25K--$60K** |

**Constitutional provisions (C14 alignment):**
- L0 (Immutable): Prohibits for-profit conversion, asset distribution to individuals, and profit extraction. Amendment requires unanimous Foundation Council + Purpose Trust Protector approval.
- L1 (Structural): Dual-entity governance, Foundation Council composition, Purpose Trust integration.
- L2 (Policy): 5% annual spending cap, 20% emergency reserve, AIC treasury management.
- L3 (Operational): Delegated to PBC within L0--L2 constraints.

## 3.3 Delaware PBC

**Governing law:** DGCL Subchapter XV (8 Del. C. 361--368)
**Public benefit statement:** "The stewardship of mission-locked sovereign intelligence and the responsible externalization of bounded, accountable derivative capabilities for the long-term benefit of humanity."

**Responsibilities:**
- Employs all operational staff under US labor law
- Operates the Foundry licensing desk, enterprise bounded-services surface, and release-law controlled commercial interfaces
- Generates and collects all revenue (licensing fees, enterprise contracts, strategic partnerships, and other constitutionally permitted service income)
- Pays competitive salaries, signing bonuses, milestone bonuses, and PVR payouts
- Files biennial benefit reports per DGCL 366
- Reports to Stiftung board; operates within constitutional framework

**Formation:** $15K--$25K over 2 months (Month -2 to Month 0). 100% shares issued to Stiftung (via Purpose Trust at Phase 2).

**Fiduciary alignment:** PBC directors must balance stockholder interests with public benefit. Since the sole stockholder (Stiftung) exists to advance the public benefit, these duties are perfectly aligned. This is the cleanest possible PBC governance structure.

## 3.4 Cayman Purpose Trust (Phase 2+)

Deferred to Month 18+. Holds PBC shares and provides an independent Protector with authority to block any action that violates L0 constitutional provisions. Estimated formation cost: $30K--$50K. Annual maintenance: $15K--$25K.

## 3.5 IP Ownership and Employment Flow

All employees are hired by the PBC. All work product is assigned to the PBC via IP assignment agreements signed at hire. The PBC licenses all IP to the Stiftung under a perpetual, irrevocable license. The Stiftung holds ultimate IP ownership.

Publication posture follows the Mission-Locked Sovereignty Doctrine:
- recursion-critical models, training recipes, self-improvement loops, and unsanitized internal traces are not open sourced by default,
- patentable or commercially licensable derivative inventions route through the Foundry,
- public disclosure is limited to accountability artifacts, safety reports, research summaries, and selectively approved non-sensitive releases.

This structure avoids Liechtenstein labor law complications, dual-employment jurisdictional conflicts, and social security treaty issues.

---

# 4. Funding Architecture

## 4.1 Three-Stage Model

The funding architecture sequences capital from lowest-risk to highest-risk sources, using each stage's deliverables to unlock the next stage's funding.

### Stage 0: Founding Capital (Month 0--3, $950K--$1.25M)

**Sources:** Founder personal investment + co-founder capital + parallel pre-seed grant application.

**Purpose:** Fund W0 validation experiments (3 pre-registered experiments testing core architectural hypotheses per C22), entity formation, and the initial operating reserve. Submit 3--5 grant applications concurrently.

**Team:** 4--6 engineers for 3 months.

**Deliverables:** Quantitative experiment results, an accountability-safe technical evidence bundle, academic paper(s) or technical memoranda as approved under release law, and 3--5 submitted grant applications.

**Recommended strategy (B+D Hybrid):**
1. Joshua Dunn contributes $500K (Month 0)
2. One co-founding partner contributes $450K--$750K (Month 0--1)
3. Parallel pre-seed grant application to Open Philanthropy (submitted Month -2, decision Month 2--4)
4. $200K ring-fenced operating reserve within the total

**Decision framework:**
- IF co-founder identified within 8 weeks: Execute B+D ($950K--$1.25M founding capital)
- ELSE IF founder can commit $950K+: Execute A+D (higher concentration risk, faster start)
- ELSE IF founder can commit $500K and patron structure is legal: Execute C+D (lead patron or patron syndicate covering the remaining $450K--$750K)
- ELSE: Project cannot launch. Reduce scope to solo research + grant applications.

**Co-founder value proposition:** Capital contribution AND one of: CTO role (technical co-founder), CFO/COO function (operations co-founder), or established funder relationships (network co-founder). Co-founders receive: AIC allocation (0.03--0.05% of treasury, 4-year vest, 1-year cliff), PVR participation, founding team recognition. No equity --- the Stiftung cannot issue equity.

### Stage 1: Growth Capital (Month 4--13, $2.5M--$4.5M)

**Sources:** Government grants (EU Horizon Europe, DARPA), private foundations (Open Philanthropy, Schmidt Futures), and strategic partnerships (reserved GPU capacity, bare-metal habitat sponsorship, audited evaluation/quarantine funding, and academic co-development).

**Trigger:** W0 advancement criteria met. W0 results constitute the primary evidence package.

**Team:** 8--13 engineers over 10 months.

**Deliverables:** W1--W2 functional layers, partnership agreements, initial Foundry commercialization templates, and funding for continued doctrine-aligned buildout.

### Stage 2: Scaling Capital (Month 14--36, $6M--$9.5M)

**Sources:** Foundry patent licensing ($1.5M--$3.5M), Enterprise bounded services and supervised service contracts ($1M--$2.5M), renewal/expansion grants ($1.5M--$3M), strategic stewardship partnerships ($0.5M--$1.5M), and sovereign-compute reservation / model-adaptation sponsorship ($1.5M--$2.5M).

**Team:** 15--19 engineers over 14--23 months.

**Deliverables:** W3--W5 production system, active Foundry licensing pipeline, bounded enterprise service surface, and a self-sustaining revenue path that does not require public access to the novelty engine.

## 4.2 Why W0 Is the Pivot

Pre-W0, Atrahasis is a whitepaper project with 21,000 lines of specifications. Post-W0, it is a validated architecture with quantitative evidence. This distinction is the difference between speculative and evidence-based fundraising.

The W0 Pivot is modeled on the biotech pipeline: Phase 1 clinical results drive Series B fundraising. In Atrahasis's case, W0 experiment results (tidal scheduling throughput, ZKP verification costs, behavioral fingerprinting accuracy, settlement economics) drive all Stage 1 grant applications and partnership negotiations.

**Pre-W0 applications** (Open Philanthropy, Horizon Europe Stage 1) reference experimental design and specification depth.
**Post-W0 applications** (DARPA, Schmidt Futures, NSF, DOE) include quantitative results and published code.

---

# 5. Grant Strategy

## 5.1 Portfolio Approach

Nine target programs diversified across US government, EU, and private foundations. No single grant represents more than 30% of the total funding plan.

**Portfolio statistics:**
- Total applications: 9
- Total asked: $8M--$24M
- Expected success rate: 12--20% per application
- Expected grants funded (Year 1): 1.3--2.2
- Expected total granted (Year 1): $750K--$3M
- Probability of zero grants (Year 1): 15--22%
- Probability of 2+ grants (Year 1): 45--55%

## 5.2 Grant Calendar

### Tier 1: Submit Pre-W0 or During W0 (Month -2 to Month 3)

**G-01: Open Philanthropy --- AI Safety Infrastructure**
- Ask: $500K--$2M | Success probability: 25--35%
- Submit: Month -2 (concept note) | Decision: Month 1--3 | First disbursement: Month 2--4
- Entity: Stiftung or PBC | Alignment: VERY HIGH
- Narrative: "Pre-registered AI infrastructure experiment with kill criteria. The only AI research project designed from Day 1 as a public-benefit institution with constitutional safeguards against profit conversion."

**G-02: EU Horizon Europe --- AI Security and Robustness (HORIZON-CL4-2026-DIGITAL-EMERGING)**
- Ask: EUR 3--4M (consortium) | Success probability: 12--18%
- Submit: Month 1--2 (Stage 1) | Stage 1 decision: Month 5--7 | Full proposal: Month 7--9 | Final decision: Month 10--13 | First disbursement: Month 12--15 (40% pre-financing)
- Entity: Stiftung (EEA-eligible) | Requires 1--2 academic consortium partners
- Narrative: "Verifiable AI infrastructure: economic incentives for formal verification of AI outputs. Addresses AI Act compliance through novel verification economics."

**G-03: Open Philanthropy --- AI Governance Mechanisms**
- Ask: $250K--$1M | Success probability: 20--30%
- Submit: Month 2 | Decision: Month 4--6 | First disbursement: Month 5--7
- Narrative: "Operational testing of the first AI governance constitution with immutable safeguards. The AiBC structure implements lessons from OpenAI's failed nonprofit governance."

### Tier 2: Submit During W0 With Preliminary Results (Month 3--6)

**G-04: DARPA I2O BAA --- Trustworthy AI Verification**
- Ask: $1M--$3M | Success probability: 10--15%
- Submit: Month 4 (abstract), Month 5 (full proposal) | Decision: Month 8--10 | Disbursement: Month 10--12
- Entity: PBC (US entity required) | W0 Experiments 1--2 strengthen proposal

**G-05: Schmidt Futures --- AI Governance Infrastructure**
- Ask: $500K--$1.5M | Success probability: 15--20%
- Submit: Month 3--4 (via warm introduction) | Decision: Month 6--9

**G-06: Patrick J. McGovern Foundation --- Responsible AI**
- Ask: $250K--$500K | Success probability: 10--15%
- Submit: Month 3 | Decision: Month 6--9

### Tier 3: Submit During W1--W2 With W0 Results (Month 6--12)

**G-07: NSF --- Distributed Systems and Formal Verification** ($500K--$2M, requires university co-PI)
**G-08: DOE Genesis Mission --- AI Infrastructure Challenges** ($5M--$10M)
**G-09: Ethereum Foundation ESP --- Verification Overlap** ($50K--$200K)

## 5.3 Grant Timeline Visualization

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

## 5.4 Academic Partnership Strategy

Three target co-PI profiles to strengthen grant applications:

1. **Distributed Systems / Formal Verification Faculty** (ETH Zurich, MIT CSAIL, CMU, Imperial College). Co-PI on NSF (G-07) and Horizon Europe (G-02). Target: 1 confirmed by Month 3.

2. **Cryptography / ZKP Faculty** (Stanford, UC Berkeley, Technion, University of Waterloo). Co-PI on DARPA (G-04) and Horizon Europe (G-02). Also a source of ZKP engineer hires. Target: 1 confirmed by Month 4.

3. **AI Safety / Governance Faculty** (Oxford, UC Berkeley CHAI, Georgetown CSET, Cambridge Leverhulme). Co-PI on Open Philanthropy applications (G-01, G-03). Target: 1 confirmed by Month 2.

## 5.5 Grant Narrative Templates

**Philanthropic funders (Open Philanthropy, Schmidt Futures, McGovern):** Lead with the OpenAI structural failure and Atrahasis as the antidote. Emphasize immutable constitutional governance, pre-registered kill criteria, and the W0 evidence package. Frame as institution-building, not technology speculation.

**Government funders (DARPA, Horizon Europe, NSF, DOE):** Lead with the technical gap in multi-agent AI verification. Emphasize formal specifications, quantitative benchmarks, and defense/governance relevance. Split the architecture into independently fundable modules --- verification economics (C5), distributed scheduling (C3), anti-forgery (C11), anti-collusion (C12), behavioral fingerprinting (C17).

**Post-W0 evidence integration:** Every application from Month 4 onward includes the W0 evidence package: technical report, academic paper(s) or technical memorandum, sanitized benchmark/code excerpts as approved, 1-page executive summary, and 5-minute video demonstration.

---

# 6. Compensation Architecture

## 6.1 Five-Component Model

Every employee receives a compensation package designed to close the for-profit gap through a combination of guaranteed cash, near-term performance incentives, and long-term speculative upside.

| Component | Function | Timing | Source | Certainty |
|-----------|----------|--------|--------|-----------|
| Base salary | Living cost, market competitiveness | Monthly | PBC payroll | HIGH (guaranteed) |
| Signing bonus | Close the for-profit gap at hire | Start date | PBC operating funds | HIGH (guaranteed) |
| Wave milestone bonus | Near-term performance incentive | Upon C22 wave advancement | PBC operating funds | MEDIUM (contingent on wave success) |
| AIC allocation | Long-term speculative upside | Vests over 3 years, 1-year cliff | Stiftung treasury | LOW (speculative, no current market value) |
| Phantom Value Rights | Bridge between cash and speculative | Within 2.5 months of trigger | PBC operating revenue | MEDIUM (contingent on wave + revenue) |

## 6.2 Base Salary Schedule

Benchmarked at 75th percentile of nonprofit technology organizations (Mozilla: $203K avg, Linux Foundation: $228K avg, Ethereum Foundation: est. $200K--$350K), adjusted upward for role scarcity.

| Role | Base Salary | Signing Bonus | Total Year 1 Cash (incl. est. milestone) |
|------|------------|---------------|------------------------------------------|
| Technical Architect / CTO | $260K--$300K | $35K--$50K | $310K--$375K |
| ZKP Engineer | $220K--$260K | $30K--$40K | $265K--$325K |
| Senior Rust / Distributed Systems | $200K--$240K | $20K--$30K | $235K--$295K |
| ML/LLM Engineer | $190K--$230K | $20K--$30K | $225K--$285K |
| Protocol Engineer | $180K--$210K | $15K--$25K | $210K--$260K |
| Formal Verification (TLA+) | $190K--$230K | $20K--$30K | $225K--$285K |
| Security Engineer | $190K--$230K | $20K--$25K | $225K--$280K |
| DevOps / Infrastructure | $170K--$210K | $15K--$20K | $200K--$255K |

**Benefits (all roles):** Employer-paid health insurance ($15K--$25K/year), 401(k) with 4% match, 25 days PTO + US federal holidays, $3K/year equipment stipend, $2K/year professional development, remote-first with optional co-working stipend ($250/month).

**Blended personnel-loaded cost per engineer:** ~$270K/year average (base $200K + benefits $40K + payroll taxes $20K + equipment $5K + remote stipend $5K). Shared sovereign compute/model operations are budgeted separately in Section 9.1.

## 6.3 Honest Compensation Assessment

Atrahasis Year 1 total cash ($235K--$295K for a senior engineer) is competitive with blockchain startups and reaches 60--85% of FAANG total cash. The gap is the equity component. FAANG offers $100K--$250K in liquid RSUs; Atrahasis offers AIC with zero current market value.

**The gap is closed through:**
- Mission premium (~15% salary discount accepted by mission-aligned candidates)
- AIC speculative upside (potentially orders of magnitude above FAANG equity IF the system succeeds)
- Founding team status and career positioning
- Technical novelty (6-layer AI infrastructure, novel economics --- no comparable role exists elsewhere)

**Target candidate profile:** Engineers who have left or would leave a FAANG/AI lab role because of concerns about profit-driven AI development, who value technical ownership (founding team, not team #47), and who accept the asymmetric bet of speculative AIC upside.

---

# 7. AIC Allocation Program

## 7.1 Treasury Allocation

The total employee allocation pool is **0.5% of the 10B AIC treasury (50M AIC)**, reserved for the first 3 years of hires.

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

**Total allocated (19-person team):** ~35M--45M AIC (0.35--0.45% of treasury)
**Remaining pool for future hires:** 5M--15M AIC (0.05--0.15%)

## 7.2 Vesting and Valuation

AIC vests monthly after the 1-year cliff. Unvested AIC returns to the treasury upon departure. Vested AIC is non-transferable and non-convertible until the CRF (C15 DA-01) is operational (estimated Phase 2, Month 18+).

**Notional value scenarios (illustrative, not guaranteed):**

| ACI Level | Reference Price (C15 SWECV) | 2M AIC Value (ZKP Eng) | 5M AIC Value (CTO) |
|-----------|----------------------------|------------------------|---------------------|
| 0.001 (early system) | ~$10 | $20M notional / 99% discount = $200K | $50M / 99% = $500K |
| 0.01 (functional system) | ~$100 | $200M notional / 95% discount = $10M | $500M / 95% = $25M |
| 0.10 (scaled system) | ~$1,000 | $2B notional / 90% discount = $200M | $5B / 90% = $500M |

Discounts reflect illiquidity, conversion restrictions, and probability weighting. Actual realized value will vary dramatically from these projections.

## 7.3 Tax Treatment

1. AIC allocation is NOT a taxable event at grant (zero fair market value). Tax liability arises only upon CRF conversion.
2. 83(b) election is NOT applicable --- AIC is not equity in a US corporation. The allocation agreement specifies AIC is a contractual right to a digital asset, not a property transfer.
3. Allocation agreement includes explicit zero-value disclaimer: "AIC has no current market value and may never have market value."

## 7.4 AIC Dashboard

An internal dashboard (simple spreadsheet in Phase 0, lightweight web app from Phase 1) visible to all AIC holders, with six panels: My Allocation (vested/unvested/progress), ACI Progress (current value and history), Notional Value (scenarios with disclaimers), CRF Status (funding level and availability), Wave Progress (current wave, criteria status, next bonus trigger), and PVR Status (units, triggers, projected payout).

---

# 8. Phantom Value Rights (PVR)

## 8.1 Legal Structure

PVR is structured as a **short-term deferral bonus plan** exempt from IRC 409A under Treas. Reg. 1.409A-1(b)(4):

- PVR bonuses are paid within 2.5 months of the end of the fiscal year in which the vesting condition is met
- Vesting conditions are objective milestones: C22 wave advancement criteria (observable events)
- This qualifies as a "short-term deferral" and avoids 409A compliance complexity

## 8.2 PVR Formula

```
PVR_payout = PVR_units x Wave_multiplier x PBC_revenue_factor

Where:
  PVR_units          = Granted at hire (see table below)
  Wave_multiplier    = $1,000 per wave advancement (W0->W1 = $1K, W1->W2 = $1K, etc.)
  PBC_revenue_factor = MIN(1.0, PBC_quarterly_revenue / $100K)
```

**Phase 0 override:** When PBC revenue is $0, PVR payouts are funded from the operating budget at 50% of formula value, provided runway exceeds 6 months.

## 8.3 PVR Unit Allocation

| Role | PVR Units | Max Payout Per Wave (full factor) | Max Total (6 waves) |
|------|-----------|-----------------------------------|---------------------|
| CTO / Technical Architect | 25 | $25,000 | $150,000 |
| ZKP Engineer | 20 | $20,000 | $120,000 |
| Senior Engineer | 15 | $15,000 | $90,000 |
| Engineer | 10 | $10,000 | $60,000 |
| Part-time CFO | 8 | $8,000 | $48,000 |

## 8.4 PVR vs. Traditional Equity-Like Instruments

| Dimension | Stock Appreciation Rights (SAR) | Phantom Equity | Atrahasis PVR |
|-----------|-------------------------------|----------------|---------------|
| Trigger | Stock price appreciation | Company valuation event | Wave milestone + PBC revenue |
| Valuation basis | Market price | Board-determined FMV | Formula-based (objective) |
| 409A exposure | HIGH (nonqualified deferred comp) | HIGH | LOW (short-term deferral exempt) |
| Dilution risk | Yes (if settled in shares) | No | No |
| Tied to | Company equity value | Company equity value | Technical progress + revenue |
| Liquidity event needed | Yes | Yes | No (paid from operating funds) |

PVR is designed to reward technical progress independent of equity valuation events. This is critical in a nonprofit context where there is no equity and no liquidity event.

## 8.5 PVR Legal Requirements

1. Written PVR plan document reviewed by employment tax counsel ($20K budget)
2. PVR granted at hire with written allocation notice
3. Payout calculated and paid within 2.5 months of fiscal year-end in which wave advancement occurs
4. Treated as ordinary income to employee and deductible expense to PBC
5. Forfeited upon voluntary termination (retention mechanism)
6. Plan is discretionary --- PBC board (controlled by Stiftung) can amend or terminate with 90 days notice

---

# 9. Cash Flow Model

## 9.1 Budget Summary

**Revised total: $11.3M (baseline) to $15.7M (full ramp)**

| Category | Baseline ($11.3M) | Full Ramp ($15.7M) |
|----------|-------------------|-------------------|
| Personnel (payroll + benefits) | $6.8M | $8.5M |
| Signing bonuses | $180K | $350K |
| Wave milestone bonuses | $360K | $570K |
| PVR payouts | $200K | $400K |
| Sovereign compute + model operations | $1.55M | $2.45M |
| CRF (Conversion Reserve) | $500K | $1M |
| Legal/regulatory/insurance | $280K | $420K |
| Grant management (0.5 FTE CFO, Month 7+) | $120K | $160K |
| Travel/conferences/recruiting | $120K | $190K |
| Operating reserve (ring-fenced) | $200K | $200K |
| Contingency (10%) | $1.03M | $1.42M |
| **TOTAL** | **$11.3M** | **$15.7M** |

Personnel remains the primary cost center, but sovereign compute and model operations now rise to roughly 14--16% of total spend because Alternative C replaces cheap bridge-era assumptions with financed leased-cognition control planes, native message/runtime infrastructure, and `C47` adaptation/quarantine throughput.

### 9.1.1 Sovereign Compute Cost Posture

The old cost model treated infrastructure largely as ordinary cloud spend. The Alternative C posture adds three explicit cost buckets that must be financed up front:

1. **Sovereign runtime and protocol infrastructure.**
   Native `AACP/AASL` services, registries, manifests, conformance fixtures, and operator-visible provenance capture.
2. **Leased-cognition control planes.**
   `C45` outer-membrane leased routes for `PUBLIC`, `ENTERPRISE`, and `FOUNDRY` surfaces while native model coverage is still incomplete.
3. **Forge adaptation and quarantine throughput.**
   `C47` model adaptation, benchmark quarantine, shadow evaluation, and promotion gating needed to reduce leased-provider dependence over time.

These costs are not optional "scale later" spend. They are part of the minimum viable sovereign path and therefore belong in baseline planning rather than contingency fiction.
### 9.1.2 Budget Scope Statement

**C18 provides the fully-loaded budget** covering all costs required to operate the Atrahasis project from entity formation through financial sustainability. C22's $6.9M--$10.0M (pre-contingency) / $7.6M--$11.0M (with contingency) represents the engineering subset of C18's fully-loaded budget, covering personnel, sovereign compute/model operations, tooling, and recruiting only.

Under the T-304 rewrite, C22's engineering subset is now **$6.9M--$10.0M pre-contingency / $7.6M--$11.0M with contingency**, because `C45` leased-cognition controls and `C47` adaptation/quarantine capacity are now treated as first-order engineering costs rather than deferred operational overhead.

**Reconciliation: C22 engineering costs within C18 fully-loaded budget**

| Component | Baseline | Full Ramp | Source |
|-----------|----------|-----------|--------|
| Engineering (personnel + sovereign compute/model ops + tooling + recruiting) | $6.9M--$7.6M | $8.8M--$11.0M | C22 scope |
| Legal/regulatory/insurance | $280K | $420K | C18 only |
| Grant management (0.5 FTE CFO) | $120K | $160K | C18 only |
| Travel/conferences/recruiting (non-engineering) | $120K | $190K | C18 only |
| Signing bonuses | $180K | $350K | C18 only |
| Wave milestone bonuses | $360K | $570K | C18 only |
| PVR payouts | $200K | $400K | C18 only |
| CRF (Conversion Reserve) | $500K | $1M | C18 only |
| Operating reserve (ring-fenced) | $200K | $200K | C18 only |
| Contingency (10%) | $1.03M | $1.42M | C18 only |
| **TOTAL** | **$11.3M** | **$15.7M** | **C18 fully-loaded** |

### 9.1.2 Timeline Scope Statement

C18's 30--36 month timeline covers the full project lifecycle from entity formation (Month 0) through financial sustainability (Month 36). This includes:

- **Pre-W0 (Months 0--3):** Legal entity formation (Stiftung + PBC), founding capital deployment, initial hiring
- **W0--W5 (Months 3--33):** Technical delivery per C22's 21--30 month implementation timeline
- **Post-W5 (Months 33--36):** Revenue ramp to sustainability, operational transition

C22's W0--W5 delivery timeline is a subset of C18's broader timeline, beginning after entity formation is complete. The ~3-month offset accounts for legal formation, initial fundraising, and founding team assembly that must precede engineering work.

## 9.2 Revenue Sources by Month

| Source | Month Available | Expected Amount |
|--------|----------------|----------------|
| Founding capital | Month 0 | $950K--$1.25M (one-time) |
| Open Philanthropy pre-seed | Month 3--5 | $250K--$500K |
| Open Phil/Schmidt (post-W0) | Month 6--10 | $500K--$1.5M |
| DARPA Phase 1 | Month 10--12 | ~$100K/month for 12 months |
| Horizon Europe pre-finance | Month 12--15 | ~$1.3M--$1.7M (40% at grant signature) |
| Horizon Europe drawdowns | Month 15--36 | ~$80K/month |
| Sovereign compute reservation / sponsorship | Month 6+ | $25K--$100K/month equivalent |
| Consulting revenue | Month 8+ | $20K--$30K/month |
| Foundry pilot retainers / license deposits | Month 18+ | $25K--$150K/month growing |
| Enterprise bounded services | Month 20+ | $20K--$120K/month growing |
| Accountability / assurance packages | Month 20+ | $10K--$60K/month growing |
| Strategic stewardship partnerships | Month 18+ | Varies |

The monthly projection tables below remain staffing-centric and should be read with a sovereign-compute overlay:
- W1-W2: add roughly $20K-$35K/month of `C45` leased-cognition and protocol-infrastructure cost.
- W3-W4: add roughly $45K-$80K/month for `C47` adaptation, quarantine, and evaluation throughput.
- W5: add roughly $70K-$125K/month for sustained native-model promotion and Forge-backed replacement of leased routes.

## 9.3 36-Month Projection (Expected Scenario)

### Phase 0: Months 1--6 (W0)

| Month | Team | Burn | Funding In | Cash on Hand | Runway |
|-------|------|------|-----------|-------------|--------|
| 1 | 4 | $95K | $1,000K (founding) | $905K | 9.5 mo |
| 2 | 5 | $105K | $0 | $800K | 7.6 mo |
| 3 | 6 | $115K | $0 | $685K | 6.0 mo |
| 4 | 6 | $125K | $375K (Open Phil) | $935K | 7.5 mo |
| 5 | 6 | $130K | $0 | $805K | 6.2 mo |
| 6 | 6 | $130K | $0 | $675K | 5.2 mo |

Month 6 is the first stress point: runway dips below 6 months. W0 results should be complete. The post-W0 fundraising pivot activates.

### Phase 1: Months 7--18 (W1--W2)

| Month | Team | Burn | Funding In | Cash on Hand | Runway |
|-------|------|------|-----------|-------------|--------|
| 7 | 8 | $160K | $0 | $515K | 3.2 mo |
| 8 | 9 | $175K | $500K (post-W0 grant) | $840K | 4.8 mo |
| 9 | 10 | $190K | $500K (tranche 2) | $1,150K | 6.1 mo |
| 10 | 10 | $195K | $100K (DARPA start) | $1,055K | 5.4 mo |
| 11 | 11 | $210K | $100K (DARPA) | $945K | 4.5 mo |
| 12 | 11 | $215K | $150K (DARPA + Eth ESP) | $880K | 4.1 mo |
| 13 | 12 | $230K | $1,400K (Horizon 40% pre-finance) | $2,050K | 8.9 mo |
| 14 | 12 | $235K | $100K (DARPA) | $1,915K | 8.1 mo |
| 15 | 13 | $250K | $180K (DARPA + Horizon) | $1,845K | 7.4 mo |
| 16 | 13 | $255K | $100K (Horizon + consulting) | $1,690K | 6.6 mo |
| 17 | 13 | $260K | $105K (Horizon + consulting) | $1,535K | 5.9 mo |
| 18 | 14 | $270K | $210K (Horizon + consulting + stewardship partner) | $1,475K | 5.5 mo |

**Months 7--12 are the most dangerous period.** Runway drops below 4 months at Month 12 if grants are delayed. The Horizon Europe pre-finance at Month 13 is the single most important cash event after founding capital.

### Phase 2: Months 19--36 (W3--W5)

| Month | Team | Burn | Funding In | Cash on Hand | Runway |
|-------|------|------|-----------|-------------|--------|
| 19 | 15 | $300K | $130K (Horizon + consulting + Foundry pilot) | $1,305K | 4.4 mo |
| 24 | 17 | $345K | $900K (Horizon + Foundry/Enterprise + grants) | $1,830K | 5.3 mo |
| 30 | 19 | $380K | $620K (Foundry + Enterprise + partnerships + grants) | $1,545K | 4.1 mo |
| 36 | 19 | $380K | $460K (Foundry + Enterprise + partnerships) | $1,315K | 3.5 mo |

Revenue begins to matter at Month 24+ but does not cover burn until approximately Month 42--48 under expected assumptions.

## 9.4 Scenario Analysis

| Dimension | Pessimistic (25th pct) | Expected (50th pct) | Optimistic (75th pct) |
|-----------|----------------------|--------------------|-----------------------|
| Total funding (36 mo) | $8.0M | $12.0M | $15.5M |
| Peak team size | 10 | 17 | 19 |
| W5 completion | Month 42+ (delayed) | Month 33 | Month 27 |
| Self-sustaining revenue | Month 48+ | Month 40 | Month 34 |
| CRF funded at | $0--$200K | $500K | $1.5M |
| ACI at Month 36 | 0.0001 | 0.001 | 0.005 |
| Survival probability at Month 36 | 55% | 80% | 95% |

## 9.5 Contingency Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| **Yellow** | Runway < 6 months | Hiring freeze. Accelerate grant follow-up. Activate consulting revenue. Monthly board briefing. |
| **Orange** | Runway < 4 months | Scope reduction: defer next wave. Reduce team by 2--3 (LIFO, voluntary separation preferred). Emergency fundraising sprint. |
| **Red** | Runway < 2 months | Emergency scope reduction to 4--5 core engineers. All non-essential spending frozen. Board emergency session. Consider bridge loan against confirmed grants. |
| **Terminal** | Runway < 1 month AND no confirmed incoming funding | Orderly wind-down. Preserve all sensitive IP under Stiftung custody, publish only approved accountability/research artifacts, and provide 30-day notice to employees. |

## 9.6 Danger Zone Analysis

The cash flow model reveals **five distinct danger zones** where runway drops below 4 months:

1. **Month 6--7** (pre-grant, post-W0): Founding capital exhausting, grants not yet awarded
2. **Month 10--12** (pre-Horizon disbursement): DARPA alone insufficient, Horizon decision pending
3. **Month 19--23** (Phase 2 ramp before revenue): Team scaling outpaces revenue growth
4. **Month 25--26** (between grant drawdowns): Inter-tranche gap
5. **Month 29--36** (transition from grants to revenue): Grant funding winds down before revenue covers burn

**Structural reality:** The project operates on permanently tight margins. An $11M-$16M budget over 36 months with 6--19 engineers still leaves limited room for large reserves because sovereign compute, leased cognition, and Forge promotion all compete with payroll for the same cash envelope. This is honest and must be communicated to all stakeholders.

---

# 10. PBC Revenue Operations

## 10.1 Revenue Streams

### Foundry Patent Licensing (Month 14+ pipeline, Month 18+ revenue)

The Foundry is the primary commercialization surface. External organizations do not receive raw access to the Atrahasis novelty engine. Instead, they petition the Foundry for bounded R&D outcomes. Atrahasis performs the high-capability work internally, then licenses approved downstream inventions under field-of-use, milestone, and accountability constraints.

| Phase | Months | Milestone | Revenue |
|-------|--------|-----------|---------|
| Pre-launch | 1--13 | Build intake, release-law review, patent and licensing workflow | $0 |
| Pilot | 14--17 | 2--3 paid discovery retainers, first petition pipeline | $0--$25K/mo |
| Early licensing | 18--24 | 1--3 licensed inventions, first upfront fees and milestone payments | $25K--$150K/mo |
| Scaling | 25--36+ | 3--8 active licenses across verticals; renewals, royalties, and milestone payments | $100K--$500K+/mo |

**Foundry deal shapes:**
- Non-refundable discovery retainer: $25K--$100K
- Non-exclusive field-of-use license: $100K--$500K upfront + support fees
- Exclusive vertical license: $500K--$2M upfront + milestone/royalty structure
- Ongoing stewardship / update retainer: $50K--$250K/year

### Enterprise Bounded Services

Enterprise revenue comes from safe, non-recursive, bounded capabilities exposed through supervised services or tightly constrained software surfaces. Clients purchase outcomes, not direct access to the core research engine.

Examples:
- custom operational forecasting or planning engagements,
- bounded software-generation services,
- annual enterprise contracts for release-approved capability bundles,
- integration and workflow hardening tied to Foundry-derived outputs.

Indicative pricing:
- pilot engagement: $50K--$150K
- annual bounded service contract: $100K--$500K/year
- integration package: $25K--$200K per engagement

### Accountability / Assurance Packages

Open accountability still has economic value. Atrahasis can package selected governance, verification, and safety evidence into paid assurance deliverables for regulators, institutional partners, and high-trust customers without exposing the underlying recursive core.

Examples:
- release-law compliance dossiers,
- governance and refusal-path audit packages,
- bounded verification and safety attestations,
- selective red-team or assurance reviews around licensed outputs.

### Consulting Revenue (Bridge Income)

From Month 8+, the team's distributed systems and ZKP expertise generates consulting revenue at $20K--$30K/month. This is bridge income, not a core business line. Consulting is capped at 15% of engineering hours to prevent distraction from core development.

### Strategic Stewardship Partnerships (Month 18+)

These are mission-aligned institutional relationships that provide funding, co-development support, or infrastructure sponsorship without granting access to the closed core or governance override rights.

Illustrative forms:
- annual strategic research retainer,
- compute or infrastructure sponsorship,
- regulated-sector pilot partnership,
- joint accountability program funding.

Target: 3--6 strategic partners by Month 24.

## 10.2 Revenue Projections by Quarter

| Quarter | Foundry | Enterprise | Assurance | Partnerships | Consulting | **Total** |
|---------|---------|------------|-----------|--------------|------------|-----------|
| Q1--Q4 (Yr 1) | $0 | $0 | $0 | $0 | $0 | **$0** |
| Q5 | $0 | $0 | $0 | $0 | $30K | **$30K** |
| Q6 | $15K | $0 | $0 | $5K | $60K | **$80K** |
| Q7 | $40K | $20K | $10K | $25K | $75K | **$170K** |
| Q8 | $90K | $60K | $15K | $75K | $75K | **$315K** |
| Q9 | $150K | $100K | $30K | $45K | $50K | **$375K** |
| Q10 | $200K | $125K | $40K | $60K | $50K | **$475K** |
| Q11 | $240K | $160K | $45K | $80K | $30K | **$555K** |
| Q12 | $300K | $210K | $50K | $115K | $30K | **$705K** |

**Year 1:** $0 | **Year 2:** $595K | **Year 3:** $2.1M

## 10.3 Foundry Licensing Economics

The Foundry is intentionally higher-friction and higher-value than a task marketplace. Revenue is less continuous but far better aligned to the doctrine.

**Economic structure:**
- Retainers fund problem framing, feasibility review, and safe-scoping before Atrahasis commits core R&D effort.
- Upfront license fees monetize invention transfer without granting internal-core access.
- Milestone payments and royalties capture downstream upside when licensed inventions create real value.
- Support retainers fund bounded post-transfer assistance without converting Atrahasis into an open services shop.

**Commercial safeguards:**
- no license grants direct access to Sanctum or recursion-critical tooling,
- all deals are field-of-use bounded,
- all releases remain subject to constitutional and release-law review,
- licenses can require audit, refusal, and clawback clauses if downstream use violates agreed bounds.

---

# 11. Pitch Strategy

## 11.1 Audiences and Angles

| Audience | Pitch Angle | Key Concern | Ask |
|----------|------------|-------------|-----|
| AI Safety Philanthropy | Structural antidote to profit-driven AI | "Is this team credible?" | $500K--$2M |
| Government Grants | Trustworthy AI infrastructure research | "Is this technically rigorous?" | $1M--$4M |
| Strategic Partners | Early ecosystem positioning | "What do I get?" | Reserved GPU capacity, evaluation/quarantine sponsorship, and co-development |
| Strategic Licensees / Stewardship Partners (Yr 2+) | Access bounded derivative capability without core exposure | "Is this deployable and defensible?" | $100K--$500K+/year |

## 11.2 Core Differentiation

| Their Pitch | Atrahasis Counter |
|-------------|-------------------|
| "We'll build safe AI" | "We'll build the infrastructure that verifies whether ANY AI is safe" |
| "Trust our safety team" | "Trust the math: SNARK proofs, behavioral fingerprints, economic incentives" |
| "We need $30B" | "We need $950K--$1.25M to validate in 3 months, then $11.3M--$15.7M to scale responsibly" |
| "We're a PBC with a trust" | "We're a Stiftung with an immutable constitution and an independent Protector" |
| "Revenue from our AI products" | "Revenue from bounded licensing and services without exposing the recursive core" |

## 11.3 Pitch Deck Structure (12 slides)

1. **The Problem:** "Who Watches the AI?" --- no trustworthy verification infrastructure exists
2. **The Structural Failure:** Profit-driven labs cannot self-govern (OpenAI's 6 mission rewrites)
3. **The Solution:** Verifiable AI infrastructure, public benefit by design
4. **How It Works:** Sovereign coordination, verification, knowledge, settlement, and commercialization infrastructure (`C3`, `C5`, `C6`, `C7`, `C8`, `C38`-`C47`)
5. **Differentiation:** Stiftung vs. PBC vs. corporate subsidiary comparison table
6. **The Evidence:** W0 results (pre-W0: experimental design and kill criteria; post-W0: quantitative data)
7. **The Team:** Engineers, not executives. Academic partners. Advisory board.
8. **The Plan:** 27--36 months, pre-registered milestones, funding gates between waves
9. **The Business Model:** Foundry licensing, bounded enterprise services, accountability packages, path to self-sustainability
10. **The Ask:** Customized per audience
11. **The Governance:** Stiftung + Purpose Trust + PBC entity diagram
12. **The Opportunity:** "The window is now" --- post-OpenAI conversion, 2--3 year receptive window

## 11.4 W0 Evidence Package

Prepared post-W0 and included with every subsequent application:
1. Technical report (quantitative results, methodology, raw data)
2. Academic paper(s) submitted to NSDI, SOSP, ACM CCS, or IEEE S&P
3. Sanitized code/benchmark package or controlled review bundle, as approved under release law
4. One-page executive summary (non-technical)
5. Five-minute narrated video demonstration

---

# 12. Integration with Atrahasis Architecture

## 12.1 Cross-Specification Dependencies

| Spec | C18 Integration Point |
|------|-----------------------|
| **C14 (AiBC Governance)** | Legal entity structure (Stiftung/PBC/Purpose Trust), constitutional layers (L0--L3), spending constraints (5% annual, 20% reserve), immutable prohibitions |
| **C15 (AIC Economics)** | SWECV valuation basis for internal AIC notional values, thermodynamic budget discipline, and pricing guardrails for doctrine-aligned commercialization |
| **C22 (Implementation Plan)** | Wave structure (W0--W5) defines funding stages, team composition, and milestone bonuses. Kill criteria define contingency triggers. Sovereign compute, leased cognition, and Forge adaptation costs now feed the cash flow model. |
| **C5 (PCVM)** | Verification economics underpin assurance-package pricing and the credibility of accountability artifacts. SNARK verification costs (W0 Experiment 2) validate evidence-production cost models. |
| **C3 (Tidal Noosphere)** | Scheduling experiments (W0 Experiment 1) provide grant evidence. Tidal epoch structure defines settlement timing. |
| **C7 (RIF)** | Task orchestration underlies internal Foundry execution and bounded enterprise service delivery. |
| **C8 (DSF)** | Settlement Plane handles internal resource accounting and commercial bookkeeping interfaces without assuming an open public provider marketplace. |
| **C45 (AACP Sovereign Compiler Framework)** | Defines the lease-bounded execution modes, provider controls, and explicit non-native cost surfaces that now shape Stage 1 and Stage 2 spending. |
| **C47 (AACP Automated Cross-Compilation Forge)** | Defines the native model-adaptation lane, quarantine throughput, and promotion costs required to reduce long-run dependence on leased providers. |

## 12.2 Feedback Loops

**C18 depends on C15:** Internal AIC valuation and resource-allocation logic determine employee notional value scenarios and commercialization guardrails.

**C18 depends on C45/C47:** The cost envelope for leased cognition, model adaptation, quarantine, and native promotion determines how much Foundry/Enterprise revenue must be reinvested before the system becomes compute-sovereign.

**C15 depends on C18:** Foundry and enterprise revenue fund the infrastructure that underwrites internal compute budgets and long-horizon sovereignty.

**C22 depends on C18:** Implementation timeline depends on funding arrival. Team size depends on budget allocation. Wave advancement gates depend on cash flow.

**C18 depends on C22:** Burn rate depends on team composition. Milestone bonuses depend on wave advancement criteria. Grant evidence depends on W0 experiment results.

This circular dependency is resolved by treating C22 wave milestones as the independent variable: the funding plan adapts to whichever scenario (pessimistic/expected/optimistic) materializes.

---

# 13. Risk Analysis

## 13.1 Risk Register

| # | Risk | Probability | Impact | Category |
|---|------|------------|--------|----------|
| R-01 | Founding capital insufficient (<$750K) | LOW | CRITICAL | Funding |
| R-02 | Zero grants awarded by Month 12 | 15--22% | HIGH | Funding |
| R-03 | ZKP engineer not hireable at budget | MEDIUM | MEDIUM | Talent |
| R-04 | W0 kill criterion triggered | 10--15% | CRITICAL | Technical |
| R-05 | AIC classified as security (SEC/FMA) | 5--10% | HIGH | Regulatory |
| R-06 | MiCAR authorization delay | MEDIUM | MEDIUM | Regulatory |
| R-07 | Founder burnout or incapacity | 10--15% | HIGH | Operational |
| R-08 | Competitor captures verification market | 15--20% | MEDIUM | Strategic |
| R-09 | Horizon Europe not awarded (highest-impact single grant) | 50--60% | HIGH | Funding |
| R-10 | Key person departure (CTO) | LOW | HIGH | Operational |

## 13.2 Mitigation Strategies

**R-01 (Insufficient founding capital):** Reduce W0 to 3 engineers over 4 months. Activate patron structure (Option C) to supplement.

**R-02 (Grant drought):** Month 6 trigger: activate consulting bridge ($30K--$50K/month). Month 8: reduce team to 4 core engineers. Month 9--12: publish W0 results aggressively, apply to 3--4 additional programs, approach venture philanthropy. Month 12: if zero funding, transition to hibernation (2 engineers, part-time, founder pursues full-time fundraising).

**R-03 (ZKP hiring failure):** Four-tier contingency: (1) direct hire at top of range ($260K + $40K signing), (2) academic partnership (postdoc at $80K--$120K), (3) consulting engagement ($30K--$80K for W0 Experiment 2), (4) defer Experiment 2 to W1 (W0 proceeds with 3 experiments).

**R-04 (W0 kill criterion):** Publish negative results transparently within doctrine bounds. Analyze which hypotheses failed. If partial failure (1 of 3): revise architecture, reduce scope, resubmit grants. If total failure (2+): orderly wind-down, return unused capital, and publish an approved accountability/research record rather than defaulting to full open-source release.

**R-05 (AIC as security):** Convert employee allocations to additional PVR units. CRF deferred to Phase 3+. Marketplace operates in fiat only. AIC becomes internal accounting unit. Engage securities counsel for Regulation D or MiCAR-compliant issuance.

**R-07 (Founder incapacity):** CTO hired as first/second employee with 6-month co-leadership ramp. Key-person insurance ($4M policy). All institutional knowledge documented in shared system. Stiftung Foundation Council can appoint acting director.

**R-08 (Competitor capture):** Structural differentiation (independent nonprofit vs. conflicted for-profit). Accountability-first differentiation rather than open-core imitation. Design for interoperability where safe. Niche-first (government, healthcare, financial regulation where independence is mandatory).

**R-09 (Horizon Europe not awarded):** This is the highest-impact single-grant failure. Mitigation: accelerate DARPA Phase 2, increase sponsored sovereign-compute capacity and bounded integration retainers, apply to 2--3 replacement programs (EIC Pathfinder, additional NSF, UK AISI partnership). Accept slower Phase 2 team ramp (12--14 instead of 17--19).

## 13.3 Honest Assessment

The project operates on permanently tight margins with five distinct danger zones. There is a 15--22% probability of zero grants in Year 1, which triggers a near-death experience requiring emergency scope reduction. There is a 20% probability that the project does not survive to Month 36. These risks are structural to the challenge: a nonprofit building speculative AGI infrastructure with an $11M--$16M budget.

The risk is managed, not eliminated. The Stiftung structure, pre-registered kill criteria, milestone-gated funding, and transparent communication of uncertainty are the tools for managing it. Anyone entering this project --- as a funder, employee, or partner --- must understand that this is a high-risk, high-reward endeavor with a meaningful probability of failure.

---

# 14. Formal Requirements

## 14.1 Funding Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| FR-01 | Founding capital of $950K--$1.25M SHALL be committed and transferred to the PBC operating account before W0 launch. | CRITICAL | Bank statement |
| FR-02 | At least 4 grant applications SHALL be submitted within 4 months of W0 launch. | HIGH | Application receipts |
| FR-03 | At least 1 grant SHALL be awarded within 12 months of W0 launch. | HIGH | Grant agreement |
| FR-04 | An operating reserve of $200K SHALL be maintained in a segregated account, accessible only for payroll in emergency. | HIGH | Separate account statement |
| FR-05 | Runway SHALL NOT drop below 2 months at any time. Breach of this threshold triggers Terminal contingency. | CRITICAL | Monthly financial report |
| FR-06 | No single funding source SHALL exceed 40% of total 36-month funding. | MEDIUM | Annual financial audit |
| FR-07 | Monthly financial reports SHALL be provided to the Stiftung Foundation Council. | HIGH | Board meeting minutes |
| FR-08 | Quarterly runway projections SHALL be updated and distributed to all board members. | HIGH | Projection documents |

## 14.2 Compensation Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| CR-01 | Base salaries SHALL be benchmarked at the 75th percentile of nonprofit technology organizations. | HIGH | Annual compensation survey |
| CR-02 | The PVR plan SHALL be reviewed by employment tax counsel and confirmed as 409A-exempt short-term deferral before any PVR grants. | HIGH | Legal opinion letter |
| CR-03 | All AIC allocation agreements SHALL include an explicit zero-value disclaimer and statement that AIC may never have market value. | HIGH | Signed agreement |
| CR-04 | Total employee AIC allocation SHALL NOT exceed 0.5% of treasury (50M AIC) during the first 3 years. | MEDIUM | AIC ledger audit |
| CR-05 | Wave milestone bonuses SHALL be paid within 30 days of wave advancement certification. | MEDIUM | Payment records |
| CR-06 | PVR payouts SHALL be made within 2.5 months of the end of the fiscal year in which the triggering wave advancement occurs. | HIGH | Payment records |

## 14.3 Operations Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| OR-01 | A CTO or operational successor SHALL be hired by Month 2 and SHALL be capable of independent project leadership by Month 6. | HIGH | Employment agreement |
| OR-02 | Contingency triggers (Yellow/Orange/Red/Terminal) SHALL be evaluated monthly by the financial controller and reported to the board. | MEDIUM | Financial controller report |
| OR-03 | W0 results SHALL be packaged into a doctrine-compliant technical evidence bundle within 30 days of W0 completion. | MEDIUM | Published or controlled-access evidence package |
| OR-04 | A part-time CFO (0.5 FTE) SHALL be engaged from Month 7 for grant management and financial reporting. | HIGH | Engagement agreement |
| OR-05 | All employees SHALL sign IP assignment agreements at hire, assigning work product to the PBC. | HIGH | Signed agreements |
| OR-06 | Consulting revenue SHALL NOT exceed 15% of total engineering hours in any quarter. | MEDIUM | Time tracking records |

## 14.4 Revenue Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| RR-01 | A Foundry pilot commercialization program SHALL launch by Month 14 with 2--3 paid discovery or petitioned R&D engagements. | MEDIUM | Signed engagement letters |
| RR-02 | Foundry licensing agreements SHALL include field-of-use bounds, release-law review, and audit/remedy clauses. | HIGH | Executed license templates |
| RR-03 | Revenue SHALL be tracked monthly by stream (Foundry, enterprise, assurance, partnerships, consulting) and reported to the board. | HIGH | Revenue report |
| RR-04 | Enterprise bounded-service offerings SHALL preserve no-direct-core-access and no-raw-novelty-engine exposure. | HIGH | Service design review |
| RR-05 | The PBC SHALL target self-sustaining revenue (revenue >= burn rate) by Month 40 under expected scenario. | MEDIUM | Financial projections |

## 14.5 Legal Requirements

| ID | Requirement | Priority | Verification |
|----|------------|----------|-------------|
| LR-01 | Stiftung statutes SHALL include an immutable prohibition on for-profit conversion, asset distribution to individuals, and profit extraction, aligned with C14 L0 layer. | CRITICAL | Legal review of filed statutes |
| LR-02 | PBC Certificate of Incorporation SHALL identify the specific public benefit per DGCL 362(a). | HIGH | Filed certificate |
| LR-03 | AIC classification opinion SHALL be obtained from both FMA counsel (Liechtenstein) and US securities counsel before any AIC distribution to employees. | HIGH | Legal opinion letters |
| LR-04 | Key-person insurance on the founder ($4M minimum) SHALL be in force before W0 launch. | HIGH | Insurance policy |
| LR-05 | PBC biennial benefit report SHALL be filed per DGCL 366, aligned with ACI metrics. | MEDIUM | Filed report |

---

# 15. Configurable Parameters

All tunable numbers with defaults and valid ranges. These parameters may be adjusted by the Stiftung Foundation Council or PBC board within the specified ranges.

| Parameter | Default | Range | Unit | Governing Authority |
|-----------|---------|-------|------|-------------------|
| Founding capital target | $1.0M | $750K--$1.5M | USD | Founder decision |
| Operating reserve | $200K | $150K--$300K | USD | Stiftung board |
| Employee AIC pool (3-year) | 50M AIC (0.5%) | 30M--75M AIC | AIC | Stiftung board |
| Founder AIC allocation | 5M AIC (0.05%) | 3M--7M AIC | AIC | Stiftung board |
| CTO AIC allocation | 5M AIC (0.05%) | 3M--7M AIC | AIC | Stiftung board |
| AIC vesting period (non-founder) | 3 years | 2--4 years | years | Employment agreement |
| AIC cliff | 1 year | 6 months--1 year | months | Employment agreement |
| PVR wave multiplier | $1,000/unit | $500--$2,000/unit | USD/wave | PBC board |
| PVR revenue factor denominator | $100K/quarter | $50K--$200K/quarter | USD | PBC board |
| Wave milestone bonus (senior) | $15K--$25K | $10K--$35K | USD/wave | PBC board |
| Signing bonus range | $15K--$50K | $10K--$75K | USD | PBC board |
| Foundry discovery retainer | $50K | $25K--$100K | USD | PBC board |
| Foundry license floor | $250K | $100K--$2M | USD | PBC board |
| Foundry royalty rate | 3% | 1--8% | % of licensed revenue | PBC board |
| Assurance package base price | $25K | $10K--$100K | USD | PBC board |
| Yellow alert threshold | 6 months runway | 5--8 months | months | Stiftung board |
| Orange alert threshold | 4 months runway | 3--5 months | months | Stiftung board |
| Red alert threshold | 2 months runway | 1.5--3 months | months | Stiftung board |
| Consulting hour cap | 15% of eng hours | 10--25% | % per quarter | PBC board |
| CRF target (Phase 2) | $500K | $200K--$2M | USD | Stiftung board |
| Enterprise annual bounded-service contract | $150K/year | $75K--$750K/year | USD | PBC board |
| Strategic stewardship partnership | $150K/year | $50K--$500K/year | USD | PBC board |
| Base salary benchmark percentile | 75th (nonprofit tech) | 50th--90th | percentile | PBC board |
| Contingency reserve | 10% of budget | 8--15% | % | Stiftung board |

---

# 16. Patent-Style Claims

## Claim 1: Stiftung-Anchored Synthetic Equity Compensation

A method of compensating employees of a nonprofit foundation's operational subsidiary, comprising:
(a) allocating units of an internal digital currency (AIC) from a foundation treasury to employees of a public benefit corporation wholly owned by the foundation;
(b) vesting said AIC units over a defined period (default 3 years) with a cliff period (default 1 year);
(c) anchoring the notional value of said AIC units to a capability index (ACI) calculated via a Systemic Weighted Expected Creation Value (SWECV) formula per C15;
(d) deferring convertibility of said AIC units until a Conversion Reserve Fund (CRF) is funded from operational revenue;
(e) wherein said allocation is structured as a contractual right to a digital asset (not equity), with zero fair market value at grant, thereby avoiding taxable events until conversion;
(f) wherein the foundation's constitutional provisions immutably prohibit conversion to a for-profit structure, preventing the dilution or value extraction that characterizes equity instruments.

## Claim 2: Pre-Registered Kill Criteria as Fundraising Pivot

A staged funding method for speculative technology development, comprising:
(a) raising minimum founding capital (Stage 0) sufficient to fund a defined validation experiment period (W0);
(b) executing pre-registered experiments with quantitative success and kill criteria published before execution;
(c) using the quantitative results of said experiments as the primary evidence package for all subsequent fundraising activities (Stage 1 and Stage 2);
(d) structuring Stage 1 grant applications to incorporate W0 results as validation evidence, such that pre-W0 applications reference experimental design while post-W0 applications include measured data;
(e) wherein kill criteria triggering terminates Stage 1 fundraising and initiates orderly wind-down, preserving funder confidence through transparent accountability.

## Claim 3: W0-Pivot Portfolio Funding with Foundry-First Commercialization

A method of funding nonprofit technology infrastructure comprising:
(a) establishing a three-stage funding architecture (founding capital, grants/partnerships, Foundry/enterprise revenue) where each stage's deliverables unlock the next stage's funding sources;
(b) diversifying across 4+ funding categories (government grants, private foundations, strategic partnerships, Foundry licensing, enterprise services) such that no single source exceeds 40% of total funding;
(c) operating a public benefit corporation subsidiary that generates revenue through bounded patent licensing, enterprise service contracts, assurance packages, and other constitutionally permitted interfaces rather than open public access to the core system;
(d) managing cash flow against defined contingency triggers (Yellow/Orange/Red/Terminal) with pre-specified actions at each threshold;
(e) wherein the nonprofit foundation structure (Stiftung) immutably prohibits the asset distribution, profit extraction, and for-profit conversion that have captured other nonprofit AI organizations.

---

# 17. Open Questions

## 17.1 Unresolved Design Decisions

| # | Question | Impact | Resolution Timeline |
|---|----------|--------|-------------------|
| OQ-01 | Which accountability artifacts, code excerpts, or research bundles should be public-by-default versus controlled-access under release law? | MEDIUM | Pre-W0 |
| OQ-02 | How should international employees (non-US) be handled? Employer of Record adds $400--$800/month per person. Budget for 1--3 international hires ($10K--$20K/year). | LOW | Month 1 |
| OQ-03 | Who will serve as the independent Liechtenstein-licensed trustee on the Foundation Council? This person must be identified and recruited during formation. Budget: $10K--$20K/year. | MEDIUM | Month -3 |
| OQ-04 | Should the Founding Patron program (Option C) be used if the co-founder path (Option B) fails? Legal opinion required on whether AIC "gratitude allocations" constitute securities. | HIGH | Month -2 |
| OQ-05 | What happens to AIC allocations if the project terminates before CRF is operational? Current design: unvested AIC returns to treasury; vested AIC is worthless (no CRF). Should there be a terminal-event payout in fiat? | MEDIUM | Pre-W0 |
| OQ-06 | Should the PBC pursue B Corp certification alongside PBC status for additional credibility with philanthropic funders? | LOW | Phase 1 |
| OQ-07 | How will the Stiftung manage AIC treasury value if ACI appreciates significantly? The 5% annual spending cap may be insufficient for operations at scale. | LOW (long-term) | Phase 2+ |

---

# 18. Glossary

| Term | Definition |
|------|-----------|
| **ACI** | Atrahasis Capability Index. Composite metric measuring the system's verification, coordination, and settlement capabilities. Drives AIC reference price via C15 SWECV formula. |
| **AIC** | Atrahasis Internal Currency. Internal unit of account and resource-allocation mathematics inside the Atrahasis system. |
| **CRF** | Conversion Reserve Fund. Fiat reserve (target $500K--$2M) enabling AIC-to-fiat conversion at the reference rate (C15 DA-01). |
| **DGCL** | Delaware General Corporation Law. Governs the PBC. |
| **FMA** | Financial Market Authority (Finanzmarktaufsicht). Liechtenstein financial regulator. |
| **Foundry** | The commercialization membrane that converts internally generated inventions into bounded licensing and release-managed external products. |
| **Fully-loaded cost** | For personnel planning, total employer cash cost per employee: salary + benefits + payroll taxes + equipment + stipends. Shared sovereign compute/model operations are budgeted separately in Section 9.1. Estimated ~$270K/year average. |
| **MiCAR** | Markets in Crypto-Assets Regulation. EU regulation governing token issuance and crypto-asset service providers. |
| **Open Accountability** | Publication posture that favors safety audits, governance signals, and bounded evidence release without exposing recursion-critical capabilities. |
| **PBC** | Public Benefit Corporation. Delaware for-profit entity with dual fiduciary duty (stockholder interests + identified public benefit). |
| **PGR** | Personen- und Gesellschaftsrecht (Persons and Companies Act). Liechtenstein law governing Stiftungen. |
| **PVR** | Phantom Value Rights. Contractual right to cash bonus calculated from PVR units x wave multiplier x revenue factor. 409A-exempt as short-term deferral. |
| **Runway** | Months of remaining cash at current burn rate. Cash on Hand / Monthly Burn Rate. |
| **Strategic stewardship partnership** | Mission-aligned institutional funding relationship that supports Atrahasis without granting direct access to the closed core. |
| **Stiftung** | Liechtenstein foundation. Nonprofit legal entity that holds IP, manages AIC treasury, and enforces constitutional governance. |
| **SWECV** | Systemic Weighted Expected Creation Value. C15 formula for calculating AIC reference price as a function of ACI. |
| **TVTG** | Token and Trustworthy Technology Act. Liechtenstein law establishing legal framework for token issuance. |
| **Wave (W0--W5)** | Implementation phases defined in C22. Each wave has pre-registered success criteria and kill criteria. |
| **W0 Pivot** | Fundraising strategy: use minimum capital to run validation experiments, then use quantitative results as primary evidence for all subsequent fundraising. |

---

# 19. References

## Atrahasis Specifications

- C3: Tidal Noosphere Master Tech Spec (coordination layer)
- C5: PCVM Master Tech Spec (verification layer)
- C7: RIF Master Tech Spec (orchestration layer)
- C8: DSF Master Tech Spec (settlement layer)
- C14: AiBC Master Tech Spec (governance, legal entity structure)
- C15: AIC Economics Master Tech Spec (valuation, CRF, SWECV)
- C22: Implementation Plan (waves, team composition, kill criteria)

## External Sources

### Organizational Precedents
- OpenAI restructuring timeline: TechCrunch (2025-10-28), TIME, Fortune
- Anthropic LTBT and funding: anthropic.com, TechCrunch, CNBC
- Ethereum Foundation grants: ethereum.org, CryptoBriefing
- Mozilla Foundation compensation: ProPublica Nonprofit Explorer
- Linux Foundation compensation: ProPublica Nonprofit Explorer

### Funding Programs
- DARPA I2O BAA HR001126S0001: darpa.mil
- DOE Genesis Mission ($320M): grantedai.com
- EU Horizon Europe 2026--2027: grantsfinder.eu
- Open Philanthropy AI Safety: openphilanthropy.org

### Legal Frameworks
- Liechtenstein Stiftung: PGR Art. 522 et seq.; GLI Blockchain Laws 2026; Grant Thornton overview
- Delaware PBC: DGCL Subchapter XV; Cooley GO FAQ; Harvard Law review
- MiCAR/TVTG: EWR-MiCA-DG (effective Feb 2025); FMA Liechtenstein

### Compensation and Market Data
- AI talent salary benchmarks: HeroHunt (2025), Rise (2026)
- ZK talent market: Blockchain Staffing Ninja (2026)
- Phantom equity legal structure: Carta, Plancorp, Cummings Law
- IRC 409A short-term deferral: Treas. Reg. 1.409A-1(b)(4)

---

*End of C18 Master Tech Spec. Document ID: C18-MTS-v1.0.1. Total budget: $11.3M--$15.7M. Duration: 30--36 months. Structure: Liechtenstein Stiftung + Delaware PBC. Strategy: Staged Portfolio Funding with W0 Pivot.*
