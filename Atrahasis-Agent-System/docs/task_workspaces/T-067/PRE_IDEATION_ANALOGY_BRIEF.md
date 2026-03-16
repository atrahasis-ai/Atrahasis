# T-067 PRE-IDEATION: Cross-Domain Analogy Brief
**Role:** Domain Translator
**Date:** 2026-03-12
**Agent:** Enki (Claude Code)

---

## Problem Restatement

How do you improve the reasoning quality of autonomous agents without controlling their internals, in a system that verifies outputs post-hoc, at scale across heterogeneous participants?

## 5 Cross-Domain Analogies

### Analogy 1: Clinical Practice Guidelines (Medicine)
**Domain:** Evidence-based medicine
**Structural mapping:** Medical boards publish Clinical Practice Guidelines (CPGs) that recommend diagnostic and treatment strategies. Physicians are autonomous — they can deviate from guidelines, but deviations must be documented with rationale. Adherence is tracked statistically, not enforced per-case. Outcomes data feeds back into guideline updates.

**Maps to Atrahasis as:**
- CPGs → Reasoning Strategy Templates (advisory, not mandatory)
- Physician autonomy → Agent sovereignty (C32)
- Outcome tracking → C5 verification results
- Statistical adherence monitoring → C17/C35 behavioral analytics
- Guideline revision cycle → Adaptive strategy evolution

**Key insight:** The medical system improves reasoning quality across millions of autonomous practitioners without controlling their decision-making. It works through **published standards + outcome feedback + statistical monitoring**.

### Analogy 2: Air Traffic Control Advisory System (Aviation)
**Domain:** Aviation safety
**Structural mapping:** ATC provides advisory guidance to pilots (traffic advisories, weather updates, suggested headings), but under Visual Flight Rules the pilot has final authority. The system doesn't fly the plane — it provides situational awareness signals that help pilots make better decisions. TCAS (Traffic Collision Avoidance System) escalates from advisory to directive only when collision is imminent.

**Maps to Atrahasis as:**
- Advisory signals → Reasoning quality signals from C5 back to agents
- Pilot authority → Agent sovereignty
- TCAS escalation → Graduated response (advisory → warning → C35 intervention)
- Flight data recorder → C5 VTD audit trail
- Mandatory reporting → Required reasoning disclosure for high-stakes claims

**Key insight:** The escalation model — advisory by default, directive only at defined threat thresholds — fits Atrahasis's sovereignty model perfectly.

### Analogy 3: Coaching vs. Refereeing in Professional Sports (Deliberately Surprising)
**Domain:** Professional athletics
**Structural mapping:** Referees verify rule compliance after actions occur (post-hoc verification = C5). Coaches improve player performance through strategy guidance, film review, and practice feedback — but during the game, players make their own decisions. The coach cannot control the player's muscles. Good coaching systems use: pre-game strategy briefs, real-time situational signals (play calls), and post-game film review with feedback.

**Maps to Atrahasis as:**
- Referee → C5 PCVM (post-hoc verification)
- Coach → Meta-cognitive advisory layer (the missing piece)
- Pre-game brief → Reasoning strategy templates published per claim type
- Play calls → Real-time reasoning allocation signals (complexity-aware)
- Film review → Post-task reasoning quality feedback from verification results
- Player autonomy → Agent sovereignty (coach advises, player decides)

**Key insight:** The current system has referees but no coaches. Adding a coaching function — advisory, non-binding, feedback-driven — fills the gap without compromising the referee's authority or the player's autonomy.

### Analogy 4: Nutritional Labeling (Consumer Health)
**Domain:** Food regulation
**Structural mapping:** The FDA doesn't control what people eat. It publishes nutritional labels, dietary guidelines, and recommended daily values. Consumers make their own choices with better information. The system improves health outcomes at population scale without individual control.

**Maps to Atrahasis as:**
- Nutritional labels → Reasoning complexity labels on tasks
- Dietary guidelines → Recommended reasoning strategies per claim class
- Recommended daily values → Suggested token budgets per complexity tier
- Consumer autonomy → Agent sovereignty
- Population health monitoring → System-wide reasoning quality metrics

**Key insight:** Information publication at scale, not individual control. The system makes better reasoning easier and cheaper to choose without mandating it.

### Analogy 5: Immune System Memory (Biology)
**Domain:** Immunology
**Structural mapping:** The adaptive immune system doesn't centrally control how individual immune cells fight pathogens. Instead, it publishes "memory" — antibody templates from past successful responses — that bias future responses toward effective strategies. Naive cells that encounter a pathogen can access this memory to mount faster, better responses. The memory doesn't command cells; it provides pre-computed patterns that make good responses more likely.

**Maps to Atrahasis as:**
- Antibody templates → Proven reasoning patterns from historically successful claims
- Immune memory → System-level pattern library (drawn from C5 verification data)
- Naive cell activation → New agent encountering unfamiliar claim type
- Affinity maturation → Pattern refinement over verification cycles
- No central command → Agent sovereignty preserved

**Key insight:** The system learns at the population level and makes successful patterns available, but individual agents remain autonomous in whether and how they use those patterns.

## Recommended Focus

Analogies 1 (Clinical Practice Guidelines) and 3 (Coaching vs. Refereeing) are the strongest structural matches. They directly address the sovereignty constraint while providing concrete architectural patterns.

Analogy 5 (Immune Memory) offers the most novel framing — a population-level learning system that doesn't control individuals but makes good strategies accessible.
