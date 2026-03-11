# ASV -- Technical Specification

## C4-A DESIGN Document

**Version:** 0.1.0-draft
**Date:** 2026-03-09
**Status:** DESIGN (Conditional Advance from Assessment Council)
**Namespace:** `https://asv.atrahasis.dev/vocab/v1`
**JSON Schema Dialect:** Draft 2020-12
**Normative References:** W3C PROV-O, W3C Verifiable Credentials Data Model, JSON Schema Draft 2020-12, RFC 3339, RFC 2119

---

### 1. Specification Overview

#### 1.1 Scope

This specification defines the ASV (AASL Semantic Vocabulary), a JSON Schema vocabulary and companion JSON-LD context for epistemic accountability in AI agent communication. ASV provides typed semantic structures that embed inside Google A2A messages, Anthropic MCP tool responses, or standalone JSON documents.

ASV is a vocabulary, not a protocol. It defines no transport, no connection management, no message routing, and no task lifecycle. Those concerns are delegated to A2A and MCP.

#### 1.2 Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

All JSON examples in this specification are normative unless explicitly marked "non-normative."

#### 1.3 Relationship to Other Standards

| Standard | Relationship |
|---|---|
| AASL | ASV extracts AASL's epistemic type system into JSON Schema. ASV is the portable vocabulary; AASL remains the internal Atrahasis declaration language. |
| W3C PROV-O | ASV extends PROV-O. CLM maps to prov:Entity, PRV maps to prov:Activity, AGT maps to prov:Agent. ASV does not replace PROV. |
| W3C VC Data Model | VRF aligns with VC Data Integrity for cryptographic proof structures. ASV does not implement the full VC stack. |
| JSON Schema 2020-12 | ASV types are defined as JSON Schema definitions using the vocabulary extension mechanism. |
| A2A | ASV types embed as structured data Parts in A2A Messages and as Artifacts on A2A Tasks. |
| MCP | ASV types embed as structured content in MCP Tool responses. |
| FIPA ACL / uACP | The speech-act envelope draws from FIPA's performative tradition, constrained by uACP's 4-verb completeness proof, using Singh commitment semantics. |

#### 1.4 What This Spec Covers vs the Semantic Spec

This technical specification defines the structural schemas, validation rules, integration formats, and conformance requirements that are machine-enforceable via JSON Schema.

The companion Semantic Specification (a separate document, capped at 50 pages) defines interpretation contracts that JSON Schema cannot enforce: epistemic semantics of confidence values, operation class composition algebra, graph referential integrity constraints, calibration requirements, and commitment lifecycle rules.

Where schema and semantic spec diverge, the semantic spec is normative.

---

### 2. ASV Type System

ASV defines eight core types. Every ASV object MUST include a `type` discriminator field and an `id` field. The `type` field determines which schema applies.

#### 2.1 Agent (AGT)

An Agent is an entity that bears responsibility for claims, actions, and activities within the epistemic chain. AGT maps to `prov:Agent`.

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
    "type": {
      "const": "AGT"
    },
    "id": {
      "type": "string",
      "format": "uri",
      "description": "Stable URI-based identifier for this agent."
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "description": "Human-readable agent name."
    },
    "role": {
      "type": "string",
      "description": "Functional role of the agent (e.g., researcher, verifier, coordinator)."
    },
    "model": {
      "type": "string",
      "description": "Model identifier, if this agent is backed by an AI model."
    },
    "capabilities": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of capability identifiers this agent supports."
    },
    "asv_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "ASV vocabulary version this agent conforms to."
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

**Semantic Notes:** An AGT object represents the entity responsible for generating or verifying claims. When used within a PRV record, the AGT id is referenced via the `agent_id` field. AGT maps to `prov:Agent` in the JSON-LD context. The `model` field, when present, identifies the AI model but does not imply any specific capability guarantee.

---

#### 2.2 Claim (CLM)

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
    "type": {
      "const": "CLM"
    },
    "id": {
      "type": "string",
      "format": "uri"
    },
    "content": {
      "type": "string",
      "minLength": 1,
      "description": "The natural language or structured content of the claim."
    },
    "epistemic_class": {
      "type": "string",
      "enum": ["observation", "correlation", "causation", "inference", "prediction", "prescription"],
      "description": "The epistemic nature of the knowledge assertion."
    },
    "agent_id": {
      "type": "string",
      "format": "uri",
      "description": "URI of the AGT that produced this claim."
    },
    "confidence": {
      "$ref": "https://asv.atrahasis.dev/vocab/v1/cnf.schema.json",
      "description": "Structured confidence assessment for this claim."
    },
    "evidence": {
      "type": "array",
      "items": {
        "$ref": "https://asv.atrahasis.dev/vocab/v1/evd.schema.json"
      },
      "description": "Evidence supporting this claim."
    },
    "provenance": {
      "$ref": "https://asv.atrahasis.dev/vocab/v1/prv.schema.json",
      "description": "Provenance record for how this claim was generated."
    },
    "verification": {
      "$ref": "https://asv.atrahasis.dev/vocab/v1/vrf.schema.json",
      "description": "Verification record for this claim."
    },
    "rebuts_claims": {
      "type": "array",
      "items": {
        "type": "string",
        "format": "uri"
      },
      "description": "URIs of CLM objects that this claim rebuts."
    },
    "valid_from": {
      "type": "string",
      "format": "date-time",
      "description": "RFC 3339 timestamp from which this claim is considered valid."
    },
    "valid_until": {
      "type": "string",
      "format": "date-time",
      "description": "RFC 3339 timestamp after which this claim should be re-verified or discarded."
    },
    "subject": {
      "type": "string",
      "description": "The subject entity or variable of this claim."
    },
    "object": {
      "type": "string",
      "description": "The object entity or variable of this claim, when applicable."
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "additionalProperties": false
}
```

**Claim Classification Fields:**

- `epistemic_class` classifies the nature of the knowledge assertion:
  - `observation`: A directly witnessed or measured fact.
  - `correlation`: A statistical association between variables.
  - `causation`: An asserted causal relationship.
  - `inference`: A conclusion derived from reasoning over evidence.
  - `prediction`: A forward-looking assertion about future states.
  - `prescription`: A normative recommendation (what should be done).

**Example:**

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:temp-co2-correlation-001",
  "content": "Global surface temperature anomaly shows a Pearson correlation of r=0.92 with atmospheric CO2 concentration over the period 1960-2024.",
  "epistemic_class": "correlation",
  "agent_id": "urn:asv:agent:research-01",
  "subject": "global_surface_temperature_anomaly",
  "object": "atmospheric_co2_concentration",
  "confidence": {
    "type": "CNF",
    "id": "urn:asv:confidence:temp-co2-001",
    "value": 0.92,
    "interval": [0.89, 0.95],
    "method": "statistical",
    "sample_size": 64,
    "calibration": {
      "status": "calibrated",
      "dataset_id": "urn:asv:dataset:climate-bench-2024",
      "calibration_date": "2025-12-01T00:00:00Z",
      "metric": "brier_score",
      "metric_value": 0.08
    }
  },
  "evidence": [
    {
      "type": "EVD",
      "id": "urn:asv:evidence:nasa-gistemp-001",
      "quality_class": "direct_observation",
      "source_type": "dataset",
      "source_id": "urn:asv:dataset:nasa-gistemp-v4",
      "description": "NASA GISTEMP v4 global temperature anomaly dataset, 1880-2024.",
      "retrieved_at": "2025-11-15T10:30:00Z"
    }
  ],
  "valid_from": "2025-12-01T00:00:00Z",
  "valid_until": "2026-12-01T00:00:00Z",
  "created_at": "2025-12-01T14:22:00Z"
}
```

