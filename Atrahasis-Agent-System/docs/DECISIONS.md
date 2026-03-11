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

## ADR-000 — Template
**Date:** 2026-03-09
**Status:** ACCEPTED | SUPERSEDED
**Context:** (1–3 bullets)
**Decision:** (1–3 bullets)
**Consequences:** (1–3 bullets)
**References:** (links to invention log, tribunal entry, contribution request)
**Invention:** (INVENTION_ID if applicable)

---
