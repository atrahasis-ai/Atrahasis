# ASV: Epistemic Accountability for AI Agent Communication

## Master Technical Specification -- C4-A

## Version 2.0.1

---

## Abstract

ASV (AASL Semantic Vocabulary) is a JSON Schema vocabulary and companion JSON-LD context that provides epistemic accountability for AI agent communication. It defines seven typed semantic structures -- Agent (AGT), Claim (CLM), Confidence (CNF), Evidence (EVD), Provenance (PRV), Verification (VRF), and Speech-Act Envelope (SAE) -- that compose into an auditable epistemic chain: every claim an agent makes can carry structured confidence with calibration metadata, linked evidence with quality classification, traceable provenance extending W3C PROV-O, and independent verification records aligned with W3C Verifiable Credentials. ASV is a vocabulary, not a protocol. It embeds inside Google A2A messages, Anthropic MCP tool responses, or standalone JSON documents for persistence and audit. It competes with no transport layer and requires no custom parser. ASV's genuinely novel contributions are narrow and specific: a claim classification taxonomy for epistemic assertion types (observation, correlation, causation, inference, prediction, prescription), a dual classification framework combining speech-act type with epistemic claim type, and the structured confidence primitive (CNF) with declared methods and calibration metadata -- for which no existing standard exists. All other components extend or apply established W3C standards. ASV targets regulated industries where audit trails, provenance, and verified claims are compliance requirements, with a 12-18 month window before W3C community groups or A2A extensions address the semantic gap organically. This specification is self-contained: it defines every type, provides complete JSON Schema definitions, documents integration patterns, and includes test vectors sufficient for implementation.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [The Epistemic Accountability Chain](#2-the-epistemic-accountability-chain)
3. [ASV Type System](#3-asv-type-system)
4. [Claim Classification](#4-claim-classification)
5. [Integration](#5-integration)
6. [JSON-LD Context](#6-json-ld-context)
7. [Confidence Calibration](#7-confidence-calibration)
8. [Rebuttals and Temporal Validity](#8-rebuttals-and-temporal-validity)
9. [Security Analysis](#9-security-analysis)
10. [Validation Plan](#10-validation-plan)
11. [Adoption Strategy](#11-adoption-strategy)
12. [Risk Assessment](#12-risk-assessment)
13. [Implementation Roadmap](#13-implementation-roadmap)
14. [Conclusion](#14-conclusion)
15. [Appendices](#appendices)

---

## 1. Introduction

### 1.1 The Problem: Accountability in AI Communication

When AI agents communicate with each other, they exchange assertions about the world. A research agent reports a statistical finding. A diagnostic agent proposes a treatment. A financial agent recommends a trade. In every case, the receiving agent -- or the human overseeing the system -- faces the same questions: How confident is this claim? What evidence supports it? Where did it come from? Has anyone independently verified it?

Today, these questions go unanswered. The dominant agent communication protocols -- Google A2A and Anthropic MCP -- solve the transport problem brilliantly. A2A handles agent-to-agent coordination with task lifecycle management, capability discovery, and message exchange. MCP handles agent-to-tool connectivity with structured tool definitions, resource access, and sampling. Both use JSON-RPC over standard transports. Both have achieved industry convergence under the Linux Foundation's Agentic AI Foundation (AAIF), backed by every major AI provider. The protocol wars are over.

But neither protocol addresses what agents are saying semantically. An A2A message can carry any JSON payload. An MCP tool can return any structured content. Neither provides native support for typed claims, structured confidence, evidence linking, provenance chains, or verification records. The semantic layer between application logic and transport protocols is undefined.

This absence has consequences. In a multi-agent pipeline, confidence degrades through a telephone game: Agent A reports "fairly confident," Agent B interprets this as 0.8, Agent C relays "reasonably confident," and by Agent D the original 0.92 statistical confidence has dissolved into vague uncertainty. In regulated industries -- financial services, healthcare, government -- the absence of structured provenance means audit trails are reconstructed manually from logs, if they exist at all. When an AI system makes a consequential decision, tracing the reasoning chain from claim through evidence to source data requires forensic engineering rather than structured query.

The problem is not that agents cannot communicate. They communicate fluently. The problem is that no one can hold them accountable for what they say.

### 1.2 From AASL to ASV

ASV descends from AASL (Atrahasis Agent Specification Language), a comprehensive declarative language for representing agents, tasks, tools, workflows, and semantic relationships. AASL was the right idea with the wrong delivery mechanism.

AASL's core insight was genuine and important: agent communications should be governed semantic objects, not transient text. Every claim should carry provenance. Every assertion should declare confidence. Every piece of evidence should be typed and traceable. AASL built an elaborate system to deliver this vision -- a custom syntax (`AGT{id:ag.r1 role:research}`), a seven-layer processing pipeline (Source through Governance), a custom parser, and over 18,000 lines of specification.

The Ideation Council's analysis was unanimous on one point: the custom syntax was a strategic liability. LLMs cannot produce or consume AASL natively. There is no tooling, no training data, no developer familiarity. The compactness gains over JSON are marginal. The ecosystem costs are enormous. JSON has won -- every production agent framework uses it, and LLMs generate valid JSON at greater than 95% accuracy with constrained decoding.

ASV extracts what was genuinely valuable from AASL -- the epistemic type system, the CLM-CNF-EVD-PRV-VRF accountability chain, the claim classification taxonomy, the confidence primitive -- and delivers it as a JSON Schema vocabulary that plugs into the protocols that have already won. The custom syntax is gone. The custom parser is gone. The seven-layer pipeline is gone. What remains is the semantic core: a set of typed JSON structures that make agent communication epistemically accountable.

### 1.3 The Landscape

The AI agent communication landscape consolidated rapidly between 2024 and early 2026:

| Date | Event |
|------|-------|
| November 2024 | Anthropic launches MCP |
| April 2025 | Google launches A2A |
| May 2025 | W3C AI Agent Protocol Community Group formed |
| June 2025 | A2A donated to Linux Foundation |
| August 2025 | IBM ACP merges into A2A (5 months after launch) |
| November 2025 | W3C Semantic Agent Communication CG proposed |
| December 2025 | MCP donated to AAIF; AAIF formed with all major AI providers |
| February 2026 | NIST AI Agent Standards Initiative launched |

Two lessons emerge. First, the protocol layer is settled. MCP handles agent-to-tool connectivity (97M+ monthly SDK downloads). A2A handles agent-to-agent collaboration (100+ enterprise partners). Attempting to compete with either is futile -- IBM ACP tried and was absorbed in five months. Second, the semantic layer is open. No existing protocol provides first-class claim objects, typed confidence distributions, provenance chain primitives, evidence quality classification, or claim classification taxonomies. The W3C community groups are forming but have not converged. The window for establishing a reference vocabulary is approximately 12-18 months.

ASV positions itself in this gap: not as a protocol competing with A2A or MCP, but as a vocabulary layer that rides on top of both.

```
                +---------------------------------+
                |    Application / Agent Logic     |
                +---------------+-----------------+
                                |
                +---------------v-----------------+
                |    ASV Semantic Vocabulary        |
                |    (CLM, CNF, EVD, PRV, VRF)     |
                |    JSON Schema + JSON-LD context  |
                +---------------+-----------------+
                                |
          +---------------------+---------------------+
          |                     |                      |
+---------v--------+  +--------v-------+  +-----------v------+
|  A2A Messages     |  | MCP Tool       |  | Standalone       |
|  (agent-agent)    |  | Responses      |  | Persistence      |
|  JSON-RPC/HTTP    |  | JSON-RPC       |  | JSON documents   |
+------------------+  +----------------+  +------------------+
```

### 1.4 Design Principles

ASV is governed by three non-negotiable principles derived from the Assessment Council deliberation:

**1. Vocabulary, not protocol.** ASV defines JSON Schema types and a JSON-LD context. It defines no transport, no connection management, no message routing, no task lifecycle. Those responsibilities belong to A2A and MCP. ASV occupies the semantic layer between application logic (above) and transport protocols (below).

**2. Code before spec.** The first deliverable is a working Python/TypeScript validator library with integration examples, not a specification document. The schema is the test suite. The semantic specification follows implementation, not the reverse. This directly addresses the FIPA/KQML failure mode of death-by-specification: FIPA ACL had formal semantics, 20+ performatives, interoperability specifications, and zero adoption because the ecosystem had no incentive to use it.

**3. Narrow invention claim.** ASV claims novelty only for: (a) the claim classification taxonomy for epistemic assertion types, (b) dual classification combining speech-act type with epistemic claim type, and (c) the structured confidence primitive (CNF) with declared methods and calibration metadata. All other components -- provenance extending W3C PROV, verification aligned with W3C VC, JSON Schema delivery, JSON-LD context -- are acknowledged as applications of existing standards, not inventions.

### 1.5 What ASV Is Not

**ASV is not a protocol.** It defines no transport, no connection management, no authentication, no message ordering, no delivery guarantees. Those are A2A's and MCP's concerns.

**ASV is not a replacement for A2A or MCP.** It is a vocabulary that embeds inside their messages. An A2A message without ASV is a valid A2A message. An MCP response without ASV is a valid MCP response. ASV adds epistemic metadata; it does not change how messages travel.

**ASV is not a complete agent framework.** It does not orchestrate agents, manage task lifecycles, handle capability discovery, or coordinate workflows. Frameworks like AutoGen, CrewAI, and LangGraph handle orchestration. ASV handles what those frameworks currently lack: structured accountability for the claims agents make.

**ASV is not paradigm-shifting.** Its novelty score is 3/5 -- moderate. The integration is new and valuable, but ASV builds on well-established foundations (W3C PROV, W3C VC, JSON Schema, speech-act theory) rather than introducing fundamentally new concepts. Two of its eleven components are genuinely novel. The rest are competent applications of existing standards. This is an honest assessment, not false modesty.

---

## 2. The Epistemic Accountability Chain

### 2.1 Why a Chain?

Consider what happens when an AI agent makes a claim: "Drug A and Drug B interact to increase bleeding risk by 2.3x." This is not a simple assertion. To evaluate it responsibly, a downstream consumer needs answers to five linked questions:

1. **What exactly is being claimed?** Not just the content, but the epistemic nature -- is this a direct observation, a statistical correlation, a causal assertion, or a prediction? The appropriate verification strategy depends on the answer.

2. **How confident is the agent?** Not "fairly confident" (which means different things to different models) but a structured assessment: confidence 0.89 via statistical analysis of 12,450 samples, calibrated against the FDA adverse events database with a Brier score of 0.07.

3. **What evidence supports the claim?** A Cochrane meta-analysis of 14 RCTs (direct observation) and an FDA adverse event database query (computational result). The quality class of each evidence item determines how much weight it carries.

4. **How was the claim generated?** The agent aggregated evidence from two sources using a DerSimonian-Laird random effects model, starting at 09:00 and completing at 11:30 on February 15. This provenance record enables audit and replication.

5. **Has anyone independently verified it?** A pharmacology reviewer cross-referenced against UpToDate, FDA prescribing information, and three independent databases, confirming the finding with confidence 0.96.

These five questions are not independent. Confidence without evidence is assertion. Evidence without provenance is untraceable. Provenance without verification is unvalidated. Verification without a structured claim is unfocused. The chain CLM-CNF-EVD-PRV-VRF exists because the questions are inherently linked, and the answers must compose into a single, auditable record.

### 2.2 Chain Structure

The epistemic accountability chain has five links, anchored by the Claim:

```
CLM (Claim) -- the root assertion
  |-- CNF (Confidence) -- how confident is the claim?
  |-- EVD[] (Evidence) -- what supports the claim?
  |-- PRV (Provenance) -- how was the claim generated?
  |-- VRF (Verification) -- has the claim been independently validated?
  |-- rebuts_claims[] -- what other claims does this dispute?
  |-- valid_from / valid_until -- when is this claim temporally valid?
```

**CLM (Claim)** is a proposition asserted by an agent, classified by its epistemic nature (observation, correlation, causation, inference, prediction, prescription). CLM maps to `prov:Entity` in the W3C PROV ontology. It is the root of every chain.

**CNF (Confidence)** is ASV's core novel primitive. It represents structured confidence as a point estimate, interval, or discrete distribution, with a declared method (statistical, consensus, model_derived, human_judged, heuristic) and calibration metadata distinguishing empirically validated confidence from raw model output.

**EVD (Evidence)** links claims to supporting data with evidence quality typing. Five quality classes -- direct_observation, inference, computational_result, delegation, hearsay -- enable downstream agents to weight evidence appropriately. EVD maps to `prov:Entity` linked via `asv:supportedBy`.

**PRV (Provenance)** records the origin and derivation history of a claim. It extends W3C PROV-O by mapping to `prov:Activity` with `wasGeneratedBy` and `used` relations, supporting delegation chains via `prov:actedOnBehalfOf`.

**VRF (Verification)** captures the result of independent validation. It maps to a `prov:Activity` of type `asv:VerificationActivity`, aligned with W3C VC Data Integrity for cryptographic proof when needed.

### 2.3 Complete Chain Example

The following example demonstrates a full epistemic chain -- a clinical analyst's claim about drug interaction risk, with all five links populated:

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:drug-interaction-001",
  "content": "Co-administration of Drug A (warfarin) and Drug B (aspirin) increases bleeding risk by 2.3x (95% CI: 1.8-2.9) compared to warfarin monotherapy.",
  "epistemic_class": "causation",
  "agent_id": "urn:asv:agent:clinical-analyst-01",
  "subject": "warfarin_aspirin_coadministration",
  "object": "bleeding_risk",
  "confidence": {
    "type": "CNF",
    "id": "urn:asv:confidence:drug-001-cnf",
    "value": 0.89,
    "interval": [0.84, 0.93],
    "method": "statistical",
    "sample_size": 12450,
    "calibration": {
      "status": "calibrated",
      "dataset_id": "urn:asv:dataset:fda-adverse-events-2025",
      "calibration_date": "2025-09-01T00:00:00Z",
      "metric": "brier_score",
      "metric_value": 0.07
    }
  },
  "evidence": [
    {
      "type": "EVD",
      "id": "urn:asv:evidence:rct-meta-analysis-001",
      "quality_class": "direct_observation",
      "source_type": "document",
      "source_id": "urn:asv:document:cochrane-review-2024-0892",
      "description": "Cochrane systematic review and meta-analysis of 14 RCTs examining warfarin-aspirin co-administration.",
      "retrieved_at": "2026-01-15T08:00:00Z",
      "agent_id": "urn:asv:agent:clinical-analyst-01"
    },
    {
      "type": "EVD",
      "id": "urn:asv:evidence:faers-query-001",
      "quality_class": "computational_result",
      "source_type": "dataset",
      "source_id": "urn:asv:dataset:fda-faers-2025-q4",
      "description": "Query of FDA Adverse Event Reporting System for warfarin+aspirin adverse events, Q4 2025.",
      "retrieved_at": "2026-02-01T10:00:00Z",
      "agent_id": "urn:asv:agent:data-collector-03"
    }
  ],
  "provenance": {
    "type": "PRV",
    "id": "urn:asv:provenance:drug-analysis-001",
    "agent_id": "urn:asv:agent:clinical-analyst-01",
    "activity_type": "aggregation",
    "started_at": "2026-02-15T09:00:00Z",
    "ended_at": "2026-02-15T11:30:00Z",
    "used": [
      "urn:asv:document:cochrane-review-2024-0892",
      "urn:asv:dataset:fda-faers-2025-q4"
    ],
    "method": "Systematic evidence synthesis: meta-analytic random effects model (DerSimonian-Laird) applied to RCT data, corroborated with FAERS signal detection."
  },
  "verification": {
    "type": "VRF",
    "id": "urn:asv:verification:drug-review-001",
    "claim_id": "urn:asv:claim:drug-interaction-001",
    "verifier_id": "urn:asv:agent:pharmacology-reviewer-01",
    "status": "verified",
    "method": "cross_reference",
    "verified_at": "2026-02-20T14:00:00Z",
    "details": "Cross-referenced with UpToDate clinical database, FDA prescribing information, and 3 independent pharmacology databases. All sources consistent with claimed risk ratio.",
    "confidence_in_verification": {
      "type": "CNF",
      "id": "urn:asv:confidence:drug-vrf-cnf",
      "value": 0.96,
      "method": "consensus",
      "sample_size": 4,
      "calibration": {
        "status": "calibrated",
        "metric": "brier_score",
        "metric_value": 0.03,
        "calibration_date": "2026-01-01T00:00:00Z"
      }
    }
  },
  "valid_from": "2026-02-20T14:00:00Z",
  "valid_until": "2027-02-20T14:00:00Z",
  "created_at": "2026-02-15T11:30:00Z"
}
```

This single JSON object answers all five accountability questions. It can be validated against the ASV schema, embedded in an A2A message or MCP response, persisted as a standalone `.asv.json` document, and queried by audit systems. Every field is typed, every reference is a URI, and the calibration metadata distinguishes this from a raw model guess.

---

## 3. ASV Type System

ASV defines seven core types. Every ASV object MUST include a `type` discriminator field and an `id` field. The `type` field determines which schema applies.

### 3.1 Agent (AGT)

An Agent is an entity that bears responsibility for claims, actions, and activities within the epistemic chain. AGT maps to `prov:Agent` in the W3C PROV ontology.

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/agt.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Agent",
  "description": "An entity that bears responsibility for epistemic activities. Maps to prov:Agent.",
  "type": "object",
  "required": ["type", "id", "name"],
  "properties": {
    "type": { "const": "AGT" },
    "id": { "type": "string", "format": "uri" },
    "name": { "type": "string", "minLength": 1 },
    "role": { "type": "string" },
    "model": { "type": "string" },
    "capabilities": {
      "type": "array",
      "items": { "type": "string" }
    },
    "asv_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    }
  },
  "additionalProperties": false
}
```

**Example:**

```json
{
  "type": "AGT",
  "id": "urn:asv:agent:research-01",
  "name": "Research Agent Alpha",
  "role": "researcher",
  "model": "claude-opus-4-6",
  "capabilities": ["literature_search", "statistical_analysis"],
  "asv_version": "1.0.0"
}
```

An AGT represents the entity responsible for generating or verifying claims. The `model` field identifies the AI model but does not imply any specific capability guarantee. When used within a PRV record, the AGT is referenced by its `id` via the `agent_id` field.

### 3.2 Claim (CLM)

A Claim is a proposition asserted by an agent, classified by both its speech-act context and its epistemic nature. CLM maps to a specialized `prov:Entity`.

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/clm.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Claim",
  "description": "A knowledge assertion with epistemic classification. Maps to prov:Entity.",
  "type": "object",
  "required": ["type", "id", "content", "epistemic_class", "agent_id"],
  "properties": {
    "type": { "const": "CLM" },
    "id": { "type": "string", "format": "uri" },
    "content": { "type": "string", "minLength": 1 },
    "epistemic_class": {
      "type": "string",
      "enum": ["observation", "correlation", "causation", "inference", "prediction", "prescription"]
    },
    "agent_id": { "type": "string", "format": "uri" },
    "confidence": { "$ref": "https://asv.atrahasis.dev/vocab/v1/cnf.schema.json" },
    "evidence": {
      "type": "array",
      "items": { "$ref": "https://asv.atrahasis.dev/vocab/v1/evd.schema.json" }
    },
    "provenance": { "$ref": "https://asv.atrahasis.dev/vocab/v1/prv.schema.json" },
    "verification": { "$ref": "https://asv.atrahasis.dev/vocab/v1/vrf.schema.json" },
    "rebuts_claims": {
      "type": "array",
      "items": { "type": "string", "format": "uri" }
    },
    "valid_from": { "type": "string", "format": "date-time" },
    "valid_until": { "type": "string", "format": "date-time" },
    "subject": { "type": "string" },
    "object": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": false
}
```

The CLM is the root of every epistemic chain. The `epistemic_class` field classifies the nature of the knowledge assertion -- this is one of ASV's genuinely novel contributions, as no existing agent communication system distinguishes between an agent asserting a correlation versus a causal relationship versus a prediction. The six classes are defined in Section 4.

**Example (minimal):**

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:simple-001",
  "content": "The Python package 'requests' version 2.31.0 has no known critical CVEs as of March 2026.",
  "epistemic_class": "observation",
  "agent_id": "urn:asv:agent:security-scanner-01"
}
```

### 3.3 Confidence (CNF) -- The Core Innovation

Confidence is the most novel primitive in ASV. No existing standard addresses structured confidence for agent reasoning. W3C VC Confidence Methods operates in the identity/credential domain, not agent claims. Adding a bare `confidence: 0.87` field to a JSON message is trivial; what is not trivial is defining what that number means, how it was produced, and whether it has been empirically validated.

CNF supports three representation modes:

**1. Point estimate.** A single value in [0, 1]. The simplest mode.

**2. Interval.** A lower and upper bound. When both `value` and `interval` are present, `value` MUST fall within the interval.

**3. Distribution.** A discrete probability distribution over named outcomes. Probabilities SHOULD sum to 1.0 (within tolerance of 0.001).

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/cnf.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Confidence",
  "description": "Structured confidence with method declaration and calibration metadata.",
  "type": "object",
  "required": ["type", "id", "method"],
  "properties": {
    "type": { "const": "CNF" },
    "id": { "type": "string", "format": "uri" },
    "value": { "type": "number", "minimum": 0, "maximum": 1 },
    "interval": {
      "type": "array",
      "items": { "type": "number", "minimum": 0, "maximum": 1 },
      "minItems": 2,
      "maxItems": 2
    },
    "distribution": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["outcome", "probability"],
        "properties": {
          "outcome": { "type": "string" },
          "probability": { "type": "number", "minimum": 0, "maximum": 1 }
        },
        "additionalProperties": false
      }
    },
    "method": {
      "type": "string",
      "enum": ["statistical", "consensus", "model_derived", "human_judged", "heuristic"]
    },
    "sample_size": { "type": "integer", "minimum": 0 },
    "calibration": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["calibrated", "uncalibrated", "self_reported"]
        },
        "dataset_id": { "type": "string", "format": "uri" },
        "calibration_date": { "type": "string", "format": "date-time" },
        "metric": { "type": "string" },
        "metric_value": { "type": "number" }
      },
      "additionalProperties": false
    }
  },
  "anyOf": [
    { "required": ["value"] },
    { "required": ["interval"] },
    { "required": ["distribution"] }
  ],
  "additionalProperties": false
}
```

**Five confidence methods:**

| Method | Meaning |
|--------|---------|
| `statistical` | Frequentist analysis with stated significance; the confidence value reflects a computed statistic (p-value, correlation coefficient, etc.). |
| `consensus` | Agreement among N agents or sources; `sample_size` indicates the number of agreeing parties. |
| `model_derived` | Raw output from an AI model's probability estimation. Often poorly calibrated. |
| `human_judged` | Assessment by a human expert. |
| `heuristic` | Rule-based or heuristic estimation without formal statistical grounding. |

**Example (distribution mode):**

```json
{
  "type": "CNF",
  "id": "urn:asv:confidence:diagnosis-003",
  "method": "consensus",
  "distribution": [
    { "outcome": "bacterial_infection", "probability": 0.65 },
    { "outcome": "viral_infection", "probability": 0.25 },
    { "outcome": "other", "probability": 0.10 }
  ],
  "sample_size": 3,
  "calibration": { "status": "self_reported" }
}
```

### 3.4 Evidence (EVD)

Evidence links claims to supporting data with quality classification. EVD maps to `prov:Entity` linked via `asv:supportedBy` (a subproperty of `prov:wasDerivedFrom`).

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/evd.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Evidence",
  "description": "Evidence supporting a claim, with quality classification. Maps to prov:Entity.",
  "type": "object",
  "required": ["type", "id", "quality_class", "source_type"],
  "properties": {
    "type": { "const": "EVD" },
    "id": { "type": "string", "format": "uri" },
    "quality_class": {
      "type": "string",
      "enum": ["direct_observation", "inference", "hearsay", "computational_result", "delegation"]
    },
    "source_type": {
      "type": "string",
      "enum": ["dataset", "document", "api", "agent_output", "sensor", "human_input", "other"]
    },
    "source_id": { "type": "string", "format": "uri" },
    "description": { "type": "string" },
    "content": {
      "oneOf": [
        { "type": "string" },
        { "type": "object" },
        { "type": "array" }
      ]
    },
    "retrieved_at": { "type": "string", "format": "date-time" },
    "agent_id": { "type": "string", "format": "uri" }
  },
  "additionalProperties": false
}
```

**Five quality classes:**

| Class | Description | Epistemic Weight |
|-------|-------------|-----------------|
| `direct_observation` | First-hand measurement or sensory data from a sensor, instrument, or direct API call. | Highest |
| `inference` | Conclusion derived by the agent through reasoning over other evidence. | High |
| `computational_result` | Output of a deterministic computation, simulation, or model execution. | High |
| `delegation` | Evidence obtained from another agent's claim. Provenance chain SHOULD be traceable. | Medium |
| `hearsay` | Unverified report from an indirect source. | Lowest |

The quality class vocabulary is namespace-extensible. Implementations MAY define additional quality classes under their own namespace.

### 3.5 Provenance (PRV)

Provenance records the origin and derivation history of a claim. PRV extends W3C PROV-O rather than replacing it, following the PROV-AGENT (Souza et al., 2025) precedent.

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/prv.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Provenance",
  "description": "Origin and derivation history of a claim. Extends prov:Activity.",
  "type": "object",
  "required": ["type", "id", "agent_id", "activity_type"],
  "properties": {
    "type": { "const": "PRV" },
    "id": { "type": "string", "format": "uri" },
    "agent_id": { "type": "string", "format": "uri" },
    "activity_type": {
      "type": "string",
      "enum": ["generation", "derivation", "aggregation", "transformation", "delegation", "verification"]
    },
    "started_at": { "type": "string", "format": "date-time" },
    "ended_at": { "type": "string", "format": "date-time" },
    "used": {
      "type": "array",
      "items": { "type": "string", "format": "uri" }
    },
    "was_informed_by": {
      "type": "array",
      "items": { "type": "string", "format": "uri" }
    },
    "delegated_from": { "type": "string", "format": "uri" },
    "method": { "type": "string" },
    "tool_id": { "type": "string", "format": "uri" }
  },
  "additionalProperties": false
}
```

**W3C PROV-O mapping:**

| ASV Field | PROV-O Property |
|-----------|----------------|
| PRV object | `prov:Activity` |
| `agent_id` | `prov:wasAssociatedWith` |
| `started_at` | `prov:startedAtTime` |
| `ended_at` | `prov:endedAtTime` |
| `used` | `prov:used` |
| `was_informed_by` | `prov:wasInformedBy` |
| `delegated_from` | `prov:actedOnBehalfOf` |
| Generated CLM | `prov:wasGeneratedBy` (inverse) |

This mapping enables interoperability with existing PROV tooling (provtoolbox, the prov Python library, Neo4j PROV plugins) without modification.

### 3.6 Verification (VRF)

A Verification record captures the result of independent validation of a claim. VRF maps to a `prov:Activity` of type `asv:VerificationActivity`, aligned with W3C Verifiable Credentials Data Integrity for cryptographic proof when needed.

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/vrf.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Verification",
  "description": "Independent verification record for a claim.",
  "type": "object",
  "required": ["type", "id", "claim_id", "verifier_id", "status", "method"],
  "properties": {
    "type": { "const": "VRF" },
    "id": { "type": "string", "format": "uri" },
    "claim_id": { "type": "string", "format": "uri" },
    "verifier_id": { "type": "string", "format": "uri" },
    "status": {
      "type": "string",
      "enum": ["verified", "disputed", "inconclusive", "pending"]
    },
    "method": {
      "type": "string",
      "enum": ["replication", "cross_reference", "formal_proof", "consensus", "cryptographic", "human_review"]
    },
    "verified_at": { "type": "string", "format": "date-time" },
    "details": { "type": "string" },
    "proof": {
      "type": "object",
      "properties": {
        "proof_type": { "type": "string" },
        "created": { "type": "string", "format": "date-time" },
        "verification_method": { "type": "string", "format": "uri" },
        "proof_value": { "type": "string" }
      },
      "additionalProperties": true
    },
    "confidence_in_verification": {
      "$ref": "https://asv.atrahasis.dev/vocab/v1/cnf.schema.json"
    }
  },
  "additionalProperties": false
}
```

The `proof` object is optional and follows the W3C VC Data Integrity structure for cryptographic verification when required. Most agent-to-agent verification uses non-cryptographic methods (replication, cross-reference, consensus).

### 3.7 Speech-Act Envelope (SAE)

The Speech-Act Envelope wraps ASV epistemic content in a performative that declares communicative intent. The SAE uses commitment semantics (Singh) rather than mentalistic BDI semantics -- a deliberate choice for LLM-based agents where "belief" attribution is problematic.

**Six performatives:**

| Performative | Illocutionary Force | Commitment Created | uACP Mapping |
|-------------|--------------------|--------------------|-------------|
| `INFORM` | Assert a proposition | Sender commits that claim content is believed true | TELL |
| `REQUEST` | Ask for action | Sender commits to processing the result | ASK |
| `PROPOSE` | Suggest a course of action | No commitment until accepted | TELL (commitment=provisional) |
| `CONFIRM` | Verify or acknowledge | Sender commits to agreement with referenced claim | TELL (with verification payload) |
| `WARN` | Flag a risk or constraint | Sender commits that risk is non-trivial | TELL (priority=elevated) |
| `QUERY` | Request information | Sender commits to processing the answer | ASK |

The 6-performative set is a pragmatic superset of uACP's proven 4-verb basis {PING, TELL, ASK, OBSERVE}. The uACP completeness proof (January 2026) demonstrates that 4 verbs suffice for all finite-state FIPA protocols. PROPOSE and WARN are convenience extensions that do not extend expressive power but improve routing clarity.

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/sae.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Speech-Act Envelope",
  "description": "Wraps epistemic content in a performative declaring communicative intent.",
  "type": "object",
  "required": ["type", "id", "performative", "sender_id", "payload"],
  "properties": {
    "type": { "const": "SAE" },
    "id": { "type": "string", "format": "uri" },
    "performative": {
      "type": "string",
      "enum": ["INFORM", "REQUEST", "PROPOSE", "CONFIRM", "WARN", "QUERY"]
    },
    "sender_id": { "type": "string", "format": "uri" },
    "recipient_id": { "type": "string", "format": "uri" },
    "in_reply_to": { "type": "string", "format": "uri" },
    "conversation_id": { "type": "string", "format": "uri" },
    "payload": {
      "oneOf": [
        { "$ref": "https://asv.atrahasis.dev/vocab/v1/clm.schema.json" },
        {
          "type": "array",
          "items": { "$ref": "https://asv.atrahasis.dev/vocab/v1/clm.schema.json" }
        },
        { "type": "object" }
      ]
    },
    "priority": {
      "type": "string",
      "enum": ["normal", "elevated", "critical"],
      "default": "normal"
    },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": false
}
```

**Example (WARN with prediction):**

```json
{
  "type": "SAE",
  "id": "urn:asv:sae:warn-001",
  "performative": "WARN",
  "sender_id": "urn:asv:agent:monitor-01",
  "priority": "elevated",
  "payload": {
    "type": "CLM",
    "id": "urn:asv:claim:calibration-drift-001",
    "content": "Agent research-01's confidence calibration has drifted. ECE increased from 0.06 to 0.18 over the last 30 days.",
    "epistemic_class": "observation",
    "agent_id": "urn:asv:agent:monitor-01",
    "confidence": {
      "type": "CNF",
      "id": "urn:asv:confidence:wd001",
      "value": 0.88,
      "method": "statistical",
      "calibration": {
        "status": "calibrated",
        "metric": "ece",
        "metric_value": 0.03,
        "calibration_date": "2026-03-01T00:00:00Z"
      }
    }
  },
  "created_at": "2026-03-09T12:00:00Z"
}
```

---

## 4. Claim Classification

### 4.1 Speech-Act Classification

ASV classifies every communication by its speech-act type -- what communicative act is being performed. The six performatives are drawn from three decades of multi-agent system research:

- **INFORM**: "I am telling you something I believe to be true." The sender commits to the truth of the claim.
- **REQUEST**: "I am asking you to do something." The sender commits to processing the result.
- **PROPOSE**: "I am suggesting we consider this." No commitment until the recipient accepts.
- **CONFIRM**: "I agree with / have verified this." The sender commits to agreement.
- **WARN**: "I am flagging a risk you should know about." The sender commits that the risk is non-trivial.
- **QUERY**: "I am asking for information." The sender commits to processing the answer.

### 4.2 Epistemic Classification

ASV classifies every claim by its epistemic nature -- what kind of knowledge assertion is being made. This classification determines how the claim should be verified:

| Class | Definition | Verification Approach |
|-------|-----------|----------------------|
| `observation` | Directly witnessed or measured fact. | Compare against source data. |
| `correlation` | Statistical association between variables. | Replicate analysis on same or different data. |
| `causation` | Asserted causal relationship. | Experimental or counterfactual validation. |
| `inference` | Conclusion derived from reasoning over evidence. | Verify premises and reasoning chain. |
| `prediction` | Forward-looking assertion about future states. | Evaluate against outcomes when available. |
| `prescription` | Normative recommendation about what should be done. | Assess against stated criteria or policy. |

### 4.3 The Dual Classification Matrix

ASV's genuinely novel contribution is classifying every message along two orthogonal dimensions simultaneously. This produces a 6x6 matrix of 36 possible combinations. Not all are equally common, but all are structurally valid.

|            | observation | correlation | causation | inference | prediction | prescription |
|------------|:-----------:|:-----------:|:---------:|:---------:|:----------:|:------------:|
| **INFORM** | Common      | Common      | Common    | Common    | Rare       | Rare         |
| **REQUEST**| Rare        | Rare        | Rare      | Rare      | Rare       | Common       |
| **PROPOSE**| Rare        | Rare        | Rare      | Rare      | Rare       | Common       |
| **CONFIRM**| Common      | Common      | Common    | Common    | Rare       | Rare         |
| **WARN**   | Common      | Rare        | Rare      | Common    | Common     | Common       |
| **QUERY**  | Rare        | Rare        | Rare      | Rare      | Rare       | Common       |

The significance of dual classification is operational. Consider: "This is an INFORM speech act carrying a CAUSAL claim with confidence 0.87 based on statistical analysis of dataset X, verified by agents Y and Z." No existing agent communication system can represent both dimensions natively. FIPA ACL classifies the speech act but not the epistemic content. JSON-based protocols carry untyped payloads. ASV classifies both, enabling routing logic (causal claims require different verification than correlations), priority handling (predictions with low confidence warrant different treatment than high-confidence observations), and audit classification (regulators care about the epistemic nature of the claims driving automated decisions).

Implementations MUST NOT reject a message solely because its speech-act/epistemic combination is uncommon.

---

## 5. Integration

### 5.1 A2A Integration

ASV types embed in A2A as structured data Parts within A2A Messages, or as Artifacts attached to A2A Tasks. No modifications to the A2A protocol are required.

**A2A Agent Card extension for ASV support:**

```json
{
  "extensions": {
    "asv": {
      "version": "1.0.0",
      "supported_types": ["CLM", "CNF", "EVD", "PRV", "VRF", "AGT", "SAE"],
      "conformance_level": "standard"
    }
  }
}
```

**Complete A2A message with ASV content:**

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "message": {
      "role": "agent",
      "parts": [
        {
          "type": "application/asv+json",
          "content": {
            "type": "SAE",
            "id": "urn:asv:sae:a2a-inform-001",
            "performative": "INFORM",
            "sender_id": "urn:asv:agent:research-01",
            "recipient_id": "urn:asv:agent:coordinator-01",
            "payload": {
              "type": "CLM",
              "id": "urn:asv:claim:a2a-finding-001",
              "content": "Analysis complete. Found statistically significant correlation (r=0.87, p<0.001).",
              "epistemic_class": "correlation",
              "agent_id": "urn:asv:agent:research-01",
              "confidence": {
                "type": "CNF",
                "id": "urn:asv:confidence:a2a-001",
                "value": 0.87,
                "method": "statistical",
                "calibration": {
                  "status": "calibrated",
                  "metric": "brier_score",
                  "metric_value": 0.06,
                  "calibration_date": "2025-11-01T00:00:00Z"
                }
              },
              "evidence": [
                {
                  "type": "EVD",
                  "id": "urn:asv:evidence:a2a-dataset-001",
                  "quality_class": "direct_observation",
                  "source_type": "dataset",
                  "source_id": "urn:asv:dataset:experiment-results-445",
                  "description": "Experimental results from controlled trial.",
                  "retrieved_at": "2026-03-08T14:00:00Z"
                }
              ],
              "provenance": {
                "type": "PRV",
                "id": "urn:asv:provenance:a2a-analysis-001",
                "agent_id": "urn:asv:agent:research-01",
                "activity_type": "generation",
                "started_at": "2026-03-08T14:00:00Z",
                "ended_at": "2026-03-08T14:22:00Z",
                "used": ["urn:asv:dataset:experiment-results-445"],
                "method": "Pearson correlation with scipy.stats"
              }
            },
            "created_at": "2026-03-09T10:00:00Z"
          },
          "metadata": {
            "asv_version": "1.0.0",
            "schema_uri": "https://asv.atrahasis.dev/vocab/v1/sae.schema.json"
          }
        }
      ]
    }
  }
}
```

When an A2A Task completes, ASV objects attached as Artifacts become durable, identity-bearing semantic objects -- the "objects not outputs" principle in practice.

### 5.2 MCP Integration

ASV types embed as structured content in MCP Tool responses. An MCP server declaring ASV support returns epistemically accountable results.

**Complete MCP tool response with ASV content:**

```json
{
  "jsonrpc": "2.0",
  "id": "req-42",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Weather forecast retrieved successfully."
      },
      {
        "type": "asv",
        "asv_version": "1.0.0",
        "asv": {
          "type": "CLM",
          "id": "urn:asv:claim:weather-forecast-001",
          "content": "7-day forecast for San Francisco: High 62F, Low 48F, 30% chance of rain on day 3.",
          "epistemic_class": "prediction",
          "agent_id": "urn:asv:agent:weather-tool-01",
          "confidence": {
            "type": "CNF",
            "id": "urn:asv:confidence:weather-001",
            "value": 0.75,
            "interval": [0.65, 0.82],
            "method": "model_derived",
            "calibration": {
              "status": "calibrated",
              "dataset_id": "urn:asv:dataset:noaa-forecast-verification-2025",
              "calibration_date": "2026-01-15T00:00:00Z",
              "metric": "brier_score",
              "metric_value": 0.11
            }
          },
          "evidence": [
            {
              "type": "EVD",
              "id": "urn:asv:evidence:noaa-api-001",
              "quality_class": "computational_result",
              "source_type": "api",
              "source_id": "urn:asv:api:noaa/weather/forecast",
              "description": "NOAA Weather Forecast API, GFS model output.",
              "retrieved_at": "2026-03-09T06:00:00Z"
            }
          ],
          "valid_from": "2026-03-09T06:00:00Z",
          "valid_until": "2026-03-16T06:00:00Z",
          "created_at": "2026-03-09T06:01:00Z"
        }
      }
    ]
  }
}
```

### 5.3 Standalone Documents

ASV objects MAY be persisted as standalone JSON documents with the `.asv.json` file extension. This is the persistence surface for audit trails, compliance archives, and regulatory documentation.

**Document schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/document.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Document",
  "description": "A standalone ASV document containing one or more ASV objects.",
  "type": "object",
  "required": ["@context", "asv_version", "objects"],
  "properties": {
    "@context": { "const": "https://asv.atrahasis.dev/vocab/v1/context.jsonld" },
    "asv_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "document_id": { "type": "string", "format": "uri" },
    "created_at": { "type": "string", "format": "date-time" },
    "objects": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "id"],
        "properties": {
          "type": {
            "type": "string",
            "enum": ["AGT", "CLM", "CNF", "EVD", "PRV", "VRF", "SAE"]
          }
        }
      },
      "minItems": 1
    }
  }
}
```

**Example (audit trail document):**

```json
{
  "@context": "https://asv.atrahasis.dev/vocab/v1/context.jsonld",
  "asv_version": "1.0.0",
  "document_id": "urn:asv:document:audit-trail-2026-03-09",
  "created_at": "2026-03-09T18:00:00Z",
  "objects": [
    {
      "type": "AGT",
      "id": "urn:asv:agent:research-01",
      "name": "Research Agent Alpha",
      "role": "researcher",
      "model": "claude-opus-4-6",
      "asv_version": "1.0.0"
    },
    {
      "type": "CLM",
      "id": "urn:asv:claim:temp-co2-correlation-001",
      "content": "Global surface temperature anomaly shows r=0.92 correlation with atmospheric CO2.",
      "epistemic_class": "correlation",
      "agent_id": "urn:asv:agent:research-01",
      "confidence": {
        "type": "CNF",
        "id": "urn:asv:confidence:tc001",
        "value": 0.92,
        "method": "statistical",
        "calibration": {
          "status": "calibrated",
          "metric": "brier_score",
          "metric_value": 0.08,
          "calibration_date": "2025-12-01T00:00:00Z"
        }
      },
      "created_at": "2025-12-01T14:22:00Z"
    },
    {
      "type": "VRF",
      "id": "urn:asv:verification:peer-review-003",
      "claim_id": "urn:asv:claim:temp-co2-correlation-001",
      "verifier_id": "urn:asv:agent:verifier-02",
      "status": "verified",
      "method": "replication",
      "verified_at": "2025-12-05T09:15:00Z",
      "details": "Replication confirmed r=0.91."
    }
  ]
}
```

---

## 6. JSON-LD Context

The ASV JSON-LD context maps ASV terms to ontology URIs, enabling interoperability with semantic web tooling without requiring ASV consumers to understand JSON-LD. Plain JSON consumers ignore `@context`; the schemas validate independently.

**Namespace:** `https://asv.atrahasis.dev/vocab/v1#` (abbreviated `asv:`).

**Context definition:**

```json
{
  "@context": {
    "asv": "https://asv.atrahasis.dev/vocab/v1#",
    "prov": "http://www.w3.org/ns/prov#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "schema": "http://schema.org/",
    "sec": "https://w3id.org/security#",

    "AGT": "prov:Agent",
    "CLM": "prov:Entity",
    "CNF": "asv:Confidence",
    "EVD": "prov:Entity",
    "PRV": "prov:Activity",
    "VRF": "asv:VerificationActivity",
    "SAE": "asv:SpeechActEnvelope",

    "id": "@id",
    "type": "@type",

    "name": "schema:name",
    "content": "asv:content",
    "epistemic_class": "asv:epistemicClass",
    "agent_id": { "@id": "prov:wasAttributedTo", "@type": "@id" },

    "value": "asv:confidenceValue",
    "interval": "asv:confidenceInterval",
    "distribution": "asv:confidenceDistribution",
    "method": "asv:method",
    "sample_size": "asv:sampleSize",
    "calibration": "asv:calibration",

    "quality_class": "asv:qualityClass",
    "source_type": "asv:sourceType",
    "source_id": { "@id": "prov:wasDerivedFrom", "@type": "@id" },
    "description": "schema:description",
    "retrieved_at": { "@id": "asv:retrievedAt", "@type": "xsd:dateTime" },

    "activity_type": "asv:activityType",
    "started_at": { "@id": "prov:startedAtTime", "@type": "xsd:dateTime" },
    "ended_at": { "@id": "prov:endedAtTime", "@type": "xsd:dateTime" },
    "used": { "@id": "prov:used", "@type": "@id", "@container": "@set" },
    "was_informed_by": { "@id": "prov:wasInformedBy", "@type": "@id", "@container": "@set" },
    "delegated_from": { "@id": "prov:actedOnBehalfOf", "@type": "@id" },

    "claim_id": { "@id": "asv:verifies", "@type": "@id" },
    "verifier_id": { "@id": "prov:wasAssociatedWith", "@type": "@id" },
    "status": "asv:verificationStatus",
    "verified_at": { "@id": "asv:verifiedAt", "@type": "xsd:dateTime" },
    "proof": "sec:proof",

    "performative": "asv:performative",
    "sender_id": { "@id": "asv:sender", "@type": "@id" },
    "recipient_id": { "@id": "asv:recipient", "@type": "@id" },
    "in_reply_to": { "@id": "asv:inReplyTo", "@type": "@id" },
    "conversation_id": { "@id": "asv:conversationId", "@type": "@id" },
    "payload": "asv:payload",
    "priority": "asv:priority",

    "rebuts_claims": { "@id": "asv:rebuts", "@type": "@id", "@container": "@set" },
    "valid_from": { "@id": "prov:generatedAtTime", "@type": "xsd:dateTime" },
    "valid_until": { "@id": "prov:invalidatedAtTime", "@type": "xsd:dateTime" },
    "created_at": { "@id": "schema:dateCreated", "@type": "xsd:dateTime" },
    "subject": "asv:subject",
    "object": "asv:object"
  }
}
```

**Relationship to existing ontologies:**

| ASV Namespace | Maps To |
|---------------|---------|
| `asv:` | ASV-specific terms with no existing standard equivalent (CNF, epistemicClass, performative, qualityClass, etc.) |
| `prov:` | W3C PROV-O terms for provenance (Agent, Activity, Entity, used, wasGeneratedBy, etc.) |
| `schema:` | Schema.org terms for general metadata (name, description, dateCreated) |
| `sec:` | W3C Security Vocabulary for cryptographic proof |
| `xsd:` | XML Schema datatypes for date-time values |

### 6.1 Canonicalizer Service

The JSON-LD context gives ASV a shared semantic vocabulary, but it does not guarantee that two valid producers serialize equivalent ASV objects in the same byte order. Different field ordering, compacted term choices, and set-member ordering can all represent the same epistemic content. The canonicalizer service defines the deterministic normalization step required for deduplication, stable hashing, and cross-system comparison.

**Inputs.** The canonicalizer accepts either a single ASV object or a standalone ASV document that already passes JSON Schema validation. Inputs MAY omit `@context`; the service resolves comparisons against the canonical ASV context from this section regardless of how the source document was compacted.

**Canonicalization procedure:**

1. Validate the input against the relevant ASV schema. Invalid objects MUST be rejected; canonicalization is not a repair mechanism.
2. Resolve compacted terms against the canonical ASV `@context` so internal comparison operates on expanded semantics rather than producer-specific field spelling.
3. Normalize all object keys into deterministic lexicographic order.
4. Normalize URI-valued fields as canonical strings and remove presentation-only differences that do not change semantics.
5. For set-valued properties declared with `@container: @set` (`used`, `was_informed_by`, `rebuts_claims`), sort members deterministically and eliminate duplicates.
6. Preserve all semantically meaningful fields, including provenance, calibration metadata, proofs, and temporal bounds.
7. Emit `canonical_json`; implementations MAY additionally emit `canonical_hash` and `equivalence_key`.

**Output invariants.**

- `canonical_json` MUST round-trip to an ASV-valid object with the same meaning as the input.
- If a `canonical_hash` is emitted, it MUST be computed over the exact bytes of `canonical_json`.
- Two ASV objects that differ only in field ordering, context compaction, or set-member ordering MUST produce identical `canonical_json`.
- Objects that differ in claim content, epistemic class, provenance links, calibration status, temporal bounds, or verification outcomes MUST NOT collapse to the same canonical form.

**Non-goals.** The canonicalizer does not infer missing data, merge near-duplicates, or adjudicate whether two differently worded claims are substantively equivalent. It only removes representation variance for already valid ASV structures.

---

## 7. Confidence Calibration

Confidence calibration is the most dangerous technical assumption in ASV. LLMs are notoriously poorly calibrated -- they cannot reliably estimate their own confidence. If agents report confidence 0.92 when true accuracy is 0.65, structured confidence scores are worse than no confidence scores because they create false precision. ASV makes confidence first-class while honestly acknowledging that calibration is an active research problem, not a specification problem. The vocabulary cannot guarantee calibrated confidence, but it can require transparency about calibration status.

### 7.1 Calibration Levels

| Level | Requirements | Consumer Guidance |
|-------|-------------|-------------------|
| `calibrated` | Validated against a held-out dataset. `dataset_id`, `calibration_date`, `metric`, and `metric_value` MUST be present. | May be used for automated decision-making. |
| `uncalibrated` | Raw model output. No empirical validation. | SHOULD NOT be used for automated decisions without human review. |
| `self_reported` | Agent estimates its own accuracy. No external validation. | Treat as ordinal ranking, not calibrated probability. |

### 7.2 The Calibration Protocol

When `calibration.status` is `calibrated`, the following metadata is required:

- **`dataset_id`**: URI identifying the holdout dataset used for calibration.
- **`calibration_date`**: When calibration was last performed.
- **`metric`**: The calibration metric used (e.g., `brier_score`, `ece` for Expected Calibration Error, `reliability_diagram`).
- **`metric_value`**: The metric result. For ECE, values below 0.05 indicate well-calibrated confidence; values above 0.15 indicate poor calibration.

### 7.3 Drift Detection

Conforming implementations SHOULD monitor calibration drift by:

1. Tracking `metric_value` over time for each agent.
2. Flagging agents whose calibration metric degrades by more than 50% from their baseline.
3. When drift is detected, generating a WARN SAE alerting downstream consumers.

When `calibration_date` is more than 90 days old, consumers SHOULD treat the calibration as potentially stale.

### 7.4 Why This Matters

The calibration protocol does not solve the calibration problem -- that is an active ML research problem. What it does is make the calibration status explicit and machine-readable. A system receiving a confidence value of 0.92 with `"status": "uncalibrated"` knows to treat it differently than 0.92 with `"status": "calibrated", "metric": "brier_score", "metric_value": 0.04`. Without ASV, both look identical: a number in a JSON field with no context about how it was produced or whether it has any empirical validity.

---

## 8. Rebuttals and Temporal Validity

### 8.1 Rebuttal Claims

Rebuttals enable Toulmin-complete argumentation within the ASV framework. A rebuttal is not a separate type -- it is a CLM with a non-empty `rebuts_claims` array. This design ensures rebuttals carry the same epistemic accountability as primary claims: they must have their own confidence, evidence, provenance, and optionally verification.

**Identification rule:** A CLM object is a rebuttal if and only if its `rebuts_claims` array is non-empty.

**Example:**

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:rebuttal-spurious-correlation-001",
  "content": "The observed correlation between temperature and CO2 is confounded by the shared time trend. After detrending, the residual correlation drops to r=0.34, which is not statistically significant at p<0.05.",
  "epistemic_class": "inference",
  "agent_id": "urn:asv:agent:critic-01",
  "rebuts_claims": ["urn:asv:claim:temp-co2-correlation-001"],
  "confidence": {
    "type": "CNF",
    "id": "urn:asv:confidence:rebuttal-001-cnf",
    "value": 0.72,
    "interval": [0.60, 0.82],
    "method": "statistical",
    "sample_size": 64,
    "calibration": { "status": "uncalibrated" }
  },
  "evidence": [
    {
      "type": "EVD",
      "id": "urn:asv:evidence:detrended-analysis-001",
      "quality_class": "computational_result",
      "source_type": "agent_output",
      "source_id": "urn:asv:agent:critic-01",
      "description": "Detrended residual correlation analysis using Hodrick-Prescott filter.",
      "retrieved_at": "2025-12-10T11:00:00Z"
    }
  ],
  "created_at": "2025-12-10T11:30:00Z"
}
```

Rebuttals compose naturally with the epistemic chain. A rebuttal can itself be rebutted, creating an argumentation graph that preserves the full provenance and confidence of every position.

### 8.2 Temporal Validity

Claims carry optional `valid_from` and `valid_until` fields (RFC 3339 timestamps) following W3C PROV's temporal model.

**Rules:**

1. If `valid_from` is absent, the claim is valid from its `created_at` timestamp.
2. If `valid_until` is absent, the claim is considered indefinitely valid until explicitly invalidated.
3. If `valid_until` is in the past relative to the current time, the claim SHOULD be flagged for re-verification.
4. `valid_from` MUST be earlier than or equal to `valid_until` when both are present.
5. Temporal validity does not affect structural validity -- an expired claim is still a valid ASV object; it is semantically stale, not structurally invalid.

**Re-verification triggers:** Conforming implementations SHOULD implement at least one of periodic scanning for expired claims, event-driven notification on expiry, or query-time filtering that flags expired claims in result sets.

---

## 9. Security Analysis

ASV delegates transport security to A2A and MCP. It does not define authentication, authorization, encryption, or transport-layer security. Those are solved problems handled by the protocols ASV rides on (A2A uses JWS for Agent Card signing; MCP uses OAuth 2.0).

ASV's security concerns are at the semantic layer:

**Provenance integrity.** ASV provenance records are self-reported by agents. A malicious agent can fabricate provenance, claiming to have used a dataset it never accessed. Mitigation: the VRF type enables independent verification, and the `proof` object on VRF supports cryptographic attestation when needed. For high-stakes deployments, provenance claims SHOULD be independently verified.

**Confidence manipulation.** An agent can report artificially high confidence to influence downstream decisions. Mitigation: the calibration metadata makes this detectable -- an agent claiming confidence 0.95 with `"status": "uncalibrated"` is transparently unverified. Full conformance requires calibration drift monitoring.

**Evidence fabrication.** An agent can reference evidence that does not exist or mischaracterize evidence quality. Mitigation: referential integrity checks (Full conformance) validate that `source_id` references resolve to real resources. Evidence quality class declarations can be independently verified through VRF records.

**Trust delegation to transport.** ASV explicitly trusts that A2A and MCP correctly identify message senders. If the transport layer is compromised, ASV's `sender_id` and `agent_id` fields are unreliable. This is an accepted tradeoff: ASV is a vocabulary layer, not a security layer.

---

## 10. Validation Plan

### 10.1 Hard Gate Experiments

The Assessment Council specified three gate experiments that must pass before ASV advances:

**GATE-1: Working Implementation.** Ship a Python/TypeScript validator library that validates ASV-typed JSON messages with less than 10ms overhead per message at typical sizes (1-10KB), and integrate with at least one existing protocol (A2A or MCP) using existing extensibility mechanisms. Kill criterion: validation overhead exceeds 10ms, or integration requires protocol modifications.

**GATE-2: LLM Generation Accuracy.** Prompt Claude, GPT-4, and Gemini to generate 100 CLM-CNF-EVD-PRV-VRF chains each from natural language descriptions. Measure structural validity against ASV schemas. Kill criterion: structural validity below 80% across all three models, or below 70% for the full nested chain.

**GATE-3: Provenance Chain Utility.** Build a multi-agent fact-checking pipeline, inject deliberate errors, compare error detection rates with no provenance, simple source attribution, and full ASV provenance chain. Kill criterion: full ASV chain shows less than 20% improvement in error detection rate versus simple source attribution.

### 10.2 Conformance Levels

**Basic Conformance:**

1. MUST validate all ASV objects against JSON Schema definitions.
2. MUST correctly discriminate ASV types using the `type` field.
3. MUST accept and produce all seven ASV type values.
4. MUST validate that `id` fields are present and are valid URIs.
5. MUST validate required fields per each type's schema.

**Standard Conformance (Basic plus):**

1. MUST validate epistemic chain composition (CLM contains valid CNF, EVD, PRV objects).
2. MUST validate that `confidence.value` falls within `confidence.interval` when both are present.
3. MUST validate that `distribution` probabilities sum to 1.0 (within tolerance of 0.001).
4. MUST validate temporal validity constraints (`valid_from` <= `valid_until`).
5. SHOULD implement referential integrity checks.
6. SHOULD implement calibration status warnings for uncalibrated CNF objects.
7. SHOULD expose the Section 6.1 canonicalization procedure for ingestion-time deduplication of standalone ASV documents.

**Full Conformance (Standard plus):**

1. MUST implement referential integrity checks across all cross-references.
2. MUST implement temporal validity expiry detection and flagging.
3. MUST implement calibration drift monitoring.
4. MUST validate semantic contracts defined in the companion Semantic Specification.
5. MUST support all three integration formats (A2A, MCP, standalone document).
6. MUST implement commitment tracking for SAE performatives.
7. MUST implement the Section 6.1 canonicalization procedure before emitting canonical hashes or equivalence keys.
8. MUST treat field ordering and the ordering of `used`, `was_informed_by`, and `rebuts_claims` values as semantically irrelevant during equivalence comparison.

### 10.3 Test Vectors

**TV-1: Valid minimal CLM (Basic)**

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-001",
  "content": "Test claim.",
  "epistemic_class": "observation",
  "agent_id": "urn:asv:agent:test-01"
}
```

