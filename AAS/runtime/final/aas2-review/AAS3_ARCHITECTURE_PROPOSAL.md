# AAS3 Architecture Proposal

## Decision

Propose `AAS3` as an evolutionary architecture improvement over AAS2.

This is not a full reset. It preserves:

- the single orchestration authority
- the human-guided decision model
- repo-backed canonical artifacts
- the research-program and invention-intelligence model

It changes the runtime shape underneath those principles.

## AAS3 Target Shape

### Control Plane

1. `InventionPipelineManager`
   - remains the only execution controller
2. `PipelineStageRegistry`
   - declares stage ordering, dependencies, and command-specific execution profiles
3. `WorkflowContextStore`
   - keeps stage outputs, decision state, and resumable workflow context

### Knowledge Plane

4. `KnowledgeIndex`
   - incremental index for repo docs, task artifacts, prior art, and invention history
5. `DiscoveryGraphStore`
   - durable graph state for concepts, hypotheses, contradictions, solution paths, and programs
6. `ArtifactProjectionLayer`
   - projects canonical JSON and markdown artifacts from durable runtime state

### Governance Plane

7. `GovernanceKernel`
   - authoritative scope/domain locks, dependency pauses, and lifecycle transitions
8. `ProgramStateStore`
   - durable research-program state and history
9. `ResearchDirectorModel`
   - prioritization and branch allocation over durable governance state

### Reasoning Plane

10. existing invention modules remain
   - hypothesis, contradiction, solution, novelty, feasibility, opportunity, analogy, gap detection
11. these modules consume typed workflow context instead of loose transitive dict coupling

### Operator Plane

12. `OperatorSessionManager`
   - durable pending decisions, redirects, replay, and session continuity
13. `HumanDecisionInterface`
   - remains the rendering surface, now backed by session state rather than only artifacts

### Observability Plane

14. `TelemetryAggregator`
   - rolling health summaries, pressure signals, and architecture diagnostics
15. append-only logs remain, but become one output of a richer observability model

## AAS3 Stack

1. Invention Pipeline Manager
2. Pipeline Stage Registry
3. Workflow Context Store
4. Governance Kernel
5. Program State Store
6. Knowledge Index
7. Discovery Graph Store
8. Invention Intelligence Modules
9. Research Director Model
10. Operator Session Manager
11. Human Decision Interface
12. Artifact Projection Layer
13. Telemetry Aggregator

## Why AAS3 Is Better

### Better Capability

- supports long-running research programs without repeated full reconstruction
- makes discovery and program state durable rather than report-derived
- supports richer operator workflows and resumable sessions

### Better Stability

- reduces hidden orchestration coupling
- creates authoritative governance state for scope locks and dependencies
- keeps artifact outputs while moving fragile state out of raw file scans

### Better Evolution

- stage registry makes new modules easier to insert safely
- workflow context reduces dict-shaped coupling
- graph and program stores make future reasoning modules easier to integrate

## Explicit Non-Changes

AAS3 does not:

- remove human authority
- replace the single-controller model with distributed autonomous controllers
- replace repo artifacts as the human-readable system of record

## Recommendation

Adopt AAS3 as the next architecture target, but implement it incrementally on top of AAS2.