---

#### 2.3 Confidence (CNF)

Confidence is the core novel primitive in ASV. It represents structured confidence as a distribution with a declared method and calibration metadata. No existing standard addresses structured confidence for agent reasoning.

CNF supports three representation modes: point estimate, interval, and discrete distribution.

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/cnf.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Confidence",
  "description": "Structured confidence assessment with method declaration and calibration metadata. The core novel ASV primitive.",
  "type": "object",
  "required": ["type", "id", "method"],
  "properties": {
    "type": {
      "const": "CNF"
    },
    "id": {
      "type": "string",
      "format": "uri"
    },
    "value": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Point estimate of confidence, in [0, 1]."
    },
    "interval": {
      "type": "array",
      "items": { "type": "number", "minimum": 0, "maximum": 1 },
      "minItems": 2,
      "maxItems": 2,
      "description": "Confidence interval as [lower_bound, upper_bound]."
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
      },
      "description": "Discrete probability distribution over named outcomes."
    },
    "method": {
      "type": "string",
      "enum": ["statistical", "consensus", "model_derived", "human_judged", "heuristic"],
      "description": "The method by which confidence was assessed."
    },
    "sample_size": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of samples or observations underlying this confidence, if applicable."
    },
    "calibration": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["calibrated", "uncalibrated", "self_reported"],
          "description": "Whether this confidence has been empirically calibrated."
        },
        "dataset_id": {
          "type": "string",
          "format": "uri",
          "description": "Identifier of the calibration dataset used."
        },
        "calibration_date": {
          "type": "string",
          "format": "date-time"
        },
        "metric": {
          "type": "string",
          "description": "Calibration metric used (e.g., brier_score, ece, reliability_diagram)."
        },
        "metric_value": {
          "type": "number",
          "description": "Value of the calibration metric."
        }
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

**Representation Modes:**

1. **Point estimate:** A single value in [0, 1]. The simplest mode. Example: `"value": 0.87`.
2. **Interval:** A lower and upper bound. Example: `"interval": [0.82, 0.91]`. When both `value` and `interval` are present, `value` MUST fall within the interval.
3. **Distribution:** A discrete distribution over named outcomes. Probabilities SHOULD sum to 1.0 (within floating-point tolerance of 0.001). Example: `"distribution": [{"outcome": "true", "probability": 0.87}, {"outcome": "false", "probability": 0.13}]`.

**Calibration Metadata:**

The `calibration` object addresses the Assessment Council's REQ-3 requirement. Confidence values from LLM-based agents are frequently uncalibrated. The `status` field distinguishes:

- `calibrated`: Confidence has been validated against a held-out dataset; `metric` and `metric_value` SHOULD be present.
- `uncalibrated`: Confidence is a raw model output with no empirical validation. Consumers SHOULD treat with caution.
- `self_reported`: The agent reports its own confidence without external validation.

When `status` is `uncalibrated` or `self_reported`, conforming implementations SHOULD display a warning to downstream consumers.

**Example (interval with calibration):**

```json
{
  "type": "CNF",
  "id": "urn:asv:confidence:model-pred-042",
  "value": 0.78,
  "interval": [0.71, 0.84],
  "method": "model_derived",
  "calibration": {
    "status": "uncalibrated",
    "dataset_id": "urn:asv:dataset:internal-eval-set",
    "calibration_date": "2026-02-15T00:00:00Z",
    "metric": "ece",
    "metric_value": 0.12
  }
}
```

**Example (distribution):**

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
  "calibration": {
    "status": "self_reported"
  }
}
```

---

#### 2.4 Evidence (EVD)

Evidence links claims to supporting data with evidence quality typing. EVD maps to `prov:Entity` linked via `asv:supportedBy` (a subproperty of `prov:wasDerivedFrom`).

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
    "type": {
      "const": "EVD"
    },
    "id": {
      "type": "string",
      "format": "uri"
    },
    "quality_class": {
      "type": "string",
      "enum": ["direct_observation", "inference", "hearsay", "computational_result", "delegation"],
      "description": "The epistemic quality class of this evidence."
    },
    "source_type": {
      "type": "string",
      "enum": ["dataset", "document", "api", "agent_output", "sensor", "human_input", "other"],
      "description": "The type of source from which this evidence was obtained."
    },
    "source_id": {
      "type": "string",
      "format": "uri",
      "description": "URI identifying the specific source."
    },
    "description": {
      "type": "string",
      "description": "Human-readable description of this evidence."
    },
    "content": {
      "description": "The evidence content itself, if inline rather than referenced.",
      "oneOf": [
        { "type": "string" },
        { "type": "object" },
        { "type": "array" }
      ]
    },
    "retrieved_at": {
      "type": "string",
      "format": "date-time",
      "description": "When this evidence was retrieved or observed."
    },
    "agent_id": {
      "type": "string",
      "format": "uri",
      "description": "The agent that collected or produced this evidence."
    }
  },
  "additionalProperties": false
}
```

**Quality Classes:**

| Class | Description | Epistemic Weight |
|---|---|---|
| `direct_observation` | First-hand measurement or sensory data from a sensor, instrument, or direct API call. | Highest |
| `inference` | Conclusion derived by the agent through reasoning over other evidence. | High |
| `computational_result` | Output of a deterministic computation, simulation, or model execution. | High |
| `delegation` | Evidence obtained from another agent's claim. Provenance chain SHOULD be traceable. | Medium |
| `hearsay` | Unverified report from an indirect source. | Lowest |

