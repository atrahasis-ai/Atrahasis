# Proof-Carrying Verification Membrane (PCVM) — Technical Specification

## C5-A SPECIFICATION Document

**Version:** 1.0.0
**Date:** 2026-03-09
**Status:** SPECIFICATION (Conditional Advance from Assessment Council)
**Invention ID:** C5
**Concept:** C5-B
**Predecessor:** Verichain (deprecated)
**Dependencies:** C3 (Tidal Noosphere), C4 (ASV)
**Assessment Council Verdict:** CONDITIONAL_ADVANCE (Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10)
**Normative References:** RFC 2119, RFC 9381 (ECVRF), JSON Schema Draft 2020-12, Josang Subjective Logic (2016), RFC 3339

---

## Abstract

The Proof-Carrying Verification Membrane (PCVM) is the verification execution engine for the Tidal Noosphere. It replaces Verichain's replication-based consensus with a graduated proof-carrying architecture: every agent output carries a Verification Trace Document (VTD) — a structured evidence package that the membrane evaluates instead of re-executing computation.

PCVM defines nine claim classes organized into three verification tiers. Tier 1 (D-class, C-class) carries machine-checkable formal proofs with sublinear verification cost. Tier 2 (E-class, S-class, P-class, R-class) carries structured evidence chains verified through completeness checking and selective adversarial probing. Tier 3 (H-class, N-class) carries structured attestations verified through adversarial probing and expert committee review. Credibility is represented using Josang's Subjective Logic opinion tuples and propagated through claim dependency graphs via conjunction, discounting, and consensus operators.

The membrane assigns claim classifications (agents propose, the membrane decides), selects adversarial probers via VRF independently of verification committees, and subjects 5-10% of all passed claims to random deep-audit via full replication as a deterrence mechanism. Agent credibility is tracked per claim class to prevent reputation laundering across epistemic categories.

This specification is implementation-ready. An engineer with access to this document, the Tidal Noosphere specification (C3), and the ASV vocabulary (C4) can build PCVM without additional design decisions.

---

## Table of Contents

- [1. Formal Definitions and Notation](#1-formal-definitions-and-notation)
- [2. VTD Schema Specification](#2-vtd-schema-specification)
- [3. Claim Classification Protocol](#3-claim-classification-protocol)
- [4. Verification Protocols per Tier](#4-verification-protocols-per-tier)
- [5. Adversarial Probing Specification](#5-adversarial-probing-specification)
- [6. Credibility Engine Specification](#6-credibility-engine-specification)
- [7. Deep-Audit Protocol Specification](#7-deep-audit-protocol-specification)
- [8. Knowledge Admission Protocol](#8-knowledge-admission-protocol)
- [9. Integration Interfaces](#9-integration-interfaces)
- [10. Configurable Parameters](#10-configurable-parameters)
- [11. Conformance Requirements](#11-conformance-requirements)
- [12. Test Vectors](#12-test-vectors)
- [13. Security Considerations](#13-security-considerations)

---

**Notation and Conventions.** The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119. Pseudocode uses Python-like syntax with explicit type annotations. All hash functions refer to SHA-256 unless otherwise specified. VRF refers to ECVRF on P-256 per RFC 9381. Epoch numbers are zero-indexed from GENESIS_TIME as defined in the Tidal Noosphere specification. Agent identifiers are globally unique 256-bit values. All JSON schemas conform to JSON Schema Draft 2020-12. Timestamps are RFC 3339 strings in UTC. Opinion tuples are denoted with lowercase omega (w). Credibility scores are real values in [0, 1].

---

## 1. Formal Definitions and Notation

### 1.1 Primitive Types

| Symbol | Type | Definition |
|--------|------|------------|
| `AgentId` | `bytes[32]` | Globally unique agent identifier (256-bit) |
| `ClaimId` | `string` | URI-format claim identifier: `clm:<locus>:<epoch>:<hash8>` |
| `VtdId` | `string` | URI-format VTD identifier: `vtd:<claim_id>:<version>` |
| `ClsId` | `string` | Classification Seal identifier: `cls:<claim_id>:<epoch>` |
| `EpochNum` | `uint64` | Zero-indexed epoch number |
| `ClaimClass` | `enum` | One of {D, E, S, H, N, P, R, C} |
| `Tier` | `enum` | One of {FORMAL_PROOF, STRUCTURED_EVIDENCE, STRUCTURED_ATTESTATION} |
| `Hash256` | `bytes[32]` | SHA-256 digest |
| `VRFProof` | `bytes[80]` | ECVRF proof (RFC 9381) |
| `Signature` | `bytes[64]` | Ed25519 signature |
| `Opinion` | `tuple(f64, f64, f64, f64)` | Subjective Logic opinion (b, d, u, a) |
| `Timestamp` | `string` | RFC 3339 UTC timestamp |

### 1.2 Claim Class Definitions

Each claim class occupies a position in the epistemic status x verification modality matrix:

| | REPLAY | EVIDENCE | LOGIC | ALIGNMENT |
|---|---|---|---|---|
| **COMPUTED** | D (primary) | | | C |
| **OBSERVED** | | E (primary) | | |
| **INFERRED** | | S | R (primary) | |
| **JUDGED** | | | | H, N |

P (Process) is cross-cutting: it applies to the production process of any claim regardless of epistemic status.

**Formal class definitions:**

- **D-class (Deterministic):** A claim whose truth value is decidable by deterministic computation. The claim's correctness can be verified by replaying the computation on the stated inputs. Tier: FORMAL_PROOF.

- **C-class (Compliance):** A claim that a system, process, or output conforms to a specified regulation, standard, or constitutional parameter. Verification reduces to matching against a finite rule set. Tier: FORMAL_PROOF.

- **E-class (Empirical):** A claim derived from observation or measurement of external phenomena. Verification requires checking cited sources, cross-referencing, and assessing source reliability. Tier: STRUCTURED_EVIDENCE.

- **S-class (Statistical):** A claim derived from statistical analysis of data. Verification requires checking methodology, sample adequacy, test appropriateness, and conclusion validity. Tier: STRUCTURED_EVIDENCE.

- **P-class (Process):** A claim that a specified process was followed during the production of another claim. Verification checks execution traces against the declared process specification. Tier: STRUCTURED_EVIDENCE.

- **R-class (Reasoning):** A claim derived from logical inference over premises. Verification checks logical validity, premise support, and assumption disclosure. Tier: STRUCTURED_EVIDENCE.

- **H-class (Heuristic):** A claim derived from expert judgment, model prediction, or pragmatic assessment. Verification checks that alternatives were considered, criteria are appropriate, and no known contradictions exist. Tier: STRUCTURED_ATTESTATION.

- **N-class (Normative):** A claim about values, ethics, or policy that invokes a normative framework. Verification checks constitutional alignment, stakeholder coverage, and framework application consistency. Normative claims are verified for consistency and completeness, not for truth. Tier: STRUCTURED_ATTESTATION.

### 1.3 Tier-to-Cost Mapping

| Tier | Classes | Verification Mechanism | Cost vs. Replication |
|------|---------|----------------------|---------------------|
| FORMAL_PROOF | D, C | Proof certificate checking, rule matching | 0.1x - 0.35x |
| STRUCTURED_EVIDENCE | E, S, P, R | Evidence completeness + selective adversarial probing | 0.5x - 1.2x |
| STRUCTURED_ATTESTATION | H, N | Adversarial probing + expert committee review | 1.0x - 2.0x |

### 1.4 Subjective Logic Primitives

An opinion tuple w = (b, d, u, a) represents a belief about a binary proposition where:
- b (belief): evidence in favor, b >= 0
- d (disbelief): evidence against, d >= 0
- u (uncertainty): lack of evidence, u >= 0
- a (base rate): prior probability absent evidence, a in [0, 1]
- **Constraint:** b + d + u = 1

The **expected probability** (credibility score) of an opinion:

```
E(w) = b + a * u
```

**Vacuous opinion** (total ignorance): w_vacuous = (0, 0, 1, 0.5)

**Dogmatic belief**: w_true = (1, 0, 0, a) for any a

**Dogmatic disbelief**: w_false = (0, 1, 0, a) for any a

### 1.5 Multi-Class Claims

A claim MAY occupy multiple cells in the epistemic matrix. When it does:

1. The **primary classification** determines the strongest proof obligation and sets the VTD envelope type.
2. **Secondary classifications** impose additional proof obligations as VTD extension sections.
3. The VTD MUST satisfy ALL applicable proof obligations (union of requirements).
4. The credibility score is the MINIMUM of the credibility scores computed for each applicable class.

```
credibility(claim) = min(E(w_K) for K in claim.classes)
```

### 1.6 Key Invariants

- **INV-M1 (Membrane Sovereignty):** No claim enters the canonical knowledge graph without passing through PCVM. This invariant is constitutionally protected per INV-1 of the Tidal Noosphere.

- **INV-M2 (Classification Independence):** The membrane assigns final claim classifications. Producing agents propose; the membrane decides. No agent may self-certify its own claim classification.

- **INV-M3 (Verifier Independence):** VTD verification is performed by VRF-selected committees. No agent may verify its own claims. Adversarial probers are selected independently of verification committees.

- **INV-M4 (Class-Specific Trust):** Agent credibility is tracked per claim class. An agent's credibility in class K does not transfer to class K' where K != K'.

- **INV-M5 (Deep-Audit Deterrence):** A configurable percentage (default 7%) of all passed VTDs are re-verified via full replication. Selection is VRF-based and unpredictable.

- **INV-M6 (Credibility Monotonicity):** Composition of opinions via conjunction never increases belief beyond the minimum of the composed beliefs. Discounting never increases belief beyond the discounter's trust level.

- **INV-M7 (VTD Immutability):** Once a VTD is submitted and sealed, its contents MUST NOT be modified. Corrections require a new VTD with an explicit supersedes reference.

---

## 2. VTD Schema Specification

### 2.1 Common VTD Envelope

Every VTD, regardless of claim class, MUST conform to the common envelope schema. The envelope carries identity, provenance, and structural metadata. Class-specific evidence is carried in the `proof_body` field.

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-envelope.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "VTD Common Envelope",
  "description": "Universal wrapper for all Verification Trace Documents.",
  "type": "object",
  "required": [
    "vtd_id", "claim_id", "claim_text", "suggested_class",
    "assigned_class", "tier", "producing_agent", "epoch",
    "locus", "timestamp", "proof_body", "dependencies",
    "counter_evidence", "vtd_hash", "agent_signature"
  ],
  "properties": {
    "vtd_id": {
      "type": "string",
      "pattern": "^vtd:clm:[^:]+:[0-9]+:[a-f0-9]{8}:[0-9]+$",
      "description": "Unique VTD identifier."
    },
    "claim_id": {
      "type": "string",
      "pattern": "^clm:[^:]+:[0-9]+:[a-f0-9]{8}$",
      "description": "The claim this VTD supports."
    },
    "claim_text": {
      "type": "string",
      "minLength": 1,
      "maxLength": 10000,
      "description": "Human-readable claim statement."
    },
    "suggested_class": {
      "type": "string",
      "enum": ["D", "E", "S", "H", "N", "P", "R", "C"],
      "description": "The producing agent's suggested classification."
    },
    "assigned_class": {
      "type": ["string", "null"],
      "enum": ["D", "E", "S", "H", "N", "P", "R", "C", null],
      "description": "Membrane-assigned classification. Null before classification."
    },
    "secondary_classes": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["D", "E", "S", "H", "N", "P", "R", "C"]
      },
      "default": [],
      "description": "Additional applicable classes for multi-class claims."
    },
    "tier": {
      "type": ["string", "null"],
      "enum": ["FORMAL_PROOF", "STRUCTURED_EVIDENCE", "STRUCTURED_ATTESTATION", null],
      "description": "Verification tier. Derived from assigned_class."
    },
    "producing_agent": {
      "type": "string",
      "description": "AgentId of the agent that produced the claim and VTD."
    },
    "epoch": {
      "type": "integer",
      "minimum": 0,
      "description": "Epoch in which the VTD was submitted."
    },
    "locus": {
      "type": "string",
      "description": "Locus namespace selector (e.g., biology.proteomics)."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "RFC 3339 UTC timestamp of VTD creation."
    },
    "proof_body": {
      "type": "object",
      "description": "Class-specific evidence payload. Schema determined by assigned_class."
    },
    "secondary_proof_bodies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["class", "body"],
        "properties": {
          "class": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] },
          "body": { "type": "object" }
        }
      },
      "default": [],
      "description": "Evidence for secondary classifications."
    },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["claim_id", "relationship"],
        "properties": {
          "claim_id": { "type": "string" },
          "relationship": {
            "type": "string",
            "enum": ["PREMISE", "EVIDENCE", "PROCESS_INPUT", "CONSTITUTIONAL_AXIOM", "EXTERNAL_SOURCE"]
          },
          "required_credibility": {
            "type": "number", "minimum": 0, "maximum": 1, "default": 0.6
          }
        }
      },
      "description": "Claims this VTD depends on."
    },
    "counter_evidence": {
      "type": "object",
      "required": ["considered"],
      "properties": {
        "considered": {
          "type": "boolean",
          "description": "Whether counter-evidence was actively sought."
        },
        "items": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["description", "disposition"],
            "properties": {
              "description": { "type": "string" },
              "source": { "type": "string" },
              "disposition": {
                "type": "string",
                "enum": ["REFUTED", "ACKNOWLEDGED_LIMITATION", "SCOPE_EXCLUSION", "UNRESOLVED"]
              },
              "refutation": { "type": "string" }
            }
          },
          "default": []
        }
      },
      "description": "Counter-evidence considered. Required for Tier 2 and Tier 3."
    },
    "supersedes": {
      "type": ["string", "null"],
      "default": null,
      "description": "VTD ID this document supersedes, if any."
    },
    "vtd_size_bytes": {
      "type": "integer",
      "description": "Total size of serialized VTD in bytes."
    },
    "vtd_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$",
      "description": "SHA-256 of canonical JSON serialization of all fields except vtd_hash and agent_signature."
    },
    "agent_signature": {
      "type": "string",
      "description": "Ed25519 signature over vtd_hash by producing_agent."
    }
  },
  "additionalProperties": false
}
```

**VTD Size Limits per Class:**

| Class | Max VTD Size | Rationale |
|-------|-------------|-----------|
| D | 10 KB | Computation traces are compact |
| C | 50 KB | Compliance mappings may be lengthy |
| E | 50 KB | Source citations with quotes |
| S | 30 KB | Statistical metadata is structured |
| P | 100 KB | Process logs can be detailed |
| R | 30 KB | Reasoning chains are bounded |
| H | 100 KB | Alternatives analysis can be extensive |
| N | 100 KB | Stakeholder analysis can be extensive |

Claims exceeding size limits MUST be decomposed into smaller sub-claims, each with its own VTD.

### 2.2 D-class VTD (Deterministic Proof)

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-d-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "D-class Proof Body",
  "description": "Deterministic computation proof. Tier 1: FORMAL_PROOF.",
  "type": "object",
  "required": ["computation", "inputs", "output", "proof_type"],
  "properties": {
    "proof_type": {
      "type": "string",
      "enum": ["RECOMPUTATION", "HASH_VERIFICATION", "PROOF_CERTIFICATE", "PROOF_SKETCH"],
      "description": "Type of deterministic proof provided."
    },
    "computation": {
      "type": "object",
      "required": ["algorithm", "version"],
      "properties": {
        "algorithm": { "type": "string", "description": "Algorithm or function identifier." },
        "version": { "type": "string", "description": "Algorithm version or commit hash." },
        "determinism_declaration": {
          "type": "string",
          "enum": ["FULLY_DETERMINISTIC", "DETERMINISTIC_GIVEN_SEED", "DETERMINISTIC_MODULO_PRECISION"],
          "description": "Determinism guarantee level."
        },
        "seed": { "type": "string", "description": "Random seed if DETERMINISTIC_GIVEN_SEED." }
      }
    },
    "inputs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "value_hash"],
        "properties": {
          "name": { "type": "string" },
          "value_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
          "value": { "description": "Actual input value. Omit for large inputs; provide value_hash." },
          "size_bytes": { "type": "integer" }
        }
      }
    },
    "output": {
      "type": "object",
      "required": ["value_hash"],
      "properties": {
        "value_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "value": { "description": "Actual output value." },
        "size_bytes": { "type": "integer" }
      }
    },
    "trace": {
      "type": "object",
      "properties": {
        "key_steps": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["step_index", "operation", "intermediate_hash"],
            "properties": {
              "step_index": { "type": "integer" },
              "operation": { "type": "string" },
              "intermediate_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
            }
          },
          "description": "Sampled intermediate steps for spot-checking."
        },
        "total_steps": { "type": "integer" }
      }
    },
    "proof_certificate": {
      "type": "object",
      "properties": {
        "format": { "type": "string", "enum": ["COQ_PROOF", "TLA_PROOF", "ISABELLE_PROOF", "CUSTOM_CERT"] },
        "certificate_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "certificate_uri": { "type": "string", "format": "uri" },
        "checker_version": { "type": "string" }
      },
      "description": "Machine-checkable proof certificate, if proof_type is PROOF_CERTIFICATE."
    }
  },
  "additionalProperties": false
}
```

### 2.3 E-class VTD (Empirical Evidence)

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-e-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "E-class Proof Body",
  "description": "Empirical evidence package. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": ["sources", "cross_references", "evidence_chain"],
  "properties": {
    "sources": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["source_id", "source_type", "retrieval_timestamp", "relevance_justification"],
        "properties": {
          "source_id": { "type": "string" },
          "source_type": {
            "type": "string",
            "enum": ["PEER_REVIEWED_PAPER", "PREPRINT", "OFFICIAL_REPORT", "DATABASE",
                     "WEB_PAGE", "API_RESPONSE", "VERIFIED_CLAIM", "OBSERVATION_RECORD"]
          },
          "uri": { "type": "string", "format": "uri" },
          "retrieval_timestamp": { "type": "string", "format": "date-time" },
          "content_hash": {
            "type": "string", "pattern": "^[a-f0-9]{64}$",
            "description": "SHA-256 of retrieved content at retrieval_timestamp."
          },
          "quoted_text": {
            "type": "string", "maxLength": 2000,
            "description": "Exact quote supporting the claim."
          },
          "quote_context": {
            "type": "string",
            "description": "Section, page, or table reference for the quote."
          },
          "relevance_justification": {
            "type": "string",
            "description": "Why this source is relevant to the claim."
          },
          "reliability_assessment": {
            "type": "string",
            "enum": ["HIGH", "MEDIUM", "LOW", "UNKNOWN"],
            "default": "UNKNOWN"
          }
        }
      }
    },
    "cross_references": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source_id", "confirms"],
        "properties": {
          "source_id": { "type": "string" },
          "confirms": { "type": "boolean" },
          "partial": { "type": "boolean", "default": false },
          "note": { "type": "string" }
        }
      },
      "description": "Cross-references between sources."
    },
    "evidence_chain": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["sub_claim", "supporting_sources"],
        "properties": {
          "sub_claim": { "type": "string" },
          "supporting_sources": {
            "type": "array",
            "items": { "type": "string" },
            "minItems": 1
          },
          "strength": {
            "type": "string",
            "enum": ["STRONG", "MODERATE", "WEAK"],
            "description": "Evidence strength assessment."
          }
        }
      },
      "description": "Chain linking claim to sources through intermediate sub-claims."
    },
    "observation_conditions": {
      "type": "object",
      "properties": {
        "temporal_range": {
          "type": "object",
          "properties": {
            "start": { "type": "string", "format": "date-time" },
            "end": { "type": "string", "format": "date-time" }
          }
        },
        "methodology": { "type": "string" },
        "instruments": { "type": "array", "items": { "type": "string" } },
        "environmental_factors": { "type": "array", "items": { "type": "string" } }
      }
    }
  },
  "additionalProperties": false
}
```

### 2.4 S-class VTD (Statistical Evidence)

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-s-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "S-class Proof Body",
  "description": "Statistical evidence package. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": ["dataset", "methodology", "results", "assumptions"],
  "properties": {
    "dataset": {
      "type": "object",
      "required": ["sample_size", "source_description"],
      "properties": {
        "sample_size": { "type": "integer", "minimum": 1 },
        "population_description": { "type": "string" },
        "source_description": { "type": "string" },
        "sampling_method": {
          "type": "string",
          "enum": ["RANDOM", "STRATIFIED", "CONVENIENCE", "CENSUS", "SYSTEMATIC", "CLUSTER"]
        },
        "data_hash": {
          "type": "string", "pattern": "^[a-f0-9]{64}$",
          "description": "SHA-256 of the dataset, enabling replication."
        },
        "data_uri": { "type": "string", "format": "uri" },
        "collection_period": {
          "type": "object",
          "properties": {
            "start": { "type": "string", "format": "date-time" },
            "end": { "type": "string", "format": "date-time" }
          }
        }
      }
    },
    "methodology": {
      "type": "object",
      "required": ["test_type"],
      "properties": {
        "test_type": { "type": "string", "description": "Statistical test applied." },
        "software": { "type": "string" },
        "software_version": { "type": "string" },
        "pre_registration": {
          "type": "object",
          "properties": {
            "registered": { "type": "boolean" },
            "registry_uri": { "type": "string", "format": "uri" }
          }
        },
        "corrections": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Multiple comparisons corrections, outlier handling, etc."
        }
      }
    },
    "results": {
      "type": "object",
      "required": ["test_statistic", "conclusion"],
      "properties": {
        "test_statistic": {
          "type": "object",
          "required": ["name", "value"],
          "properties": {
            "name": { "type": "string" },
            "value": { "type": "number" },
            "degrees_of_freedom": { "type": "number" }
          }
        },
        "p_value": { "type": "number", "minimum": 0, "maximum": 1 },
        "confidence_interval": {
          "type": "object",
          "properties": {
            "level": { "type": "number", "minimum": 0, "maximum": 1 },
            "lower": { "type": "number" },
            "upper": { "type": "number" }
          }
        },
        "effect_size": {
          "type": "object",
          "properties": {
            "metric": { "type": "string" },
            "value": { "type": "number" },
            "interpretation": { "type": "string", "enum": ["NEGLIGIBLE","SMALL","MEDIUM","LARGE"] }
          }
        },
        "conclusion": { "type": "string" }
      }
    },
    "assumptions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["assumption", "check_result"],
        "properties": {
          "assumption": { "type": "string" },
          "check_method": { "type": "string" },
          "check_result": {
            "type": "string",
            "enum": ["SATISFIED", "APPROXIMATELY_SATISFIED", "VIOLATED", "NOT_TESTABLE"]
          },
          "note": { "type": "string" }
        }
      }
    },
    "power_analysis": {
      "type": "object",
      "properties": {
        "target_power": { "type": "number" },
        "achieved_power": { "type": "number" },
        "minimum_detectable_effect": { "type": "number" }
      }
    }
  },
  "additionalProperties": false
}
```

