# C7 RIF Master Tech Spec — Patch Addendum
## Findings F47 through F51
## Version 1.0 — 2026-03-10

**Applies to:** C7-A Recursive Intent Fabric Master Tech Spec v1.0
**Status:** NORMATIVE PATCH — all corrections in this addendum supersede the corresponding text in the base specification.

---

## Table of Contents

- [PA-1: F47 — Dual Schema Conflict Resolution (HIGH)](#pa-1-f47--dual-schema-conflict-resolution-high)
- [PA-2: F48 — Strategy Selection Algorithm (MEDIUM)](#pa-2-f48--strategy-selection-algorithm-medium)
- [PA-3: F49 — Operation Class Name Inconsistency (MEDIUM)](#pa-3-f49--operation-class-name-inconsistency-medium)
- [PA-4: F50 — PBFT Variant Specification: HotStuff (MEDIUM)](#pa-4-f50--pbft-variant-specification-hotstuff-medium)
- [PA-5: F51 — Shared Resource Contention Protocol (MEDIUM)](#pa-5-f51--shared-resource-contention-protocol-medium)
- [PA-6: E-C7-01 — Settlement Router Target Correction](#pa-6-e-c7-01--settlement-router-target-correction)

---

## PA-1: F47 — Dual Schema Conflict Resolution (HIGH)

### Problem

Section 5.1 and Appendix A each define a JSON Schema for the IntentQuantum. They diverge in field names, structural organization, success criteria modeling, compensation strategy enums, and required-field lists. Two competing normative schemas in the same specification create ambiguity for implementers.

### Conflict Inventory

Every difference between the Section 5.1 schema and the Appendix A schema is enumerated below.

| # | Field / Area | Section 5.1 | Appendix A | Resolution |
|---|---|---|---|---|
| 1 | `title` | `"RIF Intent Quantum"` | `"IntentQuantum"` | Use `"IntentQuantum"` (PascalCase matches type name in pseudocode) |
| 2 | `description` (field) | Present as top-level field, `maxLength: 4096` | Absent; replaced by `content` field | **Merge both.** Keep `description` (max 4096, human-readable). Add `content` (structured specification). See below. |
| 3 | `content` | Absent | Present (`type: string`, structured intent spec) | Add to normative schema. |
| 4 | `intent_id.format` | `"format": "uuid"` (UUID format hint) | `"pattern": "^[0-9a-f]{64}$"` (256-bit hex) | Use Appendix A pattern. The spec says "256-bit identifier" (line 469), which is 64 hex chars, not a 128-bit UUID. |
| 5 | `scope.target_parcels` | Present (`array of string`) | Absent | Retain from 5.1. Parcels are C3's addressable state units; targeting them is meaningful. |
| 6 | `scope.requires_exclusive_access` | Present (`boolean, default false`) | Absent | Retain from 5.1. Used by `map_to_operation_class()` at line 1765. |
| 7 | `scope.is_bounded_local` | Present (`boolean, default true`) | Absent | Retain from 5.1. Used by `map_to_operation_class()` at line 1766. |
| 8 | `scope.requires_verification` | Present (`boolean, default false`) | Absent | Retain from 5.1. Used by `map_to_operation_class()` at line 1770. |
| 9 | `scope.target_loci.minItems` | Not specified | `minItems: 1` | Use Appendix A constraint. At least one target locus is logically required. |
| 10 | `origin.proposal_epoch` | Present (required) | Absent | Retain from 5.1. Needed for deadline calculations relative to proposal time. |
| 11 | `origin.causal_stamp.wall_time_ms` | Present (required) | Absent | Retain from 5.1. CausalStamp `$defs` requires it. |
| 12 | `origin.causal_stamp.agent_id` | Present (in CausalStamp `$defs`, required) | Absent | Retain from 5.1. |
| 13 | `origin.causal_stamp.locus_id` | Present (in CausalStamp `$defs`, required) | Absent | Retain from 5.1. |
| 14 | `origin.causal_stamp.signature` | Absent | Present (`Ed25519 signature`, required) | Add from Appendix A. Cryptographic provenance is essential for sovereign agents. |
| 15 | `authorization` | Absent | Present (`object or null`, GovernanceToken) | Add from Appendix A. Required for cross-locus and G-class intents. |
| 16 | `decomposition_strategy` nullable | `type: ["string", "null"]`, null allowed in enum | `type: "string"`, `default: "RECURSIVE"`, null not in enum | Use 5.1 approach: nullable. Root intents proposed by agents should not pre-specify strategy; System 3 selects it. But add `default: "RECURSIVE"` from Appendix A for non-null cases. |
| 17 | `constraints.decomposition_token_limit` | Present (name: `decomposition_token_limit`, required) | Present (name: `decomposition_budget_tokens`, NOT required) | Use 5.1 name `decomposition_token_limit` (matches line 554). Add to required list. |
| 18 | `constraints.allow_spanning` default | `default: true` | `default: false` | Use 5.1 default `true`. The spec assumes spanning is permitted unless restricted (line 686). |
| 19 | `constraints` required fields | `["max_depth", "decomposition_budget_ms", "decomposition_token_limit"]` | `["max_depth", "decomposition_budget_ms"]` | Use 5.1 (three required). Token limit is a termination guarantee (C-04). |
| 20 | `resource_bounds.bandwidth_bytes` | Present (name: `bandwidth_bytes`) | Present (name: `network_bytes`) | Use 5.1 name `bandwidth_bytes`. Matches §6.4 resource bound preservation text (line 1181). |
| 21 | `resource_bounds.iops` | Present | Absent | Retain from 5.1. Shared-resource contention needs IOPS tracking. |
| 22 | `resource_bounds` minimums | `minimum: 0` for all | `minimum: 1` for compute_tokens and wall_time_ms | Use Appendix A minimums for compute_tokens and wall_time_ms (minimum: 1). Zero compute or zero time is nonsensical for executable intents. Keep minimum: 0 for optional fields. |
| 23 | `success_criteria.criteria_type` | Present (`enum: PREDICATE, THRESHOLD, TEMPORAL, COMPOSITE`) | Absent | Retain from 5.1. The criteria_type discriminator enables schema validation per criteria form. |
| 24 | `success_criteria.predicates` structure | `predicate_id`, `observable`, `operator` (9-value enum), `expected_value` | `predicate_id`, `expression` (string), `weight`, `required` | **Merge.** Keep 5.1's structured fields (observable, operator, expected_value) as the primary form. Add `weight` and `required` from Appendix A. Add `expression` as optional override for complex predicates. See merged definition below. |
| 25 | `success_criteria.thresholds` | Present (separate array with metric/operator/value) | Absent (folded into predicates) | Retain from 5.1. Thresholds are semantically distinct from boolean predicates. |
| 26 | `success_criteria.temporal_bound` | Present (`$ref TemporalBound`) | Absent | Retain from 5.1. |
| 27 | `success_criteria.composition` | `enum: ["AND", "OR"]` | Absent; replaced by `aggregation` | Use Appendix A's richer `aggregation` enum (`ALL_REQUIRED`, `WEIGHTED_THRESHOLD`, `ANY_REQUIRED`). Rename field to `aggregation`. Map: AND -> ALL_REQUIRED, OR -> ANY_REQUIRED. |
| 28 | `success_criteria.threshold` (aggregation threshold) | Absent | Present (`number 0-1`, for WEIGHTED_THRESHOLD) | Add from Appendix A. |
| 29 | `lifecycle_state` | Absent from 5.1 schema | Present in Appendix A | Add from Appendix A. The ISR tracks this field (line 1493). |
| 30 | `parent_intent_id` | Absent from 5.1 schema | Present (nullable string) | Add from Appendix A. Required for tree traversal. |
| 31 | `child_intent_ids` | Absent from 5.1 schema | Present (array, default []) | Add from Appendix A. |
| 32 | `provenance` (top-level W3C PROV object) | Absent from 5.1 schema | Present (object) | Add from Appendix A. Distinct from `origin.provenance_chain` (which tracks C4 claim IDs). |
| 33 | `compensation.strategy` enum | `["REVERSE_SETTLEMENT", "RE_DECOMPOSE", "ESCALATE", "NONE"]` | `["SAGA_ROLLBACK", "COMPENSATING_INTENT", "ABANDON"]` | **Merge into unified enum.** See below. |
| 34 | `compensation.max_compensation_epochs` | Present (5.1 name) | Present as `timeout_epochs` | Use `timeout_epochs` (clearer semantics). |
| 35 | `compensation.compensation_intents` | Absent | Present (array of intent IDs) | Add from Appendix A. |
| 36 | `metadata.created_epoch` / `last_modified_epoch` | Present | Absent | Retain from 5.1. |
| 37 | Required top-level fields | `["intent_id", "intent_type", "origin", "scope", "description", "success_criteria", "resource_bounds", "constraints", "output_spec"]` | `["intent_id", "intent_type", "content", "scope", "origin", "constraints", "resource_bounds", "success_criteria", "lifecycle_state"]` | See merged required list below. |

### Normative Merged Schema

This schema supersedes both Section 5.1 and Appendix A. All RIF implementations MUST conform to this schema.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.org/rif/intent-quantum/v1.1",
  "title": "IntentQuantum",
  "description": "The fundamental unit of work in the Recursive Intent Fabric. A self-describing goal with typed semantics, machine-evaluable success criteria, resource bounds, decomposition constraints, and W3C PROV provenance.",
  "type": "object",
  "properties": {
    "intent_id": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "Globally unique 256-bit identifier (64 hex characters)"
    },
    "intent_type": {
      "type": "string",
      "enum": ["GOAL", "DIRECTIVE", "QUERY", "OPTIMIZATION"],
      "description": "GOAL=open-ended objective, DIRECTIVE=specific instruction, QUERY=information request, OPTIMIZATION=improve existing state"
    },
    "operation_class": {
      "type": ["string", "null"],
      "enum": ["M", "B", "X", "V", "G", null],
      "description": "C3 operation class. Null for non-leaf intents; derived at leaf level by map_to_operation_class()."
    },
    "origin": {
      "type": "object",
      "properties": {
        "proposer_agent_id": { "type": "string" },
        "proposer_locus_id": { "type": "string" },
        "proposal_epoch": { "type": "integer" },
        "causal_stamp": { "$ref": "#/$defs/CausalStamp" },
        "provenance_chain": {
          "type": "array",
          "items": { "type": "string" },
          "description": "C4 ASV claim IDs forming the provenance chain"
        }
      },
      "required": ["proposer_agent_id", "proposer_locus_id",
                    "proposal_epoch", "causal_stamp"]
    },
    "scope": {
      "type": "object",
      "properties": {
        "domain": { "type": "string" },
        "target_loci": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "target_parcels": {
          "type": "array",
          "items": { "type": "string" }
        },
        "requires_exclusive_access": { "type": "boolean", "default": false },
        "is_bounded_local": { "type": "boolean", "default": true },
        "affects_governance": { "type": "boolean", "default": false },
        "requires_verification": { "type": "boolean", "default": false }
      },
      "required": ["domain", "target_loci"]
    },
    "description": {
      "type": "string",
      "maxLength": 4096,
      "description": "Human-readable description of the intent's purpose"
    },
    "content": {
      "type": ["string", "null"],
      "description": "Structured intent specification in natural language or domain-specific format. Null for intents where description is sufficient."
    },
    "authorization": {
      "type": ["object", "null"],
      "description": "GovernanceToken; required for cross-locus and G-class intents, null otherwise.",
      "properties": {
        "token_id": { "type": "string" },
        "granted_by": { "type": "string", "description": "G-class vote ID or System 5 authorization" },
        "scope": { "type": "string", "enum": ["CROSS_LOCUS", "G_CLASS", "SOVEREIGNTY_RELAXATION"] },
        "expiry_epoch": { "type": "integer" }
      }
    },
    "success_criteria": {
      "type": "object",
      "properties": {
        "criteria_type": {
          "type": "string",
          "enum": ["PREDICATE", "THRESHOLD", "TEMPORAL", "COMPOSITE"],
          "description": "Discriminator for which criteria fields are populated"
        },
        "predicates": {
          "type": "array",
          "items": { "$ref": "#/$defs/SuccessPredicate" }
        },
        "thresholds": {
          "type": "array",
          "items": { "$ref": "#/$defs/SuccessThreshold" }
        },
        "temporal_bound": { "$ref": "#/$defs/TemporalBound" },
        "aggregation": {
          "type": "string",
          "enum": ["ALL_REQUIRED", "WEIGHTED_THRESHOLD", "ANY_REQUIRED"],
          "default": "ALL_REQUIRED",
          "description": "ALL_REQUIRED=all predicates/thresholds must pass, WEIGHTED_THRESHOLD=weighted sum >= threshold, ANY_REQUIRED=at least one must pass"
        },
        "threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Required when aggregation=WEIGHTED_THRESHOLD: minimum weighted sum of predicate results"
        }
      },
      "required": ["criteria_type"]
    },
    "resource_bounds": { "$ref": "#/$defs/ResourceBounds" },
    "constraints": {
      "type": "object",
      "properties": {
        "max_depth": {
          "type": "integer", "minimum": 1, "maximum": 20, "default": 10
        },
        "decomposition_budget_ms": {
          "type": "integer", "minimum": 100, "maximum": 60000, "default": 5000
        },
        "decomposition_token_limit": {
          "type": "integer", "minimum": 100, "maximum": 1000000, "default": 10000
        },
        "deadline_epoch": { "type": ["integer", "null"] },
        "priority": {
          "type": "integer", "minimum": 0, "maximum": 100, "default": 50
        },
        "min_agent_credibility": {
          "type": "number", "minimum": 0, "maximum": 1, "default": 0.5
        },
        "allow_spanning": { "type": "boolean", "default": true }
      },
      "required": ["max_depth", "decomposition_budget_ms",
                    "decomposition_token_limit"]
    },
    "decomposition_strategy": {
      "type": ["string", "null"],
      "enum": ["RECURSIVE", "PARALLEL", "SEQUENTIAL", "CONDITIONAL", null],
      "default": null,
      "description": "Null when proposed; System 3 assigns via select_strategy(). RECURSIVE is default when assigned."
    },
    "input_references": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ref_type": {
            "type": "string",
            "enum": ["PARCEL", "INTENT_OUTPUT", "EMA_QUANTUM",
                     "ASV_CLAIM", "EXTERNAL"]
          },
          "ref_id": { "type": "string" },
          "required": { "type": "boolean", "default": true }
        },
        "required": ["ref_type", "ref_id"]
      }
    },
    "output_spec": {
      "type": "object",
      "properties": {
        "output_type": {
          "type": "string",
          "enum": ["PARCEL", "CLAIM", "METRIC", "NONE"]
        },
        "output_schema_ref": { "type": ["string", "null"] },
        "output_parcel_target": { "type": ["string", "null"] }
      },
      "required": ["output_type"]
    },
    "compensation": {
      "type": ["object", "null"],
      "properties": {
        "strategy": {
          "type": "string",
          "enum": ["REVERSE_SETTLEMENT", "RE_DECOMPOSE", "ESCALATE",
                   "SAGA_ROLLBACK", "COMPENSATING_INTENT", "ABANDON", "NONE"],
          "description": "REVERSE_SETTLEMENT=undo settlement entries, RE_DECOMPOSE=retry with different strategy, ESCALATE=push to parent, SAGA_ROLLBACK=execute compensation intents in reverse, COMPENSATING_INTENT=execute specified compensation intent, ABANDON=mark as failed with no compensation, NONE=no compensation needed"
        },
        "compensation_intents": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Intent IDs to execute for SAGA_ROLLBACK or COMPENSATING_INTENT strategies"
        },
        "timeout_epochs": { "type": "integer", "description": "Maximum epochs allowed for compensation to complete" }
      }
    },
    "lifecycle_state": {
      "type": "string",
      "enum": ["PROPOSED", "DECOMPOSED", "ACTIVE", "COMPLETED", "DISSOLVED"],
      "description": "Current lifecycle state. Set to PROPOSED on creation."
    },
    "parent_intent_id": {
      "type": ["string", "null"],
      "description": "Null for root intents"
    },
    "child_intent_ids": {
      "type": "array",
      "items": { "type": "string" },
      "default": []
    },
    "provenance": {
      "type": ["object", "null"],
      "description": "W3C PROV compatible provenance record. Distinct from origin.provenance_chain (which tracks C4 claim IDs)."
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_epoch": { "type": "integer" },
        "last_modified_epoch": { "type": "integer" },
        "tags": { "type": "array", "items": { "type": "string" } },
        "annotations": {
          "type": "object",
          "additionalProperties": { "type": "string" }
        }
      }
    }
  },
  "required": ["intent_id", "intent_type", "origin", "scope",
               "description", "success_criteria", "resource_bounds",
               "constraints", "output_spec", "lifecycle_state"],

  "$defs": {
    "CausalStamp": {
      "type": "object",
      "properties": {
        "wall_time_ms": { "type": "integer" },
        "vector_clock": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "epoch": { "type": "integer" },
        "locus_id": { "type": "string" },
        "agent_id": { "type": "string" },
        "signature": {
          "type": "string",
          "description": "Ed25519 signature over (wall_time_ms, vector_clock, epoch, locus_id, agent_id)"
        }
      },
      "required": ["wall_time_ms", "vector_clock", "epoch",
                    "locus_id", "agent_id", "signature"]
    },
    "ResourceBounds": {
      "type": "object",
      "properties": {
        "compute_tokens": {
          "type": "integer", "minimum": 1,
          "description": "Maximum compute tokens (additive resource)"
        },
        "wall_time_ms": {
          "type": "integer", "minimum": 1,
          "description": "Maximum wall-clock time in milliseconds (additive resource)"
        },
        "bandwidth_bytes": {
          "type": "integer", "minimum": 0,
          "description": "Maximum network bandwidth in bytes (shared resource)"
        },
        "iops": {
          "type": "integer", "minimum": 0,
          "description": "Maximum I/O operations per second (shared resource)"
        },
        "storage_bytes": {
          "type": "integer", "minimum": 0,
          "description": "Maximum storage consumption in bytes (additive resource)"
        },
        "stake_required": {
          "type": "number", "minimum": 0,
          "description": "Minimum stake the executing agent must hold"
        }
      },
      "required": ["compute_tokens", "wall_time_ms"]
    },
    "SuccessPredicate": {
      "type": "object",
      "properties": {
        "predicate_id": { "type": "string" },
        "observable": {
          "type": "string",
          "description": "The metric or state observable to evaluate"
        },
        "operator": {
          "type": "string",
          "enum": ["EQ", "NEQ", "GT", "GTE", "LT", "LTE",
                   "CONTAINS", "MATCHES", "EXISTS"]
        },
        "expected_value": {},
        "expression": {
          "type": ["string", "null"],
          "description": "Optional machine-evaluable expression override. When present, takes precedence over observable+operator+expected_value."
        },
        "weight": {
          "type": "number", "minimum": 0, "maximum": 1, "default": 1.0,
          "description": "Weight for WEIGHTED_THRESHOLD aggregation"
        },
        "required": {
          "type": "boolean", "default": true,
          "description": "If true, this predicate must pass regardless of aggregation mode"
        },
        "description": { "type": "string" }
      },
      "required": ["predicate_id", "observable", "operator", "expected_value"]
    },
    "SuccessThreshold": {
      "type": "object",
      "properties": {
        "threshold_id": { "type": "string" },
        "metric": { "type": "string" },
        "operator": { "type": "string", "enum": ["GTE", "LTE"] },
        "value": { "type": "number" },
        "description": { "type": "string" }
      },
      "required": ["threshold_id", "metric", "operator", "value"]
    },
    "TemporalBound": {
      "type": "object",
      "properties": {
        "bound_type": {
          "type": "string",
          "enum": ["WITHIN_EPOCHS", "BEFORE_EPOCH", "AFTER_EPOCH"]
        },
        "epoch_value": { "type": "integer" },
        "description": { "type": "string" }
      },
      "required": ["bound_type", "epoch_value"]
    }
  }
}
```

### Formal Tuple Update

Replace the Section 5.1 tuple definition (line 452) with:

```
IQ = (id, type, class, origin, scope, description, content, authorization,
      criteria, bounds, constraints, strategy, inputs, output,
      compensation, lifecycle_state, parent_id, child_ids, provenance, metadata)
