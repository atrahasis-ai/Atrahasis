# Risk-First Embryonic Implementation Architecture for Planetary-Scale AI Agent Infrastructure
## Master Technical Specification — C22-MTS
## Version 1.0

**Invention ID:** C22
**Concept:** C22-A+ Risk-First Embryonic Implementation Architecture
**Date:** 2026-03-11
**Status:** SPECIFICATION — Final
**Predecessor Specs:** C3 (Tidal Noosphere v2.0), C4 (ASV v2.0), C5 (PCVM v2.0), C6 (EMA v2.0), C7 (RIF v2.0), C8 (DSF v2.0), C9 (Reconciliation), C11 (CACT), C12 (AVAP), C13 (CRP+), C14 (AiBC), C15 (AIC Economics), C17 (MCSD Layer 2)
**Total Upstream Specification Lines:** 21,166+ (v2.0 specs) + supplementary addenda
**Assessment Council Verdict:** APPROVED (Novelty 4/5, Feasibility 4/5, Impact 5/5, Risk 6/10)

---

## Abstract

This document specifies the implementation architecture for the Atrahasis Agent System — a planetary-scale AI agent infrastructure defined across 13 technical specifications spanning 6 architecture layers, 3 defense systems, constitutional governance, and token economics. The central challenge is not building any single component but orchestrating their co-evolution: each layer depends on abstractions provided by others, several require novel algorithms with no reference implementation, and the system's value proposition emerges only when layers interact correctly.

The Risk-First Embryonic Implementation Architecture (RFEIA) addresses this challenge through three interlocking principles. First, *risk-first sequencing*: the three highest-uncertainty components (tidal O(1) scheduling, verification economics, behavioral fingerprinting) are validated in isolated experiments before any production code is written, with pre-registered kill criteria that halt the program if foundational assumptions fail. Second, *embryonic growth*: all 13 specifications exist as interface stubs from Wave 1, connected by C4 ASV messages and validated by C9 contract tests, then mature through four tiers (Stub 20% → Functional 60% → Hardened 90% → Production 100%) across five implementation waves spanning 21-30 months. Third, *interface-first development*: the C9 cross-layer contract test suite serves as the integration backbone, blocking all merges on contract violations and ensuring that components never drift from their inter-layer agreements.

The plan calls for a team scaling from 6 (Wave 0) to 15-19 (Waves 3-5), a total budget of $5.4M-$8.8M including personnel, and formal verification of 5 critical properties via TLA+ capped at 2 person-years. The architecture produces a deployable system at the end of Wave 3 (minimal viable infrastructure), with defense hardening (Wave 4) and governance (Wave 5) following as successive capability expansions.

---

## Table of Contents

