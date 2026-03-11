# C18 --- Funding Strategy + Business Operations --- IDEATION

**Invention ID:** C18
**Stage:** IDEATION
**Date:** 2026-03-11
**Subject:** Funding strategy, business model, personnel compensation, operating costs, and pitch architecture for Atrahasis Inc (AiBC) --- aligned with Liechtenstein Stiftung / Delaware PBC structure, integrating C15 AIC valuation and C22 implementation plan
**Constraint Context:**
- Legal: Liechtenstein Stiftung (nonprofit) + Delaware PBC (operational) + Cayman Purpose Trust (Phase 2+)
- Budget: $8M--$12M over 27--36 months (from C22 DA-06: $5.4M--$8.8M implementation + contingency)
- Team: 6 engineers (W0) scaling to 19 (W5)
- Mission: Achieve AGI through planetary-scale AI infrastructure; reward human team generously within nonprofit governance
- Founder: Joshua Dunn (partner, in-the-system-not-above-it principle)

---

# PART 1 --- PRE-IDEATION QUICK SCAN

## 1.1 Nonprofit AI Research Organizations

### OpenAI (2015--2026)
- **Original structure:** 501(c)(3) nonprofit, $1B initial pledge from Altman, Musk, and others
- **2019 pivot:** Created "capped-profit" subsidiary (OpenAI LP) with 100x return cap to attract venture capital. Raised $1B from Microsoft.
- **2023--2025 escalation:** Profit cap began increasing 20%/year. Total funding exceeded $13B. $157B valuation by late 2024.
- **October 2025:** Completed for-profit recapitalization to OpenAI Group PBC. The original nonprofit (now "OpenAI Foundation") retained 26% equity stake ($130B value). Microsoft holds 27%.
- **Lesson:** The nonprofit-to-for-profit pipeline is well-trodden and lucrative --- but it destroys mission alignment. OpenAI's mission statement changed 6 times in 9 years. The foundation became a minority stakeholder in the entity it created.
- **Warning for Atrahasis:** The AiBC's constitutional prohibition on for-profit conversion (C14 immutable layer) is the firewall OpenAI lacked. But the economic pressure that drove OpenAI's conversion --- $14B/year burn rate, $580B infrastructure costs --- will apply to any system at scale.

### Anthropic (2021--2026)
- **Structure:** Delaware Public Benefit Corporation with Long-Term Benefit Trust (LTBT) holding Class T shares for board election rights
- **Funding:** $300M from Google (2023), $2B+ additional Google investment, $1B more in Jan 2025, $30B Series G at $380B valuation (2026)
- **LTBT composition:** 4 independent trustees (Shah, Bahl, Robinson, Fontaine) --- no corporate investors on the trust
- **Key insight:** Anthropic achieved massive funding ($30B+) while maintaining a mission-governance structure through the LTBT. Google has no voting rights or board seats despite $3B+ investment. This proves that investors will accept governance constraints if the technology is compelling enough.
- **Warning for Atrahasis:** Anthropic is still a for-profit PBC. Investors expect returns. The LTBT provides governance protection but does not eliminate the profit motive. A Stiftung has no profit motive by design --- this is structurally stronger but makes fundraising harder.

### DeepMind (2010--2014--present)
- **Original:** UK company with "ethics board" requirement in acquisition agreement
- **2014:** Acquired by Google/Alphabet for ~$500M
- **Outcome:** Ethics board never materialized as independent body. DeepMind's research direction is now set by Alphabet's commercial priorities.
- **Lesson:** Acquisition is the ultimate capture vector. The Stiftung structure prevents acquisition since foundation assets cannot be sold.

## 1.2 Foundation-Funded Technology Development

### Mozilla Foundation
- **Structure:** 501(c)(3) foundation owns Mozilla Corporation (for-profit subsidiary)
- **Revenue:** ~$500M/year, primarily from search engine default agreements (Google pays Mozilla to be default search in Firefox)
- **Compensation:** Average $203K/employee (2023), executives at $3.3M total, CEO (Mitchell Baker) earned $6.1M before stepping down
- **Model:** Nonprofit owns for-profit subsidiary, profits flow upward
- **Relevance:** Mozilla demonstrates that a nonprofit/for-profit hybrid can sustain significant engineering operations and competitive compensation. But Mozilla's revenue depends on a single commercial relationship (Google), creating dependency.

### Linux Foundation
- **Structure:** 501(c)(6) trade association
- **Revenue:** ~$260M/year from membership fees (tiered: Platinum $500K, Gold $100K, Silver $20K)
- **Compensation:** Average $228K/employee (2023), executives at $7.1M total, 298 employees
- **Model:** Corporate membership funds shared infrastructure development
- **Relevance:** Membership-tiered funding works for industry consortia but requires a large ecosystem of corporate beneficiaries. Atrahasis at Phase 0 has no corporate ecosystem yet.