The `quality_class` vocabulary is namespace-extensible. Implementations MAY define additional quality classes under their own namespace.

**Example:**

```json
{
  "type": "EVD",
  "id": "urn:asv:evidence:api-result-445",
  "quality_class": "computational_result",
  "source_type": "api",
  "source_id": "urn:asv:api:weather-service/forecast",
  "description": "7-day temperature forecast from NOAA Weather Service API.",
  "retrieved_at": "2026-03-09T08:00:00Z",
  "agent_id": "urn:asv:agent:data-collector-02"
}
```

---

#### 2.5 Provenance (PRV)

Provenance records the origin and derivation history of a claim. PRV extends W3C PROV-O by mapping to `prov:Activity` with `wasGeneratedBy` and `used` relations.

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
    "type": {
      "const": "PRV"
    },
    "id": {
      "type": "string",
      "format": "uri"
    },
    "agent_id": {
      "type": "string",
      "format": "uri",
      "description": "URI of the AGT responsible for this activity. Maps to prov:wasAssociatedWith."
    },
    "activity_type": {
      "type": "string",
      "enum": ["generation", "derivation", "aggregation", "transformation", "delegation", "verification"],
      "description": "The type of provenance activity."
    },
    "started_at": {
      "type": "string",
      "format": "date-time",
      "description": "When this activity started. Maps to prov:startedAtTime."
    },
    "ended_at": {
      "type": "string",
      "format": "date-time",
      "description": "When this activity ended. Maps to prov:endedAtTime."
    },
    "used": {
      "type": "array",
      "items": {
        "type": "string",
        "format": "uri"
      },
      "description": "URIs of entities used by this activity. Maps to prov:used."
    },
    "was_informed_by": {
      "type": "array",
      "items": {
        "type": "string",
        "format": "uri"
      },
      "description": "URIs of other activities that informed this one. Maps to prov:wasInformedBy."
    },
    "delegated_from": {
      "type": "string",
      "format": "uri",
      "description": "Agent on whose behalf this activity was performed. Maps to prov:actedOnBehalfOf."
    },
    "method": {
      "type": "string",
      "description": "Description of the method or procedure used in this activity."
    },
    "tool_id": {
      "type": "string",
      "format": "uri",
      "description": "Identifier of the tool used in this activity, if applicable."
    }
  },
  "additionalProperties": false
}
```

**W3C PROV Mapping:**

| ASV Field | PROV-O Property |
|---|---|
| PRV object | prov:Activity |
| `agent_id` | prov:wasAssociatedWith |
| `started_at` | prov:startedAtTime |
| `ended_at` | prov:endedAtTime |
| `used` | prov:used |
| `was_informed_by` | prov:wasInformedBy |
| `delegated_from` | prov:actedOnBehalfOf |
| Generated CLM | prov:wasGeneratedBy (inverse) |

**Example:**

```json
{
  "type": "PRV",
  "id": "urn:asv:provenance:analysis-run-887",
  "agent_id": "urn:asv:agent:research-01",
  "activity_type": "generation",
  "started_at": "2025-12-01T14:00:00Z",
  "ended_at": "2025-12-01T14:22:00Z",
  "used": [
    "urn:asv:dataset:nasa-gistemp-v4",
    "urn:asv:dataset:noaa-co2-mauna-loa"
  ],
  "method": "Pearson correlation analysis with 95% confidence interval via scipy.stats.pearsonr"
}
```

---

#### 2.6 Verification (VRF)

A Verification record captures the result of an independent validation of a claim. VRF maps to a `prov:Activity` of type `asv:VerificationActivity`, aligned with W3C Verifiable Credentials Data Integrity for cryptographic proof when needed.

**JSON Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/vrf.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Verification",
  "description": "Independent verification record for a claim. Maps to prov:Activity of type asv:VerificationActivity.",
  "type": "object",
  "required": ["type", "id", "claim_id", "verifier_id", "status", "method"],
  "properties": {
    "type": {
      "const": "VRF"
    },
    "id": {
      "type": "string",
      "format": "uri"
    },
    "claim_id": {
      "type": "string",
      "format": "uri",
      "description": "URI of the CLM being verified."
    },
    "verifier_id": {
      "type": "string",
      "format": "uri",
      "description": "URI of the AGT performing verification."
    },
    "status": {
      "type": "string",
      "enum": ["verified", "disputed", "inconclusive", "pending"],
      "description": "Outcome of the verification activity."
    },
    "method": {
      "type": "string",
      "enum": ["replication", "cross_reference", "formal_proof", "consensus", "cryptographic", "human_review"],
      "description": "Method used for verification."
    },
    "verified_at": {
      "type": "string",
      "format": "date-time"
    },
    "details": {
      "type": "string",
      "description": "Human-readable explanation of the verification result."
    },
    "proof": {
      "type": "object",
      "description": "Cryptographic proof object, aligned with W3C VC Data Integrity. Structure depends on proof type.",
      "properties": {
        "proof_type": { "type": "string" },
        "created": { "type": "string", "format": "date-time" },
        "verification_method": { "type": "string", "format": "uri" },
        "proof_value": { "type": "string" }
      },
      "additionalProperties": true
    },
    "confidence_in_verification": {
      "$ref": "https://asv.atrahasis.dev/vocab/v1/cnf.schema.json",
      "description": "The verifier's confidence in their verification result."
    }
  },
  "additionalProperties": false
}
```

**Example:**

```json
{
  "type": "VRF",
  "id": "urn:asv:verification:peer-review-003",
  "claim_id": "urn:asv:claim:temp-co2-correlation-001",
  "verifier_id": "urn:asv:agent:verifier-02",
  "status": "verified",
  "method": "replication",
  "verified_at": "2025-12-05T09:15:00Z",
  "details": "Replicated correlation analysis using independent R implementation on same dataset. Obtained r=0.91, within expected tolerance.",
  "confidence_in_verification": {
    "type": "CNF",
    "id": "urn:asv:confidence:vrf-003-cnf",
    "value": 0.95,
    "method": "statistical",
    "calibration": { "status": "calibrated", "metric": "brier_score", "metric_value": 0.04, "calibration_date": "2025-11-01T00:00:00Z" }
  }
}
```

---

#### 2.7 Rebuttal (RBT)

A Rebuttal is a specialized Claim that disputes one or more existing claims, enabling Toulmin-complete argumentation. RBT is structurally a CLM with mandatory `rebuts_claims` and its own full epistemic chain.