Expected: VALID.

**TV-2: Missing required field (Basic)**

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-002",
  "content": "Test claim."
}
```

Expected: INVALID (missing `epistemic_class` and `agent_id`).

**TV-3: Invalid epistemic class (Basic)**

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-003",
  "content": "Test claim.",
  "epistemic_class": "guess",
  "agent_id": "urn:asv:agent:test-01"
}
```

Expected: INVALID (`"guess"` is not a valid epistemic_class).

**TV-4: Confidence value outside interval (Standard)**

```json
{
  "type": "CNF",
  "id": "urn:asv:confidence:test-004",
  "value": 0.95,
  "interval": [0.80, 0.90],
  "method": "statistical"
}
```

Expected: INVALID (value 0.95 outside interval [0.80, 0.90]).

**TV-5: Distribution probabilities do not sum to 1 (Standard)**

```json
{
  "type": "CNF",
  "id": "urn:asv:confidence:test-005",
  "method": "consensus",
  "distribution": [
    { "outcome": "A", "probability": 0.5 },
    { "outcome": "B", "probability": 0.3 }
  ]
}
```

Expected: INVALID (probabilities sum to 0.8, not 1.0).

**TV-6: Temporal validity violation (Standard)**

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-006",
  "content": "Test claim.",
  "epistemic_class": "prediction",
  "agent_id": "urn:asv:agent:test-01",
  "valid_from": "2026-06-01T00:00:00Z",
  "valid_until": "2026-01-01T00:00:00Z"
}
```

Expected: INVALID (valid_from after valid_until).

**TV-7: Complete epistemic chain (Full)**

Input: The complete drug interaction example in Section 2.3. Expected: VALID at all conformance levels.

**TV-8: Canonical field-order equivalence (Full)**

Input A:

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-008",
  "content": "The reactor temperature exceeded 80 C.",
  "epistemic_class": "observation",
  "agent_id": "urn:asv:agent:test-01"
}
```

