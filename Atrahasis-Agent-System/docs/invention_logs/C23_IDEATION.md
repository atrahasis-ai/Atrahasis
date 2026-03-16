# C23 IDEATION - Sovereign Cell Runtime (SCR)

**Invention:** C23 - Sovereign Cell Runtime (SCR)
**Parent Task:** T-061
**Stage:** IDEATION
**Date:** 2026-03-12
**Status:** COMPLETE

---

## Problem Statement

Atrahasis specifies how work is proposed, decomposed, scheduled, verified, and settled, but it does not specify the runtime that actually executes a leaf intent on an assigned agent. The missing substrate includes:

- runtime agent profiles,
- execution isolation,
- inference provisioning,
- tool and network rights,
- evidence emission back into verification and settlement.

## Concepts Considered

### IC-1 - Agent-as-Container Fabric

- Strength: very feasible and familiar.
- Weakness: too generic and too permissive for Atrahasis sovereignty and evidence requirements.

### IC-2 - Sovereign Cell Runtime (SCR)

- Strength: integrates execution cells, leases, provider access, capability rights, and evidence sealing into one stack-native runtime.
- Weakness: more complex than generic workload orchestration.

### IC-3 - Serverless Intent Function Plane

- Strength: elastic and simple for burst workloads.
- Weakness: poor fit for parcel locality and persistent agent identity.

## Selection

**Selected concept: IC-2 - Sovereign Cell Runtime (SCR).**

## Rationale

SCR is the only concept that closes all four runtime gaps with one coherent control model. The central insight is to separate:

- persistent agent identity,
- transient execution cell,
- explicit lease granting rights and budgets.

That separation lets Atrahasis keep agent sovereignty while still enforcing least privilege, inference control, and auditable execution.

## Stage Verdict

**ADVANCE to RESEARCH**

Open questions for RESEARCH:

- Which execution profiles must be mandatory for each operation class?
- How should inference rights be leased across local versus hosted providers?
- What evidence should be mandatory for C5 without overstating reproducibility?