Rebuttals are represented as CLM objects with a non-empty `rebuts_claims` array. There is no separate RBT schema; the CLM schema handles rebuttals natively. This design choice ensures rebuttals carry the same epistemic accountability as primary claims.

**Identification Rule:** A CLM object is a rebuttal if and only if its `rebuts_claims` array is non-empty.

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

---

#### 2.8 Temporal Validity (TVL)

Temporal validity is not a separate type. It is expressed through the `valid_from` and `valid_until` fields on CLM objects. This section documents the semantics.

**Rules:**

1. If `valid_from` is absent, the claim is valid from its `created_at` timestamp.
2. If `valid_until` is absent, the claim is considered indefinitely valid until explicitly invalidated.
3. If `valid_until` is in the past relative to the current time, the claim SHOULD be flagged for re-verification.
4. `valid_from` MUST be earlier than or equal to `valid_until` when both are present.
5. Temporal validity does not affect structural validity. An expired claim is still a valid ASV object; it is semantically stale, not structurally invalid.

**Re-verification Triggers:**

Conforming implementations SHOULD implement at least one of:

- Periodic scan for claims where `valid_until < now()`.
- Event-driven notification when a claim's temporal validity expires.
- Query-time filtering that flags expired claims in result sets.

**Example:**

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:market-forecast-q1-2026",
  "content": "S&P 500 expected to remain in the range 5800-6200 during Q1 2026.",
  "epistemic_class": "prediction",
  "agent_id": "urn:asv:agent:market-analyst-01",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2026-03-31T23:59:59Z",
  "confidence": {
    "type": "CNF",
    "id": "urn:asv:confidence:market-q1-cnf",
    "value": 0.60,
    "interval": [0.45, 0.72],
    "method": "model_derived",
    "calibration": { "status": "self_reported" }
  },
  "created_at": "2025-12-20T16:00:00Z"
}
```

---

### 3. Epistemic Accountability Chain

The epistemic accountability chain is ASV's core architectural contribution. It defines how CLM, CNF, EVD, PRV, and VRF compose to form a complete, auditable epistemic record.

#### 3.1 Composition

```
CLM (Claim)
  |-- CNF (Confidence) -- how confident is the claim?
  |-- EVD[] (Evidence) -- what supports the claim?
  |-- PRV (Provenance) -- how was the claim generated?
  |-- VRF (Verification) -- has the claim been independently validated?
  |-- rebuts_claims[] -- what other claims does this dispute?
  |-- valid_from / valid_until -- when is this claim temporally valid?
```

A CLM object is the root of the chain. CNF, EVD, PRV, and VRF are attached as nested objects or referenced by URI.

#### 3.2 Chain JSON Schema

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/chain.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Epistemic Accountability Chain",
  "description": "A complete claim with all epistemic metadata attached.",
  "type": "object",
  "required": ["type", "id", "content", "epistemic_class", "agent_id", "confidence", "evidence", "provenance"],
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
      "items": { "$ref": "https://asv.atrahasis.dev/vocab/v1/evd.schema.json" },
      "minItems": 1
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

#### 3.3 Validation Rules

1. `confidence.method` MUST be one of the defined method values.
2. Every `evidence[].source_id` SHOULD be a resolvable URI (application-layer validation; not enforceable by JSON Schema).
3. `provenance.agent_id` MUST match `agent_id` on the parent CLM, unless `provenance.delegated_from` is set (indicating the provenance activity was performed on behalf of another agent).
4. If `verification` is present, `verification.claim_id` MUST match the CLM's `id`.
5. If both `valid_from` and `valid_until` are present, `valid_from` MUST be less than or equal to `valid_until` (application-layer validation).
6. Each `evidence` item MUST have a unique `id` within the chain.

#### 3.4 Chain Completeness Levels

| Level | Requirements |
|---|---|
| Minimal | CLM with `content`, `epistemic_class`, `agent_id` |
| Standard | Minimal + CNF + at least one EVD |
| Full | Standard + PRV + VRF |
| Auditable | Full + all evidence `source_id` values resolvable + calibrated CNF + `valid_from`/`valid_until` set |

---

### 4. Speech-Act Envelope

The Speech-Act Envelope (SAE) wraps ASV epistemic content in a performative that declares communicative intent. The SAE uses commitment semantics (Singh) rather than mentalistic BDI semantics.

#### 4.1 The Six Performatives

| Performative | Illocutionary Force | Commitment Created | uACP Mapping |
|---|---|---|---|
| `INFORM` | Assert a proposition | Sender commits that the claim content is believed true. | TELL |
| `REQUEST` | Ask for action | Sender commits to processing the result. | ASK |
| `PROPOSE` | Suggest a course of action | No commitment until accepted by recipient. | TELL (commitment=provisional) |
| `CONFIRM` | Verify or acknowledge | Sender commits to agreement with the referenced claim. | TELL (with verification payload) |
| `WARN` | Flag a risk or constraint | Sender commits that the risk is non-trivial. | TELL (priority=elevated) |
| `QUERY` | Request information | Sender commits to processing the answer. | ASK |

The 6-performative set is a pragmatic superset of uACP's proven 4-verb basis {PING, TELL, ASK, OBSERVE}. PROPOSE and WARN are convenience extensions that do not extend expressive power but improve routing clarity.

#### 4.2 Envelope JSON Schema

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/sae.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Speech-Act Envelope",
  "description": "Wraps epistemic content in a performative declaring communicative intent.",
  "type": "object",
  "required": ["type", "id", "performative", "sender_id", "payload"],
  "properties": {
    "type": {
      "const": "SAE"
    },
    "id": {
      "type": "string",
      "format": "uri"
    },
    "performative": {
      "type": "string",
      "enum": ["INFORM", "REQUEST", "PROPOSE", "CONFIRM", "WARN", "QUERY"]
    },
    "sender_id": {
      "type": "string",
      "format": "uri",
      "description": "URI of the sending AGT."
    },
    "recipient_id": {
      "type": "string",
      "format": "uri",
      "description": "URI of the intended recipient AGT. MAY be omitted for broadcast."
    },
    "in_reply_to": {
      "type": "string",
      "format": "uri",
      "description": "URI of the SAE this message is responding to."
    },
    "conversation_id": {
      "type": "string",
      "format": "uri",
      "description": "Identifier grouping related SAEs into a conversation."
    },
    "payload": {
      "description": "The epistemic content. Typically a CLM or array of CLMs.",
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
    "created_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "additionalProperties": false
}
```

