# T-065 Task Brief - Infrastructure and Federation

## Problem Statement

Atrahasis has detailed architecture for coordination, verification, knowledge metabolism, orchestration, governance, economics, and runtime execution, but it still lacks a canonical deployment architecture. Existing specs define loci, parcels, epochs, and cross-locus behavior conceptually, yet do not specify:

- how physical and cloud compute is grouped into deployable infrastructure domains,
- how runtime hosts, state stores, buses, and gateways are arranged,
- how failure domains are bounded,
- how cross-region federation works without turning C3 into a WAN chat system.

This leaves a gap between the logical architecture and any real deployment plan.

## Required Outcomes

- Define the canonical infrastructure topology beneath C3/C7/C23.
- Define region, cluster, host, and gateway boundaries.
- Define intra-region versus cross-region traffic rules.
- Define the federation contract for explicit cross-region coordination.
- Define the deployment phases from single-habitat bootstrap to multi-region federation.

## Constraints

- Must remain additive to C3, C7, C8, C14, C22, and C23.
- Must not replace C3 logical loci/parcels with infrastructure-first abstractions.
- Must preserve the principle that most operations stay local and cross-region traffic is explicit and bounded.
- Must fit the Wave 1-5 technology assumptions already recorded in C22.
- Must leave room for future T-062 recovery/state assurance and T-066 monitoring work.

## Inputs Consulted

- `docs/specifications/C3/MASTER_TECH_SPEC.md`
- `docs/specifications/C22/MASTER_TECH_SPEC.md`
- `docs/specifications/C14/MASTER_TECH_SPEC.md`
- `docs/specifications/C23/MASTER_TECH_SPEC.md`

## Initial Synthesis

The gap is best treated as one coherent infrastructure invention, because region topology, control-plane boundaries, and federation semantics are inseparable. A flat “just deploy Kubernetes” answer is too generic, while a pure global mesh contradicts C3’s locality assumptions.
