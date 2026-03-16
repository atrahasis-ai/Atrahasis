# T-301 Task Brief

## Task
`T-301` - Repo-Wide Communication Dependency Audit

## Type
Analysis

## Agent
Inanna (Codex)

## Date
2026-03-12

## Objective
Inventory the canonical repo artifacts that still assume the old communication model
`C4 ASV + A2A/MCP`, then produce a dependency-safe retrofit patch order for the
Alternative B program.

## Verified prerequisites
- `T-200` is complete.
- `T-201` is also complete, but it is not a formal prerequisite for this task.
- `T-210` is not complete, so this audit does not invent missing protocol
  architecture. It only identifies dependency surfaces and orders future patching.

## Governing authority
- `ADR-041`: Alternative B is the active communication program.
- `ADR-042`: C4/ASV stays in-repo as historical baseline and compatibility
  reference; it is not normative design authority for `T-200+` protocol-design work.
- `TODO.md` Dependency Safety Rules and T-202 wave ordering are authoritative for
  sequencing.
- The Alternative B source packet is primary for program direction.

## Deliverables
- `COMM_DEPENDENCY_AUDIT.md` - narrative audit and patch-order recommendation
- `COMM_DEPENDENCY_INVENTORY.md` - artifact-by-artifact inventory of retrofit targets

## Scope notes
- Included: canonical specs, roadmap/implementation artifacts, funding/package
  artifacts, and current shared state where relevant.
- Excluded from retrofit inventory: prior-art research, handoffs, claim files,
  completed-task archive rows, and historical logs unless they materially affect
  patch ordering.
