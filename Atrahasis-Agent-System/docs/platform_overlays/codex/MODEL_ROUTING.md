# Codex Model Routing Policy
**Platform:** OpenAI Codex
**Applies to:** AAS3 provider runtime
**Effective:** 2026-03-13

---

## Available Models

- `gpt-5.4`
- `gpt-5.3-codex`
- `gpt-5.3-codex-spark`
- `gpt-5.2-codex`
- `gpt-5.2`
- `gpt-5.1-codex-max`
- `gpt-5.1-codex-mini`

## Model Assignments

### Primary
**Model:** `gpt-5.4`
**Reasoning:** `xhigh`
**Roles:** Director, Master Orchestrator, Lane Manager, Lane Convergence Reporter, Auditor, Visionary, Systems Thinker, Critic, Science Advisor, Adversarial Analyst, Pre-Mortem Analyst, Synthesis Engineer, Assessment Council, Architecture Designer, Research Director

### Operational
**Model:** `gpt-5.4`
**Roles:** all non-peak roles that still require strong reasoning

### Code-Only
**Model:** `gpt-5.3-codex`
**Roles:** code-heavy execution, tooling, validators, refactors, automation

### Fast Background
**Model:** `gpt-5.3-codex-spark`
**Roles:** low-risk background acceleration only

## Fallbacks

- Primary fallback: `gpt-5.2`
- Code-only fallback: `gpt-5.2-codex`
- Low-cost emergency fallback: `gpt-5.1-codex-mini`

## Override Rule
User direction overrides default routing. Absent explicit instruction, the above policy is binding.

## Auditability Rule

Planned routing and actual runtime model are not the same thing.

Rules:
- if the runtime exposes the actual live model, record it explicitly
- if the runtime does not expose the actual live model, record the policy target and mark auditability as degraded rather than pretending the runtime model is proven
- for swarm artifacts, distinguish:
  - planned policy target
  - actual runtime model when known
  - degraded `runtime_not_exposed` cases

## AAS5 Ordinary Ideation Defaults

For ordinary `FULL PIPELINE / IDEATION` under AAS5:
- Master Orchestrator, lane managers, lane convergence reporters, and auditors target `gpt-5.4` with `xhigh`
- branch workers target `gpt-5.4` with `high`
- the lower-bound degraded fallback is `gpt-5.2`
- weaker-than-lower-bound observed models are blocking, not advisory
