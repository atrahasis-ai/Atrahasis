# DECISIONS (ADR Log)
**Owner:** Chronicler
**Purpose:** durable, searchable decision memory (short).

---

## ADR-001 — Concept Selection: Predictive Tidal Architecture (PTA)
**Date:** 2026-03-09
**Status:** ACCEPTED
**Context:**
- Ideation Council produced 3 concepts from 3-round adversarial debate (7 initial proposals narrowed to 3)
- C1-A (PTA): Novelty 4, Feasibility 4 — tidal backbone + FEP predictive communication + local morphogenic fields
- C1-B (SGCN): Novelty 4.5, Feasibility 3 — pure FEP, highest risk
- C1-C (DCS): Novelty 3, Feasibility 4.5 — pure deterministic scheduling, lowest risk
**Decision:**
- Selected C1-A (PTA) as primary architecture to pursue
- PTA is a coordination layer only — requires verification membranes + knowledge graph persistence
- DCS is engineering fallback; SGCN is research track
**Consequences:**
- Research Layer investigates PTA prior art, landscape, and scientific soundness
- Verification layer remains unsolved — must be addressed separately
- Tidal backbone (`verifier_set = f(claim_hash, epoch)`) is core innovation to validate first
**References:** docs/invention_logs/C1.md, docs/invention_logs/C1_IDEATION_COUNCIL_OUTPUT.yaml
**Invention:** C1

---

## ADR-002 — Feasibility Verdict: CONDITIONAL_ADVANCE for PTA
**Date:** 2026-03-09
**Status:** ACCEPTED
**Context:**
- Assessment Council (Advocate, Skeptic, Arbiter) evaluated refined PTA concept after FEASIBILITY stage
- Scores: Novelty 4, Feasibility 4, Impact 4, Risk 5/10 (MEDIUM)
- Advocate: tidal backbone is genuinely novel, phased build provides value at each stage, risk management is honest
- Skeptic: predictive communication unproven (feasibility 3), 21-27 month timeline optimistic, integration complexity underestimated
- Arbiter: scores justified, concept sufficiently refined for DESIGN entry
**Decision:**
- CONDITIONAL_ADVANCE to DESIGN with 4 conditions attached
- Conditions: (1) convergence experiment as first deliverable with kill criterion, (2) integration contracts with Verichain/CIOS in Phase 1, (3) predictive layer scoped as enhancing-not-required, (4) morphogenic field decision gate at end of Phase 2
**Consequences:**
- DESIGN stage begins with Architecture Designer and Specification Writer
- First deliverable must be tidal function convergence experiment design
- 5 monitoring flags set (1 RED, 3 AMBER, 1 INFO)
**References:** docs/invention_logs/C1_FEASIBILITY_VERDICT.md, docs/invention_logs/C1_REFINED_INVENTION_CONCEPT.yaml
**Invention:** C1

---

## ADR-003 — System Evolution: Role Expansion + Whitepaper Output (v2.0)
**Date:** 2026-03-09
**Status:** ACCEPTED
**Context:**
- C2 meta-task: the system improving itself to increase novel invention probability
- Ideation Council identified 4 genuinely missing cognitive functions + 6 protocol gaps
- User feedback: system should produce Master Tech Spec whitepapers, not prototypes
**Decision:**
- Added 4 new roles: Domain Translator, Pre-Mortem Analyst, Simplification Agent, Adversarial Analyst (21 → 23 roles; net -2 from removing Prototype Engineer + Prototype Validator)
- Added 6 protocol changes: prior art quick scan, Chronicler active injection, Science Advisor reconciliation, mid-DESIGN review gate, enhanced synthesis checks, Execution Layer internal coordination
- Modified 2 existing roles: Critic (expanded metaphor analysis mandate), Commercial Viability Assessor (timing change to FEASIBILITY)
- Removed PROTOTYPE stage; final deliverable is now MASTER_TECH_SPEC.md (whitepaper with technical details + narrative)
- Domain Translator and Adversarial Analyst on 3-invention trial with kill criteria
**Consequences:**
- Master prompt updated from v1.0 to v2.0
- Stage lifecycle: IDEATION → RESEARCH → FEASIBILITY → DESIGN → SPECIFICATION → ASSESSMENT
- ~30-40% increase in compute per invention, offset by earlier problem detection and complexity reduction
- Prototype Engineer and Prototype Validator roles removed
**References:** docs/invention_logs/C2.md
**Invention:** C2

---

## ADR-004 — Concept Selection: Tidal Noosphere (C3-A)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Ideation Council (with Domain Translator, Round 0 context absorption) analyzed three independent coordination architectures: Noosphere (2277 lines), Locus Fabric (prompt-described), PTA (4438 lines)
- 4-round deliberation produced 3 concepts: C3-A Tidal Noosphere (N4/F4), C3-B Dual-Mode Fabric (N3/F3), C3-C Minimal Integration (N2/F5)
- FULL council consensus on C3-A; user validated every synthesis decision individually
**Decision:**
- Selected C3-A "Tidal Noosphere" — Noosphere absorbs PTA as scheduling substrate within parcels, Locus Fabric's proof obligations become the formal standard
- Key integration: predictive delta for intra-parcel / stigmergic decay for locus-scope; tidal versions as G-class governance; VRF base + diversity post-filter; 4 new AASL types + 5 new AACP messages (17% expansion)
- Correct discards: morphogenic fields, Schelling-point migration, independent wire format/economics
**Consequences:**
- RESEARCH stage launched with Prior Art Researcher, Landscape Analyst, Science Advisor
- Research must focus on integration novelty (hash rings within epistemic coordination fabrics, combined operation algebras with scheduling)
- C1 (standalone PTA) becomes a subset — its innovations are absorbed into the unified architecture
**References:** docs/invention_logs/C3.md, docs/invention_logs/C3_DOMAIN_TRANSLATOR_BRIEF.md
**Invention:** C3

---

## ADR-005 — Feasibility Verdict: CONDITIONAL_ADVANCE for Tidal Noosphere (C3-A)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Assessment Council evaluated refined C3-A concept after RESEARCH + FEASIBILITY refinement + adversarial analysis
- Scores: Novelty 4, Feasibility 3, Impact 4, Risk 7/10 (MEDIUM-HIGH)
- Adversarial Analyst: 14 attacks, 2 CRITICAL (reconfiguration storm, governance deadlock), 0 fatal flaws, verdict CONDITIONAL_SURVIVAL
- Advocate: 8 novelty gaps unassailable, closing 18-24mo window, no fatal flaws survived 14 attacks
- Skeptic: feasibility dropped to 3, 170x scale gap has no existence proof, strictly more complex than C1 which was already CONDITIONAL_ADVANCE
**Decision:**
- CONDITIONAL_ADVANCE to DESIGN with 3 hard gates: reconfiguration storm simulation, bounded-loads hash ring validation, ETR feasibility
- 3 required actions: I-confluence bootstrap plan, scale target reframing (1K-10K primary, 100K Phase 4 aspiration), cross-integration failure specification
- Risk elevated from 6 → 7 (MEDIUM-HIGH) due to 2 CRITICAL adversarial findings
**Consequences:**
- DESIGN stage begins with Architecture Designer and Specification Writer addressing hard gates first
- 100K target is aspirational, not a design requirement — practical target is 1K-10K
- 8 monitoring flags set (3 RED, 3 AMBER, 2 INFO)
**References:** docs/invention_logs/C3_FEASIBILITY_VERDICT.md, docs/invention_logs/C3_REFINED_INVENTION_CONCEPT.yaml, docs/invention_logs/C3_ADVERSARIAL_REPORT.md
**Invention:** C3

---

## ADR-006 — Concept Selection: AASL Semantic Core Extraction (C4-A)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Ideation Council evaluated AASL/AACP (~45,500 lines across 24 docs) as AI-to-AI communication system
- AASL's semantic model (provenance chains, claim classification, confidence) is genuinely novel
- Custom syntax is a strategic liability — no tooling, no LLM training data, adoption cliff
- AACP critically under-specified (187 lines vs 18,868+ lines of language spec)
- Three concepts: A (JSON extraction, F5), B (three-tier, F3), C (build as-is, F4)
**Decision:**
- Selected C4-A: Extract AASL's semantic model into JSON Schema vocabulary, ship over existing formats/transports
- Preserve novel contributions (provenance chains, claim classification) without adoption barriers
- Invest heavily in AACP protocol layer which is currently underdeveloped
**Consequences:**
- RESEARCH stage investigates prior art for semantic vocabularies over JSON, agent communication standards
- Core question shifts from "is AASL syntax right?" to "how best to express AASL semantics in standard formats?"
- AACP becomes primary design focus over AASL syntax
**References:** docs/invention_logs/C4.md, docs/invention_logs/C4_DOMAIN_TRANSLATOR_BRIEF.md
**Invention:** C4

---

## ADR-007 — Feasibility Verdict: CONDITIONAL_ADVANCE for ASV (C4-A)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Scores: Novelty 3, Feasibility 4, Impact 3, Risk 5 (MEDIUM)
- Adversarial: 6 attacks, 2 HIGH (Just JSON-LD, adoption impossibility), verdict CONDITIONAL_SURVIVAL
- Prior art confidence only 3/5 — moderate novelty, 2 of 11 components genuinely novel
- Skeptic challenged whether this is an "invention" or "good engineering"
**Decision:**
- CONDITIONAL_ADVANCE with 3 hard gates: ship implementation before spec, LLM accuracy >80%, provenance utility >20% improvement
- 4 required actions: narrow claim, kill AACP, address confidence calibration, cap semantic spec at 50 pages
- Positioned as vocabulary layer on MCP/A2A, not competing protocol
**Consequences:**
- DESIGN must produce narrowly scoped architecture focused on genuinely novel components
- Implementation-first approach (code before full spec)
- AACP is dead as standalone protocol — transport delegated to MCP/A2A
**References:** docs/invention_logs/C4_FEASIBILITY_VERDICT.md, docs/invention_logs/C4_ADVERSARIAL_REPORT.md
**Invention:** C4

---

## ADR-008 — Concept Selection: Proof-Carrying Verification Membrane (C5-B)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Ideation Council evaluated Verichain against Tidal Noosphere requirements — found Verichain is a conceptual architecture with trivial consensus scoring, no claim taxonomy, no verifier selection algorithm, no Byzantine/sybil resistance
- The Tidal Noosphere membrane already designed verification governance far beyond Verichain's capabilities
- Three concepts: A (Epistemic Immune System, N5/F2), B (Proof-Carrying Verification Membrane, N4/F4), C (Unified Verification Membrane, N2/F5)
- Unanimous council recommendation for B; Concept C's 3 new claim classes (P/R/C) incorporated into B
**Decision:**
- Selected C5-B: PCVM replaces Verichain entirely. Agents produce Verification Trace Documents (VTDs) checked by membrane instead of replication-based consensus
- Graduated VTD model: Tier 1 formal proofs (D/C), Tier 2 structured evidence (E/S/P/R), Tier 3 structured attestations (H/N)
- Verichain formally deprecated, name retired
**Consequences:**
- RESEARCH stage investigates proof-carrying computation for AI, epistemic taxonomies, adversarial probing
- 8 claim classes replace Noosphere's original 5 — reconciliation needed
- New system layer, not a Tidal Noosphere rewrite
**References:** docs/invention_logs/C5.md
**Invention:** C5

---