### Apache Software Foundation
- **Structure:** 501(c)(3) charity
- **Revenue:** ~$2M/year from sponsorship + individual donations
- **Staff:** ~12 paid employees, 8,000+ volunteers
- **Model:** Volunteer-driven with minimal paid staff
- **Relevance:** Not applicable --- Atrahasis requires 6--19 full-time engineers, not volunteers.

## 1.3 Stiftung-Based Technology Ventures

### Ethereum Foundation
- **Structure:** Swiss Stiftung (Zug, Switzerland)
- **Initial funding:** 2014 ICO raised ~$18.3M (31,591 BTC at the time)
- **Endowment management:** Foundation held significant ETH reserves (peak: ~$10B), managed through a spending policy
- **Grant programs:** $32M in Q1 2025 alone (94 projects), 63% increase from prior quarter. New ESP model with targeted RFPs and wishlists.
- **Key insight:** The ICO created an endowment large enough to fund decades of development. But this was possible because Ethereum launched in 2014 when ICO regulatory scrutiny was minimal. In 2026, token sales face MiCAR (EU), SEC scrutiny (US), and other regulatory frameworks.
- **Relevance for Atrahasis:** The Stiftung model works. But Atrahasis cannot replicate the ICO path. AIC is explicitly NOT a security (C14, C15 regulatory design). The funding must come from other sources.

### Cardano/IOHK/Emurgo
- **Structure:** Three-entity model --- IOHK (for-profit research, Charles Hoskinson), Emurgo (for-profit venture), Cardano Foundation (Swiss Stiftung)
- **Funding:** IOHK funded through ADA token reserves from genesis; Cardano Foundation holds ADA endowment
- **Relevance:** Multi-entity model with nonprofit foundation + for-profit subsidiaries, each with different mandates.

### Web3 Foundation (Polkadot)
- **Structure:** Swiss Stiftung
- **Funding:** DOT token sale raised ~$145M (2017)
- **Grant programs:** Active grant program for ecosystem development
- **Relevance:** Another Stiftung + token sale model, but again from the 2017 ICO era.

## 1.4 Hybrid Nonprofit/For-Profit Structures

### Chan Zuckerberg Initiative (CZI)
- **Structure:** LLC (not a foundation), owned by Zuckerberg/Chan
- **Funding:** $45B+ in Meta shares pledged
- **Model:** Uses LLC structure to make both investments and grants
- **Relevance:** Demonstrates that mission-driven entities can use flexible legal structures. But CZI's funding comes from a single billionaire's personal wealth.

### Schmidt Futures
- **Structure:** Philanthropic LLC
- **Model:** Makes grants, investments, and operates programs
- **Relevance:** Potential funder for AI governance/safety research

## 1.5 Government-Funded Moonshot Programs

### DARPA
- **Model:** Milestone-based contracts, 3--5 year program cycles, $5M--$100M per program
- **2026 AI programs:** I2O BAA (HR001126S0001) covers transformative AI, trustworthy/explainable/ethically-aligned systems
- **Key insight:** DARPA funds high-risk, high-reward research with pre-registered milestones and kill criteria. This maps directly to C22's W0 experiment structure.
- **Constraint:** DARPA funding typically requires US entity (Delaware PBC qualifies), US-based researchers, and alignment with defense applications.

### DOE/ARPA-E
- **2026:** $320M "Genesis Mission" for 26 AI Grand Challenges
- **Model:** Challenge-based funding with defined technical milestones
- **Relevance:** Atrahasis's verification, coordination, and knowledge synthesis systems could qualify as AI infrastructure research.

### EU Horizon Europe
- **2026--2027:** EUR 14B total, ~EUR 2B for AI specifically
- **AI Security calls:** EUR 3--4M per selected project (adversarial robustness, data integrity, private AI)
- **AI Governance/Standardization:** Supports AI governance standards development
- **GenAI4EU:** EUR 700M specifically for generative AI
- **Constraint:** Requires EU-based entity or consortium partner. Liechtenstein is EEA member, so the Stiftung qualifies.
- **Key insight:** Horizon Europe is the largest accessible grant program for AI governance and safety research in 2026. EUR 3--4M per project could fund 30--50% of a single wave.

### NSF (National Science Foundation)
- **Model:** Investigator-initiated grants, typically $500K--$5M for 3--5 years
- **Relevance:** Funds fundamental research in distributed systems, verification, AI safety
- **Constraint:** Requires US entity (PBC qualifies), typically university-affiliated PI

