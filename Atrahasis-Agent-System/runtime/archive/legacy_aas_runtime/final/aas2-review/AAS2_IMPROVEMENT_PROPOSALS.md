# AAS2 Improvement Proposals

## Proposal Set

### P1 - Introduce a Pipeline Stage Registry

- Problem: the orchestration spine is still hand-wired and tightly sequenced.
- Improvement: define runtime stages as registered units with declared inputs, outputs, and gating rules.
- Impact: lowers orchestration complexity and makes command-profile variation easier.
- Priority: `high`

### P2 - Add a Persistent Knowledge Index

- Problem: repo scanning and hypothesis archive loading are repeated every run.
- Improvement: build an incremental knowledge index over `docs/`, task artifacts, and research evidence.
- Impact: improves performance, reduces context drift, and creates a foundation for better retrieval.
- Priority: `high`

### P3 - Split Discovery Map into Graph Store + Artifact Projection

- Problem: the current Discovery Map is rebuilt as an artifact rather than maintained as durable runtime state.
- Improvement: keep a persistent graph store and project `DISCOVERY_MAP.json` from it.
- Impact: improves graph consistency, queryability, and long-running invention continuity.
- Priority: `high`

### P4 - Convert Research Program Governance into a Governance Kernel

- Problem: current governance logic is still report-centric and heuristic.
- Improvement: introduce a lock table, scope-domain registry, dependency graph, and explicit program transitions.
- Impact: improves stability under multi-program exploration and supports real L0 pause behavior.
- Priority: `high`

### P5 - Add Operator Session Management

- Problem: human review is rendered well, but not maintained as a durable conversation/session state machine.
- Improvement: persist operator decisions, pending actions, redirect history, and replayable review state.
- Impact: reduces operator friction and makes interrupted work resumable.
- Priority: `medium-high`

### P6 - Add Telemetry Aggregation and Runtime Health Summaries

- Problem: telemetry is append-only JSONL without higher-level health views.
- Improvement: add aggregation, counters, alert conditions, and workflow correlation summaries.
- Impact: improves diagnosis, pressure testing, and architecture tuning.
- Priority: `medium`

### P7 - Introduce Command Execution Profiles

- Problem: `AASBT`, `AASAQ`, `AASNI`, and `AASA` share most of the same execution shape.
- Improvement: define command-specific stage policies, stage skips, and depth rules.
- Impact: improves operator usability and prevents unnecessary reasoning work.
- Priority: `medium`

### P8 - Strengthen Typed Contracts Between Modules

- Problem: modules communicate mainly through loose dictionaries.
- Improvement: move critical runtime contracts to typed envelopes or dataclasses with versioned schemas.
- Impact: reduces hidden coupling and lowers change risk.
- Priority: `medium`

## Recommended Improvement Order

1. Pipeline Stage Registry
2. Persistent Knowledge Index
3. Governance Kernel
4. Discovery Graph Store
5. Operator Session Manager
6. Telemetry Aggregator
7. Command Profiles
8. Typed Runtime Contracts

## Non-Recommendations

The review does not recommend:

- replacing the single orchestration authority with autonomous distributed controllers
- abandoning repo-backed artifacts as canonical outputs
- removing mandatory human review gates