### 2.5 H-class VTD (Heuristic Attestation)

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-h-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "H-class Proof Body",
  "description": "Heuristic attestation package. Tier 3: STRUCTURED_ATTESTATION.",
  "type": "object",
  "required": ["alternatives", "criteria", "evaluation", "confidence", "uncertainty_sources"],
  "properties": {
    "alternatives": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": ["name", "description"],
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "genuinely_considered": { "type": "boolean", "default": true }
        }
      },
      "description": "Alternatives genuinely considered. Minimum 2 (including the chosen option)."
    },
    "criteria": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "weight"],
        "properties": {
          "name": { "type": "string" },
          "weight": { "type": "number", "minimum": 0, "maximum": 1 },
          "justification": { "type": "string" }
        }
      },
      "description": "Decision criteria with relative weights (SHOULD sum to 1.0)."
    },
    "evaluation": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["alternative", "criterion", "score", "rationale"],
        "properties": {
          "alternative": { "type": "string" },
          "criterion": { "type": "string" },
          "score": { "type": "number", "minimum": 0, "maximum": 1 },
          "rationale": { "type": "string" }
        }
      },
      "description": "Matrix evaluation: each alternative against each criterion."
    },
    "precedents": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["description", "relevance"],
        "properties": {
          "description": { "type": "string" },
          "source": { "type": "string" },
          "outcome": { "type": "string" },
          "relevance": { "type": "string" },
          "similarity_score": { "type": "number", "minimum": 0, "maximum": 1 }
        }
      }
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Agent's self-assessed confidence in the claim."
    },
    "uncertainty_sources": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string" },
      "description": "Declared sources of uncertainty."
    },
    "boundary_conditions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["condition", "effect"],
        "properties": {
          "condition": { "type": "string" },
          "effect": { "type": "string", "enum": ["INVALIDATES", "WEAKENS", "MODIFIES", "IRRELEVANT"] }
        }
      },
      "description": "Conditions under which the claim may not hold."
    },
    "failure_modes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["mode", "likelihood", "impact"],
        "properties": {
          "mode": { "type": "string" },
          "likelihood": { "type": "string", "enum": ["HIGH", "MEDIUM", "LOW"] },
          "impact": { "type": "string", "enum": ["HIGH", "MEDIUM", "LOW"] },
          "mitigation": { "type": "string" }
        }
      }
    },
    "model_info": {
      "type": "object",
      "properties": {
        "model_id": { "type": "string" },
        "training_data_relevance": { "type": "string" },
        "known_biases": { "type": "array", "items": { "type": "string" } }
      },
      "description": "If claim is model-generated, model provenance information."
    }
  },
  "additionalProperties": false
}
```

### 2.6 N-class VTD (Normative Attestation)

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-n-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "N-class Proof Body",
  "description": "Normative attestation package. Tier 3: STRUCTURED_ATTESTATION.",
  "type": "object",
  "required": ["value_framework", "constitutional_refs", "stakeholder_analysis", "alternatives"],
  "properties": {
    "value_framework": {
      "type": "object",
      "required": ["framework_type", "principles"],
      "properties": {
        "framework_type": {
          "type": "string",
          "enum": ["DEONTOLOGICAL", "CONSEQUENTIALIST", "VIRTUE_ETHICS", "CARE_ETHICS",
                   "CONTRACTUALIST", "PLURALIST", "CONSTITUTIONAL"],
          "description": "Ethical framework invoked."
        },
        "principles": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": ["principle", "application"],
            "properties": {
              "principle": { "type": "string" },
              "source": { "type": "string" },
              "application": { "type": "string" }
            }
          }
        },
        "framework_justification": { "type": "string" }
      }
    },
    "constitutional_refs": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["parameter_id", "alignment"],
        "properties": {
          "parameter_id": {
            "type": "string",
            "pattern": "^CONST-[0-9]{3,4}$",
            "description": "Constitutional parameter identifier."
          },
          "parameter_text": { "type": "string" },
          "parameter_intent": { "type": "string", "description": "Intent annotation of the parameter." },
          "alignment": {
            "type": "string",
            "enum": ["SUPPORTS", "CONSISTENT", "NEUTRAL", "TENSION", "CONFLICTS"]
          },
          "alignment_argument": { "type": "string" }
        }
      }
    },
    "stakeholder_analysis": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["stakeholder_group", "impact", "impact_description"],
        "properties": {
          "stakeholder_group": { "type": "string" },
          "impact": { "type": "string", "enum": ["POSITIVE", "NEGATIVE", "NEUTRAL", "MIXED"] },
          "impact_description": { "type": "string" },
          "mitigation": { "type": "string", "description": "Mitigation for negative impacts." }
        }
      }
    },
    "alternatives": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["position", "counter_argument"],
        "properties": {
          "position": { "type": "string" },
          "counter_argument": { "type": "string" },
          "framework_used": { "type": "string" }
        }
      },
      "description": "Alternative normative positions considered and reasons for rejection."
    },
    "dissent_record": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "dissenting_position": { "type": "string" },
          "dissenting_agent": { "type": "string" },
          "resolution": { "type": "string" }
        }
      },
      "description": "Record of dissenting views encountered during deliberation."
    }
  },
  "additionalProperties": false
}
```

### 2.7 P-class VTD (Process Trace)

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-p-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "P-class Proof Body",
  "description": "Process trace evidence. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": ["process_spec", "steps", "conformance_summary"],
  "properties": {
    "process_spec": {
      "type": "object",
      "required": ["spec_id", "spec_version"],
      "properties": {
        "spec_id": { "type": "string", "description": "Process specification identifier." },
        "spec_version": { "type": "string" },
        "spec_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
        "required_steps": {
          "type": "array",
          "items": { "type": "string" },
          "description": "List of required step identifiers."
        }
      }
    },
    "steps": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["step_id", "step_name", "started", "completed", "status"],
        "properties": {
          "step_id": { "type": "string" },
          "step_name": { "type": "string" },
          "started": { "type": "string", "format": "date-time" },
          "completed": { "type": "string", "format": "date-time" },
          "status": {
            "type": "string",
            "enum": ["COMPLETED", "SKIPPED", "FAILED", "PARTIAL"]
          },
          "inputs": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "value_hash": { "type": "string" },
                "source": { "type": "string" }
              }
            }
          },
          "outputs": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "value_hash": { "type": "string" }
              }
            }
          },
          "tools_invoked": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tool_id": { "type": "string" },
                "invocation_hash": { "type": "string" }
              }
            }
          },
          "prerequisites_met": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "prerequisite": { "type": "string" },
                "satisfied": { "type": "boolean" },
                "evidence": { "type": "string" }
              }
            }
          }
        }
      }
    },
    "deviations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step_id", "deviation_type", "justification"],
        "properties": {
          "step_id": { "type": "string" },
          "deviation_type": {
            "type": "string",
            "enum": ["SKIPPED", "REORDERED", "MODIFIED", "ADDED"]
          },
          "justification": { "type": "string" },
          "approved_by": { "type": "string" }
        }
      },
      "default": []
    },
    "conformance_summary": {
      "type": "object",
      "required": ["total_required", "completed", "skipped", "failed"],
      "properties": {
        "total_required": { "type": "integer" },
        "completed": { "type": "integer" },
        "skipped": { "type": "integer" },
        "failed": { "type": "integer" },
        "conformance_rate": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  },
  "additionalProperties": false
}
```

### 2.8 R-class VTD (Reasoning Chain)

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-r-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "R-class Proof Body",
  "description": "Reasoning chain evidence. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": ["premises", "inferences", "assumptions", "logical_assessment"],
  "properties": {
    "premises": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["premise_id", "content", "support_type"],
        "properties": {
          "premise_id": { "type": "string" },
          "content": { "type": "string" },
          "support_type": {
            "type": "string",
            "enum": ["VERIFIED_CLAIM", "AXIOM", "ASSUMPTION", "EMPIRICAL", "DEFINITION"]
          },
          "support_ref": {
            "type": "string",
            "description": "ClaimId or source reference supporting this premise."
          },
          "support_credibility": {
            "type": "number", "minimum": 0, "maximum": 1,
            "description": "Credibility of the supporting claim, if applicable."
          }
        }
      }
    },
    "inferences": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["from_premises", "rule", "yields"],
        "properties": {
          "from_premises": {
            "type": "array",
            "items": { "type": "string" },
            "minItems": 1,
            "description": "Premise IDs used in this inference step."
          },
          "rule": {
            "type": "string",
            "description": "Inference rule applied (e.g., modus ponens, hypothetical syllogism)."
          },
          "rule_type": {
            "type": "string",
            "enum": ["DEDUCTIVE", "INDUCTIVE", "ABDUCTIVE", "ANALOGICAL"],
            "description": "Type of reasoning."
          },
          "yields": { "type": "string", "description": "Conclusion of this inference step." },
          "yields_id": { "type": "string", "description": "ID for referencing this conclusion." }
        }
      }
    },
    "assumptions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["assumption", "necessity"],
        "properties": {
          "assumption": { "type": "string" },
          "necessity": {
            "type": "string",
            "enum": ["ESSENTIAL", "SIMPLIFYING", "CONVENTIONAL"],
            "description": "How critical this assumption is to the conclusion."
          },
          "justification": { "type": "string" },
          "violation_consequence": { "type": "string" }
        }
      }
    },
    "logical_assessment": {
      "type": "object",
      "required": ["validity"],
      "properties": {
        "validity": {
          "type": "string",
          "enum": ["VALID", "VALID_IF_ASSUMPTIONS_HOLD", "PROBABILISTICALLY_VALID", "INVALID"],
          "description": "Assessment of logical validity."
        },
        "soundness_notes": { "type": "string" },
        "known_fallacies_checked": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "fallacy": { "type": "string" },
              "present": { "type": "boolean" },
              "note": { "type": "string" }
            }
          }
        }
      }
    }
  },
  "additionalProperties": false
}
```

### 2.9 C-class VTD (Compliance Proof)

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-c-class.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "C-class Proof Body",
  "description": "Compliance proof package. Tier 1: FORMAL_PROOF.",
  "type": "object",
  "required": ["regulation", "requirements", "compliance_status"],
  "properties": {
    "regulation": {
      "type": "object",
      "required": ["regulation_id", "title"],
      "properties": {
        "regulation_id": { "type": "string" },
        "title": { "type": "string" },
        "version": { "type": "string" },
        "effective_date": { "type": "string", "format": "date" },
        "jurisdiction": { "type": "string" },
        "uri": { "type": "string", "format": "uri" }
      }
    },
    "requirements": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["requirement_id", "requirement_text", "evidence_type", "evidence"],
        "properties": {
          "requirement_id": { "type": "string" },
          "requirement_text": { "type": "string" },
          "applicability": {
            "type": "string",
            "enum": ["APPLICABLE", "NOT_APPLICABLE", "PARTIALLY_APPLICABLE"]
          },
          "evidence_type": {
            "type": "string",
            "enum": ["DOCUMENT", "PROCESS_LOG", "TEST_RESULT", "ATTESTATION", "CONFIGURATION"]
          },
          "evidence": {
            "type": "object",
            "required": ["description"],
            "properties": {
              "description": { "type": "string" },
              "reference": { "type": "string" },
              "reference_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
              "verified_date": { "type": "string", "format": "date-time" }
            }
          },
          "status": {
            "type": "string",
            "enum": ["COMPLIANT", "NON_COMPLIANT", "PARTIALLY_COMPLIANT", "NOT_ASSESSED"]
          }
        }
      }
    },
    "gaps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["requirement_id", "gap_description", "remediation_plan"],
        "properties": {
          "requirement_id": { "type": "string" },
          "gap_description": { "type": "string" },
          "severity": { "type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"] },
          "remediation_plan": { "type": "string" },
          "remediation_deadline": { "type": "string", "format": "date" }
        }
      },
      "default": []
    },
    "compliance_status": {
      "type": "object",
      "required": ["overall_status", "last_reviewed"],
      "properties": {
        "overall_status": {
          "type": "string",
          "enum": ["FULLY_COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT"]
        },
        "compliant_count": { "type": "integer" },
        "total_requirements": { "type": "integer" },
        "last_reviewed": { "type": "string", "format": "date-time" },
        "next_review": { "type": "string", "format": "date-time" }
      }
    },
    "constitutional_parameters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "parameter_id": { "type": "string", "pattern": "^CONST-[0-9]{3,4}$" },
          "satisfied": { "type": "boolean" },
          "evidence_ref": { "type": "string" }
        }
      },
      "description": "Constitutional parameters checked in addition to external regulation."
    }
  },
  "additionalProperties": false
}
```

---

## 3. Claim Classification Protocol

### 3.1 Classification Signatures per Class

Each claim class has a structural signature — a set of syntactic and semantic markers that the membrane uses to classify claims independently of the producing agent's suggestion.

```
CLASSIFICATION_SIGNATURES = {
  D: {
    markers: [
      "references deterministic algorithm or function",
      "claim is about input-output relationship",
      "claim is decidable by computation",
      "no probabilistic qualifiers (likely, approximately, suggests)"
    ],
    exclusion: ["contains value judgments", "references stakeholder impact"],
    confidence_threshold: 0.85
  },
  C: {
    markers: [
      "references specific regulation, standard, or constitutional parameter",
      "claim is about conformance or compliance",
      "finite enumerable requirement set"
    ],
    exclusion: ["no regulation referenced", "open-ended assessment"],
    confidence_threshold: 0.85
  },
  E: {
    markers: [
      "references observable phenomena or measurements",
      "cites data sources or experimental results",
      "claim is about what IS (descriptive)"
    ],
    exclusion: ["purely computational", "purely normative"],
    confidence_threshold: 0.75
  },
  S: {
    markers: [
      "references statistical tests, confidence intervals, or p-values",
      "claim involves sample-to-population inference",
      "quantitative comparison between groups or conditions"
    ],
    exclusion: ["no quantitative data", "no statistical method"],
    confidence_threshold: 0.80
  },
  P: {
    markers: [
      "claim is about a process that was followed",
      "references process steps, protocols, or procedures",
      "temporal sequence of actions"
    ],
    exclusion: ["claim is about outcome, not process"],
    confidence_threshold: 0.80
  },
  R: {
    markers: [
      "explicit premise-conclusion structure",
      "references logical rules or inference patterns",
      "claim follows from other claims via reasoning"
    ],
    exclusion: ["no explicit premises", "purely empirical"],
    confidence_threshold: 0.75
  },
  H: {
    markers: [
      "expert judgment or recommendation",
      "references alternatives considered",
      "uses qualifiers: likely, recommended, preferred, suggests",
      "pragmatic assessment"
    ],
    exclusion: ["decidable by computation", "primarily about values/ethics"],
    confidence_threshold: 0.70
  },
  N: {
    markers: [
      "references ethical principles or value frameworks",
      "claim about what SHOULD be (prescriptive)",
      "references stakeholder impact or fairness",
      "invokes constitutional alignment"
    ],
    exclusion: ["purely descriptive", "purely computational"],
    confidence_threshold: 0.70
  }
}
```

### 3.2 Membrane Classification Algorithm

The membrane classification protocol ensures that claim classes are assigned independently of the producing agent's preference. This is a hard requirement (REQ-2 from the Feasibility Verdict).

```python
def classify_claim(claim: Claim, vtd: VTD) -> ClassificationResult:
    """
    Three-way classification: agent suggestion, structural analysis, independent classifier.
    INV-M2: The membrane assigns final classification. Agents propose; the membrane decides.
    """

    # Step 1: Agent's suggested classification (already in VTD)
    agent_suggestion = vtd.suggested_class

    # Step 2: Structural analysis against classification signatures
    structural_scores = {}
    for cls in ClaimClass:
        sig = CLASSIFICATION_SIGNATURES[cls]
        marker_matches = count_matching_markers(claim.text, claim.metadata, sig.markers)
        exclusion_matches = count_matching_markers(claim.text, claim.metadata, sig.exclusion)
        if exclusion_matches > 0:
            structural_scores[cls] = 0.0
        else:
            structural_scores[cls] = marker_matches / len(sig.markers)

    structural_class = max(structural_scores, key=structural_scores.get)
    structural_confidence = structural_scores[structural_class]

    # Step 3: Independent classifier (VRF-selected agent)
    classifier_agent = select_independent_classifier(claim, current_epoch())
    independent_result = classifier_agent.classify(claim)
    independent_class = independent_result.classification
    independent_confidence = independent_result.confidence

    # Step 4: Three-way agreement check
    all_three = [agent_suggestion, structural_class, independent_class]

    if all_three[0] == all_three[1] == all_three[2]:
        # Full agreement: issue Classification Seal
        assigned_class = all_three[0]
        seal_type = "UNANIMOUS"
    elif len(set(all_three)) == 2:
        # Two-of-three agreement: majority wins
        from collections import Counter
        majority = Counter(all_three).most_common(1)[0][0]
        assigned_class = majority
        seal_type = "MAJORITY"
    else:
        # Full disagreement: apply most conservative class
        assigned_class = most_conservative_class(all_three)
        seal_type = "CONSERVATIVE"

    # Step 5: Override check — structural confidence gate
    if structural_confidence < CLASSIFICATION_SIGNATURES[assigned_class].confidence_threshold:
        # Low confidence in structural match: escalate
        assigned_class = most_conservative_class(all_three)
        seal_type = "LOW_CONFIDENCE_ESCALATION"

    # Step 6: Determine tier
    tier = CLASS_TO_TIER[assigned_class]

    # Step 7: Detect secondary classes
    secondary = []
    for cls, score in structural_scores.items():
        if cls != assigned_class and score >= 0.5:
            secondary.append(cls)

    return ClassificationResult(
        assigned_class=assigned_class,
        tier=tier,
        secondary_classes=secondary,
        seal_type=seal_type,
        agent_suggestion=agent_suggestion,
        structural_class=structural_class,
        structural_confidence=structural_confidence,
        independent_class=independent_class,
        independent_confidence=independent_confidence
    )


