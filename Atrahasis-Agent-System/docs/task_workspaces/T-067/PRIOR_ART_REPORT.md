# C37 — Epistemic Feedback Fabric (EFF): Prior Art Research Report

**Researcher:** Prior Art Researcher, Atrahasis Agent System
**Date:** 2026-03-12
**Invention:** C37 — Epistemic Feedback Fabric (EFF)
**Agent:** Enki (Claude Code)

---

## Executive Summary

The EFF occupies a novel intersection: privacy-preserving aggregation of post-hoc verification outcomes into population-level reasoning quality signals, delivered as advisory-only (non-binding) information to sovereign, heterogeneous AI agents. No single prior art reference covers this full combination. However, several references overlap with individual EFF components. The strongest overlap comes from (1) Governance-as-a-Service (GaaS), which shares the "external-to-agent-internals" philosophy but enforces rather than advises; (2) Token-Budget-Aware LLM Reasoning, which addresses reasoning budget allocation but at the individual model level; and (3) Subjective Logic / federated trust aggregation, which addresses privacy-preserving opinion fusion but without the verification-feedback-to-advisory-signal pipeline.

**Overall patent risk assessment: LOW-MEDIUM.** No single reference anticipates EFF's core claims. The primary novelty — a formally guaranteed advisory membrane separating population-level verification feedback from agent behavioral enforcement — appears to have no close prior art.

---

## 1. Patents

### 1.1 US20220067109A1 / US12292937B2 — Cognitive Automation Platform (Aera Technology)

**What it does:** A cognitive operating system that crawls enterprise data, identifies root causes, and prescribes actions. Includes a "cognitive data layer" that processes metrics, trends, and metadata to generate recommendations and predictions.

**Overlap with EFF:** Generates recommendations/prescriptions for autonomous action. Advisory signals based on aggregated data analysis.

**Novelty gap:** Aera's system is enterprise-centric (supply chain/business), not multi-agent AI reasoning. It prescribes actions (coercive), not advisory-only signals. No verification feedback loop. No privacy-preserving aggregation. No sovereignty guarantee or advisory membrane.

**Patent risk: LOW.**

### 1.2 US20120204026A1 — Privacy-Preserving Aggregation of Time-Series Data

**What it does:** Private Stream Aggregation (PSA) allowing encrypted data upload to an untrusted aggregator. Aggregator decrypts only aggregate statistics. Guarantees distributed differential privacy.

**Overlap with EFF:** Privacy-preserving aggregation of individual data into population-level statistics — directly analogous to EFF's VFL anonymization of per-agent verification outcomes.

**Novelty gap:** PSA is a generic cryptographic primitive for time-series data. It does not address: verification trust documents, claim-class reasoning quality metrics, reasoning strategy catalogs, budget advisory signals, or any agent-specific feedback loop. EFF uses differential privacy as one mechanism within a larger verification-to-advisory pipeline.

**Patent risk: LOW.** PSA is prior art for the privacy-preserving aggregation technique itself, but EFF's claims are at a higher architectural level.

### 1.3 US12140915 — Generative AI and Agentic AI for Industrial Systems (Rockwell/etc.)

**What it does:** Agentic AI for industrial equipment analytics, control, and optimization.

**Overlap with EFF:** Multi-agent system with feedback loops for optimization.

**Novelty gap:** Industrial control domain. Agents are controlled, not sovereign. No advisory membrane, no reasoning quality signals, no verification feedback loop.

**Patent risk: NEGLIGIBLE.**

---

## 2. Academic Papers

### 2.1 Token-Budget-Aware LLM Reasoning — TALE (ACL 2025 Findings)

**Reference:** Han et al., "Token-Budget-Aware LLM Reasoning," arXiv:2412.18547, ACL 2025.

**What it does:** Dynamically adjusts reasoning token budgets based on problem complexity. Reduces token costs by 67% while maintaining performance.

**Overlap with EFF:** Directly relevant to EFF's CABS (Budget Advisory Signals).

**Novelty gap:** TALE operates at the individual model level (self-budgeting via prompting). EFF's CABS operates at the population level (advisory signals derived from aggregate verification outcomes attached to inference leases). TALE is prescriptive; CABS is advisory. TALE has no verification feedback loop.

**Patent risk: MEDIUM.** EFF's CABS claims must be carefully distinguished as population-derived, verification-outcome-based, advisory-only, and attached to inference leases.

### 2.2 BudgetThinker (arXiv:2508.17196, August 2025)

**What it does:** Inserts control tokens during inference to inform the model of remaining token budget. Uses SFT + curriculum-based RL with length-aware reward.

**Novelty gap:** Same gaps as TALE — single-model, self-contained, no population-level feedback, no verification loop, no advisory membrane.

**Patent risk: LOW-MEDIUM.**

### 2.3 SOFAI-LM: Metacognitive Architecture (arXiv:2508.17959, 2025)

**What it does:** A metacognitive module monitors solver performance and dynamically selects the best solver. Provides iterative feedback with relevant examples. No fine-tuning required.

**Novelty gap:** Single-system architecture. EFF operates at population level across sovereign agents. SOFAI-LM's feedback is prescriptive (selects solver); EFF's is advisory. No privacy-preserving aggregation.

