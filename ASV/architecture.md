# ASV -- System Architecture
## C4-A DESIGN Document

**Invention:** C4-A ASV (AASL Semantic Vocabulary) -- Epistemic Accountability Layer
**Status:** DESIGN (following CONDITIONAL_ADVANCE verdict)
**Date:** 2026-03-09
**Feasibility Score:** 4/5 | **Novelty:** 3/5 | **Risk:** MEDIUM (5/10)

---

### 1. Architecture Overview

#### 1.1 Design Philosophy

ASV is governed by three non-negotiable principles derived from the Assessment Council deliberation:

1. **Vocabulary, not protocol.** ASV defines JSON Schema types and a JSON-LD context. It defines no transport, no connection management, no message routing, no task lifecycle. Those responsibilities belong to A2A and MCP. ASV occupies the semantic layer between application logic (above) and transport protocols (below).

2. **Code before spec.** The first deliverable is a working Python/TypeScript validator library with integration examples, not a specification document. The schema is the test suite. The semantic specification follows implementation, not the reverse. This directly addresses the FIPA/KQML failure mode of death-by-specification.

3. **Narrow invention claim.** ASV claims novelty only for: (a) the claim classification taxonomy for epistemic assertion types, (b) dual classification combining speech-act type with epistemic claim type, and (c) the structured confidence primitive (CNF) with declared methods and calibration metadata. All other components -- provenance extending W3C PROV, verification aligned with W3C VC, JSON Schema delivery, JSON-LD context -- are acknowledged as applications of existing standards.

#### 1.2 What ASV Is

ASV is a set of seven JSON Schema type definitions and a companion JSON-LD context that encode the epistemic accountability chain: CLM (Claim), CNF (Confidence), EVD (Evidence), PRV (Provenance), VRF (Verification), AGT (Agent), and SAE (Speech-Act Envelope). These types compose into a chain where every claim carries structured confidence, linked evidence, grounded provenance, and verification records -- wrapped in a speech-act envelope declaring communicative intent.

#### 1.3 What ASV Is Not

- Not a protocol. A2A and MCP handle transport.
- Not a runtime. ASV objects are validated and stored; execution is the consumer's responsibility.
- Not a replacement for W3C PROV. ASV extends PROV-O following the PROV-AGENT (2025) precedent.
- Not a replacement for AASL. ASV extracts AASL's semantic innovations; the broader AASL type system (agents, tasks, workflows, tools, policies) remains separate.
- Not AACP. AACP is formally retired (REQ-2). The protocol is A2A/MCP.

#### 1.4 Relationship to Standards

| Standard | Relationship |
|----------|-------------|
| W3C PROV-O | ASV PRV extends prov:Activity; CLM extends prov:Entity; AGT extends prov:Agent |
| W3C VC 2.0 | ASV VRF aligns with Data Integrity proofs; CLM structure informed by credentialSubject |
| FIPA ACL | ASV SAE performatives derive from FIPA's 20+ acts, reduced to 6 via uACP completeness proof |
| JSON Schema Draft 2020-12 | ASV types are defined as a JSON Schema vocabulary with URI-identified keywords |
| JSON-LD 1.1 | ASV provides a @context mapping terms to PROV-O and ASV namespace URIs |
| Google A2A | ASV types embed in A2A Message Parts and Task Artifacts |
| Anthropic MCP | ASV types embed in MCP Tool response structured content |

---

### 2. Hard Gate Experiments

These three gates are kill-or-continue checkpoints mandated by the Assessment Council. Failure at any gate halts advancement.

#### 2.1 HG-1: Implementation Sprint (GATE-1)

**Objective:** Ship a working Python/TypeScript validator library that processes ASV-typed JSON messages and integrates with at least one existing protocol (A2A or MCP) before writing the full semantic specification.

**6-Week Sprint Deliverables:**
1. JSON Schema files for all 7 core types (CLM, CNF, EVD, PRV, VRF, AGT, SAE)
2. JSON-LD @context document mapping ASV terms to PROV-O and FIPA ontology URIs
3. Python reference validator (`pip install asv-validator`): schema validation + basic semantic checks
4. TypeScript reference validator (`npm install asv-validator`): schema validation + basic semantic checks
5. Three integration examples:
   - A2A Task with ASV Artifacts (multi-agent claim with provenance)
   - MCP Tool response with ASV structured content (confidence-rated tool output)
   - Standalone ASV document (regulatory audit trail record)
6. Ten example ASV objects covering all 7 types and 6 performatives

**Success Criteria:**
- Schema validation adds <10ms overhead per message at typical sizes (1-10KB)
- A2A/MCP integration uses existing extensibility mechanisms with zero protocol modifications
- All 10 example objects validate against the published schemas

**Kill Criteria:**
- Validation overhead >10ms per message
- Integration requires protocol modifications to A2A or MCP
- Schemas cannot represent the full CLM-CNF-EVD-PRV-VRF chain as composed types

#### 2.2 HG-2: LLM Generation Accuracy (GATE-2)

**Objective:** Demonstrate that LLMs can generate valid ASV objects from natural language descriptions at >80% structural validity.

**Test Methodology:**
1. Define a prompt template that describes a scenario and asks for an ASV-typed JSON response
2. Prompt three models (Claude, GPT-4, Gemini) to generate 100 CLM-CNF-EVD-PRV-VRF chains each
3. Validate each output against the ASV JSON Schemas
4. Measure structural validity (passes schema validation) and semantic plausibility (human-judged)
5. Compare single-step generation vs. two-step generation (free reasoning then structured formatting)

**Benchmark Design:**

| Metric | Target | Minimum |
|--------|--------|---------|
| Structural validity (individual types) | >90% | >80% |
| Structural validity (full nested chain) | >80% | >70% |
| Semantic plausibility (human-judged) | >70% | >60% |
| Two-step generation structural validity | >95% | >90% |

