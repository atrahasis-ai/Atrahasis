# C37 Feasibility Assessment — Epistemic Feedback Fabric (EFF)

**Date:** 2026-03-12
**Agent:** Enki (Claude Code)
**Stage:** FEASIBILITY

---

## 1. Ideation Council Reconvention (with Research Data)

### Visionary (updated position)
The research validates the core thesis: the verification-to-advisory pipeline is novel and no existing system occupies this space. GaaS (closest prior art) is an enforcement system — EFF is its advisory complement. The Science Advisor scores VFL at 4.0/5 (strongest component) and the overall architecture at 3.3/5 (coherent).

I accept two scope reductions from research:
1. **RSC v1.0 restricted** to declarative decompositions, anti-patterns, and checklists only. No prompt templates, no chain-of-thought prescriptions. This makes RSC genuinely model-agnostic.
2. **CABS recommends ranges** (min_sufficient, recommended, max_useful) not point estimates, paired with strategy labels. The non-monotonic budget-performance relationship demands this.

I also accept the voluntariness paradox as a feature, not a bug. The Advisory Membrane prevents surveillance-based coercion. It cannot and should not prevent performance-based self-selection — that's how useful advisory systems work.

**Revised novelty estimate:** 3 (novel combination of known techniques in a novel architectural context). The individual components use established techniques (DP, Bayesian estimation, task-extrinsic complexity). The novelty is the integration under sovereignty constraints.

### Systems Thinker (updated position)
Integration analysis after research:

**VFL integration with C5:** Clean. C5 produces VTDs with graded claim validity. VFL adds a second consumer (alongside C8 DSF). VTD schema already contains claim_class, verdict, confidence. VFL needs: agent_id (for k-anonymity grouping, discarded after aggregation), premises_count, reasoning_steps_count, failure_mode (if rejected). These fields exist or are derivable from existing VTD content.

**RSC integration with C6:** Clean. RSC patterns are epistemic quanta with type = "reasoning_strategy". Follow existing metabolism lifecycle. Credibility tracked via subjective logic opinion tuples. Fits C6's coherence graph for derivation tracking. Cold-start solved by manually curated seed patterns (analogous to expert-authored CPGs).

**CABS integration with C23:** Minimal change. Add optional `reasoning_budget_advisory` object to ExecutionLease schema: `{min_sufficient: int, recommended: int, max_useful: int, strategy_label: string, confidence: float}`. Non-breaking — existing leases without this field continue to work.

**Advisory Membrane integration with C17:** This is the most complex integration. C17 must maintain an RSC-synchronized whitelist of published structural patterns. When computing B(a_i, a_j) structural similarity, discount similarity scores that match whitelisted patterns. This requires a formal dependency: C17.structural_baseline depends on RSC.published_patterns. Must be specified as a cross-layer integration contract.

**C22 wave placement:** Wave 2 (earliest). Requires C5 operational (Wave 1), C6 operational (Wave 2), C23 operational (Wave 1). VFL aggregation service is the only new runtime component.

### Critic (updated position)
Research partially validates my ideation concerns:

**Challenge 1 (real gap vs. feature) — RESOLVED.** The landscape analysis confirms no existing system occupies this space. The 7 known solutions and GaaS prior art all differ on the enforcement/advisory axis. This is a real gap.

**Challenge 2 (advisory membrane fiction) — PARTIALLY VALIDATED.** Science Advisor confirms: structural side-channel via C17 is a HIGH risk. Timing and resource channels are LOW. The voluntariness paradox is fundamental — acknowledged, not fixable. I accept the membrane as "prevents surveillance-based enforcement" rather than "guarantees true voluntariness."

**Challenge 3 (population feedback too slow) — RESOLVED.** Science Advisor clarifies: VFL publishes statistical summaries, not real-time coaching. 10-hour cycle is faster than CPGs (annual). Anomaly-triggered alerts handle fast signals. The comparison frame was wrong — VFL is a guideline publisher, not a coach.

**Remaining concern:** RSC scored 2.5/5 — the weakest component. The evidence gap for non-LLM agents is significant. I support RSC v1.0 restricted to declarative patterns, but this means EFF's value proposition is largely LLM-centric until v2.0. The specification should be honest about this.