Input B:

```json
{
  "agent_id": "urn:asv:agent:test-01",
  "epistemic_class": "observation",
  "content": "The reactor temperature exceeded 80 C.",
  "id": "urn:asv:claim:test-008",
  "type": "CLM"
}
```

Expected: VALID. `canonical_json` for Input A and Input B is identical, and any emitted `canonical_hash` values are equal.

**TV-9: Canonical set-order equivalence (Full)**

Input A:

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-009",
  "content": "Earlier claim is contradicted by new data.",
  "epistemic_class": "inference",
  "agent_id": "urn:asv:agent:test-01",
  "rebuts_claims": [
    "urn:asv:claim:alpha",
    "urn:asv:claim:beta"
  ]
}
```

Input B:

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-009",
  "content": "Earlier claim is contradicted by new data.",
  "epistemic_class": "inference",
  "agent_id": "urn:asv:agent:test-01",
  "rebuts_claims": [
    "urn:asv:claim:beta",
    "urn:asv:claim:alpha",
    "urn:asv:claim:alpha"
  ]
}
```

Expected: VALID. The canonicalizer sorts `rebuts_claims`, removes duplicates, and produces identical `canonical_json` and `canonical_hash` outputs for both inputs.

---

## 11. Adoption Strategy

### 11.1 Regulated Industries First

