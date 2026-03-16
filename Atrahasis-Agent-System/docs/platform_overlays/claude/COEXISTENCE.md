# Claude-Codex Coexistence Protocol
**Platform:** Claude Code (Anthropic)
**Purpose:** Rules for operating alongside Codex without corruption
**Shared boundary:** See `docs/platform_overlays/SHARED_OPERATING_MODEL.md`
**Parallel execution:** See `docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md`

---

## Parallel Execution (Claude-specific notes)

The full protocol is in `PARALLEL_EXECUTION_PROTOCOL.md`. Claude-specific behavior:

### Claiming
- Use `Read` tool to check `docs/task_claims/*.yaml` before claiming
- Create claim file with `Write` tool
- Platform field: `CLAUDE`

### Safe zone work
- Use Claude `Agent` tool for parallel sub-stages within a single invention (e.g., parallel assessors)
- All agent output writes to the claimed task's safe zone paths only
- For `FULL PIPELINE` tasks, do not promote any ideation concept or create per-invention artifacts until `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` records explicit user approval

### Handoff creation
- When task is done, create `docs/handoffs/T-<ID>_CLAUDE_HANDOFF.md`
- Follow the template in `docs/handoffs/HANDOFF_TEMPLATE.md`
- Include exact text for all shared state updates — not summaries, exact content

### Closeout
- Codex is the default closeout platform — Claude does NOT update shared state after parallel execution
- Claude writes a handoff file and waits for Codex to apply all deltas
- If Codex is unavailable for closeout, the user may explicitly direct Claude to perform closeout instead
- If Claude is designated for closeout, read ALL handoff files (both Claude and Codex) and apply in one pass using `Edit` tool

---

## Standing Rules (apply always)

### Rule 1: No model names in shared files
Reference `docs/platform_overlays/claude/MODEL_ROUTING.md` instead.

### Rule 2: ADRs are append-only history
ADR-030 (Codex model routing) stays in DECISIONS.md as historical record.

### Rule 3: Invention content is platform-independent
The ideas don't change based on which AI produced them.

### Rule 4: Repo is canonical, desktop is export-only
All active AAS work lives in `docs/`. Desktop folder is optional archive only.

### Rule 5: If conflict detected, flag don't delete
If Claude finds unexpected Codex-specific content in shared files:
1. Do not delete it
2. Note it in the pipeline output
3. Flag it to the user
4. Propose relocation to `docs/platform_overlays/codex/`

---

## Solo Execution

When Claude is confirmed as the only active platform:
- Claim files are optional but recommended
- Claude may update shared state directly — no handoff file needed
- The handoff protocol only applies during confirmed parallel execution

---

## Claude-Only Files (safe to modify freely, always)

| Path | Purpose |
|------|---------|
| `docs/platform_overlays/claude/*` | Claude overlay docs |
| `docs/handoffs/T-*_CLAUDE_HANDOFF.md` | Claude's completion handoffs |
| `docs/task_claims/T-*.yaml` (Claude-claimed only) | Claude's active claims |
| `~/.claude/projects/.../memory/MEMORY.md` | Claude session memory |
