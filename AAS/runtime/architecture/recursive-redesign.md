# AAS Recursive Runtime Redesign

## Target Stack

- Strategic Planning Layer: sets long-horizon evolution objective and capability roadmap.
- PAEE: maintains three isolated swarms with distinct optimization philosophies.
- Coordination Kernel: explicit control plane for cycle orchestration, swarm lifecycle management, proposal routing, task scheduling, and telemetry aggregation.
- CSSM Store: canonical and swarm-isolated architecture snapshots under `/AAS/runtime/state/cssm/`.
- Registry Core: agent capability registry, proposal registry, council records, and task graph snapshots.
- GCML Bridge: existing repo docs remain the canonical narrative memory; runtime state points back to those artifacts.
- Architecture Pressure Testing: mandatory simulation of scalability, governance conflict, failure recovery, and evolution flexibility.
- Adversarial Architecture Review: mandatory red-team invalidation of architecture proposals before selection.
- Telemetry Spine: JSONL event logs back swarm, proposal, task, pressure, adversarial, council, and system activity.
- Recovery Loop: latest recovery manifest points to deterministic resume sources for CSSM, task graph, registry state, and expanded log streams.

## Evaluation Pipeline

- PAEE swarm exploration
- architecture proposals
- council review
- architecture pressure testing
- adversarial architecture review
- final architecture selection
- CSSM update

## Convergence Policy

- `maximum_cycles = 20`
- stop when at least two of `capability_plateau`, `swarm_consensus`, and `aep_stagnation` are met

## Readiness State

- AAS-RE has been upgraded in code, documents, and runtime metadata.
- PAEE has not been run after this upgrade.
