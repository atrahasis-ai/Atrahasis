# The Atrahasis Agent System
## Master Overview — System Design, Rationale, and Usage Guide
### Version 1.0 | March 9, 2026

---

## What this is

The Atrahasis Agent System (AAS) is a structured multi-agent workflow for **inventing new technologies and software**. It enables AI agents to collaboratively generate, research, validate, design, prototype, and formally specify novel inventions.

It is designed to work with **ephemeral** agents (they run, return output, and terminate) coordinated by a single persistent coordinator (**Director**).

The system optimizes for:

- **Genuine novelty** (adversarial ideation with structured dissent)
- **Prior art rigor** (dedicated research layer with structured reports)
- **Stage-gate discipline** (inventions advance only after assessment)
- **Parallel throughput without artifact conflicts** (contribution request queue)
- **Durable session continuity** (resume exactly where you left off)
- **Institutional memory that compounds** (patterns, decisions, and anti-patterns persist)
- **Patent-ready specifications** (formal claims, embodiments, and architecture)

---

## The core problems (what breaks without structure)

1. **Convergent thinking bias**
   - Without structured dissent, agents converge on the first plausible idea rather than exploring the most novel one.

2. **Prior art blindness**
   - Without dedicated research, agents reinvent existing solutions and miss existing patents.

3. **Specification incompleteness**
   - Without formal structure, specifications lack the detail needed to reproduce or patent the invention.

4. **Novelty assessment difficulty**
   - Without adversarial assessment, it's unclear whether an invention is genuinely novel or merely a recombination.

5. **Context decay**
   - Without condensed memory, every session restarts cold and loses accumulated knowledge.

6. **Parallel artifact conflicts**
   - Without controlled integration, multiple specialists editing shared documents creates chaos.

---

## The v1.0 design responses

### 1) Ideation Council (adversarial invention generation)
Three roles — Visionary, Systems Thinker, Critic — debate in structured rounds. This prevents convergent thinking and ensures concepts are challenged before resources are committed.

### 2) Dedicated Research Layer
Prior Art Researcher, Landscape Analyst, and Science Advisor work in parallel. Each produces structured reports that inform feasibility decisions.

### 3) Stage-Gate Lifecycle
Inventions progress through: IDEATION → RESEARCH → FEASIBILITY → DESIGN → PROTOTYPE → SPECIFICATION → ASSESSMENT. Each transition requires an Assessment Council verdict.

### 4) Contribution Request Queue (prevents shared artifact conflicts)
Specialists never edit shared artifacts directly. They submit structured contribution requests. The Synthesis Engineer applies all changes in one controlled pass.

### 5) Assessment Council (adversarial quality gate)
Advocate, Skeptic, and Arbiter evaluate each invention. Four possible verdicts: ADVANCE, CONDITIONAL_ADVANCE, PIVOT, REJECT.

### 6) Context Condensation (read small, archive big)
The Chronicler maintains condensed memory documents for quick session startup. Full transcripts are archived but not read by default.

### 7) Typed State + Validators
All state is YAML with JSON Schema validation. Contribution requests and invention concepts have schemas and validators.

### 8) Human-in-the-Loop Gates
Default mode is autonomous, except for: concept selection, pivot decisions, external research, patent decisions, public disclosure risk, and abandonment.

---

## Documents in the system

### Core documents (always present)
- `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md` — system constitution / operating manual
- `docs/INVENTION_CONTEXT.md` — institutional memory + conventions
- `docs/AGENT_STATE.md` — current execution state (YAML)
- `docs/TRIBUNAL_LOG.md` — full council transcript archive (append-only)

### Read-first condensed documents (Opening Brief reads these)
- `docs/SESSION_BRIEF.md`
- `docs/INVENTION_DASHBOARD.md`
- `docs/DECISIONS.md`
- `docs/PATTERN_REGISTER.md`

### Execution support
- `docs/invention_logs/` — one file per invention
- `docs/contribution_requests/` — one file per invention needing shared artifact changes
- `docs/prior_art/` — one directory per invention with research findings
- `docs/specifications/` — one directory per invention with formal specifications
- `prototypes/` — one directory per invention with proof-of-concept code
- `docs/schemas/` — JSON schemas
- `docs/templates/` — templates for logs, requests, and reports
- `scripts/` — validators

---

## Quick start (how to use)

1. Paste the **Director Activation Prompt** from `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md`
2. Director runs the Opening Brief (reads state + condensed docs)
3. Provide a problem domain, technology area, or invention prompt
4. Ideation Council generates and debates invention concepts
5. Director presents concepts for user selection (HITL gate)
6. Research layer investigates prior art, landscape, and scientific feasibility
7. Ideation Council reconvenes with research data for refinement
8. Architecture Designer and Specification Writer produce formal documents
9. Prototype Engineer builds proof-of-concept
10. Assessment Council issues final verdict

---

## Design intent

The system is intentionally conservative about:
- premature commitment to a concept (stage gates)
- prior art blindness (dedicated research)
- specification incompleteness (formal templates)
- shared artifact conflicts (contribution requests)
- implicit memory (condensed, validated state)

…and aggressively optimized for:
- novelty discovery (adversarial ideation)
- parallel throughput (independent specialist work)
- reproducibility (schemas + validators)
- resumability (durable state)
- compounding institutional knowledge (patterns + decisions)
- patent readiness (formal claims and specifications)

---