**Kill Criteria:**
- Structural validity below 80% across all three models for individual types
- Structural validity below 70% for the full nested CLM-CNF-EVD-PRV-VRF chain
- If killed: simplify vocabulary, decompose chain into independently usable components

#### 2.3 HG-3: Provenance Chain Utility (GATE-3)

**Objective:** Demonstrate that the full ASV epistemic chain produces >20% improvement in error detection over simple source attribution.

**What to Measure:**
- Error detection rate: percentage of injected errors caught before reaching end consumers
- Error propagation distance: number of downstream agents affected before detection
- Time to root cause: minutes from error detection to identification of the originating agent/claim
- False positive rate: percentage of non-errors flagged as errors

**Baseline Comparison Methodology:**
1. Build a multi-agent fact-checking pipeline (minimum 4 agents in chain)
2. Inject deliberate errors (factual inaccuracies, inflated confidence, fabricated evidence) at known points
3. Run three conditions:
   - **Control:** No provenance metadata (natural language only)
   - **Simple attribution:** Source agent ID and timestamp only
   - **Full ASV chain:** CLM-CNF-EVD-PRV-VRF with evidence quality typing

**Success Criteria:**
- Full ASV chain shows >20% improvement in error detection rate vs. simple attribution
- Error propagation distance reduced by >30% vs. control
- False positive rate <10%

**Kill Criteria:**
- Error detection improvement <20% vs. simple source attribution
- If killed: extract claim classification taxonomy and dual classification as standalone contributions; do not pursue integrated vocabulary

---

### 3. ASV Core Components

These are the genuinely novel components that constitute ASV's invention claim, plus the standards-based components that complete the chain.

#### 3.1 Epistemic Accountability Chain (CLM-CNF-EVD-PRV-VRF)

The chain models the epistemic lifecycle of a knowledge assertion:

```
SAE (Speech-Act Envelope)
 +-- performative: INFORM | REQUEST | PROPOSE | CONFIRM | WARN | QUERY
 +-- CLM (Claim)
      +-- claim_type: speech-act classification
      +-- epistemic_class: knowledge-type classification
      +-- CNF (Confidence)
      |    +-- value / interval / distribution
      |    +-- method: statistical | consensus | model_derived | human_judged
      |    +-- calibration metadata
      +-- EVD[] (Evidence)
      |    +-- quality_class: direct_observation | inference | hearsay | computational_result | delegation
      |    +-- source references
      |    +-- temporal validity
      +-- PRV (Provenance)
      |    +-- agent reference (prov:Agent)
      |    +-- activity trace (prov:Activity)
      |    +-- delegation chain (prov:actedOnBehalfOf)
      +-- VRF (Verification)
           +-- status: verified | unverified | disputed | expired
           +-- method: consensus | replication | statistical | cryptographic
           +-- verifier references
```

**Composition Rules:**
- A CLM MUST contain exactly one CNF.
- A CLM MAY contain zero or more EVD objects.
- A CLM MAY contain zero or one PRV object (provenance is optional for lightweight claims).
- A CLM MAY contain zero or one VRF object.
- An SAE MUST contain exactly one CLM.
- All objects MAY be referenced by stable URI-based identifiers for cross-document linking.

**Example: Complete Chain**

```json
{
  "@context": "https://asv.atrahasis.org/v1/context.jsonld",
  "type": "SAE",
  "id": "urn:asv:sae:msg-20260309-001",
  "performative": "INFORM",
  "commitment": "sender_asserts_truth",
  "claim": {
    "type": "CLM",
    "id": "urn:asv:clm:corr-temp-co2-001",
    "claim_type": "INFORM",
    "epistemic_class": "correlation",
    "subject": "global_temperature",
    "predicate": "correlates_with",
    "object": "atmospheric_co2",
    "statement": "Global surface temperature shows strong positive correlation with atmospheric CO2 concentration (r=0.92, p<0.001) over the period 1960-2025.",
    "valid_from": "2026-03-09T00:00:00Z",
    "valid_until": "2027-03-09T00:00:00Z",
    "rebuts_claim": [],
    "confidence": {
      "type": "CNF",
      "id": "urn:asv:cnf:corr-temp-co2-001",
      "representation": "point",
      "value": 0.92,
      "interval": {
        "low": 0.88,
        "high": 0.95,
        "level": 0.95
      },
      "method": "statistical",
      "calibration": {
        "calibrated": true,
        "dataset_id": "urn:asv:ds:calibration-2026q1",
        "calibration_date": "2026-01-15T00:00:00Z",
        "metric": "brier_score",
        "metric_value": 0.08
      }
    },
    "evidence": [
      {
        "type": "EVD",
        "id": "urn:asv:evd:noaa-climate-2025",
        "quality_class": "direct_observation",
        "source_type": "dataset_reference",
        "source_id": "urn:asv:ds:noaa-global-temp-2025",
        "description": "NOAA Global Surface Temperature Dataset, annual averages 1960-2025",
        "valid_from": "1960-01-01T00:00:00Z",
        "valid_until": "2025-12-31T23:59:59Z",
        "rebuttal_support": false
      },
      {
        "type": "EVD",
        "id": "urn:asv:evd:keeling-co2-2025",
        "quality_class": "direct_observation",
        "source_type": "dataset_reference",
        "source_id": "urn:asv:ds:keeling-curve-2025",
        "description": "Mauna Loa CO2 measurements, monthly averages 1960-2025",
        "valid_from": "1960-01-01T00:00:00Z",
        "valid_until": "2025-12-31T23:59:59Z",
        "rebuttal_support": false
      }
    ],
    "provenance": {
      "type": "PRV",
      "id": "urn:asv:prv:corr-analysis-001",
      "prov:wasGeneratedBy": {
        "activity_id": "urn:asv:act:pearson-correlation-run",
        "activity_type": "statistical_analysis",
        "started_at": "2026-03-09T10:15:00Z",
        "ended_at": "2026-03-09T10:15:03Z"
      },
      "prov:wasAttributedTo": "urn:asv:agt:research-agent-01",
      "prov:used": [
        "urn:asv:ds:noaa-global-temp-2025",
        "urn:asv:ds:keeling-curve-2025"
      ],
      "delegation_chain": []
    },
    "verification": {
      "type": "VRF",
      "id": "urn:asv:vrf:corr-temp-co2-001",
      "status": "verified",
      "method": "replication",
      "verifiers": [
        "urn:asv:agt:verification-agent-02",
        "urn:asv:agt:verification-agent-03"
      ],
      "verified_at": "2026-03-09T11:00:00Z",
      "result": {
        "replicated_value": 0.91,
        "within_tolerance": true
      }
    }
  }
}
```