**Patent risk: MEDIUM.** Establishes metacognitive feedback for reasoning quality as prior art. EFF's population-level, privacy-preserving, advisory-only signals remain novel.

### 2.4 MUSE: Metacognitive Self-Assessment for RL Agents (arXiv:2411.13537)

**What it does:** Equips model-based RL agents with metacognitive self-assessment and self-regulation.

**Novelty gap:** Individual agent metacognition, not population-level. No external feedback fabric.

**Patent risk: LOW.**

### 2.5 Governance-as-a-Service (GaaS) (arXiv:2508.18765, August 2025)

**Reference:** "Governance-as-a-Service: A Multi-Agent Framework for AI System Compliance and Policy Enforcement."

**What it does:** A modular, policy-driven enforcement layer that regulates agent outputs at runtime without altering model internals. Uses declarative rules and a Trust Factor scoring mechanism. Model-agnostic.

**Overlap with EFF:** This is the closest prior art found. Key overlaps: external to agent internals, multi-agent system with heterogeneous agents, trust-based scoring, runtime operation, model-agnostic.

**Novelty gap (CRITICAL):** GaaS is an **enforcement** system — it blocks, redirects, penalizes. EFF is an **advisory** system. GaaS constrains outputs; EFF informs reasoning. GaaS has no verification feedback loop, no reasoning strategy catalog, no budget advisory signals. Most importantly, GaaS has no advisory membrane — its entire purpose is enforcement.

**Patent risk: MEDIUM.** GaaS is strong prior art for "external governance of multi-agent AI systems." The advisory membrane claim is the key differentiator.

### 2.6 Emergent Coordination in Multi-Agent LLMs (arXiv:2510.05174)

**What it does:** Uses information-theoretic framework to measure dynamical emergence in multi-agent LLM systems.

**Novelty gap:** Analytical framework, not operational feedback system.

**Patent risk: LOW.**

### 2.7 MAS-ProVe: Process Verification of Multi-Agent Systems (arXiv:2602.03053)

**What it does:** Systematically studies process verification across three verification paradigms in multi-agent LLM systems.

**Novelty gap:** Verification methodology paper, not feedback system. Verifies reasoning but does not aggregate outcomes into advisory signals.

**Patent risk: LOW-MEDIUM.**

### 2.8 Federated Reasoning LLMs Survey (2025)

**What it does:** Surveys federated approaches to LLM reasoning including federated prompt learning, adapter learning, and knowledge distillation.

**Novelty gap:** Federated learning modifies model parameters — inherently prescriptive. EFF preserves sovereignty and does not modify internals. FL uses gradients, not verification outcomes.

**Patent risk: LOW-MEDIUM.**

---

## 3. Products and Projects

### 3.1 Google A2A (Agent-to-Agent Protocol)
Communication/discovery protocol, not feedback system. **Patent risk: LOW.**

### 3.2 Anthropic MCP (Model Context Protocol)
Standardized tool/data interface, not reasoning feedback. **Patent risk: NEGLIGIBLE.**

### 3.3 LangGraph / LangSmith (LangChain)
Developer observability, not agent-facing advisory signals. **Patent risk: LOW.**

### 3.4 AutoGen (Microsoft)
Peer-to-peer critique in conversations, not population-level signals. **Patent risk: LOW.**

### 3.5 MASC: Metacognitive Self-Correction for MAS (arXiv:2510.14319)
Self-correction (prescriptive/enforcement), not advisory-only. **Patent risk: LOW-MEDIUM.**

---

## 4. Composite Novelty Analysis

### What EFF does that NO prior art does:

1. **Verification-to-Advisory Pipeline:** Aggregating post-hoc VTDs into per-claim-class reasoning quality metrics, then delivering as advisory-only signals. No reference combines verification outcomes with advisory feedback this way.

2. **Advisory Membrane:** Formal guarantee that feedback signals cannot be used for behavioral enforcement. GaaS does the opposite. No reference provides a formal non-enforcement guarantee.

3. **Reasoning Strategy Catalog (RSC):** Publishing proven reasoning patterns as knowledge quanta derived from verification outcomes. Existing catalogs are human-curated and static. RSC is dynamically generated from population data.

4. **Budget Advisory from Verification Outcomes:** TALE/BudgetThinker operate at individual model level using complexity estimation. CABS derives from population-level verification outcomes attached to inference leases.

5. **The Full Stack Together:** No single reference or combination covers VFL + RSC + CABS + Advisory Membrane.

### Potential blocking combinations:

GaaS + FL + TALE + Subjective Logic = closest combination. Still lacks advisory membrane, verification-to-reasoning pipeline, and RSC. Examiner would need 4+ references with significant modification — weak obviousness argument.

---

## 5. Recommendations for Patent Claims

1. **Lead claim:** Advisory Membrane (strongest differentiator, no close prior art)
2. **VFL claim:** Verification-trust-document-to-claim-class-quality-metric pipeline
3. **CABS claims:** Population-derived, verification-outcome-based, advisory-only, attached to inference leases
4. **RSC claims:** Dynamic generation from verification data
5. **Cite as background:** PSA, Subjective Logic, TALE, GaaS, FL surveys