---

# PART 2 --- DOMAIN TRANSLATOR BRIEF

## Round 0: Cross-Domain Analogies

The C18 challenge is threefold: (1) fund an $8M--$12M, 27--36 month technology project through a nonprofit foundation, (2) compensate a small elite team generously within nonprofit constraints, and (3) create a compelling pitch for speculative technology. The following analogies illuminate structural solutions from unrelated domains.

---

### Analogy 1: Cathedral Building (Medieval Europe)

**Domain:** Medieval cathedrals took 50--200 years to build. Funding came from diverse sources: royal grants, papal indulgences, merchant guild donations, pilgrimage revenue, and community labor tithes. No single funder could afford a cathedral. The Bishop assembled a portfolio of funding sources, each with different motivations and timelines.

**Structural Parallels:**
- Multi-decade timeline with uncertain completion
- No single funder has sufficient resources
- The "product" does not exist yet and is speculative
- The institution (the See/Diocese) is perpetual and nonprofit
- Workers must be retained across funding gaps

**Insights for C18:**
- **Portfolio funding is mandatory.** No single grant, investor, or revenue stream will cover $8M--$12M. C18 must design a portfolio of 4--6 funding sources with staggered timelines.
- **Milestone visibility matters.** Cathedral builders showed visible progress (foundation, walls, roof) to maintain donor confidence. C22's wave structure provides natural milestones: W0 validation, W1 stubs, W2 functional layers.
- **Worker retention across funding gaps requires reserves.** Cathedral projects maintained 6--12 months of worker wages in reserve. C18 must include a 6-month runway buffer.

---

### Analogy 2: Pharmaceutical R&D Pipeline (Biotech)

**Domain:** Biotech startups fund speculative drug development through staged investment rounds tied to clinical milestones. Pre-clinical ($2--5M seed), Phase 1 ($5--20M Series A), Phase 2 ($20--100M Series B), Phase 3 ($50--300M Series C). At each stage, the probability of success increases and new investors enter at higher valuations. Failure triggers ratchets, pivots, or wind-down.

**Structural Parallels:**
- Speculative technology with staged probability gates
- Each stage requires different funding amounts and sources
- Kill criteria are pre-registered (clinical endpoints)
- Team compensation includes significant equity upside
- The product does not generate revenue until late stages

**Insights for C18:**
- **Map C22 waves to funding stages.** W0 = pre-clinical ($500K--$1M). W1--W2 = Phase 1 ($3M--$5M). W3--W5 = Phase 2 ($5M--$8M). Each stage has defined success criteria.
- **Use milestone-triggered funding tranches.** Rather than raising $12M upfront, raise $2--3M for W0--W1 and unlock subsequent tranches upon hitting C22 advancement criteria. This reduces funder risk and aligns incentives.
- **Compensation: phantom equity tied to ACI milestones.** Biotech uses equity upside. Atrahasis is nonprofit, so real equity is impossible. But phantom equity (synthetic equity rights) tied to ACI achievement milestones can replicate the incentive structure.

---

### Analogy 3: Film Production Financing

**Domain:** Independent films are funded through a combination of: pre-sales (distributors buy rights before the film exists), equity investment (producers invest for profit share), tax credits (government incentives), gap financing (banks lend against pre-sale contracts), and completion bonds (insurance against non-delivery). A $10M indie film might have 5--8 funding sources.

**Structural Parallels:**
- Budget in the $8--12M range
- The product is speculative (no one knows if the film will be good)
- Multiple funding sources with different risk/return profiles
- Completion timeline is 18--36 months
- Talent (actors/directors) must be attracted with competitive compensation

**Insights for C18:**
- **"Pre-sales" = compute service commitments.** Organizations that commit to using the Atrahasis task marketplace upon launch provide forward revenue that can secure bridge financing.
- **"Tax credits" = government grants.** EU Horizon Europe, DARPA, NSF grants function like film tax credits --- they reduce the net cost that must be raised from other sources.
- **"Completion bond" = milestone escrow.** Funders' capital is held in escrow and released upon C22 milestone achievement. Protects both parties.
- **Talent attraction: deferred compensation + milestone bonuses.** Film directors accept lower upfront pay for backend profit participation. Engineers accept below-market base salary for milestone bonuses and AIC allocation.

---

### Analogy 4: Open Source Business Models (Red Hat, Elastic, Canonical)

**Domain:** Open source companies give away the core technology and monetize through enterprise support, managed services, premium features, and certifications. Red Hat generated $3.4B revenue selling support for free software. Canonical (Ubuntu) is funded by Mark Shuttleworth's personal investment + enterprise services.

