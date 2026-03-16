# Gemini-Codex Coexistence Protocol
**Platform:** Gemini CLI
**Purpose:** Rules for operating alongside Codex without corrupting shared AAS state
**Shared boundary:** See `docs/platform_overlays/SHARED_OPERATING_MODEL.md`, `docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md`, and `docs/platform_overlays/PROVIDER_RUNTIME_ABSTRACTION.md`

---

## Shared Canon

Gemini must keep shared repo state vendor-neutral.

Do not inject Gemini-specific runtime behavior into:

- `docs/AGENT_STATE.md`
- `docs/SESSION_BRIEF.md`
- `docs/DECISIONS.md`
- `docs/TODO.md`
- `docs/COMPLETED.md`
- `docs/INVENTION_DASHBOARD.md`
- `docs/TRIBUNAL_LOG.md`

Put backend-specific behavior in:

- `docs/platform_overlays/gemini/*`

---

## Safe Concurrent Operation

When Codex and Gemini run simultaneously:

- both platforms must register backend sessions
- each task must have exactly one active claim
- each platform writes only inside its safe zone
- shared-state updates are serialized through handoffs when parallel execution is active

Codex remains the default closeout platform unless the user explicitly overrides that rule.
