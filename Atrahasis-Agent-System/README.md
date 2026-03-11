# Atrahasis Agent System — v1.0 (March 9, 2026)

A multi-agent AI system for **inventing new technologies and software**. Agents collaborate through structured workflows to generate, research, validate, design, prototype, and formally specify novel inventions.

## What this system does

- **Generates** novel technology concepts through adversarial ideation (Visionary vs. Systems Thinker vs. Critic)
- **Researches** prior art, competitive landscape, and scientific feasibility
- **Assesses** novelty, feasibility, impact, and commercial viability
- **Designs** system architectures for new inventions
- **Prototypes** proof-of-concept implementations
- **Specifies** inventions to patent-ready level (claims, embodiments, figures)
- **Evaluates** through adversarial assessment (Advocate vs. Skeptic vs. Arbiter)

## Stage-Gate Lifecycle

`IDEATION → RESEARCH → FEASIBILITY → DESIGN → PROTOTYPE → SPECIFICATION → ASSESSMENT`

Each stage transition requires an Assessment Council verdict: `ADVANCE | CONDITIONAL_ADVANCE | PIVOT | REJECT`

## Quick Start

1. Paste the **Director Activation Prompt** from `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md` §15.1
2. Director runs the Opening Brief (reads state + condensed docs)
3. Provide a problem domain or invention prompt
4. Agents take it from there through the stage-gate lifecycle

## Validation

```bash
python scripts/validate_agent_state.py docs/AGENT_STATE.md
python scripts/validate_contribution_requests.py docs/contribution_requests
python scripts/validate_invention_concept.py <concept-file>
```

## Repository Structure

```
├── README.md
├── docs/
│   ├── ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md    # System constitution
│   ├── ATRAHASIS_SYSTEM_OVERVIEW_v1.md         # High-level overview
│   ├── AGENT_STATE.md                          # Durable state (YAML)
│   ├── SESSION_BRIEF.md                        # Read-first session summary
│   ├── INVENTION_DASHBOARD.md                  # Invention status table
│   ├── DECISIONS.md                            # ADR-style decision log
│   ├── PATTERN_REGISTER.md                     # Recurring patterns
│   ├── TRIBUNAL_LOG.md                         # Council transcript archive
│   ├── INVENTION_CONTEXT.md                    # Institutional memory + conventions
│   ├── GUARDRAILS.md                           # Safety and format guardrails
│   ├── HITL_POLICY.md                          # Human-in-the-loop policy
│   ├── RESEARCH_PROTOCOL.md                    # Prior art research workflow
│   ├── PROTOTYPE_VALIDATOR_GUIDE.md            # Prototype validation guide
│   ├── SYNTHESIS_PLAYBOOK.md                   # Shared artifact integration
│   ├── TOOLS.md                                # Tooling conventions
│   ├── schemas/
│   │   ├── agent_state.schema.json
│   │   ├── contribution_request.schema.json
│   │   ├── invention_concept.schema.json
│   │   ├── prior_art_report.schema.json
│   │   └── assessment_verdict.schema.json
│   ├── templates/
│   │   ├── INVENTION_LOG_TEMPLATE.md
│   │   ├── CONTRIBUTION_REQUEST_TEMPLATE.yaml
│   │   └── ASSESSMENT_AND_SYNTHESIS_JSON_TEMPLATES.md
│   ├── invention_logs/                         # Per-invention logs
│   ├── contribution_requests/                  # Shared artifact change requests
│   ├── prior_art/                              # Per-invention research
│   └── specifications/                         # Per-invention formal specs
├── prototypes/                                 # Per-invention proof-of-concept code
└── scripts/
    ├── validate_agent_state.py
    ├── validate_contribution_requests.py
    └── validate_invention_concept.py
```

## Agent Roles

### Coordinator Layer
- **Director** — orchestrates everything; never generates invention content
- **Chronicler** — owns state + memory artifacts

### Ideation Layer (adversarial debate)
- **Visionary** — bold, unconstrained concepts
- **Systems Thinker** — technical architecture and feasibility
- **Critic** — prior art risks, impossibilities, fatal flaws

### Research Layer
- **Prior Art Researcher** — patents, papers, products, open-source
- **Landscape Analyst** — competitive and technology landscape
- **Science Advisor** — scientific/engineering soundness

### Execution Layer
- **Prototype Engineer** — proof-of-concept code
- **Specification Writer** — formal specs, patent-style claims
- **Architecture Designer** — system architecture documents
- **Synthesis Engineer** — integrates outputs, owns shared artifacts

### Assurance Layer
- **Technical Feasibility Assessor**
- **Novelty Assessor**
- **Impact Assessor**
- **Specification Completeness Assessor**
- **Commercial Viability Assessor**
- **Prototype Validator**
- **Assessment Council** (Advocate, Skeptic, Arbiter)

---

*Built on the proven structural patterns of the Atrahasis Agent Team System v5.0, rewritten for invention rather than product development. Named after the Atrahasis distributed AI architecture.*