```

### Migration Notes

- Appendix A is redesignated as **non-normative reference**. The schema in Section 5.1 (as replaced by this patch) is the sole normative definition.
- The `composition` field (values `"AND"`, `"OR"`) in any existing intent quanta maps to `aggregation` as: `AND` -> `ALL_REQUIRED`, `OR` -> `ANY_REQUIRED`.
- The `max_compensation_epochs` field maps to `timeout_epochs`.
- The `network_bytes` field maps to `bandwidth_bytes`.
- The `decomposition_budget_tokens` field maps to `decomposition_token_limit`.

---

## PA-2: F48 — Strategy Selection Algorithm (MEDIUM)

### Problem

The `select_strategy()` function is called at line 1718 but never defined. The strategy selection table at lines 1752-1757 provides prose descriptions of when each strategy applies but no machine-evaluable decision rules.

### Normative Algorithm

Insert the following after line 1748 (after the `decompose_intent` function), replacing the prose table at lines 1750-1757:

```
FUNCTION select_strategy(intent: IntentQuantum) -> DecompositionStrategy:
    // ---------------------------------------------------------------
    // Step 0: Honor explicit proposer preference (Tier 3, A-02)
    // ---------------------------------------------------------------
    IF intent.decomposition_strategy != null:
        candidate = intent.decomposition_strategy
        IF validate_strategy_compatibility(intent, candidate):
            RETURN candidate
        // else: proposer preference is incompatible; fall through to auto-select

    // ---------------------------------------------------------------
    // Step 1: Classify by intent_type
    // ---------------------------------------------------------------
    MATCH intent.intent_type:

        CASE QUERY:
            // Queries are read-only. If multiple data sources, parallelize.
            // If single source or sequential dependency, use SEQUENTIAL.
            IF count_independent_data_sources(intent.scope) > 1:
                RETURN PARALLEL
            ELSE:
                RETURN SEQUENTIAL

        CASE DIRECTIVE:
            // Directives are specific instructions. Strategy depends on
            // whether sub-tasks are independent or ordered.
            GOTO step_2_structural_analysis

        CASE GOAL:
            // Goals are open-ended. Strategy depends on criteria structure
            // and available decomposition depth.
            GOTO step_2_structural_analysis

        CASE OPTIMIZATION:
            // Optimizations are System 4 proposals. Always CONDITIONAL
            // unless the optimization has been pre-decomposed by S4
            // into independent sub-tasks.
            IF intent.input_references contains ref_type == "EMA_QUANTUM":
                // EMA-driven optimization: conditional on metabolic phase
                RETURN CONDITIONAL
            ELSE:
                GOTO step_2_structural_analysis

    // ---------------------------------------------------------------
    // Step 2: Structural analysis of success criteria
    // ---------------------------------------------------------------
    step_2_structural_analysis:

    criteria = intent.success_criteria

    // 2a: If criteria have branching predicates (conditional evaluation),
    //     use CONDITIONAL strategy.
    IF criteria.criteria_type == "COMPOSITE"
       AND has_branching_predicates(criteria):
        // Branching = predicates where evaluation of one determines
        // whether others are relevant (mutually exclusive paths)
        RETURN CONDITIONAL

    // 2b: If criteria are conjunctive with independent sub-goals,
    //     use PARALLEL strategy.
    IF criteria.aggregation IN ["ALL_REQUIRED", "WEIGHTED_THRESHOLD"]
       AND all_predicates_are_independent(criteria.predicates):
        // Independent = no predicate's observable depends on another
        // predicate's output
        RETURN PARALLEL

    // 2c: If criteria require ordered evaluation (output chaining),
    //     use SEQUENTIAL strategy.
    IF has_output_chain_dependency(intent):
        // Output chain = child N's input_references include
        // INTENT_OUTPUT from child N-1
        RETURN SEQUENTIAL

    // ---------------------------------------------------------------
    // Step 3: Resource and depth heuristics
    // ---------------------------------------------------------------

    remaining_depth = intent.constraints.max_depth - current_depth(intent)

    // 3a: If remaining depth <= 2, prefer PARALLEL to minimize tree height
    IF remaining_depth <= 2:
        RETURN PARALLEL

    // 3b: If resource bounds are tight relative to estimated child count,
    //     prefer SEQUENTIAL (easier to reclaim unused resources)
    estimated_children = estimate_child_count(intent)
    per_child_compute = intent.resource_bounds.compute_tokens / estimated_children
    IF per_child_compute < 100:
        // Not enough tokens to parallelize safely
        RETURN SEQUENTIAL

    // ---------------------------------------------------------------
    // Step 4: Historical success rate lookup
    // ---------------------------------------------------------------
    history = memo_cache.get_strategy_stats(
        intent_type   = intent.intent_type,
        operation_class = intent.operation_class,
        domain        = intent.scope.domain
    )

    IF history != null AND history.sample_count >= 10:
        // Pick the strategy with the highest success rate,
        // weighted by recency (exponential decay, half-life = 50 epochs)
        best = history.best_strategy_by_weighted_success()
        IF best.success_rate >= 0.7:
            RETURN best.strategy

    // ---------------------------------------------------------------
    // Step 5: Default fallback by operation class
    // ---------------------------------------------------------------
    MATCH intent.operation_class:
        CASE G:     RETURN SEQUENTIAL   // Governance: ordered deliberation
        CASE V:     RETURN PARALLEL     // Verification: independent checks
        CASE X:     RETURN SEQUENTIAL   // Exclusive: serialize access
        CASE B:     RETURN PARALLEL     // Bounded: independent local ops
        CASE M:     RETURN PARALLEL     // Merge: parallel reads (though M is terminal)
        CASE null:  RETURN RECURSIVE    // Non-leaf, class not yet assigned

    // Should be unreachable
    RETURN RECURSIVE


