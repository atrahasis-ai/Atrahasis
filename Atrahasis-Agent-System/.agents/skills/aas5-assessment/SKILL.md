---
name: aas5-assessment
description: Assess AAS5 artifacts for bugs, regressions, doctrinal conflicts, and missing validation. Use when Codex needs to review specs, code, or task outputs before approval, merge, or closeout.
---

# AAS5 Assessment

## Overview

Use this skill to run the AAS5 assessment posture: findings first, evidence anchored, and explicit about residual risk.

## Workflow

1. Read the artifact and its immediate upstream authority surfaces.
2. Review for:
   - bugs or internal contradictions
   - behavioral regressions
   - doctrine or HITL violations
   - missing validators or missing evidence
3. Prefer a review-first output:
   - findings ordered by severity
   - open questions / assumptions
   - short change summary only after findings
4. For code or spec changes that warrant a formal review run, use Codex review tooling in addition to manual inspection.
5. End with a clear recommendation:
   - accept
   - advance with conditions
   - block pending fixes

## Output Rules

- Cite exact file paths for each finding.
- If there are no findings, say so explicitly and note residual testing gaps.
- Keep summaries brief; the findings are the main deliverable.

## Guardrails

- Do not soften real defects into "suggestions."
- Do not confuse style preferences with correctness issues.
- Do not close the gate if the required evidence or validation is missing.
