# AAS Coordination Kernel Specification

The Coordination Kernel is the operating control plane of AAS-RE.

## Core Responsibilities

- PAEE cycle orchestration
- swarm lifecycle management
- proposal routing
- task graph scheduling
- telemetry aggregation

## Pipeline Ownership

The kernel advances every cycle through:

1. PAEE swarm exploration
2. architecture proposals
3. council review
4. architecture pressure testing
5. adversarial architecture review
6. final architecture selection
7. CSSM update

## State Ownership

The kernel reads and writes:

- canonical CSSM snapshots
- swarm-isolated CSSM snapshots
- proposal registry
- task graph
- council decisions
- recovery manifest
- telemetry logs

## Governance Contract

Councils retain approval authority, but the kernel is responsible for
ensuring proposals cannot bypass pressure testing, adversarial review,
or convergence checks.

## Convergence Contract

- `maximum_cycles = 20`
- stop when at least two of `capability_plateau`, `swarm_consensus`,
  and `aep_stagnation` are satisfied

## Objective

The kernel turns AAS-RE into a deterministic architecture research
runtime rather than a loosely coordinated prompt workflow.