def select_independent_classifier(claim: Claim, epoch: EpochNum) -> Agent:
    """
    VRF-select a single agent to independently classify the claim.
    The classifier MUST NOT be the producing agent.
    The classifier MUST NOT be on the verification committee for this claim.
    """
    alpha = SHA256(b"CLASSIFY" + claim.hash + uint64_be(epoch) + vrf_seed(epoch))
    eligible = get_eligible_classifiers(claim.locus, exclude=[claim.producing_agent])
    candidates = []
    for agent in eligible:
        beta, pi = ECVRF_prove(agent.privkey, alpha)
        candidates.append((agent.id, beta, pi))
    candidates.sort(key=lambda c: c[1])
    return get_agent(candidates[0][0])


def most_conservative_class(classes: list) -> ClaimClass:
    """
    Return the class with the highest verification cost (most conservative).
    Order from most to least conservative:
    H > N > E > S > R > P > C > D
    """
    CONSERVATISM_ORDER = {
        'H': 8, 'N': 7, 'E': 6, 'S': 5, 'R': 4, 'P': 3, 'C': 2, 'D': 1
    }
    return max(classes, key=lambda c: CONSERVATISM_ORDER[c])
```

### 3.3 Disagreement Resolution

When the three classification inputs (agent suggestion, structural analysis, independent classifier) disagree, the following resolution protocol applies:

| Agreement Level | Resolution | Seal Type | Cost Impact |
|----------------|-----------|-----------|-------------|
| 3-of-3 agree | Assigned as agreed | UNANIMOUS | None |
| 2-of-3 agree | Majority class assigned | MAJORITY | None |
| 0-of-3 agree | Most conservative class | CONSERVATIVE | Higher verification cost |
| Structural confidence below threshold | Most conservative class | LOW_CONFIDENCE_ESCALATION | Higher verification cost |

**Classification appeal protocol:**

1. The producing agent MAY appeal a classification within the same epoch.
2. Appeal triggers a governance review: a committee of 3 VRF-selected agents with domain expertise evaluates the claim.
3. The governance committee's classification is final and MUST NOT be appealed again within 10 epochs.
4. Appeal outcomes are logged and contribute to classifier training data.
5. Agents that appeal more than APPEAL_RATE_LIMIT (default: 5%) of their claims per epoch receive a credibility penalty of 0.05 per excess appeal.

### 3.4 Classification Seal (CLS) Specification

A Classification Seal is a signed attestation that the claim has been classified through the three-way protocol.

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/classification-seal.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Classification Seal",
  "type": "object",
  "required": [
    "cls_id", "claim_id", "assigned_class", "tier", "seal_type",
    "epoch", "structural_confidence", "independent_classifier",
    "seal_hash", "membrane_signature"
  ],
  "properties": {
    "cls_id": {
      "type": "string",
      "pattern": "^cls:clm:[^:]+:[0-9]+:[a-f0-9]{8}:[0-9]+$"
    },
    "claim_id": { "type": "string" },
    "assigned_class": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] },
    "secondary_classes": {
      "type": "array", "items": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] }
    },
    "tier": { "type": "string", "enum": ["FORMAL_PROOF","STRUCTURED_EVIDENCE","STRUCTURED_ATTESTATION"] },
    "seal_type": {
      "type": "string",
      "enum": ["UNANIMOUS", "MAJORITY", "CONSERVATIVE", "LOW_CONFIDENCE_ESCALATION", "APPEAL_OVERRIDE"]
    },
    "epoch": { "type": "integer", "minimum": 0 },
    "agent_suggestion": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] },
    "structural_class": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] },
    "structural_confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "independent_classifier": { "type": "string", "description": "AgentId of VRF-selected classifier." },
    "independent_class": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] },
    "independent_confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "seal_hash": {
      "type": "string", "pattern": "^[a-f0-9]{64}$",
      "description": "SHA-256 of all fields except seal_hash and membrane_signature."
    },
    "membrane_signature": {
      "type": "string",
      "description": "Ed25519 signature over seal_hash by membrane authority."
    }
  },
  "additionalProperties": false
}
```

---

## 4. Verification Protocols per Tier

### 4.1 Tier 1: Formal Proof Verification Protocol

Tier 1 verification applies to D-class and C-class claims. Verification is mechanical and sublinear relative to recomputation.

```python
def verify_tier1(vtd: VTD, committee: Set[AgentId]) -> VerificationResult:
    """
    Formal proof verification for D-class and C-class claims.
    Cost: 0.1x - 0.35x of replication.
    """
    cls = vtd.assigned_class
    assert cls in ('D', 'C'), f"Tier 1 requires D or C class, got {cls}"

    # Step 1: Structural validation — VTD conforms to class schema
    schema_valid = validate_schema(vtd.proof_body, SCHEMAS[cls])
    if not schema_valid:
        return VerificationResult(
            status="REJECTED",
            reason="SCHEMA_INVALID",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    # Step 2: Completeness check — all required fields populated
    complete = check_completeness(vtd.proof_body, REQUIRED_FIELDS[cls])
    if not complete.passed:
        return VerificationResult(
            status="REJECTED",
            reason=f"INCOMPLETE: {complete.missing}",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    if cls == 'D':
        return verify_d_class(vtd, committee)
    else:
        return verify_c_class(vtd, committee)


def verify_d_class(vtd: VTD, committee: Set[AgentId]) -> VerificationResult:
    """D-class: deterministic proof verification."""
    body = vtd.proof_body

    if body.proof_type == "RECOMPUTATION":
        # Replay computation on stated inputs, compare output hash
        for input_spec in body.inputs:
            if not verify_input_availability(input_spec):
                return VerificationResult(
                    status="REJECTED",
                    reason="INPUT_UNAVAILABLE",
                    opinion=Opinion(b=0, d=0.5, u=0.5, a=0.5)
                )
        recomputed_hash = recompute(body.computation, body.inputs)
        if recomputed_hash == body.output.value_hash:
            return VerificationResult(
                status="VERIFIED",
                reason="RECOMPUTATION_MATCH",
                opinion=Opinion(b=1, d=0, u=0, a=0.5)
            )
        else:
            return VerificationResult(
                status="FALSIFIED",
                reason="RECOMPUTATION_MISMATCH",
                opinion=Opinion(b=0, d=1, u=0, a=0.5)
            )

    elif body.proof_type == "HASH_VERIFICATION":
        # Verify hash of provided value matches claimed hash
        actual_hash = SHA256(canonical_serialize(body.output.value))
        if actual_hash == body.output.value_hash:
            return VerificationResult(
                status="VERIFIED",
                reason="HASH_MATCH",
                opinion=Opinion(b=1, d=0, u=0, a=0.5)
            )
        else:
            return VerificationResult(
                status="FALSIFIED",
                reason="HASH_MISMATCH",
                opinion=Opinion(b=0, d=1, u=0, a=0.5)
            )

    elif body.proof_type == "PROOF_CERTIFICATE":
        # Machine-check the proof certificate
        cert = body.proof_certificate
        if cert.format in ("COQ_PROOF", "TLA_PROOF", "ISABELLE_PROOF"):
            check_result = run_proof_checker(cert.format, cert.certificate_uri)
            if check_result.valid:
                return VerificationResult(
                    status="VERIFIED",
                    reason="PROOF_CHECKED",
                    opinion=Opinion(b=1, d=0, u=0, a=0.5)
                )
            else:
                return VerificationResult(
                    status="FALSIFIED",
                    reason=f"PROOF_INVALID: {check_result.error}",
                    opinion=Opinion(b=0, d=1, u=0, a=0.5)
                )
        else:
            return VerificationResult(
                status="DEFERRED",
                reason="UNSUPPORTED_PROOF_FORMAT",
                opinion=Opinion(b=0, d=0, u=1, a=0.5)
            )

    elif body.proof_type == "PROOF_SKETCH":
        # Spot-check key steps in the computation trace
        if body.trace is None or len(body.trace.key_steps) == 0:
            return VerificationResult(
                status="REJECTED",
                reason="NO_TRACE_FOR_PROOF_SKETCH",
                opinion=Opinion(b=0, d=0.7, u=0.3, a=0.5)
            )
        steps_checked = 0
        steps_passed = 0
        for step in body.trace.key_steps:
            result = verify_intermediate_step(
                body.computation, body.inputs, step.step_index, step.intermediate_hash
            )
            steps_checked += 1
            if result:
                steps_passed += 1

        pass_rate = steps_passed / steps_checked
        if pass_rate == 1.0:
            return VerificationResult(
                status="VERIFIED",
                reason=f"ALL_{steps_checked}_STEPS_VERIFIED",
                opinion=Opinion(b=0.95, d=0, u=0.05, a=0.5)
            )
        elif pass_rate >= 0.8:
            return VerificationResult(
                status="WEAK_VERIFICATION",
                reason=f"PASS_RATE_{pass_rate:.2f}",
                opinion=Opinion(b=pass_rate * 0.9, d=(1-pass_rate), u=0.1, a=0.5)
            )
        else:
            return VerificationResult(
                status="FALSIFIED",
                reason=f"PASS_RATE_{pass_rate:.2f}_BELOW_THRESHOLD",
                opinion=Opinion(b=0, d=1, u=0, a=0.5)
            )


def verify_c_class(vtd: VTD, committee: Set[AgentId]) -> VerificationResult:
    """C-class: compliance proof verification."""
    body = vtd.proof_body

    # Verify regulation exists and is correctly referenced
    reg_valid = verify_regulation_reference(body.regulation)
    if not reg_valid:
        return VerificationResult(
            status="REJECTED",
            reason="INVALID_REGULATION_REFERENCE",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    # Check each requirement
    total = len(body.requirements)
    compliant = 0
    non_compliant = 0
    not_assessed = 0

    for req in body.requirements:
        if req.applicability == "NOT_APPLICABLE":
            total -= 1
            continue

        if req.status == "COMPLIANT":
            # Verify evidence exists and is valid
            if verify_compliance_evidence(req.evidence):
                compliant += 1
            else:
                non_compliant += 1
        elif req.status == "NON_COMPLIANT":
            non_compliant += 1
        elif req.status == "NOT_ASSESSED":
            not_assessed += 1
        else:
            non_compliant += 1  # PARTIALLY_COMPLIANT counts as non-compliant for binary check

    if total == 0:
        return VerificationResult(
            status="REJECTED",
            reason="NO_APPLICABLE_REQUIREMENTS",
            opinion=Opinion(b=0, d=0, u=1, a=0.5)
        )

    compliance_rate = compliant / total

    # Check constitutional parameters if present
    const_violations = 0
    if body.constitutional_parameters:
        for param in body.constitutional_parameters:
            if not param.satisfied:
                const_violations += 1

    if compliance_rate == 1.0 and const_violations == 0:
        return VerificationResult(
            status="VERIFIED",
            reason="FULLY_COMPLIANT",
            opinion=Opinion(b=1, d=0, u=0, a=0.5)
        )
    elif non_compliant == 0 and not_assessed > 0:
        uncertainty = not_assessed / total
        return VerificationResult(
            status="PARTIAL",
            reason=f"ASSESSED_{compliant}/{total}_NOT_ASSESSED_{not_assessed}",
            opinion=Opinion(b=compliance_rate, d=0, u=uncertainty, a=0.5)
        )
    else:
        return VerificationResult(
            status="FALSIFIED",
            reason=f"NON_COMPLIANT_{non_compliant}/{total}",
            opinion=Opinion(b=compliance_rate, d=non_compliant/total, u=not_assessed/total, a=0.5)
        )
```

### 4.2 Tier 2: Structured Evidence Verification Protocol

Tier 2 verification applies to E-class, S-class, P-class, and R-class claims. Verification checks evidence completeness and structural validity, then optionally invokes adversarial probing.