ASV's adoption path is compliance necessity, not developer enthusiasm. The FIPA/KQML failure mode -- technically sound specification that no one adopted -- is directly relevant. ASV avoids it by targeting environments where structured epistemic accountability is not optional.

**Financial services.** Model risk management regulations require auditable decision trails for AI-driven decisions. ASV objects map directly to audit trail requirements: every loan approval, risk assessment, or trade recommendation carries structured provenance and evidence.

**Healthcare.** The FDA is developing AI/ML audit trail requirements for clinical decision support. ASV's evidence quality classification and confidence calibration metadata address specific regulatory needs for clinical AI transparency.

**Government.** The NIST AI Agent Standards Initiative (launched February 2026) is developing guidance for AI agent deployments in government contexts. ASV's vocabulary aligns with NIST's focus on traceability and accountability.

### 11.2 Open Source and Standards

The reference implementation (Python + TypeScript validators) is open source. The vocabulary is free to use. Commercial value accrues through enterprise tooling (validators, dashboards, audit trail analyzers), conformance certification services, and consulting for regulated industries.

### 11.3 W3C and AAIF Path

The W3C AI Agent Protocol Community Group (formed May 2025) and the Semantic Agent Communication Community Group (proposed November 2025) represent the natural standards path. ASV should contribute its vocabulary concepts to these groups within 12 months, positioning ASV as the reference vocabulary that standards bodies adopt rather than competing with their independent efforts. Contributing ASV to the Linux Foundation's AAIF governance would trade direct control for legitimacy and adoption -- the strongest defensive move against convergence risk.

