# C35 Commercial Viability Report — Seismographic Sentinel with PCM-Augmented Tier 2

**Invention ID:** C35
**Stage:** FEASIBILITY
**Role:** Commercial Viability Assessor
**Date:** 2026-03-11

---

## 1. Internal Value Assessment

### 1.1 C35's Role in the AAS Value Chain

C35 is not a product. It is load-bearing infrastructure. The Atrahasis Agent System is an adversarial multi-agent platform where agents submit claims, verify each other's work, synthesize knowledge, and settle economic transactions. Every step assumes agent independence. Without a detection layer that can identify when that independence is violated, the platform has no security guarantee — and a platform without security guarantees has no users.

C35 provides the unified detection pipeline that the existing defense triad (C11 CACT, C12 AVAP, C13 CRP+) was designed to assume but that no prior specification fully instantiates. The existing specs each handle a specific attack class:

| Spec | Attack Class | Detection Method | What It Lacks |
|------|-------------|-----------------|---------------|
| C11 CACT | VTD forgery | Commit-attest-challenge-triangulate | No per-agent behavioral baseline; relies on post-hoc temporal analysis |
| C12 AVAP | Collusion | Honeypots, sealed opinions, behavioral analysis (Mechanism 5) | No streaming anomaly detection; pairwise MI screening is batch, not continuous |
| C13 CRP+ | Consolidation poisoning | KL divergence on consolidation inputs | No cross-channel fusion; single-signal detector |
| C17 MCSD L2 | Sybil identity | Pairwise behavioral similarity B(a_i,a_j) | Identity detection only; no real-time anomaly triggering or causal tracing |

C35 unifies these into a coherent three-tier pipeline: Tier 1 provides continuous per-agent anomaly monitoring (the "always-on" baseline that C11 and C12 currently lack), Tier 2 provides neighborhood-scoped multi-channel correlation (the cross-signal fusion that C13 and C17 currently lack), and Tier 3 provides causal traceback (which no existing spec addresses).

**Critical observation:** C12's Layer 1 ("Sentinel Graph") is explicitly referenced as infrastructure fingerprinting and behavioral clustering — but no existing specification actually implements this layer. C35 is, in effect, the implementation specification for C12's assumed-but-unbuilt detection substrate.

### 1.2 Value Quantification

C35 does not generate revenue directly. Its value is defensive: it protects the integrity of the knowledge verification pipeline that underlies the entire AAS economic model.

**If C35 functions correctly:** The platform can credibly claim that Sybil rings are detectable within 20 epochs (~20 minutes), collusion patterns are identifiable via PCM residual analysis, and infrastructure manipulation triggers automated responses through ETR (Emergency Tidal Rollback). This credibility is prerequisite to:
- Attracting external task marketplace participants (C15: projected $2.1M Year 3 revenue)
- Maintaining nominating body confidence (C16: 8 institutional relationships)
- Justifying the AIC token's reference rate (C15: ACI capability index requires trustworthy verification)
- Operating Phase 2+ governance transitions (C14: AI trustees cannot be admitted if Sybil defense is insufficient)

**If C35 fails:** The defense triad (C11/C12/C13) operates without a unified detection substrate. Each spec's detection mechanisms work in isolation. C12's Mechanism 5 (conditional behavioral analysis) operates on batch pairwise MI screening rather than streaming detection. C13's poison detection uses single-channel KL divergence without cross-channel corroboration. The system remains functional but its detection capability is fragmented, slower, and has larger blind spots — particularly for sophisticated adversaries who coordinate across attack vectors.

**Estimated value-at-risk without C35:** Platform credibility loss is difficult to quantify precisely, but the platform's C14 Operational Condition #2 (MCSD fully operational before Phase 1 entry) and C22 Wave 4 security audit requirement (WR-08: no unresolved CRITICAL findings) both assume a coherent detection layer. Without C35, Wave 4 security audit is likely to identify detection fragmentation as a CRITICAL finding.

### 1.3 Dependency Map

C35 is referenced by or depends on the following specifications:

| Spec | Relationship | Nature |
|------|-------------|--------|
| C3 (Tidal) | C35 CONSUMES scheduling data, PRODUCES ETR triggers (skew, starvation, divergence) | Bidirectional |
| C5 (PCVM) | C35 CONSUMES verification outcomes as Tier 1 primary metrics | Input |
| C6 (EMA) | C35 CONSUMES knowledge consolidation data for Tier 2 economic channel | Input |
| C7 (RIF) | C35 PRODUCES cluster membership API consumed by orchestration routing | Output |
| C8 (DSF) | C35 CONSUMES settlement data for Tier 2 economic channel | Input |
| C12 (AVAP) | C35 CONSUMES confirmed AVAP edges as pre-confirmed Tier 2 triggers; AVAP Layer 1 is implemented by C35 | Bidirectional |
| C17 (MCSD L2) | C35 CONSUMES B(a_i,a_j) behavioral similarity scores; C17's LSH infrastructure provides candidate pair pre-filtering | Input |