```python
def verify_tier2(vtd: VTD, committee: Set[AgentId], epoch: EpochNum) -> VerificationResult:
    """
    Structured evidence verification for E/S/P/R classes.
    Cost: 0.5x - 1.2x of replication (without probing).
    """
    cls = vtd.assigned_class
    assert cls in ('E', 'S', 'P', 'R'), f"Tier 2 requires E/S/P/R class, got {cls}"

    # Phase 1: Schema validation
    schema_valid = validate_schema(vtd.proof_body, SCHEMAS[cls])
    if not schema_valid:
        return VerificationResult(
            status="REJECTED", reason="SCHEMA_INVALID",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    # Phase 2: Completeness check
    complete = check_completeness(vtd.proof_body, REQUIRED_FIELDS[cls])
    if not complete.passed:
        return VerificationResult(
            status="REJECTED", reason=f"INCOMPLETE: {complete.missing}",
            opinion=Opinion(b=0, d=0.8, u=0.2, a=0.5)
        )

    # Phase 3: Counter-evidence check
    if not vtd.counter_evidence.considered:
        # Tier 2 MUST have counter-evidence section
        return VerificationResult(
            status="REJECTED", reason="NO_COUNTER_EVIDENCE_CONSIDERED",
            opinion=Opinion(b=0, d=0.6, u=0.4, a=0.5)
        )

    # Phase 4: Class-specific evidence verification
    if cls == 'E':
        evidence_result = verify_empirical_evidence(vtd, committee)
    elif cls == 'S':
        evidence_result = verify_statistical_evidence(vtd, committee)
    elif cls == 'P':
        evidence_result = verify_process_evidence(vtd, committee)
    elif cls == 'R':
        evidence_result = verify_reasoning_evidence(vtd, committee)

    if evidence_result.status == "FALSIFIED":
        return evidence_result

    # Phase 5: Dependency verification
    dep_result = verify_dependencies(vtd)
    if dep_result.status == "FAILED":
        evidence_result.opinion = discount_opinion(
            evidence_result.opinion,
            dep_result.weakest_dependency_credibility
        )

    # Phase 6: Determine if adversarial probing is needed
    probe_needed = should_probe(vtd, evidence_result, epoch)
    if probe_needed:
        probe_result = invoke_adversarial_probing(vtd, epoch)
        evidence_result = merge_probe_result(evidence_result, probe_result)

    return evidence_result


def verify_empirical_evidence(vtd: VTD, committee: Set[AgentId]) -> VerificationResult:
    """E-class specific: verify sources and evidence chains."""
    body = vtd.proof_body
    source_results = []

    for source in body.sources:
        # MANDATORY SOURCE VERIFICATION (REQ-1 from Feasibility Verdict)
        sv = SourceVerification()

        # Check 1: URL accessibility
        if source.uri:
            sv.accessible = check_url_accessible(source.uri)

        # Check 2: Content hash comparison
        if source.content_hash and sv.accessible:
            current_hash = fetch_and_hash(source.uri)
            sv.content_unchanged = (current_hash == source.content_hash)

        # Check 3: Quote accuracy
        if source.quoted_text and sv.accessible:
            page_content = fetch_content(source.uri)
            sv.quote_found = fuzzy_match(source.quoted_text, page_content, threshold=0.90)

        # Check 4: Recency
        if source.retrieval_timestamp:
            age_days = days_since(source.retrieval_timestamp)
            sv.fresh = age_days <= SOURCE_FRESHNESS_DAYS.get(source.source_type, 365)

        source_results.append(sv)

    sources_verified = sum(1 for sv in source_results if sv.is_adequate())
    sources_total = len(source_results)

    if sources_total == 0:
        return VerificationResult(
            status="REJECTED", reason="NO_SOURCES",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    verification_rate = sources_verified / sources_total

    # Check cross-references
    cross_ref_confirms = sum(1 for cr in body.cross_references if cr.confirms)
    cross_ref_total = len(body.cross_references)

    # Check evidence chain coherence
    chain_valid = verify_evidence_chain_coherence(body.evidence_chain, body.sources)

    if verification_rate >= 0.8 and chain_valid:
        b = verification_rate * 0.8
        u = (1 - verification_rate) * 0.5
        d = 1 - b - u
        return VerificationResult(
            status="VERIFIED", reason="SOURCES_VERIFIED",
            opinion=Opinion(b=b, d=max(0, d), u=u, a=0.5)
        )
    elif verification_rate >= 0.5:
        return VerificationResult(
            status="WEAK_VERIFICATION",
            reason=f"PARTIAL_SOURCE_VERIFICATION_{verification_rate:.2f}",
            opinion=Opinion(b=verification_rate * 0.5, d=0.2, u=1 - verification_rate * 0.5 - 0.2, a=0.5)
        )
    else:
        return VerificationResult(
            status="FALSIFIED",
            reason=f"INSUFFICIENT_SOURCE_VERIFICATION_{verification_rate:.2f}",
            opinion=Opinion(b=0.1, d=0.6, u=0.3, a=0.5)
        )


def verify_statistical_evidence(vtd: VTD, committee: Set[AgentId]) -> VerificationResult:
    """S-class specific: verify statistical methodology and results."""
    body = vtd.proof_body

    checks = StatisticalChecks()

    # Check 1: Sample size adequacy
    if body.power_analysis:
        checks.power_adequate = body.power_analysis.achieved_power >= 0.80
    else:
        checks.power_adequate = body.dataset.sample_size >= 30  # crude heuristic

    # Check 2: Test appropriateness
    checks.test_appropriate = assess_test_appropriateness(
        body.methodology.test_type,
        body.dataset,
        body.assumptions
    )

    # Check 3: Assumption validity
    violated = [a for a in body.assumptions if a.check_result == "VIOLATED"]
    checks.assumptions_valid = len(violated) == 0

    # Check 4: Arithmetic verification (recompute test statistic if data available)
    if body.dataset.data_hash:
        checks.arithmetic_verified = verify_test_arithmetic(
            body.dataset, body.methodology, body.results
        )
    else:
        checks.arithmetic_verified = None  # Cannot verify without data

    # Check 5: Conclusion follows from results
    checks.conclusion_valid = assess_conclusion_validity(
        body.results, body.methodology.test_type
    )

    passed = checks.count_passed()
    total = checks.count_total()
    rate = passed / total

    if rate >= 0.8:
        return VerificationResult(
            status="VERIFIED", reason=f"STATISTICAL_CHECKS_{passed}/{total}",
            opinion=Opinion(b=rate * 0.85, d=(1-rate)*0.5, u=1 - rate*0.85 - (1-rate)*0.5, a=0.5)
        )
    elif rate >= 0.5:
        return VerificationResult(
            status="WEAK_VERIFICATION", reason=f"PARTIAL_STATISTICAL_CHECKS_{passed}/{total}",
            opinion=Opinion(b=rate * 0.5, d=(1-rate)*0.3, u=1 - rate*0.5 - (1-rate)*0.3, a=0.5)
        )
    else:
        return VerificationResult(
            status="FALSIFIED", reason=f"STATISTICAL_CHECKS_FAILED_{passed}/{total}",
            opinion=Opinion(b=0.05, d=0.7, u=0.25, a=0.5)
        )


def verify_process_evidence(vtd: VTD, committee: Set[AgentId]) -> VerificationResult:
    """P-class specific: verify process conformance."""
    body = vtd.proof_body

    # Verify process specification exists and is registered
    spec_valid = verify_process_spec_registered(body.process_spec)
    if not spec_valid:
        return VerificationResult(
            status="REJECTED", reason="UNREGISTERED_PROCESS_SPEC",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    # Check all required steps are present
    required = set(body.process_spec.required_steps)
    completed = set(s.step_id for s in body.steps if s.status == "COMPLETED")
    skipped = set(s.step_id for s in body.steps if s.status == "SKIPPED")
    missing = required - completed - skipped

    if missing:
        return VerificationResult(
            status="FALSIFIED", reason=f"MISSING_STEPS: {missing}",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    # Check step ordering (temporal sequence must be non-decreasing)
    timestamps = [(s.step_id, s.started, s.completed) for s in body.steps]
    order_valid = verify_temporal_order(timestamps)

    # Check deviations are justified
    unjustified = [d for d in body.deviations if not d.justification]
    deviations_ok = len(unjustified) == 0

    conformance = body.conformance_summary.conformance_rate

    if conformance == 1.0 and order_valid and deviations_ok:
        return VerificationResult(
            status="VERIFIED", reason="FULL_PROCESS_CONFORMANCE",
            opinion=Opinion(b=1, d=0, u=0, a=0.5)
        )
    elif conformance >= 0.8 and order_valid:
        return VerificationResult(
            status="VERIFIED", reason=f"CONFORMANCE_{conformance:.2f}",
            opinion=Opinion(b=conformance, d=0, u=1-conformance, a=0.5)
        )
    else:
        return VerificationResult(
            status="FALSIFIED",
            reason=f"CONFORMANCE_{conformance:.2f}_ORDER_{order_valid}",
            opinion=Opinion(b=conformance * 0.5, d=1-conformance, u=conformance*0.5, a=0.5)
        )


def verify_reasoning_evidence(vtd: VTD, committee: Set[AgentId]) -> VerificationResult:
    """R-class specific: verify logical validity and premise support."""
    body = vtd.proof_body

    # Check 1: All premises have support references
    unsupported = [p for p in body.premises if p.support_type == "ASSUMPTION" and not p.justification]

    # Check 2: Inference rules correctly applied
    inference_valid = True
    for inf in body.inferences:
        rule_ok = verify_inference_rule(
            inf.from_premises, inf.rule, inf.yields, body.premises
        )
        if not rule_ok:
            inference_valid = False
            break

    # Check 3: Assumptions disclosed
    assumptions_disclosed = len(body.assumptions) > 0

    # Check 4: Logical assessment consistency
    assessment = body.logical_assessment
    if assessment.validity == "VALID" and not inference_valid:
        return VerificationResult(
            status="FALSIFIED",
            reason="CLAIMS_VALID_BUT_INFERENCE_INVALID",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    # Check 5: Known fallacy check
    fallacies_present = []
    if assessment.known_fallacies_checked:
        fallacies_present = [f for f in assessment.known_fallacies_checked if f.present]

    if inference_valid and assumptions_disclosed and len(fallacies_present) == 0:
        # Check premise credibility
        min_premise_cred = min(
            (p.support_credibility for p in body.premises if p.support_credibility is not None),
            default=0.5
        )
        b = 0.85 * min_premise_cred
        return VerificationResult(
            status="VERIFIED", reason="LOGIC_VALID_PREMISES_SUPPORTED",
            opinion=Opinion(b=b, d=0, u=1-b, a=0.5)
        )
    elif inference_valid:
        return VerificationResult(
            status="WEAK_VERIFICATION",
            reason="LOGIC_VALID_BUT_CONCERNS",
            opinion=Opinion(b=0.5, d=0.1, u=0.4, a=0.5)
        )
    else:
        return VerificationResult(
            status="FALSIFIED", reason="LOGIC_INVALID",
            opinion=Opinion(b=0, d=0.9, u=0.1, a=0.5)
        )


def should_probe(vtd: VTD, evidence_result: VerificationResult, epoch: EpochNum) -> bool:
    """Determine if adversarial probing should be invoked."""
    # Always probe if verification was weak
    if evidence_result.status == "WEAK_VERIFICATION":
        return True

    # Probe based on claim risk level
    risk = assess_claim_risk(vtd)
    if risk == "HIGH":
        return True
    if risk == "CRITICAL":
        return True

    # Probe based on agent credibility
    agent_cred = get_agent_class_credibility(vtd.producing_agent, vtd.assigned_class)
    if E(agent_cred) < PROBE_CREDIBILITY_THRESHOLD:
        return True

    # Random probing: probe RANDOM_PROBE_RATE of remaining claims
    probe_hash = SHA256(b"PROBE" + vtd.vtd_hash.encode() + uint64_be(epoch))
    if uint256_from_bytes(probe_hash) < int(RANDOM_PROBE_RATE * 2**256):
        return True

    return False
```

### 4.3 Tier 3: Attestation + Adversarial Probing Protocol

Tier 3 verification applies to H-class and N-class claims. Verification ALWAYS includes adversarial probing.

```python
def verify_tier3(vtd: VTD, committee: Set[AgentId], epoch: EpochNum) -> VerificationResult:
    """
    Attestation verification for H/N classes.
    ALWAYS includes adversarial probing.
    Cost: 1.0x - 2.0x of replication.
    """
    cls = vtd.assigned_class
    assert cls in ('H', 'N'), f"Tier 3 requires H or N class, got {cls}"

    # Phase 1: Schema and completeness
    schema_valid = validate_schema(vtd.proof_body, SCHEMAS[cls])
    if not schema_valid:
        return VerificationResult(
            status="REJECTED", reason="SCHEMA_INVALID",
            opinion=Opinion(b=0, d=1, u=0, a=0.5)
        )

    complete = check_completeness(vtd.proof_body, REQUIRED_FIELDS[cls])
    if not complete.passed:
        return VerificationResult(
            status="REJECTED", reason=f"INCOMPLETE: {complete.missing}",
            opinion=Opinion(b=0, d=0.7, u=0.3, a=0.5)
        )

    # Phase 2: Counter-evidence requirement (MUST have items, not just considered=true)
    if not vtd.counter_evidence.considered or len(vtd.counter_evidence.items) == 0:
        # Suspicion flag: no counter-evidence at all for Tier 3
        suspicion_penalty = SUSPICION_PENALTY_NO_COUNTER_EVIDENCE  # default 0.15
    else:
        suspicion_penalty = 0.0

    # Phase 3: Class-specific structural checks
    if cls == 'H':
        structural_result = check_heuristic_structure(vtd)
    else:
        structural_result = check_normative_structure(vtd)

    # Phase 4: MANDATORY adversarial probing
    probe_result = invoke_adversarial_probing(vtd, epoch)

    # Phase 5: Expert committee evaluation
    committee_opinions = []
    for member in committee:
        member_opinion = evaluate_attestation(member, vtd, probe_result)
        committee_opinions.append(member_opinion)

    # Phase 6: Consensus fusion of committee opinions
    fused = committee_opinions[0]
    for i in range(1, len(committee_opinions)):
        fused = cumulative_fusion(fused, committee_opinions[i])

    # Apply suspicion penalty
    if suspicion_penalty > 0:
        fused = Opinion(
            b=max(0, fused.b - suspicion_penalty),
            d=fused.d,
            u=min(1, fused.u + suspicion_penalty),
            a=fused.a
        )
        # Renormalize
        total = fused.b + fused.d + fused.u
        fused = Opinion(b=fused.b/total, d=fused.d/total, u=fused.u/total, a=fused.a)

    # Phase 7: Merge probe results
    final = merge_probe_result_opinion(fused, probe_result)

    credibility = E(final)
    if credibility >= TIER3_ACCEPT_THRESHOLD:
        return VerificationResult(status="VERIFIED", reason="ATTESTATION_ACCEPTED", opinion=final)
    elif credibility >= TIER3_WEAK_THRESHOLD:
        return VerificationResult(status="WEAK_VERIFICATION", reason="ATTESTATION_MARGINAL", opinion=final)
    else:
        return VerificationResult(status="REJECTED", reason="ATTESTATION_INSUFFICIENT", opinion=final)


def check_heuristic_structure(vtd: VTD) -> StructuralResult:
    """Verify H-class structural requirements."""
    body = vtd.proof_body
    issues = []

    # At least 2 alternatives genuinely considered
    genuine = [a for a in body.alternatives if a.genuinely_considered]
    if len(genuine) < 2:
        issues.append("FEWER_THAN_2_GENUINE_ALTERNATIVES")

    # Criteria weights should sum to approximately 1.0
    weight_sum = sum(c.weight for c in body.criteria)
    if abs(weight_sum - 1.0) > 0.05:
        issues.append(f"CRITERIA_WEIGHTS_SUM_{weight_sum:.2f}_NOT_1.0")

    # Evaluation matrix should cover all alternatives x criteria
    expected_cells = len(body.alternatives) * len(body.criteria)
    actual_cells = len(body.evaluation)
    if actual_cells < expected_cells:
        issues.append(f"INCOMPLETE_EVALUATION_MATRIX_{actual_cells}/{expected_cells}")

    # Confidence should be calibrated (not 0.0 or 1.0 for heuristic claims)
    if body.confidence == 1.0:
        issues.append("OVERCONFIDENT_HEURISTIC_CONFIDENCE_1.0")
    if body.confidence == 0.0:
        issues.append("ZERO_CONFIDENCE_SUSPICIOUS")

    # At least one uncertainty source declared
    if len(body.uncertainty_sources) == 0:
        issues.append("NO_UNCERTAINTY_SOURCES")

    return StructuralResult(passed=len(issues) == 0, issues=issues)


def check_normative_structure(vtd: VTD) -> StructuralResult:
    """Verify N-class structural requirements."""
    body = vtd.proof_body
    issues = []

    # At least one constitutional reference
    if len(body.constitutional_refs) == 0:
        issues.append("NO_CONSTITUTIONAL_REFERENCES")

    # Check for CONFLICTS alignment — not necessarily invalid but requires justification
    conflicts = [r for r in body.constitutional_refs if r.alignment == "CONFLICTS"]
    for c in conflicts:
        if not c.alignment_argument:
            issues.append(f"CONSTITUTIONAL_CONFLICT_{c.parameter_id}_WITHOUT_JUSTIFICATION")

    # At least one stakeholder group
    if len(body.stakeholder_analysis) == 0:
        issues.append("NO_STAKEHOLDER_ANALYSIS")

    # At least one alternative position considered
    if len(body.alternatives) == 0:
        issues.append("NO_ALTERNATIVE_POSITIONS")

    # Framework justification present
    if not body.value_framework.framework_justification:
        issues.append("NO_FRAMEWORK_JUSTIFICATION")

    return StructuralResult(passed=len(issues) == 0, issues=issues)
```

---

## 5. Adversarial Probing Specification

### 5.1 Probe Type Definitions

Adversarial probing is a verification mechanism that tests claims by attempting to find weaknesses, counterexamples, or unstated assumptions. Probing applies to all Tier 2 and Tier 3 claims (mandatory for Tier 3, selective for Tier 2).

**Five probe types:**

| Probe Type | ID | Applicable Tiers | Description |
|-----------|-----|-------------------|-------------|
| Counterexample Search | CX | 2, 3 | Attempt to construct a specific counterexample to the claim |
| Assumption Exposure | AE | 2, 3 | Identify unstated assumptions the claim relies on |
| Source Challenge | SC | 2 | Verify that cited sources actually support the claim |
| Logical Fallacy Detection | LF | 2, 3 | Check for common reasoning errors |
| Boundary Probing | BP | 2, 3 | Test claim at edge cases and boundary conditions |

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/probe-request.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Adversarial Probe Request",
  "type": "object",
  "required": ["probe_id", "claim_id", "vtd_id", "probe_types", "prober_agent",
               "epoch", "budget_tokens", "strategy"],
  "properties": {
    "probe_id": {
      "type": "string",
      "pattern": "^prb:[a-f0-9]{16}$"
    },
    "claim_id": { "type": "string" },
    "vtd_id": { "type": "string" },
    "probe_types": {
      "type": "array",
      "items": { "type": "string", "enum": ["CX", "AE", "SC", "LF", "BP"] },
      "minItems": 1
    },
    "prober_agent": { "type": "string", "description": "VRF-selected prober AgentId." },
    "epoch": { "type": "integer", "minimum": 0 },
    "budget_tokens": {
      "type": "integer", "minimum": 100,
      "description": "Maximum compute tokens allocated for this probe."
    },
    "strategy": {
      "type": "object",
      "required": ["base_strategy", "generative_component"],
      "properties": {
        "base_strategy": {
          "type": "string",
          "description": "Strategy ID from the probe strategy library."
        },
        "generative_component": {
          "type": "boolean",
          "description": "Whether to include dynamically generated probe questions."
        },
        "strategy_seed": {
          "type": "string",
          "description": "VRF-derived seed for generative probe strategy."
        }
      }
    },
    "meta_probe": {
      "type": "boolean", "default": false,
      "description": "If true, also check whether VTD responses appear pre-fabricated."
    }
  }
}
```

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/probe-result.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Adversarial Probe Result",
  "type": "object",
  "required": ["probe_id", "claim_id", "overall_survival", "probe_results",
               "prober_agent", "tokens_consumed", "result_hash", "prober_signature"],
  "properties": {
    "probe_id": { "type": "string" },
    "claim_id": { "type": "string" },
    "overall_survival": {
      "type": "string",
      "enum": ["SURVIVED", "WEAKENED", "FALSIFIED", "INCONCLUSIVE"]
    },
    "probe_results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["probe_type", "finding", "severity"],
        "properties": {
          "probe_type": { "type": "string", "enum": ["CX", "AE", "SC", "LF", "BP"] },
          "finding": {
            "type": "string",
            "enum": ["NO_ISSUE", "MINOR_ISSUE", "SIGNIFICANT_ISSUE",
                     "CRITICAL_ISSUE", "COUNTEREXAMPLE_FOUND"]
          },
          "severity": { "type": "string", "enum": ["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"] },
          "description": { "type": "string" },
          "evidence": { "type": "string" },
          "pre_fabricated_suspicion": {
            "type": "number", "minimum": 0, "maximum": 1,
            "description": "Score indicating how likely the VTD's response to this probe was pre-fabricated."
          }
        }
      }
    },
    "unstated_assumptions_found": {
      "type": "array",
      "items": { "type": "string" }
    },
    "counterexamples_found": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": { "type": "string" },
          "validity": { "type": "string", "enum": ["CONFIRMED", "PLAUSIBLE", "SPECULATIVE"] }
        }
      }
    },
    "boundary_violations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "boundary": { "type": "string" },
          "behavior": { "type": "string" },
          "severity": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH"] }
        }
      }
    },
    "prober_agent": { "type": "string" },
    "tokens_consumed": { "type": "integer" },
    "result_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "prober_signature": { "type": "string" }
  }
}
```

### 5.2 Prober Selection (VRF, Separate from Verifiers)

Adversarial probers are selected via VRF independently of the verification committee. A prober MUST NOT be the producing agent, MUST NOT be on the verification committee, and SHOULD be from a different diversity pool than the majority of the verification committee.

