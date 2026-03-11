

# C7 — Recursive Intent Fabric (RIF)

## Architecture Document — Part 1 (Sections 1–6)

---

## 1. Executive Summary

### 1.1 What RIF Replaces

The Coordinated Intent Orchestration System (CIOS) proposed in early Atrahasis design sketches provided a flat, single-layer intent dispatch model. CIOS assumed homogeneous agents, ignored causal ordering across loci, lacked formal decomposition semantics, and offered no governance integration. It could not answer three fundamental questions:

1. How does a high-level goal become concrete work assignments?
2. How does the system guarantee that decomposition terminates?
3. How does governance constrain what intents the system may pursue?

RIF answers all three.

### 1.2 Why RIF Exists

Planetary-scale AI coordination requires an orchestration layer that is:

- **Recursive**: Goals decompose into sub-goals, sub-goals into tasks, tasks into leaf operations — with formal termination guarantees.
- **Intent-native**: The fundamental unit of work is not a message or a transaction but an *intent quantum* — a self-describing goal with success criteria, resource bounds, and provenance.
- **Two-plane**: Operational state (agents, clocks, intent registries) lives in a Domain-Scoped State Plane replicated per-locus. Strategic and governance functions live in an Executive Plane modeled on Stafford Beer's Viable System Model (Systems 3/4/5).
- **Substrate-aware**: RIF does not reinvent scheduling, settlement, credibility, or knowledge metabolism. It delegates to C3 (Tidal Noosphere), C4 (ASV), C5 (PCVM), and C6 (EMA) respectively.

### 1.3 Key Innovations

| Innovation | Description |
|---|---|
| Intent Quantum | Self-describing work unit with lifecycle, success criteria, resource bounds, and provenance chain |
| Formal Decomposition Algebra | Operation-class-aware decomposition with proven termination and cycle-freedom |
| Two-Plane Separation | Domain state replicates per-locus; executive functions span loci with minimal cross-locus traffic |
| VSM-Aligned Executive | System 3 (operational), System 4 (strategic), System 5 (governance) map cleanly onto C3 operation classes |
| Memoized Decomposition | Cache prior decomposition plans keyed on (intent_type, scope, context_hash), delta-adjust on reuse |
| Resource Bound Preservation | Formal proof that child intents cannot exceed parent resource envelopes |

### 1.4 Architecture Summary

RIF comprises two planes:

**Domain-Scoped State Plane** — Five components replicated within each C3 locus:
Agent Registry, Clock Service, Intent State Registry, Settlement Router, Failure Detector.

**Executive Plane** — Three systems spanning loci as needed:
System 3 (Operational Control), System 4 (Strategic Intelligence), System 5 (G-Class Governance).

An intent enters the system as a PROPOSED quantum. System 3 decomposes it into a tree of child intents. Leaf intents map to C3 operation classes (M/B/X/V/G) and execute within tidal epochs. Results propagate upward through the tree. System 4 observes trends and proposes adaptations. System 5 arbitrates conflicts and enforces constitutional constraints.

---

## 2. Architecture Overview

### 2.1 Two-Plane Architecture Diagram

```
+=========================================================================+
|                        EXECUTIVE PLANE                                  |
|                                                                         |
|  +-------------------+  +---------------------+  +------------------+  |
|  |    SYSTEM 5        |  |     SYSTEM 4         |  |    SYSTEM 3       |  |
|  |  G-Class           |  |  Strategic            |  |  Operational      |  |
|  |  Governance        |  |  Intelligence         |  |  Control          |  |
|  |                   |  |                       |  |                  |  |
|  | - Constitutional  |  | - Horizon Scanning    |  | - Intent Decomp  |  |
|  |   consensus       |  | - Anticipatory        |  | - Resource Opt   |  |
|  | - Conflict        |  |   capacity planning   |  | - Perf Monitor   |  |
|  |   resolution      |  | - Adaptation          |  | - Failure Play   |  |
|  | - Sovereignty     |  |   proposals           |  | - Compensation   |  |
|  |   relaxation      |  | - Oscillation         |  | - Decomp Memo    |  |
|  | - Emergency       |  |   dampening           |  |                  |  |
|  |   rollback        |  |                       |  |                  |  |
|  +--------+----------+  +----------+------------+  +--------+---------+  |
|           |                        |                         |           |
|           |    S5 arbitrates       |   S4 proposes           |           |
|           +<-----------------------+                         |           |
|           |                        +<------------------------+           |
|           |    S5 constrains S3    |   S3 reports to S4      |           |
|           +------------------------------------------------>+           |
|                                                                         |
+=====+=====================+===================+=================+=======+
      |                     |                   |                 |
      | G-class ops         | V-class verify    | X/B/M execute   | Events
      v                     v                   v                 v
+=========================================================================+
|                   DOMAIN-SCOPED STATE PLANE                             |
|                        (per-locus)                                      |
|                                                                         |
|  +---------------+  +-----------+  +--------+  +---------+  +--------+ |
|  | Agent         |  | Clock     |  | Intent |  | Settle- |  | Failure| |
|  | Registry      |  | Service   |  | State  |  | ment    |  | Detect-| |
|  | (CRDT)        |  | (NTP +    |  | Regis- |  | Router  |  | or     | |
|  |               |  |  Vector)  |  | try    |  | (ALO)   |  | (Sent.)| |
|  +-------+-------+  +-----+-----+  +---+----+  +----+----+  +---+----+ |
|          |               |             |            |            |      |
+=========================================================================+
           |               |             |            |            |
           v               v             v            v            v
+=========================================================================+
|                     SUBSTRATE LAYER                                     |
|                                                                         |
|  +------------------+  +--------+  +----------+  +------------------+  |
|  | C3 Tidal         |  | C4 ASV |  | C5 PCVM  |  | C6 EMA           |  |
|  | Noosphere        |  |        |  |          |  |                  |  |
|  | (loci, parcels,  |  |(claims,|  |(VTDs,    |  |(epistemic quanta,|  |
|  |  tidal sched,    |  | evid., |  | MCTs,    |  | metabolic life-  |  |
|  |  VRF, M/B/X/V/G) |  | prov.) |  | cred.)   |  | cycle, SHREC)    |  |
|  +------------------+  +--------+  +----------+  +------------------+  |
|                                                                         |
+=========================================================================+
```

### 2.2 Component Inventory

| Component | Plane | Scope | Replication | Primary Substrate |
|---|---|---|---|---|
| Agent Registry | Domain State | Per-locus | CRDT (intra-locus full, cross-locus summary) | C3 parcels |
| Clock Service | Domain State | Per-locus + federation | NTP + vector clocks | C3 epoch timing |
| Intent State Registry (ISR) | Domain State | Per-locus (spanning for cross-locus) | CRDT with 5% bandwidth cap | C4 provenance |
| Settlement Router | Domain State | Per-locus | At-least-once broker | C3 settlement ledger |
| Failure Detector | Domain State | Per-locus | Sentinel-integrated | C5 credibility |
| System 3 — Operational Control | Executive | Cross-locus | Leader per intent tree | C3 operation classes |
| System 4 — Strategic Intelligence | Executive | Global (read-only) | Stateless observers | C6 EMA projections |
| System 5 — G-Class Governance | Executive | Global | C3 G-class consensus | C3 constitutional consensus |

### 2.3 Intent Data Flow

```
                          EXTERNAL
                          REQUEST
                             |
                             v
                    +------------------+
                    |  Intent Proposal |
                    |  (PROPOSED)      |
                    +--------+---------+
                             |
                    validate & admit
                             |
                             v
                    +------------------+
                    |  System 3:       |
                    |  Decomposition   |
                    |  Engine          |
                    +--------+---------+
                             |
              decompose into child intents
                             |
               +-------------+-------------+
               |             |             |
               v             v             v
          +---------+   +---------+   +---------+
          | Child 1 |   | Child 2 |   | Child 3 |
          | (DECOMP)|   | (DECOMP)|   | (DECOMP)|
          +----+----+   +----+----+   +----+----+
               |             |             |
          further decomp     |        leaf (M-class)
          if needed          |             |
               |             v             v
               |        leaf (B-class) +--------+
               v             |         | ACTIVE |
          +---------+        v         +---+----+
          | Sub-    |   +--------+         |
          | children|   | ACTIVE |     execute via
          +---------+   +---+----+     C3 scheduler
               |            |             |
               v            v             v
          all children  settle via    result parcel
          complete      C3 ledger     written
               |            |             |
               +------+-----+------+------+
                      |            |
                      v            v
               +------------------+
               |  Parent intent   |
               |  evaluates       |
               |  success criteria|
               +--------+---------+
                         |
                    criteria met?
                    /           \
                  yes            no
                  /               \
                 v                 v
          +----------+     +-------------+
          |COMPLETED |     | Compensate  |
          +----+-----+     | or re-decomp|
               |           +-------------+
               v
          +-----------+
          | DISSOLVED |
          | (GC after |
          |  100 ep.) |
          +-----------+
```

### 2.4 Integration Points

| Substrate | RIF Reads | RIF Writes | Integration Mechanism |
|---|---|---|---|
| C3 Tidal Noosphere | Locus topology, parcel state, epoch boundaries, VRF outputs, operation class definitions | Leaf intent execution requests, settlement entries | Leaf intents map to M/B/X/V/G operations scheduled within tidal epochs |
| C4 ASV | Claim schemas, evidence structures, provenance chains | Intent success/failure claims, decomposition provenance | Intent outcomes expressed as ASV claims with confidence and evidence |
| C5 PCVM | Agent credibility scores (VTDs, MCTs), claim class assessments | Intent outcome verification requests | Failure Detector uses PCVM credibility to weight liveness reports; Byzantine agent detection |
| C6 EMA | Epistemic quanta projections, SHREC regulation state, coherence trends | None (read-only) | System 4 reads EMA projections for horizon scanning; volatility discounting |

---

## 3. Domain-Scoped State Plane

### 3.1 Agent Registry

#### 3.1.1 Purpose

The Agent Registry maintains the authoritative mapping of agents to their capabilities, cryptographic identities, stake positions, reputation scores, and locus assignments. It is the foundation for all intent assignment decisions — System 3 cannot assign a leaf intent to an agent whose capabilities do not match the required operation class.

#### 3.1.2 Data Structures

```json
{
  "$schema": "https://atrahasis.org/rif/agent-registry/v1",
  "type": "object",
  "properties": {
    "agent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Globally unique agent identifier"
    },
    "pubkey": {
      "type": "string",
      "format": "ed25519-public-key",
      "description": "Ed25519 public key for identity verification"
    },
    "capabilities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "operation_class": {
            "type": "string",
            "enum": ["M", "B", "X", "V", "G"]
          },
          "domain": {
            "type": "string",
            "description": "Capability domain (e.g., 'inference', 'storage', 'verification')"
          },
          "capacity": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Normalized capacity [0,1] for this capability"
          },
          "attested_epoch": {
            "type": "integer",
            "description": "Epoch at which capability was last attested"
          }
        },
        "required": ["operation_class", "domain", "capacity", "attested_epoch"]
      }
    },
    "stake": {
      "type": "object",
      "properties": {
        "amount": {
          "type": "number",
          "minimum": 0,
          "description": "Staked collateral amount"
        },
        "locked_until_epoch": {
          "type": "integer",
          "description": "Epoch until which stake is locked"
        }
      },
      "required": ["amount", "locked_until_epoch"]
    },
    "reputation": {
      "type": "object",
      "properties": {
        "composite_score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "PCVM-derived composite reputation"
        },
        "intent_completion_rate": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "last_failure_epoch": {
          "type": ["integer", "null"]
        },
        "total_intents_completed": {
          "type": "integer",
          "minimum": 0
        }
      },
      "required": ["composite_score", "intent_completion_rate",
                    "last_failure_epoch", "total_intents_completed"]
    },
    "locus_id": {
      "type": "string",
      "description": "C3 locus to which this agent is currently assigned"
    },
    "parcel_id": {
      "type": "string",
      "description": "C3 parcel within the locus"
    },
    "status": {
      "type": "string",
      "enum": ["ACTIVE", "SUSPENDED", "DRAINING", "DEPARTED"]
    },
    "last_heartbeat_epoch": {
      "type": "integer"
    },
    "version_vector": {
      "type": "object",
      "additionalProperties": { "type": "integer" },
      "description": "CRDT version vector for conflict resolution"
    }
  },
  "required": ["agent_id", "pubkey", "capabilities", "stake",
               "reputation", "locus_id", "parcel_id", "status",
               "last_heartbeat_epoch", "version_vector"]
}
```

