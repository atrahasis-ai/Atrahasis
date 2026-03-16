# Gemini Model Routing Policy
**Platform:** Gemini CLI
**Applies to:** AAS3 provider runtime
**Effective:** 2026-03-13

---

## Model Assignments

### Primary
**Model:** `gemini-3.1-pro-preview`
**Roles:** Director, Visionary, Systems Thinker, Critic, Science Advisor, Adversarial Analyst, Pre-Mortem Analyst, Synthesis Engineer, Assessment Council, Architecture Designer, Research Director

### Operational
**Model:** `gemini-3-flash-preview`
**Roles:** Chronicler, Prior Art Researcher, Landscape Analyst, Domain Translator, Simplification Agent, Commercial Viability Assessor

### Code-Only
**Model:** `gemini-3-flash-preview`
**Roles:** implementation, validation, tooling, schema work
**Note:** Gemini currently uses the same operational path for code-heavy execution in AAS3.

### Fast Background
**Model:** `gemini-2.5-flash-lite`
**Roles:** low-risk background fan-out only

## Fallbacks

- Primary fallback: `gemini-2.5-pro`
- Operational fallback: `gemini-2.5-flash`

## Override Rule
User direction overrides default routing. Absent explicit instruction, the above policy is binding.