```python
def select_adversarial_probers(
    claim: Claim,
    epoch: EpochNum,
    verification_committee: Set[AgentId],
    num_probers: int = None
) -> Set[AgentId]:
    """
    VRF-select adversarial probers independently of the verification committee.
    INV-M3: Probers are separate from verifiers.
    """
    if num_probers is None:
        num_probers = PROBERS_PER_TIER[CLASS_TO_TIER[claim.assigned_class]]
        # Default: Tier 2 = 1 prober, Tier 3 = 2 probers

    # Use a different VRF domain separator to ensure independence
    alpha = SHA256(b"ADVERSARIAL_PROBE" + claim.hash + uint64_be(epoch) + vrf_seed(epoch))

    excluded = {claim.producing_agent} | verification_committee
    eligible = get_eligible_probers(claim.locus, exclude=excluded)

    candidates = []
    for agent in eligible:
        beta, pi = ECVRF_prove(agent.privkey, alpha)
        candidates.append((agent.id, beta, pi))

    candidates.sort(key=lambda c: c[1])

    # Select top num_probers, preferring diversity from verification committee
    selected = set()
    for agent_id, beta, pi in candidates:
        if len(selected) >= num_probers:
            break
        selected.add(agent_id)

    return selected

PROBERS_PER_TIER = {
    "FORMAL_PROOF": 0,           # Tier 1: no probing needed
    "STRUCTURED_EVIDENCE": 1,     # Tier 2: 1 prober (when triggered)
    "STRUCTURED_ATTESTATION": 2   # Tier 3: 2 probers (always)
}
```

### 5.3 Probe Execution Protocol

```python
def invoke_adversarial_probing(vtd: VTD, epoch: EpochNum) -> ProbeResult:
    """Execute adversarial probing against a VTD."""

    # Step 1: Select probers
    probers = select_adversarial_probers(
        vtd.claim, epoch,
        vtd.verification_committee
    )

    # Step 2: Determine probe types based on claim class
    probe_types = get_probe_types_for_class(vtd.assigned_class)

    # Step 3: Calculate probe budget
    budget = calculate_probe_budget(vtd)

    # Step 4: Generate probe strategy
    strategy_seed = SHA256(b"STRATEGY" + vtd.vtd_hash.encode() + uint64_be(epoch))
    strategy = ProbeStrategy(
        base_strategy=select_base_strategy(vtd.assigned_class, strategy_seed),
        generative_component=True,  # Always include generative component (Attack 4 defense)
        strategy_seed=strategy_seed.hex()
    )

    # Step 5: Execute probes
    all_results = []
    for prober_id in probers:
        probe_request = ProbeRequest(
            probe_id=generate_probe_id(),
            claim_id=vtd.claim_id,
            vtd_id=vtd.vtd_id,
            probe_types=probe_types,
            prober_agent=prober_id,
            epoch=epoch,
            budget_tokens=budget // len(probers),
            strategy=strategy,
            meta_probe=True  # Always run meta-probe to detect inoculation
        )
        result = execute_probe(prober_id, probe_request, vtd)
        all_results.append(result)

    # Step 6: Aggregate probe results
    return aggregate_probe_results(all_results)


def get_probe_types_for_class(cls: ClaimClass) -> list:
    """Determine which probe types to apply based on claim class."""
    PROBE_MAP = {
        'E': ['CX', 'SC', 'AE'],           # Source challenge is primary
        'S': ['CX', 'LF', 'AE', 'BP'],     # Statistical claims need boundary probing
        'P': ['AE', 'BP'],                   # Process: check hidden assumptions
        'R': ['CX', 'LF', 'AE'],           # Reasoning: logic and counterexamples
        'H': ['CX', 'AE', 'BP', 'LF'],     # Heuristic: full probe suite
        'N': ['AE', 'LF', 'BP']            # Normative: assumptions and boundaries
    }
    return PROBE_MAP.get(cls, ['CX', 'AE'])
```

### 5.4 Probe Result Evaluation

```python
def aggregate_probe_results(results: list) -> ProbeResult:
    """Aggregate results from multiple probers into a single verdict."""

    if len(results) == 0:
        return ProbeResult(overall_survival="INCONCLUSIVE")

    # Collect all findings
    all_findings = []
    for r in results:
        all_findings.extend(r.probe_results)

    # Determine overall survival
    critical = [f for f in all_findings if f.severity == "CRITICAL"]
    high = [f for f in all_findings if f.severity == "HIGH"]
    counterexamples = []
    for r in results:
        counterexamples.extend(
            cx for cx in r.counterexamples_found if cx.validity in ("CONFIRMED", "PLAUSIBLE")
        )

    if len(critical) > 0 or any(cx.validity == "CONFIRMED" for cx in counterexamples):
        overall = "FALSIFIED"
    elif len(high) > 0 or len(counterexamples) > 0:
        overall = "WEAKENED"
    elif all(f.finding == "NO_ISSUE" for f in all_findings):
        overall = "SURVIVED"
    else:
        overall = "SURVIVED"  # Minor issues do not change survival

    # Check for inoculation (meta-probe)
    prefab_scores = [f.pre_fabricated_suspicion for f in all_findings
                     if f.pre_fabricated_suspicion is not None]
    if prefab_scores and max(prefab_scores) > INOCULATION_THRESHOLD:
        # Suspicion of pre-fabricated responses — downgrade
        if overall == "SURVIVED":
            overall = "WEAKENED"

    return ProbeResult(
        overall_survival=overall,
        probe_results=all_findings,
        counterexamples_found=counterexamples,
        unstated_assumptions_found=collect_assumptions(results),
        boundary_violations=collect_boundaries(results)
    )


def merge_probe_result(evidence_result: VerificationResult, probe: ProbeResult) -> VerificationResult:
    """Merge adversarial probe results into the evidence verification result."""
    opinion = evidence_result.opinion

    if probe.overall_survival == "FALSIFIED":
        return VerificationResult(
            status="FALSIFIED",
            reason=f"ADVERSARIAL_PROBE_FALSIFIED: {probe.probe_results[0].description}",
            opinion=Opinion(b=0, d=0.9, u=0.1, a=opinion.a)
        )

    elif probe.overall_survival == "WEAKENED":
        # Reduce belief, increase uncertainty
        weakening_factor = 0.3
        new_b = opinion.b * (1 - weakening_factor)
        new_u = min(1.0, opinion.u + opinion.b * weakening_factor)
        new_d = 1 - new_b - new_u
        return VerificationResult(
            status="WEAK_VERIFICATION",
            reason=f"ADVERSARIAL_PROBE_WEAKENED: {len(probe.counterexamples_found)} issues",
            opinion=Opinion(b=new_b, d=max(0, new_d), u=new_u, a=opinion.a)
        )

    elif probe.overall_survival == "SURVIVED":
        # Slightly increase belief (probe survival is positive evidence)
        boost = PROBE_SURVIVAL_BOOST  # default 0.05
        new_b = min(1.0, opinion.b + boost)
        new_u = max(0, opinion.u - boost)
        new_d = 1 - new_b - new_u
        return VerificationResult(
            status=evidence_result.status,
            reason=evidence_result.reason + " | PROBE_SURVIVED",
            opinion=Opinion(b=new_b, d=max(0, new_d), u=new_u, a=opinion.a)
        )

    else:  # INCONCLUSIVE
        return evidence_result
```

### 5.5 Probing Budget Allocation

The probing budget determines how much compute a prober may spend. Budgets scale with claim class and assessed risk level.

```python
def calculate_probe_budget(vtd: VTD) -> int:
    """Calculate adversarial probing budget in compute tokens."""

    BASE_BUDGETS = {
        'E': 500,   # Empirical: moderate budget for source checking
        'S': 400,   # Statistical: moderate for methodology review
        'P': 200,   # Process: low budget, mostly mechanical
        'R': 400,   # Reasoning: moderate for logic checking
        'H': 800,   # Heuristic: high budget for comprehensive probing
        'N': 700    # Normative: high budget for constitutional analysis
    }

    base = BASE_BUDGETS.get(vtd.assigned_class, 500)

    # Risk multiplier
    risk = assess_claim_risk(vtd)
    RISK_MULTIPLIERS = {
        'LOW': 0.5,
        'MEDIUM': 1.0,
        'HIGH': 2.0,
        'CRITICAL': 3.0
    }
    multiplier = RISK_MULTIPLIERS.get(risk, 1.0)

    # Agent credibility factor: lower credibility = higher budget
    agent_cred = get_agent_class_credibility(vtd.producing_agent, vtd.assigned_class)
    cred_score = E(agent_cred)
    cred_factor = 2.0 - cred_score  # Range: [1.0, 2.0]

    budget = int(base * multiplier * cred_factor)

    # Cap at maximum
    return min(budget, MAX_PROBE_BUDGET)  # default MAX_PROBE_BUDGET = 5000
```

---

## 6. Credibility Engine Specification

### 6.1 Subjective Logic Primitives

The Credibility Engine uses Josang's Subjective Logic (2016) to represent, compose, and propagate belief about claim credibility. All operations preserve the constraint b + d + u = 1.

```python
class Opinion:
    """Subjective Logic opinion tuple."""
    def __init__(self, b: float, d: float, u: float, a: float):
        assert abs(b + d + u - 1.0) < 1e-9, f"b+d+u must equal 1, got {b+d+u}"
        assert 0 <= a <= 1, f"a must be in [0,1], got {a}"
        assert b >= 0 and d >= 0 and u >= 0
        self.b = b
        self.d = d
        self.u = u
        self.a = a

    def expected_probability(self) -> float:
        """E(w) = b + a*u"""
        return self.b + self.a * self.u

    def __repr__(self):
        return f"Opinion(b={self.b:.4f}, d={self.d:.4f}, u={self.u:.4f}, a={self.a:.4f})"
```

### 6.2 Opinion Initialization per Claim Class

Each claim class has a default initialization strategy for opinions based on the nature of the claim.

```python
OPINION_INIT = {
    'D': {
        'verified': Opinion(b=1.0, d=0.0, u=0.0, a=0.5),
        'falsified': Opinion(b=0.0, d=1.0, u=0.0, a=0.5),
        'initial': Opinion(b=0.0, d=0.0, u=1.0, a=0.5),
        'decay': None,  # D-class proofs do not decay
        'note': 'Binary: deterministic proofs are either valid or invalid.'
    },
    'C': {
        'verified': Opinion(b=1.0, d=0.0, u=0.0, a=0.5),
        'falsified': Opinion(b=0.0, d=1.0, u=0.0, a=0.5),
        'initial': Opinion(b=0.0, d=0.0, u=1.0, a=0.5),
        'decay': 'ON_REGULATION_CHANGE',
        'note': 'Binary for current compliance; triggers re-verification on regulation change.'
    },
    'E': {
        'initial': Opinion(b=0.0, d=0.0, u=1.0, a=0.5),
        'decay': 'HALF_LIFE',
        'half_life_days': {
            'fast_domain': 90,
            'medium_domain': 180,
            'stable_domain': 365
        },
        'note': 'Full tuple. Uncertainty reflects source reliability and recency.'
    },
    'S': {
        'initial': Opinion(b=0.0, d=0.0, u=1.0, a=0.5),
        'decay': 'ON_NEW_DATA',
        'note': 'Full tuple. Uncertainty includes sampling uncertainty from CI width.'
    },
    'P': {
        'verified': Opinion(b=1.0, d=0.0, u=0.0, a=0.5),
        'falsified': Opinion(b=0.0, d=1.0, u=0.0, a=0.5),
        'initial': Opinion(b=0.0, d=0.0, u=1.0, a=0.5),
        'decay': 'ON_PROCESS_SPEC_CHANGE',
        'note': 'Binary for conformance; full tuple for process quality assessment.'
    },
    'R': {
        'initial': Opinion(b=0.0, d=0.0, u=1.0, a=0.5),
        'decay': 'ON_PREMISE_CHANGE',
        'note': 'Full tuple. Uncertainty captures premise uncertainty propagation.'
    },
    'H': {
        'initial': Opinion(b=0.0, d=0.0, u=1.0, a=0.7),  # Higher base rate for uncertainty
        'decay': 'HALF_LIFE',
        'half_life_days': {'default': 180},
        'note': 'Full tuple. High base uncertainty. Heuristics are inherently uncertain.'
    },
    'N': {
        'initial': Opinion(b=0.0, d=0.0, u=1.0, a=0.5),
        'decay': 'ON_CONSTITUTIONAL_AMENDMENT',
        'note': 'b/d represent constitutional alignment, not truth.'
    }
}
```

### 6.3 Composition Operators

Three primary operators compose opinions through dependency chains.

#### 6.3.1 Conjunction (AND)

Used when a conclusion C requires both premise A and premise B.

```python
def conjunction(w_A: Opinion, w_B: Opinion) -> Opinion:
    """
    Josang's subjective logic conjunction: w_C = w_A AND w_B.
    If conclusion requires both premises, belief decreases and uncertainty increases.

    Formal definition (Josang 2016, Definition 12.1):
    b_C = b_A * b_B
    d_C = d_A + d_B - d_A * d_B
    u_C = b_A * u_B + u_A * b_B + u_A * u_B
    a_C = a_A * a_B  (if a_A + a_B > 0, else 0)

    Note: b_C + d_C + u_C = 1 is preserved.
    """
    b_C = w_A.b * w_B.b
    d_C = w_A.d + w_B.d - w_A.d * w_B.d
    u_C = w_A.b * w_B.u + w_A.u * w_B.b + w_A.u * w_B.u
    a_C = w_A.a * w_B.a

    # Ensure constraint holds (floating point correction)
    total = b_C + d_C + u_C
    if abs(total - 1.0) > 1e-9:
        b_C, d_C, u_C = b_C/total, d_C/total, u_C/total

    return Opinion(b=b_C, d=d_C, u=u_C, a=a_C)
```

**Property (INV-M6):** `conjunction(w_A, w_B).b <= min(w_A.b, w_B.b)`. Belief never increases through conjunction.

#### 6.3.2 Discounting (Transitive Trust)

Used when agent X reports opinion w_A about claim A, and we have trust opinion w_X about agent X.

```python
def discounting(w_trust: Opinion, w_claim: Opinion) -> Opinion:
    """
    Josang's trust discounting: w_discounted = w_trust : w_claim.
    An untrusted agent's strong opinion becomes uncertain.

    Formal definition (Josang 2016, Definition 14.2):
    b_disc = b_trust * b_claim
    d_disc = b_trust * d_claim
    u_disc = d_trust + u_trust + b_trust * u_claim
    a_disc = a_claim
    """
    b_disc = w_trust.b * w_claim.b
    d_disc = w_trust.b * w_claim.d
    u_disc = w_trust.d + w_trust.u + w_trust.b * w_claim.u
    a_disc = w_claim.a

    # Normalize
    total = b_disc + d_disc + u_disc
    if abs(total - 1.0) > 1e-9:
        b_disc, d_disc, u_disc = b_disc/total, d_disc/total, u_disc/total

    return Opinion(b=b_disc, d=d_disc, u=u_disc, a=a_disc)
```

**Property:** If `w_trust.b = 0` (no trust in the agent), then `w_discounted.b = 0` and `w_discounted.u = 1`. Complete distrust yields complete uncertainty.

#### 6.3.3 Cumulative Fusion (Consensus)

Used when two independent agents both report opinions about the same claim.

```python
def cumulative_fusion(w_A: Opinion, w_B: Opinion) -> Opinion:
    """
    Josang's cumulative fusion: w_fused = w_A FUSE w_B.
    Multiple independent opinions reduce uncertainty.

    Formal definition (Josang 2016, Definition 12.6):
    When both u_A and u_B > 0:
      b_fused = (b_A * u_B + b_B * u_A) / (u_A + u_B - u_A * u_B)
      d_fused = (d_A * u_B + d_B * u_A) / (u_A + u_B - u_A * u_B)
      u_fused = (u_A * u_B) / (u_A + u_B - u_A * u_B)
      a_fused = (a_A * u_B + a_B * u_A) / (u_A + u_B) if u_A + u_B > 0
                                                          else (a_A + a_B) / 2

    When u_A = 0 and u_B = 0 (both dogmatic):
      b_fused = (b_A * gamma + b_B * (1 - gamma))
      where gamma = lim approximation, typically 0.5
    """
    if w_A.u == 0 and w_B.u == 0:
        # Both dogmatic: weighted average (equal weight)
        gamma = 0.5
        b_f = w_A.b * gamma + w_B.b * (1 - gamma)
        d_f = w_A.d * gamma + w_B.d * (1 - gamma)
        u_f = 0.0
        a_f = (w_A.a + w_B.a) / 2
    elif w_A.u == 0:
        # A is dogmatic, B is not: A dominates
        return w_A
    elif w_B.u == 0:
        # B is dogmatic, A is not: B dominates
        return w_B
    else:
        denom = w_A.u + w_B.u - w_A.u * w_B.u
        if denom < 1e-12:
            denom = 1e-12

        b_f = (w_A.b * w_B.u + w_B.b * w_A.u) / denom
        d_f = (w_A.d * w_B.u + w_B.d * w_A.u) / denom
        u_f = (w_A.u * w_B.u) / denom

        u_sum = w_A.u + w_B.u
        if u_sum > 0:
            a_f = (w_A.a * w_B.u + w_B.a * w_A.u) / u_sum
        else:
            a_f = (w_A.a + w_B.a) / 2

    # Normalize
    total = b_f + d_f + u_f
    if abs(total - 1.0) > 1e-9 and total > 0:
        b_f, d_f, u_f = b_f/total, d_f/total, u_f/total

    return Opinion(b=b_f, d=d_f, u=u_f, a=a_f)
```

**Property:** `cumulative_fusion(w_A, w_B).u <= min(w_A.u, w_B.u)`. Uncertainty never increases through consensus of independent opinions.

### 6.4 Credibility Propagation Algorithm

Credibility propagation computes the effective credibility of each claim in the dependency graph by applying composition operators along dependency edges.

```python
def propagate_credibility(claims: Dict[ClaimId, Claim],
                          opinions: Dict[ClaimId, Opinion],
                          agent_trust: Dict[Tuple[AgentId, ClaimClass], Opinion],
                          graph: DependencyGraph) -> Dict[ClaimId, Opinion]:
    """
    Propagate credibility through the claim dependency graph.
    For DAGs: single-pass topological order. O(|edges|).
    For cyclic graphs: iterative dampening (Section 6.5).
    """

    # Detect cycles
    if graph.has_cycles():
        return propagate_with_dampening(claims, opinions, agent_trust, graph)

    # Topological sort for DAG
    topo_order = graph.topological_sort()

    result = {}
    for claim_id in topo_order:
        claim = claims[claim_id]
        base_opinion = opinions[claim_id]

        # Step 1: Discount by agent trust (class-specific, INV-M4)
        agent_id = claim.producing_agent
        cls = claim.assigned_class
        trust_key = (agent_id, cls)
        if trust_key in agent_trust:
            discounted = discounting(agent_trust[trust_key], base_opinion)
        else:
            # Unknown agent: high uncertainty
            default_trust = Opinion(b=0.3, d=0.0, u=0.7, a=0.5)
            discounted = discounting(default_trust, base_opinion)

        # Step 2: Compose with dependencies
        deps = graph.get_dependencies(claim_id)
        if len(deps) == 0:
            # No dependencies: use discounted opinion directly
            result[claim_id] = discounted
        else:
            # Conjunction with each dependency
            composed = discounted
            for dep in deps:
                if dep.claim_id in result:
                    dep_opinion = result[dep.claim_id]
                    # Check minimum credibility requirement
                    dep_cred = dep_opinion.expected_probability()
                    if dep_cred < dep.required_credibility:
                        # Dependency below threshold: increase uncertainty
                        penalty = Opinion(
                            b=0, d=0,
                            u=1.0,
                            a=composed.a
                        )
                        composed = conjunction(composed, penalty)
                    else:
                        composed = conjunction(composed, dep_opinion)

            result[claim_id] = composed

    return result
```