FUNCTION validate_strategy_compatibility(intent: IntentQuantum,
                                          strategy: DecompositionStrategy) -> bool:
    // CONDITIONAL requires branching predicates in success criteria
    IF strategy == CONDITIONAL:
        RETURN has_branching_predicates(intent.success_criteria)

    // SEQUENTIAL requires at least 2 decomposable sub-tasks
    IF strategy == SEQUENTIAL:
        RETURN estimate_child_count(intent) >= 2

    // PARALLEL requires independent sub-goals
    IF strategy == PARALLEL:
        RETURN NOT has_output_chain_dependency(intent)

    // RECURSIVE is always valid
    RETURN true


FUNCTION has_branching_predicates(criteria: SuccessCriteria) -> bool:
    // Branching predicates: two or more predicates whose observables
    // are mutually exclusive (evaluating one makes the other irrelevant)
    IF criteria.predicates == null OR len(criteria.predicates) < 2:
        RETURN false
    // Check for predicates with complementary operators on the same observable
    observables = group_by(criteria.predicates, p -> p.observable)
    FOR obs, preds IN observables:
        IF len(preds) >= 2:
            operators = set(p.operator FOR p IN preds)
            IF ("GT" IN operators AND "LTE" IN operators)
               OR ("GTE" IN operators AND "LT" IN operators)
               OR ("EQ" IN operators AND "NEQ" IN operators):
                RETURN true
    RETURN false


