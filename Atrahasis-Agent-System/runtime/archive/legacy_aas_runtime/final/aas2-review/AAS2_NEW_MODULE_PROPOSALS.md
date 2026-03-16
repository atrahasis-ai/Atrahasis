# AAS2 New Module Proposals

## Proposed Modules

### `pipeline_stage_registry.py`

- Purpose: declare stage ordering, dependencies, command-profile rules, and gating conditions.
- Inputs: command request, workflow context, stage definitions.
- Outputs: executable stage plan for the orchestration layer.
- Integration: sits directly under `InventionPipelineManager`.

### `workflow_context_store.py`

- Purpose: hold mutable workflow state between stages without forcing every module to reconstruct context.
- Inputs: normalized command request, stage outputs, operator decisions.
- Outputs: current workflow context snapshot and resumable state.
- Integration: shared runtime state owned by the orchestration layer.

### `knowledge_index.py`

- Purpose: incremental index over repo documents, task workspaces, prior-art materials, and hypotheses.
- Inputs: file deltas, artifact writes, document metadata.
- Outputs: queryable evidence references, summaries, embeddings or keyword profiles, change sets.
- Integration: replaces repeated full-manifest scans as the primary retrieval surface.

### `discovery_graph_store.py`

- Purpose: maintain the Discovery Map as durable graph state rather than a transient artifact.
- Inputs: synthesis signals, hypotheses, contradictions, solution paths, program relationships.
- Outputs: graph queries, graph diffs, artifact projections.
- Integration: sits below the discovery plane and above `DISCOVERY_MAP.json` generation.

### `governance_kernel.py`

- Purpose: persist scope locks, dependency pauses, program transitions, and per-domain active program rules.
- Inputs: program proposals, contradiction clusters, frontier signals, operator decisions.
- Outputs: authoritative program state transitions and governance decisions.
- Integration: becomes the control authority for research-program state while remaining subordinate to the orchestrator.

### `program_state_store.py`

- Purpose: durable storage for research-program lifecycle data, resolved contradictions, and branch histories.
- Inputs: governance decisions, ranking outcomes, experiment results.
- Outputs: current and historical program state.
- Integration: backing store for the governance kernel and research director.

### `operator_session_manager.py`

- Purpose: maintain pending review queues, operator decisions, redirects, and replayable interaction history.
- Inputs: decision packets, operator commands, exploration control recommendations.
- Outputs: active operator session state and resumable pending actions.
- Integration: between `HumanDecisionInterface` and task workspace persistence.

### `telemetry_aggregator.py`

- Purpose: aggregate workflow telemetry into health summaries and pressure signals.
- Inputs: system logs, artifact writes, workflow events, error counts.
- Outputs: rolling health snapshots, pressure indicators, operator-visible summaries.
- Integration: supports both AAS runtime health and future AAS-RE review cycles.

### `command_profile_engine.py`

- Purpose: define execution depth and stage policy per command modifier.
- Inputs: normalized command request and workflow context.
- Outputs: stage enablement, depth policy, optional fast-path rules.
- Integration: sits between the router and stage registry.

## Module Justification

These modules are proposed because the current AAS2 architecture already has the right major concepts, but lacks durable system surfaces for:

- long-running state
- modular execution policy
- graph persistence
- operator continuity
- operational observability

## Modules Explicitly Not Proposed

- no autonomous swarm controller inside AAS2
- no distributed actor fabric as the primary runtime
- no replacement of human-guided approval with automated commitment logic