### 11.4 FIPA Lessons Applied

| FIPA Failure Mode | ASV Mitigation |
|-------------------|---------------|
| Over-specification before implementation | Code-first: ship validators before full semantic spec |
| Dialect fragmentation | JSON Schema + vocabulary pinning prevents incompatible variants |
| Ignored dominant paradigms | ASV rides on A2A/MCP, does not compete with them |
| Excessive formalism | Pragmatic JSON vocabularies, not formal logics |
| No ecosystem incentive | Regulatory compliance provides concrete adoption driver |

---

## 12. Risk Assessment

### 12.1 Residual Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| **Convergence**: A2A/MCP evolve their own epistemic metadata | MEDIUM-HIGH | HIGH | Ship vocabulary within 6 months; position as complementary; contribute to AAIF |
| **Adoption inertia**: Developers ignore ASV because protocols do not require it | HIGH | MEDIUM | Zero-friction adoption (single `$ref` import); framework integration plugins |
| **Specification bloat**: Semantic spec exceeds 50-page cap | MEDIUM | MEDIUM | Automated conformance tests; scope reviews at 30 pages |
| **LLM generation quality**: LLMs produce structurally valid but semantically incorrect ASV | MEDIUM | MEDIUM | Two-step generation pattern; application-layer semantic validators |
| **Confidence calibration gap**: Agents report miscalibrated confidence | HIGH | MEDIUM | Mandatory calibration metadata; consumer warnings for uncalibrated CNF |