Seven cross-layer integration points is high but not unprecedented within AAS (C9 reconciliation addressed comparable complexity). The Assumption Validation Report rates integration coherence at 3.5/5 — architecturally sound but complex.

---

## 2. Build vs. Buy Analysis

### 2.1 Available Alternatives

The Prior Art Quick Scan identifies 8 categories of existing technology. None is a substitute for C35, but several could serve as components.

| Technology | Could Replace | Cannot Replace | Verdict |
|-----------|--------------|----------------|---------|
| **SentinelAgent** (Hu et al., 2025) | LLM prompt-level oversight | Verification economics, tidal epochs, PCM residuals, cross-layer ETR | INSUFFICIENT — different threat model entirely (LLM prompt injection vs. multi-agent coordination attacks) |
| **MIDAS** (Bhatia et al., 2020) | Streaming edge anomaly detection (Tier 2 substrate) | Domain semantics, PCM structural correction, multi-channel fusion, ETR | COMPONENT — viable as Tier 2 streaming backbone, already referenced in IC-2 |
| **SybilRank/SybilSCAR family** | Graph-based Sybil detection | Verification co-occurrence signals, behavioral fingerprinting, tidal epoch awareness | SUPERSEDED — C17 MCSD L2 already provides more domain-specific Sybil detection |
| **GNN collusion detection** (Gomes et al., 2024) | Graph-based collusion pattern recognition | Verification committee structure, MQI metrics, streaming operation | COMPONENT — potential Tier 2 enhancement, not replacement |
| **CooccurrenceAffinity** (Mainali et al., 2024) | Co-occurrence null distribution correction | Streaming updates, adversarial robustness, epoch structure | COMPONENT — methodological input to PCM, not replacement |
| **Streaming graph infrastructure** (Neo4j+Flink, TinkerPop) | Graph storage and streaming ingestion primitives | All domain logic, detection algorithms, cross-layer contracts | INFRASTRUCTURE — buy for primitives, build for logic |
| **MAESTRO/MAAIS frameworks** | Threat modeling taxonomy | Actual detection algorithms | TAXONOMIC — useful for threat enumeration, not detection |

### 2.2 Build vs. Buy Verdict

**Build the architecture, buy the primitives.** The Prior Art Report identifies 6 capabilities that do not exist in any available system:

1. Verification committee co-occurrence as a security signal
2. Unified graph combining behavioral, infrastructure, and economic signals
3. Epoch-aware streaming detection tied to tidal scheduling
4. Cross-layer security feedback loops (detection → scheduling/verification/economics/governance)
5. LSH-accelerated behavioral similarity at verification scale
6. MQI metric ingestion for graph construction

These 6 gaps constitute C35's novel contribution. No combination of off-the-shelf tools addresses them. However, C35 can and should leverage existing components:

- **MIDAS**: Constant-time streaming edge detection as Tier 2 substrate (~15% of implementation effort saved)
- **Spectral clustering**: Standard implementations available (Ng et al., 2001) for neighborhood partitioning (~5% saved)
- **LSH**: C17 already specifies the LSH infrastructure (20 tables x 8 hashes); C35 consumes this (~10% saved)
- **Graph databases**: Production infrastructure (Neo4j, TigerGraph, or embedded alternatives) for graph storage (~5% saved)

**Estimated off-the-shelf reuse: ~35-45% of total implementation**, consistent with the 55% novel / 45% off-the-shelf split stated in the task context.

### 2.3 Risk of Not Building C35

If AAS attempts to operate without C35, the defense layer must rely on:
- C12 Mechanism 5 (batch pairwise MI screening) for collusion detection — effective but slow (batch, not streaming)
- C17 B(a_i,a_j) for Sybil detection — effective but identity-focused, not behavior-anomaly-focused
- C13 KL divergence for consolidation poisoning — effective but single-channel

This configuration has two critical gaps:
1. **No real-time per-agent anomaly baseline**: No existing spec provides continuous STA/LTA monitoring of individual agent behavior. Anomalies are detected only when batch analysis runs.
2. **No cross-channel fusion**: Each defense spec operates on its own signal. A coordinated attack that manifests across verification, behavioral, infrastructure, and economic channels simultaneously would need to be detected independently by each spec — and no mechanism aggregates these signals into a unified alert.