#### 3.2 Confidence Primitive (CNF)

CNF is ASV's most novel component. No existing standard provides structured confidence representation for agent communication claims.

**Three Representation Modes:**

1. **Point estimate:** A single value in [0, 1] with declared method.
2. **Interval:** Low/high bounds with a confidence level (e.g., 95% CI).
3. **Distribution:** Discrete distribution over named outcomes.

```json
{
  "type": "CNF",
  "id": "urn:asv:cnf:prediction-001",
  "representation": "distribution",
  "distribution": [
    { "outcome": "market_up", "probability": 0.45 },
    { "outcome": "market_stable", "probability": 0.35 },
    { "outcome": "market_down", "probability": 0.20 }
  ],
  "method": "model_derived",
  "calibration": {
    "calibrated": false,
    "warning": "Model-reported probabilities; no empirical calibration performed"
  }
}
```

**Calibration Requirements (addressing Adversarial Probe C):**

The Assessment Council mandated (REQ-3) that ASV address confidence calibration explicitly. CNF objects MUST include:

1. **method** (REQUIRED): One of `statistical`, `consensus`, `model_derived`, `human_judged`. Declares how the confidence value was produced.
2. **calibration.calibrated** (REQUIRED): Boolean indicating whether empirical calibration has been performed.
3. **calibration.warning** (REQUIRED when calibrated=false): Human-readable warning that the confidence value has not been empirically validated.
4. **calibration.dataset_id** (REQUIRED when calibrated=true): Identifier of the calibration holdout dataset.
5. **calibration.metric** (RECOMMENDED when calibrated=true): Calibration metric used (e.g., Brier score, expected calibration error).

This design distinguishes model-reported confidence (which LLMs produce poorly) from empirically validated confidence (which requires external measurement). Downstream consumers can filter on `calibration.calibrated` to decide how much weight to assign.

**Uncalibrated CNF Example:**

```json
{
  "type": "CNF",
  "id": "urn:asv:cnf:llm-estimate-001",
  "representation": "point",
  "value": 0.85,
  "method": "model_derived",
  "calibration": {
    "calibrated": false,
    "warning": "LLM self-reported confidence. Studies show LLM confidence estimates may have <0.3 correlation with actual accuracy. Treat as ordinal ranking, not calibrated probability."
  }
}
```

#### 3.3 Claim Classification Taxonomy

This is ASV's second genuinely novel component: dual classification combining speech-act type with epistemic nature.

**Speech-Act Classification (what communicative act is being performed):**

The 6 performatives, grounded in FIPA ACL tradition and constrained by the uACP completeness proof (4 verbs suffice; ASV adds 2 convenience extensions):

| Performative | Illocutionary Force | Commitment Created | uACP Mapping |
|-------------|--------------------|--------------------|--------------|
| INFORM | Assert a proposition | Sender commits that claim is believed true | TELL |
| REQUEST | Ask for action | Sender commits to processing the result | ASK |
| PROPOSE | Suggest a course of action | No commitment until accepted | TELL (commitment=provisional) |
| CONFIRM | Verify/acknowledge | Sender commits to agreement | TELL (with verification payload) |
| WARN | Flag a risk or constraint | Sender commits that risk is non-trivial | TELL (priority=elevated) |
| QUERY | Request information | Sender commits to processing the answer | ASK |

**Epistemic Classification (what kind of knowledge claim is being made):**

| Epistemic Class | Definition | Verification Approach |
|----------------|------------|----------------------|
| observation | Direct measurement or sensor reading | Compare against source data |
| correlation | Statistical association between variables | Replicate analysis on same/different data |
| causation | Causal mechanism asserted | Experimental or counterfactual validation |
| inference | Logical deduction from premises | Verify premises and reasoning chain |
| prediction | Future state forecast | Evaluate against outcomes when available |
| normative | Value judgment or recommendation | Assess against stated criteria/policy |

**Dual Classification Example:**

```json
{
  "type": "SAE",
  "performative": "WARN",
  "commitment": "sender_asserts_risk_nontrivial",
  "claim": {
    "type": "CLM",
    "claim_type": "WARN",
    "epistemic_class": "prediction",
    "statement": "Server cluster utilization will exceed 95% within 48 hours based on current growth trajectory.",
    "confidence": {
      "type": "CNF",
      "representation": "interval",
      "interval": { "low": 0.72, "high": 0.89, "level": 0.90 },
      "method": "statistical",
      "calibration": { "calibrated": true, "dataset_id": "urn:asv:ds:capacity-forecast-cal-2026q1", "calibration_date": "2026-02-01T00:00:00Z", "metric": "coverage", "metric_value": 0.91 }
    },
    "evidence": [
      {
        "type": "EVD",
        "quality_class": "computational_result",
        "source_type": "model_output",
        "source_id": "urn:asv:model:capacity-forecast-v3",
        "description": "Linear extrapolation from 30-day utilization trend"
      }
    ]
  }
}
```