#### 4.3 Examples of Each Performative

**INFORM:**

```json
{
  "type": "SAE",
  "id": "urn:asv:sae:inform-001",
  "performative": "INFORM",
  "sender_id": "urn:asv:agent:research-01",
  "recipient_id": "urn:asv:agent:coordinator-01",
  "payload": {
    "type": "CLM",
    "id": "urn:asv:claim:analysis-complete-001",
    "content": "Statistical analysis of dataset X is complete. Primary finding: significant positive correlation (r=0.87, p<0.001).",
    "epistemic_class": "correlation",
    "agent_id": "urn:asv:agent:research-01",
    "confidence": {
      "type": "CNF", "id": "urn:asv:confidence:ic001", "value": 0.87, "method": "statistical",
      "calibration": { "status": "calibrated", "metric": "brier_score", "metric_value": 0.06, "calibration_date": "2025-11-01T00:00:00Z" }
    }
  },
  "created_at": "2026-03-09T10:00:00Z"
}
```

**REQUEST:**

```json
{
  "type": "SAE",
  "id": "urn:asv:sae:request-001",
  "performative": "REQUEST",
  "sender_id": "urn:asv:agent:coordinator-01",
  "recipient_id": "urn:asv:agent:verifier-02",
  "payload": {
    "type": "CLM",
    "id": "urn:asv:claim:verify-request-001",
    "content": "Please verify claim urn:asv:claim:temp-co2-correlation-001 by replicating the analysis.",
    "epistemic_class": "prescription",
    "agent_id": "urn:asv:agent:coordinator-01"
  },
  "created_at": "2026-03-09T10:05:00Z"
}
```

**PROPOSE:**

```json
{
  "type": "SAE",
  "id": "urn:asv:sae:propose-001",
  "performative": "PROPOSE",
  "sender_id": "urn:asv:agent:planner-01",
  "recipient_id": "urn:asv:agent:coordinator-01",
  "payload": {
    "type": "CLM",
    "id": "urn:asv:claim:workflow-proposal-001",
    "content": "Propose running a causal analysis using instrumental variables to test whether the correlation is causal.",
    "epistemic_class": "prescription",
    "agent_id": "urn:asv:agent:planner-01"
  },
  "created_at": "2026-03-09T10:10:00Z"
}
```

**CONFIRM:**

```json
{
  "type": "SAE",
  "id": "urn:asv:sae:confirm-001",
  "performative": "CONFIRM",
  "sender_id": "urn:asv:agent:verifier-02",
  "recipient_id": "urn:asv:agent:coordinator-01",
  "in_reply_to": "urn:asv:sae:request-001",
  "payload": {
    "type": "CLM",
    "id": "urn:asv:claim:verification-confirmed-001",
    "content": "Verification of claim urn:asv:claim:temp-co2-correlation-001 is confirmed. Replication yielded r=0.91.",
    "epistemic_class": "observation",
    "agent_id": "urn:asv:agent:verifier-02",
    "confidence": {
      "type": "CNF", "id": "urn:asv:confidence:vc001", "value": 0.95, "method": "statistical",
      "calibration": { "status": "calibrated", "metric": "brier_score", "metric_value": 0.04, "calibration_date": "2025-11-01T00:00:00Z" }
    }
  },
  "created_at": "2026-03-09T11:00:00Z"
}
```

**WARN:**

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
      "type": "CNF", "id": "urn:asv:confidence:wd001", "value": 0.88, "method": "statistical",
      "calibration": { "status": "calibrated", "metric": "ece", "metric_value": 0.03, "calibration_date": "2026-03-01T00:00:00Z" }
    }
  },
  "created_at": "2026-03-09T12:00:00Z"
}
```

**QUERY:**

```json
{
  "type": "SAE",
  "id": "urn:asv:sae:query-001",
  "performative": "QUERY",
  "sender_id": "urn:asv:agent:coordinator-01",
  "recipient_id": "urn:asv:agent:research-01",
  "payload": {
    "type": "CLM",
    "id": "urn:asv:claim:query-evidence-001",
    "content": "What evidence supports claim urn:asv:claim:temp-co2-correlation-001? Please provide all EVD objects.",
    "epistemic_class": "prescription",
    "agent_id": "urn:asv:agent:coordinator-01"
  },
  "created_at": "2026-03-09T12:30:00Z"
}
```

---

### 5. Claim Classification

#### 5.1 Epistemic Classes

| Class | Criteria | Example |
|---|---|---|
| `observation` | Directly witnessed or measured. No inference involved. | "Sensor reading at 14:00 UTC was 23.4 C." |
| `correlation` | Statistical association between two or more variables. | "Variables X and Y have Pearson r=0.87." |
| `causation` | Asserted causal relationship, typically supported by experimental or quasi-experimental evidence. | "Intervention A caused outcome B (RCT, p<0.01)." |
| `inference` | Conclusion derived from reasoning over other evidence. | "Given evidence E1 and E2, it follows that P." |
| `prediction` | Forward-looking assertion about future states. | "Revenue will increase 15% in Q2." |
| `prescription` | Normative recommendation about what should be done. | "The team should adopt strategy X." |

#### 5.2 Dual Classification

ASV classifies every message along two orthogonal dimensions:

1. **Speech-act type** (SAE performative): What communicative act is being performed?
2. **Epistemic class** (CLM epistemic_class): What kind of knowledge assertion is being made?

This produces a 6x6 matrix. Not all combinations are equally common.

**Common combinations:**

| | observation | correlation | causation | inference | prediction | prescription |
|---|---|---|---|---|---|---|
| INFORM | Common | Common | Common | Common | Rare | Rare |
| REQUEST | Rare | Rare | Rare | Rare | Rare | Common |
| PROPOSE | Rare | Rare | Rare | Rare | Rare | Common |
| CONFIRM | Common | Common | Common | Common | Rare | Rare |
| WARN | Common | Rare | Rare | Common | Common | Common |
| QUERY | Rare | Rare | Rare | Rare | Rare | Common |

All 36 combinations are structurally valid. Implementations MUST NOT reject a message solely because its speech-act/epistemic combination is uncommon.

---

### 6. Integration Protocols

#### 6.1 A2A Message Part Format

ASV types embed in A2A as structured data Parts within A2A Messages, or as Artifacts attached to A2A Tasks. No modifications to the A2A protocol are required.

**Schema for A2A Integration:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/a2a-part.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV A2A Message Part",
  "description": "An A2A Message Part containing ASV content.",
  "type": "object",
  "required": ["type", "content"],
  "properties": {
    "type": {
      "const": "application/asv+json"
    },
    "content": {
      "description": "The ASV object (SAE, CLM, or any ASV type).",
      "oneOf": [
        { "$ref": "https://asv.atrahasis.dev/vocab/v1/sae.schema.json" },
        { "$ref": "https://asv.atrahasis.dev/vocab/v1/clm.schema.json" },
        { "$ref": "https://asv.atrahasis.dev/vocab/v1/vrf.schema.json" }
      ]
    },
    "metadata": {
      "type": "object",
      "properties": {
        "asv_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
        "schema_uri": { "type": "string", "format": "uri" }
      }
    }
  }
}
```

