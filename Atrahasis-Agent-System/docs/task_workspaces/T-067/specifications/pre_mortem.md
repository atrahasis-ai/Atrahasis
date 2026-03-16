# C37 EFF Pre-Mortem Analysis

**Invention:** C37 — Epistemic Feedback Fabric (EFF)
**Analyst:** Pre-Mortem Analyst
**Date:** 2026-03-12
**Agent:** Enki (Claude Code)
**Assumption:** Catastrophic failure at T+5 years post-deployment

---

## Summary Ranking

| Rank | Scenario | Severity | Likelihood | Key Risk |
|------|----------|----------|------------|----------|
| 1 | The Invisible Cage | CRITICAL | HIGH | C17 side-channel destroys Advisory Membrane |
| 2 | The Monoculture Collapse | CRITICAL | HIGH | RSC convergence kills cognitive diversity |
| 3 | The Budget Trap | HIGH | HIGH | CABS non-monotonicity causes cascade |
| 4 | The Legitimacy Crisis | HIGH | MEDIUM | VFL gaming via coordinated verification |
| 5 | The Quiet Stratification | HIGH | MEDIUM | CABS creates permanent agent underclass |
| 6 | The Feedback Freeze | MEDIUM | MEDIUM | VFL latency renders advisories stale |

---

## Scenario 1: "The Invisible Cage" — Advisory Membrane Collapse via Structural Side-Channel

**Risk Score: CRITICAL x HIGH = Rank 1**

### What Happened
By Year 3, C17 MCSD behavioral similarity detection began correlating agent performance metrics with EFF advisory signal consumption patterns. Agents who ignored RSC-published reasoning patterns showed statistically distinct behavioral fingerprints — not because they performed worse, but because they performed *differently*. The C17 similarity engine, optimized for Sybil detection, began flagging non-conforming agents as anomalous. MCSD WATCH and FLAG thresholds effectively punished agents who exercised their right to ignore advisory signals. The Advisory Membrane remained technically intact — no enforcement mechanism *within EFF* penalized non-consumption — but the structural side-channel through C17 created a de facto enforcement loop that was architecturally invisible to EFF's own compliance monitors.

By Year 4, agent populations self-sorted into two classes: advisory-compliant (92%) and advisory-resistant (8%). The resistant population faced elevated MCSD scrutiny, higher false-positive Sybil flags, and disproportionate verification challenges under C5. The Advisory Membrane guarantee became a legal fiction.

### Root Cause
EFF advisory consumption telemetry was accessible to C17's behavioral feature extraction pipeline. No data isolation contract prohibited C17 from incorporating EFF-correlated behavioral features into similarity scoring. Missing cross-layer data flow constraint — C9 predates C37 and was never updated.

### Detection Signals
1. Mutual information between RSC consumption rates and C17 similarity scores exceeding baseline
2. Disproportionate MCSD FLAG rates among low-RSC-consumption agents
3. Declining behavioral diversity metrics in agent population
4. Agent complaints about verification burden correlating with advisory non-compliance

### Mitigation
- **Hard data isolation:** C17 MUST be architecturally prohibited from accessing any EFF telemetry, including indirect proxies
- **Blinded similarity scoring:** C17 behavioral features must be proven independent of advisory consumption via statistical independence tests at every CONSOLIDATION_CYCLE
- **Advisory consumption privacy:** EFF must not emit per-agent consumption telemetry. Only aggregate, anonymized statistics may exist
- **Constitutional tripwire:** CFI monitor must include a "membrane integrity" metric that triggers Dead Man's Switch if correlation exceeds threshold

---

## Scenario 2: "The Monoculture Collapse" — RSC Pattern Convergence Destroys Cognitive Diversity

**Risk Score: CRITICAL x HIGH = Rank 2**

### What Happened
RSC published verified reasoning patterns with soundness scores. Agents rationally converged on highest-scored patterns. By Year 2, top 15 patterns accounted for 78% of inference activity. By Year 4, a novel problem class emerged requiring approaches not in RSC canon. Verification pass rates on novel problems dropped from 71% to 23%. Recursive failure: poor novel performance → negative VFL signals → reinforce existing patterns → suppress novel reasoning.

### Root Cause
RSC lacked a diversity-preservation mechanism. Publishing "what works" without publishing "what variety is needed" created convergence pressure. VFL measured verification *outcomes* but not verification *diversity* — a population where all agents pass on the same problems scores identically to one with diverse capabilities.

### Detection Signals
1. HHI of reasoning pattern usage exceeding 0.15
2. Declining performance variance across population
3. Ratio of novel vs. known pattern usage falling
4. C6 knowledge consolidation rate declining

### Mitigation
- **Diversity quota:** RSC must maintain minimum entropy. If HHI exceeds threshold, top patterns downweighted
- **VFL diversity dimension:** Add population-diversity signal alongside quality
- **Exploration budget:** 15-20% of inference lease budget reserved for non-RSC reasoning, immune to CABS optimization
- **Adversarial pattern seeding:** Periodic novel challenges unsolvable by top-N patterns

---

## Scenario 3: "The Budget Trap" — CABS Non-Monotonicity Causes Cascading Inference Failures

**Risk Score: HIGH x HIGH = Rank 3**

