# Epistemic Metabolism Architecture (EMA) — Technical Specification

## C6 SPECIFICATION Document

**Version:** 1.0.0
**Date:** 2026-03-10
**Status:** SPECIFICATION
**Invention ID:** C6
**Concept:** C6-A+B — Epistemic Metabolism Architecture
**Predecessor:** Knowledge Cortex (deprecated, underspecified)
**Dependencies:** C3 (Tidal Noosphere), C4 (ASV/AASL), C5 (PCVM)
**Assessment Council Verdict:** CONDITIONAL_ADVANCE (Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10)
**Normative References:** RFC 2119, JSON Schema Draft 2020-12, Josang Subjective Logic (2016), W3C PROV-DM (2013), Dung Bipolar Argumentation (1995), RFC 3339, UUID v7 (RFC 9562)

---

## Abstract

The Epistemic Metabolism Architecture (EMA) is the knowledge lifecycle engine for the Atrahasis stack. It replaces the underspecified Knowledge Cortex with a formally defined metabolic system in which knowledge units — epistemic quanta — are ingested, circulated through a coherence graph, consolidated via LLM-driven dreaming with PCVM verification gating, and catabolized when they lose credibility or relevance. A five-signal regulatory system (SHREC) governs metabolic rates through ecological budget competition with PID safety overlay. Bounded-loss projection functions allow C3 (Tidal Noosphere), C4 (ASV), and C5 (PCVM) to view canonical quanta in subsystem-native formats with measurable fidelity guarantees.

EMA sits between PCVM (verification) and the Settlement Plane (economy) in the Atrahasis stack. It is the canonical store of all verified knowledge in the system. No subsystem stores knowledge independently; all subsystem-local knowledge is a projection of the canonical quantum held by EMA.

This specification is implementation-ready. An engineer with access to this document, the Tidal Noosphere specification (C3), the ASV vocabulary (C4), and the PCVM specification (C5) can build EMA without additional design decisions.

---

## Table of Contents