This message carries two independent classifications: it is a WARN (speech-act: flagging risk) carrying a PREDICTION (epistemic: future state forecast). No existing agent communication system can natively represent both dimensions simultaneously.

#### 3.4 Evidence Quality Typing

EVD objects declare their quality class, enabling downstream agents to weight evidence appropriately. The 5 quality classes, derived from epistemology and argumentation theory:

| Quality Class | Definition | Typical Weight |
|--------------|------------|----------------|
| direct_observation | First-hand measurement, sensor data, direct API response | Highest |
| inference | Logical derivation from other evidence | High |
| computational_result | Output of a model, simulation, or algorithm | Medium-High |
| hearsay | Reported by another agent without independent verification | Medium-Low |
| delegation | Result delegated to a sub-agent whose methods are opaque | Low |

**Rebuttal Support (Toulmin-complete):**

CLM objects include an optional `rebuts_claim` field containing an array of claim IDs that the current claim disputes. A rebuttal carries its own full CLM-CNF-EVD-PRV-VRF chain.

```json
{
  "type": "CLM",
  "id": "urn:asv:clm:rebuttal-001",
  "epistemic_class": "observation",
  "statement": "The correlation between temperature and CO2 disappears when controlling for solar irradiance variation.",
  "rebuts_claim": ["urn:asv:clm:corr-temp-co2-001"],
  "confidence": {
    "type": "CNF",
    "representation": "point",
    "value": 0.43,
    "method": "statistical",
    "calibration": { "calibrated": true, "dataset_id": "urn:asv:ds:solar-control-cal", "calibration_date": "2026-03-01T00:00:00Z", "metric": "brier_score", "metric_value": 0.22 }
  },
  "evidence": [
    {
      "type": "EVD",
      "quality_class": "computational_result",
      "source_type": "analysis_output",
      "source_id": "urn:asv:analysis:partial-correlation-solar",
      "description": "Partial correlation analysis controlling for total solar irradiance"
    }
  ]
}
```

**Temporal Validity:**

CLM and EVD objects carry optional `valid_from` and `valid_until` timestamps (RFC 3339). Claims without temporal bounds are treated as indefinitely valid. Claims with expired `valid_until` are automatically flagged for re-verification.

```json
{
  "type": "CLM",
  "statement": "Current API rate limit for service X is 1000 req/min",
  "epistemic_class": "observation",
  "valid_from": "2026-03-01T00:00:00Z",
  "valid_until": "2026-04-01T00:00:00Z"
}
```

---

### 4. Integration Architecture

ASV is delivered through three integration surfaces. All three use the same JSON Schema types -- the only difference is the transport envelope.

#### 4.1 A2A Integration

ASV types embed in A2A Message Parts and Task Artifacts using A2A's existing extensibility mechanisms. No protocol modifications are required.

**Embedding Pattern:** ASV objects are carried as structured data Parts within A2A Messages, with `type: "application/json"` and an ASV schema reference.

**Agent Card Extension:** An A2A Agent Card declares ASV vocabulary support as a capability:

```json
{
  "name": "Research Agent",
  "capabilities": {
    "asv": {
      "version": "1.0",
      "supported_types": ["CLM", "CNF", "EVD", "PRV", "VRF", "SAE"],
      "performatives": ["INFORM", "QUERY", "CONFIRM"]
    }
  }
}
```

**Example: A2A Message with ASV Part**

```json
{
  "role": "agent",
  "parts": [
    {
      "type": "text",
      "text": "Analysis complete. Temperature-CO2 correlation is strong."
    },
    {
      "type": "data",
      "mimeType": "application/asv+json",
      "data": {
        "type": "SAE",
        "performative": "INFORM",
        "claim": {
          "type": "CLM",
          "epistemic_class": "correlation",
          "statement": "Temperature correlates with CO2 (r=0.92)",
          "confidence": {
            "type": "CNF",
            "representation": "point",
            "value": 0.92,
            "method": "statistical",
            "calibration": { "calibrated": true, "dataset_id": "urn:asv:ds:cal-001", "calibration_date": "2026-01-15T00:00:00Z", "metric": "brier_score", "metric_value": 0.08 }
          }
        }
      }
    }
  ]
}
```

**Task Artifacts:** When an A2A Task completes, ASV objects attached as Artifacts become durable, identity-bearing semantic objects -- the "objects not outputs" principle in practice.

#### 4.2 MCP Integration

ASV types embed in MCP Tool responses as structured content. An MCP server declaring ASV support returns epistemically accountable results.

**Server Capability Declaration:**

```json
{
  "name": "financial-data-tool",
  "version": "1.0",
  "capabilities": {
    "asv": {
      "version": "1.0",
      "output_types": ["CLM", "CNF", "EVD"]
    }
  }
}
```

**Example: MCP Tool Response with ASV**

```json
{
  "content": [
    {
      "type": "text",
      "text": "Retrieved quarterly revenue data for ACME Corp."
    },
    {
      "type": "resource",
      "resource": {
        "uri": "asv://financial-data/acme-q4-2025",
        "mimeType": "application/asv+json",
        "text": "{\"type\":\"CLM\",\"epistemic_class\":\"observation\",\"statement\":\"ACME Corp Q4 2025 revenue was $2.3B\",\"confidence\":{\"type\":\"CNF\",\"representation\":\"point\",\"value\":0.99,\"method\":\"direct_observation\",\"calibration\":{\"calibrated\":true,\"dataset_id\":\"urn:asv:ds:sec-filings\",\"calibration_date\":\"2026-02-15T00:00:00Z\",\"metric\":\"accuracy\",\"metric_value\":0.998}},\"evidence\":[{\"type\":\"EVD\",\"quality_class\":\"direct_observation\",\"source_type\":\"regulatory_filing\",\"source_id\":\"urn:sec:filing:acme-10q-2025q4\",\"description\":\"SEC 10-Q filing, filed 2026-02-14\"}]}"
      }
    }
  ]
}
```

