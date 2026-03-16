# T-300 Task Brief

## Task
`T-300` - ADR: C4 Supersession Boundary and Compatibility Policy

## Type
Governance

## Agent
Ninlil (Codex)

## Date
2026-03-15

## Objective
Define the authoritative supersession boundary for `C4 ASV` under the active
Alternative C program: what remains required as compatibility or historical
baseline, what is no longer normative design authority, and what downstream
retrofit tasks must replace rather than reinterpret.

## Verified prerequisites
- `T-210` is complete as `C38`, so Alternative C has a root sovereign
  communication architecture.
- `T-301` is complete, so the old `C4 ASV + A2A/MCP` footprint has already been
  audited instead of guessed.
- `T-291` is complete, but it is not a formal prerequisite for this task.
- No active non-`DONE` task claim currently overlaps the governance/shared-doc
  lane or `docs/task_workspaces/T-300/`.

## Governing authority
- `ADR-006` and `ADR-007` are the old communication-line decisions being
  superseded at the governance level.
- `ADR-041` activates the sovereign replacement program and explicitly preserves
  `C4` until supersession tasks define the boundary.
- `ADR-042` keeps `C4 ASV` in-repo as historical baseline and compatibility
  reference, and makes it required source material for `T-300+` work.
- `ADR-044` / `C38` define the root Alternative C communication architecture
  that now replaces `C4` as normative forward design authority.
- `docs/TODO.md` defines `T-300` as the next dispatchable canonical task and
  places it on the serialized governance/shared-doc lane.
- `docs/task_workspaces/T-301/COMM_DEPENDENCY_AUDIT.md` and
  `docs/task_workspaces/T-301/COMM_DEPENDENCY_INVENTORY.md` define the audited
  old-stack dependency footprint that this boundary must govern.

## Primary source files
- `docs/specifications/C04 - Agent Abstraction and Control Protocol/C4_Agent_Abstraction_and_Control_Protocol_Master_Tech_Spec.md`
- `docs/specifications/C04 - Agent Abstraction and Control Protocol/architecture.md`
- `docs/specifications/C04 - Agent Abstraction and Control Protocol/technical_spec.md`
- `docs/specifications/C38 - AACP Full Sovereign Protocol Architecture/C38_AACP_Full_Sovereign_Protocol_Architecture_Master_Tech_Spec.md`
- `docs/specifications/UNIFIED_ARCHITECTURE.md`

## Deliverables
- `TASK_BRIEF.md` - task scope, prerequisites, and governing authority
- `BOUNDARY_POLICY_DRAFT.md` - explicit C4 supersession and compatibility policy
- Shared-state closeout across the governance surfaces owned by this task

## Scope notes
- Included: the governance boundary for `C4`, compatibility-only retention
  rules, forward design authority under Alternative C, and downstream retrofit
  obligations implied by the boundary.
- Excluded: direct cross-layer spec rewrites (`T-302+`), bridge retirement
  strategy details (`T-307`), and terminology-only cleanup (`T-308`).
- This task must not collapse the baseline and the replacement into one blended
  posture. It has to state exactly where `C4` stops being normative and exactly
  where Alternative C starts being mandatory.

