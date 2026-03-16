# Provider Runtime Abstraction
**Scope:** AAS3 provider/backend runtime for multi-terminal execution
**Effective:** 2026-03-13

---

## Purpose

This document defines the AAS3 provider runtime layer that allows supported CLI backends to operate in parallel while sharing the same Atrahasis Agent System state.

The provider runtime does not replace:

- the single orchestration authority inside AAS3
- the repo-canonical artifact model
- the task-claim and handoff safety protocol

It adds:

- supported backend registration
- role-to-model routing policy
- active backend session state
- a code-backed task-claim helper

---

## Supported Backends

Current AAS3-supported backends:

- `codex`
- `gemini`

Not active in the current provider runtime:

- `claude`

Claude historical overlay files remain in the repo, but the current provider runtime and model-routing policy are built for Codex and Gemini only.

---

## Runtime State

Provider runtime state lives under:

- `runtime/state/provider_runtime/`

Key files:

- `registry.json`
- `sessions/codex/*.json`
- `sessions/gemini/*.json`

Task claims continue to live in:

- `docs/task_claims/`

Task-ID allocation policy lives in:

- `docs/TASK_ID_POLICY.md`

---

## Registration Scripts

Register a backend session:

```bash
python scripts/register_aas_backend.py <provider> <agent_name> <session_id> --agent-type <type>
```

Claim a task safely:

```bash
python scripts/claim_aas_task.py <task_id> "<title>" <platform> <agent_name>
```

Run AAS3 and register the backend in one step:

```bash
python scripts/run_aas5.py AASBT T-260 "..." --provider codex --agent-name Nergal --session-id abc123 --agent-type director
```

Run an ad hoc analysis/question/idea workflow and let AAS3 mint the task ID:

```bash
python scripts/run_aas5.py AASAQ "Explain the current provider runtime architecture and supported backends." --provider gemini --agent-name Enki --session-id gemini-session-001 --agent-type primary
```

---

## Routing Tiers

The provider runtime uses four routing tiers:

- `primary`
- `operational`
- `code_only`
- `fast_background`

Agent-role examples:

- `primary`: Director, Visionary, Systems Thinker, Critic, Science Advisor, Adversarial Analyst, Architecture Designer, Research Director
- `operational`: Chronicler, Prior Art Researcher, Landscape Analyst, Domain Translator, Simplification Agent
- `code_only`: Code Implementer, Schema Validator, Tooling Agent, Refactor Agent
- `fast_background`: low-risk background workers only

---

## Codex Routing

- `primary` -> `gpt-5.4` with `reasoning_effort = xhigh`
- `operational` -> `gpt-5.4`
- `code_only` -> `gpt-5.3-codex`
- `fast_background` -> `gpt-5.3-codex-spark`

---

## Gemini Routing

- `primary` -> `gemini-3.1-pro-preview`
- `operational` -> `gemini-3-flash-preview`
- `code_only` -> `gemini-3-flash-preview`
- `fast_background` -> `gemini-2.5-flash-lite`

---

## Collaboration Rule

Multiple terminals may run at the same time only if they obey:

1. provider registration
2. task claiming
3. safe-zone isolation
4. handoff-based shared-state integration when parallel execution is active

The provider runtime is therefore an execution registry and routing layer, not a bypass around the parallel execution protocol.