#### 4.3 Standalone Usage

ASV objects persist as JSON documents in file systems, document stores, or regulatory archives. Each object has a stable URI-based identity.

**File Format:** `.asv.json`

**Standalone Document Structure:**

```json
{
  "$schema": "https://asv.atrahasis.org/v1/schema.json",
  "@context": "https://asv.atrahasis.org/v1/context.jsonld",
  "document_id": "urn:asv:doc:audit-trail-2026-03-09",
  "created_at": "2026-03-09T14:30:00Z",
  "objects": [
    {
      "type": "SAE",
      "id": "urn:asv:sae:decision-001",
      "performative": "INFORM",
      "claim": {
        "type": "CLM",
        "id": "urn:asv:clm:loan-decision-001",
        "epistemic_class": "inference",
        "statement": "Loan application #A-7721 approved based on credit score, income verification, and debt-to-income ratio analysis.",
        "confidence": {
          "type": "CNF",
          "representation": "point",
          "value": 0.94,
          "method": "model_derived",
          "calibration": {
            "calibrated": true,
            "dataset_id": "urn:asv:ds:loan-model-cal-2025h2",
            "calibration_date": "2025-12-01T00:00:00Z",
            "metric": "expected_calibration_error",
            "metric_value": 0.03
          }
        },
        "evidence": [
          {
            "type": "EVD",
            "quality_class": "direct_observation",
            "source_type": "credit_bureau_report",
            "source_id": "urn:credit:report:applicant-7721",
            "description": "Credit score 742, pulled 2026-03-08"
          },
          {
            "type": "EVD",
            "quality_class": "direct_observation",
            "source_type": "income_verification",
            "source_id": "urn:payroll:verification:applicant-7721",
            "description": "Annual income $95,000, verified via payroll API"
          },
          {
            "type": "EVD",
            "quality_class": "computational_result",
            "source_type": "model_output",
            "source_id": "urn:asv:model:loan-risk-v4.2",
            "description": "Risk model output: DTI 28%, probability of default 0.03"
          }
        ],
        "provenance": {
          "type": "PRV",
          "prov:wasGeneratedBy": {
            "activity_id": "urn:asv:act:loan-evaluation-7721",
            "activity_type": "automated_decision",
            "started_at": "2026-03-09T14:28:00Z",
            "ended_at": "2026-03-09T14:28:12Z"
          },
          "prov:wasAttributedTo": "urn:asv:agt:loan-underwriting-agent",
          "delegation_chain": [
            {
              "delegator": "urn:asv:agt:loan-coordinator",
              "delegate": "urn:asv:agt:loan-underwriting-agent",
              "prov:actedOnBehalfOf": true
            }
          ]
        },
        "verification": {
          "type": "VRF",
          "status": "verified",
          "method": "consensus",
          "verifiers": [
            "urn:asv:agt:compliance-reviewer-01",
            "urn:asv:agt:senior-underwriter-agent"
          ],
          "verified_at": "2026-03-09T14:29:30Z"
        }
      }
    }
  ]
}
```

This standalone document is a complete regulatory audit trail: every decision is traceable from claim through evidence, provenance, and verification. This is the compliance use case that drives regulated-industry adoption.

---

### 5. JSON Schema Design

#### 5.1 Schema Structure

ASV schemas are organized as a JSON Schema vocabulary (Draft 2020-12) with URI-identified keywords:

```
asv-schema/
  v1/
    meta-schema.json          # ASV meta-schema extending JSON Schema Draft 2020-12
    vocabulary.json            # Vocabulary definition with URI
    types/
      sae.schema.json          # Speech-Act Envelope
      clm.schema.json          # Claim
      cnf.schema.json          # Confidence
      evd.schema.json          # Evidence
      prv.schema.json          # Provenance
      vrf.schema.json          # Verification
      agt.schema.json          # Agent
    context.jsonld             # JSON-LD @context
    asv-document.schema.json   # Standalone document schema
```

#### 5.2 Type Discrimination

All ASV types use a `type` discriminator property for polymorphic validation:

```json
{
  "type": "object",
  "required": ["type"],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["CLM", "CNF", "EVD", "PRV", "VRF", "AGT", "SAE"]
    }
  },
  "oneOf": [
    { "$ref": "types/clm.schema.json" },
    { "$ref": "types/cnf.schema.json" },
    { "$ref": "types/evd.schema.json" },
    { "$ref": "types/prv.schema.json" },
    { "$ref": "types/vrf.schema.json" },
    { "$ref": "types/agt.schema.json" },
    { "$ref": "types/sae.schema.json" }
  ]
}
```

#### 5.3 Vocabulary Extension Mechanism

Third parties extend ASV via namespace-qualified properties in JSON-LD:

```json
{
  "@context": [
    "https://asv.atrahasis.org/v1/context.jsonld",
    {
      "medicalASV": "https://example.org/medical-asv/v1/"
    }
  ],
  "type": "CLM",
  "epistemic_class": "observation",
  "medicalASV:clinical_significance": "statistically_significant",
  "medicalASV:icd10_code": "E11.9"
}
```

Custom vocabulary extensions are validated by their own schemas; the core ASV schema ignores unknown properties (via `additionalProperties: true` on extension points).

#### 5.4 The 75-80% Structural Coverage

JSON Schema enforces structural validity. The Science Assessment identified three categories that require the supplementary semantic specification:

| Category | What Schema Handles | What Semantic Spec Handles |
|----------|-------------------|-----------------------------|
| Confidence semantics | Value range [0,1], required method field | What confidence 0.85 means given method=statistical vs. method=model_derived |
| Operation class algebra | Field is one of {M, B, X, V, G} | Composition rules: M+V=X, B+anything=B |
| Graph referential integrity | agent_id is a string matching URI pattern | agent_id MUST resolve to an AGT object in the same document or a linked registry |
| Calibration requirements | calibration object shape validation | confidence 0.90 should correspond to 90% accuracy on holdout data |
| Evidence-claim consistency | EVD array is valid JSON array | Evidence quality class should be consistent with evidence content |

---

### 6. Semantic Specification (scoped to 50 pages)

The Assessment Council mandated (REQ-4) a 50-page cap on the semantic specification. This section defines what must be included, what can be deferred, and how interpretation contracts work.

#### 6.1 What Must Be In the Semantic Spec (Phase 2)

1. **Confidence method interpretation contracts** (~8 pages)
   - Precise definitions of `statistical`, `consensus`, `model_derived`, `human_judged`
   - How to aggregate confidence across multiple evidence sources
   - When and how confidence values propagate through delegation chains

2. **Epistemic class definitions and verification guidance** (~6 pages)
   - Definitions of all 6 epistemic classes with boundary cases
   - Recommended verification approach for each class
   - How epistemic class affects evidence weighting

3. **Performative commitment semantics** (~4 pages)
   - What commitment each of the 6 performatives creates
   - How commitments compose (e.g., PROPOSE followed by CONFIRM)
   - Graceful degradation for unknown performatives

4. **Evidence quality class definitions** (~4 pages)
   - Definitions of all 5 quality classes
   - Guidance for evidence producers on class selection
   - How quality class affects downstream weighting

5. **Referential integrity contracts** (~4 pages)
   - Which references MUST resolve vs. MAY be dangling
   - Cross-document reference resolution rules
   - How to handle unresolvable references

6. **Temporal validity semantics** (~3 pages)
   - How expired claims are treated
   - Re-verification trigger rules
   - Time zone handling (UTC normalization)

7. **Calibration protocol** (~5 pages)
   - How to perform calibration for each confidence method
   - Minimum calibration dataset requirements
   - How to report calibration results in CNF objects

8. **Conformance levels** (~4 pages)
   - Level 1: Structural (passes schema validation)
   - Level 2: Semantic (satisfies interpretation contracts)
   - Level 3: Full (structural + semantic + calibration)

**Total: ~38 pages, leaving 12 pages for examples and edge cases.**

#### 6.2 What Can Be Deferred

- Operation class composition algebra (M/B/X/V/G) -- deferred until demonstrated need
- Federation semantics (cross-organization trust boundaries) -- deferred to Phase 3
- Binary encoding specification -- deferred to Phase 4
- Advanced delegation chain semantics (multi-hop trust attenuation) -- deferred to v2.0
- Formal verification properties (TLA+/Coq) -- deferred to Phase 4

#### 6.3 Interpretation Contracts for JSON Schema Gaps

Where JSON Schema cannot enforce a semantic constraint, the specification defines an **interpretation contract**: a normative statement that conforming implementations MUST enforce at the application layer.

Example interpretation contract:

> **IC-CNF-001: Calibration Integrity.**
> A CNF object with `calibration.calibrated: true` MUST have been validated against a holdout dataset identified by `calibration.dataset_id`. An implementation claiming Conformance Level 2 or higher MUST reject CNF objects where `calibrated: true` but `dataset_id` is absent or unresolvable.

Reference implementations (Python and TypeScript validators) enforce all interpretation contracts and serve as the normative behavioral reference when the prose specification is ambiguous.

---

### 7. Security Considerations

#### 7.1 Provenance Integrity

ASV provenance records (PRV) carry `prov:wasAttributedTo` and `prov:wasGeneratedBy` claims. These are self-reported by the producing agent. ASV does not provide cryptographic provenance integrity by default.

**For high-assurance deployments:**
- VRF objects MAY include a `proof` field aligned with W3C VC Data Integrity, containing a cryptographic signature over the CLM+PRV content.
- The signature binds the provenance claim to a verifiable identity.
- Without cryptographic proofs, provenance is trust-based: consumers must trust the producing agent's self-report.

```json
{
  "type": "VRF",
  "status": "verified",
  "method": "cryptographic",
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-rdfc-2022",
    "verificationMethod": "did:key:z6Mkf5rG...",
    "proofPurpose": "assertionMethod",
    "proofValue": "z3FXQqF..."
  }
}
```

#### 7.2 Confidence Manipulation Risks

Adversarial agents may report inflated confidence scores to influence downstream decisions. Mitigations:

1. **Calibration metadata is mandatory.** Uncalibrated confidence scores carry explicit warnings.
2. **Evidence quality typing enables cross-checking.** A confidence of 0.99 based on `hearsay` evidence is suspicious and can be flagged.
3. **Verification records provide independent assessment.** VRF objects from trusted verifier agents can override self-reported confidence.
4. **Temporal validity limits exposure.** Claims expire and require re-verification.

#### 7.3 Trust Model

ASV itself does not define a trust model. Trust is delegated to the transport protocol:

- **A2A:** Agent Cards and authentication mechanisms establish agent identity and trust.
- **MCP:** Server authentication and capability declarations establish tool trust.
- **Standalone:** Document signing (W3C VC Data Integrity) provides tamper evidence.

ASV adds epistemic trust signals (confidence calibration, evidence quality, verification status) on top of transport-level identity trust. The combination enables nuanced trust decisions: "I trust this agent's identity (A2A) and I can see that its confidence is calibrated and its evidence is direct observation (ASV)."

---

### 8. Adoption Strategy

#### 8.1 Regulated Industry First

ASV's primary adoption path is compliance necessity in regulated industries, not developer enthusiasm. Target verticals:

