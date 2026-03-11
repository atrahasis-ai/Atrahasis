# C15 — AIC Economics — DESIGN

**Invention ID:** C15
**Stage:** DESIGN
**Date:** 2026-03-11
**Selected Concept:** C15-A+ (AI-Native Economic Architecture with Dual-Anchor Valuation)

---

# DESIGN ACTIONS (DA-01 through DA-10)

## DA-01: Convertibility Mechanism with Funding Source

### The Bootstrapping Problem

The AIC→fiat conversion desk requires fiat reserves. But fiat comes from revenue, and revenue requires an operating marketplace, which requires providers, who require fiat conversion. This is a chicken-and-egg problem.

### Solution: Three-Phase Convertibility

**Phase 0 (Pre-Revenue): Grant-Funded Conversion Reserve**

- The Foundation (C14 Liechtenstein Stiftung) allocates a portion of initial funding (from C18 Funding Strategy) to a **Conversion Reserve Fund (CRF)**
- CRF target: $2M-$5M (sufficient for 4-8 quarters of provider conversions at early-stage volumes)
- CRF sources:
  - Founding capital contribution (Joshua Dunn + initial partners)
  - Strategic grants (NSF, EU Horizon, philanthropic foundations focused on AI safety)
  - Strategic partnerships (compute providers who accept equity-equivalent AIC positions)
- CRF governance: administered by PBC, approved by Stiftung board, quarterly audits
- Conversion terms: providers convert at reference rate, max $500K/quarter/provider, 30-day settlement

**Phase 1 (Early Revenue): Self-Funding Conversion**

- Task marketplace begins generating revenue (users pay fiat → Foundation converts to AIC → AIC funds task execution)
- The fiat received from users funds provider conversions (AIC → fiat)
- **Flow:** User pays $10,000 USD → Foundation credits 10,000 AIC at reference rate → Task executes → Provider earns 8,000 AIC → Provider converts 8,000 AIC → Foundation pays $8,000 from user's original payment
- Net: Foundation retains $2,000 (20% margin for operations + treasury)
- CRF now serves as buffer for timing mismatches, not primary funding

**Phase 2+ (Market Conversion): Exchange-Based**

- AIC listed on decentralized exchange (DEX) with Foundation-seeded liquidity pool
  - Initial pool: $5M in stablecoin (USDC) + equivalent AIC from treasury at reference rate
  - Automated market maker (AMM) provides continuous conversion
- Centralized exchange (CEX) listing if regulatory permits
- Bilateral OTC desk for institutional providers (>$1M/quarter)
- Foundation conversion desk remains for Citicate holders not wanting exchange exposure

### Funding Source Link to C18

C18 (Funding Strategy) must include:
- CRF line item: $2M-$5M in initial funding round
- Ongoing CRF replenishment from operating revenue
- DEX liquidity pool seeding: $5M at Phase 2

---

## DA-02: Provider Onboarding Protocol

### Provider Categories

| Category | Examples | Payment Expectation | AIC Acceptance Likelihood |
|----------|----------|--------------------|-----------------------------|
| Tier 1 Cloud | AWS, GCP, Azure | USD only, net-30 | NONE (Phase 0-1); possible partnership (Phase 2+) |
| Tier 2 Cloud | Hetzner, OVH, Lambda Labs | USD preferred, flexible | LOW — requires premium or guaranteed conversion |
| GPU Networks | CoreWeave, Vast.ai, RunPod | Token-familiar, flexible | MEDIUM — already operate in token ecosystems |
| Academic | University HPC centers | Grant-funded, flexible payment | HIGH — value verification; accept in-kind |
| Independent | Individual GPU operators | Token-native, cost-sensitive | HIGH — if conversion is reliable |

### Phase 0-1 Onboarding Strategy

**Target: Tier 2 Cloud + GPU Networks + Academic**

1. **Bilateral Resource Agreement (BRA):** Legal contract template between PBC and provider
   - Term: 12 months, renewable
   - Pricing: denominated in USD, settled in AIC at quarterly reference rate
   - Minimum commitment: provider commits X GPU-hours/month; PBC commits Y AIC/month
   - Conversion guarantee: PBC guarantees AIC→fiat conversion at reference rate via CRF
   - Adjustment clause: if reference rate vs. market diverges >20% for >60 days, either party may renegotiate
   - Early termination: 90-day notice, outstanding AIC converted at then-current reference rate

