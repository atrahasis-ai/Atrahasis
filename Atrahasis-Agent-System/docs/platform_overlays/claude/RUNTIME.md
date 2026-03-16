# Claude Runtime Configuration
**Platform:** Claude Code (Anthropic)
**Purpose:** Claude-specific operational behavior for running AAS

---

## Session Persistence

Claude Code uses two persistence mechanisms:

### 1. Auto-Memory (cross-session)
- **Location:** `C:\Users\jever\.claude\projects\C--Users-jever\memory\MEMORY.md`
- **Purpose:** Carries key state (completed inventions, project locations, architectural decisions) across conversations
- **Limit:** ~200 lines visible in context; keep concise
- **Update rule:** After any AAS pipeline completion, update MEMORY.md with the new invention summary

### 2. Repo-Side Durable State (canonical)
- **Location:** `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\docs\`
- **Files:** AGENT_STATE.md, SESSION_BRIEF.md, DECISIONS.md, TODO.md, COMPLETED.md, INVENTION_DASHBOARD.md
- **Rule:** These are the source of truth. MEMORY.md is a summary cache, not authoritative.

### Context Compaction
Claude Code automatically compresses older messages when approaching context limits. This means:
- Long pipeline runs may lose early-stage details from conversational context
- Always write intermediate results to disk (invention logs, stage outputs) before proceeding
- The Opening Brief protocol (§5) exists precisely to recover state after compaction

---

## Agent Spawning

Claude Code can launch parallel sub-agents. Use this for:
- **Parallel specialist assessors** (§12.1) — all 5-6 assessors can run simultaneously
- **Parallel research** (§11) — Prior Art, Landscape, Science can run in parallel
- **Batch spec edits** — independent spec fixes across different files

Do NOT use parallel agents for:
- Sequential stage gates (IDEATION must complete before RESEARCH)
- Synthesis (requires all inputs gathered first)
- Any HITL gate (must pause for user)

### FULL PIPELINE HITL Enforcement

When Claude is assigned a `FULL PIPELINE` task and there is no separate persistent
Director session, Claude acts as the Director proxy for ideation approval gates.

Rules:
- stop after `IDEATION` once concept options exist,
- present the concepts to the user for selection,
- do not mint any `C-xxx` invention ID until the user explicitly approves concept
  promotion,
- record that approval in `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` before
  creating per-invention artifacts.

`recommended_concepts` and `hitl_required: true` are decision inputs, not self-
executing authorization.

---

## File I/O

### Output Paths
- **Canonical working state (all active AAS work):** `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\docs\`
- **Desktop folder (optional export/archive only):** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\`
- **Rule:** All pipeline work reads from and writes to the repo. The desktop folder is an export/archive/publish destination only — never a source of truth during active work. Export to desktop only when the user explicitly requests it.

### Tool Usage
- Use `Read` tool (not `cat`) for file reads
- Use `Edit` tool (not `sed`) for targeted edits
- Use `Write` tool for new file creation
- Use `Grep`/`Glob` for search (not `grep`/`find`)
- Use `Agent` tool for parallel sub-agent work
- Reserve `Bash` for git operations and script execution only

---

## Operational Notes

### Opening Brief Execution
The Master Prompt §5 specifies `cat` commands. Claude Code should use the `Read` tool instead:
```
Read docs/AGENT_STATE.md
Read docs/SESSION_BRIEF.md
Read docs/INVENTION_DASHBOARD.md
Read docs/PATTERN_REGISTER.md
Read docs/DECISIONS.md
Read docs/TODO.md
```
These can be read in parallel (up to 6 simultaneous reads).

Operational reminder:
- for `FULL PIPELINE` tasks, the ideation gate is a required stop point even after
  the opening brief is complete; do not self-promote a recommended concept.

### Schema Validation
Run validators via Bash tool:
```bash
python scripts/validate_agent_state.py docs/AGENT_STATE.md
```

### Git Operations
- Commit after each pipeline stage completion
- Use descriptive commit messages referencing invention ID and stage
- Do not push unless user explicitly requests it
