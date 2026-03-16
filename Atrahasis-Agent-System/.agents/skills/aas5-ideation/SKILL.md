---
name: aas5-ideation
description: Run the ideation stage for a full-pipeline task through the active AAS5 25-agent topology.
---

# AAS5 Ideation

## Overview

Use this skill to produce the ideation output without prematurely promoting a concept into design or specification work.

## Workflow

1. Confirm the task is actually `FULL PIPELINE` and read the active task workspace plus the current authority surfaces:
   - `docs/TODO.md`
   - `docs/DECISIONS.md`
   - `docs/INVENTION_CONTEXT.md`
   - relevant task workspace files under `docs/task_workspaces/T-<ID>/`
   - the contents of the current claim YAML files for parallel-context awareness
   - use `rg` when available for fast lookup, but if it is missing from the shell fall back to `Get-ChildItem` / `Select-String` without treating that as a blocker
   - when authority surfaces are named only by spec id (`C42`, `C45`, etc.), resolve the real titled spec path first with `python scripts/resolve_spec_path.py <SPEC_ID>` or MCP `get_spec`
2. Run the ideation structure explicitly:
   - parent Master Orchestrator baseline
   - for ordinary `FULL PIPELINE / IDEATION`, use the default AAS5 hierarchy:
     - `1` parent Codex Master Orchestrator
     - `4` lane managers: `Alpha`, `Beta`, `Gamma`, `Radical`
     - `12` lane workers: `visionary`, `systems_thinker`, and `critic` under each manager
     - `4` lane convergence reporters
     - `4` independent auditors: swarm compliance, runtime audit, authority coverage, adversarial integrity
   - optional advisory companion: `memory_reuse_analyst` when redesign history is materially relevant and policy allows it
3. If the ideation is architecture-heavy, compares a candidate subsystem against current authority, or the operator is asking for agent findings before choosing a path:
   - real child sessions are mandatory
   - if this is an exploratory/noncanonical idea run, create the analysis-band `T-900x` workspace first with `python scripts/prepare_aas5_idea_task.py ...`
   - if the operator used the textual modifier `Full Pipeline Task:`, treat that as a hard no-fallback directive: do not answer with parent-only advisory analysis
   - operator instructions such as “do not add it to TODO”, “do not claim a canonical task”, or “do not edit shared state yet” do not cancel the noncanonical `T-900x` workspace requirement
   - create the full AAS5 ideation artifact bundle, including `TEAM_PLAN.yaml`, `FUTURE_BRANCH_REPORT.json`, `SWARM_EXECUTION_RECORD.json`, `CHILD_RESULT_MERGE_PACKAGE.json`, lane plans, lane convergence reports, audit artifacts, `SWARM_TOPOLOGY_GRAPH.json`, `EXECUTION_PARALLELISM_RECORD.json`, and one child result artifact per real non-parent participant under `docs/task_workspaces/T-<ID>/children/`
   - structure that swarm as parent -> 4 lane managers -> 12 workers, plus 4 reporters and 4 auditors
   - if the runtime cannot form a real child swarm, stop and report the blocker
   - do not output a swarm readout backed only by internal role simulation
   - do not present a recommendation until `python scripts/validate_swarm_execution_record.py T-<ID>` passes and the AAS5 artifacts authorize recommendation
   - if execution is batched rather than simultaneous, treat it as degraded rather than equivalent, and require explicit operator acknowledgement before recommendation
   - if the required workspace or swarm artifacts do not exist, stop and report noncompliance rather than improvising a parent-session advisory answer
4. If the operator names explicit authority surfaces, existing modules, or asks whether the idea is already subsumed versus requiring a new subsystem:
   - extract those surfaces into an obligation list first
   - produce `AUTHORITY_COVERAGE_MATRIX.json`
   - make sure every named surface has:
     - current authority summary
     - coverage status
     - disposition
     - whether new authority is still needed
   - block the recommendation until all named surfaces are addressed
5. Distill the negotiation into a small concept set:
   - concept label
   - one-sentence description
   - key novelty
   - main integration burden
   - main risk
   - exact downstream task consequences if chosen
6. Produce `recommended_concepts` and identify the preferred option, but treat that preference as advisory only.
7. Stop and hand the result to the operator for concept approval.

## Output Rules

- Keep concept count small. Default to two or three serious options rather than a brainstorm dump.
- Make doctrinal conflicts explicit instead of silently sanding them off.
- If a prerequisite subsystem is missing, say so directly rather than pretending the concept is dispatchable.
- If named authority surfaces were provided, recommendation is incomplete unless each surface is explicitly addressed.

## Guardrails

- Do not mint any `C-xxx` invention ID during ideation.
- Do not create per-invention specification folders during ideation.
- Do not claim the HITL gate is satisfied just because a preferred concept exists.
- Route approval handling through `aas5-hitl-gates`, not through this skill.
- Do not silently skip a named authority surface just because the broader answer already feels directionally correct.
- Do not label solo internal roleplay as a swarm. If the required child swarm did not actually run, the ideation result is incomplete.
- Do not guess spec filesystem paths from bare ids. Resolve them first.
- Do not treat a noncanonical `T-900x` workspace as forbidden shared-state editing. It is the required local audit surface for exploratory ideation.
- If `FUTURE_BRANCH_REPORT.json` or `SWARM_EXECUTION_RECORD.json` does not authorize recommendation, do not recommend.
- If the operator used `Full Pipeline Task:`, do not make a judgment call to stay lightweight. Run the strict routed path or stop and report noncompliance.
- Do not treat a 17-node or 13-node ideation shape as compliant ordinary ideation under AAS5.
