# Task Brief - T-290

## Task

- ID: `T-290`
- Title: `AACP v2 Cross-Layer Integration with Atrahasis Stack`
- Type: `DIRECT SPEC`
- Priority: `HIGH`

## Verified prerequisites

- `T-210` complete as `C38` Five-Layer Sovereign Protocol Architecture
- `T-230` complete as `C40` Dual-Anchor Authority Fabric
- `T-240` complete as `C42` Lease-Primed Execution Mesh
- `T-214` complete as `C41` Layered Semantic Capability Manifest
- `T-301` complete as the repo-wide communication dependency audit

## Problem statement

Alternative B now has native transport, session, security, manifest, and tool
authority surfaces, but the live Atrahasis stack still treats `C4 ASV` as the
canonical inter-layer message surface in several places. `T-290` must specify
the additive integration contract that lets the stack move onto native
`AACP v2 + AASL` without prematurely rewriting the owning legacy specs.

## Required scope

- Define the canonical inter-layer communication spine for `C3`, `C5`, `C6`,
  `C7`, `C8`, `C23`, `C24`, and `C36`.
- Bind each layer to existing `C39` message classes rather than inventing new
  runtime message families.
- Define minimum `C40` security posture, `C41` manifest posture, and `C42`
  tool/runtime handoff posture for each major surface.
- Clarify the additive retrofit boundary for the rest of the stack so `T-302+`
  can rewrite legacy contracts against one agreed integration profile.

## Explicit non-goals

- Do not rewrite `C3`, `C5`, `C7`, `C8`, or `C36` inline.
- Do not mint a new `C-xxx` invention or ADR.
- Do not admit new public `AASL` object families beyond already-governed
  registry surfaces.
- Do not define bridge retirement or full supersession policy; that remains
  downstream of `T-300`, `T-302`, and `T-307`.

## Governing inputs

- `docs/specifications/C38/MASTER_TECH_SPEC.md`
- `docs/specifications/C39/MASTER_TECH_SPEC.md`
- `docs/specifications/C40/MASTER_TECH_SPEC.md`
- `docs/specifications/C41/MASTER_TECH_SPEC.md`
- `docs/specifications/C42/MASTER_TECH_SPEC.md`
- `docs/specifications/C23/MASTER_TECH_SPEC.md`
- `docs/specifications/C24/MASTER_TECH_SPEC.md`
- `docs/specifications/C36/MASTER_TECH_SPEC.md`
- `docs/specifications/C3/MASTER_TECH_SPEC.md`
- `docs/specifications/C5/MASTER_TECH_SPEC.md`
- `docs/specifications/C7/MASTER_TECH_SPEC.md`
- `docs/specifications/C8/MASTER_TECH_SPEC.md`
- `docs/task_workspaces/T-301/COMM_DEPENDENCY_AUDIT.md`
- `docs/task_workspaces/T-301/COMM_DEPENDENCY_INVENTORY.md`
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_AAS_Tasks.md`
