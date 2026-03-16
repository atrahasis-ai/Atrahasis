# C24 IDEATION - Federated Habitat Fabric (FHF)

**Invention:** C24 - Federated Habitat Fabric (FHF)
**Parent Task:** T-065
**Stage:** IDEATION
**Date:** 2026-03-12
**Status:** COMPLETE

---

## Problem Statement

Atrahasis lacks a canonical deployment architecture. The stack defines loci, parcels, runtimes, governance, and settlement, but it does not define the infrastructure boundary that hosts them or the explicit mechanism for cross-region federation.

## Concepts Considered

### IC-1 - Cloud-Native Monocluster

- Strength: easy bootstrap and highly feasible.
- Weakness: too generic and too centralized to answer the long-term infrastructure question.

### IC-2 - Federated Habitat Fabric (FHF)

- Strength: introduces the missing region-scoped deployment primitive and explicit federation gateways.
- Weakness: adds control-plane structure and inter-habitat rules that must be kept disciplined.

### IC-3 - Planetary Flat Mesh

- Strength: globally flexible in theory.
- Weakness: poor locality discipline, diffuse failure domains, and weak sovereignty boundaries.

## Selection

**Selected concept: IC-2 - Federated Habitat Fabric (FHF).**

## Rationale

FHF is the only concept that solves both halves of the task:

- infrastructure topology,
- cross-region federation.

The central move is to define the **Habitat** as the missing deployment primitive between logical loci/parcels and raw cloud/physical infrastructure.

## Stage Verdict

**ADVANCE to RESEARCH**

Open questions for RESEARCH:

- What must remain habitat-local versus globally discoverable?
- How should cross-habitat state and artifacts move?
- How rigid should habitat boundaries be under scaling pressure?
