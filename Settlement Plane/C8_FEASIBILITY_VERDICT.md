# C8 — Deterministic Settlement Fabric (DSF): Feasibility Verdict

## TASK 3: ASSESSMENT COUNCIL

---

### Council Convened

**Participants:** Systems Architect, Science Advisor, Economics Analyst, Security Auditor, Integration Specialist

---

### 1. FEASIBILITY VERDICT: CONDITIONAL_ADVANCE

**Rationale:** The v2 refined concept addresses the fatal CRDT ledger flaw and the six critical scientific gaps with a sound architectural resolution (Hybrid Deterministic Ledger). The core economic design (three-budget model, four-stream settlement, multi-rate settlement) remains sound and novel. However, the redesign introduces new complexity (EABS, reliable broadcast) that requires careful specification in DESIGN. The system is feasible but depends on successful resolution of the open research questions enumerated in Section 12.

The Council is unanimous that the v1 concept (pure CRDT) was not viable for advancement. The v2 concept (HDL with EABS) is viable, contingent on the hard gates below.

---

### 2. SCORES

| Dimension | Score | Justification |
|---|---|---|
| **Novelty** | **4/5** | The combination of CRDT-replicated reads with epoch-anchored batch settlement for an AI agent economy has no architectural precedent. Individual components (CRDTs, batch settlement, capability-weighted stake) exist in isolation but their integration is novel. Reduced from potential 5/5 because EABS resembles existing batch settlement systems (ACH, CLS) more than the original pure-CRDT design would have. |
| **Feasibility** | **3/5** | The v2 architecture is implementable with known techniques. EABS is essentially a deterministic state machine fed by reliable broadcast — well-understood. The main feasibility risk is the number of interacting mechanisms (three budgets × four streams × three settlement speeds × capability scores × capacity market) creating emergent behavior that is hard to predict without simulation. The open research questions (Section 12) are tractable but non-trivial. |
| **Impact** | **4/5** | If DSF works as designed, it provides a complete economic substrate for the Atrahasis agent system. It enables C3, C5, C6, and C7 to operate with well-defined economic semantics. The multi-rate settlement and intent-budgeted model are directly applicable to real AI agent workloads. The capacity market addresses a genuine need (resource allocation for heterogeneous AI tasks). |
| **Risk** | **6/10** | Moderate-high risk. The primary risks are: (a) complexity — the system has many interacting mechanisms and emergent behavior is hard to predict (MEDIUM-HIGH); (b) thin market viability — the capacity market may not achieve sufficient liquidity at launch (MEDIUM); (c) parameter sensitivity — many governance-tunable parameters (epoch duration, decay rates, position limits, etc.) that may require extensive simulation to set correctly (MEDIUM); (d) reliable broadcast assumptions — EABS depends on reliable broadcast, which has known limitations under adversarial network conditions (MEDIUM). Risk reduced from v1's ~8/10 because the fatal CRDT flaw is resolved. |

---

### 3. HARD GATES (Must-Pass for DESIGN)

**HG-1: EABS Protocol Specification**
The Epoch-Anchored Batch Settlement protocol must be fully specified, including: (a) reliable broadcast protocol selection with message complexity analysis, (b) deterministic ordering algorithm, (c) epoch batch format, (d) settlement function pseudocode, (e) failure recovery protocol. The DESIGN document must include a proof sketch that EABS preserves conservation under the assumed fault model.

**HG-2: Conservation Invariant Proof**
A formal proof (or rigorous proof sketch suitable for later formalization) that the CSO conservation invariant holds under EABS processing. This must cover: (a) normal operation, (b) epoch rollback/recovery, (c) pending state timeouts. The proof must address the gap identified in Science Assessment — runtime enforcement, not just theoretical correctness.

**HG-3: Three-Budget Equilibrium Model**
A quantitative economic model (analytical or simulation-based) demonstrating that the three-budget system reaches a stable equilibrium under realistic demand scenarios. The model must show that cross-budget friction mechanisms prevent arbitrage from collapsing the system to effective single-token behavior. If the model shows collapse, the DESIGN must either fix the friction mechanisms or honestly reduce to fewer budgets.

**HG-4: Capability Score Game-Theoretic Analysis**
A formal analysis showing that the capped logarithmic capability score is not gameable at a cost lower than direct AIC collateral acquisition. Specifically: the cost of farming capability_score from 1.0 to 3.0 (the cap) must exceed the AIC value of the resulting 3x stake amplification. If this condition fails, the multiplier cap must be reduced until it holds.

**HG-5: Capacity Market Minimum Viable Scale**
Determination (via simulation or analytical model) of the minimum number of capacity providers required for the market to function without protocol intervention (bootstrap capacity provider). The DESIGN must include a credible plan for reaching this scale and a timeline for sunsetting bootstrap provisions.