**Structural Parallels:**
- Core technology is open/public benefit (like Stiftung IP)
- Revenue comes from services around the technology
- Early-stage funding often comes from founder or mission-aligned investors
- Team attracted by mission + technical challenge, not just salary

**Insights for C18:**
- **The PBC can sell services while the Stiftung holds IP.** Verification-as-a-service, AI task execution, compute brokerage --- these are PBC revenue streams that fund operations while the Stiftung retains IP ownership.
- **Early-stage: founder investment + mission-aligned grants.** Canonical survived on Shuttleworth's $10M+ investment for years before enterprise revenue materialized. Joshua Dunn's founding contribution + mission-aligned grants bridge to service revenue.
- **Enterprise partnerships for Phase 2+.** Once the system is functional (W3+), enterprise partnerships (universities, research labs, AI companies) provide recurring revenue.

---

### Analogy 5: Space Agency Funding (ESA Model)

**Domain:** The European Space Agency (ESA) is funded by member-state contributions proportional to GDP (~EUR 7.8B/year in 2025). Programs are approved through multi-year ministerial councils. Industrial contracts are distributed by "juste retour" --- each country receives contracts proportional to its contribution.

**Structural Parallels:**
- Multi-stakeholder funding for shared infrastructure
- Long-term programs (5--10 year horizons)
- Technology benefits are public goods
- Industrial participation provides indirect returns to funders

**Insights for C18:**
- **"Member" funding model for Phase 2+.** Organizations (universities, AI labs, governments) contribute to the Stiftung in exchange for governance participation rights (not equity --- advisory board seats, priority task marketplace access, co-development agreements).
- **"Juste retour" = contributor benefits proportional to contribution.** Funders receive compute credits, priority API access, or research collaboration proportional to their contribution level.
- **Multi-year commitment structure.** ESA's ministerial council model --- funders commit to 3--5 year programs, not annual grants --- provides funding stability.

---

## Domain Translator Summary

| Analogy | Key Insight for C18 |
|---------|-------------------|
| Cathedral building | Portfolio funding (4--6 sources), milestone visibility, 6-month runway buffer |
| Biotech pipeline | Map C22 waves to funding stages, milestone-triggered tranches, phantom equity |
| Film production | Pre-sales (compute commitments), grants as tax credits, deferred compensation |
| Open source business | PBC sells services, Stiftung holds IP, founder bridge + enterprise revenue |
| ESA funding model | Member contributions with governance participation, multi-year commitments |

---

# PART 3 --- IDEATION COUNCIL

## Council Composition

- **Visionary:** Bold funding architecture, maximum ambition
- **Systems Thinker:** Structural coherence, cash flow modeling, incentive alignment
- **Critic:** Failure modes, regulatory obstacles, team retention risks

---

## Round 1: Independent Concept Generation

### Visionary --- Concept C18-A: "Stacked Funding Architecture"

The $8M--$12M budget is achievable through a deliberately sequenced stack of funding sources, each unlocking the next:

**Layer 1: Founding Capital ($500K--$1M)**
- Joshua Dunn personal investment + 1--2 founding partners
- Covers W0 (3 months, 4--6 engineers)
- Demonstrates skin-in-the-game to subsequent funders

**Layer 2: Mission-Aligned Grants ($2M--$4M)**
- EU Horizon Europe: AI governance/safety (EUR 3--4M per project) --- Stiftung eligible as EEA entity
- DARPA I2O BAA: Trustworthy AI, verification systems --- PBC eligible as US entity
- NSF: Distributed systems, formal verification research
- Private foundations: Open Philanthropy, Schmidt Futures, Patrick J. McGovern Foundation
- Timeline: Submit during W0, receive during W1

**Layer 3: Strategic Partnerships ($2M--$3M)**
- Compute provider partnerships: Lambda Labs, CoreWeave, or academic HPC centers provide compute credits in exchange for being early ecosystem partners
- Research institution partnerships: Universities (MIT, ETH Zurich, Oxford) co-develop specific layers with their researchers, co-funded by their existing grants
- AI lab partnerships: Smaller AI companies integrate with the verification/coordination layer for independent testing

**Layer 4: AIC Ecosystem Bootstrapping ($1M--$2M)**
- Once W2--W3 produces functional layers, early compute marketplace revenue begins
- Provider onboarding per C15 DA-02: BRA agreements with Tier 2 cloud + GPU networks
- Revenue flows through PBC, funds operations