**Cross-locus capability summary** (the only structure that replicates beyond locus boundaries):

```json
{
  "$schema": "https://atrahasis.org/rif/agent-capability-summary/v1",
  "type": "object",
  "properties": {
    "locus_id": { "type": "string" },
    "summary_epoch": { "type": "integer" },
    "agent_count": { "type": "integer" },
    "aggregate_capabilities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "operation_class": {
            "type": "string",
            "enum": ["M", "B", "X", "V", "G"]
          },
          "domain": { "type": "string" },
          "total_capacity": { "type": "number" },
          "available_capacity": { "type": "number" }
        },
        "required": ["operation_class", "domain",
                     "total_capacity", "available_capacity"]
      }
    },
    "digest": {
      "type": "string",
      "format": "sha256",
      "description": "Hash of full registry state for consistency checks"
    }
  },
  "required": ["locus_id", "summary_epoch", "agent_count",
               "aggregate_capabilities", "digest"]
}
```

#### 3.1.3 Replication Model

- **Intra-locus**: Full state CRDT replication using Last-Writer-Wins Register for scalar fields and Observed-Remove Set for capabilities list. Convergence guaranteed within 2 tidal epochs under normal conditions.
- **Cross-locus**: Only `AgentCapabilitySummary` objects replicate. Summaries are computed once per epoch by the locus coordinator and broadcast via C3 parcel gossip. Stale summaries (older than 10 epochs) are discarded by receivers.
- **Bandwidth budget**: Agent Registry CRDT traffic must not exceed 2% of locus network capacity. If exceeded, replication frequency halves until budget is met.

#### 3.1.4 Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| Agent crash | Heartbeat timeout (3 consecutive epochs) | Status → SUSPENDED; reassign active intents |
| CRDT divergence | Digest mismatch on periodic audit (every 10 epochs) | Full state reconciliation from locus coordinator |
| Byzantine agent | PCVM credibility drop below 0.3 | Status → SUSPENDED; stake slashing proposal to System 5 |
| Locus partition | No cross-locus summary received for 5 epochs | Mark locus as PARTITIONED; freeze cross-locus intent assignment to that locus |

#### 3.1.5 Integration Contracts

- **To System 3**: `query_capable_agents(operation_class, domain, min_capacity) → List[AgentId]`
- **To Failure Detector**: `report_agent_liveness(agent_id, epoch, alive: bool)`
- **To C3**: `sync_locus_assignment(agent_id, locus_id, parcel_id)` — called when C3 tidal rebalancing moves an agent
- **To C5 PCVM**: `refresh_reputation(agent_id) → ReputationScore` — called once per epoch per active agent

---

### 3.2 Clock Service

#### 3.2.1 Purpose

The Clock Service provides a shared notion of time across agents within a locus and a causally consistent ordering of events across loci. RIF needs both wall-clock time (for decomposition budgets, TTLs, and epoch alignment) and causal ordering (for intent state transitions that must respect happens-before relationships).

#### 3.2.2 Data Structures

```json
{
  "$schema": "https://atrahasis.org/rif/clock-service/v1",
  "type": "object",
  "properties": {
    "locus_id": { "type": "string" },
    "wall_clock": {
      "type": "object",
      "properties": {
        "timestamp_ms": {
          "type": "integer",
          "description": "Milliseconds since Unix epoch"
        },
        "uncertainty_ms": {
          "type": "integer",
          "minimum": 0,
          "maximum": 500,
          "description": "Clock uncertainty bound in ms"
        },
        "ntp_stratum": {
          "type": "integer",
          "minimum": 1,
          "maximum": 15
        },
        "last_sync_epoch": {
          "type": "integer"
        }
      },
      "required": ["timestamp_ms", "uncertainty_ms",
                    "ntp_stratum", "last_sync_epoch"]
    },
    "vector_clock": {
      "type": "object",
      "additionalProperties": { "type": "integer" },
      "description": "Map of locus_id → logical timestamp"
    },
    "epoch_info": {
      "type": "object",
      "properties": {
        "current_epoch": { "type": "integer" },
        "epoch_start_ms": { "type": "integer" },
        "epoch_duration_ms": { "type": "integer" },
        "tidal_phase": {
          "type": "string",
          "enum": ["RISING", "HIGH", "FALLING", "LOW"]
        }
      },
      "required": ["current_epoch", "epoch_start_ms",
                    "epoch_duration_ms", "tidal_phase"]
    }
  },
  "required": ["locus_id", "wall_clock", "vector_clock", "epoch_info"]
}
```

**Causal event stamp** (attached to every intent state transition):

```json
{
  "$schema": "https://atrahasis.org/rif/causal-stamp/v1",
  "type": "object",
  "properties": {
    "wall_time_ms": { "type": "integer" },
    "vector_clock": {
      "type": "object",
      "additionalProperties": { "type": "integer" }
    },
    "epoch": { "type": "integer" },
    "locus_id": { "type": "string" },
    "agent_id": { "type": "string" }
  },
  "required": ["wall_time_ms", "vector_clock", "epoch",
               "locus_id", "agent_id"]
}
```

#### 3.2.3 Replication Model

- **Intra-locus NTP federation**: Each locus elects a stratum-1 time source (or federates with an external NTP server). Agents within the locus synchronize to stratum-2 with ±500ms maximum tolerated skew.
- **Cross-locus vector clocks**: Vector clocks piggyback on all cross-locus messages. Each locus maintains a vector clock entry for every locus it has communicated with in the last 100 epochs. Entries older than 100 epochs are pruned.
- **Epoch alignment**: All loci share the same epoch numbering derived from C3 tidal scheduling. Epoch boundaries are authoritative from C3; the Clock Service merely tracks them.

#### 3.2.4 Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| NTP source failure | Stratum increase or sync timeout | Fallback to secondary NTP source; if none available, enter DEGRADED mode (widen uncertainty to ±2000ms) |
| Clock skew exceeds ±500ms | Periodic skew measurement against locus peers | Agent excluded from intent assignment until resynchronized |
| Network partition | Vector clock entries stop advancing for remote locus | Mark affected locus as PARTITIONED in vector clock metadata; freeze non-local intent processing for that locus |
| Epoch desynchronization | Local epoch counter diverges from C3 authoritative epoch | Hard reset to C3 epoch; invalidate all pending wall-clock deadlines |

#### 3.2.5 Integration Contracts

- **To ISR**: `stamp_transition(intent_id, transition) → CausalStamp`
- **To System 3**: `current_epoch() → EpochInfo`
- **To System 3**: `is_within_budget(start_stamp, budget_ms) → bool`
- **To C3**: `sync_epoch_boundary(epoch, start_ms, duration_ms)` — called by C3 at each epoch boundary
- **To Failure Detector**: `report_clock_anomaly(agent_id, skew_ms)`

---

### 3.3 Intent State Registry (ISR)

#### 3.3.1 Purpose

The ISR is the authoritative store for all intent quanta within a locus. It maintains the current lifecycle state of every intent, the parent-child decomposition tree, and the history of state transitions. It is the component that System 3 reads from and writes to most frequently.

#### 3.3.2 Data Structures

**ISR Entry** (one per intent quantum):

```json
{
  "$schema": "https://atrahasis.org/rif/isr-entry/v1",
  "type": "object",
  "properties": {
    "intent_id": {
      "type": "string",
      "format": "uuid"
    },
    "intent": {
      "$ref": "#/$defs/IntentQuantum",
      "description": "Full intent quantum (see Section 5)"
    },
    "lifecycle_state": {
      "type": "string",
      "enum": ["PROPOSED", "DECOMPOSED", "ACTIVE", "COMPLETED", "DISSOLVED"]
    },
    "parent_intent_id": {
      "type": ["string", "null"],
      "description": "Null for root intents"
    },
    "children_intent_ids": {
      "type": "array",
      "items": { "type": "string" }
    },
    "assigned_agent_id": {
      "type": ["string", "null"],
      "description": "Non-null only for leaf intents in ACTIVE state"
    },
    "assigned_locus_id": {
      "type": "string",
      "description": "Locus where this intent is registered"
    },
    "spanning_loci": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Non-empty only for intents that span multiple loci"
    },
    "transition_log": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "from_state": { "type": "string" },
          "to_state": { "type": "string" },
          "causal_stamp": { "$ref": "#/$defs/CausalStamp" },
          "reason": { "type": "string" },
          "trigger_agent_id": { "type": "string" }
        },
        "required": ["from_state", "to_state", "causal_stamp",
                     "reason", "trigger_agent_id"]
      }
    },
    "result": {
      "type": ["object", "null"],
      "properties": {
        "outcome": {
          "type": "string",
          "enum": ["SUCCESS", "PARTIAL_SUCCESS", "FAILURE", "TIMEOUT"]
        },
        "output_parcel_ids": {
          "type": "array",
          "items": { "type": "string" }
        },
        "success_criteria_evaluation": {
          "type": "object",
          "additionalProperties": { "type": "boolean" }
        },
        "completion_epoch": { "type": "integer" }
      }
    },
    "resource_accounting": {
      "type": "object",
      "properties": {
        "allocated": { "$ref": "#/$defs/ResourceBounds" },
        "consumed": { "$ref": "#/$defs/ResourceBounds" },
        "returned_to_parent": { "$ref": "#/$defs/ResourceBounds" }
      },
      "required": ["allocated", "consumed", "returned_to_parent"]
    },
    "version_vector": {
      "type": "object",
      "additionalProperties": { "type": "integer" }
    },
    "gc_eligible_epoch": {
      "type": ["integer", "null"],
      "description": "Epoch after which this entry may be garbage collected (set when DISSOLVED)"
    }
  },
  "required": ["intent_id", "intent", "lifecycle_state",
               "parent_intent_id", "children_intent_ids",
               "assigned_locus_id", "transition_log",
               "resource_accounting", "version_vector"]
}
```

**Cross-locus spanning intent stub** (replicated to remote loci for spanning intents):

```json
{
  "$schema": "https://atrahasis.org/rif/spanning-intent-stub/v1",
  "type": "object",
  "properties": {
    "intent_id": { "type": "string", "format": "uuid" },
    "root_intent_id": { "type": "string", "format": "uuid" },
    "originating_locus_id": { "type": "string" },
    "operation_class": {
      "type": "string",
      "enum": ["M", "B", "X", "V", "G"]
    },
    "required_capabilities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "domain": { "type": "string" },
          "min_capacity": { "type": "number" }
        }
      }
    },
    "resource_bounds": { "$ref": "#/$defs/ResourceBounds" },
    "deadline_epoch": { "type": "integer" },
    "lifecycle_state": { "type": "string" },
    "causal_stamp": { "$ref": "#/$defs/CausalStamp" }
  },
  "required": ["intent_id", "root_intent_id", "originating_locus_id",
               "operation_class", "required_capabilities",
               "resource_bounds", "deadline_epoch",
               "lifecycle_state", "causal_stamp"]
}
```

#### 3.3.3 Replication Model

- **Intra-locus**: Full CRDT replication of all ISR entries. Uses operation-based CRDT with state transitions as operations. Conflict resolution: causal stamp ordering; ties broken by agent_id lexicographic order.
- **Cross-locus**: Only `SpanningIntentStub` objects replicate. Full intent state remains in the originating locus. Remote loci receive enough information to decide whether to accept and execute a spanning child intent.
- **Bandwidth budget**: ISR CRDT traffic capped at 5% of locus network capacity. If exceeded, replication batches increase in size (more ops per message, fewer messages) and non-critical fields (transition_log entries older than 10 epochs) are elided from replication.
- **GC policy**: Entries in DISSOLVED state are retained for 100 epochs after `gc_eligible_epoch`, then hard-deleted. Transition logs are compacted: only first, last, and failure transitions are retained after 50 epochs.

#### 3.3.4 Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| ISR CRDT divergence | Periodic Merkle root comparison (every 5 epochs) | Incremental reconciliation from Merkle diff |
| Orphaned intents | Parent intent DISSOLVED but children still ACTIVE | Children receive forced DISSOLVED with reason "PARENT_DISSOLVED" |
| Spanning intent unreachable | Remote locus PARTITIONED for > 5 epochs | Spanning intent transitions to COMPLETED(TIMEOUT); compensation at parent |
| ISR storage exhaustion | Storage utilization > 90% | Aggressive GC: reduce DISSOLVED retention to 10 epochs; alert System 3 |