---

### 4. REQUIRED ACTIONS (Must Be Incorporated in DESIGN)

**RA-1: Reliable Broadcast Fault Model**
Specify the exact fault model (crash-fault, Byzantine, partial synchrony, etc.) under which EABS operates. This determines the reliable broadcast protocol choice and the system's actual resilience guarantees. Do not leave this as "to be determined."

**RA-2: Parameter Sensitivity Analysis**
For each governance-tunable parameter (epoch duration, PC decay rate, CS position limits, capability score cap, slashing schedule, challenge bond percentage, etc.), provide: (a) recommended initial value, (b) sensitivity analysis (what breaks if the parameter is 2x or 0.5x), (c) governance adjustment procedure.

**RA-3: Economic Simulation Scenarios**
Extend the existing E1-E7 scenarios to include: (E8) thin capacity market with <10 providers, (E9) cross-budget arbitrage attempt, (E10) reputation laundering attempt, (E11) epoch boundary manipulation attempt. Each scenario must demonstrate that v2 protections are effective.

**RA-4: Integration Protocol Specifications**
For each integration point (C3, C5, C6, C7), specify the exact API surface: what data flows, at what frequency, with what consistency guarantees (CRDT-optimistic or EABS-settled), and what happens when the integration partner is unavailable.

**RA-5: Failure Mode Catalogue**
Enumerate at least 15 failure modes covering: node failures, network partitions, Byzantine nodes, EABS settlement failures, capacity market failures, and cross-layer integration failures. For each, specify detection mechanism, impact, and recovery procedure.

**RA-6: Migration Path from Bootstrap**
Specify how the system transitions from bootstrap phase (treasury-funded capacity provider, governance-set parameters) to steady-state operation (market-driven capacity, community governance). Include quantitative triggers for each transition.

---

### 5. MONITORING FLAGS (Watch Items, Not Blocking)

**MF-1: CRDT Read-Path Staleness**
Monitor: The gap between CRDT-optimistic balances and EABS-settled balances during normal operation. If the gap exceeds acceptable bounds (to be defined in DESIGN), the read path may mislead users. Watch for situations where optimistic reads lead to failed transactions at settlement time.

**MF-2: Reliable Broadcast Latency at Scale**
Monitor: As the network grows beyond 100 nodes, reliable broadcast message complexity may become a bottleneck. If EABS settlement latency exceeds epoch duration, the system cannot keep up. Evaluate whether the chosen reliable broadcast protocol scales to the target network size.

**MF-3: Secondary Market Formation for Protocol Credits**
Monitor: Despite friction mechanisms, secondary markets for PC-denominated services may emerge. Track whether PC-as-a-service arrangements appear and whether they undermine spam control effectiveness. Not blocking because the design explicitly accepts imperfect isolation, but watch for worst-case degradation.

**MF-4: Capacity Market Price Volatility**
Monitor: Epoch-to-epoch price swings in the capacity market. High volatility suggests insufficient liquidity or gaming. The progressive release mechanism (60/20/20) should dampen volatility, but verify empirically. If volatility exceeds 50% epoch-over-epoch, market design may need revision.

**MF-5: Governance Parameter Ossification**
Monitor: Whether governance actually adjusts parameters in response to changing conditions, or whether initial parameters become de facto permanent. Many of v2's protections depend on governance responsiveness (reserve pricing, bootstrap sunset, slashing schedule). If governance is inactive, these protections degrade.

**MF-6: Cross-Layer Settlement Dependency Chain**
Monitor: DSF settles rewards based on data from C3, C5, C6, and C7. If any upstream layer produces delayed or incorrect data, settlement quality degrades. Track data freshness and accuracy from each integration partner. Particular concern: C5 (PCVM) credibility scores feeding capability_score — if C5 is compromised, DSF's staking model is undermined.

---

### COUNCIL STATEMENT

The Deterministic Settlement Fabric v2.0 represents a sound and novel economic substrate for the Atrahasis agent system. The critical intervention — replacing the pure-CRDT ledger with the Hybrid Deterministic Ledger — resolves the fatal architectural flaw that would have prevented v1 from functioning as a reliable financial layer. The remaining design is ambitious but grounded in well-understood mechanisms (batch settlement, auction markets, graduated penalties) adapted to the novel domain of AI agent economies.

The Council advances DSF v2.0 to DESIGN with the five hard gates enumerated above. Failure to satisfy any hard gate at DESIGN stage will trigger a return to FEASIBILITY for re-evaluation.

**VERDICT: CONDITIONAL_ADVANCE**

Scores: Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10.

---

*End of C8 Feasibility Stage — Tasks 1, 2, and 3 complete.*