- [1. Formal Definitions and Notation](#1-formal-definitions-and-notation)
- [2. Epistemic Quantum Schema](#2-epistemic-quantum-schema)
- [3. Ingestion Protocol](#3-ingestion-protocol)
- [4. Circulation Protocol](#4-circulation-protocol)
- [5. Consolidation Protocol](#5-consolidation-protocol)
- [6. Catabolism Protocol](#6-catabolism-protocol)
- [7. SHREC Specification](#7-shrec-specification)
- [8. Projection Engine Specification](#8-projection-engine-specification)
- [9. Retrieval Interface](#9-retrieval-interface)
- [10. Integration Interfaces](#10-integration-interfaces)
- [11. Configurable Parameters](#11-configurable-parameters)
- [12. Conformance Requirements](#12-conformance-requirements)
- [13. Test Vectors](#13-test-vectors)
- [14. Security Considerations](#14-security-considerations)

---

**Notation and Conventions.** The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119. Pseudocode uses Python-like syntax with explicit type annotations. All hash functions refer to SHA-256 unless otherwise specified. Epoch numbers are zero-indexed from GENESIS_TIME as defined in the Tidal Noosphere specification (C3). Agent identifiers are globally unique 256-bit values as defined in C5 (PCVM). All JSON schemas conform to JSON Schema Draft 2020-12. Timestamps are RFC 3339 strings in UTC. Opinion tuples are denoted with lowercase omega (w). Credibility scores are real values in [0, 1]. The symbol sigma denotes standard deviation of a rolling window unless otherwise qualified.

---

## 1. Formal Definitions and Notation

### 1.1 Primitive Types

| Symbol | Type | Definition |
|--------|------|------------|
| `AgentId` | `bytes[32]` | Globally unique agent identifier (256-bit), per C5 |
| `QuantumId` | `string` | URI-format identifier: `eq:<locus>:<epoch>:<uuid7_short>` |
| `LocusId` | `string` | Locus namespace selector, per C3 Definition 2.1 |
| `ParcelId` | `string` | Parcel identifier, per C3 Definition 2.2 |
| `EpochNum` | `uint64` | Zero-indexed epoch number |
| `ClaimClass` | `enum` | One of {D, E, S, H, N, P, R, C}, per C5 Section 1.2 |
| `Hash256` | `bytes[32]` | SHA-256 digest |
| `Opinion` | `tuple(f64, f64, f64, f64)` | Subjective Logic opinion (b, d, u, a) |
| `Timestamp` | `string` | RFC 3339 UTC timestamp |
| `EdgeType` | `enum` | One of {SUPPORT, CONTRADICTION, DERIVATION, ANALOGY, SUPERSESSION} |
| `MetabolicState` | `enum` | One of {ACTIVE, CONSOLIDATING, DECAYING, QUARANTINED, DISSOLVED} |
| `ShardId` | `string` | Coherence graph shard identifier, derived from LocusId |
| `DreamingSessionId` | `string` | Unique identifier for a consolidation session: `ds:<epoch>:<hash8>` |
| `SignalName` | `enum` | One of {HUNGER, CONSOLIDATION, STRESS, IMMUNE, NOVELTY} |
| `Regime` | `enum` | One of {NORMAL, ELEVATED, CRITICAL, CONSTITUTIONAL} |
| `ProjectionTarget` | `enum` | One of {C3, C4, C5} |
| `FidelityScore` | `f64` | Value in [0.0, 1.0] representing round-trip information preservation |

### 1.2 Subjective Logic Primitives

An opinion tuple w = (b, d, u, a) represents belief about a binary proposition where:
- b (belief): evidence in favor, b >= 0
- d (disbelief): evidence against, d >= 0
- u (uncertainty): lack of evidence, u >= 0
- a (base rate): prior probability absent evidence, a in [0, 1]
- **Constraint:** b + d + u = 1

The **expected probability** (credibility score):

```
E(w) = b + a * u
```

**Vacuous opinion** (total ignorance): `w_vacuous = (0, 0, 1, 0.5)`

**Dogmatic belief**: `w_true = (1, 0, 0, a)` for any a

**Dogmatic disbelief**: `w_false = (0, 1, 0, a)` for any a

**Conjunction operator** (combining dependent opinions):

```
w_AB = w_A AND w_B
b_AB = b_A * b_B
d_AB = b_A * d_B + d_A * b_B + d_A * d_B
u_AB = b_A * u_B + u_A * b_B + u_A * u_B + u_A * d_B + d_A * u_B  -- INCORRECT
```

Per Josang (2016), the conjunction for independent opinions:

```
b_AB = b_A * b_B + b_A * u_B * a_B + u_A * a_A * b_B
       -- (normalized, see Josang 2016 Def. 12.2)
```

Implementations MUST use the full Josang multinomial conjunction formula. The simplified forms above are for exposition only.

**Discounting operator** (trust-weighted opinion):

```
w_A:B = A discounts B
b_A:B = b_A * b_B
d_A:B = b_A * d_B
u_A:B = d_A + u_A + b_A * u_B
a_A:B = a_B
```

**Consensus operator** (fusing independent opinions from multiple sources):

```
w_fused = cumulative fusion of w_1, w_2, ..., w_n
```

Per Josang (2016) Def. 12.6, cumulative fusion for n sources. Implementations MUST use the full Josang cumulative fusion formula with dogmatic opinion handling.

### 1.3 Epistemic Edge Semantics

| Edge Type | Directionality | Weight Semantics | Formal Basis |
|-----------|---------------|------------------|--------------|
| SUPPORT | Directed: A supports B | Strength of evidential support [0, 1] | Dung bipolar argumentation (support relation) |
| CONTRADICTION | Mutual: A contradicts B | Severity of contradiction [0, 1] | Dung abstract argumentation (attack relation) |
| DERIVATION | Directed: B derived from A | Derivation confidence [0, 1] | W3C PROV wasDerivedFrom |
| ANALOGY | Bidirectional: A analogous to B | Structural similarity [0, 1] | Gentner (1983) structure-mapping theory |
| SUPERSESSION | Directed: B supersedes A | Replacement completeness [0, 1] | Temporal versioning with coverage measure |

Edge weight dynamics follow Hebbian reinforcement:
- **Strengthening:** When both endpoint quanta are accessed within the same epoch, edge weight increases by `reinforcement_rate * (1 - current_weight)`.
- **Decay:** Edges not reinforced within `edge_ttl` epochs decay by `decay_rate * current_weight` per epoch.
- **Minimum weight:** Edges below `min_edge_weight` are pruned.

### 1.4 Key Invariants

- **INV-E1 (Canonical Source):** The epistemic quantum stored in EMA is ALWAYS the canonical representation of a piece of knowledge. All subsystem-local copies are projections. When projections and canonical representations conflict, the canonical version governs unless the projected update carries PCVM verification (in which case the canonical is updated).

- **INV-E2 (PCVM Gate):** No quantum enters ACTIVE state without passing through PCVM verification. This extends INV-M1 (Membrane Sovereignty) from C5 to cover all knowledge lifecycle transitions, not just initial admission.

- **INV-E3 (Metabolic Ordering):** Within each epoch, metabolic phases execute in strict order: Ingestion, Circulation, Consolidation, Catabolism, Regulation. No phase begins until its predecessor completes for the current epoch.

- **INV-E4 (Consolidation Lock):** A quantum in CONSOLIDATING state MUST NOT transition to DECAYING, QUARANTINED, or DISSOLVED. Consolidation locks have bounded TTL to prevent deadlock.

- **INV-E5 (Dissolution Irreversibility):** Once a quantum enters DISSOLVED state, it MUST NOT return to any other state. Only the dissolution_record persists. Recovery requires creating a new quantum with provenance linking to the dissolution record.

- **INV-E6 (Edge Budget):** No quantum MAY have more than `MAX_EDGES_PER_QUANTUM` edges. No shard MAY have more than `MAX_EDGES_PER_SHARD` total edges. Edge creation beyond budget triggers pruning of lowest-weight edges.

- **INV-E7 (SHREC Floor):** SHREC budget allocation for each signal MUST NOT fall below the signal's configured floor allocation. Floor allocations are constitutional bounds that SHREC cannot violate.

- **INV-E8 (Projection Fidelity):** Each projection function MUST maintain round-trip fidelity above its configured target. If measured fidelity falls below target minus tolerance, the projection cache MUST be invalidated and the projection function re-evaluated.

- **INV-E9 (Provenance Completeness):** Every quantum MUST have a complete W3C PROV provenance record tracing its origin to either an external source or a generating agent action. Provenance chains MUST NOT have gaps.

- **INV-E10 (Single-Agent Contradiction Cap):** The total contradiction_factor contributed by any single agent to any single target quantum MUST NOT exceed `MAX_AGENT_CONTRADICTION_WEIGHT` (default 0.3). This prevents weaponized catabolism via contradiction flooding.

### 1.5 Epoch Processing Model

Each epoch is divided into five sequential metabolic phases:

```
EPOCH(t):
  Phase 1 — INGESTION    [t, t + 0.2)   New quanta validated, decomposed, inserted
  Phase 2 — CIRCULATION  [t + 0.2, t + 0.4)  Active quanta pushed to subscribers
  Phase 3 — CONSOLIDATION [t + 0.4, t + 0.6)  Dreaming engine runs if triggered
  Phase 4 — CATABOLISM   [t + 0.6, t + 0.8)  Dissolution criteria evaluated
  Phase 5 — REGULATION   [t + 0.8, t + 1.0)  SHREC computes signals, adjusts budget
```

Phase boundaries are logical, not wall-clock. Each phase completes when its processing queue is drained or its budget allocation is exhausted, whichever comes first. The fractional notation indicates ordering, not proportional time allocation.

---

## 2. Epistemic Quantum Schema

### 2.1 Complete JSON Schema

```json
{
  "$id": "https://ema.atrahasis.dev/schema/v1/epistemic-quantum.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Epistemic Quantum",
  "description": "The fundamental knowledge unit in the Epistemic Metabolism Architecture.",
  "type": "object",
  "required": [
    "id", "content", "opinion", "provenance", "edges",
    "metabolic_state", "projections", "timestamps",
    "dissolution_record", "claim_class"
  ],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^eq:[^:]+:[0-9]+:[a-f0-9]{12}$",
      "description": "Globally unique quantum identifier: eq:<locus>:<epoch>:<uuid7_short>"
    },
    "content": {
      "$ref": "#/$defs/QuantumContent"
    },
    "opinion": {
      "$ref": "#/$defs/SubjectiveLogicOpinion"
    },
    "provenance": {
      "$ref": "#/$defs/ProvenanceRecord"
    },
    "edges": {
      "type": "array",
      "items": { "$ref": "#/$defs/EpistemicEdge" },
      "maxItems": 50,
      "description": "Typed epistemic edges to other quanta. Max per INV-E6."
    },
    "metabolic_state": {
      "$ref": "#/$defs/MetabolicState"
    },
    "projections": {
      "$ref": "#/$defs/ProjectionCache"
    },
    "timestamps": {
      "$ref": "#/$defs/QuantumTimestamps"
    },
    "dissolution_record": {
      "oneOf": [
        { "type": "null" },
        { "$ref": "#/$defs/DissolutionRecord" }
      ],
      "default": null,
      "description": "Null until quantum is dissolved."
    },
    "claim_class": {
      "type": "string",
      "enum": ["D", "E", "S", "H", "N", "P", "R", "C"],
      "description": "PCVM claim class from C5 taxonomy."
    },
    "quantum_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$",
      "description": "SHA-256 of canonical JSON serialization of content + opinion + provenance."
    },
    "shard_id": {
      "type": "string",
      "description": "Coherence graph shard this quantum belongs to, derived from locus."
    },
    "citation_count": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "description": "Number of other quanta citing this quantum via DERIVATION or SUPPORT edges. Used for structural protection (self/non-self discrimination)."
    },
    "version": {
      "type": "integer",
      "minimum": 1,
      "default": 1,
      "description": "Monotonically increasing version number. Incremented on any opinion or edge update."
    }
  },
  "additionalProperties": false,
  "$defs": {
    "QuantumContent": {
      "type": "object",
      "required": ["claim_text", "claim_type", "domain_tags"],
      "properties": {
        "claim_text": {
          "type": "string",
          "minLength": 1,
          "maxLength": 4096,
          "description": "Natural language or structured claim content."
        },
        "claim_type": {
          "type": "string",
          "enum": ["observation", "inference", "prediction", "consolidation", "axiom", "governance"],
          "description": "Semantic type of the claim."
        },
        "domain_tags": {
          "type": "array",
          "items": { "type": "string", "maxLength": 128 },
          "minItems": 1,
          "maxItems": 10,
          "description": "Ontological domain tags for circulation routing."
        },
        "evidence": {
          "type": "array",
          "items": { "$ref": "#/$defs/EvidenceItem" },
          "default": [],
          "description": "Evidence basis for the claim."
        },
        "structured_content": {
          "type": "object",
          "description": "Optional machine-readable payload (key-value, formulae, measurements).",
          "additionalProperties": true
        }
      },
      "additionalProperties": false
    },
    "EvidenceItem": {
      "type": "object",
      "required": ["evidence_type", "weight"],
      "properties": {
        "source_quantum_id": {
          "type": ["string", "null"],
          "description": "ID of supporting quantum, null for external evidence."
        },
        "external_reference": {
          "type": ["string", "null"],
          "description": "URI of external evidence source."
        },
        "evidence_type": {
          "type": "string",
          "enum": ["empirical", "testimonial", "inferential", "synthetic"]
        },
        "weight": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "description": "Relative weight of this evidence item."
        }
      },
      "additionalProperties": false
    },
    "SubjectiveLogicOpinion": {
      "type": "object",
      "required": ["belief", "disbelief", "uncertainty", "base_rate"],
      "properties": {
        "belief": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Evidence-supported belief mass."
        },
        "disbelief": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Evidence-supported disbelief mass."
        },
        "uncertainty": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Uncommitted belief mass (ignorance)."
        },
        "base_rate": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Prior probability for expected probability computation."
        }
      },
      "additionalProperties": false,
      "description": "Constraint: belief + disbelief + uncertainty = 1.0. E(w) = belief + base_rate * uncertainty."
    },
    "ProvenanceRecord": {
      "type": "object",
      "required": ["generating_agent", "generating_activity", "generation_time"],
      "properties": {
        "generating_agent": {
          "type": "string",
          "description": "AgentId of the agent that produced this quantum."
        },
        "generating_activity": {
          "type": "string",
          "enum": ["ingestion", "inference", "consolidation", "governance", "external_import"],
          "description": "W3C PROV activity type."
        },
        "generation_time": {
          "type": "string", "format": "date-time",
          "description": "RFC 3339 UTC timestamp of quantum creation."
        },
        "generation_epoch": {
          "type": "integer", "minimum": 0,
          "description": "Epoch number at creation."
        },
        "derived_from": {
          "type": "array",
          "items": { "type": "string" },
          "default": [],
          "description": "QuantumIds this quantum was derived from (PROV wasDerivedFrom)."
        },
        "method": {
          "type": ["string", "null"],
          "description": "Description of the method used to generate this quantum."
        },
        "source_vtd_id": {
          "type": ["string", "null"],
          "description": "VTD ID from PCVM verification, if applicable."
        },
        "attribution_chain": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["agent_id", "role", "timestamp"],
            "properties": {
              "agent_id": { "type": "string" },
              "role": {
                "type": "string",
                "enum": ["creator", "reviewer", "consolidator", "verifier"]
              },
              "timestamp": { "type": "string", "format": "date-time" }
            },
            "additionalProperties": false
          },
          "default": [],
          "description": "Full attribution chain per W3C PROV."
        }
      },
      "additionalProperties": false
    },
    "EpistemicEdge": {
      "type": "object",
      "required": ["target_id", "edge_type", "weight", "created_at"],
      "properties": {
        "target_id": {
          "type": "string",
          "description": "QuantumId of the connected quantum."
        },
        "edge_type": {
          "type": "string",
          "enum": ["SUPPORT", "CONTRADICTION", "DERIVATION", "ANALOGY", "SUPERSESSION"]
        },
        "weight": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Edge strength. Decays with disuse, strengthens with co-activation."
        },
        "created_at": {
          "type": "string", "format": "date-time"
        },
        "last_activated": {
          "type": "string", "format": "date-time",
          "description": "Last epoch in which both endpoints were accessed (Hebbian activation)."
        },
        "creating_agent": {
          "type": "string",
          "description": "AgentId that created this edge."
        }
      },
      "additionalProperties": false
    },
    "MetabolicState": {
      "type": "object",
      "required": ["phase", "vitality"],
      "properties": {
        "phase": {
          "type": "string",
          "enum": ["ACTIVE", "CONSOLIDATING", "DECAYING", "QUARANTINED", "DISSOLVED"]
        },
        "vitality": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Composite health score. See Section 2.4 for computation."
        },
        "circulation_count": {
          "type": "integer", "minimum": 0, "default": 0,
          "description": "Number of times delivered to consumers."
        },
        "consolidation_lock": {
          "oneOf": [
            { "type": "null" },
            { "$ref": "#/$defs/ConsolidationLock" }
          ],
          "default": null
        },
        "decay_rate_override": {
          "type": ["number", "null"],
          "description": "If set, overrides default decay rate for this quantum."
        }
      },
      "additionalProperties": false
    },
    "ConsolidationLock": {
      "type": "object",
      "required": ["dreaming_session_id", "locked_at", "lock_ttl_epochs"],
      "properties": {
        "dreaming_session_id": {
          "type": "string",
          "description": "DreamingSessionId that holds the lock."
        },
        "locked_at": {
          "type": "string", "format": "date-time"
        },
        "lock_ttl_epochs": {
          "type": "integer", "minimum": 1, "maximum": 20, "default": 5,
          "description": "Lock expires after this many epochs."
        },
        "lock_epoch": {
          "type": "integer", "minimum": 0,
          "description": "Epoch at which lock was acquired."
        }
      },
      "additionalProperties": false
    },
    "ProjectionCache": {
      "type": "object",
      "properties": {
        "c3": {
          "oneOf": [
            { "type": "null" },
            { "$ref": "#/$defs/CachedProjection" }
          ],
          "default": null
        },
        "c4": {
          "oneOf": [
            { "type": "null" },
            { "$ref": "#/$defs/CachedProjection" }
          ],
          "default": null
        },
        "c5": {
          "oneOf": [
            { "type": "null" },
            { "$ref": "#/$defs/CachedProjection" }
          ],
          "default": null
        }
      },
      "additionalProperties": false
    },
    "CachedProjection": {
      "type": "object",
      "required": ["projected_at", "fidelity_score", "payload"],
      "properties": {
        "projected_at": {
          "type": "string", "format": "date-time"
        },
        "projection_epoch": {
          "type": "integer", "minimum": 0
        },
        "fidelity_score": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Measured round-trip fidelity at projection time."
        },
        "payload": {
          "type": "object",
          "description": "Subsystem-native representation.",
          "additionalProperties": true
        },
        "stale": {
          "type": "boolean", "default": false,
          "description": "Set true when canonical quantum is updated after projection."
        }
      },
      "additionalProperties": false
    },
    "QuantumTimestamps": {
      "type": "object",
      "required": ["created_at"],
      "properties": {
        "created_at": {
          "type": "string", "format": "date-time"
        },
        "last_circulated": {
          "type": ["string", "null"], "format": "date-time", "default": null
        },
        "last_verified": {
          "type": ["string", "null"], "format": "date-time", "default": null
        },
        "decay_start": {
          "type": ["string", "null"], "format": "date-time", "default": null,
          "description": "Timestamp when quantum entered DECAYING state."
        },
        "last_accessed": {
          "type": ["string", "null"], "format": "date-time", "default": null
        }
      },
      "additionalProperties": false
    },
    "DissolutionRecord": {
      "type": "object",
      "required": ["reason", "dissolved_at_epoch", "recycled_to", "eliminated_evidence"],
      "properties": {
        "reason": {
          "type": "string",
          "enum": ["low_credibility", "temporal_expiry", "superseded", "quarantine_timeout", "manual"],
          "description": "Why the quantum was dissolved."
        },
        "dissolved_at_epoch": {
          "type": "integer", "minimum": 0
        },
        "dissolved_at": {
          "type": "string", "format": "date-time"
        },
        "recycled_to": {
          "type": "array",
          "items": { "type": "string" },
          "description": "QuantumIds that received redistributed evidence components."
        },
        "eliminated_evidence": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "evidence_hash": { "type": "string" },
              "reason": { "type": "string" }
            }
          },
          "description": "Evidence components that were eliminated (not recyclable)."
        },
        "content_hash": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$",
          "description": "SHA-256 of original content for audit trail."
        },
        "final_opinion": {
          "$ref": "#/$defs/SubjectiveLogicOpinion",
          "description": "Opinion at time of dissolution."
        },
        "quarantine_snapshot_hash": {
          "type": ["string", "null"],
          "description": "Hash of full serialized quantum at quarantine entry. Full snapshot retained for QUARANTINE_SNAPSHOT_RETENTION_EPOCHS."
        }
      },
      "additionalProperties": false
    }
  }
}
```

### 2.2 Lifecycle State Machine

The metabolic state of an epistemic quantum follows this state machine:

```
                    ┌─────────────────────────────────┐
                    │                                 │
                    v                                 │ (consolidation completes
              ┌──────────┐                            │  or lock TTL expires)
   Ingestion  │          │  consolidation lock        │
   ─────────> │  ACTIVE  │ ──────────────────> ┌──────────────┐
              │          │                     │ CONSOLIDATING │
              └──────────┘ <────────────────── └──────────────┘
                    │
                    │ vitality < decay_threshold
                    │ OR temporal_expiry
                    v
              ┌──────────┐
              │ DECAYING  │
              └──────────┘
                    │
                    │ vitality < quarantine_threshold
                    │ OR decay_timeout
                    v
              ┌──────────────┐    rescue by dreaming
              │ QUARANTINED  │ ──────────────────────> ACTIVE
              └──────────────┘
                    │
                    │ quarantine_timeout
                    │ OR manual dissolution
                    v
              ┌──────────┐
              │ DISSOLVED │  (terminal state)
              └──────────┘
```

**Transition Rules:**

| From | To | Trigger | Guard |
|------|----|---------|-------|
| (external) | ACTIVE | Ingestion + PCVM verification pass | claim_class assigned, opinion computed |
| ACTIVE | CONSOLIDATING | Consolidation lock acquired | dreaming session active, lock TTL set |
| CONSOLIDATING | ACTIVE | Consolidation completes or lock TTL expires | lock released |
| ACTIVE | DECAYING | vitality < `DECAY_THRESHOLD` OR temporal validity expired | NOT in CONSOLIDATING state |
| DECAYING | QUARANTINED | vitality < `QUARANTINE_THRESHOLD` OR decay duration > `MAX_DECAY_EPOCHS` | NOT in CONSOLIDATING state |
| DECAYING | ACTIVE | vitality recovers above `DECAY_THRESHOLD` (e.g., new supporting evidence) | support edge weight increase |
| QUARANTINED | ACTIVE | Dreaming rescue OR manual rescue OR new strong supporting evidence | citation_count > 0 or explicit rescue |
| QUARANTINED | DISSOLVED | quarantine duration > `MAX_QUARANTINE_EPOCHS` OR manual dissolution | recycling procedure completed |
| DISSOLVED | (none) | Terminal state | INV-E5 |

**State transition pseudocode:**

```python
def evaluate_state_transition(q: EpistemicQuantum, epoch: EpochNum) -> MetabolicState:
    """Evaluate and apply metabolic state transitions for quantum q at epoch."""

    current = q.metabolic_state.phase

    if current == "DISSOLVED":
        return "DISSOLVED"  # Terminal, INV-E5

    if current == "CONSOLIDATING":
        lock = q.metabolic_state.consolidation_lock
        if lock is None:
            return "ACTIVE"  # Lock released, return to active
        if epoch - lock.lock_epoch >= lock.lock_ttl_epochs:
            release_consolidation_lock(q)
            return "ACTIVE"  # TTL expired
        return "CONSOLIDATING"  # Lock still held

    vitality = compute_vitality(q, epoch)
    q.metabolic_state.vitality = vitality

    if current == "ACTIVE":
        if vitality < DECAY_THRESHOLD:
            q.timestamps.decay_start = current_timestamp()
            return "DECAYING"
        return "ACTIVE"

    if current == "DECAYING":
        if vitality >= DECAY_THRESHOLD:
            q.timestamps.decay_start = None
            return "ACTIVE"  # Recovery
        decay_epochs = epoch - epoch_of(q.timestamps.decay_start)
        if vitality < QUARANTINE_THRESHOLD or decay_epochs > MAX_DECAY_EPOCHS:
            create_quarantine_snapshot(q)
            return "QUARANTINED"
        return "DECAYING"

    if current == "QUARANTINED":
        quarantine_epochs = epoch - epoch_of(q.timestamps.decay_start)  # reuse decay_start
        if quarantine_epochs > MAX_QUARANTINE_EPOCHS:
            execute_dissolution(q, reason="quarantine_timeout")
            return "DISSOLVED"
        return "QUARANTINED"
```

### 2.3 Edge Type Definitions

#### 2.3.1 SUPPORT Edge

A directed edge from quantum A to quantum B indicating that A provides evidential support for B.

**Creation conditions:**
- Agent explicitly declares support relationship
- Ingestion discovers semantic similarity with positive polarity
- Consolidation identifies supporting relationship

**Weight update rule:**
```python
def update_support_weight(edge: EpistemicEdge, epoch: EpochNum) -> float:
    """Update support edge weight via Hebbian reinforcement and decay."""
    epochs_since_activation = epoch - epoch_of(edge.last_activated)

    if epochs_since_activation == 0:
        # Co-activation this epoch: strengthen
        new_weight = edge.weight + REINFORCEMENT_RATE * (1.0 - edge.weight)
    else:
        # Decay proportional to time since activation
        decay_factor = EDGE_DECAY_RATE * epochs_since_activation
        new_weight = edge.weight * max(0.0, 1.0 - decay_factor)

    return clamp(new_weight, MIN_EDGE_WEIGHT, 1.0)
```

**Effect on vitality:** Each SUPPORT edge contributes `edge.weight * SUPPORT_VITALITY_FACTOR` to the target quantum's vitality.

#### 2.3.2 CONTRADICTION Edge

A mutual edge between quantum A and quantum B indicating that A and B are in epistemic conflict.

**Creation conditions:**
- Agent explicitly declares contradiction
- PCVM adversarial probing identifies inconsistency
- Ingestion discovers semantic similarity with negative polarity

**Mutual enforcement:** When a CONTRADICTION edge is created from A to B, a reciprocal edge from B to A MUST also be created with the same weight. Both edges share the same lifecycle.

**Per-agent cap:** Per INV-E10, the total contradiction weight from any single agent to any target quantum MUST NOT exceed `MAX_AGENT_CONTRADICTION_WEIGHT`.

```python
def validate_contradiction_creation(
    source: EpistemicQuantum,
    target: EpistemicQuantum,
    creating_agent: AgentId,
    proposed_weight: float
) -> bool:
    """Check whether a new contradiction edge would violate per-agent cap."""
    existing_contradiction_weight = sum(
        e.weight for e in target.edges
        if e.edge_type == "CONTRADICTION"
        and e.creating_agent == creating_agent
    )
    return (existing_contradiction_weight + proposed_weight) <= MAX_AGENT_CONTRADICTION_WEIGHT
```

**Effect on vitality:** Each CONTRADICTION edge reduces the target quantum's vitality by `edge.weight * CONTRADICTION_VITALITY_FACTOR`.

#### 2.3.3 DERIVATION Edge

A directed edge from quantum A to quantum B indicating that B was derived from A (B wasDerivedFrom A in W3C PROV).

**Creation conditions:**
- Agent creates a new quantum citing existing quantum as source
- Consolidation produces a new quantum from source quanta
- Inference chain produces a conclusion from premises

**Immutability:** DERIVATION edges MUST NOT be deleted or have their weight reduced below their initial value. They represent provenance relationships that are historically factual.

**Effect on citation_count:** The source quantum's citation_count increments by 1 for each DERIVATION edge pointing to it. Quanta with `citation_count > STRUCTURAL_PROTECTION_THRESHOLD` are immune to catabolism (structural knowledge protection).

#### 2.3.4 ANALOGY Edge

A bidirectional edge between quantum A and quantum B indicating structural similarity across domains.

**Creation conditions:**
- Dreaming process discovers cross-domain structural mapping
- Agent explicitly declares analogy

**Weight semantics:** Weight represents structural similarity per Gentner's structure-mapping theory — higher weight indicates more relational (not just attributional) similarity.

**Consolidation trigger:** Clusters of quanta connected by ANALOGY edges with weight > `ANALOGY_CONSOLIDATION_THRESHOLD` are candidates for dreaming consolidation.

#### 2.3.5 SUPERSESSION Edge

A directed edge from quantum A to quantum B indicating that B replaces A. B is the newer, superseding quantum.

**Creation conditions:**
- Agent explicitly declares supersession with VTD
- Consolidation produces a generalization that subsumes existing quanta
- PCVM verification produces updated credibility that invalidates prior version

**Effect on source:** When quantum A is superseded by B, A's vitality decays at `SUPERSESSION_DECAY_MULTIPLIER` times the normal rate. If B has higher credibility than A, A transitions to DECAYING.

**Transitivity:** If A is superseded by B, and B is superseded by C, then A is transitively superseded by C. The system SHOULD maintain transitive supersession chains but MUST NOT create direct SUPERSESSION edges for transitive relationships (to avoid edge budget inflation).

### 2.4 Metabolic State — Vitality Computation

Vitality is a composite health score that determines metabolic state transitions.

```python
def compute_vitality(q: EpistemicQuantum, epoch: EpochNum) -> float:
    """Compute composite vitality score for quantum q at epoch."""

    # 1. Base decay: exponential decay from creation
    age_epochs = epoch - q.provenance.generation_epoch
    base_decay = math.exp(-BASE_DECAY_RATE * age_epochs)

    # 2. Access recency: boost for recent access
    if q.timestamps.last_accessed is not None:
        epochs_since_access = epoch - epoch_of(q.timestamps.last_accessed)
        access_recency = math.exp(-ACCESS_DECAY_RATE * epochs_since_access)
    else:
        access_recency = 0.5  # Never accessed: neutral

    # 3. Support factor: boosted by support edges
    support_weights = [
        e.weight for e in q.edges if e.edge_type == "SUPPORT"
    ]
    support_factor = min(1.0, 0.5 + sum(support_weights) * SUPPORT_VITALITY_FACTOR)

    # 4. Contradiction factor: reduced by contradiction edges (with per-agent cap applied)
    contradiction_weights = [
        e.weight for e in q.edges if e.edge_type == "CONTRADICTION"
    ]
    contradiction_factor = min(
        MAX_TOTAL_CONTRADICTION_FACTOR,
        sum(contradiction_weights) * CONTRADICTION_VITALITY_FACTOR
    )

    # 5. Credibility factor: opinion-based
    credibility = q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty
    credibility_factor = credibility

    # 6. Supersession penalty
    superseded_by = [
        e for e in q.edges if e.edge_type == "SUPERSESSION" and e.target_id != q.id
    ]
    if superseded_by:
        supersession_penalty = max(e.weight for e in superseded_by) * SUPERSESSION_DECAY_MULTIPLIER
    else:
        supersession_penalty = 0.0

    # Composite
    vitality = (
        base_decay
        * access_recency
        * support_factor
        * (1.0 - contradiction_factor)
        * credibility_factor
        * (1.0 - supersession_penalty)
    )

    return clamp(vitality, 0.0, 1.0)
```

---

## 3. Ingestion Protocol

### 3.1 MCT/BDL to Quantum Mapping

When a claim passes through PCVM verification (C5), it enters EMA via the ingestion protocol. The mapping from PCVM's Verification Trace Document (VTD) to an epistemic quantum is as follows:

```python
def map_vtd_to_quantum(vtd: VTD, pcvm_result: PCVMResult) -> EpistemicQuantum:
    """Map a verified VTD from PCVM to an epistemic quantum."""

    quantum = EpistemicQuantum()

    # 1. Identity
    quantum.id = generate_quantum_id(
        locus=vtd.locus,
        epoch=vtd.epoch
    )

    # 2. Content
    quantum.content = QuantumContent(
        claim_text=vtd.claim_text,
        claim_type=map_claim_class_to_type(vtd.assigned_class),
        domain_tags=extract_domain_tags(vtd.locus, vtd.claim_text),
        evidence=[
            map_vtd_evidence(dep) for dep in vtd.dependencies
        ],
        structured_content=extract_structured_content(vtd.proof_body)
    )

    # 3. Opinion — from PCVM credibility assessment
    quantum.opinion = SubjectiveLogicOpinion(
        belief=pcvm_result.opinion.belief,
        disbelief=pcvm_result.opinion.disbelief,
        uncertainty=pcvm_result.opinion.uncertainty,
        base_rate=pcvm_result.opinion.base_rate
    )

    # 4. Provenance
    quantum.provenance = ProvenanceRecord(
        generating_agent=vtd.producing_agent,
        generating_activity="ingestion",
        generation_time=vtd.timestamp,
        generation_epoch=vtd.epoch,
        derived_from=[dep.claim_id for dep in vtd.dependencies],
        method=f"PCVM-verified {vtd.assigned_class}-class claim",
        source_vtd_id=vtd.vtd_id,
        attribution_chain=[
            AttributionEntry(
                agent_id=vtd.producing_agent,
                role="creator",
                timestamp=vtd.timestamp
            )
        ]
    )

    # 5. Initial edges — from VTD dependencies
    quantum.edges = []
    for dep in vtd.dependencies:
        if dep.relationship in ("PREMISE", "EVIDENCE"):
            quantum.edges.append(EpistemicEdge(
                target_id=resolve_claim_to_quantum(dep.claim_id),
                edge_type="DERIVATION",
                weight=dep.required_credibility,
                created_at=vtd.timestamp,
                last_activated=vtd.timestamp,
                creating_agent=vtd.producing_agent
            ))

    # 6. Metabolic state
    quantum.metabolic_state = MetabolicState(
        phase="ACTIVE",
        vitality=1.0,
        circulation_count=0,
        consolidation_lock=None
    )

    # 7. Claim class
    quantum.claim_class = vtd.assigned_class

    # 8. Timestamps
    quantum.timestamps = QuantumTimestamps(
        created_at=vtd.timestamp,
        last_circulated=None,
        last_verified=vtd.timestamp,
        decay_start=None,
        last_accessed=None
    )

    # 9. Projections and dissolution — initialized empty
    quantum.projections = ProjectionCache(c3=None, c4=None, c5=None)
    quantum.dissolution_record = None

    # 10. Metadata
    quantum.quantum_hash = compute_quantum_hash(quantum)
    quantum.shard_id = derive_shard_id(vtd.locus)
    quantum.citation_count = 0
    quantum.version = 1

    return quantum
```

**Claim class to claim type mapping:**

| PCVM Claim Class | EMA Claim Type | Rationale |
|-----------------|----------------|-----------|
| D (Deterministic) | observation | Deterministic computation results are system observations |
| E (Empirical) | observation | Empirical observations directly map |
| S (Statistical) | inference | Statistical conclusions are inferred from data |
| H (Heuristic) | inference | Heuristic judgments are inferred from experience |
| N (Normative) | governance | Normative claims are governance rules |
| P (Process) | observation | Process compliance is an observed fact |
| R (Reasoning) | inference | Reasoning produces inferences |
| C (Compliance/Consolidation) | consolidation | C-class from dreaming maps to consolidation type |

### 3.2 ASV to Quantum Field Mapping

When knowledge arrives via ASV/AASL communication (C4) rather than PCVM, it MUST still pass through PCVM before quantum creation. The ASV message provides preliminary field mapping:

```python
def map_asv_to_vtd_draft(asv_message: AASLMessage) -> VTDDraft:
    """Pre-map an AASL message to a VTD draft for PCVM submission."""

    draft = VTDDraft()
    draft.claim_text = asv_message.content.payload
    draft.suggested_class = map_aasl_type_to_claim_class(asv_message.message_type)
    draft.locus = asv_message.topic_ontology.primary_locus
    draft.producing_agent = asv_message.sender.agent_id

    # AASL confidence metadata maps to initial opinion
    if asv_message.confidence is not None:
        draft.initial_opinion = SubjectiveLogicOpinion(
            belief=asv_message.confidence.belief,
            disbelief=asv_message.confidence.disbelief,
            uncertainty=asv_message.confidence.uncertainty,
            base_rate=asv_message.confidence.base_rate
        )
    else:
        draft.initial_opinion = VACUOUS_OPINION

    draft.evidence_refs = asv_message.evidence_references

    return draft
```

The VTD draft is then submitted to PCVM for classification, verification, and sealing. Only after PCVM verification does the quantum enter EMA via the standard MCT/BDL mapping (Section 3.1).

### 3.3 Coherence Graph Insertion

After quantum creation, the quantum is inserted into the coherence graph:

```python
def insert_into_coherence_graph(q: EpistemicQuantum) -> None:
    """Insert quantum into the coherence graph shard for its locus."""

    shard = get_or_create_shard(q.shard_id)

    # 1. Check shard edge budget
    if shard.total_edges >= MAX_EDGES_PER_SHARD:
        prune_lowest_weight_edges(shard, target_count=MAX_EDGES_PER_SHARD * 0.9)

    # 2. Add quantum as node
    shard.add_node(q.id, q)

    # 3. Add pre-existing edges (from VTD dependencies, Section 3.1)
    for edge in q.edges:
        if shard.contains(edge.target_id):
            shard.add_edge(q.id, edge.target_id, edge)
        else:
            # Cross-shard edge: register in cross-shard edge index
            register_cross_shard_edge(q.id, edge.target_id, edge)

    # 4. Run initial edge discovery (Section 3.4)
    discovered_edges = discover_initial_edges(q, shard)
    for edge in discovered_edges:
        if len(q.edges) < MAX_EDGES_PER_QUANTUM:
            q.edges.append(edge)
            shard.add_edge(q.id, edge.target_id, edge)

    # 5. Update version and hash
    q.version += 1
    q.quantum_hash = compute_quantum_hash(q)
```

**Sharding strategy:** The coherence graph is sharded by locus, aligning with C3's parcel partitioning. Each locus has exactly one shard. Cross-locus edges are stored in a cross-shard edge index. This ensures that coherence computation within a locus is bounded to O(V_local * E_max) per epoch, satisfying HG-2.

**Shard structure:**

```python
class CoherenceGraphShard:
    shard_id: ShardId
    locus_id: LocusId
    nodes: Dict[QuantumId, EpistemicQuantum]   # Active quanta in this shard
    edges: Dict[Tuple[QuantumId, QuantumId], EpistemicEdge]
    total_edges: int
    node_count: int

    # Indexes for efficient queries
    edges_by_type: Dict[EdgeType, Set[Tuple[QuantumId, QuantumId]]]
    edges_by_target: Dict[QuantumId, Set[Tuple[QuantumId, EdgeType]]]
    domain_tag_index: Dict[str, Set[QuantumId]]
```

### 3.4 Initial Edge Discovery

When a new quantum is inserted, EMA discovers potential edges to existing quanta using similarity-based heuristics:

```python
def discover_initial_edges(
    q: EpistemicQuantum,
    shard: CoherenceGraphShard
) -> List[EpistemicEdge]:
    """Discover initial edges for a newly inserted quantum."""

    candidates = []

    # 1. Domain tag overlap: find quanta with shared domain tags
    tag_neighbors = set()
    for tag in q.content.domain_tags:
        tag_neighbors.update(shard.domain_tag_index.get(tag, set()))
    tag_neighbors.discard(q.id)

    # 2. Score candidates by semantic similarity
    q_embedding = compute_embedding(q.content.claim_text)
    scored = []
    for neighbor_id in tag_neighbors:
        neighbor = shard.nodes[neighbor_id]
        if neighbor.metabolic_state.phase in ("ACTIVE", "DECAYING"):
            n_embedding = compute_embedding(neighbor.content.claim_text)
            similarity = cosine_similarity(q_embedding, n_embedding)
            if abs(similarity) > EDGE_DISCOVERY_THRESHOLD:
                scored.append((neighbor_id, similarity))

    # 3. Sort by absolute similarity, take top-K
    scored.sort(key=lambda x: abs(x[1]), reverse=True)
    top_k = scored[:INITIAL_EDGE_DISCOVERY_K]

    # 4. Create edges based on similarity polarity and magnitude
    edges = []
    for neighbor_id, similarity in top_k:
        if similarity > SUPPORT_SIMILARITY_THRESHOLD:
            edge_type = "SUPPORT"
            weight = similarity
        elif similarity < -CONTRADICTION_SIMILARITY_THRESHOLD:
            edge_type = "CONTRADICTION"
            weight = abs(similarity)
        else:
            edge_type = "ANALOGY"
            weight = abs(similarity)

        edges.append(EpistemicEdge(
            target_id=neighbor_id,
            edge_type=edge_type,
            weight=weight,
            created_at=current_timestamp(),
            last_activated=current_timestamp(),
            creating_agent="ema:edge_discovery"
        ))

    return edges
```

**Discovery parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `EDGE_DISCOVERY_THRESHOLD` | 0.4 | Minimum absolute cosine similarity to create edge |
| `INITIAL_EDGE_DISCOVERY_K` | 10 | Maximum edges discovered per insertion |
| `SUPPORT_SIMILARITY_THRESHOLD` | 0.6 | Positive similarity above this creates SUPPORT edge |
| `CONTRADICTION_SIMILARITY_THRESHOLD` | 0.6 | Negative similarity below this creates CONTRADICTION edge |

---

## 4. Circulation Protocol

### 4.1 Subscription Model

Agents and subsystems subscribe to quantum circulation using topic-based subscriptions:

```json
{
  "$id": "https://ema.atrahasis.dev/schema/v1/subscription.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Circulation Subscription",
  "type": "object",
  "required": ["subscriber_id", "subscription_type", "filter"],
  "properties": {
    "subscriber_id": {
      "type": "string",
      "description": "AgentId or subsystem identifier."
    },
    "subscription_type": {
      "type": "string",
      "enum": ["domain_tag", "claim_class", "locus", "credibility_threshold", "composite"],
      "description": "Type of subscription filter."
    },
    "filter": {
      "type": "object",
      "properties": {
        "domain_tags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Match quanta with any of these domain tags."
        },
        "claim_classes": {
          "type": "array",
          "items": { "type": "string", "enum": ["D","E","S","H","N","P","R","C"] },
          "description": "Match quanta with any of these claim classes."
        },
        "loci": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Match quanta in any of these loci."
        },
        "min_credibility": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Only circulate quanta with E(w) >= this threshold."
        },
        "min_vitality": {
          "type": "number", "minimum": 0.0, "maximum": 1.0,
          "description": "Only circulate quanta with vitality >= this threshold."
        },
        "exclude_claim_types": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Exclude quanta with these claim types."
        }
      }
    },
    "max_per_epoch": {
      "type": "integer", "minimum": 1, "default": 100,
      "description": "Maximum quanta delivered per epoch to this subscriber."
    },
    "projection_target": {
      "type": ["string", "null"],
      "enum": ["C3", "C4", "C5", null],
      "description": "If set, deliver projected form instead of canonical quantum."
    },
    "priority": {
      "type": "integer", "minimum": 0, "maximum": 10, "default": 5,
      "description": "Subscriber priority for budget allocation. 10=highest."
    }
  }
}
```

**Subscription registration:**

```python
def register_subscription(sub: Subscription) -> SubscriptionId:
    """Register a circulation subscription. Returns unique subscription ID."""
    validate_subscriber_exists(sub.subscriber_id)
    validate_filter(sub.filter)
    sub_id = generate_subscription_id()
    subscription_registry[sub_id] = sub
    rebuild_routing_index()
    return sub_id
```

### 4.2 Push Notification Protocol

During the Circulation phase of each epoch, EMA pushes quanta to matching subscribers:

```python
def execute_circulation(epoch: EpochNum, budget: float) -> CirculationReport:
    """Execute circulation phase for the current epoch."""

    report = CirculationReport(epoch=epoch)
    budget_remaining = budget
    delivery_queue = []

    # 1. Identify quanta eligible for circulation
    eligible = [
        q for q in all_active_quanta()
        if q.metabolic_state.phase == "ACTIVE"
        and should_circulate(q, epoch)
    ]

    # 2. Sort by circulation priority
    eligible.sort(key=lambda q: circulation_priority(q, epoch), reverse=True)

    # 3. Match quanta to subscribers
    for q in eligible:
        if budget_remaining <= 0:
            break
        matching_subs = find_matching_subscriptions(q)
        for sub in matching_subs:
            if sub.delivered_this_epoch >= sub.max_per_epoch:
                continue
            delivery_queue.append((q, sub))

    # 4. Execute deliveries within budget
    for q, sub in delivery_queue:
        if budget_remaining <= DELIVERY_COST:
            break

        if sub.projection_target is not None:
            payload = project_quantum(q, sub.projection_target)
        else:
            payload = serialize_quantum(q)

        deliver_to_subscriber(sub.subscriber_id, payload)

        # Update quantum metadata
        q.metabolic_state.circulation_count += 1
        q.timestamps.last_circulated = current_timestamp()
        sub.delivered_this_epoch += 1
        budget_remaining -= DELIVERY_COST
        report.deliveries += 1

    report.budget_used = budget - budget_remaining
    return report


def should_circulate(q: EpistemicQuantum, epoch: EpochNum) -> bool:
    """Determine if a quantum should be circulated this epoch."""
    # Newly created quanta: always circulate in first epoch
    if q.provenance.generation_epoch == epoch:
        return True
    # Recently updated quanta (opinion or edges changed)
    if q.timestamps.last_verified is not None:
        if epoch - epoch_of(q.timestamps.last_verified) <= RECIRCULATION_WINDOW:
            return True
    # High-vitality quanta that haven't been circulated recently
    if q.metabolic_state.vitality > VITALITY_CIRCULATION_THRESHOLD:
        if q.timestamps.last_circulated is None:
            return True
        if epoch - epoch_of(q.timestamps.last_circulated) > CIRCULATION_COOLDOWN:
            return True
    return False


def circulation_priority(q: EpistemicQuantum, epoch: EpochNum) -> float:
    """Compute circulation priority. Higher = circulated first."""
    recency_bonus = 1.0 if q.provenance.generation_epoch == epoch else 0.0
    vitality_score = q.metabolic_state.vitality
    credibility = q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty
    novelty = 1.0 / (1.0 + q.metabolic_state.circulation_count)
    return recency_bonus * 2.0 + vitality_score + credibility + novelty
```

### 4.3 Flow Control (SHREC-Regulated)

Circulation throughput is regulated by SHREC (Section 7). The circulation budget is allocated by SHREC each epoch:

```python
def get_circulation_budget(epoch: EpochNum) -> float:
    """Get SHREC-allocated budget for circulation this epoch."""
    shrec_state = get_shrec_state(epoch)
    # Circulation draws primarily from epistemic_hunger signal allocation
    hunger_budget = shrec_state.allocations["HUNGER"]
    # Also draws partially from novelty signal
    novelty_contribution = shrec_state.allocations["NOVELTY"] * NOVELTY_TO_CIRCULATION_RATIO
    return hunger_budget + novelty_contribution
```

**Flow control rules:**

1. **Budget exhaustion:** When circulation budget is exhausted, remaining deliveries are deferred to the next epoch. Deferred deliveries get priority bonus in the next epoch's queue.
2. **Backpressure:** If a subscriber's delivery queue exceeds `MAX_SUBSCRIBER_BACKLOG`, new deliveries to that subscriber are dropped with a backpressure signal sent to SHREC (increases metabolic_stress signal).
3. **Priority inversion prevention:** High-priority subscribers (priority >= 8) are guaranteed at least `MIN_HIGH_PRIORITY_DELIVERIES` per epoch before lower-priority subscribers receive any deliveries.

### 4.4 Edge Weight Update Rules

During circulation, edge weights are updated based on co-activation patterns:

```python
def update_edge_weights_for_epoch(shard: CoherenceGraphShard, epoch: EpochNum) -> None:
    """Update all edge weights in shard based on epoch activity."""

    accessed_this_epoch = set()
    for qid, q in shard.nodes.items():
        if q.timestamps.last_accessed is not None:
            if epoch_of(q.timestamps.last_accessed) == epoch:
                accessed_this_epoch.add(qid)

    for (src, tgt), edge in shard.edges.items():
        if src in accessed_this_epoch and tgt in accessed_this_epoch:
            # Co-activation: Hebbian strengthening
            edge.weight = edge.weight + REINFORCEMENT_RATE * (1.0 - edge.weight)
            edge.last_activated = current_timestamp()
        else:
            # Check decay
            epochs_since = epoch - epoch_of(edge.last_activated)
            if epochs_since > EDGE_TTL:
                # Mark for pruning
                edge.weight = 0.0
            elif epochs_since > 0:
                edge.weight = edge.weight * (1.0 - EDGE_DECAY_RATE)

        # Prune dead edges
        if edge.weight < MIN_EDGE_WEIGHT and edge.edge_type != "DERIVATION":
            shard.remove_edge(src, tgt)
            # Note: DERIVATION edges are never pruned (immutable provenance)
```

**Edge weight parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REINFORCEMENT_RATE` | 0.05 | Per-epoch Hebbian strengthening rate |
| `EDGE_DECAY_RATE` | 0.02 | Per-epoch decay rate for inactive edges |
| `EDGE_TTL` | 50 | Epochs without reinforcement before edge is pruned |
| `MIN_EDGE_WEIGHT` | 0.05 | Minimum weight; below this, edge is pruned (except DERIVATION) |
| `MAX_EDGES_PER_QUANTUM` | 50 | Maximum edges per quantum (INV-E6) |
| `MAX_EDGES_PER_SHARD` | 500000 | Maximum total edges per shard (INV-E6) |

---

## 5. Consolidation Protocol

The consolidation (dreaming) protocol is EMA's anabolic process. It identifies clusters of related quanta, synthesizes higher-level principles via LLM inference, gates outputs through PCVM verification, and integrates verified consolidations into the coherence graph.

### 5.1 Candidate Identification Algorithm

Consolidation candidates are clusters of quanta that meet density and diversity requirements:

```python
def identify_consolidation_candidates(
    shard: CoherenceGraphShard,
    epoch: EpochNum
) -> List[ConsolidationCandidate]:
    """Identify clusters eligible for consolidation in this shard."""

    candidates = []

    # 1. Find dense subgraphs via mutual support edge detection
    active_quanta = [
        q for q in shard.nodes.values()
        if q.metabolic_state.phase == "ACTIVE"
        and q.metabolic_state.consolidation_lock is None
    ]

    # 2. Build support adjacency for active quanta
    support_adj = defaultdict(set)
    for (src, tgt), edge in shard.edges.items():
        if edge.edge_type == "SUPPORT" and edge.weight > CONSOLIDATION_MIN_EDGE_WEIGHT:
            if src in [q.id for q in active_quanta] and tgt in [q.id for q in active_quanta]:
                support_adj[src].add(tgt)
                support_adj[tgt].add(src)  # Treat as undirected for clustering

    # 3. Find connected components with >= MIN_CLUSTER_SIZE nodes
    visited = set()
    for q in active_quanta:
        if q.id in visited:
            continue
        cluster = bfs_collect(q.id, support_adj, visited)
        if len(cluster) >= MIN_CLUSTER_SIZE:
            # 4. Verify mutual support density
            mutual_support_count = count_mutual_support_edges(cluster, shard)
            if mutual_support_count >= MIN_MUTUAL_SUPPORT_EDGES:
                candidates.append(ConsolidationCandidate(
                    quantum_ids=cluster,
                    mutual_support_count=mutual_support_count,
                    shard_id=shard.shard_id,
                    identified_at_epoch=epoch
                ))

    # 5. Sort by consolidation potential (larger, denser clusters first)
    candidates.sort(
        key=lambda c: len(c.quantum_ids) * c.mutual_support_count,
        reverse=True
    )

    # 6. Limit to MAX_CONSOLIDATION_CANDIDATES_PER_EPOCH
    return candidates[:MAX_CONSOLIDATION_CANDIDATES_PER_EPOCH]


def bfs_collect(start: QuantumId, adj: Dict, visited: Set) -> Set[QuantumId]:
    """BFS to collect connected component."""
    queue = deque([start])
    component = set()
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        component.add(node)
        for neighbor in adj.get(node, set()):
            if neighbor not in visited:
                queue.append(neighbor)
    return component
```

**Candidate identification parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MIN_CLUSTER_SIZE` | 5 | Minimum quanta in a consolidation candidate cluster |
| `MIN_MUTUAL_SUPPORT_EDGES` | 3 | Minimum mutual support edges within cluster |
| `CONSOLIDATION_MIN_EDGE_WEIGHT` | 0.3 | Minimum edge weight to count for clustering |
| `MAX_CONSOLIDATION_CANDIDATES_PER_EPOCH` | 5 | Maximum clusters to attempt consolidation per epoch |

### 5.2 Provenance Diversity Verification

Each consolidation candidate MUST pass provenance diversity checks before proceeding. This prevents consolidation poisoning (Adversarial A3).

```python
def verify_provenance_diversity(
    candidate: ConsolidationCandidate,
    shard: CoherenceGraphShard
) -> DiversityResult:
    """Verify that consolidation candidate has sufficient provenance diversity."""

    quanta = [shard.nodes[qid] for qid in candidate.quantum_ids]

    # 1. Count independent generating agents
    agents = set()
    for q in quanta:
        agents.add(q.provenance.generating_agent)
        for attr in q.provenance.attribution_chain:
            if attr.role == "creator":
                agents.add(attr.agent_id)
    independent_agents = len(agents)

    # 2. Count independent parcels (from locus/shard mapping)
    parcels = set()
    for q in quanta:
        parcel = resolve_quantum_to_parcel(q.id)
        if parcel is not None:
            parcels.add(parcel)
    independent_parcels = len(parcels)

    # 3. Check derivation chain independence
    # Two quanta are derivation-independent if neither derives from the other
    derivation_chains = build_derivation_chains(quanta)
    independent_chains = count_independent_chains(derivation_chains)

    # 4. Evaluate diversity
    passes = (
        independent_agents >= MIN_INDEPENDENT_AGENTS
        and independent_parcels >= MIN_INDEPENDENT_PARCELS
        and independent_chains >= MIN_INDEPENDENT_CHAINS
    )

    return DiversityResult(
        passes=passes,
        independent_agents=independent_agents,
        independent_parcels=independent_parcels,
        independent_chains=independent_chains,
        reason=None if passes else generate_diversity_failure_reason(
            independent_agents, independent_parcels, independent_chains
        )
    )


def count_independent_chains(chains: List[Set[QuantumId]]) -> int:
    """Count derivation chains with no shared ancestors."""
    # Two chains are independent if their ancestor sets do not overlap
    independent = 0
    used = set()
    for chain_ancestors in sorted(chains, key=len):
        if not chain_ancestors.intersection(used):
            independent += 1
            used.update(chain_ancestors)
    return independent
```

**Diversity parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MIN_INDEPENDENT_AGENTS` | 5 | Minimum distinct generating agents (HG-3) |
| `MIN_INDEPENDENT_PARCELS` | 3 | Minimum distinct source parcels (HG-3) |
| `MIN_INDEPENDENT_CHAINS` | 3 | Minimum derivation-independent chains |

### 5.3 Consolidation Lock Protocol

Before LLM synthesis begins, all candidate quanta MUST be locked to prevent concurrent catabolism (INV-E4):

```python
def acquire_consolidation_locks(
    candidate: ConsolidationCandidate,
    session_id: DreamingSessionId,
    epoch: EpochNum
) -> LockResult:
    """Atomically acquire consolidation locks on all candidate quanta.
    Returns success or failure — partial locking is not permitted.
    """

    quanta = [get_quantum(qid) for qid in candidate.quantum_ids]

    # 1. Pre-check: all quanta must be in ACTIVE state
    for q in quanta:
        if q.metabolic_state.phase != "ACTIVE":
            return LockResult(
                success=False,
                reason=f"Quantum {q.id} in state {q.metabolic_state.phase}, not ACTIVE"
            )
        if q.metabolic_state.consolidation_lock is not None:
            return LockResult(
                success=False,
                reason=f"Quantum {q.id} already locked by {q.metabolic_state.consolidation_lock.dreaming_session_id}"
            )

    # 2. Atomic lock acquisition (all or nothing)
    lock = ConsolidationLock(
        dreaming_session_id=session_id,
        locked_at=current_timestamp(),
        lock_ttl_epochs=CONSOLIDATION_LOCK_TTL,
        lock_epoch=epoch
    )

    for q in quanta:
        q.metabolic_state.phase = "CONSOLIDATING"
        q.metabolic_state.consolidation_lock = lock

    return LockResult(success=True, locked_count=len(quanta))


def release_consolidation_locks(session_id: DreamingSessionId) -> int:
    """Release all locks held by a dreaming session. Returns count released."""
    released = 0
    for q in find_quanta_locked_by(session_id):
        q.metabolic_state.phase = "ACTIVE"
        q.metabolic_state.consolidation_lock = None
        released += 1
    return released
```

**Lock parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CONSOLIDATION_LOCK_TTL` | 5 | Maximum epochs a lock can be held |
| `LOCK_TTL_HALVING_ON_FAILURE` | true | Halve TTL on repeated consolidation failure for same quantum |
| `MIN_LOCK_TTL` | 1 | Minimum lock TTL after halving |

### 5.4 LLM Synthesis Specification

The LLM synthesis pass generates candidate consolidated claims from source quanta:

```python
def execute_llm_synthesis(
    candidate: ConsolidationCandidate,
    shard: CoherenceGraphShard,
    session_id: DreamingSessionId
) -> List[SynthesisResult]:
    """Execute 3-pass LLM synthesis with majority voting."""

    source_quanta = [shard.nodes[qid] for qid in candidate.quantum_ids]

    # 1. Prepare synthesis context
    context = prepare_synthesis_context(source_quanta)

    # 2. Execute 3 independent passes with different prompt framings
    pass_results = []
    for pass_num in range(NUM_SYNTHESIS_PASSES):
        prompt = construct_synthesis_prompt(
            context=context,
            framing=SYNTHESIS_FRAMINGS[pass_num],
            pass_number=pass_num
        )
        result = llm_inference(
            prompt=prompt,
            temperature=SYNTHESIS_TEMPERATURE,
            max_tokens=SYNTHESIS_MAX_TOKENS
        )
        parsed = parse_synthesis_output(result)
        pass_results.append(parsed)

    # 3. Majority voting: retain claims that appear in >= 2 of 3 passes
    consolidated_claims = majority_vote(pass_results, threshold=MAJORITY_THRESHOLD)

    # 4. Filter: consolidated claim must not duplicate existing active quanta
    filtered = []
    for claim in consolidated_claims:
        if not is_semantically_duplicate(claim, shard):
            filtered.append(claim)

    return filtered


def prepare_synthesis_context(quanta: List[EpistemicQuantum]) -> SynthesisContext:
    """Prepare context package for LLM synthesis."""
    return SynthesisContext(
        claim_texts=[q.content.claim_text for q in quanta],
        domain_tags=collect_unique_tags(quanta),
        edge_structure=extract_edge_summary(quanta),
        opinion_summary=[
            {
                "id": q.id,
                "credibility": q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty,
                "uncertainty": q.opinion.uncertainty
            }
            for q in quanta
        ],
        instruction="Identify cross-domain patterns, structural analogies, or generalizable principles that emerge from these knowledge units. Flag uncertain inferences explicitly."
    )
```

**Synthesis prompt framings (3 passes):**

| Pass | Framing | Purpose |
|------|---------|---------|
| 0 | "What general principle connects these observations?" | Inductive generalization |
| 1 | "What structural analogy exists between these domains?" | Cross-domain pattern detection |
| 2 | "What prediction follows from combining these claims?" | Deductive/predictive synthesis |

**Synthesis parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `NUM_SYNTHESIS_PASSES` | 3 | Number of independent LLM passes |
| `SYNTHESIS_TEMPERATURE` | 0.3 | LLM temperature (low creativity, high coherence) |
| `SYNTHESIS_MAX_TOKENS` | 2048 | Maximum tokens per synthesis output |
| `MAJORITY_THRESHOLD` | 2 | Minimum passes a claim must appear in |
| `SEMANTIC_DUPLICATE_THRESHOLD` | 0.92 | Cosine similarity above which claim is considered duplicate |

**Majority voting algorithm:**

```python
def majority_vote(
    pass_results: List[List[ParsedClaim]],
    threshold: int
) -> List[ConsolidatedClaim]:
    """Retain claims appearing in >= threshold passes."""

    # Flatten all claims and group by semantic similarity
    all_claims = []
    for pass_num, results in enumerate(pass_results):
        for claim in results:
            all_claims.append((pass_num, claim))

    # Cluster by semantic similarity
    clusters = cluster_by_similarity(
        [c.text for _, c in all_claims],
        threshold=MAJORITY_VOTE_SIMILARITY
    )

    # Retain clusters with claims from >= threshold distinct passes
    retained = []
    for cluster_indices in clusters:
        passes_represented = set(all_claims[i][0] for i in cluster_indices)
        if len(passes_represented) >= threshold:
            # Select the claim with highest inter-cluster similarity as representative
            representative = select_representative(cluster_indices, all_claims)
            retained.append(ConsolidatedClaim(
                text=representative.text,
                source_quantum_ids=[q.id for q in pass_results[0]],  # All source quanta
                passes_confirmed=len(passes_represented),
                synthesis_reasoning=representative.reasoning
            ))

    return retained
```

### 5.5 VTD Construction for Consolidated Claims

Each consolidated claim is packaged as a C-class VTD for PCVM submission:

```python
def construct_consolidation_vtd(
    claim: ConsolidatedClaim,
    source_quanta: List[EpistemicQuantum],
    session_id: DreamingSessionId
) -> VTD:
    """Construct a C-class VTD for a consolidated claim."""

    vtd = VTD()
    vtd.claim_text = claim.text
    vtd.suggested_class = "C"
    vtd.producing_agent = f"ema:dreaming:{session_id}"
    vtd.epoch = current_epoch()
    vtd.locus = determine_consolidation_locus(source_quanta)
    vtd.timestamp = current_timestamp()

    # C-class proof body
    vtd.proof_body = {
        "source_quanta": [
            {
                "quantum_id": q.id,
                "claim_text": q.content.claim_text,
                "credibility": q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty,
                "domain_tags": q.content.domain_tags
            }
            for q in source_quanta
        ],
        "synthesis_reasoning": claim.synthesis_reasoning,
        "novelty_justification": generate_novelty_justification(claim, source_quanta),
        "falsifiability_statement": generate_falsifiability_statement(claim),
        "confidence_basis": {
            "method": "LLM synthesis with 3-pass majority voting",
            "passes_confirmed": claim.passes_confirmed,
            "initial_uncertainty": max(0.4, 1.0 - claim.passes_confirmed * 0.2),
            "rationale": "High initial uncertainty due to synthetic origin per EMA specification."
        }
    }

    # Dependencies: all source quanta
    vtd.dependencies = [
        {
            "claim_id": resolve_quantum_to_claim(q.id),
            "relationship": "EVIDENCE",
            "required_credibility": 0.5
        }
        for q in source_quanta
    ]

    # Counter-evidence
    vtd.counter_evidence = {
        "considered": True,
        "items": generate_counter_evidence_analysis(claim, source_quanta)
    }

    # Compute hash and sign
    vtd.vtd_hash = compute_vtd_hash(vtd)
    vtd.agent_signature = sign_vtd(vtd, f"ema:dreaming:{session_id}")

    return vtd
```

**Initial opinion for consolidated claims:**

```python
def compute_initial_consolidation_opinion(
    claim: ConsolidatedClaim,
    source_quanta: List[EpistemicQuantum]
) -> SubjectiveLogicOpinion:
    """Compute initial opinion for a C-class consolidated claim.
    Uncertainty MUST be >= 0.4 per C-class requirements.
    """
    # Average source credibility, discounted for synthesis uncertainty
    avg_credibility = mean([
        q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty
        for q in source_quanta
    ])

    # Synthesis discount: consolidation adds uncertainty
    synthesis_discount = 0.6  # Retain 60% of source credibility
    adjusted_belief = avg_credibility * synthesis_discount * 0.5

    # Ensure minimum uncertainty
    uncertainty = max(0.4, 1.0 - adjusted_belief - 0.05)
    disbelief = 1.0 - adjusted_belief - uncertainty
    disbelief = max(0.0, disbelief)

    # Renormalize
    total = adjusted_belief + disbelief + uncertainty
    return SubjectiveLogicOpinion(
        belief=adjusted_belief / total,
        disbelief=disbelief / total,
        uncertainty=uncertainty / total,
        base_rate=0.5  # Neutral base rate for synthetic claims
    )
```

### 5.6 PCVM Submission and Verification

Consolidated VTDs are submitted to PCVM for verification via the standard C5 API:

```python
def submit_consolidation_to_pcvm(
    vtd: VTD,
    session_id: DreamingSessionId
) -> PCVMResult:
    """Submit C-class VTD to PCVM for verification."""

    # 1. Submit to PCVM via integration API (Section 10.1)
    result = pcvm_api.submit_vtd(vtd)

    # 2. If high-impact (source quanta connected to >5 active quanta),
    #    request adversarial probing
    if count_downstream_connections(vtd) > HIGH_IMPACT_THRESHOLD:
        adversarial_result = pcvm_api.request_adversarial_probe(vtd.vtd_id)
        if adversarial_result.probe_succeeded:
            # Adversarial probe found a flaw
            result.verdict = "REJECTED"
            result.rejection_reason = adversarial_result.flaw_description
            log_adversarial_rejection(session_id, vtd, adversarial_result)

    return result
```

**PCVM verification requirements for C-class claims (from C5 spec):**

1. Source quanta MUST all be in ACTIVE phase (not quarantined/dissolved)
2. At least 3 source quanta from at least 2 different domains
3. Consolidated claim MUST NOT be semantically equivalent to any existing active quantum
4. If consolidation modifies existing claim, SUPERSESSION edge required
5. Synthesis reasoning chain MUST be logically valid
6. Falsifiability statement MUST be non-trivial

### 5.7 Post-Verification Integration

When a consolidated claim passes PCVM verification:

```python
def integrate_verified_consolidation(
    vtd: VTD,
    pcvm_result: PCVMResult,
    candidate: ConsolidationCandidate,
    session_id: DreamingSessionId
) -> EpistemicQuantum:
    """Integrate a verified C-class claim into the coherence graph."""

    # 1. Create new quantum via standard ingestion mapping
    new_quantum = map_vtd_to_quantum(vtd, pcvm_result)
    new_quantum.content.claim_type = "consolidation"
    new_quantum.provenance.generating_activity = "consolidation"

    # 2. Create DERIVATION edges from source quanta to new quantum
    source_quanta = [get_quantum(qid) for qid in candidate.quantum_ids]
    for source_q in source_quanta:
        edge = EpistemicEdge(
            target_id=new_quantum.id,
            edge_type="DERIVATION",
            weight=1.0,
            created_at=current_timestamp(),
            last_activated=current_timestamp(),
            creating_agent=f"ema:dreaming:{session_id}"
        )
        if len(source_q.edges) < MAX_EDGES_PER_QUANTUM:
            source_q.edges.append(edge)
        source_q.citation_count += 1  # Increment citation count

    # 3. Insert into coherence graph
    insert_into_coherence_graph(new_quantum)

    # 4. Release consolidation locks
    release_consolidation_locks(session_id)

    # 5. Log consolidation event
    log_consolidation_success(
        session_id=session_id,
        new_quantum_id=new_quantum.id,
        source_count=len(source_quanta),
        pcvm_verdict=pcvm_result.verdict
    )

    return new_quantum
```

### 5.8 Failure Handling and Cooldown

When consolidation fails (PCVM rejects the claim, or synthesis produces no valid candidates):

```python
def handle_consolidation_failure(
    candidate: ConsolidationCandidate,
    session_id: DreamingSessionId,
    failure_reason: str
) -> None:
    """Handle failed consolidation attempt."""

    # 1. Release locks
    release_consolidation_locks(session_id)

    # 2. Log failure
    log_consolidation_failure(
        session_id=session_id,
        quantum_ids=candidate.quantum_ids,
        reason=failure_reason
    )

    # 3. Apply cooldown: source quanta cannot be consolidation candidates
    #    for CONSOLIDATION_COOLDOWN_EPOCHS
    for qid in candidate.quantum_ids:
        q = get_quantum(qid)
        set_consolidation_cooldown(q, CONSOLIDATION_COOLDOWN_EPOCHS)

    # 4. Reduce lock TTL for future attempts on these quanta
    for qid in candidate.quantum_ids:
        q = get_quantum(qid)
        current_ttl = get_effective_lock_ttl(q)
        new_ttl = max(MIN_LOCK_TTL, current_ttl // 2)
        set_effective_lock_ttl(q, new_ttl)

    # 5. Update SHREC: consolidation failure increases consolidation_pressure
    shrec_signal_update("CONSOLIDATION", delta=+CONSOLIDATION_FAILURE_SIGNAL_BOOST)
```

**Failure parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CONSOLIDATION_COOLDOWN_EPOCHS` | 20 | Epochs before failed candidates can be retried |
| `HIGH_IMPACT_THRESHOLD` | 5 | Downstream connections triggering adversarial probing |
| `CONSOLIDATION_FAILURE_SIGNAL_BOOST` | 0.1 | SHREC signal increase on failure |

### 5.9 Empirical Validation Queue for C-Class

Per RA-5 and Adversarial A2, C-class claims without empirical validation are subject to aging uncertainty increase:

```python
def age_unvalidated_consolidations(epoch: EpochNum) -> None:
    """Increase uncertainty of C-class claims lacking empirical validation."""

    for q in all_active_quanta():
        if q.claim_class != "C":
            continue
        if q.content.claim_type != "consolidation":
            continue

        age = epoch - q.provenance.generation_epoch

        # Check for confirming or disconfirming evidence
        has_evidence = any(
            e.edge_type in ("SUPPORT", "CONTRADICTION")
            and epoch_of(e.created_at) > q.provenance.generation_epoch
            and e.creating_agent != q.provenance.generating_agent
            for e in q.edges
        )

        if not has_evidence and age > CCLASS_VALIDATION_WINDOW:
            # Increase uncertainty by CCLASS_AGING_UNCERTAINTY_RATE per window
            periods = (age - CCLASS_VALIDATION_WINDOW) // CCLASS_VALIDATION_WINDOW
            uncertainty_increase = periods * CCLASS_AGING_UNCERTAINTY_RATE

            # Apply: shift belief mass to uncertainty
            new_uncertainty = min(0.95, q.opinion.uncertainty + uncertainty_increase)
            belief_reduction = new_uncertainty - q.opinion.uncertainty
            new_belief = max(0.01, q.opinion.belief - belief_reduction)

            q.opinion = SubjectiveLogicOpinion(
                belief=new_belief,
                disbelief=q.opinion.disbelief,
                uncertainty=new_uncertainty,
                base_rate=q.opinion.base_rate
            )
            # Renormalize
            normalize_opinion(q.opinion)
            q.version += 1
```

**Aging parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CCLASS_VALIDATION_WINDOW` | 50 | Epochs before aging begins |
| `CCLASS_AGING_UNCERTAINTY_RATE` | 0.1 | Uncertainty increase per validation window |

---

## 6. Catabolism Protocol

The catabolism protocol manages the dissolution of quanta that have lost credibility, relevance, or temporal validity. It implements a two-phase process: quarantine (reversible) followed by dissolution (irreversible, with recycling).

### 6.1 Dissolution Criteria Evaluation

During the Catabolism phase of each epoch, all non-locked quanta in ACTIVE or DECAYING state are evaluated:

```python
def evaluate_catabolism(shard: CoherenceGraphShard, epoch: EpochNum) -> CatabolismReport:
    """Evaluate all quanta in shard for catabolism triggers."""

    report = CatabolismReport(epoch=epoch)

    for qid, q in shard.nodes.items():
        # Skip quanta that are locked, already quarantined, or dissolved
        if q.metabolic_state.phase in ("CONSOLIDATING", "QUARANTINED", "DISSOLVED"):
            continue

        # Skip structurally protected quanta
        if is_structurally_protected(q):
            continue

        # Evaluate dissolution criteria (OR logic)
        triggers = []

        # Criterion 1: Low credibility AND old
        credibility = q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty
        age = epoch - q.provenance.generation_epoch
        if credibility < CATABOLISM_CREDIBILITY_THRESHOLD and age > DECAY_AGE_THRESHOLD:
            triggers.append("low_credibility")

        # Criterion 2: Temporal validity expired
        if has_temporal_expiry(q) and is_expired(q, epoch):
            triggers.append("temporal_expiry")

        # Criterion 3: Superseded by higher-credibility quantum
        superseding = find_superseding_quanta(q, shard)
        if superseding and superseding_credibility(superseding) > credibility + SUPERSESSION_MARGIN:
            triggers.append("superseded")

        # Criterion 4: Quarantine timeout (handled in state machine, Section 2.2)

        # Apply transitions
        if triggers:
            if q.metabolic_state.phase == "ACTIVE":
                q.metabolic_state.phase = "DECAYING"
                q.timestamps.decay_start = current_timestamp()
                report.newly_decaying += 1
            elif q.metabolic_state.phase == "DECAYING":
                vitality = compute_vitality(q, epoch)
                if vitality < QUARANTINE_THRESHOLD:
                    transition_to_quarantine(q, triggers[0])
                    report.newly_quarantined += 1

    # Process quanta already in quarantine
    for qid, q in shard.nodes.items():
        if q.metabolic_state.phase == "QUARANTINED":
            quarantine_age = epoch - epoch_of(q.timestamps.decay_start)
            if quarantine_age > MAX_QUARANTINE_EPOCHS:
                execute_dissolution(q, reason="quarantine_timeout")
                report.dissolved += 1

    return report
```

**Catabolism parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CATABOLISM_CREDIBILITY_THRESHOLD` | 0.3 | Credibility below which quantum is dissolution candidate |
| `DECAY_AGE_THRESHOLD` | 100 | Minimum age (epochs) before low-credibility catabolism applies |
| `QUARANTINE_THRESHOLD` | 0.15 | Vitality below which quantum is quarantined |
| `MAX_QUARANTINE_EPOCHS` | 100 | Maximum epochs in quarantine before dissolution |
| `SUPERSESSION_MARGIN` | 0.1 | Superseding quantum must exceed by this margin |
| `MAX_DECAY_EPOCHS` | 50 | Maximum epochs in DECAYING state before forced quarantine |

### 6.2 Structural Protection (Self/Non-Self Discrimination)

Quanta with high citation counts are structurally important to the knowledge graph and are immune to catabolism. This is analogous to self/non-self discrimination in biological immune systems.

```python
def is_structurally_protected(q: EpistemicQuantum) -> bool:
    """Check if quantum is protected from catabolism by structural importance."""

    # Primary protection: citation count
    if q.citation_count >= STRUCTURAL_PROTECTION_THRESHOLD:
        return True

    # Secondary protection: keystone detection
    # A quantum is a keystone if its removal would disconnect > KEYSTONE_DISCONNECT_THRESHOLD
    # other quanta from the coherence graph
    if is_keystone(q):
        return True

    return False


def is_keystone(q: EpistemicQuantum) -> bool:
    """Check if quantum is a graph keystone (removal causes disconnection)."""
    shard = get_shard(q.shard_id)
    # Count quanta reachable only through this quantum
    reachable_without = count_reachable_without(q.id, shard)
    total_reachable = shard.node_count - 1
    disconnected = total_reachable - reachable_without
    return disconnected > KEYSTONE_DISCONNECT_THRESHOLD
```

**Protection parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `STRUCTURAL_PROTECTION_THRESHOLD` | 10 | Citation count granting catabolism immunity |
| `KEYSTONE_DISCONNECT_THRESHOLD` | 5 | Disconnection count making quantum a keystone |

### 6.3 Recycling Procedure

Before dissolution, the system recycles valuable components from the quantum to surviving quanta:

```python
def execute_recycling(q: EpistemicQuantum) -> RecyclingResult:
    """Recycle evidence and provenance from a quantum before dissolution."""

    result = RecyclingResult()

    # 1. Identify recyclable evidence
    for evidence_item in q.content.evidence:
        if evidence_item.source_quantum_id is not None:
            source = get_quantum(evidence_item.source_quantum_id)
            if source is not None and source.metabolic_state.phase == "ACTIVE":
                # Evidence references active quantum: already preserved
                result.preserved_references.append(evidence_item.source_quantum_id)
                continue

        if evidence_item.external_reference is not None:
            # External reference: redistribute to quanta with same domain tags
            recipients = find_quanta_by_domain_overlap(
                q.content.domain_tags,
                exclude=[q.id],
                limit=MAX_RECYCLING_RECIPIENTS
            )
            for recipient in recipients:
                if can_accept_evidence(recipient, evidence_item):
                    add_evidence_to_quantum(recipient, evidence_item)
                    result.recycled_to.append(recipient.id)
                    break
            else:
                result.eliminated.append({
                    "evidence_hash": hash_evidence(evidence_item),
                    "reason": "no_eligible_recipient"
                })

    # 2. Preserve DERIVATION edges in dissolution record
    derivation_edges = [
        e for e in q.edges if e.edge_type == "DERIVATION"
    ]
    result.preserved_derivations = [
        {"target": e.target_id, "weight": e.weight}
        for e in derivation_edges
    ]

    # 3. Update citation counts on quanta that cited this quantum
    for e in q.edges:
        if e.edge_type == "DERIVATION" and e.target_id == q.id:
            # Another quantum derived from this one
            pass  # Citation counts on THIS quantum don't matter after dissolution
        if e.edge_type in ("SUPPORT", "DERIVATION"):
            target = get_quantum(e.target_id)
            if target is not None:
                # Don't decrement citation_count — the historical fact remains
                pass

    return result
```

### 6.4 Elimination Procedure

After recycling, components that cannot be recycled are eliminated:

```python
def execute_dissolution(q: EpistemicQuantum, reason: str) -> None:
    """Execute final dissolution of a quantum."""

    # 1. Execute recycling
    recycling_result = execute_recycling(q)

    # 2. Create dissolution record
    q.dissolution_record = DissolutionRecord(
        reason=reason,
        dissolved_at_epoch=current_epoch(),
        dissolved_at=current_timestamp(),
        recycled_to=recycling_result.recycled_to,
        eliminated_evidence=[
            {"evidence_hash": e["evidence_hash"], "reason": e["reason"]}
            for e in recycling_result.eliminated
        ],
        content_hash=sha256(json_serialize(q.content)),
        final_opinion=copy(q.opinion),
        quarantine_snapshot_hash=compute_snapshot_hash(q) if q.metabolic_state.phase == "QUARANTINED" else None
    )

    # 3. Remove edges (except record in dissolution record)
    shard = get_shard(q.shard_id)
    edges_to_remove = list(q.edges)
    for edge in edges_to_remove:
        shard.remove_edge(q.id, edge.target_id)
        # Also remove reciprocal edges (CONTRADICTION)
        if edge.edge_type == "CONTRADICTION":
            target = get_quantum(edge.target_id)
            if target is not None:
                target.edges = [
                    e for e in target.edges
                    if not (e.target_id == q.id and e.edge_type == "CONTRADICTION")
                ]

    # 4. Clear content (retain only dissolution record and id)
    q.content = None  # Content preserved only via content_hash
    q.edges = []
    q.projections = ProjectionCache(c3=None, c4=None, c5=None)
    q.metabolic_state.phase = "DISSOLVED"
    q.metabolic_state.vitality = 0.0

    # 5. Invalidate any cached projections referencing this quantum
    invalidate_projections_referencing(q.id)

    # 6. Schedule quarantine snapshot cleanup
    if q.dissolution_record.quarantine_snapshot_hash is not None:
        schedule_snapshot_cleanup(
            q.id,
            after_epochs=QUARANTINE_SNAPSHOT_RETENTION_EPOCHS
        )
```

### 6.5 Dissolution Record Schema

The dissolution record preserves audit trail information after quantum dissolution. See Section 2.1 (`DissolutionRecord` in `$defs`) for the complete JSON Schema.

**Retention policy:**

| Component | Retention Period | Rationale |
|-----------|-----------------|-----------|
| Dissolution record metadata | Permanent | Audit trail, provenance chain integrity |
| Content hash | Permanent | Enables verification that content existed |
| Final opinion | Permanent | Historical credibility record |
| Quarantine snapshot (full serialization) | `QUARANTINE_SNAPSHOT_RETENTION_EPOCHS` (default 200) | Full reversibility window |
| Recycling details | Permanent | Provenance of evidence redistribution |

**Dissolution parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `QUARANTINE_SNAPSHOT_RETENTION_EPOCHS` | 200 | Epochs to retain full quarantine snapshot |
| `MAX_RECYCLING_RECIPIENTS` | 5 | Maximum quanta to receive recycled evidence |

---

## 7. SHREC Specification

SHREC (Stress, Hunger, Renewal, Elimination, Consolidation) is the five-signal regulatory system that governs metabolic resource allocation. It combines ecological budget competition (Lotka-Volterra) with PID safety overlay and constitutional floor guarantees.

### 7.1 Signal Definitions and Computation

Each SHREC signal measures a distinct aspect of metabolic health:

```python
class SHRECSignals:
    """Five metabolic regulation signals."""

    @staticmethod
    def compute_epistemic_hunger(state: SystemState, epoch: EpochNum) -> float:
        """Measures unmet knowledge demand — knowledge gaps and unanswered queries."""
        # Count queries that returned no results or low-relevance results
        unanswered_queries = state.query_log.count_unanswered(
            window=SIGNAL_WINDOW_EPOCHS
        )
        total_queries = state.query_log.count_total(
            window=SIGNAL_WINDOW_EPOCHS
        )
        if total_queries == 0:
            return 0.0

        # Factor in domain coverage gaps
        covered_domains = state.coherence_graph.count_covered_domains()
        known_domains = state.domain_registry.count_all()
        coverage_ratio = covered_domains / max(1, known_domains)

        hunger = (
            (unanswered_queries / total_queries) * 0.6
            + (1.0 - coverage_ratio) * 0.4
        )
        return clamp(hunger, 0.0, 1.0)

    @staticmethod
    def compute_consolidation_pressure(state: SystemState, epoch: EpochNum) -> float:
        """Measures cross-domain synthesis opportunity — potential for dreaming."""
        # Count consolidation candidates available
        candidates = count_consolidation_candidates(state.coherence_graph)
        # Weight by time since last successful consolidation
        epochs_since_consolidation = epoch - state.last_successful_consolidation_epoch
        staleness_factor = min(1.0, epochs_since_consolidation / CONSOLIDATION_STALENESS_WINDOW)

        # Factor in C-class validation queue length
        unvalidated_cclass = count_unvalidated_cclass(state)
        validation_pressure = min(1.0, unvalidated_cclass / MAX_CCLASS_QUEUE)

        pressure = (
            min(1.0, candidates / TARGET_CANDIDATES) * 0.5
            + staleness_factor * 0.3
            + validation_pressure * 0.2
        )
        return clamp(pressure, 0.0, 1.0)

    @staticmethod
    def compute_metabolic_stress(state: SystemState, epoch: EpochNum) -> float:
        """Measures system overload — processing backlog and resource exhaustion."""
        # Ingestion queue depth
        ingestion_backlog = state.ingestion_queue.size() / MAX_INGESTION_QUEUE
        # Circulation delivery failures
        delivery_failures = state.circulation_report.failures / max(1, state.circulation_report.attempts)
        # Edge budget utilization
        edge_utilization = state.coherence_graph.total_edges / state.coherence_graph.max_edges
        # Subscriber backpressure signals
        backpressure_ratio = state.backpressure_count / max(1, state.subscriber_count)

        stress = (
            ingestion_backlog * 0.3
            + delivery_failures * 0.25
            + max(0, edge_utilization - 0.8) * 5.0 * 0.25  # Spike above 80% utilization
            + backpressure_ratio * 0.2
        )
        return clamp(stress, 0.0, 1.0)

    @staticmethod
    def compute_immune_response(state: SystemState, epoch: EpochNum) -> float:
        """Measures knowledge integrity threats — contradictions and anomalies."""
        # Active contradictions (high-weight contradiction edges)
        active_contradictions = count_high_weight_contradictions(
            state.coherence_graph, threshold=0.5
        )
        total_active = state.coherence_graph.active_node_count
        contradiction_density = active_contradictions / max(1, total_active)

        # Recent PCVM rejections (potential adversarial activity)
        recent_rejections = state.pcvm_log.count_rejections(window=SIGNAL_WINDOW_EPOCHS)
        rejection_rate = recent_rejections / max(1, state.pcvm_log.count_submissions(window=SIGNAL_WINDOW_EPOCHS))

        # Quarantine false positive rate (autoimmune indicator)
        fp_rate = state.immune_audit.false_positive_rate

        immune = (
            contradiction_density * 0.4
            + rejection_rate * 0.35
            + fp_rate * 0.25
        )
        return clamp(immune, 0.0, 1.0)

    @staticmethod
    def compute_novelty_signal(state: SystemState, epoch: EpochNum) -> float:
        """Measures novel knowledge influx — rate of new, diverse quanta."""
        # New quanta ingested in recent window
        new_quanta = state.ingestion_log.count_new(window=SIGNAL_WINDOW_EPOCHS)
        # Domain diversity of new quanta
        new_domains = state.ingestion_log.count_new_domains(window=SIGNAL_WINDOW_EPOCHS)
        # Ratio of new vs. reinforcing quanta
        reinforcing = state.ingestion_log.count_reinforcing(window=SIGNAL_WINDOW_EPOCHS)
        novelty_ratio = new_quanta / max(1, new_quanta + reinforcing)

        novelty = (
            min(1.0, new_quanta / TARGET_INGESTION_RATE) * 0.4
            + min(1.0, new_domains / TARGET_DOMAIN_DIVERSITY) * 0.3
            + novelty_ratio * 0.3
        )
        return clamp(novelty, 0.0, 1.0)
```

**Signal computation parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SIGNAL_WINDOW_EPOCHS` | 20 | Rolling window for signal computation |
| `TARGET_CANDIDATES` | 10 | Target number of consolidation candidates |
| `CONSOLIDATION_STALENESS_WINDOW` | 50 | Epochs before consolidation staleness saturates |
| `MAX_INGESTION_QUEUE` | 1000 | Ingestion queue size at which stress = max |
| `TARGET_INGESTION_RATE` | 50 | Target new quanta per window |
| `TARGET_DOMAIN_DIVERSITY` | 10 | Target new domains per window |
| `MAX_CCLASS_QUEUE` | 20 | C-class validation queue size at which pressure = max |

### 7.2 Budget Computation

The total metabolic budget is derived from measured system throughput:

```python
def compute_total_budget(state: SystemState, epoch: EpochNum) -> float:
    """Compute total metabolic budget for epoch.
    B(t) = measured_throughput_capacity * (1 - safety_margin)
    """
    # Measure actual throughput capacity from recent epochs
    recent_throughput = state.throughput_log.moving_average(
        window=BUDGET_MEASUREMENT_WINDOW
    )
    # Apply safety margin to avoid exceeding capacity
    budget = recent_throughput * (1.0 - BUDGET_SAFETY_MARGIN)
    # Clamp to configured bounds
    return clamp(budget, MIN_TOTAL_BUDGET, MAX_TOTAL_BUDGET)
```

**Budget parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `BUDGET_SAFETY_MARGIN` | 0.15 | Fraction of capacity reserved as safety margin |
| `BUDGET_MEASUREMENT_WINDOW` | 10 | Epochs for throughput measurement averaging |
| `MIN_TOTAL_BUDGET` | 100.0 | Minimum budget (arbitrary units) |
| `MAX_TOTAL_BUDGET` | 10000.0 | Maximum budget cap |

### 7.3 Floor Allocation

Constitutional floor allocations guarantee minimum budget for each signal, preventing competitive exclusion (INV-E7):

```python
FLOOR_ALLOCATIONS = {
    "IMMUNE":        0.15,  # 15% — highest floor, knowledge integrity is critical
    "STRESS":        0.10,  # 10% — system health monitoring
    "NOVELTY":       0.08,  # 8% — minimum new knowledge intake
    "HUNGER":        0.05,  # 5% — minimum circulation to detect gaps (revised from refined concept)
    "CONSOLIDATION": 0.05,  # 5% — minimum dreaming budget (revised: was 8%, reduced per cost analysis)
}
# Total floor: 0.43 (revised from 0.33 after immune and stress floors were raised)
# Competitive pool: 0.57

TOTAL_FLOOR = sum(FLOOR_ALLOCATIONS.values())  # 0.43
COMPETITIVE_POOL = 1.0 - TOTAL_FLOOR            # 0.57

def compute_floor_budget(total_budget: float) -> Dict[str, float]:
    """Compute floor budget allocations."""
    return {
        signal: total_budget * floor_fraction
        for signal, floor_fraction in FLOOR_ALLOCATIONS.items()
    }
```

**Floor allocation rationale:**

| Signal | Floor | Rationale |
|--------|-------|-----------|
| IMMUNE | 0.15 | Knowledge integrity is a safety-critical function. Under-allocating immune response risks accepting corrupted quanta. |
| STRESS | 0.10 | System health monitoring must always be active. Ignoring stress leads to cascading failures. |
| NOVELTY | 0.08 | Without novel knowledge intake, the system becomes stale. Minimum ensures some ingestion always occurs. |
| HUNGER | 0.05 | Minimal circulation ensures queries can be answered even under stress. |
| CONSOLIDATION | 0.05 | Dreaming is expensive (LLM inference). Floor ensures consolidation is possible but does not waste budget when unnecessary. |

### 7.4 Competitive Allocation Algorithm

The remaining budget (competitive pool) is allocated by signal intensity ratio with frequency-dependent boost:

```python
def compute_competitive_allocation(
    signals: Dict[str, float],
    total_budget: float,
    floor_budget: Dict[str, float]
) -> Dict[str, float]:
    """Allocate competitive pool by signal intensity with frequency-dependent boost."""

    competitive_pool = total_budget * COMPETITIVE_POOL

    # 1. Compute effective intensities with frequency-dependent selection
    effective_intensity = {}
    for signal_name, intensity in signals.items():
        current_allocation = floor_budget[signal_name] / total_budget
        if current_allocation < 2.0 * FLOOR_ALLOCATIONS[signal_name]:
            # Signal is near floor: boost intensity (rare species advantage)
            boost = 2.0 * FLOOR_ALLOCATIONS[signal_name] / max(0.01, current_allocation)
            effective_intensity[signal_name] = intensity * boost
        else:
            effective_intensity[signal_name] = intensity

    # 2. Normalize to get allocation ratios
    total_intensity = sum(effective_intensity.values())
    if total_intensity == 0:
        # Equal split if all signals are zero
        allocation_ratios = {s: 1.0 / len(signals) for s in signals}
    else:
        allocation_ratios = {
            s: i / total_intensity for s, i in effective_intensity.items()
        }

    # 3. Allocate competitive pool by ratio
    competitive_allocation = {
        s: competitive_pool * ratio for s, ratio in allocation_ratios.items()
    }

    # 4. Total allocation = floor + competitive
    total_allocation = {
        s: floor_budget[s] + competitive_allocation[s] for s in signals
    }

    return total_allocation
```

### 7.5 Statistical Self-Model

SHREC maintains a rolling statistical model of each signal's behavior for regime detection:

```python
class SignalStatistics:
    """Rolling statistics for a single SHREC signal."""

    def __init__(self, window: int = STATS_WINDOW_EPOCHS):
        self.window = window
        self.history: Deque[float] = deque(maxlen=window)
        self.mean: float = 0.0
        self.variance: float = 0.0
        self.sigma: float = 0.0
        # Bayesian priors for cold start
        self.prior_mean: float = 0.5
        self.prior_variance: float = 0.1
        self.prior_weight: float = BAYESIAN_PRIOR_WEIGHT

    def update(self, value: float) -> None:
        """Update rolling statistics with new observation."""
        self.history.append(value)
        n = len(self.history)

        if n < MIN_STATS_SAMPLES:
            # Insufficient data: use Bayesian prior
            effective_mean = (
                self.prior_weight * self.prior_mean + n * mean(self.history)
            ) / (self.prior_weight + n)
            effective_var = (
                self.prior_weight * self.prior_variance
                + sum((x - effective_mean)**2 for x in self.history)
            ) / (self.prior_weight + n)
        else:
            effective_mean = mean(self.history)
            effective_var = variance(self.history)

        self.mean = effective_mean
        self.variance = effective_var
        self.sigma = math.sqrt(max(0.0, effective_var))

    def z_score(self, value: float) -> float:
        """Compute z-score of value relative to rolling distribution."""
        if self.sigma < MIN_SIGMA:
            return 0.0  # Not enough variance to compute meaningful z-score
        return (value - self.mean) / self.sigma


class SHRECStatisticalModel:
    """Statistical self-model for all SHREC signals."""

    def __init__(self):
        self.signal_stats: Dict[str, SignalStatistics] = {
            name: SignalStatistics() for name in SIGNAL_NAMES
        }
        self.regime: Regime = "NORMAL"
        self.regime_history: Deque[Regime] = deque(maxlen=100)

    def update_all(self, signals: Dict[str, float]) -> None:
        """Update all signal statistics."""
        for name, value in signals.items():
            self.signal_stats[name].update(value)
```

**Statistics parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `STATS_WINDOW_EPOCHS` | 100 | Rolling window for signal statistics |
| `MIN_STATS_SAMPLES` | 10 | Minimum samples before using empirical (vs Bayesian prior) stats |
| `BAYESIAN_PRIOR_WEIGHT` | 5.0 | Effective sample count of Bayesian prior |
| `MIN_SIGMA` | 0.01 | Minimum sigma to avoid division by zero |

### 7.6 Regime Detection and Transition

SHREC operates in one of four regimes based on aggregate signal deviation:

```python
def detect_regime(model: SHRECStatisticalModel, signals: Dict[str, float]) -> Regime:
    """Detect current operating regime from signal z-scores."""

    # Compute maximum absolute z-score across all signals
    z_scores = {
        name: model.signal_stats[name].z_score(value)
        for name, value in signals.items()
    }
    max_z = max(abs(z) for z in z_scores.values())

    # Check constitutional bounds
    for name, value in signals.items():
        if is_near_constitutional_bound(name, value):
            return "CONSTITUTIONAL"

    # Regime thresholds
    if max_z > CRITICAL_Z_THRESHOLD:
        return "CRITICAL"
    elif max_z > ELEVATED_Z_THRESHOLD:
        return "ELEVATED"
    else:
        return "NORMAL"


def is_near_constitutional_bound(signal_name: str, value: float) -> bool:
    """Check if signal is near a constitutional bound."""
    # Constitutional bounds are system limits that must not be violated
    bounds = CONSTITUTIONAL_BOUNDS.get(signal_name)
    if bounds is None:
        return False
    lower, upper = bounds
    margin = CONSTITUTIONAL_MARGIN
    return value < lower + margin or value > upper - margin


# Regime thresholds
ELEVATED_Z_THRESHOLD = 1.5   # >1.5 sigma from mean
CRITICAL_Z_THRESHOLD = 2.5   # >2.5 sigma from mean
CONSTITUTIONAL_MARGIN = 0.05  # Within 5% of constitutional bound
```

**Regime behaviors:**

| Regime | PID Active | Budget Adjustment | Description |
|--------|-----------|-------------------|-------------|
| NORMAL | No | Ecological competition only | Steady-state operation, < 1.5 sigma |
| ELEVATED | Yes (clamped) | PID adjusts up to +/-10% | Moderate deviation, 1.5-2.5 sigma |
| CRITICAL | Yes (unclamped) | PID adjusts up to +/-25% | Severe deviation, > 2.5 sigma |
| CONSTITUTIONAL | Yes (emergency) | Emergency reallocation | Near system bounds, override ecology |

**Regime transition rules:**

```python
def transition_regime(
    current: Regime,
    detected: Regime,
    model: SHRECStatisticalModel,
    epoch: EpochNum
) -> Regime:
    """Apply hysteresis to regime transitions to prevent oscillation."""

    # Upward transitions (NORMAL->ELEVATED->CRITICAL->CONSTITUTIONAL): immediate
    regime_order = {"NORMAL": 0, "ELEVATED": 1, "CRITICAL": 2, "CONSTITUTIONAL": 3}

    if regime_order[detected] > regime_order[current]:
        return detected

    # Downward transitions: require sustained stability
    if regime_order[detected] < regime_order[current]:
        # Must remain at lower level for REGIME_HYSTERESIS_EPOCHS to transition down
        epochs_at_lower = count_consecutive_epochs_at_or_below(
            model.regime_history, detected
        )
        if epochs_at_lower >= REGIME_HYSTERESIS_EPOCHS:
            return detected
        return current  # Stay at current regime

    return current

REGIME_HYSTERESIS_EPOCHS = 5  # Epochs of stability required for downward transition
```

### 7.7 PID Overlay

The PID controller acts as a safety net during ELEVATED, CRITICAL, and CONSTITUTIONAL regimes:

```python
class PIDController:
    """PID controller for a single SHREC signal."""

    def __init__(self, signal_name: str):
        self.signal_name = signal_name
        self.integral: float = 0.0
        self.previous_error: float = 0.0
        self.derivative_history: Deque[float] = deque(maxlen=DERIVATIVE_WINDOW)

    def compute(
        self,
        error: float,
        sigma: float,
        regime: Regime
    ) -> float:
        """Compute PID output for signal deviation."""

        if regime == "NORMAL":
            return 0.0  # PID inactive in NORMAL regime

        # Sigma-derived gains per refined concept
        if sigma < MIN_SIGMA:
            sigma = MIN_SIGMA

        Kp = 1.0 / sigma
        Ki = Kp / (4.0 * STATS_WINDOW_EPOCHS)
        Kd = Kp * (STATS_WINDOW_EPOCHS / 10.0)

        # Proportional term
        p_term = Kp * error

        # Integral term with anti-windup
        self.integral += error
        self.integral = clamp(self.integral, -INTEGRAL_CLAMP, INTEGRAL_CLAMP)
        i_term = Ki * self.integral

        # Derivative term with smoothing
        derivative = error - self.previous_error
        self.derivative_history.append(derivative)
        smoothed_derivative = mean(self.derivative_history)
        d_term = Kd * smoothed_derivative

        self.previous_error = error

        # Total PID output
        pid_output = p_term + i_term + d_term

        # Clamp based on regime
        if regime == "ELEVATED":
            pid_output = clamp(pid_output, -PID_CLAMP_ELEVATED, PID_CLAMP_ELEVATED)
        elif regime == "CRITICAL":
            pid_output = clamp(pid_output, -PID_CLAMP_CRITICAL, PID_CLAMP_CRITICAL)
        elif regime == "CONSTITUTIONAL":
            # No clamping in constitutional regime
            pass

        return pid_output

    def reset_integral(self) -> None:
        """Reset integral term (called on regime change-point)."""
        self.integral = 0.0
```

**Anti-windup with CUSUM change-point detection:**

```python
def detect_changepoint_cusum(
    signal_history: Deque[float],
    threshold: float = CUSUM_THRESHOLD
) -> bool:
    """Detect change-point using CUSUM algorithm."""
    if len(signal_history) < 2:
        return False

    mu = mean(list(signal_history)[:-1])  # Mean excluding latest
    latest = signal_history[-1]

    # Accumulate positive and negative deviations
    S_pos = max(0, latest - mu - CUSUM_SLACK)
    S_neg = max(0, mu - latest - CUSUM_SLACK)

    return S_pos > threshold or S_neg > threshold


def apply_pid_with_antiwindup(
    pid: PIDController,
    error: float,
    sigma: float,
    regime: Regime,
    signal_history: Deque[float]
) -> float:
    """Apply PID with anti-windup reset on change-points."""
    if detect_changepoint_cusum(signal_history):
        pid.reset_integral()
    return pid.compute(error, sigma, regime)
```

**Derivative monitor:** If the derivative term exceeds `DERIVATIVE_ALARM_THRESHOLD` for more than `DERIVATIVE_ALARM_EPOCHS` consecutive epochs, SHREC logs a stability warning and increases PID damping (Kd *= 2.0).

**PID parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `PID_CLAMP_ELEVATED` | 0.10 | Max PID adjustment in ELEVATED regime (10% of budget) |
| `PID_CLAMP_CRITICAL` | 0.25 | Max PID adjustment in CRITICAL regime (25% of budget) |
| `INTEGRAL_CLAMP` | 0.20 | Anti-windup integral clamp |
| `DERIVATIVE_WINDOW` | 5 | Epochs for derivative smoothing |
| `CUSUM_THRESHOLD` | 2.0 | CUSUM change-point detection threshold |
| `CUSUM_SLACK` | 0.5 | CUSUM slack parameter |
| `DERIVATIVE_ALARM_THRESHOLD` | 0.5 | Derivative magnitude triggering stability alarm |
| `DERIVATIVE_ALARM_EPOCHS` | 3 | Consecutive epochs before derivative alarm fires |

### 7.8 Immune Self-Audit Protocol

Periodic audit that checks whether catabolism is attacking valid knowledge (autoimmune pathology):

```python
def execute_immune_self_audit(
    state: SystemState,
    epoch: EpochNum
) -> ImmuneAuditResult:
    """Execute immune self-audit every IMMUNE_AUDIT_INTERVAL epochs."""

    if epoch % IMMUNE_AUDIT_INTERVAL != 0:
        return None

    # 1. Sample recently quarantined quanta
    recently_quarantined = state.get_quarantined_quanta(
        window=IMMUNE_AUDIT_WINDOW
    )
    sample_size = max(1, int(len(recently_quarantined) * IMMUNE_AUDIT_SAMPLE_RATE))
    sample = random_sample(recently_quarantined, sample_size)

    # 2. Check each sampled quantum for active support
    false_positives = 0
    for q in sample:
        active_support_edges = [
            e for e in get_edges_pointing_to(q.id)
            if e.edge_type == "SUPPORT"
            and e.weight > 0.3
            and get_quantum(e.target_id) is not None  # edge stored on source
            and get_quantum_by_edge_source(e).metabolic_state.phase == "ACTIVE"
        ]
        if len(active_support_edges) >= IMMUNE_AUDIT_SUPPORT_THRESHOLD:
            false_positives += 1

    false_positive_rate = false_positives / max(1, sample_size)

    # 3. Evaluate autoimmune condition
    result = ImmuneAuditResult(
        epoch=epoch,
        sample_size=sample_size,
        false_positives=false_positives,
        false_positive_rate=false_positive_rate,
        autoimmune_alarm=false_positive_rate > AUTOIMMUNE_ALARM_THRESHOLD
    )

    # 4. If alarm: increase catabolism thresholds
    if result.autoimmune_alarm:
        state.catabolism_threshold_multiplier = AUTOIMMUNE_THRESHOLD_BOOST
        state.autoimmune_recovery_epoch = epoch + AUTOIMMUNE_RECOVERY_EPOCHS
        log_autoimmune_alarm(result)

    # 5. If past recovery: reset thresholds
    if hasattr(state, 'autoimmune_recovery_epoch'):
        if epoch >= state.autoimmune_recovery_epoch:
            state.catabolism_threshold_multiplier = 1.0

    return result
```

**Immune audit parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `IMMUNE_AUDIT_INTERVAL` | 50 | Epochs between immune self-audits |
| `IMMUNE_AUDIT_WINDOW` | 50 | Window of recent quarantines to sample from |
| `IMMUNE_AUDIT_SAMPLE_RATE` | 0.10 | Fraction of quarantined quanta to sample |
| `IMMUNE_AUDIT_SUPPORT_THRESHOLD` | 2 | Active support edges indicating false positive |
| `AUTOIMMUNE_ALARM_THRESHOLD` | 0.20 | False positive rate triggering alarm |
| `AUTOIMMUNE_THRESHOLD_BOOST` | 2.0 | Catabolism threshold multiplier during alarm |
| `AUTOIMMUNE_RECOVERY_EPOCHS` | 10 | Duration of threshold boost |

### 7.9 Lotka-Volterra Stability Formulation

The competitive dynamics of SHREC signals are modeled using generalized Lotka-Volterra equations:

**Continuous-time model (theoretical basis):**

```
dS_i/dt = r_i * S_i * (1 - sum_j(alpha_ij * S_j / K_i)) + floor_correction_i
```

Where:
- `S_i` = budget share of signal i
- `r_i` = intrinsic growth rate of signal i (measured from signal dynamics)
- `K_i` = carrying capacity of signal i (maximum useful budget share)
- `alpha_ij` = competitive effect of signal j on signal i
- `alpha_ii` = 1 (intra-signal self-limitation)
- `floor_correction_i = max(0, floor_i - S_i) * restoration_rate`

**Discrete-time implementation (per epoch):**

```python
def lotka_volterra_step(
    current_shares: Dict[str, float],
    signals: Dict[str, float],
    params: LVParams
) -> Dict[str, float]:
    """Execute one Lotka-Volterra step for budget share evolution."""

    new_shares = {}
    for i, signal_name in enumerate(SIGNAL_NAMES):
        S_i = current_shares[signal_name]
        r_i = params.growth_rates[signal_name]
        K_i = params.carrying_capacities[signal_name]

        # Competition sum
        competition = sum(
            params.alpha[signal_name][other] * current_shares[other] / K_i
            for other in SIGNAL_NAMES
        )

        # Lotka-Volterra dynamics
        dS = r_i * S_i * (1.0 - competition)

        # Floor correction
        floor = FLOOR_ALLOCATIONS[signal_name]
        if S_i < floor:
            dS += (floor - S_i) * FLOOR_RESTORATION_RATE

        # Apply signal intensity as growth rate modifier
        intensity_modifier = signals[signal_name]
        dS *= intensity_modifier

        new_shares[signal_name] = max(0.0, S_i + dS * DT)

    # Normalize to sum to 1.0
    total = sum(new_shares.values())
    if total > 0:
        new_shares = {s: v / total for s, v in new_shares.items()}

    return new_shares
```

**Coexistence conditions:**

For stable coexistence of all 5 signals, the following conditions MUST hold:

1. **Weak inter-specific competition:** `alpha_ij * alpha_ji < 1` for all pairs (i, j) where i != j
2. **Niche differentiation:** Each signal has a primary resource where it is the dominant consumer
3. **Floor guarantees:** Floor allocations provide absolute minimum regardless of competition

**Default competitive coefficients (alpha matrix):**

```
         HUNGER  CONSOL  STRESS  IMMUNE  NOVELTY
HUNGER    1.0     0.2     0.3     0.1     0.2
CONSOL    0.2     1.0     0.1     0.2     0.3
STRESS    0.3     0.1     1.0     0.2     0.1
IMMUNE    0.1     0.2     0.2     1.0     0.1
NOVELTY   0.2     0.3     0.1     0.1     1.0
```

All off-diagonal products `alpha_ij * alpha_ji` are in range [0.01, 0.09], well below 1.0, satisfying the coexistence condition.

**Stability analysis (per refined concept):**

The Jacobian at the interior equilibrium S*:

```
J_ij = -r_i * S_i* * alpha_ij / K_i    (for i != j)
J_ii = -r_i * S_i* / K_i                (diagonal)
```

For the default alpha matrix with weak inter-specific competition, the eigenvalues are approximately `-r_i * S_i* / K_i` (all negative), confirming local asymptotic stability.

The Lyapunov function:

```
V = sum_i (S_i - S_i* - S_i* * ln(S_i / S_i*))
```

`dV/dt < 0` when `alpha_ij < K_i / K_j` for all i, j. With the default parameters, this condition holds since all alpha_ij are 0.1-0.3 and K_i/K_j ratios are near 1.0.

**Lotka-Volterra parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DT` | 0.1 | Discrete time step for LV dynamics |
| `FLOOR_RESTORATION_RATE` | 2.0 | Rate at which floor corrections restore minimum allocation |
| Default `r_i` | 1.0 for all signals | Intrinsic growth rates (adjusted by signal measurement) |
| Default `K_i` | 0.4 for all signals | Carrying capacities (no signal should exceed 40% of budget) |

### 7.10 SHREC Epoch Orchestrator

The complete SHREC regulation cycle for each epoch:

```python
def execute_shrec_regulation(
    state: SystemState,
    epoch: EpochNum
) -> SHRECResult:
    """Execute SHREC regulation phase for current epoch."""

    # 1. Compute all signals
    signals = {
        "HUNGER": SHRECSignals.compute_epistemic_hunger(state, epoch),
        "CONSOLIDATION": SHRECSignals.compute_consolidation_pressure(state, epoch),
        "STRESS": SHRECSignals.compute_metabolic_stress(state, epoch),
        "IMMUNE": SHRECSignals.compute_immune_response(state, epoch),
        "NOVELTY": SHRECSignals.compute_novelty_signal(state, epoch),
    }

    # 2. Update statistical model
    state.shrec_model.update_all(signals)

    # 3. Detect regime
    new_regime = detect_regime(state.shrec_model, signals)
    state.shrec_model.regime = transition_regime(
        state.shrec_model.regime, new_regime, state.shrec_model, epoch
    )

    # 4. Compute total budget
    total_budget = compute_total_budget(state, epoch)

    # 5. Compute floor allocations
    floor_budget = compute_floor_budget(total_budget)

    # 6. Lotka-Volterra competitive allocation
    lv_shares = lotka_volterra_step(
        state.shrec_shares, signals, state.lv_params
    )

    # 7. Apply competitive allocation to budget
    allocations = {
        s: total_budget * lv_shares[s] for s in SIGNAL_NAMES
    }

    # 8. Enforce floors
    for s in SIGNAL_NAMES:
        allocations[s] = max(allocations[s], floor_budget[s])

    # 9. Apply PID overlay if not NORMAL regime
    if state.shrec_model.regime != "NORMAL":
        for s in SIGNAL_NAMES:
            error = signals[s] - state.shrec_model.signal_stats[s].mean
            pid_adjustment = apply_pid_with_antiwindup(
                state.pid_controllers[s],
                error,
                state.shrec_model.signal_stats[s].sigma,
                state.shrec_model.regime,
                state.shrec_model.signal_stats[s].history
            )
            allocations[s] += total_budget * pid_adjustment
            allocations[s] = max(allocations[s], floor_budget[s])  # Re-enforce floor

    # 10. Normalize to total budget
    total_allocated = sum(allocations.values())
    if total_allocated > total_budget:
        scale = total_budget / total_allocated
        allocations = {s: v * scale for s, v in allocations.items()}
        # Re-enforce floors after scaling
        for s in SIGNAL_NAMES:
            allocations[s] = max(allocations[s], floor_budget[s])

    # 11. Update state
    state.shrec_shares = {s: allocations[s] / total_budget for s in SIGNAL_NAMES}
    state.shrec_allocations = allocations

    # 12. Execute immune self-audit if scheduled
    audit_result = execute_immune_self_audit(state, epoch)

    return SHRECResult(
        epoch=epoch,
        signals=signals,
        regime=state.shrec_model.regime,
        total_budget=total_budget,
        allocations=allocations,
        audit_result=audit_result
    )
```

---

## 8. Projection Engine Specification

The projection engine translates canonical epistemic quanta into subsystem-native representations and reconstructs updates from subsystem projections back to canonical form.

### 8.1 C3 Projection (Tidal Noosphere)

**Forward projection (EMA -> C3):**

```python
def project_to_c3(q: EpistemicQuantum) -> C3Projection:
    """Project epistemic quantum to C3 Tidal Noosphere native format."""

    # Preserved fields
    projection = C3Projection()
    projection.claim_text = q.content.claim_text                    # Full preservation
    projection.parcel_tags = map_domain_tags_to_parcels(            # Mapped
        q.content.domain_tags
    )
    projection.relevance_score = (                                  # Collapsed from SL
        q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty
    )
    projection.generating_agent = q.provenance.generating_agent     # Direct map
    projection.epoch = q.provenance.generation_epoch                # Direct map

    # Edges: map to parcel-local graph
    projection.local_edges = []
    for edge in q.edges:
        if edge.edge_type in ("SUPPORT", "CONTRADICTION"):
            target_parcel = resolve_quantum_to_parcel(edge.target_id)
            if target_parcel in projection.parcel_tags:
                projection.local_edges.append(C3Edge(
                    target=edge.target_id,
                    type=edge.edge_type.lower(),
                    weight=edge.weight
                ))

    # Lost fields (acknowledged)
    # - Full Subjective Logic opinion (collapsed to scalar)
    # - Uncertainty quantification
    # - Evidence array details (reduced to count)
    # - Metabolic state
    # - Analogy and derivation edges outside parcel scope
    projection.evidence_count = len(q.content.evidence)
    projection.source_quantum_id = q.id  # Back-reference for inverse projection

    return projection
```

**Inverse projection (C3 -> EMA update):**

```python
def reconstruct_from_c3(
    c3_update: C3ProjectionUpdate,
    canonical: EpistemicQuantum
) -> QuantumUpdate:
    """Reconstruct canonical quantum update from C3 projection update."""

    update = QuantumUpdate()

    # Claim text updates: direct (if C3 modified text)
    if c3_update.claim_text != canonical.content.claim_text:
        update.content_text = c3_update.claim_text

    # Relevance score -> opinion: cannot recover full SL from scalar
    # Use heuristic reconstruction
    if c3_update.relevance_score != (canonical.opinion.belief + canonical.opinion.base_rate * canonical.opinion.uncertainty):
        new_expected = c3_update.relevance_score
        # Preserve original uncertainty proportion
        original_expected = canonical.opinion.belief + canonical.opinion.base_rate * canonical.opinion.uncertainty
        if original_expected > 0:
            scale = new_expected / original_expected
            update.opinion = SubjectiveLogicOpinion(
                belief=clamp(canonical.opinion.belief * scale, 0, 1),
                disbelief=clamp(canonical.opinion.disbelief * (2 - scale), 0, 1),
                uncertainty=canonical.opinion.uncertainty,  # Preserved (not in C3)
                base_rate=canonical.opinion.base_rate       # Preserved
            )
            normalize_opinion(update.opinion)

    # Edge updates from C3 local graph
    for c3_edge in c3_update.edge_updates:
        update.edge_updates.append(EdgeUpdate(
            target_id=c3_edge.target,
            edge_type=c3_edge.type.upper(),
            new_weight=c3_edge.weight
        ))

    # Information loss acknowledgment
    update.reconstruction_fidelity = compute_c3_fidelity(c3_update, canonical)
    update.lost_fields = [
        "full_subjective_logic_opinion",
        "uncertainty_quantification",
        "evidence_details",
        "metabolic_state",
        "non_local_edges"
    ]

    return update
```

**C3 fidelity metric:**

```python
def compute_c3_fidelity(c3_data: C3Projection, canonical: EpistemicQuantum) -> float:
    """Compute round-trip fidelity for C3 projection."""

    # 1. Semantic similarity of claim content (weight 0.5)
    reconstructed_text = c3_data.claim_text
    original_text = canonical.content.claim_text
    text_sim = cosine_similarity(
        compute_embedding(reconstructed_text),
        compute_embedding(original_text)
    )

    # 2. Opinion Wasserstein distance (weight 0.3)
    original_expected = canonical.opinion.belief + canonical.opinion.base_rate * canonical.opinion.uncertainty
    projected_expected = c3_data.relevance_score
    opinion_distance = abs(original_expected - projected_expected)
    opinion_preservation = 1.0 - opinion_distance  # Scalar-only, no uncertainty recovery

    # 3. Edge graph edit distance (weight 0.2)
    original_local_edges = set(
        (e.target_id, e.edge_type)
        for e in canonical.edges
        if e.edge_type in ("SUPPORT", "CONTRADICTION")
    )
    projected_edges = set(
        (e.target, e.type.upper())
        for e in c3_data.local_edges
    )
    if len(original_local_edges) == 0 and len(projected_edges) == 0:
        edge_fidelity = 1.0
    else:
        intersection = original_local_edges.intersection(projected_edges)
        union = original_local_edges.union(projected_edges)
        edge_fidelity = len(intersection) / max(1, len(union))

    # Composite fidelity
    fidelity = text_sim * 0.5 + opinion_preservation * 0.3 + edge_fidelity * 0.2
    return clamp(fidelity, 0.0, 1.0)
```

**C3 target fidelity:** 0.85

### 8.2 C4 Projection (ASV/AASL)

**Forward projection (EMA -> C4):**

```python
def project_to_c4(q: EpistemicQuantum) -> C4Projection:
    """Project epistemic quantum to C4 ASV/AASL native format."""

    projection = C4Projection()

    # Preserved fields
    projection.content = q.content.claim_text                        # Full preservation
    projection.message_type = map_claim_class_to_aasl_type(q.claim_class)  # Mapped
    projection.topic_ontology = map_domain_tags_to_aasl_topics(      # Mapped
        q.content.domain_tags
    )
    projection.sender_agent_id = q.provenance.generating_agent       # Direct map

    # AASL supports full Subjective Logic confidence
    projection.confidence = AASLConfidence(
        belief=q.opinion.belief,
        disbelief=q.opinion.disbelief,
        uncertainty=q.opinion.uncertainty,
        base_rate=q.opinion.base_rate
    )

    # Evidence references (flattened from structured array)
    projection.evidence_references = [
        AASLEvidenceRef(
            ref_id=ev.source_quantum_id or ev.external_reference,
            type=ev.evidence_type,
            weight=ev.weight
        )
        for ev in q.content.evidence
    ]

    # Lost fields
    # - Coherence edges (AASL is message-oriented)
    # - Metabolic state
    # - Vitality score
    projection.source_quantum_id = q.id

    return projection
```

**Inverse projection (C4 -> EMA update):**

```python
def reconstruct_from_c4(
    c4_update: C4ProjectionUpdate,
    canonical: EpistemicQuantum
) -> QuantumUpdate:
    """Reconstruct canonical quantum update from C4 projection update."""

    update = QuantumUpdate()

    if c4_update.content != canonical.content.claim_text:
        update.content_text = c4_update.content

    # Full opinion recovery (AASL preserves SL)
    if c4_update.confidence is not None:
        update.opinion = SubjectiveLogicOpinion(
            belief=c4_update.confidence.belief,
            disbelief=c4_update.confidence.disbelief,
            uncertainty=c4_update.confidence.uncertainty,
            base_rate=c4_update.confidence.base_rate
        )

    update.reconstruction_fidelity = compute_c4_fidelity(c4_update, canonical)
    update.lost_fields = ["coherence_edges", "metabolic_state", "vitality"]

    return update
```

**C4 fidelity metric:**

```python
def compute_c4_fidelity(c4_data: C4Projection, canonical: EpistemicQuantum) -> float:
    """Compute round-trip fidelity for C4 projection."""

    # 1. Semantic content similarity (weight 0.4)
    text_sim = cosine_similarity(
        compute_embedding(c4_data.content),
        compute_embedding(canonical.content.claim_text)
    )

    # 2. Opinion preservation (weight 0.4) — full SL preserved
    opinion_distance = wasserstein_distance_sl(
        c4_data.confidence, canonical.opinion
    )
    opinion_preservation = 1.0 - opinion_distance

    # 3. Claim type preservation (weight 0.2)
    original_class = canonical.claim_class
    projected_class = reverse_map_aasl_to_claim_class(c4_data.message_type)
    if original_class == projected_class:
        type_fidelity = 1.0
    elif is_compatible_class(original_class, projected_class):
        type_fidelity = 0.8
    else:
        type_fidelity = 0.0

    fidelity = text_sim * 0.4 + opinion_preservation * 0.4 + type_fidelity * 0.2
    return clamp(fidelity, 0.0, 1.0)


def wasserstein_distance_sl(a: SubjectiveLogicOpinion, b: SubjectiveLogicOpinion) -> float:
    """Compute Wasserstein distance between two Subjective Logic opinions."""
    return (
        abs(a.belief - b.belief)
        + abs(a.disbelief - b.disbelief)
        + abs(a.uncertainty - b.uncertainty)
    ) / 2.0  # Normalized to [0, 1]
```

**C4 target fidelity:** 0.88

### 8.3 C5 Projection (PCVM)

**Forward projection (EMA -> C5):**

```python
def project_to_c5(q: EpistemicQuantum) -> C5Projection:
    """Project epistemic quantum to C5 PCVM native format (Claim + VTD stub)."""

    projection = C5Projection()

    # Preserved fields (highest fidelity projection)
    projection.claim_text = q.content.claim_text                    # Full
    projection.claim_class = q.claim_class                          # Full
    projection.opinion = copy(q.opinion)                            # Full SL preserved
    projection.provenance = copy(q.provenance)                      # Full PROV chain
    projection.evidence = copy(q.content.evidence)                  # Full array

    # Support and contradiction edges (mapped to VTD coherence check)
    projection.coherence_edges = [
        C5CoherenceEdge(
            target_claim=resolve_quantum_to_claim(e.target_id),
            relationship=map_edge_to_vtd_relationship(e.edge_type),
            weight=e.weight
        )
        for e in q.edges
        if e.edge_type in ("SUPPORT", "CONTRADICTION", "DERIVATION")
    ]

    # Lost fields
    # - Analogy edges
    # - Vitality and circulation metadata
    # - Metabolic phase
    projection.source_quantum_id = q.id

    return projection
```

**Inverse projection (C5 -> EMA update):**

```python
def reconstruct_from_c5(
    c5_update: C5ProjectionUpdate,
    canonical: EpistemicQuantum
) -> QuantumUpdate:
    """Reconstruct canonical quantum update from C5 projection update.
    C5 is the highest-fidelity projection; most fields recover fully.
    """

    update = QuantumUpdate()

    if c5_update.claim_text != canonical.content.claim_text:
        update.content_text = c5_update.claim_text

    # Full opinion recovery
    if c5_update.opinion is not None:
        update.opinion = c5_update.opinion

    # Full provenance recovery
    if c5_update.provenance is not None:
        update.provenance = c5_update.provenance

    # Edge updates from coherence check
    for c5_edge in c5_update.coherence_updates:
        update.edge_updates.append(EdgeUpdate(
            target_id=resolve_claim_to_quantum(c5_edge.target_claim),
            edge_type=reverse_map_vtd_to_edge_type(c5_edge.relationship),
            new_weight=c5_edge.weight
        ))

    update.reconstruction_fidelity = compute_c5_fidelity(c5_update, canonical)
    update.lost_fields = ["analogy_edges", "vitality", "metabolic_phase"]

    return update
```

**C5 fidelity metric:**

```python
def compute_c5_fidelity(c5_data: C5Projection, canonical: EpistemicQuantum) -> float:
    """Compute round-trip fidelity for C5 projection."""

    # 1. Claim content exact match (weight 0.3)
    text_match = 1.0 if c5_data.claim_text == canonical.content.claim_text else (
        cosine_similarity(
            compute_embedding(c5_data.claim_text),
            compute_embedding(canonical.content.claim_text)
        )
    )

    # 2. Opinion Wasserstein distance (weight 0.3) — full SL
    opinion_dist = wasserstein_distance_sl(c5_data.opinion, canonical.opinion)
    opinion_preservation = 1.0 - opinion_dist

    # 3. Provenance chain completeness — Jaccard (weight 0.2)
    original_sources = set(canonical.provenance.derived_from)
    projected_sources = set(c5_data.provenance.derived_from) if c5_data.provenance else set()
    if len(original_sources) == 0 and len(projected_sources) == 0:
        prov_fidelity = 1.0
    else:
        intersection = original_sources.intersection(projected_sources)
        union = original_sources.union(projected_sources)
        prov_fidelity = len(intersection) / max(1, len(union))

    # 4. Evidence coverage — recall (weight 0.2)
    original_evidence = set(
        ev.source_quantum_id or ev.external_reference
        for ev in canonical.content.evidence
    )
    projected_evidence = set(
        ev.source_quantum_id or ev.external_reference
        for ev in c5_data.evidence
    )
    if len(original_evidence) == 0:
        evidence_recall = 1.0
    else:
        evidence_recall = len(
            original_evidence.intersection(projected_evidence)
        ) / len(original_evidence)

    fidelity = text_match * 0.3 + opinion_preservation * 0.3 + prov_fidelity * 0.2 + evidence_recall * 0.2
    return clamp(fidelity, 0.0, 1.0)
```

**C5 target fidelity:** 0.92

### 8.4 Fidelity Monitoring

The projection engine continuously monitors round-trip fidelity for each subsystem:

```python
class FidelityMonitor:
    """Monitors projection fidelity across all subsystems."""

    def __init__(self):
        self.fidelity_history: Dict[str, Deque[float]] = {
            "C3": deque(maxlen=FIDELITY_WINDOW),
            "C4": deque(maxlen=FIDELITY_WINDOW),
            "C5": deque(maxlen=FIDELITY_WINDOW),
        }
        self.targets = {
            "C3": C3_FIDELITY_TARGET,
            "C4": C4_FIDELITY_TARGET,
            "C5": C5_FIDELITY_TARGET,
        }

    def record_fidelity(self, target: str, score: float) -> None:
        self.fidelity_history[target].append(score)

    def check_fidelity(self, target: str) -> FidelityStatus:
        history = self.fidelity_history[target]
        if len(history) < MIN_FIDELITY_SAMPLES:
            return FidelityStatus(healthy=True, reason="insufficient_data")

        avg_fidelity = mean(history)
        target_fidelity = self.targets[target]

        if avg_fidelity < target_fidelity - FIDELITY_TOLERANCE:
            return FidelityStatus(
                healthy=False,
                avg_fidelity=avg_fidelity,
                target=target_fidelity,
                reason=f"Average fidelity {avg_fidelity:.3f} below target {target_fidelity:.3f}"
            )
        return FidelityStatus(healthy=True, avg_fidelity=avg_fidelity)
```

**Fidelity parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `C3_FIDELITY_TARGET` | 0.85 | C3 round-trip fidelity target |
| `C4_FIDELITY_TARGET` | 0.88 | C4 round-trip fidelity target |
| `C5_FIDELITY_TARGET` | 0.92 | C5 round-trip fidelity target |
| `FIDELITY_TOLERANCE` | 0.05 | Tolerance below target before alarm |
| `FIDELITY_WINDOW` | 100 | Rolling window for fidelity measurement |
| `MIN_FIDELITY_SAMPLES` | 20 | Minimum samples before fidelity evaluation |

### 8.5 Cache Invalidation Protocol

Projection caches are invalidated when the canonical quantum changes:

```python
def invalidate_projection_cache(q: EpistemicQuantum, changed_fields: Set[str]) -> None:
    """Invalidate cached projections when canonical quantum is updated."""

    # Determine which projections are affected
    field_to_projection = {
        "content": {"C3", "C4", "C5"},
        "opinion": {"C3", "C4", "C5"},
        "edges": {"C3", "C5"},
        "provenance": {"C5"},
        "claim_class": {"C4", "C5"},
    }

    affected = set()
    for field in changed_fields:
        affected.update(field_to_projection.get(field, set()))

    # Mark affected projections as stale
    for target in affected:
        cache = getattr(q.projections, target.lower())
        if cache is not None:
            cache.stale = True

    # If any projection is stale and subscriber has strong consistency requirement,
    # re-project immediately
    for target in affected:
        if has_strong_consistency_subscribers(q.id, target):
            new_projection = project_quantum(q, target)
            setattr(q.projections, target.lower(), new_projection)
```

**Consistency model (per RA-4):**

| Consistency Level | Scope | Behavior |
|-------------------|-------|----------|
| Eventual (default) | All standard quanta | Stale projection refreshed within 1 epoch |
| Epoch-boundary | Quanta with `claim_class in ("C", "N")` | Projection refreshed at epoch boundary |
| Strong | Safety-critical quanta (governance, constitutional) | Projection refreshed immediately on canonical update |

---

## 9. Retrieval Interface

### 9.1 Query Types

EMA supports four query types for knowledge retrieval:

```json
{
  "$id": "https://ema.atrahasis.dev/schema/v1/query.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EMA Query",
  "type": "object",
  "required": ["query_id", "query_type", "requester"],
  "properties": {
    "query_id": {
      "type": "string",
      "description": "Unique query identifier."
    },
    "query_type": {
      "type": "string",
      "enum": ["semantic", "structural", "temporal", "metabolic_state"],
      "description": "Type of retrieval query."
    },
    "requester": {
      "type": "string",
      "description": "AgentId or subsystem requesting retrieval."
    },
    "semantic_params": {
      "type": "object",
      "properties": {
        "query_text": { "type": "string", "maxLength": 4096 },
        "domain_tags": { "type": "array", "items": { "type": "string" } },
        "min_credibility": { "type": "number", "minimum": 0, "maximum": 1 },
        "claim_classes": { "type": "array", "items": { "type": "string" } }
      },
      "description": "Parameters for semantic queries."
    },
    "structural_params": {
      "type": "object",
      "properties": {
        "root_quantum_id": { "type": "string" },
        "edge_types": { "type": "array", "items": { "type": "string" } },
        "max_depth": { "type": "integer", "minimum": 1, "maximum": 10, "default": 3 },
        "direction": { "type": "string", "enum": ["outgoing", "incoming", "both"], "default": "both" }
      },
      "description": "Parameters for graph-structural queries."
    },
    "temporal_params": {
      "type": "object",
      "properties": {
        "epoch_range": {
          "type": "object",
          "properties": {
            "start": { "type": "integer" },
            "end": { "type": "integer" }
          }
        },
        "created_after": { "type": "string", "format": "date-time" },
        "created_before": { "type": "string", "format": "date-time" },
        "modified_after": { "type": "string", "format": "date-time" }
      },
      "description": "Parameters for temporal queries."
    },
    "metabolic_params": {
      "type": "object",
      "properties": {
        "phases": {
          "type": "array",
          "items": { "type": "string", "enum": ["ACTIVE", "CONSOLIDATING", "DECAYING", "QUARANTINED", "DISSOLVED"] }
        },
        "vitality_range": {
          "type": "object",
          "properties": {
            "min": { "type": "number" },
            "max": { "type": "number" }
          }
        },
        "min_citation_count": { "type": "integer" }
      },
      "description": "Parameters for metabolic-state queries."
    },
    "limit": { "type": "integer", "minimum": 1, "maximum": 1000, "default": 50 },
    "offset": { "type": "integer", "minimum": 0, "default": 0 },
    "projection_target": {
      "type": ["string", "null"],
      "enum": ["C3", "C4", "C5", null],
      "description": "If set, return results in projected form."
    },
    "include_dissolution_records": {
      "type": "boolean", "default": false,
      "description": "Include dissolved quanta (dissolution records only)."
    }
  }
}
```

### 9.2 Relevance Ranking Algorithm

Query results are ranked by a composite relevance score:

```python
def rank_query_results(
    query: EMAQuery,
    candidates: List[EpistemicQuantum]
) -> List[Tuple[EpistemicQuantum, float]]:
    """Rank query candidates by composite relevance score."""

    scored = []
    for q in candidates:
        # 1. Semantic relevance (for semantic queries)
        if query.query_type == "semantic" and query.semantic_params:
            q_embedding = compute_embedding(q.content.claim_text)
            query_embedding = compute_embedding(query.semantic_params.query_text)
            semantic_score = cosine_similarity(q_embedding, query_embedding)
        else:
            semantic_score = 1.0  # Non-semantic queries: all pass

        # 2. Credibility score
        credibility = q.opinion.belief + q.opinion.base_rate * q.opinion.uncertainty

        # 3. Vitality score
        vitality = q.metabolic_state.vitality

        # 4. Recency score (exponential decay from current epoch)
        age = current_epoch() - q.provenance.generation_epoch
        recency = math.exp(-RECENCY_DECAY_RATE * age)

        # 5. Citation importance
        citation_importance = math.log1p(q.citation_count) / math.log1p(CITATION_NORMALIZATION)

        # Composite relevance
        relevance = (
            semantic_score * SEMANTIC_WEIGHT
            + credibility * CREDIBILITY_WEIGHT
            + vitality * VITALITY_WEIGHT
            + recency * RECENCY_WEIGHT
            + citation_importance * CITATION_WEIGHT
        )

        scored.append((q, relevance))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
```

**Ranking weights:**

| Weight | Default | Description |
|--------|---------|-------------|
| `SEMANTIC_WEIGHT` | 0.40 | Weight for semantic relevance |
| `CREDIBILITY_WEIGHT` | 0.25 | Weight for opinion credibility |
| `VITALITY_WEIGHT` | 0.15 | Weight for metabolic vitality |
| `RECENCY_WEIGHT` | 0.10 | Weight for temporal recency |
| `CITATION_WEIGHT` | 0.10 | Weight for citation importance |
| `RECENCY_DECAY_RATE` | 0.01 | Exponential decay rate for recency scoring |
| `CITATION_NORMALIZATION` | 50 | Citation count at which importance saturates |

### 9.3 Context-Aware Retrieval

Queries can include context from the requester's current task to improve relevance:

```python
def context_aware_retrieval(
    query: EMAQuery,
    context: RequesterContext
) -> List[EpistemicQuantum]:
    """Retrieve quanta with context-aware relevance boosting."""

    # Standard retrieval
    candidates = execute_query(query)

    # Context boost: quanta connected to requester's recent interactions
    if context.recent_quantum_ids:
        context_neighbors = find_graph_neighbors(
            context.recent_quantum_ids,
            max_depth=2,
            edge_types=["SUPPORT", "DERIVATION", "ANALOGY"]
        )
        for q, score in candidates:
            if q.id in context_neighbors:
                # Boost score for contextually related quanta
                score *= (1.0 + CONTEXT_BOOST_FACTOR)

    # Re-rank after context boost
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [q for q, _ in candidates[:query.limit]]
```

### 9.4 Citation Tracking

EMA maintains citation tracking for provenance and structural protection:

```python
def update_citation_on_access(q: EpistemicQuantum, requester: str) -> None:
    """Track access for citation counting and vitality maintenance."""
    q.timestamps.last_accessed = current_timestamp()
    q.metabolic_state.circulation_count += 1

    # Update Hebbian edge weights for co-accessed quanta
    # (handled in Section 4.4 edge weight update)


def get_citation_chain(quantum_id: QuantumId, depth: int = 5) -> CitationTree:
    """Retrieve the full citation chain for a quantum."""
    tree = CitationTree(root=quantum_id)

    def traverse(qid: QuantumId, current_depth: int):
        if current_depth >= depth:
            return
        q = get_quantum(qid)
        if q is None:
            return
        for edge in q.edges:
            if edge.edge_type == "DERIVATION":
                tree.add_citation(qid, edge.target_id, edge.weight)
                traverse(edge.target_id, current_depth + 1)

    traverse(quantum_id, 0)
    return tree
```

---

## 10. Integration Interfaces

### 10.1 PCVM API

EMA integrates with PCVM (C5) for verification of all incoming knowledge:

```python
class PCVMInterface:
    """EMA's integration interface with PCVM (C5)."""

    def submit_for_verification(self, vtd: VTD) -> PCVMResult:
        """Submit a VTD for PCVM verification.
        Called during: Ingestion (Phase 1), Consolidation (Phase 3).
        """
        # Serialize VTD per C5 schema (Section 2.1 of C5 spec)
        payload = serialize_vtd(vtd)
        result = pcvm_client.verify(payload)
        return PCVMResult(
            verdict=result.verdict,           # "ACCEPTED" or "REJECTED"
            assigned_class=result.assigned_class,
            opinion=result.opinion,           # Subjective Logic opinion
            seal=result.classification_seal,
            rejection_reason=result.rejection_reason
        )

    def request_adversarial_probe(self, vtd_id: str) -> AdversarialResult:
        """Request adversarial probing for high-impact C-class claims.
        Per C5 Section 5: VRF-selected probers attempt to find flaws.
        """
        return pcvm_client.probe(vtd_id)

    def notify_opinion_update(self, quantum_id: QuantumId, new_opinion: Opinion) -> None:
        """Notify PCVM when a quantum's opinion is updated
        (e.g., via edge weight changes or aging).
        """
        claim_id = resolve_quantum_to_claim(quantum_id)
        pcvm_client.update_credibility(claim_id, new_opinion)

    def query_verification_status(self, claim_id: str) -> VerificationStatus:
        """Query current verification status of a claim."""
        return pcvm_client.get_status(claim_id)
```

### 10.2 Tidal Noosphere API

EMA integrates with the Tidal Noosphere (C3) for spatial coordination:

```python
class NoosphereInterface:
    """EMA's integration interface with Tidal Noosphere (C3)."""

    def resolve_locus(self, domain_tags: List[str]) -> LocusId:
        """Resolve domain tags to a locus in the Noosphere topology."""
        return noosphere_client.resolve_locus(domain_tags)

    def resolve_parcel(self, locus_id: LocusId, agent_id: AgentId) -> ParcelId:
        """Resolve agent's current parcel assignment within a locus."""
        return noosphere_client.get_agent_parcel(locus_id, agent_id)

    def push_projection(self, quantum_id: QuantumId, projection: C3Projection) -> None:
        """Push a C3 projection to the Noosphere for parcel-local availability."""
        target_parcels = projection.parcel_tags
        for parcel_id in target_parcels:
            noosphere_client.inject_knowledge_token(
                parcel_id=parcel_id,
                token=projection.to_knowledge_token(),
                source_quantum=quantum_id
            )

    def receive_parcel_update(self, update: ParcelKnowledgeUpdate) -> None:
        """Receive knowledge updates from Noosphere parcels.
        Triggers inverse C3 projection (Section 8.1) and canonical update.
        """
        canonical = get_quantum(update.source_quantum_id)
        if canonical is not None:
            quantum_update = reconstruct_from_c3(update, canonical)
            if quantum_update.reconstruction_fidelity >= C3_FIDELITY_TARGET - FIDELITY_TOLERANCE:
                apply_quantum_update(canonical, quantum_update)

    def get_parcel_topology(self, locus_id: LocusId) -> ParcelTopology:
        """Get current parcel topology for shard alignment."""
        return noosphere_client.get_topology(locus_id)
```

### 10.3 ASV API

EMA integrates with ASV/AASL (C4) for agent communication:

```python
class ASVInterface:
    """EMA's integration interface with ASV/AASL (C4)."""

    def receive_aasl_message(self, message: AASLMessage) -> QuantumId:
        """Receive an AASL message and route to ingestion.
        Message is converted to VTD draft and submitted to PCVM.
        """
        vtd_draft = map_asv_to_vtd_draft(message)
        vtd = finalize_vtd(vtd_draft)
        pcvm_result = pcvm_interface.submit_for_verification(vtd)

        if pcvm_result.verdict == "ACCEPTED":
            quantum = map_vtd_to_quantum(vtd, pcvm_result)
            insert_into_coherence_graph(quantum)
            return quantum.id
        else:
            log_ingestion_rejection(message, pcvm_result)
            return None

    def send_quantum_as_aasl(self, quantum_id: QuantumId, recipient: AgentId) -> None:
        """Send a quantum to an agent via AASL message."""
        q = get_quantum(quantum_id)
        projection = project_to_c4(q)
        aasl_message = projection.to_aasl_message(recipient=recipient)
        asv_client.send(aasl_message)

    def broadcast_circulation(self, quantum_id: QuantumId, subscribers: List[str]) -> None:
        """Broadcast quantum to AASL subscribers."""
        q = get_quantum(quantum_id)
        projection = project_to_c4(q)
        for sub_id in subscribers:
            aasl_message = projection.to_aasl_message(recipient=sub_id)
            asv_client.send(aasl_message)
```

### 10.4 Settlement API

EMA integrates with the Settlement Plane for economic coordination:

```python
class SettlementInterface:
    """EMA's integration interface with the Settlement Plane."""

    def report_metabolic_activity(self, epoch: EpochNum, report: MetabolicReport) -> None:
        """Report metabolic activity for settlement computation.
        Settlement may reward agents whose quanta are highly cited,
        frequently circulated, or successfully consolidated.
        """
        settlement_client.report(
            epoch=epoch,
            quanta_ingested=report.ingested_count,
            quanta_circulated=report.circulated_count,
            quanta_consolidated=report.consolidated_count,
            quanta_dissolved=report.dissolved_count,
            top_cited_agents=report.top_cited_agents,
            consolidation_contributors=report.consolidation_contributors
        )

    def query_agent_contribution(self, agent_id: AgentId) -> ContributionScore:
        """Query agent's knowledge contribution for settlement purposes."""
        # Count quanta originated by this agent that are still active
        active_quanta = count_active_quanta_by_agent(agent_id)
        # Sum citations across agent's quanta
        total_citations = sum_citations_by_agent(agent_id)
        # Count successful consolidations involving agent's quanta
        consolidation_count = count_consolidations_involving_agent(agent_id)

        return ContributionScore(
            active_quanta=active_quanta,
            total_citations=total_citations,
            consolidation_contributions=consolidation_count
        )
```

### 10.5 Sentinel Graph API

EMA integrates with the Sentinel Graph for system-level monitoring:

```python
class SentinelGraphInterface:
    """EMA's integration interface with the Sentinel Graph."""

    def report_health_metrics(self, epoch: EpochNum) -> None:
        """Report metabolic health metrics to the Sentinel Graph."""
        metrics = compute_metabolic_health_metrics()
        sentinel_client.report_metrics(
            subsystem="EMA",
            epoch=epoch,
            metrics={
                "metabolic_rate": metrics.metabolic_rate,
                "metabolic_efficiency": metrics.metabolic_efficiency,
                "anabolic_catabolic_ratio": metrics.anabolic_catabolic_ratio,
                "circulatory_efficiency": metrics.circulatory_efficiency,
                "coherence_density": metrics.coherence_density,
                "immune_health": metrics.immune_health,
                "shrec_regime": metrics.current_regime,
                "active_quanta_count": metrics.active_count,
                "total_edges": metrics.total_edges,
            }
        )

    def report_shrec_state(self, shrec_result: SHRECResult) -> None:
        """Report SHREC regulatory state for system-level visibility."""
        sentinel_client.report_metrics(
            subsystem="EMA:SHREC",
            epoch=shrec_result.epoch,
            metrics={
                f"signal_{name}": value
                for name, value in shrec_result.signals.items()
            } | {
                f"allocation_{name}": value
                for name, value in shrec_result.allocations.items()
            } | {
                "regime": shrec_result.regime,
                "total_budget": shrec_result.total_budget,
            }
        )

    def receive_system_alert(self, alert: SystemAlert) -> None:
        """Receive system-level alerts that affect EMA behavior."""
        if alert.type == "RESOURCE_CONSTRAINT":
            # Reduce total budget
            adjust_budget_ceiling(alert.constraint_factor)
        elif alert.type == "SECURITY_INCIDENT":
            # Increase immune signal
            boost_immune_signal(alert.severity)
```

---

## 11. Configurable Parameters

All configurable parameters consolidated for deployment reference:

### 11.1 Metabolic State Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| `DECAY_THRESHOLD` | 0.30 | [0.1, 0.5] | 2.2 |
| `QUARANTINE_THRESHOLD` | 0.15 | [0.05, 0.3] | 2.2 |
| `MAX_DECAY_EPOCHS` | 50 | [10, 200] | 2.2 |
| `MAX_QUARANTINE_EPOCHS` | 100 | [20, 500] | 2.2 |
| `BASE_DECAY_RATE` | 0.005 | [0.001, 0.05] | 2.4 |
| `ACCESS_DECAY_RATE` | 0.02 | [0.005, 0.1] | 2.4 |
| `SUPPORT_VITALITY_FACTOR` | 0.1 | [0.05, 0.3] | 2.4 |
| `CONTRADICTION_VITALITY_FACTOR` | 0.15 | [0.05, 0.3] | 2.4 |
| `MAX_TOTAL_CONTRADICTION_FACTOR` | 0.8 | [0.5, 1.0] | 2.4 |
| `SUPERSESSION_DECAY_MULTIPLIER` | 2.0 | [1.5, 5.0] | 2.4 |

### 11.2 Edge Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| `REINFORCEMENT_RATE` | 0.05 | [0.01, 0.2] | 4.4 |
| `EDGE_DECAY_RATE` | 0.02 | [0.005, 0.1] | 4.4 |
| `EDGE_TTL` | 50 | [10, 200] | 4.4 |
| `MIN_EDGE_WEIGHT` | 0.05 | [0.01, 0.1] | 4.4 |
| `MAX_EDGES_PER_QUANTUM` | 50 | [20, 100] | 4.4 |
| `MAX_EDGES_PER_SHARD` | 500000 | [100000, 5000000] | 4.4 |
| `EDGE_DISCOVERY_THRESHOLD` | 0.4 | [0.2, 0.7] | 3.4 |
| `INITIAL_EDGE_DISCOVERY_K` | 10 | [3, 20] | 3.4 |

### 11.3 Consolidation Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| `MIN_CLUSTER_SIZE` | 5 | [3, 10] | 5.1 |
| `MIN_MUTUAL_SUPPORT_EDGES` | 3 | [2, 8] | 5.1 |
| `CONSOLIDATION_MIN_EDGE_WEIGHT` | 0.3 | [0.1, 0.6] | 5.1 |
| `MAX_CONSOLIDATION_CANDIDATES_PER_EPOCH` | 5 | [1, 20] | 5.1 |
| `MIN_INDEPENDENT_AGENTS` | 5 | [3, 10] | 5.2 |
| `MIN_INDEPENDENT_PARCELS` | 3 | [2, 5] | 5.2 |
| `MIN_INDEPENDENT_CHAINS` | 3 | [2, 5] | 5.2 |
| `CONSOLIDATION_LOCK_TTL` | 5 | [1, 20] | 5.3 |
| `NUM_SYNTHESIS_PASSES` | 3 | [2, 5] | 5.4 |
| `SYNTHESIS_TEMPERATURE` | 0.3 | [0.1, 0.7] | 5.4 |
| `MAJORITY_THRESHOLD` | 2 | [2, NUM_SYNTHESIS_PASSES] | 5.4 |
| `CONSOLIDATION_COOLDOWN_EPOCHS` | 20 | [5, 50] | 5.8 |
| `CCLASS_VALIDATION_WINDOW` | 50 | [20, 200] | 5.9 |
| `CCLASS_AGING_UNCERTAINTY_RATE` | 0.1 | [0.05, 0.2] | 5.9 |

### 11.4 Catabolism Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| `CATABOLISM_CREDIBILITY_THRESHOLD` | 0.3 | [0.1, 0.5] | 6.1 |
| `DECAY_AGE_THRESHOLD` | 100 | [20, 500] | 6.1 |
| `SUPERSESSION_MARGIN` | 0.1 | [0.05, 0.3] | 6.1 |
| `STRUCTURAL_PROTECTION_THRESHOLD` | 10 | [5, 50] | 6.2 |
| `KEYSTONE_DISCONNECT_THRESHOLD` | 5 | [2, 20] | 6.2 |
| `QUARANTINE_SNAPSHOT_RETENTION_EPOCHS` | 200 | [50, 1000] | 6.4 |
| `MAX_RECYCLING_RECIPIENTS` | 5 | [1, 10] | 6.3 |
| `MAX_AGENT_CONTRADICTION_WEIGHT` | 0.3 | [0.1, 0.5] | 2.3.2 |

### 11.5 SHREC Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| `BUDGET_SAFETY_MARGIN` | 0.15 | [0.05, 0.3] | 7.2 |
| `STATS_WINDOW_EPOCHS` | 100 | [20, 500] | 7.5 |
| `BAYESIAN_PRIOR_WEIGHT` | 5.0 | [1.0, 20.0] | 7.5 |
| `ELEVATED_Z_THRESHOLD` | 1.5 | [1.0, 2.0] | 7.6 |
| `CRITICAL_Z_THRESHOLD` | 2.5 | [2.0, 3.5] | 7.6 |
| `REGIME_HYSTERESIS_EPOCHS` | 5 | [2, 20] | 7.6 |
| `PID_CLAMP_ELEVATED` | 0.10 | [0.05, 0.2] | 7.7 |
| `PID_CLAMP_CRITICAL` | 0.25 | [0.15, 0.4] | 7.7 |
| `INTEGRAL_CLAMP` | 0.20 | [0.1, 0.5] | 7.7 |
| `IMMUNE_AUDIT_INTERVAL` | 50 | [10, 100] | 7.8 |
| `AUTOIMMUNE_ALARM_THRESHOLD` | 0.20 | [0.1, 0.4] | 7.8 |

### 11.6 Circulation Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| `RECIRCULATION_WINDOW` | 3 | [1, 10] | 4.2 |
| `VITALITY_CIRCULATION_THRESHOLD` | 0.5 | [0.3, 0.8] | 4.2 |
| `CIRCULATION_COOLDOWN` | 5 | [1, 20] | 4.2 |
| `MAX_SUBSCRIBER_BACKLOG` | 500 | [100, 5000] | 4.3 |
| `CONTEXT_BOOST_FACTOR` | 0.3 | [0.1, 0.5] | 9.3 |

### 11.7 Projection Parameters

| Parameter | Default | Range | Section |
|-----------|---------|-------|---------|
| `C3_FIDELITY_TARGET` | 0.85 | [0.75, 0.95] | 8.1 |
| `C4_FIDELITY_TARGET` | 0.88 | [0.80, 0.95] | 8.2 |
| `C5_FIDELITY_TARGET` | 0.92 | [0.85, 0.98] | 8.3 |
| `FIDELITY_TOLERANCE` | 0.05 | [0.02, 0.10] | 8.4 |
| `FIDELITY_WINDOW` | 100 | [20, 500] | 8.4 |

---

## 12. Conformance Requirements

### 12.1 MUST Requirements (Mandatory)

An implementation MUST satisfy all of the following to claim EMA conformance:

| ID | Requirement | Section |
|----|-------------|---------|
| CR-1 | Implement the complete epistemic quantum schema (all 10 tuple fields) | 2.1 |
| CR-2 | Enforce the lifecycle state machine with all defined transitions | 2.2 |
| CR-3 | Enforce b + d + u = 1 constraint on all Subjective Logic opinions | 1.2 |
| CR-4 | Gate all quantum creation through PCVM verification (INV-E2) | 3.1 |
| CR-5 | Execute metabolic phases in strict order within each epoch (INV-E3) | 1.5 |
| CR-6 | Implement consolidation locks with bounded TTL (INV-E4) | 5.3 |
| CR-7 | Enforce dissolution irreversibility (INV-E5) | 2.2 |
| CR-8 | Enforce edge budget limits per quantum and per shard (INV-E6) | 4.4 |
| CR-9 | Enforce SHREC floor allocations (INV-E7) | 7.3 |
| CR-10 | Maintain complete W3C PROV provenance for every quantum (INV-E9) | 2.1, 3.1 |
| CR-11 | Enforce per-agent contradiction weight cap (INV-E10) | 2.3.2 |
| CR-12 | Implement provenance diversity verification for consolidation (>= 5 agents, >= 3 parcels) | 5.2 |
| CR-13 | Implement 3-pass majority voting for LLM synthesis | 5.4 |
| CR-14 | Submit all C-class claims to PCVM for verification | 5.6 |
| CR-15 | Implement two-phase catabolism (quarantine then dissolution) | 6.1, 6.4 |
| CR-16 | Preserve dissolution records permanently | 6.5 |
| CR-17 | Implement structural protection for highly-cited quanta | 6.2 |
| CR-18 | Compute all five SHREC signals each epoch | 7.1 |
| CR-19 | Implement regime detection with hysteresis | 7.6 |
| CR-20 | Implement PID overlay with anti-windup for ELEVATED+ regimes | 7.7 |
| CR-21 | Implement projection functions for C3, C4, and C5 | 8.1-8.3 |
| CR-22 | Monitor projection fidelity and alarm on degradation | 8.4 |
| CR-23 | Implement C-class aging uncertainty for unvalidated consolidations | 5.9 |
| CR-24 | DERIVATION edges MUST NOT be pruned or have weight reduced | 2.3.3 |

### 12.2 SHOULD Requirements (Recommended)

| ID | Requirement | Section |
|----|-------------|---------|
| SR-1 | SHOULD implement Hebbian edge weight reinforcement | 4.4 |
| SR-2 | SHOULD implement context-aware retrieval | 9.3 |
| SR-3 | SHOULD implement immune self-audit at configurable intervals | 7.8 |
| SR-4 | SHOULD implement frequency-dependent selection for rare SHREC signals | 7.4 |
| SR-5 | SHOULD implement CUSUM change-point detection for PID anti-windup | 7.7 |
| SR-6 | SHOULD implement quarantine rescue by dreaming process | 2.2 |
| SR-7 | SHOULD implement keystone detection for structural protection | 6.2 |
| SR-8 | SHOULD implement Lotka-Volterra dynamics for competitive allocation | 7.9 |
| SR-9 | SHOULD cache projections and implement staleness detection | 8.5 |
| SR-10 | SHOULD report metabolic health metrics to Sentinel Graph | 10.5 |
| SR-11 | SHOULD implement evidence recycling before dissolution | 6.3 |
| SR-12 | SHOULD implement derivative monitoring alarm for PID stability | 7.7 |

### 12.3 MAY Requirements (Optional)

| ID | Requirement | Section |
|----|-------------|---------|
| MR-1 | MAY implement additional edge types beyond the five defined | 2.3 |
| MR-2 | MAY implement cross-shard consolidation for multi-locus patterns | 5.1 |
| MR-3 | MAY implement additional projection targets beyond C3, C4, C5 | 8 |
| MR-4 | MAY implement configurable per-locus metabolic parameters | 11 |
| MR-5 | MAY implement decay_rate_override for individual quanta | 2.1 |
| MR-6 | MAY implement additional synthesis prompt framings beyond three | 5.4 |
| MR-7 | MAY implement settlement-aware circulation priority | 4.2 |

---

## 13. Test Vectors

### 13.1 TV-1: Epistemic Quantum Construction

**Input:** A verified D-class VTD with the following fields:

```json
{
  "vtd_id": "vtd:clm:biology.proteomics:100:a1b2c3d4:1",
  "claim_id": "clm:biology.proteomics:100:a1b2c3d4",
  "claim_text": "Protein folding rate for sequence ACGT... is 3.2ms under standard conditions.",
  "assigned_class": "D",
  "producing_agent": "agent-alpha-7f3a",
  "epoch": 100,
  "locus": "biology.proteomics",
  "timestamp": "2026-03-10T14:23:00Z",
  "dependencies": [],
  "proof_body": {"computation": "fold_sim_v3", "inputs": {"seq": "ACGT..."}, "output": "3.2ms"}
}
```

**PCVM result opinion:** `(b=0.95, d=0.0, u=0.05, a=0.5)`

**Expected quantum:**
- `id`: matches pattern `eq:biology.proteomics:100:<uuid7_short>`
- `content.claim_type`: `"observation"` (D-class maps to observation)
- `content.domain_tags`: includes `"biology"` and `"proteomics"`
- `opinion`: `(b=0.95, d=0.0, u=0.05, a=0.5)`
- `metabolic_state.phase`: `"ACTIVE"`
- `metabolic_state.vitality`: `1.0`
- `claim_class`: `"D"`
- `provenance.generating_activity`: `"ingestion"`
- `edges`: empty (no dependencies)
- `dissolution_record`: `null`

**Verification:** `E(w) = 0.95 + 0.5 * 0.05 = 0.975`

### 13.2 TV-2: Vitality Computation

**Input quantum state:**
- Age: 50 epochs
- Last accessed: 10 epochs ago
- Support edges: 3 edges with weights [0.8, 0.6, 0.4]
- Contradiction edges: 1 edge with weight 0.5
- Opinion: `(b=0.7, d=0.1, u=0.2, a=0.5)`
- No supersession

**Computation (with defaults):**

```
base_decay = exp(-0.005 * 50) = exp(-0.25) = 0.7788
access_recency = exp(-0.02 * 10) = exp(-0.2) = 0.8187
support_factor = min(1.0, 0.5 + (0.8+0.6+0.4) * 0.1) = min(1.0, 0.5 + 0.18) = 0.68
contradiction_factor = min(0.8, 0.5 * 0.15) = 0.075
credibility = 0.7 + 0.5 * 0.2 = 0.8
supersession_penalty = 0.0

vitality = 0.7788 * 0.8187 * 0.68 * (1.0 - 0.075) * 0.8 * (1.0 - 0.0)
         = 0.7788 * 0.8187 * 0.68 * 0.925 * 0.8
         = 0.7788 * 0.8187 = 0.6377
         * 0.68 = 0.4336
         * 0.925 = 0.4011
         * 0.8 = 0.3209
```

**Expected vitality:** approximately 0.321

**State transition:** Since 0.321 > `DECAY_THRESHOLD` (0.30), quantum remains ACTIVE.

### 13.3 TV-3: SHREC Floor Enforcement

**Scenario:** All signals at zero intensity except IMMUNE at 1.0.

**Expected behavior:**
- Total budget: 1000 (arbitrary units)
- Floor allocations: IMMUNE=150, STRESS=100, NOVELTY=80, HUNGER=50, CONSOLIDATION=50 (total=430)
- Competitive pool: 570
- With only IMMUNE having intensity > 0, competitive allocation gives 100% of pool to IMMUNE
- Final: IMMUNE=150+570=720, STRESS=100, NOVELTY=80, HUNGER=50, CONSOLIDATION=50
- Total: 1000

**Verification:** All signals receive at least their floor allocation. No signal is at zero. INV-E7 satisfied.

### 13.4 TV-4: Consolidation Pipeline

**Input:** 7 active quanta in shard `biology.proteomics`:
- Q1-Q7, all ACTIVE, all with opinion uncertainty > 0.3
- Mutual support edges: Q1-Q2 (0.7), Q1-Q3 (0.6), Q2-Q3 (0.5), Q3-Q4 (0.8), Q4-Q5 (0.6), Q5-Q6 (0.4), Q6-Q7 (0.3)
- Generating agents: 6 distinct agents across 4 parcels
- No shared derivation chains

**Expected steps:**
1. Candidate identification: BFS finds connected component {Q1,Q2,Q3,Q4,Q5,Q6,Q7} (size=7 >= MIN_CLUSTER_SIZE=5)
2. Mutual support count: 6 edges with weight > 0.3 (>= MIN_MUTUAL_SUPPORT_EDGES=3)
3. Provenance diversity: 6 agents >= 5 (pass), 4 parcels >= 3 (pass)
4. Lock acquisition: all 7 quanta transition to CONSOLIDATING
5. LLM synthesis: 3 passes generate candidate claims
6. Majority voting: claims appearing in >= 2 passes retained
7. VTD construction: C-class VTD with all 7 source quanta
8. PCVM submission: if accepted, new quantum created with DERIVATION edges from Q1-Q7
9. Lock release: all 7 quanta return to ACTIVE

**Verification:** New quantum has claim_class="C", opinion.uncertainty >= 0.4, provenance.generating_activity="consolidation".

### 13.5 TV-5: Catabolism with Structural Protection

**Input:** Quantum Q-old with:
- opinion: `(b=0.1, d=0.5, u=0.4, a=0.5)` -> credibility = 0.1 + 0.5*0.4 = 0.3
- age: 150 epochs (> DECAY_AGE_THRESHOLD=100)
- citation_count: 15 (> STRUCTURAL_PROTECTION_THRESHOLD=10)

**Expected behavior:** Despite meeting catabolism criteria (credibility=0.3 at threshold AND age > 100), quantum is structurally protected due to citation_count=15. Quantum remains ACTIVE.

**Verification:** `is_structurally_protected(Q-old)` returns `True`. No state transition occurs.

### 13.6 TV-6: Per-Agent Contradiction Cap

**Input:** Agent `agent-malicious` attempts to create 5 contradiction edges to quantum Q-target, each with weight 0.1.

**Computation:**
- After edge 1: total = 0.1 (<= MAX_AGENT_CONTRADICTION_WEIGHT=0.3) -> allowed
- After edge 2: total = 0.2 (<= 0.3) -> allowed
- After edge 3: total = 0.3 (<= 0.3) -> allowed
- Edge 4: total would be 0.4 (> 0.3) -> REJECTED per INV-E10

**Expected result:** Only 3 contradiction edges created. Fourth and fifth rejected.

### 13.7 TV-7: Regime Detection with Hysteresis

**Input sequence:**
- Epoch 100: max z-score = 1.8 (ELEVATED), current regime = NORMAL
- Epoch 101: max z-score = 1.2 (NORMAL), current regime = ELEVATED
- Epoch 102: max z-score = 1.1 (NORMAL), current regime = ELEVATED
- Epoch 103: max z-score = 0.9 (NORMAL), current regime = ELEVATED
- Epoch 104: max z-score = 1.0 (NORMAL), current regime = ELEVATED
- Epoch 105: max z-score = 0.8 (NORMAL), current regime = ELEVATED

**Expected transitions:**
- Epoch 100: NORMAL -> ELEVATED (upward: immediate)
- Epochs 101-104: remain ELEVATED (downward: need 5 consecutive epochs at NORMAL)
- Epoch 105: ELEVATED -> NORMAL (5 consecutive epochs at NORMAL achieved)

### 13.8 TV-8: Projection Fidelity (C3)

**Input quantum:**
- claim_text: "Protein folding rate for sequence ACGT is 3.2ms"
- opinion: `(b=0.8, d=0.05, u=0.15, a=0.5)`
- edges: 3 SUPPORT edges (2 within parcel, 1 cross-parcel), 1 ANALOGY edge

**C3 projection:**
- claim_text preserved (1.0 match)
- relevance_score: E(w) = 0.8 + 0.5*0.15 = 0.875
- local_edges: 2 SUPPORT edges (cross-parcel and ANALOGY lost)

**Round-trip reconstruction:**
- Text similarity: 1.0 (unchanged)
- Opinion: original E(w)=0.875, reconstructed=0.875, but uncertainty not recovered -> Wasserstein penalty
  - Reconstructed opinion: (b=0.8, d=0.05, u=0.15, a=0.5) using heuristic -> distance ~ 0.0 if scale=1.0
  - opinion_preservation: ~1.0 (scalar matches, but SL detail potentially lost)
- Edge fidelity: 2 out of 3 relevant edges preserved = 2/3 = 0.667 (ANALOGY excluded from comparison)
  - Original local: {(target1, SUPPORT), (target2, SUPPORT)} -> 2 edges
  - Projected: {(target1, SUPPORT), (target2, SUPPORT)} -> 2 edges
  - If both within-parcel edges match: Jaccard = 2/2 = 1.0

**Fidelity: 1.0*0.5 + 1.0*0.3 + 1.0*0.2 = 1.0** (best case, within-parcel)

**Note:** Fidelity degrades when cross-parcel edges and analogy edges are important to the consumer.

---

## 14. Security Considerations

### 14.1 Consolidation Poisoning (A3)

**Threat:** Coordinated agents inject quanta designed to steer dreaming toward a desired conclusion.

**Mitigations:**
1. Provenance diversity requirement (>= 5 independent agents, >= 3 parcels) prevents single-actor manipulation (CR-12)
2. Per-agent contradiction cap (INV-E10, CR-11) limits influence per agent
3. PCVM verification of C-class claims catches logically invalid consolidations (CR-14)
4. 3-pass majority voting reduces stochastic manipulation (CR-13)

**Residual risk:** A coordinated group of >= 5 agents across >= 3 parcels can still steer consolidation. Mitigation: PCVM adversarial probing for high-impact consolidations, plus immune self-audit detecting systematic patterns.

### 14.2 Catabolism Weaponization (A6)

**Threat:** Agents strategically create contradiction edges to drive valid quanta toward dissolution.

**Mitigations:**
1. Per-agent contradiction weight cap (INV-E10): total contradiction from any single agent capped at 0.3
2. Structural protection (Section 6.2): highly-cited quanta immune to catabolism
3. Immune self-audit (Section 7.8): detects systematic false positive quarantining
4. Quarantine rescue (Section 2.2): dreaming can rescue falsely quarantined quanta

### 14.3 Projection Gap Exploitation (A4)

**Threat:** Exploiting information loss in projections to inject inconsistent knowledge across subsystems.

**Mitigations:**
1. Canonical source principle (INV-E1): canonical quantum always governs in conflicts
2. PCVM verification required for all updates that modify canonical quantum
3. Fidelity monitoring (Section 8.4): detects systematic fidelity degradation
4. Consistency model (Section 8.5): safety-critical quanta use strong consistency

### 14.4 SHREC Signal Gaming (A5)

**Threat:** Agents manipulate SHREC signals to starve certain metabolic processes.

**Mitigations:**
1. Floor allocations (INV-E7): constitutional minimums cannot be violated
2. Frequency-dependent selection: rare signals get competitive advantage
3. PID overlay with anti-windup: prevents runaway signal manipulation
4. Regime hysteresis: prevents oscillation-based attacks

### 14.5 Coherence Graph Scale Attack (A8)

**Threat:** Overwhelming the coherence graph with edges to cause computational collapse.

**Mitigations:**
1. Edge budget per quantum (MAX_EDGES_PER_QUANTUM=50) and per shard (MAX_EDGES_PER_SHARD=500000) (INV-E6)
2. Edge pruning: lowest-weight edges removed when budget exceeded
3. Shard-aligned scaling: coherence computation bounded to O(V_local * E_max) per shard
4. Edge TTL: edges decay and are pruned if not reinforced

### 14.6 Data Integrity

**Requirements:**
1. All quantum content MUST be hashed (SHA-256) and hash stored in `quantum_hash` field
2. Dissolution records MUST preserve `content_hash` for post-dissolution audit
3. Provenance chains MUST NOT have gaps (INV-E9)
4. DERIVATION edges MUST NOT be deleted (CR-24)

### 14.7 Access Control

**Requirements:**
1. Only PCVM-verified agents MAY submit quanta for ingestion
2. Only the EMA dreaming engine (identified by `ema:dreaming:*` agent pattern) MAY acquire consolidation locks
3. Only EMA's catabolism process MAY transition quanta to DISSOLVED state
4. Retrieval queries MUST be authenticated by AgentId
5. Settlement contribution queries MUST be authorized per agent (agents can only query their own contributions)

### 14.8 Denial of Service

**Threats and mitigations:**
1. **Ingestion flooding:** SHREC metabolic_stress signal detects backlog; SHREC reduces ingestion budget
2. **Query flooding:** Rate limiting per agent on retrieval interface
3. **Consolidation starvation:** SHREC consolidation_pressure signal increases until dreaming is triggered; floor allocation guarantees minimum budget
4. **Edge flooding:** Edge budget per quantum and per shard; pruning of lowest-weight edges

---

*Specification produced under Atrahasis Agent System v2.0 protocol.*
*C6: Epistemic Metabolism Architecture (EMA) -- SPECIFICATION stage.*
*Version 1.0.0 -- 2026-03-10*
