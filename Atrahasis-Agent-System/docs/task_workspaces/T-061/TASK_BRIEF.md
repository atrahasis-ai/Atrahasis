# T-061 Task Brief - Agent Execution Runtime

## Problem Statement

Atrahasis has orchestration (C7), coordination (C3), verification (C5), knowledge metabolism (C6), settlement (C8), and implementation planning (C22), but it does not yet define the runtime substrate that actually executes agent work. Existing specs assume that agents can:

- receive leaf intents from C7 Parcel Executors,
- run reasoning or tool work inside a bounded execution environment,
- acquire model access and external capabilities under policy,
- emit auditable evidence back into C5 and C8,
- preserve parcel-local placement without turning the runtime into an independent scheduler.

Those assumptions are architectural gaps today.

## Required Outcomes

- Define how an assigned agent actually runs work after `c3.schedule_operation()` and `parcel_executor.enqueue(...)`.
- Define runtime agent profiles without confusing them with constitutional AAS roles.
- Define execution isolation, resource budgets, and lifecycle semantics for cell execution.
- Define inference provisioning across local and remote model providers.
- Define the evidence contract from runtime execution into C5 PCVM and C8 DSF.

## Constraints

- Must remain additive to C3, C5, C7, C8, and C22 rather than replacing them.
- Must preserve agent sovereignty: identity and governance standing cannot collapse into container ownership.
- Must support both local and hosted inference providers.
- Must default to least privilege and deny ambient network/tool access.
- Must be implementable in the C22 Wave 1-3 technology stack (Rust, Python, TypeScript, NATS/PostgreSQL, local model adapters).

## Inputs Consulted

- `docs/specifications/C3/MASTER_TECH_SPEC.md`
- `docs/specifications/C5/MASTER_TECH_SPEC.md`
- `docs/specifications/C7/MASTER_TECH_SPEC.md`
- `docs/specifications/C22/MASTER_TECH_SPEC.md`

## Initial Synthesis

The runtime gap is one coherent subsystem, not three separate inventions, because execution isolation, inference access, evidence emission, and parcel-local placement are coupled by the same control surface: the lease that binds a leaf intent to an executing agent. The ideation step should still consider simpler alternatives, but the likely answer is one integrated runtime invention rather than multiple disconnected specs.