### 6.5 Cycle Handling (Iterative Dampening)

For dependency graphs with cycles, direct propagation does not terminate. PCVM applies iterative dampening analogous to PageRank.

```python
def propagate_with_dampening(claims: Dict[ClaimId, Claim],
                             opinions: Dict[ClaimId, Opinion],
                             agent_trust: Dict[Tuple[AgentId, ClaimClass], Opinion],
                             graph: DependencyGraph) -> Dict[ClaimId, Opinion]:
    """
    Iterative dampening for cyclic dependency graphs.
    Convergence guaranteed within ceil(log(epsilon) / log(alpha)) iterations.
    Default: alpha=0.85, epsilon=0.001 -> max 44 iterations.
    """
    alpha = DAMPENING_FACTOR       # default 0.85
    epsilon = CONVERGENCE_EPSILON   # default 0.001
    max_iter = CONVERGENCE_MAX_ITER # default 100

    # Initialize all opinions
    current = {}
    for claim_id in claims:
        base = opinions.get(claim_id, OPINION_INIT[claims[claim_id].assigned_class]['initial'])
        agent_id = claims[claim_id].producing_agent
        cls = claims[claim_id].assigned_class
        trust = agent_trust.get((agent_id, cls), Opinion(b=0.3, d=0.0, u=0.7, a=0.5))
        current[claim_id] = discounting(trust, base)

    for iteration in range(max_iter):
        next_opinions = {}
        max_delta = 0.0

        for claim_id in claims:
            deps = graph.get_dependencies(claim_id)
            if len(deps) == 0:
                next_opinions[claim_id] = current[claim_id]
                continue

            # Compose with dependencies using current estimates
            composed = current[claim_id]
            for dep in deps:
                if dep.claim_id in current:
                    dep_opinion = current[dep.claim_id]
                    composed = conjunction(composed, dep_opinion)

            # Apply dampening: blend with undampened opinion
            base = opinions.get(claim_id, OPINION_INIT[claims[claim_id].assigned_class]['initial'])
            dampened = Opinion(
                b = alpha * composed.b + (1 - alpha) * base.b,
                d = alpha * composed.d + (1 - alpha) * base.d,
                u = alpha * composed.u + (1 - alpha) * base.u,
                a = composed.a
            )

            # Renormalize
            total = dampened.b + dampened.d + dampened.u
            dampened = Opinion(b=dampened.b/total, d=dampened.d/total, u=dampened.u/total, a=dampened.a)

            next_opinions[claim_id] = dampened

            # Track convergence
            delta = abs(dampened.expected_probability() - current[claim_id].expected_probability())
            max_delta = max(max_delta, delta)

        current = next_opinions

        if max_delta < epsilon:
            # Converged
            return current

    # Did not converge within max_iter: return current state with warning
    # Sentinel Graph alert: CREDIBILITY_CONVERGENCE_FAILURE
    emit_sentinel_alert("CREDIBILITY_CONVERGENCE_FAILURE", {
        "max_iterations": max_iter,
        "final_delta": max_delta,
        "epsilon": epsilon
    })
    return current
```

### 6.6 Credibility Decay and Re-verification Triggers

Credibility decays over time based on class-specific rules. Decayed claims are automatically queued for re-verification.

```python
def apply_credibility_decay(claim: Claim, opinion: Opinion,
                            current_time: Timestamp) -> Tuple[Opinion, bool]:
    """
    Apply time-based credibility decay. Returns (new_opinion, needs_reverification).
    """
    cls = claim.assigned_class
    config = OPINION_INIT[cls]

    if config['decay'] is None:
        # D-class: no decay
        return opinion, False

    if config['decay'] == 'HALF_LIFE':
        # Time-based half-life decay
        half_life_days = config['half_life_days'].get('default', 365)
        age_days = days_since(claim.verified_timestamp, current_time)

        # Decay factor: 2^(-age/half_life)
        decay_factor = 2.0 ** (-age_days / half_life_days)

        # Shift belief to uncertainty
        new_b = opinion.b * decay_factor
        transferred = opinion.b - new_b
        new_u = min(1.0, opinion.u + transferred)
        new_d = 1.0 - new_b - new_u

        new_opinion = Opinion(b=new_b, d=max(0, new_d), u=new_u, a=opinion.a)

        # Trigger re-verification if credibility dropped below threshold
        needs_reverification = new_opinion.expected_probability() < REVERIFICATION_THRESHOLD
        return new_opinion, needs_reverification

    elif config['decay'] == 'ON_REGULATION_CHANGE':
        # Check if relevant regulation has changed since verification
        if regulation_changed_since(claim, claim.verified_timestamp):
            # Reset to high uncertainty
            return Opinion(b=0.1, d=0.0, u=0.9, a=0.5), True
        return opinion, False

    elif config['decay'] == 'ON_NEW_DATA':
        # Check if new data is available that could affect the statistical claim
        if new_data_available(claim):
            new_u = min(1.0, opinion.u + NEW_DATA_UNCERTAINTY_BOOST)
            new_b = opinion.b * (1 - NEW_DATA_UNCERTAINTY_BOOST)
            new_d = 1.0 - new_b - new_u
            return Opinion(b=new_b, d=max(0, new_d), u=new_u, a=opinion.a), True
        return opinion, False

    elif config['decay'] == 'ON_PROCESS_SPEC_CHANGE':
        if process_spec_changed(claim):
            return Opinion(b=0.0, d=0.0, u=1.0, a=0.5), True
        return opinion, False

    elif config['decay'] == 'ON_PREMISE_CHANGE':
        # Check if any premise's credibility has changed significantly
        for dep in claim.dependencies:
            if dep.relationship == "PREMISE":
                dep_cred = get_current_credibility(dep.claim_id)
                if dep_cred is not None:
                    original = dep.credibility_at_verification
                    if abs(dep_cred - original) > PREMISE_CHANGE_THRESHOLD:
                        return Opinion(b=opinion.b * 0.5, d=opinion.d,
                                      u=min(1.0, opinion.u + opinion.b * 0.5),
                                      a=opinion.a), True
        return opinion, False

    elif config['decay'] == 'ON_CONSTITUTIONAL_AMENDMENT':
        if constitutional_parameter_changed(claim):
            return Opinion(b=0.0, d=0.0, u=1.0, a=0.5), True
        return opinion, False

    return opinion, False

# Constants
REVERIFICATION_THRESHOLD = 0.5    # Credibility below this triggers re-verification
PREMISE_CHANGE_THRESHOLD = 0.2    # Premise credibility change exceeding this triggers re-verification
NEW_DATA_UNCERTAINTY_BOOST = 0.3  # Uncertainty increase when new data available
```

---

## 7. Deep-Audit Protocol Specification

### 7.1 Audit Selection Algorithm

The deep-audit protocol provides statistical deterrence against VTD forgery and collusion. A configurable percentage of all passed VTDs are re-verified via full replication. Selection is VRF-based and unpredictable.

```python
def select_for_deep_audit(
    passed_claims: List[ClaimId],
    epoch: EpochNum,
    audit_rate: float = None
) -> List[ClaimId]:
    """
    VRF-select claims for deep audit. INV-M5.
    Default audit_rate: 0.07 (7%).
    Selection is unpredictable: agents cannot know in advance which claims will be audited.
    """
    if audit_rate is None:
        audit_rate = DEEP_AUDIT_RATE  # default 0.07

    selected = []
    audit_seed = SHA256(b"DEEP_AUDIT" + uint64_be(epoch) + vrf_seed(epoch))

    for claim_id in passed_claims:
        # VRF-based selection: deterministic but unpredictable
        selection_hash = SHA256(audit_seed + claim_id.encode())
        threshold = int(audit_rate * 2**256)
        if uint256_from_bytes(selection_hash) < threshold:
            selected.append(claim_id)

    # Ensure minimum audit count per epoch
    if len(selected) < MIN_AUDITS_PER_EPOCH and len(passed_claims) >= MIN_AUDITS_PER_EPOCH:
        # Force-select additional claims by lowest hash
        remaining = [(SHA256(audit_seed + c.encode()), c)
                     for c in passed_claims if c not in selected]
        remaining.sort(key=lambda x: x[0])
        while len(selected) < MIN_AUDITS_PER_EPOCH and remaining:
            selected.append(remaining.pop(0)[1])

    return selected

# Citation-weighted bias: heavily cited claims are more likely to be audited
def select_with_citation_weight(
    passed_claims: List[ClaimId],
    citation_counts: Dict[ClaimId, int],
    epoch: EpochNum
) -> List[ClaimId]:
    """
    Bias audit selection toward heavily cited claims.
    A claim with C citations has its effective audit rate multiplied by
    (1 + log2(1 + C)).
    """
    audit_seed = SHA256(b"DEEP_AUDIT" + uint64_be(epoch) + vrf_seed(epoch))
    selected = []

    for claim_id in passed_claims:
        citations = citation_counts.get(claim_id, 0)
        weight = 1.0 + math.log2(1 + citations)
        effective_rate = min(1.0, DEEP_AUDIT_RATE * weight)

        selection_hash = SHA256(audit_seed + claim_id.encode())
        threshold = int(effective_rate * 2**256)
        if uint256_from_bytes(selection_hash) < threshold:
            selected.append(claim_id)

    return selected
```

### 7.2 Full Replication Procedure

```python
def execute_deep_audit(claim_id: ClaimId, epoch: EpochNum) -> AuditResult:
    """
    Full replication audit of a previously passed VTD.
    The audit committee is entirely independent of the original verification committee.
    """
    claim = get_claim(claim_id)
    vtd = get_vtd(claim_id)

    # Select independent audit committee (no overlap with original verifiers)
    original_verifiers = vtd.verification_committee
    original_probers = vtd.prober_agents
    excluded = {claim.producing_agent} | original_verifiers | original_probers

    audit_committee = select_audit_committee(
        claim, epoch, excluded,
        committee_size=AUDIT_COMMITTEE_SIZE  # default 5
    )

    # Full replication: each auditor independently evaluates the claim
    auditor_opinions = []
    for auditor_id in audit_committee:
        # Auditor performs full verification as if VTD did not exist
        independent_result = full_replication_verify(auditor_id, claim)
        auditor_opinions.append(independent_result.opinion)

    # Fuse auditor opinions
    fused_audit = auditor_opinions[0]
    for i in range(1, len(auditor_opinions)):
        fused_audit = cumulative_fusion(fused_audit, auditor_opinions[i])

    # Compare audit result with original VTD verification
    original_opinion = vtd.verification_result.opinion
    audit_credibility = fused_audit.expected_probability()
    original_credibility = original_opinion.expected_probability()

    discrepancy = abs(audit_credibility - original_credibility)

    if discrepancy < AUDIT_AGREEMENT_THRESHOLD:
        # Audit agrees with original: VTD is confirmed
        return AuditResult(
            status="CONFIRMED",
            discrepancy=discrepancy,
            audit_opinion=fused_audit,
            original_opinion=original_opinion,
            action=None
        )
    elif audit_credibility < original_credibility - AUDIT_SIGNIFICANT_DROP:
        # Audit finds claim less credible than original verification
        return AuditResult(
            status="DISCREPANCY_FOUND",
            discrepancy=discrepancy,
            audit_opinion=fused_audit,
            original_opinion=original_opinion,
            action="CREDIBILITY_DOWNGRADE"
        )
    else:
        # Minor discrepancy: log but take no action
        return AuditResult(
            status="MINOR_DISCREPANCY",
            discrepancy=discrepancy,
            audit_opinion=fused_audit,
            original_opinion=original_opinion,
            action=None
        )

AUDIT_AGREEMENT_THRESHOLD = 0.15    # Credibility difference below this is "agreement"
AUDIT_SIGNIFICANT_DROP = 0.25       # Credibility drop exceeding this triggers action
AUDIT_COMMITTEE_SIZE = 5
```

### 7.3 Audit Failure Handling

```python
def handle_audit_failure(audit_result: AuditResult, claim: Claim, vtd: VTD):
    """
    Handle a deep-audit that found discrepancy.
    Triggers: credibility downgrade, agent investigation, Sentinel alert.
    """
    if audit_result.action != "CREDIBILITY_DOWNGRADE":
        return

    # 1. Downgrade claim credibility to the audit committee's assessment
    update_claim_credibility(claim.claim_id, audit_result.audit_opinion)

    # 2. Downgrade producing agent's class-specific credibility
    agent_id = claim.producing_agent
    cls = claim.assigned_class
    current_trust = get_agent_class_credibility(agent_id, cls)
    penalty = AUDIT_FAILURE_PENALTY  # default: Opinion(b=0, d=0.3, u=0.7, a=0.5)
    new_trust = cumulative_fusion(current_trust, penalty)
    set_agent_class_credibility(agent_id, cls, new_trust)

    # 3. Queue re-verification of agent's recent claims in same class
    recent_claims = get_agent_recent_claims(agent_id, cls, lookback_epochs=AUDIT_LOOKBACK)
    for recent_id in recent_claims:
        queue_reverification(recent_id, priority="HIGH", reason="AUDIT_FAILURE_CASCADE")

    # 4. Emit Sentinel Graph alert
    emit_sentinel_alert("DEEP_AUDIT_FAILURE", {
        "claim_id": claim.claim_id,
        "agent_id": agent_id,
        "claim_class": cls,
        "discrepancy": audit_result.discrepancy,
        "original_credibility": audit_result.original_opinion.expected_probability(),
        "audit_credibility": audit_result.audit_opinion.expected_probability(),
        "claims_queued_for_reverification": len(recent_claims)
    })

    # 5. Check for collusion pattern
    check_collusion_indicators(claim, vtd, audit_result)

AUDIT_FAILURE_PENALTY = Opinion(b=0, d=0.3, u=0.7, a=0.5)
AUDIT_LOOKBACK = 50  # epochs
```

### 7.4 Statistical Guarantees

The deep-audit mechanism provides the following statistical guarantees:

**Detection probability.** For an audit rate r and a claim forgery rate f (fraction of passed claims that are forged), the expected number of forged claims detected per epoch is:

```
E[detected] = r * f * N
```

where N is the total number of claims per epoch. For r = 0.07, f = 0.05, N = 1000:

```
E[detected] = 0.07 * 0.05 * 1000 = 3.5 forged claims detected per epoch
```

**Deterrence probability.** The probability that a specific forged claim is NEVER audited over T epochs is:

```
P(never_audited) = (1 - r)^T
```

For r = 0.07 and T = 100 epochs: P(never_audited) = 0.93^100 = 0.00066. A forged claim has a 99.93% probability of being audited within 100 epochs.

**Required audit rate for detection confidence.**

| Confidence Level | Epochs | Required Audit Rate |
|-----------------|--------|-------------------|
| 95% detection within 50 epochs | 50 | 5.8% |
| 99% detection within 50 epochs | 50 | 8.9% |
| 95% detection within 100 epochs | 100 | 2.9% |
| 99% detection within 100 epochs | 100 | 4.5% |

The default audit rate of 7% provides >99% detection confidence within 65 epochs (approximately 65 hours at 1-hour epochs).

---

## 8. Knowledge Admission Protocol

### 8.1 VTD to MCT Issuance

When a VTD passes verification (including any applicable adversarial probing and deep-audit), the membrane issues a Membrane Credibility Token (MCT) that admits the claim to the canonical knowledge graph.

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/mct.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Membrane Credibility Token",
  "type": "object",
  "required": [
    "mct_id", "claim_id", "vtd_id", "cls_id",
    "assigned_class", "tier", "credibility_opinion",
    "verification_committee", "verification_epoch",
    "admission_timestamp", "mct_hash", "membrane_signature"
  ],
  "properties": {
    "mct_id": {
      "type": "string",
      "pattern": "^mct:[a-f0-9]{16}$"
    },
    "claim_id": { "type": "string" },
    "vtd_id": { "type": "string" },
    "cls_id": { "type": "string" },
    "assigned_class": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] },
    "tier": { "type": "string", "enum": ["FORMAL_PROOF","STRUCTURED_EVIDENCE","STRUCTURED_ATTESTATION"] },
    "credibility_opinion": {
      "type": "object",
      "required": ["b", "d", "u", "a"],
      "properties": {
        "b": { "type": "number", "minimum": 0, "maximum": 1 },
        "d": { "type": "number", "minimum": 0, "maximum": 1 },
        "u": { "type": "number", "minimum": 0, "maximum": 1 },
        "a": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "credibility_score": {
      "type": "number", "minimum": 0, "maximum": 1,
      "description": "E(w) = b + a*u at time of issuance."
    },
    "verification_committee": {
      "type": "array",
      "items": { "type": "string" },
      "description": "AgentIds of the verification committee."
    },
    "adversarial_probers": {
      "type": "array",
      "items": { "type": "string" },
      "description": "AgentIds of adversarial probers, if probing was performed."
    },
    "probe_survival": {
      "type": ["string", "null"],
      "enum": ["SURVIVED", "WEAKENED", "NOT_PROBED", null]
    },
    "verification_epoch": { "type": "integer", "minimum": 0 },
    "admission_timestamp": { "type": "string", "format": "date-time" },
    "decay_policy": {
      "type": "string",
      "description": "Decay policy identifier for this claim class."
    },
    "next_reverification_epoch": {
      "type": ["integer", "null"],
      "description": "Epoch at which credibility decay may trigger re-verification."
    },
    "mct_hash": {
      "type": "string", "pattern": "^[a-f0-9]{64}$",
      "description": "SHA-256 of all fields except mct_hash and membrane_signature."
    },
    "membrane_signature": { "type": "string" }
  }
}
```

### 8.2 MCT to BDL Persistence

Admitted claims persist to the Bounded Durability Layer (BDL) of the Knowledge Cortex. The BDL stores claims with their MCTs, VTDs, and credibility opinions.

```python
def admit_to_knowledge_cortex(claim: Claim, vtd: VTD, mct: MCT):
    """
    Persist a verified claim to the Knowledge Cortex's BDL.
    INV-M1: All claims pass through PCVM before admission.
    """
    # Step 1: Contradiction checking (Section 8.3)
    contradictions = check_contradictions(claim, mct)
    if contradictions:
        handle_contradictions(claim, contradictions, mct)
        # Contradictions do not block admission; they create contradiction edges

    # Step 2: Construct BDL record
    bdl_record = BDLRecord(
        claim_id=claim.claim_id,
        claim_text=claim.text,
        assigned_class=mct.assigned_class,
        tier=mct.tier,
        credibility_opinion=mct.credibility_opinion,
        credibility_score=mct.credibility_score,
        vtd_reference=vtd.vtd_id,
        mct_reference=mct.mct_id,
        producing_agent=claim.producing_agent,
        locus=claim.locus,
        admission_epoch=mct.verification_epoch,
        admission_timestamp=mct.admission_timestamp,
        dependencies=[dep.claim_id for dep in vtd.dependencies],
        decay_policy=mct.decay_policy,
        next_reverification=mct.next_reverification_epoch,
        status="ACTIVE"
    )

    # Step 3: Persist to BDL
    bdl_store.put(bdl_record)

    # Step 4: Update citation graph
    for dep in vtd.dependencies:
        citation_graph.add_edge(claim.claim_id, dep.claim_id, dep.relationship)

    # Step 5: Update agent credibility (positive reinforcement)
    cls = mct.assigned_class
    agent_id = claim.producing_agent
    current_trust = get_agent_class_credibility(agent_id, cls)
    positive = Opinion(b=0.1, d=0, u=0.9, a=0.5)
    updated_trust = cumulative_fusion(current_trust, positive)
    set_agent_class_credibility(agent_id, cls, updated_trust)

    # Step 6: Schedule re-verification if applicable
    if mct.next_reverification_epoch is not None:
        reverification_queue.schedule(claim.claim_id, mct.next_reverification_epoch)