**Layer 5: Institutional Membership ($1M--$3M, Phase 2+)**
- Modeled on Linux Foundation tiers: Founding Member ($250K/year), Contributing Member ($100K/year), Associate Member ($25K/year)
- Members receive: advisory board seat, priority compute access, co-development rights, brand association
- Target: 4--8 Founding Members by Month 18

**Compensation Model:**
- Base salary: 75th percentile nonprofit tech (not 50th --- we compete with Mozilla/Linux Foundation, not Red Cross)
- Benchmark: $180K--$220K base for senior engineers, $250K+ for ZKP/distributed systems specialists
- **AIC Milestone Allocation:** Each engineer receives an AIC allocation from the Stiftung treasury (not equity --- an allocation of the internal currency) that vests upon C22 wave milestones. If ACI reaches target thresholds, the AIC has real conversion value through the CRF (C15 DA-01).
- **Phantom Value Rights (PVR):** A contractual right to a cash bonus calculated as a function of ACI growth. If ACI doubles, PVR holders receive a defined cash bonus from PBC operating revenue. This replicates startup equity upside without actual equity.
- **Milestone bonuses:** $25K--$50K cash bonus per C22 wave advancement criterion met.

**Pitch Strategy:**
- Target: AI governance/safety funders first (Open Philanthropy, Schmidt Futures, EU Horizon)
- Pitch angle: "The first AI infrastructure designed for public benefit from Day 1, not retrofitted after a profit pivot"
- Key differentiator: 13 specifications already designed --- this is not a whitepaper project, it's an implementation-ready architecture with pre-registered kill criteria

### Systems Thinker --- Concept C18-B: "Milestone-Gated Capital"

The Visionary's stack is directionally correct but lacks cash flow discipline. The core risk is timing: grants take 6--12 months from application to disbursement, partnerships take 3--6 months to negotiate, and revenue is 18+ months away. The team needs to be paid every two weeks.

**Cash Flow Architecture:**

| Month | Source | Amount | Cumulative | Burn Rate | Runway |
|-------|--------|--------|------------|-----------|--------|
| 1--3 | Founding capital | $750K | $750K | $100K/mo (4 eng + cloud) | 7.5 mo |
| 4--6 | Grant advance (Horizon Europe) | $500K | $1.25M | $150K/mo (6 eng) | 8.3 mo |
| 7--9 | DARPA contract (if awarded) | $400K | $1.65M | $150K/mo | 11 mo |
| 10--12 | Strategic partnership compute credits | $300K equiv | $1.95M | $200K/mo (11 eng) | 9.75 mo |
| 13--18 | Grant drawdowns + partnership revenue | $1.5M | $3.45M | $250K/mo (13 eng) | 13.8 mo |
| 19--27 | Revenue + institutional membership | $3M | $6.45M | $350K/mo (19 eng) | 18.4 mo |
| 28--36 | Scaling revenue + renewal grants | $3.5M | $9.95M | $350K/mo | 28.4 mo |

**Key principle:** Never let runway drop below 6 months. If runway falls below 6 months, trigger a hiring freeze and scope reduction per C22 DA-05 simplified team (4 engineers for W0).

**Compensation Model:**

I agree with the Visionary on base salary benchmarks but propose a more structured incentive system:

- **Tier 1 (Base):** 75th percentile nonprofit tech: $180K--$250K depending on role and market. ZKP and Rust distributed systems specialists command premium.
- **Tier 2 (AIC Allocation):** 0.01%--0.05% of treasury per engineer, vesting over 3 years with 1-year cliff. At ACI=0.01, AIC reference price is ~$100 (C15 formula), so 0.01% of 10B = 1M AIC = ~$100M notional. Even at a 99% discount for illiquidity and risk, this is $1M notional per engineer --- meaningful upside.
- **Tier 3 (Phantom Value Rights):** Cash bonus = PVR_units x (ACI_current - ACI_at_grant) x PVR_multiplier. PVR_multiplier set so that if ACI goes from 0.001 to 0.01 (10x), a senior engineer receives ~$100K--$500K bonus.
- **Tier 4 (Wave Milestone Bonus):** $10K--$25K per wave advancement, paid from PBC operating funds.

**Pitch Strategy:**
- Lead with C22's pre-registered kill criteria: "We will know within 3 months if this architecture works. Your first $750K buys a definitive answer."
- Second: SWECV framework (C15): "Conservative terminal value: $340B. At ACI=0.10, even the pessimistic scenario produces $100B in expected creation value."
- Third: Implementation readiness: "21,000 lines of specifications, 13 Master Tech Specs, 3 defense systems, all reconciled. This is the most thoroughly designed AI infrastructure ever attempted."

### Critic --- Concept C18-C: "Lean Bootstrap with Safety Nets"

