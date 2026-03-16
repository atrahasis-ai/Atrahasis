# Claude Model Routing Policy
**Platform:** Claude Code (Anthropic)
**Applies to:** AAS Master Prompt §2.6 model routing
**Effective:** 2026-03-11

---

## Model Assignments

### Primary (invention-quality work)
**Model:** `claude-opus-4-6`
**Roles:** Director, Visionary, Systems Thinker, Critic, Science Advisor, Adversarial Analyst, Pre-Mortem Analyst, Synthesis Engineer, Assessment Council (Advocate, Skeptic, Arbiter), Specification Writer, Architecture Designer

### Operational (routine work)
**Model:** `claude-sonnet-4-6`
**Roles:** Chronicler, Prior Art Researcher, Landscape Analyst, Domain Translator, Simplification Agent, Commercial Viability Assessor
**Usage:** Also acceptable as fallback for primary roles when context window pressure requires it, or when the user explicitly requests faster execution.

### Code-Only
**Model:** `claude-sonnet-4-6`
**Roles:** Schema validators, script execution, tooling
**Note:** Claude does not have a separate code-only model. Sonnet handles both operational and code tasks.

## Override Rule
User direction overrides default routing. Absent explicit instruction, the above policy is binding.

## Mapping to §2.6 Tier System
| Master Prompt Tier | Claude Model |
|--------------------|-------------|
| PRIMARY | `claude-opus-4-6` |
| OPERATIONAL | `claude-sonnet-4-6` |
| CODE-ONLY | `claude-sonnet-4-6` |
