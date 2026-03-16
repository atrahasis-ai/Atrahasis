# AAS Controller App
**Platform:** OpenAI Codex
**Purpose:** Provide a small operator-facing control surface over the existing
AAS pipeline and task state

---

## What It Is

The controller app is:
- a small local CLI
- built on top of the existing `InventionPipelineManager`
- paired with the same read/control-plane surface used by the MCP server
- extended with HITL persistence, workflow policy, redesign-memory retrieval, audit timeline, daemon management, and background monitoring

Entry point:

```bash
python scripts/aas_controller.py
```

---

## Core Commands

### Run AAS

```bash
python scripts/aas_controller.py run AASAQ "Explain the current provider runtime architecture."
```

### Show Task Status

```bash
python scripts/aas_controller.py status T-9002
```

### Render The Current Human Review Prompt

```bash
python scripts/aas_controller.py prompt T-9002
```

### Show Dispatchable Tasks

```bash
python scripts/aas_controller.py dispatchable
```

### Dispatch A Child Team

```bash
python scripts/aas_controller.py dispatch T-9002 --spawn-id spawn:model --execute
```

### Inspect Controller State

```bash
python scripts/aas_controller.py run-state T-9002
python scripts/aas_controller.py workflow-policy T-9002
python scripts/aas_controller.py audit-timeline T-9002
python scripts/aas_controller.py dashboard-summary
python scripts/aas_controller.py notifications
python scripts/aas_controller.py improvement-advisories --refresh --high-confidence-only
```

The controller run state also carries a distilled `redesign_memory` snapshot:
- the current task's latest redesign/improvement cycle, if one exists
- related prior redesign cycles from other tasks with overlapping architectural pressure

The controller also maintains a repo-wide `AAS5` improvement-observer index:
- it watches structured controller state instead of scraping raw terminal text
- it only emits major system-improvement advisories
- it is advisory only and never mutates canonical Atrahasis artifacts by itself

You can acknowledge one advisory without clearing it from the historical record:

```bash
python scripts/aas_controller.py acknowledge-improvement-advisory aas5-update-controller-reliability
```

### Workflow Policy, HITL, And Closeout

```bash
python scripts/aas_controller.py hitl-queue --task-id T-9002
python scripts/aas_controller.py evaluate-workflow-policy T-9002
python scripts/aas_controller.py configure-workflow-policy T-9002 --dispatch-mode hook_only
python scripts/aas_controller.py recover-state
python scripts/aas_controller.py monitor-cycle --task-id T-9002
python scripts/aas_controller.py execute-closeout T-9002 --review-json "{...}" --human-decision-json "{...}"
```

### Convergence And Finalization

```bash
python scripts/aas_controller.py start-convergence-decision T-9002 --note "Need parent disposition."
python scripts/aas_controller.py finalize-review T-9002 REVIEW_APPROVED "Looks good."
python scripts/aas_controller.py finalize-adversarial-review T-9002 REVIEW_APPROVED "Risk checked."
python scripts/aas_controller.py finalize-convergence-decision T-9002 hybridize "Blend Alpha and Beta."
```

### Serve The Local Operator UI

```bash
python scripts/aas_controller.py serve --open
```

### Start Or Install The Operator Stack

```bash
pwsh -File scripts/start_aas5_operator_stack.ps1 -Open
pwsh -File scripts/start_aas5_operator_stack.ps1 -Daemon -Open
pwsh -File scripts/install_aas5_operator_stack.ps1
```

The install script writes repo-local launcher wrappers under `runtime/launchers/`.

### Run The Local Controller Regression Suite

```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Run The Controller Validation Harness

```bash
python scripts/validate_controller_flows.py offline --task-id T-9002
```

Use `--service-url http://127.0.0.1:4180` to target an already-running controller service.

---

## Relationship To MCP

- The controller app is for the operator.
- The MCP server is for Codex tool access.
- Both use the same underlying control-plane reads and narrow writes so they stay aligned.

---

## Runtime Posture

The old controller-owned Codex App Server runtime was retired from AAS5.

That means:
- the controller no longer starts local App Server subprocesses
- the controller no longer owns thread, turn, or review-session startup
- the local operator UI is now a policy/state/finalization surface rather than a session runtime surface

Direct model execution now lives in provider sessions and task-local workflows, not inside the controller app.

See `docs/platform_overlays/codex/OPERATOR_UI.md`.