Both C18-A and C18-B assume that grants and partnerships will materialize on schedule. They won't. Grant cycles are 9--18 months. Partnership negotiations take 6--12 months. Here is the realistic scenario:

**Month 1--6 funding availability:**
- Founding capital: Yes (Joshua Dunn controls this)
- Grants: No (applications submitted but not yet awarded)
- Partnerships: No (negotiations ongoing)
- Revenue: No (system doesn't exist)

**So the real question is: can you fund 6 months of operations with founding capital alone?**

At 4 engineers x $200K/year fully loaded = $66K/month payroll + $6K/month cloud = $72K/month. Six months = $432K. With a 50% buffer: $648K.

**Founding capital requirement: $650K--$750K minimum.** This is the irreducible number. If Joshua cannot commit this, the project cannot start.

**Failure Modes I See:**

1. **Grant timing gap.** You apply for Horizon Europe in Month 1, get awarded in Month 9, first drawdown in Month 12. That's 12 months with no grant revenue. Founding capital must cover this.

2. **Specialist hiring failure.** ZKP engineers command $175K--$250K+ base. The Visionary's 75th percentile nonprofit target is approximately $180K--$220K. But the market for ZKP talent is $200K--$275K at for-profit companies. The nonprofit premium (mission, AIC allocation, phantom equity) must close a $50K--$100K gap. Will it? Unknown.

3. **AIC valuation circularity.** The compensation model assumes AIC has future value. But AIC's value depends on the system being built. The system being built depends on the team being hired. The team being hired depends on AIC having future value. This is a confidence game --- it works if everyone believes, fails if anyone doubts.

4. **Regulatory classification of AIC allocation.** If AIC allocations to employees are classified as taxable compensation (likely), the tax burden falls on the employee at grant/vest --- but the AIC may not be convertible yet. This creates a tax liability with no liquidity. IRC 409A compliance is critical.

5. **Stiftung employment law.** Liechtenstein employment law is not US employment law. If the Stiftung directly employs anyone, Liechtenstein labor regulations apply. More likely: the PBC employs all staff, the Stiftung funds the PBC through grants.

**My Concept C18-C:**

- **Phase 0 (Month 1--6):** $750K founding capital. 4 engineers. Run W0. Apply for grants.
- **Phase 1 (Month 7--18):** First grant(s) arrive. Scale to 8--11 engineers. Run W1--W2. Begin partnership negotiations.
- **Phase 2 (Month 19--36):** Multiple grant streams + early revenue + partnerships. Scale to 15--19 engineers. Run W3--W5.

**If grants don't arrive by Month 12:** Trigger contingency: reduce to 2 engineers (architect + 1 senior), preserve IP and specifications, pivot to consulting revenue (the team's expertise in distributed systems/ZKP is commercially valuable), and reapply for grants with W0 results as evidence.

**Compensation Model (conservative):**
- Base: Market rate for the PBC's geographic location (likely remote-first, so US rates)
  - Senior Rust engineer: $180K--$200K
  - ZKP specialist: $200K--$250K (premium required)
  - ML engineer: $170K--$200K
  - Protocol engineer: $160K--$180K
  - Technical architect: $220K--$280K
- AIC allocation: YES, but with explicit disclaimer that AIC has zero current market value and may never have market value. No tax event until conversion. Structure as deferred compensation under IRC 409A.
- Phantom Value Rights: YES, but denominated in USD, paid from PBC operating funds, triggered by C22 wave milestones (not AIC price). This avoids the circularity problem.
- Signing bonus: $15K--$30K for specialists to compensate for the nonprofit salary gap.

**Pitch Strategy:**
- Do NOT lead with SWECV or $340B terminal values. Institutional funders will dismiss this as speculation.
- Lead with: "We have a pre-registered experiment (W0) with quantitative kill criteria. Fund the experiment. If it fails, you lose $750K and gain definitive knowledge. If it succeeds, you're funding the next wave of a proven architecture."
- For government grants: frame as AI governance/safety infrastructure research, not AGI moonshot.
- For philanthropic funders: frame as public-benefit AI institution building --- the antidote to OpenAI's profit pivot.

---

## Round 2: Cross-Critique and Refinement

### Visionary Responds to Critic

The Critic's $750K founding capital requirement is correct. This is the irreducible constraint. Everything else is sequencing.

But the Critic's contingency plan (reduce to 2 engineers, pivot to consulting) is a death spiral. Once you lose 4+ engineers with ZKP and distributed systems expertise, you cannot rehire them. The market for this talent is too competitive. The project would be de facto dead.

