# T-067 PRE-IDEATION: Quick Scan — Known Solutions
**Role:** Prior Art Researcher
**Date:** 2026-03-12
**Agent:** Enki (Claude Code)

---

## Problem Statement

Atrahasis has no specification for cognitive control or meta-cognition. The system verifies agent reasoning outputs (C5 R-class claims) but does not guide, allocate, or improve reasoning processes. Agents are treated as black boxes. The question is whether this gap should be filled — and if so, how — without violating agent sovereignty (C32 MIA) or the post-hoc verification model (C5 PCVM).

## 7 Known Solutions / Approaches

### 1. Reflection Agent Pattern (LangChain / LangGraph)
- **What:** Dual-component architecture: executor + reflector. After each action, a reflection module critiques the output and feeds corrections back before final delivery.
- **Scope:** Per-task self-correction within a single agent.
- **Limitation:** Requires tight coupling between executor and reflector. No multi-agent governance. No sovereignty model.
- **Relevance to Atrahasis:** Low architectural fit — assumes control over agent internals.

### 2. Token-Budget-Aware LLM Reasoning (ACL 2025)
- **What:** Dynamically allocates reasoning token budgets based on problem complexity. Reduces token costs by ~67% while maintaining accuracy.
- **Key variants:** TALE (complexity estimation), BudgetThinker (control tokens), SelfBudgeter (autonomous prediction), Plan-and-Budget (sub-question decomposition with per-step budgets).
- **Limitation:** Operates at the inference call level. Assumes single-model control.
- **Relevance to Atrahasis:** HIGH — C23 SCR already meters inference leases. Budget-aware reasoning could integrate as a reasoning allocation strategy within the lease framework.

### 3. Metagent-P (ACL Findings 2025)
- **What:** Planning-verification-execution-reflection framework combining symbolic reasoning with LLM world knowledge. Neuro-symbolic planning agent.
- **Limitation:** Assumes a single agent with a planning module. Not designed for sovereign multi-agent systems.
- **Relevance to Atrahasis:** Medium — the planning-verification loop is analogous to C7 RIF → C5 PCVM, but Metagent-P adds explicit reflection as a fourth stage.

### 4. Meta-Cognitive Architecture for Governable Autonomy (arXiv 2602.11897)
- **What:** Embeds "meta-cognitive judgement" — the capacity to decide whether, when, and under what authority an action should be executed. Evaluates legitimacy, proportionality, and autonomy before execution.
- **Scope:** Cybersecurity domain, but architecturally general.
- **Limitation:** Governance-focused, not reasoning-quality-focused.
- **Relevance to Atrahasis:** HIGH — directly addresses the sovereignty tension. Meta-cognitive oversight as architectural function rather than external constraint. Compatible with C14 governance model.

### 5. TRAP Framework (Transparency, Reasoning, Adaptation, Perception)
- **What:** Four-component metacognitive framework. Transparency = explainability. Reasoning = logical inference. Adaptation = learning from feedback. Perception = environmental awareness.
- **Limitation:** Taxonomy, not architecture. No concrete specification.
- **Relevance to Atrahasis:** Low as direct prior art, but useful as a conceptual map.

### 6. Constitutional AI / Self-Critique (Anthropic)
- **What:** Models trained to critique their own outputs against a set of principles. Feedback loop improves alignment and safety.
- **Limitation:** Operates at training time, not inference time. Requires model fine-tuning.
- **Relevance to Atrahasis:** LOW for direct use (Atrahasis doesn't train models), but the principle of "critique against constitution" is analogous to C5 verification against claim requirements.

### 7. AgentOS / Cognitive Memory Hierarchy
- **What:** Treats the LLM as a "Reasoning Kernel" with a Semantic Memory Management Unit and Cognitive Memory Hierarchy. Context window managed as addressable semantic space.
- **Limitation:** Single-agent framework. Assumes control over agent runtime.
- **Relevance to Atrahasis:** Medium — C23 SCR already provides execution isolation. The cognitive memory hierarchy could map to C6 EMA's epistemic metabolism, but adding an active reasoning guidance layer on top.

## Key Insight

No existing solution addresses the specific Atrahasis constraint set:
1. Agents are **sovereign** (C32 MIA — cannot prescribe internals)
2. Trust is **post-hoc verification** (C5 PCVM — verify outputs, don't control inputs)
3. Scale is **1,000-100,000 agents** (individualized guidance infeasible)
4. Agents are **heterogeneous** (different models, capabilities, providers)

The gap is real but the solution space is heavily constrained by Atrahasis's own architectural commitments. Any meta-cognition layer must be **advisory, not prescriptive** — it can offer signals, not commands.
