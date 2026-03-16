# AAS2 Architecture Review

- Review target: `C:\Users\jever\Atrahasis\Atrahasis-Agent-System`
- Review mode: `AAS-RE architecture review and improvement cycle`
- Baseline runtime: `AAS2`
- Outcome: `targeted architectural evolution recommended`

## Baseline Sources

The requested `AAS1_*` reference files were not present under the Atrahasis workspace during this run.

This review therefore used the live AAS2 implementation and current runtime artifacts as the baseline:

- `src/aas1/invention_pipeline_manager.py`
- `src/aas1/gcml_memory_interface.py`
- `src/aas1/discovery/discovery_map.py`
- `src/aas1/research_program_engine.py`
- `src/aas1/research_director_model.py`
- `src/aas1/human_decision_interface.py`
- `docs/task_workspaces/T-903/*`

## Current AAS2 Shape

AAS2 is a human-guided invention intelligence runtime with the following strengths:

- one explicit orchestration authority
- schema-validated artifact production
- research-program governance with scope levels
- operator-facing decision packets
- cross-domain reasoning and ranking signals
- append-only telemetry and durable task workspaces

Its active architecture can be summarized as:

1. `InventionPipelineManager` as single orchestration authority
2. document-backed GCML memory and full-doc manifest scan
3. discovery and research synthesis plane
4. invention reasoning and evaluation plane
5. research-program governance and strategic prioritization
6. human decision and exploration control handoff
7. artifact persistence plus telemetry logging

## Swarm Findings

### Swarm Alpha - Optimization and Stabilization

Alpha found that AAS2 is architecturally coherent, but still paying a high complexity tax inside the orchestration spine.

Primary findings:

- `InventionPipelineManager` remains a control, persistence, sequencing, and telemetry monolith.
- `GCMLMemoryInterface` rescans the repo and rebuilds working context per run.
- the current strategy layer is useful, but still heuristic and stateless.
- command modifiers normalize input, but do not yet drive materially different execution profiles.

Alpha conclusion:

- optimize the current architecture rather than replace it
- introduce a stage registry and cached knowledge index
- keep the single-controller rule

### Swarm Beta - Structural Improvement and Decomposition

Beta found the highest-value improvements in durable state and module boundaries.

Primary findings:

- research-program governance still behaves as a report generator more than a true governance kernel
- the Discovery Map is an artifact projection, not a persistent graph service
- knowledge access is file-scan based rather than indexed or incremental
- operator interaction is a rendered prompt, not a durable session model

Beta conclusion:

- evolve AAS2 into a more stateful research runtime
- preserve human-guided control
- decompose orchestration into explicit control-plane services without distributing execution authority

### Swarm Gamma - Radical Alternatives

Gamma explored first-principles alternatives:

- persistent actor-style multi-agent runtime
- event-sourced architecture with long-lived autonomous workers
- database-first replacement of repo-backed artifacts

Gamma found real upside in persistent state and asynchronous coordination, but also identified serious risks:

- higher operator opacity
- weaker human-guided review unless additional control systems are built
- significantly higher implementation and debugging cost
- risk of replacing a clear controller with a distributed failure surface

Gamma conclusion:

- reject a radical distributed runtime for now
- absorb only the durable-state lessons

## Architectural Contradictions

1. AAS2 wants durable research memory, but its primary memory access path still rebuilds context from repo scans each run.
2. AAS2 wants governed long-running programs, but program state is still computed from transient artifacts rather than persisted as first-class runtime state.
3. AAS2 wants a discovery graph, but the graph is still an exported structure rather than a queryable system of record.
4. AAS2 wants modular evolution, but raw `dict[str, Any]` payload coupling is still the dominant module contract.
5. AAS2 wants operator leverage, but the operator interface is still prompt-centric rather than session-centric.
6. AAS2 wants structural flexibility, but most runtime policy still lives inside a single manager module.

## Evaluation Summary

- AAS2 baseline score: `0.68`
- Alpha candidate score: `0.73`
- Beta candidate score: `0.81`
- Gamma candidate score: `0.70`

Interpretation:

- AAS2 is not near-optimal.
- Improvement is large enough to justify a real architecture proposal.
- The best path is not radical replacement.
- The strongest result is a structured AAS3 evolution that preserves the single-controller and human-guided principles while adding durable control-plane state.

## Review Conclusion

AAS2 should not be discarded.

AAS2 should be evolved into AAS3 through targeted structural redesign in these areas:

- stage orchestration
- persistent knowledge indexing
- discovery graph persistence
- governance state
- operator session state
- telemetry aggregation

This is an architectural evolution, not a reset.