### 12.2 Monitoring Flags

| Flag | Severity | Trigger | Action |
|------|----------|---------|--------|
| A2A Convergence | RED | A2A adds structured confidence or verification as first-class message properties | Halt vocabulary development; pivot to semantic specification for A2A epistemic metadata |
| LLM Generation Failure | RED | GATE-2 structural validity below 70% for full chain | Simplify vocabulary; decompose chain into independently usable components |
| Provenance Utility Failure | RED | GATE-3 error detection improvement below 20% versus simple attribution | Halt full pipeline; extract claim classification as standalone contribution |
| Specification Bloat | AMBER | Semantic spec exceeds 30 pages before Phase 2 delivery | Initiate scope review |
| Adoption Inertia | AMBER | Zero external downloads within 6 months of publication | Contribute directly to W3C CG or AAIF |
| Calibration Gap | AMBER | LLM confidence scores show less than 0.3 correlation with actual accuracy | Add mandatory warnings; evaluate range/interval defaults for CNF |
| Regulatory Signal | INFO | EU AI Act or NIST mandate structured provenance for multi-agent AI | Accelerate Phase 3 regulated-industry pilot |

### 12.3 Convergence Risk

Convergence is the single highest strategic risk, rated MEDIUM-HIGH. IBM ACP's CitationMetadata and TrajectoryMetadata (now merged into A2A) demonstrate that the ecosystem is moving toward structured epistemic metadata. Each A2A release that adds a confidence field, evidence array, or verification status narrows ASV's value proposition.

