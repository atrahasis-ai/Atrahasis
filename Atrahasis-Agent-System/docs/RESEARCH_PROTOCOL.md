# Research Protocol (v1.0)

## When this applies
Use this workflow for every invention concept that advances past IDEATION stage:
- Prior art investigation
- Technology landscape mapping
- Scientific/engineering feasibility validation

---

## Step 1 — Prior Art Research (Prior Art Researcher)
Goal: determine if the invention concept has genuine novelty.

Outputs:
- Structured `PRIOR_ART_REPORT` (JSON)
- Search queries used
- Patents, papers, products, and open-source projects found
- Closest prior art with explicit differentiators
- Novelty assessment

## Step 2 — Landscape Analysis (Landscape Analyst)
Goal: map the competitive and technological context.

Outputs:
- Structured `LANDSCAPE_REPORT` (JSON)
- Competitor analysis
- Adjacent technologies
- Market gaps and opportunities
- Technology readiness assessment

## Step 3 — Science Assessment (Science Advisor)
Goal: confirm the underlying principles are sound.

Outputs:
- Structured `SCIENCE_ASSESSMENT` (JSON)
- Physical/mathematical/computational constraints
- Known theoretical limits
- Required breakthroughs (if any)
- Confidence in scientific foundations

## Step 4 — Director Synthesis
Director reviews all three research outputs and determines:
- Does the concept survive research? (novelty + feasibility intact)
- Are there fatal prior art conflicts?
- Should the concept be refined before advancing?

If the concept survives → advance to FEASIBILITY stage.
If fatal issues → present to user with PIVOT or REJECT recommendation.

---

## Research Quality Standards

### Search Coverage
- At least 3 distinct search query formulations per key innovation
- Cross-reference across patent databases, academic literature, commercial products, and open-source

### Citation Requirements
- Every reference must include: title, source, relevance level (HIGH/MEDIUM/LOW), and a summary
- Closest prior art must include explicit differentiators showing how the invention differs

### Honesty Standard
- If a researcher cannot find prior art, they must state their confidence level
- Absence of evidence is not evidence of absence — state search limitations explicitly

---

## Note
If external research tools or databases are needed, this triggers the EXTERNAL_RESEARCH HITL gate.
The Director must obtain user approval before dispatching researchers to external services.
