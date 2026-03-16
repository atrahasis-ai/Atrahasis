# AAS3 Implementation Plan

## Implementation Strategy

Implement AAS3 as a staged evolution of AAS2.

Do not replace the current runtime in one move.

## Phase 1 - Control Spine Decomposition

- add `PipelineStageRegistry`
- add `WorkflowContextStore`
- move stage definitions out of `InventionPipelineManager`
- keep the current stage order and human review behavior unchanged

Exit criteria:

- current workflows still run
- stage sequencing is registry-driven rather than hard-coded

## Phase 2 - Persistent Knowledge Infrastructure

- add `KnowledgeIndex`
- cache and incrementally update repo manifest data
- route `GCMLMemoryInterface` reads through the index when available

Exit criteria:

- full repo rescans are no longer required for every run
- evidence retrieval quality remains compatible with current artifacts

## Phase 3 - Discovery and Governance State

- add `DiscoveryGraphStore`
- add `GovernanceKernel`
- add `ProgramStateStore`
- treat `RESEARCH_PROGRAM_REPORT.json` and `DISCOVERY_MAP.json` as projections from runtime state

Exit criteria:

- scope/domain locks are authoritative
- program lifecycle transitions are persisted
- discovery graph is durable and queryable

## Phase 4 - Operator Continuity

- add `OperatorSessionManager`
- persist pending human decisions, redirects, and replayable session state
- keep `HUMAN_DECISION_RECORD.json` as the outward-facing artifact

Exit criteria:

- workflows can pause and resume without manual JSON inspection
- operator history is durable across sessions

## Phase 5 - Telemetry and Diagnostics

- add `TelemetryAggregator`
- produce workflow health summaries and pressure indicators
- expose architecture diagnostics for future AAS-RE cycles

Exit criteria:

- logs remain intact
- health summaries and architecture signals are queryable

## Phase 6 - Contract Hardening

- replace critical raw dict flows with typed context objects where practical
- version key runtime contracts
- add validation and regression coverage around stage inputs and outputs

Exit criteria:

- lower change risk for new modules
- clearer integration boundaries between planes

## Migration Rules

- preserve the current artifact filenames where possible
- preserve the single-controller rule
- preserve mandatory human review
- preserve compatibility with current task workspace outputs

## Recommended First Modules

1. `pipeline_stage_registry.py`
2. `workflow_context_store.py`
3. `knowledge_index.py`
4. `governance_kernel.py`

## Final Recommendation

Proceed with AAS3 as a targeted architectural evolution of AAS2.

The review does not recommend a radical runtime replacement.