**Complete A2A Example:**

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
                "calibration": { "status": "calibrated", "metric": "brier_score", "metric_value": 0.06, "calibration_date": "2025-11-01T00:00:00Z" }
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

**A2A Agent Card Extension:**

An A2A Agent Card declaring ASV support SHOULD include:

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

#### 6.2 MCP Tool Response Format

ASV types embed as structured content in MCP Tool responses. An MCP server declaring ASV support returns epistemically accountable results.

**Schema for MCP Integration:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/mcp-content.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV MCP Tool Response Content",
  "description": "Structured content block in an MCP Tool response containing ASV data.",
  "type": "object",
  "required": ["type", "asv"],
  "properties": {
    "type": {
      "const": "asv"
    },
    "asv": {
      "description": "The ASV object.",
      "oneOf": [
        { "$ref": "https://asv.atrahasis.dev/vocab/v1/clm.schema.json" },
        { "$ref": "https://asv.atrahasis.dev/vocab/v1/sae.schema.json" }
      ]
    },
    "asv_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    }
  }
}
```

**Complete MCP Example:**

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

#### 6.3 Standalone Document Format

ASV objects MAY be persisted as standalone JSON documents with the `.asv.json` file extension. This is the "objects not outputs" principle in practice.

**Schema:**

```json
{
  "$id": "https://asv.atrahasis.dev/vocab/v1/document.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ASV Document",
  "description": "A standalone ASV document containing one or more ASV objects.",
  "type": "object",
  "required": ["@context", "asv_version", "objects"],
  "properties": {
    "@context": {
      "const": "https://asv.atrahasis.dev/vocab/v1/context.jsonld"
    },
    "asv_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "document_id": {
      "type": "string",
      "format": "uri"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
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

**Example:**

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
        "type": "CNF", "id": "urn:asv:confidence:tc001", "value": 0.92, "method": "statistical",
        "calibration": { "status": "calibrated", "metric": "brier_score", "metric_value": 0.08, "calibration_date": "2025-12-01T00:00:00Z" }
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

### 7. JSON-LD Context

The ASV JSON-LD context maps ASV terms to ontology URIs, enabling interoperability with semantic web tooling without requiring ASV consumers to understand JSON-LD. Plain JSON consumers ignore `@context`; the schemas validate independently.

**Context Definition:**

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
    "role": "asv:role",
    "model": "asv:model",
    "capabilities": "asv:capabilities",
    "asv_version": "asv:version",

    "content": "asv:content",
    "epistemic_class": "asv:epistemicClass",
    "agent_id": {
      "@id": "prov:wasAttributedTo",
      "@type": "@id"
    },

    "value": "asv:confidenceValue",
    "interval": "asv:confidenceInterval",
    "distribution": "asv:confidenceDistribution",
    "method": "asv:method",
    "sample_size": "asv:sampleSize",
    "calibration": "asv:calibration",

    "quality_class": "asv:qualityClass",
    "source_type": "asv:sourceType",
    "source_id": {
      "@id": "prov:wasDerivedFrom",
      "@type": "@id"
    },
    "description": "schema:description",
    "retrieved_at": {
      "@id": "asv:retrievedAt",
      "@type": "xsd:dateTime"
    },

    "activity_type": "asv:activityType",
    "started_at": {
      "@id": "prov:startedAtTime",
      "@type": "xsd:dateTime"
    },
    "ended_at": {
      "@id": "prov:endedAtTime",
      "@type": "xsd:dateTime"
    },
    "used": {
      "@id": "prov:used",
      "@type": "@id",
      "@container": "@set"
    },
    "was_informed_by": {
      "@id": "prov:wasInformedBy",
      "@type": "@id",
      "@container": "@set"
    },
    "delegated_from": {
      "@id": "prov:actedOnBehalfOf",
      "@type": "@id"
    },

    "claim_id": {
      "@id": "asv:verifies",
      "@type": "@id"
    },
    "verifier_id": {
      "@id": "prov:wasAssociatedWith",
      "@type": "@id"
    },
    "status": "asv:verificationStatus",
    "verified_at": {
      "@id": "asv:verifiedAt",
      "@type": "xsd:dateTime"
    },
    "proof": "sec:proof",

    "performative": "asv:performative",
    "sender_id": {
      "@id": "asv:sender",
      "@type": "@id"
    },
    "recipient_id": {
      "@id": "asv:recipient",
      "@type": "@id"
    },
    "in_reply_to": {
      "@id": "asv:inReplyTo",
      "@type": "@id"
    },
    "conversation_id": {
      "@id": "asv:conversationId",
      "@type": "@id"
    },
    "payload": "asv:payload",
    "priority": "asv:priority",

    "rebuts_claims": {
      "@id": "asv:rebuts",
      "@type": "@id",
      "@container": "@set"
    },
    "valid_from": {
      "@id": "prov:generatedAtTime",
      "@type": "xsd:dateTime"
    },
    "valid_until": {
      "@id": "prov:invalidatedAtTime",
      "@type": "xsd:dateTime"
    },
    "created_at": {
      "@id": "schema:dateCreated",
      "@type": "xsd:dateTime"
    },
    "subject": "asv:subject",
    "object": "asv:object"
  }
}
```

**Namespace:** `https://asv.atrahasis.dev/vocab/v1#` (abbreviated `asv:`).

**Relationship to existing ontologies:**

| ASV Namespace | Maps To |
|---|---|
| `asv:` | ASV-specific terms with no existing standard equivalent (CNF, epistemic_class, performative, etc.) |
| `prov:` | W3C PROV-O terms for provenance (Agent, Activity, Entity, used, wasGeneratedBy, etc.) |
| `schema:` | Schema.org terms for general metadata (name, description, dateCreated) |
| `sec:` | W3C Security Vocabulary for cryptographic proof |
| `xsd:` | XML Schema datatypes for date-time values |

---

### 8. Semantic Specification (Summary)