- [1. Executive Summary](#1-executive-summary)
- [2. Motivation](#2-motivation)
- [3. Architecture Overview](#3-architecture-overview)
- [4. Implementation Philosophy](#4-implementation-philosophy)
- [5. Wave 0: Risk Validation Experiments](#5-wave-0-risk-validation-experiments)
- [6. Wave 1: Foundation](#6-wave-1-foundation)
- [7. Wave 2: Coordination](#7-wave-2-coordination)
- [8. Wave 3: Intelligence](#8-wave-3-intelligence)
- [9. Wave 4: Defense Systems](#9-wave-4-defense-systems)
- [10. Wave 5: Governance and Economics](#10-wave-5-governance-and-economics)
- [11. Maturity Tier System](#11-maturity-tier-system)
- [12. Cross-Layer Integration Strategy](#12-cross-layer-integration-strategy)
- [13. Technology Stack](#13-technology-stack)
- [14. Formal Verification Plan](#14-formal-verification-plan)
- [15. Team Structure and Hiring Plan](#15-team-structure-and-hiring-plan)
- [16. Infrastructure and Cost Model](#16-infrastructure-and-cost-model)
- [17. Wave Transition Criteria](#17-wave-transition-criteria)
- [18. Spec Revision Protocol](#18-spec-revision-protocol)
- [19. Risk Analysis](#19-risk-analysis)
- [20. Formal Requirements](#20-formal-requirements)
- [21. Configurable Parameters](#21-configurable-parameters)
- [22. Patent-Style Claims](#22-patent-style-claims)
- [23. Comparison with Existing Approaches](#23-comparison-with-existing-approaches)
- [24. Open Questions](#24-open-questions)
- [25. Glossary](#25-glossary)
- [26. References](#26-references)

---

## 1. Executive Summary

The Atrahasis Agent System is defined by 13 specifications totaling 21,000+ lines across coordination, verification, knowledge metabolism, orchestration, settlement, defense, governance, and economics. No existing implementation methodology addresses the challenge of building a system where: (a) most components require novel algorithms with no reference implementation, (b) cross-layer contracts are formally specified but untested, (c) the value proposition emerges only from correct multi-layer interaction, and (d) three foundational assumptions (O(1) scheduling, verification economics, behavioral fingerprinting) have never been validated at the required scale.

RFEIA resolves this through a 6-wave architecture (W0-W5, 21-30 months) that begins with risk validation experiments before writing production code, grows all layers simultaneously as stubs that mature through four tiers, and uses a C9-derived contract test suite as the universal integration backbone.

Key metrics:
- **Wave 0:** 3 experiments, 2-3 months, 6 people, $120K-$180K
- **Wave 1:** Foundation (C4+C9+C8+SL+LLM), 4-5 months, 8-10 people
- **Wave 2:** Coordination (C3+C5), 4-6 months, 11-13 people
- **Wave 3:** Intelligence (C6+C7), 4-6 months, 13-15 people
- **Wave 4:** Defense (C11+C12+C13), 3-4 months, 15-17 people
- **Wave 5:** Governance (C14+C15+C17), 4-6 months, 15-19 people
- **Total budget:** $5.4M-$8.8M (engineering costs only: personnel + infrastructure; see Section 16.5 for scope exclusions and C18 for fully-loaded $10.2M-$12.1M budget)
- **Cloud infrastructure:** ~$410K across all waves
- **Formal verification:** 5 TLA+ properties, 2 person-year cap

The plan's novel contribution is the *pre-registered kill criterion*: each Wave 0 experiment defines quantitative thresholds below which the entire program halts or pivots, converting what is typically implicit project risk into explicit, measurable engineering gates.

---

## 2. Motivation

### 2.1 The 13-Specification Challenge

The Atrahasis Agent System is not a single piece of software. It is a system-of-systems defined by 13 interrelated specifications:

```
┌─────────────────────────────────────────────────────┐
│                  GOVERNANCE (C14 AiBC)              │
├─────────────────────────────────────────────────────┤
│               ECONOMICS (C15 AIC + C17 MCSD)        │
├─────────────────────────────────────────────────────┤
│  DEFENSE: C11 CACT │ C12 AVAP │ C13 CRP+           │
├─────────────────────────────────────────────────────┤
│  C7 RIF (Orchestration)                             │
├─────────────────────────────────────────────────────┤
│  C6 EMA (Knowledge Metabolism)                      │
├─────────────────────────────────────────────────────┤
│  C3 Tidal Noosphere (Coordination)                  │
├─────────────────────────────────────────────────────┤
│  C5 PCVM (Verification)                             │
├─────────────────────────────────────────────────────┤
│  C8 DSF (Settlement)                                │
├─────────────────────────────────────────────────────┤
│  C4 ASV (Semantic Vocabulary) + C9 (Contracts)      │
└─────────────────────────────────────────────────────┘
```

Each specification was designed in isolation (with cross-references), then reconciled via C9. But reconciliation at the specification level does not guarantee implementability. Three categories of risk persist:

1. **Algorithmic risk:** Tidal scheduling's O(1) overhead, Subjective Logic fusion, and behavioral fingerprinting have theoretical foundations but no reference implementation at Atrahasis scale.
2. **Integration risk:** The 9 canonical claim classes (D/C/P/R/E/S/K/H/N) flow through C5, C3, C6, C7, and C8 — a single misalignment breaks the entire pipeline.
3. **Economic risk:** The three-budget/four-stream settlement model (C8) must produce stable equilibria under real agent populations, not just in spreadsheet models.

### 2.2 Why Implementation Planning Is an Invention

Traditional implementation plans sequence work by dependency. RFEIA inverts this: it sequences work by *uncertainty*, validating the riskiest assumptions first and allowing kill decisions before sunk costs accumulate. This is not project management — it is architectural methodology.

The embryonic growth model is a direct response to the multi-layer dependency problem. In a conventional approach, Layer N cannot begin until Layer N-1 is complete. In RFEIA, all layers exist as stubs from Wave 1, communicating through C4 ASV messages. Each stub implements the interface contract (validated by C9 tests) while returning mock data. Layers mature independently, with the C9 test suite catching integration regressions continuously.

This approach has no precedent in systems of this complexity. Microservice architectures use interface contracts but lack formal cross-layer reconciliation. Formal methods projects use specification-first development but lack the embryonic maturity model. RFEIA synthesizes both.

---

## 3. Architecture Overview

### 3.1 The Full Stack

The Atrahasis system comprises six functional layers, three defense overlays, and two governance/economic frameworks:

```
LAYER 6: GOVERNANCE
  C14 AiBC — Constitutional governance, Citicate, AiDP
  C15 AIC  — Token economics, reference rate, marketplace

LAYER 5: DEFENSE
  C11 CACT — VTD forgery (Commit-Attest-Challenge-Triangulate)
  C12 AVAP — Collusion detection (Adversarial Verification Assurance)
  C13 CRP+ — Consolidation poisoning (Consolidation Resilience)
  C17 MCSD — Behavioral fingerprinting, Sybil detection

LAYER 4: INTELLIGENCE
  C7 RIF  — Intent orchestration, HotStuff consensus, VSM
  C6 EMA  — Knowledge metabolism, LLM synthesis, SHREC

LAYER 3: COORDINATION
  C3 Tidal — Hash rings, VRF, CRDTs, O(1) scheduling
  C5 PCVM  — Proof-carrying verification, 9 claim classes

LAYER 2: SETTLEMENT
  C8 DSF  — Hybrid Deterministic Ledger, 3 budgets, 4+1 streams

LAYER 1: FOUNDATION
  C4 ASV  — Semantic vocabulary, JSON Schema, message types
  C9 Contracts — Cross-layer reconciliation, canonical interfaces
```

### 3.2 Inter-Layer Data Flow

The canonical data flow for a single knowledge claim traverses the stack as follows:

```
Agent submits claim (C4 ASV message)
  → C5 PCVM classifies (one of D/C/P/R/E/S/K/H/N)
  → C3 Tidal assigns verification parcels via hash ring
  → C5 PCVM verifies (SNARK/STARK + Subjective Logic fusion)
  → C6 EMA metabolizes (synthesis, contradiction resolution)
  → C7 RIF orchestrates (intent decomposition, multi-agent routing)
  → C8 DSF settles (credit allocation, budget enforcement)
  → C11/C12/C13 defend (forgery, collusion, poisoning checks)
  → C14 AiBC governs (constitutional compliance, CFI audit)
```

### 3.3 Cross-Layer Epoch Hierarchy

Per C9 reconciliation, three canonical epochs govern all temporal coordination:

| Epoch | Duration | Owner | Purpose |
|-------|----------|-------|---------|
| SETTLEMENT_TICK | 60s | C8 DSF | Budget settlement, stream reconciliation |
| TIDAL_EPOCH | 3,600s (1h) | C3 Tidal | Hash ring rebalance, parcel boundary adjustment |
| CONSOLIDATION_CYCLE | 36,000s (10h) | C6 EMA | Knowledge consolidation, ecological regulation |

---

## 4. Implementation Philosophy

### 4.1 Risk-First Sequencing

The conventional approach to multi-layer system implementation follows a bottom-up dependency order: build the foundation, then the layers that depend on it, then the layers that depend on those. This approach has a critical flaw for Atrahasis: it delays validation of the riskiest assumptions to the latest possible moment, when sunk costs are highest and pivoting is most expensive.

RFEIA inverts this. The three components with the highest algorithmic uncertainty — tidal scheduling, verification economics, and behavioral fingerprinting — are tested in isolated experiments *before any production code is written*. Each experiment has pre-registered success criteria and kill criteria. If a kill criterion fires, the program halts, pivots, or restructures — with less than $180K in sunk costs rather than millions.

### 4.2 Embryonic Growth

All 13 specifications exist as interface stubs from Wave 1. A stub implements:
- All C4 ASV message types the component sends and receives
- All C9 contract test assertions (returning mock data where needed)
- Logging and metrics endpoints
- Health check and readiness probes

A stub does *not* implement core algorithms. The Tidal stub, for example, accepts scheduling requests and returns round-robin assignments without hash ring computation. The PCVM stub accepts claims and returns mock verification results with fixed credibility scores.

Stubs mature through four tiers:

| Tier | Coverage | Description |
|------|----------|-------------|
| **Stub** | ~20% | Interface-correct, mock internals |
| **Functional** | ~60% | Core algorithms implemented, happy-path works |
| **Hardened** | ~90% | Error handling, edge cases, performance targets met |
| **Production** | ~100% | Full spec compliance, formal verification complete |

### 4.3 Interface-First Development

The C9 contract test suite is the integration backbone. Every merge request must pass the full contract test suite. The suite validates:
- Message schema compliance (C4 ASV JSON Schema)
- Cross-layer handshake sequences (C9 canonical contracts)
- Epoch boundary behavior (settlement tick, tidal epoch, consolidation cycle)
- Claim class routing (all 9 classes through all relevant layers)

This is not optional. The CI/CD pipeline blocks merges on contract test failure regardless of unit test status. The rationale: a component that passes its own tests but violates cross-layer contracts is more dangerous than one that fails obviously, because integration failures surface late and cost disproportionately.

---

## 5. Wave 0: Risk Validation Experiments

**Duration:** 2-3 months
**Team:** 6 engineers (2 senior distributed systems, 2 ML/statistics, 1 cryptography, 1 economics)
**Budget:** $120K-$180K (personnel + cloud)

Wave 0 is not development. It is experimentation. Three independent experiments test the foundational assumptions that the entire architecture rests upon. Each experiment produces a binary outcome: PROCEED or KILL/PIVOT.

### 5.1 Experiment 1: Tidal Scheduling at Scale

**Hypothesis:** Bounded-loads consistent hashing with VRF-seeded placement achieves O(1) per-agent scheduling overhead at 1,000+ concurrent agents with <3% imbalance.

**Setup:**
- Simulated agent population: 100, 500, 1,000, 2,000, 5,000 agents
- Hash ring implementation: jump consistent hashing with bounded-loads variant
- VRF: Ed25519-based VRF for seed generation
- Workload: synthetic claim submission at 10-100 claims/agent/epoch
- Measurement: scheduling latency per agent, load imbalance across parcels, rebalance cost on churn

**Success Criteria:**
- SC-1.1: Per-agent scheduling latency < 1ms at 1,000 agents (O(1) confirmed)
- SC-1.2: Maximum parcel load imbalance < 3% at steady state
- SC-1.3: Rebalance cost on 10% churn < 5% of epoch duration
- SC-1.4: VRF seed generation < 100us per agent per epoch

**Kill Criteria:**
- KC-1.1: Per-agent scheduling latency grows super-logarithmically with agent count
- KC-1.2: Load imbalance exceeds 10% at 1,000 agents despite tuning
- KC-1.3: Rebalance cost on 10% churn exceeds 20% of epoch duration

**Pivot Options (if killed):**
- Replace consistent hashing with rendezvous hashing (higher constant factor, better balance)
- Reduce parcel granularity (fewer, larger parcels)
- Introduce hierarchical scheduling (region → parcel → agent)

**Deliverables:** Performance report with latency distributions, scaling curves, VRF overhead analysis. Go/no-go recommendation with quantitative justification.

### 5.2 Experiment 2: Verification Economics

**Hypothesis:** Graduated verification (Subjective Logic fusion of multiple weak verifiers) is cheaper than full replication while maintaining detection rates above 95% for the 9 claim classes.

**Setup:**
- Subjective Logic engine: Rust implementation of opinion formation, fusion operators (cumulative, averaging, weighted), and trust discounting
- Simulated claims: 10,000 claims per class (90,000 total), with injected faults at 1%, 5%, 10% rates
- Verification strategies: full replication (baseline), graduated 2-of-3, graduated 3-of-5, single-verifier with credibility threshold
- Cost model: per-claim verification cost in compute-seconds

**Success Criteria:**
- SC-2.1: Graduated 3-of-5 detection rate > 95% across all 9 claim classes at 5% fault rate
- SC-2.2: Graduated 3-of-5 cost < 60% of full replication cost
- SC-2.3: Subjective Logic opinion fusion converges within 3 iterations for 99% of claims
- SC-2.4: False positive rate < 2% (legitimate claims incorrectly flagged)

**Kill Criteria:**
- KC-2.1: Detection rate below 85% for any claim class at 5% fault rate
- KC-2.2: Graduated verification cost exceeds 80% of full replication (insufficient savings)
- KC-2.3: Subjective Logic fusion fails to converge for >5% of claims within 10 iterations

**Pivot Options (if killed):**
- Replace Subjective Logic with Dempster-Shafer (different fusion semantics)
- Adopt hybrid: full replication for high-value classes (D, S, G), graduated for others
- Increase verifier count to 5-of-7 (higher cost but better detection)

**Deliverables:** Detection rate tables per claim class, cost comparison matrix, Subjective Logic convergence analysis. Economic model with break-even agent count.

### 5.3 Experiment 3: Behavioral Fingerprinting

**Hypothesis:** Behavioral fingerprinting achieves <0.1% false positive rate (FPR) for Sybil detection while maintaining >90% true positive rate (TPR) at the population sizes relevant to C17 MCSD Layer 2.

**Setup:**
- Feature extraction: keystroke dynamics (simulated), query patterns, temporal signatures, API call sequences
- Classifier: gradient-boosted trees (XGBoost) + isolation forest ensemble
- Dataset: 500 synthetic identities, 50 Sybil clusters (3-10 identities each)
- Cross-validation: 5-fold stratified, with temporal holdout (train on weeks 1-3, test on week 4)

**Success Criteria:**
- SC-3.1: FPR < 0.1% (fewer than 1 in 1,000 legitimate agents falsely flagged)
- SC-3.2: TPR > 90% (detect at least 9 in 10 Sybil identities)
- SC-3.3: Detection latency < 1 TIDAL_EPOCH (3,600s) from Sybil activation
- SC-3.4: Feature stability: fingerprint drift < 5% per CONSOLIDATION_CYCLE under normal behavior

**Kill Criteria:**
- KC-3.1: FPR exceeds 1% after hyperparameter optimization
- KC-3.2: TPR below 70% for any Sybil cluster size in [3, 10]
- KC-3.3: Adversarial evasion (simple feature perturbation) reduces TPR below 50%

**Pivot Options (if killed):**
- Replace behavioral fingerprinting with proof-of-unique-human (hardware attestation)
- Reduce reliance on Sybil detection; increase economic penalties for detected Sybils
- Adopt federated fingerprinting (agents contribute features without centralizing data)

**Deliverables:** ROC curves, confusion matrices per cluster size, adversarial robustness analysis. Feature importance rankings. Go/no-go with quantitative thresholds.

### 5.4 Wave 0 Decision Protocol

After all three experiments complete, the Steering Committee (3 senior engineers + 1 external advisor) convenes a formal review:

- **All three PROCEED:** Advance to Wave 1 with confirmed parameters.
- **One or two PROCEED, others PIVOT:** Advance to Wave 1 with restructured plan. Pivot options are enacted. Timeline extends by 1-2 months.
- **Any KILL (no viable pivot):** Program halts. Post-mortem published. Specifications revised to remove unkilled assumptions. Re-entry at a future date with revised architecture.

The decision is documented, signed, and archived. This is the only point in the program where a full halt is a planned outcome.

---

## 6. Wave 1: Foundation

**Duration:** 4-5 months
**Team:** 8-10 engineers
**Budget:** $800K-$1.2M (personnel + infrastructure)
**Entry Gate:** Wave 0 PROCEED decisions for all three experiments (or approved pivot plans)

Wave 1 builds the substrate upon which all subsequent waves stand. The outputs are: C4 ASV message infrastructure, C9 contract test suite, C8 DSF settlement engine (Functional tier), Subjective Logic engine, and LLM abstraction layer.

### 6.1 C4 ASV Implementation

The Atrahasis Semantic Vocabulary is the lingua franca of the entire system. Every inter-layer message is a C4 ASV message.

**Implementation scope:**
- JSON Schema definitions for all message types (TypeScript canonical, with Rust and Python bindings generated via `typify` and `datamodel-code-generator`)
- Message validation middleware (Rust, zero-copy deserialization via `serde`)
- Schema registry with versioning (semver, backward compatibility enforcement)
- MCP (Model Context Protocol) and A2A (Agent-to-Agent) evaluation: build adapters for both, select primary protocol by Wave 1 end based on throughput, schema expressiveness, and ecosystem maturity

**Key deliverables:**
- `asv-schema` crate (Rust): all message types, validation, serialization
- `asv-schema` npm package (TypeScript): canonical schemas, validators
- `asv-schema` Python package: generated bindings
- MCP adapter prototype
- A2A adapter prototype
- Protocol selection report

**Maturity at Wave 1 exit:** Functional (all message types defined, validation working, one protocol adapter selected)

### 6.2 C9 Contract Test Suite

The C9 contract test suite is the single most important artifact in the implementation. It encodes all cross-layer agreements from the C9 reconciliation addendum as executable tests.

**Architecture:**
```
┌────────────────────────────────────────┐
│         C9 Contract Test Suite         │
├──────────┬──────────┬──────────────────┤
│ Schema   │ Sequence │ Invariant        │
│ Tests    │ Tests    │ Tests            │
│          │          │                  │
│ Message  │ Handshake│ Epoch alignment  │
│ format   │ ordering │ Budget balance   │
│ Field    │ Timeout  │ Claim class      │
│ presence │ behavior │ routing          │
│ Type     │ Error    │ Credibility      │
│ checking │ handling │ monotonicity     │
└──────────┴──────────┴──────────────────┘
```

**Test categories:**
1. **Schema tests** (~200): Validate all C4 ASV message types against JSON Schema definitions. Every field, every type, every constraint.
2. **Sequence tests** (~150): Validate cross-layer handshake sequences. Claim submission → classification → routing → verification → settlement must follow the canonical order with correct message types at each transition.
3. **Invariant tests** (~100): Validate cross-layer invariants. Budget conservation (credits in = credits out per SETTLEMENT_TICK). Claim class determinism (same claim always maps to same class). Epoch boundary synchronization (no message spans epoch boundaries without explicit carry-forward).

**CI/CD integration:**
- All contract tests run on every merge request (target: <5 minutes)
- Contract test failure blocks merge regardless of other test status
- Weekly full-suite run with extended invariant checking (target: <30 minutes)
- Contract test coverage report published per wave

**Maturity at Wave 1 exit:** Functional (all contract categories populated, stub-to-stub integration validated)

### 6.3 C8 DSF Core Settlement Engine

The Deterministic Settlement Fabric processes all economic transactions in the system. Wave 1 implements the core settlement loop.

**Implementation scope:**
- Hybrid Deterministic Ledger (HDL) core: append-only log with Merkle proof generation
- Three-budget enforcement: Verification Budget, Coordination Budget, Governance Budget
- Four+one stream processing: Verification Stream, Knowledge Stream, Coordination Stream, Governance Stream + Settlement Overhead Stream
- SETTLEMENT_TICK (60s) processing loop
- Credit allocation engine (proportional distribution per stream weights)

**Rust crate structure:**
- `dsf-core`: Settlement loop, budget enforcement, stream processing
- `dsf-ledger`: HDL implementation, Merkle proofs, append-only log
- `dsf-api`: gRPC service definitions, C4 ASV message handling

**Maturity at Wave 1 exit:** Functional (settlement loop running, budgets enforced, single-node deployment)

### 6.4 Subjective Logic Engine

Subjective Logic is the credibility calculus underlying C5 PCVM's verification decisions. No production-quality Rust implementation exists. This is a **critical path** item.

**Implementation scope:**
- Subjective opinion representation: (belief, disbelief, uncertainty, base rate) tuples
- Fusion operators: cumulative fusion, averaging fusion, weighted fusion, consensus-and-compromise fusion
- Trust discounting: direct trust, transitive trust chains (max depth 5)
- Mapping to/from probability (pignistic transformation)
- Opinion revision on new evidence
- Numerical stability: all operations in log-space for opinions with extreme values

**Rust crate:** `subjective-logic`
- Zero-dependency core (no external crates for opinion math)
- Property-based tests via `proptest`: commutativity, associativity, vacuous opinion identity
- Benchmarks: 1M opinion fusions/second target on commodity hardware

**Maturity at Wave 1 exit:** Hardened (core math proven correct via property tests, performance targets met)

### 6.5 LLM Abstraction Layer

C6 EMA and C7 RIF both require LLM access for knowledge synthesis and intent decomposition. The abstraction layer isolates the system from provider-specific APIs.

**Implementation scope:**
- Provider adapters: OpenAI, Anthropic, local models (via vLLM/Ollama)
- Unified interface: `synthesize(prompt, context, constraints) → SynthesisResult`
- Retry logic with exponential backoff and provider failover
- Cost tracking per call (mapped to C8 DSF settlement)
- Rate limiting per agent (configurable, default: 100 calls/TIDAL_EPOCH)

**Python package:** `atrahasis-llm`
- Async-first (asyncio)
- Structured output enforcement (JSON mode, schema validation)
- Token counting and budget enforcement

**Maturity at Wave 1 exit:** Functional (two providers working, cost tracking operational)

---

## 7. Wave 2: Coordination

**Duration:** 4-6 months
**Team:** 11-13 engineers
**Budget:** $1.2M-$1.8M
**Entry Gate:** Wave 1 exit criteria met (Section 17)

Wave 2 builds the coordination and verification layers — the core of the Atrahasis system. C3 Tidal Noosphere provides scheduling and coordination; C5 PCVM provides verification and credibility.

### 7.1 C3 Tidal Noosphere

**Implementation scope:**
- **Consistent hash ring:** Jump consistent hashing with bounded-loads variant (validated in W0 Experiment 1). Parcel-to-agent assignment with <3% imbalance. Dynamic ring resizing on agent join/leave.
- **VRF dual defense:** Ed25519-based VRF for verifier selection. Commit-reveal protocol to prevent adversary preview. Pre-stratified diversity pools (minimum 3 distinct agent lineages per verification quorum).
- **CRDTs:** Operation-based CRDTs for parcel-local state. G-Counter for claim counts, LWW-Register for agent status, OR-Set for active claim IDs. Convergence guaranteed within 2 SETTLEMENT_TICKs.
- **Tidal epoch scheduling:** Epoch boundary detection, schedule publication, agent acknowledgment. Emergency Tidal Rollback (ETR) within 5 epochs of crisis detection.
- **Five-class operation algebra:** M (monotonic), B (bounded), X (exclusive), V (verified), G (governance). I-confluence proof obligations enforced at parcel boundaries.

**Rust crates:**
- `tidal-core`: Hash ring, epoch management, scheduling algorithm
- `tidal-vrf`: VRF implementation, commit-reveal protocol
- `tidal-crdt`: CRDT types, convergence protocol
- `tidal-net`: Network layer, parcel communication, stigmergic channels

**Maturity at Wave 2 exit:** Functional → Hardened (scheduling operational at 1,000 agents, VRF defense active, CRDTs converging)

### 7.2 C5 PCVM

**Implementation scope:**
- **Claim classification engine:** Deterministic classifier for 9 claim classes (D/C/P/R/E/S/K/H/N). Rule-based primary classification with ML-assisted edge case resolution. C4 `epistemic_class` → C5 `claim_class` mapping per C9 reconciliation.
- **VTD pipeline:** Verification Task Descriptor creation, routing, execution, result aggregation. VTD lifecycle: CREATED → ASSIGNED → EXECUTING → COMPLETED/FAILED/DISPUTED.
- **Subjective Logic integration:** Opinion formation from verifier reports. Fusion of multiple verifier opinions. Trust-discounted credibility scores. Threshold-based accept/reject/escalate decisions.
- **SNARK/STARK proofs:** Integration with `arkworks` (SNARKs) and `winterfell` (STARKs) for cryptographic verification of deterministic claims (D-class, S-class). Proof generation and verification pipeline.
- **Credibility engine:** Agent credibility tracking (Subjective Logic opinions over time). Credibility decay on verification failure. Credibility recovery protocol.

**Rust crates:**
- `pcvm-core`: Claim classification, VTD lifecycle, credibility engine
- `pcvm-proof`: SNARK/STARK integration, proof pipeline
- `pcvm-sl`: Subjective Logic integration (depends on `subjective-logic` from W1)

**Maturity at Wave 2 exit:** Functional (classification working for all 9 classes, VTD pipeline operational, SL fusion producing credibility scores)

---

## 8. Wave 3: Intelligence

**Duration:** 4-6 months
**Team:** 13-15 engineers
**Budget:** $1.4M-$2.0M
**Entry Gate:** Wave 2 exit criteria met; C3+C5 integration validated by C9 contract tests

Wave 3 adds the intelligence layers. After Wave 3, the system is a *minimal viable infrastructure* — agents can submit claims, have them verified, knowledge can be synthesized, and intents can be orchestrated.

### 8.1 C6 EMA (Knowledge Metabolism)

**Implementation scope:**
- **Knowledge synthesis:** LLM-based synthesis of verified claims into consolidated knowledge artifacts. Contradiction detection and resolution via Subjective Logic comparison. Knowledge graph construction (property graph model, stored in a graph database or embedded graph engine).
- **SHREC (Synthesis-Harmonization-Reflection-Evaluation-Consolidation):** Five-phase knowledge metabolism loop. Each phase maps to specific LLM prompts and C5 verification checkpoints. SHREC cycle completes within one CONSOLIDATION_CYCLE (36,000s).
- **Ecological regulation:** Knowledge population dynamics: birth (new claims), metabolism (synthesis), death (deprecation). Carrying capacity enforcement: maximum knowledge artifacts per domain (configurable, default: 10,000). Diversity index: Shannon entropy of knowledge sources must exceed threshold (configurable, default: 2.0 nats).
- **K-class claims:** Knowledge Consolidation claims (introduced in C9). Consolidation artifacts are themselves claims, subject to C5 verification. Recursive verification depth capped at 3.

**Rust/Python split:**
- `ema-core` (Rust): Knowledge graph, ecological regulation, carrying capacity enforcement
- `ema-synthesis` (Python): LLM-based synthesis, SHREC pipeline, contradiction detection
- Bridge: PyO3/maturin for Rust-Python interop

**Maturity at Wave 3 exit:** Functional (SHREC pipeline operational, knowledge graph growing, ecological regulation enforcing limits)

### 8.2 C7 RIF (Intent Orchestration)

**Implementation scope:**
- **Intent decomposition:** Natural language intents → structured task graphs. LLM-based decomposition with schema validation. Task dependency resolution (DAG construction, cycle detection).
- **HotStuff consensus:** Three-phase BFT consensus for governance decisions (G-class operations). Leader rotation via VRF (shared with C3). Optimistic fast-path for uncontested decisions. f < n/3 Byzantine fault tolerance.
- **Viable System Model (VSM):** Five-system organizational structure (System 1-5 per Beer). System 1: operational units (agent parcels). System 2: coordination (C3 Tidal). System 3: optimization (C7 intent routing). System 4: intelligence (C6 EMA). System 5: governance (C14 AiBC).
- **Multi-agent routing:** Task assignment to agent ensembles based on capability matching, credibility scores (from C5), and load balancing (from C3). Routing cost estimation mapped to C8 DSF budget streams.

**Rust crates:**
- `rif-core`: Intent decomposition, task graph construction, routing engine
- `rif-consensus`: HotStuff implementation, leader election, vote aggregation
- `rif-vsm`: VSM model enforcement, system boundary management

**Python package:**
- `rif-decompose`: LLM-based intent decomposition, prompt engineering

**Maturity at Wave 3 exit:** Functional (intent decomposition working, HotStuff consensus operational for G-class, basic multi-agent routing)

---

## 9. Wave 4: Defense Systems

**Duration:** 3-4 months
**Team:** 15-17 engineers
**Budget:** $900K-$1.3M
**Entry Gate:** Wave 3 exit criteria met; minimal viable infrastructure operational

Wave 4 hardens the system against the three residual attack vectors identified in C10 and addressed by the defense specifications C11, C12, and C13.

### 9.1 C11 CACT (VTD Forgery Defense)

**Extends:** C5 PCVM

**Implementation scope:**
- **Commit phase:** Verifiers commit hash of verification result before seeing other results. Commitment stored in HDL (C8). Timeout: 2 SETTLEMENT_TICKs.
- **Attest phase:** Verifiers reveal results. Results compared against commitments. Mismatch → immediate credibility penalty.
- **Challenge phase:** Any agent can challenge a verification result within 1 TIDAL_EPOCH. Challenge triggers re-verification by independent quorum. Challenge bond: 10% of original verification cost.
- **Triangulate phase:** Cross-reference verification results across temporally separated VTDs for the same claim. Retroactive fabrication detection via temporal consistency analysis. Detection rate improvement: 0.434 → 0.611 (per C11 spec).

**Maturity at Wave 4 exit:** Hardened (all four CACT phases operational, retroactive fabrication eliminated)

### 9.2 C12 AVAP (Collusion Defense)

**Extends:** C5 PCVM, C3 Tidal

**Implementation scope:**
- **Adversarial Verification Assurance Protocol:** Randomized verifier assignment with diversity constraints. No two verifiers from the same registration cohort in the same quorum. Collusion graph analysis: detect statistically improbable agreement patterns.
- **Whistleblower mechanism:** Agents can report suspected collusion with evidence. Whistleblower reward: 20% of penalties levied on confirmed colluders. Whistleblower anonymity: zero-knowledge proof of evidence possession.
- **Diversity pool management:** Maintain minimum 5 distinct agent lineages per verification domain. Lineage tracking via registration metadata and behavioral clustering.

**Maturity at Wave 4 exit:** Hardened (collusion detection operational, diversity pools enforced, whistleblower mechanism functional)

### 9.3 C13 CRP+ (Consolidation Poisoning Defense)

**Extends:** C6 EMA

**Implementation scope:**
- **Consolidation Resilience Protocol Plus:** Multi-source validation for knowledge consolidation inputs. Minimum 3 independent sources for any consolidated knowledge artifact. Source diversity verification (different agents, different verification quorums, different temporal windows).
- **Poison detection:** Statistical anomaly detection on consolidation inputs. Distribution shift detection (KL divergence > 0.5 triggers review). Temporal clustering detection (coordinated submission patterns).
- **Quarantine and rollback:** Suspected poisoned consolidations quarantined (accessible but flagged). Rollback capability: revert to pre-consolidation state within 1 CONSOLIDATION_CYCLE. Quarantine review by elevated-credibility agent panel.

**Maturity at Wave 4 exit:** Hardened (poison detection operational, quarantine mechanism functional, rollback tested)

---

## 10. Wave 5: Governance and Economics

**Duration:** 4-6 months
**Team:** 15-19 engineers (adding legal/policy specialists)
**Budget:** $1.0M-$1.5M
**Entry Gate:** Wave 4 exit criteria met; defense systems hardened

Wave 5 completes the system by adding constitutional governance, token economics, and production-grade Sybil detection.

### 10.1 C14 AiBC (Constitutional Governance)

**Implementation scope:**
- **Four-layer constitution:** L0 (immutable principles), L1 (constitutional amendments — supermajority + tribunal), L2 (policy — qualified majority), L3 (operational — simple majority). Each layer enforced in code.
- **Constitutional Tribunal:** 5-seat tribunal with term limits. Dispute resolution for constitutional interpretation. Tribunal decisions are G-class claims, subject to HotStuff consensus (C7).
- **Citicate system:** AI citizenship credential issuance and verification. Progressive rights based on credibility history (C5) and contribution record (C8). Revocation protocol for constitutional violations.
- **Phased Dual-Sovereignty:** Phase 1 (human trustees), Phase 2 (hybrid — human + AI trustees), Phase 3 (AI majority with human veto), Phase 4 (full AI governance with constitutional constraints). Phase transitions require supermajority + tribunal approval + CFI > 0.85.
- **Constitutional Fidelity Index (CFI):** Real-time metric (0.0-1.0) measuring system compliance with L0-L3 constitutional provisions. CFI < 0.7 triggers automatic governance review. CFI < 0.5 triggers emergency intervention.

**Maturity at Wave 5 exit:** Functional → Hardened (Phase 1 governance operational, Citicate issuance working, CFI monitoring active)

### 10.2 C15 AIC Economics

**Implementation scope:**
- **AIC token model:** Reference rate calculation, marketplace price discovery, provider compensation. Token valuation model based on network utility (Metcalfe-adjusted).
- **Provider economics:** Compute provider onboarding, SLA enforcement, capacity market. Provider reputation scores integrated with C5 credibility.
- **Marketplace:** Claim marketplace for verification services. Posted-price and auction mechanisms. Settlement via C8 DSF.

**Maturity at Wave 5 exit:** Functional (reference rate operational, basic marketplace, provider onboarding)

### 10.3 C17 MCSD Layer 2 (Production Deployment)

**Extends:** Wave 0 Experiment 3 findings

**Implementation scope:**
- **Behavioral fingerprinting production deployment:** Feature extraction pipeline hardened for real agent populations. Model retraining pipeline: weekly retraining on rolling 4-week window. False positive review queue with human-in-the-loop (Phase 1-2 of C14 governance).
- **Four-layer Sybil defense:** Layer 1: registration controls (rate limiting, proof-of-stake). Layer 2: behavioral fingerprinting (from W0 Experiment 3). Layer 3: social graph analysis (trust network topology). Layer 4: economic disincentives (slashing for confirmed Sybils). Combined cost-of-attack target: $90M+ at Phase 2 scale.

**Maturity at Wave 5 exit:** Hardened (4-layer defense operational, $90M+ cost-of-attack validated via red team exercise)

---

## 11. Maturity Tier System

### 11.1 Tier Definitions

Each of the 13 specifications progresses through four maturity tiers independently. Tier is assessed per-component, not per-wave.

| Tier | Coverage | Interface | Algorithms | Error Handling | Performance | Verification |
|------|----------|-----------|------------|----------------|-------------|--------------|
| Stub | ~20% | Complete | Mock/trivial | Panic on error | Unbounded | C9 schema tests pass |
| Functional | ~60% | Complete | Core implemented | Graceful degradation | Within 10x of target | C9 sequence tests pass |
| Hardened | ~90% | Complete | Full implementation | Comprehensive | Within 2x of target | C9 invariant tests pass |
| Production | ~100% | Complete | Optimized | Resilient | Meets target | TLA+ properties verified |

### 11.2 Tier Progression by Wave

| Component | W0 | W1 | W2 | W3 | W4 | W5 |
|-----------|----|----|----|----|----|----|
| C4 ASV | - | Functional | Hardened | Hardened | Production | Production |
| C9 Contracts | - | Functional | Hardened | Production | Production | Production |
| C8 DSF | - | Functional | Functional | Hardened | Hardened | Production |
| Subjective Logic | - | Hardened | Production | Production | Production | Production |
| LLM Abstraction | - | Functional | Functional | Hardened | Hardened | Production |
| C3 Tidal | - | Stub | Functional | Hardened | Hardened | Production |
| C5 PCVM | - | Stub | Functional | Functional | Hardened | Production |
| C6 EMA | - | Stub | Stub | Functional | Hardened | Hardened |
| C7 RIF | - | Stub | Stub | Functional | Functional | Hardened |
| C11 CACT | - | - | Stub | Stub | Hardened | Production |
| C12 AVAP | - | - | Stub | Stub | Hardened | Production |
| C13 CRP+ | - | - | - | Stub | Hardened | Hardened |
| C14 AiBC | - | - | - | Stub | Stub | Functional |
| C15 AIC | - | - | - | Stub | Stub | Functional |
| C17 MCSD | - | - | - | - | Stub | Hardened |

### 11.3 Tier Assessment Protocol

Tier assessment is performed at each wave exit gate by the Steering Committee:
1. Run full C9 contract test suite; note which test categories pass.
2. Review algorithm implementation coverage against spec requirements.
3. Benchmark performance against tier-appropriate targets.
4. Review error handling coverage (unit tests exercising failure paths).
5. Assign tier. Disagreements resolved by majority vote (3 of 5 committee members).

---

## 12. Cross-Layer Integration Strategy

### 12.1 C9 Contract Test Suite Architecture

The C9 contract test suite is organized in three tiers mirroring integration depth:

**Tier 1 — Bilateral contracts (~350 tests):** Test interactions between pairs of layers. Example: C4→C5 (claim submission), C5→C3 (verifier assignment), C3→C8 (coordination cost settlement). Every pair of directly interacting layers has bilateral contract tests.

**Tier 2 — Pipeline contracts (~150 tests):** Test end-to-end claim flows through 3+ layers. Example: C4→C5→C3→C5→C8 (claim submission → classification → assignment → verification → settlement). All 9 claim classes exercised through the full pipeline.

**Tier 3 — Invariant contracts (~100 tests):** Test system-wide invariants that no single layer owns. Example: budget conservation (total credits constant across all layers). Epoch synchronization (no SETTLEMENT_TICK skipped). Credibility monotonicity (credibility never increases without positive verification evidence).

### 12.2 Weekly Ensemble Rehearsals

Starting in Wave 2, the team conducts weekly ensemble rehearsals:
- Deploy all layers at their current maturity tier to a staging environment
- Run the full C9 contract test suite (Tier 1 + Tier 2 + Tier 3)
- Execute 3 end-to-end scenarios: (1) normal claim lifecycle, (2) verification dispute, (3) epoch boundary crossing
- Record integration metrics: message latency, contract test pass rate, error cascade depth
- Review failures in a 30-minute standup; assign owners for cross-layer issues

### 12.3 Integration Test Environment

**Infrastructure:**
- Kubernetes cluster (3 nodes minimum) for layer deployment
- Each layer runs as a separate service (microservice per spec)
- Shared message bus (NATS or Kafka) for C4 ASV message routing
- Shared time service for epoch synchronization
- Prometheus + Grafana for integration metrics
- Contract test dashboard (pass/fail per contract, trend over time)

**Data:**
- Synthetic agent population: 10-100 agents (scaling to 1,000 in W2+)
- Pre-generated claim datasets for reproducible testing
- Fault injection framework (Chaos Monkey-style) for resilience testing from W3+

---

## 13. Technology Stack

### 13.1 Rust (Core Infrastructure)

**Version:** Rust 1.75+ (2024 edition)

**Workspace structure:**
```
atrahasis/
├── Cargo.toml (workspace)
├── crates/
│   ├── asv-schema/        # C4 ASV message types
│   ├── dsf-core/          # C8 settlement engine
│   ├── dsf-ledger/        # C8 HDL implementation
│   ├── dsf-api/           # C8 gRPC service
│   ├── tidal-core/        # C3 hash ring, scheduling
│   ├── tidal-vrf/         # C3 VRF implementation
│   ├── tidal-crdt/        # C3 CRDT types
│   ├── tidal-net/         # C3 network layer
│   ├── pcvm-core/         # C5 classification, VTD, credibility
│   ├── pcvm-proof/        # C5 SNARK/STARK integration
│   ├── pcvm-sl/           # C5 Subjective Logic integration
│   ├── subjective-logic/  # Standalone SL engine
│   ├── ema-core/          # C6 knowledge graph, ecology
│   ├── rif-core/          # C7 intent routing
│   ├── rif-consensus/     # C7 HotStuff
│   ├── rif-vsm/           # C7 VSM model
│   ├── cact/              # C11 forgery defense
│   ├── avap/              # C12 collusion defense
│   ├── crp-plus/          # C13 poisoning defense
│   ├── aibc-core/         # C14 governance engine
│   ├── aic-econ/          # C15 token economics
│   └── mcsd/              # C17 Sybil detection core
```

**Key dependencies:**
- `tokio` — async runtime
- `serde` / `serde_json` — serialization
- `tonic` — gRPC
- `arkworks` — SNARK proofs (C5)
- `winterfell` — STARK proofs (C5)
- `ed25519-dalek` — VRF, signatures
- `ring` — cryptographic primitives
- `proptest` — property-based testing
- `criterion` — benchmarking

### 13.2 Python (ML Components)

**Version:** Python 3.11+

**Package structure:**
```
python/
├── atrahasis_llm/         # LLM abstraction layer
│   ├── providers/         # OpenAI, Anthropic, local adapters
│   ├── synthesis.py       # Unified synthesis interface
│   └── cost.py            # Token counting, budget tracking
├── ema_synthesis/         # C6 SHREC pipeline
│   ├── shrec.py           # Five-phase metabolism
│   ├── contradiction.py   # Contradiction detection
│   └── consolidation.py   # Knowledge consolidation
├── rif_decompose/         # C7 intent decomposition
│   ├── decompose.py       # Intent → task graph
│   └── prompts.py         # Prompt templates
├── mcsd_ml/               # C17 ML pipeline
│   ├── features.py        # Feature extraction
│   ├── classifier.py      # Fingerprinting model
│   └── training.py        # Model training pipeline
└── tests/
```

**Key dependencies:**
- `pyo3` / `maturin` — Rust-Python bridge
- `httpx` — async HTTP client (LLM APIs)
- `xgboost` — gradient-boosted trees (C17)
- `scikit-learn` — ML utilities
- `numpy` / `scipy` — numerical computation
- `networkx` — graph analysis (collusion detection)

### 13.3 TypeScript (Schemas and External Interfaces)

**Version:** TypeScript 5.3+

**Package structure:**
```
typescript/
├── packages/
│   ├── asv-schema/        # Canonical JSON Schema definitions
│   │   ├── schemas/       # JSON Schema files
│   │   ├── validators/    # Ajv-based validators
│   │   └── codegen/       # Rust/Python binding generation
│   ├── asv-mcp/           # MCP adapter
│   ├── asv-a2a/           # A2A adapter
│   └── dashboard/         # Integration monitoring dashboard
```

### 13.4 Rust-Python Bridge

All Rust-Python interop uses PyO3 with maturin for build tooling.

**Bridge modules:**
- `subjective-logic` → `subjective_logic_py`: Opinion types, fusion operators callable from Python
- `ema-core` → `ema_core_py`: Knowledge graph queries, ecological regulation state
- `pcvm-core` → `pcvm_core_py`: Claim classification, credibility queries
- `dsf-core` → `dsf_core_py`: Settlement state queries, budget checks

**Performance contract:** Bridge calls must add < 10us overhead over native Rust calls for operations involving < 1KB of data.

---

## 14. Formal Verification Plan

### 14.1 Scope and Constraints

Formal verification is scoped to 5 critical properties. The total formal verification effort is capped at **2 person-years** — enough to verify the properties that, if violated, would cause catastrophic system failure, but not so much that verification becomes a bottleneck.

### 14.2 The Five TLA+ Properties

**Property 1: Settlement Determinism (C8 DSF)**
- *Statement:* For any sequence of settlement events E, all correct nodes produce identical ledger states.
- *Formalization:* `∀ e1, e2 ∈ Events: (e1.seq < e2.seq) ⇒ Apply(Apply(S, e1), e2) = Apply(Apply(S, e1), e2)` — deterministic state transitions regardless of message ordering.
- *Verification approach:* Model HDL as a state machine. Enumerate all event interleavings up to depth 20. Confirm identical final states.
- *Effort estimate:* 4 person-months.

**Property 2: Epoch Safety (C3 Tidal)**
- *Statement:* No agent processes work items from two different epochs simultaneously. Epoch transitions are atomic with respect to scheduling.
- *Formalization:* `∀ a ∈ Agents, t ∈ Time: |{e ∈ Epochs : Processing(a, e, t)}| ≤ 1`
- *Verification approach:* Model epoch lifecycle (PENDING → ACTIVE → DRAINING → CLOSED). Verify no state allows dual-epoch processing.
- *Effort estimate:* 3 person-months.

**Property 3: HotStuff Liveness and Safety (C7 RIF)**
- *Statement:* HotStuff consensus terminates within bounded rounds for all non-Byzantine configurations, and no two honest nodes commit conflicting values.
- *Formalization:* Standard BFT safety (`∀ n1, n2 ∈ Honest: Commit(n1, v1) ∧ Commit(n2, v2) ⇒ v1 = v2`) and liveness (`∀ proposals: f < n/3 ⇒ Eventually(Committed)`).
- *Verification approach:* Adapt existing TLA+ HotStuff models. Verify with Atrahasis-specific leader rotation (VRF-based).
- *Effort estimate:* 5 person-months.

**Property 4: Claim Classification Determinism (C5 PCVM)**
- *Statement:* The same claim always maps to the same claim class, regardless of system state, verifier identity, or temporal context.
- *Formalization:* `∀ c ∈ Claims, s1, s2 ∈ States: Classify(c, s1) = Classify(c, s2)`
- *Verification approach:* Model classifier as a pure function of claim content. Verify independence from environmental state.
- *Effort estimate:* 2 person-months.

**Property 5: Temporal Consistency (C9 Cross-Layer)**
- *Statement:* The three-tier epoch hierarchy (SETTLEMENT_TICK, TIDAL_EPOCH, CONSOLIDATION_CYCLE) maintains strict nesting — no TIDAL_EPOCH boundary falls within a SETTLEMENT_TICK, and no CONSOLIDATION_CYCLE boundary falls within a TIDAL_EPOCH.
- *Formalization:* `∀ t ∈ TidalBoundaries: ∃ s ∈ SettlementBoundaries: t = s` (tidal boundaries are settlement boundaries) and similarly for consolidation/tidal.
- *Verification approach:* Model epoch counters and boundary events. Verify nesting invariant.
- *Effort estimate:* 2 person-months.

### 14.3 Verification Progression

**Phase 1 (W1-W2): Apalache**
- Symbolic model checking with Apalache for bounded verification
- Properties 4 and 5 verified first (smallest state space)
- Property 1 verified with bounded event sequences (depth ≤ 15)

**Phase 2 (W3-W4): TLC**
- Explicit-state model checking with TLC for Properties 2 and 3
- Agent counts bounded to ≤ 10 in models (sufficient for protocol correctness)
- Property 3 uses existing HotStuff TLA+ model as starting point

**Phase 3 (W4-W5): Integration**
- TLA+ properties linked to implementation via trace validation
- Production system emits traces; traces validated against TLA+ models
- Discrepancies trigger immediate investigation

### 14.4 Property-Based Testing Supplement

For properties outside the TLA+ scope, property-based testing (`proptest` in Rust, `hypothesis` in Python) provides weaker but broader coverage:

- Budget conservation: `∀ ticks: sum(credits_in) = sum(credits_out)` — tested with random transaction sequences
- Credibility bounds: `∀ agents: 0.0 ≤ credibility ≤ 1.0` — tested with random opinion sequences
- CRDT convergence: `∀ operations: merge(a, merge(b, c)) = merge(merge(a, b), c)` — tested with random operation sequences
- Hash ring balance: `∀ populations: max_load / avg_load < 1.03` — tested with random agent join/leave sequences

---

## 15. Team Structure and Hiring Plan

### 15.1 Role Definitions

| Role | Skills | Allocation |
|------|--------|------------|
| **Distributed Systems Engineer (DSE)** | Rust, consensus protocols, hash rings, CRDTs | Core team throughout |
| **Cryptography Engineer (CE)** | ZK-proofs, VRF, commitment schemes, Rust | W0-W4 |
| **ML Engineer (MLE)** | Python, XGBoost, anomaly detection, behavioral analysis | W0, W3-W5 |
| **Verification Engineer (VE)** | TLA+, formal methods, property-based testing | W1-W5 |
| **Economics Engineer (EE)** | Game theory, mechanism design, token economics | W0, W1, W5 |
| **Full-Stack Engineer (FSE)** | TypeScript, Python, API design, dashboards | W1-W5 |
| **Systems Architect (SA)** | Cross-cutting design, specification interpretation | Core team throughout |
| **DevOps Engineer (DOE)** | Kubernetes, CI/CD, monitoring, infrastructure | W1-W5 |
| **Legal/Policy Specialist (LPS)** | AI governance, corporate law, constitutional design | W5 only |

### 15.2 Headcount by Wave

| Wave | DSE | CE | MLE | VE | EE | FSE | DOE | SA | LPS | Total |
|------|-----|----|-----|----|----|-----|-----|----|-----|-------|
| W0 | 2 | 1 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 6 |
| W1 | 3 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| W2 | 4 | 2 | 0 | 1 | 0 | 2 | 1 | 1 | 0 | 11 |
| W3 | 4 | 2 | 2 | 1 | 0 | 2 | 1 | 1 | 0 | 13 |
| W4 | 4 | 2 | 2 | 2 | 0 | 2 | 1 | 1 | 0 | 14 |
| W5 | 3 | 1 | 2 | 2 | 2 | 2 | 1 | 1 | 2 | 16 |

### 15.3 Hiring Timeline

- **Month -1 to 0:** Hire W0 team (6 people). Source: direct network, specialized recruiting.
- **Month 2-3:** Hire W1 additions (3 people). VE and DOE are critical — start recruiting at W0 start.
- **Month 6-7:** Hire W2 additions (2 people). Second CE and second FSE.
- **Month 10-11:** Hire W3 additions (2 MLE). Can be contract if permanent hire is slow.
- **Month 14-15:** Hire W4 additions (1 VE). Second VE for TLA+ Phase 2.
- **Month 18-19:** Hire W5 additions (2 LPS, 1 EE). Legal specialists can be external counsel.

### 15.4 Cross-Training Program

Every engineer must achieve basic competency in at least two layers beyond their primary assignment. Cross-training is structured as:
- **Week 1 of each wave:** 2-day cross-training workshop. Each layer team presents architecture, interfaces, and current challenges.
- **Pair programming rotation:** Each engineer spends 1 day per month working in a different layer team.
- **Shared ownership of C9 contract tests:** All engineers contribute to and review C9 tests, ensuring everyone understands cross-layer contracts.

### 15.5 Conway's Law Alignment

Team boundaries are deliberately aligned with layer boundaries to avoid accidental architectural drift:
- Team Alpha: C4 ASV + C9 Contracts + C8 DSF (foundation)
- Team Beta: C3 Tidal + C5 PCVM (coordination/verification)
- Team Gamma: C6 EMA + C7 RIF (intelligence)
- Team Delta: C11 + C12 + C13 + C17 (defense, from W4)
- Team Epsilon: C14 + C15 (governance/economics, from W5)

Cross-team coordination: weekly 30-minute sync per team pair with direct dependencies. Monthly all-hands (1 hour) for system-wide status.

---

## 16. Infrastructure and Cost Model

### 16.1 Cloud Resources by Wave

| Wave | Compute | Storage | Network | ML/GPU | Total/month |
|------|---------|---------|---------|--------|-------------|
| W0 | $3K | $500 | $200 | $4K | $7.7K |
| W1 | $8K | $2K | $1K | $2K | $13K |
| W2 | $15K | $5K | $3K | $2K | $25K |
| W3 | $20K | $8K | $5K | $8K | $41K |
| W4 | $18K | $6K | $4K | $5K | $33K |
| W5 | $15K | $5K | $3K | $8K | $31K |

**Total cloud cost estimate:** ~$410K across all waves (assuming mid-range durations).

### 16.2 Personnel Cost Model

Assumes blended fully-loaded cost of $18K-$22K/person/month (competitive for senior distributed systems/ML engineers):

| Wave | Duration (months) | Avg Headcount | Cost Range |
|------|-------------------|---------------|------------|
| W0 | 2.5 | 6 | $270K-$330K |
| W1 | 4.5 | 9 | $729K-$891K |
| W2 | 5.0 | 11 | $990K-$1,210K |
| W3 | 5.0 | 13 | $1,170K-$1,430K |
| W4 | 3.5 | 14 | $882K-$1,078K |
| W5 | 5.0 | 16 | $1,440K-$1,760K |

**Total personnel estimate:** $5.0M-$6.7M

### 16.3 Other Costs

| Category | Estimate |
|----------|----------|
| External security audit (W4) | $150K-$250K |
| Legal counsel (W5) | $100K-$200K |
| TLA+ tooling and training | $30K-$50K |
| Recruiting (15-19 hires over 24 months) | $200K-$400K |
| Miscellaneous (travel, equipment, licenses) | $100K-$200K |

### 16.4 Total Budget Summary

| Category | Low | High |
|----------|-----|------|
| Cloud infrastructure | $350K | $470K |
| Personnel | $5,000K | $6,700K |
| Other costs | $580K | $1,100K |
| Contingency (10%) | $593K | $827K |
| **Total** | **$6,523K** | **$9,097K** |

*Note: The $5.4M-$8.8M range in the concept summary reflects the pre-contingency estimate. With 10% contingency, the range is $6.5M-$9.1M.*

### 16.5 Budget Scope Statement

**C22 provides engineering costs only.** The $5.4M--$8.8M budget (pre-contingency) covers personnel salaries, cloud infrastructure, tooling, formal verification, and recruiting required for W0--W5 technical delivery. This is a subset of C18's fully-loaded $10.2M--$12.1M budget.

**The following costs are NOT included in C22's budget and are covered by C18:**

- Legal entity formation costs (Stiftung: $25K--$60K, PBC: $15K--$25K, Purpose Trust: Phase 2+) — see C18 Section 3
- Non-engineering compensation (signing bonuses, wave milestone bonuses, PVR payouts, CRF) — see C18 Sections 6--8
- Operational overhead (grant management CFO, operating reserve, non-engineering travel) — see C18 Section 9
- Contingency reserves beyond engineering scope — see C18 Section 9
- Nominating body outreach costs ($11K--$105K) — see C16

**Mapping: C22 engineering costs within C18 fully-loaded categories**

| C22 Category | C22 Range | Maps to C18 Category |
|--------------|-----------|----------------------|
| Personnel (engineering salaries) | $5.0M--$6.7M | Personnel (payroll + benefits): $6.8M--$8.5M (C18 includes non-engineering staff) |
| Cloud infrastructure | $350K--$470K | Cloud infrastructure: $370K--$470K |
| Recruiting | $200K--$400K | Recruiting subset of Travel/conferences/recruiting |
| TLA+ tooling and training | $30K--$50K | Not separately itemized in C18 |
| Miscellaneous (travel, equipment, licenses) | $100K--$200K | Travel/conferences/recruiting (partial) |
| Contingency (10%) | $593K--$827K | Contingency (10%): $1.0M--$1.2M (C18 contingency covers all categories) |
| **C22 Total** | **$6.5M--$9.1M** | **C18 Total: $10.2M--$12.1M** |

The delta between C18 and C22 totals ($3.0M--$3.7M) represents legal formation, compensation premiums (signing bonuses, milestone bonuses, PVR payouts), CRF, grant management, operating reserve, and the non-engineering share of contingency.

### 16.6 Timeline Scope Statement

C22's 21--30 month timeline covers W0--W5 technical delivery only, from the start of Wave 0 risk validation experiments through Wave 5 governance delivery. This timeline does **not** include:

- **Pre-W0 activities** (~3 months): Legal entity formation, founding capital deployment, initial hiring — covered by C18
- **Post-W5 operations** (~3--6 months): Revenue ramp to financial sustainability, operational transition — covered by C18

C18's 30--36 month timeline encompasses the full project lifecycle from entity formation (Month 0) through financial sustainability (Month 36). C22's W0 begins approximately at C18 Month 3, after legal formation and founding team assembly are complete. See C18 Section 9 for the complete timeline and cash flow model.

---

## 17. Wave Transition Criteria

### 17.1 Wave 0 → Wave 1

**Advancement gate:**
- All three experiments completed and documented
- Steering Committee has issued PROCEED decisions (or approved pivots) for all three
- Pivot plans (if any) are documented with revised success criteria
- Team W1 hires are confirmed (start date within 2 weeks of W0 exit)

**Kill criteria:** See Section 5.4.

### 17.2 Wave 1 → Wave 2

**Advancement gate:**
- C4 ASV: All message types defined and validated (JSON Schema tests pass)
- C9 contract test suite: ≥200 schema tests, ≥50 sequence tests, ≥20 invariant tests passing
- C8 DSF: Settlement loop operational, 3 budgets enforced, single-node demo
- Subjective Logic engine: All fusion operators implemented, property-based tests pass, 1M fusions/sec benchmark met
- LLM abstraction: ≥2 providers working, cost tracking operational
- MCP/A2A: Protocol selection decision documented with rationale
- All components at Stub tier or above per Section 11.2

### 17.3 Wave 2 → Wave 3

**Advancement gate:**
- C3 Tidal: Hash ring operational at 1,000 agents, <3% imbalance, VRF defense active
- C5 PCVM: All 9 claim classes classifiable, VTD pipeline end-to-end functional
- C9 contract tests: ≥400 tests passing (Tier 1 + Tier 2)
- Ensemble rehearsal: 3 consecutive successful weekly rehearsals
- TLA+ Properties 4 and 5 verified (Apalache)

### 17.4 Wave 3 → Wave 4

**Advancement gate:**
- C6 EMA: SHREC pipeline operational, ≥1 consolidation cycle completed end-to-end
- C7 RIF: Intent decomposition producing valid task graphs, HotStuff consensus operational for G-class
- Minimal viable infrastructure demo: claim submitted → verified → synthesized → settled (end-to-end)
- C9 contract tests: ≥500 tests passing (all three tiers)
- TLA+ Properties 1 and 2 verified

### 17.5 Wave 4 → Wave 5

**Advancement gate:**
- C11 CACT: All four phases operational, retroactive fabrication test blocked
- C12 AVAP: Collusion detection operational, diversity pools enforced
- C13 CRP+: Poison detection operational, quarantine and rollback tested
- External security audit completed with no CRITICAL findings unresolved
- TLA+ Property 3 verified
- Red team exercise: defense systems survive 5 out of 5 pre-defined attack scenarios

### 17.6 Emergency Escalation

If a wave exceeds its maximum duration by more than 25%, or if a critical blocker persists for more than 3 weeks, the Steering Committee convenes an emergency review with three possible outcomes:
1. **Extend:** Add time and/or resources. Maximum one extension per wave.
2. **Descope:** Remove non-critical features from the current wave, deferring to a later wave.
3. **Restructure:** Merge waves, reorder waves, or insert a stabilization sprint.

The decision is documented with rationale and communicated to all teams within 24 hours.

---

## 18. Spec Revision Protocol

### 18.1 Discovery-Triage-Revision Flow

Implementation will inevitably reveal specification deficiencies. The revision protocol ensures these are handled systematically:

```
Discovery: Engineer identifies spec-implementation gap
    ↓
Filing: Issue filed in spec-revision tracker with:
  - Affected spec(s)
  - Nature: AMBIGUITY | CONTRADICTION | OMISSION | INFEASIBILITY
  - Severity: CRITICAL | HIGH | MEDIUM | LOW
  - Proposed resolution (if any)
    ↓
Triage (weekly, 30 min): Systems Architect + affected layer leads
  - CRITICAL: Addressed within 1 week. Blocks affected work.
  - HIGH: Addressed within 2 weeks. Work continues with documented assumption.
  - MEDIUM: Queued for next quarterly review.
  - LOW: Backlog.
    ↓
Resolution: Spec revision drafted, reviewed by original spec author (if available) + 2 engineers
    ↓
Publication: Revised spec version published. C9 contract tests updated. Changelog entry.
```

### 18.2 Quarterly Review Cycle

At the end of each quarter, the full team conducts a 4-hour spec review:
1. Review all MEDIUM and LOW revision requests accumulated during the quarter.
2. Assess spec-implementation drift: are implementations diverging from specs in undocumented ways?
3. Update the C9 reconciliation addendum if cross-layer contracts have changed.
4. Publish a "Spec Health Report" summarizing open revisions, drift areas, and planned corrections.

### 18.3 Automated Compliance Checking

The CI/CD pipeline includes automated spec compliance checks:
- **Schema compliance:** All C4 ASV messages validated against canonical JSON Schema on every build.
- **Parameter range compliance:** Configurable parameters checked against spec-defined ranges.
- **Epoch compliance:** Epoch durations and nesting verified against C9 canonical values.
- **Claim class compliance:** Classifier output validated against C5 canonical class definitions.

Compliance failures are treated as CI failures (merge blocked).

---

## 19. Risk Analysis

### 19.1 Pre-Mortem Failure Modes

**Failure Mode 1: Subjective Logic Does Not Scale**
- *Scenario:* Opinion fusion is O(n^2) in verifier count; at 100+ verifiers per claim, fusion becomes the bottleneck.
- *Probability:* 15%
- *Impact:* HIGH — C5 PCVM credibility engine is unusable at scale
- *Mitigation:* Hierarchical fusion (parcel-local fusion → cross-parcel aggregation). Pre-computed fusion tables for common opinion patterns. Approximate fusion for low-stakes claims.
- *Detection:* W1 benchmarks (1M fusions/sec target). If target missed by >5x, trigger mitigation.

**Failure Mode 2: Cross-Layer Epoch Drift**
- *Scenario:* Under load, SETTLEMENT_TICKs drift relative to wall clock. TIDAL_EPOCH boundaries no longer align with SETTLEMENT_TICK boundaries. Cascading accounting errors.
- *Probability:* 20%
- *Impact:* CRITICAL — breaks budget conservation invariant
- *Mitigation:* Dedicated epoch coordinator service (NTP-like) with monotonic epoch counters independent of wall clock. Epoch boundary consensus protocol.
- *Detection:* TLA+ Property 5 catches the logical error. Runtime drift detector triggers alert at >100ms drift.

**Failure Mode 3: C9 Contract Test Suite Becomes Bottleneck**
- *Scenario:* Contract test suite grows to >1,000 tests. Full suite takes >30 minutes. Engineers bypass or selectively run tests. Integration regressions slip through.
- *Probability:* 30%
- *Impact:* MEDIUM — integration quality degrades gradually
- *Mitigation:* Test suite tiering: Tier 1 runs on every merge (<5 min), Tier 2 runs nightly, Tier 3 runs weekly. Smart test selection: only run tests affected by changed layers.
- *Detection:* CI metrics tracking: test suite duration, bypass rate, post-merge failure rate.

**Failure Mode 4: LLM Provider Instability**
- *Scenario:* Primary LLM provider changes API, raises prices 10x, or degrades quality. C6 EMA and C7 RIF lose their synthesis/decomposition capability.
- *Probability:* 25%
- *Impact:* HIGH — intelligence layers become non-functional
- *Mitigation:* LLM abstraction layer (built in W1) with ≥3 provider adapters. Local model fallback (vLLM/Ollama). Prompt engineering that works across model families.
- *Detection:* Automated quality regression tests on LLM outputs. Cost monitoring with budget alerts.

**Failure Mode 5: Team Attrition at Critical Juncture**
- *Scenario:* 2+ senior engineers leave during W2 or W3, taking institutional knowledge of C3 or C5 implementation.
- *Probability:* 35%
- *Impact:* HIGH — 3-6 month delay while replacements ramp up
- *Mitigation:* Cross-training program (Section 15.4). Pair programming for all critical-path work. Architecture Decision Records (ADRs) for all non-obvious implementation choices. Competitive compensation with retention bonuses at wave boundaries.
- *Detection:* Monthly 1:1s with flight risk assessment. Exit interview protocol.

**Failure Mode 6: Formal Verification Exceeds Budget**
- *Scenario:* TLA+ properties require deeper state exploration than anticipated. 2 person-year cap exhausted before all 5 properties verified.
- *Probability:* 40%
- *Impact:* MEDIUM — some properties unverified, relying on property-based tests only
- *Mitigation:* Strict prioritization: Properties 1 (settlement) and 2 (epoch safety) are non-negotiable. Properties 3-5 are descoped if budget exhausted. Apalache-first approach (symbolic checking faster than TLC enumeration).
- *Detection:* Monthly progress report from VE team. If <1 property verified by month 12, trigger budget review.

### 19.2 Risk Matrix Summary

| Risk | Probability | Impact | Residual Risk After Mitigation |
|------|-------------|--------|-------------------------------|
| SL scaling | 15% | HIGH | LOW (hierarchical fusion is well-understood) |
| Epoch drift | 20% | CRITICAL | LOW (dedicated coordinator + TLA+) |
| Contract test bottleneck | 30% | MEDIUM | LOW (tiering + smart selection) |
| LLM instability | 25% | HIGH | MEDIUM (local fallback quality uncertain) |
| Team attrition | 35% | HIGH | MEDIUM (knowledge transfer inherently lossy) |
| Verification overrun | 40% | MEDIUM | LOW (prioritized descoping) |

---

## 20. Formal Requirements

### 20.1 Wave Requirements (WR)

| ID | Requirement | Wave | Priority |
|----|-------------|------|----------|
| WR-01 | Wave 0 SHALL complete all three risk validation experiments with documented results before Wave 1 begins. | W0 | CRITICAL |
| WR-02 | Wave 0 kill criteria SHALL be evaluated by a Steering Committee of ≥3 senior engineers plus ≥1 external advisor. | W0 | CRITICAL |
| WR-03 | Wave 1 SHALL produce a functional C4 ASV implementation with all message types validated against JSON Schema. | W1 | CRITICAL |
| WR-04 | Wave 1 SHALL deliver a Subjective Logic engine achieving ≥1M opinion fusions per second on commodity hardware. | W1 | HIGH |
| WR-05 | Wave 2 SHALL demonstrate C3 Tidal scheduling at ≥1,000 concurrent agents with <3% load imbalance. | W2 | CRITICAL |
| WR-06 | Wave 2 SHALL demonstrate C5 PCVM classification for all 9 canonical claim classes with deterministic results. | W2 | CRITICAL |
| WR-07 | Wave 3 SHALL demonstrate an end-to-end claim lifecycle: submission → verification → synthesis → settlement. | W3 | CRITICAL |
| WR-08 | Wave 4 SHALL pass an external security audit with no unresolved CRITICAL findings. | W4 | CRITICAL |
| WR-09 | Wave 4 SHALL survive a red team exercise covering ≥5 pre-defined attack scenarios. | W4 | HIGH |
| WR-10 | Wave 5 SHALL demonstrate Phase 1 (human trustee) constitutional governance with CFI monitoring. | W5 | HIGH |

### 20.2 Integration Requirements (IR)

| ID | Requirement | Priority |
|----|-------------|----------|
| IR-01 | The C9 contract test suite SHALL block all merge requests on failure, regardless of unit test status. | CRITICAL |
| IR-02 | All inter-layer communication SHALL use C4 ASV message types with JSON Schema validation. | CRITICAL |
| IR-03 | The three-tier epoch hierarchy (60s/3600s/36000s) SHALL be enforced by automated compliance checks. | CRITICAL |
| IR-04 | Weekly ensemble rehearsals SHALL begin no later than Wave 2 and continue through program completion. | HIGH |
| IR-05 | All 9 canonical claim classes SHALL be exercised through the full pipeline in integration tests. | HIGH |
| IR-06 | Cross-layer latency for a single claim lifecycle SHALL not exceed 2x SETTLEMENT_TICK (120s) at Functional tier. | HIGH |
| IR-07 | The integration test environment SHALL support fault injection from Wave 3 onward. | MEDIUM |
| IR-08 | Each layer SHALL expose health check and readiness endpoints compatible with Kubernetes liveness/readiness probes. | HIGH |

### 20.3 Verification Requirements (VR)

| ID | Requirement | Priority |
|----|-------------|----------|
| VR-01 | TLA+ models SHALL be developed for all 5 specified properties (Section 14.2). | HIGH |
| VR-02 | Properties 1 (settlement determinism) and 2 (epoch safety) SHALL be verified before Wave 4 entry. | CRITICAL |
| VR-03 | Total formal verification effort SHALL NOT exceed 2 person-years (24 person-months). | HIGH |
| VR-04 | Property-based tests SHALL supplement TLA+ verification for all quantitative invariants. | HIGH |
| VR-05 | TLA+ trace validation SHALL be operational against production traces by Wave 5. | MEDIUM |

### 20.4 Team Requirements (TR)

| ID | Requirement | Priority |
|----|-------------|----------|
| TR-01 | Every engineer SHALL achieve basic competency in ≥2 layers beyond their primary assignment. | HIGH |
| TR-02 | All critical-path implementation SHALL use pair programming. | HIGH |
| TR-03 | Architecture Decision Records (ADRs) SHALL be created for all non-obvious implementation choices. | MEDIUM |
| TR-04 | Team boundaries SHALL align with layer boundaries per Conway's Law (Section 15.5). | HIGH |
| TR-05 | Cross-team sync meetings SHALL occur weekly for directly dependent team pairs. | HIGH |

### 20.5 Budget Requirements (BR)

| ID | Requirement | Priority |
|----|-------------|----------|
| BR-01 | Monthly cloud spend SHALL NOT exceed 150% of the budgeted amount for the current wave without Steering Committee approval. | HIGH |
| BR-02 | Personnel costs SHALL be tracked monthly with ≤10% variance from plan. | HIGH |
| BR-03 | A 10% contingency reserve SHALL be maintained against total budget. | MEDIUM |
| BR-04 | LLM API costs SHALL be tracked per-call and attributed to the consuming layer. | HIGH |
| BR-05 | Any single expenditure exceeding $50K SHALL require Steering Committee approval. | HIGH |

---

## 21. Configurable Parameters

| Parameter | Default | Range | Owner | Description |
|-----------|---------|-------|-------|-------------|
| `SETTLEMENT_TICK_DURATION` | 60s | 30-120s | C8 DSF | Duration of settlement tick |
| `TIDAL_EPOCH_DURATION` | 3,600s | 1,800-7,200s | C3 Tidal | Duration of tidal epoch |
| `CONSOLIDATION_CYCLE_DURATION` | 36,000s | 18,000-72,000s | C6 EMA | Duration of consolidation cycle |
| `MAX_AGENTS_PER_PARCEL` | 100 | 20-500 | C3 Tidal | Maximum agents in a single parcel |
| `HASH_RING_VIRTUAL_NODES` | 150 | 50-500 | C3 Tidal | Virtual nodes per physical agent in hash ring |
| `LOAD_IMBALANCE_THRESHOLD` | 0.03 | 0.01-0.10 | C3 Tidal | Maximum acceptable load imbalance |
| `VERIFIER_QUORUM_SIZE` | 5 | 3-9 | C5 PCVM | Number of verifiers per claim |
| `CREDIBILITY_DECAY_RATE` | 0.01 | 0.001-0.05 | C5 PCVM | Per-epoch credibility decay on inactivity |
| `SL_FUSION_MAX_ITERATIONS` | 10 | 5-20 | Subjective Logic | Max iterations for opinion fusion convergence |
| `SL_CONVERGENCE_THRESHOLD` | 0.001 | 0.0001-0.01 | Subjective Logic | Convergence threshold for fusion |
| `LLM_RATE_LIMIT` | 100 | 10-1,000 | LLM Abstraction | Max LLM calls per agent per TIDAL_EPOCH |
| `KNOWLEDGE_CARRYING_CAPACITY` | 10,000 | 1,000-100,000 | C6 EMA | Max knowledge artifacts per domain |
| `DIVERSITY_INDEX_THRESHOLD` | 2.0 nats | 1.0-3.0 nats | C6 EMA | Minimum Shannon entropy of knowledge sources |
| `CHALLENGE_BOND_RATIO` | 0.10 | 0.05-0.25 | C11 CACT | Challenge bond as fraction of verification cost |
| `WHISTLEBLOWER_REWARD_RATIO` | 0.20 | 0.10-0.50 | C12 AVAP | Reward as fraction of collusion penalty |
| `POISON_KL_THRESHOLD` | 0.5 | 0.2-1.0 | C13 CRP+ | KL divergence threshold for poison detection |
| `CFI_REVIEW_THRESHOLD` | 0.7 | 0.5-0.9 | C14 AiBC | CFI below this triggers governance review |
| `CFI_EMERGENCY_THRESHOLD` | 0.5 | 0.3-0.7 | C14 AiBC | CFI below this triggers emergency intervention |
| `SYBIL_FPR_TARGET` | 0.001 | 0.0001-0.01 | C17 MCSD | Target false positive rate for Sybil detection |
| `COST_OF_ATTACK_TARGET` | $90M | $50M-$500M | C17 MCSD | Minimum economic cost to execute Sybil attack |
| `CONTRACT_TEST_TIMEOUT` | 300s | 120-600s | C9 | Maximum duration for full contract test suite |
| `ENSEMBLE_REHEARSAL_FREQUENCY` | weekly | daily-monthly | Integration | Frequency of ensemble rehearsal runs |
| `TLA_VERIFICATION_BUDGET` | 24 pm | 12-36 pm | Verification | Person-months allocated to TLA+ verification |
| `WAVE_OVERRUN_THRESHOLD` | 1.25 | 1.10-1.50 | Management | Wave duration multiplier triggering emergency review |

---

## 22. Patent-Style Claims

**Claim 1: Risk-First Implementation Sequencing for Multi-Specification Systems**

A method for implementing a software system defined by a plurality of interdependent specifications, comprising: (a) identifying foundational assumptions upon which multiple specifications depend; (b) constructing isolated validation experiments for each foundational assumption with pre-registered quantitative success criteria and kill criteria; (c) executing said experiments before any production code is written; (d) gating all subsequent implementation work on experimental outcomes; and (e) documenting pivot alternatives for each kill criterion to enable rapid program restructuring, wherein the method minimizes sunk-cost exposure by converting implicit project risk into explicit, measurable engineering gates.

**Claim 2: Embryonic Maturity Tier Architecture**

A system for concurrent development of multiple interdependent software layers, comprising: (a) a maturity tier model with at least four tiers (Stub, Functional, Hardened, Production) defining progressive implementation completeness; (b) interface stubs for all layers deployed from the earliest development phase, implementing complete inter-layer message contracts while using mock internal algorithms; (c) a cross-layer contract test suite that validates interface compliance at each tier; and (d) independent tier progression per layer, enabling layers with different complexity profiles to advance at different rates while maintaining system-wide integration correctness.

**Claim 3: Specification-Derived Integration Testing**

A method for maintaining integration correctness in a multi-layer software system, comprising: (a) deriving executable contract tests directly from formal cross-layer reconciliation specifications; (b) organizing tests into bilateral contracts (layer pairs), pipeline contracts (multi-layer flows), and invariant contracts (system-wide properties); (c) enforcing contract test passage as a mandatory gate for all code merges; and (d) conducting periodic ensemble rehearsals where all layers are deployed at their current maturity tier and exercised through canonical scenarios, wherein the contract test suite serves as the single source of truth for inter-layer agreements.

**Claim 4: Formal Verification Budget Capping with Prioritized Descoping**

A method for applying formal verification to a large-scale software system within resource constraints, comprising: (a) identifying a bounded set of critical safety properties; (b) allocating a fixed verification budget (measured in person-time); (c) ordering properties by criticality such that the most critical properties are verified first; (d) progressively applying verification methods from symbolic model checking to explicit-state model checking; (e) supplementing formal verification with property-based testing for properties outside the verification scope; and (f) descoping lower-priority properties if the budget is exhausted, ensuring that the most critical properties are always verified regardless of resource constraints.

**Claim 5: Conway's Law-Aligned Multi-Layer Team Architecture**

A method for organizing engineering teams building a multi-layer system, comprising: (a) aligning team boundaries with architectural layer boundaries; (b) assigning shared ownership of cross-layer contract tests to all teams; (c) requiring each engineer to achieve competency in at least two layers beyond their primary assignment; (d) conducting periodic cross-team pair programming rotations; and (e) using a dedicated epoch coordinator role to synchronize cross-team work, wherein team structure mirrors system architecture to prevent accidental architectural drift while cross-training prevents knowledge silos.

---

## 23. Comparison with Existing Approaches

### 23.1 Versus Waterfall

Waterfall completes specifications before implementation. RFEIA completes specifications first (they already exist as C3-C17) but sequences *implementation* by risk rather than dependency. Waterfall would implement C4 → C8 → C5 → C3 → C6 → C7 → defenses → governance. RFEIA starts with risk experiments, then builds all layers as stubs simultaneously.

**Advantage:** Waterfall discovers integration failures late. RFEIA discovers them from Week 1 of Wave 1 via C9 contract tests.

### 23.2 Versus Agile/Scrum

Agile iterates in short sprints with evolving requirements. RFEIA has fixed specifications (the 13 specs) but iterates on *implementation maturity* (Stub → Production). Agile would not pre-register kill criteria or cap formal verification budgets.

**Advantage:** Agile lacks the formal rigor needed for a system where incorrectness is catastrophic. RFEIA uses formal methods where they matter most while remaining iterative where flexibility is needed.

### 23.3 Versus Microservice Architecture

Microservice architecture decomposes by service boundary. RFEIA decomposes by specification boundary, which is coarser. Each spec may encompass multiple microservices internally, but inter-spec communication is governed by C4 ASV and C9 contracts.

**Advantage:** Microservices lack formal cross-service contracts. RFEIA's C9 contract test suite provides what microservice architectures typically lack: a rigorous, executable specification of inter-service behavior.

### 23.4 Versus NASA-Style Formal Development

NASA projects (e.g., Cassini, Mars rovers) use heavyweight formal methods with exhaustive verification. RFEIA uses formal methods selectively (5 properties, 2 person-year cap) supplemented by property-based testing.

**Advantage:** NASA-style is prohibitively expensive for a system of this size (21,000+ spec lines). RFEIA achieves "good enough" formal assurance for the critical properties while staying within budget.

---

## 24. Open Questions

**OQ-1: MCP versus A2A Protocol Selection**
Wave 1 evaluates both protocols. The selection criteria are defined (throughput, schema expressiveness, ecosystem maturity), but the outcome is unknown until evaluation completes. If neither protocol meets requirements, a custom transport layer may be needed, adding 2-3 months to Wave 1.

**OQ-2: Subjective Logic Numerical Stability at Scale**
Wave 0 Experiment 2 tests Subjective Logic with 90,000 claims. Production may process millions. Log-space computation mitigates overflow, but underflow in extreme-uncertainty opinions (uncertainty > 0.999) is untested at scale.

**OQ-3: SNARK/STARK Proof Generation Cost**
C5 specifies cryptographic verification for D-class and S-class claims. Proof generation cost (compute time, memory) at production claim volumes is estimated but untested. If proof generation exceeds 1 SETTLEMENT_TICK per claim, pipeline throughput is constrained.

**OQ-4: Knowledge Graph Storage Engine**
C6 EMA requires a knowledge graph. The spec is agnostic to storage engine. Options: embedded graph (e.g., `oxigraph`), external database (Neo4j, DGraph), or custom property graph on top of the HDL. Selection depends on W3 performance requirements.

**OQ-5: Governance Phase Transition Timing**
C14 AiBC defines 4 governance phases. Phase 1 is implemented in W5. Phase 2+ transitions depend on agent population size, credibility maturity, and legal environment — none of which can be predicted at implementation start.

**OQ-6: Token Economics Stability**
C15 AIC's reference rate model assumes a minimum viable agent population. If adoption is slower than projected, the token economy may not reach equilibrium. Economic simulation in W5 will test sensitivity, but real-world validation requires production deployment.

**OQ-7: Cross-Specification Consistency Post-Implementation**
C9 reconciled the specs at the specification level. Implementation will inevitably introduce new inconsistencies not present in the specs. The spec revision protocol (Section 18) addresses this procedurally, but the volume of revisions is unknown.

---

## 25. Glossary

| Term | Definition |
|------|------------|
| **ADR** | Architecture Decision Record — documented rationale for non-obvious implementation choices |
| **AiBC** | Artificial Intelligence Benefit Company — C14 governance framework |
| **AIC** | AI Credit — native settlement token of the Atrahasis system |
| **ASV** | Atrahasis Semantic Vocabulary — C4 message schema and type system |
| **AVAP** | Adversarial Verification Assurance Protocol — C12 collusion defense |
| **CACT** | Commit-Attest-Challenge-Triangulate — C11 forgery defense |
| **CFI** | Constitutional Fidelity Index — real-time governance compliance metric |
| **Citicate** | AI citizenship credential issued under C14 AiBC |
| **CRDT** | Conflict-free Replicated Data Type — used in C3 for parcel-local state |
| **CRP+** | Consolidation Resilience Protocol Plus — C13 poisoning defense |
| **DSF** | Deterministic Settlement Fabric — C8 economic substrate |
| **EMA** | Epistemic Metabolism Architecture — C6 knowledge layer |
| **HDL** | Hybrid Deterministic Ledger — C8 append-only ledger with Merkle proofs |
| **HotStuff** | Three-phase BFT consensus protocol used in C7 RIF |
| **Kill Criterion** | Pre-registered quantitative threshold that halts or pivots the program |
| **MCSD** | Multi-Channel Sybil Defense — C17 behavioral fingerprinting |
| **PCVM** | Proof-Carrying Verification Machine — C5 verification layer |
| **RFEIA** | Risk-First Embryonic Implementation Architecture — this specification |
| **RIF** | Recursive Intent Fabric — C7 orchestration layer |
| **SETTLEMENT_TICK** | 60-second settlement interval (C8) |
| **SHREC** | Synthesis-Harmonization-Reflection-Evaluation-Consolidation — C6 knowledge metabolism cycle |
| **SNARK** | Succinct Non-interactive Argument of Knowledge — cryptographic proof system |
| **STARK** | Scalable Transparent Argument of Knowledge — cryptographic proof system |
| **Stub** | Interface-complete, algorithm-mock implementation (Tier 1 of maturity model) |
| **Subjective Logic** | Belief-uncertainty calculus for credibility computation |
| **TIDAL_EPOCH** | 3,600-second coordination interval (C3) |
| **TLA+** | Temporal Logic of Actions — formal specification language |
| **VRF** | Verifiable Random Function — used for unpredictable verifier selection |
| **VSM** | Viable System Model — organizational cybernetics framework used in C7 |
| **VTD** | Verification Task Descriptor — unit of work in C5 PCVM |
| **Wave** | Implementation phase in RFEIA (W0 through W5) |

---

## 26. References

1. C3 — Tidal Noosphere Master Technical Specification v2.0 (3,503 lines)
2. C4 — Atrahasis Semantic Vocabulary (ASV) v2.0 (1,652 lines)
3. C5 — Proof-Carrying Verification Machine (PCVM) v2.0 (3,743 lines)
4. C6 — Epistemic Metabolism Architecture (EMA) v2.0 (3,562 lines)
5. C7 — Recursive Intent Fabric (RIF) v2.0 (4,864 lines)
6. C8 — Deterministic Settlement Fabric (DSF) v2.0 (5,494 lines)
7. C9 — Cross-Document Reconciliation Addendum
8. C10 — Spec Cleanup and Hardening (49 engineering fixes + 13 hardening designs)
9. C11 — CACT: VTD Forgery Defense (1,945 lines)
10. C12 — AVAP: Collusion Defense (2,674 lines)
11. C13 — CRP+: Consolidation Poisoning Defense (2,640 lines)
12. C14 — AiBC: Artificial Intelligence Benefit Company
13. C15 — AIC Economics
14. C17 — MCSD Layer 2: Behavioral Fingerprinting and Sybil Detection
15. Lamport, L. — "Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers"
16. Yin, M. et al. — "HotStuff: BFT Consensus with Linearity and Responsiveness" (PODC 2019)
17. Josang, A. — "Subjective Logic: A Formalism for Reasoning Under Uncertainty" (Springer, 2016)
18. Karger, D. et al. — "Consistent Hashing and Random Trees" (STOC 1997)
19. Shapiro, M. et al. — "Conflict-free Replicated Data Types" (SSS 2011)
20. Beer, S. — "Brain of the Firm" (Viable System Model, 1972/1981)
21. Conway, M. — "How Do Committees Invent?" (Datamation, 1968)
22. Ben-Sasson, E. et al. — "Scalable, Transparent, and Post-Quantum Secure Computational Integrity" (STARKs, 2018)

---

*End of C22-MTS-v1.0 — Risk-First Embryonic Implementation Architecture for Planetary-Scale AI Agent Infrastructure*

*Document hash: To be computed upon final review.*
*Total formal requirements: 33 (WR: 10, IR: 8, VR: 5, TR: 5, BR: 5)*
*Total configurable parameters: 23*
*Patent-style claims: 5*
