# Atrahasis Agent System

The Atrahasis Agent System currently runs on the AAS3 architecture. It is a human-guided invention intelligence platform for the Atrahasis repository. It analyzes the repository as a research corpus, detects opportunity zones, generates invention hypotheses, evaluates solution paths, and produces structured artifacts for operator review.

## System Model

- `InventionPipelineManager` is the single workflow controller.
- `CommandModifierRouter` normalizes requests but does not control execution.
- Knowledge, reasoning, evaluation, and human-guidance modules run only through the orchestration layer.
- Historical invention logs, prior art, and specifications remain available as evidence and portfolio memory.

## Command Modifiers

- `AASBT`: implementation and buildout tasks
- `AASAQ`: architecture questions
- `AASNI`: new idea integration
- `AASA`: full system analysis

## Task ID Policy

- Canonical backlog work uses `T-001` to `T-7999`
- Ad hoc `AASA`, `AASAQ`, and `AASNI` runs use `T-9000` to `T-9499`
- Runtime/provider validation uses `T-9500` to `T-9799`
- Demo/operator walkthroughs use `T-9800` to `T-9999`

The runtime now auto-mints task IDs for `AASA`, `AASAQ`, and `AASNI` when no task ID is supplied. `AASBT` still requires an explicit canonical task ID. See `docs/TASK_ID_POLICY.md`.

## Quick Start

### CLI-First AAS5 Evaluation

If the goal is to test whether Codex performs better with the new Atrahasis Agent System than with the previous setup, use the terminal-first path and ignore the controller UI for now.

Start Codex in the repo with the AAS5 repo-local configuration:

```powershell
pwsh -File scripts/start_aas5_codex.ps1
```

Useful variants:

```powershell
pwsh -File scripts/start_aas5_codex.ps1 -Alpha
pwsh -File scripts/start_aas5_codex.ps1 -Search
pwsh -File scripts/start_aas5_codex.ps1 -CodeMode
pwsh -File scripts/start_aas5_codex.ps1 -MultiAgent
```

This keeps the workflow close to your normal Codex CLI usage:
- same terminal conversation model
- repo-local MCP enabled from `.codex/config.toml`
- repo-canonical docs and runtime state available in the working directory

For direct A/B testing guidance, see `docs/platform_overlays/codex/CLI_FIRST_TESTING.md`.

Register a backend session:

```bash
python scripts/register_aas_backend.py codex Nergal session-001 --agent-type director
```

Run an AAS task:

```bash
python scripts/run_aas1.py AASBT T-260 "Design the native server framework, decorator model, schema validation, auto-wrapping, provenance generation, and FastAPI/Express/Actix adapters." --constraint "Keep human approval mandatory"
```

Run an ad hoc architecture question and let AAS3 mint the task ID:

```bash
python scripts/run_aas1.py AASAQ "Explain the current provider runtime architecture and supported backends."
```

Run a validation-band task explicitly:

```bash
python scripts/run_aas1.py AASAQ "Validate provider runtime registration flow." --task-class validation
```

Validate state and workspace artifacts:

```bash
python scripts/validate_agent_state.py docs/AGENT_STATE.md
python scripts/validate_aas1_task_workspace.py docs/task_workspaces/T-901
```

Validate one artifact:

```bash
python scripts/validate_aas1_artifact.py hypothesis_packet docs/task_workspaces/T-901/HYPOTHESIS_PACKET.json
```

## Repository Structure

```text
docs/
  ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md
  ATRAHASIS_SYSTEM_OVERVIEW_v1.md
  AGENT_STATE.md
  HITL_POLICY.md
  RESEARCH_PROTOCOL.md
  SYNTHESIS_PLAYBOOK.md
  schemas/
  templates/
  task_workspaces/
src/aas1/
  invention_pipeline_manager.py
  command_modifier_router.py
  gcml_memory_interface.py
  artifact_registry.py
  telemetry.py
  discovery/
  reasoning/
  validation/
scripts/
  run_aas1.py
  register_aas_backend.py
  claim_aas_task.py
  validate_agent_state.py
  validate_aas1_artifact.py
  validate_aas1_task_workspace.py
```

## Human Guidance Rule

The operator remains the final decision authority. The Atrahasis Agent System generates evidence, hypotheses, contradictions, solution paths, and decision packets. It does not self-authorize pivots or commitments.
