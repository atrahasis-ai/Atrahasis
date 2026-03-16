# T-300 Boundary Policy Draft

## Purpose

Define the exact authority boundary between the old communication stack
(`C4 ASV + A2A/MCP`) and the active Alternative C sovereign stack so downstream
retrofit tasks can replace the old assumptions without deleting the baseline
they still need to reference.

## Governing inputs

- `ADR-006` and `ADR-007` established the old posture:
  - `ASV` as the communication vocabulary
  - `A2A/MCP` as the protocol layer
  - `AACP` retired as a sovereign protocol direction
- `ADR-041` activated the sovereign replacement backlog and explicitly deferred
  final `C4` retirement/adaptation boundaries to later supersession work.
- `ADR-042` retained `C4` as historical baseline and compatibility reference.
- `ADR-044` / `C38` established the new root authority for sovereign
  communication architecture.
- `T-301` identified the audited old-stack footprint that still depends on the
  old posture.

## Boundary decision

### 1. What is superseded

The following `C4` positions are superseded as forward-looking normative design
authority for Atrahasis:

- `ASV` as the intended end-state communication layer for the repo.
- `A2A` and `MCP` as the canonical protocol substrate for future Atrahasis
  communication design.
- `AACP is retired` as a standing architectural doctrine.
- `Vocabulary, not protocol` as the controlling end-state communication posture.
- Any statement that Atrahasis communication should remain embedded in external
  protocol ecosystems as its primary permanent architecture.
- Any top-level architecture description that still names `ASV` as Layer 1 of
  the active future stack.

### 2. What remains authoritative from C4

`C4` remains authoritative only in these bounded roles:

- historical record of the old communication architecture that the rest of the
  repo was written against
- compatibility baseline for retrofit, migration, audit, and bridge-policy work
- source of old-stack semantic object expectations where downstream rewrite
  tasks need to understand what existing specs meant before Alternative C
  replacement
- comparison baseline for `T-300+` retrofit tasks and any later migration or
  bridge retirement analysis

`C4` does **not** remain authoritative for new sovereign communication design.

### 3. What replaces C4 as forward authority

Alternative C forward authority now resolves as follows:

- root architecture: `C38`
- message inventory and lineage posture: `C39`
- security authority: `C40`
- discovery manifest authority: `C41`
- tool authority surface: `C42`
- native server framework authority: `C45`
- A2A ingress boundary as bounded migration membrane: `C46`
- zero-runtime-bridge ingestion and native upgrade path: `C47`
- cross-layer integration target for Atrahasis specs: `T-290` / `AXIP-v1`

For any future design or direct-spec task, these Alternative C authorities win
over `C4` unless the task is explicitly scoped to compatibility, audit,
supersession, migration, or historical comparison.

## Canonical file classification

### Compatibility / historical baseline surfaces to retain

- `docs/specifications/C4 - Agent Abstraction and Control Protocol/C4_Agent_Abstraction_and_Control_Protocol_Master_Tech_Spec.md`
- `docs/specifications/C4 - Agent Abstraction and Control Protocol/architecture.md`
- `docs/specifications/C4 - Agent Abstraction and Control Protocol/technical_spec.md`

These files stay in the repo and remain citable only as old-stack baseline and
compatibility context.

### Immediate boundary-affected narrative surface

- `docs/specifications/UNIFIED_ARCHITECTURE.md`

This file currently presents `ASV` as Layer 1 of the architecture narrative.
After `T-300`, that posture must be treated as superseded old-stack narrative,
not current end-state doctrine.

### Downstream retrofit surfaces governed by this boundary

- `T-302`: cross-layer communication rewrites
- `T-303`: provenance / trust boundary rewrites
- `T-304`: economics and funding assumptions tied to the old stack
- `T-305`: implementation roadmap and sequencing assumptions
- `T-306`: interface / DX rewrite of old communication assumptions
- `T-307`: migration and conversion strategy under the new boundary
- `T-308`: terminology cleanup after substantive rewrites
- `T-309`: external packaging refresh after all above changes settle

## Operational rules for downstream work

1. A task in `T-200` through `T-291` MUST NOT treat `C4` as normative forward
   communication authority.
2. A task in `T-300` through `T-309` MUST read `C4` directly when rewriting
   old-stack assumptions.
3. Downstream retrofit tasks MUST replace explicit `ASV + A2A/MCP` end-state
   assumptions with the relevant Alternative C authorities rather than vaguely
   referring to a generic future protocol.
4. No task may delete `C4` or hide it from the working repo until the retrofit
   program completes and a later governance decision defines archive posture.
5. Historical references to `Alternative B` remain valid as source-packet
   lineage, but repo-canonical execution posture remains `Alternative C`.

## Main failure mode to avoid

The dangerous mistake is collapsing `C4` into one of two wrong extremes:

- treating `C4` as still normatively active, which would preserve stale
  `ASV + A2A/MCP` assumptions in downstream retrofits
- treating `C4` as disposable and fully obsolete, which would destroy the
  baseline needed to rewrite the repo coherently

This task must instead keep `C4` visible, retained, and bounded while making
Alternative C the only forward design authority.
