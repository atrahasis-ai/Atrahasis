# Atrahasis Repo Guide

## Scope
- Treat `Atrahasis-Agent-System/` as the canonical working area for the active Atrahasis workflow.
- Treat the other top-level folders as source material, historical outputs, or parallel concept folders. Do not reorganize or bulk-edit them unless the user explicitly asks.
- When the same concept appears both at the repo root and under `Atrahasis-Agent-System/docs/`, prefer the `Atrahasis-Agent-System` copy unless the task is explicitly about reconciliation.

## Read Order
- Start every substantive task by reading `Atrahasis-Agent-System/docs/SESSION_BRIEF.md`.
- Then read `Atrahasis-Agent-System/docs/AGENT_STATE.md` and `Atrahasis-Agent-System/docs/TODO.md`.
- Read `Atrahasis-Agent-System/docs/INVENTION_CONTEXT.md` before editing shared workflow artifacts.
- Pull in only the invention-specific files needed for the task after that.

## Current Source Of Truth
- Prefer the live filesystem over older descriptive docs.
- If documents conflict, use this precedence:
  1. `Atrahasis-Agent-System/docs/SESSION_BRIEF.md`
  2. `Atrahasis-Agent-System/docs/AGENT_STATE.md`
  3. `Atrahasis-Agent-System/docs/TODO.md`
  4. Relevant per-invention files in `Atrahasis-Agent-System/docs/`
  5. Older README or historical concept documents
- Important current-state correction: the active workflow uses `IDEATION -> RESEARCH -> FEASIBILITY -> DESIGN -> SPECIFICATION -> ASSESSMENT`. `PROTOTYPE` is no longer a default lifecycle stage, even though some older docs still mention it.
- Important current-state correction: the usual final deliverable is `docs/specifications/<ID>/MASTER_TECH_SPEC.md`, not separate `technical_spec.md` and `claims.md` files.

## Working Model
- New architecture or subsystem work should align to the AAS stage-gate process used in `Atrahasis-Agent-System`.
- Tasks in `docs/TODO.md` labeled as new inventions or new subsystems should be treated as full pipeline work.
- Tasks in `docs/TODO.md` labeled as direct spec edits should modify existing specifications instead of inventing a fresh subsystem.
- Preserve invention IDs (`C17`, `C23`, `T-070`, etc.) exactly and keep naming consistent across files.

## File Placement
- Session-wide state lives in `Atrahasis-Agent-System/docs/AGENT_STATE.md`, `Atrahasis-Agent-System/docs/INVENTION_DASHBOARD.md`, `Atrahasis-Agent-System/docs/DECISIONS.md`, and `Atrahasis-Agent-System/docs/TRIBUNAL_LOG.md`.
- Invention logs live in `Atrahasis-Agent-System/docs/invention_logs/`.
- Prior-art research lives in `Atrahasis-Agent-System/docs/prior_art/<ID>/`.
- Formal specifications live in `Atrahasis-Agent-System/docs/specifications/<ID>/`.
- Prototypes live in `Atrahasis-Agent-System/prototypes/<ID>/`.
- Contribution requests live in `Atrahasis-Agent-System/docs/contribution_requests/<ID>.yaml`.

## Edit Rules
- Read any target artifact fully before editing it.
- Keep changes narrow and mechanically consistent with the existing document structure.
- Do not rewrite large portions of master specs unless the task requires it.
- If the task is specialist-style work, do not directly edit Synthesis-owned shared artifacts; place requested changes in `docs/contribution_requests/<ID>.yaml` instead.
- If the task is synthesis-style work, apply contribution requests deterministically, then update the relevant state artifacts.
- When a task changes stage, status, or completion state, update the corresponding entries in `docs/AGENT_STATE.md`, `docs/INVENTION_DASHBOARD.md`, and related logs if they are part of the requested workflow.

## Validation
- Run `python scripts/validate_agent_state.py docs/AGENT_STATE.md` after editing `Atrahasis-Agent-System/docs/AGENT_STATE.md`.
- Run `python scripts/validate_contribution_requests.py docs/contribution_requests` after editing contribution request files.
- Run `python scripts/validate_invention_concept.py <file>` for invention concept JSON/YAML artifacts.
- If a prototype is added or changed, follow the commands in `Atrahasis-Agent-System/prototypes/<ID>/README.md` and capture exit codes and raw outputs.

## Human Approval Gates
- Stop and ask for explicit approval before concept selection, pivot decisions, external research, resource-intensive prototyping, patent strategy decisions, public disclosure, or abandonment.
- Record approval-sensitive changes in the canonical Atrahasis state files when the task includes state maintenance.

## Practical Notes
- Expect some documentation drift. Verify assumptions against the current files before propagating them.
- The repository is documentation-heavy; use `rg` to find the specific invention, task ID, or subsystem before editing.
- Preserve existing filenames, IDs, and terminology unless the task is explicitly about renaming or reconciliation.