#### 3.3.5 Integration Contracts

- **To System 3**: `propose_intent(intent_quantum) → intent_id`
- **To System 3**: `transition_intent(intent_id, new_state, reason) → CausalStamp`
- **To System 3**: `query_intents(filter) → List[ISREntry]`
- **To System 3**: `get_intent_tree(root_intent_id) → Tree[ISREntry]`
- **To Settlement Router**: `notify_settlement(intent_id, outcome)`
- **To Clock Service**: Requests `CausalStamp` for every state transition
- **To C4 ASV**: `emit_intent_claim(intent_id, outcome)` — publishes intent outcome as ASV claim with provenance

---

### 3.4 Settlement Router

#### 3.4.1 Purpose

The Settlement Router bridges RIF's intent lifecycle with C3's settlement ledger. When an intent completes (successfully or not), the Settlement Router ensures that all resource accounting, stake adjustments, and reputation updates are recorded in the C3 settlement ledger. It provides at-least-once delivery semantics with idempotent processing to guarantee that no settlement is lost even under partitions or crashes.

#### 3.4.2 Data Structures

**Settlement Message**:

```json
{
  "$schema": "https://atrahasis.org/rif/settlement-message/v1",
  "type": "object",
  "properties": {
    "settlement_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique idempotency key"
    },
    "intent_id": {
      "type": "string",
      "format": "uuid"
    },
    "settlement_type": {
      "type": "string",
      "enum": [
        "RESOURCE_RETURN",
        "STAKE_ADJUSTMENT",
        "REPUTATION_UPDATE",
        "COMPENSATION_DEBIT",
        "COMPLETION_CREDIT"
      ]
    },
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "agent_id": { "type": "string" },
          "resource_type": { "type": "string" },
          "amount": { "type": "number" },
          "direction": {
            "type": "string",
            "enum": ["CREDIT", "DEBIT"]
          }
        },
        "required": ["agent_id", "resource_type", "amount", "direction"]
      }
    },
    "causal_stamp": { "$ref": "#/$defs/CausalStamp" },
    "delivery_attempts": {
      "type": "integer",
      "minimum": 0
    },
    "first_attempt_epoch": { "type": "integer" },
    "last_attempt_epoch": { "type": "integer" },
    "status": {
      "type": "string",
      "enum": ["PENDING", "DELIVERED", "CONFIRMED", "DEAD_LETTER"]
    }
  },
  "required": ["settlement_id", "intent_id", "settlement_type",
               "entries", "causal_stamp", "delivery_attempts",
               "first_attempt_epoch", "last_attempt_epoch", "status"]
}
```

**Delivery Queue State**:

```json
{
  "$schema": "https://atrahasis.org/rif/settlement-queue/v1",
  "type": "object",
  "properties": {
    "locus_id": { "type": "string" },
    "queue_depth": { "type": "integer" },
    "oldest_pending_epoch": { "type": ["integer", "null"] },
    "dead_letter_count": { "type": "integer" },
    "throughput_per_epoch": { "type": "number" },
    "backpressure_active": { "type": "boolean" }
  },
  "required": ["locus_id", "queue_depth", "oldest_pending_epoch",
               "dead_letter_count", "throughput_per_epoch",
               "backpressure_active"]
}
```

#### 3.4.3 Replication Model

- **No cross-locus replication**: Settlement messages are locus-local. Each locus has its own settlement queue and its own connection to the C3 settlement ledger partition for that locus.
- **Persistence**: Settlement messages are persisted to local durable storage before first delivery attempt. Persistence is write-ahead-log style: message is durable before acknowledgment to ISR.
- **At-least-once delivery**: Messages are retried with exponential backoff (1 epoch, 2 epochs, 4 epochs, ... up to 32 epochs). After 10 failed attempts, the message moves to DEAD_LETTER status and alerts System 3.

#### 3.4.4 Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| C3 ledger unreachable | Delivery timeout (1 epoch) | Retry with exponential backoff |
| Duplicate delivery | C3 ledger rejects duplicate settlement_id | Mark as CONFIRMED (idempotent success) |
| Dead letter accumulation | Dead letter count > 100 | System 3 alert; manual intervention required |
| Queue backpressure | Queue depth > 10000 or oldest pending > 50 epochs | Throttle new intent completions; System 3 notified |
| Settlement Router crash | Failure Detector liveness check | Restart from WAL; replay all PENDING messages |

#### 3.4.5 Integration Contracts

- **From ISR**: `submit_settlement(intent_id, settlement_type, entries) → settlement_id`
- **To C3 Settlement Ledger**: `settle(settlement_message) → {ACCEPTED | DUPLICATE | REJECTED}`
- **To System 3**: `report_dead_letters(count, oldest_epoch)`
- **To System 3**: `report_backpressure(queue_state)`

---

### 3.5 Failure Detector

#### 3.5.1 Purpose

The Failure Detector serves two functions beyond simple liveness detection:

1. **Agent liveness**: Is the agent alive and responsive? (Traditional failure detection.)
2. **Intent outcome verification**: Did the intent's result actually advance the parent intent's success criteria? (Semantic failure detection via PCVM integration.)

The second function is what distinguishes RIF's Failure Detector from a conventional heartbeat monitor. An agent may be alive and responsive but consistently producing results that do not advance system goals. The Failure Detector integrates with C5 PCVM to detect this pattern.

#### 3.5.2 Data Structures

**Liveness Report**:

```json
{
  "$schema": "https://atrahasis.org/rif/liveness-report/v1",
  "type": "object",
  "properties": {
    "agent_id": { "type": "string" },
    "locus_id": { "type": "string" },
    "epoch": { "type": "integer" },
    "alive": { "type": "boolean" },
    "response_latency_ms": {
      "type": ["integer", "null"],
      "description": "Null if agent did not respond"
    },
    "reporter_agent_id": {
      "type": "string",
      "description": "Sentinel agent that performed the check"
    },
    "reporter_credibility": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "PCVM credibility of the reporting sentinel"
    }
  },
  "required": ["agent_id", "locus_id", "epoch", "alive",
               "reporter_agent_id", "reporter_credibility"]
}
```

**Intent Outcome Verification**:

```json
{
  "$schema": "https://atrahasis.org/rif/outcome-verification/v1",
  "type": "object",
  "properties": {
    "intent_id": { "type": "string" },
    "parent_intent_id": { "type": "string" },
    "verifier_agent_id": { "type": "string" },
    "verification_epoch": { "type": "integer" },
    "criteria_evaluated": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "criterion_id": { "type": "string" },
          "expected": { "type": "boolean" },
          "actual": { "type": "boolean" },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": ["criterion_id", "expected", "actual", "confidence"]
      }
    },
    "advancement_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "How much this intent's completion advanced the parent's success criteria"
    },
    "byzantine_suspicion": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "PCVM-derived suspicion score for the executing agent"
    },
    "verification_claim_id": {
      "type": "string",
      "description": "C4 ASV claim ID for this verification"
    }
  },
  "required": ["intent_id", "parent_intent_id", "verifier_agent_id",
               "verification_epoch", "criteria_evaluated",
               "advancement_score", "byzantine_suspicion",
               "verification_claim_id"]
}
```

**Failure Detector Configuration**:

```json
{
  "$schema": "https://atrahasis.org/rif/failure-detector-config/v1",
  "type": "object",
  "properties": {
    "liveness_check_interval_epochs": {
      "type": "integer",
      "default": 1,
      "description": "How often to check each agent"
    },
    "liveness_timeout_epochs": {
      "type": "integer",
      "default": 3,
      "description": "Consecutive missed heartbeats before declaring dead"
    },
    "sentinel_quorum": {
      "type": "integer",
      "default": 3,
      "description": "Number of sentinels that must agree on liveness"
    },
    "min_sentinel_credibility": {
      "type": "number",
      "default": 0.5,
      "description": "Minimum PCVM credibility to serve as sentinel"
    },
    "outcome_verification_sample_rate": {
      "type": "number",
      "default": 0.1,
      "minimum": 0,
      "maximum": 1,
      "description": "Fraction of completed intents to verify"
    },
    "byzantine_suspicion_threshold": {
      "type": "number",
      "default": 0.7,
      "description": "Suspicion score above which agent is flagged"
    },
    "advancement_score_min": {
      "type": "number",
      "default": 0.2,
      "description": "Minimum advancement score below which intent outcome is flagged as non-advancing"
    }
  },
  "required": ["liveness_check_interval_epochs",
               "liveness_timeout_epochs", "sentinel_quorum",
               "min_sentinel_credibility",
               "outcome_verification_sample_rate",
               "byzantine_suspicion_threshold",
               "advancement_score_min"]
}
```

#### 3.5.3 Replication Model

- **Intra-locus**: Liveness reports are broadcast to all sentinels within the locus. Quorum-based: an agent is declared dead only when `sentinel_quorum` sentinels agree within the same epoch window.
- **Cross-locus**: Only aggregate failure statistics replicate (number of failures per epoch, locus health score). Individual liveness reports do not cross locus boundaries.
- **Sentinel selection**: Sentinels are agents with `min_sentinel_credibility` or higher PCVM credibility. Each epoch, the sentinel set is refreshed by selecting the top-K credible agents (K = 2 * sentinel_quorum to allow for sentinel failures).

#### 3.5.4 Failure Handling

| Failure Mode | Detection | Response |
|---|---|---|
| Sentinel failure | Other sentinels detect missing sentinel heartbeat | Replace from sentinel candidate pool; no gap if pool has headroom |
| False positive (live agent declared dead) | Agent self-reports after recovery | Re-evaluate with fresh quorum check; if alive, restore status; reassign intents if already reassigned |
| False negative (dead agent not detected) | Intent timeout without result | Intent timeout triggers independent liveness check; if confirmed dead, declare failure retroactively |
| Byzantine sentinel (lying about liveness) | PCVM credibility drop; inconsistent reports vs. majority | Exclude sentinel; PCVM credibility update propagates |
| Outcome verification disagreement | Verifier and executor disagree on advancement | Escalate to System 3 for arbitration; if unresolved, escalate to System 5 |

#### 3.5.5 Integration Contracts

- **To Agent Registry**: `report_agent_liveness(agent_id, epoch, alive)`
- **To ISR**: `flag_non_advancing_intent(intent_id, advancement_score)`
- **To System 3**: `report_agent_failure(agent_id, failure_type, evidence)`
- **To System 3**: `report_outcome_verification(verification_result)`
- **To C5 PCVM**: `query_agent_credibility(agent_id) → credibility_score`
- **To C5 PCVM**: `submit_byzantine_evidence(agent_id, evidence)`
- **To C4 ASV**: `publish_verification_claim(verification) → claim_id`

---

## 4. Executive Plane

### 4.1 System 3 — Operational Control

System 3 is the operational heart of RIF. It receives intent proposals, decomposes them into executable sub-intents, assigns leaf intents to agents, monitors execution, and handles failures. It is the most active component in the Executive Plane.

#### 4.1.1 Intent Decomposition Engine

The Intent Decomposition Engine receives PROPOSED intents and transforms them into trees of child intents. Decomposition continues recursively until every leaf intent maps to a single C3 operation class (M, B, X, V, or G) that can be executed by a single agent within a single epoch.

**Pseudocode: `decompose_intent()`**