**Verdict: BUILD. C35 is not discretionary.** It fills a structural gap in the defense architecture that no existing spec or off-the-shelf tool addresses. Without it, Wave 4's defense hardening is incomplete and WR-08 (security audit with no CRITICAL findings) is at risk.

---

## 3. Cost Estimation

### 3.1 Development Cost Model

C35 development cost is estimated within C22's budget framework, using the same personnel cost assumptions ($18K-$22K blended fully-loaded per person per month).

**Component breakdown:**

| Component | Effort (person-months) | Novel % | Off-the-Shelf % | Risk |
|-----------|----------------------|---------|-----------------|------|
| **Tier 1: STA/LTA engine** | 3-4 | 40% (dual-baseline fusion, AAS-specific metrics) | 60% (STA/LTA is mature seismology) | LOW — well-understood algorithm adapted to new domain |
| **Tier 2: PCM residual computation** | 6-9 | 80% (no direct precedent for streaming adversarial PCM) | 20% (covariate-adjusted networks from ecology) | HIGH — most novel, least validated component |
| **Tier 2: Multi-channel fusion** | 3-4 | 50% (weighted Bayesian fusion over AAS-specific channels) | 50% (Dempster-Shafer, Bayesian network methods) | MEDIUM — known techniques, novel application |
| **Tier 2: Neighborhood partitioning** | 2-3 | 30% (adversarial hardening) | 70% (spectral clustering standard) | MEDIUM — adversarial robustness is active research |
| **Tier 3: Epidemiological traceback** | 2-3 | 50% (digital application of epi methods) | 50% (overdispersion analysis is standard epi) | LOW-MEDIUM — sound methodology, sample size concern |
| **Cross-layer integration** | 4-6 | 70% (7 cross-layer contracts, AAS-specific) | 30% (gRPC/messaging standard) | MEDIUM — high complexity, manageable with C9 framework |
| **ETR output generation** | 1-2 | 60% (AAS-specific trigger semantics) | 40% (threshold-based alerting standard) | LOW |
| **Testing + hardening** | 4-6 | N/A | N/A | MEDIUM — adversarial testing requires red team |

**Total estimated effort: 25-37 person-months**

**Cost at C22 rates:**
- Low estimate: 25 person-months x $18K = $450K
- High estimate: 37 person-months x $22K = $814K
- **Mid-range: $550K-$700K**

### 3.2 Infrastructure Cost

C35 requires:
- Graph database instance for agent correlation graph: $2K-$5K/month
- Compute for PCM precomputation at CONSOLIDATION_CYCLE cadence: $1K-$3K/month
- Streaming infrastructure for Tier 1 continuous monitoring: $1K-$2K/month
- Simulation environment for calibration and testing: $3K-$8K/month (temporary, W0/early implementation)

**Monthly infrastructure: $4K-$10K during development; $4K-$10K ongoing**
**Total infrastructure through implementation: $50K-$120K**

### 3.3 Fit Within C22 Budget

C22 allocates Wave 4 (Defense Systems) at $900K-$1.3M for C11+C12+C13 over 3-4 months with 15-17 engineers. C35 was not part of the original C22 plan — it is a new specification that emerged post-C22.

**Budget integration options:**

| Option | Approach | Cost Impact | Timeline Impact |
|--------|----------|-------------|-----------------|
| **A: Absorb into Wave 4** | Add C35 to existing W4 defense scope. Extend W4 by 2-3 months. Add 2-3 engineers (Team Delta). | +$400K-$700K to W4 budget | W4 extends from 3-4 months to 5-7 months; downstream W5 delayed |
| **B: Parallel track starting Wave 3** | Begin C35 Tier 1 during W3 (when C3/C5 data becomes available). PCM development in W4. Integration in W5. | +$550K-$700K spread across W3-W5 | Minimal timeline impact; spreads load |
| **C: Separate Wave 4.5** | Insert a dedicated C35 wave between W4 and W5. | +$500K-$650K as separate budget line | 2-3 month insertion between W4 and W5 |

**Recommended: Option B (Parallel Track).** C35's Tier 1 (per-agent STA/LTA) requires only C3 scheduling data and C5 verification outcomes, both available at Wave 2 exit. Starting Tier 1 development during Wave 3 allows the most expensive component (Tier 2 PCM) to begin in Wave 4 alongside the defense hardening it supports.