FUNCTION has_output_chain_dependency(intent: IntentQuantum) -> bool:
    // True if any input_reference is of type INTENT_OUTPUT
    IF intent.input_references == null:
        RETURN false
    RETURN any(ref.ref_type == "INTENT_OUTPUT" FOR ref IN intent.input_references)


FUNCTION estimate_child_count(intent: IntentQuantum) -> int:
    // Heuristic: based on predicate count, scope breadth, and domain history
    base = max(len(intent.success_criteria.predicates OR []), 1)
    scope_factor = len(intent.scope.target_loci)
    RETURN max(base * scope_factor, 2)
```

### Strategy Selection Summary Table (updated)

| Strategy | Primary Selection Trigger | Fallback For | Failure Behavior |
|---|---|---|---|
| RECURSIVE | Default for unclassified non-leaf intents (null operation_class) | None | Partial success; evaluate combined results |
| PARALLEL | Independent conjunctive sub-goals; V/B/M-class defaults; depth <= 2 | Low depth budget | All-or-nothing by default; configurable partial threshold |
| SEQUENTIAL | Output chain dependency; G/X-class defaults; tight resource bounds | Ordered criteria | First failure halts pipeline; compensate completed steps |
| CONDITIONAL | Branching predicates; EMA-driven optimizations | Mutually exclusive paths | Selected branch fails => no fallback unless configured |

---

## PA-3: F49 — Operation Class Name Inconsistency (MEDIUM)

### Problem

The spec uses inconsistent names for operation classes B and X:
- **B** is called "Bounded" (Section 6.1, line 1052) and "Branch" (Appendix B, line 3697; Glossary, line 3875).
- **X** is called "Exclusive" (Section 6.1, line 1050) and "Cross-reference" (Appendix B, line 3696).

### Canonical Naming Table (aligned with C3 Tidal Noosphere)

| Code | Canonical Name | Canonical Long Form | Description |
|---|---|---|---|
| **M** | Merge | Merge/Convergence | Read-only merge operations |
| **B** | Bounded | Bounded Local Commit | Bounded local operations; near-atomic |
| **X** | Exclusive | Exclusive | Single-agent exclusive access |
| **V** | Verification | Verification | Cross-agent validation |
| **G** | Governance | Governance | Constitutional consensus |

### Location-by-Location Corrections

| Line | Current Text | Correction |
|---|---|---|
| 3696 | `X (Cross-reference)` | `X (Exclusive)` |
| 3697 | `B (Branch)` | `B (Bounded)` |
| 3875 | `One of M (Merge), B (Branch), X (Cross-reference), V (Verification), G (Governance)` | `One of M (Merge), B (Bounded), X (Exclusive), V (Verification), G (Governance)` |

These are the three locations where incorrect names appear. All other references in the spec (Section 6.1 lines 1046-1054, the decomposition matrix lines 1084-1091, and the abstract line 70) already use the correct canonical names.

### Verification

After applying these corrections, a full-text search for "Branch" should return zero hits in operation-class contexts, and a search for "Cross-reference" should return zero hits in operation-class contexts.

---

## PA-4: F50 — PBFT Variant Specification: HotStuff (MEDIUM)

### Problem

Section 10.2.2 (line 2621) specifies "PBFT" for GE consensus but does not name the specific BFT variant. Classic PBFT has O(n^2) message complexity per round (line 2649), which becomes a scalability bottleneck at higher replica counts (f=2 yields 49 messages/round, line 2643). The spec also references PBFT generically in 15+ locations without distinguishing between classic PBFT semantics and the actual protocol to be implemented.

### Specification: HotStuff BFT

The Global Executive SHALL use the **HotStuff** BFT consensus protocol (Yin et al., 2019). HotStuff is selected for the following properties:

1. **Linear message complexity:** O(n) messages per round (vs. O(n^2) for classic PBFT), achieved through threshold signatures aggregated by the leader.
2. **Pipelined phases:** HotStuff pipelines its three phases (PREPARE, PRE-COMMIT, COMMIT) such that a new proposal can begin before the previous one fully commits, increasing throughput.
3. **Optimistic responsiveness:** In the common case (honest leader, synchronous network), consensus completes in the time of actual message delays, not worst-case timeout bounds.
4. **Simple leader rotation:** Replaces PBFT's complex view-change protocol with a straightforward leader rotation after each decision (or on timeout).
5. **Safety under asynchrony:** Safety (no two honest replicas commit conflicting states) holds regardless of network timing assumptions.
6. **Liveness under partial synchrony:** Progress is guaranteed after GST (Global Stabilization Time) when the leader is honest — matches the partial synchrony model assumed by the Atrahasis stack.

### Revised GE Replication Configuration

Replace the configuration block at lines 2623-2631 with:

```
GE Replication Configuration:
  f                   = 1 (default; tolerates 1 Byzantine node)
  replicas            = 3f + 1 = 4
  consensus_protocol  = HotStuff (linear, pipelined)
  message_complexity  = O(n) per round (threshold signatures)
  leader_rotation     = Per tidal epoch, round-robin among GE seats
                        (fallback: on leader timeout = 2 * epoch_duration)
  liveness            = Guaranteed under partial synchrony with honest leader
  safety              = BFT: tolerates f < n/3 Byzantine replicas
  state_sync          = Merkle-diff, every 10 epochs
  checkpoint          = Every 50 epochs; 2 retained
  threshold_signature = BLS12-381 (n-of-n aggregation for O(n)->O(1) verification)