```
function decompose_intent(intent: IntentQuantum, depth: int) -> DecompositionResult:
    // --- Guard clauses ---
    if depth > intent.constraints.max_depth:
        return DecompositionResult.failure(
            reason="MAX_DEPTH_EXCEEDED",
            intent_id=intent.intent_id
        )

    if wall_clock_elapsed(intent.decomposition_start) > intent.constraints.decomposition_budget_ms:
        return DecompositionResult.failure(
            reason="DECOMPOSITION_BUDGET_EXHAUSTED",
            intent_id=intent.intent_id
        )

    if tokens_consumed > intent.constraints.decomposition_token_limit:
        return DecompositionResult.failure(
            reason="TOKEN_BUDGET_EXHAUSTED",
            intent_id=intent.intent_id
        )

    // --- Check memoization cache ---
    cache_key = (intent.intent_type, intent.scope, context_hash(intent))
    cached = memo_cache.get(cache_key)
    if cached != null and cached.ttl > current_epoch():
        delta = compute_state_delta(cached.snapshot, current_state())
        if delta.is_minor():
            plan = cached.plan.apply_delta(delta)
            return DecompositionResult.success(plan, source="CACHE_HIT")

    // --- Check if intent is already a leaf ---
    if is_leaf_operation(intent):
        // M-class intents or intents already mapped to a single operation
        validate_resource_bounds(intent)
        agent = select_agent(intent.operation_class, intent.scope.domain)
        if agent == null:
            return DecompositionResult.failure(
                reason="NO_CAPABLE_AGENT",
                intent_id=intent.intent_id
            )
        return DecompositionResult.leaf(intent, agent)

    // --- Select decomposition strategy ---
    strategy = select_strategy(intent)

    // --- Apply decomposition rules ---
    children = apply_decomposition_rules(intent, strategy)

    // --- Validate operation class monotonicity ---
    for child in children:
        assert child.operation_class <= intent.operation_class,
            "Child operation class must not exceed parent"

    // --- Validate resource bounds preservation ---
    validate_resource_partition(intent.resource_bounds, children)

    // --- Recursively decompose non-leaf children ---
    results = []
    for child in children:
        child_result = decompose_intent(child, depth + 1)
        if child_result.is_failure():
            // Compensation: dissolve already-created siblings
            for created in results:
                dissolve_subtree(created)
            return DecompositionResult.failure(
                reason="CHILD_DECOMPOSITION_FAILED",
                intent_id=intent.intent_id,
                child_failure=child_result
            )
        results.append(child_result)

    // --- Memoize successful decomposition ---
    plan = DecompositionPlan(strategy, results)
    memo_cache.put(cache_key, plan, ttl=current_epoch() + 50)

    // --- Register all children in ISR ---
    for result in results:
        isr.register_intent_tree(result)

    // --- Transition parent to DECOMPOSED ---
    isr.transition_intent(intent.intent_id, "DECOMPOSED",
                          reason="decomposition_complete")

    return DecompositionResult.success(plan, source="COMPUTED")
```

**Decomposition Strategy Selection**:

```
function select_strategy(intent: IntentQuantum) -> DecompositionStrategy:
    // RECURSIVE: break into smaller instances of the same type
    if intent.is_divisible() and intent.scope.can_partition():
        return RECURSIVE

    // PARALLEL: independent sub-tasks that can execute concurrently
    if intent.success_criteria.is_conjunctive()
       and intent.sub_goals_are_independent():
        return PARALLEL

    // SEQUENTIAL: ordered steps where each depends on prior output
    if intent.success_criteria.is_ordered_sequence():
        return SEQUENTIAL

    // CONDITIONAL: branching based on intermediate results
    if intent.success_criteria.has_conditionals():
        return CONDITIONAL

    // Default: SEQUENTIAL (safest)
    return SEQUENTIAL
```

**Strategy Semantics**:

| Strategy | Execution Model | Child Ordering | Failure Behavior |
|---|---|---|---|
| RECURSIVE | Divide scope, apply same intent type to each partition | Unordered (parallel) | Partial success possible; parent evaluates combined results |
| PARALLEL | All children execute concurrently | Unordered | All-or-nothing by default; configurable partial-success threshold |
| SEQUENTIAL | Children execute in declared order; output of N feeds input of N+1 | Strictly ordered | First failure halts pipeline; compensation for completed steps |
| CONDITIONAL | Branch selector evaluates predicate, chooses one branch | Predicate → branch | If selected branch fails, no fallback unless configured |

**Operation Class Mapping at Leaf Level**:

When decomposition reaches a leaf intent (one that cannot or should not be further decomposed), the leaf must map to exactly one C3 operation class:

```
function map_to_operation_class(leaf: IntentQuantum) -> OperationClass:
    match leaf.intent_type:
        case GOAL:
            // Goals should not reach leaf level; if they do, something is wrong
            raise DecompositionError("GOAL intent reached leaf level")
        case DIRECTIVE:
            if leaf.scope.requires_exclusive_access:
                return X  // Exclusive operation
            elif leaf.scope.is_bounded_local:
                return B  // Bounded local operation
            else:
                return M  // Merge operation (default)
        case QUERY:
            return M  // Queries are always merge operations
        case OPTIMIZATION:
            if leaf.scope.affects_governance:
                return G  // Governance operation
            elif leaf.scope.requires_verification:
                return V  // Verification operation
            else:
                return B  // Bounded local optimization
```

#### 4.1.2 Resource Optimizer

The Resource Optimizer tracks resource allocations across the entire intent tree and reclaims unused margins when children complete under-budget.

```
function reconcile_resources(parent_id: IntentId):
    parent = isr.get_intent(parent_id)
    children = isr.get_children(parent_id)

    total_allocated = sum(c.resource_accounting.allocated for c in children)
    total_consumed = sum(c.resource_accounting.consumed
                         for c in children if c.lifecycle_state == COMPLETED)
    total_returned = total_allocated - total_consumed

    // Return unused resources to parent's available pool
    parent.resource_accounting.returned_to_parent += total_returned

    // If parent has siblings still pending, the parent's parent can
    // redistribute returned resources
    if parent.parent_intent_id != null:
        notify_parent_of_surplus(parent.parent_intent_id, total_returned)
```

**Resource redistribution rules**:
- Returned resources are available to sibling intents of the returning child.
- Redistribution happens lazily: siblings request additional resources when needed, not proactively.
- Resources cannot flow upward past a completed parent (once a parent COMPLETES, its resources are settled).

#### 4.1.3 Performance Monitor

The Performance Monitor tracks operational health metrics and feeds them to System 4 for strategic analysis.

**Tracked Metrics**:

| Metric | Granularity | Collection | Alert Threshold |
|---|---|---|---|
| Intent completion rate | Per-locus, per-epoch | Count COMPLETED / (COMPLETED + FAILED) | < 80% over 5-epoch window |
| Decomposition latency | Per-intent | Wall-clock from PROPOSED → DECOMPOSED | > 2x mean over 10-epoch window |
| Decomposition depth (actual) | Per-intent | Maximum depth of realized tree | > 80% of max_depth constraint |
| Resource utilization | Per-locus, per-epoch | Consumed / Allocated across all intents | > 90% (overload) or < 20% (underload) |
| Queue depth | Per-locus | ISR entries in PROPOSED state | > 1000 (backlog forming) |
| Cross-locus intent ratio | Per-locus, per-epoch | Spanning intents / total intents | > 30% (excessive cross-locus traffic) |
| Memoization hit rate | Per-locus, per-epoch | Cache hits / total decompositions | < 10% after 100 epochs (cache not effective) |

**Metrics Export Structure**:

```json
{
  "$schema": "https://atrahasis.org/rif/performance-metrics/v1",
  "type": "object",
  "properties": {
    "locus_id": { "type": "string" },
    "epoch": { "type": "integer" },
    "intent_completion_rate": { "type": "number" },
    "mean_decomposition_latency_ms": { "type": "number" },
    "p99_decomposition_latency_ms": { "type": "number" },
    "max_decomposition_depth": { "type": "integer" },
    "resource_utilization": { "type": "number" },
    "proposed_queue_depth": { "type": "integer" },
    "cross_locus_intent_ratio": { "type": "number" },
    "memo_cache_hit_rate": { "type": "number" },
    "active_intent_count": { "type": "integer" },
    "failed_intent_count": { "type": "integer" }
  },
  "required": ["locus_id", "epoch", "intent_completion_rate",
               "mean_decomposition_latency_ms", "resource_utilization",
               "proposed_queue_depth", "active_intent_count"]
}
```

#### 4.1.4 Failure Playbooks

Failure Playbooks are pre-defined response procedures for common failure scenarios. They are triggered automatically by the Failure Detector and Performance Monitor.

```
FailurePlaybook = {
    "AGENT_CRASH": {
        trigger: "Failure Detector reports agent_id dead",
        steps: [
            "1. Identify all ACTIVE intents assigned to agent_id",
            "2. For each intent: transition to PROPOSED (re-enter queue)",
            "3. Blacklist agent_id for 5 epochs",
            "4. If intent has exceeded 50% of its deadline, escalate to",
            "   parent for potential re-decomposition"
        ],
        escalation: "System 5 if agent_id has stake > threshold"
    },

    "DECOMPOSITION_TIMEOUT": {
        trigger: "decompose_intent() exceeds budget",
        steps: [
            "1. Dissolve all partially-created children",
            "2. Mark intent as COMPLETED(FAILURE, DECOMPOSITION_TIMEOUT)",
            "3. Notify parent intent",
            "4. Log decomposition attempt for System 4 analysis"
        ],
        escalation: "System 4 if this intent_type has > 30% timeout rate"
    },

    "RESOURCE_EXHAUSTION": {
        trigger: "Resource utilization > 95% for 3 consecutive epochs",
        steps: [
            "1. Pause acceptance of new PROPOSED intents",
            "2. Allow in-flight intents to complete",
            "3. Aggressive GC on DISSOLVED entries",
            "4. Request System 4 capacity planning review"
        ],
        escalation: "System 5 if pause exceeds 10 epochs"
    },

    "CASCADE_FAILURE": {
        trigger: "Intent completion rate < 50% for 3 consecutive epochs",
        steps: [
            "1. Halt all new decompositions",
            "2. Identify common failure pattern (shared agent, shared",
            "   resource, shared decomposition plan)",
            "3. Invalidate relevant memoization cache entries",
            "4. Resume decompositions one at a time to isolate cause"
        ],
        escalation: "System 5 for emergency tidal rollback consideration"
    },

    "SETTLEMENT_BACKLOG": {
        trigger: "Settlement Router reports backpressure",
        steps: [
            "1. Throttle intent completion rate to match settlement",
            "   throughput",
            "2. Prioritize settlements for intents with stake-bearing",
            "   agents",
            "3. If backlog exceeds 50 epochs, alert System 5"
        ],
        escalation: "System 5 if dead letters > 100"
    },

    "SPANNING_INTENT_PARTITION": {
        trigger: "Remote locus PARTITIONED for spanning intent",
        steps: [
            "1. Wait 5 epochs for partition resolution",
            "2. If unresolved, timeout the spanning child",
            "3. Re-decompose parent intent excluding partitioned locus",
            "4. If re-decomposition fails, escalate to parent"
        ],
        escalation: "System 4 for cross-locus capacity rebalancing"
    }
}
```

#### 4.1.5 Compensation Protocols

Compensation protocols implement saga-style rollback for partial decomposition or execution failures.

```
function compensate_subtree(intent_id: IntentId, reason: string):
    intent = isr.get_intent(intent_id)
    children = isr.get_children(intent_id)

    // Phase 1: Stop all active children (depth-first, leaves first)
    for child in reverse_topological_order(children):
        if child.lifecycle_state == ACTIVE:
            // Send cancellation signal to assigned agent
            cancel_agent_execution(child.assigned_agent_id, child.intent_id)
            isr.transition_intent(child.intent_id, "DISSOLVED",
                                  reason="COMPENSATION:" + reason)
        elif child.lifecycle_state == DECOMPOSED:
            // Recursively compensate this child's subtree
            compensate_subtree(child.intent_id, reason)
        elif child.lifecycle_state == COMPLETED:
            // Already completed; emit compensation settlement
            settlement_router.submit_settlement(
                child.intent_id,
                "COMPENSATION_DEBIT",
                reverse_entries(child.resource_accounting)
            )
            isr.transition_intent(child.intent_id, "DISSOLVED",
                                  reason="COMPENSATION:" + reason)

    // Phase 2: Dissolve the parent
    isr.transition_intent(intent_id, "DISSOLVED",
                          reason="COMPENSATION:" + reason)

    // Phase 3: Notify upward
    if intent.parent_intent_id != null:
        notify_parent_child_compensated(intent.parent_intent_id, intent_id)
```

**Compensation Guarantees**:
- All settlements for compensated intents are reversed via COMPENSATION_DEBIT entries.
- Compensation is idempotent: compensating an already-DISSOLVED intent is a no-op.
- Compensation is eventually consistent: settlement reversals may lag behind intent state changes.

#### 4.1.6 Decomposition Memoization

(Detailed in Section 6.6; System 3 integration summary here.)

System 3 maintains a decomposition memoization cache per locus. The cache stores previously successful decomposition plans keyed by `(intent_type, scope, context_hash)`. On cache hit, the prior plan is reused with delta adjustments for system state changes since the cached snapshot.