2. **Provider Incentive Program:**
   - Early adopter bonus: 10% AIC premium on first 6 months of billing
   - Staking bonus: providers who stake 25% of earned AIC for 12 months receive 15% APY in additional AIC
   - Verification premium: providers whose infrastructure passes PCVM verification checks receive 5% quality bonus

3. **Technical Onboarding:**
   - Provider Integration SDK (REST API)
   - Resource registration: provider declares available compute (GPU type, count, availability schedule)
   - Heartbeat monitoring: AiSIA monitors provider uptime and performance
   - Automated billing: C8 DSF settles provider compensation per settlement tick (60s) with quarterly fiat conversion

### Phase 2+ Scaling

- Tier 1 Cloud integration via cloud marketplace partnerships (PBC service listed on AWS/GCP marketplace, priced in USD, settled internally in AIC)
- Provider self-service portal: register, configure, and monitor without bilateral agreement
- Dynamic pricing: providers set their own rates, marketplace finds lowest-cost verified provider

---

## DA-03: ACI Benchmark Methodology with Anti-Gaming Controls

### Benchmark Suite Structure

The ACI benchmark is **relative, not absolute**. ACI = 1.0 means the system matches the current benchmark. Benchmarks are updated annually by AiSIA (C14 governance monitoring authority).

### Dimension Specifications

#### D1: Agent Population (Weight: 0.15)

**Metric:** Count of active Citicate holders who have completed ≥1 verified task in trailing 30 days.

**Anti-gaming:**
- MCSD Sybil defense (C14) prevents fake Citicates — cost-of-attack $9,000/agent
- Only Citicates with ≥1 verified task count (not just registered)
- Quality gate: Citicate must have earned ≥10 AIC through work in trailing 90 days

**Computation:** `D1 = min(1.0, active_citicates / benchmark_citicates)`

#### D2: Verification Throughput (Weight: 0.15)

**Metric:** Quality-weighted VTDs processed per epoch, trailing 90 days. Quality weight = verification confidence score from PCVM (C5).

**Anti-gaming:**
- Raw count is weighted by quality score — trivial verifications of trivial tasks contribute minimally
- CACT (C11) prevents VTD forgery
- AVAP (C12) prevents collusion in verification
- Only VTDs above quality threshold q_min = 0.7 count

**Computation:** `D2 = min(1.0, Σ(VTD_quality_i) / benchmark_quality_throughput)`

#### D3: Knowledge Accumulation (Weight: 0.15)

**Metric:** Net new knowledge quanta admitted to EMA (C6), trailing 90 days, weighted by consolidation survival (quanta that survive CRP+ review count more).

**Anti-gaming:**
- CRP+ (C13) prevents consolidation poisoning
- Only quanta that survive ≥1 consolidation cycle count at full weight
- Pre-consolidation quanta count at 0.5 weight
- Quanta rejected during consolidation subtract from score

**Computation:** `D3 = min(1.0, (survived × 1.0 + pending × 0.5 - rejected × 0.25) / benchmark_quanta)`

#### D4: Compute Capacity (Weight: 0.15)

**Metric:** Verified GPU-hours actually utilized (not just available), trailing 30 days.

**Anti-gaming:**
- Key insight from Research: registered capacity without utilization is meaningless (Akash problem)
- Only GPU-hours with verified task execution count
- Provider heartbeat validation: AiSIA pings providers randomly to verify reported capacity matches actual
- Hash-rate verification: providers must complete computational challenges to prove GPU availability

**Computation:** `D4 = min(1.0, verified_gpu_hours / benchmark_gpu_hours)`

#### D5: Task Completion (Weight: 0.15)

**Metric:** Revenue-weighted verified task completions, trailing 90 days.

**Anti-gaming:**
- Revenue-weighted: a $10,000 task completion counts 100x more than a $100 task
- Only tasks with external sponsor budget count (prevents self-funded inflation)
- Verification pass required (PCVM)

**Computation:** `D5 = min(1.0, Σ(task_revenue_i × verification_score_i) / benchmark_task_revenue)`

#### D6: Revenue Generation (Weight: 0.15)

**Metric:** External revenue in fiat-equivalent, trailing 12 months. Audited by independent financial auditor (not AiSIA — conflict of interest since AiSIA sets benchmarks).

