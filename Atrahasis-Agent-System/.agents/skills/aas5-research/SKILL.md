---
name: aas5-research
description: Run the AAS5 research stage for prior art, landscape, and science assessment. Use when Codex needs external or repo-local evidence to test novelty, feasibility, standards posture, or adjacent technical landscape before feasibility or specification work.
---

# AAS5 Research

## Overview

Use this skill to gather bounded evidence for the research stage and package it into machine-usable or operator-usable outputs.

## Workflow

1. Read the local task context first:
   - `docs/TODO.md`
   - `docs/DECISIONS.md`
   - relevant task workspace files
   - existing `docs/prior_art/<ID>/` or prior research artifacts if they exist
   - when a repo surface names a spec by bare id (`C39`, `C42`, etc.), resolve the actual titled spec path before reading it
2. Split the research surface into three lanes:
   - prior art
   - technical / product landscape
   - science / soundness
3. Prefer repo-local evidence first. Use live web search only when current external evidence is actually required.
4. When the output must feed automation, use:
   - `python scripts/run_aas5_schema_exec.py --schema <schema> --output <artifact> --prompt-file <prompt>`
5. When live external search is needed, follow:
   - `docs/platform_overlays/codex/WEB_SEARCH.md`
6. Keep source evidence separate from inference. Cite the exact file path or URL for each important claim.
7. If the operator or upstream ideation step names explicit authority surfaces or asks whether the current architecture already absorbs an idea:
   - keep an authority-coverage obligation list
   - update or produce `AUTHORITY_COVERAGE_MATRIX.json`
   - make sure every named surface has an explicit disposition before recommending absorb / extend / replace
8. If this research stage is continuing a swarm-required `FULL PIPELINE` path:
   - preserve the truth of how the work is being executed
   - do not describe solo internal viewpoint checks as if they were real child-agent research lanes
   - if the operator explicitly wants multi-agent research findings, use a real child team or stop and report the blocker

## Output Rules

- Summarize novelty gaps, not just source lists.
- Distinguish "closest known analogue" from "direct overlap."
- Mark confidence levels when evidence is thin or mixed.
- If web research is approval-sensitive, stop and request approval rather than browsing around it.
- If named authority surfaces were supplied, do not collapse the answer to a recommendation until each one is explicitly covered.
- If the stage is meant to be swarm-backed, keep the report honest about whether real child execution happened.

## Guardrails

- Do not use ambient browsing as a substitute for task scoping.
- Do not let web evidence overwrite repo-canonical doctrine or task authority.
- Do not claim legal clearance, patent clearance, or scientific proof from shallow search results.
- Do not assume `docs/specifications/<ID>/MASTER_TECH_SPEC.md` exists as a literal path; resolve the actual spec path first.