```

### Revised Throughput Model

Replace the throughput block at lines 2638-2650 with:

```
GE Throughput Budget:
  Target:     100 cross-locus intents per epoch
  Hard limit: 200 (backpressure above this)
  Per-intent: ~5ms routing decision + ~15ms HotStuff consensus round
  At f=1 (4 replicas): 4 messages per consensus round (O(n), leader collects)
  At f=2 (7 replicas): 7 messages per consensus round (O(n), leader collects)

Routing Decision for cross-locus intent:
  1. Read locus capability summaries     O(L)       L = target loci
  2. Select optimal locus assignment     O(L*logA)  A = agents
  3. Produce SpanningIntentStubs         O(L)
  4. Commit via HotStuff                 O(n)       n = replicas
```

### HotStuff Integration with C3 G-Class

The GE's HotStuff consensus IS the mechanism that implements C3's G-class governance operations at the cross-locus level:

```
FUNCTION ge_hotstuff_round(proposal: IntentQuantum | GovernanceVote) -> ConsensusResult:
    // HotStuff 3-phase pipeline (PREPARE -> PRE-COMMIT -> COMMIT)

    leader = ge_seats[current_epoch % len(ge_seats)]

    // Phase 1: PREPARE
    // Leader proposes; replicas validate and send partial threshold signatures
    prepare_msg = HotStuffMessage {
        type:      PREPARE,
        proposal:  proposal,
        view:      current_epoch,
        leader_id: leader.id,
        qc:        last_committed_qc    // quorum certificate from previous round
    }
    leader.broadcast(prepare_msg)
    prepare_votes = leader.collect_threshold_sigs(phase=PREPARE, quorum=2f+1)
    prepare_qc = aggregate_threshold_signatures(prepare_votes)

    // Phase 2: PRE-COMMIT
    // Leader sends prepare_qc; replicas lock on proposal
    precommit_msg = HotStuffMessage {
        type:      PRE_COMMIT,
        proposal:  proposal,
        view:      current_epoch,
        qc:        prepare_qc
    }
    leader.broadcast(precommit_msg)
    precommit_votes = leader.collect_threshold_sigs(phase=PRE_COMMIT, quorum=2f+1)
    precommit_qc = aggregate_threshold_signatures(precommit_votes)

    // Phase 3: COMMIT
    // Leader sends precommit_qc; replicas commit
    commit_msg = HotStuffMessage {
        type:      COMMIT,
        proposal:  proposal,
        view:      current_epoch,
        qc:        precommit_qc
    }
    leader.broadcast(commit_msg)
    commit_votes = leader.collect_threshold_sigs(phase=COMMIT, quorum=2f+1)
    commit_qc = aggregate_threshold_signatures(commit_votes)

    // Committed: apply to GE state
    ge_state.apply(proposal)

    RETURN ConsensusResult {
        status:    COMMITTED,
        qc:        commit_qc,
        epoch:     current_epoch,
        proposal:  proposal
    }