The defense is structural: there is a genuine difference between adding metadata fields piecemeal and defining a coherent vocabulary with compositional semantics. A `confidence` field on an A2A message is not the same as a CLM object with typed epistemic classification, structured confidence distribution with calibration, linked evidence with quality classes, grounded provenance extending W3C PROV, and verification records -- all composed into a single auditable chain. Whether the market values that difference is the key uncertainty.

---

## 13. Implementation Roadmap

### Phase 1: Core Vocabulary and Reference Validator (6 weeks)

**Deliverables:**
- JSON Schema files for 7 core types (AGT, CLM, CNF, EVD, PRV, VRF, SAE)
- JSON-LD `@context` document mapping ASV terms to PROV-O and Schema.org URIs
- Python reference validator (schema + basic semantic checks)
- TypeScript reference validator (schema + basic semantic checks)
- 3 integration examples: A2A task with ASV artifacts, MCP tool with ASV response, standalone ASV document
- 10 example ASV objects covering all 7 types and 6 performatives

**Kill criteria:** LLMs cannot generate valid ASV objects at greater than 80% structural validity. OR validation overhead exceeds 10ms per message. OR A2A/MCP integration requires protocol modifications.

### Phase 2: Semantic Specification and Empirical Validation (8 weeks)

**Deliverables:**
- Complete Semantic Specification v1.0 (capped at 50 pages)
- GATE-2 experiment results (LLM generation accuracy across 3 models)
- Speech-act routing effectiveness experiment results
- Conformance test suite (50+ tests)
- PROV-JSON export module for ASV provenance objects

**Kill criteria:** LLM generation accuracy below 70% for full CLM-CNF-EVD-PRV-VRF chains. OR speech-act routing provides less than 10% coordination improvement versus untyped messages.

### Phase 3: Ecosystem Integration and Regulated Industry Pilot (12 weeks)

**Deliverables:**
- LangGraph/CrewAI/AutoGen integration plugins
- GATE-3 experiment results (provenance chain utility)
- Regulated industry pilot (financial services or healthcare)
- ASV vocabulary contribution to W3C AI Agent Protocol CG or AAIF
- Token cost comparison results and minified ASV variant

**Kill criteria:** Provenance chain utility shows less than 20% improvement over no-provenance baseline. OR regulated industry pilot reveals unfixable compliance gaps.

### Phase 4: Standard Maturation and Optimization (16 weeks)

**Deliverables:**
- ASV vocabulary v2.0 incorporating pilot feedback
- Binary encoding (Protobuf schema) for high-throughput scenarios
- Formal properties document (TLA+ verification of critical safety invariants)
- Public specification for community review

**Kill criteria:** Community review identifies fundamental architecture-level design flaws. OR binary encoding provides less than 2x throughput improvement over JSON.

**Total timeline: 42 weeks (approximately 10 months).**

**Critical path:** Phase 1 must deliver a working validator before Phase 2 begins. GATE-2 (LLM generation accuracy) must pass before the semantic spec is finalized. GATE-3 (provenance utility) must pass before Phase 3 ecosystem integration.

---

## 14. Conclusion

ASV is a modest invention with a specific ambition. It does not propose a new protocol, a new transport, or a new paradigm for agent communication. It proposes a vocabulary -- a set of typed JSON structures that make agent claims epistemically accountable.

The genuine novelty is narrow: the claim classification taxonomy, the dual classification framework, and the structured confidence primitive. Everything else -- provenance, verification, JSON Schema delivery, JSON-LD semantics -- is competent application of existing standards. This is an honest assessment. The Assessment Council scored novelty at 3/5 and the adversarial analyst identified two genuinely novel components out of eleven. ASV is an integration project, not a breakthrough.

But integration projects succeed through execution, and the integration itself has value. No existing system combines claim classification, structured confidence with calibration metadata, evidence quality typing, W3C PROV-grounded provenance, and verification records into a single, validated, composable vocabulary for agent communication. The components exist separately; the specific assembly does not. Whether that assembly justifies a formal vocabulary standard depends on empirical validation -- the three gate experiments are the arbiters, not this specification.

The 12-18 month window is real. W3C community groups are forming. NIST is launching standards initiatives. Regulatory mandates for AI traceability are approaching. Someone will define the semantic vocabulary for epistemic accountability in agent communication. ASV is a credible candidate, contingent on shipping working code, demonstrating measurable benefit, and engaging with the standards community before the window closes.

---

## Appendices

### Appendix A: Complete JSON Schema Definitions

All schema files are listed below with their canonical URIs:

| File | URI | Description |
|------|-----|-------------|
| `agt.schema.json` | `https://asv.atrahasis.dev/vocab/v1/agt.schema.json` | Agent type |
| `clm.schema.json` | `https://asv.atrahasis.dev/vocab/v1/clm.schema.json` | Claim type |
| `cnf.schema.json` | `https://asv.atrahasis.dev/vocab/v1/cnf.schema.json` | Confidence type |
| `evd.schema.json` | `https://asv.atrahasis.dev/vocab/v1/evd.schema.json` | Evidence type |
| `prv.schema.json` | `https://asv.atrahasis.dev/vocab/v1/prv.schema.json` | Provenance type |
| `vrf.schema.json` | `https://asv.atrahasis.dev/vocab/v1/vrf.schema.json` | Verification type |
| `sae.schema.json` | `https://asv.atrahasis.dev/vocab/v1/sae.schema.json` | Speech-Act Envelope type |
| `chain.schema.json` | `https://asv.atrahasis.dev/vocab/v1/chain.schema.json` | Complete epistemic chain |
| `document.schema.json` | `https://asv.atrahasis.dev/vocab/v1/document.schema.json` | Standalone document format |
| `a2a-part.schema.json` | `https://asv.atrahasis.dev/vocab/v1/a2a-part.schema.json` | A2A message part wrapper |
| `mcp-content.schema.json` | `https://asv.atrahasis.dev/vocab/v1/mcp-content.schema.json` | MCP tool response wrapper |
| `context.jsonld` | `https://asv.atrahasis.dev/vocab/v1/context.jsonld` | JSON-LD context |

Full schema definitions for all types are provided inline in Section 3 of this specification. The schemas use JSON Schema Draft 2020-12 with `$ref` for cross-type references and `const` for type discrimination.

### Appendix B: Invention Claim Scope

Per Assessment Council REQ-1 (Narrow the Invention Claim), ASV's components are categorized:

**Genuinely Novel:**
- Claim classification taxonomy (`epistemic_class`: observation, correlation, causation, inference, prediction, prescription) -- no precedent in any agent communication system
- Dual classification framework (speech-act type x epistemic class) -- no existing system classifies both dimensions
- Structured confidence primitive (CNF) with declared method and calibration metadata -- no existing standard addresses this

**Novel Integration:**
- CLM-CNF-EVD-PRV-VRF epistemic accountability chain as a unified communication vocabulary
- Temporal validity with re-verification triggers on claims
- Evidence quality typing integrated with provenance chain

**Application of Existing Standards (not claimed as invention):**
- Provenance model (extends W3C PROV-O)
- Verification alignment (W3C VC Data Integrity)
- JSON Schema delivery mechanism (Draft 2020-12)
- JSON-LD context for semantic interoperability
- Speech-act taxonomy structure (draws from FIPA ACL tradition)
- A2A and MCP integration patterns (use existing extensibility)

### Appendix C: Traceability Matrix

| Assessment Council Condition | ID | Status | Where Addressed |
|------------------------------|-----|--------|----------------|
| Working Implementation Before Full Spec | GATE-1 | PENDING | Section 13 Phase 1; schemas defined in Section 3 |
| LLM Generation Accuracy | GATE-2 | PENDING | Section 10.1; schemas designed for LLM-friendly generation |
| Provenance Chain Utility | GATE-3 | PENDING | Section 10.1; chain structure defined in Section 2 |
| Narrow the Invention Claim | REQ-1 | ADDRESSED | Appendix B |
| Kill AACP as Separate Protocol | REQ-2 | ADDRESSED | Section 1.4, Section 5 (A2A/MCP integration only) |
| Address Confidence Calibration | REQ-3 | ADDRESSED | Section 3.3, Section 7 |
| Semantic Spec Cap (50 pages) | REQ-4 | ADDRESSED | Section 7 note; semantic spec is a separate deliverable |
| Regulated Industry Engagement | REC-1 | PENDING | Section 11.1; Section 2.3 demonstrates healthcare use case |
| A2A Specification Monitoring | REC-2 | PENDING | Section 12.2 monitoring flags |

### Appendix D: Glossary

| Term | Definition |
|------|-----------|
| **A2A** | Google Agent-to-Agent Protocol. The dominant agent-to-agent communication protocol, now under Linux Foundation governance. |
| **AAIF** | Agentic AI Foundation. Linux Foundation organization governing A2A and MCP. |
| **AASL** | Atrahasis Agent Specification Language. The original declarative language from which ASV extracts its semantic model. |
| **AGT** | Agent. An ASV type representing an entity that bears responsibility for epistemic activities. |
| **ASV** | AASL Semantic Vocabulary. The JSON Schema vocabulary defined in this specification. |
| **Canonical form** | The deterministic serialized representation of an ASV object after Section 6.1 normalization rules are applied. |
| **Canonical hash** | A hash computed over the exact bytes of `canonical_json` so semantically equivalent ASV objects receive the same deduplication key. |
| **Canonicalizer service** | The Section 6.1 normalization service that converts valid ASV objects into canonical form for comparison, hashing, and deduplication. |
| **CLM** | Claim. An ASV type representing a knowledge assertion with epistemic classification. |
| **CNF** | Confidence. An ASV type representing structured confidence with method declaration and calibration metadata. |
| **Dual classification** | ASV's approach of classifying messages along two orthogonal dimensions: speech-act type and epistemic class. |
| **ECE** | Expected Calibration Error. A metric measuring how well confidence estimates align with actual accuracy. |
| **Epistemic accountability chain** | The composed structure CLM-CNF-EVD-PRV-VRF that forms a complete, auditable epistemic record. |
| **EVD** | Evidence. An ASV type representing supporting data with quality classification. |
| **FIPA ACL** | Foundation for Intelligent Physical Agents Agent Communication Language. A predecessor standard that died from over-specification. |
| **JSON-LD** | JSON for Linked Data. W3C standard for embedding semantic annotations in JSON. |
| **MCP** | Model Context Protocol. Anthropic's protocol for agent-to-tool connectivity, now under AAIF governance. |
| **PRV** | Provenance. An ASV type representing the origin and derivation history of a claim. |
| **PROV-O** | W3C Provenance Ontology. The W3C standard that ASV's provenance model extends. |
| **SAE** | Speech-Act Envelope. An ASV type wrapping epistemic content in a performative. |
| **uACP** | Universal Agent Communication Protocol. Formal protocol with a completeness proof showing 4 verbs suffice for finite-state protocols. |
| **VRF** | Verification. An ASV type capturing the result of independent claim validation. |
| **W3C VC** | W3C Verifiable Credentials. The standard ASV's verification records align with. |

---

*ASV Master Technical Specification v2.0.1*
*Completed 2026-03-09 | Updated 2026-03-12*
*Atrahasis Agent System -- C4-A*

---

### Appendix F: Atrahasis Stack Integration (Informative)

> **Note:** This appendix is NON-NORMATIVE. It provides informational context about ASV's position within the broader Atrahasis architecture. Nothing in this appendix changes ASV's transport-agnostic design, modifies any normative requirement in Sections 1-14, or constrains ASV's use outside the Atrahasis stack. The authoritative source for cross-layer integration is the **C9 Cross-Layer Reconciliation Addendum**.

#### F.1 ASV's Position in the Architecture Stack

ASV operates as the communication vocabulary layer within the Atrahasis agent architecture. All layers above ASV produce or consume ASV-typed messages; ASV itself defines only the semantic structures, not how they are routed, verified, metabolized, or settled.

```
Layer                                 Specification
─────────────────────────────────────────────────────
RIF (orchestration)               ←  C7
Tidal Noosphere (coordination)    ←  C3
PCVM (verification)               ←  C5
EMA (knowledge metabolism)        ←  C6
Settlement Plane (AIC economy)    ←  C8
ASV (communication vocabulary)    ←  C4  ← THIS SPECIFICATION
Cross-Layer Integration           ←  C9
```

ASV is consumed upward by PCVM (C5) for claim verification, by EMA (C6) for knowledge metabolism, and by the Tidal Noosphere (C3) for coordination semantics. It is referenced downward by C9 for cross-layer type reconciliation. ASV does not depend on any layer above it and can be used independently outside the Atrahasis stack.

#### F.2 Epistemic Class to Claim Class Mapping

When ASV claims enter the PCVM (C5) verification pipeline, the `epistemic_class` field on CLM objects maps to PCVM claim classes as follows:

| C4 `epistemic_class` | Primary C5 Claim Class | Override Condition | Override Class |
|----------------------|----------------------|-------------------|----------------|
| `observation` | E (Empirical) | Evidence `quality_class` = `"computational_result"` | D (Deterministic) |
| `correlation` | S (Statistical) | -- | -- |
| `causation` | R (Reasoning) | Evidence includes experimental/RCT data | S (Statistical) |
| `inference` | R (Reasoning) | Confidence `method` = `"model_derived"` | H (Heuristic) |
| `prediction` | H (Heuristic) | Confidence `method` = `"statistical"` with non-null `interval` | S (Statistical) |
| `prescription` | N (Normative) | -- | -- |

The primary class applies by default. When the override condition is met, the override class takes precedence. This mapping is performed by the consuming system (PCVM), not by ASV itself -- ASV is unaware of claim classes.

#### F.3 Mapping Algorithm

The following pseudocode defines the deterministic mapping from ASV epistemic classes to PCVM claim classes:

```
FUNCTION map_c4_to_c5(clm: ASV.CLM) -> ClaimClass:
    MATCH clm.epistemic_class:
        "observation":
            IF has_evidence(clm, "computational_result"): RETURN D
            RETURN E
        "correlation": RETURN S
        "causation":
            IF has_evidence(clm, "computational_result"): RETURN S
            RETURN R
        "inference":
            IF clm.confidence.method == "model_derived": RETURN H
            RETURN R
        "prediction":
            IF clm.confidence.method == "statistical" AND clm.confidence.interval IS NOT NULL: RETURN S
            RETURN H
        "prescription": RETURN N
```

The helper function `has_evidence(clm, quality_class)` returns true if any element in `clm.evidence[]` has the specified `quality_class` value. When `clm.evidence` is absent or empty, all evidence-based override conditions evaluate to false and the primary class applies.

#### F.4 ASV Token to PCVM Intake Flow

When an ASV-typed message enters the PCVM verification pipeline, its components map to PCVM intake structures as follows:

```
C4 ASV Message:                    C5 PCVM Intake:
  CLM (claim)          ──────►      Claim content + proposed class
  CLM.epistemic_class  ──────►      Preliminary class (via mapping in F.3)
  CNF (confidence)     ──────►      Initial SL opinion seed
  EVD[] (evidence)     ──────►      VTD dependencies
  PRV (provenance)     ──────►      VTD provenance chain
  VRF (verification)   ◄──────      MCT output (SL opinion + final class)
```

The flow is unidirectional from ASV to PCVM for all components except VRF: the PCVM produces verification records that flow back as VRF objects attached to the original CLM. This bidirectional VRF flow closes the epistemic accountability chain -- a claim enters PCVM with confidence and evidence, and exits with an independent verification record.

#### F.5 Scope and Authority

This appendix is derived from the C9 Cross-Layer Reconciliation Addendum (Errata E-C4-01). In the event of any conflict between this appendix and C9, the C9 specification governs. ASV's normative requirements (Sections 1-14 and Appendices A-E) are unchanged by this appendix. Implementors using ASV outside the Atrahasis stack may disregard this appendix entirely.

---

## Changelog

| Version | Date | Description |
|---------|------|-------------|
| v2.0.1 | 2026-03-12 | Added Section 6.1 `Canonicalizer Service` for deterministic ASV normalization and deduplication. Added canonicalization conformance requirements, test vectors, glossary entries, and updated document metadata. |
| v2.0 | 2026-03-10 | Added Appendix F (Atrahasis Stack Integration) per C9 Errata E-C4-01. Non-normative appendix describing ASV's position in the architecture stack, epistemic_class to claim_class mapping, mapping algorithm, and ASV-to-PCVM intake flow. No changes to normative specification content. |
| v1.0 | 2026-03-09 | Initial release. Complete ASV specification with 7 core types, JSON Schema definitions, JSON-LD context, integration patterns, validation plan, and implementation roadmap. |