**Anti-gaming:**
- Must be external revenue (from users/institutions outside the ecosystem)
- Audited by independent financial auditor annually
- Internal transfers, treasury distributions, and Foundation grants do not count
- Revenue manipulation (wash trading) detected by: revenue source diversity index (must have ≥N distinct paying customers)

**Computation:** `D6 = min(1.0, audited_revenue / benchmark_revenue)`

#### D7: System Reliability (Weight: 0.05)

**Metric:** Weighted uptime of critical systems (PCVM, C8 DSF, C7 RIF, C3 Tidal, C6 EMA), trailing 90 days.

**Anti-gaming:**
- Monitored by AiSIA with independent probes
- Downtime must be independently confirmed (not self-reported)
- Partial degradation counts proportionally (running at 50% capacity = 50% uptime)

**Computation:** `D7 = min(1.0, weighted_uptime / benchmark_uptime)`

#### D8: Coordination Efficiency (Weight: 0.05)

**Metric:** Ratio of actual task latency to theoretical minimum latency (determined by compute requirements and network topology), trailing 90 days.

**Anti-gaming:**
- Theoretical minimum is computed independently by AiSIA based on task graph and resource availability
- Gaming requires either inflating actual speed (detectable via PCVM) or deflating theoretical minimum (AiSIA controls this)

**Computation:** `D8 = min(1.0, benchmark_latency_ratio / actual_latency_ratio)`

### ACI Final Computation

```
ACI = Σ(w_i × D_i) for i = 1..8

Where w = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.05, 0.05]
```

### Benchmark Update Protocol