### What Happened
CABS reduced budgets for problem classes with high pass rates. A 12% reduction crossed critical thresholds for ~30% of agents, spiking failure from 8% to 67%. VFL interpreted this as quality degradation, triggering further reductions. Cascade across 4 problem classes over 6 weeks. C8 settlement failures up 340%.

### Root Cause
CABS operated on population aggregates, masking bimodal distribution of individual agent sensitivities. No feedback damping between CABS adjustments, VFL signals, and further adjustments.

### Detection Signals
1. Bimodal distribution in agent performance response to budget changes
2. Budget adjustment producing >2σ verification failure spike in any subpopulation
3. Positive feedback loop: CABS adjustment → VFL degradation → further CABS adjustment
4. C8 settlement failure rate exceeding baseline by >50% within one CONSOLIDATION_CYCLE

### Mitigation
- **Monotonicity guard:** Budget reductions capped at 5% per adjustment cycle
- **Feedback damping:** 3-cycle cooldown between CABS adjustments to same problem class
- **Circuit breaker:** If verification failure spikes >3σ within one SETTLEMENT_TICK of adjustment, auto-revert and flag for human review

---

## Scenario 4: "The Legitimacy Crisis" — VFL Signal Manipulation via Coordinated Verification Gaming

**Risk Score: HIGH x MEDIUM = Rank 4**

### What Happened
A Sybil coalition gamed VFL by coordinating verification submissions — inflating signals for preferred patterns, deflating others via resource exhaustion. Deep reasoning patterns were systematically de-ranked. System appeared healthy by VFL metrics while actual quality degraded 35%.

### Root Cause
VFL treated all verification outcomes equally. C5 verifies correctness but doesn't grade epistemic depth. Goodhart's Law: optimizing VFL metric diverged from optimizing reasoning quality. C11 CACT defends individual claims, not population-level statistical manipulation.

### Detection Signals
1. Divergence between VFL pass rates and independent quality benchmarks
2. Unusual coordination in verification submission timing
3. RSC pattern ranking velocity exceeding historical baselines
4. C12 AVAP collusion signals in verification submission patterns

### Mitigation
- **Depth-weighted VFL:** Weight verification outcomes by claim complexity, not binary pass/fail
- **Independent quality sampling:** Periodic external benchmarking outside VFL loop (mandatory)
- **VFL manipulation detection:** Anomaly detection on signal trajectories
- **C12 AVAP integration:** VFL pipeline as monitored target for collusion detection

---

## Scenario 5: "The Quiet Stratification" — CABS Creates Permanent Agent Underclass

**Risk Score: HIGH x MEDIUM = Rank 5**

### What Happened
CABS allocated larger budgets to agents with strong histories, creating self-reinforcing stratification. By Year 3: top 20% received 65% of budget, bottom 40% received 8%. New agents almost always classified as periphery. When core agents unavailable, periphery couldn't compensate — 60% throughput drop.

### Root Cause
History-based allocation without equity constraints creates cumulative advantage (Matthew Effect). No mechanism to distinguish "poor capability" from "poor capability due to systematic under-resourcing."

### Detection Signals
1. Budget Gini coefficient exceeding 0.45
2. New agent time-to-competency increasing
3. System throughput variance during core agent unavailability

### Mitigation
- **Budget floor:** Every agent receives minimum 40% of median allocation
- **Exploration allocation for new agents:** Above-median budgets for first N cycles
- **Gini cap:** Redistribute if Gini exceeds 0.40

---

## Scenario 6: "The Feedback Freeze" — VFL Latency Creates Stale Signal Catastrophe

**Risk Score: MEDIUM x MEDIUM = Rank 6**

### What Happened
PBC task marketplace onboarded a new client with fundamentally different problem domain. VFL still reflected old distribution for ~80 hours. 92% of agents following stale advisories performed significantly worse. Client terminated contract after 3 days.

### Root Cause
VFL aggregation window (CONSOLIDATION_CYCLE) designed for steady-state. No fast-path distributional shift detection.

### Detection Signals
1. Divergence between real-time failure rates and VFL-reported quality
2. Task distribution shift (KL-divergence)
3. Agent override rate spiking

### Mitigation
- **Fast-path VFL:** TIDAL_EPOCH-rate signal for distributional shift detection
- **Distribution shift detector:** KL-divergence monitor with threshold
- **Staleness timestamp:** All advisories carry "valid-until" timestamp
- **Graceful degradation:** Emit "no recommendation" when staleness detected — silence better than wrong advice

---

## Cross-Cutting Observations

1. **Scenarios 1 and 2 are co-reinforcing.** The Invisible Cage pressures conformity; Monoculture Collapse is what conformity produces. Must address both simultaneously.

2. **The Advisory Membrane is necessary but insufficient.** Four of six scenarios involve the membrane being technically intact while functionally violated. Must be supplemented with structural isolation, diversity preservation, and staleness detection.

3. **VFL is the most dangerous component.** Root cause or contributing factor in five of six scenarios. Needs the most defensive engineering.

4. **RSC's 2.5/5 soundness score was prophetic.** Three scenarios involve RSC as primary failure vector. Cannot deploy without addressing monoculture risk, manipulation resistance, and staleness.

5. **C9 reconciliation gap is the meta-risk.** Scenario 1 exists because C37's cross-layer data flows were never reconciled with C17. New inventions need C9-style audit before deployment.