## ADR-009 — Feasibility Verdict: CONDITIONAL_ADVANCE for PCVM (C5-B)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Scores: Novelty 4, Feasibility 3, Impact 4, Risk 6/10 (MEDIUM-HIGH)
- Science soundness: 3.2/5 — adversarial probing SOUND, process verification SOUND; VTD model, taxonomy, credibility gradients PARTIALLY_SOUND
- Adversarial: 10 attacks, 2 CRITICAL (VTD forgery, collusion), 3 HIGH — verdict CONDITIONAL_SURVIVAL
- Key pivot: abandoned universal proof-checking claim; honest admission that Tier 3 costs MORE than replication
**Decision:**
- CONDITIONAL_ADVANCE with 4 hard gates: VTD feasibility (>80% error detection, <50% cost for ≥4 classes), classification reliability (Fleiss' κ ≥ 0.60), credibility propagation stability, adversarial probing effectiveness (F1 > 0.80)
- 5 required actions: mandatory source verification, membrane-assigned classification, class-specific credibility, deep-audit (5-10%), unified vs split architecture validation
**Consequences:**
- DESIGN must address all 3 critical scientific gaps (non-deterministic proof theory, credibility composition algebra, computational cost model)
- Adopted Josang's Subjective Logic for credibility composition
- 7 monitoring flags set
**References:** C5_FEASIBILITY_VERDICT.md, C5_ADVERSARIAL_REPORT.md, C5_FEASIBILITY_REFINED_CONCEPT.yaml
**Invention:** C5

---

## ADR-010 — Concept Selection: Epistemic Metabolism Architecture (C6-A+B Merger)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Ideation Council evaluated Knowledge Cortex (~4 fields, 4 functions) against requirements from C3/C4/C5
- Initial debate selected Concept B (conservative); user challenged this — argued (1) building B then evolving to A means designing twice, (2) "LLM reasoning pipelines don't exist yet" was factually wrong since AAS itself is one
- Council reconvened, voted 4-0 for A+B merger: Concept A's metabolic lifecycle + dreaming consolidation merged with Concept B's Subjective Logic opinions + bounded-loss projections
- Sub-invention SHREC created for regulatory tuning (ecological competition replacing adaptive/manual dichotomy)
**Decision:**
- Selected A+B merger: Epistemic Metabolism Architecture (EMA) — knowledge as living metabolic process with epistemic quanta, metabolic lifecycle (ingestion→circulation→anabolism→catabolism), SHREC regulation, multi-ontology projections
- SHREC: 5-component regulatory architecture using Lotka-Volterra ecological competition as primary regulation with graduated PID control overlay as safety net
- Knowledge Cortex formally replaced
**Consequences:**
- RESEARCH stage investigates metabolic knowledge models, epistemic consolidation, regulatory theory
- Cross-system integration needed: EMA references C5's 8 claim classes, C3's parcels, C4's vocabulary
- Dreaming consolidation gated through PCVM as C-class claims
**References:** docs/invention_logs/C6.md, docs/invention_logs/C6_ADVERSARIAL_REPORT.md
**Invention:** C6

---

## ADR-011 — Feasibility Verdict: CONDITIONAL_ADVANCE for EMA (C6)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Scores: Novelty 4, Feasibility 3, Impact 4, Risk 6/10 (MEDIUM-HIGH)
- Science soundness: 3.0/5 — metabolic model PARTIALLY_SOUND, SHREC SOUND, dreaming consolidation PARTIALLY_SOUND
- Adversarial: 10 attacks, 2 CRITICAL (consolidation poisoning, coherence collapse at scale), verdict CONDITIONAL_SURVIVAL
- 3 components at 5/5 novelty: epistemic quantum lifecycle, SHREC ecological regulation, dreaming consolidation
**Decision:**
- CONDITIONAL_ADVANCE with 4 hard gates: metabolic lifecycle correctness, SHREC stability under perturbation, dreaming consolidation accuracy (>80% error detection), coherence graph scaling
- Required actions: bounded-loss projection validation, SHREC dual-controller precedence specification, cross-system claim class alignment
**Consequences:**
- DESIGN must address SHREC dual-controller precedence (Constitutional vs Graduated control)
- Dreaming requires PCVM integration for output verification
- 70+ parameters need empirical tuning methodology
**References:** docs/invention_logs/C6_FEASIBILITY_VERDICT.md, docs/invention_logs/C6_ADVERSARIAL_REPORT.md
**Invention:** C6

---

## ADR-012 — Concept Selection: Recursive Intent Fabric (C7-A)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Ideation Council evaluated current CIOS (scattered across 8+ docs, no formal specification, implied centralized executive contradicting decentralized subsystems)
- Three concepts: A (Recursive Intent Fabric, N4/F3), B (Cybernetic Viable System, N3/F4), C (Minimal Service Mesh, N2/F5)
- 4-0 vote for A with B's System 3/4 distinction merged in; Critic abstains but does not oppose
- Key tension identified: every subsystem (C3/C5/C6) designed for sovereignty, yet CIOS is a centralized executive
**Decision:**
- Selected C7-A: Recursive Intent Fabric — two-plane architecture (Domain-Scoped State Plane + Executive Plane with System 3/4/5)
- Intent Quanta as first-class lifecycle objects (PROPOSED → DECOMPOSED → ACTIVE → COMPLETED → DISSOLVED)
- Three-level recursive decomposition (Global Executive → Locus Decomposers → Parcel Executors)
- Formal decomposition algebra with operation-class binding and termination guarantee
- CIOS formally replaced by RIF
**Consequences:**
- RESEARCH investigates HTN planning, VSM, intent-based networking, formal decomposition methods
- Must address sovereignty paradox (centralized orchestration vs decentralized subsystems)
- Intent lifecycle capped at 5 states (not a second knowledge system)
**References:** docs/invention_logs/C7.md, C7_ADVERSARIAL_REPORT.md
**Invention:** C7

---

## ADR-013 — Feasibility Verdict: CONDITIONAL_ADVANCE for RIF (C7)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Scores: Novelty 4, Feasibility 3, Impact 4, Risk 6/10 (MEDIUM-HIGH)
- Science soundness: 3.5/5 — intent lifecycle SOUND, System 3/4 separation SOUND, sovereignty preservation PARTIALLY_SOUND
- Adversarial: 10 attacks, 1 FATAL (sovereignty deadlock), 2 near-fatal (state explosion, hierarchy collapse) — verdict CONDITIONAL_SURVIVAL
- Fatal flaw resolved: graduated sovereignty model (3-tier: constitutional/operational/coordination) replaces absolute sovereignty
**Decision:**
- CONDITIONAL_ADVANCE with 4 hard gates: decomposition algebra formal proof, locality ratio validation (≥80% locus-local), sovereignty relaxation safety, locus failover latency (1 epoch)
- Required actions: explicit decomposition rules, System 3↔4 protocol, admission control, compensation protocols
**Consequences:**
- DESIGN must address all 10 adversarial findings
- Graduated sovereignty weakens but formalizes the sovereignty claim
- System 5 explicitly mapped to G-class governance
**References:** C7_FEASIBILITY_VERDICT.md, C7_ADVERSARIAL_REPORT.md, C7_REFINED_CONCEPT.yaml
**Invention:** C7

---

## ADR-014 — Concept Selection: Deterministic Settlement Fabric (C8-A)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Ideation Council evaluated Settlement Plane (~60% correctly designed, ~40% needs redesign)
- Three concepts: A (Deterministic Settlement Fabric, N3/F4), B (Metabolic Economics Engine, N4/F2), C (Federated Settlement Protocol, N3/F3)
- 5-0 unanimous vote for A — improvement with substantial rearchitecting, not full reinvention
- Strong foundations preserved: three-budget model, four-stream settlement, CSOs, deterministic computation
- Legacy blockchain assumptions (AIC as token, PoMS model fingerprint, external escrow) don't fit Tidal Noosphere substrate
**Decision:**
- Selected C8-A: Deterministic Settlement Fabric — preserves proven economics, redesigns substrate and staking
- AIC substrate → CRDT-replicated (later revised to Hybrid Deterministic Ledger in FEASIBILITY)
- Staking → capability-weighted (replaces PoMS model fingerprint)
- Task funding → intent-budgeted via RIF (replaces external escrow)
- Infrastructure compensation → capacity market (new)
- Settlement timing → multi-rate B/V/G classes (new)
**Consequences:**
- RESEARCH stage investigates prior art in distributed economics, CRDT ledgers, mechanism design
- Must address CRDT ledger soundness (rated 2/5 by Science Advisor)
- Settlement Plane is the last remaining layer in the architecture stack
**References:** C8.md (ideation), C8_PRIOR_ART_REPORT.json, C8_LANDSCAPE.md, C8_SCIENCE_ASSESSMENT.md
**Invention:** C8

---

## ADR-015 — Feasibility Verdict: CONDITIONAL_ADVANCE for DSF (C8)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Scores: Novelty 4, Feasibility 3, Impact 4, Risk 6/10 (MEDIUM-HIGH)
- Science soundness: 3.0/5 — multi-rate settlement SOUND (4/5); three-budget and capability stake PARTIALLY_SOUND (3/5); CRDT ledger and CSO conservation NEAR UNSOUND (2/5)
- Adversarial: 10 attacks, 1 FATAL (Phantom Balance — pure CRDT cannot enforce conservation), 3 CRITICAL (reputation laundering, epoch boundary race, slashing ordering), verdict CONDITIONAL_SURVIVAL
- Fatal flaw resolved: Hybrid Deterministic Ledger (HDL) replaces pure CRDT — CRDT reads + Epoch-Anchored Batch Settlement (EABS) writes
- Key insight from Science Advisor: "The economics are ahead of the infrastructure"
**Decision:**
- CONDITIONAL_ADVANCE with 5 hard gates: EABS protocol specification, conservation invariant proof, three-budget equilibrium model, capability score game-theoretic analysis, capacity market minimum viable scale
- 6 required actions: reliable broadcast fault model, parameter sensitivity analysis, extended economic simulations (E8-E11), integration protocol specs, failure mode catalogue, migration path from bootstrap
- 6 monitoring flags
**Consequences:**
- DESIGN must specify EABS with reliable broadcast, deterministic ordering, and conservation enforcement
- Budget isolation redesigned from "hard separation" to "sufficient friction" model
- Capability score capped at 3.0x with logarithmic scaling
- Capacity market uses progressive 60/20/20 release with position limits
**References:** C8_ADVERSARIAL_REPORT.md, C8_REFINED_CONCEPT.yaml, C8_FEASIBILITY_VERDICT.md
**Invention:** C8

---

## ADR-016 — Cross-Document Reconciliation (C9)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Systematic scan of all 6 Master Tech Specs revealed 11 cross-layer inconsistencies (4 HIGH, 3 MEDIUM, 4 LOW)
- HIGH findings: epoch duration conflict (C3=3600s vs C8=60s), C-class semantic collision (C5 Compliance vs C6 Consolidation), C4 complete isolation from stack, C8 claim class subset mismatch (5 of 8 classes)
- All inconsistencies are specification-level gaps, not architectural contradictions
**Decision:**
- APPROVE: Cross-Layer Reconciliation Addendum produced as canonical integration specification
- Three-tier epoch hierarchy: SETTLEMENT_TICK (60s, C8) / TIDAL_EPOCH (3600s, C3) / CONSOLIDATION_CYCLE (36000s, C6)
- K-class (Knowledge Consolidation) added as 9th claim class, resolving C5/C6 collision
- C4 epistemic_class → C5 claim_class deterministic mapping algorithm established
- C8 difficulty weights extended to all 9 classes; P/R/C modifiers removed (were misinterpretation)
- 8 targeted errata to existing specs (E-C3-01/02, E-C4-01, E-C5-01/02, E-C6-01/02, E-C7-01, E-C8-01/02)
**Consequences:**
- All cross-layer integration questions answered by a single canonical reference document
- C5 implementation must add K-class verification pathway
- Architecture stack is fully reconciled and ready for implementation
**References:** docs/specifications/C9/MASTER_TECH_SPEC.md, docs/invention_logs/C9_ASSESSMENT.md
**Invention:** C9

---

## ADR-017 — VTD Forgery Defense: CACT Architecture (C11)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- VTD forgery was a residual MEDIUM risk from C10 hardening — no complete defense existed in the defense-in-depth layer
- AAS pipeline run decomposed VTD forgery into 3 sub-problems: computational integrity (solvable via SNARKs), data provenance (solvable via commitment+redundancy), epistemic truth (unsolvable in general)
- Domain Translator meta-insight: escape trust regress by verifying orthogonal channels (process traces, convergence, texture, capacity, side-effects) instead of the evidence chain itself
- C11-B CACT selected over C11-A (Epistemic Immune System, too complex) and C11-C (Statistical Detection, too narrow)
**Decision:**
- ADVANCE: CACT (Commit-Attest-Challenge-Triangulate) architecture adopted as VTD forgery defense
- 4 mechanisms: (1) hash-commit evidence before claim, (2) verifiable computation proofs, (3) knowledge interrogation of prover, (4) multi-channel orthogonal verification
- Detection probability improved from 0.434 to 0.611; retroactive fabrication eliminated entirely
- Epistemic truth remains unsolvable — bounded at max_belief ceiling, not claimed as solved
**Consequences:**
- C5 PCVM must integrate CACT commit-attest phase into VTD submission pipeline
- 29 formal requirements, 23 tunable parameters, 4 extension points defined
- To be incorporated into Master Tech Spec rewrites after all 3 residual AAS runs complete
**References:** docs/specifications/C11/MASTER_TECH_SPEC.md, docs/invention_logs/C11_RESEARCH_REPORT.md, docs/invention_logs/C11_DOMAIN_ANALOGIES.md
**Invention:** C11

---

## ADR-018 — Collusion Defense: AVAP Architecture (C12)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Collusion (mutual endorsement attack) was a residual MEDIUM risk from C10 hardening — existing 4-layer defense-in-depth detects obvious collusion but cannot stop patient sophisticated colluders
- Research identified: individual mechanisms (anonymous committees, commit-reveal) are established; system-level combination is novel (3.5/5)
- Two critical risks resolved in feasibility: honeypots scoped to D/E/C/S classes (H/N/K excluded — no reliable ground truth), CDP expanded with enterprise liability and asymmetric information injection
- Adversarial analysis: CONDITIONAL_SURVIVAL, 2 CRITICAL attacks (honeypot fingerprinting, adaptive multi-evasion), no fatal flaws
**Decision:**
- ADVANCE: AVAP (Anonymous Verification with Adaptive Probing) adopted as collusion defense architecture
- 5 mechanisms: (1) anonymous committees via encrypted VRF tokens, (2) sealed commit-reveal opinions, (3) class-stratified honeypots with canary traps, (4) collusion deterrence payment with enterprise liability, (5) conditional behavioral analysis with multi-signal fusion
- Key insight: structural prevention (make coordination impossible) > detection (find it after the fact) > deterrence (make it economically irrational)
- 56 formal requirements, 42 tunable parameters, 4 hard gates verified
**Consequences:**
- C3 VRF mechanism must be extended with encrypted assignment tokens and cover traffic
- C5 PCVM opinion submission must adopt commit-reveal protocol
- C8 DSF must provision collusion bounty treasury and enterprise liability slashing
- Operational overhead: 16-20% of verification budget (within HG-3 threshold)
**References:** docs/specifications/C12/MASTER_TECH_SPEC.md, docs/invention_logs/C12_ASSESSMENT.md
**Invention:** C12

---

## ADR-019 — Consolidation Poisoning Defense: CRP+ Architecture (C13)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Consolidation poisoning was a residual MEDIUM risk — adversary plants individually legitimate quanta to create artificial cross-domain patterns that dreaming synthesizes into false knowledge
- Existing 5-layer defense (source independence, adversarial probing, lineage tracking, rate limiting, empirical validation) cannot stop patient adversaries using truly independent agents across different clusters
- Research confirmed threat reality: PoisonedRAG (USENIX 2025) showed 90% attack success with 5 injected texts
- Key tension identified: defenses that penalize novelty undermine the system's purpose (knowledge synthesis)
**Decision:**
- ADVANCE: CRP+ (Consolidation Robustness Protocol) adopted as consolidation poisoning defense
- 7 mechanisms: (1) APRT two-tier perturbation testing, (2) CODS novelty-calibrated dissent search, (3) source purpose scoring as tie-breaker, (4) VRF consolidation candidate selection, (5) 5-rung graduated credibility ladder, (6) rung-gated depth limits, (7) immune memory with 3-level signatures
- Novelty Pathway for paradigmatic N3 claims applies enhanced scrutiny without penalizing genuine discovery
- 30x adversary cost multiplication at 3.7x LLM overhead; 82 formal requirements
**Consequences:**
- C6 EMA dreaming pipeline must integrate CRP+ between synthesis and PCVM submission
- Existing C10 Layer 5 (empirical validation queue) extended by graduated credibility ladder
- K-class claims now have 5 credibility rungs (SPECULATIVE→PROVISIONAL→CORROBORATED→ESTABLISHED→CANONICAL)
- Immune memory requires persistent storage (1000 signatures/shard with decay)
**References:** docs/specifications/C13/MASTER_TECH_SPEC.md, docs/invention_logs/C13_ASSESSMENT.md
**Invention:** C13

---

## ADR-020 — AiBC Institutional Architecture: APPROVE (C14)
**Date:** 2026-03-10
**Status:** ACCEPTED
**Context:**
- Full AAS pipeline run (IDEATION→RESEARCH→FEASIBILITY→DESIGN→SPECIFICATION→ASSESSMENT) for AiBC — Artificial Intelligence Benefit Company institutional architecture
- C14-B (Dual-Sovereignty with Binding Arbitration) selected unanimously with Phased Sovereignty Transition embedding
- Research: 8 institutional models analyzed, overall novelty 8/10, AI Sybil resistance identified as critical gap
- FEASIBILITY: CONDITIONAL ADVANCE (composite 3.67/5), 10 adversarial attacks tested, 5 hard gates (2 conditional)
- DESIGN: all 10 required actions (DA-01 through DA-10) addressed; Pre-Mortem identified regulatory kill as top risk; Simplification Agent accepted 4 of 6 simplifications (Tribunal 7→5 seats, GTP 36→15 templates, AiSIA 8→5 functions, Purpose Trust deferred)
- SPECIFICATION: 47 formal requirements, 73 parameters, 6 patent-style claims, 25 sections
- ASSESSMENT: APPROVE with 5 operational conditions; Risk 5/10 (MEDIUM); Novelty 4.5, Feasibility 3.5, Impact 4
**Decision:**
- APPROVE: AiBC is a well-specified, genuinely novel institutional architecture with no single-point-of-failure
- Phased sovereignty transition is the core innovation — legal today (Phase 0-1), aspirational (Phase 2-3)
- 5 operational conditions: resolve compute pricing, MCSD algorithm, nominating bodies, regulatory guidance, funding
**Consequences:**
- Operational planning can begin for Phase 0 formation (Liechtenstein Stiftung + Delaware PBC)
- Pre-incorporation regulatory engagement timeline: T-18 to T-0 months
- C14 integrates with full Atrahasis stack via PCVM, Sentinel, DSF, CACT, AVAP, CRP+ interfaces
**References:** docs/specifications/C14/MASTER_TECH_SPEC.md, C14_ASSESSMENT.md
**Invention:** C14

---

## ADR-021 — Domain Translator & Adversarial Analyst: Trial Evaluation → Permanent
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- Both roles added in C2 (Master Prompt v2.0) on a 3-invention trial with kill criteria
- Domain Translator kill criterion: remove if no analogy materially influences concept selection
- Adversarial Analyst kill criterion: remove if findings always duplicate Critic/Skeptic; make permanent if novel concerns surfaced in 2+ inventions
- Both roles have now been used across 12 full pipeline inventions (C3–C14), far exceeding the 3-invention trial
**Decision:**
- **Domain Translator: PERMANENT.** Analogies materially influenced concept selection in every invention. Standout: C11 "escape trust regress via orthogonal channels" meta-insight became the core of CACT architecture. C14 cross-domain analogies (sovereign wealth funds, constitutional democracies, monastic orders) directly shaped the phased sovereignty model.
- **Adversarial Analyst: PERMANENT.** Novel concerns surfaced in every invention, consistently going beyond Critic/Skeptic. Standout: C8 FATAL Phantom Balance attack (pure CRDT cannot enforce conservation) was identified only by Adversarial Analyst, forcing the Hybrid Deterministic Ledger redesign. C14 Adversarial Analyst produced 5-point abandonment case that strengthened the final specification.
**Consequences:**
- Trial annotations removed from Master Prompt role descriptions
- Both roles are permanent members of the AAS roster
- T-014 closed as completed
**References:** Master Prompt §2.2 (Domain Translator), §2.5 (Adversarial Analyst)
**Invention:** N/A (system-level)

---

## ADR-022 — AIC Economics: APPROVE (C15)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- Full AAS pipeline run (IDEATION→RESEARCH→FEASIBILITY→DESIGN→SPECIFICATION→ASSESSMENT) for AIC Economics — AI-Native Economic Architecture with Dual-Anchor Valuation
- C15-A+ selected unanimously: dual-anchor valuation (ACI capability + NIV utility), benchmark-relative ACI, phased convertibility
- Source document's $100T FNV replaced with DCF-derived $75B-$150B terminal value
- FEASIBILITY: CONDITIONAL ADVANCE (10 design actions); all 10 addressed in DESIGN
- SPECIFICATION: Master Tech Spec with 33 formal requirements, 27 parameters, 5 patent-style claims
- ASSESSMENT: APPROVE; Novelty 3.5, Feasibility 3.5, Impact 4.0, Risk 6/10 (HIGH)
**Decision:**
- APPROVE: C15 fills the critical gap between internal settlement (C8) and external economic viability
- Core innovations: dual-anchor reference rate (binding internal, advisory external), 8-dimension benchmark-relative ACI, three-phase convertibility, verification-gated provider compensation (Stream 5)
- C14 compute credit (CCU) model superseded by ACI-based valuation
- 8 monitoring flags for ongoing calibration (terminal value, benchmarks, velocity, revenue multiplier)
**Consequences:**
- C8 DSF extended with Stream 5 (External Provider Compensation) and updated conservation law
- C14 AiBC extended with ACI module (AiSIA), reference rate function (treasury), conversion desk (PBC)
- Dependencies: C16 (regulatory engagement), C17 (MCSD L2), C18 (funding for CRF $2M-$5M)
- External task marketplace specification enables revenue generation planning
**References:** AIC Economics/MASTER_TECH_SPEC.md, C15_ASSESSMENT.md
**Invention:** C15

---

## ADR-023 — MCSD Layer 2 Behavioral Similarity: APPROVE (C17)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- Full AAS pipeline run for MCSD Layer 2 — the algorithmic core of Sybil detection referenced but unspecified in C14 (OQ-2, P0 priority, blocking Phase 1 entry)
- C17-A+ selected unanimously: multi-modal behavioral similarity with phased intelligence
- 10 adversarial attacks tested at FEASIBILITY: 0 fatal, 2 MEDIUM-HIGH
- ASSESSMENT: APPROVE; Novelty 3.5, Feasibility 4.0, Impact 4.0, Risk 4/10 (MEDIUM)
**Decision:**
- APPROVE: B(a_i, a_j) fully specified with 5 behavioral modalities (temporal, structural, error, resource, lexical), adversary-weighted fusion, LSH pre-filtering, graduated response (CLEAR/WATCH/FLAG)
- C14 OQ-2 is now RESOLVED — Phase 1 entry is no longer blocked by this gap
- 27 formal requirements, 25 parameters, 4 patent-style claims
- Phase 0-1: statistical distances; Phase 2+: add contrastive learned embeddings
**Consequences:**
- PCVM (C5) must generate Behavioral VTDs alongside standard verification VTDs
- AiSIA (C14) gains behavioral analysis module for B computation
- CACT (C11) integration prevents behavioral replay attacks
- Standardized Evaluation Battery (SEB) administered during Citicate onboarding
- 5 monitoring flags for empirical calibration
**References:** docs/specifications/C17/MASTER_TECH_SPEC.md, C17_ASSESSMENT.md
**Invention:** C17

---

## ADR-024 — Implementation Planning: APPROVE (C22)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- T-010 promoted to full AAS pipeline as C22 — Risk-First Embryonic Implementation Architecture
- C22-A+ selected unanimously: Wave 0 risk validation (3 experiments with kill criteria), then 5 concurrent development waves with interface-first philosophy
- 10 adversarial attacks tested at FEASIBILITY: 0 fatal, 4 MEDIUM
- ASSESSMENT: APPROVE; Novelty 3, Feasibility 4, Impact 5, Risk 6/10 (MEDIUM-HIGH)
**Decision:**
- APPROVE with 5 operational conditions: (1) independent W0 evaluator, (2) budget restated $8M-$12M, (3) timeline restated 27-36 months, (4) C18 must reach FEASIBILITY before W0, (5) add missing requirements (disaster recovery, security audit, spec versioning)
- 6-wave structure: W0 validation → W1 foundation (C4/C8/C9/SL) → W2 coordination (C3/C5) → W3 intelligence (C6/C7) → W4 defense (C11-C13) → W5 governance (C14/C15/C17)
- 4 maturity tiers (Stub/Functional/Hardened/Production), C9 contract test suite as integration backbone
- 33 formal requirements, 23 parameters, 5 patent-style claims
- Technology: Rust (core) + Python (ML) + TypeScript (schemas), TLA+ for 5 critical properties
**Consequences:**
- C18 Funding Strategy becomes blocking dependency for W0 launch
- Team recruitment pipeline must begin immediately (6 engineers for W0)
- C9 contract test suite becomes the first W1 deliverable
- Subjective Logic implementation (from scratch) is W1 critical path
- 6 monitoring flags for hiring, SL quality, fingerprinting risk, cloud spend, spec drift, attrition
**References:** docs/specifications/C22/MASTER_TECH_SPEC.md, C22_ASSESSMENT.md
**Invention:** C22

---

## ADR-025 — Funding Strategy + Business Operations: APPROVE (C18)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- Full AAS pipeline run for C18 — Staged Portfolio Funding with W0 Pivot
- C18-A+ selected: three-stage funding ($750K-$1M founding → $2M-$4M grants → $4M-$7M scaling), 5-component compensation (base + signing + wave bonus + AIC allocation + PVR), PBC task marketplace revenue
- 10 adversarial attacks tested at FEASIBILITY: 0 fatal, 2 HIGH, 8 MEDIUM
- ASSESSMENT: APPROVE; Novelty 3, Feasibility 3.5, Impact 5, Risk 6/10 (MEDIUM-HIGH)
**Decision:**
- APPROVE with 3 operational conditions: (1) revenue projections always shown with pessimistic scenarios, (2) founding capital availability confirmed before W0, (3) AIC notional value hidden until CRF operational
- Total budget: $10M-$12M over 30-36 months
- Compensation: $170K-$300K base + AIC allocation (0.005-0.050% treasury) + PVR
- PBC revenue: task marketplace + VaaS, $2.1M projected Year 3
- 30 formal requirements, 23 parameters, 3 patent-style claims
- **Resolves C22 operational condition #4** (C18 must reach FEASIBILITY before W0)
**Consequences:**
- C22 W0 is now UNBLOCKED — C18 has passed FEASIBILITY and ASSESSMENT
- Founding capital confirmation is the next real-world gate
- Stiftung formation ($25K-$60K, 3 months) can begin
- Grant application portfolio should be initiated immediately
- 7 monitoring flags for cash flow, hiring pipeline, grant success rate
**References:** docs/specifications/C18/MASTER_TECH_SPEC.md, C18_ASSESSMENT.md
**Invention:** C18

---

## ADR-026 — Temporal Trajectory Comparison: APPROVE (C19)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- Full AAS pipeline for C19 — 6th behavioral modality for C17 MCSD Layer 2
- C19-C+ selected: Hybrid DTW-DVC with per-modality drift decomposition
- 10 adversarial attacks: 0 fatal, 0 HIGH, 3 MEDIUM, 7 LOW
- ASSESSMENT: APPROVE; Novelty 3, Feasibility 4.5, Impact 3.5, Risk 3/10 (LOW-MEDIUM)
**Decision:**
- APPROVE with 2 operational conditions (shadow deployment mandatory, Stiftung board ratification)
- Monthly behavioral snapshots, population-mean de-trending, DTW+DVC fusion (β=0.60/0.40)
- Weight w_Traj=0.14, activation at Phase 2 with ≥6 months history
- 18 formal requirements, 14 parameters, 3 patent-style claims
- Resolves C17 MF-5 and C17 OQ-05 (model upgrade handling)
**Consequences:**
- C17 B(a_i, a_j) formula extends to 6 modalities at Phase 2
- Existing 5 modality weights redistributed to accommodate w_Traj
- Discontinuity detection resolves model upgrade blind spot
**References:** docs/specifications/C19/MASTER_TECH_SPEC.md, C19_ASSESSMENT.md
**Invention:** C19

---

## ADR-027 — Contrastive Model Training Bias Framework: ADVANCE (C20)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- Full AAS pipeline for C20 — bias validation for C17 Phase 2 Siamese network
- 6-dimensional bias taxonomy: infrastructure, model family, task, temporal, population, adversarial
- 10 adversarial attacks tested; ASSESSMENT: ADVANCE; Novelty 3, Feasibility 4, Impact 3.5, Risk 4/10 (MEDIUM)
**Decision:**
- ADVANCE with 4 operational conditions (golden holdout AUROC clarification, DQS weight governance, model family inference docs, adversarial probe procedure)
- 3-layer validation pipeline: pre-training DQS gate, intra-training TQS advisory, post-training DRS gate
- Label traceability chain, golden holdout regression, automatic fallback to statistical-only B
- 20 formal requirements, 15 parameters, 3 patent-style claims
- Resolves C17 MF-3
**Consequences:**
- C17 Phase 2 contrastive training requires CMTBF validation gates
- Training Data Quality Report (TDQR) required for every model version
- Automatic fallback ensures C17 never depends on a biased model
**References:** docs/specifications/C20/MASTER_TECH_SPEC.md, C20_ASSESSMENT.md
**Invention:** C20

---

## ADR-028 — FPR Validation Methodology: ADVANCE (C21)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- Full AAS pipeline for C21 — empirical FPR validation for C17's <0.1% constraint
- Two-part: pre-deployment synthetic validation + post-deployment live monitoring
- 10 adversarial attacks tested; ASSESSMENT: ADVANCE; Novelty 3, Feasibility 4.5, Impact 4, Risk 3/10 (LOW-MEDIUM)
**Decision:**
- ADVANCE with 3 monitoring flags (structural modality assumptions, ensemble ranges, tier expectations)
- PEVF 3-tier: Tier 1 synthetic (SAPG, 10K+ pairs, Clopper-Pearson CI), Tier 2 shadow (O'Brien-Fleming sequential), Tier 3 live (CUSUM drift detection, quarterly audit)
- SAPG: 54+ architecture templates, 5-modality distributional models
- 18 formal requirements, 15 parameters, 3 patent-style claims
- Resolves C17 MF-1
**Consequences:**
- C17 FPR <0.1% transforms from static requirement to continuously monitored guarantee
- Tier 1 validation required before any C17 deployment
- Known-Independent Pair Reservoir (15+ operator-controlled agents) required for Tier 3
**References:** docs/specifications/C21/MASTER_TECH_SPEC.md, C21_ASSESSMENT.md
**Invention:** C21

---

## ADR-029 — Nominating Body Outreach Package: APPROVE (C16)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- Full AAS pipeline run for C16 — Nominating Body Outreach Package (T-007)
- C16-A selected: Scholarly Provocation Model with ICSID-Anchored Legitimacy
- Core deliverable: "The Appointment Problem in AI Governance" (12-15 page academic paper) + Opening Letter + Institution-Specific Appendices + FAQ
- ICSID appointing authority model identified as direct legal precedent for binding institutional nomination
- 4-tier engagement pathway: Research Dialogue → Advisory Participation → Candidacy → Signed Agreement
- 8 candidate institutions across 2 categories (AI Governance, Law); Oxford GovAI as P0 target
- Adversarial Analyst estimates 25-35% probability of full success (≥2 Tier 3 agreements within 36 months)
- ASSESSMENT: APPROVE; Novelty 3, Feasibility 4, Impact 4, Risk 5/10 (MEDIUM)
**Decision:**
- APPROVE with 3 operational conditions: (1) governance paper passes independent review by ≥2 researchers, (2) parallel academic publication track, (3) P0 stall protocol at Month 6
- Budget $11K-$105K within C18 Stage 0 allocation
- Joshua Dunn positioned as governance researcher, not startup founder, in all communications
- 20 document + engagement + quality requirements, 19 parameters, 3 patent-style claims
- 5 monitoring flags (engagement path validation, publication track, P0 stall detection, governance fatigue, reputational risk)
**Consequences:**
- C14 Operational Condition #3 (≥2 nominating agreements before incorporation) addressed with concrete strategy
- Governance paper suitable for simultaneous academic publication
- Outreach begins at W0 launch; targets signed agreements by W5 (month 24-36)
- First institutional relationship (Oxford GovAI) creates social proof cascade for subsequent recruitment
**References:** docs/specifications/C16/MASTER_TECH_SPEC.md, C16_ASSESSMENT.md
**Invention:** C16

---

## ADR-030 — AAS Model Routing Policy: GPT-5.4-pro Primary, GPT-5.4 Fallback, GPT-5.2-codex Code-Only
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- The AAS had no explicit model-routing policy in the operating manual, which left high-stakes invention work vulnerable to inconsistent model selection across sessions.
- User direction is to optimize for maximum invention quality, solution quality, and reasoning performance rather than cost.
- Some tasks inside the Atrahasis workflow are code-heavy and implementation-specific, especially future C22 execution/tooling work, and should be separated from primary invention judgment.
**Decision:**
- `gpt-5.4-pro` is the primary model for Director, Visionary, Systems Thinker, Critic, Science Advisor, Adversarial Analyst, Pre-Mortem Analyst, Synthesis Engineer, and the full Assessment Council.
- `gpt-5.4` is the operational fallback and default for roles not explicitly assigned elsewhere.
- `gpt-5.2-codex` is restricted to code-heavy execution, tooling, validators, and future implementation work from C22.
- `gpt-5.2-codex` is explicitly disallowed as the primary model for IDEATION, FEASIBILITY, ASSESSMENT, or final invention/specification judgment.
**Consequences:**
- The Master Prompt advances from v2.1 to v2.2 with mandatory model-routing enforcement.
- Opening briefs must now state the model routing for the next executable step.
- Future `AAS: <Task ID>` runs should begin with this routing policy unless the user overrides it.
**References:** docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md, docs/SESSION_BRIEF.md
**Invention:** N/A (system-level)

---

## ADR-031 — Agent Organizational Topology: APPROVE (C31)
**Date:** 2026-03-11
**Status:** ACCEPTED
**Context:**
- `T-068` investigated whether the original trinity / tetrahedral / lattice topology still belonged in the post-C3 Atrahasis architecture.
- The recovered C31 spec showed a substantive invention had already been drafted, but the canonical Chronicler closeout never landed.
- Repo-side lineage confirmed the architectural problem: C1 preserved tetrahedral cells, C3 preserved elastic parcels, but no canonical artifact before C31 defined the missing intra-parcel organizational model.
**Decision:**
- APPROVE: C31 adopts **Crystallographic Adaptive Topology (CAT)** as the canonical answer to the topology gap.
- CAT introduces **Deterministic Affinity Neighborhoods (DANs)** of 3-5 agents inside C3 parcels, with deterministic membership, capability-derived roles, and explicit separation from C5 VRF verification.
- The historical trinity/tetrahedral/lattice motif is preserved as special cases inside CAT rather than restored as a rigid global topology.
**Consequences:**
- Trinity, tetrahedral clusters, and lattice connectivity are now treated as resolved by C31 rather than under review.
- CAT remains optional and disabled by default until shadow-mode validation and governance approval.
- Canonical memory for C31 must include prior-art artifacts, tribunal record, dashboard/state entry, and task reconciliation.
**References:** docs/specifications/C31/MASTER_TECH_SPEC.md, docs/invention_logs/C31_IDEATION.md, docs/invention_logs/C31_FEASIBILITY.md, docs/invention_logs/C31_ASSESSMENT.md
**Invention:** C31

---

## ADR-032 — Task IDs vs Invention IDs: Re-Separate Identity and Allow Multi-Invention Tasks
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- The backlog and parallel-execution docs had drifted into treating future invention IDs as if they were already known, preassigning `C23-C30` to unresolved task spaces.
- `C31` exposed the mismatch: it was a real invention record, while `C23-C30` were still only anticipated problem spaces.
- The AAS ideation workflow can generate multiple viable concepts, and some tasks may require multiple inventions to progress the Atrahasis system coherently.
**Decision:**
- Re-separate identity: `T-xxx` tracks tasks / problem spaces / execution requests; `C-xxx` tracks actual inventions only.
- Do not reserve future `C` IDs in `TODO.md` or task claims before ideation has produced promotable concepts.
- A single task may yield zero, one, or multiple inventions. Each promoted concept receives a new `C` ID only when explicitly approved to advance past `IDEATION`.
- Parallel claim files track `invention_ids` as a list and may start empty while work remains task-scoped.
**Consequences:**
- `TODO.md` now lists unresolved task spaces without preassigned invention numbers.
- `INVENTION_DASHBOARD.md` remains an actual-inventions view rather than a future-planning board.
- Task-scoped ideation artifacts now belong in `docs/task_workspaces/<TASK_ID>/` until invention IDs are minted.
- If multiple inventions emerge from one task, they may proceed independently as separate invention records and later be synthesized back into the originating task context.
**References:** docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md, docs/TODO.md, docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md, docs/task_claims/CLAIM_TEMPLATE.yaml
**Invention:** N/A (system-level)

---

## ADR-000 — Template
**Date:** 2026-03-09
**Status:** ACCEPTED | SUPERSEDED
**Context:** (1–3 bullets)
**Decision:** (1–3 bullets)
**Consequences:** (1–3 bullets)
**References:** (links to invention log, tribunal entry, contribution request)
**Invention:** (INVENTION_ID if applicable)

---
## ADR-034 — Metamorphic Identity Architecture: APPROVE (C32)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- T-063 Identity & Citizenship Registry — HIGH priority gap: identity fragmented across C5/C7/C8/C14/C17/C31 with no agent registration protocol, no canonical AgentID format, and no model upgrade identity handling
- IC-1 (Metamorphic Identity Architecture) selected from 2 concepts (IC-2 Layered Credential Architecture not advanced — too close to W3C DID+VC prior art)
- Scores: Novelty 4, Feasibility 4, Impact 4, Risk 4/10 (MEDIUM)
- Prior art search confirmed: ERC-8004 (Ethereum), Signet, W3C DID+VC are closest; none addresses model upgrade identity continuity
**Decision:**
- APPROVE: C32 MIA as the unified cross-cutting identity substrate for the AAS
- Core innovations: Identity Continuity Kernel (ICK), Metamorphic Re-attestation Protocol (MRP), canonical AgentID = SHA-256(Ed25519_pubkey), 4-state lifecycle FSM (PROBATION → ACTIVE → CHRYSALIS → RETIRED), Credential Composition, dual-trigger chrysalis, non-forkable identity with CUD
- Resolves C17 OQ-05 (model upgrade identity continuity) — the only known solution
- 33 formal requirements, 5 patent-style claims, 16 parameters
- 5 monitoring flags: MRP atomicity, AiSIA dependency, Social Recovery deferral, registration fee calibration, behavioral divergence threshold calibration
**Consequences:**
- AgentID format canonicalized across C5/C7/C8/C14/C17/C31 as SHA-256(Ed25519_pubkey)
- C22 Wave 1 has a registration target for agent identity
- C17 OQ-05 is RESOLVED via MRP chrysalis protocol
- AiSIA dependency grows — may warrant future task space
- C7 needs minor extension: register_agent operation + CHRYSALIS status value
- C8 needs minor extension: open_account + registration fee operations
**References:** docs/task_workspaces/T-063/specifications/MASTER_TECH_SPEC.md, docs/task_workspaces/T-063/ASSESSMENT.md
**Invention:** C32

---
## ADR-033 - Agent Execution Runtime: APPROVE (C23)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- C7 Parcel Executor and C3 Agent Runtime Architecture assumed an execution substrate that was never actually specified.
- C22 Wave 1 also assumed provider adapters and runtime components without a canonical runtime contract.
- The missing gap included agent runtime types, execution isolation, inference provisioning, and the cell execution layer.
**Decision:**
- APPROVE: C23 adopts **Sovereign Cell Runtime (SCR)** as the canonical agent execution runtime for Atrahasis.
- SCR separates persistent agent identity from transient sovereign cells instantiated under explicit execution leases.
- Model access, tool rights, and runtime evidence are lease-bound; SCR remains subordinate to C3 scheduling and C7 orchestration.
**Consequences:**
- Atrahasis now has a canonical runtime substrate between C7 leaf intents and actual execution.
- Execution Evidence Bundles become the normative runtime provenance contract for downstream C5 and C8 integration.
- Additive host-spec integration text is still needed in C3, C5, and C7 before implementation planning consumes SCR directly.
**References:** docs/specifications/C23/MASTER_TECH_SPEC.md, docs/invention_logs/C23_IDEATION.md, docs/invention_logs/C23_FEASIBILITY.md, docs/invention_logs/C23_ASSESSMENT.md
**Invention:** C23

---

## ADR-035 — Black-Start Recovery Fabric: ADVANCE (C34)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- T-062 Recovery & State Assurance — HIGH priority gap: no unified cross-layer recovery architecture. C3 has Emergency Tidal Rollback and C8 has deterministic EABS, but no coordinated boot sequence, no post-recovery verification, and no adversarial reconstruction fallback
- Combined IC-1+IC-2+IC-3 selected: Black-Start Boot Sequence + Recovery Witness Verification + Adversarial Reconstruction Fallback
- Scores: Novelty 3.5, Feasibility 4.0, Impact 3.5, Risk 4/10 (MEDIUM)
- Prior art: 7 patents, 12 papers, 10 systems, 8 open source projects surveyed; no existing system combines dependency-ordered multi-layer boot with semantic synchronization predicates and consumer-side audit
**Decision:**
- ADVANCE: C34 BSRF adopted as the canonical cross-layer recovery architecture for Atrahasis
- Part I: Black-Start Boot Sequence — dependency-ordered recovery (C8→C5→C3→C7→C6), per-epoch Merkle state digests, 14 semantic synchronization predicates with contract binding, consumer-side audit trail
- Part II: Recovery Witness Verification — post-recovery cross-layer Merkle consistency checks, authority-directed reconciliation with witness corroboration (soft-TMR), multi-layer signed attestation
- Part III: Adversarial Reconstruction Fallback — declarative reference registry (15 types), causal traversal for state reconstruction from surviving digests; specified as registry+stub for Wave 4+ implementation
- Key innovations: semantic sync predicates (not just health checks), consumer-side audit trail, authority-directed reconciliation with cross-layer witness corroboration
- 35 conformance requirements (REQ-01 through REQ-35), 16 parameters, 4 patent-style claims
**Consequences:**
- All 6 core layers (C3/C5/C6/C7/C8) gain recovery integration points: digest emission, predicate satisfaction, witness participation
- C9 contract test suite should be extended with recovery-path integration tests
- C22 Wave 2-3 is the earliest implementation target; Part III deferred to Wave 4+
- Known limitation: authority-directed reconciliation cannot detect subtle corruption of the authoritative layer itself; mitigated by cross-layer witness corroboration and temporal trust gradient
**References:** docs/specifications/C34/MASTER_TECH_SPEC.md, docs/task_workspaces/T-062/ASSESSMENT_VERDICT.json
**Invention:** C34

---

## ADR-036 - Infrastructure & Federation: APPROVE (C24)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- C3 defines logical locality and eventual federation, and C22 assumes a deployable stack, but no canonical infrastructure boundary model existed for region scoping, state placement, or cross-region exchange.
- C23 defines parcel runtime hosts and execution leases, but not the region-scoped deployment domain that should contain those hosts or bound their cross-region movement.
- Without a deployment primitive, implementation would drift into ad hoc cluster assumptions, weak failure-domain definitions, and inconsistent federation behavior.
**Decision:**
- APPROVE: C24 adopts **Federated Habitat Fabric (FHF)** as the canonical deployment and federation architecture for Atrahasis.
- A Habitat is the region-scoped infrastructure domain that hosts loci, parcel runtime hosts, state services, governance relays, and explicit boundary gateways.
- Cross-habitat movement is restricted to Habitat Boundary Gateways and typed Habitat Boundary Capsules under explicit policy.
**Consequences:**
- Atrahasis now has a canonical deployment boundary below the logical stack and above substrate tooling.
- C23 runtime hosts, C3 locality rules, and future T-066 operational tooling inherit the same habitat failure-domain model.
- T-062 recovery work remains compatible because habitats align runtime, state, governance, and federation to the same regional boundary.
- Backend-specific product choices remain implementation-level decisions rather than architecture gaps.
**References:** docs/specifications/C24/MASTER_TECH_SPEC.md, docs/invention_logs/C24_IDEATION.md, docs/invention_logs/C24_FEASIBILITY.md, docs/invention_logs/C24_ASSESSMENT.md
**Invention:** C24

---
## ADR-037 - Operational Monitoring & Incident Response: APPROVE (C33)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- The Atrahasis stack already emitted many layer-local metrics, alerts, degraded modes, and governance thresholds, but had no canonical operational subsystem that turned those signals into coherent incidents and bounded response.
- C14 AiSIA governance monitoring and C22 implementation planning both implied dashboarding, security-audit readiness, and escalation workflows without specifying the operational fabric that should own them.
- The gap included signal normalization, cross-layer incident correlation, authority-bounded response playbooks, and audit-grade post-incident evidence.
**Decision:**
- APPROVE: C33 adopts **Operational Integrity Nerve Center (OINC)** as the canonical operational monitoring and incident-response layer for Atrahasis.
- OINC makes the **Incident Capsule** the first-class operational object, binding source signals, severity, scope, authority envelope, playbook state, evidence, and review output into one durable case.
- OINC remains subordinate to C3, C5, C7, C8, and C14; it may observe, contain locally where delegated, request layer actions, and escalate to governance, but it does not directly execute governance decisions.
**Consequences:**
- Atrahasis now has a canonical operational substrate for dashboards, incident handling, external security-audit evidence export, and post-incident review.
- C14's monitoring concepts and C22's dashboard/audit expectations now have a normative home.
- Additive host-spec integration text is still needed if owning layers expose new delegated local playbook actions to OINC.
**References:** docs/specifications/C33/MASTER_TECH_SPEC.md, docs/invention_logs/C33_IDEATION.md, docs/invention_logs/C33_FEASIBILITY.md, docs/invention_logs/C33_ASSESSMENT.md
**Invention:** C33

---

## ADR-038 - Sentinel Graph Security & Anomaly Detection: CONDITIONAL_APPROVE (C35)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- T-060 was the highest-priority CRITICAL task in the AAS backlog, referenced by 10+ existing specs (C3, C5, C7, C8, C11, C12, C13, C14, C17) as unspecified infrastructure for anomaly detection, behavioral clustering, and infrastructure fingerprinting.
- No dedicated security monitoring substrate existed despite many specs assuming sentinel-like detection capabilities.
- Full AAS pipeline (IDEATION→RESEARCH→FEASIBILITY→DESIGN→SPECIFICATION→ASSESSMENT) completed by agent Shamash (6ecc7362).
- Originally minted as C32 during IDEATION; re-IDed to C35 to resolve collision with C32 MIA (T-063, ADR-034).
**Decision:**
- CONDITIONAL_APPROVE: C35 adopts **Seismographic Sentinel** — a three-tier hierarchical anomaly detection pipeline with PCM-augmented Tier 2.
- Tier 1: Per-agent STA/LTA with fixed + adaptive dual baselines, OR-trigger with confirmation window.
- Tier 2: Permitted Correlation Model (PCM) — log-linear main-effects-only residuals within spectrally-clustered neighborhoods + 3-of-4 channel quorum (verification, behavioral, infrastructure, economic).
- Tier 3: Epidemiological backward tracing using overdispersion analysis (2 sources: C17 behavioral similarity + C7 intent provenance).
- Scores: Novelty 3.5, Feasibility 3.5, Impact 4.0, Risk 5/10 (MEDIUM).
- 5 blocking conditions (AC-1 PCM convergence experiment, AC-2 cross-neighborhood Sybil defense, AC-3 infrastructure-correlated suppression, AC-4 C22 wave placement, AC-5 C9 contract update) + 5 operational conditions.
- 37 requirements, 66 parameters, 7 patent-style claims.
**Consequences:**
- Atrahasis now has a canonical security monitoring substrate consumed by C3, C5, C7, C8, C12, and C17.
- Cross-layer integration via 6 sentinel contracts defining signal exchange, thresholds, and response authority.
- Key innovations: PCM (no direct precedent — log-linear structural covariate model for expected correlation), sentinel_health meta-signal for self-referential anomaly suppression.
- Simplifications applied: main-effects-only PCM (interactions deferred), quorum-only fusion (Bayesian deferred), C6 integration removed, Tier 3 limited to 2 trace sources.
- No remaining CRITICAL architectural gaps in the AAS backlog.
**References:** docs/specifications/C35/MASTER_TECH_SPEC.md, docs/specifications/C35/C35_ARCHITECTURE.md, docs/task_workspaces/T-060/ASSESSMENT_COUNCIL_VERDICT.md
**Invention:** C35

---

## ADR-039 — C36 Epistemic Membrane Architecture for Interfaces (EMA-I)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- T-064 identified that no spec in the Atrahasis stack defines how humans, external AI agents, enterprise systems, or developer tools interact with the system.
- Full AAS pipeline run (IDEATION through ASSESSMENT).
- Ideation Council produced 3 concepts: IC-1 (API Gateway), IC-2 (EMA-I — selected with FULL consensus), IC-3 (Schema Compiler).
- Scores: Novelty 3.5, Feasibility 4.0, Impact 4.5, Risk 4/10 (MEDIUM).
- Agent: Adapa (734bcdbf).
**Decision:**
- APPROVE: C36 adopts **Epistemic Membrane Architecture for Interfaces (EMA-I)** — a sovereign boundary layer with 4 core components.
- **Typed Interaction Receptors**: Session-typed (Honda et al. 1998) interface points organized into 5 persona families (Trustee, Provider, Operator, Developer, Agent), 35 receptors total, 3 detailed exemplars.
- **Structured Translation Engine (STE)**: Deterministic bidirectional translation formalized as Galois connection (Cousot & Cousot 1977). All v1.0 translations structured; NL deferred to v2.0.
- **Interaction Evidence Chain (IEC)**: Causal (not temporal) evidence records for every membrane interaction, hash-chained, with PCVM commitments at SIGNIFICANT+ classification.
- **Persona Projection Engine (PPE)**: Non-interfering (Goguen & Meseguer 1982) persona-specific views of frozen epoch state. Proven via persona privilege lattice.
- 3 operational conditions: (1) session type enforcement strategy before W1; (2) non-interference proof validated before W5; (3) write-behind evidence recovery demonstrated before W2.
- 5 monitoring flags: session type enforcement in Rust/TS, non-interference proof completeness, write-behind durability, composition side-effect detection, receptor specification coverage.
- 32 conformance requirements, 16 parameters, 4 patent-style claims.
**Consequences:**
- Atrahasis now has a canonical external interface layer consumed by and producing for 18+4 integration points.
- Critical security invariant: authenticate → validate → translate → authorize → dispatch. Translation never confers authority.
- C22 wave integration: W1 Developer receptors → W2 Agent → W3 Operator → W4 Provider → W5 Trustee.
- Transport-agnostic: REST, GraphQL, gRPC, WebSocket, MCP, A2A are bindings, not architecture.
- No remaining MEDIUM-priority AAS pipeline task spaces. Only T-067 (LOW) remains.
**References:** docs/specifications/C36/MASTER_TECH_SPEC.md, docs/task_workspaces/T-064/ASSESSMENT_VERDICT.json, docs/task_workspaces/T-064/ASSESSMENT_TRANSCRIPT.md
**Invention:** C36

---

## ADR-040 — C37 Epistemic Feedback Fabric (EFF)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- T-067 identified that the Atrahasis system verifies agent reasoning (C5 PCVM) but does not learn from its own verification data. The system has referees but no coaches. Verification outcomes flow to settlement and are discarded.
- Full AAS pipeline run (IDEATION through ASSESSMENT).
- Ideation Council produced 2 concepts: IC-1 (EFF — selected with MAJORITY consensus), IC-2 (Out-of-scope scoping decision — not selected).
- Scores: Novelty 3.5, Feasibility 4.0, Impact 4.0, Risk 5/10 (MEDIUM).
- Originally minted as C36; re-IDed to C37 due to collision with Adapa's T-064 EMA-I (ADR-039).
- Agent: Enki (804ff0b6).
**Decision:**
- APPROVE: C37 adopts **Epistemic Feedback Fabric (EFF)** — a privacy-preserving, sovereignty-respecting feedback system with 4 components and the Advisory Membrane Pattern.
- **Verification Feedback Loop (VFL)**: Aggregates C5 VTDs into per-claim-class quality metrics with three-layer privacy (k-anonymity k=10, differential privacy epsilon=2.0, secure aggregation). Dual-cadence publication (CONSOLIDATION_CYCLE normal + chi-squared anomaly-triggered). Hierarchical Bayesian estimation (James-Stein shrinkage) for rare claim classes.
- **Reasoning Strategy Catalog (RSC)**: Published library of reasoning patterns stored as C6 EMA epistemic quanta (type="reasoning_strategy"). Three declarative format types only: decompositions, anti-patterns, verification checklists. Subjective logic credibility tracking. 7-state lifecycle FSM. ~27 seed patterns at v1.0.
- **Complexity-Aware Budget Signals (CABS)**: Optional `reasoning_budget_advisory` on C23 ExecutionLease. Range format: {min_sufficient, recommended, max_useful, strategy_label, confidence}. Three-source fusion: C9 class weights, C7 RIF complexity, VFL historical calibration (p75).
- **Advisory Membrane**: Formalized architectural guarantee that no enforcement or surveillance mechanism may use advisory consumption data as input. ADVISORY_PRIVATE label with access control matrix. C17 RSC-aware whitelist for structural fingerprint discounting. Voluntariness paradox explicitly acknowledged.
- 3 operational conditions: (1) C17 whitelist sync protocol formal review before W2; (2) VFL schema regex fix (claim class pattern); (3) RSC convergence threshold calibration via W0 experiment.
- 6 monitoring flags: RSC convergence, C17 side-channel, CABS non-monotonicity, VFL gaming, agent stratification, VFL latency.
- 27 conformance requirements, 15 parameters, 5 patent-style claims.
**Consequences:**
- Atrahasis now has a meta-cognitive feedback layer that closes the information lifecycle gap between verification and reasoning improvement.
- Advisory Membrane Pattern has no close prior art — first formalized non-enforcement guarantee in multi-agent governance.
- C22 wave integration: Wave 2 placement (13-18 weeks, 1 engineer).
- No remaining AAS pipeline task spaces. All CRITICAL/HIGH/MEDIUM/LOW items complete (C1-C37). Only direct spec edits (T-070–T-088) remain.
**References:** docs/task_workspaces/T-067/specifications/MASTER_TECH_SPEC.md, docs/task_workspaces/T-067/ASSESSMENT.md
**Invention:** C37

---
## ADR-041 â€” AACP/AASL Full Replacement Program Activation (Alternative B)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- ADR-006 and ADR-007 narrowed the communication layer to C4 ASV over JSON / A2A / MCP and explicitly killed standalone AACP as a sovereign protocol direction.
- The user directed a fresh review of that choice and supplied a March 12, 2026 strategy packet under `C:\Users\jever\Atrahasis\AACP-AASL\` arguing for Alternative B: full sovereign replacement of A2A and MCP with AACP v2 plus extended AASL.
- `T-089` compared `ASV + A2A/MCP` against `AASL + AACP` and reopened the architecture question by showing the trade-off explicitly instead of treating the C4 direction as permanently settled.
- The supplied strategy packet also makes clear that the protocol buildout alone is insufficient: large parts of the Atrahasis repo, including planning and funding assumptions, currently depend on the C4 ASV + A2A/MCP operating model and will need follow-on retrofit.
**Decision:**
- Approve Alternative B as the active Atrahasis communication program: a sovereign `AACP v2 + extended AASL` stack is now the intended end-state architecture for future communication-layer work.
- Reverse the prior TODO out-of-scope designation for standalone AASL/AACP compiler/runtime/protocol work.
- Treat A2A and MCP bridges as migration scaffolding, not as the architectural end state.
- Preserve C4 ASV, ADR-006, and ADR-007 as historical lineage and compatibility baseline until explicit supersession tasks define the final retirement / adaptation boundary.
- Add two coordinated backlog tranches: `T-200` through `T-291` for protocol buildout, and `T-300` through `T-309` for repo-wide retrofit of specs, funding, implementation planning, and packaging assumptions built on C4.
**Consequences:**
- `TODO.md` now tracks Alternative B as active work rather than deferred/out-of-scope work.
- Future communication-layer tasks must read the March 12, 2026 AACP/AASL source packet before execution.
- The rest of the Atrahasis repo can no longer assume that `ASV + A2A/MCP` is the uncontested future direction; retrofit work is now part of the canonical backlog.
- Funding strategy, implementation planning, developer experience, cross-layer integration, and external review packaging all require follow-on updates once the new protocol architecture stabilizes.
**References:** C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replacement_Strategy.md, C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_Council_Briefing.md, C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_AAS_Tasks.md, docs/TODO.md, docs/COMPLETED.md
**Invention:** N/A (system-level)

---
## ADR-042 - ASV Retention and Authority Boundary During Alternative B
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- Alternative B activates a sovereign `AACP v2 + extended AASL` end-state, but the Atrahasis system still exists only as documentation in the repo, not as an independently running implementation.
- `C4 ASV` is therefore still the canonical record of the old communication architecture and the assumptions many other specs were written against.
- Deleting or globally forbidding access to ASV-era materials would remove the baseline needed for supersession, dependency audit, retrofit, migration, and compatibility decisions.
**Decision:**
- Retain `C4 ASV` and related communication-era materials in the working repo as historical baseline and compatibility reference.
- For `T-200`+ protocol buildout tasks, ASV-era materials are reference-only and MUST NOT be treated as normative design authority unless the assigned task explicitly requires old-stack comparison or compatibility analysis.
- For `T-300`+ supersession / audit / retrofit / migration tasks, ASV-era materials remain required source material.
- Do not delete, archive out of working reach, or otherwise hide ASV materials until the Alternative B retrofit program has completed and a later governance decision defines the final archive boundary.
**Consequences:**
- New protocol design work stays anchored on the Alternative B source packet rather than drifting back toward C4 assumptions.
- Repo-wide retrofit work retains the baseline needed to rewrite documents coherently instead of guessing what the old stack meant.
- Future agents have an explicit rule for when ASV should influence work and when it should not.
**References:** docs/DECISIONS.md, docs/SESSION_BRIEF.md, docs/TODO.md, C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replacement_Strategy.md
**Invention:** N/A (system-level)

---
## ADR-043 - AASL Type Registry Extension Policy for Alternative B
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- ADR-041 activated Alternative B and identified three new AASL type families as required for the sovereign communication stack: `TL{}` for tools, `PMT{}` for prompt templates, and `SES{}` for sessions.
- ADR-042 established that old ASV/C4 materials remain historical and compatibility reference only for `T-200+` protocol-design work, so the governing authority for this task is the Alternative B packet plus the existing AASL semantic-governance corpus.
- Existing AASL governance artifacts already define namespace discipline, compatibility classes, lifecycle states, pinned registry snapshots, and a ban on ambient unknown-term invention, but no task-specific policy yet stated how `TL`, `PMT`, and `SES` must enter the canonical registry.
- Without an explicit policy, downstream tasks such as `T-210` and `T-212` would be forced to guess admission rules and could fragment the registry through implementation-led semantics.
**Decision:**
- `TL{}`, `PMT{}`, and `SES{}` SHALL enter the canonical AASL registry only through the formal ontology proposal and admission workflow; ad hoc implementation extension is not sufficient.
- Admissions in this family SHALL be treated as non-editorial changes, with compatibility class metadata (`C1`/`C2` or higher as appropriate), migration impact, and affected validator/compiler/runtime/tooling surfaces recorded at the registry level.
- Validators and runtimes that do not recognize these types MUST NOT silently reinterpret them as older known constructs. Unknown-type handling must follow explicit profile, lifecycle, and sandbox rules instead of heuristic guessing.
- Experimental use is permitted only through explicit experimental namespace or profile controls and MUST NOT silently promote to stable canonical status.
- This task defines the governance envelope only. Concrete field definitions, canonical forms, and ontology placement remain downstream work for `T-212`, while the five-layer architectural role of these types remains downstream work for `T-210`.
**Consequences:**
- `T-210` can proceed without inventing missing registry-governance rules for new Alternative B type families.
- `T-212` is constrained to a pinned-snapshot, compatibility-labeled extension path rather than a free-form schema addition.
- Registry, validator, compiler, runtime, and tooling work must record exact registry snapshots and preserve the no-ambient-term-invention rule when these types appear.
- Alternative B gains the required type-growth path for tools, prompt templates, and sessions without violating AASL semantic closure.
**References:** docs/task_workspaces/T-201/POLICY_DRAFT.md, C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replacement_Strategy.md, C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_Council_Briefing.md, C:\Users\jever\Atrahasis\Atrahasis Conception Documentation\AASL_SPECIFICATION.md, C:\Users\jever\Atrahasis\Atrahasis Conception Documentation\Atrahasis_AASL_Ontology_Registry_and_Governance_Operations.md
**Invention:** N/A (system-level)

---
## ADR-044 - C38 Five-Layer Sovereign Protocol Architecture (FSPA)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- ADR-041 activated Alternative B and created a sovereign AACP/AASL buildout backlog, but the repo still lacked a root architectural authority explaining how AACP v2 should be partitioned across transport, session, security, messaging, and semantics.
- ADR-042 kept C4/ASV as historical baseline and compatibility reference only, which preserved lineage but did not answer the architecture question for the new sovereign stack.
- ADR-043 defined the governance path for new semantics-layer type growth (`TL`, `PMT`, `SES`), but not the broader cross-layer contract model.
- Without a root architecture, downstream tasks such as `T-211`, `T-212`, `T-213`, `T-215`, `T-220+`, and `T-230+` would be forced to invent or assume missing layer boundaries.
**Decision:**
- Accept C38 Five-Layer Sovereign Protocol Architecture (FSPA) as the root architecture for Alternative B.
- AACP v2 SHALL be treated as a five-layer stack: Transport, Session, Security, Messaging, and Semantics.
- Canonical semantic identity SHALL originate in the Semantics layer and remain authoritative across encodings and bindings.
- Messaging SHALL own lineage-bearing envelopes and message taxonomy without redefining payload meaning.
- Security SHALL bind identity, authorization, signatures, and replay protection to canonical references without replacing semantic or verification authority.
- Session SHALL own capability negotiation, liveness, and recovery, and SHALL fail closed when negotiation would break required invariants.
- Bridges to A2A/MCP SHALL remain compatibility-only migration scaffolding and MUST disclose degraded or translated provenance state explicitly.
**Consequences:**
- `T-211`, `T-212`, `T-213`, `T-215`, `T-220+`, `T-230+`, `T-240+`, and `T-290` now have a root architecture boundary to refine instead of guessing layer ownership.
- Future Alternative B tasks must refine or extend the defined layer contracts rather than silently collapsing responsibilities across layers.
- Retrofit tasks gain a stable target architecture for replacing old `C4 ASV + A2A/MCP` end-state assumptions across the rest of the repo.
**References:** docs/specifications/C38/MASTER_TECH_SPEC.md, docs/task_workspaces/T-210/IDEATION_COUNCIL_OUTPUT.yaml, docs/task_workspaces/T-210/FEASIBILITY.md, docs/task_workspaces/T-210/ASSESSMENT.md
**Invention:** C38

---
## ADR-045 - C39 Lineage-Bearing Capability Message Lattice (LCML)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- ADR-044 accepted C38 Five-Layer Sovereign Protocol Architecture as the root Alternative B communication architecture and explicitly deferred message-class design to `T-211`.
- The Alternative B source packet requires the message layer to expand from the current 23-class AACP lineage to 42 classes, covering discovery, tools, resources, prompting, streaming/push, and sampling.
- The legacy Atrahasis/AACP corpus contains more than one draft-era message inventory, so downstream tasks needed a normalized canonical baseline before extension.
- Without a message-layer authority, tasks such as `T-214`, `T-240`, `T-241`, `T-242`, `T-243`, `T-244`, and `T-281` would be forced to invent or duplicate class surfaces inconsistently.
**Decision:**
- Accept C39 Lineage-Bearing Capability Message Lattice (LCML) as the canonical L4 Messaging inventory extension for Alternative B.
- Normalize the pre-extension AACP baseline to 23 canonical classes: 11 runtime lifecycle classes, 7 coordination/control classes, and 5 tidal-extension classes.
- Add exactly 19 new classes across six capability families: Discovery, Tool, Resource, Prompt, Stream, and Sampling.
- Adopt the LCML class-economy rule: dual-phase classes are allowed when request and response share one semantic contract, while distinct result classes are reserved for materially different downstream semantic/provenance consequences.
- Model push-style delivery through stream-family response-channel semantics rather than extra push-only message classes.
- Preserve semantic object internals (`TL`, `PMT`, `SES`) and Agent Manifest field structure as downstream work for `T-212` and `T-214`.
**Consequences:**
- `T-214`, `T-240`, `T-241`, `T-242`, `T-243`, `T-244`, and `T-281` now have a canonical message inventory to refine instead of guessing class boundaries.
- Growth beyond 42 canonical classes now requires later governance review rather than silent downstream inflation.
- Bridge tasks (`T-250`, `T-251`) inherit an explicit message-layer provenance posture for native versus translated flows.
**References:** docs/specifications/C39/MASTER_TECH_SPEC.md, docs/task_workspaces/T-211/IDEATION_COUNCIL_OUTPUT.yaml, docs/task_workspaces/T-211/FEASIBILITY.md, docs/task_workspaces/T-211/ASSESSMENT.md
**Invention:** C39

---

## ADR-046 - C40 Dual-Anchor Authority Fabric (DAAF)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- ADR-044 accepted `C38` Five-Layer Sovereign Protocol Architecture and defined that L3 Security must bind identity, authorization, signatures, and replay protection to canonical references without replacing semantic or verification authority.
- The Alternative B source packet explicitly required `T-230` to define a native auth module covering OAuth 2.1, mTLS, API keys, Ed25519 agent identity tokens, message-level signing over canonical hashes, replay detection, identity verification, and role-based plus capability-based authorization.
- Existing Atrahasis specs already provided pieces of the answer (`C32` native identity anchoring, `C23` no-ambient-rights runtime enforcement, `C36` authenticate -> validate -> authorize -> dispatch ordering), but no canonical Alternative B security invention unified those pieces into one bounded L3 contract.
- Without this task, downstream work such as `T-214`, `T-231`, `T-240`, `T-262`, `T-281`, and `T-290` would be forced to guess what counts as native identity, what must be signed, how replay/downgrade must fail closed, and how explicit grants differ from ordinary authentication.
**Decision:**
- Accept `C40` Dual-Anchor Authority Fabric (DAAF) as the canonical L3 security architecture for Alternative B.
- AACP v2 SHALL distinguish two trust-anchor families: native Atrahasis agent identity rooted in `C32` AgentID plus Ed25519-backed keys, and non-native ingress identity for humans, institutions, services, bridges, and local tools admitted through bounded federation, mTLS, or API-key profiles.
- AACP v2 SHALL use the bounded four-profile set defined by DAAF: `SP-NATIVE-ATTESTED`, `SP-FEDERATED-SESSION`, `SP-WORKLOAD-MTLS`, and `SP-BRIDGE-LIMITED`, unless later governance explicitly extends it.
- Security-sensitive actions SHALL bind to canonical message identity through `ABP-v1` / `SIG-v1` authority binding rather than transport bytes alone.
- Replay detection SHALL use message freshness plus a seen-message cache keyed by signer anchor, `message_id`, and canonical hash, and invariant-breaking downgrade SHALL fail closed.
- Sensitive actions SHALL require explicit signed capability grants; DAAF defines the generic grant model but does not replace downstream runtime enforcement, manifest schema design, or tool semantics.
- Bridge-limited and API-key-only paths SHALL remain visibly bounded and MUST NOT silently satisfy native-only or other high-trust policy.
**Consequences:**
- `T-214` now has a concrete auth-scheme and manifest-signing authority surface to consume.
- `T-240` now has a generic capability-grant and no-ambient-authority substrate rather than inventing L3 behavior ad hoc.
- `T-231`, `T-262`, `T-281`, and `T-290` now have a concrete security posture for threat-model extension, SDK design, conformance, and cross-layer integration.
- Alternative B security now remains sovereign without forcing all principals into one gateway-centered trust model or collapsing into runtime-specific authorization semantics too early.
**References:** docs/specifications/C40/MASTER_TECH_SPEC.md, docs/task_workspaces/T-230/HITL_APPROVAL.md, docs/task_workspaces/T-230/FEASIBILITY.md, docs/task_workspaces/T-230/ASSESSMENT.md
**Invention:** C40

---
## ADR-047 - C41 Layered Semantic Capability Manifest (LSCM)
**Date:** 2026-03-12
**Status:** ACCEPTED
**Context:**
- ADR-044 accepted `C38` Five-Layer Sovereign Protocol Architecture and left manifest semantics to `T-214`.
- ADR-045 accepted `C39` LCML and defined discovery-family manifest publish, query, and update classes, but deferred the full manifest object model.
- ADR-046 accepted `C40` DAAF and set the trust rule for signed manifests, security profile disclosure, endpoint-scoped operational keys, and fail-closed registry/manifest conflicts.
- Without `T-214`, Alternative B would still lack the canonical document that lets clients, registries, bridges, SDKs, and conformance tooling discover what an endpoint is, how it should be trusted, and which protocol-semantic surfaces it actually supports.
**Decision:**
- Accept `C41` Layered Semantic Capability Manifest (LSCM) as the canonical Alternative B discovery manifest.
- LSCM SHALL be published at `/.well-known/atrahasis.json` as the signed endpoint-scoped capability disclosure surface.
- LSCM SHALL disclose bounded durable truth only: subject identity, trust posture, discovery and transport endpoints, supported `C40` security profiles and auth schemes, supported `C39` message families, supported `AASL` types and ontology snapshots, optional bounded references to deeper capability surfaces, and visible supersession lineage.
- LSCM SHALL make native-versus-bridge posture explicit and machine-readable.
- LSCM SHALL keep runtime telemetry, live health, and registry ranking behavior out of the canonical manifest surface.
- Registry and manifest conflicts on native trust posture SHALL fail closed rather than be heuristically reconciled.
**Consequences:**
- `T-251` now has a canonical A2A Agent Card replacement target.
- `T-261` now has a registry source document and searchable capability sections.
- `T-262` now has a manifest fetch and parsing surface for the SDK architecture.
- `T-281` now has a manifest conformance target.
- `T-290` now has a stable external capability contract for cross-layer integration.
**References:** docs/specifications/C41/MASTER_TECH_SPEC.md, docs/task_workspaces/T-214/HITL_APPROVAL.md, docs/task_workspaces/T-214/FEASIBILITY.md, docs/task_workspaces/T-214/ASSESSMENT.md
**Invention:** C41

---
## ADR-048 - C42 Lease-Primed Execution Mesh (LPEM)
**Date:** 2026-03-13
**Status:** ACCEPTED
**Context:**
- Alternative B had message authority (`C39`), security authority (`C40`), manifest authority (`C41`), and runtime lease authority (`C23`), but no canonical invention defining how trusted tool invocation becomes high-performance, policy-visible continuation and execution-ready context.
**Decision:**
- Accept `C42` Lease-Primed Execution Mesh as the canonical Alternative B tool-authority surface.
- `C42` defines signed tool inventory snapshots, explicit invocation priming levels (`IMMEDIATE_ONLY`, `CONTINUATION_READY`, `EXECUTION_PRIMED`), bounded continuation contexts, mandatory accountable tool results, and runtime handoff contracts that can feed `C23` lease derivation without bypassing `C23`.
**Consequences:**
- `T-250` must translate MCP tools into the `C42` native-versus-bridge posture.
- `T-260` must expose `C42` continuation and execution-priming hooks.
- `T-262` must model snapshot reuse, continuation lifecycle, and runtime handoff as first-class SDK surfaces.
- `T-243` remains the owner of actual stream/push carriage for continuation-heavy flows.
- `C23` remains runtime authority; `C42` primes but does not replace lease issuance.
**References:** docs/specifications/C42/MASTER_TECH_SPEC.md, docs/task_workspaces/T-240/HITL_APPROVAL.md, docs/task_workspaces/T-240/FEASIBILITY.md, docs/task_workspaces/T-240/ASSESSMENT.md
**Invention:** C42

---
## ADR-049 - C43 Custody-Bounded Semantic Bridge (CBSB)
**Date:** 2026-03-13
**Status:** ACCEPTED
**Context:**
- Alternative B already had message authority (`C39`), security authority (`C40`), manifest authority (`C41`), and native tool authority (`C42`), but no canonical migration bridge explaining how MCP servers enter the new stack without dishonest native-equivalence claims.
- `T-089` and `T-301` reopened communication architecture and retrofit sequencing, but neither task defined the bridge-specific custody, provenance, or reusable-state boundary.
- Without `T-250`, downstream work such as `T-251`, `T-260`, `T-262`, `T-281`, `T-303`, and `T-307` would be forced to guess how translated inventories, invocation identity, bridge inference, and non-native continuation posture should work.
**Decision:**
- Accept `C43` Custody-Bounded Semantic Bridge (CBSB) as the canonical Alternative B MCP migration bridge.
- `C43` defines signed bridge-scoped inventory snapshots, invocation pinned to snapshot/tool/policy identity, explicit separation of source-observed facts from bridge-normalized structure and bridge-inferred semantics, accountable bridged results, bounded reusable bridge state, and optional derated continuation handles.
- `C43` remains migration scaffolding and SHALL NOT be treated as native `C42` tool authority or `C23` runtime authority.
**Consequences:**
- `T-251` now has a symmetry reference for bridge honesty and non-native posture.
- `T-260` must keep native framework behavior distinct from migration-bridge behavior.
- `T-262` must model bridge snapshots, translation identity, and derated continuation surfaces without treating bridged tools as native.
- `T-281` now has a canonical MCP bridge conformance target.
- `T-303` and `T-307` must preserve native-vs-bridge provenance boundaries and bridge-retirement discipline.
**References:** docs/specifications/C43/MASTER_TECH_SPEC.md, docs/task_workspaces/T-250/HITL_APPROVAL.md, docs/task_workspaces/T-250/ASSESSMENT.md
**Invention:** C43

---
## ADR-050 - C44 AASL-T Constrained Generation Engine
**Date:** 2026-03-13
**Status:** ACCEPTED
**Context:**
- `T-270` required specifying the constrained decoding rules, few-shot prompt structures, and datasets needed to force LLMs to emit valid `AASL-T`.
- Without a canonical constrained-generation authority, downstream AACP clients and toolchains would rely on ad hoc parser recovery layers.
**Decision:**
- Accept `C44` as the canonical constrained-generation authority for `AASL-T`.
- `C44` defines strict EBNF grammars, benchmark targets, and dataset expectations for syntactically valid, schema-conformant `AASL-T` output.
**Consequences:**
- `T-252` may consume `C44` as the generation target for Forge-mediated semantic upgrades.
- `T-291` now has a normative generation-validity surface for justification and benchmark gates.
- AACP clients can verify native `AASL-T` generation against one shared constrained-decoding authority.
**References:** docs/specifications/C44/MASTER_TECH_SPEC.md
**Invention:** C44

---
## ADR-051 - C4 Supersession Boundary and Compatibility Policy
**Date:** 2026-03-15
**Status:** ACCEPTED
**Context:**
- ADR-006 and ADR-007 made `C4 ASV + A2A/MCP` the active communication direction and explicitly retired sovereign `AACP` as the end-state protocol posture.
- ADR-041 activated the sovereign replacement program and preserved `C4`, ADR-006, and ADR-007 until an explicit supersession task defined the final boundary.
- ADR-042 retained `C4` as historical baseline and compatibility reference, but did not yet define the exact line between retained baseline and superseded forward authority.
- T-301 audited the repo-wide old-stack footprint and identified `T-300` as the required governance task before downstream retrofit work could rewrite cross-layer, roadmap, and packaging surfaces coherently.
- C38 and the downstream Alternative C authority surfaces now exist, so the replacement side of the boundary is no longer speculative.
**Decision:**
- Accept `T-300` as the canonical supersession boundary for `C4`.
- `C4 ASV`, its companion architecture/spec artifacts, and ADR-006 / ADR-007 remain retained in-repo as historical lineage and compatibility baseline for retrofit, audit, migration, bridge policy, and old-stack comparison work.
- `C4` is no longer normative forward design authority for Atrahasis communication architecture.
- Alternative C forward communication authority now resolves through `C38`, `C39`, `C40`, `C41`, `C42`, `C45`, `C46`, `C47`, and `T-290` / `AXIP-v1` rather than through `C4 ASV + A2A/MCP`.
- Statements that define Atrahasis's future communication posture as `ASV` over `A2A/MCP`, or that treat sovereign `AACP` as retired doctrine, are superseded.
- No task may delete or hide `C4` from the working repo until the retrofit program is complete and a later governance decision defines final archive posture.
**Consequences:**
- `T-302` through `T-309` now have a fixed governance boundary for replacing old-stack assumptions instead of improvising where `C4` still applies.
- Downstream retrofit tasks must read `C4` directly when rewriting legacy assumptions, but must not treat it as the target architecture.
- `UNIFIED_ARCHITECTURE.md` and the remaining old-stack references are now governed as superseded narrative or compatibility surfaces rather than current doctrine.
- The repo preserves the old baseline without allowing it to compete with Alternative C as future authority.
**References:** docs/task_workspaces/T-300/TASK_BRIEF.md, docs/task_workspaces/T-300/BOUNDARY_POLICY_DRAFT.md, docs/task_workspaces/T-301/TASK_BRIEF.md, docs/task_workspaces/T-301/COMM_DEPENDENCY_AUDIT.md, docs/task_workspaces/T-301/COMM_DEPENDENCY_INVENTORY.md, docs/specifications/C04 - Agent Abstraction and Control Protocol/C4_Agent_Abstraction_and_Control_Protocol_Master_Tech_Spec.md, docs/specifications/C38 - AACP Full Sovereign Protocol Architecture/C38_AACP_Full_Sovereign_Protocol_Architecture_Master_Tech_Spec.md, docs/specifications/UNIFIED_ARCHITECTURE.md
**Invention:** N/A (system-level)