```
MemoizationCache = {
    max_entries: 10000,
    ttl_epochs: 50,
    eviction_policy: "LRU",
    invalidation_triggers: [
        "agent_registry_change",
        "locus_topology_change",
        "system_5_policy_change",
        "operation_class_rule_change"
    ]
}
```

---

### 4.2 System 4 — Strategic Intelligence

System 4 is the forward-looking component of the Executive Plane. It reads trends, anticipates future resource needs, and proposes adaptations to System 3's operational parameters. System 4 has no direct authority to change operations — it can only propose. System 5 arbitrates when System 3 and System 4 disagree.

#### 4.2.1 Horizon Scanning

System 4 reads EMA projections (C6) in read-only mode to identify emerging knowledge trends that may affect future intent workloads.

```
function horizon_scan(locus_id: string, window_epochs: int) -> HorizonReport:
    // Read EMA projections — STRICTLY READ-ONLY
    projections = ema.get_projections(locus_id, window_epochs)

    trends = []
    for projection in projections:
        // Identify rising knowledge domains
        if projection.growth_rate > TREND_THRESHOLD:
            trends.append(Trend(
                domain=projection.domain,
                direction="RISING",
                confidence=projection.confidence,
                projected_impact=estimate_intent_volume_impact(
                    projection, locus_id
                )
            ))

        // Identify declining domains (potential resource reclamation)
        if projection.growth_rate < -TREND_THRESHOLD:
            trends.append(Trend(
                domain=projection.domain,
                direction="FALLING",
                confidence=projection.confidence,
                projected_impact=estimate_resource_reclamation(
                    projection, locus_id
                )
            ))

    return HorizonReport(
        locus_id=locus_id,
        scan_epoch=current_epoch(),
        window_epochs=window_epochs,
        trends=trends,
        overall_volatility=compute_volatility(projections)
    )
```

**Horizon Report Structure**:

```json
{
  "$schema": "https://atrahasis.org/rif/horizon-report/v1",
  "type": "object",
  "properties": {
    "locus_id": { "type": "string" },
    "scan_epoch": { "type": "integer" },
    "window_epochs": { "type": "integer" },
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "domain": { "type": "string" },
          "direction": {
            "type": "string",
            "enum": ["RISING", "FALLING", "STABLE"]
          },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "projected_impact": {
            "type": "object",
            "properties": {
              "intent_volume_change_pct": { "type": "number" },
              "resource_demand_change_pct": { "type": "number" },
              "affected_operation_classes": {
                "type": "array",
                "items": {
                  "type": "string",
                  "enum": ["M", "B", "X", "V", "G"]
                }
              }
            }
          }
        },
        "required": ["domain", "direction", "confidence",
                     "projected_impact"]
      }
    },
    "overall_volatility": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Aggregate volatility of all projections"
    }
  },
  "required": ["locus_id", "scan_epoch", "window_epochs",
               "trends", "overall_volatility"]
}
```

#### 4.2.2 Anticipatory Capacity Planning

Based on horizon scan results, System 4 predicts future resource needs and proposes pre-positioning actions.

```
function plan_capacity(horizon: HorizonReport) -> CapacityPlan:
    proposals = []

    for trend in horizon.trends:
        if trend.direction == "RISING" and trend.confidence > 0.6:
            // Project resource needs N epochs ahead
            needed = project_resource_needs(
                trend, lookahead_epochs=20
            )
            current = get_current_capacity(
                horizon.locus_id, trend.domain
            )

            if needed > current * 1.2:  // 20% headroom threshold
                proposals.append(CapacityProposal(
                    action="SCALE_UP",
                    domain=trend.domain,
                    target_capacity=needed * 1.1,  // 10% buffer
                    urgency=compute_urgency(needed, current, trend),
                    confidence=trend.confidence
                ))

        elif trend.direction == "FALLING" and trend.confidence > 0.7:
            // Higher confidence required for scale-down (conservative)
            freeable = estimate_freeable_resources(
                horizon.locus_id, trend.domain
            )
            if freeable > 0:
                proposals.append(CapacityProposal(
                    action="SCALE_DOWN",
                    domain=trend.domain,
                    freeable_capacity=freeable,
                    urgency="LOW",
                    confidence=trend.confidence
                ))

    return CapacityPlan(
        locus_id=horizon.locus_id,
        epoch=current_epoch(),
        proposals=proposals,
        horizon_volatility=horizon.overall_volatility
    )
```

#### 4.2.3 Adaptation Proposal Protocol

System 4 communicates with System 3 exclusively through formal adaptation proposals. Each proposal has a defined structure, is subject to cool-down enforcement, and is checked for similarity against recent proposals to prevent oscillation.

**Adaptation Proposal Structure**:

```json
{
  "$schema": "https://atrahasis.org/rif/adaptation-proposal/v1",
  "type": "object",
  "properties": {
    "proposal_id": {
      "type": "string",
      "format": "uuid"
    },
    "proposer": {
      "type": "string",
      "const": "SYSTEM_4"
    },
    "epoch": { "type": "integer" },
    "category": {
      "type": "string",
      "enum": [
        "CAPACITY_CHANGE",
        "DECOMPOSITION_RULE_UPDATE",
        "THRESHOLD_ADJUSTMENT",
        "AGENT_REBALANCING",
        "OPERATION_CLASS_REMAPPING"
      ]
    },
    "description": { "type": "string" },
    "justification": {
      "type": "object",
      "properties": {
        "horizon_report_id": { "type": "string" },
        "supporting_metrics": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "metric_name": { "type": "string" },
              "current_value": { "type": "number" },
              "projected_value": { "type": "number" },
              "confidence": { "type": "number" }
            }
          }
        },
        "risk_assessment": {
          "type": "string",
          "enum": ["LOW", "MEDIUM", "HIGH"]
        }
      },
      "required": ["horizon_report_id", "supporting_metrics",
                    "risk_assessment"]
    },
    "proposed_changes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "parameter": { "type": "string" },
          "current_value": {},
          "proposed_value": {},
          "rollback_value": {}
        },
        "required": ["parameter", "current_value",
                     "proposed_value", "rollback_value"]
      }
    },
    "cool_down_epochs": {
      "type": "integer",
      "default": 5,
      "description": "Minimum epochs before a similar proposal can be made"
    },
    "stability_gate": {
      "type": "object",
      "properties": {
        "required_stable_epochs": {
          "type": "integer",
          "default": 3
        },
        "stability_metric": { "type": "string" },
        "stability_threshold": { "type": "number" }
      }
    },
    "status": {
      "type": "string",
      "enum": ["PENDING", "ACCEPTED", "REJECTED", "DEFERRED",
               "COOLDOWN_BLOCKED", "SIMILARITY_BLOCKED"]
    }
  },
  "required": ["proposal_id", "proposer", "epoch", "category",
               "description", "justification", "proposed_changes",
               "cool_down_epochs", "status"]
}
```

**Proposal Submission Flow**:

```
function submit_proposal(proposal: AdaptationProposal) -> ProposalOutcome:
    // 1. Cool-down check
    last_similar = find_last_similar_proposal(proposal.category)
    if last_similar != null:
        epochs_since = current_epoch() - last_similar.epoch
        if epochs_since < proposal.cool_down_epochs:
            proposal.status = "COOLDOWN_BLOCKED"
            return ProposalOutcome(
                status="BLOCKED",
                reason="cool_down",
                retry_after_epoch=last_similar.epoch + proposal.cool_down_epochs
            )

    // 2. Similarity detection
    recent_proposals = get_proposals_in_window(
        category=proposal.category,
        window_epochs=20
    )
    for recent in recent_proposals:
        if cosine_similarity(proposal.proposed_changes,
                             recent.proposed_changes) > 0.85:
            proposal.status = "SIMILARITY_BLOCKED"
            return ProposalOutcome(
                status="BLOCKED",
                reason="similar_proposal_recent",
                similar_proposal_id=recent.proposal_id
            )

    // 3. Stability gate check
    if proposal.stability_gate != null:
        stable_count = count_stable_epochs(
            proposal.stability_gate.stability_metric,
            proposal.stability_gate.stability_threshold
        )
        if stable_count < proposal.stability_gate.required_stable_epochs:
            proposal.status = "DEFERRED"
            return ProposalOutcome(
                status="DEFERRED",
                reason="stability_gate_not_met",
                stable_epochs=stable_count,
                required=proposal.stability_gate.required_stable_epochs
            )

    // 4. Submit to System 3 for consideration
    proposal.status = "PENDING"
    system3.receive_proposal(proposal)
    return ProposalOutcome(status="PENDING")
```

#### 4.2.4 Volatility-Aware Confidence

When EMA projection volatility is high, System 4 discounts the confidence of its own proposals to prevent overreaction to noisy signals.

```
function discount_confidence(
    raw_confidence: float,
    volatility: float
) -> float:
    // Sigmoid discount: high volatility → sharply reduced confidence
    // At volatility=0, discount=1.0 (no discount)
    // At volatility=0.5, discount≈0.62
    // At volatility=1.0, discount≈0.27
    discount_factor = 1.0 / (1.0 + exp(4.0 * (volatility - 0.5)))
    return raw_confidence * discount_factor
```

**Confidence thresholds for proposal categories**:

| Category | Minimum Confidence (after discount) | Rationale |
|---|---|---|
| CAPACITY_CHANGE | 0.5 | Moderate confidence needed; errors are recoverable |
| DECOMPOSITION_RULE_UPDATE | 0.7 | Higher bar; changes affect all future decompositions |
| THRESHOLD_ADJUSTMENT | 0.4 | Low bar; thresholds are continuously adjustable |
| AGENT_REBALANCING | 0.6 | Moderate; rebalancing is disruptive but reversible |
| OPERATION_CLASS_REMAPPING | 0.8 | High bar; operation class changes have system-wide impact |

#### 4.2.5 Oscillation Dampening

Three mechanisms prevent System 4 from causing oscillatory behavior:

**1. Cool-down timer**: After any accepted proposal, no similar proposal may be submitted for `cool_down_epochs` (default: 5 epochs).

**2. Similarity detector**: Proposals with > 85% cosine similarity to a proposal made within the last 20 epochs are blocked. Similarity is computed over the normalized parameter change vectors.

**3. Stability gating**: Certain proposal categories require N consecutive stable epochs (default: 3) before submission. "Stable" means the relevant metric has varied by less than the stability threshold across the required window.

```
function count_stable_epochs(
    metric_name: string,
    threshold: float
) -> int:
    // Count consecutive recent epochs where metric variation
    // is below threshold
    consecutive = 0
    epochs = get_metric_history(metric_name, window=10)

    for i in range(len(epochs) - 1, 0, -1):
        variation = abs(epochs[i] - epochs[i-1]) / max(epochs[i-1], 0.001)
        if variation < threshold:
            consecutive += 1
        else:
            break

    return consecutive
```

---

### 4.3 System 5 — G-Class Governance

System 5 is the identity and governance layer of RIF. It maps directly onto C3's existing G-class constitutional consensus mechanism. System 5 does not introduce new governance primitives — it provides the interface through which RIF's Executive Plane interacts with C3's governance.

#### 4.3.1 Governance Scope

System 5 has authority over:

| Domain | Authority | Mechanism |
|---|---|---|
| System 3 vs System 4 conflict resolution | Final arbiter when System 3 rejects a System 4 proposal and System 4 escalates | G-class vote among governance-capable agents |
| Operational sovereignty relaxation | Temporarily relax constraints (e.g., allow System 3 to exceed normal resource limits) | 90% supermajority vote; max 50-epoch lease |
| Emergency tidal rollback | Coordinate rollback of tidal epoch state when systemic failure detected | G-class emergency consensus; requires System 3 to halt all intent processing |
| System identity constraints | Define and enforce invariants that no operational or strategic action may violate | Constitutional rules; immutable except by G-class amendment |
| Stake slashing | Authorize slashing of agent stake for proven Byzantine behavior | G-class vote with PCVM evidence required |

#### 4.3.2 Conflict Resolution Protocol