**Better contingency:** If grants don't arrive by Month 12, the team has 3 months of remaining runway (6-month buffer from founding capital). Use those 3 months to:
1. Publish W0 results as academic papers (instant credibility for grant applications)
2. Open-source W0 code (community building, visibility)
3. Apply to 2--3 additional grant programs with W0 evidence
4. Approach venture philanthropy (Open Philanthropy, Good Ventures) with concrete results

The key insight: **W0 results change the fundraising conversation entirely.** Pre-W0, you're selling a whitepaper. Post-W0, you're selling validated architecture with quantitative evidence.

### Systems Thinker Responds to Visionary

Agreed that the post-W0 fundraising pivot is critical. But I want to quantify the "AIC allocation" incentive more carefully.

**The AIC incentive only works if there's a credible path to convertibility.** C15 DA-01 defines the Conversion Reserve Fund (CRF) at $2M--$5M. But this CRF is funded from... the same founding capital and grants we're trying to raise for operations. You can't allocate $2M to a CRF when you need every dollar for payroll.

**Resolution:** The CRF is a Phase 1+ line item, not Phase 0. During Phase 0, AIC allocations are "paper value" with a contractual commitment that the CRF will be funded when resources allow. This is honest and transparent --- employees know the AIC upside is speculative at Phase 0.

For Phase 0 compensation, rely on:
- Competitive base salary (not discounted --- full market rate for a nonprofit)
- Signing bonus for specialists
- Milestone cash bonuses (W0 completion = $15K--$25K per engineer)
- AIC allocation as speculative upside (clearly communicated as such)

### Critic Responds to Both

The Visionary's W0-as-fundraising-pivot is the strongest idea in this round. Let me steel-man it:

**The W0 Funding Experiment Strategy:**
1. Raise $750K founding capital (Joshua + 1--2 co-founders/angels)
2. Run W0 (3 months, 4 engineers, $216K payroll + $19K cloud)
3. W0 produces: 4 experiment results with quantitative data, kill/advance decisions, open-source code, 1--2 academic papers
4. Use W0 results to raise W1--W2 funding ($3M--$5M) from grants and partnerships
5. Use W1--W2 results to raise W3--W5 funding ($4M--$7M) from institutional members and revenue

This is essentially the biotech pipeline model (Analogy 2) applied to AI infrastructure.

**The risk:** W0 takes 3 months. Grant applications take 6--12 months. Even with W0 results, the next funding arrives in Month 9--15. That's a 6--12 month gap. The $750K must cover Month 1--12 if grants are slow.

At 4 engineers: $72K/month x 12 = $864K. This exceeds $750K.

**Resolution:** Either raise $1M founding capital (stretch target) or start with 3 engineers for the first 6 months ($54K/month x 12 = $648K, within $750K).

---

## Round 3: Synthesis

### All Three Converge on "C18-A+ v1.0: Staged Portfolio Funding with W0 Pivot"

**Core Architecture:**

1. **Stage 0 (Pre-W0):** $750K--$1M founding capital. 3--4 engineers. 3 months.
   - Purpose: Validate architecture (C22 W0 experiments)
   - Deliverable: Quantitative experiment results, open-source code, academic paper(s)
   - Concurrent: Submit 3--5 grant applications (Horizon Europe, DARPA, NSF, Open Philanthropy)

2. **Stage 1 (Post-W0, W1--W2):** $2M--$4M from grants + strategic partnerships. 8--13 engineers. 10 months.
   - Triggered by: W0 advancement criteria met
   - Sources: EU Horizon Europe (EUR 3--4M), DARPA I2O ($1--3M), private foundations ($500K--$1M each)
   - Partnerships: Compute provider agreements (BRA per C15), academic co-development
   - Concurrent: Begin CRF funding ($500K--$1M), begin PBC service design

3. **Stage 2 (W3--W5):** $4M--$7M from institutional membership + revenue + renewal grants. 15--19 engineers. 14--23 months.
   - Sources: Institutional membership ($1M--$3M), task marketplace early revenue ($500K--$2M), renewal/expansion grants ($2M--$4M)
   - CRF fully funded ($2M--$5M per C15 DA-01)
   - AIC convertibility begins (Phase 1 per C15)

**Compensation Architecture:**

| Component | Phase 0 | Phase 1 | Phase 2 |
|-----------|---------|---------|---------|
| Base salary | Market rate ($180K--$250K) | Market rate + 5% COLA | Market rate + 10% |
| AIC allocation | 0.01--0.05% treasury, speculative | Same, CRF partially funded | Same, CRF operational |
| Phantom Value Rights | Granted, denominated in USD | Accruing value as ACI grows | Potentially payable |
| Wave milestone bonus | $15K--$25K | $15K--$25K | $15K--$25K |
| Signing bonus | $15K--$30K (specialists) | As needed | As needed |

