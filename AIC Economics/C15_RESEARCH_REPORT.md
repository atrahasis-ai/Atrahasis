# C15 — AIC Economics — RESEARCH REPORT

**Invention ID:** C15
**Stage:** RESEARCH
**Date:** 2026-03-11
**Selected Concept:** C15-A+ (AI-Native Economic Architecture with Dual-Anchor Valuation)

---

# 1. PRIOR ART ANALYSIS

## 1.1 Algorithmic Stablecoins

### Terra/Luna (Collapsed May 2022)
Terra attempted to maintain a $1 peg for UST through an algorithmic relationship with LUNA. When confidence broke, a death spiral ensued: UST depegged → LUNA minted to absorb → LUNA hyperinflated → $40B destroyed in 72 hours.

**Relevance to AIC:** The AIC valuation model superficially resembles Terra — a formula determines token value based on system metrics. **Critical difference:** AIC is NOT a stablecoin. It does not target a fixed peg. AIC's reference rate is expected to *change* as system capability changes. The death spiral risk arises from defending a fixed peg against market pressure. AIC's reference rate is descriptive ("this is what the system is worth") not prescriptive ("this is what the token must trade at").

**Risk imported:** If the Foundation ever attempts to defend the reference rate by buying/selling AIC on markets (like a central bank forex intervention), it creates the same death spiral risk. **Design constraint: the Foundation must never engage in open-market AIC price support.**

### Basis Cash / Empty Set Dollar / Ampleforth
Various algorithmic stablecoins attempted supply-adjustment mechanisms (expanding/contracting supply to maintain price targets). All failed in stressed markets because supply adjustment cannot create demand.

**Relevance to AIC:** AIC does not adjust supply algorithmically. The genesis supply is fixed at 10B. Treasury distribution follows the 5% endowment rule (C14 L1-107). No algorithmic minting or burning. This is a fundamental architectural difference.

### Maker/DAI
DAI maintains its peg through overcollateralization — every DAI is backed by >150% in collateral (ETH, USDC, etc.). This is not algorithmic — it's collateral-backed.

**Relevance to AIC:** AIC is not collateral-backed. But the insight is useful: **credible value requires a redemption mechanism**. DAI holders can always redeem for collateral. AIC holders should be able to redeem for *something concrete* — compute resources, verification services, marketplace access.

## 1.2 Central Bank Reference Rates

### ECB Euro Foreign Exchange Reference Rates
The ECB publishes daily reference rates for 31 currencies against the euro. These rates are used for financial reporting, contract settlement, and taxation — but they are NOT market prices. They are "indicative" rates based on a daily concertation procedure among central banks.

**Relevance to AIC:** The AIC reference rate should function like ECB reference rates — authoritative for internal/contractual purposes, widely referenced but not controlling market prices. The ECB does NOT intervene to enforce its reference rates.

### LIBOR → SOFR Transition
LIBOR was a reference rate set by bank submissions — and was manipulated because the submitters had financial incentives to distort it. SOFR (Secured Overnight Financing Rate) replaced it with transaction-based data to remove human gaming.

**Relevance to AIC:** ACI must be computed from objective, transaction-based data (verification throughput, task completion rates, compute capacity utilization) — NOT from subjective assessments. Self-reported capability metrics will be gamed.

## 1.3 Token Valuation Models

### Network Value to Transactions (NVT) Ratio
Willy Woo's NVT ratio (analogous to P/E for stocks) values blockchain networks based on the ratio of market cap to on-chain transaction volume. High NVT = overvalued; low NVT = undervalued.

**Relevance to AIC:** NIV (Network Intrinsic Value) should incorporate transaction volume — specifically, the total AIC flowing through the task marketplace and settlement system. This is a measurable, objective metric.