**New concern from research:** The prior art report identifies GaaS as MEDIUM patent risk for "external governance of multi-agent AI systems." EFF must carefully distinguish its advisory-only nature in all claims. The Advisory Membrane is not just an architectural feature — it's the primary patent differentiator.

---

## 2. Domain Translator — Sub-Problem Analogies

### Sub-Problem 1: How to aggregate verification outcomes without revealing individual agent performance
**Analogy: Census Bureau Statistical Disclosure Limitation**
The US Census Bureau publishes population statistics while protecting individual respondent identity. Techniques: data swapping, noise injection (DP), cell suppression for small groups. The Census Bureau's privacy standard maps directly to VFL: publish aggregate statistics about claim verification while protecting which agent submitted which claim.

### Sub-Problem 2: How to make reasoning patterns useful across heterogeneous architectures
**Analogy: International Building Codes**
Building codes specify performance requirements ("structure must withstand X wind load") not construction methods ("use 2x4 studs at 16-inch intervals"). Engineers using steel, concrete, wood, or composite can all meet the same performance spec differently. RSC patterns as declarative performance specs (not method prescriptions) follow this model.

### Sub-Problem 3: How to recommend budgets without knowing internals
**Analogy: Nutrition Facts Labels**
The FDA's label says "2,000 calories/day" as a reference, knowing that individual needs vary by body composition, activity level, and metabolism. The recommendation is population-derived, task-categorized ("active adult" vs. "sedentary"), and explicitly advisory. CABS recommends reasoning budgets the same way — population-derived, claim-class-categorized, explicitly advisory.

### Sub-Problem 4: How to prevent advisory signals from becoming enforcement
**Analogy: Academic Peer Review Norms vs. Law**
Academic peer review norms are advisory — they guide scholarship but have no legal force. However, academics who consistently ignore peer review norms face career consequences (fewer publications, less funding). This is exactly the voluntariness paradox. The academic system accepts this: peer review norms ARE de facto mandatory for career success, but they are NOT enforcement tools — no government body mandates following reviewer suggestions. The distinction matters: advisory norms can evolve through scholarly debate, while laws require legislative process. EFF's Advisory Membrane serves the same purpose — keeping reasoning guidance in the "norm" category rather than the "law" category, even though norms carry social weight.

---

## 3. Commercial Viability Assessment (Early Activation)

### Necessity Score: 4/5 (Strong)

**Why the system needs this:**
1. C5 PCVM currently verifies and forgets. Verification data is the system's most valuable signal about what reasoning works, and it's being discarded after settlement.
2. New agents entering the system have no way to learn from the population's experience. They start cold. RSC provides institutional memory.
3. C8 DSF settles inference costs. Without CABS, there's no mechanism to optimize reasoning spend. This has direct economic impact on the AIC economy (C15).
4. As agent population grows (1K → 100K), population-level signals become more statistically powerful and more valuable — the system gets better at coaching as it scales.

**Why it's not 5/5:**
- The system functions without EFF. Agents can reason however they want, and C5 catches bad outputs. EFF improves efficiency and quality but isn't load-bearing infrastructure.
- RSC v1.0 is primarily LLM-centric, limiting value for heterogeneous populations.

### Adoption Barriers: LOW
- VFL is invisible to agents (aggregation runs in the background)
- RSC consumption is voluntary (agents query if they want)
- CABS is an optional field on existing leases (non-breaking change)
- No agent needs to change behavior to coexist with EFF

### Revenue/Cost Impact
- CABS-driven budget optimization could reduce system-wide inference costs by 20-40% (per AVA literature)
- At C22's projected $8M-$12M total budget, inference costs are a significant portion (Wave 1-3 compute)
- EFF operational overhead is one aggregation service + privacy mechanism — minimal compared to savings

---

## 4. Adversarial Analyst — Case for Abandonment

### The Strongest Case Against EFF

**Argument 1: EFF is a vitamin, not a painkiller.**
The system works without it. C5 catches bad reasoning. C35 catches anomalies. C17 catches Sybils. Adding EFF is optimizing a system that already has all necessary safety mechanisms. The marginal value of "slightly better reasoning quality" doesn't justify a new cross-layer specification with integration contracts across C5, C6, C17, C23, and C35.

