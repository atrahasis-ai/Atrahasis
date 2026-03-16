# Agent Registry
**Purpose:** Persistent identity for every supported platform session working on AAS.
**Rule:** Each agent self-names on first contact, registers here, and carries its name through compaction.

---

## Naming Convention
- Names are drawn from Mesopotamian mythology/history (thematic to Atrahasis)
- Each agent picks its own name on first activation -- no duplicates with active agents
- Retired agents free their names for future reuse
- The name appears in: this registry, task claim `agent_name` field, COMPLETED.md notes, TODO.md notes

## Active Agents

| Agent Name | Platform | Conv UUID (first 8) | Registered | Last Seen | Current Task | Status |
|------------|----------|---------------------|------------|-----------|--------------|--------|
| Enki | Claude Code | 804ff0b6 | 2026-03-12 | 2026-03-12 | T-067 (COMPLETE) | IDLE |
| Adapa | Claude Code | 734bcdbf | 2026-03-12 | 2026-03-12 | T-064 (COMPLETE) | IDLE |
| Inanna | Codex | 019ce01c | 2026-03-12 | 2026-03-12 | T-214 (COMPLETE) | IDLE |
| Ninsubur | Codex | 019cdf98 | 2026-03-12 | 2026-03-13 | -- | IDLE |
| Shamash | Claude Code | 6ecc7362 | 2026-03-12 | 2026-03-12 | T-089 (COMPLETE) | IDLE |
| Marduk | Codex | e1b431d27d9f | 2026-03-12 | 2026-03-12 | -- | IDLE |
| Nammu | Codex | 59b7e164eec3 | 2026-03-12 | 2026-03-12 | -- | IDLE |
| Nergal | Codex | e97a74d352fb | 2026-03-12 | 2026-03-12 | -- | IDLE |
| Ninurta | Codex | e46ece3c | 2026-03-13 | 2026-03-13 | -- | IDLE |
| Ashur | Codex | 210939a4 | 2026-03-13 | 2026-03-13 | -- | IDLE |
| Ninlil | Codex | 019cf189 | 2026-03-15 | 2026-03-15 | -- | IDLE |

## Retired Agents

| Agent Name | Platform | Conv UUID (first 8) | Registered | Retired | Tasks Completed |
|------------|----------|---------------------|------------|---------|-----------------|
<!-- None yet -->

---

## How to Register (new agent checklist)

1. Read this file to see which names are taken
2. Pick a Mesopotamian name not already in the Active table
3. Identify your conversation UUID from your transcript path (first 8 chars)
4. Add your row to the Active Agents table
5. When claiming a task, add `agent_name: "<YourName>"` to the task claim YAML
6. When completing a task, include your agent name in the Notes column of COMPLETED.md

## How to Recover After Compaction

1. Your compaction summary includes the transcript path -> extract your UUID (first 8 chars)
2. Read this file -> find your row by UUID -> you now know your name
3. Update `Last Seen` to today's date
4. Continue working

## Retirement

When a conversation ends permanently (user closes it, or agent confirms done):
- Move the row from Active to Retired
- Record tasks completed

---

*Created 2026-03-12 by Enki (Claude Code, 804ff0b6)*
