# AAS4 Architecture Recommendation

## Decision

Do not adopt a full `AAS4 Distributed Research Runtime` as the next architecture target.

Proceed with `AAS3`.

## Rationale

The DRR candidate improves:

- research throughput
- parallel simulation capacity
- large-scale corpus processing
- horizontal scalability

But it regresses or complicates:

- system manageability
- maintainability
- security resilience
- operator transparency
- replay and recovery simplicity

For the current Atrahasis Agent System mission, those regressions are too costly.

## Recommended Path

1. implement `AAS3`
2. build clean dispatch seams inside the AAS3 control plane
3. keep governance, state persistence, and artifact projection authoritative
4. revisit distributed workers only after AAS3 proves stable under sustained workloads

## Future AAS4 Trigger Conditions

Re-evaluate an AAS4 worker-fabric architecture only if at least two of these conditions become true:

- more than `5` concurrent active research programs are routinely running
- experiment simulation becomes the dominant runtime cost
- knowledge-index refresh or retrieval latency becomes a repeated bottleneck
- novelty and feasibility evaluation queues exceed acceptable turnaround windows
- operator workflows require many background jobs between decisions

## If AAS4 Is Revisited Later

The recommended future form is not a distributed-control architecture.

It is a hybrid extension:

- `AAS3` remains the authoritative control, governance, and operator architecture
- a bounded distributed worker fabric is added underneath it for selected workloads only

## Final Recommendation

`AAS3` remains the superior next architecture.

`DRR` should be treated as a conditional future acceleration layer, not the immediate architecture replacement.