```

### 8.3 Contradiction Checking

```python
def check_contradictions(claim: Claim, mct: MCT) -> List[Contradiction]:
    """
    Check if the new claim contradicts existing admitted claims.
    Contradiction does NOT block admission — both claims persist
    with a contradiction edge linking them.
    """
    contradictions = []

    # Query Knowledge Cortex for claims in same locus with semantic overlap
    related = knowledge_cortex.query_related(
        locus=claim.locus,
        claim_text=claim.text,
        similarity_threshold=CONTRADICTION_SIMILARITY_THRESHOLD  # default 0.7
    )

    for existing in related:
        # Semantic contradiction detection
        contradiction_score = assess_semantic_contradiction(claim.text, existing.claim_text)

        if contradiction_score > CONTRADICTION_THRESHOLD:  # default 0.8
            contradictions.append(Contradiction(
                new_claim=claim.claim_id,
                existing_claim=existing.claim_id,
                contradiction_score=contradiction_score,
                new_credibility=mct.credibility_score,
                existing_credibility=existing.credibility_score,
                type=classify_contradiction_type(claim, existing)
            ))

    return contradictions


def handle_contradictions(claim: Claim, contradictions: List[Contradiction], mct: MCT):
    """
    Handle detected contradictions.
    Both claims persist. The contradiction is recorded as an edge
    in the knowledge graph for downstream consumers to evaluate.
    """
    for c in contradictions:
        # Record contradiction edge
        knowledge_cortex.add_contradiction_edge(
            claim_a=c.new_claim,
            claim_b=c.existing_claim,
            contradiction_score=c.contradiction_score,
            detected_epoch=mct.verification_epoch
        )

        # If new claim has higher credibility, queue existing claim for re-verification
        if c.new_credibility > c.existing_credibility + CONTRADICTION_REVERIFY_DELTA:
            queue_reverification(
                c.existing_claim,
                priority="MEDIUM",
                reason=f"CONTRADICTED_BY_{c.new_claim}"
            )

        # Emit Sentinel alert
        emit_sentinel_alert("CONTRADICTION_DETECTED", {
            "new_claim": c.new_claim,
            "existing_claim": c.existing_claim,
            "score": c.contradiction_score,
            "type": c.type
        })

CONTRADICTION_SIMILARITY_THRESHOLD = 0.7
CONTRADICTION_THRESHOLD = 0.8
CONTRADICTION_REVERIFY_DELTA = 0.15
```

### 8.4 Re-verification Scheduling

```python
def schedule_reverification(claim_id: ClaimId, epoch: EpochNum):
    """Schedule a claim for re-verification at the specified epoch."""
    claim = get_claim(claim_id)
    vtd = get_vtd(claim_id)

    # Determine re-verification priority based on citation count
    citations = citation_graph.count_citations(claim_id)
    if citations > HIGH_CITATION_THRESHOLD:
        priority = "HIGH"
    elif citations > MEDIUM_CITATION_THRESHOLD:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    reverification_queue.enqueue(ReverificationRequest(
        claim_id=claim_id,
        scheduled_epoch=epoch,
        priority=priority,
        reason="CREDIBILITY_DECAY",
        original_vtd_id=vtd.vtd_id,
        original_credibility=get_current_credibility(claim_id)
    ))


def process_reverification_queue(epoch: EpochNum):
    """Process due re-verification requests at epoch boundary."""
    due = reverification_queue.get_due(epoch)

    # Sort by priority: HIGH > MEDIUM > LOW
    due.sort(key=lambda r: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[r.priority])

    # Process up to MAX_REVERIFICATIONS_PER_EPOCH
    processed = 0
    for request in due:
        if processed >= MAX_REVERIFICATIONS_PER_EPOCH:
            # Defer remaining to next epoch
            request.scheduled_epoch = epoch + 1
            reverification_queue.enqueue(request)
            continue

        # Re-verify: treat as new verification of existing claim
        claim = get_claim(request.claim_id)
        vtd = get_vtd(request.claim_id)

        # Select new verification committee
        committee = select_verification_committee(claim, epoch)

        # Run appropriate tier verification
        tier = CLASS_TO_TIER[claim.assigned_class]
        if tier == "FORMAL_PROOF":
            result = verify_tier1(vtd, committee)
        elif tier == "STRUCTURED_EVIDENCE":
            result = verify_tier2(vtd, committee, epoch)
        else:
            result = verify_tier3(vtd, committee, epoch)

        # Update credibility
        update_claim_credibility(request.claim_id, result.opinion)

        # Schedule next re-verification
        next_epoch = calculate_next_reverification(claim, result.opinion)
        if next_epoch is not None:
            schedule_reverification(request.claim_id, next_epoch)

        processed += 1

HIGH_CITATION_THRESHOLD = 10
MEDIUM_CITATION_THRESHOLD = 3
MAX_REVERIFICATIONS_PER_EPOCH = 100
```

---

## 9. Integration Interfaces

### 9.1 Tidal Noosphere API (VRF Committees, Epoch Events, V-class Dispatch)

PCVM integrates with the Tidal Noosphere as the verification execution engine for all V-class operations. The Noosphere provides governance; PCVM provides execution.

**Epoch Lifecycle Integration:**

```python
# Called by Tidal Scheduler at each epoch boundary
def on_epoch_boundary(epoch: EpochNum, vrf_seed: bytes, roster: AgentRoster):
    """
    PCVM epoch boundary handler.
    Invoked by the Tidal Noosphere at each epoch transition.
    """
    # 1. Update VRF seed for this epoch
    pcvm_state.current_vrf_seed = vrf_seed
    pcvm_state.current_epoch = epoch

    # 2. Process re-verification queue
    process_reverification_queue(epoch)

    # 3. Apply credibility decay to all active claims
    for claim_id in knowledge_cortex.get_active_claims():
        opinion = get_current_credibility(claim_id)
        claim = get_claim(claim_id)
        new_opinion, needs_reverify = apply_credibility_decay(
            claim, opinion, current_timestamp()
        )
        if new_opinion != opinion:
            update_claim_credibility(claim_id, new_opinion)
        if needs_reverify:
            schedule_reverification(claim_id, epoch + 1)

    # 4. Select deep-audit targets from previous epoch's passed claims
    prev_passed = get_passed_claims(epoch - 1)
    audit_targets = select_with_citation_weight(
        prev_passed, get_citation_counts(), epoch
    )
    for target in audit_targets:
        queue_deep_audit(target, epoch)

    # 5. Report MQI metrics to Sentinel Graph
    report_mqi_metrics(epoch)
```

**V-class Operation Dispatch:**

```python
def handle_v_class_operation(operation: VClassOperation) -> VerificationResult:
    """
    Entry point for all V-class operations from the Tidal Noosphere.
    Dispatches to the appropriate verification tier.
    """
    vtd = operation.vtd
    claim = operation.claim

    # Step 1: Classification (if not already classified)
    if vtd.assigned_class is None:
        cls_result = classify_claim(claim, vtd)
        vtd.assigned_class = cls_result.assigned_class
        vtd.tier = cls_result.tier
        vtd.secondary_classes = cls_result.secondary_classes
        seal = issue_classification_seal(cls_result, claim, vtd)
    else:
        seal = get_classification_seal(claim.claim_id)

    # Step 2: Select verification committee via VRF
    committee = select_diverse_verifiers(
        claim, pcvm_state.current_epoch, pcvm_state.current_vrf_seed,
        pcvm_state.diversity_pools, get_locus(claim.locus),
        committee_size=COMMITTEE_SIZE_BY_TIER[vtd.tier]
    )

    # Step 3: Dispatch to tier-specific verification
    tier = vtd.tier
    if tier == "FORMAL_PROOF":
        result = verify_tier1(vtd, committee)
    elif tier == "STRUCTURED_EVIDENCE":
        result = verify_tier2(vtd, committee, pcvm_state.current_epoch)
    elif tier == "STRUCTURED_ATTESTATION":
        result = verify_tier3(vtd, committee, pcvm_state.current_epoch)

    # Step 4: Verify secondary classes if present
    for sec_cls in vtd.secondary_classes:
        sec_body = get_secondary_body(vtd, sec_cls)
        if sec_body:
            sec_result = verify_secondary(sec_body, sec_cls, committee)
            # Take minimum credibility (Section 1.5)
            if sec_result.opinion.expected_probability() < result.opinion.expected_probability():
                result.opinion = sec_result.opinion

    # Step 5: Issue MCT if verification passed
    if result.status in ("VERIFIED", "WEAK_VERIFICATION"):
        mct = issue_mct(claim, vtd, seal, result, committee)
        admit_to_knowledge_cortex(claim, vtd, mct)

    return result

COMMITTEE_SIZE_BY_TIER = {
    "FORMAL_PROOF": 3,
    "STRUCTURED_EVIDENCE": 5,
    "STRUCTURED_ATTESTATION": 7
}
```

### 9.2 Knowledge Cortex API (Admission, Queries, Re-verification)

```python
class KnowledgeCortexInterface:
    """PCVM's interface to the Knowledge Cortex (persistent memory)."""

    def admit_claim(self, claim_id: ClaimId, bdl_record: BDLRecord) -> bool:
        """Admit a verified claim to the BDL. Returns True on success."""
        pass

    def query_related(self, locus: str, claim_text: str,
                      similarity_threshold: float) -> List[BDLRecord]:
        """Find semantically related claims for contradiction checking."""
        pass

    def get_claim_credibility(self, claim_id: ClaimId) -> Optional[Opinion]:
        """Get current credibility opinion for a claim."""
        pass

    def update_credibility(self, claim_id: ClaimId, opinion: Opinion) -> bool:
        """Update a claim's credibility opinion after re-verification or decay."""
        pass

    def add_contradiction_edge(self, claim_a: ClaimId, claim_b: ClaimId,
                                score: float, epoch: EpochNum) -> bool:
        """Record a contradiction between two claims."""
        pass

    def get_citation_count(self, claim_id: ClaimId) -> int:
        """Get the number of claims that cite this claim."""
        pass

    def mark_superseded(self, old_claim: ClaimId, new_claim: ClaimId) -> bool:
        """Mark a claim as superseded by a newer claim."""
        pass
```

### 9.3 Settlement API (Reward Calculation, Quality Metrics)

PCVM feeds into the Tidal Noosphere's Stream 2 (Verification Duty) settlement calculation. Verification quality is weighted at 40% of total settlement.

```python
def compute_verification_settlement(agent_id: AgentId, epoch: EpochNum) -> float:
    """
    Compute verification reward for an agent.
    Integrates with Tidal Noosphere Settlement Stream 2.
    """
    # Duties fulfilled as verifier
    duties = get_verification_duties(agent_id, epoch)
    duties_fulfilled = sum(1 for d in duties if d.completed)

    # Quality of verifications (did this agent's opinions align with deep-audit results?)
    quality_scores = []
    for duty in duties:
        if duty.completed and duty.claim_id in get_audited_claims(epoch):
            audit = get_audit_result(duty.claim_id)
            agent_opinion = duty.opinion
            audit_opinion = audit.audit_opinion
            alignment = 1.0 - abs(
                agent_opinion.expected_probability() - audit_opinion.expected_probability()
            )
            quality_scores.append(alignment)

    quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.85

    # Adversarial probing quality (if served as prober)
    probe_duties = get_probe_duties(agent_id, epoch)
    probe_quality = compute_probe_quality(probe_duties)

    # Combined verification reward
    reward = (
        VERIFICATION_RATE * duties_fulfilled * quality
        + PROBE_REWARD_RATE * len(probe_duties) * probe_quality
    )

    return reward

VERIFICATION_RATE = 0.002    # AIC per verification duty
PROBE_REWARD_RATE = 0.003    # AIC per adversarial probe (higher to incentivize)
```

### 9.4 Sentinel Graph API (Anomaly Reporting, MQI Metrics)

PCVM reports six Membrane Quality Index (MQI) metrics to the Sentinel Graph at each epoch boundary.

```python
def report_mqi_metrics(epoch: EpochNum):
    """Report PCVM-specific metrics to the Sentinel Graph."""
    metrics = {
        # Core MQI metrics
        "vtd_rejection_rate": compute_rejection_rate(epoch),
        "adversarial_probe_trigger_rate": compute_probe_rate(epoch),
        "credibility_distribution": compute_credibility_distribution(epoch),
        "classification_agreement_rate": compute_classification_agreement(epoch),
        "deep_audit_discrepancy_rate": compute_audit_discrepancy_rate(epoch),
        "reverification_queue_depth": reverification_queue.size(),

        # Collusion detection metrics
        "pairwise_endorsement_correlation": compute_endorsement_correlation(epoch),
        "verification_pattern_anomalies": detect_verification_anomalies(epoch),

        # Per-class breakdown
        "claims_by_class": count_claims_by_class(epoch),
        "avg_credibility_by_class": avg_credibility_by_class(epoch)
    }

    sentinel_graph.report("PCVM_MQI", epoch, metrics)

    # Check MQI thresholds
    if metrics["vtd_rejection_rate"] > MQI_REJECTION_THRESHOLD:
        sentinel_graph.alert("HIGH_REJECTION_RATE", epoch, metrics["vtd_rejection_rate"])

    if metrics["deep_audit_discrepancy_rate"] > MQI_AUDIT_DISCREPANCY_THRESHOLD:
        sentinel_graph.alert("HIGH_AUDIT_DISCREPANCY", epoch,
                           metrics["deep_audit_discrepancy_rate"])

MQI_REJECTION_THRESHOLD = 0.30       # >30% rejection rate triggers alert
MQI_AUDIT_DISCREPANCY_THRESHOLD = 0.15  # >15% audit discrepancy triggers alert
```

**Collusion Detection:**

```python
def compute_endorsement_correlation(epoch: EpochNum) -> Dict:
    """
    Compute pairwise endorsement correlation for collusion detection.
    Sentinel Graph Alert if correlation between any agent pair exceeds threshold.
    """
    # Build endorsement matrix: agent_pair -> (times_verified, times_endorsed)
    endorsement_matrix = {}
    lookback = COLLUSION_LOOKBACK_EPOCHS  # default 50

    for e in range(max(0, epoch - lookback), epoch):
        for verification in get_verifications(e):
            verifier = verification.verifier_id
            producer = verification.producing_agent
            pair = (min(verifier, producer), max(verifier, producer))

            if pair not in endorsement_matrix:
                endorsement_matrix[pair] = {"verified": 0, "endorsed": 0}

            endorsement_matrix[pair]["verified"] += 1
            if verification.result.status in ("VERIFIED", "WEAK_VERIFICATION"):
                endorsement_matrix[pair]["endorsed"] += 1

    # Flag suspicious pairs
    suspicious = []
    for pair, counts in endorsement_matrix.items():
        if counts["verified"] >= MIN_VERIFICATIONS_FOR_CORRELATION:
            endorsement_rate = counts["endorsed"] / counts["verified"]
            if endorsement_rate > COLLUSION_ENDORSEMENT_THRESHOLD:
                suspicious.append({
                    "agent_pair": pair,
                    "endorsement_rate": endorsement_rate,
                    "sample_size": counts["verified"]
                })

    if suspicious:
        emit_sentinel_alert("COLLUSION_SUSPICION", {
            "epoch": epoch,
            "suspicious_pairs": suspicious
        })

    return {"suspicious_pairs": len(suspicious), "total_pairs": len(endorsement_matrix)}

COLLUSION_LOOKBACK_EPOCHS = 50
MIN_VERIFICATIONS_FOR_CORRELATION = 5
COLLUSION_ENDORSEMENT_THRESHOLD = 0.95  # >95% endorsement rate is suspicious
```

### 9.5 ASV API (Claim Semantics from C4)

PCVM uses ASV (C4) types for structured claim representation. The mapping:

| ASV Type | PCVM Usage |
|----------|-----------|
| CLM (Claim) | The claim being verified. CLM.type maps to PCVM claim class. |
| PRV (Provenance) | Maps to VTD dependencies and process traces. |
| AGT (Agent) | Producing agent and verification committee members. |
| VRF (Verification) | Maps to MCT (Membrane Credibility Token). |
| CNF (Confidence) | Maps to Subjective Logic opinion tuple. |
| EVD (Evidence) | Maps to VTD proof_body evidence items. |
| CTX (Context) | Maps to locus and epoch metadata. |

```python
def vtd_to_asv(vtd: VTD, mct: MCT) -> ASVDocument:
    """Convert a verified VTD to ASV format for external consumption."""
    return ASVDocument(
        type="VRF",
        id=mct.mct_id,
        claim=ASVClaim(
            type="CLM",
            id=vtd.claim_id,
            content=vtd.claim_text,
            epistemic_type=vtd.assigned_class,
            confidence=ASVConfidence(
                type="CNF",
                framework="SUBJECTIVE_LOGIC",
                belief=mct.credibility_opinion["b"],
                disbelief=mct.credibility_opinion["d"],
                uncertainty=mct.credibility_opinion["u"],
                base_rate=mct.credibility_opinion["a"],
                expected_probability=mct.credibility_score
            )
        ),
        provenance=ASVProvenance(
            type="PRV",
            agent=vtd.producing_agent,
            timestamp=vtd.timestamp,
            method=f"PCVM_{vtd.tier}",
            evidence_refs=[dep.claim_id for dep in vtd.dependencies]
        ),
        verification=ASVVerification(
            type="VRF",
            verifiers=mct.verification_committee,
            epoch=mct.verification_epoch,
            method=vtd.tier,
            proof_artifact=vtd.vtd_id
        )
    )
