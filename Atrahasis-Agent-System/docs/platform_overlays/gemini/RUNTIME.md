# Gemini Runtime Configuration
**Platform:** Gemini CLI
**Purpose:** Gemini-specific operational behavior for running AAS3

---

## Session Persistence

Gemini must treat the repo as the canonical live state for AAS work.

- Canonical repo root: `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\`
- Canonical docs root: `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\docs\`

Rules:

- read shared state from the repo
- write active AAS artifacts to the repo
- do not treat desktop exports as live execution state

---

## Backend Registration

Gemini sessions must register through the AAS3 provider runtime before sustained work begins.

Preferred path:

```bash
python scripts/register_aas_backend.py gemini <agent_name> <session_id> --agent-type <type>
```

---

## Parallel Execution

When another platform has an active claim:

- claim Gemini work through `docs/task_claims/<TASK_ID>.yaml`
- write only inside the claimed task safe zone
- treat shared state as read-only during active parallel execution
- write shared-state deltas through handoff files

The provider runtime registry does not remove the need for the task-claim and handoff protocol.

---

## File I/O

- Active working state lives in the repo
- Desktop export remains optional archive/publish output only
- Preserve unrelated changes from other platforms

---

## HITL Rule

Gemini may help execute AAS work, but it must not bypass the mandatory human-guided review gates.
