---
name: aas5-feasibility
description: Run the AAS5 feasibility stage after ideation and research. Use when Codex needs to translate concept options and evidence into hard gates, required mitigations, monitoring flags, and an explicit advance or block recommendation.
---

# AAS5 Feasibility

## Overview

Use this skill to turn ideation and research outputs into a defensible decision about whether Atrahasis should advance, conditionally advance, or block the work.

## Workflow

1. Read the ideation output and research artifacts fully before scoring anything.
2. Identify the strongest objections from:
   - critic / adversarial reasoning
   - research contradictions
   - doctrinal or governance conflicts
   - implementation prerequisites
3. Convert those objections into explicit feasibility structure:
   - hard gates
   - required actions
   - monitoring flags
   - residual risks
4. Score novelty, feasibility, impact, and risk only after the gating logic is clear.
5. End with one recommendation:
   - `ADVANCE`
   - `CONDITIONAL_ADVANCE`
   - `BLOCK`

## Output Rules

- Hard gates must be testable.
- Required actions must be concrete enough to assign later.
- Monitoring flags should capture the main failure modes that survive advancement.
- If the main answer is "depends on an unstated subsystem," say that directly.

## Guardrails

- Do not rewrite the concept to hide infeasibility.
- Do not collapse scientific, engineering, and governance risks into one vague score.
- Do not promote the work to design just because the concept is interesting.