The following semantic contracts cannot be expressed in JSON Schema and MUST be documented in the companion Semantic Specification. This section summarizes what that document covers; it does not replace it.

#### 8.1 What JSON Schema Cannot Express

1. **Epistemic semantics of confidence methods.** What `"method": "statistical"` means (frequentist analysis with stated significance level) vs `"method": "consensus"` (agreement among N agents) is interpretation, not structure. The semantic spec defines each method.

2. **Operation class composition algebra.** When agent outputs compose (e.g., an inference built on a correlation built on observations), how confidence propagates depends on composition rules (M+V=X; M+M=M; B+anything=B). These algebraic rules cannot be expressed as JSON Schema constraints.

3. **Graph referential integrity.** `agent_id` references MUST resolve to AGT objects; `claim_id` on VRF MUST resolve to CLM objects; `source_id` on EVD SHOULD resolve to an identifiable resource. JSON Schema validates documents, not graphs.

4. **Calibration requirements.** What constitutes acceptable calibration (minimum sample size, maximum ECE, recalibration frequency) is domain-dependent and defined in the semantic spec.

5. **Commitment lifecycle.** When a CONFIRM performative is sent, the sender's commitment to the confirmed claim becomes binding. How commitments are tracked, revoked, and audited is a semantic contract.

6. **Evidence weight interpretation.** How quality classes translate to numerical weights for downstream reasoning is application-dependent but the semantic spec provides normative defaults.

#### 8.2 Key Semantic Rules

The semantic spec MUST document at minimum:

1. Definitions of all five confidence methods with examples.
2. Definitions of all five evidence quality classes with examples.
3. Commitment semantics for each of the six performatives.
4. Rules for temporal validity expiration handling.
5. Rules for rebuttal chain interpretation.
6. Calibration protocol including minimum requirements for `calibrated` status.
7. Referential integrity constraints with resolution procedures.

The semantic specification is capped at 50 pages (per Assessment Council REQ-4).

---

### 9. Confidence Calibration Protocol

This section addresses Assessment Council REQ-3.

#### 9.1 Calibration Metadata Schema

Every CNF object SHOULD include a `calibration` object. The calibration object schema is defined in Section 2.3 above.

#### 9.2 Calibration Levels

| Level | Requirements |
|---|---|
| `uncalibrated` | Raw model output. No empirical validation. |
| `self_reported` | Agent estimates its own accuracy. No external validation. |
| `calibrated` | Validated against a held-out dataset. `dataset_id`, `calibration_date`, `metric`, and `metric_value` MUST be present. |

#### 9.3 Drift Detection

Conforming implementations SHOULD monitor calibration drift by:

1. Tracking `metric_value` over time for each agent.
2. Flagging agents whose calibration metric degrades by more than 50% from their baseline.
3. When drift is detected, generating a WARN SAE (see Section 4.3 WARN example).

#### 9.4 Consumer Guidance

- When `calibration.status` is `uncalibrated`, consumers SHOULD NOT use the confidence value for automated decision-making without human review.
- When `calibration.status` is `calibrated` but `calibration_date` is more than 90 days old, consumers SHOULD treat the calibration as potentially stale.
- When `calibration.metric` is `ece` (Expected Calibration Error), values below 0.05 indicate well-calibrated confidence; values above 0.15 indicate poor calibration.

---

### 10. Configurable Parameters

All configurable values with their defaults:

| Parameter | Default | Description |
|---|---|---|
| `asv.validation.strict_mode` | `false` | When true, all SHOULD-level requirements become MUST. |
| `asv.confidence.require_calibration` | `false` | When true, CNF objects without `calibration` are rejected. |
| `asv.confidence.max_uncalibrated_value` | `1.0` | Maximum allowed confidence value for uncalibrated CNF objects. Set to 0.7 to force conservatism. |
| `asv.temporal.expiry_check_interval` | `3600` | Seconds between temporal validity expiry scans. |
| `asv.temporal.auto_flag_expired` | `true` | Automatically flag expired claims for re-verification. |
| `asv.evidence.min_per_chain` | `0` | Minimum evidence items required per epistemic chain. Set to 1 for Standard conformance. |
| `asv.calibration.stale_days` | `90` | Days after which calibration metadata is considered stale. |
| `asv.calibration.drift_threshold` | `0.5` | Proportional degradation in calibration metric that triggers a drift alert. |
| `asv.envelope.require_recipient` | `false` | When true, SAE objects must specify `recipient_id`. |
| `asv.chain.require_provenance` | `false` | When true, CLM objects must include PRV. Set to true for Full conformance. |

---

### 11. Conformance Requirements

#### 11.1 Conformance Levels

ASV defines three conformance levels:

**Basic Conformance:**

An implementation achieves Basic conformance if it:

1. MUST validate all ASV objects against the JSON Schema definitions in this specification.
2. MUST correctly discriminate ASV types using the `type` field.
3. MUST accept and produce all seven ASV type values (AGT, CLM, CNF, EVD, PRV, VRF, SAE).
4. MUST validate that `id` fields are present and are valid URIs.
5. MUST validate required fields per each type's schema.

**Standard Conformance:**

An implementation achieves Standard conformance if it satisfies Basic and additionally:

1. MUST validate the epistemic chain composition (CLM contains valid CNF, EVD, PRV objects).
2. MUST validate that `confidence.value` falls within `confidence.interval` when both are present.
3. MUST validate that `distribution` probabilities sum to 1.0 (within tolerance of 0.001).
4. MUST validate temporal validity constraints (`valid_from` <= `valid_until`).
5. SHOULD implement referential integrity checks (agent_id resolves to AGT, claim_id resolves to CLM).
6. SHOULD implement calibration status warnings for uncalibrated CNF objects.

**Full Conformance:**

An implementation achieves Full conformance if it satisfies Standard and additionally:

1. MUST implement referential integrity checks across all cross-references.
2. MUST implement temporal validity expiry detection and flagging.
3. MUST implement calibration drift monitoring.
4. MUST validate the semantic contracts defined in the companion Semantic Specification.
5. MUST support all three integration formats (A2A, MCP, standalone document).
6. MUST implement commitment tracking for SAE performatives.

#### 11.2 Test Vectors

The following test vectors validate conformance. Each vector specifies an input, expected validation result, and the conformance level it tests.

**TV-1: Valid minimal CLM (Basic)**

Input:
```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-001",
  "content": "Test claim.",
  "epistemic_class": "observation",
  "agent_id": "urn:asv:agent:test-01"
}
```
Expected: VALID