| Vertical | Regulatory Driver | ASV Value |
|----------|------------------|-----------|
| Financial Services | Model risk management (SR 11-7), EU AI Act | Auditable decision chains for automated lending, trading, risk assessment |
| Healthcare | FDA AI/ML guidance, clinical decision support requirements | Structured confidence for diagnostic recommendations |
| Government | NIST AI Agent Standards Initiative (Feb 2026), EU AI Act | Transparent provenance for AI-assisted policy analysis |

#### 8.2 Open Source Reference Implementation

Phase 1 delivers MIT-licensed Python and TypeScript validator libraries. The reference implementation is the normative behavioral specification -- when prose and code disagree, code wins (until the prose is corrected).

**Distribution:**
- Python: `pip install asv-validator`
- TypeScript/JavaScript: `npm install asv-validator`
- Schema files: CDN-hosted at `https://asv.atrahasis.org/v1/`

#### 8.3 W3C/AAIF Contribution Path

**Timeline:**
- Month 3: Submit ASV concept paper to W3C AI Agent Protocol Community Group
- Month 6: Present reference implementation and benchmark results
- Month 9: Propose ASV vocabulary as a contribution to AAIF (Linux Foundation)
- Month 12: Evaluate whether ASV should be an independent standard or folded into A2A/MCP extensions

**Pivoting:** If W3C CG or AAIF publishes a competing vocabulary, ASV pivots to contributing its novel components (claim classification taxonomy, dual classification, CNF) to the competing effort rather than maintaining a parallel standard.

#### 8.4 Avoiding FIPA/KQML Failure Modes

The Assessment Council and Adversarial Analyst both identified the FIPA parallel as the primary historical risk. ASV addresses each FIPA failure mode:

| FIPA Failure Mode | How ASV Avoids It |
|-------------------|-------------------|
| Too many performatives (20+) | ASV uses 6, informed by uACP proof that 4 suffice |
| Custom syntax with no tooling | ASV uses JSON with universal tooling |
| Specification before implementation | ASV ships code in 6 weeks, spec follows |
| Mentalistic semantics (BDI) inappropriate for AI | ASV uses commitment semantics (Singh) |
| No killer application | ASV targets regulatory compliance as forcing function |
| Protocol competition | ASV is vocabulary on A2A/MCP, not a competing protocol |

---

### 9. Architectural Decisions

#### ARCH-C4-001: JSON Schema Over Custom Syntax
**Decision:** ASV types are defined as JSON Schema (Draft 2020-12) with no custom syntax.
**Rationale:** LLMs generate valid JSON at >95% accuracy (StructEval 2025). Custom AASL syntax has zero training data support, requiring translation layers that negate any token savings. The bootstrapping problem is existential for custom syntax and non-existent for JSON.
**Tradeoff:** JSON is ~30-40% more verbose than compact AASL syntax. Accepted because the ecosystem cost of custom syntax vastly outweighs the compactness benefit.

#### ARCH-C4-002: Vocabulary Layer, Not Protocol
**Decision:** ASV defines no transport, routing, connection management, or task lifecycle. These are delegated to A2A and MCP.
**Rationale:** IBM ACP was absorbed into A2A in 5 months. Protocol competition is a losing strategy. ASV occupies the semantic layer that A2A and MCP explicitly leave unaddressed.
**Tradeoff:** ASV depends on A2A/MCP extensibility mechanisms. If those mechanisms prove insufficient, ASV cannot work without protocol modifications (which is a kill criterion for GATE-1).

#### ARCH-C4-003: W3C PROV Extension, Not Custom Provenance
**Decision:** ASV provenance maps to W3C PROV-O entities (CLM -> prov:Entity, PRV -> prov:Activity, AGT -> prov:Agent) following the PROV-AGENT (2025) precedent.
**Rationale:** W3C PROV is a mature 2013 Recommendation with 13 years of stability, existing tooling (provtoolbox, prov Python library, Neo4j PROV plugins), and established adoption. Extending PROV is cheaper and more interoperable than inventing custom provenance.
**Tradeoff:** PROV's generic extension mechanism was not designed for rich epistemic metadata. ASV's extensions (confidence, evidence quality, verification status) may require custom serializers for full PROV-JSON export.

#### ARCH-C4-004: Six Performatives
**Decision:** ASV defines exactly 6 speech-act performatives: INFORM, REQUEST, PROPOSE, CONFIRM, WARN, QUERY.
**Rationale:** uACP proves 4 verbs suffice for all finite-state FIPA protocols. FIPA's 20+ performatives were too many -- most systems used only 4-6. ASV's 6 are a pragmatic middle ground: the 4-verb uACP basis (TELL, ASK mapped to INFORM, REQUEST, QUERY, CONFIRM) plus two convenience extensions (PROPOSE, WARN) that represent common communicative intents without extending expressive power.
**Tradeoff:** 6 may be too many (confusing LLMs choosing among similar options) or too few (forcing awkward encoding of some speech acts). The set is namespace-extensible; HG-2 will validate whether LLMs reliably distinguish among 6 options.

#### ARCH-C4-005: Mandatory Calibration Metadata for CNF
**Decision:** Every CNF object MUST declare whether it is calibrated and, if uncalibrated, MUST include a warning.
**Rationale:** LLMs are poorly calibrated -- confidence scores without calibration metadata create false precision that actively misleads downstream consumers (Adversarial Probe C). Distinguishing model-reported from empirically validated confidence addresses the core concern without solving the unsolved calibration research problem.
**Tradeoff:** Adds friction for simple use cases where approximate confidence is sufficient. Accepted because false precision in confidence is worse than no confidence in regulated contexts.