FUNCTION ge_leader_timeout_handler():
    // If leader fails to drive consensus within 2 * epoch_duration:
    //   1. Replicas increment view (epoch stays the same, view is logical)
    //   2. Next leader in round-robin takes over
    //   3. New leader includes highest QC it has seen (key HotStuff liveness property)
    //   4. No complex view-change sub-protocol (unlike classic PBFT)
    next_leader_idx = (current_leader_idx + 1) % len(ge_seats)
    new_view_msg = HotStuffMessage {
        type:      NEW_VIEW,
        view:      current_view + 1,
        leader_id: ge_seats[next_leader_idx].id,
        highest_qc: local_highest_qc
    }
    broadcast(new_view_msg)
```

### G-Class Mapping

```
C3 G-class governance operation
    |
    v
System 5 receives G-class intent (operation_class = G)
    |
    v
System 5 packages governance vote via GovernanceVoteRequest
    |
    v
GE routes to HotStuff consensus round (ge_hotstuff_round)
    |
    v
HotStuff commits with 2f+1 threshold signatures
    |
    v
Result returned to System 5 as VoteResult
    |
    v
System 5 applies governance outcome (relaxation, parameter change, etc.)
```

### Text Replacements

All occurrences of "PBFT" in the spec that refer to the GE's consensus protocol should be read as "HotStuff". Specifically:

| Line | Current | Replacement |
|---|---|---|
| 2621 | `using Practical Byzantine Fault Tolerance (PBFT)` | `using the HotStuff BFT consensus protocol` |
| 2627 | `consensus = PBFT` | `consensus_protocol = HotStuff (linear, pipelined)` |
| 2641 | `~50ms PBFT consensus round` | `~15ms HotStuff consensus round` |
| 2642 | `At f=1 (4 replicas): 16 messages per consensus round` | `At f=1 (4 replicas): 4 messages per consensus round` |
| 2643 | `At f=2 (7 replicas): 49 messages per consensus round` | `At f=2 (7 replicas): 7 messages per consensus round` |
| 2649 | `Commit via PBFT     O(n^2)     n = replicas` | `Commit via HotStuff     O(n)     n = replicas` |
| 3191 | `PBFT time: 200 * 50ms = 10s` | `HotStuff time: 200 * 15ms = 3s` |
| 3196 | `PBFT time: 400 * 50ms = 20s` | `HotStuff time: 400 * 15ms = 6s` |
| 3253 | `PBFT view change` | `HotStuff view change` |
| 3255 | `PBFT view change` | `HotStuff view change` |
| 3294 | `PBFT with 3f+1 replicas...` | `HotStuff with 3f+1 replicas (default f=1, 4 replicas). Safety: no two honest replicas commit conflicting states. Liveness: progress guaranteed with 2f+1 honest and reachable replicas and honest leader. Leader rotation every tidal epoch prevents long-lived Byzantine leaders.` |
| 3310 | `GE via PBFT view change` | `GE via HotStuff view change` |
| 3431 | `regional PBFT + cross-region federation` | `regional HotStuff + cross-region federation` |
| 3512 | `The PBFT model assumes bounded network delay` | `The HotStuff model assumes eventual synchrony (partial synchrony)` |
| 3828 | `PBFT replica count (3f+1)` | `HotStuff replica count (3f+1)` |
| 3877 | `PBFT | Practical Byzantine Fault Tolerance; consensus protocol...` | `HotStuff | HotStuff BFT consensus protocol (Yin et al., 2019); linear message complexity O(n), pipelined 3-phase commit, tolerating f Byzantine nodes with 3f+1 replicas` |

Note: Lines 3338 and 3346 reference "no BFT" and "BFT: DISABLED" for small-scale configurations. These are not PBFT-specific and remain unchanged. Line 3358 references "4 replicas, f=1 BFT" generically and also remains unchanged. Line 3396 references "GE f=2, FD f=1 per locus" generically and remains unchanged.

---

## PA-5: F51 — Shared Resource Contention Protocol (MEDIUM)

### Problem

When multiple intents target the same shared resource (same agent, same capacity slice, same parcel), contention management is unspecified. The ISR tracks intent state but has no resource reservation mechanism. The Agent Registry tracks capability but not current assignment load.

### Shared Resource Contention Protocol

#### 5.1 Contention Detection

The Intent State Registry is extended with a resource reservation index:

```
ISR Extension: ResourceReservationIndex