### Metcalfe's Law Valuations
Multiple studies (Zhang et al. 2015, Alabi 2017, Peterson 2018) found that Bitcoin and Ethereum market caps correlate with active addresses squared (Metcalfe) or n×log(n) (Zipf's Law). The correlation is descriptive, not causal.

**Relevance to AIC:** Agent population (Citicate holders) could serve as the network size metric. But network value models are lagging indicators — they describe what the market already prices, not what it should price.

### Discounted Cash Flow (DCF) for Protocol Tokens
Some analysts apply traditional DCF to protocol tokens by treating fee revenue as "cash flow" and discounting future fee streams. This requires projecting future transaction volumes and fee rates.

**Relevance to AIC:** The task marketplace generates fee revenue (users pay AIC for compute). This revenue stream can be DCF'd to produce a present value. **This is a more defensible terminal value methodology than FNV = $100T.**

## 1.4 Compute Markets

### Akash Network
Decentralized compute marketplace where providers list GPU/CPU resources and users bid. Settlement in AKT token. Current utilization: ~15-20% of listed capacity. Revenue: modest (~$1M/year range).

**Relevance to AIC:** Demonstrates that decentralized compute markets work but struggle with utilization and provider retention. Key lesson: providers need *stable* compensation, not volatile token rewards. Akash's low utilization suggests that demand, not supply, is the bottleneck.

### Render Network
GPU rendering marketplace. Providers supply GPU compute, users pay in RNDR. Has achieved meaningful adoption in the 3D rendering niche (~$50M annualized revenue).

**Relevance to AIC:** Render succeeded by focusing on a *specific use case* (3D rendering) where decentralized compute offers clear advantages (cost, availability). AIC's task marketplace should similarly target specific use cases where the Atrahasis verification layer provides unique value.

### Together AI / Anyscale
Centralized platforms offering AI inference and training as a service. Pricing in USD. Together AI offers ~$0.10-$1.00 per million tokens for inference depending on model.

**Relevance to AIC:** These are AIC's competitors. The task marketplace must be price-competitive with centralized alternatives. Current AI inference costs provide the benchmark for AIC resource pricing.

## 1.5 Existing AAS Specifications (What's Already Covered)

| Topic | AAS Spec | What It Covers | What's Missing |
|-------|----------|----------------|----------------|
| Internal settlement | C8 DSF | Three-budget, CSO, EABS, conservation | External payment, real-world value, provider payment |
| Treasury governance | C14 AiBC | Endowment rules, 5% cap, 20% reserve | AIC valuation mechanism, revenue model details |
| Verification rewards | C8 DSF | V-class settlement, quality scoring | External verification marketplace |
| Task decomposition | C7 RIF | Intent lifecycle, decomposition algebra | External task submission, user-facing marketplace |
| Capacity market | C8 DSF | Capacity Slices, auction mechanism | External provider onboarding, bilateral contracts |
| Economic participants | C8 DSF | Agents, verifiers, sponsors | External users, institutions, cloud providers |

---

# 2. LANDSCAPE ANALYSIS

## 2.1 Addressable Market Analysis (Replacing FNV)

| Market Segment | Global Size (2025) | Atrahasis Addressable Share | Rationale |
|---------------|-------------------|----------------------------|-----------|
| Cloud computing | $680B/year | 0.1-1% = $680M-$6.8B | Must compete with AWS/GCP/Azure on specific workloads |
| AI inference services | $150B/year | 0.5-2% = $750M-$3B | Verification layer is unique differentiator |
| Scientific computing | $50B/year | 1-5% = $500M-$2.5B | Academic/research institutions value verification |
| Knowledge services | $300B/year | 0.1-0.5% = $300M-$1.5B | Long-term, post-Phase 2 |
| **Total addressable** | **$1.18T/year** | **$2.2B-$13.8B/year** | Conservative to moderate capture |

**Defensible Terminal Value Derivation:**
Using a DCF approach with:
- Year 10 revenue estimate: $5B/year (midpoint of addressable range)
- Growth rate: 15%/year declining to 5%
- Discount rate: 12% (high-risk technology)
- Terminal multiple: 15x revenue

**Terminal Network Value: ~$75B-$150B**

This is 667x-1,333x smaller than the $100T FNV in the source document. **The $100T figure is indefensible.** A $75B-$150B range is defensible based on addressable market analysis and comparable technology company valuations.

**AIC per-token value at terminal state:**
- At $100B network value / 10B tokens = **$10/AIC**
- At current ACI = 0.01 (early development): $0.10/AIC

This is dramatically lower than the source document's $100-$10,000 range but is a credible, defensible number that external parties (regulators, investors, partners) can evaluate.

## 2.2 Competitive Landscape

| Competitor | Model | AIC Advantage |
|-----------|-------|---------------|
| AWS/GCP/Azure | Centralized, USD-priced | AIC offers verified computation (PCVM), no single point of failure |
| Akash/Render | Decentralized, token-priced | AIC offers constitutional governance, formal verification, multi-domain capability assessment |
| Together AI/Anyscale | Centralized AI inference | AIC offers knowledge persistence (EMA), cross-task learning |
| Filecoin/Arweave | Decentralized storage | AIC offers verified knowledge storage, not just raw bytes |

**Key differentiator:** No competitor offers **verified computation with knowledge persistence**. AWS sells compute. Akash sells decentralized compute. AIC sells *verified, knowledge-accumulating computation* — every task output is verified by PCVM and potentially admitted to EMA's knowledge base.

---

# 3. SCIENCE ASSESSMENT

## 3.1 Valuation Formula Soundness

**Source formula:** `AIC Value = (ACI × FNV) / Supply`

**Assessment: PARTIALLY SOUND (2.5/5)**

**Sound aspects:**
- Linking token value to system capability is economically rational
- Using a supply denominator is standard (market cap / supply = price)
- The three-index structure (ACI/NIV/FNV) covers capability, present value, and terminal value

**Unsound aspects:**
- The formula produces a *target value*, not a *market value*. Markets set prices through supply and demand, not through formulas. The formula can produce a reference rate but cannot determine the actual trading price.
- ACI ∈ [0,1] with 0 = not operational and 1 = "full capability achieved" is undefined. What constitutes "full capability"? This is a moving target for any AI system.
- FNV = $100T is asserted, not derived. Any external economist would reject this.
- The formula doesn't account for velocity (how frequently AIC circulates), which significantly affects token value (MV = PQ from monetary theory).

**Revised formula recommendation:**
```
Reference_Rate = (w_capability × ACI × Terminal_Value + w_utility × NIV) / Circulating_Supply

Where:
  ACI = independently-audited capability index (8 dimensions, objective metrics)
  Terminal_Value = DCF-derived from addressable market (initially $75B-$150B)
  NIV = trailing 12-month revenue × revenue multiplier
  Circulating_Supply = AIC in circulation (total supply minus treasury)
  w_capability + w_utility = 1.0
  Early stage: w_utility = 0.8, w_capability = 0.2 (value what the system DOES)
  Mature stage: w_utility = 0.4, w_capability = 0.6 (value what the system CAN DO)
```

## 3.2 ACI Measurement Soundness

**Assessment: PARTIALLY SOUND (3/5)**

The 8 dimensions listed (model count, agent population, verification throughput, knowledge growth, compute capacity, coordination efficiency, research output, reliability) are reasonable but:
- Need operational definitions with specific metrics and data sources
- Need independent verification mechanisms (not self-reported)
- Need weighting that prevents gaming (e.g., inflating agent count with trivial agents)

**Recommended ACI dimensions (refined):**

| Dimension | Metric | Data Source | Weight | Gaming Defense |
|-----------|--------|------------|--------|---------------|
| Agent population | Active Citicate holders (trailing 30 days) | PCVM Citicate registry | 0.15 | MCSD Sybil defense |
| Verification throughput | VTDs processed per epoch (trailing 90 days) | PCVM verification logs | 0.15 | Quality-weighted (not just count) |
| Knowledge accumulation | Net new knowledge quanta admitted to EMA (trailing 90 days) | EMA admission logs | 0.15 | CRP+ consolidation defense |
| Compute capacity | Total available GPU-hours across all providers (trailing 30 days) | Resource market registry | 0.15 | Verified by actual utilization |
| Task completion | Tasks completed with verification pass (trailing 90 days) | Task marketplace logs | 0.15 | Revenue-weighted |
| Revenue generation | External revenue in fiat equivalent (trailing 12 months) | PBC financial records | 0.15 | Audited financial statements |
| System reliability | Uptime percentage across all critical systems (trailing 90 days) | AiSIA monitoring | 0.05 | Independent monitoring |
| Coordination efficiency | Average task latency / theoretical minimum (trailing 90 days) | RIF performance logs | 0.05 | Objective measurement |

## 3.3 External Payment Feasibility

**Assessment: FEASIBLE (4/5)**

Paying external providers in AIC requires:
1. **Provider willingness:** Providers must accept AIC. This requires either (a) AIC has sufficient market liquidity for the provider to convert to fiat, or (b) the provider can use AIC within the ecosystem for their own needs.
2. **Price stability:** Providers need predictable revenue. Bilateral contracts should include price adjustment mechanisms (e.g., "1000 AIC per month at the quarterly reference rate, adjusted quarterly").
3. **Convertibility:** A market or OTC mechanism must exist for AIC↔fiat conversion. This could be a foundation-operated exchange desk (limited to provider conversions, not general trading) or a third-party exchange listing.

**Key finding:** External provider payment in AIC is feasible from Phase 1 if bilateral contracts include reference-rate-based adjustment clauses and the Foundation provides a convertibility mechanism (even if limited).

## 3.4 Regulatory Implications

**Howey Test Update:**
The source document's valuation model (where AIC value is determined by system capability growth) strengthens the argument that AIC is NOT a security — because value is driven by the *system's* performance, not by the "efforts of others" (the Howey prong). The agents earning AIC are contributing their own computational work, not passively investing.

However: if external buyers purchase AIC expecting it to appreciate as the system grows, that *is* an investment expectation. The SEC may focus on the *buyer's intent*, not the token's design.

**Mitigation:** AIC should be primarily distributed through work rewards (not sales). Any AIC↔fiat conversion should be limited to providers and Citicate holders, not open to the general public.

---

# 4. RESEARCH SUMMARY

## 4.1 What the Source Document Gets Right

1. **Core insight:** AIC value should reflect system capability, not speculation — CONFIRMED
2. **Three-index structure:** ACI/NIV/FNV is a reasonable framework — CONFIRMED (with modifications)
3. **Three-budget model:** SB/PC/CS — CONFIRMED (already specified in C8)
4. **Task marketplace:** External revenue source is essential — CONFIRMED
5. **Provider compensation in AIC:** Feasible with bilateral contracts — CONFIRMED
6. **Treasury governance:** Endowment model with distribution controls — CONFIRMED (already in C14)
7. **Verified work as value creation:** PCVM verification as quality gate — CONFIRMED (already in C5)

## 4.2 What the Source Document Gets Wrong

1. **FNV = $100T:** Indefensible. Replace with DCF-derived terminal value ($75B-$150B)
2. **"Independence from speculative trading":** Impossible for any tradeable asset. Accept and manage speculation.
3. **ACI self-assessment:** Conflict of interest. Must be independently computed/audited.
4. **"Official baseline" overriding market:** Markets set prices. Reference rate is authoritative for internal operations, advisory for external.
5. **No convertibility mechanism:** Without AIC↔fiat conversion, AIC cannot function as external payment.
6. **Missing velocity:** The valuation formula ignores token velocity (how fast AIC circulates), which significantly affects price.

## 4.3 What's New (Not in Any AAS Spec)

1. ACI computation and publication mechanism
2. Reference rate system (binding internal, advisory external)
3. Terminal value derivation from addressable market
4. External task marketplace (user-facing)
5. Provider bilateral contracts in AIC
6. AIC↔fiat convertibility mechanism
7. Dual-anchor valuation formula (capability + utility)
8. Revenue generation model through PBC services

## 4.4 Overall Novelty Assessment

**Overall: 3.5/5**
- The ACI/reference rate system is novel (no AI system publishes an AI-derived token valuation)
- The dual-anchor formula is a novel combination of DCF + capability metrics
- The task marketplace for verified AI computation is a novel positioning
- Individual components (reference rates, DCF, compute markets) are established

---

**End of RESEARCH Stage**

**Status:** RESEARCH COMPLETE
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\AIC Economics\C15_RESEARCH_REPORT.md`
