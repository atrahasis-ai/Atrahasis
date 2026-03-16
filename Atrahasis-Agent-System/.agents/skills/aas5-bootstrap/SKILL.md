---
name: aas5-bootstrap
description: Initialize a Codex session under the current Atrahasis operating prompt for the active AAS5 doctrine.
---

# AAS5 Bootstrap

## Overview

Use this skill to execute the Atrahasis initialization sequence without drifting into active task work. The repo copy of the active master prompt is mandatory context, not optional background.

## Workflow

1. Read the required initialization surfaces in order:
   - `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v5.md`
   - `docs/SESSION_BRIEF.md`
   - `docs/AGENT_STATE.md`
   - `docs/TODO.md`
   - `docs/DECISIONS.md`
   - `docs/INVENTION_DASHBOARD.md`
   - `docs/INVENTION_CONTEXT.md`
   - `docs/platform_overlays/SHARED_OPERATING_MODEL.md`
   - `docs/platform_overlays/AGENT_REGISTRY.md`
   - `docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md`
   - `docs/platform_overlays/codex/RUNTIME.md`
   - `docs/platform_overlays/codex/MODEL_ROUTING.md`
   - `docs/platform_overlays/codex/COEXISTENCE.md`
   - `docs/platform_overlays/codex/TEAM_FORMATION.md`
   - the contents of the current active `docs/task_claims/*.yaml` files
   - `docs/specifications/STRATEGY/MASTER_REDESIGN_SPEC.md`
   - the resolved canonical master tech spec for `C14`
   - the resolved canonical master tech spec for `C48`
   - verify whether `rg` is actually available in the shell; otherwise fall back to PowerShell-native `Get-ChildItem` / `Select-String`
2. Pick a non-colliding Mesopotamian name by checking `docs/AGENT_STATE.md` and `docs/platform_overlays/AGENT_REGISTRY.md`.
3. If the operator requested full initialization rather than a read-only test, register the session narrowly in `docs/AGENT_STATE.md`. Update `docs/platform_overlays/AGENT_REGISTRY.md` only when the runtime exposes a stable session id.
   - When editing `docs/AGENT_STATE.md`, do not set schema-constrained top-level fields such as `last_updated_by` to your agent name unless the schema explicitly allows it. Preserve the existing schema-allowed value or use the allowed system-maintainer value already defined by the file schema.
4. Validate `docs/AGENT_STATE.md` after editing it:
   - `python scripts/validate_agent_state.py docs/AGENT_STATE.md`
5. Run a bootstrap runtime audit:
   - `python scripts/audit_aas5_bootstrap.py --agent-name <NAME>`
   - pass `--parent-model`, `--reasoning-effort`, and `--child-agent-capable true|false` only when the runtime exposes them explicitly
6. Report:
   - chosen name
   - registration status
   - next dispatchable task from `docs/TODO.md`
   - one-sentence institutional primary objective from `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v5.md`, not the objective of the next task
   - bootstrap audit summary: active claim count, `rg` availability, child-agent capability status, parent-model auditability, and ordinary AAS5 ideation readiness (`verified`, `degraded`, or `unknown`)
7. Stop. Do not claim or start work until instructed.
   - After bootstrap, route the next substantive operator prompt through `aas5-task-routing` before answering it directly.
   - If the next prompt begins with `Full Pipeline Task:`, treat that as a hard modifier requiring strict full-pipeline routing rather than a lightweight judgment call.

## Guardrails

- Treat `Atrahasis-Agent-System/` as the only live working state.
- If the operator says `read-only`, `test only`, or `do not register`, skip registration and state that explicitly.
- Do not claim tasks, mint invention IDs, or cross HITL gates during bootstrap.
- If parent model identity or child-agent capability are not exposed, report degraded auditability instead of claiming verified readiness.