**Pitch Portfolio:**

| Audience | Pitch Angle | Ask | Timing |
|----------|------------|-----|--------|
| Founding partners | Skin-in-the-game, founding team, AIC allocation | $250K--$500K each | Month 0 |
| EU Horizon Europe | AI governance infrastructure, verification systems, EEA entity | EUR 3--4M | Month 1--2 (submit) |
| DARPA I2O | Trustworthy AI, formal verification, distributed consensus | $1--3M | Month 1--3 (submit) |
| Open Philanthropy | AI safety institution building, alternative to profit-driven labs | $500K--$2M | Month 3 (post-W0 results) |
| Schmidt Futures | AI governance, public-benefit AI infrastructure | $500K--$1M | Month 3--6 |
| Compute providers | Early ecosystem partner, BRA agreement | $300K--$1M compute credits | Month 6--12 |
| Universities | Co-development, shared publication, student pipelines | In-kind (researcher time) | Month 6--18 |
| Institutional members | Advisory board, priority access, co-development rights | $100K--$250K/year | Month 18+ |

**Runway Management:**

- Minimum runway threshold: 6 months
- If runway < 6 months: hiring freeze
- If runway < 3 months: scope reduction to 2--3 core engineers + emergency fundraising
- Monthly financial reporting to Stiftung board
- Quarterly runway projection updates

---

## Selected Concept Output

```yaml
concept_id: C18-A+
version: "1.0"
title: "Staged Portfolio Funding with W0 Pivot"
description: >
  Three-stage funding architecture that sequences founding capital,
  mission-aligned grants, strategic partnerships, and institutional
  membership to fund a $8M-$12M, 27-36 month AI infrastructure
  implementation. Uses C22 W0 experiment results as the critical
  fundraising pivot point. Compensation combines competitive base
  salary with AIC treasury allocation, phantom value rights, and
  wave milestone bonuses to attract and retain elite engineering
  talent within nonprofit constraints.

funding_stages:
  stage_0:
    name: "Pre-W0 Validation"
    amount: "$750K-$1M"
    sources: ["founding_capital"]
    team: "3-4 engineers"
    duration: "3 months"
    deliverable: "W0 experiment results + grant applications"
  stage_1:
    name: "Post-W0 Foundation Building"
    amount: "$2M-$4M"
    sources: ["government_grants", "private_foundations", "strategic_partnerships"]
    team: "8-13 engineers"
    duration: "10 months"
    deliverable: "W1-W2 functional layers"
  stage_2:
    name: "Full Implementation"
    amount: "$4M-$7M"
    sources: ["institutional_membership", "task_marketplace_revenue", "renewal_grants", "partnerships"]
    team: "15-19 engineers"
    duration: "14-23 months"
    deliverable: "W3-W5 production system"

compensation_model:
  base_salary: "75th percentile nonprofit tech ($180K-$250K)"
  aic_allocation: "0.01-0.05% of 10B treasury, 3-year vest with 1-year cliff"
  phantom_value_rights: "Cash bonus tied to ACI growth, paid from PBC revenue"
  wave_milestone_bonus: "$15K-$25K per wave advancement"
  signing_bonus: "$15K-$30K for scarce specialists"

pitch_strategy:
  primary_angle: "Implementation-ready architecture with pre-registered kill criteria"
  key_differentiator: "13 specifications, 21,000 lines, 3 defense systems — most thoroughly designed AI infrastructure ever attempted"
  regulatory_frame: "AI governance and safety infrastructure research"
  mission_frame: "Public-benefit AI institution — the structural antidote to profit-driven AI development"

budget_summary:
  total_range: "$8M-$12M"
  personnel: "$5.4M-$8.4M (65-70%)"
  cloud_infrastructure: "$410K (4%)"
  conversion_reserve_fund: "$1M-$3M (15-20%)"
  operations_legal_admin: "$500K-$1M (8-10%)"
  contingency: "$500K-$1M (8-10%)"

key_risks:
  - "Grant timing gap (6-12 month application-to-disbursement)"
  - "ZKP/Rust specialist hiring in competitive market"
  - "AIC valuation circularity in early compensation"
  - "Regulatory classification of AIC employee allocations (IRC 409A)"
  - "W0 kill criterion triggered — requires graceful wind-down plan"

integrations:
  c14: "Legal entity structure (Stiftung/PBC/Purpose Trust)"
  c15: "AIC valuation (SWECV, CRF, reference rate), provider onboarding (BRA)"
  c22: "Implementation waves (W0-W5), team composition, cloud costs, kill criteria"
```