**Total C35 budget impact on C22: +$550K-$700K (8-11% increase on $6.5M-$9.1M)**

This is within C22's 10% contingency reserve ($593K-$827K) at the low end, and requires modest contingency draw at the high end.

---

## 4. Adoption Barriers

### Barrier 1: PCM Calibration Validation Risk
**Severity: HIGH**

The PCM (Permitted Correlation Model) is the most novel component and has no direct precedent. The Assumption Validation Report rates A-4 (PCM calibration convergence) as "PLAUSIBLE BUT UNVALIDATED" and flags EXP-3 simulation as BLOCKING for FEASIBILITY advancement.

**Specific concern:** The Science Assessment identifies a linear-additive model assumption (Σ_k f_k(structural_overlap_k)) that is unlikely to hold because covariates are dependent. Interaction terms are needed, which changes the computational model and may increase the calibration period beyond 1,000 epochs.

**Mitigation:**
- Accept non-linear model (log-linear or kernel-based) at DESIGN stage as recommended by Science Advisor
- EXP-3 simulation must be added to W0 or early W3 experimental program
- Fallback: Condition C-3 already specifies degradation to raw correlation analysis below PCM coverage threshold of 0.70
- Pre-register kill criterion: if PCM calibration requires >5,000 epochs (~83 hours), the PCM approach must be redesigned or descoped to a simpler structural correction

### Barrier 2: Cross-Layer Integration Complexity
**Severity: HIGH**

C35 integrates with 7 existing specifications — the highest cross-layer dependency count of any AAS specification. Each integration point requires a formal C9 contract, data format agreement, timing synchronization, and failure mode handling.

**Specific concerns:**
- C35 must consume data from layers at different maturity tiers during staged rollout (e.g., C3 may be Functional while C8 is still Stub during Wave 3)
- Timing: Tier 1 operates per SETTLEMENT_TICK (60s), Tier 2 per TIDAL_EPOCH (3600s), neighborhood partitioning per CONSOLIDATION_CYCLE (36,000s) — three different temporal cadences requiring synchronization
- ETR output generation must be compatible with C3's existing Emergency Tidal Rollback protocol, which was designed before C35 existed

**Mitigation:**
- Leverage C9 cross-layer contract framework (already handles comparable complexity)
- Design C35's integration layer with graceful degradation: missing inputs from unavailable layers reduce capability but do not cause failure
- Begin with Tier 1 only (depends on C3 + C5 only — 2 contracts, not 7) and add integration points incrementally as layers mature
- Allocate 4-6 person-months specifically to cross-layer integration (already included in cost estimate)

### Barrier 3: Decision Fusion Formalism Gap
**Severity: MEDIUM**

Three distinct fusion problems are formally unresolved:
1. **Dual-baseline fusion** (Tier 1): How to combine fixed and adaptive STA/LTA when they disagree (Contradiction C-3)
2. **Multi-channel fusion** (Tier 2): The 3-of-4 quorum assumes channel independence, which does not hold (Contradiction C-2)
3. **PCM + raw correlation fusion**: How to blend PCM residuals with raw correlation during the Bootstrap-to-Calibrated transition

**Mitigation:**
- All three are design-stage problems with well-studied solutions (Bayesian networks, Dempster-Shafer, weighted voting)
- The 3-of-4 quorum can serve as a simplified fallback while principled fusion is developed
- Specify fusion rule selection as a DESIGN deliverable with explicit operating-point analysis (FAR/FRR tradeoff)

### Barrier 4: Adversarial Evasion of Fixed Baselines
**Severity: MEDIUM**

Monitoring Flag MF-4 identifies that an adversary who can observe system behavior during the calibration window may be able to infer fixed baseline parameters and craft behavior that stays just below detection thresholds.

**Specific concern:** The fixed baseline is established at agent registration and never updated. If the adversary knows the registration-time behavioral profile of the system, they can reconstruct what "normal" looked like at registration and calibrate their evasion accordingly.

**Mitigation:**
- Red Team evaluation at FEASIBILITY (per MF-4 requirement)
- Noise injection into fixed baseline parameters (add calibrated random offset to thresholds)
- Periodic fixed-baseline refresh with safeguards (e.g., refresh only from agents with credibility > 0.8, minimum 100 contributing agents)
- Asymmetric information: do not publish fixed baseline thresholds; adversary must infer from observation, which requires extended probing that itself generates detectable patterns

### Barrier 5: Sample Size Constraints for Tier 3
**Severity: MEDIUM**