STRUCTURE ResourceReservation:
    resource_id:     string          // agent_id, parcel_id, or capacity_slice_id
    resource_type:   enum { AGENT, PARCEL, CAPACITY_SLICE }
    intent_id:       string          // the intent holding this reservation
    operation_class: enum { M, B, X, V, G }
    priority:        int             // from intent.constraints.priority
    deadline_epoch:  int | null      // from intent.constraints.deadline_epoch
    reserved_epoch:  int             // epoch when reservation was made
    expiry_epoch:    int             // reserved_epoch + 2 * TIDAL_EPOCH_DURATION

// ISR maintains a map: resource_id -> List[ResourceReservation]
// sorted by (operation_class rank DESC, deadline_epoch ASC, intent_id ASC)
```

Detection is triggered whenever a new leaf intent is assigned to an agent or parcel:

```
FUNCTION detect_contention(new_intent: IntentQuantum,
                           target_resource_id: string,
                           resource_type: ResourceType) -> ContentionResult:

    existing = isr.resource_index.get(target_resource_id)
    IF existing == null OR len(existing) == 0:
        RETURN ContentionResult { contended: false }

    // Check for exclusive access conflict
    IF resource_type == AGENT:
        active_count = count(r FOR r IN existing
                             IF r.intent_id != new_intent.intent_id
                             AND isr.get_state(r.intent_id) == ACTIVE)
        IF active_count > 0 AND new_intent.scope.requires_exclusive_access:
            RETURN ContentionResult {
                contended: true,
                reason: EXCLUSIVE_CONFLICT,
                blocking_intents: [r.intent_id FOR r IN existing IF active]
            }

    // Check for capacity overload
    IF resource_type == AGENT:
        concurrent_leaves = count(r FOR r IN existing
                                  IF isr.get_state(r.intent_id) IN [ACTIVE, DECOMPOSED])
        IF concurrent_leaves >= MAX_CONCURRENT_LEAVES:  // default: 3
            RETURN ContentionResult {
                contended: true,
                reason: CAPACITY_OVERLOAD,
                blocking_intents: [r.intent_id FOR r IN existing],
                queue_position: concurrent_leaves - MAX_CONCURRENT_LEAVES + 1
            }

    RETURN ContentionResult { contended: false }
```

#### 5.2 Contention Resolution

Resolution follows a strict priority ordering:

```
FUNCTION resolve_contention(new_intent: IntentQuantum,
                            contention: ContentionResult,
                            target_resource_id: string) -> ResolutionAction:

    new_rank = class_rank(new_intent.operation_class)
    new_priority = new_intent.constraints.priority
    new_deadline = new_intent.constraints.deadline_epoch

    // Rule 1: Higher operation class wins
    FOR blocker_id IN contention.blocking_intents:
        blocker = isr.get_intent(blocker_id)
        blocker_rank = class_rank(blocker.operation_class)

        IF new_rank > blocker_rank:
            // New intent has higher operation class -> preempt blocker
            RETURN ResolutionAction {
                action: PREEMPT,
                preempt_intent_id: blocker_id,
                reason: "operation_class " + new_intent.operation_class +
                        " > " + blocker.operation_class
            }

    // Rule 2: Within same operation class, earlier deadline wins
    same_class_blockers = [b FOR b IN contention.blocking_intents
                           IF class_rank(isr.get_intent(b).operation_class) == new_rank]

    FOR blocker_id IN same_class_blockers:
        blocker = isr.get_intent(blocker_id)
        IF new_deadline != null AND blocker.constraints.deadline_epoch != null:
            IF new_deadline < blocker.constraints.deadline_epoch:
                RETURN ResolutionAction {
                    action: PREEMPT,
                    preempt_intent_id: blocker_id,
                    reason: "deadline " + str(new_deadline) +
                            " < " + str(blocker.constraints.deadline_epoch)
                }
        // If new has a deadline and blocker does not, new wins
        IF new_deadline != null AND blocker.constraints.deadline_epoch == null:
            RETURN ResolutionAction {
                action: PREEMPT,
                preempt_intent_id: blocker_id,
                reason: "deadline-bearing intent takes priority over open-ended"
            }

    // Rule 3: Tie-break by intent_id hash (deterministic, no favoritism)
    // Lower hash wins (arbitrary but consistent across all nodes)
    FOR blocker_id IN same_class_blockers:
        IF hash(new_intent.intent_id) < hash(blocker_id):
            RETURN ResolutionAction {
                action: PREEMPT,
                preempt_intent_id: blocker_id,
                reason: "hash tie-break"
            }

    // New intent loses all comparisons -> queue it
    RETURN ResolutionAction {
        action: QUEUE,
        queue_position: contention.queue_position,
        estimated_wait_epochs: estimate_wait(contention.blocking_intents)
    }
```

#### 5.3 Backpressure Mechanism

```
CONSTANT MAX_CONCURRENT_LEAVES = 3    // per agent
CONSTANT QUEUE_EXPIRY_EPOCHS   = 2    // in tidal epochs

FUNCTION apply_backpressure(agent_id: string,
                            new_intent: IntentQuantum) -> BackpressureResult:

    reservations = isr.resource_index.get(agent_id)
    active_leaves = count(r FOR r IN reservations
                          IF isr.get_state(r.intent_id) IN [ACTIVE]
                          AND r.resource_type == AGENT)

    IF active_leaves < MAX_CONCURRENT_LEAVES:
        // No backpressure needed; assign immediately
        isr.resource_index.add(agent_id, ResourceReservation {
            resource_id:     agent_id,
            resource_type:   AGENT,
            intent_id:       new_intent.intent_id,
            operation_class: new_intent.operation_class,
            priority:        new_intent.constraints.priority,
            deadline_epoch:  new_intent.constraints.deadline_epoch,
            reserved_epoch:  current_epoch(),
            expiry_epoch:    current_epoch() + QUEUE_EXPIRY_EPOCHS
        })
        RETURN BackpressureResult { action: ASSIGN_NOW }

    // Agent is at capacity. Queue the intent.
    queue_entry = QueueEntry {
        intent_id:    new_intent.intent_id,
        agent_id:     agent_id,
        queued_epoch: current_epoch(),
        expiry_epoch: current_epoch() + QUEUE_EXPIRY_EPOCHS
    }
    isr.assignment_queue.enqueue(agent_id, queue_entry)

    RETURN BackpressureResult {
        action:               QUEUED,
        queue_position:       isr.assignment_queue.depth(agent_id),
        expiry_epoch:         queue_entry.expiry_epoch,
        estimated_wait_epochs: estimate_wait_from_queue(agent_id)
    }


