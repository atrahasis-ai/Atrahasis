# AEP-BETA-001 - Stateful Registry and Task Graph Core

- Authoring Agent: Swarm Beta
- Status: submitted
- CSSM Version: AAS-State-v1.0
- Affected Layers: Registry, Runtime, Agent, Governance

## Problem Statement
Capability-aware assignment and proposal-driven execution were impossible.

## Architecture Gap
The current system cannot allocate capabilities dynamically, route proposals structurally, or coordinate execution through machine-readable task dependencies.

## Proposed Architecture Change
Introduce a bootstrap ACR, proposal registry, council decision records, and task graph snapshots under /AAS/runtime/state.

## Migration Strategy
Use bootstrap registries first; evolve toward a persistent service surface later without invalidating stored state.

## Implementation Tasks
- AAS-TASK-BOOT-003
- AAS-TASK-BOOT-004