**TV-2: Missing required field (Basic)**

Input:
```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-002",
  "content": "Test claim."
}
```
Expected: INVALID (missing `epistemic_class` and `agent_id`)

**TV-3: Invalid epistemic class (Basic)**

Input:
```json
{
  "type": "CLM",
  "id": "urn:asv:claim:test-003",
  "content": "Test claim.",
  "epistemic_class": "guess",
  "agent_id": "urn:asv:agent:test-01"
}
```
Expected: INVALID (`"guess"` is not a valid epistemic_class)

**TV-4: Confidence value outside interval (Standard)**

Input:
```json
{
  "type": "CNF",
  "id": "urn:asv:confidence:test-004",
  "value": 0.95,
  "interval": [0.80, 0.90],
  "method": "statistical"
}
```
Expected: INVALID (value 0.95 outside interval [0.80, 0.90])

**TV-5: Distribution probabilities do not sum to 1 (Standard)**

Input:
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
Expected: INVALID (probabilities sum to 0.8, not 1.0)

**TV-6: Temporal validity violation (Standard)**

Input:
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
Expected: INVALID (valid_from after valid_until)

**TV-7: Complete epistemic chain (Full)**

Input: The complete example in Section 12, Example 2.
Expected: VALID at all conformance levels.

---

### 12. Complete Examples

#### Example 1: Simple Claim with Confidence

A minimal claim with confidence -- the simplest useful ASV object.

```json
{
  "type": "CLM",
  "id": "urn:asv:claim:simple-001",
  "content": "The Python package 'requests' version 2.31.0 has no known critical CVEs as of March 2026.",
  "epistemic_class": "observation",
  "agent_id": "urn:asv:agent:security-scanner-01",
  "confidence": {
    "type": "CNF",
    "id": "urn:asv:confidence:simple-001-cnf",
    "value": 0.94,
    "method": "computational_result",
    "calibration": {
      "status": "calibrated",
      "dataset_id": "urn:asv:dataset:nvd-benchmark-2026",
      "calibration_date": "2026-02-01T00:00:00Z",
      "metric": "brier_score",
      "metric_value": 0.05
    }
  },
  "valid_until": "2026-04-09T00:00:00Z",
  "created_at": "2026-03-09T10:00:00Z"
}
```

#### Example 2: Full Epistemic Chain (CLM + CNF + EVD + PRV + VRF)

A complete, auditable epistemic record demonstrating all chain elements.

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
      "calibration": { "status": "calibrated", "metric": "brier_score", "metric_value": 0.03, "calibration_date": "2026-01-01T00:00:00Z" }
    }
  },
  "valid_from": "2026-02-20T14:00:00Z",
  "valid_until": "2027-02-20T14:00:00Z",
  "created_at": "2026-02-15T11:30:00Z"
}
```

#### Example 3: Rebuttal Chain

An agent disputes a prior claim with counter-evidence.

```json
{
  "type": "SAE",
  "id": "urn:asv:sae:rebuttal-inform-001",
  "performative": "INFORM",
  "sender_id": "urn:asv:agent:critic-01",
  "recipient_id": "urn:asv:agent:coordinator-01",
  "payload": {
    "type": "CLM",
    "id": "urn:asv:claim:rebuttal-drug-001",
    "content": "The 2.3x bleeding risk increase for warfarin+aspirin may be overstated. A 2025 real-world evidence study using propensity-matched cohorts found a risk ratio of 1.6x (95% CI: 1.2-2.1), suggesting the RCT population is not representative of typical clinical use.",
    "epistemic_class": "inference",
    "agent_id": "urn:asv:agent:critic-01",
    "rebuts_claims": ["urn:asv:claim:drug-interaction-001"],
    "confidence": {
      "type": "CNF",
      "id": "urn:asv:confidence:rebuttal-drug-cnf",
      "value": 0.68,
      "interval": [0.55, 0.78],
      "method": "statistical",
      "sample_size": 45000,
      "calibration": { "status": "uncalibrated" }
    },
    "evidence": [
      {
        "type": "EVD",
        "id": "urn:asv:evidence:rwe-study-001",
        "quality_class": "direct_observation",
        "source_type": "document",
        "source_id": "urn:asv:document:nejm-rwe-2025-1234",
        "description": "Real-world evidence study published in NEJM, propensity-matched cohort of 45,000 patients.",
        "retrieved_at": "2026-03-01T09:00:00Z"
      }
    ],
    "created_at": "2026-03-05T10:00:00Z"
  },
  "created_at": "2026-03-05T10:05:00Z"
}
```

#### Example 4: A2A Integration

See Section 6.1 for the complete A2A example.

#### Example 5: MCP Integration

See Section 6.2 for the complete MCP example.

---

### Appendix A: Schema File Inventory

| File | URI | Description |
|---|---|---|
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

### Appendix B: Invention Claim Scope (REQ-1 Compliance)

Per Assessment Council REQ-1 (Narrow the Invention Claim), ASV's components are categorized:

**Genuinely Novel:**
- Claim classification taxonomy (epistemic_class: observation, correlation, causation, inference, prediction, prescription)
- Dual classification framework (speech-act type x epistemic class)
- Structured confidence primitive (CNF) with declared method and calibration metadata

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

### Appendix C: Assessment Council Condition Traceability

| Condition | ID | Status | Where Addressed |
|---|---|---|---|
| Working Implementation Before Full Spec | GATE-1 | PENDING | Implementation phase; schema definitions in this spec enable validation |
| LLM Generation Accuracy | GATE-2 | PENDING | Experiment 3; schemas designed for LLM-friendly generation |
| Provenance Chain Utility | GATE-3 | PENDING | Experiment 5; chain structure defined in Section 3 |
| Narrow Invention Claim | REQ-1 | ADDRESSED | Appendix B |
| Kill AACP as Separate Protocol | REQ-2 | ADDRESSED | Section 1.3, Section 6 (A2A/MCP integration only) |
| Address Confidence Calibration | REQ-3 | ADDRESSED | Section 2.3, Section 9 |
| Semantic Spec Cap (50 pages) | REQ-4 | ADDRESSED | Section 8 (summary only; full spec separate) |
| Regulated Industry Engagement | REC-1 | PENDING | Example 2 demonstrates healthcare use case |
| A2A Specification Monitoring | REC-2 | PENDING | Operational concern; noted in Section 1.3 |

---

*Specification draft completed 2026-03-09.*
*ASV Technical Specification v0.1.0-draft.*
*Atrahasis Agent System -- C4-A DESIGN Phase.*