Tier 3 (epidemiological backward tracing) requires confirmed anomalies as input. The Science Assessment notes that overdispersion analysis needs at least 30 confirmed anomalies per analysis window. If the system is working well (few anomalies), Tier 3 may rarely accumulate sufficient sample sizes.

**Mitigation:**
- Lower Tier 3 activation threshold to include WATCH-level events (not just confirmed FLAG events)
- Use synthetic/simulated anomalies for Tier 3 calibration (standard practice in epidemiology for rare events)
- Accept Tier 3 as a "rare event" capability that provides high value when activated but is not continuously active
- This is acceptable: Tier 3 is designed for post-incident root cause analysis, not continuous monitoring

### Barrier 6: Spectral Clustering Adversarial Vulnerability
**Severity: MEDIUM**

The Assumption Validation Report notes (A-5) that spectral clustering is vulnerable to adversarial graph perturbations — an attacker controlling O(sqrt(V)) edges can significantly alter cluster boundaries (Bojchevski & Gunnemann, 2019). Manipulated cluster boundaries could isolate colluding agents from detection neighborhoods or merge them with high-credibility agents to dilute anomaly signals.

**Mitigation:**
- Robust spectral methods (certified robustness, Zugner et al. 2020) — adds computational cost but mitigates boundary manipulation
- Randomized perturbation of clustering input graph (run multiple clustering iterations with random edge perturbations, take majority assignment)
- Detection of adversarial graph modification itself (anomalous clustering instability across iterations is a signal)
- The 2*log(V) cap with split-on-overflow already mitigates concentration attacks

### Barrier 7: Team Expertise Availability
**Severity: LOW-MEDIUM**

C35 requires engineers with expertise in streaming anomaly detection, graph algorithms, statistical modeling, and adversarial robustness. This intersection is narrower than general distributed systems engineering.

**Mitigation:**
- C22's cross-training strategy applies: hire strong distributed systems engineers, train them on anomaly detection
- Team Delta (defense systems) is the natural home for C35 implementation
- PCM development can leverage academic collaboration (the ecological covariate-adjusted network methodology has active research communities)
- Tier 1 (STA/LTA) is straightforward enough for any signal-processing-aware engineer

### Barrier 8: C22 Budget and Timeline Strain
**Severity: LOW-MEDIUM**

C35 was not part of the original C22 plan. Adding it mid-implementation creates budget pressure and potential schedule disruption.

**Mitigation:**
- Option B (parallel track) minimizes timeline disruption by spreading C35 across W3-W5
- Cost ($550K-$700K) is within or near C22's 10% contingency reserve
- C35 can be phased: Tier 1 at Wave 3 (low cost, high immediate value), Tier 2/3 at Wave 4-5 (higher cost, deferred)
- If budget is constrained, Tier 1 alone ($150K-$220K) provides significant value as a standalone per-agent anomaly detector

### Summary Table

| # | Barrier | Severity | Timeframe | Mitigation Confidence |
|---|---------|----------|-----------|----------------------|
| 1 | PCM calibration validation | HIGH | FEASIBILITY/DESIGN | MEDIUM — requires EXP-3 simulation results |
| 2 | Cross-layer integration complexity | HIGH | DESIGN/IMPLEMENTATION | HIGH — C9 framework handles this pattern |
| 3 | Decision fusion formalism gap | MEDIUM | DESIGN | HIGH — well-studied alternatives exist |
| 4 | Fixed baseline adversarial evasion | MEDIUM | FEASIBILITY/DESIGN | MEDIUM — Red Team evaluation needed |
| 5 | Tier 3 sample size constraints | MEDIUM | IMPLEMENTATION | HIGH — acceptable as rare-event capability |
| 6 | Spectral clustering vulnerability | MEDIUM | DESIGN | MEDIUM — robust methods exist but add cost |
| 7 | Team expertise availability | LOW-MEDIUM | IMPLEMENTATION | HIGH — cross-training strategy covers this |
| 8 | Budget and timeline strain | LOW-MEDIUM | IMPLEMENTATION | HIGH — within contingency, phased deployment |

---

## 5. Risk to Platform

### 5.1 If C35 Fails Entirely

**Scenario:** PCM does not converge, or the multi-channel fusion produces unacceptable false positive rates, and C35 is abandoned.

**Impact: SERIOUS but not FATAL.** The AAS platform continues operating with the existing defense triad:
- C11 CACT handles VTD forgery (commit-reveal + temporal triangulation)
- C12 AVAP handles collusion (honeypots, sealed opinions, behavioral MI screening)
- C13 CRP+ handles consolidation poisoning (KL divergence, quarantine)
- C17 MCSD L2 handles Sybil identity detection (behavioral similarity)