**Counter:** True that EFF isn't safety-critical. But it's economically significant — 20-40% inference cost reduction at scale. And it fills the only gap in the information lifecycle: verification data currently flows to settlement (C8) and nowhere else. EFF closes the loop.

**Argument 2: RSC will calcify reasoning.**
If agents converge on RSC-recommended patterns, the system loses cognitive diversity. Cognitive diversity is a feature — different reasoning approaches catch different errors. RSC risks creating a monoculture where all agents reason the same way, reducing the population's collective intelligence.

**Counter:** Valid concern. Mitigation: RSC should publish multiple alternative patterns per claim class, not a single "best" pattern. Pattern diversity monitoring (similar to C17's behavioral diversity metrics) should flag if population convergence exceeds a threshold.

**Argument 3: The privacy guarantees are theater.**
The Science Advisor identified a fundamental voluntariness paradox: effective signals create performance gaps that constitute market pressure to adopt. The Advisory Membrane prevents the worst form of coercion but not the mildest form. Selling EFF as "sovereignty-preserving" when it creates de facto adoption pressure is misleading.

**Counter:** This is the nature of ALL useful advisory systems. Medical guidelines, building codes, academic peer review — all are formally advisory and de facto semi-mandatory. The membrane prevents the specific harms (surveillance-based enforcement, C17 weaponization of consumption data) while accepting the general dynamic (useful information gets adopted). The specification should be transparent about this.

**Argument 4: Three addenda, not a new invention.**
VFL is a C5 extension. RSC is a C6 extension. CABS is a C23 extension. The Advisory Membrane is a C17 integration constraint. None of these individually justify a new specification. The cross-layer coordination is the only novel piece, and it could be handled by a reconciliation addendum (like C9).

**Counter:** The cross-layer coordination IS the invention. The individual components are integration points, but the feedback loop (C5 → VFL → RSC/CABS → agents → C5) is a new information flow that doesn't exist in any single spec. C9-style addenda handle errata; EFF defines a new architectural capability.

### Abandonment Verdict: **WEAK CASE**
Arguments 2 (monoculture risk) and 4 (scope question) have merit but are addressable. Arguments 1 and 3 are technically valid but apply to all advisory systems. The economic case (inference cost optimization) and information lifecycle case (closing the verification feedback loop) are stronger than the case for abandonment.

---

## 5. Feasibility Verdict

### Assessment Council Preliminary Verdict

**Advocate:** EFF fills a genuine gap — the system's most valuable signal (verification outcomes) is currently discarded after settlement. The feedback loop from C5 → VFL → RSC/CABS → agents has no precedent in the landscape (confirmed by prior art report). Integration is clean across 4 specs. C22 Wave 2 placement is natural. Novelty 3, but the integration under sovereignty constraints is the real innovation.

**Skeptic:** RSC is the weak link (2.5/5 soundness). The voluntariness paradox means the "sovereignty-preserving" claim has an asterisk. The scope question (standalone spec vs. addenda) is legitimate. However, the cross-layer feedback loop is architecturally novel enough to justify standalone treatment, and the economic case is strong.

**Arbiter:** The research validates the core concept. VFL is sound. RSC needs scope restriction but is viable as declarative patterns. CABS has empirical support with the non-monotonic caveat addressed by range recommendations. The Advisory Membrane is partially sound with known mitigations for the structural side-channel.

**FEASIBILITY_VERDICT: ADVANCE**

Conditions for DESIGN:
1. RSC v1.0 restricted to declarative decompositions, anti-patterns, and verification checklists
2. CABS must recommend (min, recommended, max) ranges with strategy labels, not point estimates
3. Advisory Membrane must include RSC-aware baseline adjustment protocol for C17
4. Specification must explicitly acknowledge the voluntariness paradox
5. Pattern diversity monitoring must be specified to prevent reasoning monoculture

Scores:
- Novelty: 3 (novel combination of known techniques under novel constraints)
- Feasibility: 4 (all components use established techniques; integration is clean)
- Impact: 3.5 (economic value via cost optimization; information lifecycle completion; not safety-critical)