```
function resolve_conflict(
    system3_position: OperationalDecision,
    system4_proposal: AdaptationProposal
) -> Resolution:
    // Package conflict for G-class vote
    conflict = ConflictPackage(
        system3_position=system3_position,
        system4_proposal=system4_proposal,
        performance_context=get_recent_metrics(window=20),
        horizon_context=get_recent_horizon_reports(window=20)
    )

    // Submit to G-class consensus
    vote_result = c3.g_class_vote(
        topic="S3_S4_CONFLICT",
        package=conflict,
        quorum_threshold=0.66,   // Simple majority for conflicts
        timeout_epochs=5
    )

    if vote_result.outcome == "SYSTEM_4_ACCEPTED":
        system3.apply_proposal(system4_proposal)
        return Resolution(
            winner="SYSTEM_4",
            applied_changes=system4_proposal.proposed_changes,
            vote_record=vote_result
        )
    elif vote_result.outcome == "SYSTEM_3_SUSTAINED":
        system4.acknowledge_rejection(system4_proposal.proposal_id)
        return Resolution(
            winner="SYSTEM_3",
            applied_changes=none,
            vote_record=vote_result
        )
    elif vote_result.outcome == "COMPROMISE":
        merged = vote_result.compromise_changes
        system3.apply_proposal(merged)
        return Resolution(
            winner="COMPROMISE",
            applied_changes=merged,
            vote_record=vote_result
        )
    else:
        // Timeout or no quorum: System 3 position holds (status quo)
        return Resolution(
            winner="SYSTEM_3_DEFAULT",
            applied_changes=none,
            reason="No quorum reached; status quo preserved"
        )
```

#### 4.3.3 Sovereignty Relaxation

Under exceptional circumstances, System 3 may need to operate outside its normal constraints (e.g., exceed resource limits during a surge, bypass memoization during a novel workload, extend decomposition depth limits). This requires System 5 authorization.

```json
{
  "$schema": "https://atrahasis.org/rif/sovereignty-relaxation/v1",
  "type": "object",
  "properties": {
    "relaxation_id": {
      "type": "string",
      "format": "uuid"
    },
    "requester": {
      "type": "string",
      "const": "SYSTEM_3"
    },
    "epoch": { "type": "integer" },
    "constraint_relaxed": {
      "type": "string",
      "description": "Which constraint is being relaxed"
    },
    "original_value": {},
    "relaxed_value": {},
    "justification": { "type": "string" },
    "lease_epochs": {
      "type": "integer",
      "maximum": 50,
      "description": "How long the relaxation lasts"
    },
    "vote_result": {
      "type": "object",
      "properties": {
        "votes_for": { "type": "integer" },
        "votes_against": { "type": "integer" },
        "total_eligible": { "type": "integer" },
        "supermajority_met": { "type": "boolean" }
      }
    },
    "status": {
      "type": "string",
      "enum": ["REQUESTED", "APPROVED", "DENIED", "ACTIVE", "EXPIRED",
               "REVOKED"]
    },
    "expiry_epoch": {
      "type": ["integer", "null"]
    }
  },
  "required": ["relaxation_id", "requester", "epoch",
               "constraint_relaxed", "original_value", "relaxed_value",
               "justification", "lease_epochs", "status"]
}
```

**Relaxation rules**:
- 90% supermajority of G-class governance-capable agents required.
- Maximum lease: 50 epochs. No renewal without a fresh vote.
- System 5 may revoke a relaxation early if the justifying conditions no longer hold.
- All relaxations are logged immutably in the C3 settlement ledger.

#### 4.3.4 Emergency Tidal Rollback

When systemic failure is detected (e.g., cascading intent failures across multiple loci, settlement ledger corruption, Byzantine supermajority), System 5 coordinates an emergency tidal rollback.

```
function emergency_rollback(
    trigger: EmergencyTrigger
) -> RollbackResult:
    // Phase 1: Halt
    system3.halt_all_intent_processing()
    broadcast_all_loci("EMERGENCY_HALT", trigger)

    // Phase 2: Vote
    vote = c3.g_class_vote(
        topic="EMERGENCY_ROLLBACK",
        package=trigger,
        quorum_threshold=0.90,
        timeout_epochs=3   // Shorter timeout for emergencies
    )

    if not vote.supermajority_met:
        system3.resume_intent_processing()
        return RollbackResult(
            status="ABORTED",
            reason="Supermajority not reached"
        )

    // Phase 3: Determine rollback point
    rollback_epoch = determine_safe_epoch(trigger)

    // Phase 4: Execute rollback via C3
    c3.tidal_rollback(rollback_epoch)

    // Phase 5: Reconstruct ISR state from rollback point
    isr.rebuild_from_epoch(rollback_epoch)

    // Phase 6: Resume
    system3.resume_intent_processing()

    return RollbackResult(
        status="COMPLETED",
        rollback_epoch=rollback_epoch,
        intents_dissolved=isr.count_dissolved_by_rollback(),
        vote_record=vote
    )
```

#### 4.3.5 System Identity Constraints

System 5 enforces a set of identity constraints — invariants that define what the system *is* and *is not*. These cannot be violated by any operational or strategic action.

| Constraint | Description | Enforcement |
|---|---|---|
| Decomposition Termination | All intent decompositions must terminate (Section 6.2) | System 3 enforces max_depth; System 5 audits |
| Resource Bound Integrity | Children cannot exceed parent resource bounds (Section 6.4) | System 3 validates at decomposition time; System 5 audits settlement records |
| Operation Class Monotonicity | Decomposition cannot produce children with higher operation class than parent (Section 6.1) | System 3 enforces; System 5 validates decomposition logs |
| Governance Primacy | No operational action can override a G-class decision | System 5 intercepts any System 3 action that contradicts active G-class resolutions |
| Settlement Completeness | Every intent that reaches COMPLETED must have a corresponding settlement | Settlement Router guarantees; System 5 audits |
| Provenance Chain Integrity | Every intent state transition must have a valid causal stamp and ASV provenance | ISR enforces; System 5 audits via C4 |

---

## 5. Intent Quantum Specification