The platform has defense-in-depth without C35. What it lacks is:
- Continuous per-agent anomaly monitoring (gap: slow-developing anomalies go undetected until batch analysis)
- Cross-channel signal fusion (gap: coordinated multi-vector attacks detected slowly or not at all)
- Automated causal traceback (gap: root cause analysis remains manual)

**Estimated detection capability without C35:** Approximately 60-70% of the detection capability with C35, based on the C12 Research Report's estimate that sophisticated rings can evade batch-only defenses for 100+ epochs vs. C35's target of 20-epoch detection.

**Fallback path:** If C35 fails, the most valuable component (Tier 1 STA/LTA) can likely be salvaged as a standalone per-agent anomaly detector integrated into C5 PCVM's credibility engine. This preserves ~30% of C35's value at ~20% of the cost.

### 5.2 If C35 Is Delayed

**Scenario:** C35 takes 6-12 months longer than planned. Waves 4-5 proceed without it.

**Impact: MODERATE.** The defense hardening wave (W4) can proceed with C11+C12+C13 as originally planned. C35 becomes a post-Wave 5 addition. The main consequences:
- Wave 4 security audit (WR-08) may identify detection fragmentation as a finding, but likely HIGH not CRITICAL if the individual defense specs are operational
- C14 Phase 2 entry (which requires MCSD fully operational) may be affected if C17+C35 integration is on the critical path
- The task marketplace (C15) can operate with reduced detection capability, but institutional confidence may be lower

**Mitigation:** Phase C35 delivery: Tier 1 by end of Wave 4 (minimal delay), Tiers 2-3 by end of Wave 5 or post-Wave 5.

### 5.3 If C35 Succeeds

**Scenario:** C35 delivers on its specifications. PCM converges. Multi-channel fusion operates within acceptable FAR/FRR bounds.

**Impact: SIGNIFICANT POSITIVE.** The AAS platform gains:
- The first unified, streaming, multi-channel anomaly detection system for any multi-agent platform
- Automated ETR triggers that create a closed-loop between detection and scheduling (security → operational adjustment in <20 epochs)
- A detection substrate that makes C11, C12, C13, and C17 more effective by providing them with pre-filtered, structurally-corrected anomaly signals
- A defensible competitive advantage (see Section 6)

---

## 6. Competitive Moat Assessment

### 6.1 PCM as Defensive Innovation

The Permitted Correlation Model is C35's most novel component. It computes expected inter-agent correlation from structural covariates (committee co-assignment, parcel overlap, temporal co-occurrence, resource sharing) and detects anomalies as unexplained residuals. This approach:

1. **Has no direct precedent in multi-agent security.** Configuration-model residual networks (Newman 2010) and covariate-adjusted association networks (Ovaskainen et al. 2017) are methodological predecessors from network science and ecology, but neither operates in adversarial settings with streaming updates.

2. **Is hard to replicate without the AAS context.** PCM's structural covariates are AAS-specific: committee rotation schedules (C3), verification co-occurrence (C5), settlement data (C8), behavioral similarity (C17). A competitor would need equivalent infrastructure to generate equivalent covariates.

3. **Creates a learning advantage.** As PCM accumulates calibration data, its residual accuracy improves. A late entrant starts with no calibration data and no structural covariate history. This creates a time-based moat — the first platform with PCM has better detection than any platform that implements it later with less history.

### 6.2 Competitive Landscape

| Competitor / Approach | What It Does | Why It Is Not C35 |
|----------------------|-------------|-------------------|
| SentinelAgent (2025) | LLM prompt-level oversight via graph-based anomaly detection | Different threat model (prompt injection, tool misuse). No verification economics, no structural correction, no tidal epoch awareness. |
| Traditional IDS (Snort, Suricata) | Network intrusion detection via signature matching | Wrong level of abstraction. Detects network attacks, not agent behavioral anomalies. |
| Blockchain fraud detection | Transaction graph anomaly detection | Single-signal (economic only). No behavioral, infrastructure, or verification channels. |
| ML-based anomaly detection (general) | Unsupervised anomaly detection on time series | No structural correction (PCM). Cannot distinguish legitimate correlation from adversarial. High false positive rates without domain-specific baselines. |

**No competing system provides structural correction of inter-agent correlation in a multi-agent verification context.** This gap is not an accident — it reflects the fact that multi-agent verification platforms with formal economic settlement layers do not yet exist at scale. C35's moat is tied to the AAS platform's uniqueness.

