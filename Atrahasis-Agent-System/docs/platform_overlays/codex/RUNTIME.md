# Codex Runtime Configuration
**Platform:** OpenAI Codex
**Purpose:** Codex-specific operational behavior for running AAS

---

## Session Persistence

Codex relies on repo-side durable state as the canonical memory surface for AAS work.

- **Canonical repo state:** `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\docs\`
- **Primary read-first files:** `AGENT_STATE.md`, `SESSION_BRIEF.md`, `TODO.md`, `DECISIONS.md`, `INVENTION_DASHBOARD.md`

Rule:
- treat repo docs as authoritative
- do not rely on desktop export folders for live context
- when a long run is recovered, rebuild context from repo artifacts first

## Bootstrap Readiness

Before claiming bootstrap is complete, Codex should confirm more than name registration.

Required bootstrap checks:
- read the contents of current active claim YAML files
- read `docs/specifications/STRATEGY/MASTER_REDESIGN_SPEC.md`
- resolve and read canonical `C14` and `C48`
- verify whether `rg` is actually available
- record whether child-agent capability is explicitly verified or still unverified
- record the parent model when the runtime exposes it; otherwise mark auditability as degraded

Preferred helper:

```bash
python scripts/audit_aas5_bootstrap.py --agent-name <NAME>
```

If the runtime does not expose parent model or child-agent capability, report that degraded auditability explicitly rather than claiming bootstrap proof you do not have.

---

## Tooling Behavior

Codex can:
- read and edit repo files directly
- run shell commands for validation, search, and diff review
- parallelize safe read-only exploration
- spawn bounded child sessions when the task warrants real delegation
- run schema-constrained non-interactive executions for machine-consumed artifacts
- opt into live web search when a research task actually requires current external evidence

Operational rules:
- prefer `rg` for search
- if `rg` is unavailable in the session shell, fall back to PowerShell-native search (`Get-ChildItem`, `Select-String`) instead of treating that as a blocker
- use non-destructive git commands
- update shared state explicitly after meaningful AAS work
- when a prompt or repo doc names a spec by id such as `C42` or by old shorthand such as `docs/specifications/C42/MASTER_TECH_SPEC.md`, resolve the real titled file path first with `python scripts/resolve_spec_path.py <SPEC_ID>` or the MCP `get_spec` / `resolve_spec_path` tools
- keep platform-specific policy inside `docs/platform_overlays/codex/`
- follow `docs/platform_overlays/codex/TEAM_FORMATION.md` when deciding whether
  to stay single-session or form a real child-agent team
- if a substantive post-bootstrap operator prompt arrives, route it through task classification before answering it directly
- if a prompt begins with `Full Pipeline Task:`, treat that as a hard operator modifier: no judgment-call downgrade to parent-only advisory analysis is allowed
- follow `docs/platform_overlays/codex/SCHEMA_EXECUTION.md` when the output must
  match a schema or feed another AAS5 artifact
- follow `docs/platform_overlays/codex/WEB_SEARCH.md` before enabling live
  external search

## Team Formation

Codex may use real child sessions, but delegation is a controlled execution
pattern rather than an open-ended swarm.

Rules:
- the parent session remains the Swarm Director and is accountable for the final
  result
- child sessions are read-only by default unless the parent has assigned a
  specific task safe zone
- child sessions do not own HITL gates, concept promotion, invention-ID minting,
  or shared-state closeout
- use `docs/platform_overlays/codex/TEAM_FORMATION.md` as the binding policy for
  role choice, fan-out limits, and child-result handling
- when the task is architecture-heavy, Codex may use a bounded
  `FUTURE_BRANCH_SWARM` so the parent can compare typed futures before
  converging
- when the future swarm is used for a live task, treat it as bounded
  task-improvement lanes rather than as a detached redesign exercise
- for ordinary `FULL PIPELINE / IDEATION`, the default future swarm is the
  AAS5 `25`-agent hierarchy: `1` master orchestrator, `4` lane managers,
  `12` branch workers, `4` lane convergence reporters, and `4` independent
  auditors
- when the improvement trigger policy is enabled, Codex must surface the parent
  integration decision explicitly through `TASK_IMPROVEMENT_REPORT.json`
- when the future swarm enables a radical redesign lane, Codex must surface the
  parent decision explicitly through `RADICAL_REDESIGN_REPORT.json`
- architecture-heavy `FULL PIPELINE / IDEATION` must use a real bounded child
  swarm with execution evidence; if real child sessions are unavailable, stop
  and report the blocker instead of simulating the swarm internally
- the ordinary `FULL PIPELINE / IDEATION` default is the four-lane
  `Alpha/Beta/Gamma/Radical` future swarm with lane managers, not the older
  flat three-role readout

## MCP Surface

Repo-local Codex config enables the Atrahasis read-only MCP server for
structured access to canonical state.

Read:
- `docs/platform_overlays/codex/MCP_SERVER.md`

Use the MCP tools for structured lookup and validation when they are a better
fit than manually re-reading large repo surfaces.

## FULL PIPELINE HITL Enforcement

When Codex is assigned a `FULL PIPELINE` task and there is no separate persistent
Director session, Codex acts as the Director proxy for ideation approval gates.

Rules:
- stop after `IDEATION` once concept options exist,
- present the concepts to the user for selection,
- do not mint any `C-xxx` invention ID until the user explicitly approves concept
  promotion,
- record that approval in `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` before
  creating per-invention artifacts.

For architecture-heavy ideation:
- do not present an AAS swarm option set unless the task has a real
  `TEAM_PLAN.yaml`, `FUTURE_BRANCH_REPORT.json`, `SWARM_EXECUTION_RECORD.json`,
  `CHILD_RESULT_MERGE_PACKAGE.json`, `SWARM_TOPOLOGY_GRAPH.json`,
  `EXECUTION_PARALLELISM_RECORD.json`, four lane convergence reports, and four
  audit artifacts
- do not present an ideation recommendation unless the AAS5 artifact bundle
  authorizes recommendation and `validate_swarm_execution_record.py` passes
- if execution was batched instead of simultaneous, record that as degraded
  rather than equivalent and require explicit operator acknowledgement before
  recommendation
- if multi-agent capability is disabled or unavailable, stop and report that
  the required swarm could not be formed
- if the operator used `Full Pipeline Task:`, parent-only advisory fallback is not allowed; either run the strict ideation path or report noncompliance

`recommended_concepts` and `hitl_required: true` are decision inputs, not self-
executing authorization.

---

## File I/O

### Paths
- **Canonical working state:** `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\docs\`
- **Desktop export/archive root:** `C:\Users\jever\OneDrive\Desktop\Atrahasis Agent System\`

Rule:
- all active AAS work reads from and writes to the repo
- desktop paths are historical/export destinations only
- export to desktop only when the user explicitly requests it

### Parallel execution rule
When another platform has an active claim:
- claim Codex work through `docs/task_claims/<TASK_ID>.yaml`
- write only to the claimed task safe zone
- do not modify shared state directly
- write completion deltas to `docs/handoffs/<TASK_ID>_CODEX_HANDOFF.md`
- if the completed task appears in `docs/TODO.md`'s `User Dispatch Order (Simple)`, include the exact UDO removal in the handoff
- wait for designated sequential closeout per `docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md`

### Validation
Use the repo validators when available:

```bash
python scripts/validate_agent_state.py docs/AGENT_STATE.md
python scripts/validate_contribution_requests.py docs/contribution_requests
```

If local dependencies are missing, report the gap rather than assuming validation passed.

## Schema-Driven Execution

Use schema-driven execution when the result is meant to feed another artifact or
automation surface.

Preferred wrapper:

```bash
python scripts/run_aas5_schema_exec.py \
  --schema docs/schemas/<schema>.json \
  --output docs/task_workspaces/T-<ID>/<ARTIFACT>.json \
  --prompt-file <prompt.txt>
