# Atrahasis MCP Server
**Platform:** OpenAI Codex
**Purpose:** Provide a structured tool surface over canonical
Atrahasis state

---

## Phase 2 Scope

The server remains read-heavy, but now supports narrow writes.

The server exposes structured access to:
- `docs/SESSION_BRIEF.md`
- `docs/TODO.md`
- `docs/DECISIONS.md`
- `docs/task_claims/*.yaml`
- `docs/task_workspaces/<TASK_ID>/`
- runtime workflow and operator-session state
- runtime controller-run and HITL queue state
- runtime workflow-policy and audit-timeline state
- runtime redesign-memory state across tasks and cycles
- canonical spec lookup
- local schema validation

Narrow writes now supported:
- create a task claim
- write a task handoff
- record an operator decision into the current human/workflow records

It still does not perform arbitrary repo writes or bypass HITL gates.

---

## Config

Repo-local Codex config enables the server through:

```toml
[mcp_servers.atrahasis]
command = "python"
args = ["scripts/atrahasis_mcp_server.py"]
cwd = "C:\\Users\\jever\\Atrahasis\\Atrahasis-Agent-System"
enabled = true
startup_timeout_sec = 20
```

---

## Exposed Tools

- `get_session_brief`
- `get_dispatchable_tasks`
- `get_task_claims`
- `get_task_workspace_manifest`
- `get_decisions`
- `get_spec`
- `get_latest_workflow_context`
- `get_controller_run_state`
- `get_redesign_memory`
- `search_redesign_memory`
- `get_hitl_queue`
- `get_workflow_policy`
- `get_audit_timeline`
- `get_dashboard_summary`
- `get_notifications`
- `search_canonical_artifacts`
- `validate_artifact`
- `get_active_provider_sessions`
- `create_claim`
- `write_handoff`
- `record_human_decision`

---

## Operator Use

Inside this repo, Codex should see the MCP server automatically.

Use MCP tools when:
- the question is structured and repetitive
- the answer should come from canonical Atrahasis state
- you want to avoid re-reading large docs manually
- the write is one of the controller-approved narrow operations above

Do not treat MCP as a substitute for final synthesis or HITL judgment.