#### ARCH-C4-006: Dual Classification (Speech-Act + Epistemic Type)
**Decision:** Every ASV claim carries two independent classifications: what communicative act is performed (speech-act type) and what kind of knowledge assertion is made (epistemic class).
**Rationale:** This is ASV's core integrative novelty. FIPA classifies speech acts. No existing system classifies epistemic claim types. The combination produces message types that enable routing and processing logic impossible with either classification alone.
**Tradeoff:** Adds complexity -- agents must select from 6 performatives AND 6 epistemic classes (36 possible combinations). HG-2 will validate whether this is too complex for LLM generation.

#### ARCH-C4-007: Kill AACP
**Decision:** AACP (Atrahasis Agent Communication Protocol) is formally retired. No further development.
**Rationale:** AACP is a 187-line sketch with no connection management, authentication, error handling, or versioning. A2A and MCP are production-grade protocols with massive ecosystem support (100+ enterprise partners for A2A, 97M+ monthly SDK downloads for MCP). Maintaining AACP wastes credibility and engineering resources on a solved problem.
**Tradeoff:** Atrahasis loses the aspiration of a custom communication protocol. Accepted because vocabulary-layer innovation is more defensible and more feasible than protocol competition.

#### ARCH-C4-008: Paired Schema + Semantic Specification
**Decision:** ASV ships as two co-versioned deliverables: JSON Schema files (machine-enforceable) and a Semantic Specification document (human/LLM-readable, capped at 50 pages).
**Rationale:** JSON Schema captures ~75-80% of ASV's type system (Science Assessment SQ-1). The remaining 20% -- epistemic semantics, referential integrity, calibration requirements -- requires normative prose. This paired model follows precedent: OpenAPI has schemas + specification, FHIR has schemas + implementation guides.
**Tradeoff:** The semantic spec creates documentation burden and risks divergence from schemas. Mitigated by co-versioning (schema v1.2 always pairs with spec v1.2), automated conformance tests, and treating the reference implementation as the normative behavioral authority.

---

### Appendix A: Traceability -- Assessment Council Conditions

| Condition | Type | Architecture Section |
|-----------|------|---------------------|
| GATE-1: Working Implementation Before Full Spec | GATE | 2.1 (HG-1), 8.2 (reference implementation) |
| GATE-2: LLM Generation Accuracy >80% | GATE | 2.2 (HG-2), ARCH-C4-001, ARCH-C4-006 |
| GATE-3: Provenance Chain Utility >20% | GATE | 2.3 (HG-3), 3.1 (chain design) |
| REQ-1: Narrow Invention Claim | REQUIRED | 1.1 (philosophy point 3), 3.2, 3.3 (novel components identified) |
| REQ-2: Kill AACP | REQUIRED | 1.3, ARCH-C4-007 |
| REQ-3: Address Confidence Calibration | REQUIRED | 3.2 (calibration requirements), ARCH-C4-005 |
| REQ-4: Semantic Spec Cap 50 Pages | REQUIRED | 6.1, 6.2, ARCH-C4-008 |
| REC-1: Regulated Industry Engagement | RECOMMENDED | 8.1 (adoption strategy) |
| REC-2: A2A Specification Monitoring | RECOMMENDED | 8.3 (W3C/AAIF path), 8.4 (failure mode avoidance) |

### Appendix B: Traceability -- Adversarial Findings

| Attack/Probe | Severity | Architecture Response |
|-------------|----------|----------------------|
| Attack 1: "Just JSON-LD" Reassembly | HIGH | 3.2-3.3 (novel components that resist reassembly: CNF, dual classification). HG-3 demonstrates emergent value of integration. |
| Attack 2: Adoption Impossibility | HIGH | 8.1 (regulated industry path), 8.2 (open source), 8.4 (FIPA failure mode avoidance) |
| Attack 3: LLM Irrelevance | MEDIUM | ARCH-C4-001 (JSON for LLM compatibility), 4.1-4.3 (non-LLM consumers: audit, compliance, monitoring) |
| Attack 4: "Integration Not Invention" | MEDIUM | 1.1 (narrowed claim), 3.2 (CNF novelty), 3.3 (dual classification novelty) |
| Attack 5: Timing Attack | MEDIUM | 8.3 (W3C/AAIF contribution timeline), HG-1 (6-week sprint) |
| Attack 6: The 20% Gap | MEDIUM | 5.4 (coverage table), 6.1-6.3 (scoped semantic spec), ARCH-C4-008 |
| Probe A: Can ASV Survive Without AACP? | -- | ARCH-C4-007 (AACP killed) |
| Probe B: "Objects Not Outputs" | -- | 4.3 (standalone documents with identity), acknowledged as philosophy not mechanism |
| Probe C: Confidence Calibration | -- | 3.2 (calibration metadata), ARCH-C4-005 |
| Probe D: Specification Inversion | -- | 2.1 (code-first sprint), ARCH-C4-008 (implementation before spec) |

### Appendix C: Monitoring Flags

| Flag | Severity | Trigger | Architecture Response |
|------|----------|---------|----------------------|
| A2A Convergence | RED | A2A adds structured confidence/verification as first-class properties | Pivot ASV to semantic spec for A2A's epistemic metadata (Section 8.3) |
| LLM Generation Failure | RED | GATE-2 structural validity <70% for full chain | Decompose chain into independently usable components (Section 3.1 composition rules already support partial chains) |
| Provenance Utility Failure | RED | GATE-3 error detection <20% vs. simple attribution | Extract claim classification + dual classification as standalone contributions (Section 3.3) |
| Specification Bloat | AMBER | Semantic spec exceeds 30 pages before Phase 2 | Trigger scope review; convert prose contracts to conformance tests (Section 6.3) |
| Adoption Inertia | AMBER | Zero external downloads/integrations within 6 months | Contribute directly to W3C CG or AAIF (Section 8.3) |
| Calibration Gap | AMBER | LLM confidence <0.3 correlation with accuracy | Add mandatory warnings; default CNF to interval representation (Section 3.2) |

---

*Architecture document completed 2026-03-09. ASV C4-A Design Phase.*