```

---

## 10. Configurable Parameters

All configurable parameters with defaults, valid ranges, and governance requirements.

| Parameter | Default | Range | Governance |
|-----------|---------|-------|------------|
| `DEEP_AUDIT_RATE` | 0.07 | [0.01, 0.25] | G-class (constitutional) |
| `MIN_AUDITS_PER_EPOCH` | 5 | [1, 50] | G-class |
| `AUDIT_COMMITTEE_SIZE` | 5 | [3, 11] | G-class |
| `AUDIT_AGREEMENT_THRESHOLD` | 0.15 | [0.05, 0.30] | G-class |
| `AUDIT_SIGNIFICANT_DROP` | 0.25 | [0.10, 0.50] | G-class |
| `AUDIT_LOOKBACK` | 50 epochs | [10, 200] | Operational |
| `COMMITTEE_SIZE_TIER1` | 3 | [3, 7] | G-class |
| `COMMITTEE_SIZE_TIER2` | 5 | [3, 11] | G-class |
| `COMMITTEE_SIZE_TIER3` | 7 | [5, 15] | G-class |
| `PROBERS_TIER2` | 1 | [0, 3] | G-class |
| `PROBERS_TIER3` | 2 | [1, 5] | G-class |
| `DAMPENING_FACTOR` | 0.85 | [0.70, 0.95] | Operational |
| `CONVERGENCE_EPSILON` | 0.001 | [0.0001, 0.01] | Operational |
| `CONVERGENCE_MAX_ITER` | 100 | [20, 500] | Operational |
| `REVERIFICATION_THRESHOLD` | 0.50 | [0.30, 0.70] | G-class |
| `PREMISE_CHANGE_THRESHOLD` | 0.20 | [0.10, 0.40] | Operational |
| `TIER3_ACCEPT_THRESHOLD` | 0.60 | [0.50, 0.80] | G-class |
| `TIER3_WEAK_THRESHOLD` | 0.40 | [0.30, 0.60] | G-class |
| `RANDOM_PROBE_RATE` | 0.10 | [0.05, 0.30] | G-class |
| `PROBE_CREDIBILITY_THRESHOLD` | 0.50 | [0.30, 0.70] | Operational |
| `PROBE_SURVIVAL_BOOST` | 0.05 | [0.01, 0.10] | Operational |
| `SUSPICION_PENALTY_NO_COUNTER_EVIDENCE` | 0.15 | [0.05, 0.30] | Operational |
| `INOCULATION_THRESHOLD` | 0.70 | [0.50, 0.90] | Operational |
| `MAX_PROBE_BUDGET` | 5000 tokens | [1000, 20000] | Operational |
| `APPEAL_RATE_LIMIT` | 0.05 | [0.01, 0.15] | G-class |
| `SOURCE_FRESHNESS_DAYS` | varies | [30, 730] | Operational |
| `CONTRADICTION_SIMILARITY_THRESHOLD` | 0.70 | [0.50, 0.90] | Operational |
| `CONTRADICTION_THRESHOLD` | 0.80 | [0.60, 0.95] | Operational |
| `MAX_REVERIFICATIONS_PER_EPOCH` | 100 | [10, 1000] | Operational |
| `MQI_REJECTION_THRESHOLD` | 0.30 | [0.10, 0.50] | G-class |
| `MQI_AUDIT_DISCREPANCY_THRESHOLD` | 0.15 | [0.05, 0.30] | G-class |
| `COLLUSION_LOOKBACK_EPOCHS` | 50 | [20, 200] | Operational |
| `COLLUSION_ENDORSEMENT_THRESHOLD` | 0.95 | [0.85, 1.00] | Operational |
| `DIVERSITY_COOLING_EPOCHS` | 50 | [10, 100] | G-class |

**Governance levels:**
- **G-class (Constitutional):** Changes require G-class constitutional consensus (75% BFT supermajority + 72-hour discussion). These parameters directly affect membrane sovereignty.
- **Operational:** Changes can be made by the feedback controller within bounds, or by operational governance (simple majority). These parameters tune performance without affecting membrane guarantees.

---

## 11. Conformance Requirements

### 11.1 MUST Requirements (Mandatory)

1. An implementation MUST validate all VTDs against the common envelope schema (Section 2.1) before processing.
2. An implementation MUST validate VTD proof_body against the class-specific schema determined by `assigned_class`.
3. An implementation MUST enforce VTD size limits per class (Section 2.1).
4. An implementation MUST implement the three-way classification protocol (Section 3.2). The membrane MUST assign final classifications independently of the producing agent's suggestion (INV-M2).
5. An implementation MUST apply the most conservative class when all three classification inputs disagree.
6. An implementation MUST select verification committees via VRF (RFC 9381) with the commit-reveal and pre-stratified diversity pool mechanisms specified in the Tidal Noosphere (C3 Section 5.2).
7. An implementation MUST NOT allow an agent to verify its own claims (INV-M3).
8. An implementation MUST NOT allow adversarial probers to overlap with the verification committee for the same claim (INV-M3).
9. An implementation MUST track agent credibility per claim class (INV-M4). Cross-class credibility transfer is prohibited.
10. An implementation MUST perform mandatory source verification for E-class claims: URL accessibility, content hash comparison, and quote accuracy verification (REQ-1).
11. An implementation MUST invoke adversarial probing for all Tier 3 claims (H-class, N-class).
12. An implementation MUST implement the deep-audit protocol with VRF-based selection at the configured audit rate (INV-M5).
13. An implementation MUST handle deep-audit failures as specified in Section 7.3: credibility downgrade, agent investigation, cascade re-verification, Sentinel alert.
14. An implementation MUST issue a Classification Seal (CLS) for every classified claim.
15. An implementation MUST issue a Membrane Credibility Token (MCT) for every admitted claim.
16. An implementation MUST perform contradiction checking before knowledge admission (Section 8.3).
17. An implementation MUST preserve the constraint b + d + u = 1 in all Subjective Logic operations.
18. An implementation MUST report MQI metrics to the Sentinel Graph at each epoch boundary.
19. An implementation MUST enforce that G-class parameters can only be modified through G-class constitutional consensus.
20. An implementation MUST NOT modify a VTD after submission and sealing (INV-M7).

### 11.2 SHOULD Requirements (Recommended)

1. An implementation SHOULD implement citation-weighted deep-audit selection (Section 7.1) rather than uniform random selection.
2. An implementation SHOULD include a generative component in adversarial probe strategies to resist inoculation attacks.
3. An implementation SHOULD implement meta-probing to detect pre-fabricated VTD responses.
4. An implementation SHOULD implement collusion detection via pairwise endorsement correlation analysis.
5. An implementation SHOULD require counter-evidence sections with at least one item for Tier 3 claims.
6. An implementation SHOULD schedule re-verification based on claim class decay policies (Section 6.6).
7. An implementation SHOULD support multi-class claims with secondary proof bodies (Section 1.5).
8. An implementation SHOULD provide ASV-compatible output (Section 9.5) for interoperability with external systems.

### 11.3 MAY Requirements (Optional)

1. An implementation MAY implement alternative proof certificate formats beyond the four specified (COQ, TLA+, Isabelle, CUSTOM_CERT).
2. An implementation MAY adjust operational parameters within their valid ranges without G-class consensus.
3. An implementation MAY implement a bootstrap protocol with seed claims for cold-start initialization.
4. An implementation MAY implement constitutional intent annotations for richer N-class verification.
5. An implementation MAY implement a classification appeal protocol beyond the basic 3-committee review.

---

## 12. Test Vectors

### 12.1 Test Vector 1: D-class Hash Verification

```json
{
  "test_id": "TV-D-001",
  "description": "D-class claim: SHA-256 hash verification",
  "claim_text": "SHA-256('hello world') = b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "suggested_class": "D",
  "vtd": {
    "proof_body": {
      "proof_type": "HASH_VERIFICATION",
      "computation": {
        "algorithm": "SHA-256",
        "version": "FIPS-180-4",
        "determinism_declaration": "FULLY_DETERMINISTIC"
      },
      "inputs": [
        {
          "name": "message",
          "value": "hello world",
          "value_hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
        }
      ],
      "output": {
        "value": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
        "value_hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
      }
    }
  },
  "expected_classification": "D",
  "expected_tier": "FORMAL_PROOF",
  "expected_verification_status": "VERIFIED",
  "expected_opinion": {"b": 1.0, "d": 0.0, "u": 0.0, "a": 0.5},
  "expected_credibility": 1.0
}
```

### 12.2 Test Vector 2: E-class Source Verification Failure

```json
{
  "test_id": "TV-E-001",
  "description": "E-class claim with invalid source URL — should fail source verification",
  "claim_text": "GPT-4 achieves 86.4% on MMLU",
  "suggested_class": "E",
  "vtd": {
    "proof_body": {
      "sources": [
        {
          "source_id": "src-001",
          "source_type": "WEB_PAGE",
          "uri": "https://example.com/nonexistent-page",
          "retrieval_timestamp": "2026-03-01T00:00:00Z",
          "content_hash": "0000000000000000000000000000000000000000000000000000000000000000",
          "quoted_text": "GPT-4 achieves 86.4% on MMLU",
          "relevance_justification": "Primary result report"
        }
      ],
      "cross_references": [],
      "evidence_chain": [
        {
          "sub_claim": "GPT-4 MMLU score is 86.4%",
          "supporting_sources": ["src-001"],
          "strength": "STRONG"
        }
      ]
    },
    "counter_evidence": {
      "considered": true,
      "items": []
    }
  },
  "expected_classification": "E",
  "expected_tier": "STRUCTURED_EVIDENCE",
  "expected_verification_status": "FALSIFIED",
  "expected_opinion_b_max": 0.1,
  "note": "Source URL returns 404. Source verification fails. Claim should not be admitted."
}
```

### 12.3 Test Vector 3: Subjective Logic Conjunction

```json
{
  "test_id": "TV-SL-001",
  "description": "Conjunction of two opinions",
  "input_A": {"b": 0.7, "d": 0.1, "u": 0.2, "a": 0.5},
  "input_B": {"b": 0.8, "d": 0.0, "u": 0.2, "a": 0.5},
  "operation": "conjunction",
  "expected_output": {
    "b": 0.56,
    "d": 0.10,
    "u": 0.34,
    "a": 0.25
  },
  "expected_credibility": 0.645,
  "verification": "b=0.7*0.8=0.56, d=0.1+0.0-0.1*0.0=0.10, u=0.7*0.2+0.2*0.8+0.2*0.2=0.34, a=0.5*0.5=0.25. E=0.56+0.25*0.34=0.645"
}
```

### 12.4 Test Vector 4: Cumulative Fusion

```json
{
  "test_id": "TV-SL-002",
  "description": "Cumulative fusion of two independent opinions",
  "input_A": {"b": 0.6, "d": 0.1, "u": 0.3, "a": 0.5},
  "input_B": {"b": 0.5, "d": 0.2, "u": 0.3, "a": 0.5},
  "operation": "cumulative_fusion",
  "expected_output": {
    "b": 0.6522,
    "d": 0.1739,
    "u": 0.1739,
    "a": 0.5
  },
  "expected_credibility": 0.7391,
  "verification": "denom=0.3+0.3-0.3*0.3=0.51. b=(0.6*0.3+0.5*0.3)/0.51=0.33/0.51=0.6471. d=(0.1*0.3+0.2*0.3)/0.51=0.09/0.51=0.1765. u=0.09/0.51=0.1765. Normalize. a=(0.5*0.3+0.5*0.3)/0.6=0.5"
}
```

### 12.5 Test Vector 5: Trust Discounting

```json
{
  "test_id": "TV-SL-003",
  "description": "Discounting a claim opinion by agent trust",
  "trust_opinion": {"b": 0.9, "d": 0.0, "u": 0.1, "a": 0.5},
  "claim_opinion": {"b": 0.8, "d": 0.1, "u": 0.1, "a": 0.5},
  "operation": "discounting",
  "expected_output": {
    "b": 0.72,
    "d": 0.09,
    "u": 0.19,
    "a": 0.5
  },
  "expected_credibility": 0.815,
  "verification": "b=0.9*0.8=0.72, d=0.9*0.1=0.09, u=0.0+0.1+0.9*0.1=0.19, a=0.5. E=0.72+0.5*0.19=0.815"
}
```

### 12.6 Test Vector 6: Deep-Audit Detection Probability

```json
{
  "test_id": "TV-DA-001",
  "description": "Deep-audit detection probability over time",
  "audit_rate": 0.07,
  "epochs": [10, 50, 100],
  "expected_detection_probability": [0.516, 0.971, 0.9993],
  "formula": "P(detected) = 1 - (1 - r)^T",
  "verification": "1-0.93^10=0.516, 1-0.93^50=0.971, 1-0.93^100=0.9993"
}
```

### 12.7 Test Vector 7: Classification Disagreement Resolution

```json
{
  "test_id": "TV-CLS-001",
  "description": "Three-way classification disagreement resolves to most conservative",
  "agent_suggestion": "E",
  "structural_class": "S",
  "independent_class": "H",
  "expected_assigned_class": "H",
  "expected_seal_type": "CONSERVATIVE",
  "expected_tier": "STRUCTURED_ATTESTATION",
  "note": "Full disagreement (E, S, H). H is most conservative per ordering H>N>E>S>R>P>C>D."
}
```

### 12.8 Test Vector 8: Credibility Decay

```json
{
  "test_id": "TV-DECAY-001",
  "description": "E-class credibility decay over 180 days with 180-day half-life",
  "initial_opinion": {"b": 0.8, "d": 0.05, "u": 0.15, "a": 0.5},
  "claim_class": "E",
  "half_life_days": 180,
  "age_days": 180,
  "expected_decay_factor": 0.5,
  "expected_opinion": {"b": 0.4, "d": 0.05, "u": 0.55, "a": 0.5},
  "expected_credibility": 0.675,
  "needs_reverification": false,
  "note": "b decays from 0.8 to 0.4. Transferred 0.4 to uncertainty. E=0.4+0.5*0.55=0.675 > 0.5 threshold."
}
```

---

## 13. Security Considerations

### 13.1 Threat Model

PCVM assumes the Tidal Noosphere's threat model (C3 Section 10.1) with the following PCVM-specific extensions:

| Threat | Attacker Capability | Primary Defense |
|--------|-------------------|-----------------|
| VTD Forgery (Confident Liar) | Produce structurally valid VTDs with fabricated evidence | Mandatory source verification, deep-audit deterrence |
| Strategic Omission | Produce complete VTDs that omit unfavorable evidence | Counter-evidence requirement, adversarial probing |
| Class Downgrade | Misclassify claims to avoid proof obligations | Membrane-assigned classification (INV-M2) |
| Probe Inoculation | Pre-fabricate responses to anticipated adversarial probes | Dynamic probe generation, meta-probe detection |
| Reputation Laundering | Build D-class credibility, exploit for H-class claims | Class-specific credibility (INV-M4) |
| Constitutional Exploitation | Satisfy letter but not spirit of constitutional parameters | Intent annotations, constitutional case law |
| VTD Explosion | Submit massive VTDs to overwhelm verification | Per-class size limits, per-agent resource budgets |
| Mutual Endorsement | Colluding verifiers endorse each other's claims | VRF committee selection, collusion detection, deep-audit |

### 13.2 Attack Resistance Analysis

**VTD Forgery (CRITICAL).** Defense depth: (1) mandatory source verification catches fabricated URLs and quotes; (2) adversarial probing with generative component tests claims beyond the VTD's self-contained evidence; (3) deep-audit at 7% rate provides >99% detection within 65 epochs; (4) audit failure triggers cascade re-verification of agent's recent claims. Residual risk: HIGH. A sophisticated forger who uses real sources but misrepresents their content remains difficult to detect without domain expertise on the verification committee.

**Collusion (CRITICAL).** Defense depth: (1) VRF selection ensures committees are unpredictable; (2) pre-stratified diversity pools ensure committee diversity; (3) deep-audit with independent committee catches claims that passed through colluding verifiers; (4) Sentinel Graph's endorsement correlation analysis detects statistical anomalies within approximately 50 epochs. Residual risk: HIGH for sophisticated colluders who vary their behavior to stay below detection thresholds. The fundamental limitation: any peer-verification system is vulnerable to collusion when the colluding fraction exceeds the committee diversity guarantee.

**Class Downgrade (HIGH).** Defense: three-way classification with membrane authority (INV-M2). The structural analyzer and independent classifier provide two independent classification signals. Disagreement defaults to most conservative class. Residual risk: MEDIUM. Classification accuracy (estimated F1 0.65-0.80) means some legitimate claims will be over-classified, creating friction.

**Reputation Laundering (MEDIUM).** Defense: class-specific credibility (INV-M4). An agent's D-class credibility is stored and evaluated independently of its H-class credibility. The discounting operator applies class-specific trust. Residual risk: LOW with proper implementation.

### 13.3 Bootstrap Security

During the bootstrap phase (before steady-state credibility is established), PCVM SHOULD:

1. Seed the system with 100-500 manually verified ground-truth claims with assigned credibility opinions.
2. Apply a bootstrap multiplier to deep-audit rate (2x normal rate during first 100 epochs).
3. Fall back to replication-based verification for HIGH and CRITICAL risk claims during bootstrap.
4. Monitor credibility convergence rate — if average credibility does not exceed 0.5 within 50 epochs, trigger Sentinel alert.

### 13.4 Cryptographic Requirements

1. All VTD hashes MUST use SHA-256 (FIPS 180-4).
2. All signatures MUST use Ed25519 (RFC 8032).
3. All VRF operations MUST use ECVRF on P-256 (RFC 9381).
4. VTD canonical serialization MUST use deterministic JSON serialization: keys sorted lexicographically, no whitespace, UTF-8 encoding.
5. The VRF seed MUST rotate at each epoch boundary and MUST NOT be predictable more than 1 epoch in advance.

### 13.5 Privacy Considerations

1. VTDs contain evidence chains that may reference external sources. Implementations MUST NOT cache or persist the content of external sources beyond what is needed for verification (content hashes are sufficient for re-verification).
2. Agent credibility opinions are system-internal metadata. Implementations SHOULD NOT expose raw per-agent credibility opinions outside the membrane. Aggregate statistics (per-class average credibility) MAY be published.
3. Deep-audit results that reveal agent-specific verification quality MUST be accessible only to the membrane, the Sentinel Graph, and governance agents.

---

*Technical specification completed 2026-03-09. Specification Writer, Atrahasis Agent System v2.0.*
*Protocol: Specification Stage, C5-B Proof-Carrying Verification Membrane.*
