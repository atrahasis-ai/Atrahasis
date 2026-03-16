# Atrahasis Operator UI
**Platform:** OpenAI Codex  
**Purpose:** Run a local operator console over the Atrahasis controller HTTP service and the local Codex App Server bridge

---

## What It Is

The operator UI is:
- a browser console served locally from this repo
- backed by the Atrahasis HTTP controller surface for canonical state and controller actions
- backed by the controller-owned Codex App Server bridge for thread, turn, review, and approval control

Start it with:

```bash
python scripts/aas_controller.py serve --open
```

---

## Runtime Split

- `scripts/aas_controller.py serve`
  Starts the local HTTP service and serves the browser UI.
- `src/aas1/operator_http_service.py`
  Hosts the controller HTTP endpoints and manages the optional local App Server subprocess.
- `ui/operator_console.html`
  Browser UI for operator workflows.
- `codex app-server`
  Owns thread lifecycle, turns, review mode, approvals, and live runtime events.

This means:
- Atrahasis policy stays in the controller layer.
- Codex session mechanics stay in the App Server layer.
- The browser UI sits in front of the controller, and the controller owns the App Server session.

---

## Dashboard Surface

The operator console is now structured as a dashboard instead of a flat wall of raw payloads.

### Operator Dashboard

- **Overview summary**
  Shows the selected task, queue pressure, pending HITL count, notification count, audit event count, and last refresh signal.
- **Notifications**
  Derives operator alerts from service health, App Server posture, pending HITL, workflow-policy next actions, and recent audit churn.
- **AAS5 Update Window**
  Surfaces only major, high-confidence controller-observed AAS5 improvement advisories, such as reliability hardening, HITL pressure, convergence tuning, or stage-contract drift. Advisories now need sustained evidence across consecutive controller cycles before they open, and acknowledging one suppresses reopening for a cooldown window.
- **Service & App Health**
  Summarizes controller health, App Server status, event-stream state, and provider-session visibility.

### Active Work Surfaces

- **Active Tasks & Dispatchable Queue**
  Renders dispatchable work as tiles instead of a flat list so operators can load tasks directly into the runtime panels.
- **Task Runtime & Focus**
  Shows selected-task status, stage, thread bindings, and dispatch posture before the raw run-state payload.
- **Redesign Memory**
  Surfaces the current task's distilled redesign-memory entry plus related prior redesign cycles so operators can see relevant historical structural moves without opening raw branch artifacts.
- **Workflow Policy**
  Surfaces policy-provided next actions before the underlying JSON payload and keeps dispatch mode, auto-closeout, and monitor controls together.
- **HITL Queue**
  Adds a summary layer by HITL category so pending approvals are visible before the detailed queue entries.
- **Audit Timeline**
  Adds a timeline rollup with visible event count, latest event, dominant category, and a short recent-event list before the raw payload.

### Operator Forms

- **Review Form**
  Finalize controller review outcomes from a structured surface.
- **Human Decision Form**
  Record the operator decision and workflow status explicitly.
- **Claim Form**
  Create controller-owned claims with bounded scope metadata.
- **Handoff Form**
  Write handoff packets without leaving the dashboard.
- **Closeout**
  Execute closeout with validator control and raw result visibility.

---

## HTTP Endpoints Used By The UI

### Reads

- `GET /api/health`
- `GET /api/controller/dispatchable`
- `GET /api/controller/provider-sessions`
- `GET /api/controller/dashboard-summary`
- `GET /api/controller/notifications`
- `GET /api/controller/improvement-advisories`
- `GET /api/controller/daemon-status`
- `GET /api/controller/run-state?task_id=T-300`
- `GET /api/controller/workflow-policy?task_id=T-300`
- `GET /api/controller/audit-timeline?task_id=T-300`
- `GET /api/controller/hitl-queue?task_id=T-300`
- `GET /api/controller/events?task_id=T-300`

### Actions

- `POST /api/app-server/start`
- `POST /api/app-server/stop`
- `POST /api/controller/start-task-thread`
- `POST /api/controller/start-task-turn`
- `POST /api/controller/sync-task-run`
- `POST /api/controller/evaluate-workflow-policy`
- `POST /api/controller/configure-workflow-policy`
- `POST /api/controller/recover-state`
- `POST /api/controller/monitor-cycle`
- `POST /api/controller/start-review`
- `POST /api/controller/acknowledge-notification`
- `POST /api/controller/acknowledge-improvement-advisory`
- `POST /api/controller/respond-hitl`
- `POST /api/controller/record-human-decision`
- `POST /api/controller/finalize-review`
- `POST /api/controller/create-claim`
- `POST /api/controller/write-handoff`
- `POST /api/controller/execute-closeout`
- `POST /api/controller/daemon-start`
- `POST /api/controller/daemon-stop`

---

## Operator Workflow

1. Open the local operator console.
2. Inspect the overview summary for selected-task posture, queue load, notifications, AAS5 update pressure, and audit churn.
3. Start the App Server if runtime work is needed and it is not already running.
4. Use **Active Tasks & Dispatchable Queue** to choose the next task to load.
5. Inspect **Task Runtime & Focus** before starting a new thread or turn.
6. Use **Workflow Policy** to understand dispatch posture and next actions before forcing manual changes.
7. Resolve **HITL Queue** items directly from the dashboard instead of jumping into raw payloads first.
8. Use the structured forms for review, decisions, claims, handoffs, and closeout.
9. Check the **AAS5 Update Window** when you want controller-authored opinions about major system improvements that may be worth implementing.
10. Watch **Audit Timeline** and **Event Stream** for recent controller behavior and drift.

---

## Why This Split Exists

The controller app and the App Server are not the same component.

- The controller app knows Atrahasis workflow and canonical state.
- The App Server knows Codex thread, turn, review, and runtime protocol.
- The UI is more reliable when App Server mutations and approvals are mediated by the controller instead of browser-local state.

---

## Current Limits

The controller now provides authoritative dashboard, notification, and daemon surfaces, so the browser is no longer inventing those summaries locally.

Remaining limits:
- the UI is still a local operator workbench, not a packaged desktop product
- live validation still depends on a working local Codex/App Server environment with real model traffic
- review templates are role-aware, but they are still markdown-driven rather than backed by a richer policy language