FUNCTION process_assignment_queue(agent_id: string):
    // Called when an agent completes a leaf intent (ACTIVE -> COMPLETED/DISSOLVED)
    // or when a reservation expires.

    // 1. Remove completed/expired reservations
    isr.resource_index.remove_if(agent_id,
        r -> isr.get_state(r.intent_id) IN [COMPLETED, DISSOLVED]
             OR r.expiry_epoch <= current_epoch())

    // 2. Process queue
    WHILE isr.resource_index.active_count(agent_id) < MAX_CONCURRENT_LEAVES:
        next = isr.assignment_queue.dequeue(agent_id)
        IF next == null:
            BREAK   // queue empty

        // Check expiry
        IF next.expiry_epoch <= current_epoch():
            // Expired: transition intent to DISSOLVED with reason QUEUE_TIMEOUT
            isr.transition_intent(next.intent_id, DISSOLVED, "QUEUE_TIMEOUT")
            // Trigger compensation at parent
            parent_id = isr.get_intent(next.intent_id).parent_intent_id
            IF parent_id != null:
                notify_parent_of_child_failure(parent_id, next.intent_id,
                                                "QUEUE_TIMEOUT")
            CONTINUE

        // Assign
        isr.resource_index.add(agent_id, ResourceReservation {
            resource_id:     agent_id,
            resource_type:   AGENT,
            intent_id:       next.intent_id,
            operation_class: isr.get_intent(next.intent_id).operation_class,
            priority:        isr.get_intent(next.intent_id).constraints.priority,
            deadline_epoch:  isr.get_intent(next.intent_id).constraints.deadline_epoch,
            reserved_epoch:  current_epoch(),
            expiry_epoch:    current_epoch() + QUEUE_EXPIRY_EPOCHS
        })
        pe_execute_intent(isr.get_intent(next.intent_id),
                          agent_registry.get(agent_id))
```

#### 5.4 Configuration Parameters

Add to Appendix E (Parameter Reference):

| Parameter | Default | Range | Location | Description |
|---|---|---|---|---|
| MAX_CONCURRENT_LEAVES | 3 | 2-5 | Agent Registry / ISR | Max concurrent leaf intents per agent |
| QUEUE_EXPIRY_EPOCHS | 2 | 1-5 | ISR | Tidal epochs before queued assignment expires |

#### 5.5 Integration Points

- **Agent Registry:** Extended with `current_assignment_count` field, updated by ISR on reservation add/remove.
- **Failure Detector:** QUEUE_TIMEOUT dissolution events are reported to the Failure Detector for agent health tracking. An agent that consistently causes queue timeouts (> 5 in 10 epochs) triggers a liveness investigation.
- **System 3 Performance Monitor:** Contention rate (contentions per epoch per locus) is added as a performance metric. If contention rate exceeds 20% of leaf assignments, System 4 is notified for capacity planning.
- **Decomposition Engine:** The `select_agent()` function (called at line 1713) must consult the resource reservation index before assignment:

```
FUNCTION select_agent(operation_class, domain, resource_bounds) -> AgentRecord | null:
    candidates = agent_registry.query_capable_agents(
        operation_class = operation_class,
        domain          = domain,
        min_capacity    = resource_bounds.compute_tokens
    )

    // Filter by contention: prefer agents with available capacity
    candidates = sort(candidates, key = c -> (
        isr.resource_index.active_count(c.agent_id),   // fewer assignments first
        -c.credibility_score                             // higher credibility second
    ))

    FOR candidate IN candidates:
        contention = detect_contention(
            current_intent, candidate.agent_id, AGENT)
        IF NOT contention.contended:
            RETURN candidate

    // All candidates contended; return least-loaded candidate
    // (backpressure will queue it)
    IF len(candidates) > 0:
        RETURN candidates[0]

    RETURN null
```

---

## PA-6: E-C7-01 — Settlement Router Target Correction

### Problem

Per C9 erratum E-C7-01, the Settlement Router references "C3 settlement ledger" throughout the spec. The correct target is "C8 DSF settlement ledger, accessed via C3's CRDT replication infrastructure."

### Corrections

| Line | Current Text | Corrected Text |
|---|---|---|
| 333 | `C3 settlement ledger` | `C8 DSF settlement ledger (via C3 CRDT infrastructure)` |
| 1571 | `C3's settlement ledger` | `C8 DSF's settlement ledger (accessed via C3's CRDT replication infrastructure)` |
| 1601 | `its C3 settlement ledger partition` | `its C8 DSF settlement ledger partition (via C3 CRDT infrastructure)` |
| 1604 | `C3 ledger rejects duplicate` | `C8 DSF ledger rejects duplicate` |
| 1611 | `C3 rejects duplicate settlement_id` | `C8 DSF rejects duplicate settlement_id` |
| 2023 | `the C3 settlement ledger` | `the C8 DSF settlement ledger` |
| 2302 | `a settlement entry in C3 ledger` | `a settlement entry in C8 DSF ledger` |
| 3050 | `the C3 settlement ledger atomically` | `the C8 DSF settlement ledger atomically (via C3 CRDT infrastructure)` |
| 3882 | `forwards intent cost accounting to C3's settlement ledger` | `forwards intent cost accounting to C8 DSF's settlement ledger (via C3 CRDT infrastructure)` |

Additionally, the integration table at line 363 should be updated:

| Line | Current | Corrected |
|---|---|---|
| 363 (C3 row, "RIF Writes" column) | `settlement entries` | `leaf intent execution requests` (remove settlement entries from C3 row) |
| (new row) | — | Add row: `C8 DSF | Settlement ledger partition per locus | Settlement entries (via Settlement Router) | Settlement confirmation, idempotency enforcement` |

### Glossary Addition

Add to Appendix F (Glossary):

| Term | Definition |
|---|---|
| DSF | Distributed Settlement Fabric (C8); settlement ledger and accounting infrastructure. Settlement Router forwards to DSF via C3's CRDT replication layer. |

---

## Summary of Changes

| Patch | Finding | Severity | Lines Affected | Nature |
|---|---|---|---|---|
| PA-1 | F47 | HIGH | §5.1 (447-712), Appendix A (3536-3685) | Schema unification; 37 conflicts resolved |
| PA-2 | F48 | MEDIUM | After line 1748 | New: `select_strategy()` algorithm (~100 lines pseudocode) |
| PA-3 | F49 | MEDIUM | Lines 3696, 3697, 3875 | Three name corrections |
| PA-4 | F50 | MEDIUM | Lines 2621-2650, 3191-3196, 3253-3294, 3310, 3431, 3512, 3828, 3877 | PBFT -> HotStuff; revised message complexity; consensus pseudocode |
| PA-5 | F51 | MEDIUM | New subsection in §7.3; update §10.3.3 | Contention protocol: detection, resolution, backpressure (~150 lines pseudocode) |
| PA-6 | E-C7-01 | ERRATA | 9 line corrections + 1 new integration table row + 1 glossary entry | Settlement Router -> C8 DSF |

---

*End of Patch Addendum F47-F51*
