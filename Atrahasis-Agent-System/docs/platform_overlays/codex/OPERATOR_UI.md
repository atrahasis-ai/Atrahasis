# Atrahasis Operator UI
**Platform:** OpenAI Codex  
**Purpose:** Run a local operator console over the Atrahasis controller HTTP service

---

## What It Is

The operator UI is:
- a browser console served locally from this repo
- backed by the Atrahasis HTTP controller surface for canonical state and controller actions
- focused on workflow policy, HITL, convergence, closeout, notifications, and repo-wide operator visibility

Start it with:

```bash
python scripts/aas_controller.py serve --open
```

---

## Runtime Posture

The controller-owned App Server runtime has been retired from AAS5.

That means:
- the UI no longer starts or stops a local App Server
- the UI no longer starts controller-owned threads, turns, or review sessions
- live model work happens through direct provider sessions, not through the browser console

The controller now acts as:
- a policy and state surface
- a review/finalization surface
- a HITL and closeout surface
- a repo-wide operational dashboard

---

## Dashboard Surface

### Operator Dashboard

- **Overview summary**
  Shows the selected task, queue pressure, pending HITL count, notification count, audit event count, and last refresh signal.
- **Notifications**
  Derives operator alerts from service health, retired-runtime posture, pending HITL, workflow-policy next actions, and recent audit churn.
- **AAS5 Update Window**
  Surfaces major, high-confidence controller-observed AAS5 improvement advisories.
- **Service & Runtime Health**
  Summarizes controller health, retired runtime posture, event-stream state, daemon state, and provider-session visibility.

### Active Work Surfaces

- **Canonical Dispatchable Queue**
  Renders dispatchable work directly from `docs/TODO.md`.
- **Task Runtime & Focus**
  Shows selected-task status, stage posture, retained run metadata, and dispatch posture before the raw run-state payload.
- **Redesign Memory**
  Surfaces the current task's distilled redesign-memory entry plus related prior redesign cycles.
- **Workflow Policy**
  Surfaces policy next actions before the underlying JSON payload and keeps dispatch mode, auto-closeout, and monitor controls together.
- **HITL Queue**
  Adds a summary layer by HITL category so pending approvals are visible before detailed queue entries.
- **Audit Timeline**
  Adds a timeline rollup with visible event count, latest event, dominant category, and a short recent-event list before the raw payload.

### Operator Forms

- **Review Form**
  Finalize review outcomes from a structured surface.
- **Convergence Gate**
  Record explicit parent disposition for branch-heavy stages.
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

- `POST /api/controller/evaluate-workflow-policy`
- `POST /api/controller/configure-workflow-policy`
- `POST /api/controller/recover-state`
- `POST /api/controller/monitor-cycle`
- `POST /api/controller/start-convergence-decision`
- `POST /api/controller/acknowledge-notification`
- `POST /api/controller/acknowledge-improvement-advisory`
- `POST /api/controller/respond-hitl`
- `POST /api/controller/record-human-decision`
- `POST /api/controller/finalize-review`
- `POST /api/controller/finalize-adversarial-review`
- `POST /api/controller/finalize-convergence-decision`
- `POST /api/controller/create-claim`
- `POST /api/controller/write-handoff`
- `POST /api/controller/execute-closeout`
- `POST /api/controller/daemon-start`
- `POST /api/controller/daemon-stop`

---

## Operator Workflow

1. Open the local operator console.
2. Inspect the overview summary for selected-task posture, queue load, notifications, AAS5 update pressure, and audit churn.
3. Use **Canonical Dispatchable Queue** to choose the next task to load.
4. Inspect **Task Runtime & Focus** before forcing policy changes or finalization decisions.
5. Use **Workflow Policy** to understand dispatch posture and next actions.
6. Resolve **HITL Queue** items directly from the dashboard.
7. Use the structured forms for review finalization, decisions, claims, handoffs, convergence, and closeout.
8. Watch **Audit Timeline** and **Event Stream** for recent controller behavior and drift.

---

## Current Limits

- the UI is still a local operator workbench, not a packaged desktop product
- it does not run direct model sessions itself
- controller-owned thread/turn/review startup was intentionally removed along with the retired App Server runtime
