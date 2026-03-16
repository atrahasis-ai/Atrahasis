# Distributed Research Runtime Architecture Proposal

## Purpose

`DRR` is a candidate architecture for increasing research throughput through bounded distributed execution while preserving the current Atrahasis control principles.

It is not a distributed-autonomy design.

## Governing Rules

DRR must preserve:

1. one orchestration authority
2. human-guided decisions
3. artifact-first system of record
4. governed research programs

## DRR Runtime Shape

### Control Plane

1. `InventionPipelineManager`
   - remains the only authority that sequences stages, commits state, and requests human decisions
2. `PipelineStageRegistry`
   - defines which stages may dispatch distributed jobs
3. `WorkflowContextStore`
   - stores typed stage inputs, task batches, and merge results
4. `TaskDispatcher`
   - translates stage work into bounded execution batches

### Distributed Execution Plane

5. `ResearchWorkerFabric`
   - transport and worker-registration layer for remote or local distributed workers
6. `WorkerPool`
   - scalable worker groups specialized by capability
7. `BatchResultMerger`
   - reconciles worker outputs into canonical stage outputs

### Worker Types

8. `ResearchIngestionWorker`
9. `HypothesisExplorationWorker`
10. `SimulationWorker`
11. `AnalysisWorker`

### State and Governance Plane

12. `GovernanceKernel`
13. `ProgramStateStore`
14. `KnowledgeIndex`
15. `DiscoveryGraphStore`
16. `ArtifactProjectionLayer`
17. `TelemetryAggregator`

### Operator Plane

18. `OperatorSessionManager`
19. `HumanDecisionInterface`

## Execution Rules

- workers may process tasks, but may not directly mutate governance state
- workers may not finalize artifacts directly
- only the pipeline manager may merge, accept, reject, or publish results
- all distributed tasks must be idempotent and replayable
- every worker result must carry provenance, batch id, and replay metadata

## Best-Fit Workloads

DRR is strongest when the runtime is dominated by:

- large research corpus ingestion
- many parallel novelty or feasibility checks
- large hypothesis fan-out exploration
- simulation-heavy workloads

## Main Risks

1. increased failure surface across queues, workers, and merges
2. result reconciliation conflicts
3. weaker operator transparency unless session and replay tooling are excellent
4. higher security and secrets-handling burden
5. higher debugging cost than AAS3

## Architectural Constraint

DRR only makes sense if AAS3-style durable context, governance state, and graph persistence already exist.

Without those foundations, distributed execution would raise throughput while lowering trust and control.