### 6.3 Moat Durability

**Strong moat (3-5 years):** The PCM approach is novel enough that a competitor would need to independently develop the concept, build comparable structural covariate infrastructure, and accumulate calibration data. This is a multi-year effort.

**Weakening factors:**
- The PCM concept, once published in C35's specification, becomes replicable in principle
- If the AAS specs are open-sourced (per C22's implementation philosophy), competitors gain free access to the design
- General-purpose ML anomaly detection is improving rapidly; a sufficiently powerful general model might achieve comparable detection without structural correction

**Net assessment:** C35 creates moderate-to-strong competitive advantage for the 3-5 year AAS implementation horizon. The advantage is strongest in the combination of PCM with AAS-specific integration (7 cross-layer contracts), not in PCM as an isolated algorithm.

---

## 7. Timeline Assessment

### 7.1 C35 Within the Wave Structure

C35 was not part of C22's original wave plan. The existing wave structure:

```
W0 (2-3 mo) → W1 (4-5 mo) → W2 (4-6 mo) → W3 (4-6 mo) → W4 (3-4 mo) → W5 (4-6 mo)
                                                              ^^^^^^^^
                                                              Defense
                                                              C11+C12+C13
```

C35 fits most naturally as a parallel track beginning at Wave 3 and extending through Wave 5:

```
W0 ──→ W1 ──→ W2 ──→ W3 ──────→ W4 ──────→ W5
                       │          │           │
                       │ C35 T1   │ C35 T2    │ C35 T3 + Integration
                       │ (STA/LTA)│ (PCM)     │ (Epi traceback)
                       └──────────┴───────────┘
```

**Rationale:**
- **Tier 1 at Wave 3:** Requires only C3 scheduling data + C5 verification outcomes, both available at W2 exit. STA/LTA engine is the simplest component (3-4 person-months). Delivers immediate value: per-agent anomaly baselines operational before defense hardening begins.
- **Tier 2 at Wave 4:** PCM requires more data inputs (C8 settlement, C17 behavioral similarity) and more development time (6-9 person-months for PCM alone). Aligns with defense hardening wave. Multi-channel fusion developed alongside C11/C12/C13 integration.
- **Tier 3 + full integration at Wave 5:** Epidemiological traceback requires confirmed Tier 2 anomalies as input. Cross-layer integration finalized. ETR outputs connected to C3.

### 7.2 Team Allocation

C22 assigns Team Delta to defense systems from Wave 4. Under Option B:

- **Wave 3:** 1-2 engineers from Team Delta begin C35 Tier 1 development (borrowed capacity; main team working on C6+C7). Cost: ~$70K-$130K in incremental W3 spend.
- **Wave 4:** 3-4 engineers on C35 within Team Delta (alongside C11+C12+C13 work). C35 consumes approximately 25-30% of Team Delta's Wave 4 capacity.
- **Wave 5:** 2-3 engineers complete Tier 3 and full integration. C35 consumes approximately 15-20% of Team Delta/Epsilon capacity.

### 7.3 Critical Path Items

| Item | When | Blocking |
|------|------|----------|
| PCM convergence simulation (EXP-3 equivalent) | Early Wave 3 or pre-Wave 3 | Tier 2 design decisions |
| Dual-baseline fusion rule specification | Wave 3 (Tier 1 design) | Tier 1 implementation |
| Multi-channel correlation analysis | Wave 4 (Tier 2 design) | Quorum threshold selection |
| Red Team fixed-baseline evaluation (MF-4) | Wave 3-4 boundary | Tier 1 hardening |
| C9 contract updates for 7 integration points | Waves 3-5 progressively | Cross-layer integration |

### 7.4 Timeline Confidence

**HIGH for Tier 1:** STA/LTA is well-understood. Dual-baseline extension is novel but tractable. 3-4 person-months is conservative.

**MEDIUM for Tier 2:** PCM is the least validated component. If convergence simulation (EXP-3) reveals problems, Tier 2 design may need iteration. The 6-9 person-month estimate has high variance.

**MEDIUM-HIGH for Tier 3:** Epidemiological methods are sound. Sample size concern is mitigable. 2-3 person-months is achievable.

**Overall: C35 can be delivered within the extended C22 timeline (W3-W5) with MEDIUM-HIGH confidence.** The primary schedule risk is Tier 2 PCM development; if PCM convergence proves difficult, the schedule could extend 2-3 months.

---

## 8. Recommendation

### Verdict: CONDITIONAL_ADVANCE

C35 should advance to DESIGN with the following conditions.

### Justification

**Why ADVANCE (not REJECT):**
1. C35 fills a structural gap in the defense architecture. The existing defense triad (C11/C12/C13) operates without a unified detection substrate. C35 provides the streaming, multi-channel, structurally-corrected anomaly detection layer that these specs assume but do not implement.
2. No off-the-shelf alternative exists. The Prior Art Report identifies 8 categories of existing technology; none is a substitute. C35's PCM has no direct precedent.
3. The cost ($550K-$700K) is within or near C22's contingency reserve. Budget impact is 8-11% of total C22 budget.
4. The platform can operate without C35, but with materially degraded detection capability (~60-70% of potential). For a platform whose value proposition depends on verification integrity, this degradation is strategically unacceptable.

**Why CONDITIONAL (not unconditional ADVANCE):**
1. PCM convergence is unvalidated. EXP-3 simulation is blocking.
2. Three decision fusion problems are formally unresolved. Each is tractable but none has been solved yet.
3. Fixed baseline adversarial reconstructibility (MF-4) requires Red Team evaluation.
4. The cross-layer integration count (7 specs) is the highest in AAS and carries non-trivial coordination risk.

### Required Conditions for DESIGN Entry

| ID | Condition | Blocking? |
|----|-----------|-----------|
| **CC-1** | PCM convergence simulation (EXP-3 equivalent) must demonstrate calibration within 5,000 epochs for a 1,000-agent synthetic population with 5 structural covariates. Kill criterion: if convergence requires >10,000 epochs, PCM must be redesigned. | YES |
| **CC-2** | Dual-baseline fusion rule must be specified with explicit FAR/FRR operating point analysis for at least 3 candidate rules (OR, AND, weighted). | YES |
| **CC-3** | Red Team evaluation of fixed-baseline reconstructibility (MF-4) must produce either (a) an attack that demonstrates practical reconstructibility with mitigation design, or (b) a formal argument bounding adversary's inference capability. | YES |
| **CC-4** | C22 Steering Committee must approve budget augmentation of $550K-$700K or identify offsetting savings within the existing Wave 3-5 budget. | YES |
| **CC-5** | C9 contract framework must be extended with preliminary interface specifications for all 7 C35 integration points before Tier 2 development begins. | NO (may proceed during Wave 3; required before Wave 4) |

### Monitoring Flags

| ID | Flag | Review Point |
|----|------|-------------|
| MF-A | PCM non-linear model (interaction terms) computational cost must remain within O(V log V) amortized bound after model revision. | DESIGN |
| MF-B | Multi-channel fusion must account for channel correlation; 3-of-4 quorum is acceptable as fallback only. | DESIGN |
| MF-C | Tier 3 sample size feasibility must be validated via simulation before Tier 3 implementation begins (Wave 5). | Wave 4 exit |
| MF-D | Spectral clustering adversarial robustness must be evaluated; if robust methods add >50% computational overhead, consider randomized perturbation alternative. | DESIGN |

### Scoring Summary

```json
{
  "type": "COMMERCIAL_VIABILITY_ASSESSMENT",
  "invention_id": "C35",
  "stage": "FEASIBILITY",
  "decision": "CONDITIONAL_ADVANCE",
  "internal_value": "HIGH — fills structural gap in defense architecture; enables unified streaming detection",
  "build_vs_buy": "BUILD — no off-the-shelf substitute; ~35-45% component reuse achievable",
  "cost_estimate": "$550K-$700K (8-11% of C22 total budget)",
  "adoption_barriers": {
    "HIGH": 2,
    "MEDIUM": 4,
    "LOW-MEDIUM": 2,
    "blocking": "PCM convergence validation (CC-1), dual-baseline fusion (CC-2), Red Team evaluation (CC-3), budget approval (CC-4)"
  },
  "platform_risk_without_C35": "SERIOUS — detection capability degrades to ~60-70% of potential; Wave 4 security audit at risk for CRITICAL finding",
  "competitive_moat": "MODERATE-TO-STRONG — PCM is novel (no precedent), AAS-specific integration creates 3-5 year advantage",
  "timeline_fit": "MEDIUM-HIGH — parallel track W3-W5 achievable; Tier 2 PCM is primary schedule risk",
  "conditions_count": 5,
  "monitoring_flags_count": 4
}
```

---

**End of Commercial Viability Report**

**Status:** FEASIBILITY — CONDITIONAL_ADVANCE with 5 conditions and 4 monitoring flags
**Output location:** `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\docs\task_workspaces\T-060\COMMERCIAL_VIABILITY_REPORT.md`