```

This wrapper captures:
- the schema-constrained final output
- the Codex JSONL event stream
- stderr sidecar logs

## Web Search

Live web search is opt-in and research-scoped.

Interactive launcher:

```powershell
pwsh -File scripts/start_aas5_codex.ps1 -Search
```

Non-interactive wrapper:

```bash
python scripts/run_aas5_schema_exec.py --search --schema <schema> --output <artifact> --prompt-file <prompt.txt>
```

Use live search only when current external evidence is actually required.

---

## Git Behavior

- Do not commit unless the user requests it
- Do not push unless the user requests it
- Treat existing local changes carefully
- Preserve unrelated user/Claude changes in shared files

---

## Opening Brief Adaptation

The Master Prompt opening brief is executed against repo-canonical docs.

Minimum read set:
- `docs/AGENT_STATE.md`
- `docs/SESSION_BRIEF.md`
- `docs/TODO.md`
- `docs/DECISIONS.md`
- `docs/INVENTION_DASHBOARD.md`

Operational reminder:
- for `FULL PIPELINE` tasks, the ideation gate is a stop point; after reading the
  repo context, Codex must still pause for user concept approval before promotion
  if the task has reached ideation output.
- for `DIRECT SPEC` tasks, Codex must not stop at narrative progress checkpoints;
  it should continue until blocked, HITL-gated, or ready for assessment/closeout.

## CLI Task Hardening

When the operator starts a real backlog task in the terminal, Codex should turn
that into machine-checked setup and finish rules rather than relying on prose
memory alone.

Required commands:

```bash
python scripts/prepare_aas5_task.py T-<ID>
```

Use the generated `TASK_START_CHECKLIST.json` as the start contract.

For exploratory `AASNI` or noncanonical architecture-heavy `FULL PIPELINE / IDEATION` tasks:

```bash
python scripts/prepare_aas5_idea_task.py --title "<IDEA TITLE>" --prompt-file <prompt.txt>
```

Use the generated analysis-band `T-900x` workspace as the ideation anchor. Do
not keep the run session-only.

This noncanonical workspace is task-local audit state. It does not count as the
forbidden shared-state progression covered by `docs/TODO.md`, task claims, or
handoff closeout.

Reference templates:
- `docs/platform_overlays/codex/templates/AAS5_TASK_EXECUTION_PROMPT_TEMPLATE.md`
- `docs/templates/AUTHORITY_COVERAGE_MATRIX_TEMPLATE.json`
- `docs/templates/TASK_START_CHECKLIST_TEMPLATE.json`
- `docs/templates/DIRECT_SPEC_AUDIT_RECORD_TEMPLATE.json`
- `docs/templates/DIRECT_SPEC_VERIFICATION_REPORT_TEMPLATE.json`
- `docs/templates/CLOSEOUT_CONSISTENCY_REPORT_TEMPLATE.json`
- `docs/templates/FUTURE_BRANCH_REPORT_TEMPLATE.json`
- `docs/templates/SWARM_EXECUTION_RECORD_TEMPLATE.json`

Spec resolver:

```bash
python scripts/resolve_spec_path.py C42
```

For architecture-heavy `FULL PIPELINE / IDEATION` tasks:

```bash
python scripts/validate_swarm_execution_record.py T-<ID>
```

For `DIRECT SPEC` tasks:

```bash
python scripts/verify_direct_spec_task.py T-<ID>
python scripts/validate_task_closeout_consistency.py T-<ID>
```

Rules:
- do not claim a purge or terminology sweep is clean until the direct-spec
  verification report records `clean=true`
- do not mark a task `DONE` until the closeout consistency report records
  `valid=true`
- keep at least the minimal task-local audit surface even when the actual edits
  land in shared canonical specs outside the task workspace
- read the contents of current claim YAML files before exploratory ideation so
  the swarm has real parallel-context awareness
- when ideation or research names explicit authority surfaces or asks whether an
  idea is already subsumed versus requiring a new subsystem, produce
  `AUTHORITY_COVERAGE_MATRIX.json` and do not finalize a recommendation until
  every named surface has an explicit disposition
- when a real swarm is required, persist child result artifacts under
  `docs/task_workspaces/T-<ID>/children/` and make sure
  `SWARM_EXECUTION_RECORD.json` points at them and `FUTURE_BRANCH_REPORT.json`
  enumerates the required Alpha/Beta/Gamma/Radical branch ids
- when child artifacts are persisted, record session identity, model auditability,
  and whether the artifact was written directly by the child or by a parent proxy
- the default `scripts/start_aas5_codex.ps1` launcher should come up with
  `multi_agent` enabled; pass `-NoMultiAgent` only when intentionally debugging
  or running an explicitly non-swarm session
- the default launcher should also inject the vendored `rg.exe` path into
  `PATH` when available so Codex child shells can use `rg` consistently
- when a real swarm is required, internal role-play is not a valid substitute

Read `docs/TRIBUNAL_LOG.md` only when needed for adjudication, recovery, or dispute resolution.