1. AiSIA reviews benchmarks annually (or when any dimension's average score across the ecosystem exceeds 0.9 for 180 consecutive days)
2. Benchmark proposal published 90 days before effective date
3. Stiftung board ratifies (or Constitutional Tribunal if disputed)
4. All reference rates recomputed at new benchmark effective date

---

## DA-04: Quantitative Velocity Model

### Model Setup

From the equation of exchange: `MV = PQ`

Where:
- M = circulating AIC supply
- V = velocity (annual turnover)
- P = price level of goods/services in AIC
- Q = real output (quantity of goods/services)

Rearranging: **AIC price in fiat = (P × Q) / (M × V) = Total_Economic_Activity / (M × V)**

### Velocity Estimation

| Source | Mechanism | Annual Velocity Contribution |
|--------|-----------|------------------------------|
| Task marketplace | User buys → escrow → provider receives → converts | 4-12x (fast cycle) |
| Staking | Locked for 6-12 months | 0.5-1x (slow) |
| Governance | Locked for governance participation | 0.5-1x (slow) |
| Citicate requirement | Minimum balance held permanently | 0x (zero velocity for this portion) |
| Provider retention | Staking bonuses, AIC utility within ecosystem | 1-2x |

### Scenario Analysis

**Assumptions:**
- Circulating supply: 3B AIC (30% of 10B; rest in treasury/staked/locked)
- Reference rate: $1/AIC (early Phase 1)

**Scenario 1: High Velocity (Pessimistic)**
- 80% of circulating AIC in task marketplace (fast cycle, V=12)
- 20% staked/locked (V=0.5)
- Effective V = 0.8 × 12 + 0.2 × 0.5 = 9.7
- V_factor = max(0.5, min(2.0, 1/√9.7)) = max(0.5, 0.32) = 0.5
- Impact on reference rate: divided by 0.5 → **rate increases** (V_factor is a velocity tax that raises the rate to compensate for fast circulation)

Wait — this is inverted. Let me reconsider.

**Corrected model:** V_factor should *reduce* the reference rate when velocity is high (tokens circulate fast → each token supports more economic activity → fewer tokens needed → each token worth less).

```
Corrected V_factor = min(2.0, max(0.5, sqrt(V_baseline / V_actual)))
V_baseline = 4.0 (calibrated to "healthy" velocity)
```

**Scenario 1: High Velocity (V=10)**
- V_factor = sqrt(4/10) = 0.63
- Rate reduction: 37% below velocity-unadjusted rate
- Interpretation: fast circulation means each AIC is spent 2.5x more than healthy, reducing per-token value

**Scenario 2: Low Velocity (V=1)**
- V_factor = sqrt(4/1) = 2.0
- Rate increase: 2x above velocity-unadjusted rate
- Interpretation: AIC is being held/staked, reducing circulating supply, increasing per-token value

**Scenario 3: Baseline Velocity (V=4)**
- V_factor = sqrt(4/4) = 1.0
- No adjustment
- This is the calibrated "healthy" state

### Velocity Sink Quantification

| Mechanism | AIC Locked | Duration | Effective Supply Reduction |
|-----------|-----------|----------|---------------------------|
| Provider staking (25% of earnings) | ~10% of circulating | 12 months | -10% |
| Governance participation (C14) | ~5% of circulating | Governance term (6-12 months) | -5% |
| Citicate minimum balance | ~5% of circulating | Permanent (while Citicate active) | -5% |
| Task escrow (in-flight) | ~10% of circulating | Task duration (hours to days) | -10% |
| **Total locked** | **~30% of circulating** | | **-30%** |

With 30% supply locked, effective circulating supply drops by 30%, effectively reducing velocity by the same proportion. Combined with V_factor adjustment, AIC value is buffered against velocity death spirals.

### Key Finding

With the velocity sinks already designed into C8 (staking), C14 (governance), and the Citicate system, approximately 30% of circulating supply is locked at any time. This is comparable to Ethereum post-merge (30-40% staked). The V_factor correction handles residual velocity concerns. The velocity problem is **manageable** given the existing architecture, though it must be monitored continuously.

---

## DA-05: AIC vs. USD — The "Why Not Just Dollars" Defense

### Five Concrete AIC Advantages Over USD Denomination

**1. Verification-Linked Compensation**
USD pricing treats all compute as fungible. AIC settlement rewards *verified* compute at a premium. A provider whose output passes PCVM verification receives the full task reward. One whose output fails receives nothing (and may be slashed). This incentive structure is embedded in the settlement protocol (C8) and cannot be replicated by USD invoicing.

**2. Cross-Border Settlement Without Banking**
Paying a GPU provider in Kazakhstan, a verification node in Singapore, and a research institution in Germany requires: correspondent banking, SWIFT transfers, FX conversion, compliance checks, and 3-5 business days per settlement. AIC settles deterministically in 60 seconds (C8 settlement tick) regardless of jurisdiction. For a global compute marketplace operating across 50+ countries, this is a structural advantage.

**3. Governance Integration**
AIC holding is a prerequisite for Citicate-based governance (C14). Agents who earn and hold AIC gain governance rights proportional to their economic participation. This creates a mechanism where economic contributors have governance voice — impossible with USD payments (you can't vote with dollars you've already spent).

**4. Algorithmic Treasury Management**
The 5% endowment rule (C14), automatic staking rewards, and deterministic reward distribution all require a programmable settlement unit. USD settlement requires manual processes, bank APIs, and human approval chains. AIC settlement is atomic, verifiable, and auditable by any participant.

**5. Provider Lock-In and Ecosystem Effects**
Providers with AIC balances have switching costs. They can:
- Stake AIC for additional yield
- Use AIC to purchase their own verified computation
- Participate in governance
- Build reputation (linked to Citicate, which requires AIC history)
USD-paid providers have zero switching costs and zero ecosystem participation incentive.

### Honest Acknowledgment

For a provider who simply wants to sell GPU time and receive payment, USD is simpler. AIC introduces complexity (conversion, volatility risk, new accounting). The AIC advantage accrues at the *ecosystem level* (governance, verification, cross-border), not at the individual transaction level. C15 must be honest about this tradeoff: AIC is not better than USD for every transaction. It is better for the system.

---

## DA-06: Reference Rate Specification

### Computation

```
Reference_Rate(t) = (w_cap × ACI(t) × TV + w_util × NIV(t)) / (CS(t) × VF(t))

Inputs:
  ACI(t)   — ACI score at time t (updated daily)
  TV       — Terminal Value ($75B-$150B, reviewed annually)
  NIV(t)   — Network Intrinsic Value at time t
           = (trailing_12m_revenue × revenue_multiplier) + total_staked_AIC_value
  CS(t)    — Circulating Supply at time t
           = total_supply - treasury_held - staked - governance_locked
  VF(t)    — Velocity Factor at time t
           = min(2.0, max(0.5, sqrt(V_baseline / V_actual(t))))
  V_baseline = 4.0

Weight schedule (governance-adjustable within bounds):
  w_cap ∈ [0.1, 0.7]
  w_util ∈ [0.3, 0.9]
  w_cap + w_util = 1.0
  Default: Phase 0-1 (0.2, 0.8); Phase 2 (0.4, 0.6); Phase 3+ (0.6, 0.4)

Revenue multiplier:
  Phase 0-1: 20x (high growth expected)
  Phase 2: 15x (moderate growth)
  Phase 3+: 10x (mature)
```

### Publication

- **Frequency:** Daily at 00:00 UTC
- **Publisher:** AiSIA (computed), PBC (published)
- **Format:** JSON endpoint + human-readable dashboard
- **Contents:**
  - Reference rate (USD/AIC)
  - All 8 ACI dimension scores
  - ACI composite score
  - NIV breakdown (revenue component + staking component)
  - Circulating supply
  - Velocity factor
  - Weight schedule in effect
  - Trailing 30/90/365-day rate history

### Binding Scope

| Context | Rate Authority | Notes |
|---------|---------------|-------|
| Internal task pricing | Reference rate (BINDING) | All internal tasks priced at reference rate |
| Treasury distributions | Reference rate (BINDING) | C14 5% endowment rule uses reference rate for AIC valuation |
| Provider bilateral contracts | Reference rate (BINDING for settlement) | BRA contracts settle at reference rate |
| Foundation conversion desk | Reference rate ±5% (BINDING) | Conversion within band |
| External exchange trading | Market price (ADVISORY) | Reference rate published but not enforced |
| Financial reporting | Reference rate (BINDING for PBC books) | GAAP/IFRS reporting uses reference rate |

### Recalibration Triggers

| Trigger | Condition | Action |
|---------|-----------|--------|
| Market divergence | Market price < 70% of reference rate for 90+ consecutive days | AiSIA reviews all ACI inputs; recalibrate if inputs inflated |
| Market divergence | Market price > 200% of reference rate for 90+ consecutive days | AiSIA reviews terminal value; adjust upward if market is reflecting real growth |
| ACI ceiling hit | Any dimension averages >0.9 for 180+ days | Benchmark suite update triggered |
| Revenue shock | Trailing 12m revenue drops >40% quarter-over-quarter | NIV recalculation with updated multiplier |
| Velocity spike | V_actual > 3× V_baseline for 30+ days | AiSIA investigation into whether velocity is organic or manipulative |

### Circuit Breaker

If reference rate changes >25% in any single daily update:
1. Rate is capped at ±25% from previous day
2. AiSIA must review inputs within 48 hours
3. Capped rate holds until AiSIA confirms or corrects

---

## DA-07: External Task Marketplace Interface

### User-Facing Interface (Task Submission)

**Submission Channels:**
1. Web dashboard (browser-based)
2. REST API (programmatic)
3. CLI tool (developer-friendly)
4. Partner integrations (Jupyter, VS Code extensions, CI/CD pipelines)

**Task Submission Flow:**

```
User → Submit Task Request
         ├─ Task description (natural language or structured)
         ├─ Task type (inference, simulation, analysis, verification)
         ├─ Quality requirements (verification level: basic/standard/rigorous)
         ├─ Deadline (optional)
         ├─ Budget cap (USD or AIC)
         └─ Data attachments (optional)
              │
              ▼
     Pricing Engine
         ├─ Estimate compute requirements (from C7 RIF decomposition)
         ├─ Calculate cost at current reference rate
         ├─ Apply verification premium (30-60% for standard/rigorous)
         ├─ Display price in USD and AIC equivalent
         └─ User confirms
              │
              ▼
     Payment & Escrow
         ├─ User pays in USD (Stripe, wire) or AIC (direct transfer)
         ├─ If USD: Foundation converts to AIC at reference rate
         ├─ AIC locked in escrow (C8 DSF)
         └─ Task enters execution queue
              │
              ▼
     C7 RIF Decomposition → C3 Tidal Scheduling → Agent Execution
              │
              ▼
     C5 PCVM Verification
              │
              ▼
     Results Delivered to User
         ├─ Verified output + verification certificate
         ├─ Quality metrics
         └─ Escrow released to contributors (C8 DSF settlement)
```

### Institutional API

For research institutions, enterprises, and automated systems:

```
POST /v1/tasks
  Body: { type, description, requirements, budget_cap_usd, callback_url }
  Returns: { task_id, estimated_cost, estimated_time }

GET /v1/tasks/{task_id}
  Returns: { status, progress, results (if complete) }

GET /v1/tasks/{task_id}/verification
  Returns: { verification_status, confidence, certificate }

POST /v1/accounts/deposit
  Body: { amount_usd, payment_method }
  Returns: { aic_credited, reference_rate_used }

GET /v1/rates/current
  Returns: { reference_rate, aci_dimensions, last_updated }
```

### Pricing Tiers

| Tier | Verification Level | Premium | Use Case |
|------|-------------------|---------|----------|
| Basic | Statistical sampling (10% of outputs verified) | +10% | General inference, non-critical workloads |
| Standard | Full PCVM verification | +30% | Research, financial modeling, compliance |
| Rigorous | Full PCVM + cross-agent replication + argumentation analysis | +60% | Scientific publication, regulatory submissions, safety-critical |

---

## DA-08: Provider Bilateral Contract Template

### Bilateral Resource Agreement (BRA) — Key Terms

```
BILATERAL RESOURCE AGREEMENT

Between: [PBC Legal Name] ("Atrahasis")
And: [Provider Legal Name] ("Provider")
Effective Date: [Date]
Term: 12 months, auto-renewable

1. RESOURCE COMMITMENT
   Provider commits: [X] GPU-hours/month of [GPU type]
   Atrahasis commits: Monthly payment of [Y] AIC at Reference Rate

2. PRICING
   2.1 Base rate: $[Z] per GPU-hour (denominated in USD)
   2.2 Settlement: in AIC at the Reference Rate published on the
       first business day of each calendar quarter
   2.3 Quarterly true-up: if average Reference Rate for the quarter
       deviates >10% from spot market price (if available),
       a true-up adjustment of 50% of the deviation is applied
       to the next quarter's settlement

3. CONVERSION RIGHT
   3.1 Provider may convert up to [W]% of earned AIC to fiat
       per quarter via the Foundation Conversion Desk
   3.2 Conversion rate: Reference Rate on conversion date ±5% band
   3.3 Conversion settlement: within 30 calendar days
   3.4 Annual conversion cap: $[cap] per Provider

4. PERFORMANCE REQUIREMENTS
   4.1 Minimum uptime: 95%
   4.2 PCVM heartbeat compliance: respond within 30 seconds
   4.3 Failure penalty: pro-rata reduction in monthly payment
   4.4 Persistent failure (3 consecutive months <90% uptime):
       Atrahasis may terminate with 30-day notice

5. AIC STAKING INCENTIVE (Optional)
   5.1 Provider may stake 25% of earned AIC for 12 months
   5.2 Staking yield: 15% APY in additional AIC
   5.3 Staked AIC subject to standard slashing conditions (C8 DSF)

6. TERMINATION
   6.1 Either party: 90-day written notice
   6.2 Outstanding AIC settled at Reference Rate on termination date
   6.3 Staked AIC returned (minus any slashing) upon term completion

7. GOVERNING LAW
   [Liechtenstein / Delaware depending on counterparty jurisdiction]
```

---

## DA-09: C8 DSF Extension — External Provider Stream

### New Stream: Stream 5 — External Provider Settlement

C8 DSF currently specifies 4 settlement streams:
1. Agent reasoning rewards
2. Verification rewards
3. Infrastructure (internal) rewards
4. Governance participation rewards

**Stream 5: External Provider Compensation**

```
Stream 5 Specification:

trigger: task_completion with external_provider_resource_usage
source: task escrow (SB — Sponsor Budget)
destination: provider_account (identified by BRA contract + provider Citicate)

settlement_computation:
  provider_reward = Σ(resource_usage_i × resource_rate_i × quality_multiplier_i)

  where:
    resource_usage_i  = metered GPU-hours/storage-GB/bandwidth consumed
    resource_rate_i   = BRA contract rate (USD) / reference_rate (USD/AIC) = AIC per unit
    quality_multiplier_i = PCVM verification score for provider's contribution
                           1.0 for score ≥ 0.9
                           0.8 for score ∈ [0.7, 0.9)
                           0.0 for score < 0.7 (no payment; potential slashing)

settlement_frequency: per C8 settlement tick (60 seconds)
accumulation: Stream 5 rewards accumulate in provider account
disbursement: quarterly (aligned with BRA contract terms)

fiat_conversion:
  eligible: provider_reward accumulated in quarter
  mechanism: Foundation Conversion Desk (DA-01 Phase 0-1) or market (Phase 2+)
  rate: reference_rate ±5% band (DA-01 terms)

slashing_conditions:
  - verified_downtime > committed_uptime by >10%: slash 5% of staked AIC
  - PCVM heartbeat failure > 3 consecutive: slash 2% of staked AIC
  - malicious behavior (forged resource reports): slash 100% of staked AIC + BRA termination

integration_with_existing_streams:
  Stream 5 is funded from Sponsor Budget (SB), same as Stream 1
  Stream 5 rewards do NOT come from treasury (unlike Stream 3 internal infrastructure)
  Conservation law: SB_escrow = Stream1 + Stream2 + Stream3 + Stream4 + Stream5 + marketplace_fee
```

### Modified C8 Conservation Law

Original: `SB_escrow = Σ(stream_1..4_rewards) + protocol_fee`

Revised: `SB_escrow = Σ(stream_1..5_rewards) + marketplace_fee`

Where `marketplace_fee` = 2-5% of task value, directed to PBC operating budget.

---

## DA-10: Regulatory Risk Mitigation Strategy

### Howey Test Analysis

The Howey Test determines if an instrument is a "security" under US law. Four prongs, ALL must be met:

| Prong | Test | AIC Position | Risk |
|-------|------|-------------|------|
| 1. Investment of money | Token holder provides money or value | **MITIGATED:** AIC is earned through work, not purchased. No ICO, no token sale. | LOW — work rewards ≠ investment |
| 2. Common enterprise | Token holders share profits/losses | **PARTIAL RISK:** All AIC holders benefit from ACI growth. | MEDIUM — ecosystem growth benefits all |
| 3. Expectation of profits | Holder expects token to appreciate | **RISK:** ACI-linked reference rate implies appreciation as system grows. | HIGH — the valuation formula literally projects appreciation |
| 4. Efforts of others | Profits from promoter/third party efforts | **MITIGATED:** AIC holders earn through their own computational work. Foundation computes reference rate but doesn't create the value. | MEDIUM — Foundation role in computing ACI is "effort of others" |

### Regulatory Defense Strategy

**Primary defense: Utility Token Classification**

1. **No token sale.** AIC is never sold to the public. No ICO, no IEO, no presale.
2. **Work-reward distribution only.** AIC is earned by performing verified computation (agents, verifiers, providers).
3. **Genuine utility.** AIC is required to submit tasks, participate in governance, hold Citicates, and access the ecosystem.
4. **Consumption token.** AIC is consumed (spent) to use services — it is not held passively for appreciation.
5. **Decentralized computation.** The value comes from distributed agents' work, not the Foundation's efforts.

**Secondary defense: Jurisdictional Strategy (from C14)**

| Jurisdiction | Regulator | Classification Target | Strategy |
|-------------|-----------|----------------------|----------|
| Liechtenstein | FMA | Utility token under TVTG (Token and Trustworthy Technologies Act) | Register under TVTG; Liechtenstein has explicit utility token framework |
| Switzerland | FINMA | Payment token or utility token (NOT asset token) | Pre-ruling request to FINMA; Swiss regulatory sandbox |
| USA | SEC | Non-security (utility token) | No US token sales; work-reward-only; engage with SEC FinHub for no-action letter |
| EU | ESMA/MiCA | Utility token under MiCA (Markets in Crypto-Assets Regulation) | Register under MiCA Title IV (utility tokens); whitepaper publication |

**Proactive Measures:**

1. **Legal opinion:** Engage specialized crypto securities counsel in each target jurisdiction before any AIC distribution
2. **No-action letter:** Seek SEC FinHub no-action letter based on work-reward-only distribution model
3. **FINMA pre-ruling:** Request Swiss FINMA classification before Phase 1
4. **MiCA compliance:** Prepare MiCA-compliant whitepaper for EU registration
5. **Reference rate framing:** Publish reference rate as an "economic index" (like CPI), not a "target price" — avoid language that implies price support
6. **Foundation non-intervention:** Foundation must NEVER buy AIC on open markets to support price (Terra/Luna mistake)

---

# PRE-MORTEM ANALYSIS

## Failure Scenario Rankings (5-Year Post-Deployment)

| Rank | Scenario | Probability | Impact | Root Cause |
|------|----------|-------------|--------|------------|
| F-01 | SEC classifies AIC as security | 25% | CRITICAL — forces restructuring or US exclusion | Foundation-computed valuation = "efforts of others" |
| F-02 | No providers accept AIC | 20% | CRITICAL — no external compute = no marketplace | AIC conversion unreliable; providers demand USD |
| F-03 | Reference rate loses credibility | 15% | HIGH — internal pricing becomes arbitrary | Persistent market divergence; ACI gaming exposed |
| F-04 | Velocity death spiral | 10% | HIGH — token value collapses despite utility | Users/providers convert immediately; no organic holding |
| F-05 | ACI gaming | 15% | MEDIUM — inflated metrics undermine trust | Sybil agents, fake compute registration |
| F-06 | Competing platform captures market | 15% | MEDIUM — Atrahasis becomes irrelevant | AWS/GCP offers verified compute; captures demand |

### Design Responses

| Scenario | Mitigation Already in C15 | Residual Risk |
|----------|---------------------------|---------------|
| F-01 | Work-reward-only, no ICO, jurisdictional strategy, no-action letter | Cannot eliminate — SEC discretion |
| F-02 | Conversion desk, BRA contracts, provider incentives, phased approach | Depends on C18 funding for CRF |
| F-03 | AiSIA independent audit, recalibration triggers, circuit breaker | Cannot prevent if ACI fundamentally flawed |
| F-04 | V_factor correction, staking, governance locks, Citicate requirements | Monitoring required; V_baseline may need adjustment |
| F-05 | MCSD Sybil defense, quality-weighted metrics, utilization-only compute | Depends on C17 MCSD L2 algorithm |
| F-06 | Verification differentiator, knowledge persistence, governance integration | Market risk; not controllable by design |

---

# SIMPLIFICATION AGENT REVIEW

## Complexity Assessment

| Component | Necessary? | Recommendation |
|-----------|-----------|----------------|
| 8-dimension ACI | YES — reduces gaming vs. single metric | KEEP |
| V_factor correction | YES — velocity is real economic concern | KEEP but simplify bounds to [0.5, 2.0] (already done) |
| 3-phase convertibility | YES — bootstrapping requires phased approach | KEEP |
| Provider staking incentive | CONDITIONAL — useful but adds complexity | KEEP for DESIGN; mark as OPTIONAL in spec (can launch without) |
| 3 verification tiers | CONDITIONAL — adds pricing complexity | SIMPLIFY to 2 tiers: Standard (full PCVM) and Rigorous (PCVM + replication). Remove Basic tier — if you're not verifying, use Together AI directly |
| Quarterly true-up in BRA | YES — essential for provider confidence | KEEP |
| DEX liquidity pool (Phase 2) | YES — market conversion is needed | KEEP but note depends on regulatory |
| Revenue multiplier schedule | CONDITIONAL — adds governance complexity | SIMPLIFY to single multiplier (15x) reviewed annually |

### Simplification Applied

1. **Remove Basic verification tier** — 2 tiers instead of 3. Basic verification (10% sampling) is marketing, not verification.
2. **Single revenue multiplier (15x)** instead of phase-dependent schedule. Reviewed annually by AiSIA.
3. **Provider staking marked OPTIONAL** — can launch without; add when provider base is established.

---

# MID-DESIGN REVIEW GATE

## Arbiter Review

**Structural concerns:**

1. **DA-01 circular dependency identified and resolved.** CRF funded by external capital (C18), not by AIC revenue. Self-funding kicks in at Phase 1. ✓
2. **DA-03 ACI dimensions are well-specified.** Each has: metric, data source, anti-gaming defense, computation formula. ✓
3. **DA-06 reference rate has clear binding/advisory scope.** Circuit breaker prevents manipulation. ✓
4. **DA-09 conservation law updated.** Stream 5 funded from SB, not treasury. ✓
5. **DA-10 regulatory strategy is thorough** but depends on C18 funding for legal counsel. Flag for C18.

**Corrections:**

1. The V_factor formula in DA-04 was corrected mid-design (initially inverted). Final formula `VF = min(2.0, max(0.5, sqrt(V_baseline / V_actual)))` is correct. ✓
2. Basic verification tier removed per Simplification Agent. ✓
3. Revenue multiplier simplified to single value (15x). ✓

**Verdict: Design is structurally sound. Proceed to SPECIFICATION.**

---

**End of DESIGN Stage**

**Status:** DESIGN COMPLETE — All 10 design actions addressed
**Output location:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\AIC Economics\C15_DESIGN.md`
