---
name: aas5-task-routing
description: Classify an operator request and choose the correct execution path under the active AAS5 doctrine.
---

# AAS5 Task Routing

## Overview

Use this skill to decide what kind of task is being executed and what rules apply before any edits or delegation.

## Workflow

1. Read the current claim files, target artifacts, and the relevant TODO row or operator prompt. Use `rg` when available, but fall back to `Get-ChildItem` / `Select-String` if the shell does not expose it.
   - If the prompt begins with `Full Pipeline Task:` or `FULL PIPELINE TASK:`, treat that as a hard operator modifier.
   - That modifier forbids judgment-call downgrade to parent-only advisory analysis.
2. Classify the task as one of:
   - `FULL PIPELINE`
   - `DIRECT SPEC`
   - `Governance`
   - `Analysis`
   - `Packaging`
3. Check prerequisites, dependency gates, and active claims before starting.
4. Identify the authoritative write surface:
   - task workspace
   - existing spec
   - shared governance doc
   - handoff only
5. Decide whether the task is dispatchable now, blocked, or requires HITL before progress.
6. State the artifact path and validator path before editing.
7. If the task is an exploratory `AASNI` or noncanonical `FULL PIPELINE` idea, allocate an analysis-band `T-900x` workspace instead of leaving the run session-only.
   - constraints against shared-state progression (`TODO.md`, claims, handoffs) do not prohibit this noncanonical workspace
   - if the prompt carried the `Full Pipeline Task:` modifier, the `T-900x` workspace plus strict AAS5 ordinary ideation path are mandatory for exploratory ideation

## Guardrails

- Do not treat a blocked dependency as a suggestion.
- Do not convert a direct-spec request into a new invention line.
- For `FULL PIPELINE`, route to ideation first and stop for concept approval before promotion.
- For `FULL PIPELINE / IDEATION`, default to the real AAS5 ordinary ideation hierarchy: `1` parent, `4` lane managers, `12` workers, `4` lane convergence reporters, and `4` independent auditors.
- For exploratory idea work, read the current claim YAML contents and create the `T-900x` workspace before swarm ideation starts.
- If the operator asks for ideation findings but the `T-900x` workspace or swarm validator path is not being executed, stop and report noncompliance instead of answering informally.
- If the operator used `Full Pipeline Task:`, treat any parent-only option set or recommendation as noncompliant unless the strict routed path has actually run.
- Do not treat degraded batched execution as equivalent to ideal simultaneous AAS5 execution.