### 5.1 Complete JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.org/rif/intent-quantum/v1",
  "title": "RIF Intent Quantum",
  "description": "The fundamental unit of work in the Recursive Intent Fabric",
  "type": "object",
  "properties": {
    "intent_id": {
      "type": "string",
      "format": "uuid",
      "description": "Globally unique intent identifier"
    },
    "intent_type": {
      "type": "string",
      "enum": ["GOAL", "DIRECTIVE", "QUERY", "OPTIMIZATION"],
      "description": "Classification of intent purpose"
    },
    "operation_class": {
      "type": ["string", "null"],
      "enum": ["M", "B", "X", "V", "G", null],
      "description": "C3 operation class. Null for non-leaf intents; set at leaf level."
    },
    "origin": {
      "type": "object",
      "properties": {
        "proposer_agent_id": {
          "type": "string",
          "description": "Agent that proposed this intent"
        },
        "proposer_locus_id": {
          "type": "string"
        },
        "proposal_epoch": {
          "type": "integer"
        },
        "causal_stamp": {
          "$ref": "#/$defs/CausalStamp"
        },
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
        "domain": {
          "type": "string",
          "description": "Knowledge/operational domain"
        },
        "target_loci": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Loci where this intent may execute"
        },
        "target_parcels": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Specific C3 parcels in scope"
        },
        "requires_exclusive_access": {
          "type": "boolean",
          "default": false
        },
        "is_bounded_local": {
          "type": "boolean",
          "default": true
        },
        "affects_governance": {
          "type": "boolean",
          "default": false
        },
        "requires_verification": {
          "type": "boolean",
          "default": false
        }
      },
      "required": ["domain", "target_loci"]
    },
    "description": {
      "type": "string",
      "maxLength": 4096,
      "description": "Human-readable description of the intent"
    },
    "success_criteria": {
      "type": "object",
      "properties": {
        "criteria_type": {
          "type": "string",
          "enum": ["PREDICATE", "THRESHOLD", "TEMPORAL", "COMPOSITE"]
        },
        "predicates": {
          "type": "array",
          "items": { "$ref": "#/$defs/SuccessPredicate" },
          "description": "Present when criteria_type is PREDICATE or COMPOSITE"
        },
        "thresholds": {
          "type": "array",
          "items": { "$ref": "#/$defs/SuccessThreshold" },
          "description": "Present when criteria_type is THRESHOLD or COMPOSITE"
        },
        "temporal_bound": {
          "$ref": "#/$defs/TemporalBound",
          "description": "Present when criteria_type is TEMPORAL or COMPOSITE"
        },
        "composition": {
          "type": "string",
          "enum": ["AND", "OR"],
          "description": "How sub-criteria combine in COMPOSITE type"
        }
      },
      "required": ["criteria_type"]
    },
    "resource_bounds": {
      "$ref": "#/$defs/ResourceBounds"
    },
    "constraints": {
      "type": "object",
      "properties": {
        "max_depth": {
          "type": "integer",
          "minimum": 1,
          "maximum": 20,
          "default": 10,
          "description": "Maximum decomposition depth"
        },
        "decomposition_budget_ms": {
          "type": "integer",
          "minimum": 100,
          "maximum": 60000,
          "default": 5000,
          "description": "Wall-clock time limit for decomposition"
        },
        "decomposition_token_limit": {
          "type": "integer",
          "minimum": 100,
          "maximum": 1000000,
          "default": 10000,
          "description": "Token budget for decomposition inference"
        },
        "deadline_epoch": {
          "type": ["integer", "null"],
          "description": "Hard deadline epoch; null for no deadline"
        },
        "priority": {
          "type": "integer",
          "minimum": 0,
          "maximum": 100,
          "default": 50,
          "description": "Higher = more urgent"
        },
        "min_agent_credibility": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.5,
          "description": "Minimum PCVM credibility for assigned agent"
        },
        "allow_spanning": {
          "type": "boolean",
          "default": true,
          "description": "Whether children may span multiple loci"
        }
      },
      "required": ["max_depth", "decomposition_budget_ms",
                    "decomposition_token_limit"]
    },
    "decomposition_strategy": {
      "type": ["string", "null"],
      "enum": ["RECURSIVE", "PARALLEL", "SEQUENTIAL", "CONDITIONAL", null],
      "description": "Set by System 3 during decomposition; null before"
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
      },
      "description": "References to input data this intent needs"
    },
    "output_spec": {
      "type": "object",
      "properties": {
        "output_type": {
          "type": "string",
          "enum": ["PARCEL", "CLAIM", "METRIC", "NONE"]
        },
        "output_schema_ref": {
          "type": ["string", "null"],
          "description": "Reference to expected output schema"
        },
        "output_parcel_target": {
          "type": ["string", "null"],
          "description": "Target parcel for output (if PARCEL type)"
        }
      },
      "required": ["output_type"]
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_epoch": { "type": "integer" },
        "last_modified_epoch": { "type": "integer" },
        "tags": {
          "type": "array",
          "items": { "type": "string" }
        },
        "annotations": {
          "type": "object",
          "additionalProperties": { "type": "string" }
        }
      }
    }
  },
  "required": ["intent_id", "intent_type", "origin", "scope",
               "description", "success_criteria", "resource_bounds",
               "constraints", "output_spec"],

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
        "agent_id": { "type": "string" }
      },
      "required": ["wall_time_ms", "vector_clock", "epoch",
                    "locus_id", "agent_id"]
    },

    "ResourceBounds": {
      "type": "object",
      "properties": {
        "compute_tokens": {
          "type": "integer",
          "minimum": 0,
          "description": "Maximum compute tokens (additive resource)"
        },
        "wall_time_ms": {
          "type": "integer",
          "minimum": 0,
          "description": "Maximum wall-clock time (additive resource)"
        },
        "bandwidth_bytes": {
          "type": "integer",
          "minimum": 0,
          "description": "Maximum network bandwidth (shared resource)"
        },
        "iops": {
          "type": "integer",
          "minimum": 0,
          "description": "Maximum I/O operations per second (shared resource)"
        },
        "storage_bytes": {
          "type": "integer",
          "minimum": 0,
          "description": "Maximum storage consumption (additive resource)"
        },
        "stake_required": {
          "type": "number",
          "minimum": 0,
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
          "description": "Dot-path to an observable system state value"
        },
        "operator": {
          "type": "string",
          "enum": ["EQ", "NEQ", "GT", "GTE", "LT", "LTE",
                   "CONTAINS", "MATCHES", "EXISTS"]
        },
        "expected_value": {},
        "description": { "type": "string" }
      },
      "required": ["predicate_id", "observable", "operator",
                    "expected_value"]
    },

    "SuccessThreshold": {
      "type": "object",
      "properties": {
        "threshold_id": { "type": "string" },
        "metric": {
          "type": "string",
          "description": "Metric name to evaluate"
        },
        "operator": {
          "type": "string",
          "enum": ["GTE", "LTE"]
        },
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

### 5.2 Lifecycle State Machine

```
                    +----------+
                    | PROPOSED |
                    +----+-----+
                         |
            validate & admit (System 3)
                         |
                         v
                   +------------+
              +--->| DECOMPOSED |<----+
              |    +-----+------+     |
              |          |            |
              |   activate leaves     |
              |   (all children       |
              |    registered)        |
              |          |            |
              |          v            |
              |    +--------+         |
              |    | ACTIVE  |---------+
              |    +----+----+  partial failure
              |         |       triggers re-decomp
              |    execute &    (ACTIVE → DECOMPOSED)
              |    evaluate
              |    success
              |    criteria
              |         |
              |         v
              |   +-----------+
              |   | COMPLETED |
              |   +-----+-----+
              |         |
              |    GC after 100
              |    epochs
              |         |
              |         v
              |   +-----------+
              +---| DISSOLVED |
                  +-----------+
                   (terminal)
```

**State Transition Table**:

| From | To | Trigger | Conditions |
|---|---|---|---|
| PROPOSED | DECOMPOSED | System 3 completes decomposition | Valid decomposition plan; all children registered in ISR |
| PROPOSED | DISSOLVED | Proposal rejected or decomposition fails | Invalid intent, no capable agents, budget exhaustion |
| DECOMPOSED | ACTIVE | All children registered and at least one child activated | Leaf children assigned to agents; non-leaf children begin their own decomposition |
| DECOMPOSED | DISSOLVED | Parent dissolved or compensation triggered | Parent lifecycle change or failure cascade |
| ACTIVE | COMPLETED | Success criteria evaluated | All leaf descendants report results; criteria evaluated as SUCCESS, PARTIAL_SUCCESS, FAILURE, or TIMEOUT |
| ACTIVE | DECOMPOSED | Partial failure requires re-decomposition | Some children failed; parent re-enters decomposition to produce replacement children (special case) |
| ACTIVE | DISSOLVED | Compensation or parent dissolution | External compensation trigger or parent lifecycle change |
| COMPLETED | DISSOLVED | GC after retention period | 100 epochs after completion (configurable) |
| DISSOLVED | (none) | Terminal state | Entry removed after GC retention |

**Special Case: ACTIVE to DECOMPOSED**

When a child intent fails during execution and the parent's decomposition strategy supports partial recovery (e.g., PARALLEL with partial-success threshold), the parent transitions back to DECOMPOSED. System 3 then re-decomposes only the failed portion, producing replacement children while preserving the results of successful children.

```
function handle_partial_failure(parent_id: IntentId,
                                 failed_child_id: IntentId):
    parent = isr.get_intent(parent_id)
    children = isr.get_children(parent_id)

    completed = [c for c in children if c.lifecycle_state == COMPLETED
                 and c.result.outcome == SUCCESS]
    failed = [c for c in children if c.lifecycle_state == COMPLETED
              and c.result.outcome in (FAILURE, TIMEOUT)]

    if parent.decomposition_strategy == PARALLEL:
        success_ratio = len(completed) / len(children)
        if success_ratio >= parent.partial_success_threshold:
            // Enough children succeeded; parent completes
            complete_parent(parent_id, "PARTIAL_SUCCESS")
            return

    // Re-decompose: transition parent back to DECOMPOSED
    isr.transition_intent(parent_id, "DECOMPOSED",
                          reason="PARTIAL_FAILURE_REDECOMP")

    // Create replacement children for failed ones
    failed_scope = aggregate_scope(failed)
    replacement_intent = create_replacement_intent(
        parent, failed_scope
    )
    decompose_intent(replacement_intent, parent.current_depth + 1)
```

### 5.3 Intent Types

#### 5.3.1 GOAL

A high-level objective with success criteria but no specific execution instructions. Goals are always decomposed — they never reach leaf level.

```json
{
  "intent_id": "a1b2c3d4-...",
  "intent_type": "GOAL",
  "operation_class": null,
  "description": "Achieve 95% accuracy on domain X classification task",
  "success_criteria": {
    "criteria_type": "COMPOSITE",
    "thresholds": [
      {
        "threshold_id": "accuracy",
        "metric": "domain_x.classification.accuracy",
        "operator": "GTE",
        "value": 0.95
      }
    ],
    "temporal_bound": {
      "bound_type": "WITHIN_EPOCHS",
      "epoch_value": 100
    },
    "composition": "AND"
  }
}
```

#### 5.3.2 DIRECTIVE

A specific instruction to execute. Directives may decompose further or may be leaf intents depending on their complexity. Leaf directives map to a single operation class.

```json
{
  "intent_id": "e5f6g7h8-...",
  "intent_type": "DIRECTIVE",
  "operation_class": "B",
  "description": "Retrain local model on updated parcel data",
  "success_criteria": {
    "criteria_type": "PREDICATE",
    "predicates": [
      {
        "predicate_id": "model_updated",
        "observable": "parcel.model.version",
        "operator": "GT",
        "expected_value": 42
      }
    ]
  }
}
```

#### 5.3.3 QUERY

An information retrieval request. Queries are always M-class at leaf level (merge operations that read but do not mutate state).

```json
{
  "intent_id": "i9j0k1l2-...",
  "intent_type": "QUERY",
  "operation_class": "M",
  "description": "Retrieve current accuracy metrics for domain X across all loci",
  "success_criteria": {
    "criteria_type": "PREDICATE",
    "predicates": [
      {
        "predicate_id": "result_populated",
        "observable": "output.records_count",
        "operator": "GT",
        "expected_value": 0
      }
    ]
  },
  "output_spec": {
    "output_type": "PARCEL",
    "output_schema_ref": "https://atrahasis.org/schemas/metrics-report/v1"
  }
}
```

#### 5.3.4 OPTIMIZATION

A system self-improvement proposal originating from System 4. Optimizations go through the Adaptation Proposal Protocol before becoming intents.

```json
{
  "intent_id": "m3n4o5p6-...",
  "intent_type": "OPTIMIZATION",
  "operation_class": null,
  "description": "Rebalance agent distribution across loci to match projected demand",
  "success_criteria": {
    "criteria_type": "THRESHOLD",
    "thresholds": [
      {
        "threshold_id": "balance_ratio",
        "metric": "loci.agent_distribution.gini_coefficient",
        "operator": "LTE",
        "value": 0.15
      }
    ]
  },
  "scope": {
    "domain": "system_operations",
    "target_loci": ["*"],
    "affects_governance": false
  }
}
```

### 5.4 Success Criteria Language

The success criteria language provides four evaluation modes that can be composed.

#### 5.4.1 Predicate-Based

Boolean conditions over observable system state. Observables are addressed by dot-path notation.

```
Predicate := observable OPERATOR expected_value

Operators:
  EQ       — observable == expected_value
  NEQ      — observable != expected_value
  GT       — observable > expected_value
  GTE      — observable >= expected_value
  LT       — observable < expected_value
  LTE      — observable <= expected_value
  CONTAINS — observable (collection) contains expected_value
  MATCHES  — observable (string) matches expected_value (regex)
  EXISTS   — observable is non-null

Examples:
  parcel.model.version GT 42
  locus.agent_count GTE 10
  output.classification.label EQ "positive"
  agent.capabilities CONTAINS "inference"
  result.error_log EXISTS false
```

#### 5.4.2 Threshold-Based

Numeric metric meets a threshold. Used for quantitative goals.

```
Threshold := metric (GTE | LTE) value

Examples:
  domain_x.classification.accuracy GTE 0.95
  system.latency_p99_ms LTE 500
  locus.resource_utilization LTE 0.85
```

#### 5.4.3 Temporal

Bounds on when success must be achieved.

```
TemporalBound :=
  | WITHIN_EPOCHS n    — must complete within n epochs of activation
  | BEFORE_EPOCH e     — must complete before epoch e
  | AFTER_EPOCH e      — must not start before epoch e

Examples:
  WITHIN_EPOCHS 100    — complete within 100 epochs
  BEFORE_EPOCH 50000   — hard deadline at epoch 50000
```

#### 5.4.4 Composite

Combine sub-criteria with AND/OR.

```
Composite := (AND | OR) of [Predicate | Threshold | Temporal | Composite]

Example (AND):
  ALL of:
    - accuracy GTE 0.95
    - latency_p99 LTE 500ms
    - WITHIN_EPOCHS 100

Example (OR):
  ANY of:
    - accuracy GTE 0.98 (high bar, any timeline)
    - accuracy GTE 0.95 AND WITHIN_EPOCHS 50 (lower bar, faster)
```

**Evaluation Semantics**:
- AND: all sub-criteria must be true simultaneously at evaluation time.
- OR: at least one sub-criterion must be true.
- Temporal bounds are evaluated against the Clock Service's current epoch.
- Predicates are evaluated against the observable system state at evaluation time.
- Thresholds are evaluated against the most recent metric snapshot.
- Evaluation is performed by System 3 when all leaf descendants report results.

---

## 6. Formal Decomposition Algebra

### 6.1 Operation Class Decomposition Rules

The five C3 operation classes form a strict partial order that governs which classes may appear as children during intent decomposition.

**Operation Class Partial Order**:

```
    G  (Governance — constitutional consensus)
    |
    V  (Verification — cross-agent validation)
    |
    X  (Exclusive — single-agent exclusive access)
    |
    B  (Bounded — bounded local operations)
    |
    M  (Merge — read-only merge operations)
```

**Formal Decomposition Rules**:

Let `class(i)` denote the operation class of intent `i`, and `children(i)` the set of child intents produced by decomposing `i`.

```
Rule G-DECOMP:
  class(i) = G  ==>  for all c in children(i):
                        class(c) in {M, B, X, V, G}
  (Governance intents may decompose into any combination)

Rule V-DECOMP:
  class(i) = V  ==>  for all c in children(i):
                        class(c) in {M, B, X}
  (Verification cannot spawn governance or further verification)

Rule X-DECOMP:
  class(i) = X  ==>  for all c in children(i):
                        class(c) in {M, B}
  (Exclusive ops decompose into simpler, non-exclusive operations)

Rule B-DECOMP:
  class(i) = B  ==>  for all c in children(i):
                        class(c) in {M}
  (Bounded local ops decompose only into merge operations)

Rule M-TERMINAL:
  class(i) = M  ==>  children(i) = empty set
  (Merge operations are terminal — they cannot decompose further)
```

**Rationale for restrictions**:

- **V cannot spawn V**: Verification of verification creates infinite regress. A single V-class operation produces a verifiable result; if that result itself needs verification, the parent's parent handles it.
- **V cannot spawn G**: Verification is an operational check, not a governance action. If verification reveals a need for governance, it reports upward and the parent decides.
- **X cannot spawn X**: Exclusive access is non-composable. If an X-class operation needs to touch multiple exclusive resources, it must be decomposed into B/M operations with explicit sequencing.
- **B cannot spawn B**: Bounded local operations are already the simplest non-trivial unit. Further decomposition yields only M-class merge reads.

**Visual decomposition matrix**:

```
Parent \ Child |  M  |  B  |  X  |  V  |  G  |
---------------|-----|-----|-----|-----|-----|
      G        |  Y  |  Y  |  Y  |  Y  |  Y  |
      V        |  Y  |  Y  |  Y  |  N  |  N  |
      X        |  Y  |  Y  |  N  |  N  |  N  |
      B        |  Y  |  N  |  N  |  N  |  N  |
      M        | (terminal — no children)      |
```

### 6.2 Termination Proof Sketch

**Claim**: Every intent decomposition terminates in a finite number of steps.

**Proof sketch**:

Define a well-founded ordering on intents as a pair `(class_rank, remaining_depth)` where:

```
class_rank(M) = 0
class_rank(B) = 1
class_rank(X) = 2
class_rank(V) = 3
class_rank(G) = 4

remaining_depth(i) = i.constraints.max_depth - current_depth(i)
```

Define the lexicographic order on pairs: `(r1, d1) < (r2, d2)` iff `r1 < r2`, or `r1 == r2` and `d1 < d2`.

**Step 1**: Show that every decomposition step produces children strictly less than the parent in this ordering.

Case analysis by parent class:

- `class(parent) = G`: Children have `class(c) in {M,B,X,V,G}`.
  - If `class(c) < G`: `class_rank(c) < class_rank(parent)`. Strictly less by first component.
  - If `class(c) = G`: `class_rank(c) = class_rank(parent)`, but `remaining_depth(c) = remaining_depth(parent) - 1`. Strictly less by second component.

- `class(parent) = V`: Children have `class(c) in {M,B,X}`. `class_rank(c) < class_rank(V) = 3`. Strictly less by first component.

- `class(parent) = X`: Children have `class(c) in {M,B}`. `class_rank(c) < class_rank(X) = 2`. Strictly less by first component.

- `class(parent) = B`: Children have `class(c) in {M}`. `class_rank(c) = 0 < class_rank(B) = 1`. Strictly less by first component.

- `class(parent) = M`: No children. Decomposition terminates immediately.

**Step 2**: The ordering is well-founded.

- `class_rank` ranges over `{0, 1, 2, 3, 4}` — finite.
- `remaining_depth` ranges over `{0, 1, ..., max_depth}` — finite.
- The lexicographic product of two finite well-ordered sets is well-founded.

**Step 3**: By the well-ordering principle, every strictly descending chain in a well-founded order is finite. Therefore, every decomposition chain terminates. QED.

**Practical bound**: Maximum decomposition tree size is bounded by:

```
max_tree_size <= sum_{d=0}^{max_depth} (max_branching_factor ^ d)
             = (max_branching_factor^(max_depth+1) - 1) /
               (max_branching_factor - 1)
```

With default `max_depth = 10` and a practical branching factor of 5, this yields at most `(5^11 - 1) / 4 = 12,207,031` nodes. In practice, trees are far smaller because class descent reduces depth quickly.

### 6.3 Cycle-Freedom Proof Sketch

**Claim**: No decomposition can produce a cycle (intent A is an ancestor of itself).

**Proof sketch**:

**Assume for contradiction** that a cycle exists: there is a sequence of intents `i_0, i_1, ..., i_k` where `i_{j+1} in children(i_j)` and `i_k = i_0`.

By the decomposition rules (Section 6.1), for each step in the sequence:

```
class_rank(i_{j+1}) <= class_rank(i_j)
```

And when `class_rank(i_{j+1}) = class_rank(i_j)` (which can only happen when `class(i_j) = G` and `class(i_{j+1}) = G`):

```
remaining_depth(i_{j+1}) = remaining_depth(i_j) - 1
```

Since `remaining_depth` is a non-negative integer that decreases by 1 on same-class edges, and class rank is non-increasing, the pair `(class_rank, remaining_depth)` is strictly decreasing along every edge (as proved in Section 6.2).

If `i_k = i_0`, then `(class_rank(i_k), remaining_depth(i_k)) = (class_rank(i_0), remaining_depth(i_0))`. But we just showed the pair is strictly decreasing along every edge. A strictly decreasing sequence cannot return to its starting value. **Contradiction**.

Therefore, no cycle exists. QED.

**Additional structural guarantee**: Each intent's `intent_id` is a UUID generated at creation time. The decomposition engine never reuses an `intent_id`. Even if the same logical decomposition pattern recurs (via memoization), the child intents receive fresh UUIDs.

### 6.4 Resource Bound Preservation

**Invariant**: No decomposition step allocates more resources to children than the parent possesses.

**Additive resources** (compute_tokens, wall_time_ms, storage_bytes):

```
For resource r classified as ADDITIVE:
  sum(child.resource_bounds.r for child in children) <=
      parent.resource_bounds.r - decomposition_overhead.r
```

The `decomposition_overhead` accounts for the resources consumed by the decomposition process itself (inference tokens, wall-clock time for decomposition computation).

**Shared resources** (bandwidth_bytes, iops):

```
For resource r classified as SHARED:
  max(child.resource_bounds.r for child in children) <=
      parent.resource_bounds.r
```

Shared resources are not divided among children — each child may use up to the parent's bound, but they contend for the same pool.

**Formal resource partition validation**:

```
function validate_resource_partition(
    parent_bounds: ResourceBounds,
    children: List[IntentQuantum]
) -> ValidationResult:

    // Decomposition overhead (configurable per locus)
    overhead = ResourceBounds(
        compute_tokens = DECOMP_OVERHEAD_TOKENS,   // default: 100
        wall_time_ms   = DECOMP_OVERHEAD_MS,       // default: 500
        storage_bytes  = 0,
        bandwidth_bytes = 0,
        iops           = 0
    )

    // Validate additive resources
    for field in ADDITIVE_FIELDS:  // [compute_tokens, wall_time_ms, storage_bytes]
        child_sum = sum(getattr(c.resource_bounds, field) for c in children)
        parent_available = getattr(parent_bounds, field) - getattr(overhead, field)

        if child_sum > parent_available:
            return ValidationResult.failure(
                resource=field,
                parent_available=parent_available,
                children_requested=child_sum,
                deficit=child_sum - parent_available
            )

    // Validate shared resources
    for field in SHARED_FIELDS:  // [bandwidth_bytes, iops]
        child_max = max(getattr(c.resource_bounds, field) for c in children)
        parent_available = getattr(parent_bounds, field)

        if child_max > parent_available:
            return ValidationResult.failure(
                resource=field,
                parent_available=parent_available,
                child_max_requested=child_max,
                deficit=child_max - parent_available
            )

    return ValidationResult.success()
```

**Resource return on completion**:

```
function return_unused_resources(child: IntentQuantum):
    for field in ADDITIVE_FIELDS:
        allocated = getattr(child.resource_accounting.allocated, field)
        consumed  = getattr(child.resource_accounting.consumed, field)
        returned  = allocated - consumed

        if returned > 0:
            child.resource_accounting.returned_to_parent[field] = returned
            // Parent's Resource Optimizer picks up this surplus
```

### 6.5 Decomposition Budget Mechanics

Decomposition itself is a computational process that consumes resources. Without explicit budgets, a malicious or poorly constructed intent could cause unbounded decomposition inference.

#### 6.5.1 Wall-Clock Limit

```
constraint: decomposition_budget_ms
default:    5000 (5 seconds)
range:      [100, 60000]

Behavior:
  - Timer starts when decompose_intent() is called
  - Timer is checked at every recursive call
  - If elapsed > budget: DECOMPOSITION_BUDGET_EXHAUSTED
```

#### 6.5.2 Computation Limit

```
constraint: decomposition_token_limit
default:    10000 tokens
range:      [100, 1000000]

Behavior:
  - Token counter increments with each inference step during
    strategy selection and rule application
  - If consumed > limit: TOKEN_BUDGET_EXHAUSTED
```

#### 6.5.3 Failure on Budget Exhaustion

When either budget is exhausted, decomposition fails cleanly:

```
function handle_decomposition_budget_failure(
    intent_id: IntentId,
    reason: string,
    partial_children: List[IntentId]
):
    // 1. Dissolve all partially-created children
    for child_id in partial_children:
        isr.transition_intent(child_id, "DISSOLVED",
                              reason="PARENT_DECOMP_BUDGET_EXHAUSTED")

    // 2. Emit explicit failure event
    event = DecompositionFailedEvent(
        intent_id=intent_id,
        reason=reason,
        children_dissolved=len(partial_children),
        epoch=current_epoch()
    )
    emit_event(event)

    // 3. Transition intent to COMPLETED(FAILURE)
    isr.transition_intent(intent_id, "COMPLETED",
                          reason=reason)
    isr.set_result(intent_id, IntentResult(
        outcome="FAILURE",
        success_criteria_evaluation={},
        completion_epoch=current_epoch()
    ))

    // 4. Notify parent (if any)
    if isr.get_intent(intent_id).parent_intent_id != null:
        notify_parent_child_failed(
            isr.get_intent(intent_id).parent_intent_id,
            intent_id,
            reason
        )
```

### 6.6 Memoization Strategy

Decomposition memoization prevents redundant computation when similar intents arrive repeatedly.

#### 6.6.1 Cache Key

```
cache_key = (intent_type, scope_hash, context_hash)

where:
  intent_type  = GOAL | DIRECTIVE | QUERY | OPTIMIZATION
  scope_hash   = hash(scope.domain, scope.target_loci, scope.flags)
  context_hash = hash(relevant_system_state_at_decomposition_time)
```

**Context hash components**:

```
function context_hash(intent: IntentQuantum) -> Hash:
    relevant_state = {
        "agent_capabilities": agent_registry.get_capability_summary(
            intent.scope.target_loci
        ),
        "locus_topology": c3.get_topology_hash(intent.scope.target_loci),
        "active_policies": system5.get_active_policy_hash(),
        "resource_availability": get_resource_snapshot(
            intent.scope.target_loci
        )
    }
    return sha256(canonical_json(relevant_state))
```

#### 6.6.2 Cache Hit Behavior

On cache hit, the prior decomposition plan is not blindly reused. A delta is computed between the cached state snapshot and the current state:

```
function apply_cached_plan(
    cached: CachedDecomposition,
    intent: IntentQuantum
) -> DecompositionResult:

    delta = compute_state_delta(cached.state_snapshot, current_state())

    if delta.is_major():
        // State has changed too much; invalidate cache entry
        memo_cache.invalidate(cached.key)
        return null  // Force fresh decomposition

    if delta.is_minor():
        // Apply delta adjustments to cached plan
        plan = cached.plan.clone()

        // Adjust agent assignments (agents may have departed/arrived)
        for leaf in plan.leaves():
            if not agent_registry.agent_available(leaf.assigned_agent_id):
                new_agent = select_agent(
                    leaf.operation_class, leaf.scope.domain
                )
                if new_agent == null:
                    memo_cache.invalidate(cached.key)
                    return null
                leaf.assigned_agent_id = new_agent

        // Adjust resource bounds (availability may have changed)
        for node in plan.all_nodes():
            adjust_resource_bounds(node, delta.resource_changes)

        return DecompositionResult.success(plan, source="CACHE_HIT_DELTA")

    // delta.is_none(): exact match, reuse as-is
    return DecompositionResult.success(cached.plan, source="CACHE_HIT_EXACT")
```

**Delta classification**:

| Delta Type | Criteria | Action |
|---|---|---|
| NONE | context_hash unchanged | Reuse plan exactly |
| MINOR | < 20% of agents changed; topology unchanged; policies unchanged | Delta-adjust agent assignments and resource bounds |
| MAJOR | >= 20% of agents changed, OR topology changed, OR policies changed | Invalidate cache; recompute |

#### 6.6.3 TTL and Invalidation

```
Cache Configuration:
  max_entries:        10000
  default_ttl_epochs: 50
  eviction_policy:    LRU (Least Recently Used)

Invalidation Triggers:
  1. agent_registry_change:
     - Agent departure or arrival in a target locus
     - Triggers MINOR delta on next access
  2. locus_topology_change:
     - C3 tidal rebalancing changes locus structure
     - Triggers MAJOR invalidation for all plans targeting affected loci
  3. system_5_policy_change:
     - G-class governance changes active policies
     - Triggers MAJOR invalidation for all cached plans
  4. operation_class_rule_change:
     - Decomposition rules themselves change (rare, requires G-class)
     - Full cache flush
```

**Cache entry structure**:

```json
{
  "$schema": "https://atrahasis.org/rif/memo-cache-entry/v1",
  "type": "object",
  "properties": {
    "cache_key": {
      "type": "object",
      "properties": {
        "intent_type": { "type": "string" },
        "scope_hash": { "type": "string", "format": "sha256" },
        "context_hash": { "type": "string", "format": "sha256" }
      },
      "required": ["intent_type", "scope_hash", "context_hash"]
    },
    "plan": {
      "type": "object",
      "description": "Serialized DecompositionPlan"
    },
    "state_snapshot": {
      "type": "object",
      "description": "System state at decomposition time (for delta computation)"
    },
    "created_epoch": { "type": "integer" },
    "ttl_epoch": { "type": "integer" },
    "hit_count": { "type": "integer", "minimum": 0 },
    "last_hit_epoch": { "type": "integer" },
    "delta_adjustments_applied": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of times this entry was delta-adjusted rather than recomputed"
    }
  },
  "required": ["cache_key", "plan", "state_snapshot",
               "created_epoch", "ttl_epoch", "hit_count",
               "last_hit_epoch"]
}
```

---

*End of Part 1 (Sections 1-6). Part 2 continues with Sections 7-14: Cross-Locus Intent Coordination, Settlement Protocol, Tidal Integration, ASV/PCVM/EMA Integration, Security Model, Operational Parameters, Migration Path, and Appendices.*